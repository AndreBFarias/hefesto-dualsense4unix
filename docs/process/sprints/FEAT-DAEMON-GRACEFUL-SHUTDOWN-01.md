# FEAT-DAEMON-GRACEFUL-SHUTDOWN-01 — fechar IPC/UDP com timeout no shutdown

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** P · **Dependências:** — · **Status:** DONE (escopo ajustado)

## Contexto

O plano previa "shutdown gracioso com flush de estado". A auditoria mostrou que o shutdown
(`connection.shutdown`) **já era gracioso** (para plugins/mouse/keyboard/IPC/UDP/autoswitch com
`suppress`, cancela tasks, desconecta, fecha executor) e **já testado** (gracioso + tolera
subsystem que falha no stop + idempotente). E o estado relevante já é persistido
**incrementalmente**: perfil ativo no `profile.switch`, estado de pausa no `pause()` — restaurados
no boot.

O único gap real era o citado no plano: "fechar o socket com timeout". Um `stop()` que **trave**
(cliente em voo, await pendurado) penduraria o shutdown indefinidamente — o `suppress` não cobre
travamento, só exceção.

## Decisão / Entrega

- `daemon/connection.py`: `ipc_server.stop()` e `udp_server.stop()` no shutdown agora rodam sob
  `asyncio.wait_for(..., timeout=2.0)` — um fechamento que trave não pendura mais o shutdown.

## Critérios de aceite

- Shutdown completa mesmo se o fechamento do IPC/UDP travar (timeout de 2 s).
- ruff + mypy --strict + pytest (testes de shutdown/connection existentes) verdes.

## Arquivos tocados

- `src/hefesto_dualsense4unix/daemon/connection.py`

## Nota

O "flush de estado" já é incremental (perfil/pausa persistidos quando mudam); não há estado em voo
crítico que se perca no shutdown. O graceful shutdown em si já estava implementado e testado.
