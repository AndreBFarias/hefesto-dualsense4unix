# MESA-CHEIA-02 — a marca de quem escolheu, na aba Gatilhos

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a [01](2026-08-13-MESA-CHEIA-01-a-fita-do-alvo-ganha-a-cor-de-cada-um.md)
  (a linguagem de cor), a
  [09](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md) (a aba **mente na
  volta** — ver a caixa da seção 1.1) **e de uma decisão de desenho dela**
  (seção 4)
- **Custo mínimo:** 6 h
- **É a aba em que ela estava olhando quando pediu.**

---

## 1. O defeito, medido

A aba Gatilhos mostra **exatamente um estado**: o do alvo escolhido no
cabeçalho.

`_refresh_triggers_from_draft` (`app/actions/triggers_actions.py:151-188`) faz
uma chamada só:

    triggers_draft = draft.effective_triggers_for(
        getattr(self, "_edit_target_uniq", None)
    )

`app/actions/triggers_actions.py:164-166`. E `_edit_target_uniq` é **um escalar**
— um MAC ou `None`, declarado em `app/actions/status_actions.py:427`. Trocar de
alvo no cabeçalho repinta a aba inteira
(`_refresh_target_tabs`, `app/actions/status_actions.py:2036-2058`), e o estado
anterior **some da tela**.

**Com quatro controles na mesa, três dos quatro gatilhos são invisíveis o tempo
todo.** É literalmente o que ela descreveu: não dá para ver quem escolheu o quê.

### E o dado dos outros três já está calculado

`draft.effective_triggers_for(uniq)` (`app/draft_config.py:871-889`) aceita
**qualquer** MAC e resolve o override por peça sobre a seção global. Ela é
chamada com um argumento — o alvo — e **ninguém nunca a chamou em laço**.

A lista de quem está na mesa também já existe, na mesma janela:
`_connected_controllers` (`app/actions/status_actions.py:2379-2391`).

**O defeito em uma frase:** a aba tem a função que responde "qual o gatilho do
jogador N" e a lista de quem são os N — e pergunta uma vez só.

---

## 1.1 O que o censo de 13/08 acrescentou: a aba MIRA CERTO e MENTE NA VOLTA

Duas coisas que esta sprint não sabia, e as duas mudam a ordem de execução.

**A boa:** a aba **acerta o alvo nos dois eixos** — `:164-166` na leitura do
rascunho e `:287` no pedido que sai. Ela é uma das três que honram
`_edit_target_uniq`. O trabalho aqui é **mostrar**, não consertar mira.

**As duas más, e elas vêm ANTES da marca:**

1. **A aba diz *"aplicado"* em três casos em que nenhum byte saiu** — alvo
   desconectado, alvo sem MAC 12-hex, e Modo Nativo com output mutado. A frase é
   montada em `app/actions/triggers_actions.py:599` e o daemon **não pode**
   confirmar: `trigger.set` devolve `{"status": "ok"}` seco
   (`daemon/ipc_handlers.py:958`) enquanto `led.set`, no mesmo arquivo, já
   devolve `aplicado_em` (`:1061`). É a
   [MESA-CHEIA-09](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md).
2. **O botão "Desligar" RE-ARMA, 300 ms depois, a trava que acabou de soltar** —
   a cura R-19 está desfeita, e o teste que a protege não morde. É a
   [MESA-CHEIA-08](2026-08-13-MESA-CHEIA-08-o-desligar-que-re-arma-a-trava.md).

**Por que isto reordena a leva:** uma marca colorida em cima de uma aba que
afirma "aplicado" sem ter aplicado torna a mentira **mais bonita**. A marca diz
*"o jogador 2 está em Rígido"* com a autoridade de uma cor, e o jogador 2 pode
estar desconectado com o override apenas guardado. **Consertar a volta custa 2 h
15 e vem primeiro.**

### E há um degrau mais barato antes desta sprint

O censo mediu que a aba Gatilhos é hoje **byte-idêntica** com um ou com quatro
controles — nada nela diz para quem vai o ajuste. Antes das quatro marcas cabe
uma entrega de 125 min: **um rótulo com o controle corrente e o swatch ao lado
de cada moldura L2/R2**, mais o toast nomeando o controle. O dado já existe
(`_edit_target_label`, `app/actions/status_actions.py:428`, e
`_edit_target_slot`, `:448` — os dois mantidos em sincronia com o daemon pela
mesma rotina que move o alvo). Não substitui esta sprint — é o meio-degrau que
ela pode **ver** com o único controle ligado hoje.

---

## 2. O que muda na tela

A grade de 19 modos continua **uma só**. Cada botão passa a carregar as marcas
de quem escolheu aquele modo — cor da lightbar **mais o número**, nunca cor
sozinha.

```
   HOJE — a aba Gatilhos com quatro controles na mesa
   ┌──────────────────────────────────────────────────────────────┐
   │ L2 (gatilho esquerdo)                                        │
   │                                                              │
   │        ┌───────────┬───────────┬───────────┐                 │
   │ Modo:  │[Desligado]│  Rígido   │Rígido simp│                 │
   │        │  Pulso    │Pulso (A)  │Pulso (B)  │                 │
   │        │Resistência│Arco flecha│  Galope   │   ... 19 modos   │
   │        └───────────┴───────────┴───────────┘                 │
   └──────────────────────────────────────────────────────────────┘
   Quem está escolhendo? O do cabeçalho. Os outros três: invisíveis.


   DEPOIS — a mesma grade, com as marcas
   ┌──────────────────────────────────────────────────────────────┐
   │ L2 (gatilho esquerdo)              na mesa: ■1 ■2 ■3 ■4      │
   │                                                              │
   │        ┌───────────┬───────────┬───────────┐                 │
   │ Modo:  │ Desligado │[Rígido]   │Rígido simp│                 │
   │        │      ■2 ■4│        ■1 │           │                 │
   │        ├───────────┼───────────┼───────────┤                 │
   │        │  Pulso    │Pulso (A)  │Pulso (B)  │                 │
   │        ├───────────┼───────────┼───────────┤                 │
   │        │Resistência│Arco flecha│  Galope   │                 │
   │        │           │           │        ■3 │                 │
   │        └───────────┴───────────┴───────────┘                 │
   └──────────────────────────────────────────────────────────────┘
     [Rígido] com moldura = o alvo do cabeçalho (quem ela edita agora)
     ■N no canto = quem MAIS está naquele modo, na cor da barra dele
```

Duas coisas a ler nesse desenho:

- **a moldura continua sendo o alvo de edição.** A marca diz *onde cada um
  está*; a moldura diz *quem ela está mexendo*. São dois papéis e duas formas —
  sem isso a tela ganha quatro seleções e nenhum foco;
- **a marca carrega o número.** `■1` e não `■`. Cor sozinha exclui quem não
  distingue cor, e a própria paleta desta casa já se preocupou com isso ao
  escolher rosa em vez de magenta *"para não confundir com o azul em brilho
  baixo"* (`core/led_control.py:143-146`).

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_02_quatro_gatilhos_na_tela.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

A entrega expõe **uma função pura**, sem GTK:

    marcas_do_lado(draft, conectados, lado) -> dict[str, list[Marca]]

`conectados` é a lista de `state_full.controllers`; a chave do dicionário é o
`mode` (o mesmo id do `SegmentedSelector`); `Marca` é `(uniq, numero, rgb)`.

### Mordida 1 — ler o global em vez do efetivo

**Arrancar:** trocar `draft.effective_triggers_for(uniq)` por `draft.triggers`
dentro do laço.

**Por que reprova:** o dublê tem o perfil com `triggers.left.mode = "Off"` no
global e um override do controle 2 para `"Rigid"`
(`draft.with_controller_triggers`, `app/draft_config.py:922-931`). Com o global,
os quatro caem em `"Off"` e a marca `■2` some de `"Rigid"`. O teste exige a
marca `■2` em `"Rigid"` e as outras três em `"Off"`.

É a mordida principal: sem ela, a tela pareceria certa com a mesa em que
ninguém tem override — que é a mesa dela hoje.

### Mordida 2 — a marca do controle que caiu

**Arrancar:** iterar `draft.controllers` (o mapa do perfil) em vez de
`conectados`.

**Por que reprova:** o dublê tem um perfil com override para quatro MACs e
**dois** controles conectados. Iterando o perfil, a tela mostra `■3` e `■4` de
controles que não estão na mesa. O teste exige duas marcas, não quatro.

### Mordida 3 — a cor de fábrica no lugar da cor viva

Mesma mordida da 01, aqui aplicada à marca: trocar `cor_do_chip(entry, ...)`
por `player_slot_color(slot)` e ver reprovar no dublê em que o controle 2 está
com a barra em magenta.

### Mordida 4 — a foto

`scripts/gui-captura/retratar_abas.py` com o dublê de quatro controles: a foto
`readme_gatilhos.png` tem de mostrar marcas em pelo menos dois modos
diferentes. Arrancar a chamada que passa as marcas ao selector: a foto volta a
ser a de hoje e a asserção reprova.

### O que este teste NÃO prova

Que a aba fica legível. Dezenove botões com marcas em cima é densidade, e
densidade é olho dela.

---

## 4. O que é decisão dela, e o que é execução minha

**A decisão que BLOQUEIA esta sprint** está na seção 3.1 do
[índice](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md): quatro
painéis lado a lado, ou um painel com quatro marcas? O desenho acima é a
**opção B**, e ele está aqui porque ela decide vendo — não porque eu escolhi.

O preço da opção A, nesta aba especificamente, está medido: a grade de 19 modos
pede ~480 px (`app/widgets/segmented_selector.py:31-36`), a aba já tem **dois**
painéis (L2 e R2), e quatro jogadores fariam **oito** painéis — 3840 px contra
os 1920 px da tela dela (`scripts/gui-captura/retratar_abas.py:104`) e os 760 px
de piso da janela (`gui/main.glade:114`).

| decisão dela | execução minha |
|---|---|
| **A ou B** (ou a terceira: marcas só de leitura, sem gesto) | qualquer uma das três, mesmo motor puro por baixo |
| **A marca fica DENTRO do botão ou numa faixa acima da grade?** Dentro é preciso; acima é legível | desenhar onde ela disser |
| **O alvo do cabeçalho ganha moldura ou continua só "apertado"?** Hoje o botão ativo já é o apertado do `linked` | manter o apertado e acrescentar a moldura só se ela pedir |
| **Quando os quatro estão no mesmo modo, mostra `■1 ■2 ■3 ■4` ou "todos"?** | mostrar os quatro; "todos" é resumo e resumo esconde |
| — | a API por botão: `set_marcadores({id: [Marca]})` no `SegmentedSelector`, espelho exato do `set_tooltips` que já existe ali (`app/widgets/segmented_selector.py:97-110`) — não é mecanismo novo, é o mesmo formato `{id: valor}` |
| — | pintar no tique LENTO (2 Hz) e só com a aba à vista, como a aba "No jogo" já faz (`app/actions/status_actions.py:766-779`); nenhum `GLib.timeout_add` novo |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** tudo o que está na seção 3. A função é pura, os dublês são de
quatro controles, e a foto é offscreen.

**Só a bancada dela:**

- que a aba com quatro marcas **continua legível** — é a pergunta da
  PROVA-DE-TELA-01, e a resposta é o olho dela;
- que a marca acompanha a troca de perfil sem piscar valor velho;
- e a pergunta que só aparece com quatro controles de verdade: **ela consegue
  achar o dela na grade em menos de um segundo?** Se não, a marca virou enfeite.

**O que ela NÃO consegue ver hoje:** com um controle só, a aba mostra uma marca
apenas. A prova completa espera a mesa cheia — que já esteve montada em
11/08 (quatro DualSense, dois no cabo e dois no rádio,
[CANETA-NA-MÃO-01](2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md)).
