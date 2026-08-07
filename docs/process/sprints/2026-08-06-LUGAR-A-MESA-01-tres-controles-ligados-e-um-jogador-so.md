# LUGAR À MESA-01 — três controles ligados, e um jogador só

- **Status:** **PARCIALMENTE EM EXECUÇÃO** desde 07/08/2026 — ver a nota do
  cabeçalho abaixo. Escrita em 06/08 como proposta; commitada em `a68c04e`
- **Prioridade:** ALTA — é a queixa dela desta noite, medida ao vivo com os
  aparelhos na mesa, e o defeito de honestidade atinge **qualquer pessoa que
  ligue um controle de outra marca**, não só esta bancada
- **Faixa:** 2 — o produto se contradiz. E, no caso do LED, ele **afirma**
- **Causa-raiz:** **PROVADA no código** (três contabilidades, duas se falam)
- **Depende de decisão dela:** SIM. Ver *"O VETO"* — a entrega que fecha a
  queixa literal **reabre o `8BIT-02` por escrito**, e isso é dela
- **Fecho de tela:**
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)

> ### **DUAS PERGUNTAS QUE SÓ ELA RESPONDE**, e vêm antes do código
>
> 1. **Ela quer que controle de outra marca vire jogador de verdade** (gamepad
>    virtual próprio, como os DualSense já têm) — sabendo que quem segurar o
>    Nintendo vai ver desenho de botão de PlayStation na tela do jogo?
> 2. **Enquanto isso não existe, o Hefesto deve continuar acendendo número
>    nesses controles?** Hoje ele acende "jogador 2" no Pro Controller, e o
>    jogo trata os três como jogador 1.
>
> Sem a resposta 1, esta sprint para na E1. Sem a resposta 2, a E0 não sabe se
> conserta a boca ou se cala a lâmpada.

> ### **RESPOSTA DA PERGUNTA 1 — 07/08/2026. A 2 SEGUE ABERTA.**
>
> **Grau: DECISÃO DELA**, registrada em
> [as onze respostas do painel](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md).
>
> **Pergunta 1: sim, mas SÓ DEPOIS da máscara por controle.** Ela não recusou a
> entrega — recusou **o preço**: o botão de PlayStation na tela do jogo para
> quem segura o Pro Controller. A `MASCARA-01` deixa de ser sprint paralela e
> vira **pré-requisito** da `E3`. A ordem passa a ser
> `MASCARA-01` → `E3` → `E4`.
>
> O veto do `QUATRO-NO-RÁDIO-01` e a decisão dela de 19/07 (*"externo não ganha
> controle virtual"*) **não foram derrubados — foram adiados com condição**.
> Enquanto a máscara não existir, valem. Quem retomar: **não comece a adoção.**
>
> **Pergunta 2 continua sem dona.** Ela não foi feita no painel de 07/08, e a
> resposta 1 não a decide: adiar a adoção não diz o que a lâmpada deve fazer
> enquanto isso. A `E0` fica presa nela — é escolher entre *calar a luz* (honesto,
> mas ela perde o instrumento pelo qual distingue os controles) e *manter o
> número com a boca da tela corrigida* (ela mantém o instrumento, e o plástico
> segue afirmando o que o jogo não cumpre).
>
> **O que JÁ foi feito sem depender dela**, porque não toca a lâmpada: a `E0a` —
> o `coop status` passou a imprimir os dois números nomeados, e existe teste que
> impede dois aparelhos de acenderem o mesmo jogador.

---

## A queixa dela, palavra por palavra

Em 06/08/2026, com os controles ligados:

> *"pro Controller e o 8bitdo e o dualsense todos conectados e todos no player 1"*

Ela não estava lendo a janela. Ela estava **jogando**, e viu os três aparelhos
disputarem o mesmo jogador dentro do jogo.

---

## A medição ao vivo, inteira — 06/08/2026, 21h08

**GRAU: MEDIDO.** Esta é a medição entregue, com os aparelhos na mesa dela.
Nenhum endereço aparece abaixo: os aparelhos são citados por nome e os
fabricantes por OUI público (Sony, Nintendo, 8BitDo).

### O inventário físico, confirmado por ela

**UM** 8BitDo (com dois modos: PS4 e Pro Controller), **UM** Pro Controller
Nintendo genuíno, **DOIS** DualSense. **Quatro controles.**

Na mesa no momento da medição: 1 DualSense + 1 Pro Controller + 1 8BitDo (o
segundo DualSense desligado). **Três ligados.**

### O que o kernel vê (hidraw)

| nó | nome | id |
|---|---|---|
| `hidraw2` | `Wireless Controller` | `0005:054C:05C4` — o 8BitDo em modo PS4 |
| `hidraw3` | `DualSense Wireless Controller (Hefesto P1)` | `0003:054C:0DF2` — o vpad do Hefesto |
| `hidraw6` | `DualSense Wireless Controller` | `0005:054C:0CE6` — o DualSense físico |
| `hidraw7` | `Pro Controller` | `0005:057E:2009` — o Pro Controller |

### O que o JOGO veria (nós com handler `js*`)

```
DualSense Wireless Controller (Hefesto P1)     <- o vpad
DualSense Wireless Controller                  <- o FÍSICO, que deveria estar escondido
Wireless Controller                            <- o 8BitDo
(o Pro Controller NÃO aparece como js)
```

### O que o Hefesto acha que tem

```
hefesto-dualsense4unix controller list  ->  "Controle 1 — BT"      (UM SÓ)
hefesto-dualsense4unix coop status      ->  "jogadores ativos: 1"  (com TRÊS ligados)
```

### O registro de ordem (`controllers.json`, versão 3)

| lugar | espécie | quem é |
|---|---|---|
| `rank=1` | `dualsense` | o outro DualSense, **desligado agora** |
| `rank=2` | `dualsense` | o DualSense ligado |
| `rank=3` | `external` | Pro Controller (OUI Nintendo `e0:f6:b5`) |
| `rank=4` | `external` | 8BitDo, **rosto A** (OUI 8BitDo `e4:17:d8`) |
| `rank=5` | `external` | 8BitDo, **rosto B** (mesmo OUI) |

**CINCO entradas para QUATRO controles.**

### O daemon NUMERA os externos, e não os CONTA

```
journal: external_led_written hidraw=/dev/hidraw2 slot=3   <- 8BitDo
journal: external_led_written hidraw=/dev/hidraw7 slot=2   <- Pro Controller
```

Os dois **ganham número de jogador aceso no plástico**, e o `coop status` diz
"1 jogador" no mesmo instante.

### Uma segunda medição, feita FORA da entregue

**GRAU: MEDIDO POR LEITOR, e reproduzido de forma independente por um segundo
leitor. Leitura read-only (`python-evdev`, `/sys/class/input`,
`/proc/bus/input/devices`, `busctl get-property`). Não faz parte da medição
entregue e deve ser reconfirmada quando os quatro voltarem à mesa.**

A **forma do eixo** de cada aparelho, que ninguém tinha olhado:

| aparelho | ABS_X/Y/RX/RY | ABS_Z / ABS_RZ | zona morta declarada |
|---|---|---|---|
| DualSense físico (`054c:0ce6`) | 0..255 | presentes, 0..255 | 0 |
| vpad do Hefesto (`054c:0df2`) | 0..255 | presentes, 0..255 | 0 |
| **8BitDo modo PS4** (`054c:05c4`) | **0..255** | **presentes, 0..255** | 0 |
| **Pro Controller** (`057e:2009`) | **-32767..32767** | **AUSENTES** | **flat=500** |

E o `Modalias` que cada um declara ao BlueZ:

| aparelho | Modalias |
|---|---|
| DualSense (OUI Sony) | `usb:v054Cp0CE6d0100` |
| **8BitDo modo PS4** (OUI 8BitDo) | `usb:v054Cp05C4d0100` |
| Pro Controller (OUI Nintendo) | `usb:v057Ep2009d0001` |

Os três gamepads reportam `Class = 9480` idêntico.

---

## A MENTIRA NA TELA — e ela não está na tela, está no plástico

**Este é o achado que os três juízes independentes destacaram, e é o que esta
sprint registra com destaque.**

> **Hoje o produto acende, no plástico, um indicador de JOGADOR 2 e de JOGADOR 3
> em controles que o próprio co-op não conta como jogadores — e que o jogo trata
> como jogador 1.**

O caminho, medido linha a linha:

1. `daemon/subsystems/external_identity.py:1213-1219` escreve e registra
   `external_led_written slot=N`;
2. quem executa é `core/external_leds.py:314` (`apply_player_number`), e o
   efeito **físico depende do modo**:
   - **Pro Controller** cai em `write_player_number`
     (`core/external_leds.py:98`): é a **barra de LEDs de jogador**, o padrão
     Nintendo de N verdes à esquerda. **Isto é literalmente um indicador de
     jogador.** A pessoa lê "jogador 2" porque o hardware existe para dizer
     exatamente isso;
   - **8BitDo em modo PS4** cai em `write_lightbar_slot`
     (`core/external_leds.py:291`): é a **lightbar RGB na cor do slot**
     (1=azul, 2=vermelho, 3=verde, 4=rosa — a mesma paleta dos DualSense).
     Não é uma barra de jogador; é a cor que, nesta casa, significa jogador N.
     **Correção contra a medição entregue:** dizer "LED de jogador 3 no 8BitDo"
     é impreciso — o que acende é a **cor do jogador 3**. A mentira é a mesma;
     o mecanismo é outro, e ele importa para quem for testar;
3. ao mesmo tempo, `daemon/subsystems/coop.py:191-193` responde
   `player_count() = 1 + len(self._players)` — **1**;
4. e `grep -c external` em `daemon/subsystems/coop.py` devolve **0**.

**Por que isto é pior que um número errado numa janela:** a janela ela pode não
estar olhando. O plástico está na mão dela. A casa já tem registrado que *ela
distingue os controles pela COR da luz e pelo LED de jogador*
(`app/actions/home_actions.py:13`). O instrumento que ela lê primeiro é o que
está mentindo, e nenhuma frase de tela reescreve uma afordância de hardware.

**Consequência de método, e ela reordena as entregas:** qualquer entrega que
conserte só a boca da tela **não fecha o critério da queixa**. Está escrito nas
entregas abaixo, e é o principal enxerto que os juízes obrigaram.

---

## A causa, confirmada no código: são TRÊS contabilidades, e só DUAS se falam

**GRAU: MEDIDO.** Conferido na árvore de 06/08/2026 (`ae32c10`).

### 1. O co-op — a contabilidade que conta JOGADORES

| pergunta | resposta | caminho:linha |
|---|---|---|
| o que entra em `_players` | só o que sai de `discover_dualsense_evdevs()`, menos o primário | `daemon/subsystems/coop.py:333-337` |
| `player_count()` | `1 + len(self._players)`; **nunca** consulta externo nenhum | `daemon/subsystems/coop.py:191-193` |
| `should_be_active()` | `coop_enabled` **e** `_gamepad_device is not None` | `daemon/subsystems/coop.py:183-189` |

O bloqueio duro, na letra:

```python
# daemon/subsystems/coop.py:333-337
want = {
    mac: str(path)
    for mac, path in discover_dualsense_evdevs().items()
    if mac != primary
}
```

E `discover_dualsense_evdevs` (`core/evdev_reader.py:130`) filtra em
`core/evdev_reader.py:165-168` por `DUALSENSE_VENDOR = 0x054C` e
`DUALSENSE_PIDS = {0x0CE6, 0x0DF2}` (`core/evdev_reader.py:28-29`).

### 2. O registro de externos — a contabilidade que NUMERA e ACENDE

- **Lugar na fila (`rank`):** `ExternalIdentityRegistry.slot_for`
  (`daemon/subsystems/external_identity.py:473`), gravado no `controllers.json`
  com `kind=external`;
- **Número exibido/aceso:** **não é o rank.** `_posicao_locked`
  (`daemon/subsystems/external_identity.py:455`) devolve a **colocação entre os
  presentes da mesa**, DualSense inclusive;
- **Quem escreve o LED:** `ExternalLedSync.tick`
  (`daemon/subsystems/external_identity.py:1099`), no pool `hefesto-ext`, com
  cache por valor e limite de taxa.

**A derivação bate com o journal dela** (GRAU: MEDIDO no código, casa com a
medição entregue): com um DualSense presente (rank 2) e o Pro em rank 3, o Pro
tem `antes = 0 externos à frente + 1 DualSense presente` = **posição 2**; o
8BitDo (rank 4) tem `antes = 1 externo + 1 DualSense` = **posição 3**. É
exatamente o `slot=2` (hidraw7) e o `slot=3` (hidraw2) do journal.

**O caminho de externos não põe ninguém no player 1. Ele acerta.** O "todos no
player 1" não nasce aqui — nasce no que o jogo enxerga.

### 3. O registro de identidade — a fila ÚNICA, que já conta os dois

`ControllerIdentityRegistry.slot_for` (`daemon/subsystems/identity.py:543`) já
devolve a colocação entre os presentes **contando externos**, via
`set_external_presence_provider` (`daemon/subsystems/identity.py:523`), fiado
por `ExternalLedSync._wire_presence_providers`
(`daemon/subsystems/external_identity.py:961`).

### Os pontos de encontro — três, e todos de mão única para o que importa

- **A** — `daemon/subsystems/external_identity.py:993` (`_ds_reserve`): o
  externo **lê** `coop.player_count()` para não colidir. O co-op nunca lê de
  volta;
- **B** — `daemon/subsystems/external_identity.py:961`: mão dupla **de
  presença**, e só de presença. Serve à **exibição**, nunca à contagem de
  jogadores;
- **C** — `daemon/subsystems/coop.py:1019` (`_numero_exibido`): o co-op consulta
  a fila única para decidir **que número acender**, e continua sem saber dos
  externos **para contar jogadores**.

**É a assimetria exata da queixa: o co-op sabe dos externos o suficiente para
acender a lâmpada certa, e não o suficiente para contá-los.**

### E o dado certo existe, publicado, sem um único leitor

`daemon/ipc_handlers.py:1843-1849` publica `coop.externals` desde 25/07
(EXT-COUNT-01), com o comentário que já diz a doutrina inteira: *"o número certo
não é inflar `players`: é dizer os dois"*.

`grep` por consumidores em `src/`, `packaging/` e `tests/`: **zero**.
`cli/cmd_coop.py:125-126` lê `coop["players"]` e imprime `jogadores ativos: N`.
Nunca lê `coop["externals"]`. **Doze dias de campo publicado e mudo.**

---

## O achado do 8BitDo que se declara Sony

**GRAU: MEDIDO.**

O 8BitDo em modo PS4 se apresenta com **VID `054C` (Sony)** e **PID `05C4`
(DualShock 4)**. Ele não se declara genérico — **ele se declara Sony**.

O que o projeto faz com esse par, e são **seis decisores independentes**:

| onde | o que faz com `054c:05c4` |
|---|---|
| `core/evdev_reader.py:28-29` + `:423-426` | `05C4` não está em `DUALSENSE_PIDS`, então **não** é excluído do inventário de externos. É aqui que "Sony ou externo" de fato se decide — e ele é excluído do co-op **pelo PID, não pelo fabricante**: passa a um octeto de entrar |
| `broker/hidraw_broker.py:109`, `:200` | só aceita `054c:0ce6`; o hidraw do 8BitDo é **rejeitado**. Correto |
| `app/actions/external_controllers.py:27-38` | `_TYPE_BY_VIDPID` **não tem entrada** para `054c:05c4` |
| `app/actions/external_controllers.py:41-49` | `_VENDOR_BY_VID` tem `"054c": "Sony"`, com o comentário *"não deveria chegar aqui"* — e chega |
| `app/actions/external_controllers.py:57-67` | `_BRAND_BY_OUI` faz o OUI `e4:17:d8` **vencer o VID**, e o comentário já diz por quê: o firmware *"MENTE o VID 054c (Sony) e o nome `Wireless Controller`, ficando IDÊNTICO a um DS4 Sony de verdade"*. Por Bluetooth a tela diz "8BitDo"; **por cabo, sem `uniq`, cai em "Sony"** |
| `app/actions/external_controllers.py:230-255` | `input_mode` devolve **`"outro"`**, e `MODE_SELECTOR_ITEMS` só conhece `nintendo`/`xbox` — **a ficha do modo PS4 fica muda** |
| `daemon/launch_env.py:83` | `_IGNORE_VALUE = "0x054c/0x0ce6"` é **um par cravado**; `05c4` não casa, e o 8BitDo **não** é escondido do SDL — o que hoje está **certo**, porque ele não tem vpad |

**A armadilha que este achado cria para a máquina de um desconhecido, e que
manda no desenho da E4:** `054c:05c4` é **também** o par de um **DualShock 4
Sony genuíno**. Emitir esse par no `SDL_GAMECONTROLLER_IGNORE_DEVICES` numa
máquina onde ele é um DS4 sem vpad **suma com o controle da pessoa**.

### O aviso do doctor, e a metade dele que a medição de 04/08 derrubou

`scripts/doctor.sh:1889` (`check_bt_clone_ds4`) dispara quando o `Modalias` do
D-Bus contém `usb:v054Cp05C4` (`:1901`) — **só isso**: não mede erro nenhum, não
filtra por `Connected` (dispara com o controle desligado) e **não olha a OUI**,
apesar de o endereço estar na variável duas linhas acima. O texto (`:1903`) diz
que o firmware *"não calcula a verificação de integridade e INUNDA o sistema de
erros"* — verdadeiro e medido — e emenda *"degradando o Bluetooth de TODOS os
controles"*, que é **a causalidade que a
[RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)
refutou por controle negativo** em 04/08: na janela de 23:51 a 23:58 o clone
despejou 26.884 erros de CRC e produziu **zero** frames L2CAP corrompidos.

**Não é entrega desta sprint** — está registrado aqui porque *decisão medida não
se apaga, e a refutação também é decisão medida*. Dona: a própria
RADIO-BOMBARDEADO-01.

---

## O IDENTIDADE-DUPLA visível no registro: rank 4 E 5

**GRAU: MEDIDO** (a fila acima, na medição entregue).

O 8BitDo ocupa **dois lugares permanentes** na fila. Os dois são endereço de
hardware da mesma OUI (`e4:17:d8`), e endereço de hardware **nunca é podado**:
`_prune_volatile_locked` (`daemon/subsystems/external_identity.py:550`) só solta
identidade **volátil**, e `_is_synthesized_mac`
(`daemon/subsystems/external_identity.py:184`) é literalmente
"primeiro octeto igual a `02`" — um endereço real começa pelo OUI do
fabricante, logo os dois rostos vão ao disco e ficam.

**Correção de premissa, e ela vem de dentro de casa.** A
[REGRA-NÃO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md)
(escrita hoje, mesma árvore) mediu duas coisas que mudam o que este achado
significa:

1. **O fantasma ausente NÃO infla o número exibido.** `_posicao_locked` conta
   só quem está em `_connected` — disco em 3/4/5, tela em 2/3. É cura da NUM-01.
   Logo o "rank 4 e 5" **não é** a causa do "todos no player 1";
2. **os dois endereços nunca escreveram LED no mesmo tick**, varrendo o journal
   de 27/07 a 06/08. A afirmação da
   [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)
   de que "os dois estão ativos no mesmo período" era leitura de
   `external_fila_restaurada`, que imprime a fila **do disco**, ausentes
   inclusive — não presença.

**O que sobra, e é real:** o fantasma **infla o lugar de quem chega depois**
(`slot_for` faz `max(ocupados, reserve) + 1` sobre a fila **inteira**), é
**permanente** e é **sem teto** (`_MAX_PERSISTED_SLOTS = 16` existe em
`daemon/subsystems/identity.py:215` e não é aplicado do lado externo).

**Por que isto entra nesta sprint mesmo não sendo dela:** hoje o efeito é uma
luz trocada quando ela muda o modo do 8BitDo. **Depois da E3, é o lugar dela na
partida.** Ver a tabela de relações, adiante.

---

## O desenho escolhido, e por que ele venceu

Quatro desenhos foram postos na mesa e julgados por três leitores independentes.

| desenho | o que entrega | nota |
|---|---|---|
| **UNIFICAR — o externo vira jogador** | descoberta única, normalizador de eixo, grab, **vpad próprio para cada externo**, esconde-esconde por par | **7** |
| **PUBLICAR A MESA** | o `state_full` publica a lista de externos do cache que o tick já monta; cartões por controle; nenhum caminho de input muda | 7 |
| **LUZ-QUE-PROMETE** | as bocas dizem dois números nomeados; o LED para de afirmar sob autoridade do jogo | 6 |

**Venceu o UNIFICAR, e por um motivo só: é o único que fecha a queixa que ela
fez.** Os outros dois consertam a **legenda**; ela não reclamou da legenda. Ela
reclamou de três controles disputarem o mesmo jogador dentro do jogo, e isso só
muda quando cada controle tiver um dispositivo de jogo próprio.

**As três razões técnicas que sustentam a escolha:**

1. **O eixo do desenho já existe, e é invariante desta casa.**
   `daemon/launch_env.py:44-48`: *"um controle físico produz exatamente UM
   dispositivo de jogo"*. Hoje isso vale só para os Sony. Unificar é **aplicar
   o invariante que já está escrito**, não inventar um;
2. **a fila unificada já existe** (`daemon/subsystems/identity.py:543`), e o
   co-op **já a consulta** para acender a lâmpada
   (`daemon/subsystems/coop.py:1019`). O que falta não é a fila: é o co-op
   **adotar** quem já está nela;
3. **o promotor já aceita externo — é letra morta.**
   `daemon/subsystems/coop.py:567-574` diz, textualmente: *"jogador com controle
   não-DualSense (8BitDo, Pro Controller) também ganha vpad uhid Edge — decisão
   de produto do VPAD-09"*. **O promotor aceita; o descobridor não entrega
   nenhum.**

### Os cinco enxertos que os juízes obrigaram, e sem os quais o desenho mente

**1. A promessa em linguagem de leiga estava maior que o desenho.**
O desenho vencedor prometia *"o número aceso no controle passa a ser o mesmo que
a tela mostra"* e, na seção de limites, admitia *"a luz pode dizer 2 e a tela do
jogo dizer 3"*. **As duas não podem ser verdadeiras.** O texto que vale é o
desta sprint, na seção *"O que fica ABERTO"*, item 1.

**2. "A espinha pode parar em qualquer degrau sem mentir" é FALSO.**
Parar na E1 ou na E2 deixa o `ExternalLedSync.tick` escrevendo `slot=2` no Pro e
a cor do slot 3 no 8BitDo, **exatamente como hoje** — enquanto a tela nova passa
a dizer "3 controles, 1 jogador". Hoje tela e luz mentem juntas; depois da E1
elas mentem **em desacordo**, e a pessoa não tem como saber em qual acreditar.
A cura é a **E0**, abaixo, que nasceu deste enxerto.

**3. A cura barata nunca tinha sido precificada.**
Se o defeito é "o LED afirma um número de jogador que o sistema não entrega", o
conserto mínimo é **parar de afirmar** — e a máquina existe:
`daemon/subsystems/external_identity.py:1171-1179` já implementa *"automático
OFF, PARA DE AFIRMAR (zero escritas, sem apagar ativamente)"*, lendo
`identity.auto_numbers_enabled` (`daemon/subsystems/identity.py:473`), que hoje
é `True` fixo porque *"sem campo no schema ainda, fica `True` até alguém pedir
o contrário"* (`daemon/subsystems/identity.py:440-446`). **Está na E0, com o
preço declarado e a recusa registrada** — porque apagar o número destruiria a
cura medida da R-24/R-25 (*"dois player 1, dois player 2"*), e **decisão medida
não se apaga**.

**4. A E1 não é um degrau só, e o pedaço caro estava escondido no barato.**
A linha da CLI é de risco perto de zero (o dado já está no fio). A **frase da
GUI não é**: `_format_players_hint` (`app/actions/home_actions.py:467-484`)
conta `len(controllers)`, e `controllers` vem do backend, que só conhece
DualSense — com 1 DualSense + Pro + 8BitDo ela devolve **string vazia**, e
nenhum valor de `coop.externals` muda isso. Para a frase falar, os externos
precisam **entrar na lista `controllers`**, que é consumida pelos cartões, pela
cor, pela bateria e pelo alvo de edição. **São dois degraus, e estão separados
abaixo.**

**5. Lista vazia não é "zero externos": é "não sei".**
O tick de externos degrada por desenho (HANG-01: dois tempos esgotados
consecutivos e ele fica mudo). Publicar a mesa a partir do cache **sem** um
estado DESCONHECIDO distinto de zero reproduz a queixa dela em silêncio, e com
mais autoridade que hoje. A guarda de frescor da E1 tem de produzir
**"não estou conseguindo ler os externos"**, nunca `0` — é a mesma regra do
`"—"` que `slot_label` já aplica (`app/actions/external_controllers.py:177`).

---

## As entregas

### E0 — o LED e a boca param de afirmar o que ninguém entrega

*(Nasceu do enxerto 2. É a única entrega que fecha a metade da queixa que está
no plástico, e não depende da resposta dela sobre vpad.)*

- **E0a — a CLI diz os dois números, nomeados.** `cli/cmd_coop.py:125-126` passa
  a ler `coop["externals"]`, que `daemon/ipc_handlers.py:1849` já publica. Sem a
  chave (daemon antigo), imprime `—`, **nunca `0`**:

  ```
  co-op local: ligado
  jogadores pelo Hefesto: 1
  controles na mesa: 3  (2 externos — dentro do jogo, quem numera é o jogo)
  ```

  E `controller list` sem `--external` ganha rodapé dizendo o que omitiu.
- **E0b — o eixo da numeração ganha interruptor.** `auto_numbers` já é lido; o
  que não existe é campo no schema nem superfície. Default **ligado** (nada muda
  para quem não pedir).
- **E0c — a decisão dela sobre a luz.** Pergunta 2 do cabeçalho. As três opções,
  com o preço de cada uma, estão em *"O que fica ABERTO"*, item 2.

**Risco:** perto de zero para E0a. **Não** toca `coop.py`, `external_identity.py`
nem caminho de input.

### E1 — a mesa aparece na tela, servida do cache que já existe

- **E1a — o cache.** `ExternalLedSync.tick`
  (`daemon/subsystems/external_identity.py:1099`) já monta o inventário, as
  identidades e os lugares, fora do event loop, e **joga tudo fora ao sair da
  função**. Passa a guardar um instantâneo serializável com carimbo de tempo.
  **Nenhuma enumeração nova**: o `state_full` roda a 10 Hz e tem proibição
  escrita de pagar enumeração (`daemon/ipc_handlers.py:1841-1843`);
- **E1b — a publicação, com guarda de frescor e estado DESCONHECIDO** (enxerto
  5);
- **E1c — a frase e os cartões.** Só aqui, e sabendo que exige os externos na
  lista `controllers` (enxerto 4).

### E2 — descoberta unificada, normalizador de eixo, e reencontro

Sem adoção nenhuma: o co-op continua não pegando ninguém. Prova inteira por
dublê.

- **descoberta única** que classifica cada nó em `dualsense`/`external` e
  devolve identidade, caminho, VID/PID, driver, hidraw irmão **e o `absinfo` de
  cada eixo** — substituindo a duplicação entre `core/evdev_reader.py:130` e
  `core/evdev_reader.py:379`, que hoje abrem **todos** os nós **duas vezes**, em
  dois laços diferentes;
- **normalizador por aparelho**, montado do `absinfo` na abertura, e **síntese
  de gatilho digital** quando faltam `ABS_Z`/`ABS_RZ`. Hoje
  `EvdevReader._handle_abs` (`core/evdev_reader.py:971-989`) faz `value & 0xFF`
  **seis vezes seguidas**, supondo "DualSense, 0..255". Com o Pro Controller
  (-32767..32767), o **centro** do stick vira `0`, que em 0..255 significa
  **talo à esquerda e para cima**: o personagem anda sozinho para o canto e não
  para. **Este é o item que decide se a cura funciona na máquina de um
  desconhecido** — uma tabela de "controles conhecidos" seria a versão que só
  funciona nesta bancada;
- **reencontro por identidade:** `_locate` (`core/evdev_reader.py:922`) hoje só
  procura em `discover_dualsense_evdevs()`. Sem isto, o externo nunca volta
  depois de um replug.

### E3 — a adoção (é aqui que a queixa fecha, e é aqui que o veto mora)

Um externo por vez, atrás do mesmo portão de modo que o co-op já tem
(`daemon/subsystems/coop.py:183-189`). Falha de `EVIOCGRAB` **cai no
comportamento de hoje por construção** (`daemon/subsystems/coop.py:430`: sem
grab, nada nasce) — o desenho falha para o status quo, que é o lado certo.

**O que QUEBRA se a E3 entrar sem as duas rotas abaixo — MEDIDO no código:**

- **o rumble do externo faz TODOS os DualSense vibrarem.**
  `apply_game_rumble` (`daemon/subsystems/gamepad.py:743-745`, e o caminho em
  `:757-766`) documenta: se `set_rumble_for(MAC)` não casar handle, **cai no
  broadcast**. O endereço de um externo **jamais** casa um handle do backend.
  A pessoa com o 8BitDo joga e o DualSense da outra pessoa vibra;
- **o player-LED do externo precisa de precedência declarada.** Passa a haver
  **dois escritores** para a mesma luz: o jogo (pelo vpad) e o tick da fila. O
  árbitro já existe e chama-se `_display_authority`
  (`daemon/subsystems/external_identity.py:1160-1190`) — a E3 tem de **usá-lo**,
  não criar um segundo caminho. E toda escrita tem de entrar pelo limitador de
  taxa do tick: o firmware clone do 8BitDo **morre** sob bombardeio de LED
  (medido, `daemon/ipc_handlers.py:286-291`).

**O que NÃO se faz, e a recusa é declarada:** **não se alarga o
`hidraw_broker`.** A allowlist de `broker/hidraw_broker.py:109` e `:200`
(só `054c:0ce6`) é a propriedade de **segurança** de um processo que roda como
root. Custo aceito: o externo com vpad fica **visível no hidraw**, e a defesa
dele é só o grab e o `IGNORE` do SDL.

### E4 — o esconde-esconde honesto, com cobertura POR PAR

`daemon/launch_env.py:83` carrega **um par**, não uma lista. A E4 compõe a linha
a partir da mesa, com a regra: **o par só sai no `IGNORE` se TODO aparelho
daquele par na mesa tiver vpad vivo.** É generalização direta da doutrina já
escrita nesta casa — *duplicado é melhor que zero controles* — e é o que impede
o desenho de sumir com o DualShock 4 genuíno de um desconhecido (ver o achado do
8BitDo que se declara Sony). O wrapper **não muda**: `assets/hefesto-launch.sh`
repassa a linha literal.

---

## O VETO

**Esta sprint reabre, por escrito, uma decisão medida — e por isso ela não
começa sem a palavra dela.**

O veto está registrado em três lugares, e nenhum deles é apagado:

1. [QUATRO-NO-RÁDIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md),
   na lista *"O que NÃO fazer"*: **"não dar vpad aos externos sem reabrir o
   `8BIT-02` explicitamente"**;
2. `daemon/subsystems/coop.py:770-776`: *"controle externo (8BitDo/Nintendo) não
   tem handle no backend e fica sem espelho POR DESIGN (…) dar-lhe vpad
   reverteria o `8BIT-02`"*;
3. `daemon/lifecycle.py:1411-1414`: *"Controles EXTERNOS NÃO entram na conta, e
   isso é decisão: eles já chegam ao jogo como gamepad nativo (`8BIT-02`)"*.

E o [índice de 03/08](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md), na
linha 225,
já tinha escrito a condição de saída: *"Vira sprint quando ela decidir se quer
vpad para externos"*.

**Esta sprint É essa decisão, e o que ela custa, dito na cara:**

- quem segurar o Pro Controller vai ver **desenho de botão de PlayStation** na
  tela do jogo, com A/B e X/Y fisicamente trocados no plástico. A máscara do
  vpad é **global**; máscara por jogador é a MÁSCARA-01;
- a **vibração** do externo pode não funcionar na primeira entrega (é o que a
  rota de FF da E3 resolve, e ela é a parte SEM PROVA do desenho);
- o hidraw do externo **fica visível**, porque a recusa de alargar o broker é
  firme;
- e o **rádio ganha tráfego novo** (FF e LED) na direção do firmware mais frágil
  da mesa, que é justamente o clone.

**As entregas E0, E1 e E2 NÃO reabrem o veto** e podem andar sem essa decisão.
**A E3 e a E4 não existem sem ela.**

---

## O que fica ABERTO

**1. Ninguém, no Linux, diz ao jogo QUEM é o jogador N.**
GRAU: SUSPEITA COM MECANISMO, forte. O jogo escolhe o índice dele **pela ordem
em que abre os dispositivos**. A cura transforma *"todos no player 1"* em *"cada
um em um player"* — mas **qual** número cada um recebe continua não sendo nosso.
**A luz pode dizer 2 e a tela do jogo dizer 3, e isso sobrevive à entrega
inteira.** Que a ordem de criação dos vpads influencie a ordem de enumeração é
suspeita, não medição. Qualquer texto de tela ou de README que prometa
"o número aceso é o mesmo do jogo" está **proibido** por esta sprint.

**2. O que fazer com a luz enquanto a E3 não existe.** Três opções, e a escolha
é dela:
   - **manter como está** — o Pro segue acendendo jogador 2. É a mentira medida;
   - **calar (E0b)** — zero escritas, sem apagar. Custo: quem tem dois externos
     perde o sinal que distingue um do outro, que é a cura medida da R-24/R-25;
   - **calar só com jogo aberto** — usa `_display_authority`. Custo: contradiz a
     decisão medida de `daemon/subsystems/external_identity.py:930-933`
     (*"device NOVO sem cache ainda recebe a numeração 1x — 8BitDo chegando no
     meio do jogo não fica apagado"*), e há um risco real
     na máquina de terceiros: com `display_authority` preso em `unknown`
     (Wayland puro, detector de janela sem leitura útil), **nenhum** externo
     receberia número nunca. GRAU: SUSPEITA COM MECANISMO.

**3. O grab e o FF num aparelho que não é Sony — SEM PROVA.**
`EVIOCGRAB` é do evdev, não do driver (mecanismo a favor), mas **ninguém nesta
casa jamais grabou um `hid-nintendo`**. E não se sabe se o firmware clone do
8BitDo sobrevive ao efeito de FF escrito de volta. **É o pressuposto central da
E3, e ele só fecha com os quatro na mesa.**

Além destes três, ficam fora do escopo e **com dono declarado**: o desenho do
botão (MÁSCARA-01); a fusão dos dois rostos do 8BitDo (REGRA-NÃO-REGISTRO-01); a
ficha muda do modo PS4 e o nome "Sony" por cabo (NOME-HONESTO-01); o duplicado
fora da Steam e o banner que é cego justamente aí (`daemon/ipc_handlers.py:2498`
só calcula `wrapper_used` com janela de jogo da Steam em foco); o DualSense Edge
**físico** de terceiros, que nunca é escondido porque `0df2` é o PID do nosso
vpad e incluí-lo é proibido por escrito (`daemon/launch_env.py:85-90`); e o Pro
Controller sem nó `js`, que é ordem de `input_register_device` no `hid-nintendo`
de origem — SDL2 o enxerga, a API `js` legada não.

---

## NOTA DATADA — 06/08/2026, 22h40: a segunda medição, e o achado que faltava

Ela voltou a ligar os três e relatou: *"os 3 controles conectados e com os 3 como
player 1"*. A medição foi refeita, e **o defeito não mudou** — mas apareceu um
dado que a medição das 21h08 não tinha.

### O que o produto responde, com os três na mesa

```
$ hefesto-dualsense4unix coop status
co-op local: ligado
jogadores ativos: 1

$ hefesto-dualsense4unix controller list
alvo de output: todos (broadcast)
  Controle 1 — BT
```

**Um.** O sistema tem três controles físicos; o daemon lista **um**; o co-op
conta **um jogador**. **Grau: MEDIDO** — é o produto respondendo sobre si mesmo,
sem intermediário.

### O achado novo: DOIS aparelhos no MESMO jogador 3

Lido direto do `sysfs`, `brightness=1`:

| LED aceso | dono | barramento |
|---|---|---|
| `input1147:white:player-3` | `DualSense ... (Hefesto P1)` — o **vpad** | `0003` (USB, virtual) |
| `input1151:white:player-3` | `DualSense Wireless Controller` — o **físico** | `0005` (Bluetooth) |
| `...:green:player-1` **e** `player-2` | `Pro Controller` | `0005` (Bluetooth) |

Duas coisas, e as duas são novas:

1. **O vpad e o controle físico acendem o mesmo número.** A sprint já registrava
   que o produto acende jogador em quem o co-op não conta; o que não estava
   registrado é que ele acende **o mesmo jogador em dois aparelhos ao mesmo
   tempo**. Quem olha o plástico vê dois "jogador 3" na mesa.
2. **O vpad chama-se `Hefesto P1` e acende `player-3`.** O nome do dispositivo e
   o LED que ele acende **discordam entre si**, no mesmo objeto. Nenhuma das três
   contabilidades da seção anterior explica isso sozinha — é o par
   (nome fixado na criação do vpad) contra (slot atribuído depois).
3. **O Pro Controller acende jogador 1 E 2 juntos.** É o padrão do `hid-nintendo`
   para "não numerado", e não uma atribuição nossa. Reforça o que a sprint já
   diz: sem adoção, o hardware escolhe sozinho o que exibir.

**Grau: MEDIDO** (leitura de `sysfs` e resposta do próprio produto, na máquina
dela, com os três ligados). **SEM PROVA:** que o jogo veja os três como jogador
1 — foi o que ela relatou, e o caminho até o jogo não foi instrumentado nesta
medição.

### O que isto muda nas entregas

Nada é reordenado, mas a **`E0`** ganha um critério a mais: não basta parar de
afirmar o que não se entrega — é preciso garantir que **dois aparelhos nunca
acendam o mesmo número**, inclusive quando um deles é o nosso próprio vpad. Um
teste que conte LEDs acesos por número fecha isso, e não existe hoje.

---

## Relação com as sprints que já existem

| sprint | esta sprint... | por quê |
|---|---|---|
| [MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) (ABERTA) | **absorve a entrega 2** ("descoberta por-jogador que aceite externos") e **depende do resto** | a E2+E3 são literalmente aquela entrega. O que **não** absorve é a máscara **por controle**, que é o preço declarado do veto: quem segura o Nintendo vê prompt de PlayStation até a MÁSCARA-01 fechar |
| [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md) (ABERTA) | **depende** para a E3, **não** para E0/E1/E2 | E3 promete "o seu lugar na partida"; prometer isso com a identidade do 8BitDo ainda instável é prometer o que a fila não tem. E1 e E2 andam sem ela |
| [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md) (aberta) | **não absorve, não depende, e a TORNA mais grave** | o rank duplo não causa a queixa (o número exibido é por presença — ver a correção acima). Mas depois da E3 trocar de modo passa a trocar **o lugar dela na partida**, não só a cor da luz. Ver a nota datada 3 |
| [REGRA-NÃO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md) (PROPOSTA, hoje) | **depende dela para a E3**, e **entrega algo a ela de graça** | é o desenho de cura da identidade dupla. O que esta sprint lhe dá: a descoberta unificada da E2 passa a ser **um** produtor de identidade em vez de dois, isto é, **um único lugar** onde a regra de fusão terá de ser aplicada |
| [QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md) (PROPOSTA) | **não absorve; é vizinha, e a E3 aumenta a superfície dela** | aquela é **identidade e relógio** sob quatro controles piscando; esta é **contagem e adoção**. Nenhuma das duas cura a outra. Mas dar vpad a externo põe mais um objeto por controle no ciclo de vida que aquela sprint diz estar com dois escritores — **a E3 não deveria entrar antes de a QUATRO-NA-MESA-01 ser lida** |
| [POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md) (PROPOSTA) | **não absorve, não depende — e a E3 CONTRADIZ o alcance declarado dela** | aquela sprint é a posse de **output por controle**, e trata de DualSense. A E3 cria saída (FF, LED) para aparelhos que **não têm handle no backend**, isto é, que estão **fora** do modelo de precedência por campo e por MAC de `core/backend_pydualsense.py`. Não é contradição de conclusão: é de **alcance**. Se as duas andarem, a POSSE-POR-CONTROLE-01 tem de dizer o que vale para quem não está no backend |
| [CONTAGEM-01](2026-07-25-CONTAGEM-01-a-tela-diz-dois-com-quatro-na-mesa.md) (ABERTA) | **absorve as entregas 1 e 5**, e **contradiz a entrega 2** | a lista de externos no `state_full` e a rota única de dados são a E1. A entrega 2 ("uma contagem só, e ela inclui os externos") **já tinha caducado** em 29/07 pela CONTAGEM-E-COOP-01: somar tudo num número regride os cartões e o rótulo dos externos. A resposta é **dois números NOMEADOS** |
| [CONTAGEM-E-COOP-01](2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md) | **reusa, não toca** | `ContagemDeControles` e `texto_de_contagem` (`app/actions/status_actions.py:100-168`) são o vocabulário certo, e já dizem `"1 do Hefesto + 2 externos"`. O defeito é que só a aba Status os usa |
| [JOGO-01](2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md) | **é a mesma cadeia, um nível acima** | lá o jogo via `js0`=vpad e `js2`=físico e mandava o controle para o player 2. Aqui são três aparelhos independentes no player 1. A causa é a mesma: **a ordem de enumeração não é nossa** |
| [NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md) | **sobe o preço de ela estar aberta** | a E1 põe o nome do externo num **cartão**, mais visível que hoje. Se ele diz "Sony" para um 8BitDo por cabo, a E1 amplifica o defeito em vez de criá-lo |

---

## As notas datadas que esta sprint deve

*Decisão medida não se apaga.* Quatro ganham nota de 06/08/2026:

1. **`8BIT-02` / QUATRO-NO-RÁDIO-01 / `coop.py:770-776` /
   `lifecycle.py:1411-1414`** — *"externo não ganha vpad"*. Continua sendo a
   decisão vigente **até ela responder a pergunta 1**. A nota registra a
   evidência nova de 06/08: com três controles ligados, o produto acendeu
   jogador 2 e jogador 3 em dois aparelhos que o jogo trata como jogador 1.
2. **CONTAGEM-01, entrega 2** — *"uma contagem só, e ela inclui os externos"*.
   **Caducou em 29/07**, superada por medição pela CONTAGEM-E-COOP-01. As
   entregas 1 e 5 seguem valendo e são a E1 desta sprint.
3. **IDENTIDADE-DUPLA-01, seção "O que está medido"** — a leitura de
   simultaneidade a partir de `external_fila_restaurada` **não se sustenta**:
   aquela linha imprime a fila do **disco**, ausentes inclusive. A correção é da
   REGRA-NÃO-REGISTRO-01, e está registrada aqui porque a queixa desta noite fez
   o achado voltar à mesa.
4. **`README.md:38` e `:43-45`, e `docs/usage/modos.md:71-78`** — a mesma frase
   serve hoje a duas coisas diferentes: para o DualSense *"vira um jogador"*
   significa **ganha um controle virtual próprio**; para o externo significa
   **ganha um número e uma luz**. `modos.md:75-78` diz que os externos *"entram
   na contagem como jogadores"*, o que é falso sobre o jogo e verdadeiro só
   sobre a luz. As frases **não se apagam**: ganham a data e o que caducou.

   **PAGA em 07/08/2026 — e o `grep` achou mais do que os dois arquivos acima.**
   A nota 4 dizia dois lugares; a varredura por *"entram na contagem como
   jogadores"*, *"jogadores adicionais"*, *"vira um jogador"* e *"um por
   jogador"* achou **sete frases em cinco arquivos**. Nenhuma foi apagada; cada
   uma ganhou nota datada com o que caducou e o que é verdade hoje:

   | arquivo | a frase | a nota diz |
   |---|---|---|
   | `README.md` (seção *"O que é"*) | *"cada um vira um jogador"* e *"entram como jogadores adicionais"* | vale para DualSense; externo não entra na contagem nem ganha controle virtual |
   | `README.md` (seção do 8BitDo por Bluetooth) | *"quatro controles (…), um por jogador"* | é lugar na fila, não jogador na partida |
   | `docs/usage/modos.md` (*"Co-op local"*) | *"entram na contagem como jogadores e recebem número de LED próprio"* | a luz é verdade, a contagem caducou — com as duas ressalvas do LED de 22h40 |
   | `docs/usage/bluetooth.md` (8BitDo por Bluetooth) | *"quatro controles (…), um por jogador"* | lugar na fila, não jogador |
   | `docs/usage/troubleshooting-8bitdo.md` (placar do teste ao vivo) | *"um por jogador"* e o `slot` de 1 a 4 | o `slot` serve à luz e à ordem, não à contagem |
   | `docs/usage/cli.md` (`coop on\|status`) | *"cada controle = um jogador"* e *"Cada controle conectado é um jogador, sempre"* | a conta do `status` vem só dos DualSense descobertos |

   **Examinada e deixada como está:** `docs/usage/interface.md:7-11` fala em
   *"o cenário de co-op que o projeto persegue"* — é meta declarada, não
   afirmação de entrega, e por isso não caducou.

---

## Como validar

### Sem nenhum aparelho, e cada um MORDE

| teste | a mordida (arrancar a cura tem de reprovar) |
|---|---|
| **normalizador de eixo** | com o `absinfo` do Pro (-32767..32767, `flat=500`) e valor cru **0**, o código de hoje devolve **0** e o curado devolve **128** |
| **gatilho digital sintetizado** | sem `ABS_Z`/`ABS_RZ` e com `BTN_TL2` pressionado, o gatilho tem de valer 255; hoje fica 0 para sempre |
| **descoberta unificada** | `054c:0ce6` classifica dualsense; `054c:05c4` e `057e:2009` classificam externo; nó virtual fora; **uma entrada por plástico** |
| **reencontro** | trocar o `eventN` do externo (replug simulado) e exigir que o leitor reencontre pela mesma identidade |
| **o rumble não vaza** — o teste que teria pego o defeito | com identidade externa e backend sem handle, o caminho de **broadcast** não pode ser alcançado. Hoje ele é |
| **contagem dupla** | `coop status` imprime as duas linhas; com daemon antigo imprime `—`, **nunca `0`** |
| **frescor** | entrada acima do teto **não é publicada**, e a tela diz **"não sei"**, não "zero externos" |
| **o caminho quente não paga enumeração** | fazer a descoberta de externos **levantar exceção** e exigir que `daemon.state_full` responda normal, com a lista vinda do cache |
| **cobertura por par** | mesa com um `054c:05c4` **sem** vpad: o par **não** pode sair no `IGNORE`. É o teste que protege a máquina do desconhecido |
| **portão anti-recaída** | nenhuma das quatro superfícies (daemon, CLI, GUI, applet) pode emitir número de jogador sem a palavra que o qualifica |

### Só fecha com os quatro na mesa

1. **que o `EVIOCGRAB` segura de fato num Pro Controller e num 8BitDo**, e que o
   jogo para de ver o nó cru — hoje **SEM PROVA**;
2. **que o FF escrito de volta chega aos motores** e que o firmware clone
   **sobrevive** a isso;
3. **que o jogo enxerga três jogadores distintos** — a queixa literal — e em
   **dois** cenários: com o `hefesto-launch` (Steam) e **sem** ele (nativo,
   Lutris, Heroic), que é onde o duplicado é a regra;
4. **que o `IGNORE` por par não subtrai o controle de ninguém** num título real;
5. **que o número aceso no plástico casa com o que a tela diz** — o par
   luz-e-tela é o critério que ela usa, e nenhum teste o alcança;
6. **PROVA-DE-TELA-01**: foto antes e depois, e a palavra final é dela.

---

**Nenhum endereço de hardware consta neste documento.** Os fabricantes são
citados por OUI público (Sony, Nintendo `e0:f6:b5`, 8BitDo `e4:17:d8`) ou pelo
nome do aparelho. Todo `caminho:linha` foi conferido contra a árvore de
06/08/2026 (`ae32c10`).
