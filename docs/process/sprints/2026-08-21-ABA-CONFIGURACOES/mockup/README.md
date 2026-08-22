# O mockup

`aba-configuracoes.html` — abre com duplo clique, não precisa de servidor nem de rede.

## O que ele é

Um desenho da aba **como ela deve ficar**, no tema real do projeto. Todos os
tokens de cor e a escala tipográfica são cópia literal de
[`src/hefesto_dualsense4unix/gui/theme.css`](../../../../src/hefesto_dualsense4unix/gui/theme.css) —
inclusive a regra que o próprio CSS escreve na linha 28:

```css
@define-color pink #ff79c6;  /* MARCA e aba ativa — só isso */
```

O rosa aparece em exatamente dois lugares no mockup: o sublinhado da aba ativa e
a faixa de microfone no medidor de rádio. Nenhuma cor nova foi inventada.

## O que ele NÃO é

**Não é a aba.** É HTML, não GTK. Serve para decidir hierarquia, agrupamento e
texto antes de alguém escrever um `.glade`. Três coisas não se decidem aqui:

1. **Espaçamento real.** O GTK mede diferente do navegador; a conferência é com
   `scripts/gui-captura/retratar_abas.py` depois de a aba existir.
2. **Se ficou bonito.** `OffscreenWindow` e navegador nenhum passam pelo
   compositor — sem sombra, sem canto arredondado de janela, sem o tema do
   COSMIC por cima. Isso é olho na tela real.
3. **Se os números batem.** Todo valor visível é **cenário de exemplo**, e a
   tarja roxa no topo diz isso. Os endereços, os `831 / 1600` e os VID:PID são
   ilustração — nenhum foi lido de uma máquina.

## Estados

O rodapé mostra os oito estados dos botões (padrão, hover, foco, ativo,
desabilitado, carregando, erro, sucesso) lado a lado, de propósito, para servir
de referência a quem for implementar. **Os três últimos botões do rodapé não
existem na aba real** — são demonstração, e o próprio rodapé diz isso.

O foco visível é `2px solid` no ciano `#8be9fd`, que é o que o `theme.css` já usa
em `entry:focus` e `combobox:focus` (linha 485). Não é escolha nova.

## Conferir contra o produto

```bash
# as dez abas de hoje, para comparar densidade e voz
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/olhar --mesa-cheia
```

A variável é necessária quando o terminal é um snap: ele exporta o cache de
loaders do próprio confinamento, e o `retratar_abas.py` morre com
`Failed to load ... image-missing.svg` antes de desenhar o primeiro pixel. Não é
defeito do script — é o ambiente emprestado, o mesmo problema que o commit
`911d099` tratou para o ícone da bandeja.
