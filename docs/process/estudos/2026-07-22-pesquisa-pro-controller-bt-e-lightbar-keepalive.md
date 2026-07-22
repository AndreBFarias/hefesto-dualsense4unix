# Pesquisa 2026-07-22 (noite) — Pro Controller BT que cai sob carga + lightbar apagada: causas-raiz e curas de software

**Contexto**: a mantenedora rejeitou explicitamente contornos de hardware/uso
("gambiarra da gambiarra") — kernel e sudo estão liberados para curar na RAIZ.
Contra-exemplo dela que refutou "banda saturada": 2 DualSense + 8BitDo por BT
convivem bem no mesmo adaptador; só o Pro real cai. Duas frentes: (1) pesquisa
web profunda (8 rodadas, fontes primárias: fonte do BlueZ, switchbrew,
MissionControl, SDL, linux-firmware, patches Valve, commits do kernel); (2)
forense byte-a-byte de captura btmon local.

## 1. ⭐ Por que o Pro cai em BT sob carga (e o 8BitDo não) — checagem do NOME do host

**Mecanismo (3 fontes independentes):** o Pro Controller lê o **nome Bluetooth
do host**. Em host que NÃO se chama "Nintendo*", ele cai para **sniff mode**,
que não envia keepalives periódicos e espera o host mandar tráfego com
frequência. Com rumble + IMU, os reports enfileiram; o controle perde o tráfego
esperado, assume que o link morreu e desconecta — exatamente a cascata
`timeout waiting for input report` → disconnect `0x16`/`0x22` que medimos.
- Fyra Labs, "Your Joy-Cons are Vibrating Themselves to Death" — descreve o
  mecanismo sniff/keepalive e a cura pelo nome.
- BlueZ issue #1797 (jan/2026, fechada "not planned"): com nome prefixado
  "Nintendo", "all of these problems clear up... resolved by doing this".
- ArchWiki Gamepad + relatos independentes: rename do adaptador é o workaround
  do disconnect com rumble.

**O que o console Switch faz (switchbrew + MissionControl):** é master, envia
comando **vendor Broadcom 0xFD95 (SetTsi)** + `HCI_Set_MWS_Signaling` (coex) +
`HCI_Sniff_Mode` com parâmetros tabelados casados à cadência do controle; se o
controle recusa o Sniff_Mode, o console derruba. O Linux só aceita o sniff
default que o controle pede. O nome "Nintendo*" é o atalho que o controle
oferece para sair do sniff frágil sem o vendor command.

**Cura nº 1 (aplicada ao vivo 22/07 para teste): alias do adaptador com prefixo
"Nintendo"** — `busctl set-property org.bluez /org/bluez/hci0
org.bluez.Adapter1 Alias s "Nintendo <hostname>"` (persistido em
`/var/lib/bluetooth/<adapter>/settings`). Custo zero, reversível (Alias de
volta ao hostname), não afeta DualSense/8BitDo. Se validar ao vivo, virar
entrega: `Name`/alias idempotente pelo install.sh + check no doctor.

**Knobs por-conexão alternativos (mesmo efeito, se o nome não bastar):**
- `hcitool sr <MAC> MASTER` + `hcitool lp <MAC> RSWITCH,HOLD,PARK` (omitir
  SNIFF → o LM local recusa `LMP_sniff_req` → força modo ativo).
- `hcitool lst <MAC> 8000` (supervision timeout 5s por conexão; requer central).
- debugfs BR/EDR: `/sys/kernel/debug/bluetooth/hci0/{idle_timeout,
  sniff_min_interval,sniff_max_interval}`. ATENÇÃO: `conn_min_interval`/`lecup`
  são LE-only, NÃO se aplicam ao Pro (BR/EDR) — erro comum nos guias.
- Aplicar na borda de conexão (hook do VPAD-09 já existe).

## 2. ⭐ Por que o bond do Pro EVAPORA (e o do DualSense não) — Virtual Cable Unplug no caminho uhid

Quando o Pro se desliga (ele desliga sozinho após perder o link), manda um
**HID Virtual Cable Unplug** (byte `0x15` no canal de controle HID, L2CAP
PSM 17). No BlueZ, `profiles/input/device.c`:
`hidp_recv_ctrl_hid_control()` → `connection_disconnect(..., 1<<HIDP_VIRTUAL_
CABLE_UNPLUG)` → `virtual_cable_unplug()` → **`device_remove_bonding(...,
BDADDR_BREDR)`** → bond apagado do disco.
- **Esse caminho só existe com input via uhid** — que o nosso backport 5.85/5.86
  ativou. No 5.72 stock (hidp.ko no kernel) o bond NUNCA era removido por isso.
  A janela temporal bate com o início do sintoma.
- O commit `ab6ce0c` (mai/2025, no 5.86) fez o BlueZ REALMENTE transmitir o
  VC-unplug no modo uhid → para device ainda-`temporary`, o BlueZ descarta o
  lado dele E manda o controle apagar a chave do host → explica o `Pair()`
  explícito que "não pega".
- Precedente idêntico sem fix upstream: bluez #2048 (headset perde pairing ao
  desligar via VC-unplug; fechada "not planned", sem opção de config).
- Por que só o Pro? O SDP `HIDVirtualCable` arma o bit; a linhagem Nintendo
  (herança Wiimote) sinaliza desligamento via VC-unplug. DualSense não emite.

**Cura nº 2 (após verificação btmon): patch de ~20 linhas no backport BlueZ**
neutralizar/gate o `device_remove_bonding()` do caminho virtual-cable-unplug em
`profiles/input/device.c`. Upstream recusou consertar (#2048/#1797), então o
patch próprio é o caminho — e nós já compilamos o backport.
**Verificação (5 min, ANTES de patchar):** `btmon` durante uma queda/desligamento
do Pro; procurar frame ACL no canal de controle com byte `0x15`
(`btl2cap.psm == 17 && payload[0] == 15`) OU `bluetoothd -d` + grep
`virtual_cable_unplug`/`Removing bonding`.

## 3. Dúvida do BlueZ, respondida em definitivo

- Commit `17a227b7` (o que motivou o 5.86) **NÃO remove bond nem marca
  temporary** — só adiciona `auth_failures`/threshold 3 e desabilita autoconnect
  em auth-failure repetida (com backoff `1<<n`). Storage intocado. Os motivos de
  disconnect do Pro (0x16/0x22) nem mapeiam para AUTH_FAILURE. **O 5.86 não é o
  ladrão de bonds; a decisão de versão NÃO reabre por isso.** (Ele explica o
  "autoconnect regredido" DEPOIS que o bond some e a reconexão vira auth-failure.)
- **Kernel: o DKMS local já está À FRENTE do Steam Deck de 2023.** A estabilidade
  do Pro no Deck veio do commit `d750d1480362` (HID: nintendo, mainline 6.4 —
  só transmite subcmd/rumble após 3 deltas consecutivos de 8-17ms + offset 4ms +
  limite 60ms BT/20ms USB). Verificado: o nosso `hid-nintendo.c` já tem TUDO
  isso (`consecutive_valid_report_deltas`, `JC_INPUT_REPORT_MIN/MAX_DELTA 8/17`,
  `JC_SUBCMD_TX_OFFSET_MS 4`, `JC_SUBCMD_RATE_LIMITER_BT_MS 60`) + o patch de
  out/2025 (`JC_SUBCMD_RATE_MAX_ATTEMPTS 500→25`, corta o pior caso 60s→3s).

## 4. Higiene do escritor (paridade SDL/kernel), independente das curas acima

- SDL `SDL_hidapi_switch.c`: `RUMBLE_WRITE_FREQUENCY_MS 30` ("mais frequente que
  isso desliga o controle em BT"); modo "simple" default em BT. Filosofia:
  minimizar subcomandos sobre BT.
- Recomendação da comunidade para rádio ruim: rumble é o gatilho nº1; sob link
  degradado, throttle agressivo/corte de rumble+subcmd para o Pro; NUNCA escrever
  LED/rumble em rajada na borda de reconexão.
- `options btusb reset=1` (o que a Valve faz no SteamOS) + check no doctor de que
  o RTL8761B carregou `rtl8761bu_fw` versão `0xDFC6D922` — a ÚLTIMA que existe
  no linux-firmware (mai/2023; não há firmware novo para esperar; o dongle local
  já está nela).

## 5. Descartado por evidência (não repetir)

- Novos knobs no hid-nintendo (o DKMS local já tem tudo upstream até out/2025).
- Comandos vendor Realtek de prioridade de link (não existem públicos; o coex do
  RTL8761B vive no firmware; como é BT-puro sem WiFi, a "coex" com o Archer T3U é
  EMI aérea/USB3, sem interface para tunar).
- Firmware do controle mais novo (Pro já está no fw 4.33, o mais recente; 8BitDo
  emula fw 3.72 — a diferença NÃO é idade de firmware, é o comportamento de rádio
  de cada chip).
- main.conf estilo Valve (os patches deles não atacam esse problema).
- 2º dongle BT / jogar no cabo (contornos; a mantenedora recusou — e a cura de
  software existe).

---

## Forense da lightbar apagada em BT (captura btmon-reconexao-roxo-1523.snoop)

**Veredito: o NOSSO keepalive re-engata a máquina de setup da lightbar a cada
500ms.** Decodificação byte-a-byte (599 reports 0x31 TX, todos CRC válido):
- O keepalive sai com **valid_flag2 = 0x03** (bit 0x01 brightness-control +
  bit 0x02 LIGHTBAR_SETUP_CONTROL_ENABLE) — o `ledOption=Both` (0x03) da
  pydualsense vazando cru no `_build_common`. O bit 0x02 é o MESMO que o kernel
  usa UMA vez por conexão (opcode 2 = LIGHT_OUT) para tomar a barra; disparado
  487× em regime, trava a exibição (o firmware aceita a cor no registrador — o
  sysfs mostra — mas não exibe).
- O reset 0x08 está bem-formado (CRC ok, seq coerente, chega antes da 1ª cor) —
  refutadas as hipóteses de reset malformado/fora de ordem. O kernel REESCREVE
  a cor do slot (38,162,105) 19× ao longo da captura, todas ignoradas.
- Regressão temporal: a cura de 17/07 funcionava porque os keepalives pré-
  BTREPORT-02 eram malformados e o firmware os descartava; o BTREPORT-02 (18/07)
  consertou o envelope → os keepalives passaram a CHEGAR carregando o flag2=0x03
  que sempre esteve no `_build_common`. A supressão FEAT-DSX-LIGHTBAR-SYSFS-01
  limpava só o flag1 e esqueceu o flag2.

**Fix (LIGHTBAR-BT-KEEPALIVE-01, entregue):** sob `_suppress_leds`, zerar também
os bits de setup/brilho do flag2 (0x02|0x01) e os bytes common[41..46]
(lightbar/player/setup) — o keepalive vira LED-neutro de fato. Constantes novas
em `ds_output_report.py`; teste em `test_backend_keepalive_neutro.py`.
