# A documentação da v0.3.0 — índice da rodada de 29/07/2026

- **Escrito em:** 29/07/2026, sobre `restauro/inicio-da-sessao`, depois de a
  `v0.3.0` ser publicada em `2c18504`
- **O que é:** seis documentos saíram na mesma rodada. Nenhum deles tem código;
  todos são levantamento, plano ou lista para ela escolher. Esta página diz o
  que cada um responde e em que ordem ler
- **Regra da rodada:** nada fora de `docs/` foi tocado. Nenhum commit, nenhuma
  instalação, nenhum daemon reiniciado
- **Portões:** os seis passam em `validar-acentuacao.py`, `validar-glifos.py` e
  `validar-referencias-docs.py`, rodados com caminho explícito porque são
  arquivos novos e o `--all` da acentuação só enxerga o que já está no git

## Os seis, e o que cada um responde

| # | Documento | Responde a pergunta |
|---|---|---|
| 1 | [O mapa da sessão e o que os agentes mediram](2026-07-29-mapa-da-sessao-e-o-que-os-agentes-mediram.md) | *O que aconteceu entre `5489c2a` e a v0.3.0, e o que a auditoria de quatorze agentes descobriu sobre este projeto que não estava escrito em lugar nenhum* |
| 2 | [INDICE — o que falta depois da v0.3.0](../sprints/2026-07-29-INDICE-o-que-falta-depois-da-v030.md) | *Quais sprints continuam de pé, o que ficou pela metade nesta sessão, e o que ainda nem tem documento* |
| 3 | [SENSOR-VIVO-01 — touchpad, giroscópio, microfone e som dentro do jogo](../sprints/2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md) | *Dos quatro sensores, quais já chegam ao jogo hoje e o que falta para os outros* |
| 4 | [SOM-02 — o alto-falante que funciona](../sprints/2026-07-29-SOM-02-o-alto-falante-que-funciona.md) | *Como fazer o alto-falante funcionar na janela, e qual é o preço exato de assumir o volume* |
| 5 | [LARGURA-01 — a mesma largura em todas as abas](../sprints/2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | *O que a aba Status ganhou serve para as outras oito? Aba por aba, com número* |
| 6 | [GATILHO-PALAVRA-01 — os dezenove modos em português](../sprints/2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md) | *Como chamar cada um dos dezenove modos de gatilho, com três opções e uma recomendação para ela riscar* |

## Em que ordem ler

**Se você tem dez minutos:** o **1** e o **2**, nessa ordem. O primeiro conta o
que a sessão produziu; o segundo diz o que fazer a seguir. Os outros quatro são
consulta.

**Se você vai escolher a próxima leva:** comece pelo **2**, que já classifica
tudo por faixa de dano, e desça para o documento da sprint que ela escolher.

**Se você vai mexer na janela:** leia a seção 7 do **1** primeiro. Ela tem as
seis lições de layout e de portão que custaram medição nesta sessão — no GTK3
não existe largura máxima declarada, `importorskip("gi")` aceita stub, typelib
parcial derruba a coleta inteira, SVG sem librsvg muda a geometria, gate cego a
arquivo novo, e morte silenciosa aos 40% da coleta é assinatura de falta de
memória. Depois vá para o **5**.

**Se você vai mexer no som:** o **3** e o **4** são irmãos e têm de ser lidos
juntos, nessa ordem. O **3** mede o caminho do som **até o jogo** (o PipeWire, a
camada que decide se sai som); o **4** desenha o controle **na janela** (o
registrador HID). Ler só o **4** leva a construir um controle deslizante que é
obedecido pelo firmware e não produz som nenhum, porque a camada de cima está
muda — que é exatamente o estado desta máquina hoje.

## O que os quatro pedidos dela viraram

Os quatro documentos de sprint desta rodada nasceram de quatro frases, e cada
uma está transcrita literal na página que responde a ela.

| A frase dela | Virou |
|---|---|
| *"como vamos fazer o autofalante, o touchpad, microfone, e giroscopio funcionar no jogo ao vivo?"* | SENSOR-VIVO-01 (o **3**) |
| *"temos que fazer a sprint do autofalante, inclusive, como vamos fazer ele funcionar na interface"* | SOM-02 (o **4**) |
| *"aba de status semi perfeita, vale a sprint pra usarmos a largura igual nas demais abas"* | LARGURA-01 (o **5**) |
| *"preciso que renomeie os nomes dos tipos de gatilhos que temos pra sinonimos pode fazer uma lista pra gente?"* | GATILHO-PALAVRA-01 (o **6**) |

## As três respostas que contrariam o que se esperava

Vale destacar, porque em três dos seis a medição disse o contrário da hipótese
de partida, e é o tipo de coisa que se perde num índice mal escrito.

1. **A régua única não serve para as nove abas.** O **5** mediu e a resposta é
   "oito sim, uma não": o log da aba Sistema tem a única linha da janela com uso
   legítimo para a largura inteira — 175 caracteres que pedem 1400px exatos —, e
   um teto de 1400px na página quebraria essa linha em duas. A exceção está
   escrita, com aceite que pede o **contrário** do teto.
2. **Dois dos quatro sensores já funcionam, e a sprint não propõe trabalho para
   eles.** O **3** mediu no daemon vivo: `motion_streaming=true`, 189,2 Hz, e a
   posição do dedo do touchpad viaja dentro da mesma janela de bytes do
   giroscópio. O que falta é só o **clique**, e o motivo é uma linha de fiação —
   o codificador já sabe montar o bit, o nome do botão é que nunca chega.
3. **O alto-falante tem três camadas de volume e a janela só alcança a do
   meio** — justamente a única sem leitura e com preço. O **4** mediu que a
   camada de cima está muda agora, com 40% persistido no WirePlumber.

## O que esta rodada corrigiu nos próprios documentos

Registrado para não parecer que os seis nasceram prontos. Tudo abaixo foi achado
conferindo um documento contra o outro e contra a árvore.

| O que estava errado | Onde | Como ficou |
|---|---|---|
| `LARGURA_CARD_ELASTICA` citado na linha 317 | o **1**, duas vezes | é a linha **316** (conferido em `app/widgets/controller_card.py`) |
| `GLYPH_FATOR_UNICO_OITAVOS` citado na linha 194 | o **1**, duas vezes | é a linha **195** |
| o vão da Navegação com o teto dito como 571px na prosa e 565px na tabela do mesmo documento | o **5** | **565px**, que é o valor no JSON da medição |
| o cadeado `autoswitch_locked` listado como "não medido" | o **2** | **foi medido**: o arquivo existe, mtime 28/07 18:18 — e as duas explicações valem ao mesmo tempo |
| a SOM-02 listada como "sprint nova que falta ser escrita" | o **2** | foi escrita na mesma rodada; a linha agora aponta para ela e diz que continua **sem código** |
| a E5 do **3** dizia que o controle deslizante de volume "não está sendo reaberto", enquanto a E1 do **4** propõe exatamente esse controle | entre o **3** e o **4** | não era veto, era divisão de trabalho — os dois documentos agora dizem qual camada cada um trata e por que a ordem importa |

## Uma divergência que fica registrada, e não foi reescrita

O comentário de `app/widgets/controller_card.py:226` diz que a folga da aba
Status com dois cards é de **128px**, citando o teste
`test_dois_cards_lado_a_lado_cabem_na_largura_da_janela`. A bancada do **4**
mediu **116px** (1064px pedidos de 1180px disponíveis) na montagem dela. Os dois
números vêm de montagens diferentes e nenhum dos dois foi conferido contra o
outro nesta rodada. Fica escrito aqui em vez de um dos dois ser silenciosamente
adotado como verdade — e quem for mexer no orçamento de largura da aba Status
tem de remedir antes, não escolher.

## O que esta rodada NÃO fez

- **Nenhuma linha de código.** Os seis são documento. As entregas numeradas dos
  quatro documentos de sprint são propostas com critério de aceite, não trabalho
  feito.
- **Nada foi visto na tela dela.** As medidas de geometria são de
  `Gtk.OffscreenWindow` renderizada em PNG; as de áudio e de sensor são desta
  máquina, hoje, com o daemon vivo. O aceite continua sendo o dela, pela regra
  da
  [PROVA-DE-TELA-01](../sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
- **Os cabeçalhos `Status:` das sprints antigas continuam mentindo.** O **2**
  mede o tamanho do problema: 36 de 39 dizem ABERTA, várias delas entregues.
  Corrigir isso é trabalho de uma leva própria, e não foi feito aqui para a
  rodada não misturar documento novo com edição em massa de documento velho.
