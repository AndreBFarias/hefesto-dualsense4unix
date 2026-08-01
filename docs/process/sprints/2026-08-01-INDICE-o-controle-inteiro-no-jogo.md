# O controle inteiro no jogo — índice das sprints de 01/08/2026 (noite)

- **Escrito em:** 01/08/2026, sobre a `v0.7.0` publicada, na branch
  `restauro/inicio-da-sessao`
- **Por que este índice existe:** ela pediu, literal — *"primeiro eu quero que
  você planeje e materialize as sprints pra caso mesmo que nossa sessão caia,
  depois você vai saber o que fazer e somente executar ela sem precisar do
  mesmo tanto de contexto que você tem agora"*. **Este arquivo é o ponto de
  entrada.** Quem retomar o trabalho lê ele primeiro e não precisa de mais nada
  da conversa que o originou

## A pergunta que abriu tudo

Ela perguntou, olhando a aba Status:

> *"não sei se agora o alto-falante, giroscópio, microfone e touchpad — todas
> as features — na hora de jogar um jogo na Steam se elas vão estar
> funcionando. Elas precisam funcionar."*

E depois foi mais precisa:

> *"vamos pegar jogos da Sony: temos o áudio da tela, o giroscópio do controle
> nativo, o touch, o gatilho adaptativo, a possibilidade de usar o mic e temos
> o próprio som que sai adicionalmente no próprio controle (outro canal
> específico de som). O ponto é que isso precisa funcionar na parte da Sony e
> também deve funcionar quando eu opto pelo Hefesto na opção DualSense. É isso
> que queremos garantir. E naquela aba de Status podemos ver o funcionamento de
> tudo, e o funcionamento de lá obviamente impacta o funcionamento real do
> controle na hora de jogar."*

**Dois requisitos saem daí, e são o eixo destas sprints:**

1. **paridade** — tudo o que funciona em "Jogar direto (Sony)" tem de funcionar
   em "Jogar pelo Hefesto → DualSense";
2. **a aba Status é o painel da verdade** — o que ela mostra vale no jogo, e
   quando não vale, ela diz por quê.

## O que já foi medido (não repita este trabalho)

Auditoria de 01/08, com o daemon vivo e o DualSense no cabo. Cada linha tem
evidência no código, e as marcadas "medido" foram conferidas na máquina dela:

| recurso | Sony nativo | Hefesto → DualSense | Hefesto → Xbox 360 |
|---|---|---|---|
| vibração | nativo | **FUNCIONA** | funciona |
| lightbar | nativo | **FUNCIONA** (108 réplicas no journal) | — |
| player-LEDs | nativo | **FUNCIONA** (99 réplicas) | — |
| gatilho adaptativo | nativo | **FUNCIONA** (28+28 réplicas; o kernel não tem essa API, logo veio do jogo) | — |
| alto-falante (o canal do controle) | PipeWire | **FUNCIONA** (SOM-02/SOM-04) — não passa pelo gamepad | igual |
| áudio da tela | PipeWire | igual | igual |
| giroscópio | nativo | **provável** — dado byte-idêntico no vpad, e a SDL3 o enumera; falta aceite em jogo | **não existe na API** |
| acelerômetro | nativo | idem | **não existe na API** |
| touchpad (dedo + clique) | nativo | **não confirmado** — dado presente; ver JOGO-COMPLETO-01 | **não existe na API** |
| microfone | PipeWire | **USB sim** (mas MUDO nesta máquina agora); **BT em aberto** | igual |

> **Correção de 01/08, à noite.** Uma medição anterior deste índice concluiu que
> só a vibração chegava ao jogo. **Estava errada**: mediu a `libSDL2` 2.30.0 do
> Ubuntu, que nenhum jogo da Steam carrega. Refeito contra a SDL3 3.4.10 que a
> Steam distribui, o gamepad virtual **é enumerado por completo**
> (`054c:0df2 /dev/hidraw5`). O suporte a `uhid` entrou no `hidapi` em 2020 e o
> SDL3 herdou; o SDL2 clássico nunca sincronizou. **Todo instrumento desta leva
> tem de declarar contra qual biblioteca está medindo.**

**Os três modos existem e são escolha dela**, na aba Início e por perfil:
`Controlar o PC` / `Jogar pelo Hefesto` (com máscara DualSense ou Xbox 360) /
`Jogar direto (Sony)`. Em Sony nativo o backend entra em `_output_muted`
(`core/backend_pydualsense.py`) e o jogo escreve direto no hidraw; em Hefesto
→ DualSense o vpad uhid espelha entrada e replica saída.

**A única perda real é a máscara Xbox**, e ela é da API do controle de Xbox,
não do Hefesto: `integrations/virtual_pad.py` recusa o backend uhid para todo
sabor que não seja `dualsense`, e o vpad uinput declara 8 eixos e 11 botões —
não há onde pôr IMU nem dedo.

**A lacuna de paridade suspeitada — e NÃO medida:** os bytes de áudio do
report de saída não estão na lista de replicação do REPLICA-03. A frase que
estava aqui — *"um jogo que ajuste o volume escreve no vpad e o pedido morre
ali"* — **nunca foi medida**, e o mapeamento desses bytes é documentação de
comunidade, não fato: o kernel os declara `reserved`. Por isso a
PARIDADE-SONY-01 começa por um portão de medição, e pode terminar como
cicatriz.

## As cinco sprints, na ordem de execução

Cada uma é auto-suficiente. A ordem importa: a 1 é acabamento e não depende de
nada; a 2 e a 3-bis mexem no mesmo arquivo (`controller_card.py`) e é melhor
não cruzá-las; a 3 pode virar cicatriz no próprio portão; a 4 é independente.

**Se for executar uma só, execute a 3-bis** — ela carrega os dois interruptores
que ela mandou entrar no install, que é o furo mais concreto medido hoje.

### 1. [CARD-ÚNICO-01](2026-08-01-CARD-UNICO-01-o-estado-entra-no-card-e-o-l3-vira-marca-dagua.md) — o Estado entra no card

O frame "Estado" desaparece e o que sobra dele entra no card do controle; o
`· não ajustado` sai do título do alto-falante; L3 e R3 viram marca d'água no
centro do analógico.

**As cinco anotações do print dela**, e as duas escolhas que ela já fechou
(o desenho do card e o destino dos valores X/Y), estão no documento.

*Risco:* baixo. É layout. O único teste que não pode ser afrouxado é o teto de
altura do card (467px).

### 2. [PAINEL-DA-VERDADE-01](2026-08-01-PAINEL-DA-VERDADE-01-a-aba-status-diz-o-que-chega-ao-jogo.md) — a aba diz o que chega ao jogo

Cada recurso do card ganha um indicador de **estado real**: está chegando ao
jogo AGORA, sim ou não, e quando não, por quê (máscara Xbox, vpad degradado,
Steam Input assumindo, daemon parado).

É o requisito 2 dela, e o mais valioso dos quatro: hoje a aba mostra que o
sensor EXISTE, não que ele CHEGA.

*Risco:* médio. Mexe no `state_full` (contrato de IPC) e no card.

### 3. [PARIDADE-SONY-01](2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md) — o volume do jogo chega ao alto-falante

Fecha a lacuna de paridade: os bytes de áudio do vpad passam a ser replicados
no controle físico, como já são o gatilho, a lightbar e os player-LEDs.

*Risco:* médio-alto. Há uma regra de POSSE do volume que esta casa já pagou
para manter (o daemon assumir o registrador faz o botão físico parar de valer),
e a sprint tem de conviver com ela.

### 3-bis. [JOGO-COMPLETO-01](2026-08-01-JOGO-COMPLETO-01-os-nove-recursos-dentro-do-jogo.md) — os nove recursos no jogo

Pedido dela: *"vai materializando os outros tópicos pra ir colocando e
adicionando eles ao modo jogo, tipo aqueles 7 mais mic e speaker"*. A matriz
dos nove recursos, o que já funciona, o que falta confirmar, e **os dois
interruptores que ela mandou entrar no install sem flag** (o broker
`hide-hidraw` e o wrapper — hoje todo jogo enxerga dois DualSense).

*Risco:* médio. A E4 mexe no install, e a ordem importa (wrapper antes do
broker).

### 4. [ESCOLHA-DELA-VENCE-01](2026-08-01-ESCOLHA-DELA-VENCE-01-a-mascara-do-perfil-e-o-tooltip-do-xbox.md) — a escolha do perfil prevalece

Ela disse: *"o que eu quero é que minha escolha aqui prevaleça sempre. E ao
deixar o mouse sobre a opção Xbox, ele falaria que o Xbox não tem tais
features. Mas em todos eu poderia escolher Hefesto ou Sony pra usar e tirar
proveito de tudo."*

Duas coisas: a máscara escolhida no perfil não pode ser sobrescrita por
ninguém, e o botão Xbox do editor de perfis ganha o tooltip que a aba Início já
tem.

*Risco:* médio. Esta casa tem histórico registrado de *"a config que eu deixo
nunca é respeitada"* — três escritores do perfil sem dono. A sprint começa por
mapear a precedência real.

## O que NÃO entra em nenhuma delas

- **Trocar os seis perfis dela para máscara DualSense.** Ela respondeu que a
  escolha é dela e tem de prevalecer — a entrega é o tooltip e a precedência,
  não a troca.
- **O aceite em jogo real.** Nenhuma destas sprints fecha sem ela abrir um jogo
  e usar. O que se pode automatizar é o dado chegar ao vpad; que o JOGO o
  consuma é medição de fora.

## O que fica para ela decidir, e está esperando

- **A rota de som está LIGADA** hoje: o `Default Sink` do sistema é o
  alto-falante do controle, a 40%, com o HDMI guardado como anterior em
  `gui_preferences.json`. Se o som do jogo deveria sair na TV, o botão que
  agora vive no bloco Alto-falante do card desfaz.
- **Os seis perfis com máscara Xbox** (`acao`, `aventura`, `corrida`,
  `esportes`, `fps`, `coop_local`): continuam como estão, por decisão dela.

## Como retomar do zero

1. leia este índice;
2. leia a sprint que for executar — ela tem os caminhos, os testes que vão
   reprovar e as armadilhas nomeadas;
3. rode `pytest tests/unit -k "status or card or largura or layout or som"`
   para ter a linha de base (hoje: 550 verdes; a suíte inteira: 6645);
4. as bancadas de medição estão em `scripts/gui-captura/`;
5. a regra de aceite de interface é a
   [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
   foto antes e depois, e o olho dela no fim.
