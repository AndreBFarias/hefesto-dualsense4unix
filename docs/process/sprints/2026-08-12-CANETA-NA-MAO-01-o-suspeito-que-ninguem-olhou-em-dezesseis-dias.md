# CANETA NA MÃO — o suspeito que ninguém olhou em dezesseis dias

- **Escrito em:** 12/08/2026, no fim da bancada de 11→12/08, na branch
  `restauro/inicio-da-sessao`
- **Rótulo:** `BANCADA MEDIDA` — três features fechadas, um suspeito novo que
  contamina o passado, e cinco erros de método que são meus
- **Grau, e ele muda por bloco:** **MEDIDO** = há linha em
  [`docs/data/ensaios.csv`](../../data/ensaios.csv) com o olho dela e a fala
  literal; **INFERIDO** = o caminho foi lido e fecha, o efeito não foi
  observado; **RELATO DA SESSÃO** = aconteceu na bancada e não virou linha de
  ensaio. Nenhum bloco herda o grau do bloco de cima.
- **O que fecha:** o rumble por evdev, com a causa isolada **e com número**; o
  gatilho adaptativo nos dois lados e nos dois transportes; e a lightbar
  obedecendo a **verde puro** nos três controles quando ninguém tem o hidraw
  aberto no instante da probe.
- **O que fica aberto:** a volta do ensaio da lightbar (reproduzir a falha com o
  Steam vivo na probe); o elemento específico do gatilho; sete dos oito modos de
  gatilho; e um apagador de efeito de gatilho com período de **minutos**, sem
  suspeito nomeado.
- **Fonte primária:** as 42 linhas de `docs/data/ensaios.csv`. **28 delas são
  desta sessão** (linhas 16 a 43), e as 42 têm `observado_por = olho-dela`.
- **O método que se percorreu:** o checklist de
  [`METODO-DE-ISOLAMENTO.md`](../METODO-DE-ISOLAMENTO.md), item por item. Esta
  página é o que aquele checklist comprou numa noite.

---

## 1. A mesa, e o que ela comprou

**GRAU: MEDIDO.**

Quatro DualSense ao mesmo tempo: **P2 e P3 no cabo, P1 e P4 no rádio**. A
identificação saiu do padrão de LED de jogador lido no fonte do driver
(`hid-playstation.c:1836-1842`, os padrões são palíndromos e não há como errar
por orientação) e foi conferida contra a leitura dela — **bateram quatro de
quatro, inclusive o transporte**
([`METODO-DE-ISOLAMENTO.md`](../METODO-DE-ISOLAMENTO.md), seção *O segundo
gabarito*).

A mesa cheia não é enfeite. Ela é o que permite o passo **C1** do checklist —
acionar a mesma feature num controle do cabo e num do rádio **na mesma janela**,
com espalhamento de disparo medido — e é o que responde as linhas de família
`combinacao` do mapa de canais, que **não se respondem com um controle só**
(`scripts/ensaio_rumble_em_par.py`, docstring: *"as nove linhas de `familia =
combinacao` do mapa de canais só se respondem com dois ou mais ligados
juntos"*).

---

## 2. O que FECHOU, e a prova de cada um

### 2.1 O rumble por evdev — causa isolada, e com número

**GRAU: MEDIDO.** Ensaios `rumble-ff-par-vivo-1/2`, `rumble-ff-par-morto-1/2`,
`rumble-ff-quatro-morto`, `rumble-ff-quatro-vivo`, `keepalive-dose-cabo`,
`keepalive-dose-radio`, `keepalive-premissa-troca-de-lado`
(`docs/data/ensaios.csv:16-24`).

A pergunta era a linha `vibracao.rumble.ff` do mapa, que até esta noite estava
`inferido-do-codigo` nos dois transportes. O instrumento
(`scripts/ensaio_rumble_em_par.py`) dispara força-feedback **pelo evdev**, que é
o caminho que os jogos usam — não passa pelo daemon e não disputa o hidraw,
então roda com o daemon vivo sem medir a briga em vez da feature (a armadilha 1
da casa).

| passo do checklist | o que se fez | o que se viu |
|---|---|---|
| **B1** linha de base | daemon **vivo**, 40 s de FF, P2 no cabo | não vibrou nada |
| **B1** linha de base | daemon **vivo**, 40 s de FF, P4 no rádio | vibrou **uma vez** e parou |
| **D1** o ensaio que discrimina | daemon **parado**, mesmo comando, mesmos alvos | contínuo os 40 s, nos dois |
| **C1** no par | quatro controles, janela de **0,0 ms**, daemon parado | *"sim vibraram todos"* — duas rodadas |

A assinatura da falha já dizia o que era: **cancelamento logo após o início, não
pulsação periódica** (`ensaios.csv:17`). Com o daemon fora, a fala dela foi
*"ambos vibraram sem parar de forma contínua"* (`ensaios.csv:19`).

**E então veio o passo que transforma indício em causa — o D2, dose-resposta.**
A constante `OUT_REPORT_KEEPALIVE_SEC` (`core/backend_pydualsense.py:228`) foi
mudada de **0,5 s para 8,0 s**, o daemon reiniciado, e o **mesmo** comando
disparado nos **mesmos** alvos. A vibração passou a durar **oito segundos
exatos** nos dois transportes — `/dev/input/event23` (P2, cabo) e
`/dev/input/event30` (P4, rádio). Literal dela: *"cibrou ambos por 8 segundos"*
(`ensaios.csv:22-23`). Com 0,5 s era um pulso instantâneo.

> **A duração seguiu o valor da constante.** Isso é relação causal, não
> correlação — e é a diferença entre *o keepalive é vizinho do defeito* e *o
> keepalive é o cronômetro do defeito*.

A constante foi **revertida para 0,5 e o daemon reiniciado** no mesmo ensaio
(`ensaios.csv:22`). Fica registrado porque instrumento que não volta ao lugar
contamina a próxima medição.

**A segunda metade, e ela derrubou a premissa de uma cura inteira.** A cura que
estava escrita apostava que **desligar os bits de autorização de vibração**
bastava para o firmware conservar o motor de outro dono. O ensaio de
**troca de lado** (`keepalive-premissa-troca-de-lado`, `ensaios.csv:24`)
respondeu: com o daemon parado, o EV_FF ligou o motor **esquerdo**; um único
report com os bits de vibração **desligados** pediu `common[2]=200` (direito) e
`common[3]=0` (esquerdo). Literal dela: *"esquerda e senti que foi pra direita e
lá morreu"*.

O tremor **trocou de lado**. Logo o report agiu, e agiu **pelos bytes**, com os
bits desligados. É o item **D3** do checklist, e a resposta dele para o
DualSense é: **o firmware honra os BYTES de motor, não os bits de autorização**.
Os bytes saem em **todo** report, fora de qualquer condicional.

### 2.2 O gatilho adaptativo — os dois lados, os dois transportes

**GRAU: MEDIDO** para o aceite; a proveniência é a célula
`gatilho.esquerdo.adaptativo` / `gatilho.direito.adaptativo` de
[`docs/data/mapa-controles.csv`](../../data/mapa-controles.csv)
(`provado_em = 2026-08-11`), **não** `ensaios.csv` — ver a ressalva na seção 8.

O comando foi `hefesto-dualsense4unix test trigger --side {left,right} --mode
Rigid --params '3,8'`, **pela rota do daemon** e não por `--raw` — que é a
armadilha registrada desta casa (o `--raw` disputa o hidraw e imprime "aplicado"
sem ter aplicado). Ela apertou o gatilho dos **quatro** controles em cada
rodada, dois no cabo e dois no rádio:

| rodada | fala literal dela |
|---|---|
| lado esquerdo autorizado | *"todos funcionaram"* |
| lado direito autorizado | *"deu certo o r2 em todos"* |
| `--mode Off` | *"soltou em todos"* |

**A volta ao neutro vale tanto quanto a ida.** É o equivalente do
`weak=0 strong=0` que provou, em 10/08, que o motor não fica preso — sem essa
metade, uma feature que **liga** e não **desliga** passaria por aprovada.

Isto sobe o grau das linhas de gatilho de `MONTOU` para `O APARELHO OBEDECEU`.
`MONTOU` significa que o produto montou o report certo e **nada** sobre o
aparelho obedecer, e tratar um pelo outro é a mentira mais cara desta casa.

**E uma previsão herdada foi medida, e caiu.** De **D3** vinha o palpite de que
o keepalive apagaria o efeito de gatilho de terceiro pelo mesmo mecanismo com
que apaga o rumble — os blocos de gatilho (`common[10..20]` e `common[21..31]`)
também são escritos em todo report, fora de qualquer condicional
(`core/backend_pydualsense.py:799-815`). **Não apaga:** um `rigid(3,8)` escrito
por report cru, por fora do daemon, com o daemon **vivo** e rodando o código
**não curado**, sobreviveu a 8 s e a 30 s (`ensaios.csv:29-30`, literal dela:
*"l2 duro a todo momento e o r2 solto"*). O rumble, sob o mesmo keepalive de
0,5 s, morria em menos de meio segundo. **São mecanismos diferentes**, e o
keepalive está inocentado para o gatilho (`ensaios.csv:37`).

### 2.3 A lightbar — verde puro nos três, com a mesa vazia ANTES da probe

**GRAU: MEDIDO.** Ensaio `lightbar-probe-limpa` (`ensaios.csv:41`).

É **o ensaio mais limpo da noite, e o primeiro em dezesseis dias feito com a
mesa vazia ANTES da probe e não depois**. A ordem foi: fechar o Steam, parar o
daemon, conferir que **nenhum processo tinha descritor de hidraw aberto**, e só
**então** ela acordou os três controles.

- Os três nasceram **acesos** — *"os 3 estão azuis"*, que é o azul que o driver
  pinta sozinho na probe.
- Escrito **verde puro** (`0 255 0`) por sysfs, com o daemon parado, os **três**
  obedeceram. Literal dela: *"todos verdes"*.

Duas coisas fazem essa medição valer mais que as anteriores:

1. **A cor é arbitrária.** Verde puro não é padrão nenhum do driver. Provar
   obediência de cor exige uma cor que **ninguém mais queira** — foi o que
   faltou nas tentativas anteriores.
2. **As três revisões de hardware estavam representadas** (`0x0710`, `0x1111` e
   `0x0711`). A suspeita de *revisão de hardware* cai **com prova, não por
   argumento**.

---

## 3. O SUSPEITO QUE NINGUÉM TINHA OLHADO EM DEZESSEIS DIAS: o Steam

**GRAU: MEDIDO.** Ensaios `lightbar-probe-suja-steam` e
`lightbar-steam-nunca-foi-suspeito` (`ensaios.csv:42-43`).

Com o daemon **parado**, `readlink` sobre `/proc/*/fd` mostrou o processo
`steam` com `/dev/hidraw4`, `/dev/hidraw5`, `/dev/hidraw6` e `/dev/hidraw7`
abertos, e o `/proc/PID/fdinfo` confirmou **leitura+escrita** nos quatro.

**Reproduzido de novo enquanto esta página era escrita**, com o daemon
`inactive`:

| descritor | dispositivo | `flags` em `fdinfo` |
|---|---|---|
| 105 | `/dev/hidraw4` | `02000002` |
| 106 | `/dev/hidraw5` | `02000002` |
| 150 | `/dev/hidraw6` | `02000002` |
| 91 | `/dev/hidraw7` | `02000002` |

Os dois bits baixos de `02000002` são `O_RDWR`. **Não é um leitor curioso: é um
escritor.** E o Steam Input tem suporte nativo a DualSense e **pinta lightbar** —
o que a casa já tinha escrito em
[`pilha-steam-input-xpad-sdl.md`](../../protocol/pilha-steam-input-xpad-sdl.md)
e ninguém tinha ligado a este defeito.

**O contraste que fecha a conta**, medido seis minutos antes com **os mesmos
três controles** (`ensaios.csv:42`): naquela rodada eu tinha fechado o Steam
**depois** de eles subirem, então a probe aconteceu com o Steam vivo e com
`hidraw4..7` abertos em leitura+escrita. Resultado: **só um dos três obedeceu ao
verde**. E o mesmo controle branco (hw `0x0711`) que obedeceu ali **não** tinha
obedecido ao magenta numa instância anterior.

| | probe com o Steam vivo | probe com a mesa vazia |
|---|---|---|
| controles acordados | os mesmos três | os mesmos três |
| transporte | rádio | rádio |
| daemon | parado nos dois casos | parado nos dois casos |
| obedeceram ao verde | **1 de 3** | **3 de 3** |

Mesmo controle, mesma revisão, mesmo transporte, mesmo dia, resultados opostos.
**O que muda entre as duas rodadas não é o controle, nem o transporte, nem a
ordem de subida: é quem estava com o hidraw aberto no instante da probe.**

### O preço: isto contamina o passado

**GRAU: MEDIDO quanto ao fato; INFERIDO quanto ao alcance.**

Dezesseis dias de investigação perseguiram, um a um: o `0x08`, o keepalive, a
adoção por Bluetooth, o cache do sysfs, a **instância de conexão** e a revisão
de hardware. **E o Steam esteve com a caneta na mão o tempo inteiro — inclusive
durante as medições que concluíram cada uma daquelas hipóteses.**

Isso **contamina retroativamente toda leitura de lightbar feita com o Steam
aberto**, o que inclui a noite inteira de 11/08 até o momento em que ele foi
fechado (`ensaios.csv:43`). Não significa que aquelas leituras estejam erradas;
significa que **elas não isolam nada**, porque a variável que hoje sabemos ser
decisiva estava livre em todas.

**É a armadilha 7 da casa em escala grande** — só um lado do ensaio, seis vezes
seguidas — com um agravante: nem sabíamos que havia um lado.

---

## 4. Os erros de método desta noite, e eles são meus

**GRAU: MEDIDO.** Cada um tem linha de ensaio ou linha de arquivo, e cinco deles
já viraram armadilha numerada em
[`METODO-DE-ISOLAMENTO.md`](../METODO-DE-ISOLAMENTO.md).

Esta seção existe porque é ela que a casa aprende. Registrar o acerto é
inventário; registrar o erro é método.

### 4.1 Registrei obediência do lado que não testei

Marquei `gatilho.direito` como `O APARELHO OBEDECEU` porque o **R2 ficou solto**
enquanto o L2 endurecia. Aquilo prova que o comando **não vazou de lado** — é
controle negativo, item **C3** do checklist. **Não prova que o lado direito
obedece.** Ela pegou.

**O custo foi baixo só por sorte:** a suspeita de que o mapeamento estivesse
invertido foi levantada e eliminada na mesma rodada, autorizando de fato o
direito (`flag0 0x04`, bloco `common[10..19]`) — o R2 endureceu e o L2 ficou
solto, literal dela *"r2 duro, l2 solto"* (`ensaios.csv:36`). O mapeamento do
produto está **certo**. Mas a linha do mapa esteve escrita **antes** desse
ensaio existir. Virou a **armadilha 10**: *confundir controle negativo com
prova*.

### 4.2 Copiei para o caderno uma afirmação que só existia em docstring

Registrei como **medição** uma frase que morava numa docstring
(`cli/cmd_lightbar_reset.py:18-20`): *"cinco dias e vinte adoções por Bluetooth
sem nenhum `0x08`, e a barra continuou morta"*.

**É falsa.** A escavação do journal e dos transcritos, feita no mesmo dia em que
eu escrevi o erro, achou a barra **acesa** no rádio **dentro daqueles cinco
dias, quatro vezes**, três delas com fala literal dela (`ensaios.csv:28`,
`:31-34`):

| quando | o que ela disse | por que conta |
|---|---|---|
| 08/08 16:39 | *"roxo tá com lightbar verde"* | uso normal, sem gesto nenhum; o roxo estava no rádio |
| 08/08 21:35 | *"roxo lightbar laranja player 1"* | uso normal |
| 08/08 23:48 | *"o branco tá conectado led player 1 e lightbar vermelho"* | **o mais forte**: adoção BT sem `0x08`, e vermelho não é a cor que o driver pinta na probe — a cor era **nossa**, e casa com `lightbar_reassert` no journal |
| 11/08 11:40 | *"dualsense roxo aceso em azul (lightbar)"*, com foto | no boot de hoje e com o binário do driver de hoje |

Virou a **armadilha 12**, e é a mais silenciosa de todas: *o caderno não erra
sozinho — ele fica certo sobre o dia em que foi escrito*. Uma medição que só
existe em docstring faz o `scripts/eliminacao.py` acusar com autoridade um
culpado removido do produto há sete dias.

### 4.3 Desenhei dois ensaios que pediam cronômetro à mão dela

As duas primeiras rodadas do ensaio do keepalive pediam que ela
**cronometrasse** em que instante o motor mudou. Uma respondeu *"parou no meio"*
e a outra *"6 segundos eu acho"* — e **as duas são incompatíveis entre si**: na
segunda, o motor teria parado **antes** de o report sair (`ensaios.csv:25`).

**O defeito é do instrumento, não dela.** Um ensaio que exige da mão humana uma
precisão que a mão não dá já falhou no desenho, e a saída não é repetir com mais
cuidado — é **redesenhar para que a resposta seja sentida, e não medida**. O
desenho de **troca de lado** fechou numa rodada o que duas rodadas não fecharam:
*ou muda de mão, ou não muda*.

As duas rodadas descartadas estão **registradas como descartadas**, com o
motivo — é o item **F1** do checklist. Sem esse registro, a próxima pessoa
repete o ensaio ruim. Virou a **armadilha 8**; e a irmã dela, a **9**, é o mesmo
defeito por outro lado: *ela não vê a janela do comando*, então o "aperte agora"
só chega depois que o comando terminou.

### 4.4 Quase concluí `não obedece` para a lightbar porque escrevi verde com o daemon vivo

Na primeira tentativa de provar a cor arbitrária, escrevi verde com o **daemon
vivo**. Ela respondeu *"não ficou... ainda tá azul"*. **Eu quase registrei `não
obedece`** (`ensaios.csv:40`).

O cache tinha voltado para `[0 0 255]` em menos de um minuto: o daemon reescreveu
**a cor dele** por cima. E azul era justamente a cor que ele queria — ou seja, a
barra **estava** obedecendo, só que **a ele**. Só com o daemon parado o verde
passou.

**Sem o teste de cor arbitrária com o daemon fora, este ensaio teria concluído o
oposto do que é verdade.** A regra que fica: para provar obediência de cor, use
cor que **ninguém mais queira**, e com o daemon parado.

### 4.5 Ia registrar "a instância de conexão é a causa" — e ela me parou

Depois de derrubar o controle roxo pelo BlueZ e vê-lo voltar aceso, eu ia
escrever que a causa era **a instância de conexão**. O alerta dela, literal:

> *"não é só instância de conexão, se escavar o projeto vai ver que isso é um
> falso positivo recorrente"*

**Ela estava certa.** `reconectar cura` já foi concluído nesta casa e derrubado
depois — **quatro vezes desde 17/07** (`ensaios.csv:38-39`). A instância era
**proxy**: o que ela carregava junto era **quem estava com o hidraw aberto na
probe**. Nas duas rodadas daquele par o Steam estava vivo com `hidraw4..7` em
leitura+escrita, **e eu não sabia**.

Os dois ensaios foram **reclassificados em 12/08** para o suspeito certo. E o
próprio `scripts/eliminacao.py` já recusava fechar aquele suspeito: devolvia
`CONFUSO`, porque o mesmo lado dava resultados diferentes. **O instrumento
estava certo e eu ia escrever por cima dele.**

---

## 5. O que a memória dela acertou e o repositório não tinha

**GRAU: MEDIDO** nos três casos, e é o padrão que interessa, não o placar.

Três vezes nesta sessão a memória dela afirmou algo que a minha leitura do
repositório não sustentava — e **nas três ela estava certa, e a leitura estava
incompleta**.

| o que ela afirmou | o que o repositório dizia | o que se mediu |
|---|---|---|
| **que os quatro vibravam por Bluetooth jogando** | a célula `combinacao.rumble_simultaneo` estava **muda** — até esta noite nenhum instrumento da casa sabia mirar mais de um controle por vez (`scripts/ensaio_rumble_em_par.py`, docstring) | quatro controles, janela de **0,0 ms**, daemon parado: *"sim vibraram todos"*, duas rodadas (`ensaios.csv:20`) |
| **que "reconectar cura" é falso positivo recorrente** | eu ia registrar a instância de conexão como causa | derrubado quatro vezes desde 17/07; o suspeito real é o escritor com o hidraw aberto na probe (`ensaios.csv:38-39`) |
| **que os controles conectavam e acendiam no rádio** | uma docstring afirmava cinco dias de barra morta (`cli/cmd_lightbar_reset.py:18-20`) | **quatro acendimentos** dentro daqueles cinco dias, três com fala literal dela (`ensaios.csv:28`, `:31-34`) |

**A leitura que fica, e ela não é elogio — é procedimento:** quando a memória
dela contradiz o repositório, **a hipótese de trabalho é que o repositório está
incompleto**, e a próxima ação é escavar antes de argumentar. Nos três casos a
escavação levou minutos e produziu linha de ensaio; o argumento teria produzido
mais um documento errado com autoridade.

---

## 6. O que o caderno diz hoje — inclusive onde ele recusa fechar

**GRAU: MEDIDO** — saída de `.venv/bin/python scripts/eliminacao.py` sobre as 42
linhas, rodada para esta página.

| chave e transporte | veredito do caderno | o que falta |
|---|---|---|
| `vibracao.rumble.ff` [cabo] | **É A CAUSA** — o daemon escrevendo no mesmo hidraw | — |
| `vibracao.rumble.ff` [rádio] | **É A CAUSA** — idem | — |
| `vibracao.rumble.esquerdo` [rádio] | **É A CAUSA** — `common[3]` (strong) | — |
| `vibracao.rumble.direito` [rádio] | **É A CAUSA** — `common[2]` (weak) | — |
| `combinacao.rumble_simultaneo` [cabo] | inconclusivo | um ensaio **com** o suspeito |
| `combinacao.rumble_simultaneo` [rádio] | inconclusivo | um ensaio **sem** o suspeito |
| `gatilho.esquerdo.adaptativo` [cabo] | inconclusivo | um ensaio **sem** o suspeito (há 3 só com) |
| `gatilho.direito.adaptativo` [cabo] | inconclusivo | um ensaio **sem** o suspeito |
| `luz.lightbar.cor` [cabo] | inconclusivo | um ensaio de cada lado |
| `luz.lightbar.cor` [rádio] | **CONFUSO** | o mesmo lado deu resultados diferentes |

**Duas leituras honestas desta tabela, e elas importam mais que os quatro
`É A CAUSA`:**

1. **O Steam ainda NÃO está fechado como causa.** No suspeito *escritor com o
   hidraw aberto na probe* o caderno tem cinco ensaios — `com` deu
   `não obedece`, `parcial`, `não obedece`; `sem` deu `obedece`, `obedece`. O
   `parcial` no lado `com` é o que faz o instrumento devolver `CONFUSO`, e ele
   está certo em recusar: **um `parcial` é exatamente o que ainda não foi
   explicado**. O que está medido é que o Steam **escreve** e que a probe limpa
   muda o resultado de 1 em 3 para 3 em 3. O que **não** está medido é a volta —
   reproduzir a falha com o Steam vivo na probe, de propósito.
2. **`gatilho` aparece só em `[cabo]`.** As três linhas de gatilho em
   `ensaios.csv` são todas do cabo, porque foram a sub-investigação do
   keepalive. O aceite dela nos **dois** transportes existe, e é sólido, mas
   mora na célula do mapa (`provado_em = 2026-08-11`) e **não** em linha de
   ensaio. Ver a seção 8.

---

## 7. O que continua aberto, sem maquiar

**GRAU: cada item declara o seu.**

1. **A volta do ensaio da lightbar. [MEDIDO que falta]** O item **D1** do
   checklist pede ida **e** volta: tirar o suspeito e ver curar, **devolver e
   ver o defeito voltar**. A ida está feita (mesa vazia → 3 de 3). A volta —
   subir os controles **com o Steam vivo e com o hidraw aberto de propósito** —
   **estava em curso quando dois controles caíram sozinhos do rádio** e a
   bancada acabou ali. **Só a volta distingue causa de coincidência.**
   *(A queda dos dois controles é `RELATO DA SESSÃO`: aconteceu na bancada e não
   virou linha de ensaio. Cair por Bluetooth já está registrado nesta casa como
   rotina, e não há medição desta noite que a atribua a qualquer coisa.)*
2. **O elemento específico do gatilho não está isolado. [MEDIDO que falta]** É a
   pergunta **F5**, a que fecha assunto: *o elemento específico que faz ele
   funcionar de fato está isolado?* Sabe-se que o conjunto funciona; **não** se
   sabe de qual bit de autorização (`flag0 0x04` direito, `0x08` esquerdo) ou de
   qual byte o aparelho depende. É exatamente onde o rumble estava na manhã de
   11/08 — e o rumble só encolheu o produto depois de responder isso.
3. **Sete dos oito modos de gatilho nunca foram tocados. [MEDIDO que falta]** Um
   modo só foi exercitado, `Rigid`, com **um** jogo de parâmetros (posição 3,
   força 8).
4. **Há algo que apaga o efeito de gatilho com período de MINUTOS. [MEDIDO o
   fenômeno, SEM SUSPEITO NOMEADO]** Três rodadas, mesmo comando, só o tempo
   mudou — **e o resultado não é monotônico** (`ensaios.csv:37`): aos 8 s L2
   duro / R2 solto; aos 30 s L2 duro / R2 solto; aos **120 s** L2 **solto** e R2
   **vivo**. Literal dela: *"r2 vivo durante os dois minutos l2 não"*. O
   keepalive de 0,5 s está inocentado — se fosse ele, o efeito morreria antes
   dos 8 s, como o rumble morria. Os candidatos a investigar **pelo código** são
   o tick do daemon (30 s, fatiado em 2 s) e o `reassert_resolved_outputs`, que
   roda a cada tick. **Nada disso foi medido.**
5. **O cancelamento é total com dois alvos e apenas parcial com quatro.
   [MEDIDO, NÃO EXPLICADO]** Com o daemon vivo e **quatro** alvos os quatro
   vibraram, porém *"por duração diferente"* (`ensaios.csv:21`); com **dois**
   alvos o cancelamento é total. O contraste está registrado de propósito, sem
   explicação, porque explicação sem medição vira folclore com data.
6. **A cura do rumble e a mordida dela. [MEDIDO que falta]** A célula
   `vibracao.rumble.ff` do mapa tem `teste_que_morde` preenchido e
   `mordida_provada_em` **vazio** — ninguém arrancou a cura do arquivo de
   produção e viu reprovar. É o item **F2**, e é o que impede tudo isto de
   voltar na próxima mexida.
7. **A poda não foi feita. [MEDIDO que falta]** É o item **F4** e o passo 7 do
   ciclo — a metade que dá lucro. O que foi inocentado pode **parar de ser
   acionado**, e nada saiu do produto nesta sessão.

---

## 8. O que esta página NÃO afirma

A casa separa medido de inferido, e é isso que dá valor ao arquivo. As
ressalvas, nominalmente:

- **Não afirmo que o Steam é a causa da lightbar travada.** Está medido que ele
  escreve, e que a probe limpa muda o desfecho de 1 em 3 para 3 em 3. O caderno
  devolve `CONFUSO` para esse suspeito, e ele está certo em devolver.
- **Não afirmo que o `0x08` está inocente pelo motivo que a docstring dava.** O
  `0x08` está **ausente** nos dois desfechos — nos quatro acendimentos de 08 e
  11/08 e no contraponto de 11/08 23h00, em que os dois do cabo acenderam e os
  dois do rádio não (`ensaios.csv:35`). Um suspeito ausente dos dois lados
  **não explica nada**, e é por isso que ele sai do banco dos réus — pela razão
  **oposta** à que eu havia escrito.
- **Não afirmo que "azul" prova cor nossa.** No acendimento de 11/08 11:40
  *"azul"* não distingue a nossa cor (`0,0,255`) da que o driver pinta na probe
  (`0,0,128`). Aquilo prova que a barra **não estava travada**, e nada mais
  (`ensaios.csv:34`).
- **Não afirmo que a leitura de gatilho no rádio tem linha de ensaio.** Tem
  aceite dela, com fala literal e com o `--mode Off` medido, registrado na
  célula do mapa. **Não tem linha em `ensaios.csv`** — por isso o
  `scripts/eliminacao.py` só enxerga `[cabo]`. **É dívida de registro, não de
  medição**, e ela deve virar linha antes que alguém leia a ausência como
  ausência de prova.
- **Há uma divergência de data no próprio caderno, e ela fica dita.** As três
  linhas do bloco do Steam trazem `quando = 2026-08-12T23:20:00`, enquanto a
  nota de uma delas descreve a contaminação como *"a noite inteira de 11/08 até
  23h13"*. Uma das duas está errada, e não sei qual sem o journal na mão — então
  **não escolhi por conta própria**. Quem for reconciliar o caderno, comece por
  aqui.

---

## 9. A frase da noite

**O suspeito mais caro não é o que se investiga e se descarta — é o que nunca
entra na lista.**

Dezesseis dias, seis hipóteses, dezenas de ensaios com o olho dela, um método
escrito para não errar — e a resposta dependia de uma pergunta que o método
**faz** e que ninguém tinha feito neste elemento: *quem mais está escrevendo
aqui?* A pergunta 1 do
[`METODO-DE-ISOLAMENTO.md`](../METODO-DE-ISOLAMENTO.md) é *"o instrumento briga
com o produto?"*. Ela precisa ser lida por inteiro:

> **quem mais tem este dispositivo aberto — e com que permissão?**
