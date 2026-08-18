# Mapa: o domínio — DualSense, HID, Bluetooth e os problemas de Linux

- **Levantado em:** 26-27/07/2026
- **Escopo:** o que o software controla no hardware, e quais problemas reais de
  Linux ele resolve
- **Natureza:** este é o conhecimento mais difícil de reconstruir do repositório.
  Boa parte não existe documentada em outro lugar

## Dispositivos: duas classes com fronteira rígida

**Adotados** (o daemon abre o hidraw, escreve output report, gerencia): **só
DualSense e DualSense Edge**. Filtro por VID **e** PID em
`core/evdev_reader.py:28-29`.

**Externos** (somente leitura: entram no inventário, ganham número e LED de
jogador; o input segue pelo kernel ou pela Steam): Nintendo Pro, 8BitDo, Xbox,
HORI, PowerA, Valve.

| VID:PID | Aparelho | Driver |
|---|---|---|
| `054c:0ce6` | DualSense | `hid-playstation` |
| `054c:0df2` | DualSense Edge — **e o vpad forjado do projeto** | `hid-playstation` |
| `054c:05c4` | DualShock 4 — **e o 8BitDo em modo DirectInput/PS4** | `hid-playstation` |
| `057e:2009` | Nintendo Switch Pro **e** 8BitDo em modo Switch | `hid-nintendo` |
| `045e:028e` | Xbox 360 — e a máscara Xbox do vpad uinput | `xpad` |
| `2dc8` / `0f0d` / `20d6` / `28de` | 8BitDo / HORI / PowerA / Valve | vários |

**Dois discriminadores fora de VID/PID**, porque o firmware clone mente o VID:

- **`bcdDevice`** separa Pro genuíno (`0210`) do clone 8BitDo (`0200`) no cabo —
  eles colidem em VID, PID **e número de série**. `assets/84-*.rules` cria
  `/dev/hefesto/nintendo-pro` e `/dev/hefesto/8bitdo-pro-clone`.
- **OUI do MAC**, único sinal por rádio: `e0f6b5` = Nintendo genuíno,
  `e417d8` = 8BitDo.

## Formato dos relatórios HID

| Direção | Transporte | ID | Tamanho | CRC |
|---|---|---|---|---|
| Input | USB | `0x01` | 64 B | não |
| Input | BT | `0x31` | **78 B** | CRC-32 LE, semente **0xA1** |
| Output | USB | `0x02` | 64 B | não |
| Output | BT | `0x31` | **78 B** | CRC-32 LE, semente **0xA2** |
| Feature (GET) | BT | — | — | semente **0xA3** |
| Áudio (saída) | BT | `0x32` | **142 B** | semente 0xA2 |

O payload "common" tem **47 bytes e é idêntico nos dois transportes**; o que muda
é o envelope:

```
USB (64 B):  [0]=0x02, [1..47]=common
BT  (78 B):  [0]=0x31
             [1]=seq<<4          nibble alto, 0..15
             [2]=0x10            tag magico OBRIGATORIO
             [3..49]=common
             [74..77]=CRC-32 LE sobre (0xA2 || bytes[0..73])
```

### O achado que explica anos de sintoma

`core/ds_output_report.py:5-7` registra: **o 0x31 que a `pydualsense` 0.7.5 monta
é malformado.** Off-by-one — `[1]=0x02` fixo onde deveria ir o nibble de
sequência, `0xFF` onde o firmware espera o tag `0x10`, campos deslocados um byte.
O firmware descarta em silêncio.

Era isso o *"a cor nunca funcionou por Bluetooth"* e o rumble mudo por rádio. O
projeto reescreveu o envelope inteiro **contra o kernel**, não contra a
biblioteca.

### Offsets dentro do `common` (47 B)

| Offset | Campo | Bit de validação |
|---|---|---|
| `[0]`, `[1]` | valid_flag0, valid_flag1 | — |
| `[2]`, `[3]` | motor direito (weak), esquerdo (strong) | flag0 `0x01`\|`0x02` |
| `[4..7]` | volumes de fone, alto-falante, mic, roteamento | flag0 `0x10`..`0x80` |
| `[8]` | LED do microfone | flag1 `0x01` |
| `[9]` | power_save — bit `0x10` é o mute do mic | flag1 `0x02` |
| `[10..20]` | efeito do gatilho **direito** (modo + 10 params) | flag0 `0x04` |
| `[21..31]` | efeito do gatilho **esquerdo** | flag0 `0x08` |
| `[41]`, `[42]` | setup e brilho da lightbar | flag2 `0x02`, `0x01` |
| `[43]` | LEDs de jogador (`& 0x1F`) | flag1 `0x10` |
| `[44..46]` | lightbar R, G, B | flag1 `0x04` |

**Ressalva de proveniência registrada no código** (`ds_output_report.py:67-73`):
o kernel declara `[4..7]` como `reserved[4]` e **nunca os escreve**. A
nomenclatura por bit vem de documentação de comunidade e está marcada como
**provável, não medida**.

**Armadilha do bit flag2 `0x02`** (`ds_output_report.py:115-119`): é o que o
kernel usa **uma vez por conexão** para tomar a barra de luz. Mantê-lo engatado
em regime **trava a exibição no firmware** — o registrador aceita a cor, o sysfs
mostra, e a barra fica apagada.

**Máquina de estados da lightbar em BT** (`backend_pydualsense.py:363-381`):
existe uma janela de ~3,4 s pós-conexão em que um 0x31 malformado faz a lightbar
**latchear apagada até o power-off do controle** — sobrevive a re-parear e a
rebind de driver. O cabo escapa. É por isso que a supressão de LEDs nasce ligada.

## Recursos de hardware, um a um

### Lightbar
Duas rotas: **sysfs** (`multi_intensity` + `brightness`) que delega ao kernel a
montagem do report — funciona igual em USB e BT — e hidraw. Quando o sysfs é
gravável, o backend **suprime** os bits de LED do report: a disputa de escritores
era o que fazia a cor não colar.

Paleta automática por slot (`core/led_control.py:146-155`): 1=azul, 2=vermelho,
3=verde, 4=rosa, 5..8=amarelo/ciano/laranja/roxo.

### LEDs de jogador
- **DualSense**: 5 LEDs brancos, padrões canônicos do PS5, estendidos até 8 por
  decisão da casa (R-25).
- **Nintendo/8BitDo modo Switch**: 4 verdes + o 5º **azul** usado como bit "+5",
  chegando a 9 slots distinguíveis.
- **8BitDo por BT em modo DS4**: não tem barra de jogador; o número vira **cor da
  lightbar**.

### Gatilhos adaptativos
Dois níveis. **HID**: 10 modos + 7 bytes de força (`Off`, `Rigid`, `Pulse`,
`Rigid_A/B/AB`, `Pulse_A/B/AB`, `Calibration`). **Presets**: 19 fábricas em
`core/trigger_effects.py` que produzem `(modo, forças)`. O multiplicador **x32**
normaliza a nomenclatura 0-8 do DSX para o byte 0-255.

Saturação medida: `frequency` aceita 0-255, mas o firmware **satura em ~150-160
Hz** nos modos `Pulse*`.

Existe um caminho **raw de 11 bytes** que embute verbatim o bloco que o **jogo**
escreveu, porque `TriggerEffect` só carrega 7 forças e zeraria os parâmetros 8, 9
e 10 do efeito do jogo.

### Rumble
`common[2]` weak, `common[3]` strong. O bit flag2 `0x04`
(`COMPATIBLE_VIBRATION2`) depende de firmware `>= 0x0215` — testar só o bit
`0x01` descartava **todo** o rumble no hardware alvo.

**Keepalive neutro (GUERRA-01):** os bits de vibração só ligam com rumble nosso
ativo, ou num único report de transição. Sem isso o keepalive de 0,5 s zerava o
rumble de terceiros escrevendo direto no hidraw.

**Rede contra rumble preso:** se o jogo liga a vibração e depois só manda reports
sem os bits dela, o `stop` nunca chega. Teto de silêncio de 3 s, valor **medido**
(17 disparos em 90 min de jogo real; a primeira versão usou 6 s por prudência e a
medição a desmentiu).

### Giroscópio e acelerômetro
**Não há matemática: é cópia byte a byte** de 25 bytes (offsets 15..39) do report
físico para o vpad. Taxas medidas: **250 Hz em USB**, **~765 Hz em BT**. O nó de
movimento do vpad emitia **zero** antes desse espelho.

Teto de silêncio **por transporte**: 1 s em USB, **30 s em BT** — o firmware BT
emudece com o controle em repouso, e com 1 s valendo para os dois o leitor entrava
em ciclo de reabertura a ~1 Hz, ~1600 linhas de journal em 45 min.

Calibração: feature `0x05` (41 bytes), cache **por MAC** porque é imutável por
unidade.

**IMU do Nintendo Pro:** o `hid-nintendo` declara e deixa em standby. O projeto
manda o subcomando **0x40 arg 0x01** cru no hidraw, dentro do envelope de 12
bytes com rumble neutro. Só por USB.

### Touchpad
Pontos de toque nos offsets **32 e 36** (não 31/35 — o `reserved2` empurra), e o
byte de contato é **invertido**: `ativo = !(contact & 0x80)`. Payload zerado
produz dois dedos fantasma presos em (0,0).

A regionalização esquerda/meio/direita é **invenção do projeto** para o modo
mouse — o DualSense real só reporta "clicou".

### Bateria
No vpad, `payload[52]`: `nibble*10+5`, 11 níveis. Zerado, o vpad anuncia "5%
descarregando para sempre"; sem dado o projeto usa `0x1F` — "cheio e carregando",
a mentira que não dispara alerta.

### Firmware
**Não há atualização — zero linhas.** O que existe é leitura do feature `0x20`
(64 B), cujo `update_version` `0x0630` liga `use_vibration_v2` no driver. As duas
pesquisas em `docs/research/` são exploratórias e trazem aviso no topo.

## O microfone: dois mundos

### Por USB — problema de política, não de transporte
Dispositivo de áudio USB comum. **Três mutes empilhados**, cada cura revelando o
de baixo:

1. **Rota do WirePlumber** — `mute:true` persistido em `default-routes`,
   restaurado a cada conexão **sem nada no log**.
2. **Perfil da placa** — preso em `input:iec958-stereo`, que é S/PDIF e não
   carrega sinal, porque o WirePlumber marca a analógica indisponível sem fone
   plugado. Mas o mic embutido usa esse caminho.
3. **Firmware do controle** — o mesmo estado que o botão físico alterna.

`mic.set` tem **três** estados, e confundir dois deles foi o defeito real:
`true` muta; `false` **desmuta como ordem** e o botão físico para de mandar;
`null` **devolve a posse** ao driver.

### Por Bluetooth — Opus tunelado em HID
**O DualSense não implementa A2DP/HFP/HSP** — confirmado pelo mantenedor do
BlueZ. O áudio trafega **dentro do HID**, como quadros **Opus**, e o
`hid-playstation` não os trata, então o hidraw os entrega intactos. A ponte é
inteiramente em espaço de usuário.

Ligar: output `0x32`, corpo em cadeia TLV, tag `0x11` (AudioControl).
Ouvir: input `0x31`, byte `[1]` com **bit0 = pacote de input, bit1 = pacote de
ÁUDIO**, mutuamente exclusivos — não cabem juntos em 78 bytes.

**O preço, medido em A/B de 3 s:**

```
mic DESLIGADO : input 260,4 Hz   audio   0,0 Hz
mic LIGADO    : input 170,5 Hz   audio 106,2 Hz
```

O total é o mesmo: **o áudio não abre canal novo, ocupa lugar na mesma fila.**
Custa ~35% dos reports de input. Por isso a ponte é sempre opt-in.

**BT-MIC-GATING-01 continua ABERTO:** o firmware declara mudo em 55-75% do tempo,
sobrando ~40% do sinal. **Três hipóteses refutadas por medição.** O principal
suspeito não testado está registrado no código: o próprio daemon é um segundo
escritor de `0x31` nesse device.

## Os problemas de Linux que o projeto resolve

### Storm `-71` / enumeração de áudio USB
A teoria antiga (BIOS, C-state, "troque de porta") foi **refutada**. A causa é a
enumeração das interfaces de áudio pelo `snd-usb-audio`: uma rajada de
control-transfers no EP0 tomba o link. Provado A/B: **áudio desligado = zero
storm em qualquer porta**, e é port-independente.

Três alavancas, as duas primeiras mutuamente exclusivas:

| Camada | Efeito |
|---|---|
| `usbcore.quirks=054c:0ce6:gn` (cmdline) | espaça a rajada, **preserva** mic e fone |
| `quirk_flags=...ignore_ctl_error\|ctl_msg_delay_1m` (modprobe) | tolera erro do mixer; **ortogonal**, soma |
| regra udev 75, `authorized=0` (opt-in) | mata o áudio inteiro |

### Bonds de Bluetooth que evaporam — duas causas distintas
Procurar só uma leva ao lugar errado metade das vezes:

| | com crash | sem crash |
|---|---|---|
| Assinatura | `malloc_consolidate(): unaligned fastbin chunk`, `status=6/ABRT` | `search_cb() ... Host is down (112)`, `NRestarts=0` |
| Gatilho medido | reconexão de dois controles Nintendo-class em segundos | **controle pareado por BT e em uso pelo cabo ao mesmo tempo** |

Mitigação: snapshot de bonds na **borda de cada conexão** (`assets/83-*.rules`) —
com timer de 15 min, um pareamento feito logo após um snapshot sumia sem cópia.
O restore é **manual por decisão**: reimpor chave antiga em controle que já
rotacionou gera laço de autenticação, a mesma classe de gatilho do crash.

### 163.925 falhas de CRC num único boot
99,97% de todas as ocorrências registradas. Assinatura: **RSSI -30 dBm com Link
quality 0** = interferência, não distância. Adaptador BT e WiFi do mesmo
fabricante, ambos em 2,4 GHz, no mesmo controlador. Nenhuma correção de software
compensa quadro corrompido na camada de enlace.

Mitigação do lado do daemon: o laço de `sendReport` do upstream roda **sem pausa**
a 250 Hz-1 kHz; com 2+ controles satura o controlador USB, onde o adaptador BT
também vive. O projeto throttla (8 ms base, escalado até 32 ms com 4 controles) e
faz dedup do write.

### Duplicação de dispositivo
- vpad forjado como Edge `0df2` para que o IGNORE esconda só o físico;
- `assets/78-*.rules` zera `ID_INPUT_JOYSTICK` nos Motion Sensors — com 2
  controles a lista do jogo mostrava **6 "joysticks"**;
- `assets/80-*.rules` esconde os `js*` de movimento da API legada;
- `assets/76-*.rules` impede o touchpad de mover o cursor **em dobro**;
- broker escondendo o hidraw físico.

### Steam Input e Proton
Os sintomas do Steam Input aparecem **mesmo sem o Hefesto instalado** — as
toggles vivem no `localconfig.vdf` por usuário. Fato registrado sem alarme: a
Steam mantém descritor aberto no hidraw de **todo** controle suportado; **fd
aberto é estado normal, não assinatura de conflito.**

No Proton: `PROTON_DISABLE_HIDRAW` (o `ENABLE` morreu no Proton 10), Proton
pinado por SHA-256, e o **fail-safe de ouro**: qualquer vpad degradado significa
**nenhum** `IGNORE_DEVICES`.

## Multi-controle

Modelo base: **N controles, 1 jogador** — output em broadcast, input só do
primário. O co-op acrescenta uma camada, sem tocar no caminho do P1: por controle
extra, um leitor evdev **com grab** e um vpad próprio.

Garantia: o vpad de um secundário **só nasce depois do `EVIOCGRAB` confirmado** —
antes, um grab pendente com recusa tardia deixava ~2 s de input **dobrado**.

Evolução da numeração, em quatro correções: R-15 (fim da expiração por sessão
vazia), R-23 (o número sobrevive ao boot — MAC é identidade, não sessão), R-24
(atribuição deixa de ser preguiçosa) e **NUM-01** (persiste-se o **lugar na
fila**, não o número absoluto; a posição é 1..N entre os presentes). Critério que
resume: **nunca existe um jogador 2 sem um jogador 1.**

## Duas armadilhas de medição que já enganaram

Registradas para não repetir:

1. **Ordenar `/sys/bus/hid/devices/` por nome mente** — o nome começa pelo
   barramento (`0003:` antes de `0005:`), não pela ordem de chegada. A ordem real
   é o contador hexadecimal no fim.
2. **`/sys/class/leds` do vpad não diz o número que o jogo escreveu.** O jogo
   escreve como output report HID, interceptado em espaço de usuário — nunca
   chega à classe LED do kernel. E a tabela de padrões do kernel é **idêntica** à
   nossa em 1..4, logo o padrão aceso é ambíguo por construção. **A única
   testemunha do autor é o log.**
