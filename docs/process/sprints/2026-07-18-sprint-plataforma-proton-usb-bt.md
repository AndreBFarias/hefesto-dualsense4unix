# Sprint PLATAFORMA 2026-07-18 — Proton pinado · USB sem economia · BT máximo · Game Mode

> MATERIALIZADA em 2026-07-18 a pedido da mantenedora; EXECUTAR SOMENTE após o fechamento da
> onda "fim da guerra" (núcleo+externos+GUI+infra). Motivação: a v1 de produção não pode
> depender de versão de Proton do dia (a semântica winebus MUDOU entre Proton 9→10:
> PROTON_ENABLE_HIDRAW morreu — provado no estudo 2026-07-18), nem de power-saving agressivo
> de fabricante (System76/COSMIC economiza onde pode), nem do acaso do BT.
> Baseline da máquina de referência HOJE (2026-07-18 ~22h, coletado ao vivo): 0 erros -71 no
> boot; quirk snd_usb_audio ativo (0ce6+0df2); usbcore.autosuspend=-1 (Aurora); TODOS os
> devices USB power/control=on; btusb.enable_autosuspend=Y (furo: neutralizado só pelo global
> da Aurora); system76-power = Performance. As portas USB "abandonadas" nunca tiveram defeito
> (storm era config de áudio) — liberadas para uso.

## PLAT-01 — Proton PINADO pelo install (reprodutibilidade acima de tudo)

Objetivo: o hefesto valida UMA versão exata de Proton (candidata: GE-Proton10-34 — a validada
a nível de binário no estudo 2026-07-18) e o install a instala e TRAVA, imunizando o setup
contra upgrades que mudem semântica (o caso PROTON_ENABLE→DISABLE_HIDRAW nunca mais).
1. `assets/proton-pin.conf` (fonte da verdade): nome, URL do release GitHub, SHA256 do tarball.
2. Passo do install (DEFAULT, opt-out `--no-proton-pin`; regra install-SEM-FLAGS mantida):
   - Se `~/.steam/steam/compatibilitytools.d/<versão-pinada>/` já existe e o checksum do
     manifest bate → nada a fazer (offline-first; memória: "offline antes de online").
   - Senão baixa (curl com resume), VERIFICA SHA256 (falhou = aborta o passo, nunca instala
     binário não verificado), extrai em compatibilitytools.d.
   - Cache do tarball em `~/.cache/hefesto-dualsense4unix/` para reinstalls offline.
3. Travamento por jogo (com a Steam FECHADA, mesmo gate do apply_wrapper_to_all_games):
   `CompatToolMapping` no `~/.steam/steam/config/config.vdf` — default global (`"0"`) apontando
   para a versão pinada + entradas por appid dos jogos instalados. Backup do config.vdf antes
   (padrão do disable_steam_input). Botão na GUI (aba Sistema): "Travar Proton validado".
4. Doctor: reporta versão pinada presente/ausente, jogos fora do pin, e AVISA se algum jogo
   usa Proton ≤9 (sem PROTON_DISABLE_HIDRAW → vazamento winebus volta).
5. Uninstall simétrico: desfaz o CompatToolMapping que NÓS escrevemos (marcador próprio no
   vdf ou lista em estado local); o tarball extraído fica (dado do usuário; documentar).
6. Upgrade DELIBERADO: trocar a versão = editar proton-pin.conf + rodar install — nunca
   automático.

## PLAT-02 — Independência de Proton: broker root hide-hidraw (a "solução udev global")

Promovida de FUT-01 para execução na próxima onda. É a cura que funciona com QUALQUER
Proton/loader (env nenhuma): se o processo do jogo não consegue ABRIR o hidraw do físico,
não há vazamento — em nenhum backend (SDL, winebus-hidraw, libScePad, HIDAPI).
Desenho (detalhes em 2026-07-18-sprint-futuro-broker-imu-rdr2.md §FUT-01):
- Unit system root hardened (`hefesto-hidraw-broker.service` + socket) com API mínima
  hide/restore validada por sysfs (SÓ nós filhos de DualSense físico 054c:0ce6).
- Daemon pede hide ao adotar físico com vpad vivo; restore no teardown/Modo Nativo/exit
  (inclusive trap de crash: broker restaura tudo se o daemon sumir do socket — fail-safe
  "duplicado > zero controles" preservado).
- Install SEM FLAGS: instala unit+socket+polkit-free (socket com SO_PEERCRED restrito ao uid
  da sessão); uninstall simétrico.
- Com o broker ativo, PROTON_DISABLE_HIDRAW/IGNORE viram defesa em profundidade, não a cura.

## PLAT-03 — USB sem economia de energia (o hefesto é dono da cura, não herdeiro)

> DECISÃO DA MANTENEDORA (2026-07-18, noite): TUDO desta sprint entra no install por DEFAULT
> SEM FLAG. O hefesto INCORPORA as curas hoje providas pela Aurora como defaults próprios
> (detectando e NÃO duplicando quando já aplicadas — atribuição preservada nos cabeçalhos) e
> VAI ALÉM a nível de kernel. Instalação em máquina virgem tem que ficar completa sozinha.

1. Nova regra udev NOSSA (ex.: `81-hefesto-usb-power.rules`): `power/control=on` +
   `autosuspend_delay_ms=-1` para: Sony 054c (controles), Nintendo 057e, 8BitDo 2dc8,
   Microsoft 045e (controles), e ADAPTADORES BT (classe e0/01/01 — cobre o TP-Link 2357:0604).
2. **Cmdline de kernel GERENCIADO pelo install** (Pop!_OS: via `kernelstub`; fallback GRUB):
   garantir `usbcore.autosuspend=-1` e `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`.
   Idempotente: se já presente (Aurora ou manual), NÃO duplica e REGISTRA "já provido por
   terceiro" no estado local; se ausente, adiciona e registra "nosso" — o uninstall remove SÓ
   o que registramos como nosso. Cabeçalho/registro deixa claro quem é o dono de cada param.
3. **Runtime PM dos HOSTS USB (nível além da Aurora)**: regra udev/tmpfiles para
   `power/control=on` nos controladores xHCI PCI (classe 0x0c0330) — a economia no HOST
   derruba o barramento inteiro, não só o device (o storm -71 de maio derrubava teclado+mouse
   juntos: era o barramento). Cobrir também `pcie_aspm` via doctor (reportar policy ativa;
   mudar policy é decisão do dono — instruir).
4. **Caça a sabotadores**: doctor detecta TLP/powertop/tuned com autosuspend USB agressivo
   (são os que religam economia por cima do udev) e alerta com instrução de exceção.
5. Doctor: seção "Energia USB" — autosuspend global, power/control de controles E hosts,
   contagem de -71 do boot (storm.log), e o aviso didático "todas as portas são utilizáveis;
   o storm era config de áudio, não hardware" (a família vai ler).
6. Testes: regras sintáticas + doctor com sysfs fake + kernelstub mockado (nunca rodar o real
   nos testes).

## PLAT-04 — Bluetooth no máximo (sem restrição/limitação)

1. `assets/modprobe.d/hefesto-btusb-no-autosuspend.conf`: `options btusb enable_autosuspend=0`
   (default no install; runtime via sysfs quando possível para valer sem reboot). Cura o furo
   `btusb.enable_autosuspend=Y` visto ao vivo.
2. Regra udev power/control=on do adaptador BT (já na PLAT-03 item 1).
3. INVESTIGAÇÃO (agente, na execução): tuning do BlueZ para gamepads — main.conf
   (ex.: `FastConnectable`, parâmetros de link supervision/latency), coexistência 2.4G
   (2 receivers Compx no ar!), e o CLONE DS4 054C:05C4 que stormou o adaptador com 211k CRC
   fails (estudo 18/07): doctor passa a DETECTAR o clone pareado e recomendar despareá-lo
   (ele degrada o rádio para TODOS). Entregável: relatório + o que for seguro como default.
4. Meta honesta: o muro do hid-nintendo BT (8BitDo/Pro Controller) é do kernel — o que nos
   cabe é não agravar (EXT-04 já cura o bombardeio de LED) e manter o rádio saudável.
   O 8BitDo está NO CABO desde 2026-07-18 ~22h (decisão da mantenedora após a queda) — no cabo
   ele é um segundo "Pro Controller" USB 057e:2009; validações devem considerar isso.

## PLAT-05 — Game Mode COSMIC (aproveitar o máximo do sistema)

1. Wrapper hefesto-launch (fase pós-env): pedir Performance ao system76-power via D-Bus no
   launch do jogo e RESTAURAR o perfil anterior no exit (best-effort, timeout curto, nunca
   bloqueia o jogo — fail-safe absoluto). Na máquina de referência já vive em Performance;
   vale para a v1 (notebooks System76 economizam por default).
2. Doctor: seção "Sistema pronto pra jogar" — perfil de energia, compositor (COSMIC XWayland
   quirks conhecidos), GPU (NVIDIA PRIME/offload se aplicável), memória do detector de janela
   degradado no cosmic-comp.
3. NÃO assumir controle permanente de energia do sistema (só durante jogo, com restauração) —
   atribuição Aurora/dono respeitada.

## PLAT-06 — Kernel hardening próprio (além do que a Aurora provê)

Frente de investigação+implementação (agentes na execução), tudo default sem flag:
1. **modprobe.d consolidado do hefesto**: snd_usb_audio (já temos), btusb enable_autosuspend=0
   (PLAT-04), e avaliar parâmetros do hid_playstation/usbhid relevantes a estabilidade
   (ex.: quirks usbhid para clones problemáticos detectados).
2. **Coexistência 2.4GHz**: 2 receivers Compx + BT no mesmo espectro — investigar se o
   posicionamento de barramento/hub interfere (relatório, não automação).
3. **Latência de input**: avaliar `usbhid.jspoll`/taxa de poll dos controles USB (DualSense já
   é 250Hz+; medir antes de mexer) — só aplicar se medição provar ganho sem custo.
4. **Watchdog do ecossistema**: o storm-watch existente vira "kernel-watch" — além do -71,
   monitora joycon_enforce_subcmd_rate (o assassino do 8BitDo BT), CRC fails de BT (o clone
   DS4), e resets de xHCI; journal dedicado + doctor lê e resume pro leigo.
5. Regra permanente: cada item novo entra no install DEFAULT + uninstall simétrico + doctor
   verificando + teste; NADA atrás de flag (flags só para opt-OUT documentado).

## Gate de aceite da sprint (quando executada)
- Suíte completa 0 skipped + ruff + mypy + anonimato; install SEM FLAGS idempotente.
- Máquina de referência: `btusb enable_autosuspend=0` ativo; doctor "Energia USB" verde;
  clone DS4 detectado (se pareado) com aviso; Proton pinado presente e jogos travados nele;
  broker: jogo lançado SEM wrapper com vpad ativo NÃO enxerga o físico (lsof prova).
