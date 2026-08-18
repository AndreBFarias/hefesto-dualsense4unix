# CARD-ÚNICO-01 — o Estado entra no card, e o L3 vira marca d'água

- **Status:** ENTREGUE em 01/08/2026 (noite). As três entregas estão na tela e
  a suíte foi de 6645 para 6664 verdes. Ver "O que foi entregue", no fim
- **Status anterior:** PROPOSTA, pronta para executar. Escrita em 01/08/2026 **para
  sobreviver à queda da sessão**: ela pediu, literal, *"primeiro eu quero que
  você planeje e materialize as sprints pra caso mesmo que nossa sessão caia,
  depois você vai saber o que fazer e somente executar ela sem precisar do
  mesmo tanto de contexto que você tem agora"*. Tudo o que é preciso para
  executar está NESTE arquivo
- **Prioridade:** MÉDIA — é acabamento visual, sem risco funcional, na aba que
  ela mais olha
- **Aberta em:** 01/08/2026, por ela, com print anotado da aba Status
- **Sucede:** [ALINHA-DUAS-LINHAS-01](2026-08-01-ALINHA-DUAS-LINHAS-01-a-aba-status-que-ela-chamou-de-feia.md),
  que alinhou as duas linhas do card e reduziu o frame Estado a três linhas.
  Esta sprint remove o frame Estado de vez
- **Decisões dela, tomadas em 01/08 e já fechadas:** o desenho do card
  unificado (opção A do preview) e o destino dos valores X/Y dos analógicos
  (ficam embaixo). Ver "As duas escolhas dela", abaixo

## As cinco anotações do print

Ela marcou a tela com cinco setas. Em ordem de leitura:

1. *"apaga estado, a bateria fica ao lado do hertz do giroscópio até o final e
   adicionamos as duas linhas"*;
2. *"conexão e perfil acima do giroscópio hertz — sem o conexão, tá com tab no
   início"*;
3. *"unir os dois blocos num só"*;
4. *"remover o não ajustado"*;
5. *"L3 e R3 saem do X: e vão ficar no centro do desenho do analógico com
   transparência 70% e grande ao fundo"*.

## As duas escolhas dela

**Escolha 1 — o desenho do card unificado.** Confirmada por ela em 01/08:

```
┌─ Controle 1 — USB · Jogador 1 ─────────────────────────────┐
│                                                             │
│  Perfil ativo: Nenhum          Hefesto: Ligado              │
│                                                             │
│  Giroscópio: fluindo p/ o jogo (~194 Hz)  [████████──] 85 % │
│                                                             │
│  L2  [──────────────────────────]  0 / 255                  │
│  R2  [──────────────────────────]  0 / 255                  │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

`Conexão:` e `Transporte:` **saem** — não por economia de espaço, mas porque
cada um já é dito noutro lugar da mesma tela: a conexão no cabeçalho
(*"Conectado Via USB"*, canto superior direito) e o transporte no título do
card (*"Controle 1 — USB"*). Repetir os dois era o frame Estado dizendo o que
o resto da aba já dizia.

**Escolha 2 — os valores X/Y dos analógicos ficam onde estão**, embaixo do
desenho. Só o rótulo `L3`/`R3` sai da linha e vira marca d'água.

## Entregas

### E1. O frame Estado desaparece; o que sobra dele entra no card

O que sai: o `GtkFrame` `frame_status_estado` inteiro, com a legenda "Estado",
o `status_grid` e a linha da bateria.

O que entra no card, no topo do corpo, acima da linha do giroscópio:

| linha | conteúdo |
|---|---|
| 1 | `Perfil ativo: <valor>` e `Hefesto: <valor>`, lado a lado |
| 2 | a linha do giroscópio à esquerda + a barra de bateria + o `NN %` à direita |

**Onde mexer:**

- `src/hefesto_dualsense4unix/gui/main.glade` — o bloco do
  `frame_status_estado` (procure `id="frame_status_estado"`; ele contém
  `status_estado_box`, `status_grid`, `status_battery_row`,
  `status_battery_bar`, `status_battery_pct`, `status_battery_caption`,
  `status_connection`, `status_transport`, `status_active_profile`,
  `status_daemon`);
- `src/hefesto_dualsense4unix/app/widgets/controller_card.py` — o corpo do card
  é montado em `_montar_ui`; a linha de bateria do card já existe
  (`_battery_row`, hoje ESCONDIDA no modo único porque o frame Estado a
  mostrava) e volta a ser usada;
- `src/hefesto_dualsense4unix/app/actions/status_actions.py` — quem escreve
  nesses widgets: `_set_battery_text` (dono único do número da bateria),
  `_set_battery_row_visible`, e os `_set_label` de `status_active_profile` e
  `status_daemon`.

**Duas armadilhas medidas na leva anterior, que continuam valendo:**

1. **o `GtkProgressBar` desenha o próprio texto CENTRADO.** Numa barra larga o
   `85 %` fica a centenas de pixels de cada borda — é o defeito que ela apontou
   nas barras de L2/R2, com outro nome. A barra tem de continuar com
   `show-text=False` e o número num rótulo ao lado (`status_battery_pct`);
2. **uma célula de `GtkGrid` nunca é mais larga que as colunas que ela
   abrange.** Se a linha da bateria for uma célula de grade e pedir largura
   inteira, TODAS as colunas expandem junto. Ela precisa de caixa própria.

**Onde os widgets do glade vão morar depois.** O `frame_status_estado` sumindo,
os widgets que sobrevivem (`status_active_profile`, `status_daemon`,
`status_battery_bar`, `status_battery_pct`) precisam de um pai. Duas formas, e
a segunda é a recomendada:

- **(a)** mantê-los no glade, dentro de um contêiner invisível, e reparentá-los
  para o card em runtime — é o que a `status_actions._alojar_botao_da_rota` já
  faz com o botão da rota de som, e o precedente está lá;
- **(b) recomendada:** o card passa a CONSTRUIR esses rótulos (ele já constrói
  todo o resto), e a `status_actions` escreve neles pelo card em vez de pelo
  builder. Menos indireção, e tira do glade widgets que só existem para o card.

Quem escolher (b) precisa atualizar os testes que buscam esses ids pelo builder
— eles estão listados em "Testes que vão reprovar".

**Aceite:** com um controle conectado, a aba Status mostra UM card, sem moldura
"Estado" acima dele, com as duas linhas novas no topo. Com DOIS controles, cada
card mostra a própria bateria (é o que já acontece hoje) e nada fica órfão.

### E2. O `· não ajustado` sai do título do alto-falante

Hoje o título do bloco é `Alto-falante · não ajustado` quando não há volume
conhecido — o valor entrou ali na leva anterior, para o botão da rota caber na
linha de baixo. Ela pediu para remover.

**Decisão a tomar por quem executar, e as duas opções têm preço:**

- **remover só o texto "não ajustado"**, mantendo o valor quando ele existe
  (`Alto-falante · 71 %`): o título fica limpo no estado comum (sem posse) e
  informativo depois do primeiro ajuste. É a leitura literal do pedido dela;
- **remover o sufixo inteiro**: o título volta a ser sempre `Alto-falante`, e o
  valor precisa de outro lugar — mas os três lugares possíveis já foram
  medidos e todos custam (ver ALINHA-DUAS-LINHAS-01, seção "O que entrou",
  item 3). **Não escolha esta sem reler aquela seção.**

**Onde mexer:** `controller_card.py`, `_escrever_valor_do_speaker` (monta o
título) e `TEXTO_SPEAKER_SEM_DADO`.

**Aceite:** sem volume conhecido, o título do bloco não diz "não ajustado".

### E3. L3 e R3 viram marca d'água no centro do analógico

O rótulo sai da linha de valores e é desenhado **dentro** do círculo do
analógico: grande, ao fundo, com ~70% de transparência (ou seja, alpha ~0,3).
Os valores `X:128 / Y:128` continuam embaixo, como hoje.

**Onde mexer:** `src/hefesto_dualsense4unix/gui/widgets/stick_preview_gtk.py`
— a classe `StickPreviewGtk`, que é o desenho Cairo do analógico (atenção ao
caminho: é `gui/widgets/`, não `app/widgets/`) — e
`app/widgets/controller_card.py`, `_montar_capsula_stick`, que a instancia com
`StickPreviewGtk(label=rotulo_stick)` e monta o título e a linha de valores.
Repare que o rótulo JÁ é passado ao desenho: é ele que vira a marca d'água.

**Como desenhar, sem inventar:** o `GyroBars._on_draw`
(`app/widgets/sensor_widgets.py`) é o molde mais próximo no repo — ele mostra
`select_font_face`, `set_font_size` e `show_text` sobre um `DrawingArea`. Para
a transparência use `ctx.set_source_rgba(r, g, b, 0.3)`; para centrar, meça o
texto com `ctx.text_extents(...)` e desloque por `-largura/2`, `+altura/2`.

**A ordem de pintura importa:** a marca d'água é FUNDO. Ela tem de ser
desenhada ANTES da cruz e do ponto do analógico, senão cobre o que importa.

**O tamanho tem de derivar da escala de fonte**, e não ser um literal: o card
inteiro obedece `theme.escala_fonte()`, e um número fixo aqui quebraria na
primeira mudança de escala dela. O `GLYPH_PX_POR_DEGRAU_DE_FONTE` do
`controller_card.py` é o precedente.

**Aceite:** o círculo do analógico mostra "L3"/"R3" grande e apagado ao fundo;
a linha de baixo tem só os números; e a legenda "Analógico esquerdo/direito"
acima continua (ela não pediu para tirar).

## Testes que vão reprovar, e por quê

Rode `pytest tests/unit -k "status or card or largura or layout or som"` antes
de começar: hoje são **550 verdes**. Estes são os que a mudança toca:

| teste | o que ele trava | o que fazer |
|---|---|---|
| `test_status_faixa_blocos.py::test_o_frame_estado_tem_a_mesma_largura_do_card` | lê o glade e exige `frame_status_estado` com `width-request == LARGURA_CARD_UNICO` | o frame some: o teste tem de medir a largura do CARD contra `LARGURA_CARD_UNICO`, que é o fato que ele sempre quis |
| `test_status_faixa_blocos.py::test_a_bateria_do_card_sai_quando_o_frame_estado_ja_a_mostra` | `_battery_row` invisível no card único | inverte: a bateria do card passa a ser a única, e fica VISÍVEL nos dois modos |
| `test_status_faixa_blocos.py::test_cada_sensor_tem_moldura_propria...[Alto-falante]` | o rótulo da moldura começa com "Alto-falante" | continua válido se você mantiver o prefixo (E2) |
| `test_largura_a_mesma_em_todas_as_abas.py` (3 testes do `status_grid`) | a coluna de valores e o número da bateria | o grid some: estes testes passam a medir os rótulos dentro do card |
| `test_contagem_um_numero_na_janela.py` | `status_battery_caption` visível | idem |
| `test_status_cards.py::test_...battery_caption` | idem | idem |
| `test_status_som_04_rota.py` (3 testes) | o botão da rota nasce no `status_grid` | o berço muda; o teste tem de apontar para o novo pai no glade |
| `test_layout_orcamento_altura.py::test_card_de_um_controle_so_tambem_cabe_na_faixa` | o card ≤ 467px de altura | **este NÃO pode ser afrouxado.** O card ganha duas linhas; se estourar, é sinal de que o desenho precisa mudar, não o teste |

**A regra da casa sobre estes testes**, e ela vale aqui inteira: nenhum deles é
apagado. Cada um passa a medir a REGRA NOVA, com a mordida escrita no
docstring — e onde o teste travava um MECANISMO (o id de um widget), ele passa
a travar o COMPORTAMENTO (a bateria aparece uma vez só na tela).

## Como medir sem depender do olho

Duas bancadas já existem e foram escritas para isto:

- `scripts/gui-captura/retrato_offscreen.py <dir>` — as nove abas em 1920x1080,
  a partir do glade cru;
- o retrato da aba Status **com o card vivo** e a bancada de posições dos
  blocos foram escritos na leva de 01/08 e ficaram no diretório temporário da
  sessão. **Se não existirem mais, reescreva:** montar `ControllerCard(compact=False)`
  numa `Gtk.OffscreenWindow`, chamar `card.update(_ENTRY, _ESTADO, LeituraMic(...))`
  com os dublês de `tests/unit/test_status_faixa_blocos.py`, e imprimir
  `get_allocation()` de cada bloco. É meia página de código e paga em cinco
  minutos.

**A regra da PROVA-DE-TELA-01 vale:** foto antes e depois, e o aceite final é o
olho dela.

## O que NÃO fazer

- **Não mexer nas larguras que a ALINHA-DUAS-LINHAS-01 acabou de acertar.** Os
  dois `Gtk.SizeGroup` que amarram a linha de cima às metades da faixa de baixo
  são a entrega dela de 01/08; encostar neles desalinha o que ela pediu.
- **Não tirar a legenda "Analógico esquerdo/direito"** — ela não pediu, e há um
  `SizeGroup` vertical (`_grupo_titulos_stick`) que trava a altura dessas duas
  legendas juntas.
- **Não aproveitar a leva para "limpar" o glade.** Os ids são contrato: há
  testes que os buscam pelo nome, e o `tab_navegacao_dsx` é o caso registrado
  de id que sobrevive à mudança de rótulo.

---

## O que foi entregue — 01/08/2026, noite

**As três entregas, na tela.** A foto do depois está em
`docs/usage/assets/readme_status.png` (regerada por
`scripts/gui-captura/retratar_abas.py`). Suíte: **6645 → 6664 verdes**.

### E1 — o frame Estado apagou

O frame **não foi apagado do glade**, e a decisão é medida, não preguiça: sem
controle nenhum não existe card, e a aba Status ficaria **muda** — sem dizer
que o daemon está parado e sem o botão da rota de som. Ele virou o que sempre
foi na prática, e agora só isso: o **fallback**.

A regra tem três casos, e `test_o_frame_estado_some_com_um_controle_e_volta_sem_card_unico`
trava os três:

| controles | quem fala |
|---|---|
| **1** | só o card — o frame some inteiro (o pedido dela) |
| **0** | só o frame — não há card para falar |
| **2+** | o frame — perfil e daemon são fatos GLOBAIS e num card por controle apareceriam repetidos |

**A opção escolhida foi a (a) da sprint, não a (b) recomendada**, e por um
motivo que a sprint não tinha: com a (b), o caso de zero controles perde a
única voz da aba. O que a (b) trazia de bom — um escritor só — foi obtido de
outro jeito: `status_actions._set_estado_global` é o **ponto único** que
escreve o par nos dois lugares, e as oito chamadas de `_set_label` para
`status_active_profile`/`status_daemon` passaram por ele.

`Conexão:` e `Transporte:` continuam existindo no frame de fallback, e não
entraram no card: cada um já é dito noutro lugar da mesma tela (a conexão no
cabeçalho, o transporte no título do card).

### E2 — o `· não ajustado` saiu

Escolhida a **primeira** opção da sprint, a literal: o sufixo some no estado
sem dado (`Alto-falante`) e continua quando há valor (`Alto-falante · 71 %`).
A segunda opção obrigaria o valor a achar um terceiro lugar, e os três
candidatos já foram medidos na ALINHA-DUAS-LINHAS-01 — todos cobram pixel.

### E3 — L3 e R3 viraram marca d'água

O rótulo **já chegava** ao `StickPreviewGtk` pelo construtor e nunca era
desenhado. Agora é pintado ANTES da borda, da cruz e do ponto (ela é fundo), com
alpha `0,3` — a "transparência 70%" que ela pediu — e corpo derivado do **raio
alocado** (`MARCA_DAGUA_FRACAO_DO_RAIO`), nunca um literal em px: o desenho tem
dois tamanhos e o card obedece à escala de fonte dela.

O `_markup_xy` perdeu o prefixo e o `pad` de espaços que só existia para
alinhar o `Y` sob o `X`.

**O teste renderiza.** `test_a_marca_dagua_e_realmente_pintada_dentro_do_circulo`
pinta o widget numa `cairo.ImageSurface` e conta a tinta do miolo com e sem
rótulo. Perguntar ao widget se ele guardou o rótulo provaria só que o
construtor funciona — e o construtor já funcionava antes desta sprint.

## O achado que a leva encontrou pelo caminho — ROTA-ÓRFÃ-01

**Medido antes de curado**, com GTK 3.24 e o glade real: o botão da rota de som
é reparentado para o bloco "Alto-falante" do card; plugar um **segundo**
controle recria os cards, e o `child.destroy()` do card antigo deixava o botão
**órfão** (`get_parent() is None`) — vivo, porque o Builder o referência, mas
**fora da tela**.

Para ela: a rota de som está LIGADA nesta máquina. Ao entrar no co-op ela
perdia o botão que desfaz, e só o recuperava desplugando um controle.

Cura: o ramo "sem destino" do `_alojar_botao_da_rota` agora **devolve o botão
ao berço** (`status_grid`, coluna 4, altura 2 — o mesmo empacotamento do
glade, para o grid não ganhar uma linha que ele não tem).

## Uma armadilha nova, para a COMO-OLHAR-A-TELA

**`scripts/gui-captura/retratar_abas.py` rodado pelo shebang (o Python do
sistema) sai SEM O CARD** — ele avisa numa linha (`card não injetado (No module
named 'structlog')`) e fotografa a aba Status vazia mesmo assim. É o comando
que o `CLAUDE.md` manda rodar. **Rode-o com `.venv/bin/python`.**

E o script deixou de **repetir** as regras de runtime da aba: ele agora
CHAMA `_alojar_botao_da_rota` e `_set_frame_estado_visivel` da própria
`status_actions`. Uma cópia delas ali seria um segundo dono, e a foto passaria
a mentir no dia em que a aba mudasse — que é o defeito que este script existe
para não deixar acontecer.

## O que ficou para o olho dela

O vão entre `Perfil ativo:` e `Hefesto:` é a largura do card (os dois pares
ficam ancorados nas bordas, como o giroscópio e a bateria na linha de baixo).
No desenho ASCII que ela aprovou eles estão mais próximos — mas aquele desenho
tem 60 colunas e o card tem 1400px. **Se ela preferir os dois juntos à
esquerda, é uma linha em `_montar_estado_global`** (mover o `vao` para depois
do segundo par).
