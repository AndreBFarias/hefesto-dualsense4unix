# O par que faltava — o doente e o são no mesmo rádio

- **Quando:** 15/08/2026, entre 14h31 e 14h45, com o defeito VIVO.
- **O que é inédito:** toda medição anterior desta frente teve só o lado
  doente. Esta teve **doente e são no mesmo transporte, no mesmo host, na mesma
  sessão do daemon, no mesmo instante**. É comparação pareada.
- **Nada foi desligado, nada foi reiniciado.** O daemon rodou o tempo todo. A
  única escrita foi `0 255 0` — o mesmo valor que já estava no sysfs — nos dois
  nós, para pôr a escrita ignorada no ar e fotografá-la.

## O lastro — os seis arquivos, e o que cada um sustenta

Nota datada — 15/08/2026: até esta linha ser escrita, a conclusão estava
versionada e o lastro dela **não**. Todo número deste estudo agora tem endereço.
Cada citação abaixo aponta arquivo e linha, e os arquivos estão mascarados com
a régua da casa (octetos 4 e 5 do MAC zerados) — os `.btsnoop` binários pelo
`scripts/mascarar_btsnoop.py`, que procura o endereço **nas duas ordens de
byte**, porque numa captura HCI ele viaja invertido.

| arquivo | o que sustenta |
|---|---|
| [`…-PAREADO-lightbar-branco-doente-x-vermelho-sao.txt`](../../data/ensaios-brutos/2026-08-15-PAREADO-lightbar-branco-doente-x-vermelho-sao.txt) | o roteiro do ensaio, a procedência declarada e a leitura já sintetizada |
| [`…-PAREADO-sysfs-0019-vermelho-sao.txt`](../../data/ensaios-brutos/2026-08-15-PAREADO-sysfs-0019-vermelho-sao.txt) | os 306 atributos do VERMELHO/SÃO (nó `…0019`, `hidraw8`) |
| [`…-PAREADO-sysfs-001A-branco-doente.txt`](../../data/ensaios-brutos/2026-08-15-PAREADO-sysfs-001A-branco-doente.txt) | os mesmos 306 do BRANCO/DOENTE (nó `…001A`, `hidraw9`) |
| [`…-PAREADO-hci-decodificado.txt`](../../data/ensaios-brutos/2026-08-15-PAREADO-hci-decodificado.txt) | a captura HCI em texto, 15056 linhas — é a forma que este estudo cita por *handle* e por número de pacote |
| [`…-PAREADO-hci.btsnoop`](../../data/ensaios-brutos/2026-08-15-PAREADO-hci.btsnoop) | a mesma captura em binário, 238451 B, **2153 registros** — o original de onde o texto acima foi decodificado |
| [`…-PAREADO-hci-controle-negativo.btsnoop`](../../data/ensaios-brutos/2026-08-15-PAREADO-hci-controle-negativo.btsnoop) | o **controle negativo**: `btmon` SEM root, 16 B, **zero registros** — só o cabeçalho do formato |

O controle negativo é o que separa "captura" de "silêncio": sem root o `btmon`
grava um arquivo válido e VAZIO. Se a captura boa também tivesse 16 bytes, tudo
o que este estudo diz sobre o ar seria leitura de nada.

## A mesa

| papel | MAC (mascarado) | nó HID | hidraw | leds | handle ACL | `hardware_version` |
|---|---|---|---|---|---|---|
| VERMELHO — **são** | `44:46:48:00:00:03` | `0005:054C:0CE6.0019` | `hidraw8` | `input285` | 5 | `0x00000811` |
| BRANCO — **doente** | `14:3a:9a:00:00:ab` | `0005:054C:0CE6.001A` | `hidraw9` | `input288` | 6 | `0x00000711` |

Identificados pelo `HID_UNIQ` do `uevent` cruzado com o `coop_player_added
identity=` do journal (14:17:00), **não pelo LED**. O par MAC→cor vem da tabela
do estudo [A ESCADA QUE RESPONDE](2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md),
conferida com o olho dela naquele ensaio; o firmware não foi perguntado aqui.

## A tabela de diferenças — 306 atributos, três diferenças

Foram lidos **306 atributos de sysfs em cada aparelho** (todo o `leds/`,
`input/`, `hidraw/`, `power/`, `power_supply/` sob o nó HID), normalizados os
números de nó e os MACs, e comparados com `diff`. Os dois dumps estão
versionados inteiros — `…-PAREADO-sysfs-0019-vermelho-sao.txt` e
`…-PAREADO-sysfs-001A-branco-doente.txt`, uma linha `caminho|valor` por
atributo, as 306 começando na linha 38 de cada um (antes vem o cabeçalho de
procedência). Quem quiser refazer o `diff` refaz.

**Diferem — e são só estes três:**

| # | atributo | VERMELHO (são) | BRANCO (doente) | onde |
|---|---|---|---|---|
| a | `power_supply/.../status` | **`Full`** (`power_state` 0x2 = carga completa) | **`Discharging`** (0x0) | linha 327 dos dois dumps |
| b | `hardware_version` | `0x00000811` | `0x00000711` | linha 40 dos dois dumps |
| c | padrão de player-LED | player 3 aceso | players 2 e 4 acesos | linhas 220 a 272, `leds/…:white:player-N/brightness` |

O (c) é a numeração do co-op, não defeito. Sobram **dois**.

> **Correção de fato — 15/08/2026, ao versionar o lastro.** Esta linha dizia
> "player 3" e "player 4". O que os dumps mostram é o `brightness` de cada um
> dos cinco nós: no VERMELHO só o `player-3` está aceso; no BRANCO, o
> `player-2` e o `player-4`. Traduzir esses padrões em "é o jogador N" depende
> da tabela do `hid_playstation`, que não foi conferida neste ensaio — então
> fica o que foi medido. Nada disso muda a conclusão: o (c) segue sendo
> numeração de co-op e não defeito.

**É idêntico — e isto vale tanto quanto o que difere:**

- `report_descriptor`, por `cmp`, byte a byte, 320 B — e o `rdesc` do debugfs.
  Nos dumps versionados ele está na linha 342, transcrito em hexadecimal entre
  `<hex>` e `</hex>` porque o valor é binário e não é texto; ali são 300 B, que
  é o mesmo valor depois de o coletor comer os `0x0a`. O `sha256` do valor é
  **idêntico nos dois arquivos**, e cada cabeçalho o imprime;
- `firmware_version` = `0x0110002a` nos dois (linha 39); `country` (linha 38),
  `modalias`, `HID_ID`, `HID_NAME`, `HID_PHYS`, `DRIVER=playstation` — todos na
  linha 343, a do `uevent`;
- todas as `capabilities` de evdev, e `id/{bustype,product,vendor,version}`;
- **os nós de LED**: `brightness=255`, `multi_intensity=0 255 0`,
  `multi_index`, `trigger=[none]`. O sysfs do doente **aceitou e guarda** o
  verde. A barra está apagada;
- o `info` do BlueZ, campo a campo (menos a chave de enlace e o minuto do
  pareamento): `Class`, `SupportedTechnologies`, `Trusted`, `Blocked`,
  `CablePairing`, `WakeAllowed`, `Services`, `DeviceID`;
- o enlace: `CENTRAL AUTH ENCRYPT` nos dois, mesma *link policy*
  (`RSWITCH HOLD SNIFF PARK`), mesmo *supervision timeout* (20 s), mesmo mapa
  AFH. **Nenhum dos dois está em sniff que o distinga**;
- quem tem o nó aberto: `steam` (610430) e o daemon (615228) — **nos dois**;
- os parâmetros de `hid_playstation`, que são de módulo;
- e o tratamento do daemon: `(0, 255, 0)` para os quatro nós às 14:24:06 e
  14:27:34, `lightbar_reset_sob_demanda enviado=True` para as quatro chaves às
  14:27:33. Simétrico na entrada, assimétrico na saída.

## O achado central: a escrita sai IDÊNTICA no ar

`btmon` passivo durante as duas escritas. Em **2153 registros** de captura há
exatamente **dois** `ACL Data TX` — um por controle — e o pacote é o mesmo:

```
VERMELHO  a2 31 b0 10 00 04 ... 00 ff 00 ... 1e 40 ce 70
BRANCO    a2 31 90 10 00 04 ... 00 ff 00 ... 4c a9 b7 88
```

Endereço de cada um, em `…-PAREADO-hci-decodificado.txt`:

| pacote | linha | o que é |
|---|---|---|
| `#603`, t=2.448113 | 4248 a 4254 | `ACL Data TX: Handle 5` — a escrita no VERMELHO |
| `#606`, t=2.452483 | 4269 a 4272 | `Number of Completed Packets`, Handle 5, Count 1 |
| `#1216`, t=4.449787 | 8536 a 8542 | `ACL Data TX: Handle 6` — a escrita no BRANCO |
| `#1217`, t=4.454506 | 8543 a 8546 | `Number of Completed Packets`, Handle 6, Count 1 |
| `#1218`, t=4.455425 | 8547 | `ACL Data RX: Handle 6` — o doente segue mandando entrada |

"Dois `ACL Data TX` na captura inteira" é contável de fora: `grep -c "ACL Data
TX"` no arquivo devolve 2.

Byte a byte iguais, com duas exceções obrigatórias: `[2] = seq<<4` (0xb0 x
0x90, o contador do driver) e o CRC-32 que é consequência dele. `[3]=0x10` tag,
`[5]=valid_flag1=0x04` (`LIGHTBAR_CONTROL_ENABLE`), RGB `00 ff 00` em
`[48..50]`.

E o doente **confirma a entrega no enlace**: `Number of Completed Packets,
Handle 6, Count 1` (`#1217`, linhas 8543 a 8546), e logo em seguida um `ACL
Data RX` (`#1218`, linha 8547) — ele segue mandando entrada normalmente. A
barra continua apagada.

> **O kernel monta certo, o CRC está certo, o rádio entrega, o aparelho ACK-a.
> O que ignora a cor está DENTRO DO FIRMWARE DO BRANCO.**

## Os candidatos, ranqueados

### 1. O estado de ENERGIA — o são está alimentado, o doente está na bateria

**Por que explicaria a barra ignorar escrita:** a lightbar é o maior consumidor
do aparelho. Um regime de firmware que a mantenha desligada enquanto o aparelho
está só na bateria explica *ignorar a escrita sem recusar o report* — o report é
processado (o enlace confirma, a entrada continua), e o bloco de cor é
descartado por política interna.

**Como explica o vermelho estar são:** ele não está na bateria. Diz
`power_state = 0x2`, carga completa — o que este aparelho reporta quando há
alimentação externa presente. Endereço: linha 327 de
`…-PAREADO-sysfs-0019-vermelho-sao.txt` (`status|Full`) contra a mesma linha 327
de `…-PAREADO-sysfs-001A-branco-doente.txt` (`status|Discharging`).

**O que este candidato explica da HISTÓRIA, e é o que o promove ao primeiro
lugar:**

- *"por cabo sempre funciona"* — por cabo há VBUS. Sempre houve.
- *"persiste até o POWER-OFF FÍSICO"* — a casa nunca separou desligar de
  desplugar. Se a variável é VBUS e não o ciclo de energia, os dois ritos
  curam, e por motivos diferentes.
- *"reconectar cura" foi derrubado quatro vezes desde 17/07* — reconectar não
  muda VBUS. Tinha de falhar, e falhou.
- E casa com a correção **dela**, de 12/08: *"não é só instância de conexão, se
  escavar o projeto vai ver que isso é um falso positivo"*. A instância de
  conexão nunca foi a variável.

**O que o enfraquece, e fica dito:** não está provado que o vermelho tenha um
cabo de energia ligado — o que está medido é que **o firmware dele diz carga
completa**. E `power_state = 0x2` com nível de bateria 9 (não 10) nos dois é
estranho o bastante para merecer o olho dela antes de virar conclusão.

### 2. A revisão de placa — `0x0811` contra `0x0711`

**Por que explicaria:** revisão de placa diferente é firmware/hardware de
lightbar diferente. Esta casa já mediu que coisa de firmware varia por série
neste modelo (o layout do feature `0x22` muda com o `sw_series`).

**Como explica o vermelho estar são:** seria simplesmente uma revisão que não
tem o defeito. Endereço: linha 40 dos dois dumps de sysfs — `0x00000811` no
vermelho, `0x00000711` no branco, com `firmware_version` igual (`0x0110002a`,
linha 39) nos dois.

**O que o enfraquece:** é a explicação que não explica nada mais. Não diz por
que o cabo cura, nem por que o power-off cura, nem por que a mesma barra
obedeceu a `0x31`, `0x32` e `0x39` **neste mesmo branco**, hoje, no ensaio da
escada. Um defeito de revisão de placa não vai e volta.

### 3. Estado de firmware herdado do ensaio da escada (só o branco o recebeu)

O ensaio da escada, mais cedo hoje, mandou `0x31`, `0x32` e `0x39` **só no
branco** — o vermelho, textualmente, *"NÃO foi tentado"*. O `0x39` levou 469
bytes não identificados. É a única assimetria de tratamento conhecida entre os
dois.

**O que o enfraquece muito:** naquele ensaio a barra do branco **obedeceu**, e o
último passo pedido foi *apagar*, com o mesmo `common` de cor — não com
`LIGHT_OUT`. E o defeito é anterior a hoje: o mapa já o descrevia como o que
acontece *na adoção*, semanas antes de existir escada. Fica registrado por ser
assimétrico, não por ser provável.

## O que JÁ POSSO DESCARTAR, com medição

- **A rota de escrita, o CRC, o tamanho, o `seq`** — o pacote sai idêntico e é
  confirmado no enlace.
- **A supressão do produto, a disputa de hidraw, a Steam** — os mesmos dois
  processos têm os dois nós abertos, e um obedece.
- **Transporte, papel de enlace, sniff, política de enlace, *supervision
  timeout*, mapa AFH, RSSI** — idênticos ou irrelevantes.
- **O BlueZ** — o `info` é o mesmo campo a campo.
- **O descritor HID** — `cmp` byte a byte; e o `sha256` do valor transcrito
  (linha 342 dos dois dumps) bate.
- **O driver e seus parâmetros** — são de módulo, valem para os dois.
- **O daemon** — mandou o mesmo para os quatro nós, nos mesmos segundos.
- **O ensaio `E7`** — rodada seca no rádio; nada foi ao fio. O `.btsnoop` é a
  prova: dois `ACL Data TX` na captura inteira, os dois do ensaio pareado.
- **`DualSense input CRC's check failed`** — acontece nos dois, e **mais** no
  são. É ruído de rádio.

## O ensaio que separa o candidato 1 do candidato 2

**Tirar a alimentação do VERMELHO.** Se ele começar a ignorar a cor sem ter sido
desligado nem reconectado, o candidato 1 está isolado e o 2 cai.

- **Não destrói evidência nenhuma.** Não desliga controle, não reconecta, não
  reinicia unit. É reversível: religar a alimentação devolve o estado.
- **Converte o controle são no doente** — que é a forma mais forte de prova que
  esta mesa pode dar, e a que nunca esteve disponível antes.
- **Antes de mexer, conferir com o olho dela:** o vermelho tem cabo de energia
  ligado? Se a resposta for *não*, o candidato 1 cai por si, sem ensaio, e a
  frente vira firmware/revisão de placa.
- **O complemento, se houver cabo só de carga (sem dados):** ligá-lo no BRANCO.
  Se a barra voltar a obedecer **sem sair do rádio**, o candidato 1 fica provado
  nos dois sentidos. Cabo COM dados não serve: ele troca o transporte e
  confunde a medição.

## Se a comparação não tivesse achado nada

Fica dito, porque quase foi esse o resultado: **306 de 306 atributos iguais,
menos dois**. Não há diferença de software, de pilha, de enlace, de descritor,
de driver ou de disputa que separe estes dois aparelhos. Se as duas diferenças
que sobraram caírem, a frente **muda para o firmware**, e a comparação pareada
terá sido o que fechou todas as outras portas.
