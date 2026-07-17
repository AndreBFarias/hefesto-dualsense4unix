# Sprint 2026-07-16 — Bluetooth: o vpad mudo (blueprint sintético mata a dependência do físico)

**Status (2026-07-17): BT-01/BT-02 construídos na Fase 1 (`bc68718` — blueprint
sintético, uinput 0df2); BT-04 (a)+(b) implementados na Fase 1 e (c) SUPERADO pela nota
de resolução abaixo; BT-03 construído em 2026-07-17 (vpad_backend+vpad_motivo por
controle no state_full, badge no card da aba Status, evento `vpad.degraded` no bus).
BT-06 SEGUE GATEADO de propósito: a remoção automática da option NÃO foi ligada (o
caminho suportado virou o wrapper `hefesto-launch` da Fase 2 + migração do vdf no
install/GUI; doctor e compose_launch já não recomendam o veneno). Pendente: BT-07
(gate humano — Sackboy/RDR2 por BT, matriz com máscara Xbox).** Frente do Estudo 1
(117 agentes) + relato ao vivo da Vitória ("em BT nada funciona"), com revisão
adversarial em 3 lentes já incorporada. Branch `sprint/harmonia-uhid`.

## TL;DR

O vpad uhid precisa LER 3 feature reports (0x05/0x09/0x20) do DualSense físico na hora de nascer.
Por Bluetooth, com o controle ocioso na mesa, o firmware do controle emudece (BlueZ segue dizendo
"Connected: yes", gyro emite ZERO eventos) e cada `GET_REPORT` estoura o timeout de 5 s do `hidp`
do kernel com EIO — janela que dura MINUTOS, até alguém tocar no controle. O blueprint falha e o
vpad cai para uinput `054c:0ce6`, indistinguível do físico. A launch option
`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` persistida na Steam esconde então físico E vpad
(modo hefesto) ou o físico sem vpad nenhum (modo nativo) = **jogo com zero controles**.

A cura: **o blueprint vira 100% sintético** (descriptor USB canônico + features capturados de um
DualSense real, embutidos no código) — o vpad nunca mais lê o físico, sobe uhid Edge `0df2`
SEMPRE (em BT, em USB, até sem controle) e **o Bluetooth deixa de importar para o vpad**. Junto:
o vpad uinput degradado também vira `0df2` (nunca mais nasce `0ce6`), e a launch option venenosa
é removida da Steam pelo guard — **só depois** que a dedup por udev da frente irmã estiver provada
também no caminho HIDAPI.

**Honestidade obrigatória (as 3 revisões insistiram):** esta frente cura a **cadeia provada**
(Sackboy com a launch option persistida; plausivelmente RDR2 no modo hefesto via vpad degradado).
Ela **NÃO explica** RDR2 + modo nativo + BT (não há launch option no appid 1174180 — verificado;
não há vpad nem grab no nativo). Existe pelo menos uma **segunda causa em aberto**. BT-07 não é
validação decorativa: é o **gate da entrega** e parte da investigação. E o relato do 8BitDo
"descontrolado" **não é tocado por esta frente** — fica para a frente multi-controle.

## O que está provado (e o quê cada prova vale)

### PROVADO AO VIVO (medido nesta máquina, 2026-07-16, reproduzido pelas revisões)

- **A janela de EIO é por estado, não aleatória.** Janela ativa: 150/150 `GET` ok (5-40 ms,
  burst de 120 em 3,8 s). Janela de sono: 33/33 EIO consecutivos de 5,25-5,35 s cada, no MESMO
  `/dev/hidraw4`, com gyro do físico BT emitindo ZERO eventos por 60 s e BlueZ "Connected: yes".
  A revisão técnica reproduziu de forma independente às 15:02 (EIO 5,31 s / 5,12 s; gyro BT
  0 eventos/8 s vs 10.502 do USB ocioso ao lado — ocioso ≠ mudo em USB, o mudo é do transporte BT).
- **A cadeia inteira aconteceu no boot real de hoje**: descriptor BT lido → EIO 0x05 → EIO 0x09 →
  EIO 0x20 (~5,1 s cada) → `uhid_blueprint_sem_mac` → `uinput_device_created flavor=dualsense
  product=0xce6` (13:06:21→13:06:38); às 13:09:22 o MESMO caminho subiu uhid normal.
- **Descriptors reais**: USB = 289 B, sem item `85 31`, **byte-idêntico** (cmp) a
  `captures/dualsense_usb_descriptor_054c0ce6.bin`; BT = 321 B, com `85 31`.
- **Vpad uhid com blueprint de OUTRO controle funciona**: experimento criou vpad com descriptor
  BT + features do outro DualSense → bindou e o input fluiu. Logo: **templates funcionam, nada
  precisa ser lido do físico**.
- **A launch option está persistida em EXATAMENTE UM jogo**: appid 1599660 (Sackboy), linha 914
  de `~/.steam/steam/userdata/1300222895/config/localconfig.vdf`, junto com
  `SDL_JOYSTICK_HIDAPI=0` e `__GL_SHADER_DISK_CACHE*` na MESMA linha. RDR2 (1174180): **zero
  entries** — confirmado por parse independente nas 3 revisões.
- **O boot com BT dormindo bloqueia ~15,7 s** (3 timeouts de ~5,2 s) só para falhar; e no boot
  normal o P1 SEMPRE nasce uinput primeiro (o gamepad sobe antes do `controller.connect`).
- **Rádio 2.4 GHz sujo (secundário)**: 4 `DualSense input CRC's check failed` hoje no dmesg, no
  físico BT (2 receivers wireless + BT no mesmo espectro).

### PROVADO NO CÓDIGO (file:line conferidos pelas 3 revisões — sem alucinação)

- O timeout de ~5 s é o `hidp_get_raw_report` do kernel (transporte BT-HID em uso; `lsmod` mostra
  `hidp` usado; `UserspaceHID` comentado em `/etc/bluetooth/input.conf`).
- `daemon/connection.py:208-231` (reconnect_loop) publica `CONTROLLER_CONNECTED` mas **não** chama
  `upgrade_primary_vpad_to_uhid`; só `daemon/lifecycle.py:390-393` (boot) chama.
- `daemon/subsystems/gamepad.py:296-298`: early-return compara **só o flavor** — re-selecionar
  DualSense na GUI com vpad degradado é NO-OP (os dois backends dizem `dualsense`).
- `integrations/uinput_gamepad.py:84`: o vpad uinput forja `054c:0ce6`; o próprio código admite
  que `IGNORE_DEVICES` "não desduplica". O uhid usa `VPAD_PRODUCT=0x0DF2`.
- `integrations/virtual_pad.py:127-175`: `_try_uhid` **exige** `hidraw_path` — sem físico
  legível, não há vpad uhid, por desenho.

### PRECISÃO DE LINGUAGEM (as revisões corrigiram o estudo — o doc adota a versão corrigida)

- **O fallback NÃO é silencioso no log** (`uhid_feature_read_failed` ×3 +
  `uhid_blueprint_sem_mac` aparecem). Ele é **invisível na GUI/IPC por player** — e o `state_full`
  **já** expõe `gamepad_emulation.backend` do P1 (`ipc_handlers.py:411-426`; o `compose_launch`
  o consome). O gap real: backend POR PLAYER + motivo da degradação + superfície visual.
- **Não cravar o mecanismo do sono BT.** Durante a janela de EIO, o `hcitool con` mostra o ACL
  em modo ATIVO (`lm CENTRAL AUTH ENCRYPT`, **sem** SNIFF). O que está provado é a fenomenologia:
  *o firmware do controle emudece* (não responde features, não emite input) *com o link vivo*.
  Logs, docs e mensagens devem descrever o sintoma medido — "controle BT ocioso não responde
  features; GET_REPORT estoura o timeout de 5 s do hidp" — **não** "sniff/economia de energia do
  link" como fato. (HIPÓTESE FORTE: gerenciamento de energia do firmware; cravar exigiria sniffer.)
- **A prova "journalctl --user 13:06" não é reproduzível nesta máquina**: o daemon roda
  `--foreground` fora do systemd (PID 61637) — os logs estruturados vão para o stdout do processo.
  Nenhum critério de aceite desta frente pode ser "o journal mostra X"; a fonte é o stdout/arquivo
  de log do daemon (ou o journal SÓ quando instalado como serviço).

### REFUTADO / PARCIALMENTE REFUTADO

- **REFUTADO (parcial!) o medo do descriptor BT** (`uhid_gamepad.py:344-355`): vpad uhid criado
  com o descriptor BT de 321 B + `BUS_USB` bindou e o input **ABS** fluiu. MAS a refutação cobre
  **só o fluxo de eixos**: touch points (offsets 32/36) e bateria (offset 52) ficam ALÉM dos
  ~10 B que o report 0x01 do descriptor BT declara e **não foram exercitados** — se truncar, o
  sintoma seria toque fantasma/bateria 5%, invisível num teste de ABS. O doc **não afirma**
  "descriptor BT no vpad é seguro". Para a solução é irrelevante: o blueprint sintético usa o
  descriptor USB canônico e o warning morre como **dead code**, não como "seguro provado".
- **REFUTADO retry/backoff** (alternativa a): a janela dura minutos (≥ ~20 min medidos entre
  estudo e revisão) e cobre exatamente o boot (controle na mesa); cada rodada custa 3×5,2 s
  bloqueando o start.
- **REFUTADO "SDL ≥ 2.24 conhece o Edge"** (risco do estudo original): o suporte ao DualSense
  Edge é da série **2.26** (paddles em dez/2022) e o **mapping evdev Linux do Edge só chegou no
  SDL 2.26.5** (fev/2023). Consequência real documentada no BT-02.
- **REFUTADA a "promoção a uhid no hotplug"** como fix (o BT-04 original): pós-BT-01 a
  viabilidade do uhid deixa de depender do físico (o `hid_playstation` autocarrega por modalias
  na criação do device uhid — `alias: hid:b0003g*v0000054Cp00000DF2` confirmado no kernel desta
  máquina). Chamar a promoção no hotplug nunca conseguirá o que a criação não conseguiu. O item
  foi reescrito (ver BT-04). *(Atualização 2026-07-16: o que segue refutado é vendê-la como fix
  da causa-raiz. Como REDE DE SEGURANÇA para disponibilidade tardia do uhid — ex.: ACL do
  `/dev/uhid` aplicada depois do boot — o call site do `reconnect_loop` FICOU, por decisão do
  VPAD-01; ver a NOTA DE RESOLUÇÃO no BT-04.)*

## O que a causa-raiz NÃO explica (segunda causa em aberto)

O relato dela é "em BT, NENHUM input, em QUALQUER modo, idem RDR2". A cadeia provada explica:

| Cenário | Explicado? |
|---|---|
| Sackboy, qualquer modo, BT (launch option persistida) | **SIM** (cadeia provada) |
| RDR2, modo hefesto, BT | PLAUSÍVEL (vpad degradado 0ce6 = jogo vê DOIS 054c:0ce6, um grabado/morto) |
| RDR2, modo nativo/Sony, BT | **NÃO** — sem launch option, sem vpad, sem grab: o físico deveria funcionar |
| 8BitDo "descontrolado" | **FORA DESTA FRENTE** (frente multi-controle) |

Candidatos para a segunda causa (investigação no BT-07): **Steam Input PSSupport** — que o NOSSO
install zera por default (step 11) com guard que reaplica a cada 30 min; em jogos que dependem do
Steam Input para converter DualSense em XInput, isso participa do sintoma e é interação nossa —,
dedup interno do SDL entre vpad-evdev e físico-HIDAPI, e os 4 CRC fails/dia do rádio 2.4 GHz.
O sprint promete **a cura da cadeia provada**, não "a cura do BT".

## A solução (b + d): blueprint sintético + nunca mais nascer 0ce6

1. **Embutir no código** o descriptor USB canônico de 289 B (o repo já tem o capture, provado
   idêntico ao vivo) + templates dos 3 features **capturados de um DualSense real** (0x05
   calibração, 0x09 MAC — já sobrescrito por player hoje —, 0x20 firmware). Nenhuma leitura do
   físico no caminho de criação. O vpad sobe uhid Edge `0df2` SEMPRE.
2. **Paridade de PID**: o uinput flavor dualsense passa a forjar `054c:0df2` — mesmo degradado,
   o vpad nunca mais é indistinguível do físico, e a regra udev da frente irmã só precisa marcar
   o `0ce6` físico.
3. **Fim da degradação invisível**: backend real POR PLAYER + motivo no IPC, superfície na aba
   Status (dentro da reforma da frente irmã — não uma GUI paralela).
4. **Early-return por (flavor, backend)** com latch anti-churn; aposentar o upgrade de hotplug.
5. **Desenvenenar a Steam**: o guard (default no install, opt-out `--keep-steam-input`) remove a
   launch option — **condicionado** à dedup substituta provada inclusive no caminho HIDAPI.

### Alternativas descartadas (com os argumentos que sobreviveram à revisão)

- **(a) Retry/backoff**: REFUTADO ao vivo (janela de minutos cobrindo o boot; ver acima).
- **(c) Cache do blueprint USB por controle**: não cobre o primeiro boot BT-only, adiciona
  persistência/invalidação, e é redundante — features de outro controle funcionam, logo template
  embutido cobre 100%.
- **Acordar o link BT com um write antes do GET**: descartado **pelos argumentos de
  arquitetura** — mantém a dependência do físico e não cobre boot sem controle. (A revisão
  derrubou o argumento de intrusividade: um output report com valid_flags zerados não pisca
  lightbar nem vibra — o parser do próprio repo o trata como inócuo. E ninguém mediu se um write
  acorda o firmware em < 5 s. O descarte fica, o motivo mudou.)
- **Launch option "mais esperta"**: é a burocracia de colar coisas que a regra de ouro veta, e o
  Estudo 1 provou que option persistida vira veneno quando o ambiente muda.
- **Traduzir descriptor BT→USB no capture**: irrelevante com blueprint sintético (e a refutação
  do medo BT é parcial — ver acima).

## Regra de ouro (conferida pelas 3 revisões)

BT-01..05 são **código puro** (nada a instalar). BT-06 estende o `hefesto-steam-input-guard`, que
o `install.sh` **já habilita por default** (step 11, opt-out `--keep-steam-input`) e o
`uninstall.sh` já remove simetricamente (units, `uninstall.sh:190-193`). Nada exige flag, comando
colado ou sudo em runtime. **SE** o BT-06 criar arquivo novo no guard, as três pontas
(install/uninstall/doctor) entram juntas no mesmo diff. O estado final prometido — "a launch
option deixa de existir" — **depende da frente irmã** (dedup por udev) entregue E validada também
contra o HIDAPI; essa dependência está declarada como gate no BT-06.

---

## Itens

### BT-01 — Blueprint 100% sintético: descriptor USB canônico + features capturados, embutidos (nunca ler o físico) — **P0, CLAUDE**

**O que fazer**
- Embutir em `uhid_gamepad.py` o descriptor USB canônico de 289 B (fonte:
  `captures/dualsense_usb_descriptor_054c0ce6.bin`, provado byte-idêntico ao físico).
- **Capturar dos DualSense da Vitória e commitar em `captures/`** os 3 features que o repo hoje
  NÃO tem (só o descriptor existe — confirmado pelas revisões): `0x05` (41 B), `0x09` (20 B),
  `0x20` (64 B). **O 0x05 TEM que ser bytes capturados de um DualSense real, nunca "calibração
  neutra" inventada** — o `hid_playstation` usa esses campos como divisores/escala da calibração
  de gyro/accel; zeros podem rejeitar o probe ou quebrar o motion.
- **O template do 0x20 decide o modo de vibração do kernel**: fw ≥ 0x0215 liga
  `use_vibration_v2` (valid_flag0 fica só com HAPTICS_SELECT 0x02). Os controles dela são fw
  0x0630 e só esse caminho foi testado (comentário em `uhid_gamepad.py:126-139`); o parser
  `_VIBRATION_FLAGS = 0x03` cobre os dois em teoria — **o teste de rumble deste item exercita o
  caminho induzido pelo fw que o template embute**.
- O MAC do 0x09 continua sobrescrito por player (`02:fe:00:00:00:0N`, LE) como hoje.
- `capture_dualsense_blueprint` **sai do caminho de criação** (`virtual_pad.py:153` é o único
  call site) — vira ferramenta de diagnóstico ou morre. `_try_uhid` deixa de exigir
  `hidraw_path`: o vpad uhid sobe SEMPRE, inclusive no boot sem controle nenhum (mata também o
  "P1 sempre nasce uinput no boot").
- **Absorve o antigo BT-05** (decisão da revisão de escopo — item separado era burocratização):
  remover o warning `uhid_blueprint_bt_descriptor` como **dead code pós-BT-01** (não como
  "descriptor BT é seguro" — a refutação é parcial) e eliminar os ~15,7 s de bloqueio do boot
  (os 3 GET de 5,2 s vivem dentro da função que sai do fluxo). Se a captura sobreviver como
  diagnóstico, as mensagens descrevem o sintoma medido ("controle BT ocioso não responde
  features; GET_REPORT estoura o timeout de 5 s do hidp"), **sem** cravar sniff/economia do link
  e sem sugerir "use USB ou máscara Xbox".
- Documentar o congelamento: jogos que leem 0x05/0x20 via HIDAPI verão os bytes do template
  (calibração e fw de um DualSense real, não do controle dela) — cosmético, e o vpad já não
  emite motion hoje (não é regressão).

**Arquivos**: `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`,
`src/hefesto_dualsense4unix/integrations/virtual_pad.py`, `captures/` (3 arquivos novos + o
descriptor existente), `tests/` (novos herméticos; reescrever
`tests/unit/test_vpad_upgrade_para_uhid.py`, que testa o caminho de captura).

**Critério de aceite (verificável)**
1. AO VIVO: com o físico SÓ em BT e o link na janela de sono (GET 0x09 em `/dev/hidraw4` dando
   EIO — condição verificada com o probe do estudo ANTES do teste), o daemon sobe vpad uhid Edge
   `054c:0df2` e o evdev do vpad emite ABS ao `forward_analog` (reproduzir o script do estudo).
2. AO VIVO: start do vpad < 1 s com BT dormindo (hoje: ~15,7 s) — medido no stdout/log do daemon
   (**não** no journal --user; o daemon roda --foreground).
3. Rumble AO VIVO no vpad sintético, exercitando o caminho de vibração do fw embutido no 0x20.
4. Grep: nenhum caminho de criação de vpad abre `/dev/hidrawN`.
5. Teste hermético: descriptor e features embutidos == os `.bin` de `captures/`, byte a byte.
6. Gate 2410 verde + `validar-acentuacao` ok nas linhas tocadas.

### BT-02 — Vpad uinput flavor dualsense forja 054c:0df2 (nunca mais nascer 0ce6) — **P0, CLAUDE**

**O que fazer**
- Em `uinput_gamepad.py`, trocar o product do flavor dualsense de `DUALSENSE_PRODUCT` (0x0CE6)
  para o mesmo `VPAD_PRODUCT` (0x0DF2) do uhid — mesmo degradado, o vpad nunca é indistinguível
  do físico; `IGNORE_DEVICES=0x054c/0x0ce6` (e a regra udev da frente irmã) nunca o atingem.
- Raio de impacto **menor** do que o estudo estimou (revisões conferiram): consumidores reais =
  `compose_launch` (`daemon_actions.py`) + ~6 arquivos de teste que assumem 0ce6 no vpad
  (`test_uhid_edge_dedup.py`, `test_storm_launch_options.py`, etc.) — **tudo no MESMO commit**.
  `coop.py` e perfis não usam PID; `evdev_reader.py:27` já tem `DUALSENSE_PIDS={0x0CE6,0x0DF2}`
  e o filtro `_is_virtual_evdev` (por `/devices/virtual/` no sysfs) impede self-adoption — sem
  risco de feedback loop.
- **ATENÇÃO — GUID do SDL**: o GUID evdev = bustype+VID+PID+version, e `uinput_gamepad.py:65-68`
  avisa que o `DEVICE_VERSION=0x3` atual foi preservado para o match no gamecontrollerdb
  ("validado ao vivo em gameplay"). Trocar o product INVALIDA essa validação: o GUID novo
  (054c:0df2 + version 0x3, que nenhum Edge real tem) pode cair no auto-mapping heurístico — a
  MESMA classe de sintoma do "8BitDo descontrolado" (botões trocados).
- **Versão correta do SDL** (a revisão refutou o "≥ 2.24"): o mapping evdev Linux do Edge só
  existe do **SDL 2.26.5** (fev/2023) em diante. Jogos com SDL estático < 2.26.5 veem o vpad
  uinput 0df2 como joystick SEM mapping de GameController (hoje, com 0ce6, casam com a entry
  antiga do DS5). Proton/Steam Runtime atuais: ok. Documentar o cenário de regressão em jogos
  nativos antigos.
- **Limitação de nicho, registrar**: um DualSense Edge FÍSICO (054c:0df2) fica indistinguível do
  vpad para qualquer dedup por VID/PID. Pré-existente desde bfd51db no uhid; este item a estende
  ao uinput. A Vitória não tem Edge; usuários futuros terão.

**Arquivos**: `src/hefesto_dualsense4unix/integrations/uinput_gamepad.py`,
`src/hefesto_dualsense4unix/app/actions/daemon_actions.py` (compose_launch), `tests/` (~6
arquivos que assumem 0ce6 no vpad).

**Critério de aceite (verificável)**
1. Teste unitário: vpad uinput dualsense expõe product 0x0DF2.
2. Teste SDL local (ferramenta do repo) com `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`:
   enxerga o vpad, não enxerga o físico, **E o MAPEAMENTO de botões/eixos está correto** (Cruz =
   A do layout, sticks nos eixos certos) — visibilidade sozinha NÃO fecha o item (exigência da
   revisão de regressão).
3. Gate verde; compose_launch e testes no mesmo commit.

### BT-03 — Backend real POR PLAYER + motivo, visível — **P1, CLAUDE** *(rebaixado de P0 pela revisão de escopo)*

**O que fazer**
- Precisão primeiro (as revisões corrigiram o estudo): o `state_full` **JÁ** expõe
  `gamepad_emulation.backend` do vpad primário (`ipc_handlers.py:411-426`) e o botão de launch
  options já mostra dica honesta quando degradado. O gap real: (a) backend **por player**
  (co-op), (b) o **motivo** da degradação (nó ausente, sem `hid_playstation`, probe recusou),
  (c) superfície **passiva** na GUI.
- Publicar evento no bus na degradação + estender o payload do status IPC com
  `backend`+`motivo` por player.
- A superfície visual nasce **DENTRO da reforma da aba Status** que o pedido nº 1 da Vitória já
  exige (frente irmã de GUI/Status) — **não** construir uma GUI de backend paralela
  (feature creep vetado). Este item entrega o dado no IPC + o slot na aba reformada.

**Arquivos**: `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
`src/hefesto_dualsense4unix/integrations/virtual_pad.py`,
`src/hefesto_dualsense4unix/daemon/ipc_handlers.py`, GUI da aba Status (coordenar com a frente
irmã).

**Critério de aceite (verificável)**
1. Teste hermético força a degradação (uhid indisponível) e verifica o payload por player com
   `backend='uinput'` + motivo; com tudo saudável, `backend='uhid'`.
2. GUI renderiza o estado por player (screenshot de validação na aba reformada).
3. Nenhum texto mente sobre o mecanismo do sono BT (ver Precisão de linguagem).

### BT-04 — Early-return por (flavor, backend) com latch anti-churn + aposentar o upgrade de hotplug — **P1, CLAUDE** *(reescrito: a metade "promoção no hotplug" foi REFUTADA)*

**O que fazer**
- **(a) Fix do NO-OP da GUI (mantido)**: em `start_gamepad_emulation`
  (`gamepad.py:296-298`), o early-return passa a comparar flavor **E** backend desejado —
  re-selecionar DualSense na GUI com vpad degradado recria o vpad no backend certo.
- **(b) Latch anti-churn (exigência da revisão de regressão)**: se o uhid falhou por razão
  ESTÁVEL (sem `/dev/uhid`, kernel sem `hid_playstation`), NÃO retentar automaticamente — sem o
  latch, o autoswitch flapando em `wm_class=unknown` (bug medido às 13:07:18; a histerese é item
  de OUTRA frente, não dá para assumir corrigida) + o early-return novo destruiriam e recriariam
  o vpad em LOOP no meio do jogo, pagando 0,5 s de `wait_for_bind` (que roda DENTRO do poll
  loop = input congelado) por tentativa. Retry automático só quando a disponibilidade do uhid
  MUDOU; caso contrário, só em ação explícita da usuária.
- **(c) Aposentar/simplificar `upgrade_primary_vpad_to_uhid`** em vez de adicionar call site no
  reconnect_loop: pós-BT-01 o gate `resolve_hidraw_path is None → return False` morre e a
  promoção no hotplug é código morto por desenho (o `hid_playstation` autocarrega por modalias,
  sem físico nenhum). NÃO vender promoção-no-hotplug como fix do boot — o boot já nasce uhid
  com BT-01.
- Documentar o comportamento na recriação: o docstring do upgrade já admite que "o jogo aberto
  PERDE o vpad por um instante" — a recriação via GUI é ação explícita da usuária (aceitável);
  a automática é vetada pelo latch.

**Arquivos**: `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
`src/hefesto_dualsense4unix/daemon/connection.py` (remoção/simplificação, não adição),
`tests/`.

**Critério de aceite (verificável)**
1. Teste: com vpad degradado e uhid DISPONÍVEL, re-selecionar DualSense recria em uhid; com uhid
   indisponível por razão estável, N re-seleções automáticas (autoswitch/perfil) NÃO recriam
   (latch), e 1 ação explícita da usuária tenta 1 vez.
2. AO VIVO: ligar o controle depois do daemon resulta em vpad Edge 0df2 sem reiniciar nada
   (consequência do BT-01, verificada aqui).
3. Gate verde; nenhum caminho recria vpad em loop sob flapping simulado do autoswitch.

> **NOTA DE RESOLUÇÃO (2026-07-16, pós-revisão adversarial da Fase 1).** Este item conflitava
> com o **VPAD-01** do doc irmão (`2026-07-16-sprint-vpad-sempre-edge.md`): o (c) daqui mandava
> aposentar o upgrade de hotplug SEM call site novo no `reconnect_loop`; o VPAD-01 mandava
> exatamente o call site. Resolução registrada nos dois docs:
>
> - **VPAD-01 VENCE no (c)**: o call site do `reconnect_loop` FICA, como rede de segurança com
>   precheck `uhid_available()` + cooldown compartilhado. A premissa do (c) — "pós-BT-01 a
>   disponibilidade do uhid é estática, logo a promoção no hotplug é código morto" — não vale:
>   a ACL do `/dev/uhid` pode chegar DEPOIS do boot do daemon (primeira sessão pós-install, o
>   `udevadm trigger` do subsystem misc), e nesse cenário real o vpad nasceu uinput e a borda
>   de conexão é o único gatilho automático de recuperação. O **(c) fica SUPERADO nessa parte**;
>   um agente de fase futura NÃO deve remover o call site "ao pé da letra" deste doc.
> - **(a) e (b) IMPLEMENTADOS** (`_deve_promover_backend` em
>   `daemon/subsystems/gamepad.py`): o (a) compara (flavor, backend); o (b) virou latch por
>   ORIGEM — `origin='profile'` (perfil/autoswitch) NUNCA promove por apply idêntico, só o
>   gesto manual da usuária tenta (1 clique = 1 tentativa, cooldown de 30 s contra clique
>   repetido). O critério 1 acima está coberto por teste
>   (`tests/unit/test_vpad_backend_wiring.py::TestRebackendPorReselecao`).

### ~~BT-05~~ — ABSORVIDO no BT-01 *(decisão da revisão de escopo)*

Não é um item: o warning `uhid_blueprint_bt_descriptor` e os ~15,7 s de bloqueio vivem dentro da
função que o BT-01 tira do fluxo — item separado com critério próprio era exatamente a
burocratização que a regra de ouro veta. Ver os critérios 2 e 4 do BT-01.

### BT-06 — Desenvenenar a Steam: guard remove a launch option, doctor acusa, uninstall desenvenena — **P1, AMBOS** *(com GATE de dependência da frente irmã)*

**O que fazer**
- **GATE (as 3 revisões insistiram — sem isso o item NÃO liga):** a remoção automática só é
  habilitada depois que a dedup substituta (regra udev `ID_INPUT_JOYSTICK=0` da frente irmã +
  BT-02) estiver instalada E provada **também no caminho HIDAPI do SDL**. Motivo:
  `ID_INPUT_JOYSTICK=0` só esconde o físico do caminho evdev; a enumeração HIDAPI varre
  `/dev/hidraw*` por VID/PID SEM consultar esse atributo, e o `compose_launch` do modo Edge
  mantém o HIDAPI LIGADO de propósito (`PROTON_ENABLE_HIDRAW=1`). Remover a option sem essa
  prova devolve o controle DUPLICADO (físico via HIDAPI + vpad Edge) — o bug que a option matou
  na v3.13 — e regride o ÚNICO setup que ela declarou PERFEITO (USB + máscara Xbox). Prova
  exigida: teste SDL com HIDAPI LIGADO + regra udev instalada = exatamente 1 controle.
- **Remoção cirúrgica**: só os tokens que o hefesto plantou
  (`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` e, SÓ quando acompanhado dele, o
  `SDL_JOYSTICK_HIDAPI=0` do par) preservando o resto da linha (`__GL_SHADER_DISK_CACHE*`,
  `%command%`). **`SDL_JOYSTICK_HIDAPI=0` NÃO é lixo incondicional** — a máscara Xbox o emite de
  propósito (`daemon_actions.py:226`); não remover de jogo onde a usuária usa máscara Xbox.
  O sed atual do guard (feito para PSSupport, chave-valor) **não serve** para editar DENTRO do
  valor de LaunchOptions: é cirurgia nova, com backup (`.bak.steam-input-<ts>`, mecânica que o
  guard já tem) e teste de que o resto da linha sobrevive.
- **Coerência interna no MESMO sprint (revisão de regressão):** `scripts/doctor.sh:387` hoje
  RECOMENDA exatamente a string que o guard passaria a remover, e
  `daemon_actions.py compose_launch/on_storm_copy_launch` a GERA para colar. Sem atualizar os
  dois aqui, o sistema briga consigo mesmo (ela cola, o timer remove em 30 min). O doctor ganha
  o check do veneno; o compose_launch para de emitir `IGNORE_DEVICES` quando a dedup udev
  estiver ativa (e o botão vira informativo — atende o pedido nº 5 dela: a option DEIXA de
  existir, melhor do que popup).
- **Simetria do uninstall (regra histórica — a mesma que já quebrou o mic):** desinstalar o
  hefesto com o veneno no vdf deixa o Sackboy sem controle NENHUM para sempre (físico escondido,
  vpad inexistente). O `uninstall.sh` também desenvenena os `localconfig.vdf` (ou restaura
  backup).
- **Timing honesto:** o guard automático roda `--apply-quiet`, que ADIA a edição enquanto a
  Steam estiver aberta (editar com a Steam viva é inútil — ela sobrescreve ao sair). O efeito
  real vem no próximo ciclo com Steam fechada — o critério de aceite e a comunicação à usuária
  dizem isso.
- Estado atual do veneno: exatamente 1 jogo (appid 1599660, linha 914 de
  `~/.steam/steam/userdata/1300222895/config/localconfig.vdf`).

**Arquivos**: `scripts/disable_steam_input.sh` (ou script irmão do guard), `scripts/doctor.sh`,
`src/hefesto_dualsense4unix/app/actions/daemon_actions.py`, `uninstall.sh`, `install.sh` (SÓ se
o guard ganhar arquivo novo — as três pontas juntas), `tests/shell/`.

**Critério de aceite (verificável)**
1. GATE provado ANTES de ligar: teste SDL com HIDAPI ligado + regra udev da frente irmã ativa =
   1 controle exatamente (registrado no doc da frente irmã).
2. `doctor.sh` aponta o veneno enquanto existir e confere a regra udev ativa.
3. Com a Steam fechada, após o ciclo do guard: grep `IGNORE_DEVICES` nos `localconfig.vdf`
   vazio; a linha do Sackboy mantém `__GL_SHADER_DISK_CACHE*` e `%command%` intactos (teste com
   fixture do vdf real); backup criado.
4. `compose_launch` e `doctor.sh` não recomendam mais a option quando a dedup está ativa.
5. `uninstall.sh` desenvenena; ciclo uninstall→install→doctor verde sem flag nenhuma (regra de
   ouro); simetria conferida.

### BT-07 — Validação humana por BT em jogo real — **P0 (GATE DA ENTREGA), VITORIA_HUMANO** *(promovido de P2: é investigação, não decoração)*

**O que fazer**
- Com BT-01/02/06 entregues, a Vitória joga por BT: **Sackboy** (desenvenenado) e **RDR2**, nos
  modos hefesto/playstation E nativo.
- **Célula de controle obrigatória (revisão técnica):** BT + **máscara Xbox** — o relato dela
  não cobre essa célula da matriz; se funcionar, isola o problema no layout PS.
- **Se o RDR2 continuar sem input por BT** (cenário esperado como possível — a segunda causa
  está em aberto), abrir investigação nova com os candidatos, POR ORDEM: (1) **Steam Input
  PSSupport** — o nosso install o zera por default com guard de 30 min; testar religando
  temporariamente para o RDR2; (2) dedup interno do SDL entre vpad-evdev e físico-HIDAPI;
  (3) os 4 CRC fails/dia do rádio 2.4 GHz (2 receivers + BT no mesmo espectro).
- Qualquer falha registrada com o **stdout/log do daemon** + dmesg do momento (não "journal
  --user" — ver Precisão de linguagem).
- O 8BitDo NÃO entra aqui (frente multi-controle).

**Arquivos**: `docs/process/sprints/` (registro do resultado).

**Critério de aceite (verificável)**
1. Ela confirma inputs + vibração por BT no Sackboy nos dois modos, sem launch option nenhuma.
2. RDR2 por BT: ou funciona (frente encerrada), ou a falha é registrada com logs+dmesg e a
   investigação da segunda causa abre com a matriz acima preenchida.
3. Invariante do projeto honrada: **teste verde sem validação ao vivo NÃO fecha item** — este
   item é o que fecha a frente.

---

## Armadilhas conhecidas que esta frente atravessa

- **MAC próprio por vpad** (`02:fe:00:00:00:0N`, bytes 1..6 do 0x09 em LE): MAC duplicado =
  probe falha com -17. O template do 0x09 continua sobrescrito por player.
- **valid_flag do rumble é máscara `0x03`, nunca só `0x01`**: fw ≥ 0x0215 usa
  `COMPATIBLE_VIBRATION2` com valid_flag0 = 0x02 sozinho. O fw do template 0x20 (BT-01) decide o
  caminho — testar o caminho que o template induz.
- **`_INPUT_PAYLOAD_SIZE = 63`**: o driver compara com `DS_INPUT_REPORT_USB_SIZE=64` e descarta
  CALADO report de tamanho errado (o vpad nasce mudo). Touch em 32/36, bateria em 52.
- **udev < 73 para uaccess**: quem vira a TAG em ACL é a 73-seat-late; nós em `SUBSYSTEM=misc`
  (uhid/uinput) exigem `udevadm trigger --subsystem-match=misc`. (Nada novo de udev NESTA
  frente — a regra dinâmica é da frente irmã — mas o BT-06 depende dela.)
- **Sudo-zero na GUI em runtime** (decisão bfd51db): nada desta frente pede senha em clique de
  botão; o guard é unit --user.
- **Dropdowns quebram no COSMIC** (cosmic-comp#2497): a superfície do BT-03 na aba Status usa
  os padrões já adotados (botões segmentados/labels), nunca popups novos.
- **GIL/throttling**: `wait_for_bind` (0,5 s) roda dentro do poll loop = input congelado — por
  isso o latch do BT-04 e a proibição de retry em loop.
- **Fonte de log real**: daemon em `--foreground` = stdout, não journal --user. Todo critério de
  aceite desta frente cita a fonte certa.

## Ordem

BT-01 → BT-02 (mesmo dia, é o par que muda a identidade do vpad) → BT-04 → BT-03 (junto com a
reforma da aba Status da frente irmã) → BT-06 (SÓ após o gate da dedup HIDAPI da frente irmã) →
BT-07 (gate humano da entrega — Sackboy + RDR2 + célula BT+Xbox).

## Referências

- Estudo 1 (117 agentes, 2026-07-16) — cadeia EIO→uinput/0ce6→launch option, medições de janela
  ativa/sono, experimento do blueprint híbrido.
- Revisões adversariais (3 lentes, 2026-07-16) — reproduções independentes (EIO às 15:02,
  hcitool sem SNIFF, parse do vdf), refutações (SDL 2.26.5, promoção-no-hotplug, refutação
  parcial do descriptor BT) e as ressalvas obrigatórias incorporadas acima.
- `docs/process/sprints/2026-07-15-sprint-uhid-dualsense-de-verdade.md` — PoC uhid, os 5 bugs
  que só o hardware pegou.
- `docs/process/sprints/2026-07-16-sprint-edge-dedup-e-fechamento.md` — UHID-04, compose_launch,
  o aviso BT log-only que o BT-01 aposenta.
- Frente irmã: dedup por udev (`ID_INPUT_JOYSTICK=0`) + reforma da aba Status + histerese do
  autoswitch (`profiles/autoswitch.py:69-74`).
- Kernel: `net/bluetooth/hidp/core.c` (`hidp_get_raw_report`, timeout 5*HZ → -EIO),
  `drivers/hid/hid-playstation.c` (calibração/firmware/vibração v2).
