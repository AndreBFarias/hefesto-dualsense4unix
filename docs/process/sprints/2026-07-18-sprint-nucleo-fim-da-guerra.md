# Sprint NÚCLEO 2026-07-18 — Fim da guerra de escritores (GUERRA-01 · BTREPORT-02 · REPLICA-03)

> Causa-raiz e evidências: `docs/process/estudos/2026-07-18-estudo-guerra-de-escritores-hidraw.md`.
> Tudo aqui é P0. Ordem interna: GUERRA-01 itens 1-2 → BTREPORT-02 → REPLICA-03 → GUERRA-01 item 3.

## GUERRA-01 — o jogo para de enxergar (e de escrever n)o físico

### Item 1 — envs Proton modernas (`daemon/launch_env.py` + `assets/hefesto-launch.sh`)
- `compose_env()` (launch_env.py:71-106): flavor dualsense+uhid passa a emitir
  `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` no lugar de `PROTON_ENABLE_HIDRAW=1`, mantendo
  `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`. NUNCA incluir 0x0DF2 no DISABLE (o vpad
  precisa do hidraw — é por ele que triggers/rumble/lightbar do jogo chegam).
  Racional binário: winebus.sys dos Protons 10/11 lê PROTON_DISABLE_HIDRAW (lista VID/PID);
  a whitelist default já dá hidraw ao Edge 0df2. PROTON_ENABLE_HIDRAW morreu no Proton 10.
- Modo Nativo (`native`): manter o comportamento de expor o físico (sem DISABLE, sem IGNORE).
- Máscara xbox: manter `SDL_JOYSTICK_HIDAPI=0` + IGNORE e ADICIONAR o DISABLE dos físicos
  (o vazamento winebus vale para qualquer máscara).
- Allowlist do wrapper (`assets/hefesto-launch.sh:84-92`) e espelho (`launch_env.py:58-64`):
  trocar `PROTON_ENABLE_HIDRAW` por `PROTON_DISABLE_HIDRAW`.
- Migração: `materialize_launch_env()` regrava os .env → nada persistente a migrar; conferir
  que nenhum outro ponto emite PROTON_ENABLE_HIDRAW (grep).

### Item 2 — keepalive neutro no report_thread (`core/backend_pydualsense.py`)
Problema: `_PinnedPyDualSense.sendReport` (L262-303) reescreve report com `flag0=0xFF`
(bits de vibração SEMPRE ligados) e motores=0 → zera rumble de terceiros a cada ≤0.5s.
- No override `prepareReport` (L305-339): quando NÃO há rumble nosso ativo (motores desejados
  == 0 e sem transição pendente ativa→0), LIMPAR os bits de vibração do flag0 (0x01|0x02 e o
  bit de atenuação v2 se aplicável) — report vira neutro, firmware mantém estado anterior.
- Estado novo `_rumble_dirty`: `setLeftMotor/setRightMotor` (via `set_rumble_for`) marca;
  a transição para 0 envia UM report com flags ligados (para parar o motor de verdade) e então
  volta ao neutro. Cuidado com o dedup `_last_out_report` (o report neutro difere do ativo).
- Vale para USB (0x02) e BT (0x31) — offsets de flag0 diferem ([1] USB, [3] BT pós-fix).
- NÃO tocar na supressão de LED existente (flags 0x04|0x10) — ela continua.

### Item 3 — reassert de LED com cache (`core/sysfs_leds.py` + `core/backend_pydualsense.py`)
- `SysfsLedNode.set_rgb` (sysfs_leds.py:137-150): cache por instância do último (rgb, brightness)
  escrito; skip silencioso se igual. Nó recriado (wake/adoção BT) = instância nova = escreve.
- Resultado: `reassert_resolved_outputs()` (backend:1600-1631) continua rodando a cada
  reconciliação, mas só GERA output report quando a cor resolvida MUDA — o "flash azul de 30s"
  morre. Método `invalidate_cache()` para os casos de posse retomada (ex.: fim do REPLICA-03).
- Telemetria: 1 log INFO `lightbar_reassert_skip_cache` na primeira vez que o cache pega (por nó),
  para o journal provar a cura.

## BTREPORT-02 — o report 0x31 correto (rumble/triggers/lightbar BT de verdade)

Problema: pydualsense 0.7.5 monta o 0x31 MALFORMADO ([1]=0x02 fixo em vez de seq<<4; [2]=0xFF
em vez do tag 0x10) → firmware descarta → nosso caminho de output BT inteiro é no-op (o rumble
"perfeito" do roxo vinha do jogo escrevendo direto — canal que GUERRA-01 fecha).
- No override `_PinnedPyDualSense.prepareReport` (backend_pydualsense.py:305-339): quando
  transporte BT, MONTAR o buffer correto nós mesmos: `[0]=0x31, [1]=seq<<4, [2]=0x10 (tag),
  [3..]=payload comum do 0x02 (flags/motores/LED/triggers), CRC32 nos 4 últimos bytes` —
  aproveitar o gerador/CRC de `core/lightbar_reset.py:41-77` (extrair helper comum, ex.:
  `core/ds_output_report.py`, para reset e report normal usarem o mesmo builder).
- Sequence number: contador por handle (wrap 0-15), como o hid_playstation faz.
- O keepalive neutro do GUERRA-01 item 2 se aplica IGUAL por BT (agora que o report cola).
- Validar contra o layout do kernel (`drivers/hid/hid-playstation.c`, struct
  dualsense_output_report_bt): offsets exatos, não confiar na pydualsense.
- Teste: builder puro com vetores conhecidos (CRC de referência calculado no teste), USB e BT.

## REPLICA-03 — o output do jogo chega ao físico (a experiência PS5 completa)

Hoje `uhid_gamepad._handle_output` (integrations/uhid_gamepad.py:856-878) parseia SÓ rumble e
DESCARTA o resto do report que o jogo manda ao vpad. Com GUERRA-01 o jogo só fala com o vpad —
replicar o output inteiro ao físico correspondente:
1. **Gatilhos adaptativos**: parsear os blocos de trigger effect do report 0x02 do Edge
   (valid_flag0 bits dos triggers R/L; modos+parâmetros) e aplicar ao físico via backend
   (rota raw existente de triggers por perfil). Política de posse: efeito do JOGO vence o
   perfil enquanto a sessão uhid estiver aberta (fd do jogo aberto = `UHID_OPEN`..`UHID_CLOSE`);
   no CLOSE, reaplicar o perfil.
2. **Lightbar**: valid_flag1 LIGHTBAR_CONTROL_ENABLE → aplicar cor do jogo ao físico (rota
   sysfs normal), como camada "game" acima da paleta por slot no merge de desired
   (`_merged_desired_for_key`, backend:518-551). No CLOSE da sessão, camada some e a paleta
   volta (usar `invalidate_cache()` do GUERRA-01 item 3).
3. **Player-LEDs**: valid_flag1 PLAYER_INDICATOR → replicar aos white:player-N do físico via
   sysfs (rota do co-op `_apply_coop_player_leds`). Assim o NÚMERO NO CONTROLE = o número que o
   JOGO atribuiu (cura P3 para DualSense por construção). No CLOSE, volta o player_index do co-op.
4. **Telemetria**: expor no state_full contadores POR VPAD (`ff_play_count`, `output_count`,
   novos `trigger_replicas`, `lightbar_replicas`, `player_led_replicas`) — hoje o agregado
   esconde qual vpad recebeu o quê (ipc_handlers.py:703-716).
5. Aplicar em AMBOS os vpads (P1 via dispatch_gamepad, P2+ via coop tick) — o sink de replicação
   deve resolver o físico-alvo como o rumble já faz (primary_uniq / identity do coop).
6. Segurança: rate-limit interno (não repassar mais que ~250 Hz por categoria; dedup por valor)
   para não saturar o report_thread nem o rádio BT.

## Testes exigidos (todos herméticos, rodam na CI)
- launch_env: compose/materialize com PROTON_DISABLE_HIDRAW; allowlist do wrapper (shell test já
  existe — `tests/unit/test_hefesto_launch_wrapper.py` + `test_launch_env.py`).
- Builder de report USB/BT com CRC de referência; seq wrap; keepalive neutro (flags OFF em idle,
  ON em rumble ativo, transição ativa→0 emite um report com flags).
- pump_ff/_handle_output: parse de triggers/lightbar/player-LED com reports sintéticos do Edge;
  posse jogo-vence/CLOSE-devolve; contadores por vpad no state_full.
- sysfs cache: segunda escrita igual não toca o filesystem (tmpfs fake dos testes existentes).

## Gate de aceite ao vivo (eu, Claude, valido via sudo — sem esperar o jogo)
- Escrever report 0x02 de rumble no hidraw do vpad P1 (simulando o jogo) → o físico BRANCO USB
  deve vibrar; idem trigger effect e lightbar; player-LED 2 no vpad → físico mostra 2.
- journal: `lightbar_reassert_skip_cache` presente; ZERO flash azul periódico no sysfs mtime.
- launch_env/*.env com PROTON_DISABLE_HIDRAW=0x054C/0x0CE6 e SEM PROTON_ENABLE_HIDRAW.
