# Estudo: IMU/touchpad REAIS no vpad (FUT-02 / DEDUP-02)

> Materializado 2026-07-18 (noite). Onda de pesquisa READ-ONLY sobre a árvore
> (auditoria rodando em paralelo — nenhum arquivo de código foi tocado). Fonte
> das ondas: `docs/process/sprints/2026-07-18-sprint-futuro-broker-imu-rdr2.md`
> (FUT-02). Este doc é a SPEC de implementação: offsets exatos, arquitetura
> escolhida com justificativa, hook points `arquivo:linha` e plano de teste.

## TL;DR (a decisão)

Hoje o vpad uhid Edge (`054c:0df2`) já expõe os nós **Motion Sensors** e
**Touchpad** (o `hid_playstation` DO PRÓPRIO vpad os cria) — mas eles emitem
zero: o report de input 0x01 que o daemon monta preenche só sticks/botões/d-pad
e deixa os bytes de IMU zerados e os dois dedos marcados como "sem toque"
(`uhid_gamepad.py:_encode_body`, offsets 15–39). É o gate DEDUP-02.

**Arquitetura escolhida: ESPELHO DE REPORT PARCIAL (raw hidraw → vpad), só para
a janela IMU+touch.** Uma thread nova (`PhysicalReportReader`) abre o hidraw do
controle FÍSICO em **somente-leitura**, extrai VERBATIM os bytes 15–39 do report
cru (gyro/accel/timestamp + 2 pontos de toque) e os injeta no report 0x01 do
vpad via um método novo `forward_motion(window)`. Sticks/botões/d-pad continuam
vindo do caminho evdev endurecido (grab/hotplug/watchdog/retarget) — sem mexer
nele. Calibração: carimbar o feature **0x05 do físico** no blueprint do vpad
(como já se faz com o MAC no 0x09), com fallback fail-safe para o 0x05 canônico.

Por que espelho e não evdev: (1) o nó evdev Motion do físico entrega valores JÁ
CALIBRADOS — para alimentar o report 0x01 (que carrega int16 CRU) seria preciso
DES-calibrar e depois o driver do vpad re-calibra: duas transformações, erro
acumulado; (2) o evdev **não tem o `sensor_timestamp`**, e o SDL usa esse campo
para o `dt` de integração do gyro (gyro aiming); (3) o espelho copia bytes, sem
matemática que possa errar; timestamp e id-de-dedo vêm de graça. Por que NÃO o
espelho TOTAL (substituir o evdev por hidraw também nos sticks): risco alto —
descartaria anos de endurecimento do `EvdevReader` (EVIOCGRAB, filtro de device
virtual, watchdog de nó obsoleto, retarget por MAC, decode de d-pad HAT). FUT-02
é IMU/touch, não reescrita do caminho de input.

Custo medido/estimado: ~250 leituras + ~250 escritas de 64 B por controle por
segundo (USB) = <1% CPU/controle; nenhum tráfego de rádio novo (leitura só copia
do buffer do kernel). Latência de IMU CAI (hoje o poll loop é **60 Hz**; o reader
entrega no ritmo nativo do físico, ~250 Hz).

---

## 1. Offsets EXATOS do report de input do DualSense

### Fonte

- **Kernel** `drivers/hid/hid-playstation.c` — `struct dualsense_input_report` e
  `dualsense_parse_report()`. Módulo presente na máquina:
  `/lib/modules/7.0.11-76070011-generic/kernel/drivers/hid/hid-playstation.ko`
  (`srcversion 30AB15023997E11620142CB`). Constantes:
  `DS_INPUT_REPORT_USB = 0x01`, `DS_INPUT_REPORT_USB_SIZE = 64`,
  `DS_INPUT_REPORT_BT = 0x31`, `DS_INPUT_REPORT_BT_SIZE = 78`,
  `DS_GYRO_RES_PER_DEG_S = 1024`, `DS_ACC_RES_PER_G = 8192`.
- **SDL** `SDL_hidapi_ps5.c` — `PS5StatePacket_t` (mesmo layout). O SDL abre o
  hidraw do vpad, lê o report CRU e o feature 0x05, e **calibra por conta
  própria**; usa `rgucSensorTimestamp` como base de tempo do gyro.
- **Evidência viva** (2026-07-18, `evdev.list_devices`): o físico `054c:0ce6`
  expõe `event9` "…Motion Sensors" (ABS_X/Y/Z accel `res=8192`; ABS_RX/RY/RZ
  gyro `res=1024`; PROP `ACCELEROMETER`) e `event10` "…Touchpad"
  (ABS_MT_SLOT 0..1, ABS_MT_POSITION_X 0..1919, Y 0..1079, ABS_MT_TRACKING_ID).
  O **vpad** `054c:0df2` já tem `event27`/`event28` com ranges IDÊNTICOS — prova
  de que o `hid_playstation` do vpad monta os mesmos nós e aplicará a calibração.
- **Cross-check no nosso código**: `uhid_gamepad.py` já documenta (medido em
  report cru) `reserved2` em 31, pontos de toque em 32/36, `status` em 52, `seq`
  em 6, e `_INPUT_PAYLOAD_SIZE = 63`. Este estudo só ADICIONA a janela IMU+touch.

### Layout do payload (report 0x01 USB, após o report id — 63 bytes)

| offset | campo | estado no vpad hoje |
|---|---|---|
| 0 | x  (LX) | preenchido (`_axes`) |
| 1 | y  (LY) | preenchido |
| 2 | rx (RX) | preenchido |
| 3 | ry (RY) | preenchido |
| 4 | z  (L2 analógico) | preenchido |
| 5 | rz (R2 analógico) | preenchido |
| 6 | seq_number | preenchido (`_SEQ_OFFSET`) |
| 7 | buttons[0] (d-pad HAT + □×) | preenchido |
| 8 | buttons[1] (L1/R1/L2/R2/create/options/L3/R3) | preenchido |
| 9 | buttons[2] (PS / mic / **touchpad click** 0x02) | preenchido |
| 10 | buttons[3] (contador de toque / plug) | 0 (ok deixar 0) |
| 11–14 | reserved[4] | 0 |
| **15–16** | **gyro[0] = X (pitch), le16** | **ZERADO ← preencher** |
| **17–18** | **gyro[1] = Y (yaw), le16** | **ZERADO ← preencher** |
| **19–20** | **gyro[2] = Z (roll), le16** | **ZERADO ← preencher** |
| **21–22** | **accel[0] = X, le16** | **ZERADO ← preencher** |
| **23–24** | **accel[1] = Y, le16** | **ZERADO ← preencher** |
| **25–26** | **accel[2] = Z, le16** | **ZERADO ← preencher** |
| **27–30** | **sensor_timestamp, le32 (unidades de 0,333 µs)** | **ZERADO ← preencher (SDL usa p/ dt)** |
| 31 | reserved2 | 0 |
| **32–35** | **points[0] = dedo 0 (4 B)** | inativo (0x80 em 32) ← preencher |
| **36–39** | **points[1] = dedo 1 (4 B)** | inativo (0x80 em 36) ← preencher |
| 40–51 | reserved3[12] | 0 |
| 52 | status (bateria/carga) | preenchido (`forward_battery`) |
| 53–62 | reserved4[10] | 0 |

Mapeamento eixo→ABS (do `dualsense_parse_report`, relevante só se um dia se optar
pelo caminho evdev): gyro[0]→ABS_RX, gyro[1]→ABS_RY, gyro[2]→ABS_RZ;
accel[0]→ABS_X, accel[1]→ABS_Y, accel[2]→ABS_Z.

### `struct dualsense_touch_point` (4 bytes/dedo)

```
byte +0  contact : bit7 = !active (0x80 = SEM toque) ; bits0..6 = touch id (incrementa por contato novo)
byte +1  x_lo    : X[7:0]
byte +2  bits0..3 = x_hi = X[11:8]  ;  bits4..7 = y_lo = Y[3:0]
byte +3  y_hi    : Y[11:4]
```

Decode (o que o driver do vpad fará com nossos bytes):
`X = ((byte2 & 0x0F) << 8) | byte1` (0..1919);
`Y = (byte3 << 4) | (byte2 >> 4)` (0..1079);
`active = not (byte0 & 0x80)`.

Encode a partir de (id, active, X, Y):
`byte0 = (0x00 if active else 0x80) | (id & 0x7F)`;
`byte1 = X & 0xFF`;
`byte2 = ((X >> 8) & 0x0F) | ((Y & 0x0F) << 4)`;
`byte3 = (Y >> 4) & 0xFF`.

> O `_TOUCH_INACTIVE = 0x80` que o vpad já carimba nos offsets 32/36 (contato
> INVERTIDO) permanece o estado neutro correto quando não há dedo.

### Report 0x31 (Bluetooth) — só importa se o FÍSICO for BT

O físico BT emite report **0x31** (78 B). O `struct` de input começa em
`data[2]` (0x31 + 1 byte de header), e os **4 últimos bytes são CRC32**. Logo,
para o READER, quando o físico for BT: `struct_base = 2` e os offsets acima
somam +2 no buffer cru; ignorar os 4 bytes finais. **O VPAD nunca muda** — ele é
sempre `BUS_USB` emitindo 0x01 (`uhid_blueprint.py`: descriptor sem `85 31`); a
janela extraída do 0x31 do físico é copiada para as MESMAS posições 15–39 do
report 0x01 do vpad. Detecção por `report[0]`: 0x01→base 1; 0x31→base 2.

---

## 2. Como o vpad injeta — confirmação de que "basta preencher o report"

O vpad monta o report inteiro em `UhidDualSense._encode_body()`
(`uhid_gamepad.py:794`) e o entrega por `send_report()` → `UHID_INPUT2`. O driver
`hid_playstation` do vpad faz o resto: cria os nós Motion/Touchpad e (para o
kernel-evdev) aplica a calibração 0x05; o SDL lê o report cru + 0x05 e calibra
sozinho. **Ambos os consumidores leem os MESMOS bytes 15–39.** Confirmado ao
vivo pela existência de `event27`/`event28` do vpad com ranges idênticos aos do
físico.

Portanto o trabalho é exatamente: **preencher `body[15:40]`** com a janela do
físico (IMU 15–30, reserved2 31, dois pontos 32–39) — mais garantir que o vpad
EMITA no ritmo do físico (senão o gyro fica a 60 Hz). Nada de novo no lado do
kernel; nenhum feature/descriptor novo (o 0x05 já é pedido no probe e já está no
blueprint — só passa a ser por-controle).

---

## 3. FONTE dos dados — evdev vs hidraw cru (a decisão de arquitetura)

### O que o evdev JÁ dá (e por que não basta)

- **Motion**: `event9` do físico dá gyro/accel via ABS_RX/RY/RZ e ABS_X/Y/Z,
  mas **CALIBRADOS** (o driver já aplicou o 0x05 do físico). O `EvdevReader`
  atual NEM lê esse nó (só o gamepad principal, caps BTN_GAMEPAD). Precisaria de
  um `MotionReader` novo.
- **Touchpad**: `TouchpadReader` já lê `event10`, mas só extrai **1 dedo**
  (movimento p/ cursor + região do clique) e joga fora o multitouch de 2 slots e
  as coordenadas cruas. Precisaria reescrever para ABS_MT_SLOT/TRACKING_ID/
  POSITION_X/Y com 2 dedos.
- **Faltando de vez**: o `sensor_timestamp` (o evdev não expõe) — e o SDL usa ele
  para o `dt` do gyro.

### As três arquiteturas avaliadas

**ARCH-1 — Espelho de report PARCIAL (ESCOLHIDA).** Thread nova lê o hidraw cru
do físico (O_RDONLY), extrai bytes 15–39 VERBATIM, injeta em `body[15:40]` do
vpad. Sticks/botões continuam via evdev.
- Prós: cópia byte a byte (zero matemática); timestamp e id-de-dedo preservados
  → SDL feliz; agnóstico de calibração no caminho de dados (o 0x05 resolve);
  não toca no `EvdevReader` endurecido; latência de IMU no ritmo nativo.
- Contras: um 2º fd (read-only) no hidraw do físico; precisa tratar 0x01 vs 0x31;
  calibração exata exige carimbar o 0x05 do físico (item 4).

**ARCH-2 — evdev Motion + transformada inversa-canônica (REJEITADA).** Ler o nó
Motion calibrado e aplicar `raw = canon_uncalibrate(valor_evdev)` usando as
constantes conhecidas de `CANONICAL_FEATURE_0X05`; o driver do vpad re-calibra
canônico e o resultado bate para QUALQUER unidade sem ler 0x05 do físico.
- Prós: fica no caminho evdev; calibração exata sem feature read.
- Contras (por que rejeitada): replica a matemática do
  `dualsense_get_calibration_data` E a inverte (frágil a mudança de kernel);
  **perde o `sensor_timestamp`** (teria de sintetizar um contador — aproximação
  que o SDL sente no `dt` do gyro); reescreve o `TouchpadReader` para MT;
  3 threads evdev. Mais código e mais risco que a ARCH-1 para um resultado
  igual ou pior.

**ARCH-3 — Espelho TOTAL (FUTURO, não agora).** Ler TUDO do hidraw cru
(sticks+botões+IMU+touch) e repassar o report inteiro, aposentando o
`EvdevReader` do caminho primário. É a forma "limpa" que o FUT-02 imagina
("elimina 2 camadas de tradução"), mas descarta EVIOCGRAB, filtro de virtual,
watchdog de nó obsoleto, retarget por MAC e decode de HAT — mudança grande e
arriscada, fora do escopo de "IMU/touch". Fica registrada como evolução.

**Custo de CPU / rumble / latência (ARCH-1):**
- Leitura: `os.read(64)` acorda a cada report do físico (~250 Hz USB); slice +
  1 `os.write` de 64 B ao /dev/uhid. <1% CPU por controle.
- Rádio/USB: NENHUM tráfego novo — os reports já fluem para o kernel; o 2º fd só
  copia do buffer. (Ao contrário do report_thread da pydualsense, que **escreve**
  e por isso é throttlado; o reader não escreve no físico, então lê a rate
  cheia sem contenção — não reabre a "guerra de escritores", que é sobre
  WRITERS.)
- Rumble/REPLICA-03: intocados — direção e report diferentes (ver item 5).
- Latência: MELHORA. Hoje o gyro seria limitado a `poll_hz=60`. O reader entrega
  no ritmo nativo (~250 Hz), sub-ms de overhead.

---

## 4. Calibração (feature 0x05)

O `hid_playstation` do vpad calibra o Motion com **o 0x05 que o vpad responder no
probe** (hoje `CANONICAL_FEATURE_0X05`, congelado de UMA unidade — a branca USB
desta máquina). O SDL, idem, lê o 0x05 do vpad e calibra. Logo a regra é a mesma
para os dois consumidores: **para o gyro não drivar/escalar errado, o 0x05 do
vpad tem de bater com a unidade que alimenta os dados.**

- **P1 (branca USB)**: o 0x05 canônico veio DESTA unidade → passthrough cru já é
  exato. (É a nota já registrada em `uhid_blueprint.py:43-46`: "Se um dia houver
  passthrough de gyro/touchpad, a calibração por unidade volta a importar.")
- **Outras unidades (ex.: P2 roxa BT)**: o canônico erra o BIAS (→ drift lento
  na mira) e a sensibilidade. Cura: **carimbar o 0x05 do físico no blueprint do
  vpad**, exatamente como o `start()` já carimba o MAC no 0x09
  (`_features_com_mac_proprio`, `uhid_gamepad.py:667`).
- **Como ler o 0x05 do físico, fail-safe**: `hidapi.Device` já expõe
  `get_feature_report` (confirmado no venv) — o handle da pydualsense do físico
  está ABERTO e o report_thread prova que o I/O funciona; um
  `get_feature_report(0x05, 41)` é barato e serializado pela hidapi. Alternativa
  já provada no repo: `capture_dualsense_blueprint` abre o hidraw O_RDWR e faz
  `HIDIOCGFEATURE` (`uhid_gamepad.py:344,415`). **Fallback**: se a leitura
  falhar (BT ocioso → EIO, o modo de falha documentado), usa o 0x05 canônico —
  o vpad sobe do mesmo jeito (invariante "vpad sempre nasce" preservado); o gyro
  funciona, só pode ter leve drift até uma sessão USB.
- O `hid_playstation` do vpad NÃO auto-calibra: ele lê o 0x05 no probe e usa como
  divisor/escala. Não há calibração online — por isso o 0x05 correto importa.

Decisão: **carimbar 0x05 do físico quando legível; senão canônico.** Barato,
correto para todas as unidades, sem regressão.

---

## 5. Interação com o que acabou de ser feito (REPLICA-03) — sem conflito

REPLICA-03 é o caminho **INVERSO** deste:
- **REPLICA-03 (OUTPUT)**: jogo → vpad (evento `UHID_OUTPUT`, report **0x02**)
  → `pump_ff`/sinks → físico. Drenado no poll loop.
- **Este (INPUT)**: físico → `PhysicalReportReader` → vpad (`UHID_INPUT2`, report
  **0x01**) → kernel/SDL → jogo.

Direções opostas, reports diferentes (0x02 vs 0x01). Pontos de contato a
respeitar:

1. **hidraw do físico**: REPLICA-03/pydualsense ESCREVEM output no físico; o
   reader LÊ. Leitura e escrita em hidraw são independentes e o reader usa um fd
   próprio O_RDONLY — não disputa nada (a "guerra" é de escritores).
2. **fd do /dev/uhid do vpad**: `pump_ff` faz `os.read` (drena output); o reader,
   via `forward_motion`→`send_report`, faz `os.write`. Direções independentes.
   `send_report` já serializa escrita e o fechamento do fd sob `self._lock`
   (`uhid_gamepad.py:891,902`) — o reader HERDA essa proteção. Ordem em `stop()`:
   o reader precisa ser parado ANTES/junto do `stop()` do vpad (o daemon já tem
   o padrão: parar o subsistema antes de destruir o device).
3. **Sessão/graça do REPLICA-03** (`_game_open`, `_GAME_REPLICA_GRACE_S`): é do
   OUTPUT. O INPUT pode transmitir sempre que o vpad estiver `is_bound`. Opção de
   economia (recomendada): só transmitir IMU quando `_game_open` (um consumidor
   abriu o hidraw) — senão o SDL nem está lendo; poupa as 250 escritas/s ociosas.
4. **Nenhuma disputa de bytes**: output mexe em 0x02 (rumble/trigger/lightbar);
   input mexe em 0x01 (IMU/touch). Estados separados.

---

## 6. Hook points (arquivo:linha)

**Módulo novo** `core/physical_report_reader.py` — classe `PhysicalReportReader`,
espelhando o padrão de `_EvdevReconnectLoop` (`evdev_reader.py:314`) mas sobre
hidraw:
- abre `hidraw_path` do físico O_RDONLY|O_NONBLOCK numa thread com reconnect/
  backoff e o mesmo `request_reopen`/`retarget` por MAC;
- por report: detecta `report[0]` (0x01→base 1 / 0x31→base 2, tira CRC), extrai
  `raw[base+15 : base+40]` (janela de 25 B) e chama `vpad.forward_motion(window)`;
- `set_streaming` liga/desliga o gate no vpad ao abrir/fechar o device.

**`integrations/uhid_gamepad.py`**
- `_encode_body` (`:794`): escrever `body[15:40] = self._motion_window` quando
  presente (default = neutro: zeros de IMU + `_TOUCH_INACTIVE` em 32/36, exato
  como hoje). Novas constantes de offset perto de `:199-282`
  (`_IMU_OFFSET=15`, `_MOTION_WINDOW=slice(15,40)`).
- `forward_motion(self, window: bytes)` novo, irmão de `forward_analog`
  (`:744`): valida `len==25`, guarda em `self._motion_window` sob `_lock`,
  e EMITE (o reader é o relógio). Quando `self._motion_streaming` estiver ligado,
  `forward_analog`/`forward_buttons` só atualizam cache e NÃO emitem (evita
  emissão dupla e mantém o ritmo do reader) — `_emit_if_changed` (`:776`) ganha
  o gate.
- `set_motion_streaming(self, on: bool)` novo (o reader chama no connect/
  disconnect). Com `off`, volta ao comportamento atual (emite no delta do poll,
  IMU neutro).
- `_features_com_mac_proprio` (`:667`): além do MAC no 0x09, se
  `self.calibration_0x05` (campo novo, `bytes|None`) estiver setado e válido
  (41 B), substituir `features[0x05]` por ele.
- Novo campo no dataclass: `calibration_0x05: bytes | None = None`,
  `_motion_window: bytes | None = None`, `_motion_streaming: bool = False`.
  `stop()` (`:688`) zera os dois de motion.

**`integrations/virtual_pad.py`**
- `make_virtual_pad` (`:112`) e `_try_uhid` (`:175`): aceitar
  `calibration_0x05: bytes | None = None` e repassá-lo ao
  `UhidDualSense.for_flavor(..., calibration_0x05=...)` (`:206`). Blueprint segue
  `canonical_blueprint()`.

**`core/backend_pydualsense.py`**
- Reusar `hidraw_path(uniq)` (`:558`) para o reader achar o nó do físico.
- Método novo `read_calibration(uniq=None) -> bytes | None`: do handle primário
  (ou por uniq), `handle.device.get_feature_report(0x05, 41)` sob `_io_lock`,
  com `suppress(Exception)` → None. (BT ocioso pode falhar → fallback canônico.)

**`daemon/subsystems/gamepad.py`**
- `start_gamepad_emulation` (`:612`): passar
  `calibration_0x05=daemon.controller.read_calibration()` ao `make_virtual_pad`;
  após device uhid criado, criar/startar
  `PhysicalReportReader(hidraw=daemon.controller.hidraw_path(), vpad=device)` e
  guardar em `daemon._motion_reader`.
- `stop_gamepad_emulation` (`:664`): parar `daemon._motion_reader`.
- Na troca de primário (`backend_pydualsense._recompute_primary`, `:952`, que já
  faz `self._evdev.retarget(...)`): retargetar também o reader (novo hidraw).

**`daemon/subsystems/coop.py`** (FASE 2 — ver riscos)
- `_promote_player` (`:457`) e `forward_all` (`:784`): cada jogador teria seu
  `PhysicalReportReader` (hidraw do físico DAQUELE jogador). Precisa de
  hidraw-por-jogador (hoje o co-op resolve só o evdev por jogador). Fica para
  uma segunda leva depois do P1 provado.

---

## 7. Plano de teste

**Unit / hermético (sem hardware):**
1. `test_uhid_motion_encode`: dado um report cru sintético do físico, o vpad
   escreve `body[15:40]` VERBATIM; com `_motion_window=None`, `body` fica idêntico
   ao de hoje (IMU zero, 0x80 em 32/36) — anti-regressão.
2. `test_touch_point_roundtrip`: encode(id, active, X, Y) → decode bate; caso
   sem toque = `0x80` no byte de contato.
3. `test_report_base_detection`: 0x01→base 1; 0x31→base 2 e CRC de 4 B ignorado.
4. `test_motion_streaming_gate`: com `set_motion_streaming(True)`,
   `forward_analog` NÃO emite; `forward_motion` emite. Com `False`, comportamento
   de delta atual.
5. `test_calibration_stamp`: `calibration_0x05` de 41 B entra em `features[0x05]`;
   `None` ou tamanho errado → mantém o canônico (fallback).
6. `test_physical_report_reader` (fd falso alimentando reports): chama
   `vpad.forward_motion` com o slice certo; reconnect/backoff no EBADF.

**Ao vivo (gate humano DEDUP-02):** máquina da mantenedora, P1 branca USB.
1. `evtest` no `event27` ("Hefesto Virtual DualSense P1 Motion Sensors"): mover o
   controle FÍSICO move os eixos do vpad; parado, gyro fica ~0 (prova a
   calibração casada — sem drift).
2. `evtest` no `event28` (Touchpad do vpad): dois dedos no touchpad do físico
   aparecem como 2 slots MT no vpad, com X 0..1919 / Y 0..1079.
3. Jogo/tester com gyro (SDL): mira por giroscópio segue o controle; o
   `sensor_timestamp` faz o `dt` do SDL ficar suave (sem serrilhado de 60 Hz).
4. **Simultâneo com REPLICA-03**: enquanto o gyro transmite, confirmar que rumble,
   gatilhos adaptativos e lightbar do jogo continuam chegando ao físico (input e
   output convivem).
5. BT (P2 roxa): repetir; se o `read_calibration` falhar por BT ocioso, verificar
   fallback (gyro funciona, drift leve tolerável) e logar o motivo.
6. `top`/journal: CPU do daemon estável; sem storm/CRC novo no `dmesg`.
7. Flip do gate: DEDUP-02 sai de "nós existem, sem dados" para "gyro/touch reais".

---

## 8. Riscos e escopo em aberto

- **Escopo v1 = vpad do P1 (primário)**. Co-op multi-jogador precisa de
  hidraw-por-jogador (o co-op hoje resolve só evdev por jogador) — FASE 2.
- **Calibração por BT**: `read_calibration` pode dar EIO no físico BT ocioso →
  fallback canônico (drift leve). Aceito por design; mitigável lendo o 0x05
  numa sessão USB e cacheando por MAC (futuro).
- **Ritmo de emissão**: com IMU sempre variando, o vpad emite ~250 Hz. Validar
  que 4 vpads (co-op) a 250 Hz não pesam no /dev/uhid (a escrita já é enxuta —
  `send_report` não faz padding de 4 KB, `:896`). Se pesar, throttle por-vpad.
- **0x31 do físico**: confirmar ao vivo o offset exato do `struct` no 0x31
  (base 2 + CRC nos 4 últimos) com um report cru — o descriptor BT carrega
  `85 31` mas o header/CRC deve ser conferido byte a byte antes de fossilizar.
- **Ordem de teardown**: o `PhysicalReportReader` deve parar antes do `stop()`
  do vpad (fd do uhid); seguir o padrão dos outros subsistemas do daemon.
- **ARCH-3 (espelho total)** fica registrada como evolução: só vale a pena se um
  dia o caminho evdev virar dívida — não é pré-requisito de FUT-02.

---

### Apêndice — janela a copiar (resumo operacional)

Do report CRU do físico (`base` = 1 se `report[0]==0x01`, 2 se `==0x31`):
`vpad_body[15:40] = raw[base+15 : base+40]`
(= gyro 6 B + accel 6 B + timestamp 4 B + reserved2 1 B + 2 pontos de 4 B).
O resto do `vpad_body` (sticks/botões/seq/status) segue como está.

---

## Confirmação AO VIVO (2026-07-19, read-only) — o gyro do vpad está MORTO

Amostragem de 1,5s dos nós Motion Sensors (evdev, O_RDONLY, sem grab):

| nó | dispositivo | eventos | gyro/accel | veredito |
|----|-------------|---------|-----------|----------|
| event9 | DualSense branco USB (físico) | 2286 | 1534 (6 eixos) | **GYRO VIVO** |
| event260 | DualSense roxo BT (físico) | 8635 | 6377 (6 eixos) | **GYRO VIVO** |
| event27 | vpad P1 (Hefesto Virtual) | 0 | 0 | **SILÊNCIO TOTAL** |
| event263 | vpad P2 (Hefesto Virtual) | 60 | 0 | só não-ABS (sem gyro) |

CONCLUSÃO: o hardware e o hid-playstation entregam gyro/accel perfeitamente nos DualSense
FÍSICOS (USB e BT). O VPAD — o que o jogo enxerga jogando pelo hefesto com a máscara DualSense
— emite ZERO gyro/accel. Ou seja: gyro aiming pela via do co-op/wrapper está morto HOJE (gate
DEDUP-02 confirmado empiricamente). Jogo que lê o físico direto (nativo/plug-direto) tem gyro;
jogo que lê o vpad, não. FUT-02 (forward_motion espelhando o report do físico) é a cura exata.

## Achado 2026-07-19: a IMU do Nintendo Pro REAL está em STANDBY (não é vpad)

Leitura crua via EVIOCGABS dos nós IMU (parados na mesa, read-only):

| controle | accel X,Y,Z | gyro RX,RY,RZ | eixos que mudam em 0,3s |
|----------|-------------|---------------|------------------------|
| Nintendo Pro REAL (E0:F6:B5) | **0,0,0** | 8994,-1000,-3000 (congelado) | **0/6 — PRESO** |
| 8BitDo modo Switch (E4:17:D8) | 169,36,4188 | varia | 6/6 — amostrando |

Prova: accel=0,0,0 é impossível num sensor vivo (sempre sente ~1g; cf. Z=4188 do 8BitDo).
A IMU do Nintendo genuíno NÃO amostra no Linux — `hid-nintendo` lê a factory cal e declara os
eixos (abs=0x3f), mas não liga o sensor deste firmware; no Switch o console ativa a IMU pelo
protocolo dele. É native/kernel, INDEPENDENTE do vpad (um vpad copiaria os zeros). ninguém segura
o nó (lsof vazio). CANDIDATO DE CURA (avaliar risco): enviar subcomando 0x40/0x01 (enable IMU) no
hidraw do Nintendo — MESMO território que matou o 8BitDo BT por subcmd rate; por cabo é mais seguro.
Não bloqueia a v1: o fix de gyro via vpad é do DualSense; o 8BitDo já amostra nativo.
