# CONFIG-01 — a aba existe e está vazia

> **Portão da leva.** Enquanto a décima primeira aba não abrir vazia sem quebrar
> as dez existentes, nenhuma outra sprint começa.

**Liberada.** [D-A1 e D-A2 respondidas em 21/08/2026](DECISOES-ABERTAS.md) — a aba nasce com as cinco seções.

## O que entrega

Uma aba "Configurações" no fim da tira, com as seções vazias, a fita de alvo
esmaecida e nenhum comportamento. Nada persiste, nada lê o sistema.

Parece pouco. Não é: é aqui que se descobre se onze abas cabem na tira e se a
página nova estoura o orçamento de largura da janela — e essas duas descobertas
custam caro se vierem depois do conteúdo pronto.

## Onde mexer

| Arquivo | O quê |
|---|---|
| `src/hefesto_dualsense4unix/gui/main.glade` | Página nova no `GtkNotebook id="main_notebook"` (abre em `:218`), depois da última `<child type="tab">`. A página copia o molde da Início (`:234-247`): um `GtkScrolledWindow` próprio em volta de um `GtkBox` vazio com `spacing=12` e `margin=12` — e o `id` no box interno **não é opcional** |
| **A CRIAR** — src/hefesto_dualsense4unix/app/actions/config_actions.py | `ConfigActionsMixin` com `install_config_tab()`. Molde verificado: `home_actions.py` |
| `src/hefesto_dualsense4unix/app/app.py` | TRÊS edições: importar o mixin (bloco de imports, `:29-42`), acrescentá-lo às bases de `class HefestoApp` (`:155-167`) e chamar `install_config_tab()` nos **dois** blocos de `install_*` — o do `show()` e o do `run()` com `start_hidden` |

> **Confira as linhas antes de editar.** Os relatórios de reconhecimento
> divergiram em ±1 nas linhas dos `<child type="tab">` (243/244, 657/658, …).
> Ancore por conteúdo, nunca por número.

## Restrições duras

1. **Largura é o recurso escasso, não a altura.** A janela nasce com 1180px e a
   rolagem horizontal é `NEVER` — o mínimo da página mais larga vira o mínimo da
   janela. A aba mais larga hoje é Lightbar, com 1138px. **Teto para a aba nova:
   1180px de largura mínima**, que é a largura com que a janela abre; o teto de
   altura por aba é 657px.
2. **Nada de `homogeneous` em caixa com rótulo longo.** Já custou caro: uma
   fileira de quatro botões do Rumble respondeu por 1004 dos 1066px de largura
   mínima da janela.
3. **`GtkComboBox` é proibido.** O cosmic-comp rouba o foco no clique e fecha o
   popup (cosmic-epoch#2497 / pop#3660). Use `app/widgets/segmented_selector.py`
   — com `wrap=True` ele monta grade de **3 colunas fixas**, nunca `FlowBox`
   (que mediu 606px de altura empilhada).
4. **Saída cedo tolerante.** `widget = self._get(id); if widget is None: return`,
   mais `contextlib.suppress(Exception)` na fiação. Uma aba que não existe no XML
   não pode derrubar a janela.
5. **Todo rótulo explicativo:** `set_xalign(0.0)` + `set_line_wrap(True)` +
   `set_max_width_chars(84..100)` + `dim-label`.
6. **Cor:** só os 20 tokens de `theme.css:21-54`, escritos como `@token` — nunca
   hex solto. Rosa é só marca e aba ativa. Aviso de rádio congestionado é
   **amarelo** (alerta reversível), não vermelho.
7. **Texto:** `translatable="yes"` no Glade, `_("...")` no Python. Rótulo pela
   consequência, não pela tecnologia — a lista viva de jargão banido é a
   `JARGAO_BANIDO` de `scripts/validar-palavra-de-tela.py:85`, e o portão
   também recusa palavra como "daemon", "systemd", "uinput", "JSON",
   "polling" e "throttle".

## Prova de trabalho

```bash
# 1. os portões de texto e estilo
python3 scripts/validar-palavra-de-tela.py
python3 scripts/validar-acentuacao.py
pytest tests/unit/test_paleta_unica.py tests/unit/test_contraste_css.py \
       tests/unit/test_layout_orcamento_altura.py -q

# 2. as onze abas, com a janela cheia
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/config01 --mesa-cheia
```

**Aceite:**

- As onze abas fotografam sem erro, e as dez antigas mudam **só no retângulo do
  rótulo novo**. O "idênticas" que estava escrito aqui não era alcançável: a
  tira de abas aparece em TODAS as fotos, então um rótulo a mais muda todos os
  onze arquivos por construção. Medido em 21/08/2026, comparando pixel a pixel
  contra uma captura do commit anterior: a diferença cabe em `x 994..1106`,
  `y 19..32` — exatamente onde "Configurações" é desenhado — e mais nada se
  move em nenhuma das dez.
- A tira de abas não ganha rolagem horizontal em 1180px de largura.
- A largura mínima da janela não sobe: `Gtk.Window.get_preferred_width()` antes e
  depois dá o mesmo número.
- A aba abre com `XDG_CURRENT_DESKTOP` vazia, em COSMIC e em GNOME.

## Armadilha conhecida

`retratar_abas.py` morre com `Failed to load ... image-missing.svg` quando o
terminal é um snap — ele exporta o cache de loaders do próprio confinamento. A
variável de ambiente acima resolve. Não é defeito do script; é o mesmo ambiente
emprestado que o commit `911d099` tratou para o ícone da bandeja.
