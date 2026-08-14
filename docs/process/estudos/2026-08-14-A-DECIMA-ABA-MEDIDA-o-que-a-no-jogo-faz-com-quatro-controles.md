# A décima aba, medida — o que a "No jogo" faz com quatro controles

- **Escrito em:** 14/08/2026, na branch `restauro/inicio-da-sessao`. A medição
  começou sobre `d85a088` (06:03) e o texto fechou às 07:05, quando o `HEAD` já
  era `48e7fd5` (06:38) — **três commits à frente**. Dois são de documentação e
  o terceiro (`c1ed06a`, `feat(tela)`) **gerou a foto desta aba com os quatro
  controles**, que este texto só passou a usar na 3ª rodada; os três estão
  citados onde tocam. O que anda depressa (endereço de linha, contagem de
  testes) foi trocado por símbolo e por critério
- **É a entrega E1 da** [MESA-CHEIA-07](../sprints/2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md)
  (item **1.1** do [índice da mesa cheia](../sprints/2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md))
- **Status:** **MEDIÇÃO** — nenhuma linha de código de produto foi alterada por
  este documento
- **A lacuna que ele fecha:** dez agentes mediram a janela aba por aba em
  13/08 e nenhum mediu esta, porque a lista entregue a eles tinha nove nomes.
  Era lacuna declarada, não achado — e o
  [censo das dez abas](2026-08-13-o-censo-das-dez-abas-o-que-a-janela-faz-com-quatro-controles.md)
  registrou a dívida no mesmo dia em que a descobriu.

---

## 0. A régua, declarada antes de qualquer número

Esta casa já perdeu um dia inteiro para um instrumento que mediu contra a
biblioteca errada, e a regra que sobrou é declarar a régua antes do número.

| o que | como |
|---|---|
| os formatadores | os **de produção**, importados do `src/` pelo `.venv/bin/python` — `painel_no_jogo.linhas_do_controle`, `titulo_do_painel`, `recado_do_controle`, `recado_global`, `texto_do_contexto`, `aviso_do_perfil`, `jogo_steam_aberto`, e o `controller_card.accent_do_card` para comparar |
| o payload | `tests/fixtures/state_full_quatro_controles.json` — os **quatro controles reais** de 14/08 (dois USB, dois BT, quatro cores, co-op com quatro jogadores), medidos em [A MESA CHEIA, MEDIDA](2026-08-14-A-MESA-CHEIA-MEDIDA-o-que-quatro-controles-revelaram.md) |
| quais chaves a aba lê | instrumentado: um `dict` que registra toda leitura, passado no lugar do `entry` e do `state_full`. Não é grep — é o que o código **executou** |
| as fotos | duas, ambas 1920x1080 e geradas pelo caminho da casa, **decodificadas pixel a pixel** (`zlib` + desfiltragem à mão, sem PIL) para a geometria não depender de olhômetro: `assets/mesa-cheia/mesa_cheia_no_jogo.png` — **esta aba com os quatro controles**, e é dela que sai a geometria vertical — e `docs/usage/assets/readme_no_jogo.png` (dois controles), que serve de contraprova |
| o único experimento | uma sonda temporária no `painel_no_jogo.py` para aferir um portão (§9.2), inserida e retirada — o arquivo voltou limpo |
| a auto-mordida | uma régua executável que mede tudo isto de novo e **exige que este texto diga o mesmo**: **76** afirmações numéricas, incluindo os algarismos *derivados* (alturas, vãos, passos, onde o quarto painel termina, a cor dos rótulos) e uma regra estrutural que reprova o retorno de endereço absoluto de linha. Cada régua nasceu cega onde a anterior errou: a da 2ª rodada conferia três grandezas do PNG e passava verde com "778 px" trocado por "99999 px"; a da 3ª pegava o 99999, mas tomava a moldura por **uma** borda só e batia contra uma frase que descrevia **outra** — passava verde com a descrição errada. Esta mede as **quatro bordas em separado** e cobra do texto qual delas cada algarismo usa |
| o que NÃO foi feito | nenhuma janela real, nenhum daemon reiniciado, nenhum clique. A aba não foi aberta na tela dela. **Nenhuma linha de produto ficou alterada** |

**Confirmado, não derrubado:** `painel_no_jogo.py` tem **667 linhas** e
`grep -cE 'lightbar|accent|swatch|player_slot'` devolve **0** — a contagem de
13/08 continua valendo em `d85a088`. `grep -c uniq` no mesmo arquivo também
devolve **0**, o que o índice ainda não tinha medido.

**Corrigido em 14/08/2026, depois de três rodadas de conferência cética.** Na
primeira, três ceticismos independentes refizeram esta medição com régua própria:
o miolo passou inteiro e **cinco números não reproduziram**. Na segunda, uma
quarta cética releu a correção e derrubou **mais dois** — um deles *introduzido
pela própria correção*. Na terceira, a geometria vertical inteira saiu de cena:
descobriu-se que a foto **com os quatro controles já existia**, e o parágrafo
extrapolava da foto de dois; e uma segunda passada da mesma rodada, remedindo a
foto do zero, derrubou **mais três** — dois deles *introduzidos pela correção
anterior*, e pelo mesmo motivo de sempre: um algarismo certo debaixo de uma
descrição que era de outra régua. O terceiro (`~780 px`, no §10) era o `778`
arredondado, que tinha sobrevivido dez seções abaixo de onde foi corrigido; e um
endereço absoluto de linha ainda vivo (`daemon/connection.py`, no §2) virou
símbolo, pela regra que o próprio §9.1 tinha escrito e que ninguém aplicara ali.
Todos os números foram **substituídos** pelo que a régua acima devolve,
remedidos do zero a cada rodada e não copiados de quem apontou, e não guardados
ao lado do certo: é a regra da casa para fato errado, e um número errado num
resumo custa mais que a linha que ele ocupa.

| onde | dizia | mede |
|---|---|---|
| §6, o giroscópio parado | os corpos "colapsam em **dois**" | **três** — e três já era a contagem antes, então não há colapso |
| §1, linha 5 | "em **três** outros a única célula que difere" | **dois** pares, e a diferença é de estado inteiro, não de algarismo |
| §6, o Hz que pisca | "**três** dos quatro painéis" distinguidos pelo algarismo | **dois** painéis exibem Hz, e o algarismo não é a única diferença de nenhum par |
| §6, a foto na horizontal | "~1200 px vazios **à direita**" | **960 px** até a borda direita da imagem, dos quais **959 de fundo puro** — 1220 é `1920 - 700`, que cobra à direita a margem de 260 px que está à esquerda |
| §9.1, a distância | "**oito** linhas acima" | **dez** — e o endereço absoluto virou símbolo, porque o arquivo anda |
| §6, a foto na vertical (2ª rodada) | "a moldura mede **170 px**, mais 30 de vão; quatro pedem **778 px**, terminando em `y=958`" | **764 px**, de `y=102` a `y=865` — e agora **medidos na foto dos quatro**, não projetados a partir da de dois |
| §9.2, a contagem de suítes (2ª rodada) | "as **seis** suítes que tocam esta aba: **108 passed**" | número volátil: andou de **129** para **130** entre dois comandos meus. Apagado e trocado pelo critério, que não anda |
| §6, a moldura e o rótulo (3ª rodada) | "a **moldura pura** (só a borda do `Gtk.Frame`, sem o rótulo) mede **168, 166, 164 e 164 px**, e o **rótulo** ocupa os **12 px** logo acima da borda de cima" | os dois algarismos existem, mas **descrevem outra coisa**: 168 é a **borda da esquerda**, que começa 7 px abaixo da de cima; da borda de cima até a de baixo são **175, 173, 171 e 171 px**. O rótulo mede **14 px** e **atravessa** a borda de cima em vez de ficar acima dela; os 12 px eram a distância até o começo da borda da esquerda |
| §6, o vazio à direita e a sobra embaixo (3ª rodada) | "**960 px** (`x=960..1919`)" e "sobram **214 px** até os 1080" | certos como distância até a borda da imagem, **enganosos como vazio**: a última coluna e a última linha são a borda de 1 px da janela. Fundo puro: **959** colunas e **213** linhas. As duas contas ficam escritas, com a régua de cada uma |
| §10, a medida que diz que cabem (3ª rodada) | "a medida de **~780 px** diz que cabem" | **764 px** — arredondamento do `778` derrubado no §6, que tinha sobrevivido dez seções abaixo. A régua desta passada cobra o §10 também |

A nota fica (em vez de a correção entrar calada) por causa de **quatro** coisas:

1. a receita descartada do §6 — *"envelhecendo o `visto_ha_s`"* — é convidativa e
   **inerte**, e quem quiser reconferir a repetiria. O §6 explica por quê;
2. os **778 px** não eram um algarismo trocado: eram **três réguas misturadas
   dentro de uma frase só**. A frase declarava a *moldura pura* (170 px + 30 de
   vão), imprimia coordenadas de moldura, e então somava com a *tinta* do segundo
   painel (178 px) — `3 x 200 + 178 = 778`. Sob a régua que ela mesma declarava, a
   conta dava 770; e "a moldura mede 170 px" era desmentido pela segunda
   coordenada que a própria frase imprimia (`y=392..557` são 166 px). Lição:
   **escolha a régua antes do número**, e diga qual escolheu;
3. e a lição maior, que só apareceu na 3ª rodada: **duas revisões inteiras
   discutiram a aritmética de uma extrapolação sem que ninguém perguntasse se
   havia foto dos quatro**. Havia — commitada 36 minutos antes de o texto fechar,
   pela leva ao lado, e sem nenhum documento apontando para ela. Nenhuma régua
   pega esse erro: a régua confere o número contra a fonte declarada, e a fonte
   declarada é que estava errada. Antes de extrapolar, **procure o dado real** —
   nesta casa ele costuma existir e estar órfão;
4. e a lição que se repetiu **três vezes seguidas**, sempre na frase que a
   correção anterior tinha acabado de escrever: **o erro não estava no algarismo,
   estava na descrição**. O 778 era tinta chamada de moldura; o 168 é a borda da
   esquerda chamada de "a borda, sem o rótulo"; o 960 é distância até a borda da
   imagem chamada de vazio. Nos três casos a conta reproduz — o que não reproduz
   é a **frase**. Uma régua que confere só o número passa verde em todos eles;
   por isso a desta passada mede as quatro bordas em separado e cobra do texto
   **qual** delas cada algarismo usa.

---

## 1. A resposta curta

A "No jogo" **é** a cópia inacabada do molde da Status, e a medição de hoje
aperta o diagnóstico: ela não é uma aba sem cor — ela é uma aba que **recebe** a
cor de quatro controles distintos no mesmo payload e a **joga fora antes de
desenhar**. Os quatro `lightbar_rgb` chegam intactos ao `atualizar`; nenhum é
lido.

```
   o que CHEGA ao painel                 o que ELE lê
   ─────────────────────────             ────────────────
   transport   player   player_slot  →   transport, player, player_slot
   is_primary                        →   is_primary
   lightbar_rgb                      ×
   lightbar_source                   ×
   lightbar_on                       ×
   uniq                              ×
   index                             ×   (só se faltar player_slot)
   battery_pct  inputs  audio        ×
   vpad_backend  vpad_motivo         ×
```

E as seis respostas pedidas, em uma linha cada:

| # | pergunta | resposta medida |
|---|---|---|
| 1 | frases no singular com quatro na mesa | **quatro** — três delas globais, uma repetida por painel |
| 2 | por controle x do primário | **um painel por controle**; quatro linhas de moldura são globais, e **nada** é do primário — mas o casamento com o vpad tem um guarda que só o primário atravessa |
| 3 | o que descarta do payload | `lightbar_rgb`, `lightbar_source`, `lightbar_on`, `uniq`, `battery_pct`, `inputs`, `vpad_backend`; e no global, o bloco **`coop` inteiro** e o `steam_input` |
| 4 | a fita "Ajustes vão para:" | **mentira** nesta aba — zero leituras do alvo em toda a superfície da aba |
| 5 | quatro painéis iguais? | **sim**: dos seis pares, **um é idêntico letra por letra**, e em **dois** outros a única célula que difere é a do `giroscópio` — e ali ela difere por **estado inteiro** ("no jogo agora (~184 Hz)" contra "sem pedido ainda"), não por um algarismo |
| 6 | custo de terminar a cópia (2.3) | **10 símbolos, 2 arquivos, ~45 linhas** — e **zero** em `status_actions.py` |

---

## 2. As frases no singular — quatro, e cada uma com um preço diferente

Todas medidas em `app/widgets/painel_no_jogo.py`, no símbolo indicado.

### 2.1 `TEXTO_DESKTOP` — singular e SEM sujeito

> "**O controle** está movendo o mouse e o teclado. Enquanto estiver assim, o
> Hefesto não entrega controle nenhum ao jogo — troque para "Jogar pelo
> Hefesto" na aba Início."

Ela sai por `recado_global`, que **substitui os quatro painéis por uma frase
só** (`status_actions._sync_paineis_no_jogo`: com `recado` não-nulo,
`conectados` vira lista vazia e nenhum painel é pintado).

O singular não é errado no mecanismo — o daemon tem **um** `_mouse_device`
(`daemon/connection.py`, `grep -n _mouse_device`; o endereço absoluto saiu daqui
pelo mesmo motivo do §9.1: este arquivo também anda hoje). Mas com quatro na
mesa a frase não diz **qual dos
quatro** está com o mouse, e é a única tela em que ela poderia dizer: os quatro
painéis, que teriam onde escrever isso, acabaram de ser substituídos por ela.

### 2.2 `TEXTO_NATIVO` — singular e no meio de quatro DualSense

> "Não há controle virtual nenhum neste modo: o jogo abre **o controle físico**
> e fala direto com ele. Movimento, toque, vibração e som saem **do próprio
> DualSense** […]"

Mesmo mecanismo da anterior (também vem por `recado_global`). Aqui o singular é
mais defensável: o modo vale para a mesa inteira. E o docstring de
`recado_global` já registra, medido em 10/08, **por que** ela é global — com
dois controles na mesa a frase saía duas vezes, palavra por palavra. Com quatro
sairia quatro vezes. A decisão de içá-la para o topo está certa e sobrevive à
mesa cheia.

### 2.3 `TEXTO_SEM_VPAD` — singular correto, e é o que se repete

> "O jogo ainda não vê **este controle**. Se você acabou de conectá-lo, ele
> entra sozinho em alguns segundos; se demorar, use "Reconciliar jogadores" na
> aba Início."

Esta é fato de **um** controle (`recado_do_controle`), e o singular está certo.
O problema não é o número gramatical — é a **multiplicação**. Medido, forçando o
casamento com o vpad a falhar nos três secundários:

```
Controle 4 — USB · Jogador 1  ->  (painel normal, seis linhas)
Controle 1 — USB · Jogador 1  ->  "O jogo ainda não vê este controle. […]"
Controle 3 — BT  · Jogador 1  ->  "O jogo ainda não vê este controle. […]"
Controle 2 — BT  · Jogador 1  ->  "O jogo ainda não vê este controle. […]"
```

**Três vezes a mesma frase de 157 caracteres, e o mesmo conselho três vezes.** É
exatamente o defeito que o `recado_global` foi criado para curar em 10/08 — e
que continua vivo no terceiro caso, o único que ficou de fora daquela cura.

> **Ressalva de honestidade:** o cenário acima foi *forçado* (co-op desligado e
> `is_primary` só no primeiro). Não confirmei que ele seja alcançável pela
> interface hoje — o co-op é sempre ligado por decisão dela. O caminho que **é**
> alcançável e produz o mesmo efeito está no próprio payload: o campo
> `coop.derrubado_por_steam_input`, que a aba **não lê** (ver §4).

### 2.4 `texto_do_contexto` — "**o** controle", com quatro vpads na mesa

Com o fixture real, o cabeçalho da aba diz:

> "Jogar pelo Hefesto · O jogo vê **o controle** como: DualSense (botões
> PlayStation)"

Hoje isso é verdade e é global: a máscara sai de `gamepad_emulation.flavor`, que
é um campo só (`mode_transition.mode_of_state` e `_FLAVOR_ITEMS`). **Mas a
decisão D-5 já foi tomada** — *"a máscara do gamepad é do JOGADOR, com o jogo
como padrão"*
([as onze respostas da mesa cheia](../2026-08-14-DECISOES-DE-PO-as-onze-respostas-da-mesa-cheia.md)).
No dia em que a D-5 entrar, esta linha vira **falsa**, e ela é o cabeçalho da
aba que responde justamente *"o que o jogo está vendo"*. É a dívida que a D-5
cria aqui, e ela não está anotada em lugar nenhum. Fica anotada.

---

## 3. O que é por controle, e o que é da moldura

Medido: a aba tem **duas camadas**, e a fronteira é limpa.

| peça | escopo | símbolo |
|---|---|---|
| a existência da aba na tira | global | `jogo_steam_aberto` + `status_actions._sync_visibilidade_no_jogo` |
| a linha de contexto (modo + máscara) | global | `texto_do_contexto` |
| o recado que substitui tudo (Nativo / Controlar o PC) | global | `recado_global` |
| o aviso do perfil que não entrou | global | `aviso_do_perfil` |
| "Nenhum controle conectado." | global | `status_actions._no_jogo_vazio` |
| **o título do painel** | **por controle** | `titulo_do_painel` -> `controller_card.titulo_do_card` |
| **as seis linhas de recurso** | **por controle** | `linhas_do_controle` -> `controller_card.estado_do_recurso` |
| **o recado sem vpad** | **por controle** | `recado_do_controle` |

**Nada é "do primário" na tela.** Mas há um lugar onde o primário decide sozinho,
e ele fica escondido dois níveis abaixo: `controller_card._item_do_vpad` recusa
o casamento quando `player == 1` e `is_primary` é falso. Com o co-op ligado (o
caso da mesa cheia) todo mundo tem um `player` próprio e o guarda nunca dispara;
sem co-op, os quatro chegam como jogador 1 e **só o primário casa** — que é o
cenário do §2.3.

### E há uma peça global que é da JANELA, não da aba

A fita **"Ajustes vão para:"** mora no `header_bar`
(`gui/main.glade:136`, montada em `status_actions._init_controller_target_combo`)
e está **acima** do notebook: ela não sai da tela ao entrar aqui.

---

## 4. O que a aba descarta — e a chave que dói

Instrumentado com um `dict` espião. Com o payload real dos quatro:

**Do `entry` de cada controle — LÊ quatro chaves:**
`transport`, `player`, `player_slot`, `is_primary`.

**Do `entry` — DESCARTA onze:**
`lightbar_rgb`, `lightbar_source`, `lightbar_on`, `uniq`, `index`,
`battery_pct`, `inputs`, `audio`, `connected`, `vpad_backend`, `vpad_motivo`.

**Do `state_full` — LÊ cinco:**
`gamepad_emulation`, `native_mode`, `rumble_ff`, `jogo_steam`,
`perfil_do_jogo_que_nao_entrou`.

**Do `state_full` — DESCARTA o resto, e dois deles importam:**

- **`coop`** — o bloco inteiro. `enabled`, `players`, `externals`,
  `secundarios_derrubados` e, sobretudo, **`derrubado_por_steam_input`**. A aba
  que existe para responder *"o que está chegando ao jogo"* não lê o campo que
  diz *"o Steam Input derrubou o co-op"* — e é essa a causa mais provável de os
  três painéis secundários caírem todos no `TEXTO_SEM_VPAD` do §2.3, com um
  conselho ("Reconciliar jogadores") que não é o que resolve.
- **`steam_input`** — idem, e a casa já registrou que
  [o Steam Input faz um espelho Xbox de cada controle que ele vê](2026-08-13-o-projeto-inteiro-num-mapa-so.md).

**A cor está no primeiro grupo, e é a resposta literal da pergunta 3 da faixa:**
`lightbar_rgb` chega, com quatro valores distintos, e não é lida. `accent`
também não — mas `accent` não é chave de payload: é derivado
(`controller_card.accent_do_card`), e a aba não o chama. `player_slot` **é**
lido, mas só por dentro de `titulo_do_card`. `uniq` não é lido pelo painel; ele
existe no caminho, mas em `status_actions._status_card_keys_for`, e só como
metade da chave `(index, uniq)` que decide **quando reconstruir** os painéis.

> Comparação justa com a Status, para não repetir um erro do plano: o card da
> Status **também não mostra o MAC na tela**. Ele o **carrega** dentro do widget
> (`ControllerCard._uniq`) porque ele **age** — o `mic.set`, o `speaker.set` e a
> ponte BT vão só naquele controle. O painel da "No jogo" não age, e por isso não
> precisa carregar o MAC. **A ausência do `uniq` aqui não é dívida.** A do
> `lightbar_rgb` é.

---

## 5. A fita "Ajustes vão para:" nesta aba: **mentira**

Confirmado por leitura, e não por citação: `_edit_target_uniq` é um campo de
`status_actions.py`, e **todas** as suas leituras moram dentro do próprio
mecanismo do alvo — o editor avançado, a gravação do override, a montagem do
rótulo da fita. **Nenhuma delas está no caminho da aba "No jogo"**, e
`painel_no_jogo.py` não contém a palavra `uniq` uma única vez em 667 linhas.

A fita também **não sabe** que a aba mudou: `_set_target_strip_visible` tem três
chamadores, e os três decidem por contagem de controles ou por daemon desligado.
Não há um `if` de aba no caminho.

> **Os números de linha saíram daqui em 14/08, de propósito** (a mesma correção
> do §9.1). A versão anterior citava `status_actions.py:427`, `:1773`, `:1812`,
> `:1930`, `:1942-1944`, `:1961`, `:1673`, `:2094`, `:2177` e `:2505`. Horas
> depois, no mesmo dia, **nove** desses dez endereços já estavam deslocados — o
> arquivo é editado por várias frentes ao mesmo tempo. Endereço absoluto neste
> arquivo apodrece em **minutos**; o símbolo, não. Quem quiser conferir:
> `grep -n _edit_target_uniq` e `grep -n _set_target_strip_visible`.

**Isto confirma a linha "No jogo" da tabela da
[MESA-CHEIA-10](../sprints/2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md),
que a tinha marcado como falsa sem que ninguém tivesse medido a aba.** E a cura
já está decidida: pela **D-2**, a fita **se requalifica** aqui em vez de sumir.

---

## 6. Quatro painéis iguais? Sim — provado com o payload real

Rodando `linhas_do_controle` sobre os quatro controles do fixture, e comparando
os corpos par a par:

```
painel 0 x painel 1 : 2 células de 6 diferem
painel 0 x painel 2 : 2 células de 6 diferem
painel 0 x painel 3 : 2 células de 6 diferem
painel 1 x painel 2 : 1 célula  de 6 difere
painel 1 x painel 3 : 1 célula  de 6 difere
painel 2 x painel 3 : 0 células — IDÊNTICOS, letra por letra
```

E **qual** célula difere importa mais que quantas:

| par | a única diferença |
|---|---|
| 1 x 2 e 1 x 3 | `giroscópio`: "no jogo agora (~184 Hz)" contra "sem pedido ainda" |
| 0 x demais | `giroscópio` (o Hz) e `som do controle` ("parou" x "sem pedido ainda") |

O `~163 Hz` e o `~184 Hz` são números que o tique de 2 Hz reescreve **duas vezes
por segundo** — e só **dois** dos quatro painéis chegam a exibir um deles (os dois
no cabo; os dois no Bluetooth dizem "sem pedido ainda", com `motion_hz` 0,0 e
`motion_forwards` 0). Medido: o algarismo **não é a única diferença de nenhum dos
seis pares**. No único par em que dois números de Hz se encaram — 0 x 1 — a linha
`som do controle` também difere; e o que separa o painel 1 dos painéis 2 e 3 é o
estado inteiro do giroscópio, não o dígito. O número que pisca é ruído em cima da
igualdade, e não o que a sustenta.

Das **24 linhas** na tela (quatro painéis x seis recursos), **17 dizem a mesma
frase**: *"sem pedido ainda"*. Cinco dizem *"parou"*. Duas dizem *"no jogo
agora"*.

E quando o giroscópio para — o instante em que ela larga o controle, ou o menu do
jogo abre — os corpos **continuam sendo três**: não há colapso, porque três já era
a contagem antes. Medido, zerando o `motion_streaming` dos quatro vpads: os
painéis 0 e 1 trocam o Hz por *"parou"*, os pares com uma só célula diferente
sobem de **dois para três** (0 x 1 entra na conta), o número que piscava some da
tela — e a contagem de textos distintos não se mexe.

**Dois** só sai zerando também o `motion_forwards`, e isso é outro cenário: esse
contador é **cumulativo**, e zerá-lo diz *"o giroscópio nunca fluiu"*, não *"o
giroscópio parou"* (`controller_card.estado_do_recurso`, o ramo do `giroscopio`
— é ele quem separa as duas situações, e é dele a decisão desde a
ORFAOS-QUE-VOLTAM-01). Envelhecer o `visto_ha_s` não muda nada aqui, e **não
podia**: esse bloco não é consultado no ramo do giroscópio, e neste payload os
quatro carimbos já chegam entre 143,5 s e 9608,3 s — todos muito acima dos 3,0 s
do `ATIVIDADE_FRESCA_S`. Rodar a receita inteira devolve o mesmo que rodar só a
primeira metade.

### O que a foto acrescenta, e que o texto não mostrava

Lendo as duas fotos, ambas 1920x1080 e decodificadas pixel a pixel:

- os **títulos dos quatro painéis saem no mesmo `#BD93F9`** — o lilás do rótulo
  de `Gtk.Frame` do tema —, contado pixel a pixel nos quatro rótulos da foto da
  mesa cheia, e no mesmo payload em que chegam **quatro cores diferentes**
  (`#FF0080`, `#0000FF`, `#00FF00`, `#FF0000`). Não é só que falta cor **por
  jogador**: existe uma cor na tela, e ela é **igual para todos**, o que empurra
  ativamente na direção errada;
- na horizontal a aba usa **700 px de 1920** (`LARGURA_PAINEL` + `halign=START`):
  a moldura vai de `x=260` a `x=959`, e à direita dela sobram **960 colunas** até
  a borda direita da imagem (`x=960..1919`) — das quais **959 são fundo puro**
  (`x=960..1918`) e a última é a **borda de 1 px da própria janela**, que a foto
  também captura. Os dois algarismos ficam escritos porque medem coisas
  diferentes, e a régua de cada um está dita. O que **não** é medida nenhuma é
  1220: essa é a conta `1920 - 700`, que cobra à direita a margem de 260 px que
  está à **esquerda**. Uma coluna só. **Não é proposta** — é a medida, e o
  desenho é decisão dela.

### A vertical, medida na foto que já existia com os quatro

**Este trecho extrapolava, e não precisava.** As duas versões anteriores mediram
a foto de **dois** controles e projetaram a de quatro; existe, desde o commit
`c1ed06a` (06:29, 36 minutos antes de este texto fechar),
[`assets/mesa-cheia/mesa_cheia_no_jogo.png`](assets/mesa-cheia/mesa_cheia_no_jogo.png)
— **esta mesma aba, com os quatro controles**, gerada pelo caminho da casa a
partir do payload real. Nenhum documento a citava. Os números abaixo saem dela,
decodificada pixel a pixel.

A contabilidade é a da **TINTA** — tudo que um painel pinta, o rótulo lilás
incluído —, porque é a tinta que decide se a coisa cabe:

| painel | tinta | altura | passo até o próximo |
|---|---|---|---|
| Controle 4 — USB · Jogador 1 | `y=102..281` | **180 px** | 198 px |
| Controle 1 — USB · Jogador 2 | `y=300..477` | **178 px** | 196 px |
| Controle 3 — BT · Jogador 3 | `y=496..671` | **176 px** | 194 px |
| Controle 2 — BT · Jogador 4 | `y=690..865` | **176 px** | — |

- **os quatro ocupam 764 px**, de `y=102` a `y=865`, e abaixo deles sobram
  **214 linhas** até a borda de baixo da imagem (`y=866..1079`) — **213 de fundo
  puro** mais a borda de 1 px da janela, a mesma de que a conta horizontal fala.
  **Os quatro cabem, medidos** — não projetados. A página ainda tem rolagem
  (`_wrap_notebook_pages_in_scroll`), então o pior caso continua sendo rolar;
- **os painéis não têm a mesma altura, e o passo cai**: 198, 196, 194. O vão
  limpo entre a tinta de um e a do seguinte é que é constante — **18 px** nos
  três —, e o passo é `altura do painel de cima + 18`. **Por que a altura varia
  eu não medi**; o que medi é que ela varia com o conteúdo, e que a variação é
  pequena (4 px do primeiro ao último);
- a outra régua da mesma pilha, a da **moldura**, é onde a versão anterior deste
  parágrafo escorregou de novo, e o motivo é que **a moldura do `Gtk.Frame` não é
  um retângulo fechado**: o rótulo abre um vão na borda de cima e empurra o
  começo da borda da esquerda para baixo. Medido, borda por borda:
  - a **borda de cima** é o segmento horizontal **à direita do rótulo**, em
    `y=107`, `y=305`, `y=501` e `y=695` — cinco px abaixo do topo da tinta —,
    indo de onde o rótulo acaba (`x=482` nos dois primeiros, `x=473` nos dois
    últimos, porque `USB` é mais largo que `BT`) até `x=959`;
  - a **borda da esquerda** (coluna `x=260`) só começa em `y=114`, `y=312`,
    `y=508` e `y=702` — **sete px mais abaixo** que a de cima. A **borda da
    direita** (coluna `x=959`) acompanha a de cima, e a de baixo fecha em
    `y=281`, `y=477`, `y=671` e `y=865`, que é o fim da tinta;
  - daí **duas alturas para a mesma moldura**, e é preciso dizer qual: da **borda
    de cima** até a de baixo dá **175, 173, 171 e 171 px**; da **borda da
    esquerda** até a de baixo dá **168, 166, 164 e 164 px**. A versão anterior
    imprimia a segunda e a chamava de *"só a borda do `Gtk.Frame`, sem o
    rótulo"* — que é a descrição da **primeira**;
  - o **rótulo lilás** mede **14 px** de tinta nos quatro (`y=102..115`,
    `y=300..313`, `y=496..509`, `y=690..703`), e **não fica acima da borda de
    cima: ele a atravessa** — `y=107` cai dentro do rótulo do primeiro painel.
    Os **12 px** que a versão anterior chamava de altura do rótulo eram a
    distância do topo da tinta até o começo da borda da **esquerda**, que é
    outra coisa;
- a foto de dois controles (`readme_no_jogo.png`) dá as mesmas molduras de 700 px
  (`x=260..959`) e o mesmo vão limpo de 18 px, e o miolo dela começa mais baixo —
  em `y=180`, porque acima há o aviso de três linhas do perfil que não entrou, que
  é **mais largo que os painéis** e leva a tinta da aba até `x=1091`. **Mesmo
  assim cabem:** os 764 px começando em `y=180` terminariam em `y=943`.

### A ORDEM dos painéis, que já tinha sido vista na foto meia hora antes

**Não é achado desta medição, e a versão anterior deste trecho dizia que era.** A
ordem `4 · 1 · 3 · 2` já estava publicada em
[A MESA CHEIA, MEDIDA](2026-08-14-A-MESA-CHEIA-MEDIDA-o-que-quatro-controles-revelaram.md)
(commit `48e7fd5`, 06:38, 27 minutos antes deste texto fechar), vista nos cards
da Status e do Início. O que **esta** aba acrescenta é o lugar: é a única tela em
que o número do controle e o número do jogador aparecem lado a lado na mesma
linha, um ao lado do outro, quatro vezes.

Os painéis são empilhados na ordem de inserção de `state_full.controllers`
(`status_actions._connected_controllers`, que só filtra por `connected`, sem
ordenar). Com o payload real de hoje, a tela sai assim, de cima para baixo:

```
   Controle 4 — USB · Jogador 1
   Controle 1 — USB · Jogador 2
   Controle 3 — BT  · Jogador 3
   Controle 2 — BT  · Jogador 4
```

**Nem a coluna do "Controle" nem nada mais sobe em ordem.** Os jogadores sobem
1-2-3-4; os controles descem 4-1-3-2. É herdado da aba Status (a mesma lista, a
mesma função) e não é defeito **desta** aba.

---

## 7. A pergunta que só a mesa cheia permite: a divergência aparece aqui?

**Aparece — e esta é, com a Status, a única tela do produto em que os dois
números da divergência estão impressos na MESMA linha.**

O endereço exato: `painel_no_jogo.titulo_do_painel`, que devolve
`controller_card.titulo_do_card(entry)` sem tocar em nada — e o
`titulo_do_card` monta `Controle {player_slot} — {transport} · Jogador {player}`.

> **Todo endereço em `controller_card.py` neste documento é por SÍMBOLO, nunca
> por linha:** o arquivo está sendo editado por outra sessão enquanto isto é
> escrito (cresceu de 4818 para 5024 linhas durante a medição). Número de linha
> ali nasce podre.

Rodado sobre o fixture real:

| controle | cor viva | `player_slot` | `player` | o que a aba escreve |
|---|---|---|---|---|
| rosa | (255, 0, 128) | 4 | 1 | **"Controle 4 — USB · Jogador 1"** |
| azul | (0, 0, 255) | 1 | 2 | **"Controle 1 — USB · Jogador 2"** |
| verde | (0, 255, 0) | 3 | 3 | "Controle 3 — BT · Jogador 3" |
| vermelho | (255, 0, 0) | 2 | 4 | "Controle 2 — BT · Jogador 4" |

E não é só cálculo: as quatro linhas estão **impressas** em
[`assets/mesa-cheia/mesa_cheia_no_jogo.png`](assets/mesa-cheia/mesa_cheia_no_jogo.png),
nessa ordem, nos quatro rótulos lilases.

É a mesma divergência que a mesa cheia mediu hoje, e ela bate: o rosa é
*"Controle 4 — P1"* e o azul é *"Controle 1 — P2"*.

**Isto tem uma consequência prática para a D-12**, que é a pergunta que voltou
para ela: *qual dos dois números a marca colorida carrega?* Esta aba já
**publica os dois**, um ao lado do outro, quatro vezes. Se a marca da D-1 entrar
aqui pelo `player_slot`, a linha lida assim:

```
   ■(rosa) Controle 4 — USB · Jogador 1
```

— cor e primeiro número concordam, e o segundo número diverge, na mesma linha,
sem nenhuma explicação a três centímetros de distância. **A "No jogo" é a tela
onde a resposta da D-12 fica visível mais depressa**, e é por isso que ela é
boa candidata a ir junto com a decisão em vez de antes dela.

---

## 8. O que custa terminar a cópia (entrega 2.3), em símbolos

Contado abrindo cada símbolo, não estimado.

### O que MUDA — 10 símbolos, 2 arquivos, ~45 linhas

**Em `app/widgets/controller_card.py` (4 símbolos):**

| símbolo | o que | tamanho |
|---|---|---|
| `desenhar_swatch` | **novo**, de módulo. Hoje o desenho vive em `ControllerCard._on_draw_swatch`, um método **aninhado dentro do `if _GTK_DISPONIVEL`** — inalcançável de fora. Extrair é mover ~18 linhas | 18 movidas |
| `ControllerCard._on_draw_swatch` | passa a delegar | 3 |
| `cor_crua_do_card` | **novo**, uma linha: `return _rgb3(entry.get("lightbar_rgb"))`. É o dono único que a mordida da identidade exige — hoje `_rgb3` é privado e o swatch o chama inline dentro de `_update_lightbar`. **O padrão já existe e é de hoje:** outra sessão acabou de acrescentar `uniq_do_entry` a este mesmo módulo (visto na árvore de trabalho, ainda não commitado) pela mesma razão — um acessor público em vez de um `entry.get` repetido | 1 |
| `__all__` | +2 nomes | 2 |

**Em `app/widgets/painel_no_jogo.py` (6 símbolos):**

| símbolo | o que | tamanho |
|---|---|---|
| `cor_do_painel` | **novo**, irmã de `titulo_do_painel`, uma linha, delega em `cor_crua_do_card` | 1 |
| `PainelNoJogo.__init__` | o cabeçalho do frame vira **widget**: `Gtk.Box` com um `Gtk.DrawingArea` de 14x14 + `Gtk.Label`, via `set_label_widget`. Espelho de `ControllerCard._montar_ui`. +3 atributos | ~12 |
| `PainelNoJogo._on_draw_swatch` | **novo**, delega no desenhador partilhado | 3 |
| `PainelNoJogo.atualizar` | a `assinatura` ganha a cor, e `self.set_label(titulo)` vira `self._titulo_label.set_text(titulo)` | 4 |
| `PainelNoJogo` (stub sem GTK) | `self.cor` no `__init__` e no `atualizar` — espelho do `self.accent` do stub `ControllerCard` (o do ramo `else`, sem GTK). **Sem isto o teste não roda no CI**, que é sem PyGObject | 2 |
| `__all__` | +2 nomes | 2 |

### O que NÃO muda — e é isto que barateia a entrega

- **`status_actions.py`: zero linhas.** `install_no_jogo_tab`,
  `_sync_paineis_no_jogo` e `_rebuild_paineis_no_jogo` já entregam ao painel o
  `entry` inteiro **e** o `state_full` inteiro. A cor já está lá dentro.
- **`gui/main.glade`: zero linhas.** A `tab_no_jogo_box` é uma caixa vazia
  (`:678-682`); tudo é montado em código.
- **Zero timers.** O painel pega carona no tique de 2 Hz que já existe.
- **Zero vocabulário novo.** A D-1 pede *"sempre cor E número"*, e **o número já
  está lá** desde o primeiro dia, dentro do título reusado. A "No jogo" é a aba
  que já cumpre metade da D-1 — o que é, exatamente, a razão de ela ser a mais
  barata das coloridas.

### As duas armadilhas, ditas antes de alguém cair nelas

**1. O diff engole a cor.** `PainelNoJogo.atualizar` começa com

```
assinatura = (titulo, recado, tuple(linhas))
if assinatura == self._ultimo:
    return
```

A cor **não está** na assinatura. Um controle que muda só de cor — que é o gesto
inteiro da aba Lightbar — nunca repintaria, e o sintoma seria a **ausência** de
mudança, não um erro. É a família de defeito mais cara desta casa.

**2. `set_label` apaga o `set_label_widget`.** Depois que o cabeçalho virar
widget, a chamada `self.set_label(titulo)` que hoje mora no `atualizar`
**substitui o widget inteiro por um rótulo de texto** — e o swatch some. Não
some no boot: some na primeira vez que o título mudar, ou seja, quando o co-op
renumerar. Um defeito que só aparece com a mesa cheia e nunca com um controle
só.

---

## 9. Três correções ao plano da MESA-CHEIA-07

A E1 existia para poder mudar a E2. Mudou.

### 9.1 A mordida 2 (`strict=True`) **não pode morder**

O plano manda arrancar o `strict=True` do `zip(keys, conectados, strict=True)`
(`status_actions._sync_paineis_no_jogo`; era a linha 831 quando este documento foi
escrito, e o arquivo já andou desde então — por isso o endereço aqui é o símbolo)
e diz que *"o dublê tem três chaves e quatro controles conectados"*. **Esse dublê
não é construível pelo caminho público:** **dez** linhas acima, dentro do mesmo
método, `keys = self._status_card_keys_for(conectados)` — as chaves são
**derivadas** da mesma lista, uma por elemento. `len(keys) == len(conectados)`
por construção, sempre. Só um `monkeypatch` do `_status_card_keys_for` produziria
o desencontro, e um teste desses prova coisa sobre o `monkeypatch`, não sobre o
produto.

### 9.2 A mordida 3 (o timer novo) **não tem portão que a sustente**

**Quem viu primeiro foi o
[mapa de colisão](2026-08-14-O-MAPA-DE-COLISAO-o-que-dez-frentes-mediram-antes-de-a-leva-comecar.md),
§3.1** (commit `ae0f88a`, 06:19 — 46 minutos antes deste texto fechar), e ele já
dizia a frase inteira: *"Um `GLib.timeout_add` posto em `PainelNoJogo` hoje passa
em 100% da suíte"*. Ele chegou lá **lendo** o portão; o que esta seção acrescenta
é ter **plantado a sonda** e visto o verde com os próprios olhos. Fica aqui,
apesar de repetido, porque é a única das três correções ao plano que muda o que a
E2 tem de escrever — mas o crédito é de lá.

O docstring de `PainelNoJogo` promete: *"O gate de timers da `status_actions`
conta as ocorrências de `GLib.timeout_add` no fonte — este widget não acrescenta
nenhuma, de propósito."* O portão é
`tests/unit/test_status_cards.py::test_gate_timers_nenhuma_ocorrencia_nova_vs_baseline`,
e ele lê **dois** arquivos: `status_actions.py` e `controller_card.py`.
**`painel_no_jogo.py` não está lá**, e nenhum outro teste do repositório conta
timers nesse arquivo.

**Isto não foi lido — foi provado.** Enfiei um poller cego no construtor do
painel, na linha seguinte ao `self._montar_linhas()`:

```python
GLib.timeout_add(500, lambda: True)   # SONDA TEMPORÁRIA
```

Um `timeout_add` que devolve `True` para sempre, dentro do widget que nasce
**uma vez por controle** — quatro cópias com a mesa cheia. É a forma exata do
defeito que custou 104% de um núcleo a esta casa. O resultado:

```
$ .venv/bin/python -m pytest -q \
    tests/unit/test_status_cards.py::test_gate_timers_nenhuma_ocorrencia_nova_vs_baseline
.                                                                        [100%]
1 passed in 0.29s
```

E as suítes da aba também não mordem, o que é o ponto: **nenhum arquivo de teste
deste repositório conta timers em `painel_no_jogo.py`**. Quem conta timers em
fonte é um só — `tests/unit/test_status_cards.py`, via `re.findall` —, e ele lê
dois arquivos, nenhum deles o painel. **Esse é o critério, e é o que fica aqui.**

Este parágrafo dizia, de manhã, *"as seis suítes que tocam esta aba, com a sonda
dentro: 108 passed"*. O número saiu, e o motivo é o mesmo do §9.1: **ele anda
mais rápido do que o texto**. Enquanto eu remedia, à tarde, a contagem das
suítes que importam o módulo passou de **129** para **130** entre dois comandos
meus, porque outro agente estava acrescentando teste no mesmo minuto. Contagem
de testes não é medida a se gravar em documento; o critério é. A sonda foi
retirada e o arquivo está limpo (`git status` sem saída para ele).

**A cura é de uma linha** — somar `src_painel` ao portão existente — e ela vale
por si, fora da 2.3: hoje o arquivo tem uma promessa escrita e nenhuma trava.

### 9.3 A mordida 1 é a boa, e fica **mais forte** com um endereço a mais

A asserção de identidade (a cor do painel tem de ser byte a byte a do card para
o mesmo `entry`) é a única das três que morde — e o §8 mostra por quê: hoje **não
existe** um símbolo público que devolva a cor crua. Quem escrever a 2.3 sem criar
o `cor_crua_do_card` vai reescrever `_rgb3(entry.get("lightbar_rgb"))` no painel,
que é literalmente o segundo dono que a mordida existe para reprovar.

---

## 10. O que este documento NÃO prova

- **Que a aba aparece.** Com o payload real de 14/08, `jogo_steam.appid` é
  `null` com `lido: true`, e portanto `jogo_steam_aberto` devolve **`False`**: a
  aba **não está na tira**. Todas as medições acima foram feitas chamando os
  formatadores diretamente, como o `retratar_abas.py` já faz (ele devolve `None`
  para o `main_notebook` justamente para escapar dos dois portões). **A mesa
  cheia foi medida sem jogo aberto** — e é jogando que esta aba existe.
- **Que quatro painéis coloridos se leem de relance.** Isso é a bancada dela,
  com o jogo aberto. A medida de **764 px** diz que **cabem**; não diz que
  funcionam. (Dizia "~780 px" — arredondamento do `778` que a 3ª rodada
  derrubou, e que sobrevivera aqui.)
- **Que o cenário do §2.3 é alcançável pela interface.** Ver a ressalva lá.
- **Que a cor do swatch bate com a barra na mão dela.** É a mesma ressalva que a
  MESA-CHEIA-07 já fazia, e continua sendo dela.

---

## 11. O que muda no índice da leva

- **O item 1.1 está feito.** Os 60 min foram gastos; este documento é a entrega.
- **A estimativa de 45 min do item 2.3 se sustenta** — 10 símbolos, ~45 linhas,
  metade delas movimento — **desde que** o `cor_crua_do_card` e o
  `desenhar_swatch` sejam extraídos primeiro. Sem eles a entrega parece de 20
  min e nasce com dois donos da cor.
- **Duas das três mordidas da 2.3 precisam ser reescritas** (§9.1 e §9.2), e uma
  delas (§9.2) virou **item próprio**, independente da cor: o portão de timers
  não cobre `painel_no_jogo.py`.
- **A D-5, quando entrar, quebra o cabeçalho desta aba** (§2.4). Não trava nada
  hoje; fica anotado para não ser redescoberto.
- **A dívida do `coop` descartado** (§4) não é da 2.3 e não estava em nenhuma
  sprint. É o campo `derrubado_por_steam_input` chegando à aba que responde pelo
  jogo e não sendo lido.
