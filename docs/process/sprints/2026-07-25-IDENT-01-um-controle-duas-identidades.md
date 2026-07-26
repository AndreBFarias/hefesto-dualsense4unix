# IDENT-01 — um controle, duas identidades

- **Status:** ABERTA
- **Prioridade:** MÉDIA
- **Aberta em:** 25/07/2026, a partir de pergunta feita com os quatro controles na mesa

## A pergunta que abriu

> "os 4 controles temos mapeados tanto por BT como por cabo, né? Tipo, o 8BitDo
> sempre vai ser o jogador 4?"

A resposta medida é **não**, e só para um dos quatro.

## O que foi medido

| controle | endereços vistos em 8 h de log | estável entre vias? |
|---|---|---|
| DualSense (branco) | `14:3a:9a:00:00:01` | **sim** — visto por rádio às 15:39 e por cabo às 21:00, mesmo endereço |
| DualSense (segundo) | `a0:fa:9c:00:00:02` | **sim** |
| Nintendo Pro | `e0:f6:b5:00:00:03` | **sim** — endereço único em todo o período |
| **8BitDo Pro** | `e4:17:d8:1c:00:04` e `e4:17:d8:1c:00:05` | **não** |

O DualSense usa o endereço de rádio como identidade mesmo no cabo — por isso
trocar de via não muda nada para ele. **O que muda a identidade do 8BitDo não é a
via, é o MODO**: em modo Switch ele se apresenta com um endereço, em modo
DirectInput/PS4 com outro.

Consequência prática: trocar de modo faz o controle aparecer como um aparelho
**novo**, que pega o próximo número livre. Com quatro na mesa, vira jogador 5 — e
o DualSense só tem cinco luzes de jogador, então empurrar alguém para lá é
defeito visível.

## O que o projeto já sabia, e por que não basta

`daemon/subsystems/external_identity.py` documenta este mesmo problema sob o ID
MODO-01, e a conclusão registrada foi:

> *"A cura NÃO é adivinhar que os dois são o mesmo plástico (não há nada em comum
> entre eles: OUI, VID/PID e driver diferem) — é reconhecer que a identidade
> sintética não é identidade."*

**Aquela conclusão estava certa para aquele caso, e não cobre o de hoje.** A
diferença importa:

| | caso registrado (MODO-01) | caso medido em 25/07 à noite |
|---|---|---|
| modo Switch | endereço **sintetizado** (`02` + fabricante + produto + barramento) | endereço **real** `e4:17:d8:1c:00:04` |
| modo PS4 | endereço real | endereço real `e4:17:d8:1c:00:05` |
| em comum | nada | os quatro primeiros octetos |

Naquele episódio o controle não respondia ao pedido de identificação no cabo e o
kernel fabricava um endereço — daí "nada em comum", literalmente verdadeiro. Hoje
ele respondeu nos dois modos, e os dois endereços são de hardware, do mesmo
fabricante, divergindo só nos dois últimos octetos.

A cura da identidade volátil continua válida e não é revogada por esta sprint —
ela resolve o endereço fabricado. Esta trata do caso vizinho: **dois endereços
reais do mesmo plástico**.

## Por que o palpite automático é recusado

O prefixo `e4:17:d8:1c` agrupa os dois endereços do 8BitDo e não colide com
nenhum outro controle da casa. É tentador usá-lo, e é errado:

**Endereços dentro de um fabricante são alocados em sequência.** Dois 8BitDo do
mesmo modelo, comprados juntos, muito provavelmente também compartilham os quatro
primeiros octetos. Fundir por prefixo transformaria **dois controles distintos em
um só** — um jogador que some da mesa, defeito pior que o atual.

E não há como distinguir os dois cenários de fora: quatro octetos iguais podem
significar "mesmo aparelho em outro modo" ou "dois aparelhos irmãos". Qualquer
regra automática acerta um caso e erra o outro, em silêncio.

Vale registrar as alternativas consideradas e por que caem:

- **Número de série** — o 8BitDo não expõe um estável entre modos (é justamente o
  campo que o clone preenche de forma inconsistente, causa do defeito que o
  patch `0003` do hid-nintendo existe para contornar).
- **Nunca ver os dois ao mesmo tempo** — verdadeiro, mas insuficiente: um
  aparelho ausente pode simplesmente estar desligado.
- **Perguntar ao aparelho** — não há comando de "quem é você" que atravesse os
  dois modos; a identidade *é* o que muda.

## O desenho: ela declara, o projeto obedece

O Hefesto não adivinha — ele oferece o gesto e guarda a decisão.

### Entrega 1 — declarar que dois endereços são o mesmo controle

Um comando novo (`identity.alias.set` ou nome equivalente justificado) que registre
um endereço como **apelido** de outro. O registro passa a resolver o apelido para
a identidade principal antes de decidir a posição, então os dois modos ocupam o
**mesmo lugar** na ordem de preferência — nunca dois.

O vínculo mora no mesmo `controllers.json`, com versão de esquema nova. A entrada
de apelido guarda também **por que** foi criada (declarada por ela, e quando):
sem isso, um arquivo editado à mão vira mistério em três meses.

### Entrega 2 — o gesto na janela

Onde ela já vê os controles (aba Status), oferecer *"este é o mesmo controle
que…"* com a lista dos conhecidos. O momento natural é quando um aparelho
desconhecido aparece com o mesmo fabricante de um já registrado — a janela pode
**sugerir** sem aplicar:

> *"Apareceu um controle 8BitDo novo. É o mesmo 8BitDo do jogador 4, em outro
> modo? [Sim, é o mesmo] [Não, é outro controle]"*

Sugerir é diferente de adivinhar: o palpite fica visível e a decisão é dela. E a
resposta "não, é outro" também precisa ser guardada, senão a pergunta volta a
cada conexão.

### Entrega 3 — desfazer

Todo vínculo declarado tem de poder ser desfeito pela mesma superfície. Se ela
errar, ou vender um controle e comprar outro do mesmo modelo, o apelido precisa
sair sem editar arquivo à mão.

### Entrega 4 — o `doctor` enxerga

Um check que liste identidades que **parecem** o mesmo aparelho (mesmo
fabricante, prefixo próximo, nunca vistas juntas) e diga se estão vinculadas ou
não. Diagnóstico, não cura automática.

## O paliativo que já existe

Enquanto esta sprint não entra, o `identity.number.set` (PLAYER-01, entregue em
25/07) resolve em um comando: trocou de modo, ela põe o controle de volta no
número certo, e aquele endereço guarda a posição. O custo é fazer isso uma vez
por modo — não a cada conexão.

## Como validar

1. 8BitDo em modo Switch → jogador 4.
2. Declarar o endereço do modo PS4 como o mesmo controle.
3. Trocar para modo PS4 → **continua jogador 4**, sem gesto nenhum.
4. Voltar para Switch → continua 4.
5. Com os quatro na mesa, **ninguém é empurrado para o slot 5**.
6. Um segundo 8BitDo de verdade (se houver) → é reconhecido como **outro**
   controle, não fundido ao primeiro.

O critério que resume: **o número acompanha o plástico, não a identidade que o
firmware resolveu apresentar naquele dia.**

## Nota de método

Este é o terceiro episódio da mesma família nesta máquina — o Nintendo Pro
genuíno e o clone 8BitDo compartilhando fabricante e produto, o endereço
fabricado que não é identidade, e agora dois endereços reais do mesmo aparelho.
A lição que se repete: **identidade de periférico não é um fato, é uma
declaração do firmware** — e firmware muda de opinião conforme o modo. Onde o
projeto precisa de estabilidade, quem decide tem de ser a pessoa, com o gesto
guardado.
