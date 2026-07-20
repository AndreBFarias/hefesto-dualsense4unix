# ESTUDO — Validação de premissas da Onda W (WiFi raiz / rtw88)

Data: 2026-07-20 (tarde). Validador: agente read-only. Nada foi modificado no sistema nem no repo.
Sprint alvo: `docs/process/sprints/2026-07-20-sprint-onda-w-wifi-raiz.md`.

## Sumário de vereditos

| # | Premissa | Veredito |
|---|----------|----------|
| 1 | Source exato do rtw88 do kernel em uso | **CONFIRMADA** — obtido; Pop não patcha o rtw88 (diff vs vanilla = 0) |
| 2 | Bug do fantasma: driver em retry loop segura referência e bloqueia o disconnect | **PARCIAL** — fantasma provado, mas o mecanismo alegado está ERRADO; ver §2 |
| 3 | Existe fix upstream? | **CONFIRMADA a busca; fix NÃO existe** — modelo pronto para portar = rtw89 (`RTW89_FLAG_UNPLUGGED`) |
| 4 | `disable_lps_deep=N` hoje; virar Y estabiliza | **PARCIAL** — knob confirmado em N, mas **é NO-OP em USB**; o alvo certo é o LPS raso (NM powersave) |
| 5 | Topologia: WiFi+BT no mesmo xHCI; 02:00.0 com portas livres | **CONFIRMADA** — e os 2 controles no cabo também caíram no xHCI lotado |
| 6 | morrownr/88x2bu como alternativa | **CONFIRMADA a pesquisa; veredito desfavorável** — auto-deprecado, mantenedor recomenda o in-kernel |
| 7 | Ferramental para medir BT sem instalar nada | **CONFIRMADA** — btmon/hciconfig/btmgmt/debugfs presentes; única lacuna: iperf3 ausente |

---

## §1 — Source exato do driver (CONFIRMADA)

**Rota** (a mais leve; deb-src existe mas não foi preciso baixar 200MB):

1. A versão do pacote embute o hash do repo Git do Pop:
   `linux-image-7.0.11-76070011-generic = 7.0.11-76070011.202606011647~1783638829~24.04~3af2f9d`
   → hash curto **`3af2f9d`** de `github.com/pop-os/linux`.
2. Resolvido via API GitHub: **`3af2f9de43174ce5063110f94b7b01226499ba13`**
   ("ALSA: hda/realtek: Add Clevo V560GN, L550JN", committer Jeremy Soller, 2026-07-09 — bate com o
   timestamp de build `~1783638829`).
3. Fetch esparso (`--depth 1 --filter=blob:none` + sparse-checkout de
   `drivers/net/wireless/realtek/rtw88/`) → **8,5MB**, em
   `onda-w-premissas/pop-linux/drivers/net/wireless/realtek/rtw88/`.
4. Vanilla de comparação: tag **v7.0.11** (`bb532bfaf "Linux 7.0.11"`) da árvore stable de
   git.kernel.org, mesmo diretório, em `onda-w-premissas/vanilla-stable/...`.

**Diff Pop × vanilla no rtw88: ZERO arquivos diferentes.** O kernel da System76 usa o rtw88 do
stable 7.0.11 intocado. Qualquer patch nosso parte do vanilla — sem surpresa de fork.

Nota deb-src: `Types: deb deb-src` já habilitado em `/etc/apt/sources.list.d/pop-os-release.sources`
e `system.sources` — `apt source` funcionaria como rota B sem tocar em nada.

---

## §2 — Bug do fantasma (PARCIAL: fantasma real, mecanismo alegado refutado)

### 2a. Anatomia dos helpers (código real, `pop-linux/.../rtw88/usb.c`)

- **`rtw_usb_read`** (usb.c:72-103): **UMA** tentativa de `usb_control_msg` (timeout 1000ms), sem
  retry. Erro é logado só se `ret < 0 && ret != -ENODEV && count++ < 4` (usb.c:93-95) — `count` é
  **`static`**: máximo **4 logs por vida do módulo**, depois silêncio eterno. Nenhum tratamento de
  -EPROTO/-ESHUTDOWN além do log.
- **`rtw_usb_write`** (usb.c:120-151): idem (timeout 500ms, cap de 4 logs próprio, usb.c:143-145).
- **`rtw_usb_reg_sec`** (usb.c:42-70): nos chips 8822B/8822C/8821C, **toda** leitura E escrita de
  registrador "on-section" dispara uma escrita EXTRA no reg 0x4e0 (usb.c:100 e 150) — mesmo quando a
  operação principal já falhou. Log **sem cap** (só -ENODEV é silenciado, usb.c:67-69). É por isso
  que o flood típico no 8822BU é o `rtw_usb_reg_sec ... -71`.
- **NÃO existe flag de device-gone**: `struct rtw_usb` (usb.h:64-89) não tem nada disso; nenhum
  `test_bit`/early-return em caminho algum.
- **NÃO existe retry loop nos helpers.** Os "loops" são das camadas de cima: sequência de power
  on/off com polling (`rtw_pwr_cmd_polling`, mac.c:~140-160, `read_poll_timeout` de 50µs ×
  `RTW_PWR_POLLING_CNT`=20000, main.h:922 → teto ~1s por comando de polling), saída de LPS com
  poll de 100ms (ps.c:~117-150), ack de firmware 15ms (ps.c `rtw_power_mode_change`). Tudo
  **limitado no tempo** — o teardown observado levou ~0,9s, não infinito.
- **Bug lateral (dado corrompido silencioso)**: em falha, `rtw_usb_read` retorna
  `le32_to_cpu(*data)` do ring buffer compartilhado (usb.c:88-102) = **valor velho de outra
  leitura**. Polling de power-off contra hardware morto pode "passar" com lixo.
- **RX completion** (usb.c:737-777): com status -EPROTO/-ENODEV/-ESHUTDOWN/-EILSEQ o URB **não** é
  ressubmetido (case-break em usb.c:759-771) — não há tempestade vinda do RX; ele só estaciona.
- **Referência do udev**: o probe usa `interface_to_usbdev(intf)` e guarda o ponteiro
  (usb.c:1044-1047) — **não há `usb_get_dev`** neste kernel (o fix do CVE-2026-31604, leak de
  referência em erro de probe, já está contido no 7.0.11). O driver **não retém referência extra**
  do usb_device.
- **`rtw_usb_disconnect`** (usb.c:1349-1376): `rtw_unregister_hw` (→ power-off com I/O de
  registrador) → deinit tx/rx → **`usb_reset_device(rtwusb->udev)` se o estado ≠ NOTATTACHED
  (usb.c:1367-1368)** → frees. Este `usb_reset_device` é o personagem-chave do desfecho abaixo.

### 2b. O incidente, reconstituído do journal (boot -1, 19/07 14:35 → 20/07 12:38)

| Instante | Evento |
|---|---|
| 19/07 16:15:35 | Dongle enumera em **4-3** (SuperSpeed, device 3), vira `wlx000000000000` (phy3/rfkill5) |
| 19/07 23:16:31 | Firmware do dongle **já wedged**: `error beacon valid` + `failed to download rsvd page` + `failed to download firmware` ×2 em 4-3 |
| 19/07 23:18:59 | Mantenedora move o dongle de porta: enumera **3-2** (USB2 HS) → driver faz o switch USB2→USB3 (`switch_usb_mode`) → disconnect 3-2 → enumera **4-2** SuperSpeed (23:19:02), vira `wlan0` (phy5), conecta no AP |
| 19/07 23:19:18 | Último suspiro do fantasma: `4-3:1.0: write register 0x1d00 failed with -71` — **e silêncio por 13 horas** |
| — | **`usb 4-3: USB disconnect` NUNCA aparece.** O fantasma segue em lsusb/sysfs, **dono do nome** `wlx000000000000` |
| 20/07 12:01:26 | Novo replug do dongle; udev falha o rename: `wlan0 → wlx000000000000: Arquivo existe` — dano concreto do fantasma (colisão de nome persistente) |
| 20/07 12:01:06 | **Prova de que o hub estava vivo**: `usb 4-2: USB disconnect, device number 4` processado normalmente **no mesmo bus 4** enquanto o fantasma 4-3 persistia |
| 20/07 12:09:51.122 | `echo 4-3:1.0 > .../rtw88_8822bu/unbind` |
| 12:09:51.167-.256 | A rajada -71 nasce AQUI, **durante o teardown do unbind**: `read register 0x4c failed with -71` ×3 + `rtw_usb_reg_sec reg 0x4e0 ... -71` ×6 (power-off contra hardware ausente; cada acesso duplicado pelo reg_sec) |
| 12:09:52.002 | `usb 4-3: USB disconnect, device number 3` — o core FINALMENTE processa, no instante em que `rtw_usb_disconnect` executa `usb_reset_device` (usb.c:1367-1368), que força a revalidação da porta |
| 12:09:52.002 | WARNING mac80211: **"Have pending ack frames!"** em `ieee80211_free_ack_frame` (net/mac80211/main.c:1722), pilha `ieee80211_free_hw ← rtw_usb_disconnect` — skbs de ack vazados no teardown sujo |

Detalhe probatório fino: os 3 logs `read register ... -71` de 12:09:51 estavam dentro do cap de 4
por vida de módulo — ou seja, **o fantasma quase não fez I/O nas 13 horas** (a interface estava
down; watchdog/LPS param quando o mac80211 desativa o vif). Não havia loop rodando.

### 2c. Veredito do mecanismo

- ~~"driver ficava em loop ... segurando a referência do usb_device ... o USB core não recicla um
  device cujo driver o retém"~~ → **REFUTADO nos três pontos**: (i) não há retry loop nos helpers
  nem I/O contínuo do fantasma (13h de silêncio); (ii) não há referência extra
  (`interface_to_usbdev` sem get; e refcount não bloquearia `usb_disconnect` de qualquer forma —
  só adia o kfree); (iii) o hub/core estava saudável — processou o disconnect do 4-2 no mesmo
  bus com o fantasma presente.
- **Causa real do fantasma**: o evento de mudança de status da porta 4-3 (unplug físico ~23:18)
  **nunca chegou/foi processado** pelo USB core — perda de port-status-change no nível
  xHCI/porta (plausível num unplug de porta SuperSpeed com device já wedged e num barramento com
  histórico de EMI; a causa exata é nível xHCI e não é determinável só pelo journal).
- **Por que o unbind "curou"**: não foi o unbind em si — foi o `usb_reset_device` dentro de
  `rtw_usb_disconnect` (usb.c:1367-1368), que obriga o core a revalidar a porta; porta vazia →
  disconnect processado 0,9s depois.
- **Pecados reais do driver** (o que um patch W1 conserta de verdade):
  1. Não detecta device-gone → teardown faz dezenas de control msgs contra hardware morto
     (cada uma duplicada pelo reg_sec), retorna **lixo silencioso** ao polling e vaza ack frames
     (o WARNING do mac80211).
  2. Não tem autorrecuperação: um device que só responde -EPROTO indefinidamente nunca provoca a
     revalidação da porta — o fantasma vive até unbind/reboot manual.

### 2d. Desenho recomendado do patch W1 (funções/linhas alvo)

Portar o padrão do **rtw89** (mainline, `drivers/net/wireless/realtek/rtw89/usb.c`, commit
`2135c28be6a8`), confinado a `usb.c`/`usb.h` (= só o módulo `rtw88_usb`; Makefile:112-113
`rtw88_usb-objs := usb.o` → DKMS enxuto):

1. **`usb.h` (struct rtw_usb, linha ~64)**: adicionar `struct usb_interface *intf;`,
   `atomic_t continual_io_error;` e `bool device_gone;` (ou bit em flags próprio do rtwusb —
   manter local ao módulo para não tocar main.h).
2. **`rtw_usb_read` (usb.c:72) / `rtw_usb_write` (usb.c:120) / `rtw_usb_reg_sec` (usb.c:42) /
   `rtw_usb_write_firmware_page` (usb.c:168)**: early-return se `device_gone`; em
   `-ENODEV`/`-ESHUTDOWN` → seta `device_gone`; em outros erros (`-EPROTO`, `-EILSEQ`,
   `-ETIMEDOUT`) → `atomic_inc_return(&continual_io_error) > 4` → seta `device_gone`; sucesso →
   zera o contador. (Cópia fiel da lógica `continual_io_error` do rtw89.)
3. **`rtw_usb_read_port_complete` (usb.c:759-771)**: nos cases -EPROTO/-EILSEQ/-ENODEV/-ESHUTDOWN,
   setar `device_gone` (rtw89 faz isso para EPROTO no RX).
4. **A adição além do rtw89 — a cura do fantasma**: na primeira armada de `device_gone`, chamar
   **`usb_queue_reset_device(rtwusb->intf)`**. O reset enfileirado (seguro em contexto atômico)
   força o core a revalidar a porta: device presente-mas-wedged → reset o recupera; device
   ausente → o core descobre e processa o disconnect sozinho — **exatamente o efeito que o
   unbind manual produziu via usb.c:1367-1368**, agora automático. Sem essa peça, o patch só
   silencia o teardown mas o fantasma continuaria até alguém mexer.
5. Em `rtw_usb_read`, quando `device_gone`/falha: retornar valor determinístico (rtw89 usa
   estilo "-ENODEV imediato") em vez do lixo do ring buffer — mata o bug lateral do §2a.
6. Bônus de mesmo veículo: incluir o backport de **`6b964941bbfe`** ("rtw88: usb: fix memory
   leaks on USB write failures", CVE-2026-63821, `Cc: stable`) — foi backportado para 6.6.144+,
   6.12.95+, 6.18.38+ e 7.1.3+, e a série **7.0.y ficou de fora** (EOL); é exatamente o cenário
   disconnect/replug desta máquina.
7. **Upstream**: bug órfão confirmado (§3) — formatar com `git format-patch` + Signed-off-by
   contra wireless-next citando: journal deste incidente (fantasma 13h + WARN mac80211),
   precedente rtw89 (mesmo mantenedor, Ping-Ke Shih) e análogos mt76 (`MT76_REMOVED`) e rt2x00
   (`DEVICE_STATE_PRESENT`).
8. **Teste de aceite W1** (o do sprint, agora com fundamento): arrancar o dongle da porta →
   `usb X-Y: USB disconnect` deve sair em segundos **sem unbind**; `lsusb`×`/sys/bus/usb/devices`
   sem divergência; sem WARN "pending ack frames"; replug reusa o nome `wlx...` sem "Arquivo existe".

---

## §3 — Upstream (CONFIRMADA a busca; fix não existe — portar do rtw89)

Pesquisa completa (mainline via espelho GitHub do torvalds, wireless-next via backport declarado
lwfinger/rtw88, lore/patchwork, issues de campo):

- **Nenhum fix upstream** trata device-gone/-EPROTO nos helpers do `rtw88/usb.c` — nem mainline
  (auditado até ~jun/2026), nem wireless-next, nem série pendente. Só `-ENODEV` é silenciado, desde
  o commit fundador `a82dfd33d123` ("wifi: rtw88: Add common USB chip support", dez/2022).
- Commits relevantes que NÃO são o fix: `1f1784a59caf` (flood da rx_queue, 2023);
  **`41a7acb7dde8`** ("8821cu: Fix firmware upload fail", v6.9 — é quem **introduziu** o
  `rtw_usb_reg_sec` e seu flood sem cap); `28818b4d871b` (beacon loss, não unplug);
  `bbb15e71156c` (CVE-2026-31604, leak no probe — **já contido no 7.0.11**);
  `6b964941bbfe` (CVE-2026-63821, memleak no write fail — **provavelmente ausente no 7.0.11**,
  backport foi para 6.6.144+/6.12.95+/6.18.38+/7.1.3+, sem 7.0.y).
- Sintoma reproduzido em campo sem cura: lwfinger/rtw88 issues #377 (mesmo `write register 0xc4
  failed with -71` + `reg_sec 0x4e0 -71` num TP-Link 8822BU), #402, #430, #343.
- **Modelo para portar (mainline!)**: rtw89 USB, commit `2135c28be6a8` (Bitterblue Smith,
  2025-06-30; série incluía "Hide some errors when the device is unplugged"):
  `RTW89_FLAG_UNPLUGGED` + `continual_io_error > 4` (pega EPROTO!) + early-return no vendorreq +
  EPROTO no RX arma a flag. Mesmo subsistema, mesmo mantenedor — precedente ideal.
- Análogos: mt76 (`MT76_REMOVED` em -ENODEV/-EPROTO), rt2x00 (`DEVICE_STATE_PRESENT`).
  rtl8xxxu não tem nada (não serve).
- Tentativa "usb: Prevent TX URB use after free" no lwfinger (jan/2025) foi **revertida** um mês
  depois — teardown de URB no rtw88 é terreno sensível; patch deve ser cirúrgico.

## §4 — Knobs e LPS deep (PARCIAL: knob real, efeito irreal em USB)

Estado vivo confirmado (`/sys/module/rtw88_core/parameters/`): `disable_lps_deep=N`,
`support_bf=Y`, `debug_mask=0`. `rtw88_usb` expõe `switch_usb_mode=Y` (o mecanismo que vimos agir
no journal às 23:18-23:19: enumera USB2 → chaveia → re-enumera SuperSpeed). `rtw88_8822bu` sem
parm próprio. Cmdline: `usbcore.autosuspend=-1` (global) confirmado.

**O que `disable_lps_deep` faz de verdade**: `main.c:38` → `rtw_update_lps_deep_mode`
(main.c:1354-1371) devolve `LPS_DEEP_MODE_NONE` → `__rtw_enter_lps_deep` retorna cedo (ps.c:214).
**Mas em USB isso já é letra morta**: quem seta `RTW_FLAG_LEISURE_PS_DEEP` são só **pci.c:638,
sdio.c:795 e wow.c:642**; o op de HCI do USB é **função vazia** (`rtw_usb_deep_ps`,
usb.c:836-839, "empty function for rtw_hci_ops"). O 8822B até declara suporte LCLK
(rtw8822b.c:2545), mas o deep PS **nunca engaja via USB**. → `disable_lps_deep=Y` neste dongle =
**no-op** (inofensivo, porém sem efeito medível esperado). O asset modprobe.d do sprint, como
está desenhado, não se sustenta sem medição que o contradiga.

**O que ESTÁ ativo e tem histórico de instabilidade**: o **LPS raso** (firmware power save) engaja
em USB sim — `rtw_watch_dog` → `rtw_enter_lps` (main.c:302-304) quando `ps_enabled` (que vem do
`vif->cfg.ps` do mac80211). E a máquina tem
`/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf: wifi.powersave = 3` (**ligado**;
perfil Beholder herda o default). Evidência upstream de que PS em rtw88-USB é problemático: a
série original tinha o patch "disable powersave modes for USB devices" (thread jun/2022,
openwall — pings de 15405ms, "Connection to AP lost" em loop) que **não sobreviveu** ao merge; e
lwfinger#402 (2025, 8822BU 5GHz): "firmware failed to leave lps state", cura = desligar power
saving. O wedge de 23:16 (`error beacon valid`/`failed to download rsvd page`) é da família
rsvd-page/PS.

**Plano de medição W2 (executável, sem patch)** — A/B com `nmcli connection modify Beholder
802-11-wireless.powersave 2` (disable) vs `3` (enable) + re-ativar a conexão; em cada braço
≥120s de: `ping -i 0.2` no gateway (mediana/p95/perda), download grande via curl/wget
(throughput médio e estabilidade), e observar journal por `failed to leave lps state`/beacon
errors. `iw` está AUSENTE; iperf3 AUSENTE (se quiser iperf3, vira dependência declarada no
install — regra da casa). `support_bf`: só mexer se a medição A/B de powersave não bastar.

## §5 — Topologia USB agora (CONFIRMADA; sem fantasma no momento)

Boot atual desde 13:58 (a máquina reiniciou após o incidente; dongle re-enumerou limpo).

**xHCI `0000:0c:00.3`** (Matisse — o barramento lotado):
- Bus 3 (USB2): **3-1** = TP-Link BT `2357:0604` (btusb, 12M) · **3-2** = Pro Controller
  `057e:2009` (12M) · **3-4** = 8BitDo em modo Switch `057e:2009` (12M)
- Bus 4 (USB3): **4-3** = Archer T3U `2357:012d` (rtw88_8822bu, **5000M SuperSpeed**)

**xHCI `0000:02:00.0`** (400 Series Chipset):
- Bus 1 (USB2, 10 portas): **1-3** = receiver 2.4G `3554:fa09` · **1-4** = receiver 2.4G
  `25a7:fa07` — 8 portas livres
- Bus 2 (USB3, **4 portas SuperSpeed 10G, TODAS LIVRES**)

Leituras: (i) a premissa do sprint confirma — WiFi + BT + (agora também) os 2 controles no cabo
dividem o MESMO xHCI 0c:00.3; os controles novos de hoje caíram no barramento errado do ponto de
vista da W3; (ii) o 02:00.0 tem porta SuperSpeed livre de sobra para receber o dongle (W3.2) —
mudança de topologia interna, não gambiarra; (iii) **sem fantasma agora**: lsusb × /sys/bus/usb/
devices 1:1, todos com driver (`/sys/class/ieee80211/` = só phy1). DualSense ×2 estão via BT
(nenhum no USB neste momento). Registro do dia: bluetooth.service caiu com core-dump às 11:57
(crônico já conhecido, fora do escopo W).

## §6 — morrownr/88x2bu (CONFIRMADA a pesquisa; desaconselhado)

- Repo vivo porém **auto-deprecado**: README recomenda o in-kernel rtw88 (≥6.12 "of good
  quality", "a much better driver than this one"); sem updates oficiais de API além do 6.14
  (só PRs comunitários reativos).
- Kernel máximo **confirmado por teste**: 7.1.3 XanMod (PR #277, mergeado **19/07/2026**, gates
  `>= KERNEL_VERSION(7,0,0)` — 7.0.11 provavelmente compila, mas **nunca testado em 7.0.x**);
  histórico = quebra a cada série de kernel com semanas/meses de espera (issues #246, #256,
  #262/#266/#267).
- Coexistência: o instalador copia `88x2bu.conf` para `/etc/modprobe.d/` com
  `blacklist rtw88_8822bu` (não blacklista rtw88_usb/core) + DKMS oficial + assinatura MOK p/
  Secure Boot.
- Tabela do próprio morrownr (USB-WiFi): RTL8812BU = "Recommended for Linux: **Yes**" justamente
  pelo suporte in-kernel. Único ponto a favor do out-of-tree: relatos de instabilidade
  5GHz/LPS no rtw88 (lwfinger#402) — que o W2 ataca por config, e o W1 por patch.
- **Recomendação**: W4 só se W1+W2 medidos falharem; e mesmo então, A/B formal antes de adotar.

## §7 — Ferramental de medição BT (CONFIRMADA; nada a instalar)

Presentes: `btmon`, `hciconfig`, `hcitool`, `btmgmt`, `bluetoothctl`; debugfs BT rico
(`/sys/kernel/debug/bluetooth/hci0/` com conn_info_*, supervision_timeout, hardware_error,
device_list etc. — root). Ausente: `iperf3` (afeta só o braço de carga do W2/W3; substituível
por download grande).

**Plano W3 executável** (3 braços: WiFi ocioso / WiFi em carga / `rfkill block wifi`):
1. Delta de contadores do controlador: `hciconfig -a hci0` antes/depois de cada braço
   (`RX bytes/acl/events/errors`, `TX ... errors`) — baseline atual: RX errors:0, TX errors:0
   com 978778 ACL RX acumulados.
2. Captura `sudo btmon -w /tmp/braçoX.snoop` durante cada braço; pós-processar contando
   HCI Hardware Error, Disconnection Complete (reason), retransmissões/pacing de Number of
   Completed Packets.
3. Lado dos controles: taxa de reports e lacunas via evdev (o daemon do hefesto já mede perda de
   reports — reaproveitar a métrica dos estudos de 19/07).
4. debugfs por conexão: `conn_info_min/max_age` e, por dispositivo, RSSI via
   `hcitool rssi`/`btmgmt` (read-only).
Braço de carga WiFi sem iperf3: download contínuo (curl -o /dev/null) do mirror mais rápido.

---

## Arquivos deste estudo
- `onda-w-premissas/pop-linux/drivers/net/wireless/realtek/rtw88/` — source EXATO do kernel em uso
  (commit 3af2f9de43174ce5063110f94b7b01226499ba13)
- `onda-w-premissas/vanilla-stable/drivers/net/wireless/realtek/rtw88/` — vanilla v7.0.11 (diff = 0)
- Journal citado: boot -1 (19/07 14:35 → 20/07 12:38) e boot 0 (20/07 13:58+), timestamps precisos
  no §2b.
