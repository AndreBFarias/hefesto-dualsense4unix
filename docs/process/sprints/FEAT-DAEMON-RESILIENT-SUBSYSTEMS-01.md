# FEAT-DAEMON-RESILIENT-SUBSYSTEMS-01 — um subsystem que falha não derruba o daemon

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** M · **Dependências:** — · **Status:** DONE

## Contexto

Parte do "mais seguro e inteligente": no boot, cada subsystem (IPC, UDP, autoswitch, mouse,
keyboard, hotkey, plugins) era iniciado direto; se um levantasse (dep nativa ausente, porta em
uso, permissão negada), o `run()` inteiro abortava — o daemon não subia, mesmo que o problema
fosse num subsystem opcional.

## Decisão / Entrega

- `daemon/lifecycle.py`: helper `_safe_start(name, starter)` que isola a inicialização de cada
  subsystem em try/except (aceita starters síncronos e assíncronos). Falha vira log + registro em
  `_failed_subsystems` (nome -> erro), e o boot segue.
- Os 8 starts no `run()` passaram a usar `_safe_start`. `_failed_subsystems` exposto no
  `DaemonProtocol` para diagnóstico (doctor/status).

## Critérios de aceite

- Um subsystem que levanta no start é isolado; o daemon segue rodando (poll/perfis vivos).
- ruff + mypy --strict + pytest (suíte completa, 1410) verdes — o boot não regrediu.

## Arquivos tocados

- `src/hefesto_dualsense4unix/daemon/lifecycle.py`, `src/hefesto_dualsense4unix/daemon/protocols.py`
- `tests/unit/test_daemon_resilient_subsystems.py` (novo)

## Notas / futuro

- Backoff/retry em runtime (circuit-breaker completo) e exposição de `_failed_subsystems` no
  `doctor`/`daemon.status` ficam para iteração futura; a base (isolamento + registro) já existe.
