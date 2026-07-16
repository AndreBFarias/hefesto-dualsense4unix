# Sprint SPRINT-UX-AUTOSWITCH-01 — autoswitch com histerese, extinção da launch option e sinal de degradação do vpad

**Este documento é um PLANO. Nada daqui foi implementado.** Frente derivada do Estudo 1
(117 agentes, 2026-07-16) + relato ao vivo da Vitória, refinada por 3 revisões
adversariais (técnica, regressão, escopo). Branch `sprint/harmonia-uhid`.

Pedido da mantenedora que esta frente responde (pedido nº 5, nas palavras dela): *"O botão
'Copiar opções p/ jogos' deveria ser acionado AUTOMATICAMENTE e mostrar um popup na tela
com o comando."* — **a resposta desta frente é um NÃO fundamentado** (ver §Decisão sobre o
pedido 5), porque a opção que o botão copia é o veneno provado do "em BT nada funciona".
Junto, esta frente cura o "a emulação morre no meio do jogo" (medido hoje na sessão dela)
e dá à GUI o sinal de degradação do vpad que hoje não existe.

## TL;DR

1. **O drop no meio do jogo tem causa dupla, provada**: (1) o autoswitch trata "não sei
   qual janela está em foco" como "é o desktop" — `run()` passa qualquer leitura ao
   `select_for_window`, o `MatchAny` do perfil padrão `vitoria` casa com tudo, e perfil
   com `mode=null` reverte o gamepad ligado por perfil; (2) o `_NET_ACTIVE_WINDOW` do
   XWayland fica **rançoso** no COSMIC (aponta até janela morta) enquanto
   `XGetInputFocus` devolve 0. Cura: **histerese** no autoswitch (UX-01) + **gate de
   foco** no XlibBackend (UX-02).
2. **A launch option `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` é veneno
   persistido**: está AGORA no `localconfig.vdf` dela (linha 914, appid 1599660) e,
   quando o vpad cai em uinput/`0ce6` (EIO de BT, hotplug) ou no modo Nativo, ela esconde
   físico **e** vpad → jogo com **zero controles**. O plano: **remover o veneno
   persistido** (UX-04) e **aposentar a recomendação** (UX-05) — mas **gateado por dedup
   PROVADA AO VIVO**, nunca por "regra udev instalada" (a revisão adversarial refutou esse
   gate: o caminho HIDAPI do SDL escapa do udev).
3. **A degradação do vpad é invisível**: `state_full` já expõe
   `gamepad_emulation.backend` e ninguém além do botão de copiar consome — quando o vpad
   cai em uinput ela conclui que "o hefesto não funciona". Cura: banner na GUI (UX-03,
   com texto honesto — "reconecte o controle" foi **refutado** pela revisão).

Prioridades: **P0** = UX-01, UX-02, UX-04. **P1** = UX-03, UX-05. **P2** = UX-06, UX-07.

## Regra de ouro (ditada pela Vitória, vale para todo item)

*"não queremos burocratizar a solução, mas tudo tem que tá no install funcionando SEM
FLAGS"*. Tradução operacional que este plano honra:

- Tudo que a solução precisa entra por **default** no `install.sh` (flag só como
  opt-out). O `uninstall.sh` é **simétrico** (regra histórica: a assimetria já quebrou o
  microfone dela).
- **Nada de "cole isto depois"**: se só funciona quando ela cola algo, não está pronta —
  é exatamente a queixa sobre a launch option.
- GUI/daemon seguem **sudo-zero em runtime** (decisão do commit `bfd51db`): sudo só no
  install, uma vez, com TTY.
- O `doctor.sh` verifica o que o install põe.
- Favorável a esta frente: o guard `hefesto-steam-input-guard.path/.timer` (UX-04) **já é
  default no install, já está ativo na máquina dela e o uninstall já remove as units** —
  a simetria está pronta. O item que NÃO cabe nas restrições nesta onda é a dependência
  nova do UX-07 (`pywayland`): por isso o protótipo roda **fora do repo** e a dependência
  só entra no release em que o backend shippar (ver UX-07).

## Causa-raiz (com nível de prova)

### 1. Autoswitch: leitura sem informação vira "é o desktop" — PROVADO AO VIVO + NO CÓDIGO

- **[PROVADO AO VIVO]** journal 2026-07-16 **13:07:18**: `profile_autoswitch
  from_=sackboy_nativo to=vitoria wm_class=unknown wm_name=` (vazio) +
  `gamepad_emulation_stopped` **no mesmo segundo**. Episódio idêntico às **03:40:29**.
- **[PROVADO NO CÓDIGO]** o mecanismo, linha a linha (conferido pelas 3 revisões):
  - `profiles/autoswitch.py:67-97` — o `run()` passa QUALQUER leitura (inclusive info
    vazio e `wm_class="unknown"`) ao `select_for_window`, sem filtro;
  - `profiles/schema.py:64-65` — `MatchAny.matches` retorna `True` incondicional;
  - `~/.config/hefesto-dualsense4unix/profiles/vitoria.json` — o perfil padrão dela é
    exatamente o gatilho: `match type=any`, `mode=null`, prioridade 5;
  - `daemon/lifecycle.py:1062-1078` — `apply_profile_mode(None)` reverte o gamepad
    ligado por perfil (contrato FEAT-PROFILE-MODE-01, **correto** — o defeito é trocar
    de perfil sem evidência, não o revert).
- **[PROVADO AO VIVO]** o mesmo caminho derruba a emulação quando ela foca a **GUI do
  hefesto** (journal **13:06:03**: `to=vitoria wm_class=Hefesto-Dualsense4Unix` +
  `gamepad_emulation_stopped`) — evidência positiva, por design, mas atrapalha o caso de
  uso "mexer no lightbar durante o jogo" (ver UX-06).

### 2. XlibBackend: `_NET_ACTIVE_WINDOW` rançoso no cosmic-comp — PROVADO AO VIVO (2x, independente)

- **[PROVADO AO VIVO]** reproduzido de forma independente pelas duas revisões, na sessão
  dela (`DISPLAY=:1`): `_NET_ACTIVE_WINDOW=0x1200007` aponta para **janela X morta**
  (`BadWindow` ao consultar `WM_CLASS`) enquanto `get_input_focus().focus == 0` (int).
  O cosmic-comp não limpa a propriedade quando o foco vai para janela Wayland nativa nem
  quando a janela X morre.
- **[PROVADO NO CÓDIGO]** `window_backends/xlib.py:64-111` confia cegamente na
  propriedade — zero uso de `get_input_focus` hoje; nesse estado o backend devolve
  `wm_class='unknown'` (o reader converte `None` em `_UNKNOWN_WINDOW`,
  `window_detect.py:150-166,199-209`).

### 3. A launch option é veneno persistido — PROVADO AO VIVO (Estudo 1 + vdf dela)

- **[PROVADO AO VIVO]** `~/.steam/steam/userdata/1300222895/config/localconfig.vdf:914`
  sob o appid 1599660 (Sackboy): `SDL_JOYSTICK_HIDAPI=0
  SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6 __GL_SHADER_DISK_CACHE=1
  __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%` — variante Xbox de antes do UHID-04.
  `grep -c IGNORE_DEVICES` no vdf = **1** (o veneno existe em exatamente 1 appid, e a
  linha tem **2 dos 3** tokens — não há `PROTON_ENABLE_HIDRAW` nela).
- **[PROVADO AO VIVO — Estudo 1]** o vpad nem sempre sobe Edge `0df2`: em BT o
  `capture_dualsense_blueprint` dá EIO intermitente nos feature reads → fallback
  **silencioso** para uinput/`0ce6`; o hotplug não promove (único call site do
  `upgrade_primary_vpad_to_uhid` é o connect do boot, `lifecycle.py:393`; o
  `reconnect_loop` em `connection.py:208-231` não promove). Nesse estado a opção colada
  esconde físico **e** vpad → zero controles. No modo Nativo (sem vpad), idem.
- **[PROVADO NO CÓDIGO]** o `doctor.sh:387` ainda **recomenda** o veneno ("máscara Xbox
  360 (recomendada): `SDL_JOYSTICK_HIDAPI=0 SDL_GAMECONTROLLER_IGNORE_DEVICES=… %command%`").

### 4. A degradação do vpad é invisível — PROVADO NO CÓDIGO

- `daemon/ipc_handlers.py:421-426` produz `gamepad_emulation.backend` (`uhid`/`uinput`);
  o **único consumidor** é o botão de copiar (`daemon_actions.py:251-254`);
  `home_actions._render_home:358-369` lê só flavor/enabled. Nenhuma tela mostra nada
  quando o vpad cai em uinput.

## Vereditos da revisão adversarial (o que mudou no plano)

A causa-raiz e a solução **sobrevivem** nas 3 lentes, com 3 refutações pontuais que este
plano incorpora — não vendemos o que foi refutado:

| Alvo | Veredito | O que mudou aqui |
|---|---|---|
| Texto "Reconecte o controle" no banner UX-03 | **REFUTADO** | Reconectar NÃO promove o vpad a uhid no código atual (promoção só no boot; re-selecionar máscara é no-op, `gamepad.py:296-298`). Texto vira "reinicie o Hefesto na aba Sistema" — ou o banner entra junto com o fix de promoção-no-hotplug da frente UHID. Item rebaixado a **P1** (banner é sinal, não fix). |
| Gate "mesmo release da dedup" no strip UX-04 | **REFUTADO** | A unit do guard executa o script do **working tree** (`ExecStart` aponta para o repo, timer 30 min) — "release" não gateia nada na máquina dela; qualquer commit no branch armaria o strip. O gate tem de ser em **RUNTIME, dentro do próprio script** (ver UX-04). |
| Gate "regra udev instalada" para aposentar a opção (UX-05) | **REFUTADO** | `ID_INPUT_JOYSTICK=0` só esconde o físico do caminho **evdev** do SDL. O driver **HIDAPI** (default para PS5) enumera `/dev/hidraw*` direto e ignora a propriedade — e os hidraw do físico dela têm ACL da usuária (provado ao vivo: `user:vitoriamaria:rw-` em hidraw2 USB e hidraw4 BT). O próprio `doctor.sh:384-386` documenta o escape. O gate passa a ser **dedup PROVADA AO VIVO cobrindo o caminho HIDAPI** (jogo vê exatamente 1 controle, sem launch option, nas 2 máscaras, USB e BT). |

E as ressalvas estruturais que o plano assume por inteiro:

- **UX-01 sozinha cura os dois episódios medidos** de drop (ambos com `wm_class=unknown`
  E `wm_name` vazio). UX-02 é a outra metade correta do bug (mata a leitura rançosa-viva,
  ex.: Steam em background devolvendo `steam` como falsa evidência positiva), mas o doc
  **não vende UX-02 como requisito** do fix dos episódios observados.
- **A histerese NÃO é "fim do drop no meio do jogo"**: janela X intermediária com classe,
  título ou PID válidos (launcher da Rockstar no RDR2 — jogo real dela —, splash de
  Proton, crash handler Wine) ainda troca perfil por evidência positiva, **por design**.
  A cura estrutural desses casos é perfil para o launcher ou o backend zcosmic (UX-07).
- **Retenção de perfil é o preço do pacote** UX-01+UX-02(+UX-06) — ver §Modo de falha novo.
- **`SDL_JOYSTICK_HIDAPI=0` e `PROTON_ENABLE_HIDRAW=1` NÃO são veneno**: o primeiro é fix
  comum de controles de terceiros (o **8BitDo dela**, hoje "descontrolado", pode vir a
  precisar dele); o segundo é o **enabler** que entrega o hidraw do vpad Edge ao jogo
  Proton (docstring do próprio `compose_launch`, `daemon_actions.py:228`) e pode ser o
  que sustenta o rumble validado ao vivo. O strip nunca os caça soltos (ver UX-04).

## Decisão sobre o pedido 5 (popup automático do "Copiar opções") — precisa do OK da Vitória

**Veredito: NÃO fazer o popup automático.** Contraria o pedido literal, então fica
registrado aqui, explícito, para o aceite dela:

- O que o botão copia é **o veneno provado pelo Estudo 1**: quando o vpad cai em
  uinput/`0ce6` (EIO de BT, hotplug sem promoção) ou no modo Nativo, a opção colada
  esconde físico E vpad → **zero controles**. Automatizar o popup automatizaria a
  distribuição do veneno.
- O espírito do pedido ("não quero ter que colar nada") é atendido **melhor** pela
  **extinção** da launch option (dedup udev da frente DEDUP + UX-04/UX-05 daqui) — zero
  colagem, que é também a regra de ouro.
- Ela mesma apontou a saída: *"se vamos usar um comando pra desabilitar inputs… SE ISSO
  FOSSE POSSÍVEL SEM PRECISAR DE UMA SOLUÇÃO QUE DESLIGUE OS CONTROLES EXTERNOS NEM
  PRECISARÍAMOS."*
- **Plano B, por escrito** (se a extinção se provar impossível — o escape HIDAPI pode
  não ter cura via udev): o pedido não fica sem resposta. Em vez de colar às cegas, a
  GUI passa a **cruzar** (leitura read-only do vdf) a opção persistida com o estado atual
  do vpad e **avisa quando a opção colada virou veneno** (vpad em uinput/Nativo com
  `IGNORE_DEVICES` persistido), oferecendo o texto certo para o estado daquele momento.
  Detector desse estado = o banner UX-03. Nunca escrita automática no vdf fora do guard.

## Itens

### UX-01 — Histerese no autoswitch: leitura sem informação não troca perfil
- **Prioridade**: P0 · **Quem**: CLAUDE
- **Arquivos**: `src/hefesto_dualsense4unix/profiles/autoswitch.py`,
  `tests/unit/test_autoswitch.py`
- **O que fazer**: no `run()` do `AutoSwitcher`, pular o tick **inteiro** (sem mudar
  candidato, sem reiniciar debounce, sem ativar nada) quando a leitura não tem
  informação: info vazio OU (`wm_class in {'', 'unknown'}` **e** `wm_name` vazio **e**
  `exe_basename` vazio). Log `autoswitch_window_info_unavailable` deduplicado por
  episódio (padrão do `_log_suppressed_once`). **NÃO tocar** no revert de
  `lifecycle.py:1062-1078` (contrato FEAT-PROFILE-MODE-01: perfil sem opinião DEVE poder
  reverter o modo — é o único caminho de saída desenhado; o defeito era trocar SEM
  evidência). **Sem TTL**: TTL re-introduziria o drop em glitch mais longo que o limite
  (o EIO de BT já mede 5,1 s; loading screens duram minutos) — só evidência positiva
  troca perfil.
- **Armadilhas de implementação (obrigatórias, das revisões)**:
  1. O debounce é **wall-time** (`_candidate_since`, `autoswitch.py:77-82`): ao retomar
     leituras úteis depois de um episódio de skip, **congelar/resetar** o
     `_candidate_since` — sem isso, duas leituras-glitch idênticas separadas por minutos
     ativam INSTANTANEAMENTE (o tempo pulado conta como estabilidade).
  2. O skip **não pode pular o reset da `suppress_log_key`** (linhas 89-90) — regressão
     do BUG-AUTOSWITCH-LOG-KEY-STUCK-01.
  3. A condição estrita é de propósito: janela X com **título ou PID** preenchidos ainda
     entra no `select` (preserva perfis por `process_name`/`window_title_regex`).
     Tradeoff residual aceito: janela X sem WM_CLASS mas com título, por mais que o
     debounce (0,5 s), ainda ativa o fallback — registrado, coberto por teste.
- **Honestidade de escopo**: cura os episódios "leitura sem informação" (os 2 medidos).
  NÃO cura launcher/splash com evidência positiva (RDR2/Rockstar) — isso é perfil de
  launcher ou UX-07.
- **Critério de aceite (verificável)**:
  1. Sequência Doom estável → N ticks `{'wm_class': 'unknown'}` → mantém
     `_current_profile='shooter'` e `counter('profile.activated')==1`;
  2. com perfil MatchAny salvo, reads `{}` ou unknown NUNCA o ativam;
  3. leitura com `wm_class='unknown'` mas `exe_basename` preenchido AINDA entra no
     select;
  4. teste do buraco do debounce: glitch útil → skip longo → glitch útil idêntico NÃO
     ativa na hora;
  5. caso fresh-install: desktop Wayland puro sem `last_profile` salvo — perfil MatchAny
     não ativa sozinho via unknown; comportamento **intencional e testado** (para a
     Vitória o `restore_last_profile` cobre o boot: `connection.py:80-92` +
     `manager.py:127-128`, provado no código);
  6. **suíte completa SEM filtro** (o gate "2410 verde" tem 22 skips falsos que já
     esconderam 1 vermelho) e journal sem flood (1 log por episódio).

### UX-02 — Gate de foco X no XlibBackend (mata a leitura rançosa)
- **Prioridade**: P0 · **Quem**: CLAUDE
- **Arquivos**: `src/hefesto_dualsense4unix/integrations/window_backends/xlib.py`,
  `tests/unit/test_window_backends.py`
- **O que fazer**: em `get_active_window_info`, consultar `display.get_input_focus()`
  ANTES de confiar no `_NET_ACTIVE_WINDOW`; foco em {0 (None), 1 (PointerRoot)} →
  retornar `None` (vira `unknown` e a histerese UX-01 segura).
- **Armadilhas de implementação (obrigatórias)**:
  1. python-xlib devolve `focus` como **int (0/1) OU objeto Window** — normalizar com
     `getattr(focus, 'id', focus)` antes de comparar; teste cobrindo **os dois tipos**
     (comparar direto com `{0, 1}` quebra no caminho feliz).
  2. **Tradeoff declarado** (corrigindo o texto de risco da frente original, que
     afirmava o contrário): tratar PointerRoot (1) como sem-foco **cega permanentemente
     sessões X11 legadas focus-follows-mouse**. Aceito porque o alvo é COSMIC; fica
     coberto por teste para o comportamento ser intencional.
- **Honestidade de escopo**: os 2 drops medidos são curados pela UX-01 sozinha; o
  diferencial do gate é matar a leitura rançosa-**viva** (ex.: com terminal COSMIC em
  foco e Steam viva em background, hoje o backend devolve `steam` — falsa evidência
  positiva que pode trocar perfil errado). O estado rançoso foi reproduzido ao vivo 2x.
- **Critério de aceite (verificável)**: teste com display fake:
  `get_input_focus().focus=0` (e também como objeto Window de id 0) +
  `_NET_ACTIVE_WINDOW`=janela viva de jogo → `get_active_window_info()` retorna `None`;
  focus=janela válida → comportamento atual intocado. **Validação ao vivo** (VITÓRIA +
  CLAUDE): com o jogo em foco o autoswitch ativa o perfil do jogo; com terminal COSMIC
  em foco e Steam em background, a leitura vira unknown (hoje devolve `steam`).

### UX-03 — Sinal de degradação do vpad na GUI (backend uinput visível)
- **Prioridade**: **P1** (rebaixado pela revisão: banner é sinal, não fix — o P0
  verdadeiro é a promoção-no-hotplug, que é da frente UHID) · **Quem**: AMBOS
- **Arquivos**: `src/hefesto_dualsense4unix/app/actions/home_actions.py`,
  `src/hefesto_dualsense4unix/app/actions/status_actions.py`, `tests/unit/`
- **O que fazer**: consumir `gamepad_emulation.backend` do `state_full` nas abas Início
  e Status: banner de aviso quando `mode=='gamepad' && flavor=='dualsense' &&
  backend=='uinput'`. Lógica numa **função pura testável** (padrão `_flavor_label`).
- **Texto do banner — REFUTADO o original**: "Reconecte o controle" é conselho ineficaz
  no código atual (`upgrade_primary_vpad_to_uhid` só roda no boot, `lifecycle.py:393`
  único call site; o `reconnect_loop` não promove; re-selecionar a máscara é no-op,
  `gamepad.py:296-298`). Texto honesto: **"O gamepad virtual subiu no modo simples: a
  vibração e a separação do controle físico não estão garantidas. Reinicie o Hefesto na
  aba Sistema."** Se a frente UHID entregar a promoção-no-reconnect, o texto pode virar
  "reconecte" — dependência explícita, nunca antes.
- **Armadilhas de implementação (obrigatórias)**:
  1. Tratar backend **ausente/`''`** como estado distinto SEM alarme falso — é
     transitório real (`enabled=True` com `_gamepad_device=None`; o
     `ipc_handlers.py:421-426` só emite a chave com device vivo).
  2. O banner fala **só pelo vpad primário** (`daemon._gamepad_device`); os vpads dos
     players 2-4 do co-op podem divergir e o aviso não os cobre — aceito no escopo, dito
     na cara do doc.
  3. **Coordenação de arquivo**: `status_actions.py` é o MESMO arquivo da frente que
     atende o pedido 1 dela (cores por player na aba Status) — sequenciar para não
     colidir.
- **Critério de aceite (verificável)**: teste unitário da função pura:
  `(dualsense, uinput, gamepad)` → texto de degradação; `(dualsense, uhid, gamepad)` →
  `None`; `(xbox, uinput, gamepad)` → `None`; `(dualsense, uinput, desktop)` → `None`;
  `(dualsense, '', gamepad)` e chave ausente → `None` (sem falso alarme). **Validação
  visual da Vitória** (invariante do projeto: teste verde sem validação ao vivo NÃO
  fecha item): provocar o vpad uinput (ligar o controle depois do daemon) e VER o aviso
  na aba Início.

### UX-04 — Remover o veneno persistido do localconfig.vdf (guard existente + uninstall)
- **Prioridade**: P0 · **Quem**: AMBOS
- **Arquivos**: `scripts/disable_steam_input.sh`,
  `assets/hefesto-steam-input-guard.service`, `install.sh`, `uninstall.sh`,
  `scripts/doctor.sh`
- **Infra que já existe (provado ao vivo)**: `hefesto-steam-input-guard.path/.timer` é
  **default no install** (`install.sh:~1027-1041`), está **ativo agora na máquina dela**,
  o `--apply-quiet` **adia com exit 0 se a Steam vive**, edita com **backup**
  (`.bak.steam-input-<ts>`) e tem gate de idempotência (`needs_fix` — sem ele, o `.path`
  que vigia o userdata entraria em **loop de auto-disparo** a cada edição do próprio
  guard; manter essa disciplina é obrigatório). O `uninstall.sh:190-193` já remove as
  units — simetria pronta, **zero flags** (regra de ouro atendida).
- **O que fazer — dois caminhos com gates DIFERENTES**:
  1. **Uninstall (INCONDICIONAL, sem gate nenhum)**: o `uninstall.sh` passa a strippar
     `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` das LaunchOptions. Razão:
     desinstalado o hefesto não existe vpad nenhum — a opção persistida esconde o físico
     → **jogo com zero controles pós-uninstall**. A revisão refutou o gate de dedup para
     este caminho.
  2. **Guard em runtime (gate em RUNTIME dentro do script — o gate "mesmo release" foi
     REFUTADO)**: a unit executa o script do **working tree** (`ExecStart` →
     `~/Desenvolvimento/.../disable_steam_input.sh`, timer a cada 30 min) — qualquer
     commit no branch armaria o strip antes de qualquer release. O strip só roda quando,
     **em runtime**, o script confirmar: (a) probe da propriedade **efetiva** no device
     físico (via `udevadm info`/pyudev — sudo-zero OK; presença do arquivo de regra NÃO
     é prova) **e** (b) o marcador de **validação ao vivo** que a frente DEDUP só grava
     depois do roteiro end-to-end passar (jogo SDL real, HIDAPI ligado, exatamente 1
     controle — ver UX-05). Sem os dois, o strip devolve o controle duplicado e destrói
     a ÚNICA configuração que funciona hoje (USB + máscara Xbox depende da linha 914).
- **Escopo do strip (ressalva obrigatória das 3 revisões)**: remover **SÓ** a assinatura
  hefesto-específica `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`; tokens adjacentes
  (`SDL_JOYSTICK_HIDAPI=0`, `PROTON_ENABLE_HIDRAW=1`) apenas em linhas que **contenham a
  assinatura** — NUNCA caçá-los soltos em outros appids (o primeiro é fix comum de
  controles de terceiros — o 8BitDo dela; o segundo é o enabler do hidraw do vpad Edge em
  Proton). Preservar `__GL_SHADER_*` e o resto da linha **byte a byte**. E antes de
  qualquer strip de `PROTON_ENABLE_HIDRAW=1` mesmo co-ocorrente: **validar ao vivo** que
  o rumble da máscara DualSense-Edge sobrevive sem ele num jogo Proton.
- **Doctor**: check novo que **acusa** `IGNORE_DEVICES` em qualquer LaunchOptions.
- **Risco de edição**: LaunchOptions é conteúdo arbitrário de usuário (aspas, escapes,
  `%command%` no meio) — diferente do edit numérico do PSSupport que o script faz hoje.
  Exige testes de fixture com linhas reais, **incluindo a linha 914 dela verbatim**
  (que tem 2 dos 3 tokens — o critério de aceite reflete o conteúdo real), e o
  rollback-do-backup que o script já tem (linhas 178-186).
- **Critério de aceite (verificável)**: com Steam fechada, o guard roda e a linha 914 do
  vdf dela (appid 1599660) perde `IGNORE_DEVICES` + `SDL_JOYSTICK_HIDAPI=0`
  (co-ocorrentes) mantendo shader-cache + `%command%` byte a byte; backup criado ao
  lado; doctor acusa antes e passa depois; rodar 2x é **idempotente** (needs_fix);
  com Steam aberta o script **adia sem tocar no arquivo** (exit 0); com o gate de
  runtime insatisfeito o strip NÃO roda (teste); o caminho do uninstall strippa
  **incondicionalmente**. Validação ao vivo da Vitória: pós-strip, jogo por cabo
  continua com controles (nada de regressão do cenário que funciona).

### UX-05 — Aposentar a recomendação do veneno (botão + doctor) — gate por validação ao vivo
- **Prioridade**: P1 · **Quem**: CLAUDE (código) + VITORIA_HUMANO (a validação que abre o gate)
- **Arquivos**: `src/hefesto_dualsense4unix/app/actions/daemon_actions.py`,
  `scripts/doctor.sh`, `tests/unit/`
- **O que fazer**: `compose_launch` ganha o estado da dedup — e o critério é **dedup
  PROVADA AO VIVO cobrindo o caminho HIDAPI** (o gate "regra instalada ou flag no
  state_full" foi **REFUTADO**: o HIDAPI enumera `/dev/hidraw*` direto, ignora
  `ID_INPUT_JOYSTICK`, e os hidraw do físico têm ACL da usuária — esconder o hidraw do
  jogo sem esconder do daemon é impossível via udev para processos do mesmo usuário).
  Roteiro que abre o gate (com a frente DEDUP): jogo SDL real, HIDAPI ligado, **sem
  nenhuma launch option**, vê **exatamente 1 controle** — nas 2 máscaras, USB **e** BT.
  Só então: nenhuma variante emite `IGNORE_DEVICES`/`SDL_JOYSTICK_HIDAPI`;
  `doctor.sh:387` para de recomendar o veneno; o botão muda o rótulo para acessório
  ("Copiar aceleração de carregamento").
- **Ressalva sobre "resta só o preload de shaders"**: isso assume que
  `PROTON_ENABLE_HIDRAW=1` também morre — depende do allowlist de hidraw do Proton para
  o Edge `0df2` e **precisa de teste ao vivo**; se ele continuar necessário, o rótulo
  novo não pode mentir "extinção total" (o botão continua emitindo o enabler, sem o
  IGNORE).
- **Enquanto o gate não abre (`dedup_validada=False`)**: comportamento atual preservado,
  mas **sem** o rótulo "fallback honesto" seco — o toast/doc avisa o **descompasso
  persistência-vs-estado**: a opção colada PERSISTE na Steam, e a variante certa depende
  do estado do vpad NAQUELE momento (Estudo 1: vpad caindo para uinput/`0ce6` faz o
  IGNORE persistido esconder físico E vpad). Declarado: **o banner UX-03 é o detector
  desse estado**.
- **Critério de aceite (verificável)**: teste unitário: `compose_launch` com
  `dedup_validada=True` não contém `IGNORE_DEVICES` nem `SDL_JOYSTICK_HIDAPI` em nenhum
  (flavor, backend); com `dedup_validada=False`, comportamento atual + aviso de
  persistência presente no texto. `grep -n 'IGNORE_DEVICES' scripts/doctor.sh` não
  retorna recomendação ativa (o check de ACUSAÇÃO do UX-04 pode citar o token). O gate
  em si: roteiro ao vivo documentado com resultado, assinado pela validação da Vitória.

### UX-06 — GUI do hefesto como janela neutra no autoswitch (decisão da Vitória)
- **Prioridade**: P2 · **Quem**: AMBOS (**exige OK explícito dela** — muda comportamento
  desenhado)
- **Arquivos**: `src/hefesto_dualsense4unix/profiles/autoswitch.py`,
  `tests/unit/test_autoswitch.py`
- **O que fazer**: tratar `wm_class=='Hefesto-Dualsense4Unix'` como tick sem informação
  (mesmo caminho da UX-01), para ela abrir a GUI no meio do jogo (mexer no lightbar —
  caso de uso da frente perfis-por-controle) sem derrubar a emulação — hoje derruba
  (**[PROVADO AO VIVO]** journal 13:06:03). Fixar tanto o wm_class X quanto um futuro
  `app_id` Wayland da GUI.
- **Custo composto (obrigatório no pedido de OK)**: a GUI é **forçada a XWayland** no
  COSMIC (`main.py:161`) — logo é a única janela X que ela pode SEMPRE invocar, e hoje é
  a **rampa de saída garantida** da retenção de perfil (focar a GUI ativa `vitoria` e
  reverte o modo-jogo). Neutralizá-la antes do UX-07 deixa o cenário "joguei, saí, só
  tenho janelas Wayland-nativas e a Steam minimizada" **sem nenhuma saída automática** —
  só gesto manual na aba Perfis. **Não shipar UX-06 antes de existir saída garantida**:
  ordenar depois do UX-07, ou shipar junto com uma saída manual explícita e documentada.
- **Critério de aceite (verificável)**: jogo em foco → GUI em foco → jogo: perfil do
  jogo permanece ativo e `counter('profile.activated')` não cresce; validação ao vivo
  dela: abrir a GUI durante o Sackboy e a vibração continuar; o texto do OK dela
  registrado neste doc (com o efeito colateral por escrito: focar a GUI nunca mais troca
  perfil).

### UX-07 — Backend COSMIC nativo via `zcosmic_toplevel_info_v1` (investigação, fora do repo)
- **Prioridade**: P2 · **Quem**: CLAUDE
- **Arquivos NESTE sprint**: nenhum do repo — protótipo no scratchpad com venv
  descartável. (`window_backends/`, `pyproject.toml` e `install.sh` só no release em que
  o backend shippar.)
- **Base provada**: **[PROVADO AO VIVO, 2x independente]** o cosmic-comp da sessão dela
  expõe `zcosmic_toplevel_info_v1` v3 (estado `activated` + `app_id`),
  `ext_foreign_toplevel_list_v1` v1 e `zcosmic_toplevel_manager_v1` v4. É a cura
  **definitiva** da cegueira Wayland (leitura POSITIVA de qualquer janela, nativa ou
  XWayland) — e da retenção de perfil introduzida pela histerese.
- **Ressalvas obrigatórias**:
  1. **Escopo enxuto (lente de escopo da revisão)**: a regra "tudo replicável via
     script" vale para feature **shippada**, não para experimento — a dependência nova
     (`pywayland` ou similar) **NÃO entra** no pyproject/install.sh neste sprint;
     entra por default (regra de ouro, sem flags, uninstall simétrico) no release do
     backend, se o go/no-go der go.
  2. cosmic-comp **NÃO expõe** `zwlr_foreign_toplevel` — o backend wlrctl existente não
     serve; é protocolo novo.
  3. `window_detect.py:125-127` escolhe `XlibBackend` SEMPRE que `DISPLAY` está setado
     (e o daemon tem DISPLAY) — o backend novo exige mudar a **ordem de seleção**, não
     só existir.
  4. Prefixo `z` = protocolo **instável**: bump de versão do cosmic-comp pode quebrar —
     degradação graciosa obrigatória (cair para o XlibBackend + histerese).
- **Critério de aceite (verificável)**: protótipo (fora do repo) lendo `app_id` +
  `activated` da janela em foco na sessão COSMIC dela, **incluindo janela Wayland nativa
  (hoje invisível)**; decisão go/no-go documentada NESTE doc com medição de
  custo/latência.

## Modo de falha novo (documentado, não escondido): retenção de perfil

Com UX-01+UX-02, um fluxo **100% Wayland-nativo** ao sair do jogo não gera evidência
positiva → o perfil de jogo fica **retido** (suppress/grab ativos) até focar uma janela X
com evidência ou gesto manual. Compromissos:

- **Rampas de saída nomeadas**: (1) a Steam é XWayland e, na prática, retoma o foco
  pós-jogo → reverte sozinha — **validar ao vivo** que isso acontece no fluxo real dela
  (é a mitigação de hoje); (2) focar a GUI do hefesto (XWayland) — deixa de existir se
  UX-06 shippar, por isso o gate de ordenação de lá; (3) gesto manual na aba Perfis.
- A cura estrutural é o UX-07 (leitura positiva de janela Wayland).
- O boot NÃO depende do autoswitch: `restore_last_profile`
  (FEAT-PERSIST-SESSION-01, `connection.py:80-92`) + `save_last_profile` a cada ativação
  (`manager.py:127-128`) — **[PROVADO NO CÓDIGO]** a histerese não quebra o restore do
  perfil `vitoria` ao abrir o programa.

## Armadilhas conhecidas que esta frente atravessa

- **MAC próprio por vpad** (`02:fe:00:00:00:0N` no report 0x09, little-endian) — MAC
  duplicado = probe -17.
- **valid_flag do rumble é máscara `0x03`**, nunca só `0x01` (firmware >= 0x0215 usa
  vibração v2 com HAPTICS_SELECT sozinho no flag0).
- **`_INPUT_PAYLOAD_SIZE=63`** — com 62 o driver descarta calado e o vpad nasce mudo.
- **Regra udev de uaccess precisa de número < 73** (a 73-seat-late converte a tag em
  ACL); nós em `SUBSYSTEM=misc` exigem `udevadm trigger --subsystem-match=misc`.
- **Sudo-zero na GUI em runtime** (bfd51db) — o probe do UX-04/UX-05 lê via
  `udevadm info`/pyudev, nunca escreve com sudo por clique.
- **Dropdowns quebram no COSMIC** (cosmic-epoch#2497) — qualquer UI nova do banner
  UX-03 usa rótulo/banner ou botões segmentados, nunca combo/popover.
- **GIL/throttling**: o gate de foco (UX-02) roda no tick de 0,5 s do autoswitch — nada
  de chamada bloqueante nova no loop de input (lição do HARM-17).
- **Gate "2410 verde" tem 22 skips FALSOS** — rodar a suíte inteira sem filtro em todo
  item; **`test_quit_app` já matou o daemon dela** — cuidado ao rodar testes na máquina.
- **Nunca `git checkout <arquivo>`** (já destruiu trabalho não-commitado).
- **validar-acentuacao**: manter as linhas tocadas com acentuação correta.

## Ordem

UX-01 → UX-02 (fecham o drop medido; validação ao vivo em seguida) → UX-03 (depois de
sequenciar com a frente do pedido 1 em `status_actions.py`) → UX-04 caminho-uninstall
(incondicional, pode já) → **espera o gate da frente DEDUP** → UX-04 caminho-guard +
UX-05 (só com dedup provada ao vivo no caminho HIDAPI) → UX-07 (protótipo) → UX-06
(só depois do UX-07 ou com saída manual garantida + OK da Vitória).

## Referências

- Estudo 1 (117 agentes, 2026-07-16): EIO intermitente de BT no blueprint, fallback
  silencioso uhid→uinput, hotplug sem promoção, launch option persistida.
- `2026-07-16-sprint-edge-dedup-e-fechamento.md` (UHID-04, compose_launch atual, §BT).
- `2026-07-15-sprint-uhid-dualsense-de-verdade.md` (armadilhas do uhid, PoC).
- Journal da sessão dela: 03:40:29, 13:06:03, 13:07:18 (drops medidos).
- `~/.steam/steam/userdata/1300222895/config/localconfig.vdf:914` (o veneno persistido).
- Frente DEDUP (irmã desta onda): regra udev dinâmica + validação end-to-end que abre o
  gate de UX-04(guard)/UX-05.
