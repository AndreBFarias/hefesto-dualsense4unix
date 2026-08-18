# A noite em que medimos a lightbar do Bluetooth

- **Medido em:** 03/08/2026, das 17:45 às 20:10, no hardware dela, com dois
  DualSense, um Pro Controller e um 8BitDo na mesa
- **Método:** um suspeito de cada vez, com o olho dela confirmando cada cor.
  Nenhuma linha de código do produto foi alterada
- **Por que existe:** porque a causa-raiz que estava escrita há dois dias
  (`LIGHTBAR-BT-CLAIM-01`) está **refutada**, e a de julho
  (`LIGHTBAR-BT-ADOPT-01`) **acusou o culpado errado** — a cura que ela
  introduziu é a causa do defeito de hoje

---

## O VEREDITO

> **O `0x08` (`VALID_FLAG1_RELEASE_LEDS`), enviado dentro da janela de ~3,4 s
> após a conexão por Bluetooth, trava a lightbar até o power-off físico do
> controle. Fora dessa janela ele é inofensivo para a barra — mas apaga os
> player-LEDs, sempre.**
>
> **Ele foi acrescentado em 18/07/2026 como a CURA da lightbar por Bluetooth.**

### A correlação, em sete eventos do journal

| # | evento | `0x08` depois de conectar? | barra |
|---|---|---|---|
| 1 | branco `17:48:24.266` | sim — **mesmo milissegundo** | travou |
| 2 | roxo `17:48:36.709` | sim — **53 ms** | travou |
| 3 | roxo `19:34:45.476` | sim — mesmo ms | travado |
| 4 | roxo `19:53:17.904` | sim | travado |
| 5 | roxo `19:56:08.022` | sim — **695 ms** | travado |
| 6 | **roxo `20:03:56`** | **NÃO** (reconectou sem o report) | **OBEDECE** |
| 7 | branco `20:04:20.989` | sim — **515 ms** | travou |

Sete de sete. **O único controle que não recebeu o report é o único que
obedece** — e os dois estavam no mesmo rádio, na mesma mesa, no mesmo minuto.

### Por que o teste isolado do `0x08` NÃO travou (e isso não contradiz)

Às 19:45 o `0x08` foi enviado sozinho, pelo próprio
`build_bt_release_leds_report` do projeto, num controle conectado havia dez
minutos. **A barra obedeceu à cor seguinte.** O que travou foi só o
player-LED.

Não há contradição: aquele controle estava **fora da janela**. É a mesma
assimetria que separa o evento 6 do evento 7 — e foi ela que enganou as duas
sprints anteriores.

---

## O que foi REFUTADO (não reabrir)

### 1. `BT-SURDO-01` — "o rádio emudece com o controle parado"

**Refutada.** Com os controles parados na mesa:

| controle | janela | bytes lidos do hidraw | taxa |
|---|---|---|---|
| branco | 60 s | 1.402.128 | **~300 Hz** |
| branco | 20 s | 509.652 | ~326 Hz |
| roxo | 20 s | 474.006 | ~304 Hz |

O DualSense por Bluetooth **não emudece em repouso**. A premissa que sustentava
a sprint inteira caiu; as entregas E2/E3/E4 dela seguem válidas por serem
defeitos de código independentes.

### 2. `LIGHTBAR-BT-CLAIM-01` — "o gatilho é o reinício do daemon"

**Refutada em três pontos:**

- **o `0x08` não devolve o claim ao firmware de forma fatal fora da janela** —
  evento 4 do quadro acima: enviado às 19:53:17, e a barra obedeceu;
- **o gatilho não é o reinício do daemon** — o evento 6 é uma reconexão com o
  daemon **vivo**, e não travou; o evento 7 é outra, e travou. A diferença é o
  report, não o daemon;
- **a cura proposta APAGA a barra.** A sprint manda
  `common[41] = LIGHT_OUT` para "tomar a barra de volta". O driver desta
  máquina diz o contrário, textualmente:

  ```c
  report.common->lightbar_setup = DS_OUTPUT_LIGHTBAR_SETUP_LIGHT_OUT; /* Fade light out. */
  ```

  `LIGHT_OUT` **apaga**. Quem executasse aquela cura escreveria código para
  apagar a barra acreditando que a acendia. *(Testado ao vivo: nenhum efeito.)*

### 3. Os quatro suspeitos inocentados, um a um

Todos testados no controle vivo, com a barra confirmada pelo olho dela entre um
e outro:

| suspeito | veredito |
|---|---|
| abrir o hidraw (`hidapi.Device`, como o `_open_one` faz) | inocente |
| feature report `0x05` (calibração, 41 bytes lidos com sucesso) | inocente |
| `pydualsense.init()` completo + `report_thread` escrevendo 2 s | inocente |
| o `0x08` **fora** da janela | inocente para a barra |

**A barra obedeceu a seis cores seguidas por Bluetooth** — vermelho, ciano,
magenta, amarelo, verde e vermelho de novo — entre esses testes. O transporte
nunca foi o problema.

---

## O que foi PROVADO, além da causa-raiz

### O `0x08` apaga os player-LEDs — sempre

Medido isoladamente: antes, `--x--` (P1 aceso); depois de enviar só o `0x08`,
**todos apagados**. É o que o nome diz — `RELEASE_LEDS`, plural.

O projeto o envia em **toda adoção de handle novo**
(`core/backend_pydualsense.py:1524-1533`). Logo, **todo reconnect por Bluetooth
apaga o número do jogador** — pagando um efeito colateral real por um benefício
que este estudo demonstra inexistente.

### O kernel define o bit e nunca o usa

`grep RELEASE_LEDS` no `hid-playstation.c` desta máquina devolve **uma linha** —
a definição (`:189`). Zero usos. O `0x08` é decisão exclusiva deste projeto,
copiada do comportamento do SDL.

### O pipeline de cor do projeto está correto

Duas provas independentes:

1. **o cabo escapa** — com o daemon parado, o mesmo comando de sysfs, no mesmo
   instante, pintou o controle no USB e não pintou o do rádio;
2. **comandos pendentes materializaram-se no cabo** — o amarelo e o padrão P5
   que eu mandei no Bluetooth (sem efeito) apareceram no controle assim que ele
   foi plugado. O `_desired` guardou; o transporte é que não entregava.

### O `multi_intensity` não é a verdade do hardware

Provado da forma mais limpa possível: depois do power-off, o nó novo nasceu
`0 0 0` **com a barra acesa em azul** (o `KERNEL_DEFAULT_BLUE` do probe). E,
travado, o nó aceita qualquer valor sem que a barra mude.

Isto já estava escrito em `core/sysfs_leds.py:92-105` (`STATUS-01`) e **a aba
Status inteira depende dele** — é a base do defeito 3 da `BT-E-VPAD-01` (*"a
tela mente"*).

---

## Dois defeitos das sprints, capturados ao vivo no journal

Não eram o objeto da medição; apareceram sozinhos.

### O `EBUSY` do co-op (`COOP-QUE-NÃO-DESMONTA-01`)

```
20:03:57.314  evdev_started      path=/dev/input/event14
20:03:57.314  evdev_grab_failed  [Errno 16] Dispositivo ou recurso está ocupado
20:03:58.256  coop_player_removed  identity=a0fa9c…  players=1
```

O jogador entra e sai em **0,9 s**, exatamente como a sprint descreve. E ela viu
com os próprios olhos, sem saber que era isso: *"o controle branco entrou como
player 2 no início, mas logo tomou o player 1 do controle do bt"* — é a
re-eleição de primário roubando o número.

### Os externos renumerados a cada hotplug

```
20:03:57  external_led_written  slot=2  →  external_led_repintado  intruso=3
20:04:21  external_led_written  slot=3  →  external_led_repintado  intruso=2
```

O Pro Controller foi renumerado **duas vezes em 24 segundos** — 2, depois 3 —
a cada entrada/saída de um DualSense do rádio. É a queixa dela sobre o 8BitDo,
com o mecanismo à vista.

---

## As armadilhas de medição desta noite

Cada uma custou tempo, e todas se repetem:

1. **medir fora da janela** — os quatro testes isolados de suspeitos rodaram com
   o controle conectado havia minutos, e por isso nenhum reproduziu. **A janela
   de 3,4 s tem de fazer parte do protocolo de teste**, não do acaso;
2. **o `zsh` come `:r`** — `$n:rgb:indicator` expande errado. Já estava escrito
   na `LIGHTBAR-BT-CLAIM-01`, e caí nela assim mesmo. Use `${n}`;
3. **o daemon DESFAZ escrita de sysfs alheia** em ≤30 s (`NUMA-03`) — com o
   daemon vivo, o teste por sysfs mede a defesa, não o firmware. Toda medição de
   cor com o daemon no ar precisa passar pelo IPC ou aceitar ser desfeita;
4. **o número de sequência** — reports escritos à mão no hidraw competem com o
   `_bt_seq` do daemon. Três testes meus foram inconclusivos por isso, e só o
   caminho do kernel (sysfs) ou o do daemon (IPC) são confiáveis com ele vivo;
5. **`/dev/hidrawN` do físico fica `0600 root`** pelo broker — sem `sudo`,
   qualquer instrumento reporta "sem dispositivo" e parece defeito do produto.

---

## A cura, e o que ela NÃO é

**A cura de raiz é não enviar o `0x08`.** Ele foi introduzido para curar a
lightbar por Bluetooth; este estudo prova que ele **não cura** (a barra obedece
sem ele — evento 6), que **causa** o latch dentro da janela, e que **apaga os
player-LEDs** fora dela. Não há benefício a preservar.

**Se houver receio de removê-lo de uma vez**, o meio-termo medido é adiá-lo para
fora da janela de ~3,4 s pós-conexão. Mas isso conserva um report que já não tem
função conhecida — e o custo dele (player-LEDs apagados) continua.

**O que NÃO é cura, e a casa já pagou por cada uma:**

- **mandar `LIGHT_OUT` para "retomar"** — apaga (testado, sem efeito);
- **religar a escrita de LED da pydualsense por BT** — `LIGHTBAR-BT-NEVER-01`,
  pago com a barra latcheada até o power-off;
- **reenviar o `0x08` por timer** — o `RESET-02` já proíbe, com motivo;
- **mexer no cache do `sysfs_leds`** — a escrita acontece; não é o cache.

## O que fica ABERTO

- **por que o `0x08` trava dentro da janela** — a correlação é perfeita (7/7),
  o mecanismo interno do firmware não foi medido e provavelmente não é
  mensurável daqui. Para efeito de cura, não é preciso saber;
- **o evento 6 é sorte ou regra?** O roxo reconectou às 20:03:56 e **não**
  recebeu o `0x08`, porque o `adopt_candidates` sai de `new_handles`
  (`core/backend_pydualsense.py:1524-1526`) e aquele handle não era novo.
  Entender quando o handle é reaproveitado explicaria por que o defeito é
  intermitente — que é exatamente a queixa dela de que *"sempre arrumamos mas
  sempre volta"*;
- **os player-LEDs do branco continuaram funcionando** com a barra travada, o
  que reproduz o sintoma de julho (*"player-LEDs e gatilhos seguem funcionando,
  não têm máquina de estados própria"*) e confirma que o latch é **da barra**,
  não do canal.
