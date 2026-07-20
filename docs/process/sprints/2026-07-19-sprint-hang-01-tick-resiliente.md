# Sprint HANG-01 — o poll loop nunca mais morre por um tick pendurado

> Investigação completa (agente da tarde, evidência em scratchpad da sessão 089ae384:
> daemon-hang-pyspy-20260719-1620.txt + daemon-hang-kernel-stacks-20260719.txt).
> EXECUTAR APÓS a Onda N (mesmos arquivos). Âncoras de linha = HEAD 27b51d5; revalidar offsets.

## Mecanismo provado (16:08:56, PID 2835 — silêncio total por 10 min)

1. `lifecycle.py:1796-1798` — o poll loop (~2s) chama `await self._sync_external_leds()`
   ANTES do gate de conexão (roda até com tudo desplugado — estado exato da debandada).
2. `lifecycle.py:1756` — `await self._run_blocking(sync.tick)` **SEM timeout**;
   `_run_blocking` (`:2034-2037`) = `run_in_executor` no pool `hefesto-hid`
   (`ThreadPoolExecutor(max_workers=2)`, `:310`).
3. `external_identity.py:313` — `tick()` → `discover_external_gamepads()`; o try/except de
   `:314` protege contra EXCEÇÃO, não contra BLOQUEIO.
4. `evdev_reader.py@27b51d5:308` — `dev.close()` no finally do loop por-device (abre TODOS os
   nodes de /dev/input; na debandada, nodes morrendo sob os pés).
5. `evdev/device.py:295` (evdev 1.7.0 em /usr/lib/python3/dist-packages — o .venv NÃO tem evdev
   próprio) — linha 295 = `os.close(self.fd)`. Kernel: thread em `futex_wait`, NENHUMA em
   D-state ⇒ o close(2) retornou; a thread nunca REOBTEVE O GIL (wedge de GIL/condvar sob churn
   extremo de threads). Não-determinístico — o daemon seguinte, ocioso, não travou.
6. Amplificação: o future nunca resolve ⇒ a corrotina do poll loop fica suspensa PARA SEMPRE em
   `:1756` ⇒ zero read_state, zero logs, zero watchdog (todo log periódico nasce do poll loop).

## Fix (menor mudança estrutвтural correta)

1. **Poll loop nunca aguarda o tick de externos inline** (`lifecycle.py:1743-1758`): o
   `_sync_external_leds` vira task auxiliar com guard de reentrância —
   `if self._external_tick_task and not self._external_tick_task.done(): pular este ciclo
   (contador +1)`; senão `self._external_tick_task = asyncio.create_task(...)`. O poll loop
   segue SEMPRE.
2. **Timeout + telemetria**: dentro da task, `await asyncio.wait_for(self._run_blocking(
   sync.tick), timeout=10.0)`; em `TimeoutError`: log WARNING `external_tick_pendurado`
   (1º) e ERROR a partir do 2º consecutivo. Documentar no comentário: a THREAD presa não é
   recuperável (padrão INIT_TIMEOUT_SEC, backend_pydualsense.py — trade-off já aceito no
   projeto: vaza 1 worker; o pool tem 2 e o poll loop não depende dele para input).
3. **Degradação após 2 timeouts consecutivos**: parar de agendar `discover` (inventário
   congela; `external_led` para de atualizar) até o próximo `input_dir_change` do
   `InputDirWatch` — e log INFO `external_tick_degradado` com instrução de doctor.
4. **Side-fix de thread-safety** (`evdev_reader.py:431/459`): `request_reopen`/`stop()` fecham
   o MESMO `InputDevice` de outra thread; aplicar o padrão GYRO-FD-01 (só a thread dona fecha;
   sinalização por flag + wake via self-pipe/`_stop_flag`). Já existe precedente no repo
   (physical_report_reader) — espelhar.

## Testes (falha-sem/passa-com)

1. Fake `discover` que bloqueia num `threading.Event` ⇒ poll loop (loop de teste asyncio)
   completa ≥3 ciclos seguintes, `external_tick_pendurado` logado, task não re-agendada
   enquanto pendente (no HEAD: o await inline suspende o loop — falha).
2. 2 timeouts consecutivos ⇒ `external_tick_degradado` + discover não re-agendado até
   `input_dir_change` simulado.
3. Reopen/stop: fake device com close instrumentado ⇒ close acontece SÓ na thread dona.

## Aceite
- Suíte completa verde (0 skipped) + ruff + mypy.
- Replay mental da debandada de 16:08: daemon continua logando e respondendo IPC com o tick
  eternamente pendurado.
