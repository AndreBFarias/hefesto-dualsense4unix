# GUI-ESTABILIDADE-COSMIC-REMEDIATION-01 — remediação da instabilidade da GUI no COSMIC

Data: 2026-07-08. Branch: `feat/mouse-point-and-click-v3.11`. Status: **DONE (validado ao vivo, não commitado)**.

> **Resultado (2026-07-08):** 5 sprints entregues por agentes em paralelo (arquivos
> disjuntos). Gate verde: ruff + mypy + acentuação + anonimato + **1841 pytest passed,
> 19 skipped, 0 failures**. Validação visual ao vivo no COSMIC: rodapé com os 4 botões,
> janela pinta no boot (sem tela preta) capturada a 3s, ZERO `Negative content width`
> no log, aba Gatilhos em grade que quebra linha, exclusão mútua do Rumble confirmada
> (1 afundado por vez, slider acompanha). Falta só commitar.

## Contexto

A usuária reportou a GUI "bugadíssima, tanto botões quanto o funcionamento como um
todo" e "muito instável" no COSMIC + Wayland + NVIDIA (GUI sob XWayland). Screenshots
ao vivo mostraram: (1) janela abrindo **totalmente preta**; (2) **rodapé quebrado** —
só "Aplicar" aparece, os outros 3 botões somem.

**Triagem:** NÃO há sprint de GUI "em aberto" — todas as specs de UI estão entregues
no git. O problema é que **o código entregue regrediu / tem bugs**. Esta sprint é a
remediação (bugs novos), não a execução de specs antigas.

Diagnóstico produzido por reprodução ao vivo (screenshots + logs) + 4 auditorias
paralelas read-only do código. 19 achados, agrupados abaixo em 5 workstreams
**file-disjuntos** (rodam em paralelo sem conflito de arquivo).

---

## Catálogo de achados

### CRÍTICO
- **F1 (rodapé):** `footer_buttons_box` virou `GtkFlowBox` (commit `d68c373`) e dropa 3
  de 4 botões — só "Aplicar" renderiza. Log cheio de `Gtk-WARNING: Negative content
  width -27 … GtkButton/GtkFlowBoxChild`. `gui/main.glade:2345` + statusbar
  `hexpand=True` em `:2331`. Confirmado ao vivo em 953px (espaço de sobra → é bug de
  alocação do FlowBox, não de largura).
- **T1 (Teclado):** `parse_binding` (`core/keyboard_mappings.py:71-91`) rejeita os
  tokens virtuais `__OPEN_OSK__`/`__CLOSE_OSK__`, que são os **defaults de l3/r3**.
  `_persist_key_bindings_to_draft` (`input_actions.py:206-228`) faz `parse_binding` de
  cada linha e `except ValueError: continue` → descarta l3/r3. Clicar "Adicionar" +
  "Salvar Perfil" grava o perfil **sem** os toggles de teclado virtual (PERDA DE DADOS).
  Existe `is_virtual_token()` (`keyboard_mappings.py:66`) pronto.
- **R1 (janela preta):** race de primeiro-frame XWayland+NVIDIA, amplificada por
  `HefestoApp.show()` (`app.py:713-732`) construir/reparentar todos os widgets dinâmicos
  (sticks, grid de glyphs, 5 SegmentedSelectors com remove/add/show_all) **depois** de
  `window.show_all()`. Sem nenhuma mitigação de repaint.

### ALTO
- **A1 (Rumble):** os 4 botões de política são `GtkToggleButton` independentes (sem
  `group`); o clique direto (`_set_policy`, `rumble_actions.py:140-163`) nunca desmarca
  os irmãos → vários afundados ao mesmo tempo; clicar num já-ativo desmarca todos e
  **não reenvia IPC** (clique morto). `_activate_policy_toggle` já existe e desmarca os
  irmãos, mas só o caminho do slider o chama.
- **R2 (busy-loop):** `compact_window.py:118` faz `GLib.idle_add(self._tick_refresh)` e
  `_tick_refresh` retorna `True` → busy-loop 100% CPU (mesma falha de
  BUG-GUI-IDLE-ADD-BUSY-LOOP-01). Gated por `HEFESTO_DUALSENSE4UNIX_COMPACT_WINDOW=1`.
- **T2 (Emulação):** `on_emulation_refresh` (`emulation_actions.py:60-62`) só chama
  `_refresh_emulation_view()`; não refaz gamepad/modo-jogo/mic/steam. Botão "Atualizar"
  não reconcilia a maioria dos status.
- **T3 (Emulação):** página 6 (Emulação) ausente do `refresh_map` de switch-page
  (`app.py:658-668`). Se o daemon subir depois do boot, a aba fica "offline"/"—" até a
  usuária apertar um botão de gamepad.

### MÉDIO
- **R3 (jank):** `_render_live_state` (`status_actions.py:594-655`) escreve
  set_fraction/set_text/set_markup **incondicionalmente a 10 Hz** (inclui `header.set_markup`
  a 10 Hz) → repaint contínuo mesmo com controle parado. Diffar antes de escrever.
- **R4 (contenção):** 3 pollers de `daemon.state_full` (10 Hz + 2 Hz + 0.5 Hz;
  `status_actions.py:127-131`) no executor de 1 worker; os de 2/0.5 Hz sem guard de
  inflight. Um poller alimenta os 3 renderers (subsampling) ou adicionar guards.
- **M1 (race):** `_guard_refresh` é UM atributo compartilhado por triggers/rumble/mouse
  mixins. Callback async de sync de política do Rumble pode ser engolido por um refresh
  de Gatilhos. Renomear o guard por mixin (Lightbar já faz isso).
- **M2 (layout):** SegmentedSelector de Gatilhos (`wrap=True`, 19 botões largos,
  `min_children_per_line=1`, `segmented_selector.py:159-168`) exige largura mínima do
  botão mais largo → `Negative content width` + coluna larga sob scroller `hscroll=NEVER`.
- **T4 (Perfis):** `on_profile_activate`/duplo-clique chamam `profile_switch` **síncrono**
  (`profiles_actions.py:314-322`) na thread GTK → freeze até timeout. Usar `call_async`.
- **T5 (Daemon):** dois botões "Reiniciar" redundantes (`daemon_restart_button` →
  `on_daemon_restart` e `btn_restart_daemon` → `on_daemon_service_restart`), com
  sensibilidade inconsistente. Remover o redundante, manter `on_daemon_service_restart`.
- **T6 (Mouse):** `install_mouse_tab` (`mouse_actions.py:81-87`) não chama
  `_refresh_mouse_from_draft()`; se o daemon estiver offline no bootstrap, a aba mostra
  defaults do glade em vez dos valores do perfil ativo.

### BAIXO
- **B2 (Lightbar):** `on_lightbar_off` (`lightbar_actions.py:146-160`) não atualiza
  `self.draft.leds.lightbar_rgb` → "Apagar" + "Salvar" salva a cor antiga.
- **T7 (Perfis):** `install_profiles_tab` (`profiles_actions.py:138-140`) dispara
  `on_profile_advanced_toggle` sem `_suppress_advanced_toggle` → grava pref no disco na
  thread GTK durante o boot.
- **T8 (Daemon):** `_daemon_autostart_guard` (`daemon_actions.py:38`) sem default de
  classe (frágil se acionado antes do install).
- **B1 (fragilidade):** `_get(...)` desreferenciado sem None-guard em
  `status_actions.py:514/554/560/606/623-628` e `rumble_actions.py:302-308`.
- **B3 (cosmético):** entradas mortas `on_trigger_left/right_preset_changed` em
  `app.py:229-230` (glade não referencia; ligadas em código).

---

## Workstreams (file-disjuntos — paralelos)

### Sprint 1 — Janela preta + rodapé + wiring  `[glade footer, app.py, compact_window.py]`
- **R1:** em `app.py`, reordenar `show()` para chamar todos os `install_*_tab()` +
  `connect("switch-page")` **antes** de `window.show_all()`; adicionar
  `_force_initial_repaint()` (via `GLib.timeout_add(60, …)` que faz
  `self.window.get_window().invalidate_rect(None, True)` + `queue_draw()`). Aplicar a
  mesma reordenação ao ramo `start_hidden` de `run()`.
- **F1:** em `gui/main.glade`, reverter `footer_buttons_box` de `GtkFlowBox` para
  `GtkBox` horizontal (`spacing=6`, `halign=end`, `homogeneous` opcional), removendo os
  wrappers `GtkFlowBoxChild`; garantir que os 4 botões apareçam em 953px. Zerar os
  `Negative content width` do rodapé.
- **T3:** em `app.py`, adicionar a página 6 ao `refresh_map` de `_on_notebook_switch_page`
  (ex.: `6: getattr(self, "_refresh_emulation_tab", None)` — criar agregador se preciso,
  coordenando com Sprint 4 que possui `emulation_actions.py`; **alternativa sem cross-file:**
  apontar para um método já existente de emulação seguro). Se precisar de método novo em
  `emulation_actions.py`, deixar para a Sprint 4 e aqui só referenciar o nome.
- **T5-glade:** remover o `<child>` do `daemon_restart_button` do glade e a entrada
  `on_daemon_restart` do `_signal_handlers` em `app.py` (a remoção do método fica na Sprint 5).
- **B3:** remover as 2 entradas mortas de preset em `_signal_handlers`.
- **R2:** em `compact_window.py:118`, trocar por
  `GLib.idle_add(lambda: self._tick_refresh() and False)`.

### Sprint 2 — Fluidez do Status (jank + contenção)  `[status_actions.py]`
- **R3:** cachear último valor de cada widget de live-state e só escrever no `set_*`
  quando mudar; parar de reescrever `header.set_markup` a 10 Hz (deixar para reconnect).
- **R4:** um único poller (`_tick_live_state`) guarda o último `state` e deriva
  slow/reconnect com subsampling (ex.: a cada 5º/20º tick), eliminando as chamadas IPC
  independentes de 2/0.5 Hz — OU, no mínimo, adicionar guard de inflight nesses dois.
- **B1-status:** padronizar `w = self._get(id); if w is not None:` nos pontos sem guard.

### Sprint 3 — Gatilhos/Rumble/Mouse widgets  `[rumble_actions.py, triggers_actions.py, mouse_actions.py, segmented_selector.py]`
- **A1:** em `_set_policy`, antes do IPC, chamar `_activate_policy_toggle(policy)` sob
  guard (desmarca os irmãos). Preferível: converter os 4 `GtkToggleButton` em
  `GtkRadioButton` num `group` (exclusão nativa; impossível desmarcar todos). Se mexer no
  glade for necessário, coordenar com Sprint 1 (dona do glade) — preferir a solução em
  código para manter file-disjunto.
- **M1:** renomear `_guard_refresh` por mixin: `_triggers_guard_refresh`,
  `_rumble_guard_refresh`, `_mouse_guard_refresh` (todos os usos nos 3 arquivos).
- **M2:** dar largura de referência ao FlowBox do SegmentedSelector (`set_min_content_width`
  no scroller, ou `width-request`, ou reduzir min por linha) para zerar os
  `Negative content width` de Gatilhos.
- **T6:** chamar `self._refresh_mouse_from_draft()` no fim de `install_mouse_tab`.
- **B1-rumble:** None-guard em `rumble_weak_scale`/`rumble_strong_scale`.

### Sprint 4 — Teclado (perda de dados) + Emulação  `[input_actions.py, core/keyboard_mappings.py, emulation_actions.py]`
- **T1:** em `parse_binding` (`keyboard_mappings.py`), aceitar tokens virtuais via
  `is_virtual_token()`: se o token for virtual, aceitá-lo como está; senão exigir `KEY_*`.
  Verificar que o daemon consome o mesmo formato (os defaults já são esses tokens).
  Garantir que edição de célula, persist e loader passam a aceitar OSK.
- **T2:** em `on_emulation_refresh`, chamar também `_refresh_gamepad_and_gamemode()`,
  `_refresh_mic_status()` e `_refresh_steam_input_status()`. Se a Sprint 1 pedir um
  agregador `_refresh_emulation_tab`, criá-lo aqui.

### Sprint 5 — Perfis + Daemon + Lightbar  `[profiles_actions.py, daemon_actions.py, lightbar_actions.py]`
- **T4:** trocar `profile_switch(name)` síncrono por `call_async("profile.switch", …)` com
  toast no callback em `on_profile_activate`.
- **T7:** envolver o `set_active` do install de perfis com `_suppress_advanced_toggle`.
- **T5-logic:** remover o método `on_daemon_restart` (botão removido pela Sprint 1) e
  manter `on_daemon_service_restart` como caminho único; conferir sensibilidade.
- **T8:** default de classe `_daemon_autostart_guard: bool = False`.
- **B2:** em `on_lightbar_off`, atualizar `self.draft.leds.lightbar_rgb = (0,0,0)`.

---

### Sprint 6 — Centralizar sincronia FAKEsocket (BUG-FAKE-SOCKET-SYNC-01)  `[xdg_paths.py, daemon/main.py]`
Descoberto AO VIVO durante a validação: o header mostrava "Conectado Via USB" com o
controle desconectado. Causa: um daemon fake cru (`HEFESTO_DUALSENSE4UNIX_FAKE=1` sem
`IPC_SOCKET_NAME`) usava o socket de PRODUÇÃO e **sequestrava** o daemon real (a GUI
falava com um FakeController). As duas variáveis (`FAKE` e `IPC_SOCKET_NAME`) precisavam
andar em sincronia (só o `run.sh --fake` as setava juntas) — footgun de dessincronia.
- **Fix:** `xdg_paths.ipc_socket_name()` (fonte única) deriva o socket do próprio switch
  de fake: `FAKE=1` sem override → `hefesto-dualsense4unix-fake.sock` isolado
  automaticamente. `ipc_socket_path()` e `daemon.main.single_instance_name()` usam essa
  resolução. Precedência: override explícito > fake-auto > default. Impossível um daemon
  fake tocar o socket de produção, mesmo iniciado como `daemon start` cru.
- **Prova ao vivo:** daemon fake cru bind `…-fake.sock`; socket de produção intacto;
  daemon real segue `connected:False`.

### Cleanup — dead code do T5  `[app.py, daemon_actions.py]`
Removido o `on_daemon_restart` (método + entrada de `_signal_handlers`) que ficou inerte
após a Sprint 1 remover o botão "Reiniciar" redundante do glade. Caminho único de restart:
`on_daemon_service_restart`.

## Aceitação
- Rodapé: os 4 botões (Aplicar/Salvar/Importar/Restaurar) 100% visíveis em 953px (janela
  tiled do COSMIC) — validado visualmente por screenshot.
- Janela abre pintada (sem tela preta) — validado por screenshot em boot repetido.
- Rumble: exatamente 1 política afundada por vez; clique sempre reenvia IPC.
- Teclado: "Adicionar" + "Salvar Perfil" preserva l3/r3 (OSK) no perfil.
- Emulação: "Atualizar" reconcilia todos os status; aba se corrige ao entrar.
- Log da GUI sem `Gtk-WARNING: Negative content width`.
- Gate verde: ruff + mypy + pytest + acentuação + anonimato.

## Notas de execução
-  NÃO rodar `./run.sh --smoke` nem subir daemon de produção — mata o daemon do systemd.
- Testes: pytest é hermético; validação runtime-real da GUI é por screenshot no COSMIC
  (input sintético xdotool NÃO chega à janela sob XWayland/cosmic-comp).
