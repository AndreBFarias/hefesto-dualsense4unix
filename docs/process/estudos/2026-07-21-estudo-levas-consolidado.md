# Estudo 2026-07-21 — Levas concluídas desde 15/07: inventário consolidado e mapa de materialização

**Objetivo**: responder com precisão "o que está materializado em `docs/process/` vs. o que só
vive na memória persistente do assistente" para cada leva/onda de trabalho desde a Onda Harmonia
(15/07). Fonte: `docs/process/estudos/`, `docs/process/sprints/`, `docs/process/CHECKLIST-VALIDACAO-
5-ONDAS.md`, os arquivos de memória em `~/.claude/projects/.../memory/`, e `git log`. Nada aqui foi
inventado — cada linha do inventário cita a fonte.

**Achado de partida**: a crença da mantenedora de que só a leva do BlueZ e o estudo MMJ estão
materializados é verdadeira apenas para os dois documentos **novos e ainda não commitados** desta
sessão (`git status` os mostra como `??`). Todo o histórico anterior (15/07 em diante) TEM,
sim, documentação commitada em `docs/process/sprints/` e `docs/process/estudos/` — a cobertura real
é muito maior do que ela lembra. As lacunas verdadeiras são pontuais (ver seção "Lacunas de
materialização"), não a régua inteira.

---

## 1. Inventário de levas (15/07 → 21/07)

| # | Leva/onda | Período | Objetivo | Status | Commits principais | Materializada em |
|---|---|---|---|---|---|---|
| 1 | **Harmonia** (vpad uinput→uhid, co-op checkbox, PT-BR) | 15/07 | Fundação uhid do vpad DualSense; UI em português; um dono por conceito | Entregue no hardware; release segurado (faltava sentir rumble em jogo real) | 8 commits `sprint/harmonia-uhid` (não isolados no log atual, squashed na história) | `docs/process/sprints/2026-07-15-sprint-harmonia-*.md` + `2026-07-15-INDEX-harmonia.md` + `docs/process/estudos/achado_uhid_vpad_dualsense_real` (memória) |
| 2 | **Auditoria Harmonia** (9 áreas, 84 bugs) | 15/07 | Auditar a onda antes de liberar | Entregue (auditoria) | — | `docs/process/sprints/2026-07-15-auditoria-resultado-consolidado.md` + `2026-07-15-anexo-inventario-de-textos.md` |
| 3 | **Fases 1-3 multicontrole/dedup** (vpad Edge sintético, wrapper fail-safe, perfis por controle) | 16/07 (noite) | Vpad nunca mais divide VID/PID com físico; launch option fail-safe; fundação 4P | Entregue e validado ao vivo | `bc68718`, `f2e2aad`, `8e59601` | `docs/process/sprints/2026-07-16-CHECKPOINT-fases-1-3-construidas.md`, `2026-07-16-INDICE-onda-multicontrole-e-dedup.md`, `2026-07-16-sprint-vpad-sempre-edge.md`, `-dedup-sem-launch-option.md`, `-perfis-por-controle.md` |
| 4 | **Achado: launch option veneno** | 16/07 | Causa-raiz de "0 controles" com IGNORE_DEVICES | Investigação fechada | — | `docs/process/sprints/2026-07-16-sprint-autoswitch-e-launch-options.md` + memória `achado_launch_option_veneno_20260716` |
| 5 | **Fases 4-5** (cor automática por controle, aba Status em cards, 8BitDo sem mentiras) | 17/07 (madrugada) | Paleta PS5 automática; identidade MAC→slot; inventário externo read-only | Entregue, instalado; gates humanos pendentes | `17006f2` + fix pós-install | `docs/process/sprints/2026-07-17-CHECKPOINT-fases-4-5-construidas.md`, `2026-07-16-sprint-cores-e-led-automaticos.md`, `-status-por-controle-e-cores.md` |
| 6 | **Auditoria onda multicontrole (28 agentes)** | 17/07 (manhã) | Validar as 5 Fases "com perfeição"; jargão pro leigo | 6 HIGH + 41/52 MED/LOW corrigidos; release **v3.14.0 publicado** | vários, ver `docs/process/sprints/2026-07-17-AUDITORIA-*` | `docs/process/sprints/2026-07-17-AUDITORIA-onda-validacao-e-correcoes.md` |
| 7 | **8BIT-02** (controles externos no seletor, ficha read-only, LED via daemon) | 17/07 (tarde) | Nintendo/8BitDo aparecem no seletor; daemon numera e acende LED | Entregue, validado ao vivo | `9532eb1`, `d4c5874` | `docs/process/sprints/2026-07-16-sprint-8bitdo-e-outros-controles.md` |
| 8 | **Lightbar BT × ADOÇÃO** (Reset LED 0x08) | 17/07 (noite) | Lightbar apagava na adoção BT | Entregue | `e855f0d`, `62483b2` | `docs/process/sprints/2026-06-28-lightbar-bt-auditoria-producao-v3.10.0.md` (base) + memória `sessao_coop_misto_lightbar_p2_20260717` |
| 9 | **Guerra de escritores hidraw** (winebus Proton 10/11 expõe físicos por default) | 18/07 | PROTON_DISABLE_HIDRAW; keepalive neutro; report BT malformado | Investigação + curas decididas | agrupado no commit `b4589a1` "fim da guerra" | `docs/process/estudos/2026-07-18-estudo-guerra-de-escritores-hidraw.md` |
| 10 | **Onda Plataforma** (Proton pinado, USB sem economia, BT máximo, Game Mode) | 18/07 | Estabilidade de plataforma independente do hefesto | Entregue (parte do commit `b4589a1`) | `b4589a1` | `docs/process/sprints/2026-07-18-sprint-plataforma-proton-usb-bt.md`, `-sprint-nucleo-fim-da-guerra.md`, `-sprint-infra-kernel-install.md` |
| 11 | **Broker hide-hidraw (1ª tentativa, "future-broker")** | 18-19/07 | Esconder hidraw físico do jogo | **Parkado** (broker×motion colidia) — removido, superado pela Onda S | — | `docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md` + memória `leva_final_auditoria_broker_parkado_20260719` |
| 12 | **BlueZ 5.85 backport (Onda R original)** | 19/07 | Curar bugs #815/HIDP do BlueZ 5.72 stock | Entregue (backport instalado) | `6d6d252` (install integra) | `docs/process/estudos/2026-07-19-estudo-bluez-backport-onda-r.md` |
| 13 | **BLUEZ-UHID-01** (input BT vira uhid ≥5.73; filtro por identidade) | 19/07 | Daemon não cegar para input BT via uhid | Entregue | incluso na leva N/R/HANG/G/U | memória `achado_bluez_uhid_01_20260719` (sem doc de estudo dedicado além da menção acima) |
| 14 | **Maratona 5 ondas: N/R/HANG/G/U** | 19/07 (noite) | Numeração una, install BlueZ, HANG-01 (poll trava), gyro Nintendo cabo, GUI "perfil eterno" | Entregue e instalado | `c223a83`(N) `6d6d252`(R) `6a3c3cc`(HANG-01) `6f619a0`(G) `4f6f223`(U) | `docs/process/sprints/2026-07-19-INDICE-maratona-noite.md` + `-sprint-numeracao-una.md` + `-sprint-onda-r-radio-install.md` + `-sprint-hang-01-tick-resiliente.md` + `-sprint-onda-g-gyro02-doctor.md` + `-sprint-onda-u-gui-regressoes.md` |
| 15 | **Triagem Onda U (Causa A)** | 20/07 | Achar a causa-raiz do "perfil eterno" | Investigação fechada | incluso em `4f6f223`/correções seguintes | `docs/process/estudos/2026-07-20-triagem-onda-u-gui.md` |
| 16 | **Premissas T/W validadas no source** | 20/07 | Confirmar mecanismo antes de patchear kernel | Investigação fechada | `15abbf8` | `docs/process/estudos/2026-07-20-estudo-premissas-onda-t-hid-nintendo.md` + `-onda-w-rtw88.md` |
| 17 | **Onda S — broker root hide-hidraw (fd-injection)** | 20/07 (tarde) | Esconder hidraw físico sem quebrar o motion reader | Entregue e ativo | `40fd33b`/`bee4677` | `docs/process/estudos/2026-07-20-desenho-onda-s-broker-fd-injection.md` |
| 18 | **Onda T — hid-nintendo DKMS (patch 0001)** | 20/07 (tarde) | Probe BT resiliente + parar de martelar o rádio | Entregue; ativação só no reboot | `7a8e82f`/`f6c20d8` | `docs/process/estudos/2026-07-20-desenho-onda-t-patch-dkms.md` |
| 19 | **Onda W — rtw88_usb DKMS** | 20/07 (tarde) | Cura do "fantasma USB" do dongle WiFi | Entregue; ativação só no reboot | `858872a`/`f1da9b5` | `docs/process/estudos/2026-07-20-desenho-onda-w-patch-dkms.md` |
| 20 | **Onda L — lightbar no wake BT** | 20/07 (tarde) | Reenviar Reset 0x08 na borda do wake, não só na adoção | Entregue; gate humano (suspender/acordar) pendente | `f11b0e9`/`9a842c9` | **Sem doc de desenho dedicado.** Só a validação/achado em memória (`achado_lightbar_bt_borda_wake_20260720`) e menções no `CHECKLIST-VALIDACAO-5-ONDAS.md` e na auditoria (`2026-07-21-auditoria-pos-leva-stwl.md`) |
| 21 | **Auditoria cross-cutting S/T/W/L** | 20/07 (fim de tarde) | Interação entre as 4 ondas simultâneas | 6 achados, todos corrigidos | `95c44af`/`bebb40d` | Coberta dentro dos docs de desenho S/T/W (sem doc próprio; ver memória `leva_std_wl_completa_20260720`) |
| 22 | **Purga de MAC no histórico Git** | 20/07 (noite) | Remover MACs reais de commits pushados | Entregue (main/sprint/4 branches/37 tags); 7 branches antigas bloqueadas | `git filter-repo --replace-text` (fora do log de commits normais) | **Sem doc em `docs/process/`.** Só memória `purga_mac_historico_20260720` |
| 23 | **Auditoria pós-leva S/T/W/L (5 agentes)** | 21/07 (manhã) | Inventariar pendências reais da leva de 20/07 | Entregue (relatório) | `b0e2f58` | `docs/process/estudos/2026-07-21-auditoria-pos-leva-stwl.md` |
| 24 | **Lotes 1/2/4 + L-01 + INSTALL-HEADLESS-01 + S-4 + S-5** (correções da auditoria) | 21/07 | Corrigir os HIGH/MED apontados na auditoria acima | Entregue e instalado ao vivo | `4184f79`(lote1) `3c887f5`(lote2) `d65ded9`(lote4) `57fb185`(L-01) `c99250b`(INSTALL-HEADLESS) `37b977c`(S-4) `d094e19`(S-5) | Atualizações **dentro do próprio** `2026-07-21-auditoria-pos-leva-stwl.md` (commits `e12588c`, `446bd57`, `755c5d2`) + `CHECKLIST-VALIDACAO-5-ONDAS.md` |
| 25 | **Instalação NOPASSWD headless** (técnica operacional) | 21/07 | Rodar install/uninstall sem TTY | Resolvido (técnica) | — | **Sem doc.** Só memória `install_nopasswd_headless_20260721` (referência operacional, não leva de produto) |
| 26 | **VPAD-09 (21/07) — borda de conexão revive vpad + grupo `hefesto`** | 21/07 (pós-reboot) | Corrigir a race da ACL uaccess que fazia a emulação morrer inteira no boot | Entregue e ativo | `ff374da`, `459e9f1` | **Sem doc em `docs/process/`.**  Atenção: existe um doc `2026-07-16-sprint-vpad-sempre-edge.md` com uma seção também chamada "VPAD-09" — é **outro item, sem relação** (co-op com controles não-DualSense, de 16/07). Colisão de nome só na memória (`auditoria_pos_leva_20260721`) e nas mensagens de commit |
| 27 | **TOUCHPAD-76-BT-VPAD-01** | 21/07 (pós-reboot) | Regra udev 76 não cobria touchpad BT nem o do vpad → cursor duplicado no FPS | Entregue | `aa8dd68` | **Sem doc.** Só memória `auditoria_pos_leva_20260721` e a mensagem do commit |
| 28 | **Estudo MMJ — caminhos DualSense (7 agentes)** | 21/07 (noite) | Por que o vpad é invisível ao Mullet Mad Jack; mapa dos 3 caminhos | Entregue (estudo + recomendações, sem código) | — | `docs/process/estudos/2026-07-21-estudo-mmj-caminhos-dualsense.md` (**ainda não commitado**, `??` no git status) |
| 29 | **DKMS hid-nintendo patch 0002 + tuning** (registra LEDs mesmo com SET inicial falho) | 21/07 (noite, dentro da sessão Sackboy do estudo MMJ) | Curar o Pro Controller sem LEDs/evdev quando o rádio congestiona | Entregue e ATIVO no sistema (`/sys/module` confere 3/Y/Y/4/500/4000) | ainda **não commitado** (arquivos `M`/`??` no git status: `hid-nintendo.c`, `BASELINE`, `patch/0002-*.patch`, `README.md`, conf) | Só o "Adendo 21/07 noite" dentro do `2026-07-21-estudo-mmj-caminhos-dualsense.md` + memória `checkpoint_pos_install_crash_bt_20260721` |
| 30 | **8BIT-03 — SDL_GAMECONTROLLER_USE_BUTTON_LABELS** | 21/07 (noite) | 8BitDo com A/B trocados no jogo (etiquetas Nintendo por default) | Entregue, ativo no launch_env | não commitado ainda (mesmo lote acima) | Adendo do estudo MMJ (item 4) |
| 31 | **Crash crônico do bluetoothd (#6, 21/07 22:14) — heap corruption `unaligned fastbin`** | 21/07 (noite) | Registrar o 6º crash, gatilho (rmmod com BT vivo) e sequelas (3 bonds destruídos) | Incidente registrado; mitigação operacional acordada (nunca `rmmod` driver HID com BT vivo) | — (incidente, não código) | Mecanismo citado resumidamente em `2026-07-21-sprint-pesquisa-bluez-estabilidade.md` (fato medido #2); **playbook por MAC/controle e "sequelas" só em memória** (`checkpoint_pos_install_crash_bt_20260721`, `achado_bluetoothd_crash_cronico_20260719`) |
| 32 | **Sprint (pesquisa): estabilidade do BlueZ** | 21/07 (noite) | Decidir versão/integração do BlueZ por pesquisa neutra, sem viés | Aberta (pesquisa, nenhuma decisão tomada — por design) | — | `docs/process/sprints/2026-07-21-sprint-pesquisa-bluez-estabilidade.md` (**ainda não commitado**, `??` no git status) |

---

## 2. Detalhe por leva — entregue, gated, armadilhas

### Harmonia + Fases 1-5 + auditorias (15-17/07)
- **Entregue**: vpad 100% sintético (nunca lê o físico; blueprint fossilizado), wrapper
  `hefesto-launch` fail-safe (pior caso é duplicado, nunca zero controles), perfis por controle
  (merge por campo), paleta PS5 automática + aba Status em cards, 8BIT-02 (externos no seletor).
- **Gated na época**: sentir rumble em jogo real (Harmonia); layout PS no Sackboy USB; BT com
  journal; 4 controles nunca exercitados — todos fechados em rodadas posteriores (documentado
  no fluxo dos checkpoints de fase).
- **Armadilha a não repetir**: testes de GUI que exigem stack `gi`+`cairo` completa NÃO rodam na
  CI headless de release (custou 4 rounds no v3.14.0) — usar `importorskip("cairo")` +
  `sys.modules["cairo"]=None` para simular localmente.

### Guerra de escritores hidraw + Onda Plataforma (18/07)
- **Entregue**: `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` (a env moderna, pois `PROTON_ENABLE_HIDRAW`
  morreu no Proton 10/11); keepalive neutro; Proton pinado por SHA256; USB sem economia
  (autosuspend=-1); BT máximo (autosuspend btusb=0).
  Fonte: `docs/process/estudos/2026-07-18-estudo-guerra-de-escritores-hidraw.md`.
- **Armadilha**: `SDL_GAMECONTROLLER_IGNORE_DEVICES` NÃO filtra o caminho winebus dos Protons
  10/11 — não confiar nela sozinha. Ler inventário externo por poll também pode ESCREVER LED e
  estourar rate-limit do hid-nintendo (já corrigido, mas o padrão "leitura pura vs. side-effect"
  deve ser respeitado em código novo).

### Broker (1ª tentativa parkada 18-19/07 → Onda S entregue 20/07)
- **Beco sem saída documentado**: esconder o hidraw físico via ACL/chmod sem fd-injection quebra
  o motion reader (bate EACCES ao reabrir o nó escondido) — por isso a 1ª tentativa foi parkada.
  A cura definitiva (Onda S) usa `SCM_RIGHTS` para entregar o fd já aberto, nunca reabrindo por
  caminho enquanto o nó está escondido.
- **Entregue (Onda S)**: broker root com validação de identidade D1-D4 (nunca por topologia),
  executor dedicado (não fura o HANG-01), fail-safe (broker ausente = duplicado, nunca zero).
- **Risco residual aceito**: janela de ~2s de exposição no replug; uhid forjado do mesmo UID
  passa sem checagem (sem escalonamento — já era dono via uaccess).

### N/R/HANG/G/U — maratona da madrugada de 19/07
- **Entregue**: numeração una (`game_signal`/`display_authority`/defesa de LED), install integra
  BlueZ 5.85 + JustWorks + bt-agent, poll loop nunca mais trava (HANG-01), IMU do Nintendo Pro no
  cabo, GUI "perfil eterno" investigado (ver Onda U abaixo).
- **Causa-raiz do "perfil eterno" (Causa A, achada em 20/07)**: os handlers IPC de aplicação
  parcial (`led.set`, `rumble.set`, `DraftApplier.apply`) não armavam a trava manual — o
  AutoSwitcher reaplicava o perfil salvo por cima da edição da usuária a cada troca de foco.
  Fonte: `docs/process/estudos/2026-07-20-triagem-onda-u-gui.md`.
- **Armadilha**: a trava manual virou (na 1ª correção) um booleano ÚNICO — terminar "Testar
  motores" na Rumble apagava também a trava de cor da Lightbar. Corrigido depois virando um
  CONJUNTO de categorias {trigger, led, rumble} (lote 2 da auditoria de 21/07, `3c887f5`).

### S/T/W/L (20/07 tarde) + auditoria cross-cutting
- **Entregue e ativo**: broker (S), patch hid-nintendo DKMS 0001 (T, probe BT resiliente +
  para de martelar o rádio), patch rtw88_usb DKMS (W, device-gone + `usb_queue_reset_device`
  no fantasma USB), reenvio do Reset 0x08 na borda do wake BT (L).
- **Gated (ativação só no próximo boot, por design fail-safe do install)**: T e W não recarregam
  módulo com controle/WiFi em uso.
- **Gated (validação humana)**: L-02/L-03/L-04 (o gatilho do wake — `L-01` da auditoria de 21/07
  levanta a hipótese de que a assinatura atual PROVAVELMENTE nunca dispara no caso real, precisa
  de instrumentação DEBUG antes do gate); W2/W3 (medição do `hang_reset`/LPS via scripts
  dedicados, execução é gate humano).
- **Achado importante sobre o risco de reset do W (validado)**: o reset do W **não dispara** numa
  rajada de EMI porque `RTW_USB_RXCB_NUM=4` fica abaixo do limiar 5 de completions em voo — risco
  central da onda foi PROVADO inócuo, não presumido.
- **Armadilha (pino de ABI, único HIGH real da Onda W)**: o patch precisa travar no build EXATO
  do kernel (`^7\.0\.11-76070011-`), não só na versão nominal — um respin da mesma 7.0.11
  corromperia memória por offset resolvido em compile-time.

### Auditoria pós-leva 21/07 + lotes 1/2/4 + INSTALL-HEADLESS + S-4/S-5
- **Entregue**: mktemp -d no comando elevado (S-1, escalação local a root fechada);
  `_broker_restore_for_recovery` no reconnect (S-2, "duplicado > zero controles" restaurado);
  trava manual por categoria (lote 2); doctor detecta drift `uname -r` vs. kernel testado (T-2);
  aviso de Secure Boot (PKG-1); `./install.sh` funciona sem TTY/flags via `ask_yn` com default em
  não-interativo (INSTALL-HEADLESS-01); identidade do hidraw por `HIDIOCGRAWINFO` (S-4, fecha
  primitiva de keylogger por minor-reuse); calibração 0x05 lida via broker opener (S-5, fim do
  drift do gyro com hidraw escondido).
- **GATED conscientemente (não esquecimento)**: L-02/L-03/L-04 e W-1 (ratificar `hang_reset=Y`)
  ficam para a validação humana ao vivo — mexer sem o gate arriscaria a Onda L não-validada.
  LOWs (U-F4..F8, S-7..S-11, DOC-1) viraram backlog deferido por valor marginal.
- **Armadilha (S-1)**: o caminho NATIVO do install (`install.sh`) já usava `mktemp -d`; só o
  caminho EMPACOTADO (deb/rpm/arch/flatpak via `install-host-udev.sh`) tinha o `/tmp` fixo — ao
  auditar scripts elevados, sempre conferir os DOIS caminhos (nativo × empacotado).

### VPAD-09 (21/07) + TOUCHPAD-76-BT-VPAD-01 (incidentes pós-reboot, sem doc)
- **VPAD-09 (21/07)**: o daemon de sessão perdia a corrida contra o logind aplicando a ACL
  uaccess de `/dev/uhid`/`/dev/uinput` no login → emulação inteira falhava
  (`gamepad_emulation_start_failed`) → jogo via o físico cru ("pra cima infinito" no Mullet Mad
  Jack). Cura imediata: revive na borda de conexão (`ff374da`). Cura determinística: grupo
  dedicado `hefesto` nas regras udev 71-* em vez de depender do uaccess do logind (`459e9f1`).
  **Nunca usar o grupo `input`** (equivale a keylogger).
- **TOUCHPAD-76-BT-VPAD-01**: a regra udev 76 só casava o nome USB do touchpad; em BT/uhid o
  nome muda (`DualSense Wireless Controller Touchpad` / `Hefesto Virtual DualSense P1 Touchpad`)
  e nenhum ganhava `LIBINPUT_IGNORE_DEVICE` → 2 ponteiros vivos, cursor em dobro no FPS. Fix:
  wildcard `*DualSense*Touchpad` (`aa8dd68`). A flag só vale no re-add do dispositivo → reboot é
  o jeito garantido de aplicar.
- **Ambos entregues e ativos**, mas **sem doc dedicado em `docs/process/`** — só existem na
  memória (`auditoria_pos_leva_20260721.md`) e nas mensagens de commit.

### DKMS patch 0002 + crash do bluetoothd (21/07 noite, dentro da sessão de validação com Sackboy)
- **Entregue e ativo, mas AINDA NÃO COMMITADO** (confirmado em `git status`: `hid-nintendo.c`,
  `BASELINE`, `README.md`, `patch/0002-HID-nintendo-register-leds-even-when-initial-set-fai.patch`
  novo, conf modprobe.d, `doctor.sh`, `launch_env.py`, `gui_dialogs.py`, `main.glade`,
  `external_controllers.py`, testes — todos com mudanças pendentes de commit).
- **O que o patch 0002 faz**: registra os LEDs de player mesmo quando o SET inicial falha
  (`register_leds_on_set_failure`), com tuning persistido (`sync_send_tries=4`,
  `input_report_wait_ms=500`, `probe_info_timeout_ms=4000`) — cura o Pro Controller que ficava
  sem LEDs e depois sem evdev quando o rádio BT congestionava (medido às 20:25:24 com o probe
  falhando `ret=-110` + `joycon_enforce_subcmd_rate: exceeded max attempts`).
- **O crash #6 do bluetoothd (22:14:34, `malloc(): unaligned fastbin chunk detected 2`)**:
  gatilho medido foi o `rmmod` do `hid_nintendo` (para trocar pelo módulo novo) desligando os 2
  controles Nintendo simultaneamente → bluetoothd entrou em loop "Host is down" reconectando os 2
  MACs → heap corrompeu. **Sequela grave**: TODOS os controles caíram; bonds do DualSense roxo e
  do Pro Controller foram DESTRUÍDOS (precisam re-pareamento); o bluetoothd renascido ficou
  "doente" (recusava dispositivos que ele mesmo listava) até o reboot.
- **Mitigação operacional já acordada** (política, não código): nunca rodar `rmmod` de driver
  HID com controles BT conectados — desconectar antes.
- **Materialização**: o mecanismo do crash está resumido (fato medido #2) na
  `2026-07-21-sprint-pesquisa-bluez-estabilidade.md`; o **playbook por controle/MAC** e a
  sequência completa de sequelas só existem na memória (`checkpoint_pos_install_crash_bt_20260721`).

### Estudo MMJ — caminhos DualSense (21/07 noite)
- **Causa-raiz confirmada**: o vpad é DualSense Edge (0x0DF2) por decisão de arquitetura
  (UHID-04); o middleware do Mullet Mad Jack (InControl) não tem NENHUM perfil para 0x0DF2 em
  nenhuma versão (nem a 1.8.10 atual) → "Unknown Device". Não é bug do hefesto nem do kernel.
- **Correção importante registrada no próprio doc**: a máscara `dualsense` FOI validada ao vivo
  em Sackboy, Mad King Redemption e Pragmata (a suspeita inicial de que "só a máscara xbox
  funciona" era baseada em falta de registro escrito, não em falha real).
- **Becos sem saída explícitos** (não repetir): tentar resolver no kernel (nenhum patch faz um
  jogo XInput-only reconhecer 0x0DF2); fazer o winebus expor PID Sony como XInput (não existe,
  lista não é configurável); remover as envs do broker "porque ele já esconde" (decisão em
  contrário, documentada — defesa em profundidade, o broker não cobre fd pré-hide nem Proton ≤9).

### Sprint (pesquisa): estabilidade do BlueZ (21/07 noite)
- **Status**: deliberadamente ABERTA — nenhuma decisão de versão tomada, por pedido explícito da
  mantenedora de decidir por pesquisa neutra (ver `feedback_bt_confiavel_sem_vies_20260721` na
  memória). O doc define perguntas de pesquisa (P1-P6) e critérios de decisão fixados ANTES dos
  resultados — não interpretar isso como trabalho incompleto, é o desenho correto do processo.

---

## 3. Lacunas de materialização (conhecimento que só existe na memória do assistente)

Itens onde o trabalho foi **entregue/decidido** mas não tem doc correspondente em
`docs/process/` — candidatos a virar doc se a mantenedora quiser esse conhecimento pesquisável
no repo em vez de só na memória do assistente:

1. **Onda L (lightbar no wake BT)** — não tem doc de desenho dedicado (as ondas S/T/W têm
   `2026-07-20-desenho-onda-*.md`; a L só aparece espalhada no checklist e na auditoria).
   Memória: `achado_lightbar_bt_borda_wake_20260720`.
2. **VPAD-09 (21/07) e TOUCHPAD-76-BT-VPAD-01** — dois incidentes pós-reboot com causa medida e
   fix commitado, mas zero doc. Risco extra: o nome "VPAD-09" já existe para OUTRO item (16/07,
   co-op com controles não-DualSense) — colisão de identificador que só quem lê a memória percebe.
   Memória: `auditoria_pos_leva_20260721`.
3. **Purga de MAC no histórico Git** (20/07 noite) — operação de segurança/privacidade de grande
   porte (724 commits reescritos, force-push em 4 branches + 37 tags) sem nenhum registro em
   `docs/process/`. Memória: `purga_mac_historico_20260720`.
4. **Crash crônico do bluetoothd — playbook operacional completo** — o mecanismo está resumido
   na sprint de pesquisa do BlueZ, mas o playbook por MAC/controle (o que fazer com cada bond
   após um crash) só está na memória. Memórias: `checkpoint_pos_install_crash_bt_20260721`,
   `achado_bluetoothd_crash_cronico_20260719`.
5. **DKMS patch 0002 (hid-nintendo) + 8BIT-03** — entregue e ATIVO no sistema, mas o código está
   **uncommitted** no repo agora; o único registro escrito é o "Adendo" dentro do estudo MMJ.
   Sem commit, esse trabalho não sobrevive a um `git stash`/reset acidental.
6. **Técnica NOPASSWD headless para instalar sem TTY** — é conhecimento operacional útil (não é
   uma leva de produto), mas também só vive na memória (`install_nopasswd_headless_20260721`);
   poderia virar uma nota em `docs/` ou `README` de desenvolvimento se for reusada com frequência.
7. **BLUEZ-UHID-01** (input BT virar uhid ≥5.73 e o filtro por identidade phys/uniq) — citado
   dentro da leva N/R/HANG/G/U mas sem doc de achado próprio; só memória
   `achado_bluez_uhid_01_20260719`.

## 4. Fios soltos (pendências em aberto, por risco)

1. **[ALTO] Trabalho de 21/07 noite não commitado** — DKMS patch 0002 + tuning + 8BIT-03 +
   diálogo enxuto + testes atualizados estão ATIVOS no sistema mas fora do git. Qualquer reset
   duro perde a mudança. (Fonte: `git status` + memória `checkpoint_pos_install_crash_bt_20260721`.)
2. **[ALTO] Bonds BT destruídos pelo crash #6** — DualSense roxo e Pro Controller precisam
   re-pareamento manual (playbook na memória, sem doc); DualSense branco e 8BitDo devem
   reconectar sozinhos. Ainda não confirmado pós-reboot no momento deste estudo.
3. **[ALTO] Decisão de versão do BlueZ em aberto** — sprint de pesquisa criada mas P1-P6 não
   respondidas; enquanto isso o sistema roda BlueZ 5.85 (1 crash conhecido) sem comparação
   rigorosa com 5.72 stock nem outras versões.
4. **[MÉDIO] L-01 (lightbar wake) — hipótese de que o gatilho nunca dispara no caso real** —
   requer instrumentação DEBUG (`lightbar_reclaim_avaliado`) e um gate humano de
   suspender/acordar antes de decidir L-02/L-03/L-04. Não mexer no código antes do dado ao vivo.
5. **[MÉDIO] W2/W3 (medição do rtw88) não executados** — `hang_reset=Y` está ativo por default
   sem a medição que o ratificaria; scripts prontos (`medir_w2_lps.sh`, `medir_w3_coex.sh`), só
   falta rodar (gate humano).
6. **[MÉDIO] Checklist de validação ao vivo (`CHECKLIST-VALIDACAO-5-ONDAS.md`) ainda sem nenhum
   item marcado** — cobre Pro Controller na GUI, gyro sem drift, trava por categoria, broker,
   numeração, rádio; pendente desde a rodada de 21/07.
7. **[MÉDIO] Diagnóstico aberto**: DualSense roxo adotado corretamente no `state_full` mas não
   aparecia na GUI (21/07 manhã) — causa não encontrada, ficou pendente de "ver a janela ao vivo".
8. **[MÉDIO] `usb 1-6` full-speed falhando enumeração no boot** (6-7× erro -71) — não é o
   DualSense nem o padrão do storm de áudio já resolvido; candidato a controle/cabo desligado,
   não investigado.
9. **[BAIXO] 7 branches antigas com MAC real ainda no origin** — bloqueadas pelo pre-push hook
   de identidade (commits do André); decisão de bypass/deletar/mailmap pendente da mantenedora.
10. **[BAIXO] Backlog LOW deferido** (U-F4..F8, S-7..S-11, DOC-1) e diagnóstico do "Modo Nativo
    por perfil é persistência assimétrica" (item B do estudo MMJ) — valor marginal, não
    esquecimento.
11. **[BAIXO] Matriz Sackboy/RDR2 por caminho (Sony direto / vpad / xbox / Steam Input) nunca
    formalizada por escrito** — testemunhada ao vivo mas sem doc tabular; o estudo MMJ já aponta
    essa lacuna explicitamente.

---

## 5. Notas de auditoria (contradições e ajustes de crença)

- A crença da mantenedora ("só BlueZ e MMJ estão materializados") reflete corretamente o que é
  **novo nesta sessão** (`??` no git status), mas subestima o volume real de documentação já
  commitada desde 15/07 — há pelo menos 27 outras entregas com doc próprio em `docs/process/`.
- O estudo MMJ (`2026-07-21-estudo-mmj-caminhos-dualsense.md`) já continha um "adendo" com um
  achado adicional relevante (crash do bluetoothd, patch 0002) que também é citado na sprint do
  BlueZ — os dois docs se referenciam parcialmente sem se citarem por nome; útil linkar
  explicitamente se algum dos dois for revisado.
- Não foi encontrada nenhuma contradição factual entre os docs commitados e a memória — a memória
  está, no geral, mais detalhada e mais atualizada que os docs (esperado, já que os docs
  capturam o "resumo materializável" e a memória guarda o processo completo).
