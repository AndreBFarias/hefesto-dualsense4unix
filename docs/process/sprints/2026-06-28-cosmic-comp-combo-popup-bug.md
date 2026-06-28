# BUG-COMBO-POPUP-FLICKER / cosmic-comp fecha popups (saga + resolução)

Data: 2026-06-28. Branch: `feat/dsx-definitive-fix-usb-hdmi`.

## Sintoma

Na GUI GTK, **TODOS** os combos/dropdowns abriam e fechavam na hora ao clicar,
impossibilitando escolher. A mantenedora descreveu: "pisca, às vezes acerta,
instável, tem conflito". Suspeita inicial (errada) foi do seletor de controle novo.

## Diagnóstico (o que foi descartado, pra não repetir)

1. **NÃO era o refresh do combo a 10 Hz.** Tornei idempotente (FLICKER-01) — não
   resolveu.
2. **NÃO era o re-layout dos labels dos sticks** (que tremem em repouso). Testei
   isolado: o popup SOBREVIVE ao re-layout a 10 Hz. O grab-gate (pausar render no
   grab — FLICKER-02) ajudou um pouco no Wayland mas não resolveu.
3. **NÃO era a presença do combo no banner / titlebar** (header_bar é GtkBox do
   corpo).
4. **NÃO era instalação velha** (a GUI roda do repo via `run.sh`/`.venv`; o fix
   estava carregado e mesmo assim piscava).
5. **NÃO era o backend** (x11 vs Wayland) — pisca nos dois, Wayland só menos.

## Causa raiz (PROVADA ao vivo)

É bug do **cosmic-comp** (compositor do COSMIC / System76): ele rouba o foco da
janela no instante do clique, então o popup do combo (que depende do foco) fecha.
Issues upstream: [cosmic-epoch#2497](https://github.com/pop-os/cosmic-epoch/issues/2497)
("menus close instantly, applets vanish on click"),
[pop#3660](https://github.com/pop-os/pop/issues/3660) (perda de foco com **NVIDIA
RTX 4060** — o HW dela), cosmic-comp #1815/#2064 ("Unable to re-configure
repositioned popup"). Agravado por NVIDIA + uso prolongado.

**Prova decisiva** (`scripts/teste_combo.py`, combo GTK mínimo e LIMPO, sem nosso
app): XWayland ~95% "fecha sozinho" (<400 ms, sem escolher); Wayland nativo 100%;
Wayland + grab-gate ainda ~40%. Nenhuma mudança no nosso código conserta um dropdown
nessa COSMIC. Ferramenta de diagnóstico ficou versionada em `scripts/teste_combo.py`.

## Resolução

Dropdown é insalvável → **trocar por botões sempre visíveis** (sem popup/grab →
imunes ao bug).

- **Seletor de controle-alvo** → `GtkRadioButton` em modo toggle (segmented control,
  classe "linked") no banner. Commit `ee832af` (`app/actions/status_actions.py`:
  `_init_controller_target_combo`/`_rebuild_target_buttons`/`_set_target_active`).
- **Widget reutilizável `SegmentedSelector`** (`app/widgets/segmented_selector.py`):
  Gtk.Box com sinal "changed", API por-id (`set_items`/`get_active_id`/
  `set_active_id`) espelhando GtkComboBox; lógica pura em `_SegmentedLogic`
  (testável headless); `wrap=True` usa GtkFlowBox. Commit `bc2568b`.
- **Convertidos via `SegmentedSelector`:** `trigger_left/right_mode` (têm 19 presets
  → FlowBox que quebra linha) e `profile_aplica_a_combo`. Combos viraram slots no
  `main.glade`. Commit `bc2568b`.

## Validado

- Seletor: mantenedora trocou o player-LED só no controle BT alvo (mira certo).
- Gate verde em cada etapa (1662 testes, ruff/mypy, acentuação, anonimato).
- Smoke real dos botões em display :1 (labels, single-active invariant).

## Pendente

- 2 **preset combos** (`trigger_left/right_preset_combo`): muitos itens → outra UI
  (lista rolável, sem popup) num passo futuro. Seguem dropdowns por ora.
- Reportar upstream à System76 (é bug deles). Workaround do sistema: logout/login
  reinicia o cosmic-comp.
- UX dos 19 botões de modo de gatilho: validar visualmente; se poluído, virar lista
  rolável.

## Junto nesta sessão (correlatos)

- Throttle do report_thread (USB+BT, 0 CRC); multi-controle visível; co-op local;
  seletor por-controle (output target). Popover do applet ganhou scroll
  (`max_height`) — commit `f2e3083`.
