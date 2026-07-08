# FEAT-MOUSE-CURSOR-FEEL-01 — Cursor digno: pipeline float + expo + carry, persistência de velocidade, fix HID-raw

**Tipo:** feat + fix (médio — daemon/integrations, zero GUI).
**Wave:** V3.11.
**Estimativa:** 1-2 iterações.
**Dependências:** nenhuma (independente de BUG-MOUSE-GUI-SYNC-01; tocam arquivos
disjuntos exceto `lifecycle.py` — coordenar merge).
**Status:** READY.

---

**Tracking:** labels `type:feat`, `hardware`, `mouse-emu`, `ai-task`, `status:ready`.

## Contexto

Diagnóstico 2026-07-03, achados A5-A7, todos confirmados com repro numérica:

1. **A7 — cursor lento e quantizado** (`uinput_mouse.py:108-113`): fórmula
   `int((raw-128)/128 * speed)` por tick de 60 Hz, linear, truncada, sem acumulador
   (o touchpad TEM carry — `uinput_mouse.py:355-361` — o stick não). Medido com o
   código real:
   - speed=6 (default): máx 300 px/s (1920px em 6,4s); só 5 velocidades discretas
     (60/120/180/240/300 px/s), saltos de 60 px/s; menor movimento possível = 60 px/s.
   - speed=12 (máx): 660 px/s — ainda 3-6x mais lento que um mouse real em uso
     deliberado (~1000-4000 px/s em flicks).
   - speed=1: INCAPAZ de mover para direita/baixo (trunca a 0 em todo o range
     positivo); speed=2 exige ≥50% de deflexão.
   - Assimetria: máximo negativo -speed vs positivo speed-1 (360 vs 300 px/s @ 6).
   É o "velocidade não tá igual deveria estar" da Vitória — o modo mouse funciona,
   mas é inutilizável para point-and-click.
2. **A5 — velocidade não persiste**: `mouse_emulation.flag` guarda só o enabled
   (`utils/session.py:138-161`); `run_daemon` cria `DaemonConfig` do zero
   (`daemon/main.py:74-84`) → após restart, speed/scroll voltam a 6/1. Precedente
   idiomático no repo: `gamepad_emulation.flag` já guarda DADO no conteúdo (flavor,
   `session.py:167-198`).
3. **A6 — fallback HID-raw converte stick errado** (`backend_pydualsense.py:620-623`):
   `int(state.LX) & 0xFF` assume 0-255, mas a pydualsense 0.7.5 instalada armazena
   `state.LX = states[1] - 128` (range -128..127, centrado em 0). Repouso cru=128 →
   LX=0 → raw=0 → dx=-6 (cursor voa na diagonal); cru=125 → raw=253 (bate com a
   memória "sticks ~253 em repouso"). O ramo dispara quando o evdev não está
   disponível (SDP HID ausente em BT, permissão, node não encontrado) e contamina
   também gamepad virtual, scroll e o check de neutralidade
   (`ipc_handlers.py:255`). Gatilhos NÃO são afetados (já são 0-255 crus).

## Decisão

1. **Pipeline float com carry no stick** (substitui `_compute_move`/`_emit_move` em
   `uinput_mouse.py`):
   - Normalizar radialmente: `nx=(lx-128)/128`, `ny=(ly-128)/128`, `mag=hypot(nx,ny)`.
   - Deadzone radial REESCALADA: `m = max(0, (mag - dz) / (1 - dz))` com `dz=20/128`
     — resposta começa em 0 logo após a deadzone (elimina o degrau 0→60 px/s).
   - Curva expo: `curved = m ** MOUSE_EXPO` com `MOUSE_EXPO = 1.6` (constante de
     módulo; configurabilidade fica fora de escopo).
   - Velocidade alvo em px/s float: `vel = curved * (speed * MOUSE_PX_PER_SEC_STEP)`
     com `MOUSE_PX_PER_SEC_STEP = 125.0` → speed 6 = 750 px/s máx, speed 12 =
     1500 px/s máx, speed 1 = 125 px/s máx (todas as speeds passam a FUNCIONAR).
   - Delta por tick: `vel * (1/poll_hz)` distribuído por eixo proporcional a
     `nx/mag, ny/mag`, acumulado em `_stick_carry_x/_stick_carry_y` (mesmo padrão do
     `_tp_carry_*`), emitir `int()`, manter resto. Simétrico em ambas as direções.
   - O período do tick vem do poll loop; passar `poll_hz` (ou o período) ao device na
     criação para não hardcodar 60.
2. **Persistir speed/scroll no flag** (padrão flag-com-conteúdo do gamepad):
   - `save_mouse_emulation(enabled, speed=None, scroll_speed=None)` — quando enabled,
     escreve JSON `{"speed": N, "scroll_speed": M}` no `mouse_emulation.flag`; unlink
     quando desligado (preserva semântica existe=ligado).
   - `load_mouse_emulation() -> (bool, int|None, int|None)` tolerante ao conteúdo
     legado `"1\n"` (JSONDecodeError → speeds None → defaults).
   - Wrappers com os nomes antigos podem permanecer para não tocar testes legados.
   - `subsystems/mouse.py:97` salva com as velocidades da config; em
     `set_mouse_emulation` (ramo enabled com device já vivo, `lifecycle.py:416-420`)
     re-salvar o flag após `set_speed` — cobre mudança de velocidade com mouse já
     ligado (start retorna cedo).
   - Restore no boot (`lifecycle.py:236-238`): aplicar com clamp 1-12/1-5.
3. **Fix do fallback HID-raw** (`backend_pydualsense.py:620-623`):
   `raw_lx = max(0, min(255, int(state.LX) + 128))` (idem LY/RX/RY). NÃO tocar
   l2_raw/r2_raw. Teste unitário sem hardware espelhando o repro: injetar report USB
   de 64 bytes com sticks 128/125 via `readInput` real da pydualsense e afirmar
   raw 128/125 e `_compute_move`≈0.

## Critérios de aceite

- [ ] Tabela de regressão do pipeline: deflexão 0%, 16% (borda da deadzone), 30%,
      60%, 100% → px/s esperados para speed 1, 6 e 12 (teste paramétrico com
      tolerância; validar simetria positivo/negativo e resposta contínua sem degrau).
- [ ] Carry: deflexão constante pequena (ex.: 20% @ speed 6) acumula movimento
      sub-pixel e emite ~N px após M ticks (sem zerar como hoje).
- [ ] speed=1 move em TODAS as direções.
- [ ] Flag JSON: ligar com speed=9/scroll=3 → restart (simulado) → daemon restaura
      9/3 (teste com XDG isolado). Conteúdo legado `"1"` → defaults sem crash.
- [ ] Fallback HID-raw: repouso cru 128 e 125 → raw 128/125, cursor parado.
- [ ] Scroll continua funcional (deadzone 40, rate-limit 50ms — sem mudança).
- [ ] Touchpad-cursor (B4) continua funcional (carry existente intocado).
- [ ] Suite completa verde; ruff/mypy limpos; smoke USB e BT sem traceback.

## Arquivos tocados

- `src/hefesto_dualsense4unix/integrations/uinput_mouse.py` (pipeline novo,
  constantes, docstring da política).
- `src/hefesto_dualsense4unix/utils/session.py` (flag JSON).
- `src/hefesto_dualsense4unix/daemon/subsystems/mouse.py` (save com velocidades;
  passar poll_hz ao device).
- `src/hefesto_dualsense4unix/daemon/lifecycle.py` (restore com clamp; re-save no
  set_speed).
- `src/hefesto_dualsense4unix/core/backend_pydualsense.py` (+128 no fallback).
- `tests/unit/test_uinput_mouse*.py` (reescrever casos de `_compute_move`),
  `tests/unit/test_session*.py`, `tests/unit/test_backend_fallback_sticks.py` (novo).

## Proof-of-work runtime

```bash
.venv/bin/pytest tests/unit -q
.venv/bin/ruff check src/ tests/
.venv/bin/mypy src/
./scripts/check_anonymity.sh
python3 scripts/validar-acentuacao.py --all
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=usb HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=bt  HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke --bt

# Cenário manual (validação da Vitória, controle via BT):
# 1. dsx mouse on --speed 6: atravessar a tela deve levar ~2,5s em deflexão total
#    (750 px/s em 1920px), com micro-ajuste suave perto do centro.
# 2. dsx mouse on --speed 9/12: sensivelmente mais rápido, sem "saltos".
# 3. Reiniciar o daemon → dsx mouse status mostra speed persistido.
```

## Notas para o executor

- O clamp 1-12 do slider/CLI NÃO muda (contrato IPC estável); muda só o que cada
  nível significa (px/s). Documentar a tabela nível→px/s no docstring.
- `MOUSE_EXPO` e `MOUSE_PX_PER_SEC_STEP` são constantes de módulo com comentário —
  não viram config de usuário nesta sprint.
- Cuidado com testes existentes que fixam `int((raw-128)/128*speed)` — reescrever
  para o contrato novo (px/s), não "consertar" o valor esperado.
- O device é criado em `subsystems/mouse.py:42-45` e `81-84` — os dois callsites
  precisam do poll_hz.
- Verificar interação com o throttle do report_thread BT (~125 Hz): o poll de 60 Hz
  segue mandando; nenhuma dependência de transporte deve entrar no cálculo.
- Fix do A6 é cirúrgico: somar 128 e clampar. Não refatorar o fallback inteiro.

## Fora de escopo

- Scroll de alta resolução (REL_WHEEL_HI_RES) e curva de scroll.
- Expo configurável por perfil/GUI.
- Modificador de precisão (segurar botão reduz velocidade) — candidato a sprint
  futura se a Vitória sentir falta.
- Persistência de velocidade por PERFIL (entra na FEAT-POINT-AND-CLICK-01 via seção
  mouse do Profile).
