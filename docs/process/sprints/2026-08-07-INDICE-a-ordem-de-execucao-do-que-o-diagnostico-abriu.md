# A ordem de execução do que o diagnóstico abriu — índice de 07/08/2026

- **Escrito em:** 07/08/2026, na branch `restauro/inicio-da-sessao`, sobre a
  árvore de HEAD `6e04c57` mais as duas mudanças da BUSCA-QUE-ESTOURA-01 no
  índice do git
- **Por que este arquivo existe:** ela pediu, com estas palavras:

  > *"faz uma sprint order de todas as novas sprints que criamos ao
  > diagnosticarmos tudo pra que tudo possa ser executado em levas posteriores"*

- **O que este arquivo é:** o **ponto de entrada de quem for executar**. Quem
  abrir isto amanhã, ou daqui a um mês, sai sabendo em que ordem pegar o
  trabalho e **por que** essa ordem. Não é resumo do dia: é a fila.
- **Lacuna de acervo que ele fecha, e que era real:** **não existia índice de
  07/08**. Oito sprints e cinco estudos nasceram fora de índice, e o índice de
  06/08 os cita em três linhas. **Grau: MEDIDO.**

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, teste que reprova ou `grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou; **DECISÃO DELA** = palavra dela,
que não se repropõe. Este índice **declara o seu em cada bloco** e **não herda**
o grau das sprints que cita.

**Convenção de custo, usada na fila inteira:** **P** = leva pequena (um arquivo,
uma condição); **M** = média (um par de arquivos e um portão); **G** = sprint
inteira. **tela** = exige foto antes e depois pela
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
**jogo** = toca código que chega à partida, com risco de ela perder controle no
meio.

---

## 1. O dia em uma página

**Grau: MEDIDO** nas cinco linhas.

1. **A numeração não colide — ela CRUZA.** O DualSense branco é *Jogador 1* no
   jogo e acende **4** no plástico; o roxo é *Jogador 2* e acende **1**. Os dois
   mentem, e mentem **trocados**.
2. **Calar a luz dos externos curou um defeito que ninguém tinha medido.** A
   decisão dela, tomada por honestidade, apagou um bombardeio de subcomando que
   estava vivo havia dois dias: 348 eventos de `joycon_enforce_subcmd_rate` do
   lado que falava, **zero** do lado calado.
3. **O 8BitDo conecta e desliga porque a busca de serviços estoura**, e não
   porque alguma cura nossa quebrou: o histórico de sete dias mostra a
   intermitência **antes** das curas suspeitas, e os dois relógios que estouram
   são do adaptador e do kernel.
4. **O `doctor` imprimiria selo verde sobre o defeito.** O filtro de
   elegibilidade descarta justamente o controle doente, porque exige do bond um
   campo que um bond nascido sem serviços não tem.
5. **Ela respondeu dezessete perguntas**, e a décima sétima mudou a régua de
   tudo: *"produto — tem que funcionar em máquina limpa"*.

Fonte das cinco:
[DUAS-CONTABILIDADES-01](2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md),
[o estudo ISOLAR](../estudos/2026-08-07-ISOLAR-os-externos-o-metodo-da-lightbar-no-pro-e-no-8bitdo.md),
[BUSCA-QUE-ESTOURA-01](2026-08-07-BUSCA-QUE-ESTOURA-01-o-sdp-que-nao-responde-a-tempo.md)
e [as respostas dela](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md).

---

## 2. A cadeia que manda na ordem

**Quem não entender esta seção vai executar na ordem errada e reabrir defeito
curado.** Ela é curta de propósito.

### As duas travas que ela criou

**Grau: DECISÃO DELA**, as duas, em 07/08/2026.

| trava | o que ela decidiu | consequência para quem executa |
|---|---|---|
| **resposta 3** | os externos ganham lugar próprio na partida **só depois da máscara por controle** | *"não comece a adoção dos externos. Comece pela máscara. A ordem virou `MASCARA-01` → `E3` → `E4`"* |
| **resposta 12** | **calar a luz até a entrega existir** | *"a luz volta quando a entrega existir, não quando alguém achar que já dá"* |

A trava 3 promoveu a
[MASCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) de
sprint paralela a **pré-requisito**. A trava 12 desligou o player-LED dos
externos — `EXTERNAL_PLAYER_LED_ENABLED = False` em
`daemon/subsystems/external_identity.py`. **Grau: MEDIDO** (a constante está lá,
e o chamador a consulta antes de escrever).

### O desenho da cadeia

```
                REAVALIAR as seis entregas da MASCARA-01
                contra a arvore de hoje  (nao foi feita)
                                |
                                v
  M-1 (FEITA) --> M-2 (portao) --> M-4 (tela) --> M-5 (travessao)
                                |
                                |   [ isto e "a mascara por controle" ]
                                v
                     LUGAR-A-MESA-01 / E3  (a adocao)
                                |
                                v
                     LUGAR-A-MESA-01 / E4  (esconde-esconde por par)
                                |
                                v
                   M-3 (emitir as variaveis da mesa)
                                |
                                v
                A LUZ VOLTA, e com numero que nao mente

  Fora da cadeia, e liberadas por escrito pelo VETO:
      E0a (FEITA)   E0b (aberta)   E1 (aberta)   E2 (FEITA)
```

### A circularidade, e a leitura que a desfaz

**Grau: MEDIDO** que a circularidade existe no texto. A **entrega 3 da
MÁSCARA-01** (ligar a lista de pares) está declarada como dependente da `E4` da
LUGAR-À-MESA-01, que depende da `E3`, que depende da MÁSCARA-01. Se *"MÁSCARA-01
pronta"* significar **as seis entregas**, a cadeia **não anda nunca**.

**A leitura que este índice adota, e que está escrita para poder ser derrubada:**
o que a resposta 3 exige é a **máscara por controle** — a `M-1` (feita), o
portão residual da `M-2`, a tela da `M-4` e a honestidade da `M-5`. A `M-3` é a
**emissão** das variáveis, e essa é a **última** da fila, não a primeira.
**Grau: SUSPEITA COM MECANISMO** — a leitura fecha nos dois textos, e ninguém a
confirmou com ela. **A pergunta está pronta na seção 4, e é a primeira da lista.**

Enquanto ela não responder, a ordem anda até a `M-5` sem tocar na `E3`. Nada se
perde: tudo o que vem antes da `E3` é necessário nas duas leituras.

### A dependência morta, que trava a cadeia antes do primeiro passo

**Grau: MEDIDO.** A MÁSCARA-01 declara a
[IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md) como
*"pré-requisito duro"* — e a IDENT-01 **caducou em 06/08**, substituída pela
[REGRA-NAO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md),
que está em **PROPOSTA**, sem uma linha escrita.

O diário de execução já registrou o que fazer: *"Uma sprint que espera por uma
dependência morta não anda"*, e manda a onda 3 começar por **reavaliar** as seis
entregas contra a árvore de hoje. **Essa reavaliação ainda não foi feita, e é o
primeiro passo da cadeia** (leva 2, abaixo).

### O fato que complica: calar a luz curou o Pro por acidente

**A casa canônica deste fato é a
[A-LUZ-QUE-CUROU-01](2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)**,
escrita depois deste índice e encaixada nele. Ela recontou os números na máquina
dela viva e **derrubou três dos cinco passos** da cadeia que a casa tinha
escrito — o desfecho estava certo, o meio estava errado.

**Grau: MEDIDO.** Régua do kernel dos dois lados, no journal dela.

| métrica | lado A, LED falando (18h20m) | lado B, LED calado (3h27m) |
|---|---|---|
| `joycon_enforce_subcmd_rate` | **348** | **0** |
| `Setting an LED's brightness failed` (`-110`) | **83** | **0** |
| storms com escrita nossa no mesmo minuto | 15 de 15 | — |

A escrita do Hefesto **causa** o storm: subiu de SUSPEITA COM MECANISMO para
**MEDIDO**. E o mesmo bombardeio é o mecanismo que a `EXT-04` registra como
tendo **matado** o 8BitDo — o comentário está em `daemon/ipc_handlers.py`, e
diz, com todas as letras, que aquela função *"NUNCA MAIS escreve LED"*.

**Nove coisas que a ordem carrega por causa disso**, e que valem para toda leva
daqui para baixo:

1. **A janela do lado B fecha na primeira escrita nova.** Recontar o E-1 com as
   24 h que a previsão pedia custa **zero** e só é possível agora. **Grau:
   MEDIDO que falta** (existem 3h27m contra 24 h pedidas).
2. **Uma linha de `joycon_enforce_subcmd_rate` com o portão em `False` significa
   um segundo escritor** — e achar quem é passa à frente de tudo.
3. **A escrita idempotente é pré-requisito MEDIDO da `E3`, não sugestão.** O
   laço nasce da escrita que **falha no meio**, não do número. Voltar a luz sem
   idempotência devolve o laço inteiro.
4. **Toda escrita da `E3` passa pelo limitador de taxa do tick e usa o
   `_display_authority` que já existe** em
   `daemon/subsystems/external_identity.py` — sem criar um segundo caminho.
   **Grau: MEDIDO** (o método está lá, na linha 1118).
5. **O 8BitDo é mais frágil que o Pro, e o E-4 ainda não rodou.** O firmware
   clone morre sob bombardeio de LED, e ele **não** passa pelo `hid-nintendo` —
   o rate-limit que protegeu o Pro não existe para ele. Religar os dois ao mesmo
   tempo mistura dois riscos com mecanismos diferentes.
6. **Enquanto qualquer janela de medição estiver aberta, religar a escrita
   invalida a régua.** O storm calado já riscou um suspeito de graça.
7. **A régua é do KERNEL nos dois lados.** Nunca o `probe_offline`: comparar um
   lado pelo daemon e o outro pelo kernel é o erro que inventa resultado.
8. **O custo já foi aceito e já foi pago:** a barra do Pro está **congelada** em
   `player-1=1, player-2=1` desde 15h24:01. Não é defeito novo; é o preço da
   resposta 12. Se alguma leva mexer nisso, volta a ser pergunta dela.
9. **O teste tem de morder no lugar certo.** A `E2` já provou que prova de
   comportamento não alcança recaída de arquitetura: o portão anti-adoção
   precisou ler o **texto** do `daemon/subsystems/coop.py`.

### A trava que a A-LUZ-QUE-CUROU-01 acrescenta, e ela reordena duas levas

> **NENHUMA CURA DE LUZ ENTRA ANTES DA CURA DA NUMERAÇÃO.**

**Grau: MEDIDO** nas três razões, que não são estilo:

1. **Curar a escrita antes do número prepara o cano para devolver o número
   ERRADO com mais confiança e mais barato.** Hoje o produto acende 4 no
   plástico que o jogo chama de *Jogador 1*. Uma escrita idempotente e
   verificada faria isso de forma mais estável e mais convincente.
2. **Curar o DETECTOR sem curar a ESCRITA liga o laço infinito que hoje não
   existe.** É a cegueira do detector que faz a repintura terminar. Um detector
   honesto sobre uma escrita que ainda falha no meio repinta a cada 2 s, **para
   sempre**.
3. **A cura da numeração é a única que não custa NADA à resposta 12.** Ela se
   mede e se prova com os dois DualSense, **com a luz dos externos calada**,
   hoje, na mesa dela.

**E a honestidade que fecha a trava:** nenhuma dessas curas reacende coisa
alguma. Elas fazem o número ficar certo e a escrita ficar barata **enquanto a
luz continua calada**. Até ela mandar reacender, **o plástico não muda um
lúmen**.

**Consequência na fila:** a leva 7 (o cruzamento) passa a ser **pré-requisito da
leva 9**, e não apenas uma leva de valor próprio. A ordem 7 antes de 9 já estava
certa; agora ela é **obrigatória**.

**E o achado de método, que vale para a ordem inteira:** *"parar de afirmar o
que não se entrega apaga trabalho que ninguém tinha medido"*. O corolário é
executável: **quando uma decisão de honestidade desligar um caminho, medir no
journal o que ela apagou, dos dois lados do corte** — o A/B nasce montado e de
graça. **Grau: MEDIDO uma vez.** Uma ocorrência não é lei, e a ressalva fica
colada.

### A regra de operação que vale para todas as levas

**Grau: MEDIDO.** A suíte cria **17 teclados falsos com nome de produção** a
cada rodada, e o daemon dela **reage** a eles: escreve no estado e esconde
`/dev/hidraw2`. Enquanto a `BT-1` da
[BERCO-DE-TMP-01](2026-08-07-BERCO-DE-TMP-01-a-suite-nao-suja-a-config-dela-suja-o-tmp.md)
não estiver curada, **nenhuma leva roda a suíte durante janela de medição** — e
nenhuma medição feita com a suíte em execução vale como prova.

---

## 3. As levas, em ordem

A fila está ordenada por **o que destrava, dividido por custo mais risco**,
respeitando as dependências da seção 2. **Coisa que ela sente hoje ganha peso.**
Onde a ordem contraria o gosto de quem executa, o motivo está escrito na coluna
*"por que aqui"*.

---

### LEVA 0 — A janela que fecha, e só existe agora

**Por que aqui:** é a única leva cujo custo é **zero** e cuja perda é
**irreversível**. Nenhum dos três itens escreve no controle, no rádio ou no
`/etc`; os três perdem dado se ficarem para depois.

| item | o que entra | o que destrava | custo |
|---|---|---|---|
| **IS-J5** | recontar o E-1 com as **24 h** que a previsão pedia, mesma régua do kernel, mesmo comando | a previsão cumprida **no tamanho**, e não só na direção | zero |
| **IS-E4** | deixar o 8BitDo em PS4 uma noite com o rádio limpo, para saber se ele cai sozinho | é quem decide se o storm matava o 8BitDo — o E-1 **não** responde isso | zero atenção dela |
| **OQ-1** | extrair do journal os 348 eventos de 05 a 07/08 **antes de qualquer restart** — falta um `fflush()`, e eles estão num buffer, não no arquivo dela | ela ter a explicação da queda | P |

**Grau: MEDIDO** que a janela existe e que ela fecha na primeira escrita nova.
**Grau: SUSPEITA COM MECANISMO** para o `fflush` ausente — o caminho de código
fecha, e ninguém o provou na máquina dela.

**Armadilha desta leva:** o `storm_watch.sh` com `-n0` faz o caderno não valer
como prova de nada (118 linhas, zero eventos, três storms antes de a unit
subir). **Se a leva 0 usar o `storm_watch.sh`, a `CR-9` da leva 3 vem junto.**

---

### LEVA 1 — O defeito que ela sente, e que já tem causa medida

**Por que aqui:** é a **única frente de gravidade ALTA que atinge o uso dela
agora**. Ela pediu para esperar os trabalhos em voo; eles terminam com este
índice. E a causa deixou de ser suspeita: são **dois relógios**, os dois medidos
na máquina dela, e nenhum é nosso.

| erro | quantos | tempo até falhar | relógio |
|---|---|---|---|
| `Host is down (112)` | 3 | **6 s** | page timeout do adaptador |
| `Connection timed out (110)` | 2 | **42 s**, idênticos | `L2CAP_CONN_TIMEOUT` de 40 s, no cabeçalho do kernel |

**Grau: MEDIDO.** E a correção que esta leva carrega: o histórico de sete dias
(01/08=17, 02/08=18, 03/08=1, 04/08=4, 05 e 06/08=0, 07/08=5) mostra que a
"regressão" é **anterior** às curas suspeitas. **A suspeita sobre o
`JustWorksRepairing=confirm` não está confirmada, e não está apagada** — ver a
`CD-1` na seção 5.

| item | o que entra | por que aqui | custo |
|---|---|---|---|
| **cura B** | só **avisar** quando o par `unknown device` + `error updating services` aparecer dentro de um minuto (hoje: 4 ocorrências, nenhuma sem defeito) | não toca o rádio, e transforma um defeito invisível em defeito visível | P |
| **cura D** | o retrato de bond do `scripts/bt_bonds_snapshot.sh` **recusar** bond sem serviços | impede que um bond doente seja gravado como bom e restaurado depois | P |
| **CD-3** | o terceiro estado do `scripts/doctor.sh`: o check sai por `info` sem sudo, e `info` lê-se como *"nada a relatar"* quando significa *"não olhei"* | diagnóstico honesto; hoje o selo verde cobre o buraco | P |
| **o filtro cego** | o `check_bt_sdp_cache_envenenado` exige `Services=` no `info` — e **descarta justamente o bond doente**, que nasceu sem serviços | é a lição da [BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md) reproduzida cinco dias depois, com prova datada | P |

**Armadilha para quem escrever o gatilho, MEDIDA:** o Pro está agora com
`ServicesResolved=false`, conectado e funcionando. **`ServicesResolved` não
serve de critério** — só os `UUIDs`.

**Achado de método que fica:** num defeito que se cura ao ser tocado, o
**carimbo de tempo é a medição**. Ler conteúdo antes de `mtime` produz
absolvição falsa — foi assim que a BT-SDP-VAZIO-01 quase foi dada como caduca.

**O que NÃO entra aqui:** a cura A (empurrão do host) espera o protocolo de dois
minutos da seção 5; a C (re-parear sozinho) **nunca**, por decisão de máquina; a
E (mexer no rádio) não. **Grau: DECISÃO DE PROJETO**, escrita na sprint.

---

### LEVA 2 — A reavaliação que destrava a cadeia inteira

**Por que aqui:** é o **maior destravamento por unidade de custo de toda a
ordem**. Custa leitura e um documento; libera tudo o que vem depois. E o próprio
diário de execução já a declarou como o primeiro passo da onda 3.

| item | o que entra | custo |
|---|---|---|
| **reavaliar as seis** | ler as seis entregas da MÁSCARA-01 contra a árvore de hoje e escrever **nota datada** dizendo quais sobrevivem, quais mudaram e o que a dependência morta vira | M |
| **a dependência morta** | a IDENT-01 caducou; declarar por escrito o que a REGRA-NAO-REGISTRO-01 substitui, e o que **não** substitui | P |
| **a leitura de "pronta"** | registrar a leitura da seção 2 — ou levar a pergunta a ela, que já está pronta na seção 4 | P |
| **a contradição do applet** | a `E0.2` da [APPLET-MONOCROMATICO-01](2026-08-07-APPLET-MONOCROMATICO-01-o-icone-que-destoa-do-painel.md) continua listada como PENDENTE, e a **resposta 13 já respondeu: não** | P |
| **a nota da mãe** | colar na LUGAR-A-MESA-01 a nota datada da DUAS-CONTABILIDADES-01, que ainda não está lá | P |

**Grau: MEDIDO** que nenhum destes cinco foi feito. **Nenhum toca código de
partida, nenhum toca a tela.**

**Regra da casa que se aplica inteira aqui:** *não se apaga decisão medida*. A
reavaliação **anota o que caducou com data**; não reescreve a sprint por cima.

---

### LEVA 3 — O instrumento e a página param de mentir

**Por que aqui:** cada item é **P**, nenhum toca a partida, e todos eles são
pré-condição para que as medições das levas seguintes valham alguma coisa. Um
instrumento quebrado não atrasa uma leva — ele **inventa resultado** e contamina
todas as que vierem depois.

| item | o que entra | o que destrava | custo |
|---|---|---|---|
| **CR-9** | o `scripts/storm_watch.sh` com `-n0` faz o caderno não valer como prova | o caderno voltar a ser evidência | P |
| **CR-8** | nota datada no `README.md`: os *"~40% do sinal"* e os *"55% a 75%"* **caducaram** — foram medidos com um desmutador acidental por baixo | honestidade de produto, custo trivial | P |
| **CR-P7** | o *"~35% de banda"* é de **um** controle, janelas de 3 s, 25/07, nunca remedido | o número publicado ser verdade | P |
| **OQ-7** | duas asserções que faltam no portão de paridade: o alvo do `RUN+=` e o `groupadd`. Hoje ele imprime OK para a regra 82 **exatamente enquanto ela falha 15 vezes em 15** | portão que pare de mentir | P |
| **PR-4** | `probe_offline` é **um nome só para três coisas diferentes** — cabo, `bluetoothd` e link. É isso que faz *"três por dia"* parecer defeito único | nenhuma leva futura refaz a classificação à mão | P |
| **PR-5** | a borda de subida não registra **de onde veio** a volta | a `PR-Q3` fechar sem cronômetro | P |
| **PR-6** | o arquivo de amostras carrega endereço, e a forma compacta de 12 dígitos **passa pelos dois portões** | não vazar endereço | P |
| **EN-2** | `tests/unit/test_poll_loop_evdev_cache.py` continua com a forma antiga; a cura existe e é de **três linhas** | um teste a menos que reprova por relógio | P |
| **BT-6** | `utils/i18n.py` e `core/system_check.py` leem o `$HOME` real sob teste | teste que não dependa da máquina | P |
| **BT-3** | sobram arquivos de trava órfãos: o produto apaga o perfil e esquece a trava | higiene (limpar os que já existem é gesto dela) | P |
| **IN-3 / IS-8** | **doze** arquivos de `assets/` e três docstrings da árvore citam estudos que **não existem** nesta árvore — e o portão não vê, porque só varre `docs/` | procedência auditável | M |
| **IN-4** | o `nix run` do `README.md` é impossível por construção | honestidade; a cura de verdade não cabe aqui (ver seção 6) | P |
| **BZ-2** | conferir se o defeito upstream #2034 aparece no journal dela — fecha em **um comando**, sem hardware | uma hipótese a menos nas recusas | P |
| **EN-1** | o A/B do governador de CPU. **Nada toca hidraw, rádio ou serviço; nenhum controle cai** | se a bancada em economia muda o veredito da suíte | P |
| **BT-1** | os 17 teclados falsos com nome de produção, aos quais o daemon dela **reage** | para de contaminar medição e de mexer no controle dela | M |
| **RS-4** | a recusa `incerta` é grosseira: **uma** regra não avaliável tira o conserto de um nó legítimo | consertos legítimos que hoje são recusados | P |

**Grau: MEDIDO** em todos, menos a `EN-1`, que é a medição em si.

**A `BT-1` é a mais cara da leva e a que mais paga**, porque é a única que
impede a suíte de mexer no controle dela. Se a leva tiver de ser cortada, a
`BT-1` é a última a sair.

---

### LEVA 4 — As curas que chegam e não valem, ou não chegam

**Por que aqui:** a **resposta 17** mudou a régua — *"produto: tem que funcionar
em máquina limpa"*. Isso promoveu três curas de "detalhe" a dívida alta, e
derrubou a dependência que segurava a `IN-5`. Cada item é P ou M, todos já têm
desenho, e **nenhum existe hoje com teste que morda**.

| item | o que entra | por que aqui | custo | jogo |
|---|---|---|---|---|
| **OQ-2 + OQ-3** | o cadeado que comeu 42,8 dos 57,25 segundos de Bluetooth fora do ar, **e** o teto de tempo. O parsing de argumentos tem **uma vaga só** e tem de virar laço | **os dois no MESMO commit**: sem o OQ-2, o teto vira guilhotina; sem o laço, a cura nasce inerte | P | **sim** |
| **OQ-6** | a regra que daria acesso aos nós de entrada **nunca foi escrita**. Hoje o touchpad e o giroscópio dela só funcionam porque ela está no grupo `input` por fora | numa máquina limpa, falham **em silêncio** — é o caso exemplar da resposta 17 | M | **sim** |
| **OQ-5** | a regra 78 procura um nome de aparelho que o produto renomeou: a rede de segurança dos sensores está morta desde um rename | rede de segurança no cenário de quatro jogadores | P | não |
| **OQ-4** | a regra 72 escuta `add` e o install dispara `change`: o passo é **no-op silencioso**, e o ADR documenta o comando errado como se fosse a cura | higiene; a regra 81 já a subsumiu | P | não |
| **OQ-8** | a janela não sabe dizer qual Pro Controller é qual: a marca é gravada em quatro camadas e **nenhuma linha de Python a lê** — e o `install.sh` **imprime a promessa** | o Pro genuíno separado do clone | M | não |
| **OQ-9** | a página de solução de problemas manda ela colar uma receita que **não funcionaria** com nenhum controle dela | não queimar a confiança na página numa noite ruim | P | não |
| **IN-5** | quatro dos doze perfis de fábrica são **biografia dela** — o `meu_perfil` com prioridade 1 vira o catch-all na máquina de outra pessoa | **destravado pela resposta 17**; era "pergunta aberta" e virou dívida com data | M | não |

**Grau: MEDIDO** em todos. **Ressalva de segurança, e ela não é opcional:** estes
itens mudam o repositório, não a máquina dela. **A instalação na máquina dela
espera uma janela sem controle na mesa** — a `OQ-6` escreve regra de udev, e a
`OQ-2`/`OQ-3` mexem no ciclo do Bluetooth.

---

### LEVA 5 — O áudio para de quebrar o sensor

**Por que aqui:** é **uma condição e um teste que morde**, e é **pré-requisito
duro** de tudo o que ela quer no
[CONTROLE-INTEIRO-NO-RADIO-01](2026-08-07-CONTROLE-INTEIRO-NO-RADIO-01-o-mic-e-o-fone-que-nao-atravessam.md).
Custa P e evita uma quebra real.

| item | o que entra | custo | jogo |
|---|---|---|---|
| **CR-P0** | **ligar o mic por rádio hoje quebra o giroscópio e o touchpad** — cerca de 106 pacotes de áudio por segundo entram como estado de input. A condição que impede isso, mais o teste que reprova quando ela é arrancada | P | **sim, direto** |

**Grau: MEDIDO.** E o estado da frente, dito sem rodeio: *"jogar no BT com mic e
fone hoje é, na melhor das hipóteses, jogar no BT com mic — e mesmo esse mic não
chega ao Don't Scream sozinho"*.

**O resto da sprint de áudio não entra aqui**, e o motivo é dependência, não
gosto: a `CR-P4` (por qual report o áudio sai — a casa tem **duas respostas
incompatíveis**, `0x39` contra `0x32`, e nenhuma foi medida) precisa de meia hora
com o controle na mão dela, e é ela que destrava a `CR-P5`, a metade que **não
existe** — não há uma linha em toda a árvore no sentido host para controle.

---

### LEVA 6 — A mesa aparece na tela

**Por que aqui:** é a primeira coisa que **ela vê mudar** desde que a luz calou —
e a luz calando custou a ela o próprio instrumento, porque ela distingue os
controles pela cor e pelo LED de jogador. Devolver a mesa na tela paga parte
disso **sem acender nada e sem adotar ninguém**. As três entregas estão
**autorizadas por escrito** pelo VETO: *"As entregas E0, E1 e E2 NÃO reabrem o
veto e podem andar sem essa decisão."*

| item | o que entra | o que destrava | custo | tela |
|---|---|---|---|---|
| **LM-E1** | a mesa nos cartões servidos do cache que já existe, com estado **DESCONHECIDO** distinto de zero | ela ver a mesa sem que nada seja afirmado | M | **sim** |
| **LM-E0b** | o eixo da numeração ganha interruptor: `auto_numbers` com campo no esquema e superfície | dar a ela o controle do eixo | P | **sim** |
| **M-2** | o portão *"só quando a máscara pedir"* — camada fina sobre a descoberta que a `E2` já entregou | quem recebe tratamento de jogador | P | não |

**Grau: MEDIDO** que a `LM-E0b` está aberta: `auto_numbers_enabled` é lido no
daemon, e o `grep` em `config/` e `app/` devolve **zero**. Conferido nesta
árvore, hoje.

**Proibição que esta leva carrega, MEDIDA:** ninguém, no Linux, diz ao jogo QUEM
é o jogador N. **Nenhum texto de tela pode prometer que o número aceso é o mesmo
do jogo.** A LUGAR-À-MESA-01 proíbe isso por escrito.

**Tela:** a resposta 11 autoriza executar **tudo, inclusive a tela**, sem ela na
cadeira. Isso **não** revoga a PROVA-DE-TELA-01: o trabalho é feito e
**apresentado com as fotos**, e a palavra final continua dela. Rodar
`scripts/gui-captura/retratar_abas.py` antes e depois.

---

### LEVA 7 — O cruzamento

**Por que aqui:** é **o defeito que ela vê toda sessão**, é o **caminho mais
curto para a dor real** — DualSense contra DualSense, **não passa pela
máscara**, não dá vpad a externo nenhum, não acende externo nenhum — e, desde a
A-LUZ-QUE-CUROU-01, é **pré-requisito da leva 9**. Vem depois das levas 0 a 6
porque custa mais e mexe no co-op e no registro ao mesmo tempo.

| item | o que entra | custo | tela | jogo |
|---|---|---|---|---|
| **DC-1 / S9** | o branco é *Jogador 1* e acende **4**; o roxo é *Jogador 2* e acende **1**. **Uma só conta**, para o número da lâmpada e o nome do jogo saírem do mesmo lugar | M a G | **sim** | **sim** |
| **DC-3** | o teste que morde já tem meia casa pronta; falta o caso de **dois** DualSense com o co-op ligado — que é a mesa dela de hoje | P | não | não |
| **S10** | prender o número ao lugar persistido, para parar a renumeração que oscila sozinha | P a M | não | **sim** |

**Grau: MEDIDO** o cruzamento. **Correção de 07/08, e ela derruba o que este
índice dizia antes:** a cura **tem desenho agora** — é a saída `S9` da
A-LUZ-QUE-CUROU-01, com veredito *"ENTRA, e vai na frente"*. Onde este índice
dizia *"sem desenho"*, leia-se **desenhada, com dois caminhos e a escolha
pendente**.

**Os dois caminhos, e a escolha é dela porque é desenho:**

1. **a exibição obedece ao jogo** — a lâmpada passa a ler a conta do co-op
   quando o co-op está ativo;
2. **o jogo obedece à fila** — o co-op passa a eleger o primário pela fila
   persistida, em vez de *"o primeiro que entrou e ainda está presente"*.

**Risco medido do caminho 2:** ele **muda quem é o Jogador 1 no meio da
sessão**, e a casa já mediu o preço de derrubar e recriar jogador —
`tests/unit/test_vpad_anti_recreate.py` existe por causa disso. **Grau:
MEDIDO.**

**Relação com a `DC-2`, agora precisa:** o caminho 1 **não** depende da `DC-2`;
o caminho 2 **é** a `DC-2` (a ordem da fila, que revoga três decisões medidas de
25/07). Ou seja: **dá para curar o cruzamento sem responder a `DC-2`, desde que
se escolha o caminho 1.** A escolha está na seção 4. **Grau: MEDIDO** pela
leitura das duas sprints.

**Onde o teste já tem meia casa:**
`tests/unit/test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py`. Falta o caso
de dois DualSense com o co-op ligado — literalmente a mesa dela.

**Companheira desta leva, e ela tem dono:** a `DC-4` — o nó contra a identidade
no co-op é a `E1` da
[COOP-QUE-NAO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md),
**sem uma linha escrita**. Custo M, toca a partida.

---

### LEVA 8 — A máscara na tela

**Por que aqui:** é a **condição literal da resposta 3**. Andar aqui é andar na
cadeia, não contorná-la. Depende da leva 2 (a reavaliação) e da `M-1`, que já
está feita.

| item | o que entra | custo | tela |
|---|---|---|---|
| **M-4** | a tela onde ela escolhe a máscara de cada controle, **com o preço de cada opção escrito** | M | **sim** |
| **M-5** | controle em *"como ele mesmo"* mostra **travessão**, não número que mentiria | P | **sim** |

**Grau: MEDIDO** que as duas estão abertas e não começadas. **Grau: MEDIDO** que
a `M-1` está feita (`daemon/subsystems/external_mask.py` existe nesta árvore).

**O preço que a tela tem de escrever, e é medido:** *"Como DualSense"* num Pro
Controller **custa o giroscópio**, enquanto a `M-6` não existir. Uma tela que
oferece a opção sem dizer isso mente por omissão.

---

### LEVA 9 — O que a `E3` exige antes de existir

**Por que aqui:** as peças podem ser construídas **com o portão em `False`** —
construí-las **não reacende nada**, porque o chamador continua desligado. E sem
elas a `E3` quebra coisa medida.

**Ordem interna, imposta pela A-LUZ-QUE-CUROU-01 e não negociável:** primeiro a
leva 7 (o número certo), **depois** a escrita barata e honesta — as saídas `S3`
(o detector comparar contra o que **nós** escrevemos, correção de uma linha),
`S4` (escrita **diferencial**: só o nó cujo valor muda), `S5` e `S7` (o limite
por subcomando). Inverter isso liga um laço infinito que hoje não existe.

| item | o que entra | por que antes da `E3` | custo | jogo |
|---|---|---|---|---|
| **S5** | tirar o azul da conta: o `blue:player-5` deixa de ser o bit *"+5"*, e o produto para de escrever num nó que é o **LED HOME**. **Declarada obrigatória, independente de tudo** | menos um subcomando por chamada, sempre | P | não |
| **escrita idempotente** (`S3` + `S4`) | a escrita do LED externo que não repete o que já está no aparelho, e o detector que compara contra o que nós escrevemos | **pré-requisito MEDIDO**: o laço nasce da escrita que falha no meio | M | não (portão em `False`) |
| **rota de FF** | hoje o rumble de um externo faz **todos** os DualSense vibrarem: o endereço de um externo jamais casa handle do backend, e o código **cai no broadcast histórico** | sem ela, a `E3` estraga o rumble de quem já funciona | M | **sim** |
| **precedência do LED** | com a `E3`, o player-LED do externo passa a ter **dois escritores** e precisa de precedência declarada | sem ela, dois donos escrevem no mesmo aparelho | P | **sim** |
| **M-6** | ponte de giroscópio para externo mascarado | sem ela, *"Como DualSense"* num Pro custa o giroscópio | G | **sim** |

**Grau: MEDIDO** o broadcast — está em `daemon/subsystems/gamepad.py`, e o
comentário na linha 783 diz literalmente que o MAC que não casa handle cai no
*"broadcast histórico (documentado)"*. Conferido nesta árvore, hoje.

**Três coisas que a `E2` deixou abertas e caem nesta leva:** ninguém leu um
`absinfo` de verdade neste caminho (tudo é dublê); a zona morta do Pro
(`flat=500`) não é aplicada; e o normalizador **não tem consumidor** — quem
apontaria é a `E3`.

**As três exigências que a `E3` herda, e nenhuma existe hoje.** **Grau:
SUSPEITA COM MECANISMO** — derivação direta dos achados, nenhuma executada nem
medida:

1. **um número ESTÁVEL para escrever** — enquanto o estado de conexão tiver dois
   escritores, o valor a pintar oscila sozinho (é a leva 7 e a `S10`);
2. **uma escrita que saiba se falhou** — hoje o código declara sucesso com uma
   lâmpada de cinco, e o cache grava como se tudo tivesse ido;
3. **um limite cuja unidade seja o SUBCOMANDO**, não a chamada, e cujo valor
   seja maior que o custo medido de uma repintura.

**A regra que não se apaga:** a `S5` derruba a regra R-25 (o azul como *"+5"*),
que é decisão medida. Ela **ganha nota datada, não sumiço** — e os três testes
que travam hoje o comportamento antigo em `tests/unit/test_external_leds.py`
mudam **junto**, no mesmo commit, com a nota.

---

### LEVA 10 — A adoção (`LM-E3`)

**Por que aqui:** está **bloqueada pela resposta 3** e não existe sem a leva 8 e
a leva 9. É **G**, toca a partida e a tela, e é a leva que **fecha a queixa** que
abriu a LUGAR-À-MESA-01: três controles ligados e um jogador só.

**Pressuposto central que continua SEM PROVA:** o grab e o FF num aparelho que
**não é Sony**. Ninguém mediu. Uma leva que comece assumindo que funciona começa
apostando.

**E o veto:** o de 19/07 (*"externo não ganha controle virtual"*) **não foi
derrubado — foi adiado com condição**. Enquanto a máscara não existir, ele vale.
**Grau: DECISÃO DELA.**

---

### LEVA 11 — O esconde-esconde, e a luz que volta

| item | o que entra | custo | jogo |
|---|---|---|---|
| **LM-E4** | o esconde-esconde honesto, com cobertura **por par** de VID/PID | M | **sim** |
| **M-3** | as variáveis que escondem os controles do jogo passam a ser montadas da mesa (a função pura já existe, composta de uma lista com **um** item) | M | **sim** |
| **a luz** | o player-LED dos externos volta, **com número que não mente** | P | **sim** |

**Grau: MEDIDO** que a `M-3` está pela metade. **A luz é a última coisa da
ordem, e isso é decisão dela:** *"a luz volta quando a entrega existir, não
quando alguém achar que já dá"*. **Encurtar isso é repropor decisão medida —
proibido pela casa.**

---

### NOTA DATADA — 07/08/2026: quatro itens de rádio, controles e protocolo que esta ordem não roteou

**Esta seção não acrescenta trabalho novo — acrescenta ENDEREÇO.** Uma varredura
de 07/08 conferiu as listas de *"o que fica ABERTO"* das dezessete sprints de 06
e 07/08 contra as doze levas acima, e o que saiu é **MEDIDO**: `grep -c -F`
neste arquivo devolvia **zero** para o nome de dez sprints de 06/08. O que delas
chegou aqui chegou de carona nos inventários de 07/08 (os rótulos `EN-`, `BT-`,
`IN-`, `OQ-`, `CR-`, `RS-`, `PR-`, `IS-`, `CD-`, `BZ-`, `AP-`), nunca pela
leitura da lista de aberto da sprint de origem. Por isso a cobertura é boa em
07/08 e rala em 06/08.

**Esta nota e a nota `PI-` do fim deste arquivo são IRMÃS, e não se repetem:**
aquela roteia produto, instalação e interface; esta, **rádio, controles e
protocolo**. As duas dívidas de máquina limpa e de áudio que também são de rádio
já entraram lá como `PI-1` e `PI-2`, e por isso **não** são repetidas aqui.
Somadas, são **dez** itens sobre o placar da seção 7, que continua contado às
21h15 e não se reescreve.

**Nenhum destes quatro está esquecido:** todos estão escritos e datados na sprint
que os mediu, e nenhuma sprint foi apagada. O defeito é de **roteamento** — quem
abrir este índice amanhã, que é o ponto de entrada de quem executa, não os
encontra. **E a leva sugerida é sugestão, não decisão:** a ordem tem travas dela
(as respostas 3 e 12), e mexer nelas não é de quem varre.

1. **A réplica do parser do `bluez_config.sh` recusa menos que o oráculo.**
   **GRAU: MEDIDO.** `scripts/bluez_config.sh:344` (`_linha_que_o_parser_recusa`)
   decide se o `bluetoothd` aceitaria o `main.conf` com **duas** regras; o
   GKeyFile de verdade recusa mais — chave vazia (`=`), chave com `[` ou `]`,
   grupo `[]`. Nesses casos o `bluetoothd` **descarta o arquivo inteiro**,
   inclusive a configuração de segurança da casa, e o dono único responde
   `veredito: OK`, o `aplicar` anuncia "garantidos" e o `doctor` imprime
   `[ OK ]`. **A bancada não morde:** os três casos da `_TABELA_DA_RECUSA` caem
   dentro das duas regras já implementadas. Escrito em
   [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md),
   seção *"ABERTO, GRAVIDADE ALTA"*. É a mesma classe que as levas 1 e 3 existem
   para curar — **diagnóstico que mente** — e é o único item de gravidade ALTA
   que ficou de fora. **Leva candidata: 1 ou 3**, ao lado do `CD-3`.

2. **A varredura de regras de udev não lê `ENV{...}` nem `GOTO`.**
   **GRAU: SUSPEITA COM MECANISMO.** Regra de terceiro que abra o hidraw por
   caminho indireto passa batida em três lugares: na acusação do `doctor`, no
   defeito 3 do SELO-VERDE e no inventário do restauro — onde ganhou
   consequência nova: o nó aberto por regra indireta é classificado como
   **órfão**, e o restauro nesse caso é **atropelo** (o texto na tela avisa que
   o nó pode reabrir, mas aviso é consolo, não trava). Escrito em
   [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md)
   e em
   [RESTAURO-SO-COM-SINTOMA-01](2026-08-07-RESTAURO-SO-COM-SINTOMA-01-o-conserto-que-ninguem-podia-chamar.md).
   A `RS-4` e a `RS-5` desta última atravessaram para a leva 3; este, escrito no
   parágrafo **vizinho de cima**, não. **Leva candidata: 3**, ao lado da `RS-4`.

3. **O 8BitDo saiu do rádio e continua sem HID — a terceira forma de zumbi.**
   **GRAU: MEDIDO.** Está catalogada na seção 1.2 de
   [os externos, a referência canônica](../../protocol/externos-referencia-canonica.md),
   **não tem cura em lugar nenhum**, e a vigia `scripts/bt_health_watchdog.sh`
   não diz uma palavra sobre ela: a linha 165 pula todo aparelho cujo cache de
   SDP já tenha `[ServiceRecords]`, e o 8BitDo tem o cache completo porque já
   conectou dezenas de vezes. Quatro passagens da vigia **depois** de o HID
   sumir, e nenhuma acusou. Isso **muda a mesa** de qualquer medição de externo
   — e a `IS-E4` da leva 0 pede exatamente deixar o 8BitDo uma noite no rádio.
   **Leva candidata: 0 ou 1**, como pré-condição declarada da `IS-E4`, ou a
   medição nasce contaminada.

4. **A QUATRO-NA-MESA-01 (defeito 1) e a QUATRO-NO-RÁDIO-01 (B4, B5) continuam
   ABERTAS desde 03/08.** **GRAU: MEDIDO.** A
   [A-LUZ-QUE-CUROU-01](2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
   as chama de *"a raiz medida disto tudo"* e registra que o preço delas
   **subiu**: de *"o número dança na tela"* para *"348 recusas de firmware"*. O
   veto da
   [QUATRO-NO-RADIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md)
   aparece na leva 10 **sem nome** (*"o veto de 19/07"*), e o defeito 1 da
   [QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md)
   não aparece de forma nenhuma — apesar de a LUGAR-À-MESA-01 escrever que *"a
   E3 não deveria entrar antes de a QUATRO-NA-MESA-01 ser lida"*. **Destino:
   leitura obrigatória declarada da LEVA 10.**

---

## 4. O que espera a palavra dela

**Isto não é trabalho: é decisão.** Cada linha traz a pergunta pronta. Nenhuma
delas deve ser respondida por quem executa.

| # | assunto | a pergunta, pronta |
|---|---|---|
| 1 | **a cadeia inteira** | *"Quando você disse 'só depois da máscara por controle', a máscara está pronta com a tela e o travessão (entregas 1, 2, 4 e 5), ou você quer as seis, incluindo a emissão das variáveis? A leitura da casa é a primeira — porque a sexta depende da adoção, e a adoção depende da máscara."* |
| 2 | **o ícone do painel** | *"São três desenhos: o novo, a opção C e o antigo. Qual fica?"* |
| 3 | **o preço da cura de segurança** | *"A RADIO-ABERTO-01 previu que a cura do pareamento cobraria um preço. Ninguém te perguntou se você aceita esse preço. Aceita, ou revemos a cura?"* |
| 4 | **a ordem da fila** | *"Hoje a fila é a ordem da PRIMEIRA VEZ que cada controle apareceu. Você descreveu a ordem da SESSÃO. Trocar revoga três decisões medidas de 25/07 — troco?"* |
| 4b | **quem obedece a quem** (a cura do cruzamento) | *"Para o número parar de mentir, as duas contas viram uma. Dá para fazer de dois jeitos: (1) a LÂMPADA passa a obedecer ao jogo, ou (2) o JOGO passa a obedecer à fila. O jeito 2 pode mudar quem é o Jogador 1 no meio da sessão. Qual você quer?"* |
| 5 | **os dois endereços de teste** | *"Tem dois endereços de teste dentro da sua fila real, restaurados a cada início do daemon, empurrando todo controle de verdade para o terceiro lugar. O cano já foi curado; a sujeira ficou. Apago?"* |
| 6 | **a faxina do `/tmp`** | *"São 911 alvos e 2,0 MB de sobra da suíte no seu `/tmp`. Rodo a faxina com `--apagar`?"* |
| 7 | **a marca do mic promovido à mão** | *"Quem promove o microfone à mão não deixa marca persistente — a variável morre com o terminal. Onde essa marca deve morar, e como se chama?"* |
| 8 | **o salva-vidas de pareamentos** | *"O salva-vidas de bonds é copiado e é apagado no desinstalar, e nada o aciona. Quem deve acioná-lo? (E antes disso preciso curar o restaurador, que hoje sobrescreve chave nova com chave velha.)"* |
| 9 | **o pin do DualSense** | *"O DualSense está pinado como fonte e saída padrão no `default-nodes`. Ninguém decidiu se isso fica. Fica?"* |
| 10 | **o restauro do hidraw** | *"O `--restaurar-hidraw-uaccess` fecha o nó e NÃO concede uaccess. Se você queria um comando que também concedesse, ele entrega metade. Qual dos dois você quis?"* |
| 11 | **o backtrace do BlueZ** | *"Para pegar o crash que derruba seu Bluetooth preciso gravar uma configuração GLOBAL do kernel (`kernel.core_pattern`) e esperar um crash acontecer. Autoriza?"* |
| 12 | **a página de Bluetooth** | *"O `docs/usage/bluetooth.md` atribui o crash à família errada e chama a issue de 'aberta'. As duas coisas caducaram. É página que você publica — corrijo com nota datada?"* |
| 13 | **a auditoria de 26/06** | *"A auditoria de 26/06 continua fora do git. Ela entra, ou a CLEAN-ROOM manda ela ficar de fora?"* |
| 14 | **a referência do Nintendo** | *"A referência canônica não fala do Pro nem do 8BitDo — zero linhas. Quer uma referência canônica própria para eles, com grau por linha? É trabalho grande."* |
| 15 | **as telas em outra língua** | *"Ligar o encanamento de tradução às telas é sprint grande: 15 dos 18 arquivos escrevem português direto no widget. Você já decidiu que português é a língua do produto. Confirmo que isso NÃO entra?"* |
| 16 | **a regra do OpenRGB** | *"Estreitar a regra do OpenRGB por aparelho é trabalho no seu self-heal, fora deste repositório — e estreitar às cegas apaga o RGB de algum periférico que ninguém listou. Quer que eu liste primeiro?"* |
| 17 | **o tema claro do ícone** | *"O tema claro só foi simulado; ninguém olhou a sua barra clara de verdade. Troca de tema um minuto para eu fotografar?"* |

**Grau: DECISÃO DELA** em todas, quando respondidas. **Grau: MEDIDO** que
nenhuma foi respondida até o fecho de 07/08 — exceto onde as respostas 13, 15,
16 e 17 do painel já fecharam o assunto, e essas **não** estão nesta lista.

---

## 5. O que espera o hardware na mão dela

**A ordem da cabeça já está decidida. Resposta 9 de 07/08: *"o protocolo de
06/08 primeiro"*. Grau: DECISÃO DELA.** Esse protocolo está em
[o que só fecha com o controle na mão dela](../estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md)
e tem **41 medições pendentes**, das quais **32 dão para fazer agora** com o que
está na mesa. **Nada do que 07/08 abriu passa na frente dele.**

### Depois dele, e nesta ordem

| # | o que | custo dela | por que nesta posição |
|---|---|---|---|
| 1 | **IS-E3** — régua de bateria do Pro: ele **não publica** percentual, só cinco degraus, e o amostrador lê o campo errado | **5 min** | **corrige um instrumento que gravaria "AUSENTE" a noite inteira** — vem antes da PR-Q1, ou a noite dela se perde |
| 2 | **o clique** (BUSCA-QUE-ESTOURA) — `dbus-monitor` mais journal, para saber qual método a interface dispara | **2 min** | destrava a cura A da leva 1; a previsão escrita é `Device1.Connect()` |
| 3 | **CR-10** — plugar um aparelho sabidamente bom na porta `usb 1-6` e ver se a rajada volta | **2 min** | tira o storm do repositório |
| 4 | **CD-1** — por que a confirmação de pareamento é recusada **com o agente vivo**, com contraste em `always` | **5 min** | **risco: mexer no agente com quatro conectados pode derrubar os quatro.** Fazer com a mesa vazia |
| 5 | **DC-6** — quatro protocolos: a troca de transporte (15 min) e os três curtos (a lâmpada do virtual, o padrão do Pro, e o cruzamento de olho) | ~30 min | o ramo do cruzamento tem a **palavra final dela**, e alimenta a leva 7 |
| 6 | **CR-P4** — por qual report o áudio SAI: `0x39` contra `0x32`, duas respostas incompatíveis na casa e nenhuma medida | **30 min** | **é o experimento mais barato da sprint mais cara**, e destrava a `CR-P5` |
| 7 | **IS-E2** — o pacote de 12 bytes que liga o giroscópio do Pro faz alguma coisa, ou é código morto? | **10 min** | exige o **Pro no cabo**; decide se o componente deve existir |
| 8 | **PR-Q1** — a bateria no fim explica as nove quedas? | **uma noite, sem atenção** | é a **única hipótese viva**, e depende do item 1 |
| 9 | **PR-Q3** — quem reconecta: ela ou o sistema? | **10 min de não tocar no controle** | pega carona na PR-Q1, e fecha sem cronômetro se a `PR-5` da leva 3 existir |
| 10 | **PR-Q2** — o daemon contribui para as quedas? | **uma noite sem o produto** | se a resposta for sim, **vira sprint de defeito** — e é o único caminho |
| 11 | **IS-E5** — o Pro esquece este host quando volta ao Switch? | **20 min, e repareamento** | **só vale se a PR-Q1, a IS-E3 e a IS-E4 não explicarem** (ver seção 6) |

### E a mais barata da fila, que entrou depois desta tabela

**A `P-4`, na metade que sobrou: a lightbar do 8BitDo chega às luzes do
plástico?** **Trinta segundos dela.** Não está na tabela acima porque depende
de o aparelho estar **ligado e no rádio**, e ele não está desde a saída de
19h38.

- **O que se faz:** escrever uma cor conhecida na lightbar dele (caminho `ds4`)
  e ela dizer se as quatro luzes de jogador do plástico mudaram.
- **O que decide:** se `write_lightbar_slot` **já numera** o 8BitDo, ou se
  escreve num lugar que não chega a lugar nenhum. **Bloqueia a numeração dele**,
  e a numeração é a linha de chegada das levas 8 a 11.
- **O que já está respondido:** ela olhou o aparelho às 21h06 — *"não há
  lightbar mas existe led de identificação de player nele também, igual o pro
  controller"*. A ausência de lightbar RGB **física** passou a MEDIDA; **quem
  acende as quatro luzes é o que sobra. GRAU: SEM PROVA.**
- **DECISÃO DELA (resposta 23):** *"preparar, e rodar quando ele estiver
  ligado"*. O preparo pode ser escrito agora; a rodada espera o aparelho.
- **A trava, e ela é a resposta 12:** hoje o produto **não escreve** em externo
  (`EXTERNAL_PLAYER_LED_ENABLED = False`), então esta medição é **de bancada**,
  fora do produto — e ainda assim ela **acende uma luz no plástico dela**. Não
  se arma sem ler a decisão 12 antes.

O protocolo, com o `P0` e a leitura do driver que o sustenta, está na seção 8.4
de
[os externos, a referência canônica](../../protocol/externos-referencia-canonica.md).

### E um protocolo que não custa atenção dela nenhuma: a `CURA-A/B-01`

**Grau: MEDIDO** o desenho; a medição não rodou. O A/B natural (luz falando
contra luz calada) **já aconteceu** e é o E-1 do estudo dos externos. **Falta o
A/B da CURA:** a escrita diferencial custa mesmo zero subcomando quando nada
muda?

**E o desenho é o achado:** o padrão que está no plástico agora **é exatamente o
que o slot pediria**. Então os dois primeiros braços escrevem **o que já está
lá** — nenhuma lâmpada muda, nada novo é afirmado, e **a resposta 12 fica
intacta**. A medição inteira acontece **sem que a tela dela mude e sem que o
plástico mude**.

**Quatro travas do `P0`, e as quatro são obrigatórias:** não reiniciar o daemon
(reiniciar zera o cronômetro do lado B); o portão continua `False` e a medição
**não passa pelo produto** — é bancada; **suíte parada**, porque ela suja o
journal e este protocolo lê o journal; e **anotar o denominador do rádio**
(quantos ACL, se está descobrindo, se a tela de Bluetooth do COSMIC está
aberta), sem o que a rodada não é comparável com nenhuma anterior.

### Três coisas que quem for medir carrega, e todas são MEDIDAS

1. **Quem cai é o DualSense; o Pro é o estável.** Pro: 3 links novos em 7 dias, o
   atual de pé havia 17h25m. DualSense: 8 instâncias distintas. **Qualquer leva
   que comece tratando "a queda do Pro" como o problema começa mirando o
   controle errado.**
2. **O gamepad virtual do Hefesto tem `power_supply` próprio**, e o histórico
   dele fica **ao lado** do controle de verdade, com nome parecido. Quem ler sem
   conferir o endereço pode medir o virtual e concluir *"bateria no fim"* com o
   controle cheio.
3. **Duas regras de instrumento, do protocolo de 06/08:** amostrar
   `daemon.state_full`, **nunca** `/sys/class/leds`; e `journalctl` **sempre com
   data completa** — `--since "23:20"` sem data devolve zero em todas as
   janelas, e zero em todas é sinal de instrumento quebrado, não de ausência de
   defeito.

### E uma medição de 20h que reordena o diagnóstico

**Grau: MEDIDO.** O ciclo do 8BitDo tentando entrar e sendo recusado **triplica**
a perda de IMU do Pro: 14,6 por minuto com a mesa estável, **48,4** durante o
ciclo. *"Não é a quantidade de aparelhos — é o aparelho que não consegue
entrar."* Um mecanismo explica quatro sintomas, e isso põe a leva 1 na frente de
qualquer trabalho de contenção de rádio.

---

## 6. O que não entra, e por quê

**Uma ordem que só acrescenta nunca termina.** Estes ficam de fora, e cada um
com o motivo escrito. Nenhum é apagado: todos continuam nas sprints de origem.

| o que | por que não entra |
|---|---|
| **a cura C da BUSCA-QUE-ESTOURA** (re-parear sozinho) | **nunca por decisão de máquina.** Um produto que apaga bond por conta própria pode apagar o certo |
| **a cura E** (mexer no rádio) | o que falhou — o controle responder — **não é nosso**. Mexer no page timeout só alonga cada falha |
| **EN-3** (exercitar as outras 55 ocorrências uma a uma) | exigiria **23 execuções isoladas** para medir o tamanho de um defeito cuja cura é de **três linhas** e já está na leva 3. O custo é do tamanho do trabalho que ele evitaria |
| **EN-6** (atribuir a ausência de driver de cpuidle ao firmware) | fechar exige **entrar na BIOS**, isto é, **reiniciar a máquina dela**. O prêmio é uma classificação |
| **EN-4** (aleatorização de ordem nos testes) | não há aleatorização hoje, então o defeito é determinístico. É **risco futuro registrado**, não trabalho |
| **RS-5** (o nó fechado **demais**) | declarado fora de escopo **por escrito**, para ninguém procurar aqui |
| **BT-5** (o canário ver **leitura**) | limite **estrutural** declarado na [CANARIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md). Não há desenho de outro mecanismo, e **inventar um aqui seria contrariar a casa** |
| **BT-4** (1,3 GB em pastas de teste) | é o mesmo assunto da `BT-7`, que é **gesto dela** (seção 4, item 6). Fazer por fora seria apagar coisa da máquina dela sem pedir |
| **LP-2** (ligar o i18n às telas) | é **G**, e a **resposta 10** já decidiu que português é a língua do produto. Construir a estrada agora é construir para lugar nenhum |
| **LP-1** (o `scripts/i18n_extract.sh` que destrói tradução manual) | **a cura não tem desenho.** O que cabe agora é **nota datada no próprio script**, avisando que o caminho documentado já custou 37 traduções. A cura de verdade espera o dia em que o i18n for ligado |
| **IN-4** (o `nix run` impossível) | **não há `nix` nesta máquina**, então a cura não pode ser verificada aqui. Entra só a nota datada, na leva 3 |
| **BZ-4** (esperar o BlueZ 5.88) | **não é trabalho, é gatilho.** O 5.87 tem quatro coisas que ela quer e uma que ela **não pode aceitar**. Quando o anúncio sair, a migração descarta os bonds — e ela repareia uma vez, **com ela presente** |
| **AP-5** (a cópia da logo dentro do tema dela) | o arquivo **não é nosso** e **nenhum portão deste repositório o vê**. Fica como **risco declarado**, não como entrega |
| **AP-3** (recompilar o binário Rust do applet) | a build do libcosmic é longa e **a máquina dela está em uso**. Entra na primeira janela ociosa, não numa leva |
| **a regra do OpenRGB por aparelho** | é trabalho no **self-heal dela**, fora deste repositório — e depende da pergunta 16 da seção 4 |
| **IS-E5** (o Pro esquece este host?) | **20 min e um repareamento de propósito**, para testar a hipótese mais cara. **Só vale se a PR-Q1, a IS-E3 e a IS-E4 não explicarem** as quedas. Se explicarem, este experimento nunca precisa acontecer |

### E o que expressamente NÃO tem caminho mais curto

**A luz.** O critério de volta é dela e é objetivo: a luz volta **quando a
entrega existir**. Encurtar isso é **repropor decisão medida**, e a casa proíbe.
**Grau: DECISÃO DELA.**

---

## 7. O placar, para não se perder

**Grau: MEDIDO** — contado sobre este índice.

| bloco | quantos itens | quanto custa |
|---|---|---|
| levas 0 a 3 (janela, defeito sentido, reavaliação, instrumento) | 25 | quase tudo **P**, uma **M** |
| levas 4 a 6 (máquina limpa, áudio, a mesa na tela) | 11 | **P** e **M** |
| levas 7 a 11 (cruzamento, máscara, pré-requisitos, adoção, luz) | 16 | duas **G** |
| espera a palavra dela | 18 | zero — é decisão |
| espera o hardware na mão dela | o protocolo de 06/08 (41 medições), mais 11, mais a `CURA-A/B-01` | ~85 min mais três noites |
| não entra | 15 | zero, e é o ponto |

**A primeira coisa a fazer amanhã é a leva 0**, porque é a única cuja janela
fecha sozinha.

**A segunda é a leva 1**, porque é a única coisa desta lista que ela sente na
mão hoje, e porque a causa já está medida.

---

## NOTA DATADA — 07/08/2026, 22h: seis frentes de produto, instalação e interface que esta ordem não pegou

**Nada aqui é entrega nova, e nada aqui é medição nova.** As seis já estavam
escritas e datadas nas sprints de origem, que continuam no repositório. O que
faltava era **roteamento**: este arquivo diz de si que é o ponto de entrada de
quem for executar, e quem entrar por ele amanhã não encontra nenhuma das seis.

**O mecanismo, e ele é MEDIDO por `grep -c -F` neste próprio arquivo, às 22h05,
antes desta nota:** este é um índice de 07/08. Treze sprints de 06/08 tinham
**zero** ocorrências pelo nome aqui — entre elas as cinco que abrem as frentes
abaixo, e é esta nota que passa a citá-las. O que dessas sprints chegou à
ordem chegou de carona nos inventários de 07/08 (os rótulos `EN-`, `BT-`, `IN-`,
`OQ-`, `CR-`, `RS-`, `PR-`, `IS-`, `CD-`, `BZ-`, `AP-`), nunca pela leitura da
lista de ABERTO da sprint de origem. Um caso mostra o mecanismo inteiro: a
[CONTROLE-INTEIRO-NO-RADIO-01](2026-08-07-CONTROLE-INTEIRO-NO-RADIO-01-o-mic-e-o-fone-que-nao-atravessam.md)
**está** citada aqui (leva 5) e, mesmo assim, o item 8 do "O que fica ABERTO"
dela não atravessou — a citação veio pela `CR-P0`, e o resto da lista ficou.

**Os códigos `PI-` são novos** e não renumeram nada: `grep -c -F '**PI-'` neste
arquivo devolvia zero antes desta nota.

**Sobre o placar da seção 7:** ele foi contado às 21h15, sobre o índice como
estava, e **não é reescrito aqui** — não se apaga contagem medida. Quem recontar
soma seis: três na leva 3, uma na leva 4, uma na leva 5, e uma que não tem leva.

### PI-1 (LEVA 4) — as três dívidas de máquina limpa que a sprint do rádio já marcou como bloqueio

**O que entra:** os três itens do "O que fica ABERTO" (item 8) da
[CONTROLE-INTEIRO-NO-RADIO-01](2026-08-07-CONTROLE-INTEIRO-NO-RADIO-01-o-mic-e-o-fone-que-nao-atravessam.md):

- o quirk `usbcore.quirks` é **opt-in** no `install.sh` (passos `3b` e `3e`) e
  **não entra no `.deb`** — conferido nesta árvore hoje: `grep -rn usbcore
  packaging/` devolve **zero**, e o `packaging/debian/postinst` existe;
- a **ponte de mic não tem gate em instalador nenhum** e **morre com o processo**
  que a subiu — conferido hoje: o nome só aparece em `src/` (nove arquivos, entre
  eles `daemon/subsystems/bt_mic.py`), e zero vezes no `install.sh` ou em
  `packaging/`;
- a **eleição de fonte** só não morde nesta bancada porque a pilha persistida do
  WirePlumber dela disfarça; **em máquina limpa não há pilha**.

**Por que na leva 4:** ela nasceu da **resposta 17** — *"produto: tem que
funcionar em máquina limpa"* — e é o único lugar da ordem cujo critério de
admissão é exatamente o critério que estes três violam. A sprint fecha com
*"nenhum dos três está pronto. Cura que só funciona nesta bancada é dívida"*.

**GRAU: MEDIDO** nos dois primeiros; no terceiro, **MEDIDO** o mecanismo e **NÃO
MEDIDO** em máquina limpa de verdade. **Custo: não estimado** — a sprint de
origem não estimou, e esta nota não inventa número.

### PI-2 (LEVA 5) — o áudio dela: a causa medida, e o pré-requisito que trava a cura

**Este item junta dois achados que são o mesmo fato por dois ângulos**, e por
isso não vira duas linhas na fila.

- **A causa.** O drop-in 51 rebaixa o mic do DualSense para
  `priority.session = 50`, abaixo de alto-falantes de 696 e 736 — numa máquina em
  que o controle é o **único** microfone, o monitor ganha a eleição. A
  [RECEITA-ERRADA-01](2026-08-06-RECEITA-ERRADA-01-o-doctor-mandava-rodar-o-que-nao-resolvia.md)
  fecha o ponto assim: *"o sintoma ficou honesto; a causa ficou"*. **GRAU:
  MEDIDO** (o rebaixamento e as três prioridades).
- **O pré-requisito que impede a cura de ser proposta.** A
  [SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md)
  declara, antes de qualquer entrega, uma medição que ninguém fez: se o
  `pipewire-pulse` faz a **própria** seleção quando a metadata está vazia, então
  zerar `default.audio.source` não muda o que `pactl get-default-source` devolve,
  e toda cura pelo lado do WirePlumber nasce inerte. **GRAU: SEM PROVA**, e é a
  própria sprint que se declara assim.

**A junção, declarada:** este é o mesmo assunto do terceiro item da `PI-1`, visto
do outro lado — lá é *"a cura não sobrevive a uma máquina limpa"*, aqui é *"a
política que fabrica o defeito continua de pé"*.

**Por que na leva 5:** a leva de áudio leva hoje **um** item (a `CR-P0`), e não
inclui a causa medida do defeito de áudio que ela **já sentiu**. O aceite da
sprint de origem já está escrito em cinco linhas, e a quinta é *"arrancar a cura
escolhida faz o teste reprovar"*.

### PI-3 (LEVA 3) — o `coop.py` ainda ensina o default que a decisão dela inverteu

**O que entra:** `src/hefesto_dualsense4unix/daemon/subsystems/coop.py:29` diz,
no bloco de pré-requisitos do `should_be_active`, que o co-op depende de
`config.coop_enabled` *"(default OFF — preserva o modo '1 player')"*. Esse
default foi invertido, e a nota datada que o declara caduco está a poucos
arquivos de distância: `daemon/lifecycle.py:151-165`, com `coop_enabled: bool =
True` na linha 165 e a fala dela citada no meio. Origem:
[FEAT-COOP-DEFAULT-ON-01](2026-08-06-FEAT-COOP-DEFAULT-ON-01-o-co-op-deixa-de-ser-opcao.md),
"O que fica ABERTO", primeiro item.

**Por que na leva 3:** o título da leva é *"o instrumento e a página param de
mentir"*, e esta é a página mais provável de ser lida por quem for executar as
levas **7** e **11**, que mexem no co-op — e ela contradiz uma decisão dela.

**GRAU: MEDIDO**, conferido nesta árvore hoje. **Tamanho:** uma linha de
docstring; a sprint de origem não pôs rótulo de custo, e esta nota não põe.

### PI-4 (LEVA 3, e ela depende da `AP-3`) — o painel dela diz o nome velho ao lado do nome novo

**O que entra:** o bloco de status do applet ainda diz *"Jogando direto (pelo
perfil)"* e *"Jogando direto (Sony)"* (`packaging/cosmic-applet/src/app.rs:610` e
`:612`), enquanto o **seletor do mesmo painel**, setenta linhas abaixo, já diz
*"Conexão Nativa (Sony)"* (`:682`). O portão de vocabulário não pega porque só
casa **listas de pares** — frase solta fica fora do alcance dele, e foi por aí
que o item sobreviveu. Origem:
[FEAT-COOP-DEFAULT-ON-01](2026-08-06-FEAT-COOP-DEFAULT-ON-01-o-co-op-deixa-de-ser-opcao.md),
itens 2 e 3.

**A dependência, e é ela que obriga este item a estar escrito aqui:** trocar o
texto no `app.rs` **não muda o painel dela** enquanto o binário não for
recompilado, e a seção 6 deixou a `AP-3` fora das levas **de propósito** (*"a
build do libcosmic é longa e a máquina dela está em uso"*, ver
[APPLET-MONOCROMATICO-01](2026-08-07-APPLET-MONOCROMATICO-01-o-icone-que-destoa-do-painel.md)).
Quem recompilar o applet na primeira janela ociosa sem ler isto vai recompilar o
nome velho.

**GRAU: MEDIDO**, conferido nesta árvore hoje.

### PI-5 (LEVA 3) — a lista de jogos dela mostraria cada jogo duas vezes

**O que entra:** `src/hefesto_dualsense4unix/integrations/steam_launch_options.py:815`
deduplica as pastas de biblioteca com `candidata not in pastas` — comparação de
`Path` que **não resolve symlink**. **MEDIDO hoje, nesta máquina:**
`~/.steam/steam` é symlink para `~/.steam/debian-installation`, logo a mesma
pasta entra **duas vezes** na lista devolvida por `pastas_steamapps`.

Os dois consumidores de hoje são imunes **por acidente da estrutura de dados**
(um acumula num `set`, o outro devolve no primeiro acerto), e é por isso que
ninguém viu. Mas qualquer lista de escolha construída iterando essa função —
que é o caminho óbvio, porque é o módulo que sabe traduzir nome — **mostra cada
jogo dela duas vezes**, e uma lista com tudo em dobro é pior que um campo de
texto: ela não sabe qual dos dois clicar. Origem:
[JOGOS-QUE-ELA-TEM-01](2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md),
`F3`, que fecha com *"uma linha, um teste, reversível sozinha. Vale mesmo que o
resto desta sprint nunca aconteça"*.

**Por que na leva 3:** é uma lista que ela lê, e ela mente. A sprint inteira está
fora da ordem — `grep -c -F 'Steam'` neste arquivo devolvia **zero** antes desta
nota —, e este passo é o único dela que **não** depende de decisão dela.

**GRAU: MEDIDO.**

### PI-6 (sem leva) — a recarga silenciosa que pode comer o que ela não salvou

**O que entra:** `src/hefesto_dualsense4unix/app/actions/profiles_actions.py:1702-1706`
— o `_refazer_as_abas_apos_ativar` pergunta *"há edição pendente?"* dentro de um
`contextlib.suppress(Exception)` com default `pendente = False`. Se o
`_tem_edicao_pendente` estourar ali, as abas são recarregadas **em silêncio** e o
que ela não salvou some — **sem** o diálogo que a
[ATIVAR-NAO-MENTE-01](2026-08-05-ATIVAR-NAO-MENTE-01-o-botao-que-parecia-falhar-e-ativava-duas-vezes.md)
criou justamente para dar essa decisão a ela, e cujo default é MANTER o que ela
não salvou (está no docstring da própria função, `:1697-1700`). Origem:
[NUNCA-TROCA-O-ALVO-01](2026-08-06-NUNCA-TROCA-O-ALVO-01-a-janela-trocava-o-nome-e-o-salvar-ia-para-o-arquivo-errado.md),
"O segundo `except` que ainda falha ABERTO".

**GRAU: SUSPEITA COM MECANISMO** — o caminho de código fecha; ninguém viu o
`_tem_edicao_pendente` estourar. **Esta nota não promove o grau.**

**Onde entra: não há leva de janela nesta ordem.** A mais próxima é a leva 6, e o
assunto dela é a mesa na tela, não os perfis. Fica **registrado sem alocação**:
a ordem é dela e tem travas que uma leitura de fora não deve mexer. O que não
pode continuar é o item viver só dentro de uma sprint que **nenhuma leva
retoma** — é perda de trabalho **dela**, sem aviso, que é a classe mais cara que
a casa tem.

### O que esta nota NÃO faz

Não propõe ordem, e não estima custo onde a sprint de origem não estimou. **Não
toca uma linha de código:** os cinco defeitos com caminho e linha acima continuam
vivos exatamente como estão, e a `PI-2` continua sem cura possível até a medição
que ela mesma exige. E não recolhe todos os órfãos de 06/08 — só os de produto,
instalação e interface.

**Grau desta nota: MEDIDO.** Cada `caminho:linha` citado foi conferido nesta
árvore em 07/08/2026, entre 22h e 22h30, por leitura pura: nenhum serviço foi
reiniciado, nada em `/etc` foi tocado, e a única leitura fora do repositório foi
um `ls -ld` no `~/.steam` dela.

---

## Nota de honestidade sobre este índice

Este arquivo foi escrito por **leitura pura** da árvore, das oito sprints e dos
cinco estudos de 07/08, dos dois arquivos de decisão do dia, e das sprints-mãe
de 06/08 e 25/07. **Nenhum serviço foi reiniciado, nenhum controle foi
derrubado, nada em `/etc` foi tocado.** As afirmações sobre o código foram
conferidas contra esta árvore com `grep` — e três delas mudaram de linha desde
o inventário que as levantou, o que está corrigido acima.

**O que este índice NÃO tem:** entrega inventada. Onde uma frente está aberta
**sem desenho** — a cura do `scripts/i18n_extract.sh`, o mecanismo alternativo
do canário — está escrito *"sem desenho"*, e a leva correspondente começa pelo
desenho. Imaginar a solução aqui seria contorno, e contorno é gambiarra.

**Uma sprint nasceu depois deste índice e foi encaixada nele.** A
[A-LUZ-QUE-CUROU-01](2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
foi escrita em paralelo, recontou os números na máquina dela viva e trouxe duas
coisas que **mudaram esta fila**:

1. **a cura do cruzamento deixou de ser "sem desenho"** — ela é a saída `S9`, com
   dois caminhos e a escolha pendente (pergunta 4b da seção 4). O texto anterior
   deste índice, que a dava por não desenhada, **está corrigido na leva 7 e
   permanece registrado aqui**, porque não se apaga o que já foi escrito;
2. **a trava "nenhuma cura de luz entra antes da cura da numeração"**, que
   promoveu a leva 7 de "leva de valor próprio" a **pré-requisito da leva 9**.

**Grau: MEDIDO** que as duas mudanças vieram daquela sprint, e não desta leitura.
