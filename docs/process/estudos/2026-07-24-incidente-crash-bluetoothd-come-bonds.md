# 2026-07-24 — Incidente: o bluetoothd crashou e comeu os bonds Nintendo-class

Investigação dos dois sintomas relatados ao vivo em 24/07 à noite:

> "o pro controler da nintendo voltou a desconectar direto, ontem tínhamos
> resolvido isso também" e "o 8bitdo voltou a conectar automaticamente e a
> desligar. ambos regressão."

**Desfecho: não é regressão do código de 23/07.** As duas curas suspeitas estão
no ar e funcionando. A causa é o crash crônico do `bluetoothd`, que voltou a
acontecer e levou bonds junto.

## O que foi descartado (com prova)

| Hipótese | Como foi descartada |
|---|---|
| Regressão do `BT-SNIFF-PER-OUI-01` (23/07) | Nenhum device com a OUI do Pro genuíno estava conectado no momento das quedas; o filtro nem chegou a agir |
| `BOND-KEEP-01` revertido | String presente no binário: `keeping bond on virtual cable unplug (HEFESTO BOND-KEEP-01)` |
| Backport do BlueZ substituído por downgrade | `dpkg -l bluez` → `5.86-0ubuntu0.1~hefesto24.04.3`, exatamente o `_BZ_TARGET` do install |
| Merge malfeito na janela 23→24/07 | `git log --merges` na janela: **zero merges**; a linha é toda linear |
| Código instalado divergente do repo | Instalação é **editável** (`_editable_impl_*.pth`); daemon e GUI carregam de `src/` |

## O que aconteceu, com hora

Correlação entre o journal e os snapshots de bond do próprio projeto
(`/var/lib/hefesto-dualsense4unix/bt-bonds/`):

| Hora | Bonds no snapshot | Pro genuíno |
|---|---|---|
| 15:40 | 3 | presente |
| 17:39 | 3 | presente |
| 17:54 | 3 | presente |
| **20:31:32** | — | **crash do bluetoothd** |
| 20:39 | **1** | sumiu |
| 20:54 | 1 | sumiu |
| 21:24 | 4 | re-pareado pela mantenedora |
| 21:54 | **2** | sumiu de novo |

O crash:

```
20:31:32 bluetoothd[1008]: malloc_consolidate(): unaligned fastbin chunk detected
20:31:33 systemd[1]: bluetooth.service: Main process exited, code=dumped, status=6/ABRT
20:31:33 systemd[1]: bluetooth.service: Failed with result 'core-dump'
```

Nove reinícios do serviço no dia.

## O gatilho (achado novo)

Os 30 s anteriores ao crash, no log do kernel:

```
20:31:02 input: Pro Controller as .../uhid/0005:057E:2009.0005/input/input81
20:31:02 nintendo 0005:057E:2009.0005: hidraw4: BLUETOOTH HID v80.01 Gamepad [Pro Controller]
20:31:09 nintendo 0005:057E:2009.0006: hidraw5: BLUETOOTH HID v80.01 Gamepad [Pro Controller]
20:31:32 bluetoothd: malloc_consolidate(): unaligned fastbin chunk detected
```

**Dois "Pro Controller" conectaram com 7 s de diferença** — o da Nintendo e o da
8BitDo. Os dois se apresentam com o **mesmo VID:PID `057E:2009` e o mesmo nome**,
porque o da 8BitDo clona a identidade do genuíno (já documentado na arqueologia
de 23/07; a OUI é o único discriminador confiável).

Vinte e três segundos depois, o heap do `bluetoothd` corrompeu.

Diferença em relação ao crash #6 (21/07): **não houve `rmmod`**. O playbook
"nunca `rmmod` driver HID com BT vivo" continua válido, mas não cobre este
caminho. Este é o cenário de reconexão da família do issue upstream #815
("random crash on device reconnect" — SEGV + lista duplamente ligada corrompida
na via kernel-HIDP), para o qual o estudo `2026-07-19-estudo-bluez-backport-onda-r.md`
registra: **"NÃO encontrado: fix upstream para heap corruption na via kernel-HIDP"**.

## Por que os sintomas são esses

Sem bond, o `bluetoothd` recusa a conexão de entrada do controle:

```
21:56:52 profiles/input/server.c:connect_event_cb() Refusing input device connect: No such file or directory (2)
21:56:52 profiles/input/server.c:confirm_event_cb() Refusing connection from E4:17:D8:1C:66:1A: unknown device
21:57:13 src/device.c:search_cb() E4:17:D8:1C:66:1A: error updating services: Connection timed out (110)
```

O controle acende, tenta conectar, é recusado, desiste. Visto de fora: "conecta
sozinho e desliga" (8BitDo) e "desconecta direto" (Pro). São **o mesmo defeito**,
não dois.

Note que `E4:17:D8` foi recusado como "unknown device" **mesmo tendo bond em
disco** — sinal de que o estado em memória do daemon, depois do crash e do
restart, não corresponde ao que está gravado.

## O que NÃO foi feito (de propósito)

Restaurar o bond do snapshot. O `bt_bonds_restore.sh` é manual por decisão de
projeto: se o controle já rotacionou a própria chave, reimpor a LinkKey antiga
gera loop de falha de autenticação — a mesma classe de gatilho do crash de heap.
A decisão é da mantenedora.

## Encaminhamentos

1. **Reproduzir sob controle**: ligar os dois Nintendo-class em sequência curta,
   com `btmon` gravando, e confirmar se o crash é determinístico. Se for, é a
   receita mínima para reportar upstream — algo que os 6 crashes anteriores
   nunca tiveram.
2. **Mitigação operacional enquanto não há fix**: serializar a adoção dos dois
   Nintendo-class (não deixar os dois se conectarem na mesma janela de segundos).
3. **Reduzir a perda quando acontecer**: hoje o snapshot roda a cada 30 min. Um
   snapshot na BORDA de cada bond novo custaria pouco e transformaria "perdi os
   bonds do dia" em "perdi os últimos segundos".
4. **A captura forense NÃO está armada** — e é por isso que o dump de hoje não
   ficou retido. Verificado: `/proc/sys/kernel/core_pattern` aponta para o
   `apport` do Pop!_OS, que descarta crash de pacote fora da distro — e o
   `bluetoothd` daqui é justamente o backport. O `bt_crash_capture.sh --on`
   existe para isso (troca o `core_pattern` para o `systemd-coredump` via
   `/etc/sysctl.d/99-hefesto-bt-coredump.conf`), mas está desligado.
   **Armar antes da próxima sessão de caça**, ciente de que `core_pattern` é
   global do kernel — o script documenta o custo e tem `--off`.

## O que já foi mitigado (24/07)

- **Snapshot de bond na borda da conexão** (`83-hefesto-bond-snapshot.rules`):
  o snapshot deixou de depender só do timer de 15 min. Um pareamento feito logo
  depois de uma foto não some mais sem cópia no crash seguinte — foi exatamente
  o que aconteceu com o Pro (re-pareado 21:24, sumido 21:54, com a foto das
  21:24 como única cópia).
