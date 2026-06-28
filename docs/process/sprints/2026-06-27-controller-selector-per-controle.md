# Sprint: Seletor de controle (config por-controle) — FEAT-DSX-CONTROLLER-SELECTOR-01

**Data:** 2026-06-27 · **Autora:** vitoriamaria · **Status:** A EXECUTAR (agente)

## Objetivo

Hoje o output do multi-controle é **broadcast**: tudo que se configura (lightbar,
gatilhos, player-LED, rumble, mic-LED) vai para TODOS os controles igual — por
isso, com 2 controles, **ambos mostram o LED do Player 1**. Esta sprint adiciona
um **seletor de controle**: a pessoa escolhe um controle (no banner da GUI / no
applet) e as ações de output passam a mirar **só ele**. Resolve o "ambos P1"
(seleciono o Controle 2 → seto o LED dele como Player 2) e permite config por
controle (cor azul no P1, vermelha no P2). Padrão = "Todos" (broadcast, igual a
hoje). Complementa o co-op (FEAT-DSX-COOP-LOCAL-01, já entregue).

## Contexto do código (já existe)

- Backend real: `src/hefesto_dualsense4unix/core/backend_pydualsense.py`
  (`PyDualSenseController`). Handles multi-controle em `self._handles` (dict
  ORDENADO por inserção; 1º = primário). Todo output passa por
  `_for_each(op, what=...)` (linha ~489) → escreve em cada handle. `describe_controllers()`
  (linha ~593) devolve `[{connected, transport, is_primary}]` por handle.
- `daemon.state_full` (`daemon/ipc_handlers.py::_handle_daemon_state_full`) já
  expõe o bloco `result["controllers"]` (via `describe_controllers`) e blocos
  `gamepad_emulation`/`coop`. Registro de métodos IPC em `daemon/ipc_server.py`
  (dict `"metodo": self._handle_...`). Handlers ficam no mixin `ipc_handlers.py`.
- GUI: aba Status em `app/actions/status_actions.py` (helpers estáticos
  `_connected_controllers`/`_controllers_transports` já existem e leem
  `state["controllers"]`). Header em `header_connection`. Banner/cabeçalho da
  janela: ver `gui/main.glade` (o header com logo + "Conectado…"). Tray GTK:
  `app/tray.py`. Janela compacta: `app/compact_window.py`. Applet COSMIC (Rust):
  `packaging/cosmic-applet/src/{app.rs,ipc.rs}` (struct `DaemonState` +
  `ControllerInfo` já têm `transport`/`is_primary`).
- CLI: subcomandos em `cli/cmd_*.py` registrados em `cli/app.py` via `add_typer`.
  Padrão de comando: ver `cli/cmd_coop.py` (on/off/status com `_run_call`).

## Design

### 1. Backend (`backend_pydualsense.py`) — alvo por controle
- Novo campo no `__init__`: `self._output_target_key: str | None = None`
  (None = TODOS / broadcast). Guardar a KEY (estável: serial/MAC), NÃO o índice.
- `_for_each`: sob `_io_lock`, se `_output_target_key` está setada E presente em
  `_handles`, aplicar SÓ a esse handle; senão, a todos (comportamento atual).
  Se a key alvo sumiu (controle desconectou), cair em broadcast.
- `set_output_target(self, index: int | None) -> int | None`: mapeia ÍNDICE
  (posição em `list(self._handles)`, 0=primário) → key e guarda. `None`/fora de
  faixa → `None` (todos). Devolve o índice efetivo (ou None). Sob `_io_lock`.
- `get_output_target_index(self) -> int | None`: mapeia a key guardada → posição
  atual (`list(self._handles).index(key)`); None se "todos" ou se o alvo sumiu.
- `describe_controllers()`: adicionar `"index": idx` em cada item (enumerate).
- NÃO mexer no `_desired` (limitação MVP documentada: o re-apply de perfil no
  hotplug e a troca de perfil seguem globais; a config por-controle é "ao vivo".
  Persistência por-controle entre reconexões fica para uma fase futura — anote no
  CHANGELOG/known).

### 2. IPC
- `daemon/ipc_server.py`: registrar `"controller.target.set": self._handle_controller_target_set`.
- `daemon/ipc_handlers.py`: `_handle_controller_target_set(params)` — valida
  `index` (int ou null), chama `self.controller.set_output_target(index)` via
  getattr (tolerar backend sem o método), devolve `{status, target_index}`.
- No `_handle_daemon_state_full`, adicionar `result["output_target_index"]` lendo
  `getattr(self.controller, "get_output_target_index", None)` (coerção defensiva
  a int/None igual ao bloco `coop` — o daemon pode ser MagicMock em teste).

### 3. GUI (banner)
- Um `Gtk.ComboBoxText` (ou dropdown) no banner/cabeçalho (perto do
  `header_connection`) listando "Todos" + cada controle ("Controle 1 — BT",
  "Controle 2 — USB", do bloco `controllers`/índice). Default selecionado =
  reflete `output_target_index` do state_full (None → "Todos").
- On-change → `_run_call("controller.target.set", {"index": <idx ou None>})`.
- Atualizar a lista no tick de estado (mesma cadência do header), preservando a
  seleção atual (por índice). Aparece só quando há 2+ controles (com 1, esconder
  ou mostrar desabilitado). Reusar o padrão de async/`call_async` da aba Status.
- Adicionar o widget no `gui/main.glade` (id ex.: `controller_target_combo`) OU
  criá-lo em runtime e empacotar no header (preferir runtime se o glade for
  arriscado de editar — ver como `_init_stick_previews` insere widgets em slots).

### 4. Applet COSMIC (Rust)
- `ipc.rs`: adicionar `output_target_index: Option<i64>` (serde default) ao
  `DaemonState`.
- `app.rs`: no popover, quando houver 2+ controles, um seletor (lista/botões) que
  envia `controller.target.set` via o mesmo caminho IPC dos outros comandos
  (ver como o mic/gamepad mandam comandos). Se for muito custoso, no MÍNIMO
  exibir qual é o alvo atual ("Aplicando em: Controle 2") — mas o seletor é o
  objetivo. `cargo check` deve passar sem warnings.

### 5. CLI (espelhar `cmd_coop.py`)
- `cli/cmd_controller.py` (novo) registrado em `cli/app.py`:
  `hefesto-dualsense4unix controller target <n|all>` e `controller list`
  (lista os controles do bloco `controllers` com índice/transporte/alvo).

### 6. Testes
- Backend: `tests/unit/test_backend_output_target.py` — `set_output_target`/
  `get_output_target_index` (índicekey, alvo sumido → None), e `_for_each`
  mirando só o alvo vs broadcast (usar stub de handles; ver
  `tests/unit/test_backend_multi_controller.py` para o padrão de stub do
  `_enumerate_device_keys`/handles).
- IPC: cobrir `controller.target.set` + `output_target_index` no state_full
  (ver `tests/unit/test_ipc_*`).
- GUI/CLI: testes de lógica pura onde der (ver `tests/unit/test_multi_controller_ui.py`).

## Gate (OBRIGATÓRIO antes de cada commit)
```
.venv/bin/ruff check src/hefesto_dualsense4unix tests
.venv/bin/python -m mypy src/hefesto_dualsense4unix
.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q
python3 scripts/validar-acentuacao.py --all        # 0 violações nas linhas tocadas
bash scripts/check_anonymity.sh                     # rodar APÓS git add
cd packaging/cosmic-applet && cargo check           # se mexer no applet
```

## Commit / push
- Branch atual: `feat/dsx-definitive-fix-usb-hdmi`. Após o gate verde:
  `git add -A` → commit → `git branch -f main HEAD` → `git push origin main`.
- Remote do fork: **`origin` = [REDACTED]/hefesto-dualsense4unix** (NUNCA
  upstream). Em `gh`, sempre `-R [REDACTED]/hefesto-dualsense4unix`.

## Restrições (inegociáveis)
- **Anonimato**: zero atribuição a IA em código/comentários/mensagens de commit
  (`check_anonymity.sh` + workflow `anonymity-check.yml`). Sem "feito por"/trailers.
- **Acentuação PT-BR estrita** nas linhas novas (`validar-acentuacao.py --all`);
  nunca trocar acento por ASCII. Há dívida pré-existente — manter limpas só as
  linhas tocadas.
- Comentários/docstrings em PT-BR, no estilo do arquivo (densidade, IDs de
  feature/bug como `FEAT-DSX-CONTROLLER-SELECTOR-01`).
- Não quebrar o caso single-controle (default = broadcast, idêntico a hoje).

## Aceitação
1. Com 2 controles: selecionar "Controle 2" e setar player-LED 2 → SÓ o controle
   2 muda (resolve o "ambos P1"); "Todos" volta ao broadcast.
2. `daemon.state_full` expõe `output_target_index`; CLI `controller target`/`list`
   funcionam; GUI e applet mostram o seletor com 2+ controles.
3. Gate 100% verde (ruff/mypy/pytest/acentuação/anonimato + `cargo check`).
4. Commitado no main e pushado no fork. CHANGELOG ([Unreleased] → Added) com a
   feature e a limitação conhecida (config por-controle é ao vivo; perfil/hotplug
   seguem globais nesta fase).
