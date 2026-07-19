# Sprint GYRO 2026-07-19 — gyro do DualSense via vpad + IMU nativa do Nintendo

> Estudo: `docs/process/estudos/2026-07-19-estudo-gyro-universal-vpad.md`.
> Medição ao vivo: vpad DualSense emite 0 gyro; físico USB=250 Hz, BT=765 Hz; 8BitDo nativo OK;
> Nintendo real com IMU em standby. Regra: install SEM FLAGS; testes herméticos; nunca import gi no topo.

## GYRO-01 — forward_motion: DualSense físico → vpad (ENTRA NA LEVA ATUAL, P0)

Objetivo: o gyro/accel/touchpad do DualSense físico chega ao jogo pelo vpad (máscara Edge).
Escopo (do estudo, Parte 1):
1. `integrations/uhid_gamepad.py`: `_motion_window` (25 B, default neutro), `forward_motion(window)`
   (:744, valida len==25, sob _lock, emite), `_encode_body` (:794) preenche `body[15:40]`,
   `set_motion_streaming(on)` em `_emit_if_changed` (:776) — streaming desliga a emissão dos
   forward_analog/buttons por tick (evita emissão dupla; reader é o relógio).
2. Novo `PhysicalReportReader` (thread): abre 2º fd O_RDONLY no hidraw do físico
   (`controller.hidraw_path()`), lê report 0x01 (base 1) / 0x31 (base 2, valida CRC32), copia
   `raw[base+15:base+40]` → `vpad.forward_motion(...)`. Throttle de emissão **250-500 Hz** (dedup +
   coalescência do último valor) — a 765 Hz BT × 4 vpads seria ~3000 writes/s ao /dev/uhid.
3. Calibração por unidade: `read_calibration()` no backend (`get_feature_report(0x05,41)` sob
   _io_lock; fallback canônico em EIO); carimbar no blueprint do vpad em `_features_com_mac_proprio`
   (uhid_gamepad.py:667) quando `calibration_0x05` válido. Sem isso, unidades ≠ P1 branca drivam.
4. Fiação: spawn em `start_gamepad_emulation` (gamepad.py:576/630), teardown em
   `stop_gamepad_emulation` (:682 antes de device.stop()), retarget em `_recompute_primary`
   (backend_pydualsense.py:952 junto do _evdev.retarget()).
5. Passthrough do touchpad (2 dedos) vem junto na mesma janela (offsets 32-39) — bônus.
Testes (herméticos): parser 0x01/0x31 com reports sintéticos (CRC BT validado); _encode_body
preenche 15-40 e mantém neutro sem streaming (anti-regressão); throttle capa a taxa; 0x05-por-unidade
carimba/fallback; forward_motion não emite lixo com window curta.
Gate ao vivo (eu valido): escrever no hidraw do vpad P1 a janela de um report real do físico →
o nó Motion do vpad (event27) passa a AMOSTRAR (hoje é silêncio); e em jogo com gyro aiming a mira
responde ao girar o DualSense branco (USB) e o roxo (BT).

## GYRO-02 — Nintendo Pro real: enable-IMU nativo (FASEADO — análise de risco antes)

NÃO entra na leva atual. A IMU do Nintendo genuíno (uniq E0:F6:B5) está em standby; cura candidata =
subcomando 0x40/0x01 (Enable IMU) no hidraw, MAS é o território que matou o 8BitDo no BT por
subcmd-rate. Pré-requisitos antes de implementar:
1. Confirmar o formato do pacote de saída do hid-nintendo (rumble+subcmd) na versão do kernel local.
2. Enviar UMA vez na adoção, por CABO, com backoff; nunca em loop; kernel-watch vigiando
   joycon_enforce_subcmd_rate.
3. Reconfirmar a identidade do device pela OUI no momento (E4:17:D8=8BitDo, E0:F6:B5=Nintendo) —
   não confiar em ordem de barramento.
Entregável desta fase = doc de risco + protótipo validado por cabo antes de virar default.

## GYRO-03 — telemetria e doctor (LEVA ATUAL, P2)
- state_full por vpad: `motion_streaming` (bool) e `motion_hz` (taxa de emissão) — hoje não há
  visibilidade de que o gyro flui.
- doctor: check "gyro do vpad" — amostra o nó Motion do vpad quando emulação ativa e reporta
  vivo/silêncio (o teste que rodei à mão, virado ferramenta pro leigo).

## Ordem na leva atual
GYRO-01 e GYRO-03 entram JUNTO com a implementação do broker/IMU-touchpad das próximas ondas
(mesma leva, sobre a árvore já corrigida pela auditoria). GYRO-02 fica faseado.
