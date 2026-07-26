# PLAYER-01 — um número de jogador, e ele é editável

- **Status:** ENTREGUE em 25/07/2026 pelo commit `14cd31b`
- **Prioridade:** MÉDIA
- **Aberta em:** 25/07/2026
- **Absorve:** UI-SELETOR-01 (ordem dos chips), aberta mais cedo em 25/07

## Os relatos

> "a escolha do player nos LEDs de jogador não sincroniza com o botão superior
> que informa o controle e o player"

> "talvez o nome da seção devesse mudar também"

## O achado

A expectativa dela — *escolho o player e o cabeçalho acompanha* — **é
irrealizável hoje por construção**. Não existe, em lugar nenhum do projeto, um
comando que atribua um número de jogador a um controle. Só existe o
`identity.renumber`, que compacta todos preservando a ordem relativa, e que fica
na aba Início.

Ela está clicando num controle de **aparência** esperando que ele mude
**identidade**. E o rótulo da tela promete exatamente isso.

## Cinco conceitos, três widgets

| # | conceito | onde é editado | onde é exibido |
|---|---|---|---|
| 1 | cor da lightbar | aba Lightbar | prévia + hardware |
| 2 | **desenho das 5 luzes** | aba Lightbar, moldura "LEDs de Jogador" | **em lugar visível nenhum** |
| 3 | **número do jogador** (identidade) | **em lugar nenhum** | chip do cabeçalho, cartões |
| 4 | controle-alvo da edição | chip do cabeçalho | o próprio chip |
| 5 | número do jogador no co-op | subsistema de co-op | sufixo nos cartões |

Os conceitos **3 e 4 dividem um único widget**. Os conceitos **3 e 5** são
números distintos que a própria base de código adverte não confundir
(`app/actions/base.py:26`) — e a aba Status os exibe **lado a lado na mesma
linha**: "Controle 3 — BT · Jogador 1".

## O chip do cabeçalho carrega três números

`app/actions/status_actions.py:380` e `:383`:

| | valor | de onde vem |
|---|---|---|
| o que ele **mostra** | `Sony 3 · BT` | o número de identidade |
| o que ele **envia** | `0` | a posição de enumeração, base zero |
| o que ele **significa** | "alvo das edições" | só o tooltip diz |

Daí a queixa já registrada de que os chips saem fora de ordem: o laço percorre os
conectados na ordem de enumeração e usa o número de identidade **apenas no
rótulo**. Ordenar a exibição não pode reordenar o índice que o comando espera —
por isso os dois precisam ser separados, não reordenados.

## Por que não sincroniza

A ligação existe **numa direção só**: mudar o chip atualiza a aba Lightbar. O
caminho de volta **não existe** — `lightbar_actions.py` só lê o alvo, e nunca
escreve no estado do seletor. E não poderia funcionar mesmo que escrevesse: o
número do chip vem do registro de identidade, e o comando de LED **jamais toca
esse registro**.

Resultado medido: com o chip em "Sony 3", clicar em "Player 2" acende o padrão do
jogador 2 no hardware, enquanto o cabeçalho continua "Sony 3", o cartão da aba
Status continua "Controle 3" e o da aba Início continua "Controle 3 — P1".
**Três superfícies, dois números, o mesmo controle.**

## Dois casos em que a escolha manual é desfeita

- **Pedido sem controle identificado** (`lightbar_actions.py:558`) — quando o
  mapa de controles ainda não foi preenchido por um tique do daemon, o pedido vai
  sem destinatário e grava numa camada **abaixo** da automática. O automático
  vence no próximo reforço, e a escolha dela "volta sozinha".
- **Co-op ligado** — a camada de co-op sobrescreve o padrão de luzes **acima** da
  escolha manual, por construção. Com co-op ativo, escolher o desenho não adianta.

## Rótulos que estão factualmente errados

- `gui/main.glade:955` — *"Os interruptores manuais valem com as cores
  automáticas desligadas."* **Falso desde o R-14**, por dois motivos
  independentes: a escolha manual vence a automática por campo, com a automática
  ligada; e a caixa de "cores automáticas" não governa mais a numeração. Além
  disso fala de interruptores que estão **ocultos**.
- `gui/main.glade:830` — *"Escolha o jogador"*. Não escolhe jogador nenhum:
  escolhe um desenho de luzes. **É exatamente a queixa (b) dela.**

## Entregas

### 1. Renomear para o que a coisa é

| onde | de | para |
|---|---|---|
| `main.glade:820` | "LEDs de Jogador" | **"Desenho das 5 luzes"** |
| `main.glade:830` | "Escolha o jogador…" | **"Escolha o desenho das luzes. Isto muda só a aparência — o número do controle continua sendo o do cabeçalho."** |
| `main.glade:881-903` | "Player 1…4" | **"Desenho do P1…P4"** |
| `main.glade:955` | o aviso falso | **remover** ou reescrever para o que o código faz |

### 2. O que está faltando de verdade: atribuir número

Um comando novo — `controller.player.set` — que escreva o número de jogador de um
controle, e um controle na interface perto do chip: **"Número deste controle"**.

Sem isso, nenhuma renomeação resolve a expectativa dela; apenas para de prometer
o que não existe. **Esta é a entrega principal**, e ela depende de NUM-01: só faz
sentido atribuir número depois que a numeração deixar de ser um inteiro absoluto
persistido e passar a ser ordem de preferência.

### 3. Separar os dois papéis do chip

O chip deve deixar claro que é um **seletor de alvo** — hoje a única pista é um
tooltip. O selo "Editando: Controle 3" já faz metade do trabalho, mas só aparece
quando há endereço estável.

### 4. Ordenar os chips sem quebrar o índice *(absorve UI-SELETOR-01)*

Ordenar a **exibição** por número de identidade, mantendo o índice de enumeração
no envio. São dois campos; hoje são um só usado para as duas coisas.

### 5. Mostrar o estado resolvido, não o rascunho

A aba lê apenas o rascunho, e a camada automática nunca entra nele. Num perfil
novo, a moldura mostra *nada selecionado* enquanto o controle exibe três luzes
acesas. **A janela não tem leitura de volta do estado real.**

### 6. Corrigir o pedido sem destinatário

Quando não houver controle identificado, o pedido deve **falhar visivelmente** em
vez de gravar numa camada onde o automático o desfaz em seguida.

## Como validar

1. Trocar o desenho das luzes → o cabeçalho **não** muda de número *(correto — são
   coisas diferentes, e agora a tela diz isso)*.
2. Mudar o número pelo controle novo → **cabeçalho, cartão da Status e cartão da
   Início mudam juntos**.
3. Com co-op ligado, a tela avisa que o co-op governa o desenho.
4. Chips em ordem crescente, e clicar em cada um edita o controle certo.
5. Perfil recém-criado: a moldura mostra o desenho que **está aceso**.

## Nota

Este é o mesmo defeito de fundo do MODO-01, noutra superfície: **um nome para
várias coisas**. Lá são seis "modo jogo"; aqui, cinco números de jogador. Vale
como regra da casa: quando a mesma palavra aparece em cinco camadas com sentidos
diferentes, o próximo defeito já está escrito.
