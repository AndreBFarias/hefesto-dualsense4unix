# BUSCA-QUE-ESTOURA-01 — o SDP que não responde a tempo

- **Achado em:** 07/08/2026, às 20h30, medindo a máquina dela com os quatro
  controles na mesa. **Leitura pura**: nenhum serviço reiniciado, nenhum bond
  tocado, nenhum controle derrubado
- **Estado:** **CAUSA ISOLADA E MEDIDA, NÃO CURADA.** Esta sprint desenha a
  cura e **não a implementa** — a escolha entre os desenhos é dela
- **Gravidade:** **ALTA** — é o que ela vê como *"conecta e desliga em
  sequência"*, e o ciclo suja o rádio dos outros três controles
- **Causa-raiz:** **MEDIDA** na cadeia inteira, com três fontes independentes
  que fecham no mesmo relógio (journal, retratos de bond, disco)
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Nasce de:**
  [CONECTA-E-DESLIGA-01](2026-08-07-CONECTA-E-DESLIGA-01-a-regressao-que-ela-relatou-e-a-suspeita-que-recai-sobre-nos.md)
  — aquela sprint registrou o **sintoma** e três hipóteses. **As três caíram.**
  Esta aqui é a causa
- **Ressuscita:**
  [BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md)
  — dada como não aplicável às 20h30 de 07/08, **e ela se aplica inteira**. O
  motivo do engano é o achado de método desta sprint
- **Parentes:**
  [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
  (dona do `JustWorksRepairing=confirm`),
  [BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md)
  (dona dos retratos de bond que serviram de prova aqui),
  [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
  (o parente direto do defeito de diagnóstico do fim desta página)

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, retrato ou arquivo que sustenta; **SUSPEITA COM MECANISMO** = o
caminho fecha e o efeito não foi observado nesta bancada; **SEM PROVA** = está
dito e ninguém verificou aqui.

Endereços de rádio aparecem na máscara da casa (octetos 4 e 5 zerados).

---

## O resumo, em cinco linhas

**Grau: MEDIDO.**

1. O 8BitDo perdeu o pareamento por volta das 19h50 e **re-pareou sozinho**,
   sem cabo, entre 19h52 e 20h07.
2. O pareamento novo **nasceu sem serviços**: `info` sem `Services=`, sem
   `[DeviceID]`, e `cache/<endereço>` com **35 bytes** — só o nome.
3. Sem perfil HID registrado, o BlueZ recusa a reconexão entrante do aparelho
   como `unknown device`. É o laço que ela vê.
4. A busca de serviços que consertaria isso sozinha **estourou por tempo, duas
   vezes**, com **42 segundos** cada — o aparelho não respondeu.
5. O clique dela na tela de Bluetooth, às **20:21:10**, completou a busca na
   primeira tentativa e escreveu os 1485 bytes que faltavam. **Zero linha de
   erro no journal nessa janela.**

---

## A linha do tempo — três fontes independentes, o mesmo relógio

**Grau: MEDIDO.** As três fontes são: o journal do `bluetooth.service`; os
retratos de bond que o `scripts/bt_bonds_snapshot.sh` grava sozinho a cada
mudança; e os arquivos vivos em disco.

| horário | fonte | o que diz |
|---|---|---|
| 19:22:19 | retrato | 8BitDo **sadio**: `info` com HID `0x1124`, `[DeviceID]`, cache de **1485 b** com `[ServiceRecords]` |
| 19:48:21 | journal | `confirm_event_cb() Refusing connection from E4:17:D8:00:00:83: unknown device` |
| 19:49:03 | journal | `search_cb() ...: error updating services: Connection timed out (110)` |
| 19:49:22 | journal | o `scripts/bt_health_watchdog.sh` aplica `Trusted=true` no 8BitDo — **logo ele estava sem trust** |
| 19:52:22 | retrato | o 8BitDo **sumiu inteiro**: sem `info`, sem cache. Restam três controles |
| entre 19:52 e 20:07 | inferido | **re-pareamento**, sem cabo (`CablePairing=false`), `[LinkKey]` nova |
| 20:00:18 | journal | `Refusing connection ...: unknown device` (de novo) |
| 20:01:00 | journal | `error updating services: Connection timed out (110)` (de novo) |
| 20:07:23 | retrato | 8BitDo de volta e **doente**: `info` **sem** `Services=`, **sem** `[DeviceID]`; cache de **35 bytes**, **sem** `[ServiceRecords]` |
| 20:21:10 | retrato + disco | 8BitDo **curado**: cache de **1485 b** com `[ServiceRecords]`, `info` com HID e `[DeviceID]`. **Nenhuma linha no journal entre 20:20:40 e 20:21:40** |

O conteúdo integral do cache de 35 bytes, no retrato das 20:07:23:

```
[General]
Name=Wireless Controller
```

São **os mesmos 35 bytes** que a BT-SDP-VAZIO-01 mediu em 02/08 e nomeou como
a assinatura do defeito. A doença é a mesma, e voltou.

### O paralelo do DualSense roxo, no mesmo dia

**Grau: MEDIDO.** O roxo passou pelo mesmo ciclo mais cedo, e **saiu dele
sozinho** — o que dá o contraste que faltava:

```
19:06:56  Refusing connection from A0:FA:9C:00:00:F0: unknown device
19:07:02  error updating services: Host is down (112)
19:07:08  error updating services: Host is down (112)   (e nova recusa)
19:07:14  error updating services: Host is down (112)
19:07:16  cache escrito, 1433 bytes, com [ServiceRecords]
19:07:18  info escrito, com Services= e [DeviceID]
```

Vinte segundos, três falhas, e a quarta tentativa pegou. **Sem clique.**
O 8BitDo, com o mesmo laço, levou **33 minutos e um clique**.

---

## A ARMADILHA DE MÉTODO — eu li o cache DEPOIS da cura

**Grau: MEDIDO, e é o achado que mais vale desta sprint.**

Às 20h30 eu li os quatro caches com root, vi `[ServiceRecords]` nos quatro, e
concluí: *"a hipótese BT-SDP-VAZIO-01 caiu"*. **A conclusão estava errada, e o
instrumento estava certo.** O cache do 8BitDo tinha sido reescrito às
**20:21:10** — nove minutos antes de eu olhar, pelo clique dela.

Eu medi o paciente depois do remédio e assinei que ele nunca esteve doente.

> **A forma geral:** num defeito que **se cura ao ser tocado**, toda medição
> feita depois do toque mede a cura, não a doença. O carimbo de tempo do
> arquivo não é acessório — **é a medição**. Ler `mtime` antes de ler conteúdo
> teria evitado o engano inteiro.

É prima da lição de 01/08 (*"medir contra a biblioteca errada produz alarme
convincente e falso"*) e da refutação da PARIDADE-SONY-01 (*"o instrumento
estava certo e respondia a pergunta errada"*). A diferença é o eixo: ali o
erro era **de referência**, aqui é **de tempo**.

**O que salvou:** os retratos de bond da
[BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md).
Eles existem para **restaurar**, e nesta sprint serviram para **datar** —
foram eles que provaram o estado doente das 20:07:23, que o disco de hoje já
não tem como mostrar. Um salva-vidas virou máquina do tempo.

---

## POR QUE A BUSCA ESTOURA — dois modos, dois relógios

**Grau: MEDIDO nos dois relógios; SUSPEITA COM MECANISMO no motivo do
aparelho se calar.**

As cinco falhas de hoje não são todas iguais. Elas se separam pelo `errno` **e
pelo tempo até falhar**, e cada par conta uma história diferente:

| erro | quantas hoje | tempo até falhar | o que isso significa |
|---|---|---|---|
| `Host is down (112)` | 3 (roxo) | **6 s** | não houve enlace nenhum: o adaptador **paginou** o controle e ele não atendeu |
| `Connection timed out (110)` | 2 (8BitDo) | **42 s** | o enlace existia; o controle **não respondeu** ao pedido de canal SDP |

Os dois relógios estão **medidos na máquina dela**, e nenhum dos dois é chute:

- **6 segundos** casa com o *page timeout* do adaptador. Lido do próprio
  adaptador: `Page timeout: 8192 slots (5120.00 ms)`. Cinco segundos e um
  pouco de contabilidade é o que se vê no journal.
- **42 segundos** casa com o tempo de espera de conexão do L2CAP no núcleo.
  Lido dos cabeçalhos do núcleo instalado nesta máquina
  (`include/net/bluetooth/l2cap.h`, linha 55):
  `#define L2CAP_CONN_TIMEOUT msecs_to_jiffies(40000)`.
  Quarenta segundos de silêncio, mais a contabilidade, é **exatamente** o
  intervalo medido — e ele se repetiu **idêntico** nas duas ocorrências
  (19:48:21 para 19:49:03; 20:00:18 para 20:01:00).

**Logo:** no caso do 8BitDo, a busca não foi "lenta". Ela foi **muda**. O
adaptador pediu um canal SDP ao controle e passou quarenta segundos sem
resposta nenhuma, com o enlace de rádio de pé.

### O que isso diz sobre de quem é a culpa

**Grau: MEDIDO onde diz "host"; SUSPEITA COM MECANISMO onde diz "aparelho".**

| peça | de quem é | valor nesta máquina | dá para configurar? |
|---|---|---|---|
| *page timeout* | host (adaptador) | 5120 ms | **sim**, por comando HCI — mas aumentar só faz **cada** falha demorar mais |
| espera do L2CAP | host (núcleo) | 40000 ms | **não**. É constante compilada; não há botão em `/sys/kernel/debug/bluetooth` nem em `sysctl` — **conferido, não há** |
| se a busca acontece | host (BlueZ) | padrão | `ReverseServiceDiscovery` no `main.conf`. **Não está escrita no arquivo dela** — vale o padrão |
| tempo de espera de SDP | BlueZ | não existe | **não há** chave de tempo de SDP no `main.conf` dela — conferido |
| **responder ao SDP** | **o controle** | — | **nenhum botão nosso alcança isso** |

**A conclusão honesta:** o único relógio que dá para mexer é o do *page
timeout*, e mexer nele **piora** — alonga cada falha sem tornar nenhuma
resposta mais provável. Os quarenta segundos são do núcleo e não têm botão.
E o que de fato falhou — o controle responder — **não é nosso**.

**Por que o 8BitDo se cala** (grau: **SUSPEITA COM MECANISMO**, herdada da
BT-SDP-VAZIO-01 e não fechada lá nem aqui): ele economiza rádio de forma
agressiva. Terminada a própria tentativa de conexão — e recusado — ele deixa
de atender. O roxo, que é um DualSense, atendeu na quarta tentativa em vinte
segundos. **Não foi medido com analisador de rádio**, e sem isso continua
sendo mecanismo plausível, não fato.

### O histórico diz que isto não nasceu hoje

**Grau: MEDIDO.** Sete dias de journal, contando `error updating services`:

| dia | `Host is down (112)` | `Connection timed out (110)` | outros |
|---|---|---|---|
| 01/08 | 17 | — | — |
| 02/08 | 17 | 1 | — |
| 03/08 | — | 1 | — |
| 04/08 | 2 | 1 | 1 (`Input/output error`) |
| 05/08 | — | — | — |
| 06/08 | — | — | — |
| 07/08 | 3 | 2 | — |

Dois dias limpos (05 e 06/08) e a volta em 07/08. **A palavra "regressão" dela
tem base**: o defeito é intermitente e voltou depois de dois dias quietos.
O que **não** se sustenta é atribuir a volta a uma mudança de configuração
nossa — 01 e 02/08 têm dezessete ocorrências por dia, **antes** de qualquer
uma das curas suspeitas.

---

## O QUE O CLIQUE FAZ DE DIFERENTE

Esta é a pergunta que decide a cura: **o que o clique dela faz que a
reconexão automática não faz?** Se soubermos, sabemos o que o produto tem de
fazer sozinho.

### O que está MEDIDO sobre o clique

**Grau: MEDIDO.**

- Às **20:21:10** o cache e o `info` foram escritos, com o conteúdo completo
  (1485 b, `[ServiceRecords]`, `Services=`, `[DeviceID]`).
- **Não há uma única linha de `bluetoothd` no journal entre 20:20:40 e
  20:21:40.** Nem recusa, nem tempo esgotado, nem aviso. A busca completou **na
  primeira tentativa**.
- Antes disso, nas 33 minutos anteriores, o caminho automático falhou duas
  vezes com quarenta segundos de silêncio cada.

**O contraste é total**: mesmo controle, mesmo rádio, mesmos minutos. O
caminho automático não conseguiu nem uma resposta; o caminho do clique
conseguiu tudo de primeira.

### As três explicações possíveis, e como distinguir

**Grau: SUSPEITA COM MECANISMO nas três. Nenhuma foi medida — e medir exige
ela clicando.**

**(A) O clique chama `org.bluez.Device1.Connect()` — e quem paga o enlace é o
host.** Na reconexão automática, quem abre o enlace é o controle; o host
responde com uma busca de serviços **de volta** para um aparelho que acabou de
ser recusado e já está indo dormir. Com `Connect()`, é o host que **chama** o
controle, o host que **segura** o enlace, e a busca corre sobre uma linha que o
host controla do começo ao fim.

**(B) Abrir a tela de Bluetooth já basta, porque ela liga a busca de
aparelhos.** Isto está registrado e medido na casa: o `scripts/doctor.sh` já
avisa que *"a tela de Bluetooth do cosmic-settings aberta mantém
`Discovering=yes`"*. Um resultado de busca traz a lista de serviços anunciada
pelo próprio aparelho — o suficiente, em tese, para o BlueZ registrar o perfil
HID **sem SDP nenhum** e parar de recusar. **Contra esta explicação**: os 1485
bytes de registros SDP no cache **exigem** uma busca SDP completa; anúncio de
aparelho não os escreveria. Se (B) age, age **antes** de (A), destravando o
caminho para que a busca finalmente ocorra.

**(C) Coincidência.** O controle estava acordado naquele segundo. Trinta e
três minutos de tentativas fracassadas tornam isso pouco provável, mas **uma
amostra é uma amostra**.

O que se sabe dos binários da tela dela, e é pouco: `/usr/bin/cosmic-settings`
fala `org.bluez.Device1` e `org.bluez.Adapter1`, e tem `RemoveDevice`,
`StartDiscovery` e `StopDiscovery` como literais. **O nome do método do botão
Conectar não sai por leitura de binário** — os nomes de método ficam colados
num bloco único. Grau desta linha: **MEDIDO** no que aparece, **SEM PROVA**
sobre qual método o botão dispara.

### O protocolo que decide, e custa dois minutos dela

**Não execute sem ela.** É leitura pura, mas depende de um gesto dela.

**P0.** Com o 8BitDo no laço (recusa no journal), deixar rodando em duas
janelas:

```
journalctl -u bluetooth -f
sudo dbus-monitor --system "type='method_call',interface='org.bluez.Device1'" "type='method_call',interface='org.bluez.Adapter1'"
```

**P1 — o gesto.** Ela **abre** a tela de Bluetooth e **não clica em nada**.
Esperar trinta segundos.

- Se o laço parar **só de abrir**, a explicação é **(B)** — e a cura do produto
  é registrar o perfil sem depender de SDP.
- Se não parar, seguir.

**P2 — o clique.** Ela clica em Conectar.

- `dbus-monitor` mostra **qual** método sai. Se for `Device1.Connect`, a
  explicação é **(A)** — e a cura do produto é chamar esse método sozinho.

**P3 — repetir três vezes.** Uma amostra não separa (A)/(B) de (C).

**PREVISÃO REGISTRADA, para poder errar por escrito:** eu aposto em **(A)**,
com **(B)** como destravador. Motivo: os 1485 bytes só podem vir de uma busca
SDP completa, e a única diferença que explica uma busca completar **de
primeira** depois de duas falharem por silêncio de quarenta segundos é **quem
está segurando o enlace**.

---

## A CURA POSSÍVEL — cinco desenhos, nenhum implementado

O gatilho é sempre o mesmo par no journal, e ele é **específico**: `unknown
device` seguido, dentro de um minuto, de `error updating services`. Hoje esse
par apareceu quatro vezes e **nunca** apareceu sem o defeito estar presente.

| # | desenho | custo | risco | grau |
|---|---|---|---|---|
| **A** | **Empurrão do host.** Ao ver o par, chamar `Device1.Connect()` no aparelho, uma vez, com espera crescente e teto de tentativas | baixo: um método D-Bus, sem privilégio de root | **médio.** Se (A) não for a explicação, gasta rádio à toa **no meio do ciclo** — que é quando o rádio está pior. Precisa de teto e de silêncio depois | SUSPEITA COM MECANISMO |
| **B** | **Só avisar.** Aviso na tela dela: *"o 8BitDo está entrando em laço; abra a tela de Bluetooth e clique em Conectar"* | muito baixo | **muito baixo.** É o único desenho que não toca no rádio. **Não cura** — devolve o trabalho para ela | MEDIDO que funciona: é o que ela já faz |
| **C** | **Re-parear sozinho** (`RemoveDevice` + apagar o cache + parear) — a cura da BT-SDP-VAZIO-01, automatizada | alto: exige root e o gesto de pareamento do controle | **ALTO, e eu recomendo NÃO.** Destrói o bond por decisão de máquina. Se o diagnóstico errar, ela perde um controle que estava só dormindo. A BT-SDP-VAZIO-01 exigiu autorização dela para fazer isso **uma** vez | MEDIDO que cura; MEDIDO que é destrutivo |
| **D** | **Retrato que se recusa a fotografar defeito.** O `scripts/bt_bonds_snapshot.sh` guardar bond **sem** serviços é guardar o que não presta para restaurar | baixo: uma condição antes de gravar | **baixo**, com uma ressalva séria: um retrato **ruim** ainda é melhor que **nenhum**. Tem de marcar como suspeito, nunca descartar | **MEDIDO que o buraco existe**: o retrato das 20:07:23 guardou o estado quebrado. A BT-SDP-VAZIO-01 previu isso em 02/08 e voltou a acontecer |
| **E** | **Mexer no rádio** (baixar `FastConnectable`, alongar o *page timeout*) | baixo de escrever | **ALTO, e eu recomendo NÃO.** `FastConnectable` existe por um motivo medido (o botão PS reconectar rápido) e alongar o *page timeout* só faz cada falha demorar mais | SEM PROVA de que ajude |

**A ordem que eu proporia, e a decisão é dela:** **B** primeiro, porque é o
único de risco quase nulo e transforma um mistério em instrução; **D** junto,
porque é higiene do salva-vidas e não toca no rádio; **A** só **depois** de o
protocolo acima dizer que (A) é a explicação. **C** nunca por decisão de
máquina.

### O que isto tem a ver com o rádio sujo

**Grau: SUSPEITA COM MECANISMO.**

A CONECTA-E-DESLIGA-01 mediu a perda de pacotes do Pro subir de 14,6 para
48,4 por minuto (3,3 vezes) durante o ciclo. As duas coisas se
retroalimentam: o ciclo suja o rádio, e o rádio sujo torna a resposta do
controle mais improvável.

Há uma peça nossa nesse laço, e é honesto registrar: `FastConnectable=true`,
que **nós** instalamos, está no `/etc/bluetooth/main.conf` dela — e o
comentário que **nós mesmos** escrevemos ali o descreve como *"page scan
agressivo"*. Um adaptador que varre mais tempo à procura de quem chama é um
adaptador que passa menos tempo servindo quem já está conectado. **Quanto**
disso custa às perdas do Pro **não foi medido**, e sem medir isso é mecanismo,
não fato. Não é motivo para desligar a chave — é motivo para não fingir que
ela não está ali.

**E uma porta que fica fechada, para o próximo não perder tempo:** o
`main.conf` dela tem **dois** cabeçalhos `[General]` (o da distribuição e o do
nosso bloco). Isso **não** é defeito: **MEDIDO** que o leitor de configuração
funde grupos repetidos — carregado o arquivo, `FastConnectable=true` e
`JustWorksRepairing=confirm` são lidos normalmente.

---

## O DEFEITO DE DIAGNÓSTICO — o check que se cala e não diz que está cego

**Grau: MEDIDO. Vale muito além deste caso, e por isso está registrado como
achado próprio.**

O `scripts/doctor.sh` tem um check para exatamente esta família,
`check_bt_sdp_cache_envenenado`, escrito em 23/07 e com a cura na mensagem.
Sem senha de root, ele faz isto (`scripts/doctor.sh`, linhas 2282 a 2285):

```bash
if ! sudo -n true 2>/dev/null; then
    info "sem sudo sem senha — não leio o cache SDP (...)"
    return
fi
```

**Ele sai por `info`.** E `info`, na saída do doctor, lê-se como *"nada a
relatar"*. Não é: é *"não olhei"*. São **duas** coisas diferentes e o
instrumento as imprime iguais. O mesmo padrão está na linha 2247, no check que
lê `/var/lib/bluetooth`.

> **A forma geral:** um instrumento que não pode olhar tem de gritar que não
> pode. Um `[INFO]` no meio de trinta linhas verdes é indistinguível de
> silêncio saudável — e quem lê sai com **mais** confiança do que entrou. Não
> basta um terceiro texto: precisa de um terceiro **estado**, que conte no
> resumo final e **impeça o selo verde**.

É a mesma doença da
[SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
— afirmar mais do que se mediu — vista pelo outro lado: ali o instrumento
afirmava demais; aqui ele **cala** e o silêncio é lido como afirmação.

### E há uma cegueira pior, que esta sprint mediu de novo

**Grau: MEDIDO.** Mesmo **com** root, o check antigo **não** teria visto o
8BitDo às 20:07. Rodei o filtro de elegibilidade dele contra o retrato das
20:07:23 — o retrato do estado doente, congelado:

| controle | o filtro `Services=...0x1124` diz | o cache estava |
|---|---|---|
| DualSense 14:3A:9A:00:00:AB | elegível | com `[ServiceRecords]` |
| DualSense A0:FA:9C:00:00:F0 | elegível | com `[ServiceRecords]` |
| Pro E0:F6:B5:00:00:53 | elegível | com `[ServiceRecords]` |
| **8BitDo E4:17:D8:00:00:83** | **DESCARTADO pelo filtro** | **SEM `[ServiceRecords]`** |

O único doente é justamente o único que o filtro joga fora — porque o filtro
pede `Services=` no `info`, e um bond que nasceu sem serviços **não tem**
`Services=`. O check teria impresso, com root e tudo:

```
[ OK ] cache SDP íntegro em todos os controles com bond (todos têm [ServiceRecords])
```

**É a mesma cegueira que a BT-SDP-VAZIO-01 nomeou em 02/08** — *"um check que
primeiro filtra 'só devices sadios o bastante para me interessarem' fica cego
na proporção da gravidade"* — e agora ela tem uma **segunda** medição, cinco
dias depois, com um retrato datado por prova. A lição não foi só descrita:
**foi reproduzida.**

**O que salva o dia:** o check NOVO que a BT-SDP-VAZIO-01 entregou junto (o
que pergunta ao D-Bus, em `check_bt_radio`, e reprova `Paired` sem `0x1124`
nos `UUIDs`) **teria** apontado o 8BitDo às 20:07. Ele existe, tem mordida
conferida em `tests/unit/test_doctor_bond_sem_servicos.py`, e estava certo.

**O que sobra em aberto, e é o buraco de verdade:** **ninguém rodou o doctor
entre 19h50 e 20h21.** O check certo existia, funcionava, e ficou parado
enquanto ela clicava. Um diagnóstico que só fala quando alguém pergunta não
serve para um defeito que dura trinta minutos e some ao ser tocado. **O
gatilho é o que falta, não o check.**

### Uma armadilha para quem for escrever o gatilho

**Grau: MEDIDO.** Lendo o D-Bus agora, os quatro controles têm o perfil HID
nos `UUIDs`, e **o Pro está com `ServicesResolved=false` conectado e
funcionando**. Ou seja: **`ServicesResolved` não serve de critério.** Quem
escrever o aviso tem de olhar os `UUIDs`, como o check novo faz, e não o
`ServicesResolved`, que reprova um controle são.

---

## O que esta sprint NÃO fecha

1. **Qual dos três caminhos o clique dispara.** O protocolo acima decide, e
   custa dois minutos dela. Até lá, a cura **A** não deve ser escrita.
2. **Por que o bond do 8BitDo sumiu entre 19:49 e 19:52.** Não há linha de
   journal para isso. Pode ter sido ela (esquecer e parear de novo na tela),
   pode ter sido o próprio BlueZ descartando um device temporário. **Sem
   prova.** É a peça que falta para a cadeia ficar completa de ponta a ponta.
3. **Por que o 8BitDo se cala por quarenta segundos.** Mecanismo plausível,
   sem medição de rádio.
4. **Quanto o `FastConnectable` custa nas perdas do Pro.** Mecanismo, sem
   número.

---

## O que NÃO fazer

- **Não medir o cache SDP sem olhar o `mtime` primeiro.** É o erro desta
  sprint, e ele quase enterrou a causa certa.
- **Não desparear por decisão de máquina.** A cura **C** funciona e é
  destrutiva; ela exige autorização dela, caso a caso.
- **Não mexer nos relógios.** O do L2CAP não tem botão, e alongar o *page
  timeout* piora.
- **Não desligar a vigia de trust do `scripts/bt_health_watchdog.sh`.** Hoje
  ela agiu certo, às 19:49:22, e não é ela que está errada.
- **Não concluir "conectou, logo curou"** sem olhar os `UUIDs`. O rádio subir
  não é o perfil subir — e foi essa confusão que fez o defeito parecer três
  defeitos em 02/08.
