# Sprint (proposta): suporte a MÚLTIPLOS DualSense simultâneos

**Origem**: pergunta da Vitória (2026-06-27) — *"se eu conectar outro controle de PS5
ele vai ficar com os gatilhos adaptativos também?"*

**Resposta curta**: **hoje não.** O daemon gerencia **um** DualSense por instância,
em todas as camadas. Um segundo controle conectado **não** recebe gatilhos
adaptativos / perfis. Este documento levanta o escopo para mudar isso.

> Nota: o backlog já previa isso — `docs/process/SPRINT_ORDER.md` lista
> *"Multi-controle simultâneo: HID + IPC multiplexado"* em "Backlog aberto sem
> sprint (V2.x+)". E o IPC já tem um método `controller.list` (hoje hardcoded
> com 1 item) — ou seja, a API foi desenhada antevendo N controles.

---

## STATUS: IMPLEMENTADO  (FEAT-DSX-MULTI-CONTROLLER-01) — 2026-06-27 madrugada

Implementado via workflow (design em paralelo → implementação coesa → verificação
adversarial). Escopo escolhido pela Vitória: **gatilhos adaptativos + lightbar +
rumble + perfil ativo aplicados a TODO DualSense conectado, com hotplug; emulação
(mouse/gamepad virtual/teclado) só no controle PRIMÁRIO.**

**O que foi feito** (1555 testes verdes, ruff limpo, anonimato OK):
- `core/backend_pydualsense.py` (reescrito, núcleo): `self._ds` único → `self._handles:
  dict[serial→pydualsense]` + `_primary_key` + `_io_lock`. Como a `pydualsense` não é
  multi-device (abre por VID/PID e pega "o primeiro"; `# TODO` na própria lib), foi
  criada a subclasse `_PinnedPyDualSense` que sobrescreve o `__find_device` manglado e
  abre por `hidapi.Device(path=…)` — abertura determinística por device. `_ds` virou
  property de compat (= handle primário).
- `connect()` virou **tick de reconciliação de hotplug**: enumera, fecha removidos
  (sem vazar handle/thread), abre novos e **re-aplica o perfil ativo** no recém-chegado
  (`_DesiredOutput` cacheia triggers/lightbar/player-LEDs/mic-LED; rumble é transitório,
  fica de fora). Setters fazem **fan-out a todos** via `_for_each` (1 handle morto não
  derruba os outros).
- INPUT/EMULAÇÃO intactos: `read_state`/`get_battery`/`transport`/evdev leem só o
  PRIMÁRIO (um leitor/grab — sem duplicação).
- `daemon/ipc_handlers.py`: `controller.list` agora lista os N controles reais.
- Testes novos: `tests/unit/test_backend_multi_controller.py` (fan-out, enumerate/dedupe,
  hotplug add/remove, promoção de primário, não-regressão single).

**BUG P0 pego no review adversarial e JÁ CORRIGIDO**: `_enumerate_device_keys` chamava
`.decode()` no `serial_number`, mas o `hidapi` real retorna serial como **`str`** (vem
de `wchar_t*`); `path` é que é `bytes` (`char*`). Isso levantava `AttributeError` e
**impedia QUALQUER conexão — até com 1 controle** (regressão total). O teste mascarava
(fake usava `serial: bytes`). Corrigidos código (`key = serial if serial else
path.decode(...)`) e o fake do teste. Confirmado pela fonte do hidapi.py (l.167/173).

**Limitações conhecidas (médias, NÃO corrigidas — TODO pós-validação):**
1. **Modo-jogo + gamepad virtual = "tijolo"**: acionar a supressão (PS+Options) com o
   gamepad virtual ligado congela o pad virtual MAS mantém o grab do controle físico →
   o jogo não vê nem o virtual nem o cru. Footgun raro (modo-jogo via PS longpress está
   desligado por default; só via combo deliberado). Correção sugerida: não gatear o
   gamepad por `_emulation_suppressed`, ou soltar grab+flush ao suprimir.
2. **Primário do input vs output descoordenado**: com 2+ controles, QUAL controle físico
   dirige o cursor/gamepad (evdev "primeiro") pode não ser o mesmo reportado como
   primário no HID (`hidapi.enumerate` "primeiro"). Não é crash; é arbitrário. Aceitável
   no MVP "emulação no primário"; alinhar inputoutput é refinamento futuro.
- Menores tolerados: `_desired` é last-write-wins (não snapshot); player-LEDs iguais em
  todos (fan-out); leituras de `_handles` sem lock (seguro em CPython, padrão pré-existente).

**Pendente desta feature**: validação ao vivo com 2 controles físicos (precisa da Vitória).
Não bloqueia o release do escopo anterior, mas como é grande, sobe a v3.8.4 → **v3.9.0**.

---

## 1. Veredito: single-controller em todas as camadas (levantamento original)

Confirmado por varredura do código (referências arquivo:linha abaixo). O design é
fundamentalmente de **um controle**; não há `dict[path]`/lista em lugar nenhum do
caminho quente.

## 2. Levantamento técnico (contexto preservado do agente Explore)

### Detecção / conexão — `core/evdev_reader.py`
- `find_dualsense_evdev()` (linhas **62-93**): retorna `Path | None`; o loop
  **encerra no primeiro match** (`return Path(path)`) — não coleta vários.
- `find_dualsense_touchpad_evdev()` (**387-417**): mesma limitação.
- `EvdevReader._device_path` (**104**): guarda **um** `Path | None`.
- `EvdevReader._active_dev` (**109**): mantém **um** `InputDevice` aberto.
- `EVIOCGRAB` / `set_grab()` (**268-285**): grab aplicado ao `self._active_dev`
  (device único).
- Hotplug (`refresh_device()`, **127-138**): hotplug-safe **só** para o device em
  `self._device_path` (BUG-DAEMON-EVDEV-HOTPLUG-CACHE-01).

### Escrita HID / gatilhos adaptativos — `core/backend_pydualsense.py`
- `self._ds: pydualsense | None` (**48**): **um** objeto HID por instância.
- `connect()` (**60-143**): inicializa **um** `pydualsense()`.
- `set_trigger()` / `set_led()` / `set_rumble()`: todas escrevem em `self._ds`.
- `profiles/manager.py` `apply()` (**79-87**): aplica trigger+LED em **um**
  `self.controller`.

### Subsystems / lifecycle — `daemon/lifecycle.py`
- `controller: IController` (**128**): **um** campo.
- Emulação singleton por daemon (**139-144**): `_mouse_device`, `_keyboard_device`,
  `_gamepad_device` (mutex com mouse), `_hotkey_manager` — todos únicos.
- `DaemonContext` (`daemon/context.py`): **um** `controller` injetado em todos os
  subsystems.
- `StateStore` (`daemon/state_store.py`): `_controller_state` (**53**) e
  `_active_profile` (**54**) são únicos (não `dict[path]`).
- Poll loop (**677-853**): `is_connected()` / `read_state()` / dispatch — tudo
  sobre **um** controller por tick.

### IPC / status — `daemon/ipc_handlers.py`
- `_handle_daemon_status()` (**195-210**): escalares (`battery_pct`, `transport`,
  `active_profile`), não arrays.
- `_handle_daemon_state_full()` (**222-319**): estado consolidado num objeto.
- `_handle_controller_list()` (**321-331**): **array hardcoded com 1 item** (o
  gancho para N já existe, falta popular).

### Singletons que bloqueiam N (mapa)
| Singleton | Arquivo | Linha |
|---|---|---|
| `Daemon.controller` | `lifecycle.py` | 128 |
| `Daemon._mouse_device` | `lifecycle.py` | 139 |
| `Daemon._gamepad_device` | `lifecycle.py` | 143 |
| `StateStore._controller_state` | `state_store.py` | 53 |
| `StateStore._active_profile` | `state_store.py` | 54 |
| `EvdevReader._device_path` | `evdev_reader.py` | 104 |
| `EvdevReader._grab` / `_active_dev` | `evdev_reader.py` | 268 / 109 |
| `PyDualSenseController._ds` | `backend_pydualsense.py` | 48 |

## 3. Esforço por camada (estimativa grosseira)

| Camada | Mudança | Tamanho |
|---|---|---|
| Detecção (`evdev_reader.py`) | `find_*` → `list[Path]`; readers → `{path: reader}` | Médio |
| HID-write (`backend_pydualsense.py`) | `self._ds` → `{path: pydualsense}`; fan-out | Médio |
| Subsystems (`lifecycle.py`, `mouse.py`…) | devices por-path; dispatch fan-out | **Grande** |
| IPC (`ipc_handlers.py`) | `controller.list` real; versionar protocolo | Médio |
| Persistência (`state_store.py`, `manager.py`) | estado/perfil por-device | **Grande** |
| GUI/CLI (`app/`, `cli/`) | seletor de controle; painel por-device | **Grande** |

**Total estimado: ~2 meses para um MVP de N controles.**

## 4. Riscos / armadilhas

- **A-1** dois readers disputando `EVIOCGRAB` no mesmo device → input perdido.
- **A-2** dois writers em hidraw simultâneos → frames HID corrompidos
  (triggers/rumble dessincronizados). Precisa serializar escrita por device.
- **A-3** gamepad virtual + físico grabado: quem libera o quê? FEAT-DSX-GAMEPAD-
  FLAVOR-01 assume device exclusivo.
- **A-4** perfis por device: "Jogo A" no controle 1, "Jogo B" no 2 → qual perfil no
  autoswitch?
- **A-5** clientes CLI/GUI legados esperam `controllers[0]` → quebra de protocolo
  sem migração suave.
- **A-6** rumble simultâneo em 2 controles → pico de corrente no hub USB (eco do
  próprio storm de enumeração que já conhecemos — ver
  `storm_dualsense_e_config_nossa_nao_hardware`).

## 5. Caminhos possíveis (decisão da Vitória)

- **Opção A — múltiplas instâncias do daemon** (rápido, ~200 LOC de orquestração):
  uma instância por controle (`--device-id=…`), sandbox por PID/socket. Resolve o
  caso "2 controles com gatilhos" sem reescrever o core. Risco baixo. **Recomendada
  se a necessidade for imediata.**
- **Opção B — dict-ificação mínima (MVP técnico, ~500 LOC)**: `find_* → list`,
  `EvdevReaderPool{path→reader}`, poll loop em for-loop, `controller.list` real.
  Para aqui (sem multi-perfil / multi-mouse). Triggers/rumble ainda exigem
  arbitragem de single-writer.
- **Opção C — N-controle pleno (~2 meses)**: tudo por-device (estado, perfil,
  emulação, GUI com seletor). É o "feito de verdade", mas é a sprint grande.

## 6. Próximos passos

1. Vitória escolhe A / B / C (ou adia — é V2.x+ no backlog).
2. Se A: especificar o orquestrador (systemd template `@.service` por device-id).
3. Se B/C: abrir as tasks por camada seguindo a tabela da §3.

*(Não faz parte da v3.8.4 — a release atual segue como o último passo do escopo
já pronto: B4 + gamepad-flavor + GUI + storm-watch + applet.)*
