# BUG-GUI-COMBOBOX-POPUP-SELECTED-COSMIC-01 — Item selecionado do dropdown ilegível no COSMIC

**Tipo:** fix (GUI/CSS).
**Wave:** V3.8.1 — correções pós-release v3.8.0.
**Estimativa:** XS — regras CSS para o estado selecionado do `menuitem`.
**Dependências:** nenhuma.
**Status:** DONE (CSS). Falta validação visual na máquina (rodada final).

---

## Contexto

A mantenedora relatou que "as listas abrem bugadas aqui e em qualquer lista suspensa do app". No
screenshot do dropdown "Modo" (aba Gatilhos) aberto, a lista renderiza com fundo escuro correto na
maioria dos itens, mas o item **atualmente selecionado** (o valor corrente, ex.: "Desligado") aparece
com fundo cinza-claro destoante e borda — herdando o realce do tema claro do sistema.

## Diagnóstico (causa-raiz)

O popup do `GtkComboBoxText` é um `menu` toplevel (já tratado em BUG-GUI-COMBOBOX-MENU-POPUP-WHITE-01).
O CSS em `gui/theme.css` estilizava o fundo do menu e os estados `:hover`/`:focus` do `menuitem`, mas
**não** os estados de seleção (`:selected`/`:active`/`:checked`) que o GTK aplica ao item ativo quando
o menu abre. Esse item herdava o realce do tema do sistema (claro no COSMIC).

## Decisão / Entrega

Estender o bloco de realce do `menu menuitem` para cobrir `:selected`, `:active` e `:checked` (e seus
`label`) com o mesmo fundo Dracula `#44475a` e texto `#f8f8f2`, em paridade com `:hover`/`:focus`.
Fix aditivo — não altera regras existentes.

## Critérios de aceite

- [x] Acentuação + anonimato OK.
- [ ] Smoke visual na máquina: abrir o dropdown "Modo" (e outros) no COSMIC — item selecionado
  legível (fundo Dracula, não claro).

## Arquivos tocados

- `src/hefesto_dualsense4unix/gui/theme.css` — estados `:selected`/`:active`/`:checked` do
  `menu menuitem`.

## Notas para o executor

Se o item ativo ainda aparecer claro após a validação, inspecionar o nó/estado exato via
`GTK_DEBUG=interactive` (GTK Inspector) e cobrir o seletor faltante (ex.: `cellview` interno, ou a
variante `combobox window treeview`). A altura/posição da lista longa (menu cobrindo a UI) é
comportamento padrão do `GtkComboBoxText` — fora de escopo deste fix.

## Fora de escopo

- Trocar `GtkComboBoxText` por `Gtk.DropDown`/popover (mudaria o GLADE — grande).
- Posicionamento/altura do popup longo.
