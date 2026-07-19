# Estudo 2026-07-18 — A guerra de escritores no hidraw e o co-op 4P misto

> Frota de 10 agentes (8 mapeadores + 2 diagnósticos ao vivo read-only) sobre a sessão real de
> gameplay de 2026-07-18 (~20h): 2 DualSense (branco USB + roxo BT), Pro Controller Nintendo USB,
> 8BitDo modo Switch BT, Sackboy via GE-Proton10-34. Retornos brutos por agente em
> `2026-07-18-frota-coop-4p/`. MACs redigidos (`<MAC-DS-BRANCO>`, `<MAC-DS-ROXO>`, `<MAC-NINTENDO>`).

## TL;DR — causas-raiz PROVADAS

**FATO 0 (causa-mãe de P1-rumble, P1-lightbar, P2 e P3):** o jogo rodou **SEM o wrapper**
`hefesto-launch`. As LaunchOptions do Sackboy só têm shader-cache; o binário existe apenas em
`~/.local/share/hefesto-dualsense4unix/bin/` (fora do PATH). O daemon materializa as envs de dedup
fielmente (`launch_env/*.env`) mas ninguém as consome. `dedup_ok: true` do state_full é
falso-tranquilizante (só checa "vpads são uhid", nunca se o jogo herdou a env).

**FATO 1 (o vazamento que a env atual NÃO cura):** o winebus dos Protons 10/11 dá hidraw à
família Sony inteira POR DEFAULT (whitelist interna) — físicos 0ce6 E vpads 0df2 (provado por
lsof: `winedevice` abriu hidraw3/6/7/8 sem env nenhuma). `SDL_GAMECONTROLLER_IGNORE_DEVICES`
só filtra o caminho SDL; o caminho winebus-hidraw ignora a env. E `PROTON_ENABLE_HIDRAW=1`
(nossa env) é herança do Proton ≤9 — nos Protons 10/11 o script nem a menciona; o binário
`winebus.sys` ainda a lê, mas ela só AMPLIA exposição. **A env moderna é `PROTON_DISABLE_HIDRAW`
com lista `0xVID/0xPID,...`** (strings UTF-16 confirmadas no winebus.sys do GE-Proton10-34;
a própria Valve usa a lista para o God of War Ragnarok no Steam Deck, com 0x0CE6 e 0x0DF2 nela).

**P1-lightbar (race verde-limãoazul no branco USB) — 2 escritores:**
- AZUL = o daemon: paleta slot 1 = (0,0,255)×0.6 = `0 0 153` via sysfs, reescrita
  INCONDICIONALMENTE por `reassert_resolved_outputs()` ao fim de TODO `connect()` — e o
  `reconnect_loop` roda connect() a cada 30s (mtime do nó sysfs avançando a cada 30s exatos,
  provado ao vivo).
- VERDE-LIMÃO = o jogo (winedevice, hidraw3 aberto via whitelist default do winebus): o jogo
  enxerga o físico como controle EXTRA (o "player 3/4" do P2) e pinta a cor PS de player 3
  (verde). Escrita hidraw crua NÃO atualiza a classe LED do kernel — por isso o sysfs lia azul
  com a barra fisicamente verde (prova cabal da escrita fora-de-banda).
- No roxo BT a MESMA race existe mas é invisível: daemon diz slot 2 = vermelho E o jogo diz
  player 2 = vermelho. Colisão de cores esconde a briga.

**P1-rumble (branco USB não vibra; roxo BT vibra):**
- O jogo quase não usa o vpad (`rumble_ff.plays=19` na sessão inteira) — manda FF DIRETO no
  hidraw3 do físico.
- O report_thread da pydualsense reescreve report 0x02 com motores=0 e flags de vibração
  SEMPRE ligados (`flag0=0xFF`) na mudança de estado E no keepalive de 0.5s → todo rumble que o
  jogo escreve no branco é ZERADO em ≤0.5s. Mesma física do bug curado no Modo Nativo pelo
  output-mute — que aqui não está armado.
- O roxo BT vibra por um BUG PROTETOR: o report BT 0x31 da pydualsense 0.7.5 é MALFORMADO
  (off-by-one: `[1]=0x02` fixo em vez de seq<<4, `[2]=0xFF` em vez do tag obrigatório 0x10) —
  o firmware o DESCARTA, então nosso keepalive é no-op por BT e o rumble do jogo sobrevive.
  Corolário grave: **nosso caminho legítimo de rumble vpad→físico BT também é no-op** — se o
  dedup passar a funcionar sem consertar o report BT, o roxo PARA de vibrar.

**P3 (8BitDo LED 2, jogo player 1):** 4 domínios de numeração independentes, zero acoplamento
(identity registry dos DualSense / player_index do co-op / slot dos externos = ds_count+índice
por event-node recalculado A CADA poll de 4s da GUI / ordem SDL-winebus do jogo). Ao vivo o LED
do 8BitDo já tinha mudado sozinho para player 4.

**P3-BÔNUS — BUG NOVO GRAVE achado ao vivo:** `_external_inventory` ESCREVE os LEDs como efeito
colateral de toda leitura `controller.list{external:true}`, e a GUI polla a cada 4s sem comparar
estado → bombardeio de subcomandos BT no firmware clone → `joycon_enforce_subcmd_rate: exceeded
max attempts` em loop no dmesg a partir de 20:23 → **o hid-nintendo DESREGISTROU o 8BitDo**
(a "morte por BT" que atribuíamos só ao kernel é AGRAVADA por nós: leitura com efeito de escrita).

**P4 (dropdown de modo na ficha):** nunca existiu — 9532eb1 entregou detecção read-only + texto
("O jogo vê como: Nintendo (modo Switch)"); o design 8BIT-02 veta dropdowns (bug de foco do
cosmic-comp) e o modo é troca de HARDWARE (combo no controle). Gap real é de UX: o texto não
parece um "seletor". Solução conforme o design da casa: botões segmentados read-only.

**P5 (diálogo do wrapper claro):** `_build_wrapper_dialog` cria `Gtk.MessageDialog` SEM
`add_class("hefesto-dualsense4unix-window")` — todo o CSS Drácula é escopado a essa classe.
Sob XWayland (GDK_BACKEND=x11 forçado por causa do cosmic-epoch#2497) o XSettings aponta
gtk-theme Yaru, que NEM ESTÁ INSTALADO → Adwaita claro. Fix de 1 linha com precedente idêntico
em `gui_dialogs.py:248-249`.

**P6 (Motion Sensors viram js2/js4/js6/js8):** joydev do kernel cria jsN para os nós de
acelerômetro (e cada vpad DOBRA o ruído). SDL2 já os ignora (`ID_INPUT_ACCELEROMETER=1`, sem
`ID_INPUT_JOYSTICK`); polui só a API js legada. Cura: regra udev `js*` com pai `*Motion Sensors*`
→ MODE 0000.

## Achados colaterais (não relatados pela usuária)

1. `policy=max` aplica `mult=0.7` (deveria ser 1.0) — rumble do jogo atenuado indevidamente.
2. Autoswitch trata a PRÓPRIA GUI (wm_class `Main.py`/`Hefesto-Dualsense4Unix`) como janela →
   flapping vitoriasackboy_nativo a cada troca de foco.
3. Toggle manual de emulação na GUI recriou os vpads MID-GAME (20:15) → handles do jogo
   invalidados (Steam nunca reabriu o hidraw6).
4. `evdev_read_lost EBADF` no teardown do co-op (fd fechado antes do join da thread).
5. Regra 70 não cobre o hidraw do vpad uhid — o acesso do jogo ao vpad depende do pacote
   steam-devices (terceiro). Portabilidade: acrescentar match `0003:054C:0DF2.*`.
6. TAG uaccess das regras 77/79 é morto (>73); funcionam via chmod 0666 — lightbar sysfs
   world-writable (qualquer processo pode escrever).
7. hidraw0/1/4/5 em 0666 = `60-openrgb.rules` do Aurora (terceiro), não nosso.
8. `rumble_ff.plays` é agregado — sem split por vpad no state_full (telemetria cega).
9. Assets 73/74 mortos no repo (install os remove desde 2026-06-23).
10. CI roda só `tests/unit` — `tests/core/test_sysfs_leds.py` (rota sysfs de LED!) só roda no
    gate local `pytest tests/` (3136/0/0 hoje). Faixa cega headless de ~120-140 testes de GUI.

## Decisões arquiteturais da onda (2026-07-18)

1. **Fim da guerra**: `compose_env` passa a emitir `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6`
   (só físicos; vpad 0df2 continua com hidraw pleno pela whitelist default) + manter o IGNORE do
   SDL; aposentar `PROTON_ENABLE_HIDRAW=1`. Allowlist do wrapper e do launch_env atualizada.
2. **Keepalive neutro**: report de output do daemon só liga os bits de vibração do flag0 quando
   há rumble NOSSO ativo (ou transição ativa→0); keepalive idle vira neutro e para de zerar
   rumble de terceiros — em USB e BT, qualquer cenário.
3. **Report BT consertado**: corrigir o layout 0x31 no override `_PinnedPyDualSense`
   (seq<<4, tag 0x10, CRC já dominado em `lightbar_reset.py`) — rumble/triggers/lightbar do
   daemon passam a funcionar de verdade por BT.
4. **Replicação completa do output do jogo** vpad→físico: rumble (já existe) + gatilhos
   adaptativos + lightbar + player-LEDs, com política "jogo vence enquanto a sessão uhid está
   aberta; reassert da paleta no CLOSE". Player-LED replicado = a numeração dos DualSense passa
   a ser A DO JOGO (cura P3 para DualSense por construção).
5. **Externos com identidade**: registry persistente por uniq (como os DualSense), numeração e
   LED movidos para tick do DAEMON com escrita só-em-mudança + rate-limit (cura a morte do
   8BitDo e o LED instável); leitura IPC vira pura.
6. **Reassert com cache**: `SysfsLedNode.set_rgb` ganha cache de último valor escrito — o flash
   azul de 30s morre; nó recriado (wake BT) escreve de novo naturalmente.
7. **Honestidade do dedup**: `hefesto-launch` grava marker de execução; daemon compara com a
   janela steam_app detectada e expõe `wrapper_used` no state_full; GUI mostra aviso quando o
   jogo roda sem wrapper.
8. **GUI**: diálogo do wrapper (e demais toplevels) com a classe de tema; ficha do externo ganha
   segmented read-only do modo detectado.
9. **Kernel/udev**: regra 70 cobre vpad; nova regra js-Motion MODE 0000; 78 ampliada (nomes BT e
   vpad); assets 73/74 removidos do repo; `hefesto-launch` symlink no PATH.
10. **Fica para outra onda** (materializado em sprint futura): broker root para esconder hidraw
    do físico sem env (cura P2 plug-direto na raiz), IMU/touchpad reais no vpad (DEDUP-02),
    2ª causa RDR2 (BT-07).

## Riscos mapeados

- Consertar o report BT sem o keepalive neutro mataria o rumble BT direto-do-jogo (cenário
  sem-wrapper). ORDEM OBRIGATÓRIA: keepalive neutro JUNTO ou ANTES do fix BT.
- Replicação de lightbar do jogo × paleta por slot: política de posse clara (sessão de jogo
  vence; paleta volta no CLOSE) para não recriar a race internamente.
- Protons ≤9 (sem PROTON_DISABLE_HIDRAW): continuam com o vazamento winebus — documentar;
  GE-Proton10+/Valve 10+ cobrem a máquina de referência.
- Testes novos de GUI: seguir o padrão `_install_gi_stubs` (GATE-SKIP-MASK-01); nunca
  `import gi` no topo (armadilha dos 4 rounds do release 3.14.0).
