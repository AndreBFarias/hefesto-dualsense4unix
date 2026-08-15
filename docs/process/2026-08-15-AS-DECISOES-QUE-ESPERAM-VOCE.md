# AS DECISÕES QUE ESPERAM VOCÊ

- **Escrito em:** 15/08/2026, na branch `restauro/inicio-da-sessao`, com a mesa de
  quatro controles montada para o ENSAIO 2+2. **Nenhum arquivo de produto foi
  tocado para escrever esta página.**
- **Para que serve:** juntar numa página só as **21 perguntas numeradas** (D-13 a
  D-33) que estão espalhadas por seis documentos, mais as **quatro antigas sem
  número**. Nada aqui é novo — é o mesmo conteúdo, condensado para caber em
  vinte minutos.
- **O que eu NÃO faço aqui:** decidir no seu lugar. Toda decisão tem
  recomendação minha, e **nenhuma foi tomada**.

---

## O placar, e o relógio

| tipo | quantas | quanto tempo |
|---|---|---|
| **Travam CÓDIGO ou ENTREGA** — sprint parada, ou código já escrito esperando | **15** | 12 min |
| **Travam MEDIÇÃO** — bancada com você, e nada anda sem a autorização | **5** | 5 min |
| **Nome / vocabulário** | **1** | 1 min |
| **As quatro antigas, sem número** (de 11-12/08) | **4** | 2 min |
| **A que nasceu enquanto esta página era escrita** (a máscara) | **1** | 1 min |

**A página inteira: cerca de 20 minutos.** A **D-30 come 5 deles sozinha** e
merece — ela é a única que reverte uma medição sua anterior.

### Se você só tem cinco minutos, decida estas três

1. **D-30** — o número do jogador sai da ordem em que você conecta hoje, ou do
   lugar gravado por MAC? **Tem código escrito e não commitado do lado que você
   disse que não queria.**
2. **D-19** — "navegar a janela do Hefesto" e "comandar o PC" são a mesma coisa
   ou duas? **A resposta "duas" derruba de 960 a 1200 minutos de trabalho.**
3. **D-31** — autoriza a bateria de escritas da escada? **Sem ela, seis ensaios
   de 1 h 25 não saem do papel, e o áudio por rádio para onde está.**

---

# PARTE 1 — as que travam código ou entrega

## D-30 — o número do jogador segue a ordem em que você conecta hoje, ou o lugar que o produto gravou por MAC?

> **Esta é a decisão mais cara da página, e é a única que reverte uma medição
> sua.** Ela está longa de propósito: sem as duas medições lado a lado, você
> decidiria sem saber que está desfazendo a si mesma.

### As duas medições, lado a lado

| quando | quem mediu | o que se mediu | o que se decidiu |
|---|---|---|---|
| **23/07 (R-15)** | esta casa, no seu aparelho | numerar por ordem de wake **trocava cor e número de dono**: desligar os dois DualSense e religar na ordem invertida devolvia o 1 ao que voltasse primeiro. E entre expirar e reatribuir, o piso que os externos leem valia 0 — a queixa **"dois player 1, dois player 2"** | **arrancar** a renumeração por ordem de conexão |
| **25/07 (R-23)** | esta casa | o número não sobrevivia ao boot: **todo reboot renumerava por ordem de conexão**, e bastava reiniciar o daemon. A queixa foi sua: *"ao abrir os jogos ou o perfil, os controles se reenumeram e nunca sei o que é o quê"* | **gravar** a fila por MAC, que atravessa boot |
| **12/08 (você)** | você | — | *"nada de macs, nada de personalização por controle"* |
| **15/08 03:54 (você)** | você, com os quatro resetados de fábrica e re-pareados na ordem vermelho, azul, branco, roxo | saíram **vermelho 1, branco 2, roxo 3, azul 4** | *"deve ser lembrado por ordem de conexão naquele momento apenas. **Não uma imagem fixa salva por mec**"* |

O motivo está escrito no próprio código, em
`daemon/subsystems/identity.py:14-22` (R-15) e `:23-34` (R-23). **O que você
pediu em 15/08 é literalmente o comportamento que a R-15 arrancou em 23/07.**

**E há uma segunda leitura, que é a que eu não quero que se perca:** a R-23
curou *"o número muda sozinho"*. Você não está pedindo isso — você está pedindo
*"o número segue a ordem que EU escolhi ao conectar"*. **As duas coisas só
colidem num caso: o controle que cai e volta no meio da partida.** Fora dele,
não há conflito nenhum.

E a fila gravada por MAC é, ela mesma, a *"personalização por controle"* que
você vetou em 12/08. **Nesse ponto a sua decisão de 15/08 não contradiz você —
ela repete você.**

### As três respostas

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **(a) só a ordem do momento** | você conecta vermelho, azul, branco, roxo e a mesa mostra 1, 2, 3, 4 nessa ordem — nas guias, na lâmpada do plástico e no rótulo. **Um controle que cai e volta pode virar outro jogador no meio do jogo** | 90 min (E2) | volta a queixa de 25/07 no caso do replug |
| **(b) a ordem do momento, CONGELADA quando a mesa fica estável** | igual à (a) no que você viu hoje. **A diferença só aparece no replug: quem volta recupera o número que tinha** | 90 min (E2) + a regra de congelamento | nada — o gravado continua existindo como desempate |
| **(c) continua como está** | nada muda; a sua frase das 03:54 fica sem efeito. Para reordenar, o gesto **"Renumerar agora"**, que hoje só existe no IPC e **não tem botão em aba nenhuma** | 40 min (E3, só o botão) | você continua sem controle sobre a ordem, exceto por gesto |

**O que trava:** a
[ORDEM-DE-CHEGADA-01](sprints/2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md)
inteira (E2 e E3), **e a cura MESA-CHEIA-12 que está escrita na árvore e não
commitada** — ela uniu a lâmpada e o rótulo **na fila gravada**, que é o lado B
da sua frase. A união está certa e não se desfaz; o que se decide aqui é **em
qual das duas filas** eles ficam unidos.

**Minha recomendação: (b).** Ela entrega o que você pediu no caso que você viu
esta madrugada, e paga zero do preço que a R-15 e a R-23 mediram — porque a
fila gravada não é destruída, vira desempate.

**Três coisas que NÃO estão nesta decisão, e não vou fingir que estão:**

- *"a nossa ordem deveria sobrescrever a parte da steam"* — terceira metade da
  sua frase. **Não medida nesta sessão.** Frente própria, sem promessa;
- se os quatro `rank` de hoje nasceram nesta sessão ou antes dela — o mecanismo
  está provado, a data de cada `rank` não;
- o comportamento com Pro Controller ou 8BitDo na mesa: a fila é a mesma, e
  nenhuma entrega foi conferida contra um externo ligado.

---

## D-19 — "navegar a janela do Hefesto" e "comandar o PC" são a MESMA coisa ou DUAS?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **duas coisas** | a aba Navegação ganha duas seções: *"Comandar o PC"* (as duas colunas de hoje, intactas) e *"Navegar esta janela"*. **Os quatro controles navegam a janela ao mesmo tempo** | a rota cara **cai**: de 960 a 1200 min economizados (estimativa) | nada — a D-10 continua valendo inteira para comandar o PC |
| **a mesma coisa** | a aba fica como está, e a navegação tem **um dono por vez** | 0 agora | os quatro navegarem juntos |

**O que trava:** as entregas 3.4, 3.5 e 3.6 da onda 3 (o verbo dos quatro
botões, o badge de quem navega, e o botão que não chega ao jogo).

**Recomendação: duas coisas** — navegar a janela **não passa por uinput**, então
a objeção dos quatro cursores virtuais, que era o que sustentava os 960-1200
min, não se aplica a essa metade.

---

## D-16 — a cor do plástico é do PERFIL ou da PEÇA?

**Ela contradiz o item 3 do seu pedido** (*"tudo salvo dentro do perfil ativo"*),
e a contradição é real.

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **da PEÇA** (arquivo por endereço) | a cor do plástico é a mesma em todo perfil. Trocar de perfil **não** repinta o desenho do controle | baixo — o arquivo já existe e lista os seus quatro | a cor variar por jogo |
| **do PERFIL** | **trocar de perfil repinta o plástico na tela** — o mesmo controle vermelho vira azul ao abrir outro jogo | baixo | nada |

**O que trava:** onde a cor mora — e portanto a entrega 3.1 da onda 3.

**Recomendação: a PEÇA**, com um preço na mesa que eu não posso esconder:
**guardar a cor por endereço é, por definição, personalização por MAC — o que
você vetou em 12/08.** Se a **D-15** for pelo caminho (b), a cor sai do próprio
aparelho e **não existe arquivo por MAC nenhum**, e esta decisão perde o preço.

> **Atenção — esta decisão está sendo CITADA como se você já a tivesse tomado.**
> O índice da leva, na D-15, escreve *"D-16 já decidiu que é da PEÇA"*. **Você
> nunca respondeu.** Quem decidiu fui eu, em prosa, e a citação virou fato.

---

## D-15 — que cor é "a cor física dele"?

São duas coisas, e você usou a palavra "física".

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **a cor VIVA da lightbar** | chega a 2 Hz e é só pintar. **Dois controles com a mesma luz acesa ficam com guias iguais** | baixo | distinguir dois controles da mesma cor de luz |
| **a cor do PLÁSTICO** | cada guia com o colorway de fábrica, sempre, independente da luz | ver os três caminhos abaixo | — |
| **as duas, em superfícies diferentes** | a viva no **miolo** e o plástico no **contorno**: *"que luz está acesa?"* e *"que peça é essa na minha mão?"* | soma dos dois | — |

**E se for o plástico, três caminhos, com preço diferente:**

| caminho | o que custa | o que entrega |
|---|---|---|
| **(a) não fazer** | zero risco. Você escolhe a cor de cada controle na interface **uma vez** | a tela pinta certo hoje, e nunca escreve nada no aparelho |
| **(b) ler do aparelho, POR CABO** | é o caminho **provado**, e ainda assim é **escrita na família de comandos de fábrica** — a mesma em que `[1,1]` reseta e `[12,1,...]` grava calibração na NVS. Não há desfazer | a cor sai do aparelho, sem você digitar nada — inclusive de controle comprado depois |
| **(c) tentar POR RÁDIO** | território **não demonstrado**: some ao risco da escrita o transporte que já deu timeout e resposta trocada no censo de hoje | o mesmo de (b), sem cabo — se funcionar |

**O que trava:** a entrega 3.1 da onda 3 e a sprint `UNIDADE-COR-01`, aberta e
não começada desde 10/08.

**Recomendação: (a) agora e (b) depois** — a tela sai hoje sem nenhuma escrita
de fábrica no caminho crítico de um recurso visual.

---

## D-25 — o alto-falante por rádio nasce LIGADO ou opt-in? E quem escolhe fone x alto-falante?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **nasce ligado** | nada de novo para ligar: funciona | **custa cerca de 3x mais rádio que o microfone** (~27 kB/s contra ~8), e com quatro na mesa **esse orçamento nunca foi medido** | nada |
| **opt-in** | um interruptor novo por controle | zero de rádio até alguém ligar | contraria a sua regra de 08/08: *"nada à mão, nada opt-in"* |

E o segundo lado, que é outra pergunta dentro da mesma: **com o fone plugado no
controle, quem decide?** O protocolo separa por um byte (`0x13` alto-falante,
`0x16` fone), e o firmware de referência tem três modos: segue o jack sozinho,
trava no fone, ou desliga.

**O que trava:** o desenho do produto para o alto-falante por rádio — e, com
ele, metade do que você pediu de SFX.

**Recomendação: nasce ligado, com o orçamento de rádio medido ANTES de sair** —
opt-in contraria a sua regra de 08/08, e desligado por padrão é a mesma coisa
com outro nome. E o **Hefesto segue o jack sozinho**, com o travamento como
ajuste no perfil de cada controle para quem quiser.

---

## D-26 — o SFX do Sackboy sai do ALTO-FALANTE do controle ou do FONE plugado nele?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **do fone** | uma escolha de rota por controle, na aba de som | **boa parte já existe**: o registrador de rota é por controle, endereçado por `uniq`, e está implementado | nada |
| **do alto-falante por rádio** | o mesmo controle, sem fone, tocando SFX | é o EXP-SPK-01 inteiro — hoje o **E-5** da escada, e ele **só começa depois** que os ensaios de payload disserem onde o formato mora | nada |

**E o nome na tela:** *"SFX do jogador 1"*, *"Alto-falante do controle 1"*, ou
outro? O léxico da casa hoje tem **"Controle N"** (a peça) e **"jogador N"** (o
lugar na mesa). **Eu não sei qual dos dois é o certo aqui, e você já me corrigiu
que nome que não deriva do léxico existente é sinal de conceito errado.**

**O que trava:** a metade de SFX da
[SOM-DE-CADA-JOGADOR-01](sprints/2026-08-15-SOM-DE-CADA-JOGADOR-01-o-botao-que-nunca-funcionou-com-a-mesa-cheia.md)
(as outras duas entregas dela não dependem de nada e podem andar hoje).

**Recomendação: o fone primeiro, o alto-falante depois** — o caminho do fone já
está escrito, e entrega som por jogador nesta semana; o outro depende de um
formato de payload que ninguém identificou.

---

## D-23 — a tabela de navegação por controle entra no perfil?

**Isto reabre uma decisão sua de 10/08:** o perfil **proíbe** mouse e atalhos de
teclado por unidade, e a justificativa escrita era a dívida do leitor único.

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **reabrir só a tabela de navegação** | cada controle com a sua tabela de botões, no perfil. Mouse e teclado continuam fora | médio (estimativa) | nada |
| **manter fechado** | um único mapeamento de navegação para todos | zero | você mudar o botão só de um controle |

**Medido hoje:** a dívida do leitor único **caiu pela metade** — o co-op já cria
um leitor por endereço, e o `state_full` já publica os botões de cada controle
separadamente. **Mouse e teclado continuam esbarrando no cursor único e no foco
único do PC**, que seguem sendo um só.

**O que trava:** o desenho da aba Navegação por controle (entrega 3.4).

**Recomendação: reabrir só a tabela de navegação** — é literalmente o que você
deixou aberto na D-10 (*"a parte que aguenta por jogador é a tabela de
atalhos"*).

---

## D-22 — com o jogo aberto atrás, o X que escolhe na tela também chega ao jogo?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **roubado, só os quatro botões** | você aperta X para escolher na tela e **o seu personagem não pula**. Os analógicos continuam indo ao jogo, então ninguém trava andando | baixo — há uma linha só para isso no co-op | nada |
| **não roubado** | escolher na tela **também** age no jogo | zero | usar a janela com o jogo aberto sem efeito colateral |

**E junto:** os outros três seguem jogando normalmente, ou tudo congela junto?

**O que trava:** a entrega 3.6 da onda 3.

**Recomendação: roubado, só os quatro botões, e só do dono da navegação** — a
supressão é por jogador e cabe numa linha; congelar os quatro puniria quem não
pediu nada.

---

## D-17 — nos botões 1 2 3 4: a cor de quem OCUPA o número, ou a do escolhido?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **de quem ocupa** | os quatro botões viram **a mesa inteira em quatro cores**, e trocar o número **troca as cores de lugar** — confirmação visual do gesto | mesmo widget | nada |
| **a do escolhido no cabeçalho** | os quatro botões ficam **da mesma cor** | mesmo widget | ler a mesa pelos botões |

**O que trava:** a entrega 3.2 da onda 3.

**Recomendação: de quem ocupa** — é mais informação pelo mesmo pixel.

---

## D-18 — a borda pode ficar SÓ com a identidade?

Hoje **borda roxa = selecionado** em toda a interface.

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **sim, a seleção vira anel por dentro** | a borda passa a dizer **quem é**, e a seleção vira um anel de 2 px por dentro — **medido: não muda um pixel de tamanho** | baixo | nada |
| **não, a seleção fica só com o fundo** | marcado e não marcado se separam por **1,28:1**, que é pouco para qualquer olho | zero | ler a seleção com o canto do olho |

**Duas de borda vêm junto:** (a) no **alto contraste** do sistema, a borda
colorida some ou vence? — **eu deixaria o alto contraste vencer**, e o preço é
que nesse modo os quatro ficam iguais de novo; (b) os controles **externos**
ganham borda? A D-7 já disse que *"cada player"* inclui quem não é DualSense,
mas **não medi se existe cor por unidade para eles**.

**O que trava:** a entrega 3.1 da onda 3, junto da D-15.

**Recomendação: sim, anel por dentro** — as duas informações param de disputar o
mesmo pixel, e o contraste melhora nas duas.

---

## D-20 — o R1 já tem dono: "próxima aba" ou Alt+Tab?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **dois significados, decididos pelo foco** | dentro da janela do Hefesto o R1 é "aba"; fora, é Alt+Tab. **Isso precisa estar dito na tela** | baixo | nada |
| **"aba" em todo lugar** | o Alt+Tab **perde o botão dele** | zero | usar o controle como teclado para trocar de aplicativo |

**O que trava:** a entrega 3.4 da onda 3.

**Recomendação: dois significados pelo foco** — é o mesmo R1 que em 29/07
trocava de aplicativo dentro do jogo, e ninguém quer isso de volta.

---

## D-21 — o verbo do círculo, e a volta do carrossel

**"Bola pra desescolher"** pode ser três coisas: **desmarcar** o que está
selecionado, **voltar** (devolver o foco à tira de abas), ou **sair** (fechar a
janela). No PS5 o círculo é sair.

E: **R1 na última aba para, ou dá a volta para a primeira?** No PS5 o carrossel
dá a volta; num aplicativo de desktop, normalmente para.

**O que trava:** a entrega 3.4 da onda 3.

**Recomendação: círculo = voltar à tira de abas** (fechar a janela por engano é
caro, desmarcar é raro), **e o R1 para na última** — é aplicativo de desktop, e
dar a volta esconde onde a lista acaba.

---

## D-29 — duas dívidas medidas de raspão, e caras se ficarem sem dono

**1. O grab do controle primário está FALHANDO agora.** Medido:
`primary_grab_state="failed"`, `[Errno 16] recurso ocupado` no
`/dev/input/event265`. **Com o vpad de pé, isso é input DOBRADO no jogo para o
P1** — o físico e o virtual chegam juntos.

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **abrir frente própria** | o P1 para de receber comando dobrado | não estimado | nada |
| **deixar na fila** | continua como está | zero | — |

**2. Os `/dev/hidraw` dos DualSense por BT estão `root:root` 0600, sem ACL.**
**Isto já foi respondido pela medição de 15/08 e ninguém marcou:** é **de
propósito** — quem tira a ACL é o próprio Hefesto, em
`broker/hidraw_broker.py:416-427` (`hide`), para esconder o físico do Steam
Input. A regra udev **pegou** (`CURRENT_TAGS=:seat:uaccess:`). O que sobra não é
decisão de comportamento, é **o que fazer com a linha 0660 da regra**, que é
resto de uma era anterior.

**Recomendação: (1) abrir a frente — é defeito ao vivo no seu jogo, não questão
de gosto; (2) não é decisão sua, é fato medido — a linha da regra sai, com o
porquê escrito ao lado.**

---

## D-13 — as duas colunas do mapa dizem coisas diferentes com nomes parecidos

`confianca` tem **98 células** `medido` e é ganhável por um teste unitário que
afere **o nosso próprio byte**. `grau` tem **15 células** `O APARELHO OBEDECEU`
e exige ensaio de bancada. **A segunda é a que concorda com você.**

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **`confianca` vira derivada do `grau`** | o `specs.html` mostra **uma coluna** de confiança, e o mapa **encolhe** | alto (estimativa: CSV, portão, `specs.html` e testes) | nada |
| **ficam as duas, com o cabeçalho explicando em uma linha** | duas colunas, com uma frase dizendo que uma mede o **código** e a outra mede o **aparelho** | baixo (estimativa) | a confusão continua possível para quem não ler o cabeçalho |

**O que trava:** o formato do `docs/data/mapa-controles.csv` e do `specs.html`
que ele gera — e portanto as entregas 1.1 e 1.3 da onda 1.

**Recomendação: uma coluna só** — manter dois nomes que se confundem foi o que
fez o mapa mentir **sem ninguém mentir**.

---

## D-14 — rebaixar seis células de `medido` para `inferido-do-codigo`?

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **rebaixar** | o censo do portão sai de **48** para **42** afirmações fortes. **O produto não muda uma linha** | baixo | nada — repromover exige ensaio |
| **manter** | o mapa continua dizendo 48 | zero | o portão `medido-sem-quem-provou` fazer sentido |

**O preço, e é real:** o mapa passa a parecer que sabe **menos** do que ontem,
mesmo sabendo que algumas dessas coisas provavelmente funcionam (o volume do
alto-falante no cabo, por exemplo).

**O que trava:** a entrega 1.2 da onda 1.

**Recomendação: rebaixar** — é a regra da casa, e o mapa é a sua memória externa:
memória que exagera é pior que memória curta.

---

# PARTE 2 — as que travam medição

## D-31 — a bateria de escritas da escada: autoriza?

Você já autorizou, nesta madrugada, escrever output report por rádio com o
daemon parado — foi assim que se mediu que o firmware **executa** o `0x32` e o
`0x39`. O que os seis ensaios pedem agora é **mais do mesmo, em série**: da
ordem de 50 a 60 escritas de output, todas com CRC válido e tamanho declarado
pelo descritor do próprio aparelho, mais uma rajada de 3 s a 50 Hz (cerca de 150
pacotes) **só** no ensaio final.

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **a série inteira** | você vê a lightbar obedecer degrau a degrau, e no fim ouve (ou não) o alto-falante | **1 h 25 de bancada com você presente** | nada |
| **só o que NÃO manda payload** (E-1, E-2, E-3, E-6) | a mesma coisa, sem o teste de som | **45 min** | saber se sai som nesta rodada |
| **só o E-4** | nada na tela — é leitura pura | **10 min** | tudo o mais |

**O que trava:** a
[ESCADA-QUE-RESPONDE-01](sprints/2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
inteira, e com ela o item 4 do seu pedido.

**A frase honesta sobre o risco, e ela não é "nulo":** é a **mesma classe de
escrita que a ponte do microfone faz aqui desde 25/07**, nada toca a família
`0xF0`-`0xF7` da atualização de firmware — e o que os bytes excedentes acionam é
justamente o que não sabemos.

**Recomendação: a série inteira, com você presente.** O E-1 sozinho já responde
*"onde o payload mora"*, e parar antes dele deixa a leva parada por semanas.

---

## D-32 — o `0xF6` e a família `0xF0`-`0xF7`: até onde?

O `0xF6` é um FEATURE de 546 bytes que **só existe no rádio**, do mesmo tamanho
de payload do OUTPUT `0x39`. Lido sem estímulo, veio **vazio** nos quatro. **Ele
mora na família por onde o firmware é atualizado.**

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **ler o `0xF6`, e só ler** | nada — leitura pura | 10 min (E-4) | saber o resto da família |
| **ler a família inteira, só leitura** | nada | ~15 min (estimativa) | nada |
| **escrever (`SET_FEATURE`) em qualquer um** | — | — | **eu não faço isso sem a sua palavra explícita, e recomendo que você não a dê agora** |

**O que trava:** o E-4 da escada — o único ensaio que roda **sem** a D-31.

**Recomendação: ler a família inteira, só leitura, nunca escrever** — ler é
grátis; escrever nessa família, não.

---

## D-28 — o ensaio do canal 3, às cegas

**São 5 a 10 minutos com o controle na sua mão, no cabo, sem fone plugado.** Um
tom de 440 Hz num canal por vez, e você diz, para cada um: **OUVIU**, **SENTIU
na mão**, ou **nada**. Depois repete com o fone.

| o que você sentir no canal 3 | o que fica provado |
|---|---|
| sentiu vibração fina e não ouviu | canais 3-4 **são** os motores, e o modelo do mapa ganha |
| ouviu o tom pelo alto-falante | **o canal 3 é saída de som e você está certa** |
| nem ouviu nem sentiu, no volume máximo | o `chmap` declara quatro canais e **não há transdutor atrás de 3-4** |

**Eu quero que você diga o que percebeu ANTES de eu dizer o que eu esperava** —
se eu contar a expectativa primeiro, contamino a única medição desta frente que
depende do seu corpo.

**E uma de borda, que é decisão de verdade:** o acelerômetro passou a ser medido.
**Quer o número na tela, ou basta que ele chegue ao jogo pelo vpad (que já
chega)?**

**O que trava:** a metade de SFX da SOM-DE-CADA-JOGADOR-01 e a célula do canal 3
no mapa — hoje **os dois modelos estão empatados em zero prova**.

**Recomendação: fazer, e o número do acelerômetro fica no diagnóstico, não na
aba principal** — é onde as medições já moram, e não gasta pixel de quem só quer
jogar.

---

## D-27 — o censo de cor, e as portas que eu deixei fechadas de propósito

**São três coisas, e uma delas já aconteceu:**

1. **Quantos DualSense você tem, e qual é a cor de cada um?** Sem o rótulo o
   censo não decide nada — **eu leio os bytes, só você lê o plástico.** Custa
   dois minutos e é o que destrava a D-15.
2. **Posso sondar os reports `0x80` a `0x83`?** — **já foram sondados**, no
   censo dos dezessete de 15/08, e devolveram constante idêntica nos quatro. A
   pergunta que sobra não é essa: é a **escrita** do `SET_FEATURE 0x80`, e essa
   é a D-15.
3. **Se o censo der "nenhum byte correlaciona com a cor"** — e **deu**, em
   15/08 —, a casa registra isso como **amostra fechada de quatro unidades**, ou
   eu procuro uma quinta emprestada antes de escrever?

| resposta ao item 3 | o que muda | custo | o que fica impossível |
|---|---|---|---|
| **amostra fechada de quatro** | a casa escreve, com data e tamanho de amostra, *"quatro unidades, quatro cores, nenhum byte correlaciona"* | zero | nada — é reversível com uma quinta unidade |
| **procurar uma quinta** | a afirmação fica em suspenso até aparecer | indefinido | fechar a frente |

**Recomendação: amostra fechada de quatro, escrita com data e tamanho** — a
resposta útil já existe, e o caminho da cor não passa por esses reports mesmo.

---

## D-24 — autoriza o EXP-SPK-01, que escreve no controle?

> **Esta pergunta envelheceu em horas, e eu recomendo DERRUBÁ-LA em vez de
> respondê-la.** Ver a Parte 5.

Ela nasceu dizendo *"é a única proposta desta leva que escreve no aparelho"*.
**Isso deixou de ser verdade por decisão sua**, na madrugada de 15/08: você
autorizou parar o daemon e escrever output reports por rádio, e a classe de
escrita já foi exercida sem nada quebrar. **O que restava dela virou a D-31**,
que separa taxa e conteúdo do que já foi feito.

**O que sobra de verdade é operacional, e não é decisão de produto:** prefere que
eu **pare o daemon** antes, ou que eu use o **broker**?

**Recomendação: responda só a D-31; e a escrita vai com o daemon parado** — é o
caminho já exercido esta madrugada, e o broker acrescenta um segundo dono do nó
sem acrescentar segurança.

---

# PARTE 3 — nome e vocabulário

## D-33 — o nome da falácia gêmea

Esta casa nomeou em 14/08 a **falácia do perfil ausente** (*não achei, logo não
existe*), e o nome se pagou: foi ele que fez a palavra "impossível" cair da
célula do áudio por rádio.

A gêmea nasceu com o achado de 15/08, e eu proponho **FALÁCIA DO CANAL QUE
RESPONDE**: *respondeu, logo faz o que eu queria*.

```
   FALACIA DO PERFIL AUSENTE      nao achei    ->  logo NAO EXISTE
   FALACIA DO CANAL QUE RESPONDE  respondeu    ->  logo FAZ O QUE EU QUERIA
```

| resposta | o que muda | custo | o que fica impossível |
|---|---|---|---|
| **aprova** | vira vocabulário da casa, como o outro virou | zero — já está escrito em dois documentos | nada |
| **veta** | um `sed` em dois arquivos, e a forma de erro fica sem nome | 5 min | — |

**Recomendação: aprovar** — o nome deriva do léxico que já existe, e **duas
frentes chegaram a ele separadamente na mesma noite**. Forma de erro sem nome
volta a acontecer.

---

# PARTE 4 — as quatro antigas, sem número

Estão em
[ONDE-PARAMOS](2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md),
seção 3, e nenhuma foi respondida.

| # | a pergunta | o que trava | recomendação |
|---|---|---|---|
| **V-A** | **Quando o produto vira `1.0.0`?** O critério que você deu é *"ver funcionando num PC novo"* | a release, e as fotos que a acompanham | **não decidir hoje** — os três módulos DKMS nunca foram construídos contra outro kernel, e sem isso "PC novo" é achismo |
| **V-B** | **De onde veio a arte dos SVG?** Você não lembra, e os desenhos foram editados aqui — fica como **risco aberto de licença** | nada hoje; trava a distribuição pública | **redesenhar os três do zero** a partir dos seus aparelhos, sem pressa. É o único caminho que fecha o risco |
| **V-C** | **O que *"nada de MAC, nada de personalização por controle"* (12/08) implica no CÓDIGO?** Foi aplicado à **sua configuração**; o override por peça, a `PERFIL-01` e a `POR-UNIDADE-01` continuam de pé no código | duas sprints inteiras — e é a **mesma junta** da D-16 e da D-30 | **decida junto com a D-16 e a D-30**, porque as três falam do mesmo arquivo por endereço. Separadas, você responde três vezes a mesma pergunta |
| **V-D** | **Um controle cai no meio da partida: o produto renumera os que ficam?** Hoje **renumera** (quem era P4 vira P3) e **devolve** quando ele volta. Medido em 12/08, ensaio `comb-slot-jogador-2200` | é literalmente a metade da **D-30** que a sprint chama de *"o replug no meio da partida"* | **responda dentro da D-30** — a opção (b) que eu recomendo lá é exatamente "não renumera no meio da partida" |

### E uma que nasceu enquanto esta página era escrita — a máscara do gamepad

**Ela não tem número, tem sprint**, escrita hoje por outro agente:
[MÁSCARA-POR-JOGADOR-01](sprints/2026-08-15-MASCARA-POR-JOGADOR-01-a-decisao-de-14-08-esbarra-na-de-10-08.md).

**A pergunta, numa frase:** em **10/08** você escreveu que a máscara do gamepad
é **da sessão**, pelo mesmo motivo do `mode`; em **14/08** você escolheu a
máscara **por jogador** (a D-5). **As duas não cabem juntas.**

| resposta | o que muda na tela | custo | o que fica impossível |
|---|---|---|---|
| **A frase de 10/08 fica** | uma frase declarando o escopo, como já aconteceu na D-6. A máscara continua uma só para a mesa | zero de código | a D-5 cai, e 509 linhas já escritas ficam sem futuro |
| **A frase é reescrita para valer só para o `mode`** | cada controle aparece nos jogos do jeito dele | **≈ 480 min** (estimativa da D-5) | **risco NÃO MEDIDO:** um jogo pode não aceitar controles heterogêneos na mesma sessão |

**Medido hoje, e é o que separa os dois casos:** o `mode` **é** mesmo um só no
daemon, mas a máscara **já tem** um lugar por jogador — cada controle tem o
gamepad virtual dele. **A frase de 10/08 continua certa para o `mode` e ficou
larga demais para a máscara.**

**Recomendação: reescrever a frase para valer só para o `mode`** — a razão que
ela dava não se aplica à máscara, e a D-5 é de 14/08, quatro dias mais nova.

---

# PARTE 5 — as que eu recomendo DERRUBAR em vez de responder

**Três perguntas desta lista estão mal feitas, e responder a uma pergunta mal
feita custa mais caro que não responder.**

1. **A D-24 inteira.** Ela pergunta se você autoriza uma classe de escrita que
   **você já autorizou e que já foi exercida** em 15/08. Responder "sim" não
   muda nada, e responder "não" contradiz o que já rodou. **O que restou dela
   virou a D-31**; o resto é escolha operacional minha.
2. **O item 2 da D-27** (*"posso sondar `0x80`-`0x83`?"*). Os quatro já foram
   sondados no censo dos dezessete. **A pergunta que importa é sobre a escrita,
   e ela é a D-15.**
3. **O item 2 da D-29** (*"o hidraw 0600 é de propósito ou é portão caído?"*).
   **Já foi medido: é de propósito**, e é o próprio Hefesto que esconde o nó.
   Não é decisão sua — é uma linha de regra udev a apagar.

**E uma quarta, que não é mal feita mas está mal colocada:** o *"topa?"* da
**D-28**. Ele não é uma decisão entre dois caminhos, é um **convite para dez
minutos de bancada**. A decisão de verdade escondida ali é a de borda: **o
acelerômetro em número na tela, ou não.**

---

# PARTE 6 — o que já está decidido e ninguém marcou

1. **A D-30 já tem a sua resposta escrita, duas vezes.** Em 12/08 (*"nada de
   macs, nada de personalização por controle"*) e em 15/08 às 03:54 (*"não uma
   imagem fixa salva por mec"*). **O que continuava faltando não era a sua
   escolha — era o preço que a R-15 e a R-23 mediram, e ele está na mesa agora.**
   Se depois de vê-lo você mantiver o que disse, a decisão está tomada e o que
   falta é código.
2. **A D-16 está sendo citada como decidida, e não é.** O índice da leva escreve
   *"D-16 já decidiu que é da PEÇA"* dentro da D-15. **Quem decidiu fui eu, em
   prosa.** Ou você confirma, ou aquela linha é uma citação circular.
3. **O item 2 da D-29** — respondido pela medição, ver a Parte 5.
4. **O item 2 da D-27** — respondido pelos fatos, ver a Parte 5.

---

## Onde cada decisão mora, se você quiser o contexto inteiro

| onde | o que tem lá |
|---|---|
| [o índice da leva da cor e do som](sprints/2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md), seção 8 | **as 21 numeradas**, D-13 a D-33, com o texto original de cada uma |
| [ORDEM-DE-CHEGADA-01](sprints/2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md) | a D-30 inteira: o mecanismo lido no fonte, as três entregas, e as mordidas que protegem a R-15 |
| [ESCADA-QUE-RESPONDE-01](sprints/2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md) | a D-31 e a D-32: os seis ensaios, um por um, com o tempo de cada |
| [SOM-DE-CADA-JOGADOR-01](sprints/2026-08-15-SOM-DE-CADA-JOGADOR-01-o-botao-que-nunca-funcionou-com-a-mesa-cheia.md) | a D-26 e a D-28, e os dois defeitos de áudio que **não** dependem de decisão nenhuma |
| [o índice da madrugada](sprints/2026-08-15-INDICE-a-madrugada-que-quase-nao-virou-pagina.md), seção 3 | as suas sete falas de 14-15/08, com hora, e o que cada uma trava |
| [ONDE-PARAMOS](2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md), seção 3 | as quatro antigas, sem número |

---

**Uma última linha, e ela é de honestidade:** os custos em minutos desta página
**não foram medidos**, exceto os da escada (1 h 25 somados, medidos ensaio a
ensaio), os da ORDEM-DE-CHEGADA-01 (90 min e 40 min) e o da SOM-DE-CADA-JOGADOR-01
(4 h 45). Todo o resto é estimativa, e está marcado como tal.
