# ÍNDICE — a tarde que só virou commit depois de morrer

- **Escrito em:** 15/08/2026, no fim do dia, na branch `restauro/inicio-da-sessao`,
  sobre `f94d416`.
- **Grau:** **REGISTRO DE EXECUÇÃO + índice dos documentos da tarde.** Não é
  plano. A seção 2 é o que **já está commitado**; a seção 3 é o que estava sem
  porta de entrada; a seção 6 aponta para onde mora o que continua aberto.
- **O que ele cobre:** a leva de **15/08 à tarde** — seis frentes em paralelo
  entre 13h30 e 14h50, a queda da sessão, e os **sete commits** que fecharam a
  leva às 16h55.
- **O irmão da manhã:**
  [o índice da madrugada](2026-08-15-INDICE-a-madrugada-que-quase-nao-virou-pagina.md)
  fecha às 02h55 e **não conhece nada da tarde**. Ele continua válido para o que
  registrou.
- **O irmão de hoje:**
  [A QUEDA](../2026-08-15-A-QUEDA-o-que-sobreviveu-e-o-que-falta-materializar.md)
  é o inventário do que **ficou aberto**. Esta página é o oposto: o que
  **fechou**, e onde está.

---

## Por que este documento é novo, e não uma seção no índice da madrugada

A pergunta foi feita, e a resposta é o que a casa já faz. Desde 25/07 há
**dezenove** índices em `docs/process/sprints/`, e todos seguem a mesma forma:
**um por leva**, com a data da leva no nome do arquivo. Nenhum foi jamais
estendido depois de fechado.

Três motivos, e o terceiro é o que decide:

1. **O índice da madrugada declara o próprio escopo na primeira linha** — *"a
   sessão de 14/08 de manhã até 15/08 de madrugada"*, escrito *"sobre `97c2cbf`
   com a árvore suja"*. Uma seção da tarde ali dentro faria o documento mentir
   sobre si mesmo logo no cabeçalho, que é o pedaço que mais gente lê.
2. **As duas levas não têm a mesma natureza.** A da madrugada foi materialização
   de transcrito; a da tarde foi medição no aparelho, com seis frentes em
   territórios exclusivos e uma sessão morta no meio. Misturar as duas obriga
   quem lê a separá-las de cabeça.
3. **O `CLAUDE.md` manda abrir *"o índice de sprints aberto mais recente
   (`*INDICE*`)"*, e a escolha se faz pelo NOME do arquivo.** Este nome foi
   escolhido para ordenar **depois** do da madrugada num `ls`: `a-madrugada`
   antes de `a-tarde`. Uma seção nova deixaria o arquivo mais recente com nome
   de madrugada — e quem entrasse por ele leria o cabeçalho de 02h55 e pararia
   ali.

O que a madrugada ganhou foi **uma linha de encaminhamento** no topo, e a
correção dos dois fatos que ela afirmava e que deixaram de ser verdade (§5).

---

## 1. Como ler

1. **Os sete commits** — se o que você ia fazer está aqui, está feito e
   commitado.
2. **Os cinco documentos que nenhum índice citava** — o defeito que fez esta
   página existir.
3. **O que a tarde mediu**, com os números.
4. **O que continua aberto**, com dono, e onde ele mora.

---

## 2. Os sete commits, e o que cada um fechou

Sete commits em dois minutos (16:55–16:56), **um por frente** — a leva inteira
some **37 arquivos, 6.341 inserções e 182 deleções** desde `1a475d0`, o último
commit de antes da queda.

| commit | frente | o que fechou |
|---|---|---|
| `79d143d` | máscara por jogador | o sabor do vpad deixa de ser decisão da mesa: nasce `registro_de_mascaras`, `mascara_efetiva` e `vpad_ficou_para_tras`, com o `ExternalMaskRegistry` (de 07/08) **finalmente ligado ao caminho de produção**. 351 linhas de teste |
| `fd4ed6b` | grab dobrado (D-29) | `reconciliar_grab_do_primario` a cada 2,0 s no laço do `lifecycle` — o irmão que faltava do retry que o co-op tem desde julho. 305 linhas de teste |
| `86563c2` | ordem do jogador (D-30 b) | o número passa a sair da **ordem de chegada daquele momento**, com onda de 0,5 s e congelamento após 4,0 s de mesa parada; o `rank` gravado sobra como desempate. 644 linhas de teste |
| `ece9083` | cor do plástico (D-15) | o instrumento `cor_do_plastico.py` (1.101 linhas) lê a cor no firmware pela feature `0x20`. Dois lidos no cabo; no rádio, **exercido e recusado** |
| `adeb015` | lightbar travada | o instrumento `byte_no_fio.py` (713 linhas), o par doente-contra-são no mesmo rádio, e a arqueologia de tudo o que já caiu nesta frente |
| `fe6f74c` | colunas do mapa (D-13/D-14) | `confianca` e `grau` viram **`de_onde_sei`** e **`ate_onde_foi`**, nos dois transportes, sem alias, em dez arquivos; dez linhas rebaixadas com nota datada |
| `f94d416` | privacidade | dois dos quatro DualSense **não estavam no portão de anonimato**, e a docstring que ensina a mascarar usava o endereço e o serial reais dela como exemplo |

**A frente que fechou sozinha** foi a do grab: causa achada, cura ligada, nove
mordidas arrancadas e devolvidas, sprint escrita. As outras cinco foram cortadas
no meio pela queda da sessão e só fecharam depois — é isso que o nome desta
página conta.

---

## 3. Os cinco documentos que nenhum índice citava

Este é o defeito que a página conserta. O censo, feito com `grep -rl` antes de
escrever uma linha:

| documento | linhas | quem o citava antes desta página |
|---|---|---|
| [A QUEDA — o que sobreviveu, e o que falta materializar](../2026-08-15-A-QUEDA-o-que-sobreviveu-e-o-que-falta-materializar.md) | 412 | **ninguém** |
| [A lightbar travada — o que já caiu, e o que nunca foi tentado](../estudos/2026-08-15-A-LIGHTBAR-TRAVADA-o-que-ja-caiu-e-o-que-nunca-foi-tentado.md) | 565 | **ninguém** |
| [O par que faltava — o doente e o são no mesmo rádio](../estudos/2026-08-15-O-PAR-QUE-FALTAVA-o-doente-e-o-sao-no-mesmo-radio.md) | 181 | **ninguém** |
| [GRAB-DOBRADO-01 — o P1 perdia o grab e ninguém tentava de novo](2026-08-15-GRAB-DOBRADO-01-o-P1-perdia-o-grab-e-ninguem-tentava-de-novo.md) | 196 | só ela mesma |
| [`docs/data/ensaios-brutos/2026-08-15-144356-byte-no-fio.txt`](../../data/ensaios-brutos/2026-08-15-144356-byte-no-fio.txt) | 53 | **ninguém** |

E dois instrumentos novos que nenhum documento nomeava: `byte_no_fio.py` (713
linhas) e — fora da lista acima porque a sprint da cor já o cita —
`cor_do_plastico.py` (1.101 linhas), o **único** de `scripts/ensaios/` que
escreve no aparelho.

**Por que isto é defeito, e não arrumação:** o `CLAUDE.md` manda a próxima
sessão começar pelo índice de sprints mais recente. Documento que índice nenhum
cita não é lido — foi exatamente assim que o achado da cor ficou **cinco dias**
enterrado num transcrito, e está registrado na §4.11 do índice da madrugada.

---

## 4. O que a tarde mediu, com os números

### 4.1. O par que faltava — 306 atributos, duas diferenças reais

Pela primeira vez esta frente teve **doente e são no mesmo transporte, no mesmo
host, na mesma sessão do daemon, no mesmo instante**: um DualSense branco com a
barra apagada e um vermelho são, os dois no rádio. Lidos **306 atributos de
sysfs em cada um** e comparados com `diff`: **três** diferenças, e uma delas é a
numeração do co-op. Sobram **duas** — o estado de energia (`Full` contra
`Discharging`) e a revisão de placa.

O que é **idêntico** vale tanto quanto: descritor HID byte a byte, versão de
firmware, capacidades de evdev, o `info` do BlueZ campo a campo, o papel e a
política de enlace, quem tem o nó aberto — e **os nós de LED**, com
`brightness=255` e `multi_intensity` verde nos dois. *O kernel acha que a barra
do travado está acesa e verde.*

O candidato que subiu ao primeiro lugar é o **estado de energia**, e ele subiu
por explicar o que já se sabia: *"por cabo sempre funciona"* (por cabo há VBUS),
e *"reconectar cura"* ter caído quatro vezes desde 17/07 (reconectar não muda
VBUS). O ensaio que o separa da revisão de placa custa **tirar a alimentação do
vermelho** — não desliga controle, não reconecta, não reinicia nada, e é
reversível.

### 4.2. O byte no fio — o host está inocentado

`btmon` passivo com `kprobe` armado em `dualsense_send_output_report`. Na captura
inteira: **2.729** quadros ACL com payload L2CAP, **120** reports de saída
`0x31` do host para os aparelhos, **60 por handle**, e a cor mágica que o
instrumento escreveu aparece em **30 de 30** quadros esperados nos dois lados.

O diff byte a byte dos dois `0x31` de 78 bytes tem **cinco** posições
diferentes: o `seq_tag` (contador rotativo do driver) e os quatro bytes de CRC-32
que são consequência dele. **Tudo o mais é igual, e o doente ACK-a a entrega no
enlace.** O que ignora a cor está dentro do firmware.

### 4.3. A cor do plástico — lida no cabo, recusada no rádio

Feature `0x20`, os caracteres 5 e 6 do serial de fábrica: `hidraw4`
(`hardware_version 0x00001111`) devolveu **05 = Starlight Blue**; `hidraw5`
(`0x00000710`) devolveu **04 = Galactic Purple**. Com **âncora independente**: a
sprint UNIDADE-COR-01 já registrava, *sem saber a cor*, que `0x1111` era o azul
e `0x0710` era o roxo.

No rádio o ensaio foi **exercido e recusado**, com a autorização dela: duas
tentativas, uma com CRC-32 e outra sem, as duas com **`EIO` (errno 5)
imediato** — execução inteira em **0,249 s**, longe dos ~3 s do
`REPORT_REQ_TIMEOUT` do BlueZ. Isso descarta o timeout e descarta *"o report não
existe neste transporte"* (que daria `EPIPE`), e deixa de pé a hipótese não
medida: recusa na camada HIDP/L2CAP.

**Nenhum controle se alterou:** o `0x20` saiu idêntico byte a byte antes e depois
de cada escrita, o `hardware_version` não mudou, e 3 de 3 reports de entrada
continuaram chegando.

### 4.4. O grab do primário — o estado absorvente

Quatro ocorrências de `evdev_grab_failed` em três dias, **todas** vindas do
`(re)open` de um nó e **nenhuma** seguida de recuperação. A pergunta certa não
era *"por que falha"* — qualquer um falha num instante de re-enumeração — e sim
**"por que fica falhado"**: o secundário tinha retry desde julho e o primário
não tinha nenhum. *A casa sabia e o produto não fazia.*

### 4.5. As colunas do mapa — o que o censo diz hoje

Medido agora, com `csv.DictReader` no cabeçalho real e com o portão:

| o que | quanto |
|---|---|
| colunas do CSV | 45, com `cabo_de_onde_sei`, `radio_de_onde_sei`, `cabo_ate_onde_foi`, `radio_ate_onde_foi` nas posições exatas das quatro que substituíram |
| células com `de_onde_sei` = `medido` | **98** |
| afirmações fortes (`sim` + `medido`) | **46** — nenhuma sem teste que morda |
| graus fortes (`SAIU NO FIO` ou `O APARELHO OBEDECEU`) | **25** — nenhum sem ensaio no caderno |
| rebaixadas pela D-14 | **dez linhas**, **catorze células**, cada uma com nota datada |

Nenhum `ate_onde_foi` foi mexido pelo rebaixamento: o que caiu foi **de onde se
sabe**, não **até onde a prova chegou** — que é exatamente a distinção que a
renomeação existe para tornar impossível de confundir.

### 4.6. A privacidade — a régua aplicada numa forma só, pela terceira vez

`_OUIS_REAIS_OCTETOS` não listava dois dos quatro DualSense da mesa, e **17 e 18
documentos versionados** já citavam cada um deles — mascarados **à mão**. E a
docstring da função que mascara usava o endereço real como exemplo do "antes";
o mesmo com o serial, que passou verde no `check_anonymity.sh` porque a régua
varre a forma de um MAC, não a de um serial.

---

## 5. Os dois fatos que o índice da madrugada afirmava e que deixaram de ser verdade

Corrigidos **na fonte**, não aqui, e registrados aqui para quem lembrar de ter
lido o contrário:

| o que a página dizia | o que o `git` diz |
|---|---|
| *"as curas de Bluetooth — na máquina dela, **NÃO commitadas**"* | commitadas em **`7c3a0c7`**, 15/08 às 02:12:19 |
| *"a MESA-CHEIA-12 — na árvore, **NÃO commitada**"* | commitada em **`9441678`**, 15/08 às 02:12:38 |

As duas afirmações eram verdadeiras quando foram escritas — o documento saiu
entre 01h e 02h, e os commits vieram **dez minutos depois**. Pela regra da casa
isto não é decisão medida que ganha nota datada: é fato que a medição derrubou,
e sai por substituição. Quem lesse hoje iria procurar trabalho solto que não
existe.

---

## 6. O que continua aberto — e onde ele mora

Esta página **não duplica** a fila. Ela aponta:

- **O que exige a palavra dela:** as sete escolhas de produto da
  [§5 de A QUEDA](../2026-08-15-A-QUEDA-o-que-sobreviveu-e-o-que-falta-materializar.md) —
  entre elas o `EIO` do rádio fechar ou não a D-15, a supressão incondicional de
  hidraw por Bluetooth (o caminho que **comprovadamente funciona** é o que o
  produto se proíbe de usar), e as duas ondas perecíveis que precisam da mesa de
  pé **e dela presente**.
- **A ordem de execução da próxima leva:** a
  [§6 de A QUEDA](../2026-08-15-A-QUEDA-o-que-sobreviveu-e-o-que-falta-materializar.md),
  em quatro faixas por dependência e risco.
- **As vinte e seis respostas dela**, que são a fonte de verdade onde qualquer
  sprint discordar:
  [AS DECISÕES — RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md).
- **O histórico completo da frente da lightbar**, para não se propor pela quinta
  vez uma hipótese já refutada:
  [A LIGHTBAR TRAVADA](../estudos/2026-08-15-A-LIGHTBAR-TRAVADA-o-que-ja-caiu-e-o-que-nunca-foi-tentado.md).
  Dos **quinze** suspeitos de rádio do caderno, **zero** estão inocentados — a
  poda nunca aconteceu nesta linha.

**O risco que nenhuma página fecha:** a pasta de recuperação
`_recuperacao-2026-08-15/`, com os dez relatórios extraídos das sessões mortas,
**não é repositório git** e existe em cópia única. Está na §3 de A QUEDA, e
continua valendo.

---

## 7. A conferência — como cada afirmação desta página foi checada

| afirmação | como foi conferida |
|---|---|
| os sete commits e os números de cada um | `git log --format='%h %ad %s'` e `git show --stat` nos sete |
| o total de 37 arquivos e 6.341 inserções | `git diff --shortstat 1a475d0 f94d416` |
| `7c3a0c7` e `9441678` estão na história | `git merge-base --is-ancestor <sha> HEAD` nos dois, e `git show` para a hora |
| os cinco documentos sem citação | `grep -rl` por cada nome em `docs/`, antes de escrever esta página |
| as contagens do mapa | `csv.DictReader` no cabeçalho real e `scripts/check_paridade_transporte.py` (`rc=0`) |
| as dez linhas e catorze células da D-14 | varredura das 300 linhas do CSV procurando a nota `D-14` |
| os números do par doente-são e do byte no fio | os dois brutos versionados em `docs/data/ensaios-brutos/` |

**O que esta página NÃO conferiu:** não rodei a suíte inteira (o retrato de
9.692 verdes é de A QUEDA, escrito às 16:32, e a árvore mudou desde então), não
abri janela nenhuma, não toquei em aparelho e não reiniciei serviço nenhum.
