# FEAT-DAEMON-PAUSE-RESUME-01 — pausar/retomar o daemon em runtime

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** M · **Dependências:** — · **Status:** DONE (backend); GUI/applet em follow-up

## Contexto

A mantenedora notou que, uma vez instalado, não dava para "desativar" o programa sem desinstalar:
o CLI/GUI só ofereciam `stop`/`start` (que matam e revivem o daemon, derrubando o socket IPC).
Faltava um **pausar** — manter o daemon vivo (telemetria, IPC, GUI/applet conectados) mas parar de
enviar input ao sistema.

## Decisão / Entrega (backend)

- `daemon/lifecycle.py`: flag `_paused` + métodos `pause()`/`resume()`/`is_paused()`. O gate de
  despacho do `_poll_loop` passou a respeitar `_paused` (reusa o mesmo mecanismo do grace-period):
  pausado, o loop segue lendo estado/bateria e publicando STATE_UPDATE, mas NÃO despacha
  teclado/mouse/hotkey nem publica BUTTON_DOWN/UP. O baseline de botões fica sincronizado durante
  a pausa, então ao retomar botões segurados não disparam.
- Persistência: `utils/session.py` ganhou `save_paused_state`/`load_paused_state` (arquivo-flag
  `paused.flag`). `run()` restaura o estado no boot — retoma pausado após restart.
- IPC: métodos `daemon.pause`/`daemon.resume`, e `paused` exposto em `daemon.status`
  (`ipc_handlers.py`, `ipc_server.py`). `DaemonProtocol` atualizado.
- CLI: `hefesto-dualsense4unix daemon pause` / `resume` (via IPC).

## Critérios de aceite

- `daemon pause` para o despacho de input sem matar o daemon (socket/telemetria seguem vivos).
- `daemon resume` restaura o despacho; botões segurados não disparam ao retomar.
- Retoma pausado após restart.
- ruff + mypy --strict + pytest (5 testes novos) verdes.

## Follow-up (mesma feature, próxima leva)

- GUI: botão Pausar/Retomar na aba Daemon (estado visual distinto de parado).
- Applet COSMIC (Rust): ação TogglePause no popover (recompila o applet).

## Arquivos tocados

- `src/hefesto_dualsense4unix/daemon/lifecycle.py`, `protocols.py`, `ipc_handlers.py`, `ipc_server.py`
- `src/hefesto_dualsense4unix/utils/session.py`, `src/hefesto_dualsense4unix/cli/app.py`
- `tests/unit/test_daemon_pause.py` (novo)
