# Sprint 2026-07-16 — DualSense Edge desduplica (UHID-04), launch options, sudo-zero, simetria do install

Sessão ultracode. Objetivo da Vitória: fechar as "besteiras" que sobraram da onda UHID —
controle duplicado, rumble, conveniência (sem sudo, sem colar comando toda hora) — com
"solução completa e definitiva a nível de C". Branch `sprint/harmonia-uhid`.

## TL;DR do que entrou (gate 2410 verde, working tree)

1. **UHID-04 — fim do duplicado no layout PS (o item que faltava construir).** O vpad UHID
   passa a se apresentar como **DualSense Edge `054c:0df2`** em vez de `054c:0ce6`. Como o
   físico é `0ce6` e o vpad virou `0df2`, a launch option `SDL_GAMECONTROLLER_IGNORE_DEVICES=
   0x054c/0x0ce6` esconde **só o físico** e o vpad Edge sobrevive → layout PS, rumble, sem
   duplicar. **Validado ao vivo:** `playstation 0003:054C:0DF2...: Registered DualSense
   controller` (kernel binda o Edge com o blueprint do 0ce6). Arquivo: `uhid_gamepad.py`
   (`VPAD_PRODUCT`, `product` no dataclass, `_create2_event` usa `self.product`).
2. **Botão "Copiar opções p/ jogos" reescrito** (`daemon_actions.py` `compose_launch`): compõe
   por máscara/backend. Xbox → `SDL_JOYSTICK_HIDAPI=0 IGNORE %command%`; DualSense-Edge (uhid)
   → `PROTON_ENABLE_HIDRAW=1 IGNORE %command%`; fallback dualsense+uinput → aviso honesto.
   Ambas embutem o **pré-carregamento de shaders** NVIDIA (`__GL_SHADER_DISK_CACHE=1
   __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1` — "carregamento completo antes da tela"). Parou de
   empurrar pro Xbox.
3. **Backend exposto no `state_full`** (`gamepad_emulation.backend` = uhid/uinput) — o botão
   decide a variante; property `backend` em `VirtualPad`/`Uhid`/`Uinput`.
4. **Sudo em runtime da GUI ZERADO** (`daemon_actions.on_storm_fix_safe`): removido o
   `install_snd_quirk.sh --runtime` (era o único `sudo tee`; o rótulo "não pede senha" mentia).
   O quirk persistente (`/etc/modprobe.d`, default do install) pega no replug.
5. **Simetria do install (mic)** (`install.sh`): `WITH_WIREPLUMBER_FIX=1` agora é **DEFAULT** —
   o uninstall remove o drop-in 51 por padrão, então o install tem de recolocá-lo por padrão.
   Opt-out `--keep-dualsense-mic`. Antes, o ciclo uninstall→install deixava o DualSense virar o
   mic padrão.
6. **Tooltip da máscara DualSense** (glade) honesto: agora dedup + PS layout com o botão.
7. **Aviso de paridade BT** (log-only) em `capture_dualsense_blueprint` — ver §BT.

Testes novos: `test_uhid_edge_dedup.py`, `test_storm_launch_options.py`.

## Validação ao vivo (Sackboy, USB, co-op 2 players)

- ** Rumble in-game CONFIRMADO** (`rumble_ff.plays=3` — o jogo mandou FF ao vpad e o sink
  entregou ao físico).
- ** SEM duplicação de controles** (a Vitória confirmou na tela).
- ** Veio em interface XBOX**, não PS — porque o perfil dela `sackboy_nativo` forçava
  `gamepad_flavor: "xbox"`. **Corrigido**: troquei p/ `dualsense` no
  `~/.config/hefesto-dualsense4unix/profiles/sackboy_nativo.json`. (o vpad Edge subiu certinho
  antes da troca: `hidraw6/7 = 054c:0df2` ao lado dos físicos `hidraw4/5 = 054c:0ce6`.)
- ** Autoswitch derrubou a emulação no meio do jogo**: `profile_autoswitch to=sackboy_nativo
  wm_class=steam_app_1599660` (ok) → depois `to=vitoria wm_class=unknown` → o perfil padrão
  "vitoria" **desligou a emulação**. Causa: a detecção de janela perdeu a Sackboy (virou
  `unknown`) — é o WARN do XWayland/COSMIC (`zcosmic_toplevel_info_v1` ausente). Ver §Pendências.

## Ciclo uninstall→install (rodado na máquina, doctor verde)

- `uninstall.sh -y` + `install.sh -y` (sem flags = o default). Doctor no fim: tudo `[ OK ]`
  (serviço, socket, udev, /dev/uinput, /dev/uhid, hid_playstation, applet, mic-não-DualSense,
  sink preservado, Steam Input off, sem -71). Venv reinstalado já roda o código Edge
  (`VPAD_PRODUCT=0xdf2`).
- **Caveat sudo/TTY**: os passos root do install/uninstall exigem TTY real (sem TTY, o `sudo`
  interno não herda o ticket e os passos root são pulados com aviso, mas o script segue dizendo
  "instalado"). Para a Vitória num terminal real, funciona (1 senha). Rodei via ferramenta com
  um drop-in NOPASSWD temporário (`/etc/sudoers.d/99-hefesto-temp-install`) **removido logo
  depois** (confirmado `sudo -n true` falhar).
- **Mic**: o default caiu num `.monitor` porque **não há microfone real plugado na placa** —
  fallback esperado, NÃO bug. O mic-INPUT do DualSense está deprioritizado (doctor OK). O 51 só
  cobre `alsa_input.*DualSense`, não o monitor da saída `alsa_output.*DualSense` (se um dia
  reclamar de voz-chat pegando áudio do sistema, estender o 51 pro output — ela usa HDMI de
  saída, é seguro).

## Paridade BT (§BT — analisado, fix definitivo p/ amanhã)

- **O que JÁ funciona em BT** (memória + código): input do físico (evdev, transport-agnostic),
  rumble→físico (`set_rumble`/pydualsense), lightbar/player-LED (sysfs), e a **dedup**
  (`IGNORE 0x054c/0x0ce6` — o DualSense via BT ainda é `054c:0ce6`). O vpad Edge é sempre
  "USB-style" (virtual, `BUS_USB`), independe do transporte do físico.
- **O RISCO não-validado**: `capture_dualsense_blueprint` copia o **report descriptor** do
  físico. Via USB o descriptor usa report de input **`0x01`** (289 B, confirmado — ver
  `captures/dualsense_usb_descriptor_054c0ce6.bin`). Via BT o descriptor declara **`0x31`** como
  input principal. Como o vpad é `BUS_USB` e emite `0x01`, um descriptor de BT pode fazer o HID
  core dimensionar errado o report e o vpad nascer torto.
- **Feito nesta sessão**: aviso log-only `uhid_blueprint_bt_descriptor` (dispara só se o
  descriptor tiver `85 31` = BT; no USB nunca dispara) + captura do descriptor USB de referência.
- **Fix definitivo (amanhã, com teste em BT)**: o vpad usar um **descriptor USB canônico**
  (independente do transporte do físico) em vez de copiar o do físico — ou cachear o descriptor
  USB e reusá-lo quando o mesmo controle aparecer em BT. Zero risco ao caminho USB (só troca o
  descriptor quando o físico é BT). Não implementei blind porque não dá pra testar BT sem parear.

## Pendências para a validação humana (amanhã)

1. **Layout PS in-game**: abrir a Sackboy e confirmar prompts de PlayStation (□) + sem
   duplicar + vibração, agora que o perfil está em `dualsense`. Precisa da launch option
   DualSense colada (botão "Copiar opções p/ jogos" → gera
   `PROTON_ENABLE_HIDRAW=1 SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6 __GL_SHADER_DISK_CACHE=1 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%`).
2. **Autoswitch-flap (emulação cai quando a janela vira `unknown`)**: é o limite do XWayland no
   COSMIC. Mitigações a discutir: (a) o perfil padrão NÃO desligar a emulação; (b) histerese no
   autoswitch (ignorar `unknown` transitório e manter o último perfil de jogo); (c) fixar o
   perfil manualmente durante o jogo (`autoswitch_suppressed_by_manual_override`).
3. **Paridade BT**: parear um DualSense via BT e testar a máscara DualSense (ver o aviso
   `uhid_blueprint_bt_descriptor` no log). Se bugar, implementar o descriptor USB canônico.
4. **Os 2 warnings do doctor (não são desta onda)**:
   - `/dev/hidraw0-3 estão 0666`: são os dongles do teclado/mouse (CX/Compx `3554:fa09` /
     `25a7:fa07`), NÃO o DualSense (`hidraw4/5` estão 0660+uaccess). Ajuste manual antigo / de
     outra toolchain, não do hefesto.
   - `detecção de janela DEGRADADO (só XWayland)`: limitação do COSMIC (falta
     `zcosmic_toplevel_info_v1`), a mesma do item 2. Não é bug do hefesto.

## Regras/armadilhas honradas
MAC próprio por jogador (`02:fe:00:00:00:0N`), udev de uhid/uinput `<73` (uaccess→ACL via
73-seat-late), máscara `0x03` no valid_flag do rumble, `_INPUT_PAYLOAD_SIZE=63`, commit anônimo
