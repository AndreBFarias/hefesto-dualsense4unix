# PLANO DA MESA 2+2 — o que só se mede com quatro

- **Escrito em:** 15/08/2026, manhã, na branch `restauro/inicio-da-sessao`, sobre
  `ce03f6e`.
- **Grau:** **PLANO.** Nenhum ensaio deste documento foi executado. O que aqui
  aparece como **MEDIDO** foi lido do sysfs desta máquina durante o desenho —
  leitura pura, nenhum byte enviado a aparelho nenhum, e cada linha diz de onde
  veio.
- **Por que existe:** a mesa de agora — **dois DualSense no cabo e dois no
  rádio, ao mesmo tempo, no mesmo host, com o mesmo firmware** — é o instrumento
  que separa *"o aparelho não faz"* de *"o transporte não leva"*. É desenho
  dela, de 15/08 às 04:20: *"vamos conectar dois controles por cabo e 2 sem
  cabo, vamos usar isso pra irmos isolando o canal exato do cabo e o canal exato
  via rádio"*.
- **A janela:** a mesa fica de pé por cerca de seis horas **sem ninguém para
  remontá-la**. Isso governa o plano inteiro: nada aqui pode derrubá-la, e nada
  aqui pode pedir a mão dela.
- **Irmãos deste documento:**
  [ESCADA-QUE-RESPONDE-01](../sprints/2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
  (os ensaios de **escrita**, que aqui vão para o bloco dela),
  [A-PORTA-QUE-A-CASA-CONSTRUIU-01](../sprints/2026-08-15-A-PORTA-QUE-A-CASA-CONSTRUIU-01-os-instrumentos-batem-na-porta-errada.md)
  (a porta que todo ensaio deste plano usa) e
  [`scripts/ensaios/README.md`](../../../scripts/ensaios/README.md) (os quatro
  instrumentos que já existem).

---

## 0. A mesa de agora, lida — e não suposta

Tudo nesta seção saiu de `/sys` e do `uevent` em 15/08/2026, por volta das 06h40,
com o daemon **vivo**. Nenhuma escrita.

### 0.1 Quem é quem

| nó | `HID_ID` | transporte | quem é |
|---|---|---|---|
| `/dev/hidraw4` | `0003:054C:0CE6` | **cabo** (USB) | DualSense físico, porta `usb3/3-2` |
| `/dev/hidraw5` | `0003:054C:0CE6` | **cabo** (USB) | DualSense físico, porta `usb3/3-3` |
| `/dev/hidraw9` | `0005:054C:0CE6` | **rádio** (BT) | DualSense físico |
| `/dev/hidraw11` | `0005:054C:0CE6` | **rádio** (BT) | DualSense físico |
| `/dev/hidraw6` | `0003:054C:0DF2` | — | vpad do Hefesto (`HID_PHYS=hefesto-vpad`) |
| `/dev/hidraw7` | `0003:054C:0DF2` | — | vpad do Hefesto |
| `/dev/hidraw10` | `0003:054C:0DF2` | — | vpad do Hefesto |
| `/dev/hidraw12` | `0003:054C:0DF2` | — | vpad do Hefesto |

Os **quatro físicos** estão `crw------- root root`. Os **quatro vpads** estão
`crw-rw----+`, com ACL. **Não é defeito**: é o `hide` do broker escondendo o
físico do Steam Input, e está registrado em A-PORTA-QUE-A-CASA-CONSTRUIU-01.

O vpad forja `BUS_USB` de propósito — ler o barramento e chamá-lo de "cabo"
falseia toda tabela deste plano. A régua é `HID_PHYS=hefesto-vpad`, **nunca** o
VID/PID.

### 0.2 A topologia do fio — e ela é o achado gratuito deste desenho

```
  pci 0000:0c:00.3  (xHCI)  ->  usb3
        |
        +-- 3-2 : DualSense CABO      480M   (hidraw4 + placa ALSA)
        +-- 3-3 : DualSense CABO      480M   (hidraw5 + placa ALSA)
        +-- 3-4 : adaptador btusb      12M   (hci0 -> hidraw9, hidraw11)
```

**Os dois controles do cabo e o adaptador de rádio dividem o mesmo controlador
USB.** É exatamente a pré-condição física que a linha
`combinacao.adaptador_no_mesmo_controlador@dualsense` do mapa levantou como
suspeita, a partir do defeito medido em 10/08 — *"um controle NO CABO matava a
saída do controle NO BT"*.

**Isto é topologia, não é dano.** Que dividam o controlador não prova que um
atrapalhe o outro; é o ENSAIO 6 que mede o dano, por dose-resposta.

### 0.3 O áudio, lido de `/proc/asound/cards`

Duas placas `USB-Audio DualSense Wireless Controller` — as **dos dois do cabo**.
Nenhuma dos dois do rádio. Confere com o que a canônica já registra, e agora com
os dois braços na mesa ao mesmo tempo.

Os dois do cabo têm nó `Headset Jack` no evdev; os dois do rádio, não.

---

## 1. As quatro leis deste plano

Cada uma nasceu de uma restrição real desta janela, e nenhuma é negociável.

### Lei 1 — o daemon fica vivo, então a porta é o broker

Parar o daemon derruba os quatro vpads e o co-op. **Está proibido nesta janela.**
Isso tem uma consequência dura: `censo_features.py` e qualquer leitura de hidraw
físico **não podem** usar a receita do README (`systemctl --user stop …`).

A porta é o socket que a casa já construiu, e o cliente já existe:

```python
from hefesto_dualsense4unix.integrations.hidraw_broker_client import HidrawBrokerClient

cliente = HidrawBrokerClient()
fd, motivo = cliente.abrir_no("/dev/hidraw9")   # (fd O_RDWR, "broker") ou (None, razão)
```

Três coisas medidas no fonte do broker, e as três são o que torna isto seguro
(`src/hefesto_dualsense4unix/broker/hidraw_broker.py`):

1. **`open` é ortogonal ao `hide`.** Ele *"NÃO altera lease/refcount"* e funciona
   nos dois estados. Um instrumento que só abre não muda estado nenhum.
2. **A conexão é a lease, e a lease só governa o que ela mesma escondeu.** Um
   cliente novo que nunca chamou `hide` não segura nada, e desconectar não
   restaura nada.
3. **`restore` num nó que outra lease viva segura devolve `hidden` sem tocar no
   sistema de arquivos.** O daemon segura os quatro.

**Regra do instrumento, e ela é absoluta:** só `ping`, `status` e `open`.
**Nunca** `hide`, `restore` ou `restore_all` — um `restore_all` de um instrumento
não desfaz o hide do daemon, mas a regra existe para que ninguém precise ter
lido este parágrafo para estar seguro.

**Cada relatório declara a porta usada**, ao lado da biblioteca. Medir no nó
escondido produz zero convincente e falso, do mesmo jeito que medir contra a
biblioteca errada produz alarme convincente e falso.

### Lei 2 — nenhum ensaio pede cronômetro a mão humana

É a armadilha `A-8`/`A-9`/`A-21` desta casa, e ela já custou duas rodadas em
11/08. Ela não está aqui, e não estará por seis horas.

**O que salva o plano inteiro:** o DualSense **transmite relatório de entrada em
intervalo fixo, parado na mesa**. Não é preciso apertar nada, mexer em nada, nem
olhar para nada — a máquina conta. Todo ensaio do bloco de leitura se apoia
nisso, e por isso nenhum deles precisa dela.

Onde a resposta dependeria do olho dela — a lightbar obedecendo, o som saindo —
o ensaio vai para o **bloco dela**, no fim, sem exceção.

### Lei 3 — leitura e escrita são dois blocos, e o segundo não roda hoje

Os ensaios de **SOMENTE LEITURA** (seção 4) não enviam um byte a aparelho nenhum:
abrem o nó, leem, contam, fecham. O pior desfecho de um erro de programação ali é
um relatório errado.

Os ensaios que **ESCREVEM** (seção 5) têm um preço que só ela pode autorizar, e
cada um traz escrito o que pode ficar num estado ruim e como se volta **sem
re-parear**.

### Lei 4 — o confundimento braço/unidade, e como cada ensaio escapa dele

Esta é a limitação central da mesa 2+2 com os braços fixos, e ela precisa estar
escrita antes dos ensaios, não depois.

São **dois** aparelhos por braço. Toda diferença que aparecer entre "os do cabo"
e "os do rádio" é, a rigor, **transporte somada a unidade** — os quatro
controles têm `hardware_version` diferentes entre si (`0x0711`, `0x0811`,
`0x0710`, `0x1111`), e dois deles são de outra revisão de placa.

O índice da leva já tinha nomeado a cura: **trocar os braços** e repetir. Mas
trocar os braços significa desplugar cabo e reconectar rádio — **derruba a
mesa**, e vai para o bloco dela.

**A escapatória que este plano usa:** priorizar ensaios cuja resposta é uma
**referência absoluta**, e não uma comparação entre braços. Um acelerômetro
parado tem de dar **1 g** — não "mais que o outro braço". Um microfone vivo tem
de dar **piso de ruído diferente de zero** — não "mais que o outro". Um CRC de
entrada tem de **conferir** — não "conferir mais que o outro".

Cada ensaio abaixo declara se é **IMUNE** ou **CONFUNDIDO**, e nenhum ensaio
confundido pode produzir célula com grau `medido` sem a troca de braços.

---

## 2. O que a mesa 2+2 NÃO pode preencher — dito antes de prometer

As **185 células mudas** do mapa (régua `aciona` vazio, que é a do censo do
portão) se repartem assim:

| controle | células mudas |
|---|---|
| Pro Controller | 77 |
| 8BitDo SN30 | 76 |
| **DualSense** | **32** |

**153 das 185 são de aparelhos que não estão nesta mesa.** Nenhum ensaio deste
plano as toca, e qualquer relatório que citar "reduzimos as 185" sem esta
repartição está mentindo por omissão.

O alvo real deste plano são as **32 mudas do DualSense na régua `aciona`** (e as
41 na régua `aceita`), com prioridade para a família `combinacao`, que existe
**exatamente** para a mesa cheia e cujas nove linhas estão quase todas em
`existe = desconhecido`.

---

## 3. Os instrumentos que faltam, e o que cada um precisa fazer

Nenhum destes existe hoje. **Construí-los é o primeiro item da fila.**

### I-1 — `scripts/ensaios/taxa_no_hidraw.py` <!-- ref-externa: instrumento a CRIAR por este plano, ainda não existe -->

O cavalo de carga do plano: dele saem os ensaios 2, 3 e 6.

O que ele tem de fazer:

1. **Cabeçalho declarando as DUAS portas.** Ele mede os quatro físicos **pelo
   broker** e os quatro vpads **por `open()` direto** (os vpads têm ACL; o broker
   recusa vpad, e recusar é o comportamento certo). O relatório imprime, por nó,
   qual porta serviu — é a mordida 2 de A-PORTA-QUE-A-CASA-CONSTRUIU-01.
2. **Declarar a biblioteca por caminho de arquivo**, não por nome. `os.read` e
   `time.monotonic` do `.venv/bin/python`, e nada mais. **Nenhuma `pydualsense`,
   nenhuma `evdev`, nenhuma SDL** — este instrumento mede o fio, não o jogo.
3. **Contar relatório, não `SYN_REPORT`.** A régua tem de aparecer no cabeçalho
   e no rodapé; é a `A-3` na sua versão mais barata.
4. **Ler os oito nós na MESMA janela**, com `select`/`poll` num laço só. Duas
   janelas em fila não são um ensaio de coexistência.
5. **Carimbar T0 e T1 em hora de parede** (`E5` do método), para cruzar com
   `journalctl` depois.
6. **Casar `hidrawN` -> `HID_UNIQ` pelo `uevent` a cada chamada**, nunca guardado
   — em 15/08 um controle sumiu e outro reapareceu com `eventN` diferente entre
   duas leituras com segundos de diferença. MAC mascarado no relatório.
7. **`--verificar-crc`**, que liga a conferência do CRC-32 de entrada
   (semente `0xA1`, `core/ds_output_report.py:57`) nos nós de rádio, e escreve
   `sem trailer` — nunca `0 falhas` — nos do cabo.
8. **CSV de saída.** Ensaio que não vira linha de tabela vira lembrança.

**A mordida do instrumento:** rode com os nós trocados na linha de comando. Se o
relatório não trocar de endereço junto, ele está lendo a ordem de enumeração e
não o aparelho.

### I-2 — `scripts/ensaios/imu_no_cabo.py` <!-- ref-externa: instrumento a CRIAR por este plano, ainda não existe -->

Lê o relatório de entrada dos quatro físicos pelo broker, extrai acelerômetro e
giroscópio, e imprime `|v|` em **g** contra a régua declarada
`DS_ACC_RES_PER_G = 8192`. Declara no cabeçalho de onde veio a régua (o driver,
e o mesmo número que o `absinfo` publica) — sem isso é `A-3`.

Tem de imprimir **os offsets que usou**, por transporte, porque o relatório do
cabo (`0x01`) e o do rádio (`0x31`) não têm o mesmo deslocamento.

### I-3 — `scripts/ensaios/microfone_no_cabo.py` <!-- ref-externa: instrumento a CRIAR por este plano, ainda não existe -->

Grava N segundos de cada placa ALSA de DualSense e decide por régua de máquina:
**zeros exatos em todas as amostras = não captou; qualquer piso de ruído =
captou.** Amarra placa ao controle pelo dispositivo USB em comum, como o
`audio_por_transporte.py` já faz — com dois no cabo, adivinhar por ordem erraria
metade das vezes.

---

## 4. OS ENSAIOS DE SOMENTE LEITURA — os que rodam hoje, sem ela

Ordem de valor por hora. Nenhum destes envia byte a aparelho nenhum.

---

### E-0 — O censo de abertura: a mesa é a que eu penso?

**1. Pergunta.** Estão mesmo dois no cabo e dois no rádio, com quatro vpads de
pé, agora?

**2. Célula.** `combinacao.tres_na_mesa@dualsense`, colunas `cabo_aceita` e
`radio_aceita` (2 mudas) e a coluna `existe`, hoje `desconhecido`.

**3. Somente leitura.** Sysfs e `uevent`. Nenhum hidraw aberto.

**4. Comando literal.**

```bash
cd /mnt/Apate/Desenvolvimento/hefesto-dualsense4unix
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/quem_e_quem.py
```

**Sem `--apertar`** — o modo interativo pede a mão dela e está fora desta janela.

**5. Os dois desfechos.** Dois `cabo` e dois `rádio` na coluna de transporte,
mais quatro vpads: a mesa está de pé, `combinacao.tres_na_mesa` passa a
`existe = tem` com quatro (que é mais que três), e a fila abaixo pode rodar. Se a
contagem der outra coisa — três de um lado, ou um controle sumido — **para
tudo**: uma tabela "cabo contra rádio" com um transporte só não compara nada, e
todo ensaio abaixo herdaria a mentira.

**6. Custo:** 3 minutos. **Armadilha:** `A-16`, o instrumento mirar no vpad — ele
já escapa por desenho, mostrando `vpad (sem transporte)` e tirando-o de toda
comparação.

**7. Precisa dela?** Não.

**Confundimento:** IMUNE (é censo, não comparação).

---

### E-1 — A topologia do fio: cabo e rádio dividem o controlador USB?

**1. Pergunta.** O adaptador de Bluetooth mora no mesmo controlador USB dos
controles do cabo?

**2. Célula.** `combinacao.adaptador_no_mesmo_controlador@dualsense` — coluna
`existe` (hoje `desconhecido`) e `cabo_aceita` + `radio_aceita` (2 mudas). As
duas colunas de `aciona` ficam para o E-6, que mede o **dano**, não a topologia.

**3. Somente leitura.** Sysfs puro. Porta: nenhuma. Biblioteca: nenhuma — é
`readlink` do shell, e essa é a graça.

**4. Comando literal.**

```bash
echo "== adaptador de radio =="
readlink -f /sys/class/bluetooth/hci0

echo "== controles do cabo =="
for n in 4 5; do
  printf 'hidraw%s -> ' "$n"
  readlink -f "/sys/class/hidraw/hidraw$n/device"
done

echo "== a arvore, com velocidade =="
lsusb -t
```

**5. Os dois desfechos.** **Mesmo nó PCI de xHCI** (é o que a leitura de 15/08 já
mostra: `0000:0c:00.3`): a hipótese de saturação de 10/08 tem base física nesta
máquina, e o E-6 mede se ela cobra alguma coisa. **Nós PCI diferentes:** a
hipótese morre nesta máquina, o defeito de 10/08 tinha outra causa — e a linha do
mapa passa a ser **condicional de hardware**, o que muda o conselho ao usuário de
*"não misture"* para *"depende da sua placa-mãe, e aqui está como conferir"*.
Os dois desfechos ensinam, e é por isso que este ensaio de dois minutos abre a
fila.

**6. Custo:** 2 minutos. **Armadilha:** `A-3`, medir contra a régua errada — o
"controlador" tem de ser o **nó PCI do xHCI**, não o número de "Bus" do `lsusb`
nem o hub intermediário. Escapa porque `readlink -f` devolve o caminho inteiro e
a comparação é textual, não de rótulo.

**7. Precisa dela?** Não.

**Confundimento:** IMUNE (topologia não tem unidade).

---

### E-2 — A taxa dos oito nós, na mesma janela. **É o ensaio que rende mais.**

**1. Pergunta.** Quantos relatórios por segundo cada um dos quatro controles
entrega, e cada um dos quatro vpads repassa, medidos todos ao mesmo tempo?

**2. Células — este é o ensaio que preenche mais:**

| linha do CSV | colunas | o que fecha |
|---|---|---|
| `combinacao.cabo_e_radio.taxa@dualsense` | `cabo_aceita`, `radio_aceita`, `cabo_aciona`, `radio_aciona` (4 mudas) | a taxa de cada braço, medida junta |
| `combinacao.cabo_e_radio.entrada@dualsense` | as mesmas 4 mudas | a entrada de cada um continua chegando |
| `combinacao.tres_na_mesa@dualsense` | `cabo_aciona`, `radio_aciona` (2 mudas) | os quatro vpads servidos ao mesmo tempo |
| `movimento.giroscopio.taxa@dualsense` | sobe `parcial` -> medido nos dois | a taxa declarada contra a entregue |

**3. Somente leitura.**

**4. Comando literal** (instrumento **I-1**, a construir):

```bash
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/taxa_no_hidraw.py --segundos 20 --csv /tmp/taxa-2-2.csv
date +%F' '%T.%3N
```

**Portas declaradas:** os quatro físicos pelo **broker**; os quatro vpads por
**`open()` direto**. As duas no mesmo relatório, e o relatório diz qual serviu
cada nó.

**5. Os dois desfechos.** **Taxas estáveis e distintas por transporte:** é a
primeira medição de coexistência dos dois braços no mesmo minuto, e ela ou
confirma ou derruba o par já registrado (250,0 Hz cravados no cabo contra
~414 Hz no rádio, medidos em 15/08 **com o daemon parado e sem companhia**).
Se a taxa do rádio vier **abaixo** dos ~414 Hz com a mesa cheia, existe um custo
de coexistência e o E-6 mede o mecanismo. Se vier igual, a companhia é de graça,
e a suspeita de 10/08 tem de mudar de alvo — de barramento para laço de escrita.

**6. Custo:** 15 minutos rodando, mais a construção do I-1. **Armadilhas:**
`A-16` (mirar no vpad do próprio produto) — escapa exigindo
`HID_PHYS != hefesto-vpad` e **imprimindo os vpads numa seção separada**;
`A-1` (disputar o hidraw) — não disputa, porque cada fd de hidraw tem fila de
entrada própria e este instrumento não escreve; `A-3` (régua) — declara se conta
relatório ou `SYN_REPORT`.

**Controle negativo, embutido e de graça:** os quatro vpads na mesma janela. Se a
taxa de um vpad sair **exatamente igual** à do físico correspondente, desconfie
do instrumento antes de comemorar: pode estar lendo o mesmo nó duas vezes.

**7. Precisa dela?** Não. O controle parado na mesa já transmite.

**Confundimento:** IMUNE do lado do cabo (existe régua independente: o
`bInterval` do endpoint declara 250 Hz); CONFUNDIDO na comparação absoluta entre
braços, e por isso a conclusão que se escreve é *"cada braço entregou X"*, nunca
*"o rádio é melhor que o cabo"*.

---

### E-3 — Os dois no rádio corrompem a entrada um do outro?

**1. Pergunta.** Com dois DualSense no mesmo adaptador, quantos relatórios de
entrada chegam com CRC quebrado?

**2. Célula.** `combinacao.dois_no_radio.crc@dualsense` — as 4 mudas
(`cabo_aceita`, `radio_aceita`, `cabo_aciona`, `radio_aciona`). O próprio código
já suspeita disto por escrito: `core/backend_pydualsense.py:200-207` cita
`DualSense input CRC's check failed` e nomeia a contenção com múltiplos
controles.

**3. Somente leitura.**

**4. Comando literal** (mesmo instrumento I-1, com a chave):

```bash
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/taxa_no_hidraw.py \
    --segundos 60 --verificar-crc --csv /tmp/crc-2-2.csv
date +%F' '%T.%3N
```

**Por que isto funciona com o daemon vivo, e é o detalhe que faz o ensaio
existir:** o `hidraw` recebe o relatório **antes** de o driver `hid_playstation`
validar o CRC e descartá-lo. Um leitor de hidraw enxerga o que o kernel depois
joga fora — que é exatamente a corrupção que se quer contar.

**5. Os dois desfechos.** **Taxa de falha diferente de zero e estável:** existe
contenção de rádio com dois controles, e ela passa a ter número — o que muda a
conversa sobre o que a interface deve avisar. **Zero falhas em 60 segundos nos
dois:** a suspeita registrada no código cai por medição, e a linha `A-20` obriga
a apagar a hipótese em vez de mantê-la "por via das dúvidas".

**6. Custo:** 10 minutos (reusa o instrumento do E-2). **Armadilha:** `A-3` de
novo, na forma mais traiçoeira — **conferir CRC no braço do cabo produz "difere"
em todos os relatórios**, porque no cabo os quatro últimos bytes são payload
comum. Escapa porque o instrumento escreve `sem trailer` no cabo, e nunca
`0 falhas`. É a mesma lição que o `censo_features.py` já pagou.

**Controle positivo obrigatório:** antes de contar falha, o instrumento tem de
provar que **conferiu certo pelo menos um quadro** — CRC que nunca confere em
lugar nenhum é instrumento quebrado, não aparelho corrompido.

**7. Precisa dela?** Não.

**Confundimento:** IMUNE (a régua é o próprio CRC, absoluta).

---

### E-4 — O acelerômetro no cabo: a célula que nunca teve um controle no cabo

**1. Pergunta.** O acelerômetro do controle **no cabo** entrega número calibrado?

**2. Célula.** `movimento.acelerometro@dualsense`, coluna `cabo_confianca` — hoje
`inferido-do-codigo`. O índice da leva é explícito: por cabo *"continua não
medido — não há controle no cabo"*. **Agora há dois.** O braço do rádio já foi
medido em 14/08 (`|v|` de 0,9945 g e 0,9823 g), e este ensaio fecha o par **no
mesmo minuto**, que é o pedido nº 5 dela: *"giroscópio, acelerômetro também.
todos via cabo e bt"*.

**3. Somente leitura.**

**4. Comando literal** (instrumento **I-2**, a construir):

```bash
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/imu_no_cabo.py --segundos 10 --csv /tmp/imu-2-2.csv
date +%F' '%T.%3N
```

**Porta:** broker, nos quatro físicos. **Não é evdev** — o co-op faz `EVIOCGRAB`
nos evdev físicos, e um leitor ingênuo ali lê zero e conclui que o aparelho está
calado. **Biblioteca:** `os.read` no fd do broker mais aritmética própria;
nenhuma `evdev`, nenhuma `pydualsense`. **Régua declarada:** 8192 LSB/g, do
driver, o mesmo número que o `absinfo` publica.

**5. Os dois desfechos.** **`|v|` perto de 1 g nos dois do cabo:** o acelerômetro
por cabo passa a `medido`, o par cabo/rádio fecha no mesmo instante, e uma das
oito células do pedido nº 5 dela deixa de ser inferência. **`|v|` longe de 1 g:**
ou os offsets do relatório do cabo não são os que o código supõe, ou a calibração
de fábrica não está sendo aplicada naquele braço — e isso é achado grande,
porque é o número que o produto entrega ao jogo.

**6. Custo:** 20 minutos, mais a construção do I-2. **Armadilha:** `A-3` — o
relatório do cabo (`0x01`) e o do rádio (`0x31`) não têm o mesmo deslocamento, e
usar o offset de um no outro produz número absurdo com cara de medida. Escapa
porque o instrumento **imprime os offsets que usou, por transporte**.

**Controle negativo obrigatório:** o mesmo cálculo nos **dois do rádio**, na
mesma janela. Eles têm de reproduzir os 0,98–0,99 g de 14/08. Se não
reproduzirem, quem mudou foi o instrumento, e nada do braço do cabo vale.

**7. Precisa dela?** Não — a gravidade é o sinal, e o controle parado na mesa é
a condição de ensaio, não um problema.

**Confundimento:** IMUNE. 1 g é referência absoluta; nenhuma conclusão depende de
comparar braço com braço.

---

### E-5 — O microfone no cabo, medido no aparelho e não no arquivo de configuração

**1. Pergunta.** O microfone do controle **no cabo** capta de verdade?

**2. Célula.** `audio.microfone@dualsense`, coluna `cabo_confianca` — hoje
`inferido-do-codigo`, e o índice da leva registra que a evidência atual é **o
arquivo do WirePlumber**, o que é medir a configuração e não o aparelho. O braço
do rádio já é `medido` de verdade (protocolo byte a byte, Opus decodificado).

**3. Somente leitura.** ALSA, sem tocar em hidraw nenhum.

**4. Comando literal** (instrumento **I-3**, a construir):

```bash
arecord -l    # confere quais placas sao dos DualSense do cabo

date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/microfone_no_cabo.py --segundos 5 --csv /tmp/mic-2-2.csv
date +%F' '%T.%3N
```

**Porta:** ALSA (`alsa-lib` via `arecord`), declarada no cabeçalho. Nenhum
hidraw, nenhum broker.

**5. Os dois desfechos.** **Piso de ruído diferente de zero nos dois do cabo:** o
microfone por cabo passa a `medido` no aparelho, e as duas metades do pedido nº 5
dela sobre microfone ficam medidas nos dois transportes. **Zeros exatos em todas
as amostras:** a rota ALSA está de pé e não entrega som — o que é um defeito de
produto e não um limite de aparelho, porque o mesmo microfone atravessa por
rádio desde 25/07.

**6. Custo:** 15 minutos, mais a construção do I-3. **Armadilha:** `A-10`,
confundir controle negativo com prova. Os dois do rádio **não têm placa ALSA
nenhuma** — e isso é o negativo do braço, mas prova apenas que **a rota ALSA** não
existe no rádio. **Não** prova que o aparelho não capta por rádio: já está medido
que capta, por HID e Opus. Essa frase, exatamente essa, tem de entrar na célula,
senão a falácia do perfil ausente volta pela porta dos fundos.

**Controle negativo de régua:** gravar do monitor de um sink mudo tem de dar
**zeros exatos**. Sem isso, "piso de ruído" é adjetivo, não medida.

**7. Precisa dela?** Não. Sala em silêncio é a condição ideal: o que se mede é o
piso, não conteúdo.

**Confundimento:** IMUNE (zero exato contra não-zero é absoluto).

---

### E-6 — O custo da companhia: dose-resposta no controlador compartilhado

**1. Pergunta.** Quando o controlador USB é carregado pelos controles do cabo, a
entrada dos do rádio cai?

**2. Célula.** `combinacao.adaptador_no_mesmo_controlador@dualsense`, colunas
`cabo_aciona` e `radio_aciona` (2 mudas) — o **dano**, que o E-1 não mede; e
`combinacao.cabo_e_radio.entrada@dualsense`, colunas de `aciona` (2 mudas).

**3. Somente leitura no aparelho.** A carga é **captura de microfone USB**, que é
leitura isócrona no mesmo controlador — nenhum byte HID enviado a controle
nenhum. É por isso que este ensaio existe nesta forma: a versão óbvia (martelar
com rumble) escreveria, e escrita está fora desta janela.

**4. Comando literal** (três patamares, o mesmo I-1 medindo):

```bash
# patamar 0 — sem carga (esta e a linha de base, e ela vem do E-2)
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/taxa_no_hidraw.py --segundos 20 --csv /tmp/dose-0.csv

# patamar 1 — UM microfone do cabo capturando
arecord -D hw:2,0 -f S16_LE -r 48000 -c 1 -d 25 /dev/null &
sleep 2
.venv/bin/python scripts/ensaios/taxa_no_hidraw.py --segundos 20 --csv /tmp/dose-1.csv
wait

# patamar 2 — OS DOIS microfones do cabo capturando
arecord -D hw:2,0 -f S16_LE -r 48000 -c 1 -d 25 /dev/null &
arecord -D hw:3,0 -f S16_LE -r 48000 -c 1 -d 25 /dev/null &
sleep 2
.venv/bin/python scripts/ensaios/taxa_no_hidraw.py --segundos 20 --csv /tmp/dose-2.csv
wait
date +%F' '%T.%3N
```

Os números de placa (`hw:2`, `hw:3`) **saem do `arecord -l` da hora**, nunca
gravados: a numeração já mudou duas vezes num único dia nesta máquina, e uma
medição de áudio virou lenda por causa disso.

**5. Os dois desfechos.** **A taxa dos do rádio cai monotonicamente com o
patamar:** a saturação existe, tem dose-resposta, e isso é **prova causal** — não
indício. O defeito de 10/08 ganha mecanismo, e a interface passa a ter o que
dizer. **A taxa não se move nos três patamares:** a topologia compartilhada não
basta para produzir o dano, o suspeito "barramento" é inocentado, e o próximo
suspeito passa a ser o **laço de escrita** do `sendReport` — que é outro lugar,
outra cura, e economiza a sessão inteira que se gastaria no lugar errado.

**6. Custo:** 20 minutos. **Armadilhas:** `A-7` (só um lado do ensaio) — os três
patamares são os dois lados e mais um; `A-20` (presumir causa e escrever como
medição) — só se escreve o que a curva mostrar, e "não mexeu" é resultado, não
falha do ensaio; `A-9` — nada aqui pede a mão de ninguém.

**7. Precisa dela?** Não.

**Confundimento:** IMUNE — a comparação é do **mesmo aparelho consigo mesmo** em
três patamares. É o `D2` do método (dose-resposta) e é o desenho mais forte deste
plano inteiro.

---

### E-7 — O censo dos feature reports **pela porta certa**

**1. Pergunta.** Os 22 do cabo e os 17 do rádio se leem com o daemon **vivo**,
pelo broker?

**2. Célula.** Nenhuma diretamente — e é por isso que ele não vem antes. O valor
dele é **provar a porta**: se este ensaio passar, toda leitura de feature deixa de
exigir derrubar o daemon, e o conselho do `scripts/ensaios/README.md` muda.

**3. Somente leitura.**

**4. Comando literal** (instrumento existente, depois da entrega E2 de
A-PORTA-QUE-A-CASA-CONSTRUIU-01):

```bash
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/censo_features.py --tentativas 6
date +%F' '%T.%3N
```

**5. Os dois desfechos.** **Os 22 e os 17 saem com o daemon vivo:** a receita
`systemctl --user stop` sai do README, e todo ensaio de leitura desta casa deixa
de custar uma mesa. **A leitura por rádio fica pior que com o daemon parado
(mais retentativas, mais timeouts):** o custo é da **coexistência com o daemon**,
não do rádio — e essa distinção nunca foi feita, porque nunca se mediu dos dois
jeitos no mesmo dia.

**6. Custo:** 15 minutos, quase todo em timeout de 3 s do BlueZ. **Armadilhas:**
`A-1` (o instrumento disputar o hidraw) — não disputa: `GET_FEATURE` por ioctl no
fd do broker é ortogonal ao fluxo de entrada do daemon; a `A-5` (relatório de
agente não é prova) — o CSV do instrumento é a prova, não o resumo.

**Controle negativo obrigatório:** pedir um id que o descritor **daquele
transporte** não declara. Tem de falhar, e a falha tem de ser distinguida do
timeout: `EPIPE` na hora é resposta definitiva do aparelho; 3,2–3,7 s é o timeout
do BlueZ; falhas em ~0,01 s são o controle tendo desconectado.

**7. Precisa dela?** Não.

**Confundimento:** CONFUNDIDO para qualquer afirmação "o rádio custa mais que o
cabo" (são unidades diferentes); IMUNE para "com o daemon vivo dá para ler".

---

### E-8 — O `0x22`: o feature que este projeto nunca leu, nos dois braços

**1. Pergunta.** O feature `0x22` carrega identidade por unidade — e ela é a
mesma pelos dois transportes?

**2. Célula.** Linha nova na família `identidade`. O `0x22` é o último candidato
de identidade que **não** foi descartado por medição própria: a UNIDADE-COR-01
registra que o offset 45-51 é ASCII numa série e binário noutra, e que o
`0x20` bytes 32-43 difere por unidade sem ninguém ter decifrado.

**3. Somente leitura.**

**4. Comando literal.**

```bash
date +%F' '%T.%3N
.venv/bin/python scripts/ensaios/censo_features.py --so 0x22 --so 0x20 --tentativas 8
date +%F' '%T.%3N
```

**5. Os dois desfechos.** **Difere por unidade E é idêntico nos dois
transportes:** existe chave de identidade independente de canal, que é
exatamente o que o README dos instrumentos pede e o que falta para o
`hardware_version` deixar de ser âncora de acaso de lote. **Difere por
transporte:** não serve de identidade, a linha nasce com a ressalva escrita, e a
próxima pessoa não gasta a tarde que essa descoberta custaria.

**6. Custo:** 10 minutos. **Armadilha:** a `A-3` na versão barata que o índice já
nomeou — **declarar a unidade**. `0x22` tem 64 ou 63 bytes conforme se conte o
byte do Report ID, e nenhum relatório desta casa declarou a régua. O instrumento
tem de imprimir os dois números lado a lado.

**Controle negativo:** o próprio `0x20` na mesma rodada, que é conhecido — se ele
vier diferente do que o censo de 15/08 registrou, o instrumento mudou.

**7. Precisa dela?** Não.

**Confundimento:** IMUNE para "difere por unidade" (é o objetivo); CONFUNDIDO
para "difere por transporte" enquanto os braços não trocarem — dois aparelhos por
braço não separam as duas coisas. **Esta ressalva tem de entrar na célula.**

---

## 5. O BLOCO DELA — o que NÃO roda nesta janela, e por quê

Nada abaixo pode rodar sem ela na sala. Não é excesso de cuidado: cada item
escreve no aparelho, ou derruba a mesa, ou pede o olho dela como instrumento.

### 5.1 Os que ESCREVEM no aparelho

| ensaio | de onde vem | o que pode ficar ruim | como se volta **sem re-parear** |
|---|---|---|---|
| **E-6 da ESCADA** — mandar o `0x32` do rádio para um controle **no cabo** | ESCADA-QUE-RESPONDE-01 §E-6 | o firmware do cabo recebe um relatório que o descritor dele não declara; o esperado é recusa silenciosa | o daemon reescreve o estado de saída no próximo keepalive (0,5 s). Não toca NVS |
| **E-1/E-2/E-3 da ESCADA** — a escada de output e o byte `[2]` | ESCADA-QUE-RESPONDE-01 | lightbar, LED de jogador e gatilho num estado que ninguém pediu | idem: keepalive de 0,5 s devolve o estado do perfil. **Depende da D-31** |
| **A cor de fábrica** (`SET_FEATURE 0x80` + `GET 0x81`) | UNIDADE-COR-01 §4 | **é a família de comandos de fábrica**: `[1,1]` reseta o controle, `[12,1,…]` grava calibração de stick na NVS | **não há volta garantida.** É por isso que é a **D-15**, e é por isso que o payload tem de ser montado uma vez, conferido em `--dry-run`, e nunca gerado por laço |
| **EXP-SPK-01** — o `0x39` com o bloco `0x13` a 50 Hz por 3 s | ESCADA-QUE-RESPONDE-01 §E-5 | rajada de 547 B a 50 Hz pode saturar a fila do enlace e **derrubar o link** | reconectar pelo botão PS. **Risco real de derrubar a mesa**, e por isso é o último de todos. **Depende da D-31** |
| **Qualquer `SET_FEATURE` em `0xF0`-`0xF7`** | — | **é o canal de atualização de firmware** | **PROIBIDO.** É a **D-32**, e a proibição é da casa |

**Por que a mesa 2+2 é o que dá valor a estes:** o E-6 da ESCADA só significa
alguma coisa com um controle no cabo e um no rádio **no mesmo minuto** — é o
negativo de transporte, e é o único desenho que separa *"a escada é do rádio"* de
*"a escada é de hoje"*. E a cor de fábrica só está demonstrada **por cabo**: com
os dois braços na mesa, uma falha no rádio é atribuível ao transporte, e não à
unidade nem ao dia.

### 5.2 Os que derrubam a mesa

| ensaio | célula | por que derruba |
|---|---|---|
| **A troca de braços** (o do cabo vira rádio e vice-versa) | é a cura do confundimento da **Lei 4** — sem ela, nenhum ensaio CONFUNDIDO pode virar `medido` | exige desplugar cabo e reconectar rádio |
| **A estabilidade do slot no rádio** | `combinacao.slot_jogador.estabilidade@dualsense`, `radio_aciona` (1 muda) — o braço do cabo já foi medido em 12/08 | exige desconectar e religar um controle do rádio |
| **A saída com dois no rádio / cabo e rádio juntos** | `combinacao.dois_no_radio.saida@dualsense` (3 mudas) e `combinacao.cabo_e_radio.saida@dualsense` (2 mudas) | é saída: escreve cor, LED e rumble, e a régua é o olho dela |
| **O canal 3 às cegas** (D-28) | `audio.saida_dedicada@dualsense`, e desempata o modelo dela contra o do mapa — hoje **empatados em zero prova** | é a orelha dela, e é escrita |

**Uma armadilha que vale repetir aqui, porque ela já custou uma sessão:**
**plugar o cabo pode não trocar o transporte.** Um DualSense pareado por
Bluetooth que recebe o cabo pode continuar falando por rádio e só carregar. O
braço se confere no `HID_ID` do `uevent` (`0003` é USB, `0005` é Bluetooth) —
**nunca** na suposição de que "está plugado, logo é USB" —, e a conferência entra
no relatório, não no comentário.

---

## 6. ORDEM DE EXECUÇÃO — a fila literal, e onde ela para

```
   [construir I-1]  taxa_no_hidraw.py           <- bloqueia E-2, E-3, E-6
        |
   E-0  censo da mesa                (3 min)    <- PARA TUDO se a mesa nao for 2+2
        |
   E-1  topologia do fio             (2 min)    <- so le sysfs; nunca falha por acesso
        |
   E-2  taxa dos oito nos           (15 min)    <- PARA a coluna do hidraw se o broker nao abrir
        |
   E-3  CRC dos dois do radio       (10 min)    <- reusa o I-1
        |
   [construir I-2]  imu_no_cabo.py
        |
   E-4  acelerometro no cabo        (20 min)
        |
   [construir I-3]  microfone_no_cabo.py
        |
   E-5  microfone no cabo           (15 min)    <- e a carga do E-6; nesta ordem de proposito
        |
   E-6  dose-resposta da companhia  (20 min)    <- precisa da linha de base do E-2
        |
   E-7  censo pela porta certa      (15 min)
        |
   E-8  o 0x22 nos dois bracos      (10 min)
        |
   ======================= ela volta =======================
        |
   D-31 / D-15 / D-32  (a palavra dela)
        |
   ESCADA E-6 (o negativo de transporte, 5 min)  <- o mais barato do bloco dela
   ESCADA E-3, E-1, E-2                          <- o montador, a estrutura, os degraus
   a troca de bracos                             <- cura o confundimento da Lei 4
   a cor de fabrica pelos dois bracos
   EXP-SPK-01                                    <- por ultimo, e so por ultimo
```

**Onde a fila para, e o que fazer:**

1. **E-0 falha** (a mesa não é 2+2): **para tudo.** Nada abaixo compara nada.
   Registre o estado encontrado e espere por ela — remontar a mesa é
   re-pareamento, e re-pareamento está fora desta janela.
2. **O broker não abre** (`abrir_no` devolve `(None, motivo)` nos quatro): param
   **E-2, E-3, E-4, E-7 e E-8** juntos — todos leem hidraw físico. **E-1, E-5 e o
   E-6 do lado da carga continuam**, porque não passam por hidraw. Registre o
   `motivo` literal: ele distingue *broker ausente* de *broker recusando*, e essa
   distinção é a entrega E1 de A-PORTA-QUE-A-CASA-CONSTRUIU-01.
3. **O controle positivo de um ensaio falha** (o CRC nunca confere; o rádio não
   reproduz os 0,98 g de 14/08; o `0x20` sai diferente do censo de 15/08):
   **para aquele ensaio**, não a fila. O réu é o instrumento, e a casa já tem três
   medições falsas num dia por não ter parado nesse ponto.
4. **Um controle some no meio** (`ENODEV`, falhas voltando em ~0,01 s): pare o
   ensaio em curso, rode o E-0 de novo, e **não** conclua nada sobre o aparelho —
   ele não está mais lá. Anote a hora de parede: é o que permite cruzar com
   `journalctl -k` depois.

---

## 7. O que este plano NÃO promete

Repetido no fim de propósito, porque quem lê plano de bancada lê o começo e o
fim.

- **Ele não toca 153 das 185 células mudas.** Aquelas são do Pro Controller e do
  8BitDo, e não há Pro nem 8BitDo nesta mesa.
- **Ele não mede saída.** Todo o bloco de leitura mede o que o aparelho
  **entrega**; o que ele **obedece** exige escrita, e escrita exige ela.
- **Ele não decide nada sobre áudio por rádio.** O canal responde e o payload
  segue não identificado — e é a **falácia do canal que responde** que faria
  qualquer outra frase parecer justificada.
- **Ele não separa transporte de unidade** nos ensaios marcados CONFUNDIDO. Só a
  troca de braços separa, e ela está no bloco dela.
- **O que ele promete, e é bastante:** oito ensaios que rodam sozinhos em cerca
  de uma hora e meia de máquina, sem derrubar a mesa, sem pedir a mão dela, e
  que preenchem células que estão mudas desde que o mapa nasceu — a começar
  pelas da família `combinacao`, que existe exatamente para esta mesa e que nunca
  teve a mesa para ser respondida.

---

## 8. Onde cada resultado é escrito

**Medição sobre o aparelho tem como destino o mapa de canais** — não um
comentário de código, não um relatório de agente, não um transcrito. É a regra
que a UNIDADE-COR-01 deixou escrita depois de cinco dias de um achado enterrado,
e as specs são a memória externa dela.

Cada ensaio fechado escreve, na linha do CSV que ele nomeia:

- `cabo_aceita` / `radio_aceita` / `cabo_aciona` / `radio_aciona` — o veredito;
- `cabo_confianca` / `radio_confianca` — `medido` só com instrumento, data e quem
  mediu;
- `cabo_evidencia` / `radio_evidencia` — **o comando que refaz a medição**, não a
  conclusão dela;
- `provado_em` — a data;
- `assimetria_declarada` — quando um lado fica mudo **por construção** (o CRC no
  cabo, a escada no cabo), porque vazio sem essa frase é lido como "ninguém
  respondeu";
- `nota` — a ressalva do confundimento braço/unidade, nos ensaios marcados
  CONFUNDIDO.

E o `linha_id` de cada ensaio carrega o `@dualsense`: sem ele o ensaio não casa
com o mapa e **some do julgador**, que é a armadilha `A-22`.
