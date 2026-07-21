# Estudo 2026-07-18 — BT no máximo (PLAT-04): stack Bluetooth da máquina de referência

> Missão BT-MAX da sprint `2026-07-18-sprint-plataforma-proton-usb-bt.md` (§PLAT-04 item 3).
> Coleta 100% read-only ao vivo em 2026-07-18 ~22h (boot atual iniciado 19:58). Toda
> afirmação abaixo tem a evidência (comando/arquivo/journal) anotada. Convenção:
> **[DEFAULT-SEGURO]** = provado existir e inócuo, pode entrar no install sem flag;
> **[INVESTIGAR-MAIS]** = existe mas exige medição/decisão; **[REJEITADA]** = não fazer.

## 1. Estado atual do stack (inventário provado)

| Item | Valor | Evidência |
| --- | --- | --- |
| Adaptador | TP-Link 2357:0604 = **Realtek RTL8761BU**, HCI/LMP 5.1 | `hciconfig -a` (Manufacturer 93/Realtek, HCI 5.1); dmesg `RTL: loading rtl_bt/rtl8761bu_fw.bin` |
| Firmware | carregado OK, `fw version 0xdfc6d922`, config `rtl8761bu_config.bin` (cfg_sz 6) | dmesg boot atual, t=9.7–10.1s |
| Saúde do link | `errors:0` RX e TX; RX 339 MB acl:3.9M | `hciconfig -a` |
| BlueZ | **5.72** (`bluetoothd --version`), binário `/usr/libexec/bluetooth/bluetoothd` | comando ao vivo |
| main.conf | **100% default** — única linha ativa: `AutoEnable=true` em `[Policy]` | `grep -vE '^\s*(#|$)' /etc/bluetooth/main.conf` |
| input.conf | **100% default** (nenhuma linha ativa além de `[General]`) | idem |
| btusb | `enable_autosuspend=Y` (default do módulo — o FURO da sprint) | `/sys/module/btusb/parameters/enable_autosuspend` |
| USB do dongle (3-1) | `power/control=on`, `autosuspend_delay_ms=-1000`, `runtime_status=active`, 12 Mbps | sysfs `/sys/bus/usb/devices/3-1/power/*` |
| Quem garante o "on" hoje | `usbcore.autosuspend=-1` no cmdline (**Aurora**, terceiro) | `/proc/cmdline` |
| Pareados | SÓ 2: DualSense `aa:bb:cc:00:00:02` (conectado, **Trusted: no**, RSSI −72) e "Pro Controller" `e4:17:d8:00:00:03` (Trusted: yes, desconectado, OUI E4:17:D8 = 8BitDo → é o 8BitDo em modo Switch) | `bluetoothctl devices Paired` + `info` |
| **Clone DS4 054C:05C4** | **NÃO está mais pareado** (sobrou só rastro no cache, §4) | `bluetoothctl devices` (2 entradas) |
| Discovering | **yes AO VIVO** — causa: `cosmic-settings bluetooth` aberto (pid 4015) | `bluetoothctl show` + `pgrep -af` |
| debugfs hci0 | `idle_timeout=0`, sniff 80–800 slots; `supervision_timeout=42`/`conn_*_interval 24/40` são os defaults **LE** (não se aplicam a gamepads BR/EDR) | `/sys/kernel/debug/bluetooth/hci0/*` |

Leitura do estado: o rádio está saudável HOJE (0 erros HCI, firmware ok, autosuspend
neutralizado), mas a garantia do power management é herdada da Aurora (cmdline global), não
nossa — exatamente o furo que a PLAT-04 item 1 cura.

## 2. Histórico de erros (journal, boots −5..0)

### 2.1 O storm do clone DS4 — dimensionado com precisão

Boot −1 (17/07 15:45 → 18/07 01:42):

- **211.222 linhas** `playstation 0005:054C:05C4.*: DualShock4 input CRC's check failed`
  entre **17:03:51 e 19:57:55** (~2h54 ≈ **20 msgs/s** contínuas).
  Evidência: `journalctl -k -b -1 | grep -c "DualShock4 input CRC"`.
- No connect (17:03:51) o kernel já denuncia firmware clone: `unknown main item tag 0x0`,
  `Failed to retrieve feature with reportID 163: -5`, `Failed to retrieve DualShock4
  firmware info: -5`, calibração de gyro/accel toda inválida,
  `Registered DualShock4 controller hw_version=0x00000000 fw_version=0x00000000`.
- Mecânica do dano PROVADA no host: o hid-playstation valida CRC32 de todo input report BT;
  o firmware clone não o calcula → **todo report é descartado + 1 linha de kernel log por
  report** → flood de journald/dmesg na taxa de input. Dano ao rádio (retransmissão/ocupação
  de banda ACL para lixo) é o efeito colateral: no MESMO boot o DualSense REAL registrou
  39 `DualSense input CRC's check failed` (corrupção RF de verdade), contra 2 no boot atual,
  2 no −2, 14 no −3, 6 no −5.
- O clone reconectou de novo às 21:54:41 do mesmo boot (novo hid `0005:054C:05C4.0016`).

### 2.2 Boot atual (18/07 19:58 →)

- 2 ocorrências de `DualSense input CRC's check failed` (nível de fundo aceitável), zero
  l2cap error, zero supervision timeout, zero erro HCI (`hciconfig errors:0`).
- bluetoothd: `connect to e4:17:d8:00:00:03: Connection refused (111)` às 21:34 e 21:40 +
  `Can't get HIDP connection info` — o 8BitDo (agora NO CABO por decisão da mantenedora)
  tentando/negando reconexão BT; consistente com o muro do hid-nintendo BT (§PLAT-04 item 4).
  Nada a curar aqui via BlueZ.
- `ACL packet for unknown connection handle` ×5 apenas no shutdown do boot −1 (teardown,
  inócuo).

### 2.3 Rádio extra na mesa (achado colateral)

No boot −1 — o boot do storm — havia um **Wi-Fi USB rtw88_8822bu** ativo
(`wlxdc6279705ae7`, associado a AP; dmesg 17/07 15:45). Ele está AUSENTE no boot atual
(`ip link`: só lo + enp9s0). Quando plugado, é um 4º rádio de 2.4 GHz no ar. Entra no texto
de coexistência do doctor (§5).

## 3. O que EXISTE de verdade no BlueZ 5.72 instalado (verificação anti-invenção)

Não há man page de `main.conf` no pacote Ubuntu (`man main.conf` = nada; só
`org.bluez.*.5`). Verificação feita em DUAS fontes: o template comentado
`/etc/bluetooth/main.conf` (documenta a versão instalada) e `strings` do binário
`/usr/libexec/bluetooth/bluetoothd` (option parser). **Confirmadas presentes no binário**:

- `[General]`: `FastConnectable`, `ControllerMode`, `Privacy`, `JustWorksRepairing`,
  `TemporaryTimeout`, `KernelExperimental`, `ReconnectAttempts`/`ReconnectIntervals`/
  `ReconnectUUIDs` (estas três são de [Policy]).
- `[BR]` (carregadas no kernel via MGMT_LOAD_DEFAULT_PARAMETERS antes do power-on):
  `PageScanType/Interval/Window`, `InquiryScan*`, **`LinkSupervisionTimeout`**,
  `PageTimeout`, `MinSniffInterval`/`MaxSniffInterval`.
- `[LE]`: `MinConnectionInterval`/`MaxConnectionInterval`/`ConnectionLatency`/
  `ConnectionSupervisionTimeout`/`Scan*` — **irrelevantes para os gamepads da casa**
  (DualSense, DS4, 8BitDo/Pro Controller são BR/EDR clássico, HIDP; provado pelos nós
  `0005:*` = bus BLUETOOTH clássico no dmesg).
- `input.conf`: `IdleTimeout` (default 0 = **nunca desconecta por ociosidade** — já é o
  máximo), `UserspaceHID`, `ClassicBondedOnly` (default true), `LEAutoSecurity`.

Módulos (modinfo, provado):

- `btusb`: parm `enable_autosuspend` (bool) — alvo da cura. Também `reset` (Y default).
- `hid_playstation`: **nenhum parâmetro de módulo** (não existe nada a tunar aí — não
  inventar).
- `hid_nintendo`: nenhum parâmetro exposto; `joycon_enforce_subcmd_rate` é comportamento
  interno (mensagem hardcoded), não configurável.
- `usbhid`: `jspoll`/`quirks` existem (assunto da PLAT-06 item 3, medir antes).

### Análise opção a opção

| Opção | Veredito | Racional/evidência |
| --- | --- | --- |
| `btusb enable_autosuspend=0` (modprobe.d) | **[DEFAULT-SEGURO]** | O estado-alvo é o estado ATUAL da máquina (power on/active, que funciona há semanas) — só muda o DONO da garantia de Aurora→hefesto. Furo real provado (`=Y` hoje). Vale no próximo boot; runtime já está coberto (control=on). |
| `FastConnectable=true` ([General]) | **[DEFAULT-SEGURO]** (com ressalvas de implementação abaixo) | Existe no binário 5.72; efeito: page scan agressivo → reconexão entrante mais rápida (o PS-button do DualSense conecta mais rápido). Custo documentado no próprio template: só consumo do dongle (desktop: irrelevante). NÃO mexe em link ativo. Ressalvas: (a) `/etc/bluetooth/main.conf` é conffile do dpkg → editar com bloco marcado idempotente + backup + uninstall simétrico (padrão da casa); (b) só vale após restart do bluetoothd → NÃO forçar restart no install (derruba controles BT conectados — visto ao vivo em 8BIT-02); aplicar e avisar "vale no próximo boot/restart". |
| Check doctor: `IdleTimeout` do input.conf | **[DEFAULT-SEGURO]** (check read-only) | Default 0 já é "sem restrição"; o doctor só alerta se alguém setou >0 (regressão de terceiro). |
| `JustWorksRepairing=confirm` | **[INVESTIGAR-MAIS]** | Curaria o re-pareamento manual pós-dessincronia de bond (caso SDP da memória de 2026-06). "confirm" exige agente respondendo; interação com o agente do COSMIC não testada. "always" = risco de re-pareamento por peer arbitrário — não. |
| `[BR] LinkSupervisionTimeout` | **[INVESTIGAR-MAIS]** | Existe (strings). Default do kernel BR/EDR = 0x7D00 (20 s). Reduzir detecta queda mais rápido porém derruba o link em fade transitório de RF; sem medição de campo, não mexer. |
| `[BR] Min/MaxSniffInterval`, `PageScan*` | **[INVESTIGAR-MAIS]** | PageScan* fica redundante com FastConnectable; sniff não é usado pelo DualSense em jogo (sem evidência de sniff nos logs). Só com medição. |
| `Privacy` (RPA) | **[REJEITADA]** | Default off; ligar RPA pode quebrar reconexão de periféricos clássicos. Nada a ganhar para gamepad. |
| `ControllerMode=bredr` | **[REJEITADA]** | Gamepads são BR/EDR, MAS o cache mostra periféricos LE reais da casa (Redmi Watch, buds); forçar bredr os quebraria. |
| `ClassicBondedOnly=false` | **[REJEITADA]** | Default true é proteção; o clone 05C4 pareava normalmente (não é esse o problema dele). |
| Tuning `[LE]` qualquer | **[REJEITADA]** | Nenhum gamepad da casa é LE (todos `0005:*` HIDP clássico). |

## 4. Clone DS4 054C:05C4 — detecção pelo doctor

**Estado hoje: despareado** (só DualSense + 8BitDo-modo-Switch em `bluetoothctl devices`).
Mas ele já voltou uma vez no mesmo boot (§2.1) e pode voltar — o doctor precisa vigiar.

**Identidade provável do clone (achado novo):** o cache do adaptador
(`/var/lib/bluetooth/d8:44:89:00:00:05/cache/`) guarda
`E4:17:D8:00:00:07 → Name=Wireless Controller` (MAC mascarado, distinto do Pro
Controller pareado; "Wireless Controller" é o nome exato do
DS4) com **OUI E4:17:D8 = 8BitDo** — o mesmo OUI do "Pro Controller" pareado
(`e4:17:d8:00:00:03`). Ou seja: o "clone DS4" é quase certamente **um 8BitDo em modo
D-input/DS4** (esse modo se apresenta como 054C:05C4), não um controle pirata avulso.
Plausível (OUI + nome; o cache não guarda Modalias) — muda o TOM do texto: não é "jogue
fora", é "troque o modo do controle".

**Critério de detecção (provado com os comandos reais):**

1. Pareado: para cada MAC de `bluetoothctl devices`, `bluetoothctl info <MAC>` e procurar
   `Modalias: usb:v054Cp05C4` → candidato a clone.
   (Cuidado honesto: 054C:05C4 é também o PID do **DS4 v1 LEGÍTIMO**. Desambiguar por:
   OUI do MAC fora dos ranges Sony e/ou sinais de firmware clone no journal —
   `hw_version=0x00000000`, `Failed to retrieve DualShock4 firmware info`.)
2. Ativo/degradando: `journalctl -k -b 0 | grep -c "DualShock4 input CRC's check failed"`
   — qualquer contagem alta (>100) = clone conectado bombardeando o log (no storm foram
   20/s). O mesmo contador serve de métrica "rádio sujo" para o DualSense real
   (`DualSense input CRC's check failed`; hoje: 2 = fundo aceitável).

**Texto sugerido para o doctor (leigo):**

> "Um controle tipo DualShock 4 'genérico' (054C:05C4) está pareado neste computador. Esse
> modelo não calcula a verificação de integridade dos dados e inunda o sistema com erros
> (já foram 211 mil em uma noite), degradando o Bluetooth para TODOS os controles.
> Recomendação: desparear (`bluetoothctl remove <MAC>`). Se ele for um 8BitDo, prefira o
> modo Switch (ou use no cabo) — funciona melhor e não polui o rádio."

## 5. Coexistência 2.4 GHz — topologia e recomendações

**Topologia USB provada** (`lsusb -t` + resolução de `/sys/bus/usb/devices/usbN` → PCI):

- Bus 1/2 = chipset AMD 400 Series (`02:00.0`): receiver 2.4G CX `3554:fa09` (porta 1-3),
  receiver 2.4G Areson `25a7:fa07` (porta 1-4), Pro Controller USB (1-6).
- Bus 3/4 = CPU Matisse (`0c:00.3`): **dongle BT (3-1)**, 8BitDo-no-cabo como Pro
  Controller (3-3), DualSense USB (3-4).

Conclusão: BT e os 2 receivers Compx estão em **controladores USB separados** — não há
disputa de barramento/hub entre eles (bom; nada a mudar de porta por causa de USB).
O problema de coexistência é **de RF, não de barramento**: 3 rádios de 2.4 GHz (dongle BT +
2 receivers proprietários) enfiados no mesmo painel traseiro, a centímetros de distância e
atrás do gabinete de metal — mais o Wi-Fi USB 2.4G quando plugado (presente no boot do
storm, §2.3). RSSI do DualSense conectado medido ao vivo: **−72 dBm** (margem baixa; bom
seria > −60).

**Texto prático para o doctor (seção "Rádio 2.4 GHz")** [DEFAULT-SEGURO como texto/check]:

1. Dongle BT num **extensor USB curto**, saindo da sombra do gabinete e afastando-o ≥20 cm
   dos receivers de mouse/teclado — é a única mudança física com ganho real comprovável
   (RSSI sobe na hora; o doctor pode reler o RSSI e mostrar o antes/depois).
2. Evitar porta USB 3.x com tráfego 5 Gbps adjacente ao dongle (ruído broadband de USB 3.0
   cai exatamente em 2.4–2.5 GHz — interferência conhecida da literatura Intel; hoje o
   dongle está em enlace 12M e não há device 5G no mesmo grupo de portas: ok).
3. Wi-Fi USB 2.4 GHz (rtw88) plugado = mais um competidor de espectro durante co-op BT —
   preferir o cabo Ethernet (que a máquina já usa) e o Wi-Fi despluggado.
4. Alerta ao vivo: **página Bluetooth do cosmic-settings aberta mantém Discovering=yes**
   (provado hoje: pid 4015) — inquiry contínuo rouba slots de banda dos links ACL dos
   controles. Doctor: se `bluetoothctl show | grep Discovering: yes` com gamepad BT
   conectado → "feche a tela de Bluetooth enquanto joga".
5. Métrica contínua: contadores de `input CRC's check failed` por boot (kernel-watch da
   PLAT-06 item 4) — é o termômetro de rádio sujo que já diferenciou storm (211k) de fundo
   (2–39).

## 6. Achados extras (fora do escopo estrito, registrados)

- **DualSense pareado está `Trusted: no`** (o 8BitDo está yes). Sem trust, a reconexão
  entrante pode depender de autorização do agente da sessão. Doctor: detectar gamepad
  pareado não-confiado e sugerir `bluetoothctl trust <MAC>` (1 comando, reversível)
  [DEFAULT-SEGURO como check+texto; aplicar automaticamente só com consentimento].
- `Failed to confirm name for hci0: Invalid Parameters (0x0d)` 1× no boot (bluetoothd) —
  cosmético, sem correlação com falha.
- hciconfig mostra `Discoverable: yes` no momento da coleta (efeito da tela de settings
  aberta; timeout 180 s default) — sem ação.

## 7. Recomendações priorizadas (consolidado)

| # | Recomendação | Marca | Evidência-chave |
| --- | --- | --- | --- |
| 1 | `assets/modprobe`: conf `options btusb enable_autosuspend=0` no install (já é o item 1 da PLAT-04) | **[DEFAULT-SEGURO]** | `enable_autosuspend=Y` hoje; estado-alvo = estado atual que funciona; só muda o dono da garantia |
| 2 | Doctor: detecção do clone 054C:05C4 pareado (Modalias via `bluetoothctl info`) + contador de `CRC's check failed` do boot + texto §4 | **[DEFAULT-SEGURO]** (read-only) | storm de 211.222 msgs provado no boot −1; comandos de detecção validados ao vivo |
| 3 | Doctor: seção "Rádio 2.4 GHz" com os 5 checks/textos do §5 (RSSI, Discovering, extensor, Wi-Fi USB, contadores) | **[DEFAULT-SEGURO]** (read-only) | RSSI −72 medido; Discovering=yes reproduzido ao vivo; topologia provada por sysfs/lsusb |
| 4 | Doctor: gamepad pareado com `Trusted: no` → sugerir trust | **[DEFAULT-SEGURO]** (check; escrita só com consentimento) | DualSense hoje Trusted: no |
| 5 | `FastConnectable=true` em `/etc/bluetooth/main.conf` (bloco marcado, backup, uninstall simétrico, SEM restart forçado do serviço) | **[DEFAULT-SEGURO]** com ressalvas | opção confirmada no binário 5.72 + template; custo = consumo (desktop); conffile dpkg exige idempotência |
| 6 | Doctor: check de `IdleTimeout` não-zero em input.conf (regressão de terceiro) | **[DEFAULT-SEGURO]** (read-only) | default 0 confirmado = já ótimo |
| 7 | `JustWorksRepairing=confirm` (cura re-pareamento pós-dessincronia SDP) | **[INVESTIGAR-MAIS]** | opção existe; interação com agente COSMIC não testada |
| 8 | `[BR] LinkSupervisionTimeout` / sniff / page-scan finos | **[INVESTIGAR-MAIS]** | existem no binário; sem medição de campo, não mexer |
| 9 | `Privacy`, `ControllerMode=bredr`, `ClassicBondedOnly=false`, tuning `[LE]` | **[REJEITADA]** | §3 — quebram periféricos reais da casa ou não se aplicam a gamepads BR/EDR |

**Meta honesta reafirmada** (§PLAT-04 item 4): não há botão de "BT mais rápido" no BlueZ
para gamepads BR/EDR já conectados — o link ativo negocia seus próprios parâmetros. O que
está ao nosso alcance e este estudo prova: (a) garantir que NADA dorme (item 1), (b) manter
o rádio limpo (itens 2–3: clone fora, espectro arrumado, inquiry fechado), (c) reconectar
mais rápido (item 5) e (d) medir sempre (contadores de CRC como termômetro).
