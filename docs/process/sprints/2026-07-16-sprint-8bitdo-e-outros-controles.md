# Sprint SPRINT-8BITDO-01 — 8BitDo SN30 Pro e os outros controles: ver, entender, não interferir

Frente da onda 2026-07-16 (Estudo 1, 117 agentes + relato ao vivo da Vitória). Branch
`sprint/harmonia-uhid`. Passou por revisão adversarial em 3 lentes (técnica, regressão,
escopo); as refutações e ressalvas estão incorporadas no texto.

**Status (2026-07-17): 8BIT-03 construído (doctor detecta a CASCATA via journal, zero
falso-positivo — a morte real de 2026-07-16, 70 timeouts na `.0014`, dispara; a
não-terminal `.0008` não); 8BIT-06 construído (`docs/usage/troubleshooting-8bitdo.md`);
8BIT-01 construído (inventário read-only opt-in no `controller.list`, exclusões do
vpad/DualSense provadas ao vivo — a validação POSITIVA ficou pendente porque o Pro
Controller BT morreu às 23:52 desta madrugada com a assinatura curta do estudo: 3×
`exceeded max attempts` + re-probe `-110`; NOTA honesta: assinatura curta fica ABAIXO
do threshold de 10 timeouts do 8BIT-03 — viés anti-falso-positivo deliberado; pode ter
sido idle-off, não dá para cravar morte-por-cascata). 8BIT-02 NÃO construído — aguarda
o OK de produto da mantenedora (controles externos 100% read-only na aba
multi-controle). 8BIT-04: o item 1 ficou SEM OBJETO nesta onda (não existe regra udev
de dedup — o mecanismo vencedor foi o wrapper `hefesto-launch`); os requisitos do item
2 seguem registrados abaixo e valem para qualquer onda futura que reviva a regra.
8BIT-05 (decisão de modo) segue com a Vitória — custo zero de código.**

Pedido da mantenedora (escopo, nas palavras dela): *"Eu NÃO quero que vire uma central completa
das marcas e afins. [...] Só uma aba pra conectar os controles e ver como eles aparecem com o
output de saída similar ao que fizemos pro dsx, só isso. Não vamos virar uma super central."*

## Honestidade primeiro (leia antes dos itens)

**O hefesto está fora da cadeia causal do 8BitDo, e NENHUM item de código desta frente conserta
o controle dela.** A cura real é uma decisão humana já destravada por este estudo, sem uma linha
de código: escolher o modo do controle (`8BIT-05`). O que o hefesto entrega aqui é garantia de
não-interferência, observabilidade enxuta e diagnóstico honesto — dentro da regra de ouro.

Duas correções obrigatórias sobre o estudo original (a revisão pegou frases falsas que este doc
não pode repetir):

1. **"O daemon real nem estava rodando durante as mortes" é FALSO.** O serviço real
   (`fake=False`, PID 3061) subiu às 12:36:42 e estava vivo na morte das 12:38:46. A inocência
   do hefesto se prova pelo caminho certo: o discovery só adota vendor `0x054C` com PID
   `{0x0CE6, 0x0DF2}` (`core/evdev_reader.py:26-27,124-131`; `coop.py:226,242` usa
   `discover_dualsense_evdevs`; `grep -riE 'nintendo|8bitdo|057e' src/` = zero) — o daemon é
   incapaz de abrir ou grabbar um device `057e`.
2. **"O daemon fake não tem nenhum device de input aberto" é FALSO.** O fake TEM `/dev/uinput`
   aberto e criou o `Hefesto - Dualsense4Unix Virtual Keyboard` (input213). A conclusão de
   não-interferência no 8BitDo permanece (teclado virtual não toca gamepads; nenhum
   `event*`/hidraw de gamepad aberto), mas um device virtual a mais é enumerável pelo Steam e
   pelos jogos — o inventário do `8BIT-01` tem de excluí-lo.

## O que está provado — e o que não está

Invariante do projeto: **teste verde sem validação ao vivo NÃO fecha item.** A mesma régua vale
para afirmações: cada uma abaixo carrega o seu nível.

### PROVADO AO VIVO (nesta máquina, hoje)

- **O "8BitDo por cabo" está em modo Switch**: enumera como Nintendo Pro Controller
  `057e:2009`, driver `hid-nintendo` — mas o OUI do MAC (`E4:17:D8`) é da 8BITDO TECHNOLOGY HK
  LIMITED (`systemd-hwdb query OUI:E417D8`; `uniq=e4:17:d8:00:00:02`).
- **A morte "sem desconectar" é o `hid-nintendo` desistindo, por Bluetooth**: 3 sessões BT
  (`0005:057E:2009.0008` às 12:38:46-47 e `.0014` às 13:15:34 e 13:22:52-13:24:00) com dezenas
  de `timeout waiting for input report` culminando em `joycon_enforce_subcmd_rate: exceeded max
  attempts` — o driver desiste e o input morre com o link BT ainda de pé.
- **A primeira morte BT aconteceu SEM Steam rodando**: boot às 12:31:30, morte às 12:38:46,
  Steam só às 12:46:51 (journal + `ps lstart`). O mecanismo de morte dispensa qualquer
  duplo-mestre — **é proibido vender "feche o Steam" como cura**.
- **A assinatura nem sempre é terminal**: às 12:38:46 o `exceeded max attempts` estourou na
  conexão e o controle viveu mais ~8 minutos (tráfego de IMU às 12:46:58). O padrão de morte
  real é a CASCATA de timeouts (13:23:53→13:24:00). O diagnóstico do doctor exige a cascata,
  não a linha isolada.
- **A única configuração provadamente estável é modo Switch POR CABO**: a instância USB
  (`0003:057E:2009.0015`, desde 13:28:31) está sem um único timeout.
- **Fd aberto pelo Steam é estado NORMAL, não assinatura de conflito**: o Steam (PID 16399)
  segura o hidraw6 (8BitDo) E os hidraw2/hidraw4 dos dois DualSense — que funcionam
  perfeitamente com `SteamController_PSSupport=0` persistido. Segurar fd não corrompe.
- **O firmware é clone**: descriptor HID malformado no bind (`unknown main item tag 0x0`,
  12:38:44) — firmware original não produz isso.
- **O SN30 Pro TEM IMU real** (gyro 3 eixos + acelerômetro): `using factory cal for IMU` +
  input `Pro Controller (IMU)` com `ID_INPUT_ACCELEROMETER=1`. O gyro só é exposto em modo
  Switch (o protocolo XInput não tem canal de motion).
- **A regra udev Sony-only da frente DEDUP não respinga no 8BitDo**: `udevadm info` do node
  dele mostra `ID_VENDOR_ID=057e ID_MODEL_ID=2009 ID_INPUT_JOYSTICK=1` — fora do match
  `054c/0ce6`. (Precedente no repositório: `assets/78-dualsense-motion-not-joystick.rules`
  manipula `ID_INPUT_JOYSTICK` com match Sony e comprovadamente não o toca.)
- **`journalctl -b -k` funciona SEM sudo** nesta máquina (grupo `adm`; `kernel.dmesg_restrict=1`
  torna o `dmesg` cru restrito) — e o `doctor.sh` já usa esse padrão (linhas 579 e 656).
- **`xpad` é USB-only**: `modinfo xpad` = 116 aliases `usb:`, ZERO aliases `hid:`. Em modo
  X-input por Bluetooth o controle cai em `hid-microsoft`/`hid-generic` (aliases
  `hid:b0005...v045e` para `02e0`/`02fd`), nunca no `xpad`. **Só o cabo garante
  `045e:028e`/xpad/Xbox 360 real.**
- **O kernel nunca viu um Xbox hoje**: zero enumerações `045e`/xpad/xbox no dmesg — o rótulo
  "Xbox" que ela vê vem de camada acima do kernel (ver Hipóteses).
- **A launch option envenenada segue PERSISTIDA** no Sackboy (`localconfig.vdf`, appid 1599660,
  linha ~914): `SDL_JOYSTICK_HIDAPI=0 SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6 ...
  %command%` — junto de `UseSteamControllerConfig=0` (~1103) e `PSSupport=0` (1108).
- **A sonda "quem segura o hidraw" funciona sem sudo** para processos do mesmo usuário
  (readlink em `/proc/16399/fd/174` → `/dev/hidraw6` como usuária comum; ~4600 fds enumeráveis
  em ~6 ms).

### PROVADO NO CÓDIGO

- Filtro DualSense-only no discovery (`evdev_reader.py:26-27,124-131`); co-op só adota o que
  sai dele (`coop.py:226,242`). Zero referências a nintendo/8bitdo/057e em `src/`.
- Infra que os itens desta frente devem ESTENDER (não duplicar): `_handle_controller_list` /
  `describe_controllers` no IPC (`ipc_handlers.py:501-506`), listagem por controle no Status
  (`status_actions.py:220-230,534-545`), `_is_virtual_evdev` (`evdev_reader.py:43-59`, exclui
  `/devices/virtual` — cobre o vpad uhid, que vive sob `/devices/virtual/misc/uhid`).
- A enumeração de evdev custa **10-40 ms** (comentário em `evdev_reader.py:70-79`, lição
  PERF-MULTI-CONTROLLER-01) — não pode rodar no event loop.
- `compose_launch` (`daemon_actions.py:207-228`): o docstring dá ao `SDL_JOYSTICK_HIDAPI=0`
  função ALÉM da dedup ("força o SDL a ler o evdev, que o daemon graba"); a máscara Edge emite
  `PROTON_ENABLE_HIDRAW=1`.
- Precedente de edição segura do `localconfig.vdf` com Steam fechado:
  `scripts/disable_steam_input.sh:158-178`.
- A GUI é Glade-based (`gui/main.glade`; `app.py:741,743,761` — `append_page` + refresh em
  `switch-page`): aba nova SEM editar o .glade é impossível.

### HIPÓTESE (plausível, NÃO provada — o doc não pode tratar como fato)

- **Duplo-mestre corrompe o hidraw do clone** (Steam/SDL driver de Switch × `hid-nintendo`
  escrevendo subcommands no mesmo hidraw) e produz o "descontrolado": a COABITAÇÃO está provada
  (lsof), a CORRUPÇÃO não — e o contra-exemplo vivo são os DualSense, que coabitam sem
  corromper. É agravante plausível, documentado na comunidade para o protocolo Switch
  (stateful). **Quem fecha ou derruba a hipótese é o `8BIT-05`.**
- **"Reconhecido como Xbox"**: hipótese A = vpad XInput do Steam Input para o Pro Controller;
  hipótese B (mais parcimoniosa) = a ponte winebus/XInput do Proton, que apresenta QUALQUER pad
  como "Xbox 360" sem Steam Input nenhum. A hipótese A conflita com o
  `UseSteamControllerConfig=0` persistido no Sackboy (Steam Input forçado OFF naquele app pelo
  guard do próprio hefesto). Nenhuma das duas está provada; a aba (`8BIT-02`) não pode concluir
  XInput a partir de fd aberto.
- **"O suporte a Switch fica no default ON do Steam"**: NÃO verificado (nenhuma key de Switch
  persistida; o default varia por versão). Tratar como hipótese.

### ESPECULAÇÃO (nunca exercitado nesta máquina)

- Estabilidade do modo X-input por Bluetooth (zero enumerações `045e` no dmesg de hoje).
- O "descontrolado" reproduzindo por CABO (a instância USB está limpa desde 13:28).

## Causa-raiz (sobrevive à revisão, com as ressalvas)

1. **PROVADA**: por Bluetooth, o firmware clone do SN30 Pro em modo Switch engasga com o
   protocolo de subcommands do `hid-nintendo`; o driver estoura o rate-limiter e desiste — o
   input morre sem desconectar. Acontece com ou sem Steam.
2. **HIPÓTESE (rebaixada pela revisão)**: o duplo-mestre no hidraw como agravante do
   "descontrolado". Não é causa demonstrada de nenhum evento registrado hoje.

O hefesto está fora das duas: filtro Sony-only no código, e nem a launch option participa do
caminho do 8BitDo (as mortes são em BT, fora de jogo).

## Regra de ouro (tudo no install, sem flags) — como esta frente a satisfaz

**Por vacuidade**: esta frente não instala NADA novo no sistema (blacklists e quirks para o
clone seriam invasivos — ver alternativas descartadas). A única peça instalável relacionada (a
regra udev de dedup) pertence à frente DEDUP, onde já nasce default no install, simétrica no
uninstall e verificada pelo doctor. Sudo-zero em runtime: a aba nova não pede senha para nada, e
o doctor usa `journalctl -b -k` (sem sudo, grupo `adm`). Nenhum item abaixo pede "cole isto" ou
"rode aquilo" como requisito.

## O que o hefesto NÃO vai fazer (alternativas descartadas, com os motivos certos)

- **Blacklistar `hid_nintendo` no install**: mata o evdev do controle para QUALQUER app fora do
  Steam — quebra em vez de proteger, com efeito colateral system-wide.
- **Adotar o 8BitDo no vpad do hefesto**: é a "super central" vetada, e adicionaria um TERCEIRO
  mestre na briga pelo hidraw do clone.
- **Mais launch options** (ex.: `SDL_JOYSTICK_HIDAPI_SWITCH=0` por jogo): burocracia colável —
  exatamente a queixa da Vitória — e não cura a morte por BT.
- **Regra udev `ID_INPUT_JOYSTICK=0` para `057e:2009`**: cega apps fora do Steam para um
  controle que não é problema nosso; o conflito de hidraw continuaria.
- **Tratar como auto-sleep**: refutado — as mortes ocorreram em uso ativo com o link BT vivo.
- **Tratar como colisão com o vpad Xbox do hefesto**: refutado — o 8BitDo não é Xbox no kernel
  e o daemon é incapaz de abrir devices `057e`.

## Itens

Prioridades honram a lente de escopo da revisão: **NADA nesta frente é P0** — os P0 verdadeiros
da onda moram na frente DEDUP (regra udev default no install, simétrica no uninstall). O único
desbloqueador imediato do 8BitDo é o `8BIT-05`, humano e com custo zero de código.

### 8BIT-05 — Validação humana: escolher o modo do 8BitDo e jogar 10 minutos

- **Quem**: VITORIA_HUMANO. **Prioridade**: P1 (primeiro da fila — destrava sem código).
- Decisão com dado na mão, opções reescritas com honestidade após a revisão:
  - **(a) Modo Switch POR CABO** — a ÚNICA configuração provadamente estável (instância limpa
    desde 13:28:31). Sobre o gyro: ele só chega ao jogo via Steam Input ativo — **e isso
    conflita com o próprio hefesto**: o `hefesto-steam-input-guard` reaplica Steam Input OFF e
    o Sackboy já tem `UseSteamControllerConfig=0`, que desliga o Steam Input do app para TODOS
    os controles. Para ter gyro nesse arranjo a Vitória precisa reativar o Steam Input naquele
    jogo, **sabendo que o guard pode desfazer a escolha sozinho**. Dito com todas as letras.
  - **(b) Modo X-input (ligar segurando X+Start)** — **POR CABO** vira `045e:028e` via `xpad`
    (Xbox 360 de verdade): estável esperado, **SEM gyro** (limitação do protocolo XInput, não
    nossa) e cria um segundo "Xbox 360 pad" ao lado do vpad Xbox do hefesto — não colidem
    funcionalmente, mas confundem na UI de jogos; a aba do `8BIT-02` mitiga mostrando qual é
    qual. **POR BLUETOOTH é EXPERIMENTO, não saída garantida**: `xpad` é USB-only; em BT o
    controle cai em `hid-microsoft`/`hid-generic` (PID provável `02e0`/`02fd`, não `028e`) e a
    estabilidade nunca foi exercitada nesta máquina.
  - **(c) Modo Switch por BT com Steam Input de Switch desligado** — aceita o risco do firmware
    clone: as 3 mortes de hoje foram nesse modo, e uma delas SEM Steam rodando — desligar o
    Steam Input não é cura provada de nada.
- Validar o modo escolhido em jogo real por 10 minutos observando o sintoma
  "descontrolado/inputs cancelados". **Este item também fecha ou derruba a hipótese do
  duplo-mestre**: se falhar POR CABO, capturar `journalctl -k` + `lsof` do hidraw no ato.
- **Aceite**: 10 minutos de gameplay sem perda de input no modo escolhido; em falha, evidência
  coletada no ato e anexada a este doc.

### 8BIT-03 — doctor.sh aprende a assinatura de morte por BT do clone (REDESENHADO)

- **Quem**: CLAUDE. **Prioridade**: P1. **Arquivos**: `scripts/doctor.sh`.
- O desenho original ("driver nintendo + Steam segura o hidraw → avisar dois mestres") foi
  **REFUTADO** pelas três lentes: o Steam abre o hidraw de TODO controle suportado — inclusive
  dos DualSense saudáveis — então o aviso dispararia SEMPRE que o Steam estivesse aberto,
  inclusive na configuração provadamente estável. Alarme falso crônico ensina a usuária a
  ignorar o doctor.
- Desenho novo:
  - Detecção via `journalctl -b -k` **sem sudo** (grupo `adm`; padrão que o doctor já usa nas
    linhas 579/656) — não `dmesg`/sudo.
  - Gate do diagnóstico = a **CASCATA**: série de `timeout waiting for input report` culminando
    em `joycon_enforce_subcmd_rate: exceeded max attempts` (padrão 13:23:53→13:24:00). A linha
    isolada NÃO dispara (12:38:46 não foi terminal — o controle viveu mais ~8 min).
  - Mensagem: "o driver desistiu do controle: por Bluetooth o firmware 8BitDo em modo Switch
    engasga com o hid-nintendo; a configuração provadamente estável é cabo em modo Switch;
    X-input por cabo vira Xbox 360 real (sem gyro); X-input por Bluetooth é experimento".
  - A coabitação Steam×hidraw vira, NO MÁXIMO, uma linha informativa neutra ("hidraw também
    aberto pelo Steam — normal") — nunca warning.
  - Saída informativa, exit code inalterado, nada é alterado no sistema, nenhuma flag nova.
- **Aceite (o teste do falso-positivo é o critério central)**: com os timeouts de hoje no
  journal, o doctor imprime o diagnóstico citando a instância certa; com journal limpo, Steam
  aberto e o 8BitDo por cabo funcionando, **não imprime aviso nenhum**; roda sem sudo; exit
  code inalterado.

### 8BIT-01 — Inventário de gamepads físicos no daemon (todos os vendors, read-only)

- **Quem**: CLAUDE. **Prioridade**: P1. **Arquivos**: `src/hefesto_dualsense4unix/core/evdev_reader.py`,
  `src/hefesto_dualsense4unix/daemon/ipc_handlers.py`, `tests/`.
- `discover_external_gamepads()` em `evdev_reader.py`: enumeração evdev com caps de gamepad
  (BTN_GAMEPAD/BTN_SOUTH) SEM filtro de vendor, excluindo virtuais via `_is_virtual_evdev`
  (cobre o vpad uhid sob `/devices/virtual/misc/uhid`, os vpads virtuais do Steam E o teclado
  virtual do próprio daemon) e os DualSense já cobertos pelo caminho existente. Por device:
  name, vid, pid, bus (usb/bluetooth), uniq/MAC, driver kernel (readlink do driver no sysfs HID
  pai), evdev path, hidraw irmão.
- **ESTENDER** `_handle_controller_list`/`describe_controllers` (`ipc_handlers.py:501-506`) —
  não criar handler paralelo `controllers.external`: uma lista de controles com um dono só.
- **Fora do event loop, obrigatoriamente**: a enumeração custa 10-40 ms (lição
  PERF-MULTI-CONTROLLER-01) e o handler IPC roda no mesmo loop asyncio do daemon — síncrono,
  abrir a aba no meio do jogo congela o input dela. Rodar em executor/thread. Sob demanda
  (nunca no tick; nada entra no `state_full` quente).
- Sonda `holders` (quem segura o hidraw): **opcional e degradável** — sob demanda, restrita aos
  PIDs do steam (não `/proc/*/fd` de todos os processos), timeout curto, e a resposta funciona
  sem ela (campo ausente, sem erro). **Não é critério de aceite.**
- Testes resolvem o node dinamicamente por VID:PID — nunca hardcodar `eventN` (o principal do
  8BitDo hoje é event261 e o IMU event262; renumeram a cada replug).
- **Aceite**: com o 8BitDo plugado, a chamada IPC devolve uma entrada `vid=057e pid=2009
  driver=nintendo bus=usb`; o inventário exclui o vpad uhid e o Virtual Keyboard do daemon
  (teste dedicado); teste unitário hermético com sysfs/evdev fake cobre o shape; nenhuma
  chamada nova no poll loop (custo do tick inalterado); teste prova que o handler não bloqueia
  o event loop. Validação ao vivo com o 8BitDo plugado — **teste verde sozinho não fecha**.

### 8BIT-02 — Aba "Controles" ÚNICA, fundida com a frente multi-controle

- **Quem**: CLAUDE (constrói) + VITORIA_HUMANO (decisão de produto ANTES). **Prioridade**: P1,
  condicionado à fusão. **Arquivos**: `src/hefesto_dualsense4unix/app/app.py`,
  `src/hefesto_dualsense4unix/app/actions/controllers_actions.py` (novo mixin, padrão
  `status_actions.py`), `src/hefesto_dualsense4unix/app/ipc_bridge.py`,
  **`src/hefesto_dualsense4unix/gui/main.glade`** (a GUI é Glade-based — o plano original
  omitia e por isso era impossível como especificado), `tests/`.
- **Pré-requisitos de produto (bloqueiam a construção)**:
  1. Confirmar com a Vitória que os controles externos são **100% read-only** na aba — o
     "escolher o output" do pedido 4 é ambíguo, e read-only é a posição defensável (adotar
     externos = terceiro mestre no hidraw + super central vetada).
  2. Coordenar com a frente dos pedidos 1/3 (Status por controle): **UMA aba/lista de
     controles com UM dono** — duas listas concorrentes ferem a lente "um dono por conceito".
     Esta é a aba do item 4 da Vitória; a frente multi-controle e esta constroem a MESMA
     superfície juntas.
- Um card por controle físico. DualSense: reusa transporte/bateria/seletor existentes.
  Externos: nome + VID:PID + barramento + driver + identificação honesta ("Pro Controller
  (modo Switch) — 8BitDo pelo OUI do MAC").
- **A linha "como o jogo vê" NÃO pode derivar de fd aberto** (REFUTADO ao vivo: o Steam segura
  os hidraws dos DualSense com PSSupport=0 — a regra proposta rotularia como "Steam Input em
  uso" exatamente os controles onde o projeto garante que está OFF; a aba nasceria mentindo).
  Fontes honestas: driver kernel + keys per-app do `localconfig.vdf`
  (`UseSteamControllerConfig`/`PSSupport`) + Steam rodando — e texto que não conclui o que não
  sabe: "hidraw aberto pelo Steam" em vez de "aparece como Xbox 360". O mecanismo do
  "vira Xbox" é apresentado como hipótese (winebus/Proton OU Steam Input).
- Card de aviso do 8BitDo **condicionado à assinatura de morte do `8BIT-03`** (nunca à
  coabitação), com as saídas do `8BIT-05` em linguagem simples — orientação visível, nunca
  requisito colável.
- ZERO knobs proprietários para outras marcas. Sem dropdowns/popups (bug de foco do
  cosmic-comp — usar cards e botões segmentados, como o resto da GUI). Refresh no
  `switch-page` (padrão existente em `app.py:761`) + botão de atualizar manual.
- **Aceite**: com 2 DualSense + 8BitDo plugados, a aba lista os 3 com identidade correta;
  os DualSense **não** ganham rótulo de "Steam Input em uso" só porque o Steam segura o hidraw
  (teste de regressão do falso-positivo); nenhum clique exige sudo; abrir/fechar a aba não
  escreve em nenhum device (read-only provado por ausência de writes no fluxo). Validação ao
  vivo obrigatória.

### 8BIT-04 — Teste de não-respingo + requisitos cedidos à frente DEDUP

- **Quem**: CLAUDE. **Prioridade**: P1. **Arquivos**: `tests/` (só). **Esta frente NÃO edita
  `install.sh`, `uninstall.sh` nem `daemon_actions.py`** — são da frente DEDUP; duas frentes
  nos mesmos arquivos = conflito garantido (refutação da lente de escopo).
- O item original (regra udev + aposentar launch option, como P0 daqui) foi **desmontado pela
  revisão**. O que esta frente entrega:
  1. **O caso de teste de não-respingo**: `udevadm test` no devpath do 8BitDo (resolvido
     dinamicamente por VID:PID) provando que `ID_INPUT_JOYSTICK` permanece `1` para
     `057e:2009` com a regra da DEDUP instalada — automatizado (regra aplicada em ambiente de
     teste) + verificação ao vivo. Precedente: `78-dualsense-motion-not-joystick.rules`.
  2. **Requisitos por escrito, entregues ao item da DEDUP** (esta seção É o registro):
     - Aposentar `IGNORE_DEVICES`/`SDL_JOYSTICK_HIDAPI=0` é **CONDICIONAL**, não consequência
       automática da regra udev: `ID_INPUT_JOYSTICK=0` cega só o backend evdev/joystick — o
       SDL HIDAPI enumera hidraw DIRETO e ignora propriedades udev, o grab do daemon não
       bloqueia hidraw, e a máscara Edge emite `PROTON_ENABLE_HIDRAW=1`, que reexpõe o
       DualSense físico ao jogo (risco já registrado na memória do projeto: "o HIDAPI pode
       escapar do udev"). Só remover após prova em jogo real, **nas duas máscaras, nativo E
       Proton**, de que a dedup fica de pé sem a launch option — ou prova de que o rumble do
       Edge funciona sem `PROTON_ENABLE_HIDRAW` (FF via evdev do `hid_playstation` — plausível,
       não testado).
     - Retirar a launch option do `compose_launch` **não limpa o que JÁ está persistido**
       (`localconfig.vdf` linha ~914, Sackboy): a DEDUP precisa de detecção no doctor por appid
       + **remoção assistida com Steam fechado** (padrão `disable_steam_input.sh:158-178`).
       "A UI orienta a remover" é burocracia colável ao contrário e viola a regra de ouro.
- **PROIBIÇÃO (lente de escopo, literal)**: é proibido documentar "`SDL_JOYSTICK_HIDAPI=0` era
  nocivo aos controles de terceiros" como verdade. Nenhuma falha do 8BitDo passa pela launch
  option (mortes em BT, fora de jogo); com Steam Input OFF por app — o estado real dela —
  `HIDAPI=0` até EVITA que o jogo vire um terceiro mestre no hidraw do clone
  (neutro-a-protetor). O motivo real para aposentá-la é o da frente DEDUP: **opção persistida ×
  vpad de flavor/backend variável → jogo com ZERO controles.** A remoção não é "blindagem de
  terceiros" — é higiene, e o benefício ao 8BitDo é latente.
- **Aceite**: teste de não-respingo presente e verde no gate + `udevadm test` ao vivo com a
  regra instalada mostrando `ID_INPUT_JOYSTICK=1` no 8BitDo; os requisitos acima referenciados
  pelo doc da frente DEDUP; `git diff` desta frente com zero linhas em
  `install.sh`/`uninstall.sh`/`daemon_actions.py`.

### 8BIT-06 — UMA página de troubleshooting (não um manual multi-marca)

- **Quem**: CLAUDE. **Prioridade**: P2. **Arquivos**: `docs/`.
- Uma página só — a versão documental da "super central" também está vetada:
  - Identificar o modo do SN30 Pro: OUI `E4:17:D8` vs VID apresentado; `057e:2009` +
    `hid-nintendo` = modo Switch; `045e:028e` + `xpad` = modo X-input **por cabo** (por BT o
    X-input cai em `hid-microsoft`/`hid-generic`, PID provável `02e0`/`02fd`).
  - O que cada modo expõe: gyro SÓ em Switch (e SÓ chega ao jogo com Steam Input ativo — que o
    guard do hefesto desliga por app; dizer o conflito com todas as letras); rumble em ambos.
  - A assinatura de morte por BT (cascata de `timeout waiting for input report` →
    `joycon_enforce_subcmd_rate`) e que ela pode aparecer sem ser terminal.
  - Os comandos de diagnóstico usados hoje: `systemd-hwdb query OUI:...`, `journalctl -b -k`
    filtrado (sem sudo), readlink do driver no sysfs, `udevadm info` resolvendo o node por
    VID:PID (nunca `eventN` fixo), sonda de fd por `/proc/PID/fd`.
  - O "aparece como Xbox" documentado como hipótese (winebus/Proton OU Steam Input), não fato.
- **Aceite**: doc existe, passa no gate `validar-acentuacao`, e reproduzir os comandos nele
  identifica corretamente o modo do controle na máquina dela.

## Ordem

`8BIT-05` (humano — destrava o controle HOJE, sem código) → `8BIT-03` (doctor, redesenhado) →
`8BIT-01` (inventário) → `8BIT-02` (aba, após o OK de produto e a fusão com a frente
multi-controle) → `8BIT-04` (junto do cronograma da DEDUP) → `8BIT-06` (doc).

## Armadilhas conhecidas que esta frente atravessa

- **Enumeração evdev custa 10-40 ms** e o GIL já é gargalo: inventário SEMPRE em
  executor/thread, sob demanda, nunca no tick (PERF-MULTI-CONTROLLER-01).
- **`eventN` renumera a cada replug**: testes e docs resolvem por VID:PID.
- **O vpad uhid vive sob `/devices/virtual/misc/uhid`** e tem MAC forjado próprio por jogador
  (`02:fe:00:00:00:0N`): o inventário exclui por `/devices/virtual`, e o daemon já aprendeu uma
  vez (UHID-02) a não adotar o próprio vpad — não regredir.
- **Sudo-zero na GUI** (decisão do commit bfd51db): nenhum clique da aba pede senha; o doctor
  usa `journalctl -b -k` (grupo `adm`), não `dmesg`.
- **Dropdowns quebram no COSMIC** (bug de foco do cosmic-comp): a aba usa cards e botões
  segmentados, sem popups.
- **udev**: qualquer regra com `uaccess` precisa de número `< 73` (a ACL vem da
  `73-seat-late.rules`) e nós em `SUBSYSTEM=misc` exigem `udevadm trigger
  --subsystem-match=misc` — relevante para o teste do `8BIT-04` contra a regra da DEDUP.
- **Máscara `0x03` no valid_flag do rumble e `_INPUT_PAYLOAD_SIZE=63`**: intocados por esta
  frente, mas qualquer teste que encoste no vpad uhid respeita os dois (lição UHID-02).
- **`kernel.dmesg_restrict=1`**: o `dmesg` cru exige sudo; o caminho sem sudo é o journal.

## Referências

- Frente DEDUP (dona da regra udev, do `compose_launch` e da limpeza da launch option
  persistida): doc do sprint Edge-dedup desta onda.
- `2026-07-16-sprint-edge-dedup-e-fechamento.md` (estado UHID-04, launch options atuais).
- Pedidos 1/3/4 da Vitória (frente multi-controle/Status): a aba do `8BIT-02` é compartilhada.
- Kernel: `drivers/hid/hid-nintendo.c` (`joycon_enforce_subcmd_rate`), `drivers/input/joystick/xpad.c`
  (USB-only), `hid-microsoft` (aliases BT `045e:02e0/02fd`).
- Evidências ao vivo desta frente: dmesg/journal de 2026-07-16 (sessões `0005:057E:2009.0008` e
  `.0014`, instância USB `.0015`), `localconfig.vdf` (linhas ~914/1103/1108), `modinfo
  xpad`/`hid_microsoft`, `systemd-hwdb query OUI:E417D8`.
