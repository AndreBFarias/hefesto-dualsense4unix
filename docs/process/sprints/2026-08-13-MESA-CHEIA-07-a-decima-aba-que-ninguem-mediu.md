# MESA-CHEIA-07 — a décima aba, e a cor que a cópia deixou para trás

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Índice da leva:** [as ondas da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Nasceu do censo das abas de 13/08**, e é a primeira coisa da leva: o censo
  descobriu uma aba que ninguém tinha olhado
- **Duas entregas, em duas ondas:** a **E1** é medição (onda 1, ninguém precisa
  estar presente); a **E2** é tela (onda 2, precisa do olho dela)

---

## 1. O defeito, medido — e ele começa por uma contagem errada

**São DEZ abas, não nove.** O `main_notebook`
(`src/hefesto_dualsense4unix/gui/main.glade:212`) põe dez páginas, e a terceira é
a **"No jogo"** — `tab_no_jogo_box`, `gui/main.glade:678`, com o rótulo em
`:685`. Ela é montada em código por `install_no_jogo_tab`
(`app/actions/status_actions.py:541`) e repintada por `_sync_paineis_no_jogo`
(`:766`).

Dez agentes mediram a janela em 13/08. **Nenhum mediu esta.** Não foi descuido
deles: a lista que eu entreguei tinha nove nomes. É lacuna declarada, não achado.

### E o que se enxerga de fora já é o achado que barateia a leva inteira

A "No jogo" **já é** um painel por controle, montado pelas mesmas chaves da aba
Status:

| a peça | onde | grau |
|---|---|---|
| um painel por controle, com `zip(..., strict=True)` sobre `_status_card_keys_for` | `app/actions/status_actions.py:766` e `:1095` | **LIDO NO CÓDIGO** |
| o **mesmo título** da Status — `titulo_do_painel` devolve `titulo_do_card(entry)` | `app/widgets/painel_no_jogo.py:468`, com o import em `:84` | **LIDO NO CÓDIGO** |
| o módulo declara que **chama** a regra do card em vez de reimplementá-la | `app/widgets/painel_no_jogo.py:1-46` | **LIDO NO CÓDIGO** |
| **zero cor**: `grep -c 'lightbar\|accent\|swatch\|player_slot'` no arquivo de 667 linhas devolve **0** | `app/widgets/painel_no_jogo.py` | **MEDIDO** (contagem rodada em 13/08) |

```
   A aba Status  →  título + swatch colorido + accent + o MAC dentro do widget
   A aba No jogo →  título                                        (e mais nada)
                            ↑
                    a casa copiou o molde uma vez
                    e deixou a cor para trás
```

**O defeito em uma frase:** a casa já provou que copiar a Status funciona — e o
que se perdeu na cópia foi exatamente a peça que ela pediu.

---

## 2. As duas entregas

### E1 — medir a aba (onda 1)

Planejar a leva sem ela é planejar contra um mapa incompleto. As mesmas nove
perguntas que as outras abas responderam:

1. qual é a **natureza** da aba (mostra-estado, edita-por-controle, global)?
2. ela **honra o alvo** de edição (`_edit_target_uniq`,
   `app/actions/status_actions.py:427`)? Deve honrar?
3. o que acontece **com quatro controles**?
4. o que ela **afirma na tela** que o código não faz?
5. onde a **cor por jogador** caberia?
6. o que se prova **sem aparelho**?

**Custo: 60 min.** Não precisa de aparelho nem da janela aberta — a aba tem 667
linhas de widget mais o sincronizador em `status_actions.py`, e a foto offscreen
já existe no caminho da casa
([`scripts/gui-captura/retratar_abas.py`](../../../scripts/gui-captura/retratar_abas.py)).

### E2 — terminar a cópia: a aba ganha a cor (onda 2)

O painel de cada controle ganha o **swatch** que o card da Status já tem, na
mesma posição relativa ao título — porque o título já é o mesmo.

```
   HOJE (quatro controles no co-op)
   ┌────────────────────────┐ ┌────────────────────────┐
   │ Controle 1 — USB       │ │ Controle 2 — BT        │
   │ · Jogador 1            │ │ · Jogador 2            │
   ├────────────────────────┤ ├────────────────────────┤
   │ gatilhos: ativos       │ │ gatilhos: ativos       │
   │ vibração: do jogo      │ │ vibração: do jogo      │
   └────────────────────────┘ └────────────────────────┘
     quatro painéis iguais; para saber qual é o dela,
     ela tem de ler o número e traduzir

   DEPOIS
   ┌────────────────────────┐ ┌────────────────────────┐
   │ ■ Controle 1 — USB     │ │ ■ Controle 2 — BT      │
   │   · Jogador 1          │ │   · Jogador 2          │
   ├────────────────────────┤ ├────────────────────────┤
   │ gatilhos: ativos       │ │ gatilhos: ativos       │
   │ vibração: do jogo      │ │ vibração: do jogo      │
   └────────────────────────┘ └────────────────────────┘
     azul                       vermelho
```

**Custo: 45 min** (estimativa minha — a E1 pode mudá-la, e é para isso que ela
vem antes).

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_07_o_painel_tem_a_cor_dele.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — a cor reimplementada em vez de reusada

**Arrancar:** escrever uma função de cor própria dentro de `painel_no_jogo.py`
em vez de chamar a do card.

**Por que reprova:** a asserção é de **identidade**, não de aparência: para o
mesmo `entry`, a cor do painel tem de ser **byte a byte** a mesma do card. Um
dublê com `lightbar_source = "sysfs"` e `lightbar_rgb = (128, 0, 255)` passa
pelas duas funções e o teste compara os dois resultados. Duas implementações
divergem no primeiro caso de borda — e o cabeçalho do próprio módulo
(`app/widgets/painel_no_jogo.py:1-46`) promete o contrário: *"Este módulo
**chama** aquela função; não reimplementa nem uma linha dela."*

Esta é a mordida principal porque é a regra que a cópia **já cumpriu para o
título** e que a cor tem de cumprir também.

### Mordida 2 — o `strict=True` arrancado

**Arrancar:** trocar `zip(keys, conectados, strict=True)` por `zip(...)` simples
em `_sync_paineis_no_jogo` (`app/actions/status_actions.py:766`).

**Por que reprova:** o dublê tem três chaves e quatro controles conectados. Com
`strict=True` o desencontro **estoura**; sem ele, o quarto controle some em
silêncio e os três primeiros ficam com a cor de quem calhar. O teste exige a
exceção.

### Mordida 3 — o timer novo

**Arrancar:** pintar a cor num `GLib.timeout_add` próprio em vez de pegar carona
no tique lento de 2 Hz.

**Por que reprova:** o gate está escrito no docstring de `_sync_paineis_no_jogo`
(`app/actions/status_actions.py:766-779`) com o número: *"um poller cego já
custou 104% de um núcleo nesta casa"*. O teste conta os `GLib.timeout_add`
registrados na montagem da aba e exige que o número não suba.

### O que este teste NÃO prova

Que a cor é a que ela vê na barra. Isso é a bancada dela — e, nesta aba, com o
jogo aberto.

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **A cor é a viva ou a da paleta?** É a **D-1** do índice, e ela trava esta sprint como trava todas as coloridas | usar a que ela escolher, por uma função só |
| **O painel do controle sem cor conhecida fica com contorno, ou sem marca?** O card já responde contorno neutro | seguir o card, salvo palavra dela |
| **A E1 vira documento próprio, ou nota nesta sprint?** As nove abas irmãs viraram relatório | escrever onde ela preferir; o padrão da casa é relatório por aba |
| — | a E1 inteira, o swatch por reuso, e a carona no tique lento |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** a E1 inteira (é leitura de fonte); as três mordidas; e a foto
offscreen da aba com dublê de quatro controles.

**Só a bancada dela:** que os quatro painéis coloridos **cabem** com o jogo
aberto — esta aba existe para ser olhada durante a partida, e a densidade dela
com quatro nunca foi vista por ninguém.

**Ela vê a metade que importa hoje**, com o único controle ligado: o painel dele
ganha a cor, e ela confere contra a barra na mão. O que espera a mesa cheia é
saber se quatro painéis coloridos ainda se leem de relance.
