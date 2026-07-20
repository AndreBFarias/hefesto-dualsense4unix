# Sprint Onda G — GYRO-02 (IMU do Nintendo real) + doctor de rádio + telemetria

> Executar APÓS Onda N e HANG-01 (colisão em external_identity/doctor). Base:
> `2026-07-19-estudo-gyro-universal-vpad.md` (GYRO-02) + mapa §3.4 + estudo BlueZ (doctor).

## G1 — GYRO-02: ligar a IMU do Nintendo Pro REAL (FASEADO, USB primeiro)
Contexto medido: o Pro real (OUI `E0:F6:B5`) tem IMU em STANDBY (accel 0,0,0 congelado — o
hid-nintendo lê a calibração mas não LIGA o sensor); o 8BitDo (OUI `E4:17:D8`) tem IMU nativa
viva (NADA a fazer nele). Ligar = subcomando `0x40` com argumento `0x01`. É o MESMO território
de subcomando que já matou o 8BitDo BT por rate (EXT-04) — daí o faseamento.

1. Implementar em `core/external_leds.py`/`external_identity.py` (onde o LED de player já
   escreve subcomando com rate-limit): função `enable_imu(hidraw)` que monta o pacote
   rumble+subcmd padrão do Switch (espelhar o formato do write_player_number existente,
   trocando subcmd/arg) e envia **UMA vez na adoção**, com backoff (nunca loop; nunca retry
   além de 2 com ≥2s), APENAS quando: uniq OUI == `E0:F6:B5` (Nintendo real) E bus == usb
   (fase 1 — BT só após medição de campo com kernel-watch [JOYCON] limpo).
2. Telemetria: log `external_imu_enable_enviado {uniq, bus}` + resultado; nunca falha
   propaga (suppress + warn).
3. Teste: fake hidraw registra o pacote exato (golden bytes do subcmd 0x40/0x01 conforme o
   formato do kernel hid-nintendo — conferir contra drivers/hid/hid-nintendo.c do kernel da
   máquina, /usr/src ou source online); OUI errado ⇒ zero escrita; bus BT ⇒ zero escrita
   (fase 1); rate: 1 envio por adoção.
4. Gate humano (validação final): Pro no cabo, evtest no node IMU dele → eixos vivos; depois
   `(IMU)` node do jogo/Steam.

## G2 — doctor: seção "Rádio e pareamento"
Checks read-only novos (padrão dos checks existentes em scripts/doctor.sh):
1. Versão do bluez: `<5.79` ⇒ FAIL com dica do backport (estudo/install ONDA-R); `≥5.79` OK.
2. `hefesto-bt-agent.service` ativo ⇒ OK; ausente/inativo ⇒ WARN com o porquê (bond meio-salvo).
3. Detector "Connected sem hidraw": para cada device BT input-gaming conectado no bluetoothctl,
   existe hidraw com HID_UNIQ correspondente? Não ⇒ FAIL "pareamento meio-salvo — remove+PS".
4. "Paired sem Bonded" via bluetoothctl info ⇒ FAIL com a mesma dica.
5. Sink de áudio padrão MUTED ⇒ WARN com dica wpctl (sintoma U12 de hoje).
6. Autoridade de exibição (se NUMA-05 ainda não a expôs no doctor, fazer aqui): `unknown`
   preso ⇒ WARN com causa.

## G3 — telemetria por vpad
`state_full`: expor `ff_play_count` e `motion_hz` POR vpad/jogador (hoje agregado) — consumo
pela aba Status (cards) sem quebra de schema (campos novos opcionais). Teste de shape.

## Aceite
- Suíte completa + ruff + mypy verdes; zero skipped.
- G1 não dispara NENHUM subcomando para 8BitDo/BT (testes provam); doctor cobre os 6 checks.
