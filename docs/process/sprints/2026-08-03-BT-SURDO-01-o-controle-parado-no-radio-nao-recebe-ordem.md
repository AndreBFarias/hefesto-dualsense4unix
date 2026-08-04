# BT-SURDO-01 — o controle parado no rádio não recebe ordem

> ## ATENÇÃO — A PREMISSA CAIU EM 03/08/2026 — MEDIDA E REFUTADA
>
> **A E0 fez o trabalho dela: o portão de medição impediu que se escrevesse
> código sobre uma causa-raiz falsa.**
>
> Com os dois controles **parados na mesa**, lendo o hidraw direto:
>
> | controle | janela | bytes | taxa |
> |---|---|---|---|
> | branco | 60 s | 1.402.128 | **~300 Hz** |
> | branco | 20 s | 509.652 | ~326 Hz |
> | roxo | 20 s | 474.006 | ~304 Hz |
>
> **O DualSense por Bluetooth NÃO emudece em repouso.** Cai a premissa, cai a
> prioridade máxima, e cai a **E1** (o acoplamento input→output existe no
> código, mas não produz o sintoma previsto).
>
> **O que CONTINUA VÁLIDO** — são defeitos de código, independentes da premissa:
> **E2** (o `init()` abandonado que não fecha o device e deixa `report_thread`
> fantasma), **E3** (o `HIDIOCGFEATURE` segurando o `_io_lock` central) e
> **E4** (o boot chamando no event loop, quando o irmão de `connection.py` já
> usa `_run_blocking`).
>
> Ver o estudo [a noite em que medimos a lightbar do Bluetooth](../estudos/2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md).


- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **MÁXIMA DA LEVA.** Se este documento estiver certo, ele
  explica a classe inteira de *"mexi na janela e não aconteceu nada no
  Bluetooth"* — e é o que separa o Bluetooth de ser uma variante do cabo
- **Faixa:** 1 — o produto não obedece
- **Causa-raiz:** **PROVADA no código.** A premissa (o rádio emudece em repouso)
  é afirmada pela própria árvore, mas **nunca foi medida com número** — e a
  E0 desta sprint é essa medição, de dez segundos
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Referência:** [o protocolo canônico](../../protocol/dualsense-referencia-canonica.md)

---

## O pedido dela, que é o critério de aceite desta sprint

> *"deixar o projeto robusto de tal forma que eu não note que estou no bt ou
> cabo, a ideia é termos tudo funcionando via bt principalmente."*

## A causa-raiz: o output do HID é relogiado pelo INPUT

`core/backend_pydualsense.py:512-538` — o laço que põe **tudo** no fio:

```python
while self.ds_thread:
    try:
        in_report = self.device.read(self.input_report_length)   # <-- PRIMEIRO
        self.readInput(in_report)
        self._captura_status_audio()
        if not self._output_muted:
            out = self.prepareReport()
            now = time.monotonic()
            if (out != self._last_out_report
                    or (now - self._last_write_at) >= OUT_REPORT_KEEPALIVE_SEC):
                self.writeReport(out)                            # <-- DEPOIS
```

**Nada é escrito antes de um report ser lido.** E o `read` **bloqueia** — isto
foi conferido na biblioteca instalada, não suposto:

- `hidapi.Device.__init__(..., blocking=True)` é o **default**, e o construtor
  só chama `hid_set_nonblocking(dev, 1)` **quando `blocking` é falso**;
- a pydualsense abre com o default (`pydualsense.py:211`, `hidapi.Device(...)`
  sem `blocking=`), e este projeto também
  (`core/backend_pydualsense.py:500`, `hidapi.Device(path=self._pinned_path)`);
- `read(length)` sem argumentos cai em `rv = hidapi.hid_read(...)`, que respeita
  o modo do device — ou seja, **bloqueia**.

### O que isso faz por USB e o que faz por Bluetooth

No cabo o DualSense emite **250 Hz incondicionalmente**: o `read` volta em ~4 ms
e a escrita sai logo atrás. **Por rádio, o firmware emudece com o controle
parado** — e isso não é hipótese nova: é a premissa que já sustenta o
`GYRO-BT-SILENCIO-01` (`core/physical_report_reader.py:126-142`), que existe
justamente porque silêncio ≥ 1 s por Bluetooth era **rotina**.

**Consequência:** com o controle parado na mesa, nada do que ela mexe na janela
chega ao controle. Gatilho, rumble, LED do microfone, os bytes de áudio
(`common[4..7]` e `common[37]`) — todos só mutam estado no handle
(`:2071`, `:2174`, `:2196`, `:2361`); quem os põe no fio é **exclusivamente**
esse laço.

E o keepalive não salva: `OUT_REPORT_KEEPALIVE_SEC = 0.5` (`:228`) só é
**avaliado depois** do `read`. Num link silencioso ele nunca dispara.

### E isso explica o que JÁ funcionava — a regra da casa

- **dentro do jogo** o input flui a 250-1000 Hz e tudo parece normal. O defeito
  não aparece jogando;
- **no cabo** ele não existe;
- ele aparece exatamente no **gesto de GUI com o controle parado** — que é como
  se configura um controle — e no **stop de um efeito** que termina enquanto ela
  está imóvel.

Com quatro controles, cada um tem o próprio relógio: os que estão na mesa ficam
surdos, os que estão na mão obedecem. É indistinguível de "às vezes funciona".

---

## E0 — A MEDIÇÃO QUE DECIDE (dez segundos, sem tocar em código)

**Esta sprint não vira código antes desta medição.** A premissa do silêncio é
afirmada pela árvore e nunca foi medida com número.

Com **um DualSense conectado por Bluetooth, parado na mesa**:

```bash
sudo timeout 60 cat /dev/hidrawN | wc -c        # N = o nó do controle BT
```

- **zero (ou quase) bytes em 60 s** ⇒ a causa-raiz está provada e as entregas
  abaixo são as certas;
- **fluxo contínuo** ⇒ a premissa caducou, e esta sprint vira uma nota datada.

> **Armadilha, e ela custou tempo nesta casa:** `/dev/hidrawN` do controle
> físico fica em `0600 root:root` — o broker o esconde a cada 30 s. Sem `sudo`,
> o comando devolve "sem permissão" e **parece** que o controle sumiu.

**A segunda medição, que a usuária faz sem terminal:** controle BT parado na
mesa; trocar o preset na aba Gatilhos; **não encostar no controle**; apertar o
L2 só depois de 10 s. Se o efeito só aparecer no **segundo** aperto, está
provado pelo tato.

---

## As entregas

### E1 — o output deixa de depender do input

O laço passa a escrever **mesmo sem report de entrada**. Duas saídas, com preços
diferentes:

- **(a) `read` com timeout curto** — `self.device.read(len, timeout_ms=8)`. O
  laço volta a cada 8 ms mesmo em silêncio, e a escrita segue o caminho normal.
  **Recomendado**: uma linha, sem thread nova, e o `timeout_ms` já existe na
  API instalada (`hid_read_timeout`);
- **(b) separar as duas metades** em threads próprias. Correto no papel e caro:
  duas threads por controle, quatro controles, e o `_io_lock` no meio.

**Aceite:** com o controle parado por 30 s no Bluetooth, mudar a cor pela janela
acende **na hora**. Medível sem hardware pela contagem de `writeReport` num
device falso que nunca devolve report.

**Por que é raiz e não contorno:** não estamos acrescentando um "reenviar de
tempos em tempos". Estamos desfazendo um acoplamento acidental — o output nunca
teve motivo para depender do input; ele depende porque o laço do upstream lia e
escrevia no mesmo `while`.

**Armadilha nomeada:** o throttle de 8 ms
(`REPORT_THREAD_THROTTLE_SEC`) existe por um defeito medido —
`BUG-MULTI-CONTROLLER-BT-CRC-CONTENTION-01`, o link BT degradando com 2+
controles. **A E1 não pode virar um laço apertado.** O `timeout_ms` da (a) deve
ser da ordem do throttle, não menor.

### E2 — o `init()` abandonado deixa de virar um escritor fantasma

`core/backend_pydualsense.py:1396-1425`: quando o `init()` estoura o
`INIT_TIMEOUT_SEC` de 5 s, o `_open_one` devolve `None` **sem chamar
`ds.close()`** e a thread é abandonada.

O `init()` chama `determineConnectionType()`, que faz **`self.device.read(100)`
bloqueante** só para descobrir se o report tem 64 ou 78 bytes
(`pydualsense.py:157-169`). Por Bluetooth, com o controle em repouso, esse read
é exatamente o do E1 — **não volta**.

Quando ela encosta no controle, aquele `init()` **completa**, marca
`ds_thread = True` e **starta um `report_thread`** num objeto que não está em
`self._handles`, que ninguém fecha, e que escreve `0x31` com o **próprio
contador `_bt_seq`** (`:452`, `:812-818`) por cima do handle legítimo e do
kernel.

**O comentário do `INIT_TIMEOUT_SEC` (`:191-201`) assume que o caso patológico é
D-state de USB.** O caso comum é o rádio calado.

**Aceite:** um `init()` que estoura o prazo **fecha o device** quando termina, e
nenhum `report_thread` sobrevive fora de `_handles`. Medível: um device falso
que demora 6 s a responder, e a asserção de que `close()` foi chamado.

**Como PROVAR que existe hoje, na máquina dela:**
`py-spy dump --pid $(pgrep -f hefesto-dualsense4unix)` e contar quantas threads
estão em `sendReport` contra o número de controles em `controller.list`. **Mais
threads que controles = fantasma.**

**Custo de não fazer:** `connect()` é serial (`:1455-1492`) — quatro controles
frios custam até **20 s dentro de um `connect()`**, ocupando um dos dois workers
do pool.

### E3 — a calibração para de segurar o lock central durante um ioctl de 5 s

`core/backend_pydualsense.py:1037-1055`: o `HIDIOCGFEATURE` da calibração
(`:1047`) roda **dentro do `with self._io_lock:`** de `:1037`. A própria
docstring diz o motivo do prazo: *"BT ocioso responde EIO no GET_REPORT (timeout
de 5 s do hidp)"* (`:1025`), e `daemon/subsystems/coop.py:654` repete o número.

O `_io_lock` é o **mesmo** de `is_connected()` (`:1866`),
`describe_controllers` (`:3182`), `_for_each` (`:1995`) e
`reassert_resolved_outputs` (`:3246`).

**Um GET_REPORT lento num controle congela o input, o `state_full` e a GUI de
todo mundo** — que é literalmente o sintoma que o `R-22` dizia ter curado
(*"o input dos QUATRO jogadores e o IPC da GUI congelam por segundos"*,
`coop.py:651-658`). O R-22 tirou a leitura do event loop e **deixou o lock**.

**Aceite:** o ioctl roda fora do `_io_lock`. Medível: um `HIDIOCGFEATURE` falso
que demora 5 s, com uma segunda thread chamando `is_connected()` e a asserção de
que ela responde em milissegundos.

### E4 — o boot para de fazer o ioctl no event loop

`daemon/lifecycle.py:731-736` chama `upgrade_primary_vpad_to_uhid(self)`
**síncrono dentro da corrotina `run()`** — e ele desce até
`read_primary_calibration` → `read_calibration()`, o ioctl da E3.

**O contraste está na própria árvore:** `daemon/connection.py:437-441` faz a
mesma chamada por `_run_blocking`. O caminho de reconexão foi corrigido; o de
boot não.

**Aceite:** boot com o primário em Bluetooth ocioso não deixa o daemon mudo. A
correção é trocar a chamada por `_run_blocking`, como o irmão já faz.

### E5 — a bancada que morde

A suíte é **cega a BT por construção** — está registrado nesta casa como bug
recorrente, e o levantamento de hoje deu o número: **9 ocorrências de
`transport="bt"` contra 202 de `"usb"`, e zero marcador de skip por hardware
BT**.

**A bancada mínima desta sprint:** um device falso com **silêncio programável**
— um `read` que não devolve nada por N segundos. Com ele, cada entrega acima
ganha um teste que morde:

1. **E1:** device mudo por 30 s → contar `writeReport`. Hoje: zero. Depois:
   contínuo. *Arranque o timeout e veja voltar a zero.*
2. **E2:** `init()` que demora 6 s → asserção de `close()` chamado e de nenhuma
   thread órfã.
3. **E3:** ioctl de 5 s + `is_connected()` concorrente → asserção de latência.
4. **E4:** asserção de que a chamada de boot passa por `_run_blocking` (a mesma
   forma do teste que já protege o caminho de reconexão).

**Este device falso é a peça que falta para o projeto inteiro deixar de ser cego
ao Bluetooth**, e por isso é entrega, não acessório.

---

## Testes que vão reprovar

```
pytest tests/unit -k "backend or pydualsense or report_thread or calibration or connect"
```

## O que NÃO fazer

- **Não escrever antes de a E0 medir.** Se o rádio não emudece nesta máquina, a
  causa-raiz é outra e as quatro entregas mudam de endereço;
- **Não tirar o throttle** para "ganhar tempo" no laço — ele paga um defeito
  medido de contenção do link BT;
- **Não trocar o `INIT_TIMEOUT_SEC` como cura da E2.** O prazo está certo; o que
  falta é o `close()`. Aumentá-lo só faz o `connect()` demorar mais;
- **Não mover o `_io_lock` inteiro** para resolver a E3. O lock protege o mapa de
  handles; o que sai de dentro dele é **o ioctl**, não a proteção;
- **Não medir a taxa de output contra a `libSDL2` do sistema.** A lição de
  método de 01/08 vale aqui: todo instrumento declara contra o que mede.

## O que fica ABERTO

- **quanto tempo o rádio fica mudo** — a E0 responde;
- **se existe report_thread fantasma na máquina dela agora** — o `py-spy` da E2
  responde, e é um comando;
- **quanto tempo o `HIDIOCGFEATURE` leva de fato num BT ocioso** — os 5 s são
  citados pela árvore, nunca medidos aqui.
