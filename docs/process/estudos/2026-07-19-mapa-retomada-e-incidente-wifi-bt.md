# Mapa consolidado de retomada — hefesto-dualsense4unix (2026-07-19, HEAD 27b51d5)

Síntese de 13 leitores (estudos 16–19/07, sprints, frota coop-4p, memórias, código do HEAD e journal ao vivo do boot 14:35 de hoje). O leitor de journal/estado-vivo MEDIU o incidente desta noite — suas medições dominam o ranking da seção 4.

---

## 1. Regras invioláveis e decisões vigentes

### Guerra de escritores / Proton / wrapper
- **PROTON_DISABLE_HIDRAW=0x054C/0x0CE6 (nunca incluir 0x0DF2)**; PROTON_ENABLE_HIDRAW aposentado — winebus dos Protons 10/11 expõe Sony por DEFAULT e só lê a lista DISABLE; o vpad Edge PRECISA do hidraw (canal de rumble/triggers/lightbar do jogo).
- **Única launch option permitida = `hefesto-launch %command%`**; toda env vive DENTRO do wrapper fail-safe (daemon morto → nenhuma env → pior caso duplicado) — launch option persistida com IGNORE é VENENO (zero controles, 16/07).
- **Keepalive neutro**: sem rumble nosso os bits de vibração saem DESLIGADOS; transição ativa→0 emite UM report de stop — o keepalive 0.5s com flag0=0xFF zerava o rumble do jogo em ≤0.5s.
- **Report BT 0x31 montado por nós** (builder próprio: [1]=seq<<4 por-handle, [2]=tag 0x10, CRC seed 0xA2) e **sempre JUNTO do keepalive neutro** — o 0x31 malformado da pydualsense era bug-PROTETOR; consertá-lo sozinho mataria o rumble BT do jogo.
- **REPLICA-03**: replicação integral do output do jogo vpad→físico (rumble, triggers, lightbar, player-LEDs) com política "jogo vence enquanto a sessão uhid está aberta; paleta/perfil voltam no UHID_CLOSE" — o número no DualSense em jogo é O DO JOGO por decisão explícita (gamepad.py:256-259).
- **Modo Nativo = output_mute total** (nem keepalive, nem sysfs LED) — o jogo é o dono; expor o físico é o objetivo do modo.
- **"Duplicado > zero controles" é lei** — nenhum hide/dedup jamais é pré-condição para o jogo ter controle.

### Lightbar / LED / BT DualSense
- **LIGHTBAR-BT-NEVER-01**: por BT a pydualsense NUNCA escreve LED (suprimida permanente); rota de cor BT é sysfs do kernel — a rota pydualsense BT apagou AS DUAS lightbars ao vivo.
- **_suppress_leds nasce True** e **toda adoção BT envia Reset LED state (flag1=0x08)** antes do reassert — a adoção em si (abertura + feature-reads) derruba o claim da lightbar no firmware; só power-off curava; 0x08 é o que o SDL faz e o kernel define mas nunca usa.
- **Cache do SysfsLedNode.set_rgb** (skip de escrita igual à última bem-sucedida; invalidate no fim de sessão de jogo) — o reassert incondicional a cada 30s causava o flash azul periódico. *Limitação conhecida: o cache NÃO detecta escritor estrangeiro (ver S5).*
- **Falha de UM device não aborta o connect()** — um erro pontual não pode impedir o reassert dos demais.

### Externos (Nintendo / 8BitDo)
- **EXT-04**: leitura de inventário IPC é 100% PURA; LED de externo escrito SÓ pelo tick ~2s do daemon, com cache por-valor + rate-limit 2s/dispositivo — leitura-com-efeito-de-escrita + poll de 4s da GUI estourou joycon_enforce_subcmd_rate e o hid-nintendo DESREGISTROU o 8BitDo BT.
- **Externos passam DIRETO ao jogo, sem vpad** (gyro nativo deles) — dar vpad a externos reverteria o design 8BIT-02 e herdaria a fragilidade do hid-nintendo sem ganho.
- **Ficha do externo é read-only, sem dropdowns** (veto 8BIT-02: bug de foco do cosmic-comp) — modo Nintendo/Xbox é troca de HARDWARE por combo no controle (8BIT-05 = decisão humana).
- **OUI é a fonte da verdade de identidade** (E4:17:D8=8BitDo, E0:F6:B5=Nintendo real), nunca ordem de barramento.
- **Nintendo/8BitDo estáveis = CABO ou X-input** — hid-nintendo em BT é muro de kernel sem knob (modinfo: zero parâmetros).

### Numeração / identidade
- **Estabilidade VENCE compactação (D2)**: disconnect RESERVA o slot ao MAC; renumeração só quando a sessão DualSense esvazia (zero conectados); externos NUNCA expiram nem renumeram — racional: "LED mudava sozinho" e "o PS5 numera por sessão". S2 é comportamento projetado do lado do daemon.
- **Espaço de numeração único best-effort**: externo numera acima do maior slot DualSense; DualSense novo pula slots detidos por externos (reserve providers bidirecionais) — só evita colisões NOVAS, nunca renumera quem já tem slot.
- **Vpad nunca ganha slot** (prefixo MAC 02fe rejeitado) e **slot de exibição ≠ player_index do co-op** (D3) — slot repetido no MAC do vpad daria -EEXIST no probe uhid.
- **Co-op**: primário é SEMPRE player 1; secundário ganha menor índice livre ≥2; índice de quem sai é REUSADO; vpad de secundário só nasce com EVIOCGRAB confirmado.
- **Nunca ancorar lógica por-controle em CONTROLLER_CONNECTED** (só dispara offline→online do backend inteiro); ponto certo = reconcile de hotplug.

### Vpad / gyro / motion
- **Vpad é SEMPRE Edge 054c:0df2 com blueprint 100% sintético** (descriptor 289B + features fossilizadas + MAC forjado 02:fe:...:0N) — ler o físico ao nascer falha em BT (firmware adormecido, EIO).
- **Gyro-via-vpad é SÓ DualSense (GYRO-01, entregue no HEAD)**: PhysicalReportReader = 2º fd O_RDONLY no hidraw físico, cópia VERBATIM da janela payload[15:40] (gyro+accel+sensor_timestamp+2 touch points), reader é o relógio, throttle 250Hz, calibração 0x05 do físico carimbada no blueprint com fallback canônico — evdev como fonte foi refutado (sem sensor_timestamp, valores já calibrados).
- **GYRO-FD-01**: só a própria thread do reader fecha o fd (sinalização por flag + self-pipe) — fd reciclado sob select = reader drenando fd alheio.
- **GYRO-02 (ligar IMU do Nintendo real, subcmd 0x40/0x01) é FASEADO**: doc de risco + protótipo por CABO, envio único na adoção com backoff, kernel-watch armado, identidade por OUI — mesmo território de subcomando que matou o 8BitDo BT.

### Broker (parkado)
- **Broker hide-hidraw PARKADO** (código preservado em docs/process/future-broker/) — o hide por ACL/chmod impede o motion reader (mesmo uid do jogo; DAC não separa) de REABRIR o hidraw → EACCES em loop, gyro morre; + 9 HIGH de robustez na auditoria.
- **Retorno obrigatório = fd-injection**: cmd `open` no broker + fd via SCM_RIGHTS; sequência no hotplug/retarget = nó nasce visível → abre fds (backend+reader) → SÓ ENTÃO hide; **PROIBIDO restore→open→re-hide** (janela de exposição).
- **Validar identidade por HID_ID do uevent do pai HID imediato** (0003/0005:054C:0CE6), NUNCA subindo até idVendor — no BT o pai USB é o adaptador TP-Link.
- Broker só roda DEPOIS de gyro + ondas atuais validadas ao vivo e commitadas; re-auditoria adversarial antes de instalar.

### Install / udev / plataforma
- **Regra de ouro: tudo default no install SEM FLAGS; uninstall simétrico; sudo-zero em runtime; doctor verifica tudo que o install põe** (flags só para opt-out).
- **uaccess só vira ACL em regra <73** (73-seat-late); 77/79 vivem do RUN chmod 0666 (TAG inerte); a 71-uhid foi renumerada de 79→71 exatamente por isso.
- **NUNCA reiniciar o bluetoothd** — derruba os controles BT conectados (provado 17/07); FastConnectable vale no próximo boot.
- **Cmdline gerenciado via kernelstub com registro de DONO** (hefesto/terceiro); **UM token usbcore.quirks= — sempre MERGE**, nunca segundo token; nunca reintroduzir NO_LPM/max_cstate=1/threadirqs.
- **USB power via udev, não tmpfiles.d** (regras 81 devices por vendor+classe e0, e hosts xHCI classe 0x0c03*); **btusb enable_autosuspend=0 via modprobe.d** (default do módulo é Y = furo).
- **Proton PINADO** (GE-Proton10-34, SHA256 + CompatToolMapping) — a semântica winebus mudou entre Proton 9→10; upgrade só deliberado.
- **Game Mode**: wrapper pede Performance ao system76-power via D-Bus e RESTAURA no exit, best-effort, nunca bloqueia o jogo.
- **btmon vetado em produção**; proxy de rádio sujo = contadores hci snapshotados pelo kernel-watch ([USB-71]/[JOYCON]/[BT-HCI]/[XHCI]/[BT-ERR]).
- **Doctor é read-only** (exceto --fix); ASPM reportado SEMPRE pelo /proc/cmdline (a policy sysfs MENTE com pcie_aspm=off).

### GUI / processo / gates
- **GDK_BACKEND=x11 em COSMIC** (cosmic-epoch#2497) e toda toplevel com a classe `hefesto-dualsense4unix-window` — sem ela, XSettings aponta Yaru não-instalado → Adwaita claro.
- **Gate local = `pytest tests/` completo com 0 skipped** + ruff 0.15.20 pinado + mypy + check_anonymity; testes de GUI nunca importam gi no topo (CI headless quebra na coleta); CI só roda tests/unit (furo conhecido).
- **Não reiniciar o daemon de produção durante o dev** — ciclo install+restart UMA vez na validação final; **escolher o modo ANTES de abrir cada célula de teste, nunca mid-game** (recriar vpad invalida handles do jogo — provado: Steam nunca reabriu o hidraw6).
- **Registro de falha de gate ao vivo**: daemon em --foreground + dmesg -w, nunca journalctl --user; anexar lsof dos hidraws + hciconfig.

---

## 2. Fatos medidos e becos refutados (NUNCA re-pesquisar)

### Medições do incidente de HOJE (journal do boot 14:35, leitor ao vivo)
- **Timeline**: 14:37:40 branco USB=slot 1 azul; 14:38:48 Pro BT=slot externo 2; 14:39:04 8BitDo=slot externo 3; 14:39:50 roxo BT=slot 4, coop P2; 14:42:17 **Steam abre**; 14:42:31 cliente Steam escreve player_leds+lightbar nos vpads (uhid_replica_ativa) = escritor comprovado 14s pós-start; **14:43:37 dongle WiFi Archer T3U (2357:012d, rtw88_8822bu) enumera pela 1ª vez no MESMO bus USB2 do adaptador BT**, re-enumera SuperSpeed; **14:43:46 WiFi associa ao AP e NO MESMO SEGUNDO o Pro BT perde ~2700 IMU reports (~40s de rádio mudo)**; 14:44:57–14:45:00 roxo BT morre; 14:52/14:55 Pro reconecta e morre com loop de `timeout waiting for input report` + 3× `joycon_enforce_subcmd_rate: exceeded` (S4).
- **A queda dos BT correlaciona com a ativação do dongle WiFi, NÃO com o start do processo Steam** (80s de rádio saudável entre os dois eventos).
- **Cliente Steam escreve LEDs nos físicos**: lightbar do branco AGORA em multi_intensity `0 64 0` (VERDE) + player-1/3/5 (padrão player 3), com o registro do hefesto dizendo branco=slot 1 e o cache do daemon acreditando em azul — escritor estrangeiro comprovado; vpad P1 também reescrito por fora.
- **controllers.json intacto durante o incidente**: slots={branco:1, roxo:4}, externals={Nintendo:2, 8BitDo:3} — SEM colisão no registro; a colisão de S5 é só na exibição física.
- **S3 medido**: NÃO existe hidraw 0005:054C:0CE6 no sistema — o roxo "conectado" está sem sessão HID (bond/SDP quebrado); sem hidraw NINGUÉM escreve LED; azul = default do firmware.
- **REFUTADOS hoje**: PSSupport re-ativado (vdf ao vivo = 0, Switch/Xbox/Generic ausentes); guard (--apply-quiet adia com Steam viva), autoswitch (suprimido por override) e daemon (vivo o incidente inteiro) como atores do S1; WARN 15:01 é path_noexec de Wine, sem relação com BT.

### Protocolo / kernel DualSense
- Offsets do payload 0x01 (0-based pós report-id): gyro 15-20, accel 21-26, sensor_timestamp le32 27-30 (0,33µs), touch points 32-35/36-39 (byte de contato INVERTIDO, 0x80=sem toque); status 52; USB 0x01=64B base 1; BT 0x31=78B exatos base 2, CRC-32 nos 4 finais. Seeds CRC: input 0xA1, output 0xA2, feature 0xA3.
- Taxas MEDIDAS: DualSense USB 250Hz, BT **765Hz** (3× a suposição antiga); poll loop do daemon 60Hz; motion pipeline validado no firmware real (400/400 CRC ok, accel 0,96g parado).
- Report BT 0x31 da pydualsense 0.7.5 é MALFORMADO ([1]=0x02 fixo, [2]=0xFF) → firmware descarta → todo output BT nosso era no-op (por isso o roxo vibrava: o keepalive era no-op).
- Adoção BT derruba o claim da lightbar: 330k escritas sysfs corretas NUNCA acenderam; re-parear NÃO cura, rebind NÃO cura, SÓ power-off; P2 sozinho no adaptador não acendeu (contenção de banda REFUTADA); cura = Reset 0x08 (o que o SDL manda).
- DualSense BT ocioso EMUDECE: 33/33 GET_REPORT EIO na janela de sono vs 150/150 ativo; janela dura MINUTOS (retry ≤8s = morto); BlueZ jura Connected: yes; é o CONTROLE, não o link.
- Escrita hidraw crua NÃO atualiza a classe LED do kernel (sysfs lia azul com barra fisicamente verde); kernel no probe ZERA multi_intensity e acende azul por fora da classe; KERNEL_DEFAULT_BLUE=(0,0,128).
- Vpad uhid: input report de 63B de payload ou o kernel descarta CALADO; MAC 02:fe duplicado = -EEXIST; UHID_START não é probe OK; kernel numera jogadores contando físicos+vpads (o probe do hid_playstation emite player-LED próprio — filtrado pela graça de 0.5s do REPLICA-03).

### Nintendo / 8BitDo
- Assinatura de morte hid-nintendo BT: cascata `timeout waiting for input report` → `joycon_enforce_subcmd_rate: exceeded` (função hardcoded, SEM parâmetro de módulo); morte provada SEM Steam e SEM código nosso na cadeia; gate do doctor = ≥10 timeouts antes do exceeded (3× exceeded com 1 timeout não é terminal).
- IMU do Nintendo Pro REAL em STANDBY (accel 0,0,0 congelado = sensor desligado; hid-nintendo lê factory cal mas não liga o sensor); 8BitDo modo Switch = IMU nativa VIVA (nada a fazer).
- Clone DS4 054C:05C4 pareado = storm de 211k CRC fails degradando o adaptador para TODOS (é quase certo um 8BitDo em modo D-input; desambiguar por OUI + hw_version=0x00000000); fundo aceitável = 2–39 CRC/boot.
- xpad é USB-only (zero aliases hid) — X-input por BT não existe de verdade.
- 8BitDo no CABO desde 18/07 ~22h = 2º "Pro Controller" USB 057e:2009 nas validações.

### Proton / Steam
- winebus Proton 10/11 abre hidraw da família Sony POR DEFAULT (lsof: winedevice com hidraw3/6/7/8 sem env); IGNORE do SDL NÃO filtra o caminho winebus; PROTON_ENABLE_HIDRAW morreu no Proton 10 (só AMPLIA exposição); PROTON_DISABLE_HIDRAW confirmada nas strings do winebus.sys do GE-Proton10-34.
- O cliente Steam roda FORA do wrapper: nenhuma env nossa o alcança; ele abre e ESCREVE em todo hidraw acessível (uaccess nosso + steam-devices cobre 057E:2009 BT e 054C:05C4).
- FATO 0 de 18/07: o jogo rodou SEM o wrapper (binário fora do PATH; LaunchOptions sem hefesto-launch); dedup_ok:true era falso-tranquilizante; launch_env/default.env de hoje: envs corretas, last_run vazio (nenhum jogo via wrapper neste boot).
- Steam Input: disable_steam_input.sh zera SÓ PSSupport e UseSteamControllerConfig — SwitchSupport/XBox/Generic ficam no default Valve.

### Numeração (design confirmado no código)
- TRÊS autoridades internas (identity DualSense, external registry, coop player_index) + a numeração DO JOGO/Steam; nenhum canal cruza exibição entre elas; durante sessão uhid os DualSense exibem o número DO JOGO e os externos SEMPRE o do daemon.
- mark_disconnected não tem chamador — desconexão detectada só pelo diff do tick de ~2s; resolve_player_numbers com co-op OFF rotula todos como jogador 1.
- ExternalLedSync: cache por-VALOR do nosso slot — se terceiro escreve o LED, o daemon NÃO repinta (slot não mudou → skip).
- Fallback posicional de exibição de externos = ds_count+índice+1 (só quando o registry não opinou) — re-embaralha; o registro não.

### Rádio / USB / máquina
- Adaptador BT TP-Link 2357:0604 (RTL8761BU) em Bus003 Port1; **dongle WiFi Archer T3U na porta vizinha do MESMO xHCI**; 2 receivers Compx 2.4G no mesmo painel; RSSI do DualSense BT medido -72dBm (margem baixa); tela Bluetooth do cosmic-settings aberta mantém Discovering=yes contínuo (rouba banda ACL).
- btusb enable_autosuspend=Y é o default do módulo (furo, agora coberto por modprobe.d próprio); system76-power seta med_power_with_dipm em scsi_host mesmo em Performance (sabotador real); TLP/powertop/tuned ausentes.
- Storm -71 = snd-usb-audio enumerando o áudio USB do DualSense (A/B provado, PORT-INDEPENDENTE) — NUNCA atribuir a BIOS/cabo/porta/I-O-die (3 memórias antigas SUPERSEDED).
- BR/EDR: não há "botão BT mais rápido" no BlueZ para link já conectado; debugfs conn_intervals são LE, não se aplicam; input.conf IdleTimeout=0 já é o máximo; hid_playstation e hid_nintendo têm ZERO parâmetros de módulo.
- Polling: DualSense USB bInterval 6 = 250Hz; Pro/8BitDo cabo = 125Hz (único candidato a jspoll, e jspoll é GLOBAL + unidade vira expoente em high-speed — só com benchmark+replug).

### Becos refutados (lista canônica)
1. PROTON_ENABLE_HIDRAW=1 como cura de dedup — ampliava exposição.
2. SDL_GAMECONTROLLER_IGNORE_DEVICES como filtro suficiente — winebus ignora.
3. udev ID_INPUT_JOYSTICK=0 para desduplicar — HIDAPI lê /dev/hidraw direto.
4. Retry/backoff ≤8s para EIO BT — a janela dura minutos.
5. Contenção de banda BT como causa da lightbar — P2 sozinho não acendeu.
6. Re-parear/rebind para curar o claim da lightbar — só power-off (pré-0x08).
7. Pintar secundário via pydualsense BT — apagou as duas lightbars.
8. Policy sysfs de ASPM como verdade — mostra [default] com pcie_aspm=off.
9. Validar identidade por idVendor subindo a cadeia no BT — acha o adaptador TP-Link.
10. chmod 000 do físico (sprint dedup) — derrubava o próprio daemon (mesmo uid reabre).
11. evdev como fonte de motion — sem sensor_timestamp, valores já calibrados.
12. Gêmeo colapsado no SDL como 2ª causa RDR2 — 4 HID_UNIQ distintos; SDL casa por serial.
13. CRC/rádio como 2ª causa RDR2 — 2 fails em 3,5h, hci errors 0.
14. Dropdown de modo do externo "sumiu" — nunca existiu (9532eb1 é read-only por design).
15. Supressão do 62483b2 engolindo rumble; report_threads mortos; autoswitch pintando LED — todos inocentados por medição.
16. Storm -71 como defeito de HW/porta/cabo/BIOS — é config de áudio (SUPERSEDED ×3).
17. Força-bind hid-generic para 8BitDo — descriptor clone malformado, falha.
18. "Steam segurando hidraw" como detector de morte do Nintendo — Steam segura hidraw de TODO controle suportado.
19. **HOJE**: PSSupport reativado, guard, autoswitch e daemon como causas do S1 — refutados por vdf + journal.
20. Strip cego de SDL_JOYSTICK_HIDAPI=0/PROTON_ENABLE_HIDRAW de launch options alheias — proibido (legítimas na máscara Xbox); só tokens co-ocorrendo com IGNORE na mesma linha.

---

## 3. Pendências ordenadas (com dependências)

**0. Imediato (antes de qualquer onda)** — sem dependências:
- Re-parear o DualSense roxo (bond/SDP quebrado: remove+pair+trust+PS) — cura direta do S3.
- A/B do dongle WiFi: repetir a abertura da Steam com o Archer T3U despluggado/realocado (extensor USB2, controlador oposto); confirmar a banda do BSS 48:b2:5d:00:00:06 (iw ausente na máquina — instalar/medir).
- Gates humanos da leva atual: power-off + lightbars permanecem (Reset 0x08); gyro do vpad em jogo real (evtest event27/28 + gyro aiming, branco USB e roxo BT); rumble+layout PS; convivência com REPLICA-03.

**1. Onda R — rádio robusto (NOVA, promovida pelo incidente de hoje)** — depende das medições do item 0:
- Coexistência dongle WiFi×BT: posição física (extensor ≥20cm, fora da sombra do gabinete, longe de porta USB3), btcoex do rtw88, canal/banda do AP; Wi-Fi USB despluggado durante co-op como mitigação imediata.
- INVESTIGAR-MAIS do estudo BT: JustWorksRepairing=confirm (curaria o padrão SDP), LinkSupervisionTimeout [BR], sniff/page-scan finos, usbhid.jspoll (protocolo benchmark+replug definido e nunca executado) — todos SÓ com medição de campo.
- Trust do DualSense (Trusted:no hoje), vigiar clone 05C4, calibrar regexes [XHCI]/[BT-HCI] do kernel-watch antes de alarmar leigo.

**2. Onda N — numeração una + posse de LED** — depende de decisão de produto (hoje "o jogo vence" só vale para DualSense):
- Unificar/reconciliar as autoridades (identity, external, coop, exibição GUI) e definir postura frente à numeração da Steam pintada nos LEDs (adotar o número do jogo também para externos OU reassertar o nosso em todos).
- Reassert que detecta escritor estrangeiro: re-ler o sysfs antes do skip_cache (hoje o cache acredita em azul com o LED verde); ExternalLedSync idem.
- Corrigir o fallback posicional ds_count+índice+1; lock único + validação cruzada de namespaces no load do controllers.json (TOCTOU/lost-update entre os dois registries); assimetria auto_player_colors OFF (DualSense some, externo continua).

**3. Onda S — broker fd-injection (guerra de escritores cap. 2; única cura para o CLIENTE Steam)** — depende de: GYRO-01 validado ao vivo E commitado; ondas atuais estáveis; re-auditoria adversarial antes de instalar:
- Reimplementar com cmd `open` + SCM_RIGHTS (reader nunca reabre por caminho); sequência visível→abrir-fds→hide; lições 2-6 do sprint (restore idempotente, lease resiliente, socket sobrevive a restart sem RuntimeDirectory=, minor-reuse/TOCTOU, install/packaging); refiar os hooks removidos (lista exata em future-broker/README).
- Gates do §10: jogo sem wrapper não abre hidraw3 mas abre hidraw6; kill -9 → getfacl volta em <1s; Modo Nativo mantém exposto; doctor com subseção.
- Aproveitar o já-acertado: validador HID_ID, ACL via os.setxattr byte-idêntica, units hardened, protocolo JSON+SO_PEERCRED.

**4. GYRO-02 — IMU do Nintendo Pro real (subcmd 0x40 arg 0x01)** — depende de: rádio estável (Onda R) + kernel-watch [JOYCON] armado:
- Doc de risco + protótipo por CABO; confirmar formato do pacote rumble+subcmd no kernel local; envio ÚNICO na adoção com backoff (nunca loop); identidade por OUI.

**5. BT-07 / 2ª causa RDR2** — depende de: wrapper validado no PATH; rádio estável (para não confundir causas):
- Matriz de 7 células (Sackboy 1599660 / RDR2 1174180 × USB/BT × modos) com daemon --foreground + dmesg -w; A/B da célula #7 (PSSupport 0→1; Steam Input por-jogo; modo vpad); refazer células #2/#5 (rumble BT) agora que 0x31+keepalive neutro entraram; verificar wrapper_used/dedup no state_full em cada célula. Só validação ao vivo fecha.

**6. Touchpad completo + resto do motion** — depende do gate humano do GYRO-01:
- Touchpad 2 dedos já flui na janela 32-39 do forward_motion (validar em jogo); externos não têm touchpad físico (fora de escopo salvo pedido); avaliar peso de 4 vpads a 250Hz no /dev/uhid; cache do 0x05 por MAC lido em sessão USB (mitigação BT).

**7. Higiene / instalador (FUT-04 + achados do leitor de install)** — sem dependências, oportunista:
- disable_steam_input.sh cobrir SteamController_SwitchSupport (ligado à decisão da Onda S); hefesto-dsx-recover.service (decidir: default, opt-in ou remover asset); storm.conf órfão no `--keep-udev`; texto/flag `--disable-usb-audio` no install.sh; TAG uaccess inerte nas 77/79; rm compensatório 73/74 sai no próximo release; CI incluir tests/core; faixa cega de ~120-140 testes GUI; venv legado; 45 violações de acentuação; expor ff_play_count POR vpad no state_full.

---

## 4. Sintoma → hipóteses ranqueadas

### S1 — Abrir a Steam derrubou Nintendo Pro BT e DualSense roxo BT
1. **[CONFIRMADA POR MEDIÇÃO — mais forte] Interferência do dongle WiFi USB, não a Steam em si.** O Archer T3U (rtw88) enumerou 80s APÓS o start da Steam, no bus USB2 vizinho do adaptador BT, saltou a SuperSpeed e associou ao AP às 14:43:46 — no MESMO segundo o Pro BT perdeu ~2700 IMU reports; o roxo morreu 14:45:00. Entre 14:42:17 (Steam) e 14:43:37 o rádio esteve saudável. A Steam entra na cadeia porque abri-la leva ao uso do dongle. Evidência: journal -k do boot 14:35 (plug 2357:012d + assoc + "compensating for 2700 dropped IMU reports"); daemon coop_player_removed 14:45:00. **Verificação ao vivo**: abrir a Steam com o dongle despluggado (BT não deve cair); replugar o dongle com controles BT ativos (queda deve reproduzir); confirmar banda do BSS.
2. **[MÉDIA — contribuinte comprovado como escritor, não como assassino] Cliente Steam abre e escreve em todos os hidraws acessíveis** (uhid_replica_ativa nos vpads 14s pós-start; LEDs do branco reescritos; steam-devices dá uaccess ao Pro BT 057E:2009) — escritor extra de subcomandos/feature-reads num link BT frágil; nenhuma env nossa alcança o cliente (era o papel do broker parkado). Evidência: journal daemon 14:42:31-32; /usr/lib/udev/rules.d/60-steam-input.rules; scripts/disable_steam_input.sh:178-179 (só zera as 2 chaves PS). **Verificação**: abrir Steam sem dongle WiFi e monitorar hciconfig errors + journal -k pela cascata do hid-nintendo — se BT sobreviver, a Steam sozinha não derruba.
3. **[FRACA — terreno, não gatilho] Margem RF crítica e reconexão frágil**: RSSI -72dBm, 3 rádios no painel traseiro, Discovering=yes se a tela BT do COSMIC estiver aberta; Trusted:no + FastConnectable recém-instalado tornam a queda persistente em vez de blip. Evidência: docs/process/estudos/2026-07-18-estudo-bt-maximo.md:150-188. **Verificação**: RSSI antes/depois de realocar antena/dongle; `bluetoothctl info` (Trusted) nos dois controles.

### S2 — Numeração não se reajustou após as quedas (cabo virou 3, 8BitDo virou 1)
1. **[CONFIRMADA POR MEDIÇÃO + DESIGN] O daemon nunca renumera (D2) E os números que ela viu eram DA STEAM.** O registro ficou intacto o incidente inteiro (branco=1, roxo=4 reservado, externos 2/3 — controllers.json ao vivo); disconnect RESERVA slot (identity.py:269-319) e externos nunca expiram (external_identity.py:157-176). O "cabo=3 / 8BitDo=1" é a Steam re-enumerando após as quedas e pintando os LEDs por hidraw; o ExternalLedSync não repinta porque o cache é por-valor do NOSSO slot (external_identity.py:334-335) e a camada GAME entrega o número do jogo aos DualSense por decisão (gamepad.py:250-268). **Verificação**: no próximo incidente, comparar controllers.json + journal (nenhum evento de renumeração) contra os LEDs físicos; fechar a Steam → UHID_CLOSE deve devolver a paleta dos DualSense; o LED do 8BitDo NÃO deve ser corrigido pelo tick (prova do cache) até invalidação/replug.
2. **[SECUNDÁRIA] Fallback posicional da exibição de externos** (ds_count+índice+1 quando o registry não opinou, ipc_handlers.py:194-208/1198-1211) re-embaralha os números na GUI quando ds_count muda. **Verificação**: GUI aberta durante queda BT; cards devem divergir do LED físico só nesse caminho.

### S3 — DualSense roxo reconectado: lightbar azul, sem player LED/número
1. **[CONFIRMADA POR MEDIÇÃO — mais forte] Reconexão BT SEM sessão HID (bond/SDP quebrado).** Não existe NENHUM hidraw 0005:054C:0CE6 no sistema; o kernel não criou hidraw/input; o daemon não tem o que adotar (nenhum log pós-14:45) e ninguém consegue escrever LED — azul é o default do firmware. Padrão conhecido "Connected: yes sem hidraw" (reference_dualsense_bt_repair_sdp). Evidência: listagem /sys/class/hidraw ao vivo; journal daemon 14:45→15:11. **Verificação/cura**: `bluetoothctl` remove+pair+trust + botão PS; hidraw deve nascer e a adoção pintar slot 4 (rosa) + player LEDs.
2. **[LATENTE — vale para reconexões COM hidraw] Priming sem desired**: nó novo com cor resolvida None → escreve KERNEL_DEFAULT_BLUE e player-LEDs SÓ se desired.player_leds is not None; supressão pydualsense é permanente em BT — azul sem player é a assinatura desse caminho (backend_pydualsense.py:1217-1238, 1185-1202). **Verificação**: journal deve mostrar adoção + reassert; sysfs multi_intensity = 0 0 128 vs cor de slot.
3. **[FRACA] Camada GAME rançosa reaplicada no hotplug** (sobrevive à desconexão, backend_pydualsense.py:1854) se o UHID_CLOSE não veio — número/cor de jogo fechado reaparecendo. **Verificação**: state_full com sessão uhid aberta sem jogo.

### S4 — Nintendo Pro BT conecta, mostra player 2, desconecta
1. **[CONFIRMADA POR MEDIÇÃO — mais forte] hid-nintendo desiste por timeouts de ACK sob rádio degradado (o mesmo dongle WiFi do S1).** Reconexões 14:52/14:55; a NOSSA escrita única e rate-limitada de LED colou ("player 2" = external_led_written slot=2); em seguida loop de `timeout waiting for input report` + 3× `joycon_enforce_subcmd_rate: exceeded` → driver desregistra. O assassino é o rádio, não nosso volume (EXT-04 já limita a 1 escrita/2s). Evidência: journal -k 14:52-14:56; external_identity.py:1-30,59-64. **Verificação**: reconectar o Pro por BT com o dongle WiFi fora — deve estabilizar; `journalctl -b -k | grep -E 'timeout waiting|subcmd_rate'` (gate ≥10 timeouts).
2. **[MÉDIA] Escritor extra do cliente Steam no hidraw do Pro BT** (uaccess do steam-devices; init/identificação vira subcomando concorrente). Evidência: 60-steam-input.rules cobre *057E:2009*; doctor.sh:1210-1216. **Verificação**: A/B com Steam fechada×aberta, dongle fora nas duas.
3. **[CONSTANTE DE FUNDO] Muro do kernel**: sem knob de módulo; nada nosso cura o transporte — rota estável = CABO/X-input; robustez real exigiria patch de kernel (alinhado ao S6).

### S5 — 8BitDo=3 e DualSense branco=3 (verde); roxo azul sem player
1. **[CONFIRMADA POR MEDIÇÃO — mais forte] Duas AUTORIDADES pintando LEDs; não há colisão no registro.** A Steam numerou o branco como player 3 DELA e escreveu VERDE + padrão 1/3/5 direto no hidraw (sysfs input12 = `0 64 0` AGORA, com controllers.json dizendo branco=slot 1 e o cache do daemon acreditando em azul); o hefesto acendeu o slot 3 legítimo no 8BitDo. Verde é a cor de player 3 nas DUAS paletas (led_control.py:123-128), o que mascara a autoria. O reassert não corrige porque skip_cache não re-lê o sysfs. Evidência: /sys/class/leds/input12*; controllers.json ao vivo; log lightbar_reassert_skip_cache rgb=(0,0,255). **Verificação**: fechar a Steam (UHID_CLOSE) → paleta deve voltar (azul no branco); `cat multi_intensity` antes/depois; se não voltar, o gap é o cache (fix da Onda N).
2. **[SECUNDÁRIA — estrutural, não foi o caso hoje] Colisão interna possível por construção**: TOCTOU entre os dois registries com locks separados (identity.py:243-254 × external_identity.py:132-141), lost-update no controllers.json (dois escritores RMW) e load sem cross-check de namespaces. **Verificação**: teste de estresse conectando DualSense e externo simultaneamente; inspecionar controllers.json após.
3. O roxo azul sem player = mecanismo do S3 (sem hidraw, fora de todas as numerações) — e por estar invisível à Steam, desloca a numeração DELA sobre os demais.

---

## 5. Lacunas (nenhum leitor cobriu; merece leitura/medição)

1. **Banda do BSS 48:b2:5d:00:00:06** (2.4GHz ch11 × 5GHz) — `iw` ausente/sem saída na máquina; é O dado que fecha ou reabre a hipótese nº1 do S1.
2. **Contribuição isolada do cliente Steam sobre links BT** — nunca instrumentada com o dongle WiFi fora do ar (todas as medições de guerra de escritores foram com winedevice/Proton ou com o WiFi ativo). A/B limpo pendente.
3. **Driver rtw88_8822bu**: opções de coexistência (btcoex), disable_lps etc. — nenhum leitor leu o driver/modinfo do dongle WiFi.
4. **Detecção de bond quebrado ("Connected: yes sem hidraw")** — nem daemon nem doctor têm check para o estado do S3; o daemon não loga nada quando um DualSense BT reconecta sem criar hidraw. Candidato: check no doctor + evento no journal + aviso na GUI.
5. **Reassert com re-leitura do sysfs** (detectar escritor estrangeiro antes do skip_cache) — decisão e custo não estudados; nenhum leitor mediu a frequência segura de re-leitura.
6. **Efeito real de zerar SteamController_SwitchSupport** no cliente (para de abrir/escrever o hidraw do Pro/8BitDo?) — nunca testado; hoje a chave nem existe no vdf (default Valve).
7. **Estado da GUI durante o incidente** (cards player × player_slot, banner wrapper_used, applet) — nenhum leitor olhou a exibição ao vivo; e a faixa cega de ~120-140 testes GUI headless + tests/core fora da CI persistem.
8. **Validação em jogo do GYRO-01/touchpad** (gate humano): evtest confirma nós, mas nenhum jogo com gyro aiming foi jogado; convivência forward_motion × REPLICA-03 sob carga 4P não medida.
9. **Telemetria por-vpad no state_full** (ff_play_count/motion_hz por jogador) — estado pós-27b51d5 não confirmado por nenhum leitor.
10. **kernel-watch no incidente de hoje** — ninguém conferiu se [JOYCON]/[BT-ERR] flagraram a cascata de 14:55 (calibração dos regexes contra caso real).
11. **controllers.json**: nenhum teste cobre lost-update entre os dois escritores RMW nem colisão gravada em disco ressuscitada no restart.
12. **MACs reais em docs/process/estudos/2026-07-16-*.jsonl** — quebra de anonimato latente; scrub pendente de decisão da mantenedora.
