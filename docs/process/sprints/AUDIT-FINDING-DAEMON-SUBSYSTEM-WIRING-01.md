# AUDIT-FINDING-DAEMON-SUBSYSTEM-WIRING-01 — subsystems: wiring perdido + abstração duplicada

> Status: **AUDITADO (2026-06-03)** — NÃO é "código morto" a deletar. É dívida arquitetural + 1 bug
> de wiring. Remoção cega tiraria feature testada; requer decisão de refactor. Registrado aqui para
> virar sprint **com o daemon de pé** (esta máquina roda sem o daemon instalado — só valida por testes).

## Contexto
Auditoria de "código morto no daemon" pedida na faxina de 2026-06-03. A verificação mostrou que os 3
pontos sinalizados **não são removíveis com segurança** — cada um é uma coisa diferente:

## Achado 1 — `MetricsSubsystem` perdeu o wiring (BUG real, não código morto)
- `MetricsSubsystem` (`daemon/subsystems/metrics.py`) é feature documentada (ADR-016), tem sprint
  (FEAT-METRICS-01) e testes (`tests/unit/test_metrics.py`), com `is_enabled()` gated em
  `metrics_enabled` (default `False`, `lifecycle.py:96`).
- **MAS `Daemon.run()` (`lifecycle.py:207-220`) NUNCA o inicia** — a sequência é hand-rolled via
  `_safe_start("ipc"/"udp"/...)` e **não há `_safe_start("metrics", ...)`**. Logo, mesmo com
  `metrics_enabled=True` o servidor Prometheus **não sobe** (regressão provável do REFACTOR-LIFECYCLE-01).
- `test_metrics.py` testa o subsystem **isolado** (start/stop direto), não via `run()` → o wiring não
  tem cobertura.
- **Ação (sprint próprio, daemon de pé):** religar seguindo o padrão de `_plugins_subsystem`
  (`connection.shutdown` para por atributo `daemon._plugins_subsystem`): adicionar campo
  `_metrics_subsystem`, método `_start_metrics` (cria `MetricsSubsystem`, monta `DaemonContext`,
  `start(ctx)`, guarda), `if self.config.metrics_enabled: await self._safe_start("metrics", ...)` em
  `run()`, e `stop()` em `connection.shutdown`. Validar com `curl :9090/metrics` no daemon real.

## Achado 2 — Duas implementações de subsystem coexistindo (dívida arquitetural)
- `SUBSYSTEM_REGISTRY` (`daemon/subsystems/__init__.py:24`) lista 8 CLASSES-subsystem
  (`PollSubsystem`, `IpcSubsystem`, …) com a "ordem canônica de start/stop". **Nada importa o
  registry** (0 usos fora do `__init__`/`__all__`) — `run()` ignora-o e usa funções `_start_*`.
- Porém as classes **não são lixo**: cada uma tem módulo próprio (`subsystems/ipc.py`, …) e **teste
  próprio** (`tests/unit/test_subsystem_*.py`). Ou seja, existe uma abstração class-based testada **em
  paralelo** com a implementação function-based que o `run()` realmente usa.
- **Decisão necessária (maintainer):** (A) migrar `run()`/`shutdown` para serem dirigidos pelo
  `SUBSYSTEM_REGISTRY` (ordem declarativa + stop em ordem inversa — elimina a duplicação e o
  hand-roll), OU (B) remover a camada class-based + o registry + seus testes (se a direção é manter
  só as funções `_start_*`). Não decidir e só "deletar o registry" deixa as classes órfãs meio-soltas.
- **`KeyboardSubsystem`** é a única classe **totalmente órfã** (nem módulo de teste) — candidata segura
  a remoção isolada se a direção for (B).

## Achado 3 — `_rumble_engine` nunca é instanciado (latente; manter por ora)
- `ipc_handlers.py:305` e `ipc_rumble_policy.py:45` leem `getattr(daemon, "_rumble_engine", None)`;
  **nada no src atribui** `_rumble_engine` → sempre `None` em produção. 3 testes o setam a `None`
  explicitamente (scaffolding defensivo).
- Consequência **latente**: o writeback do multiplicador da política de rumble (economia/balanceado/
  max/auto) pode **não ser aplicado** de fato (sempre `None`). Não é "código morto" a deletar (é
  caminho defensivo testado) — é uma **feature possivelmente não-conectada** a confirmar **com
  hardware** (a política de intensidade realmente muda o rumble?). Se confirmado que não aplica:
  instanciar o engine no daemon OU consolidar a leitura em `_last_auto_mult`.

## Por que NÃO mexer agora
Daemon não instalado nesta máquina (setup enxuto) → só dá pra validar por unit tests, e os 3 itens ou
não têm cobertura do caminho afetado (metrics wiring) ou exigem decisão de refactor (registry) ou
verificação com HW (rumble). Mexer às cegas arrisca regressão numa peça crítica por ganho de higiene.
