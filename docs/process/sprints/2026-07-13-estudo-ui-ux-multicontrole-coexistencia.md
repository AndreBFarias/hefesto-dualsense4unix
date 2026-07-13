# Estudo 2026-07-13 — UI/UX, multi-controle 4P, coexistência de features e sincronização

Status: APROVADO PELA MANTENEDORA (2026-07-13, decisões de UI/UX delegadas) —
W1+W2+W3 ENTREGUES; W4 núcleo ENTREGUE; W5 parcial. Working tree NÃO commitado.

## 0. Status de entrega (2026-07-13, mesma sessão)

- W1 ENTREGUE: identidade por MAC (`discover_dualsense_evdevs`, `EvdevReader.retarget`/
  `target_uniq`, `primary_uniq` no backend, coop keyed por MAC com respawn em troca de
  node), grab VERIFICADO (`set_grab` retorna bool, `grab_state` off/pending/held/failed,
  coop não cria vpad sem grab e derruba/recria em falha), regra udev 78 (Motion Sensors
  deixam de enumerar como joystick — APLICADA e verificada ao vivo:
  `ID_INPUT_ACCELEROMETER=1`, sem `ID_INPUT_JOYSTICK`), paridade nos 3 instaladores +
  uninstall. Testes novos em test_subsystem_coop.py (3º controle, path stale, node
  change, grab refused/degraded).
- W2 ENTREGUE: `InputDirWatch` (listdir ~µs em vez de enumeração de ~10-40ms por tick de
  2s no event loop — coop.sync e is_stale gateados), delta-check no `forward_analog`
  (zero writes com stick parado), `os.nice(5)` (env HEFESTO_DUALSENSE4UNIX_NICE),
  throttle adaptativo por nº de controles (base×N, cap 32ms) + write OUT com dirty-flag
  e keepalive 0.5s (report idêntico não vai mais ao barramento ~100Hz). Bench formal
  antes/depois com jogo fica para a validação de gameplay.
- W3 ENTREGUE: seção `mode` no perfil (desktop/gamepad+flavor+coop/native), applier
  `Daemon.apply_profile_mode` (lock manual 30s, origem rastreada, perfil-sem-opinião
  reverte só modo-de-perfil, desktop explícito limpa tudo), autoswitch NÃO congela com
  nativo-de-perfil (origem no store), presets `sackboy_nativo` + `coop_local`
  (instalados), `native_mode_origin`/`mode_from_profile`/`primary_grab_state` no
  state_full. Autoswitch NÃO estava quebrado: detecta janelas XWayland (jogos Proton);
  `unknown` só em foco Wayland-nativo (limitação COSMIC conhecida).
- W4 NÚCLEO ENTREGUE (validado ao vivo por screenshot): aba INÍCIO nova (primeira) com
  comutador Desktop/Jogo(gamepad)/Jogo nativo + co-op + máscara + cards por controle
  (P1/P2, primário, aviso de grab) + botão "Desligar Hefesto (voltar ao Linux puro)"
  que NÃO religa ao reabrir a GUI (`_user_stopped_daemon`; "Iniciar" desarma) +
  glossário dos 4 conceitos de parar. Perfis: linha do ATIVO em negrito. Emulação:
  cartão UINPUT reflete a máscara REAL (era hardcoded Xbox) e o label do modo jogo
  parou de dizer "ativo" quando desligado (BUG-GAMEMODE-LABEL-AMBIGUO-01). Status:
  bateria com texto e "(Controle 1)" com 2+; tooltip órfão dos glyphs eliminado.
  Gatilhos: grade compacta (3 colunas, botões menores).
- W5 PARCIAL: install/uninstall/deb com a regra 78 (feito); gate completo VERDE (1852
  passed, ruff, mypy, anonimato, acentuação das linhas tocadas); daemon+GUI da máquina
  recarregados com o código novo (journal: `coop_player_added identity=<mac> players=2`,
  `gamepad_controller_grab ok=True`).

SESSÃO 2 (2026-07-13, noite) — validação + entregas:
- BUG-HOME-SEGMENTED-SIGNATURE-01 (CORRIGIDO): os handlers do comutador de modo e da
  máscara da aba Início pediam 2 argumentos, mas o sinal "changed" do SegmentedSelector
  é SEM argumentos → TypeError engolido pelo PyGObject → os botões mudavam de visual
  sem NUNCA disparar o IPC (era o "problemas nos botões" relatado). Fix: handler
  `(self, selector)` + `get_active_id()`; regressão em
  tests/unit/test_home_actions_handlers.py. REGRA para o futuro: todo handler de
  SegmentedSelector segue o contrato do GtkComboBox::changed (sem args).
- "3º controle não aparece": diagnóstico ao vivo — o 3º controle conectado é um
  Nintendo Switch Pro Controller (057e:2009, js0), não um DualSense; daemon/GUI
  mostrando 2 é correto. Decisão de produto em aberto: card "detectado, não gerenciado"
  para controles não-DualSense.
- Applet COSMIC ENTREGUE: seção "Modo do sistema" (Desktop/Jogo/Jogo nativo, radio),
  toggle co-op com nº de jogadores, máscara DualSense/Xbox, linha de modo no status
  ("(pelo perfil)" quando origem profile); ipc.rs parseia native_mode/coop/
  gamepad_emulation + 3 setters novos; build release + cargo test (9) + clippy verdes.
- Seletor de `mode` no editor de Perfis ENTREGUE: seção "Modo" (Sem opinião/Desktop/
  Jogo/Jogo nativo + co-op + máscara, só SegmentedSelector), carrega/salva/round-trip;
  tests/unit/test_profiles_editor_mode.py (14 testes).
- rumble_policy persistida no perfil ENTREGUE (FEAT-RUMBLE-POLICY-PROFILE-01):
  RumbleConfig.policy/custom_mult no schema (aditivo), rumble_policy_applier no
  ProfileManager, Daemon.apply_profile_rumble_policy (lock manual 30s, reversão ao
  estado pré-perfil, adoção, gesto manual carimbado nos handlers IPC), draft grava e
  persiste a política; tests/unit/test_profile_rumble_policy.py (17 testes).
- Gate do conjunto: 1890+ passed, ruff, mypy strict, anonimato.

SESSÃO 2b (2026-07-13, noite) — hardening multi-controle (6 frentes, 4 agentes):
- FEAT-BACKEND-HOTPLUG-FAST-01: reconnect_loop online agora consulta InputDirWatch a
  cada 2s (listdir ~µs) e dispara controller.connect() via executor SÓ quando
  /dev/input mudou; fallback de 30s mantido. Controle novo entra no backend em ~2s.
- FEAT-STATE-PER-CONTROLLER-01: describe_controllers ganhou `uniq` (MAC) e
  `battery_pct` por controle (sem I/O HID extra); cards da Início mostram
  "USB · primário · 87%" + "…c311f0".
- FEAT-COOP-PLAYER-LED-01: com co-op ativo, cada controle mostra o padrão canônico do
  seu jogador (P1..P4, sysfs por MAC, best-effort, reversão ao padrão do perfil ao
  desligar); presets Player 3/Player 4 na aba Lightbar (glade + handlers).
- BUG-COOP-GRAB-PENDING-VPAD-01: vpad de secundário SÓ nasce com grab_state=="held"
  (player pendente é promovido pelo forward_all/sync; pending→failed nunca cria vpad).
  Zero janela de input dobrado no hotplug.
- FIX-PACKAGING-SEED-PARITY-01: semeadura runtime dos presets (loader.py, copy-if-
  absent + marker compartilhado com install_profiles.sh, fontes repo→/usr/share —
  cobre .deb/AppImage), paridade de regras udev no check_packaging_parity.sh (todas as
  9, incl. a 78), texto do install.sh derivado dos assets, Icon= do .desktop do applet
  corrigido (era hefesto-dualsense4unix, ícones são com.vitoriamaria.*).
- FEAT-WINDOW-DETECT-DIAG-01: detector de janela com diagnóstico de primeira classe —
  backend ativo/saúde/última wm_class útil no store E no state_full
  (window_detect_backend/healthy/last_class — dá para capturar o wm_class do Sackboy
  por IPC, sem journal), seção nova no doctor.sh com veredito OK/DEGRADADO/CEGO
  (validado ao vivo: COSMIC = DEGRADADO, só XWayland — wlrctl não funciona porque o
  cosmic-comp não expõe wlr-foreign-toplevel; suporte nativo futuro =
  zcosmic_toplevel_info_v1 via pywayland ou helper Rust/cosmic-client-toolkit).

PENDENTE (próximas sessões): chip de alvo nas abas de output; draft de lightbar/LEDs
nascendo do estado vivo; fusão Emulação+Mouse+Teclado numa aba "Entrada" (W4.2);
wm_class real do Sackboy (abrir o jogo e ler window_detect_last_class por IPC, ajustar
o preset); validação de gameplay 2P/3P/4P + bench py-spy antes/depois; card
"detectado, não gerenciado" p/ controles não-DualSense (ex.: Switch Pro Controller);
cliente zcosmic_toplevel_info_v1 p/ detecção em Wayland nativo no COSMIC;
FEAT-HIDE-PHYSICAL-01 (esconder também os nodes físicos grabados via flag+path-unit —
fase B do HidHide).
Método: leitura dirigida do código (file:line), 2 varreduras independentes (runtime e UX),
inspeção AO VIVO da GUI com 2 DualSense USB conectados + co-op ligado (screenshots
2026-07-13 16:56–16:58), inventário de /proc/bus/input/devices e `daemon.state_full` por IPC.

## 1. Pedido da mantenedora (2026-07-13)

1. Co-op local hoje "trava" em 2 players; meta: até 4 players locais funcionando.
2. Com 2 controles no daemon, o JOGO sofre throttling/stutter (GPU quase ociosa) — input funciona.
3. Ao conectar um 3º controle, ele "duplica": dois inputs saem como um único controle. Inutiliza.
4. Interface confusa/não otimizada; falta botão de "desligar de verdade e voltar ao estado
   normal"; as soluções deveriam morar no PERFIL.
5. Sackboy (exclusivo Sony) deveria usar por default as features nativas do DualSense — hoje não dá.
6. Conflitos com o sistema (System76/COSMIC), features que não coexistem ligadas, perfis
   dessincronizados de GUI/applet/run/install. Autorizada linguagem de baixo nível se preciso.

## 2. Diagnóstico dos problemas relatados

### 2.1 Co-op "limitado a 2 players" — NÃO há cap no código; o limite é o bug 2.2

`CoopManager.sync()` (`daemon/subsystems/coop.py:84`) cria um jogador secundário para CADA
evdev físico além do primário — 4 controles produziriam P1+P2+P3+P4 sem mudança de código.
O "bloqueio a 2" observado é consequência do colapso de identidade ao entrar o 3º (2.2).
Escalar a 4P exige: consertar identidade (2.2), custo por-controle (2.3) e expor co-op na GUI.

### 2.2 Duplicação do 3º controle — três causas-raiz combinadas

Sintoma: o jogo passa a receber dois inputs espelhados "como um único controle".

(a) TRÊS identidades divergentes para "quem é o primário/quem é quem":
  - Backend elege primário pela ordem de inserção no dict de handles hidapi
    (`backend_pydualsense.py:448` — `next(iter(self._handles))`, key = serial/MAC).
  - O `EvdevReader` do primário localiza device por MENOR NÚMERO de node
    (`evdev_reader.py:106-113` — `find_dualsense_evdev` = primeiro da lista ordenada).
  - O coop identifica jogadores por PATH do node (`coop.py:61` — `_players: dict[str(path)]`)
    e exclui "o primário" lendo `controller._evdev._device_path` (`coop.py:77-80`).
  Qualquer re-enumeração (hotplug do 3º, storm -71, replug) faz essas três visões divergirem:
  o coop pode criar um vpad para o node que o P1 já forwarda → dois vpads espelhando o mesmo
  controle físico. Evidência ao vivo: journal de hoje mostra o evdev primário migrando de
  `event21` para `event25` em 10 s (15:27:58 → 15:28:08).

(b) Grab EVIOCGRAB é best-effort e SILENCIOSO: `set_grab` engole qualquer exceção
    (`evdev_reader.py:326-341`, `contextlib.suppress`) e a reaplicação na reconexão idem
    (`evdev_reader.py:250-252`). Se o grab falha (EBUSY porque outro reader já graba aquele
    node), o jogador é criado MESMO ASSIM → o jogo vê o físico CRU + o vpad = input dobrado.
    Nenhum log/aviso/recusa.

(c) Mesmo com grab OK, os devices físicos NÃO são escondidos dos jogos. Inventário ao vivo
    com 2 controles + co-op (11 devices / 6 joysticks):

    | node | o que é | visível p/ jogo? |
    |---|---|---|
    | event21/js0 | DualSense físico 1 (grabado) | sim — "joystick morto" |
    | event22/js1 | Motion Sensors do 1 | sim — jorra eventos de acelerômetro |
    | event23/mouse2 | Touchpad do 1 (vira MOUSE do sistema) | sim |
    | event25/js2, event26/js3, event27/mouse3 | idem controle 2 | sim |
    | event257/js4 | vpad virtual P1 | sim (o único correto p/ P1) |
    | event259/js5 | vpad virtual P2 (coop) | sim (correto p/ P2) |

    O jogo enumera 6 "joysticks": 2 mortos (físicos grabados), 2 acelerômetros e 2 corretos.
    Seleção de controle no jogo vira loteria; com 3 controles seriam 9. O spec original W6.3
    previa "esconder HID real (HidHide-equivalente, udev trick)"; a decisão V1-2.5 adiou para
    uma "W9 exploratória" que nunca aconteceu. É a dívida-raiz do multi-controle.

### 2.3 Throttling do jogo com 2 controles — ranking de causas (GPU ociosa = starvation de CPU)

Números da varredura de runtime (file:line no relatório interno):

1. GIL + 1 core saturado, dobra de 1→2 controles: cada controle adiciona 1 thread
   `EvdevReader.read_loop` processando ~1000-1500 eventos/s em Python sob RLock durante jogo
   + 1 `report_thread` pydualsense (~80-100 Hz de parse/monta report em Python, write HID OUT
   incondicional). Tudo serializado pelo GIL, sem `nice` (o daemon disputa CPU com o jogo em
   SCHED_OTHER). Com 1 controle não satura; com 2 passa do joelho. Projeção 4 controles: ~2×.
2. Hitch rítmico de ~10-40 ms A CADA 2 s NO EVENT LOOP: `coop.sync()` roda inline e re-enumera
   /dev/input inteiro (`find_all_dualsense_evdevs` abre/consulta/fecha ~15-30 nodes)
   (`lifecycle.py:1246-1248` + `evdev_reader.py:84-103`); em paralelo o watchdog `heal` faz
   OUTRA varredura via executor no mesmo período. Bloqueia o forward dos vpads → micro-stutter
   de input periódico. Só existe com co-op (2+).
3. Contenção USB: 2 report_threads escrevendo OUT ~80-100 Hz cada (write incondicional mesmo
   sem mudança — `pydualsense.py:502`) + 2 conjuntos de interfaces de ÁUDIO USB no mesmo host
   controller (família do storm -71; o throttle de 8 ms já mitigou o CRC-fail, mas a pressão
   continua).
4. Writes uinput sem coalescing: `forward_analog` emite 6 EV_ABS + SYN SEMPRE, por vpad, por
   tick (`uinput_gamepad.py:203-212`) ≈ 960 writes/s com 2 vpads, inline no event loop. E os
   sticks TREMEM em repouso (ao vivo: X:125→126, Y:122→125) → eventos reais entregues ao jogo
   continuamente, inclusive dos Motion Sensors expostos (2.2c) que o jogo drena sem querer.
5. Dispatch todo inline no event loop (gamepad P1 + coop + mouse/teclado/hotkey); só
   read_state/heal/connect usam o executor de 2 workers. `hid_enumerate` (~dezenas de ms) roda
   a cada 30 s no reconnect_loop — hitch secundário.

Não-causas verificadas: GUI aberta (state_full lê cache em memória), rumble reassert
(atribuições em memória), re-enumeração de áudio em runtime (não existe).

### 2.4 "Botão de desligar de verdade" — o Modo Nativo não tem superfície gráfica

- `native.mode.set` existe no IPC e na CLI (`native on|off|status`) — mas NÃO há botão na GUI
  nem no applet (adiado por spec em FEAT-NATIVE-MODE-01 "Fora de escopo V3.12+"). A feature
  que resolve a dor número 1 dela está invisível.
- A GUI tem QUATRO conceitos de "parar" sem glossário: Parar daemon (aba Daemon), Modo jogo
  (suppress, aba Emulação), pause (nem exposto), Modo Nativo (só CLI). "Parar" + reabrir a GUI
  religa o daemon (`ensure_daemon_running` em `app.py:745`) sem avisar.
- O applet tem "Sair (desligar Hefesto)"; a GUI não tem equivalente com esse nome.

### 2.5 Sackboy com features nativas por default — dois bloqueios

(a) O schema de perfil NÃO tem seção de MODO: só `mouse` e `suppress_desktop_emulation`
    (`profiles/schema.py:172-223`). Não existe "este jogo → Modo Nativo" nem "este jogo →
    gamepad virtual/coop". Perfil não consegue expressar o que ela quer.
(b) O autoswitch está CEGO no serviço systemd DESTA máquina: journal de hoje mostra
    `profile_autoswitch from_=None to=vitoria wm_class=unknown wm_name=` — a detecção de
    janela retorna unknown (backend Xlib/cascade falhando no contexto do serviço), então
    NENHUM perfil por jogo casa; tudo cai no de maior prioridade com match any ("vitoria").
    Enquanto isso não for corrigido, perfil-por-jogo é letra morta — inclusive point_and_click.

### 2.6 Conflitos de features e dessincronias (estado vivo capturado hoje)

- Exclusões mútuas atuais: gamepad desliga mouse; mouse desliga gamepad; Modo Nativo desliga
  ambos; suppress desliga mouse/teclado; coop exige gamepad. A usuária quer COEXISTÊNCIA —
  a semântica correta é "por perfil/por contexto" (o perfil do jogo decide o modo), não
  toggles globais que se atropelam.
- Dessincronias flagradas ao vivo na GUI:
  - Aba Emulação: cartão UINPUT diz "Microsoft X-Box 360 pad / 045E:028E" com o gamepad real
    em flavor dualsense (info stale/errada); "Modo jogo: ativo" com `emulation_suppressed:
    false` no daemon.
  - Lightbar: prévia verde e LEDs 1-5 desmarcados ≠ estado real dos controles (draft nasce de
    default, não do estado vivo).
  - Perfis: a lista NÃO indica qual perfil está ATIVO; "Salvar" do editor convive com "Salvar
    Perfil" do rodapé; "Salvar Perfil" DESCARTA a política de rumble (`draft_config.py:282`).
  - Status: tooltip "PS" ficou preso na tela (vazou de hover); barra de bateria sem rótulo e
    sem dizer de QUAL controle é; seletor de alvo (Todos/1/2) silencioso e sem eco nas abas de
    output.
  - Steam Input LIGADO em 1 perfil (conflito ativo, [WARN] no cartão anti-storm de hoje).
- Paridade de superfícies (buracos): Modo Nativo — só CLI; Co-op — só CLI; pause/resume — sem
  superfície; alvo por-controle — banner Status + applet, sem eco; applet sem
  nativo/coop/flavor/Steam Input.

## 3. Inventário UX da GUI (resumo do top 20 — relatório completo na varredura)

1. Modo Nativo invisível na GUI/applet (crítico).
2. SEIS botões "Aplicar" com escopos diferentes; dois com rótulo idêntico (crítico).
3. "Salvar Perfil" perde a política de rumble; "Aplicar" do rodapé não a re-aplica (crítico).
4. Co-op só na CLI (alto).
5. Abas de output não indicam o controle-alvo; resultado "ambos Player 1" (alto).
6. Seletor de alvo escondido/silencioso (alto).
7. "Parar" ≠ desligar; reabrir GUI religa o daemon sem avisar (alto).
8. Emulação × Mouse com responsabilidade cruzada e mapeamento duplicado (alto).
9. Quatro conceitos de "parar/soltar" sem glossário (alto).
10. Gatilhos: modo é live-preview, parâmetros exigem Aplicar — misto não sinalizado (méd-alto).
11. Lightbar por BT não pinta cor e a GUI não avisa (méd-alto).
12. 19 modos como paredão de botões (2 colunas × ~8 linhas POR GATILHO) dominando a aba;
    sliders/Aplicar abaixo da dobra; rótulo "Modo:" desalinhado (méd-alto; confirmado ao vivo).
13. Cor/brilho silenciosos até o Aplicar (médio).
14. pause/resume sem toggle em superfície alguma (médio).
15. Reconciliação de Emulação/Mouse só ao entrar na aba (médio).
16. Cartão anti-storm expõe jargão (storm/-71/dsx/quirk) (médio).
17. Sem onboarding/first-run (médio).
18. Player-LED com três caminhos (checkbox/preset/Aplicar LEDs) (médio).
19. Sliders de mouse com estado dirty/in_profile invisível (baixo-médio).
20. Riscos de regressão: layout validado mas dependente de workarounds COSMIC (baixo).

Bugs visuais novos observados hoje: tooltip "PS" órfão na aba Status; bateria sem rótulo;
grande área vazia nas abas Lightbar/Mouse/Teclado (densidade desperdiçada em 1080p).

## 4. Matriz feature × superfície (alvo: paridade)

| Feature | IPC | CLI | GUI | Applet | Perfil |
|---|---|---|---|---|---|
| Modo Nativo | sim | sim | NÃO | NÃO | NÃO (proposto: sim) |
| Gamepad virtual (flavor) | sim | sim | sim | NÃO | NÃO (proposto: sim) |
| Co-op N players | sim | sim | NÃO | NÃO | NÃO (proposto: sim) |
| Mouse por perfil | sim | sim | sim | NÃO | sim (point_and_click) |
| Modo jogo (suppress) | sim | — | sim | sim | sim |
| Alvo por-controle | sim | sim | banner | sim | — (fase futura) |
| Pause/resume | sim | — | NÃO | NÃO | — |
| Desligar de verdade | — | sim | ambíguo | sim | — |

## 5. Proposta: 5 waves (V3.12) — da fundação à interface

### W1 — Identidade e isolamento de controle (a fundação; destrava 4P e mata a duplicação)
1. Identidade universal por MAC/serial (uniq do evdev == serial hidapi, técnica já usada em
   `sysfs_leds.discover`): `find_all_dualsense_evdevs` retorna mapping {mac → node};
   backend, EvdevReader do primário e CoopManager passam a falar MAC entre si; coop keyed por
   MAC (path vira detalhe volátil). Elimina as 3 visões divergentes (2.2a).
2. Grab verificado: `set_grab` retorna sucesso/falha e loga; `_spawn_player` NÃO cria vpad se
   o grab falhou (retry no próximo sync); contador no state_full para a GUI mostrar.
3. Esconder dos jogos o que não é jogável (o "HidHide do Linux", udev + sysfs, sem C):
   regra udev marcando os nodes FÍSICOS de gamepad com ID_INPUT_JOYSTICK="0" (dinâmica,
   aplicada pelo daemon ao ligar gamepad/coop via `udevadm` ou property por-device) e os
   Motion Sensors (js1/js3) permanentemente sem ID_INPUT_JOYSTICK (SDL2/jogos ignoram);
   reversão simétrica ao desligar. Resultado: o jogo enumera SÓ os vpads P1..PN.
4. Validação: matriz 2/3/4 controles com hotplug em cada estado (spec de teste com contadores
   de vpads/grabs ativos + asserts de unicidade por MAC).

### W2 — Performance multi-controle (mata o throttling; abre espaço p/ 4P)
1. Tirar as varreduras do caminho quente: cache/invalidação por udev-monitor (pyudev) em vez
   de re-enumerar /dev/input a cada 2 s (coop.sync + watchdog compartilham a MESMA visão,
   invalidada por evento de hotplug); `coop.sync` sai do event loop.
2. Delta-check no `forward_analog` (só emite eixo que mudou) + deadzone de repouso opcional
   para o tremor de stick; agrupa em 1 SYN.
3. `os.nice(10)` no daemon (e/ou `CPUSchedulingPolicy=idle`… não: input precisa de latência —
   usar nice moderado + `IOSchedulingClass`) — nunca competir de igual com o jogo.
4. Report_threads: elevar throttle default com 2+ controles (janela adaptativa) e suprimir
   write OUT quando o report não mudou (dirty-flag no prepareReport pin).
5. SE (e só se) o Python continuar sendo gargalo com 4 controles: helper de forward em Rust
   (evdev→uinput por controle, ~200 linhas, sem GIL), daemon Python segue orquestrando por
   IPC. Baixo nível autorizado, mas é plano B — os itens 1-4 provavelmente bastam.
6. Bench antes/depois: py-spy + contadores por tick no metrics (p95 do tick, eventos/s).

### W3 — Perfis como fonte de verdade dos MODOS (Sackboy nativo por default)
1. Schema v2 do perfil: seção `mode` opcional — `{"kind": "native" | "gamepad" | "desktop",
   "gamepad_flavor": "dualsense|xbox", "coop": bool}` — com a MESMA semântica de lock manual
   de 30 s do point_and_click. Perfil Sackboy: `mode.kind=native` → focou o jogo, o daemon
   solta o controle (adaptativos nativos Sony); saiu do jogo, restaura. É o "coexistir": cada
   contexto ativa seu conjunto, sem toggles globais brigando.
2. Consertar o autoswitch cego no systemd (wm_class=unknown ao vivo): diagnosticar
   `_ensure_display_env` + backend na sessão real; expor na GUI/doctor um "detector de janela:
   OK/FALHOU + qual backend"; sem isso, perfil por jogo não existe.
3. Presets novos: `sackboy_nativo` (match Steam appid/proton), `coop_local` (gamepad+coop).
4. GUI de perfil ganha o seletor de modo (segmentado: Desktop / Gamepad / Nativo + checkbox
   co-op) e a lista de perfis passa a destacar o ATIVO.

### W4 — Redesign da GUI (a cirurgia de UX, guiada pelo top 20)
1. Aba nova "Início/Modo" (primeira): estado dos N controles (cards por controle com bateria,
   transporte, player, alvo) + UM comutador central de modo do sistema (Desktop / Jogo
   gamepad / Jogo nativo / Co-op) + botão "Desligar Hefesto (voltar ao Linux puro)" com
   confirmação — o Modo Nativo/desligar deixa de ser easter egg. Espelha os 4 conceitos de
   parar num só lugar com texto claro.
2. Unificação do Aplicar: manter SÓ o Aplicar global (rodapé) + ações imediatas explícitas
   ("enviar agora" com ícone) nas abas; eliminar rótulos duplicados; toast padronizado com o
   ALVO ("Aplicado ao Controle 2").
3. Alvo por-controle visível em TODA aba de output (chip "Alvo: Todos" clicável no topo das
   abas Gatilhos/Lightbar/Rumble).
4. Gatilhos: modos em grade compacta (FlowBox 4 colunas, botões menores, coluna única por
   gatilho com cabeçalho fixo) OU lista rolável com busca; parâmetros/Aplicar acima da dobra;
   comportamento live-preview × Aplicar sinalizado no rótulo.
5. Fundir Emulação+Mouse+Teclado numa aba "Entrada" com 3 seções (gamepad/mouse/teclado) e
   mover Steam Input/mic/anti-storm para "Sistema" (com o cartão do daemon); glossário curto
   embutido (o que é modo jogo / nativo / pause).
6. Corrigir sincronizações: draft nasce do estado VIVO (lightbar/LEDs/política); rumble_policy
   entra no draft/perfil; lista de perfis marca ativo; matar tooltip órfão; rótulo de bateria
   por controle.
7. Applet: adicionar Modo Nativo, co-op, flavor e "abrir GUI na aba X"; manter paridade com o
   comutador da W4.1.

### W5 — Sincronização run/install/applet + validação de conjunto
1. install.sh/uninstall.sh: nova regra udev dos Motion Sensors + propriedade dinâmica de
   esconder (W1.3) com reversão simétrica; applet ganha os métodos novos; smoke de paridade
   (o check_packaging_parity já existe — estender).
2. Testes de coexistência: matriz de features (nativo×coop×mouse×suppress×hotkey) com
   propriedade-alvo "nenhuma combinação deixa o controle mudo ou dobrado".
3. Validação ao vivo: 2/3/4 controles (emprestar 2), Sackboy nativo por perfil, jogo co-op 4P.

## 6. Decisões em aberto para a mantenedora

1. Aprovar a ordem W1→W5 (fundação antes de interface) ou priorizar W4 (dor visível) após W1?
2. W2.5 (helper Rust) fica como plano B condicionado a bench, ok?
3. Aba "Início/Modo" substitui a atual Status como primeira aba (Status vira "Monitor")?
4. Co-op na GUI: toggle simples ou seleção de player por controle (arrastar ordem)?

## 7. Evidências

- Screenshots 2026-07-13: /tmp/Screenshot_2026-07-13_16-5[5-8]*.png (Status com tooltip órfão,
  Gatilhos paredão, Lightbar dessincronizada, Rumble, Perfis sem ativo, Daemon com [WARN]
  Steam Input + log de migração event21→event25, Emulação contraditória, Mouse, Teclado).
- /proc/bus/input/devices com 2 controles + coop: 11 devices / js0-js5 (§2.2c).
- daemon.state_full 17:02: gamepad dualsense ON, coop ON players=2, suppressed=false,
  native=false, perfil "vitoria".
- Varredura de runtime e inventário UX completos: sessão de estudo 2026-07-13 (agentes de
  leitura, referências file:line inline neste doc).
