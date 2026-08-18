# LARGURA-01 — a mesma largura em todas as abas

- **Status:** ABERTA — documento de medição e plano. Nada de código nesta rodada
- **Prioridade:** MÉDIA — é pedido de leitura sobre uma entrega que ela aprovou,
  não correção de defeito
- **Aberta em:** 29/07/2026, depois de ela olhar a aba Status entregue pela
  SOM-01, com a janela maximizada em 1920x1080
- **Sucede:** [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md), que criou
  o piso, o teto elástico e a `CaixaDeTetoElastico`
- **Relacionada:** [VÃO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md),
  que mediu o vazio **vertical** das mesmas nove abas e declarou, na abertura,
  que nada dela entrava na aba Status. Esta sprint faz o caminho contrário: pega
  o que a aba Status ganhou e pergunta, aba por aba, se serve nas outras
- **Também relacionada:**
  [LEGIBILIDADE-01](2026-07-25-LEGIBILIDADE-01-texto-legivel-alvo-clicavel.md)
  (a largura é a restrição dura desta janela) e
  [STATUS-SIMETRIA-02](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md)
  (distanciar não é organizar)
- **Rodada:** é um dos seis documentos de 29/07; a ordem de leitura está no
  [índice da documentação da v0.3.0](../estudos/2026-07-29-INDICE-a-documentacao-da-v030.md)

## A frase dela, literal

> *"aba de status semi perfeita, vale a sprint pra usarmos a largura igual nas
> demais abas"*

Duas coisas estão ditas aí, e as duas são pedido:

1. a aba Status ficou **quase** boa — "semi perfeita" não é aprovação completa;
2. o que ela ganhou deve valer para as outras oito.

Esta sprint responde às duas com medida, e a resposta da segunda **não é um
número só para todas** — a medição diz o contrário, e diz onde.

## O que já existe, conferido no código

| Peça | Onde | O que faz |
|---|---|---|
| `LARGURA_CARD_UNICO = 1040` | `app/widgets/controller_card.py:298` | PISO do card de um controle; repetido no `width-request` do frame Estado em `gui/main.glade:321` |
| `LARGURA_CARD_ELASTICA = 1400` | `app/widgets/controller_card.py:316` | TETO elástico |
| corte do teto no card | `app/widgets/controller_card.py:886-911` | `do_size_allocate` corta a alocação e devolve o excedente como margem, centrado |
| `CaixaDeTetoElastico` | `app/widgets/controller_card.py:1986-2015` | dá o mesmo corte a um widget vindo do glade |
| instalação da caixa | `app/app.py:839-871`, chamada em `:888` | hoje envolve **um único** widget: o `frame_status_estado` |
| teto por widget, dentro do card | `app/widgets/controller_card.py:337-339` | `LARGURA_BARRA_GATILHO_UNICO = 400`, `LARGURA_GYRO_UNICO = 420` — a outra metade da receita |

A aba Status é a única com esse tratamento. As outras oito recebem a largura
inteira e a repassam adiante.

## A bancada de medição

Janela montada numa `Gtk.OffscreenWindow` de 1920x1080, com o tema na escala de
fonte que de fato sai (`app/theme.py`), o conteúdo dinâmico de todas as nove
abas instalado pelos `install_*_tab` **reais** do `HefestoApp`, as páginas
envolvidas em rolagem como o `app/app.py:873-918` faz, o `frame_status_estado`
dentro da `CaixaDeTetoElastico` como o `app/app.py:888` faz, e um
`ControllerCard(compact=False)` no `status_players_slot` com todos os sensores
acesos. O laço principal roda de verdade por 2,5 s antes de medir, para os
refresh assíncronos das abas (estado do daemon, diagnóstico anti-storm)
chegarem — sem isso, metade dos rótulos ainda diz `Consultando...` e a medida é
de outra tela.

Receita e capturas em
`/tmp/claude-1000/-home-vitoriamaria-Desenvolvimento-hefesto-dualsense4unix/16d5a94d-66ea-4225-a04e-e1716b5ef847/scratchpad/largura01/`
(um PNG por aba, mais `medicao-1920.json`, `medicao-1180.json`,
`medicao-1426.json`, `experimento-teto.json` e `vao-coluna-1920.json`).

**Com a janela em 1920, cada página do notebook recebe 1894px** (1886 no Rumble
e 1898 nos Perfis — a diferença é a barra de rolagem vertical e o divisor de
colunas). O card fica em 1400 e o frame Estado também em 1400: os dois param no
mesmo número, como a SOM-01 prometeu.

### A armadilha de medição que me pegou primeiro

O primeiro medidor comparava a posição vertical de dois widgets para decidir se
eles estão "na mesma linha". **Isso não vale quando os dois vivem dentro de
`GtkScrolledWindow` diferentes**: cada rolador tem a própria `GdkWindow`, e a
alocação dos filhos é reportada em sistemas de coordenadas distintos. Há seis
roladores no glade (`gui/main.glade:422`, `:556`, `:694`, `:1515`, `:2148`,
`:2932`) mais um por página criado em `app/app.py:910`. Com isso, o medidor
emparelhou o `—` do frame Estado (aba Status) com o título do giroscópio, que
está 200px mais abaixo na tela.

Por isso **os vãos publicados abaixo são só os que também confiro na captura**.
Os números que não dependem de coordenada vertical — largura alocada contra
largura natural, largura de coluna, mínimo pedido — valem todos.

### A segunda armadilha: mínimo medido depois de alocar

O mínimo de largura de um `GtkLabel` com quebra **depende da largura que ele já
recebeu**: o GTK3 usa a alocação corrente como referência para não entrar em
laço de redimensionamento. Medida a mesma aba Sistema nas duas janelas: mínimo
de **1166px** com a janela em 1180 e de **1454px** com a janela em 1920, sem
nada ter mudado no conteúdo. O número honesto é o da janela pequena, e é o que
o `tests/unit/test_layout_orcamento_altura.py` já usa. Quem repetir esta medição
numa janela larga vai ver 1454 e concluir, errado, que a aba Sistema não cabe na
janela de projeto.

## As nove abas, medidas

### Quanto de conteúdo real e quanto de vão sobra

O "mínimo" é a largura abaixo da qual a aba começa a espremer, medida com a
janela no tamanho de projeto (1180px), que é como o
`tests/unit/test_layout_orcamento_altura.py:260` já mede.

| Aba | id no glade | colunas | recebe | mínimo | sobra sem dono |
|---|---|---:|---:|---:|---:|
| Início | `tab_home_box` (`gui/main.glade:197`) | 1 | 1894 | 483 | **1411 (74%)** |
| Status | `tab_status_box` | 1 | 1894 | 1064 | 830 (44%) — 494 já viram margem |
| Gatilhos | `tab_triggers_box` (`:461`) | 2 | 1894 | 936 | 958 (51%) |
| Lightbar | `tab_lightbar_box` (`:759`) | 2 | 1894 | 1126 | 768 (41%) |
| Rumble | `tab_rumble_box` (`:1201`) | 1 | 1886 | 684 | **1202 (64%)** |
| Perfis | `profiles_paned` (`:1481`) | 2 | 1898 | 906 | 992 (52%) |
| Sistema | `daemon_box` (`:1899`) | 1 | 1894 | 1166 | 728 (38%) |
| Emulação | `emulation_box` (`:2176`) | 1 + 2 cartões | 1894 | 958 | 936 (49%) |
| Navegação | `tab_navegacao_dsx` (`:2655`) | 2 | 1894 | 949 | 945 (50%) |

O mínimo **subestima** o que uma aba com texto corrido precisa: um rótulo com
quebra reporta mínimo de quase nada, então 483px de mínimo no Início não quer
dizer que a aba se leia bem em 483px. Serve para uma coisa só, e é a que
interessa aqui: mostrar que **nenhuma das nove precisa de 1894px**.

### Onde o vão aparece, aba por aba

Só o que também aparece na captura correspondente.

| Aba | O que foi medido |
|---|---|
| **Início** | 723px de nada entre o texto do botão `Xbox 360` e o do `DualSense (botões PlayStation)`. O botão `Xbox 360` recebe 807px para 70px de texto; os três de `O que o controle faz agora` recebem 604 a 620px cada para 105 a 160px de texto. O parágrafo mais largo mede 1872px de linha |
| **Status** | O teto funciona por fora (card 1400, frame 1400) e **não alcança o miolo do frame**: a coluna de valores do `status_grid` recebe 1242px e a maior tinta de valor tem 112px. A `status_battery_bar` (`gui/main.glade:370`) recebe 1242px para 150px de natural, com o `— %` desenhado no meio: 620px de barra vazia de cada lado do número |
| **Gatilhos** | Duas colunas de 941px. Dentro de cada uma: 379px entre `Aplicar em L2` e `Desligar` (378 do lado do R2). A grade dos 19 modos é de **3 colunas fixas** (`app/widgets/segmented_selector.py:33`, `column_homogeneous` + `hexpand` por botão), o que dá 285px por botão de cada lado |
| **Lightbar** | Colunas de 481 e 1401px. 229px entre os textos de `Desenho do P1` e `Desenho do P2` (quatro botões de 338px para ~113px de texto). Parágrafo de 1367px de linha. `lightbar_brightness_scale` (`gui/main.glade:931`) em 447px para 58px de natural |
| **Rumble** | O pior esticão da janela: `rumble_weak_scale` e `rumble_strong_scale` (`gui/main.glade:1339` e `:1358`) recebem **1731px cada** para 58px de natural. `rumble_policy_slider` (`:1281`) em 837px. A fileira `Economia / Balanceado / Máximo / Auto` é `homogeneous` (`:1221`) e dá 460px a cada botão: 416px de nada entre `Máximo` e `Auto`. Parágrafo de 1856px |
| **Perfis** | Colunas de 880 e 1002px. `profile_name_entry` (`gui/main.glade:1655`) em 907px para 168px de natural; `profile_priority_scale` (`:1672`) em 907px para 73px. Os botões de `Aplica a:` ficam com ~330px para ~70px de texto |
| **Sistema** | 298px entre `Atualizar` e `Ver detalhes` — a fileira de cinco botões dá ~380px a cada um para ~130px de texto. **O log é o oposto:** a linha mais longa tem 175 caracteres e a fonte monoespaçada mede 8px por caractere, então ela pede 1400px exatos, e é isso que o `daemon_status_text` reporta como natural |
| **Emulação** | 715px entre `054C:0DF2 (DualSense)` (cartão da esquerda) e `Próximo:` (cartão da direita) — os dois cartões estão na mesma faixa e ambos param antes da metade. Parágrafo de 1874px de linha. Os botões desta aba **já** têm tamanho natural, e é a única em que isso vale |
| **Navegação** | Colunas de 1037 e 841px. 812px entre o rótulo `Emular mouse+teclado` e o interruptor que ele nomeia. `mouse_speed_scale` e `mouse_scroll_speed_scale` (`gui/main.glade:2734` e `:2753`) em 813px cada para 38 e 48px de natural |

## A medição que decide a sprint

Repeti a montagem inteira com a janela em 1426px, que entrega exatamente 1400px
a cada página — ou seja, **a tela que ela veria se todas as abas ganhassem o
teto elástico do card**. Comparação dos vãos que confiro na captura:

| Aba (bloco medido) | vão hoje (1894) | com o teto (1400) | aceite de 200px |
|---|---:|---:|---|
| Início (fileira da máscara) | 723 | 475 | **ainda reprova** |
| Navegação (coluna esquerda) | 812 | 565 | **ainda reprova** |
| Emulação (entre os dois cartões) | 715 | 715 | **não muda** |
| Rumble (fileira de política) | 416 | 293 | **ainda reprova** |
| Gatilhos (por coluna) | 379 | 256 | **ainda reprova** |
| Sistema (fileira de botões) | 298 | 199 | passa, no limite |
| Lightbar (coluna direita) | 229 | 106 | passa |
| Perfis (coluna da lista) | 125 | 76 | já passava |
| Status | — | — | o teto já está posto, e o miolo do frame continua com 1242px de coluna para 112px de tinta |

**O teto elástico sozinho resolve três dos nove blocos medidos e deixa cinco
reprovando.** Onde ele atua, tira cerca de um terço do vão; onde o vão é interno
a um bloco que já para no tamanho natural — Emulação — ele não muda nada. Isso
não é surpresa: é literalmente o que a SOM-01 escreveu ao explicar por que o
teto do card veio acompanhado de glifos maiores, analógicos maiores e medidores
maiores — *"o que impede a volta dele não é o teto: é o CONTEÚDO crescer junto"*.

E o custo em altura do teto, medido com o mesmo laço:

| Aba | altura em 1894 | altura em 1400 | diferença |
|---|---:|---:|---:|
| Início, Status, Rumble, Perfis, Sistema, Navegação | — | — | **0** |
| Gatilhos | 506 | 522 | +16 |
| Emulação | 608 | 650 | +42 |
| Lightbar | 440 | 484 | +44 |

**A hipótese de que o teto quebraria o orçamento de altura fica REFUTADA**, e
por uma razão que vale escrever: no tamanho de projeto (1180px) o teto de 1400
**nem entra em ação**, e é nesse tamanho que o
`tests/unit/test_layout_orcamento_altura.py` cobra a altura. As alturas pedidas
a 1154px já são maiores que as duas colunas acima (Início 710, Gatilhos 554,
Lightbar 528, Emulação 670) — o pior caso continua sendo a janela pequena, como
sempre foi.

## Aba por aba: o teto serve? e o que serve onde ele não serve

### Serve, e é a entrega mais barata (duas abas)

- **Início** e **Rumble** são coluna única, 74% e 64% de sobra sem dono, e o teto
  custa **zero** de altura. São as duas que mais lucram e as que menos arriscam.
  Mas nas duas o teto **precisa vir com o corte por widget**, senão param em
  475px e 293px de vão.

### Serve, com o cuidado de manter a proporção (quatro abas)

- **Gatilhos**, **Lightbar**, **Perfis** e **Navegação** têm duas colunas. O teto
  aplicado à página inteira encolhe as duas juntas e preserva a proporção — foi
  o que a simulação em 1400 mediu, com custo de 0 a 44px de altura. O que ele
  **não** resolve em nenhuma delas é o widget que não merece a largura que
  recebe. Medido com a página em 1400px: as barras do Rumble ainda ficam com
  1237px cada, o campo de nome dos Perfis com 660px e a barra de bateria da aba
  Status com os mesmos 1242px de sempre, porque ela já está dentro do teto.
- Em **Gatilhos** há um segundo caminho, e ele usa a largura em vez de devolvê-la:
  a grade de modos é de 3 colunas fixas (`app/widgets/segmented_selector.py:33`).
  Numa coluna de 941px isso dá 285px por botão. Com 4 ou 5 colunas quando a
  largura permite, o mesmo espaço vira **menos linhas** e a aba encolhe em
  altura. Isso é decisão de desenho, não de medida, e por isso entra por último.

### NÃO serve como está (uma aba)

- **Sistema.** O log é a única coisa da janela que tem uso legítimo para 1894px:
  a linha mais longa mede 1400px exatos, o `daemon_log_scroll` tem
  `hscrollbar-policy: never` e o `daemon_status_text` tem `wrap-mode: word-char`
  (`gui/main.glade:2148-2162`). Um teto de 1400px na página inteira deixa ~1370px
  úteis ao log e **quebra a linha mais longa em duas**. O teto aqui vale para o
  cabeçalho, a fileira de cinco botões e o cartão de saúde; o bloco do log fica
  **de fora, por escrito**.

### O teto não é o problema nem a cura (duas abas)

- **Emulação** é a única aba cujos botões já têm tamanho natural, e o vão de
  715px é **entre os dois cartões de informação do topo**, que param onde o texto
  deles acaba. O teto não muda esse número (medido: 715 nos dois casos). O que
  serve é um `GtkSizeGroup` horizontal entre os dois cartões, ou empurrar o
  segundo para junto do primeiro. O outro defeito da aba é linha de 1874px de
  texto corrido, que é comprimento de leitura, não vão.
- **Status** já tem o teto e continua com o miolo solto. O que falta é o
  orçamento **dentro** do frame Estado: a coluna de valores e a barra de bateria.

## Entregas, na ordem em que devem entrar

A ordem é por risco crescente. Cada uma se desfaz sozinha se ela não gostar.

### E1. Teto por widget nos controles que não merecem largura

O precedente é da própria casa: `LARGURA_BARRA_GATILHO_UNICO = 400` e
`LARGURA_GYRO_UNICO = 420` (`app/widgets/controller_card.py:337-339`), que
curaram exatamente este defeito **dentro** do card. Aqui ele sai do card.

| Widget | Onde | Hoje | Natural | Teto proposto |
|---|---|---:|---:|---:|
| `rumble_weak_scale` | `gui/main.glade:1339` | 1731 | 58 | 400 |
| `rumble_strong_scale` | `gui/main.glade:1358` | 1731 | 58 | 400 |
| `rumble_policy_slider` | `gui/main.glade:1281` | 837 | 58 | 400 |
| `status_battery_bar` | `gui/main.glade:370` | 1242 | 150 | 300 |
| `profile_priority_scale` | `gui/main.glade:1672` | 907 | 73 | 400 |
| `profile_name_entry` | `gui/main.glade:1655` | 907 | 168 | 420 |
| `mouse_speed_scale` | `gui/main.glade:2734` | 813 | 38 | 400 |
| `mouse_scroll_speed_scale` | `gui/main.glade:2753` | 813 | 48 | 400 |
| `lightbar_brightness_scale` | `gui/main.glade:931` | 447 | 58 | 400 |

**Cuidado que já custou caro aqui:** teto no GTK3 **não** é `width-request` —
pedido de tamanho é MÍNIMO, e declarar um mínimo com `halign=center` trava o
widget no número exato. É a lição escrita em `app/widgets/controller_card.py:314`
e generalizada na seção 7.1 do
[mapa da sessão](../estudos/2026-07-29-mapa-da-sessao-e-o-que-os-agentes-mediram.md),
com os dois corolários que custaram medição: a alocação recebida não pode ser
mutada (o corte vai numa cópia), e widget vindo do glade não tem onde receber
esse código — por isso o teto dele vem de fora, na `CaixaDeTetoElastico`.
Para widget de glade, o caminho é `halign=start` mais um `width-request` que
funcione como largura desejada, ou a `CaixaDeTetoElastico` parametrizada.

**Aceite:** com a janela em 1920, nenhum `GtkScale`, `GtkProgressBar` ou
`GtkEntry` de nenhuma das nove abas recebe mais de 420px.

**Risco:** baixo. É local, não reflui layout e não muda altura (medido: os
widgets afetados estão todos em linha própria ou em linha com folga).

### E2. O miolo do frame Estado — a aba que ela chamou de "semi perfeita"

A coluna de valores do `status_grid` recebe 1242px para no máximo 112px de
tinta, e a barra de bateria pinta 1242px para dizer um número de dois dígitos.

**Aceite:** com a janela em 1920, a coluna de valores do `status_grid` não
recebe mais de 3x a maior tinta de valor (hoje 112px, então teto de ~340px), e o
`— %` da bateria fica a menos de 200px da borda da barra.

**Risco:** baixo, e é a entrega com maior retorno por linha: mexe na aba que ela
está olhando agora.

### E3. Comprimento de linha do texto corrido

Seis abas têm parágrafo com linha acima de 1000px, e quatro delas passam de
1850px — mais de 200 caracteres por linha. A ferramenta é `max-width-chars`, que
limita o **natural** e deixa o mínimo intacto — foi a mesma escolhida pela
[VÃO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md), entrega E2,
pelos rótulos da Emulação.

**Aceite:** nenhum parágrafo de nenhuma aba passa de 100 caracteres por linha
(cerca de 800px na escala de fonte que sai hoje).

**Risco:** baixo, mas com uma pegadinha declarada: `max-width-chars` num rótulo
que **não** tem `wrap` não faz nada. Conferir os dois atributos juntos, rótulo a
rótulo.

### E4. O teto elástico nas duas abas de coluna única

`Início` e `Rumble` ganham o mesmo par piso/teto do card (1040 / 1400), pela
mesma `CaixaDeTetoElastico` e pelo mesmo ponto de instalação
(`app/app.py:839-871`), generalizado para receber uma lista de páginas em vez de
um widget fixo.

**Aceite:** com a janela em 1920, o conteúdo das duas abas mede 1400px e fica
centrado; com a janela em 1180, mede 1154px (o teto não entra em ação) e nada
sai pela borda. Custo em altura medido: 0px nas duas.

**Risco:** médio-baixo. É o mesmo mecanismo já no ar na aba Status, aplicado a
mais duas páginas.

### E5. O teto elástico nas quatro abas de duas colunas

`Gatilhos`, `Lightbar`, `Perfis` e `Navegação`, mesmos números.

**Aceite:** as quatro medem 1400px de conteúdo centrado em 1920; a proporção
entre as colunas não muda (medida hoje: Gatilhos 941/941, Lightbar 481/1401,
Perfis 880/1002, Navegação 1037/841); a altura sobe no máximo 44px, e
`tests/unit/test_layout_orcamento_altura.py` continua verde.

**Risco:** médio. É a entrega que mais muda a foto, e é a que ela precisa
aprovar de olho antes de virar commit — regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).

### E6. Sistema, com o log de fora — por escrito

Teto para o cabeçalho, a fileira de cinco botões e o cartão `Saúde do sistema`.
O `daemon_log_scroll` (`gui/main.glade:2148`) **não** entra.

**Aceite:** com a janela em 1920, a fileira de botões mede no máximo 1400px e o
`daemon_status_text` continua recebendo pelo menos 1440px — margem sobre os
1400px que a linha mais longa pede.

**Risco:** médio. É a entrega em que a régua única quebraria alguma coisa, e por
isso ela é a única com aceite que pede o **contrário** do teto.

### E7. Emulação: os dois cartões do topo com a mesma largura

`GtkSizeGroup` horizontal entre os dois cartões de informação, para o vão de
715px virar duas colunas iguais. Não é teto.

**Aceite:** os dois cartões medem o mesmo, e o vão entre a última tinta do
cartão da esquerda e a primeira do da direita cai abaixo de 200px.

**Risco:** médio. Mexe em estrutura, não em número.

### E8. Gatilhos: usar a largura em vez de devolvê-la

`_WRAP_COLUNAS` (`app/widgets/segmented_selector.py:33`) deixa de ser 3 fixo e
passa a depender da largura recebida, com 3 como piso.

**Aceite:** com a janela em 1920 a grade dos 19 modos usa 4 ou 5 colunas e a aba
Gatilhos encolhe em altura; com a janela em 1180 ela continua com 3 colunas e
`tests/unit/test_layout_orcamento_altura.py` continua verde.

**Risco:** o mais alto da lista, e por dois motivos escritos. O primeiro: o
comentário em `app/widgets/segmented_selector.py:168-179` conta que ali houve um
`GtkFlowBox` que decidia colunas pela largura recebida, reportava a altura de 19
botões empilhados (606px) e virava o piso de altura de **todas** as nove páginas.
Reintroduzir decisão-por-largura é chegar perto do mesmo buraco. O segundo: a
aba Gatilhos foi o alvo do commit `b39fec9`, rejeitado, e a
[VÃO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md) já declarou que
ela não pega carona em leva nenhuma — entra sozinha, com foto antes e depois.

**E há um terceiro motivo, que nasceu na mesma rodada:** a
[GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md)
mediu, caractere a caractere nesta mesma grade, que o limite prático de rótulo é
**22 caracteres no piso de 1040px com três colunas** — e a lista de sinônimos
que ela propõe foi construída contra esse número. Se a E8 entrar antes e mudar o
piso de 3 colunas, a lista de nomes precisa ser remedida. A ordem segura é a
troca de rótulos primeiro (custo de geometria zero, medido) e a E8 depois.

### E9. Gatilhos: os botões de ação no rodapé da coluna

Pedido dela, olhando a aba Gatilhos maximizada em 29/07 às 03h00:

> "aqui não seria melhor abaixar os botões tipo o Aplicar e Desligar pra ficar no
> rodapé das colunas deles?"

**O que eu medi na captura** (1920x1080, janela maximizada, L2 em "Arma
semi-automática" e R2 em "Pulso"): os botões "Aplicar em L2" e "Desligar" ficam
em y≈714, logo abaixo do último parâmetro. O frame da coluna vai até y≈955.
Sobram **cerca de 240px de vazio abaixo dos botões, dentro da própria coluna** —
e não é o vão da aba, é vão de dentro do bloco.

Na coluna da direita fica pior, e o motivo é informativo: o modo "Pulso" não tem
parâmetro nenhum, então entre a descrição (y≈554) e os botões (y≈714) já há um
vazio, e **depois** dos botões vêm os mesmos 240px. Duas colunas com quantidades
diferentes de parâmetro produzem botões em alturas diferentes — hoje isso não
acontece por sorte (os dois blocos de ação começam na mesma altura), mas
acontecerá assim que um lado tiver mais parâmetros que o outro.

**Entrega:** os botões de ação de cada gatilho ancorados no RODAPÉ da coluna a
que pertencem (`valign=END` no filho, ou `pack_end` no container da coluna), de
modo que cada coluna passe a ter cabeça (a grade de modos), meio (a descrição e
os parâmetros) e pé (as ações). O vazio deixa de sobrar embaixo dos botões e vai
para o meio, onde ele lê como respiro e não como defeito.

**Aceite:** com qualquer par de modos selecionado nas duas colunas — inclusive um
com três parâmetros e outro com nenhum — os dois pares de botões ficam na MESMA
altura, e a distância do botão até a borda inferior da coluna é o espaçamento
padrão da faixa, não mais que isso.

**Risco:** baixo, e menor que o da E8. Isto não mexe em quantas colunas a grade
tem nem no piso de altura da página: move a âncora vertical de dois blocos de
botão dentro de um container que já existe. Não depende da E8 e pode entrar
antes dela. Mas vale a mesma regra da VÃO-01: a aba Gatilhos entra sozinha, com
foto antes e depois.

## O risco que a SOM-01 pagou, e que esta paga de novo

A SOM-01 escreveu, e vale copiar: **teto rígido demais devolve o vazio como
buraco DENTRO da faixa.** Quem impede isso não é o teto, é o conteúdo crescer
junto e a sobra se repartir entre os blocos. Quem cobra é o teste de vão máximo,
`tests/unit/test_status_faixa_blocos.py:251`, com `VAO_MAXIMO_ENTRE_BLOCOS = 200`
(`:59`) medido na tela dela, `LARGURA_DA_TELA_DELA = 1870` (`:53`).

Duas provas de que o risco é real, e não teórico:

1. **A simulação em 1400** acima: o teto sozinho leva o Início de 723 para 475px
   de vão, e o Navegação de 812 para 565. Vão que sobra depois do teto é vão que
   virou buraco no meio de um bloco mais estreito.
2. **A aba Status, hoje, já entregue.** O teto está posto nos dois blocos e o
   miolo do frame Estado continua com 1242px de coluna para 112px de tinta. É o
   defeito exatamente onde a cura já foi aplicada — e é por isso que a E2 vem
   antes de qualquer teto novo.

## O teste que cada aba precisaria

O modelo é o `test_nenhum_vao_de_mais_de_200px_entre_os_blocos_da_faixa`. Ele
funciona porque percorre uma lista **nomeada** de blocos de uma faixa só. Copiar
isso para uma aba inteira exige duas adaptações, e ambas vêm da armadilha do
começo deste documento.

**Regra dura para todos os testes abaixo:** nunca comparar dois widgets que
estejam em `GtkScrolledWindow` diferentes. O `y` deles vive em espaços de
coordenada distintos, e a comparação passa a medir ficção. A lista de roladores
está em `gui/main.glade:422`, `:556`, `:694`, `:1515`, `:2148`, `:2932`, mais um
por página em `app/app.py:910`.

| Aba | Teste que ela precisaria | Mordida (a cura arrancada que tem de reprovar) |
|---|---|---|
| **Todas, um teste só** | nenhum `GtkScale`/`GtkProgressBar`/`GtkEntry` recebe mais de 420px com a janela em 1870 | tirar o teto de um deles: o Rumble volta a 1731px |
| **Início** | vão máximo de 200px entre as tintas da fileira de máscara e da fileira de modo | tirar o teto da página: volta a 723px |
| **Status** | a coluna de valores do `status_grid` não passa de 3x a maior tinta; o texto da barra de bateria fica a menos de 200px da borda | tirar o teto da coluna: volta a 1242px, e o teste de faixa do card continua verde — provando que ele **não** cobre o frame |
| **Gatilhos** | vão máximo **por coluna**, com as duas colunas medidas em separado | comparar as duas colunas juntas: o número salta para 824px e o teste vira ruído |
| **Lightbar** | vão máximo na coluna direita; e a coluna esquerda não passa de 500px | dar `hexpand` à coluna esquerda: ela come a direita |
| **Rumble** | vão máximo de 200px na fileira de política; largura das duas barras | devolver `homogeneous=True` sem teto: volta a 416px |
| **Perfis** | vão máximo na coluna do editor; largura do campo de nome e da escala | tirar o teto do campo: volta a 907px |
| **Sistema** | **o contrário de um teto**: o `daemon_status_text` recebe pelo menos 1440px com a janela em 1870 | pôr o teto de 1400 na página: a linha de 175 caracteres quebra em duas |
| **Emulação** | os dois cartões do topo medem o mesmo, e o vão entre eles fica abaixo de 200px | tirar o `GtkSizeGroup`: volta a 715px |
| **Navegação** | vão máximo entre o rótulo do interruptor e o interruptor; largura das duas barras | tirar o teto do cabeçalho: volta a 812px |

E um teste de linha de texto, comum às sete abas com parágrafo: nenhum rótulo
com `wrap` recebe mais de 800px. Mordida: tirar o `max-width-chars` de um deles
faz a Emulação voltar a 1874px.

**Todos medem o widget MONTADO e ALOCADO numa `Gtk.OffscreenWindow`** — widget
sem alocação devolve 1x1 em tudo, e um teste de geometria sobre ele passa com
qualquer layout. É a mesma nota que a SOM-01 deixou.

## Como você valida na tela

1. Janela **maximizada**. Passe pelas nove abas com Ctrl+PageDown e olhe a borda
   direita: hoje sete delas terminam a 1894px e nenhuma tem conteúdo lá.
2. Aba **Rumble**: as duas barras de vibração vão de ponta a ponta da janela
   para dizer um número de 0 a 100. É o mesmo defeito que você apontou nas
   barras de L2/R2 dentro do card, fora dele.
3. Aba **Status**: a barra de bateria vai de `Bateria:` até a borda do quadro,
   com o `— %` boiando no meio.
4. Aba **Início**: o botão `Xbox 360` tem 807px para duas palavras.
5. Aba **Sistema**: role o log até uma linha longa. Ela cabe numa linha só hoje
   — é isso que a E6 protege.
6. Encolha a janela até o tamanho de projeto: nada pode mudar, porque o teto só
   entra em ação acima de 1400px.

## O que fica de fora desta sprint, e por quê

- **Uma régua única para as nove abas.** A medição não sustenta: o log da aba
  Sistema pede 1400px para a linha mais longa, e um teto de 1400px na página
  inteira deixa ~1370px úteis. A régua é a mesma em oito abas e tem exceção
  escrita na nona.
- **Mexer no número 1400.** Ele foi medido para o card na SOM-01 e está travado
  por teste. Se alguma entrega daqui pedir outro número, ele vira uma constante
  nova com nome próprio, e não uma edição da constante do card.
- **Tokens de espaço em CSS.** É a entrega E5 da
  [VÃO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md), a única que
  não se desfaz apagando uma linha, e continua depois de tudo.
- **A barra de abas e o rodapé.** Ficam fora do notebook e têm orçamento próprio,
  já medido pela LEGIBILIDADE-01.
- **Os 12px entre as duas alocações da aba Status.** Medido: o card começa em
  x=247 e o frame Estado em x=259, os dois com 1400px. Na captura as bordas
  desenhadas coincidem, então é margem do slot e não desalinhamento visível —
  fica registrado para o caso de aparecer com outra escala de fonte.
- **Validação na tela dela.** Todas as medidas deste documento são de
  `Gtk.OffscreenWindow` renderizada em PNG e conferida com o olho. O aceite é o
  dela.
