# MESA-CHEIA-03 — a mesma marca na aba Lightbar, e o lugar em que ela não serve

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a [02](2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md)
  (o formato da marca), a
  [09](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md) (os dois toasts que
  mentem — ver a caixa da seção 1.1) **e da decisão D-11 dela**
- **Custo mínimo:** 5 h. **O censo de 13/08 mediu 390 min (6 h 30)** para a
  faixa dos quatro completa, e a estimativa dele é a mais cara das duas — vale a
  do censo até alguém medir de novo

---

## 1. O defeito, medido — e a descoberta que muda o desenho

A aba Lightbar tem **duas metades**, e elas não aceitam a mesma marca. Isto não
é opinião: é o que a foto de hoje mostra
([`docs/usage/assets/readme_lightbar.png`](../../usage/assets/readme_lightbar.png)).

### Metade esquerda — "Lightbar (barra de LED)"

Não é uma grade de opções. É um seletor de cor com **uma** prévia
(`lightbar_preview`, `gui/main.glade:1095`, repintada em
`app/actions/lightbar_actions.py:439-442`), um deslizador de luminosidade e
quatro botões de ação.

O alvo vem do mesmo escalar: `_edit_uniq()`
(`app/actions/lightbar_actions.py:230-237`) devolve `_edit_target_uniq`. Uma
prévia, um alvo, uma cor.

**E aqui a marca colorida não serve.** Marcar "o jogador 2 escolheu vermelho"
com um quadradinho vermelho, em cima de um seletor de vermelho, não se lê — o
sinal e o fundo são a mesma coisa. **Nesta metade a marca tem de ser o
NÚMERO**, com a cor como preenchimento da própria prévia.

### Metade direita — "Desenho das 5 luzes"

Esta **é** uma grade de opções discretas: seis botões
(`player_leds_preset_p1` a `player_leds_preset_p4`, `_all` e `_none`,
`gui/main.glade:1334-1382`). Aqui a marca da sprint 02 cabe sem mudança
nenhuma de conceito.

### E o terceiro estado, que é o que mais engana

Com **"Cores automáticas por controle" LIGADO** — o padrão do esquema
(`profiles/schema.py:295`) — **ninguém escolheu cor nenhuma**: cada controle
exibe a cor da paleta pelo seu slot. A aba já sabe disso e já mente menos por
causa de um achado ao vivo de 17/07: `_auto_preview_slot`
(`app/actions/lightbar_actions.py:239-260`) existe justamente porque *"a prévia
mostrava a manual (roxo), MENTINDO"*.

**Se a marca ignorar esse estado, as quatro marcas ficam todas em cima da cor
manual global — e nenhuma delas é verdade.**

---

## 1.1 O que o censo de 13/08 acrescentou: a aba mais disciplinada mente em duas bordas

O censo confirmou o que esta sprint já dizia — a Lightbar honra o alvo em seis
pontos e é a mais disciplinada da casa — **e achou duas mentiras de borda que
pioram com quatro na mesa**:

1. **Alvo desconectado:** o toast diz *"Cor enviada ao controle ({pct}% de
   brilho)"* (`app/actions/lightbar_actions.py:54`) e nenhum byte saiu. A causa
   é a mesma dos Gatilhos — o `apply_output_for` sai calado quando não há handle
   (`core/backend_pydualsense.py:3417-3423`) — e o alvo é **mantido de
   propósito** quando o controle some (R-16), então ela vai continuar clicando.
2. **Co-op ligado:** o toast diz *"Desenho das luzes aplicado — …"*
   (`app/actions/lightbar_actions.py:986`) enquanto o rótulo três centímetros
   abaixo diz *"Aceso agora: o desenho do co-op — com o co-op ligado, é ele que
   manda nas 5 luzes."* (`:163-167`). **A mesma tela se contradiz.**

**Por que isto vem antes das quatro prévias:** uma prévia por jogador é uma
afirmação forte sobre o que cada barra está mostrando. Construí-la sobre uma aba
que já afirma "enviada" sem ter enviado é empilhar. O conserto está na
[MESA-CHEIA-09](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md), custa 60
min do lado desta aba, e **a GUI já tem os dois dados**: quem está na mesa
(`_uniqs_conectados`, `app/actions/lightbar_actions.py:206-228`) e se o co-op
manda (o texto de `:163-167` já é escolhido por ele).

**A decisão 3.2.4 do índice virou D-11** na renumeração de 13/08 — mesma
pergunta, mesmo texto, numeração alinhada com as dez decisões do censo.

---

## 2. O que muda na tela

```
   METADE ESQUERDA — HOJE                     METADE ESQUERDA — DEPOIS
   ┌──────────────────────────┐               ┌──────────────────────────┐
   │ Cores automáticas [ ]    │               │ Cores automáticas [ ]    │
   │                          │               │                          │
   │  ┌──┐  Prévia            │               │  Prévia de cada um:      │
   │  │  │  ┌───────────────┐ │               │  ┌──┐┌──┐┌──┐┌──┐        │
   │  └──┘  │               │ │               │  │1 ││2 ││3 ││4 │        │
   │        └───────────────┘ │               │  └──┘└──┘└──┘└──┘        │
   │ [Aplicar no controle]    │               │   ^^ o 1 com moldura =   │
   │ [Apagar]                 │               │      o alvo do cabeçalho │
   └──────────────────────────┘               │ [Aplicar no controle]    │
     uma prévia, do alvo                      │ [Apagar]                 │
                                              └──────────────────────────┘
                                                quatro prévias, uma por
                                                jogador, com o NÚMERO dentro


   METADE DIREITA — DEPOIS (a marca da sprint 02, sem mudança de conceito)
   ┌───────────────────────────────────────────────────────────┐
   │ Presets rápidos:                                          │
   │  ┌────────────┬────────────┬────────────┬────────────┐    │
   │  │Desenho P1  │Desenho P2  │Desenho P3  │Desenho P4  │    │
   │  │         ■1 │         ■2 │            │         ■4 │    │
   │  ├────────────┼────────────┤            └────────────┘    │
   │  │Todas acesas│Todas apag. │                              │
   │  │         ■3 │            │                              │
   │  └────────────┴────────────┘                              │
   └───────────────────────────────────────────────────────────┘


   O ESTADO QUE NÃO PODE MENTIR — automático LIGADO
   ┌──────────────────────────────────────────────────┐
   │ Cores automáticas [X]                            │
   │  ┌──┐┌──┐┌──┐┌──┐    azul, vermelho, verde, rosa │
   │  │1 ││2 ││3 ││4 │    <- a paleta, não a escolha  │
   │  └──┘└──┘└──┘└──┘                                │
   │  Ninguém escolheu cor: estas são as automáticas. │
   └──────────────────────────────────────────────────┘
```

A frase da última caixa não é enfeite. É a diferença entre a tela dizendo
*"cada um escolheu a sua"* e a verdade, que é *"ninguém escolheu; o produto
escolheu por todos"*.

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_03_a_previa_de_cada_um.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

A função pura:

    previas_da_mesa(draft, conectados) -> list[Previa]

`Previa` é `(uniq, numero, rgb, origem)`, com `origem` em
`{"escolha", "automatica", "desconhecida"}` — a terceira palavra é o que
permite a tela dizer o que sabe.

### Mordida 1 — a prévia que ignora o automático

**Arrancar:** devolver sempre `draft.effective_leds_for(uniq).lightbar_rgb`,
sem olhar `draft.leds.auto_player_colors`.

**Por que reprova:** o dublê tem `auto_player_colors = True` e a cor manual
global em roxo. A função arrancada devolve **quatro roxos**; o esperado é
`origem = "automatica"` e as cores da paleta (azul, vermelho, verde, rosa —
`core/led_control.py:147-150`). É **exatamente** o defeito ao vivo de 17/07 que
o `_auto_preview_slot` já curou para uma prévia, agora multiplicado por quatro.

### Mordida 2 — o slot tirado do rótulo em vez do estado

**Arrancar:** derivar o número do jogador com a regex do rótulo
(`re.search(r"Controle\s+(\d+)", label)`, `app/actions/lightbar_actions.py:258-260`)
em vez do `player_slot` de cada entrada de `conectados`.

**Por que reprova:** o dublê tem quatro controles e um só rótulo de alvo. A
regex responde por **um**; as outras três prévias ficam sem número ou repetem
o do alvo. É o mesmo espaço-de-numeração-duplo que a R-24 removeu do daemon —
a tela não pode reintroduzi-lo.

### Mordida 3 — a marca da metade direita

Mesma da sprint 02, aplicada a `player_leds`: arrancar
`effective_leds_for(uniq)` e ler o global; a marca do controle com desenho
próprio some do botão certo.

### Mordida 4 — a foto

`readme_lightbar.png` com o dublê de quatro controles: quatro prévias
numeradas na metade esquerda e ao menos duas marcas na direita.

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **D-11 — a metade esquerda vira quatro prévias, ou continua uma prévia com quatro marcas ao lado?** Aqui a marca **É** a cor: um quadradinho vermelho em cima de um seletor de vermelho não se lê. É o que trava esta sprint | montar a que ela escolher |
| **A prévia mostra o número dentro do quadrado, ou embaixo?** Dentro precisa de contraste sobre a própria cor | usar `ensure_min_contrast` contra a cor da prévia (`utils/color_contrast.py:120-145`), que já sabe fazer isso |
| **Com automático ligado, a tela avisa?** A proposta é a frase *"Ninguém escolheu cor: estas são as automáticas."* — que é léxico novo e por isso é dela | escrever a frase que ela aprovar; sem frase, a tela mente |
| **Clicar na prévia de um jogador troca o alvo?** É a sprint 04 | — |
| — | a função pura, os quatro `DrawingArea`, e a repintura no tique lento com a aba à vista |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** as quatro mordidas. A `previas_da_mesa` é pura e os três
estados (escolha, automática, desconhecida) são dublês.

**Só a bancada dela:**

- que as quatro prévias batem com as **quatro barras acesas** na frente dela —
  e esta é a única prova que interessa, porque a aba inteira existe para isso;
- que ligar e desligar "Cores automáticas por controle" muda as quatro prévias
  na hora, e não só a do alvo;
- e o caso que já mordeu esta casa antes: **trocar de perfil** com quatro
  controles e ver se as prévias seguem, ou se congelam no valor velho.

**Com um controle só ela vê um terço disto:** a prévia dele, com número, e o
estado "automática". As outras três esperam a mesa cheia.
