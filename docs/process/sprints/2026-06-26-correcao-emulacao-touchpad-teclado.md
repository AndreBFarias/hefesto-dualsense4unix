# Sprint de correção — Emulação / Touchpad / Teclado (DualSense)

> Origem: sessão longa de trabalho (2026-06-26), depois de estabilizar o storm
> (áudio off). Esta sprint reúne (A) o que já foi corrigido AO VIVO nesta sessão e
> (B) o que falta — a aplicar/validar **após o logout+login** da Vitória.
> Logs da sessão de jogo (abrir/fechar) ficam na seção "Anexos" no fim.

## Contexto — bugs encontrados (todos pequenos, todos reais)

1. **Emulação de mouse "não funcionava"** — na verdade o **modo-jogo (supressão)** estava
   ligado. Ela alternava sem querer porque o **long-press do PS (1000ms)** colidia com o gesto
   de abrir a Steam. E o limiar nem era configurável (HotkeyManager criado sem config).
2. **"Control/Meta sempre segurado" + desktop "quebrado" com a emulação ativa** — `options`
   tem binding de teclado `KEY_LEFTMETA`. Ao fazer **PS+Options** (combo de modo-jogo), o
   `options` **vazava** pra emulação de teclado → Meta ia pro COSMIC. Pior: no mesmo tick a
   supressão ligava, o poll loop **parava de despachar** e o **release do Meta nunca era
   enviado → modificador TRAVADO**.
3. **Touchpad "engasgado" e "funciona sempre, independente do estado"** — o kernel
   `hid_playstation` expõe o touchpad como **device libinput separado** (`event14`) que move o
   cursor sempre, **brigando** com a emulação analógica do hefesto (duas fontes de ponteiro).
4. **Toggle de mouse não persistia** — `mouse_emulation_enabled` voltava ao default (off) a
   cada restart/reboot do daemon.
5. **evdev estagnado pós-restart** — em restart com controle conectado, o novo leitor evdev às
   vezes não anexa (corrida de grab com o daemon anterior no grace do takeover) → input
   "morto" (sticks/botões neutros) apesar de "conectado". Warning: `state_stale_neutral_warning`.

## (A) JÁ CORRIGIDO ao vivo nesta sessão (no fork, instalação editável)

| ID | O quê | Arquivos |
|----|-------|----------|
| FEAT-EMULATION-GAMEMODE-COMBO-01 | Modo-jogo agora é **combo PS+Options** (deliberado), não mais long-press. Long-press configurável e **desligável** (`ps_long_press_ms`, 0=off). | `integrations/hotkey_daemon.py` (combo `gamemode`, guarda `>0`, passthrough), `daemon/lifecycle.py` (`DaemonConfig.ps_long_press_ms`), `daemon/subsystems/hotkey.py` (BUGFIX: propaga config — antes ficava preso em 1000ms), `daemon/main.py` (lê env) |
| FEAT-HOTKEY-COMBO-NO-LEAK-01 | Botões de um combo (PS+Options, PS+dpad) **não** são despachados à emulação → fim do vazamento de Meta/setas. | `integrations/hotkey_daemon.py` (`combo_buttons_active`), `daemon/lifecycle.py` (poll loop subtrai os botões bloqueados) |
| FEAT-EMULATION-GAMEMODE-FLUSH-01 | Ao **ligar a supressão**, solta tudo nos devices virtuais (mouse+teclado) → nenhum modificador trava. | `daemon/lifecycle.py` (`_flush_emulation_devices` chamado em `set_emulation_suppressed`) |
| FEAT-MOUSE-PERSIST-01 | Toggle de mouse **persiste** entre restart/reboot (flag-file, espelha `paused.flag`). **Provado**: restart → mouse religou sozinho. | `utils/session.py` (save/load), `daemon/lifecycle.py` (carrega no startup), `daemon/subsystems/mouse.py` (grava no toggle) |
| FEAT-DUALSENSE-TOUCHPAD-IGNORE-01 | Touchpad do DualSense **ignorado como ponteiro libinput** → para de brigar com o analógico. Click do touchpad segue lido pelo hefesto (teclas). | `assets/76-dualsense-touchpad-libinput-ignore.rules` (instalado em `/etc/udev/rules.d/`) |
| DURABILIDADE-DIST-UPGRADE-01 | `install.sh` recria o venv se o Python do sistema bumpar (full dist upgrade) ou se `bin/python` ficar inexecutável. | `install.sh` |

Config aplicada para a Vitória: `~/.config/environment.d/91-hefesto-dualsense-gamemode.conf`
(`...PS_LONG_PRESS_MS=0`); `mouse_emulation.flag` presente.

## (B) A FAZER após logout+login

### B0. Verificação pós-login (checklist)
- [ ] `systemctl --user show-environment | grep PS_LONG_PRESS_MS` → `=0` (veio do environment.d).
- [ ] Daemon sobe: `hotkey_manager_started ps_long_press_ms=0`, `mouse_emulation_started` (auto),
      **sem** `state_stale_neutral_warning`.
- [ ] **Replugar o controle 1x** → confirmar que o touchpad parou de mover o cursor
      (`LIBINPUT_IGNORE_DEVICE=1` só vale após re-add do device).
- [ ] PS+Options alterna modo-jogo **sem** abrir o launcher do COSMIC e **sem** travar Meta.
- [ ] PS (toque curto) abre a Steam; nunca cai no modo-jogo.

### B1. evdev estagnado pós-restart — auto-recuperação  *(robustez; média prioridade)*
Detectar `state_stale_neutral` persistente (N ticks neutros logo após conectar) e **re-anexar
o evdev / forçar reconnect** automaticamente, em vez de exigir replug. Hoje o daemon só *avisa*.
Risco real: em boot com o controle plugado, a mesma corrida pode deixar o input morto.

### B2. GUI: indicador de modo-jogo  *(UX; alta — foi o que fez a "flag parecer não ativar")*
A aba Mouse mostra só `mouse_emulation_enabled`. Falta mostrar **suprimido (modo-jogo) sim/não**
e, idealmente, um controle. Expor também `ps_long_press_ms` e `gamemode_toggle` nas preferências.

### B3. CLI: `mouse suppress on/off`  *(conveniência)*
Hoje a supressão só por IPC/combo. Expor no CLI (`hefesto-dualsense4unix mouse suppress ...`).

### B4. Touchpad gerenciado pelo hefesto  *(opcional; melhor UX que o B0-ignore)*
Em vez de só ignorar no libinput, o hefesto **grabar** o `event14` e integrar o touchpad à
emulação (move cursor quando emulação ON; respeita o modo-jogo). Aí o touchpad "respeita o
estado", que era o pedido original. Decisão de design pendente (ignore simples já resolve a briga).

### B5. Touchpad-click → Backspace/Enter/Delete  *(revisar)*
`core/keyboard_mappings.py` mapeia os 3 cliques do touchpad pra teclas destrutivas. Pode causar
"texto quebrado" ao clicar o touchpad sem querer. Avaliar tornar opcional/desligável.

### B6. Persistir `gamemode_toggle`/`ps_long_press_ms` em config de usuário
Hoje `ps_long_press_ms` só via env e `gamemode_toggle` só default. Levar pra um `daemon.toml`
ou pro session/prefs para edição sem mexer em environment.d.

## Anexos — outputs da sessão de jogo (abrir/fechar)
> Preenchido a partir de `scratchpad/game_watch.log` após a Vitória abrir e fechar o jogo.

_(pendente — coletando ao vivo)_
