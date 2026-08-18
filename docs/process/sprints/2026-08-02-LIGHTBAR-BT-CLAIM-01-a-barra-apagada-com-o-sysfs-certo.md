# LIGHTBAR-BT-CLAIM-01 — a barra apagada com o sysfs certo

> ## ATENÇÃO — CADUCOU EM 03/08/2026 — REFUTADA POR MEDIÇÃO NO HARDWARE
>
> **Não execute a cura deste documento: ela APAGA a lightbar.**
>
> A medição de 03/08, com dois DualSense no rádio e o olho dela confirmando cada
> cor, refutou os três pilares desta sprint:
>
> 1. **"o gatilho é o reinício do daemon"** — não é. Uma reconexão com o daemon
>    **vivo** não travou (evento 6 do estudo); outra, no mesmo minuto, travou. A
>    diferença é o `0x08`, não o daemon;
> 2. **"o `0x08` devolve o claim ao firmware e ninguém retoma"** — não
>    fatalmente. Enviado às 19:53:17 num controle **fora da janela** de 3,4 s, a
>    barra obedeceu à cor seguinte;
> 3. **a cura proposta na seção "A cura de RAIZ, mínima" APAGA a barra.** Ela
>    manda `common[41] = LIGHT_OUT`; o driver desta máquina diz, textualmente:
>    `report.common->lightbar_setup = DS_OUTPUT_LIGHTBAR_SETUP_LIGHT_OUT; /* Fade light out. */`.
>    Testado ao vivo: **nenhum efeito**.
>
> **A causa-raiz real:** o `0x08` enviado **dentro** da janela de ~3,4 s
> pós-conexão trava a barra até o power-off — correlação perfeita em 7 eventos.
> Ele foi acrescentado em 18/07 como a *cura* da lightbar por Bluetooth.
>
> Ver [LIGHTBAR-BT-CULPADO-01](2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md)
> e o estudo [a noite em que medimos a lightbar do Bluetooth](../estudos/2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md).
>
> **O documento fica inteiro, e não é por formalidade.** O método dele — as
> refutações medidas, a leitura do journal, as armadilhas nomeadas — continua
> correto e foi o que permitiu chegar à causa real. O que errou foi a
> conclusão. *O registro de uma cura errada vale tanto quanto o da certa.*

- **Status:** **REFUTADA em 03/08/2026** (ver o bloco acima). Status anterior:
  *diagnóstico fechado, cura proposta e não aplicada* — e ainda bem que não foi
  aplicada
- **Prioridade:** ALTA — ela encontrou usando, e o sintoma reaparece a cada
  reinício do daemon
- **Aberta por:** a medição de 02/08/2026, que **refuta** a nota de veredito da
  [BT-E-VPAD-01](2026-08-01-BT-E-VPAD-01-o-que-so-existe-no-cabo-e-os-seis-furos.md)
  (*"o defeito 2 não se reproduz"*) e refuta também a previsão escrita no
  comentário `LIGHTBAR-BT-RESET-03` (*"a barra ficaria apagada até a cor
  MUDAR"*) — a cor mudou e a barra continuou apagada
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)
- **Referência:** [o protocolo canônico](../../protocol/dualsense-referencia-canonica.md)

---

## O sintoma, na frase dela

Dois DualSense no Bluetooth ao mesmo tempo, e **as duas lightbars apagadas** —
enquanto o `multi_intensity` do kernel diz a cor certa, o valor **persiste**, os
gatilhos funcionam, os LEDs de jogador funcionam, e mandar uma cor nova pelo
IPC muda o sysfs sem acender nada.

Isso é pior do que "não escreve". É **escreve, gruda, e não acende**.

---

## O que está MEDIDO (02/08/2026, máquina dela)

### 1. O sysfs está certo e persiste

| nó | controle | transporte | `multi_intensity` | `brightness` | `trigger` |
|---|---|---|---|---|---|
| `input37:rgb:indicator` | `a0:fa:9c:00:00:f0` | **bt** | `255 0 0` | 255 | `[none]` |
| `input60:rgb:indicator` | `14:3a:9a:00:00:ab` | **bt** | `0 0 255` | 255 | `[none]` |
| `input79:rgb:indicator` | `02:fe:00:00:00:01` | vpad | `0 0 0` | 255 | `[none]` |
| `input84:rgb:indicator` | `02:fe:00:00:00:02` | vpad | `0 0 0` | 255 | `[none]` |

Escrita direta no sysfs pela usuária: o daemon **desfaz** (defesa contra
escritor estrangeiro, `NUMA-03`). Escrita via IPC `led.set` com `uniq`: o valor
**persiste**. Nos dois casos a barra continua apagada.

### 2. Os dois DualSense por BT são dispositivos `uhid`

```
/sys/class/leds/input37:rgb:indicator
  -> /sys/devices/virtual/misc/uhid/0005:054C:0CE6.0008
     HID_ID=0005:0000054C:00000CE6   (bus 0005 = Bluetooth)
     driver -> ../bus/hid/drivers/playstation
```

Ou seja: o `bluetoothd` (BlueZ ≥ 5.73, `BLUEZ-UHID-01`) cria o device por
`/dev/uhid`, o `hid-playstation` liga nele, e **toda** saída — a do kernel e a
nossa — sai por `uhid` → `bluetoothd` → L2CAP. Um caminho só, três escritores.

### 3. Os dois nós físicos de `hidraw` estão ESCONDIDOS pelo broker

```
crw-------  root root  /dev/hidraw7   (a0:fa:9c:00:00:f0)
crw-------  root root  /dev/hidraw8   (14:3a:9a:00:00:ab)
crw-rw----+ root root  /dev/hidraw4   (vpad P1, com ACL uaccess)
```

E no journal, a cada 30 segundos, sem parar:

```
15:47:47  [info] hidraw_broker_hidden  node=/dev/hidraw7
15:47:47  [info] hidraw_broker_hidden  node=/dev/hidraw8
```

O daemon segue escrevendo neles porque **já tinha o fd** e porque o
`make_broker_opener` recebe fd de root (`hidraw_broker_fd_recebido` no journal).
O daemon mantém **dois** fds RW por controle físico (o handle da pydualsense e o
espelho do `PhysicalReportReader`). **Isto não é a causa da barra apagada** — a
rota da cor é o sysfs, que não passa por `hidraw`. Mas é uma armadilha de
medição de primeira grandeza; ver "As armadilhas".

### 4. A linha do tempo de hoje — e ela é o achado

Do journal do dia, só as linhas que importam (boot às 13:39):

```
13:40:49  systemd: Started hefesto-dualsense4unix.service
13:40:52  controller_connected        transport=usb          <- 14:3a NO CABO
13:40:52  sysfs_led_cobertura         cobertos=['14:3a...']  <- SEM 0x08 (usb)
13:57:35  lightbar_reset_enviado      key=a0:fa...           <- a0:fa CONECTA por BT
13:57:35  lightbar_reassert_skip_cache  node=input37 rgb=(255,0,0)
              ^ este é o estado que a BT-E-VPAD-01 mediu de MANHÃ, ACESO

14:11:20  controller_primary_bound    transport=bt           <- o do cabo saiu
14:13:00  systemd: Stopped / Started                         <- REINÍCIO 1
14:13:01  lightbar_reset_enviado      key=a0:fa...           <- 0x08 num controle
                                                                adotado 16 min ANTES
14:15:05  systemd: Stopped / Started                         <- REINÍCIO 2
14:15:06  lightbar_reset_enviado      key=a0:fa...
14:21:54  lightbar_reset_enviado      key=14:3a...           <- 14:3a volta, agora por BT
14:40:19  systemd: Stopped / Started                         <- REINÍCIO 3
14:40:21  lightbar_reset_enviado      key=a0:fa...
14:40:21  lightbar_reset_enviado      key=14:3a...           <- 0x08 nos DOIS, os dois
                                                                adotados MUITO antes
14:42:27  lightbar_reassert_skip_cache  node=input37 rgb=(0,255,0)   <- verde dela
15:39:47  systemd: Stopped / Started                         <- REINÍCIO 4
15:39:49  lightbar_reset_enviado      key=a0:fa... e 14:3a...
```

**Leia de novo a coluna da direita.** O `0x08` ("Reset LED state") **não** é
enviado quando o CONTROLE chega. Ele é enviado quando **o nosso handle** é novo
— e todo reinício do daemon fabrica handles novos para controles velhos.

### 5. O que NÃO está acontecendo (refutações medidas)

- **Não é perda de pacote no ar.** O `discover()` fabrica uma instância NOVA de
  `SysfsLedNode` a cada `_refresh_sysfs_leds` (`core/sysfs_leds.py:301-318`),
  e o mapa inteiro é substituído (`core/backend_pydualsense.py:1834`). Cache
  novo = vazio = o `reassert_resolved_outputs` **reescreve de verdade a cada
  reconciliação** (≤ 30 s, `backend_pydualsense.py:1636`). De 14:40 até agora
  são mais de cem escritas reais, cada uma agendando um output report de
  lightbar no kernel. Perda estocástica não erra cem de cem;
- **não é a fila do `uhid` estourando.** O `dmesg` inteiro não tem nenhuma
  linha `Output queue is full`;
- **não é o nó de sysfs faltando** (que era a causa de 01/08): o
  `sem_no_sysfs` sai **vazio** em todas as coberturas de hoje;
- **não é `_output_mute`** (Modo Nativo): se fosse, nem o `0x08` nem o priming
  teriam saído — e os dois saíram, no mesmo milissegundo.

---

## A causa-raiz

> **O `0x08` devolve o claim da lightbar ao firmware, e do lado do host ninguém
> volta a tomá-lo — porque quem toma a barra é o `lightbar_setup`, e o kernel só
> o manda UMA vez por conexão, no probe. O nosso `0x08` é disparado pela novidade
> do HANDLE, não pela novidade do CONTROLE; por isso todo reinício do daemon
> solta uma barra que o kernel já tinha tomado, e nada a retoma.**

A prova de cada elo:

1. **O `0x08` é RELEASE, não TAKE.** `VALID_FLAG1_RELEASE_LEDS = 0x08`
   (`core/ds_output_report.py:165`). O report que mandamos tem **só** esse bit:
   `common[1] = VALID_FLAG1_RELEASE_LEDS`, todo o resto zerado
   (`core/lightbar_reset.py:48-50`) — de propósito, e está escrito lá: *"não
   toca rumble, gatilhos, player LEDs nem cor; só devolve o claim da lightbar
   ao host"*. Devolver não é tomar.

2. **Quem TOMA a barra é o `lightbar_setup`, e ele é one-shot.** A própria
   árvore documenta, em `core/ds_output_report.py:184-189`:

   > bit1 (kernel `DS_OUTPUT_VALID_FLAG2_LIGHTBAR_SETUP_CONTROL_ENABLE`):
   > habilita o SETUP da lightbar (`common[41]` = fade-in/fade-out). **O kernel
   > o usa UMA vez por conexão (opcode 2 = LIGHT_OUT) para tomar a barra**;
   > mantê-lo engatado em regime (keepalive) trava a exibição no firmware — ver
   > `LIGHTBAR-BT-KEEPALIVE-01`.

   "Uma vez por conexão" quer dizer: no probe do `hid-playstation`, e **nunca
   mais** enquanto o device existir. Depois disso o kernel só manda
   `LIGHTBAR_CONTROL_ENABLE` + RGB — que escreve os registradores de COR, não o
   registrador de POSSE.

3. **Nós nunca mandamos o setup.** `_build_common` **apaga** o bit sob
   supressão (`core/backend_pydualsense.py:713-716`), e por BT a supressão é
   permanente (`LIGHTBAR-BT-NEVER-01`, `backend_pydualsense.py:1789-1795`).
   Correto para o keepalive — e é justamente por isso que, depois de um
   `0x08`, **não existe no processo inteiro nenhum caminho que retome a barra.**

4. **O gatilho do `0x08` é o handle, não o controle.** `adopt_candidates` sai de
   `new_handles` (`backend_pydualsense.py:1524-1526`), que é a lista dos handles
   abertos NESTE `connect()`. Num reinício do daemon, todo controle conectado é
   um handle novo. A linha do tempo mostra isso quatro vezes.

5. **E isso explica o que JÁ funcionava** — que é a regra desta casa:
   - **USB nunca teve o problema:** o cabo não tem o claim (dito desde
     `LIGHTBAR-BT-RESET-01`, `core/lightbar_reset.py:1-24`);
   - **13:57 funcionou** porque o `0x08` chegou colado no probe do kernel: o
     firmware ainda estava na janela da animação de ligar (a mesma janela de
     ~3,4 s que o comentário `LIGHTBAR-BT-ADOPT-01` já nomeava), o reset
     encerrou a animação, e a cor seguinte colou. Foi essa a configuração que a
     BT-E-VPAD-01 mediu de manhã e chamou de "não reproduz";
   - **as curas de 17-22/07 sempre foram medidas logo depois de um connect
     fresco** — nunca depois de um reinício do daemon com o controle já adotado.
     Por isso passaram, e por isso a regressão levou duas semanas para aparecer.

**Grau de confiança:** a correlação da linha do tempo é **ALTA** (quatro
reinícios, dois controles, e o sintoma só existe depois deles). O mecanismo
interno do firmware — "o `0x08` recolhido fora da janela devolve a barra para
uma máquina de estados que ninguém mais aciona" — é **MÉDIA-ALTA**: é a única
hipótese que sobrevive a todas as refutações acima, mas não foi medida
diretamente. O experimento abaixo mede.

---

## O experimento que decide (dez segundos, sem tocar em código)

Faça **nesta ordem**, com as duas barras apagadas:

1. **Desligue e ligue UM controle** (segurar PS por ~10 s, depois PS de novo).
   Ele re-enumera, o kernel faz o probe e manda o `LIGHT_OUT`, o daemon o adota
   como handle novo e manda o `0x08` dentro da janela.
   → **Previsão: a barra desse controle ACENDE.** O outro segue apagado.
2. Sem tocar em mais nada, **reinicie o daemon**
   (`systemctl --user restart hefesto-dualsense4unix.service`).
   → **Previsão: a barra que acabou de acender APAGA de novo**, no segundo do
   `lightbar_reset_enviado`, e o `multi_intensity` continua com a cor certa.

Se as duas previsões baterem, a causa-raiz está provada e a cura abaixo é a
certa. Se a (1) falhar, o latch é mais fundo (sobrevive à re-enumeração) e a
cura passa a ser a de (b) na lista abaixo. Se a (2) falhar, o `0x08` é inocente
e o achado volta para a mesa.

**Enquanto isso não for medido, nada disso vira código.**

---

## As três perguntas do log, respondidas

### 1. Por que o `skip_cache` saiu 3,7 ms DEPOIS do reset, se o `RESET-03` existe para invalidar o cache?

Porque o `RESET-03` **é um no-op por construção**, em dois níveis:

```
backend_pydualsense.py:1542-1546
    with self._io_lock:
        node = self._sysfs.get(_key)      # <- o mapa AINDA É O ANTIGO
    if node is not None:
        node.invalidate_cache()           # <- num objeto que vai ser DESCARTADO
```

- **num reinício do daemon, `self._sysfs` está VAZIO** (`backend_pydualsense.py:927`),
  então `node` é `None` e o `invalidate_cache()` **nunca roda**. Foi exatamente o
  caso de 14:40:21 e de 15:39:49;
- e mesmo quando não está vazio, o objeto devolvido morre 70 linhas depois:
  o `_refresh_sysfs_leds()` (linha 1620) chama `sysfs_leds.discover()`, que
  **constrói uma instância nova de `SysfsLedNode` por nó, a cada chamada**
  (`core/sysfs_leds.py:301-318`), e a linha 1834 troca o mapa inteiro. O
  `reassert` da linha 1636 lê o mapa NOVO. **O objeto invalidado e o objeto
  lido nunca são o mesmo.** O mesmo vale para o irmão do `RESET-02`
  (linhas 1612-1614).

Então de onde veio o `skip_cache`? Da **escrita dupla dentro do mesmo passe**:

1. `_refresh_sysfs_leds` vê a chave como nova (linha 1810-1814) e faz o priming:
   `node.set_rgb(*cor)` (linha 1828) → `_last_write = ((255,0,0), 255)`;
2. o `reassert_resolved_outputs` (linha 1636) chama `set_rgb` **no mesmo objeto,
   com a mesma cor** → bate no cache (`core/sysfs_leds.py:183`) → loga o skip
   (linhas 197-201).

**Ou seja: a escrita ACONTECEU** (foi o priming), e o skip só engoliu a segunda
cópia dela. É por isso que o `multi_intensity` está certo. **O `skip_cache` é
uma pista falsa** — não é ele que mantém a barra apagada.

Um efeito colateral que precisa ficar registrado: como as instâncias são
refeitas a cada tick, **o cache do `GUERRA-01` nunca sobrevive entre
reconciliações** — na prática o daemon reescreve a cor nos dois nós a cada
≤ 30 s. Isso é o que permitiu refutar a hipótese de perda de pacote (item 5 dos
medidos), mas quer dizer que o "flash azul de 30 s" só não volta porque a cor
reescrita é a resolvida, e não o azul.

### 2. Como um cache pula uma escrita cujo valor MUDOU de (255,0,0) para (0,255,0)?

Não pula. A comparação não é "a cor mudou?", é
`self._last_write == wanted` (`core/sysfs_leds.py:182-183`) — o último valor
que **aquela instância** escreveu com sucesso. A sequência de 14:42:27 foi:

1. `led.set` com `uniq` → `_apply_por_uniq` → `apply_output_for`
   (`backend_pydualsense.py:2639-2641`) → `_write_partial_output` →
   `node.set_rgb(0,255,0)` (linha 2136). **Escreveu de verdade** — e é por isso
   que o sysfs foi para `0 255 0`. `_last_write` vira verde;
2. o handler chama `reassert_resolved_outputs()` logo em seguida
   (`daemon/ipc_handlers.py:728-730`), que faz `set_rgb(0,255,0)` **no mesmo
   objeto** → cache-hit → log.

O `rgb=(0,255,0)` do log é a cor da **segunda** escrita, não a de uma escrita
suprimida. E a linha reaparece com cor nova (em vez de ficar muda para sempre)
porque o `_skip_logged` (`core/sysfs_leds.py:65`, 202) é por instância — e as
instâncias são refeitas a cada tick.

### 3. Por que `reclamar=False`? E quando `should_reclaim_on_wake` daria True?

`core/lightbar_reset.py:116-122` só devolve `True` quando as quatro condições
valem ao mesmo tempo: `transport == "bt"`, `desired_rgb` existe e é diferente do
default do kernel, `current_sysfs_rgb` é legível, e
**`current_sysfs_rgb == KERNEL_DEFAULT_BLUE (0,0,128)`**.

O log mediu `current=(255,0,0)`. Não é o azul-default. Fim.

**E essas condições são alcançáveis nesta máquina?** Praticamente não:

- a classe LED só volta a `(0,0,128)` quando o kernel refaz o probe — e um
  probe novo cria um `inputN` novo, ou seja, um `indicator_dir` novo;
- mas o laço do reclaim roda **ANTES** do `_refresh_sysfs_leds`
  (linhas 1577 e 1620), lendo o mapa do tick anterior: com o nó recriado, o
  `node.get_rgb()` do nó velho devolve `None` (arquivo sumiu,
  `core/sysfs_leds.py:106-110`) e a guarda da linha 121 corta em `False`;
- e se por acaso o `inputN` fosse o mesmo, o priming/reassert do tick anterior
  já teria reposto a cor resolvida por cima do azul.

Isto é **exatamente** o que o comentário `L-01` da auditoria de 21/07 já
antecipava, dentro do próprio código (`backend_pydualsense.py:1588-1597`):
*"o estudo W12 sugere que ele NÃO reescreve em parte dos casos, então a
assinatura pode nunca casar"*. **Casou nunca.** O `RESET-02` é código morto em
regime, e o `lightbar_reclaim_avaliado` de hoje é a instrumentação dele
cumprindo o papel para que foi escrita: provar que o gatilho não dispara.

### 4. Os DOIS por BT, o broker, o vpad e o co-op fazem o firmware perder o dono?

**Não pelo caminho que a pergunta supõe, e a diferença importa.**

- **o broker `hide-hidraw`** deixa `/dev/hidraw7` e `/dev/hidraw8` em
  `0600 root:root` a cada 30 s, mas **a cor não passa por `hidraw`** — passa
  pela classe LED do kernel. O esconde-esconde não tem como apagar a barra. E
  o daemon continua escrevendo: o fd já estava aberto, e o
  `make_broker_opener` recebe fd de root para os que faltam;
- **o vpad** tem nó de LED próprio (`input79`/`input84`, ambos em `0 0 0`) e
  não compartilha registrador nenhum com o físico;
- **o co-op** publica cor e LED de jogador por slot e entra no mesmo reassert
  (`R-13`) — é ele que troca o `a0:fa` entre vermelho e azul conforme o número
  de jogadores, o que aparece na linha do tempo e **não** é defeito;
- **"dois por BT" é coincidência do momento, não a condição.** A condição real é
  *reinício do daemon com o controle já adotado*. O primeiro a apagar foi o
  `a0:fa` às 14:13, quando ele era o **único** controle da máquina.

O que os dois por BT fazem de verdade é **dobrar a chance de o reinício pegar
alguém adotado** — e por isso o sintoma parece ligado a eles.

---

## A cura proposta — o que é raiz e o que é gambiarra

### A cura de RAIZ, mínima (recomendada)

**Depois de soltar, TOME de volta.** Onde hoje está

```
backend_pydualsense.py:1533-1546   if send_release_leds(handle): ...
```

o `0x08` precisa ser seguido, **no mesmo handle e no mesmo instante**, de um
único `0x31` bem-formado que refaça o que o kernel faz no probe: `valid_flag2`
com `VALID_FLAG2_LIGHTBAR_SETUP_CONTROL_ENABLE` (`core/ds_output_report.py:189`)
e `common[41] = LIGHT_OUT`, seguido da cor resolvida com
`VALID_FLAG1_LIGHTBAR_CONTROL_ENABLE`. O construtor já existe
(`build_bt_report`, `core/ds_output_report.py:221-235`) e o envelope BT já é o
correto desde o `BTREPORT-02` — falta só o report novo em
`core/lightbar_reset.py`, irmão do `build_bt_release_leds_report`.

Por que é raiz e não contorno: restaura o invariante que o sistema tinha e
perdeu — *"depois de toda adoção, alguém do lado do host é dono da lightbar"*.
Hoje a adoção **solta** e ninguém pega.

Isto **não desfaz** nenhuma cura de 17-22/07 e **não** afrouxa o
`LIGHTBAR-BT-NEVER-01`: aquilo proíbe o `0x31` **malformado** da pydualsense
0.7.5 em regime; isto é um report bem-formado, **um só**, na borda da adoção —
a mesma disciplina que o `LIGHTBAR-BT-KEEPALIVE-01` exige (*"o kernel o usa uma
vez por conexão"*; mantê-lo engatado é que trava).

### A cura complementar, também de raiz

**Parar de mandar o `0x08` quando ele não pode ajudar.** O gatilho certo não é
"handle novo" (`backend_pydualsense.py:1524-1526`), é "o **controle** acabou de
aparecer". Um reinício do daemon não é uma conexão nova de Bluetooth. O sinal
honesto ainda precisa ser escolhido, e há duas opções com preços diferentes:

- **(a)** o sinal que o SDL usa para decidir quando o reset de LED pode sair —
  **precisa ser lido no fonte da SDL3 que a Steam distribui**, e não na
  `libSDL2` do Ubuntu (é a lição de método de 01/08, e ela já custou um alarme
  falso inteiro nesta casa);
- **(b)** a idade do device HID no `sysfs`, que é barata mas frágil.

Com a cura de cima aplicada, esta vira otimização (deixa de mandar dois reports
inúteis por reinício), não requisito.

### O que seria contorno, e a casa reprova

- **mexer no cache do `sysfs_leds` para "forçar a reescrita"**: já está provado
  acima que a escrita acontece e não adianta. Pior: fazer a instância
  sobreviver entre ticks (o que "consertaria" o `RESET-03` de verdade)
  **pararia** a reescrita de 30 s que hoje existe por acidente, e é uma
  regressão silenciosa;
- **reenviar o `0x08` por timer**: o próprio `RESET-02` já proíbe, com motivo
  (`core/lightbar_reset.py:105-107`) — pisca a barra de quem está bem;
- **religar a escrita de LED da pydualsense por BT**: `LIGHTBAR-BT-NEVER-01`,
  pago com a barra latcheada até o power-off. Não.

### E a tela, que continua mentindo (defeito 3 da BT-E-VPAD-01)

Independente da cura: o `multi_intensity` **não é a verdade do hardware** — está
escrito no próprio código (`core/sysfs_leds.py:92-105`, `STATUS-01`). Enquanto
a barra apagada for indistinguível de barra acesa para o daemon, a tela precisa
dizer *"mandamos esta cor"* e não *"esta cor está no controle"*. O defeito 3
segue aberto e ganhou, hoje, a prova mais forte que já teve.

---

## Testes que reprovariam a cura (e um que a atrapalha)

- `tests/unit/test_lightbar_reset.py` — a família inteira do `send_release_leds`
  e do `should_reclaim_on_wake`;
- `tests/unit/test_lightbar_reset.py:122-129` —
  **`test_connect_chama_should_reclaim_on_wake` é um teste-muralha**: ele lê o
  **texto-fonte** de `backend_pydualsense.py` e exige as strings
  `should_reclaim_on_wake` e `lightbar_reset_reenviado_wake`. Quem for aposentar
  o `RESET-02` (que esta sprint mostra ser código morto) **tem de encarar esse
  teste primeiro** — ele trava a correção, que é a definição de muralha;
- `tests/unit/test_ds_output_report.py` — o layout/CRC do `0x31`, que o report
  novo tem de respeitar byte a byte;
- `tests/core/test_sysfs_leds.py:164-172` —
  `test_invalidate_cache_forca_a_proxima_escrita` cobre o `invalidate_cache`
  **isolado**. Note o buraco: **não existe teste nenhum ligando o
  `invalidate_cache` ao `connect()`** — foi assim que a metade "cache" do
  `RESET-03` viveu duas semanas sendo um no-op sem ninguém notar. A mordida que
  falta é essa, e ela precisa nascer junto com a cura.

A mordida da cura nova, para não repetir o erro: **arrancar o report de retomada
e ver o teste reprovar** — um teste que só afirma que o report foi *montado* não
prova nada; ele tem de afirmar que o report saiu **pelo mesmo handle** e
**depois** do `0x08`.

---

## As armadilhas desta investigação (todas custaram tempo hoje)

1. **`/dev/hidraw7` e `/dev/hidraw8` dão `EACCES` para ela.** O broker os deixa
   em `0600 root:root` a cada 30 s. Qualquer instrumento que faça
   `open("/dev/hidraw7")` como usuária vai reportar "sem dispositivo" e parecer
   defeito do produto. Use o broker (`make_broker_opener`) ou `sudo`;
2. **o `multi_intensity` NÃO é a verdade do hardware.** É a memória do último
   valor escrito **via classe LED**. Ler `255 0 0` ali e concluir "está
   vermelha" é o erro central deste defeito — e é o que a tela ainda faz;
3. **`lightbar_reassert_skip_cache` parece a causa e não é.** Ele marca a
   *segunda* escrita do mesmo passe. Quem procurar "por que pulou a escrita"
   vai investigar o cache por horas e não achar nada, porque a escrita
   aconteceu;
4. **o `zsh` come `:r`.** `$n:rgb:indicator` expande errado (modificador de
   parâmetro); use `${n}:rgb:indicator`. Perdi uma medição inteira nisso;
5. **o `dmesg` desta máquina ROTACIONA em poucas horas** — o `nintendo` inunda o
   anel com "compensating for N dropped IMU reports". Procurar mensagem de boot
   ali não funciona; o journal do usuário, sim (guarda desde 21/07);
6. **o instrumento pode estar brigando com o produto** (armadilha 3 do
   `CLAUDE.md`): escrever no sysfs à mão para "testar" faz o daemon desfazer em
   ≤ 30 s pela defesa de escritor estrangeiro, e o resultado parece do
   firmware.

---

## O que fica ABERTO

- **A medição de dez segundos** (a seção "O experimento que decide"). Sem ela a
  cura não sai — e ela exige a mão dela nos controles;
- **o defeito 3 da BT-E-VPAD-01** (a tela que afirma o que não mediu). Esta
  sprint dá a prova, não a cura;
- **a hipótese 1 de 01/08** — o nó de sysfs que às vezes não existe no BT
  (`sem_no_sysfs=['a0:fa:9c:00:00:f0']`) — **continua aberta e é OUTRO defeito**.
  Hoje o nó existe em todas as coberturas; aquilo é uma corrida, e vai voltar;
- **o sinal do SDL3** para decidir a janela do `0x08` (opção (a) da cura
  complementar): não medido, e só pode ser medido contra a SDL3 que a Steam
  distribui;
- **o `RESET-02` como código morto.** A casa não apaga decisão medida — então
  ele não sai por esta sprint; sai com a nota datada e com o teste-muralha
  encarado, quando a cura de raiz tornar o gatilho dele desnecessário.

---

## Nota para a BT-E-VPAD-01

A nota de veredito daquela sprint (*"o defeito 2 NÃO se reproduz"*) **caducou na
mesma tarde**, e a própria nota já registra isso e aponta para cá. O que ela
mediu de manhã continua verdadeiro: com um controle no cabo e outro no BT,
recém-conectado, a barra do BT **acende**. O que caducou é a generalização —
porque o que decide não é o transporte do vizinho, é **há quanto tempo aquele
controle foi adotado quando o daemon reiniciou**.
