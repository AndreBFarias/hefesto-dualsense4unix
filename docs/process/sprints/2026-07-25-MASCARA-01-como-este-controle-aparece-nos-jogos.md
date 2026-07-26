# MÁSCARA-01 — "como este controle deve aparecer nos jogos"

- **Status:** ABERTA
- **Prioridade:** MÉDIA (depende de outras três)
- **Aberta em:** 25/07/2026 — desenho proposto pela mantenedora

## De onde veio

Discutindo por que a numeração do jogo não bate com a nossa, a saída óbvia era
dar gamepad virtual a todos os controles — inclusive Nintendo e 8BitDo — para que
o jogo enxergasse só dispositivos nossos, na ordem que montamos.

O problema dessa saída é o **rótulo dos botões**: um Nintendo Pro apresentado como
DualSense faz o jogo pedir `` onde o botão físico diz `X`.

A proposta dela resolve transferindo a escolha para quem sabe:

> *"na interface ao clicarmos no controle — tipo o Switch — ele abre a tela que
> escolhemos como ele deve aparecer na tela"*

Em vez de o projeto decidir por todos, **cada controle tem a sua máscara, e o
preço é dito na hora da escolha.**

## Por que isto é o que resolve a numeração

Não porque passemos a controlar a ordem — **não controlamos, e isso foi
verificado**. Não existe variável de ambiente nem canal que informe número de
jogador a um jogo, e o critério que os jogos usam nunca foi medido neste projeto
*(as afirmações existentes sobre "ordem de enumeração" são inferência, não
experimento)*.

O que controlamos é o **conjunto**. Se todo dispositivo que o jogo enxerga é um
gamepad virtual nosso, qualquer critério que ele use opera sobre uma lista que
**nós montamos** — e o número que ele atribuir volta pelo caminho de repasse,
fechando o laço.

A única alavanca real que existe hoje é **negativa**: tirar dispositivo de cena.
Esta sprint a usa deliberadamente.

## A tela

```
Como este controle deve aparecer nos jogos?

  ( ) Como ele mesmo — Nintendo Pro
      Os botões batem com o que está escrito neles.
      Este controle é numerado pelo jogo, fora da sua ordem.

  ( ) Como DualSense
      Entra na sua ordem de jogador. Gatilhos, luz e vibração funcionam.
      O jogo vai pedir  onde o seu botão diz X.
      Enquanto a ponte de movimento não existir, perde o giroscópio.

  ( ) Como Xbox 360
      Máxima compatibilidade. Sem gatilhos adaptativos.
```

**Cada opção diz o que custa.** É o que falta na interface hoje, e é metade do
valor desta sprint.

## Onde a máscara mora — a decisão, com o argumento

A máscara é propriedade do **aparelho**, não da configuração do jogo.

*"Este Nintendo Pro se apresenta como DualSense"* é uma verdade sobre o controle e
sobre os rótulos impressos nele. Não muda porque a janela em foco mudou.

E há uma razão dura, além da conceitual: **trocar a máscara derruba e recria o
gamepad virtual.** Se ela morasse na configuração por perfil, cada troca
automática de perfil — cada alt-tab — faria o controle sumir e voltar no meio da
partida. Isso é pior que o defeito que a sprint conserta.

Portanto: registro de identidade, no mesmo arquivo que já guarda a ordem de
preferência, com versão de esquema nova. A configuração por perfil pode, no
máximo, ter uma recusa explícita.

## O que hoje impede

Três coisas, todas encontradas no código:

1. **Os externos não têm gamepad virtual.** Existe comentário dizendo que ganham
   — é letra morta: o conjunto de candidatos vem de uma descoberta fechada em
   fabricante e produto da Sony. Nenhum externo chega a ser promovido.
2. **Os externos não são escondidos do jogo.** As variáveis que escondem os
   físicos carregam **um** par fabricante/produto, cravado. Nintendo e 8BitDo
   nunca entram.
3. **A identidade de externo não é endereço.** Ela é um caminho de dispositivo, e
   **todo** o direcionamento por endereço curto-circuita nesse formato — em
   quatro lugares distintos. Sem identidade estável, o controle mascarado não tem
   alvo.

## Entregas

1. **Máscara por aparelho** no registro de identidade, com bump de esquema.
2. **Descoberta por-jogador que aceite externos** — quando, e só quando, a
   máscara pedir. A descoberta atual continua existindo para o caminho DualSense.
3. **As variáveis que escondem os físicos deixam de ser constantes** e passam a
   ser montadas a partir dos controles mascarados.  A lista de variáveis
   permitidas é **espelhada no script de lançamento** — mudar de um lado exige
   mudar do outro, ou o jogo recebe ambiente diferente do que o daemon acha que
   mandou.
4. **A tela**, com o preço em cada opção.
5. **Honestidade na numeração mista.** O controle em "como ele mesmo" sai da
   nossa ordem — o cartão dele **precisa mostrar um travessão**, não um número
   que mentiria. É a mesma regra que o projeto já aplica noutro lugar: nulo
   honesto vale mais que número errado.
6. **Ponte de movimento para externo mascarado.** Hoje o espelho de giroscópio
   exige um caminho de hidraw que não existe para externos, **por decisão**. Sem
   esta entrega, "Como DualSense" num Pro custa o giroscópio — e a tela tem de
   dizer isso enquanto for verdade.

## Dependências

```
JOGO-01  (entregue) ──┐
NUM-01   (entregue) ──┤
IDENT-01 (aberta)   ──┴──> MÁSCARA-01
PLAYER-LED-01 (aberta) ───> (independente, entrega valor sozinha)
```

**IDENT-01 é pré-requisito duro**: sem identidade estável para externo, não há
onde pendurar a máscara nem para onde mandar o repasse.

E enquanto a exceção do Steam Input mantiver gamepad virtual de pé sem
deduplicação, o co-op de quatro continua sendo loteria e **nenhuma numeração se
sustenta** — por isso JOGO-01 vinha primeiro.

## O que foi considerado e recusado

**Adotar a numeração do kernel como nossa.** O contador do kernel reusa o menor
identificador livre e **conta os gamepads virtuais junto com os físicos** — cada
recriação de vpad e cada reconexão por rádio renumeraria a mesa inteira. Seria
trocar a instabilidade que a NUM-01 acabou de curar por outra pior.

**Impor o nosso número ao jogo.** Não existe canal. Verificado.

## Como validar

1. Nintendo Pro em "como ele mesmo" → botões corretos, cartão mostra travessão em
   vez de número.
2. O mesmo Pro em "como DualSense" → entra na ordem, ganha gatilhos e luz, e a
   tela avisou sobre os rótulos antes.
3. Quatro controles mascarados → o jogo vê **quatro** dispositivos, todos nossos.
4. Alt-tab não derruba nenhum vpad *(a máscara não mora no perfil)*.
5. Trocar a máscara com jogo aberto → recusa ou avisa, mas não deixa a pessoa sem
   controle no meio da partida.
