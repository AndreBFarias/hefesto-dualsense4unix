# DUAS CONTABILIDADES-01 — a lâmpada conta a mesa inteira, e o co-op só metade

- **Achado em:** 07/08/2026, às **19h10**, na **máquina dela**, com os **quatro
  controles ligados por Bluetooth ao mesmo tempo** — dois DualSense, o 8BitDo em
  modo DualShock 4 e o Pro Controller. A medição nasceu de uma pergunta dela, e
  a pergunta estava certa antes da resposta existir
- **Estado:** **DIAGNÓSTICO. Nenhuma linha de código tocada.** Leitura pura: nada
  foi reiniciado, nenhum controle foi derrubado, nada foi escrito em `hidraw`
  nem em `/etc`, e o arquivo de configuração dela não foi tocado. O que só fecha
  mexendo virou **protocolo para ela rodar**, no fim deste documento
- **Gravidade:** **ALTA** — o defeito que a medição encontrou não é o que a casa
  procurava, e atinge o caso normal dela: **com dois DualSense e o co-op ligado,
  o plástico que o jogo chama de Jogador 1 acende o número 4, e o que o jogo
  chama de Jogador 2 acende o número 1.** Quem confia na lâmpada para saber quem
  é quem — que é exatamente para isso que a lâmpada existe — pega o controle
  errado
- **Causa-raiz:** **MEDIDA.** São **três** contabilidades vivas na mesa, não
  duas; duas delas contam os controles de outra marca e a terceira, que é a que
  o **jogo** vê, não conta. As três nunca se falam
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [LUGAR À MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)
    — **a mãe desta**. É lá que mora a queixa original ("todos no player 1"), a
    releitura das 19h00 de hoje e as entregas `E3`/`E4`, que ela autorizou só
    depois da MÁSCARA-01. Esta sprint **corrige uma afirmação daquela** (ver a
    seção *"O que mudou no entendimento desta casa hoje"*) e **não** mexe nas
    entregas dela;
  - [COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md)
    — é o dono do "Jogador 2 que morre e renasce", que é metade da resposta 4
    (o cabo no meio da partida). Continua **PROPOSTA**, sem uma linha tocada, e
    a bancada da `E4` dela ainda não existe;
  - [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)
    — mede o **mesmo fenômeno pelo outro lado**: o mesmo plástico com dois
    endereços. O protocolo do cabo, aqui embaixo, encosta nele de graça;
  - [PLAYER-01](2026-07-25-PLAYER-01-um-numero-de-jogador.md) e
    [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md)
    — as duas que fundaram a fila de identidade e o número único. O desenho que
    ela descreve na pergunta é, em boa medida, o que essas duas entregaram;
  - [MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md)
    — o pré-requisito que ela pôs, em 07/08, na frente de qualquer adoção de
    controle de outra marca. **Nada aqui a atropela.**

> **Grau de cada afirmação**, como manda a casa: **MEDIDO** = há leitura ao
> vivo, linha de journal, arquivo lido ou teste que reprova com a cura
> arrancada; **SUSPEITA COM MECANISMO** = o caminho de código foi lido ponta a
> ponta e fecha, o efeito não foi observado; **SEM PROVA** = está dito e ninguém
> verificou.
>
> **Endereços:** todo endereço de rádio neste documento está **mascarado** pela
> convenção da casa — octetos 4 e 5 zerados. No journal dela eles aparecem
> inteiros; se for procurar, procure pelo começo e pelo fim.

---

## A pergunta dela, palavra por palavra

> *"na lógica o certo eram eles irem se acomodando e virando o player à medida
> que conectássemos eles, não? tipo um controle vira o player 1, o outro player
> 2, 3, 4 nos 4 controles independente de estarem por cabo ou usb ou bt."*

E o que estava na mesa às 19h10, decodificado pela tabela canônica de
[`core/led_control.py`](../../../src/hefesto_dualsense4unix/core/led_control.py):

| o aparelho | o que as lâmpadas dizem | o produto diz |
|---|---|---|
| controle virtual "Hefesto P1" | **jogador 1** | — |
| controle virtual "Hefesto P2" | **jogador 5** | — |
| DualSense roxo | **jogador 1** | — |
| DualSense branco | **jogador 4** | — |
| Pro Controller | padrão que **não existe** na tabela do DualSense | — |
| a janela do Hefesto | | *"jogadores pelo Hefesto: 2 / controles na mesa: 4, sendo 2 externos"* |

**GRAU: MEDIDO** — leitura dos nós de LED na máquina dela, 07/08 às 19h10.

---

## A resposta, em quatro frases

1. **Sim, o desenho dela é o certo — e metade dele já existe e está funcionando
   hoje.** A metade que existe é *"1, 2, 3, 4 sem buraco, contando todo mundo
   que está na mesa"*. A metade que não existe é *"na ordem de hoje"*: a ordem é
   a da **primeira vez** que cada controle apareceu, e isso foi **decisão
   medida**, não descuido. **GRAU: MEDIDO.**
2. **O branco mostra 4 e não 2 porque a nossa fila conta os quatro controles, e
   os outros dois não acendem número desde as 15h27 de hoje.** A conta está
   certa; o que ela vê é um buraco onde estão os dois controles calados.
   **GRAU: MEDIDO.**
3. **Não há colisão no jogador 1 — há coisa pior: um cruzamento.** As duas
   lâmpadas que mostram "1" pertencem a dois universos que não se tocam, e é
   coincidência. O defeito real é que **o controle que o jogo chama de Jogador 1
   acende 4, e o que o jogo chama de Jogador 2 acende 1**. **GRAU: MEDIDO.
   Precisa de sprint.**
4. **Se ela plugar o cabo no meio da partida:** no controle do **Jogador 1**,
   provavelmente nada acontece de ruim; no controle do **Jogador 2, 3 ou 4**, o
   caminho de código diz que o jogador é derrubado e recriado — e esta casa já
   mediu o preço disso, que é o jogo perder o controle e a Steam não reabrir.
   **GRAU: SUSPEITA COM MECANISMO** para o gatilho; **MEDIDO** para o preço.
   **Hoje eu não recomendo o gesto no meio de uma partida que importe.**

O resto deste documento é o porquê de cada uma, com o dedo em cima da medição.

---

## O quadro que explica os cinco números: são TRÊS contas, não duas

O nome deste arquivo diz *duas contabilidades* — ele nasceu antes da medição
terminar. **São três.** Fica o nome, porque arquivo desta casa não se reescreve
para parecer que sempre soube.

| # | quem conta | o que ela conta | quem ela pinta | quem a lê |
|---|---|---|---|---|
| 1 | **a fila da casa** (nossa) | todo controle **presente**: DualSense **e** os de outra marca | a barra dos **DualSense** | a janela do Hefesto, a linha de comando, a cor |
| 2 | **a conta do kernel** (do Linux, não nossa) | **todo** aparelho estilo PlayStation que aparece, inclusive os **controles virtuais** que nós mesmos criamos e o 8BitDo em modo DualShock 4 | a barra dos **controles virtuais** | ninguém, de propósito — nós nunca escrevemos ali |
| 3 | **a conta do co-op** | só os DualSense que o Hefesto **adota** | ninguém | **o jogo**. É o "Jogador 1", "Jogador 2" que aparece na tela |

**GRAU: MEDIDO** para as três. A primeira é
`daemon/subsystems/identity.py`; a segunda é o driver `hid-playstation` que esta
casa empacota (a soma dele roda dentro do kernel, no instante em que o aparelho
aparece); a terceira é `daemon/subsystems/coop.py`.

E agora os cinco números da mesa dela, um a um:

| o aparelho | número | de qual conta ele veio |
|---|---|---|
| controle virtual "Hefesto P1" | 1 | **conta 2** (o kernel deu-lhe o índice 0) |
| controle virtual "Hefesto P2" | 5 | **conta 2** (o kernel deu-lhe o índice 4) |
| DualSense roxo | 1 | **conta 1** (a nossa fila) |
| DualSense branco | 4 | **conta 1** (a nossa fila) |
| Pro Controller | dois verdes acesos | **nenhuma das três** — é o driver da Nintendo, com um contador só dele |
| *"2 jogadores"* na janela | 2 | **conta 3** (o co-op: um primário e um secundário) |

**GRAU: MEDIDO** — cada linha tem evidência nas seções abaixo.

Uma observação que vale a pena guardar, porque engana à primeira vista: as duas
tabelas de padrão — a nossa e a do driver `hid-playstation` — são **iguais byte
a byte**. É por isso que a decodificação dela funcionou nos controles virtuais
também. Elas concordam sobre **como desenhar** um número, e discordam
completamente sobre **qual número desenhar**. **GRAU: MEDIDO.**

---

## Resposta 1 — o desenho dela é o certo? Sim. E quanto dele já existe

### A metade que já existe, e está funcionando agora

A fila da casa faz **exatamente** o que ela descreveu, com uma frase de critério
escrita no próprio código: *"nunca existe um jogador 2 sem um jogador 1"*. O
desenho é o seguinte, e é de 25/07:

- **quem é quem** fica gravado pelo **endereço** do controle, e o que se grava é
  o **lugar na fila** — não o número. Isso atravessa desligar, religar e
  reiniciar a máquina;
- **o número** é recontado a cada consulta, **1, 2, 3, 4 entre quem está
  presente agora**, sem buraco. DualSense e controles de outra marca entram na
  **mesma fila**, e a conta soma os dois tipos na mesma linha de código.

Hoje, na mesa dela, essa fila entrega: **roxo = 1, 8BitDo = 2, Pro = 3, branco =
4.** Quatro controles, quatro números, nenhum repetido — que é literalmente o
que ela pediu. **GRAU: MEDIDO** (arquivo de configuração dela lido ao vivo, mais
a aritmética em `identity.py`).

E **sim, independente do transporte**, para os DualSense: o endereço de um
DualSense é a **mesma string** no cabo e no rádio, nas três fontes que o produto
usa para perguntar quem ele é. O journal dela prova isso com o mesmo controle
aparecendo com o mesmo endereço numa sessão só-cabo (05/08) e numa sessão
só-rádio (04/08). **GRAU: MEDIDO.**

### A metade que não existe, e por que ela foi negociada

Ela disse *"à medida que conectássemos"*. Isso é a ordem de **hoje**. A fila
guarda a ordem da **primeira vez** que cada controle apareceu — e isso foi uma
troca deliberada, feita porque a queixa anterior desta casa era a oposta:
*"os controles se reenumeram e nunca sei o que é o quê"*. Prender o lugar ao
endereço curou aquilo. **GRAU: MEDIDO** (as três regras estão nomeadas e
comentadas em `identity.py`; a sprint que as fundou é a PLAYER-01).

Quer dizer: se ela ligar hoje o branco primeiro e o roxo depois, o branco
**não** vira 1. Ele vira o número que a fila dele diz. **Se ela quiser a ordem
da sessão**, isso é revogar três decisões medidas — e a regra da casa é que
decisão medida não se apaga, ganha nota datada. **É dela a palavra, e eu não
tomo essa decisão sozinha.** Fica registrado em *"O que fica ABERTO"*.

### E o que NÃO existe de jeito nenhum

1. **Nada escreve esse número nos controles de outra marca desde as 15h27 de
   hoje.** Foi decisão dela ("calar a luz até a entrega existir"), na resposta 12
   do [painel](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md). Dos
   quatro plásticos na mesa, só os dois DualSense mostram o número da casa.
   **GRAU: MEDIDO** — a última escrita nossa num controle externo, no journal
   dela, é às **15h24:01**, e não há nenhuma depois.
2. **O jogo nunca vê os controles de outra marca.** O co-op só numera os
   DualSense que ele adota; o input dos outros vai direto para o kernel e para a
   Steam, sem passar pelo Hefesto — está escrito assim em
   `core/external_leds.py`: *"SÓ LED, nunca input"*. **GRAU: MEDIDO.**
3. **A conta do kernel não é nossa e conta os nossos próprios controles
   virtuais.** Não há como pedir educadamente para ela parar. **GRAU: MEDIDO.**

**Resumo honesto da resposta 1:** o desenho dela está certo, está implementado, e
está **funcionando numa das três contas** — a que quase ninguém consegue ver
hoje, porque metade dos plásticos está com a luz calada por decisão dela e a
outra metade está sendo cruzada pelo defeito da resposta 3.

---

## Resposta 2 — por que o branco mostra 4, e não 2

A fila persistida dela, lida ao vivo em 07/08 (arquivo
`~/.config/hefesto-dualsense4unix/controllers.json`, esquema 3):

| lugar | endereço (mascarado) | tipo | estava na mesa às 19h10? |
|---|---|---|---|
| 1 | `aa:bb:cc:00:00:01` | DualSense | **não** — endereço de teste, ver o achado de borda |
| 2 | `aa:bb:cc:00:00:02` | DualSense | **não** — idem |
| 3 | `a0:fa:9c:00:00:f0` | DualSense | **sim** — o roxo |
| 4 | `e4:17:d8:00:00:83` | outra marca | **sim** — o 8BitDo em modo DualShock 4 |
| 5 | `e0:f6:b5:00:00:53` | outra marca | **sim** — o Pro Controller |
| 6 | `14:3a:9a:00:00:ab` | DualSense | **sim** — o branco |

A conta, que é uma linha de código só (*1 + quantos presentes têm lugar antes do
dele*):

- **roxo:** ninguém presente antes dele -> **1**;
- **branco:** três presentes antes (o roxo, o 8BitDo e o Pro) -> **4**.

**GRAU: MEDIDO.** Os dois endereços dos lugares 1 e 2 **não atrapalham**: eles
nunca estão presentes, e a conta só olha para quem está. Foi exatamente para
isso que a regra de 25/07 separou *lugar na fila* de *número exibido*.

Então a resposta direta é: **o 4 do branco está certo pela regra da casa.** O que
está errado é o que ela **vê**: entre o 1 e o 4 há dois controles que ocupam
lugar na fila e **não mostram número nenhum**, porque a luz deles foi calada
hoje às 15h27 por decisão dela. O buraco que a mesa exibe é o desenho da decisão
12 encontrando a fila unificada — as duas coisas certas, sozinhas, produzindo
uma mesa que parece quebrada.

**Um detalhe que fecha a questão de quem calcula o quê:** às 19h00 o branco
acendia **3**; às 19h10 acende **4**. Nesse meio-tempo o aparelho **não foi
religado nem reconhecido de novo** pelo kernel — o roxo é que entrou, às
19h07:16. O kernel só numera no instante em que o aparelho aparece; quem recalcula
a cada mudança na mesa é a **nossa** conta. **GRAU: MEDIDO** — e é esta a
observação que derruba a causa que a nota das 19h00 tinha atribuído (ver a seção
da honestidade).

---

## Resposta 3 — há colisão no jogador 1? Não. Há cruzamento, e é pior

Esta é a pergunta que decide se existe defeito novo. **Existe.** Mas não é o que
a leitura sugeria.

### Por que os dois "1" não são uma colisão

O controle virtual "Hefesto P1" acende 1 porque o **kernel** lhe deu o índice 0 —
ele foi o primeiro aparelho estilo PlayStation a aparecer nesta sessão, às
18h07:13. O DualSense roxo acende 1 porque a **nossa fila** lhe deu o primeiro
lugar entre os presentes. **São dois contadores que não sabem um do outro.**
Nós nunca escrevemos na lâmpada de um controle virtual, e há **três** camadas
independentes no código que proíbem isso — o registro de identidade recusa
qualquer endereço que comece com o prefixo dos virtuais, o backend filtra na
enumeração, e o leitor de eventos filtra de novo. **GRAU: MEDIDO.**

Os dois mostrarem "1" ao mesmo tempo é **coincidência de dois universos
disjuntos**. E dá para provar que é coincidência: o outro controle virtual se
chama **P2** e acende **5**. Se um espelhasse o outro, esse par não existiria.
**GRAU: MEDIDO** — os nós de LED dos dois virtuais foram lidos ao vivo.

A reconstrução completa da conta do kernel nesta sessão, que fecha os dois
números dos virtuais:

| ordem em que apareceu | aparelho | índice do kernel | padrão |
|---|---|---|---|
| 18h07:13 | controle virtual "Hefesto P1" | 0 | jogador 1 |
| 19h05:44 | 8BitDo em modo DualShock 4 | 1 | (não tem barra; ver abaixo) |
| 18h41:38 | DualSense branco | 2 | — |
| 19h07:16 | DualSense roxo | 3 | — |
| 19h07:18 | controle virtual "Hefesto P2" | 4 | **cinco lâmpadas acesas** = o nosso "jogador 5" |

**GRAU: MEDIDO.** E há uma **prova independente** desse contador, num aparelho
que nem barra de player tem: o 8BitDo, em modo DualShock 4, tem uma barra
colorida em vez de lâmpadas — e a cor dela agora é o **vermelho exato** que o
driver do kernel pinta no aparelho de índice 1. Se fôssemos nós, seria outro
vermelho e outro número. **O controle de outra marca ocupa lugar na fila do
kernel do mesmo jeito que ocupa na nossa** — a intuição dela, confirmada por um
segundo caminho. **GRAU: MEDIDO.**

### O defeito, e ele é sério

O co-op registrou, às **19h07:18**, o roxo como **segundo** jogador
(`coop_player_added identity=a0fa9c0000f0 player=2`, endereço mascarado). Isso
quer dizer que o **branco é o primário** — porque o critério do primário está
escrito no código com todas as letras: *"o primeiro que entrou e ainda está
presente"*, e o branco chegou às 18h41, enquanto o roxo (que tinha caído) só
voltou às 19h07.

Logo, na mesa dela, agora:

| o plástico | o nome que o **jogo** vê | o número que a **lâmpada** dele mostra |
|---|---|---|
| DualSense **branco** | **Jogador 1** | **4** |
| DualSense **roxo** | **Jogador 2** | **1** |

**GRAU: MEDIDO.** Isto é o **cruzamento**: os dois controles estão mentindo, e
estão mentindo **trocados**. Se ela pegar o controle que acende 1 achando que é
o Jogador 1, ela pegou o Jogador 2.

E isto é **exatamente** a metade do invariante que a nota das 19h00 já tinha
isolado — *"a lâmpada no plástico não contradiz o nome que o jogo mostra"* —
agora violada nos **dois** aparelhos ao mesmo tempo, e não em um. O teste que já
modela essa metade é
`tests/unit/test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py`; o que ele
ainda não tem é o caso de **dois** DualSense com o co-op ligado.

**Resposta direta à pergunta: sim, há defeito, e precisa de sprint. Não é uma
colisão de dois no mesmo número — é um cruzamento entre a lâmpada e o nome, nos
dois controles ao mesmo tempo.**

---

## Resposta 4 — o que acontece se ela pluga o cabo no meio da partida

### O que sobrevive, e está medido

- **A identidade do DualSense não muda.** O endereço é a mesma string no cabo e
  no rádio, nas três fontes que o produto consulta. **GRAU: MEDIDO.**
- **O lugar na fila e o número não se perdem.** A fila é indexada pelo endereço;
  desligar guarda o lugar, e ao voltar cada um recupera o seu. **GRAU: MEDIDO**
  (por construção, com o journal dela mostrando o mesmo endereço nos dois
  transportes).
- **O controle virtual do Jogador 1 não morre.** Ele é do daemon, não do
  controle: o journal dela mostra o "Hefesto P1" criado às 20h08 de 05/08 e o
  controle físico chegando só às 22h35, sem nenhum controle virtual novo
  nascendo. **GRAU: MEDIDO.**

### O que não sobrevive, e é o pior caso que ela nomeou

O co-op pergunta *"é o mesmo jogador?"* comparando **o endereço do controle
dentro do Linux** — o número do nó de eventos, que muda a cada conexão — e
**não** a identidade. Caminho novo **derruba o jogador e o recria**; derrubar o
jogador destrói o controle virtual dele, e o ciclo seguinte cria um **novo**.
Para o jogo, isso é um controle sumindo e outro entrando.

**GRAU: SUSPEITA COM MECANISMO** para o gatilho *troca de transporte* — o
caminho de código foi lido ponta a ponta e fecha, mas a linha de log que ele
emite (`coop_player_node_changed`) **não aparece uma única vez** no journal dela,
e não há teste que a cubra.

**GRAU: MEDIDO** para o efeito irmão, com o mesmo mecanismo por outro gatilho: em
03/08, às 19h53, nasceu o controle virtual "Hefesto P2"; às 19h55 o nó de eventos
morreu; às 19h56 nasceu um "Hefesto P2" **novo**, instância diferente. O número
voltou; o aparelho, não.

**GRAU: MEDIDO** para o preço, e é uma medição desta casa, de 18/07, registrada
no próprio código: *"recriar os vpads no meio do jogo invalidou os handles do
jogo — a Steam nunca reabriu"*. Existe teste que trava essa regra
(`tests/unit/test_vpad_anti_recreate.py`).

### O terceiro fio, o mais silencioso

Há um caminho que só aparece na leitura ponta a ponta: o daemon abre e fecha a
conexão de escrita do controle **por chave**, e a chave é o endereço — que **não
muda** na troca de transporte. Resultado previsto: a conexão do nó **morto** é
preservada, o nó **novo** nunca é aberto, e **nenhuma linha aparece no journal**.
O input do Jogador 1 tem uma rede de segurança que reabre sozinha a cada 2
segundos; a **saída** daquele controle — barra de luz, gatilho adaptativo,
vibração — fica órfã, em silêncio.

**GRAU: SUSPEITA COM MECANISMO.** É a única coisa deste documento que eu não
consigo fechar sem a mão dela, e é o item que o protocolo abaixo mede.

### E o Pro Controller no cabo

Previsão forte: no cabo ele provavelmente deixa de ter endereço próprio e passa a
ser identificado por um endereço **sintético**, que muda com o transporte e nunca
é gravado — ou seja, **vira outra pessoa**, entra no fim da fila e renumera quem
estiver atrás dele. **GRAU: MEDIDO** para o 8BitDo (aconteceu em 03/08, está no
journal dela); **SUSPEITA COM MECANISMO** para o Pro genuíno, que no rádio tem
endereço real e no cabo nunca foi medido.

### A recomendação, hoje

**Enquanto isto não estiver medido e curado: não plugue o cabo no controle do
Jogador 2, 3 ou 4 no meio de uma partida que importe.** No Jogador 1 o risco é
menor — mas *menor* aqui é leitura de código, não medição. Se o controle
descarregar no meio do jogo, o gesto seguro é o que ela já faz por instinto:
plugar **antes** de entrar na partida.

---

## O que mudou no entendimento desta casa hoje

Esta casa errou **duas vezes seguidas** na mesma pergunta, em menos de 24 horas,
por dois motivos diferentes. As duas vezes o erro foi para o mesmo lado: **achar
que já sabia.**

### Erro 1 — 06/08, 22h40: o instrumento perguntou a coisa errada

Registrou-se *"dois aparelhos no mesmo player-3"* como defeito. A leitura tinha
tomado o **nome** de uma lâmpada (`player-3`, que quer dizer *"a terceira
lâmpada da barra"*) como se fosse **o número do jogador**. No DualSense o número
é o **padrão** das cinco lâmpadas, não o nome de nenhuma delas. Corrigido em
07/08, às 19h00, com nota datada — e **quem leu certo primeiro foi ela**, olhando
o plástico.

### Erro 2 — 07/08, 19h00: a decodificação foi corrigida, a causa não

A nota das 19h00 acertou ao derrubar a colisão e ao ler os cinco nós. Mas
atribuiu o número do controle físico ao kernel, nestes termos:

> *"O `hid-playstation` numera por ordem de registro e conta o nosso vpad como
> mais um DualSense: por isso o físico é empurrado para o 3 — GRAU: SUSPEITA COM
> MECANISMO, forte"*

**Isso está errado, e agora está medido.** Aquele 3 era **nosso**: era a nossa
fila contando dois controles de outra marca à frente do branco. A prova é que o
número mudou de **3 para 4** entre 19h00 e 19h10 **sem o aparelho ser
reconhecido de novo** — e o kernel só numera no instante em que o aparelho
aparece. **GRAU: MEDIDO.**

E cai junto a segunda afirmação daquela nota, a de que *"o vpad P1 concorda
consigo mesmo"*: o controle virtual **P2** se chama P2 e acende **5**. O acordo
do P1 era **sorte** — ele calhou de ser o índice 0 do kernel —, não desenho.
**GRAU: MEDIDO.**

### O que sobrevive daquela nota, inteiro

- a decodificação pela tabela canônica (foi ela que tornou esta medição
  possível);
- a queda da colisão "dois no jogador 3";
- a lição, que continua valendo e é reaproveitável: **nome de recurso do kernel
  não é valor de domínio.**

### A nota datada que ainda precisa ser levada ao arquivo da mãe

**Esta sprint escreve um arquivo só** — foi o mandato desta sessão. A correção
acima precisa aparecer **também** em
[LUGAR À MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md),
onde a afirmação errada mora, como **nota datada de 07/08**, sem apagar uma
linha do que está lá. O texto está pronto e é este:

> **NOTA DATADA — 07/08/2026, 19h10: a causa atribuída ao kernel era nossa.**
> A frase *"o `hid-playstation` numera por ordem de registro e conta o nosso
> vpad como mais um DualSense: por isso o físico é empurrado para o 3"* está
> **refutada**. O número do DualSense físico é calculado pela **nossa** fila
> (`identity.py`), que conta os controles de outra marca presentes à frente
> dele. **GRAU: MEDIDO** — às 19h00 o branco exibia 3 e às 19h10 exibia 4, sem
> que o aparelho fosse reconhecido de novo pelo kernel; quem recalcula a cada
> mudança na mesa é a nossa conta. Cai junto a afirmação de que *"o vpad P1
> concorda consigo mesmo"*: o vpad **P2** acende **5**, porque o contador do
> kernel conta os dois vpads e o 8BitDo. O diagnóstico completo, com as três
> contabilidades, está em
> [DUAS-CONTABILIDADES-01](2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md).

E a pergunta que aquela nota deixou explicitamente em aberto — *"o padrão do Pro
é resíduo nosso ou é do firmware?"* — **fechou hoje, por leitura**: é do driver
da Nintendo, que tem um contador próprio, separado do da PlayStation, e o
aparelho apareceu às **18h06:43**, depois da nossa última escrita (15h24) e
depois de a luz ser calada (15h27). O padrão de dois verdes é o do **segundo**
lugar na conta **dele**. E, mesmo que tivéssemos escrito, o número não bateria:
pela nossa conta o Pro exibiria **3** hoje, o que seriam **três** verdes.
**GRAU: MEDIDO.**

**Um detalhe que vale para a próxima leitura:** o quinto nó do Pro, que se chama
`blue:player-5`, **não é uma quinta lâmpada de jogador** — é a luz do botão HOME,
que o driver registra com esse nome. Contá-la como lâmpada de jogador é a mesma
armadilha de instrumento do erro 1. **GRAU: MEDIDO.**

---

## O achado de borda: dois endereços de teste dentro da fila real dela

Os lugares 1 e 2 da fila dela são `aa:bb:cc:00:00:01` e `aa:bb:cc:00:00:02` — a
faixa forjada que o próprio código nomeia como *"a faixa das fixtures"*, isto é,
**dado de teste dentro da configuração de produção dela**. Eles são restaurados a
cada início do daemon.

**GRAU: MEDIDO** para a presença e para o efeito. **SUSPEITA COM MECANISMO** para
a origem: o caminho mais provável é uma execução da suíte ou do backend de mentira
que não isolou a pasta de configuração — o cano foi curado em 05/08
([CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md))
e reforçado em 07/08
([BERÇO-DE-TMP-01](2026-08-07-BERCO-DE-TMP-01-a-suite-nao-suja-a-config-dela-suja-o-tmp.md)),
mas **o arquivo dela ainda carrega os dois**, porque a cura fecha a torneira e
não limpa o que já entrou.

O que eles **não** fazem: estragar número nenhum. A conta só olha para quem está
presente, e eles nunca estão. Foi justamente para isso que a regra de 25/07
existe.

O que eles **fazem**:

1. empurram todo controle real para o terceiro lugar em diante (é por isso que a
   reserva lida pelos controles de outra marca nasceu no 3);
2. consomem 2 das 16 vagas do teto da fila;
3. sobrevivem a reiniciar a máquina, por desenho.

**Eu não toquei no arquivo.** Limpar é gesto dela, e o gesto está no fim, em
*"O que fica ABERTO"*.

---

## PROTOCOLO TROCA-DE-TRANSPORTE-01 — o cabo no meio da partida

Executável por ela. **Custo: cerca de 15 minutos.** Tudo do meu lado é leitura;
o único gesto é o dela, com o cabo.

### Antes de qualquer coisa (P0)

1. **Suíte de testes parada.** Ela já sujou o journal e a configuração dela
   antes, e este protocolo lê os dois.
2. **Copiar a configuração dela para um lugar seguro, com a data no nome** — o
   arquivo `controllers.json` da pasta de configuração. A medição pode mexer na
   fila, e a fila dela já está suja (ver o achado de borda).
3. **Eu fotografo o ANTES:** o endereço e a identidade de todos os nós de
   controle, a lista de dispositivos de entrada, o estado completo do daemon
   (quem é primário, qual transporte, quais números) e a lista de controles
   virtuais vivos.

### O estado de partida

Quatro controles no rádio, co-op ligado, os dois controles virtuais no ar.
**Com jogo aberto só se ela aceitar o risco** — o pior caso é perder o
personagem. Sem jogo, a tela do Hefesto e o journal respondem tudo, menos
*"o jogo perdeu o controle"*, que é a única pergunta que exige o jogo.

### O gesto dela — um de cada vez, 60 segundos entre eles

1. plugar o cabo no DualSense **secundário** (é o caso dela: descarregou no meio);
2. tirar o cabo;
3. plugar o cabo no DualSense **primário**;
4. tirar o cabo;
5. plugar o cabo no **Pro Controller**.

### O contraste que decide quase tudo

**Com o cabo dentro, existem DOIS nós com o mesmo endereço, ou o do rádio
sumiu?** Uma linha de leitura responde, e é ela que separa os ramos.

### As previsões, e como cada uma pode ser derrubada

| ramo | o que aconteceria | previsão | o que a derruba |
|---|---|---|---|
| **1** — os dois links coexistem (é o que a nossa página de solução de problemas afirma) | aparece um segundo nó com o mesmo endereço | o co-op escolhe o nó de **menor** número: se o do cabo for menor, o Jogador 2 morre e renasce; se for maior, **nada** acontece e o cabo só carrega | o nó do cabo ter número menor **e** o jogador **não** ser derrubado |
| **2** — o rádio cai quando o cabo entra | o controle troca de nó | o lugar e o número **se mantêm**; o controle virtual do secundário **morre e renasce** (ela perde o personagem); a **saída** daquele controle fica muda, sem log | a barra continuar obedecendo ao perfil depois da troca, ou aparecer erro de abertura no journal |
| **3** — cabo no **primário** | — | se o primário for **reeleito** no instante do cabo, a chave mudou entre transportes e caímos no conflito já medido na COOP-QUE-NÃO-DESMONTA-01; se **não** for, a chave é a mesma e vale o ramo 2 | é o ramo que **decide entre as duas causas**, e a leitura é de uma linha só |
| **4** — Pro Controller no cabo | — | previsão forte: ele vira **outra identidade**, entra no fim da fila e renumera quem estiver atrás | o endereço dele no cabo continuar sendo o mesmo do rádio; aí o Pro está a salvo |

### O que eu observo (leitura pura, nenhuma escrita)

O journal filtrado pelos eventos de co-op, de criação de controle virtual, de
eleição de primário, de reabertura de nó e de atribuição de lugar na fila; os
endereços dos nós antes, durante e depois; a lista de dispositivos de entrada; o
estado completo do daemon; e a foto da tela dela, para os números que ela vê.

### Cabe junto com a sessão de 06/08?

**Cabe, como item novo do mesmo protocolo**, não como sessão própria, com duas
condições: (a) rodar **depois** dos itens que replugar contamina, reusando a
mesma cópia da configuração feita no P0 — e o IDENTIDADE-DUPLA-01 mede o mesmo
fenômeno pelo outro lado, então encostar um no outro sai quase de graça; (b) só
vira sessão própria se ela quiser medir **com jogo aberto**, porque aí o critério
de aceite é *"o personagem sobreviveu?"* e o pior caso é perder a partida.

**E o que não precisa dela:** a pergunta *"o controle virtual do secundário morre
quando o nó muda?"* fecha inteira numa bancada de relógio virtual — a `E4` da
COOP-QUE-NÃO-DESMONTA-01, que ainda não existe. Se a bancada nascer primeiro,
este protocolo encolhe para os ramos 1 e 4, que são os únicos que exigem plástico
de verdade.

---

## Os três protocolos curtos — o que falta medir

Cada um fecha uma pergunta que a leitura sozinha não fecha. **Todos exigem
mexer**, e por isso são dela. **GRAU de todos: SEM PROVA** até que ela rode.

**PROTOCOLO A — a lâmpada do controle virtual é 100% do kernel?**
Com os controles como estão, deixar as mensagens do kernel rolando numa aba e,
na outra, desligar e religar **um** controle de outra marca. O driver da Nintendo
imprime o número que atribuiu, no instante em que atribui. Se o número impresso
bater com a barra do Pro e **não** houver nenhuma escrita nossa no journal, está
fechado.

**PROTOCOLO B — o padrão do Pro é do firmware, sem sombra de dúvida?**
É o experimento que a nota das 19h00 pediu e ninguém fez: **parar o daemon**,
religar o Pro do zero e ler os nós de LED dele. Se der o mesmo padrão com o
daemon parado, o assunto morre. Minha medição de hoje já favorece esse resultado,
mas por leitura, não por experimento.

**PROTOCOLO C — o cruzamento, de olho, e a palavra final é dela.**
Com o co-op ligado, apertar um botão no plástico **branco** e conferir num
testador de controle que quem se mexe é o **Jogador 1** — enquanto o branco
acende **4**. É a prova de olho do defeito da resposta 3, e é ela quem fecha.

---

## O que isto pede, e de quem é (PROPOSTA — nada tocado)

1. **O cruzamento (resposta 3) precisa de sprint própria.** A cura provável é
   fazer o número que a lâmpada acende e o nome que o jogo mostra saírem da
   **mesma** conta — hoje saem de duas. Isso mexe no co-op e no registro de
   identidade ao mesmo tempo, e **não** é mudança que se entrega sem o olho dela
   na mesa.
2. **O teste que morde já tem meia casa pronta.** O invariante das duas metades
   está em `tests/unit/test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py`; o
   que falta é o caso de **dois** DualSense com o co-op ligado, que é exatamente a
   mesa dela de hoje.
3. **O nó contra a identidade no co-op (resposta 4)** já tem dono declarado: a
   `E1` da COOP-QUE-NÃO-DESMONTA-01, que continua sem uma linha escrita.
4. **A mesa inteira chegar ao jogo** continua sendo as entregas `E3`/`E4` da
   LUGAR À MESA-01, **atrás da MÁSCARA-01**, por decisão dela. **Nada aqui
   antecipa isso**, e quem retomar não deve começar a adoção.

---

## O que fica ABERTO

1. **A decisão dela sobre a ordem.** A fila hoje guarda a ordem da **primeira
   vez**; ela descreveu a ordem da **sessão**. Mudar isso revoga três decisões
   medidas de 25/07 e reabre a queixa que elas curaram (*"nunca sei o que é o
   quê"*). **É dela a palavra.** Se ela quiser, a saída provável não é trocar uma
   pela outra, e sim um gesto explícito de *"reordenar a mesa agora"* — mas isso
   é desenho, e desenho novo passa por ela.
2. **O cruzamento não tem cura escrita.** Está diagnosticado e medido; nenhuma
   linha de código foi tocada nesta sessão.
3. **A nota datada ainda não está no arquivo da mãe.** O texto está pronto na
   seção da honestidade, e precisa ser colado em LUGAR À MESA-01, **sem apagar
   nada**.
4. **Os dois endereços de teste continuam na fila dela.** Limpar é gesto dela, e
   o custo de não limpar hoje é baixo (dois lugares e duas vagas). Eu não toquei
   no arquivo.
5. **Os quatro protocolos** — o da troca de transporte e os três curtos — estão
   por rodar. Nenhum deles cabe em leitura pura.
6. **O que acontece com o Pro Controller no cabo continua SEM MEDIÇÃO.** A
   previsão é forte e vem de um aparelho vizinho; o Pro genuíno no cabo nunca foi
   visto por esta casa.
7. **O terceiro fio da resposta 4** — a saída do controle ficando muda depois da
   troca de transporte, sem uma linha no journal — é **SUSPEITA COM MECANISMO** e
   é o achado mais silencioso deste documento. Se ele for verdade, ele já
   aconteceu com ela e ninguém percebeu, porque não há como perceber.
