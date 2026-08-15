# ORDEM-DE-CHEGADA-01 — a fila que ela pediu não é a fila que o produto guarda

- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf` com a árvore suja — a cura MESA-CHEIA-12 estava escrita e
  ainda não commitada naquela hora (ela entrou depois, em `9441678`).
- **Grau:** **MEDIDO** na bancada dela, com os quatro DualSense na mesa. A
  divergência foi observada por ela primeiro, e reproduzida em código depois.
- **Índice da leva:** [a cor do controle e o som de cada jogador](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
- **Status (15/08, tarde):** **ela respondeu, e a E2 está ENTREGUE.** A palavra
  dela é a **D-30** de
  [AS-DECISOES-RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md): *"(b)
  ordem do momento, CONGELADA quando a mesa estabiliza. Quem cai e volta
  recupera o número. O gravado não some: vira desempate."* A E2 saiu no commit
  `feat(identidade): a fila do momento, e ela congela quando a mesa para de
  mexer` (`86563c2`). A **E3** continua em aberto.
- **O que esta sprint NÃO é:** ela não desfaz a MESA-CHEIA-12. A MESA-CHEIA-12
  está certa no que se propôs (unir dois números que divergiam) e está na
  árvore. Esta sprint é sobre **em qual dos dois eles foram unidos**.

---

## 1. O que ela viu, e as palavras dela

Às 03h37 de 15/08 ela deu **reset de fábrica nos quatro controles** e re-pareou
do zero, um de cada vez, na ordem que eu pedi: **vermelho, azul, branco, roxo**
(as confirmações dela chegaram às 03:39, 03:41, 03:45 e 03:47).

Às 03:54:51 ela escreveu, sobre o número de jogador:

> *"não, to falando que deve ser lembrado por ordem de conexão naquele momento
> apenas. **Não uma imagem fixa salva por mec**, o bond mesmo se desfaz com
> facilidade. Mas por exemplo conectamos hoje. Vermelho, deveria ser o player 1,
> azul, o player 2, branco o player 3, roxo o player 4. mas tá agora, vermelho
> 1, branco 2, roxo 3, azul 4 e a nossa ordem deveria sobrescrever a parte da
> steam inclusive igual quando descobrimos como fazer junto ao lightbar"*

São **três pedidos numa frase só**, e eles não são o mesmo pedido:

| # | o pedido | quando esta sprint foi escrita (03h54) | depois da E2 (`86563c2`) |
|---|---|---|---|
| **A** | o número sai da **ordem de conexão daquele momento** | **NÃO** — saía da ordem de **primeira aparição**, gravada por MAC | **SIM** — `_ordem_do_momento_locked` ordena por onda de chegada |
| **B** | **não** é uma imagem fixa salva por MAC | **NÃO** — era exatamente uma imagem fixa salva por MAC (`controllers.json`) | **SIM, com a ressalva que ela mesma pôs:** o gravado não some, vira **desempate** e recebe a foto quando a mesa congela |
| **C** | a ordem da casa **sobrescreve a da Steam**, como já se fez com a lightbar | **não medido nesta sessão** — ver §6 | **continua não medido** |

E o que ela relatou — *"vermelho 1, branco 2, roxo 3, azul 4"* — é o produto
funcionando **exatamente como projetado**. O defeito não é um bug: é uma decisão
antiga que a decisão nova dela contradiz.

---

## 2. O mecanismo, lido no fonte

### 2.a Onde o número nasce

`src/hefesto_dualsense4unix/daemon/subsystems/identity.py`:

| passo | endereço | o que faz |
|---|---|---|
| entrada na fila | `identity.py:586-620` (`_assign_locked`) | `rank = max(ocupados) + 1` — **fim da fila**, na primeira vez que aquele MAC é consultado |
| gravação | `identity.py:610-612` | `self._ordem[key] = rank`; `self._dirty = True` quando o MAC é persistível |
| exibição | `identity.py:646-664` (`_posicao_locked`) | `1 + quantos PRESENTES têm rank menor` |
| porta pública | `identity.py:543-583` (`slot_for`) | atribui na primeira consulta (lazy, D1) e devolve a colocação |

O `rank` **é gravado em disco**. O arquivo dela, agora
(`~/.config/hefesto-dualsense4unix/controllers.json`, `version: 3`, escrito
15/08 01:15), tem quatro entradas `dualsense` com `rank` **1, 2, 3 e 4** — e
esses ranks foram atribuídos quando cada endereço apareceu pela primeira vez,
não quando ela ligou o controle às 03:41.

**A colocação é dinâmica; a ORDEM não é.** Com os quatro presentes, a colocação
é a ordem dos ranks — e a ordem dos ranks é a de um dia qualquer do passado.

### 2.b E o produto DECLARA que é assim, de propósito

O cabeçalho do módulo (`identity.py:1-60`) não esconde nada — ele registra três
auditorias que **construíram** este comportamento:

- **R-15 (23/07)**: a expiração por "sessão esvaziou" foi **REMOVIDA**, e o
  motivo está escrito: ela *"trocava cor/número de dono conforme a **ORDEM DE
  WAKE** — desligar os dois DualSense e religar em ordem invertida devolvia o 1
  ao que voltasse primeiro"*, e abria janela de duplicata — *"a queixa 'dois
  player 1, dois player 2'"* (`identity.py:15-23`);
- **R-23 (25/07)**: o número passou a sobreviver **ao boot**, porque *"TODO
  reboot renumerava por ordem de conexão"* era a queixa *"ao abrir os jogos ou o
  perfil, os controles se reenumeram e nunca sei o que é o quê"*
  (`identity.py:24-34`);
- **NUM-01 (25/07)**: o que se persiste deixou de ser o número e passou a ser o
  **lugar na fila**; a posição 1..N é derivada dos presentes (`identity.py:44-60`).

E a linha que fecha o caso, `identity.py:32-34`:

> *"renumerar por vontade dela continua sendo o **GESTO explícito** ('Renumerar
> agora' → `compact`)"*

**Ou seja: o comportamento que ela pediu em 15/08 é literalmente o que R-15
arrancou em 23/07, e por um motivo medido.** Isto não a torna errada — torna a
decisão cara, e é por isso que ela tem de ser dela e não minha.

### 2.c O que a MESA-CHEIA-12 fez, e o que ela não podia decidir

A cura de 15/08 01h00 (`9441678`) uniu dois números que
divergiam: a lâmpada acesa no plástico e o `player` publicado no `state_full`.
`CoopManager.player_indexes()` passou a sair de
`CoopManager.numeros_de_jogador()` (`daemon/subsystems/coop.py:1162-1212`), a
mesma função que escolhe o desenho.

**Isso está certo, e não se desfaz.** Duas superfícies que falam do mesmo
controle não podem discordar.

Mas a união foi feita **na fila persistida** — que é o lado B da frase dela.
Depois da MESA-CHEIA-12, a lâmpada e o rótulo concordam, e **os dois estão na
ordem que ela disse que não queria**. O defeito saiu de *"a tela e o plástico
discordam"* e virou *"a tela e o plástico concordam na ordem errada"*, que é
menos confuso e igualmente distante do que ela pediu.

---

## 3. As três entregas

| # | entrega | grau | custo |
|---|---|---|---|
| **E1** | **A pergunta na mesa dela, com o preço dos dois lados** (seção 5). Nada em código antes disso | **RESPONDIDA** (D-30, 15/08) | 10 min dela |
| **E2** | **A ordem do momento, que ela escolheu:** uma fila de SESSÃO ao lado da fila persistida — não no lugar dela | **ENTREGUE** (`86563c2`) | 90 min |
| **E3** | **O gesto "Renumerar agora" alcançável de onde ela está** — hoje é IPC (`identity.renumber`) e não tem botão nas abas onde a queixa nasce | PLANO | 40 min |

### E2 — ENTREGUE em 15/08: o que foi escrito

A E1 foi respondida com **(b) ordem do momento, congelada quando a mesa
estabiliza**, e a E2 saiu no mesmo dia. O que está na árvore, em
`daemon/subsystems/identity.py`:

| peça | o que faz |
|---|---|
| `_chegada` (`identity.py:473`) | a **fila do momento**: o dicionário MAC -> número da onda em que aquele endereço chegou |
| `JANELA_DE_ONDA_SEC = 0.5` (`identity.py:271`) | quem chega dentro da mesma janela **chega junto**, e o desempate cai para o gravado |
| `_marcar_chegada_locked` (`identity.py:740`) | abre ou reaproveita a onda corrente quando um MAC conecta |
| `_ordem_do_momento_locked` (`identity.py:762`) | ordena por `(chegada, rank gravado, chave)` — **a fila do momento manda, o gravado desempata**, que é a frase dela |
| `JANELA_MESA_ESTAVEL_SEC = 4.0`, `_avaliar_mesa_locked` e `_congelar_locked` (`identity.py:290`, `:776`, `:792`) | quando a mesa passa quatro segundos sem ninguém entrar nem sair, a ordem do momento é **gravada** por PERMUTAÇÃO dos `rank` que os presentes já detêm — é o "CONGELADA" da resposta dela, e é o que faz quem cai e volta recuperar o número |
| `_mesa_mexeu_locked` (`identity.py:728`) | descongela nos três pontos em que a mesa muda |
| `snapshot_chegada` (`identity.py:827`) | a fila do momento, legível de fora, para o teste e para o IPC |

Do lado do `CoopManager` **nenhuma linha de lógica mudou**: como a
MESA-CHEIA-12 já tinha unido lâmpada e rótulo na mesma função, trocar a fonte
do registro trocou os dois de uma vez (`coop.py:1222-1229` registra isso).

### E2 — por que uma fila NOVA, e não trocar a regra da que existe

O raciocínio abaixo é o que a entrega seguiu, e continua valendo como a razão
de o `rank` gravado não ter sido tocado.

Trocar `_assign_locked` para reordenar por conexão **reabre R-15 e R-23 inteiras**:
a cor automática, o LED do número, a reserva que os externos leem
(`_ds_reserve` em `external_identity.py`) e o `controllers.json` gravado saem
todos da mesma fila. Um replug no meio de uma partida renumeraria os quatro.

A saída barata é **não trocar o dono, e sim acrescentar um**: a ordem de
**conexão desta sessão** é um dado que o registro já tem à mão (é a ordem em que
`slot_for(assign=True)` marcou cada MAC como conectado — `identity.py:580-582`
alimenta `self._connected`, hoje um `set` **sem ordem**). Trocar esse `set` por
um dicionário ordenado custa quase nada e dá a fila do momento **sem tocar em
rank nenhum**.

A partir daí a escolha é uma linha só, e é a linha que ela decide na E1: qual
das duas filas alimenta `numeros_de_jogador()`.

### E3 — o gesto que já existe e que ela não alcança

`identity.renumber` (o `compact`) põe os **conectados** na frente da fila e
anexa os ausentes atrás (`identity.py:765-778`, `snapshot_connected`). É
exatamente a operação que ela descreveu, **feita à mão**. Hoje ela vive no IPC e
o único disparo citado no código é o encadeamento do modo jogo
(`app/actions/mode_transition.py:185`).

Se a resposta da E1 for *"automático não, mas eu quero poder"*, a E3 sozinha
resolve o caso dela — e é a entrega mais barata da sprint.

---

## 4. O teste que MORDE

**Escrito e na árvore:** `tests/unit/test_ordem_de_chegada_01_a_fila_do_momento.py`
— 644 linhas, 19 casos em 6 classes, entregue junto com a E2 no `86563c2`. As
três mordidas planejadas abaixo estão todas cobertas, e as classes dizem qual
é qual: `TestOCasoDela` (mordida 1), `TestQuemCaiEVolta` e
`TestOGravadoEDesempate` (mordida 2), `TestALampadaEORotuloSeguemJuntos`
(mordida 3). `TestCongelarEGravar` e `TestAMesaMistaContinuaFechando` cobrem o
congelamento e a mesa com externo, que a resposta dela acrescentou.

### Mordida 1 — a fila do momento não é a fila gravada (é a principal)

**Arrancar:** fazer `numeros_de_jogador()` continuar lendo o `rank` persistido.

**Por que reprova:** o dublê grava `controllers.json` com a fila `[A, B, C, D]`
e **conecta na ordem `[A, C, D, B]`** — a mesa dela desta madrugada, com os
endereços da faixa forjada. O teste exige que os números saiam `A=1, C=2, D=3,
B=4` pela ordem de conexão. Com a leitura do rank, saem `1, 2, 3, 4` na ordem
gravada, e o teste cai.

Esta é a principal porque é **o caso dela, sem tradução**: quatro controles,
resetados de fábrica, re-pareados numa ordem escolhida, e o número saindo de
outra.

### Mordida 2 — a fila persistida continua de pé para quem depende dela

**Arrancar:** fazer a fila de sessão **substituir** o `rank` (em vez de
conviver).

**Por que reprova:** o teste desliga e religa dois controles em ordem invertida
dentro da mesma sessão e exige que a **cor automática** e o piso que os externos
leem (`_ds_reserve`) NÃO troquem de dono — é literalmente o defeito que R-15
mediu e arrancou em 23/07, e ele não pode voltar de carona. Sem esta mordida a
E2 vira uma regressão de três semanas com nome novo.

### Mordida 3 — a lâmpada e o rótulo continuam sendo a mesma função

**Arrancar:** alimentar `numeros_de_jogador()` com a fila do momento e deixar o
escritor da lâmpada (`_numero_exibido`) na fila gravada.

**Por que reprova:** é a MESA-CHEIA-12 sendo desfeita pela porta dos fundos. O
teste é o que já existe —
`tests/unit/test_mesa_cheia_12_o_desenho_e_o_numero.py` — e ele lê o desenho de
volta do `/sys/class/leds` falso escrito pelo escritor de produção. Qualquer
entrega desta sprint que separe outra vez os dois espaços **reprova ali**, e é
por isso que aquele arquivo é a rede desta.

### O que estes testes NÃO provam

Que a ordem do momento é a resposta certa. Isso é dela, e é a seção 5.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | resposta dela, 15/08 |
|---|---|
| **A pergunta central: o número de jogador segue a ordem de conexão DESTA sessão, ou o lugar gravado do endereço?** O preço de cada lado está abaixo, e é real nos dois | **RESPONDIDA (D-30): a ordem do momento.** *"O gravado não some: vira desempate"* |
| **Se a resposta for "a ordem do momento": o que acontece com um replug no meio da partida?** Renumerar ali é o defeito que R-15 mediu; NÃO renumerar significa "ordem de conexão" com um asterisco | **RESPONDIDA (D-30): CONGELA quando a mesa estabiliza.** *"Quem cai e volta recupera o número"* — quatro segundos parados, e a ordem do momento é gravada |
| **O pedido C — "a nossa ordem deveria sobrescrever a parte da steam"** — é uma frente própria e não está medida nesta sessão (§6) | **em aberto** — medir antes de prometer |
| — | execução minha: as entregas, as mordidas, e a fila de sessão sem tocar em `rank` |

**O preço de cada lado, na mesa:**

- **ordem do momento** — ela conecta na ordem que quiser e os números saem
  daí. O custo: um controle que cai e volta no meio de uma partida pode virar
  outro jogador, que é a queixa *"nunca sei o que é o quê"* de 25/07; e a cor
  automática de cada controle muda junto, porque sai da mesma fila.
- **lugar gravado** (hoje) — os números nunca se mexem, nem por replug nem por
  reboot. O custo: é o que ela viu esta madrugada, e a única forma de mudar é
  o gesto explícito.

---

## 6. O que esta sprint NÃO mediu, e não finge ter medido

1. **O pedido C, sobre a Steam.** Ela citou o precedente da lightbar —
   *"igual quando descobrimos como fazer junto ao lightbar"*. Não medi nesta
   sessão se o número de jogador que a Steam atribui ao vpad obedece à nossa
   ordem, e **o espelho Xbox que o Steam Input faz de cada controle** é
   justamente onde essa disputa moraria. Fica como frente aberta, sem promessa.
2. **Se os quatro `rank` de hoje nasceram nesta sessão ou antes dela.** O
   `boot_id` do arquivo é o do boot corrente (a máquina subiu em 14/08 02:44) e
   o arquivo foi escrito às 01:15 de 15/08 — mas o `rank` de um MAC não muda ao
   ser reescrito. O que está provado é o **mecanismo**; a data de cada rank, não.
3. **O comportamento com externo na mesa** (Pro Controller, 8BitDo), **no
   aparelho**. A fila é global e compartilhada com eles
   (`external_identity.py`), e a E2 cobriu isso **em teste**
   (`TestAMesaMistaContinuaFechando`: a mesa mista continua fechando 1..N, e a
   permutação não vaza para o `present_ranks` que o lado externo lê). Contra um
   externo **ligado na bancada dela**, nada foi conferido.
