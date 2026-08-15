# O LAÇO DE ESCRITA 02 — os dois achados viram cura

**15/08/2026.** Sucessor direto da §8 de
[O-LACO-DE-ESCRITA-01](2026-08-15-O-LACO-DE-ESCRITA-01-o-suspeito-que-sobrou.md),
que nomeou dois defeitos por leitura de código e não pôde tocá-los (`src/` era
de outro agente naquela janela). Esta página é o que aconteceu com eles.

**Nada aqui foi medido no aparelho.** A única medição desta página é uma
CONTAGEM NO JOURNAL, e ela deu ZERO — está dita na cara na §2.

---

## 1. Defeito A — o `_bt_seq` sem lock: CONFIRMADO e curado

`writeReport`, em `core/backend_pydualsense.py`, fazia um *read-modify-write* de
`self._bt_seq` sem exclusão mútua:

```python
stamped = list(outReport)
rep.stamp_bt_seq(stamped, self._bt_seq)     # LÊ
self._bt_seq = (self._bt_seq + 1) & 0x0F    # INCREMENTA
self.device.write(bytes(stamped))           # ENTREGA
```

E há mais de uma thread chamando `writeReport` no MESMO handle:

| escritor | thread | transporte |
|---|---|---|
| `sendReport` (regime) | a `report_thread` daquele handle | cabo e rádio |
| `reescrever_lightbar_por_hidraw` | IPC / executor do poll loop | **só rádio** |
| `_pintar_por_hidraw_bt` | idem | **só rádio** |
| `core/lightbar_reset.py` | idem | **só rádio** |

Duas threads podiam ler o mesmo `_bt_seq` e carimbar o MESMO `seq` em dois
quadros. **O firmware descarta o quadro fora de sequência e o nosso log diz
"escrito"** — o sintoma que esta casa já pagou uma vez e deixou escrito dentro
do próprio `reescrever_lightbar_por_hidraw`. É defeito **só do rádio**: o `0x02`
do cabo não tem `seq` nem CRC no envelope.

### A cura

Um `threading.Lock` **por handle** (`_write_lock`, criado no `__init__`),
tomado em `writeReport` em volta do **par carimbo+entrega** — não só do
contador. Serializar apenas o incremento daria `seq` distintos entregues **fora
de ordem**, e report fora de sequência é exatamente o que o firmware joga fora:
trocaria um defeito por outro com a mesma cara.

### Por que não trava

- O lock é **por handle**. Um `hid_write` pendurado num controle não cala os
  outros três da mesa.
- O corpo do lock não chama nada do backend: **não toma `_io_lock`**, não chama
  de volta para o `PyDualSenseController`, não é reentrante. Não existe caminho
  que pegue `_write_lock` e depois `_io_lock` — a única ordem possível é
  `_io_lock` → `_write_lock`, e **nem essa acontece hoje**: os três escritores
  avulsos soltam o `_io_lock` ANTES do I/O, de propósito e com docstring
  dizendo por quê.
- O tempo de posse é o de um `hid_write`, que o kernel **já serializava** no
  mesmo descritor. O lock só antecipa a espera para o espaço do usuário.

---

## 2. Defeito B — o `TypeError` da leitura vazia: CONFIRMADO, e sem
   evidência de ter disparado

O handle é aberto sem `blocking=True`, então `hidapi.Device.read` devolve
`None` quando não há dado (`rv == 0`). O `readInput` do upstream começa com
`list(inReport)`, o que levanta `TypeError` — e o laço só capturava `OSError` e
`AttributeError`. A `report_thread` morria e **o controle ficava sem saída**
(sem rumble, sem lightbar, sem gatilho), sem linha estruturada no journal e sem
`connected = False`. O `connect()` do `reconnect_loop` não reabre handle de
controle que continua enumerado, então nada o ressuscitava.

### A medição: o journal não tem nada

`journalctl --user -u hefesto-dualsense4unix.service --since "-7 days"` — 67 mil
linhas — e o journal do usuário inteiro em **30 dias**:

| procurado | achado |
|---|---|
| `Exception in thread` (o `threading.excepthook` padrão, que vai para o stderr e daí para o journal) | **0** |
| `object is not iterable` | **0** |
| `sendReport` em traceback | **0** |
| `report_thread_nao_encerrou` (o `close()`, outro defeito, já curado) | 6 |

**A pré-condição nunca disparou nesta máquina.** E há um detalhe que corrige a
LACO-DE-ESCRITA-01: a morte **não** seria totalmente calada — o
`threading.excepthook` padrão imprime traceback no stderr, e a unit não
sobrescreve `StandardOutput`, então ele chegaria ao journal. O que era calado é
o que importa para o produto: **sem log estruturado, sem `connected = False`,
sem ressurreição, e com a tela dela jurando que o controle está conectado.**

Isto **rebaixa a urgência** e não muda o veredito sobre o defeito: a
pré-condição é estreita (~2 s de silêncio do aparelho com a fila do `hidraw`
cheia), impossível no cabo, possível no rádio.

### A cura, e por que não é capturar a exceção

Capturar o `TypeError` trocaria uma morte calada por um **laço calado**, e
continuaria tratando como acidente uma resposta que a API **promete**. A cura é
parar de passar `None` adiante:

- `read` devolveu `None` → não há entrada para interpretar; o ciclo **pula a
  metade de ENTRADA e segue direto para a metade de SAÍDA**. O controle continua
  tendo saída durante o silêncio, que é o desfecho certo — e o INPUT do produto
  vem do evdev, não daqui.
- O silêncio deixa **rastro**: `report_thread_entrada_muda` (warning) **uma vez
  por episódio**, quando ele passa de `LEITURA_VAZIA_AVISO_SEC` = 1,0 s, e
  `report_thread_entrada_voltou` (info) quando a entrada fala de novo. Uma por
  episódio e não por ciclo: com a mesa cheia são ~31 ciclos por segundo, e um
  aviso por ciclo afogaria o journal justo quando ele mais precisa ser lido.

E uma rede, para a CATEGORIA e não para o caso: `except Exception` no fim do
laço agora registra `report_thread_morreu_por_excecao` (error, com tipo e
mensagem) e marca `connected = False` antes de sair. O desfecho é o mesmo do
`OSError` — **de propósito**: seguir o laço depois de uma exceção que não se
sabe nomear é girar sem saber em quê, e este laço escreve no aparelho dela. O
que muda é que fica escrito, e `connected` para de mentir.

---

## 3. A mordida — arrancada, rodada, devolvida

Testes em `tests/unit/test_laco_de_escrita_02.py` (8 verdes). Cada cura foi
arrancada, o teste rodou, e a reprovação está transcrita:

| arrancada | o que reprovou |
|---|---|
| `with self._write_lock:` fora de `writeReport` | `seq repetido entre escritores: [0, 0, 0, 0]` — as quatro threads carimbaram zero |
| lock **só no contador**, `write` fora | `o write do rádio saiu fora do lock` (asserção estrutural, `Lock.locked()` de dentro do `write`) |
| `self._write_lock = threading.Lock()` fora do `__init__` | dois handles compartilhando o lock de classe |
| a guarda `if in_report is None` (o código de antes) | `a thread não chegou ao fim dos ciclos: 0 == 4`, com `TypeError: 'NoneType' object is not iterable` no log |
| a rede `except Exception` | `ValueError` escapando de `sendReport` |
| o aviso passa a sair **a cada ciclo** | `assert 4 == 1` |
| o silêncio **sem rastro nenhum** | `assert 0 == 1` |

O dublê de `readInput` reproduz **literalmente** a primeira linha do upstream
(`list(inReport)[1:]`) — é ali que o `None` vira `TypeError`, e um dublê
complacente teria feito a arrancada passar.

---

## 4. O QUE FICOU PARA ELA — a pergunta que não decidi

**Handle cuja `report_thread` morreu não volta sozinho, e isso vale para o
`OSError` de sempre, não só para o defeito novo.** Quando a thread sai
(`connected = False`), o handle **continua em `self._handles`**: o `connect()`
do `reconnect_loop` só abre o que falta e fecha o que sumiu — um controle que
continua enumerado é "já presente" e fica intacto, sem thread e sem saída, até
alguém desplugar ou re-parear. `is_connected()` e `describe_controllers` passam
a dizer "desconectado" (é o que `connected` significa), então **a tela dela
mostra desconectado num controle que está lá e continua mandando input pelo
evdev**.

Curar isso é mudar comportamento de produto — o reconciliador passaria a
**derrubar e recriar** um handle vivo — e recriar handle tem preço medido nesta
casa: a adoção derruba o claim da lightbar no firmware por BT
(LIGHTBAR-BT-RESET-01) e a janela de ~3,4 s do `0x08` é o
LIGHTBAR-BT-CULPADO-01. **Não decidi por ela.** A pergunta, em uma linha:

> *Quando a thread de saída de um controle morre mas o controle continua
> plugado, o Hefesto deve derrubar e reabrir o handle sozinho — pagando o risco
> da adoção na lightbar por rádio —, ou deve deixar como está e apenas dizer no
> journal e na tela que aquele controle perdeu a saída?*

Enquanto ela não responde, o produto faz o segundo: diz. Que é estritamente
melhor do que antes, quando não dizia.
