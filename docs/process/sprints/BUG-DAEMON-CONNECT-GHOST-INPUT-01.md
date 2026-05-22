# BUG-DAEMON-CONNECT-GHOST-INPUT-01 — Ao conectar, microfone muta e teclas disparam sozinhas (estado inicial fantasma)

**Tipo:** fix (daemon/input).
**Wave:** V3.6 — acabamento COSMIC round 2 (uso real).
**Estimativa:** M — 1–2 iterações; concorrência/estado + testes.
**Dependências:** nenhuma.
**Status:** DONE (implementado + testes unit verdes; smoke real pendente da mantenedora).

---

## Contexto

Relato da mantenedora (Pop!_OS COSMIC + DualSense USB, 2026-05-21):

> "ao conectar o controle ele **muta** e fica **aleatório os comandos**."

Ou seja: no instante em que o DualSense é conectado, (a) o **microfone do sistema
é mutado** sozinho e (b) o desktop "enlouquece" — janelas trocam, launcher abre,
PrintScreen dispara, teclado virtual aparece — sem o usuário tocar em nada.

Por padrão o daemon sobe com `keyboard_emulation_enabled=True` e
`mic_button_toggles_system=True` (`daemon/lifecycle.py:72,82`). A emulação de
mouse fica OFF por padrão, então o sintoma é de **teclado + microfone**.

## Diagnóstico (causa-raiz)

O estado **inicial cru** lido no momento da conexão é tratado como input real,
sem nenhum período de assentamento:

1. **`previous_buttons` nasce vazio** — `daemon/lifecycle.py:403`. No 1º tick após
   conectar, `pressed_now = current_buttons - previous_buttons = current_buttons`.
   Qualquer botão presente no estado inicial vira um `BUTTON_DOWN`
   (`lifecycle.py:458-463`).
2. **`mic_btn` vem de HID-raw cru** — `core/backend_pydualsense.py:149-153` lê
   `ds.state.micBtn`; o próprio comentário admite "primeiro tick pode ter state
   cru antes do firmware enviar o primeiro report completo". Se vier `True`,
   `mic_btn` entra em `state.buttons_pressed` → `BUTTON_DOWN("mic_btn")` →
   `mic_button_loop` (`daemon/subsystems/hotkey.py:80-108`) chama
   `toggle_default_source_mute()` → **muta o microfone** + acende o LED do mic.
3. **`UinputKeyboardDevice.dispatch` é edge-triggered com `_pressed_buttons`
   vazio** — `integrations/uinput_keyboard.py:163-183`. No 1º dispatch após a
   conexão, `newly_pressed = now_mapped - frozenset()` = **todos** os botões
   mapeados presentes no snapshot evdev → emite a sequência de cada um. Bindings
   default (`core/keyboard_mappings.py:41-63`): `options→Super`, `r1→Alt+Tab`,
   `l1→Alt+Shift+Tab`, `create→PrintScreen`, `l3→abre OSK` — **os "comandos
   aleatórios"**.
4. **Sem grace-period pós-conexão** — `daemon/connection.py` (connect/
   `reconnect_loop`) e o `_poll_loop` despacham input imediatamente; o estado
   inicial (HID sujo + snapshot evdev ainda populando) não é descartado.

## Decisão / Entrega

Introduzir um **período de assentamento pós-conexão (settling/grace)** + um
**baseline de botões no 1º tick**, sem desabilitar nenhuma feature:

1. **Baseline no 1º tick conectado**: ao detectar a borda *desconectado→conectado*
   dentro do `_poll_loop` (hoje o loop faz `continue` enquanto desconectado —
   `lifecycle.py:411-417`), inicializar `previous_buttons = current_buttons` e
   semear o edge-tracker do teclado (`UinputKeyboardDevice._pressed_buttons`) com
   o mesmo baseline. Assim botões já "pressionados"/fantasma no instante da
   conexão **não** geram evento — só disparam quando o usuário soltar e
   pressionar de novo.
2. **Grace-period**: novo atributo no `Daemon` (ex.: `_input_ready_at: float`)
   setado no momento da conexão para `now + GRACE` (sugestão 250–400 ms). Enquanto
   `loop.time() < _input_ready_at`, o `_poll_loop` **não** despacha
   teclado/mouse/hotkey nem publica `BUTTON_DOWN`/`BUTTON_UP` (continua lendo
   estado, atualizando store e publicando `STATE_UPDATE`/bateria normalmente —
   só o input emulado é suprimido). Cobre o `mic_btn` fantasma sem tocar no
   backend (preferível: o gate no poll loop barra o mute na origem).
3. **Rearmar em reconexão**: `connection.reconnect()` e o ramo de reconnect do
   `_poll_loop` (`lifecycle.py:424-428`) e a transição online do `reconnect_loop`
   (`connection.py:136-152`) devem rearmar `_input_ready_at` + zerar o baseline.
4. **Testes** (`tests/unit/`): com `FakeController` retornando botões já no
   primeiro `read_state` (incl. `mic_btn`): assert que **nenhum** `BUTTON_DOWN`,
   tecla emulada ou `toggle_default_source_mute` ocorre durante o settling; assert
   que pressionar **depois** do settling emite normalmente; assert rearmar em
   reconexão.

## Critérios de aceite

- [ ] Conectar o controle **não muta** o microfone do sistema nem dispara
      teclas/atalhos sozinho.
- [ ] Após o grace-period, tudo funciona: emulação de teclado, toggle manual do
      mic (apertando o botão de verdade), mouse quando ligado.
- [ ] Botão **fisicamente segurado** durante a conexão não dispara ação até ser
      solto e re-pressionado.
- [ ] Reconexão (unplug/replug) reaplica o settling.
- [ ] Testes unit cobrindo baseline de 1º tick, grace-period e `mic_btn` fantasma.
- [ ] Gates: `ruff`, `mypy --strict`, `pytest tests/unit -q`,
      `validar-acentuacao.py --all`, `check_anonymity.sh`.
- [ ] Proof-of-work: `journalctl --user -u hefesto-dualsense4unix -f` mostrando o
      settling no connect + smoke real conectando o controle sem efeitos fantasma.

## Arquivos tocados (previsão)

- `src/hefesto_dualsense4unix/daemon/lifecycle.py` — `_poll_loop` (borda de
  conexão, baseline, gate de dispatch por `_input_ready_at`) + campo no `Daemon`.
- `src/hefesto_dualsense4unix/daemon/connection.py` — setar/rearmar settling no
  connect/reconnect/reconnect_loop.
- `src/hefesto_dualsense4unix/core/backend_pydualsense.py` — apenas se a
  supressão de `mic_btn` no poll loop não bastar (preferir não tocar).
- `tests/unit/test_daemon_*.py` / `tests/unit/test_poll_*.py` (novos casos).

## Notas para o executor

- `previous_buttons` é **local** do `_poll_loop`; o estado de settling precisa
  sobreviver entre ticks → use atributo no `Daemon` (já há vários `_campo: Any`).
  Detecte a borda conectado dentro do loop (a 1ª iteração em que
  `controller.is_connected()` vira True após ter sido False).
- O `EvdevReader._reset_on_disconnect` (`core/evdev_reader.py:237-243`) já limpa
  botões ao cair — bom; o snapshot pode demorar a popular ao reconectar, e o
  grace cobre essa janela.
- Para semear o edge-tracker do teclado, há a opção de expor um método no
  `UinputKeyboardDevice` (ex.: `prime(buttons)`) que seta `_pressed_buttons` sem
  emitir — análogo ao racional de `_release_all`. Evita gambiarra acessando
  atributo `_`-privado de fora.
- **Não desligar features**: `keyboard_emulation_enabled=True` segue default; o
  fix é sobre o **estado inicial**, não sobre desabilitar emulação.
- **Nota sobre o "muta" de áudio de saída**: se, mesmo após este fix, o **som do
  sistema** (não o microfone) baixar/trocar ao conectar o DualSense, isso é o
  PipeWire/WirePlumber trocando o *default sink* para a placa de áudio USB do
  controle — comportamento do SO, **fora do escopo** desta sprint (abrir sprint
  dedicada de política de áudio se confirmado). Este fix resolve o mute do
  **microfone** causado pelo próprio Hefesto.
- **Não** editar `CHANGELOG.md` nem `SPRINT_PLAN_COSMIC.md`. Atualize só o
  `Status:` deste arquivo ao concluir.
- Senha sudo local (se precisar de `/dev/uinput`/grupos para smoke): `***SENHA-REMOVIDA-DO-HISTORICO***`.

## Proof-of-work runtime

```bash
# unit
.venv/bin/pytest tests/unit -q -k "poll or connect or mic or keyboard"
.venv/bin/ruff check src/ && .venv/bin/mypy --strict src/hefesto_dualsense4unix
python3 scripts/validar-acentuacao.py --all
# smoke real (hardware): em um terminal
journalctl --user -u hefesto-dualsense4unix -f
# noutro: systemctl --user restart hefesto-dualsense4unix ; conectar o DualSense
# observar: settling logado, sem mute do mic, sem teclas fantasma
```

## Fora de escopo

- Redesenho dos bindings default de teclado.
- Política de áudio do sistema / autoswitch de sink do PipeWire.
- Deadzone/curvas do mouse (mouse é OFF por padrão).
