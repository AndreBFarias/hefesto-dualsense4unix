# Triagem Onda U — 13 sintomas de GUI (read-only, 2026-07-20)

> Investigação read-only pós-Onda-N/R. Descoberta central: **Causa A** — root cause de código
> NOVA, não coberta pela Onda N, que sozinha explica U3+U4+U9(parte)+U11. Backlog no fim.

## Causa A (a maior alavanca) — falta de trava manual nos IPCs de aplicação

`ipc_draft_applier.py:40-54` (`DraftApplier.apply`): cada seção só roda se a chave estiver
presente; o `mark_manual_trigger_active()` que suprime o autoswitch está DENTRO de
`_apply_triggers` (`:217`), não no topo de `apply()`. O rodapé "Aplicar" global sempre inclui a
seção `triggers` → arma a trava por acidente. Mas o "Aplicar no controle" da aba Lightbar
(`lightbar_actions.py:241-266`) manda `{"leds": {...}}` SEM triggers → nenhuma trava → o
`AutoSwitcher` (`autoswitch.py:158-176,219-228`) reativa o perfil ATIVO no próximo tick com
mudança de foco de janela, e `ProfileManager.apply()` (`profiles/manager.py:171-229`) reescreve
triggers+LEDs+player_leds+rumble do perfil SALVO, apagando a edição não-persistida.
IPCs afetados sem trava: `led.set`/`led.player_set` (`ipc_handlers.py:371-411`),
`rumble.set/stop/passthrough` (`:1334+`). Triggers já tem (fix antigo BUG-MOUSE-TRIGGERS-01).

## Sintoma a sintoma (classificação)

- **U1** (P0) PRECISA_FIX(UX)+CURADO_POR_INSTALL: não existe IPC system.enable/disable — liga/
  desliga é `systemctl --user start/stop` direto (`daemon_actions.py:858-865,1157-1174`); unit
  hoje ativa/enabled. Falta o toggle in-place "Ligar o Hefesto" na aba Início offline
  (`home_actions.py:472-496,418-421` não tocado pela N).
- **U2** (P0) PRECISA_FIX: slots de externos NUNCA expiram (`external_identity.py:93-94,168-176`)
  e `identity.py:260-267` (slot_for) une `_extra_reserved()` ao `used` → números detidos por
  externo já visto no boot bloqueiam DualSense PERMANENTEMENTE → "sony 1/sony 4" com 2 controles.
  `sync_connected` (`identity.py:319-336`) só limpa o registro DualSense. Falta IPC
  `identity.renumber` (compacta ambos p/ 1..N com sessão fechada) + botão.
- **U3** (P0) PRECISA_FIX: Causa A (principal) + Causa B (botão "Ativar"/`profile.switch`
  disparável por duplo-clique `row-activated`, glade:1167, `profiles_actions.py:462-468`).
- **U4** (P0) INVESTIGAR_AO_VIVO: guardas de draft-por-aba sólidos (`app.py:678-720`
  idempotente); hipótese líder = mesma Causa A. Aplicar fix A e re-testar isolado.
- **U5** (P1) JÁ EXISTE: botão "Aplicar aos jogos da Steam" (`daemon_actions.py:386-484`,
  `integrations/steam_launch_options.py`) já implementado no 27b51d5. Re-teste.
- **U6** (P1) CURADO_POR_INSTALL: `hefesto-launch` confirmado no PATH. Re-teste com launch option.
- **U7** (P1) INVESTIGAR_AO_VIVO: Triggers já protegido; reproduzir se persistir.
- **U8** (P1) INVESTIGAR_AO_VIVO: override por-uniq é a camada de maior prioridade
  (`backend_pydualsense.py:876-918`) mas `ProfileManager.apply()` faz `reset_output_overrides()`
  do disco (`manager.py:217-218`) — vulnerável à Causa A. Aplicar A e testar reconexão isolada.
- **U9** (P0) PRECISA_FIX (3 causas): (1) Causa A = "perfil eterno"; (2) player-LEDs/presets não
  vencem porque o D4 (auto-disable de cores automáticas) SÓ dispara para `lightbar_rgb`, nunca
  `player_leds` (`lightbar_actions.py:87-103`) → a paleta automática (COR-03,
  `identity.py:455-495`) sempre reescreve por cima; fix = estender D4 p/ `"player_leds" in
  update`; (3) brightness "não 100%" = o perfil `meu_perfil.json:13` tem 0.4 (defaults de código
  já são 1.0) → decisão de produto editar o asset.
- **U10** (P2) PRECISA_FIX: mesma entrega do U2 (botão renumerar).
- **U11** (P1) PRECISA_FIX: Causa A nos handlers de rumble.
- **U12** (P0) RESOLVIDO ao vivo (sink HDMI muted global; nenhum código do daemon mexe em SINK —
  só o drop-in de prioridade do mic, inocente). Residual = check de doctor "sink muted"
  (JÁ no escopo do G2/Onda G, check #5).
- **U13** (P2) JÁ SATISFEITO POR DESENHO: `_is_virtual_evdev` (`evdev_reader.py:306-307`) já
  exclui os uinput forwarded do input-remapper (mesma classe do vpad). Só falta doc.

## Backlog PRECISA_FIX (ordenado)

1. **Causa A (U3+U4+U9+U11)** — mover `mark_manual_trigger_active()` p/ topo incondicional de
   `DraftApplier.apply()` (`ipc_draft_applier.py:41`) + acrescentar em `_handle_led_set`,
   `_handle_led_player_set`, `_handle_rumble_set/stop/passthrough`. MAIOR ALAVANCA.
2. **U9-player** — estender D4 em `_persist_leds_update` (`lightbar_actions.py:99-101`) p/
   `"player_leds" in update`.
3. **U1** — toggle "Ligar o Hefesto" in-place na Início offline (`home_actions.py`), reusa
   `on_daemon_start`.
4. **U2+U10** — IPC `identity.renumber` (handler + `ipc_server.py`) gated por sessão fechada +
   botão "Renumerar agora".
5. **U3-B** — confirmar/remover `row-activated` da lista de perfis.
6. **U9-brightness** — `assets/profiles_default/meu_perfil.json` 0.4→1.0 (produto).
7. **U12-residual** — check doctor "sink muted" (coberto pela Onda G/G2 #5).
8. **U13** — doc de convivência input-remapper.
