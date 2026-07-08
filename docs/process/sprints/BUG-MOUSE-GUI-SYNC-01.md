# BUG-MOUSE-GUI-SYNC-01 — Aba Mouse mente: sincronizar GUI com estado vivo + Aplicar seguro

**Tipo:** fix (médio — GUI + 1 rota IPC).
**Wave:** V3.11.
**Estimativa:** 1 iteração.
**Dependências:** nenhuma.
**Status:** READY.

---

**Tracking:** labels `type:fix`, `ui`, `mouse-emu`, `ai-task`, `status:ready`.

## Contexto

Diagnóstico 2026-07-03 (ver `2026-07-03-diagnostico-emulacao-mouse-grim-fandango.md`,
achados A1-A4, todos confirmados com repro). A aba Mouse da GUI opera sobre um draft
que NUNCA sincroniza com o estado vivo do daemon, e o rodapé envia a seção mouse
inteira mesmo quando a usuária não a tocou. Quatro bugs concretos:

1. **A1 — GUI dessincronizada**: `_compute_draft_from_active_profile` (`app/app.py:568-571`)
   chama `daemon_state_full()` mas lê só `active_profile`, descartando o bloco
   `mouse_emulation {enabled, speed, scroll_speed}` que o daemon expõe
   (`daemon/ipc_handlers.py:316-320`). Com daemon em modo mouse (flag persistido no
   boot, CLI, applet), a GUI abre com toggle OFF e sliders 6/1 — e sliders com toggle
   OFF não aplicam nada (`mouse_actions.py:118-120`).
2. **A2 — Aplicar desliga emulação viva**: `to_ipc_dict` SEMPRE emite a seção mouse
   (`draft_config.py:274-278`, default `enabled=False`); `DraftApplier._apply_mouse`
   chama `set_mouse_emulation(False)` que destrói o device E persiste
   `mouse_emulation.flag` off (`subsystems/mouse.py:113-118`). Usuária liga modo mouse
   via CLI/applet, abre a GUI para ajustar gatilhos, clica Aplicar → modo mouse morre
   e nem restart traz de volta.
3. **A3 — RecursionError no toggle com daemon offline**: no caminho de falha,
   `switch.set_active(not enabled)` (`mouse_actions.py:93`) reemite `state-set` sem
   `_guard_refresh` → 999 reentradas (repro GTK3 real), até ~4 min de UI congelada
   (0,25s de timeout IPC por reentrada com daemon travado-mas-escutando).
4. **A4 — Slider religa emulação**: `on_mouse_speed_changed` decide pelo WIDGET
   (`_mouse_is_enabled()`) e envia `mouse_emulation_set(True, ...)`. Com toggle
   stale-ON (daemon desligou mouse via CLI `mouse off` ou via gamepad-ON), arrastar o
   slider religa a emulação, MATA o gamepad virtual em pleno jogo
   (`lifecycle.py:413-414`) e persiste `enabled=True`.

Extras da mesma área (mapeados, baixo risco): handlers de mouse fazem IPC bloqueante
na thread GTK (contrato de `ipc_bridge.py:52` proíbe); `FROZEN_WIDGET_IDS` não
congela os sliders; card "Mapeamento" com glyphs strippados ("Triângulo ()" vazio,
ADR-011).

## Decisão

1. **Sync no bootstrap e na troca de aba (A1)**: em `_compute_draft_from_active_profile`,
   após montar o draft do perfil, sobrepor o bloco vivo:
   `me = state.get("mouse_emulation")` → se dict,
   `draft = draft.model_copy(update={"mouse": MouseDraft(**me)})`. Complemento: refresh
   assíncrono da aba Mouse no switch-page da página 7 (padrão de
   `emulation_actions.py:289-321` — `call_async("daemon.state_full")` → widgets sob
   `_guard_refresh` + `model_copy` no draft).
2. **Rota IPC speed-only (A4, fix principal)**: `mouse.emulation.set` passa a aceitar
   params SEM `enabled` (`ipc_handlers.py:546-548`): só `speed`/`scroll_speed` →
   atualiza `config.mouse_speed/mouse_scroll_speed` e chama `_mouse_device.set_speed()`
   se o device existir, SEM start/stop. GUI envia só `{speed}` nos handlers de slider.
   Religação por construção impossível, mesmo com toggle stale.
3. **Aplicar seguro (A2)**: dirty-tracking da seção mouse no draft — `to_ipc_dict`
   emite `mouse: None` quando a seção não foi tocada nesta sessão da GUI
   (`_apply_section` já pula raw None, `ipc_draft_applier.py:55-56`; daemon não muda).
   Tocar toggle ou slider marca dirty. O sync do item 1 zera o risco residual
   (draft reflete o vivo).
4. **Guard no revert (A3)**: envolver `switch.set_active(not enabled)` do caminho de
   falha com `self._guard_refresh = True; try: ...; finally: self._guard_refresh = False`.
5. **Handlers async**: os 3 handlers de mouse migram de `_safe_call` síncrono para
   `call_async` (padrão do rodapé, `footer_actions.py:127-133`), com coalescing
   simples nos sliders (aplicar o último valor; um in-flight por vez).
6. **Freeze completo**: adicionar `mouse_speed_scale` e `mouse_scroll_speed_scale` a
   `FROZEN_WIDGET_IDS`.
7. **Glyphs do card Mapeamento**: corrigir "Triângulo ()" e "Círculo ()" no glade via
   NCR (`&#9651;`/`&#9675;`) — sobrevive ao sanitizer ADR-011.

## Critérios de aceite

- [ ] GUI aberta com daemon em modo mouse (flag persistido): toggle ON e sliders com
      os valores vivos do daemon — teste com state_full fake.
- [ ] `mouse.emulation.set {"speed": 9}` (sem enabled) com mouse LIGADO: muda
      velocidade ao vivo, sem destruir/recriar device. Com mouse DESLIGADO: atualiza
      config, NÃO liga emulação, NÃO cria device — teste de regressão do A4.
- [ ] Arrastar slider com toggle stale-ON e daemon com mouse off: emulação continua
      OFF (nenhum `uinput_mouse_created` no log).
- [ ] Aplicar com seção mouse não-tocada: NENHUMA chamada a `set_mouse_emulation`
      (repro do A2 vira teste: draft default → `to_ipc_dict()["mouse"] is None`).
- [ ] Aplicar com seção mouse tocada: comportamento atual preservado.
- [ ] Toggle com daemon offline: exatamente 1 tentativa de IPC + 1 revert; sem
      reentrada (contador no teste), sem RecursionError.
- [ ] Sliders/toggle congelados durante transação do Aplicar.
- [ ] Card Mapeamento renderiza "Triângulo ()" e "Círculo ()".
- [ ] Suite completa verde; ruff/mypy limpos.

## Arquivos tocados

- `src/hefesto_dualsense4unix/app/app.py` (overlay no bootstrap + refresh página 7).
- `src/hefesto_dualsense4unix/app/actions/mouse_actions.py` (guard no revert,
  handlers async, envio speed-only, dirty-mark).
- `src/hefesto_dualsense4unix/app/draft_config.py` (dirty da seção mouse;
  `to_ipc_dict` emite None quando limpa).
- `src/hefesto_dualsense4unix/app/actions/footer_actions.py` (`FROZEN_WIDGET_IDS`).
- `src/hefesto_dualsense4unix/daemon/ipc_handlers.py` (`enabled` opcional).
- `src/hefesto_dualsense4unix/daemon/lifecycle.py` (caminho set-speed-only se
  necessário).
- `src/hefesto_dualsense4unix/gui/main.glade` (NCR dos glyphs).
- `tests/unit/test_mouse_actions*.py`, `tests/unit/test_ipc_mouse*.py`,
  `tests/unit/test_draft_config*.py` (novos casos).

## Proof-of-work runtime

```bash
.venv/bin/pytest tests/unit -q
.venv/bin/ruff check src/ tests/
.venv/bin/mypy src/
./scripts/check_anonymity.sh
python3 scripts/validar-acentuacao.py --all
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=usb HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=bt  HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke --bt

# Cenário manual (validação da Vitória):
# 1. dsx mouse on --speed 9; abrir GUI → toggle ON, slider em 9.
# 2. Ajustar gatilhos, Aplicar → mouse continua ligado (dsx mouse status).
# 3. dsx mouse off (GUI aberta); arrastar slider → mouse continua desligado.
# 4. systemctl --user stop hefesto-dualsense4unix; clicar toggle → 1 toast de erro,
#    switch reverte, GUI responsiva.
```

## Notas para o executor

- O bloco `mouse_emulation` do state_full JÁ existe e é consumido pela CLI
  (`cli/cmd_mouse.py:93`) — o contrato está provado; não inventar rota nova.
- Cuidado com `_guard_refresh`: é o mesmo guard usado pelo refresh programático;
  salvar/restaurar valor anterior (padrão do fix `_update_preset_to_custom`,
  commit pós-ce1ef80) em vez de setar False absoluto.
- Gtk.Switch em GTK3: `set_state` chama `set_active` internamente — o guard é
  necessário em qualquer variante. `return True` no handler NÃO evita a reentrada.
- No dirty-tracking, "Restaurar Default" deve LIMPAR o dirty da seção mouse (recarrega
  do perfil, que não tem mouse).
- Não mexer na semântica do toggle (liga/desliga device de MOUSE; teclado é
  independente) — rename/UX do toggle fica fora de escopo.

## Fora de escopo

- Persistência de velocidade entre restarts (FEAT-MOUSE-CURSOR-FEEL-01).
- Curva de aceleração/expo do cursor (FEAT-MOUSE-CURSOR-FEEL-01).
- Perfil point-and-click e supressão por janela (FEAT-POINT-AND-CLICK-01).
- Card Mapeamento dinâmico (refletir key_bindings reais) — só o fix cosmético dos
  glyphs entra aqui.
