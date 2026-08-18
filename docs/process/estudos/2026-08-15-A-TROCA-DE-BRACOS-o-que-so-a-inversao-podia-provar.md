# A troca de braços — o que só a inversão podia provar

- **Medido em:** 15/08/2026, 19h, na máquina dela, com os **mesmos** quatro
  DualSense nos **dois** transportes, com minutos de diferença
- **Quem mediu:** ela, com a mão — desplugou os dois do cabo e religou por
  rádio, plugou os dois do rádio no cabo; os instrumentos, com o daemon vivo
- **Grau:** **MEDIDO NO APARELHO**, e o que não fechou está dito com nome
- **Brutos:**
  [`…-TROCA-DE-BRACOS-os-mesmos-quatro-nos-dois-transportes.txt`](../../data/ensaios-brutos/2026-08-15-TROCA-DE-BRACOS-os-mesmos-quatro-nos-dois-transportes.txt)
  (a mesa antes, a mesa depois, o censo de features depois) e
  [`…-TROCA-DE-BRACOS-taxa-e-0x22-depois.txt`](../../data/ensaios-brutos/2026-08-15-TROCA-DE-BRACOS-taxa-e-0x22-depois.txt)
  (a taxa depois da troca e o E-8). O "antes" da taxa é
  [`…-E2-taxa-dos-oito-nos.txt`](../../data/ensaios-brutos/2026-08-15-E2-taxa-dos-oito-nos.txt),
  da corrida das 07:43:56
- **Nota de lastro, 15/08/2026:** o segundo bruto foi versionado **junto com esta
  página**. As duas corridas que ele guarda — a taxa das 19:32 e o E-8 das
  19:33 — tinham ficado fora da árvore, e sem elas dois números daqui não
  teriam endereço. A regra desta casa é que medição citada tem endereço, e a
  correção foi versionar o bruto, não abrandar o texto

---

## 1. Por que a inversão era necessária

O [PLANO DA MESA 2+2](2026-08-15-PLANO-DA-MESA-2-2-o-que-so-se-mede-com-quatro.md)
escreveu a limitação antes dos ensaios, não depois. É a **Lei 4**, e ela diz
textualmente:

> São **dois** aparelhos por braço. Toda diferença que aparecer entre "os do
> cabo" e "os do rádio" é, a rigor, **transporte somada a unidade** — os quatro
> controles têm `hardware_version` diferentes entre si (`0x0711`, `0x0811`,
> `0x0710`, `0x1111`), e dois deles são de outra revisão de placa.
>
> Cada ensaio abaixo declara se é **IMUNE** ou **CONFUNDIDO**, e **nenhum ensaio
> confundido pode produzir célula com grau `medido` sem a troca de braços**.

Até as 19h de hoje, **toda** comparação cabo × rádio desta casa comparava
aparelhos diferentes ao mesmo tempo que comparava transportes. Isso não é
detalhe de método: é um confundimento que atravessa o mapa. Seis linhas de
`controle=dualsense` carregam hoje, escrita na própria célula, a frase que o
admite — *"a mesa tem DOIS aparelhos por braço, e nenhum aparelho trocou de
braço"*. Cinco delas contam como **pareadas** no placar. Uma comparação
confundida não é uma comparação errada; é uma comparação que **não sabe do que
está falando**, e que produz número com cara de medida.

A cura estava nomeada desde o plano e custava cinco minutos da mão dela. Ela os
gastou às 19h.

## 2. A mesa, antes e depois

| aparelho | cor | `hardware_version` | antes (07h43) | depois (19h32) |
|---|---|---|---|---|
| `d4:2f:4b:00:00:d8` | AZUL | `0x00001111` (BDM-060M) | CABO | **RÁDIO** |
| `a0:fa:9c:00:00:f0` | ROXO | `0x00000710` | CABO | **RÁDIO** |
| `44:46:48:00:00:03` | VERMELHO | `0x00000811` | RÁDIO | **CABO** |
| `14:3a:9a:00:00:ab` | BRANCO | `0x00000711` | RÁDIO | **CABO** |

O par MAC↔cor dos dois de cima é **melhor que apelido**: veio do serial lido do
firmware no E-7, sem consultar tabela nenhuma — `Starlight Blue` para o
`d4:2f:4b` e `Galactic Purple` para o `a0:fa:9c`
([`…-E7-cor-do-plastico.txt`](../../data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.txt),
linhas 54 a 58). Os dois de baixo são os apelidos de
[A ESCADA QUE RESPONDE](2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md),
conferidos com o olho dela naquele ensaio — o serial deles não saiu (`EIO` por
rádio, e o outro nem foi tentado).

**Onde está o "antes", e é honesto ser exato sobre isso.** A mesa **depois** está
inteira, os quatro aparelhos com braço, `hardware_version`, placa e bateria, na
seção **(2)** do bruto irmão — saída literal do `quem_e_quem.py` às 19h10. O
**antes** não está num arquivo só; está repartido em três, todos versionados e
todos com a mesma arrumação de braços:

| o antes de quê | onde | quando |
|---|---|---|
| a taxa dos quatro | `…-E2-taxa-dos-oito-nos.csv` | 07:43:56 |
| o custo de `GET_FEATURE` (família `0xF0`-`0xF7`) | `…-D-32-familia-f0-f7.txt` | 17h32 |
| a placa de áudio USB | `…-E5-E6-microfone_no_cabo.txt`, linhas 44-45 | manhã |
| o `hardware_version` por MAC e por braço | `…-E7-cor-do-plastico.txt`, linhas 54-58 | tarde |

A seção **(1)** do bruto irmão — *"a mesa antes da troca"* — é uma foto tirada
**no meio** da troca, com **um** controle de pé (`14:3a:9a`, no rádio). Ela vale
pelo que mostra dessa unidade, e o próprio instrumento imprime o aviso: *"SÓ UM
TRANSPORTE presente — isto NÃO é o ensaio 2+2"*. Quem citar a seção (1) como "a
mesa antes" cita uma tabela de uma linha.

## 3. A tabela do que seguiu o quê

Esta é a tabela que só a inversão podia escrever. Antes dela, cada linha só
podia dizer *"um braço deu X e o outro deu Y"*.

| o que | seguiu o | evidência (antes → depois) |
|---|---|---|
| **250,0 Hz de entrada** | **BRAÇO** (é do cabo) | `…-E2-taxa-dos-oito-nos.csv` → bruto novo, seção (1) |
| **taxa variável de entrada** | **BRAÇO** (é do rádio) | as mesmas duas corridas |
| **0,21 s por `GET_FEATURE`** | **BRAÇO** (é do cabo) | `…-D-32-familia-f0-f7.txt` → bruto irmão, seção (3) |
| **0,01 s por `GET_FEATURE`** | **BRAÇO** (é do rádio) | as mesmas duas corridas |
| **o descritor HID inteiro** | **BRAÇO** | `…-D-32…` e bruto irmão, seção (3), *"O QUE CADA TRANSPORTE DECLARA"* |
| **a placa de áudio USB** | **BRAÇO** | `…-E5-E6-microfone_no_cabo.txt`:44-45 → bruto irmão, seção (2), coluna `placa ALSA` |
| **o estado de carga** (`Full`/`Discharging`) | **BRAÇO** | bruto irmão, seções (1) e (2), coluna `bateria` — só do `14:3a:9a`, que é a única unidade com as duas fotos |
| **o `hardware_version`** | **APARELHO** | todas as corridas do dia — é o controle positivo, §6 |
| **o feature `0x22`** | **não se sabe** | bruto novo, seção (2) — o E-8 não tem "antes", §7 |

### 3.1 A taxa de entrada — o E-2 refeito, e o confundimento cai

Os **quatro** aparelhos entregaram **exatamente 250,0 Hz no cabo**, e taxa
variável no rádio. Por aparelho, nos dois braços:

| aparelho | no CABO | no RÁDIO |
|---|---|---|
| `d4:2f:4b` | **250,0 Hz** (5000 em 20 s, às 07h43) | 279,1 Hz (5582 em 20 s, às 19h32) |
| `a0:fa:9c` | **250,0 Hz** (5001 em 20 s, às 07h43) | 157,8 Hz (3157 em 20 s, às 19h32) |
| `44:46:48` | **250,0 Hz** (5000 em 20 s, às 19h32) | 381,5 Hz (7631 em 20 s, às 07h43) |
| `14:3a:9a` | **250,0 Hz** (5000 em 20 s, às 19h32) | 191,4 Hz (3828 em 20 s, às 07h43) |

- **No cabo:** report `0x01`, 64 B, quatro de quatro em 250,0 Hz. E há **régua
  independente**: o endpoint de interrupção **declara** o intervalo. O E-1 leu
  `ep_03` e `ep_84` com `interval=4ms` nos dois controles que estavam no fio de
  manhã (`…-E1-topologia-do-fio.txt`, linhas 51 a 55) — 4000 us são 250 Hz, o
  `bInterval 6` em High Speed que
  [o driver `hid-playstation` por dentro](../../protocol/driver-hid-playstation.md)
  registra na seção do descritor USB. O número não vem só da contagem; vem
  também da declaração do barramento, e as duas batem. **A ressalva:** o E-1
  rodou antes da troca, então a declaração do endpoint foi lida em duas das
  quatro unidades. O que a troca acrescenta é que as **outras duas**, ao entrar
  no mesmo braço, entregaram o mesmo 250,0 Hz contado.
- **No rádio:** report `0x31`, 78 B, faixa de **157,8 a 381,5 Hz** — mais de 2×
  entre os extremos, e a variação **não acompanha a unidade**: o `d4:2f:4b` deu
  279,1 e o `a0:fa:9c` deu 157,8 na **mesma janela**, e nos dois casos com o
  mesmo cabo-que-não-existe.

**A conclusão que só a inversão autoriza:** os 250,0 Hz são do **cabo**; a
variabilidade é do **rádio**. Nenhum aparelho escapa de um nem do outro. Isso
transforma *"cada braço entregou X"* em *"cada transporte entrega X"* — que é o
enunciado que o mapa precisa e que nenhuma medição anterior tinha o direito de
escrever.

O empate perfeito dos dois do cabo (5000 relatórios contados, os dois) fez o
próprio instrumento levantar a mão com um controle negativo — *"confira se não é
o mesmo nó lido duas vezes"*. Os nós são distintos (`hidraw8` e `hidraw10`), os
MAC são distintos, e a corrida das 07h43 já tinha dado 5000 e 5001 nos **outros**
dois. O empate é do produto, não do instrumento.

### 3.2 O descritor HID — segue o braço, byte a byte

Os **9 reports declarados por um transporte só** são os **mesmos** antes e
depois da troca:

    só no CABO:   0x0a, 0x0c, 0x21, 0x84, 0x85, 0xa0, 0xe0
    só no RÁDIO:  0xf6, 0xf7

A união continua **24**. O cabo declara 22, o rádio 17, e **nenhum conjunto é
subconjunto do outro**. A tabela *"O QUE CADA TRANSPORTE DECLARA"* sai idêntica
nas duas corridas — na D-32 das 17h32 (`…-D-32-familia-f0-f7.txt`, a partir da
linha 92) e no bruto irmão, seção (3) — com os pares de unidades **trocados**
entre elas.

**O descritor é do TRANSPORTE.** Não existe "a lista dos feature reports do
DualSense" — existe **uma por transporte**. Antes da troca isto era uma
afirmação sobre dois pares de aparelhos; agora é uma afirmação sobre dois
braços, com os mesmos quatro aparelhos dos dois lados.

Esta é também a armadilha que o `censo_features.py` documenta ter caído: a
primeira versão dele tirava a lista de reports do **primeiro** aparelho e a
aplicava a todos, de modo que os exclusivos do outro transporte nunca eram
pedidos. Hoje ele usa a **união** dos descritores e imprime quem declara o quê
antes de ler qualquer coisa.

### 3.3 A placa de áudio USB — segue o braço

De manhã, `card2` (`Controller`) e `card3` (`Controller_1`) nasciam de
`d4:2f:4b` e `a0:fa:9c`
([`…-E5-E6-microfone_no_cabo.txt`](../../data/ensaios-brutos/2026-08-15-E5-E6-microfone_no_cabo.txt),
linhas 44-45). Depois da troca, `card2` e `card3` nascem de `44:46:48` e
`14:3a:9a` — os que estão no cabo **agora** (bruto irmão, seção (2), coluna
`placa ALSA`). **Os mesmos dois índices de placa, outros dois aparelhos.** Os
dois do rádio não expõem placa nenhuma, **seja qual for a unidade**.

Isto já era a conclusão de 15/08 de madrugada, e continuava confundida: era
possível — improvável, mas possível — que aquelas duas unidades tivessem placa e
as outras duas não. Agora não é mais possível.

## 4. O achado que INVERTE a crença da casa: o custo de `GET_FEATURE`

Este é o caso pedagógico da página.

78 leituras, quatro aparelhos, os dois braços (bruto irmão, seção (3)):

| aparelho | no CABO | no RÁDIO |
|---|---|---|
| `d4:2f:4b` | 0,21 s | 0,01 s |
| `a0:fa:9c` | 0,21 s | 0,01 s |
| `44:46:48` | 0,21 s | 0,01 s |
| `14:3a:9a` | 0,21 s | 0,02 s |

**O custo trocou de lado junto com os braços, sem exceção.** O rádio é **~20×
mais rápido que o cabo** para ler feature. E o 0,21 s do cabo é notavelmente
estável: `min = max = 0,21` em **44** leituras de cabo, o que tem cara de
**temporizador**, não de contenção — nem o `0xf6` de 547 B por rádio (0,01 s a
0,05 s) chega perto.

**E o 0,21 s já estava no bruto de duas horas antes, com as OUTRAS unidades no
cabo.** A corrida D-32 das 17h32 — braços originais, `d4:2f:4b` e `a0:fa:9c` no
fio — leu a família `0xF0`-`0xF7` e deu **0,21 s em dez de dez leituras de
cabo** contra **0,01 a 0,07 s nas catorze de rádio**
([`…-D-32-familia-f0-f7.txt`](../../data/ensaios-brutos/2026-08-15-D-32-familia-f0-f7.txt),
linhas 127 a 165). Ou seja: **o 0,21 s reproduz em duas corridas independentes,
com pares de unidades diferentes no cabo em cada uma** — e é isso que o
transforma de curiosidade em constante do braço.

Vale dizer o que isso significa sobre a nossa própria leitura: o número já
estava versionado às 17h32 e **ninguém olhou para ele**. A célula do mapa
escrita a partir dessa mesma corrida registrou que o **rádio** era rápido e
passou ao largo de que o **cabo**, ali do lado, era vinte vezes mais lento. Não
foi falta de dado; foi falta de pergunta.

### 4.1 O que estava escrito, e cai

Três células do mapa (`identidade.leitura_de_feature`, `identidade.firmware`,
`plataforma.feature_f6`, coluna `radio_comando`) e o docstring de
`scripts/ensaios/censo_features.py` afirmavam que o **rádio** era o braço caro:
*"cada falha de `GET_FEATURE` por rádio custa 3,2-3,7 s; a cura é REPETIR"* — e
uma delas chamava isso de *"regra que vale para toda medição futura desta
casa"*.

Medido: o braço caro é o **cabo**, por um fator de vinte.

### 4.2 Como a crença nasceu — e ela não nasceu de erro

Isto importa mais que o número, porque a crença nasceu de uma medição **boa**.

Na manhã de 15/08 o censo dos dezessete features rodou com os quatro aparelhos
**por rádio**. Ali o `REPORT_REQ_TIMEOUT` de 3 s do BlueZ **bateu de verdade**:
dois dos quatro responderam na primeira tentativa e um só respondeu na
**quinta**, e cada falha custou os 3,2 a 3,7 s de relógio de parede que a
assinatura descreve. Nada disso é falso, e nada disso foi desmedido hoje.

O erro está no **salto**: de *"quando falha, custa 3 s"* para *"ler por rádio
custa 3 s"*. A amostra que sustentava o salto tinha uma propriedade que ninguém
declarou — **ela era só do rádio**. Sem o outro braço na mesma janela não havia
como perceber que o caso de 3 s era a **exceção**, nem como comparar o regime
normal do rádio com o regime normal do cabo. A generalização foi feita sobre a
metade da mesa que estava disponível, e virou "regra da casa" numa frase.

É a mesma forma de erro que a Lei 4 descreve, só que no eixo do tempo em vez do
eixo da unidade: **generalizar a partir de um braço só**.

### 4.3 A ressalva honesta, que TEM de entrar junto

O timeout de ~3 s do BlueZ **existe** e **foi observado**, na manhã de 15/08. O
que caiu é que ele seja o **regime normal**. O retry é **seguro de vida, não
pedágio** — e continua justificando o `feature_retries` do DKMS desta árvore,
que não muda.

O lastro do regime normal: **24 leituras** da corrida das 17h32 (a D-32) **mais
78** desta — **102 leituras**, todas na **primeira tentativa**, **nenhum**
retry, nos dois braços e com os quatro aparelhos passando pelos dois.

Quem orçar 3 s por leitura desenha o ensaio em cima de um custo que não existe.
Quem tirar o retry perde a leitura no dia em que o timeout bater.

## 5. A tabela do que o firmware não entrega, e é datável

Cinco reports são **declarados no descritor do CABO** e devolvem `EPIPE` na
leitura, nos dois aparelhos do cabo: `0x0a`, `0x0c`, `0x21`, `0x84`, `0xa0`.

`EPIPE` não é silêncio nem timeout: é o aparelho respondendo **"não tenho"**.
É resposta definitiva, e por isso é datável — a lista vale para o firmware
`0x0110002a` destes aparelhos, em 15/08/2026. O descritor promete; o firmware
não entrega. Quem ler o descritor como inventário de capacidades escreve cinco
linhas erradas com convicção.

## 6. O controle positivo da inversão — o `hardware_version` que NÃO mudou

O `0x00001111` continua colado no `d4:2f:4b`, esteja ele no braço que estiver.
Idem para os outros três — e os quatro pares MAC↔`hardware_version` estão
versionados **dos dois lados** da troca: no E-7
([`…-E7-cor-do-plastico.txt`](../../data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.txt),
linhas 54 a 58) com a arrumação de braços da tarde, e no bruto irmão, seção (2),
com ela invertida. **As quatro linhas batem, e só o braço mudou.**

**É ele que valida tudo o mais desta página.** A inversão inteira se apoia numa
suposição frágil: a de que o instrumento sabe qual aparelho é qual depois de ela
mexer nos cabos. Se o `hardware_version` tivesse **mudado** de MAC, uma de duas
coisas seria verdade — ou o instrumento estava trocando os rótulos, ou o
`hardware_version` também é do braço. Nos dois casos **nenhuma** conclusão
acima valeria, porque nenhuma das linhas da tabela do §3 poderia ser atribuída
a braço ou a aparelho.

É o mesmo papel do controle negativo do `btmon` sem root em
[O PAR QUE FALTAVA](2026-08-15-O-PAR-QUE-FALTAVA-o-doente-e-o-sao-no-mesmo-radio.md):
o que separa "medição" de "leitura de nada". Um experimento de inversão sem
âncora que **não** inverte não é um experimento — é uma tabela de rótulos
embaralhados.

## 7. O que NÃO fechou

**O E-8 — o feature `0x22`.**

A metade **IMUNE** respondeu: o `0x22` difere nos **quatro** aparelhos (quatro
valores em quatro), e por isso é candidato a **identidade de unidade** — está no
bruto novo, seção (2).

A metade **CONFUNDIDA não fecha**, e a razão é constrangedoramente simples: **o
E-8 nunca rodou antes da troca.** Estava planejado e não foi executado às 07h43.
Sem o "antes" por unidade, não se pode dizer se o `0x22` segue o **aparelho** ou
o **braço** — as duas hipóteses explicam igualmente bem "difere nos quatro",
porque os quatro estão em braços diferentes de manhã e de noite.

**Esta ressalva tem de viajar com a célula.** Um `0x22` que difere nos quatro
parece identidade de unidade e pode ser envelope de transporte.

**O custo de fechar:** trocar os braços **de volta** e rodar o E-8 nos quatro —
**cinco minutos da mão dela**, e nada mais. Nenhum instrumento novo, nenhuma
escrita em aparelho, nenhum risco. É a medição mais barata em aberto neste
momento, e é a única coisa que separa um candidato a identidade de unidade de
mais um número confundido.

## 8. O que isto habilita

A **Tabela de Roseta** — que **ainda não está neste repositório**, e mora fora
dele, em
`/mnt/Apate/Desenvolvimento/_recuperacao-2026-08-15/roseta/A-TABELA-DE-ROSETA.md`
— repartiu as 106 linhas de `controle=dualsense` do mapa em **97 pareáveis** e
**9 que saem por construção** (não há CRC no envelope USB, não há bond a
esquecer no fio, não há sniff no fio…). Enquanto ela estiver fora da árvore,
este parágrafo é a única cópia do número dentro dela.

**O placar de hoje, contado no CSV** (régua declarada: `cabo_de_onde_sei` **e**
`radio_de_onde_sei` iguais a `medido`, sobre as 97 do alvo):

> **29 das 97 linhas pareáveis estão pareadas em `medido/medido`.**

**Quantas a inversão destrava: zero — e não é isso que ela faz.** A troca de
braços **não fecha par nenhum**, e é honesto dizer isso na primeira linha em vez
da última. O que ela faz é outra coisa, e é o que sustenta o resto do plano:

1. **Descontamina 5 das 29 que já contam como pareadas** —
   `combinacao.cabo_e_radio.entrada`, `combinacao.cabo_e_radio.taxa`,
   `combinacao.tres_na_mesa`, `movimento.acelerometro` e
   `movimento.giroscopio.taxa`. As cinco carregam hoje, na ressalva, a frase do
   confundimento. Elas contavam como pareadas **estando confundidas**;
   passam a contar por direito. Uma sexta linha,
   `combinacao.dois_no_radio.crc`, carrega a mesma frase e está **fora** das 97
   por construção — a pergunta dela é sobre dois no rádio, e não há equivalente
   no fio.
2. **Substitui um fato errado em 3 outras** — `identidade.leitura_de_feature`,
   `identidade.firmware` e `plataforma.feature_f6`, cuja coluna `radio_comando`
   ainda descreve o rádio como o braço caro (§4).
3. **Valida o método de tudo o que vier depois.** Sem a inversão, todo ensaio
   comparativo da mesa 2+2 mede *unidades* e escreve *transportes* — o que é
   precisamente a Lei 4. Com ela, o desenho 2+2 fica autorizado a produzir grau
   `medido` em ensaio **confundido**, que é o que a Lei 4 proibia.

O ganho não aparece no placar porque o placar conta pares, e o que a inversão
entrega é **verdade nos pares que já estavam contados**. Um mapa que conta 29
pareadas com 5 confundidas vale menos que um que conta 29 com zero.

## 9. O que ficou fora desta página, e é dívida

- **O E-8 sem "antes"** (§7). Cinco minutos da mão dela.
- **As oito células do mapa** listadas no §8 continuam com o texto de ontem.
  Esta página é o endereço da prova; **escrever nas células é outro território**,
  e não foi feito aqui.
- **A cor do plástico dos dois que agora estão no cabo** (`0x0811` e `0x0711`) —
  o brinde que a troca de braços tornou possível, porque a família de fábrica
  `SET_FEATURE 0x80` só foi lida por cabo. É **escrita** em aparelho, e não se
  faz sem a palavra dela.
