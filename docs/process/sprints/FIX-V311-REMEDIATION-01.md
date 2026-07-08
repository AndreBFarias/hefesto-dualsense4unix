# FIX-V311-REMEDIATION-01 — Remediação da auditoria da wave V3.11 (mouse/point-and-click)

**Tipo:** fix (grande — 3 HIGH + médios + baixos + hermeticidade de testes).
**Wave:** V3.11 (fecha antes do release).
**Status:** MATERIALIZADO — aguardando validação ao vivo da Vitória + re-auditoria.

---

## Contexto

A wave V3.11 (specs BUG-MOUSE-GUI-SYNC-01, FEAT-MOUSE-CURSOR-FEEL-01,
FEAT-POINT-AND-CLICK-01) saiu **code-complete e verde nos testes unitários**, mas
uma auditoria adversarial (workflow: 3 auditores de spec + 6 caçadores de bug por
dimensão + verificadores por maioria, 2026-07-07) provou que **não era shippable**.
Dois HIGH foram confirmados por leitura manual do código (os verificadores
adversariais desses achados morreram no limite de cota do modelo — o bucket
"refutados" do workflow os continha por não-verificação, não por refutação).

Esta sprint corrige todos os bloqueadores antes do release da V3.11.

## Achados corrigidos

### HIGH

1. **`BUG-BOOT-RESTORE-FLIPS-EMULATION-01`** — `daemon/connection.py`.
   `restore_last_profile` injetava `mouse_applier=daemon.set_mouse_emulation`.
   Como `activate()` grava `save_last_profile` em TODA ativação
   (`manager.py:108`), o `point_and_click` virava last_profile por mero
   autoswitch; no boot seguinte o restore rodava `set_mouse_emulation(True)`
   DEPOIS do gamepad já restaurado dos flags → matava o gamepad, apagava
   `gamepad_emulation.flag` e invertia a escolha persistida da usuária a CADA
   boot. **Fix:** `mouse_applier=None` no restore — o estado de emulação no boot
   é governado pelos FLAGS persistidos, não reaplicado pela seção mouse do perfil.
   O perfil ainda restaura triggers/LEDs/teclado. A supressão segue restaurada
   (applier presente, lock-aware). Teste: `test_boot_restore_nao_aplica_secao_mouse`.

2. **`BUG-PROFILE-MOUSE-KILLS-GAMEPAD-01`** — `profiles/manager.py`,
   `daemon/lifecycle.py`, subsystems `ipc/autoswitch/hotkey`,
   `assets/profiles_default/point_and_click.json`.
   `apply_emulation` chamava `set_mouse_emulation(profile.mouse.enabled, …)`
   incondicionalmente → ao focar (autoswitch) um perfil com `mouse.enabled=true`,
   o gamepad virtual morria no meio do jogo. Sem lock manual (a supressão tinha,
   o mouse não). O match do `point_and_click` incluía `scummvm`/`residualvm`
   genéricos → qualquer jogo ScummVM disparava. **Fix (3 partes):**
   - Novo applier guardado `Daemon.apply_profile_mouse(enabled, speed, scroll)`
     que espelha `apply_profile_suppression`: respeita o **lock manual** de 30 s
     (`MANUAL_PROFILE_LOCK_SEC`) e é **idempotente** (com o mouse já no estado
     desejado, só ajusta velocidade — não recria o device a cada tick).
   - `set_mouse_emulation`/`set_gamepad_emulation` ganham `origin` — gesto MANUAL
     (default) carimba `_emu_manual_ts`; aplicação por perfil (`origin="profile"`)
     não. Um `gamepad on` na mão trava o applier de perfil por 30 s.
   - Os 3 callsites de ativação (IPC switch, autoswitch, hotkey) passam a injetar
     `apply_profile_mouse` em vez de `set_mouse_emulation` cru.
   - `point_and_click.json`: match estreitado para `["GrimFandango", "grim"]`
     (o port Linux do Grim Remastered é NATIVO, não roda sob ScummVM).
   Testes: `test_apply_profile_mouse_respeita_lock_manual`,
   `…_aplica_apos_lock_expirar`, `…_idempotente_so_ajusta_velocidade`,
   `test_match_grim_fandango`.

3. **`BUG-MOUSE-SAVE-DROPS-SECTION-01`** — `app/draft_config.py`, `app/app.py`.
   `from_profile` populava `MouseDraft(dirty=False)` e `to_profile` só emitia a
   seção com `dirty=True` → abrir um perfil que JÁ tem seção mouse (point_and_click)
   e salvar (mesmo sem tocar a aba Mouse) DESCARTAVA a seção silenciosamente —
   o fluxo default de "Salvar Perfil" (nome pré-preenchido do perfil ativo)
   destruía a feature central. **Fix:** `MouseDraft` ganha `in_profile` (separa
   "veio de um perfil" de "tocado nesta sessão"); `from_profile` seta
   `in_profile=True` quando `profile.mouse` existe; o overlay do bootstrap
   (`app.py`) preserva `in_profile` via `model_copy(update=...)` em vez de
   reconstruir o draft; `to_profile` emite quando `dirty OR in_profile`;
   `to_ipc_dict` mantém o gate SÓ-`dirty` (o "Aplicar" não pode religar emulação
   viva — A2 preservado). Testes: `test_roundtrip_perfil_com_mouse_preserva_secao`,
   `test_to_ipc_dict_gate_e_so_dirty_nao_in_profile`.

### MEDIUM

4. **`INSTALL-PROFILES-COPY-IF-ABSENT-01`** — `scripts/install_profiles.sh`.
   O installer só copiava presets quando o dir de perfis estava VAZIO → em
   upgrade (o caso da Vitória, 10 perfis da v3.10) o `point_and_click` NUNCA
   chegava — feature morta. **Fix:** copy-if-absent de TODOS os presets (paridade
   com o `meu_perfil.json`), nunca sobrescrevendo perfis editados. Validado ao
   vivo: copiou só o `point_and_click.json` faltante (10→11 perfis).

5. **`BUG-EMU-DEVICE-RACE-01`** — `daemon/lifecycle.py`.
   `set_mouse_emulation` passou a rodar também na thread do executor (hotkey de
   ciclo via `_run_blocking(activate)`), concorrendo com o event loop
   (IPC/autoswitch); o check-then-act sem lock em `start_mouse_emulation` podia
   criar 2 devices uinput e vazar 1. **Fix:** `_emu_lock` (RLock) serializa as
   transições de device em `set_mouse_emulation`/`set_gamepad_emulation`.

6. **`BUG-MOUSE-SLIDER-PREF-LOSS-01`** — `app/actions/mouse_actions.py`.
   `_refresh_mouse_from_daemon_async` sobrescrevia edição pendente (dirty) dos
   sliders ao revisitar a aba → perdia a preferência e persistia o valor do
   daemon. **Fix:** guard `if draft.mouse.dirty: return` no sync.

7. **`BUG-TEST-DBUS-NOTIFY-NONHERMETIC-01`** — `tests/unit/test_profile_suppression_lock.py`.
   Os testes disparavam ~12 notificações D-Bus REAIS por run (popups "Modo jogo"
   na tela da Vitória em COSMIC). **Fix:** fixture autouse que stubba
   `notify_emulation_suppressed`.

### LOW

8. **`BUG-MOUSE-TOGGLE-STALE-REVERT-01`** — o revert do toggle usava o valor
   capturado no clique (`not enabled`); dois toggles rápidos com daemon travado
   deixavam o switch preso ON. **Fix:** reverte para o último estado CONFIRMADO
   (`draft.mouse.enabled`).
9. **`BUG-MOUSE-RESTORE-DEFAULT-LIES-01`** — "Restaurar Default" usava
   `_refresh_mouse_from_draft` (não sincroniza com o daemon vivo) →  aba mentia
   com emulação viva. **Fix:** usa `_refresh_mouse_tab`.
10. **`BUG-AUTOSWITCH-LOG-KEY-STUCK-01`** — a chave do rate-limit do log só
    zerava dentro de `_activate` (que não roda com candidate==current) → o
    próximo episódio de supressão não logava. **Fix:** reset também no run-loop a
    cada tick quando a supressão cessa (`_suppression_active()`). Teste via
    `run()` real: `test_run_reabre_log_com_candidato_estavel_igual_ao_corrente`.
11. **`BUG-TEST-UINPUT-HASH-COLLISION-01`** — o fake uinput usava
    `hash(name) & 0xFFFF` (randomizado por `PYTHONHASHSEED`) → colisão
    `REL_X==REL_Y` flaky. **Fix:** códigos por índice sequencial (`enumerate`).
12. **`BUG-TEST-TOUCHPAD-SYSFS-NONHERMETIC-01`** — `find_dualsense_touchpad_evdev`
    lê `/sys/class/input/` real; com o daemon rodando, seus nós uinput faziam o
    teste flakear. **Fix:** fixture autouse isola `_is_virtual_evdev` na classe.
13. **Docs de protocolo** — `docs/protocol/ipc-unix-socket.md` referenciava
    método inexistente `daemon.mouse.set` e não documentava o contrato
    `enabled`-opcional de `mouse.emulation.set`. **Fix:** corrigido + rota
    speed-only documentada + comportamento do restore.

## Segunda rodada (re-auditoria adversarial das próprias correções)

Uma re-auditoria (6 auditores + verificadores por maioria) achou que o fix #3
(in_profile) tinha introduzido um NOVO HIGH, mais alguns menores. Corrigidos:

14. **`BUG-MOUSE-OVERLAY-CLOBBERS-SECTION-01` (HIGH — introduzido pelo fix #3)** —
    `app/app.py`, `app/actions/mouse_actions.py`. O overlay do estado vivo do
    daemon (`draft.mouse.model_copy(update=vivo)`) preservava `in_profile=True`
    mas SOBRESCREVIA enabled/speed/scroll com o vivo. Quando o lock manual
    bloqueava a ativação do point_and_click (gamepad on + focar Grim em <30s), o
    vivo divergia (mouse off/6) do perfil (on/8); ao Salvar Perfil, o vivo era
    persistido por cima — re-quebrando a feature. **Fix:** o overlay (bootstrap e
    refresh da aba) SÓ se aplica a perfis SEM seção mouse (`not in_profile`). Para
    perfil COM seção, a aba mostra o valor do PERFIL (= o que será salvo); editar
    a aba (dirty) é o caminho para mudar a seção. Teste do cenário:
    `test_bootstrap_perfil_com_mouse_nao_clobbera_com_vivo`.
15. **`BUG-PROFILE-MOUSE-IDEMPOTENT-STALE-CONFIG-01` (LOW)** —
    `daemon/lifecycle.py`. A idempotência de `apply_profile_mouse` confiava em
    `config.mouse_emulation_enabled`; no boot, config pode ser True com o device
    morto (uinput falhou no start) → ativar o perfil só ajustava velocidade (no-op)
    em vez de religar. **Fix:** `actual_on = config AND _mouse_device is not None`.
    Teste: `test_apply_profile_mouse_recupera_config_stale_sem_device`.
16. **`INSTALL-PROFILES-RESPECT-DELETION-01` (LOW)** — `scripts/install_profiles.sh`.
    O copy-if-absent ressuscitava um preset que a usuária deletou de propósito.
    **Fix:** marker `.seeded_presets` — só copia presets ausentes E ainda-não-
    semeados; presets presentes na 1ª execução são registrados sem cópia, então
    deleções posteriores são respeitadas. Validado: point_and_click chega no
    upgrade mas NÃO ressuscita após deleção+reinstalação.
17. **Testes fracos** — `test_hotkey_profile_cycle.py` (`_FakeManager` agora
    REGISTRA os appliers → prova que o hotkey injeta `apply_profile_mouse`/
    `apply_profile_suppression`, não os setters crus) e
    `test_bootstrap_perfil_com_mouse_nao_clobbera_com_vivo` (amarra overlay+save).

Achado refutado: "match estreitado pode não casar o wm_class real do Grim" — não
verificável sem o jogo aberto; documentado como pendência de validação ao vivo.

## Proof-of-work

```bash
.venv/bin/pytest tests/unit -q            # verde
.venv/bin/ruff check src/ tests/          # limpo
.venv/bin/mypy src/                        # limpo
./scripts/check_anonymity.sh
python3 scripts/validar-acentuacao.py --all
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=usb HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=bt  HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke --bt
```

Validação ao vivo (controle USB, daemon do systemd — NÃO rodar smokes com o
daemon vivo: o smoke faz takeover single-instance e mata o daemon):
1. `install_profiles.sh` → `point_and_click` em `profile list` (feito, 10→11).
2. `gamepad on` na mão + `profile.switch point_and_click` dentro de 30 s → o
   gamepad SOBREVIVE e o mouse NÃO liga (lock manual).
3. Focar o Grim Fandango → autoswitch ativa `point_and_click` → cursor liga.
4. Salvar o `point_and_click` na GUI sem tocar a aba Mouse → a seção mouse
   PERMANECE no JSON.
5. Reboot → o estado de emulação (gamepad/mouse) segue os flags, não é invertido.

## Fora de escopo (V3.12+)

- Modo Nativo (release total do controle p/ Sackboy) — release total global +
  perfil por-jogo.
- Unificação do `dsx.sh` no hefesto (absorver o seguro + botão).
- Instabilidade da GUI (piscar/redimensionar) — diagnóstico ao vivo + 2 preset
  combos restantes.
