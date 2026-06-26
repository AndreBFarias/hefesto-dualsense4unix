# 2026-06-26 — A causa REAL do storm do DualSense é a enumeração do ÁUDIO USB (mic)

> Continuação de `2026-06-23-storm-71-porta-usb-vs-config.md`. Sessão de investigação
> que rastreou, por eliminação, o "controle conecta/desconecta quando jogo" até a causa real.

## TL;DR

O flap do DualSense **NÃO é** cabo, porta, die do Ryzen nem conflito de software de usuário.
É a **enumeração das interfaces de ÁUDIO USB do controle** (o "microfone") sobre um link USB já no
limite. Prova A/B limpa: **áudio ligado → storm** (16 desconexões / 25 s, `-71`, em qualquer porta,
inclusive a do chipset); **áudio desligado (regra 75)** → **0 desconexões, estável até na 3-1
"frágil"**. O storm é **disparado por carga/estado** (jogo, troca de profile, re-enum), não por
"áudio ligado = cai sempre" — em repouso o áudio fica bindado e estável; sob estresse, desaba.

A Vitória estava certa o tempo todo que **não era a porta nem o cabo** — foi um erro de condução
ter ido por "trocar de porta" (3-1 → 3-4 → 1-6, todas falham com áudio on; todas estáveis com
áudio off).

## Como chegamos lá (linha do tempo da eliminação)

1. **Guerra do PSSupport (resolvida)** — o Ritual da Aurora forçava `SteamController_PSSupport=2`
   (Steam gerencia o DualSense) e o hefesto força `=0`. As duas brigando no mesmo `localconfig.vdf`
   → Steam re-pegava o hidraw em rajadas → re-enumeração LIMPA (sem `-71`). Resolvido: desativada a
   feature `aurora-steam-input-fix` no Ritual (v3.23) + `PSSupport=0`. (Esse era um flap REAL, mas
   diferente do storm.)
2. **Topologia USB mapeada** — `lsusb -t` + PCI: chipset `02:00.0` = **Bus 1/2** (robusto, onde
   teclado/mouse vivem e NUNCA caem); Matisse/Ryzen `0c:00.3` = **Bus 3/4** (frágil; DualSense e
   dongle BT). 3-1 e 3-4 são o MESMO controlador frágil. Mover entre eles não resolveu.
3. **Eliminação de software** — parado o daemon do hefesto: ainda flapa. Parado TAMBÉM o
   WirePlumber: ainda flapa. Logo não é software de usuário; é o **kernel `snd-usb-audio`** montando
   as 3 interfaces de áudio na enumeração.
4. **Teste decisivo (A/B do áudio)** — aplicada a **regra 75** (`install_udev.sh --disable-usb-audio`,
   que dá `unbind` do snd-usb-audio nas interfaces classe 01): **storm parou na hora** (0/30 s),
   estável até na 3-1. Removendo o áudio (mantendo tudo o mais) = fim do storm. **Causa confirmada.**

## Sequência exata da falha (do journal, com áudio ON)

```
playstation 0003:054C:0CE6...: Failed to retrieve feature with reportID 9: -71
playstation ...: Failed to get MAC address from DualSense / Failed to create dualsense.
playstation ...: probe with driver playstation failed with error -71
usb 1-6: 1:1: usb_set_interface failed (-19)
usb 1-6: 2:0: failed to get current value for ch 0 (-22)   # interface de ÁUDIO
usb 1-6: 5:0: cannot get min/max values for control 2
usbhid ...: probe with driver usbhid failed with error -71
usb 1-6: device descriptor read/64, error -71
```

Tanto o HID (`playstation`) quanto o áudio falham com `-71` **juntos, só quando o áudio entra**.
Mecanismo: a enumeração do áudio é uma rajada pesada de control-transfers no EP0; o link não
aguenta HOJE e tomba no meio. Só-HID (enum leve) passa. "Funcionava antes" = a margem do link era
suficiente e caiu — **a causa da queda de margem não foi identificada** (não é a config de áudio:
testado com daemon+WirePlumber parados).

## Mudanças aplicadas nesta sessão

### Ritual da Aurora (`~/.config/zsh/scripts/ritual-aurora-self-heal.sh`)
- **v3.23**: desativada a feature `aurora-steam-input-fix` (forçava PSSupport=2). Teardown da
  `aurora-steam-input.service` + script.
- **v3.24**: removidas as opções de kernel `usbcore.quirks=054c:0ce6:k` (NO_LPM, efeito nulo num
  USB-2) e `processor.max_cstate=1` (custo de CPU, redundante com o BIOS C-state). Comentadas no
  self-heal (não re-adiciona) + removidas do bootloader via `kernelstub --delete-options`.
  **Mantidas** (pró-estabilidade, baixo custo): `pcie_aspm=off`, `usbcore.autosuspend=-1`.

### Sistema (runtime)
- `SteamController_PSSupport=0` fixado no `localconfig.vdf` (guard do hefesto mantém).
- **regra 75** instalada em `/etc/udev/rules.d/75-ps5-controller-disable-usb-audio.rules` →
  controle estável SEM mic. **Caveat: a regra 75 é racy** (o `RUN+= unbind` corre contra o kernel)
  e às vezes NÃO pega numa reconexão — então o áudio volta a bindar e o storm pode reincidir.
- WirePlumber: drop-ins 51/52 removidos; estado persistido ainda tem `pro-audio` + default-source =
  DualSense (stale — com áudio off cai no monitor HDMI). Limpar quando definir o rumo do mic.
- env `HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED=1` em `~/.config/environment.d/` (inócuo com
  áudio off; reavaliar).

### hefesto
- Daemon reinstalado (`./install.sh --enable-autostart --no-hotplug-gui --no-cosmic-applet`),
  autostart ON. **Triggers/haptics/LED/perfis funcionam plenos com o áudio off** (testado ao vivo:
  Rigid no R2, Galloping no L2, rumble, lightbar — 0 desconexões).
- Patch `FEAT-DUALSENSE-MIC-INTENDED-01` (commit no fork): `system_check.py` respeita o env e o
  `fix_wireplumber_default_source.sh` ganhou modo `--enable-mic`.

## Estado atual / o que jogar agora

- **Pronto pra jogar**: controle estável + hefesto pleno, COM o áudio off. Mic de voz pela
  webcam C920.
- **Mic do controle**: indisponível com a regra 75. Para tê-lo de volta + estável precisa que a
  enumeração do áudio passe — é o objeto do teste pós-reboot.

## Pendências / próximos passos

1. **Reboot test (FEITO — não resolveu)**: com o kernel limpo (sem quirks/max_cstate), pós-reboot
   removida a regra 75 — o áudio **NÃO** enumerou sem storm. "Apenas rebootar" **não** é a alavanca:
   a enumeração do áudio só passa sem storm com o quirk `gn` (item 2), que espaça a rajada de
   control-transfers. Detalhe e prova no doc canônico
   `docs/process/discoveries/2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md`.
2. **Quirk é a alavanca que PRESERVA o áudio.** A pesquisa profunda refinou o quirk de
   `054c:0ce6:n` (só `n`=`DELAY_CTRL_MSG`, só o PID 0ce6) para
   `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` — `g` (`DELAY_INIT`) **+** `n` (`DELAY_CTRL_MSG`) nos
   DOIS PIDs do DualSense (0ce6 e 0df2). Esse quirk espaça a rajada da enumeração control-heavy e
   mantém o mic/fone vivos (alternativa à regra 75, que desliga o áudio). Aplicação:
   `scripts/install_usb_quirk.sh` ou `./install.sh --with-usb-quirk`. Ver o doc canônico acima.
3. **regra 75 racy**: se for o caminho definitivo (áudio off), trocar o `RUN+= unbind` por um
   mecanismo confiável (impedir o bind em vez de desfazer depois).
4. **Bug de GUI (combobox)**: dropdowns do GTK3 sob COSMIC exigem segurar o clique (abrem em modo
   arrasta-pra-selecionar). Já roda em XWayland (`GDK_BACKEND=x11`) e mesmo assim buga → é do app.
   Workaround: usar a TUI (`hefesto-dualsense4unix tui`) ou o CLI. **Bug a tratar no projeto.**
5. **PS button**: toque curto = Steam; **segurar ~1 s = toggle da emulação mouse+teclado**
   (FEAT-EMULATION-GAMEMODE-LONGPRESS-01, limiar 1000 ms). Confirmar sincronia ao vivo com a GUI.
