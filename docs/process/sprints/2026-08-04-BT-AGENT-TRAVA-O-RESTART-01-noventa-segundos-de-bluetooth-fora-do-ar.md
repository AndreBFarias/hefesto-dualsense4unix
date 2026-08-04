# BT-AGENT-TRAVA-O-RESTART-01 — noventa segundos de Bluetooth fora do ar

- **Medido em:** 03→04/08/2026, no journal dela
- **Estado:** **CURADO em 04/08/2026.** Esta sprint nasce fechada — é registro
  de causa-raiz, não plano de trabalho
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
