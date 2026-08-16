# PONTO A PONTO — a lista dela, e a ordem de atacar

**16/08/2026.** Ela levantou sete pontos de uma vez e pediu: *"Pode me ajudar a
organizarmos e resolvemos ponto a ponto?"* Este documento é essa lista, com o
que JÁ se sabe de cada um e o que falta.

A ordem não é por facilidade. É por **quanto cada item custa a ela por dia**.

---

## A preocupação de fundo, e ela tem razão

> *"me preocupa o fato de serem regressões e me preocupa o fato de que isso
> possa voltar no futuro."*

Regressão que volta é regressão que não tem portão. **Todo item desta lista só
fecha com um teste que morde** — arrancar a cura, ver reprovar, devolver. É o
que separa "consertei" de "não volta".

E há um agravante medido hoje: três portões desta casa passaram verde com o
defeito vivo (o contador do wrapper, a árvore errada do vdf, o `hidden_count` do
broker). Um portão que olha para o lugar errado é pior que portão nenhum, porque
encerra a busca. Por isso cada item abaixo diz **como o portão vai morder**.

---

## 1. A reconexão BT que mata a entrada — P0

**O que é.** Controle cai e volta no rádio (ou sai do cabo para o rádio) → o
daemon registra a perda e **nunca reabre os leitores**. Segue dizendo
`connected=True` com os eixos congelados; o vpad emite 396 reports/8 s com
sequência perfeita e LX travado em 128. Para o jogo: um controle vivo que nunca
se mexe.

**Por que é P0.** É o que estragou a sessão dela em três jogos e mandou horas de
investigação para o lugar errado.

**Onde curar** (o gancho já existe, e hoje só avisa):
- `evdev_read_lost` — **não tem tratador nenhum**;
- `state_stale_neutral_warning` — já sabe dizer que estagnou.

**Chega na GUI e no install?** Sim, regra dela de 09/08. A cura é no daemon
(vale sem clique), e a janela precisa **mostrar** o estado degradado em vez de
dizer `connected=True`.

**Como o portão morde:** simular a perda do fd (errno 19) e exigir que os
leitores voltem sozinhos; e um teste que reprove se o estado disser
`connected=True` com o leitor morto.

## 2. As regressões, e como impedir que voltem — P0

**O que é.** DON'T SCREAM e Pragmata funcionavam no rádio e pararam. Duskfade é
caso à parte (nunca funcionou).

**O que falta:** um portão que exercite o CICLO — conecta, desconecta, reconecta
— em vez de só o estado estático. Nenhum teste de hoje faz isso, e é por isso que
o defeito 1 passou.

## 3. O som do alto-falante no rádio — P1

**A memória dela:** *"a minha certeza do lance do som no bt do speaker do
dualsense, o claude tinha feito funcionar quando testávamos no pragmata. Eu
simplesmente esqueci isso e achei que tivéssemos resolvido em definitivo."*

**O que o mapa diz hoje** (`mapa-controles.csv`):

| linha | radio_aceita | radio_aciona | grau |
|---|---|---|---|
| `audio.alto_falante` | sim | **não** | inferido-do-codigo |
| `audio.alto_falante.rota` | sim | sim | inferido-do-codigo — *"não medido por BT"* |
| `audio.alto_falante.volume` | sim | sim | inferido-do-codigo — *"NÃO MEDIDO por BT"* |

**O problema não é o número: é o GRAU.** Existe uma medição dela, com a orelha,
e o mapa está registrando "inferido do código". A observação dela é fonte
primária nesta casa. **Isto é dívida das specs**, exatamente do tipo que o mapa
existe para não deixar acontecer.

**Ação:** repetir o ensaio no rádio com a orelha dela (4 min), e promover a
célula para `medido` — ou registrar que caducou, com data.

## 4. Parear o que o físico manda e o que o virtual manda — P1

**Ideia dela**, e é a Pedra de Roseta aplicada ao par físico × virtual:

> *"conseguimos parear o que o controle fisico manda e o que o virtual manda?"*

**Dá, e hoje foi meio caminho andado.** Já foram medidos lado a lado:

| canal | vpad | físico |
|---|---|---|
| gamepad | 286 ev/10 s | 0 (grab, correto) |
| giroscópio | 7 231 | 19 435 |
| touchpad | 2 807 | 3 660 |

E no report HID de 64 bytes do vpad, os bytes que variam são
`2,3 · 7 · 16–27 · 28–32 · 33–36` (eixos, sequência, giro/acel, timestamp,
touchpad).

**O que falta é virar instrumento**, não medição solta: um script que capture os
dois reports no mesmo instante e diga **campo a campo** o que o físico manda e o
que o virtual repassa. Aí "o vpad é fiel?" vira uma pergunta com resposta, e não
opinião.

**Nota da medição de hoje:** o giroscópio do vpad tem ~37% dos eventos do físico
(7 231 contra 19 435). Pode ser decimação legítima ou perda. **Ninguém mediu.**

## 5. Microfone, giroscópio e touch nos jogos que funcionavam — P1

**Dado dela:** DON'T SCREAM e **Big Walk** usam mic, giroscópio e touch, e
*"ambos os jogos funcionavam via bt com gatilho adaptativo e beleza"*.

**Por que isso vale ouro:** é o **lado bom do par** para as features que hoje
falham. Não é hipótese de que "deveria funcionar" — é registro de que
funcionava, nos mesmos jogos, no mesmo transporte.

**Ação:** depois do item 1 curado, retestar os dois. Se voltarem inteiros, o
defeito 1 explicava também as features, e a lista encolhe.

## 6. O touchpad engasgando durante os testes — P2

**Relato dela:** *"durante os testes notei que tava tipo engasgando. aí depois
voltava."*

**Primeira suspeita sou eu.** Durante a bancada abri `hidraw4`, `event21/22/23` e
`event25–28` em laços de leitura não-bloqueante com `sleep` de 2–4 ms. É a
armadilha nº 3 da casa — *o instrumento briga com o produto*.

**Ação:** medir o touchpad com e sem os instrumentos rodando. Se for eu, o
conserto é do instrumento; se não for, é achado novo.

## 7. Duskfade — P3

Caso próprio: nunca funcionou em transporte nenhum, e em 16/08 deu os primeiros
inputs da vida. O par com DON'T SCREAM está montado e o
`scripts/ensaios/quem_o_jogo_abre.py` foi corrigido (ele mentia: lia o environ do
`reaper` em vez do processo do jogo).

---

## A bancada, do jeito que ela montou

> *"quer que eu teste no controle azul e deixe o vermelho carregando? eu to
> sentado no lado do bt, removi tudo que poderia bagunçar e to em cima do bt
> agora pra não dar pt por conta da distancia."*

**Sim, e é a montagem certa** — um controle só, distância curta, o resto
removido. Elimina de uma vez a distância, a disputa entre controles e a bateria
como variáveis. É a mesma regra que este dia acrescentou à metodologia:

> **Um ensaio mede UM gesto — e uma variável por vez, também na bancada.**
