# Validação ao vivo — multi-controle USB + Bluetooth (2026-06-27)

Sessão de validação ao vivo da feature multi-controle (FEAT-DSX-MULTI-CONTROLLER-01,
v3.9.0) com hardware real: **1 DualSense por USB + 1 por Bluetooth simultâneos**.

## O que funciona (confirmado no hardware)
- **Detecção dos dois juntos**: `controller.list` mostra os 2 (BT primário, USB secundário).
- **Leitura de input**: do controle primário (evdev).
- **Gatilhos adaptativos** (o coração do app): funcionam em **USB e Bluetooth**.
- **Player-LEDs**: funcionam em USB e Bluetooth.
- **Lightbar + rumble + gatilhos no USB**: 100%.

## Problemas encontrados (ambos no Bluetooth)

### 1. [EM ANDAMENTO] Corrupção do link BT com USB+BT juntos — `input CRC check failed`
Com os **dois** controles abertos, o kernel `hid_playstation` loga
`DualSense input CRC's check failed` no controle BT, e o **output do BT degrada**
(a lightbar deixa de responder ao broadcast). Com o **BT sozinho: zero CRC**, tudo
ok. Hipótese: a report_thread crua da pydualsense (read+write em hidraw) de cada
handle, somada ao driver do kernel, desincroniza/sobrecarrega o link BT (que é
mais frágil e checado por CRC). O adaptador BT (`hci0`) está em `usb3/3-1`, no
mesmo controlador USB — contenção de I/O (família do storm). **Foco de correção.**

### 2. [TODO — ESTÉTICO] Lightbar por Bluetooth não acende a cor
A lightbar RGB do controle BT **não acende** a cor, embora **gatilhos e player-LEDs
funcionem** por BT (o output report é aceito — CRC ok). Resistiu a 3 caminhos
nesta sessão:
- pydualsense crua (`setColorI`) — sem efeito na cor (gatilhos/player ok);
- pydualsense + "release" (`pulseOptions=FadeOut`/LIGHT_OUT, emulando
  `dualsense_reset_leds` do kernel) — sem efeito;
- sysfs do kernel (`/sys/class/leds/inputN:rgb:indicator/multi_intensity`+`brightness`)
  com daemon parado — sem efeito.

Como gatilhos/player funcionam, NÃO é byte de cor nem CRC nem off-by-one do
enquadramento BT (player_leds e RGB são bytes adjacentes do mesmo report aceito).
Provável: a lightbar por BT nasce sob controle de animação do firmware e o
"release" exato (sequência do kernel) não foi reproduzido — ou há contenção de
escritor (kernel output_worker vs pydualsense) específica da cor por BT.

**É cosmético** (gatilhos — a feature principal — funcionam por BT). Fica como TODO.

**Próximos passos do TODO estético:**
- Ler `drivers/hid/hid-playstation.c` (`dualsense_reset_leds` / `dualsense_output_worker`)
  para a sequência EXATA de `valid_flag2` (LIGHTBAR_SETUP_CONTROL_ENABLE) +
  `lightbar_setup` (LIGHT_ON 0x01 vs LIGHT_OUT 0x02) que solta a lightbar por BT.
- Testar `LIGHT_ON` (0x01) — a pydualsense não tem no enum `PulseOptions`, exige
  escrever o byte cru de setup antes da cor.
- Garantir UM único escritor de output por BT (kernel sysfs OU pydualsense, nunca
  os dois) e re-testar a cor.
- Se não soltar: degradar com graça — avisar na GUI que a cor da lightbar é
  confiável por USB; por BT pode não obedecer (gerenciada por firmware/kernel).
