# O QUE FICOU ABERTO-01 — e como cada um fecha

- **Escrito em:** 16/08/2026, depois de uma bancada de cerca de oito horas com
  ela e um DualSense no rádio.
- **O que este documento é:** a continuação do
  [PONTO A PONTO-01](2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md),
  escrita no fim do dia. Para cada frente que **continua aberta**: o que se
  sabe, o que falta, **quem decide** e — a parte que importa — **como o portão
  vai morder** quando fechar.
- **O que este documento NÃO é:** medição nova. Nada aqui foi medido no
  aparelho por esta passagem. Nenhum `/dev/hidraw` foi aberto, nenhum byte foi
  escrito em controle nenhum, o daemon não foi reiniciado e a Steam não foi
  aberta. O que é leitura de código está marcado **`inferido-do-codigo`**; o
  que é medição do dia vem com o endereço do documento que a registrou.
- **Fontes:**
  [O RÁDIO MEIO MUDO](../estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md),
  [O PS PRESO](../estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md),
  [O QUE A STEAM COME EM SILÊNCIO](../estudos/2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md)
  e o próprio código da árvore de hoje.

---

## A frase dela, que é o requisito deste documento

> *"me preocupa o fato de serem regressões e me preocupa o fato de que isso
> possa voltar no futuro."*

Ela não pediu conserto. Pediu **garantia de não-volta**. São coisas diferentes,
e só a segunda tem preço: um teste que morde. Por isso cada item abaixo termina
no mesmo lugar — a mordida, escrita com detalhe suficiente para outra pessoa
construir sem me perguntar nada.

## O que o dia ensinou sobre portão, e vale para todos os itens

Três portões desta casa passaram **verdes com o defeito vivo**. Não é azar: são
três modos de falha distintos, e cada um vira uma regra.

| o modo de falha | o caso medido em 16/08 | a regra que fica |
|---|---|---|
| **portão que CONTA em vez de NOMEAR** | `hidden_count` do broker; o contador de 76 jogos que a árvore viva não tinha | veredito nunca sai de um inteiro. Sai de **comparação de conjuntos**, e imprime **quem** sobrou de fora |
| **portão que olha a ÁRVORE ERRADA** | o censo lia o bloco `apps` que a Steam não lê | toda régua declara **de onde** lê, e a âncora vale nos dois lados da comparação |
| **portão de ESTADO ESTÁTICO num defeito de TRANSIÇÃO** | havia teste para a perda do fd e para o estado parado; nenhum para o **ciclo** perde-renumera-volta | defeito de transição só se prova exercitando a transição |

O terceiro é o que deixou a reconexão BT passar meses. É o mais caro dos três
porque um portão verde **encerra a busca** — e a busca encerrada foi retomada,
dias depois, do zero.

---

# A ordem, e por que ela é esta

Ordenado por **quanto custa a ela por dia**, não por facilidade de conserto. Um
item que estraga a sessão vem antes de um item que estraga um diagnóstico, e um
item que estraga um diagnóstico vem antes de um que estraga uma feature que ela
ainda não usa.

| # | frente | custo por dia | quem decide |
|---|---|---|---|
| 1 | a reconexão BT que mata a entrada | a sessão inteira, em qualquer jogo | ninguém: é defeito |
| 2 | o freio que não existe (PS em laço) e o `wmctrl` ausente | Steam abrindo sozinha; e o susto, quando dispara | ninguém no freio; **dela** o que a janela mostra |
| 3 | os portões cegos (`hidden_count`, bonds) | zero em dia bom; multiplica o custo de 1 e 2 em dia ruim | ninguém: é defeito de instrumento |
| 4 | o alto-falante no rádio: o grau contra a memória dela | uma dúvida que volta toda vez que o assunto aparece | **dela** — a orelha é a régua |
| 5 | a ponte do mic BT | zero hoje (está desligada); e uma feature parada | **dela**, e ela já decidiu como decidir |
| 6 | parear físico × virtual campo a campo | zero direto; sem ele "o vpad é fiel?" é opinião | **dela** o quanto vale o instrumento |
| 7 | o touchpad engasgando | não medido; o primeiro suspeito sou eu | ninguém até medir |
| 8 | Duskfade | um jogo, que nunca funcionou | **dela** a prioridade |

---

## 1. A reconexão BT que mata a entrada — P0

### O que se sabe, e está medido

O controle cai e volta no rádio (ou sai do cabo para o rádio) e o daemon
**nunca reabre os leitores**. Segue publicando `connected=True` com os eixos
congelados, enquanto o vpad emite 396 reports em 8 s com a sequência perfeita e
`LX` travado em 128. Para o jogo, um controle vivo que nunca se mexe — daí
*"recebeu um pouco de input e morreu"*, em três jogos. Está inteiro em
[O RÁDIO MEIO MUDO](../estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md).

### O que já FECHOU hoje, e é metade do trabalho

O `EvdevReader` está **eliminado como suspeito, com portão permanente**:
`tests/unit/test_reconexao_bt_01_o_leitor_tem_de_voltar_sozinho.py`, três
testes, que exercitam o ciclo inteiro — abre no nó velho, o nó some, volta com
outro número. **Rodados de novo nesta passagem: 3 passaram em 4,15 s.** O leitor
de evdev reabre no nó novo, não insiste no número velho e sobrevive ao sumiço
prolongado.

Isto vale tanto quanto uma reprovação: é o primeiro portão de **ciclo** desta
casa, e ele fecha um suspeito para sempre. O que ele **não** cobre são os outros
dois leitores e o probe — e é exatamente aí que sobrou o defeito.

### O que falta, com endereço

**a) O `motion_reader` depende do broker, e o caminho dele é outro.**
`motion_reader_open_failed errno 2 /dev/hidraw5` sai em
`core/physical_report_reader.py:759`. O laço dele (`_run`, a partir da linha
744) re-resolve o alvo pelo `_path_provider` e reabre com backoff — o desenho
está certo. O que ninguém provou é o **ciclo com o broker no meio**: o opener
pode ser o broker-aware (`integrations/hidraw_broker_client.py`), e um broker
que devolva um fd de um nó que já morreu produz exatamente este `errno 2`.

**b) `controller_disconnected reason=probe_offline`**, em
`daemon/connection.py:546-551`. O probe marca offline; se ele não refizer a
reconciliação, não adianta leitor nenhum estar de pé.

**c) `primary_grab_state=pending`, e este é o mais informativo dos três.**
Grau: **`inferido-do-codigo`**. Em `core/evdev_reader.py:1203` e `:1250` o
estado `pending` tem uma definição literal: *"pedido, device ainda não
aberto"*. Ou seja, o estado que ela viu ao vivo, com a entrada morta, é a
afirmação de que **o device de evdev não estava aberto naquele instante** — e
não que o grab tinha falhado. Isso não contradiz os três testes acima: eles
provam que o laço reabre quando a descoberta devolve um nó; `pending`
persistente diz que a descoberta **não estava devolvendo nó nenhum**. O próximo
fio é `find_dualsense_evdev` (`core/evdev_reader.py:404`) depois de uma
reconexão de rádio, não o laço de reabertura.

### O fio solto que este documento estreita

O estudo deixou aberto: *"o `motion_reader` cicla a cada 30 s em silêncio e o
giroscópio chega ao vpad assim mesmo — um dos dois fatos está mal entendido."*

Grau: **`inferido-do-codigo`**, e estreita sem resolver. O giroscópio do vpad
tem **uma fonte só** no código: o `PhysicalReportReader`, que copia a fatia crua
do report físico (`daemon/subsystems/gamepad.py:1634`, e o espelho em
`integrations/uhid_gamepad.py`). Os leitores do `daemon/sensor_hub.py` — o
`MotionSensorReader` do `event27` e o `TouchpadReader` — alimentam **só** o
painel do `state_full`, nascem sob demanda da janela e morrem 5 s depois do
último pedido (`sensor_hub.py:50-53`). Eles **nunca** escrevem no vpad.

Logo: *"o motion_reader está em silêncio"* e *"o giroscópio chega ao vpad"* não
podem ser verdade **no mesmo instante**. As duas medições são de momentos
diferentes, e a leitura de que existiriam "dois caminhos de leitura para o vpad"
está errada. **Isto não é medição** — é o que o código diz. A medição que
resolve é a do item 6.

### Quem decide

**A cura, ninguém**: é defeito, e a regra dela de 09/08 já responde — cura no
daemon, sem clique, e chega no install por consequência.

**Decisão dela, uma só, e é de interface:** o que a janela mostra quando o
estado está degradado. Hoje ela mostra "conectado". As opções vão de um selo no
cartão do controle até recusar o "conectado". É a regra do olho dela
(PROVA-DE-TELA-01) — não se fecha sem foto e sem a palavra dela.

### Como o portão morde

**Três portões, e nenhum é o que já existe.**

**1.1 — O ciclo do leitor de movimento, com o broker no meio.**
Molde pronto: o mesmo do `test_reconexao_bt_01`, trocado o sujeito. A bancada
entrega um `_path_provider` que devolve `/dev/hidraw5`, depois `None`, depois
`/dev/hidraw6`, e um opener falso que levanta `OSError(2)` no caminho morto. A
asserção é que o reader **abre o nó novo sozinho**, dentro de um teto de tempo.
**A mordida se prova arrancando o `_resolve_path` de dentro do laço** (fixando o
caminho na primeira resolução): o teste tem de ficar vermelho.

**1.2 — A mentira do `state_full`, e ela é a mais barata das três.**
Em `daemon/ipc_handlers.py:2142` o daemon já **sabe** dizer que está estagnado
(`state_stale_neutral_warning`) — e sete linhas abaixo, em `:2149`, o mesmo
dicionário publica `"connected": True`. **O aviso e a mentira saem do mesmo
payload.** O portão monta um `state` neutro (sticks em 128, gatilhos em 0,
`buttons` vazio) com o controller respondendo conectado, chama
`daemon.state_full` três vezes e **reprova se o resultado disser
`connected=True` sem nenhum campo que denuncie a estagnação**. Arrancamento: é o
código de hoje — o portão nasce vermelho, o que é a melhor prova de mordida que
existe.

Uma ressalva que o portão precisa carregar escrita: **esse aviso não é
watchdog**. Ele nasce dentro do handler do IPC e conta *chamadas do
`state_full`*, com limiar de 3. Com a janela fechada ninguém chama, ninguém
conta, e o daemon fica estagnado em silêncio absoluto. Quem for usar o
`state_stale_neutral_warning` como gatilho de reabertura tem de mover a contagem
para o laço do daemon primeiro — senão a cura só funciona quando ela está
olhando.

**1.3 — O `pending` que dura.** Um teste que reprove se `primary_grab_state`
ficar em `pending` por mais que um teto curto com o gamepad ligado. Hoje
`pending` é indistinguível, para quem lê o estado, de "está tudo bem" — e ele
significa "não há device aberto".

---

## 2. O freio que não existe, e o `wmctrl` ausente — P0

Duas metades do mesmo episódio das 20h19, e elas se separam limpo: uma é o
**gatilho** (a ponte do mic, item 5, hoje desligada), a outra é a **ausência de
freio**, que continua armada para qualquer gatilho futuro.

### 2.1 O PS preso vira enxurrada de janelas

**Verificado no código nesta passagem.** O caminho é
`daemon/subsystems/hotkey.py:52-55` → `open_or_focus_steam()`, e o disparo vem
de `integrations/hotkey_daemon.py:220-224`, no release do PS. Entre o release e
o `Popen` da Steam **não há debounce, não há teto de tentativas, não há "já pedi
isto há 200 ms"**. Os gates que existem ali são de outra natureza — Modo Nativo
e modo jogo (`hotkey.py:46-51`) — e nenhum deles limita **frequência**.

Medido em 16/08: `held_ms` de 17,6 / 17,5 / 17,9 ms em sequência. Mão nenhuma
faz isso; 17 ms é o intervalo entre reports a 60 Hz. O botão apareceu
pressionado por exatamente um ciclo de leitura, repetidamente.

**Por que isto é P0 mesmo com a ponte desligada:** o freio protege contra
*qualquer* fonte de estado de botão corrompido, e o dia produziu uma que ninguém
tinha previsto. A ponte foi o gatilho conhecido. O freio é a cura.

### 2.2 Sem `wmctrl`, "focar" vira "abrir" — e isso custa todo dia

Em `integrations/steam_launcher.py:83` a ausência do binário vira
`wmctrl_binary_not_found`, um `warning` que ela nunca vê; em `:173-179`, o
`_focus_steam_window` que devolve `False` cai no `_spawn_steam`. **Com a Steam
já aberta, cada toque do PS pede um processo novo em vez de trazer a janela para
frente.**

**Verificado nesta passagem, e é somente-leitura:** `wmctrl` não está no `PATH`
desta máquina, e não aparece em `install.sh`, em `scripts/doctor.sh` nem no
empacotamento. O produto depende de um binário que ele nunca pede.

**A ressalva que impede a cura errada, e ela é o achado desta seção.** Grau:
**`inferido-do-codigo` mais leitura do ambiente**. Esta sessão é
`XDG_SESSION_TYPE=wayland`, `XDG_CURRENT_DESKTOP=COSMIC`, com Xwayland em `:1`.
O `wmctrl` é ferramenta **X11**: ele só enxerga janelas que passem pelo
Xwayland, e nada do que for nativo Wayland. Se a Steam roda sob Xwayland aqui,
instalar o `wmctrl` pode funcionar — **e isso é `incerto`, ninguém mediu**.
Portanto: *"basta declarar a dependência"* é uma resposta que pode ser falsa
nesta máquina, que é a máquina dela. Medir antes de empacotar.

### Quem decide

**O freio, ninguém**: é defeito, e a cura é de daemon.

**Dela, duas coisas.** Primeira: *"o `wmctrl` ausente tem de aparecer para ela"*
— onde, e com que texto. Segunda, e maior: se a resposta certa é **declarar a
dependência** ou **trocar o mecanismo** por um que fale com o COSMIC. A segunda
é mais cara e é a única que sobrevive a um desktop Wayland puro. Não decido isso
por ela.

### Como o portão morde

**2.a — O freio.** Um teste que aciona o PS solo N vezes dentro de uma janela
curta e exige **uma** chamada a `open_or_focus_steam` — com um relógio injetado,
nunca `sleep` real. A mordida: com o debounce arrancado, o teste conta N e
reprova. Vale escrever no mesmo arquivo o caso do dia: dez disparos com
`held_ms` na casa dos 17 ms.

**2.b — Nenhum atalho abre programa sem freio.** O portão mais valioso dos dois,
porque protege o que ainda não existe: uma varredura que enumere os disparadores
de ação de janela e reprove aquele que chame `Popen` sem passar por um limitador
de frequência. É irmão de
`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`, que já faz varredura de
AST sobre a árvore e é o molde a copiar.

**2.c — A dependência que o produto não pede.** Um portão que reprove se
`integrations/steam_launcher.py` nomear um binário externo que nem o `install.sh`
declara nem o `scripts/doctor.sh` confere. Ele nasce vermelho hoje, no `wmctrl`,
e passa a proteger os próximos. **Este é o portão de maior alcance do
documento** — a família inteira de "o produto depende de algo que ninguém
instala" cabe nele.

---

## 3. Os portões cegos — P1, e é o item que barateia todos os outros

O censo de
[O QUE A STEAM COME EM SILÊNCIO](../estudos/2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md)
varreu os 61 `check_*` do `scripts/doctor.sh` mais os portões de shell da lista
de fechamento e achou **três** contadores que decidem veredito. Um foi curado
hoje (o contador de jogos com wrapper, commit `dca7170`). **Dois continuam de
pé.**

### 3.1 `hidden_count` do broker — o mais grave

**Medido por leitura de código.** Em `scripts/doctor.sh:3109` o doctor recebe do
broker a **lista** dos nós escondidos e imprime `hidden_count=len(hidden)`. A
lista morre ali. Cerca de cento e quarenta linhas depois, em `:3245-3251`, o
veredito é
`hidden_count > 0`, e o texto verde diz, com todas as letras, *"o jogo só vê o
vpad"*.

Com dois DualSense na mesa e o broker escondendo **um**: `1 > 0`, verde, e o
jogo do P2 vê dois controles. O sintoma é o defeito histórico mais caro desta
casa — o controle dobrado no jogo — e o portão que resolveria em um segundo diz
que está tudo bem, mandando a investigação para o `IGNORE_DEVICES`, para o Steam
Input e para o espelho Xbox da Steam.

**A cura, desenhada e não construída:** trocar `len(hidden)` pela lista, e o
veredito por **comparação com o censo de físicos** — o produto já sabe
enumerá-los (`src/hefesto_dualsense4unix/broker/hidraw_broker.py`,
`validate_physical_node`). O `pass` só é honesto quando `escondidos == físicos`.

**Como o portão morde:** dois físicos na fixture, um escondido. O doctor de hoje
passa; o curado **nomeia o que sobrou de fora**. A mordida é a fixture, e ela é
barata.

### 3.2 `check_bt_bonds_persistidos` — a régua de 22/07 na pergunta de hoje

**Medido por leitura de código**, `scripts/doctor.sh:2827-2842`. O portão conta
os `info` em disco e passa com `n_info > 0`. Ele nasceu para pegar uma
assinatura **total** (cache populado com ZERO bonds), e para aquela pergunta a
régua está certa.

O estado que ela vive é **parcial**: quatro controles na mesa, o bond de um
evaporado, `n_info=3`, `3 > 0`, verde — *"bonds BT persistidos em disco: 3
(cache com 7 devices vistos)"*. **A prova do defeito é impressa dentro da frase
de aprovação**, como tranquilizante. E o sintoma — *"um controle específico
parou de reconectar sozinho depois do boot"* — é a trilha em que esta casa mais
gastou tempo.

**A cura:** nomear os MACs que têm `cache/` **sem** `info/` — a diferença de
conjuntos, não a de contagens.

**Ressalva de anonimato, e ela é obrigatória:** o resultado sai na tela dela e
**nunca** em arquivo versionado. Se algum dia for para arquivo, vale a máscara
da casa (octetos 4 e 5 zerados), e há portão que reprova.

**Como o portão morde:** uma árvore de mentira com dois `cache/` e um `info/`. O
doctor de hoje passa em verde; o curado reprova e **diz qual MAC** perdeu o
bond.

### Quem decide

Ninguém: instrumento que mente é defeito de instrumento. A única decisão dela é
de prioridade, e a recomendação é fazer o 3.1 **antes** de investigar qualquer
suspeita de controle dobrado — senão a investigação começa cega.

### O que este item recusa recomendar

**Varredura periódica atrás de contadores.** Foram três em setenta e poucos
portões, e a maioria esmagadora nomeia com esmero. O que a casa precisa é da
regra escrita na hora de criar portão novo — *o veredito sai de conjuntos,
nunca de um inteiro* — e dos dois consertos acima. Uma varredura recorrente
seria custo sem achado.

---

## 4. O alto-falante no rádio: o grau contra a memória dela — P1

### A discordância, textual

> *"a minha certeza do lance do som no bt do speaker do dualsense, o claude
> tinha feito funcionar quando testávamos no pragmata. Eu simplesmente esqueci
> isso e achei que tivéssemos resolvido em definitivo."*

E o `docs/data/mapa-controles.csv` de hoje, nas três linhas de áudio do
DualSense:

| linha | `radio_aciona` | `radio_de_onde_sei` |
|---|---|---|
| `audio.alto_falante` | **não** | `inferido-do-codigo` |
| `audio.alto_falante.rota` | sim | `inferido-do-codigo` — *"não medido por BT"* |
| `audio.alto_falante.volume` | sim | `inferido-do-codigo` — *"NÃO MEDIDO por BT"* |

### O que já se sabe, e muda a forma da pergunta

Duas coisas mudaram desde que essa memória se formou, e as duas estão no CSV:

1. **No cabo, a causa está isolada por dose-resposta**, com a orelha dela em
   15/08: sem ninguém escrever volume o alto-falante fica mudo; com
   `speaker volume 85` o mesmo comando na mesma rota soa; com volume 0 volta a
   calar. O culpado é a posse dos bytes de volume, e é a mesma família do
   keepalive que cancelava o rumble.
2. **No rádio não há caminho de dados de áudio implementado.** O `BLOCO_SPEAKER`
   está declarado em uma linha de
   `src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py` e não é
   referenciado por nenhum caminho de escrita. O que existe por rádio é a
   escada de OUTPUT (`0x32` a `0x39`), cujo **conteúdo do payload segue sem
   identificação**.

Isso reformula a pergunta, e a reformulação é o produto desta seção: **o que ela
lembra pode ter sido volume e rota respondendo por rádio — que é coisa
diferente de PCM saindo pelo alto-falante por rádio.** As duas memórias são
compatíveis com o CSV se o que soou naquele dia era o som do *sistema* por outro
caminho, com o Hefesto mexendo só nos registradores. **Não sei qual das duas
foi, e não invento.**

### Por que isto não é papelada

A memória externa dela são as specs. Um grau errado no CSV não é imprecisão de
documento: é uma lembrança dela guardada no lugar errado, que vai contradizê-la
na próxima vez que o assunto aparecer — e já contradisse hoje.

### Quem decide

**Ela, e só ela.** A orelha dela é a régua, e a casa já registrou por escrito o
episódio em que um agente enfraqueceu uma medição dela por não ter medido no
mesmo dia. A regra que ficou: *"não medi hoje" NÃO é "não está medido"*.

### Como o portão morde

Este é o item cujo portão **não é um teste de Python**, e vale dizer por quê: o
que precisa não voltar é o **grau**, não o comportamento.

**4.a — O ensaio, quatro minutos, e ele já tem forma.** Repetir no rádio o mesmo
par com/sem que isolou a causa no cabo — mudo, `volume 85`, `volume 0` —
mudando **uma variável**, com o gesto isolado (a regra que este dia
acrescentou). O resultado promove a célula para `medido` **ou** registra que a
memória caducou, com data. Os dois desfechos são vitória; o empate é o único
que não vale nada.

**4.b — O portão que já existe e precisa alcançar esta linha.**
`scripts/check_paridade_transporte.py` reprova afirmação forte sem teste que a
sustente. O que falta é o inverso: reprovar **célula com `provado_por:
olho-dela` cujo grau seja `inferido-do-codigo`** — a assinatura exata de uma
medição dela perdida no caminho. É uma consulta ao CSV, e nasce nomeando as
linhas.

**4.c — A dívida vizinha, que não é deste sprint mas some junto se ninguém
olhar.** O CSV registra que quem hoje salva o canal esquerdo do alto-falante é a
conversão 2→4 do PipeWire, e que isso é **política dele**, não garantia do
aparelho: um jogo que emita quatro canais nativos perde metade do som. Enquanto
a soma L+R não estiver escrita no produto, o áudio do controle funciona por
acidente feliz. Fica citado aqui para não se perder.

---

## 5. A ponte do mic BT — P1, e a decisão dela já tem resposta

### O que se sabe

A ponte **funciona** (publica o source) e **não é segura**: com ela de pé, o
botão PS dispara em pulsos de cerca de 17 ms e o daemon tenta abrir a Steam em
laço. **Testado duas vezes em 16/08**, a segunda já com o filtro do bit de áudio
no daemon (reiniciado às 21h04, conferido) — travou em 10 segundos, 10 disparos.

**O que isso derruba:** a hipótese de que bytes de Opus caindo sobre o byte de
botões explicavam o travamento. O filtro está no lugar, provado por 13 testes
(`tests/unit/test_ps_preso_01_audio_lido_como_botao.py`, commit `702f5b6`), e o
travamento voltou igual. **O filtro continua certo e fica** — áudio lido como
input é defeito com ou sem este travamento. Ele só não era esta causa.

### O suspeito que sobra, e a contradição que ninguém mediu

A disputa do contador de sequência do report `0x32`. A ponte manda `seq=1`,
começando do zero (`integrations/dualsense_bt_audio.py:1011-1019`), enquanto o
daemon mantém a própria sequência.

**E aqui há uma contradição dentro da própria árvore, que registro porque ela é
o alvo do ensaio.** O cabeçalho de `dualsense_bt_audio.py:55-70` argumenta que a
disputa é **estruturalmente mitigada**: são report IDs diferentes (`0x31` do
kernel, `0x32` nosso), o SDL manda `0` fixo desde sempre, e a escrita é
parcimoniosa — só na borda. O comentário do MIC-BT-01 no widget do cartão diz o
oposto: que a ponte *"disputa o contador de sequência do report `0x32` com o
driver"*. **As duas afirmações estão no repositório, nenhuma foi medida com a
sequência dos dois lados no mesmo instante, e o travamento é o dado que o
argumento do cabeçalho não explica.** Uma hipótese tem de explicar o que já
funcionava — e o cabeçalho não explica por que trava.

Há ainda a disputa do **nó**: a ponte lê `/dev/hidraw5`, o mesmo de onde o
leitor de movimento lê, e não há arbitragem — o broker entrega o fd para quem
pedir. A correlação temporal é forte; **o mecanismo exato não foi isolado**.

### O risco de hoje é baixo, e é bom saber por quê

**Verificado no código nesta passagem:** a ponte é opt-in por
`HEFESTO_DUALSENSE4UNIX_BT_MIC=1` ou por `DaemonConfig.bt_mic_enabled`
(`daemon/subsystems/bt_mic.py:23,58,79`), e esse campo **não tem escritor** em
lugar nenhum de `src/` — a janela não a liga. Ela subiu hoje porque **eu** a subi
à mão. O custo por dia, portanto, é zero — e é isso que a coloca abaixo dos
itens 1 a 4, não a gravidade.

### Quem decide

**Ela**, e ela já decidiu o método: *"testar primeiro, decidir depois"*.
**Testado. O veredito é: não sobe.** A ponte não sobe sozinha e não entra no
caminho automático da interface enquanto a sequência do `0x32` tiver dois donos.

O que continua sendo decisão dela é se vale gastar bancada para destravar a
ponte — é uma feature que ela quer, e o preço agora está na mesa.

### Como o portão morde

**5.a — A arbitragem do nó, e é a cura de raiz.** O broker é o dono da posse: um
teste que peça o mesmo nó duas vezes e exija que o segundo pedido seja
**recusado ou multiplexado**, nunca servido cru. Arrancamento: com a arbitragem
fora, o teste recebe dois fds e reprova. Este portão fecha a classe inteira, não
só a ponte.

**5.b — O gate que não pode se abrir sozinho.** Um teste que reprove se
`bt_mic_enabled` ganhar um escritor em `src/` sem que o portão 5.a exista. É o
inverso do
`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`: ali a dívida é a promessa
sem caminho; aqui o perigo é o caminho **antes** da segurança.

**5.c — A regra que o episódio deixou, e ela é de método.**

> **Instrumento que ESCREVE ou que toma posse de um recurso não é instrumento —
> é mudança de estado.** Só entra com o mesmo cuidado de uma cura: uma variável
> por vez, e com o caminho de volta pronto ANTES.

A casa **tinha o aviso escrito** — no comentário de um widget — e eu subi a
ponte assim mesmo, duas vezes. Um aviso que mora só no comentário de um widget
não alcança quem está mexendo no módulo de integração três diretórios adiante.
**O portão é o lugar onde um aviso desses passa a alcançar.**

---

## 6. Parear físico × virtual campo a campo — P1

### O que se sabe: hoje foi meio caminho

Foram medidos lado a lado, com o controle na mão dela:

| canal | vpad | físico |
|---|---|---|
| gamepad | 286 ev/10 s | 0 (grab, correto) |
| giroscópio | 7 231 | 19 435 |
| touchpad | 2 807 | 3 660 |

E no report HID de 64 bytes do vpad, os bytes que variam são
`2,3` (eixos) · `7` (sequência) · `16-27` (giro/acel) · `28-32` (timestamp) ·
`33-36` (touchpad).

Isso derrubou duas hipóteses — a dos flags de validação e a de "o vpad está meio
mudo". **O repasse está íntegro pelos dois caminhos.**

### O que falta: virar instrumento

Amostragem não responde **por que o giroscópio do vpad tem cerca de 37% dos
eventos do físico**. Pode ser decimação legítima (há janela e teto de emissão no
caminho do vpad) ou perda. **Ninguém mediu**, e a diferença importa: decimação é
projeto, perda é defeito.

**O que existe hoje e não serve:** `scripts/ensaios/taxa_de_entrada.py` mede
taxa, não correspondência; `scripts/ensaios/byte_no_fio.py` compara dois
aparelhos no ar, não físico contra virtual. Nenhum instrumento desta casa captura
os dois reports **no mesmo instante** e diz, campo a campo, o que entrou e o que
saiu.

### O que este instrumento resolve de brinde

Ele é a régua que fecha o fio solto do item 1: com físico e virtual carimbados
no mesmo relógio, *"o motion_reader está em silêncio e o giroscópio chega"*
deixa de ser um paradoxo entre duas medições de horas diferentes.

### Quem decide

**Ela**, e a decisão é de preço: quanto de bancada vale um instrumento que
transforma *"o vpad é fiel?"* de opinião em pergunta com resposta. A ideia é
dela; o custo é meu de estimar e dela de aprovar.

**Aviso que a decisão precisa carregar:** este instrumento **lê** dos dois lados
e não escreve em lugar nenhum — logo, é instrumento de verdade pela regra 5.c.
Mas ele disputa leitura de nós que o produto está lendo, que é a armadilha nº 3
da casa e o suspeito número um do item 7. Ele mede com o daemon **de pé** (é o
único jeito de haver vpad), então tem de declarar isso e medir a si mesmo.

### Como o portão morde

Um instrumento não é código de produção, e a mordida dele é diferente: **o
portão prova a RÉGUA, não o produto.**

**6.a — A régua contra contagem independente.** É a lição de
*"o instrumento mente mais que o produto"*: alimentar o instrumento com um par
de capturas sintéticas de correspondência **conhecida** e exigir o veredito
certo. Sem isso, o primeiro número que ele produzir vira fato.

**6.b — O caso do gesto composto, escrito no teste.** A regra que este dia
acrescentou nasceu de um zero falso: *"gire o controle e passe o dedo"* produziu
`0/8 bytes variam` no touchpad, e quase virou acusação ao produto. O portão do
instrumento tem de reprovar quando a captura contiver mais de um gesto — ou, no
mínimo, marcar a saída como não conclusiva.

**6.c — A decimação declarada.** Se a medição disser que os 37% são projeto, o
número vira **limiar** no portão: uma faixa esperada, com o motivo escrito. Aí
uma regressão que derrube o giroscópio para 5% reprova sozinha, e é exatamente o
tipo de defeito silencioso que hoje ninguém pegaria.

---

## 7. O touchpad engasgando — P2

### O que se sabe

Relato dela, durante a bancada: *"durante os testes notei que tava tipo
engasgando. aí depois voltava."* É tudo o que existe. **Nenhuma medição.**

### O primeiro suspeito sou eu

Durante a bancada abri `hidraw4`, `event21/22/23` e `event25-28` em laços de
leitura não-bloqueante com `sleep` de 2 a 4 ms. É a armadilha nº 3 da casa — *o
instrumento briga com o produto* — e o dia inteiro deu razão a ela duas vezes.

Há um segundo suspeito, de graça, e ele é `inferido-do-codigo`: o mesmo nó de
touchpad é lido por mais de um leitor com propósitos diferentes (o do cursor e o
do painel, este último aberto com `acumular_movimento=False` justamente para não
drenar o que o outro precisa — `daemon/sensor_hub.py:28-31`). Um terceiro leitor
meu, drenando, é candidato natural a engasgo.

### Quem decide

Ninguém, até haver medição. Não vale gastar bancada dela com isto antes do item
1: se o engasgo for o defeito da reconexão em versão branda, ele some junto.

### Como o portão morde

**Só depois de medir**, e a medição é um par com/sem: contar eventos do touchpad
por janela fixa, com e sem os instrumentos rodando, tudo o mais igual. Se for eu,
o conserto é do instrumento e o portão é do item 6 (a régua que declara que está
disputando o recurso). Se não for eu, é achado novo e ganha portão próprio — mas
escrever esse portão agora seria escrever contra um sintoma que ninguém
caracterizou, e portão assim nasce frouxo.

---

## 8. Duskfade — P3

### O que se sabe

Caso próprio, e a separação dele dos outros dois é um dos resultados do dia:
**nunca funcionou em transporte nenhum**, e em 16/08 deu os primeiros inputs da
vida dele. Para ele o defeito da reconexão era agravante, não causa.

E o disco já respondeu que não sabe: `Duskfade` e `DON'T SCREAM` têm a **mesma**
assinatura em disco — mesmo motor, mesmas famílias de API, mesmo wrapper, mesmo
Steam Input desligado. Um funciona e o outro não. **A causa do Duskfade não está
no disco**; está em tempo de execução.

### O que já está pronto para ele

O par com o DON'T SCREAM está montado, e o instrumento parou de mentir:
`scripts/ensaios/quem_o_jogo_abre.py` lia o environ do primeiro processo da
árvore — o `reaper` da Steam, que roda antes do wrapper — e por isso acusava a
própria cura de não existir. Corrigido por critério **estrutural** (o processo
mais fundo que casa com o padrão), nunca por conteúdo.

### Quem decide

**Ela**, e a decisão é de prioridade pura: é um jogo, contra frentes que afetam
todos. A recomendação é rodar o par **depois** do item 1 curado, junto com o
reteste do item que vem a seguir — mesma bancada, mesmo custo de montagem.

### Como o portão morde

Aqui a resposta honesta é: **ainda não morde, e forçar seria teatro.** Sem
causa, um portão para "o Duskfade funciona" só pode ser um teste de fim a fim
com o jogo aberto, que esta casa não roda. O que existe e vale é o portão que já
nasceu: o prontuário por jogo **recusa dizer "funciona"**, e há teste travando
que `Duskfade` e `DON'T SCREAM` saiam iguais. É o portão certo para o estado
atual do conhecimento — ele impede o próximo relatório de pintar os dois de
verde.

---

## O que fecha de graça quando o item 1 fechar

Não é frente própria, e por isso não entra na ordem — mas é a maior economia
possível do dia seguinte.

**Dado dela:** DON'T SCREAM e **Big Walk** usam microfone, giroscópio e touch, e
*"ambos os jogos funcionavam via bt com gatilho adaptativo e beleza"*.

Isso é o **lado bom do par** para as features que hoje falham no rádio: não é
hipótese de que "deveria funcionar", é registro de que funcionava, nos mesmos
jogos, no mesmo transporte. Se, depois do item 1 curado, os dois voltarem
inteiros, então o defeito da reconexão explicava também as features — e a lista
de "metade do controle não atravessa no rádio" encolhe de uma vez.

**Custo:** zero de investigação, um reteste. **Ordem:** logo depois do item 1, e
antes de qualquer investigação nova sobre gatilhos, vibração ou touch no rádio.

---

## O que FECHOU em 16/08, para ninguém reabrir

| o que | onde está a prova |
|---|---|
| o `EvdevReader` como suspeito da reconexão | `tests/unit/test_reconexao_bt_01_o_leitor_tem_de_voltar_sozinho.py` — 3 testes, rodados de novo nesta passagem |
| áudio lido como estado de botão | commit `702f5b6`, 13 testes — a cura fica, mesmo não sendo a causa do travamento |
| o contador de jogos com wrapper que dizia 76 onde havia 63 | commit `dca7170` — o contador saiu; quem dá o veredito agora nomeia |
| o censo que lia a árvore `apps` errada do vdf | commit `045d3d0` e o estudo A ÁRVORE ERRADA |
| `quem_o_jogo_abre.py` lendo o environ do `reaper` | corrigido por critério estrutural |
| a Steam comendo a linha do wrapper | a sentinela, commits `4de4762` e `912617a` |

E os suspeitos que caíram com medição, que valem tanto quanto as curas: o jogo,
o Proton, o wrapper, o vpad ser pego pelo próprio IGNORE, o jogo não enxergar o
vpad, o CRC do BT, o grab oscilando, o gate de foco X11, o daemon parar de
emitir, a supressão de emulação e o perfil não entrar. A tabela inteira, com a
medição que derrubou cada um, está em
[O RÁDIO MEIO MUDO](../estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md).

---

## A tabela dos portões, num lugar só

Para quem for construir: cada linha é um portão, e cada portão diz o que
arrancar para ver vermelho.

| # | o portão | o que arrancar para vê-lo morder |
|---|---|---|
| 1.1 | o ciclo do leitor de movimento com o broker no meio | fixar o caminho na primeira resolução |
| 1.2 | `state_full` não diz `connected` com o leitor morto | nada: nasce vermelho no código de hoje |
| 1.3 | `primary_grab_state=pending` não pode durar | o retry do grab |
| 2.a | um toque de PS, uma Steam | o limitador de frequência |
| 2.b | nenhum atalho abre programa sem freio | o limitador, em qualquer disparador novo |
| 2.c | binário externo citado tem de estar declarado | nasce vermelho hoje, no `wmctrl` |
| 3.1 | escondidos comparados com o censo de físicos, por nome | voltar o veredito para `> 0` |
| 3.2 | bonds por diferença de conjuntos, com o MAC na tela | voltar o veredito para `n_info > 0` |
| 4.b | célula com `olho-dela` não pode ter grau de código | rebaixar uma célula medida por ela |
| 5.a | o broker recusa ou multiplexa o segundo pedido do mesmo nó | a arbitragem |
| 5.b | `bt_mic_enabled` não ganha escritor antes de 5.a | escrever o escritor |
| 6.a | a régua conferida contra correspondência conhecida | a conferência |
| 6.b | captura com gesto composto não vira veredito | a checagem de gesto único |

Treze portões. **Nenhum deles existe hoje.** Os três que existiam e passavam
verdes com o defeito vivo estão no topo deste documento, e é por isso que a
frase dela — *"me preocupa que isso possa voltar"* — é uma descrição correta do
estado, não um receio.

---

## O que este documento recusa afirmar

- **Que o item 1 está entendido.** Um suspeito caiu, com portão. Sobram três, e
  o mais informativo (`pending`) aponta para a **descoberta** do nó, não para o
  laço de reabertura — e isso é leitura de código, não medição.
- **Que a ponte do mic trava por causa da sequência do `0x32`.** É a única
  hipótese de pé e tem endereço, mas a sequência dos dois lados não foi medida
  no mesmo instante. A árvore contém duas afirmações contraditórias sobre isso e
  nenhuma delas foi medida.
- **Que instalar o `wmctrl` resolve o item 2.2.** A sessão é Wayland/COSMIC e o
  `wmctrl` é X11. Se a Steam sob Xwayland é alcançável por ele é **`incerto`**.
- **Que o alto-falante por rádio funcionou ou não funcionou.** A memória dela é
  fonte primária e o CSV diz outra coisa; a hipótese de reconciliação deste
  documento (volume e rota respondendo, sem PCM) **não foi medida**.
- **Que os 37% do giroscópio são perda.** Podem ser decimação de projeto.
  Ninguém mediu.
- **Que o touchpad engasga por minha causa.** É a primeira suspeita, e nada mais.
