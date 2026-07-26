# CONTAGEM-01 — a tela diz "2 jogadores" com quatro controles na mesa

- **Status:** ENTREGUE em 25/07/2026 pelo commit `0c08e77` — uma entrega ficou de
  fora por decisão, na seção de fechamento
- **Prioridade:** ALTA — atinge diretamente o objetivo dos quatro jogadores
- **Aberta em:** 25/07/2026, por inspeção visual da janela

## O que se vê

Com quatro controles conectados, a janela exibe **três contagens diferentes ao
mesmo tempo**, em três lugares:

```
aba Início — cabeçalho:    2 controles: USB + BT
aba Início — chips:       Sony 1·USB │ Sony 2·BT │ Nintendo 3·BT │ 8BitDo 4·cabo
aba Início — botão:       Preparar co-op (2 jogadores)
aba Início — texto:       2 controles = 2 jogadores
aba Início — Controles:   [Controle 1 — P1]  [Controle 2 — P2]   ← dois cartões
aba Status — Conexão:     Conectado (2 controles)
aba Emulação — Gamepads:  8 controles detectados pelo sistema
```

**Dois, quatro e oito.** A fita de chips sabe que são quatro e até os numera
certo; o resto da aba Início e a aba Status dizem dois; a aba Emulação diz oito.

O efeito prático é direto sobre o objetivo da casa: ela clica em *"Preparar co-op
(2 jogadores)"* com quatro controles na mesa.

O **oito** tem causa própria e já era conhecido: aquele campo conta todos os
dispositivos de joystick do sistema, incluindo os gamepads virtuais que nós
mesmos criamos e os do Steam Input. Ele não vem do daemon nem filtra nada — é a
única das três contagens que está simplesmente errada, não apenas respondendo a
outra pergunta.

## Confirmado no daemon

```
controllers (DualSense) : 2
co-op.externals         : 2      ← o daemon SABE que há dois externos
external_controllers    : (ausente do state_full)
```

Quatro aparelhos físicos presentes, confirmado por `hidraw`: dois DualSense, um
Nintendo Pro e um 8BitDo.

## A causa: duas fontes de verdade na mesma janela

1. **Os chips** buscam os externos por um caminho próprio, assíncrono, herdado do
   trabalho de 17/07 que trouxe os externos para o seletor. Por isso enxergam
   quatro.
2. **O cabeçalho** conta `len(conectados)` — a lista de DualSense
   (`status_actions.py:1391`).
3. **O botão e o texto de co-op** contam `len(controllers)` e `len(players)`
   (`home_actions.py:331` e `:356`) — a mesma lista, sem externos.
4. **O `state_full` publica os externos só como NÚMERO**
   (`ipc_handlers.py:1493`: `result["coop"]["externals"] = len(vistos)`), nunca
   como lista. A interface não tem como montar cartão nem somar jogador.

Não é um número errado. São **dois números certos para perguntas diferentes**,
exibidos como se fossem o mesmo.

## Por que isso importa mais do que parece

O projeto inteiro se organiza em torno de "quatro controles, quatro jogadores". A
tela principal — a primeira que se abre — afirma que há dois. Quem não conhece o
código conclui que o Hefesto não reconheceu os outros dois, quando ele reconheceu,
numerou e até acendeu os LEDs deles.

É também a superfície onde a promessa de AUTO-01 ("Preparar co-op em um clique")
se desfaz: o clique prepara para dois.

## Entregas

1. **`state_full` publica os externos como LISTA**, não como contagem — com
   endereço, nome, número e via, do mesmo jeito que já faz para os DualSense. É
   a entrega de que tudo o mais depende.
2. **Uma contagem só, e ela inclui os externos.** Cabeçalho, aba Status, texto de
   co-op e rótulo do botão passam a somar controles de jogo, não DualSense.
3. **Cartão para cada controle**, inclusive externos. Hoje a seção "Controles"
   mostra dois de quatro.
4. **O "8 controles detectados pelo sistema" sai ou passa a dizer a verdade.**
   Ele conta os nossos próprios gamepads virtuais como se fossem controles dela.
   Se a intenção era diagnóstico ("o que existe no sistema"), o rótulo tem de
   dizer isso e separar o que é nosso; se não era, o campo não deveria existir.
5. **Os chips deixam de ter caminho próprio.** Enquanto houver duas rotas de
   dados para a mesma pergunta, elas voltarão a divergir — foi assim que este
   defeito nasceu.
6. **Honestidade quando os números divergem por motivo legítimo.** Um externo em
   "como ele mesmo" (ver MÁSCARA-01) é numerado pelo jogo, não por nós — nesse
   caso o cartão deve mostrar travessão, e o texto de co-op precisa distinguir
   "controles na mesa" de "jogadores que nós numeramos". A cura não é fingir que
   os números são um.

## Colhidos na mesma inspeção, e que pertencem a sprints já abertas

- **O medidor de microfone não aparece em cartão nenhum** na aba Status — nem no
  controle por cabo. É o que MIC-USB-01 e MIC-BT-01 preveem: quando está mudo,
  ele *some* em vez de dizer que está mudo e por quê.
- **A aba Emulação afirma "Microfone do DualSense: ligado"** enquanto o firmware
  do controle está com o microfone mudo (medido). O rótulo se refere à supressão
  do WirePlumber, não ao estado real — e não há nada na tela que distinga as
  duas coisas. Entra em MIC-USB-01.
- **O botão "Ver daemon.toml (referência)"** abre um arquivo que o daemon não lê,
  e o próprio arquivo diz isso na primeira linha. Já registrado em ABAS-01 como
  PLACEHOLDER-04; a inspeção confirma que está visível na tela.
- **Sobra muito espaço vertical vazio** em Gatilhos e Emulação depois da
  legibilidade. O conteúdo ficou no topo e os botões de aplicar no rodapé, com um
  vão no meio.

  Não é defeito, e ela apontou o uso certo para ele:

  > *"essa parte vazia poderia ser os botões aparecendo maiores e mais
  > distribuídos, e no final a parte do mic"*

  Duas coisas de uma vez. Os presets de gatilho ganham área de clique maior — o
  piso subiu para 32 px na LEGIBILIDADE-01, mas com esse espaço dá para ir além
  do mínimo, e são dezenove botões numa grade apertada. E o microfone, que hoje
  **não tem lugar nenhum na aba Status**, ganha um: o rodapé da aba, onde o vão
  já existe.

  Isso resolve o buraco que MIC-USB-01 e MIC-BT-01 apontam por outro caminho —
  em vez de espremer o medidor dentro do cartão do controle, ele vira uma faixa
  própria, com espaço para dizer **qual das três camadas** está segurando o
  microfone quando ele estiver mudo.

## Como validar

1. Quatro controles conectados — dois DualSense, um Nintendo, um 8BitDo.
2. Cabeçalho diz **4 controles**.
3. Botão diz **"Preparar co-op (4 jogadores)"**.
4. Seção Controles mostra **quatro** cartões, numerados 1 a 4.
5. Desligar um → tudo cai para três **junto**, sem uma parte da tela ficar para
   trás.
6. Com um externo em "como ele mesmo", a tela mostra travessão no lugar do número
   dele e explica por quê — em vez de somar um jogador que não é nosso.

**Critério que resume:** nenhuma tela do Hefesto pode exibir dois números
diferentes para a mesma pergunta ao mesmo tempo.

## Nota

Este defeito não seria encontrado por teste. Cada número está correto para a
pergunta que o seu código faz; o erro só existe quando os dois aparecem juntos na
mesma tela, e só é visível **olhando a janela**. Foi encontrado na primeira
inspeção visual depois de LEGIBILIDADE-01 — e é o argumento de que ver a
interface é parte da validação, não acabamento.

## Fechamento (25/07/2026, commit `0c08e77`)

A fonte única existe: todos os pontos da janela leem a mesma lista, montada a
partir do `state_full`, e `coop.externals` deixou de ser medido em paralelo —
virou o tamanho da lista, então os dois não podem divergir nem por um tick. A
segunda rota de dados dos chips foi **removida**, não corrigida: enquanto ela
existisse, voltaria a divergir.

**O que a medição acrescentou ao que a sprint sabia:**

- **O "oito" tinha duas causas, não uma.** Além de contar gamepads virtuais,
  ele contava **cada controle duas vezes** — todo controle classe DualSense abre
  dois nós de joystick (gamepad e sensores de movimento). E o critério intuitivo
  para separar "o que é nosso" pelo caminho no sysfs **classificaria um DualSense
  Bluetooth como nosso**, porque desde BLUEZ-UHID-01 o BlueZ cria o HID dos
  físicos por rádio no mesmo lugar onde mora o nosso gamepad virtual. Por isso o
  campo **ficou**, passando a dizer a verdade: um diagnóstico que revela essas
  duas coisas vale mais que um campo a menos.
- **Havia um quarto lugar contando errado**, além dos três que a sprint listou:
  com externos na mesa e nenhum DualSense, o cabeçalho afirmava *"Controle
  Desconectado"* com controle ligado na frente dela.

**Ficou de fora, por decisão:** cartão de externo na **grade da aba Status**, com
sticks, bateria e sensores ao vivo. Não lemos input, bateria nem sensores desses
controles, e preencher aquelas áreas seria inventar dado — a mesma regra que esta
sprint aplica no travessão. A entrega 3 foi cumprida na seção "Controles" da aba
Início, que é onde a sprint mostra os cartões. Um cartão só-identidade na Status
merece sprint própria.

**Validação em hardware pendente:** o passo 5 do "Como validar" (desligar um
controle e tudo cair junto) é gate humano — a contagem já é única por construção,
mas a queda simultânea só se prova com os quatro na mesa.
