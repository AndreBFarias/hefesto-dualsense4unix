# FEAT-EMULATION-GAMEMODE-LONGPRESS-01 — Modo jogo via long-press do PS

**Tipo:** feat (daemon/input).
**Wave:** V3.8.1 — correções pós-release v3.8.0.
**Estimativa:** M — gesto + gate + notificação + IPC + testes.
**Dependências:** nenhuma.
**Status:** DONE (código + 8 testes; suíte 1435 verde). Falta o smoke do gesto físico na máquina.

---

## Contexto

A mantenedora relatou uma "dor real": ao iniciar um jogo, o Hefesto continua emulando mouse/teclado —
o stick move o cursor e os botões digitam teclas, conflitando com o jogo. Ela pediu um gesto para
ligar/desligar a emulação. Decisões: gatilho = segurar o PS ~1s (long-press); escopo = suprimir **só
a emulação de mouse/teclado** (manter os hotkeys de troca de perfil).

## Decisão / Entrega

- `HotkeyManager` (`integrations/hotkey_daemon.py`): detecta o long-press do PS (segurado ≥
  `ps_long_press_ms`, default 1000ms, sem combo) e dispara `on_ps_long_press` uma vez por hold. O PS
  solo (toque curto → Steam) é suprimido quando o long-press disparou; o toque curto continua
  abrindo a Steam.
- `Daemon` (`daemon/lifecycle.py`): flag `_emulation_suppressed` (transitório). O poll loop pula
  `_dispatch_mouse/keyboard_emulation` quando suprimido — os devices uinput ficam vivos e o
  `observe`/hotkeys continuam rodando (por isso o gesto de reativar funciona). Método
  `set_emulation_suppressed(value=None)` (toggle/set) + notificação.
- `subsystems/hotkey.py`: `build_ps_long_press_callback` liga o gesto a `set_emulation_suppressed()`.
- `desktop_notifications.py`: `notify_emulation_suppressed` notifica **sempre** (ação deliberada),
  independente do opt-in das notificações automáticas.
- IPC: `emulation_suppressed` em `daemon.status`/`state_full`; método `daemon.emulation.suppress`
  (toggle/set) para GUI/applet/CLI.

## Critérios de aceite

- [x] `ruff` + `mypy --strict` limpos.
- [x] `pytest tests/unit` verde (1435 passed; +8 testes: long-press ×5, toggle/callback ×2, IPC ×1).
- [ ] Smoke na máquina: segurar o PS ~1s (controle plugado) → notificação "Modo jogo ligado" + o
  stick para de mover o cursor; segurar de novo → reativa. Toque curto segue abrindo a Steam.

## Arquivos tocados

- `integrations/hotkey_daemon.py`, `daemon/lifecycle.py`, `daemon/subsystems/hotkey.py`,
  `daemon/protocols.py`, `integrations/desktop_notifications.py`, `daemon/ipc_handlers.py`,
  `daemon/ipc_server.py`.
- `tests/unit/test_hotkey_ps_button.py`, `tests/unit/test_ipc_server.py`.

## Notas para o executor

O detector de long-press roda no `HotkeyManager.observe`, chamado no poll loop só quando o input está
pronto (não pausado, fora do grace). Como o "modo jogo" usa um gate **separado** do pause
(`_emulation_suppressed`, só mouse/teclado), o `observe` continua rodando enquanto suprimido — então
o gesto de reativar funciona. Se um dia o modo jogo passar a usar `pause` (que suprime os hotkeys), o
detector precisaria rodar fora desse gate.

## Fora de escopo

- Auto-detecção de jogo em foco (frágil no COSMIC — wlrctl quebrado).
- Persistência do modo jogo entre boots (transitório por design).
- Indicador "modo jogo" na GUI/applet (o estado já é exposto via IPC `emulation_suppressed`; a UI
  fica para incremento futuro).
