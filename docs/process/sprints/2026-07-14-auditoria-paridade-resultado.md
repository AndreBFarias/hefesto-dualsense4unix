# Auditoria da Matriz de Paridade — resultado (FEAT-PARITY-REVIEW-01)

Executada 2026-07-14 por 17 agentes de leitura + verificação adversarial
(workflow `auditoria-paridade-features`). Base empírica: testes SDL2 locais que
provaram a causa-raiz do rumble in-game (ver SPRINT-GAME-RUMBLE-01 abaixo).

## 1. Matriz capacidade × modo

| Capacidade | Desktop | vpad P1 | vpad co-op | Nativo |
|---|---|---|---|---|
| **Input** (botões/sticks/gatilhos) | FUNCIONA | FUNCIONA | FUNCIONA | FUNCIONA |
| **Rumble** (jogo→controle) | N/A | DEGRADADO | DEGRADADO | FUNCIONA |
| **Gatilhos adaptativos** | N/A | MORTO | MORTO | FUNCIONA |
| **Lightbar RGB** | FUNCIONA | MORTO | MORTO | FUNCIONA |
| **Player-LED** | FUNCIONA | DEGRADADO | FUNCIONA | DEGRADADO |
| **Giroscópio / acelerômetro** | MORTO | MORTO | MORTO | FUNCIONA |
| **Touchpad** | FUNCIONA | MORTO | MORTO | DEGRADADO |
| **Microfone / áudio** | FUNCIONA | FUNCIONA | DEGRADADO | DEGRADADO |
| **Bateria** | FUNCIONA | DEGRADADO | DEGRADADO | FUNCIONA |
| **PS / Mute / Create / Options** | FUNCIONA | DEGRADADO | DEGRADADO | DEGRADADO |

Leitura: o núcleo (input) tem paridade total nos 4 modos. Quase tudo que "morre"
no vpad morre por **limite do uinput** (sem canal p/ trigger/LED/gyro/touchpad/
bateria), não por bug. O **Nativo** é o único modo onde o output completo
(rumble/gatilhos/lightbar/gyro) chega ao controle — por ceder o HID ao jogo.

## 2. Bugs corrigíveis CONFIRMADOS (priorizados)

**1. Rumble morto no vpad P1 pela máscara default** — `rumble / vpad_p1`
Pipeline FF 100% wired, mas `gamepad_flavor='dualsense'` (lifecycle.py:101;
uinput_gamepad.py:56-57,92) faz o HIDAPI do jogo enumerar o DualSense **físico**
via hidraw e ignorar o vpad (mesmo VID/PID, sem hidraw) → nenhum upload de FF →
sink nunca dispara. **Provado com SDL2 local** (2026-07-14): com máscara DualSense
o SDL vê só os 2 físicos via /dev/hidraw; com Xbox 360 o vpad aparece via evdev/FF.
*Fix:* `flavor='xbox'` nos perfis que querem rumble; documentar `SDL_JOYSTICK_HIDAPI=0`
como alternativa p/ quem quer manter prompts PS.

**2. Rumble morto no co-op + flavor não propaga aos secundários** — `rumble / vpad_coop`
`_flavor()` só é lido na criação do vpad (coop.py:244-245,347); `set_gamepad_emulation`
recria só o P1 e `coop.sync(force=True)` só existe em `set_coop_enabled`
(lifecycle.py:776), não no path de troca de flavor → P2 fica preso em `dualsense`
mesmo com P1 em `xbox`. **Confirmado ao vivo** (event258 demorou a virar Xbox).
*Fix:* teardown por flavor-mismatch em `coop.sync()` + `coop.sync(force=True)` a
partir de `set_gamepad_emulation`.

**3. Botão PS rouba foco pro Steam durante o jogo** — `ps / vpad_p1`
`observe()` (lifecycle.py:1609-1610) roda fora do `if not gamepad_dispatched`; com
`ps_button_action='steam'` um tap de PS vira BTN_MODE pro jogo **E** dá `wmctrl` no
Steam (hotkey.py:31-38). Guard `should_passthrough` é código morto.
*Fix:* early-return no callback PS-solo quando há vpad ativo; remover código morto.

**4. Player-LED (e lightbar) furam o output-mute do Nativo via sysfs** — `player_led / nativo`
O mute é lido só no report_thread HID (backend_pydualsense.py:184); a rota sysfs de
player-LED não é gateada → reasserts reescrevem o padrão do perfil e pisam no número
que o jogo setou.
*Fix:* respeitar `self._output_mute` nas escritas/reasserts sysfs, preservando
`_desired` para restaurar no unmute.

**5. TouchpadReader não é parado no Nativo → salto de cursor** — `touchpad / nativo`
`_release_controller_to_game` não para o reader; o poll dá `continue` antes de
drenar, então `_accum_dx/dy` cresce a sessão inteira e vira salto quando o mouse é
restaurado do stash na saída.
*Fix:* em nativo, `discard_touchpad_motion()` a cada tick antes do `continue`.

**Reverificado (2026-07-14):** `microfone / vpad_coop` (Mute de P2-P4 morto) —
CONFIRMADO real, mas **não é bug**: é limitação arquitetural + decisão de produto.
O `mic_btn` só é lido do controle primário (via HID cru; sem keycode evdev estável —
evdev_reader.py:347-352) e o input do bus vem só do primário (lifecycle.py:1642-1645,
backend_pydualsense.py:645-647); os secundários usam EvdevReader puro que não enxerga
`mic_btn` (coop.py:304). Como há um único microfone de sistema, o P1 já cobre 100% da
função. Ação: DOCUMENTADO no README (não implementar feature nova). Se um dia quiserem
Mute por-jogador: leitor HID-raw do `micBtn` por secundário (seam em coop.forward_all,
usando o handle por-MAC de `_handles`/`set_output_target`), com LED de mic em broadcast.

## 3. Limitações reais a DOCUMENTAR no README (não são bugs)

- Gatilhos adaptativos no vpad — uinput não tem canal de resistência. Só Nativo.
- Lightbar RGB no vpad — uinput não expõe LED. Só cor estática do perfil.
- Giroscópio/acelerômetro no vpad — motion fica no device físico. Gyro-aim só Nativo.
- Touchpad no vpad — SDL lê o touchpad pela HID real; vpad não tem BTN_TOUCH/ABS_MT.
- Bateria no jogo pelo vpad — uinput não tem power_supply → SDL vê UNKNOWN (GUI mostra a real).
- Player-LED via jogo pelo vpad — vpad anuncia EV_FF mas não EV_LED.
- Botão Mute (mic) — nenhum gamepad padrão tem; nunca encaminhável ao jogo.

## 4. Top 3 ações por impacto

1. **Destravar rumble no vpad** (bugs #1+#2) — razão de existir o "Jogar pelo Hefesto".
2. **Fechar o canal sysfs sob output-mute no Nativo** (bug #4).
3. **Higienizar o hands-off vpad/nativo** (bugs #3+#5) — PS→Steam e salto de cursor.
