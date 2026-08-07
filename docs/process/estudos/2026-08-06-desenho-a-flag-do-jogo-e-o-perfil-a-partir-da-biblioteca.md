# Desenho para aprovar ou reprovar — a caixinha do jogo e o "novo perfil para um jogo da Steam"

**Data:** 06/08/2026. **Árvore:** `restauro/inicio-da-sessao`, HEAD `ae32c10`, com as
modificações não commitadas do `git status` em pé. **Nada foi alterado nesta sessão.**
Todo `caminho:linha` abaixo foi reaberto e conferido hoje, nesta árvore — os números de
sprints anteriores já divergiam em pontos que estão corrigidos aqui.

**Graus, declarados em toda afirmação factual:**

- **MEDIDO** — li o arquivo nesta sessão, ou o `grep` fecha a conta.
- **SUSPEITA COM MECANISMO** — li o caminho de código e ele fecha; não observei rodando.
- **SEM PROVA** — está dito e ninguém verificou.

---

## 1. O que muda para você

1. No editor de perfil, com **"Jogar pelo Hefesto"** escolhido, nasce **uma caixinha** que
   diz se aquele jogo está na sua lista de exceções — e agora dá para **desmarcar**, o que
   hoje só dá pela linha de comando.
2. Na barra de Perfis nasce **um botão**: **"Novo para um jogo da Steam"**, que abre uma
   lista com os **nomes** dos seus jogos e cria o perfil daquele jogo já preenchido.
3. A caixinha **não é um modo novo**. Os quatro modos continuam os mesmos, na mesma ordem.
4. A caixinha **vale no clique**, não no "Salvar este perfil" — e a tela diz isso.
5. **O mesmo arquivo passa a ter um nome só** nas três abas: hoje ele se chama "Este jogo
   não funciona" na Sistema e "Exceção por jogo" na Emulação, e isso confunde.

E uma coisa que **não** muda, e é a parte desconfortável: **hoje, marcar um jogo tira o
controle do Hefesto daquele jogo** — o contrário do que você explicou. Isso é a seção 5.

---

## 2. A tela

### 2.1 O editor de perfil, com a caixinha marcada

Legenda: `[ X ]` = segmento **escolhido** do seletor; `( X )` = segmento disponível;
`[x]` = caixinha marcada; `[ ]` = desmarcada; `(apagada)` = insensível.

```
+---------------------------------------------------------------------------+
| ( Novo ) ( Novo para um jogo da Steam ) ( Duplicar ) ( Remover )           |
| ( Ativar ) ( Recarregar )                                                  |
+---------------------------------------------------------------------------+
| Editor do perfil                                    Modo avançado  [ O== ] |
|                                                                           |
| Nome:        [ Mullet Mad Jack                                          ] |
| Prioridade:  |-----------------------------------------------O------| 200 |
|                                                                           |
| Aplica a:                                                                 |
|   ( Qualquer )  ( Steam )  ( Navegador )                                  |
|   ( Terminal )  ( Editor )  ( Jogo )                                      |
|   [ Jogo da Steam ]                                                       |
|                                                                           |
| Nome do jogo: [ 2111190                                                 ] |
|                                                                           |
| +-- Modo (o que este perfil liga ao ativar) ---------------------------+  |
| |  ( Não mexer no modo )  ( Controlar o PC )  [ Jogar pelo Hefesto ]   |  |
| |  ( Conexão Nativa (Sony) )                                          |  |
| |                                                                     |  |
| |  O jogo vê o controle como:  ( DualSense (botões PlayStation) )      |  |
| |                              [ Xbox 360 ]                            |  |
| |                                                                     |  |
| |  [x] Este jogo está na sua lista de exceções                        |  |
| |      Mullet Mad Jack (appid 2111190). Vale para a máquina toda e     |  |
| |      já valeu: esta caixa não espera o "Salvar este perfil".         |  |
| |      Hoje, neste jogo, quem o jogo recebe é o controle físico —      |  |
| |      a máscara acima não vale e o co-op sai.                         |  |
| |                                                                     |  |
| |  "Não mexer no modo" = ativar este perfil deixa o sistema            |  |
| |  exatamente como está.                                               |  |
| +---------------------------------------------------------------------+  |
|                                                                           |
|                                                   [ Salvar este perfil ]  |
+---------------------------------------------------------------------------+
```

São **duas** frases embaixo da caixinha, não cinco. A terceira coisa que ela precisa saber
— *quando* marcar — vai para o **tooltip** da caixinha, que é onde esta casa já põe o
contexto: o comentário de `app/actions/profiles_actions.py:105-108` diz, sobre o seletor
"Aplica a", *"rótulos curtos para caber na aba; o contexto completo fica no tooltip"*
(**MEDIDO**). Tooltip proposto:

> Marque quando o jogo mostrar o controle duplicado: dois controles para um só na sua mão.

> **NOTA DATADA — 06/08/2026, 19:56: ESTE TOOLTIP CADUCOU, e o critério é
> outro.** A frase acima fica no registro porque era a melhor leitura possível
> antes do experimento — e porque era a **palavra dela** (*"os controles
> aparecem dobrados lá"*). O que a medição mostrou:
>
> - **O duplicado tem outra cura, e ela já está ligada por padrão.** Quem o cura
>   é o lançador nas Opções de Inicialização, que esconde o físico do jogo. O
>   Sackboy, **fora** da lista, listou **um** controle. Marcar um jogo por causa
>   do duplicado leva um jogo que já funciona para dentro da lista, **onde ele
>   perde o co-op sem ganhar nada**.
> - **O critério certo é de onde vem o DualSense daquele jogo.** A lista serve a
>   jogos cujo DualSense **passa pela Steam** — o Mullet Mad Jack pede os efeitos
>   à API da Steam, e sem o Steam Input **daquele jogo** o pedido não tem por onde
>   chegar. Jogo que fala com o controle sozinho **não precisa** da lista.
>
> **TOOLTIP NOVO, proposto:**
>
> > Marque quando o jogo só reconhecer o controle com o Steam Input dele ligado —
> > nesses jogos é a Steam que entrega o DualSense. Se o controle já funciona sem
> > a lista, não marque: aqui o co-op sai e a máscara acima não vale.
>
> **De onde vem cada palavra** (todas conferidas nesta árvore, hoje):
>
> | Pedaço | Procedência | Grau |
> |---|---|---|
> | "Marque quando" | a forma do tooltip anterior, desta mesma página — só o critério muda | MEDIDO |
> | "o jogo só reconhecer o controle" | o **inverso literal** de *"Use quando um jogo específico ignora o controle"*, `gui/main.glade:2430` | MEDIDO |
> | "Steam Input" | `gui/main.glade:2951` (rótulo "Steam Input:") e `:2977` ("Desligar Steam Input") | MEDIDO |
> | "é a Steam que entrega o DualSense" | *"o controle passa a ser entregue direto pela Steam"*, `gui/main.glade:2430`, cruzado com "DualSense (PS)" de `profiles_actions.py:138-141` | MEDIDO |
> | "a lista" | *"porque esse jogo não está na sua lista de exceções"*, `app/actions/emulation_actions.py:339` | MEDIDO |
> | "o co-op sai" | *"esse jogo fica sem cor, gatilhos e co-op do Hefesto"*, `gui/main.glade:2430` | MEDIDO |
> | "a máscara acima não vale" | "O jogo vê o controle como:", `profiles_actions.py:644` — o seletor que fica dois centímetros acima | MEDIDO |
>
> **Duas palavras recusadas, e por quê:**
>
> - **"nativo" / "Conexão Nativa (Sony)"** — pela mesma razão da seção 3.1: é um
>   **modo** do PC inteiro, e fica no mesmo frame. Dizer *"jogo com DualSense
>   nativo não precisa da lista"* a dois centímetros do seletor de modo é
>   convidar a leitura errada. O tooltip diz o **sintoma** (*"o controle já
>   funciona"*), não a categoria.
> - **"Steamworks"** — é jargão de quem programa, não existe em string de tela
>   nenhuma deste projeto, e a própria atribuição está em **SUSPEITA COM
>   MECANISMO**. A tela fala em **"a Steam"**, que é o que ela vê.
>
> **Grau do critério novo:** o **comportamento** dos dois jogos é MEDIDO; a
> atribuição *este usa a API da Steam, aquele fala direto* é **SUSPEITA COM
> MECANISMO** — ninguém leu os símbolos dos binários. O tooltip proposto só
> afirma o que é observável **por ela**, de propósito.

### 2.2 Os outros três estados da mesma caixinha

**Desmarcada, perfil de jogo da Steam** (só as linhas que mudam):

```
| |  [ ] Este jogo está na sua lista de exceções                         |  |
| |      Mullet Mad Jack (appid 2111190). Fora da lista, o Hefesto        |  |
| |      desliga o Steam Input deste jogo no próximo ciclo.               |  |
```

**Perfil que não é de um jogo da Steam** ("Aplica a" em Qualquer/Steam/Navegador/Terminal/
Editor/Jogo, ou campo do jogo vazio):

```
| |  [ ] Este jogo está na sua lista de exceções           (apagada)     |  |
| |      Este perfil não é de um jogo da Steam. Escolha "Jogo da Steam"   |  |
| |      em "Aplica a" e diga o número do jogo.                           |  |
```

**Enquanto grava** — a caixinha nunca pisca para o estado que ela pediu, só para o que o
disco confirmou:

```
| |  [x] Este jogo está na sua lista de exceções           (apagada)     |  |
| |      Anotando...                                                      |  |
```

**Não consegui ler a lista** (permissão, disco):

```
| |  [ ] Este jogo está na sua lista de exceções           (apagada)     |  |
| |      Não consegui ler a sua lista de exceções.                        |  |
```

### 2.3 O diálogo do botão novo

```
+-- Novo perfil para um jogo da Steam ----------------------------------+
|                                                                       |
|  Jogos da Steam instalados nesta máquina                              |
|                                                                       |
|  Jogo                                   Perfil        Steam Input     |
|  ------------------------------------------------------------------   |
|  Mullet Mad Jack (appid 2111190)        "Mullet"      na lista        |
|  <jogo> (appid 1599660)                 --            --              |
|  <jogo> (appid 1179080)                 --            --              |
|  <jogo> (appid 1332010)                 2 perfis      --              |
|  ... (13 jogos)                                                       |
|                                                                       |
|  Na sua lista de exceções, mas não vejo instalado                     |
|  ------------------------------------------------------------------   |
|  appid 620                              --            na lista        |
|                                                                       |
|  13 jogos. 2 já têm perfil. 2 na lista de exceções.                   |
|                                                                       |
|                             ( Cancelar )   [ Criar perfil ]           |
+-----------------------------------------------------------------------+
```

O botão da direita **muda com a linha escolhida**: `[ Criar perfil ]` quando não há perfil,
`[ Abrir perfil ]` quando já há (e aí **não cria um segundo**), `[ Tirar da lista de
exceções ]` na seção de baixo.

### 2.4 A aba Sistema, que precisa mudar junto

Hoje o mesmo arquivo tem outro nome e uma promessa contrária. Estado atual, **MEDIDO** em
`src/hefesto_dualsense4unix/gui/main.glade:2429-2430`:

```
  ANTES (hoje, na aba Sistema)
  ( Este jogo não funciona )
    tooltip: "...nele o controle passa a ser entregue direto pela Steam e o
              Hefesto sai da frente. (...) Atenção: ainda não existe um botão
              para desmarcar..."

  DEPOIS (nesta proposta)
  ( Pôr este jogo na lista de exceções )
    tooltip: "Põe o jogo que você acabou de abrir na sua lista de exceções:
              nela o Hefesto não desliga o Steam Input dele. Para tirar,
              desmarque a caixa no perfil do jogo, na aba Perfis."
```

Duas portas para o mesmo arquivo só param de confundir quando têm a **mesma placa**.

> **NOTA DATADA — 07/08/2026: o bloco ANTES já não existe.** O tooltip da aba
> Sistema foi reescrito nesta data, e as duas frases que este desenho cita
> caíram por motivos diferentes:
>
> - *"o Hefesto sai da frente"* saiu porque está **refutada pela metade** pela
>   medição dela de 06/08
>   ([CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
>   seção *A INVERSÃO*, **grau MEDIDO**): o que a marca entrega é a **entrada**;
>   a saída — cor, gatilhos, vibração — continua do Hefesto;
> - *"ainda não existe um botão para desmarcar"* saiu porque **passou a
>   existir**, por decisão dela (resposta 1 do painel de 07/08): a caixinha
>   `profile_steam_input_check`, no editor do perfil da aba Perfis — que é
>   exatamente onde este desenho a colocou.
>
> O **nome** do botão, porém, continua *"Este jogo não funciona"*: a
> unificação em *"lista de exceções"* que a seção P1 recomenda **não foi
> executada** e segue aberta. Este bloco fica como registro do estado de 06/08.

---

## 3. Cada rótulo, e de onde ele deriva

Regra que me impus depois das duas reprovações: **nenhuma palavra entra sem procedência**.
A coluna "grau" diz se eu conferi a procedência hoje.

| O que aparece na tela | De onde vem | Grau |
|---|---|---|
| "Não mexer no modo" / "Controlar o PC" / "Jogar pelo Hefesto" / "Conexão Nativa (Sony)" | `app/actions/profiles_actions.py:127-135` (`_MODE_KIND_ITEMS`) — intactos | MEDIDO |
| "O jogo vê o controle como:" | `profiles_actions.py:644` | MEDIDO |
| "DualSense (botões PlayStation)" / "Xbox 360" | `profiles_actions.py:138-141` (`_MODE_FLAVOR_ITEMS`) | MEDIDO |
| "Jogo da Steam" | `profiles_actions.py:110-118` (`_APLICA_A_ITEMS`) | MEDIDO |
| "Nome do jogo:" | `gui/main.glade:2055` | MEDIDO |
| "Salvar este perfil" | `gui/main.glade:2199-2200` | MEDIDO |
| "Modo (o que este perfil liga ao ativar)" | `gui/main.glade:2164` (rótulo do frame) | MEDIDO |
| **"sua lista de exceções"** | `app/actions/emulation_actions.py:339` — frase viva na aba Emulação: *"porque esse jogo não está na sua lista de exceções"* | MEDIDO |
| **"Steam Input"** | `gui/main.glade:2951` (rótulo "Steam Input:") e `:2977` ("Desligar Steam Input") | MEDIDO |
| **"o Hefesto desliga no próximo ciclo"** | `emulation_actions.py:340-341`, literal | MEDIDO |
| ~~**"controle duplicado"** (no tooltip)~~ | `app/actions/daemon_actions.py:938` (texto de diálogo, na tela dela) e `docs/usage/jogos-e-mascaras.md:42`, `docs/usage/modos.md:77,84` | MEDIDO — **mas saiu do tooltip em 06/08/2026**: a procedência da palavra está certa, o **critério** que ela expressava é que caducou. Ver a nota datada da seção 2.1 |
| **"o jogo só reconhecer o controle"** (tooltip novo, 06/08) | inverso literal de *"Use quando um jogo específico ignora o controle"*, `gui/main.glade:2430` | MEDIDO |
| **"é a Steam que entrega o DualSense"** (tooltip novo, 06/08) | *"o controle passa a ser entregue direto pela Steam"*, `gui/main.glade:2430` | MEDIDO |
| **"Mullet Mad Jack (appid 2111190)"** | `integrations/steam_launch_options.py:831` (`rotulo_do_jogo`) — o appid nunca some | MEDIDO |
| **"Novo para um jogo da Steam"** | "Novo" de `gui/main.glade:1856` + "Jogo da Steam" de `_APLICA_A_ITEMS` | MEDIDO |
| **"Tirar da lista de exceções"** | "lista de exceções" acima + o verbo do `cli/cmd_steam.py` | MEDIDO |
| **"o número do jogo"** | tooltip que já existe: *"Número do jogo na Steam (o da URL da loja)"*, `profiles_actions.py:99-103` | MEDIDO |

### 3.1 As três palavras que eu recusei, e por quê

| Candidata | Por que caiu |
|---|---|
| **"entrada da Steam"** | Eu ia usar, achando que reciclava. **Está errado, e a correção é minha:** as três ocorrências (`daemon_actions.py:321`, `:522`, `:532`) são **comentário e docstring**, nenhuma é texto de tela (**MEDIDO** por `grep`). Estrear termo achando que o recicla é exatamente o erro das duas rodadas reprovadas. A tela diz **"Steam Input"**, e é isso que a caixinha diz. |
| **"Conexão Nativa (Sony)"** | É um **modo** do PC inteiro, e fica **duas linhas acima**, no mesmo frame (`profiles_actions.py:134`). Dois nomes iguais para coisas diferentes, a dois centímetros, é a confusão que você já reprovou. |
| **"biblioteca"** | Palavra da Steam, **não existe em nenhuma string de tela** deste projeto (**MEDIDO**: o `grep` em `src/` só acha comentário e docstring, inclusive `daemon/launch_env.py:35`). O diálogo se chama "Jogos da Steam instalados nesta máquina". |

### 3.2 Nota datada, 06/08/2026 — "dobrado" e "duplicado" são o mesmo defeito com dois nomes

A sua palavra foi *"os controles aparecem **dobrados** lá"*. A palavra que o produto já
escreve na tela é **"duplicado"** — e as duas convivem **na mesma frase**, hoje, em
`gui/main.glade:2829`: *"o controle também não aparece **duplicado** — layout PS sem o
controle **dobrado**"* (**MEDIDO**).

Decisão que peço junto com este desenho: **fica "duplicado"**, porque é a palavra que já
está em mais superfícies (um diálogo real em `daemon_actions.py:938` e duas páginas de
`docs/usage/`), e o `main.glade:2829` perde o "dobrado" na mesma leva. A palavra "dobrado"
não se apaga do registro: ela é a sua, é o nome do sintoma como você o viu, e fica anotada
aqui. Se você preferir o contrário, é uma troca de texto, não de desenho.

---

## 4. Onde o dado mora — e por que a caixinha não é um campo do perfil

A regra do desenho é uma só:

> **Um fato, um arquivo, um dono. A tela é janela, nunca cópia.**

A lista de exceções é **global, por número de jogo**, num arquivo de texto
(`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`,
`integrations/steam_launch_options.py:726,742` — **MEDIDO**). O perfil é um JSON por
perfil. São duas granularidades diferentes.

**Decisão: a caixinha mora no editor do perfil, é revelada pelo perfil, e o dado que ela
liga e desliga é a lista. O perfil não ganha campo nenhum.**

O que isso resolve de graça (tudo **MEDIDO** por leitura hoje):

| Armadilha | Por que ela desaparece |
|---|---|
| **Dois perfis para o mesmo jogo** | Não podem discordar: as duas caixinhas leem a mesma linha do mesmo arquivo. Não existe "quem salvou por último". |
| **Importar/exportar perfil** | O JSON não ganha campo, então nada viaja. Um perfil de terceiro **não escreve** na configuração de Steam dela ao ser importado. |
| **Máquina de outra pessoa** | O perfil chega, a caixinha lê a lista **daquela** máquina e mostra o que ela diz. Verdade, não herança. |
| **Voltar para uma versão anterior** | `Profile.model_config = ConfigDict(extra="forbid")` (`profiles/schema.py:502`) deixa de ser risco: sem campo novo, um binário antigo não rejeita perfil nenhum. |
| **As cinco guardas do editor** (`_ha_trabalho_no_editor:895`, `_populate_editor:1904`, `on_profile_new:1228`, `on_profile_save:1517`, `_build_profile_from_editor:2208`) | A caixinha não é estado salvável, então não passa por nenhuma delas. Zero risco de repetir SALVAR-NAO-REBAIXA ou NUNCA-TROCA-O-ALVO num campo novo. |
| **O "Salvar Perfil" do rodapé apagando o campo** | `app/draft_config.py` reconstrói o `Profile` do zero; campo não transportado é campo apagado. Não há campo. |

O preço, e ele é real: **dentro do editor tudo só vale no "Salvar este perfil"; esta
caixinha vale no clique.** Não escondo — é a primeira frase embaixo dela, e é a pergunta
P2 da seção 8.

### 4.1 O mecanismo que impede a caixinha de mentir

Ela **nunca** é posicionada pela intenção do clique. Sempre por uma releitura do disco.

```
clique
  -> caixinha fica insensível, a linha de baixo vira "Anotando..."
  -> fora da thread da janela (app/ipc_bridge.py:153, run_in_thread):
       add_appid_to_steam_input_allowlist   (steam_launch_options.py:859)
         ou remove_appid_from_steam_input_allowlist (:915)
       -> RELÊ o arquivo com parse_steam_input_allowlist (:756)
       -> devolve (status, presente_no_arquivo, rótulo do jogo)
  -> de volta na janela:
       a caixinha é posicionada pelo DISCO, não pelo clique
       as linhas de baixo são repintadas
       _recarregar_apos_allowlist()          (daemon_actions.py:1305)
```

Consequências, todas deliberadas:

- **Escrita que falha** devolve `"erro"` sem levantar (`steam_launch_options.py:911-912` —
  **MEDIDO**), e a caixinha **volta** para onde o disco está. Nunca fica marcada sobre um
  arquivo intocado.
- **A leitura de disco nunca acontece na thread da janela.** Precedente literal, com o
  mesmo I/O: `emulation_actions._refresh_steam_input_status`, cujo comentário diz que a
  tradução de número para nome **lê o disco** e por isso acontece na thread (**MEDIDO**).
- **Desmarcar passa a existir.** Hoje `remove_appid_from_steam_input_allowlist` tem **zero
  chamadores** em `app/` e `gui/` — só `cli/cmd_steam.py:160,169` (**MEDIDO** por `grep`).
  Há um portão vivo cobrando isso: `tests/unit/test_steam_input_desfazer.py:202`,
  `test_a_remocao_nao_voltou_a_ser_orfa`. Esta proposta é o primeiro chamador de janela.
- **Cada leitura carrega um número de geração**, e a resposta que volta com número velho é
  descartada. Sem isso, clicar no perfil B enquanto a leitura do A está em voo pinta a
  caixinha de B com o número do A — mentira silenciosa, a pior classe. **SUSPEITA COM
  MECANISMO** (é desenho, não código medido).

---

## 5. O código de hoje faz o contrário do que você quer

> **NOTA DATADA — 06/08/2026, 19:56: esta seção foi escrita ANTES do
> experimento, e ele rodou.** O título continua valendo para **um terço** do que
> ele diz, e caducou para os outros dois. Nada abaixo é apagado; a correção está
> na **seção 5.4**, no fim desta parte.

**GRAU: MEDIDO por leitura, com a suíte travando o comportamento.**

Quando um jogo da lista entra em sessão, `sync_steam_input_exception`
(`daemon/subsystems/gamepad.py:231`) faz cinco coisas. **Quatro** são exatamente o que você
descreveu. **A quinta é o oposto.**

| # | O que acontece | Onde | Bate com o que você disse? |
|---|---|---|---|
| 1 | solta o controle físico para o jogo (o grab é pulado) | `gamepad.py:165-166` | sim |
| 2 | devolve o hidraw do físico (o esconder é pulado) | `gamepad.py:207-212` | sim |
| 3 | o arquivo de ambiente daquele jogo deixa de esconder o físico | `daemon/launch_env.py:1010-1022` | sim |
| 4 | o guarda **não** zera o Steam Input daquele jogo | `scripts/disable_steam_input.sh:269-273` | sim |
| 5 | **o gamepad do Hefesto é derrubado, e o co-op inteiro cai junto** | `gamepad.py:284` -> `:425`, teardown em `:493-497` | **NÃO — é o contrário** |

A docstring declara o princípio em letras (`gamepad.py:429-434`, **MEDIDO**): *"um controle
físico produz exatamente UM dispositivo de jogo: nos appids da allowlist esse dispositivo é
o FÍSICO"*. E o co-op cai porque `coop.disable()` roda antes (`gamepad.py:494-496`), com
`coop_enabled: bool = True` sendo o único piso desde 06/08 (`daemon/lifecycle.py:160`,
**MEDIDO**) — ou seja, **toda** mesa com dois controles perde P2 em diante naquele jogo.

Você quer o duplicado curado **mantendo** o lado do Hefesto, com a sua máscara e as
features das abas. **Enquanto o código for este, marcar a caixinha anula o seletor de
máscara que está logo acima dela, dentro da mesma caixa.** É por isso que a segunda frase
embaixo da caixinha existe, e é por isso que ela não pode ser cortada.

### 5.1 A pergunta que decide o comportamento — e que nenhum agente consegue responder

O gamepad virtual do Hefesto **é** um DualSense Edge de verdade, com hidraw
(`integrations/uhid_gamepad.py:122`, **MEDIDO**), e o código proíbe escondê-lo justamente
porque é por ele que vibração, gatilho e lightbar do jogo chegam (`launch_env.py:89-91`,
**MEDIDO**).

**A Steam, com o Steam Input ligado para aquele jogo, aceita ESSE aparelho como o DualSense
que ela entrega ao jogo?** **SEM PROVA.** É o passo 2.4 de
`docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md`,
e precisa de você, do controle e da Steam.

- **Se aceitar:** inverte-se **quem some**. Esconde-se o **físico** (como em qualquer outro
  jogo), mantém-se o gamepad do Hefesto com a sua máscara, mantém-se o co-op, e o Steam
  Input daquele jogo continua ligado. O invariante "um controle, um dispositivo" fica
  intacto; muda **qual** é o um. O teste `tests/unit/test_jogo01_um_dispositivo_por_controle.py`
  não é apagado: é **invertido**, com nota datada.
- **Se recusar:** o comportamento de hoje é o único possível, e o que muda é o **texto**,
  não o código. A caixinha continua existindo (é flag, não modo) e a segunda frase vira
  doutrina em vez de aviso provisório.

**A tela que desenhei sobrevive aos dois desfechos.** O comportamento não.

### 5.2 O que impede a tela de mentir nos dois casos

A segunda frase embaixo da caixinha **não é texto fixo escrito na janela**. Ela é derivada
do que o daemon publica. O daemon já publica o bloco `steam_input` com `excecao_ativa` e
`vpad_suspenso` (`daemon/ipc_handlers.py:1432-1457`, **MEDIDO**) e o par do co-op
(`:1857-1872`). Falta **uma chave** dentro do mesmo bloco: **quem o jogo recebe nesta
compilação** — o físico ou o do Hefesto. Derivada do código em execução, gravada em lugar
nenhum, sem virar um quarto cadastro.

Com esse fio, se o comportamento mudar e ninguém lembrar de mexer na janela, **a frase muda
sozinha**. Sem ele, o rótulo é promessa — e promessa caduca. É o item que eu defenderia até
o fim se tivesse de cortar todo o resto.

### 5.3 Notas datadas que este desenho pede (decisão medida não se apaga)

1. `daemon/subsystems/gamepad.py:429-434` — a metade descritiva (o duplicado é real, medido
   em 25/07 e 26/07) **fica e está certa**; a escolha do físico como sobrevivente é a que
   você contesta em 06/08.
2. `daemon/launch_env.py:44-49` e `:482-486` — a leitura *"a allowlist é o Hefesto sair de
   cena neste jogo"* caduca se o passo 2.4 fechar positivo.
   **Fechou, em 06/08/2026 às 19:44 (seção 5.4): a frase caducou, e por um motivo
   ainda mais forte do que o previsto** — não é que ela deixe de valer se o
   desenho mudar; ela **já** descreve mal o código de hoje, porque "sair de cena"
   só vale para a **entrada**. A nota datada dessas linhas passa a ser devida
   independentemente de qualquer decisão de produto.
3. `daemon/launch_env.py:35` — *"Resolução no MÍNIMO, sem UI de biblioteca de jogos"*
   (**MEDIDO**, a linha está lá). O diálogo da seção 2.3 **revoga** essa decisão, a seu
   pedido, e a revogação ganha data.
4. `gui/main.glade:2829` — a frase com "duplicado" e "dobrado" juntos; ver seção 3.2.

### 5.4 O RESULTADO — o experimento rodou em 06/08/2026, das 19:34 às 19:56

**Registro completo, com carimbo e journal, em
[CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
seção *O RESULTADO*.** Aqui fica só o que muda **neste** desenho.

#### O desfecho foi o positivo, e ele é maior do que esta seção previa

**GRAU: MEDIDO.** Dois jogos, o mesmo controle, dez minutos de intervalo, o
global `SteamController_PSSupport` em `"0"` o tempo todo:

| | Mullet Mad Jack (`2111190`, **na** lista) | Sackboy (`1599660`, **fora**) |
|---|---|---|
| `X-Box 360 pad` do Steam Input | **1** | **0** |
| gamepad do Hefesto | derrubado (4 nós -> 0) | de pé (4 nós) |
| controles que o jogo listou | **um** | **um** |
| gatilhos | **duros** — a Resistência **dela** segurou | **moles** — a dela não segurou |
| lightbar | o **vermelho dela**, e **ficou** | **azul da Sony**; aplicar a cor dela, o jogo devolve |

**O M-04 fechou POSITIVO:** a Steam honra o Steam Input por jogo com o global
desligado. **E a segunda metade, que ninguém tinha escrito:** durante a exceção o
Hefesto abre mão da **ENTRADA** e **mantém a SAÍDA inteira** — `hidraw abertos
pelo daemon: 1` com o Mullet aberto, e nenhum dos **oito** chamadores de
`steam_input_excecao_ativa` mora em `core/`: estão todos em
`daemon/subsystems/gamepad.py` (**MEDIDO** por `grep` nesta árvore, 06/08).

#### O que caduca nesta seção 5

| O que a seção 5 diz | Veredito da medição |
|---|---|
| itens 1 a 4 da tabela (grab, hidraw, env, guarda) | **confirmados** |
| item 5 — *"o gamepad do Hefesto é derrubado, e o co-op cai junto"* | **confirmado, e medido na tela**: o virtual foi de 4 nós a 0, e o jogo listou um controle Xbox |
| *"marcar a caixinha anula o seletor de máscara"* | **confirmado**: com máscara `dualsense` escolhida, o Mullet mostrou botões de **Xbox** |
| **o título da seção** — *"o código faz o contrário do que você quer"* | **CADUCA PELA METADE.** Ela pediu três coisas: o duplicado curado, a máscara dela e **as features das abas**. As features das abas **já valem hoje**, durante a exceção — cor e gatilhos dela obedeceram. O que não vale é a **máscara** e o **co-op** |
| *"a segunda frase embaixo da caixinha não pode ser cortada"* | **continua valendo**, e agora ela é **mais curta e mais verdadeira**: o que sai é a máscara e o co-op, **não** os ajustes das abas |

**A frase da caixinha (seção 2.1) fica errada por excesso, e a correção é esta:**

```
  ANTES  "Hoje, neste jogo, quem o jogo recebe é o controle físico —
          a máscara acima não vale e o co-op sai."

  DEPOIS "Neste jogo quem o jogo recebe é o controle físico: a máscara
          acima não vale e o co-op sai. A sua cor e os seus gatilhos
          continuam valendo."
```

A palavra **"Hoje"** cai junto, e por medição: ela prometia um estado
provisório, e o comportamento medido é **estrutural** — não existe portão da
exceção no caminho de saída. Quem escrever essa frase continua obrigado a
derivá-la do daemon (seção 5.2), pela mesma razão de antes.

#### O que a seção 5.1 perguntava NÃO foi respondido — e isto é importante

**GRAU: SEM PROVA, sem mudança.** A pergunta de 5.1 é *"a Steam aceita o **vpad**
como o DualSense que ela entrega ao jogo?"*. O experimento **não** a testou: com
a exceção ativa o vpad é derrubado **antes** de a Steam olhar, então o que se
mediu foi o mundo como ele é, não o mundo invertido. **Os dois desfechos de 5.1
continuam abertos**, e responder aquilo é **outro** experimento — com o vpad de
pé e o Steam Input ligado para o jogo, que é justamente o estado que o código de
hoje impede.

O que mudou é o **preço** da resposta: como as features das abas já sobrevivem à
exceção, a inversão de 5.1 deixou de ser a única forma de dar a ela o que ela
pediu. Ela passou a valer por **máscara e co-op**, que é menos do que se
supunha em 06/08 de madrugada.

#### E um item novo, que este desenho não previa

**GRAU: MEDIDO.** Fora da lista, o **jogo** vence os ajustes dela — o Sackboy
devolveu a lightbar ao azul e amoleceu os gatilhos. É a política escrita em
`core/backend_pydualsense.py:1253-1259` (a camada GAME é o topo da precedência),
com uma exceção: no **rumble** a usuária vence (`gamepad.py:747-748`). **A
caixinha desmarcada não é um estado neutro** — é o estado em que o jogo manda na
luz e no gatilho. Se a tela um dia disser o que a caixinha **desmarcada**
significa, é isto que ela tem de dizer.

---

## 6. Como o perfil novo nasce, quando você escolhe um jogo

Seis coisas, e nada mais (todas as funções conferidas nas linhas citadas, **MEDIDO**):

1. **Nome** = o nome do jogo (`steam_launch_options.nome_do_appid:814`), com queda para
   `"appid <N>"` quando o nome não vira arquivo (barra no nome, título sem letra latina) —
   decidido **na hora de preencher**, não descoberto no Salvar.
2. **Aplica a** = "Jogo da Steam", por `_select_radio` (`profiles_actions.py:1756`).
3. **Nome do jogo** = o número **puro** (`2111190`, nunca `steam_app_2111190`).
   `simple_match.normalize_appid:62` aceita os dois; o caminho de gravação não muda.
4. **Modo** = "Jogar pelo Hefesto" com a máscara **corrente do daemon**, reusando
   `_prefill_modo_de_jogo:1070` — ela lê a máscara viva de propósito, porque recriar o
   gamepad com jogo aberto invalida o que está em uso.
5. **Prioridade** = `_prioridade_acima_dos_catch_all:2100`, calculada, nunca digitada.
6. **Nada mais** — sem cor, sem gatilho, sem ajuste por controle.

**A caixinha nasce lendo o arquivo.** Escolher um jogo **não** o põe na lista de exceções.
Veto escrito duas vezes nas sprints de 05/08 e 06/08, e respeitado aqui.

**Se o jogo já tem perfil, não nasce um segundo.** Falta um ajudante para isso, e é o
achado central desta parte: a janela **não tem hoje como responder "quem já é dono deste
jogo"** — `find_by_slug` responde por nome de arquivo, e `perfis_em_disputa`
(`profiles_actions.py:222`) só olha perfis "Qualquer" (**MEDIDO**). A proposta é extrair
para função pública o predicado que o daemon já tem privado
(`daemon/launch_env._steam_profiles:755`), ao lado de
`profiles/steam_app.steam_appid_from_wm_class:43`, e servir com ele **três** superfícies: o
diálogo, a importação de perfil e o verificador `profiles/sanidade.verificar_perfis:358`.
Um dono, três leitores.

**Nota datada, 06/08/2026:** a prioridade calculada devolve **200 saturado** no seu disco
hoje (o catch-all mais alto está em 191 — **MEDIDO** por outro leitor nesta sessão, não por
mim). Dois perfis de jogo criados hoje empatam em 200. Não muda quem vence o autoswitch,
mas cria o empate que `sanidade._prioridades_empatadas:258` classifica como aviso. Um botão
que facilita criar perfis de jogo torna isso frequente; o conserto de verdade é o catch-all
em 191, que é dado seu.

---

## 7. O que isto NÃO faz

Honestamente, e cada item com o grau.

1. **Marcar a caixinha NÃO liga o Steam Input do jogo.** **MEDIDO** em
   `scripts/disable_steam_input.sh:269-273`: o `awk` apenas **preserva** o
   `UseSteamControllerConfig` daquele jogo — ninguém escreve 1 ou 2 em lugar nenhum. Se o
   guarda já zerou aquele jogo, marcar não o religa, e ligar continua sendo gesto seu
   dentro da Steam. Pior: as chaves globais são zeradas **sem exceção nenhuma**
   (`:267-268`, sem o teste da lista). Ler o estado por jogo exigiria um leitor novo que
   **não existe** — `integrations/storm_doctor.py` pula de propósito os jogos da lista.
   Deixei de fora e declaro: é a lacuna mais provável de você sentir como *"marquei e nada
   aconteceu"*.
2. **A marca vale por inteiro só no próximo lançamento do jogo.** **MEDIDO**:
   `daemon/launch_env.py:31-34` diz que o arquivo de ambiente existe porque *"o jogo é
   lançado ANTES de a janela existir"*, e `_recarregar_apos_allowlist:1305` **rematerializa
   o arquivo**, não reescreve o ambiente de um processo já rodando. Marcar com o jogo aberto
   muda o que o daemon faz ao vivo, e não muda o que o Proton daquela sessão recebeu.
3. **Com o daemon desligado, a segunda frase não tem fonte.** A escrita no arquivo funciona
   (é I/O puro) e o aviso ao daemon é best-effort, dentro de um `suppress`
   (`daemon_actions.py:1318-1324`, **MEDIDO**). Nesse caso a linha do preço não é exibida —
   a janela cala em vez de afirmar. **SUSPEITA COM MECANISMO.**
4. **Se você trocar o modo do perfil, a caixinha some — e o jogo continua na lista.** A
   caixinha vive dentro do bloco que `_sync_mode_options_visibility:698-708` esconde quando
   o modo não é "Jogar pelo Hefesto" (**MEDIDO**), mas a exceção vale por número de jogo,
   independente do modo. O segundo espelho continua existindo: a linha "Exceção por jogo:
   N jogo(s)" da aba Emulação (`emulation_actions.py:359`) e a seção de baixo do diálogo.
   **É um limite declarado, não um descuido.**
5. **Não avisa você de jogo órfão.** Se você trocar o alvo do perfil depois de marcar, o
   número antigo **continua na lista, e isso é a verdade** — ele está lá. Ele aparece na
   seção de baixo do diálogo, com botão de tirar. Mas nada vai até você dizer que existe.
   O dono natural disso é o `doctor`, e é outra sprint.
6. **Não desenhei a flag no applet do COSMIC**, que é a quarta superfície. A única restrição
   que deixo escrita: ele **não pode** mostrá-la como campo do perfil, porque ela não é.
7. **Não há segundo botão dentro do editor.** Considerei um "escolher da lista" ao lado do
   campo do número e cortei: você pediu **um** gesto, e três nomes para um fluxo foi a
   crítica mais dura que este desenho levou. Corrigir o número de um perfil que já existe
   continua sendo digitar, com o tooltip que já ensina onde achá-lo.
8. **Não conserta o rótulo "Nome do jogo:"**, que o próprio código documenta como defeito —
   um rótulo para dois significados (`profiles_actions.py:88-91`, **MEDIDO**). Fica anotado.
9. **Não olhei a tela nesta sessão.** Nenhuma foto. O ASCII é derivado do `gui/main.glade`
   e dos mixins de `app/actions/`; larguras, quebras de linha e o comportamento do seletor
   segmentado em modo `wrap` **não foram verificados ao vivo**. PROVA-DE-TELA-01 continua
   devendo, e a palavra final é sua.
10. **Não rodei a suíte nesta sessão.** Os números de jogos e prioridades vêm dos relatórios
    dos leitores desta sessão e estão marcados como deles.

### 7.1 Duas contas que este desenho paga, e que eu não quero esconder

- **O sinal novo no campo do número quebra 9 arquivos de teste.** **MEDIDO** por `grep`:
  `test_perfil_salva_tudo_abas.py`, `test_abas01_conflito_entre_abas.py`,
  `test_salvar_nao_rebaixa_02_o_novo_perfil_desligava_as_guardas.py`,
  `test_empate01_a_cor_volta_a_ser_dela.py`, `test_profiles_editor_mode.py`,
  `test_modo01_o_modo_jogo_liga_sozinho.py`, `test_gui_perfil_manual_editor.py`,
  `test_r10_slug_e_rename.py`, `test_r12_editor_simples_gui.py` — todos montam um campo de
  mentira **sem** o método de conectar sinal. O campo real
  (`gui/main.glade:2062`) não tem sinal nenhum hoje (**MEDIDO**: zero `<signal>` no bloco),
  e sem ele a caixinha ficaria falando do jogo anterior. Ou os 9 ganham o método, ou a
  produção vira defensiva — e defensiva é o que esta casa costuma reprovar.
  Restrições inegociáveis desse sinal: **não** tocar as marcas de gesto do editor (senão
  reabre NUNCA-TROCA-O-ALVO e SALVAR-NAO-REBAIXA), **espera** antes de ler (o campo dispara
  por tecla), e o temporizador pendente **é cancelado** ao trocar de perfil.
- **O diálogo é superfície nova de verdade.** `app/gui_dialogs.py` tem 516 linhas e **zero**
  ocorrências de lista com colunas (**MEDIDO**) — é tudo caixa de mensagem e prompt de
  texto. E `scripts/gui-captura/retratar_abas.py` fotografa **abas**, não diálogos: a prova
  de tela desse diálogo não tem instrumento e vai ser trabalho manual.

---

## 8. As três decisões que dependem de você

> **RESPONDIDO POR ELA — 06/08/2026.** As três perguntas abaixo ficam como
> estavam, com a recomendação original, porque decisão medida não se apaga e
> porque o raciocínio de cada uma continua valendo. As respostas:
>
> | | Pergunta | Resposta dela | Batia com a recomendação? |
> |---|---|---|---|
> | **P1** | Unificar o nome nas três abas | **SIM** — "lista de exceções" nas três | sim |
> | **P2** | A caixinha vale no clique | **SIM** — grava na hora, sem esperar o Salvar | sim |
> | **P3** | Entregar a caixinha agora | **NÃO — esperar o experimento** — *o experimento fechou às 19:56 de 06/08; ver o bloco logo abaixo desta tabela* | **não** |
>
> **O P3 é o que reordena o trabalho, e a recomendação era o contrário.** A
> razão dela é a que a própria seção 5 expõe: enquanto o experimento não fecha,
> marcar um jogo faz o oposto do que ela quer — derruba o gamepad do Hefesto e o
> co-op, anulando o seletor de máscara que fica dois centímetros acima da
> caixinha. Ela preferiu não pôr na tela um controle cujo efeito contradiz a
> própria intenção, mesmo com a frase avisando.
>
> **Consequência prática, e ela é limpa:** o que depende do experimento é **só a
> caixinha**. Seguem liberados, porque não dependem dele:
>
> - a **unificação do nome** (P1) — seção 2.4 e a tabela da seção 3;
> - o **"Novo para um jogo da Steam"** — seções 2.3 e 6, que respondem a um
>   pedido separado dela ("escolher o jogo e adicionar um novo perfil pro jogo")
>   e não tocam a allowlist.
>
> O P2 fica **decidido e guardado**: quando a caixinha for construída, ela vale
> no clique. Não se pergunta de novo.
>
> O caminho crítico passa a ser o experimento da sprint
> [CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
> que só ela pode rodar.

> **O P3 ESTÁ DESTRAVADO — 06/08/2026, 19:56.** O experimento rodou, com ela, das
> **19:34 às 19:56**, e **fechou**. A condição que ela pôs — *"esperar o
> experimento"* — está **satisfeita**. O P1 e o P2 continuam como ela respondeu:
> não se pergunta de novo.
>
> **A razão dela para travar o P3 caiu por medição, e é isso que destrava.** Ela
> não quis pôr na tela um controle cujo efeito contradiz a própria intenção. O
> experimento mostrou que a contradição é **menor do que se supunha**: marcar um
> jogo **não** cala o Hefesto. Durante a exceção **a cor dela fica e os gatilhos
> dela seguram** — o que sai é a **máscara** e o **co-op**, e só. A frase embaixo
> da caixinha encolhe na mesma proporção (seção 5.4).
>
> **O que isso NÃO autoriza, e a distinção é dela:**
>
> - **não** autoriza inverter quem some (esconder o físico e manter o vpad). Essa
>   é a pergunta da seção 5.1, e ela **continua SEM PROVA** — o experimento não a
>   testou, porque com a exceção ativa o vpad cai antes de a Steam olhar;
> - **não** autoriza mexer na lista dela nem no `steam_input_apps.txt`;
> - **não** dispensa a segunda frase da caixinha: ela continua vindo do daemon
>   (seção 5.2), e é o item que este desenho defenderia até o fim.
>
> **E o tooltip mudou junto:** o critério de *quando* marcar não é mais o
> controle duplicado — é *"o jogo só reconhece o controle com o Steam Input dele
> ligado"*. Texto novo e procedência de cada palavra na nota datada da seção 2.1.

### P1. O mesmo arquivo passa a ter um nome só nas três abas?

Hoje ele é **"Este jogo não funciona"** na aba Sistema (`gui/main.glade:2429`), **"Exceção
por jogo"** na aba Emulação (`emulation_actions.py:359`) e passaria a ser **"lista de
exceções"** no perfil. O tooltip da Sistema ainda promete *"o Hefesto sai da frente"* e
avisa que *"ainda não existe um botão para desmarcar"* — as duas frases ficam contraditórias
no dia em que a caixinha existir (**MEDIDO**, `gui/main.glade:2430`).

> **NOTA DATADA — 07/08/2026: o dia chegou, e as duas frases saíram.** A
> caixinha existe (`profile_steam_input_check`, aba Perfis) e o tooltip da aba
> Sistema foi reescrito — ver a nota da seção 2.4. **A pergunta P1 continua
> aberta**: o que caiu foram as duas frases do tooltip, não o **nome** do
> botão, que segue *"Este jogo não funciona"* nas duas telas.

**Recomendação: sim, unificar em "lista de exceções", na mesma leva.** Duas portas para o
mesmo arquivo só param de confundir quando têm a mesma placa; e deixar em pé um botão
chamado "Este jogo não funciona" para um jogo que você marcou **de propósito porque
funciona** é exatamente a confusão que você reprovou, distribuída em duas telas.

### P2. A caixinha vale no clique, sem esperar o "Salvar este perfil"?

Dentro do editor, tudo hoje só vale no Salvar. Esta caixinha seria a estreia de um gesto
imediato ali — e a razão é que ela **não é do perfil, é do jogo**: o arquivo é global por
número de jogo, e o perfil só dá o contexto.

**Recomendação: sim, vale no clique, com a frase avisando antes do gesto.** A alternativa
(guardar a intenção e só escrever no Salvar) reintroduz a mentira que este desenho existe
para matar: caixinha marcada, disco intocado. Se você preferir o contrário, o desenho muda
de forma — vira campo do perfil, e aí voltam todas as armadilhas da seção 4.

### P3. Entregamos a caixinha agora, com a frase do preço de hoje, ou esperamos o experimento?

O experimento é o passo 2.4 (seção 5.1) e **só você pode rodá-lo** — precisa do controle,
da Steam e de um jogo. Sem ele, a caixinha existe e funciona, mas a segunda frase embaixo
dela diz que a máscara não vale e o co-op sai, que é o oposto do que você quer que a lista
faça.

**Recomendação: entregar agora, com a frase.** A tela sobrevive aos dois desfechos e é a
mesma; só a frase muda, e quem a escreve é o daemon (seção 5.2), então ela muda sozinha
quando o comportamento mudar. Esperar significa continuar sem desmarcar pela janela, que é
o defeito que a própria docstring do código chama de *"na prática irreversível para quem não
mexe em arquivo de configuração"* (`steam_launch_options.py:928-929`, **MEDIDO**).

---

## 9. Os portões que vão avaliar isto

Existem hoje e vão morder (**MEDIDO** por leitura):

- `tests/unit/test_profiles_vocabulario_leigo.py:60-76` — congela os quatro rótulos de modo
  e os dois ids de máscara, nesta ordem. **Esta proposta não os toca**, e é este portão que
  reprova quem transformar a flag em modo.
- `tests/unit/test_steam_input_desfazer.py:202` — exige chamador de `src/` para o desmarcar.
  Esta proposta o satisfaz melhor do que hoje.
- `tests/unit/test_janela_sem_mentira.py:216` (widget invisível não declara sinal) e `:421`
  (tooltip que promete desfazer tem de desfazer) — o segundo é exatamente o que a reescrita
  do tooltip da aba Sistema tem de respeitar.
- `tests/unit/test_vocabulario_das_quatro_superficies.py`,
  `tests/unit/test_r06_allowlist_steam_input.py`,
  `tests/unit/test_steam_input_honestidade.py`,
  `tests/unit/test_steam_input_ponteiros.py`,
  `tests/unit/test_steam_input_d33_nomeia_o_jogo.py`.
- `tests/unit/test_jogo01_um_dispositivo_por_controle.py` — reprova a inversão da seção 5.1
  enquanto ela não for feita **de propósito**, com nota datada.

Portões **novos** que esta proposta pede, e cada um tem de MORDER (arrancar a cura, ver
reprovar, devolver):

1. **A flag nunca virou campo do perfil** — teste sobre os campos do `Profile` que reprova
   se aparecer chave nova. É o portão do desenho inteiro.
2. **A caixinha lê o disco, não o clique** — simular falha de escrita e exigir que ela volte
   ao estado do arquivo.
3. **Dois perfis para o mesmo jogo produzem o mesmo estado de caixinha.**
4. **Exportar com a caixinha marcada e desmarcada dá o mesmo JSON, byte a byte.**
5. **A lista do diálogo não duplica** quando duas pastas de biblioteca apontam para o mesmo
   diretório (o symlink que já foi medido nesta máquina).
6. **A segunda frase vem do daemon**, não de texto escrito na janela.
7. **O temporizador do campo do número é cancelado ao trocar de perfil** — senão é a forma
   exata do NUNCA-TROCA-O-ALVO num campo novo.

---

## 10. Arquivos que este desenho toca, se for aprovado

- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/profiles_actions.py`
  (`:667-669` a caixinha; `:698-708` a visibilidade; `:1007` a reavaliação; `:1228-1354` o
  nascimento com jogo)
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/gui/main.glade`
  (`:1844` o botão novo; `:2062` o sinal que falta no campo; `:2429-2430` o botão e o
  tooltip da aba Sistema; `:2829` a convergência "duplicado")
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/gui_dialogs.py`
  (o diálogo novo, no molde de `prompt_profile_name:32`)
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/steam_launch_options.py`
  (`:831` o rótulo; `:859` e `:915` os dois escritores — o segundo ganha o primeiro chamador
  de janela)
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/profiles/steam_app.py`
  (`:43` o predicado; casa do ajudante "quem já é dono deste jogo")
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/ipc_handlers.py`
  (`:1432-1457` a chave que faz a segunda frase não mentir)
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/daemon_actions.py`
  (`:503-546` a frase compartilhada; `:1255` o botão da Sistema; `:1305` o recarregar)
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/profiles/sanidade.py`
  (`:358` o achado "dois perfis para o mesmo jogo")
- **Só se o passo 2.4 fechar positivo:**
  `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`
  (`:284`, `:425`) e
  `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/launch_env.py`
  (`:35`, `:549-561`, `:1010-1022`)

**Não toca, de propósito:** `profiles/schema.py`, `profiles/loader.py`,
`app/draft_config.py`, `cli/cmd_profile.py` e o formato do `steam_input_apps.txt` — que
continua sendo um número por linha, porque um dos leitores é um `awk` de shell
(`scripts/disable_steam_input.sh:269-273`, **MEDIDO**) que não sabe ler nada mais rico.

**Nada foi alterado nesta sessão.**
