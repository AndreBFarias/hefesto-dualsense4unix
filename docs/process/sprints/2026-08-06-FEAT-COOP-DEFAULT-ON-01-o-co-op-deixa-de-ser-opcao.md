# FEAT-COOP-DEFAULT-ON-01 — o co-op deixa de ser opção

- **Achado em:** 06/08/2026, por **auditoria dos códigos sem documento** — uma
  varredura de `git log -S` sobre identificadores que só existiam em comentário
  de código. Não é queixa nova: a **decisão** que estes códigos executam é dela,
  e foi pedida mais de uma vez
- **Estado:** **CURA APLICADA** — e esta sprint é **materialização atrasada**:
  o código e os testes já existiam (o último passo é o commit `ae32c10`,
  06/08/2026), **o documento é que faltava**. Nada aqui pede entrega nova
- **Gravidade:** **BAIXA** no código (nada está quebrado) e **ALTA na memória**:
  três códigos, a decisão de produto que ela mais repetiu, e nenhuma página que
  diga por quê. Vocabulário sem página é vocabulário que alguém renomeia
- **Causa-raiz:** não há defeito de mecanismo a explicar — é **decisão de
  produto**. A causa-raiz da **ausência do documento** é **MEDIDA**: os três
  códigos entraram por commits de leva grande, e `grep -rn` sobre `docs/` só
  acha `UX-MODE-TERMS-01` (uma linha, na RADAR-01) — nenhum dos três tem página
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [PEDIDOS-DELA-01](2026-08-03-PEDIDOS-DELA-01-o-roteiro-dos-seis-pedidos-da-interface.md)
    — o **pedido 1** é o roteiro das sete entregas do `COOP-SEM-INTERRUPTOR-01`,
    e já tem o bloco *"CUMPRIDO em 06/08/2026"*. Esta sprint **não repete** a
    tabela de lá: cobre os três códigos que ficaram sem página nenhuma;
  - [COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md)
    — é **mecanismo** (o P2 que nasce e morre); esta é **política** (o co-op
    deixa de ser opção). Tirar o interruptor não cura o P2;
  - [LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)
    — proposta, não commitada: "um jogador por controle" ainda não alcança
    controle de outra marca;
  - [RADAR-01](2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md)
    — onde o `UX-MODE-TERMS-01` foi medido nas quatro superfícies, e de onde
    veio o portão que hoje segura o vocabulário novo;
  - [AUTO-01](2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md) — de lá veio o
    botão "Preparar co-op", que morreu nesta decisão;
  - [NUNCA-TROCA-O-ALVO-01](2026-08-06-NUNCA-TROCA-O-ALVO-01-a-janela-trocava-o-nome-e-o-salvar-ia-para-o-arquivo-errado.md)
    — mesmo commit `ae32c10`, outra queixa, nada em comum além do dia.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## Os três códigos, e quando cada um nasceu

**Grau: MEDIDO** — `git log -S "<CÓDIGO>"` sobre o repositório, datas do
próprio commit.

| código | nasceu em | commit | o que ele é |
|---|---|---|---|
| `FEAT-DSX-COOP-LOCAL-01` | 27/06/2026 | `e565334` | o **mecanismo**: cada controle físico vira um jogador com gamepad virtual próprio |
| `FEAT-COOP-DEFAULT-ON-01` | 13/07/2026 | `646cadf` | o **padrão**: com 2+ controles em modo jogo, o co-op já vem ligado; o que se persiste é o opt-out |
| `UX-MODE-TERMS-02` | 06/08/2026 | `ae32c10` | a **segunda rodada do vocabulário leigo**: "Jogar direto (Sony)" vira "Conexão Nativa (Sony)" |

A correção importa, porque muda a leitura: **o co-op não é entrega de 06/08**.
Ele tem quarenta dias de estrada, e o que 06/08 fez foi arrancar o último
interruptor. Quem for reabrir a decisão precisa saber que ela foi tomada em
**três degraus**, e não num impulso.

---

## O mecanismo — `FEAT-DSX-COOP-LOCAL-01`

**Grau: MEDIDO** (`tests/unit/test_subsystem_coop.py`, com dublês de
`EvdevReader`/`UinputGamepad` — sem hardware).

O multi-controle base é *"N controles, 1 player"*: o output vai em broadcast e o
input vem só do primário. Serve para reserva e troca de controle; **não serve
para duas pessoas** — as duas movem o mesmo personagem.

O `subsystems/coop.py` acrescenta, **sem tocar no caminho do P1**, uma camada de
jogadores secundários: para cada controle físico além do primário, um leitor
evdev dedicado (com grab) e um gamepad virtual próprio. O poll loop, depois de
despachar o P1, chama `forward_all()` e repassa cada secundário ao **seu** vpad
(`daemon/lifecycle.py`, tick do co-op reconciliado a cada ~2 s). O jogo passa a
enxergar N aparelhos distintos.

Duas invariantes do mecanismo que sobreviveram intactas à decisão de produto, e
por isso não podem ser confundidas com ela:

- **o vpad nunca nasce sem grab confirmado** (`BUG-COOP-GRAB-PENDING-VPAD-01`):
  jogador com grab `pending` fica registrado **sem** vpad e é promovido no tick
  quando o grab confirma. Antes, uma recusa tardia deixava até ~2 s de input
  dobrado dentro do jogo;
- **a suspensão por Steam Input não é desligar o co-op**: ela chama
  `CoopManager.disable()` direto, **sem tocar a flag** — e é exatamente por isso
  que o co-op volta sozinho quando o jogo fecha.

---

## A escada da decisão — três degraus, quarenta dias

| degrau | quando | o que mudou | onde mora |
|---|---|---|---|
| 1 | 27/06 | o co-op existe, e nasce **desligado** (`default OFF — preserva o modo "1 player"`) | `subsystems/coop.py` |
| 2 | 13/07 | o co-op vira **padrão** com 2+ controles; o que se grava em disco é o **opt-out** (`coop_disabled.flag`) | `utils/session.py` |
| 3 | 06/08 | o opt-out **deixa de existir**: `DaemonConfig.coop_enabled = True` é o piso único, e nenhuma superfície de comando desliga | `daemon/lifecycle.py:160` |

A palavra dela, literal, que está citada em **sete** arquivos do repositório
(`cli/cmd_coop.py`, `daemon/ipc_handlers.py`, `daemon/lifecycle.py`,
`utils/session.py`, `gui/main.glade` — onde entra abreviada — e os testes
`test_coop_sem_interruptor_01_*` e `test_coop_optout_migracao.py`):

> *"Independente do que escolhermos, todos e tudo no Hefesto tem que tá com o
> permitir co-op ligado. Eu já havia pedido pra removermos até o botão da aba
> Início e tirar essa seção de lá também, já que isso não faz sentido — afinal,
> se eu conecto 4 controles no PC eu espero, com 4 pessoas jogando, que cada um
> controle o próprio personagem. Ninguém esperaria controlar o mesmo personagem
> com cada controle."*

**Isto não é proposta técnica, e não se reabre com argumento de engenharia.** O
caso de uso que a flag protegia — o controle de reserva — não precisava de flag
nenhuma: quem quer reserva **deixa o controle desconectado**.

---

## O que o `FEAT-COOP-DEFAULT-ON-01` ensinou, e vale para todo eixo

O código de 13/07 deixou três regras que hoje são doutrina da casa, e nenhuma
delas caducou com a decisão de 06/08.

### 1. Grava-se a DECISÃO, nunca a ausência

O opt-out (`coop_disabled.flag`) existe porque *"não está ligado"* e *"ela
desligou de propósito"* são estados **diferentes**, e a automação precisa
distingui-los. O desenho virou molde citado nominalmente em dois outros eixos:

- o mouse (`HARM-06`): a chave `enabled` passou a ser gravada nos dois sentidos,
  em vez de o "off" ser o arquivo apagado;
- o gamepad virtual (`AUTO-01.1`): `gamepad_disabled.flag`, com o comentário
  dizendo *"mesmo desenho do `coop_disabled.flag` (FEAT-COOP-DEFAULT-ON-01)"*
  (`utils/session.py:452`).

### 2. Só gesto MANUAL persiste

`lifecycle.py:1382` — *"só gesto MANUAL persiste a escolha: perfil
ligando/desligando co-op não pode virar opt-out da usuária"*. A frase foi citada
como precedente quando o gamepad virtual foi consertado (`R-07`), e o efeito
medido lá é a melhor prova de por que a regra existe: ela escolhia Xbox, abria
um jogo cujo perfil pede DualSense, e **a escolha dela sumia do disco** sem ela
ter tocado em nada (`tests/unit/test_gamepad_persist_so_manual.py`).

### 3. Sair do modo jogo não apaga a preferência

`app/actions/mode_transition.py:99-101` — o plano do modo **desktop** desliga o
nativo e o gamepad e **não** desliga o co-op: desligar o gamepad já desmonta os
jogadores, e preservar a preferência faz o co-op voltar sozinho ao reentrar em
"Jogar pelo Hefesto".

**Mordida:** `tests/unit/test_home_actions_handlers.py`,
`test_modo_desktop_desliga_nativo_e_gamepad_preservando_coop` — o plano tem
exatamente três chamadas, e um `coop.set {enabled:false}` a mais reprova.

---

## A forma sobrevive, a opção morre

Este é o desenho que mais custa a entender lendo o código de hoje, e é o que
mais precisa estar escrito: **nada foi apagado**. Cada peça do interruptor
continua de pé, e cada uma explica por que continua.

| peça | o que ela faz hoje | por que não foi removida |
|---|---|---|
| `coop.set {enabled:false}` | responde `status: "recusado"`, com `enabled: true`, `players` preservado e `motivo` legível (`ipc_handlers.py:3271`) | quem lê o contrato não quebra, e quem esperava o desligamento **não é enganado por um `"ok"`** |
| `Daemon.set_coop_enabled(False)` | ramo inalcançável pelas superfícies de comando | o setter é o **mecanismo**; a política mora no handler, com a razão legível |
| `save_coop_enabled()` | **lápide**: só apaga o que versão antiga deixou, não grava mais opt-out nenhum | a assinatura é contrato público — um chamador antigo pedindo "desliga" não pode virar `TypeError` no boot |
| `load_coop_enabled()` | **lápide**: devolve `True` sempre | CLI, applet e testes a importam; uma lápide legível vale mais que um `ImportError` para quem for reabrir a decisão |
| `ProfileModeConfig.coop` | **aceito e ignorado** (`schema.py:439`), com log quando um perfil antigo pede `false` | `model_config` é `extra="forbid"`: tirar o campo faria **todo perfil dela que traz `"coop"` falhar na validação**, inclusive dois presets de fábrica (`coop_local.json` e `sackboy_nativo.json`) |
| `hefesto-dualsense4unix coop off` | **explica** e sai com código 2 (`cmd_coop.py:72`) | sumir com o subcomando devolveria um "No such command" que não ensina nada a quem o tem num script |

E duas remoções que **são** entrega, não faxina:

- **o boot deixou de reler o opt-out** (`lifecycle.py:662-670`). Enquanto o
  `run()` forçava `True` logo adiante, arrancar o `True` do dataclass **não
  reprovava teste nenhum** — a cura tinha um **sósia**. Hoje o piso tem um dono
  só, e arrancá-lo reprova (`tests/unit/test_coop_optout_migracao.py`, sobre o
  dataclass cru);
- **o perfil deixou de governar** (`lifecycle.py:2108-2122`). Um perfil antigo
  com `"coop": false` desligava o co-op dela ao ativar, pelas costas de quem
  nunca pediu isso. Hoje o campo é lido e o pedido vira uma linha de log
  (`perfil_pediu_coop_off_ignorado`).

### O pré-requisito que veio ANTES, de propósito

O botão "Preparar co-op" da `AUTO-01.2` disparava, **de carona no `coop.set`**,
o único ciclo forçado de reconciliação (`CoopManager.sync(force=True)`) que ela
alcançava por gesto. Tirar o botão sem mais nada tiraria dela o único jeito de
recuperar o jogador que nasce e morre em dois segundos.

Então o ciclo forçado ganhou **dono próprio** — o IPC `coop.sync` e o botão
"Reconciliar jogadores" da aba Início — **antes** da remoção. A lápide que
registra isso está em `app/actions/mode_transition.py:167-179`, no lugar exato
onde moravam `plan_coop_prep` e `apply_coop_prep`.

Junto veio uma correção que não estava no roteiro e é medida: o botão
"Reconciliar jogadores" **deixou de ser desabilitado com jogo aberto**. O gate
antigo estava certo enquanto o gesto só renumerava (o daemon recusa renumerar em
partida); deixou de estar quando o botão herdou a reconciliação, porque **o P2
cai DURANTE a partida** — o gate escondia o gesto na hora exata do defeito.

### A migração de quem já tinha desligado

Duas migrações one-shot, cada uma com marker próprio e idempotente:

- `session.migrate_coop_optout()` apaga o `coop_disabled.flag` de quem desmarcou
  o checkbox numa versão **já lançada** — sem isso o co-op subiria desligado
  **sem nenhum caminho de volta na interface**;
- `loader.migrate_profiles_coop_default()` **apaga a chave** `"coop": false` dos
  perfis gravados pela GUI antiga (cujo default de esquema era `False`, então
  **todo** perfil salvo carregava o desligamento). Apaga em vez de gravar `true`
  de propósito: o perfil passa a **herdar** o padrão, e um default futuro volta a
  valer sem uma segunda migração.

---

## `UX-MODE-TERMS-02` — o vocabulário que ela FIXOU

Segunda rodada do vocabulário leigo, e também **pedido antes e não cumprido**.
A palavra dela, literal, está no comentário de `home_actions.py:123`:

> *"Jogar direto é péssimo também. Já tinha pedido pra deixarmos: Conexão Nativa
> (Sony)"*

**Estes são os nomes, e eles são escolha dela. Não se repropõem.**

| id (não muda) | rótulo na tela |
|---|---|
| `none` (só na aba Perfis) | **Não mexer no modo** |
| `desktop` | **Controlar o PC** |
| `gamepad` | **Jogar pelo Hefesto** |
| `native` | **Conexão Nativa (Sony)** |

Máscara do gamepad virtual, no mesmo léxico: **DualSense (botões PlayStation)** e
**Xbox 360** — sem "(vibra)"/"(sem vibrar)", que virou mentira quando o vpad uhid
passou a vibrar nas duas.

### Por que o nome antigo caducou

Não foi gosto. Os outros dois rótulos dizem **para onde o controle fala** ("o
PC", "o Hefesto"); "Jogar direto" dizia o **gesto** e não a **coisa**, e
"direto" não completava a frase. "Conexão Nativa (Sony)" nomeia o que de fato
acontece: **o Hefesto solta a conexão** e o jogo fala com o DualSense físico,
sem intermediário.

### Só o rótulo mudou

O id `native` continua sendo chave de perfil salvo em disco, método de IPC e
comando de CLI (`native on`). **Renomear o id quebraria perfil gravado**, e a
nota está escrita nos três lugares que repetem os rótulos.

**Mordidas:**

- `tests/unit/test_profiles_vocabulario_leigo.py::test_os_quatro_rotulos_leem_como_uma_lista_so`
  — os quatro itens do editor, nesta ordem, como uma lista só; quem ressuscitar
  "Jogar direto" em qualquer um deles reprova;
- `tests/unit/test_profiles_vocabulario_leigo.py::test_ids_do_schema_intactos` —
  a outra metade: os ids **não** podem acompanhar o rótulo;
- `tests/unit/test_vocabulario_das_quatro_superficies.py` (RADAR-01/E4) — lê o
  fonte **Rust** do applet como texto e casa `home_actions._MODE_ITEMS` contra o
  `let entries` de `packaging/cosmic-applet/src/app.rs:659`. É o portão que
  impede a renomeação de entrar numa superfície só. A aba Perfis entra no mesmo
  teste, pelo item de ausência de modo mais os três.

A superfície-dona é a `_MODE_ITEMS` da aba Início. As outras duas
(`profiles_actions._MODE_KIND_ITEMS` e o applet) **repetem**, e repetir é poder
divergir — por isso o portão.

---

## Nota datada — o que caducou, e onde a nota ficou

Não se apaga decisão medida. Cada uma destas ganhou nota datada no arquivo onde
morava, e nenhuma foi removida em silêncio:

| decisão que caducou | onde a nota ficou |
|---|---|
| `coop_enabled` default `False`, *"preserva o uso de reserva/troca de controle"* | `daemon/lifecycle.py:146-159` |
| o opt-out em disco (`coop_disabled.flag`) | `utils/session.py`, no docstring de `save_coop_enabled` |
| `load_coop_enabled()` lendo o disco | `utils/session.py`, no docstring da própria função |
| `ProfileModeConfig.coop` governando o modo | `profiles/schema.py:430-438` |
| o botão "Preparar co-op" e suas três frases | lápides em `mode_transition.py:167` e `home_actions.py:487` |
| `UX-MODE-TERMS-01`, que batizou o modo de "Jogar direto (Sony)" | `home_actions.py:120-135` e `docs/usage/modos.md` |
| metade das premissas de `test_coop_optout_migracao.py` | no docstring do próprio arquivo de teste |

---

## O que fica ABERTO

- **O `subsystems/coop.py` ainda diz que o co-op nasce desligado.** A linha 29,
  no bloco de pré-requisitos do `should_be_active`, lê *"`config.coop_enabled`
  ligado (default OFF — preserva o modo "1 player")"* — o exato motivo que a
  nota de `lifecycle.py:146-159` declarou **caduco**, e o exato default que o
  `lifecycle.py:160` inverteu. **Grau da divergência: MEDIDO** (as duas linhas
  estão no repositório de hoje e se contradizem). **Grau do efeito: SEM PROVA** —
  ninguém mediu alguém sendo enganado por ela. É o arquivo mais provável de ser
  lido por quem for mexer no co-op.
- **O applet ainda diz "Jogando direto (Sony)" na linha de estado.** O
  `UX-MODE-TERMS-02` alcançou o **seletor** do applet
  (`app.rs:659`, coberto pelo portão das quatro superfícies), mas **não** a linha
  "Modo" do bloco de status: `app.rs:590` e `:592` seguem com *"Jogando direto
  (pelo perfil)"* e *"Jogando direto (Sony)"*. **Grau: MEDIDO** (as duas linhas
  foram lidas no fonte de hoje). É o mesmo painel, na mesma tela dela, dizendo o
  nome velho um centímetro acima do nome novo.
- **O portão de vocabulário só olha listas de pares.** Ele casa
  `_MODE_ITEMS` contra `let entries` e contra `_MODE_KIND_ITEMS`; **frase solta**
  (a linha de estado do applet, os tooltips do `main.glade`, os avisos da aba
  Emulação) fica fora do alcance dele — foi assim que o item anterior
  sobreviveu. **Grau: SUSPEITA COM MECANISMO** — o critério do teste foi lido e
  fecha; nenhuma renomeação nova foi construída para provar a passagem.
- **`coop off` sai com o mesmo código de "daemon offline recusou".** O
  `cmd_coop.py` usa `Exit(code=2)` tanto para a recusa de política quanto para
  `IpcError` (*"daemon recusou chamada"*), e o `3` fica com o daemon inacessível.
  Um script não distingue *"a casa decidiu que isso não desliga"* de *"o daemon
  recusou a chamada"*. **Grau: MEDIDO** (os dois `code=2` estão no mesmo
  arquivo). **Efeito em script real: SEM PROVA** — não se sabe de nenhum.
- **Controle de outra marca ainda não vira jogador.** "Cada controle é um
  jogador" vale para os controles que o co-op sabe promover; o Pro Controller e
  o 8BitDo entram na mesa e caem todos no jogador 1. A dona da queixa é a
  [LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md),
  que está em **PROPOSTA** e depende de duas respostas dela. **Grau: MEDIDO
  naquela sprint** (medição ao vivo, 06/08 às 21h08); aqui, herdado.
- **A decisão não cura o P2 que dura dois segundos.** Tirar o interruptor deu a
  ela um gesto para **desfazer** o defeito ("Reconciliar jogadores"), não o
  conserto. A dona segue sendo a
  [COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md),
  e a prioridade continua alta. **Grau: MEDIDO** (está escrito assim no bloco
  "CUMPRIDO" da PEDIDOS-DELA-01).
- **A frase "N controles = N jogadores" se cala exatamente no estado do
  defeito.** `_format_players_hint` só afirma quando o daemon numerou N
  jogadores distintos — o que está certo (afirmar antes seria mentir), mas
  significa que, com dois controles na mesa e o P2 ainda não de pé, a aba Início
  **não diz nada**. Quem fala nesse caso é o banner, e só para a suspensão por
  Steam Input (`CONTAGEM-E-COOP-01`). **Grau: SUSPEITA COM MECANISMO** — os dois
  caminhos foram lidos; o estado intermediário não foi construído em bancada.
- **Um downgrade pode deixar o opt-out órfão de volta.** A migração é one-shot
  com marker: instalar a versão nova apaga o `coop_disabled.flag` e grava o
  marker; uma versão antiga rodando depois pode regravar o flag, e a migração
  não roda de novo. Hoje isso é **inofensivo** — nada nesta versão lê o flag —,
  mas é dívida que confunde a próxima leitura. **Grau: SUSPEITA COM MECANISMO**
  (o caminho foi lido; o downgrade não foi executado).
