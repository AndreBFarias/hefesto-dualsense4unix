# BUG-GUI-IDLE-ADD-BUSY-LOOP-01 — Busy-loop a 100% CPU na GUI (e 5 GB de RAM)

**Tipo:** fix (perf/GUI).
**Wave:** V3.8.1 — correções pós-release v3.8.0.
**Estimativa:** XS — wrapper one-shot em 2 chamadas + teste.
**Dependências:** nenhuma.
**Status:** DONE (fix + teste; **validado na máquina: 104% → 2.4% CPU, 5.3 GB → 90 MB RAM**).

---

## Contexto

Durante o review de UI/UX da v3.8 a mantenedora relatou que "a interface tá muito ruim de navegar
e super lento". Sintoma observado na máquina ao reabrir a GUI: thread principal a **104% de CPU**
(core inteiro), processo crescendo até **5.3 GB de RAM** em ~5 minutos. O daemon, isoladamente,
estava saudável.

## Diagnóstico (causa-raiz)

`StatusActionsMixin.install_status_polling`
(`src/hefesto_dualsense4unix/app/actions/status_actions.py:113-121`) registra os ticks de polling
do estado em **dois** mecanismos GLib:

```python
GLib.timeout_add(LIVE_POLL_INTERVAL_MS, self._tick_live_state)     # 10 Hz — OK
GLib.timeout_add(STATE_POLL_INTERVAL_MS, self._tick_profile_state) # 2 Hz — OK
...
# Primeira leitura imediata para evitar a janela de "Consultando..." no boot
GLib.idle_add(self._tick_live_state)      # ← BUG
GLib.idle_add(self._tick_profile_state)   # ← BUG
```

`_tick_live_state` e `_tick_profile_state` retornam `True` para manter o `timeout_add` vivo
(contrato GLib). Mas `GLib.idle_add(fn)` **reagenda `fn` enquanto ela retornar `True`** — então as
duas chamadas viram **dois busy-loops infinitos na main loop GTK**, disparando `call_async` o mais
rápido possível e acumulando futures/callbacks no executor → 100% CPU + memory leak. Bug
pré-existente (commit `e5eb7561` de 2026-04-23, herdado do upstream); ficou invisível porque o
sintoma se manifesta como "GUI lenta", não como crash.

Confirmação empírica via `py-spy dump`:
```
Thread MainThread (active+gil): call_async → _tick_live_state → main loop GTK ...
```

## Decisão / Entrega

Trocar as duas chamadas de `idle_add` por wrappers one-shot que executam o tick e retornam `False`,
evitando o reagendamento. A intenção original (executar uma primeira leitura cedo) fica preservada.

```python
GLib.idle_add(lambda: self._tick_live_state() and False)
GLib.idle_add(lambda: self._tick_profile_state() and False)
```

## Critérios de aceite

- [x] `ruff` + `mypy --strict` limpos.
- [x] `pytest tests/unit` verde (1436 passed; +1 teste que prova one-shot via captura do
  `idle_add`).
- [x] Smoke na máquina: GUI passou de **104% CPU / 5.3 GB RAM** para **2.4% CPU / 90 MB RAM**.

## Arquivos tocados

- `src/hefesto_dualsense4unix/app/actions/status_actions.py` — wrappers one-shot.
- `tests/unit/test_status_actions_reconnect.py` — teste captura `idle_add` e prova retorno `False`.

## Notas para o executor

`fn() and False` é Python idiomático: o `and` avalia `fn()` (efeito colateral), e como `False`
encerra o curto-circuito, o resultado é sempre `False` — o que GLib precisa para não reagendar. O
mesmo padrão pode ser usado em qualquer ponto futuro onde se quiser uma "primeira execução
imediata" de um tick periódico.

## Fora de escopo

- Reescrever a aba Status com um único loop async — fora de proporção para o sintoma. A correção
  cirúrgica resolve o bug sem mudar a estrutura.
