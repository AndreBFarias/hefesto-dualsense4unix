# NUM-01 — quem está na mesa é 1..N

- **Status:** **ENTREGUE.** Conferido no código em 07/08/2026 — as cinco
  entregas, uma a uma, com `caminho:linha`, na nota datada no fim deste arquivo
- **Status anterior:** ABERTA (assim desde 25/07/2026). O rótulo não se apaga:
  ele é o próprio assunto da nota datada — sprint marcada como aberta é lida
  como dependência viva, e isso já custou uma sprint travada
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026

## O relato

> "ao usar o branco ele sempre liga no player 2 setado, ao invés de ligar pela
> ordem correta — se ele conectou primeiro deveria ser o player 1."

## O que foi medido

`~/.config/hefesto-dualsense4unix/controllers.json`, com **um só** controle
ligado:

```json
{"version": 2, "slots": {"a0fa9c000001": 1, "143a9a000002": 2},
 "externals": {"e0f6b5000003": 3, "e417d8000004": 4}}
```

O controle conectado era o `143a…`, sozinho na mesa, e recebeu o número 2 —
porque o número 1 estava **reservado a um endereço que não estava ligado**.

Horas depois, no mesmo dia, o arquivo apareceu **invertido**:

```json
{"slots": {"a0fa9c000001": 2, "143a9a000002": 1}}
```

A inversão aconteceu dentro de uma única sessão do daemon. Ela tem uma causa
exata, e é o gesto que a própria interface oferece como conserto.

## As três engrenagens

### 1. A reserva é permanente, por decisão

`daemon/subsystems/identity.py:445` — `mark_disconnected` só remove a chave do
conjunto de conectados; **o slot continua preso ao endereço**. A docstring diz:

> *"a reserva vale pelo BOOT inteiro — nada aqui (nem no `sync_connected`) expira
> slot por sessão esvaziada, então flap de BT, suspend e 'desliguei os dois
> controles pra jantar' devolvem o MESMO número a cada endereço."*

### 2. Nada reivindica um número vago

`_assign_locked` (`identity.py:413`) só age sobre chave **ausente** do mapa. Uma
chave que já existe nunca é reavaliada. Logo, número 1 vago fica vago.

### 3. O gesto de conserto rebaixa quem está ausente

O único caminho que reordena é `compact()` (`identity.py:543`), chamado só pelo
botão **"Renumerar agora"** via `identity.renumber` (`daemon/ipc_handlers.py:794`).
O plano ordena por `(está offline?, slot)` — os conectados descem para 1..N e
**quem estiver desligado na hora é empurrado para trás**.

Simulando com o estado medido (só `143a…` presente):

| chave | ausente? | antes | depois |
|---|---|---|---|
| `143a9a000002` | não | 2 | **1** |
| `a0fa9c000001` | **sim** | 1 | **2** |

Reproduz o arquivo em disco byte a byte. **O gesto que conserta um controle
estraga o outro** — e o estrago é permanente por causa das engrenagens 1 e 2.

## A tensão real, e por que ela não é um erro

A reserva permanente foi introduzida em 23/07 para curar um defeito oposto e
igualmente legítimo — registrado em `identity.py:469`:

> *"Com os dois DualSense desligados, o primeiro a acordar levava o slot 1 — cor
> e número trocavam de dono."*

São **dois requisitos verdadeiros ao mesmo tempo**:

- **Estabilidade** — com os dois na mesa, cada um mantém seu número entre
  sessões. Cor e posição não trocam de dono.
- **Naturalidade** — sozinho na mesa, o controle é o jogador 1. Ninguém aceita
  ser o jogador 2 de si mesmo.

A implementação atual escolheu estabilidade e pagou naturalidade. A anterior fez
o inverso. **Nenhuma das duas está errada — o erro é ter que escolher.**

## O conserto: separar "quem é você" de "que número você ocupa"

A saída é distinguir dois conceitos que hoje são o mesmo inteiro:

- **Identidade** — o endereço do aparelho. Permanente, é o que carrega
  preferências por controle.
- **Posição na mesa** — 1..N entre **quem está presente agora**. Derivada, nunca
  persistida como número absoluto.

O que se persiste deixa de ser "este endereço é o 2" e passa a ser uma **ordem
de preferência**: uma lista onde o endereço A vem antes do endereço B. A posição
exibida é a colocação dentro dessa ordem, **contando só os presentes**.

Os dois requisitos passam a valer juntos:

| situação | ordem persistida | quem está na mesa | números |
|---|---|---|---|
| os dois ligados | `[A, B]` | A, B | A=1, B=2  estável |
| só B ligado | `[A, B]` | B | **B=1**  natural |
| os dois de volta | `[A, B]` | A, B | A=1, B=2  voltou ao lugar |

O `controllers.json` ganha versão de esquema nova (o campo `slots` vira uma
lista ordenada), e o carregador já sabe descartar esquema antigo uma vez —
`CONTROLLERS_SCHEMA_VERSION` existe exatamente para isso.

## Entregas

1. **Ordem de preferência no lugar do número absoluto.** Esquema novo em
   `identity.py`, com bump de `CONTROLLERS_SCHEMA_VERSION`, e a posição exibida
   calculada sobre os presentes.
2. **"Renumerar agora" muda de significado.** Deixa de reescrever números
   absolutos e passa a reordenar a preferência dos **presentes** — sem tocar em
   quem está ausente. O botão para de ter efeito colateral.
3. **Compactação automática.** Quando um controle sai e deixa um número menor
   vago, os presentes fecham a lacuna. É o que ela espera e o que a ordem de
   preferência entrega de graça.
4. **Espaço único com os externos.** O registro dos externos
   (`external_identity.py`) compartilha o arquivo e o mesmo espaço de numeração;
   a ordem precisa ser única entre os dois, não duas listas paralelas.
5. **Corrigir a documentação interna.** A docstring de `_renumber_locked`
   (`ipc_handlers.py:609`) afirma que *"nenhum outro caminho toma os dois locks
   ao mesmo tempo"* — isso deixou de ser verdade quando o provider de reserva foi
   introduzido. Invariante documentada e morta é pior que invariante ausente.

## Corridas que agravam, e entram junto

A auditoria de concorrência encontrou três janelas que produzem a **primeira**
atribuição errada — que a persistência depois congela:

- **RACE-PLAYER-01** — o laço de leitura começa antes de `connect()` terminar
  (`lifecycle.py:541` × `:601`). Na primeira janela não há controle nenhum
  descrito, o piso de reserva vale zero, e um controle externo leva o número 1
  antes de qualquer DualSense existir. É o "não existe Controle 1".
- **RACE-PLAYER-02** — a ordem de enumeração não é a ordem de conexão. Um
  controle no cabo aparece sob `/sys/devices/pci…` e um por rádio sob
  `/sys/devices/virtual/…`; a ordenação alfabética põe o cabo antes, **mesmo que
  ele tenha conectado depois**.
- **RACE-COOP-LED-02** — nos primeiros segundos, o número exibido pelo co-op usa
  um palpite (`coop.py:1051`) e depois muda quando o registro atribui de verdade.
  É o número que pisca.

Corrigir só as corridas **não resolve o relato dela**: o número errado já está
gravado. Corrigir só a persistência deixa a atribuição inicial ao acaso. **As
duas metades são a mesma sprint.**

## Como validar

1. Ligar só o controle B. Deve ser **jogador 1**.
2. Ligar o A também. B continua 1, A vira 2 — **ninguém pisca**.
3. Desligar o B. A deve virar **jogador 1**.
4. Religar o B. Volta a ordem original: A=1, B=2.
5. Reiniciar o daemon com os dois ligados: a ordem se mantém.
6. Reiniciar a máquina: a ordem se mantém.

O critério que resume tudo: **nunca deve existir um jogador 2 sem jogador 1**.

---

## NOTA DATADA — 07/08/2026: esta sprint está ENTREGUE, e o "ABERTA" caducou

**Nada acima foi apagado.** O relato dela, o `controllers.json` medido, as três
engrenagens, a tabela da inversão e o desenho do conserto ficam inteiros: foi
esse material que produziu o código de hoje, e é por ele que se entende por que
o código é assim. O que caducou é **uma linha** — o `Status: ABERTA` do
cabeçalho, corrigido ali em cima com o rótulo anterior preservado.

### Por que uma linha de cabeçalho merece nota datada — GRAU: MEDIDO

Rótulo de sprint **é lido como dependência**. A
[MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md)
ficou parada com a justificativa escrita *"IDENT-01 é pré-requisito duro"* na
seção "Dependências" — e a nota datada de 07/08 daquela sprint mediu que o
pré-requisito **já estava superado**: a identidade estável de externo existe e
é fonte única — `identity_for_entry` (`external_identity.py:310-313`, *"FONTE
ÚNICA da string com que este projeto numera um controle externo"*), persistível
quando é MAC de hardware, e MAC de hardware nunca é podado
(`_prune_volatile_locked`). Ninguém tinha percebido, porque a
leitura parava no rótulo. **Sprint marcada como aberta bloqueia leitura de
dependência** — e o custo não é uma linha, é uma sprint parada.

### As cinco entregas, conferidas uma a uma em 07/08

| entrega | onde está, conferido |
|---|---|
| **1.** Ordem de preferência no lugar do número absoluto | `identity.py:189-194` — `CONTROLLERS_SCHEMA_VERSION = 3`, com o porquê do bump escrito na constante; `:196-201` — `ORDER_FIELD = "order"`, e os campos `slots`/`externals` do schema 2 *"não são mais lidos nem escritos"*; `:279-313` — `order_entries`, fonte única de leitura da fila; `:646-664` — `_posicao_locked`, a posição exibida calculada sobre os presentes |
| **2.** "Renumerar agora" muda de significado | `ipc_handlers.py:1288-1297` — *"o plano ordena e reescreve LUGARES NA FILA, não números de jogador. A consequência é que o item 1 deixou de ter efeito colateral"*; `identity.py:812-814` — `compact` grava lugar, não número exibido |
| **3.** Compactação automática | `identity.py:691-693` — *"a compactação automática não é um passo, é consequência de contar só os presentes"*; `identity.py:666-678` — `mark_disconnected` guarda o LUGAR, não o número |
| **4.** Espaço único com os externos | `identity.py:104-110` — uma fila só, com `kind` dizendo de quem é cada entrada; `external_identity.py:28-38` — o número exibido deixou de ser o lugar, e a parte DualSense da contagem chega por provider; `:452-462` e `identity.py:750-763` — os dois `present_ranks`, um espelho do outro |
| **5.** Corrigir a documentação interna | a frase morta *"nenhum outro caminho toma os dois locks ao mesmo tempo"* **não existe mais na árvore**: em 07/08 o `grep` por ela em `src/` devolve zero, e as únicas ocorrências no repositório são a citação da entrega 5 aqui em cima e esta linha. No lugar dela há hierarquia de locks escrita — `identity.py:125`, `external_identity.py:36-38` e `:467-471` (*"NUNCA chamar com `self._lock` tomado"*, com o ciclo que isso fecharia nomeado) |

Os **oito** pontos em que o código se declara NUM-01, todos abertos e lidos
neste dia: `external_identity.py:28` (o número exibido deixou de ser o lugar),
`:234` (`_present_ranks_of`, com a ordem de degradação quando o outro registro
é antigo), `:393` (o mapa guarda LUGAR, não número), `:452` (`present_ranks`),
`:465` (`_ds_present_ranks`, com a regra de lock) e `:518` (`slot_for` devolve
colocação entre os presentes); `identity.py:279` (`order_entries`) e `:316`
(`merged_order_payload`).

### A prova, e onde ela morde

`tests/unit/test_num01_quem_esta_na_mesa.py` — **15 testes, verdes em 07/08**
(`0,22 s`, sem aparelho, sem GTK). Os seis cenários da seção "Como validar"
desta sprint estão lá **um por um e na ordem**
(`test_1_o_controle_sozinho_na_mesa_e_o_jogador_1` até
`test_6_reboot_da_maquina_mantem_a_ordem`), mais três classes que amarram o
resto: `TestNuncaJogador2SemJogador1` (o critério que resume tudo),
`TestRenumerarAgoraNaoEstragaOAusente` (o defeito exato da tabela da inversão) e
`TestMigracaoDoArquivoReal` (o arquivo schema 2 dela descartado uma vez).

**A mordida desta nota não é em código** — nota datada não muda comportamento, e
`src/` não foi tocado. Ela é dupla, e as duas metades rodaram em 07/08:

- **no produto**, na nota da MÁSCARA-01 do mesmo dia: o alvo do rumble arrancado
  e devolvido, com a mesa inteira vibrando de um lado e um controle só do outro;
- **nos portões que guardam este arquivo**, um a um, com o defeito injetado em
  cópia e o gate conferido depois de curado: `validar-acentuacao.py` reprovou
  `decisao` sem til (saída 1), `validar-glifos.py` reprovou U+1F600 (saída 1) e
  `validar-referencias-docs.py` reprovou um link para arquivo inexistente
  (saída 1) — os três voltaram a 0 com o defeito removido. Portão que não morde
  não guarda nota nenhuma.

### O que esta nota NÃO afirma

A seção "Corridas que agravam" nomeia três. **Só duas foram conferidas hoje:**

- **RACE-PLAYER-01** (*"não existe Controle 1"*) — curada, e a cura está
  descrita no próprio módulo: `identity.py:35-43` (R-24) tirou a atribuição do
  caminho lazy e a pôs no `sync_connected`, que roda **antes** do tick dos
  externos, *"quem está na mesa ocupa 1..N antes de qualquer externo pedir
  número"*. GRAU: MEDIDO (leitura do código; o experimento com os quatro na
  mesa é da CHECKLIST de hardware, não desta nota).
- **RACE-COOP-LED-02** (*"o número que pisca"*) — a lâmpada do co-op deixou de
  usar palpite: `coop.py:1044-1058` consulta `slot_for(..., assign=False)` do
  registro e só cai no `player_index` do co-op quando não há registro
  (`FakeController`, dublê, backend legado). GRAU: MEDIDO no código; que o
  piscar tenha morrido AO VIVO é SEM PROVA — ninguém cronometrou o primeiro
  segundo hoje.
- **RACE-PLAYER-02** (a ordem de enumeração não é a ordem de conexão) — **não
  conferida**. GRAU: SEM PROVA nos dois sentidos. Quem for atrás dela não deve
  ler esta nota como "resolvida"; o identificador não aparece em `src/`.

Nenhuma das três é condição para o `Status` mudar: o relato que abriu a sprint
(*"ele sempre liga no player 2"*) é o que os seis cenários do teste cobrem.
