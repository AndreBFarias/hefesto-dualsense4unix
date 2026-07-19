# Agente: v2:f968e52c3707e5f0480439efc1d393c7bd0068134327590847ce144ec2fa8622

## report

## Caminho COMPLETO do rumble/FF (função-por-função, com linhas)

### 1. Jogo → vpad UHID
O jogo escreve o report de output 0x02 no hidraw do vpad (Edge 054c:0df2; P1=/dev/hidraw6, P2=/dev/hidraw8), diretamente (HIDAPI/libScePad/wine-hid) ou via FF de evdev (aí o hid_playstation do kernel monta o 0x02 e ele desce pro uhid). O kernel entrega como evento UHID_OUTPUT no fd de /dev/uhid do daemon.

### 2. Daemon drena o UHID_OUTPUT
- `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`:
  - `pump_ff()` L811-836 — drena até 64 eventos/tick (`_MAX_EVENTS_PER_PUMP` L153), non-blocking.
  - Chamado a cada tick do poll loop: P1 via `dispatch_gamepad` (`daemon/subsystems/gamepad.py` L598-626, chamado de `daemon/lifecycle.py` L1771→L1380-1384); P2..N via tick do coop (`daemon/subsystems/coop.py` L756-760).
  - `_handle_event()` L838-854: UHID_START/STOP/CLOSE (CLOSE → `_silence_rumble()` L616-625) e UHID_OUTPUT → `_handle_output()`.
  - `_handle_output()` L856-878: exige `report[0] == 0x02` (`_OUTPUT_REPORT_USB` L128, gate L864); gate de flags `body[0] & 0x03` (`_VIBRATION_FLAGS` L150 — máscara 0x01|0x02 por causa do vibration_v2 de fw>=0x0215, comentário L146-149); weak=body[2], strong=body[3] (L133-135); dedup contra `_last_sent` L875; `_emit_rumble()` L880-886 → `rumble_sink(weak, strong)`.

### 3. Sinks (quem mira o físico)
- P1: `make_primary_rumble_sink` (`gamepad.py` L371-389) — resolve `daemon.controller.primary_uniq` NA HORA → `apply_game_rumble(target_uniq=uniq)`.
- P2+: `CoopManager._make_player_rumble_sink(identity)` (`coop.py` L388-407) — `target_uniq` = MAC do jogador.
- `apply_game_rumble` (`gamepad.py` L159-207): early-return se `rumble_active is not None` (L186-187; ao vivo = None, não é o caso); política global `_game_rumble_mult` L127-156 (ao vivo: policy=max, mult=0.7); `set_rumble_for(target,...)` L195-202; fallback broadcast `set_rumble` L204-207.

### 4. Backend → controle físico
- `core/backend_pydualsense.py`:
  - `set_rumble_for()` L1478-1501: `_key_to_uniq`/`_key_for_uniq` → handle → `handle.setLeftMotor(strong)/setRightMotor(weak)` (só seta estado em memória).
  - `set_rumble()` L1305-1312 (broadcast via `_for_each` L1118-1159; respeita `_output_target_key`).
  - Escrita HID real: report_thread `_PinnedPyDualSense.sendReport()` L262-303 — read input hidapi → `prepareReport()` → write só se `out != self._last_out_report` OU keepalive 0.5s (`OUT_REPORT_KEEPALIVE_SEC` L130) → `writeReport(out)` → sleep `_throttle_sec` (0.008×N, cap 0.032; L115-123, ajustado em `connect()` L741-747). `_output_muted` (Modo Nativo) zera writes (L278) — ao vivo False.
  - hidapi = backend hidraw (`.venv/.../hidapi.py` L136-138 prefere libhidapi-hidraw.so): write vai em /dev/hidrawN, sem detach de driver.

### 5. Report USB vs BT (pydualsense 0.7.5, `.venv/.../pydualsense/pydualsense.py`)
- USB (L527-541): [0]=0x02, [1]=flag0=0xFF (bits de vibração 0x01|0x02 SEMPRE ligados), [2]=flag1=0x57, [3]=rightMotor(weak), [4]=leftMotor(strong). Sem seq, sem CRC.
- BT (L581-605): MALFORMADO off-by-one — [0]=0x31, [1]=0x02 fixo (deveria ser seq<<4), [2]=0xFF (deveria ser o tag 0x10 obrigatório), [3]=flags, [4]/[5]=motores, CRC em [74..77]. O firmware DESCARTA em grande parte esse report (é o motivo documentado de "cor nunca funcionou por BT", `_refresh_sysfs_leds` L928-936).
- O kernel hid_playstation monta os dois formatos CORRETOS (é a rota do sysfs LED e do FF de evdev de terceiros).

### 6. Auditoria do 62483b2 (supressão/reset) — INOCENTE para o rumble
- `_suppress_leds` nasce True (`__init__` L241, racional L223-240).
- `_refresh_sysfs_leds()` L854-943: mantém True se coberto por sysfs OU transporte BT (L937-943, política LIGHTBAR-BT-NEVER-01).
- `prepareReport()` override L305-339: limpa SÓ 0x04|0x10 no byte de flags de LED (idx 2 USB / idx 3 BT, L326-328); flag0/motores INTOCADOS; recalcula CRC BT L329-336. Não engole rumble.
- `send_release_leds` (`core/lightbar_reset.py` L41-77): report 0x31 bem-formado com flag1=0x08 e todo o resto ZERADO; enviado SÓ em BT na adoção (`connect()` L760-768). Nunca toca o caminho USB.

### 7. Adoção do físico quando o vpad sobe
- `connect()` L670-790 (tick de hotplug do reconnect_loop, `daemon/connection.py` L196-236: 30s online + imediato em mudança de /dev/input): `_enumerate_device_keys` L592-621 (hidapi enumerate 054c, vpad excluído por `_is_virtual_hidraw` L68-93), `_open_one` L623-666 (init com timeout 5s), reset BT L760-768, `_refresh_sysfs_leds` L774, `_reapply_desired` L776-777, `reassert_resolved_outputs` L790 (implementação L1600-1631 — reescreve a cor resolvida via sysfs A CADA reconciliação).
- Grab: `_set_controller_grab` (`gamepad.py` L543) → `EvdevReader.set_grab` (`core/evdev_reader.py` L583-620, EVIOCGRAB). **O grab cobre SÓ evdev; o hidraw do físico continua aberto para qualquer processo** (sem exclusividade no kernel).

## EVIDÊNCIA AO VIVO (2026-07-18 20:40-20:45, tudo read-only)

1. `daemon.state_full` via IPC: `rumble_ff.plays=19` (o jogo ENVIOU FF aos vpads), `vpads=2`, `backend=uhid`, `degraded=false`, `dedup_ok=true`, `rumble_passthrough=True`, `rumble_active=None`, policy=max mult=0.7. `controller.list`: branco USB `<MAC-DS-BRANCO>` primário, roxo BT `<MAC-DS-ROXO>`.
2. Threads do daemon (PID 2469): os DOIS report_threads VIVOS (tids 2929/5039, wchan=hrtimer_nanosleep = sleep do throttle, utime avançando 2239→2241 e 2589→2592 em 3s). O caminho de escrita do daemon para o branco está SAUDÁVEL.
3. **lsof (o smoking gun)**: `steam` (PID 6034) segura `/dev/hidraw3` (o FÍSICO branco USB!), hidraw7 (roxo físico BT), hidraw2 (Pro Controller), hidraw8 (vpad P2). `winedevice` (PID 7347, o jogo Proton) segura hidraw2, **hidraw3**, hidraw6 (vpad P1), **hidraw7**, hidraw8 — TODOS, incluindo os dois físicos 054c:0ce6, APESAR do `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` gravado nos envs (`~/.local/state/hefesto-dualsense4unix/launch_env/default.env` e `steam_app_1599660.env`, ambos também com `PROTON_ENABLE_HIDRAW=1` — composição em `daemon/launch_env.py` `compose_env` L100-102).
4. Lightbar do branco via sysfs (`/sys/class/leds/input9:rgb:indicator/multi_intensity`) lê `0 0 153` (o AZUL do daemon) estável — enquanto a usuária via VERDE-LIMÃO no hardware: o escritor do verde NÃO passa pela classe LED do kernel (sysfs fica stale) = escrita direta no hidraw3 por steam/winedevice. O "alterna para azul e volta" bate com o reassert de 30s do reconnect_loop (`reassert_resolved_outputs`).
5. Journal: branco adotado 19:59:48 (`controller_primary_bound transport=usb`, `sysfs_led_cobertura cobertos=['<MAC-DS-BRANCO>']`); roxo adotado 20:00:47 com `lightbar_reset_enviado` + `coop_player_added player=2`; ZERO `output_handle_failed`/`game_rumble_failed`/`uhid_rumble_sink_failed` hoje.

## CAUSA-RAIZ (P1: rumble não chega no branco USB + lightbar verde-limãoazul)

`PROTON_ENABLE_HIDRAW=1` (que o próprio `compose_env` emite JUNTO com o IGNORE no flavor dualsense/uhid) faz o winebus do Proton usar o backend **hidraw** para devices Sony — e esse backend **não honra `SDL_GAMECONTROLLER_IGNORE_DEVICES`** (conceito só de SDL). O físico branco ressuscita DENTRO do jogo via hidraw3: o jogo o vê como um controle EXTRA (o "player 3/4" do problema P2) e escreve nele reports 0x02 padrão (cor de slot verde + motores=0 **com os valid_flags de vibração ligados** — pacote DS5 típico). O rumble do DualSense é one-shot last-writer-wins: cada write de terceiro com motores=0 CANCELA o rumble que a cadeia do daemon acabou de escrever. Simetricamente, o keepalive de 0.5s do nosso report_thread (motores 0 + flags de LED suprimidos) mata qualquer rumble que o jogo escreva direto no hidraw3. Guerra de 3 escritores no hidraw3 → o branco nunca vibra e a lightbar oscila verde(jogo/Steam)azul(reassert 30s do daemon).

**Por que o roxo BT vibra:** o jogo fala DIRETO com o roxo via /dev/hidraw7 (input+rumble — EVIOCGRAB não cobre hidraw) com reports 0x31 BEM-FORMADOS; o escritor concorrente do daemon em BT é o 0x31 MALFORMADO da pydualsense 0.7.5, que o firmware descarta (evidência histórica: "cor via pydualsense nunca funcionou por BT"). Em BT há na prática UM escritor válido (o jogo) → rumble cola. E a cor de slot 2 do jogo (vermelho) COINCIDE com o vermelho P2 da paleta do daemon → nenhuma briga visível no roxo. Em USB os nossos reports são bem-formados → a guerra é real e ninguém vence.

## key_files

- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:76, 128-150, 811-886, 616-625 — Recepção do FF do jogo: pump_ff/_handle_event/_handle_output (gate report 0x02 + máscara 0x03 de vibração) → _emit_rumble → rumble_sink; _silence_rumble no STOP/CLOSE
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:127-207, 371-389, 453-552, 598-626 — apply_game_rumble (política+targeting por MAC), make_primary_rumble_sink (P1→primary_uniq), start_gamepad_emulation (cria vpad com o sink, L504-509), dispatch_gamepad (bombeia pump_ff por tick)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/coop.py:388-427, 756-760 — Sink por jogador do co-op (_make_player_rumble_sink → apply_game_rumble por MAC), _promote_player (vpad P2), pump_ff do co-op por tick
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/core/backend_pydualsense.py:68-93, 103-130, 203-339, 592-790, 854-943, 1118-1159, 1305-1312, 1478-1501, 1600-1631 — Escrita física: set_rumble_for/set_rumble → setLeft/RightMotor → sendReport (throttle+dirty-flag+keepalive 0.5s = o NOSSO escritor concorrente); prepareReport com supressão de LED (62483b2, inocente p/ rumble); adoção connect() + _is_virtual_hidraw + reset BT 0x08; reassert de cor a cada reconciliação (o 'azul que volta')
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/launch_env.py:58-106 — compose_env L100-102: flavor dualsense/uhid emite PROTON_ENABLE_HIDRAW=1 JUNTO do IGNORE — o PROTON_ENABLE_HIDRAW ressuscita os físicos no winebus-hidraw e derrota o dedup (raiz de P1 e P2); envs materializados confirmados em ~/.local/state/hefesto-dualsense4unix/launch_env/*.env
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/.venv/lib/python3.12/site-packages/pydualsense/pydualsense.py:527-541, 581-605 — Layout dos reports: USB correto ([1]=0xFF flags, motores [3]/[4]); BT malformado off-by-one (por que o daemon é escritor no-op em BT e o jogo vence sozinho no roxo)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/core/lightbar_reset.py:41-77 — Reset LED state 0x08 do 62483b2: BT-only, flags zerados, não toca rumble — auditado e inocente
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/connection.py:196-236 — Cadência da reconciliação (30s online + imediato em mudança de /dev/input) = período do 'volta pro azul' da lightbar
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/ipc_handlers.py:595-724 — state_full: rumble_ff.plays é AGREGADO (L703-716) — não dá para separar FF do P1 vs P2; candidato a expor por-vpad para diagnóstico
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/core/evdev_reader.py:583-620 — EVIOCGRAB do físico — cobre SÓ evdev; hidraw do físico permanece aberto/escrevível por steam/winedevice (a brecha explorada pela guerra de escritores)

## hypotheses

- H1 (ALTA, evidência ao vivo): guerra de múltiplos escritores no /dev/hidraw3 do branco USB — winedevice PID 7347 (via PROTON_ENABLE_HIDRAW=1, que ignora SDL_GAMECONTROLLER_IGNORE_DEVICES) + steam PID 6034 escrevem reports 0x02 com valid_flags de vibração ligados e motores=0 (cor de slot + keepalive), cancelando o rumble one-shot que o daemon escreve; o keepalive de 0.5s do daemon (backend_pydualsense.py L288-294) cancela na volta o que o jogo escrever. Provado por lsof (ambos seguram hidraw3) + rumble_ff.plays=19 (FF chegou aos vpads) + report_threads vivos + zero erros no journal.
- H1b (ALTA, mesmo mecanismo): a lightbar verde-limãoazul do branco é a mesma guerra — verde = cor de slot do jogo/Steam escrita DIRETO no hidraw3 (bypassa a classe LED do kernel: sysfs lia '0 0 153' azul enquanto o hardware mostrava verde), azul = reassert do daemon a cada ~30s (reconnect_loop → reassert_resolved_outputs backend L790/L1600-1631).
- H2 (ALTA, explica a assimetria USB×BT): o roxo BT vibra porque o jogo fala direto com ele via hidraw7 com reports 0x31 bem-formados, e o escritor concorrente do daemon em BT é o 0x31 MALFORMADO da pydualsense 0.7.5 ([1]=0x02 fixo, [2]=0xFF sem o tag 0x10 — .venv pydualsense.py L581-605) que o firmware descarta → um escritor só. A cor vermelha do slot 2 do jogo coincide com o vermelho P2 do daemon, escondendo a briga no roxo.
- H3 (REFUTADA em código): a supressão do 62483b2 NÃO engole o rumble — prepareReport (backend L305-339) limpa só 0x04|0x10 do byte de flags de LED; flag0 (0xFF, vibração) e motores intocados; send_release_leds é BT-only e zera todos os outros flags.
- H4 (REFUTADA ao vivo): report_thread do branco morto — os dois report_threads acumulam utime (tids 2929/5039); handles conectados; sem output_handle_failed no journal.
- H5 (REFUTADA ao vivo): rumble fixado/mute — rumble_active=None (passthrough), native=False, _output_muted=False; mult=0.7 atenua mas não zera.

## open_questions

- Quanto dos rumble_ff.plays=19 é do vpad P1 vs P2? O contador é agregado (ipc_handlers.py L703-716); expor ff_play_count POR vpad no state_full discriminaria 'FF do P1 chegou e foi pisoteado' vs 'o jogo rumbleia o branco direto no hidraw3 e o NOSSO keepalive pisoteia'. Nas duas variantes a guerra de escritores é a causa, mas o fix ideal muda (esconder o físico do jogo vs suspender nosso keepalive).
- Cadência e conteúdo exatos dos writes de steam (6034) e winedevice (7347) no hidraw3 — um strace/usbmon curto DURANTE gameplay confirmaria motores=0+flags de vibração e a origem exata do verde-limão (Steam Input slot color vs SDL do jogo). Não rodei strace para não perturbar a sessão ao vivo.
- O Steam Input está ativo para PS neste install? steam segura hidraw3/7 — se PSSupport estiver ligado no localconfig.vdf, o Steam é um TERCEIRO escritor mesmo fora do Proton (e explica writes fora do jogo).
- Fix candidato principal a validar: NÃO emitir PROTON_ENABLE_HIDRAW=1 junto do IGNORE (compose_env L100-102) — o vpad Edge tem hidraw real e o winebus-SDL o enxerga; OU restringir por udev/ACL o hidraw do físico 0ce6 adotado (análogo hidraw do EVIOCGRAB). Precisa checar se o winebus-hidraw enxerga o vpad uhid sem PROTON_ENABLE_HIDRAW.
- O winedevice também segura hidraw6/8 (vpads) — com hidraw backend o jogo pode ver 5 controles (2 físicos + 2 vpads + Nintendo), o que alimenta diretamente o P3 (numeração global do daemon nunca vai bater com a enumeração do jogo enquanto os físicos vazarem).
