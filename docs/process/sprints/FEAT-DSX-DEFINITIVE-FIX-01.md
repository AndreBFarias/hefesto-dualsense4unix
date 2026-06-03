# FEAT-DSX-DEFINITIVE-FIX-01 — Storm -71 do DualSense + HDMI piscando (Steam quebra)

> **Se você reiniciou e "não deu certo", vá direto pra seção [§7 PLAYBOOK](#7-playbook-se-nao-deu-certo).**
> Status: **IMPLEMENTADO, APLICADO e REBOOT FEITO em 2026-06-03** — kernel (fbdev/quirks/max_cstate)
> LIVE em `/proc/cmdline`; commitado (`97d5181` + `af799fe`). Pós-reboot o HDMI parou de piscar e o
> DualSense enumera limpo no boot; o storm `-71` *da Steam* exige a escalada estrutural de §8
> (Bluetooth + porta do chipset).

---

## 1. Sintoma

Desde o commit `50d5f02` o controle funcionava. A Steam atualizou e voltou: **o DualSense
fica conectando/desconectando** e o **HDMI pisca em sincronia**. Mesmo cabo, mesma porta (a que
sempre deu certo), mesmo controle. BIOS (Power Supply Idle Control = Typical Current Idle) já
confirmado correto pela usuária. Portas e cabo já esgotados — exigia solução **de software**.

## 2. Causa-raiz (confirmada por logs ao vivo)

Máquina: **Ryzen Matisse (sem iGPU) + NVIDIA RTX 4060**, Pop!_OS COSMIC/Wayland.
**Não há GPU AMD** (zero `amdgpu`/`dmcub` no journal — o "dmcub watchdog" era do notebook antigo).

Topologia PCI (de `lspci -tvnn` e `/sys`):
- DualSense `054c:0ce6` → `usb3` → controlador USB do **Ryzen `0c:00.3`** (Bus 3).
- RTX 4060 `0a:00.0` → ponte `00:03.1` = **linhas PCIe x16 do mesmo I/O die do Ryzen**.
- Teclado/mouse (dongles) → **chipset `02:00.0`** (Bus 1) — outro silício, **nunca caem**.

**O DualSense e a GPU moram no mesmo I/O die do Ryzen.** Cadeia de 3 camadas, da timeline do
boot de 2026-06-03 (`journalctl -b -k`):

1. **Substrato (HW):** o controlador Matisse tem a fragilidade clássica AMD do `-71` (EPROTO).
   Há `-71` já no boot (00:32:55), independente da Steam.
2. **Gatilho (SW):** a **Steam subindo** (Proton/DXVK → `NVRM: Xid 32 d3ddriverquery6` às 00:34:28;
   game `2358720`) provoca transição de power CPU/GPU no I/O die e **força re-enumeração** do
   DualSense → **storm de `-71`** (00:35:53→00:37:18, device pulando 6→13, portas 3-13-2).
   PSSupport estava `0` e mesmo assim quebrou — o gatilho é a atividade da Steam, não só o PSSupport.
3. **HDMI piscando:** cada re-enumeração + a pressão de memória (applets do painel COSMIC mortos
   com **código 137 / OOM** às 00:37:26) faz o **cosmic-comp reconfigurar output**
   (`Failed to destroy old mode property blob`, `Failed to set xwayland primary output`) → modeset
   → tela pisca. **A GPU não cai** (zero Xid 79).

> Honestidade: o `-71` é fragilidade do **controlador Ryzen**; software não reescreve o silício.
> A estratégia é (a) **matar o gatilho**, (b) **desacoplar o HDMI do USB** (mata o sintoma visível),
> (c) **auto-curar** o controle em segundos, (d) **tornar visível** o `-71`.

## 3. O que foi implementado (e onde)

| # | Peça | Arquivo | Precisa reboot? | Aplicado nesta sessão? |
|---|------|---------|:---:|:---:|
| 1 | `dsx.sh` (botão 1-clique) + launcher | `dsx.sh`, `assets/dsx.desktop` | não | criado (launcher: rode `./dsx.sh --install-launcher`) |
| 2 | WirePlumber só-HID (mic do DualSense desligado) | `scripts/fix_wireplumber_default_source.sh --disable-source`, `assets/wireplumber/52-…conf` | não | **SIM** |
| 3 | doctor: diagnóstico `-71` + fix do false-success | `scripts/doctor.sh` (`--watch-dropout`, seção `USB / dropout`) | não | **SIM** |
| 4 | Guard do Steam Input (path+timer, `--apply-quiet`) | `assets/hefesto-steam-input-guard.{path,service,timer}`, `scripts/disable_steam_input.sh` | não | **SIM (ativo)** |
| 5 | Watcher de auto-recuperação do storm | `scripts/dsx_recover.sh`, `assets/hefesto-dsx-recover.service` | não | **SIM (ativo, root)** |
| 6a | Kernel: `nvidia-drm.fbdev=1` + `usbcore.quirks=054c:0ce6:k` + `processor.max_cstate=1` | `~/.config/zsh/scripts/ritual-aurora-self-heal.sh` | **SIM** | **SIM — reboot feito, LIVE em `/proc/cmdline`** |
| 6b | Fixar GPU `0a:00.0`/`.1` `power/control=on` | idem (`validate_power_state`) | não | **SIM** (era `auto`, virou `on`) |
| 6c | earlyoom: `--avoid` cobre `cosmic-panel`/applets | `~/.config/zsh/scripts/earlyoom.default` | não | **SIM** |

## 4. Estado LIVE confirmado nesta sessão (2026-06-03)

- `pactl get-default-source` → **não é o mic do DualSense** (o `alsa_input` do controle sumiu;
  o `.monitor` do sink é loopback inofensivo). doctor: `[ OK ]`.
- `cat /etc/kernelstub/configuration` → contém `nvidia-drm.fbdev=1` e `usbcore.quirks=054c:0ce6:k`.
- `cat /sys/bus/pci/devices/0000:0a:00.0/power/control` → `on` (era `auto`).
- `systemctl --user is-active hefesto-steam-input-guard.{path,timer}` → `active`.
- `sudo systemctl is-active hefesto-dsx-recover.service` → `active` (watcher vigiando o journal).
- `grep cosmic-panel /etc/default/earlyoom` → presente.
- **(2026-06-03, 2a leva)** `aplay -l | grep -i dualsense` → **vazio** (áudio USB do controle desligado
  pela regra `75-…`; HID `js0` intacto). `cat /etc/kernelstub/configuration | grep max_cstate` →
  `processor.max_cstate=1` registrado.
- **(2026-06-03, pós-reboot)** `/proc/cmdline` tem `nvidia-drm.fbdev=1` + `usbcore.quirks=054c:0ce6:k`
  + `processor.max_cstate=1` LIVE; dmesg: `nvidia-drmdrmfb (fb0) is primary device`. O DualSense
  (Bus 3, Matisse) **enumera limpo no boot, zero `-71`**. Os ~6-7 `error -71` do boot são todos de
  `usb 1-5` = **Bus 1 = chipset `02:00.0`** = a **webcam (porta 7)** falhando enumeração — **NÃO** o
  DualSense. (`doctor.sh` agora atribui isso corretamente — antes culpava o Matisse por heurística.)

## 5. Reboot — FEITO (2026-06-03)

O reboot já foi dado. `/proc/cmdline` confirma `nvidia-drm.fbdev=1`, `usbcore.quirks=054c:0ce6:k` e
`processor.max_cstate=1` LIVE; o dmesg mostra `fbcon: nvidia-drmdrmfb (fb0) is primary device` (fbdev
ativo). **Resultado:** o HDMI deixou de piscar no modeset e o DualSense (Matisse, Bus 3) **enumera
limpo no boot**. PORÉM o storm `-71` *da Steam* (sob carga de GPU) ainda não está provado eliminado —
a escalada estrutural de §8 (Bluetooth + porta do chipset) é o caminho definitivo.

```bash
cat /proc/cmdline | tr ' ' '\n' | grep -E 'nvidia-drm|usbcore|max_cstate'
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
> **Nota (2026-06-03, 2a leva): a Opção A abaixo JÁ FOI FEITA** — a regra
> `75-ps5-controller-disable-usb-audio.rules` deixa o controle pure-HID no USB. Se mesmo assim o
> `-71` persiste, o gatilho NÃO é o áudio → vá direto pras rotas de hardware (§8.B BIOS / §8.C BT /
> §8.D porta do chipset), que atacam a raiz no controlador.

**Opção A — bloquear `snd-usb-audio` no DualSense (FEITO):** a regra `75-…` faz `unbind` das
interfaces de áudio (`3-2:1.0/.1/.2`) no evento `bind`, deixando só a HID (`3-2:1.3`). Controle
**só-HID de verdade no nível USB** (perde áudio out também). Reverter: remover o `75-…` + replugar.

**Opção B — desligar o sink do DualSense no WirePlumber também:** estender o drop-in 52 para casar
`alsa_output.*[Dd]ual[Ss]ense.*` com `node.disabled = true` (além do `alsa_input`). Menos profundo
que A (o kernel ainda enumera), mas tira o PipeWire de cima da placa.

**Opção C — Bluetooth:** parear o DualSense por BT remove a interface de áudio USB inteira (e o
mic-USB de brinde). Ressalva: o dongle BT (Realtek, `054c`… não — `2357:012d`) está no **mesmo
controlador Matisse** (Bus 4), então não é imunidade total ao `-71` do die, mas o protocolo BT
(L2CAP) é mais resiliente que HID-over-USB a glitches de barramento.

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
sudo kernelstub --delete-options "usbcore.quirks=054c:0ce6:k"
# (mas o self-heal da Aurora re-adiciona no próximo run — remova também das linhas
#  ensure_kernel_option em ~/.config/zsh/scripts/ritual-aurora-self-heal.sh)
```

## 8. Rotas DEFINITIVAS (todas as 4 escolhidas em 2026-06-03)

A usuária pediu o arsenal completo. Tier 2 (software) já aplicado; Tier 1 (BIOS/BT/porta) é ação dela.

### 8.A — Software agressivo (APLICADO; reversível)
- **`processor.max_cstate=1`** no kernelstub (limita C-state ao C1; `acpi_idle` expõe POLL/C1/C2).
  Mantém o I/O die mais acordado. **Vale após reboot.** Reverter:
  `sudo kernelstub --delete-options "processor.max_cstate=1"` + tirar a linha do self-heal.
- **DualSense pure-HID no USB** — regra `assets/75-ps5-controller-disable-usb-audio.rules` desliga
  as 3 interfaces de áudio USB (classe 01), deixando só a HID (classe 03). Testado ao vivo: áudio
  some, `js0` intacto, nenhum `-71` disparado. Instalada em `/etc/udev/rules.d/75-…`. **Trade-off:
  o controle perde áudio POR INTEIRO** (sem mic e sem fone do jack). Opt-in via
  `install_udev.sh --disable-usb-audio` (o `dsx.sh` já passa essa flag). Reverter: remover o `75-…`
  + replugar. **Confiança ~40-60%** (se o gatilho for re-init de áudio pela Steam, ajuda muito).
- **GPU**: já fixada `power/control=on` (impede RTD3/blip do link PCIe) + `nvidia-drm.fbdev=1`.
  Travar clock (`nvidia-smi -lgc`) NÃO foi aplicado — custo de calor/energia 24/7 alto para ganho
  marginal; disponível se quiser testar.

### 8.B — BIOS (ação da usuária) — C-states já feitos; falta voltagem + AGESA
**Atualização 2026-06-03 (foto da BIOS):** a usuária **já tem** `Global C-state Control = Disabled` E
`Power Supply Idle Control = Typical Current Idle`. Ou seja, o lever de C-state que os docs marcavam
como "maior confiança" **já está aplicado e mesmo assim o storm volta após update da Steam** → o
C-state está esgotado. A raiz é mais profunda (contention GPU/PCIe + voltagem SoC/IF no I/O die).
Levers que **ainda faltam** (placa **Gigabyte B450M S2H**, BIOS F67d):
- **DF C-States (Data Fabric) = Disabled** — *Settings/Advanced → AMD CBS → DF Common Options*. Único
  C-state ainda não confirmado (se a BIOS expuser). Baixo esforço.
- **Undervolt SoC + IF** — a RAM a 3817 MHz (XMP/DOCP) **supervolta o SoC+IF**, que desestabiliza o
  I/O die/USB. *M.I.T. → Advanced Voltage*: **VCORE SOC** Auto → **1.05–1.10 V**; reduzir **VDDG/VDDP**
  junto. Teste primeiro com **XMP off** (diagnóstico): se o `-71` sumir, confirma a voltagem; então
  reabilite XMP com SoC manual. ~40% de sucesso relatado; ataca a raiz. Reversível (volta p/ Auto).
- **Update BIOS F67d → última estável** (Q-Flash) — AGESA mais novo; marginal, mas higiene.  reseta
  C-states/voltagem **e** a entry de boot do Windows (recriar depois).
- Trade-off: idle um pouco mais quente. Anda junto com tirar o dsx do Matisse (§8.C/§8.D).

### 8.C — Bluetooth (definitivo; sidestepa o USB)
O `-71` é erro de **enumeração USB**; por BT o controle não é device USB → o storm não existe.
`hid_playstation` suporta DualSense por BT.
```bash
bluetoothctl
  power on
  scan on
# no controle: segure PS + Create (botão de cima ao lado do touchpad) até a lightbar PISCAR rápido
  pair <MAC_do_DualSense>
  trust <MAC_do_DualSense>
  connect <MAC_do_DualSense>
```
Ressalva: seu **dongle BT está na Bus 4 (Matisse)** — o tráfego BT é tolerante, mas se quiser à prova
de bala mova-o pra porta do chipset (§8.D). Trade-off: latência mínima (6–13 ms), carregar o controle.

> **ESCOLHA 2026-06-03 (híbrido):** Bluetooth para JOGAR + cabo na **porta 8 (chipset)** para
> carregar/usar com fio — os dois caminhos ficam fora do Matisse frágil. **Nunca** mais a porta 3.

### 8.D — Porta do chipset (determinístico, NÃO é adivinhação)
Mapa real desta máquina (numeração da usuária 1–8):
- **Bus 1 + Bus 2 = chipset `02:00.0` (ROBUSTO)** — teclado (1), mouse (2) na frente; portas traseiras
  pretas USB2 (**7, 8**) atrás. Nunca caem.
- **Bus 3 + Bus 4 = Matisse `0c:00.3` (FRÁGIL)** — DualSense (porta 3), wifi (5), dongle BT (6).
- **Topologia-alvo:** dsx (cabo) → **porta 8 (chipset)**; webcam sai da **porta 7** (onde dá `-71` de
  boot) para a **porta 4** (Matisse azul, vazia — webcam tolera). Deixa a porta 7 (suspeita) vazia.

Como achar a porta física do chipset (verificação, não chute):
```bash
# pluga o controle numa porta e roda:
lsusb -t | grep -iB2 dualsense
# Bus 001 ou Bus 002 no topo do bloco = porta do CHIPSET (robusta). Fim do problema.
# Bus 003/004 = Matisse — tenta outra porta.
# Dica: as portas onde o teclado/mouse estão HOJE sao do chipset — use as vizinhas.
```
O `doctor.sh` (seção USB/dropout) também diz em qual controlador o controle está a cada checagem.

## 9. Sprints relacionadas (implementadas aqui)
- `FEAT-WIREPLUMBER-DISABLE-SOURCE-MODE-01` → modo `--disable-source` (item 2). **DONE.**
- `BUG-WIREPLUMBER-FIX-FALSE-SUCCESS-01` → doctor/fix checam o ATIVO, não o configured (item 3). **DONE.**
- `FEAT-DOCTOR-USB-DROPOUT-DIAGNOSTIC-01` → seção USB/dropout + `--watch-dropout` (item 3). **DONE.**
- `FEAT-STEAM-INPUT-SELF-HEAL-01` → guard path+timer (item 4). **DONE.**
- `FEAT-DSX-RECOVER-01` → watcher de auto-recuperação (item 5). **DONE.**
