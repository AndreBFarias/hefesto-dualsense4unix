# Sprint 2026-07-16 — DEDUP: a desduplicação deixa de depender de launch option colada

**Status: PLANO — nada daqui foi construído.** Este doc nasce do Estudo 1 (117 agentes,
2026-07-16) + relato ao vivo da Vitória + revisão adversarial de 3 lentes (técnica,
regressão, escopo). A causa-raiz e a solução **sobreviveram** à revisão, mas quatro
pedaços do desenho original foram **REFUTADOS** e estão corrigidos aqui — não construir
pelo dossiê original, construir por ESTE doc. Branch `sprint/harmonia-uhid`.

## O veneno, em uma frase

A dedup de hoje é uma env **ESTÁTICA** por jogo (`SDL_GAMECONTROLLER_IGNORE_DEVICES=
0x054c/0x0ce6` persistida no `localconfig.vdf`) que pressupõe um estado **DINÂMICO**
(vpad vivo como Edge `054c:0df2`); quando o pressuposto falha — EIO de BT no blueprint,
controle ligado depois do daemon, modo Nativo sem vpad, daemon morto — a env esconde o
único controle que restou e o jogo fica com **ZERO controles**. Foi exatamente o que a
Vitória relatou hoje ("em BT nada funciona", RDR2 incluso).

## TL;DR da solução (dupla A+B, tudo sudo-zero em runtime e default no install)

- **(A) O vpad SEMPRE nasce Edge `0df2`** — fecha as três formas de o pressuposto
  quebrar: blueprint **canônico** como caminho default quando o físico é BT
  (DEDUP-02), retry+cache como otimização (DEDUP-01), promoção a uhid também no
  **hotplug** e re-seleção na GUI deixando de ser NO-OP (DEDUP-03). O fallback
  `uinput/0ce6` fica restrito a "`/dev/uhid` inutilizável" — e aí a GUI grita
  (DEDUP-06).
- **(B) A env vira DINÂMICA no momento do launch** — wrapper `hefesto-launch
  %command%` (string **constante**, caminho absoluto no `$HOME`) que decide as envs na
  hora, consultando o estado **REAL** do daemon via connect()+ping IPC (nunca "o
  arquivo de socket existe"), com degradação garantida: wrapper ausente ou daemon
  morto → **nenhuma env** → físico visível → o jogo **sempre abre e sempre tem
  controle** (DEDUP-04). A aplicação no `localconfig.vdf` é assistida, com **migração
  obrigatória** das strings velhas nossas (DEDUP-05).

**Promessa honesta (corrigida pela revisão):** *nenhum estado NO MOMENTO DO LAUNCH
deixa o jogo com zero controles.* Env é congelada no spawn — degradação DEPOIS do
launch (flap de BT, daemon cai no meio do jogo) não é coberta por nenhuma solução via
env: depende de DEDUP-01/02/03, do guard DEDUP-06 e da **histerese do autoswitch**
(frente separada — as duas têm de ser entregues juntas). O novo pior caso é **controle
duplicado**, nunca zero — e o guard aponta.

**A launch option NÃO morre nesta onda.** Ela vira uma string única, imutável e
fail-safe, aplicada com um clique. Sem o clique, o default pós-install é DUPLICADO
(nunca zero controles). A morte total — esconder o físico sem env nenhuma — exigiria
romper o sudo-zero (ver §Fora desta onda).

## Causa-raiz (SOBREVIVEU às 3 lentes da revisão adversarial)

As três pernas da falha existem no código e foram conferidas linha a linha pelos três
revisores (nenhuma citação alucinada):

1. **EIO de BT sem retry**: `capture_dualsense_blueprint` não tem retry nos feature
   reads; um EIO em 0x05/0x09/0x20 → `uhid_blueprint_sem_mac` → fallback **silencioso**
   para `uinput/0ce6` (`integrations/uhid_gamepad.py:357-381`). PROVADO NO CÓDIGO.
2. **Promoção só no boot**: `upgrade_primary_vpad_to_uhid` tem UM call site
   (`daemon/lifecycle.py:388-393`); a transição offline→online do `reconnect_loop`
   (`daemon/connection.py:208-231`) publica `CONTROLLER_CONNECTED` **sem promover** —
   ligar o controle depois do daemon deixa o vpad em uinput. PROVADO NO CÓDIGO.
3. **Re-seleção é NO-OP**: o early-return de `start_gamepad_emulation` compara **só o
   flavor** (`daemon/subsystems/gamepad.py:296-298`) — uinput e uhid dizem ambos
   `dualsense`, então re-selecionar DualSense na GUI retorna True sem fazer nada.
   PROVADO NO CÓDIGO.
4. O próprio código admite o buraco: no fallback uinput/0ce6 "nenhuma opção o
   desduplica" (`app/actions/daemon_actions.py:229-234`). PROVADO NO CÓDIGO.

E a alternativa udev desenhada em 2026-07-13 (item W1.3 de
`docs/process/sprints/2026-07-13-estudo-ui-ux-multicontrole-coexistencia.md:321-325`,
nunca construída) **não fecha o buraco**: PROVADO AO VIVO (e re-executado
independentemente pelo revisor 3) que o SDL 2.30 desta máquina enumera o DualSense pelo
**HIDAPI lendo `/dev/hidraw` direto** (`path=/dev/hidraw2`), caminho que ignora
`ID_INPUT_JOYSTICK`; e ao tirá-lo só do HIDAPI ele **reaparece pelo evdev** (teste D).
Esconder de verdade exige as duas camadas (propriedade udev + corte de acesso ao
hidraw), mas o corte de ACL derrubaria o **próprio daemon**: ele abre o físico pelo
MESMO hidraw com o MESMO uid dos jogos (`core/backend_pydualsense.py:12`; no modo
Nativo o jogo escreve no hidraw físico, `:179`). PROVADO AO VIVO (`getfacl`: única via
de acesso é `user:vitoriamaria:rw-`).

Por que a launch option atual funciona **quando** o vpad é Edge: PROVADO AO VIVO que
`SDL_GAMECONTROLLER_IGNORE_DEVICES` filtra na camada **Joystick** (não só
GameController) em ambos os backends do SDL 2.30, e o winebus do Proton a respeita
inclusive no caminho hidraw (strings conferidas nos `winebus.so` de 3 Protons).

## O que a revisão adversarial REFUTOU no desenho original (e como o plano mudou)

1. **"Gate do wrapper = o socket IPC existe" — REFUTADO.** Arquivo de socket UNIX
   sobrevive a crash/SIGKILL (o próprio `ipc_server.py:159-178` faz probe+unlink de
   socket STALE no startup — prova interna). PROVADO AO VIVO durante a revisão: neste
   momento a máquina dela tem serviço `inactive`, `daemon.pid` órfão E um socket
   **fake** aceitando conexão no mesmo diretório. Gate corrigido: **connect()+ping IPC
   no socket de PRODUÇÃO por nome exato** (nunca glob — o fake mora ao lado), e a env
   materializada tem de refletir o **backend REAL** de TODOS os vpads (daemon vivo com
   vpad em uinput/0ce6 → **SEM** IGNORE).
2. **"O wrapper roda dentro do pressure-vessel do Proton" — REFUTADO.** Launch options
   embrulham o `%command%` INTEIRO, que inclui o entry point do Steam Linux Runtime —
   o wrapper executa no **HOST, antes** do container (é assim que `mangohud %command%`
   funciona, e é assim que a env colada de hoje já chega ao jogo). O caminho no `$HOME`
   continua certo pelo motivo verdadeiro: instalável pelo passo de **usuário** do
   install.sh, sem sudo, e simétrico no uninstall. O critério de aceite "dentro de
   bwrap simulando o container" testava um cenário que não existe — trocado por launch
   REAL da Steam. O risco real: o processo herda `LD_LIBRARY_PATH`/`LD_PRELOAD` do
   Steam Runtime — helpers do host (o python3 do probe IPC) têm de rodar com essas
   vars limpas, preservando o env original no exec do jogo.
3. **"Prepend preservando LaunchOptions existentes" — REFUTADO duas vezes.**
   (a) Preservar bytes não preserva semântica: `hefesto-launch MANGOHUD=1 <cmd>` faz o
   wrapper tentar EXECUTAR `MANGOHUD=1` → ENOENT → o jogo **não abre**. O wrapper TEM
   de terminar em `exec env "$@"` (nunca `exec "$@"`). (b) Pior: o prepend cego
   PRESERVA O VENENO — a string velha está persistida AGORA no vdf dela (PROVADO AO
   VIVO: linha 914 do `localconfig.vdf`, variante de onda anterior com
   `SDL_JOYSTICK_HIDAPI=0 SDL_GAMECONTROLLER_IGNORE_DEVICES=... __GL_SHADER_DISK_CACHE=...
   %command%`) e continuaria aplicada por fora do wrapper. **Migração é obrigatória e
   P0**: detectar e REMOVER as envs NOSSAS conhecidas antes do prepend; "nunca
   clobberar" vale só para opções genuinamente do usuário.
4. **"Retry de ≤8 s resolve o EIO de BT" — PARCIALMENTE REFUTADO.** A janela de ~5,1 s
   foi medida de manhã, mas a revisão mediu, nas condições reais de produção (daemon
   segurando o físico), **EIO persistente por MINUTOS** (2/2 sondas `HIDIOCGFEATURE`
   nos 3 reports + 4/4 enumerações SDL falharam no `hidraw4`, com o controle BT vivo e
   funcional no evdev). Um retry com teto de 8 s falharia em 100% dessas amostras. A
   ênfase INVERTE: **o blueprint canônico (DEDUP-02) é o caminho DEFAULT quando o
   físico é BT**; retry+cache viram otimização (e o cache só salva controle já visto).
5. **"DEDUP-05 como P1" — REFUTADO (lente do escopo).** A string velha já persistida
   continua envenenando o Sackboy até ser substituída — entregar os P0 sem a migração
   deixa o modo Nativo dela com zero controles. DEDUP-05 **sobe para P0**, inseparável
   do DEDUP-04. E pela regra de ouro, colar na mão não pode ser o caminho suportado.
6. **"DEDUP-07 spike do broker root como item de sprint" — REFUTADO (feature creep).**
   Ela pediu escopo mínimo e a onda acabou de firmar sudo-zero (bfd51db); esqueleto de
   broker é engenharia especulativa na direção contrária. Sai como item; vira o
   parágrafo de limitação em §Fora desta onda.
7. **"Fail-safe por construção / nenhum estado do daemon volta a deixar o jogo com
   zero controles" — overclaim corrigido** para "nenhum estado **no momento do
   launch**" (ver TL;DR).

## Achado NOVO da revisão: por que o BT dela está "conectado sem input"

PROVADO AO VIVO pelo revisor 1: com um gêmeo USB de mesmo VID/PID rastreado pelo
HIDAPI, o DualSense **BT fica invisível ao SDL por INTEIRO** — o backend evdev
deferencia ao HIDAPI por VID/PID, e o HIDAPI não consegue ler o hidraw BT (EIO). Isso
corrobora o relato dela ("BT conectado, nenhum input") **mesmo sem launch option**,
reforça a solução A (o jogo só precisa ver o vpad uhid, cujos feature reads o daemon
serve sem EIO) e mostra que o **modo Nativo/Sony com físico em BT é estruturalmente
frágil**, fora do alcance de qualquer wrapper — GUI e doctor.sh devem avisar
(DEDUP-06). Complemento técnico: descriptor BT (`85 31`, input 0x01 de 10 B) num vpad
`BUS_USB` dimensiona errado o report 0x01 de 64 B — o aviso log-only
`uhid_blueprint_bt_descriptor` (`uhid_gamepad.py:344-355`) já admite "vpad pode nascer
torto"; o DEDUP-02 transforma o aviso em ação.

## Alternativas descartadas (com o porquê)

- **Regra udev `ID_INPUT_JOYSTICK=0` sozinha** (desenho W1.3 de 2026-07-13): cobre só
  o caminho evdev; o HIDAPI lê o hidraw direto (PROVADO AO VIVO). Cobriria a metade
  que não importa.
- **Cortar ACL/uaccess do hidraw físico durante a emulação**: funciona contra o jogo
  (teste E, bwrap), mas derruba o próprio daemon (mesmo hidraw, mesmo uid) a cada
  reconnect de BT. Exigiria broker root — §Fora desta onda.
- **EVIOCGRAB como dedup**: grab é evdev-only; o HIDAPI segue lendo o hidraw e
  entregando inputs ao jogo (origem histórica do duplicado com inputs vivos).
- **`SDL_HIDAPI_IGNORE_DEVICES` e variantes**: o físico volta pelo evdev (teste D) —
  pior que a atual; e qualquer env continua estática por lançamento.
- **Só consertar o fallback e manter a env colada**: não cobre modo Nativo (env
  persistida esconde o físico sem existir vpad → zero controles, relatado hoje) nem
  daemon morto.
- **Editar o vdf automaticamente em silêncio a cada mudança de modo**: a Steam
  sobrescreve o arquivo ao fechar — edição segura exige Steam fechada; fica como ação
  assistida de um clique (precedente do `disable_steam_input.sh`).
- **Env global na sessão da Steam**: estática do mesmo jeito e afeta TODOS os apps SDL
  — contraria o escopo enxuto que a Vitória ditou.

## Efeito nos outros controles (o medo do pedido 4 dela)

- O `IGNORE 0x054c/0x0ce6` é **cirúrgico por VID/PID**: PROVADO AO VIVO que o 8BitDo
  (enumerado como Nintendo Pro Controller `057e:2009` via `hid_nintendo`) permanece
  visível e `IsGameController=1` com a env ativa. A dedup NÃO desliga controles de
  outras marcas — o "descontrolado" do 8BitDo é outra frente.
- **MAS**: a variante xbox do `compose_launch` carrega `SDL_JOYSTICK_HIDAPI=0`, que
  muda o **caminho de leitura de TODOS os controles** do jogo (o Pro Controller sai do
  HIDAPI e vira evdev, expondo inclusive o nó IMU separado). Não esconde, mas altera
  comportamento. A máscara PS/uhid **dispensa** essa env — é o caminho limpo para
  multi-controle.
- Limitação honesta: jogo nativo Linux com SDL2 **antigo estaticamente linkado** pode
  aplicar o IGNORE só na camada GameController (a camada Joystick ainda veria o
  físico) — mesma limitação da launch option de hoje, não é regressão; sob Proton o
  winebus cobre (strings verificadas nos `.so`).

## Itens

### DEDUP-01 — Blueprint resiliente: canônico como rede, retry+cache como otimização
- **Quem**: CLAUDE. **Prioridade**: P0.
- **O que fazer**: em `capture_dualsense_blueprint`, retry com backoff por feature
  read que der EIO — mas com a ênfase corrigida pela revisão: o retry é
  **otimização** (cobre o surto curto), não o mecanismo principal (o EIO de BT foi
  medido persistente por MINUTOS). Ao capturar um blueprint bom, persistir em
  `~/.local/state/hefesto-dualsense4unix/blueprints/` **keyed pelo `HID_UNIQ` do
  sysfs** — nunca pelo MAC do report 0x09, que é exatamente o que não leu no momento
  da falha (furo de bootstrap apontado pela revisão). Na falha com cache presente,
  usar o cache; sem cache, cair no **canônico do DEDUP-02** (não mais em uinput).
  Todo o caminho roda **fora do event loop** (o retry pode levar segundos) e cobre
  explicitamente o **co-op**: cada jogador nasce do hidraw DAQUELE controle
  (`daemon/subsystems/coop.py:407-421`) e cai individualmente em uinput se o blueprint
  dele falhar — o `_promote_player` é chamado do sync e um sleep bloqueante congelaria
  o subsistema. Logar cada degrau (`retry_ok` / `cache_hit` / `canonico` /
  `fallback`).
- **Arquivos**: `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`,
  `src/hefesto_dualsense4unix/integrations/virtual_pad.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/coop.py`,
  `tests/unit/test_uhid_edge_dedup.py`.
- **Critério de aceite**: fake hidraw com EIO nas 2 primeiras leituras → vpad nasce
  uhid/0df2 via retry; EIO permanente + cache presente (chave `HID_UNIQ`) → uhid/0df2
  via cache; EIO permanente sem cache → uhid/0df2 via canônico (DEDUP-02), com log;
  jogador secundário do co-op com EIO → mesmo comportamento SEM congelar o sync
  (teste com timer). O fallback uinput só acontece com `/dev/uhid` inutilizável.
  Gate 2410+ verde.

### DEDUP-02 — Descriptor USB canônico + features reais embarcados (o caminho DEFAULT para físico BT)
- **Quem**: AMBOS (construção CLAUDE; validação BT VITORIA_HUMANO = **gate de
  release**). **Prioridade**: P0.
- **O que fazer**: promover `captures/dualsense_usb_descriptor_054c0ce6.bin` (289 B,
  sem `85 31`, header HID conferido pela revisão) a asset do pacote; em
  `capture_dualsense_blueprint`, quando o descriptor do físico contiver `85 31` (BT),
  usar o canônico **sempre** (o aviso log-only `uhid_blueprint_bt_descriptor` vira
  ação). Embarcar também payloads **REAIS** dos features 0x05/0x20 (capturados do
  gêmeo USB saudável: 41/20/64 B — disponíveis ao vivo) para o último recurso, com o
  MAC do jogador forjado no 0x09 — **nunca zeros**: calibração zerada historicamente
  causou div-by-zero no kernel (kernels recentes sanitizam, antigos não). Duas notas
  técnicas obrigatórias da revisão: (1) features capturados de físico BT carregam
  **CRC32 nos 4 bytes finais** — benigno no vpad `BUS_USB` (o `hid_playstation` só
  valida CRC quando bus==BLUETOOTH), mas o teste unitário precisa saber para não
  "normalizar" errado; (2) calibração de outra unidade desloca levemente a escala do
  IMU do vpad — aceitável, documentado.
- **Arquivos**: `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`,
  `captures/dualsense_usb_descriptor_054c0ce6.bin`, `pyproject.toml` (asset),
  `tests/unit/test_uhid_edge_dedup.py`.
- **Critério de aceite**: teste unitário: blueprint com descriptor BT (`85 31`) → vpad
  criado com o canônico de 289 B e log da substituição; features BT com CRC32 passam
  intactos; último recurso monta blueprint com payloads reais + MAC forjado → vpad
  Edge. **VALIDAÇÃO HUMANA (gate de release, nunca formalidade)**: DualSense pareado
  por BT + máscara DualSense → kernel binda `Registered DualSense Edge` e
  **inputs + rumble + gyro + touchpad** funcionam no jogo (a revisão exigiu
  gyro/touchpad porque features de BT parseados como USB podem corromper calibração).
  Pior caso permitido: fallback atual + guard gritando — **nunca pior que hoje**.
- **Risco declarado**: o descriptor canônico com físico em BT nunca foi validado ao
  vivo (o código atual só loga o aviso admitindo que o vpad pode nascer torto —
  `uhid_gamepad.py:344-355`). HIPÓTESE FORTE, não fato.

### DEDUP-03 — Promoção a uhid no HOTPLUG + re-seleção na GUI deixa de ser NO-OP
- **Quem**: CLAUDE. **Prioridade**: P0.
- **O que fazer**: chamar `upgrade_primary_vpad_to_uhid` na transição offline→online
  do `reconnect_loop` (`daemon/connection.py:208-231`, após publicar
  `CONTROLLER_CONNECTED`) — **via `_run_blocking`**, exigência da revisão: a captura
  do blueprint faz I/O bloqueante (os.open + ioctl no hidraw) e, com o retry do
  DEDUP-01, pode levar segundos; chamada direta congela o event loop (a chamada atual
  do lifecycle já bloqueia brevemente — não replicar o vício). E corrigir o
  early-return de `start_gamepad_emulation` (`gamepad.py:296-298`) para comparar
  **(flavor, backend)**, de modo que re-selecionar DualSense com vpad em uinput tente
  o upgrade. Atenção da revisão: isso **revoga a premissa** da docstring de
  `gamepad.py:240-242` ("a janela real é o boot, sem jogo") — a promoção agora pode
  acontecer com jogo aberto; o guard só-age-se-uinput (`gamepad.py:246-248`) limita a
  janela, e o caso uinput-mid-game é justamente o alvo. Atualizar a docstring.
- **Arquivos**: `src/hefesto_dualsense4unix/daemon/connection.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
  `tests/unit/test_uhid_edge_dedup.py`.
- **Critério de aceite**: teste: daemon sobe sem controle (vpad uinput) → simular
  connect via reconnect_loop → vpad promovido a uhid/0df2 sem reiniciar o daemon e sem
  bloquear o loop (asserção de que a promoção rodou via `_run_blocking`); teste: com
  vpad uinput e hidraw disponível, `start_gamepad_emulation('dualsense')` NÃO retorna
  cedo e promove. AO VIVO: ligar o controle DEPOIS do daemon e ver a promoção no
  journal.

### DEDUP-04 — Wrapper `hefesto-launch`: string constante, decidida na hora, fail-safe de verdade
- **Quem**: CLAUDE. **Prioridade**: P0. **Pacote com DEDUP-06** (exigência da
  revisão: o wrapper é snapshot no launch; degradação pós-launch só o guard cobre —
  se 04 entra, 06 entra junto).
- **O que fazer**: wrapper POSIX-sh instalado por default pelo passo de **usuário** do
  install.sh (sem sudo, sem flag) em
  `~/.local/share/hefesto-dualsense4unix/bin/hefesto-launch`. Ele **roda no HOST**
  (modelo corrigido pela revisão — launch options embrulham o entry point do SLR):
  1. Lê `$SteamAppId`; `SteamAppId` ausente/0 (atalho não-Steam) → fail-safe (nenhuma
     env nossa).
  2. Gate de vida: **connect()+ping IPC no socket de PRODUÇÃO por nome exato**
     (`utils/xdg_paths.py` — nunca glob: o socket FAKE convive no mesmo diretório;
     arquivo de socket sobrevive a crash, provado por `ipc_server.py:159-178`). O
     helper do probe (python3) roda com `LD_LIBRARY_PATH`/`LD_PRELOAD` **limpos** (o
     processo herda o env do Steam Runtime scout), preservando o env original no exec
     do jogo.
  3. Carrega o arquivo de env materializado por appid em
     `~/.local/state/hefesto-dualsense4unix/launch_env/` — que o daemon **regrava** em
     TRÊS gatilhos: mudança de perfil/config, **transição de backend do vpad
     (uhiduinput)** e mudança do conjunto de jogadores. O conteúdo reflete o backend
     **REAL agregado por jogador** (espelhando a honestidade de
     `daemon_actions.py:229-234`): dualsense+uhid/0df2 em TODOS os vpads →
     `PROTON_ENABLE_HIDRAW=1` + IGNORE + preload; xbox → `SDL_JOYSTICK_HIDAPI=0` +
     IGNORE + preload; nativo → `PROTON_ENABLE_HIDRAW=1` **sem** IGNORE; **qualquer**
     vpad em uinput/0ce6 → **SEM IGNORE** (duplicado > zero controles). Perfil sem
     `steam_app_<appid>` no `window_class` → arquivo de env DEFAULT (máscara/backend
     globais atuais) — resolução no MÍNIMO, sem UI de biblioteca de jogos.
  4. Termina em **`exec env "$@"`** (nunca `exec "$@"`): LaunchOptions pré-existentes
     no formato `VAR=VAL %command%` — o formato que o PRÓPRIO hefesto emite hoje
     (`tests/unit/test_storm_launch_options.py:10-49`) — viram `$1` após o prepend e
     `env(1)` os processa como assignment; `exec "$@"` tentaria executá-los → ENOENT →
     jogo não abre.
  - A string que `compose_launch` devolve vira **constante** e **degrada sozinha**
    quando o wrapper faltar (modo de falha novo apontado pela revisão: caminho órfão
    no vdf = jogo que NÃO abre, pior que a env inerte de hoje). Forma candidata (a
    validar na construção, com escaping VDF):
    `sh -c 'W="$HOME/.local/share/hefesto-dualsense4unix/bin/hefesto-launch"; [ -x "$W" ] && exec "$W" "$@"; exec env "$@"' hefesto-launch %command%`
  - **Uninstall simétrico e na ORDEM certa**: limpar o vdf ANTES de apagar o wrapper
    (regra histórica: assimetria já quebrou o mic dela; aqui quebraria o launch dos
    jogos). **Steam flatpak/snap**: proibido escrever caminho do host no vdf deles sem
    wrapper visível à sandbox (os globs do projeto já tratam `~/.var/app` e `~/snap` —
    `disable_steam_input.sh:57-62`); nesses layouts, recusar com mensagem clara.
  - doctor.sh ganha check do wrapper + da materialização.
- **Arquivos**: `assets/hefesto-launch.sh` (novo), `install.sh`, `uninstall.sh`,
  `scripts/doctor.sh`, `src/hefesto_dualsense4unix/app/actions/daemon_actions.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
  `tests/unit/test_storm_launch_options.py`.
- **Critério de aceite** (casos corrigidos pela revisão — o cenário bwrap foi
  descartado por testar algo que não existe): (a) daemon vivo + perfil gamepad do
  appid → env contém IGNORE e `PROTON_ENABLE_HIDRAW`; (b) perfil nativo → SEM IGNORE;
  (c) **daemon vivo + vpad em uinput/0ce6 → SEM IGNORE** (o caso que o desenho
  original não testava); (d) socket órfão/stale presente + daemon morto → NENHUMA env
  (gate por connect, não por existência); (e) wrapper apagado → o jogo AINDA abre
  (degradação da string); (f) LaunchOptions pré-existente `MANGOHUD=1 %command%`
  continua funcionando após o prepend (`exec env`); (g) `compose_launch` devolve
  string idêntica para qualquer máscara/backend (unitário); (h) **launch REAL pela
  Steam**: `$SteamAppId` presente no processo do wrapper e envs propagadas até o jogo
  dentro do pressure-vessel (validação ao vivo, é assim que a env de hoje já viaja).

### DEDUP-05 — Aplicação assistida no vdf + MIGRAÇÃO do veneno legado + popup automático
- **Quem**: AMBOS (construção CLAUDE; clique e validação VITORIA_HUMANO).
  **Prioridade**: **P0** (promovido pela revisão — sem a migração, o modo Nativo dela
  continua com zero controles mesmo com DEDUP-01..04 entregues).
- **O que fazer**: ação na GUI "Aplicar aos jogos da Steam" que escreve a string
  constante do wrapper no `LaunchOptions` do `localconfig.vdf`, reusando o fluxo do
  `disable_steam_input.sh:54-137` (globs, `steam -shutdown` com timeout, backup
  `.bak`, idempotente). Exigências da revisão, todas obrigatórias:
  1. **Migração**: detectar e REMOVER as strings NOSSAS conhecidas já persistidas
     (`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`, `PROTON_ENABLE_HIDRAW=1`,
     `SDL_JOYSTICK_HIDAPI=0`, `__GL_SHADER_DISK_CACHE*` — todas as variantes que o
     `compose_launch` de hoje e o de ondas anteriores emitiram) **antes** do prepend.
     PROVADO AO VIVO que a variante velha está na linha 914 do vdf dela. "Nunca
     clobberar" vale só para opções genuinamente do usuário (mangohud etc.), que são
     preservadas por inteiro via `exec env`.
  2. **Guard de jogo rodando**: `steam -shutdown` com jogo aberto MATA o jogo — o
     fluxo recusa quando houver jogo ativo (o `steam_running` atual detecta a Steam,
     não o jogo; estender a detecção).
  3. **Escaping VDF** (aspas/backslash) e as DUAS formas de merge: LaunchOptions com e
     sem `%command%` têm semânticas diferentes na Steam.
  4. **Popup automático** (pedido 5 da Vitória): quando a emulação sobe e a launch
     option ainda não está aplicada ao jogo do perfil ativo, mostrar dialog com a
     string e o botão de aplicar — **dialog, não popover/dropdown** (bug de foco do
     cosmic-comp derruba popups; regra histórica do projeto).
  5. Remoção simétrica no uninstall (a string nova E as variantes velhas nossas), na
     ordem do DEDUP-04 (vdf antes do wrapper). Flatpak/snap: mesma recusa do DEDUP-04.
  6. Dizer na UI com todas as letras: **sem o clique, o comportamento é controle
     duplicado no jogo** (nunca zero) — e cada jogo NOVO repete o ritual do
     popup+clique enquanto a limitação de §Fora desta onda existir.
- **Arquivos**: `scripts/disable_steam_input.sh` (extrair helper de edição do vdf),
  `src/hefesto_dualsense4unix/app/actions/daemon_actions.py`,
  `src/hefesto_dualsense4unix/app/`, `uninstall.sh`,
  `tests/unit/test_storm_launch_options.py`.
- **Critério de aceite**: dry-run imprime o diff do vdf sem tocar no arquivo; vdf com
  a string VELHA nossa → aplicar remove a velha e instala a do wrapper (teste com a
  string real da linha 914 dela); `MANGOHUD=1 %command%` do usuário → preservado e
  funcional; aplicar 2x é no-op; com jogo rodando → recusa com mensagem; uninstall
  remove o nosso trecho (novo e legado) e deixa o resto intacto. **VALIDAÇÃO
  HUMANA**: Vitória clica, abre o Sackboy e vê layout PS sem duplicar.

### DEDUP-06 — Guard anti-veneno: dedup quebrada nunca mais é silenciosa
- **Quem**: CLAUDE. **Prioridade**: **P0** (pacote com DEDUP-04 — exigência da
  revisão: não deixar escorregar como "P1 descartável").
- **O que fazer**: expor no `state_full` a flag `dedup_ok` **agregada POR JOGADOR**
  (correção da revisão: no co-op cada vpad nasce do hidraw daquele controle e cai
  individualmente em uinput/0ce6 — `coop.py:407-421`; identidade `path:` sem MAC →
  uinput garantido, `:395-405`; um único jogador em 0ce6 com IGNORE congelado = AQUELE
  jogador com zero controle enquanto um `dedup_ok` só-do-P1 mentiria). Quando falso
  com emulação ligada: aviso vermelho persistente na GUI ("o jogo pode ver dois
  controles ou nenhum — reconecte o controle ou use a máscara Xbox"), log
  `dedup_broken` com motivo (`sem_uhid` / `blueprint_falhou` / `hotplug_pendente` /
  `jogador_N_uinput`) e o mesmo check no doctor.sh via IPC. **Mais o aviso do achado
  novo**: físico primário em **BT + modo Nativo** → aviso na GUI e no doctor (o SDL
  pode não enxergar o físico BT nem sem launch option — fragilidade estrutural fora do
  alcance do wrapper). O guard é também quem aponta o novo pior caso ("duplicado")
  quando o wrapper degradou.
- **Arquivos**: `src/hefesto_dualsense4unix/daemon/ipc_handlers.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/coop.py`,
  `src/hefesto_dualsense4unix/app/`, `scripts/doctor.sh`.
- **Critério de aceite**: daemon fake com P1 uhid/0df2 e P2 uinput/0ce6 → `dedup_ok`
  false com motivo `jogador_2_uinput`; GUI renderiza o aviso (snapshot do estado);
  doctor.sh reporta `[WARN]` nesse estado e `[OK]` com todos os vpads Edge; físico BT
  + modo Nativo → aviso específico nos dois lugares.

## Fora desta onda (limitação registrada — SEM item de sprint)

Esconder o físico **sem env nenhuma** — a única forma de a launch option morrer por
completo — exigiria as duas camadas provadas nos testes D/E (udev tira
`ID_INPUT_JOYSTICK` **e** o acesso ao hidraw do físico enquanto emula), e o corte de
acesso derruba o próprio daemon, que abre o físico pelo mesmo hidraw com o mesmo uid
dos jogos. Consertar isso exige **broker root com fd-passing (SCM_RIGHTS)** ou daemon
com uid/grupo próprios — incompatível com o sudo-zero em runtime firmado em
`bfd51db`. Fica registrado como limitação e decisão de OUTRA onda; a revisão
adversarial cortou o spike (esqueleto de broker) desta por feature creep. Até lá:
cada jogo precisa da string do wrapper aplicada uma vez (um clique), e sem ela o
comportamento é duplicado — nunca zero controles.

## Regra de ouro (ditada pela Vitória) — como o plano a cumpre

- **Tudo no install por default, sem flags**: o wrapper e o diretório `launch_env/`
  entram pelo passo de usuário do `install.sh` (sem sudo, sem flag); nenhum passo novo
  de root é necessário nesta frente. Flags, se existirem, só como opt-out.
- **Uninstall simétrico**: remove wrapper + `launch_env/` + as strings nossas do vdf
  (novas E legadas), na ordem vdf→wrapper.
- **Sudo-zero em runtime**: nada aqui pede senha num clique — o gate é IPC, a
  materialização é arquivo do usuário, a edição do vdf é arquivo do usuário.
- **doctor.sh sabe verificar**: wrapper presente/executável, materialização viva,
  string nos jogos, `dedup_ok`, aviso BT+Nativo.
- **Admissão honesta exigida pela regra**: a dedup na máscara DualSense ainda depende
  de UMA ação por jogo (clique com a Steam fechada). Pela régua "se só funciona quando
  a usuária cola algo, não está pronta", esta frente NÃO encerra o assunto — ela mata
  o veneno (zero controles) e reduz a colagem a um clique assistido; a morte total é
  a limitação acima.

## Dependência cruzada declarada

Sem a **histerese do autoswitch** (frente separada — `profiles/autoswitch.py:69-74`,
wm_class `unknown` transitório derruba a emulação no meio do jogo, medido ao vivo
13:07:18), um jogo lançado com IGNORE pode ficar **sem vpad no flap** mesmo com tudo
desta frente entregue. As duas frentes se completam e devem ser entregues juntas.

## Armadilhas conhecidas que esta frente atravessa

- **MAC próprio por vpad**: `02:fe:00:00:00:0N` em little-endian no report 0x09; MAC
  duplicado = probe falha com -17 (vale para o blueprint canônico do DEDUP-02).
- **valid_flag do rumble é máscara `0x03`, nunca só `0x01`** (firmware >= 0x0215 usa
  HAPTICS_SELECT sozinho no flag0); `_INPUT_PAYLOAD_SIZE=63` (62 = vpad mudo,
  descartado calado pelo driver).
- **udev < 73 para uaccess**: regra numerada depois da `73-seat-late.rules` aplica
  MODE mas não ACL; nós em `SUBSYSTEM=misc` (uhid/uinput) exigem
  `udevadm trigger --subsystem-match=misc`. Relevante porque "uhid inutilizável" —
  o único caso que ainda cai em uinput — JÁ aconteceu nesta máquina por essa ordem.
- **sudo-zero na GUI** (bfd51db): nenhum botão pode virar `sudo`; tudo de root é do
  install (com TTY real — sem TTY o ticket não é herdado pelos filhos).
- **Dropdowns/popovers quebram no COSMIC** (cosmic-epoch#2497 + NVIDIA): o popup do
  DEDUP-05 e o aviso do DEDUP-06 têm de ser dialog/banner, nunca popover.
- **GIL/throttling**: retry e captura de blueprint fazem I/O bloqueante — sempre via
  `_run_blocking`/fora do event loop (DEDUP-01/03); o sync do co-op não pode congelar.
- **Testes ficam em `tests/unit/`** (`test_uhid_edge_dedup.py`,
  `test_storm_launch_options.py`) — a raiz `tests/` não os contém; seguir o dossiê
  original ao pé da letra criaria duplicatas fora do lugar.
- **Invariante do projeto**: teste verde sem validação ao vivo NÃO fecha item — os
  gates humanos do DEDUP-02 (BT com gyro/touchpad) e DEDUP-05 (Sackboy layout PS) são
  bloqueantes de release.

## Ordem

DEDUP-02 (o canônico é a rede de todo o resto) → DEDUP-01 → DEDUP-03 →
DEDUP-04 + DEDUP-06 (pacote) → DEDUP-05 (migração + clique) → validações humanas
(BT no DEDUP-02, Sackboy no DEDUP-05).

## Referências

- Estudo que motivou: Estudo 1 de 2026-07-16 (117 agentes) + relato ao vivo da
  Vitória (BT sem input, RDR2, 8BitDo).
- Desenho udev original (descartado como solução única):
  `docs/process/sprints/2026-07-13-estudo-ui-ux-multicontrole-coexistencia.md:321-325`
  (item W1.3); único `.rules` materializado:
  `assets/78-dualsense-motion-not-joystick.rules`.
- Sprint irmão desta data (Edge dedup entregue + pendências):
  `docs/process/sprints/2026-07-16-sprint-edge-dedup-e-fechamento.md`.
- Código citado (conferido pelas 3 lentes): `integrations/uhid_gamepad.py:344-381`,
  `daemon/lifecycle.py:388-393`, `daemon/connection.py:208-231`,
  `daemon/subsystems/gamepad.py:240-248,296-298`, `daemon/subsystems/coop.py:395-421`,
  `app/actions/daemon_actions.py:226-234`, `daemon/ipc_server.py:159-178`,
  `core/backend_pydualsense.py:12,179`, `scripts/disable_steam_input.sh:54-137`,
  `scripts/doctor.sh:~495-515`, `utils/xdg_paths.py:15-23`.
- Descriptor canônico: `captures/dualsense_usb_descriptor_054c0ce6.bin` (289 B, USB,
  sem `85 31`; BT real = 321 B com `85 31` e input 0x01 de 10 B).
