# Sprint Onda W — WiFi na raiz (rtw88): pedido de 19/07 que caiu no vão

> **Dívida reconhecida**: a mantenedora pediu em 19/07 para "liberar o full potencial de BT, 2.4G,
> dongle WiFi e USB". O mapa catalogou a parte WiFi como pendência da Onda R, mas a Onda R
> executada entregou **só a metade do BlueZ**. Nenhuma linha de código nossa toca WiFi
> (`grep -riE "rtw88|wifi|wlan|8822bu"` em assets/install/scripts/src = vazio). Este sprint paga
> essa dívida.
>
> **Diretriz da mantenedora (20/07)**: "volte o cabo" é GAMBIARRA e está REJEITADO. A meta é ter
> **WiFi bom E BT estável ao mesmo tempo**, consertando na raiz — programação de baixo nível e
> kernel liberados.

## Fatos medidos (não re-pesquisar)
- Hardware: TP-Link Archer T3U (2357:012d), chipset **Realtek RTL8812BU/8822BU**, driver in-kernel
  `rtw88_8822bu` + `rtw88_core` (kernel 7.0.11-76070011-generic).
- **Está na máquina desde ≥02/07** (341 registros no journal de todos os boots) — NÃO é hardware
  novo (correção de um erro anterior: `journalctl -k` implica `-b`).
- Link atual: 5805 MHz (5 GHz, ch 161), 270 Mbit/s, sinal 94. AP também expõe 2.4G (ch 11).
- Topologia: dongle em SuperSpeed (5000M) no **mesmo xHCI `0000:0c:00.3`** que o adaptador BT
  (bus 3) e o DualSense no cabo. USB3 SuperSpeed é fonte documentada de ruído em 2.4 GHz.
- Knobs existentes (`modinfo rtw88_core`): `disable_lps_deep` (**N** hoje), `support_bf` (Y),
  `debug_mask`. O `rtw88_8822bu` não expõe parm próprio.
- Erros observados: `-71` (EPROTO) em rajadas do `rtw88_8822bu`, e o **bug do fantasma** (abaixo).
- Nosso cmdline tem `usbcore.autosuspend=-1` (global, afeta o dongle).

## W1 — BUG DO FANTASMA USB: o driver segura um device que sumiu (PROVADO)
**Mecanismo (medido 20/07 12:09:51)**: ao mover o dongle de porta, o kernel NUNCA processava
`usb 4-3: USB disconnect`. O log do unbind mostrou o porquê: o driver ficava em loop
(`read register 0x4c failed with -71`, `rtw_usb_reg_sec ... -71` ×6) contra um hardware ausente,
**segurando a referência do `usb_device`** — o USB core não recicla um device cujo driver o
retém. No instante do `unbind`, o disconnect saiu.

**Fix na raiz**: patch em `drivers/net/wireless/realtek/rtw88/usb.c` — tratar
`-EPROTO`/`-ESHUTDOWN`/`-ENODEV` nos helpers de registro (`rtw_usb_read/write_*`,
`rtw_usb_reg_sec`) como **device-gone**: setar um flag de "removido", abortar o retry loop e
liberar o caminho de `disconnect()` em vez de insistir. Hoje o driver trata todo erro como
transitório.
- Entrega: **DKMS** (mesmo veículo do patch do `hid-nintendo` da Onda T), integrado ao install
  (idempotente) e ao uninstall (simétrico), com fallback para o módulo in-tree.
- Teste: reproduzir removendo o dongle de uma porta e conferindo `usb X-Y: USB disconnect` no
  mesmo segundo, sem fantasma no `lsusb`/`/sys/bus/usb/devices`.
- **Upstream**: formatar com `git format-patch` + `Signed-off-by` e avaliar envio para
  `linux-wireless` — é bug genuíno e reproduzível.
- Mitigação enquanto o patch não entra: `unbind` do fantasma (comando acima) ou reboot; e um check
  no doctor ("device USB fantasma: driver retém device removido").

## W2 — Estabilidade/latência: `disable_lps_deep=Y`
O **Deep Power Save** do rtw88 é causa documentada de picos de latência, throughput irregular e
quedas em dongles Realtek USB. Hoje está **ligado** (`disable_lps_deep=N`).
- Asset `modprobe.d` próprio (espelhando `hefesto-btusb-no-autosuspend.conf`):
  `options rtw88_core disable_lps_deep=Y`, aplicado pelo install e removido pelo uninstall.
- **Medir A/B** antes de fixar: ping/jitter contra o gateway e throughput (iperf3 se houver par;
  senão download grande), com e sem o knob. Sem medição, não entra (regra da casa).
- Avaliar também `support_bf` (beamformee) — só mexer se a medição indicar.

## W3 — Coexistência WiFi×BT sem sacrificar nenhum dos dois
Meta: os dois funcionando juntos, não escolher um.
1. **Medir a interferência de verdade**: contadores HCI do BT (erros/CRC) e reports perdidos dos
   controles, com o WiFi (a) ocioso, (b) em tráfego pesado, (c) desligado por software
   (`rfkill block wifi`) — isola a contribuição do USB3 SuperSpeed vs. do rádio 2.4G.
2. **Separar os controladores**: hoje WiFi e BT dividem o xHCI `0000:0c:00.3`. A máquina tem outro
   controlador (`0000:02:00.0`, onde vivem os receivers 2.4G). Mover o dongle WiFi para lá é
   mudança de topologia (não gambiarra) e deve eliminar a disputa de barramento — **medir** o
   efeito nos contadores acima.
3. **Se a EMI persistir**: avaliar (com medição) forçar o dongle a USB2 — só se o throughput
   resultante ainda atender; caso contrário, manter USB3 e resolver por blindagem/extensor.
4. **NÃO** aceitar "usar cabo de rede" como solução (rejeitado pela mantenedora).

## W4 — Driver alternativo (avaliar com dados, não por fé)
Para RTL8812BU/8822BU existe o driver out-of-tree `morrownr/88x2bu` (rtl8812bu), historicamente
com throughput e estabilidade melhores que o rtw88 in-kernel para esse chipset.
- Comparar A/B com o rtw88 patchado (W1+W2): throughput, jitter, quedas, comportamento no
  disconnect, e **impacto no BT**.
- Só adotar se ganhar de forma medível; entrega por DKMS (mesmo padrão), com uninstall simétrico.
- Registrar o resultado como estudo (mesmo se o veredito for "fica o in-kernel").

## Aceite
- Fantasma USB não reproduz mais (W1) — teste de remoção de porta limpo.
- Ganho medido em latência/estabilidade do WiFi (W2), com números antes/depois no estudo.
- BT e controles sem degradação com WiFi em tráfego pesado (W3) — contadores provam.
- Decisão de driver (W4) fundamentada em medição, não em preferência.
- Tudo replicável por script (install/uninstall simétricos), nada de ajuste manual perdido.
