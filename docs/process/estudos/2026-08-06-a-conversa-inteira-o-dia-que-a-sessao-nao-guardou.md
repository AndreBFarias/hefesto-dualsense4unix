# A conversa inteira — o dia que a sessão não guardou

**Escrito em 06/08/2026**, a pedido dela, depois de a sessão de trabalho ser
morta por `SIGKILL` às 22h20:

> *"faz tudo que for necessário pra não perdermos nada, materializa estudos dos
> agentes no projeto, materializa o contexto todo da conversa"*

Este documento é o **contexto**, não o resultado. O resultado está nas sprints e
no [índice do dia](../sprints/2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md).
Aqui fica o que **não cabe** numa sprint: a ordem em que as coisas foram
descobertas, o que ela pediu e como, e as vezes em que uma conclusão foi
derrubada — que é o que se perde primeiro quando a sessão morre.

**Grau de cada afirmação:** **MEDIDO** = há registro no transcrito, no journal
ou no `git log`; **SUSPEITA COM MECANISMO** = o caminho foi lido, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou. As falas dela são
**citação literal do transcrito** — grau MEDIDO por construção.

---

## 1. Os números do dia

**Grau: MEDIDO**, contados dos arquivos em disco.

| | |
|---|---|
| janela | 05/08 23h11 até 06/08 22h20 |
| mensagens dela | **51** |
| subagentes diretos | **43** (26 nesta sessão, 17 na anterior) |
| workflows | **10**, todos `completed` |
| agentes dentro dos workflows | **73** |
| **agentes no total** | **116** |
| custo somado | **9,7 milhões de tokens** |
| commits | **6** |
| suíte ao fim | **7251 verdes**, 1 pulado |

O maior workflow sozinho (`perfil-por-jogo-e-cura-do-bt`) usou **20 agentes** e
**2,19 milhões de tokens** em 80 minutos.

---

## 2. Como o dia começou: a pergunta que a resposta era "não"

A primeira mensagem dela, às 23h11 de 05/08:

> *"Estude o projeto. Hoje de madrugada e pela manhã fizemos várias pesquisas
> com os agentes, tudo foi salvo?"*

**A resposta era não.** Havia cerca de 7 mil linhas no índice do git, sem um
único commit — a leva inteira dos perfis, a um `git reset --hard` de deixar de
existir. Ela descobriu isso **por perguntar**, não por um alarme.

Foi ela também quem reconstituiu o próprio pedido perdido, colando o que o
histórico guardava:

> *"na real, pulamos tudo, estuda o sistema de perfis, os botões relacionados
> aos perfis e as prioridades deles. lança agentes. estão completamente
> quebrados agora. isso acima foi o que o histórico do chat tinha de lembrança
> dos meus inputs."*

**A lição, que virou regra:** um `git status` com tudo em `A `/`M ` **parece**
trabalho salvo. Não é — é o índice, não a história.

---

## 3. As três vezes em que ela derrubou uma conclusão

Este é o registro mais valioso do dia, e nenhum deles veio de auditoria.

### 3.1 A semântica da allowlist estava ao contrário

Depois de duas rodadas de propostas ruins, ela cortou:

> *"não. olha, é péssimo o que propõe. Esse modo do allowlist só usamos quando
> um jogo tem conexão nativa com dualsense (os controles aparecem dobrados lá,
> tanto xbox quanto sony, por conta do emulador) então quando permitimos o
> allowlist permitimos que possamos usar o hefesto e ter o output seja de xbox
> ou de dualsense com cada uma das features que marcamos aqui. Não faz sentido
> ter um modo próprio."*

O código tinha a mesma inversão. **Ela então mediu**, com o controle na mão, em
25 minutos — e fechou uma pergunta que estava aberta havia onze dias. Virou a
[CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md).

### 3.2 Os nomes propostos eram ruins, duas vezes seguidas

> *"horrível as sugestões. Tão tão confusas quanto antes. Na aba início temos a
> escolha do modo de jogo. Precisamos de nomes melhores dentro de perfis pra
> marcar uma flag lá. [...] A lógica dos nomes precisa ficar óbvia."*

E antes, sobre um caminho de interface proposto:

> *"eu tenho que escolher isso na gui, deveria ser um poder meu [...] horrível
> de verdade. o nome precisa mudar e isso deve ficar na aba de perfis se é
> importante lá."*

**A regra que ficou:** partir do **léxico que já existe na tela**. Um nome novo
que não deriva do que há é sinal de conceito errado, não de falta de vocabulário.

### 3.3 A pergunta do amigo, que matou um desenho antes de ele custar trabalho

Ao perguntar como o Hefesto se comportaria com o controle de **outra pessoa**,
ela derrubou um desenho inteiro antes de virar código. Virou a
[REGRA-NAO-REGISTRO-01](../sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md):
a cura tem de ser **regra**, não **registro** — funcionar no primeiro boot de um
desconhecido, sem ninguém declarar nada.

E o contexto do 8BitDo, na palavra dela:

> *"o 8 bitdo tem os modos pro controler e o modo ps4 mas controle físico é um
> só. são 1 pro controler e dois dualsense"*

---

## 4. O que ela mediu com o controle na mão

**Grau: MEDIDO por ela.** Este é o método que ela pediu para repetir:

> *"eu adoro quando vc faz esses testes comigo pra medirmos e resolvermos na
> raiz do problema"*

Sequência do experimento, com as respostas dela:

| momento | o que ela relatou |
|---|---|
| Mullet, no menu | *"igual o controle por enquanto"* |
| Mullet, em jogo | *"só um controle, aparece como xbox, nada de input duplicado, gatilhos duros"* |
| Mullet, lightbar | *"funcionando o vermelho com perfeição"* |
| Sackboy, no menu | *"1 controle, playstation"* |
| Sackboy, gatilhos | *"não, moles, lightbar tá azul agora"* |
| Sackboy, ao aplicar | *"nem o botão aplicar aplica, mas é pq estamos no modo sony controla né?"* |

**A conclusão dela, que virou doutrina:** no modo em que a Sony controla, o
jogo devolve a lightbar ao azul padrão — e isso está **certo**, não é defeito.

E a autorização explícita para medir sem medo:

> *"pode rodar tudo. se derrubar os controles eu arrumo de novo, o importante é
> resolvermos na raiz. Não estou jogando nem nada. Quero definitivamente apenas
> arrumar a bagunça"*

Foi essa autorização que expôs o `bluetoothd` travando **ao sair** — um
fenômeno diferente do que a sprint em aberto supunha.

---

## 5. A janela que morreu, e como ela avisou

> *"interface travou legal aqui. nem consigo fazer nada nem fechar"*

Com foto. Virou a
[DIALOGO-QUE-MATA-A-JANELA-01](../sprints/2026-08-06-DIALOGO-QUE-MATA-A-JANELA-01-o-aviso-que-deixou-a-janela-dela-morta.md):
um diálogo modal instalava um *grab* do GTK e a janela principal perdia os
**três** canais — clique, tecla e o "X" do gerenciador.

E o detalhe que torna o caso exemplar: a cura foi escrita, cobriu **onze**
diálogos, passou em tudo — e a verificação adversarial achou o **décimo
segundo**, que não passava pelo envelope, com um portão por AST que **jurava não
existir mais nenhum**.

> *"A cura fecha a porta que você atravessou e deixa a do lado aberta, com um
> portão que jura que não há mais nenhuma."*

---

## 6. O erro de método do dia

**Grau: MEDIDO.** Registrado em [CLEAN-ROOM.md](../CLEAN-ROOM.md).

Agentes rodando em paralelo **mutaram a mesma árvore** enquanto outro agente
fazia a medição do produto. Resultado: **22 medições contaminadas**, e uma
bancada acusada de instável que **não era** — ela executava `scripts/doctor.sh`
pelo caminho absoluto da árvore de trabalho, enquanto dois agentes irmãos
arrancavam e devolviam curas nesse mesmo arquivo.

**A regra que ficou: quem mede não divide árvore com quem muta.**

---

## 7. O que a verificação adversarial encontrou

Quatro rodadas sobre as curas do próprio dia. Nenhum destes veio de queixa dela,
e é isso que os torna caros — o estrago só apareceria depois.

| achado | por que importa |
|---|---|
| a poda que apagaria a prova do colapso do `main.conf` | backup **é** o instrumento de medição |
| o backup que se destruía sozinho no mesmo segundo | reproduzido antes da cura |
| o detector que aprovaria o valor perigoso | a suíte inteira aceitou a mutação verde |
| o diálogo irmão que o portão jurava não existir | provado com arquivo forjado |
| **o defeito no método** | agentes paralelos contaminando 22 medições |

E o mais instrutivo: a **cura escrita para impedir uma afirmação sem medida
afirmava sem medir** — `date -d ""` não falha, devolve meia-noite de hoje. Está
na [SELO-VERDE-CEDO-DEMAIS-01](../sprints/2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md).

---

## 8. A refutação que reabriu uma sprint

Uma conclusão registrada como certa foi derrubada pela ordem dos eventos no
journal: o `Watchdog timeout` e o `SIGABRT` do `bluetoothd` vieram **antes** do
`restart` que se supunha ser a causa. O daemon travou sozinho.

E a verificação achou o dono de verdade: o `ExecStopPost` que fotografa os bonds
a cada parada levou **42,8 s** (`flock -w 30` dentro do sandbox da unit), contra
**0,03 s** do mesmo script rodado à mão — **1400 vezes** mais lento. Os "~90
segundos fora do ar" que a sprint afirmava mediram **57,25 s**, e o `RestartSec`
que ela culpava é **1,7%** do prejuízo.

A `BT-AGENT-TRAVA-O-RESTART-01` foi **reaberta com o título refutado**.

---

## 9. O que ela decidiu sobre o projeto

> *"é open source né. Eu desenvolvo pensando ali em mim mas a ideia é ele ficar
> pra comunidade apenas."*

**Isto muda o critério de toda cura**: o que "funciona na máquina dela" não
basta. Virou o estudo
[o que só funciona na máquina dela](2026-08-06-o-que-so-funciona-na-maquina-dela.md).

---

## 10. Onde estão as coisas, para quem retomar

**Grau: MEDIDO** — caminhos conferidos em 06/08.

| o que | onde |
|---|---|
| conversa das duas sessões | `~/.claude/projects/<slug>/<sessão>.jsonl` |
| relatório de cada subagente | `<sessão>/subagents/agent-*.jsonl` + `.meta.json` irmão |
| resultado de cada workflow | `<sessão>/workflows/wf_*.json`, campo `result` |
| script de cada workflow | `<sessão>/workflows/scripts/*.js` |

O relatório final de um subagente é a **última mensagem `type=="assistant"`** do
`.jsonl`. O `wf_*.json` é melhor: traz `workflowName`, `agentCount`,
`totalTokens` e o `result` inteiro, sem reconstituição.

**O scratchpad em `/tmp` é volátil.** Para durar, o destino é este diretório.

---

## 11. O que fica ABERTO, e é dela

1. **`E3`/`E4` do `LUGAR-A-MESA-01`** — tocam o veto do `QUATRO-NO-RÁDIO-01`.
2. **A caixinha do Steam Input** — destravada, com a semântica que só existe
   porque ela mediu; falta ela dizer **onde** na aba Perfis a caixinha mora.
3. **A fila de medições com hardware na mão** — protocolo pronto.

E uma que ninguém sabe responder, registrada **sem promessa**:

> **Ninguém, no Linux, diz ao jogo quem é o jogador N.** O jogo numera por ordem
> de enumeração. A luz pode dizer 2 enquanto o jogo diz 3, mesmo com o
> `LUGAR-A-MESA` inteiro pronto. **Grau: SEM PROVA** de que exista caminho —
> ninguém procurou.
