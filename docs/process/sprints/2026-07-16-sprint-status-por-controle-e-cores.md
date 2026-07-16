# Sprint SPRINT-STATUS-CARDS-01 — aba Status vira um card por controle, inputs na cor do lightbar de cada um

Pedido da mantenedora (2026-07-16, ao vivo): *"na aba Status, a cor dos inputs deve ser a
MESMA cor do lightbar daquele controle, e deve aparecer para TODOS os players"* (pedido 1
da onda). Este doc é um **PLANO** — nada daqui foi construído ainda. Branch
`sprint/harmonia-uhid`. O desenho abaixo já incorpora a revisão adversarial (3 lentes:
técnica, regressão, escopo) — incluindo duas refutações que **mudaram** o plano original.

## TL;DR

- A aba Status é **single-controller por construção**: os widgets ao vivo (barras L2/R2,
  `StickPreviewGtk`, grid de `ButtonGlyph`) são singletons alimentados pelos campos de topo
  do `daemon.state_full` — que vêm de `daemon._last_state`, só o controle **primário**.
- O bloco `controllers` do `state_full` já traz `index/transport/is_primary/uniq/battery_pct/player`
  por controle, mas **nem cor de lightbar nem inputs**.
- O desenho: enriquecer o bloco `controllers` com `lightbar_rgb` + `inputs` (no **handler
  IPC**, nunca dentro de `describe_controllers()` — caminho quente do rumble) e a GUI virar
  **1 card por controle**, com os traços pintados na cor do lightbar daquele controle —
  **com regra de contraste obrigatória** (a cor atual dela, `16 32 72`, tem contraste
  1.12:1 contra o fundo do tema: invisível crua).
- **Correção da revisão adversarial que muda o plano**: o `multi_intensity` do sysfs NÃO é
  "a verdade do hardware" — é o último valor escrito **via classe LED**. No probe o kernel
  zera as intensidades e acende a lightbar de AZUL por fora da classe. Sem **priming**
  (escrever via sysfs a cor vigente a cada nó novo), o card mentiria em todo reconnect BT.
  A cor exibida segue o **dono da escrita** (sysfs gravável → sysfs; caminho hidraw →
  `_desired`; Nativo → "o jogo é dono do LED").
- **Regra de Ouro honrada e verificada**: NADA novo no install/uninstall (a regra
  `77-dualsense-leds.rules` já entra por default desde v3.3.1 e sai simétrica no
  uninstall; a leitura sysfs é livre). Sem launch option, sem env var, sem "cole isto".
  Sudo-zero em runtime preservado. O doctor ganha **um check read-only** (diagnóstico,
  não artefato).

## O problema, na raiz (PROVADO NO CÓDIGO)

O contrato `daemon.state_full` publica inputs ao vivo **só do primário** (topo do dict,
vindo de `daemon._last_state` — `ipc_handlers.py:276-278`, `lifecycle.py:1580,1613`), e o
bloco `controllers` nunca carregou cor de lightbar nem inputs
(`backend_pydualsense.py:977-1012`). A GUI espelha isso com widgets singleton: um único
conjunto de barras/sticks/glyphs lendo `state['l2_raw']`, `state['lx']`...
(`status_actions.py:657-707`); com 2+ controles a bateria diz "(Controle 1)" (linha 807).

A cor por controle nunca foi exposta porque o backend só rastreia um `_desired` **GLOBAL**
de fan-out: `set_led` grava `_desired.led` incondicionalmente mesmo com alvo por-controle
(`backend_pydualsense.py:915-916`), e `_reapply_desired` pinta um controle replugado com a
cor pedida para OUTRO (`871-906`) — o leak do Estudo 1. A fonte da cor (sysfs
`multi_intensity` do `hid_playstation`, legível por MAC em USB e BT, da
FEAT-DSX-LIGHTBAR-SYSFS-01) só era usada para ESCREVER, nunca ligada ao pipeline de
estado para LER.

## O que foi provado — com o rótulo honesto

**PROVADO AO VIVO (2026-07-16, daemon parado — inactive desde 13:58, NÃO reiniciado):**

- A cor de cada lightbar é legível sem privilégio, por MAC, em USB **e** BT:
  `/sys/class/leds/input30:rgb:indicator/multi_intensity` = `16 32 72`
  (BT, `HID_UNIQ=aa:bb:cc:00:00:02`) e `input75` idem (USB, `aa:bb:cc:00:00:01`);
  permissão `-rw-rw-rw-` (regra 77 instalada); `brightness=255`.
- As duas lightbars dela estão na **MESMA** cor (consequência do fan-out global do
  `_desired`) — ver a dependência entre frentes em §Fronteiras.
- Contraste WCAG de `(16,32,72)` contra `#282a36` = **1.12:1** (recalculado por dois
  revisores independentes: 1.11 e 1.115) — a cor real dela é ilegível como traço.
- O 8BitDo em modo Nintendo (`057E:2009`) registra LEDs `player-1..5` sem
  `rgb:indicator` — o glob do `discover()` não o pega (sem falso positivo).

**PROVADO NO CÓDIGO (todas as âncoras auditadas pelos 3 revisores — nenhuma alucinada):**

- Singletons e `_last_state` (acima); co-op tem reader com `snapshot()` por jogador
  (`coop.py:95-99,311-343,556-585`), gate no poll loop (`lifecycle.py:1669-1674`).
- `describe_controllers()` roda no **caminho quente do rumble**: o sink de FF do primário
  chama `apply_game_rumble` → `_resolve_output_index` → `describe()` **a cada evento FF**
  (`gamepad.py:134-144, 261-277`); o contrato do método é "leitura barata, sem HID I/O".
- `EvdevSnapshot` tem exatamente os campos do topo do `state_full`
  (`lx/ly/rx/ry/l2_raw/r2_raw/buttons_pressed`, escala 0-255) — sem conversão
  (`evdev_reader.py:31-40`).
- Campos novos no `state_full` são retrocompatíveis: applet sem `deny_unknown_fields`
  (grep vazio em `packaging/cosmic-applet/src/`), CLI usa `.get` defensivo.
- Todos os 19 SVGs `*_active.svg` têm o literal `#bd93f9` — mas moram em
  `assets/glyphs/` na **RAIZ do repo** (e instalados em
  `~/.local/share/hefesto-dualsense4unix/glyphs`), com ordem de resolução em
  `button_glyph.py:61-73`.
- O app força o tema Drácula (`theme.py:42` + CssProvider APPLICATION) e o
  `StickPreviewGtk` pinta o próprio fundo `#282a36` no cairo (`stick_preview_gtk.py:30,88-89`).

**PROVADO NO CÓDIGO DO KERNEL (achado da revisão adversarial — muda o desenho):**

- `hid-playstation.c` upstream: `ps_lightbar_register` aloca o LED multicolor com
  intensidades **zeradas** e `dualsense_create` acende a lightbar de **AZUL (0,0,128)**
  por um caminho interno (`dualsense_set_lightbar` → `schedule_work`) que **nunca**
  atualiza a classe LED. Todo controle recém-(re)conectado lê `0 0 0` no sysfs com a
  lightbar visivelmente ACESA em azul. A leitura `16 32 72` da máquina dela só é fiel
  porque o daemon escreveu via sysfs antes de parar.
- Escrita por hidraw (caminho pydualsense, usado quando o nó não é gravável —
  `backend_pydualsense.py:649,894-897` — e pelo JOGO em modo Nativo) **não** atualiza a
  classe LED: o `multi_intensity` fica stale por construção.

**HIPÓTESE (a validar no STATUS-05):** 4 cards a 10 Hz não jankeiam em NVIDIA/XWayland
com diff por card + tinting cacheado. Plano B: degradar glyphs para 24px.

## As duas refutações que mudaram o plano (honestidade primeiro)

1. **"O sysfs é a verdade do hardware" — REFUTADO em parte.** É a verdade **somente
   quando fomos nós que escrevemos via sysfs**. O desenho agora tem `lightbar_source`
   explícito e **priming** obrigatório (ver STATUS-01). E é **proibido** rotular
   `0 0 0` como "apagada" sem saber se fomos NÓS que escrevemos o `0 0 0` — estado
   "0 0 0 nunca escrito por nós" = **"cor desconhecida"**, nunca "apagada" (o LED pode
   estar brilhando azul-kernel nesse exato momento).
2. **STATUS-06 original (_desired por controle) — REMOVIDO desta frente.** O refactor
   `_DesiredOutput` global → mapa por-MAC é o **núcleo P0 da frente de perfis por
   controle** (pedido 2 da Vitória) — mantê-lo aqui duplicaria o trabalho. Ver §Fronteiras.

Além disso, três critérios/prioridades foram corrigidos pelos revisores: o critério de
timers do STATUS-02 (o original reprovava o código atual), a prioridade do STATUS-04
(P1 → **P2**: co-op é default ON sem checkbox, o buraco real é só o modo Nativo) e o
compromisso da cor ("a mesma cor" literal é impossível quando o lightbar é escuro —
ver STATUS-03 e o aceite humano no STATUS-05).

## O desenho

**Dados (daemon, zero IPC novo — pega carona no `state_full` que a GUI já polla a
10 Hz com guard `_live_inflight`; não citar "20 Hz", a docstring do handler está
desatualizada):**

1. `SysfsLedNode.get_rgb()/is_on()` em `core/sysfs_leds.py` (leitura de
   `multi_intensity` + `brightness`).
2. O enriquecimento com cor mora no **handler IPC** (`_handle_daemon_state_full`, onde
   já se enriquece com `player`) — **nunca leitura crua dentro de
   `describe_controllers()`** (caminho quente do FF). A leitura tem cache TTL ~1s.
3. Cada entrada de `controllers` ganha `lightbar_rgb: [r,g,b]|None`, `lightbar_on: bool`
   e `lightbar_source: "sysfs"|"desired"|"desconhecida"`, seguindo o **dono da escrita**:
   - nó em `_sysfs[key]` (gravável; o backend escreve por sysfs) e fora do Nativo →
     leitura sysfs é a verdade (com priming garantindo frescor);
   - nó NÃO gravável (escrita foi por pydualsense/hidraw) → sysfs stale por construção →
     usar `_desired`/última cor aplicada; sem nada, `"desconhecida"`;
   - modo Nativo (`_output_mute`) → o jogo é dono do LED → última cor conhecida +
     flag para o card avisar.
4. **Priming**: a cada nó LED novo (hotplug, reconnect BT), o daemon escreve via sysfs a
   cor vigente daquele controle — **inclusive quando `_desired.led` é None**: nesse caso
   escreve o azul-default do kernel (`0 0 128`, idempotente com o hardware) só para a
   classe LED convergir. Exceção: em Nativo não faz priming (o jogo é dono). Ponto de
   extensão: `_refresh_sysfs_leds` (`backend_pydualsense.py:664-676`), que hoje pula
   quando `_desired.led is None`.
5. `inputs: {lx,ly,rx,ry,l2_raw,r2_raw,buttons}|None` por entrada: primário de
   `daemon._last_state`; secundários casados por uniq via novo método público
   `CoopManager.live_snapshots() -> dict[mac, EvdevSnapshot]`; `None` sem leitor
   (o card mostra "—", nunca valores congelados como se fossem vivos).

**GUI:**

6. Novo widget `ControllerCard` (construído por código, como os glyphs hoje): header com
   swatch da cor **CRUA** + "Controle N — USB · Jogador X" + bateria do próprio controle;
   barras L2/R2; 2 `StickPreviewGtk` (90px com 2+ cards); grid de glyphs (28px). O glade
   troca os frames "Gatilhos"/"Sticks e botões" por `GtkScrolledWindow > status_players_slot`.
7. Reconstrução de cards SÓ quando o conjunto de controles muda, keyed por
   **`(index, uniq)` com filtro de `connected`** (uniq é None para handle keyed por path,
   e a entrada-placeholder offline não tem index nem uniq — precedente
   HARM-CARD-FANTASMA-01, `home_actions.py:381-390`). Com 0 controles: o fallback offline
   existente da aba (UI-STATUS-OFFLINE-FALLBACK-01), sem card fantasma.
8. Cor com contraste garantido: `ensure_min_contrast(rgb, bg, ratio>=3.0)` sobe a
   luminosidade em HLS preservando o matiz, calculada contra o **pior caso** dos fundos
   reais (o StickPreview pinta o próprio `#282a36`; glyphs e barras assentam no fundo do
   tema GTK escuro forçado — que não é exatamente `#282a36`). A cor crua fica no swatch;
   a ajustada pinta os traços.
9. Tinting: `StickPreviewGtk.set_accent(rgb)`; `ButtonGlyph` tinta a variante `_active`
   substituindo o literal `#bd93f9` no texto do SVG (replace-all — há 2-4 ocorrências por
   arquivo) e carregando via `GdkPixbuf.PixbufLoader` com `loader.set_size(size,size)`,
   lendo do **GLYPHS_DIR resolvido** (funciona nos 4 caminhos de resolução), cacheado por
   `(nome, size, hex)` — nunca recarga por tick. Barras L2/R2 via CssProvider por card,
   atualizado só quando a cor muda.

Segue as regras de harmonia: **sem dropdowns** (cards sempre visíveis —
cosmic-epoch#2497), gate `_popup_is_open` preservado, **sem sudo em runtime**, zero
timers periódicos novos, zero polling por controle.

## Itens

### STATUS-01 — `state_full` expõe cor da lightbar e inputs POR CONTROLE (P0, CLAUDE)

- **Arquivos**: `core/sysfs_leds.py`, `core/backend_pydualsense.py`,
  `daemon/ipc_handlers.py`, `daemon/subsystems/coop.py`,
  `tests/unit/test_ipc_state_per_controller.py` (novo).
- **O que fazer**: itens 1-5 do desenho. Obrigatório: (a) `describe_controllers()`
  permanece sem I/O de arquivo — o enriquecimento de cor vive no handler IPC com cache
  TTL ~1s (o método roda a cada evento FF do jogo); (b) `lightbar_source` pelo dono da
  escrita; (c) priming em nó novo (inclusive `_desired.led` None → azul-kernel), pulado
  em Nativo; (d) rastrear por nó se o `0 0 0` foi escrito por nós (só então significa
  "apagada"); (e) `CoopManager.live_snapshots()` não-destrutivo (o `snapshot()` já copia).
- **Critério de aceite (verificável)**: teste hermético com
  `HEFESTO_DUALSENSE4UNIX_LEDS_ROOT` fake — **atenção**: o env é lido no IMPORT de
  `sysfs_leds` (linha 31), o teste seta o env antes do import ou monkeypatcha o atributo
  do módulo. Asserts: `controllers[i]['lightbar_rgb']` == cor gravada no fake **quando o
  nó é gravável e fomos nós que escrevemos** (`lightbar_source=="sysfs"`); nó novo com
  classe zerada e sem escrita nossa → `lightbar_source=="desconhecida"` (nunca rgb 0,0,0
  apresentado como "apagada"); nó não-gravável → `lightbar_source=="desired"`; priming
  comprovado: após hotplug fake, o valor da classe converge para a cor vigente; `inputs`
  do primário espelha `_last_state`; com co-op fake ativo o secundário traz inputs do
  reader dele; sem leitor → `inputs is None`; um `describe_controllers()` chamado em loop
  não abre arquivo nenhum (assert no fake de I/O); `cmd_controller`/`cmd_status` e applet
  seguem parseando (testes de contrato verdes); gate completo verde.

### STATUS-02 — Aba Status vira 1 card por controle (todos os DualSense visíveis) (P0, CLAUDE)

- **Arquivos**: `gui/main.glade`, `app/actions/status_actions.py`,
  `app/widgets/controller_card.py` (novo), `tests/unit/test_status_cards.py` (novo),
  `tests/unit/test_status_buttons_glyphs.py`, `tests/unit/test_status_actions_reconnect.py`.
- **O que fazer**: itens 6-7 do desenho. Cards keyed por `(index, uniq)` + filtro de
  `connected`; caches `_last_*` migram para dentro do card; o tick de 10 Hz distribui
  `controllers[i].inputs` para o card i com diff por card. Com 1 controle, 1 card (layout
  equivalente ao atual). A bateria "(Controle 1)" do frame Estado sai quando há 2+ (cada
  card tem a sua). `inputs is None` → card mostra "—" (sem leitor), nunca o último valor
  como se fosse vivo. Ajustar os testes antigos da aba **na mesma PR** (vão quebrar com a
  mudança de estrutura — não deixar para depois).
- **Critério de aceite (verificável)**: teste headless: state com 2 controles → 2 cards
  com títulos e baterias próprios; 2 ticks com o MESMO conjunto → mesmos objetos de widget
  (comparação por `id()`, sem rebuild); inputs do card 2 vêm exclusivamente de
  `controllers[1].inputs`; entrada-placeholder offline e uniq None **não** criam card
  fantasma nem colidem; **nenhuma ocorrência NOVA de `GLib.timeout_add*` em relação ao
  baseline** (hoje a mixin tem 4: 3 periódicos — 100ms, 500ms, reconnect em segundos — e
  1 one-shot de 5s, mais 2 `idle_add`; o gate é diff, não contagem absoluta).

### STATUS-03 — Inputs pintados com a cor do lightbar do próprio controle, com contraste mínimo (P0, CLAUDE)

- **Arquivos**: `utils/color_contrast.py` (novo), `gui/widgets/stick_preview_gtk.py`,
  `gui/widgets/button_glyph.py`, `app/widgets/controller_card.py`,
  `tests/unit/test_color_contrast.py` (novo).
- **O que fazer**: itens 8-9 do desenho. Rótulos do card pela `lightbar_source`:
  `"sysfs"` + rgb 0,0,0 escrito por nós → "Lightbar: apagada" + accent neutro `#6272a4`;
  `"desconhecida"` → "Lightbar: cor desconhecida" + accent neutro (NUNCA "apagada");
  Nativo → "em Nativo o jogo é dono do LED" + última cor conhecida. Documentar no
  código: a garantia de contraste pressupõe o tema Drácula do app carregado (se o
  `theme.css` falhar — o app loga e segue — os widgets caem no tema claro e a régua
  contra fundo escuro deixa de valer; edge case aceito).
- **Critério de aceite (verificável)**: teste puro paramétrico com >=20 cores (incluindo
  `16 32 72` medida ao vivo e `0 0 0`): `contraste(saida, pior_fundo) >= 3.0` e
  Δmatiz <= 4° para cores cromáticas; teste de widget stub: trocar a cor N vezes gera no
  máximo 1 recarga de pixbuf por `(nome, size, hex)` (cache hit verificável); o tinting
  resolve o SVG pelo `GLYPHS_DIR` resolvido (testar com dir fake — não caminho fixo).
- **Honestidade para a validação**: os traços NÃO serão literalmente "a mesma cor" quando
  o lightbar for escuro — serão a mesma matiz, clareada. O swatch mostra a cor crua.
  A Vitória aceita (ou rejeita) esse compromisso no STATUS-05.

### STATUS-04 — Leitores passivos (SEM grab) para controles sem reader (P2, CLAUDE — só se a validação sentir falta)

- **Por que desceu de P1 para P2 (revisão adversarial)**: co-op é DEFAULT ON, o checkbox
  saiu da UI (LEIGO-01) e a migração apaga o opt-out legado — no estado normal da máquina
  dela, TODO secundário já tem reader e o card dele já terá inputs só com STATUS-01/02.
  O buraco real é o **modo Nativo** (desliga a emulação de gamepad →
  `should_be_active()==False` → co-op desmontado → secundários sem leitor) e
  emulação-off — cenários em que ela está jogando fullscreen, não olhando a GUI.
  Sem este item, nesses modos o card mostra "—" (honesto, não congelado).
- **Arquivos**: `daemon/subsystems/status_readers.py` (novo), `daemon/lifecycle.py`,
  `daemon/ipc_handlers.py`, `tests/unit/test_status_readers.py` (novo).
- **O que fazer**: pool keyed por MAC que abre `EvdevReader` SEM `set_grab` para cada
  DualSense físico conectado sem leitor. **Obrigatório (revisão adversarial)**:
  (a) reusar `discover_dualsense_evdevs()` — o filtro `_is_virtual_evdev`
  (realpath contém `/devices/virtual/`) cobre uinput E uhid; enumeração própria por
  VID/PID abriria o PRÓPRIO vpad do daemon (`0x0DF2` está em `DUALSENSE_PIDS` e o
  fallback uinput cria `054c:0ce6` idêntico ao físico — o Estudo 1 provou que esse
  fallback acontece em BT) e o card viraria feedback do próprio daemon;
  (b) **call-site próprio no poll loop** — o sync do co-op retorna cedo quando
  `should_be_active()==False` (`coop.py:209-213`), exatamente os modos em que o pool é
  necessário; não herdar esse gate; (c) ceder o leitor quando o co-op assume o controle
  (handoff na mesma reconciliação ~2s) e derrubar thread+fd no hotplug-out.
- **Critério de aceite (verificável)**: com co-op DESLIGADO e 2 controles fake:
  `controllers[1].inputs != None` e NENHUM `set_grab(True)` foi chamado no reader do
  secundário (assert no fake); o pool NUNCA abre device com realpath em
  `/devices/virtual/` (assert com vpad fake); hotplug-out remove o reader do pool sem fd
  vazado (teste de não-vazamento); com co-op ligado o pool não duplica leitor de quem já
  é jogador.

### STATUS-05 — Validação humana ao vivo com o hardware da mesa (P1, AMBOS)

- **Hardware**: 1 DualSense BT + 1 DualSense cabo (o 8BitDo NÃO participa — ver
  §Fronteiras). **Pré-requisito**: subir o daemon (estava inactive durante todo o estudo).
- **Roteiro (roteirizado por causa do leak do `_desired` global, ainda vivo até a frente
  de perfis entregar)**:
  1. Com o daemon ativo, a Vitória define **cores DIFERENTES** para cada controle
     (seletor de alvo no banner + aba Lightbar) — hoje as duas lightbars estão na MESMA
     cor (`16 32 72`, provado ao vivo); com cores iguais a validação não distingue nada.
  2. Abre a aba Status e confere: 2 cards, cada um com a cor do PRÓPRIO lightbar
     (swatch cru + traços ajustados legíveis), número do jogador e bateria própria.
  3. Mexe cada controle e vê só o card dele acender (com co-op ligado; ou em qualquer
     modo, se o STATUS-04 tiver entrado).
  4. **Aceite explícito do compromisso da cor**: swatch = cor crua, traços = mesma matiz
     clareada. Se ela rejeitar ("não é a mesma cor"), volta como decisão de design, não
     como bug.
  5. **NÃO replugar controle no meio do teste**: o replug re-pinta com a cor global
     (leak do `_desired`, causa cortada na frente de perfis) e confunde o resultado —
     se acontecer, o card vai mostrar a cor errada QUE FOI DE FATO APLICADA (o card é
     fiel; o bug é do backend).
  6. Screenshot via `claude-screenshot.sh` anexado a este doc.
- **Critério de aceite**: ela confirma verbalmente que cada card corresponde ao controle
  certo (cor + input + bateria) em USB E BT; screenshot anexado; divergência vira bug
  com o card/MAC apontado. **Atenção**: o card mostrando inputs por BT NÃO prova que BT
  funciona em JOGO — o relato "BT zero inputs" é de outra camada/frente (dedup/launch
  option); não usar a aba Status como evidência de cura desse bug.

### STATUS-06 — MOVIDO: `_desired` por controle pertence à frente de perfis por controle

Refutado pela revisão adversarial como item desta frente: o refactor
`_DesiredOutput` global → mapa por-MAC é o **núcleo P0 obrigatório do pedido 2** (perfis
por controle) — não existe entregar o pedido 2 sem ele. Mantê-lo aqui duplicaria o
refactor num campo que também é tocado pelo mute/unmute do Nativo e pela aplicação de
perfil (histórico de "vários donos do mesmo estado" do projeto). **Nesta frente**: os
cards mostram a verdade (sysfs com priming) e, enquanto o leak existir, vão EXIBIR
honestamente a cor errada que o replug de fato aplica — o card é o termômetro, a cura
mora na outra frente.

### STATUS-07 — doctor confere a regra 77 e a gravabilidade do nó LED (P2, CLAUDE)

- **Arquivos**: `scripts/doctor.sh`, teste do doctor se houver harness.
- **Por quê**: verificado nesta sessão — o `check_udev` do doctor cobre 70/71/72/75 mas
  **não a 77-dualsense-leds.rules**. Sem a 77 (outra máquina, upgrade antigo), o nó não é
  gravável → o backend escreve por hidraw → o card mostra cor via caminho degradado
  (`lightbar_source=="desired"`), e a usuária precisa saber o porquê. É um check
  **read-only de diagnóstico**, não um artefato novo de install (o install já põe a 77
  por default; o uninstall já a remove — nada muda neles).
- **Critério de aceite**: doctor com a 77 presente + nó gravável → `[ OK ]`; sem a regra →
  aviso apontando `sudo bash scripts/install_udev.sh`; com DualSense conectado, o check
  usa um nó real; sem controle, pula sem falhar.

## Ordem

STATUS-01 → STATUS-02 → STATUS-03 (os três P0 são o que ela vê) → STATUS-05 (validação
humana; decide se o STATUS-04 é necessário) → STATUS-04 (só se fizer falta) → STATUS-07.

## Fronteiras com as outras frentes (escopo honesto)

- **Só DualSense ganha card.** `describe_controllers()` enumera handles pydualsense
  (VID `054c` + `DUALSENSE_PIDS`) e o co-op/pool só descobre DualSense. O **8BitDo SN30
  Pro** dela (enumerado como Nintendo Pro Controller `057E:2009`, plugado agora na
  máquina) **NUNCA aparece nesta frente** — "todos os players" aqui significa "todos os
  DualSense". A visibilidade dos demais controles é a aba da frente multi-controle
  (pedido 4 da Vitória).
- **Cores distintas por default** vêm da frente do pedido 3 (cor automática por
  controle) e do refactor `_desired` por-MAC (frente de perfis, pedido 2). Enquanto elas
  não entregarem, os dois cards podem nascer da MESMA cor (estado atual da máquina dela)
  — o STATUS-05 contorna setando cores manualmente. Declarar isso evita a estreia
  parecer "não funciona".
- **BT em jogo** ("BT zero inputs", RDR2): outra frente (dedup por udev / launch option
  veneno). A aba Status NÃO é evidência de cura disso.
- **Modo Nativo**: o card pode divergir duas vezes — cor (o jogo escreve por hidraw, o
  sysfs fica stale → rótulo "o jogo é dono do LED") e inputs de secundários (co-op
  desmontado → "—" sem STATUS-04). Comportamento documentado no card, não escondido.

## Conformidade com a Regra de Ouro (verificada, não presumida)

- **Nada novo no install/uninstall**: a leitura sysfs é livre (0644 default do kernel já
  bastaria; a 77 dá 0666 para escrita e é **incondicional desde v3.3.1** — `install.sh`
  ~l.66-68), o uninstall remove a 77 por default (`uninstall.sh:317`), a regra está na
  máquina dela. Sem launch option, sem env var, sem flag, sem "cole isto".
- **Sudo-zero em runtime preservado**: o priming é uma escrita sysfs do daemon em nó
  0666 (regra 77) — sem sudo, sem botão que pede senha (decisão do commit bfd51db).
- **Doctor**: ganha um check read-only (STATUS-07) — diagnóstico do que o install já
  põe, coerente com a regra "o doctor.sh sabe verificar o que o install põe".

## Armadilhas conhecidas que esta frente atravessa

- **`describe_controllers()` é caminho quente** (roda por evento FF do jogo): nenhuma
  leitura de arquivo dentro dele — enriquecimento no handler IPC + cache TTL.
- **`multi_intensity` mente sem priming**: probe do kernel zera a classe e acende azul
  por fora dela; reconnect BT cria nó novo. `0 0 0` sem escrita nossa ≠ "apagada".
- **Nó não-gravável = sysfs stale** (escrita foi por hidraw): fonte vira `_desired`.
- **Vpad tem MAC próprio** (`02:fe:00:00:00:0N`) e pode ser `0df2` (uhid/Edge) OU
  `0ce6` (fallback uinput, idêntico ao físico — acontece em BT): qualquer enumeração de
  evdev DEVE filtrar `/devices/virtual/` (reusar `discover_dualsense_evdevs`).
- **Dropdowns quebram no COSMIC** (cosmic-epoch#2497): cards sempre visíveis, sem
  seletor popup; gate `_popup_is_open` preservado no rebuild.
- **GIL/throttling**: zero polling por controle, zero timers periódicos novos; um único
  `state_full` a 10 Hz (`LIVE_POLL_INTERVAL_MS=100`) com guard `_live_inflight` —
  não citar "20 Hz" (docstring desatualizada).
- **Glyphs**: SVGs em `assets/glyphs/` na raiz do repo E em `~/.local/share/...` quando
  instalado — tinting lê do `GLYPHS_DIR` resolvido (`button_glyph.py:61-73`) e usa
  `loader.set_size()`; cache por `(nome, size, hex)` obrigatório (recarga por tick a
  10 Hz = jank).
- **Testes herméticos**: `LEDS_ROOT` é lido no IMPORT de `sysfs_leds` (linha 31) —
  setar o env antes do import ou monkeypatchar o módulo.
- Herdadas da onda (não tocadas aqui, registradas por disciplina): valid_flag do rumble
  é máscara `0x03` (nunca só `0x01`), `_INPUT_PAYLOAD_SIZE=63`, regra udev de
  uhid/uinput numerada `<73` para uaccess virar ACL (+ `udevadm trigger
  --subsystem-match=misc`).

## Invariante do projeto

**Teste verde sem validação ao vivo NÃO fecha item.** STATUS-01..04 e 07 fecham com o
gate verde + os aceites herméticos; a frente inteira só fecha com o STATUS-05 (a Vitória
confirmando cardcontrole em USB e BT, com o compromisso da cor aceito explicitamente).

## Referências

- Estudo que originou a frente: Estudo 1 (117 agentes, 2026-07-16) — launch option
  veneno, vpad nem sempre Edge, leak do `_desired`.
- Revisão adversarial (3 lentes) desta frente — incorporada integralmente acima.
- `2026-07-15-sprint-uhid-dualsense-de-verdade.md` (UHID-03: LEDs por jogador via sysfs).
- `2026-07-15-sprint-4-jogadores.md` (4P-01/02/03: fundação de identidade — a frente de
  perfis por controle herda o antigo STATUS-06).
- FEAT-DSX-LIGHTBAR-SYSFS-01 (rota sysfs da lightbar, validada ao vivo em BT).
- Kernel upstream: `drivers/hid/hid-playstation.c` (`ps_lightbar_register`,
  `dualsense_create` → azul default fora da classe LED).
