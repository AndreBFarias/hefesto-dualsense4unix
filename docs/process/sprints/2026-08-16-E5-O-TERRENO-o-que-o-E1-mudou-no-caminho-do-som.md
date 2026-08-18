# E-5 O TERRENO — o que o E-1 mudou no caminho do som

> **O QUE ISTO CUSTA DE VOCÊ, e é a primeira linha de propósito:** **4 minutos de
> olho**, hoje, num ensaio novo de catorze escritas (o **E-7**, seção 6). O E-5 —
> o do Opus, o do ouvido, os 30 minutos — **não roda**, e a recomendação deste
> documento é que ele não role no desenho em que está. Se o E-7 abrir a porta, o
> E-5 volta redesenhado e custa **8 minutos seus**. Se o E-7 fechar a porta, o
> custo do E-5 passa a ser **zero**, e isso é uma economia de uma hora sua e de
> duas horas e meia de máquina.

- **Escrito em:** 16/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  com a árvore suja, os controles na mesa e a **Steam fechada**.
- **Grau:** **DESENHO.** Nada aqui foi executado. Nenhum `/dev/hidraw` foi aberto
  por esta passagem, nenhum byte foi escrito em controle nenhum, e ninguém tocou
  no hardware.
- **De onde vem:** o E-5 da
  [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md),
  relido à luz do que o E-1 mediu na madrugada de 16/08.
- **Depende de:** a **D-31** já autorizada — e o E-7 cai na faixa mais estreita
  dela, *"autoriza só o que NÃO manda payload"*. O bloqueio da família
  `0xF0`-`0xF7` (**D-32**) continua de pé e este documento não o toca.

---

## 1. A frase curta, para quem só vai ler o começo e o fim

**O E-1 não mediu o excedente do `0x32`: ele mediu o campo `reserved` do report,
e achou que ele é ignorado — que é literalmente o que "reserved" quer dizer.**

O montador do E-1 põe o recheio logo depois dos 47 bytes do `common`, no offset
`[50]`. A `struct dualsense_output_report_bt` da Sony
(`assets/dkms/hid-playstation/hid-playstation.c:351-359`) diz, byte a byte, o que
mora ali:

```
    u8 report_id;                                  [0]
    u8 seq_tag;                                    [1]
    u8 tag;                                        [2]     0x10
    struct dualsense_output_report_common common;  [3..49]  47 bytes
    u8 reserved[24];                               [50..73] <- o recheio do E-1
    __le32 crc32;
```

Os cinco recheios do E-1 caíram, todos, dentro de `reserved`. **O resultado do
E-1 é exatamente o que o fonte do driver prevê, e não precisa de hipótese
nenhuma sobre áudio para ser explicado.** Isso não torna o E-1 inútil — ele
fechou uma posição de verdade, e fechar posição é o trabalho. Torna-o **estreito
de um jeito que o desenho original não tinha percebido**.

E há uma segunda coisa, que é a que muda o rumo:

**O critério de sucesso do E-1 era ambíguo.** *"A cor ainda obedece"* é
compatível com as duas leituras que ele queria separar:

```
   a cor obedeceu  ->  o excedente é IGNORADO                (a leitura do E-1)
   a cor obedeceu  ->  a cadeia FOI ANDADA, o bloco extra foi
                       consumido sem reclamar, e o SetState
                       que veio ANTES dele já tinha acendido  (igualmente compatível)
```

O bloco de cor vinha **primeiro**. A obediência dele não depende de nada que
esteja depois ser lido. Um ensaio em que o sensor está a montante do que se quer
medir não mede aquilo — mede a si mesmo.

**A cura é uma linha de desenho: pôr o bloco candidato ANTES da cor.** Aí a cor
obedecer passa a ser prova de que o parser andou por cima do candidato usando o
comprimento declarado. É o E-7, e ele custa 4 minutos dela.

---

## 2. Onde mais o formato poderia estar — o censo das posições

O E-1 testou **uma** posição. Este é o censo do que sobrou, com o custo de cada
uma e o que cada uma decide.

| # | posição | testada? | por que ela é candidata | o que decide |
|---|---|---|---|---|
| **P1** | `[50]`, depois do `common`, no `0x32` | **SIM — E-1, ignorado** | era a primeira a tentar | fechada. E fechada com explicação: é o `reserved[24]` do driver |
| **P2** | `[2]`, um bloco **sozinho**, sem `common` nenhum | **NÃO** — e é a que o produto já usa | é exatamente onde o `0x32` do microfone põe o `0x11\|0x80` **e funciona em produção desde 25/07** | se um bloco `0x13` sozinho em `[2]` é aceito, o container existe e o E-1 estava medindo o lugar errado |
| **P3** | `[2]` bloco candidato **+ SetState depois dele** | **NÃO** | é a única forma em que a lightbar vira testemunha do encadeamento | **é o E-7.** Decide se existe cadeia de blocos, com o olho dela e sem Opus nenhum |
| **P4** | `[51]`, se o SetState tiver `len` explícito em `[3]` | **NÃO** | o bloco do microfone é `[tag][len][valor]`; se o SetState também for, a cadeia começa **um byte depois** de onde o E-1 pôs o recheio | erro de um byte é o modo de falha mais barato desta família, e o E-1 não podia distingui-lo de "ignorado" |
| **P5** | o byte `[2]` em si — `0x10` × `0x90` × `0x11` × `0x91` | **NÃO** | ela autorizou variar; a M-7 da PONTE-UNIVERSAL desenhou a tabela-verdade | ver a seção 4: **a tabela-verdade da M-7, como está, não discrimina** |
| **P6** | o degrau `0x39` (547 B) em vez do `0x32` (142 B) | **NÃO** | é o único degrau em que a única forma de payload descrita nesta casa **cabe** | ver a aritmética abaixo. Pode ser a explicação inteira do E-1 |
| **P7** | `bit6` (`BLOCO_DUPLO = 0x40`) na tag | **NÃO** | é a linha de grau mais baixo do módulo e a que o E-5 mais consome | se dois sub-blocos de tamanho declarado existem, o `0x39` é o report deles |

### 2.1 A aritmética do P6, e ela é dura

Os bytes livres depois do SetState, no montador que o E-1 usou
(`scripts/ensaios/corpo_do_degrau.py:197-211` — `tam - 4 - 3 - COMMON_LEN`):

```
   0x32  = 142 no fio  ->   88 bytes de recheio
   0x39  = 547 no fio  ->  493 bytes de recheio
```

E o tamanho da única forma de payload de alto-falante que esta casa tem escrita
(`integrations/dualsense_bt_audio.py:221-225`, dois quadros Opus de 200 B):

```
   com BLOCO_DUPLO      [tag][len=200][200 B][200 B]  =  402 bytes
   em dois blocos       2 x ([tag][len=200][200 B])   =  404 bytes
```

```
   402  >  88    -> NÃO CABE no 0x32.  O E-1 rodou no degrau pequeno demais.
   402  <= 493   -> cabe no 0x39, com 91 bytes de folga.
```

**Isto pode ser a explicação inteira do resultado do E-1**, e é a frase que o
briefing desta frente já suspeitava. O passo 4 do E-1 declarou `len = 86` num
bloco `0x13` — um "bloco de alto-falante" de 86 bytes não é nada que o protocolo
descrito preveja. **O E-1 testou a tag certa com um tamanho que o firmware não
tem motivo nenhum para reconhecer.**

### 2.2 A linha do E-1 que NÃO fechou, e ela é a que a hipótese previa

Dos cinco recheios, quatro obedeceram limpo. O do **ruído obedeceu em 2 de 3, e
a falha não se reproduziu.**

Essa é a única observação do E-1 compatível com "há estrutura", e ela está sendo
tratada como ruído. **Num canal que ou obedece ou não obedece, uma falha em três
não é dispersão: é um evento.** Os candidatos são dois, e são separáveis: ou o
pacote se perdeu no rádio (e aí o `btmon` mostra ou não mostra o `ACL Data TX`),
ou aquele recheio específico quebrou a obediência (e aí a semente fixa permite
refazer byte a byte). **Antes de esta casa escrever "o excedente é ignorado", o
passo do ruído tem de rodar N = 10 com `btmon` ligado.** Custa 2 minutos dela e
fecha a única frouxidão do E-1.

---

## 3. O que o `dualsense_bt_audio.py` já sabe — e com que grau

Li o módulo inteiro (1286 linhas). Ele afirma seis coisas sobre a estrutura do
corpo, e **as seis não têm o mesmo grau** — tratá-las como um bloco só é o erro
que este documento existe para evitar.

| o que o módulo afirma | onde | grau, em 16/08/2026 | de onde tirou |
|---|---|---|---|
| o corpo do `0x32` é uma cadeia TLV `[tag\|flags][len][valor]` | `:28-39` (docstring) | **MEDIDO NO APARELHO** | o mic atravessa em produção desde 25/07; **refeito em 15/08** pelo `corpo_do_0x32.py` em 2 unidades do rádio, com a leitura do `common` **refutada nos dois braços**. Bruto: [`2026-08-15-E1-corpo-do-0x32.txt`](../../data/ensaios-brutos/2026-08-15-E1-corpo-do-0x32.txt) |
| `BLOCO_AUDIO_CONTROL = 0x11` liga/desliga o microfone | `:217`, `:229-230`, `:252-254` | **MEDIDO NO APARELHO** | é o caminho de produção; o controle positivo do próprio ensaio são os reports de áudio que aparecem (`0 -> 979/979`) |
| `BLOCO_PRESENTE = 0x80` é "este bloco está presente" | `:224` | **MEDIDO só para a tag `0x11`** | para qualquer outra tag, **não medido** — e a escada mostra `0x10` funcionando **sem** o bit (seção 4) |
| `BLOCO_SET_STATE = 0x10` | `:216` | **CRUZADO, e as duas fontes discordam do que ele É** | o número bate com o `DS_OUTPUT_TAG` de `hid-playstation.c:203`; mas o driver o chama de **tag de envelope** (*"Magic value required in tag field"*, `:202`; *"Exact meaning is unclear"*, `:1387`) e o módulo o chama de **tag de bloco**. Mesma constante, dois significados |
| `BLOCO_HAPTICS = 0x12`, `BLOCO_SPEAKER = 0x13` (e `0x16`) | `:218-219`, `:31` | **BAIXA — fonte única, nunca escrita por esta casa** | firmware `awalol/DS5Dongle` (MIT), conferido byte a byte contra `src/audio.cpp`/`src/main.cpp`/`src/bt.cpp` pelo autor do módulo em 25/07 |
| `BLOCO_DUPLO = 0x40` — "vêm DOIS sub-blocos do tamanho declarado", e *"é assim que o `0x39` manda dois blocos de 200 bytes de Opus"* | `:221-225` (comentário) | **NÃO MEDIDO, e nunca referenciado por linha nenhuma** | o mesmo DS5Dongle. **É a afirmação de grau mais baixo do módulo e a que o E-5 inteiro consome** |

**O que ele NÃO diz, e o silêncio importa tanto quanto o texto:**

1. **Nada sobre a ORDEM dos blocos.** O módulo monta **um** bloco, sempre em
   `[2]`, e nunca dois. **Esta casa nunca escreveu uma cadeia de dois blocos em
   report nenhum.** Toda a discussão de "onde o bloco de áudio vai" pressupõe um
   encadeamento que ninguém aqui jamais produziu.
2. **Nada sobre onde a cadeia termina.** Não há terminador declarado, não há
   contagem de blocos, não há afirmação sobre o que o firmware faz com o espaço
   que sobra.
3. **Nada sobre o `0x39`.** O módulo é inteiro sobre o `0x32` de 142 bytes. O
   `0x39` aparece uma vez, num comentário, e como fonte de terceiro.
4. **Nada sobre a taxa da SAÍDA.** O que ele mede é a **entrada**: Opus mono,
   48 kHz, quadro de 10 ms, **71 bytes** (`:193-202`). Os 200 bytes da saída
   vêm do DS5Dongle. **A entrada medida e a saída suposta diferem por 2,8x**, e
   ninguém explicou por quê.

### 3.1 Três coisas que a bancada de 15 e 16/08 acrescenta, e que o módulo não sabe

- **O alto-falante interno é MONO.** O mapa dos canais de 16/08 00h05
  (`sfx-tres-saidas-quatro-canais` no caderno) mediu: canal 0 → fone L, canal 1
  → fone R **ou** alto-falante interno sem fone, canais 2 e 3 → nada. **Mandar
  Opus estéreo para um alto-falante mono é um cheiro de desenho**, e o E-5 como
  está escrito manda ("estéreo, 48 kHz, 10 ms, CBR 160 kbps").
- **Existe uma observação de som no rádio que não replicou** (`som-no-radio-...`
  no caderno, 16/08 00h10): ela ouviu ~6 s de um timbre reconhecível vindo de um
  controle **no rádio, sem placa ALSA nenhuma**, e quatro tentativas de replicar
  deram negativo. Está aberta de propósito. **Para o E-5 isso não é curiosidade:
  é o falso positivo mais caro que este ensaio pode produzir**, e é a razão do
  controle negativo novo da seção 6.3.
- **A Steam apaga a lightbar** (medido por ela, 16/08 01h05, par de eliminação
  completo). Todo ensaio cujo sensor é a lightbar é **inválido** com a Steam
  aberta, e o sysfs **não serve** para conferir (ele leu `[0 255 0]` com a barra
  apagada e com a barra verde — guarda o pedido, nunca o aceso).

---

## 4. A contradição que ninguém tinha posto lado a lado

Duas medições desta casa, as duas no **mesmo report `0x32`**, as duas com
controle positivo e negativo, e as duas **verdadeiras**:

```
  A ESCADA (15/08, olho dela, 1 unidade)
      [2]=0x10   [3..49]=common(47)                    -> a cor OBEDECEU

  O CORPO DO 0x32 (15/08, corpo_do_0x32.py, 2 unidades)
      [2]=0x91   [3]=len=1   [4]=valor                 -> o mic OBEDECEU
                                                          e o `common` foi REFUTADO
```

**As duas formas não podem ser a mesma gramática.** Se o corpo fosse um TLV
estrito começando em `[2]`, o pacote da escada leria: tag `0x10` com bit7
**apagado**, comprimento em `[3]` = `common[0]` = `valid_flag0` = **0x00** (o
`common_da_cor` do instrumento zera esse byte, `corpo_do_degrau.py:148-160`) —
bloco vazio, e o parser cairia andando por cima do `common` como se fosse uma
sequência de blocos nulos. A cor **não acenderia**. Ela acendeu, e acendeu na cor
certa, com o RGB em `[47..49]`.

**A síntese honesta, e ela é hipótese, não medição:** o firmware entende em `[2]`
uma **tag**, e o `0x10` (SetState) tem comprimento **implícito de 47** — sem byte
de `len` — enquanto o `0x11|0x80` (AudioControl) tem `len` **explícito** em `[3]`.
Alternativa igualmente compatível: **é o bit7 que decide se um byte de `len`
segue**.

### 4.1 Por isso a tabela-verdade da M-7 não discrimina

A [PONTE-UNIVERSAL-01](2026-08-15-A-PONTE-UNIVERSAL-01-o-cabo-como-pedra-de-roseta.md)
escreve, na M-7, que *"só o `0x90` discrimina"*: se `[2]=0x90` acender, `[2]` é
campo e não constante. **O desenho mantém o `common` em `[3..49]` e troca só o
byte `[2]`.** Sob a leitura TLV que ele quer testar, esse pacote é **malformado**:
com bit7 ligado o `len` tem de estar em `[3]`, e `[3]` traz `valid_flag0`.

```
   M-7 como está:   [2]=0x90  [3..49]=common          -> não acende
                    e "não acende" é lido como "o TLV está refutado"
                    quando o pacote nunca foi um TLV válido.

   M-7 corrigida:   [2]=0x90  [3]=47  [4..50]=common  -> ESTE é o discriminador
```

**Se a M-7 rodar como está escrita, ela produz um "não" que parece medição e não
é.** É a mesma junta em que o E-1 escorregou: um ensaio que muda um campo sem
mudar o layout que aquele campo governa. A correção está incorporada aos passos
5 e 6 do E-7.

---

## 5. O E-5 ainda faz sentido? — **NÃO no desenho em que está**

Digo com todas as letras, porque a pergunta pedia isso e porque é resposta
legítima.

**O que o E-5 pressupõe, e que não está medido:**

| a premissa do E-5 | grau hoje |
|---|---|
| existe uma **cadeia** de blocos no corpo do degrau | **NÃO MEDIDO.** Nunca se escreveu dois blocos no mesmo report, aqui nem em lugar nenhum desta árvore |
| a tag `0x13` significa alto-falante | **BAIXA** — DS5Dongle, fonte única |
| o payload são **dois** quadros de **200 B** | **BAIXA** — DS5Dongle, e conflita com os 71 B medidos da entrada |
| o `BLOCO_DUPLO` existe | **NÃO MEDIDO** — comentário, nunca referenciado |
| o alto-falante aceita estéreo | **REFUTADO na prática** — o alto-falante interno é mono (16/08 00h05) |
| a webcam por FFT enxerga o alto-falante do controle | **NÃO MEDIDO, e não existe instrumento.** Não há um único script nesta árvore com FFT ou webcam |

Seis premissas, e **cinco delas caem entre "não medido" e "fonte única"**. Rodar
o E-5 assim é escrever um codificador Opus e gastar o ouvido dela para produzir,
no desfecho mais provável, a frase *"não tocou, e não sabemos qual das seis
premissas era a errada"*. É um ensaio caro que não decide nada — que é
exatamente o desfecho que esta frente foi mandada evitar.

**O que fazer no lugar:** o **E-7**, que derruba a primeira premissa — a mais
básica, a que sustenta todas as outras — com o sensor mais barato e mais honesto
que esta casa tem, que é o olho dela na lightbar. Quatro minutos. **E-5 só depois
dele, e só se ele abrir a porta.**

---

## 6. O E-7 — a cor DEPOIS do bloco

**A pergunta:** o corpo do degrau é uma **cadeia** de blocos, andada pelo
comprimento declarado, ou o firmware lê **um** bloco em `[2]` e ignora o resto?

**A sacada, e é a única coisa nova neste documento:** pôr o bloco candidato
**primeiro** e o bloco de cor **depois dele**. Aí *"a cor obedeceu"* deixa de ser
ambíguo — ela só pode obedecer se o parser tiver andado por cima do candidato.

- **Instrumento:** `scripts/ensaios/corpo_do_degrau.py`, que já existe, já tem
  teste (`tests/unit/test_ensaio_em_par_recusa_o_vpad_do_proprio_produto.py` e
  irmãos) e já recusa por construção qualquer id fora de `0x31`-`0x39`. Ganha um
  modo de **cadeia** — 35 minutos de máquina, zero dela.
- **Degrau:** `0x32` (142 B). Barato de montar, barato de ler no `btmon`, e o
  bloco candidato de 8 bytes cabe folgado.
- **Autorização:** cai na faixa **"só o que NÃO manda payload"** da D-31, que é a
  mais estreita das três que ela pôs na mesa. Nenhum byte de áudio, nenhum
  feature report, nada da família `0xF0`-`0xF7`.
- **Pré-condição obrigatória, e ela é de 16/08:** **a Steam fechada, conferida por
  processo que segura o hidraw** — não por sysfs, que não sabe o que a barra
  mostra. Se a Steam estiver aberta, o sensor deste ensaio está morto e o
  instrumento tem de **recusar rodar** dizendo isso.

### 6.1 Os passos

| # | `[2]` | `[3]` | o que vem depois | cor | o que se aprende se OBEDECER |
|---|---|---|---|---|---|
| 1 | `0x10` | — | `common` em `[3..49]` | **VERMELHO** | **controle positivo.** É a linha de base já medida. Se não acender, **pare** |
| 2 | `0x93` | `8` | 8 zeros, depois `0x10` + `common` em `[12..59]` | **VERDE** | **o achado.** O parser andou a cadeia por cima de um bloco `0x13` de 8 bytes. **A cadeia existe** |
| 3 | `0x93` | `7` | igual ao 2, `len` **uma unidade menor** | **AZUL** | só roda se o 2 acender. Se **não** acender: o `len` é lido de verdade. Se acender azul certinho: o formato é **posicional**, não TLV |
| 4 | `0x9E` | `8` | igual ao 2, com tag **desconhecida** | **AMARELO** | o parser pula bloco desconhecido pelo `len` → **TLV genérico**. Se não acender, só tags conhecidas são puladas, e a lista do módulo é a lista inteira |
| 5 | `0x10` | `47` | `common` em `[4..50]`, `len` **explícito** | **CIANO** | o SetState também aceita comprimento explícito → o corpo é TLV homogêneo |
| 6 | `0x90` | `47` | `common` em `[4..50]` | **MAGENTA** | **a M-7 refeita com o layout certo.** `[2]` é campo e não constante |
| 7 | ruído do E-1, **N = 10**, com `btmon` | | | **BRANCO** | fecha a única frouxidão do E-1 (seção 2.2) |

**Controle negativo 1:** o passo 2 com o **CRC deliberadamente errado**
(`--crc-errado`, que o instrumento já tem). **Não pode acender.**
**Controle negativo 2, novo:** o passo 2 com `[2] = 0x00` — nem tag conhecida nem
constante mágica. **Não pode acender.** Sem ele, "acendeu no passo 2" é
compatível com "o firmware acende com qualquer coisa em `[2]`".

**Apagar entre todos os passos**, e conferir o apagado, porque o firmware guarda
a cor sem reforço por mais de dois minutos (§5 da canônica) — é a armadilha que
fabrica falso positivo mais barato desta família.

### 6.2 Como cada desfecho decide o E-5

```
   passo 2 ACENDE   -> a cadeia existe. O E-5 tem onde pôr o bloco 0x13,
                       e o passo 4 diz se ele precisa ser uma tag conhecida.
                       O E-5 volta com o desenho da seção 6.3.

   passo 2 NÃO ACENDE, passo 1 ACENDE
                    -> não há cadeia no 0x32 pelo caminho do SetState.
                       Sobra a P2: um bloco 0x13 SOZINHO em [2], sem common
                       nenhum — que é a forma que o microfone já usa e que
                       funciona. O E-5 nasce com essa forma, e o preço é que
                       perde a lightbar como testemunha no mesmo pacote.

   passo 1 NÃO ACENDE
                    -> o instrumento quebrou, ou a Steam está aberta.
                       Nada do resto significa o que se pensa. PARE.
```

### 6.3 O E-5 redesenhado — o que ele passa a ser, se o E-7 abrir a porta

Não escrevo o ensaio inteiro aqui: escrevo o que **muda** em relação à
ESCADA-QUE-RESPONDE-01, porque o resto de lá continua válido.

| item | como estava | como fica, e por quê |
|---|---|---|
| **degrau** | `0x39`, "porque é o maior" | **`0x39`, por aritmética:** 402 B de payload não cabem nos 88 do `0x32` e cabem nos 493 do `0x39`. O número é o argumento |
| **posição** | o bloco `0x13` "presente" | **o `0x13` PRIMEIRO, em `[2]`, e o SetState de cor DEPOIS dele** — a lightbar continua sendo testemunha de que o parser andou por cima dos 402 bytes. Sem isso o único sensor volta a ser o ouvido dela |
| **tag** | `0x13 \| 0x80` | **duas variantes, duas cores:** `0x93` com dois blocos separados de `len` 200, e `0xD3` (`\|BLOCO_DUPLO`) com `len` 200 e dois sub-blocos. É a leitura literal do módulo, e é a primeira vez que o `BLOCO_DUPLO` seria exercitado |
| **conteúdo** | 2 quadros Opus de 200 B, **estéreo** | **MONO**, porque o alto-falante interno é mono (medido em 16/08 00h05). E **duas aritméticas**: os 200 B do DS5Dongle **e** os **71 B** que a entrada realmente usa. A segunda é gratuita — o módulo já sabe montar quadro de 71 B |
| **timbre** | seno de 440 Hz | **os dois timbres dela** do `tres_casos_de_som.py`: 180 Hz contínuo e 1300 Hz pulsado a 2 Hz. O desenho é dela, de 15/08, e já provou que resolve o relato ambíguo. **Um seno de 440 Hz é o tom mais confundível que existe**, e o próprio E-5 nomeia esse viés na linha seguinte à que o propõe |
| **controle positivo do canal** | não havia | **a cor, no mesmo pacote.** Prova que o report foi consumido, no mesmo milissegundo, sem depender de som nenhum |
| **controle positivo do OUVINTE** | **não havia, e é a lacuna mais séria** | o mesmo timbre tocado pelo alto-falante de um controle **no CABO**, que já está medido como funcionando (`sfx-canal1-e-o-alto-falante`, 15/08 23h45), gravado pela mesma webcam, na mesma distância, no mesmo minuto. **Sem isto, "não ouvi nada" é indistinguível de "o instrumento não pegaria nem o som que funciona"** |
| **controle negativo 3** | não havia | **os outros três controles desligados ou fora da sala, a saída do sistema em mudo, e 10 s de gravação basal antes de qualquer escrita.** É o que a observação não replicada de 16/08 00h10 exige: ela ouviu som de um controle no rádio uma vez, e ninguém sabe de onde veio |
| **quem observa** | webcam por FFT | igual — mas registrando que **não existe instrumento** nesta árvore: nenhum script tem FFT nem webcam hoje. É trabalho novo, e o custo abaixo já o conta |

---

## 7. O que custa dela, e o que custa de máquina

| | dela | de máquina | quando |
|---|---|---|---|
| **E-7** (seção 6) | **4 min** de olho — 7 passos e 2 negativos, com apagar entre eles | **35 min**: o modo de cadeia no `corpo_do_degrau.py`, que já existe | **hoje**, se ela quiser |
| **E-1 refeito**, passo do ruído N=10 com `btmon` | **2 min** de olho | 10 min | junto com o E-7, mesma sessão |
| **E-5**, se o E-7 abrir a porta | **8 min**: 2 de mão (posicionar controle e webcam), 6 de ouvido com os dois timbres, em teste **cego** | **2 h 30**: codificador Opus por `ctypes` (o `opus_encoder_create`/`opus_encode` existem na libopus 1.4 desta máquina, e o módulo já tem o carregador), mais o instrumento de gravação e FFT, que **não existe** | outra sessão |
| **E-5**, se o E-7 fechar a porta | **0 min** | 0 | não roda |

**A conta que importa:** o desenho original pedia **30 minutos de máquina e a
hora de ouvido dela** para um ensaio com cinco premissas não medidas. Este pede
**4 minutos dela** para derrubar a primeira delas. Se a resposta for "não há
cadeia", ela economiza a hora inteira — e essa é a razão de o E-7 existir.

---

## 8. As armadilhas, e onde cada uma morde NESTE desenho

1. **O `os.write` que devolve sucesso sem veredito do firmware.** Morde em todos
   os passos. O instrumento já imprime *"O RETORNO DO os.write NÃO É A MEDIÇÃO"*
   (`corpo_do_degrau.py:261`) e pausa esperando ela dizer o que viu. Mantido.
2. **A falácia do canal que responde.** Morde no passo 2 do E-7: *"a cor acendeu
   depois de um bloco `0x13`"* prova que **o parser andou a cadeia**. Não prova
   que a tag `0x13` significa alto-falante, não prova que o bloco foi consumido
   com sentido, e não prova que 200 bytes de Opus ali dentro fariam som. A
   redação do desfecho já está escrita na seção 6.2 justamente para que ninguém a
   escreva melhor do que ela é.
3. **Controle positivo E negativo em todo ensaio.** O E-7 nasce com dois
   positivos (o passo 1, e o apagar conferido entre passos) e dois negativos (CRC
   errado, `[2]=0x00`). O E-5 ganha um terceiro negativo e um **positivo de
   ouvinte** que ele não tinha.
4. **A proibição de `SET_FEATURE` na família `0xF0`-`0xF7`.** Intacta. Nada aqui
   toca feature report nenhum; o `0x9E` do passo 4 é uma **tag de bloco**, que é
   outro espaço de nomes, e escolhi `0x1E` em vez de qualquer coisa perto de
   `0xF` exatamente para que ninguém leia a linha errado com pressa.
5. **A Steam apaga a lightbar** (nova, 16/08). O instrumento tem de **recusar
   rodar** quando outro processo segura o hidraw, e nomear a Steam. Hoje ele não
   confere isso — é o único acréscimo obrigatório de código antes do E-7.
6. **O sysfs não sabe o que a barra mostra** (nova, 16/08). Nenhum passo deste
   documento lê `multi_intensity` para nada.
7. **Instrumento que lê a ordem de enumeração em vez do aparelho.** O
   `corpo_do_degrau.py` já casa `hidrawN` → `uniq` pelo `uevent` e exige `--alvo`
   com MAC conferido. A mordida continua a mesma: rodar com os nós trocados na
   linha de comando e ver o relatório trocar de endereço junto.

---

## 9. O buraco de registro, e ele precisa ser tapado antes de qualquer célula do mapa se mover

**O resultado do E-1 não está no caderno.** Conferido nesta passagem:

- `docs/data/ensaios.csv` tem **177 ensaios** e **nenhuma linha** do E-1 da
  escada — nem "recheio", nem "excedente", nem `corpo_do_degrau`;
- `docs/data/ensaios-brutos/` não tem bruto nenhum dessa corrida (o
  `2026-08-15-E1-corpo-do-0x32.txt` é de **outro** ensaio, o da mesa 2+2, e
  conclui outra coisa — a colisão de nome "E-1" entre duas sprints vai enganar
  alguém, e provavelmente já enganou);
- o instrumento está **em `git add`, não commitado**.

Esta casa tem um portão feito exatamente contra isso —
`tests/unit/test_o_grau_forte_exige_ensaio_no_caderno.py`, nascido de uma mutação
em 12/08 em que grau forte passou com zero ensaios no CSV. **Enquanto o E-1 viver
só na memória da sessão, nenhuma célula pode dizer "o excedente é ignorado".**

E há uma divergência concreta que só o bruto resolve: **as cores relatadas não
batem com a tabela de passos do instrumento.** O `corpo_do_degrau.py:129-135` diz
passo 2 = **VERDE** e passo 3 = **AZUL**; o relato da madrugada diz **magenta** no
`0xFF` e cita um recheio **`0xF0`** que não está na tabela de passos nenhuma.
O `0xF0` é reconhecível: é o ruído com a semente reiniciada a cada byte, o defeito
que a própria docstring do instrumento registra ter pego na primeira execução de
16/08 (`:172-177`). **Duas passadas do ensaio, uma com o gerador quebrado, e a
memória juntou as duas.** Isso não se resolve lembrando; resolve-se escrevendo o
bruto.

**O que falta, e é barato:** duas linhas em `docs/data/ensaios.csv` (uma por
desfecho), o bruto da corrida em `docs/data/ensaios-brutos/`, e o commit do
instrumento.

---

## 10. O que NÃO está decidido, e é dela

1. **O E-7 roda hoje?** São 4 minutos e ela virou a noite. Se a resposta for
   "amanhã", nada se perde: o modo de cadeia é código, e código roda sem ela.
2. **O E-5 fica na fila mesmo se o E-7 abrir a porta?** São 2 h 30 de máquina e
   8 minutos dela, e há frentes com preço menor por decisão fechada.
3. **A colisão de nome "E-1".** Duas sprints da mesma semana têm um ensaio E-1, e
   eles concluem coisas diferentes sobre o mesmo report. Renomear um dos dois é
   decisão de vocabulário, e vocabulário é dela.

---

## 11. O que este documento NÃO prova, repetido no fim de propósito

- **Não prova que existe cadeia de blocos.** Prova que ninguém aqui jamais
  escreveu uma, e que o E-1 não podia tê-la detectado.
- **Não prova que o E-1 errou.** O E-1 fechou uma posição, com controle positivo
  e negativo, e fechar posição é o trabalho. O que ele não pode sustentar é a
  frase larga *"o excedente é ignorado"* — o que ele mediu foi o `reserved[24]`
  do report, numa cadeia que ele nunca abriu, no degrau em que o payload não
  cabe.
- **Não prova nada sobre áudio.** Nem um byte de áudio de saída foi escrito por
  esta casa, nem hoje nem nunca. **Não existe ponte de áudio de saída por
  rádio**, e este documento não a aproxima — ele só diz onde procurar o chão
  antes de construir.
- **O que continua provado, e é bastante:** o canal existe, transporta 552 bytes
  num pacote, e o firmware executa o `common` de 47 bytes em três degraus
  diferentes.
