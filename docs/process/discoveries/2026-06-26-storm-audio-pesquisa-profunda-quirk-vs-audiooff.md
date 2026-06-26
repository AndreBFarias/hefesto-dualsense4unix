# 2026-06-26 — Pesquisa profunda do storm: enumeração do áudio USB, quirk DELAY_CTRL_MSG vs áudio-off

> Continuação de `2026-06-26-mic-usb-audio-e-a-causa-real-do-storm.md`. Sessão de investigação,
> com o controle plugado e jogo real (PRAGMATA via Proton). Acompanhamento ao vivo do kernel +
> pesquisa aprofundada (kernel/USB de baixo nível, prior-art) a pedido da Vitória ("vale a pena
> até tentarmos a nível de alterar o SO"). Confirma o mecanismo e define as duas alavancas.

## TL;DR

- O storm é a **enumeração das interfaces de ÁUDIO USB** do DualSense pelo kernel `snd-usb-audio`:
  uma **rajada de control-transfers no EP0** (probe: `usb_set_interface`, `get min/max values for
  control`) que, sob carga, **derruba o link** do controlador Matisse → `-71` (EPROTO) → re-enum.
  Confirma o A/B anterior (áudio off = 0 storm). **Não é cabo/porta/BIOS** (port-independente).
- **Observação ao vivo (PRAGMATA):** rajada de 5 re-enum + 1 `-71` **no launch** (11:43–11:50),
  depois **estável 9+ min**. É um burst de inicialização sob carga, não um storm contínuo. Bate com
  o relato da Vitória ("caiu poucas vezes").
- **Prior-art:** é um padrão **conhecido e NÃO resolvido** em AMD Ryzen (Bazzite #3956: Ryzen 3600
  + DualSense + mesmo `device descriptor read/64, error -71`). A sabedoria pública culpa
  hardware/cabo/porta — e as pessoas confirmam que trocar cabo/porta **não** resolve. **Ninguém
  conectou publicamente à interface de áudio.** O diagnóstico A/B da Vitória está à frente da comunidade.
- **Duas alavancas:** (A) quirk `DELAY_CTRL_MSG` que PRESERVA o áudio; (B) áudio-off confiável
  (`authorized=0`) que é PROVADO mas perde mic/fone do controle.

## Evidência de hardware (descritores reais, máquina da Vitória)

DualSense `054c:0ce6`, USB 2.0, **4 interfaces**, MaxPower **500mA**:

| Interface | Classe | Papel | Driver |
|-----------|--------|-------|--------|
| If0 | 01 Audio **Control** | controle de áudio | snd-usb-audio |
| If1 | 01 Audio **Streaming** (alt1: 392B isoc) | alto-falante | snd-usb-audio |
| If2 | 01 Audio **Streaming** (alt1: 196B isoc) | **microfone** | snd-usb-audio |
| If3 | 03 HID (2× int 64B) | gamepad | usbhid |

- Plataforma: Ryzen 7 5800X (Vermeer), B450M S2H, xHCI `0c:00.3` (Bus 3, 480M). O **dongle WiFi
  `rtw88_8822bu`** está no **mesmo** controlador (Bus 4) → re-bind do controlador mata a rede.
- Kernel `7.0.11-76070011-generic`. `usbcore.autosuspend=-1`, `pcie_aspm=off`. `usbcore.quirks` vazio.
- A interface HID (If3) enumera "leve" (passa). As 3 de áudio são o probe control-heavy (tomba).

## Mecanismo do `-71`

`-71` = **EPROTO** (falha de protocolo) durante leitura de descritor / control-transfer. A rajada de
control-transfers do probe de áudio satura o EP0 sobre um link já no limite no controlador Matisse;
sob carga (jogo) a margem cai e a transação tomba no meio → o device re-enumera (às vezes caindo pra
full-speed, daí o `device descriptor read/64, error -71`). Removida a enumeração de áudio (só-HID), a
margem sobra e não tomba.

## Alavanca A — quirk `DELAY_CTRL_MSG` (PRESERVA o áudio) ⭐

Tabela de flags do `usbcore.quirks` (de `drivers/usb/core/quirks.c`), confirmada:

| Letra | Flag | O que faz |
|-------|------|-----------|
| **g** | `USB_QUIRK_DELAY_INIT` | pausa na init, após ler o device descriptor |
| **n** | `USB_QUIRK_DELAY_CTRL_MSG` | **pausa após CADA control message** |
| k | `USB_QUIRK_NO_LPM` | desliga Link Power Management (já tentado; nulo em USB-2) |
| b | `USB_QUIRK_RESET_RESUME` | reseta em vez de resumir |

`n` (`DELAY_CTRL_MSG`) é o alvo: ele **espaça** exatamente a rajada que derruba o link — o áudio
ainda enumera, só mais devagar, **sem tombar**. Combinado com `g` (`DELAY_INIT`).

- **Sintaxe (cmdline, persistente):** `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`
- **Runtime (sem reboot, aplica no próximo replug):**
  `echo '054c:0ce6:gn,054c:0df2:gn' > /sys/module/usbcore/parameters/quirks` (root).
  **Já armado nesta sessão** — aguardando 1 replug do controle para testar com áudio ON.
- **Persistência:** o cmdline é domínio do **Ritual da Aurora** (dona dos kernel params). Para não
  ser apagado no próximo self-heal, precisa entrar na allowlist da Aurora — coordenar.
- **Risco:** pode não bastar (o burst só desacelerado ainda tombar). Aí → alavanca B.

## Alavanca B — áudio-off confiável `authorized=0` (PROVADO, perde áudio)

A regra 75 atual usa `ACTION=="bind" ... snd-usb-audio/unbind` — **racy** (às vezes não pega no
replug). O mecanismo mais confiável é **deautorizar a interface de áudio** (`authorized=0`): o kernel
não bind/probe driver numa interface deautorizada → a rajada não acontece. Escopo: só `bInterfaceClass==01`
do `054c:0ce6`/`0df2`; o HID (If3) fica intacto.

- **Trade-off:** controle sem mic E sem fone pelo jack. A Vitória já usa **webcam C920** (voz) +
  **HDMI** (saída) → redundante para ela.
- **Reversível:** opt-in `HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED=1` reabilita.
- **Empacotamento:** ver plano de integração (install_udev.sh/install.sh/doctor.sh/uninstall.sh/
  build_deb.sh/flatpak), abaixo.

## Alavanca C — Bluetooth (contorna o áudio USB)

Sobre BT o `snd-usb-audio` não entra (sem interfaces de áudio USB) → sem storm de áudio. Mas o dongle
BT está no **mesmo** controlador frágil + latência maior. Só último recurso.

## Recomendação (áudio-primeiro)

1. **Testar a alavanca A** (quirk, preserva áudio): 1 replug com o quirk armado → jogar sob carga →
   ver se o storm some. Se segurar: tornar permanente (cmdline via Aurora).
2. **Se A não segurar** → aplicar a alavanca B (áudio-off `authorized=0`), já empacotada no repo.
3. Validar com `scripts/storm_loadtest.sh` em ambos os casos.

## Plano de integração no repo (do mapa da investigação de código)

- **Regra udev:** elevar o mecanismo da **75** de `unbind` (racy) para `authorized=0` (confiável),
  mantendo opt-in; casar só classe 01 de `0ce6`/`0df2`; header documenta a troca.
- **`scripts/install_udev.sh`** (flag `--disable-usb-audio`), **`install.sh`** (wiring),
  **`uninstall.sh`** (simetria de remoção), **`scripts/doctor.sh`** (check da regra + do bind do
  snd-usb-audio), **`scripts/build_deb.sh`** + **`flatpak/*.yml`** (opt-in, não auto-ativa),
  **`tests/`** (cobertura).
- **Quirk:** documentar no guia (FEAT-DSX-DEFINITIVE-FIX) como opção que preserva áudio + coordenação
  com a Aurora.

## Fontes

- Linux kernel — `drivers/usb/core/quirks.c` e `admin-guide/kernel-parameters` (letras dos quirks):
  https://github.com/torvalds/linux/blob/master/drivers/usb/core/quirks.c ·
  https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html
- Prior-art DualSense `-71` em AMD Ryzen (não resolvido): https://github.com/ublue-os/bazzite/issues/3956
- Perfil do device: https://linux-hardware.org/?id=usb:054c-0ce6
