# AUTO-03 — configurar um jogo em um clique

- **Status:** ABERTA
- **Prioridade:** ALTA — é a única sprint da leva que responde ao pedido de 25/07
  ao pé da letra, e a medição achou dois pontos em que o fluxo não é apenas
  lento: ele **descarta em silêncio** o que a pessoa acabou de configurar (ver
  AUTO-03.1 e AUTO-03.2). Fricção se aguenta; perder o ajuste sem aviso é o
  defeito histórico desta casa ("a config que eu deixo nunca é respeitada").
- **Aberta em:** 25/07/2026, por medição no código

## O pedido

> "preciso de verdade que veja as features do projeto (…) à procura de facilidade
> do usuário: ao clicar em tal coisa, ele não precisar alterar 10 coisas em abas,
> fechar a Steam, abrir, aplicar x, y e z, tudo de forma manual mas de forma
> automática, o máximo que der."

AUTO-01 (`docs/process/sprints/2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md`,
ENTREGUE no commit `8fe735d`) pegou o que **impedia os quatro jogadores** e mandou
o resto para AUTO-02 (Steam), AUTO-03 (fluxo de jogo) e AUTO-04 (o que só existe
no terminal). O índice da leva
(`2026-07-25-INDICE-leva-quatro-controles.md:76`) posiciona esta sprint como
*"configurar um jogo em um clique"*.

### Nota de honestidade: os "29 pontos de fricção" nunca foram escritos

`grep -rn "29 pontos" docs/` devolve **uma linha só** — o resumo da queixa 6 no
índice (`2026-07-25-INDICE-leva-quatro-controles.md:24`) — e o número reaparece
por extenso em `2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md:14`. Não existe
documento que liste os vinte e nove. Sobreviveu o número, não o mapeamento.

Esta sprint portanto **não herda uma lista**: ela remede a fricção do fluxo de
jogo direto no código, do zero. Onde o achado coincidir com AUTO-01, está dito.

Segunda honestidade, sobre a dependência: quando esta medição começou, **AUTO-02
não existia como documento** — `ls docs/process/sprints/ | grep AUTO-0` devolvia
só o AUTO-01. Ela foi escrita em paralelo, na mesma leva
(`2026-07-25-AUTO-02-uma-janela-de-steam-nao-tres.md`, ABERTA), e **eu não a li
antes de medir** — nada aqui foi derivado dela. O índice
(`2026-07-25-INDICE-leva-quatro-controles.md:76`) põe AUTO-03 dependente de
AUTO-02, e essa dependência vale para a metade "lado Steam" do desenho abaixo:
ela só aterrissa depois que AUTO-02 decidir quem é o dono da janela de Steam
fechada. O que **não** depende de AUTO-02 está marcado como tal ao final.

## A pergunta que esta sprint responde

**Quantos gestos, em quantas abas, uma pessoa precisa hoje para fazer um jogo
específico funcionar com os controles dela — e quantos deveriam ser.**

## O caminho de hoje, medido

A janela tem **nove abas** (`src/hefesto_dualsense4unix/gui/main.glade`, rótulos
reais nos `child type="tab"`):

| aba | linha no glade | esta aba entra no fluxo de UM jogo? |
|---|---|---|
| Início | `main.glade:241` | **sim** — modo, máscara e "Preparar co-op" |
| Status | `main.glade:419` | não (leitura) |
| Gatilhos | `main.glade:698` | **sim** — 19 presets, dois gatilhos |
| Lightbar | `main.glade:1096` | **sim** — cor do jogo |
| Rumble | `main.glade:1338` | **sim** — política de vibração |
| Perfis | `main.glade:1720` | **sim** — é onde o jogo vira uma regra |
| Sistema | `main.glade:1966` | **sim** — todo o lado Steam |
| Emulação | `main.glade:2345` | **sim** — terceiro caminho do Steam Input |
| Navegação DSX | `main.glade:2688` | não |

**Sete das nove abas participam de configurar um jogo.** E o caminho não termina
na janela: ele termina dentro da Steam.

### Os gestos, na ordem

Contadas as **superfícies e os controles que precisam ser tocados** — lidos no
código, não cronometrados numa sessão real (não abri a janela; ver "O que não foi
medido").

**Aba Início** (`main.glade:241`)

1. "Preparar co-op (N jogadores)" (`main.glade:216`, handler em
   `app/actions/home_actions.py:983`). Um clique, e ele encadeia modo de jogo,
   co-op e renumeração — isto é o que AUTO-01 entregou, e funciona.

**Aba Perfis** (`main.glade:1720`) — aqui o jogo vira uma regra

2. "Novo perfil" (`app/actions/profiles_actions.py:693`).
3. Digitar o nome (`profile_name_entry`).
4. Seletor "Aplica a:" → **"Jogo da Steam"** (`profiles_actions.py:96`; a opção
   nasceu no R-12 porque era a única forma de dizer *"este perfil é DESTE jogo"* —
   `profiles/simple_match.py:5-11`).
5. Conferir o AppID no campo livre (`profiles_actions.py:65`, dica em `:78-83`).
6. Conferir o modo (`_MODE_KIND_ITEMS`, `profiles_actions.py:103`).
7. Escolher a máscara (`_MODE_FLAVOR_ITEMS`, `profiles_actions.py:114`).
8. **Arrastar a prioridade** (`main.glade:1511`, escala 0–100). Não é opcional —
   ver AUTO-03.1.
9. "Salvar".

**Aba Perfis de novo** — ativar

10. "Ativar" (`profiles_actions.py:768`). Sem este passo, nada do que vier a
    seguir entra no arquivo do jogo — ver AUTO-03.2.

**Abas Gatilhos, Lightbar e Rumble** (`main.glade:698`, `:1096`, `:1338`)

11. Gatilho esquerdo: modo, preset, sliders, "Aplicar"
    (`app/actions/triggers_actions.py:207`); idem o direito (`:210`). São **19
    presets** por lado (`app/actions/trigger_specs.py:1` e `:61`).
12. Cor da lightbar; política de vibração.

**Aba Perfis pela terceira vez**

13. "Salvar" **de novo** — senão o JSON do jogo fica com os gatilhos em `Off`
    (`profiles/schema.py:215-218`) e a lightbar em `(0,0,0)`
    (`profiles/schema.py:225`).

**Aba Sistema** (`main.glade:1966`) — o lado Steam

14. "Deixar tudo pronto" (`main.glade:1866`, handler em
    `app/actions/daemon_actions.py:846`) + confirmar o diálogo que fecha e
    reabre a Steam (`daemon_actions.py:850`).

**Fora da janela** — se ela quiser o wrapper só **neste** jogo

15. Steam → biblioteca → jogo → botão direito → Propriedades → Opções de
    inicialização → colar → fechar. Seis gestos, e é literalmente o que o
    próprio Hefesto manda fazer
    (`app/actions/launch_wrapper_dialog.py:241-247`).

**Três abas obrigatórias, mais duas se ela quiser gatilho/cor, o perfil salvo
DUAS vezes, e uma visita à Steam.** É a queixa dela, item por item.

## O achado que resume a queixa

**O único lugar do Hefesto que sabe qual é o jogo é exatamente o único que não
pode fazer nada a respeito.**

Quando um jogo da Steam está em foco e ainda não abre pelo wrapper, a janela
levanta um diálogo sozinha (`app/actions/launch_wrapper_dialog.py:96`, avaliado
no tick de 2 Hz que a GUI já tem, `:289`). Nesse instante ela sabe **tudo**:

- o AppID, extraído da janela em foco (`launch_wrapper_dialog.py:81`, lendo
  `window_detect_last_class` do `state_full` — publicado em
  `daemon/ipc_handlers.py:1311`);
- que **este** jogo não chama o wrapper, lido do `localconfig.vdf` por AppID
  (`integrations/steam_launch_options.py:543`);
- que a emulação está de pé (`launch_wrapper_dialog.py:138`).

E o que o diálogo oferece? **"Copiar opções"** e **"Não perguntar para este
jogo"** (`launch_wrapper_dialog.py:378-379`). O texto manda a pessoa ir à Steam
colar a linha na mão (`:241-247`).

Isso **não é descuido** — é decisão consciente, e está escrita:

> "**Sem botão 'Aplicar…'** — de propósito: o gatilho deste diálogo é exatamente
> 'jogo aberto', e o fluxo assistido da Fase 2 RECUSA nesse estado duas vezes"
> (`launch_wrapper_dialog.py:20-25`)

A recusa é certa: com jogo aberto, `steam -shutdown` mataria o jogo
(`steam_launch_options.py:490-494`), e com a Steam aberta ela regrava o vdf ao
sair (`:495-497`). O erro não está na recusa — está em o Hefesto **descartar o
que descobriu**. Ele aprende o AppID no único momento em que não pode agir, e
esquece antes do momento em que poderia.

## Os defeitos medidos

### AUTO-03.1 — o perfil do jogo nasce em prioridade 0 e perde para os presets de fábrica

`on_profile_new` zera a prioridade: `profiles_actions.py:703` faz
`profile_priority_scale.set_value(0)`.

A seleção do autoswitch ordena por `(não-é-catch-all, prioridade)`
(`profiles/manager.py:624`). O desempate por catch-all salva o perfil novo do
`fallback` (prioridade 0, `assets/profiles_default/fallback.json:5`) e do
`meu_perfil` (1) — mas **não o salva dos presets de gênero**, que são regras
específicas como ele:

```
sackboy_nativo 80   coop_local 75   Aventura 70   Ação 65
FPS 60   point_and_click 60   Esportes 55   Corrida 55   Navegação 50   bow 10
```

E esses presets casam **pelo título da janela**, não pela `wm_class`. O perfil de
Elden Ring que ela acabou de criar (prioridade 0, casando
`window_class=["steam_app_1245620"]`) disputa com `aventura.json` (prioridade 70,
`window_title_regex` contendo `Elden Ring` —
`assets/profiles_default/aventura.json`) e **perde**.

O caminho que a interface oferece como "faça o perfil deste jogo" produz, sem
avisar, um perfil que o autoswitch descarta.

Note o contraste: o `coop_local` subiu de 45 para 75 justamente por perder para o
`Navegação` (AUTO-01.3, migração em `profiles/loader.py:433-434`). O perfil que a
**usuária** cria continua nascendo em 0.

### AUTO-03.2 — o que ela acabou de ajustar em Gatilhos/Lightbar/Rumble não entra no perfil novo

As abas Gatilhos, Lightbar e Rumble gravam **exclusivamente no rascunho**
(`self.draft`), e o rascunho só é mesclado no perfil que está sendo salvo quando
esse perfil é **o que o rascunho representa** — isto é, o perfil ATIVO
(`profiles_actions.py:1337`, decidido por `_edita_o_perfil_do_rascunho`,
`:1175`).

E essa função tem um portão explícito:

```
:1204   if getattr(self, "_new_profile", False):
:1205       return False
```

`_new_profile` ainda é `True` durante a montagem: `on_profile_save` chama
`_build_profile_from_editor` em `:805`, e só zera a flag em `:912`.

**Consequência medida:** ajustar os gatilhos, ir à aba Perfis, criar o perfil do
jogo e salvar produz um JSON com `triggers.left = Off` e `triggers.right = Off`
(`profiles/schema.py:215-218`) e `lightbar = (0,0,0)`
(`profiles/schema.py:225`). O ajuste continua vivo no hardware — o rascunho não
some — mas **não está no arquivo do jogo**, e volta a valer o `Off` na próxima
vez que o perfil entrar.

O portão está **certo pelo motivo dele**: o rascunho pertence ao perfil ativo, e
mesclá-lo num perfil novo clonaria a configuração de outro perfil (é a lição R-09,
documentada em `:1313-1317`). O defeito não é o portão — é **não haver nada no
lugar dele**. A pessoa não é avisada, e o único caminho que funciona (salvar,
ativar, reajustar, salvar de novo) não está escrito em lugar nenhum da tela.

*Caso degenerado, para não afirmar demais:* se ela der ao perfil novo exatamente o
nome do perfil ativo, o portão de `:1202` responde antes e o rascunho **entra** —
mas aí ela está sobrescrevendo o perfil ativo, não criando o do jogo.

### AUTO-03.3 — não existe "aplicar o wrapper a ESTE jogo"

Há exatamente **uma** função que escreve o wrapper no `localconfig.vdf`, e ela é
tudo-ou-nada: `apply_wrapper_to_all_games`
(`integrations/steam_launch_options.py:466`) varre todos os vdf elegíveis e
aplica a todos os jogos.

Por AppID existe apenas **leitura**: `appid_needs_wrapper`
(`steam_launch_options.py:543`) e `read_launch_options_by_appid` (`:310`). O
módulo já sabe ler e escrever por AppID no vdf; o que falta é a via de escrita
seletiva.

Confirmado também o pendente de **AUTO-01.4**: a função continua sem modo de
linha de comando — o `main()` do módulo só expõe `--status`, `--migrate` e
`--strip` (`steam_launch_options.py:974-986`) — e os únicos chamadores são três
pontos da GUI (`app/actions/daemon_actions.py:717`, `:800`, `:888`). O commit
`8fe735d` não tocou este arquivo.

### AUTO-03.4 — o perfil do jogo e a Steam do mesmo jogo não se conhecem

Procurei um caminho que ligue "criei o perfil deste jogo" a "preparei a Steam
para este jogo". **Não existe**, e o que existe é quase — e por isso vale medir
com precisão:

Ao salvar um perfil, a GUI avisa o daemon com `launch_env.refresh`
(`profiles_actions.py:951`, helper em `:965`), e o comentário explica por quê:

> "perfil novo/editado pode ter `steam_app_<id>` no match — o daemon rematerializa
> a antecipação por appid do launch_env AGORA" (`profiles_actions.py:948-950`)

Isso escreve o `steam_app_<appid>.env` (`daemon/launch_env.py:909` e `:934`) — o
arquivo que **o wrapper lê na hora do launch**. Ou seja: salvar o perfil do jogo
prepara a metade do Hefesto.

A outra metade — fazer a Steam **chamar** o wrapper para esse jogo — não é
tocada por nada nesse caminho. O `.env` fica pronto para um wrapper que aquele
jogo talvez nunca invoque.

E isso é silencioso nos dois sentidos: nada no salvamento consulta
`appid_needs_wrapper(appid)` (`steam_launch_options.py:543`), que responderia
"este jogo não chama o wrapper" numa leitura barata e read-only. A informação
está a uma chamada de distância e não é feita.

### AUTO-03.5 — cinco botões para o lado Steam, e nenhum é "este jogo"

Medido no cartão "Saúde do sistema" da aba Sistema (`main.glade:1824`):

| botão | linha | o que faz de fato | escopo |
|---|---|---|---|
| "Deixar tudo pronto" | `main.glade:1866` | `disable_steam_input.sh --apply-quiet` **e** `apply_wrapper_to_all_games`, os dois dentro de UMA janela de Steam fechada (`daemon_actions.py:868-908`) | **todos** os jogos |
| "Este jogo não funciona" | `main.glade:1878` | grava o AppID na allowlist do Steam Input (`daemon_actions.py:970`, escrita em `steam_launch_options.py:765`) e pede `launch_env.refresh` (`daemon_actions.py:1020`) | **este** jogo |
| "Copiar opções p/ jogos" | `main.glade:1911` | copia a linha constante do wrapper para o clipboard | nenhum — é clipboard |
| "Aplicar aos jogos da Steam" | `main.glade:1918` | `apply_wrapper_to_all_games` | **todos** os jogos |
| "Travar Proton validado" | `main.glade:1925` | aponta o `CompatToolMapping` do `config.vdf` para o Proton validado (`daemon_actions.py:1043`) | global |

**Um único botão é por-jogo — e é o botão de desistir.** "Este jogo não funciona"
é o gesto que tira o Hefesto da frente. Não há o gesto simétrico: *"este jogo eu
quero pelo Hefesto, prepare-o"*.

Vale registrar o que esse botão faz de **certo**, porque o desenho abaixo copia
dele: ele descobre o AppID sozinho por **três evidências em ordem de força**
(`daemon_actions.py:929-968`) — sessão do wrapper viva, `window_detect_last_class`
do `state_full`, e o marcador `last_run` do último jogo lançado. A terceira existe
porque *"o jogo não funcionou, ela fechou, e só então veio reclamar"*
(`daemon_actions.py:942-944`). Essa é exatamente a leitura de intenção que falta
no lado positivo.

### AUTO-03.6 — o Steam Input tem três portas para o mesmo interruptor

Além de "Deixar tudo pronto" e "Aplicar correções" (`main.glade:1904`) na aba
Sistema, a aba **Emulação** tem "Verificar" e "Desligar Steam Input"
(`main.glade:2278` e `:2285`). Três superfícies, o mesmo
`scripts/disable_steam_input.sh`, três textos diferentes. Isto pertence a AUTO-02
(unificar a janela de Steam), e fica registrado aqui porque aparece no caminho de
um jogo.

## O que JÁ funciona — e o checklist não sabia

O checklist de validação
(`2026-07-25-CHECKLIST-validacao-em-hardware.md:70`) lista como **A VALIDAR**:

> - [ ] Criar perfil pelo fluxo "Jogo da Steam" → nasce com modo de jogo já
>       escolhido

**Medido no código: nasce, sim.** `_prefill_modo_de_jogo`
(`profiles_actions.py:547`) é chamado em `:542-543` quando a escolha é "Jogo" ou
"Jogo da Steam" **e** o perfil é novo. Ele grava `kind="gamepad"` (`:585-589`).
É a entrega MODO-01/B1, e o docstring diz por que existiu:

> "o fluxo simples montava o critério de janela certinho e deixava o modo em
> `none` (…). Ela criava o perfil do jogo, ele entrava, e não ligava nada. O
> caminho que a interface oferece como solução não solucionava."
> (`profiles_actions.py:548-553`)

As três guardas medidas, todas estreitas de propósito (`:555-567`): só em perfil
novo (`:569-570`); só se o modo ainda estiver em `none` (`:574-576`); e a máscara
pré-selecionada é **a que o daemon já tem de pé**, lida em segundo plano
(`:591-618`), porque propor outra faria o perfil recriar o vpad ao entrar e
invalidar os handles de um jogo já aberto.

**E o AppID também é preenchido sozinho** — o tooltip não mente
(`profiles_actions.py:78-83`). `_prefill_steam_appid` (`:620`) é disparado em
`:544-545`, pede `daemon.state_full` (`:663-669`) e extrai o AppID de
`window_detect_last_class` (`:649`).

Mas o "sozinho" tem **quatro condições**, e nenhuma aparece na tela:

1. o daemon precisa estar de pé — `timeout_s=0.5`, falha é silêncio (`:666-668`);
2. o campo precisa estar **vazio** — sobrescrever o que ela digitou seria pior
   que não ajudar (`:629-630`, `:636-638`, `:653-654`);
3. o daemon precisa ter visto a janela do jogo: `window_detect_last_class` é o
   sticky da última `wm_class` **útil** (`daemon/state_store.py:290`,
   `:391`) — com o jogo nunca aberto nesta sessão do daemon, não há o que
   preencher;
4. ela precisa continuar em "Jogo da Steam" quando a resposta chegar (`:655-656`).

Fora dessas quatro, o campo fica em branco **sem dizer por quê** — e a pessoa
cai no caso que o R-12 já nomeou: digitar o AppID errado produz um perfil que
nunca entra, "exatamente a queixa *o perfil do jogo nunca é respeitado*"
(`profiles_actions.py:623-625`).

**Correção a fazer no checklist:** o item 3 da seção "O modo jogo liga sozinho"
tem resposta no código. O que resta validar em hardware é outra coisa — se as
quatro condições do AppID se cumprem numa sessão real.

## Entregas

### 1. Um gesto: **"Preparar este jogo"**

Um botão só, e ele aparece onde a pessoa já está olhando: no diálogo do wrapper
(`launch_wrapper_dialog.py:378`) e no cartão da aba Sistema, ao lado de "Este
jogo não funciona" (`main.glade:1878`) — o gesto simétrico do que já existe.

**De onde ele tira o AppID:** exatamente das três evidências de
`_appid_do_jogo_ativo` (`daemon_actions.py:929-968`), na mesma ordem. Nada novo a
inventar. Quando as três falharem, ele **diz que não sabe qual é o jogo** e
oferece o campo — nunca adivinha.

**O que ele faz, na ordem:**

1. **Cria (ou atualiza) o perfil deste jogo** com
   `MatchCriteria(window_class=["steam_app_<id>"])`, exatamente o que
   `from_simple_choice` já produz (`profiles/simple_match.py:104-110`),
   `kind="gamepad"` pelo caminho já existente (`profiles_actions.py:585-589`), e
   **prioridade acima dos presets de gênero** — ver entrega 2.
2. **Aplica o wrapper a este AppID** — a escrita seletiva da entrega 3.
3. **Chama `launch_env.refresh`**, como o salvamento de perfil já faz
   (`profiles_actions.py:951`), fechando a metade que hoje fica pronta sozinha.
4. **Relata cada perna pelo que ela de fato fez**, no padrão de
   `format_steam_ready_result` (`daemon_actions.py:199`) — que já separa
   "Controle:" de "Jogos:" e nunca diz "Pronto" sobre um passo adiado.

### 2. O perfil do jogo nasce podendo ganhar

Prioridade inicial de um perfil criado pelo fluxo "Jogo da Steam" **acima dos
presets de gênero de fábrica** — 85 põe acima de `sackboy_nativo` (80), que é o
único preset por `wm_class` e portanto o único concorrente do mesmo tipo.

Justificativa: um perfil que casa `steam_app_<id>` é a regra mais específica que
existe para aquele jogo. Se ela criou o perfil DESTE jogo, ele não pode perder
para uma regex de gênero que casou o título por acaso.

`profiles_actions.py:703` continua zerando a prioridade de um perfil novo
genérico — **isto é correto** e não muda. O que muda é o fluxo "Jogo da Steam",
que passa a semear a prioridade junto com o modo, no mesmo
`_prefill_modo_de_jogo` (`:547`) e sob as mesmas guardas: só em perfil novo, só
se ela não tiver mexido no slider.

### 3. Escrita do wrapper **por AppID**

Uma função irmã de `apply_wrapper_to_all_games`
(`steam_launch_options.py:466`) que aceita um AppID. Toda a maquinaria já existe:
a leitura por AppID (`:310`), a checagem read-only (`:543`), o backup
`.bak.hefesto-launch-<ts>` (`:525-528`), a escrita atômica (`:529-532`), o pulo
de vdf sandbox (`:499-503`) e os dois gates de recusa (`:490-497`).

Herda **sem relaxar** as regras do módulo: recusa com jogo aberto, recusa com a
Steam aberta, Flatpak/Snap pulado.

Ganha **modo de linha de comando** no `main()` do módulo
(`steam_launch_options.py:965`), que hoje só tem `--status`/`--migrate`/`--strip`
(`:974-986`) — fechando de passagem o pendente AUTO-01.4.

### 4. O rascunho para de sumir num perfil novo — com aviso, não com mágica

Duas metades, e a ordem importa:

- **Avisar antes**: salvar um perfil **novo** com o rascunho sujo (gatilho,
  lightbar ou rumble ajustados nesta sessão) mostra uma frase honesta — *"o
  gatilho e a cor que você ajustou pertencem ao perfil ativo; quer copiá-los para
  este perfil novo?"* — em vez de gravar `Off` calado
  (`profiles_actions.py:1204-1205`).
- **Oferecer o copiar**, e só isso. **Não** remover o portão: ele existe porque o
  rascunho é do perfil ativo, e mesclá-lo cegamente clonaria a configuração de
  outro perfil — a lição R-09 (`profiles_actions.py:1313-1317`). A escolha é
  dela; o que não pode continuar é a decisão ser tomada em silêncio.

### 5. O que o Hefesto descobre com o jogo aberto, ele guarda

Quando o diálogo do wrapper dispara (`launch_wrapper_dialog.py:96`), ele sabe o
AppID e sabe que aquele jogo não usa o wrapper. Hoje isso morre no cache de
sessão (`:269`).

Passa a ficar registrado, junto do marcador `last_run` que o wrapper já mantém
(`daemon/launch_env.py:161`), como **"jogo pendente de preparo"** — para que
"Preparar este jogo" funcione depois, com a Steam fechada, sem exigir que ela
lembre qual era o jogo. É o mesmo raciocínio da terceira evidência de
`_appid_do_jogo_ativo` (`daemon_actions.py:942-944`), aplicado ao lado positivo.

### 6. Uma frase que diz por que o campo do AppID está vazio

Quando `_prefill_steam_appid` (`profiles_actions.py:620`) não preenche, a razão é
uma das quatro condições medidas acima — e todas as quatro são frases curtas
("o daemon não está de pé", "ainda não vi este jogo abrir"). Hoje o silêncio é
indistinguível de "não sei ajudar".

## O que o gesto NÃO deve fazer sozinho

O projeto tem regra dura contra decidir pela pessoa em coisa que ela pode não
querer. Explicitamente **fora** do clique:

1. **Não fecha a Steam sem perguntar.** O consentimento continua sendo diálogo
   próprio, com o mesmo texto honesto que "Deixar tudo pronto" já usa
   (`daemon_actions.py:850`, `:836-844`): *"pause os downloads"*, *"se algum jogo
   estiver aberto eu não faço NADA"*.
2. **Não age com jogo aberto.** Os dois gates de `apply_wrapper_to_all_games`
   (`steam_launch_options.py:490-497`) valem inteiros para a via por-AppID. Com
   jogo aberto o gesto **registra a pendência** (entrega 5) e diz isso.
3. **Não troca a máscara.** Ver o preço, abaixo.
4. **Não escreve opção de lançamento estática.** O wrapper é uma string
   **constante** que decide as envs na hora consultando o daemon
   (`steam_launch_options.py:1-6`), e degrada para `exec env "$@"` se o wrapper
   sumir do caminho (`:66-72`). O caminho antigo — `IGNORE_DEVICES` cravado por
   jogo — **esconde o único controle quando o vpad degrada**, deixando o jogo com
   ZERO controles, e está provado ao vivo (`steam_launch_options.py:12-18`).
   Nada neste desenho volta atrás nisso.
5. **Não trava o Proton.** É decisão global e cara de reverter
   (`daemon_actions.py:1071-1081`); não pertence a um gesto por-jogo.
6. **Não marca o jogo na allowlist do Steam Input.** É a estratégia oposta — tira
   o Hefesto da frente (`daemon_actions.py:970-976`). O botão que faz isso já
   existe e continua sendo dela.
7. **Não sobrescreve nada que ela tenha digitado.** A regra de
   `_prefill_steam_appid` (`profiles_actions.py:629-630`) vale para o gesto
   inteiro: campo preenchido, slider movido, modo escolhido à mão — tudo dela.

## O preço da máscara, se o desenho a tocar

Ele **não deve** tocar, e este parágrafo existe para dizer por quê.

Hoje há dois literais diferentes para o valor padrão: o daemon nasce em
`dualsense` (`daemon/lifecycle.py:140`) e o normalizador de máscara em `xbox`
(`integrations/uinput_gamepad.py:136`). Isso **já foi endereçado** por AUTO-01.5:
a janela deixou de impor a máscara e o dono passou a ser o daemon — sem escolha
explícita, o plano sai sem o campo (`app/actions/mode_transition.py:71-93`).

O preço, se alguém for tentado a semear `dualsense` no perfil do jogo: **a
máscara `dualsense` faz alguns jogos ignorarem o gamepad virtual**
(SPRINT-GAME-RUMBLE-01), e é por isso que o default de preset segue `xbox` — o
piso de compatibilidade validado em qualquer backend
(`uinput_gamepad.py:130-136`). O próprio tooltip da janela avisa: *"jogos que só
entendem controle de Xbox ignoram esta máscara"* (`main.glade:2186`).

Por isso o gesto **preserva a máscara corrente do daemon**, como
`_prefill_modo_de_jogo` já faz (`profiles_actions.py:561-564`). Quem quiser
prompts de PlayStation escolhe, e paga sabendo. Escolher máscara por controle é
assunto de MÁSCARA-01, não deste clique.

## Como validar

Nenhum passo abaixo foi executado — são o roteiro, não um relato.

1. **O caminho curto existe.** Com um jogo da Steam aberto e o Hefesto em modo de
   jogo, o diálogo do wrapper aparece e agora traz **"Preparar este jogo"** além
   de "Copiar opções" e "Não perguntar".
2. **Com o jogo aberto, ele não mente.** Clicar diz que ficou **pendente** e por
   quê (fechar a Steam mataria o jogo) — nunca "Pronto".
3. **Fechar o jogo e a Steam, clicar de novo na aba Sistema.** Sem redigitar
   nada: o Hefesto lembra qual era o jogo (entrega 5).
4. **Um clique, e o resultado é conferível em três lugares:**
   - existe `<slug>.json` com `match.window_class = ["steam_app_<id>"]`,
     `mode.kind = "gamepad"` e prioridade **acima de 80**;
   - as Opções de inicialização **daquele jogo** contêm o prefixo do wrapper —
     e as dos outros jogos **não mudaram**;
   - existe `steam_app_<id>.env` (`daemon/launch_env.py:909`).
5. **Backup no lugar.** Um `.bak.hefesto-launch-<ts>` ao lado do
   `localconfig.vdf` tocado (`steam_launch_options.py:525-528`).
6. **Abrir o jogo.** O perfil do jogo entra — e **não** o preset de gênero que
   casaria pelo título. É o teste direto de AUTO-03.1: fazer isso com um jogo que
   `aventura.json` (70) ou `fps.json` (60) casam pela regex.
7. **O rascunho avisa.** Ajustar um gatilho, criar um perfil novo, salvar: aparece
   a pergunta da entrega 4 em vez de o JSON nascer com `Off`.
8. **O AppID vazio explica.** Com o daemon parado, escolher "Jogo da Steam" mostra
   a razão do campo em branco, não o silêncio.
9. **Contagem final.** Do jogo aberto até o jogo funcionando: **um clique e uma
   confirmação.** Zero abas visitadas, zero visitas à Steam, zero terminal.

## Critério que resume

**Se o Hefesto sabe qual é o jogo, ele tem de saber preparar aquele jogo — e o
número de abas que a pessoa visita para isso é zero.**

## O que não foi medido

- **Não abri a janela e não rodei o instalador.** Tudo acima é leitura de código.
  As afirmações sobre a *aparência* das abas vêm do `main.glade`; as de
  comportamento, dos handlers citados. Nenhum número de gesto foi cronometrado
  numa sessão real — foram **contadas as superfícies e os controles** que o
  código exige tocar.
- **Não medi as quatro condições do preenchimento do AppID em execução** — só as
  li em `profiles_actions.py:620-669`. Com que frequência o
  `window_detect_last_class` está "grudado" no jogo certo no instante do clique é
  pergunta de hardware.
- **Não medi o custo de `apply_wrapper_to_all_games` numa biblioteca grande.** É
  relevante para a entrega 3: se a via por-AppID for barata, ela pode virar o
  caminho preferido também do botão em massa.
- **Não investiguei a aba Navegação DSX** (`main.glade:2688`) — nada no fluxo de
  um jogo apontou para ela.
- **Não li AUTO-02** (`2026-07-25-AUTO-02-uma-janela-de-steam-nao-tres.md`), que
  foi escrita em paralelo a esta medição. A metade "uma janela de Steam fechada,
  com um dono só" deste desenho depende dela, e as duas sprints precisam ser
  lidas juntas antes da implementação — pode haver sobreposição no cartão da aba
  Sistema que nenhuma das duas enxergou sozinha. As entregas 2, 4 e 6 **não**
  dependem: são todas do lado do perfil e podem ir antes.
