# CARD-OCUPA-01 — o desenho ocupa o vão que o teto devolveu

- **Status:** **PARCIAL — as E1, E2 e E3 estão ENTREGUES EM CÓDIGO, AGUARDANDO
  A PALAVRA DELA; a E4 segue ABERTA, e a E4 É a palavra dela.** Remarcada em
  09/08/2026: entraram em `cd5eaf1` (31/07/2026). **Rótulo anterior: ABERTA**,
  preservado aqui. Ver a nota datada no fim
- **O que falta ela validar, em uma linha:** abrir a aba Estado maximizada e ver
  se o touchpad, a lightbar, o microfone e o alto-falante **ocuparam os espaços
  laterais vazios** que ela apontou — é literalmente o pedido dela, palavra por
  palavra
- **Prioridade:** MÉDIA — é a aba que ela mais olha, mas nada aqui desfaz
  trabalho dela
- **Aberta em:** 31/07/2026, 01h34, com a janela maximizada em 1920x1080, o
  DualSense no cabo e a foto guardada em
  `docs/process/estudos/assets/2026-07-31-card-ocupa/2026-07-31-0134-aba-status-maximizada-1920.png`
- **Pedido dela, literal:** *"tem muito espaço vazio aqui, dava pra aumentar a
  largura do touchpad e lightbar e do microfone e alto falante pra ocuparem os
  espaços laterais vazios"*
- **Sucede:** [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md) (criou o
  teto elástico e a régua *"a largura que a janela devolve tem de virar
  desenho, não vão"*) e
  [STATUS-SIMETRIA-02](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md)
  (criou o aceite dos 200px de vão)
- **Não confundir com** [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md),
  entrega E2: o miolo do frame **Estado** (a barra de bateria de 1242px) é
  daquela sprint e continua lá. Esta aqui é só a faixa de leitura do **card**.

## O que a foto mostra — e por que nenhum teste reclamou

A foto é o card de um controle com o teto elástico em ação: o card está nos
1400px (`LARGURA_CARD_ELASTICA`, `app/widgets/controller_card.py:316`), centrado,
como a SOM-01 desenhou. E dentro dele os desenhos continuam do tamanho do piso:
o touchpad é um retângulo de 180px numa faixa de 1400, a lightbar uma barra de
160, e a coluna do microfone e do alto-falante aperta os mesmos 180px entre os
analógicos e os glifos.

O teste guardião da faixa não reclama, e o motivo é aritmético, não defeito do
teste: `test_status_faixa_blocos.py` cobra `VAO_MAXIMO_ENTRE_BLOCOS = 200` (`:59`)
entre blocos **vizinhos**. A sobra da faixa hoje se reparte em três respiros
(`controller_card.py:1195-1204` — os três filhos entram com `expand=True,
fill=False`), então nenhum vão individual passa de 200px e o teste fica verde
com a tela mostrando ~500px de nada somados. O aceite antigo era um teto de
vão; o pedido novo é a outra metade da receita que a própria SOM-01 escreveu ao
crescer estes mesmos desenhos uma primeira vez (`controller_card.py:345-346`):
**a largura que a janela larga devolve tem de virar desenho, não vão.** Os
desenhos cresceram uma vez e pararam; a janela continuou crescendo.

## As medidas de hoje, arquivo e linha

| O que ela nomeou | Constante | Valor | Aplicada em |
|---|---|---:|---|
| Touchpad | `_TOUCHPAD_PX_UNICO` (`controller_card.py:347`) | 180 x 80 | `:1290` (`set_size_request`) |
| Microfone (medidor) | `_MIC_METER_PX_UNICO` (`:348`) | 180 x 56 | `:1320` (`set_size_request`) |
| Lightbar | `_BARRA_FINA_PX_UNICO` (`:349`) | 160 x 18 | `:1413` (`set_size_request`) |
| Alto-falante | `_BARRA_FINA_PX_UNICO` (`:349`) | 160 x 18 | `:1443` (`set_size_request`) |

Três fatos medidos que decidem o desenho da cura:

1. **`set_size_request` no GTK3 é MÍNIMO, não tamanho.** É a lição escrita no
   próprio arquivo (`controller_card.py:314-315`): não existe "largura máxima"
   declarada, e um `DrawingArea` tem largura natural igual à mínima — por isso
   os quatro desenhos ficam parados no piso enquanto o card cresce até 1400.
2. **O piso não tem folga para números fixos maiores.** O comentário do piso
   (`:294-297`) registra: com os desenhos desta leva o conteúdo do card pede
   ~1030px de um piso de 1040 (`LARGURA_CARD_UNICO`, `:298`), e o mínimo da
   janela inteira é 1062px medido
   (`test_a_janela_inteira_cabe_na_largura_de_projeto`), sem rolagem horizontal
   para onde fugir. **Subir os `size_request` estoura o piso** — a cura fixa é
   proibida pela mesma aritmética que proibiu o piso decorativo.
3. **Alargar o touchpad não mente a posição do dedo.** O `TouchpadView`
   normaliza o toque por fração (`sensor_widgets.py:446-457`:
   `px = 2 + fx * (largura - 4)`) — o ponto continua no lugar relativo certo em
   qualquer largura. O que muda é a proporção do retângulo (hoje 180x80 ≈ a
   proporção física do touchpad); se o alongamento incomodar o olho, é aceite
   visual dela, não erro de mapa.

## A cura: mínimo fica, o NATURAL cresce

O caminho que respeita as três medições acima: separar mínimo de natural nos
quatro desenhos — o mínimo continua o de hoje (o piso de 1040 não sobe um
pixel), e a largura **natural** passa a ser o teto novo. Com `expand=True,
fill=False`, que a faixa já usa, o GTK dá a cada bloco o tamanho natural quando
há espaço e o mínimo quando aperta — o comportamento elástico cai da estrutura
que já existe, sem mexer na mecânica da faixa. Em `DrawingArea` isso é
`do_get_preferred_width` devolvendo `(mínimo, natural)` distintos; a
alternativa, se a subclasse pesar, é a `CaixaDeTetoElastico`
(`controller_card.py:1986-2015`) parametrizada por bloco.

Os tetos numéricos abaixo são **propostas de partida** — o número final sai da
bancada offscreen da LARGURA-01 (a receita com `Gtk.OffscreenWindow`, o tema
real e o laço rodando 2,5s antes de medir), nunca de chute:

| Desenho | Hoje | Natural proposto | Altura |
|---|---:|---:|---|
| Touchpad | 180 | ~360 | **não muda** (80) |
| Medidor do microfone | 180 | ~360 | **não muda** (56) |
| Lightbar | 160 | acompanha a coluna do touchpad | **não muda** (18) |
| Alto-falante | 160 | acompanha a coluna do microfone | **não muda** (18) |

As barras finas não ganham teto próprio: elas esticam até a largura da coluna
em que vivem (`_montar_coluna_sensores`, `:1234-1251`, e `_montar_coluna_audio`,
`:1253`), para a lightbar não ficar curta debaixo de um touchpad largo — a
coluna é um assunto só e se lê alinhada.

**Altura não entra nesta sprint, por escrito.** O orçamento apertado do card é
vertical (`controller_card.py:194`: *"o teto de verdade é a altura, não a
largura"*), e as quatro alturas ficam exatamente como estão. Se alguém propuser
crescer o touchpad em proporção, isso é outra sprint com o orçamento de altura
na mesa.

## Entregas

### E1. Touchpad e lightbar elásticos (coluna da esquerda)

Mínimo 180/160 como hoje; natural do touchpad no teto medido pela bancada
(partida: 360); lightbar acompanhando a largura da coluna.

**Aceite:** com a janela em 1870 (`LARGURA_DA_TELA_DELA`,
`test_status_faixa_blocos.py:53`) e um controle conectado, o touchpad recebe
pelo menos 300px e a lightbar mede a largura da coluna; com a janela no tamanho
de projeto, os dois medem exatamente o que medem hoje.

### E2. Microfone e alto-falante elásticos (coluna do áudio)

Simétrica à E1: medidor com natural no teto medido (partida: 360), alto-falante
acompanhando a coluna. Os rótulos e botões do bloco ("Silenciar", "sem sinal")
não mudam de reserva — a disciplina de campo fixo de `_MIC_ESTADO_CHARS`
(`controller_card.py:369`) continua valendo.

**Aceite:** espelho do da E1, para o medidor e o alto-falante.

### E3. O teste que morde

Duas asserções novas em `tests/unit/test_status_faixa_blocos.py`, nesta ordem
de mordida:

1. **A do crescimento:** com o card montado e alocado em janela de 1870, cada
   um dos quatro desenhos recebe pelo menos o piso do aceite (300px nos dois
   grandes; largura da coluna nas duas barras). Arrancar a cura — voltar o
   `size_request` fixo — reprova aqui.
2. **A do piso:** o mínimo de largura pedido pelo card de um controle continua
   no máximo `LARGURA_CARD_UNICO`. Implementar a cura errada — request fixo
   maior — reprova aqui, e é esta asserção que impede a sprint de repetir o
   defeito que o comentário do piso documenta.

Regras herdadas que continuam valendo sem edição:
`test_nenhum_vao_de_mais_de_200px_entre_os_blocos_da_faixa` (os vãos só podem
cair), `test_o_card_de_um_controle_nao_estica_pela_tela_inteira` (o teto de
1400 não muda) e o orçamento de altura (nenhuma altura foi tocada). Todos medem
widget **montado e alocado** em `Gtk.OffscreenWindow` — widget sem alocação
devolve 1x1 e aprova qualquer layout (nota da SOM-01, repetida aqui de
propósito).

### E4. A prova de tela

Print antes e depois, mesma janela maximizada, guardados em
`docs/process/estudos/assets/2026-07-31-card-ocupa/` ao lado da foto que abriu
a sprint. Regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
o aceite final é o olho dela, e nenhuma entrega vira commit sem os prints
guardados junto.

## Como você valida na tela

1. Janela **maximizada**, aba Status, um controle no cabo: o touchpad deixou de
   ser um selo — o retângulo tem presença na coluna, e a lightbar embaixo tem a
   mesma largura que ele.
2. A coluna do microfone: o medidor alarga, o alto-falante acompanha, e os
   botões continuam onde estavam.
3. Encoste um dedo no touchpad do controle: o ponto na tela continua nascendo
   onde o dedo está — canto no canto, centro no centro.
4. **Encolha a janela** até o tamanho de projeto: tudo volta ao tamanho de
   hoje, nada corta, nada rola na horizontal.
5. Conecte um segundo controle: os cards compactos estão **idênticos ao que
   eram** — esta sprint não os toca.

## O que fica de fora, por escrito

- **O frame Estado** (a barra de bateria com 1242px para dois dígitos) — é a
  entrega E2 da LARGURA-01, medida lá, e mexer nela aqui seria pegar carona.
- **O card compacto (2+ controles).** Nele cada pixel de mínimo sobe direto
  para o mínimo da janela (`controller_card.py:325-329`); os tamanhos compactos
  ficam como estão.
- **Os glifos dos botões.** O grid 4x4 tem orçamento próprio e documentado
  (`controller_card.py:194-199`); o vão que ela apontou está à esquerda dele,
  não dentro.
- **Altura de qualquer desenho.** Dito acima; repetido aqui porque é a
  tentação mais próxima.
- **Os analógicos.** Ela não os citou — os círculos já têm o tamanho da SOM-01
  e o vão da foto não está neles.

## O que eu não medi

- **Os números finais dos tetos.** 360 é proposta com régua de dobro; a
  bancada decide, e o print decide por cima dela.
- **O efeito com escala de fonte acima de 3.** A mesma dívida declarada na
  VÃO-01 e na LARGURA-01 continua: o pior caso de largura é a escala 8 e
  ninguém a mediu em nenhuma das três sprints.
- **A janela compacta e a bandeja** (`app/compact_window.py`, `app/tray.py`).
  Se elas repetem os desenhos, a cura daqui não as alcança — a auditoria de
  31/07 está abrindo as duas pela primeira vez, e o resultado dela decide se
  esta sprint ganha uma entrega irmã.

---

## NOTA DATADA — 09/08/2026: três entregas saíram, e a quarta É a palavra dela

**Nada acima foi apagado.** O pedido literal dela, a foto de 31/07 01h34 e as
quatro entregas continuam inteiros.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **E1.** Touchpad e lightbar elásticos | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/app/widgets/controller_card.py:2554` e `:2586`, mais `src/hefesto_dualsense4unix/app/widgets/sensor_widgets.py:253` — esta última cita o pedido dela por extenso |
| **E2.** Microfone e alto-falante elásticos | ENTREGUE EM CÓDIGO, aguardando a palavra dela | mesmo par de widgets, mesma leva |
| **E3.** O teste que morde | ENTREGUE EM CÓDIGO | `src/hefesto_dualsense4unix/app/widgets/controller_card.py:3032` — *"CARD-OCUPA-01 exige os dois IGUAIS, e há teste"* |

**Commit:** `cd5eaf1`, 31/07/2026.

### A E4 continua ABERTA — e ela é a única que não podemos fechar sozinhos

**A E4 desta sprint é "A prova de tela".** Ela não é um resto de trabalho: ela
**é** a validação dela. Enquanto ela não olhar a aba Estado maximizada e disser
que o vão sumiu, esta sprint não fecha — é a regra da casa, escrita na
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
e repetida no corpo deste documento: *"o aceite final é o olho dela"*.

Por isso o rótulo desta sprint é o que é: **o código está de pé, e a entrega que
falta é a palavra dela.**
