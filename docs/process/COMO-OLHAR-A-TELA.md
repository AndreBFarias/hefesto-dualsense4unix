# Como olhar a tela deste projeto

**Leia isto antes de tentar fotografar, medir ou entender a interface.**

Pedido dela, literal, em 01/08/2026:

> *"se tiver outro conhecimento desatualizado no repositório, ou que você usou
> e não funcionou e você descobriu a forma certa, isso deve ser materializado
> como conhecimento perpétuo pra evitar perdermos tempo reaprendendo sempre sem
> necessidade."*

Este arquivo é isso. Cada linha aqui custou tempo de alguém.

---

## A regra, em uma linha

```bash
scripts/gui-captura/retratar_abas.py
```

Uma execução. Nenhum clique, nenhuma janela aberta, nenhuma tela em foco. Sai
um PNG por aba, no tamanho da tela dela maximizada (1920x1080), **com o card do
controle vivo dentro**.

**Sem argumento, ele SOBRESCREVE as imagens da documentação**
(`docs/usage/assets/readme_*.png`) — que são as mesmas do `README.md` e do
`docs/usage/interface.md`. É o comportamento pedido: rodar e a documentação
deixa de mentir.

Com um caminho como argumento, ele só olha:

```bash
scripts/gui-captura/retratar_abas.py /tmp/olhar
```

## O logo e os ícones

Mesma ideia, outro comando:

```bash
scripts/gerar_icones.sh            # gera todos os PNGs a partir do SVG
scripts/gerar_icones.sh --check    # só confere (é o que o teste roda)
```

**A fonte canônica é uma só: `assets/hefesto-logo.svg`.** Mexeu no desenho?
Rode o gerador. Os PNGs do applet COSMIC e do AppImage nascem dele, e
`tests/unit/test_icones_refletem_o_svg.py` reprova se alguém mudar o SVG sem
regerar.

**O que isso curou** (medido em 01/08): havia **dois** caminhos de ícone e o
documentado era o quebrado. O `install.sh` copiava
`assets/appimage/Hefesto-Dualsense4Unix.png`, que **não existia** — o `cp`
falhava em silêncio — e o ícone que aparecia no sistema vinha, por acidente, do
PNG do applet, versionado à mão. E o comentário do instalador afirmava que o
SVG era um placeholder, o que **deixou de ser verdade** em algum momento sem
ninguém atualizar o texto.

## Quando rodar

| momento | por quê |
|---|---|
| **ao começar a trabalhar na interface** | você vê a tela de hoje, não a de seis dias atrás |
| **antes de commitar** mudança visual | a foto do commit é a foto do que ele fez |
| **antes de gerar release** | as imagens do README acompanham a versão |

Em 01/08 as imagens da documentação eram de **26/07** — seis dias e cinco levas
atrás. E `readme_status.png` e `readme_sistema.png` **eram referenciadas e não
existiam**. Rodar o script curou os dois problemas de uma vez.

## Para quem trabalha com o Claude Code

Esta é a parte que ela levantou e que muda o dia a dia:

> *"o melhor, ele funcionaria principalmente pro Claude, pq ficaria muito mais
> fácil pro Claude entender toda a tela, sem todas as vezes o Claude tomar
> sufoco nisso"*

**Está certa, e o sufoco é real e documentado.** Um assistente que precise
entender a interface deve rodar este script e **ler os PNGs** — a ferramenta de
leitura de arquivos enxerga imagens. É mais rápido, mais fiel e infinitamente
menos frágil que as alternativas, que já falharam assim:

- **clicar por coordenada** para focar a janela: aconteceu duas vezes, e nas
  duas o clique caiu noutro aplicativo e o trouxe para a frente. Pior: um
  clique cego já desfez configuração dela sem ninguém notar;
- **percorrer abas por teclado**: o compositor perde eventos em rajada, e a
  sequência inteira sai deslocada em uma aba — a foto chamada "gatilhos"
  mostrando "status". Aconteceu duas vezes antes de existir laço de
  verificação;
- **pedir para ela tirar o print**: funciona, mas custa o tempo dela para
  responder o que uma foto automática responde.

---

## Os três scripts desta pasta, e qual usar

| script | o que faz | quando |
|---|---|---|
| **`retratar_abas.py`** | monta o glade **+ injeta o card do controle**, offscreen | **rotina, sempre** |
| `retrato_offscreen.py` | monta só o glade cru | medir vão/altura, quando o card não importa |
| `capturar_verificado.sh` | fotografa a tela **de verdade**, percorrendo por teclado | prova final, com a janela aberta e em foco |

### Por que o `retrato_offscreen.py` não basta

Ele renderiza o `.glade` **cru**: combos vazios, listas vazias e — o mais grave
— **a aba Status sem o card do controle**, que é montado em código, não no
glade. É justamente a aba mais densa da janela.

Já houve leva fotografada por ele em que o objeto que a leva mudava **não
aparecia na foto**. Ele continua útil para medir geometria de página (é o que
imprime `recebe / natural / vão`), mas não serve para entender a tela.

### Por que o `capturar_verificado.sh` não é rotina

Precisa da janela **aberta, maximizada e em foco**. E o COSMIC recusou
maximizar por atalho, por duplo clique e por F11 nesta máquina. Ele é a prova
final quando o assunto é *"ficou bonito?"* — e para isso não há substituto.

---

## O que a foto offscreen NÃO prova

Seja honesto sobre isto ao usá-la:

- **não passa pelo compositor** — não há sombra, canto arredondado nem o tema de
  janela do COSMIC;
- **não prova que a janela abre** — prova o que tem dentro dela;
- **não substitui o olho dela.** A regra da casa
  ([PROVA-DE-TELA-01](sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md))
  continua valendo: interface só fecha com ela olhando.

Para *"o que tem nesta aba, e onde?"*, a foto é fiel. É para isso que serve.

---

## Armadilhas de GTK que este projeto já pagou

Estas não são sobre foto — são sobre **medir** a interface, e cada uma custou
horas.

### Sob Xvfb não há gerenciador de janelas

Uma `Gtk.Window` de verdade **nunca é mapeada**, e o filho fica **1x1 para
sempre**, por mais que o laço de eventos rode. O `get_surface()` que destrava
uma `OffscreenWindow` não existe ali.

**Consequência:** todo teste de layout deve usar `Gtk.OffscreenWindow`, ou dar
o tamanho à janela por conta própria. Isso reprovou o CI de uma tag inteira.

### Widget sem alocação mede 1x1 — e o teste passa com qualquer desenho

Medir antes de o laço assentar dá 1x1, e uma asserção sobre 1x1 passa com
qualquer coisa. **Drene o laço mais de uma vez** antes de medir.

### `set_size_request` é MÍNIMO, nunca máximo

No GTK3 não existe "largura máxima" por pedido. Um `width-request` sozinho não
segura nada — ele precisa de `halign=start` para virar teto de fato. E com
`halign=center` ele **trava** o widget no número exato.

### `max-width-chars` sozinho não encolhe label nenhum

Ele limita a largura **natural** (o que o widget *pede*); o pai continua livre
para alocar mais, e um label esticado quebra na largura que **recebeu**. Precisa
de `halign=start` junto. Medido em 01/08: sem isso, um parágrafo de 1869px ficou
intacto.

### Uma célula de `GtkGrid` nunca é mais larga que suas colunas

Pedir largura inteira de dentro de uma grade faz **todas** as colunas
expandirem junto. Quem precisa da largura toda sai da grade, para uma caixa
própria.

### `GtkProgressBar` desenha o próprio texto CENTRADO

Numa barra larga, o número fica a centenas de pixels de cada borda. Se a barra
precisa ser larga, o texto sai dela e vira um rótulo ao lado.

### `column_homogeneous` dá metades IGUAIS

Se as duas metades reais do desenho não forem iguais, as divisórias não batem.
Para amarrar larguras entre linhas diferentes, o instrumento é `Gtk.SizeGroup`.

### O quadrado vermelho ao lado dos interruptores

Todo `GtkSwitch` do GTK3 tem dois nós `image` internos que pedem ícones que
**nenhum tema desta máquina resolve** — e o GTK pinta o "imagem faltando" do
tema ativo. `color: transparent`, `-gtk-icon-source: none` e `opacity: 0`
**não** funcionam (o fallback é ícone colorido, não simbólico). O que cura:
`-gtk-icon-transform: scale(0)`.

---

## Armadilhas de medição fora do GTK

### Medir contra a biblioteca errada produz alarme convincente e falso

Em 01/08 mediu-se o gamepad virtual contra a `libSDL2` **do Ubuntu** e
concluiu-se que ele não entregava quase nada ao jogo. A **SDL3 que a Steam
distribui** o enumera por completo. Nenhum jogo da Steam carrega a do sistema.

**Regra:** todo instrumento tem de declarar **qual biblioteca** está usando —
caminho absoluto e versão — no cabeçalho da saída.

### Struct incompleta em `ctypes` corrompe o resultado SEM erro

Faltavam três campos numa `SDL_hid_device_info`; o ponteiro de lista deslocou e
a enumeração saiu errada **em silêncio**, com aparência legítima. Confira campo
a campo contra o header da versão certa.

### O instrumento pode estar brigando com o produto

`hefesto-dualsense4unix test trigger --raw` abre um **segundo** controlador e
disputa o hidraw com o daemon, que sobrescreve em ≤ 0,5 s — **e imprime
"trigger aplicado" mesmo assim**. Testes de gatilho vão pela GUI/IPC, ou com o
daemon parado.

### `paplay --device=inexistente` sai ZERO e toca no padrão

Nunca aceite código de saída como prova de que o som saiu no dispositivo certo.

---

## Ferramentas de sistema, e o que não fazer com elas

- **`ydotool` exige `ydotoold` vivo** e só faz `mousemove` **relativo**. Clique
  por coordenada absoluta não existe — e clique cego já desfez configuração
  dela;
- **`wtype` cria e destrói um teclado virtual a cada chamada**; em rajada o
  compositor perde eventos;
- **o helper global de captura de tela dela** (fora deste repositório, em
  `/usr/local/bin`) fotografa a tela inteira e imprime o caminho do PNG. Serve
  para ver o que está na frente dela agora — não para percorrer abas.
