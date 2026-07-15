# Sprint SPRINT-ESTETICA-01 — a interface parece um sistema só

Pedido da mantenedora (2026-07-15): *"além da estética e qualidade"* / *"precisamos vender
melhor o programa"*.

O problema não é feiura: é **falta de sistema**. Cada aba foi construída numa sprint
diferente e inventou o próprio padrão — dois estilos de título, margens divergentes, cores
fora da paleta escritas à mão em Python, CSS morto de widgets que não existem mais. Quem
usa não sabe nomear isso; sente como "meio desalinhado", e é o que separa um projeto de um
produto.

Fazer **depois** do UHID/HARMONIA/LEIGO: polir tela que aqueles sprints vão apagar é
trabalho jogado fora.

## Prioridade 1 — Um sistema, não dez dialetos

- `EST-01` — **Tokens de verdade.** Hoje: 9 hexadecimais ad-hoc espalhados em Python, o
  log com `#2a2a2a` fora da paleta Drácula, e o tema competindo com cor escrita na mão.
  Extrair tokens (fundo, superfície, texto, texto-fraco, acento, sucesso, atenção, erro) e
  **proibir hex solto** — cor só via classe CSS.
  **Aceite**: `grep` por `#[0-9a-f]{6}` em `app/` não acha nada; um teste trava isso.

- `EST-02` — **Um padrão de título de seção e uma margem.** Existem **dois** padrões
  concorrentes (`GtkFrame` com label vs título em markup) e margens de aba divergentes.
  **Aceite**: as 8 abas (pós-`HARM-02`) usam o mesmo cabeçalho e as mesmas margens.

- `EST-03` — **Um lugar para montar cartões.** Cada aba remonta o próprio card/linha na
  mão. Extrair helpers (`section()`, `card()`, `row()`) para `actions/base.py`.
  **Aceite**: nenhuma aba constrói layout de seção por conta própria.

- `EST-04` — **CSS morto fora.** ~50 linhas de `GtkComboBox` (widget extinto desde o fix
  do cosmic-comp), e a regra de hover que sobrou **viola a própria política anti-jitter**
  do projeto. Mais: `.hefesto-dualsense4unix-card` está definida **duas vezes** no mesmo
  arquivo, com paddings conflitantes.
  **Aceite**: `theme.css` sem regra para widget inexistente; nenhuma classe duplicada.

## Prioridade 2 — O visual precisa dizer a verdade

- `EST-05` — **Botão destrutivo parece botão comum.** "Desligar Hefesto" tem a classe
  `destructive-action`, mas o tema **não a estiliza** — o botão que para tudo é visualmente
  igual a "Importar".
  **Aceite**: ação destrutiva é reconhecível **antes** do clique.

- `EST-06` — **Preview do perfil sem estilo.** A classe do glade
  (`hefesto-profile-preview`) **não bate** com o seletor do CSS — o JSON aparece cru.
  **Aceite**: classe e seletor casam (e um teste que falhe quando divergirem de novo).

- `EST-07` — **Estado de foco.** `:focus` não é estilizado nos botões: quem navega por
  teclado não sabe onde está.
  **Aceite**: foco visível em todo controle interativo.

- `EST-08` — **Contraste abaixo de AA** no subtítulo do banner e no vermelho de
  desconexão — justamente o texto que avisa que algo quebrou.
  **Aceite**: AA (4.5:1) em texto normal; medido, não achado.

- `EST-09` — **Alto contraste não alcança ~40 textos.** O `FEAT-A11Y-HIGH-CONTRAST-01` não
  atinge os textos coloridos via **Pango markup** (`<span foreground=…>` escrito em Python)
  — o modo existe e não cumpre o que promete.
  **Aceite**: nenhum `foreground=` hardcoded; cor de estado vem de classe.

## Prioridade 3 — Acoplamentos que quebram em silêncio

- `EST-10` — **Código acoplado a TEXTO visível.** `app.py:717` procura a aba pelo rótulo
  ("Daemon") — renomear a aba (que o `LEIGO-03` **vai** fazer, para "Sistema") ou o título
  da janela **quebra** a lógica. Mesma família: o tray e o applet procurando por nome.
  **Aceite**: nada procura widget por texto de UI; teste que renomeia e continua verde.
   **Bloqueia o `LEIGO-03`** — fazer antes.

- `EST-11` — **i18n dividido.** Metade da UI é traduzível (gettext) e a **aba Início e a
  seção Modo dos Perfis são hardcoded** — as duas telas que os outros sprints reescrevem.
  Passar tudo por `_()` **enquanto** se reescreve (custo zero agora, alto depois).
  **Aceite**: nenhuma string visível fora de `_()`; `.po` atualizado; teste que pega
  string nova sem `_()`.
   Compartilhado com `LEIGO-08` — fazer junto, não duas vezes.

## Prioridade 4 — Caber com 4 controles (visual)

Estes são a parte visual do `SPRINT-4P-01`; ficam aqui para não se perderem:

- `EST-12` — **Cards estouram com 4.** `GtkBox` horizontal homogêneo, **sem wrap nem
  scroll**, dentro de um scroller com `hscroll=NEVER`.
  **Aceite**: 4 cards cabem, inclusive em janela estreita/tiling do COSMIC.

- `EST-13` — **Status tem UMA linha fixa** de Conexão/Transporte/Bateria/Perfil no glade —
  com 4 controles ela só reflete um.
  **Aceite**: a aba mostra os 4.

- `EST-14` — **O seletor de alvo vira 5 toggles empilhados** ("Todos", "1 · USB", "2 · BT",
  "3 · BT", "4 · BT") — e com 4 controles iguais os rótulos não distinguem nada.
  **Aceite**: cabe e identifica (ver `EST-15`).

- `EST-15` — **Identidade visual por jogador.** Os cards P1–P4 são só texto; o único
  identificador é `…c311f0`. Casar **cor da lightbar** + **LED de jogador** + chip colorido
  na UI: o Controle 2 é "o azul", e é assim que a pessoa o reconhece na mesa.
  **Aceite**: dá para saber qual card é qual controle **sem ler MAC**.
   Depende do `4P-03`; é a mesma entrega, vista pela UI.

## Método

1. Tokens e helpers primeiro (`EST-01`..`EST-04`) — sem isso cada fix vira mais um dialeto.
2. `EST-10`/`EST-11` **antes** do `SPRINT-LEIGO-01` tocar os textos.
3. O resto pode ir junto com o polimento das abas.

## Validação

Screenshot de cada aba antes/depois (a sessão de 2026-07-15 já deixou o "antes" das 10),
em janela larga **e** estreita, tema claro **e** escuro, com 1 e com 4 controles. Mais:
navegar o app inteiro **só pelo teclado** e enxergar onde está o foco.
