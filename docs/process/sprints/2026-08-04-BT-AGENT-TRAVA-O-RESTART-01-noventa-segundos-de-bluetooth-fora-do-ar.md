# BT-AGENT-TRAVA-O-RESTART-01 — noventa segundos de Bluetooth fora do ar

- **Medido em:** 03→04/08/2026, no journal dela
- **Estado:** ~~CURADO em 04/08/2026~~ → **REABERTA em 06/08/2026.** A cura
  funcionou no que se propôs, e mesmo assim o sintoma dela voltou com 57
  segundos. O dono mudou: ver a **nota datada de 06/08** no fim
- **Gravidade:** alta — é a explicação do sintoma que ela reporta há semanas
- **Pré-requisito:** nenhum

---

## O sintoma, na voz dela

> *"meu bt caiu e ta pedindo autenticação, pq?"*
> *"tá mas pq tá pedindo senha?"*

Não era pedido de senha de pareamento. O `bluetooth.service` demorava tanto a
voltar que ela clicava em **Ativar** na tela do sistema — e esse botão passa
pelo polkit.

---

## A medição, e o controle positivo que a torna prova

```
23:58:07  malloc_consolidate(): unaligned fastbin chunk detected
23:58:07  bluetooth.service: Main process exited, code=dumped, status=6/ABRT
23:58:10  bluetooth.service: Scheduled restart job, restart counter is at 1
23:58:10  Stopping hefesto-bt-agent.service...
23:58:10  Stopping phomemo-m835-rfcomm.service...
23:58:10  Stopped  phomemo-m835-rfcomm.service       <- o vizinho parou NA HORA
23:59:40  hefesto-bt-agent.service: State 'stop-sigterm' timed out. Killing.
23:59:40  Stopped  hefesto-bt-agent.service          <- 90 s = TimeoutStopSec padrão
23:59:40  Starting bluetooth.service...              <- só ENTÃO o BlueZ voltou
```

O `bt-agent` do `bluez-tools` **não responde ao SIGTERM** quando o `bluetoothd`
morre: fica preso numa chamada D-Bus que nunca volta. Ele até registra
`SIGUSR1 received` às 23:58:10 e não sai. Como o `bluetooth.service` depende
dele pela ordenação, o agente segurava o restart do **próprio BlueZ**.

**Noventa segundos, a cada crash.** E o BlueZ 5.86 caiu **duas vezes em meia
hora** naquela noite (23:58:07 e 00:27:52).

O `phomemo-m835-rfcomm.service` é o **controle positivo** desta medição: mesmo
gatilho, mesmo segundo, mesma ordenação, parada instantânea. O que difere é o
programa — não o systemd, não a configuração, não a máquina.

Conferir:

```bash
journalctl --since '2026-08-03 23:58:05' --until '2026-08-03 23:59:45' --no-pager \
  | grep -iE 'bt-agent|phomemo|Stopping|Stopped|Starting bluetooth'
```

---

## A cura aplicada

**`assets/systemd/hefesto-bt-agent.service`:** `TimeoutStopSec=3s` +
`SendSIGKILL=yes`.

É seguro, e a razão importa: o `bt-agent` é um agente de pareamento **sem
estado em disco**. Matá-lo não corrompe bond nenhum, e um pareamento em curso
(se houvesse) falharia do mesmo jeito — porque o `bluetoothd` que o serve já
morreu. O que se perde ao matá-lo é exatamente nada; o que se ganha são 87
segundos de Bluetooth no ar.

**`assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf`:** `RestartSec`
de 2 s para **1 s**, a pedido dela (*"por mim voltava 1 segundo depóis"*). O
gargalo real eram os 90 s acima; com aquele curado, **este valor passa a ser o
tempo que de fato vale**.

Verificado em vigor na máquina dela:

```bash
systemctl show hefesto-bt-agent.service -p TimeoutStopUSec   # 3s
systemctl show bluetooth.service -p RestartUSec              # 1s
```

---

## O que NÃO está curado, e é importante dizer

O `bluetoothd` continua caindo por corrupção de heap. Isso é **bug upstream do
BlueZ 5.86**, e esta cura só encurta o prejuízo — de 90 s para ~4 s.

**E o produto ainda não CONTA a ela o que aconteceu.** Ela vê os quatro
controles caírem e o Bluetooth voltar, sem uma palavra na tela. Esse resto é o
aceite 4 da
[RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md).

---

## O que morde

Um teste de arquivo de unit: arrancar o `TimeoutStopSec=3s` faz reprovar. E o
portão de paridade de empacotamento (`scripts/check_packaging_parity.sh`) tem
de enxergar o campo — o unit é **instalado**, não só versionado, e a casa já
pagou por essa diferença antes (`9c944a8`: *"o ciclo uninstall+install
desligava SEIS curas em silencio"*).

---

## Relacionado

- [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md) — o outro defeito medido no MESMO crash
- [RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)
- [A noite em que o som do controle voltou](../estudos/2026-08-04-a-noite-em-que-o-som-do-controle-voltou.md)

---

## NOTA DATADA — 06/08/2026: o "~4 s" foi medido em **57 s**, e o dono é outro

Decisão medida não se apaga. O que está escrito acima continua verdadeiro; o
que caducou é o **número** e a **conclusão de que estava fechado**.

### O que aconteceu, com carimbo

Às 21h03 de 06/08 o `bluetoothd` caiu de novo na máquina dela. Linha do tempo
do `systemd[1]`, medida no journal:

```
21:03:44.516  bluetooth.service: Watchdog timeout (limit 30s)!
21:03:44.516  Killing process 1076 (bluetoothd) with signal SIGABRT
21:03:51.651  Main process exited, code=dumped, status=6/ABRT        (+7,1 s)
21:04:34.490  Failed with result 'watchdog'                          (+42,8 s)
21:04:35.517  Scheduled restart job, restart counter is at 1         (+1,0 s)
21:04:38.766  hefesto-bt-agent: stop-sigterm timed out. Killing.     (+3,2 s)
21:04:39.125  Starting bluetooth.service...
21:04:41.766  Started bluetooth.service
```

**57,25 segundos** entre o SIGABRT e o `Started`. A sprint prometia ~4 s.

### A primeira hipótese estava REFUTADA, e o controle positivo está dentro da medição

O achado que abriu esta investigação dizia *"o bluetoothd trava AO SER
REINICIADO"*. **A ordem dos carimbos é a inversa:** o único `systemctl restart
bluetooth.service` da janela foi às **21:04:40.440**, ou seja **56 segundos
DEPOIS** do watchdog, e caiu num daemon que já estava renascendo. Esse segundo
ciclo parou o `bluetoothd` em **29 milissegundos** (`Deactivated
successfully`), com o mesmo `ExecStopPost` e o mesmo agente.

Logo: o daemon **não trava ao sair**. Ele estava **vivo e travado** — o laço
principal parou de mandar `WATCHDOG=1` e o watchdog o matou. Hipótese que não
explica o que já funcionava é contorno; esta explica os dois ciclos.

### Onde os 57 segundos foram parar (MEDIDO, com dono)

| trecho | tempo | dono |
|---|---|---|
| SIGABRT → processo morto (core para o apport) | 7,1 s | nosso `WatchdogSec` |
| **`ExecStopPost` do snapshot de bonds** | **42,8 s** | **nosso** (drop-in, linha 26) |
| `RestartSec=1` (o valor que ela pediu) | 1,0 s | nosso — **1,7% do prejuízo** |
| `TimeoutStopSec=3s` do `bt-agent` | 3,2 s | nosso, funcionando como projetado |
| partida do BlueZ | 2,6 s | BlueZ |

**O `RestartSec` que esta sprint ajustou não é o gargalo — nunca foi.** O
gargalo agora é o `ExecStopPost` do snapshot, com **75% do tempo**.

**Controle:** rodar `scripts/bt_bonds_snapshot.sh` à mão, como root, sobre a
mesma fonte real (3 bonds, cache SDP completo) custou **0,03 s**; e no ciclo
limpo das 21:04:40 o mesmo `ExecStopPost` custou 29 ms. **1.400x** entre o
custo próprio do script e o que ele custou no naufrágio. Os 42,8 s são
**contenção, não trabalho**.

Candidato com aritmética que fecha: `scripts/bt_bonds_snapshot.sh:106` →
`flock -w 30`. O diretório gravado chama-se `20260806-210426-808958` — o `date`
rodou às 21:04:26, e o PID 808958 é o `ExecStopPost` bifurcado às 21:03:51:
**34,4 s parados antes de nomear o diretório**, com um `flock` que espera até
30 s logo acima. GRAU: **SUSPEITA COM MECANISMO** — não identifiquei quem
segurava o lock, e a alternativa (inanição de I/O enquanto o apport lia o core)
não pode ser separada com os dados que restaram.

### O que fazer (aceites abertos)

- **E4 — `flock -n` no gancho de PARADA.** Esperar por um lock enquanto o
  Bluetooth está fora do ar troca "snapshot perdido" (que o timer de 10 min e a
  borda udev da `83-hefesto-bond-snapshot.rules` cobrem) por "rádio morto". No
  gancho, desistir na hora é a escolha certa.
- **E5 — `TimeoutStopSec` explícito no drop-in do `bluetooth.service`**, para
  que nenhum gancho nosso possa segurar o serviço por tempo indefinido.
- **E6 — reexaminar `WatchdogSec=30`.** Ele é a única razão pela qual um
  travamento de 30 s vira SIGABRT + core + 57 s fora do ar, em vez de um
  soluço. O template do BlueZ traz `#WatchdogSec=10` **comentado**; sem o nosso
  drop-in não haveria SIGABRT. E hoje pagamos o preço sem a forense que o
  justificaria: o `core_pattern` desta máquina é o **apport**, não há
  `coredumpctl`, e `/var/crash` não tem arquivo do `bluetoothd` de hoje — o
  core foi canalizado e **descartado**. Watchdog sem backtrace é custo puro.
- **E7 — o teste de ciclo que a [CURA-QUE-FERE-01](2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md)
  já pedia (E1/E2/E3) continua sem existir**, e é ele que teria pego isto: o
  ciclo só foi exercitado sob restart LIMPO, onde o `ExecStopPost` cai no no-op
  e custa 29 ms. Sob crash, ninguém mediu.

### O que NÃO é nosso (medido, para não voltar a ser investigado)

- **`Failed to set default system config for hci0`** — 47 ocorrências em 38
  partidas, inclusive no boot frio com o adaptador ainda desligado.
  `/etc/bluetooth/main.conf` tem **quatro** linhas não-comentadas no total, e
  nenhuma chave de `[LE]`, privacidade, scan ou intervalo. Descasamento
  BlueZ 5.86 ↔ kernel. **SUSPEITA COM MECANISMO.**
- **`Failed to set privacy: Rejected (0x0b)`** — 4 ocorrências em 38 partidas,
  **ausente** no boot frio e **presente** no restart quente. `0x0b` é
  `MGMT_STATUS_REJECTED`, que é o que o kernel devolve quando o adaptador já
  está ligado na hora do pedido. É a assinatura de reiniciar o `bluetoothd` com
  o controlador de pé — **não é do adaptador TP-Link recusar privacidade LE**.
- **`control_connect_cb() ... Host is down (112)`** — três linhas, uma por bond
  em disco, no minuto seguinte à partida. É o BlueZ tentando reabrir o canal de
  controle HID de cada aparelho confiável; `112 = EHOSTDOWN` é o rádio dizendo
  que o controle está desligado. Benigno. **Sem relação** com a
  [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)
  pelo lado do VID:PID — isto roda sobre L2CAP/BR-EDR, antes de existir
  descritor HID. O que TEM relação é o 8BitDo ter dois BD_ADDR, um por modo, e
  poder ocupar dois lugares na lista de bonds.

### GRAU

MEDIDO: a linha do tempo, os 57,25 s, a repartição por dono, os 0,03 s do
controle, o `WatchdogUSec=30s` em vigor, as contagens de journal.
SUSPEITA COM MECANISMO: o `flock` como dono dos 42,8 s.
SEM PROVA: a causa do travamento de 30 s do laço principal — o core foi para o
apport e foi descartado, e sem backtrace não há causa.
