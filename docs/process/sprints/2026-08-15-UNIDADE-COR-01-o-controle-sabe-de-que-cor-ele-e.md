# UNIDADE-COR-01 — o controle sabe de que cor ele é

- **Escrito em:** 15/08/2026, sobre `c8065d8`
- **Grau:** **MEDIDO** no que descarta; **CAMINHO IDENTIFICADO, NÃO MEDIDO** no que propõe.
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

**Grau: CAMINHO IDENTIFICADO, NÃO MEDIDO por nós.** Nenhum dos quatro controles
dela teve o serial lido — ver a seção 4, que é o motivo.

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

E a leitura **só está provada por cabo**: o `dualshock-tools` recusa Bluetooth de
saída. Por rádio o canal existe (`0x80`/`0x81` estão no descritor destes
controles), mas ninguém demonstrou.

Por Bluetooth há ainda o CRC-32 semente `0xA3` nos quatro últimos bytes, que esta
casa já sabe calcular (`core/ds_output_report.py`, `bt_crc32`).

## 5. Os três caminhos, com o preço de cada um

| | o quê | custo | risco |
|---|---|---|---|
| **(a)** | ela escolhe a cor de cada controle na interface, uma vez, salvo por MAC | um gesto por controle, uma vez | **zero** |
| **(b)** | ler o serial **por cabo**, um de cada vez | desconectar o BT de um controle | baixo, e é o caminho provado |
| **(c)** | ler o serial **por rádio** | nenhum gesto físico | território não demonstrado |

**Recomendação: (a) agora, (b) depois.** A cor na tela não precisa esperar a
leitura automática — o `controllers.json` já é indexado por `addr` e já lista os
quatro. E o `hardware_version` serve de âncora enquanto isso.

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
