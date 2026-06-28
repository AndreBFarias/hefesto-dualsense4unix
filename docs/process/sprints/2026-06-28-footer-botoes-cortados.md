# BUG-FOOTER-BOTOES-CORTADOS — botões do rodapé cortados

Data: 2026-06-28. Branch: `feat/dsx-definitive-fix-usb-hdmi`. Status: **A FAZER**.

## Sintoma

No rodapé global da GUI, os botões de ação (**Aplicar · Salvar Perfil · Importar ·
Restaurar Default**) ficam **cortados** — o mais à direita ("Restaurar Default") é
clipado na borda da janela em larguras menores (visto em screenshot ao vivo).

## Causa provável

`main.glade` ~linha 2270: `footer_box` (GtkBox horizontal) =
- `status_bar` (GtkStatusbar) com `hexpand=True`, `expand=True`, `fill=True` →
  ocupa o espaço flexível à esquerda e **empurra** os botões pra direita;
- `footer_buttons_box` (GtkBox horizontal, 4 GtkButton, `expand=False`) à direita.

Não há **largura mínima de janela** que garanta o espaço dos 4 botões, nem **wrap**.
Quando a janela é mais estreita que `status_bar(min) + footer_buttons(natural) +
margens`, o conteúdo transborda e o último botão é clipado na `margin-end`.

## Opções de correção (escolher uma; preferir a mais robusta)

1. **Largura mínima da janela** suficiente p/ o footer caber (`set_size_request`/
   `default-width` na janela), garantindo que os 4 botões sempre apareçam. Simples,
   mas impõe um mínimo à janela.
2. **Wrap dos botões** quando estreito: trocar `footer_buttons_box` por um
   `GtkFlowBox` (como fizemos nos modos de gatilho) → os botões quebram linha em vez
   de cortar. Robusto a qualquer largura.
3. **Rótulos compactos / ícones** nos botões (ex.: ícone + tooltip) p/ reduzir a
   largura natural do bloco.
4. **Statusbar cede primeiro**: garantir que `footer_buttons_box` nunca encolha
   abaixo do natural e que a statusbar (hexpand) absorva o aperto; e/ou
   `status_bar` com `width-chars`/ellipsize pra não exigir largura.

Recomendação: (1) largura mínima + (2) wrap como rede de segurança — assim nunca
corta, em qualquer tamanho de janela ou tela (a TV 1080p da mantenedora inclusive).

## Aceitação

- Os 4 botões do rodapé 100% visíveis na largura padrão E ao estreitar a janela.
- Sem regressão no `FROZEN_WIDGET_IDS` (freeze durante "Aplicar") nem nos handlers
  (`on_apply_draft`/`on_save_profile`/`on_import`/`on_restore_default`).
- Gate verde (ruff/mypy/pytest/acentuação/anonimato).

## Notas

- Mesmo espírito do fix do popover do applet (que ganhou `scrollable`/`max_height`):
  conteúdo que pode transbordar precisa de wrap/scroll/min-size explícito.
- Verificar também se a janela tem um tamanho default razoável p/ 1080p.
