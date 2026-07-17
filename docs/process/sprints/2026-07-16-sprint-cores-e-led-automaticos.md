# Sprint SPRINT-COR-AUTO-01 — cor automática de lightbar por controle + LED do número do controle

Pedido da mantenedora (2026-07-16, escopo item 3): *"Para cada DualSense conectado,
automaticamente uma COR de coluna diferente no lightbar + o LED indicador do número
do player."* Branch `sprint/harmonia-uhid`.

**Status (2026-07-17): CONSTRUÍDO — COR-01 (identity.py, slot de sessão + rotulagem
CLI/applet), COR-03 (paleta automática como camada do meio no merge por campo:
explícita > auto > global, provider injetado, D1-D12 honradas), COR-04 (toggle na GUI
com a semântica D4 completa), COR-05 (player_slot + lightbar_* no state_full — D8 com
divergência fundamentada: uma cor efetiva + contraste garantido na borda da GUI),
COR-06 (doctor: 7 regras + probe de gravabilidade) e COR-08 (notas). O caminho (4) do
COR-02 fechou via PERFIL-06 (revert do co-op por-uniq); os caminhos (1)(2)(3) já
resolviam por `_merged_desired_for_key` desde a Fase 3. Pendente: COR-07 (validação
humana — roteiro no CHECKLIST_MANUAL.md).** Texto original do plano abaixo.

## TL;DR

Hoje o hefesto não diferencia controles: a lightbar é um estado GLOBAL único
(`_DesiredOutput.led`) aplicado em broadcast — ao vivo os dois DualSense (1 BT + 1 USB)
estão com a MESMA cor `16 32 72` e o MESMO padrão de player-LED (P1). O plano: (A) um
registro de identidade MAC→slot **de sessão** (replug recupera o número; sessão nova
renumera do 1); (B) desired **por-controle** no backend + APIs `set_led_for`/
`set_player_leds_for` (mata o bug do "replug pinta com a cor do outro"); (C) paleta
automática estilo PS5 (P1 azul, P2 vermelho, P3 verde, P4 rosa) aplicada **dentro do
reconcile de hotplug do backend**, com precedência única: camada runtime (co-op) >
cor explícita por-controle > automática pelo slot > global do perfil. Tudo em
userspace: **zero artefato novo de install** (a regra udev 77 já entra sem flag; falta
só o check no doctor — COR-06).

## O problema, na raiz

Não existe atribuição automática de cor/número por controle porque o modelo de estado
de LED é GLOBAL e broadcast. Tudo abaixo é **PROVADO NO CÓDIGO** (file:line conferidos
por 3 revisores independentes) ou **PROVADO AO VIVO** (medido nesta máquina hoje):

1. **`_DesiredOutput` é um slot único por backend** — não há "cor desejada por
   controle" (`core/backend_pydualsense.py:120-137`). [PROVADO NO CÓDIGO]
2. **`set_led` grava nesse global MESMO com alvo selecionado**
   (`backend_pydualsense.py:915-916`: `self._desired.led = color` incondicional, antes
   de o `_for_each_led` resolver o alvo). A escrita física vai só ao alvo, mas o
   desired global fica com a cor do alvo — e o próximo hotplug de OUTRO controle a
   re-aplica nele via `_reapply_desired` (`:555-556`, `:871-906`) e
   `_refresh_sysfs_leds` (`:668-676`). É o bug do **"replugar o Controle 1 o pinta com
   a cor do Controle 2"**. [PROVADO NO CÓDIGO]
3. **O "Controle N" da GUI é a POSIÇÃO no dict `_handles` (+1)** — replug reinsere no
   fim, o número embaralha (`:1000-1011`, `:497`, `:523`). [PROVADO NO CÓDIGO]
4. **O único código que diferencia controles** (padrões canônicos P1..P4 de player-LED,
   `daemon/subsystems/coop.py:60-74`, `:460-497`) está atrás do gate `coop_enabled` e
   escreve sysfs direto, fora do backend. [PROVADO NO CÓDIGO]
5. **Ao vivo**: `cat /sys/class/leds/input{30,75}:rgb:indicator/multi_intensity` →
   ambos `16 32 72`; player-3 brightness=1 nos dois (padrão P1 idêntico). BT =
   input30/hidraw4 (MAC `aa:bb:cc:00:00:02`), USB = input75/hidraw2 (MAC
   `aa:bb:cc:00:00:01`). A origem foi rastreada de ponta a ponta: perfil "Navegação"
   com lightbar `[40,80,180]` × brightness `0.4` = `(16,32,72)` exatos — broadcast do
   perfil confirmado. [PROVADO AO VIVO]
6. **A rota sysfs por-controle funciona nos DOIS transportes AGORA**: escrita real
   (sem sudo, daemon rodando) nos nós do BT e do USB retornou sucesso — inclusive no
   BT, que hoje sofre EIO intermitente em feature reads de hidraw (Estudo 1). A rota
   LED class do kernel é independente do caminho de feature report que falha.
   [PROVADO AO VIVO]
7. **A regra udev 77** (`77-dualsense-leds.rules`, chmod nos nós de LED) já é
   instalada SEM FLAG (`scripts/install_udev.sh:57`) e removida pelo uninstall
   (`uninstall.sh:310-319`) — mas o doctor NÃO a confere (lista canônica só tem
   70/71-uhid/71-uinput/72, `scripts/doctor.sh:92-113`) e o comentário do doctor ainda
   chama a 76 de "opt-in" (falso: é default). [PROVADO NO CÓDIGO + AO VIVO]

## Refutações da revisão adversarial (obrigatórias — mudam o desenho)

### REFUTADO 1: "ancorar a cor na conexão via `notify_controller_connected`"

O rascunho original mandava aplicar a cor automática num "hook no
`notify_controller_connected`". **Isso não existe por-controle**:
`notify_controller_connected` é a notificação de DESKTOP do COSMIC
(`integrations/desktop_notifications.py`, opt-in por env var), e a borda que a dispara
é a transição offline→online do backend INTEIRO (`connection.py:207-231`:
`if is_connected and not was_connected`). **Plugar o 2º DualSense com o 1º já online —
o caso central desta frente — não gera evento nenhum.**

**Correção (adotada nos itens):** a resolução de cor acontece DENTRO da reconciliação
de hotplug do backend — `_probe_and_open → _reapply_desired(key, handle)`
(`backend:555-556`) e os `new_keys` do `_refresh_sysfs_leds` — que é exatamente onde o
replug já repinta hoje. Isso ELIMINA a janela de ~2s (a cor do slot nasce certa no
mesmo tick que abre o handle) em vez de mitigá-la. `connection.py` **sai** da lista de
arquivos do COR-03.

### REFUTADO 2: "o co-op consome o registro de slots" (como estava escrito)

O `player_index` do co-op NÃO é só exibição: ele vai em `make_virtual_pad(player=N)` e
vira o **MAC do vpad uhid** (`player_mac(N)` = `02:fe:00:00:00:{N:02x}`,
`integrations/uhid_gamepad.py:251-258`); MAC repetido mata o probe com `-EEXIST` e o
`make_virtual_pad` cai **em silêncio** no uinput/`0ce6` (`virtual_pad.py:164-170`) — o
caminho envenenado que o Estudo 1 provou (a launch option esconde físico E vpad → zero
controles). O vpad do primário é criado com `player=1` HARDCODED
(`daemon/subsystems/gamepad.py:320-323`). Cenário concreto e comum (flap BT de ~5,1s é
rotina medida): A=slot 1 cai, B vira primário, A reconecta como secundário e o registro
lhe devolve o slot 1 → **vpad do secundário com player=1 colide com o vpad do
primário**.

**Correção (adotada no COR-01):** separar explicitamente **slot de exibição/LED**
(registro novo) de **índice de alocação do vpad** (continua o mecanismo atual,
livre de colisão: primário=1, `_next_player_index` para secundários). O registro NÃO
substitui `_next_player_index` para fins de vpad. Consequência honesta, documentada:
o nome que o jogo lista ("Hefesto Virtual DualSense P{n}") pode divergir do LED/cor
em casos de borda de replug do primário — ver §Decisões D7.

### Contradição COR-02 × COR-04 (resolvida antes de codar)

O rascunho dizia que aplicar cor com alvo "Todos" gravaria "global E por-controle dos
conectados" — o que (a) apagaria os padrões do co-op num apply broadcast e (b) com o
auto ligado (default), UM clique gravaria cor explícita em todos e o toggle "Cores
automáticas" ficaria ligado porém **inerte para sempre** (recuperável só controle a
controle). Semântica decidida em §Decisões D4.

## Decisões de desenho (fechadas — quem codar segue isto)

- **D1 — Ponto de aplicação:** dentro do reconcile do backend (`_reapply_desired` por
  handle recém-aberto + `new_keys` do `_refresh_sysfs_leds`), consultando o resolvido
  POR-KEY. Sem janela de cor global; único transiente restante é o azul default do
  kernel no bind (ver D10).
- **D2 — Slot é numeração DE SESSÃO com reserva para replug, não identidade eterna de
  máquina.** Dentro da sessão: replug recupera o mesmo número (é isso que ela veria
  quebrar). Sessão nova em que só um controle aparece → ele É o slot 1 (LED P1, cor
  azul — o PS5 numera por sessão). A persistência em `controllers.json` só influencia
  restart do daemon com controles ainda presentes; a reserva expira quando a sessão
  esvazia. **Roubo LRU de slots: CORTADO** (YAGNI — a casa tem 2 DualSense + 1 8BitDo;
  o cenário "faltam 4 slots" não existe).
- **D3 — Slot de exibição ≠ índice de alocação do vpad** (ver Refutado 2). O registro
  alimenta LED/cor/rótulos; a alocação de MAC do vpad continua como está.
- **D4 — Semântica de "Todos" (posição default do seletor):** aplicar cor com alvo
  "Todos" grava **SÓ o global** (nunca N cores explícitas por-controle). Se o auto
  está ligado, esse apply **desliga o toggle auto explicitamente, com aviso visível
  na GUI** ("Cores automáticas desligadas para aplicar uma cor única") — senão a
  aplicação seria invisível (a automática venceria). Religar o auto NÃO apaga cores
  explícitas por-controle existentes (elas continuam vencendo onde existirem).
  Desfazer em lote: botão "Voltar todos ao automático" limpa TODAS as explícitas num
  clique. Um 3º controle plugado depois: com auto ligado recebe a cor automática do
  slot; com auto desligado recebe a global.
- **D5 — Modelo de camadas (um dono por conceito):** `camada runtime (padrões do
  co-op, flash branco da hotkey — nunca persistida) > cor explícita por-controle >
  automática pelo slot (se auto ligado) > global do perfil`. Os padrões do co-op viram
  camada runtime ACIMA do desired (nunca gravada) — isso resolve de vez a limitação
  documentada em `coop.py:471-473` ("broadcast durante o co-op sobrescreve").
- **D6 — Rotulagem "Controle N" pelo slot nas TRÊS superfícies juntas**: GUI
  (`status_actions.py:217-232`), CLI (`cli/cmd_controller.py:114`) e applet COSMIC
  Rust (`packaging/cosmic-applet/src/app.rs:746` — rebuild entra pelo install normal,
  que já compila/instala o applet por default). O contrato IPC `controller.target.set`
  **continua posicional 0-based**: o mapeamento slot→index vive na borda de quem
  exibe, com teste cobrindo "seletor mira o controle certo após replug". Renumerar só
  a GUI criaria três superfícies divergentes (o docstring atual promete paridade).
- **D7 — O LED fora do co-op mostra o NÚMERO DO CONTROLE (slot), não o jogador que o
  jogo vê.** Com co-op OFF, todos os controles alimentam o mesmo vpad — para o jogo,
  todos são P1 (`coop.py:600-637`, decisão LEIGO-01b "melhor calar que mentir"). A UI
  e a doc nomeiam **"número do controle"**, nunca "do jogador". Transição: co-op ON →
  o LED passa a mostrar o número de JOGADOR do co-op (alocação do vpad); co-op OFF →
  volta ao slot. Em borda de replug do primário os dois números podem divergir — é
  inerente (jogos atribuem players por ordem de enumeração SDL) e vai dito com todas
  as letras nas notas (COR-08) e testado no jogo real (COR-07 passo 6).
- **D8 — Contrato do IPC (COR-05): pré vs pós-brilho declarado.** A cor que chega ao
  hardware é PÓS-escala de brilho (`led_control.py:113-115`; provado ao vivo:
  `[40,80,180]`×0.4 = `16 32 72` no sysfs). O IPC expõe `lightbar_rgb` = cor-identidade
  PRÉ-brilho (para a frente Status pintar inputs com cor legível — pós-brilho ficaria
  quase preta em perfis de brilho baixo) E `lightbar_rgb_effective` = pós-brilho (o que
  o sysfs mostra; para diagnóstico e testes cruzados).
- **D9 — Chave sem MAC:** o backend tem fallback de key por PATH quando o firmware não
  expõe serial em USB (`backend:399-428`; ramos `path:` no coop). Key `path:` ganha
  **slot volátil de sessão, nunca persistido** (path muda entre boots). O vpad
  (MAC `02:fe:...`) **NUNCA ganha slot** — restringir aos MACs dos handles físicos do
  backend (o filtro `_is_virtual_hidraw` já existe e é usado na enumeração,
  `backend:57-80`, `:418`); atenção: `sysfs_leds.discover()` NÃO filtra virtuais
  (`sysfs_leds.py:124-146`), por isso a atribuição parte dos handles, não do discover.
- **D10 — Cor automática é DualSense-only por natureza** (8BitDo/Pro Controller não
  tem lightbar RGB — ao vivo o 8BitDo enumera como Nintendo `057E:2009` com LEDs
  `green:player-N` que o discover nem enxerga). Coerente com o pedido literal ("para
  cada DualSense conectado"); fica dito para ninguém "consertar" depois como se fosse
  bug. E o kernel `hid_playstation` auto-atribui player-LED no bind: no replug existe
  um **pisca transitório** com o número do kernel até o daemon reafirmar — o critério
  de aceite ao vivo tolera esse pisca em vez de reprovar.
- **D11 — Brilho:** a paleta automática RESPEITA o `lightbar_brightness` do perfil
  (escala o RGB antes do `set_led`, como o caminho atual) — cor automática ignorando o
  brilho pareceria "defeito" num perfil com brilho reduzido.
- **D12 — Gate do Modo Nativo:** nenhum caminho NOVO de escrita de LED
  (`set_led_for`/`set_player_leds_for`/resolução automática) pode ignorar
  `output_mute`, incluindo o snapshot de re-aplicação no unmute
  (`backend:1046-1058`). Os gates existentes em `_for_each_led` (`:851`) e
  `_refresh_sysfs_leds` (`:669`) são o modelo. Hoje o coop escreve sysfs sem gate e
  não é furo só porque co-op e Nativo não coexistem — a refatoração do COR-02 não pode
  quebrar essa invariante por acidente.

## Regra de ouro (install sem flags) — CONFIRMADA pelas 3 lentes

**Zero artefato novo de install/uninstall.** A `77-dualsense-leds.rules` já entra sem
flag (`install_udev.sh:57`, incondicional) e sai sem flag (`uninstall.sh:310-319`,
simétrico); os nós de LED estão graváveis ao vivo nos dois transportes. Nada de
launch option, env var ou "cole isto" novo. A GUI/daemon seguem **sudo-zero em
runtime** (decisão do commit bfd51db). O `controllers.json` é config de runtime do
usuário em `~/.config` (padrão `session.json`; preservado no uninstall salvo
`--purge-config` — coerente com a casa). O único débito da frente é o check do doctor
(COR-06) — "um item no install = um check no doctor".

## Itens

### COR-01 — Registro de identidade MAC→slot de SESSÃO (fundação também da frente perfis-por-controle) — **P0, CLAUDE**

- **O que fazer:** criar `daemon/subsystems/identity.py`: MAC normalizado → slot
  (1..N), menor slot livre na 1ª aparição; no disconnect o slot fica RESERVADO ao MAC
  **dentro da sessão** (replug recupera o mesmo número); quando a sessão esvazia
  (nenhum controle), as reservas expiram e a próxima sessão renumera do 1 (D2). Sem
  roubo LRU (cortado). Persistir em `~/.config/hefesto-dualsense4unix/controllers.json`
  (escrita atômica, padrão `session.json`) **só** para o caso restart-do-daemon-com-
  controles-presentes. Key sem MAC (`path:`) = slot volátil, nunca persistido (D9).
  O vpad (`02:fe:...`) e não-DualSense nunca ganham slot (D9/D10).
  `describe_controllers` ganha `player_slot`. Rotulagem "Controle N" pelo slot nas
  três superfícies (D6): GUI + CLI + applet, com mapeamento slot→index na borda (o
  IPC `controller.target.set` continua posicional). **O registro NÃO substitui o
  índice de alocação do vpad do co-op** (D3 — Refutado 2): `_next_player_index` e o
  `player=1` do primário ficam como estão.
- **Arquivos:** `src/hefesto_dualsense4unix/daemon/subsystems/identity.py` (novo),
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py`,
  `src/hefesto_dualsense4unix/app/actions/status_actions.py`,
  `src/hefesto_dualsense4unix/cli/cmd_controller.py`,
  `packaging/cosmic-applet/src/app.rs`.
- **Critério de aceite (verificável):** unitários: conectar A,B → slots 1,2;
  desconectar A e reconectar → A volta ao 1 (não vira 2); restart do daemon com
  controles presentes preserva slots; **sessão nova com só o controle
  historicamente-slot-2 → ele vira slot 1**; vpad `02:fe` jamais recebe slot; key
  `path:` não persiste. GUI/CLI/applet exibem o MESMO número para o mesmo controle
  físico após replug; teste do seletor: com rótulo por slot, `controller.target.set`
  ainda mira o controle certo após replug (mapeamento slot→index coberto).

### COR-02 — Backend: desired POR-CONTROLE + `set_led_for`/`set_player_leds_for` + cobertura de TODOS os caminhos que re-aplicam o global — **P0, CLAUDE**

- **O que fazer:** mapa de desired por-key no `PyDualSenseController` + APIs
  parametrizadas `set_led_for(uniq, rgb)` / `set_player_leds_for(uniq, bits)` (rota
  sysfs por MAC — validada ao vivo em USB E BT — com fallback pydualsense por handle).
  Honestidade técnica: `_for_each_led` JÁ honra o `_output_target_key`
  (`backend:830-835`) — escrita por-alvo existe parcialmente como estado global de
  seleção da GUI; o que falta é a API por PARÂMETRO (usar o seletor global a partir do
  coop correria com a seleção da usuária). O docstring "em TODOS os controles"
  (`:945-946`) está stale — corrigir. `set_led`/`set_player_leds` com
  `_output_target_key` ativo gravam no desired DAQUELE controle (não no global).
  **Caminhos que re-aplicam o global e TÊM de consultar o por-key (lista fechada pela
  revisão):** (1) `_reapply_desired` (hotplug-in, `:871-906`); (2)
  `_refresh_sysfs_leds` new_keys (`:668-676`); (3) **`set_output_mute(False)`** — o
  unmute ao sair do Modo Nativo hoje repinta TODOS os nós com o global
  (`:1046-1058`); (4) **`coop._revert_player_leds`** — desligar o co-op faz broadcast
  do padrão do perfil (`coop.py:532-552`) e `_profile_player_leds` lê o `_desired`
  global direto (`:499-513`). Sem (3) e (4), "cor sobrevive" passa nos testes e quebra
  no primeiro jogo nativo ou toggle de co-op. Refatorar
  `coop._apply_coop_player_leds`/`_revert_single_player_led` para as APIs novas como
  **camada runtime** (D5 — nunca persistida), removendo a escrita sysfs duplicada.
  **Semântica declarada para cada escritor broadcast existente** (senão o atropelo só
  muda de endereço): `ipc_draft_applier` (Aplicar da GUI → passa pelo resolvedor de
  perfil), `ipc_handlers` `led.set` (com alvo → por-key; sem alvo → global transiente),
  `udp_server` (protocolo DSX externo → global transiente), `plugin_api/context`
  (idem ipc), `hotkey` (flash branco → camada runtime transiente por design; o apply
  de perfil seguinte re-resolve), `cli/cmd_test` (diagnóstico transiente). O
  `ProfileManager` é instanciado em ≥3 lugares (`connection.py` restore, `hotkey.py`,
  IPC) — o resolvedor chega aos três. Gate `output_mute` em todo caminho novo (D12).
- **Arquivos:** `src/hefesto_dualsense4unix/core/backend_pydualsense.py`,
  `src/hefesto_dualsense4unix/core/controller.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/coop.py`.
- **Critério de aceite (verificável):** teste: com alvo=Controle 2, `set_led`
  (vermelho); simular replug do Controle 1 → `_reapply_desired` NÃO pinta o C1 de
  vermelho. Teste: sair do Modo Nativo (`set_output_mute(False)`) re-aplica o
  resolvido POR-KEY de cada controle, não o global em todos. Teste: desligar o co-op
  devolve o padrão do SLOT (auto ligado) ou o do perfil (auto desligado) — nunca
  broadcast cego do `_desired` global. Teste: `set_led_for` escreve só no nó sysfs do
  MAC alvo. Teste: flash da hotkey não persiste em nenhum desired. Nenhum caminho novo
  escreve com `output_mute` ativo.

### COR-03 — Cores automáticas por controle (paleta PS5) + player-LED do número do CONTROLE fora do co-op — **P0, CLAUDE**

- **O que fazer:** paleta canônica em `led_control.py`: P1 azul, P2 vermelho, P3
  verde, P4 rosa, P5+ branco (cores do PS5 por ordem de conexão — as "colunas"
  distinguíveis que ela pediu). Campo novo `leds.auto_player_colors` (default True) no
  schema (atenção `extra=forbid` → COR-08). Resolução POR CONTROLE com a precedência
  única de D5, **ancorada no reconcile do backend (D1 — NÃO em
  `notify_controller_connected`, refutado)**: a cor do slot nasce no mesmo tick que
  abre o handle. Player-LED idem: fora do co-op acende o padrão canônico do SLOT
  (auto ligado) — nomeado "número do controle" na UI/doc (D7); os checkboxes manuais
  do perfil valem com auto desligado. A automática respeita `lightbar_brightness`
  (D11). Restrito aos MACs dos handles físicos (nunca o vpad `02:fe` — D9);
  DualSense-only (D10). Gate `output_mute` (D12).
- **Arquivos:** `src/hefesto_dualsense4unix/core/led_control.py`,
  `src/hefesto_dualsense4unix/profiles/schema.py`,
  `src/hefesto_dualsense4unix/daemon/subsystems/identity.py`,
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py`.
  (`connection.py` SAIU da lista — ver Refutado 1.)
- **Critério de aceite (verificável):** testes de precedência (runtime > explícita >
  auto > global; auto OFF = comportamento histórico broadcast). Em Modo Nativo nenhuma
  escrita automática acontece. **Ao vivo (com o daemon rodando): plugar os 2 DualSense
  (1 BT + 1 cabo) → cada um acende cor DIFERENTE + LED do seu número automaticamente,
  sem clicar nada, nos dois transportes** (conferível por `cat multi_intensity`/
  `brightness` nos nós `input*`). O critério ao vivo TOLERA o pisca transitório do
  kernel no bind/replug (D10) — reprova só se o estado FINAL estiver errado.
  Invariante da casa: teste verde sem validação ao vivo NÃO fecha o item.

### COR-04 — GUI aba Lightbar: toggle "Cores automáticas por controle" + cor por-controle sem atropelo — **P1, CLAUDE**

- **O que fazer:** checkbox "Cores automáticas por controle" (persistida no perfil via
  draft; **checkbox/switch, nunca dropdown** — popups quebram no cosmic-comp).
  Semântica D4 fechada: alvo "Todos" grava SÓ o global e, se o auto estiver ligado,
  desliga o toggle com aviso visível; alvo "Controle N" grava cor explícita
  POR-CONTROLE (na seção per-controller do perfil — armazenamento coordenado com a
  frente PERFIS); "Voltar ao automático" limpa a explícita do controle selecionado;
  **"Voltar todos ao automático"** limpa todas num clique. Nota na seção de
  player-LEDs: os checkboxes valem com o automático desligado. Swatch da cor efetiva
  por controle (exibir a cor PRÉ-brilho como identidade; ver D8).
- **Arquivos:** `src/hefesto_dualsense4unix/gui/main.glade`,
  `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py`,
  `src/hefesto_dualsense4unix/app/draft_config.py`,
  `src/hefesto_dualsense4unix/daemon/ipc_draft_applier.py`.
- **Critério de aceite (verificável):** escolher cor com alvo "Controle 2" → só o C2
  muda e a cor sobrevive a replug E a restart do daemon (não é atropelada pela
  automática). Aplicar com "Todos" e auto ligado → toggle desliga com aviso e a cor
  única aparece em todos; religar o auto NÃO apaga explícitas. 3º controle plugado
  depois: recebe automática (auto on) ou global (auto off). "Voltar todos ao
  automático" restaura a paleta num clique. Desligar o toggle = comportamento global
  histórico.

### COR-05 — Expor slot + cor efetiva por controle no IPC (interface da frente Status) — **P1, CLAUDE**

- **O que fazer:** `describe_controllers`/`state_full.controllers[i]` ganham
  `player_slot`, `lightbar_rgb` (cor-identidade PRÉ-brilho) e
  `lightbar_rgb_effective` (PÓS-brilho, o que está fisicamente aceso) — contrato
  declarado no doc do IPC (D8). É o que a frente "Status multi-player" consome para
  pintar os inputs de cada player com a cor do lightbar dele sem ficar quase preta em
  perfis de brilho baixo.
- **Arquivos:** `src/hefesto_dualsense4unix/core/backend_pydualsense.py`,
  `src/hefesto_dualsense4unix/daemon/ipc_handlers.py`.
- **Critério de aceite (verificável):** `daemon.state_full` com 2 controles devolve,
  por controle, `uniq` + `player_slot` + os dois campos de cor;
  `lightbar_rgb_effective` bate com o `multi_intensity` do sysfs do MAC
  correspondente (teste ao vivo cruzado); teste de contrato no IPC cobre pré≠pós
  quando brightness < 1.0.

### COR-06 — doctor.sh confere as regras 76/77/78 + corrige comentário stale — **P2, CLAUDE**

- **O que fazer:** incluir `76-dualsense-touchpad-libinput-ignore`,
  `77-dualsense-leds` e `78-dualsense-motion-not-joystick` na lista canônica do
  `check_udev` (total: **7 regras** — 70, 71-uhid, 71-uinput, 72, 76, 77, 78). A 75
  (audio-off) é genuinamente opt-in e fica FORA. **Corrigir o comentário
  DOCTOR-UDEV-CANONICAL-FIX-01 que afirma (falsamente) que a 76 é opt-in** — o
  install a aplica sem flag; comentário errado em script de diagnóstico induz o
  próximo agente a erro. Extra: probe de gravabilidade do `multi_intensity` quando há
  DualSense conectado (é o gate real da cor em BT).
- **Arquivos:** `scripts/doctor.sh`.
- **Critério de aceite (verificável):** com a 77 removida manualmente, doctor acusa
  (warn/fail) e aponta `sudo bash scripts/install_udev.sh`; com tudo instalado, passa
  listando as 7 canônicas; nenhum falso-negativo com a 75 ausente. Sem flag nova em
  install/uninstall (nada muda neles — já são simétricos para 76/77/78).

### COR-07 — Validação humana ao vivo (2 DualSense: 1 BT + 1 cabo) — **P1, VITORIA_HUMANO**

- **O que fazer:** com a onda aplicada, seguir o roteiro no `CHECKLIST_MANUAL.md`:
  1. ligar o daemon com os 2 DualSense → cores distintas + LEDs de número acendem
     sozinhos nos dois transportes (tolerar o pisca breve do kernel no bind — D10);
  2. replugar o Controle 1 → ele VOLTA com a mesma cor/número;
  3. escolher uma cor manual para o controle BT → sobrevive a replug e restart;
  4. salvar o perfil "vitoria", fechar e reabrir a GUI → tudo como deixou;
  5. entrar num jogo em Modo Nativo → o hefesto não pisa nos LEDs do jogo;
  6. **co-op num jogo real: conferir LED aceso vs. número de player que o JOGO
     mostra** — se divergirem (borda de replug do primário, D7), anotar o passo exato:
     é o comportamento documentado, não reprovação, mas precisa estar VISTO por ela.
- **Arquivos:** `CHECKLIST_MANUAL.md`.
- **Critério de aceite:** os 6 passos confirmados pela Vitória na máquina dela (ela é
  quem vê as cores). Qualquer divergência vira bug com o passo exato anotado.
  Invariante da casa: sem este item, NENHUM item desta frente fecha.

### COR-08 — Notas de release: mudança visível + quebra de downgrade + "número do controle" — **P2, CLAUDE**

- **O que fazer:** documentar nas notas da release que (a) perfis existentes com cor
  global salva (ex.: "vitoria", "Navegação" com `16/32/72`) passam a exibir **cores
  automáticas por controle** após o upgrade (`auto_player_colors` default True — é o
  comportamento pedido, mas é mudança visível sem ação dela; reaplicar uma cor
  manualmente volta a valer, por-controle); (b) **downgrade quebra**: `LedsConfig` é
  `extra="forbid"` (`profiles/schema.py:151`) — perfil salvo pela versão nova
  (com `auto_player_colors`/seção per-controller) fica INVÁLIDO em daemon antigo, e há
  12 perfis reais em `~/.config/.../profiles/` nesta máquina que seriam re-salvos;
  (c) o LED fora do co-op mostra o **número do CONTROLE** (slot), que pode divergir do
  número de player que o jogo atribui (D7).
- **Arquivos:** notas de release da próxima tag (CHANGELOG/corpo da release) +
  `CHECKLIST_MANUAL.md` (nota do passo 6).
- **Critério de aceite (verificável):** os 3 pontos presentes no texto da release
  antes de taggear; revisor consegue citar a linha.

## Ordem

COR-01 → COR-02 → COR-03 (o que a Vitória vê acender sozinho) → COR-05 → COR-04 →
COR-06 → COR-08 → COR-07 (validação humana fecha a frente).

## Riscos aceitos (com a mitigação decidida)

1. **Mudança de semântica visível no upgrade** — mitigada por COR-08 (notas) e pelo
   fato de ser o comportamento pedido; reaplicar cor manual volta a valer.
2. **LED (slot) pode divergir do player do jogo em borda de replug do primário** —
   inerente (SDL enumera por ordem); mitigada por D7 (nomenclatura "número do
   controle") + COR-07 passo 6 + COR-08. `player_indexes()` hoje não tem consumidor
   de produção (só testes — grep conferido), mas o contrato "número que o jogo vê"
   (`coop.py:145-165`) fica intacto porque o registro NÃO o substitui (D3).
3. **Modo Nativo** — todo caminho novo respeita `output_mute` (D12); o unmute agora
   re-aplica POR-KEY (COR-02 caminho 3).
4. **Suíte** — testes que assumem "Controle N = posição+1" vão quebrar de propósito
   (GUI/CLI/applet mudam juntos, D6); os 2379 do gate precisam seguir verdes e o gate
   tem **22 skips falsos conhecidos** que já esconderam 1 vermelho — rodar o subset de
   LED/coop/identity com atenção redobrada, não confiar só no verde agregado.
5. **Transiente do kernel no bind** — o `hid_playstation` auto-atribui player-LED; o
   reassert já existe (`_refresh_sysfs_leds` new_keys) e o aceite tolera o pisca (D10).

## Armadilhas conhecidas que esta frente atravessa (não repetir)

- **MAC próprio por vpad** (`02:fe:00:00:00:0N`, report 0x09 LE): MAC repetido =
  probe `-EEXIST` + fallback SILENCIOSO para uinput/`0ce6` = o caminho envenenado da
  launch option (Estudo 1). É a razão do Refutado 2/D3.
- **valid_flag do rumble é máscara `0x03`, nunca só `0x01`** e
  **`_INPUT_PAYLOAD_SIZE=63`** — não tocar no encoder do vpad por acidente ao mexer no
  backend.
- **udev < 73 para uaccess**: quem vira TAG `uaccess` em ACL é a 73-seat-late; regra
  numerada depois aplica MODE sem ACL. Nós em `SUBSYSTEM=misc` exigem
  `udevadm trigger --subsystem-match=misc`. (Esta frente não cria regra nova, mas o
  probe do COR-06 lê nós cobertos pela 77.)
- **GUI sudo-zero em runtime** (bfd51db): nada desta frente pede senha em clique —
  confirmado, é tudo userspace + sysfs já liberado pela 77.
- **Dropdowns quebram no COSMIC** (cosmic-epoch#2497 + NVIDIA): o toggle do COR-04 é
  checkbox/switch; nada de popup novo.
- **GIL/throttling**: a resolução de cor roda no tick de hotplug (~2s,
  `RECONNECT_HOTPLUG_POLL_INTERVAL_SEC=2.0`) e no reconcile do backend — nenhuma
  varredura nova inline no poll loop de input.
- **Autoswitch/`unknown` (XWayland)**: troca de perfil no meio do jogo re-aplica LEDs;
  a precedência por-controle (explícita/auto) tem de sobreviver ao flap de perfil —
  coberto pelo resolvedor único (D5), mas o teste de COR-04 "sobrevive a restart"
  deve incluir uma troca de perfil no meio.
- **`sysfs_leds.discover()` não filtra o vpad** — atribuição de cor parte SEMPRE dos
  handles físicos do backend (filtro `_is_virtual_hidraw`), nunca do discover cru.

## O que já está PROVADO vs. o que é DECISÃO

| Afirmação | Confiança |
|---|---|
| Estado de LED global/broadcast é a causa-raiz (file:line) | PROVADO NO CÓDIGO (3 revisores) |
| Os 2 DualSense ao vivo com mesma cor `16 32 72` e mesmo player-LED | PROVADO AO VIVO |
| Escrita sysfs de LED funciona em USB E BT agora (mesmo com EIO de hidraw no BT) | PROVADO AO VIVO |
| Regra 77 default no install, simétrica no uninstall, ausente no doctor | PROVADO NO CÓDIGO + AO VIVO |
| `notify_controller_connected` não serve de hook por-controle | PROVADO NO CÓDIGO (refutação) |
| Slot no co-op colidiria MAC do vpad (`-EEXIST` → uinput silencioso) | PROVADO NO CÓDIGO (refutação) |
| Paleta PS5 e padrões P1..P4 (já existem em `coop.py:60-74`) | PROVADO NO CÓDIGO |
| Precedência runtime > explícita > auto > global | DECISÃO (D4/D5 — resolver a contradição COR-02×COR-04) |
| Slot de sessão com reserva para replug (sem LRU) | DECISÃO (D2) |
| Pré-brilho no `lightbar_rgb` do IPC + campo effective | DECISÃO (D8) |
| Cores certas acendendo sozinhas na máquina dela | PENDENTE — só COR-07 fecha |

## Referências

- Investigação original + revisão adversarial (3 lentes): sessão de 2026-07-16.
- Estudo 1 (launch option é veneno, EIO de BT, uhid só no boot): memória
  `achado_launch_option_veneno_20260716` + `2026-07-16-sprint-edge-dedup-e-fechamento.md`.
- Fundação uhid do vpad: `2026-07-15-sprint-uhid-dualsense-de-verdade.md` (UHID-03 era
  o embrião desta frente: LEDs por jogador via sysfs do kernel).
- Rota sysfs da lightbar (BT): FEAT-DSX-LIGHTBAR-SYSFS-01 (v3.10.0).
- Frentes irmãs da mesma onda: perfis por controle (compartilha o registro MAC→slot e
  a seção per-controller do perfil), Status multi-player (consome COR-05), dedup por
  udev (mata a launch option — independente desta frente).
