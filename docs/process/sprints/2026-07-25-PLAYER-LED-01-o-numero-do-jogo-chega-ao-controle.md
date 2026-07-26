# PLAYER-LED-01 — o número do jogo chega ao controle

- **Status:** ENTREGUE em 25/07/2026 pelo commit `d1177c2` — com duas ressalvas
  medidas, na seção de fechamento
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026, depois da primeira partida com quatro controles

## O relato

> "o que tá estranho é que a numeração física dos controles, o reconhecimento nos
> jogos e na interface tão dessincronizados ou errados"

## O achado que reorienta tudo

**A intenção de projeto já é a correta, e está escrita.** A função que aplica o
número vindo do jogo declara em docstring:

> *"o número NO CONTROLE passa a ser o número que o JOGO atribuiu, não o dos
> nossos registros"*

O caminho existe, é o mesmo para o jogador 1 e para os do co-op, e a suspeita
inicial — de que o co-op reimporia o nosso número — foi **refutada lendo o
código**. Os dois caminhos repassam os bits do jogo literalmente.

**Não há escolha de projeto a fazer aqui. Há defeito a consertar.**

## O mecanismo

Quando o sinal de jogo classifica a autoridade de exibição como `daemon`, a
camada do jogo é **descartada do merge**, e o topo passa a ser a camada do co-op
— o nosso número. E não é omissão passiva: a retenção dispara uma **repintura
ativa**, que reescreve o nosso número por cima do que o jogo pediu.

O resultado é um **flip-flop**: sinal sobe, vale o número do jogo; sinal cai, a
repintura restaura o nosso. A medição ao vivo pegou a fase "nossa" — daí a
impressão de que o repasse nunca funciona.

## Os quatro defeitos, isolados

### 1. O aviso de retenção é global, não por controle
A trava que evita repetir o log é um campo único do backend. O primeiro controle
a ser retido silencia todos os outros — o endereço que aparece no journal **não é
o único afetado**, e foi exatamente isso que confundiu a leitura ao vivo.

### 2. O gate é inconsistente entre categorias
Gatilhos adaptativos **não passam** pelo gate e escrevem sempre. Luz e número
passam. Por isso o journal mostra gatilhos replicando no mesmo instante em que o
número era retido — duas rotas do mesmo subsistema discordando sobre "há jogo".

**Uma das duas está errada, e a sprint precisa decidir qual.** Se o gate protege
contra escrita indevida, o gatilho está desprotegido; se é excesso de zelo, luz e
número estão sendo bloqueados sem motivo.

### 3. `uhid_replica_ativa` é emitido antes do gate
"A réplica ativou" **não** significa "escreveu no controle". O evento sai no
momento em que o report do jogo é decodificado — bem antes de o backend decidir
se aplica. Um log que diz "ativa" quando nada chegou ao hardware é pior que log
nenhum, porque orienta a investigação para o lugar errado. *(Orientou a minha.)*

### 4. A repintura defende o número contra quem o escreveu
Defender a **cor** contra o cliente da Steam é legítimo e foi feito por um motivo
real. Defender o **número** contra o jogo que acabou de atribuí-lo contradiz a
docstring citada acima. São coisas diferentes e estão no mesmo caminho.

## Entregas

1. **Trava de log por controle**, não global.
2. **Unificar o gate entre categorias** — ou gatilhos também o respeitam, ou luz
   e número deixam de respeitá-lo. Duas rotas do mesmo subsistema não podem
   discordar sobre a existência de um jogo. Decidir com argumento escrito.
3. **A repintura para de tocar no número** quando existe camada de jogo retida
   para aquele controle. Cor continua defendida.
4. **Fechar o buraco do sinal de jogo** — a classificação exige evidência
   positiva (janela da Steam, regra de perfil, marcador do wrapper com processo
   vivo) e falha para jogo fora da Steam ou em janela nativa. Telemetria mínima:
   registrar a evidência **também quando não há transição**, para datar a queda
   seguinte em vez de descobri-la pelo sintoma.
5. **Diagnóstico honesto.** Um comando que mostre, por controle: nosso número ×
   camada do jogo × padrão aceso × número do kernel. Hoje é **impossível
   distinguir os quatro a olho** — ver a armadilha abaixo.

## A armadilha que esta sprint precisa documentar no código

**`/sys/class/leds` de um gamepad virtual não mostra o que o jogo escreveu.**

O jogo escreve o padrão como relatório HID de saída, interceptado em espaço de
usuário; nunca chega à classe de LED do kernel. O que o sysfs mostra é o número
que o **kernel** deu ao vpad no probe — por um contador que aloca o menor
identificador livre **contando físicos e virtuais juntos**.

E a tabela de padrões do kernel é **idêntica à nossa** em 1..4. Logo o padrão
aceso é ambíguo por construção: pode ser nosso, do kernel ou do jogo. **A única
testemunha do autor é o log.**

Isso custou uma conclusão errada durante a investigação e vai custar de novo se
não ficar escrito onde se lê o LED.

## Como validar

1. Abrir um jogo de co-op com quatro controles.
2. `journalctl … | grep -E "game_output_retido|uhid_replica_ativa"` → **nenhuma
   retenção** com o jogo em primeiro plano.
3. As luzes dos quatro controles batem com os números que o **jogo** mostra na
   tela.
4. Alt-tab e volta → os números **não piscam** nem trocam de dono.
5. Jogo fora da Steam → o sinal reconhece, e o número continua vindo do jogo.

**Critério que resume:** o número na luz, o número na tela do jogo e o número na
interface dizem a mesma coisa — e quando não puderem dizer, a interface admite
em vez de inventar.

## Fechamento (25/07/2026, commit `d1177c2`)

A decisão que a sprint exigia foi tomada: **o gate passou a ser por campo**. A
cor continua gateada (o gate nasceu de um incidente medido, e o dano ali é
persistente); o número saiu; os gatilhos passaram a consultar o mesmo ponto, em
vez de escrever sempre por omissão. O argumento está escrito no código, ao lado
da constante que define a política.

**Duas coisas que esta sprint pedia mudaram depois da medição, e ficam
registradas em vez de silenciadas:**

1. **A entrega 3, ao pé da letra, virou condição impossível.** Ela pedia que a
   repintura parasse de tocar no número *"quando existe camada de jogo retida"* —
   mas, com o número fora do gate, **não existe mais retenção de número**.
   Cumprir a letra exigiria manter o número gateado, que é exatamente a causa do
   flip-flop. Entregue a garantia mais forte: o número do jogo nunca sai do
   merge, e a repintura passou a **defendê-lo** contra escritor estrangeiro.
2. **O passo 2 do "Como validar" acima está desatualizado.** "Nenhuma retenção"
   não vale mais: retenção de `campos=['led']` continua possível e é **benigna** —
   é o gate fazendo o trabalho dele quando o sinal erra. O critério afiado é
   **retenção de `player_leds`**, que passou a ser impossível. E o par a procurar
   no journal é `uhid_replica_ativa` (o jogo pediu) + `game_output_aplicado` (o
   controle recebeu) — este segundo evento nasceu nesta sprint justamente porque
   o primeiro, sozinho, não testemunhava autoria nenhuma.

**Fica em aberto, declarado:** a primeira metade da entrega 4 — fechar o buraco
do sinal de jogo, que mora em `daemon/subsystems/game_signal.py`. Só a telemetria
foi entregue. O atenuante é medido: depois da decisão do gate, esse buraco
**deixou de custar o número** e afeta apenas a cor.

**Validação em hardware ainda pendente.** Nada aqui foi visto com quatro
controles e um jogo real — a prova são 15 mutações que derrubaram teste, e
mutação não substitui partida.
