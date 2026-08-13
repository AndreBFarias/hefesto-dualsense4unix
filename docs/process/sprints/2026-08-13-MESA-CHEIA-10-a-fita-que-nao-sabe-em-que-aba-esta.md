# MESA-CHEIA-10 — a fita que não sabe em que aba está

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Índice da leva:** [as ondas da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a **decisão D-2** dela. **Anda junto com a
  [01](2026-08-13-MESA-CHEIA-01-a-fita-do-alvo-ganha-a-cor-de-cada-um.md)** — as
  duas mexem no mesmo widget e as duas servem as dez abas
- **Custo mínimo:** 60 min
- **É a mentira que vale por SEIS abas de uma vez**, e não é defeito de aba
  nenhuma

---

## 1. O defeito, medido

A fita *"Ajustes vão para: [Sony 1 · USB] [Sony 2 · BT] [Todos]"* mora no
**cabeçalho**, acima do notebook — `header_bar` em
`src/hefesto_dualsense4unix/gui/main.glade:136`, com a legenda montada em
`app/actions/status_actions.py:1497` e o selo *"Editando: {alvo}"* em `:1858`.

**Ela nunca sabe em que aba está.**

A prova é de contagem, não de leitura: `_set_target_strip_visible`
(`app/actions/status_actions.py:1673`) tem **exatamente três chamadores** —
`:2094`, `:2177` e `:2505` — e os três decidem por **contagem de controles** ou
por **daemon offline**. O `_on_notebook_switch_page` (`app/app.py:957`), que é
quem sabe qual aba está à frente, **não a menciona**. Não existe um único `if`
de aba em todo o caminho.

```
   ┌─ header_bar (gui/main.glade:136) ───────────────────────────┐
   │  Ajustes vão para:  (•)Sony 1·USB  ( )Sony 2·BT  ( )Todos   │ ← sempre visível
   │  Editando: Controle 2 (BT)                                  │
   ├─ main_notebook (gui/main.glade:212) ────────────────────────┤
   │  Início │Status│No jogo│Gatilhos│Lightbar│Rumble│Perfis│…    │
   │                                                             │
   │   …e aqui embaixo, em seis das dez, nada obedece            │
   │   àquele "Controle 2".                                      │
   └─────────────────────────────────────────────────────────────┘
```

### Onde ela é verdade e onde é falsa — contado, aba por aba

Quem lê `_edit_target_uniq` (`app/actions/status_actions.py:427`) na árvore
inteira de `src/`:

| aba | módulo | a fita vale? | endereço |
|---|---|---|---|
| Status | é a **dona** do alvo | **vale** (áudio por controle) | `app/actions/status_actions.py:427` |
| Gatilhos | `triggers_actions.py` | **vale** | `:164-166` |
| Lightbar | `lightbar_actions.py` | **vale** | `:230-237` (`_edit_uniq`) |
| Rumble | `rumble_actions.py` | **vale no rascunho** | `:505-514` (`_rumble_edit_uniq`) |
| **Início** | `home_actions.py` | **NÃO** | zero leituras do alvo |
| **No jogo** | `status_actions.py` (painéis) | **NÃO** | painel de leitura |
| **Perfis** | `profiles_actions.py` | **NÃO** | `grep -c uniq` = **0** em **3357** linhas (contado em 13/08) |
| **Sistema** | `daemon_actions.py` | **NÃO** | o alvo é systemd/Steam/PipeWire |
| **Emulação** | `emulation_actions.py` | **NÃO** | as ocorrências de `uniq` ali são agrupamento de nós de `/dev/input`, não alvo de edição |
| **Navegação** | `mouse_actions.py`, `input_actions.py` | **NÃO** | zero ocorrências nos dois |

**Quatro valem, seis não.**

### A ressalva existe — e mora onde ninguém lê

O **tooltip** da fita (`app/actions/status_actions.py:1484-1487`) enumera o
escopo real: *"Controle alvo das ações (lightbar, gatilhos, LEDs, rumble)"*. **A
lista está certa** e exclui as seis de propósito. Mas é tooltip: invisível até
alguém parar o ponteiro em cima.

**Esta casa já reconheceu esse padrão como defeito uma vez.** O PLAYER-01 tirou o
terceiro papel do chip de dentro de um tooltip e o pôs na tela
(`app/actions/status_actions.py:1489-1494`). Repetir a mesma solução na mesma
fita é usar o léxico que já existe, não inventar.

---

## 2. Por que esta sprint anda colada na 01

A [01](2026-08-13-MESA-CHEIA-01-a-fita-do-alvo-ganha-a-cor-de-cada-um.md) pinta
os chips com a cor de cada jogador. **Pintar uma promessa falsa a torna mais
convincente, não mais verdadeira.** As duas mexem no mesmo widget, custam 150
minutos somadas, e servem as dez abas de uma vez — separá-las entrega meia coisa
duas vezes.

Elas continuam sendo **duas sprints** porque a 01 é só desenho e esta espera uma
decisão dela (a **D-2**). Se ela responder a D-2 hoje, saem juntas.

---

## 3. O que muda na tela

O gancho é o mesmo nas duas opções: um gate por **id de página** no
`_on_notebook_switch_page` (`app/app.py:957`) — que já identifica a aba por id e
nunca por índice, que é a regra da casa desde que dois pollers gatearam por
índice e passaram a bater por sorte.

```
   OPÇÃO A — ESCONDER  (a fita some nas seis)
   ┌─ Aba Perfis ───────────────────────────────────────────────┐
   │  Hefesto                                                    │
   ├─────────────────────────────────────────────────────────────┤
   │  Início │Status│No jogo│Gatilhos│…│[Perfis]│…                │
   └─────────────────────────────────────────────────────────────┘
     limpo — e o contexto SOME ao trocar de aba e volta ao voltar: pisca


   OPÇÃO B — REQUALIFICAR  (a fita muda de frase)
   ┌─ Aba Perfis ───────────────────────────────────────────────┐
   │  Hefesto            Esta aba vale para todos os controles   │
   ├─────────────────────────────────────────────────────────────┤
   │  Início │Status│No jogo│Gatilhos│…│[Perfis]│…                │
   └─────────────────────────────────────────────────────────────┘
     mantém o contexto e ENSINA — e é mais texto numa fita já densa
```

**E o caso que a foto tem de mostrar junto:** a volta. Sair da Perfis para a
Gatilhos e a fita reaparecer **com o mesmo alvo de antes**, sem piscar e sem
perder a escolha.

---

## 4. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_10_a_fita_sabe_a_aba.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

A entrega expõe **uma função pura**, sem GTK:

    a_fita_vale_na_aba(page_id: str) -> bool

e a lista de ids vem do `main.glade`, não de uma constante escrita à mão.

### Mordida 1 — o gate por índice (é a mordida principal)

**Arrancar:** decidir por `notebook.get_current_page()` (o índice) em vez do id
da página.

**Por que reprova:** o dublê insere uma aba **nova antes da Perfis**. Com o
índice, a fita passa a calar na aba errada e a mentir na Perfis; com o id, nada
muda. O teste insere a aba e exige que os vereditos das dez continuem os mesmos.

Esta é a principal porque é a regra da casa que já foi violada antes: dois
pollers gatearam por índice e batiam por sorte até alguém inserir uma página.

### Mordida 2 — a aba que nasce sem veredito

**Arrancar:** deixar a função devolver `True` (ou `False`) para id desconhecido.

**Por que reprova:** o teste compara a lista de páginas do
`src/hefesto_dualsense4unix/gui/main.glade` (as dez de hoje) com a tabela da
função e exige **cobertura total**. Aba nova sem veredito **estoura**. Sem isso,
a décima primeira aba nasce fora do assunto e ninguém percebe — que é
exatamente como a *"No jogo"* atravessou um censo inteiro sem ser medida.

### Mordida 3 — o alvo que se perde na ida e volta

**Arrancar:** limpar `_edit_target_uniq` quando a fita se esconde.

**Por que reprova:** o teste vai da Gatilhos com "Sony 2" escolhido para a
Perfis e volta, e exige que o alvo continue "Sony 2". Esconder o widget não pode
apagar o estado — e a casa já fixou o oposto disso de propósito na **R-16**, que
mantém o alvo quando o controle **some da mesa**. Perdê-lo por troca de aba seria
mais frágil que perdê-lo por desconexão.

### Mordida 4 — a tabela que envelhece calada

**Arrancar:** a asserção de que cada "NÃO" da tabela carrega **motivo e data**.

**Por que reprova:** a lista de recusa não é opinião; cada linha tem origem
datada (decisão dela de 10/08 para Início/Emulação/Perfis; medição de código
para a Navegação). Uma lista sem motivo apodrece e a próxima pessoa a reabre do
zero.

### O que este teste NÃO prova

Que a fita não pisca. Um `OffscreenWindow` não passa pelo compositor, e "pisca"
é um fenômeno de compositor.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **D-2 — esconder ou requalificar?** É o que trava a sprint. Esconder é limpo e pisca; requalificar ensina e é mais texto | montar a que ela escolher; o gancho é o mesmo |
| **Se requalificar: qual frase?** *"Esta aba vale para todos os controles"* é proposta minha, e frase nova é léxico — logo é dela | escrever a que ela aprovar |
| **A lista das seis está certa?** Se ela quiser alvo em alguma delas, a decisão de 10/08 é revista — e quem revoga decisão dela é ela | escrever a lista aprovada, com a data de cada veredito ao lado |
| — | o gate por id, a função pura, as quatro mordidas |

---

## 6. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** as quatro mordidas (a função é pura e a lista sai do `.glade`),
mais a foto offscreen de duas abas — uma em que a fita vale e outra em que não.

**Só a bancada dela:** que a troca de aba **não pisca** no compositor dela, e que
a frase requalificada (se for a opção B) cabe na fita com quatro chips ao lado
sem quebrar linha.

**Ela vê isto inteiro hoje, com um controle só** — a fita já aparece com 1+
controle desde a SELETOR-UNO-01 (`app/actions/status_actions.py:2082-2085`), e
"em que abas ela vale" não depende de quantos estão na mesa. É a sprint desta
leva que menos precisa da mesa cheia e a que mais abas conserta.
