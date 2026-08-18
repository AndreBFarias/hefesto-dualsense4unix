# UNIDADE-COR-01 — o controle sabe de que cor ele é

- **Escrito em:** 15/08/2026, sobre `c8065d8`
- **Grau:** **MEDIDO** no que descarta; **MEDIDO NO CABO** no que propõe
  (15/08/2026, dois controles — ver §1); **MEDIDO E RECUSADO NO RÁDIO**
  (15/08/2026, duas tentativas, `EIO` nas duas — ver §4).
- **Citada desde:** 10/08/2026, em três documentos, e nunca escrita até agora —
  o que é, ele mesmo, o defeito que esta sprint documenta.

## A dívida que esta sprint paga primeiro

O nome `UNIDADE-COR-01` aparece em três índices desta casa como se a sprint
existisse. Não existia. O portão `test_nome_citado_como_sprint_existe` reprovou em
15/08, e é assim que se descobre uma promessa que ninguém cumpriu.

A pesquisa que a sustenta foi feita em **10/08/2026** e ficou enterrada no
transcrito de um subagente (`agent-aa104bfbf8d406205.jsonl`, sessão `aad330bc`).
Cinco dias depois, em 15/08, um agente a redescobriu do zero. É o mesmo padrão do
`BLOCO_SPEAKER` ([O-ALTO-FALANTE-POR-RADIO-01](2026-08-15-O-ALTO-FALANTE-POR-RADIO-01-a-casa-ja-tinha-o-mapa.md)):
**a casa mede e não registra, e depois paga de novo.**

## O que ela quer

Que a guia de cada controle e o seletor de jogador apareçam **na cor física do
controle** — o vermelho dela com borda vermelha, o azul com azul. Nas palavras
dela, em 14/08: *"cada controle com a guia na cor física dele e mostrando a
escolha do user"*. E ela lembrava que *"tínhamos mapeado isso no passado, cada
controle tem o firmware com a cor do plástico dele"*.

Ela estava certa.

## 1. O campo existe, e o endereço é exato

O serial de fábrica de 17 caracteres carrega a cor nos **caracteres 5 e 6**:

```
SET_FEATURE 0x80, payload [0x01, 0x13]      (base=1, num=19)
GET_FEATURE 0x81 -> 64 bytes
    buf[1]=1, buf[2]=19, buf[3]=2   (senão é erro)
    buf[4..20] = 17 chars ASCII = o serial impresso na traseira
cor = serial[4:6]
```

| código | cor | | código | cor |
|---|---|---|---|---|
| `00` | White | | `06` | Grey Camouflage |
| `01` | Midnight Black | | `07` | Volcanic Red |
| `02` | Cosmic Red | | `08` | Sterling Silver |
| `03` | Nova Pink | | `09` | Cobalt Blue |
| `04` | Galactic Purple | | `10`–`12` | Chroma Teal/Indigo/Pearl |
| `05` | Starlight Blue | | `30` | 30th Anniversary |

`Z1`…`ZB` são edições especiais.

**Fontes, três independentes e concordantes:** `dualshock-tools.github.io`
(`js/controllers/ds5-controller.js:196-226` e `:404-414`), com o mantenedor
confirmando na issue #210; `nsfm/dualsense-ts`; `TechAntohere/Senshi`.

**Grau: MEDIDO NO CABO, em 15/08/2026, depois da D-15.** Ela autorizou a
escrita, e os dois controles que estavam no cabo responderam:

| nó | `hardware_version` | código | cor lida do firmware |
|---|---|---|---|
| `hidraw4` | `0x00001111` | `05` | **Starlight Blue** |
| `hidraw5` | `0x00000710` | `04` | **Galactic Purple** |

Instrumento: `scripts/ensaios/cor_do_plastico.py`. Saída bruta:
[`docs/data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.txt`](../../data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.txt).

**A âncora bateu, e é isto que dá confiança à leitura.** A tabela da §3 desta
mesma página registrava — sem saber a cor — que `0x00001111` era o controle
*azul* e `0x00000710` o *roxo*. O serial, lido do firmware sem consultar aquela
tabela, respondeu Starlight Blue e Galactic Purple. Duas confirmações
independentes de que o campo é a cor do plástico, e não um número de lote.

**Os dois controles continuaram sãos**: feature `0x20` idêntico byte a byte
antes e depois, `hardware_version` idêntico, e reports de entrada continuando a
sair. O comando foi enviado duas vezes a cada um, e as quatro provas fecharam.

**No rádio, MEDIDO E RECUSADO.** Ela autorizou a estreia do envelope de feature
por Bluetooth, com o risco na mesa. O alvo foi o **vermelho** (`hidraw8`,
`hardware_version 0x00000811`), escolhido por ser o são, e identificado pelo
`HID_UNIQ` — não pela cor do LED — com a trava `--exigir-mac`, que foi testada
contra o MAC errado e recusou. Duas tentativas, **`EIO` (errno 5) nas duas**, e
a cor não saiu. O controle não se alterou. O que a recusa permite concluir — e
o que ela ainda **não** responde — está na §4.

No outro de rádio (`hidraw9`, o branco de lightbar travada) **nada foi
escrito**: as duas execuções nele foram secas, porque outra frente mede aquele
defeito ao vivo.

## 2. O que foi DESCARTADO, e com o quê

Medido em 15/08 nos quatro controles dela, todos por Bluetooth:

| candidato | veredito | como se descartou |
|---|---|---|
| `HID_ID` / PID | idêntico (`054C:0CE6`) | `uevent` dos quatro |
| `modalias`, `country`, `report_descriptor` | idênticos | sysfs |
| BlueZ `info` | **byte a byte idêntico** | `/var/lib/bluetooth/*/*/info` |
| `iSerialNumber` USB | **não é o serial do produto** — é o MAC em 12 hex | SDL `SDL_hidapi_ps5.c:391-403` |
| feature `0x08` (48 B) | todo zero, idêntico | `HIDIOCGFEATURE` ×4 |
| feature `0x09` | MAC + `08 25 00` + MAC do host; constante | idem |
| feature `0x05` | calibração IMU, per-unidade | idem |
| feature `0x0b` | MAC + lista de pareamento | idem |
| `0x80`–`0x83`, `0xF0`–`0xF7` | idênticos **sem comando prévio** | idem |
| `0x20` bytes 32-43 (`device_info[12]`) | difere por unidade, **ninguém decifrou** | `printf` comentado no `dualsensectl` desde 2023 |
| `0x22` offset 45-51 | ASCII numa série, binário noutra — layout muda por série | idem |
| part number `CFI-ZCT1W` | não existe em report nenhum | — |
| prefixo de MAC | fornecedor de rádio/lote | nenhuma fonte liga à cor |

**Isto é resultado negativo útil e por isso está aqui:** quem tentar de novo não
precisa refazer nenhuma dessas doze verificações.

## 3. O que dá de graça HOJE, e o que ele NÃO é

O `hid_playstation` publica `hardware_version` em
`/sys/class/hidraw/hidrawN/device/hardware_version` — **sem root, sem ioctl, sem
disputa com o daemon**. Medido nos quatro controles dela: **os quatro diferem**.

| controle | `hardware_version` | placa |
|---|---|---|
| branco | `0x00000711` | BDM-050 |
| vermelho | `0x00000811` | BDM-050 |
| roxo | `0x00000710` | BDM-050 |
| azul | `0x00001111` | BDM-060M |

**Mas NÃO é a cor.** O byte `(hw>>16)&0xFF` — *Variation* na struct da comunidade
— é `0x00` nos quatro. O que varia é *Generation*, a revisão de placa. Hoje separa
os quatro **por acaso de lote**; dois controles da mesma cor comprados juntos
teriam o mesmo valor.

Serve como **âncora de sanidade**, nunca como fonte de cor.

## 4. O preço, e é por isso que a decisão é dela

Ler o serial exige **uma escrita**: `SET_FEATURE 0x80`.

**`0x80` é a família de comandos de fábrica.** `[1,1]` **reseta o controle**;
`[3,2,…]` destrava a NVS; `[12,1,…]` **grava calibração de stick na memória
não-volátil**. O nosso `[1,19]` é leitura pura — mas um byte errado no payload
escreve onde não devia.

E a leitura **só está provada por cabo** — inclusive por nós, em 15/08/2026, com
os dois da §1. O `dualshock-tools` recusa Bluetooth de saída. Por rádio o canal
existe **no descritor** (`0x80`/`0x81` estão lá, nestes controles) — e em
15/08/2026 ele **foi exercido, e recusou**. A medição está logo abaixo.

Por Bluetooth há ainda o CRC-32 semente `0xA3` nos quatro últimos bytes, que esta
casa já sabe calcular (`core/ds_output_report.py`, `bt_crc32` com
`BT_FEATURE_CRC_SEED`).

**O envelope de rádio, montado, conferido e ENVIADO** (`cor_do_plastico.py
--radio-a-serio`, 15/08 — não foi rodada seca: este buffer foi ao `ioctl`):

```
80 01 13 00 ... 00 93 0d 46 73
                   ^^^^^^^^^^^ CRC-32, semente 0xA3, little-endian
```

O `seq` e o tag `0x10` do envelope de OUTPUT (report `0x31`) **não entram
aqui**: aqueles são do canal de interrupção, e o feature report sai pelo canal
de CONTROLE, com o id no byte 0 e mais nada de cabeçalho. Confundir os dois
envelopes é o defeito que a BTREPORT-02 fechou.

### O rádio, medido em 15/08/2026: `EIO` nas duas tentativas

**A dúvida honesta que sobrava** — se o firmware **exige** o CRC num
`SET_REPORT` de feature ou se apenas o **emite** nas respostas — **foi
respondida, e a resposta é que o CRC não é o discriminante.** As duas
tentativas no `hidraw8` falharam **identicamente, no mesmo ponto**:

| # | envelope | resposta do `ioctl` |
|---|---|---|
| 1 | `80 01 13 00 … 00 93 0d 46 73` — CRC-32, semente `0xA3`, **a mesma** de `core/ds_output_report.py::BT_FEATURE_CRC_SEED` | `EIO` (errno 5), imediato |
| 2 | `80 01 13 00 … 00 00 00 00 00` — `--sem-crc` | `EIO` (errno 5), imediato |

A recusa acontece **antes de o CRC importar**.

**O controle não se alterou**, e a prova está nos transcritos 3 e 4: feature
`0x20` idêntico byte a byte antes e depois de cada escrita, `hardware_version`
idêntico, 3 de 3 reports de entrada continuando a chegar, e a lightbar intacta
(`brightness=255`, `multi_intensity=[0 255 0]`, antes e depois das duas). Na
mesma janela, **o cabo obedeceu**: `hidraw4` devolveu `05` e `hidraw5` devolveu
`04`. Quem recusa é o canal, não o comando.

**As quatro assinaturas de falha, e qual delas veio:**

| assinatura | o que significaria | veio? |
|---|---|---|
| `EPIPE` na hora | *"não tenho esse report neste transporte"* — o stall que esta casa já mediu no cabo | **não** |
| ~3 s e timeout | `REPORT_REQ_TIMEOUT` do BlueZ: o rádio se perdendo | **não** |
| eco errado no `0x81` | o firmware respondendo outra coisa | **não** — não houve resposta a ecoar |
| **`EIO` (errno 5) imediato** | o `ioctl` volta na hora com erro de E/S | **sim, nas duas** |

**O que este negativo permite concluir** — e é isto que dá valor à página:

- **não é `EPIPE`**, logo **o report EXISTE neste transporte**: não é o caso de
  o descritor prometer um canal que o rádio não tem;
- **não é o timeout de ~3 s do BlueZ**, logo **não é o canal de controle se
  esgotando** nem o rádio se perdendo — a execução inteira levou **0,25 s**;
- **sobra uma hipótese, e ela é HIPÓTESE, não medição:** o `SET_REPORT` de
  feature é recusado na camada **HIDP/L2CAP** — pelo firmware ou pelo BlueZ —
  independentemente do conteúdo. Separar *quem* recusou exige instrumentar o
  canal de controle, e isso é uma **terceira** tentativa, que não foi feita: o
  orçamento eram duas escritas, e ele acabou.

Medição bruta:
[`2026-08-15-E7-cor-do-plastico.txt`](../../data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.txt),
seção *"O RÁDIO: EXERCIDO, E RECUSADO"* e transcritos 3 e 4; linhas de resultado
no
[`.csv` irmão](../../data/ensaios-brutos/2026-08-15-E7-cor-do-plastico.csv).

## 5. Os três caminhos, com o preço de cada um

| | o quê | custo | risco |
|---|---|---|---|
| **(a)** | ela escolhe a cor de cada controle na interface, uma vez, salvo por MAC | um gesto por controle, uma vez | **zero** |
| **(b)** | ler o serial **por cabo**, um de cada vez | desconectar o BT de um controle | baixo, e é o caminho provado |
| **(c)** | ler o serial **por rádio** | nenhum gesto físico | **demonstrado em 15/08 e NEGADO** — `EIO` nas duas tentativas, sem dano ao controle; ver §4 |

**Recomendação de quem escreveu esta página: (a) agora, (b) depois.**

> **NOTA DATADA — 15/08/2026: ela escolheu o contrário, e o caminho (b) já
> rodou.** A D-15 é *a cor do PLÁSTICO, lida do aparelho, por cabo E por
> rádio*, e a D-16 é *da PEÇA, porque a cor mora no APARELHO — sem arquivo por
> endereço*. Isso **derruba o caminho (a)**: um arquivo por `addr` foi
> justamente o que ela recusou. A recomendação fica registrada porque
> recomendação errada é dado, e porque a próxima pessoa precisa saber que a
> escolha foi consciente — mas **não é o plano**. O plano é (b), **feito**; e
> (c) foi **tentado no mesmo dia, e o rádio recusou** (§4) — a metade "por
> rádio" da D-15 continua **sem caminho**, e o que falta medir é a camada
> HIDP/L2CAP. Fonte de verdade:
> [AS-DECISOES-RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md).

**A palavra final é dela** ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).

## 6. Onde a cor entra na tela

A **D-1** já foi respondida: *a cor do jogador é a cor VIVA da lightbar, sempre com
número.* A cor do **plástico** é outra coisa, e as duas precisam conviver sem que a
tela tenha dois significados para "a cor dele".

Proposta a validar com o olho dela: a **borda** da guia carrega a cor do
**plástico** (é identidade física, não muda nunca), e o **preenchimento/swatch**
carrega a cor da **lightbar** (é estado, muda). Assim as duas cabem sem competir.

**Armadilha já paga por esta casa:** *"a cor da paleta não é a cor da barra"* —
as sprints 01, 02 e 03 têm mordida escrita exatamente contra trocar uma pela
outra. E contraste: a cor do plástico pode ser preta ou branca, e borda preta em
tema escuro não aparece — a regra de fallback precisa ser medida contra o tema, não
suposta.

## 7. A dívida de método que esta sprint deixa registrada

Três documentos citaram `UNIDADE-COR-01` por cinco dias sem que ela existisse, e a
medição que a sustenta ficou num transcrito. O portão
`test_nome_citado_como_sprint_existe` pegou a citação órfã — **mas nada pegou a
medição órfã.**

O irmão que falta: um portão que reprove **medição registrada só em transcrito de
agente**. Hoje não há como escrevê-lo (o transcrito não é versionado), mas a regra
humana é simples e vale escrever: **medição sobre o aparelho tem como destino o
mapa de canais, não um comentário nem um relatório.**

Ver [[as-specs-sao-a-memoria-externa-dela]] — as specs são memória, e memória que
não é alimentada não protege ninguém.
