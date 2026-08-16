# ÍNDICE — a tarde que só virou commit depois de morrer

- **Escrito em:** 15/08/2026 às 17:39, na branch `restauro/inicio-da-sessao`,
  sobre `f94d416`. **Estendido às 19h**, sobre `f4de49c` — as seções 2.1 e 3.1
  são desta segunda passada, e estão marcadas.
- **Grau:** **REGISTRO DE EXECUÇÃO + índice dos documentos da tarde.** Não é
  plano. A seção 2 é o que **já está commitado**; a seção 3 é o que estava sem
  porta de entrada; a seção 6 aponta para onde mora o que continua aberto.
- **O que ele cobre:** a leva de **15/08 à tarde e à noite** — seis frentes em
  paralelo entre 13h30 e 14h50, a queda da sessão, os **sete commits** que
  fecharam a leva às 16h55, e os **cinco commits das 18h40** que vieram depois,
  entre eles as **três propostas de interface** (§3.1) que são o produto
  principal da noite.
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

1. **Os sete commits** (§2) e os **cinco que vieram depois** (§2.1) — se o que
   você ia fazer está aqui, está feito e commitado.
2. **Os cinco documentos que nenhum índice citava** (§3) — o defeito que fez esta
   página existir — e a **recaída** (§3.1), que é onde moram as **três propostas
   de interface**. Se você só tem tempo para uma seção, é a 3.1: é o que espera
   o olho dela.
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

### 2.1 Os cinco commits das 18h40 — que esta página não conhecia

*(Acrescentado às 19h. A tabela acima fecha em `f94d416`, que era o `HEAD`
quando o texto foi escrito às 17:39. Estes cinco entraram depois, e sem esta
seção o índice mais recente da casa terminaria uma hora antes do dia.)*

De `f94d416` a `f4de49c`: **33 arquivos, 19.505 inserções e 137 deleções**
(`git diff --shortstat`).

| commit | hora | o que fechou |
|---|---|---|
| `f33b318` | 18:40:13 | **anonimato**: o MAC dela **em binário** dentro de um `btsnoop` passava pela régua, que só varria texto. Nasce `scripts/mascarar_btsnoop.py` (340 linhas) e o `\b` que deixava passar o uevent inteiro é corrigido. Entram os brutos do par doente-são (HCI decodificado, 343 atributos de sysfs de cada um) |
| `0a40845` | 18:40:43 | **sete afirmações que a medição já tinha derrubado** e ninguém apagou, em dez arquivos — entre elas o Status de MÁSCARA-POR-JOGADOR-01 e a E2 de ORDEM-DE-CHEGADA-01, que diziam esperar por ela depois de ela já ter respondido |
| `f091253` | 18:40:44 | **esta página**, mais o CHANGELOG e o `CONTRIBUTING` |
| `1ae9ee0` | 18:40:44 | **a mordida que faltava** no `cor_do_plastico.py`: o único instrumento de `scripts/ensaios/` que **escreve** no aparelho não tinha teste. 586 linhas, e elas cobrem a recusa do alvo errado |
| `f4de49c` | 18:40:44 | **as três propostas de interface** (1.367 linhas de documento e quatro maquetes PNG) — a onda D-16 a D-22, que estava parada por falta de desenho. É o assunto da §3.1 |

**O que muda para quem lê:** a leva da tarde não terminou nos sete commits das
16h55. Ela terminou às 18h40, e o que saiu por último **não é código** — são
três desenhos esperando o olho dela.

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

### 3.1 A recaída, no MESMO dia — e é aqui que estão as três propostas de interface

*(Acrescentado às 19h.)* A lista acima foi feita às 17:39. **Entre 18h08 e
18h27 nasceram três documentos novos**, e nenhum índice os citava — o mesmo
defeito, uma hora depois de a página que o conserta ter sido escrita. Censo
refeito com `grep -rl` em `docs/` e no `README.md`, contando **quem cita cada
nome sem ser ele mesmo**:

| documento | linhas | quem o citava antes desta seção |
|---|---|---|
| [ONDE A COR MORA-01](2026-08-15-ONDE-A-COR-MORA-01-a-borda-diz-quem-e-e-o-anel-diz-o-que-esta-escolhido.md) | 393 | **ninguém** |
| [NAVEGA-PELO-CONTROLE-01](2026-08-15-NAVEGA-PELO-CONTROLE-01-quem-tem-o-foco-decide-o-que-o-R1-faz.md) | 564 | **ninguém** |
| [NAVEGAR ESTA JANELA-01](2026-08-15-NAVEGAR-ESTA-JANELA-01-a-decisao-ja-esta-tomada-e-o-dado-ja-esta-no-fio.md) | 410 | **só a página irmã** (NAVEGA-PELO-CONTROLE-01) — nenhum índice |
| [MÁSCARA-POR-JOGADOR-01](2026-08-15-MASCARA-POR-JOGADOR-01-a-decisao-de-14-08-esbarra-na-de-10-08.md) | 474 | três páginas de `docs/process/`, e **índice nenhum** |
| [ORDEM-DE-CHEGADA-01](2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md) | 269 | seis páginas, entre elas o índice da madrugada — **mas nenhum índice sabia da E2 entregue** |

E as **quatro maquetes** que nasceram com elas, em
`docs/process/estudos/assets/2026-08-15-onde-a-cor-mora/`: a fita de hoje contra
a proposta, o gesto que troca as cores de lugar, o caso que colide roxo com
roxo, e quem vence no alto contraste. São renderizações offscreen com o
`theme.css` de verdade — **não são fotos do produto**, porque o produto ainda
não faz isto.

#### As três propostas de interface — o que cada uma DECIDE ou PROPÕE

> **Leia isto antes de abrir qualquer uma das três:** nenhuma é entrega. As três
> declaram, no próprio cabeçalho, que estão sob a
> [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
> — *interface só fecha com o olho dela*. **Zero linhas de `src/` foram tocadas
> pelas três.** Quem pegar uma delas como se fosse plano aprovado vai executar
> desenho que ela ainda não viu.

| proposta | o que ela PROPÕE, em uma linha | o que ela DEIXA para ela |
|---|---|---|
| **ONDE A COR MORA-01** (18:27) | executa as **D-16/D-17/D-18**: cada chip do cabeçalho ganha **contorno fechado na cor do plástico daquele controle** (identidade) e o selecionado ganha um **anel roxo por dentro** (escolha); os botões `1 2 3 4` passam a mostrar **a mesa inteira em quatro cores**, e clicar num número **desliza as cores de lugar**. Custo estimado: ~120 linhas em `status_actions.py`, ~30 no `theme.css`, ~40 no `controller_card.py` | **três perguntas**: (1) o produto pode mandar sozinho o comando da **família de fábrica** a cada chegada no cabo, sem ninguém olhando? (2) o que a tela faz com o controle **no rádio**, que fica sem cor — hoje metade da mesa dela? (3) **quem escolhe o RGB** de cada nome de cor, já que o aparelho entrega `05` e a tabela entrega *Starlight Blue*, e ninguém entrega um tom |
| **NAVEGAR ESTA JANELA-01** (18:08) | executa a **D-19**: a aba Navegação passa a ter **duas seções empilhadas** — *"Comandar o PC"* (as duas colunas de hoje, intactas) e *"Navegar esta janela"* (os 487 px que sobram). Mede que **o dado já está no fio** (`inputs.buttons` por controle, 141-250 Hz) e nomeia o **bloqueio real**: o tique de 10 Hz **só existe na aba Status**, e navegar exige o feed em toda aba | **duas perguntas**: (1) os quatro navegam juntos — então a tela mostra **um dono ou quatro**? (recomenda quatro marcas, uma por controle, na cor de cada um, por coerência com a D-17/D-18) (2) dois apertam no mesmo tique para lados opostos: **qual ganha**? |
| **NAVEGA-PELO-CONTROLE-01** (18:13) | executa as **D-20/D-21/D-22** dentro da seção que a irmã cria: a **máquina de estados inteira** — cinco estados, seis verbos, duas bordas — com o R1/L1 em carrossel na tira de abas. O achado que muda a arquitetura: se quem detecta a borda do botão for a **GUI**, o **primeiro X de cada novo dono vaza para o jogo**; a detecção tem de morar no daemon, que mascara no mesmo tique | **uma pergunta**: o dono perde os quatro botões da frente — **perde também L1, R1 e D-pad**? O conjunto que navega ficou maior que o conjunto que a D-22 mandou roubar, e isso é consequência aritmética de duas respostas dela juntas |

**As duas irmãs se completam e não se contradizem** — a NAVEGA-PELO-CONTROLE-01
diz isso no próprio texto, e diz também que descobriu a existência da outra
**rodando o portão de referências, com a página já escrita**. Há **uma
divergência de rota** entre elas, nomeada na §8.1 da NAVEGA-PELO-CONTROLE-01
(liberar o tique do `state_full` contra abrir um tique próprio e leve), e ela
**não é decisão dela**: é escolha de quem executar.

**A ordem que o censo impõe** (§9 da NAVEGAR ESTA JANELA-01, conferido no código
às 18h00): **as sete decisões D-16 a D-22 estão respondidas e nenhuma tem
código**. A D-19 vem primeiro, porque D-20, D-21 e D-22 são o **conteúdo** da
seção que ela abre; o trio D-16/17/18 anda em paralelo, porque depende da cor e
não da navegação.

#### As duas que mudaram de estado e nenhum índice acompanhou

| sprint | o que o índice tinha de saber |
|---|---|
| **MÁSCARA-POR-JOGADOR-01** | deixou de estar *"parada, esperando ELA"*: ela respondeu **por jogador**, a frase de 10/08 passou a valer só para o `mode`, e o código está commitado em `79d143d` — o `ExternalMaskRegistry`, escrito em 07/08 e nunca ligado, **finalmente tem chamador**. Falta o **último degrau, que é a identidade** (§7.2 da sprint): as duas fábricas de vpad já sabem perguntar *"de quem é este gamepad?"* e ninguém responde. Até lá o produto se comporta **exatamente como antes**, de propósito |
| **ORDEM-DE-CHEGADA-01** | a **E2 está ENTREGUE** em `86563c2` (a D-30: ordem do momento, congelada quando a mesa estabiliza, o gravado vira desempate). O índice da madrugada ainda a lista como pendente inteira; **a E3 é o que continua aberto** |

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

> **A correção na fonte só entrou às 19h, e isto fica escrito.** Quando esta
> seção foi redigida, às 17:39, ela afirmava *"corrigidos na fonte"* e o índice
> da madrugada **continuava com os dois títulos antigos** — a correção tinha
> sido planejada e não aplicada. Foi aplicada na passada das 19h: os títulos das
> §1.c e §1.d de lá agora trazem o `sha` e a hora, a tabela de conferência de lá
> foi refeita, e o topo daquela página ganhou o encaminhamento para cá.
> **Por que isto importa:** quem entra pelo índice da madrugada — que é o
> caminho natural, por ser o mais antigo dos dois — lia a afirmação falsa e
> **nunca chegava a esta tabela**. Uma correção que mora só na página que ninguém
> abriu primeiro não é correção.

---

## 6. O que continua aberto — e onde ele mora

Esta página **não duplica** a fila. Ela aponta:

- **O que exige o OLHO dela** *(acrescentado às 19h)*: as **três propostas de
  interface** da §3.1 e as **seis perguntas** que elas deixaram — três em ONDE A
  COR MORA-01, duas em NAVEGAR ESTA JANELA-01, uma em NAVEGA-PELO-CONTROLE-01.
  Nenhuma das sete decisões D-16 a D-22 tem código; o que trava não é decisão, é
  a PROVA-DE-TELA-01.
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
| **(19h)** os cinco commits das 18h40 e o que cada um fechou | `git log --oneline -14` e `git show --stat` nos cinco |
| **(19h)** os 33 arquivos e 19.505 inserções da §2.1 | `git diff --shortstat f94d416 f4de49c` |
| **(19h)** as cinco sprints sem citação da §3.1 | `grep -rl` por cada nome em `docs/` e no `README.md`, descontando o próprio arquivo — antes de escrever a seção |
| **(19h)** as linhas de cada uma das cinco | `wc -l` nos cinco arquivos |
| **(19h)** o que cada proposta decide, propõe e deixa para ela | as três abertas e lidas: cabeçalho, seção de desenho, seção de custo e seção de perguntas de cada uma |
| **(19h)** que as três não tocaram `src/` | `git show --stat f4de49c` — quatro PNG, três `.md` e um teste; nenhum arquivo de `src/` |
| **(19h)** as quatro maquetes existem no disco | `ls docs/process/estudos/assets/2026-08-15-onde-a-cor-mora/` |

**O que esta página NÃO conferiu:** não rodei a suíte inteira (o retrato de
9.692 verdes é de A QUEDA, escrito às 16:32, e a árvore mudou desde então), não
abri janela nenhuma, não toquei em aparelho e não reiniciei serviço nenhum.
