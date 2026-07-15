# Sprint SPRINT-UHID-VPAD-01 — o gamepad virtual vira um DualSense de verdade

Pedido da mantenedora (2026-07-15, madrugada): *"ao vivo só se o controle xbox 360
tiver selecionado que ele funciona. todas as opções deveriam funcionar, inclusive
jogar direto pelo da sony… tá permitido linguagem baixa a nível kernel pra
resolvermos tudo, e tudo deve funcionar via script install e afins."*

## O problema, na raiz

O gamepad virtual (vpad) é criado hoje via **/dev/uinput**. Um device uinput é só
um nó de evdev: **não tem hidraw**. Consequências, todas já sentidas:

- O SDL, ao ver um evdev com VID/PID da Sony (máscara DualSense), usa o driver PS5
  e procura o **hidraw** para vibrar. Não acha → **a vibração não funciona**. Por
  isso a máscara Xbox 360 virou obrigatória — ela cai no caminho XInput genérico,
  que vibra por evdev/FF.
- A matriz de paridade (`2026-07-13-sprint-paridade-de-features.md`) marcou como
  MORTO/IMPOSSÍVEL no vpad, sempre pelo mesmo motivo: **gatilhos adaptativos**,
  **lightbar**, **giroscópio**, **touchpad**, **bateria**.
- O vpad tem o **mesmo nome** do controle físico e nasce sem MAC → é impossível
  para o jogo (e para nós, e para o udev) distinguir um do outro. Daí o controle
  duplicado e a dependência de launch options da Steam.

Ou seja: **um único defeito de fundação** explica a queixa nº3 inteira e metade da
matriz de paridade.

## A cura (PROVADA ao vivo antes de abrir este sprint)

Criar o vpad por **/dev/uhid** em vez de /dev/uinput. O uhid registra um device
**HID** no kernel; o driver `hid_playstation` faz bind nele e constrói o DualSense
completo — de graça, com o código que já existe no kernel.

PoC executado nesta máquina (2 controles reais conectados), copiando do físico o
report descriptor (289 B) e os feature reports 0x05/0x09/0x20 via `HIDIOCGFEATURE`:

```
playstation 0003:054C:0CE6.000C: hidraw6: USB HID v1.00 Gamepad [Hefesto Virtual DualSense P1]
input: Hefesto Virtual DualSense P1                 -> input86   (gamepad)
input: Hefesto Virtual DualSense P1 Motion Sensors  -> input87   (giroscópio!)
input: Hefesto Virtual DualSense P1 Touchpad        -> input88   (touchpad!)
input: Hefesto Virtual DualSense P1 Headset Jack    -> input89
playstation 0003:054C:0CE6.000C: Registered DualSense controller hw=0x710 fw=0x110002a
leds/: input86:rgb:indicator + input86:white:player-1..5            (lightbar + LED de jogador!)
UHID_OUTPUT recebido: 02 00 14 00 ...                (o rumble do jogo chegando até nós)
```

O que isso muda, célula por célula da matriz de paridade:

| Capacidade no vpad | uinput (hoje) | uhid (este sprint) |
|---|---|---|
| Vibração com máscara DualSense | **MORTA** | **funciona** (hidraw real → SDL/HIDAPI) |
| Gatilhos adaptativos | "IMPOSSÍVEL" | chegam como UHID_OUTPUT → repassar ao físico |
| Lightbar | MORTA | `leds/rgb:indicator` por jogador, do kernel |
| Player LED | nosso, manual | `leds/white:player-1..5` por jogador, do kernel |
| Giroscópio | MORTO | Motion Sensors criado pelo kernel |
| Touchpad | MORTO | Touchpad criado pelo kernel |
| Identidade (nome/MAC) | igual ao físico | **"Hefesto Virtual DualSense P1"** + MAC próprio |

### Detalhes críticos aprendidos no PoC (não repetir os erros)

1. **MAC duplicado = probe falha.** Copiar o feature 0x09 do físico dá
   `Duplicate device found for MAC address … / Failed to create dualsense / probe
   failed -17`. O vpad precisa de MAC próprio, na faixa localmente administrada,
   um por jogador — bytes 1..6 do report 0x09 em **little-endian**
   (`01000000fe02` = `02:fe:00:00:00:01`).
2. **Responder UHID_GET_REPORT é obrigatório** durante o probe (0x09 MAC,
   0x20 firmware, 0x05 calibração). Capturar do físico uma vez e cachear.
3. **UHID_SET_REPORT também precisa de reply**, senão o probe trava.
4. `/dev/uhid` é `crw------- root root` → precisa de regra udev, como /dev/uinput.
   **A regra tem de ser numerada < 73**: quem transforma a tag `uaccess` em ACL é a
   `/usr/lib/udev/rules.d/73-seat-late.rules`; numerada depois, o `MODE` aplica e a
   ACL não. E nós em `SUBSYSTEM=="misc"` precisam de
   `udevadm trigger --subsystem-match=misc`, senão a regra só vale no próximo boot.
5. O device nasce em `/sys/devices/virtual/misc/uhid/` → udev consegue
   distinguir vpad de físico com precisão.
6. **O report 0x02 é multiplexado** (rumble + lightbar + gatilhos + mic). Os motores
   só valem quando o `valid_flag0` traz os bits de vibração — sem checar, **todo
   report de LED (que chega com os motores zerados) mata a vibração em curso**, e
   como o `update_rumble` do driver é one-shot o controle fica mudo até o jogo mudar
   o efeito.
   E a checagem é **máscara `0x03`, nunca só `0x01`**: com firmware >= 0x0215 o driver
   liga `use_vibration_v2`, manda `COMPATIBLE_VIBRATION2` no **valid_flag2** e deixa o
   `valid_flag0` com **HAPTICS_SELECT (0x02) sozinho**. Os dois controles da máquina de
   teste são **0x0630** — testar só o `0x01` descartaria **todo** o rumble no hardware
   alvo, com a suíte verde. (Firmware: feature 0x20, `update_version` no offset 44 LE.)
7. **Ao testar FF por ctypes**: `struct ff_effect` tem **48 bytes com o union em offset
   16** (não 14 — alinha em 8 pelo ponteiro `custom_data` do `ff_periodic_effect`). Com
   o layout errado o teste reporta `(0, 64)` e parece bug do módulo. Layout correto,
   `strong=0x8000/weak=0x4000` → sink recebe `(64, 128)` = `(weak/256, strong/256)`.

## Itens

### UHID-01 — Backend uhid do vpad
- **Arquivos**: `src/hefesto_dualsense4unix/core/` (novo `uhid_device.py`),
  `daemon/subsystems/coop.py`, `daemon/subsystems/gamepad.py`.
- Criar `UhidDualSense`: CREATE2 com descriptor+features capturados do físico,
  MAC próprio por jogador, loop de eventos (START/OPEN/OUTPUT/GET_REPORT/
  SET_REPORT/CLOSE/STOP), INPUT2 para encaminhar o estado do físico, DESTROY
  limpo. Sem dependência nova (só `struct`/`os`/`fcntl`).
- **Aceite**: com 1 controle físico, `dmesg` mostra `Registered DualSense
  controller` para o vpad; `/dev/input/js*` do vpad responde a `jstest`; nenhum
  device órfão após desligar o modo.

### UHID-01b — O que falta para o co-op poder trocar de backend
Levantado pelo review adversarial do `UHID-01` (o módulo existe e está provado, mas ainda
**não tem call site** — nada em `src/` o importa, então nada disso quebra hoje):
- **`for_flavor()` ausente**: `coop.py:377` e `gamepad.py:254` constroem o vpad por
  `UinputGamepad.for_flavor(key, rumble_sink=…)` — trocar o backend sem isso é
  `AttributeError` na promoção do jogador, **fora** do try do `forward_all`.
- **`forward_analog`/`forward_buttons` ausentes**: no uhid o input vai em **report HID**
  (`send_report`), não em eventos evdev — falta o **encoder** do input report do DualSense
  (é o `UHID-02`). Sem ele: controle morto em silêncio + flood de warning por tick.
- **Sem `Protocol` comum**: `coop.py:99` anota `vpad: UinputGamepad | None`; o mypy quebra
  na troca. Extrair um `VirtualPad` (Protocol) com a interface que os dois cumprem.
- **`player` nunca é passado**: `coop` não repassa o índice do jogador → todos os vpads
  nasceriam `player=1` **com o mesmo MAC**, e o probe do 2º em diante falharia com
  `-EEXIST`. O `player` tem de vir do slot do co-op (ver `4P-02`).
- **`start()` devolve True sem confirmar o bind**: o `UHID_START` chega depois, no
  `pump_ff`. Para o fallback do `UHID-06` ser honesto, o chamador precisa de um
  `wait_for_bind(timeout)` — senão "deu certo" e o jogo fica sem controle.

### UHID-02 — Ligar o backend ao co-op (é o item que a Vitória sente no jogo)
- **Arquivos**: `integrations/uhid_gamepad.py`, `daemon/subsystems/coop.py`,
  `daemon/subsystems/gamepad.py`, `daemon/subsystems/rumble.py`,
  `core/backend_pydualsense.py`.
- **O encoder do input report** é o que falta para o vpad uhid receber o que o
  controle físico faz: no uinput o input vai em eventos evdev
  (`forward_analog`/`forward_buttons`); aqui vai em **report HID** (`send_report`).
  Montar o input report 0x01 (USB) do DualSense a partir do snapshot do físico —
  sticks, gatilhos, botões, d-pad — e alimentá-lo a cada tick do poll loop.
   Já provado: `send_report` sem padding é aceito pelo kernel e o
  `hid_playstation` decodifica (criou o input node do vpad).
- Fechar os gaps do `UHID-01b` (`for_flavor`, `Protocol` comum, `player` por slot,
  `wait_for_bind`).
- O **rumble já está pronto e provado** (`UHID_OUTPUT` → `rumble_sink` →
  `(64, 128)` no hardware): aqui é só plugar no sink real do daemon, respeitando o
  throttle de 20 ms e a política de rumble. Gatilhos/lightbar do jogo chegam pelo
  mesmo report 0x02 (ver `UHID-03` para os LEDs, que agora vêm do kernel).
- **Aceite**: jogo SDL vibra o controle físico **com a máscara DualSense**
  selecionada (o que hoje é impossível). Validar ao vivo, 1 USB + 1 BT.

### UHID-03 — Lightbar e player-LED por jogador via sysfs do kernel
- **Arquivos**: `daemon/subsystems/coop.py`, `app/actions/lightbar_actions.py`.
- Usar `leds/rgb:indicator` e `white:player-N` do próprio vpad em vez de disputar
  o hidraw do físico.
- **Aceite**: 2 controles → cores/LEDs independentes por jogador, sem storm.

### UHID-04 — Fim do controle duplicado sem launch options (udev)
- **Arquivos**: `assets/udev/`, `install.sh`, `uninstall.sh`.
- Regra para `/dev/uhid` (acesso do daemon, igual /dev/uinput — **cuidado**: o
  gatilho precisa do subsystem `misc`, senão só vale após reboot).
- Esconder do jogo o que não é jogável: os `js*` dos **Motion Sensors** (têm
  `ID_INPUT_ACCELEROMETER=1`) e, no modo vpad, os `js*`/hidraw do **físico** —
  agora possível **porque o vpad tem nome e MAC próprios**.
- Evidência do problema (medida ao vivo, 2 controles = **6 joysticks**):
  `js0`=físico USB, `js1`=Motion Sensors USB, `js2`=físico BT, `js3`=Motion
  Sensors BT, `js4`/`js5`=vpads. O grab de evdev **não** esconde o nó `js`
  (joydev é outro handler).
- **Aceite**: com 2 controles em modo vpad, o jogo enxerga exatamente 2
  gamepads (P1, P2) **sem** nenhuma launch option; `ls /dev/input/js*` reflete isso.

### UHID-05 — Máscara deixa de ser um trade-off (UI)
- **Arquivos**: `app/actions/home_actions.py`, `packaging/cosmic-applet/src/app.rs`,
  `cli/cmd_gamepad.py`.
- "DualSense (botões PS, **sem vibrar**)" → "DualSense (botões PlayStation)".
  Xbox 360 permanece para jogos que só falam XInput. Unificar o default entre
  GUI/applet/CLI (hoje a CLI ainda manda `dualsense` por omissão).
- Apagar da aba Início a frase de recomendação de 3 linhas com jargão — ela só
  existia para contornar este defeito.
- **Aceite**: trocar a máscara pela GUI, pelo applet e pela CLI leva ao mesmo
  estado; nenhuma opção visível fica sem vibração.

### UHID-06 — Fallback honesto
- Se `/dev/uhid` não existir ou o `hid_playstation` não fizer bind (kernel antigo),
  cair para o uinput atual **avisando na UI em linguagem simples**, sem mentir que
  a vibração vai funcionar.
- **Aceite**: teste com `/dev/uhid` inacessível → app usa uinput e mostra o aviso.

### UHID-07 — Validação ao vivo (obrigatória)
- 1 controle USB + 1 BT (estado atual da máquina de teste), depois 4 se houver
  hardware: vibração in-game nas duas máscaras, lightbar por jogador, gatilhos
  adaptativos no vpad, ausência de duplicação, `dmesg` limpo, sem storm -71.
- Bench de latência uhid vs uinput com 4 vpads (o GIL já é gargalo conhecido).

## Ordem

UHID-01 → UHID-02 → UHID-04 (o que a mantenedora sente no jogo) → UHID-03 →
UHID-05 → UHID-06 → UHID-07.

## Referências

- PoC e log completo: `poc_uhid.py` (scratchpad da sessão de 2026-07-15).
- Matriz que este sprint fecha: `2026-07-13-sprint-paridade-de-features.md`.
- Kernel: `drivers/hid/hid-playstation.c` (`dualsense_get_mac_address`,
  `dualsense_get_calibration_data`, `dualsense_get_firmware_info`), `linux/uhid.h`.
