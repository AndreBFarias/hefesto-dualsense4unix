# BUG-GUI-IMKILLABLE-01 — GUI ignora SIGTERM com diálogo modal aberto + subprocess síncrono na thread GTK

**Tipo:** fix (UX/GUI).
**Wave:** V3.8.2 — bugfixes de boot pós-V3.8.1.
**Estimativa:** S — signal handler defensivo + 2 callsites de subprocess/dialog.
**Dependências:** nenhuma.
**Status:** DONE (signal handler com 3 defesas validado: GUI morre em <3s no SIGTERM mesmo com
mainloop bloqueado por `subprocess.run` ou `dialog.run()`).

---

## Contexto

A mantenedora reportou: "o app travou legal, não consigo nem dar um kill nele". O comportamento
era consistente: depois de clicar em "Reiniciar daemon" (que disparava `subprocess.run` síncrono
com timeout 10s) ou de algum diálogo de erro abrir, a GUI parava de responder e `kill <pid>` não
fazia nada — só `kill -9` matava, e às vezes nem isso (quando o subprocess herdou o controle e
ficou em D-state esperando o systemd que estava esperando o daemon que estava em D-state).

## Diagnóstico (causa-raiz)

Três bugs combinados:

### A. Signal handlers via `GLib.idle_add` não rodam com mainloop bloqueado

A GUI registrava `signal.SIGUSR2 → GLib.idle_add(self.quit_app)`, mas não tinha handler
explícito para `SIGTERM`/`SIGINT`. Quando o usuário mandava `kill <pid>`, o handler default do
Python (interromper) era subjugado pelo fato do `Gtk.main_iteration_do(blocking=True)` não
processar Python signal handlers durante chamadas C bloqueantes. Pior: mesmo se tivesse o
handler com `GLib.idle_add(quit_app)`, o callback fica enfileirado e nunca executa enquanto o
mainloop está em `dialog.run()` modal ou em chamada C bloqueante.

### B. `Gtk.MessageDialog.run()` em `daemon_actions._show_restart_error`

`dialog.run()` é **modal síncrono**: bloqueia a thread principal GTK até o usuário clicar OK.
Durante esse bloqueio, **nenhum** callback idle/timeout executa — `GLib.idle_add(quit_app)` agendado
por um signal handler externo fica enfileirado para sempre. Resultado: enquanto o diálogo de
erro está aberto, a GUI é literalmente imkillable por sinal.

### C. `subprocess.run(["systemctl", ...], timeout=10)` em `on_daemon_service_restart`

Handler de botão executado na thread GTK rodava subprocess síncrono com timeout 10s. Se
`systemctl` ficasse em D-state (journal lento, dbus congestionado, daemon do hefesto em D-state
ele próprio), a UI ficava 10s sem responder. Pior: nesse intervalo o usuário podia disparar
outros handlers de botão que entravam em fila — quando o `systemctl` finalmente retornava (ou
levantava `TimeoutExpired`), o `_show_restart_error` abria um `dialog.run()` que entrava no
mesmo poço.

## Decisão / Entrega

### Fix A — Signal handler com 3 defesas (two-strikes + watchdog)

Em `HefestoApp.__init__`, instala `SIGTERM`/`SIGINT` apontando para um handler com 3 camadas:

1. **Defesa 1**: chama `Gtk.main_quit()` direto no handler (thread-safe, não passa pelo idle loop).
2. **Defesa 2**: agenda `GLib.idle_add(self.quit_app)` para o caminho de cleanup completo.
3. **Defesa 3**: spawna uma thread-watchdog daemon que dorme 2s e força `os._exit(128+sig)` —
   garante kill mesmo se ambas as defesas 1 e 2 estiverem bloqueadas pelo mainloop.

Plus: 2ª chamada de SIGTERM em <5s pula direto para `os._exit(128+sig)` (cobre o caso em que o
mainloop está em D-state irrecuperável — idle nunca roda).

### Fix B — `dialog.run()` substituído por callback "response"

`_show_restart_error` agora usa o padrão GTK3 não-bloqueante:

```python
dialog.connect("response", lambda d, _r: d.destroy())
dialog.show_all()
```

A UI segue responsiva enquanto o diálogo está aberto e sinais funcionam normalmente.

### Fix C — `subprocess.run` migrado para worker thread

`on_daemon_service_restart` agora segue o padrão já usado em `_run_systemctl_async`: submete o
subprocess para `_get_executor()` e devolve o resultado via `GLib.idle_add(_on_service_restart_done, …)`.
A thread GTK não bloqueia mais com subprocess longo.

## Critérios de aceite

- [x] `python -m py_compile` limpo.
- [x] Smoke runtime: `kill -TERM <gui_pid>` mata a GUI em <3s mesmo com handlers bloqueados (log:
  `gui_hard_exit_via_watchdog sig=15` quando a defesa 1/2 não consegue).
- [x] Smoke runtime: diálogo de erro de restart não bloqueia mais a UI — outros botões respondem
  enquanto o diálogo está aberto.

## Arquivos tocados

- `src/hefesto_dualsense4unix/app/app.py` — signal handler `_on_term_signal` com 3 defesas.
- `src/hefesto_dualsense4unix/app/actions/daemon_actions.py` — `on_daemon_service_restart` em
  worker thread + `_show_restart_error` não-bloqueante.

## Fora de escopo

- **Migrar todos os `dialog.run()` da GUI** para o padrão `connect("response", ...)`. Esta sprint
  cobre só o caminho do BUG-GUI-IMKILLABLE (handler de erro do restart). Os demais
  `dialog.run()` em `footer_actions.py` (perfil/import/restore) são menos frequentes e
  funcionam mesmo com o mainloop bloqueado (não disparam SIGTERM no meio); ficam para wave
  futura se virarem dor.
- **Substituir `os._exit` por shutdown gracioso forçado**. `os._exit(128+sig)` salta finalizadores
  Python (atexit, `__del__`, threading), mas é o ponto de design: o watchdog é última linha de
  defesa, garantia bruta de matabilidade. Cleanup gracioso já foi tentado pelas defesas 1/2.

## Notas para o executor

- A thread-watchdog é `daemon=True` — não impede o processo de morrer normalmente quando
  `Gtk.main_quit()` da defesa 1 funcionar; ela só "dispara" se o processo ainda estiver vivo
  após 2s.
- O signal handler imprime `gui_signal_quit_solicitado sig=15` na 1ª chamada e
  `gui_hard_exit_via_signal_repeat` ou `gui_hard_exit_via_watchdog` quando a 2ª/watchdog acionam
  — facilita pos-mortem no `journalctl`.
