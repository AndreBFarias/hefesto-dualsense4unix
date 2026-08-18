# QUATRO-NA-MESA-01 — o que só quebra quando são quatro

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** MÉDIA-ALTA — nenhum destes derruba a partida sozinho, e os
  quatro juntos são a sensação de *"a janela pisca e os controles trocam de cor
  sozinhos"*
- **Faixa:** 2 — o produto se contradiz
- **Causa-raiz:** 2 **PROVADOS no código**, 2 **CORRIDAS com janela
  identificada**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Irmã da:** [POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md)
  — aquela é a **posse** de output; esta é a **identidade e o relógio**


> ### **MEDIÇÃO DELA** — os quatro na mesa, com jogo aberto.
>
> Os quatro já conectaram (03/08), mas **nenhum jogo foi aberto** — e é dentro do jogo que a numeração e os recursos importam. Item 4 do protocolo.

---

## O que os quatro têm em comum

São estruturas **de um controle só** que sobreviveram à chegada do quarto. Cada
uma funciona; nenhuma foi pensada para conviver com as outras três **enquanto um
controle pisca no Bluetooth**.

---

## Defeito 1 — `_connected` tem dois escritores em cadências diferentes

**CORRIDA COM JANELA IDENTIFICADA.**

- **escritor A — o tick lento SUBSTITUI o conjunto:**
  `daemon/subsystems/identity.py:729-730` (`self._connected = vistos`),
  alimentado por `daemon/lifecycle.py:2951-2960` **a cada 2,0 s**, filtrando por
  `info.get("connected")`;
- **escritor B — a leitura de cor ADICIONA:**
  `daemon/subsystems/identity.py:581-583` (`slot_for(..., assign=True)` faz
  `self._connected.add(key)`), chamado pelo provider automático (`:1016`) dentro
  de `_merged_desired_for_key` (`core/backend_pydualsense.py:1222-1224`), que
  `resolved_led_for` (`:3160-3161`) chama **a partir da aba Status, a 10 Hz** —
  e `daemon/ipc_handlers.py:2243` diz por extenso *"o `state_full` roda a 10 Hz"*.

**O fato que fecha o argumento:** `mark_disconnected`
(`identity.py:666`) **não tem chamador de produção** — medido em 03/08: só
`tests/unit/test_identity_registry.py` e `test_auto_player_colors.py`. **A única
remoção possível é a substituição de 2 s.**

### A janela é exatamente a de um controle que piscou no Bluetooth

Enquanto o nó de sysfs dele some (o `get_rgb()` devolve `None`), o
`_lightbar_for_uniq` cai no ramo `resolved_led_for`
(`daemon/ipc_handlers.py:2228-2233`) e **o re-marca como presente 10× por
segundo**; 2 s depois o `sync_connected` o tira; e assim por diante, até o
`connect()` reapear o handle (≤30 s).

E o **número exibido** sai de `_posicao_locked`, que **conta `_connected`**
(`identity.py:658-662`).

**O que ela veria:** *"com a janela do Hefesto aberta, quando um controle pisca
os outros trocam de cor e de número sozinhos, e voltam"*. Cada `reassert` que
caia dentro dessa janela pinta o valor errado **no hardware**.

**Por que já funcionava:** com a janela fechada não há 10 Hz; no cabo o nó não
some; com um ou dois controles a mudança de contagem é invisível.

### A cura, e o que NÃO é

**A cura não é "chamar `mark_disconnected`".** Ele estar sem chamador é
**intencional**: o lugar na fila **deve** sobreviver ao disconnect (`D2`/`R-15`,
`identity.py:666-684`) — é o que faz o replug recuperar o número.

**O defeito é `_connected` ser escrito por uma LEITURA.** Uma consulta de cor
não pode ter efeito colateral sobre quem está na mesa. O `assign=True` do
provider automático precisa deixar de marcar presença — quem sabe quem está
conectado é o tick, e só ele.

**Aceite:** com a aba Status aberta e um controle ausente, `slot_for` do provider
não muda `_connected`. **A mordida:** `sync_connected` (2 s) e uma tempestade de
`state_full` (10 Hz) em threads concorrentes, com um controle marcado
`connected: False` — asserção de que o slot de cada MAC vivo é **estável**.

---

## Defeito 2 — dois espaços de numeração pintam a barra de jogador, e só um desempata

**CORRIDA COM JANELA IDENTIFICADA.**

- **o co-op desempata:** `daemon/subsystems/coop.py:999-1001` usa
  `_numero_exibido`, que garante unicidade em `:1054-1057`
  (`while numero in usados: numero += 1`);
- **a camada automática NÃO desempata:**
  `daemon/subsystems/identity.py:1026-1027`
  (`campos["player_leds"] = player_led_pattern(slot)`), com `slot` vindo direto
  de `_posicao_locked` (`:646-664`) — **sem nenhuma proteção contra empate**.

**As duas janelas:** os ~2 s após um replug, em que dois MACs ainda não entraram
em `_connected` e calculam a mesma colocação (é o defeito 1 alimentando este); e
sempre que a camada do co-op é revogada por `not self._players`
(`coop.py:978-985`), deixando a automática pintar sozinha.

**O que ela veria:** *"dois controles acesos como jogador 2 ao mesmo tempo"* — a
queixa histórica desta casa, **por um caminho diferente do que o `R-24` curou**.

**Aceite:** nenhum instante tem dois MACs com o mesmo padrão de player-LED
resolvido. É uma das asserções da bancada dos quatro controles (ver
[COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md#e4--o-teste-que-morde-a-bancada-dos-quatro-controles-com-queda-programável)).

---

## Defeito 3 — a autoridade do jogo é UMA para os quatro

**CORRIDA COM JANELA IDENTIFICADA.**

- **a camada GAME é por-uniq:** `core/backend_pydualsense.py:894`
  (`_game_output_by_uniq`), escrita por `set_game_output_for` (`:2984-2996`);
- **o portão é global:** `_game_wins()` (`:1171-1187`) consulta um provider
  **sem parâmetro**, alimentado pelo sinal único de janela
  (`daemon/lifecycle.py:3311-3348`);
- **e a defesa de exibição tem UM relógio para os quatro:** `_defend_last_at`
  (`:921`) com teto de 30 s (`DEFEND_DISPLAY_MIN_INTERVAL_S`, `:84`).

**A janela:** ~2 s de latência do sinal (`lifecycle.py:3411-3413`). Nesse
período, a réplica de qualquer um dos quatro é retida ou aplicada **em bloco**.

**O que ela veria:** *"o jogo pintou a cor certa em um controle e nos outros três
não"* — a primeira defesa consumiu a cota de 30 s dos demais.

**A cura mínima e honesta:** o teto de 30 s passa a ser **por controle**, não
global. O portão `_game_wins` continuar global é defensável (o jogo em foco é um
só); o **relógio compartilhado** não é.

**Aceite:** quatro réplicas de jogo no mesmo tick chegam aos quatro controles.

**Armadilha nomeada:** o `DEFEND_DISPLAY_MIN_INTERVAL_S` existe porque o reassert
incondicional causou o **flash azul de 30 s** (`GUERRA-01`). Tornar o teto por
controle **não** pode virar "tirar o teto".

---

## Defeito 4 — o cache anti-guerra do sysfs é jogado fora a cada reconciliação

**PROVADO no código** (a cura está morta); **ESPECULAÇÃO** quanto ao sintoma
percebido — e a sprint diz qual, para não se inventar impacto.

- **o cache vive na INSTÂNCIA do nó:** `core/sysfs_leds.py:64`
  (`self._last_write`), consultado em `:183`. É a cura do `GUERRA-01` item 3,
  documentada em `:58-63`;
- **o mapa é reconstruído com instâncias NOVAS:** `core/sysfs_leds.py:314` —
  `discover()` **sempre fabrica objetos novos** — e
  `core/backend_pydualsense.py:1834` troca o mapa inteiro. **O objeto que tinha
  o cache e o objeto que é lido nunca são o mesmo.**

Isto já está registrado na
[LIGHTBAR-BT-CLAIM-01](2026-08-02-LIGHTBAR-BT-CLAIM-01-a-barra-apagada-com-o-sysfs-certo.md#1-por-que-o-skip_cache-saiu-37-ms-depois-do-reset-se-o-reset-03-existe-para-invalidar-o-cache),
como efeito colateral: *"como as instâncias são refeitas a cada tick, o cache do
`GUERRA-01` nunca sobrevive entre reconciliações"*. **Esta sprint o promove de
nota de rodapé a item**, porque com quatro controles o custo escala.

**O custo:** ~28 escritas de sysfs por reconciliação (4 × RGB + 5 player-LED
cada), a cada ≤30 s, cada uma virando output report no link BT — **que é o
gargalo já medido** (`BUG-MULTI-CONTROLLER-BT-CRC-CONTENTION-01`,
`core/backend_pydualsense.py:203-215`).

### A predição falsificável, e ela é o que torna este item executável

> O log `lightbar_reassert_skip_cache` (`core/sysfs_leds.py:197-201`)
> praticamente **nunca** deve aparecer no journal para um nó que **não** é novo.
> **Se aparecer, esta leitura está errada.**

E a medição de 03/08 no journal dela é coerente: **8 ocorrências** de
`lightbar_reassert_skip_cache` em duas horas e meia — todas coladas em
coberturas de sysfs, nenhuma em regime.

**A armadilha, escrita para quem for consertar:** fazer a instância sobreviver
entre ticks (o conserto "óbvio") **pararia a reescrita de 30 s que hoje existe
por acidente** — e é justamente ela que permitiu refutar a hipótese de perda de
pacote na `LIGHTBAR-BT-CLAIM-01`. **É uma regressão silenciosa.** A cura tem de
preservar a reescrita periódica **e** parar de reescrever o que não mudou dentro
do mesmo passe.

**Aceite:** `connect()` chamado 10 vezes seguidas, sem nada mudar, produz **zero**
escritas de sysfs depois da primeira convergência — e a reescrita periódica
continua acontecendo. **A bancada:** um `SysfsLedNode` instrumentado contando
`open(..., "w")` por atributo, atravessando o `_refresh_sysfs_leds` (o teste de
hoje mede a instância **isolada**, e é por isso que não pegou).

---

## Testes que vão reprovar

```
pytest tests/unit tests/core -k "identity or player_led or sysfs or defend or game_output or auto_player"
```

## O que NÃO fazer

- **Não chamar `mark_disconnected` para "consertar" o defeito 1.** Ele está sem
  chamador **de propósito** — o lugar na fila sobrevive ao disconnect (`R-15`);
- **Não tirar o teto de 30 s da defesa de exibição** (defeito 3) — ele paga o
  flash azul do `GUERRA-01`. Torná-lo por controle **não** é tirá-lo;
- **Não fazer a instância do `SysfsLedNode` sobreviver entre ticks** sem
  preservar a reescrita periódica (defeito 4). É a regressão silenciosa nomeada
  acima;
- **Não mexer no desempate do co-op** (defeito 2) para "unificar" com a camada
  automática. O co-op está **certo**; quem falta desempatar é a automática.

## O que fica ABERTO

- **o sintoma real do defeito 4** — a predição falsificável está escrita; quem
  executar deve **medi-la antes** de mexer;
- **se o defeito 2 já se manifestou** — a queixa "dois no jogador 2" tem
  histórico nesta casa por outro caminho, e não há como distinguir os dois no
  journal de hoje.

---

## MEDIDO ao vivo em 04/08/2026, 02:49 — a colisão de Jogador 1

Os quatro no rádio ao mesmo tempo, conectados e estáveis (foto da tela dela).
A numeração que ela leu **nos controles**:

| controle | jogador |
|---|---|
| 8BitDo | **1** |
| Pro Controller | 3 |
| DualSense roxo (BT) | 2 |
| DualSense branco | **1** |

**Dois controles como Jogador 1**, e o 2 e o 3 ocupados — ou seja, não é "o
quarto não recebeu número", é **colisão** com o 4 livre.

### O que o sysfs dizia no mesmo instante, e por que ele NÃO decide

    0005:057E:2009.0037: player-1, player-2, player-3 ACESOS   (o Pro)
    input443:            player-1..player-5, os CINCO acesos
    input437:            player-2 e player-4 acesos
    input276, input440:  player-3

Três leituras diferentes, e nenhuma casa direto com o que ela vê. As razões já
estão medidas nesta casa e **precisam ser honradas por quem executar esta
sprint**:

1. **`/sys/class/leds` mostra o número do KERNEL, não o nosso** (medido em
   25/07) — ele não é instrumento para conferir a numeração do produto;
2. **o Pro acende TRÊS LEDs para dizer "Jogador 3"** — a convenção Nintendo é
   contar LEDs acesos, não acender o enésimo. A leitura dela (Jogador 3) está
   certa e o sysfs também; quem confunde é quem lê um pelo outro;
3. **o DualSense usa o padrão PS5** (medido em 22/07: *"player LEDs = padrão
   PS5, não bug"*), em que o conjunto aceso codifica o jogador.

**Consequência para a sprint:** o aceite não pode ser escrito contra o sysfs.
Tem de ser contra o que o daemon AFIRMA (o `player_slot` por controle) e contra
o que ela VÊ — e os dois têm de bater. Um teste que leia o sysfs vai passar com
a colisão de pé.

### O que ainda falta, e é dela

Isto foi medido **fora de jogo**. A parte que decide — se a numeração muda
sozinha durante a partida, e se o jogo enxerga os quatro — continua no item 4
do [protocolo](../estudos/2026-08-03-PROTOCOLO-as-medicoes-que-decidem-a-leva.md).
