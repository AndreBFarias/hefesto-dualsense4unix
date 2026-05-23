# BUG-DAEMON-EVDEV-HOTPLUG-CACHE-01 — Input errado (sticks ~253) quando o controle conecta após o boot

**Tipo:** fix (daemon/input).
**Wave:** V3.8.1 — hotfix de input (pós-release v3.8.0).
**Estimativa:** S — re-procura do evdev no `connect()` + testes.
**Dependências:** nenhuma.
**Status:** DONE (fix + testes; smoke hotplug real validado na máquina → daemon sobe offline, plugar dá `with_evdev` + sticks 128 sem reiniciar).

---

## Contexto

A mantenedora relatou "drift anormal" no DualSense via USB: com o controle
parado, o input se comportava como se os sticks estivessem encostados. Medido
via `daemon.state_full` (IPC) com o controle em repouso: **LX=253 LY=247 RX=254
RY=254** (constantes), quando o centro é ~128. Não era drift de hardware.

## Diagnóstico (causa-raiz)

`EvdevReader.__init__` (`core/evdev_reader.py`) chama `find_dualsense_evdev()`
**uma única vez**, na construção. O `PyDualSenseController` constrói o
`EvdevReader()` no próprio `__init__`, que roda no **boot do daemon**.

Quando o daemon sobe **offline** (PC ligado sem o controle plugado — o caso
comum: o systemd `--user` inicia o daemon no login, o controle é plugado
depois), `find_dualsense_evdev()` retorna `None` e `_device_path` nasce `None`.
Ao conectar o controle, `connect()` (`core/backend_pydualsense.py`) checava
`if self._evdev.is_available()` — `False` desde o boot — e caía no ramo
`controller_connected_without_evdev` (HID-raw cru), **sem nunca re-procurar o
evdev**. O fallback HID-raw lê os bytes dos sticks errado (→ ~253), porque o
kernel `hid_playstation` capturou o evdev e o pydualsense não recebe os reports.

Confirmação empírica: reiniciar o daemon **com o controle já conectado** faz o
`__init__` achar o evdev → `controller_connected_with_evdev` → sticks 128.

## Decisão / Entrega

Adicionar `EvdevReader.refresh_device()` (re-procura o evdev quando
`_device_path` é `None`) e chamá-lo em `PyDualSenseController.connect()`, a cada
(re)conexão, antes do gate `is_available()`. Fecha a janela do hotplug
pós-boot-offline sem custo no caminho feliz (não re-enumera se já há path).

## Critérios de aceite

- [x] `ruff check` + `mypy --strict` limpos.
- [x] `pytest tests/unit` verde (1421 passed; +3 testes: refresh relocaliza, refresh no-op, connect reativa evdev no hotplug).
- [x] Máquina: reiniciar o daemon com o controle conectado → `with_evdev` + sticks 128.
- [x] Smoke hotplug real: daemon sobe offline (sem controle), plugar → `with_evdev` (path migrou event2→event3, re-enumerado) + sticks ~128 sem reiniciar. Validado na máquina 2026-05-22.

## Arquivos tocados

- `src/hefesto_dualsense4unix/core/evdev_reader.py` — `refresh_device()` no `_EvdevReconnectLoop`.
- `src/hefesto_dualsense4unix/core/backend_pydualsense.py` — `connect()` chama `refresh_device()`.
- `tests/unit/test_evdev_reader.py` — 2 testes do refresh (relocaliza / no-op).
- `tests/unit/test_backend_no_device_resilient.py` — teste de hotplug pós-boot-offline.

## Notas para o executor

O loop interno `_run` já re-procura o device com backoff em caso de `OSError`
(perda em runtime); o bug era exclusivamente o **cache inicial** nunca
reavaliado, porque o thread jamais iniciava (gate `is_available()` em
`start()`). `refresh_device()` só re-enumera quando `_device_path is None`,
então o caminho feliz (controle presente no boot) não paga o custo (~60ms) de
enumerar `/dev/input`.

## Proof-of-work runtime

- Antes: `daemon.state_full` → LX=253 LY=247 RX=254 RY=254 (repouso); log `controller_connected_without_evdev`.
- Depois (restart com controle): LX=128 LY=128 RX=128 RY=128; log `controller_connected_with_evdev` + `evdev_started path=/dev/input/event2`.

## Fora de escopo

- Reescrever o `start()` para iniciar o thread sem device (cobriria uma race
  teórica entre a enumeração USB e a criação do evdev, mas mudaria o
  `TouchpadReader` também — risco desproporcional; na prática o evdev já existe
  quando `pydualsense.init()` tem sucesso).
