# BUG-DAEMON-BOOT-DSTATE-LOOP-01 — Loop conecta/desconecta no boot + daemon imkillable em D-state

**Tipo:** fix (estabilidade/daemon).
**Wave:** V3.8.2 — bugfixes de boot pós-V3.8.1.
**Estimativa:** S — fix cirúrgico em 2 arquivos + timeout-wrapper em `pydualsense.init()`.
**Dependências:** nenhuma.
**Status:** DONE (fixes aplicados + validados rodando na máquina: novo daemon sobe sem `EBADF` e marca offline em 5s quando hidraw está degenerado, em vez de travar para sempre).

---

## Contexto

A mantenedora reportou no boot do PC: "o controle fica conectando e desconectando, o daemon dá pau
legal", e "o app travou legal, não consigo nem dar um kill nele". Sintomas combinados visíveis no
`journalctl --user -u hefesto-dualsense4unix.service`:

1. Loop de `Main process exited, code=exited, status=1/FAILURE` a cada ~2s (systemd `Restart=on-failure`).
2. Após algumas iterações, um daemon entra em `State: D (disk sleep)` no kernel e fica imkillable:
   `Processes still around after SIGKILL. Ignoring.`

## Diagnóstico (causa-raiz)

Dois bugs independentes que se reforçam:

### A. `OSError: [Errno 9] Descritor de arquivo inválido` em `single_instance.py:244`

`acquire_or_takeover` faz `os.close(fd)` em três ramos de erro distintos:

```python
fd = os.open(...)
try:
    try:
        fcntl.flock(fd, ...)
    except OSError as exc:
        if exc.errno in (EWOULDBLOCK, EAGAIN):
            ...
            else:                          # for-else: loop completou sem break
                os.close(fd)               # ← close 1
                raise RuntimeError(...)
        else:
            os.close(fd)                   # ← close 2
            raise
    ...
except Exception:
    os.close(fd)                            # ← close 3 (DUPLICATE)
    raise
```

Quando o ramo interno EWOULDBLOCK estoura o timeout, ele faz `os.close(fd)` E levanta
`RuntimeError`. O `except Exception` externo captura o `RuntimeError` e tenta `os.close(fd)`
de novo — segundo close no mesmo fd produz `EBADF (Errno 9)`, que mascara o erro original e
derruba o daemon. systemd vê `exit code 1`, respawn em 2s, mesma sequência → o que o usuário vê
como "controle conecta/desconecta" é o ciclo de respawn do systemd, não um loop interno do daemon.

### B. `pydualsense.init()` entra em D-state quando hidraw está degenerado

Em transição USB rápida (autosuspend resume, `hid_playstation` rebind, hub low-power, daemon
anterior segurando fd órfão `/dev/hidraw* (deleted)`), a chamada `pydualsense.init()` faz HID
I/O síncrono via libhidapi que o kernel não consegue completar — a thread entra em
`D (disk sleep)`, estado imkillable (nem `SIGKILL` com sudo, nem `cgroup.kill`). O daemon some
da árvore de processos do systemd (na verdade fica como ghost) e nunca encerra; o cgroup do
service fica "deactivating" pra sempre, impedindo `systemctl start` subsequentes.

Confirmação pós-mortem no `/proc/<pid>/fd/`:
```
fd 11 -> /dev/hidraw4 (deleted)
fd 6  -> /dev/uinput
```

## Decisão / Entrega

### Fix A — Cleanup centralizado com `contextlib.suppress(OSError)`

Em `acquire_or_takeover` e `acquire_or_bring_to_front`, os `os.close(fd)` internos foram
removidos do caminho de erro; o cleanup vive apenas no `except Exception` externo, sob
`contextlib.suppress(OSError)`. O `raise` dentro do `except` interno propaga normalmente — o
externo cobre todos os casos sem double-close.

### Fix B — `pydualsense.init()` com timeout via `threading.Thread(daemon=True)`

`PyDualSenseController.connect()` agora executa `ds.init()` numa thread daemon com
`t.join(timeout=INIT_TIMEOUT_SEC)` (5s). Se a thread ainda está viva ao expirar:

- Marca `_offline = True` e retorna sem erro.
- Abandona a thread (ela morre com o processo — daemon=True).
- O `reconnect_loop` retenta na próxima iteração (5s) — quando o kernel liberar o I/O do hidraw,
  a próxima `ds.init()` retorna em <300ms e o controle volta normal.

`ThreadPoolExecutor` foi descartado: o `__exit__` do executor faz join na thread, o que travaria
o daemon novamente; `threading.Thread(daemon=True)` direto não tem essa armadilha.

Override via env: `HEFESTO_DUALSENSE4UNIX_INIT_TIMEOUT_SEC` (default `5`).

## Critérios de aceite

- [x] `python -m py_compile` limpo nos dois arquivos.
- [x] Smoke runtime: daemon morre limpo no SIGTERM em ~5s mesmo com hidraw bloqueado (o log mostra
  `pydualsense_init_timeout — marcando offline` seguido de `daemon_stopped`).
- [x] Smoke runtime: daemon novo sobe sem `EBADF` no `journalctl` — log mostra
  `single_instance_adquirido name=daemon pid=<novo>` direto, sem `OSError [Errno 9]`.
- [x] Daemon zombie pré-existente em D-state não impede novo daemon de subir (após apagar o pid
  file órfão — flock é por inode, novo arquivo = novo lock independente).

## Arquivos tocados

- `src/hefesto_dualsense4unix/utils/single_instance.py` — cleanup centralizado.
- `src/hefesto_dualsense4unix/core/backend_pydualsense.py` — timeout via thread daemon.

## Fora de escopo

- **Liberar PID em D-state pré-existente sem reboot.** Linux não tem mecanismo de userspace pra
  matar processo em `D (disk sleep)` — só morre quando o kernel der timeout no I/O (incerto) ou
  com reboot. Os fixes acima evitam o estado, não o desfazem.
- **Substituir `pydualsense.init()` por implementação interruptível.** Migração para hidraw nativo
  (sem libhidapi) seria escopo maior; o timeout no wrapper já contém o sintoma.

## Notas para o executor

- O daemon precisa pertencer mesmo após o owning-thread "morrer" no timeout — usar
  `threading.Thread(daemon=True)` (não `Thread` regular) é o que garante que o GC do processo
  não bloqueia esperando a thread vazada.
- `flock` é por inode, não por path: deletar o pid file e abrir um novo cria um lock independente
  do antigo (que ainda é detido pelo zombie). Isso é o que destrava a recuperação sem reboot na
  máquina da mantenedora.
