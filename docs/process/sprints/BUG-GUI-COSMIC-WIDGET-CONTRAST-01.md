# BUG-GUI-COSMIC-WIDGET-CONTRAST-01 — Botões e dropdowns ilegíveis (branco-sobre-branco) no COSMIC

**Tipo:** fix (UI/tema).
**Wave:** V3.6 — acabamento COSMIC round 2 (pós-v3.5.0, a partir de uso real).
**Estimativa:** M — 1–2 iterações, sobretudo CSS + validação visual.
**Dependências:** nenhuma. Continua `UI-THEME-BORDERS-PURPLE-01` (tema base) e
`BUG-GUI-NOTEBOOK-HEADER-WHITE-01`/`BUG-GUI-COMBOBOX-MENU-POPUP-WHITE-01` (v3.5.0).
**Status:** DONE (CSS + theme.py + testes; validado visualmente em COSMIC/XWayland
com `GTK_THEME=Adwaita`. Botões com fundo sólido `#383a4a`/borda roxa; toggle de
política de rumble com `:checked` roxo destacado; footer `.btn-*` sobre fundo
escuro reafirmado; containers `box/frame/grid/viewport/scrolledwindow/stack`
cobertos com `:not(.card)`; TreeView body escurecido; combobox display padronizado
com `entry`; `gtk-application-prefer-dark-theme=True` defensivo).

---

## Contexto

Validação em hardware real (mantenedora, Pop!_OS COSMIC 1.0 + Wayland/XWayland +
DualSense USB, 2026-05-21) revelou que **todos os botões aparecem brancos, sem
texto legível** (texto branco sobre fundo branco) e que **as listas suspensas
(dropdowns) estão "feias"** — em **todas as abas** (Status, Gatilhos, Lightbar,
Rumble, Perfis, Daemon, Emulação, Mouse, Teclado).

Casos observados nas screenshots:
- Aba **Daemon**: footer `Aplicar / Salvar Perfil / Importar / Restaurar Default`
  todo branco; botões `Iniciar/Parar/Reiniciar/...` idem.
- Aba **Rumble**: toggles de política (`Economia / Balanceado / Máximo / Auto`) e
  `Testar / Aplicar / Parar` todos brancos.
- Aba **Teclado / Emulação**: botões de ação (add/remove/restore, testar/refresh)
  brancos.
- Aba **Perfis**: dropdown "Qualquer janela" com aparência inconsistente.

O **v3.5.0 (hoje)** já corrigiu parte do problema no `gui/theme.css`: header do
`GtkNotebook` (`BUG-GUI-NOTEBOOK-HEADER-WHITE-01`) e o popup `menu`/`menuitem`
do `GtkComboBoxText` (`BUG-GUI-COMBOBOX-MENU-POPUP-WHITE-01`). **Faltou** tratar
os próprios **botões** e o **display fechado dos combobox** — exatamente o que a
mantenedora ainda vê.

## Diagnóstico (causa-raiz)

Raiz comum: **GTK3 não tem scoping real** (anotado em `UI-THEME-BORDERS-PURPLE-01`,
"Notas para o executor"). O nosso `Gtk.CssProvider` entra com
`GTK_STYLE_PROVIDER_PRIORITY_APPLICATION` (600 > tema 200), mas **só vence onde há
seletor nosso**. Widgets/containers/estados não cobertos caem no tema GTK do
sistema — que **no COSMIC é claro** (a sessão não aplica a variante escura por
padrão). Daí o branco.

1. **Botões** — `src/hefesto_dualsense4unix/gui/theme.css:9-15`:
   ```css
   .hefesto-dualsense4unix-window button {
       background-color: transparent;   /* ← mostra o container atrás */
       ...
       color: #f8f8f2;                  /* texto branco */
   }
   ```
   `transparent` faz o botão exibir o fundo do container pai (`GtkBox`/`GtkFrame`/
   `GtkButtonBox`/`GtkGrid`), que **não tem `background-color` no nosso CSS** →
   pintado claro pelo tema do sistema no COSMIC. Botão claro + texto branco =
   **branco-sobre-branco**. Atinge `GtkButton` e `GtkToggleButton` (rumble policy).
   Os `.btn-*` do footer (`theme.css:211-237`) também: o `background-image`
   (gradiente alpha baixo) é pintado **sobre o transparente** → some sobre claro.

2. **Combobox (display fechado)** — `theme.css:29-52`: cobrimos `combobox`,
   `combobox button/label/cellview/box/arrow`, mas no COSMIC o conjunto ainda
   destoa (borda/seta/altura/contraste). O popup (`menu`) foi coberto no v3.5.0;
   falta padronizar o display em si para casar com `entry`/`spinbutton`.

3. **Containers vazando tema claro** — não há regra para `box`/`frame`/`grid`/
   `viewport`/`scrolledwindow`/`stack` genéricos dentro de
   `.hefesto-dualsense4unix-window`; herdam o claro do sistema.

## Decisão / Entrega

1. **Botões com fundo sólido escuro** (não `transparent`): trocar para um fundo
   Drácula sólido (sugestão: `#383a4a` ou `#44475a`) mantendo a borda roxa
   `#bd93f9`. Garante contraste **independente do container/tema do sistema**.
   Ajustar `:hover` / `:active` / `:disabled` coerentes (continuar com a pista de
   borda pink no hover de `UI-THEME-BORDERS-PURPLE-01`).
2. **`GtkToggleButton` (política de rumble)**: cobrir explicitamente, com estado
   **`:checked`** visualmente distinto (fundo accent roxo) para mostrar a política
   ativa — hoje não dá pra saber qual está selecionada.
3. **Footer `.btn-*`**: aplicar fundo escuro base + manter a `border-left` colorida
   por responsabilidade + gradiente por cima (sobre o fundo escuro, não sobre
   transparente). Resultado legível e ainda diferenciado por cor.
4. **Cobrir containers internos** dentro de `.hefesto-dualsense4unix-window`
   (`box`, `frame`, `grid`, `viewport`, `scrolledwindow`, `notebook stack`) com
   fundo escuro/transparente apropriado, **sem** quebrar `.hefesto-dualsense4unix-card`
   (`#21222c`) nem as áreas de log.
5. **Combobox display**: padronizar borda/altura/seta/contraste do display fechado
   para casar com `entry`; revisar o popup garantindo hover/seleção legíveis.
6. **Camada defensiva** em `src/hefesto_dualsense4unix/app/theme.py`: setar
   `Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)`
   antes de aplicar o CSS — força a variante escura do tema do sistema quando
   existir (não substitui o CSS, complementa).
7. **Testes** em `tests/unit/test_theme*.py`: o CSS carrega sem `GLib.Error`;
   regex confirma que `button` tem `background-color` sólido (não `transparent`),
   que há regra `:checked` para toggle, e que o combobox display é coberto.

## Critérios de aceite

- [ ] Em COSMIC real, **todas as abas**: botões com texto legível, sem
      branco-sobre-branco (footer, toggles de rumble, botões de tabela/ação).
- [ ] A política de rumble **ativa** é visualmente distinguível (estado `:checked`).
- [ ] Dropdowns (display fechado **e** popup) legíveis e consistentes com o Drácula.
- [ ] `theme.css` carrega sem `GLib.Error` (sem `@media`; sem sintaxe inválida).
- [ ] Gates: `ruff check`, `mypy --strict`, `pytest tests/unit -q`,
      `python3 scripts/validar-acentuacao.py --all`, `scripts/check_anonymity.sh`.
- [ ] Proof-of-work: screenshots **antes/depois** das abas Daemon, Rumble, Teclado
      e Perfis (mostrando footer + toggles + dropdown).

## Arquivos tocados (previsão)

- `src/hefesto_dualsense4unix/gui/theme.css` (principal).
- `src/hefesto_dualsense4unix/app/theme.py` (prefer-dark defensivo).
- `src/hefesto_dualsense4unix/gui/main.glade` (só se precisar `style_class` nos
  toggles de rumble para diferenciar `:checked`).
- `tests/unit/test_theme_css.py` (ou o nome existente — localizar).

## Notas para o executor

- **GTK3 CSS**: `@media` **quebra o load inteiro** do arquivo (já documentado em
  `theme.css:296-305`). NÃO introduzir. Sem variáveis CSS custom também.
- O provider é por-screen **deste processo** — não vaza para outros apps. Pode
  cobrir `box`/`frame` à vontade dentro de `.hefesto-dualsense4unix-window`.
- **Simular o COSMIC (tema claro)** para validar localmente sem depender do
  hardware: rodar a GUI forçando um tema GTK claro, p.ex.
  `GTK_THEME=Adwaita HEFESTO_DUALSENSE4UNIX_FAKE=1 .venv/bin/hefesto-dualsense4unix-gui`
  — os botões devem permanecer legíveis. Em COSMIC a GUI já roda sob XWayland
  (`GDK_BACKEND=x11` setado em `app/main.py`).
- Captura de tela: a sessão é COSMIC/Wayland — use `cosmic-screenshot`, `grim` ou
  `import` (ImageMagick, via XWayland) conforme disponível.
- **Não** editar `CHANGELOG.md` nem `docs/process/SPRINT_PLAN_COSMIC.md` — a
  consolidação é centralizada (orquestrador). Atualize apenas o `Status:` no topo
  **deste** arquivo de sprint ao concluir.

## Proof-of-work runtime

```bash
GTK_THEME=Adwaita HEFESTO_DUALSENSE4UNIX_FAKE=1 .venv/bin/hefesto-dualsense4unix-gui &
sleep 3
# capturar a janela em Daemon/Rumble/Teclado/Perfis → /tmp/contrast_*.png
kill %1
.venv/bin/pytest tests/unit -q -k theme
.venv/bin/ruff check src/ && .venv/bin/mypy --strict src/hefesto_dualsense4unix
python3 scripts/validar-acentuacao.py --all
```

## Fora de escopo

- Redesenho de layout das abas.
- Tema claro opcional / toggle de tema em runtime.
- Applet nativo COSMIC (sprint `FEAT-COSMIC-APPLET-RUST-01`).
- Bug de input ao conectar (sprint `BUG-DAEMON-CONNECT-GHOST-INPUT-01`).
