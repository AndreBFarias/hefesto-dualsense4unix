# Sprint 2026-06-28 — Lightbar por BT + auditoria + produção (v3.10.0)

Sessão de fechamento para produção: resolver a cor da lightbar por Bluetooth,
auditar o projeto inteiro com verificação adversarial, aplicar os achados e
cortar o release **v3.10.0**. Princípio condutor da Vitória: **tudo deve funcionar
via interface (GUI/daemon), não por script standalone.**

## 1. Lightbar (cor) por Bluetooth — RESOLVIDO (FEAT-DSX-LIGHTBAR-SYSFS-01)

### Sintoma

Por Bluetooth, gatilhos adaptativos, rumble e player-LEDs obedeciam, mas a **cor**
da lightbar não mudava. Por USB a cor sempre funcionou. Resistiu a 3 tentativas
anteriores (pydualsense crua; "release" emulando `dualsense_reset_leds`; sysfs com
daemon parado) — registradas como "TODO cosmético".

### Causa raiz (linguagem baixa)

Contenção de **dois escritores** sobre o mesmo recurso HID:

- O kernel `hid_playstation` registra a lightbar como um `led_class_multicolor`
  (`/sys/class/leds/<inputN>:rgb:indicator`) e os player-LEDs como LED class
  brancos. Ele é **dono** desses LEDs e reafirma o estado deles montando o output
  report do DualSense (no BT: report `0x31`, com seq-tag e CRC-32 que o próprio
  kernel calcula).
- A pydualsense escreve o MESMO output report cru por `hidraw`, com seq-tag BT
  fixo. Os dois ficam num cabo-de-guerra. Gatilho/rumble passam porque o kernel
  **não** os disputa; lightbar/player-LED perdem porque o kernel reescreve por
  cima — e só na cor o conflito é perceptível.

### Conserto (duas peças que entram juntas)

1. **Rota sysfs do kernel** — `core/sysfs_leds.py` (novo): escreve a cor em
   `…:rgb:indicator/multi_intensity` (+ `brightness`) e os 5
   `…:white:player-N/brightness`. O **kernel** monta o report correto (CRC + seq),
   então funciona IGUAL em USB e BT. Descobre os nós por glob e mapeia
   **controle → nó por MAC** (`HID_UNIQ` do device HID, que bate com o `serial`
   do hidapi, normalizado em hex minúsculo).
2. **Cede a lightbar ao kernel** — `_PinnedPyDualSense.prepareReport` limpa os
   bits de *flag* de lightbar (`0x04`) e player (`0x10`) no byte de flags de LED
   do report quando `_suppress_leds` está ligado. Sem esses bits, o firmware
   ignora os bytes de cor/player daquele report → o `report_thread` da pydualsense
   para de reescrever a lightbar e não disputa mais.

**Gate anti-regressão:** só usa a rota sysfs se o nó for **gravável** (regra udev
nova `77-dualsense-leds.rules`: `TAG+="uaccess"` + `chmod 0666` em
`multi_intensity`/`brightness`). Se não for (sem a regra instalada), `_suppress_leds`
fica `False` e o caminho pydualsense segue como antes — sem piora. `set_led`,
`set_player_leds` e `_reapply_desired` preferem o sysfs com fallback pydualsense,
via o helper `_for_each_led` (respeita o alvo de output do seletor de controle).

**Pré-requisito do dia:** o BT precisou ser **re-pareado** — o controle estava
`Connected: yes` mas sem hidraw/evdev (HID SDP record ausente após troca de
adaptador BT). Playbook em `~/.claude/.../memory/reference_dualsense_bt_repair_sdp.md`.

**Validação ao vivo (BT):** cores vermelho → verde → azul → laranja mudaram na
lightbar via o IPC `led.set` (o mesmo caminho que a GUI usa). Testes:
`tests/core/test_sysfs_leds.py`.

## 2. Footer cortado sob o tiling do COSMIC

Os 4 botões do rodapé (Aplicar/Salvar/Importar/Restaurar) sumiam. Causa: o
`GtkNotebook` pede altura mínima = MÁXIMO de todas as páginas (puxada por
Perfis/Emulação), e o tiling do COSMIC ignora o `height-request` da janela.
Fix: páginas roláveis (`GtkScrolledWindow` por página, exceto Daemon) + botões num
`GtkFlowBox` (quebram em 2 colunas quando estreito) + `width/height-request`
mínimos. Validado visualmente: os 4 botões aparecem em qualquer largura.

## 3. Auditoria multi-agente (26 achados confirmados)

Workflow com verificação adversarial (cada achado refutado por verificadores
independentes antes de entrar): 1 HIGH, 13 MEDIUM, 9 LOW, 3 NIT; 5 rejeitados.
Todos aplicados nesta sessão. Destaques:

- **HIGH — `profile activate` não trocava o perfil do daemon vivo**: abria um 2º
  controller e só gravava o marcador; o daemon sobrescrevia. Agora vai por IPC
  `profile.switch` (fallback offline preservado).
- **"Tudo via interface"**: `test trigger`/`test rumble` também tentam IPC antes
  do hardware; subcomando standalone `emulate xbox360` removido (duplicava o
  gamepad do daemon).
- **MEDIUM — `MetricsSubsystem` nunca iniciava** (config morta): agora sobe no
  `run()` quando `metrics_enabled`.
- **MEDIUM — `mic_button_loop` bloqueava o event loop ~4s** (subprocess wpctl):
  offloadado via `daemon._run_blocking`.
- **MEDIUM — validação de `TriggerConfig.mode`**: modo inválido falha na validação
  do perfil, não em runtime no apply.
- **Perf/UX da GUI**: tray e I/O de perfil saíram da thread GTK; statusbars não
  empilham mais; `_render_offline` com None-guard.
- **LOW/NIT**: observabilidade do rumble auto vinda da política viva; guard de
  abertura concorrente no `connect()`; código morto removido
  (`_refresh_lightbar_from_state`); `uninstall.sh` remove AppImage em
  `~/.local/bin` + regras 76/77; `meu_perfil` priority 1 (catch-all acima do
  fallback); i18n de toasts; doc Nix `daemon start --foreground`; applet "Sair"
  com fallback pkill.

## 4. Release v3.10.0

- Bump `3.9.0 → 3.10.0` em `pyproject.toml`, `README.md`, `__init__.py` (fallback).
- CHANGELOG: `[Unreleased]` (que já acumulava seletor, co-op, multi-controle,
  applet, botões segmentados, fix de CRC BT) virou `[3.10.0] — 2026-06-28`, com as
  entradas de hoje; o TODO "lightbar por BT não acende" foi removido (resolvido).
- Gates locais verdes: `check_version_consistency`, `check_anonymity`, version-sync,
  ruff, mypy, **1675 testes**.
- Tag `v3.10.0` empurrada no `origin` (fork) → dispara `release.yml`
  (anonimato → testes → wheel/sdist → .deb por distro → GitHub Release).

## Arquivos-chave

- Novo: `core/sysfs_leds.py`, `assets/77-dualsense-leds.rules`,
  `tests/core/test_sysfs_leds.py`.
- Mexidos: `core/backend_pydualsense.py` (rota sysfs + suppress + guard),
  `gui/main.glade` + `app/app.py` (footer/scroll), `app/actions/*` (via-interface,
  perf, toasts), `cli/cmd_*` (IPC-first), `daemon/lifecycle.py` (metrics),
  `daemon/subsystems/hotkey.py` (mic non-blocking), `profiles/schema.py`
  (validação de modo), `scripts/install*udev*.sh` + `uninstall.sh` (regra 77).
