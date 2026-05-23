# PERF-GUI-PROFILE-LOAD-NONBLOCKING-01 — Lentidão e trava ao usar a GUI

**Tipo:** perf (GUI).
**Wave:** V3.8.1 — correções pós-release v3.8.0.
**Estimativa:** S — cache em memória + carga assíncrona.
**Dependências:** nenhuma.
**Status:** DONE (cache + `run_in_thread`; 6 testes novos; suíte 1427 verde). Falta smoke na máquina.

---

## Contexto

A mantenedora relatou "lentidão e trava real ao clicar em outras abas" na GUI durante o review de
UI/UX da v3.8. A janela congelava ao interagir, especialmente na aba Perfis.

## Diagnóstico (causa-raiz)

`load_all_profiles()` (glob de `*.json` + `FileLock` + parse Pydantic de cada perfil) rodava
**síncrono na thread de UI** em vários pontos:

- `on_profile_selection_changed` (clique em um perfil na lista).
- `_reload_profiles_store` (abrir a aba Perfis, remover, recarregar, salvar).
- `_build_profile_from_editor` — chamado por `_refresh_preview` a **cada tecla/slider** no editor.
  Pior caso: digitar o nome de um perfil relê todos os JSONs do disco a cada caractere.

Com muitos perfis em disco, cada interação travava a janela inteira.

## Decisão / Entrega

Cache em memória dos perfis + carga assíncrona:

- Novo `ipc_bridge.run_in_thread(fn, on_success, on_failure)` — generaliza `call_async` para
  qualquer função bloqueante fora de IPC (ex.: ler perfis do disco), reusando o executor de 1 worker
  e re-postando os callbacks via `GLib.idle_add`.
- `_reload_profiles_store` carrega via `run_in_thread`; popula o `ListStore` e o cache
  (`_profiles_cache`) no callback (thread GTK). Param `on_done` encadeia o sync da seleção no boot.
- `on_profile_selection_changed` e `_build_profile_from_editor` leem do cache (`_find_cached_profile`),
  sem tocar o disco.
- O footer (salvar/importar) **mantém** `load_all_profiles()` síncrono: são ações raras e
  deliberadas, e evitam detecção de conflito de nome contra um cache potencialmente desatualizado.

## Critérios de aceite

- [x] `ruff` + `mypy --strict` limpos.
- [x] `pytest tests/unit` verde (1427 passed; +6 testes: `run_in_thread` ×2, cache ×4).
- [ ] Smoke na máquina: abrir a aba Perfis com vários perfis, selecionar/digitar sem travar.

## Arquivos tocados

- `src/hefesto_dualsense4unix/app/ipc_bridge.py` — `run_in_thread`.
- `src/hefesto_dualsense4unix/app/actions/profiles_actions.py` — cache, `_find_cached_profile`,
  `_populate_profiles_store`, `_reload_profiles_store` assíncrono.
- `tests/unit/test_ipc_bridge_async.py`, `tests/unit/test_profiles_gui_sync.py` — testes.

## Notas para o executor

`_reload_profiles_store` agora é assíncrono — quem chama não pode assumir o store populado na hora
(todos os chamadores apenas disparam o reload). O cache reflete o último reload; o botão "Recarregar"
força a atualização se algo mudou por fora da GUI.

## Fora de escopo

- Suspender os timers de polling da aba Status quando a janela perde foco — esses já são
  assíncronos (`call_async`), não causavam a trava.
- Footer salvar/importar permanecem síncronos (ações raras).
