# Diagnóstico 21→22/07 (madrugada): DualSense "conectado mas morto", bonds BT que evaporam e o fantasma do "pra cima eterno"

**Contexto**: boot de 21/07 22:48 (pós-instalação com patches Nintendo ativos). Sintomas
reportados pela mantenedora ao vivo: (1) DualSense conectado mas sem input no jogo
(Sackboy, depois MMJ); (2) autoconnect dos 8BitDo/Nintendo "regredido"; (3) input
intermitente via BT (funciona → para → volta) que não acontece no cabo USB; (4) máscara
dualsense não funciona nem no cabo; (5) retorno do bug "algo invisível apertando ↑
eternamente". Diagnóstico feito com medição ao vivo (journal, hidraw cru, IPC
`daemon.state_full`, sysfs, `/var/lib/bluetooth`) + 2 agentes de estudo (código e levas)
+ 3 agentes de pesquisa (BlueZ versões, kernel/EMI, mitigações).

## Causas-raiz confirmadas (medidas, não teoria)

### 1. ⭐ Bonds BT nascem TEMPORÁRIOS — nenhum pareamento persiste em disco

- `/var/lib/bluetooth/D8:44:89:00:00:01/` continha APENAS `cache/` (25 devices, com
  mtimes recentes → escrita funciona, não é permissão), `attributes` e `settings`.
  **Zero diretórios `<MAC>/` com `info`** — nem do DualSense que estava "Paired: yes"
  e conectado havia horas.
- Quando o DualSense saiu do BT (foi para USB), `bluetoothctl devices` ficou **vazio**
  (nem Paired/Bonded/Trusted): o device era temporário em memória e evaporou.
- O journal do momento da "conexão" (22:56) não tem NENHUM evento de pairing — o
  controle conectou usando o bond do lado dele (o lado PC tinha perdido tudo no crash
  #6 do bluetoothd, 21/07 22:14) com `JustWorksRepairing=always` + bt-agent
  NoInputNoOutput, e o lado PC nunca gravou nada.
- Consequência direta: a "regressão do autoconnect" = crash comeu os bonds **e** nada
  novo persiste. O 8BitDo (`E4:17:D8:00:00:04`) passou o boot inteiro em loop de
  reconexão sendo recusado com `Refusing connection ... unknown device`.
- Agravante encontrado: `/etc/bluetooth/main.conf` tinha **três seções `[General]`
  duplicadas** (appends repetidos do install — o install.sh precisa escrever config de
  forma idempotente). GKeyFile com grupos duplicados tem comportamento indefinido
  para as chaves envolvidas (`JustWorksRepairing`, `FastConnectable`).
- Sintoma-irmão já visto em 19/07: controle roxo "Paired sem Bonded".

### 2. ⭐ Intermitência via BT = camada rádio (EMI), não a cadeia do daemon

- A/B da mantenedora: MMJ intermitente via BT, sólido via cabo USB. Fecha a camada.
- Kernel logou 4× `Bluetooth: Unexpected start frame (len 83)` na sessão BT —
  corrupção silenciosa de framing ACL no btusb (não conta como "erro hci"; upstream
  bluez#894 fechado not-planned). len 83 fixo sugere um tipo específico de report.
- Na sessão BT, o motion reader ficou 46 min em loop de silêncio→reabertura (~1.1s)
  no hidraw, e o evdev estagnou JUNTO, no mesmo nó, sem ENODEV — dois consumidores
  independentes mudos ao mesmo tempo = a causa está ABAIXO dos dois (link BT/kernel).
- Dongle BT = TP-Link 2357:0604 (RTL8761B, fw 0xdfc6d922); WiFi = Archer T3U
  (rtw88_8822bu). Nesta sessão estavam em xHCI separados (Bus 003 × Bus 004) —
  diferente da topologia da medição de 19/07; EMI por radiação/proximidade segue
  plausível, EMI por barramento não.

### 3. ⭐ Fantasma "↑ eterno" (desta noite) = pad virtual órfão do Steam

- O físico manda repouso perfeito (hidraw cru: LX=127 LY=125 dpad=8) e o daemon vê
  neutro (IPC `state_full`) → o fantasma NÃO nasce no controle nem no daemon.
- Trocar máscara/modo nativo pela GUI **com o jogo aberto** destrói o vpad no meio da
  sessão (por design: `gamepad.py:820-828` chama `stop_gamepad_emulation` antes de
  criar o novo device). O Steam Input já tinha criado pads X360 virtuais em cima do
  NOSSO vpad; com o vpad morto, o pad órfão do Steam congela no último estado — se o
  último estado era "↑" de navegação de menu, vira "↑ eterno".
- Observado no journal: cada troca de máscara em jogo gerou um conjunto NOVO de
  "Microsoft X-Box 360 pad" do Steam (input45-48, depois input57-60) convivendo com
  o antigo.
- É um fantasma DIFERENTE do histórico "↑ infinito" do VPAD-09 (aquele era HID-raw
  fallback interpretando offset errado; sticks ~253).

### 4. Lacuna estrutural no watchdog do evdev (agente de código, arquivo:linha)

- `evdev_reader.py:443-444`: `is_available()` só checa se um path já foi achado —
  não se eventos chegam. `is_stale()` (459-489) só detecta TROCA de nó; "mesmo nó,
  zero eventos" nunca dispara reabertura (o docstring admite a lacuna).
- Quando o evdev está "disponível", TUDO (eixos + botões) vem do snapshot dele
  (`backend_pydualsense.py:1536-1561`) → reader mudo = vpad emitindo neutro para
  sempre = "conectado mas morto".
- `state_stale_neutral_warning` dispara 1× no startup dentro do grace de settling —
  em xbox/USB funcionando ele também aparece; **não usar como prova de travamento**.
- Fix candidato: dar ao EvdevReader reabertura por silêncio prolongado, como o
  PhysicalReportReader já faz (`physical_report_reader.py:391-441`).

### 5. Máscara persistida e default de código

- A escolha da máscara persiste em `gamepad_emulation.flag` (por design, sobrevive a
  restart). **O default de código na ausência de flag é `xbox`**
  (`lifecycle.py:135`), não `dualsense` — contraria a expectativa "vpad sempre
  Edge/dualsense"; confirmar com a mantenedora qual deve ser o default.
- As duas sessões dualsense/uhid em USB (23:50:46 e 23:52:28) subiram LIMPAS
  (uhid_bind_ok, grab held, motion ok, Steam adotou o vpad em 10s). A falha
  percebida tem o confounder da troca em jogo. **Teste limpo pendente (gate
  humano)**: com jogo fechado → máscara dualsense → abrir o jogo.

## Hipóteses REFUTADAS pelo código (agente, não repetir)

- GET_REPORT 0x05 "acordando" o stream BT: refutado — 0x05 é calibração one-shot
  fail-safe (`backend_pydualsense.py:722-783`), sem relação com streaming.
- `suppress_desktop_emulation` matando input do jogo: refutado — suprime SÓ
  mouse/teclado desktop; o despacho do vpad roda antes do gate
  (`lifecycle.py:2249-2265`).
- Flapping gamedaemon do `game_signal` matando input: refutado — o sinal governa
  apenas posse de EXIBIÇÃO (lightbar/player LEDs); pode causar flicker visual, nunca
  input morto.

## Ações aplicadas nesta sessão (22/07 ~00:00-00:15, reversíveis)

1. `main.conf` consolidado em uma única `[General]` (`FastConnectable=true`,
   `JustWorksRepairing = always`); backup `main.conf.bak.claude-*`.
2. `bluetooth.service` reiniciado em janela segura (nenhum device BT conectado);
   adaptador subiu soft-blocked → `rfkill unblock bluetooth` + power on. Lista de
   devices limpa, aguardando re-pareamentos (que agora servem de TESTE: o bond
   `<MAC>/info` tem que aparecer em disco).
3. WiFi "Beholder" preso em 5GHz (`nmcli con modify Beholder 802-11-wireless.band a`;
   AP no canal 161). Reverter: `band ""`. Pendente opcional: BSSID lock
   `48:B2:5D:00:00:06` (mata scan de roaming em 2.4G) e extensor USB2 para o dongle BT.

## Pesquisa BlueZ (agentes; detalhes na sprint 2026-07-21-sprint-pesquisa-bluez-estabilidade.md)

- P1/P2 respondidas: candidata preliminar **5.86** — commit `17a227b7` ("device:
  Limit the number of retries on auth failures", backoff no loop de reconexão ≈
  nosso gatilho de crash). 5.87 corrige um bug do próprio retry-limit mas introduz
  UAF em `dev_disconnected` (fix só em git HEAD). A assinatura
  `malloc(): unaligned fastbin chunk detected 2` é **inédita publicamente** — somos
  os descobridores; capturar coredump antes de subir versão. Correção de registro:
  LP #2137758 é SIGSEGV em `btd_service_connecting_complete`, não "HIDP heap
  corruption" (memória antiga trocou a bola).
- Caminho de input BT hoje = **uhid** (`hidp.ko` nem carrega; input.conf default,
  `UserspaceHID` default true ≥5.73). `UserspaceHID=false` deixaria o input imune a
  crash do bluetoothd, mas quebra o filtro anti-vpad por phys/uniq — trade-off em
  aberto, decidir junto com a versão.
- P4/P6 respondidas (resultados completos na sprint doc): mecanismo dos bonds
  temporários confirmado no fonte (`store_device_info` gated por `!temporary`;
  só o D-Bus `Pair()` explícito promove de forma direta → **playbook: sempre
  `bluetoothctl pair <MAC>`**, `trust` não persiste); `Restart=on-failure` já vem
  ativo no nosso pacote; plano em camadas: install idempotente + `WatchdogSec=30`
  + snapshot de bonds com restauração MANUAL + watchdog de journal rate-limitado
  + captura forense opt-in (o core_pattern do Pop é apport, que ignora pacote
  fora da distro — por isso nunca houve dump).

## Fios operacionais imediatos

1. **Não trocar máscara/modo nativo com jogo aberto** (destrói a sessão; fantasma ↑).
   Fix de produto candidato: GUI avisar/impedir com sessão ativa + daemon enviar
   estado neutro ao vpad antes de destruí-lo.
2. Re-parear 8BitDo (botão pair) e Nintendo Pro (SYNC — testa o patch DKMS 0002) e
   DualSense (PS+Create) e **verificar o bond em disco** após cada um.
3. Teste limpo da máscara dualsense em USB (jogo aberto só depois do vpad).
4. Medição A/B WiFi on/off com receita do agente kernel/EMI (btmon + hidgap + l2ping)
   se a intermitência BT persistir após o pin de 5GHz.
