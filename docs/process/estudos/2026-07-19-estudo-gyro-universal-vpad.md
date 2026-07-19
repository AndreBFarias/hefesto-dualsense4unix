# Estudo 2026-07-19 — Gyro de todos os controles (via vpad p/ DualSense; nativo p/ externos)

> Frota de estudo (G1 DualSense completo; Nintendo/8BitDo/arquitetura/síntese caíram por limite de
> sessão — sintetizado direto por Claude a partir do G1 + medições ao vivo próprias). Read-only.
> MACs: `<MAC-NINTENDO>`=E0:F6:B5 (real), `<MAC-8BITDO>`=E4:17:D8 (OUI 8BitDo confirmada no estudo BT).

## TL;DR — o gyro por controle, MEDIDO ao vivo (2026-07-19)

| Controle | Transporte | Gyro sai? | Onde o jogo o vê | Precisa de quê |
|----------|-----------|-----------|------------------|----------------|
| DualSense branco | USB |  físico vivo (250 Hz), **vpad = 0** | vpad | **forward_motion (esta onda)** |
| DualSense roxo | BT |  físico vivo (**765 Hz!**), **vpad = 0** | vpad | **forward_motion (esta onda)** |
| Nintendo Pro REAL (E0:F6:B5) | USB |  **IMU em STANDBY** (accel 0,0,0 congelado) | nativo (passthrough) | **enable-IMU nativo (faseado, risco)** |
| 8BitDo (E4:17:D8) | USB |  **nativo vivo** | nativo (passthrough) | nada — já funciona |

**Decisão de arquitetura (confirmada pela mantenedora):** o fix "gyro via vpad" é **só do
DualSense** — é o único cujo caminho (vpad máscara Edge) mata o gyro. Externos passam direto ao
jogo (sem vpad), então o gyro deles NÃO depende de vpad; dar-lhes vpad seria reverter o design
8BIT-02 e herdar a fragilidade do hid-nintendo sem ganho. O 8BitDo já entrega gyro nativo; o
Nintendo real tem um problema **nativo/kernel** (IMU não-ativada), curável sem vpad.

## Parte 1 — Gyro do DualSense via vpad (ENTRA NESTA ONDA)

### Por que o vpad emite 0 (prova)
`integrations/uhid_gamepad.py:_encode_body` (:794) preenche sticks (body[0:6]), botões/d-pad
(:806-811), status (:803) e carimba 0x80 nos touch points (offsets 32/36). A janela **body[15:40]
fica ZERADA** — é exatamente onde moram gyro, accel, timestamp e touch. Medição confirma: nó Motion
do vpad emite silêncio total.

### Offsets EXATOS (kernel drivers/hid/hid-playstation.c `struct dualsense_input_report`, 0-based após report id)
- gyro[3] __le16 = **15-20** (x=pitch 15-16, y=yaw 17-18, z=roll 19-20)
- accel[3] __le16 = **21-26** (x 21-22, y 23-24, z 25-26)
- sensor_timestamp __le32 = **27-30** (unidade 0,33 µs — kernel faz DIV_ROUND_CLOSEST(ts,3))
- touch points[2] (4B cada) = **32-35 e 36-39**
- Constantes: DS_INPUT_REPORT_USB=0x01/SIZE=64; DS_INPUT_REPORT_BT=0x31/SIZE=78 (struct começa em
  data[2], CRC32 nos bytes 74-77); DS_GYRO_RES_PER_DEG_S=1024; DS_ACC_RES_PER_G=8192 (batem com a
  `res` dos nós evdev vivos).

### Fonte = hidraw CRU do físico (NÃO evdev) — 3 razões
1. Cópia byte-a-byte da janela 15-39 → zero matemática, touch id e timestamp de graça.
2. O `sensor_timestamp` (o dt que o SDL usa p/ integrar o gyro) **só existe no HID cru** — o evdev
   Motion não o expõe (o tv do input_event é hora de recepção, não o relógio de 0,33 µs do sensor).
3. O valor cru é int16 não-calibrado = exatamente o que o report 0x01 carrega e o que o
   hid_playstation do vpad espera calibrar. Ir por evdev exigiria DES-calibrar (duas transformações,
   erro acumulado) e reescrever o TouchpadReader p/ multitouch. Mais código, resultado pior.

### Calibração (feature report 0x05) — para não drivar/escalar errado
O hid_playstation do vpad (e o SDL) calibram o Motion com o **0x05 que o vpad responde no probe**
(`uhid_gamepad.py:_reply_get_report` :1155 devolve `_features[0x05]` = CANONICAL congelado de UMA
unidade — a P1 branca). Logo o 0x05 do vpad tem de bater com a unidade que produz os bytes crus:
- **P1 branca USB**: 0x05 canônico veio dela → passthrough já exato.
- **Outras unidades (roxa BT)**: canônico erra bias (drift lento na mira) e sensibilidade. Cura:
  **carimbar o 0x05 do físico no blueprint do vpad**, no mesmo ponto onde `_features_com_mac_proprio`
  (:667) carimba o MAC no 0x09 — substituir features[0x05] quando `calibration_0x05` (41 B) for
  válido; fallback = canônico. Ler via novo `read_calibration()` no backend
  (`get_feature_report(0x05,41)` sob `_io_lock`; hidraw em `backend_pydualsense.py:558`); BT ocioso
  pode dar EIO → fallback (gyro funciona, drift leve tolerável).

### Taxa — hoje travada em 60 Hz; físico entrega MUITO mais (MEDIDO)
Poll loop = 60 Hz (`daemon/lifecycle.py:1761`, DEFAULT_POLL_HZ=60). Um gyro amarrado ao tick ficaria
a 60 Hz. Medido ao vivo (SYN/s, estável): **DualSense USB 250 Hz; DualSense BT ~765 Hz** (3× a
suposição de "~250" do estudo anterior — rádio BT tunado nesta máquina). Portanto a thread nova
`PhysicalReportReader` (o reader é o relógio, desacoplado dos 60 Hz) é **obrigatória**. E o throttle
por-vpad é MAIS necessário do que se assumia: a 765 Hz × 4 vpads em co-op = ~3000 writes/s ao
/dev/uhid — **capar emissão em ~250-500 Hz** (jogos integram gyro bem nessa faixa).

### Hook points (arquivo:linha)
- `_encode_body` (uhid_gamepad.py:794): passar a preencher `body[15:40] = self._motion_window`
  (default neutro: IMU zero + 0x80 em 32/36 = idêntico a hoje, anti-regressão).
- Novo `forward_motion(self, window: bytes)` (irmão de `forward_analog`, :744): valida len==25,
  guarda sob `_lock`, e EMITE (o reader dita o ritmo).
- `_emit_if_changed` (:776) ganha `set_motion_streaming(on)`: com streaming, forward_analog/buttons
  só atualizam cache e NÃO emitem (o reader emite) — evita emissão dupla.
- Chamadores viram só-cache por tick: `dispatch_gamepad` (gamepad.py:737-745), `CoopSubsystem.
  forward_all` (coop.py:798-806).
- Spawn do reader: `start_gamepad_emulation` (gamepad.py:576/630) cria
  `PhysicalReportReader(hidraw=controller.hidraw_path(), vpad=device)`; teardown em
  `stop_gamepad_emulation` (:682, ANTES de device.stop()). Co-op: `_promote_player` (coop.py:457/470)
  — um reader por jogador (FASE 2, precisa de hidraw-por-jogador).
- Retarget na troca de primário: `_recompute_primary` (backend_pydualsense.py:952) já faz
  `_evdev.retarget()` (:973) — retargetar o reader também (novo hidraw).

## Parte 2 — Nintendo Pro REAL: IMU em standby (NATIVO, faseado)

Prova (EVIOCGABS ao vivo, parados na mesa):

| controle | accel X,Y,Z | gyro RX,RY,RZ | muda em 0,3s |
|----------|-------------|---------------|--------------|
| Nintendo REAL (E0:F6:B5, event7) | **0,0,0** | congelado | **0/6 — STANDBY** |
| 8BitDo (E4:17:D8, event270) | 169,36,4188 | varia | 6/6 — vivo |

accel=0,0,0 é impossível num sensor vivo (sempre sente ~1g). A IMU do Nintendo genuíno **não
amostra** no Linux: `hid-nintendo` leu a factory cal ("using factory cal for IMU" no dmesg) e
declarou os eixos (abs=0x3f), mas não ligou o sensor deste firmware. No Switch o console ativa a
IMU pelo protocolo dele. É **native/kernel, independente do vpad** (o Nintendo passa direto ao jogo;
um vpad copiaria os zeros). Ninguém segura o nó (lsof vazio).

**Candidato de cura (FASEADO, exige análise de risco):** enviar o subcomando **0x40 arg 0x01**
(Enable IMU) no hidraw do Nintendo (protocolo Joy-Con/Pro do hid-nintendo). RISCO: é o MESMO
território (subcomando no hid-nintendo) que estourou o rate e **matou o 8BitDo no BT** (2026-07-18).
Por CABO — que é o caso do Nintendo agora — é bem mais seguro (sem rádio, sem rate-limit de BT).
Precisa: (a) confirmar o formato exato do pacote de saída rumble+subcmd do hid-nintendo; (b)
enviar UMA vez na adoção, com backoff, nunca em loop; (c) reconfirmar a identificação do device
(por uniq E0:F6:B5 / OUI) no momento da implementação — o agente G1 chegou a trocar os rótulos por
caminho de barramento; a fonte da verdade é a OUI (E4:17:D8 = 8BitDo).

## Parte 3 — 8BitDo e o resto: nada a fazer
8BitDo (modo Switch, cabo) já entrega gyro nativo vivo (medido). Passa direto ao jogo. Se a
mantenedora trocar p/ D-input/X-input o comportamento pode mudar (fora de escopo até haver pedido).

## Plano incremental
- **AGORA (esta onda):** Parte 1 — forward_motion do DualSense físico→vpad (USB e BT), com
  PhysicalReportReader, throttle 250-500 Hz, e 0x05-por-unidade. Cobre os 2 DualSense.
- **FASE 2:** reader por-jogador no co-op (hidraw-por-jogador) — os secundários também com gyro.
- **FASEADO/risco:** Parte 2 — enable-IMU nativo do Nintendo real (por cabo primeiro).
