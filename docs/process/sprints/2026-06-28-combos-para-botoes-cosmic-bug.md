# FEAT-DSX-COMBO-TO-SEGMENTED-01 — Dropdowns → botões segmentados (bug do cosmic-comp)

## Por quê (causa raiz, já PROVADA ao vivo)

Na COSMIC (System76) o **cosmic-comp** rouba o foco da janela no clique, então
popups de `GtkComboBox` fecham na hora — em XWayland ~95%, Wayland nativo ~40-100%.
É bug do compositor ([cosmic-epoch#2497](https://github.com/pop-os/cosmic-epoch/issues/2497),
[pop#3660](https://github.com/pop-os/pop/issues/3660), NVIDIA), NÃO do app: até um
combo limpo e estático fecha (`scripts/teste_combo.py` comprova). Único conserto:
**não usar dropdown**. Botões sempre visíveis (sem popup/grab) são imunes.

O seletor de controle-alvo já foi convertido assim (commit ee832af, em
`app/actions/status_actions.py`: `_rebuild_target_buttons`/`_set_target_active` com
`GtkRadioButton` em modo toggle + classe "linked"). **Use isso como template.**

## Escopo

Converter para botões segmentados os 3 combos de POUCAS opções:
1. `trigger_left_mode` (modo do gatilho esquerdo)
2. `trigger_right_mode` (modo do gatilho direito)
3. `profile_aplica_a_combo` (a quem o perfil se aplica)

NÃO mexer agora em `trigger_left_preset_combo` / `trigger_right_preset_combo`
(presets = muitos itens; ficam para outra UI num passo futuro). Deixe-os como estão.

## Como (sem quebrar a semântica existente)

Os call sites usam a API por-ID do combo. Levante TODOS antes de mexer:
`grep -rn "set_active_id\|get_active_id\|trigger_left_mode\|trigger_right_mode\|profile_aplica_a_combo" src`.
Fatos já levantados:
- `triggers_actions.py`: `combo.set_active_id("Off"|trigger_draft.mode|"custom")`,
  `combo.get_active_id()`; handler `on_trigger_left/right_mode_changed(combo)` chama
  `combo.get_active_id()`; há `self._guard_refresh` que suprime o "changed" no load.
- `profiles_actions.py`: `combo.set_active_id("any"|target_id)`,
  `combo.get_active_id()`; conecta dois handlers ao "changed"
  (`_on_aplica_a_changed` e um lambda de `_refresh_preview`).
- IMPORTANTE: `GtkComboBox.set_active_id` EMITE "changed". O código depende disso
  (ex.: refresh de preview). O widget novo DEVE emitir "changed" no `set_active_id`
  também; os guards existentes (`_guard_refresh`) cuidam da supressão no load.

### Widget novo: `SegmentedSelector` (app/widgets/segmented_selector.py)

`class SegmentedSelector(Gtk.Box)` com sinal GObject `"changed"` (via `__gsignals__`
ou `@GObject.Signal`), orientação horizontal, classe de estilo "linked". API que
espelha o subconjunto do combo usado:
- `set_items(items: list[tuple[str, str]])` — `(id, label)`; reconstrói os
  `GtkRadioButton` (modo toggle, agrupados), preservando o id ativo se ainda existir.
- `get_active_id() -> str | None`
- `set_active_id(id: str) -> None` — ativa o botão do id e EMITE "changed"
  (igual ao GtkComboBox). Guard interno evita loop ao marcar programaticamente os
  outros botões do grupo como inativos.
- `connect("changed", cb)` nativo (sinal GObject). O 1º arg do cb é o widget.
- Idempotência: `set_items` não reconstrói se os itens forem idênticos.

### Integração (Glade + código)

Os combos vêm do `main.glade` via GtkBuilder. Para trocar por um widget Python:
- No `main.glade`, troque cada um dos 3 `GtkComboBoxText` por um `GtkBox` vazio
  (placeholder) com um id de slot (ex.: `trigger_left_mode_slot`). Remova o
  `<signal name="changed" .../>` do Glade (vamos conectar no código). Os ITENS
  estáticos do combo, se houver no Glade (`<items>`), viram a fonte de `set_items`
  no código; se os itens forem populados em código, reaproveite essa lista.
- No `_init_*` correspondente (triggers_actions / profiles_actions), crie o
  `SegmentedSelector`, popule via `set_items(...)` com os MESMOS pares (id,label)
  de antes, empacote no slot, conecte os mesmos handlers ao "changed" e guarde a
  referência (ex.: `self._trigger_mode["left"] = sel`).
- Atualize os call sites que faziam `self._get("trigger_left_mode")` para usar a
  referência guardada do `SegmentedSelector` (mesma API `get_active_id`/
  `set_active_id`). Confirme que `on_trigger_*_mode_changed` recebe o widget e
  `get_active_id()` funciona.
- `_update_preset_row_visibility` e o resto da lógica de gatilho devem continuar
  idênticos (só muda a fonte do `get_active_id`).

### Rótulos

Mantenha rótulos curtos (banner/aba estreita). Para os modos, use os labels atuais
(ou abreviados com tooltip). Para `profile_aplica_a`, idem.

## Gate (obrigatório, tudo verde antes do commit)

```
.venv/bin/ruff check src tests
.venv/bin/python -m mypy src/hefesto_dualsense4unix
.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q
python3 scripts/validar-acentuacao.py --all   # mantenha limpas só as linhas tocadas
bash scripts/check_anonymity.sh                # após git add
```
- Smoke real do widget (precisa de display): instancie `SegmentedSelector`,
  `set_items([("Off","Off"),("custom","Custom")])`, `set_active_id("custom")`,
  confira `get_active_id() == "custom"` e que só 1 botão fica ativo. (Veja o smoke
  do seletor: `DISPLAY=:1 GDK_BACKEND=x11 .venv/bin/python - <<PY ...`.)
- Atualize/!crie testes unit para o `SegmentedSelector` (mock de display: teste a
  lógica de id/itens sem criar GtkRadioButton real, como em
  `tests/unit/test_multi_controller_ui.py` que mocka `_rebuild_target_buttons`).
- Adicione testes para os call sites convertidos se houver testes existentes deles.

## Entrega

Commit no branch atual (`feat/dsx-definitive-fix-usb-hdmi`) + `git push origin main`
(o branch local já espelha main no fluxo deste repo). Mensagem de commit em pt-BR,
sem nome do fork (o hook de anonimato sanitiza). Reporte: o que converteu, números
do gate, e o que ficou pendente (os 2 preset combos).

## NÃO fazer

- NÃO converter os preset combos (fica para depois).
- NÃO flipar o backend pra Wayland (decisão da mantenedora foi botões).
- NÃO mexer no daemon, hardware, ou rodar a GUI/applet (sem display no agente).
