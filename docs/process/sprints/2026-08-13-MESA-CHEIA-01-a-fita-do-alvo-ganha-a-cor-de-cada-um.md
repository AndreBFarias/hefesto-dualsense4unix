# MESA-CHEIA-01 — a fita do alvo ganha a cor de cada um

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a **D-1** dela (que cor é "a cor dele"), como toda sprint
  colorida desta leva
- **Anda colada na
  [MESA-CHEIA-10](2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md)**
  — ver a caixa da seção 1.1
- **É a menor entrega da leva**, e a única que aparece nas dez abas de uma vez
- **Custo mínimo:** 3 h (o censo de 13/08 estimou 90 min só para o swatch)

---

## 1. A falta, medida

A fita do cabeçalho — *"Ajustes vão para: [Todos] [Sony 1 · USB]"* — é montada
em `app/actions/status_actions.py:1495-1506`. Os chips são
`GtkRadioButton` em modo toggle dentro de um box com a classe `linked`
(`:1565-1576`), e cada um carrega **só texto**: `_short_target_label` transforma
`"Controle 1 — USB"` em `"Sony 1 · USB"` (`:1542-1554`).

**Nenhum pixel dessa fita sabe de que cor está o controle.**

E a informação está a um campo de distância:

| o que existe | onde | grau |
|---|---|---|
| `lightbar_rgb`, `lightbar_on`, `lightbar_source` por controle no `state_full` | `daemon/ipc_handlers.py:2521-2536` | **LIDO NO CÓDIGO** |
| a janela já recebe esse bloco a 2 Hz e já o filtra por `connected` | `app/actions/status_actions.py:2379-2391` (`_connected_controllers`) | **LIDO NO CÓDIGO** |
| a regra que decide cor E rótulo a partir dele | `app/widgets/controller_card.py:866-891` (`rotulo_lightbar`) | **LIDO NO CÓDIGO** |
| o desenho do quadradinho de 14x14 com a cor CRUA | `app/widgets/controller_card.py`, **por símbolo**: a montagem é o bloco do `Gtk.DrawingArea` com `set_size_request(14, 14)` que vira `self._swatch` (hoje em `:2116-2121`), e o desenho é `_on_draw_swatch` (hoje em `:4486`). **As linhas deste arquivo estão se movendo hoje** — procure pelo nome | **LIDO NO CÓDIGO** |

O card da aba Status **já faz exatamente o que ela pediu** — só que para um
controle por vez, e só naquela aba. A foto de hoje mostra: `■ Controle 1 — USB`,
com o quadradinho rosa `#ff79c6` ao lado
([`docs/usage/assets/readme_status.png`](../../usage/assets/readme_status.png)).

**A falta em uma frase:** a linguagem de cor por jogador existe, tem nome nesta
casa (**swatch**), tem função pura e tem regra de contraste — e vive presa numa
aba de dez.

---

## 1.1 O que o censo de 13/08 acrescentou, e ele muda o que "menor entrega" quer dizer

> **A fita que esta sprint vai pintar é FALSA em seis das dez abas.**

`_set_target_strip_visible` (`app/actions/status_actions.py:1673`) tem
**exatamente três chamadores** — `:2094`, `:2177` e `:2505` — e os três decidem
por **contagem de controles** ou por **daemon offline**. O
`_on_notebook_switch_page` (`app/app.py:957`), que é quem sabe qual aba está à
frente, **não a menciona**. Não existe um único `if` de aba no caminho.

A fita vale em quatro abas (Status, Gatilhos, Lightbar e — em parte — Rumble) e
**mente em seis** (Início, No jogo, Perfis, Sistema, Emulação, Navegação). A
medição completa está na
[MESA-CHEIA-10](2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md).

**O que isso muda aqui:** pintar uma promessa falsa a torna **mais
convincente**, não mais verdadeira. Esta sprint continua sendo a menor entrega
que vale a pena — e passa a valer a pena **junto** com a 10, que custa outros 60
minutos e mexe no mesmo widget. As duas continuam separadas porque esta é só
desenho e aquela espera a **D-2** dela.

**O que NÃO muda:** o mérito da sprint. A 10 pode entrar depois sem retrabalho —
o swatch fica onde está; o que muda é **quando** a fita aparece.

---

## 2. O que muda na tela

O chip de cada controle ganha o **mesmo swatch do card**, à esquerda do texto.
Nada mais muda: mesma fita, mesma posição, mesmos botões, mesmo gesto.

```
   HOJE (um controle na mesa)
   ┌──────────────────────────────────────────────────────┐
   │  Hefesto            Ajustes vão para: [Todos][Sony 1 · USB] │
   └──────────────────────────────────────────────────────┘

   DEPOIS (um controle na mesa)
   ┌──────────────────────────────────────────────────────┐
   │  Hefesto            Ajustes vão para: [Todos][■ Sony 1 · USB] │
   └──────────────────────────────────────────────────────┘
                                                   └── a cor VIVA da barra dele

   DEPOIS (a mesa cheia — quatro no co-op)
   ┌──────────────────────────────────────────────────────────────────┐
   │  Hefesto   Ajustes vão para: [Todos][■ Sony 1][■ Sony 2][■ Sony 3][■ Sony 4] │
   └──────────────────────────────────────────────────────────────────┘
                                          azul     vermelho  verde     rosa
```

E o caso que a foto tem de mostrar junto, porque é o que impede a tela de
mentir:

```
   UM CONTROLE SEM COR CONHECIDA (lightbar_source == "desconhecida")
   [□ Sony 3 · BT]      <- só o contorno neutro, como o card já faz
```

**O que a foto vai provar:** que o swatch aparece, que a cor bate com a do card
da aba Status para o mesmo controle, e que o chip sem cor conhecida fica com
contorno em vez de preto.

**O que a foto NÃO prova:** que a cor é a que ela vê na barra. Isso é a bancada
dela.

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_01_o_chip_tem_a_cor_dele.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

A entrega expõe **uma função pura** no módulo do card, irmã de `accent_do_card`:

    cor_do_chip(entry, state_global) -> RGB | None

`None` = "sem cor conhecida, desenhe só o contorno". Ela devolve a **cor crua**
(a mesma do swatch, decisão D8: contraste só nos traços), delegando a decisão a
`rotulo_lightbar` — que já existe e já foi revisada.

### Mordida 1 — a paleta no lugar da barra (é a mordida principal)

**Arrancar:** trocar o corpo por `player_slot_color(entry["player_slot"])`.

**Por que reprova:** o dublê tem o controle 2 com `player_slot = 2` e
`lightbar_rgb = (255, 0, 255)` — porque a usuária pintou a barra dele de
magenta. A paleta diria vermelho `(255, 0, 0)`
(`core/led_control.py:148`); a barra diz magenta. O teste exige magenta.

Esta é a mordida que importa porque é a diferença entre o que ela pediu
(*"na cor do lightbar deles"*) e o atalho que parece igual com a mesa de fábrica.

### Mordida 2 — o preto que finge ser apagado

**Arrancar:** devolver `entry["lightbar_rgb"]` direto, sem passar por
`rotulo_lightbar`.

**Por que reprova:** o dublê tem um controle com `lightbar_source =
"desconhecida"` e `lightbar_rgb = None`, e outro com `lightbar_source =
"sysfs"` e `(0, 0, 0)`. Sem a delegação, o primeiro explode ou vira preto — e
preto na tela lê como "apagada", que é a afirmação que a casa proíbe fazer sem
saber (`app/widgets/controller_card.py:876-878`). O teste exige `None` no
primeiro caso e distingue os dois.

### Mordida 3 — a foto

Estender `scripts/gui-captura/retratar_abas.py` para o dublê de **quatro**
controles com quatro cores diferentes, e assertar na foto de qualquer aba que a
fita tem quatro chips. **Arrancar** o swatch da montagem do chip: a asserção de
que existem quatro `DrawingArea` na fita reprova.

### O que este teste NÃO prova

Que a cor chegou ao olho dela. Um `OffscreenWindow` não passa pelo compositor
([COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md)).

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **Cor crua ou cor com contraste garantido?** O card usa crua no swatch e ajustada nos traços (D8). O chip fica pequeno; cor crua muito escura pode sumir contra o cabeçalho | delegar a `rotulo_lightbar` e reusar `ensure_min_contrast` — os dois já existem e já têm teste |
| **Sem cor conhecida: contorno vazio, ou o chip fica como hoje (sem swatch)?** | desenhar o contorno neutro, igual ao card, se ela não disser o contrário |
| **No Modo Nativo o chip mostra a última cor conhecida?** O card mostra e avisa | seguir o card |
| **O chip "Todos" ganha alguma marca?** Hoje é só texto | deixar sem marca, e ela decide se quer as quatro cores em miniatura ali |
| — | montar o `DrawingArea`, ligar no tique lento existente, não criar `GLib.timeout_add` novo |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** a função pura (dublês de 1, 2 e 4 controles, incluindo o caso
sem cor); a foto offscreen de qualquer aba com quatro chips coloridos; que
nenhum timer novo nasceu.

**Só a bancada dela:** que o chip do controle 2 tem a cor que a **barra do
controle 2** está mostrando naquele instante — e que continua batendo depois de
trocar de perfil, que é quando a cor muda por baixo.

**Ela pode ver metade disto hoje**, com o único controle ligado: o chip
`Sony 1 · USB` ganha um swatch, e ela confere contra a barra do controle na mão.
É por isso que esta é a primeira sprint.
