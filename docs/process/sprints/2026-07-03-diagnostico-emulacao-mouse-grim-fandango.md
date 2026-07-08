# 2026-07-03 — Diagnóstico: emulação de mouse "bugada" + modo point-and-click (Grim Fandango)

> **Status:** DIAGNÓSTICO FECHADO — 2026-07-03. Sessão ao vivo com a Vitória jogando
> Grim Fandango Remastered via BT. Investigação por workflow (6 mapeadores + 11
> verificadores adversariais). **10 achados CONFIRMADOS, 1 REFUTADO.**
> Gera 3 sprints: `BUG-MOUSE-GUI-SYNC-01`, `FEAT-MOUSE-CURSOR-FEEL-01`,
> `FEAT-POINT-AND-CLICK-01`.

## Sintomas reportados

1. "A interface tá completamente bugada quando usamos ela" — GUI com emulação ativa.
2. "Precisamos de um modo que funcione pra jogos point and click."
3. "Dessa forma ele funciona mas não tá igual deveria estar tipo velocidade o r e afins."
4. "Se ativar o modo steam o default dele é assim mas ele não funciona" — Steam Input
   ligado quebra o controle no jogo.

## Estado vivo no momento do diagnóstico (22:08)

- Daemon ativo (PID 13510), DualSense via BT (bateria 85%), perfil `vitoria`.
- **Modo mouse LIGADO** (gamepad virtual destruído às 21:58:30), speed=6/scroll=1.
- GUI aberta mostrando o quê? Toggle refletia estado **divergente** do daemon (ver A1).
- Journal 21:59: `key_binding_emit options→KEY_LEFTMETA` (Super abre o launcher do
  COSMIC POR CIMA do jogo) e `create→KEY_SYSRQ` — vazamento clássico (ver A10).
- Journal inundado (1074/1477 linhas em 2h) por `autoswitch_suppressed_by_manual_override`
  a ~2 Hz.
- Steam Input: `PSSupport=0` OK; `UseSteamControllerConfig` ainda em 2 entradas
  (guard reaplica quando a Steam fechar).

## Achados confirmados

| # | Achado | Evidência-chave | Sprint |
|---|--------|-----------------|--------|
| A1 | GUI nunca lê `state_full.mouse_emulation`; abre OFF/6/1 mesmo com daemon em modo mouse | `app.py:568-571` lê só `active_profile`; grep: zero consumidores em `app/` | BUG-MOUSE-GUI-SYNC-01 |
| A2 | "Aplicar" desliga a emulação viva e **persiste o flag off** (draft default `enabled=False` sempre enviado) | repro headless: `('set_mouse_emulation', False, 6, 1)`; `draft_config.py:274-278` → `ipc_draft_applier.py:145-159` → `mouse.py:113-118` | BUG-MOUSE-GUI-SYNC-01 |
| A3 | Toggle com daemon offline → reentrada infinita (999x) + RecursionError; UI congelada até ~4 min | repro GTK3 real; `mouse_actions.py:93` reverte com `set_active` sem `_guard_refresh` | BUG-MOUSE-GUI-SYNC-01 |
| A4 | Slider com toggle stale-ON **religa** a emulação (e mata gamepad virtual em pleno jogo) + persiste | `mouse_actions.py:118-120` decide pelo widget; repro: device recriado, `save(True)` | BUG-MOUSE-GUI-SYNC-01 |
| A5 | Velocidades não persistem (flag guarda só enabled; restart volta a 6/1) | repro headless com XDG isolado; `session.py:138-161`, `main.py:74-84` | FEAT-MOUSE-CURSOR-FEEL-01 |
| A6 | Fallback HID-raw converte sticks errado: `int(state.LX) & 0xFF` com LX já centrado em 0 (pydualsense 0.7.5 faz `states[1]-128`) → repouso vira 0/~253 → cursor voa | repro com `readInput` real: cru=125 → raw=253 → dx=+5; explica memória "sticks ~253" | FEAT-MOUSE-CURSOR-FEEL-01 |
| A7 | Cursor lento e quantizado: máx 300 px/s @ speed 6 (1920px em 6,4s); só 5 velocidades discretas (saltos de 60 px/s); speed=1 é INCAPAZ de mover para direita/baixo; assimetria ±(360 vs 300 px/s) | tabela deflexão→px/tick medida com `_compute_move` real; `uinput_mouse.py:108-113` linear truncado sem carry (touchpad TEM carry, stick não) | FEAT-MOUSE-CURSOR-FEEL-01 |
| A8 | `profile.switch` (IPC) e autoswitch NÃO propagam `key_bindings` ao teclado vivo — managers capturam `keyboard_device=None` no boot (IPC/autoswitch sobem antes do keyboard) | repro pytest com wiring real falha; `subsystems/ipc.py:69` sem device; `autoswitch.py:105-109` captura None; teste existente injeta mock (mascara o bug) | FEAT-POINT-AND-CLICK-01 |
| A9 | Grim Fandango Remastered embarca SDL 2.0.3 (2014) + `controllerdef.txt` **sem** o GUID do DualSense (little-endian `e60c` ausente) — mas **com** X360 Linux e DS4 v1 | `~/.steam/debian-installation/steamapps/common/Grim Fandango Remastered/controllerdef.txt` (md5 04dffbe...); strings do binário: `SDL2-2.0.3` | FEAT-POINT-AND-CLICK-01 |
| A10 | Vazamento por design sem gate automático: com emulação ativa e sem modo-jogo, options/create/l1/r1 emitem Super/PrintScreen/Alt+Tab no desktop durante o jogo; nenhum mecanismo por janela suprime | journal 21:59 durante o jogo; único gate é manual (`_emulation_suppressed`) | FEAT-POINT-AND-CLICK-01 |

Extras menores confirmados no mapeamento (não verificados adversarialmente, baixo risco):

- Card "Mapeamento" da aba Mouse é 100% estático no glade e com glyphs strippados
  ("Triângulo ()" com parênteses vazios — ADR-011 sanitizou U+25B3/U+25CB).
- Handlers da aba Mouse fazem IPC bloqueante na thread GTK (contrato de
  `ipc_bridge.py` diz para não fazer) — jank em arrasto de slider.
- `FROZEN_WIDGET_IDS` do Aplicar não congela os sliders de mouse.
- `docs/protocol/ipc-unix-socket.md` documenta 8 de 25 métodos IPC.
- Spam `autoswitch_suppressed_by_manual_override` a ~2 Hz no journal.

## Achado REFUTADO

- **V8 — combo gamemode "fantasma" no startup**: REFUTADO. O HotkeyManager só enxerga
  botões do snapshot evdev (`lifecycle.py:852→956`), que nasce vazio e é 100%
  event-driven; o fallback HID-raw no máximo injetaria `mic_btn`; o grace de 0,3s
  gateia o hotkey também; e o `state_stale_neutral_warning` exige botões VAZIOS.
  O `hotkey_fired combo=gamemode` das 21:58:11 foi aperto físico real (PS+Options),
  ~600ms após restart deliberado do daemon. Nenhum fix necessário.

## Fatos de pesquisa (Grim Fandango Remastered)

- O jogo TEM point-and-click por mouse oficial desde 2015 (código do mod Grim Mouse
  incorporado pela Double Fine) — clique move o Manny, duplo-clique corre, diálogos
  por mouse. **O modo mouse do hefesto é o caminho certo para esse jogo** — só precisa
  de cursor digno (A7) e bindings de teclado que não vazem para o desktop (A10).
- Teclado default do jogo: setas=mover, Left Shift=correr, E=examinar, U=usar,
  P=pegar, I=inventário, Delete=trocar objeto, `.`=pular diálogo, Backspace=render,
  Z=comentários.
- Steam Input neste título é incompatível no Linux (bug conhecido de 2019, threads
  Steam) — consistente com o sintoma 4. Manter Steam Input OFF para este jogo.
- Rota alternativa de gamepad nativo: máscara **xbox360** do gamepad virtual do
  hefesto (o `controllerdef.txt` do jogo tem o GUID X360 Linux). O controle precisa
  existir ANTES de abrir o jogo.

## Decisão

Três sprints, em ordem (A depende de nada; C depende de A8 corrigido):

1. **BUG-MOUSE-GUI-SYNC-01** — a GUI para de mentir: sync com estado vivo, Aplicar
   seguro (dirty/None), guard no revert do toggle, slider não religa emulação,
   handlers async, freeze completo, glyphs do card.
2. **FEAT-MOUSE-CURSOR-FEEL-01** — cursor digno: pipeline float com carry + deadzone
   radial reescalada + curva expo + velocidade em px/s reais; persistência de
   speed/scroll no flag JSON; fix do fallback HID-raw (+128).
3. **FEAT-POINT-AND-CLICK-01** — modo point-and-click por perfil: Profile ganha seção
   opcional `mouse` + `suppress_desktop_emulation`; fix do wiring A-06 (A8, provider
   lazy); perfil default `point_and_click` (match GrimFandango/scummvm) com
   key_bindings de jogo; autoswitch aplica tudo ao focar a janela.

## Proof-of-work da sessão

- Workflows: `wf_e06ba9a5-6e4` (mapa, 6 agentes) e `wf_25dc588e-74a` (verificação,
  11 agentes). Repros headless em scratchpad da sessão (RecursionError GTK3 real,
  conversão pydualsense real, tabela px/tick, wiring A-06 via pytest).
- Nada foi modificado na máquina durante o diagnóstico (tudo read-only; daemon da
  Vitória intocado durante gameplay).
