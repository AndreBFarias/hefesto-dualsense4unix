# NUM-01 — quem está na mesa é 1..N

- **Status:** ENTREGUE em 25/07/2026 pelo commit `a343ff6`
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
