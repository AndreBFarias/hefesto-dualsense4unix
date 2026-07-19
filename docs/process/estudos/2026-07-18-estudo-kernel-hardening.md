# Estudo 2026-07-18 — Kernel hardening (PLAT-03 itens 2-4 + PLAT-06)

> Missão KERNEL-HARDENING da onda PLATAFORMA. Coleta 100% read-only na máquina de referência
> (MeowSystem: B450M S2H, Ryzen 7 5800X, Pop!_OS 24.04 COSMIC, kernel 7.0.11-76070011-generic)
> em 2026-07-18 ~22-23h. Toda afirmação abaixo tem evidência local (sysfs/journal/modinfo/
> scripts da Aurora) ou referência de fonte; nada foi inventado. Regras/confs aqui são
> ESPECIFICAÇÃO para o install — nada foi aplicado neste estudo.

## §1 — Cmdline atual e o mapa param→dono

`/proc/cmdline` (2026-07-18):

```
initrd=\EFI\Pop_OS-…\initrd.img root=UUID=7c6a1403-… ro systemd.show_status=false loglevel=0
mitigations=off nvidia-drm.modeset=1 quiet usbcore.autosuspend=-1 acpi_enforce_resources=lax
splash pcie_aspm=off nvidia-drm.fbdev=1 usbcore.quirks=054c:0ce6:gn,054c:0df2:gn
```

Fontes de dono: `/etc/kernelstub/configuration` (seções `default` vs `user`) e
`~/.config/zsh/scripts/ritual-aurora-self-heal.sh` (a Aurora tem `ensure_kernel_option()` que
GREPA a configuration e re-adiciona via `kernelstub --add-options` se o param sumir — ou seja,
"dono" = quem re-cria sozinho).

| Param | Dono | Evidência |
|---|---|---|
| `initrd=…` `root=…` `ro` | Pop!_OS (kernelstub gera) | não está em kernel_options; é o esqueleto da entry |
| `quiet` `splash` | Pop!_OS (seção `default` E `user` da configuration) | configuration `default.kernel_options` |
| `systemd.show_status=false` `loglevel=0` | usuária (manual, one-shot) | está em `user.kernel_options` mas NÃO tem `ensure_kernel_option` na Aurora — ninguém re-cria |
| `mitigations=off` | **Aurora** (self-heal) | ritual-aurora-self-heal.sh:966 |
| `nvidia-drm.modeset=1` | **Aurora** | linha 977 |
| `nvidia-drm.fbdev=1` | **Aurora** | linha 981 |
| `acpi_enforce_resources=lax` | **Aurora** | linha 975 |
| `pcie_aspm=off` | **Aurora** | linha 965 |
| `usbcore.autosuspend=-1` | **Aurora** | linha 976 |
| `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` | **co-propriedade hefesto+Aurora**: nasceu no hefesto (`scripts/install_usb_quirk.sh`), a Aurora adotou no self-heal | linha 1003 + comentário na própria Aurora ("gatilhos HID do hefesto") e no nosso `hefesto-dualsense-storm.conf` ("domínio do install_usb_quirk.sh / Ritual-Aurora") |

Histórico relevante (comentários da Aurora, linhas 91-146): `usbcore.quirks=054c:0ce6:k`
(NO_LPM), `processor.max_cstate=1` e `threadirqs` foram REMOVIDOS deliberadamente (v3.24) —
o install NÃO deve reintroduzir nenhum deles.

### Especificação do passo "cmdline gerenciado" do install (PLAT-03 item 2)

Params de interesse do hefesto: `usbcore.autosuspend=-1` e
`usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`.

1. Detecção de presença: `grep -q '"<param>"' /etc/kernelstub/configuration` (mesmo teste da
   Aurora — string exata entre aspas na lista JSON). Fallback sem kernelstub (não-Pop):
   grep em `/etc/default/grub` `GRUB_CMDLINE_LINUX_DEFAULT`.
2. Se presente → registra no estado local (`~/.local/state/hefesto-dualsense4unix/`)
   `cmdline.<param>=terceiro` e NÃO toca (nesta máquina os dois já são da Aurora — o install
   aqui vira no-op com atribuição registrada).
3. Se ausente → `kernelstub --add-options "<param>"` (ou edit do grub + `update-grub`) e
   registra `cmdline.<param>=hefesto`. Uninstall: `kernelstub --delete-options` SÓ do que está
   registrado como `hefesto`.
4. **REGRA CRÍTICA do `usbcore.quirks`**: o kernel só respeita UM token `usbcore.quirks=` no
   cmdline (documentado pela própria Aurora, linha 985: "se um dia houver outro usbcore.quirks=
   no cmdline, o kernel respeita só" um). O install NUNCA pode adicionar um segundo token: se
   já existe QUALQUER `usbcore.quirks=` sem os nossos IDs, o passo deve fazer MERGE
   (`existente,054c:0ce6:gn,054c:0df2:gn`) via delete-options + add-options do token fundido —
   e registrar que o token é compartilhado.
5. Validação pós-boot é separada da configuração: configuration pode ter o param e o boot atual
   não (falta reboot). Doctor compara `/proc/cmdline` × configuration e reporta "aplicado" /
   "pendente de reboot" (o doctor atual já faz isso pro quirk gn — manter o padrão).

## §2 — Runtime PM dos HOSTS xHCI (PLAT-03 item 3)

Controladores USB PCI (classe 0c03) desta máquina:

```
02:00.0 [1022:43d5] AMD 400 Series Chipset USB 3.1 xHCI  → power/control=on, runtime_status=active
0c:00.3 [1022:149c] AMD Matisse USB 3.0 Host Controller  → power/control=on, runtime_status=active
```

Estado de TODOS os devices USB hoje: `power/control=on` + `autosuspend_delay_ms=-1000`
(inclusive root hubs usb1-4, o TP-Link BT 3-1, DualSense 3-4, os 2 Pro Controller/8BitDo-cabo
e os 2 receivers Compx) — efeito das regras da Aurora `99-usb-kill-autosuspend.rules` (add) +
`99-usb-power-change.rules` (change) + `usbcore.autosuspend=-1`.

Efeito de `auto` num HOST xHCI: o controlador PCI inteiro entra em runtime suspend (D3hot)
quando todos os filhos estão suspensos; o religamento depende de PME/wake do chipset — no
AMD 400-series há histórico real NESTA máquina de queda do barramento INTEIRO (o storm de
maio derrubava teclado+mouse junto com o DualSense: era o barramento, não o device). Host em
`on` elimina a classe inteira de bugs de wake. Custo: ~irrelevante em desktop (host ativo).

**Descoberta de atribuição**: a Aurora JÁ cobre os hosts nesta máquina —
`/etc/udev/rules.d/99-storage-no-link-pm.rules` termina com:

```
ACTION=="add|change", SUBSYSTEM=="pci", DRIVER=="xhci_hcd", ATTR{power/control}="on"
```

O hefesto precisa da regra própria para máquina virgem, registrando "já provido por terceiro"
quando a da Aurora existir.

### Regra EXATA (novo asset `assets/81-hefesto-usb-host-power.rules`)

```
# hefesto-dualsense4unix — runtime PM dos HOSTS USB sempre ligado.
# A economia no host xHCI (power/control=auto) suspende o CONTROLADOR PCI inteiro
# quando os filhos dormem; num wake mal suportado (AMD 400-series: provado em maio
# de 2026 nesta classe de máquina) o barramento INTEIRO cai — teclado, mouse e
# controle juntos. Host em "on" custa ~nada em desktop e elimina a classe do bug.
# Classe PCI 0x0c03xx = USB host (xHCI 0x0c0330, EHCI 0x0c0320, OHCI/UHCI 0x0c0310/00).
# Match por CLASSE (não por driver): pega o host mesmo antes/sem bind do xhci_hcd.
ACTION=="add|change", SUBSYSTEM=="pci", ATTR{class}=="0x0c03*", TEST=="power/control", ATTR{power/control}="on"
```

### Regra EXATA de devices (PLAT-03 item 1, novo asset `assets/81-hefesto-usb-power.rules`)

```
# hefesto-dualsense4unix — controles e adaptadores BT nunca dormem.
# power/control=on desliga o runtime PM do device; autosuspend_delay_ms=-1 é a
# trava redundante (delay negativo = nunca suspende) caso algo devolva "auto".
# ACTION add|change: add cobre plug/coldplug (systemd-udev-trigger no boot);
# change reaplica quando qualquer agente mexe em runtime (precedente: 99-usb-power-change
# da Aurora). DEVTYPE=usb_device: o atributo power/ vive no device, não na interface.
# Sony (DualSense/Edge e afins)
ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="054c", TEST=="power/control", ATTR{power/control}="on", ATTR{power/autosuspend_delay_ms}="-1"
# Nintendo (Pro Controller e 8BitDo em modo Switch: 057e:2009)
ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="057e", TEST=="power/control", ATTR{power/control}="on", ATTR{power/autosuspend_delay_ms}="-1"
# 8BitDo (modo próprio/X-input)
ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="2dc8", TEST=="power/control", ATTR{power/control}="on", ATTR{power/autosuspend_delay_ms}="-1"
# Microsoft (controles Xbox)
ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{idVendor}=="045e", TEST=="power/control", ATTR{power/control}="on", ATTR{power/autosuspend_delay_ms}="-1"
# Adaptadores Bluetooth por CLASSE (e0 = Wireless Controller; cobre o TP-Link
# 2357:0604 desta máquina — bDeviceClass e0/01/01 PROVADO no sysfs)
ACTION=="add|change", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", ATTR{bDeviceClass}=="e0", TEST=="power/control", ATTR{power/control}="on", ATTR{power/autosuspend_delay_ms}="-1"
```

Gap conhecido e coberto: adaptadores BT COMPOSITE (bDeviceClass `ef`) escapam do match por
classe — para eles quem liga o autosuspend é o próprio `btusb` no probe, e o modprobe.d do §5
(`enable_autosuspend=0`) corta isso na raiz. As duas camadas juntas fecham o caso.

### Por que udev e NÃO tmpfiles

- `tmpfiles.d` roda UMA vez no boot, não filtra por atributo (um glob
  `/sys/bus/pci/devices/*/power/control` escreveria `on` em TODA a PCI — GPU, NVMe —
  destruindo runtime PM alheio), não reage a hotplug (replug do adaptador BT voltaria ao
  default) nem a `change`.
- udev: filtra por classe/vendor, coldplug garantido pelo `systemd-udev-trigger.service`,
  hotplug e re-assert em `change` (precedente da própria Aurora). Números 81-*: livres de
  conflito; a restrição "<73" só vale para regras com `TAG+="uaccess"` (memória
  reference_udev_uaccess_ordem_73) — estas não usam uaccess.

Install idempotente: antes de instalar, detectar cobertura equivalente de terceiro
(`grep -l 'power/control.*on' /etc/udev/rules.d/99-usb-*.rules 99-storage-no-link-pm.rules`)
e registrar atribuição; instalar a nossa mesmo assim (é inócua por cima — escreve o mesmo
valor) para que a máquina fique íntegra se a Aurora sair. Uninstall remove só as 81-*.

## §3 — ASPM (PLAT-03 item 3b)

- Cmdline: `pcie_aspm=off` (dono: Aurora, §1).
- **ARMADILHA provada ao vivo**: com `pcie_aspm=off`, o sysfs
  `/sys/module/pcie_aspm/parameters/policy` continua mostrando `[default]` — ele NÃO reflete
  o off. A prova de que o off pegou é o link: `lspci -vv` nos dois hosts mostra
  `LnkCtl: ASPM Disabled` (02:00.0 e 0c:00.3, coletado com sudo).
- O que `pcie_aspm=off` da Aurora já cobre: ASPM desabilitado em TODOS os links PCIe do boot
  inteiro (inclusive L1 substates: `L1SubCtl1` todo desligado no 02:00.0). Não há nada de ASPM
  a acrescentar pelo hefesto nesta máquina.
- **Doctor deve reportar** (sem mudar nada — política é decisão do dono):
  1. `grep -o 'pcie_aspm=[^ ]*' /proc/cmdline` → "off (Aurora)" | ausente;
  2. se ausente: mostrar a policy ativa (`cat /sys/module/pcie_aspm/parameters/policy`) e
     explicar que `powersave`/`powersupersave` podem adicionar latência/instabilidade a USB
     hosts; instruir o dono (não aplicar);
  3. NUNCA usar a policy sysfs como prova de off (armadilha acima) — cmdline é a fonte.

## §4 — Sabotadores de energia (PLAT-03 item 4)

Inventário desta máquina (dpkg + unit-files):

| Ferramenta | Instalada? | Mexe em USB autosuspend? |
|---|---|---|
| TLP | NÃO | (se entrar: `USB_AUTOSUSPEND=1` é default do TLP — religaria `auto` em tudo que não estiver na denylist) |
| powertop | NÃO | (se entrar: `--auto-tune` seta `auto` em TODOS os devices e hosts) |
| tuned | NÃO | (perfis powersave setam autosuspend 2s) |
| power-profiles-daemon | NÃO (COSMIC usa system76-power) | — |
| **system76-power** | **SIM (1.2.8, unit `com.system76.PowerDaemon.service` enabled, perfil Performance)** | ver abaixo |

**system76-power — o sabotador real e PROVADO desta distro**: no startup ele seta
`link_power_management_policy=med_power_with_dipm` em todos os `scsi_host` MESMO em perfil
performance (evidência: cabeçalho do `99-storage-no-link-pm.rules` da Aurora, que existe
exatamente para reverter isso; strings do binário confirmam `power/control` e "failed to set
disk autosuspend delay"). Em perfil battery (notebooks System76 — alvo da v1) ele aplica
runtime PM agressivo. Na máquina de referência a Aurora já o neutralizou.

**Detecção pelo doctor (seção "Energia USB")**:

```
dpkg-query -W tlp powertop tuned 2>/dev/null            # presença
systemctl is-enabled tlp.service tuned.service 2>/dev/null
systemctl is-active com.system76.PowerDaemon.service    # system76-power vivo?
system76-power profile 2>/dev/null                      # perfil atual (via CLI, sem D-Bus manual)
grep -r . /sys/class/scsi_host/host*/link_power_management_policy  # med_power_* = sabotagem ativa
cat /sys/bus/usb/devices/*/power/control                # qualquer "auto" = alerta com o caminho do device
```

Racional do alerta: instruir exceção (TLP: `USB_DENYLIST="054c:0ce6 …"`; powertop: não usar
--auto-tune; system76-power: nossa regra 81 re-assert em `change` já defende) — nunca
desinstalar nada do usuário.

## §5 — Módulos: params disponíveis (PROVADOS por modinfo local)

| Módulo | parm úteis | Estado atual |
|---|---|---|
| `usbhid` | `jspoll`/`mousepoll`/`kbpoll` (uint, "Polling interval"), `quirks` (`vendorID:productID:quirks` em hex 0x — para clones problemáticos), `ignoreled` | jspoll=0, mousepoll=0, kbpoll=0 (0 = respeita bInterval do descriptor) |
| `hid_playstation` | **NENHUM param** | — (não há knob de kernel para DualSense; tudo é nosso userspace) |
| `hid_nintendo` | **NENHUM param** | `joycon_enforce_subcmd_rate` é FUNÇÃO interna (string no .ko), não parâmetro — NÃO existe knob para relaxar o rate-limit de subcomandos. O muro BT do 8BitDo/Pro é inegociável a nível de módulo; a cura é do NOSSO lado (EXT-04: parar de bombardear LED) |
| `btusb` | `enable_autosuspend` (bool, "Enable USB autosuspend by default"), `reset`, `disable_scofix`/`force_scofix` | **enable_autosuspend=Y** — o furo: o btusb LIGA autosuspend no probe do adaptador; hoje só o global da Aurora neutraliza |
| `snd_usb_audio` | `quirk_flags` etc. | já curado: `/etc/modprobe.d/hefesto-dualsense-storm.conf` (ignore_ctl_error|ctl_msg_delay_1m para 0ce6/0df2) — manter como está |

### modprobe.d consolidado — novo asset EXATO (`assets/modprobe.d/hefesto-btusb-no-autosuspend.conf`)

```
# hefesto-dualsense4unix — o btusb liga USB autosuspend no adaptador Bluetooth no
# probe (enable_autosuspend default Y — provado por modinfo neste kernel). Em maquina
# sem usbcore.autosuspend=-1 global isso poe o radio dos controles para dormir.
# Esta opcao corta na raiz, para QUALQUER adaptador (inclusive composite classe ef
# que escapa da regra udev por classe e0). Vale a partir do proximo probe (replug
# ou reboot); a cura imediata no runtime e a regra udev 81 (power/control=on).
options btusb enable_autosuspend=0
```

Aplicação a quente sem reboot (install): escrever `0` em
`/sys/module/btusb/parameters/enable_autosuspend` só afeta probes FUTUROS; o adaptador já
plugado é curado pela regra 81 + `udevadm trigger --subsystem-match=usb --action=change`
(padrão que o install já usa para as regras 7x).

### Latência de poll atual (medida no sysfs, endpoints de interrupt)

| Controle | Speed | bInterval | Intervalo efetivo | Taxa |
|---|---|---|---|---|
| DualSense USB (3-4, if 1.3, ep 03/84) | high (480M) | 6 | 2^(6-1) microframes = **4 ms** | 250 Hz |
| Pro Controller / 8BitDo-cabo (1-6/3-3, ep 02/81) | full (12M) | 8 | **8 ms** | 125 Hz |

Semântica de `usbhid.jspoll` (por que NÃO é default-seguro):

1. **É GLOBAL** — um valor para todos os joysticks USB (não dá para acelerar só o Pro
   Controller sem tocar o DualSense).
2. **A unidade muda com o speed**: o valor vai direto ao `usb_fill_int_urb()`; em full-speed é
   milissegundos, em HIGH-speed é EXPOENTE (2^(n-1) microframes — semântica documentada em
   include/linux/usb.h e provada aqui: o DualSense high-speed com bInterval 6 roda a 4 ms).
   `jspoll=1` num device high-speed = 125 µs (8 kHz) — não é o "1 ms" que a intuição espera.
3. **Cobertura incerta para GAMEPAD**: o switch do usbhid (drivers/hid/usbhid/hid-core.c) aplica
   jspoll por usage da collection HID; o DualSense se anuncia como Game Pad (usage 0x05), não
   Joystick (0x04) — se o kernel desta versão só cobre HID_GD_JOYSTICK, jspoll nem afeta o
   DualSense. Não confirmado no binário local (fonte não instalada) — precisa prova empírica.
4. Prova empírica disponível no repo SEM tocar kernel: `scripts/benchmark_polling.py` mede a
   taxa real por timestamps de evdev. Protocolo: medir baseline → `echo N | sudo tee
   /sys/module/usbhid/parameters/jspoll` → REPLUG do controle (o param só vale em re-probe) →
   medir de novo. Só promover a default se ganho medido e zero regressão de CPU/rumble.

Nota: 250 Hz no DualSense USB já supera a janela de frame de 60-120 fps; o candidato a ganho
real é o Pro Controller/8BitDo (125 Hz) — e justamente nele a cobertura do jspoll é a mais
incerta (driver hid-nintendo sobre usbhid). Por isso: [INVESTIGAR-MAIS].

`usbhid.quirks` (PLAT-06 item 1, clones): existe e é o veículo certo SE um clone USB
problemático aparecer (`usbhid.quirks=0xVVVV:0xPPPP:0xQUIRK`); nenhum clone USB problemático
está presente hoje — especificar só quando houver um caso real (nada preventivo).

## §6 — kernel-watch (PLAT-06 item 4): de storm-watch a vigia do ecossistema

Hoje: `scripts/storm_watch.sh` + user unit `hefesto-dualsense4unix-storm-watch.service`
(enabled, `Restart=on-failure`, `RestartSec=300`) — segue `journalctl -k -f -n0 --grep=' -71'`
para `~/.local/state/hefesto-dualsense4unix/storm.log`. O journal é persistente nesta máquina
(journald-aurora-persistent.conf da Aurora), então histórico sobrevive a reboot.

### Padrões a vigiar (com proveniência)

| Tag | Regex (--grep, case-insensitive) | Proveniência |
|---|---|---|
| `[USB-71]` | `error -71\|can't add hid device\|device descriptor read/64, error\|not accepting address\|unable to enumerate USB device` | os 4 últimos já são os padrões do doctor.sh:824 (batalha de maio, provados) |
| `[JOYCON]` | `joycon_enforce_subcmd_rate` | PROVADO ao vivo: `nintendo 0005:057E:2009.000C: joycon_enforce_subcmd_rate: exceeded max attempts` em loop 18/07 20:23 (a morte do 8BitDo BT); string confirmada no .ko |
| `[BT-HCI]` | `Bluetooth: hci\d.*(timeout\|failed\|error)` | genérico kernel-side; nesta máquina o observado foi userspace (`bluetoothd: Failed to confirm name for hci0`) — ver nota CRC abaixo |
| `[XHCI]` | `xhci_hcd.*(reset\|died\|timeout\|halt)` | strings do driver upstream ("HC died; cleaning up", "Host halt failed"); ZERO ocorrências no journal local — vigiar preventivo, não alarmar por histórico |

**Nota CRC (o clone DS4)**: os 211k CRC fails do clone 054C:05C4 foram visíveis via btmon
(intrusivo — VETADO em produção). O proxy não-intrusivo e provado é o CONTADOR do adaptador:
`hciconfig hci0` → `RX … errors:N` / `TX … errors:N` (hoje 0/0). O kernel-watch deve
SNAPSHOTAR esses contadores (na partida e a cada N minutos) e logar `[BT-ERR] rx=… tx=…`
quando o delta > 0 — isso pega degradação de rádio sem btmon.

**Detecção do clone** (PLAT-04 item 3, cabe ao doctor): iterar `bluetoothctl devices` e, para
cada MAC, `bluetoothctl info <MAC>` → linha `Modalias: usb:v054Cp05C4…` = clone DS4 pareado →
alerta "desparear (degrada o rádio para todos)". HOJE o clone NÃO está pareado (provado:
só Pro Controller E4:17… e DualSense A0:FA… na lista) — o doctor guarda a guarda.

### Formato do log (evolução compatível do storm.log)

Arquivo: `~/.local/state/hefesto-dualsense4unix/kernel.log` (o storm.log continua até a
migração; o install pode symlinkar). Linhas:

```
# 2026-07-18 23:00:00 kernel-watch iniciado (padrões: USB-71 JOYCON BT-HCI XHCI + contadores hci)
2026-07-18T20:23:22-0300 [JOYCON] nintendo 0005:057E:2009.000C: joycon_enforce_subcmd_rate: exceeded max attempts
2026-07-18T20:25:00-0300 [BT-ERR] hci0 delta rx_errors=+118 tx_errors=+0 (acumulado 118/0)
```

Implementação: um `journalctl -f -n0 -o short-iso --grep='<união das regexes>'` (kernel +
`_SYSTEMD_UNIT=bluetooth.service` via match `+`) pipe em `awk` que classifica a tag pela
regex que casou e anexa; loop lateral (a cada 300 s) lê `hciconfig hci0` e emite `[BT-ERR]`
só no delta. Mesmíssimo modelo de permissão do storm_watch (grupo systemd-journal; probe de
permissão e RestartSec=300 mantidos). Doctor: nova subseção que conta ocorrências por tag no
boot corrente e traduz pro leigo ("8BitDo levou rate-limit do kernel N vezes → provável
escritor de LED em loop").

## §7 — Recomendações finais

**[DEFAULT-SEGURO]** (entram no install SEM FLAG, com uninstall simétrico + doctor + teste):

1. `assets/81-hefesto-usb-power.rules` (§2) — devices: Sony/Nintendo/8BitDo/Microsoft + BT
   classe e0. Evidência: baseline atual da máquina já é este estado (via Aurora) e é o estado
   sem storm; regra escreve o mesmo valor onde já coberto (inócua, idempotente).
2. `assets/81-hefesto-usb-host-power.rules` (§2) — hosts PCI classe 0x0c03*. Evidência:
   storm de maio derrubava o barramento inteiro; Aurora já roda regra equivalente
   (DRIVER=="xhci_hcd") sem efeito colateral desde então.
3. `assets/modprobe.d/hefesto-btusb-no-autosuspend.conf` (§5) — fecha o furo
   `btusb.enable_autosuspend=Y` (provado por modinfo) para máquinas virgens e adaptadores
   composite.
4. Passo cmdline do install (§1): garantir `usbcore.autosuspend=-1` +
   `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` via kernelstub com detecção de dono
   (nesta máquina = no-op registrado "terceiro/Aurora") e regra de MERGE do token único de
   usbcore.quirks. Nunca reintroduzir `:k`/max_cstate/threadirqs (removidos de propósito).
5. kernel-watch (§6): padrões USB-71 (já provados) + JOYCON (provado ao vivo 18/07) +
   snapshot de contadores hci — tudo read-only, mesmo modelo de unit atual.
6. Doctor "Energia USB" ampliado: power/control de devices E hosts, ASPM via /proc/cmdline
   (NUNCA pela policy sysfs — armadilha provada §3), sabotadores (§4: hoje só system76-power;
   checar scsi link PM + presença de TLP/powertop/tuned), clone DS4 por Modalias (§6).

**[INVESTIGAR-MAIS]** (não entram como default sem prova adicional):

7. `usbhid.jspoll` (§5): global, unidade muda por speed (exponente em high-speed!), cobertura
   de usage GAMEPAD não confirmada neste kernel. Protocolo de prova com
   `scripts/benchmark_polling.py` + replug descrito no §5. DualSense já está em 250 Hz.
8. Padrões `[XHCI]`/`[BT-HCI]` do kernel-watch: strings de fonte upstream, zero ocorrência
   local — shipar como vigília, mas calibrar regex contra falso-positivo no primeiro mundo
   real (não alarmar o leigo sem confirmação).
9. Política ASPM alternativa a `off` (ex.: `performance`): sem dado local que justifique
   mudança; `pcie_aspm=off` é da Aurora e funciona — doctor apenas reporta (§3).
10. `usbhid.quirks` para clones USB: veículo certo existe, caso real ainda não — especificar
    quando um clone USB problemático aparecer.

— fim do estudo —
