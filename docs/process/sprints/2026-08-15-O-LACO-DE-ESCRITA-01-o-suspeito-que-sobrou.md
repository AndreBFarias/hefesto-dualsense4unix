# O LAÇO DE ESCRITA 01 — o suspeito que sobrou

**15/08/2026.** Análise estática, sem tocar o aparelho. O produto desta página é
uma hipótese falseável e o desenho do ensaio que a testa — não uma medição.

**Nada aqui foi medido hoje.** Onde há número, ele vem do fonte lido ou de
ensaio anterior, e a procedência está dita na própria linha.

---

## 0. Por que esta página existe

O E-6 de hoje derrubou a suspeita de 10/08. A pré-condição física existe — o
`btusb` e os dois controles do cabo penduram no mesmo `0000:0c:00.3` (E-1) —,
mas a escada de carga não achou dose-resposta: a variação medida foi de **+1,0
Hz** e **−2,6 Hz** contra dispersão de **11,9 Hz** e **43,7 Hz**. Queda menor
que a própria dispersão não é dose-resposta.

O bruto está em
[`docs/data/ensaios-brutos/2026-08-15-E5-E6-microfone_no_cabo.txt`](../../data/ensaios-brutos/2026-08-15-E5-E6-microfone_no_cabo.txt);
a linha do mapa é `combinacao.adaptador_no_mesmo_controlador@dualsense` em
[`docs/data/mapa-controles.csv`](../../data/mapa-controles.csv), e ela já diz o
limite na cara:

> LIMITE DA CARGA, dito na cara: o E-6 carregou o controlador com CAPTURA DE
> MICROFONE USB (...). Isso NÃO é o laço de `sendReport` a plena carga, que é o
> mecanismo que o defeito de 10/08 acusa.

O ensaio nomeou o próprio sucessor. A carga do E-6 foi tráfego de **entrada de
terceiros**; o laço de escrita do Hefesto nunca foi a variável manipulada.
Esta página lê esse laço.

**Aviso de endereço:** os `arquivo:linha` abaixo foram conferidos em 15/08/2026
com `src/` **em movimento** (outro agente edita a mesma árvore). Cada citação
traz o **nome do símbolo** junto, que é o que não apodrece.

---

## 1. A cadência real de escrita

### 1.1 O fato que muda toda a aritmética: a leitura NÃO bloqueia

O laço de saída é `_PinnedPyDualSense.sendReport`
(`src/hefesto_dualsense4unix/core/backend_pydualsense.py:570`), e ele começa
com `self.device.read(self.input_report_length)`. Parece um laço governado pelo
aparelho. Não é.

O handle é aberto por `_pydualsense__find_device`
(`core/backend_pydualsense.py:565`) com `hidapi.Device(path=...)` — **sem**
`blocking=True`. E o construtor do `hidapi` faz
`hid_set_nonblocking(self._device, 1)` sempre que `blocking` é falso
(`.venv/.../hidapi.py:257-258`, fora da árvore). A leitura retorna na hora, com
dado ou com `None`.

**Consequência:** a cadência do laço não é a taxa do controle. É o `time.sleep`
do fim do ciclo, e só ele.

### 1.2 O teto por controle, e como ele escala

O throttle é por instância e recalculado no fim de `connect()`
(`core/backend_pydualsense.py:1735-1740`):

```python
n = max(1, len(self._handles))
throttle = min(REPORT_THREAD_THROTTLE_SEC * n, REPORT_THREAD_THROTTLE_MAX_SEC)
```

com `REPORT_THREAD_THROTTLE_SEC = 0,008` s (`:214`, sobrescrevível por
`HEFESTO_DUALSENSE4UNIX_REPORT_THROTTLE_SEC`) e
`REPORT_THREAD_THROTTLE_MAX_SEC = 0,032` s (`:222`).

| controles na mesa | throttle | teto do laço **por controle** | agregado |
|---|---|---|---|
| 1 | 0,008 s | 125 Hz | 125 Hz |
| 2 | 0,016 s | 62,5 Hz | 125 Hz |
| 3 | 0,024 s | 41,7 Hz | 125 Hz |
| **4 (a mesa dela)** | **0,032 s** | **31,25 Hz** | **125 Hz** |
| 5 | 0,032 s (teto) | 31,25 Hz | 156 Hz |

**O agregado é constante em 125 Hz até quatro controles.** Isso é desenho, não
acidente: o `n` multiplica o sono exatamente para que a soma não cresça. A
propriedade morre no quinto controle, quando o `min` passa a morder — e a mesa
dela tem quatro, ou seja, ela vive **no último ponto em que a garantia vale**.
Há teste que morde isso:
`tests/unit/test_paridade_transporte_mesa_de_dois.py::test_a_mesa_cheia_nao_passa_do_teto`.

### 1.3 Mas o teto do laço não é a taxa de escrita

Dentro do laço, a escrita passa por três portões (`sendReport`, `:587-649`):

1. **`_output_muted`** — em Modo Nativo, **zero** escritas. O jogo é o dono.
2. **dedup** — `mudou = out != self._last_out_report`. Report que não mudou não
   vai ao fio.
3. **keepalive limitado** —
   `mudou or (vencido and (dono_do_rumble or confirmando))`, com
   `vencido = (now - _last_write_at) >= OUT_REPORT_KEEPALIVE_SEC` (0,5 s, `:229`)
   e `confirmando = (now - _last_change_at) < OUT_REPORT_KEEPALIVE_CONFIRMACAO_SEC`
   (2,0 s, `:240`).

Daí sai a taxa de escrita **real**, por controle:

| regime | escritas/s por controle |
|---|---|
| ocioso, mais de 2 s sem mudança, sem rumble nosso | **0** |
| nos 2 s seguintes a qualquer mudança | até **2** (≈4 reconfirmações) |
| rumble FIXADO pela aba Rumble (`_rumble_active`) | **2**, indefinidamente |
| rumble do jogo variando | `min(teto do laço, 60)` → **31,25** com 4 controles |
| Modo Nativo | **0** |

O `reassert_rumble` do poll loop (`daemon/subsystems/rumble.py:228`, chamado a
cada 0,200 s em `daemon/lifecycle.py:3953`) **não** é uma escrita: ele reescreve
o mesmo par nos motores do backend, o report não muda, e o dedup o engole. Quem
escreve é o keepalive de 2 Hz, porque `dono_do_rumble` está ligado.

**O ocioso é ocioso de verdade.** Confirmei os três candidatos a "reconciliador
que escreve sozinho" e nenhum escreve em tique quieto:
`_sync_identity_registry` (`lifecycle.py:3249`) só lê `describe_controllers`;
`coop.sync()` (`daemon/subsystems/coop.py:312`) sai cedo pelo portão
`self._watch.poll()`; e `read_state` (`backend_pydualsense.py:2252`) lê estado
em cache. O único periódico que alcança o fio é o `connect()` do
`reconnect_loop` a cada 30 s (`daemon/connection.py:43`), que pode reescrever
LED por sysfs.

Isso importa para o ensaio: **a linha de base do E-6 é uma linha de base de zero
escritas nossas.** O 359 Hz e o 203 Hz dos dois do rádio, e as dispersões de
11,9 e 43,7 Hz, são propriedade do rádio — não do nosso laço.

### 1.4 Fan-out: onde existe e onde não existe

**Não há fan-out no laço.** Cada handle tem a sua `report_thread` e escreve só
no próprio fd. Quatro controles são quatro laços, não dezesseis escritas.

**Há fan-out no gesto.** `_for_each` e `_for_each_com_key`
(`backend_pydualsense.py:2337` e `:2380`) resolvem o alvo e, **sem alvo**,
aplicam em TODOS os handles. Uma ação da GUI, uma ativação de perfil ou um
`set_rumble` sem dono (`:2916`) muda o estado dos quatro de uma vez — e os
quatro laços escrevem no ciclo seguinte, em rajada. Com 4 controles isso é uma
rajada de 4 reports, dois deles de 78 bytes no ar.

**E há um fan-out por acidente que merece linha:** em `apply_game_rumble`
(`daemon/subsystems/gamepad.py:993-1002`), se o `target_uniq` não casar nenhum
handle, o código cai no broadcast histórico — o rumble de UM jogador vira
escrita nos QUATRO controles. Está documentado no docstring como limitação
conhecida; sob carga de jogo, é a diferença entre 31 escritas/s num controle e
31 escritas/s em quatro.

---

## 2. Serialização: quem escreve no mesmo descritor

**Não há lock nenhum no caminho de escrita.** O `_io_lock`
(`backend_pydualsense.py:1182`) protege o mapa de handles e o estado desejado, e
os dois `_for_each` **soltam o lock de propósito** antes do I/O (o docstring de
`_for_each` diz: *"faz o HID I/O fora da seção crítica"*). Isso é certo para não
segurar o lock durante um `write` que pode pendurar — mas deixa o fd sem
serialização.

Escrevem no MESMO fd, de threads diferentes:

| escritor | thread | quando |
|---|---|---|
| `sendReport` → `writeReport` (`:647`) | a `report_thread` daquele handle | em regime |
| `_pintar_por_hidraw_bt` (`:2738`) | a thread do chamador (IPC/executor do poll loop) | por ação de perfil/hotplug, **só rádio** |
| `reescrever_lightbar_por_hidraw` (`:2517`) | idem | no gatilho de conexão, **só rádio** |
| `core/lightbar_reset.py:74-79` | idem | no connect BT |

### ACHADO — a corrida do `_bt_seq`

`writeReport` (`backend_pydualsense.py:1018-1033`) faz, **sem lock**:

```python
stamped = list(outReport)
rep.stamp_bt_seq(stamped, self._bt_seq)
self._bt_seq = (self._bt_seq + 1) & 0x0F
self.device.write(bytes(stamped))
```

Três coisas de uma vez: um *read-modify-write* de `self._bt_seq` sem
exclusão mútua, e o `write` fora de qualquer ordenação. Duas threads podem
carimbar o MESMO `seq` ou trocar a ordem de chegada.

E o preço está escrito pela própria casa, três telas abaixo, em
`reescrever_lightbar_por_hidraw` (`:2543-2545`):

> Escrever cru no `device` com seq 0 já matou uma cura desta casa uma vez — o
> firmware descarta o report fora de sequência e o log diz "escrito" com a barra
> apagada.

Ou seja: **o sintoma desta corrida é exatamente o que a casa já pagou** — a
escrita que o log jura ter feito e o aparelho descartou. No cabo a corrida é
inócua (o `0x02` não tem `seq` nem CRC; o pior caso é ordem trocada entre dois
reports idempotentes). **A assimetria é do rádio, e só dele.**

Não estou consertando: `src/` é território de outro agente nesta janela. Fica
registrado como achado, com a mordida sugerida na §7.

---

## 3. Quando a escrita demora ou falha

**Não há retry. Não há backoff. Não há fila.** Isso é uma virtude aqui, e vale
dizer por quê: não existe buffer que cresça, então uma escrita lenta não vira
uma avalanche depois. O que existe é pior de outro jeito.

- **`hid_write` que falha** levanta `IOError` (que é `OSError`). Em
  `sendReport` (`:653-655`) isso é `self.connected = False; break` — a
  `report_thread` **morre** e aquele controle fica sem saída até o próximo
  `connect()` do `reconnect_loop` (até 30 s, `connection.py:43`).
- **`hid_write` que demora** não tem teto: o laço inteiro daquele handle para
  enquanto a chamada não volta. Não afeta os outros handles (threads
  independentes), mas o `close()` já pagou esse preço uma vez — é o
  QUEDA-QUE-PENDURA-01, documentado em `:660-697`, com 90 s de SIGKILL no
  journal dela.
- **Escrita avulsa que levanta** é engolida com `logger.debug`
  (`_pintar_por_hidraw_bt`) ou `logger.warning` (`_for_each`), e o laço segue.

### ACHADO — o `TypeError` que ninguém pega

`hidapi.Device.read` devolve **`None`** quando não há dado
(`.venv/.../hidapi.py:310-311`, fora da árvore). O `readInput` do upstream faz `list(inReport)`, o que levanta
`TypeError` — e `sendReport` só captura `OSError` e `AttributeError`
(`:653-658`). **`TypeError` não é capturado por ninguém.**

A thread morre em silêncio: sem log, sem `connected = False`, sem evento. O
controle continua entregando input (que vem do evdev, não daqui) e **para de
receber saída para sempre**. É a forma exata do defeito que a memória desta casa
chama de *"o sintoma é a AUSÊNCIA de dado"*.

**Sendo honesto sobre a pré-condição, que é estreita:** a fila de entrada do
`hidraw` é por descritor aberto, o laço consome **um** report por ciclo (31,25/s
com a mesa cheia) e o aparelho entrega 200-360/s. A fila vive **cheia**. Para o
`read` devolver `None` o aparelho precisa parar por tempo suficiente para drenar
a fila inteira — ordem de **2 segundos** de silêncio, com a mesa cheia. No cabo,
a 250,0 Hz com dispersão 0,0, isso não acontece. **No rádio, acontece.**

Corolário gratuito e desconfortável: como a fila vive cheia, tudo o que o laço
lê do aparelho — bateria, `status[1]` de áudio, transporte — está atrasado por
até o tamanho da fila. **Com quatro controles, o daemon enxerga um aparelho de
~2 segundos atrás.** Isso não é o dano ao rádio, mas é dívida medida, e as
specs são a memória externa dela.

---

## 4. O keepalive: ainda existe, e com que período

**Existe.** `OUT_REPORT_KEEPALIVE_SEC = 0,5` s continua lá
(`backend_pydualsense.py:229`) — o mesmo 0,5 s da dose-resposta de 11/08.

**Mas não é mais perpétuo**, e é isso que a cura RUMBLE-SEM-DONO-01 fez. Ele só
dispara com `dono_do_rumble` (rumble nosso ativo) **ou** `confirmando` (menos de
`OUT_REPORT_KEEPALIVE_CONFIRMACAO_SEC = 2,0` s desde a última mudança real). Sem
rumble nosso e com a mesa parada, passados 2 segundos, **o keepalive cala**.

Confirmei o que mais me preocupava: se algum reconciliador mudasse o report uma
vez a cada 2 s, `confirmando` ficaria verdadeiro para sempre e o keepalive
perpétuo voltaria pela porta dos fundos — e há **dois** tiques de exatamente 2,0
s no poll loop (`lifecycle.py:3829` e `:3890`). **Não acontece:** os dois saem
sem tocar o hardware em tique quieto (§1.3). A coincidência de período é real e
é frágil; quem adicionar escrita a um desses tiques religa o keepalive perpétuo
sem perceber, e o preço já está medido — 0,5 s → pulso, 8,0 s → oito segundos de
vibração alheia apagada.

**Este é o mecanismo que o E-6 não testou**, e ele é medido em taxa de escrita,
não em carga de barramento. Mas ele não chega a 250 Hz: o teto do keepalive é
2 Hz por controle. Quem chega perto do teto do laço é o rumble do jogo — e
esse ninguém mediu.

---

## 5. Onde cabo e rádio divergem

Divergem em **dois** pontos do código e em **um** ponto que não é código.

**Ponto 1 — o envelope.** `prepareReport` (`backend_pydualsense.py:981`) escolhe
por `self.conType`: `build_bt_report` ou `build_usb_report`
(`core/ds_output_report.py:252-274`).

**Ponto 2 — o carimbo.** `writeReport` (`:1018`) ramifica por
`len(outReport) == 78 and outReport[0] == 0x31`: o rádio ganha `seq` rotativo e
CRC recalculado numa **cópia** (para o dedup, que compara o buffer com `seq` 0,
continuar valendo); o cabo vai como está.

| | cabo (`0x02`) | rádio (`0x31`) |
|---|---|---|
| bytes no fio | **64** | **78** (+22%) |
| tag obrigatório | não tem | `[2] = 0x10` |
| contador de sequência | **não tem** | nibble alto de `[1]`, wrap 0-15, por handle |
| CRC | **não tem** | CRC-32 sobre seed `0xA2` + `[0..73]`, nos 4 últimos bytes |
| report fora de sequência | não existe | **descartado pelo firmware** |
| escrita avulsa fora do laço | nenhuma (só muta estado) | `_pintar_por_hidraw_bt`, no mesmo fd, de outra thread |
| LED no laço | fallback pydualsense, nunca suprimido | `_suppress_leds` nasce **True** (`:461`) |

**Ponto 3 — e é o que não é código.** No cabo, o report de entrada vive num
endpoint de interrupção com `bInterval = 4 ms` — **banda reservada na
enumeração**, escalonada pelo xHCI em hardware. O E-1 leu isso no descritor e o
E-2 mediu 250 Hz entregues. No rádio, o report é um pacote ACL que o adaptador
tem de transmitir numa janela de conexão, disputando o ar com o outro link, com
o WiFi e com tudo mais em 2,4 GHz. **Não há reserva.**

É essa terceira diferença que explica a assinatura mais forte do E-6, e ela não
está no nosso código: **250,0 Hz com dispersão 0,0 é a assinatura de banda
reservada.** Nenhum tráfego alheio a desloca. Contra 11,9 e 43,7 Hz de dispersão
do outro lado.

---

## 6. A HIPÓTESE

> **O dano ao rádio não vem do barramento USB nem do tráfego de entrada: vem dos
> próprios reports de saída que o Hefesto envia a um DualSense pelo rádio
> disputando o ar do MESMO enlace — de modo que a taxa de entrada de um controle
> do rádio cai monotonicamente com o número de escritas por segundo endereçadas
> A ELE, e não cai com escritas endereçadas ao outro controle do rádio nem aos do
> cabo; enquanto os do cabo permanecem em 250,0 Hz com dispersão 0,0 em todos os
> patamares, porque a entrada deles mora num endpoint de banda reservada que
> tráfego nenhum desloca.**

Uma frase, duas predições opostas, e as duas medíveis na mesma janela.

### 6.1 Por que ela explica o cabo estável

Porque não pede nada do cabo. Sob esta hipótese o cabo **tem** de ficar em
250,0/0,0: `bInterval = 4 ms` é banda reservada, e o endpoint de saída é
**outro** endpoint, com a sua própria fatia da mesma microtrama. Escrever no
cabo não pode deslocar ler no cabo, e escrever no rádio não chega perto do cabo.

Mais que isso: a estabilidade do cabo vira **controle negativo do próprio
ensaio**. Se algum patamar mover o cabo, o réu é a régua, não o aparelho — é a
armadilha nº 1 desta casa, e ela ganha um detector de graça.

### 6.2 Por que ela explica o que JÁ funcionava — inclusive a cura de 2026

O `BUG-MULTI-CONTROLLER-BT-CRC-CONTENTION-01` está escrito em
`backend_pydualsense.py:204-213`, e a leitura de hoje **muda a atribuição dele
sem contradizer um fato sequer**.

O laço do upstream (`.venv/.../pydualsense/pydualsense.py:252-274`, fora da
árvore) não tem sono **e não tem dedup**: ele escreve em TODA iteração. Com a
leitura não-bloqueante e a fila do `hidraw` cheia, ele não espera nada — gira na
velocidade do `hid_write`, milhares de vezes por segundo, **em cada handle,
inclusive no do rádio**.

Então o controle do rádio estava sendo escrito a milhares de reports de 78 bytes
por segundo **por nós**. Não é preciso invocar o xHCI para explicar o link
morrendo: o enlace estava sendo afogado diretamente. E o controle do cabo, que
parecia o culpado, era testemunha — a presença dele mudava `n`, e `n` mudava
tudo depois da cura, mas antes dela o rádio já se afogava sozinho.

Isso explica, sem remendo:

- **o defeito original** (a saída do BT morria com mais de um controle);
- **por que a cura funcionou** — o throttle cortou a taxa de escrita do handle
  BT em uma a duas ordens de grandeza, e o dedup cortou de novo;
- **por que o E-6 não achou nada** — captura de microfone é tráfego de entrada
  em USB; ela nunca toca o ar do enlace BT;
- **por que o cabo deu 250,0/0,0**;
- **por que a dispersão do rádio é enorme** — disputa por ar é estocástica.

E é coerente com o que a casa já teme por escrito: o
[PLANO-DA-MESA-2-2](../estudos/2026-08-15-PLANO-DA-MESA-2-2-o-que-so-se-mede-com-quatro.md),
§5.1, classifica o EXP-SPK-01 (547 B a 50 Hz por rádio) como *"pode saturar a
fila do enlace e derrubar o link"*. **A casa já acredita que escrita demais no
rádio derruba o rádio.** Esta hipótese só diz que o produto faz isso em menor
dose, todo dia, e que ninguém mediu onde fica o joelho.

### 6.3 O que ela NÃO explica — e isto não vai ser maquiado

Três coisas. Se a próxima pessoa aceitar a hipótese, aceita com estes três
buracos abertos:

1. **Não explica a assimetria entre os dois do rádio no patamar 0** (359 Hz
   contra 203 Hz, na mesma janela). No ocioso o daemon escreve **zero** (§1.3).
   Essa diferença é do aparelho, do pareamento ou do ar — **não é nossa**, e
   qualquer teoria que a atribua ao laço está errada antes de começar.
2. **Não explica `DualSense input CRC's check failed`.** Roubo de ar produz
   pacotes **em menor número**, não **corrompidos**. Se as falhas de CRC forem
   parte do defeito de 10/08, há um SEGUNDO mecanismo (retransmissão,
   interferência, coexistência com WiFi), e curar um não cura o outro. O ensaio
   abaixo conta CRC justamente para separá-los.
3. **Não explica a queixa na forma em que ela foi registrada** — *"um controle
   no cabo matava a saída do controle no BT"*. Sob esta hipótese o cabo é
   testemunha, não réu. A ponte que ofereço na §6.2 (pré-cura o rádio se afogava
   sozinho, e o cabo só mudava `n`) é **leitura de código, não medição**. O braço
   2 do ensaio existe para atacar exatamente esse ponto: se a dose no cabo
   derrubar o rádio, a minha ponte está errada e o barramento volta à mesa.

---

## 7. O ENSAIO QUE A TESTA — E-9

Os nomes E-7 e E-8 já estão tomados no
[PLANO-DA-MESA-2-2](../estudos/2026-08-15-PLANO-DA-MESA-2-2-o-que-so-se-mede-com-quatro.md),
§4. Este é o **E-9**, e ele pertence ao **bloco dela** (§5.1 do plano: os que
escrevem no aparelho).

### 7.1 A variável, e ela é uma só

**Escritas de output report por segundo endereçadas a UM controle nomeado.**
Nada mais muda: mesma mesa, mesmos quatro controles, mesma janela, mesmo minuto.

### 7.2 Os patamares — quatro, e cada um é uma âncora do produto

| patamar | escritas/s | de onde vem o número |
|---|---|---|
| **P0** | 0 | a linha de base; já medida hoje pelo E-6 |
| **P1** | 31 | o teto do produto com a mesa cheia (`REPORT_THREAD_THROTTLE_MAX_SEC` = 0,032 s) |
| **P2** | 125 | o teto do produto com UM controle (`REPORT_THREAD_THROTTLE_SEC` = 0,008 s) |
| **P3** | 1000 | a ordem de grandeza do regime **pré-cura** (laço do upstream, sem sono e sem dedup) |

Nenhum é número redondo escolhido por gosto. **P1 e P2 são os dois valores que o
produto realmente usa**, e é entre eles que a resposta interessa. **P3 é o que
decide se a cura de 2026 protege um mecanismo real** ou se ela foi um remédio
que acertou por acaso.

### 7.3 Os braços — e é aqui que o ensaio vale mais que uma dose-resposta

| braço | quem recebe a dose | o que separa |
|---|---|---|
| **B1** | um controle do **rádio** (A) | mede A, o outro do rádio (B), e os dois do cabo |
| **B2** | um controle do **cabo** (C) | a mesma dose, os mesmos quatro medidos |

- **A cai em B1, B não cai, cabo não cai** → o recurso disputado é **o ar do
  enlace de A**. É a hipótese de pé.
- **A e B caem juntos em B1** → o recurso é **o adaptador**, não o enlace. A
  cura muda de forma: o orçamento de escrita tem de ser **global entre os
  handles BT**, e o throttle atual (por handle, contando os do cabo) é a forma
  errada.
- **A cai também em B2** (dose no cabo derruba o rádio) → **o barramento volta à
  mesa**, o E-6 mediu a carga errada e não a hipótese errada, e a §6.3 item 3
  estava certa em duvidar de mim.
- **Nada se move em patamar nenhum, nem no P3** → o laço de escrita **não é** o
  mecanismo. Ver §7.7, porque este desfecho é o que mais paga.
- **O cabo se move em qualquer braço** → **pare e desconfie da régua.** Banda
  reservada não se desloca; um cabo que anda é instrumento mentindo.

### 7.4 A régua

Reports de entrada por segundo, por nó `hidraw`, para os **quatro** controles na
**mesma** janela. O instrumento já existe:
[`scripts/ensaios/taxa_no_hidraw.py`](../../../scripts/ensaios/taxa_no_hidraw.py),
que é o I-1 do plano e já serviu ao E-2, E-3 e E-6 — com controle negativo
validado hoje (a fonte que se sabe muda deu zeros exatos). A porta é o broker,
por `comum.abrir_no_hidraw(..., escrita=True)`
([`scripts/ensaios/comum.py`](../../../scripts/ensaios/comum.py)), que **já
sabe** pedir arrendamento de escrita. **Nenhuma encanação nova.**

Duas réguas de segundo grau, que custam quase nada e separam mecanismos:

1. **Contagem de `DualSense input CRC's check failed` por janela** (`journalctl
   -k`). Separa "menos pacotes" de "pacotes corrompidos" — o buraco 2 da §6.3.
2. **Contagem de escritas ACEITAS pelo kernel** (o retorno de cada `write`), por
   janela. Sem isto o ensaio mede a **intenção** de dose, não a dose. É a
   armadilha nº 1 desta casa e ela não vai me pegar de novo.

### 7.5 O protocolo

Idêntico ao do E-6, e de propósito: é contra a dispersão que **ele** mediu que o
efeito vai ser comparado.

- **15 s por patamar**, escada **subindo e descendo**, **4 rodadas**.
- 4 patamares x 4 rodadas x 2 braços = **32 janelas**, ~30 min de medição.
- Régua de decisão, a mesma: **variação menor que a dispersão do próprio
  patamar não é dose-resposta**.
- **Critério de aborto, escrito antes:** se em P3 o enlace cair (o controle
  some, `ENODEV`, falhas voltando em ~0,01 s), **para o ensaio**, registra a hora
  de parede e **não conclui nada sobre dose** — um link derrubado não é um ponto
  da curva, é o fim dela. O plano já avisa que 547 B a 50 Hz podem derrubar o
  link; 78 B a 1000 Hz é mais banda.

### 7.6 O preço — dito na cara

**Escreve no aparelho? SIM.** É o preço central, e não há versão barata: a
variável É a escrita.

- **Os bytes:** o `common` de 47 bytes **inteiramente zerado**, dentro do
  envelope certo (`build_bt_report` / `build_usb_report` de
  `core/ds_output_report.py`). Todo `valid_flag` em zero significa "não peço
  nada"; nenhum LED, nenhum gatilho, nenhum áudio, nenhuma escrita em NVS,
  nenhum feature report. **Não** toca a família `0xF0`-`0xF7` (a D-32 é da casa,
  e continua).
- **A ressalva honesta:** zerado **não** é inócuo. O `keepalive-premissa-troca-de-lado`
  de 11/08 mediu que **o firmware obedece aos bytes de motor mesmo com os bits de
  autorização desligados**. Enquanto o E-9 roda, nenhuma vibração de terceiros
  sobrevive. **Rodar sem jogo aberto**, e isso é regra do ensaio, não conselho.

**Derruba a mesa? NÃO** — e ela precisa estar cheia: são os quatro controles, nos
dois transportes, o ensaio inteiro. Nada de desplugar, nada de re-parear.

**Mas exige o daemon fora do caminho.** Com o daemon escrevendo, a dose deixa de
ser conhecida (dois escritores no mesmo fd) e o `seq` do rádio entra na corrida
da §2 — o ensaio mediria o próprio ruído. Duas saídas, e a escolha é dela:

- **Modo Nativo** (`_output_muted` por handle): zero escritas do daemon, sem
  parar serviço nenhum. É o caminho limpo, e não pede `sudo`.
- **Daemon parado**: mais simples de auditar, mas é gesto de sessão e é dela.
  A recomendação escrita na
  [página das decisões](../2026-08-15-AS-DECISOES-QUE-ESPERAM-VOCE.md) para a
  bateria de escritas da escada já foi *"a escrita vai com o daemon parado"*.

Subir `HEFESTO_DUALSENSE4UNIX_REPORT_THROTTLE_SEC` **não serve**: mexe no teto do
laço e não no keepalive, que continua a 2 Hz por controle.

**Precisa dela presente? Para RODAR, não. Para AUTORIZAR, sim.** Nenhum passo
usa o olho dela como instrumento — a régua é contagem, não percepção. Mas é
escrita no aparelho dela, na mesa montada, e isso é o **bloco dela** do plano.
**Proponho como D-38** (D-13 a D-37 estão tomadas), na mesma família da D-31.

E há uma segunda razão para ela: se o desfecho for positivo, a consequência é
mexer no throttle — e throttle é latência de gatilho, de LED e de rumble. Isso é
interface, e interface fecha com o olho dela.

**Tempo total:** ~45 min, incluindo censo de abertura e folga.

### 7.7 E se der negativo — porque ensaio cujo negativo não ensina não vale a hora

Se nada se mover até P3, o E-9 **não** volta de mãos vazias. Ele aposenta a
justificativa do throttle.

O `REPORT_THREAD_THROTTLE_MAX_SEC` cobra **até 32 ms de latência em toda mudança
de LED, gatilho e rumble** com a mesa cheia, e cobra isso para proteger contra um
mecanismo que teria sido medido como ausente a **32 vezes** o pico do próprio
produto. Um negativo compra de volta a responsividade **com prova na mão**, em
vez de deixar de pé uma cura que ninguém ousa tocar porque ninguém sabe do que
ela protege.

E manda a investigação para os dois lugares que sobram, ambos já nomeados nesta
página: a corrida do `_bt_seq` (§2) e a coexistência do adaptador com o 2,4 GHz
— que é a medição com o dongle noutro controlador que o
[`scripts/medir_w3_coex.sh`](../../../scripts/medir_w3_coex.sh) pede desde 10/08
e que nunca foi feita.

Nos dois desfechos a linha
`combinacao.adaptador_no_mesmo_controlador@dualsense` de
[`docs/data/mapa-controles.csv`](../../data/mapa-controles.csv) sai do estado
"metade do mecanismo em aberto".

---

## 8. Os dois achados que não dependem do ensaio

Nenhum dos dois foi tocado: `src/` é de outro agente nesta janela. Ficam com a
mordida sugerida, para quem for consertar.

> **CONSERTADOS no mesmo dia** —
> [O-LACO-DE-ESCRITA-02](2026-08-15-O-LACO-DE-ESCRITA-02-os-dois-achados-viram-cura.md).
> Os dois estavam certos. Uma correção de fato veio junto: a morte da thread
> **não** seria totalmente calada — o `threading.excepthook` padrão imprime
> traceback no stderr, e a unit não sobrescreve `StandardOutput`, então ele
> chega ao journal. Calado era o que importa para o produto: sem log
> estruturado, sem `connected = False`, sem ressurreição. E a pré-condição do
> segundo achado **nunca disparou nesta máquina**: zero ocorrências em 30 dias
> de journal.

| achado | onde | mordida sugerida |
|---|---|---|
| **`_bt_seq` sem lock** — dois escritores no mesmo handle podem carimbar o mesmo `seq`; o firmware descarta e o log diz "escrito" | `writeReport`, `core/backend_pydualsense.py:1018-1033` | duas threads chamando `writeReport` num handle BT em paralelo têm de produzir `seq` **todos distintos**; arrancar o lock reprova |
| **`TypeError` não capturado** — `read` devolve `None` num silêncio de ~2 s do rádio e a `report_thread` morre sem log | `sendReport`, `core/backend_pydualsense.py:582-658` | um `device.read` que devolve `None` não pode matar a thread nem passar em branco: ou continua o ciclo, ou marca `connected = False` com log. Fazer o dublê devolver `None` uma vez reprova hoje |

Um terceiro, que é dívida e não defeito: com a mesa cheia o laço consome 31,25
reports/s de um fluxo de 200-360/s, então a fila do `hidraw` vive cheia e
**bateria, `status[1]` de áudio e transporte lidos pelo daemon estão ~2 s
atrasados**. Não afeta input (que vem do evdev). Afeta o que a tela dela mostra.

---

## 9. Resumo de uma tela

- **Cadência:** teto de `min(0,008 x n; 0,032)` s por controle — 125 Hz com um,
  **31,25 Hz com quatro**, agregado constante em 125 Hz até quatro. A **taxa de
  escrita** é bem menor: **0** no ocioso, **2 Hz** com rumble nosso, e o teto do
  laço só com o rumble do jogo variando. Sem fan-out no laço; com fan-out no
  gesto.
- **Divergência cabo/rádio:** envelope (64 x 78 bytes), `seq` + CRC só no rádio,
  escrita avulsa fora do laço só no rádio — e, fora do código, **banda reservada
  no cabo contra ar disputado no rádio**.
- **Hipótese:** o dano é o nosso próprio output roubando ar do enlace BT, dose
  por dose, no controle a quem ele é endereçado.
- **Explica o cabo estável** porque não pede nada dele: 250,0/0,0 é assinatura
  de banda reservada, e vira controle negativo do ensaio. **Não explica** a
  assimetria de 359 x 203 Hz no ocioso, nem as falhas de CRC, nem a queixa na
  forma "o cabo matava o rádio" — os três estão escritos como buracos, não
  maquiados.
- **Ensaio E-9:** quatro patamares (0 / 31 / 125 / 1000 escritas/s), dois braços
  (dose no rádio, dose no cabo), 15 s x 4 rodadas, régua do E-6. **Escreve no
  aparelho**, **não derruba a mesa**, **não precisa dela para rodar — precisa
  dela para autorizar** (proposta **D-38**), e o daemon tem de sair do caminho.
  ~45 min. **O negativo aposenta a justificativa do throttle**, que hoje cobra
  até 32 ms de latência para proteger contra um mecanismo não medido.
