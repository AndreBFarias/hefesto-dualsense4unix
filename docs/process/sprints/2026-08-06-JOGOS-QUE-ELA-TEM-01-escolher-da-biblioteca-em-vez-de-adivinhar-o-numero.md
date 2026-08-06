# JOGOS-QUE-ELA-TEM-01 — escolher da biblioteca em vez de adivinhar o número

- **Escrita em:** 06/08/2026, de madrugada, com a Steam fechada e a biblioteca
  dela varrida ao vivo pelas próprias funções do produto
- **Para quem:** agentes, em execução autônoma. Cada entrega traz a **mordida**
  esperada e o **veto**; a E1 é barata e desobstrui as demais. A **E4 não é
  autônoma** — ela mexe na pasta de perfis dela e precisa da palavra dela
- **Base factual:** medição própria desta sessão (abaixo, tudo com grau) mais
  [o sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
- **Faixa:**
  [a leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
arquivo no disco, execução ao vivo ou `git grep` que fecha a conta; **SUSPEITA
COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi
observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O pedido dela

> *"Outra coisa que não foi mapeada e desenvolvida era o mapeamento default de
> todos os jogos instalados na máquina lá. Assim não precisaríamos adivinhar o
> id de marcação e poderíamos setar um perfil específico pra cada jogo."*

Dito em 06/08/2026. São **dois pedidos numa frase**, e eles têm tamanhos muito
diferentes:

1. **"não precisaríamos adivinhar o id"** — a biblioteca dela vira uma lista para
   escolher, em vez de um número para digitar. **A matéria-prima já existe
   inteira no produto e ninguém a usa para isto** (F1 e F2, abaixo).
2. **"setar um perfil específico pra cada jogo"** — nascer um perfil por jogo.
   **Isto não tem dono nenhum hoje**, é a parte grande, e é a que pode estragar
   a pasta dela se for feita sem cuidado (E4).

---

## O QUE FOI MEDIDO NESTA SESSÃO

### F1 — A enumeração da biblioteca JÁ EXISTE, e só serve ao Proton

**Grau: MEDIDO**, por leitura e por `git grep`.

`integrations/proton_pin.py:942-980`, `list_installed_appids()`, faz exatamente o
que ela pediu:

- parte da `steamapps` padrão e acrescenta **todas** as `path` do
  `libraryfolders.vdf` (`:949-960`);
- `glob("appmanifest_*.acf")` em cada uma (`:963`);
- lê o campo `name` de dentro do manifest (`:971-976`);
- e **filtra ferramentas** — Proton, Steam Linux Runtime, redistributables —
  pelo `_TOOL_MANIFEST_RE` (`:93-96`), porque *"travar o Proton-ferramenta em
  outro Proton não faz sentido"* (a docstring, em `:946-947`);
- best-effort e read-only: manifest ilegível é pulado em silêncio.

**Quem a chama hoje:** `proton_pin.py:822` (o botão *"Travar Proton validado"* da
aba Sistema), `:1077` e `:1128` (o doctor). **Zero chamadores fora do pin de
Proton.** A varredura da biblioteca dela existe, é testada
(`tests/unit/test_proton_pin.py:614-630`, o caso que prova que o filtro de
ferramenta morde) e **nunca chegou perto da aba Perfis**.

É a forma exata que a
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
cataloga — com o agravante de que aqui não é código morto: é código **vivo**,
que só nunca foi oferecido a quem precisava.

### F2 — A tradução appid para nome também já existe, e é honesta

**Grau: MEDIDO.** `integrations/steam_launch_options.py`:

| Função | Onde | O que faz |
|---|---|---|
| `pastas_steamapps` | `:792-811` | a `steamapps` padrão mais as bibliotecas do `libraryfolders.vdf` |
| `nome_do_appid` | `:814-828` | nome do jogo pelo `appmanifest_<appid>.acf`; `None` quando não instalado |
| `rotulo_do_jogo` | `:831-841` | `"Mullet Mad Jack (appid 2111190)"`, ou o cru `"appid 2111190"` sem manifest |

O critério de `rotulo_do_jogo` é o que esta sprint tem de preservar inteiro, e
está escrito na docstring: **nunca inventa nome, e o appid NUNCA some da frase**
— *"é o número que ela precisa para conferir na Steam e o único identificador
que os três cadastros do projeto compartilham"*. Foi a cura do D-33 do estudo,
em 05/08.

### F3 — A varredura está DUPLICADA, e a cópia mais nova tem um defeito que a antiga não tem

**Grau: MEDIDO**, e este é o achado próprio desta sessão.

`proton_pin.py:948-959` e `steam_launch_options.py:792-810` fazem **a mesma
coisa**: abrir o `libraryfolders.vdf`, extrair as `path`, montar a lista de
`steamapps`. São duas implementações do mesmo parágrafo, com dois regexes de par
VDF e dois desescapadores (`_vdf_unescape` e `_desescapar_acf`, este último com
o comentário *"mesmo critério do proton_pin"* — a duplicação está até
**documentada**, sem ninguém ter unificado).

**E elas divergem no resultado.** Rodadas contra a máquina dela agora:

```
pastas_steamapps() devolve TRES pastas:
    /home/<usuaria>/.steam/steam/steamapps
    /home/<usuaria>/.steam/debian-installation/steamapps
    /mnt/Mnemosyne/SteamLibrary/steamapps

mas ~/.steam/steam -> ~/.steam/debian-installation   (symlink, criado 05/08 02:45)

logo: 43 manifests varridos, 22 appids UNICOS, 21 ocorrencias repetidas
```

A dedução de `pastas_steamapps` é `candidata not in pastas` (`:809`) — comparação
de `Path`, que **não resolve symlink**. A mesma pasta entra duas vezes.

**Por que ninguém percebeu:** `list_installed_appids` acumula num `set` (`:961`),
então a repetição colapsa sozinha; e `nome_do_appid` devolve no primeiro acerto
(`:816-827`), então a segunda pasta nunca é visitada. **Os dois consumidores
existentes são imunes por acidente da estrutura de dados, não por cuidado.**

> **A consequência direta para esta sprint, e é por isso que a E1 vem primeiro:**
> qualquer lista construída iterando `pastas_steamapps` — que é o caminho óbvio,
> porque é o módulo que sabe traduzir nome — **mostra cada jogo dela duas vezes**.
> Uma lista de escolha com tudo em dobro é pior que campo de texto: ela não sabe
> qual dos dois clicar.

E há a segunda divergência, de sentido oposto: **`steam_launch_options` não tem
filtro de ferramenta.** `rotulo_do_jogo` traduz qualquer appid. Uma lista feita
só com esse módulo ofereceria "Proton 9.0", "Steam Linux Runtime" e
"Steamworks Common Redistributables" como se fossem jogos dela.

**Números de hoje, na máquina dela:**

```
22 appids unicos  ->  9 ferramentas descartadas  ->  13 JOGOS
```

Treze jogos. É o tamanho real do problema, e é bem menor do que qualquer
estimativa que circulou.

**A classe é a mesma do commit `10f4818`** — *"cinco jeitos de perguntar 'isto é
um jogo?' viram um só"*, que desceu o predicado de `steam_app_` para
`profiles/steam_app.py`. Aqui são **dois** jeitos de perguntar *"onde estão as
bibliotecas da Steam?"*, e o mais novo é o que erra.

### F4 — Onde a lista encaixa na janela, sem mexer no caminho de gravação

**Grau: MEDIDO**, por leitura do glade e do mixin.

O campo onde ela digita o número hoje é o `GtkEntry id="profile_simple_custom_name"`
(`gui/main.glade:2062`), dentro do `profile_game_entry_box` (`:2049`). Quem o
revela é `_on_aplica_a_changed` (`app/actions/profiles_actions.py:989-1050`), que
troca placeholder e tooltip conforme a escolha (`_CAMPO_LIVRE_DICAS`, `:92-104`)
e, para `steam_game`, chama `_prefill_steam_appid` (`:1050`, definido em `:1125`).

> **Aviso de número de linha, e é o DIV-10 do estudo em ação.** Este documento
> foi escrito com dois agentes irmãos editando `src/` ao mesmo tempo, e **dois
> dos arquivos citados mudaram de tamanho durante a redação**: o
> `_on_aplica_a_changed` saiu de `:848` para `:989`, e o
> `profile_simple_custom_name` do glade saiu de `:2084` para `:2062`, tudo isso
> entre duas leituras minhas. Os números foram reconferidos ao fim, mas **a
> âncora estável é o nome do símbolo (ou o `id` do widget)**, não a linha.
> Confira por `grep -n` antes de usar qualquer número deste arquivo.

**O caminho de gravação não muda em nada, e isto é o coração da proposta:**

- `from_simple_choice` (`profiles/simple_match.py:74-107`) faz
  `normalize_appid(custom_name)` e grava
  `MatchCriteria(window_class=["steam_app_<id>"])`;
- `normalize_appid` (`:62-72`) já aceita **o número puro**, o
  `steam_app_1599660` e o número com espaços em volta.

Ou seja: se a lista devolver **o appid** para o mesmo `GtkEntry`, tudo a jusante
— gravação, detecção do round-trip (`detect_simple_preset`, `:111-159`), o
matcher — continua exatamente como está, sem uma linha de mudança e sem risco de
regressão no funil que a leva de 05/08 acabou de estabilizar.

**A forma sugerida:** um `GtkEntryCompletion` no `GtkEntry` que já existe, ou um
combo-com-entry no lugar dele, alimentado pela biblioteca. Ela digita "mullet" e
escolhe **Mullet Mad Jack**; o que vai para o campo é `2111190`.

### F5 — Onde a lista NÃO pode ir, e isto é medição, não gosto

**Grau: MEDIDO**, pelo próprio CSS da casa.

**Não** no `SegmentedSelector` do *"Aplica a"* (`app/widgets/segmented_selector.py`,
os sete itens em `profiles_actions.py:110-118`). O seletor já briga para caber: o
`gui/theme.css:918-930` registra a `UX-TRIGGERS-COMPACT-01`, que existe para
*"caber em 3 colunas sem engolir a aba"*, e o comentário do widget em `:216-235`
diz que a grade é de **3 colunas fixas** porque *"um GtkGrid não negocia"*.

Treze jogos em três colunas são cinco linhas de botões dentro de um editor de
perfil. E a lista **cresce** — no dia em que ela instalar mais jogos, a aba
inteira se desmancha. O seletor é para categorias de sete itens, não para
biblioteca.

### F6 — A promessa que hoje exige o jogo aberto

**Grau: MEDIDO.** `profiles/simple_match.py:34-37`:

```
MSG_STEAM_SEM_APPID = (
    "Diga o número do jogo na Steam (ex.: 1599660). Com o jogo aberto, o "
    "campo é preenchido sozinho."
)
```

A mesma promessa está no tooltip do campo (`profiles_actions.py:101-102`, dentro
do `_CAMPO_LIVRE_DICAS`) e o mecanismo por trás dela é o `_prefill_steam_appid`
(`:1125`), que lê o `window_detect_last_class` do daemon e só preenche campo
**vazio**.

O mecanismo é bom e a frase é honesta. Mas a leitura de baixo é dura: **para
criar o perfil do jogo sem digitar número, ela precisa abrir o jogo primeiro.**
Se o jogo não está aberto — e não está, porque ela está justamente configurando
o perfil **antes** de jogar — a única saída é ir à Steam procurar o número na URL
da loja.

**Este é o ganho principal da sprint:** com a biblioteca listada, ela deixa de
precisar abrir o jogo. O `_prefill_steam_appid` **continua** valendo (é atalho de
zero cliques quando o jogo está aberto); a lista é a saída para todo o resto do
tempo.

### F7 — A segunda metade do pedido não tem dono

**Grau: MEDIDO**, por `git grep`. Nada no produto cria perfis em lote.

- `profiles/loader.py:130-184`, `seed_default_presets`, copia **presets de
  fábrica ausentes** para a pasta dela, com marker `.seeded_presets` (`:156`) e
  `FileLock` (`:159`) — mas a fonte são assets fixos, não a biblioteca dela;
- `cli/cmd_profile.py:154-215`, `profile create`, cria **um** perfil por
  invocação;
- a aba Perfis cria **um** perfil por gesto.

**Nenhum caminho existe que olhe a biblioteca e produza perfis.** É a parte do
pedido dela que ainda não foi projetada, e a E4 é a proposta — com o risco
declarado.

---

## E1 — Uma varredura só (e a que fica é a que dedup)

**Grau do defeito: MEDIDO** (F3).

Duas implementações da mesma pergunta, e a mais nova mostra a mesma pasta duas
vezes na máquina dela **hoje**.

**A ordem segura, e ela importa:**

1. **Primeiro o defeito, sozinho:** `pastas_steamapps`
   (`steam_launch_options.py:792-811`) passa a deduplicar por caminho
   **resolvido** (`Path.resolve()`), não por igualdade de `Path`. Correção de uma
   linha, com teste, **antes** de qualquer unificação. Assim a cura entra num
   commit que dá para reverter sozinho.
2. **Depois a fusão.** Uma fonte só para *"onde estão as bibliotecas"* e para
   *"quais appids são jogos"*. O destino natural é
   `integrations/steam_launch_options.py`, e não `proton_pin.py`, por dois
   motivos: é lá que já mora a tradução para nome (`rotulo_do_jogo`), e é o
   módulo que a janela já importa sem puxar nada da lane do Proton. O
   `proton_pin.list_installed_appids` vira **fachada** que delega, como o
   `10f4818` fez com o predicado de `steam_app_`.
3. **O filtro de ferramenta vai junto.** `_TOOL_MANIFEST_RE` (`proton_pin.py:93`)
   é o que separa jogo de Proton, e é a única regra desse tipo no repositório.
   Ele **tem** de acompanhar a fusão — senão a lista da E2 oferece
   "Steam Linux Runtime" para ela escolher.

**Cuidado que o `10f4818` deixou por escrito e vale de novo:** o ciclo de import.
`proton_pin` **já importa de si mesmo** para o `steam_launch_options`
(`steam_launch_options.py:798` faz `from ...proton_pin import default_steam_root`
dentro da função, justamente para não fechar ciclo no topo do módulo). Inverter o
sentido da dependência precisa ser conferido com o mesmo cuidado — e a saída, se
o ciclo aparecer, é a mesma de lá: descer a fonte comum para um módulo mais
baixo, não empilhar import tardio.

**A mordida:** um teste que monte `tmp_path` com **duas** pastas de biblioteca
sendo uma symlink da outra, e afirme que a lista sai com cada jogo **uma vez
só**. Desfeita a resolução do symlink, o teste reprova com o jogo em dobro.
Segundo caso: um `appmanifest` de ferramenta (nome contendo "Proton") não aparece
na lista de jogos — é o caso que `test_proton_pin.py:614-630` já guarda para o
lado do Proton e que passa a valer para a fonte unificada.

**Veto:** não mudar o **contrato** de `list_installed_appids` nesta entrega. Ele
tem três chamadores vivos no pin de Proton (`:822`, `:1077`, `:1128`), e o botão
*"Travar Proton validado"* mexe em configuração da Steam dela. Fachada que
delega, mesma assinatura, mesmo retorno ordenado.

---

## E2 — A biblioteca dentro do campo do appid

**Grau do defeito: MEDIDO** (F4 e F6).

Hoje, para dizer *"este perfil é do Mullet Mad Jack"*, ela precisa saber que o
Mullet Mad Jack é o `2111190`.

**O que fazer:**

1. **A lista alimenta o `GtkEntry` que já existe** (`gui/main.glade:2062`),
   por `GtkEntryCompletion` ou combo-com-entry. Cada item mostra o que
   `rotulo_do_jogo` já sabe montar — **nome e appid juntos**, nunca só o nome.
   O appid na tela é o que permite a ela conferir na Steam e o que liga esta
   escolha aos outros dois cadastros do projeto.
2. **O que vai para o campo é o appid puro.** `normalize_appid`
   (`profiles/simple_match.py:62-72`) já o aceita, e assim **o caminho de
   gravação não muda em nada** — nem `from_simple_choice`, nem
   `detect_simple_preset`, nem o matcher.
3. **Digitar continua funcionando.** A lista é sugestão, não portão. Jogo
   desinstalado, jogo que não é da Steam, appid que ela leu num fórum: tudo
   continua entrando pelo teclado, como hoje. **Uma lista que recusa o que não
   está nela transformaria uma ajuda em cadeado.**
4. **A leitura de disco sai da thread do GTK.** O padrão pronto está no
   `_prefill_steam_appid` (`profiles_actions.py:1125`), que faz o trabalho em
   segundo plano e só volta à janela com a resposta —
   `PERF-GUI-PROFILE-LOAD-NONBLOCKING-01`, a mesma regra que já vale para
   `load_all_profiles()`. A varredura da biblioteca é `glob` mais leitura de até
   algumas dezenas de arquivos, e uma delas pode estar em disco montado
   (`/mnt/Mnemosyne/SteamLibrary`, na máquina dela) — travar a janela enquanto o
   disco acorda é exatamente o defeito que aquela sprint fechou.
5. **A frase de erro acompanha.** `MSG_STEAM_SEM_APPID`
   (`profiles/simple_match.py:34-37`) promete *"com o jogo aberto, o campo é
   preenchido sozinho"*. Quando a lista existir, a frase honesta passa a ser
   *"escolha da sua biblioteca ou digite o número"* — e a promessa antiga deixa
   de ser a única saída. **A frase nova é texto de interface: a palavra final é
   dela** ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)),
   e a foto tem de ser refeita depois.

**A mordida:** três testes.

- (a) com uma biblioteca de fixture com **dois** jogos e **uma** ferramenta, a
  lista oferecida traz dois itens e nenhum deles é a ferramenta;
- (b) escolher um item e salvar grava `window_class == ["steam_app_<id>"]` — o
  mesmo que digitar o número à mão produz hoje. **Arrancada a lista, o teste de
  digitar continua verde**, que é a prova de que o caminho de gravação não foi
  tocado;
- (c) Steam ausente (nenhuma `steamapps` no `HOME` da fixture) não derruba a aba:
  a lista sai vazia e o campo continua aceitando digitação. Arrancado o
  best-effort, reprova.

**Veto:** não fazer a lista **substituir** o campo por um combo fechado. E não
oferecê-la no `SegmentedSelector` do *"Aplica a"* (F5): treze jogos em três
colunas fixas desmancham a aba, e a lista cresce com o tempo.

---

## E3 — O que a lista permite dizer, e que hoje não dá

**Grau: MEDIDO** (F6). Entrega de texto, dependente da E2, barata.

Com a biblioteca listada, três coisas que hoje o produto não consegue afirmar
passam a ser verdade:

1. **"escolha o jogo"** em vez de **"digite o número"** — o pedido dela, em
   quatro palavras;
2. **o jogo não precisa estar aberto** — some a única condição que a frase atual
   impõe;
3. **jogo desinstalado continua tendo perfil.** O `rotulo_do_jogo`
   (`steam_launch_options.py:831-841`) já resolve isso do jeito certo: sem
   manifest, o appid cru é a resposta. Um perfil antigo de jogo que ela apagou
   **não** pode sumir da aba nem virar erro — a decisão dela sobre aquele jogo
   continua sendo dela.

---

## E4 — "um perfil específico pra cada jogo": a metade sem dono

**Grau do defeito: MEDIDO** (F7 — não existe caminho nenhum). **Grau do desenho
abaixo: proposta.**

Esta é a parte grande do pedido, e a que pode estragar coisa dela. **Ela não
fecha sem a palavra dela.**

### A honestidade primeiro, porque ela decide a forma

Ela tem **15 perfis** na pasta hoje (`ls` em 06/08) e **13 jogos** instalados.
Semear um perfil por jogo **dobraria** a lista dela de uma vez.

E é uma ação **pouco reversível**: desfazer significa apagar arquivos de perfil,
e apagar arquivo de perfil é exatamente o estrago que a leva de 05/08 passou a
semana inteira consertando. Some a isso que quatro perfis dela **já estão com a
regra corrompida** (está no índice da faixa) — jogar treze arquivos novos por
cima de uma pasta nesse estado é a pior hora possível.

**Por isso a proposta é a mais conservadora que resolve o pedido:**

### A forma proposta

1. **Ela escolhe quais.** A lista da E2 aparece com caixas de seleção e
   **nenhuma marcada**. Ela marca os jogos que quer, vê **quantos** perfis vão
   nascer e com que nomes **antes** de confirmar. Nada de "criar todos".
2. **Jogo que já tem perfil não é oferecido para criar.** O produto sabe
   descobrir isso sem adivinhar: um perfil de jogo da Steam tem
   `window_class == ["steam_app_<id>"]`, e o predicado que extrai o appid está
   unificado desde o `10f4818` em `profiles/steam_app.py`
   (`steam_appid_from_wm_class`, `:43`). O item aparece marcado como *"já tem
   perfil"*, e a ação oferecida é **abrir** o que existe, nunca criar por cima.
3. **Colisão de nome de arquivo é recusa, não sobrescrita.** O `slugify` faz
   `"Navegacao"` e `"Navegação"` caírem no mesmo `.json`, e a guarda já existe e
   já está escrita: `cli/cmd_profile.py:49-75`, `_guarda_slug`, que recusa gravar
   por cima de **outro** perfil e explica por quê. Qualquer semeadura em lote
   passa por ela — nome de jogo tem acento, dois pontos e travessão, e a colisão
   é questão de tempo.
4. **A prioridade de nascimento já tem regra medida, e não se reinventa aqui.**
   `profiles_actions.py:2071-2085`, `_prioridade_acima_dos_catch_all`, dá ao
   perfil novo de jogo `_FOLGA_ACIMA_DO_CATCH_ALL = 10` (`:86`) pontos acima do
   catch-all mais alto do disco, limitado por `PRIORIDADE_MAXIMA`. É a entrega 1
   da [PERFIL-NASCE-CERTO-01](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md).
   **Cuidado que a semeadura em lote acrescenta e o caso de um perfil não tinha:**
   treze perfis calculando a prioridade um de cada vez viram treze números
   diferentes, cada um dez acima do anterior. A prioridade tem de ser calculada
   **uma vez, para o lote**, e não por arquivo.
5. **Onde o código mora.** Duas moradas plausíveis, e a escolha é de quem
   implementar:
   - **`profiles/loader.py`**, ao lado de `seed_default_presets` (`:130-184`),
     que já tem o vocabulário certo: marker de semeadura (`:156`), `FileLock`
     para o daemon e a janela não semearem ao mesmo tempo (`:159`), e a regra de
     **nunca sobrescrever** o que existe;
   - **um subcomando `profile seed-steam`** em `cli/cmd_profile.py`, ao lado de
     `create`/`historico`/`restore`, que dá porta de linha de comando e um lugar
     natural para um `--dry-run` que imprime o que faria sem escrever nada.

   **A recomendação é fazer o `--dry-run` primeiro**, nos dois casos: uma
   listagem do que nasceria, sem tocar em disco, é a coisa mais barata de
   escrever e a única que dá para mostrar a ela antes de decidir.
6. **O que o perfil novo contém.** A proposta mais conservadora é o mínimo que o
   `profile create` já produz — gatilhos em `Off`, lightbar apagada — e **só** o
   `match` preenchido. Um perfil semeado que já chega com configuração é um
   perfil que **decide por ela**, e o pedido dela foi *"poder setar"*, não
   *"receber setado".*

### A mordida

- Semear com um jogo que **já tem** perfil não escreve nada e diz que já existe.
  Arrancada a checagem, o teste vê o perfil antigo sobrescrito e reprova.
- Semear dois jogos cujos nomes colidem no `slugify` recusa o segundo com a frase
  do `_guarda_slug`, e o primeiro fica intacto.
- O lote de N jogos produz N perfis com **a mesma** prioridade, e ela é maior que
  a do catch-all mais alto da fixture. Calculada por arquivo, o teste vê N
  prioridades diferentes e reprova.
- `--dry-run` não cria arquivo nenhum: a pasta de fixture sai com a mesma
  contagem de antes.

### O VETO

- **Nenhum agente roda a semeadura na pasta dela.** Nem para "testar", nem com
  `--dry-run` seguido de confirmação própria. A pasta de perfis dela tem quatro
  arquivos com a regra corrompida e é a matéria da leva de 05/08.
- **Nada sobrescreve perfil existente**, em hipótese nenhuma, nem com `--force`
  nesta entrega. Se a semeadura precisar de `--force` um dia, é outra sprint,
  com outra conversa.
- **Não semear perfil por jogo da allowlist de Steam Input.** São cadastros
  diferentes: a allowlist é intenção dela sobre a Steam, o perfil é configuração
  de controle. Cruzá-los reinventa o duplo registro do outro lado — o veto é o
  mesmo da E5 da
  [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md).
- **A tela desta entrega não fecha sem foto e sem a palavra dela**
  ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).
  Uma caixa que cria treze arquivos é o gesto mais pesado que a aba Perfis
  passaria a oferecer.

---

## ORDEM DE EXECUÇÃO

1. **E1, passo 1** — a dedup do symlink em `pastas_steamapps`. Uma linha, um
   teste, reversível sozinha. Vale mesmo que o resto desta sprint nunca aconteça.
2. **E1, passos 2 e 3** — a fusão das duas varreduras e o filtro de ferramenta
   junto. Independente da janela.
3. **E2** — a lista no campo do appid. Depende da E1 (sem ela, tudo em dobro).
4. **E3** — os textos. Depende da E2 e da palavra dela.
5. **E4** — a semeadura, **e só o `--dry-run` primeiro**. Depende da E2 (é a
   mesma lista) e **não fecha sem ela**.

Antes de fechar qualquer leva, o bloco do `CLAUDE.md`, **depois** do `git add -A`
(os portões são cegos a arquivo novo).

**Nada de emoji em documento nenhum** — o sanitizer do pre-commit bloqueia
U+2713/U+2717, e o `validar-glifos.py --all` **não** pega isso.

---

## O QUE ESTA SPRINT NÃO COBRE — e é decisão, não esquecimento

- **Jogos que não são da Steam.** Lutris, Heroic, GOG, binário solto: nada disso
  tem `appmanifest`, e a escolha por biblioteca não os alcança. O caminho deles
  continua sendo *"Jogo específico"* com o basename do executável — que é uma
  queixa própria, porque em jogo Proton esse basename costuma ser o binário do
  wine (está dito no tooltip, `profiles_actions.py:95-97`).
- **Qual configuração cada jogo merece.** A lista diz **que** jogos existem;
  qual máscara ou quais gatilhos servem a cada um é o M-17 do estudo e se resolve
  em jogo.
- **A troca automática de perfil.** O autoswitch já casa `steam_app_<id>`; esta
  sprint só facilita **escrever** o número certo lá.
- **Os quatro perfis corrompidos dela.** O conserto é dela, na janela, e está no
  índice da faixa. Um agente não edita perfil dela.

---

## O QUE NÃO FOI MEDIDO

- **Não vi a tela nesta sessão.** Tudo sobre a janela veio do `gui/main.glade`,
  do `gui/theme.css` e dos mixins de `app/actions/`.
- **Não medi quanto tempo a varredura leva** com a biblioteca em
  `/mnt/Mnemosyne/SteamLibrary` fria. É por isso que a E2 manda fazê-la em
  segundo plano por princípio, e não por número.
- **Não sei se `Path.resolve()` basta** para toda topologia de biblioteca da
  Steam — bind mount e caminho relativo no `libraryfolders.vdf` não foram
  testados. Na máquina dela, hoje, o caso é symlink e `resolve()` resolve.
- **Não abri nenhum jogo**, e portanto não confirmei que um perfil semeado entra
  quando o jogo abre. O caminho é o mesmo do perfil digitado à mão, que já é
  testado — mas isso é **SUSPEITA COM MECANISMO**, não medição.
- **Não perguntei a ela quantos perfis por jogo ela quer de verdade.** Treze é o
  número de jogos instalados, não o número de jogos que ela joga.
