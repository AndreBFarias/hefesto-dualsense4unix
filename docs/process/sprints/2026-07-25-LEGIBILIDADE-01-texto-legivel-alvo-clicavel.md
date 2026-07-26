# LEGIBILIDADE-01 — texto legível, alvo clicável, coisas no lugar certo

- **Status:** ENTREGUE em 25/07/2026 pelo commit `a343ff6`
- **Prioridade:** MÉDIA (alta em impacto de uso diário)
- **Aberta em:** 25/07/2026

## Os relatos

> "olhando pra interface do app tô achando os botões muito pequenos e com as
> fontes minúsculas e em cores que não permitem leitura. Não seria interessante
> aumentarmos em 3 o tamanho delas? E ir realocando melhor o resto?"

> "os analógicos no Status deveriam ficar ao lado do microfone e lightbar e entre
> os botões. Eles estão acima. Temos que encaixar isso também."

## O achado que muda o conserto

**A escala tipográfica do projeto é código morto.**

`gui/theme.css:95-131` declara 14 degraus de tamanho — `.hefesto-titulo-painel`,
`.hefesto-corpo`, `.hefesto-dica`, `.hefesto-micro`, `.hefesto-selo` e outros.
Medindo o que a interface **realmente** usa:

| classe | px | usos reais |
|---|---|---|
| `.hefesto-titulo` | 21 | 1 |
| `.hefesto-rotulo-secao` | 12 | 1 |
| `.hefesto-subtitulo` | 11 | 1 |
| **as outras 11** | 15…9 | **zero** |

Todo o resto da janela — cada rótulo, cada botão, cada legenda de moldura — **não
tem regra de tamanho nenhuma** e herda o padrão do Pango: **13,33 px**, porque
`gtk-font-name` é definido sem número.

Consequência direta: **mexer nos degraus da escala não muda nada na tela dela.**
Foi essa suposição que fez o problema parecer resolvido antes.

### O texto que ela não consegue ler

| px | onde | arquivo:linha |
|---|---|---|
| **9,0** | rótulos do sensor, desenhados em Cairo | `app/widgets/sensor_widgets.py:241` |
| **9,3** | **selo MUDO/ATIVO do microfone** — o menor texto da interface | `app/widgets/controller_card.py:994` |
| **10** | **porcentagem da bateria** | `gui/theme.css:487` |
| **11** | nota do rodapé, log da aba Sistema | `theme.css:922`, `:626` |
| **11,1** | X/Y do analógico | `controller_card.py:116` |

Os quatro primeiros são exatamente **informação de estado do controle** — o que
ela mais olha. E três deles (9,0 · 9,3 · 11,1) não vêm do CSS: são atributos
Pango e Cairo no Python, fora do alcance de qualquer ajuste de tema.

## Contraste: dez pares reprovam WCAG AA

| razão | par | onde |
|---|---|---|
| **3,03:1** | `#6272a4` sobre `#282a36` | rótulo desabilitado, kicker, menu |
| **3,20:1** | `#6272a4` sobre `#242630` | **nota do rodapé e subtítulo do cabeçalho** |
| **3,36:1** | `#6272a4` sobre `#21222c` | botão desabilitado |
| **4,41:1** | `#f8f8f2` sobre `#6272a4` | botão pressionado |
| **4,47:1** | `#8b8fa8` sobre `#282a36` | `.dim-label` dentro de card — **20 usos** |

O piso para texto normal é 4,5:1. O padrão é claro: **`#6272a4` reprova como cor
de texto sobre qualquer fundo do aplicativo.** Ele é uma cor de *borda* sendo
usada como cor de *texto*.

Isso confirma a screenshot: o "Perfil aplicado ao controle." do rodapé, em
`#6272a4` a 11 px, é o pior caso da interface — texto minúsculo **e** com o menor
contraste.

### Por que os testes não pegaram

- **`test_color_contrast.py` não lê o `theme.css`.** Ele testa um auxiliar de
  runtime que corrige cores de lightbar vindas do IPC, com piso `3.0` — a régua
  de *não-texto*. Nenhum par do CSS passa por ele.
- **`test_paleta_unica.py` valida o conjunto, nunca o par.** Ele exige que todo
  hex pertença às 26 cores oficiais. `color: @comment` sobre `background: @chrome`
  é 100% aprovado — as duas cores são da paleta.

**É possível reprovar WCAG usando exclusivamente cores aprovadas pelo teste de
paleta.** É o que acontece em dez lugares. Contraste é propriedade de *par*, e
não existe teste de par no projeto.

## Aumentar +3: medido, e a altura não é o problema

Medição real com `GtkOffscreenWindow` carregando o glade e o CSS de verdade:

| aba | altura hoje | com +3 | largura hoje | com +3 |
|---|---|---|---|---|
| Emulação | 562 | **658** (estoura o teto de 600) | 814 | 1013 |
| Navegação DSX | 505 | **601** | 960 | **1200** |
| Rumble | 404 | 428 | **1066** | **1330** |
| Lightbar | 417 | 452 | 1014 | **1234** |
| **janela inteira** | 729 | **796** | **1068** | **1332** |

**A largura é o problema duro.** `app/app.py:876` define a política de rolagem
como vertical automática e **horizontal `NEVER`** — a barra vertical salva a
altura, mas o mínimo de largura sobe intacto até a janela, sem escape. Com +3 a
janela exigiria 1332 px contra os 1100 de projeto.

E o gargalo não é o tamanho da fonte: são **caixas com distribuição homogênea
contendo um rótulo longo**. A pior delas:

> `gui/main.glade:1144` — a linha de quatro botões do Rumble, homogênea, com
> *"Deixar o jogo controlar a vibração"* no meio. **Essa linha sozinha responde
> por 1004 dos 1066 px de largura mínima da janela inteira.**

Realocando primeiro (R1, R2, R3 abaixo), o +3 passa a caber:

| | janela | Rumble | Nav. DSX |
|---|---|---|---|
| +3 sem realocar | 1332 | 1330 | 1200 |
| **+3 com realocação** | **1128** | **584** | **1021** |

**A realocação que ela pediu não é acabamento — é o que paga o aumento de fonte.**

## Os analógicos fora do lugar

> "os analógicos no Status deveriam ficar ao lado do microfone e lightbar e entre
> os botões. Eles estão acima."

O cartão de controle (`app/widgets/controller_card.py`) hoje empilha os
analógicos acima da faixa de sensores. O agrupamento que ela descreve é o
correto: **microfone, lightbar e analógicos são todos leitura de estado ao vivo**
e pertencem à mesma faixa, entre os botões. Os analógicos estarem acima os separa
dos seus pares e desperdiça largura — a mesma largura que falta para o +3.

Isso entra na fase de realocação, não como item separado.

## A escala global: uma opção só é viável

| opção | veredito |
|---|---|
| variável CSS | **impossível no GTK3** — `@define-color` só declara cor, não há `calc()`, e token desconhecido **derruba a carga do arquivo inteiro** (o projeto já tropeçou nisso duas vezes: `theme.css:105` e `:805`) |
| `gtk-font-name` | move a base herdada — os ~90% da tela. Não alcança as 6 regras em px |
| provider gerado | reescreve as regras em px em memória antes de carregar |

**Recomendação: as duas últimas juntas, em `app/theme.py:46`** — que já é o dono
único do tema e já mexe em `Gtk.Settings`. Uma chave `escala_fonte` em
`gui_preferences.json` (default 0), um ponto de aplicação, sem tocar duzentos
lugares. O mecanismo foi **simulado e provado funcionando** durante a auditoria —
não é proposta no papel.

## Ordem de execução

**Fase 0 — fechar o furo do teste, antes de tudo.**
Teste novo de *pares* de cor: extrair os tokens do `theme.css`, mapear os pares
texto×fundo e exigir 4,5:1 (3,0 para texto grande). Sem isso as correções voltam
na próxima edição. Lembrete de método: o gate de acentuação varre só o que está
no índice do git — **rodar depois do `git add`**.

**Fase 1 — contraste.** Risco zero de layout. Trocar `@comment` por `@text_muted`
onde ele é texto (7 pontos), e `@text_muted` por `@text_soft` dentro de card
(2 pontos). `@comment` continua legítimo como cor de **borda**.

**Fase 2 — área clicável.** Remover o `min-height: 0` de `theme.css:831` — que
hoje deixa o seletor de modo da aba Início, o controle mais importante da
interface, com **24 px** de altura. Piso de 32 px nos botões, 24 px nos
controles deslizantes. E criar a regra de `.hefesto-external-btn`, que
`status_actions.py:525` aplica e **não existe no CSS**.

**Fase 3 — realocação, com a fonte ainda em +0.** Compra o orçamento de largura
antes de a fonte crescer:

- **R1** — tirar a distribuição homogênea da linha do Rumble e renomear o botão
  para **"Devolver ao jogo"**, que é o termo que ela já usa.
- **R2** — tirar a homogênea da aba Navegação DSX.
- **R3** — tirar a homogênea da Lightbar; encurtar *"Voltar todos ao automático"*.
- **R4** — os analógicos descem para a faixa de microfone e lightbar, entre os
  botões *(o pedido dela)*.
- **R5** — a fita de chips do cabeçalho ganha faixa própria; com quatro controles
  é a região mais densa da janela.

**Fase 4 — o mecanismo de escala**, com default 0. Nada muda visualmente; entra
só o canal, com teste do orçamento rodando nos deltas 0 a 3.

**Fase 5 — ligar o +3.** Janela de 1100×760 para 1180×830, e os tetos do teste de
orçamento atualizados **com os números medidos e justificados** — não afrouxados.
Se algo ainda estourar, **+2 é o degrau seguro** — mas só depois da Fase 3, porque
hoje até o +2 estoura a aba Emulação.

**Fase 6 — o texto minúsculo que não vem do CSS.** Os três pontos em Python
(9,0 · 9,3 · 11,1 px) não são alcançados pelo mecanismo da Fase 4 e precisam de
edição própria. Trocar os relativos do Pango por classes da escala fecha o buraco
de vez — **e dá uso às 11 classes órfãs**, que é a decisão que falta: ou elas
passam a ser aplicadas, ou saem do arquivo.

## Como validar

- Nenhum par texto×fundo abaixo de 4,5:1 no teste novo.
- Nenhum alvo clicável abaixo de 32 px.
- Nenhum texto abaixo de 12 px.
- A janela abre sem barra de rolagem em nenhuma aba, a 1180×830.
- Os analógicos aparecem na mesma faixa do microfone e da lightbar.
- E o teste que decide: **ela ler o rodapé sem se aproximar da tela.**
