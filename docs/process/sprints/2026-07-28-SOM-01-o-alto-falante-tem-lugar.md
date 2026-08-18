# SOM-01 — o alto-falante tem lugar

- **Status:** ENTREGUE (código e testes nesta leva; falta o olho dela na tela)
- **Prioridade:** MÉDIA — são três ajustes de leitura sobre uma entrega que ela
  já aprovou ("quase perfeito"), não uma correção de defeito
- **Aberta em:** 28/07/2026, 21h47, com a janela maximizada em 1920x1080 e um
  controle por USB
- **Sucede:**
  [STATUS-SIMETRIA-02](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md),
  cuja entrega 4 fez o alto-falante existir na tela pela primeira vez
- **Relacionada:**
  [MIC-PRESENTE-01](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md)
  (o vizinho de coluna) e
  [MIC-USB-01](2026-07-25-MIC-USB-01-tres-mutes-empilhados.md), que decidiu que
  o `speaker.set` FICA no protocolo e ganha superfície junto com o microfone

## As três frases dela, literais

> 1. *"dava pra colocar o auto falante abaixo do microfone"*
> 2. *"aumentar e espaçar mais os botões do controle tipo x quadrado bola e
>    triângulo e afins"*
> 3. *"permitir a expansão da janela"*

Nenhuma das três é reclamação de defeito: a v2 foi aprovada. São três pedidos de
leitura sobre a mesma tela, e os três se resolvem no mesmo lugar — a faixa de
baixo do card de um controle.

## O que foi medido, antes de mexer

Card de um controle montado numa `Gtk.OffscreenWindow` de 1870px (a largura que
a aba recebe com a janela maximizada em 1920), com todos os sensores acesos:

| O que | Antes | Depois |
|---|---|---|
| largura do card | 960px fixos, ~950px de margem morta | 1400px (elástica) |
| glifo de um botão | 36x36px | 58x58px |
| grid 4x4 inteiro | 150x150px, 2px de respiro | 262x262px, 10px de respiro |
| alto-falante (x, y) | 468, 292 — coluna da ESQUERDA | 960, 256 — abaixo do mic |
| microfone (x, y) | 986, 110 | 960, 110 |
| distância mic ↔ alto-falante | 518px, em pontas opostas da faixa | 0 (mesma coluna) |
| analógico | 110x110px | 140x140px |
| touchpad / medidor do mic | 140x60 / 140x44 | 180x80 / 180x56 |
| **maior vão entre dois blocos** | **112px** | **143px** (aceite: 200px) |
| altura pedida pelo card | 386px de uma faixa de 526px | 406px da mesma faixa |
| aba Status com 2 controles | 1052px de 1180px | 1064px de 1180px |

O alto-falante estava na coluna da esquerda por herança: quando a rodada
anterior empilhou "o que sobrou" à esquerda, ele foi junto com o touchpad e a
lightbar. Som e cor não têm relação nenhuma, e o par dele — o microfone — estava
do outro lado da faixa.

## Entregas

### E1. O alto-falante muda de coluna e fica abaixo do microfone

Nasce a **coluna do som** (`_montar_coluna_audio`), à direita dos analógicos:
microfone em cima, alto-falante imediatamente abaixo, mesma largura, mesma
moldura. A coluna da esquerda fica com touchpad e lightbar.

A coluna da esquerda **não ficou órfã de altura**: ela e a coluna do som são
ancoradas no TOPO da faixa (`valign=START`), como já eram os analógicos, e é isso
que mantém os títulos das molduras na mesma linha. Medido depois da troca: o
touchpad e o microfone começam no mesmo `y=110`; a altura que a coluna da
esquerda deixou de pedir (242 → 198px) não mudou a altura da faixa, porque quem
manda nela agora é o grid de botões (262px).

Vale nos DOIS cards — o de um controle e o compacto (2+ controles). Deixar o
compacto para trás faria a tela dela mudar de desenho quando o segundo controle
entrasse.

### E2. Os glifos dos botões maiores e espaçados

No card de UM controle: 36 → 58px por glifo (`glyph_size_unico`, cinco terços de
`glyph_size`) e 2 → 10px de respiro. O grid 4x4 sai de 150x150 para 262x262.

O tamanho continua **derivado da escala de fonte** dela, e não px cru: é
`glyph_size() * 13 // 8`. Foi a STATUS-SIMETRIA-01 que tirou o glifo de fora do
alcance do ajuste de fonte, e multiplicar um número fixo o traria de volta pela
porta dos fundos. Há teste próprio para isso.

**Decisão declarada: no card COMPACTO o glifo fica com o tamanho de hoje.** Não
é esquecimento. Com 2+ controles os cards vão lado a lado, a rolagem horizontal
da aba é `never` e a largura de cada card sobe somada até a janela: a folga da
aba inteira com dois cards é de 116px, e o grid maior custa 112px **por card** —
224px nos dois. É a mesma conta que já decidiu a moldura dos blocos em `_bloco`.
Se ela quiser o glifo grande também no co-op, o preço é a janela nascer ~110px
mais larga que o projeto, e isso é decisão dela, não minha.

### E3. O teto de largura vira elástico

O card de um controle deixa de ser 960px fixos e passa a acompanhar a janela,
do piso (1040px) até o teto elástico (1400px), centrado.

O corte fica no `do_size_allocate`, e não num `set_size_request`, por um motivo
do GTK3: pedido de tamanho é **mínimo**, não máximo — não existe "largura
máxima" declarada, e `halign=CENTER` com um mínimo declarado trava o widget
naquele número exato. Era assim que o card ficava em 960px com a janela em 1920.

**O teto não some, e é de propósito.** Sem teto nenhum o card estica pelos
1870px e a sobra vira buraco DENTRO da faixa — o defeito 4 da rodada anterior,
que tinha 673px de nada de cada lado dos analógicos. O que impede a volta dele
não é o teto: é o CONTEÚDO crescer junto (glifos, analógicos, touchpad,
medidores, barras de gatilho e giroscópio) e a sobra restante ser repartida
entre os TRÊS blocos da faixa, em vez de se acumular em dois vãos.

Medido com a mordida posta: sem o corte elástico, os vãos vão a **299px**; com o
corte mas com a sobra indo só para o miolo, vão a **206px**; com a leva inteira,
**143px**. O aceite é 200px.

O **frame "Estado"** (do glade) sobe junto no piso — 960 → 1040 — e **não** ganha
o teto elástico. É decisão escrita, com o motivo medido: ele não tem código
nosso, então só poderia crescer por `width-request`, que é mínimo e sobe intacto
até a janela; a aba Status já responde por 1064 dos 1180px com que a janela abre.
E cinco linhas de rótulo não têm o que fazer com largura extra — esticá-las é o
defeito que a rodada anterior curou.

## O que o alto-falante MOSTRA hoje — e por que não é um controle

Este é o registro que faltava no repositório: o alto-falante aparece de
passagem em ABAS-01, STATUS-SIMETRIA-01, MIC-USB-01 e DOC-VERDADE-01, e nunca
teve sprint própria.

**Hoje o bloco é LEITURA, e quase sempre leitura de "não sei".** O que ele
mostra:

| Estado | O que a faixa diz |
|---|---|
| ninguém ajustou o volume nesta sessão | a barra em repouso e `não ajustado` |
| depois de um `speaker.set` nosso | a barra no volume e a porcentagem |
| `speaker.set` com `muted=true` | `mudo`, sem perder o volume preferido |
| controle sem leitor de inputs | tudo apagado, o espaço reservado |

**Por que quase sempre é "não ajustado".** O DualSense **não devolve** o volume:
não há report de input nem feature report que leia esse registrador. Escrever é
o único jeito de o valor ser conhecido. Por isso o `daemon.state_full` só passa a
trazer a chave `speaker` DEPOIS de um `speaker.set` nosso
(`daemon/ipc_handlers.py::_handle_speaker_set`) — antes disso, publicar um número
seria inventá-lo, e um `0 %` ali seria volume mentido.

E há uma segunda razão, de posse: mic e alto-falante do DualSense são o MESMO
bloco de bytes do report de saída (`common[4..9]`, AUDIO-OWNER-01). A primeira
escrita faz o hefesto assumir a posse desses bytes — antes dela quem manda é o
firmware. Assumir posse sem que ninguém tenha pedido é exatamente o hábito que
produziu "a config que eu deixo nunca é respeitada".

**O que faltaria para virar controle de verdade** (não entra nesta leva):

1. um controle de volume no bloco — o ponto exato de fiação já está escrito em
   `app/ipc_bridge.py::speaker_set`: *"um slider de volume do controle ao lado
   do medidor, ligado por `app/actions/status_actions.py`"*;
2. um botão de mudo do alto-falante, no mesmo desenho do botão do microfone da
   MIC-USB-01, com a mesma honestidade no rótulo: quem clica assume a posse;
3. **a decisão dela sobre o preço**, que é o item que trava os dois de cima: o
   primeiro clique tira do firmware o controle do volume, e não há como devolver
   por leitura (não existe leitura). O microfone tem "Devolver" porque o estado
   do mudo é lido de volta; o alto-falante não teria como confirmar que devolveu;
4. persistência por perfil, se ela quiser que o volume do controle acompanhe o
   perfil aplicado — hoje não acompanha, e nada no produto promete que sim.

Enquanto isso não existir, **o bloco continua dizendo o que sabe e nada além**.
Um slider que o daemon aceita mas cujo valor ninguém consegue ler de volta seria
inventar controle que não funciona.

## Teste que morde

Arquivo novo: `tests/unit/test_status_som_e_janela.py` (9 testes) e dois testes
novos/ajustados em `tests/unit/test_status_faixa_blocos.py`. Todos medem o card
MONTADO e ALOCADO numa `Gtk.OffscreenWindow` de 1870px — widget sem alocação
devolve 1x1 em tudo, e um teste de geometria sobre ele passaria com qualquer
layout.

As oito mordidas, cada uma arrancada de verdade e devolvida:

| Cura arrancada | O que reprova |
|---|---|
| alto-falante de volta para a coluna da esquerda | `x` e `y` do bloco: 2 falhas |
| `glyph_size()` nos dois cards | glifo único == compacto |
| respiro do grid de volta a 2px | distância medida entre cruz e bola |
| `halign=CENTER` da v2 | as duas larguras empatam em 1040 |
| corte do `do_size_allocate` | card vai a 1870 e os vãos a 299px |
| `valign=CENTER` na coluna da esquerda | touchpad desce ~35px do microfone |
| `glyph_size_unico` virando `return 58` | escala 0 e escala 3 empatam |
| sobra deixando de se repartir nos 3 blocos | vãos vão a 206px |

## Como você valida

1. Aba Status com um controle, janela **maximizada**: o card ocupa a largura
   toda até um limite e fica centrado — não é mais uma faixa estreita no meio
   de dois vazios enormes.
2. Os botões (X, bola, quadrado, triângulo, setas, L1/R1/L2/R2, share/options/
   PS/touch) estão visivelmente maiores e com ar entre eles.
3. O alto-falante está **logo abaixo** do microfone, mesma largura, mesma
   moldura. À esquerda ficaram só touchpad e lightbar, alinhados pelo topo.
4. Encolher a janela até o tamanho de projeto: o card encolhe junto, sem barra
   de rolagem horizontal e sem nada saindo pela borda.
5. Com dois ou mais controles: os cards ficam lado a lado como antes, com o
   alto-falante também abaixo do microfone, e os glifos no tamanho de hoje.

## O que NÃO foi feito nesta leva

- **O frame "Estado" não cresce com a janela** — só o piso subiu (1040px). O
  motivo está na E3, e a saída, se ela quiser, é dar código próprio a ele (o
  mesmo corte do card), o que sai do escopo desta leva.
- **O glifo do card compacto não cresceu** — decisão declarada na E2, com o
  preço medido.
- **O alto-falante continua sem controle de volume** — o que faltaria está na
  seção acima, e o item 3 de lá é decisão dela.
- **Nada foi validado na tela dela ainda**: as medidas são de
  `Gtk.OffscreenWindow`, renderizadas em PNG e conferidas com o olho, mas o
  aceite é o dela.
