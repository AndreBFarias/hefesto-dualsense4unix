# A NOITE DOS QUATRO INVENTÁRIOS — a distância entre o que a casa sabe e o que o produto faz

- **Escrito em:** 09/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que este arquivo é:** a fila executável do que sobrou da noite de 08→09/08,
  e o registro de **quatro hipóteses minhas derrubadas por medição** — três delas
  derrubadas por ela
- **Grau:** tudo abaixo é **MEDIDO** salvo onde diz o contrário
- **Estado da fila (09/08/2026, fim do dia):** **PARCIALMENTE PAGA.** Seis itens
  da fila — **F-1, F-3, F-4, F-8, F-9 e F-10** — entraram em `7a0a655`
  (09/08/2026) e estão **ENTREGUES EM CÓDIGO, AGUARDANDO A PALAVRA DELA**.
  **F-2, F-5, F-6, F-7 e F-11 continuam ABERTOS** — dois deles com a prova da
  ausência registrada na
  [nota datada no fim](#nota-datada-09082026--o-que-a-fila-pagou-hoje-e-o-que-não). A fila
  abaixo **não foi reescrita**: ela é o texto de origem
- **RECONTAGEM (09/08/2026, fim do dia) — a linha acima está desatualizada em
  três pontos, e a de baixo é a que vale.** **ENTREGUES EM CÓDIGO, aguardando a
  palavra dela:** F-1, F-4, **F-5**, **F-6(b)**, **F-6(c)**, F-8.
  **PARCIAIS:** F-3, F-7, F-9, F-10. **ABERTOS:** F-2, **F-6(a)**, F-11. O
  F-5 estava entregue e a busca anterior não o achou — a cura se chama
  `controles_sem_driver` e mora em `app/actions/status_actions.py`, não nos dois
  arquivos que o `grep` varreu. A prova de cada item está na
  [segunda nota datada, no fim](#nota-datada-09082026-fim-do-dia--a-recontagem-e-três-correções-à-nota-acima)
- **O que falta ela validar, em uma linha:** ligar dois controles pelo rádio ao
  mesmo tempo e ver se os dois sobem; e mexer no touchpad e no giroscópio depois
  de uma instalação limpa, **sem `sudo`**, para ver se pararam de funcionar por
  acidente

---

## 1. A noite em uma frase

**O produto sabe muito mais do que faz.** Quatro inventários mediram a mesma
distância por quatro ângulos: a causa do defeito de hoje estava escrita no
repositório desde 25/07; a cura de ontem está no disco dela e não em vigor; doze
passos de cura não entram em nenhum formato que não seja `native`; e a janela não
sabe dizer que um controle sumiu.

---

## 2. As hipóteses que caíram, e quem as derrubou

Fica registrado porque o padrão importa mais que os erros: **três das quatro
foram derrubadas por ela, com observação direta do aparelho.**

| hipótese minha | quem derrubou | com o quê |
|---|---|---|
| o `skip_cache` da lightbar era o culpado | verificação adversarial | o log só sai DEPOIS de uma escrita bem-sucedida, e aparecia igual no dia em que a luz funcionava |
| a `A-LUZ-QUE-CUROU-01` (07/08) causou a regressão da barra | verificação adversarial | aquela sprint não tocou uma linha de código de lightbar |
| a caixinha do Steam Input matou o rumble | **ela** | *"funcionava com o input steam ligado e com ele desligado"* |
| o dongle/porta USB degradando o rádio | **ela**, pela segunda vez em duas semanas | *"milhares de vezes provamos que a tese é inválida"* — e o índice de 08/08 §7 já registrava o veto |
| a curva 12→37 era degradação dos DualSense | dois agentes, em separado | as falhas eram do 8BitDo e do DualShock 4; contadas por aparelho, os DualSense só aparecem em 08/08 |

**A regra que a noite reforça:** hipótese que não explica o que JÁ funcionava é
contorno. As quatro falharam nesse teste, e as quatro eram minhas.

---

## 3. A causa do controle que some — MEDIDA, e escrita desde 25/07

O sintoma dela: um DualSense conecta, acende azul, **sem LED de jogador**, e o
Hefesto não o enxerga. A aba Início chega a dizer *"Nenhum controle conectado"*.

A cadeia, e cada elo tem endereço:

1. `playstation …: Failed to retrieve feature with reportID 32: -5` (×3) →
   `Failed to create dualsense` → `probe with driver playstation failed`;
2. o `-5` é **máscara**: o BT achata qualquer erro de transporte em `-EIO`
   (`assets/dkms/hid-playstation/README.md:62-114`);
3. **quem desistiu foi o BlueZ**, não o kernel: `hidp_report_req_timeout()`,
   `REPORT_REQ_TIMEOUT` = **3 s**. Confirmado no journal dela em 08/08 23:36:14,
   :17 e :20, casado um a um com as três falhas do driver;
4. **o gatilho é dois DualSense subindo no mesmo adaptador com ~1 s de
   diferença** — o segundo perde o canal de controle L2CAP. Em 23:36:10 um
   registrou e o outro nasceu no mesmo segundo.

**Os 6 abortos de 08/08 recuperaram sozinhos** (2 a 20 min), por reconexão — não
por rebind. Não há controle órfão agora.

### 3.1 O achado que é NOSSO, e é a cura de raiz

**O retry que esta casa escreveu no patch do kernel não pode funcionar.**

- cada tentativa custa os **3 s inteiros** do BlueZ;
- o backoff entre elas é de **100 ms e 200 ms**
  (`assets/dkms/hid-playstation/hid-playstation.c:36`, `:902-920`);
- logo, **as três tentativas caem dentro da mesma janela de contenção**. Medido:
  00:17:04 → :07 → :10 → aborto.

O espaçamento é ~30× pequeno demais para o problema que ele se propõe a
atravessar. É por isso que o rebind — que espera **minutos** — cura, e o retry
não. Custo atual: a falha demora ~10 s em vez de ~3,3 s.

**Nota datada devida:** o `README.md:234-244` declarava *"que `feature_retries=2`
de fato cura"* como **NÃO MEDIDO**, com a validação prevista para o próximo boot.
A validação chegou: **6 de 6 abortos retentaram e nenhum foi salvo.** A hipótese
caiu.

E o próximo degrau já estava nomeado no mesmo README, há 14 dias, sem nunca virar
código: *"ou **serializar a subida dos controles** no daemon do hefesto"*.

---

## 4. A FILA — em ordem de raiz, não de esforço

### F-1 — o backoff do retry passa a cavalgar o timeout do BlueZ
`assets/dkms/hid-playstation/` + `assets/modprobe.d/hefesto-hid-playstation.conf`.
De 100/200 ms para além dos 3 s. **Teste que morde:** o patch declara o
espaçamento em função do teto do BlueZ, e um portão reprova quem o reduzir sem
nota. **Grau da cura: SUSPEITA COM MECANISMO** — o mecanismo é medido, o efeito
só se prova no próximo par de conexões simultâneas dela.

### F-2 — serializar a subida de dois controles no mesmo adaptador
O degrau nomeado há 14 dias. Ninguém, no produto, espaça duas conexões BT.
**Aberto: onde mora a serialização** (daemon? agente de pareamento? udev?) —
decisão de desenho, não de código.

### F-3 — o `WatchdogSec=0` em VIGOR, e um portão que meça isso
Na máquina dela, agora: o drop-in tem `WatchdogSec=0` e
`systemctl show -p WatchdogUSec` devolve **`30s`**. **Cura no disco ≠ cura em
vigor**, e o `doctor.sh` **não lê `WatchdogUSec` em lugar nenhum** — máquina
curada e máquina que vai morrer imprimem o mesmo veredito.

### F-4 — detector de probe morto do `hid-playstation` no doctor
Existe para o Pro Controller
(`doctor.sh:3495`, `_check_hid_nintendo_probe_death_signature`) e **não existe**
para o DualSense (`doctor.sh:308-315` só confere se o módulo carregou).

### F-5 — a janela precisa saber dizer "visto no rádio, não adotado"
Hoje `describe_controllers` devolve uma entrada **por handle aberto**; sem
hidraw não há handle, e a aba Início escreve *"Nenhum controle conectado"* para
um controle ligado e pareado. **Não existe no produto a noção de controle
não-adotado.**

### F-6 — as três telas que mentem
- **(a)** aba Status afirma "Conectado · USB · 85%" com a mesa vazia — o topo do
  `state_full` (`daemon/ipc_handlers.py:1644-1648`) é mantido em PARALELO à lista
  (`:1724`), nunca derivado dela. É a `ESTADO-QUE-MENTE-01` de 03/08, ainda
  proposta, sem teste;
- **(b)** o toast *"Cor aplicada no controle"*
  (`app/actions/lightbar_actions.py:636-643`) sai do `ok` do daemon, que
  significa "o report saiu" — nunca "a barra acendeu";
- **(c)** `rumble_ff.plays` só aparece na tela **quando é > 0**
  (`app/actions/rumble_actions.py:571-573`): a linha fica muda exatamente no caso
  em que teria algo a dizer.

### F-7 — o `install.sh` desiste na linha 941
Com `FORMAT != native`, ele roda cinco passos e faz `exit 0`. **Doze passos de
cura** ficam de fora — toda a camada de Bluetooth de sistema, o áudio, o wrapper
`hefesto-launch`, o kernel-watch e a conferência final. E o aviso que o próprio
script imprime (`:936-938`) **lista errado** o que está pulando.

### F-8 — o touchpad e o giroscópio dela funcionam por acidente
Nenhuma regra em `assets/*.rules` dá acesso aos nós `/dev/input/event*`;
`install_udev.sh:81-91` cria o grupo `hefesto` e **nada toca o grupo `input`**.
Ela está no `input` **por fora do produto**. Numa máquina nova, não funciona. O
doctor não checa.

### F-9 — regras-cola empacotadas sem os scripts que elas chamam
As regras 82 e 83 viajam em todos os formatos e chamam alvos em
`/usr/local/lib/...` que **nenhum pacote instala** — ruído permanente no journal
de quem instalar por pacote. O próprio `uninstall.sh:652-660` já nomeia esse modo
de falha.

### F-10 — o portão de paridade, cego ao que mais regride
Não cobre: units/timers/scripts de Bluetooth, os drop-ins de WirePlumber, o
`hefesto-launch`, o `storm_watch.sh`, dependências de tempo de execução
(`bluez-tools`, `libopus0`), o **alvo** de uma regra-cola, e a assimetria inversa
(nada verifica que o `install.sh` **recria** o que o `uninstall.sh` levou).

### F-11 — dívidas menores, todas medidas
- borda de udev existe para o snapshot de bond e **não** para o rebind de órfão —
  o controle fica invisível por até 2 min esperando o timer;
- fuga de fd em `backend_pydualsense.py:1469-1479` quando o `init()` estoura;
- `bt-bonds.pre-uninstall-<carimbo>` é órfão de nascença: o uninstall cria, o
  install não recolhe, ninguém enxerga — e são credenciais;
- o drop-in 51 de áudio repete o defeito de `108b711`: install arma, uninstall
  desarma, e o **doctor lê a ausência como escolha dela**.

---

## 5. O que ENTROU nesta noite

| cura | onde |
|---|---|
| os dois tempos da janela separados (o clique marca, o Aplicar aplica) | `1c75a1a` |
| o AGORA deixa de ser refém do DEPOIS — quatro buracos | `10f013a` |
| o diálogo deixa de depender de qual aba está à vista | `JOGO-ABERTO-SO-NA-INICIO-01`, nesta leva |
| instrumento do 0x08 (`lightbar-reset`) e do isolamento de players (`player-leds`) | nesta leva |

**E o que os instrumentos mediram na mesa dela:**
- o 0x08 **fora** da janela de conexão **não trava** a barra — confirma o
  controle negativo que a sprint de 03/08 tinha e leu ao contrário;
- o 0x08 **apaga os LEDs de jogador**, e eles não voltam sozinhos;
- **a escrita do player-LED NÃO é quem derruba a barra** (hipótese dela,
  eliminada com variável única);
- um **restart do daemon** repinta as barras — o latch não é permanente.

---

## 6. Nota de método

Quatro agentes investigaram em paralelo, nenhum com permissão de editar. Três
mediram melhor do que eu, e um corrigiu a data de uma investigação anterior — o
que derrubou dois suspeitos de uma vez.

O erro de método mais caro da noite foi meu e é digno de registro: **eu contaminei
o experimento do 0x08 com o restart que era necessário para o instrumento
existir.** A barra voltou no restart, dois minutos antes do gesto que eu queria
medir. A lição virou desenho: o instrumento seguinte (`player-leds`) é
**comutável ao vivo**, justamente para não exigir restart.

---

## NOTA DATADA (09/08/2026) — o que a fila pagou hoje, e o que não

Conferido no código do fim do dia, item a item. **A fila acima não foi
reescrita.** Tudo o que entrou está em `7a0a655` (09/08/2026), commitado — não
sobrou nada em árvore suja.

### Os seis que a noite pagou

| item | onde está hoje |
|---|---|
| **F-1** o backoff que cavalgava o timeout do BlueZ | `assets/dkms/hid-playstation/hid-playstation.c:909` e `:935` — o comentário mede o preço antigo (falha em ~10 s em vez de ~3,3 s) e declara o backoff novo contra o `REPORT_REQ_TIMEOUT` de 3 s do BlueZ |
| **F-3** o `WatchdogSec=0` em vigor, com portão que meça | `assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf:9-11` e o portão que morde em `tests/unit/test_bt_resilience_assets.py:119` — que exige `^WatchdogSec=0$` exato. O teste antigo aceitava `WatchdogSec=\d+`, **qualquer número**, e por isso ficou verde enquanto o watchdog matava o rádio dela (`:111`) |
| **F-4** detector de probe morto do `hid-playstation` | `scripts/doctor.sh:332`, com o porquê em `:14`; teste em `tests/unit/test_doctor_hid_playstation_probe.py` |
| **F-8** o touchpad e o giroscópio funcionavam por acidente | `assets/72-hefesto-touchpad-motion-uaccess.rules` — arquivo **novo**. O `:29` registra a causa: o kernel classifica o nó de movimento como `ID_INPUT_ACCELEROMETER`, e a `70-uaccess.rules` do sistema só cobre `ID_INPUT_JOYSTICK` |
| **F-9** regra-cola empacotada sem quem a instale | `scripts/install_udev.sh:58` e `:113`, e `scripts/install-host-udev.sh:194` — os **dois** caminhos de instalação passaram a instalar a regra nova |
| **F-10** o portão de paridade, cego ao que mais regride | `scripts/check_packaging_parity.sh:386` — passou a reprovar quando nenhuma regra dá `uaccess` ao nó dos sensores de movimento, e `:383` cobra a renumeração para antes da `73-seat-late.rules` |

### Os cinco que continuam abertos — e dois com prova da ausência

- **F-5 — "visto no rádio, não adotado": NÃO ENTREGUE, medido por ausência.**
  `grep` por `adotado`, `nao_adotado` e `visto_no_radio` em
  `daemon/ipc_handlers.py` e `app/actions/home_actions.py` devolve **zero**. A
  noção de controle não-adotado continua não existindo no produto, e a aba
  Início continua podendo escrever *"Nenhum controle conectado"* para um
  controle ligado e pareado.
- **F-7 — o `install.sh` que desiste: NÃO ENTREGUE.** O `exit 0` do formato
  não-`native` continua em `install.sh:941`, com os cinco passos antes dele. O
  aviso de `:935-938` foi reescrito e hoje lista o que pula com mais honestidade,
  mas **os doze passos de cura continuam de fora**.
- **F-2, F-6 e F-11 — NÃO CONFERIDOS.** Não achei evidência suficiente para
  afirmar nem para negar, e por isso **não foram remarcados**. Ficam na fila.

### O grau, como manda a casa

**MEDIDO** para os seis pagos — há símbolo, arquivo e portão que morde.
**MEDIDO por ausência** para F-5 e F-7. **SEM PROVA** para F-2, F-6 e F-11.

E **SEM PROVA** para o efeito de todos eles na máquina dela: nada aqui foi visto
com o aparelho na mão. É o que a linha de validação do cabeçalho pede.

---

## NOTA DATADA (09/08/2026, fim do dia) — a recontagem, e três correções à nota acima

**Nada acima foi apagado.** A nota anterior é honesta e a maior parte dela se
confirma. O que muda são **três itens**, e o motivo importa mais que a
correção: em dois deles **o instrumento errou, não o produto** — a busca
procurou a palavra errada, no arquivo errado.

### Correção 1 — o F-5 ESTÁ entregue; a busca é que não o achou

A nota acima declarou o F-5 *"NÃO ENTREGUE, medido por ausência"*, com `grep`
por `adotado`, `nao_adotado` e `visto_no_radio` em `daemon/ipc_handlers.py` e
`app/actions/home_actions.py`. **A cura existe e está ligada de ponta a ponta —
só que com outro nome e em outro arquivo:**

| ponta | onde |
|---|---|
| o daemon publica o bloco | `src/hefesto_dualsense4unix/daemon/ipc_handlers.py:1924` (`result["controles_sem_driver"]`) e `:2819` (`_controles_sem_driver_payload`) |
| a janela lê o bloco | `src/hefesto_dualsense4unix/app/actions/status_actions.py:221` |
| a função pura do texto | `src/hefesto_dualsense4unix/app/actions/status_actions.py:188` (`texto_de_controle_nao_adotado`) |
| o banner que pinta | `src/hefesto_dualsense4unix/app/actions/status_actions.py:2375` (monta) e `:2418` (atualiza), chamado em `:470` e `:2249` |

O nome no código é **`controles_sem_driver`**, e a superfície é a aba **Estado**,
não a Início. A docstring de `:188` cita `CONTROLE-QUE-NAO-ENTROU-01
(09/08/2026)` e descreve a mesma medição da seção 3 deste documento: dois
DualSense ligados e pareados, a janela mostrando um.

**Esta é a armadilha da casa, na forma mais pura:** *o instrumento mente mais
que o produto*. Um `grep` por três palavras que a cura não usou produziu uma
"prova de ausência" convincente e falsa. A régua correta é a que segue o dado do
daemon até a tela — e foi ela que achou.

**F-5: ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA.**

### Correção 2 — o F-6 sai de "NÃO CONFERIDO": duas partes pagas, uma aberta

| parte | estado | onde |
|---|---|---|
| **F-6(a)** a aba Estado afirma "Conectado · USB · 85%" com a mesa vazia | **ABERTO** | `src/hefesto_dualsense4unix/daemon/ipc_handlers.py:2756` diz, no próprio código, que a `ESTADO-QUE-MENTE-01` *"segue aberta neste mesmo payload"* |
| **F-6(b)** o toast *"Cor aplicada no controle"* | ENTREGUE EM CÓDIGO | `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py:54` — hoje é `"Cor enviada ao controle ({pct}% de brilho)"`, e `:29` registra por que a palavra mudou |
| **F-6(c)** `rumble_ff.plays` mudo justo no zero | ENTREGUE EM CÓDIGO | `src/hefesto_dualsense4unix/app/actions/rumble_actions.py:89-132` — a linha passou a falar no zero, com os seis casos escritos |

### Correção 3 — F-3, F-9 e F-10 pagaram uma PARTE do que o item pedia

Não é erro da nota acima: o que entrou entrou mesmo, e está bem citado. É
**escopo**. Relido contra o texto de origem da fila (seção 4), sobra pedaço em
cada um:

- **F-3.** A fila pedia duas coisas: o `WatchdogSec=0` **em vigor** (pago: o
  drop-in mais o portão que exige `^WatchdogSec=0$` exato) **e** que o
  diagnóstico soubesse distinguir *"cura no disco"* de *"cura em vigor"*. Esta
  segunda metade **continua aberta**: `grep` por `WatchdogUSec` em
  `scripts/doctor.sh` devolve **zero** — o único lugar do repositório que lê o
  valor efetivo é `scripts/retrato_do_estado.sh:83`, que é **instrumento**, não
  portão. Máquina curada e máquina que vai morrer continuam imprimindo o mesmo
  veredito no doutor.
- **F-9.** A cura cobriu a **regra nova** (a `72-...-uaccess`, instalada pelos
  dois caminhos). O item de origem, porém, fala das regras **82 e 83**:
  `assets/82-nintendo-pro-nosniff.rules:23-24` continua chamando
  `/usr/local/lib/hefesto-dualsense4unix/bt_nosniff_now.sh`, e esse script só é
  instalado pelo caminho **nativo** (`install.sh:1620`). As duas regras seguem
  viajando no `spec`, no `PKGBUILD` e no `package.nix` — quem instalar por
  pacote continua com a regra de pé e o alvo ausente.
- **F-10.** O portão ganhou uma seção nova e boa
  (`scripts/check_packaging_parity.sh:351`, o acesso da sessão aos nós de
  entrada), que é o portão do **F-8**. A lista do F-10 continua descoberta:
  units/timers/scripts de Bluetooth, os drop-ins de WirePlumber, o
  `hefesto-launch`, o `storm_watch.sh`, as dependências de tempo de execução
  (`bluez-tools`, `libopus0`), o **alvo** de uma regra-cola, e a assimetria
  inversa. As quinze seções do portão hoje estão listadas nos `echo "== ..."`
  do próprio arquivo, e nenhuma cobre esses pontos.

### A fila, recontada em 09/08 à noite

- **ENTREGUES EM CÓDIGO, aguardando a palavra dela:** F-1, F-4, **F-5**,
  **F-6(b)**, **F-6(c)**, F-8.
- **PARCIAIS:** F-3 (falta o doutor ler o valor em vigor), F-7 (o aviso ficou
  honesto, o `exit 0` de `install.sh:941` continua), F-9 (a regra nova está
  coberta; as 82 e 83 não), F-10 (ganhou o portão do F-8; a lista do F-10
  continua).
- **ABERTOS:** F-2, **F-6(a)**, F-11.

**Grau:** MEDIDO, por leitura de `caminho:linha` na árvore de trabalho de
09/08/2026 à noite — que é o que roda. **SEM PROVA**, como a nota acima já dizia,
para o efeito de qualquer um deles na máquina dela.
