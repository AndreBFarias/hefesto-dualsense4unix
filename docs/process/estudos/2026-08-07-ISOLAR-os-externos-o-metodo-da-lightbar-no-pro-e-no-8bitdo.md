# Isolar os externos — o método da lightbar aplicado ao Pro Controller e ao 8BitDo

- **Escrito em:** 07/08/2026, entre 15h20 e 16h00, com a máquina dela **viva e em
  uso** — DualSense e Pro Controller no rádio, DualSense carregando desde os 5%.
- **Ampliado em:** 07/08/2026, 18h55 — **o E-1 FECHOU**, e é a **primeira**
  medição deste protocolo a fechar. O resultado inteiro está na subseção
  [E-1 FECHADO](#e-1-fechado--07082026-18h55); o resumo em uma linha está logo
  abaixo. Custo de atenção dela: **zero minuto**, como o desenho previa. Também
  leitura pura, com a máquina dela em uso.
- **Pedido dela, com as palavras dela:** *"o certo aqui não seria a gnt ir
  isolando e testando os parâmetros pra ele e pro 8bitdo igual fizemos ao mapear
  o lightbar do bt do dualsense? talvez dessa forma conseguiríamos inclusive
  tornar permanente a conexão BT deles e dos dualsense"*.
- **O que foi feito aqui:** **leitura pura** de `/sys`, `/proc`, `/dev/input`,
  D-Bus e journal. **Zero escrita em hidraw, zero reinício de serviço, zero
  toque em `/etc`.** O que só fecha escrevendo no hardware virou **protocolo**
  (seção 8), para ela executar — não experimento meu.
- **Formato do protocolo:** o da fila de 06/08
  ([o que só fecha com o controle na mão dela](2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md))
  — **P0** tranca o cenário (com o destrancar embutido), **ANTES** é a foto
  numérica, **CONTRASTE** é o caso sem o qual nada se conclui, **PREVISÃO** é
  falsificável e derivada do código, **LEITURA** é a tabela escrita **antes** de
  medir.
- **Grau em toda linha:** MEDIDO / SUSPEITA COM MECANISMO / SEM PROVA.

---

## O resumo, antes de tudo

Ela está certa no método, e o método rendeu **na primeira aplicação**: a
varredura de hoje achou **um defeito vivo, medido, com mecanismo fechado** — o
Hefesto estava, até as 15h27 de hoje, **martelando o LED do Pro Controller num
laço que não podia terminar**, e cada rodada custava 12 recusas do kernel e um
`-110` por lâmpada. É o mesmo bombardeio que a `EXT-04` diz ter matado o 8BitDo,
acontecendo com o outro controle, hoje.

E a varredura também **corrigiu o alvo da pergunta dela sobre a conexão
permanente**. O quadro medido é o oposto do esperado:

| aparelho | quantos links novos no kernel, 01/08 a 07/08 | GRAU |
|---|---|---|
| **Pro Controller** (`057e:2009`, Bluetooth) | **3** — e o atual está de pé há **17h25m** | MEDIDO |
| **DualSense** (`054c:0ce6`, Bluetooth) | **8** instâncias distintas | MEDIDO |

**Quem cai é o DualSense; o Pro é o estável.** Qualquer leva que comece
tratando "a queda do Pro" como o problema começa mirando o controle errado.

**Adendo de 07/08, 18h55 — o E-1 fechou, e mudou duas linhas desta página.**
Com o portão fechado às 15:27:48, o storm foi a **zero** em 3h27m, enquanto a
taxa de queda do DualSense **não** mudou (0,27/h contra 0,29/h). E o pareamento
minuto a minuto do lado A mostrou que **nenhuma** recusa do kernel aconteceu sem
uma escrita nossa: a causa do storm passa de SUSPEITA COM MECANISMO para
**MEDIDO** — o storm era nosso. Mas o Pro **não caía por causa dele**: do lado A
ele atravessou 225 recusas e 54 falhas `-110` com o link intacto por 17h06m.
GRAU: MEDIDO. E o achado maior não é sobre o Pro: **a decisão dela de calar a
luz, tomada por honestidade, curou um defeito técnico que ninguém sabia que
existia** — subseção 10 do E-1.

---

## 1. O método que ela reconheceu, extraído da noite da lightbar

Fonte: [a noite em que medimos a lightbar do
Bluetooth](2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md), mais as
duas sprints que ela derrubou
([CLAIM-01](../sprints/2026-08-02-LIGHTBAR-BT-CLAIM-01-a-barra-apagada-com-o-sysfs-certo.md)
e
[CULPADO-01](../sprints/2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md)).
Sete peças, e **nenhuma é opcional**:

1. **Um suspeito de cada vez, com o olho dela entre um e outro.** Quatro
   suspeitos foram inocentados um a um — abrir o hidraw, o feature report
   `0x05`, o `init()` completo da pydualsense, e o `0x08` fora da janela — e cada
   veredito veio de ela olhar a barra, não de um número inferido.
2. **O controle negativo tem de estar no MESMO rádio, no MESMO minuto.** O que
   fechou a causa não foi a série de sete eventos: foi o **evento 6** — um
   controle que reconectou **sem** receber o report e obedeceu, enquanto o
   irmão, na mesma mesa e no mesmo minuto, recebeu e travou. Sem esse par
   simultâneo, "travou" e "o rádio estava ruim" ficam colados.
3. **A janela faz parte do protocolo, não do acaso.** Os quatro testes isolados
   não reproduziram porque rodaram **fora** da janela de ~3,4 s pós-conexão. A
   armadilha nº 1 daquela noite foi essa, e ela se repete em tudo que aqui
   depende de **borda de conexão**.
4. **O instrumento tem de declarar contra o que mede — e pode estar brigando com
   o produto.** Com o daemon vivo, o sysfs mede a **defesa do daemon**, não o
   firmware (o `NUMA-03` desfaz escrita alheia em até 30 s); e reports escritos à
   mão competem com o `_bt_seq`. Três medições daquela noite foram inconclusivas
   só por isso.
5. **A previsão sai ANTES, derivada do código, e pode morrer.** A previsão de
   que os cinco presets de `0x26` seriam idênticos **errou**, e o erro ensinou
   mais que o acerto (o empacotamento caía em cima do bitmask de zonas).
6. **A refutação é entrega, e leva data.** Três hipóteses foram **enterradas com
   nome** (`BT-SURDO-01`, o gatilho do reinício do daemon, e o `LIGHT_OUT` como
   cura) para ninguém gastar leva nelas de novo.
7. **A cura tem de explicar o que JÁ funcionava.** Foi por isso que "o transporte
   não entrega cor" caiu: a barra obedeceu a **seis cores seguidas** por
   Bluetooth entre os testes.

**O que muda ao aplicar isso aos externos**, e precisa ficar dito antes do mapa:
na lightbar o instrumento era o **olho dela** e o produto era **cor**. Aqui o
instrumento é o **journal do kernel** e o produto é **um link de rádio que dura
horas**. Isso troca a régua: nada aqui fecha em três minutos de bancada; as
medições desta página têm janelas de dezenas de minutos a uma noite.

---

## 2. O inventário desta hora — 07/08/2026, 15h46

MEDIDO agora (`/proc/bus/input/devices`, `/sys/class/hidraw/*/device/uevent`,
`lsmod`, `busctl` no `org.bluez`, `hciconfig`):

| aparelho | transporte | VID:PID | driver | instância HID | vivo desde |
|---|---|---|---|---|---|
| **Pro Controller** (OUI `e0:f6:b5`) | Bluetooth | `057e:2009` | `nintendo` | `.0017` | **06/08 22:21** |
| **DualSense** (OUI `a0:fa:9c`) | Bluetooth | `054c:0ce6` | `playstation` | `.0021` | 07/08 15:23:56 |
| **8BitDo em modo PS4** (OUI `e4:17:d8`) | Bluetooth | `054c:05c4` | `playstation` | `.001F` | **CAIU** entre 15:24 e 15:43 |
| vpad do Hefesto (P1) | uhid | `054c:0df2` | `playstation` | `.0022` | 07/08 15:27:48 |

Módulos carregados: `hid_nintendo`, `hid_playstation`, `ff_memless` (preso aos
dois), `led_class_multicolor` (só o `hid_playstation`). GRAU: MEDIDO.

Três fatos do inventário que reordenam tudo:

- **o Pro está de pé há 17h25m sem trocar de instância.** Cada perda de link
  cria uma instância HID nova (é assim que se conta, e é como o DualSense
  aparece 8 vezes). O Pro tem **3** desde 01/08 (`.000F`, `.0015`, `.0017`) e
  **nenhuma** nova desde 06/08 22:21. GRAU: MEDIDO;
- **o 8BitDo em PS4 caiu hoje, entre 15:24 e 15:43**, e o bond dele continua no
  BlueZ com `Connected=false`. GRAU: MEDIDO;
- **o daemon reiniciou às 15:27:48** (PID novo). O daemon anterior rodava desde
  antes do commit `6b1cb62` (07/08 02:59), que é o que calou o LED dos externos.
  Isso cria um **A/B natural** que a seção 4 aproveita. GRAU: MEDIDO.

---

## 3. O que o kernel já sabe de cada um

### 3.1 O Pro Controller genuíno (`057e:2009`, driver `nintendo`)

**O descritor HID — MEDIDO** (170 bytes, lidos de
`/sys/class/hidraw/hidraw7/device/report_descriptor`):

| direção | report | tamanho declarado | o que é |
|---|---|---|---|
| entrada | `0x21` | 48 B | resposta de subcomando |
| entrada | `0x30` | 48 B | relatório completo (botões + IMU) |
| entrada | `0x31`, `0x32`, `0x33` | 361 B | dados de MCU/NFC/IR |
| entrada | `0x3F` | 16 botões + hat + 4 eixos de 16 bits | o relatório "simples" de HID puro |
| **saída** | **`0x01`, `0x10`, `0x11`, `0x12`** | **48 B cada** | rumble+subcomando, rumble puro, dados de MCU |

Os nomes batem com o driver desta árvore
(`assets/dkms/hid-nintendo/hid-nintendo.c:120-124`): `JC_OUTPUT_RUMBLE_AND_SUBCMD
0x01`, `JC_OUTPUT_RUMBLE_ONLY 0x10`, `JC_OUTPUT_MCU_DATA 0x11`. GRAU: MEDIDO.

**O que o driver expõe em `/sys` — MEDIDO:**

| recurso | nó | detalhe |
|---|---|---|
| LEDs de player | `0005:057E:2009.<n>:green:player-1..4` | `max_brightness` = **1** |
| 5.º LED | `0005:057E:2009.<n>:blue:player-5` | `max_brightness` = **15** — é o **LED HOME**, não um quinto player |
| bateria | `nintendo_switch_controller_battery_0005:057E:2009.<n>` | **só `capacity_level`**; **não existe `capacity`** |
| rumble | `EV_FF`/`FF_RUMBLE` no nó de input | via `ff_memless` (`hid-nintendo.c:2321-2322`) |
| IMU | nó `Pro Controller (IMU)`, `EV_ABS` 6 eixos | **vivo por Bluetooth** — ver 3.4 |

**Duas correções ao que a árvore acredita, e as duas são MEDIDO:**

1. **o `blue:player-5` é o LED HOME.** O driver o registra com
   `led->max_brightness = 0xF` e `brightness_set_blocking =
   joycon_home_led_brightness_set`, que emite o subcomando
   `JC_SUBCMD_SET_HOME_LIGHT (0x38)` — enquanto os verdes emitem
   `JC_SUBCMD_SET_PLAYER_LIGHTS (0x30)`
   (`hid-nintendo.c:2573-2592`, `:1220-1231`, `:1233`). O
   `core/external_leds.py` o trata como o bit "+5" da numeração (R-25) e escreve
   **`1` num nó cuja escala vai a 15**. Que essa intensidade seja visível na mesa
   dela é **SEM PROVA** — nunca foi olhada;
2. **não existe percentual de bateria no Pro.** O driver só publica
   `POWER_SUPPLY_PROP_CAPACITY_LEVEL` (`hid-nintendo.c:2655-2658`), com cinco
   degraus (`Critical`/`Low`/`Normal`/`High`/`Full`). Agora ele lê `Normal`,
   `Discharging`. **O amostrador da Q-1 do
   [PROTOCOLO de 07/08](2026-08-07-PROTOCOLO-o-controle-que-cai-sozinho.md), que
   lê `capacity`, devolveria `AUSENTE` a noite inteira neste controle.** GRAU:
   MEDIDO. É defeito de instrumento, e está consertado no item E-3 da seção 8.

### 3.2 O 8BitDo em modo PS4 (`054c:05c4`, driver `playstation`)

MEDIDO no journal do kernel de hoje, 15:22:18, na última subida dele:

```
playstation 0005:054C:05C4.001F: Invalid accelerometer calibration data for axis (2), disabling calibration.
playstation 0005:054C:05C4.001F: Failed to get calibration data from DualShock4
playstation 0005:054C:05C4.001F: Gyroscope and accelerometer will be inaccurate.
playstation 0005:054C:05C4.001F: Registered DualShock4 controller hw_version=0x00000000 fw_version=0x00000000
```

O que cada linha prova, e o grau:

- **o clone não implementa os feature reports de calibração nem o de firmware.**
  `hw_version` e `fw_version` saem **zerados**, e a calibração do acelerômetro é
  recusada pelo driver. GRAU: MEDIDO. É por isto que existe o patch DKMS
  `assets/dkms/hid-playstation/patch/0002-HID-playstation-survive-a-DualShock4-pairing-info-rep.patch`;
- **ele registra assim mesmo**, com três nós de input (gamepad, sensores,
  touchpad). GRAU: MEDIDO;
- **ele tem giroscópio neste modo, e ele é impreciso por decisão do driver.** A
  [página do 8BitDo](../../usage/troubleshooting-8bitdo.md) marca esta linha como
  *"não verificado"* e *"pergunta em aberto"*. **Fica respondida aqui:** o nó de
  sensores nasce, e o driver avisa que os valores são inexatos. GRAU: MEDIDO
  para a existência; SEM PROVA para a utilidade dentro de um jogo;
- **neste modo ele NÃO tem barra de player** — tem a lightbar RGB do
  DualShock4 (`inputNN:red|:green|:blue|:global`), que é o caminho `ds4` do
  `resolve_external_leds`. GRAU: MEDIDO (código + a regra udev
  `79-external-controller-leds` ancorada em `DRIVERS=="playstation"`).

### 3.3 O 8BitDo em modo Switch (`057e:2009`, driver `nintendo`)

**Não está na mesa, e não tem bond no adaptador.** GRAU: MEDIDO — a lista de
bonds do BlueZ tem exatamente **três** entradas (seção 5), e nenhuma é o modo
Switch.

O que a árvore já sabe dele, sem precisar dele ligado:

- **ele colide com o Pro genuíno em tudo o que se pode consultar por USB** — VID,
  PID, serial (`000000000001`), `HID_NAME` e `MODALIAS`. O discriminador medido
  é o **`bcdDevice`**: `0210` = genuíno, `0200` = clone
  (`assets/84-nintendo-pro-variant.rules`, regra **instalada** em
  `/etc/udev/rules.d/`). GRAU: MEDIDO;
- **por Bluetooth o discriminador é a OUI**, nunca VID/PID — `e0:f6:b5` para o
  genuíno, `e4:17:d8` para o clone. É a fonte da verdade usada em três lugares
  independentes da árvore (`external_identity.py:200`, `scripts/bt_active_mode.sh`,
  `assets/82-nintendo-pro-nosniff.rules`). GRAU: MEDIDO;
- **os dois têm requisitos de firmware INCOMPATÍVEIS quanto ao sniff**, e isso é
  a medição mais importante já feita nesta frente (A/B de 23/07, transcrito em
  `scripts/bt_active_mode.sh`): com o no-sniff **global**, o 8BitDo acumulou 4
  probes falhadas e 0 sucessos, sempre em `Failed to get joycon info; ret=-110`;
  devolvido o sniff, probou em 54 s na primeira tentativa. GRAU: MEDIDO (a
  medição é de 23/07, e a leitura de hoje confirma que o estado do disco a
  respeita — seção 5).

### 3.4 O quadro comparativo — e o que ele diz do DualSense

Medido nesta máquina, agora, com os controles **parados na mesa**, lendo os nós
de evdev sem `EVIOCGRAB` (leitura pura, 2 s cada):

| | Pro Controller (BT) | DualSense (BT) |
|---|---|---|
| pacotes por segundo (`SYN_REPORT`) | **~268** | **~570** |
| eixos de acelerômetro mudando | sim (1 g estável num eixo, ~4195) | sim |
| eixos de giroscópio mudando | **sim** (310, 304 e 277 mudanças em 2 s) | sim |
| bateria | `capacity_level` (5 degraus) | `capacity` (percentual) |
| indicador de posição | 4 LEDs verdes + LED HOME azul | lightbar RGB + 5 player-LEDs brancos |
| custo de escrever o indicador | **subcomando HID por lâmpada** | escrita de sysfs, sem subcomando |

Duas leituras saem daí:

- **a IMU do Pro por Bluetooth está VIVA, e isso confirma a refutação de 06/08.**
  O acervo dizia que a IMU do Pro *"nasce em STANDBY"* e que por Bluetooth o
  Hefesto não a liga (verdade no código: `_IMU_ENABLE_ALLOWED_BUS = "usb"`). A
  fila de 06/08 já derrubou a **conclusão** disso; a medição de hoje fecha o
  mecanismo: **quem liga é o próprio driver** — `joycon_enable_imu()` é chamado
  incondicionalmente no probe quando o controle tem IMU
  (`hid-nintendo.c:2936-2937`), com `subcmd_id = 0x40` e `data[0] = 0x01`
  (`:1569-1580`), que é **byte a byte** o pacote que o
  `build_enable_imu_packet` monta. GRAU: MEDIDO. Ou seja: o Enable-IMU do
  produto **duplica** o do driver, e não há nada a ligar por rádio;
- **os ~570 Hz do DualSense não são nem os 250 do acervo nem os 1000 do SDL.** É
  piso, não total (o evdev só emite `SYN` quando algo muda). Não é o objeto
  desta página, mas é dado novo para a `GYRO-EDGE-RATE-01`, que a
  [referência canônica](../../protocol/dualsense-referencia-canonica.md) deixa
  aberta. GRAU: MEDIDO como piso.

---

## 4. O que o produto faz com eles hoje — e o defeito que a varredura achou

### 4.1 A superfície de escrita, inteira

O Hefesto **não adota** esses controles: o input deles segue pelo kernel e pela
Steam. A superfície de escrita cabe em duas linhas, e as duas estão em
`src/hefesto_dualsense4unix/core/external_leds.py`:

| caminho | o que escreve | onde | grau declarado pela casa |
|---|---|---|---|
| `apply_player_number` | número do jogador | **sysfs** (`/sys/class/leds/...`) | best-effort, "nunca levanta" |
| `enable_imu` | pacote cru de 12 bytes | **hidraw** | best-effort, só USB, no máximo 2 tentativas |

**A decisão dela de 07/08 desligou o primeiro.**
`EXTERNAL_PLAYER_LED_ENABLED = False`
(`daemon/subsystems/external_identity.py:194`, commit `6b1cb62`, 07/08 02:59) —
E0 da
[LUGAR-A-MESA-01](../sprints/2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md).
Enquanto o externo não for jogador de verdade, **o produto não acende número
nele**. O que continua rodando: a atribuição de lugar, a reconciliação do
registro e o Enable-IMU. GRAU: MEDIDO (leitura do código e do commit).

**E o Enable-IMU nunca disparou por rádio, por construção** — `bus == "usb"` é
gate estrito (`external_identity.py:902`), e nos journais de 06 e 07/08 não há
uma linha de `external_imu_enable_enviado` nem de `external_imu_enable_falhou`.
GRAU: MEDIDO.

Três observações sobre esse pacote, que **não** foram testadas e por isso viram
protocolo (item E-2):

- ele tem **12 bytes**, e o descritor declara o report `0x01` com **48 bytes** de
  corpo. O driver monta o dele com o `struct` completo. Que o firmware honre um
  relatório curto é **SEM PROVA**;
- ele duplica o que o driver já faz no probe (3.4). SUSPEITA COM MECANISMO de
  que seja **inócuo na melhor hipótese e um subcomando a mais na pior**;
- `/dev/hidraw7` do Pro tem ACL para o usuário dela (`getfacl`: `user:vitoriamaria:rw-`),
  então a escrita **teria** permissão. GRAU: MEDIDO — não é o gate de permissão
  que segura, é o gate de barramento.

### 4.2 O defeito vivo: o laço de repintura que não podia terminar

**Este é o achado da varredura, e é MEDIDO ponta a ponta.**

Janela colhida do journal, com o daemon **anterior** ainda de pé:

```
15:24:01.218282  daemon  external_led_written    hidraw=/dev/hidraw7 slot=2
15:24:01.218318  daemon  external_led_repintado  intruso=1
15:24:01.573    kernel  nintendo ...0017: joycon_enforce_subcmd_rate: exceeded max attempts
15:24:01.836    kernel  (idem)
15:24:02.114    kernel  (idem)
15:24:02.394    kernel  (idem)
15:24:02.394    kernel  leds ...0017:green:player-2: Setting an LED's brightness failed (-110)
15:24:03.519    kernel  leds ...0017:green:player-3: Setting an LED's brightness failed (-110)
15:24:04.663    kernel  leds ...0017:green:player-4: Setting an LED's brightness failed (-110)
```

**Uma** chamada de `apply_player_number` no Pro custa: 5 escritas de sysfs,
**12** recusas do rate-limit do kernel e **3** falhas `-110` (`ETIMEDOUT`), em
**3,7 segundos**. GRAU: MEDIDO.

**Por que o laço não podia terminar** — e este é o mecanismo, não a suspeita:

1. o `NUMA-03` manda o tick **reler** o padrão físico com `read_player_pattern`
   antes de pular por cache, e repintar se o padrão lido divergir do slot
   (`external_identity.py`, docstring do `ExternalLedSync`);
2. mas a escrita **falha no meio**: a primeira lâmpada passa, as outras morrem em
   `-110`;
3. logo a releitura devolve **sempre** um número diferente do pedido — é o
   `intruso=1` do log, com `slot=2` pedido;
4. o tick conclui "escritor estrangeiro" e **repinta**;
5. volta ao passo 2, para sempre.

> **NOTA DATADA, 07/08/2026 21h04 — três dos cinco passos acima CADUCARAM, e o
> desfecho desta seção continua de pé.** A refutação está medida ponta a ponta
> na
> [A-LUZ-QUE-CUROU-01](../sprints/2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md),
> seções 2.1 e 2.2. Nada aqui se apaga — o mecanismo escrito acima era a melhor
> leitura de 19h12, e a medição das 21h04 é que o derrubou.
>
> - **Passo 2** (*"a primeira lâmpada passa, as outras morrem em `-110`"*) —
>   **REFUTADO.** O subconjunto que passa é **arbitrário, e não é prefixo**: em
>   **16** episódios no kernel desde 06/08, em **11** deles **todas as cinco**
>   lâmpadas falharam; em 07/08 15:22:13 falhou **só a `player-2`**; em 07/08
>   13:30:15 passaram as **duas últimas**. GRAU: MEDIDO.
> - **Passo 3** (*"a releitura devolve **sempre** um número diferente do
>   pedido"*) — **REFUTADO, e é o oposto do que acontece.** O `brightness` da
>   classe LED é memória do **PEDIDO**: o kernel o grava antes de tentar o
>   hardware e **nunca o reverte** quando a escrita falha. Às 15h24 os cinco nós
>   do Pro liam `1,1,0,0,0` — exatamente o slot 2 pedido às 15:24:01 —, e
>   **três** daquelas cinco escritas tinham falhado com `-110`. GRAU: MEDIDO.
> - **Passo 5** (*"volta ao passo 2, para sempre"*) — **REFUTADO pela
>   aritmética.** Um laço travado no piso de `LED_MIN_INTERVAL_SEC = 2,0 s`
>   produziria da ordem de **34 000** escritas nas 19h04m do lado A. Foram **18**
>   no Pro — uma a cada **63,6 minutos**. GRAU: MEDIDO.
>
> **Os passos 1 e 4 ficam de pé, e o rótulo do passo 4 é que é falso.** O
> "intruso" que o log acusa foi **a nossa própria escrita anterior**, em **11 de
> 11** ocorrências: as repinturas são o daemon perseguindo o próprio eco. E o que
> sobra no lugar do laço é pior que ele — **o detector é cego à falha de
> escrita**, e não existe hoje, em ponto nenhum da árvore, um caminho que saiba
> que uma escrita de LED externo morreu no rádio (83 falhas no kernel contra
> ZERO avisos do daemon na mesma janela). GRAU: MEDIDO.

**A contagem, e ela é a régua:** **348** ocorrências de
`joycon_enforce_subcmd_rate: exceeded max attempts` no kernel desde 01/08 —
**146** em 06/08 e **202** em 07/08, e **zero** entre 01 e 05/08. Mais **83**
falhas `Setting an LED's brightness failed`. GRAU: MEDIDO.

**A honestidade sobre esses zeros:** eles **não** provam que a escrita causa o
storm, porque o Pro só entrou no rádio em 06/08 21:07 — antes disso não havia
nem controle nem escrita. O que é MEDIDO é o **emparelhamento temporal**: cada
`external_led_written` em `hidraw7` é seguido, em ~350 ms, pela cascata. A
causalidade é **SUSPEITA COM MECANISMO**, e o mecanismo está descrito acima.

**E o A/B já começou sozinho.** Desde o reinício do daemon às **15:27:48**, com
`EXTERNAL_PLAYER_LED_ENABLED = False`: **zero** escritas de LED externo e
**zero** `joycon_enforce_subcmd_rate`, com o Pro **conectado o tempo todo**.
GRAU: MEDIDO — mas a janela é de **19 minutos**, curta demais para concluir. É
exatamente esta janela que o item **E-1** da seção 8 manda esticar.

> **NOTA DATADA, 07/08/2026 18h55 — esta janela esticou para 3h27m, e o E-1
> fechou.** Duas frases desta seção caducaram, e ficam escritas assim:
>
> - *"A causalidade é SUSPEITA COM MECANISMO"* — **caducou**. O pareamento
>   minuto a minuto do lado A inteiro (subseção 3 do E-1) mostra **zero** recusas
>   do kernel sem uma `external_led_written` no Pro no mesmo minuto, em quinze
>   episódios, mais a intervenção que zerou os dois juntos. A causa passa a
>   **MEDIDO**: a escrita é nossa e o storm é dela.
> - *"a janela é de 19 minutos, curta demais para concluir"* — **parcialmente
>   caducada**. São 3h27m contra 19h04m do lado A: bastam para a causa do
>   **storm**, não para a previsão de 24 h. O que a janela ainda não cobre está
>   listado na subseção 9 do E-1, item por item.
>
> E a pergunta do título mudou de resposta: o storm **não derruba o Pro** — ele
> ficou 17h06m de pé do lado A tomando 225 recusas. GRAU: MEDIDO.

### 4.3 O que renumera os externos, e por que isso importa

O slot exibido do externo é a colocação dele entre os controles **presentes**.
Quando o DualSense cai e volta, os dois externos são **renumerados**, e cada
renumeração dispara uma escrita de LED. Medido hoje, quatro vezes em 40 minutos:

```
15:23:00  8BitDo slot=2   Pro slot=1
15:23:31  8BitDo slot=3   Pro slot=2
15:23:41  8BitDo slot=2   Pro slot=1
15:24:01  8BitDo slot=3   Pro slot=2
```

GRAU: MEDIDO. É a mesma queixa registrada em 03/08 (*"o Pro Controller foi
renumerado duas vezes em 24 segundos"*), agora com a cadeia inteira à vista: **a
instabilidade do DualSense vira tráfego de subcomando no Pro.** Que este seja o
gatilho principal do storm é SUSPEITA COM MECANISMO.

---

## 5. A pergunta dela sobre a conexão permanente

### 5.1 O que o BlueZ guarda de cada um — MEDIDO agora, via D-Bus

`/var/lib/bluetooth` é `root`-only e **não foi lido** (a máquina está em uso, e
não há razão para pedir senha por isto). O estado veio do
`org.freedesktop.DBus.ObjectManager`, que publica o mesmo conteúdo:

| aparelho | Paired | Bonded | Trusted | Blocked | Connected | ReconnectMode | WakeAllowed |
|---|---|---|---|---|---|---|---|
| Pro Controller (`e0:f6:b5`) | sim | **sim** | **sim** | não | **sim** | `device` | sim |
| DualSense (`a0:fa:9c`) | sim | **sim** | **sim** | não | **sim** | `device` | sim |
| 8BitDo PS4 (`e4:17:d8`) | sim | **sim** | **sim** | não | **não** | `device` | sim |

**São exatamente TRÊS bonds no adaptador.** Não existe bond do 8BitDo em modo
Switch nem do segundo DualSense. GRAU: MEDIDO.

Estado do adaptador, também MEDIDO:

- `Alias` = **`Nintendo MeowSystem`** — o prefixo do `bt_active_mode.sh` está
  aplicado;
- `Link policy` = **`RSWITCH HOLD SNIFF PARK`** — o sniff está no default do
  adaptador, que é o que o clone 8BitDo precisa para probar (o A/B de 23/07);
- `UP RUNNING PSCAN` — o host **escuta** (page scan), e **não** está
  descobrível (sem `ISCAN`), que é o correto para quem já pareou;
- as regras `82-nintendo-pro-nosniff.rules` e `84-nintendo-pro-variant.rules`
  estão **instaladas** em `/etc/udev/rules.d/`.

### 5.2 O que "permanente" pode e não pode significar — o mecanismo

**`ReconnectMode = "device"` nos três.** Essa propriedade do `org.bluez.Input1`
não é escolha do host: o BlueZ a deriva dos atributos SDP `HIDReconnectInitiate`
e `HIDNormallyConnectable` que **o próprio controle publica**. `device` quer
dizer: **só o controle inicia a reconexão; o host não puxa.** GRAU: MEDIDO para
o valor; MÉDIA (documentação do BlueZ) para a semântica.

Consequência exata, e ela redefine a pergunta dela:

> **Não existe ajuste no host que mantenha o link de pé com o controle
> desligado.** O host já faz tudo o que lhe cabe — bond guardado, trust dado,
> page scan ligado. O que falta é do lado do controle: ele precisa **estar
> ligado** e **querer voltar**.

Isso deixa **quatro** hipóteses vivas para "a conexão não é permanente", e só
elas:

| # | hipótese | grau hoje | fecha com |
|---|---|---|---|
| H1 | **a carga acaba** e o controle desliga | SUSPEITA COM MECANISMO (é a Q-1 de 07/08) | uma noite de amostragem |
| H2 | **o firmware do controle tem timer próprio de ociosidade** | SEM PROVA para o Pro e para o 8BitDo | E-4 |
| H3 | **o controle re-pareia noutro host e esquece este** (Switch por cabo, celular) | SEM PROVA aqui, mecanismo conhecido | E-5 |
| H4 | **o link cai sob carga por negociação de sniff** | MEDIDO para o Pro **antes** da cura de 23/07; **SEM PROVA de que a cura ainda vale hoje** | E-1 |

**O que NÃO está na lista, e por escrito:** *"o controle dorme por
inatividade"*, no sentido **host**. A
[nota datada de 07/08](2026-08-07-PROTOCOLO-o-controle-que-cai-sozinho.md), seção 2,
matou isso por dois caminhos independentes — duas sessões Bluetooth de mais de
quinze horas, e o `IdleTimeout` do perfil HID em `0` sem nenhum arquivo o
sobrescrevendo. **Não reabrir.** A H2 acima é **outra** pergunta: é o timer do
**firmware do controle**, que nenhuma medição desta casa alcançou, e que a
leitura de hoje mostra ser improvável no Pro (17h25m de pé) e por medir no
8BitDo.

E uma nota de honestidade que a H1 exige: a queda **de hoje** do DualSense
aconteceu com ele **carregando desde os 5%**, o que é o cenário em que a bateria
explica mais, não menos.

### 5.3 O que fica MEDIDO sobre a permanência, sem ela tocar em nada

- **o Pro genuíno não tem problema de permanência nesta mesa, agora.** 17h25m
  contínuas, 3 links em 7 dias. GRAU: MEDIDO;
- **o 8BitDo em PS4 caiu hoje** e o BlueZ o mantém bondado e trusted, esperando
  ele voltar. GRAU: MEDIDO;
- **quem cai é o DualSense** — 8 instâncias em 7 dias, e 26 (re)conexões contadas
  pelo mesmo caminho na fila de 07/08. GRAU: MEDIDO;
- **o bond do 8BitDo em modo Switch não existe**, então qualquer teste daquele
  modo começa por um pareamento novo — e é por isso que ele é o item mais caro
  desta página. GRAU: MEDIDO.

---

## 6. O que a referência canônica diz sobre eles — e o que ela não diz

**Ela não diz nada.** `grep -i -E "pro controller|8bitdo|nintendo|057e|05c4"` na
[referência canônica](../../protocol/dualsense-referencia-canonica.md) devolve
**zero linhas**. GRAU: MEDIDO.

Isso é coerente com o título dela — é a referência **do DualSense** — mas cria um
buraco real: **não existe, nesta casa, um documento com grau de confiança por
linha sobre o que o Pro e o 8BitDo entendem.** O que existe está espalhado em
docstrings de código, em comentários de regra udev e em páginas de uso, e nenhum
desses lugares carrega grau no formato da casa.

**Achado colateral, e ele é um defeito de acervo:** duas docstrings da árvore
citam estudos que **não existem no repositório**:

- `core/external_leds.py:24` e `external_identity.py:66` apontam para
  `docs/process/estudos/2026-07-19-estudo-gyro-universal-vpad.md`; <!-- ref-externa: a ausência deste arquivo é o assunto do parágrafo -->
- `scripts/bt_active_mode.sh` aponta para
  `docs/process/estudos/2026-07-22-pesquisa-pro-controller-bt-e-lightbar-keepalive.md`. <!-- ref-externa: a ausência deste arquivo é o assunto do parágrafo -->

<!-- ref-externa: as duas linhas acima citam arquivos que NÃO existem; essa é a informação -->


Nenhum dos dois está no disco (`ls`, 07/08). GRAU: MEDIDO. Quem for verificar a
proveniência do Enable-IMU ou do modo ativo **não tem onde**. Não é objeto desta
página curar isso; fica registrado com data.

**O que esta página propõe como destino do conhecimento**, e é decisão dela:
uma referência canônica **por linhagem** — `nintendo-referencia-canonica.md` —
com as mesmas colunas de grau. As seções 3 e 5 desta página são o rascunho dela.
Nada disso deve virar arquivo antes de ela dizer que quer.

---

## 7. O que já dá para afirmar sem gastar minuto dela

Colhido nesta varredura, sem hardware na mão além do que já estava ligado:

| # | afirmação | GRAU |
|---|---|---|
| 1 | o Pro tem giroscópio vivo por Bluetooth, e quem o liga é o driver, não o Hefesto | MEDIDO |
| 2 | o `blue:player-5` do Pro é o LED HOME, escala 0-15, e o produto escreve `1` nele | MEDIDO |
| 3 | o Pro não publica percentual de bateria — só cinco degraus | MEDIDO |
| 4 | o 8BitDo em PS4 registra sensores, com calibração recusada pelo driver | MEDIDO |
| 5 | escrever o LED do Pro custa 12 recusas de rate-limit e 3 `-110` por chamada | MEDIDO |
| 6 | o laço de repintura não pode terminar enquanto a escrita falhar no meio | MEDIDO (mecanismo derivado do código + log) |
| 7 | a renumeração dos externos é disparada pela queda/volta do DualSense | MEDIDO |
| 8 | os três bonds estão íntegros, com trust, e `ReconnectMode=device` | MEDIDO |
| 9 | nenhum ajuste de host reconecta controle desligado | MEDIDO (o valor) + MÉDIA (a semântica) |
| 10 | quem cai nesta mesa é o DualSense, não o Pro | MEDIDO |
| 11 | o storm de subcomando **causa** as quedas | **SUSPEITA COM MECANISMO** |
| 12 | o Enable-IMU de 12 bytes é honrado pelo firmware | **SEM PROVA** |
| 13 | o 8BitDo em PS4 tem timer próprio de ociosidade | **SEM PROVA** |

**NOTA DATADA, 07/08/2026 18h55 — o E-1 fechou e mexeu em duas linhas desta
tabela.** A tabela fica como está; a correção é esta:

| # | o que mudou | GRAU novo |
|---|---|---|
| 11 | **quebrou em duas.** *"a escrita do Hefesto causa o storm"* — o pareamento 1:1 de quinze episódios mais a intervenção fecham a causa | **MEDIDO** |
| 11 | *"o storm causa as quedas"*, **para o Pro** — do lado A ele levou 225 recusas e 54 `-110` com o link intacto por 17h06m; não houve queda para o storm causar | **REFUTADA nesta janela** |
| 14 | **linha nova:** não há segundo escritor da barra do Pro — nenhuma recusa do kernel sem uma escrita nossa no mesmo minuto, no boot inteiro | **MEDIDO** nesta janela |

Para o **8BitDo**, a linha 11 continua **SUSPEITA COM MECANISMO**: quem a decide
é o **E-4**, e o E-1 não o antecipa.

---

## 8. O protocolo — cinco medições, nesta ordem

Convenção: **P0** tranca (com o destrancar embutido); **ANTES** é foto numérica;
**CONTRASTE** é o caso sem o qual nada se conclui; **PREVISÃO** é falsificável e
derivada do código; **ELA** / **ASSISTENTE** é a divisão de trabalho;
**LEITURA** é a tabela escrita antes de medir.

**Custo total da sessão: 70 minutos de atenção dela, mais duas noites de
espera sem atenção nenhuma.** Os itens E-1 e E-4 rodam sozinhos; E-2, E-3 e E-5
pedem a mão dela.

**Ordem combinada com a decisão dela de 07/08** (a próxima sessão de hardware
começa pelo protocolo de 06/08): **isto vem depois**, e o E-1 pode rodar **em
paralelo** com qualquer item daquela fila, porque não pede atenção.

> **Estado da fila em 07/08/2026, 18h55:** **E-1 FECHADO** (custou os zero
> minutos previstos). Restam **quatro**: E-2, E-3, E-4 e E-5 — e o custo total
> de atenção dela cai de 70 para **70 minutos**, porque o E-1 já custava zero.
> O que o E-1 entregou de aproveitável para as outras quatro está na subseção 11
> dele.

---

### E-1. O storm de subcomando derruba o Pro? — **FECHADO em 07/08/2026, 18h55**

> **Estado: FECHADO.** O título deste item, como foi escrito às 16h de hoje, era
> *"E-1. O storm de subcomando derruba o Pro? (a que decide, e já está meio
> montada)"* — fica registrado aqui, porque a única coisa que mudou nele foi o
> estado. É a **primeira** medição desta fila a fechar, e a **primeira** do
> protocolo dos externos a fechar em geral. O desenho abaixo fica
> escrito palavra por palavra — inclusive a previsão que só se cumpriu pela
> metade — e o resultado vem depois da LEITURA, na subseção
> [E-1 fechado](#e-1-fechado--07082026-18h55). Custo real de atenção dela: **zero
> minuto**, como previsto.

**Pergunta.** Com o LED externo calado, o Pro Controller passa **mais** tempo de
pé do que com ele falando?

**Por que é a primeira.** É a **única** desta lista em que o Hefesto pode ser o
culpado, e o A/B **já começou sozinho** às 15:27:48 de hoje. Custo: **0 minutos
de atenção dela**, uma noite de relógio.

**A hipótese, com o mecanismo.** Cada `apply_player_number` no Pro produz 12
recusas de rate-limit e 3 `-110` em 3,7 s (seção 4.2), e o laço de repintura o
repete a cada renumeração. A `EXT-04` registra que foi subcomando em excesso que
fez o `hid-nintendo` **desregistrar** o 8BitDo. GRAU: SUSPEITA COM MECANISMO.

**P0 — trancar.**

1. **Não reiniciar o daemon.** O daemon de pé desde 15:27:48 de 07/08 **é** o
   lado B do experimento — ele já roda com `EXTERNAL_PLAYER_LED_ENABLED = False`.
   Reiniciá-lo não invalida, mas zera o cronômetro.
2. Parar o `hefesto-bt-health-watchdog.timer` **não** serve aqui: ele é parte do
   ambiente que produziu o lado A. **Deixar como está**, e **anotar** que estava
   `active` (está, e dispara a cada 2 min — MEDIDO 07/08 15h48).
3. Conferir que a **suíte de testes não está rodando** — ela suja o journal do
   sistema.
4. **Destrancar:** nada a religar. Registrar por escrito que o lado B usou o
   commit `6b1cb62`.

**ANTES.** A régua do lado A já está colhida e é esta, e não se remede:

| métrica, 06/08 21:07 a 07/08 15:27 (LED falando) | valor |
|---|---|
| escritas de LED no Pro (`hidraw7`) | 14 |
| `joycon_enforce_subcmd_rate` | 348 |
| `Setting an LED's brightness failed` | 83 |
| instâncias HID novas do Pro | 1 (a `.0017`, de 06/08 22:21) |

**CONTRASTE.** O **DualSense** é o controle negativo: ele não passa pelo
`hid-nintendo` e não recebe subcomando nenhum. Se a taxa de quedas **dele** mudar
junto, o que mudou foi o rádio, não o storm — e a rodada não diz nada sobre o
Pro.

**PREVISÃO, derivada do código.** Com o LED calado: **zero**
`joycon_enforce_subcmd_rate` e **zero** `-110` numa janela de 24 h com o Pro
ligado, e **zero** instâncias HID novas do Pro. **Se aparecer uma única linha de
`joycon_enforce_subcmd_rate` com o gate `False`, existe um segundo escritor** —
e achar quem é passa a ser o alvo, porque o produto não é o único a mexer nessa
barra.

**ELA.** Usa o Pro como sempre, inclusive com rumble e vários jogadores — a carga
é parte do teste. Nada mais.
**ASSISTENTE.** Ao fim da janela, conta pelo **kernel** nos dois lados (instâncias
HID novas do Pro), nunca pelo `probe_offline` do daemon — a régua tem de ser a
mesma dos dois lados, e essa é a armadilha que inventou resultado na Q-2 de
07/08.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| zero storm e zero link novo em 24 h, com carga | o storm era nosso, e a cura já está no disco | vira **nota datada**: a `EXT-04` alcançava o Pro também; e a volta do LED (E3 da LUGAR-A-MESA-01) **precisa** de escrita idempotente antes |
| zero storm, mas o Pro cai assim mesmo | o storm não era a causa da queda | a hipótese 11 morre; sobram H1/H2/H3 |
| storm aparece com o gate `False` | há um segundo escritor da barra | achado novo e mais grave — achar quem escreve vira o alvo |
| o Pro nem fica ligado 24 h | a janela não pegou o fenômeno | anotar a duração real; **não concluir nada** |
| o DualSense muda de taxa junto | contraste falhou | queda geral de rádio — descartar a rodada |

---

#### E-1 FECHADO — 07/08/2026, 18h55

**Como foi conferido.** Tudo por `journalctl -k` e pelo journal do usuário na
unidade `hefesto-dualsense4unix.service`, com **data completa em toda janela**
(nota de instrumento nº 2 da seção 9). Leitura pura: nenhum serviço reiniciado,
nenhum controle derrubado, nenhuma escrita em hidraw. A máquina dela estava
**em uso** durante toda a contagem.

**O P0 foi respeitado.** O daemon de 15:27:48 seguiu de pé até a contagem —
`NRestarts=0`, `ExecMainStartTimestamp=Fri 2026-08-07 15:27:48 -03`. GRAU:
MEDIDO. O `hefesto-bt-health-watchdog.timer` continua `active`, como mandado. A
suíte de testes não rodou na janela.

**O código do lado B, com precisão maior que a do P0.** O P0 mandou registrar
"commit `6b1cb62`". O HEAD da árvore às 15:27:48 era **`18aa9a3`** — mas o
`external_identity.py` **não foi tocado por nenhum commit depois do `6b1cb62`**,
e não tinha diferença não commitada na hora da contagem. Logo o caminho do LED
do lado B **é** o do `6b1cb62`, e o `6b1cb62` mexeu nesse arquivo **só somando**
o portão (70 linhas inseridas, nenhuma removida). O A/B é limpo neste eixo: entre
o lado A e o lado B, a **única** diferença no caminho do LED externo é a
constante. GRAU: MEDIDO.

##### 1. O relógio dos dois lados — e a assimetria que enfraquece o lado B

| lado | janela | duração | GRAU |
|---|---|---|---|
| **A** — a luz falando | 06/08 20:23:12 (1.ª recusa do boot) a 07/08 15:27:48 | **19h04m** | MEDIDO |
| **B** — a luz calada | 07/08 15:27:48 a 07/08 18:55 (hora da contagem) | **3h27m** | MEDIDO |

**O lado B é 5,5 vezes mais curto que o lado A.** Quem ler "348 contra 0" e
parar aí lê mais do que está escrito — a subseção 5 abaixo mede exatamente
quanto vale esse zero.

**Nota datada sobre a tabela ANTES, 07/08/2026.** A tabela ANTES rotula a janela
do lado A como *"06/08 21:07 a 07/08 15:27"* e escreve **348**. Os 348 são o
total do boot e começam às **20:23:12** — **103** deles caem **antes** das 21:07,
em quatro minutos (20:23, 20:50, 20:53 e 20:54) que começam no minuto em que o
Pro entrou no rádio pela primeira vez. Dentro do rótulo literal são **245**. O número não muda de sentido (é o total com a luz falando, e
é o que a seção 4.2 já quebrava certo em 146 + 202), mas o **rótulo estava 44
minutos atrasado**. A tabela fica como está; esta nota é a correção. GRAU:
MEDIDO.

##### 2. Os números, conferidos no kernel

| métrica | lado A (19h04m) | lado B (3h27m) | GRAU |
|---|---|---|---|
| `joycon_enforce_subcmd_rate: exceeded max attempts` | **348** | **0** | MEDIDO |
| `Setting an LED's brightness failed (-110)` | **83** | **0** | MEDIDO |
| `external_led_written` no Pro | **18** | **0** | MEDIDO |
| `external_led_repintado` (o laço da seção 4.2) | **11** | **0** | MEDIDO |
| instâncias HID novas do Pro | **3** | **0** | MEDIDO |
| instâncias HID novas do DualSense (o **contraste**) | **5** | **1** | MEDIDO |

Custo médio por escrita, do lado A: **19,3** recusas de rate-limit por
`external_led_written` no Pro (348 / 18) — coerente com as 12 medidas numa
chamada isolada na seção 4.2, com a diferença por conta das repinturas do laço.
GRAU: MEDIDO.

##### 3. O que fecha a causa, e não é a contagem bruta

A prova não são os 348. São os **minutos**. Estes são todos os minutos do boot em
que o kernel recusou subcomando, e todos os minutos em que o daemon escreveu o
LED **do Pro** — as duas listas, lado a lado:

```
minuto   recusa do kernel   escrita nossa no Pro
06/08 20:23      x23               x1
06/08 20:50      x40               x2
06/08 20:53      x20               x1
06/08 20:54      x20               x1
06/08 21:07      x20               x1
06/08 22:21      x23               x1
07/08 01:56      x27               x1
07/08 01:57       x5                -     <- cauda dos 3,7 s da escrita de 01:56
07/08 13:30      x14               x1
07/08 14:34      x20               x1
07/08 14:37      x20               x1
07/08 14:38      x39               x2
07/08 15:22       x4               x1
07/08 15:23      x60               x3
07/08 15:24      x13               x1
--------------------------------------------
lado B (3h27m)    0                 0
```

**Nenhuma recusa sem escrita nossa. Nenhuma escrita nossa sem recusa.** Quinze
minutos de recusa, catorze minutos de escrita, e o único descasado é o `01:57`,
que é a cauda da cascata de 3,7 s aberta no minuto anterior — o mesmo formato
medido na seção 4.2. GRAU: MEDIDO.

Isso **descarta a linha mais grave da LEITURA**: não existe segundo escritor da
barra do Pro nesta janela. GRAU: MEDIDO — para esta janela, esta mesa e estes
aparelhos, e só.

##### 4. O par que vale mais que a contagem — o "evento 6" desta rodada

O método da seção 1 diz que o que fecha causa é o **par**, não a série. Aqui ele
existe, e é o gatilho da seção 4.3:

- **Lado A.** Cada volta do DualSense ao rádio produziu escrita **e** storm no
  **mesmo minuto**: 14:34:43, 14:38:04, 15:22:09, 15:23:26 e 15:23:56 — cinco
  gatilhos, cinco episódios. GRAU: MEDIDO.
- **Lado B.** O DualSense caiu e voltou **uma** vez, às **18:41:38**, com os
  mesmos dois externos na mesa e o mesmo rádio. O daemon estava vivo e
  processou a volta (`motion_sensors_started` às 18:41:42,
  `hidraw_broker_hidden` a cada 30 s sem falha). Resultado: **zero** escrita,
  **zero** recusa. GRAU: MEDIDO.

**O mesmo estímulo, o desfecho oposto, com a intervenção no meio.** Não é o
controle negativo *simultâneo* da noite da lightbar — é um gatilho repetido
através da cura, que é mais fraco. Mas é o par, e ele existe.

##### 5. O contraste segurou — não foi uma tarde de rádio calmo

| lado | links novos do DualSense | por hora | GRAU |
|---|---|---|---|
| A (18h20m, do rótulo da tabela ANTES) | 5 | **0,27/h** | MEDIDO |
| B (3h27m) | 1 | **0,29/h** | MEDIDO |

A taxa de queda do **controle negativo** não mudou. A linha *"o DualSense muda de
taxa junto — descartar a rodada"* da LEITURA **não** se aplica: o rádio não ficou
melhor, só a nossa boca ficou fechada. GRAU: MEDIDO.

O que enfraquece o lado B não é o rádio, é o **relógio**: 3h27m e **um** gatilho
de renumeração, contra 19h04m e quinze episódios. Contando por **episódio** — que
é a unidade honesta, porque as recusas chegam em rajadas de vinte — o lado A teve
**15 episódios em 19h04m** (0,79/h) e o lado B teve **0 em 3h27m**. Se a taxa não
tivesse mudado, o esperado no lado B seriam **2,7 episódios**, e ver zero por
acaso tem probabilidade de cerca de **7%** por Poisson. Sozinho, isso **não**
fecha nada. O que fecha é o pareamento 1:1 da subseção 3 mais o mecanismo do
código: com o portão em `False` o `tick` **retorna antes do laço de escrita**
(`external_identity.py`, o `if not EXTERNAL_PLAYER_LED_ENABLED: return`), então
zero escrita no lado B é **determinístico**, não sorte. GRAU: MEDIDO.

##### 6. O Pro ficou de pé o tempo todo — e já estava de pé antes

O Pro está na **mesma** instância HID `0005:057E:2009.0017` desde **06/08
22:21:11**, sem nenhuma instância nova depois disso, e estava emitindo relatório
de IMU no minuto da contagem. São **20h33m** de link ininterrupto: **17h06m** do
lado A e **3h27m** do lado B. GRAU: MEDIDO. Bate com o olho dela às 18h: *"segue
conectado"*.

**E isto responde o título com um "não" que ninguém tinha previsto.** Contado no
intervalo `06/08 22:21:11` (nascimento da `.0017`) a `07/08 15:27:48` (o corte),
ainda **dentro do lado A**: o Pro atravessou **225** recusas de rate-limit e
**54** falhas `-110` **sem soltar o link uma vez sequer**. As três instâncias
dele nasceram todas nas duas primeiras horas em que entrou no rádio (20:23,
21:07, 22:21) e nunca mais. **O storm existe, é nosso, e não derruba o Pro.**
GRAU: MEDIDO para esta janela.

A pergunta literal do E-1 — *"passa mais tempo de pé?"* — **não pôde ser
medida**, porque o Pro nunca esteve caindo: não há queda para reduzir. O
desfecho real não é nenhuma das cinco linhas da LEITURA; é uma sexta, e está
escrita aqui.

##### 7. Nota de operação: a barra ficou congelada, e isso é o preço aceito

Os LEDs do Pro estão em `player-1=1, player-2=1, player-3=0, player-4=0` — o
padrão que a última escrita, a das 15:24:01, deixou. Com o portão fechado o
Hefesto **não apaga**, só para de escrever (é o que a docstring da constante
manda, e é a diferença entre calar e mentir ao contrário). Consequência prática:
a barra do externo **congela no último número que recebeu** e não acompanha mais
nada. Isso não é defeito novo — é exatamente o custo que a decisão 12 aceitou, e
está aqui para ninguém o redescobrir como surpresa. GRAU: MEDIDO.

##### 8. O que o E-1 fecha, com grau

1. **A escrita de LED do Hefesto no Pro CAUSA o storm de subcomando.** Sobe de
   **SUSPEITA COM MECANISMO** (seção 4.2) para **MEDIDO**: pareamento 1:1 em
   quinze episódios ao longo de 19h, mais a intervenção que zerou os dois juntos,
   mais o mecanismo lido no código.
2. **Não há segundo escritor da barra do Pro.** MEDIDO nesta janela.
3. **O storm não derruba o Pro.** MEDIDO nesta janela: 225 recusas e 54 `-110`
   com o link intacto. Para o Pro, a hipótese 11 da seção 7 fica **REFUTADA
   nesta janela** — o storm não é o mecanismo da queda dele, porque não houve
   queda dele.
4. **A decisão 12 dela curou um defeito técnico real.** 348 recusas de kernel e
   83 falhas de escrita em dois dias pararam, sem que ninguém tivesse pedido.
   MEDIDO.

##### 9. O que o E-1 NÃO prova — e esta lista é maior que a de cima

1. **Que a luz era a ÚNICA causa do bombardeio.** O pareamento 1:1 exclui um
   segundo escritor **nesta janela, nesta mesa, com estes dois externos**. Não
   exclui um que só apareça com o Pro no cabo, com um jogo segurando o hidraw,
   com quatro controles no rádio, ou com o 8BitDo em modo Switch. SEM PROVA
   fora da janela.
2. **Que o Pro não cairia por outro motivo.** Ele não caiu em 20h33m — mas as
   três quedas que teve foram todas nas duas primeiras horas dele no rádio, e
   **nenhuma** janela mediu o Pro sob rádio carregado. **H1, H2, H3 e H4 da
   seção 7 continuam vivas**, e o E-5 continua devendo a H3.
3. **Que o 8BitDo morreu pelo mesmo mecanismo.** A `EXT-04` continua sendo o que
   era: relato com mecanismo. Quem fecha isso é o **E-4**, e o E-1 não o
   antecipa.
4. **Que a previsão foi cumprida.** A PREVISÃO pedia **24 h com carga**. O que
   existe são **3h27m**. Ela está cumprida **na direção** e **não no tamanho** —
   e a única honestidade possível aqui é escrever isso, não arredondar. Recontar
   amanhã custa zero: o daemon está de pé e a régua é a mesma.
5. **Que a luz pode voltar como estava.** Voltar sem escrita idempotente devolve
   o laço inteiro da seção 4.2, porque o laço nasce da escrita que **falha no
   meio**, não do número. A **E3 da LUGAR-A-MESA-01** herda isto como
   pré-requisito medido, não como sugestão.
6. **Um A/B de um lado só não vira lei.** Este é o parágrafo que o E-1 existe
   para deixar escrito.

##### 10. O achado sobre MÉTODO — e ele é maior que o achado sobre o Pro

A decisão 12 dela — *"calar a luz até a entrega existir"*, tomada em 07/08 às
01h45 — **não foi tomada por defeito nenhum**. Foi tomada por **honestidade**:
enquanto o externo não for jogador de verdade dentro do jogo, o produto não podia
acender um número afirmando que era. Nenhuma linha daquela decisão fala de rádio,
de subcomando ou de `-110`.

E aquela constante desligou **348 recusas de kernel e 83 falhas de escrita em
dois dias** que ninguém sabia que existiam. O defeito foi descoberto **doze horas
depois** da cura já estar no disco — a varredura de hoje achou o laço já morto.

**A regra que sai daqui:**

> **Parar de afirmar o que não se entrega apaga trabalho que ninguém tinha
> medido.** Uma decisão de honestidade não é só higiene de produto: ela remove
> caminho de código que estava custando alguma coisa em algum lugar — e o custo
> só aparece se alguém for medir.

**E o corolário operacional, que é o que dá para executar:** quando uma decisão
de honestidade desligar um caminho, **medir o que ela apagou**, no journal, dos
dois lados do corte. O A/B nasce montado e de graça — o lado A é o passado, o
lado B começa no reinício, e o custo de atenção dela é **zero**. Foi assim que
esta página fechou.

GRAU: **MEDIDO uma vez.** Uma ocorrência não é lei, e esta linha fica com essa
ressalva colada. Mas conferir custa um `journalctl`, e desta vez pagou.

##### 11. O que fica de tarefa

- **Recontar amanhã**, com as 24 h que a PREVISÃO pedia. Custo zero, mesma régua,
  mesmo comando. Se aparecer **uma** linha de `joycon_enforce_subcmd_rate` com o
  portão em `False`, a subseção 3 muda de sinal e existe segundo escritor.
- **E3 da LUGAR-A-MESA-01** herda o pré-requisito da subseção 9.5: escrita
  idempotente **antes** de a luz voltar.
- **E-4** continua devendo o 8BitDo. O E-1 não o responde.
- **Q-2 do PROTOCOLO de 07/08** ganhou um dado, e ele está anotado lá.

---

### E-2. O Enable-IMU de 12 bytes faz alguma coisa? *(o único write nosso)*

**Pergunta.** O pacote de 12 bytes que o `build_enable_imu_packet` monta é honrado
pelo firmware, ou o firmware espera os 48 bytes do descritor?

**Por que existe.** É a **única** escrita em hidraw que o produto faz num
externo, e ela nunca foi exercitada — nem por cabo, que é o único barramento em
que o gate a permite. Custo: **10 minutos**.

**O que a varredura já respondeu, e muda a pergunta.** Por Bluetooth **não há
nada a ligar**: a IMU já está viva, ligada pelo próprio driver no probe (seção
3.4). Logo esta medição é **estritamente sobre o caminho USB** — e o que ela
decide é se o `ExternalImuEnabler` deve **existir**.

**P0 — trancar.**

1. **O Pro no CABO**, não no rádio — é o único barramento em que o gate
   `bus == "usb"` deixa passar, e é onde o `bcdDevice=0210` distingue o genuíno
   do clone.
2. Conferir que `/dev/hefesto/nintendo-pro` apareceu — a ausência do symlink
   **é ela mesma** o sinal de que a probe não concluiu
   (`assets/84-nintendo-pro-variant.rules`).
3. **Destrancar:** tirar o cabo no fim e conferir que ele volta pelo rádio.

**ANTES.** Com o Pro no cabo, **antes** de qualquer escrita: a taxa de pacotes do
nó `Pro Controller (IMU)` e se os eixos mudam, medidos do mesmo jeito da seção
3.4 (leitura pura de evdev, 2 s, sem `EVIOCGRAB`). Mais o `dmesg` da janela.

**CONTRASTE.** A **mesma** leitura por Bluetooth, na mesma sessão. Ela já é
conhecida (~268 Hz, seis eixos mudando) e serve de positivo: se por cabo a IMU
já vier viva **antes** do nosso pacote, não há o que ligar em barramento nenhum,
e o componente inteiro é código morto.

**PREVISÃO, derivada do código.** O driver chama `joycon_enable_imu()` no probe
**em todo barramento** (`hid-nintendo.c:2936`), sem gate de bus. Previsão: **a
IMU já vem viva por cabo**, e o pacote do produto não muda nada mensurável.
**Se por cabo a IMU vier morta e o nosso pacote a acordar**, o componente se
justifica — e o pacote de 12 bytes é honrado, o que é resultado por si só.

**ELA.** Liga o Pro no cabo e avisa. Depois tira.
**ASSISTENTE.** Mede a IMU antes, dispara **um** `enable_imu` pelo caminho do
produto (nunca à mão), mede depois, e lê o `dmesg` da janela procurando
`joycon_enforce_subcmd_rate`.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| IMU já viva por cabo antes do pacote | o `ExternalImuEnabler` é **código morto** | remover é higiene com prova; a docstring caduca com nota datada |
| IMU morta por cabo e viva depois do pacote | o pacote curto **é honrado** | o componente se justifica; e o "12 vs 48 bytes" fecha como não-problema |
| IMU morta antes e depois, e o `dmesg` acusa rate-limit | o pacote **não** é honrado | remover, e registrar que relatório curto não passa |
| a probe do cabo nem conclui (sem symlink) | é o defeito do patch 0003, não este | outro alvo; descartar a rodada |

---

### E-3. Quanto dura a carga do Pro, e com que régua? *(o instrumento que falta)*

**Pergunta.** Existe régua de bateria utilizável no Pro, e ela explica alguma
queda?

**Por que existe.** Porque o amostrador da **Q-1** do protocolo de 07/08 lê
`capacity`, e **esse arquivo não existe neste controle** (seção 3.1) — ele
gravaria `AUSENTE` a noite inteira e o resultado seria sobre o instrumento.
Custo: **5 minutos** para montar, depois roda sozinho.

**P0 — trancar.** Nenhum guarda. O que tranca é **declarar a régua**: o Pro dá
cinco degraus (`Critical`/`Low`/`Normal`/`High`/`Full`), o DualSense dá
percentual, e **os dois não se comparam**. Escrever isso no cabeçalho do arquivo
de amostras é passo do protocolo. **Destrancar:** matar o laço no fim.

**ANTES.** Uma leitura de cada nó, no mesmo instante, com `date -Is`:

```
cat /sys/class/power_supply/nintendo_switch_controller_battery_0005:057E:2009.*/capacity_level
cat /sys/class/power_supply/nintendo_switch_controller_battery_0005:057E:2009.*/status
```

**O amostrador corrigido** (o da Q-1, com o campo certo; roda na janela `OS`):

```bash
no=$(echo /sys/class/power_supply/nintendo_switch_controller_battery_0005:057E:2009.*)
while :; do
  printf '%s\t%s\t%s\n' "$(date -Is)" \
    "$(cat "$no/capacity_level" 2>/dev/null || echo AUSENTE)" \
    "$(cat "$no/status"         2>/dev/null || echo AUSENTE)"
  sleep 60
done | tee ~/pro-bateria-$(date +%F).tsv
```

O arquivo resultante **não vai para o repositório** — o caminho traz a instância
HID, e a linha de baixo traz o endereço. Máscara da casa se virar evidência.

**CONTRASTE.** O mesmo laço no **DualSense**, com `capacity`. Sem as duas séries
lado a lado não se distingue "a carga do Pro acabou" de "o rádio ficou ruim para
todo mundo".

**PREVISÃO, derivada do driver.** O nó do Pro **some** junto com o link (é filho
da instância HID). Previsão: a última amostra antes de uma queda vem `Low` ou
`Critical`, **ou** o nó some sem aviso nenhum — e o segundo caso é o mais
provável, porque o Pro está de pé há 17h. **Se a última amostra vier `Normal` ou
acima, a bateria não explica aquela queda** — um caso basta.

**ELA.** Nada, além de não pôr o Pro no cabo durante a janela.
**ASSISTENTE.** Deixa os dois laços rodando e, no instante em que ela avisar de
qualquer queda, colhe as últimas 30 linhas dos dois e o journal do kernel de
-60 s a +10 s.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| última amostra `Low`/`Critical` e o nó some | bateria explica **aquela** queda | a régua de cinco degraus basta; nada a construir |
| última amostra `Normal` ou acima | bateria **não** explica | a H1 cai para o Pro; sobram H2/H3/H4 |
| o nó some sem nenhuma amostra baixa, sempre | o instrumento morre junto com o objeto | amostrar por `daemon.state_full`, que sobrevive ao sumiço do nó |
| o Pro não cai em duas noites | o fenômeno não aparece nele | **registrar a duração** — é o dado que falta para dizer "estável" com número |

---

### E-4. O 8BitDo em PS4 cai por conta própria, com o rádio limpo?

**Pergunta.** Com o LED externo calado e sem storm nenhum, o 8BitDo em modo PS4
sobrevive a uma noite?

**Por que existe.** Ele **caiu hoje**, entre 15:24 e 15:43, e o bond continua de
pé esperando. A causa nunca foi isolada, e ele é o único dos dois que passa pelo
`hid-playstation` — logo **não** sofre o rate-limit de subcomando do
`hid-nintendo`. Custo: **0 minutos de atenção dela**, uma noite. Roda **junto**
com o E-1.

**P0 — trancar.** O mesmo do E-1, mais um: **o 8BitDo em modo PS4**, ligado com
**`Start + A`** (MEDIDO com ela em 03/08 — `X+Start` é X-input e `Y+Start` é
Switch; **vários documentos do acervo mandam para o modo errado**, não copiar
combo de sprint velha). **Destrancar:** nada.

**ANTES.** O objeto D-Bus dele, com `Connected`, `Bonded` e `Trusted`; e a
instância HID atual (`0005:054C:05C4.<n>`).

**CONTRASTE.** O **Pro** na mesma janela. Se os dois caírem no mesmo minuto, a
causa é do **rádio** e não do aparelho — é o mesmo contraste barato que a fila de
06/08 já tinha desenhado no A-6, agora com o storm removido do caminho.

**PREVISÃO, derivada do medido.** O 8BitDo em PS4 **não** passa pelo
`hid-nintendo`, então nenhuma queda dele pode ser atribuída ao rate-limit de
subcomando. Previsão: com o storm calado, **o Pro melhora e o 8BitDo não muda**.
**Se o 8BitDo também melhorar, o storm degradava o rádio inteiro** — e isso é
achado maior que o defeito original.

**ELA.** Deixa os dois ligados e avisa **qual** parou de responder, e quando.
**ASSISTENTE.** Conta instâncias HID novas de cada um pelo kernel, e lê o journal
com **data completa**.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| só o 8BitDo cai | é do aparelho/modo dele | alvo próprio; o Pro sai da conversa |
| os dois caem no mesmo minuto | é o **rádio** | o modo deixa de ser suspeito; alvo vira contenção |
| nenhum cai | o storm era o gatilho dos dois | fecha o E-1 com um segundo caminho |
| o 8BitDo melhora junto com o Pro | o storm degradava o rádio inteiro | achado maior; muda a prioridade da leva |
| o DualSense cai junto | queda geral | descartar a rodada |

---

### E-5. O Pro esquece este host quando volta ao Switch? *(a H3, e é a mais cara)*

**Pergunta.** Depois de o Pro ser usado no Switch (ou em outro host), ele volta
sozinho para esta máquina, ou precisa de pareamento novo?

**Por que é a última.** É a hipótese com **mais mecanismo conhecido e menos
medição desta casa**, e é a única que exige ela **quebrar de propósito** uma
conexão que está funcionando há 17 horas. Custo: **20 minutos**, e só vale se
E-1, E-3 e E-4 não explicarem as quedas.

**AVISO A ELA, ANTES DE COMEÇAR.** Se confirmar, **o Pro vai precisar ser
pareado de novo nesta máquina**, e isso é o desfecho esperado, não um acidente.
Este aviso é parte do protocolo.

**P0 — trancar.**

1. **Tirar um snapshot dos bonds antes** — existe script e timer para isso
   (`hefesto-bt-bonds-snapshot.timer`, `active`); confirmar que a última rodada é
   recente **antes** de mexer.
2. Parar o `hefesto-bt-health-watchdog.timer`: ele mexe em trust e bond a cada
   2 min e reescreveria o cenário no meio. **Destrancar: religar e conferir que
   voltou a `active`.** Passo do protocolo.

**ANTES.** O objeto D-Bus do Pro completo (`Paired`, `Bonded`, `Trusted`,
`Connected`, `ReconnectMode`) e a instância HID atual.

**CONTRASTE.** O **DualSense**, que fica na mesa sem ser levado a lugar nenhum. Se
ele também perder o bond na mesma janela, o que aconteceu foi no host — e o
teste não diz nada sobre o Pro.

**PREVISÃO, derivada do mecanismo.** O firmware do Pro guarda **um** host por
vez; ao parear com outro, o link key desta máquina deixa de valer **do lado do
controle**, enquanto o BlueZ continua achando que tem bond. Previsão: o objeto
D-Bus segue `Bonded=true` **e** o controle **não** volta ao apertar o botão —
a assinatura é justamente essa assimetria. **Se ele voltar sozinho, a H3 morre**,
e a permanência deixa de ter qualquer relação com o outro console.

**ELA.** Usa o Pro no Switch por um minuto, volta para perto do PC, aperta o
botão e diz se voltou.
**ASSISTENTE.** Lê o objeto D-Bus **no instante** do aviso e o journal do
`bluetoothd` da janela.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| `Bonded=true` no host e o controle **não** volta | H3 **CONFIRMADA** | a permanência é limitação de firmware; a entrega vira **avisar**, e o doctor ganha a checagem da assimetria |
| ele volta sozinho | H3 **REFUTADA** | uma causa a menos; a lista de hipóteses fica em três |
| o bond some do host também | não é o firmware, é o BlueZ | alvo muda inteiro; e o snapshot de bonds vira a cura |
| ele volta só depois de re-parear | H3 confirmada, com o custo medido | mesma consequência da linha 1, com número |
| o DualSense perde bond junto | contraste falhou | foi no host; descartar a rodada |

---

## 9. Notas de instrumento — as armadilhas desta frente

Cada uma custou tempo hoje, ou está registrada como tendo custado antes:

1. **`bluetoothctl` está MUDO nesta máquina** — `show`, `list` e `devices`
   devolvem vazio com saída 0 enquanto o D-Bus responde tudo. GRAU: MEDIDO para o
   sintoma, SEM PROVA para a causa. **Nenhum passo pode depender dele**; usar
   `busctl --system call org.bluez / org.freedesktop.DBus.ObjectManager
   GetManagedObjects`. Foi assim que a tabela da seção 5.1 saiu.
2. **`journalctl` sempre com data completa.** `--since "15:20"` sem data devolve
   zero em todas as janelas, e zero em todas é sinal de instrumento quebrado.
   GRAU: MEDIDO (custou uma medição inteira, registrado em 06/08).
3. **Contar quedas pelo KERNEL, nunca pelo `probe_offline`.** Cada perda de link
   cria uma instância HID nova; o `probe_offline` do daemon só dispara quando o
   **último** handle some, e para os externos ele nem existe. Comparar um lado
   pelo daemon e o outro pelo kernel é o erro que inventa resultado.
4. **Ler evdev é seguro; `EVIOCGRAB` não.** As medições de IMU da seção 3.4 foram
   leituras puras de `/dev/input/eventN` **sem grab** — um grab teria roubado o
   controle do co-op e do jogo, e o log de 03/08 já mostra
   `evdev_grab_failed [Errno 16]` como sintoma disso.
5. **`/dev/hidraw2` do DualSense físico é `0600 root`** pelo broker (MEDIDO
   agora). Sem `sudo`, qualquer instrumento reporta "sem dispositivo" e parece
   defeito do produto. Já o `/dev/hidraw7` do Pro **tem ACL** para o usuário dela
   — os dois não se medem do mesmo jeito.
6. **`/var/lib/bluetooth` é `root`-only e não precisa ser lido.** O D-Bus publica
   o mesmo estado, sem senha e sem risco.
7. **Escrever LED de externo NÃO é escrita de sysfs barata.** No Pro, cada
   lâmpada é um subcomando HID pelo rádio; no 8BitDo em PS4, é um output report do
   `hid-playstation`. Um instrumento que trate os dois como "escrever um arquivo"
   mede coisas diferentes com o mesmo nome.
8. **O 8BitDo tem dois combos parecidos e um errado no acervo.** PS4/DirectInput
   é **`Start + A`**; `X+Start` é X-input; `Y+Start` é Switch. MEDIDO com ela em
   03/08.
9. **A suíte de testes suja o journal do sistema** e chega a fazer o IPC recusar
   chamada por timeout. Se ela estiver rodando, nenhuma contagem vale.

---

## 10. O placar

- **2** aparelhos externos mapeados contra o kernel, com grau por linha.
- **13** afirmações fechadas sem gastar minuto dela — **10** MEDIDO, **1**
  SUSPEITA COM MECANISMO, **2** SEM PROVA.
- **1** defeito vivo encontrado e medido ponta a ponta: o laço de repintura do
  LED do Pro, **348** recusas de rate-limit e **83** falhas `-110` em dois dias.
- **1** instrumento do protocolo de 07/08 corrigido antes de custar uma noite: o
  Pro **não** publica `capacity`.
- **1** premissa do acervo fechada com mecanismo: a IMU do Pro por Bluetooth é
  ligada **pelo driver**, e o Enable-IMU do produto duplica trabalho feito.
- **1** buraco de acervo registrado com data: a referência canônica **não fala**
  destes aparelhos, e duas docstrings apontam para estudos que não existem no
  disco.
- **5** medições nesta fila; **1** delas decide, custa **zero** atenção dela, e o
  lado B já começou às 15:27:48 de hoje.

**Adendo do placar, 07/08/2026 18h55 — o E-1 fechou:**

- **1** medição deste protocolo **FECHADA** no mesmo dia em que foi desenhada, e
  é a **primeira** dos externos a fechar. Custo real de atenção dela: **zero
  minuto**, exatamente o previsto.
- **348** recusas de rate-limit e **83** falhas `-110` do lado A; **0** e **0**
  do lado B, em 3h27m. MEDIDO.
- **15** episódios de storm no lado A, **15** com escrita nossa no mesmo minuto,
  **0** sem. É o pareamento que fecha a causa — não a contagem bruta.
- **1** grau promovido: a escrita do Hefesto **causa** o storm — de SUSPEITA COM
  MECANISMO para **MEDIDO**.
- **1** hipótese **refutada nesta janela**: o storm não derruba o Pro. Ele levou
  225 recusas de pé, por 17h06m sem soltar o link.
- **1** linha de LEITURA **descartada com número**: não há segundo escritor.
- **6** coisas que o E-1 **não** prova, listadas item por item — porque um A/B de
  um lado só não vira lei.
- **1** achado sobre **MÉTODO**, e é o maior desta página: a decisão de calar a
  luz foi tomada por **honestidade**, sem saber de defeito nenhum, e apagou um
  defeito técnico de dois dias. **Parar de afirmar o que não se entrega apaga
  trabalho que ninguém tinha medido** — e o corolário é medir o que a
  honestidade apagou, porque o A/B nasce montado e de graça.

E a correção que esta página existe para entregar: **a pergunta dela era sobre a
conexão dos externos, e a medição diz que o externo estável é o Pro.** Quem cai
é o DualSense — e o que o produto fazia com o Pro era piorar o rádio de graça,
por um número que ela mesma mandou apagar em 07/08.
