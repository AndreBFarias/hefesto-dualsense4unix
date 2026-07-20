# DESENHO — Onda W: patch rtw88_usb (fantasma USB) via DKMS + medições W2/W3 + veredito W4

Data: 2026-07-20 (noite). Fase: DESENHO (nenhum asset criado no repo; nenhum módulo
instalado/carregado). Sprint: `docs/process/sprints/2026-07-20-sprint-onda-w-wifi-raiz.md`.
Premissas validadas (LER antes): `docs/process/estudos/2026-07-20-estudo-premissas-onda-w-rtw88.md`
— o mecanismo original do sprint (retry loop + referência retida) está REFUTADO; este desenho
ataca os pecados REAIS do driver (§2c do estudo) com o modelo do rtw89.

**Prova de build**: o pacote DKMS completo foi montado e compilado LIMPO contra os headers do
kernel em uso, no scratchpad da sessão (ver §8). `rtw88_usb.ko` gerado com
vermagic `7.0.11-76070011-generic SMP preempt mod_unload modversions`, zero warnings do nosso
código, CRCs de export idênticos ao in-tree. **Nada foi instalado nem carregado.**

---

## 1. W1 — o patch (confinado a `usb.c`/`usb.h` = só o módulo `rtw88_usb`)

Modelo portado: **rtw89 v7.0.11** (`drivers/net/wireless/realtek/rtw89/usb.c`, padrão do commit
`2135c28be6a8`: `RTW89_FLAG_UNPLUGGED` + `continual_io_error > 4`), verificado contra o source
REAL do v7.0.11 (baixado no sparse-checkout do estudo, não de memória). Dois patches em série:

- **0001** — backport verbatim do upstream `6b964941bbfe` ("wifi: rtw88: usb: fix memory leaks
  on USB write failures", CVE-2026-63821, `Cc: stable`; a série 7.0.y ficou de fora do backport
  por ser EOL). É PRÉ-REQUISITO do 0002: o early-return `-ENODEV` no TX depende de os chamadores
  liberarem skb/txcb quando o submit falha — sem o 0001, o 0002 criaria vazamentos novos.
- **0002** — o nosso: device-gone + port reset (detalhe abaixo).

### 1.1 Diffs concretos (função:linha do **vanilla v7.0.11** de `rtw88/usb.c`/`usb.h`)

| Alvo (vanilla) | Mudança |
|---|---|
| `usb.h:64-88` `struct rtw_usb` | + `struct usb_interface *intf;` + `DECLARE_BITMAP(flags, NUM_OF_RTW_USB_FLAGS)` + `atomic_t continual_io_error;` — e novo `enum rtw_usb_flags { RTW_USB_FLAG_DEVICE_GONE }` acima da struct. **Local ao módulo** (não toca `main.h`/`struct rtw_dev` — obrigatório no DKMS: o `rtw88_core` in-tree continua com o layout dele; p/ upstream, rebase trivial movendo p/ `rtwdev->flags` como o rtw89) |
| `usb.c:21` (após param `switch_usb_mode`) | + module param **`hang_reset`** (bool, 0644, default **Y**) — gate da parte agressiva (só o `usb_queue_reset_device`); + `#define RTW_USB_MAX_CONTINUAL_IO_ERR 4` (mesmo limiar do rtw89) |
| `usb.c:41` (antes de `rtw_usb_reg_sec`) | + 3 helpers novos: `rtw_usb_device_gone()` (test_and_set_bit; na 1ª armada loga 1x e, se `hang_reset`, **`usb_queue_reset_device(rtwusb->intf)`**), `rtw_usb_io_error(rtwusb, err)` (`-ENODEV`/`-ESHUTDOWN` → arma imediato; senão `atomic_inc_return(&continual_io_error) > 4` → arma), `rtw_usb_io_ok()` (`atomic_set(..., 0)`) |
| `rtw_usb_reg_sec` (usb.c:42-70) | early-return se device_gone (mata a DUPLICAÇÃO do flood: cada acesso on-section dispara escrita extra no reg 0x4e0); sucesso → `io_ok`; falha → `io_error` + o rtw_err existente (string preservada) |
| `rtw_usb_read` (usb.c:72-103) | early-return `0` se device_gone; em `ret < 0`: **`*data = 0`** (valor determinístico — NUNCA devolver lixo do ring buffer ao polling de power-off; mata o bug lateral §2a do estudo) + `io_error`; senão `io_ok`. Log com cap de 4 e string `"read register 0x%x failed with %d"` preservados byte a byte (kernel-watch/doctor atuais continuam casando) |
| `rtw_usb_write` (usb.c:120-151) | early-return se device_gone; `ret < 0` → `io_error`; senão `io_ok`; log preservado |
| `rtw_usb_write_firmware_page` (usb.c:168-220) | early-return se device_gone; no loop, `ret != n` → `io_error` antes do break; bloco ok → `io_ok` |
| `rtw_usb_write_port` (usb.c:365-390) | early-return `-ENODEV` se device_gone (o 0001 garante que o chamador libera skb/txcb); `usb_submit_urb == -ENODEV` → `device_gone` (paridade rtw89) |
| `rtw_usb_tx_agg_skb` (usb.c:392-462) + `rtw_usb_write_data` (usb.c:495-525) | **0001**: checar retorno de `rtw_usb_write_port`; falha → purge da `tx_ack_queue` + `kfree(txcb)` / `dev_kfree_skb_any(skb)` (verbatim upstream) |
| `rtw_usb_rx_resubmit` (usb.c:679-721) | `error == -ENODEV` → `device_gone` (senão o rtw_err existente; paridade rtw89) |
| `rtw_usb_read_port_complete` (usb.c:737-777) | switch de erro reordenado: `-ENODEV`/`-ESHUTDOWN` → `device_gone`; `-EPROTO`/`-EILSEQ`/`-ETIME`/`-ECOMM`/`-EOVERFLOW` → `io_error` (contador); `-EINVAL`/`-EPIPE`/`-ENOENT`/`-EINPROGRESS` → só break (ENOENT = URB morto pelo próprio teardown, não pode contar); default → `io_error` + rtw_err existente |
| `rtw_usb_intf_init` (usb.c:1040-1063) | + `rtwusb->intf = intf;` ao lado do `rtwusb->udev` |
| `rtw_usb_disconnect` (usb.c:1349-1376) | **INTOCADO** — o `usb_reset_device` do unbind (usb.c:1367-1368) continua; com device_gone armado o teardown early-returna (sem flood, sem lixo, sem "Have pending ack frames!") |

O que o patch **NÃO** faz (de propósito): não adiciona retry loop nos helpers (o mecanismo
"retry loop" foi refutado; e a tentativa de mexer em teardown de URB no lwfinger foi REVERTIDA —
patch cirúrgico); não mexe em `rtw_usb_write_port_tx_complete` (rtw88 não olha status de TX ali;
churn desnecessário — deteção via control path + RX + submit cobre); não zera o contador em RX
com sucesso (paridade rtw89: só o control path re-arma a confiança).

### 1.2 DECISÃO -EPROTO × reset (o risco de design crítico) — `eproto_decision`

**Decisão**: `-ENODEV`/`-ESHUTDOWN` armam `device_gone` imediatamente (o USB core JÁ sabe que o
device sumiu — sinal definitivo, zero risco de falso-positivo). `-EPROTO` (e família transitória)
**NUNCA arma direto**: só via `continual_io_error > 4` — 5 falhas CONSECUTIVAS sem UM único
sucesso no meio (qualquer transferência boa zera o contador). O **`usb_queue_reset_device` dispara
na 1ª armada, qualquer que tenha sido a causa** — inclusive a via -EPROTO persistente.

**Por que o reset NÃO pode ser só em -ENODEV/-ESHUTDOWN**: no fantasma medido (20/07), o core
NUNCA devolveu -ENODEV — precisamente PORQUE o disconnect se perdeu, o core acreditava no device
e devolvia **-71 (-EPROTO)** para sempre. Reset só-em-ENODEV = fantasma incurável (quando o core
diz -ENODEV, o disconnect já foi processado e não há fantasma). O único sinal disponível do
fantasma É o -EPROTO persistente.

**Por que isso não derruba o WiFi numa rajada de EMI** (o cenário da máquina):
1. O contador zera em qualquer sucesso de CONTROLE (`rtw_usb_io_ok`), e o watchdog do rtw88_core
   faz I/O de registrador a cada ~2s (`RTW_WATCH_DOG_DELAY_TIME`) — logo o contador é rearmado a
   cada ~2s por construção. Sucesso de RX bulk NÃO zera (paridade rtw89: só o control path re-arma
   a confiança), mas isso é seguro porque `RTW_USB_RXCB_NUM=4` < limiar 5: uma rajada dos URBs de
   RX em voo produz no máximo 4 completions com erro, que não cruzam o limiar. Rajada transitória
   nunca arma; só arma link morto/firmware wedged (5 falhas sem UM sucesso de controle no meio).
2. Cada -EPROTO de control message já embute ~3 retries de hardware do xHC — 5 consecutivos ≈ 15
   falhas de barramento em sequência. Isso não é "EMI transitória", é link morto/firmware wedged.
3. **Evidência medida nesta máquina**: no boot do incidente, o dongle passou 7h (16:15→23:16) sob
   a EMI máxima (a mesma que matava o BT — 2700 reports perdidos do Pro) com **ZERO -71 no
   próprio link 4-3**. A EMI daqui degrada o RÁDIO 2.4GHz (vítimas: BT/controles), não o link
   SuperSpeed do dongle. -71 no dongle só apareceu com firmware wedged (23:16) e device ausente
   (teardown 12:09) — exatamente os dois casos em que o reset é a CURA (re-enumera o wedged;
   destrava o disconnect do ausente).
4. Assimetria de custo: falso-positivo = 1 re-enumeração + reconexão NM (~10s, autocurável;
   `test_and_set_bit` garante UM reset por armada, sem tempestade). Falso-negativo (sem reset) =
   WiFi morto + fantasma até unbind manual/reboot — o status quo que a onda existe p/ matar.
5. **Gate de campo**: module param `hang_reset` (bool, 0644, default Y) desliga SÓ o reset; a
   detecção/silenciamento fica. Com `hang_reset=N` o comportamento vira o do rtw89 vanilla
   (device_gone latcha, I/O muta, sem autorrecuperação) — documentado como troca consciente.

Desvios do rtw89, justificados: (i) rtw89 arma UNPLUGGED também em `-EINVAL`/`-EPIPE` no RX; nós
deixamos `-EPIPE` como o vanilla (agrupado num `break` puro, sem contar nem ressubmeter o URB) —
mais conservador contra falso reset. Consequência honesta: um stall permanente de `-EPIPE` no
bulk-IN com o control path saudável NÃO auto-recupera (o RX silencia após ≤`RXCB_NUM` completions,
idêntico ao vanilla) — não é regressão (o vanilla também não recupera) e nunca foi observado nesta
máquina, onde o sintoma real do fantasma é `-EPROTO`/`-ENODEV` persistente no control path, 100%
coberto; (ii) rtw89 não tem o reset — é a nossa adição (lá nunca houve fantasma reportado; aqui é
a peça que cura; sem ela o patch só silencia o teardown).

## 2. Pacote DKMS multi-módulo (a 2ª instância da infra da Onda T)

**Descoberta que simplificou tudo** (provada no build): o `linux-headers-7.0.11-76070011-generic`
JÁ traz `Module.symvers` completo (32.580 símbolos, incluindo `rtw88_core` e `mac80211`) — os
símbolos do core resolvem SOZINHOS no modpost, sem `KBUILD_EXTRA_SYMBOLS`, sem gerar symvers no
PRE_BUILD. O que os headers NÃO trazem são os **headers privados do rtw88** — e esses vão no
pacote.

**Lista mínima de arquivos (provada por build real)** — fecho transitivo de includes do `usb.c`:
`usb.c` inclui `main.h debug.h mac.h reg.h tx.h rx.h fw.h ps.h usb.h`; `main.h` inclui `util.h`
e `hci.h`; nenhum outro include local. Total: **`usb.c` + 11 headers** (10 deles vanilla
intocados, só `usb.h` é patchado).

```
assets/dkms/rtw88-usb/
├── dkms.conf          # PACKAGE_NAME=hefesto-rtw88-usb, BUILT_MODULE_NAME[0]=rtw88_usb,
│                      # DEST_MODULE_LOCATION[0]=/updates/dkms, AUTOINSTALL=yes,
│                      # BUILD_EXCLUSIVE_KERNEL="^7\.0\.11-"  ← pino de ABI (abaixo)
├── Makefile           # obj-m := rtw88_usb.o ; rtw88_usb-objs := usb.o (2 linhas; os
│                      # CONFIG_RTW88_DEBUG/DEBUGFS/LEDS vêm do autoconf.h do kernel alvo)
├── README.md          # proveniência, invariantes, rebase, upstream
├── usb.c usb.h        # vanilla v7.0.11 + 0001 + 0002
├── main.h debug.h mac.h reg.h tx.h rx.h fw.h ps.h util.h hci.h   # vanilla INTOCADOS
└── patch/
    ├── 0001-wifi-rtw88-usb-fix-memory-leaks-on-USB-write-failures.patch   # upstream verbatim
    ├── 0002-wifi-rtw88-usb-detect-device-gone-and-queue-port-reset.patch  # nosso, git format
    └── BASELINE       # kernel base, commit Pop, SHA256 vanilla/patched/headers-bundle
```

**Pino de ABI (`BUILD_EXCLUSIVE_KERNEL="^7\.0\.11-"`)** — risco que o hid-nintendo NÃO tinha: os
headers privados empacotados congelam o layout interno do rtw88 do v7.0.11. Num kernel novo, o
AUTOINSTALL compilaria contra `struct rtw_dev` VELHO → linka limpo e corrompe memória em runtime.
Com o pino, kernel fora de `7.0.11-*` ⇒ dkms **pula o build** (fail-safe: in-tree volta, nunca
sem WiFi; o install avisa) até o ritual de rebase (BASELINE) atualizar headers + pino juntos.
7.0.y é EOL — não haverá 7.0.12; o próximo kernel do Pop muda de série e cai no pino com certeza.

**Invariantes verificáveis** (mesmo contrato da Onda T, agora com 2 patches): shipping ==
`SHA256_PATCHED_*`; `patch -R` de 0002+0001 reproduz `SHA256_VANILLA_*`; os 10 headers batem
`SHA256_HEADERS_BUNDLE`. Valores já gravados no BASELINE do scratchpad (§8).

**`scripts/dkms_lib.sh`: ZERO ajuste.** Provado: multi-módulo aqui é só "mais arquivos no source
dir" — a helper já copia o diretório inteiro, exclui `patch/`, e o dkms.conf carrega o pino. Os
assets/testes do hid-nintendo (Onda T, commitada) não são tocados. (Se o corretor da onda
discordar e ajustar a lib, re-rodar `tests/unit/test_dkms_lib.py` + suíte da Onda T é obrigatório.)

**CRCs provados no build** (CONFIG_MODVERSIONS=y): nossos exports `rtw_usb_probe`=0x391a4de4 e
`rtw_usb_disconnect`=0x1124d2ff **idênticos ao in-tree** (o patch não muda assinatura exportada)
→ o `rtw88_8822bu` in-tree carrega contra o nosso módulo; os 60 imports (rtw88_core/mac80211/
usbcore) todos com CRC do Module.symvers dos headers.

## 3. Integração install/uninstall/doctor (espelho da Onda T)

- **install.sh**: novo passo `3j` "Onda W: rtw88_usb patchado via DKMS (fantasma USB + teardown
  limpo)" → `install_dkms_rtw88_usb_host()` espelhando `install_dkms_hid_nintendo_host()`
  (install.sh:470-500): mesmo gate `NO_DKMS` (`--no-dkms` desliga AMBOS os módulos — DKMS entra
  por DEFAULT, install SEM FLAGS), mesma checagem `dkms_module_from_updates rtw88_usb` pós-lib,
  mesmo espelhamento nos formatos flatpak/appimage/deb e na seção equivalente do
  `install-host-udev.sh` (install.sh:1243+).
- **Ativação fail-safe (mensagem honesta, 3 estados)**: após staging OK —
  `dkms_module_loaded rtw88_usb` ⇒ "o módulo CARREGADO ainda é o in-tree; **NÃO recarregue com o
  WiFi em uso** — o patch vale no próximo boot ou replug do dongle"; descarregado ⇒ "entra
  sozinho no próximo plug do dongle"; staging falho ⇒ warn da lib + "in-tree continua
  (fail-safe)". A lib JÁ proíbe modprobe/rmmod por contrato (cabeçalho de dkms_lib.sh).
- **uninstall.sh**: bloco simétrico ao da Onda T (uninstall.sh:584-603):
  `dkms_remove_patched_module hefesto-rtw88-usb 1.0.0` → in-tree volta no próximo boot; + remoção
  do conf do NetworkManager (W2) se presente (uninstall simétrico sem flags).
- **doctor.sh** (reusa a estrutura da seção DKMS da Onda T, doctor.sh:1773-1877; constantes novas
  `HEFESTO_DKMS_RTW88_PKG/VER`):
  1. `check_hefesto_rtw88_usb_dkms`: `dkms status` (ausente/instalado/kernel divergente) +
     `modinfo -F filename rtw88_usb` → `updates/dkms`? + **marcador de carga**: existe
     `/sys/module/rtw88_usb/parameters/hang_reset` ⇒ PATCHADO CARREGADO (o in-tree não tem o
     param); módulo carregado sem o param ⇒ "in-tree em uso; patch staged vale no próximo
     boot/replug (não recarregue com WiFi em uso)"; descarregado ⇒ "entra no próximo plug".
  2. `check_usb_fantasma` ("device USB retido: driver segura device removido"): (a) DUPLICATA —
     mais de um device em `/sys/bus/usb/devices/*` com o mesmo idVendor:idProduct do dongle
     rtw88 (a assinatura real do incidente: fantasma 4-3 + device vivo 4-2, mesmos IDs, e só
     existe um dongle físico — comparação lsusb×sysfs é redundante, ambos leem o mesmo core); (b)
     journal do boot com colisão de rename do udev (`wlx.* File exists|Arquivo existe`) — o dano
     concreto; (c) device com driver rtw88 em sysfs sem filho `net/` + `-71` recente no kernel
     log. Cada um vira warn com a cura (`unbind` + caminho sysfs exato).
  3. `check_wifi_powersave`: reporta o powersave EFETIVO do NM (conf.d) sem julgamento até a
     medição W2 existir: `=3` ⇒ info "PS do firmware LIGADO — histórico de instabilidade em
     rtw88 USB; medir com scripts/medir_w2_lps.sh antes de mudar"; `=2` via asset nosso ⇒ pass.
     + contagem de `failed to leave lps state` no boot ⇒ warn se >0 (assinatura do LPS raso).

## 4. W2 — medição do LPS raso (NÃO modprobe.d; script pronto no scratchpad)

`disable_lps_deep` é **NO-OP em USB** e NÃO será instalado: quem seta `RTW_FLAG_LEISURE_PS_DEEP`
são só pci.c/sdio.c/wow.c; o op USB é função vazia (`rtw_usb_deep_ps`, usb.c:836-839). O vilão
ativo é o **LPS raso** (mac80211 `ps_enabled` → `rtw_enter_lps`), ligado hoje via NM
`wifi.powersave=3` (default da distro).

- **`scripts/medir_w2_lps.sh`** (pronto, `bash -n` ok): A/B `nmcli connection modify <conn>
  802-11-wireless.powersave 2` vs `3` + `connection up`; por braço (default 120s): `ping -i 0.2`
  no gateway (mediana/p95/perda), download contínuo `curl` (throughput; iperf3 AUSENTE na máquina
  — se algum dia entrar, vira dependência declarada no install, regra da casa), e janela do
  `journalctl -k` filtrada por `failed to leave lps state|error beacon valid|failed to download
  (rsvd page|firmware)`. **Dry-run por default** (mostra o plano, não toca nada); `--run` exige
  gate humano (derruba o WiFi 2x). **Trap EXIT restaura o powersave ORIGINAL** ganhe quem ganhar.
  O script MEDE E RELATA — não persiste nada.
- **Asset gateado por evidência** (`assets/NetworkManager/hefesto-wifi-powersave.conf`, pronto):
  `[connection.hefesto-wifi-powersave] match-device=type:wifi wifi.powersave=2` p/
  `/etc/NetworkManager/conf.d/`. **NÃO entra no install por default**: entra atrás de opt-in
  `--wifi-powersave-off` E só vira default quando a medição W2 provar ganho (A vence B em
  p95/perda sem regressão de throughput, números no estudo). Uninstall remove sem flag (simetria).

## 5. W3 — coexistência WiFi×BT (script pronto no scratchpad)

**`scripts/medir_w3_coex.sh`** (pronto, `bash -n` ok; dry-run default; `--run` exige root+gate
humano): 3 braços de 120s — A) WiFi ocioso; B) WiFi em carga (curl contínuo); C) `rfkill block
wifi` (**trap EXIT garante unblock** — fail-safe absoluto, nunca deixa o WiFi bloqueado). Por
braço: delta de contadores `hciconfig -a hci0` (RX/TX bytes/acl/errors), captura `btmon -w`
pós-processada (Hardware Error, Disconnection Complete + reason), taxa de reports + 3 maiores
lacunas por controle via evdev (`--evdev /dev/input/eventN`, mesma métrica dos estudos de 19/07),
e debugfs BT (`conn_info_min/max_age`, `supervision_timeout`). O relatório imprime a chave de
leitura (B≈C ruins → tráfego; B ruim/C bom → rádio; piora até em C → EMI do link USB3).

**Topologia como RECOMENDAÇÃO medível, não ação**: WiFi(4-3) + BT(3-1) + Pro(3-2) + 8BitDo(3-4)
dividem o xHCI `0c:00.3`; o `02:00.0` tem 4 portas SuperSpeed LIVRES (bus 2). Mover o dongle p/
lá é mudança de barramento interno (não gambiarra, não é "cabo de rede") — o script instrui:
re-rodar após mover e comparar A/B. Nenhum script/asset move nada automaticamente.

## 6. W4 — 88x2bu (morrownr): DESACONSELHADO, registro de decisão

Sem código nesta onda. Veredito (dados do estudo §6): repo auto-deprecado (README manda usar o
in-kernel ≥6.12), nunca testado em 7.0.x (gate `>=7.0.0` mergeado 19/07/2026 testado só em 7.1.3
XanMod), histórico de quebra a cada série de kernel, e o instalador blacklista `rtw88_8822bu`
(convive mal com o nosso DKMS do rtw88_usb). **Só entra se W1+W2 MEDIDOS falharem**, e mesmo
então via A/B formal (throughput/jitter/quedas/disconnect/impacto no BT) registrado como estudo.
Critério de "falha de W1+W2": fantasma reproduzir COM o patch carregado, ou instabilidade 5GHz
persistir com powersave=2 medido.

## 7. Manifesto por lote (sem interseção) + testes

- **dkms_files**: `assets/dkms/rtw88-usb/{dkms.conf,Makefile,README.md,usb.c,usb.h,main.h,`
  `debug.h,mac.h,reg.h,tx.h,rx.h,fw.h,ps.h,util.h,hci.h,patch/0001-*.patch,patch/0002-*.patch,`
  `patch/BASELINE}` — conteúdo EXATO já pronto no scratchpad (§8).
- **install_files**: `install.sh` (passo 3j + função + espelho packaged), `uninstall.sh` (bloco
  simétrico + NM conf), `scripts/doctor.sh` (3 checks §3). `scripts/dkms_lib.sh` fica FORA
  (zero ajuste).
- **measure_files**: `scripts/medir_w2_lps.sh`, `scripts/medir_w3_coex.sh`,
  `assets/NetworkManager/hefesto-wifi-powersave.conf` (gateado, opt-in até a evidência).
- **test_files** (todos falham-sem/passam-com, sem root/kernel vivo, espelhos da Onda T):
  - `tests/unit/test_dkms_rtw88_usb_assets.py`: dkms.conf campos exatos + `BUILD_EXCLUSIVE_KERNEL`
    presente; Makefile 2 linhas; BASELINE recalculado (shipping==PATCHED; `patch -R` 0002+0001
    devolve VANILLA; headers==HEADERS_BUNDLE); 0002 contém `hang_reset` +
    `usb_queue_reset_device` + SoB anônimo; strings de log do vanilla preservadas byte a byte.
  - `tests/unit/test_install_dkms_rtw88_default.py`: passo por default, gate `--no-dkms`
    compartilhado, args pkg/ver/dir/builtname, mensagem de ativação com "próximo boot".
  - `tests/unit/test_doctor_rtw88_signatures.py`: 3 checks presentes; marcador
    `parameters/hang_reset`; assinatura do fantasma; `failed to leave lps state`.
  - `tests/unit/test_medir_w2_w3_scripts.py`: `bash -n`; dry-run default (sem `--run` NENHUM
    nmcli modify/rfkill no caminho executado); traps de restauração presentes; W2 não escreve
    modprobe.d/NM conf.

## 8. Prova de build (feita HOJE, scratchpad da sessão)

Diretório: `<scratchpad>/onda-w-patch/` (`pkg/` = espelho exato do futuro
`assets/dkms/rtw88-usb/`; `patch/`, `measure/`, `verify/`).

1. `pkg/` montado: vanilla v7.0.11 (sha `969ce8bc…` usb.c / `eb30ffd4…` usb.h) + 0001 (aplicado
   limpo, offsets só) + 0002 → sha finais `70690339…`/`49250514…` (BASELINE).
2. Reversibilidade PROVADA: 0001+0002 forward == pkg; `-R` na ordem inversa == vanilla byte a byte.
3. `make -C /usr/src/linux-headers-7.0.11-76070011-generic M=<pkg> modules` → **`rtw88_usb.ko`
   compila LIMPO** (clean + rebuild 2x; únicos avisos: compiler-differs/pahole, ambientais,
   idênticos aos do hid-nintendo). vermagic `7.0.11-76070011-generic SMP preempt mod_unload
   modversions`; `depends=rtw88_core,mac80211`; params `switch_usb_mode` + `hang_reset`.
4. CRCs: exports idênticos ao in-tree (0x391a4de4/0x1124d2ff); 60 imports todos versionados.
5. `medir_w2_lps.sh`/`medir_w3_coex.sh`: `bash -n` ok; W3 dry-run executado (read-only, zero
   toque); W2 NÃO executado nem em dry-run (toca nmcli só em `--run`, mas a regra da sessão é
   não encostar — fica p/ o gate humano).
6. **Nada instalado**: zero dkms/modprobe/systemctl/nmcli/rfkill no sistema real.

## 9. Riscos e mitigações (honestos)

1. **Reset falso-positivo sob EMI extrema**: possível em teoria se o link SuperSpeed do PRÓPRIO
   dongle falhar 5x seguidas sem 1 sucesso; custo = ~10s de reconexão. Mitigado por limiar +
   zera-em-sucesso + `hang_reset=N` de campo; evidência local diz que EMI não gera -71 no link do
   dongle (§1.2). Residual: aceito conscientemente (assimetria de custo).
2. **`hang_reset=N` latcha mute permanente**: sem reset, device_gone armado por engano só sai com
   replug/unbind (== rtw89 vanilla). Documentado no README; default é Y.
3. **ABI drift em kernel novo**: curado por `BUILD_EXCLUSIVE_KERNEL` (dkms pula, in-tree volta,
   install avisa) + ritual de rebase no BASELINE. Sem o pino seria corrupção silenciosa — pior
   risco do desenho, tratado na raiz.
4. **Reset dispara rebind → re-probe** roda `rtw_usb_switch_mode` de novo (possível dupla
   enumeração USB2→USB3, ~4s, igual ao replug manual de 23:18 do incidente). Cosmético; NM
   reconecta sozinho.
5. **0001 é backport de CVE sem suite de regressão de memória local** — mitigado por ser verbatim
   upstream (`Fixes:` da mesma função) e compilar limpo; o teste real é o de aceite W1.
6. **Aceite W1 exige gate humano** (arrancar o dongle da porta): `USB disconnect` em segundos sem
   unbind; lsusb×sysfs sem duplicata; sem WARN "pending ack frames"; replug reusa `wlx…` sem
   "Arquivo existe". Roda DEPOIS do install + boot/replug — nunca nesta sessão.
7. **Upstream**: 0002 em git format-patch pronto p/ rebase em wireless-next (flag →
   `rtwdev->flags`); SoB placeholder anônimo — submissão real exige DCO com nome real (decisão da
   mantenedora, fora do repo).
