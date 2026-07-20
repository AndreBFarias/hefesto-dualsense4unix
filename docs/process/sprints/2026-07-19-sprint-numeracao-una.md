# Sprint NUMA 2026-07-19 — numeração una + posse de exibição (Onda N)

> Síntese da Onda N: 3 designs × 3 juízes (cada juiz escolheu um vencedor diferente — D0, D1 e D2).
> Resolução: chassi arquitetural do D2 (gate em ponto ÚNICO no merge do backend — a única arquitetura
> que satisfaz simultaneamente o veto "camada GAME órfã no restart" e o veto "repaint-all repinta a
> cor do jogo"), retenção do D0 (retain-latest + replay — veto contra drop sem retenção), sinal de
> 3 estados do D1 (UNKNOWN = comportamento atual — veto contra sinal binário sem degradação).
> Sonda de holders /proc: VETADA (beco 18; não entra). Colisão no controllers.json: drop unilateral
> da entrada externa (DualSense vence) — nunca realocação, nunca poda bilateral.
> Mapa vigente: `docs/process/estudos/2026-07-19-mapa-retomada-e-incidente-wifi-bt.md`.

## Contexto — o incidente de 14:42 (boot 14:35, medido no journal)

Sem jogo nenhum rodando, o cliente Steam abriu os hidraws dos vpads (UHID_OPEN 14:42:31) e
escreveu `player_leds`+`lightbar`: a NOSSA réplica entregou a escrita ao físico e o DualSense
branco (slot 1, azul) virou **verde/player-3 da Steam**. A camada GAME do backend
(`_game_output_by_uniq`, backend_pydualsense.py:1869) foi populada pelo cliente e o reassert
passou a DEFENDER o verde. Agravantes medidos: escrita estrangeira na classe LED
(`multi_intensity` físico `0 64 0` com cache interno azul → `skip_cache` silencioso); fallback
posicional `ds_count+index+1` re-embaralhando os externos na GUI quando `ds_count` caiu; dois
registries fazendo read-modify-write no MESMO `controllers.json` com locks separados
(lost-update latente, lacuna 11 do mapa). Causa-raiz comum: **não existe autoridade de exibição**
— "sessão uhid aberta" era tratada como "jogo", e o cliente Steam também abre sessão.

## Decisão de autoridade

A autoridade de EXIBIÇÃO (lightbar + player_leds, e SÓ elas) passa a ser governada por um sinal
global de três estados — `game` / `daemon` / `unknown`:

- **`game`** (evidência positiva de jogo): jogo vence em TODOS os controles. DualSense exibem o
  número do jogo via réplica (REPLICA-03); externos não são disputados (tick suspende correções).
- **`daemon`** (evidência positiva de NÃO-jogo, estável): daemon é a única autoridade — réplicas
  de exibição são RETIDAS (retain-latest, nunca dropadas), a camada GAME não entra no merge, e o
  daemon DETECTA e repinta escritores estrangeiros (re-leitura sysfs antes dos skips de cache,
  dentro dos rate-limits existentes).
- **`unknown`** (qualquer falha/ambiguidade): degrada byte a byte para o comportamento atual —
  réplica passa, jogo vence, daemon NÃO repinta. Nunca pior que hoje.

Rumble, trigger effects e input passam SEMPRE, nas três autoridades — "duplicado > zero
controles" fica fora do gate por construção. Modo Nativo (`_output_mute`) permanece ACIMA do
gate nos dois sentidos (nada escrito, nem repaint — backend_pydualsense.py:2078-2080).

## O sinal "jogo real ativo" (com fail-safe explícito)

Avaliado no tick lento ~2s do lifecycle (junto de `_sync_external_leds`, lifecycle.py:1743-1758),
NUNCA no caminho quente por report. Núcleo 100% PURO: `classify(...) -> game|daemon|unknown`.

**Evidência de jogo** (qualquer uma ⇒ `game` imediato, ≤1 tick):
1. wm_class CORRENTE em foco casa `steam_app_\d+` — carimbo de tempo `game_window_seen_at`
   gravado em `record_window_detect_read` (state_store.py:163) com a regex existente
   (launch_env.py:76/92); freshness por timestamp, JAMAIS o `window_detect_last_class` sticky
   (limitação documentada em ipc_handlers.py:1111-1115 — seguraria `steam_app` após o jogo
   fechar e prenderia a autoridade em `game` para sempre).
2. wm_class corrente casa regra de perfil-por-jogo do autoswitch — cobre GOG/Heroic fora da
   Steam (lê o mesmo store, custo zero).
3. Marker `last_run` do wrapper ENRIQUECIDO: fresco (janela `WRAPPER_MARKER_WINDOW_SEC`=900s,
   launch_env.py:89) E `pid` vivo E sem `last_exit` mais novo — cobre a janela launch→janela
   (shaders/AAA), Wayland puro com wrapper, e sobrevive a restart do daemon.

**Queda para `daemon`** exige TODAS: detector de janela SAUDÁVEL com leitura fresca não-jogo +
marker ausente/pid morto/exit gravado + **30s contínuos sem evidência** (histerese — alt-tab
curto não derruba; com o merge-gate a queda é barata porque a volta é auto-curativa, ver
NUMA-02). Sem nenhuma sessão uhid aberta (agregado `game_open` dos vpads), a queda dispensa a
histerese (não há escritor de réplica a proteger). UHID_CLOSE de todos os vpads segue no caminho
existente (`end_game_session_for`, backend_pydualsense.py:1883-1950 — devolve paleta na hora,
inalterado).

**Fail-safe (assimétrico, sempre para o lado do jogo)**: detector não-saudável (Wayland puro /
backend null), OSError em qualquer leitura, marker ilegível, exceção no cômputo ⇒ `unknown` +
log `game_signal_degradado` + exposição no `state_full`/doctor com a causa. Bloquear réplica e
repintar exigem evidência POSITIVA de não-jogo. Falso-`daemon` residual (jogo invisível a todos
os ramos) custa repintura COSMÉTICA rate-limitada — nunca input/rumble/trigger.

**Vetos permanentes do sinal** (dos três juízes, unânimes): "sessão uhid aberta" JAMAIS é
evidência de jogo (é o mecanismo do incidente — o cliente também abre, medido 14:42:31; serve
apenas para modular a histerese e diagnosticar); `window_detect_last_class` sticky JAMAIS é
evidência; sonda de holders em /proc NÃO entra (vetada — subespecificada, beco 18, descartável
quando a Onda S tiver posse autoritativa dos fds).

## NUMA-01 — sinal: game_signal + marker enriquecido + store (P0)

1. `daemon/subsystems/game_signal.py` (NOVO): `classify(window_healthy, window_class_current,
   window_seen_age, profile_rule_match, marker, marker_pid_alive, exit_marker, session_open)
   -> 'game'|'daemon'|'unknown'` — função PURA com tabela-verdade testável; casca `GameSignal`
   com estado/histerese (30s, `time_fn` injetado) e telemetria INFO
   `game_signal_transition {de, para, evidencia}` a cada mudança.
2. `assets/hefesto-launch.sh`: gravar `pid=$$` no `last_run` e `last_exit` (epoch) no trap de
   EXIT — best-effort com redirect p/ /dev/null (nenhum marker jamais bloqueia o jogo; regra do
   wrapper fail-safe). `compose_env` intocado (beco 20: strip cego proibido).
3. `daemon/launch_env.py`: `read_last_run_marker` (:100-128) tolera campo `pid=` opcional
   (ausente = None, comportamento atual intacto); novas puras `read_last_exit_marker()` e
   `wrapper_game_running(marker, exit_marker, pid_alive)` ao lado de `wrapper_used_state`
   (:131-155) — nunca levantam.
4. `daemon/state_store.py`: `record_window_detect_read` (:163-183) grava também
   `window_detect_current_class` a CADA leitura (inclusive 'unknown'/None) + monotonic da
   leitura + carimbo `game_window_seen_at` quando a classe casa `steam_app` (import de
   `steam_appid_from_wm_class`, launch_env.py:92); novas properties junto de
   `window_detect_last_class` (:261-269); `set_window_detect_backend` (:147-161) zera tudo.
   Consumidores atuais do sticky intocados.
5. `daemon/lifecycle.py`: instanciar `GameSignal` junto de `_wire_external_registry`
   (:1710-1730); avaliar no tick lento via `_run_blocking` (o I/O de disco do marker mora AQUI,
   nunca no provider); property PÚBLICA `daemon.display_authority` (contrato explícito — sem
   `getattr` de privado no consumidor); injetar `self.controller.set_game_authority_provider(...)`
   guardado por `hasattr` (padrão `set_auto_output_provider`, lifecycle.py:1670) — o provider é
   leitura de bool cacheado, zero I/O (contrato de backend_pydualsense.py:530-536, roda sob
   `_io_lock`). Callbacks de transição: `*→daemon` dispara `defend_display()` (NUMA-03);
   `daemon→game|unknown` dispara `replay_retained_game_outputs()` (NUMA-02). Best-effort com
   suppress — falha de um passo não aborta o tick.

## NUMA-02 — gate de exibição no backend: merge + retain-latest (P0)

Ponto ÚNICO no backend — `uhid_gamepad.py` (máquina REPLICA-03 validada), os sinks de
`gamepad.py:285-329` e `coop.py` NÃO são tocados; único toque em `uhid_gamepad.py` é expor o
agregável read-only `game_open` (já existe como estado, :525/1097-1103) se ainda não for público.

1. `core/backend_pydualsense.py`: novo `set_game_authority_provider(fn)` + `_game_wins()` —
   espelho exato de `set_auto_output_provider` (:753-763). **Sem provider injetado ou exceção no
   provider ⇒ `True`** (fail-safe de compat: FakeController e os 3684 testes atuais passam
   byte-idênticos; a fiação real só existe no daemon).
2. `_merged_desired_for_key` (:801-803): a camada GAME só é fundida quando `_game_wins()`
   (authority ≠ 'daemon'). UM ponto governa priming (:1234), reassert de hotplug (:1224-1238),
   `reassert_resolved_outputs` (:2059-2091) e unmute (:2113-2131) de uma vez. Consequências
   provadas nos replays: (a) fechar o jogo com o cliente Steam segurando a sessão uhid (o
   UHID_CLOSE nunca vem) devolve a paleta em ≤ ~32s — a camada stale é ignorada no resolve;
   (b) daemon restart com cliente aberto: escritas do cliente durante o `unknown` inicial
   populam a camada, mas a transição para `daemon` a neutraliza no merge + `defend_display`
   repinta — o cenário que quebrava o D1 passa; (c) alt-tab além da histerese é auto-curativo —
   a camada persiste e o reassert re-honra o número do jogo na volta do foco SEM o jogo
   re-escrever.
3. `set_game_output_for` (:1841/1866-1880): com authority=='daemon', a réplica de exibição é
   **RETIDA** (retain-latest: 1 valor por (uniq, categoria) — bounded; não popula
   `_game_output_by_uniq`, não escreve hardware) + log 1x por episódio
   `game_output_retido_sem_jogo` (telemetria `uhid_replica_ativa` preservada). Novo
   `replay_retained_game_outputs()`: na abertura do gate, entrega o valor MAIS RECENTE retido
   pelo caminho normal, exatamente 1x por categoria — nenhuma escrita de jogo se perde na
   latência ~2s do sinal (FATO 0: o único `player_led` que jogos escrevem 1x). Veto honrado:
   drop sem retenção é proibido.
4. `set_rumble_for` (:1780), `set_game_trigger_for` (:1803) e `end_game_session_for`
   (:1883-1950, invalidate em :1941-1943) INTOCADOS — rumble/trigger jamais gateados; devolução
   no CLOSE continua idêntica.

## NUMA-03 — defesa: escritor estrangeiro detectado e repintado (P1)

1. `core/sysfs_leds.py` `set_rgb` (:145-177) ganha `verify: bool = False`: no cache-hit com
   `verify=True`, re-lê `get_rgb()` (:88-113 — RAM do kernel, zero subcomando HID); classe
   divergente do cache ⇒ escritor estrangeiro ⇒ invalida, REESCREVE e loga INFO
   `lightbar_escritor_estrangeiro {node, lido, esperado}` 1x por episódio com re-arme (espelho
   de `_skip_logged`, :65). **`get_rgb()` None/OSError ⇒ comporta como hoje (skip, sem log, sem
   repaint)** — veto: nó sumido em BT drop não pode virar falso estrangeiro. `verify=False` é
   byte-idêntico ao atual (regressão do flash azul de 30s do GUERRA-01 guardada por teste).
   Novos `set_players_verified(bits)` (lê brightness dos player_dirs :188-196, só escreve nos
   divergentes) e `get_players()` puro (testes/doctor). Docstring documenta a limitação: escrita
   crua por hidraw que NÃO atualiza a classe LED (fato §2 do mapa) segue invisível à re-leitura
   — cobertura parcial via `defend_display`; cura completa = Onda S.
2. `core/backend_pydualsense.py`: `reassert_resolved_outputs` (:2059-2091) ganha `verify`,
   repassado a `set_rgb`/`set_players_verified`; `verify=True` SÓ com authority=='daemon' E
   posse registrada em `_sysfs_written` (:1249-1267 — leitura sem posse nunca vira verdade,
   STATUS-01). Novo `defend_display()`: `invalidate_cache` (sysfs_leds.py:179-186) em todos os
   nós + reassert 1x — disparado (a) na transição `*→daemon` e (b) rate-limitado 1x/30s quando
   uma réplica de exibição foi RETIDA (réplica retida = prova de escritor ativo ⇒ defesa
   dirigida que alcança até o vetor hidraw-direto; no incidente, repinte ≤2s da escrita).
   NÃO é o reassert incondicional do flash azul: só em transição ou sob evidência de escritor,
   sempre rate-limitado. No-op total sob `_output_mute`; suppress por item (:2085-2090) mantém
   "falha de um device não aborta".
3. `core/external_leds.py`: nova PURA `read_player_pattern(inst, leds_root) -> slot|None` — lê
   brightness dos nós `green:player-1..4` (espelho de leitura de `write_player_number`, :65-84);
   leitura de classe LED é memória do kernel, ZERO subcomando BT (EXT-04: inventário 100% puro);
   nunca levanta. Gate humano valida com journal `[JOYCON]`; qualquer sinal de tráfego ⇒
   degradar o read-back para USB-only.
4. `daemon/subsystems/external_identity.py` `ExternalLedSync.tick` (:305-354): (a) authority
   'daemon' ⇒ antes do skip por-valor (:334-335), `read_player_pattern`; padrão ≠ slot ⇒ dirty ⇒
   reescreve DENTRO do rate-limit `LED_MIN_INTERVAL_SEC` 2s (:336-339, intocado) + log
   `external_led_repintado {uniq, intruso}`; leitura falha ⇒ skip (hoje). (b) authority
   'game'/'unknown' ⇒ NÃO corrige device já cacheado (externos não são disputados em jogo), mas
   device NOVO sem cache ainda recebe a numeração 1x (atribuição ≠ disputa — 8BitDo chegando
   mid-game não fica apagado). (c) Simetria `auto_player_colors`: tick consulta o MESMO flag do
   provider DualSense (identity.py:163-167); OFF ⇒ PARA DE AFIRMAR (zero escritas — simétrico a
   identity.py:455-456 que devolve None; sem apagar ativamente) + `_last_value.clear()`;
   OFF→ON reescreve os slots. (d) Na queda `game→daemon`, re-arm limpa `_last_value`/
   `_last_write_at` e o próximo tick reacende os slots do daemon.

## NUMA-04 — controllers.json: lock único + cross-check no load (P1)

1. `daemon/subsystems/identity.py`: lock de MÓDULO `CONTROLLERS_FILE_LOCK = threading.Lock()`
   exportado; `load` (:330-377) e `_save_locked` (:391-425) o adquirem em volta do
   read→`os.replace`. `external_identity.py` `load` (:185-222) e `_save_locked` (:231-262)
   importam e usam o MESMO lock. Fecha o lost-update dos dois escritores RMW (identity.py:243-254
   × external_identity.py:132-141) com o mínimo de superfície — daemon é singleton, um Lock de
   processo basta (`flock` inter-processo REJEITADO como sobre-engenharia; unificação estrutural
   dos registries ADIADA). Regras de domínio 100% intocadas: reserva no disconnect
   (identity.py:269-281), expiração só com sessão vazia (:283-319), vpad 02:fe rejeitado
   (:228-233), externos nunca expiram/renumeram (external_identity.py:157-176), piso DualSense
   (:293-303).
2. Cross-check UNILATERAL no load: slot presente em `slots` (DualSense) E em `externals` no
   mesmo arquivo = corrupção por lost-update pretérito ⇒ **DualSense vence; a entrada EXTERNA
   colidente é DROPADA** + log WARN `controllers_json_colisao_descartada` (o externo recebe novo
   slot na próxima atribuição, ainda com sessão vazia — D2 permite). Vetos honrados: NUNCA
   realocação de slot (política nova de renumeração proibida — juízes 1 e 3); NUNCA poda
   bilateral (as duas entradas caindo renumeraria ambos — juiz 2). Só no load com sessão vazia;
   jamais em runtime com controles conectados.

## NUMA-05 — fim do posicional + diagnóstico (P2)

1. `daemon/ipc_handlers.py` `_external_inventory` (:194-208): com `slot_resolver` PRESENTE mas
   devolvendo None (registry ainda sem opinião), `player_slot = None` — NUNCA mais o posicional
   `dualsense_count+index+1` (:207) que re-embaralhava a GUI a cada mudança de `ds_count` (null
   honesto > número errado, filosofia do `wrapper_used=None`). O posicional sobrevive SÓ quando
   `resolver is None` (daemon fake/legado — compat). Call site (:1196-1211) simplifica.
2. GUI: card de externo tolera `player_slot=None` (exibe "—"), padrão read-only de 9532eb1;
   teste sem `import gi` no topo (armadilha da CI headless — custou 4 rounds na v3.14.0).
3. `state_full` (~:550): expor `game_signal {authority, evidencia, motivo, desde, degradado}`.
   Doctor: check "autoridade de exibição" — reporta `unknown` preso com a CAUSA (Wayland
   puro/detector morto/marker ilegível) e o resultado de `get_players()`/`get_rgb()` × posse.

## Plano de testes (falha-sem / passa-com)

1. `game_signal` — tabela-verdade de `classify()` (puro, `time_fn` injetado): cada ramo de
   evidência isolado; histerese 30s (não cai antes; sobe imediato); sem sessão aberta cai sem
   histerese; detector não-saudável ⇒ `unknown`; OSError em qualquer fonte ⇒ `unknown`;
   **sessão-uhid-aberta sozinha NÃO é evidência** (anti-regressão do incidente); **sticky
   `last_class` com corrente vazio NÃO é evidência** (falha-sem: prenderia `game` p/ sempre).
2. GATE-MERGE (falha-sem): camada GAME gravada + authority 'daemon' ⇒ merged SEM led/player_leds
   do jogo (no HEAD contém — falha); 'game'/'unknown'/provider levantando/sem provider ⇒ contém.
3. GATE-RETAIN (falha-sem): `set_game_output_for` com 'daemon' ⇒ `_game_output_by_uniq` vazio,
   nó fake sem escrita, log 1x/episódio; retenção bounded (1 valor/categoria — 100 escritas
   retêm só a última); abertura do gate ⇒ replay entrega o MAIS RECENTE exatamente 1x (falha-sem
   no HEAD: entrega tudo na hora; falha no drop-puro: perde a escrita única — FATO 0).
4. COMPAT-DEFAULT: backend SEM `set_game_authority_provider` ⇒ suíte REPLICA-03 inteira passa
   INALTERADA (3684 testes, zero churn).
5. FAIL-SAFE-RUMBLE: `set_rumble_for`/`set_game_trigger_for` aplicam nas TRÊS autoridades
   (guarda contra alguém gatear categoria de gameplay no futuro).
6. SYSFS-FOREIGN (replay direto do incidente, falha-sem): LEDS_ROOT fake, `set_rgb(0,0,255)`;
   mutar `multi_intensity` p/ `0 64 0` por fora; `set_rgb(0,0,255)` com `verify=True` ⇒
   REESCREVE + loga (no HEAD: skip silencioso — falha). `get_rgb()` None/OSError ⇒ skip sem log
   (veto do falso estrangeiro em BT drop). `verify=False` byte-idêntico (regressão flash azul).
7. `set_players_verified` só escreve nos brightness divergentes; `get_players()` puro.
8. DEFEND-DISPLAY: transição `*→daemon` ⇒ invalidate+reassert 1x; réplica retida ⇒ disparo
   rate-limitado 1x/30s; no-op sob `_output_mute` (Modo Nativo); `verify` só com posse em
   `_sysfs_written`; falha de um nó não aborta os demais.
9. EXT-FOREIGN (falha-sem): brightness mutado por fora + 'daemon' ⇒ repinta após ≥2s + log;
   <2s NÃO escreve (contagem de escritas asserta EXT-04); leitura falha ⇒ skip; 'game' ⇒ não
   corrige cacheado MAS numera device novo 1x.
10. EXT-AUTO-OFF (falha-sem): OFF ⇒ zero escritas externas + cache limpo (no HEAD: externo
    continuava aceso com DualSense apagado — falha); OFF→ON reescreve.
11. POSICIONAL (falha-sem): resolver presente devolvendo None ⇒ `player_slot=None` estável sob
    `ds_count` 1→0 (no HEAD: `ds_count+index+1` re-embaralha — falha); resolver ausente ⇒
    posicional legado; card GUI renderiza None sem exceção (gi tardio).
12. CONTROLLERS-LOCK (falha-sem, DETERMINIZADO por monkeypatch em `os.replace`/barrier — sem
    corrida real de threads na CI): RMW intercalado dos dois registries ⇒ ambos os namespaces
    sobrevivem (no HEAD um some); load com colisão slots×externals ⇒ entrada EXTERNA dropada +
    WARN, DualSense intacto, NENHUMA realocação; arquivo saneado no próximo save.
13. MARKER: `wrapper_game_running` (pid vivo/morto, `last_exit` mais novo/velho, arquivo com
    lixo ⇒ nunca levanta); wrapper grava `pid`/`last_exit` best-effort e o jogo lança mesmo com
    diretório ilegível.
14. STORE-SINAL: `record_window_detect_read` carimba `game_window_seen_at` p/ `steam_app_*` e
    grava `window_detect_current_class` a CADA leitura (inclusive 'unknown');
    `set_window_detect_backend` zera.
15. REPLAY-INTEGRADO (FakeController + vpad fake): (a) incidente 14:42 — OPEN do cliente +
    writes de exibição com 'daemon' ⇒ físico mantém paleta, camada GAME vazia, retenção logada;
    (b) FATO 0 — jogo escreve player_led 1x ANTES da evidência; janela ganha foco ⇒ replay
    entrega o número do jogo; (c) restart com cliente aberto — `unknown` inicial deixa passar,
    transição p/ 'daemon' neutraliza a camada no merge + defend_display repinta; (d) fechar jogo
    com cliente segurando a sessão ⇒ paleta volta ≤ ~32s sem UHID_CLOSE.
16. Gate da casa: `pytest tests/` completo com **0 skipped**, ruff 0.15.20, mypy,
    check_anonymity; nenhum teste novo importa gi no topo.

## Critérios de aceite

1. **Replay do incidente** (integração, teste 15a + gate humano): cliente Steam aberto sem jogo
   ⇒ DualSense branco PERMANECE azul/player-1; camada GAME nunca nasce; escrita estrangeira na
   classe LED repintada em ≤2s (defend_display dirigido) — no máximo um piscar; padrão de player
   rabiscado no Pro/8BitDo repintado no tick seguinte (≥2s, EXT-04); UM único "player 3" visível.
2. **Jogo real** (REPLICA-03): evidência ⇒ 'game' em ≤1 tick; valores retidos entregues 1x;
   escritas do jogo fluem; DualSense exibem o número DO JOGO; externos sem disputa; UHID_CLOSE
   devolve paleta na hora (caminho existente); fechar jogo com cliente vivo devolve em ≤ ~32s.
3. **Degradação**: Wayland puro/detector morto ⇒ `unknown` = comportamento atual, visível no
   doctor com causa; erro de leitura nunca propaga; rumble/input intocados em QUALQUER estado.
4. **Persistência**: lost-update irreproduzível com o lock único; colisão em disco reparada no
   load (drop da externa + WARN); GUI sem números posicionais re-embaralhados.
5. Gates automáticos: pytest 0 skipped + ruff 0.15.20 + mypy + check_anonymity verdes.
6. Gates humanos (mantenedora): (a) abrir cliente Steam sem jogo e conferir branco azul +
   8BitDo único player-3; (b) Sackboy com gyro/rumble (convivência gate × forward_motion sob
   carga); (c) fechar o jogo com a Steam viva e cronometrar a volta da paleta; (d) journal
   `[JOYCON]` limpo durante o read-back dos externos (se houver tráfego ⇒ read-back USB-only).

## Riscos e rollback

- **Jogo invisível ao sinal** (nativo sem wrapper com detector saudável-mas-cego): 'daemon'
  durante jogo real ⇒ repintura cosmética rate-limitada (nunca input/rumble). Mitigações:
  fail-safe `unknown` p/ detector não-saudável, marker como 2ª evidência, histerese, launch
  option padrão `hefesto-launch %command%`. Knob de campo: alargar a histerese — NUNCA gatear
  mais categorias.
- **Vetor hidraw-direto no físico** segue invisível à re-leitura de classe (fato §2 do mapa):
  coberto parcialmente pelo defend_display (transição + réplica retida); cura completa = broker
  fd-injection (Onda S). NÃO antecipar broker/ACL/chmod aqui (beco 10).
- **Retain-latest entrega o último valor do CLIENTE na subida** — aceito: cliente e jogo
  compartilham a numeração do Steam Input e o jogo sobrescreve em seguida. Não limpar a
  pendência na subida (perderia a escrita única do FATO 0).
- **Pid reuse no marker** (falso `pid vivo` até 900s): raro e limitado pela janela; `last_exit`
  encurta na prática. Não endurecer sem medição.
- **Flip-flop em alt-tab >30s**: auto-curativo (camada GAME persistente + merge-gate re-honra na
  volta); custo = ≤1 escrita/2s externos, reassert rate-limitado DualSense.
- **Rollback**: sem o provider injetado o backend é HEAD byte-idêntico — desligar a onda inteira
  = remover 1 linha de fiação no lifecycle; NUMA-01..05 são independentes e revertíveis um a um;
  `verify` e read-back nascem atrás de flags de chamada (default False/ausente).

## Fora desta onda (explícito, com destino)

- Broker fd-injection / posse autoritativa dos fds / esconder hidraw ⇒ **Onda S** (parkado,
  9 HIGH conhecidos).
- Incidente WiFi×BT (dongle T3U derruba os BT; topologia xHCI) ⇒ **Onda R**.
- Sonda de holders em /proc ⇒ **VETADA** nesta onda (beco 18); reavaliar só se a Onda S não
  entregar posse autoritativa.
- Unificação estrutural dos dois registries (classe/arquivo único) ⇒ onda futura; aqui só lock
  compartilhado + cross-check no load. `flock` inter-processo idem (singleton dispensa).
- Número do jogo para EXTERNOS ⇒ decidir com medição ao vivo de jogo numerando externos.
- Enable-IMU do Nintendo real (GYRO-02) ⇒ faseado (doc de risco + protótipo por cabo).
- Scrub de MACs nos .jsonl ⇒ pendência da mantenedora.
- Keepalive/0x31 BT, recriação de vpad mid-game, âncora em CONTROLLER_CONNECTED, LED via
  pydualsense em BT (LIGHTBAR-BT-NEVER-01) ⇒ intocáveis, não são desta onda nem de nenhuma.

## Registro de síntese — vetos dos juízes honrados

1. D1/camada GAME órfã no restart ⇒ resolvido pelo merge-gate (NUMA-02.2) — a camada stale é
   neutralizada no resolve, não defendida.
2. D0/replay "histerese ⇒ repaint-all devolve azul" falso sob camada stale ⇒ idem: o merge-gate
   torna o repaint verdadeiro.
3. D2/drop sem retenção ⇒ retain-latest + replay obrigatórios (NUMA-02.3).
4. D2/sinal binário sem degradação ⇒ estado `unknown` = comportamento atual (NUMA-01.1).
5. D2/`get_rgb()` None vira falso estrangeiro ⇒ regra explícita: falha de leitura = hoje
   (NUMA-03.1).
6. D1/sonda de holders por identidade de processo ⇒ NÃO entra (fora desta onda).
7. D0/realocação de slot no reparo de colisão ⇒ drop unilateral da entrada externa; D2/poda
   bilateral ⇒ idem, DualSense vence (NUMA-04.2).
8. Transversais: sessão uhid jamais é evidência; sticky jamais é evidência; rumble/trigger jamais
   gateados; nada de sonda por tick; nada de reassert incondicional fora de
   transição/evidência-de-escritor.
