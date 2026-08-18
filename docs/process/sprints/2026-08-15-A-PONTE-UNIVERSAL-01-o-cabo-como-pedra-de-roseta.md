# A PONTE UNIVERSAL-01 — o cabo como pedra de Roseta, e a ponte que já roda com um `if`

- **Escrito em:** 15/08/2026, 19h40, na branch `restauro/inicio-da-sessao`, com a
  árvore suja e os quatro controles de pé — **dois no cabo e dois no rádio, com
  os braços trocados por ela às 19h**.
- **Grau:** **PLANO.** Nenhum ensaio deste documento foi executado. O que aqui
  aparece como **MEDIDO** foi lido do repositório, dos brutos versionados e do
  fonte C durante o desenho; nenhum `/dev/hidraw` foi aberto por esta passagem.
- **Índice da leva:** [a cor do controle e o som de cada jogador](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
- **Método:** as quatro leis de
  [PLANO DA MESA 2+2](../estudos/2026-08-15-PLANO-DA-MESA-2-2-o-que-so-se-mede-com-quatro.md).
  Nenhuma é negociável, e a seção 7 diz onde cada uma morde neste plano.
- **Custo total:** **5 h 35 de máquina**, mais **um bloco dela de 49 minutos** —
  35 de olho, 10 de ouvido, 4 de mão. O bloco é **um só**, fica **no fim**, e
  **nada acima dele depende dele**, como manda a Lei 2. Cai para 39 minutos se o
  E-1 discriminar e o M-7 não precisar rodar.

---

## 1. O que ela pediu, e o que isso quer dizer tecnicamente

Ela pediu duas coisas em duas falas, e a segunda é a que governa este documento:

> *"A ideia do claude foi muito boa de construirmos identificadores do cabo pra
> através deles ou mapearmos os canais bt ou construirmos um meio pelo qual a via
> bt faça uso do canal de cabo, assim conseguiríamos parear 100% cada feature do
> cabo documentada com a do bt."*

> *"faz um plano pra seguirmos a metodologia pra mapearmos o bt ou construirmos a
> ponte universal para que possamos **IMPLEMENTAR** elas."*

Um **identificador do cabo** é uma coisa concreta — um comando, uma struct, um
report id, um feature, um nó do kernel — que existe no transporte **documentado**
e que se pode ir procurar, com endereço, no transporte **opaco**. O cabo é a
pedra de Roseta porque é o único lado com os dois textos deitados um ao lado do
outro: a Sony documentou o USB, o `hid_playstation` implementa o USB primeiro, e
é no cabo que quase toda medição desta casa foi feita. O rádio é onde o produto
dela precisa funcionar e é onde não existe documento nenhum. Traduzir um pelo
outro não é metáfora: é achar, para cada feature, o objeto que atravessa os dois.

O objeto central não é hipótese desta sessão — é uma `struct` com `static_assert`
no fonte da Sony. O **`common` de 47 bytes** é o corpo do comando de saída, os
dois caminhos de transporte se juntam num ponto único do driver
(`hid-playstation.c:1402` e `:1413`), e depois dali as 112 linhas do
`dualsense_output_worker` escrevem em `common->…` **sem um único
`if (hdev->bus == …)`**. O comentário do próprio autor, em `:368-372`, é a frase
que funda o pareamento: *"largely the same between Bluetooth and USB except for
different headers and CRC"*. O transporte acrescenta exatamente três coisas e
nada mais: o report id, o byte de sequência com o tag, e o CRC-32 nos quatro
últimos bytes. Na entrada é ainda mais simples — uma struct só, ancorada em
`data[1]` no cabo e `data[2]` no rádio: **o pareamento de toda linha de entrada é
uma soma de +1.**

A prova de conceito é da madrugada de 15/08 e não é argumento, é firmware
executando: o **mesmo `common` de 47 bytes** foi mandado por `0x31`, `0x32` e
`0x39` — três degraus de 78, 142 e 547 bytes — e a lightbar acendeu a cor pedida
nos três, com o olho dela, por rádio. Disso seguem duas coisas. A primeira: o
identificador do cabo **já atravessa**, e atravessa em degrau que ninguém tinha
tentado. A segunda, e é a que ordena este plano: **o que falta não é DESCOBERTA,
é MEDIÇÃO e é CÓDIGO.** Das 98 linhas pareáveis do DualSense, 87 já têm
identificador achado com endereço no fonte. E do lado do produto a ponte também
já existe: `_build_common` (`core/backend_pydualsense.py:975`) é uma função **sem
parâmetro de transporte**, e `:1136` é o **único `if` de transporte do caminho de
saída inteiro**. Quando ela escreve *"construirmos um meio pelo qual a via bt
faça uso do canal de cabo"*, o meio está escrito e roda todo dia — o que falta é
ele saber dizer o próprio nome, e é o que a seção 3 desenha.

---

## 2. O que já está provado — e ninguém remede

Esta seção é o alicerce. Cada linha tem bruto versionado ou endereço no fonte.

### 2.1 A TROCA DE BRAÇOS de 15/08 às 19h — ela fez, e resolveu a Lei 4

Os **mesmos quatro aparelhos** passaram pelos **dois transportes**, com minutos
de diferença. É a inversão limpa que nunca tinha sido feita, e é o que separa
*"é do transporte"* de *"é daquela unidade"*. Bruto:
[`docs/data/ensaios-brutos/2026-08-15-TROCA-DE-BRACOS-os-mesmos-quatro-nos-dois-transportes.txt`](../../data/ensaios-brutos/2026-08-15-TROCA-DE-BRACOS-os-mesmos-quatro-nos-dois-transportes.txt).

| aparelho | `hardware_version` | antes das 19h | depois |
|---|---|---|---|
| `d4:2f:4b:00:00:d8` | `0x1111` | cabo | **rádio** |
| `a0:fa:9c:00:00:f0` | `0x0710` | cabo | **rádio** |
| `44:46:48:00:00:03` | `0x0811` | rádio | **cabo** |
| `14:3a:9a:00:00:ab` | `0x0711` | rádio | **cabo** |

| o que | segue | a prova |
|---|---|---|
| o descritor HID inteiro (9 reports exclusivos, união de 24) | **o TRANSPORTE** | idêntico antes e depois, byte a byte |
| a placa de áudio USB | **o TRANSPORTE** | nasce sempre dos que estão no cabo agora |
| o estado de carga (`Full` × `Discharging`) | **o TRANSPORTE** | inverteu junto com os braços |
| a taxa de entrada de 250,0 Hz cravados | **o CABO** | os quatro deram 250,0 no cabo; no rádio, 157,8 a 381,5 Hz |
| `hardware_version` | **a UNIDADE** | `0x1111` continua colado no `d4:2f:4b` |

**E o custo de `GET_FEATURE` por rádio, medido de novo:** 18 leituras, todas em
uma tentativa, 12 em 0,01 s. Somadas às 14 da corrida das 17h32, são **32 de 32
leituras instantâneas em duas rodadas independentes com unidades diferentes em
cada braço**. A afirmação de que *"cada falha custa 3,2-3,7 s e a cura é
REPETIR"* — que três células do mapa chamavam de *"regra que vale para toda
medição futura desta casa"* — está derrubada, e a substituição **já está no
CSV**. O timeout de 3 s do BlueZ existe; o que caiu é que ele seja o regime.

**A ressalva que pertence ao título, e não ao rodapé:** a troca de braços
resolveu a Lei 4 **onde há dado dos dois lados**. Para o pareamento **byte a
byte** de feature reports que a ideia dela pede, ela é uma **porta de mão única
já perdida**: o `censo_features.py` grava amostra de 12 bytes, não dump
hexadecimal completo, então não existe em lugar nenhum o conteúdo inteiro do
mesmo aparelho nos dois braços. Quem citar este bruto como *"Lei 4 resolvida"*
sem essa frase está mentindo por omissão.

### 2.2 A escada, lida do descritor dos aparelhos dela

```
  cabo   289 B de descritor  ->  UM output:    0x02 (48 B no fio)
  rádio  320 B de descritor  ->  NOVE outputs: 0x31(78) 0x32(142) 0x33(206)
                                               0x34(270) 0x35(334) 0x36(398)
                                               0x37(462) 0x38(526) 0x39(547)
```

Sobe +64 por degrau até o `0x38`; o `0x39` é teto (+21, seria 589). **O rádio é o
transporte RICO, não o pobre** — e o `common` ocupa `report[3..49]` em todos.
Executaram, com o olho dela: `0x31` (controle positivo), `0x32` (verde) e `0x39`
(azul). Os degraus `0x33` a `0x38` **nunca foram tentados**, e a escada foi
provada em **um** aparelho — o branco, `hw 0x0711`, que a troca de braços pôs no
cabo.

### 2.3 O golden que já está no disco, e ninguém transformou em teste

[`docs/data/ensaios-brutos/2026-08-15-144356-byte-no-fio.txt`](../../data/ensaios-brutos/2026-08-15-144356-byte-no-fio.txt)
guarda **dois reports `0x31` de 78 bytes inteiros, capturados no ar pelo
`btmon`**, com a cor mágica `11 22 33` nos offsets 47/48/49 e o CRC conferido.
Não são opinião nem documento: são o quadro que o firmware **aceitou** e que
acendeu a barra. Trinta de sessenta quadros por handle, duas rodadas, duas cores,
com o kprobe em `dualsense_send_output_report` casando 30 a 30.

### 2.4 O placar de hoje, recontado nesta passagem

A tabela de Roseta contou 106 linhas de `controle=dualsense` e 22 pareadas. **Os
dois números mudaram enquanto ela era escrita**, e o plano usa os de agora, lidos
com `csv.DictReader` às 19h40:

| | tabela de Roseta (18h28) | o CSV agora (19h40) |
|---|---|---|
| linhas de `controle=dualsense` | 106 | **107** (nasceu `plataforma.declarado_sem_resposta`) |
| não pareáveis por construção | 9 | 9 |
| **alvo** | 97 | **98** |
| **`medido` / `medido`** | 22 | **30** — 30,6% |

O portão está **verde**: 47 afirmações fortes, **zero** sem teste que morda; 28
graus fortes, **zero** sem ensaio no caderno; 103 ensaios lidos.

---

## 3. O DESENHO — a ordem, e por que ela é esta

### 3.0 O ACERTO DE CONTAS, que vem antes do desenho

**A tarde de 15/08 pagou boa parte do que os quatro desenhos desta noite ainda
propõem.** Está tudo na árvore, no índice, com o portão verde. Quem executar este
plano sem ler esta subseção vai refazer trabalho pago — que é o defeito mais caro
que esta casa nomeia, na sua forma menos glamourosa.

| o que os desenhos propõem | estado real, conferido no CSV e no fonte |
|---|---|
| a **colheita seca** (R-0 / M-0): promover as células cuja medição já existe | **FEITO.** O placar foi de 22 para 30 `medido/medido` hoje, com o portão verde |
| a **união dos 24 ids** nos dois braços (R-2 / M-1 parcial) | **FEITO às 19h26.** 78 leituras, quatro aparelhos, dois transportes. Nasceu a linha `plataforma.declarado_sem_resposta@dualsense` |
| o **`0x22` no braço do cabo** (E-8 do plano da mesa) | **FEITO às 19h33**, na corrida de depois da troca |
| a **troca de braços** (R-3 / a cura da Lei 4) | **FEITA por ela às 19h** |
| substituir `report[55]` → `report[54]` da bateria | **FEITO.** `energia.bateria.degraus/radio_offset` já diz `report[54]` |
| substituir os *"64 bytes"* do CRC no cabo | **FEITO.** A célula agora traz as três réguas separadas |
| substituir `outReport[10]` → `report[11]` do LED de mic | **FEITO.** `backend_pydualsense.py:3214` traz a correção datada |
| substituir a regra dos *"3,2-3,7 s por leitura por rádio"* | **FEITO** nas três células |
| virar `daemon_precisa_parar` de `True` para `False` no censo | **JÁ ESTÁ `False`** (`censo_features.py:541`), com a correção na docstring |

**O que sobra desse bloco inteiro é uma linha:** `plataforma.slot_jogador` ainda
diz *"a chave é o MAC/`uniq`, não o transporte"*, e a **D-30** (entregue em
`86563c2`) mudou isso — o número do jogador passou a sair da **ordem de chegada
daquele momento**, com o `rank` gravado sobrando como desempate. É fato caduco, e
fato caduco se substitui. Custo: dois minutos, dentro da Onda 5.

### 3.1 O mecanismo, numa frase

**A ponte universal não é mecanismo novo — é o mecanismo que já roda, obrigado a
dizer o próprio nome.** Ela se entrega em três peças que não dependem umas das
outras, e é por isso que podem ser ordenadas por risco em vez de por tamanho:

1. **Quatro curas que não precisam de tabela nenhuma** — uma função, dois `if`s e
   um casamento por sysfs. Nenhuma precisa de aparelho novo, duas curam defeito
   **ativo**, e uma delas chega à tela dela hoje.
2. **Dois experimentos que podem DERRUBAR a premissa fundadora** antes de
   qualquer código, e — pela forma como este plano os desenha — **sem que
   instrumento nenhum escreva um byte**.
3. **Uma tabela pequena em `src/`, que entra pela porta da LEITURA**, com
   consumidor no dia um.

### 3.2 As quatro curas, com endereço

**P-1 — o oráculo de transporte pelo `HID_ID` do uevent.** Confirmado no fonte:

```python
# core/backend_pydualsense.py:4516-4522
@staticmethod
def _detect_transport(ds: pydualsense) -> Transport:
    con = getattr(ds, "conType", None)
    if con is None:
        return "usb"                      # <- a mentira
    name = str(getattr(con, "name", con)).lower()
    return "usb" if "usb" in name else "bt"
```

Um controle de rádio cuja `pydualsense` devolva `conType is None` é classificado
como **cabo**. Essa linha alimenta o gate de CRC do feature `0x05` (`:1463`), o
gate de supressão de LED (`:2330`), a contagem de conexões novas (`:1985`), o
`state_full` (`:4297`) e o `_transport` em cache (`:2179`, `:2449`) — **se ela
mentir, todos mentem juntos.** A régua honesta é o barramento do `HID_ID`
(`0003` cabo, `0005` rádio), que é fato do kernel e que a bancada já usa
(`scripts/ensaios/comum.py:171-193`). O leitor de uevent do próprio backend está
**dez linhas acima do erro**, em `:133`. **Três dos quatro desenhos desta noite
convergiram nesta cura de forma independente** — e convergência independente é o
sinal mais forte que apareceu em toda a rodada.

**P-2 — o discriminador `raw[1] & 0x02` no `_struct_base`.** Confirmado no fonte:
`core/physical_report_reader.py:330-355` aceita **qualquer** `0x31` de 78 bytes
com CRC bom e trata como report de estado. Só que o quadro de Opus do microfone é
também um `0x31` de 78 bytes e passa pelo **mesmo CRC** — quem nomeia o bit é o
outro módulo (`integrations/dualsense_bt_audio.py:186-194`: `INPUT_FLAG_HID =
0x01`, `INPUT_FLAG_AUDIO = 0x02`). É a causa raiz, com bit e endereço, de *"mic
BT e giroscópio não coexistem"*: um `if`, um defeito que o usuário sente.

**P-3 — `enviar_release_leds` ganha o `if` de transporte que nunca teve.**
`core/lightbar_reset.py:40` monta **sempre** um `0x31` de 78 bytes, e
`backend_pydualsense.py:2687` itera **todos** os handles sem consultar o
transporte: na mesa mista de agora, dois DualSense **no cabo** recebem um report
de rádio. **Correção honesta ao material de origem:** a própria docstring diz
*"NÃO é chamado por caminho automático nenhum"* — é instrumento sob demanda, e o
raio de dano é um operador na mesa mista, não o produto em regime. Vale as cinco
linhas de `if` e vale muito mais como **controle negativo permanente** da tese
*"o comando é o mesmo, só o envelope muda"*; não vale a frase *"a casa já tem
escrita cega a transporte e ela é um bug"*, que infla o argumento.

**P-4 — o casamento placa ALSA ↔ controle pelo dispositivo USB pai.** É a única
coisa deste plano que chega **à tela dela**, e é a forma pura do defeito que o
`CLAUDE.md` chama de mais caro. A cadeia, lida inteira:

```
app/mic_monitor.py:183-223   escolher_fonte devolve None com mais de um DualSense
                             (só casa por MAC, por sufixo da ponte BT, ou 1-para-1)
app/mic_monitor.py:226-235   escolher_sink DELEGA a escolher_fonte
app/mic_monitor.py:557-559   o coletor PULA o controle quando o sink é None,
                             então `nomes` sai vazio
app/audio_saida.py:573-574   sem `sink_do_controle`:
                             AcaoRota(..., False, DICA_ROTA_SEM_SINK, "")
```

Resultado: **o botão "Ouvir no controle" está insensível AGORA, nos quatro
cards.** E a cura está escrita, testada em bancada e do lado errado da fronteira:
`scripts/ensaios/audio_por_transporte.py:80`, `_dispositivo_usb_pai()`, cuja
própria docstring diz *"com dois controles no cabo, adivinhar por ordem erraria
metade das vezes"* — no cabo o áudio pendura na interface `:1.0` e o HID na
`:1.3`, e as duas são filhas do mesmo dispositivo USB.

Isso **desfaz uma recusa deliberada de 01/08** (*"exibir o mic do controle errado
é pior que não exibir nenhum"*), e só o casamento por sysfs autoriza desfazê-la.
A regra do *"um para um"* fica como **último** degrau; nunca se casa por posição
nem pelo sufixo `-00`/`-00.2` do PipeWire.

### 3.3 Os dois experimentos que podem derrubar premissa

**E-1 — o corpo do `0x32` é TLV ou é o `common`?** É o melhor minuto por decisão
de tudo o que se escreveu esta noite, e este plano o melhora num ponto que muda a
lei que se aplica a ele.

O produto monta o pedido de microfone assim
(`integrations/dualsense_bt_audio.py:241-257`):

```python
pkt[2] = BLOCO_AUDIO_CONTROL | BLOCO_PRESENTE   # 0x11 | 0x80 = 0x91
pkt[3] = 1                                       # comprimento do bloco
pkt[4] = AUDIO_CONTROL_MIC_ON if ligar else AUDIO_CONTROL_MIC_OFF   # 0b011 / 0b010
```

Sob a leitura **TLV**, `[2]` é tag, `[3]` é comprimento, `[4]` é valor. Sob a
leitura da **escada**, no rádio o `common` começa em `report[3]` — então `pkt[3]`
é `valid_flag0` e `pkt[4]` é `valid_flag1`.

| pacote | previsão TLV | previsão `common` |
|---|---|---|
| **LIGAR** (`0b011`) | bit0 = 1: mic ligado | flag1 `0x03` autoriza `common[8]` e `common[9]`, ambos zero: **desmuta** |
| **DESLIGAR** (`0b010`) | bit0 = 0: **mic MUDO** | flag1 `0x02` autoriza `common[9] = 0x00`: **DESMUTA** |

**As duas leituras preveem o MESMO resultado para o pacote de LIGAR** — e é
exatamente por isso que o WAV gravado em 25/07 nunca decidiu nada. **Para o
pacote de DESLIGAR elas preveem o OPOSTO.** O veredito é legível por máquina no
próprio módulo: `INPUT_OFFSET_AUDIO_STATUS = 55`, `STATUS_MIC_MUDO = 0x04`.

**A contribuição deste plano, e é o que tira o E-1 da Lei 3:** nenhum instrumento
precisa escrever. O produto já tem o comando —
`hefesto-dualsense4unix mic bt` sobe a ponte (`_escrever_pedido(ligar=True)`,
`:898`) e pará-la escreve o DESLIGAR (`:917`). E o produto já tem o **controle
positivo**: `hefesto-dualsense4unix mic mute`, que mexe no mudo do **firmware**
pelo caminho do `0x31` (`common[9]`, `POWER_SAVE_MIC_MUTE = 0x10`, com
`VALID_FLAG1_POWER_SAVE_CONTROL_ENABLE`). O instrumento **só lê o hidraw pelo
broker e conta bits.** Toda escrita é do produto, em regime, pela CLI que ele já
entrega. Isso muda o E-1 de *"escreve, logo é bloco dela"* para *"lê, logo roda
agora"* — e é por isso que ele abre a fila.

**Reenquadramento obrigatório, contra o material de origem:** o repositório já
declara `BLOCO_SET_STATE = 0x10` (`:216`). Logo o `0x10` do `common` **é** o tag
do SetState, e as duas leituras **podem estar as duas certas** — a contradição
estava mal posta. O E-1 sobrevive ao reenquadramento porque a previsão do pacote
de DESLIGAR continua oposta; a retórica de *"nos dois desfechos alguma coisa sai
errada"* não sobrevive, e sai.

**E-2 — quantas autoridades de sequência escrevem no mesmo enlace?** Trinta
minutos de `btmon` passivo, zero escrita, e é **pré-requisito duro** de qualquer
unificação de contador. Hoje há três: o `output_seq` do `hid_playstation`, o
`_bt_seq` do `writeReport` (`:1193-1199`) e o `_seq` próprio da ponte de mic
(`:831`, `:1011`, escrevendo com `os.write` num fd próprio, **fora** do
`_write_lock` do handle). O cabeçalho do módulo (`:54-70`) declara que a
mitigação é *"estrutural, não sorte: são report IDs diferentes"* — e declara
também, com todas as letras, que **ninguém sabe se o firmware mantém um contador
ou vários**. O mesmo cabeçalho afirma que *"o kernel continua dono absoluto do
fluxo do 0x31"*, e isso é falso: o backend carimba `0x31` próprio. **Tanto a
ponte que unifica os contadores quanto qualquer áudio de saída em regime apostam
arquitetura nessa resposta, e nenhum dos quatro desenhos a mede.**

### 3.4 A tabela — pequena, e pela porta da leitura

`tests/conftest.py:1244-1345` **já é a tabela de Roseta em código**:
`EnvelopeDeTransporte`, com `report_id`, `tamanho_do_report`,
`deslocamento_do_common`, `tag`, `semente_do_crc` e `tem_nibble_de_sequencia` —
e os valores **não são digitados**: ou vêm importados de produção, ou são
**medidos** chamando o builder (`_medir_deslocamento_do_common:1223`). Está só do
lado errado da fronteira `src/` × `tests/`.

Ela sobe para `src/hefesto_dualsense4unix/core/envelopes.py` <!-- ref-externa: módulo a CRIAR pela Onda 5 deste plano; hoje a tabela mora em tests/conftest.py --> com
**quatro correções e um limite**, e cada uma tem dono:

**(a) A chave é TRIPLA: `(sentido, transporte, report_id)`.** O material de
origem propõe um dicionário `{(id, tamanho) → envelope}`, e não fecha: o `0x31`
de 78 bytes é **entrada E saída**, mesmo id, mesmo tamanho, sentidos opostos.
`envelope_do_buffer(buf, sentido)` **exige** o sentido e não tem valor padrão —
um padrão ali seria um jeito novo de mentir, calado.

**(b) Três réguas de tamanho, separadas e nomeadas.** `tamanho_no_fio` (48 no
cabo, 78 no `0x31`), `tamanho_no_driver` (63, o `DS_OUTPUT_REPORT_USB_SIZE` do
`static_assert` em `hid-playstation.c:366`) e `tamanho_no_descritor` (48, medido).
Os três números estão certos em réguas diferentes, e foi a confusão entre eles
que pôs *"64 bytes"* numa célula do portão.

**(c) A tabela entra COM CONSUMIDOR, e o consumidor é a LEITURA.** Uma tabela em
`src/` que ninguém importa tem exatamente a forma de `BLOCO_SPEAKER = 0x13` —
declarado em `dualsense_bt_audio.py:219` desde 25/07, com **uma** ocorrência em
`src/` (a própria declaração) e zero chamadores. Não se cura *"a casa sabe e o
produto não faz"* criando mais um declarado e nunca ligado. Os consumidores do
dia um são `_struct_base` (`physical_report_reader.py:330`) e o
`body = report[1:]` de `integrations/uhid_gamepad.py:2073` — os dois do lado
onde **errar produz dado errado**, que um teste enxerga, em vez de report
descartado em silêncio, que só o olho dela enxerga.

**(d) A circularidade sai no MESMO commit, ou a tabela não entra.** No dia em que
os builders passarem a vir da tabela, `_medir_deslocamento_do_common`
(`tests/conftest.py:1223`) passa a medir o número que ele mesmo forneceu — um
teste que passa com a cura arrancada, que é o defeito-mãe desta casa aplicado a
si mesmo. A tabela não é fonte dos builders nesta leva: os builders continuam
sendo a fonte, e a tabela os **mede**. Se alguém um dia inverter a seta, a
medição do conftest tem de ser substituída por oráculo externo **no mesmo
commit**.

**O limite, e ele é o critério de aborto:** entra a tabela de **envelopes**, que
tem cinco linhas e cada uma é conferível contra o fonte ou contra o fio. **NÃO
entra** a tabela de campos com colunas `grau` e `de_onde_sei` — isso é um segundo
mapa, com as mesmas linhas fracas, agora onde é mais caro mexer. Documentação com
`import` continua sendo documentação.

### 3.5 O que NÃO entra, e é decisão deste plano

- **A migração do caminho de SAÍDA** (`prepareReport`, `writeReport`, os dois
  builders de lightbar) para um escritor único. Ali moram três defeitos já pagos
  — BTREPORT-02, LIGHTBAR-BT-RESET-03 e LAÇO-DE-ESCRITA-02 — e os três têm a
  **mesma assinatura**: o firmware descarta em silêncio e o log diz sucesso. Não
  há leitura de volta em transporte nenhum, então os testes ficariam verdes
  montando o mesmo buffer e quem descobriria a regressão é ela, com a barra
  apagada. Um refactor cujo único detector é o corpo dela é precisamente o que a
  Lei 2 existe para impedir.
- **Unificar os dois contadores de `seq`** antes do E-2. Trocar uma mitigação
  estrutural existente por uma hipótese não medida é aumentar risco chamando de
  higiene.
- **Fazer a pintura avulsa por hidraw valer no CABO.** É escrita nova onde não
  havia nenhuma, por baixo de um jogo, num transporte que nunca teve o problema
  de claim que motivou a rota. Não fica *"desligada por padrão"*: fica fora.
- **Qualquer produto de áudio de saída por rádio** — codificador Opus,
  `module-pipe-sink`, bloco `0x13`. Os parâmetros vêm de fonte única jamais
  medida aqui, a jusante de uma hipótese de cadeia TLV cuja evidência direta são
  dois reports de bloco **único**. E entregaria um segundo escritor contínuo a
  50 Hz no enlace, que é a violação literal da única defesa escrita que existe
  (*"só na borda, nunca em regime"*).
- **PCM contínuo nos motores voice-coil** (o bloco `0x12` por três segundos). É o
  único item de toda a rodada que pode estressar hardware de um jeito sem `git
  revert` e com detecção **nenhuma**: um VCM degradado não acende log, não derruba
  enlace, e não se atribui a uma tarde de agosto.

---

## 4. AS ONDAS

Ordenadas por **dependência real** e, dentro dela, por: (1) o que pode derrubar
premissa, (2) o que perece, (3) rendimento. **Não** por células por minuto — essa
métrica premia transcrição de leitura de fonte e pune os dois únicos ensaios que
produzem conhecimento que ninguém tem.

### Onda 1 — O BOTÃO MORTO (40 min · não exige nada dela · 0 células)

**Entrega:** o botão *"Ouvir no controle"*, hoje insensível nos quatro cards,
passa a funcionar. Portar `_dispositivo_usb_pai()` de
`scripts/ensaios/audio_por_transporte.py:80` para `app/mic_monitor.py`, e fazer
`escolher_fonte` (`:183`) e `escolher_sink` (`:226`) casarem placa e controle
pelo **dispositivo USB pai** antes de cair na regra do "um para um".

**Por que primeiro:** não toca rádio, não abre hidraw, não usa a mesa perecível,
não depende de resposta de ensaio nenhum, e é a **única linha de todo este plano
que chega à interface** — que é onde ela fixou em 09/08 que tudo tem de chegar.
Zero células no mapa: é produto, não medição, e o plano não finge o contrário.

**A onda seguinte ganha:** nada tecnicamente. Ganha que a sessão não termine com
a máquina igual, que é o critério dela.

**Fecha com foto:** par antes/depois, pela PROVA-DE-TELA-01. E **nenhum texto de
interface promete som no alto-falante** — a rota acende; para onde ela leva, é o
ensaio A-1 que diz.

### Onda 2 — OS DOIS QUE PODEM DERRUBAR (55 min · não exige nada dela · 2 células)

**Entrega:** E-1 (o corpo do `0x32`, 25 min) e E-2 (o censo dos escritores do
enlace, 30 min). Nenhum instrumento escreve um byte: no E-1 quem escreve é a CLI
do produto; no E-2 o `btmon` é sniffer passivo.

**Por que aqui:** são os únicos dois de toda a rodada capazes de **derrubar uma
premissa antes de existir código em cima dela**. Se o E-1 der `common`, o modelo
TLV inteiro desta casa está errado e o `BLOCO_SPEAKER = 0x13` sai como hipótese
refutada em vez de dívida. Se der TLV, o `[2]` é campo e não constante, e a
coluna `tag` da tabela de envelopes nasce variável em vez de fixa.

**A onda seguinte ganha:** a forma da coluna `tag`; e a autorização (ou o veto)
para qualquer unificação de contador de sequência, hoje apostada por dois
desenhos sem medição.

### Onda 3 — AS TRÊS CURAS QUE SÃO UM `if` (90 min · a foto dela no fim · 3 células)

**Entrega:** P-1 (o oráculo pelo `HID_ID`), P-2 (o `raw[1] & 0x02` no
`_struct_base`), P-3 (o `if` de transporte no `enviar_release_leds`). Cada uma
com o seu teste que morde, escrito **antes** — e o portão é cego a arquivo novo,
então roda depois do `git add`.

**Por que aqui e não antes:** o P-1 muda **dois gates ao mesmo tempo** (o CRC do
feature `0x05` e a supressão de LED). Se hoje algum controle está classificado
como cabo por engano e a supressão está desligada nele por acaso, a cura **liga**
a supressão e a barra dele muda de comportamento: **cura correta parecendo
regressão**. Isso exige foto antes e depois, e a foto é dela — por isso o
fechamento desta onda mora no bloco dela, mesmo que o código seja escrito agora.

**A onda seguinte ganha:** um oráculo de transporte que não mente, que é
pré-condição de qualquer tabela chaveada por transporte.

### Onda 4 — A MESA PERECÍVEL (55 min de máquina + o bloco dela · ~14 pares)

**Entrega, na ordem — e a linha grossa no meio é a Lei 2:**

| passo | o que | custo | exige dela |
|---|---|---|---|
| 4.1 | **M-2 — a struct de entrada nos oito nós na mesma janela**, passada passiva: bateria, jack, `sensor_timestamp`, IMU em repouso | 35 min | nada |
| 4.2 | **M-8 — o `0,21 s` do cabo é o aparelho ou o instrumento?** | 20 min | nada |
| | ======================== **O BLOCO DELA** ======================== | **49 min** | |
| 4.3 | **M-3 — a struct outra vez, passada ATIVA**: touchpad, sticks ao batente, gatilhos ao fim, um botão | 10 min | **a mão**, 3 min |
| 4.4 | **A-1b — o fone plugado**, nos dois braços, para nomear o bit que muda entre o `0x08` do cabo e o `0x40` do rádio | 5 min | **a mão**, 1 min |
| 4.5 | **A-1 — qual canal do sink é o alto-falante** (a D-28) | 10 min | **o ouvido**, e **ela fala primeiro** |
| 4.6 | **M-6 — a escada `0x33`-`0x38`** numa unidade que não provou a escada | 20 min | **o olho** |
| 4.7 | **M-7 — o tag `0x90`** — só se o E-1 não tiver discriminado | 10 min | **o olho** |
| 4.8 | **A foto antes/depois do P-1**, nos quatro cards | 5 min | **o olho** |

**O bloco dela são 49 minutos, não 15**, e o plano prefere dizer o número a
maquiá-lo. O que a Lei 2 cobra não é que ele seja curto: é que seja **um só**,
que fique **no fim**, e que **nada acima dele dependa dele** — e os passos 4.1 e
4.2 fecham sozinhos, com veredito de máquina, mesmo que o bloco nunca role.

**Sobre o instrumento do 4.1:** ele **reusa**, não se constrói. `comum.py` para a
mesa e a porta do broker, o `PERFIL_DO_TRANSPORTE` de `imu_no_cabo.py:127-130`
para as duas âncoras, o laço de `select` de `taxa_no_hidraw.py` para os oito nós
na mesma janela. Gastar 60 minutos escrevendo instrumento novo com a mesa
perecível de pé é gastar o escasso no abundante — se algo faltar, colhe-se a
janela com o que já roda e constrói-se depois que a mesa cair.

**Por que esta onda depende das anteriores:** não depende tecnicamente. Depende
da **palavra dela** para os passos 4.6 e 4.7, que são os únicos deste plano em
que um instrumento escreve no aparelho. A Lei 3 é dela.

**A onda seguinte ganha:** os offsets conferidos byte a byte, que é o que a regra
13 do portão vai cobrar da tabela.

### Onda 5 — A TABELA, COM CONSUMIDOR NO DIA UM (95 min · nada dela · 0 células)

**Entrega:**

1. `core/envelopes.py` <!-- ref-externa: módulo a CRIAR por esta onda, ainda não existe --> — a tabela de envelopes, chave tripla, três
   réguas de tamanho separadas. `tests/conftest.py:1244-1345` passa a
   **importar** em vez de definir, sem alterar um valor.
2. **O golden do fio (P-5)** — os dois `0x31` de 78 bytes do bruto de 15/08,
   replicados byte a byte pela tabela, com CRC. **Se o bruto sumir, o teste
   FALHA — nunca `skip`.** Golden que se autodesliga é a forma mais educada de
   mentir.
3. Os dois consumidores da LEITURA: `_struct_base` e `uhid_gamepad:2073`.
4. **A regra 13 do portão**, `offset-que-o-codigo-desmente` (FALHA): para toda
   linha cuja chave esteja na tabela, `cabo_offset` e `radio_offset` têm de bater
   com a soma da tabela. **Chave ausente é PULADA E CONTADA, nunca aprovada** — e
   o número de puladas sai impresso. Regra que aprova em silêncio o que não
   consegue olhar é regra desligada, e esta casa já mediu essa exata falha.
5. A substituição do fato caduco em `plataforma.slot_jogador` (a D-30).

**Por que por último:** não fecha uma célula, não cura um defeito presente, e não
precisa de aparelho nenhum. É a onda que **não perece**.

---

## 5. OS ENSAIOS, na forma da metodologia

Cada um traz o rótulo de confundimento na convenção corrigida: **IMUNE** e
**CONFUNDIDO** falam do confundimento braço/unidade da Lei 4; onde não há braço
nenhum envolvido o rótulo é **N/A — não há aparelho**. Carimbar IMUNE em ensaio
que não toca aparelho infla a contagem de imunes e barateia a palavra onde ela
precisa ter peso.

---

### E-1 — O corpo do `0x32`: contêiner TLV ou o `common` de 47 bytes?

**Pergunta.** O pacote que o produto já envia em regime quando alguém desliga o
microfone por rádio — `montar_pedido_de_mic(ligar=False)` — é lido pelo firmware
como um bloco TLV de AudioControl, ou como o `common` com `valid_flag0 = 1` e
`valid_flag1 = 0x02`?

**Confundimento:** **IMUNE.** O veredito é um bit do próprio aparelho mudando (ou
não) em resposta ao próprio produto; não há comparação entre braços.

**Porta e biblioteca.** Broker (`SCM_RIGHTS`) para ler o hidraw físico do
controle no rádio. Biblioteca: `os.read` e `zlib` do `.venv/bin/python`, por
caminho de arquivo, e nada mais. **A escrita é toda do produto**, pela CLI
`hefesto-dualsense4unix mic bt` e `mic mute`.

**Controle positivo — e ele INDICIA O INSTRUMENTO.** Antes de qualquer coisa:
`hefesto-dualsense4unix mic mute` (que mexe no mudo do firmware pelo `common[9]`,
`POWER_SAVE_MIC_MUTE = 0x10`) e depois `mic unmute`. O bit `0x04` de
`report[55]` **tem de se mover nos dois sentidos**. Se não mover, o réu é o
instrumento — ou o daemon, que escreve `0x31` a 60 Hz com
`POWER_SAVE_CONTROL_ENABLE` sempre asserido e `common[9]` a cada quadro — **e o
ensaio NÃO emite veredito.**

**Controle negativo.** Duas coisas na mesma corrida: (a) o byte vizinho,
`report[54]` (o `status[0]` da bateria), que **não** pode se mover nas mesmas
janelas; (b) uma janela de 20 s sem comando nenhum, em que o bit tem de ficar
estável. Um bit que oscila sozinho não decide nada.

**O que vai para o mapa quando fechar.**

```
audio.microfone.mudo@dualsense
  radio_comando  : += "MEDIDO em 15/08/2026 (E-1): o corpo do 0x32 é [TLV | o
                    common]. O pacote de DESLIGAR (0b010) [emudeceu | desmutou]
                    o microfone, lido no bit 0x04 de report[55], com o mute
                    pelo caminho do 0x31 como controle positivo."
  radio_ate_onde_foi : O APARELHO OBEDECEU        # + linha em ensaios.csv (regra 6)

vibracao.haptics_vcm@dualsense
  radio_ressalva : += "A contradição TLV × common do byte [2] foi DECIDIDA em
                    15/08/2026 pelo E-1. [resultado]. O repositório já declarava
                    BLOCO_SET_STATE = 0x10, então a pergunta 'é um OU o outro'
                    estava mal posta: [o que sobrou de pé]."
```

**Nos dois desfechos alguma coisa hoje escrita como fato sai errada.** Se der
TLV, a leitura da escada de 15/08 precisa explicar por que o `0x10` sem bit7
também obedeceu. Se der `common`, o bloco de constantes de
`dualsense_bt_audio.py:216-225` vira hipótese refutada com nota datada, e o
`BLOCO_SPEAKER = 0x13` **sai** — não é decisão medida, é número que a medição
derrubou.

**Custo:** 25 min. **Exige dela:** nada.

---

### E-2 — O censo dos escritores do enlace

**Pergunta.** Quantas autoridades de sequência escrevem `0x31`/`0x32` no mesmo
enlace de rádio ao mesmo tempo, e o firmware mantém um contador ou vários por
report id?

**Confundimento:** **IMUNE** (é censo do próprio enlace, não comparação de
braços).

**Porta e biblioteca.** Nenhuma porta de hidraw: `sudo btmon -w`, sniffer passivo
do HCI, que não injeta nada. É a mesma disciplina do bruto de 15/08 e do
`byte_no_fio.py`.

**Controle positivo.** A captura tem de conter, identificados, os `0x31` que o
daemon emite em regime (60 Hz) — se o `btmon` não vir o que sabidamente está
saindo, ele não está olhando o enlace certo e não há veredito.

**Controle negativo.** A captura de um enlace **sem** controle de rádio ativo tem
de vir vazia de `0x31`. O bruto de 15/08 já tem esse par (`PAREADO-hci` e
`PAREADO-hci-controle-negativo`), e a corrida nova repete o padrão.

**O que vai para o mapa quando fechar.**

```
plataforma.crc32@dualsense
  radio_ressalva : += "MEDIDO em 15/08/2026 (E-2): [N] autoridades de sequência
                    escrevem no mesmo enlace. O nibble de report[1] observado
                    [rotaciona por report id | é um contador só]. A afirmação de
                    dualsense_bt_audio.py:54-70 de que 'o kernel continua dono
                    absoluto do fluxo do 0x31' é FALSA: o writeReport do backend
                    carimba 0x31 próprio."
```

**Custo:** 30 min. **Exige dela:** nada.

---

### M-2 — A struct de entrada nos oito nós, passada passiva

**Pergunta.** Cada campo do `dualsense_input_report` lê o valor certo, nos quatro
físicos e nos quatro vpads na **mesma janela**, com base 1 no cabo e base 2 no
rádio?

**Confundimento:** **IMUNE**, e a fuga é por **régua absoluta**, não por
comparação entre braços: a gravidade tem de dar 1 g; o nibble da bateria tem de
bater com `/sys/class/power_supply/*/capacity` do mesmo aparelho casado por MAC;
o CRC-32 de entrada tem de conferir. Nenhuma conclusão depende de comparar um
braço com o outro — o que, com os braços trocados, é redundância e não muleta.

**Porta e biblioteca.** Os quatro físicos pelo **broker**; os quatro vpads por
`open()` direto (os vpads têm ACL, o broker recusa vpad, e recusar é o
comportamento certo). O relatório imprime, por nó, qual porta serviu.
Biblioteca: `os`, `selectors`, `zlib`, `fcntl`, por caminho de arquivo.

**Controle positivo.** Três, independentes entre si: a gravidade a 1 g ± 3%
(`DS_ACC_RES_PER_G = 8192`); a bateria contra o sysfs; o CRC `0xA1` conferindo.

**Controle negativo — e o primeiro é o que faz este instrumento valer.**
(a) **A base errada**: o instrumento decodifica cada report do rádio **também**
com base 1 e imprime os dois. Com a base errada a gravidade sai longe de 1 g e o
nibble da bateria vira valor impossível. **Se as duas bases derem plausível, o
instrumento não mede o que diz medir e não emite veredito.** (b) Os quatro vpads
na mesma janela, separados pelo `HID_PHYS=hefesto-vpad`, nunca pelo VID/PID.
(c) Um `0x31` sintético com um byte do CRC virado tem de ser rejeitado.

**O que vai para o mapa quando fechar** — sete linhas, os dois lados, com a régua
escrita **uma vez em cada célula tocada**, para nunca mais alguém somar errado:

> `abs_cabo = 1 + offset_do_struct` · `abs_rádio = 2 + offset_do_struct`
> (**entrada**; na SAÍDA o `common` começa em `report[1]` no cabo e `report[3]`
> no rádio — são números diferentes)

```
energia.bateria.degraus         -> os dois : medido   (report[53] / report[54])
energia.bateria.percentual      -> cabo    : medido   (o rádio já é medido)
energia.bateria.jogo            -> os dois : medido   (o MESMO byte no físico e
                                   no vpad, mesma janela, casados por MAC —
                                   fecha a dívida do forward_battery sem chamador)
energia.bateria.leitura_hefesto -> os dois : medido   (e a célula DECLARA qual
                                   das três rotas é a do relatório)
movimento.imu.perda             -> os dois : medido   (sensor_timestamp =
                                   report[28..31] / report[29..32])
movimento.acelerometro.jogo     -> os dois : medido
movimento.giroscopio            -> os dois : medido
```

**Custo:** 35 min. **Exige dela:** nada — o DualSense parado na mesa já
transmite.

---

### M-3 — A mesma struct, passada ATIVA

**Pergunta.** Quando o dedo mexe, o byte que a tabela nomeia é o byte que muda —
nos dois braços, com os aparelhos hoje no transporte **oposto** ao da manhã?

**Confundimento:** **IMUNE** (a régua é o próprio movimento: o byte nomeado muda,
os outros não).

**Controle positivo.** O byte que a tabela nomeia muda quando o gesto acontece.
**Controle negativo.** Os bytes **vizinhos** não mudam no mesmo gesto, e o mesmo
nó lido numa janela sem gesto fica parado.

**A honestidade sobre o custo dela:** metade do que este ensaio fecha —
gatilhos e sticks até o batente, um botão — poderia ser exercitada sem ela se
houvesse como, e não há. O ensaio pede **3 minutos**, e diz que pede, em vez de
orçar o corpo dela como insumo barato.

**O que vai para o mapa:**

```
toque.touchpad          -> radio : medido   (report[34..37] e [38..41];
                            contact & BIT(7) = ponto inativo)
toque.touchpad.clique   -> radio : medido   (report[11] & 0x02)
toque.touchpad.cursor   -> radio : medido   — e a célula deixa de dizer
                            NAO MEDIDO apesar da observação dela de 11/08.
                            LER PELO VPAD: o co-op faz EVIOCGRAB no evdev FÍSICO
entrada.stick           -> os dois : medido
entrada.bruta           -> cabo : medido, E a ressalva do rádio muda: "o que
                            estava medido era a ROTA; agora os OFFSETS foram
                            conferidos byte a byte"
entrada.botoes          -> cabo : medido (os quatro no cabo, o que nunca
                            aconteceu). ARMADILHA na célula: o EVIOCGRAB do co-op
                            emudece o evdev físico para leitor externo
gatilho.analogico       -> os dois : medido   (report[5]/[6] e report[6]/[7])
```

**Custo:** 10 min. **Exige dela:** a mão, 3 min.

---

### A-1b — O fone plugado, nos dois braços

**Pergunta.** O `0x08` do cabo e o `0x40` do rádio, lidos para o **mesmo estado
lógico**, são o mesmo bit visto de dois lugares, ou o par não fecha?

**Confundimento:** **IMUNE** — a régua é a **variação de estado** do mesmo
aparelho consigo mesmo (com fone e sem fone), não a comparação entre braços.

**Por que ele existe:** hoje a célula lê dois números diferentes para o mesmo
estado, em bits que o driver não nomeia, com n=1 por unidade. **A troca de braços
NÃO resolve isto**: sem variação de estado, os dois números continuam sendo dois
números. Só o fone resolve.

**Controle positivo.** Plugar e despluguar tem de mover **algum** bit em
`report[54]` (cabo) / `report[55]` (rádio). **Controle negativo.** O byte vizinho
da bateria não pode se mover no mesmo gesto.

**O que vai para o mapa:**

```
audio.jack.deteccao@dualsense
  os dois de_onde_sei : medido
  cabo_ressalva : += "PAR QUE NÃO FECHAVA: 0x08 no cabo × 0x40 no rádio para o
                   MESMO estado lógico. Resolvido em 15/08/2026 pela VARIAÇÃO:
                   o byte lido com e sem fone, nos dois transportes, nomeia o
                   bit que MUDA. [resultado]"
```

**Custo:** 5 min. **Exige dela:** a mão, 1 min. **Se não houver fone em casa,
esta linha sai da onda** e continua com dois números e nenhuma explicação — e a
célula tem de dizer isso, em vez de ficar muda.

---

### M-8 — O `0,21 s` do cabo é o APARELHO ou o INSTRUMENTO?

**Pergunta.** O custo fixo de `GET_FEATURE` no cabo mora no aparelho, no
`hid_playstation`, ou na abertura de broker que o `censo_features.py` faz **uma
por leitura**?

**Confundimento:** **IMUNE** (é o mesmo instrumento contra si mesmo, em três
configurações).

**Por que ele existe, e é o ensaio que mais protege este plano:** ele fecha
**zero** células e **protege três**. Três células do mapa estão prestes a receber
*"o rádio é ~20 vezes mais rápido que o cabo para ler feature"*, e a evidência é
44 leituras no cabo dando **0,21 s cravados** — as que deram certo e as que deram
`EPIPE` igualmente. **Constância é assinatura de custo fixo de CAMINHO, não de
latência de aparelho.** E `censo_features.py:206` chama `abrir_no_hidraw`
**dentro** de `ler_feature`: uma ida ao broker por leitura.

**Desenho:** três corridas, subtração simples. **(A)** um `open` por leitura,
como hoje. **(B)** um `open`, N leituras. **(C)** N pares `open`/`close` **sem
ioctl nenhum**. Se (C) sozinho já custa ~0,21 s por ciclo, o número é da porta.

**Controle positivo.** A corrida (A) tem de reproduzir os 0,21 s já medidos.
**Controle negativo.** A corrida (C) no braço do **rádio** tem de ser barata — se
abrir custar caro nos dois, o suspeito é o broker e não o barramento.

**O que vai para o mapa:** nada de célula nova. O que muda é o **texto** das três
células de leitura de feature, que passam a separar custo de aparelho de custo de
porta em vez de publicar um fator de 20 vezes que pode ser do instrumento.

**Custo:** 20 min. **Exige dela:** nada.

---

### O BLOCO DELA — 15 minutos, no fim, e nada acima depende dele

#### A-1 — Qual canal do sink é o alto-falante? (a D-28)

**Pergunta.** O sink `analog-surround-40` declara quatro canais; qual deles sai
pelo alto-falante do controle?

**Confundimento:** **IMUNE** (é o mesmo aparelho, no cabo, contra si mesmo).

**A regra, e é dela:** **ela fala primeiro.** Se eu disser antes o que espero, a
única medição desta frente que depende do corpo dela nasce inválida.

**Controle positivo.** Um canal em que ela **ouve** alguma coisa. **Controle
negativo.** Um canal em que ela não ouve nada, na mesma passada. Se ela ouvir em
todos ou em nenhum, o roteamento não está fazendo o que se pensa e não há
veredito.

**Por que importa:** sem saber qual canal é o alto-falante, um silêncio por rádio
é **ininterpretável** — e a Onda 1 acabou de acender um botão de rota.

**Custo:** 10 min. **Exige dela:** o ouvido.

#### M-6 — A escada `0x33`-`0x38`, numa unidade que não provou a escada

**Pergunta.** Os seis degraus nunca tentados executam o mesmo `common`, num
aparelho que **não** é o que provou a escada?

**Confundimento:** **IMUNE** — a régua é a cor que ela pede aparecendo na barra,
absoluta.

**Autorizado por ela hoje:** escrever nos degraus `0x33`-`0x38` com o `common`
conhecido. É output, não NVS. O instrumento **recusa por construção** qualquer id
fora de `0x31`-`0x39` e herda a trava da família `0xF0`-`0xF7` de
`cor_do_plastico.py:308`.

**Controle positivo.** O `0x31`, que sabidamente executa, no mesmo minuto e no
mesmo aparelho. **Controle negativo.** **Apagar entre passos** — sem isso o
degrau N herda a cor do N-1 e a escada inteira sai falso-positiva. E um pacote de
tamanho errado, que o kernel aceita e o firmware descarta.

**O veredito é o olho dela, JAMAIS o retorno do `os.write()`** — que devolve
sucesso quando o **kernel** aceita e que em 15/08 aceitou até o pacote de tamanho
errado que era o controle negativo.

**O que vai para o mapa:**

```
plataforma.escada_de_output@dualsense
  radio_evidencia : += "MEDIDO em 15/08/2026 (M-6): os degraus 0x33 a 0x38
                     [executaram | não executaram] o mesmo common, no aparelho
                     de placa [hw], que NÃO é o que provou a escada em 15/08 de
                     madrugada. A escada deixa de ser n=1 em unidade."
```

**Custo:** 20 min. **Exige dela:** o olho. **Não move o placar de pares** — e
está escrito aqui, contra o interesse de quem escreve.

#### M-7 — O tag em disputa: `0x10` × `0x90` × `0x11` × `0x91`

**Pergunta.** O `report[2]` é constante mágica de envelope ou seletor de bloco
com bit7?

**Confundimento:** **IMUNE.**

**A pergunta estava MAL POSTA, e este plano a reescreve.** O repositório declara
`BLOCO_SET_STATE = 0x10` e `BLOCO_AUDIO_CONTROL = 0x11`, com
`BLOCO_PRESENTE = 0x80`. Então o `0x10` do `common` **é** o tag do SetState, e as
duas leituras podem estar as duas certas. A tabela-verdade tem quatro linhas e um
único discriminador:

| `report[2]` | se `[2]` é envelope constante | se `[2]` é tag TLV com bit7 |
|---|---|---|
| `0x10` | acende (é o que já se sabe) | acende (SetState sem bit7 — tolerado) |
| **`0x90`** | **não acende** (não é a constante) | **acende** (SetState com bit7) |
| `0x11` | não acende | não acende (é AudioControl, não SetState) |
| `0x91` | não acende | não acende |

**Só o `0x90` discrimina.** Se ele acender, o `[2]` é campo e não constante — e
qualquer tabela de envelopes escrita antes disso nasce com uma coluna a menos.

**Controle positivo.** O `0x10`, no mesmo minuto e no mesmo aparelho.
**Controle negativo.** O `0x00`, que não é nem uma coisa nem outra e não pode
acender.

**Rode-o só se o E-1 não discriminar** — o E-1 responde a mesma família de
pergunta e não cobra nada dela.

**Custo:** 10 min. **Exige dela:** o olho.

#### A foto do P-1

Par antes/depois nos quatro cards, com a supressão de LED e o gate de CRC do
feature já na régua nova. **Cura correta pode parecer regressão**, e é ela quem
diz se é uma ou outra.

**Custo:** 5 min. **Exige dela:** o olho.

---

## 6. O QUE ESTE PLANO NÃO FAZ

Dito na cara, porque quem lê plano de bancada lê o começo e o fim.

**Não entrega áudio de saída por rádio, e não chega perto.** Não há caminho de
dados de áudio de saída por rádio nesta casa — **zero linhas de código**. O que
existe é um canal que responde. A **falácia do canal que responde** faria
qualquer outra frase parecer justificada, e é por isso que este plano não escreve
nenhuma.

**Não toca as 10 linhas T4.** Não há identificador do cabo que as encontre no
rádio porque não há identificador **em transporte nenhum**:
`plataforma.modo_relatorio` (a mais importante das dez, e vazia dos dois lados),
`plataforma.handshake_usb`, `audio.leitura_de_volta`, `gatilho.leitura`,
`luz.led_jogador.leitura`, `entrada.stick.calibracao`, `energia.desligar`,
`vibracao.rumble.frequencia`, `movimento.imu.ligar` e `luz.recursos_proprios`.
Duas merecem nota: `plataforma.modo_relatorio` é literalmente onde mora *"fazer a
via BT usar o canal do cabo"* — e a pista sem dono é que o descritor do rádio
declara um INPUT `0x01` de **10 bytes** além do `0x31` de 78, e ninguém sabe que
estímulo faz o aparelho sair do report curto para o completo. E
`audio.leitura_de_volta` é o item de **maior alavanca** do T4: se algum dos 24
ids devolvesse o estado do `common`, ele fecharia dezenas de linhas de saída de
uma vez e tiraria 11 linhas da dependência do olho dela.

**Não promove as 16 linhas de paridade por AUSÊNCIA a `medido`.** *Qual é o
ensaio de bancada que mede "o LED de jogador do DualSense não pisca em
hardware"?* Não há: há a tabela do driver. Promover isso seria inventar medição,
que é o que a D-14 acabou de proibir rebaixando cinco células.

**Não migra o caminho de SAÍDA**, não unifica os contadores de sequência, não
liga `_pintar_por_hidraw_bt` no cabo, e não escreve `SET_FEATURE` na família
`0xF0`-`0xF7` — o bloqueio dela está mantido, e ler não autoriza escrever.

**Não fecha `audio.alto_falante` no EFEITO.** Quatro linhas de áudio
(`alto_falante.preamp`, `.rota`, `.volume`, `audio.jack.volume`) fecham no BYTE
por cor mágica no fio e **continuam abertas no efeito**, porque não há som saindo
por rádio para observar.

**Não toca Pro Controller nem 8BitDo.** Das 301 linhas do mapa, 194 não são de
`controle=dualsense`, e não há Pro nem 8BitDo nesta mesa. Os instrumentos de
`scripts/ensaios/` filtram por `054C:0CE6`.

**O que a mesa 2+2 continua não alcançando, mesmo com os braços trocados:** o
pareamento **byte a byte** dos feature reports. O `censo_features.py` grava
amostra de 12 bytes, não dump completo — então o conteúdo inteiro do mesmo
aparelho nos dois braços não existe em lugar nenhum, e a janela em que existiria
já passou. Custa mais uma troca, ou mover **um** controle por 30 segundos.

**E tudo aqui é n=4 de um modelo, um firmware `0x0110002a`, um host, um BlueZ, um
dongle** — com os quatro controles e o dongle no **mesmo xHCI `0000:0c:00.3`**.
Toda frase *"o rádio faz X"* é, a rigor, *"este dongle com este BlueZ faz X"*.

---

## 7. AS ARMADILHAS QUE ESTE PLANO TEM DE RESPEITAR

Cada uma já foi paga aqui. Não são recomendações.

**1. O `os.write()` mente.** Devolve sucesso quando o **kernel** aceita a entrega;
não espera veredito do firmware, e em 15/08 aceitou o pacote de tamanho errado
que era o controle negativo. Nenhum ensaio deste plano conclui a partir do
retorno da chamada. Como não há leitura de volta em transporte nenhum, o
observador independente é o olho dela, o `btmon`, ou o bit `0x04` do E-1.

**2. O instrumento pode estar brigando com o produto — e pode estar
FABRICANDO o número.** É o que o M-8 existe para impedir. Todo instrumento
imprime **o caminho de cada biblioteca** e **a porta usada** (broker × `open()`
direto) antes da primeira linha de medição: quem bate no nó escondido mede
`EACCES` e escreve um zero convincente, do mesmo jeito que medir contra a
biblioteca errada produz alarme convincente e falso.

**3. O controle positivo que INDICIA O INSTRUMENTO.** Não é enfeite: é a cláusula
que faz o ensaio poder errar. *"Se mutar pelo caminho provado não move o bit, o
réu é o instrumento e o ensaio NÃO emite veredito"*; *"se a base certa e a base
errada derem as duas plausível, o instrumento não mede o que diz medir"*. Esta
casa já teve **três medições falsas num dia** por não ter parado nesse ponto, e a
cláusula entra no cabeçalho de **todo** instrumento deste plano, não só nos dois
onde ela foi escrita.

**4. As duas réguas de deslocamento são números diferentes.** Entrada: `+1` no
cabo, `+2` no rádio. Saída: o `common` começa em `report[1]` no cabo e `report[3]`
no rádio. E o offset do `btmon` inclui ainda o byte de transação HID-over-BT
(`0xA1` entrada, `0xA2` saída), **um byte antes do report**. Trocá-las produz
número absurdo com cara de medida — é a razão de a tabela da Onda 5 ser a única
soma de offsets do repositório.

**5. LED-SEM-DONO-01 continua aberta.** Enquanto valer, *"o LED está apagado"*
não prova nada, e qualquer aceite de M-6, M-7 ou de qualquer escrita que use LED
de microfone ou de jogador como evidência **nasce inválido**. O detector é a
LIGHTBAR com cor mágica, ou o quadro contado com CRC conferido. Nunca uma lâmpada
sem dono.

**6. Plugar o cabo pode NÃO trocar o transporte.** Um DualSense pareado por
Bluetooth que recebe o cabo pode continuar falando por rádio e só carregar. O
braço se confere no `HID_ID` do uevent (`0003` USB, `0005` BT), **nunca** na
suposição de que *"está plugado, logo é USB"*, e a conferência entra no
relatório, não no comentário. É a mesma armadilha que o P-1 cura dentro do
produto.

**7. O `EVIOCGRAB` do co-op emudece o evdev FÍSICO.** Um leitor externo lê zero
evento e conclui que o aparelho está calado — e isso é o produto funcionando.
Onde a pergunta for de evdev (`toque.touchpad.cursor`, `entrada.botoes`), lê-se
**o vpad**, que é o que o jogo vê.

**8. Casar `hidrawN` → `HID_UNIQ` pelo uevent A CADA CHAMADA, nunca guardado.**
Em 15/08 um controle sumiu e outro reapareceu com `eventN` diferente entre duas
leituras com segundos de diferença. MAC mascarado na convenção da casa — octetos
4 e 5 zerados —, e há portão que reprova.

**9. Apagar entre passos**, em toda escrita de degrau. Sem isso o degrau N herda
o estado do N-1 e a escada inteira sai falso-positiva.

**10. O portão é cego a arquivo novo, e ele morde.** Roda **depois** do `git add`,
sempre. Entre os alvos deste plano, `plataforma.distinguir_clone`,
`luz.lightbar.brilho`, `audio.microfone.volume`, `luz.led_microfone` e
`movimento.imu.ligar` estão com `teste_que_morde` **vazio**: cada par que subir
com `aciona = sim` precisa do teste **antes**. E toda célula que passar a dizer
`SAIU NO FIO` ou `O APARELHO OBEDECEU` precisa de uma linha em
[`docs/data/ensaios.csv`](../../data/ensaios.csv) para aquele `id` **naquele
transporte** (regra 6).

**11. Fato errado se SUBSTITUI; decisão medida ganha data.** O teste que separa os
dois é o da casa: *se apagar isto faria alguém repetir um trabalho ou pagar um
custo já pago?* A seção 3.0 existe inteira por causa desta regra, na direção
menos óbvia: **quatro dos cinco fatos errados que os desenhos propõem substituir
já foram substituídos hoje**, e reescrevê-los seria repetir trabalho pago.

**12. A coluna `cabo x rádio` do `censo_features.py` não vira achado.** Ela diz
DIFERE em 10 de 10 porque o rádio carrega 4 bytes de CRC que o cabo não tem, e
porque compara unidades diferentes em reports que carregam MAC e número de série.
É DIFERE **garantido antes de o instrumento abrir o nó**. Conserte o instrumento
(descontar o trailer, casar por unidade) ou não publique a coluna: DIFERE
garantido dentro de um portão é alarme convincente e falso com validade
permanente.

---

## 8. A DECISÃO QUE SOBRA PARA ELA

Três perguntas, e só três. As outras cinco que o material de origem trazia foram
respondidas pelos fatos ou por ela mesma, e repô-las na mesa seria pedir que ela
decida duas vezes:

- *"o alvo é PAREADO ou `medido/medido`?"* — **ela já respondeu: PAREADO.**
- *"a troca de braços roda hoje?"* — **ela já rodou, às 19h.**
- *"a onda cara pode escrever no rádio, e até onde?"* — **ela já autorizou** os
  degraus `0x33`-`0x38` com o `common` conhecido e a variação do tag entre `0x10`
  e `0x91`, e **manteve o bloqueio** da família `0xF0`-`0xF7`.
- *"trocar o `_detect_transport` pelo `HID_ID`?"* — não é dúvida técnica, é fila.
  Está na Onda 3, com foto.
- *"existe fone de ouvido?"* — vira uma linha do bloco dela: se houver, o A-1b
  roda em 1 minuto; se não, a célula fica aberta **dizendo que está aberta**.

### Decisão 1 — Quanto tempo a mesa fica trocada?

**Não é pergunta retórica: é a única premissa deste plano que eu não consigo
medir.** A Onda 4 inteira depende de os quatro aparelhos continuarem dois em cada
braço. Se eles voltarem ao normal hoje à noite, a Onda 4 tem de subir para logo
depois da Onda 2 e as curas da Onda 3 esperam. Se ficarem trocados por dois dias,
a ordem escrita aqui está certa e a Onda 4 pode ser a última coisa a rodar.

**Preço de deixar trocado:** a mesa dela fica com dois controles no fio por mais
tempo, e o `plataforma.slot_jogador` pode renumerar de novo no meio de um jogo.
**Preço de desmontar hoje:** M-2, M-3, A-1b, M-6 e M-7 perdem a mesa 2+2 e voltam
a medir unidade em vez de transporte — que é exatamente a Lei 4.

### Decisão 2 — A tabela de envelopes sobe para `src/` nesta leva?

**Preço de subir:** 95 minutos que não fecham célula nenhuma e não acendem luz
nenhuma. A defesa é que ela sobe **com consumidor de leitura no dia um** e com o
golden do fio, e que a regra 13 do portão passa a impedir que célula de offset
errada nasça — foi assim que o `report[55]` da bateria viveu meses.

**Preço de não subir:** `EnvelopeDeTransporte` continua em `tests/conftest.py`, a
régua do par continua espalhada por quatro instrumentos (`imu_no_cabo.py:127-130`,
`byte_no_fio.py:140-149`, `taxa_no_hidraw.py:108-116`, `cor_do_plastico.py:186`) e
`comum.py` continua sem nenhuma — e esta casa **já pagou por isso uma vez**,
quando o `identidade_do_vpad.py` nasceu porque três instrumentos respondiam
*"isto é um vpad?"* de três jeitos e um respondia errado.

**Recomendação:** subir, **mas só a tabela de envelopes** — cinco linhas, todas
conferíveis contra o fonte ou contra o fio — e **não** a tabela de campos com
colunas de grau. Se um dia a de campos for proposta, o critério de aborto é
numérico e está escrito: se as linhas que o teste não consegue conferir passarem
de **um terço**, ela não está pronta para ser produto — está sendo documentação
com `import`.

### Decisão 3 — O `BLOCO_SPEAKER` continua declarado sem chamador?

`app/widgets/controller_card.py:714` mostra ao usuário um texto sobre o bloco de
alto-falante. **Eu li o texto e ele fala do volume que o firmware não devolve,
não do bloco `0x13` do protocolo** — o desenho que propôs mexer nele o descreveu
mal, e por isso este plano **não** o toca. Mas a pergunta atrás dele é dela e é
real: enquanto `BLOCO_SPEAKER = 0x13` estiver declarado em `src/` sem um único
chamador desde 25/07, o produto carrega uma promessa que não cumpre.

**Preço de deixar:** mais um dia de *"a casa sabe e o produto não faz"*, na sua
forma visível. **Preço de tirar:** se o E-1 der TLV, o `0x13` volta a fazer
sentido em duas semanas e alguém vai reescrevê-lo do zero.

**Recomendação:** **esperar o E-1**, que custa 25 minutos e nada dela. Se der
`common`, o `BLOCO_SPEAKER` sai no mesmo commit, como número que a medição
derrubou. Se der TLV, ele ganha uma linha de comentário com a data em que a
leitura foi **medida** — e deixa de ser declaração órfã.

---

## 9. A ORDEM LITERAL, e onde a fila para

```
   ONDA 1   o botão morto (A-0)                 40 min   nada dela  -> foto no fim
        |
   ONDA 2   E-1 (25) + E-2 (30)                 55 min   nada dela
        |          <- se o E-1 der `common`, o BLOCO_SPEAKER sai e o M-7 nem roda
        |          <- se der TLV, a coluna `tag` da tabela nasce variável
        |
   ONDA 3   P-1 oráculo + P-2 raw[1] + P-3      90 min   nada dela (a foto é no fim)
        |
   ONDA 4   M-2 (35) + M-8 (20)                 55 min   nada dela
        |
        |  ===================== O BLOCO DELA =====================  49 min
        |    M-3 (10)     3 min de mão
        |    A-1b (5)     1 min de mão      -- cai fora se não houver fone
        |    A-1 (10)     o ouvido          -- ELA FALA PRIMEIRO
        |    M-6 (20)     o olho            -- escreve; depende da palavra dela
        |    M-7 (10)     o olho            -- só se o E-1 não discriminou
        |    a foto do P-1 (5)   o olho
        |  ========================================================
        |
   ONDA 5   a tabela + o golden + a regra 13    95 min   nada dela
```

**Onde a fila para, e o que fazer:**

1. **O controle positivo de um ensaio falha** (o `mic mute` não move o bit; as
   duas bases dão plausível; o `btmon` não vê o `0x31` do daemon): **para aquele
   ensaio**, não a fila. O réu é o instrumento.
2. **A mesa deixa de ser 2+2** (um controle some, `ENODEV`, falhas voltando em
   ~0,01 s): pare o ensaio em curso, rode `quem_e_quem.py` de novo, anote a hora
   de parede — e **não conclua nada sobre o aparelho**, que não está mais lá.
3. **O broker não abre**: param M-2, M-3, A-1b, M-8 e o E-1 juntos. A Onda 1, a
   Onda 3 e a Onda 5 continuam, porque não passam por hidraw. Registre o `motivo`
   literal: ele distingue *broker ausente* de *broker recusando*.
4. **O P-1 muda o comportamento da barra de algum controle**: isso é resultado,
   não falha — significa que aquele controle estava classificado errado. Foto,
   registro, e a palavra é dela.

---

## 10. Antes de fechar a leva

```bash
git add -A                                  # os portões não veem arquivo novo
.venv/bin/python -m pytest -q
.venv/bin/ruff check src/ tests/
python3 scripts/validar-acentuacao.py --all
python3 scripts/validar-glifos.py --all
python3 scripts/validar-referencias-docs.py --all
bash scripts/check_anonymity.sh
.venv/bin/python scripts/check_paridade_transporte.py
.venv/bin/python scripts/gerar-mapa.py      # senão a regra 5 morde toda linha nova
.venv/bin/mypy src/hefesto_dualsense4unix
```

E, se a Onda 1 rodar:

```bash
scripts/gui-captura/retratar_abas.py        # as imagens acompanham a versão
```

---

*Escrito em 15/08/2026, sobre a árvore de `restauro/inicio-da-sessao`. Este
documento não mediu nada e não tocou aparelho nenhum: os números vêm dos brutos
versionados em [`docs/data/ensaios-brutos/`](../../data/ensaios-brutos/), do
[mapa de canais](../../data/mapa-controles.csv) lido com `csv.DictReader` às
19h40, e do fonte C do `hid_playstation`.*
