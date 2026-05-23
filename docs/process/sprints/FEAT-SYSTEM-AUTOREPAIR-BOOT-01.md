# FEAT-SYSTEM-AUTOREPAIR-BOOT-01 — detecta infra quebrada no boot e avisa

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** M · **Dependências:** FEAT-DOCTOR-HEALTHCHECK-01 · **Status:** DONE

## Contexto

Os problemas de infra mais comuns (regras udev de hotplug com nome de unit antigo após um update;
WirePlumber sequestrando o microfone do DualSense) só eram detectados se o usuário rodasse o
`doctor` manualmente. Faltava o daemon AVISAR proativamente no boot.

## Decisão / Entrega

- Novo `core/system_check.py`: `system_warnings()` — checks read-only (espelham parte do
  `doctor.sh`): udev 73/74 com nome de unit errado, WirePlumber fixando o DualSense como source.
  Devolve mensagens com o comando de reparo sugerido. NUNCA levanta, NUNCA roda sudo/reparo.
- `daemon/lifecycle.py`: `_check_system_on_boot()` chamado no fim do boot — log + notificação D-Bus
  (uma vez) se houver problema. Best-effort.
- `integrations/desktop_notifications.py`: `notify_system_warnings()`.

## Segurança

Por design, **só detecta e sugere** — o reparo (sudo) fica a cargo do usuário (`doctor --fix` ou o
comando indicado). O daemon nunca eleva privilégio sozinho.

## Critérios de aceite

- udev de hotplug desatualizado e WirePlumber sequestrando o mic são detectados e reportados no boot.
- ruff + mypy --strict + pytest (suíte completa, 1418) verdes.

## Arquivos tocados

- `src/hefesto_dualsense4unix/core/system_check.py` (novo), `daemon/lifecycle.py`,
  `integrations/desktop_notifications.py`
- `tests/unit/test_system_check.py` (novo)
