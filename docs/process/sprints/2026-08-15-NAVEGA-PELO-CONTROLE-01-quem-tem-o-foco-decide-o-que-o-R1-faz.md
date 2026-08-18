# NAVEGA-PELO-CONTROLE-01 — quem tem o foco decide o que o R1 faz

**15/08/2026.** Isto é **proposta**, não entrega. A regra que governa esta fase é
a [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
*interface só fecha com o olho dela*. O que está aqui é o estado de hoje
fotografado, o desenho do que as decisões pedem, o custo em arquivos, o risco —
e **uma** pergunta, no fim, que nasceu depois das respostas dela e que só ela
pode fechar.

**As decisões que esta frente executa** (de
[AS-DECISOES-RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md)):

| decisão | resposta dela |
|---|---|
| **D-19** (fundação) | **duas coisas.** Navegar a janela não passa por uinput; os quatro navegam ao mesmo tempo |
| **D-20** | o R1 tem **dois significados, decididos pelo foco** |
| **D-21** | **círculo volta à tira de abas**; R1 vai para a aba da direita, L1 para a esquerda, em **carrossel** |
| **D-22** | o X é **roubado, só os quatro botões, só do dono da navegação** |
| **D-23** | **manter fechado.** Um mapeamento de navegação para todos, sem tabela por controle |

### Leia junto com a página irmã

Outra frente escreveu, na mesma tarde, a
[NAVEGAR-ESTA-JANELA-01](2026-08-15-NAVEGAR-ESTA-JANELA-01-a-decisao-ja-esta-tomada-e-o-dado-ja-esta-no-fio.md).
**As duas se completam e não se contradizem** — descobri a existência dela ao
rodar o portão de referências, com esta página já escrita, e prefiro dizer isso
a fingir coordenação que não houve.

| pergunta | quem responde |
|---|---|
| **o que a aba mostra**, com o desenho da seção nova e os 487 px que sobram | a **irmã** (§3) |
| **a taxa do fio** (cabo 242-250 Hz, rádio 141-177 Hz) e o censo da onda D-16 a D-22 | a **irmã** (§4, §9) |
| **a máquina de estados inteira** — cinco estados, seis verbos, duas bordas | **esta** (§4) |
| **quem rouba os botões e em que tique** (D-22), e por que a GUI não pode ser quem decide | **esta** (§5.1) |
| **calar o Alt+Tab** com a janela na frente (a outra metade da D-20) | **esta** (§5.4) |
| **o carrossel de verdade**, medido no GTK | **esta** (§4.5) |
| **onde o anel de foco vai morar**, e a colisão com a D-18 | **esta** (§6.2) |

Há **uma divergência de rota**, e ela está nomeada na seção 8.1.

---

## 1. O resumo, para quem só tem cinco linhas

1. **Não existe uma linha** de navegação por controle na janela hoje. Procurei:
   `grep` por `set_current_page`, `grab_focus`, `child_focus`, "dono da
   navegação", "carrossel" em `src/` devolve **um** resultado de produto, e ele
   é a saída da aba "No jogo" quando ela some.
2. **Quase toda a fundação já está pronta e medida** — o predicado da janela
   própria, os botões por controle no `state_full`, o molde de subtração de
   botões no laço, o molde do badge no cabeçalho, o léxico "Sony 3 · BT". A
   lista com arquivo e linha está na seção 3.
3. **A máquina fecha no papel** (seção 4): cinco estados, seis verbos, duas
   bordas. Ela precisa de **uma** peça nova de estado no daemon e **uma** na
   GUI; o resto é subtração de conjunto em três pontos que já existem.
4. **O achado que muda a arquitetura** (seção 5.1): se quem detecta a borda do
   botão for a **GUI**, o **primeiro X de cada novo dono VAZA para o jogo** —
   exatamente o defeito que a D-22 proíbe. A detecção tem de morar no daemon,
   que enxerga a 60 Hz e mascara **no mesmo tique**.
5. **A pergunta que sobrou** (seção 9): a D-22 nomeou *"os quatro botões"* antes
   de a D-21 dar significado de navegação ao **L1 e ao R1**. O conjunto que
   navega ficou maior que o conjunto que é roubado, e isso tem consequência na
   tela dela.

---

## 2. O estado de hoje, fotografado

### 2.1 A tira de abas — o objeto que o R1 vai mover

`docs/usage/assets/readme_status.png`, de hoje às 03:12. Dez abas, nesta ordem:

```
Início · Status · No jogo · Gatilhos · Lightbar · Rumble · Perfis · Sistema · Emulação · Navegação
```

A aba corrente é marcada por **sublinhado rosa**. A tira mede **62 px** de
altura e o teto de cada página é **654 px** — números medidos e escritos em
`gui/theme.css` (bloco `notebook > header > tabs > tab`), com a advertência de
que *engordar a tira sai do teto das páginas*. **Isso é orçamento**: qualquer
marca de navegação na tira tem de caber **sem mudar um pixel de altura**.

### 2.2 A aba Navegação — o que ela mostra hoje

`docs/usage/assets/readme_navegacao_dsx.png`. Duas colunas:

| coluna | o que tem |
|---|---|
| **Emular mouse** | interruptor, velocidade do cursor, velocidade da rolagem e a tabela de mapeamento (Cruz → botão esquerdo, Círculo → Enter, Quadrado → Esc, D-pad → setas, analógicos → cursor e rolagem) |
| **Emular teclado** | interruptor e a lista *"Atalhos de teclado do perfil ativo"* |

**A foto esconde uma coisa, e a culpa é do instrumento, não do produto.** Na
foto a lista de atalhos sai **vazia**; no produto ela mostra os oito padrões de
`core/keyboard_mappings.py`, entre eles **`r1 → Alt + Tab`** e
**`l1 → Alt + Shift + Tab`**. O motivo é que `scripts/gui-captura/retratar_abas.py`
monta as mixins de produção de **cinco** abas (Início, Status, No jogo, Perfis,
Gatilhos) e **não monta a desta**: o `key_bindings_treeview` nasce sem store, e
`_refresh_key_bindings_from_draft` volta sem escrever nada.

> **Consequência prática:** as duas linhas que esta frente vai mudar de
> significado (`r1` e `l1`) **nunca apareceram em foto nenhuma desta casa**. Se
> a prova de tela desta frente for tirada com o instrumento de hoje, ela não
> prova a metade que importa. Isto é dívida do instrumento e está anotada na
> seção 8.

### 2.3 O cabeçalho — onde o selo "Navegando" vai morar

`docs/process/estudos/assets/mesa-cheia/mesa_cheia_cabecalho.png`, o único
retrato desta casa que alcança o `header_bar`:

```
Hefesto — DualSense4Unix                     ● 4 controles: USB + USB + BT + BT
Ajustes vão para: [ Todos ] [ Sony 1 · USB ] [ Sony 2 · BT ] [ Sony 3 · BT ] [ Sony 4 · USB ]
```

O léxico do cabeçalho é **"Sony N · TRANSPORTE"** — então o selo proposto pela
sprint de 14/08, **"Navegando: Sony 3 · BT"**, deriva do que já existe e não
inventa palavra nova. (O card da aba Status usa outro rótulo, *"Controle 1 —
USB"*; o selo é de **cabeçalho**, e segue o léxico do cabeçalho.)

---

## 3. O que JÁ está pronto — e serve inteiro

Esta é a parte barata, e ela é grande. Nada abaixo precisa ser escrito.

| peça | onde | por que serve |
|---|---|---|
| **"a janela em foco é a nossa"** | `profiles/autoswitch.py`, `OWN_GUI_WM_CLASSES` | o predicado do gate do lado do daemon já existe, com quatro nomes provados no journal |
| **os botões de CADA controle** | `daemon/ipc_handlers.py`, `controllers[].inputs.buttons` | é o canal por onde a navegação lê quem apertou o quê — **não precisa de canal novo** |
| **subtrair botões antes de despachar** | `daemon/lifecycle.py`, o bloco `combo_buttons_active` | o molde exato do que a D-20 e a D-22 pedem, com o comentário do defeito que o originou |
| **soltar o que ficou preso na borda** | `daemon/lifecycle.py`, `_flush_emulation_devices` | a cura de 18 s / 33 s de tecla presa, já escrita |
| **o dono do vpad por jogador** | `subsystems/coop.py:1549` e `subsystems/gamepad.py:2039` | são **as duas únicas linhas** que entregam botão ao jogo. A D-22 mexe nelas e em mais nada |
| **badge no cabeçalho** | `app/actions/status_actions.py:1515` (`_edit_badge`) | molde pronto: `Gtk.Label` + `set_no_show_all(True)` + `pack_end`. Já há três badges assim |
| **o léxico** | "tira de abas" (`theme.css`), "Sony N · BT" (cabeçalho), "Editando: …" (badge) | a frente não precisa inventar uma palavra |

### 3.1 E o que NÃO existe: zero linhas

```
grep -rniE "dono da navega|navegando|carrossel|nav_owner" src/    -> 0 no produto
grep -rn  "set_current_page|grab_focus|child_focus"       src/app -> 1 ocorrência
```

A única ocorrência é `status_actions.py:770`, que leva o foco para a aba Status
quando a aba "No jogo" some. **A navegação por controle é greenfield.**

---

## 4. A máquina de estados inteira

*"Se ela não fechar no papel, não fecha na tela."* Aqui está ela.

### 4.1 Os três eixos que decidem tudo

| eixo | valores | quem sabe |
|---|---|---|
| **foco da janela** | `com foco` · `sem foco` | a **GUI**, nativamente (`Gtk.Window.is_active()`) — sem daemon e sem cegueira em Wayland |
| **dono da navegação** | um `uniq` (MAC), ou **nenhum** | o **daemon**, que vê as bordas a 60 Hz |
| **onde está o foco dentro da janela** | `na tira` · `no miolo` | a **GUI** |

### 4.2 Os cinco estados

```
                       ┌──────────────────────────────────────────┐
                       │  S0  JANELA SEM FOCO                     │
                       │  sem dono · nada é roubado               │
                       │  R1 = Alt+Tab (se o teclado estiver on)  │
                       └───────────────┬──────────────────────────┘
              a janela ganha foco      │      a janela perde o foco
                                       ▼      (ou botão PS)
                       ┌──────────────────────────────────────────┐
                       │  S1  COM FOCO, SEM DONO                  │
                       │  nada é roubado ainda · sem selo         │
                       │  R1 já é "aba", de quem apertar          │
                       └───────────────┬──────────────────────────┘
        qualquer verbo de navegação    │
        (o autor vira DONO no MESMO    ▼
         tique em que aperta)
                       ┌──────────────────────────────────────────┐
                       │  S2  COM DONO · FOCO NA TIRA DE ABAS     │
                       │  os quatro do dono ficam com a janela    │
                       │  selo: "Navegando: Sony 3 · BT"          │
                       └────────┬───────────────────▲─────────────┘
                    cruz (X)    │                   │  círculo
                    desce       ▼                   │  volta (D-21)
                       ┌──────────────────────────────────────────┐
                       │  S3  COM DONO · FOCO NO MIOLO DA PÁGINA  │
                       │  d-pad move o anel · cruz aciona         │
                       └──────────────────────────────────────────┘

     S4  DONO TROCA: outro controle aperta um verbo -> ele vira dono no mesmo
         tique; o dono anterior recupera os quatro botões no MESMO tique.
```

### 4.3 A tabela dos verbos, estado a estado

| botão | S0 (sem foco) | S1 (foco, sem dono) | S2 (na tira) | S3 (no miolo) |
|---|---|---|---|---|
| **R1** | Alt+Tab (padrão do perfil) | aba à **direita**, carrossel | idem | idem, **e o foco volta à tira** |
| **L1** | Alt+Shift+Tab | aba à **esquerda**, carrossel | idem | idem, **e o foco volta à tira** |
| **Cruz (X)** | vai ao jogo | vira dono e **desce** para o miolo | **desce** para o miolo | **aciona** o widget com o anel |
| **Círculo** | vai ao jogo | vira dono, sem efeito visível | **nada** (já está na tira) | **volta à tira** (D-21) |
| **Quadrado / Triângulo** | vai ao jogo | vira dono | **roubados, sem função** — ver seção 9 | idem |
| **D-pad** | vai ao jogo | vira dono, anda na tira | anda na **tira** | anda no **anel de foco** da página |
| **PS** | ação de sempre | ação de sempre | **larga a navegação** → S1 | idem |
| **analógicos, L2/R2, L3/R3, Options, Create** | vão ao jogo | vão ao jogo | **vão ao jogo, sempre** | idem |

**A linha dos analógicos é decisão dela e não é detalhe:** é ela que evita o
personagem travar em pé enquanto alguém mexe na janela.

### 4.4 Como se entra e como se sai — as duas bordas

| borda | gatilho | o que acontece no mesmo tique |
|---|---|---|
| **entrar** | um controle aperta um verbo de navegação **com a janela em foco** | ele vira dono; os quatro botões dele **param de ir ao jogo já nesta borda**; o selo acende |
| **sair** | botão **PS**; a janela **perde o foco**; ou o **lease** expira (GUI morta) | o dono some; os quatro voltam ao jogo; o selo apaga |

O **lease** é a rede de segurança: a GUI renova a posse a cada tique dela; se a
janela morrer sem se despedir, o daemon larga o dono em **1 s** e ninguém fica
com botão roubado por uma janela que não existe mais. Na perda de foco normal a
GUI manda **um pulso imediato** — o lease não é o caminho comum, é o fusível.

### 4.5 O carrossel, e a armadilha que eu medi

A D-21 pede carrossel. **`Gtk.Notebook` não tem carrossel** — e a página
"No jogo" **é escondida** quando não há jogo Steam aberto
(`status_actions.py:708`), o que torna o caminho ingênuo perigoso. Medido hoje,
offscreen, num notebook de 5 páginas com a 2 escondida:

| chamada | resultado medido |
|---|---|
| `set_current_page(2)` na página **escondida** | **não faz nada, em silêncio** — fica na 1 |
| `next_page()` a partir da 1 | vai para a **3** (pula a escondida sozinho) |
| `next_page()` na **última** | **fica na última** (não dá a volta) |
| `prev_page()` na **primeira** | **fica na primeira** |

Ou seja: `set_current_page((i + 1) % n)`, que é o que qualquer um escreveria,
**congela o R1** assim que a roda passar pela aba "No jogo" escondida — e
congela **sem erro nenhum**. O caminho certo usa o `next_page()` do próprio GTK
(que já pula escondida) e só trata a volta:

```python
def _proxima_em_carrossel(notebook):
    antes = notebook.get_current_page()
    notebook.next_page()
    if notebook.get_current_page() == antes:      # estava na última visível
        notebook.set_current_page(_primeira_visivel(notebook))
    return notebook.get_current_page()
```

Ensaiado com a **primeira** página também escondida: a volta caiu na página 1, a
primeira **visível**, e não na 0. São 8 linhas, e as duas metades são medidas.

---

## 5. Onde a decisão obriga a arquitetura

### 5.1 O achado: com a GUI decidindo, o primeiro X de cada dono VAZA

Este é o ponto que decide o desenho inteiro, e ele sai da aritmética dos
relógios, não de gosto:

| relógio | valor | fonte |
|---|---|---|
| poll loop do daemon | **60 Hz** (16,7 ms) | `DEFAULT_POLL_HZ` |
| tique vivo da GUI | **10 Hz** (100 ms) — **e só com a aba Status à vista** | `app/constants.py`, `LIVE_POLL_INTERVAL_MS` + o gate `BUG-STATUS-TICK-HIDDEN-TAB-01` |
| ida e volta de `daemon.state_full` | **0,78 ms** de mediana, **11.655 bytes** | medido hoje, 30 chamadas, daemon dela com 4 controles |
| ida e volta de `daemon.status` | **0,20 ms**, **572 bytes** | mesma medição |

Se a GUI é quem detecta a borda do X e depois avisa o daemon para mascarar, o
X **já foi entregue ao vpad** entre 1 e 6 tiques antes — o personagem pula, e
só depois a tela reage. **Isso é literalmente o defeito que a D-22 proíbe**, e
nenhuma folga de rede o conserta.

Com a detecção no daemon, a subtração acontece **no mesmo tique da borda**: o
conjunto `buttons_pressed` que decide o dono é o **mesmo** conjunto que vai ser
passado ao `forward_buttons`, e a subtração fica entre um e outro. O primeiro X
do novo dono **nunca chega ao jogo**.

**Divisão de trabalho, então:**

| quem | o que faz | por quê |
|---|---|---|
| **GUI** | diz **se tem foco** (evento nativo, sem latência, imune a Wayland) e **pinta** | é a única que sabe o foco com exatidão |
| **daemon** | detecta as bordas a 60 Hz, decide o **dono**, aplica a **máscara** | é o único que chega a tempo |

A tela pode ficar 50 ms atrás — ninguém enxerga isso numa troca de aba. A
**máscara** é que não pode.

### 5.2 O canal: um método de IPC que faz as três coisas

```
navegacao.foco  {"ativa": true}
  ->  {"dono": "<uniq>|null",
       "eventos": {"<uniq>": {"r1": 12, "l1": 3, "cross": 7, "circle": 2,
                              "dpad_up": 4, "dpad_down": 4, ...}}}
```

Uma chamada por tique da GUI: **renova o lease**, **declara o foco** e **lê as
intenções**. As intenções são **contadores monotônicos por controle e por
botão**, no idioma que a casa já usa (`store.bump`). A GUI guarda o valor
anterior e aplica a **diferença** — assim um toque duplo em 40 ms vira dois
passos de aba, e nada se perde por a GUI ter piscado. Nível de botão perderia;
contador não.

Tamanho estimado do payload: da classe do `daemon.status` (**572 bytes / 0,20
ms**), não da do `state_full` (**11.655 bytes / 0,78 ms**) — quatro vezes mais
barato, e é por isso que a proposta pede método próprio em vez de pegar carona.

**Custo do tique, com o número na mesa:** a 20 Hz (50 ms), 20 × 0,20 ms =
**4 ms de ida e volta por segundo**, ou **0,4 % de um núcleo**. Pegando carona
no `state_full`: **1,6 %**. Este número é ida-e-volta medida; não medi o custo
de parse na GUI nem o de montar o payload novo, porque ele não existe ainda.

### 5.3 O gate de foco: por que a GUI, e não só o `wm_class`

O daemon **também** sabe reconhecer a janela própria (`OWN_GUI_WM_CLASSES`), e
essa leitura vale como segunda opinião. Mas ela não pode ser a **primeira**, e
o motivo é medido:

- o detector de janela roda a **2 Hz** (`autoswitch.DEFAULT_POLL_INTERVAL_SEC =
  0.5`) — até **500 ms** de atraso para perceber que a janela ganhou o foco. É
  tempo de sobra para um R1 sair como Alt+Tab **para fora da janela que ela
  acabou de focar**;
- medido hoje, ao vivo: o backend ativo nesta máquina é o **Xlib**, e com uma
  janela Wayland nativa em foco ele devolve `wm_class: 'unknown'` — o valor
  cego. A leitura levou 14,3 ms;
- o que salva é que a **nossa** GUI é fixada em XWayland
  (`app/main.py` força `GDK_BACKEND=x11` no COSMIC; medido no processo vivo
  dela, PID 823660: `GDK_BACKEND=x11`). Conferido nas janelas X dela agora:
  `WM_CLASS = "hefesto-dualsense4unix", "Hefesto-Dualsense4Unix"` e
  `"main.py", "Main.py"` — os quatro nomes de `OWN_GUI_WM_CLASSES`, batendo.

Então o `wm_class` **funciona**, mas com meio segundo de atraso e apoiado numa
variável de ambiente. O evento da própria janela é exato e instantâneo. Usar os
dois: a GUI manda, o `wm_class` é o desempate quando não há pulso.

### 5.4 O outro lado do R1: o Alt+Tab tem de calar

Hoje o padrão de perfil é `r1 → KEY_LEFTALT+KEY_TAB`. Se a navegação mover a
aba **e** o teclado emulado disparar o Alt+Tab, o resultado é: a aba muda e a
janela **sai da frente no mesmo gesto**. Esta é a metade da D-20 que fica no
daemon, e ela é **uma subtração**, no mesmo lugar onde o combo de hotkey já
subtrai:

```python
emu_buttons = buttons_pressed
if self._hotkey_manager is not None:
    ...
# NOVO: os verbos de navegação do DONO não vazam para o desktop.
emu_buttons -= navegacao.verbos_do_dono(self)
```

Isso cala **só os botões da navegação**, e **só do dono**. O cursor emulado, as
setas, o Super, o PrintScreen e tudo o mais continuam funcionando com a janela
na frente — que é o que ela pediu quando escolheu *"dois significados"* em vez
de *"aba em todo lugar"*.

**Nota de estado, medida hoje às 17:52 na máquina dela:**
`keyboard_emulation.enabled = false` e `mouse_emulation.enabled = false`. Ou
seja: **hoje o R1 não faz nada** — nem Alt+Tab. A metade "calar o Alt+Tab"
desta frente não muda nada no que ela vê hoje; ela existe para o dia em que o
teclado voltar a ser ligado.

### 5.5 Por que o vpad não fica com botão preso

`forward_buttons` faz **diff contra o estado inteiro** nos dois backends
(`uinput_gamepad.py:545` e `uhid_gamepad.py:1527`). Tirar os quatro do conjunto
de entrada **gera o release** no tique seguinte, sozinho. A dívida de tecla
presa (18 s numa noite, 33 s na outra) é do caminho **uinput de teclado**, que
emite borda — e lá o `_flush_emulation_devices` já existe e é o que a subtração
do 5.4 tem de chamar na primeira borda.

---

## 6. O que muda na tela — o desenho

### 6.1 O selo no cabeçalho

```
Hefesto — DualSense4Unix        Navegando: Sony 3 · BT    ● 4 controles: USB + USB + BT + BT
Ajustes vão para: [ Todos ] [ Sony 1 · USB ] [ Sony 2 · BT ] [ Sony 3 · BT ] [ Sony 4 · USB ]
```

Molde do `_edit_badge`: `Gtk.Label` + `set_no_show_all(True)` + `pack_end`.
Acende quando há dono, apaga quando não há. **Não pode** mostrar o alvo de
*edição* — são dois estados diferentes, e confundi-los é a mordida da seção 7.

### 6.2 O anel de foco — e a colisão que precisa ser dita

Hoje **não há marca de foco em botão nenhum** no tema normal: `theme.css` só
declara `:focus` para `combobox` e `entry` (borda ciano de 2 px), e para botão
só no modo de **alto contraste**. Navegar com o controle hoje moveria um foco
**invisível**.

A cura tem de ser um **anel por dentro** (`box-shadow: inset`), pelo mesmo
motivo pelo qual a D-18 escolheu isso para a seleção: **não muda um pixel de
tamanho**, e a tira de abas tem orçamento apertado (62 px de tira, 654 px de
teto de página).

> **Colisão declarada, e ela é entre frentes.** Depois da D-18, a borda de um
> mesmo widget vai carregar **identidade** (a cor da peça), e o anel por dentro
> vai carregar **seleção**. Este anel de **foco de navegação** seria a terceira
> coisa disputando a mesma aresta. A frente da cor está sendo medida na bancada
> **agora** e eu não toquei nos arquivos dela. **Proposta:** o foco de navegação
> usa uma marca de natureza diferente — anel **pontilhado** por dentro, em
> `@text_muted`, 1 px — para não competir com nenhuma das duas cores. Fecha com
> a frente da cor antes de virar CSS.

### 6.3 A aba Navegação ganha a segunda metade

A aba passa a ter duas seções sob o mesmo nome, como a sprint de 14/08 previu:

| seção | conteúdo |
|---|---|
| **Comandar o PC** | exatamente as duas colunas de hoje, intactas |
| **Navegar esta janela** | a tabela nova: R1 → aba da direita · L1 → aba da esquerda · Cruz → escolher · Círculo → voltar à tira de abas · D-pad → andar · PS → largar a navegação |

E a linha que a D-20 exige por escrito, porque *"isso tem de estar dito na
tela"*:

> *Com esta janela na frente, o R1 e o L1 trocam de aba. Fora dela, continuam
> sendo o Alt+Tab do perfil ativo.*

**A D-23 aparece aqui como ausência:** não há seletor de controle nesta seção,
não há tabela por unidade, não há coluna por jogador. Um mapeamento, para
todos. Se um dia alguém propuser um seletor aqui, é esta linha que o reprova.

---

## 7. As mordidas — os testes que têm de reprovar com a cura arrancada

Sem estas, a frente não fecha. Cada uma nomeia **o que arrancar** e **o que
tem de reprovar**.

| # | o que prova | arranque isto → tem de reprovar |
|---|---|---|
| 1 | **o primeiro X do dono não vaza** | tire a subtração de `dispatch_gamepad`: o vpad do dono recebe `cross` no tique da borda |
| 2 | **só o dono paga** | com o Sony 2 como dono, o vpad do **Sony 3** tem de continuar recebendo `cross`. Trocar o alvo da máscara por "todos" reprova |
| 3 | **borda, não nível** | três snapshots com R1 **segurado** avançam a aba **uma vez**. Sem a detecção de borda, avançaria 180 vezes em 3 s |
| 4 | **o carrossel dá a volta E pula escondida** | esconda a página "No jogo", ande a roda inteira. Trocar por `set_current_page((i+1) % n)` **congela** e reprova |
| 5 | **sem foco, nada** | monte o store com `wm_class = "unknown"` (o valor medido com jogo em foco) e sem pulso da GUI: a navegação **não** age. É o Alt+Tab dentro do jogo de 29/07 |
| 6 | **o Alt+Tab cala com a janela na frente** | com foco e dono, `emu_buttons` **não** contém `r1`. Arrancar a subtração faz o Alt+Tab voltar |
| 7 | **o selo diz o dono, não o alvo de edição** | dois controles, o 3 navegando e o 2 selecionado no cabeçalho: o texto **não** pode conter "Sony 2". Apontar o selo para `_edit_badge_text` reprova |
| 8 | **o lease expira** | pare de pulsar: em 1 s o dono cai e os quatro voltam ao vpad. Arrancar o prazo deixa botão roubado para sempre |
| 9 | **o gate de timers** | o arquivo novo da GUI declara **um** `GLib.timeout_add` e nenhum `idle_add` que devolva `True` — o molde de `test_status_cards.py`, que nasceu dos 104 % de um núcleo da v3.8.1 |

---

## 8. O custo, em arquivos

**Daemon** — o dono da máquina de estados:

| arquivo | mudança | tamanho |
|---|---|---|
| `daemon/subsystems/navegacao.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha --> | **novo**: foco, lease, dono, contadores por controle, bordas, `mascarar()` | ~180 linhas |
| `daemon/lifecycle.py` | duas linhas: `observar()` no tique (ao lado de `_hotkey_manager.observe`) e a subtração de `emu_buttons` | 2 + comentário |
| `daemon/subsystems/gamepad.py` | uma linha antes de `forward_buttons` (:2039) | 1 |
| `daemon/subsystems/coop.py` | uma linha antes de `forward_buttons` (:1549) | 1 |
| `daemon/ipc_server.py` + `ipc_handlers.py` | o método `navegacao.foco` | ~60 linhas |

**GUI** — quem pinta e quem sabe o foco:

| arquivo | mudança | tamanho |
|---|---|---|
| `app/actions/navegacao_actions.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha --> | **novo**: o tique, o carrossel, o anel, o selo, o pulso de foco | ~220 linhas |
| `app/app.py` | a mixin na lista + `install_navegacao()` | ~4 linhas |
| `app/actions/input_actions.py` | a segunda seção da aba, e o título "Comandar o PC" na de hoje | ~40 linhas |
| `gui/main.glade` | o quadro "Navegar esta janela" com a tabela | ~90 linhas de XML |
| `gui/theme.css` | o anel de foco pontilhado | ~10 linhas |

**Testes**: quatro arquivos novos, um por família (máscara, carrossel, gate de
foco, selo) — as nove mordidas da seção 7.

**Instrumento** (dívida, e ela é real): `scripts/gui-captura/retratar_abas.py`
tem de passar a montar a mixin da aba Navegação, senão **a prova de tela desta
frente fotografa uma tabela vazia** (seção 2.2). É a mesma correção que já foi
feita para Início, Perfis, Gatilhos e "No jogo".

**Não incluído de propósito:** a linha do
[`mapa-controles.csv`](../../data/mapa-controles.csv). O mapa está sendo medido
na bancada agora por outra frente, e o portão
`scripts/check_paridade_transporte.py` vai exigir a linha com o grau certo —
que só existe depois de a navegação rodar na tela dela. **Fica para o fim, e o
grau não pode ser inventado antes.**

### 8.1 A divergência de rota com a página irmã — e ela é decidível

A irmã propõe **tirar o tique rápido da exclusividade da aba Status**
(`status_actions.py`, o `return True` do `BUG-STATUS-TICK-HIDDEN-TAB-01`), e
classifica o risco disso, com razão, como **médio-alto** — é mexer numa cura
existente que nasceu de 104 % de um núcleo.

Esta página propõe **não mexer nela**: um tique próprio, num arquivo próprio,
lendo um método próprio (`navegacao.foco`, seção 5.2) que é da classe de **572
bytes / 0,20 ms** em vez da de **11.655 bytes / 0,78 ms**.

| rota | custo a 20 Hz | o que ela arrisca |
|---|---|---|
| **liberar o tique do `state_full`** (irmã) | ~233 kB/s e ~1,6 % de um núcleo, no worker único | reabre o defeito que a cura de hoje fechou |
| **tique próprio e método leve** (esta) | ~11 kB/s e ~0,4 % de um núcleo | nada existente; o custo é um arquivo e um método novos |

**As duas concordam no essencial** — que a GUI leia **contador de borda** e não
nível — e a discordância é só sobre **por qual cano**. Recomendo o cano
próprio: é 4x mais barato no fio e não põe a mão numa cura que já custou caro.
**Não é decisão dela**; é escolha de quem executar, e fica escrita para não
virar descoberta no meio da implementação.

---

## 9. A pergunta que sobrou — e é uma só

**O dono perde os quatro botões da frente. Perde também o L1, o R1 e o D-pad?**

Por que a pergunta é nova, e não uma tentativa de reabrir o que ela fechou: a
D-22 foi respondida sobre a pergunta *"o X que escolhe na tela também chega ao
jogo?"*, e a resposta nomeou **os quatro botões**. Foi a **D-21**, respondida
depois, que deu significado de navegação ao **R1 e ao L1** — e a proposta da
seção 4 dá ao **D-pad** o papel de andar com o anel de foco. **O conjunto que
navega ficou maior que o conjunto que é roubado**, e isso não é hipótese: é
consequência aritmética das duas respostas juntas.

O que acontece em cada caminho:

| caminho | o que ela sente | o preço |
|---|---|---|
| **(a) só os quatro** — a letra da D-22 | apertar R1 troca de aba **e** o jogo vê o R1 (recarregar arma, trocar item). O D-pad anda na tela **e** anda no jogo | a regra fica fácil de dizer: *"os quatro botões da frente ficam com a janela"*. O jogo recebe comando que ela não quis dar |
| **(b) os quatro + L1/R1 + D-pad** | nada do que navega chega ao jogo enquanto ela está na janela | coerente com o espírito da D-22. Mas o roubo cresce de 4 para 10 botões, e sobram os analógicos, os gatilhos, L3/R3, Options e Create |
| **(c) os quatro + L1/R1, o D-pad não** | o meio-termo: o que muda **aba** é roubado; o que anda **dentro** da página não | o D-pad continua mexendo no personagem enquanto ela escolhe na tela |

**Minha recomendação é (b)**, e o motivo é o mesmo que ela usou para escolher
"roubado": se o botão está fazendo uma coisa na tela, ele não devia estar
fazendo outra no jogo ao mesmo tempo. O limite continua sendo o que ela já
fixou — **os analógicos e os gatilhos nunca são roubados**, para o personagem
não travar em pé.

**Duas coisas que decorrem, e que eu decido se ela não quiser gastar palavra:**

1. **Quadrado e triângulo ficam roubados sem função** (a D-22 nomeou os quatro
   como bloco). Eu **deixo assim** e não invento verbo — é o lugar natural de um
   "salvar" ou "aplicar" no futuro, e inventar agora é chute.
2. **Não proponho tempo de espera para largar a navegação.** Sai pelo PS ou pela
   perda de foco, que foram as duas saídas que a sprint de 14/08 já desenhou.
   Um tempo de espera seria invenção minha.

---

## 10. O que eu NÃO fiz, e por quê

- **Não escrevi uma linha de código.** A regra desta fase é PROVA-DE-TELA-01: o
  produto é a proposta que ela consegue decidir **vendo**.
- **Não rodei `retratar_abas.py`.** A captura é recurso disputado nesta leva e
  as fotos de hoje às 03:12 respondem as minhas perguntas — o `main.glade` e o
  `input_actions.py` não mudaram desde então. Reaproveitei também o
  `mesa_cheia_cabecalho.png` de 14/08, o único retrato desta casa que alcança o
  cabeçalho.
- **Não medi quanto tempo dura um toque de R1 dela.** A aritmética dos 100 ms do
  tique da GUI é aritmética, não medição; a conclusão da seção 5.1 não depende
  desse número (ela vale mesmo com o toque longo, porque o que vaza é a **borda
  de entrada**, não o toque inteiro).
- **Não toquei em `mapa-controles.csv` nem na sprint UNIDADE-COR-01** — estão
  sendo medidos na bancada agora.
- **Não reabri a D-23.** A ausência de seletor por controle na seção 6.3 é a
  decisão dela executada, não esquecida.
