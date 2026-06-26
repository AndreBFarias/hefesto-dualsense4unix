# 2026-06-23 — Storm `-71` do DualSense: causa-raiz é porta USB, não o áudio

## TL;DR
O storm `-71` (EPROTO / `device not accepting address` / `device descriptor read/64, error -71`)
do DualSense via USB **não** é causado pelo áudio USB do controle. A causa-raiz observada é
**porta USB física ruim**: na porta `3-1` o controle negociava `full-speed` (12 Mbps) e despejava
`-71` em loop; na porta `3-4` enumerou `high-speed` (480 Mbps) e ficou **estável por tempo
indefinido, com o áudio ligado**. O conjunto reativo do hefesto (watcher `dsx-recover`, regras de
GUI-hotplug `73/74`, e a `99-usb-power-change` do Ritual da Aurora) **amplificava** o storm em vez
de resolvê-lo, e o "fix" de matar o áudio (regra `75`) era paliativo.

## Sintomas
- `dmesg`: dezenas de `usb 3-1: USB disconnect` + `device descriptor read/64, error -71` +
  `device not accepting address NN, error -71`, em cascata.
- Controle conecta/desconecta em loop; às vezes derruba periféricos no mesmo barramento.
- O áudio USB do controle some/volta junto.

## Investigação
1. Removida a regra `75` (disable-usb-audio) → áudio voltou; em seguida o storm reapareceu **durante
   manipulações** (unbind/bind forçado, trocas de profile, restarts do WirePlumber). Isso induziu
   o `dsx-recover` a reagir com `authorized`-toggle (= re-enumeração), realimentando o storm.
2. Leitura do `dmesg` por timestamp: **todo** o storm ocorreu na porta `3-1` (full-speed). Ao
   reconectar na `3-4` (high-speed), enumeração limpa e **0 eventos por 60s+**, com áudio presente.
3. Mapa de conflitos entre camadas (udev hefesto `70-75`, udev Ritual `99-usb-*`, ALSA, PipeWire,
   `dsx-recover`): quatro mecanismos faziam anti-autosuspend ao mesmo tempo; o `dsx-recover`
   "curava" re-enumerando (o próprio gatilho); a `73` subia a GUI a cada `add` (abre o controle via
   hidraw durante a enumeração).

## Causa-raiz
- **Primária:** porta USB `3-1` com sinal/contato ruim → negociação `full-speed` + `-71`.
- **Amplificadores de software:** `dsx-recover` (authorized-toggle), `73/74` (GUI-hotplug),
  `99-usb-power-change` (reescreve power a cada uevent `change`).
- O que de fato segura o power nativamente (mantido): cmdline `usbcore.autosuspend=-1`,
  `usbcore.quirks=054c:0ce6:k` (NO_LPM), `processor.max_cstate=1`, `pcie_aspm=off`, e a regra `72`
  (autosuspend off, só no `add`).

## Mudanças aplicadas (2026-06-23)
- **Desarmado** `hefesto-dsx-recover.service` (stop + disable). No `dsx.sh` virou **opt-in**:
  só instala/ativa sob `HEFESTO_PURE_HID=1`; no padrão, desarma.
- **Removidas** as regras `73`/`74` (GUI auto-spawn) de `/etc` e dos instaladores
  (`install_udev.sh`, `install-host-udev.sh`).
- **Removida** a `75` (disable-usb-audio) e a conf WirePlumber `52` (disable-source); mantida a
  `51` (DualSense não-default). O áudio do controle fica ligado.
- No Ritual da Aurora (repo zsh): **desregistrada** a `99-usb-power-change` (linha comentada no
  self-heal; removida de `/etc`).

## Recomendação ao usuário
- **Use uma porta USB que enumere `high-speed`** (cheque `cat /sys/bus/usb/devices/<porta>/speed`
  = 480). Evite a porta que negocia `full-speed` para este controle.
- Se precisar da escalada antiga (porta comprovadamente ruim e sem alternativa): `HEFESTO_PURE_HID=1
  ./dsx.sh` reativa o watcher e o modo pure-HID.

## Microfone embutido — RESOLVIDO via profile `pro-audio`
O array embutido **capta** — a chave é o profile **`pro-audio`** do card, que expõe os terminais
crus e **ignora o jack-sensing**:

```bash
CARD=$(pactl list cards short | grep -i dualsense | awk '{print $2}')
pactl set-card-profile "$CARD" pro-audio
# → surge a fonte: alsa_input.usb-...DualSense...pro-input-0
pactl set-default-source alsa_input.usb-...DualSense...pro-input-0   # mic padrão
amixer -c Controller sset 'Headset' 45% cap                          # ganho (95% satura)
```

Nos profiles normais o array é mapeado como `analog-input-headset-mic`, que o jack-sensing marca
**indisponível sem um fone no jack** — por isso davam silêncio. O `iec958-stereo` é S/PDIF (também
silêncio). Validado: voz perto da base do controle → RMS 4000-16000 (nítido).

**Persistência:** o WirePlumber salva sozinho (`~/.local/state/wireplumber/default-profile` =
`...=pro-audio` e `default-nodes` = `...pro-input-0`), então volta no boot/reconexão. A conf
WirePlumber `51` (rebaixa + `dont-reconnect`) passa a ser contraproducente quando se quer o
DualSense como mic padrão — considerar remover.
