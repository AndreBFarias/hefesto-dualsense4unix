# FEAT-DAEMON-DISABLE-CONTROL-01 — desligar/desativar o daemon sem desinstalar

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** P · **Dependências:** FEAT-DAEMON-PAUSE-RESUME-01 · **Status:** DONE

## Contexto

Complemento do pausar: além de pausar em runtime (daemon vivo, sem input), faltava um "desligar"
claro — parar o daemon **e** desabilitar o auto-start no boot, sem remover a unit (uninstall).
Antes, o usuário teria de combinar `daemon stop` + `systemctl --user disable` à mão.

## Decisão / Entrega

- `daemon/service_install.py`: métodos públicos `disable()` (stop + `systemctl --user disable`,
  mantém a unit instalada) e `enable()` (`systemctl --user enable` + start).
- CLI: `hefesto-dualsense4unix daemon disable` / `enable`.
- Três níveis claros de "desativar" agora: **pausar** (runtime, daemon vivo) → **desligar**
  (`disable`: para + sem auto-start, mas instalado) → **desinstalar** (`uninstall-service`/`purge`).

## Critérios de aceite

- `daemon disable` para o daemon e desabilita o auto-start, mantendo a unit.
- `daemon enable` religa (auto-start + start).
- ruff + mypy --strict + pytest (2 testes novos) verdes.

## Arquivos tocados

- `src/hefesto_dualsense4unix/daemon/service_install.py`, `src/hefesto_dualsense4unix/cli/app.py`
- `tests/unit/test_daemon_disable_control.py` (novo)
