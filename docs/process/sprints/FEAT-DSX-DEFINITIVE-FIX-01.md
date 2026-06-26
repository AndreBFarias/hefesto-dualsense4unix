# FEAT-DSX-DEFINITIVE-FIX-01 — Storm -71 do DualSense + HDMI piscando (Steam quebra)

> **Se você reiniciou e "não deu certo", vá direto pra seção [§7 PLAYBOOK](#7-playbook-se-nao-deu-certo).**
> Status: **CAUSA-RAIZ RESOLVIDA em 2026-06-26** — o storm `-71` é a **enumeração das interfaces de
> áudio USB** (`snd-usb-audio`) sob carga: uma rajada de control-transfers no EP0 tomba o link →
> `-71` → re-enum. O caminho definitivo é UMA das duas alavancas: **(D) quirk de cmdline
> `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`** (espaça a rajada, PRESERVA o áudio no nível kernel) OU
> **(A) regra udev `75-…` (`authorized=0`)** que desliga o áudio. Provado A/B 2026-06-26:
> áudio off = 0 storm em qualquer porta (port-independente). Ver canônico:
> `docs/process/discoveries/2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md`.
> A teoria antiga do "I/O die do Ryzen + Bluetooth + porta do chipset" foi **SUPERADA**.

---

## 1. Sintoma

Desde o commit `50d5f02` o controle funcionava. A Steam atualizou e voltou: **o DualSense
fica conectando/desconectando** e o **HDMI pisca em sincronia**. Mesmo cabo, mesma porta (a que
sempre deu certo), mesmo controle. BIOS (Power Supply Idle Control = Typical Current Idle) já
confirmado correto pela usuária. Portas e cabo já esgotados — exigia solução **de software**.

## 2. Causa-raiz (confirmada por A/B + pesquisa profunda 2026-06-26)

> **Teoria do "I/O die do Ryzen" SUPERADA em 2026-06-26.** A versão antiga desta seção culpava a
> fragilidade do silício do controlador + contention GPU/PCIe. Isso foi **refutado**: o storm é
> **port-independente** (A/B provado: áudio off = 0 storm em QUALQUER porta, inclusive a do chipset)
> e some quando o áudio USB do controle não enumera. Não é HW de barramento, não é BIOS, não é cabo.

Máquina: **Ryzen 7 5800X (Vermeer, sem iGPU) + NVIDIA RTX 4060**, Pop!_OS COSMIC/Wayland.

**Mecanismo real:** o storm `-71` (EPROTO) é disparado pela **enumeração das interfaces de áudio USB
do DualSense** (`054c:0ce6` e o modo `054c:0df2`) pelo driver `snd-usb-audio`. Sob carga, o probe do
áudio dispara uma **rajada de control-transfers no endpoint EP0** (ler/setar descritores de áudio,
clocks, terminais) que **satura o EP0 e tomba o link** → `-71` → o kernel re-enumera o device →
nova rajada → **storm** auto-sustentado. O gatilho de carga (Steam/Proton subindo) só intensifica a
re-enumeração; a **raiz é a rajada de áudio**, não a atividade da GPU.

Topologia PCI (referência, NÃO é a causa):
- DualSense `054c:0ce6` → controlador USB do Ryzen (Bus 3).
- Teclado/mouse → chipset `02:00.0` (Bus 1).

Prova A/B (2026-06-26, ao vivo — PRAGMATA):
- **Áudio USB ON, sem quirk** → storm `-71` reproduzível sob carga, em qualquer porta.
- **Áudio USB OFF** (regra `75-…`, `authorized=0`) → **0 quedas**, em qualquer porta (inclusive chipset).
- **Áudio USB ON + quirk `gn,gn`** (espaça a rajada) → **0 quedas** com o áudio preservado no kernel.

**HDMI piscando:** consequência secundária — cada re-enumeração + a pressão de memória (applets do
painel COSMIC mortos com código 137 / OOM) faz o **cosmic-comp reconfigurar output** (`Failed to
destroy old mode property blob`, `Failed to set xwayland primary output`) → modeset → tela pisca.
Some quando o storm para. A GPU não cai (zero Xid 79).

> Estratégia definitiva: **eliminar a rajada de áudio** — ou pelo **quirk `gn,gn`** (espaça os
> control-transfers, preserva o áudio no nível kernel) ou pela **regra 75** (não enumera o áudio).
> O HDMI/auto-cura/visibilidade do `-71` viram mitigações secundárias, não o fix.

## 3. O que foi implementado (e onde)

| # | Peça | Arquivo | Precisa reboot? | Aplicado nesta sessão? |
|---|------|---------|:---:|:---:|
| 1 | `dsx.sh` (botão 1-clique) + launcher | `dsx.sh`, `assets/dsx.desktop` | não | criado (launcher: rode `./dsx.sh --install-launcher`) |
| 2 | WirePlumber só-HID (mic do DualSense desligado) | `scripts/fix_wireplumber_default_source.sh --disable-source`, `assets/wireplumber/52-…conf` | não | **SIM** |
| 3 | doctor: diagnóstico `-71` + fix do false-success | `scripts/doctor.sh` (`--watch-dropout`, seção `USB / dropout`) | não | **SIM** |
| 4 | Guard do Steam Input (path+timer, `--apply-quiet`) | `assets/hefesto-steam-input-guard.{path,service,timer}`, `scripts/disable_steam_input.sh` | não | **SIM (ativo)** |
| 5 | Watcher de auto-recuperação do storm | `scripts/dsx_recover.sh`, `assets/hefesto-dsx-recover.service` | não | **SIM (ativo, root)** |
| 6a | Kernel: `nvidia-drm.fbdev=1` + `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` (HDMI + storm de áudio) | `~/.config/zsh/scripts/ritual-aurora-self-heal.sh` | **SIM** | **SIM** — `:k` (NO_LPM) era no-op em USB-2, REMOVIDO; `processor.max_cstate=1` REMOVIDO (v3.24, fora do fix) |
| 6b | Fixar GPU `0a:00.0`/`.1` `power/control=on` | idem (`validate_power_state`) | não | **SIM** (era `auto`, virou `on`) |
| 6c | earlyoom: `--avoid` cobre `cosmic-panel`/applets | `~/.config/zsh/scripts/earlyoom.default` | não | **SIM** |

## 4. Estado LIVE confirmado nesta sessão (2026-06-03)

- `pactl get-default-source` → **não é o mic do DualSense** (o `alsa_input` do controle sumiu;
  o `.monitor` do sink é loopback inofensivo). doctor: `[ OK ]`.
- `cat /etc/kernelstub/configuration` → contém `nvidia-drm.fbdev=1` e o quirk de áudio
  `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` (o `:k`/NO_LPM antigo era no-op em USB-2, removido).
- `cat /sys/bus/pci/devices/0000:0a:00.0/power/control` → `on` (era `auto`).
- `systemctl --user is-active hefesto-steam-input-guard.{path,timer}` → `active`.
- `sudo systemctl is-active hefesto-dsx-recover.service` → `active` (watcher vigiando o journal).
- `grep cosmic-panel /etc/default/earlyoom` → presente.
- **(2026-06-03, 2a leva)** `aplay -l | grep -i dualsense` → **vazio** (áudio USB do controle desligado
  pela regra `75-…`; HID `js0` intacto). NOTA (v3.24): `processor.max_cstate=1` foi **REMOVIDO** — não
  faz parte do fix (não mexe na rajada de áudio do EP0).
- **(2026-06-03, pós-reboot)** `/proc/cmdline` tem `nvidia-drm.fbdev=1` + o quirk de áudio
  `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` LIVE; dmesg: `nvidia-drmdrmfb (fb0) is primary device`. O
  DualSense (Bus 3) **enumera limpo no boot, zero `-71`**. Os ~6-7 `error -71` do boot são de `usb 1-5`
  = **Bus 1 = chipset `02:00.0`** = a **webcam (porta 7)** falhando enumeração — **NÃO** o DualSense.

## 5. Reboot — FEITO (2026-06-03); causa-raiz fechada (2026-06-26)

O reboot já foi dado. `/proc/cmdline` confirma `nvidia-drm.fbdev=1` e o quirk de áudio
`usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` LIVE; o dmesg mostra `fbcon: nvidia-drmdrmfb (fb0) is
primary device` (fbdev ativo). **Resultado:** o HDMI deixou de piscar no modeset e o DualSense (Bus 3)
**enumera limpo no boot**. Em 2026-06-26 a causa-raiz foi fechada: o storm `-71` é a **rajada de
control-transfers do `snd-usb-audio` no EP0** (port-independente). O fix definitivo é o **quirk
`gn,gn`** (preserva o áudio) OU a **regra 75** (áudio-off); a escalada de hardware de §8 está
**SUPERADA**.

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'nvidia-drm|usbcore'
```

## 6. Contexto importante para a próxima sessão

- **O hefesto-daemon NÃO está instalado** (decisão de manter o sistema enxuto). O DualSense funciona
  direto pelo `hid_playstation` do kernel (`js0` presente, `DRIVER=playstation`). Por isso o
  `doctor.sh` mostra 2 `[FAIL]` esperados: "CLI não encontrado" e "nenhuma regra udev instalada".
  **Nosso fix é standalone** — depende de Aurora + watcher + guard + WirePlumber, NÃO do daemon.
- A separação de donos (ADR-018) foi respeitada: kernel/power global = Aurora; gatilho/auto-cura
  do DualSense = hefesto (`dsx.sh`, `scripts/`).
- Commitado em 2 commits no branch `feat/dsx-definitive-fix-usb-hdmi`: `97d5181` (fix base) +
  `af799fe` (rotas definitivas: pure-HID, max_cstate, guia BIOS/BT/porta).

---

## 7. PLAYBOOK "se não deu certo"

Rode na ordem. Cada passo tem o comando e o que concluir.

### 7.0 Botão rápido (tenta tudo de novo)
```bash
cd ~/Desenvolvimento/hefesto-dualsense4unix && ./dsx.sh
```

### 7.1 Confirmar o que de fato está quebrado
```bash
cd ~/Desenvolvimento/hefesto-dualsense4unix
scripts/doctor.sh | sed -n '/USB \/ dropout/,/────/p'   # quantos -71 neste boot?
```
- **0 sintomas `-71`** → o controle está estável neste boot. Se o HDMI ainda pisca, vá pra §7.4.
- **>0 sintomas** → o storm voltou. Continue.

### 7.2 O fbdev pegou? (HDMI piscando)
```bash
cat /proc/cmdline | tr ' ' '\n' | grep nvidia-drm   # tem 'nvidia-drm.fbdev=1'?
```
- Se **não tem fbdev** → o reboot não aplicou. Rode `sudo bash ~/.config/zsh/scripts/ritual-aurora-self-heal.sh`
  e **reinicie de novo**. Confirme `cat /etc/kernelstub/configuration | grep fbdev`.
- Se **tem fbdev e o HDMI ainda pisca** → vá pra §7.4.

### 7.3 O watcher de auto-recuperação está vivo?
```bash
systemctl status hefesto-dsx-recover.service
sudo journalctl -u hefesto-dsx-recover.service -n 40 --no-pager   # procure "recovery concluído"
```
- Se **inactive/failed** → reinstale: `cd ~/Desenvolvimento/hefesto-dualsense4unix && ./dsx.sh`
  (etapa "serviços"), ou manual:
  `sudo install -Dm755 scripts/dsx_recover.sh /usr/local/sbin/dsx_recover.sh && sudo systemctl enable --now hefesto-dsx-recover.service`.
- Se **active mas o controle fica morto >10s sem recuperar** → o re-bind via `authorized` não
  bastou (controlador glitchando feio). Vá pra §7.5 (escalada).

### 7.4 HDMI ainda pisca mesmo com fbdev
A GPU pode estar voltando pra `auto`. Confirme e re-fixe:
```bash
cat /sys/bus/pci/devices/0000:0a:00.0/power/control   # quer 'on'
sudo bash ~/.config/zsh/scripts/ritual-aurora-self-heal.sh   # re-fixa GPU + power
```
Se persistir, observe o que o compositor faz no instante do pisca:
```bash
journalctl -b -o short-precise | grep -iE 'cosmic-comp|drm|mode property|xwayland primary' | tail -30
```
- Se aparecer `Failed to destroy old mode property blob` junto com USB disconnect → ainda é o
  acoplamento USB→modeset. Escale o lado USB em §7.5 (matar o gatilho mais a fundo).

### 7.5 ESCALADA — se o storm `-71` persiste mesmo com tudo acima
> **Causa-raiz fechada (2026-06-26): o gatilho É o áudio USB.** O A/B (áudio off = 0 storm) e a
> pesquisa profunda confirmam que a rajada de control-transfers do probe do `snd-usb-audio` no EP0 é
> o que derruba o link → `-71`. NÃO é cabo/porta/BIOS (port-independente; a antiga "ida pras rotas de
> hardware §8" está **SUPERADA** — não escale pra HW). Detalhes e descritores reais em
> `docs/process/discoveries/2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md`.
> Use **a Opção D (quirk, preserva o áudio)** OU **a Opção A (áudio-off, perde o áudio)** — nunca as
> duas juntas.

**Opção A — bloquear `snd-usb-audio` no DualSense (FEITO):** a regra `75-…` deautoriza as interfaces
de áudio (`ATTR{authorized}="0"` no evento `add`, mecanismo PRIMÁRIO race-reduzido) e, como reforço,
faz `unbind` no evento `bind`, deixando só a HID (`3-2:1.3`). Controle **só-HID de verdade no nível
USB** (perde áudio out também). Reverter: remover o `75-…` + replugar (ou `echo 1 >
/sys/bus/usb/devices/<iface>/authorized`). Opt-in: `install_udev.sh --disable-usb-audio`.

**Opção B — desligar o sink do DualSense no WirePlumber também:** estender o drop-in 52 para casar
`alsa_output.*[Dd]ual[Ss]ense.*` com `node.disabled = true` (além do `alsa_input`). Menos profundo
que A (o kernel ainda enumera), mas tira o PipeWire de cima da placa.

**Opção C — Bluetooth (contorno de último recurso):** parear o DualSense por BT faz o controle deixar
de ser device USB — a interface de áudio USB **não existe**, logo a rajada de control-transfers no EP0
(causa do `-71`) **não tem como ocorrer**. É imune ao storm por construção, mas só fica como contorno
porque o quirk (D) ou a regra 75 (A) já resolvem no cabo. Trade-off: latência e carregar o controle.

**Opção D — quirk `DELAY_CTRL_MSG` (PRESERVA o áudio) ⭐ ALTERNATIVA à Opção A:** em vez de desligar
o áudio, **espaça** a rajada de control-transfers do probe para ela não tombar o link. Combina dois
flags do `usbcore.quirks`: `g` = `USB_QUIRK_DELAY_INIT` (pausa após ler o device descriptor) + `n` =
`USB_QUIRK_DELAY_CTRL_MSG` (pausa após CADA control message). O áudio ainda enumera, só mais devagar,
sem saturar o EP0. **Caveat:** o quirk preserva o áudio **no nível kernel** (mata o storm), mas se os
drop-ins WP `52`/`53` estiverem instalados o **nó do mic fica suprimido no PipeWire** — para de fato
usar o mic do DualSense você precisa **remover os drop-ins 52/53** e exportar
`HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED=1`.

- **Empacotado no repo (acionável, idempotente, reversível):**
  ```bash
  scripts/install_usb_quirk.sh            # aplica no bootloader (kernelstub/grub); vale no próximo boot
  scripts/install_usb_quirk.sh --status   # read-only: ativo (cmdline) / agendado (config) / runtime
  scripts/install_usb_quirk.sh --remove   # reverte (no-op se já ausente)
  scripts/install_usb_quirk.sh --runtime  # sysfs best-effort; só vale no próximo replug (não persiste)
  # ou, no fluxo de instalação (OPT-IN, default OFF):
  ./install.sh --with-usb-quirk
  ```
  O script é **ciente do bootloader** (kernelstub no Pop!_OS/System76; grub em outros) e
  **idempotente**: rodar 2x = no-op na 2a, nunca duplica o token. Se já existir um `usbcore.quirks=`
  **diferente**, ele **avisa e não adiciona um segundo às cegas** (o kernel respeita só UM token).
- **NÃO é uma regra udev — é cmdline do kernel.** Uma regra udev não consegue alterar o próprio
  enumeramento do device (o quirk precisa estar ativo ANTES do probe do `snd-usb-audio`); por isso
  vem como **passo de install** (`scripts/install_usb_quirk.sh`), não como `assets/*.rules`. Ele é a
  ⭐ **ALTERNATIVA à Opção A** (regra 75): a Opção D PRESERVA o áudio, a Opção A o descarta.
- **Runtime (sem reboot, aplica no próximo replug do controle), root:**
  ```bash
  echo '054c:0ce6:gn,054c:0df2:gn' > /sys/module/usbcore/parameters/quirks
  # depois: desconecte e reconecte o DualSense   (ou: scripts/install_usb_quirk.sh --runtime)
  ```
- **Persistente (cmdline):** `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`. O `install_usb_quirk.sh`
  edita o config do bootloader por você; em máquinas onde o cmdline é **domínio do Ritual da Aurora**
  (dona dos kernel params), a entrada também precisa entrar na allowlist da Aurora para não ser
  apagada no próximo self-heal — **coordenar com ela** nesse caso.
- **USE UMA OU OUTRA:** quirk (D) preserva o áudio; áudio-off (A, regra 75) descarta o áudio. Aplicar
  as duas é redundante e confunde o diagnóstico — escolha conforme você quer ou não o mic/fone.
- **Risco:** o burst só desacelerado ainda pode tombar sob carga; se não segurar, caia para a Opção A.
- Documentação completa (tabela de flags, mecanismo, prior-art): `docs/process/discoveries/
  2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md`.

Antes de escalar, **capture a evidência** do storm em tempo real pra sabermos o gatilho exato:
```bash
scripts/doctor.sh --watch-dropout    # deixe rodando e abra a Steam/um jogo; ele imprime o 1o -71
# em outro terminal, no mesmo instante:
journalctl -b -o short-precise | grep -iE 'usb 3-|steam|nvidia|Xid|cosmic-comp' | tail -50
```

### 7.6 Reverter qualquer peça (se algo piorou)
```bash
# WirePlumber só-HID  ->  volta o mic do controle
rm -f ~/.config/wireplumber/wireplumber.conf.d/52-hefesto-dualsense-disable-source.conf
systemctl --user restart wireplumber
# Guard do Steam Input
systemctl --user disable --now hefesto-steam-input-guard.path hefesto-steam-input-guard.timer
# Watcher
sudo systemctl disable --now hefesto-dsx-recover.service
# Kernel (fbdev/quirks) — editar e reboot
sudo kernelstub --delete-options "nvidia-drm.fbdev=1"
sudo kernelstub --delete-options "usbcore.quirks=054c:0ce6:gn,054c:0df2:gn"
# (mas o self-heal da Aurora re-adiciona no próximo run — remova também das linhas
#  ensure_kernel_option em ~/.config/zsh/scripts/ritual-aurora-self-heal.sh)
```

## 8. Rotas DEFINITIVAS — só a §8.A vale; o resto foi SUPERADO

> **Atualização 2026-06-26.** A causa-raiz é a rajada de áudio USB no EP0 (§2), **port-independente**.
> Por isso as rotas de hardware (BIOS/porta/Bluetooth) **deixaram de ser definitivas**: §8.B e §8.D
> estão **SUPERADAS** (não é BIOS, não é a porta) e §8.C (Bluetooth) fica só como contorno de último
> recurso. O fix definitivo é **software**: quirk `gn,gn` (§7.5 Opção D, preserva o áudio) OU regra 75
> (§8.A, áudio-off).

### 8.A — Software (DEFINITIVO; reversível)
- **DualSense pure-HID no USB (regra 75)** — `assets/75-ps5-controller-disable-usb-audio.rules`
  desliga as 3 interfaces de áudio USB (classe 01), deixando só a HID (classe 03): o `snd-usb-audio`
  não enumera, então a rajada de control-transfers do EP0 **não acontece** e o storm `-71` some. Áudio
  some, `js0` intacto. Instalada em `/etc/udev/rules.d/75-…`. **Trade-off: o controle perde áudio POR
  INTEIRO** (sem mic e sem fone do jack). Opt-in via `install_udev.sh --disable-usb-audio` (o `dsx.sh`
  já passa essa flag). Reverter: remover o `75-…` + replugar. **Confiança: PROVADO (A/B 2026-06-26:
  áudio-off = 0 storm, em qualquer porta).** Alternativa que PRESERVA o áudio: quirk `gn,gn` (§7.5 D).
- **`processor.max_cstate=1`** — **REMOVIDO (v3.24).** Não faz parte do fix: não toca na rajada de
  áudio do EP0 e o storm é port-independente. Mantido aqui só como registro histórico.
- **GPU**: `power/control=on` + `nvidia-drm.fbdev=1` continuam úteis para o HDMI parar de piscar (sintoma
  secundário), mas NÃO são o fix do `-71`. Travar clock (`nvidia-smi -lgc`) não foi aplicado.

### 8.B — BIOS (undervolt SoC/IF, C-states) — **SUPERADO (não é BIOS)**
> **SUPERADO 2026-06-26.** O storm é **port-independente** e some com o áudio USB desligado/espaçado
> (§2, A/B provado), o que **descarta** voltagem SoC/IF, DF C-States e AGESA como causa. A usuária já
> tinha `Global C-state Control = Disabled` + `Power Supply Idle Control = Typical Current Idle` e o
> storm voltava mesmo assim — coerente: o gatilho é a rajada de áudio no EP0, não o I/O die. **Não
> mexa na BIOS por causa do `-71`.** Mantido abaixo só como registro histórico (riscado).

~~Levers de BIOS que os docs antigos pediam (placa Gigabyte B450M S2H): DF C-States = Disabled;
undervolt VCORE SOC 1.05–1.10 V + VDDG/VDDP; teste com XMP off; update de AGESA. Todos partiam da
teoria do I/O die, hoje refutada.~~

### 8.C — Bluetooth — **só contorno de último recurso**
> Com o quirk `gn,gn` (§7.5 D) ou a regra 75 (§8.A) o problema já está resolvido **no cabo, com o
> áudio do jeito que você quiser**. O Bluetooth fica só como contorno se, por algum motivo, você não
> puder aplicar nenhuma das duas: por BT o controle não é device USB → a interface de áudio USB não
> existe → o storm `-71` não tem como ocorrer. `hid_playstation` suporta DualSense por BT.
```bash
bluetoothctl
  power on
  scan on
# no controle: segure PS + Create (botão de cima ao lado do touchpad) até a lightbar PISCAR rápido
  pair <MAC_do_DualSense>
  trust <MAC_do_DualSense>
  connect <MAC_do_DualSense>
```
Trade-off: latência um pouco maior (6–13 ms) e precisa carregar o controle. Não é mais "o definitivo"
— o definitivo é software (§7.5 D / §8.A).

### 8.D — Porta do chipset — **SUPERADO (port-independente)**
> **SUPERADO 2026-06-26.** O A/B provou que o storm é **port-independente**: com o áudio USB
> desligado/espaçado ele dá **0 quedas em QUALQUER porta**, inclusive a do chipset; e com o áudio ON
> sem quirk ele reaparece em qualquer porta. Logo, **trocar de porta NÃO é o fix** — a porta só muda
> o controlador que enumera o áudio, não a rajada de control-transfers no EP0 que causa o `-71`.
> Mantido abaixo como registro histórico (riscado).

~~Teoria antiga: mover o DualSense (cabo) para a porta do chipset (`02:00.0`, robusta) e tirar da
porta do Ryzen. `lsusb -t | grep -iB2 dualsense` mostrava o Bus; Bus 1/2 = chipset, Bus 3/4 = Ryzen.
Partia da hipótese (refutada) de que o controlador do Ryzen era "frágil".~~ O `doctor.sh` (seção
USB/dropout) ainda informa em qual controlador o controle está, mas isso é diagnóstico, não o fix.

## 9. Sprints relacionadas (implementadas aqui)
- `FEAT-WIREPLUMBER-DISABLE-SOURCE-MODE-01` → modo `--disable-source` (item 2). **DONE.**
- `BUG-WIREPLUMBER-FIX-FALSE-SUCCESS-01` → doctor/fix checam o ATIVO, não o configured (item 3). **DONE.**
- `FEAT-DOCTOR-USB-DROPOUT-DIAGNOSTIC-01` → seção USB/dropout + `--watch-dropout` (item 3). **DONE.**
- `FEAT-STEAM-INPUT-SELF-HEAL-01` → guard path+timer (item 4). **DONE.**
- `FEAT-DSX-RECOVER-01` → watcher de auto-recuperação (item 5). **DONE.**
