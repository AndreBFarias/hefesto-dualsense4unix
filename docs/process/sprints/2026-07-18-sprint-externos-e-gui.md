# Sprint EXTERNOS+GUI 2026-07-18 — EXT-04 · GUI-05

> Causa-raiz e evidências: estudo 2026-07-18 (guerra de escritores) §P3-BÔNUS, §P4, §P5.

## EXT-04 — externos com identidade; LED é do daemon; leitura é pura (P1)

Bug grave provado ao vivo: `_external_inventory` (daemon/ipc_handlers.py:156-192) ESCREVE os
LEDs como efeito colateral de toda leitura, a GUI polla a cada 4s sem comparar estado →
`joycon_enforce_subcmd_rate: exceeded max attempts` em loop → hid-nintendo DESREGISTROU o
8BitDo BT às 20:23 (a "morte por BT" era agravada por NÓS).

1. **Leitura pura**: `controller.list{external:true}` NÃO escreve LED nunca mais. Remover a
   chamada `apply_player_number` de `_external_inventory` (ipc_handlers.py:188-192).
2. **Numeração com identidade persistente**: registry de externos por `uniq` (MAC) análogo ao
   `ControllerIdentityRegistry` (daemon/subsystems/identity.py) — menor slot livre ≥
   (reserva dos DualSense), slot RESERVADO no disconnect, persistência por boot no mesmo
   controllers.json (namespace separado, ex.: `externals`). Fim do "LED muda sozinho a cada
   poll/replug" (ao vivo: 8BitDo foi 2 de madrugada e 4 à noite sem ninguém pedir).
3. **LED no tick do daemon**: aplicar o número via `core/external_leds.py` a partir do poll
   lento do daemon (ex.: junto do sync de identidade no poll de ~2s, lifecycle.py:1619-1646),
   com: (a) cache do último valor escrito por dispositivo — escreve SÓ em mudança;
   (b) rate-limit mínimo de 2s entre escritas no MESMO dispositivo; (c) telemetria INFO
   `external_led_written slot=N uniq=...` (hoje é silencioso via contextlib.suppress).
4. **GUI**: continua pollando para EXIBIR (agora leitura pura); nada muda no contrato IPC além
   do fim do efeito colateral.
5. Doctor/status: WARN quando um externo BT acumular erros do hid-nintendo no dmesg é FUTURO
   (não entra hoje — exigiria leitura de dmesg privilegiada).

## GUI-05 — tema, modo visível e honestidade do wrapper (P1)

1. **Diálogo do wrapper temado (P5, fix de 1 linha + estrutural)**:
   - `app/actions/launch_wrapper_dialog.py` `_build_wrapper_dialog` (L357-386):
     `dialog.get_style_context().add_class("hefesto-dualsense4unix-window")` (precedente:
     `app/gui_dialogs.py:248-249`).
   - Estrutural: bloco top-level `messagedialog` no `gui/theme.css` (padrão dos menus,
     theme.css:138-182) para cobrir qualquer diálogo futuro sem classe.
   - VARREDURA: todo `Gtk.MessageDialog`/`Gtk.Dialog` do app sem a classe (ex.:
     `gui_dialogs.py` confirm_delete_profile L150-213 e afins) ganha a classe.
   - Testes: espelho stub-level + assert no GTK-real existente (test_launch_wrapper_dialog.py
     TestDialogoGtkReal; test_theme_css.py) — regras de CI headless do índice.
2. **Modo do controle visível na ficha (P4, feature de UX conforme design)**:
   - A ficha do externo ganha um seletor SEGMENTADO READ-ONLY (padrão da casa, sem popup —
     veto do 8BIT-02 mantido) com `Nintendo | Xbox` e o modo DETECTADO marcado
     (`input_mode()` em app/actions/external_controllers.py:196-212), com subtítulo curto
     "modo é troca física no controle — veja o manual" ligando ao texto de orientação existente.
   - Insensitive (não clicável) mas visualmente igual aos segmentados do app; tooltip explica.
   - Testes: camada pura (rows) + montagem com stubs.
3. **Honestidade do dedup (aviso "jogo sem wrapper")**:
   - `assets/hefesto-launch.sh`: ao decidir envs, gravar marker
     `$XDG_STATE_HOME/hefesto-dualsense4unix/launch_env/last_run` (appid + epoch, best-effort).
   - Daemon: quando o detector de janela vê `steam_app_N` e NÃO há marker recente (janela de
     ~120s) para esse appid → `state_full.gamepad_emulation.wrapper_used=false` (e `true` no
     caso bom; `null` sem jogo). `dedup_ok` deixa de mentir: refletir também `wrapper_used`.
   - GUI (aba Início/Status): banner discreto quando `wrapper_used=false` com o jogo aberto:
     "O jogo está rodando sem o hefesto-launch — controles podem duplicar. Copie as opções na
     aba Sistema." (texto pro leigo, padrão da casa).
   - Testes: decisão pura do marker (parametrizada), handler IPC, banner com stubs.

## Gate de aceite
- Suíte completa local 0 skipped; ruff/mypy verdes; check_anonymity ok.
- Ao vivo (eu valido): abrir a ficha do Pro Controller → segmented visível marcando Nintendo;
  diálogo do wrapper forçado (jogo fake não mapeado) abre ESCURO; poll da GUI aberto por 10min
  sem NENHUMA escrita de LED no journal além de mudanças reais; state_full com wrapper_used.
