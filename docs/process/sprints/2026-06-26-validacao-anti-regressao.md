# Sprint de validação — caçar os "errinhos" antes que cheguem ao controle

> Motivação (Vitória): "quero uma sprint pra validação pra achar esses tipos de erros
> pequenos que temos aqui." Os bugs desta sessão (vazamento de Meta, modificador travado,
> toggle que não persistia, evdev estagnado, limiar não-configurável) eram **todos
> detectáveis por teste** — mas a suíte **nem estava sendo rodada**.

## Achado de base
`./.venv/bin/python -m pytest` falha: **`No module named pytest`** — as deps de teste não estão
instaladas no venv. Ou seja: existe suíte em `tests/`, mas ninguém a executa localmente. **Primeiro
passo de tudo: tornar a suíte executável e rodá-la.**

## V0. Tornar a suíte rodável (bloqueia o resto)
- [ ] `./.venv/bin/pip install -e ".[dev]"` (ou `pytest pytest-asyncio`); confirmar extra `dev`
      no `pyproject.toml` (criar se faltar).
- [ ] `pytest -q` verde como baseline. Anotar quantos testes existem e o que cobrem.
- [ ] Adicionar alvo `make test` / seção no `install.sh --dev` para não regredir.

## V1. Testes de regressão para os bugs DESTA sessão
Cada um é unitário e rápido (sem hardware — usa `HotkeyManager`/devices fake):
- [ ] **combo não vaza** (FEAT-HOTKEY-COMBO-NO-LEAK-01): `combo_buttons_active(["ps","options"])
      == {"ps","options"}`; `["options"] == {}`. (lógica já validada à mão nesta sessão — virar teste.)
- [ ] **long-press configurável/desligável**: `ps_long_press_ms=0` não dispara em hold de 2s;
      `=1000` dispara. (4 cenários já validados à mão — virar teste.)
- [ ] **combo gamemode** dispara `on_ps_long_press` e **suprime o PS-solo** (não abre Steam).
- [ ] **flush ao suprimir** (FEAT-EMULATION-GAMEMODE-FLUSH-01): com Meta "pressionado" no device
      virtual, `set_emulation_suppressed(True)` zera `active_keys()`.
- [ ] **persistência do mouse** (FEAT-MOUSE-PERSIST-01): `save_mouse_emulation_enabled(True)` →
      `load_…()==True`; após "restart" simulado o startup liga a emulação. E `False` remove o flag.
- [ ] **config chega ao HotkeyManager**: `start_hotkey_manager` propaga `ps_long_press_ms`
      (o bug-raiz era a config nunca chegar).

## V2. Smoke-test de integração ao vivo (CLI `doctor --emulation` ou script)
Um comando que, com o daemon rodando, verifica em segundos e reporta PASS/FAIL:
- [ ] controle conectado e **input vivo** (não estagnado): `battery_pct` muda OU `state` não-neutro;
      ausência de `state_stale_neutral_warning` recente.
- [ ] devices virtuais presentes (mouse REL+KEY, teclado KEY) e **sem tecla/modificador preso**
      (`active_keys()` vazio em repouso) — pega Meta/Ctrl travado.
- [ ] emulação ON + não-suprimida ⇒ mover o stick gera REL no device virtual (reaproveitar o
      `emu_monitor.py` desta sessão como base).
- [ ] touchpad do DualSense com `LIBINPUT_IGNORE_DEVICE=1` (não duplica ponteiro).
- [ ] `ps_long_press_ms` efetivo == esperado (lê do daemon).

## V3. Guardas contra as classes de erro que vimos
- [ ] **Estado preso**: qualquer subsistema que faça press/release num device virtual deve ter
      um "release-all" no teardown e na supressão (auditar mouse, teclado, gamepad).
- [ ] **Config fantasma**: lint/asserção garantindo que todo campo de `HotkeyConfig`/`DaemonConfig`
      relevante é realmente lido (o `ps_long_press_ms` provou que dá pra ter campo morto).
- [ ] **Persistência simétrica**: para todo toggle runtime (mouse, paused, futuro suppress),
      teste de "sobrevive ao restart".
- [ ] **Restart limpo**: teste/CI que reinicia o daemon 2x seguidas e falha se aparecer
      `state_stale_neutral_warning` (pega a corrida de grab — ver B1 da sprint de correção).

## V4. Higiene contínua
- [ ] `ruff`/`mypy` no CI (se já houver config, ligar no pre-commit).
- [ ] `pytest` no pre-push.
- [ ] Doc curto "como validar uma mudança de emulação" apontando pro smoke-test V2.

## Ordem sugerida
V0 → V1 (trava as regressões já corrigidas) → V2 (smoke vivo, alto valor p/ achar "errinhos") →
V3/V4 (estrutural).
