# O defeito do BlueZ que ela lembrou — e os outros cinco

- **Escrito em:** 07/08/2026
- **Origem:** ela, de memória: *"o bluez tinha um defeito não lembro qual. que
  era issue conhecida dele e que iriam lançar a correção disso, não sei se já
  fizeram a correção. mas ficamos de mapear isso"*
- **O que este documento é:** o mapa. Que defeitos são, onde a casa os
  registrou, qual o estado deles hoje no rastreador do BlueZ, qual a versão
  dela, o que muda quando cada correção chegar, e qual contorno nosso vira
  dívida a apagar.
- **O que este documento NÃO é:** experimento. Tudo aqui é leitura — `/sys`,
  `/etc`, journal, `dpkg`, e o rastreador público do BlueZ. Nada foi escrito em
  hidraw, nenhum serviço foi reiniciado, nenhum controle caiu.

---

## A resposta curta, para ela

**A memória dela está certa, e são DOIS defeitos que casam com a frase — com
respostas opostas.**

| | o defeito | já lançaram a correção? |
|---|---|---|
| **1** | o `bluetoothctl` ficou **mudo** fora do modo interativo (issue **#1896**) | **SIM** — saiu no **5.87**, em 07/07/2026. Ela está no **5.86** e por isso **não tem** |
| **2** | o **uso-depois-de-liberado** em `dev_disconnected` (`src/adapter.c`) | **NÃO** — a correção (`5bc6aa79`) está **um commit depois** do 5.87 e **nenhuma versão a carrega ainda** |

E o mais caro dos três — o **crash de heap** que come os pareamentos dela —
**continua sem correção upstream conhecida**, e **continua acontecendo no 5.86**
na mesma taxa em que acontecia no 5.72.

GRAU de tudo nesta tabela: **MEDIDO** (as medições estão nas seções 3 e 4).

---

## 1. Onde a casa registrou cada um

A pergunta dela era *"onde ficou isso?"*. Ficou em seis lugares, e três deles
saíram da árvore de trabalho na faxina pré-1.0 — continuam alcançáveis pela
tag, e é assim que o próprio `install.sh` os cita.

| # | o defeito | onde está registrado |
|---|---|---|
| A | crash de heap (`unaligned fastbin chunk`) | `docs/usage/bluetooth.md:71`; `docs/process/sprints/2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md:85`; `docs/process/sprints/2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md:249`; `docs/process/estudos/2026-07-25-leva-causas-raiz.md:46`; `docs/process/estudos/2026-08-03-PROTOCOLO-as-medicoes-que-decidem-a-leva.md:203`; `docs/process/estudos/2026-07-27-mapa-dominio-dualsense-hid-e-bluetooth.md:243` |
| B | issue **#815**, *"random crash on device reconnect"* | `docs/usage/bluetooth.md:71`, e a tabela de commits no estudo arquivado de 19/07 |
| C | `bluetoothctl` mudo no one-shot (**COMPAT BLUEZ-586-CTL-01**) | `scripts/doctor.sh:82-95`; `scripts/bt_health_watchdog.sh:49-54`; sprint arquivada de 21/07 |
| D | uso-depois-de-liberado do 5.87 | `install.sh:1576-1577` — *"5.87 foi descartado (UAF novo em `dev_disconnected`, fix só em git HEAD sem release)"* |
| E | o retry-limit do 5.86 com defeito próprio | `install.sh:1574-1575`, e a sprint arquivada de 21/07 |
| F | **LP #2137758**, SIGSEGV em `btd_service_connecting_complete()` | estudo arquivado de 19/07, secão 1 |

Os três arquivados abrem assim:

```
git show arquivo/processo-pre-1.0:docs/process/estudos/2026-07-19-estudo-bluez-backport-onda-r.md
git show arquivo/processo-pre-1.0:docs/process/sprints/2026-07-21-sprint-pesquisa-bluez-estabilidade.md
git show arquivo/processo-pre-1.0:docs/process/estudos/2026-07-24-incidente-crash-bluetoothd-come-bonds.md
```

**Há um sétimo que NÃO é defeito, e fica registrado para ninguém reabrir:**
`bluez/bluez#892` (`docs/process/estudos/2026-07-25-leva-causas-raiz.md:78`). O
DualSense anunciar só HID e PnP no SDP, sem A2DP/HFP/HSP, é **comportamento
correto** — confirmado pelo mantenedor. Não há o que esperar do BlueZ ali.

---

## 2. A versão dela, medida

Tudo abaixo é **MEDIDO** em 07/08/2026, por leitura, na máquina dela.

```
bluetoothctl --version                    ->  5.86
/usr/libexec/bluetooth/bluetoothd -v      ->  5.86
dpkg -l bluez                             ->  5.86-0ubuntu0.1~hefesto24.04.3
dpkg -l libbluetooth3                     ->  5.86-0ubuntu0.1~hefesto24.04.2
dpkg -l bluez-obexd                       ->  5.72-0ubuntu5.5
dpkg -l bluez-tools                       ->  2.0~20170911.0.7cb788c-4build2
apt-cache policy bluez  ->  candidato = o instalado; o archive só oferece 5.72
```

O `/usr/lib/systemd/system/bluetooth.service` **não declara versão** — declara
`ExecStart=/usr/libexec/bluetooth/bluetoothd`, `Restart=on-failure`,
`ProtectSystem=strict` e, importante, **`#WatchdogSec=10` comentado**. Os 30 s
de watchdog que mataram o daemon em 06/08 vêm do nosso drop-in
(`/etc/systemd/system/bluetooth.service.d/10-hefesto-resilience.conf`, cuja
fonte é `assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf`).
`systemctl show` confirma em vigor: `WatchdogUSec=30s`, `RestartUSec=1s`.

**Duas divergências dentro do próprio backport, que ninguém tinha escrito:**

1. **`libbluetooth3` está uma revisão atrás do `bluez`** — `~hefesto24.04.2`
   contra `~hefesto24.04.3`. A revisão `.3` é a que traz o patch
   `hefesto-0001` (manter o bond no Virtual Cable Unplug). GRAU: **MEDIDO**
   para a diferença de revisão; **SEM PROVA** de que ela tenha consequência —
   o patch é do `bluetoothd`, não da biblioteca, e a `.2` pode ser
   simplesmente a última revisão em que a biblioteca mudou. Como confirmar:
   `dpkg -L libbluetooth3` e comparar o `sha256` do `.so` com o do `.deb` das
   duas revisões em `~/.cache/hefesto-dualsense4unix/bluez-backport/`.
2. **`bluez-obexd` continua no 5.72 do Ubuntu** — o backport levou `bluez`,
   `bluez-cups` e `libbluetooth3`, e não o `obexd`. GRAU: **MEDIDO**. Efeito
   sobre controle: **nenhum** — o `obexd` é transferência de arquivo, não toca
   HID. Fica escrito para não virar susto numa auditoria futura.

---

## 3. Defeito por defeito: estado upstream contra a versão dela

Todo estado upstream desta secão foi conferido em 07/08/2026 contra o
repositório oficial do BlueZ. **A contenção de commit em versão foi medida pela
API de comparação do GitHub** (`ahead_by` / `behind_by`), não por leitura de
changelog — changelog mente por omissão, a topologia do git não.

**Fato de base, MEDIDO: o último lançamento do BlueZ é o 5.87, de 07/07/2026.
Não existe 5.88.**

### A — o crash de heap: **SEM CORREÇÃO, E VIVO NA MÁQUINA DELA**

**Assinatura.** `malloc_consolidate(): unaligned fastbin chunk detected` e
`malloc(): unaligned fastbin chunk detected 2`, seguidas de
`code=dumped, status=6/ABRT`.

**Estado upstream: não existe issue pública com esta assinatura em
`bluetoothd`.** A busca de 22/07 concluiu *"inédita publicamente"* e a busca de
hoje devolve o mesmo — os resultados que aparecem são de outros programas
(Transmission, btop, napari) ou de outras assinaturas de heap do `bluetoothd`
(`realloc(): invalid next size`, `bluez/bluez#196`). GRAU: **MEDIDO** para o
resultado da busca; **SEM PROVA** para a afirmação forte *"não existe issue"* —
uma busca que não acha não prova ausência. Como confirmar: abrir o rastreador
do BlueZ e filtrar por `fastbin`.

**O parente público mais próximo é o LP #2137758** — *"bluetoothd crashed with
SIGSEGV in `btd_service_connecting_complete()` from `control_connect_cb()`"*,
aberta em 09/01/2026 contra o `bluez` 5.84-1. Estado hoje: **Confirmed,
Undecided, sem correção lançada**, última atividade em 24/01/2026. GRAU:
**MEDIDO** (leitura da API do Launchpad).

**E aqui há um achado novo desta sessão.** O aborto de 04/08 às 02:26:32 tem, no
**mesmo segundo e no mesmo PID**, a linha imediatamente anterior:

```
02:26:32 bluetoothd: profiles/input/device.c:control_connect_cb() connect to <MAC>: Function not implemented (38)
02:26:32 bluetoothd: malloc(): unaligned fastbin chunk detected 2
02:26:32 systemd[1]: bluetooth.service: Main process exited, code=dumped, status=6/ABRT
```

`control_connect_cb()` do **perfil input** é exatamente a função do LP #2137758.
GRAU: **MEDIDO** para a adjacência das três linhas; **SUSPEITA COM MECANISMO**
para o nosso crash ser o mesmo bug do LP — assinatura de aborto diferente
(heap contra SIGSEGV) pode ser o mesmo defeito atingindo o processo em pontos
diferentes, e pode não ser. **Só o backtrace decide**, e o backtrace é
justamente o que a casa não tem.

**E o que MEDI hoje derruba a esperança que sustentava o backport.** Entre
02/08 e 07/08 — cinco dias de 5.86 — o `bluetooth.service` abortou **cinco
vezes**:

| carimbo | assinatura | classe |
|---|---|---|
| 02/08 21:22:13 | `malloc_consolidate(): unaligned fastbin chunk detected` | heap |
| 03/08 23:58:07 | `malloc_consolidate(): unaligned fastbin chunk detected` | heap |
| 04/08 00:27:52 | `malloc_consolidate(): unaligned fastbin chunk detected` | heap |
| 04/08 02:26:32 | `malloc(): unaligned fastbin chunk detected 2` | heap |
| 06/08 21:03:44 | `Watchdog timeout (limit 30s)` | travamento, não heap |

**Quatro crashes de heap em cinco dias, no 5.86.** A linha de base que motivou
o backport era **cinco crashes em cinco dias, no 5.72**. GRAU: **MEDIDO** para
as duas contagens.

Isto **não** diz que o backport foi inútil — ele foi feito por outras razões
(a família #815 na via uhid, o descritor do DualSense, o `hefesto-0001`), e as
duas janelas têm regimes de uso diferentes, o que a própria sprint de 21/07 já
alertava. O que ele diz é uma coisa mais estreita e mais dura: **subir de 5.72
para 5.86 não reduziu a taxa de crash de heap nesta máquina.** GRAU: **MEDIDO**
para as duas taxas; **SEM PROVA** para *"as versões são equivalentes"* — duas
amostras de cinco dias não decidem isso.

**O que muda quando a correção chegar: nada previsível, porque não há correção
prevista.** O que destrava o assunto não é uma versão, é um **backtrace**. A
casa já tem a ferramenta armada (`scripts/bt_crash_capture.sh`) e já tem a
regra que impede o desastre de anexar o core
(`docs/process/POLITICA-core-nunca-sai-da-maquina.md`).

### B — issue #815, *"random crash on device reconnect"*: **CORRIGIDA, E ELA JÁ TEM**

**Estado upstream: FECHADA.** GRAU: **MEDIDO**.

A família foi curada na via uhid entre 5.74 e 5.79 (`b8ad3490a`, `ea96d7d18`,
`b94f1be65`, `ee39d01fb`, `a13638e6a`, `2daddeada`, `9a6a84a8a`). Com 5.86, ela
tem **todos**. GRAU: **MEDIDO** por versão.

**Consequência que precisa ficar escrita:** `docs/usage/bluetooth.md:71` diz
hoje que o crash *"pertence à família de um problema aberto no BlueZ ('random
crash on device reconnect')"*. **Essa frase caducou em duas metades.** A issue
não está aberta — está fechada. E a família dela foi corrigida numa versão que
a máquina dela roda há semanas, enquanto o crash continua. Ou seja: **o crash
de heap desta casa NÃO é o #815.** Decisão medida não se apaga: a frase de
`bluetooth.md` descrevia corretamente o que se sabia em 24/07; o que caducou é a
atribuição, e o motivo é esta secão.

### C — issue #1896, o `bluetoothctl` mudo: **CORRIGIDA NO 5.87, E ELA NÃO TEM**

Este é o defeito que melhor casa com *"issue conhecida dele e que iriam lançar
a correção"*.

- **Título:** *"bluetoothctl cli no longer prints anything outside the shell"*
- **Aberta:** 13/02/2026, contra o 5.86 — quatro dias depois do lançamento
- **Regressão bissectada em:** `e73bf58`
- **Estado:** **fechada como resolvida em 28/02/2026**
- **Corrigida por:** `b33e923b55e4` e `21e13976f2e3` (PR **#1909**)
- **O Arch entregou como patch de distro** na revisão `5.86-3`

GRAU de tudo acima: **MEDIDO** (leitura da issue e dos treze comentários dela).

**Está no 5.87?** Sim: `b33e923b55e4` é ancestral da tag 5.87 (`behind_by=0`).
GRAU: **MEDIDO**. **Está no 5.86?** Não — o 5.86 saiu em 09/02 e a correção é
de 28/02. GRAU: **MEDIDO** por data.

**O backport desta casa é o tarball upstream do 5.86 com o `debian/` do
resolute.** Os patches do PR #1909 são posteriores ao tarball e não estão no
`debian/` do resolute, que empacotava 5.85. Logo, **ela não os tem por nenhum
caminho.** GRAU: **SUSPEITA COM MECANISMO** pela proveniência do build —
e **MEDIDO** pelo produto, que é o que decide:

```
$ bluetoothctl list      ->  rc=0,  0 bytes de saída
$ bluetoothctl show      ->  rc=0,  0 bytes de saída
$ busctl tree org.bluez  ->  3 devices               <- controle positivo
```

O daemon está são e responde tudo no D-Bus com três controles vivos; **quem
mente é o cliente**. O defeito #1896 está **vivo na máquina dela em
07/08/2026**. GRAU: **MEDIDO**.

### D — o uso-depois-de-liberado em `dev_disconnected`: **CORREÇÃO PRONTA, NÃO LANÇADA**

Este é o outro que casa com a frase dela — e é o que responde *"não, ainda não
lançaram"*.

- `5d836f1` *"adapter: Fix failed bonding attempt after LE link disconnection"*
  **introduziu** o defeito: passou a chamar `device_is_connected` depois de
  `adapter_remove_connection`, que pode liberar o device.
- `5bc6aa79` *"adapter: Fix crash on `dev_disconnected`"* **corrige**: faz
  `adapter_remove_connection()` devolver se removeu, e sai antes de chamar
  `disconnect_notify()` sobre memória já liberada.

Contenção, medida pela topologia do git:

| commit | contra 5.86 | contra 5.87 |
|---|---|---|
| `5d836f1` (o defeito) | 258 commits **depois** — fora | ancestral (`behind_by=0`) — **dentro** |
| `5bc6aa79` (a correção) | fora | **1 commit depois** — **fora** |

GRAU: **MEDIDO** nas quatro células.

**Conclusão que a tabela obriga, e é a coisa mais útil deste documento: subir
para o 5.87 hoje troca três correções por um uso-depois-de-liberado novo.** O
5.86 dela **não** tem o defeito `5d836f1`, porque ele nasceu 258 commits depois
do 5.86. **A decisão de 22/07 de ficar no 5.86 e recusar o 5.87 continua
correta em 07/08 — e agora com número.**

**O que muda quando a correção chegar:** o `5bc6aa79` entra no primeiro
lançamento após o 5.87 (previsivelmente o **5.88**, sem data anunciada). Nesse
dia, e só nesse dia, o caminho fica livre para ela ganhar, de uma vez: a
correção do `bluetoothctl` (C), a correção do retry-limit (E) e a correção do
bond dual-mode (G) — sem herdar o uso-depois-de-liberado.

### E — o retry-limit do 5.86 com defeito próprio: **CORRIGIDO NO 5.87, E ELA NÃO TEM**

O 5.86 foi escolhido **por causa** do `17a227b7` *"device: Limit the number of
retries on auth failures"* — limite de tentativas mais recuo exponencial no
laço de reconexão, que é o retrato estrutural do gatilho de crash medido em
21/07. **Confirmado: `17a227b7` é ancestral da tag 5.86** (`ahead_by=0`,
`behind_by=170`). GRAU: **MEDIDO**.

**Só que o mecanismo comprado tem defeito.** `7ca74765` *"device: Fix
auth_retry timeout not being removed on reconnect"*: `timeout_remove()` era
chamado com `0` em vez do identificador real do temporizador, porque
`auth_retry_id` era zerado **antes** da chamada. Efeito: o temporizador de nova
tentativa **não é cancelado** na reconexão. Está no **5.87**, não no 5.86.
GRAU: **MEDIDO**.

**Ou seja: a máquina dela roda o limitador de tentativas com o vazamento de
temporizador dentro.** GRAU: **MEDIDO** para a ausência do commit; **SEM
PROVA** para qualquer efeito observável na máquina dela — não medi nenhum
sintoma atribuível a isso. Como confirmar: `bluetoothd -d` numa janela de
reconexão com falha de autenticação, procurando reintento fora de hora.

### F — LP #2137758: **CONFIRMADA, SEM CORREÇÃO**

Já detalhada em (A). Estado hoje: `bluez (Ubuntu)`, **Confirmed**, importância
**Undecided**, **sem correção lançada**. GRAU: **MEDIDO**.

Correção de registro que a sprint de 21/07 já tinha feito e que vale repetir
para não voltar a circular errado: **LP #2137758 é SIGSEGV em
`btd_service_connecting_complete`, e NÃO "HIDP heap corruption"**.

### G — issue #2034, o bond dual-mode: **CORRIGIDA NO 5.87, E ELA NÃO TEM**

Achado desta sessão, não registrado antes como defeito vivo.

- **Título:** *"HID bonding check fails for dual-mode devices bonded only on
  BREDR"*
- **Aberta:** 14/04/2026. **Estado:** **fechada**
- **Sintoma:** `Rejected connection from !bonded device`
- **Causa:** `input_device_bonded()` em `profiles/input/device.c` checava o
  vínculo no endereço **LE** para um perfil que é **só clássico**
- **Corrigida por:** `756da3fa1` *"input: Fix checking LE bonding on HIDP"* —
  **ancestral da tag 5.87** (`behind_by=0`), **fora do 5.86**

GRAU: **MEDIDO**.

**Por que isto importa aqui e não é curiosidade:** os controles dela são
dual-mode, e a casa já registrou recusas de conexão de entrada com a família de
mensagem `Refusing connection ... unknown device` depois de crash. GRAU:
**SUSPEITA COM MECANISMO** para o #2034 explicar parte dessas recusas — a
mensagem que a casa mediu não é literalmente a do #2034, e as recusas medidas
em 24/07 têm explicação suficiente sem ele (o bond tinha sido comido pelo
crash). **Não promova isto a causa sem medir.** Como confirmar: procurar
`!bonded` no journal, que é a assinatura exclusiva do #2034:
`journalctl -u bluetooth.service --since '2026-08-01' | grep -F '!bonded'`.

---

## 4. O quadro fechado

| # | defeito | corrigido upstream? | em que versão | ela tem? |
|---|---|---|---|---|
| A | crash de heap `unaligned fastbin` | **não**, e sem issue pública | — | sofre, 4x em 5 dias |
| B | #815 random crash on reconnect | sim, fechada | 5.74 a 5.79 | **sim** |
| C | #1896 `bluetoothctl` mudo | sim, 28/02/2026 | **5.87** | **não** |
| D | UAF em `dev_disconnected` | **corrigido, não lançado** | pós-5.87 | não sofre (é do 5.87) |
| E | temporizador de retry não cancelado | sim | **5.87** | **não** |
| F | LP #2137758 SIGSEGV | **não**, Confirmed | — | possivelmente sofre |
| G | #2034 bond dual-mode em HIDP | sim | **5.87** | **não** |

**A leitura de uma linha: o 5.87 tem quatro coisas que ela quer (C, E, G, e as
demais correções do ciclo) e uma que ela não pode aceitar (D). O 5.88 é o
primeiro lançamento em que a conta fecha.**

---

## 5. O que ela precisaria para ter cada correção

**Nenhuma destas ações é para hoje.** Está escrito para quando o 5.88 sair.

| quero | caminho | custo |
|---|---|---|
| **C** só (o `bluetoothctl`) | os dois commits do PR #1909 como patch quilt sobre o backport 5.86, revisão `~hefesto24.04.4` | pequeno e cirúrgico; não toca o daemon, só o cliente |
| **C + E + G** | subir para 5.87 | **recusado**: traz o UAF (D) |
| **C + E + G**, sem o UAF | 5.87 mais o `5bc6aa79` como patch quilt | tenta o mesmo build do 5.86 com um commit a mais; risco: o resto do ciclo do 5.87 nunca rodou nesta máquina |
| tudo, limpo | **esperar o 5.88** e refazer o backport | o caminho da casa; o gatilho é o anúncio do lançamento |

Em qualquer um dos quatro, o preço já conhecido continua valendo, e está escrito
em `install.sh:1557-1563`: o `postinst` do próprio `bluez` **reinicia o
`bluetoothd`**, e a migração **descarta os bonds antigos no primeiro start** —
ela repareia uma vez. Com três controles na mesa, isso não é operação de
madrugada de trabalho; é operação com ela presente e sabendo.

**Como saber que o 5.88 saiu, sem depender de memória:** a página de
lançamentos do BlueZ. Enquanto o topo disser `5.87`, nada mudou.

---

## 6. A dívida de contorno — o que ela apaga, e o que NÃO apaga

Esta é a parte que a pergunta dela pedia: *o que o Hefesto faz hoje por causa
disso?*

### Vira dívida, e some com a correção

**O único contorno nosso que existe puramente por causa de um defeito do BlueZ
é o do #1896.**

`scripts/doctor.sh:91` define uma **função-sombra** que substitui o binário
`bluetoothctl` para os **22 usos** daquele script: monta o comando pelo modo
interativo, tira ANSI e prompt, e só emite o que vem depois do eco do próprio
comando.

```bash
bluetoothctl() {
    command -v bluetoothctl >/dev/null 2>&1 || return 127
    printf '%s\nquit\n' "$*" | command timeout 8 bluetoothctl 2>/dev/null \
        | sed -e $'s/\x1b\\[[0-9;]*[A-Za-z]//g' -e 's/\r//g' -e 's/^\[bluetoothctl\]> //' \
        | awk -v cmd="$*" 'BEGIN{seen=0} $0==cmd{seen=1;next} !seen{next} $0=="quit"{exit} /^\[/{next} {print}'
}
```

**No dia em que ela rodar um BlueZ com o PR #1909 dentro, estas sete linhas —
mais os nove de comentário acima delas — podem sair, e os 22 usos voltam a ser
chamada direta.** Não antes: hoje, sem elas, `scripts/doctor.sh` fica cego para
tudo que ele lê pelo `bluetoothctl`, com `rc=0` e saída vazia — que é o pior
formato de cegueira que existe, porque parece resposta.

### NÃO vira dívida — e é importante não apagar por engano

Quatro coisas parecem contorno do mesmo defeito e não são:

1. **`_btctl_lento` em `scripts/bt_health_watchdog.sh:65` FICA.** Ele não existe
   por causa do #1896; existe porque `pair` é **assíncrono** e um `quit`
   imediato cancelaria o pareamento no meio. Ele segura o `quit`. Um BlueZ
   corrigido não muda isso.
2. **A doutrina "todo estado sai do `busctl`, nunca do `bluetoothctl`" FICA.**
   Ela nasceu de um defeito **nosso**, não do BlueZ: em 22/07 a função-sombra
   leu zero controles conectados com três vivos e o watchdog derrubou uma
   sessão saudável. O comentário em `scripts/bt_health_watchdog.sh:49-54`
   registra isso. **A fonte de verdade de estado é o D-Bus por decisão medida**,
   e a correção do #1896 não a revoga.
3. **O drop-in de resiliência, o agente, os retratos de bond e o restaurador
   manual FICAM.** Eles mitigam o defeito **A**, que não tem correção. Enquanto
   o `bluetoothd` abortar quatro vezes em cinco dias, tirar o salva-vidas é
   trocar um incômodo por perda de pareamento.
4. **O piso de versão do `doctor.sh` (`>= 5.79`) FICA, mas está desatualizado.**
   `scripts/doctor.sh:2152` reprova abaixo de 5.79 com a mensagem *"crashes
   crônicos de input/HIDP do 5.72"*. O piso continua certo; o que este estudo
   acrescenta é que **passar do piso não é passar do crash** — o 5.86 crasha.
   Nota para quem for mexer: **não** transforme isto em piso 5.87 sem antes ler
   a secão D deste documento, porque 5.87 traz o UAF.

### O que vira dívida no TEXTO, não no código

`docs/usage/bluetooth.md:71` atribui o crash à família #815 e chama a issue de
*"aberta"*. As duas coisas caducaram (secão B). O documento não deve ser
apagado nem reescrito por cima — ganha nota datada, que é a regra da casa.

---

## 7. GRAU, consolidado

**MEDIDO**

- as versões instaladas, e o que o unit e o drop-in declaram;
- os cinco abortos entre 02/08 e 07/08, com carimbo e assinatura;
- as três linhas adjacentes do aborto de 04/08 02:26:32;
- `bluetoothctl list` e `show` devolvendo zero byte com `rc=0`, contra o
  `busctl` listando três devices no mesmo instante;
- o último lançamento do BlueZ ser o 5.87, de 07/07/2026;
- os estados de #815 (fechada), #1896 (fechada em 28/02), #2034 (fechada) e
  LP #2137758 (Confirmed, sem correção);
- a contenção de `17a227b7`, `7ca74765`, `5d836f1`, `5bc6aa79`, `b33e923b55e4`
  e `756da3fa1` nas tags 5.86 e 5.87, pela topologia do git.

**SUSPEITA COM MECANISMO**

- o crash de heap desta casa ser o mesmo bug do LP #2137758 — a adjacência do
  `control_connect_cb()` é forte, a assinatura de aborto difere;
- o backport dela não carregar os patches do PR #1909 pela proveniência do
  build — dito isso, o **produto** já provou que não os carrega;
- o #2034 explicar alguma das recusas de conexão de entrada já medidas.

**SEM PROVA**

- que não exista issue pública para a assinatura `unaligned fastbin` — busca
  que não acha não é ausência;
- que o vazamento de temporizador do retry (E) produza qualquer sintoma na
  máquina dela;
- que a defasagem de revisão do `libbluetooth3` tenha consequência;
- **a causa do crash de heap.** Sem backtrace não há causa, e o core de 06/08
  foi canalizado para o apport e descartado.

---

## 8. O que fica em aberto, e por quê não fechei

1. **O backtrace.** É o único caminho que fecha o defeito A, e ele **não é
   experimento meu**: exige armar `scripts/bt_crash_capture.sh --on`, que grava
   `kernel.core_pattern`, que é global do kernel — e depois **esperar um
   crash**. Vira protocolo para ela, e entra atrás do protocolo de 06/08, que
   ela já decidiu que vem primeiro.
2. **Se o #2034 aparece no journal dela.** A busca por `!bonded` fecha isso em
   um comando, e não precisa de hardware — mas precisa de uma janela de journal
   que cubra reconexões dual-mode, e eu preferi deixar a pergunta escrita a
   responder com amostra pequena.
3. **A nota datada em `docs/usage/bluetooth.md`.** É edição de documento que ela
   publica, e a casa não muda texto voltado a quem usa sem a palavra dela.

---

## Relacionado

- `docs/usage/bluetooth.md` — a página que fala com quem usa, e a que precisa
  da nota datada
- `docs/process/sprints/2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md`
  — o custo do crash em segundos fora do ar
- `docs/process/sprints/2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md`
  — o crash interrompendo a tempestade de rádio
- `docs/process/POLITICA-core-nunca-sai-da-maquina.md` — por que o relatório
  upstream leva backtrace e nunca o core
- `docs/process/estudos/2026-07-27-mapa-dominio-dualsense-hid-e-bluetooth.md`
  — as duas causas distintas de bond que evapora
- `docs/process/estudos/2026-08-07-PROTOCOLO-o-controle-que-cai-sozinho.md`
  — a queda de 03/08 23:58:07 contada do lado do daemon
