# Auditoria pós-leva S/T/W/L + inventário de pendências — 2026-07-21 (HEAD bebb40d)

Rodada de 5 agentes (S broker · T+W DKMS · L lightbar/LEDs · N/U/G/HANG/R · varredura de
pendências) + verificação ao vivo na máquina. Suíte no HEAD: **4415 passed / 0 failed / 0 skipped**
(2m10s). Releases do GitHub íntegros pós-purga de MAC (37 tags reapontadas, v3.14.0 Latest com 6
assets; tarballs autogerados agora derivam das tags reescritas = limpos).

## 0. Estado real da máquina (corrige a memória de 21/07 00:24)

- O ciclo **uninstall→install FOI rodado em 20/07 22:15** (mtimes de units/confs/DKMS) e o
  **reboot aconteceu em 21/07 10:10**. DKMS T e W construídos e resolvendo para
  `updates/dkms/`; `rtw88_usb` patchado CARREGADO (`hang_reset=Y`, `switch_usb_mode=Y`);
  broker socket ativo escondendo o físico; bt-agent ativo; doctor "tudo OK (12 avisos)".
- **Incidente ao vivo (10:19)**: o Pro Controller BT conectou e ficou no `hid-generic`
  (`unknown main item tag 0x0`; LED de player varrendo sem fixar) — o `hid_nintendo` NÃO
  autocarregou. Coincide com janela de update do PackageKit (`system76-dkms` às 10:21, que
  regenerou `modules.dep` às 10:21:18). Curado ao vivo: `modprobe hid_nintendo` (params da conf
  OK: 3/Y/25/2/250/2000) + unbind/bind → probe BT completo, calibração de usuário carregada,
  `assigned player 1 led pattern`; daemon pintou o LED externo 2s depois
  (`external_led_written hidraw=/dev/hidraw6 slot=1`). **Verificar no próximo boot** se o
  autoload volta ao normal (o alias em `modules.alias` resolve agora).
- **Aberto ao vivo**: DualSense roxo (BT, slot 2 vermelho, hidraw5) adotado e íntegro no
  `daemon.state_full` (uniq, bateria 85%, inputs) mas a mantenedora reportou que **não aparece
  na GUI** — código dos cards (Status e Início) filtraria certo; GUI roda o código do repo
  (venv, cwd correto); stdout/stderr em /dev/null. Diagnóstico pendente de ver a janela.
- **Mistério novo**: `usb 1-6` (bus 1, xHCI 02:00.0) — device *full-speed* falhou a enumeração
  inteira no boot (6-7× `error -71`, endereços 4→7, `attempt power cycle`, desistiu). NÃO é o
  DualSense (BT) nem o padrão do storm de áudio. Candidato: controle no cabo desligado/cabo mau.
- Avisos do doctor a puxar: manifesto do Proton pinado não bate (re-rodar `./install.sh`
  re-verifica SHA256); NENHUM jogo com `hefesto-launch` nas LaunchOptions (usar "Aplicar aos
  jogos"); hidraw0-3 dos receivers CX/Compx em 0666 (conferir se é regra da Aurora — atribuição,
  não necessariamente bug nosso); `wifi.powersave=3` do NM segue ON (esperado até o gate W2).
- Miudeza: units do broker com `Documentation=file:docs/...` inválido (systemd ignora com
  warning; `file:` exige caminho absoluto) — `hefesto-hidraw-broker.socket:17` e `.service:24`.

## 1. Achados por severidade (auditoria de código, verificados linha a linha)

### HIGH

- **S-1 (segurança, escalação local a root)** — `scripts/install-host-udev.sh:281-299`: o
  comando elevado renderiza as units num caminho FIXO de `/tmp` (`sed > /tmp/hefesto-…render`,
  sem `set -e`, cadeia com `;`) e depois `install -Dm644` + `enable --now`. Com
  `fs.protected_regular` (default), arquivo pré-criado por atacante local faz o `sed` de root
  falhar em silêncio e o root instala/habilita a unit DO ATACANTE; sem protected_regular há
  TOCTOU grep→install. O `install.sh` nativo faz certo (`mktemp -d`, linha ~457) — só o caminho
  empacotado (deb/rpm/arch/flatpak) é vulnerável. Fix: `mktemp -d` dentro do comando elevado +
  abortar em falha de escrita.
- **S-2 (viola "duplicado > zero controles")** — backend pydualsense NÃO é broker-aware
  (`backend_pydualsense.py:990` abre por caminho). `lifecycle.py:2164-2173` → `reconnect()`
  (`connection.py:182-193`) fecha TODOS os handles e reabre por caminho com o nó ainda
  ESCONDIDO → `PermissionError` → `connect()` falha para todos → backoff eterno (lease viva,
  rehide no-op, ninguém restaura). Handle morto sem re-enumeração (EIO transitório) dispara.
  Fix: no reopen com `PermissionError` em nó que valida como físico, `client.restore(node)`
  best-effort antes do retry (rehide re-esconde depois) — hidapi não abre por fd.
- **L-01 (eficácia do fix do wake)** — `lightbar_reset.py:100-106` + backend `1180-1183`: a
  assinatura do RESET-02 exige classe sysfs == azul-default `(0,0,128)`, mas o estudo W12 da
  própria base (`2026-07-18-frota-coop-4p/02-lightbar-writers.md:28`) diz que o azul de
  probe/resume NÃO atualiza a classe; e na variante "nó sysfs recriado" o priming escreve o
  desired direto. Ou seja: **no cenário-alvo (caso 17:28) o gatilho provavelmente nunca
  dispara**. Instrumentar o laço de reclaim (DEBUG: transport/current/desired) ANTES do gate
  humano de suspend/wake; se refutar, migrar o gatilho: detector de suspend (salto
  CLOCK_BOOTTIME−CLOCK_MONOTONIC) armando reclaim forçado + 0x08 quando nó é RECRIADO para
  handle BT existente.

### MEDIUM

- **U-F1/U-F2 (trava manual é booleano único)** — `state_store.py:123-140`;
  `ipc_handlers.py:1607`; `autoswitch.py:249-253`. Dois lados da mesma raiz: (a) o fim do
  "Testar motores" (`rumble.passthrough(True)`) limpa a trava INTEIRA e o autoswitch pode
  repintar por cima de LED/gatilho deliberados; (b) um `led.set` arma a trava para sempre e
  suprime inclusive a troca de perfil POR JOGO, sem indicador na GUI. Fix único: trava por
  categoria (led/trigger/rumble) — passthrough limpa só "rumble"; ativação por `steam_app_*`
  poderia liberar categorias não-editadas.
- **U-F3 (renumber zumbi)** — `ipc_handlers.py:532-544`: `wait_for(5s)` sobre `to_thread` não
  cancela a thread; no timeout responde `lock_timeout` mas o compact RODA depois, sem re-checar
  `display_authority` — pode renumerar/repintar com jogo aberto. Fix: re-checar autoridade
  DENTRO de `_renumber_locked` após adquirir os locks.
- **S-3 (belts mortos)** — `uninstall.sh:575` + prerm/postrm/arch/spec chamam
  `--restore-all-and-exit` SEM `HEFESTO_BROKER_ALLOWED_UID` → exit 1 `allowed_uid_missing`
  engolido por `|| true`. O belt nunca funcionou (o teste até assevera o exit errado). Fix:
  flag `--uid N` ou parsear o uid da unit instalada.
- **S-4 (TOCTOU de identidade no minor-reuse)** — `hidraw_broker.py:395-414/344-357`:
  revalidação pós-open cruza só rdevsysfs, não a identidade validada; minor reciclado entre
  uevent e open passa → fd O_RDWR root-aberto de hidraw ALHEIO servido a processo do mesmo uid
  (primitiva de keylogger com teclado BT). Fix: `ioctl HIDIOCGRAWINFO` no PRÓPRIO fd pós-open;
  reler uevent após o pin no hide/restore.
- **S-5 (calibração fura o broker)** — `backend_pydualsense.py:100` via `read_calibration:746`
  abre por caminho; na promoção VPAD-02 (`gamepad.py:599-600`, `release_grab=False`) o nó está
  escondido de propósito → EACCES → calibração canônica silenciosa (drift de gyro — o que o
  GYRO-01 quis evitar). Também corrida no respawn de coop (`coop.py:687-706` agenda restore
  assíncrono; leitura roda antes). Fix: rotear o 0x05 por `open_fd` do broker com fallback.
- **T-1 (default não-vanilla no caminho "exceeded")** — `assets/dkms/hid-nintendo/
  hid-nintendo.c:890-913`: vanilla transmite SEM atualizar timestamp nem `msleep(4)`; o
  patchado com default atualiza+dorme. Contradiz "defaults byte a byte" (inclusive na reversão
  ao vivo via sysfs). Fix de 1 linha (return early no ramo default).
- **W-1 (cura W ligada por default)** — `hang_reset=Y` embutido (`usb.c:23`), ativo AGORA, com
  o gate humano W1 desmarcado. Decisão consciente e justificada no desenho (N latcharia mute
  permanente), mas quebra o slogan "curas opt-in" — ratificar quando rodar W1.
- **PKG-1 (Secure Boot)** — com SB enforcing sem MOK, o load do .ko de updates/dkms FALHA e NÃO
  há fallback ao in-tree (modules.dep aponta um caminho só): máquina de terceiro ficaria sem
  hid-nintendo E sem WiFi. O desenho da T afirma fail-safe (incorreto) e sugere check
  `mokutil` no doctor que não existe. Na máquina de referência não morde (nvidia DKMS prova SB
  resolvido). Fix: check no doctor + warn no install quando SB ativo.
- **L-02 (assinatura consumida)** — entre o wake e o próximo tick (~30s), `defend_display` /
  reassert do unmute / replay retained escrevem a classe e apagam a evidência `(0,0,128)` sem
  mandar 0x08 → lightbar morta até reconectar (cenário: suspend com jogo aberto, jogo morre no
  resume). Fix: check de reclaim ANTES da primeira escrita de classe em nó BT (centralizar) ou
  flag "wake pendente" do detector de suspend.
- **L-03 (cache GUERRA-01 de 1 tick)** — `_refresh_sysfs_leds` recria os `SysfsLedNode` a cada
  `connect()` → `_last_write` nasce vazio → reassert reescreve TUDO a cada ~30s (o "martelar"
  que o GUERRA-01 diz ter curado; docstring de `sysfs_leds.py:58-64` mente). Colateral: é isso
  que faz o reassert pós-0x08 funcionar (invalidação implícita). Quem "consertar" o refresh
  quebra a Onda L em silêncio. Fix: `invalidate_cache()` explícito no laço do reclaim + decidir
  de propósito o destino do cache cross-tick.
- **L-04 (Modo Nativo × claim)** — adoção/wake sob mute suprime o 0x08 (correto) mas o unmute
  reasserta via classe SEM 0x08 e consome a assinatura → jogo não-SDL fica com lightbar morta.
  Fix: "reclaim pendente" por handle BT drenado no unmute antes do reassert.
- **N-01 (defesa de LED é bruta, não dirigida)** — o caminho `verify=True` do reassert é
  inalcançável (defend_display invalida caches antes → verificação só rodava em cache-hit);
  `lightbar_escritor_estrangeiro` nunca loga; a defesa funciona por repintura incondicional
  rate-limitada. Player LEDs OK; externo em modo DS4 (8BitDo BT) segue indefendido (LOW).

### LOW (lista compacta)

- U-F4: `controller.list {external:true}` via `to_thread` SEM timeout — worker travado esgota o
  pool default com o poll de 4s da GUI (`ipc_handlers.py:1497-1499`).
- U-F5: `ExternalImuEnabler` marca `done` no sucesso do `os.write` com `packet_num=0` fixo —
  subcomando dropado por dedup de contador nunca é retried (`external_identity.py:444-456`).
- U-F6: `BaseEvdevReader.stop()` com join-timeout pode deixar 2 threads vivas
  (`evdev_reader.py:504-543`) — guard barato: contador de geração.
- U-F7: backport BlueZ sob `--yes` reinicia bluetoothd sem confirmação individual
  (`install.sh:1259-1268`) — considerar default "n" com controle BT conectado.
- U-F8/S-11: `broker_executor_for`/`broker_client_for` ressuscitam executor/lease pós-shutdown
  (`hidraw_broker_client.py:383-399`, `connection.py:421-439`) — gate por `_is_stopping`.
- S-6: `gamepad.py:223` itera `players.items()` sem cópia em thread concorrente → rehide do
  ciclo perdido (até +30s de exposição). Fix: `list(...)`.
- S-7: multi-seat — `restore_all_physical` clobra ACL de outro usuário (nicho single-user).
- S-8: partial send de `sendmsg` não tratado (respostas <200B, improvável).
- S-9: modo manual (debug) do broker faz unlink do socket VIVO da socket-unit.
- S-10: timeout de 2s numa chamada derruba a lease inteira (fail-safe correto; melhoria =
  rehide imediato pós-reconexão da lease).
- W-3: receita do `BASELINE` do rtw88 quebrada (`patch -R -p6 usb.c usb.h < …` — usb.h vira
  arquivo de patch). Só a receita humana; testes usam a invocação certa.
- T-2: hid-nintendo sem pino de kernel — em upgrade que ainda compile, o DKMS mascara o
  in-tree mais novo para sempre e o doctor dá pass. Fix: warn quando `uname -r` ≠
  `KERNEL_TESTED`.
- PKG-2: uninstall mudo se o binário `dkms` sumiu (ko órfão vence o in-tree p/ sempre).
- PKG-3: versão `1.0.0` hardcoded em install.sh:520,584 / uninstall.sh:623,667 (parsear do
  dkms.conf como o install-host-udev faz).
- L-05: falso-positivo do priming manda 0x08 espúrio + loga `…_wake` sem wake (inofensivo;
  discriminador: `_sysfs_written[key] == KERNEL_DEFAULT_BLUE`).
- L-06: `__all__` de lightbar_reset sem `should_reclaim_on_wake`; TOCTOU ~ms do `_output_mute`;
  nenhum teste cobre 0x08→refresh→reassert fim-a-fim (gate humano).
- DOC-1: msg do commit W imprecisa (RX bulk também incrementa o contador); parity sem o
  `else` informativo no bloco hid-nintendo (cosmético).

### Vereditos gerais por onda

- **S (broker)**: núcleo acima da média (lease por EOF, refcount, restore verificado, validador
  BLUEZ-UHID-01, executor FIFO); problemas nas BORDAS de integração (S-1, S-2, S-3).
- **T/W (DKMS)**: engenharia alta — patches reverse-aplicam aos SHAs vanilla, lib fail-safe,
  pino de ABI da W correto, remoção simétrica em todos os formatos, gate anti-EMI resiste a
  leitura adversarial do C. Corrigir antes de release a terceiros: T-1, PKG-1, W-3.
- **L**: forma disciplinada (decisão pura testada, gates de mute completos); risco real é a
  EFICÁCIA do gatilho do RESET-02 (L-01/L-02/L-03) — instrumentar antes do gate humano.
- **N**: sólida (3 vetos respeitados, merge em ponto único, NUMA-04 com lock único; ordem de
  locks consistente). HANG-01: objetivo cumprido. G: disciplinada (USB-only, OUI exato, ≤2
  tentativas). U: Causa A coberta; arestas F1/F2/F3. R: cuidadosa e simétrica.

## 2. O que ficou por fazer (inventário)

### A. Gates humanos ao vivo (bloco principal — checklist inteiro sem marcar)

`docs/process/CHECKLIST-VALIDACAO-5-ONDAS.md` (nenhum item marcado): Steam sem jogo não repinta;
2 DualSense sem "sony 1/sony 4" + botão Renumerar; perfil eterno curado; Início toggle; Lightbar
presets/player-LEDs; Rumble testar/devolver; Sackboy com wrapper; número do jogo/paleta volta;
rumble+gatilhos; gyro aiming em jogo (USB e BT); enable_imu do Pro NO CABO; abrir Steam sem
derrubar BT; re-pair JustWorks; broker (jogo sem wrapper não vê o físico; kill -9 <1s; gyro
sobrevive); T A/B da cura com rádio degradado; W fantasma (mover dongle de porta) + medições
W2 (`medir_w2_lps.sh`) e W3 (`medir_w3_coex.sh`); L suspend/acordar (instrumentar antes — L-01).
Mais: T2.4/T3 do sprint T; matriz BT-07/RDR2 de 7 células; A/B do cliente Steam isolado (dongle
fora); efeito real de zerar SwitchSupport; U4/U7/U8 investigar ao vivo pós-Causa A.

### B. Planejado e não iniciado

W4 (driver 88x2bu A/B); usbhid.jspoll (protocolo benchmark+replug nunca executado); BR/EDR finos
(LinkSupervisionTimeout, sniff — só com medição); detecção de bond quebrado no DAEMON/GUI
(doctor já cobre); cache do feature 0x05 por MAC (mitigação BT); ROADMAP.md defasado
(2026-05-16 — reescrever pós-release).

### C. Higiene

rm compensatório 73/74 sai no próximo release (`install_udev.sh:84-87`); formalizar destino do
`hefesto-dsx-recover.service` (hoje opt-in manual de facto); `venv/` legado na raiz (uninstall
só remove `.venv`); doc de convivência input-remapper (U13); `docs/process/estudos/README.md`
indexa só 16/07; `Documentation=` das units do broker.

### D. Testes/CI

CI roda só `tests/unit` (tests/core/integration fora — `ci.yml:99`); GUI cega na CI (sem
gi/GTK); markers `requires_gtk`/`requires_display` mortos; 134 violações de acentuação
(81 tests/unit, 30 docs, 7 src) — política "só linhas tocadas" segue.

### E. Decisões da mantenedora

1. 7 branches antigas com MAC real no origin, bloqueadas pelo pre-push hook (commits do André):
   bypass `--no-verify` / deletar / mailmap.
2. Envio upstream dos patches de kernel (format-patch prontos com Signed-off-by).
3. Release + merge para main (origin/main em v3.13.3; CHANGELOG `[Unreleased]` acumula desde
   v3.14.0) — segurado até validação ao vivo.
4. Promoção do W2 (`--wifi-powersave-off` default?) e W4 — gateados por medição.
5. Ratificar W-1 (`hang_reset=Y` default) quando rodar o gate W1.

### F. TODOs no código

Praticamente zero — único TODO é citação de bug da pydualsense (`backend_pydualsense.py:9`).

## 3. Ordem sugerida de ataque — STATUS (21/07 tarde)

1.  **FEITO — Lote 1 (broker bordas)** commit `4184f79`: S-1 (mktemp -d no comando elevado),
   S-2 (`_broker_restore_for_recovery` no reconnect + probe), S-3 (belt com uid em cascata:
   env → `--allowed-uid` → parse da unit), S-6 (snapshot da iteração), `Documentation=` das units.
2.  **FEITO — Lote 2 (GUI/autoswitch)** commit `3c887f5`: U-F1/F2 (trava manual por categoria
   {trigger,led,rumble}; passthrough limpa só "rumble"; autoswitch cede ao perfil de jogo),
   U-F3 (renumber re-checa autoridade dentro dos locks, `_RenumberAuthorityChangedError`).
3.  **PARCIAL — Lote 3 (lightbar)** commit `57fb185`: L-01 = instrumentação DEBUG do reclaim
   (`lightbar_reclaim_avaliado`) ENTREGUE. L-02/L-03 (trocar o gatilho para detector de suspend /
   nó recriado em handle BT) ADIADOS de propósito para DEPOIS do gate humano de suspend/wake —
   a decisão de design depende do que o DEBUG mostrar ao vivo.
4.  **FEITO — Lote 4 (DKMS release-ready)** commit `d65ded9`: T-1 (.c+patch+BASELINE vanilla),
   W-3 (receita do BASELINE), T-2 (doctor: drift de kernel), PKG-1 (doctor+install: Secure Boot),
   PKG-2 (uninstall: dkms ausente com órfão), PKG-3 (versão do dkms.conf, não literal).
5.  **PENDENTE (humano) — gates do checklist** `CHECKLIST-VALIDACAO-5-ONDAS.md`, agora com os
   fixes 1/2/4 aplicados (uninstall→install rodado nesta sessão). Inclui o gate de suspend/wake
   que fecha a decisão do L-02/L-03 com o DEBUG do item 3.
6.   **FEITO — S-4 (segurança)** commit `37b977c`: `open_node` valida a identidade pelo
   `HIDIOCGRAWINFO` no próprio fd (à prova de corrida; ioctl 0x80084803 validado ao vivo contra o
   kernel, vpad 0df2→False); `_pin` re-lê o HID_ID do uevent no hide/restore (ilegível→prossegue,
   só root o esconde). Fecha a primitiva de keylogger do minor-reuse.
7.   **FEITO — INSTALL-HEADLESS-01** commit `c99250b`: `./install.sh` SEM FLAGS funciona sem TTY —
   `ask_yn` sem terminal usa o default (não mata o `set -e` no EOF do `read`, que matava o passo 4);
   `acquire_sudo` (install+uninstall) tenta `sudo -A -v` com `SUDO_ASKPASS`.
8.   **FEITO — S-5 (drift do gyro)**: `read_calibration` aceita opener injetável
    (`set_feature_opener`); o daemon injeta `make_broker_opener` em `_wire_feature_opener` — a
    feature 0x05 é lida por fd root do broker (funciona com o nó escondido), fim do EACCES →
    canônico → drift. Cobre promoção do vpad E respawn de coop. LIVE (`feature_opener_wired`).
9.   **GATED NA VALIDAÇÃO HUMANA (não fechar por código sem o dado ao vivo):** L-02/L-03/L-04
    (gatilho do wake da lightbar — instrumentar 1º com L-01, decidir DEPOIS do gate suspend/wake;
    mexer agora arriscaria a Onda L não-validada); W-1 (ratificar `hang_reset=Y` — precisa da
    medição W2/W3, gate humano).
10.  **BACKLOG LOW deferido (valor marginal; melhor num pass focado, não empilhado antes da
    validação):** U-F4 (o `wait_for` seria parcial, não previne o pile-up real), U-F5/F6/F7/F8,
    S-7 (nicho single-user), S-8/S-9/S-10/S-11, DOC-1. Nenhum HIGH/MED; dívida rastreada.

**Descoberta 21/07 tarde — o "Pro some da GUI" NÃO é bug de serialização.** O
`discover_external_gamepads` volta vazio porque o Pro **não tem evdev** (meio-ligado: HID/`nintendo`
ativo, IMU chegando, mas o probe BT não registrou o input). A cura da Onda T (`bt_probe_retries=3`)
está DESLIGADA até o reboot (params 0/N — o uninstall zerou e o módulo carregado ainda é o de safra
anterior). O daemon escreve o LED (via hidraw/OUI) mas a GUI (via evdev) não vê nada porque não há
evdev. **Raiz = probe frágil sem a cura ativa; o REBOOT (ativa a Onda T + o `.ko` novo) é a cura** —
não é patch de daemon.

**NÃO commitado/pushado ainda:** os commits desta sessão (`4184f79`..`37b977c`) estão LOCAIS —
push é decisão da mantenedora (a branch da fork já foi force-pushada na purga de MAC; ver
[[purga-mac-historico-20260720]]).
