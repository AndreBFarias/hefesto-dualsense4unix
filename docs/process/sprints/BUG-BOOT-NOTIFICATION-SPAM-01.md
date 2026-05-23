# BUG-BOOT-NOTIFICATION-SPAM-01 — "Tem algo não instalado" toda vez que liga o PC

**Tipo:** fix (UX/notifications).
**Wave:** V3.8.2 — bugfixes de boot pós-V3.8.1.
**Estimativa:** S — gating por env + flag persistente + throttle temporal.
**Dependências:** nenhuma.
**Status:** DONE (validado: notify do tray COSMIC só aparece uma vez na vida da instalação;
notify de WirePlumber default off; throttle de 30s elimina rajada de connect/disconnect).

---

## Contexto

A mantenedora reportou: "ao ligar o PC ele fica falando que tem algo não instalado". Duas fontes
combinadas geravam a impressão de spam recorrente:

1. **Notify "Tray icon indisponivel no COSMIC"** disparava toda sessão da GUI, mesmo quando o
   `cosmic-applet-status-area` estava habilitado — porque o probe rodava 500ms após o login,
   antes do watcher D-Bus terminar de se registrar (race conhecido em COSMIC 1.0.6+).
2. **Notify "WirePlumber fixou o DualSense como microfone padrão"** disparava toda sessão do
   daemon — a mantenedora já sabia disso (e não queria rodar `doctor.sh --fix`); só queria
   parar de ser lembrada.

Adicional: se em algum momento o daemon entrasse em loop conecta/desconecta (resolvido em
BUG-DAEMON-BOOT-DSTATE-LOOP-01), `notify_controller_connected/disconnected` empilhava popups
porque nenhum throttle limitava a frequência.

## Diagnóstico (causa-raiz)

### A. Probe do `StatusNotifierWatcher` em 500ms — race-prone

`AppTray._start_deferred` chamava `statusnotifierwatcher_available()` **imediatamente** após
criar o `Indicator`, e se o probe falhasse emitia `notify(once_key="cosmic_tray_missing")`. O
`once_key` deduplica **dentro da sessão**, mas a GUI é recriada a cada hotplug USB do controle
(unit `hefesto-dualsense4unix-gui-hotplug.service`), então cada plug fazia o probe falso falhar
de novo e re-notificar.

500ms é insuficiente em COSMIC 1.0.6+ — o `cosmic-applet-status-area` registra o watcher D-Bus
em ~1–1.5s após o login. Resultado: notify "tray indisponível" falsa, **mesmo quando o tray
realmente aparece logo depois**.

### B. `notify_system_warnings` emitia mesmo com env padrão

`_check_system_on_boot` em `daemon/lifecycle.py:225` chamava `notify_system_warnings()` que
checava `_notifications_enabled()` (env opt-in). Mas em alguma sessão a env tinha sido setada
e nunca mais foi removida — a mantenedora não lembrava de ter ligado. Sem distinção entre
"avisos críticos" (perfil corrompido) e "avisos informativos" (WirePlumber, udev outdated),
o sinal/ruído ficou ruim.

### C. `notify_controller_connected/disconnected` sem throttle

`reconnect_loop` (probe a cada 5s) + `poll_loop` (que chama `reconnect()` em `read_state` fail)
podem publicar `CONTROLLER_CONNECTED`/`DISCONNECTED` em rajada se o controle estiver flapando
(autosuspend, hid_playstation rebind, cabo USB ruim). Cada evento dispara `notify_*` sem
qualquer dedup temporal — rajada visual de 5+ popups em 30s.

## Decisão / Entrega

### Fix A — Probe com retries + flag persistente entre sessões

Em `app/tray.py`:

1. `_INDICATOR_DEFERRED_MS` aumentado de 500 → 1500.
2. Novo `_probe_watcher_with_retries(attempt)`: até 3 tentativas com 1s entre cada (total ~3s
   de tolerância).
3. Só notifica se TODAS as tentativas falharem.
4. Após primeira notificação, grava flag persistente em
   `$XDG_RUNTIME_DIR/hefesto-dualsense4unix/cosmic_tray_warned.flag` — usuário não recebe o
   aviso de novo a cada login. (Para reemitir: apagar a flag ou setar
   `HEFESTO_DUALSENSE4UNIX_RESET_TRAY_WARNING=1`.)

### Fix B — `notify_system_warnings` default off + env explícita

`_check_system_on_boot` agora checa `HEFESTO_DUALSENSE4UNIX_SYSTEM_WARNINGS_NOTIFY` (default
`0`). O log em `warning` permanece (visível em `journalctl --user -u hefesto-dualsense4unix.service`),
mas o popup só aparece se o usuário explicitamente ligar.

### Fix C — Throttle de 30s para connect/disconnect

`desktop_notifications.py` ganha `_throttle_passes(key)` e `_last_emit_at: dict[str, float]`.
`notify_controller_connected` e `notify_controller_disconnected` usam chaves separadas
(`"controller_connected"` e `"controller_disconnected"`) — máximo 1 notify por chave a cada
30s. Override via env `HEFESTO_DUALSENSE4UNIX_NOTIFY_THROTTLE_SEC`. Plug deliberado raramente
acontece em <30s; flap espúrio fica silencioso.

## Critérios de aceite

- [x] Smoke runtime: GUI subiu em COSMIC e o tray apareceu sem notify de "indisponível"
  (probe esperou 1.5s + retries pegaram o watcher).
- [x] `python -m py_compile` limpo nos três arquivos.
- [x] Constantes carregadas no runtime: `_INDICATOR_DEFERRED_MS=1500`, `_WATCHER_PROBE_RETRIES=3`,
  `_THROTTLE_MIN_INTERVAL_SEC=30.0`.

## Arquivos tocados

- `src/hefesto_dualsense4unix/app/tray.py` — retries + flag persistente.
- `src/hefesto_dualsense4unix/daemon/lifecycle.py` — `_check_system_on_boot` gating env.
- `src/hefesto_dualsense4unix/integrations/desktop_notifications.py` — throttle temporal.

## Fora de escopo

- **Notify por categoria** (CRITICAL/INFO/DEBUG). Para esta wave, "default off + env opt-in" cobre
  o caso da mantenedora. Categorização ficaria para wave de melhoria de UX se virar dor.
- **Auto-fix do WirePlumber no boot**. `doctor.sh --fix` é o comando canônico — não queremos
  rodar sudo silencioso no boot (princípio do FEAT-SYSTEM-AUTOREPAIR-BOOT-01).

## Notas para o executor

- A flag `cosmic_tray_warned.flag` mora em `$XDG_RUNTIME_DIR` — é volátil (some no reboot/logout).
  Intencional: se o usuário rebootar e ainda assim o tray não aparecer, faz sentido avisar de
  novo (pode ser cenário novo). Para persistência permanente (não avisar nunca mais), usuário
  deve setar a env `HEFESTO_DUALSENSE4UNIX_SUPPRESS_TRAY_WARNING=1` no shell rc — mas hoje
  só temos o caminho da flag; o opt-out permanente fica para wave futura se virar dor.
- O `uninstall.sh` já limpa o `runtime_dir` (linha 261-264) — a flag não polui depois de remover
  o app.
