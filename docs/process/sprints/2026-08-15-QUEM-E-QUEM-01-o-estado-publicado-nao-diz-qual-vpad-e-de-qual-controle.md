# QUEM-É-QUEM-01 — o estado publicado não diz qual vpad é de qual controle

- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf` com a árvore suja (a cura MESA-CHEIA-12 está escrita e **não
  commitada**).
- **Grau:** **MEDIDO.** A pergunta foi feita por ela às 04:05 — *"o vpad e o
  físico correspondem ao mesmo? garantimos isso?"* — e a resposta **não pôde ser
  lida do estado publicado**. Foi paga apertando botão.
- **Índice da leva:** [a cor do controle e o som de cada jogador](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md),
  onde esta dívida está **registrada** (§12.2) e **não consertada**. Esta sprint
  é o dono que aquela linha não tinha.
- **Depende de:** nada. É observabilidade pura — não muda comportamento nenhum.
- **Custo mínimo:** 2 h 05 (três entregas, a mais cara de 55 min)
- **NÃO confundir com o instrumento:** `scripts/ensaios/quem_e_quem.py` nasceu na
  mesma madrugada e resolve a mesma pergunta **por fora**, subindo o sysfs. Ele é
  a régua do ENSAIO 2+2 e é ótimo. Esta sprint é sobre o **produto**: enquanto o
  estado publicado não disser quem é quem, todo consumidor — a próxima sessão, um
  `jq` no socket, um instrumento novo — refaz aquele trabalho por conta própria.

---

## 0. ENTREGUE — 15/08/2026, na árvore

As três entregas estão de pé, com os nomes que a §2 escolheu:

| # | onde | o que ficou |
|---|---|---|
| **E1** | `daemon/subsystems/coop.py` (`CoopManager.mesa`) + `daemon/ipc_handlers.py` | `coop.mesa[]` — um item por jogador com `{uniq, player, is_primary, vpad_backend, vpad_uniq, vpad_nome, vpad_indice, aguardando_grab, nome_divergente}`. `coop.players` **ficou**, ao lado |
| **E2** | `daemon/ipc_handlers.py`, bloco `rumble_ff.per_vpad[]` | `vpad_uniq`, `vpad_nome` e `vpad_indice`, da MESMA função (`coop.identidade_do_vpad`) que monta a E1 |
| **E3** | `coop._item_da_mesa` | `nome_divergente` — `True` só quando os dois inteiros são conhecidos E diferem. É alarme, não afirmação simétrica |

**Onde ISTO CHEGA NA TELA** (regra dela de 09/08, e é a única coisa que vai
além do que a §5 previa): o rótulo do título de cada card da aba Status ganhou
uma **dica** (`controller_card.dica_do_titulo`) — *"Alimenta o gamepad virtual
do Jogador 2 (uhid · 02:fe:00:00:00:02)."*, mais o nome real do dispositivo
quando `nome_divergente`. Escolhida como DICA, e não como linha do card, por
duas razões: o endereço é **diagnóstico** e não vocabulário de interface (o
alvo por MAC foi derrubado por ela em 13/08 e nada aqui o reabre), e o corpo do
card tem altura amarrada — uma linha nova empurraria os quatro cards da mesa.
**Custa zero pixel, e por isso não aparece em foto de aba: o fecho com o olho
dela (PROVA-DE-TELA-01) é passar o cursor no título, e continua PENDENTE.**

Testes: `tests/unit/test_quem_e_quem_01_o_estado_diz_qual_vpad.py` (18) e
`tests/unit/test_quem_e_quem_01_na_tela.py` (3, GTK real — a fiação). Seis
arrancadas conferidas, uma por cura.

O instrumento `scripts/ensaios/quem_e_quem.py` teve o fato substituído: ele
declarava *"o `state_full` publica `coop.players` como um NÚMERO, não como
lista"*, o que deixou de ser verdade nesta data.

---

## 1. O defeito, medido — e ele custou um passo manual esta madrugada

Com quatro controles na mesa, ela perguntou se o gamepad virtual do jogador N
corresponde ao controle físico N. **A resposta é sim** — foi conferida apertando
X em cada controle e vendo qual `/dev/input/event*` emitia `EV_KEY` code 304
value 1, um de cada vez, com o branco confirmado isoladamente em quatro eventos.

**A resposta estava certa; o método é que era o defeito.** Nada no estado
publicado permite chegar nela por leitura.

### 1.a O que o `state_full` publica hoje

Conferido contra `tests/fixtures/state_full_quatro_controles.json`, a fotografia
real da mesa dela de 14/08:

| campo | o que é | o que falta |
|---|---|---|
| `coop.players` | o inteiro **`4`** | é uma **contagem**, não uma lista. Não nomeia ninguém |
| `controllers[]` | `uniq`, `player`, `player_slot`, `transport`, `vpad_backend`, `vpad_motivo` | é o lado **físico**, e está completo |
| `counters.per_vpad[]` | `player`, `backend`, e os contadores de rumble e de motion (`ipc_handlers.py:2599-2620`) | é o lado **virtual**, e **não carrega o nó**: nem o caminho `/dev/input/event*`, nem o nome, nem o `uniq` forjado |

A ponte entre as duas listas é o inteiro `player`, e ela funciona **dentro da
janela** — é assim que o card casa com o vpad
(`app/widgets/controller_card._bloco_do_vpad`). Para **qualquer coisa fora da
janela** — um instrumento de ensaio, um `jq` no socket, a próxima sessão — a
ponte não existe: o inteiro não diz em que dispositivo do kernel olhar.

### 1.b E a MESA-CHEIA-12 abriu uma segunda fresta, no mesmo lugar

Isto é novo de hoje, e é a parte que ninguém registrou ainda.

O nome do gamepad virtual é composto em
`integrations/uhid_gamepad.py:1038`:

```
f"DualSense Wireless Controller (Hefesto P{self.player})"
```

e o `uniq` forjado dele, em `integrations/uhid_gamepad.py:568-575`:

```
f"02:fe:00:00:00:{player:02x}"
```

**Os dois carregam o mesmo inteiro: `player_index`** — o índice de alocação do
co-op, congelado no instante em que aquele jogador nasceu.

Até 14/08 isso era inofensivo, porque `controllers[].player` publicava **o mesmo
`player_index`**. A MESA-CHEIA-12 (na árvore, 15/08 01h00) trocou o número
publicado pela **fila de chegada** — a mesma que acende a lâmpada — e com isso:

> **o número que o `state_full` chama de `player` deixou de ser o número que
> está no NOME e no `uniq` do vpad daquele jogador.**

Quem casar `controllers[].player == N` com `Hefesto P{N}` a partir de agora pode
casar o card de um controle com o dispositivo de outro. A cura declara isso como
o que ficou de fora (`test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py`,
`RAZAO_XFAIL`), e a razão é boa — renomear o vpad no meio da sessão o jogo
enxerga como gamepad desconectando. **Mas o que ficou de fora foi o
comportamento, não o AVISO**: nada no estado publicado sinaliza que os dois
inteiros podem divergir.

### 1.c O terceiro pedaço: o físico fica MUDO para quem mede

**Medido em 15/08, em dois ensaios.** Os `/dev/input/event*` dos controles
**físicos** não entregam evento nenhum a um leitor externo enquanto o co-op está
ligado, porque o co-op faz `EVIOCGRAB` neles. **É comportamento correto** — é
literalmente o que esconde o físico do SDL para o jogo ver só o vpad.

O custo é de método, e é caro: **um instrumento ingênuo mede zero e conclui que
o aparelho está calado.** Foi por isso que a correspondência vpad↔físico só se
estabeleceu no nó **virtual**, e por isso que o passo manual foi necessário.

Isto já está escrito como armadilha do ENSAIO 2+2 (índice da leva, §11.3, item
2). **Aqui ele entra como requisito de produto:** enquanto o estado não disser
quem é quem, todo ensaio com mais de um controle paga o passo manual de novo —
inclusive o 2+2 que ela pediu às 04:20.

---

## 2. As três entregas

| # | entrega | custo |
|---|---|---|
| **E1** | **`coop.players` deixa de ser só um número**: ao lado dele, uma lista `coop.mesa[]` com `{uniq, player, vpad_uniq, vpad_nome}` — uma linha por jogador com vpad vivo | 55 min |
| **E2** | **`per_vpad[]` carrega a identidade do nó**: `vpad_uniq` (o `02:fe:…`) e `vpad_nome`, que o objeto já sabe (`uhid_gamepad.py:1038` e `:1061`) e não publica | 35 min |
| **E3** | **O aviso da divergência**: quando o `player` publicado ≠ o inteiro que está no nome do vpad, o estado diz isso num campo próprio, em vez de deixar quem lê descobrir sozinho | 35 min |

**A E1 é a que fecha a §12.2 do índice**, e é a que o ENSAIO 2+2 consome. As
outras duas são o que impede a fresta de 1.b de virar uma medição confiante e
errada — que é a armadilha nº 1 desta casa.

**Compatibilidade:** `coop.players` **fica**. É lido pela CLI
(`ipc_handlers.py:4206` documenta `result["players"]`) e por três outros pontos;
tirá-lo seria pagar um preço de quebra por uma entrega de observabilidade.
`coop.mesa` nasce **ao lado**, como o `per_vpad` nasceu ao lado do agregado, pelo
mesmo motivo escrito em `ipc_handlers.py:2505-2507`: *"o agregado escondia QUAL
vpad recebeu o quê"*.

---

## 3. O que muda para quem mede

```
   HOJE — a pergunta "o vpad P2 é de qual controle?"
   ┌──────────────────────────────────────────────────────────┐
   │ coop.players = 4                                          │
   │ controllers[] .player = 1,2,3,4  (a fila)                 │
   │ per_vpad[]    .player = 1,2,3,4  (a fila)                 │
   │ /dev/input/*  nome    = "Hefesto P1..P4" (a ALOCAÇÃO)     │
   └──────────────────────────────────────────────────────────┘
     nenhuma linha liga um MAC a um nó — e dois dos inteiros
     acima podem não ser o mesmo número

   DEPOIS
   ┌──────────────────────────────────────────────────────────┐
   │ coop.mesa = [                                            │
   │   {uniq: "…", player: 1, vpad_uniq: "02:fe:00:00:00:01",│
   │    vpad_nome: "…(Hefesto P1)"},                          │
   │   {uniq: "…", player: 2, vpad_uniq: "02:fe:00:00:00:04",│
   │    vpad_nome: "…(Hefesto P4)", nome_divergente: true}    │
   │ ]                                                        │
   └──────────────────────────────────────────────────────────┘
     o ensaio lê o nó certo, e a divergência é DITA
```

---

## 4. O teste que MORDE

Arquivo novo, `tests/unit/test_quem_e_quem_01_o_estado_diz_qual_vpad.py` — mais
o irmão `tests/unit/test_quem_e_quem_01_na_tela.py`, que trava a FIAÇÃO com GTK
real (o precedente do rumble: um teste que chamava a peça e não a fiação passou
com a cura arrancada). Os dois existem desde 15/08/2026.

### Mordida 1 — a lista que não nomeia ninguém (é a principal)

**Arrancar:** manter `coop.players` como única fonte e não publicar `coop.mesa`.

**Por que reprova:** o teste monta a mesa de quatro (endereços da faixa forjada
`aa:bb:cc:…`, a mesma allowlist de `test_anonimato_de_fixtures.py`), pede o
`state_full` e exige que **para cada `uniq` da mesa exista uma linha com o
`vpad_uniq` correspondente**. Com só o inteiro, não há o que casar e o teste cai.

Esta é a principal porque é a que substitui o passo manual: se ela passar, a
pergunta de 04:05 se responde por leitura, e o ENSAIO 2+2 não a paga de novo.

### Mordida 2 — a divergência que passa calada

**Arrancar:** publicar `coop.mesa` com `vpad_uniq` derivado de
`controllers[].player` em vez de perguntar ao objeto do vpad.

**Por que reprova:** o dublê põe o co-op alocando `player_index` **4** para o
controle que a fila numera **2** — a mesa dela desta madrugada. Derivando do
`player`, o estado diz `02:fe:00:00:00:02`; o dispositivo que existe de verdade
é o `…:04`. O teste lê o `uniq` **do objeto** e cai quando o campo publicado
discorda dele.

É a mordida que impede a E1 de virar uma mentira nova com formato melhor.

### Mordida 3 — o físico mudo não vira "controle calado"

**Arrancar:** um instrumento que conclua "sem evento, logo sem controle" ao ler
o evdev físico com o co-op ligado.

**Por que reprova:** o teste simula o `EVIOCGRAB` do co-op e exige que o
`state_full` continue afirmando o controle **presente e com vpad vivo** — ou
seja, que a ausência de evento no nó físico não apareça em lugar nenhum como
ausência de controle. É a mordida de método: ela grava no código a armadilha que
custou o passo manual de hoje.

### O que estes testes NÃO provam

Que a correspondência está certa **no aparelho**. Isso se prova apertando botão,
e foi provado hoje. O que eles provam é que **da próxima vez não vai precisar**.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **Nada** no estado publicado: ele não muda comportamento e não escolhe entre dois caminhos | as três entregas e as três mordidas |
| **A dica do card** (acrescentada na execução, pela regra dela de 09/08 — *tudo tem de chegar na interface*): a frase, e se ela basta. É PROVA-DE-TELA-01 e está **pendente** — a dica só aparece com o cursor no título, então nenhuma foto de aba a mostra | escrever a dica e a fiação; **não** mexer no layout do card |
| *(fica de fora, e é da ORDEM-DE-CHEGADA-01)* **o nome do vpad passar a seguir a fila** — exigiria recriar o vpad no meio da sessão, e o jogo enxerga isso como desconectar | não fazer, e **dizer** que divergiu (E3) |

---

## 6. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: tudo.** As três mordidas rodam sobre dublês; o `state_full` é
função do estado do daemon e a suíte já o exercita com quatro controles.

**Só a bancada dela:** que a lista publicada **bate com a realidade** — o mesmo
teste do X, uma vez, para calibrar a régua contra o aparelho. É o contrário da
armadilha *"o instrumento mente mais que o produto"*: aqui a régua nova se
confere **contra a contagem manual que já foi feita hoje**, e depois disso o
manual sai de cena.
