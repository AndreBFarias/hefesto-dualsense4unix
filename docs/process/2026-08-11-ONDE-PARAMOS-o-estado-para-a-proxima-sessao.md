# ONDE PARAMOS — o estado para a próxima sessão

- **Escrito em:** 11/08/2026, no fim de uma sessão longa, a pedido dela: *"de
  forma que se eu der um barra clear o próximo Claude vá saber o que fazer"*.
- **Reescrito em 12/08/2026, à noite**, depois que a leva da bancada de 11→12/08
  **foi commitada**. A versão anterior descrevia a bancada com a árvore ainda
  suja e mandava, em caixa alta, caçar uma leva de 61 caminhos — **essa leva não
  existe mais: ela virou cinco commits**. Duas afirmações erradas saíram por
  substituição, e estão nomeadas na seção 0.1.
- **Atualizado na MESMA noite, depois da segunda bancada** (a das 22h em
  diante), a pedido dela: *"disparar agente pra corrigir e sobrescrever a
  documentação com os valores que medimos hoje"*. **Todos os números da tabela
  da seção 0 foram refeitos** contra a árvore de agora, e a bancada da noite tem
  seção própria — a **1.8**. Ela é o que converteu três curas de *"montou"* para
  **o aparelho obedeceu**, e derrubou uma hipótese grande (1.9).
- **O nome do arquivo não muda, e é de propósito:** o `CLAUDE.md` da raiz aponta
  para ele pelo nome, e renomear quebra o primeiro link que uma sessão nova
  segue.
- **Para quem chega agora:** leia o `CLAUDE.md` da raiz primeiro (ele diz a
  ordem), depois este arquivo. Ele responde três coisas: **o que mudou**, **o
  que está aberto**, e **o que é dela**.

> **ATENÇÃO — 15/08/2026, de madrugada: existem TRÊS dias inteiros de trabalho
> depois desta página.** Esta página é o retrato de 12/08 à noite, e as duas
> caixas abaixo apontam para o que veio depois. **Leia esta primeiro; a de 13/08
> continua valendo e vem em seguida.**
>
> A sessão de 14/08 → 15/08 rodou mais de quarenta subagentes, fechou sete
> commits, mediu a mesa cheia com **quatro DualSense resetados de fábrica e
> re-pareados do zero**, e deixou sete sprints novas. Comece por:
>
> 1. [A madrugada que quase não virou página](sprints/2026-08-15-INDICE-a-madrugada-que-quase-nao-virou-pagina.md)
>    — **registro de execução**: o que já rodou e não se refaz, as decisões
>    novas dela com as palavras dela, e a seção **"o que quase se perdeu"**, com
>    onze itens que estavam só no transcrito. É a página que responde
>    *"posso reabrir isto?"* em um minuto.
> 2. [O índice da leva da cor e do som](sprints/2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
>    — **plano**, com as dezessete perguntas **D-13 a D-29 dela, todas ainda em
>    aberto**, e o desenho do **ENSAIO 2+2** (dois controles no cabo e dois no
>    rádio, no mesmo minuto), que é decisão dela de 15/08.
>
> **Três coisas desta sessão estão na árvore e NÃO commitadas** — confira com
> `git status --short` antes de qualquer coisa: as duas curas de Bluetooth
> (`assets/systemd/hefesto-bt-agent.service`, `scripts/bt_bonds_restore.sh`), a
> MESA-CHEIA-12 (`daemon/subsystems/coop.py` e vizinhos), e as correções do mapa
> e da canônica.
>
> **E uma decisão dela de 15/08 está pendurada e trava código:** o número de
> jogador deve seguir a **ordem de conexão do momento**, não o lugar gravado por
> MAC — o oposto do que R-15 e R-23 fixaram em julho, com motivo medido. Está em
> [ORDEM-DE-CHEGADA-01](sprints/2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md).

> **ATENÇÃO — 13/08/2026: existe um dia inteiro de trabalho DEPOIS desta página,
> e ela ainda não o descreve.** Esta página segue sendo o retrato de 12/08 à
> noite. A sessão de 13/08 mediu o projeto inteiro, mediu as dez abas da janela,
> pagou sete dívidas que a própria medição levantou e deixou onze sprints de
> plano. Enquanto uma reescrita desta página não acontecer, **quem chega agora
> lê estes quatro documentos logo depois dela**, nesta ordem:
>
> 1. [O projeto inteiro num mapa só](estudos/2026-08-13-o-projeto-inteiro-num-mapa-so.md)
>    — o retrato de `cc768d4`, com o grau de cada afirmação. **A §6.1 já traz
>    marcados os sete itens que o próprio commit de 13/08 fechou**; os oito
>    restantes é que estão abertos.
> 2. [O que ficou de fora — o crítico de completude](estudos/2026-08-13-o-que-ficou-de-fora-o-critico-de-completude.md)
>    — o que aquele estudo **não** olhou. Ler antes de agir a partir dele.
> 3. [O censo das dez abas](estudos/2026-08-13-o-censo-das-dez-abas-o-que-a-janela-faz-com-quatro-controles.md)
>    — o que a janela faz com quatro controles na mesa, aba por aba. É a régua
>    que derrubou duas afirmações minhas sobre o rumble no mesmo dia.
> 4. [A mesa cheia — o índice das ondas](sprints/2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
>    — as três ondas, separadas por quem precisa estar presente, e as decisões
>    que travam esperando a palavra dela.
>
> **O que é dela nesta página continua valendo** — nada da sessão de 13/08
> revogou decisão dela. O que mudou foi o placar do que está feito.

---

## 0. Como ler os números desta página — e como atualizá-la barato

**A bancada dela aconteceu enquanto isto era escrito, com quatro DualSense na
mesa** — e mudou quase todos estes números uma vez. Vai mudar de novo. Por isso
cada número aqui declara **de que tipo é** e **qual comando o refaz**:

- **`[COLETA]`** — sai de um comando na árvore, em segundos, sem controle na
  mão. Se estiver velho, é porque ninguém rodou o comando. **Atualizar é
  barato.**
- **`[APARELHO]`** — só existe porque alguém pôs a mão no controle e olhou.
  Custa a bancada dela. **Não se atualiza sozinho, e envelhecer não o torna
  falso — torna-o datado.**

**Os valores abaixo são de 12/08 à noite, na árvore com a leva dos instrumentos
e da bancada já integrada** — depois de `c30c4a2`, e ainda **não commitada** no
momento em que isto foi escrito. Onde o número mudou desde a versão da tarde
desta página, o valor antigo está entre parênteses, porque a distância entre os
dois é a medida do que a noite rendeu.

| número | valor em 12/08 à noite | tipo | comando que o refaz |
|---|---|---|---|
| suíte verde | **9113 passed, 1 skipped, 4 xfailed**, exit 0, **4m43** (era 9002 passed) | `[COLETA]` | `.venv/bin/python -m pytest -q` |
| nós coletados | **9130** — `--collect-only` RODADO nesta leva, 13/08 00h. Não é a soma da execução (aquela dá 9118): a coleta enxerga nós que a execução pula | `[COLETA]` | `.venv/bin/python -m pytest -q --collect-only \| tail -1` |
| funções `def test_` em `tests/` | **7777** (era 7654) — **não** é o mesmo número, ver 0.2 | `[COLETA]` | `.venv/bin/python -m pytest -q tests/unit/test_emblemas_do_readme.py` |
| `mypy` no pacote | **Success**, 171 arquivos | `[COLETA]` | `.venv/bin/mypy src/hefesto_dualsense4unix` |
| linhas no mapa de canais | **293** | `[COLETA]` | `python3 scripts/gerar-mapa.py --check` |
| células em `O APARELHO OBEDECEU` | **15** células em **8** linhas (era 11 em 6), e **nenhuma** sem ensaio no caderno | `[APARELHO]` | coluna `cabo_grau`/`radio_grau` de `docs/data/mapa-controles.csv` |
| ensaios no caderno | **77** (eram 57), sendo **73** com `observado_por = olho-dela` | `[APARELHO]` | a linha `ensaios lidos do caderno` de `check_paridade_transporte.py` — o `wc -l` conta o cabeçalho e dá 78 |
| vereditos do caderno | **19** (eram 11) — 6 `E-A-CAUSA`, 13 `INCONCLUSIVO` | `[COLETA]` | `.venv/bin/python scripts/eliminacao.py` |
| dívida do mapa | **18 reprovações** `sem-mordida` e **21 avisos** (14 assimetria, 6 mordida-não-provada, 1 grau-sem-ensaio-que-obedeça); o portão sai **1** | `[COLETA]` | `python3 scripts/check_paridade_transporte.py` |
| linhas com `mordida_provada_em` | **0** de 293, com **40** já apontando `teste_que_morde` | `[COLETA]` | ver seção 2.1, item 6 |
| versão | **0.9.4** | `[COLETA]` | `grep '^version' pyproject.toml` |

**A dívida do mapa SUBIU de 15 para 18 reprovações, e isso é bom.** No mesmo
intervalo as **afirmações fortes** subiram de 45 para **48**: três células que
antes **calavam** passaram a afirmar alguma coisa, e afirmação forte sem mordida
é exatamente o que este portão existe para cobrar. **Um mapa que cala não tem
dívida nenhuma** — a dívida é o preço de o mapa ter passado a falar.

> **A regra que governa qualquer reescrita desta página** (fixada por ela em
> 11/08): **fato errado se SUBSTITUI; decisão medida ganha nota datada.** O
> teste que separa os dois: *se apagar isto faria alguém repetir um trabalho ou
> pagar um custo já pago?* Se sim, tem data. Se não, é só um número que a
> medição derrubou — sai. Na dúvida, guarde: errar para o lado de guardar é
> reversível.

### 0.1 O que esta reescrita SUBSTITUIU, e por quê

Ficam nomeados porque o defeito de um documento de orientação é caro de um jeito
específico: **ele manda a próxima sessão trabalhar no lugar errado.**

| o que a versão anterior dizia | o que a árvore diz |
|---|---|
| *"A ÁRVORE NÃO ESTÁ COMMITADA — 61 caminhos — e isto é a primeira coisa a fazer"* | a leva fechou em **cinco commits** de 12/08 (`34210b8`, `f1279a1`, `d4ca241`, `00733a9`, `c30c4a2`). Mandava caçar leva inexistente |
| sobre o gatilho da lightbar, em caixa alta: *"**Não está no produto**"* | **está**: `core/lightbar_gatilho.py` e `core/gatilho_fim_de_sequencia.py`, fiados em `daemon/connection.py:15-22`, com quatro arquivos de teste. É o **inverso** do defeito clássico desta casa (a cura escrita e nunca ligada) — aqui a cura foi ligada e o papel não soube |
| *"8949 testes coletados"* · *"53 ensaios, 52 com olho-dela"* | **9007** coletados · **57** ensaios, **53** com olho-dela |
| *"as armadilhas do método — doze hoje"* | continua **doze**; era o título da tabela em `METODO-DE-ISOLAMENTO.md` que ainda dizia *sete*, e foi corrigido |

Nenhuma dessas quatro passa no teste do custo já pago: são números que a medição
derrubou. **Saíram.** O que tem data e ficou está no corpo do documento.

**E o que a bancada da NOITE substituiu, algumas horas depois** — a mesma régua,
aplicada às frases que ela mesma acabara de derrubar:

| o que estava escrito | o que a bancada mediu |
|---|---|
| a **hipótese grande**: a rota `hidraw` suprimida por Bluetooth seria a causa-raiz **compartilhada** de rumble, gatilho e luz | **falsa.** A supressão limpa **só** os bits de LED; rumble e gatilho **sempre** saíram por `hidraw` no rádio, e a bancada os viu funcionando lá. A hipótese vale para **lightbar** e **número de jogador**, e só (ver 1.9) |
| *"com quatro controles a duração da vibração é diferente, e não foi explicado"* | com a cura ligada, **duas rodadas, duração igual** nas duas. A observação de 11/08 continua valendo como o retrato do defeito **antes** da cura |
| o gatilho adaptativo por **rádio** afirmado com grau forte **sem um único ensaio** que o sustentasse | agora tem: `Rigid` nos quatro, cabo e rádio, com o R2 solto como controle negativo. Foi o portão `grau-sem-ensaio` (12/08) que flagrou a falta |
| na página de solução de problemas: *"por Bluetooth a cor sai por um caminho que perde essa disputa"*, como se a **rota** fosse ruim | **não é a rota.** Sem escritor concorrente, **as duas** rotas obedecem. O que derruba a cor é **quem mais está escrevendo**, e a hora é a **conexão** |

As quatro saíram por substituição, nos arquivos onde moravam. **O ensaio de
11/08 que virou `parcial` hoje não saiu** — ele registra um custo já pago, e leva
data, que é a diferença que a régua desta casa mede.

### 0.2 O emblema do README conta uma coisa diferente — e o teste morde

**Descoberto ao consertar o emblema, em 12/08, e vale registrar porque a
armadilha é silenciosa.** O emblema da capa declara um **piso** (*"mais de
N"*), e `tests/unit/test_emblemas_do_readme.py` o confere contra o número de
**funções `def test_` em `tests/`** — hoje **7654** —, **não** contra o número
de testes coletados pelo pytest — hoje **9007**. A diferença são as
parametrizações: um `def test_` com dez casos vira dez nós coletados e continua
sendo **uma** função.

Quem pintar o piso pelo número que o pytest imprime no fim da suíte **derruba a
CI**. Foi exatamente o que aconteceu aqui: `mais de 9000` reprovou com
`7654 >= 9000` falso, e o piso correto é **`mais de 7000`**. O teste está certo,
e o desenho dele também: piso que envelhece para baixo nunca derruba a CI por
suíte que cresceu.

---

## 1. O que mudou, em uma tela

**Duas sessões encostadas, e elas se leem juntas.** A de 11→12/08 foi de
**MEDIR NO APARELHO**: quatro DualSense na mesa dela — dois no cabo, dois no
rádio — percorrendo o [`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md) item
por item. A de 12/08 à noite foi de **FECHAR**: transformar o que a bancada
mediu em código commitado, e consertar o que o instalador quebrava numa máquina
limpa.

**A página inteira da bancada, com a prova de cada linha, é a sprint
[CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md).**
Não a duplique: o que está abaixo é o resumo para decidir por onde continuar.

### 1.0 A leva fechou — os cinco commits, e o que cada um carrega

| commit | o que ele fecha |
|---|---|
| `34210b8` | **rumble + lightbar** — o keepalive deixou de ser perpétuo; o gatilho de fim de sequência nasceu genérico |
| `f1279a1` | **co-op + install** — o `IGNORE` decidido cedo demais, e o `udevadm trigger` que casava zero dispositivos |
| `d4ca241` | **release 0.9.4** — *a noite dos quatro controles* |
| `00733a9` | **install** — o instalador quebrava na máquina **limpa**, no passo 1 |
| `c30c4a2` | **daemon** — 1.287 `openat` por segundo só para perguntar *"tem jogo aberto?"* |

Os três primeiros defeitos têm a **mesma forma**, e é ela que vale como lição:
**o produto decidia DURANTE uma sequência de eventos, em vez de esperar ela
sossegar.**

### 1.1 O rumble — causa isolada, e com número

**GRAU: `[APARELHO]`**, `docs/data/ensaios.csv:16-24`, com o olho dela.

O jogo que fala com o **DualSense físico** — sem controle virtual e fora da
Conexão Nativa — manda a vibração por força-feedback no `evdev`. O **keepalive**
do daemon reescrevia `common[2]`/`common[3]` zerados a cada 0,5 s e apagava o
motor. Com o daemon vivo, 40 s de vibração deram **nada** no cabo e **um único
tranco** no rádio; com ele parado, contínuo nos dois.

**A dose-resposta é o que transforma indício em causa:** com a constante em
8,0 s a vibração passou a durar **oito segundos exatos**, nos dois transportes.

**E a segunda metade derrubou a premissa de uma cura inteira.** O que estava
escrito apostava que **desligar os bits de autorização** bastava para o firmware
conservar o motor de outro dono. Um único report com os bits **desligados**
pedindo `common[2]=200` e `common[3]=0` fez o tremor **trocar de lado** na mão
dela — *"esquerda e senti que foi pra direita e lá morreu"*. **O firmware honra
os BYTES.** Isso é fato de protocolo e está na canônica
([§2, *Os BITS de vibração não são porteiro dos BYTES de motor*](../protocol/dualsense-referencia-canonica.md)).

**A cura, e ela está em `34210b8`:** o keepalive **deixou de ser perpétuo** e
passou a valer só na janela de confirmação depois de cada mudança real.
Reconfirmar cobre report perdido; reconfirmar para sempre só apaga motor alheio.
O único write não-destrutivo é o write que **não acontece**.

### 1.2 A política de vibração — decisão dela, com o preço na mesa

**GRAU: `DECISÃO DELA`**, 11/08, depois de o preço de cada opção ir para a mesa.
Está no código: `daemon/subsystems/rumble.py:83-85`.

- **Economia 0,3× · Balanceado 1,0× · Máximo 1,5×.** O Balanceado era 0,7 e o
  tooltip prometia *"do jeito que o jogo pediu"* — duas afirmações e uma
  mentira. O Máximo era 1,0, ou seja, não aumentava nada.
- **O 2,0 foi considerado e descartado por ela:** a 2,0 metade da faixa satura
  em 255 e a variação da vibração some. A 1,5 satura de 170 para cima — um
  terço, e é o preço aceito.
- **O deslizador vai a 200 e isso não é incoerência:** os quatro botões são
  **presets seguros**; o deslizador é o ajuste livre de quem aceita o preço.
- **O produto passou a avisar** quando não há gamepad virtual **nem** Modo
  Nativo — o estado em que o multiplicador **não age**. O aviso mora em cima
  dos quatro botões da aba Rumble.

Onde isso já está escrito para quem usa:
[`interface.md`](../usage/interface.md) e [`modos.md`](../usage/modos.md).

### 1.3 A lightbar por Bluetooth — o suspeito de dezesseis dias, e a cura que ENTROU

**GRAU do fato: `[APARELHO]`. GRAU da cura: `MONTOU` — e a diferença importa.**

Com o daemon parado, `readlink` sobre `/proc/*/fd` mostrou o processo `steam`
com `/dev/hidraw4..7` abertos e o `fdinfo` confirmou **leitura+escrita**. No fio,
por `btmon`: **98** pacotes de saída durante a probe com a Steam viva (as três
barras nasceram apagadas) contra **6** sem ninguém no `hidraw` (as três nasceram
acesas, e as três obedeceram a verde puro).

Três coisas que a bancada mediu e que desenharam a cura:

1. **A rajada tem hora.** Duas rajadas, `t+0`–`t+3 s` e `t+15`–`t+18 s`, com
   silêncio entre elas. A Steam bombardeia na **probe** e depois cala.
2. **A rajada é por EVENTO, não por controle.** Cada conexão nova faz a Steam
   repintar **todos**. Um protótipo que escrevia 1,5 s depois de cada conexão
   perdeu dois dos três.
3. **A rota decide.** Com a Steam aberta, `sysfs` não muda a barra; o report
   `0x31` cru no `hidraw` pintou os três.

**A cura ENTROU no produto em `34210b8`**, com o desenho que ela aceitou na
bancada (*"perfeito"*): um mecanismo genérico de **fim de sequência**
(`core/gatilho_fim_de_sequencia.py`) que **arma a cada evento conhecido** —
conexão nova, jogo abrindo, jogo fechando — **rearma enquanto eles chegam, e só
dispara quando sossega**. Aí escreve cor **e** número de jogador no mesmo
report, por `hidraw`, em **todos** os controles do rádio, e
**incondicionalmente**: consultar o cache do `sysfs` antes de escrever é
justamente o que faz o produto pular a reescrita quando ela é necessária. O
enfiamento no daemon está em `daemon/connection.py` e `daemon/lifecycle.py`.

> **A ressalva honesta, e ela é do próprio commit:** *"os testes provam que o
> report certo sai pela rota certa no instante certo. Não provam que a barra
> acende — isso é bancada, e ela não viu ainda."* **`MONTOU` não é `O APARELHO
> OBEDECEU`.** Quem tiver o controle na mão fecha isto em um minuto; até lá, a
> linha `luz.lightbar.cor` do mapa continua devendo a volta do ensaio (2.1,
> item 1).

A medição inteira está em
[a pilha do Steam Input](../protocol/pilha-steam-input-xpad-sdl.md), seção
6-bis.

### 1.4 O co-op — o `IGNORE` decidido cedo, e o que a cura NÃO alcança

**GRAU: `[APARELHO]`** quanto ao sintoma (relato dela no Sackboy, e ela apontou
a direção: *"deve ser algo relacionado aos gamepad virtuais ou coop"*);
**`MONTOU`** quanto à cura, em `f1279a1`.

O `SDL_GAMECONTROLLER_IGNORE_DEVICES` esconde os DualSense físicos do jogo, e
por isso **exige um gamepad virtual por controle físico**. Esconder quatro e
devolver um é **zero** controles para três pessoas. O quarto vpad ficou pronto
**onze segundos** depois do primeiro, e a cobertura foi avaliada três vezes
durante a subida, sempre incompleta. Dois buracos por trás: o arquivo por
`appid` — o que um jogo **com** perfil de fato lê — nunca aplicava a cobertura,
porque o default `0` significava *"não sei"* e *"não sei"* autorizava o
`IGNORE`; e a mesa muda sem borda que materialize.

> **A ressalva, e ela também é do commit:** **isto não conserta a sessão que ela
> mediu.** O jogo lê as variáveis **uma vez**, no `exec` do wrapper, 63 segundos
> antes do primeiro vpad — e não existe chamada de sistema que troque o
> `environ` de outro processo. Regravar o arquivo não alcança processo já
> subido. Por isso a cura **avisa no journal** em vez de fingir que curou.

### 1.5 O instalador quebrava na máquina LIMPA — e é o defeito mais caro possível

**GRAU: `[COLETA]`**, medido por ciclo `uninstall → install` que ela pediu antes
de dormir. Cura em `00733a9`.

`install.sh:1012` chamava `info "distro, bluez e Secure Boot: nada que
atrapalhe"`, e **`info` nunca foi função deste script** — ele define
`step`/`ok`/`warn`/`die` e nada mais. O shell caía no `/usr/bin/info` do
sistema, o leitor de documentação GNU, que sai com erro; o `set -e` derrubava a
instalação ali.

**E o detalhe que decide:** a linha só executa quando **nada** na máquina
atrapalha. Ou seja, ele quebrava **exatamente na máquina saudável** — que é a
primeira coisa que um PC novo é. Medido: depois do `uninstall`, o `install` saía
**exit 1**, **zero** regras udev, daemon inativo. Com a correção: **exit 0**,
**11** regras de volta, daemon ativo.

**Nenhum portão pegava isto**, e a razão é reaproveitável: os portões rodam com
o produto **já instalado**, e este defeito só existe no caminho da máquina
limpa. Isto sustenta a doutrina da casa de que **`1.0.0` é o número que se põe
DEPOIS de o PC novo passar**.

### 1.6 O daemon varria a tabela de processos inteira, duas vezes por segundo

**GRAU: `[COLETA]`**, com uma honestidade que vale copiar. Cura em `c30c4a2`.

`strace -c -f` no daemon vivo devolveu **1.287 `openat` por segundo** com a
máquina parada: a cada 2,003 s o daemon forkava `pgrep -af "SteamLaunch AppId="`,
e o `pgrep` lê cinco arquivos por processo, vezes ~425 pids. Trocado por uma
helper com duas camadas — o marker que o próprio `hefesto-launch` já grava, e
uma varredura em Python puro com **um** arquivo por pid. Medido: **10,76 ms →
1,85 ms** por chamada; `execve` de 6 para 0; no caso comum, de ~1.287 para
**2** `openat` por tique.

> **A honestidade sobre a evidência, e ela é do commit:** o teste de causalidade
> (SIGSTOP no daemon por 12 s, SIGCONT) **não** condenou o daemon — tudo dentro
> do ruído —, mas rodou **sem jogo aberto**, então também não o absolve. **O que
> entrou é redução de custo com semântica idêntica, não a cura de um bug
> provado.**

E uma segunda leitura, adversarial, achou um defeito **grave** na primeira
versão: existem processos vivos nesta máquina cuja cmdline contém a agulha
**porque estão procurando por ela** — um vigia de jogo que mora fora desta
árvore, na configuração de shell dela, e o nosso próprio
`scripts/disable_steam_input.sh`. Com a agulha como substring solta, uma dessas
iscas com pid menor virava a resposta. **Rever a própria mudança com olhos de
adversário é parte do ciclo, não zelo extra.**

### 1.7 O preço do achado do Steam: ele contamina o passado

Dezesseis dias perseguiram, um a um, o `0x08`, o keepalive, a adoção por
Bluetooth, o cache do sysfs, a instância de conexão e a revisão de hardware — **e
a Steam esteve com a caneta na mão o tempo inteiro, inclusive durante as
medições que concluíram cada uma daquelas hipóteses**.

Isso **não** torna aquelas leituras erradas. Torna-as **incapazes de isolar
qualquer coisa**, porque a variável que hoje se sabe decisiva estava livre em
todas. Quem for reabrir qualquer conclusão de lightbar anterior a 12/08 pergunta
primeiro: *quem estava com o `hidraw` aberto naquele instante?*

### 1.8 A bancada da NOITE de 12/08 — as curas saíram do papel e foram ao plástico

**GRAU: `[APARELHO]`**, ensaios `docs/data/ensaios.csv:59-78`, **todos** com
`observado_por = olho-dela`. Quatro DualSense na mesa: **dois no cabo e dois no
rádio**, os três revisões de hardware representadas.

Esta é a bancada que faltava para as curas de `34210b8` deixarem de ser
`MONTOU`. O caderno saiu de 57 para **77** ensaios e o mapa passou a ter **15**
células no grau mais forte — **nenhuma** sem ensaio que a sustente, o que é a
primeira vez que isso acontece nesta casa.

| o que foi medido | o que o aparelho respondeu |
|---|---|
| **Vibração por FF, serviço VIVO**, cabo e rádio | **contínua**: 8,26 s num controle do cabo; 8,28 s no cabo e no rádio disparados na **mesma janela** (0,0 ms). **Primeira vez** que o rádio dura a janela inteira com o serviço vivo — em 11/08 dava **um tranco** |
| **Os quatro sob carga**, duas rodadas | **duração igual** nas duas. Ela mediu **dois por vez, um em cada mão** (um do cabo, um do rádio), porque comparar duas mãos é inequívoco e olhar quatro na mesa não é. Desenho pedido por ela: *"nosso resultado não deve ser ambíguo"* |
| **Gatilho `Rigid[0,8]` só no L2**, nos quatro | **L2 duro nos quatro**, cabo e rádio; **R2 solto nos quatro** como controle negativo |
| **Gatilho só no R2 de UM do rádio**, mirado por MAC | **só o mirado endureceu.** Prova duas coisas na mesma janela: o gatilho direito obedece por rádio, **e** o `uniq` é respeitado no Bluetooth (sem isso, viraria broadcast e o isolamento seria ilusão) |
| **Cor mirada por MAC num do cabo** | *"verde inequívoco, os demais mostrando a cor de antes"* — e o daemon confirmou o alvo na própria resposta (`aplicado_em`), contrato que o `trigger.set` **não** tem |
| **Cor por `hidraw` (`0x31`)**, daemon **parado** e Steam **fechada** | pintou os dois do rádio **e durou 136 s** — o dobro do prazo que o ensaio pedia, **sem reforço nenhum** |
| **Cor por `sysfs`**, mesmas condições | **também obedece.** A rota **não** é morta: o que a derruba é a **probe** com a Steam viva, não a rota |
| **Número de jogador** quando um controle cai | **renumera** quem fica (P4 → P3) e **devolve** quando ele volta. Reversível e simétrico |

**A leitura que atravessa a tabela inteira:** o que separa obedecer de não
obedecer, nesta casa, **não é o transporte** — é **quem mais está escrevendo, e
quando**. Cabo e rádio se comportaram igual em tudo que foi medido sem escritor
concorrente.

**Três consequências que valem para quem continuar:**

1. **Uma cor escrita não precisa de keepalive.** Os 136 s derrubam a suspeita de
   que o firmware esquece entre escritas. Reafirmação periódica de cor é report
   pago à toa — e esta casa já mediu o preço desse hábito no rumble, onde
   reafirmar para sempre **apagava motor alheio**.
2. **O controle negativo virou rotina, e é ele que dá valor ao resultado.** Em
   todos os ensaios de isolamento a pergunta *"e os outros três?"* foi
   respondida na mesma janela. Sem isso, `uniq` ignorado passaria por
   isolamento.
3. **O que continua sem medição não encolheu tanto quanto parece:** só `Rigid`
   foi exercitado, com **um** jogo de parâmetros; o elemento específico de que o
   efeito depende segue sem isolamento; e **ninguém viu a cura da lightbar
   acender pelo produto com a Steam viva** — ver 2.1, itens 1, 1-bis, 2 e 3.

### 1.9 A hipótese grande NÃO se confirmou — e isto é o achado mais importante da noite

**GRAU: `[APARELHO]`**, por refutação direta, e fica em seção própria porque uma
hipótese falsa que ninguém derruba custa mais que um bug.

Estava escrito, e era o desenho que organizava a investigação, que **a rota
`hidraw` suprimida por Bluetooth** seria a **causa-raiz compartilhada** de três
sintomas: rumble que morre, gatilho que some e barra que não pinta. Era elegante,
explicava tudo, e **é falsa**.

- `_suppress_leds` limpa **só os bits de LED**. Nada de motor, nada de gatilho.
- **Rumble e gatilho sempre saíram por `hidraw` no rádio** — e a bancada provou
  isso do jeito mais simples possível: **vendo os dois funcionarem lá**, com o
  serviço vivo.
- A hipótese **continua valendo** para **lightbar** e **número de jogador**, que
  são exatamente os dois campos que a supressão toca.

**A lição de método, e ela é da casa:** hipótese tem de explicar **o que já
funcionava**. Esta não explicava — se a supressão matasse a rota do rádio, o
gatilho por rádio nunca teria funcionado, e ele funciona. Bastava perguntar isso
antes; a bancada só cobrou a fatura.

---

## 2. O que está EM ABERTO — e é aqui que a próxima sessão começa

### 2.1 O que a bancada deixou aberto

Os sete itens da sprint, cada um com o próprio grau, mais um oitavo que os
commits de 12/08 criaram (o **1-bis**). A lista comentada está na seção 7 da
[CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md).
**Nenhum dos sete fechou com os commits de 12/08** — eles fecharam as *curas*, e
estes são de *prova*.

| # | o que falta | tipo | por que importa |
|---|---|---|---|
| 1 | **A VOLTA do ensaio da lightbar** — subir os controles com a Steam viva na probe, de propósito, e ver o defeito voltar | `[APARELHO]` | só a volta distingue causa de coincidência. A ida está feita; a volta parou quando dois controles caíram do rádio |
| 1-bis | **Ver a cura da lightbar ACENDER, pelo PRODUTO, com a Steam viva** | `[APARELHO]` | **encolheu, não fechou** (12/08 à noite): a *rota* está provada — o `0x31` pintou os dois do rádio e durou 136 s, sem Steam. O que falta é ver o **produto** ganhar a disputa na probe |
| 2 | **O elemento específico do gatilho** não está isolado | `[APARELHO]` | funciona **nos dois transportes**, e ninguém sabe de qual bit ou byte depende. É onde o rumble estava na manhã de 11/08 |
| 3 | **Sete dos oito modos de gatilho** nunca foram tocados | `[APARELHO]` | continua: em 12/08 à noite só `Rigid[0,8]` foi exercitado de novo, agora nos quatro controles e nos dois transportes — mais **cobertura**, mesmo **modo** |
| 4 | **Algo apaga o efeito de gatilho com período de MINUTOS** | `[APARELHO]` medido, **sem suspeito nomeado** | aos 120 s a leitura se inverteu. Candidatos a ler no código: o tick do daemon e o `reassert_resolved_outputs` |
| 5 | **O cancelamento é total com dois alvos e parcial com quatro** | `[APARELHO]` medido e **não explicado** | registrado assim de propósito: explicação sem medição vira folclore com data |
| 6 | **A mordida das curas** — `mordida_provada_em` está vazio em **todas** as 293 linhas do mapa | `[COLETA]` | `vibracao.rumble.ff` já tem `teste_que_morde` apontado (`tests/unit/test_paridade_transporte_rumble_em_par.py`), mas **ninguém arrancou a cura e viu reprovar**. É o que impede tudo isto de voltar na próxima mexida. Vale igual para `luz.lightbar.cor` |
| 7 | **A poda não foi feita** | `[COLETA]` | é a metade que dá lucro: o que foi inocentado pode **parar de ser acionado**, e nada saiu do produto |

**Se for escolher uma:** a **6**, agora sozinha no topo. Depois da bancada da
noite ela é a **única** que não depende da mão dela: `[COLETA]` pura, e é a única
que impede a regressão de voltar. A **1-bis** continua em segundo e encolheu — o
que falta dela é um minuto de bancada com a Steam **de propósito** viva.

### 2.2 A dívida do mapa de canais, em número

`python3 scripts/check_paridade_transporte.py` sai **1** hoje, e o que ele diz é
o retrato honesto do que se sabe (números refeitos em 12/08 à noite):

- **18 reprovações** `sem-mordida` (eram 15): célula que afirma `aciona = sim`
  com confiança `medido` e `teste_que_morde` vazio. *"Se isso quebrar, a suíte
  inteira continua verde."*
- **14 avisos** `assimetria-nao-declarada` (eram 13): um transporte respondeu e o
  outro não. É exatamente a forma da regressão que este mapa existe para pegar.
- **6 avisos** `mordida-nao-provada`, novos e nomeados: linha com grau forte
  **e** `teste_que_morde` apontado, mas `mordida_provada_em` vazia — ninguém
  arrancou a cura e viu reprovar. São as seis linhas do item 6 acima, agora com
  o portão dizendo o nome de cada uma.
- **1 aviso** `grau-sem-ensaio-que-obedeca`, e ele merece leitura: a linha
  `gatilho.direito.adaptativo` declara `cabo_grau = O APARELHO OBEDECEU` e o
  único ensaio de **cabo** dela diz *"não obedece"*. Ou o degrau está alto
  demais, **ou** o ensaio foi gravado com o `resultado` do **suspeito** em vez do
  que a **feature** fez. É `[COLETA]` de cinco minutos, e vale fazer antes de
  citar aquela célula.
- Censo: **586** células de transporte, **185** mudas, **84** linhas mudas dos
  **dois** lados, **48** afirmações fortes, **15** graus fortes — e **zero**
  graus fortes sem ensaio no caderno.

Este portão **não** está na lista de fechamento do `CLAUDE.md`, e é de propósito:
ele mede dívida, não regressão — e ele roda no CI **informativo**
(`continue-on-error`), justamente por isso. Pôr o nome dele no bloco do
`CLAUDE.md` hoje **reprovaria** o portão P0 (`test_nenhum_portao_da_casa_virou_aviso`),
e a reprovação estaria certa: portão que não reprova não é portão. Ele é o mapa
do que a próxima bancada compra.

### 2.3 A leva de instrumentos ENTROU — e é ela que explica os números novos

**GRAU: `[COLETA]`. Isto substitui o "relato de sessão paralela" que estava aqui
horas atrás**, e que dizia, corretamente para o momento, que aquela frente ainda
não estava na árvore.

Ela entrou. As cinco curas de instrumento estão descritas no `CHANGELOG`, seção
`[0.9.4.2] — 2026-08-13` (elas estiveram em `[Unreleased]` até a versão fechar;
hoje o `[Unreleased]` está vazio, e quem procurasse ali não acharia nada), e a
que mais importa para quem lê esta página é a primeira: **a
suíte estava saindo com código 1 desde 11/08** — a guarda da árvore congelada
acusava como *"produto apagado"* um `.pyc` que o próprio teste criava dentro da
cópia. Enquanto isso durou, *"a suíte passou"* **não era verificável nesta
casa**, e o job `lint-test` do CI estava no mesmo estado.

**A consequência para esta página:** todo número `[COLETA]` da seção 0 foi
refeito **depois** dessa cura. Os anteriores não eram mentira — eram leitura de
um instrumento torto.

**O comando que decide, e ele continua barato:** `git status --short` (a leva da
noite ainda não estava commitada quando isto foi escrito), seguido de
`.venv/bin/python -m pytest -q` e `python3 scripts/check_paridade_transporte.py`.

### 2.4 As sprints de correção, da família A

Fonte: `sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md`, seção
5. Elas existiam porque sete documentos novos contradiziam páginas antigas.

**Onze das doze fecharam** nos commits de 11/08 — A-0 e A-9 em `91cfd39`, A-1,
A-2, A-4, A-6 e A-7 em `b9b7dee`, A-3 e A-8 em `788564c`, A-10 (128 citações
realinhadas) e A-11 em `a0e71a8`.

**A-5 continua ABERTA, e tem uma armadilha medida.** O nome errado
(`DirectInput/PS4`) aparece hoje em **21 arquivos** `[COLETA]`, mas em **dois
sentidos diferentes**: o modo do 8BitDo que se disfarça de DualShock 4
(`054c:05c4` — que no vocabulário da 8BitDo é o modo **macOS**), e referências ao
**DualShock 4 de verdade** — `assets/dkms/hid-playstation/patch/0002-*.patch` é
sobre o DS4 real, e o cabeçalho dele vai para o upstream. **Substituição cega
quebra o segundo.** Quem for executar: separe os dois sentidos antes de trocar
qualquer palavra, e lembre que o D-input verdadeiro do 8BitDo é `B + Start`,
`2dc8:6001` (medido em 11/08).

### 2.5 O caminho até a versão final

Fonte: `2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md`.

**Nove dias e meio de bancada, ou dois e meio no caminho mínimo.** A ordem é por
dependência, não por importância, e a ETAPA 1 é pré-requisito de tudo: enquanto
o `doctor` sair verde com curas ausentes, nenhum critério de aceite significa
alguma coisa.

**Versão hoje: `0.9.4`, e o `1.0.0` continua sendo dela** — pela doutrina da
própria casa, `ENTREGUE EM CÓDIGO` não é `VALIDADO POR ELA`. O defeito de
`00733a9` (1.5) é a prova mais recente de que essa doutrina paga: o instalador
quebrava na máquina limpa e **nenhum portão viu**.

### 2.6 O que só o aparelho responde

- **A captura de Bluetooth** (`tests/fixtures/hid_capture_bt.bin`) continua
  devendo desde 31/07. O gravador está consertado e provado
  (`scripts/record_hid_capture.py`); o modo guiado precisa das mãos dela.
- **Os três módulos DKMS nunca foram construídos contra outro kernel** que não o
  `7.0.11-76070011-generic`. É o furo com maior chance de decidir a instalação
  numa máquina nova.
- **Ninguém rodou o produto com Secure Boot ligado.** Com a chave MOK não
  enrolada, o kernel recusa o `.ko` e **não volta ao in-tree** — a máquina fica
  pior do que sem a cura.
- **Os `.deb` do backport do BlueZ não existem.** A receita vive na árvore
  (`estudos/2026-07-19-*`), mas gerar os pacotes continua sendo trabalho. É o
  único `FAIL` que um PC novo levaria no caminho `native`.
- **Três perguntas de protocolo** entraram na canônica em 12/08, e nenhuma se
  responde lendo arquivo: de quantos bits o firmware precisa para vibrar; se os
  bits são porteiro dos blocos de **LED** e **áudio**; e quem reaplica o gatilho
  com período de minutos.

---

## 3. O que é DELA, e não se decide sem ela

**Decisões novas, de 11 e 12/08, e as três primeiras já estão no código ou na
configuração da máquina dela:**

- **A escada da vibração: 0,3× / 1,0× / 1,5×**, com o 2,0 considerado e
  descartado por ela, e o deslizador livre até 200. Ver 1.2. **Está no código**
  (`daemon/subsystems/rumble.py:83-85`).
- **Nada de MAC, nada de personalização por controle** — literal, 12/08:
  *"nada de macs, nada de personalização por controle; se eu conectar controle
  virgem ele tem que funcionar via produto"*. Foi **aplicado à configuração
  dela** (o `order` do `controllers.json` de 9 MACs para 0, e o bloco
  `controllers` de quatro perfis), com backup em
  `~/.config/hefesto-dualsense4unix/backup-limpeza-20260811-233704`. **O que
  isso implica para o CÓDIGO — o override por peça, `PERFIL-01` e
  `POR-UNIDADE-01` — não foi decidido, e é dela.** De brinde, a limpeza mediu
  uma coisa boa: o produto numerou os três controles sozinho, **sem nenhum MAC
  conhecido**.
- **Quem manda na barra, por modo** — literal, 12/08: *"no modo nativo
  devolvemos o controle pra steam e no modo conexão também, todo o resto é o
  hefesto"*. É a cerca do gatilho da cor, e é a mesma do
  `FEAT-NATIVE-OUTPUT-MUTE-01` aplicada ao LED.
- **O aviso dela sobre reincidência**, e ele vale como método: a rota de escrita
  já foi apontada como causa nesta casa antes, e *"reconectar cura"* foi
  concluído e derrubado **quatro vezes desde 17/07**. Quem for mexer na cura da
  lightbar responde primeiro o que derrubou a conclusão anterior.

- **A renumeração de jogador no meio da partida — ABERTA, e nasceu medida em
  12/08 à noite.** Quando um controle cai, o produto **renumera os que ficam**
  (quem era P4 vira P3) e **devolve** o número quando ele volta. É reversível e
  simétrico, e o produto está fazendo isso de propósito. **Se é o desejado é
  dela:** num co-op em andamento, o jogador 4 virar 3 troca quem é quem no meio
  do jogo. Ensaio `comb-slot-jogador-2200` (`docs/data/ensaios.csv:78`), grau
  `[APARELHO]`, resultado **parcial** — e o *parcial* é o dado, não a falta dele.

**As decisões antigas que continuam abertas:**

- **A procedência da arte dos SVG.** Ela não lembra a origem e os desenhos foram
  editados aqui. Fica como **risco aberto de licença**. Uma saída, sem pressa:
  redesenhar os três do zero a partir dos aparelhos dela.
- **O `1.0.0`** — quando o produto está pronto é decisão dela, e o critério é
  ver funcionando num PC novo.
- **As perguntas abertas nos índices de 07/08 e 08/08** continuam válidas;
  nenhuma foi respondida.

E há uma coisa fora do código que continua de pé: **a senha dela está em cinco
commits públicos desde 22/05**. Registrado em memória; só ela pode trocar.

---

## 4. Como não repetir o que já custou caro

Cinco armadilhas, escolhidas por preço. A lista completa e numerada — **doze**
hoje — está em [`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md), e a de tela
em [`COMO-OLHAR-A-TELA.md`](COMO-OLHAR-A-TELA.md).

1. **Pergunte QUEM MAIS está escrevendo neste dispositivo — e com que
   permissão.** É a pergunta 1 do método lida por inteiro, e foi a que custou
   dezesseis dias: o Steam com `hidraw` aberto em leitura+escrita nunca entrou
   na lista de suspeitos. O comando é barato:
   `readlink /proc/*/fd/* 2>/dev/null | grep hidraw`.
2. **Nunca peça cronômetro à mão humana.** Duas rodadas se perderam pedindo *"em
   que instante parou"*, e as duas respostas eram incompatíveis entre si —
   **defeito do instrumento, não dela**. A terceira fechou a questão trocando o
   tremor **de lado**: ou muda de mão, ou não muda. Redesenhe para que a resposta
   seja **sentida**, não medida.
3. **Controle negativo não é prova de obediência.** O R2 ficar solto enquanto o
   L2 endurece prova que o comando **não vazou de lado**; **não** prova que o
   lado direito obedece. Foi registrado errado, e ela pegou.
4. **Uma medição que só existe em docstring envelhece sem que ninguém note.**
   Uma frase de docstring foi copiada para o caderno como se fosse medição — e
   era falsa: a escavação achou quatro acendimentos dentro do período que ela
   dava como morto. Toda medição que muda um veredito **vira linha em
   `ensaios.csv` no mesmo dia**.
5. **Para provar obediência de cor, use uma cor que NINGUÉM MAIS QUEIRA, e com o
   daemon parado.** Escrever verde com o daemon vivo quase fez registrar
   `não obedece`: o daemon reescreveu a cor dele por cima em menos de um minuto,
   e a barra **estava** obedecendo — a ele.

**E uma sexta, nova de 12/08, porque ela é a que este próprio arquivo cometeu:**
**um documento de orientação erra de um jeito caro — ele manda trabalhar no
lugar errado.** Duas frases desta página mandaram caçar uma leva já commitada e
declararam ausente uma cura presente. Antes de escrever *"não está no produto"*,
`grep` no `src/`. Antes de escrever *"a árvore não está commitada"*, `git
status`.

**As cinco de 11/08 não sumiram, e continuam valendo** (cada uma agora mora
onde é usada): ler o **fonte** antes de medir por olho (canônica §5); **provar
que a peça responde** antes de perguntar de que lado ela falha (método, B2);
conferir **geometria de SVG na imagem**, não na aritmética; **valor de domínio
nunca leva acento** (`scripts/validar-acentuacao.py`); e **editar um arquivo
invalida as citações de linha dele** em todo o repositório — realinhe por diff,
não à mão.

---

## 5. Se você só tem cinco minutos

Rode isto, nesta ordem, e você sabe onde está:

```bash
git status --short                             # a leva da NOITE de 12/08 estava aberta aqui
git log --oneline c30c4a2..HEAD                # o que entrou DEPOIS desta página
.venv/bin/python -m pytest -q                  # 9113 verdes em 12/08 à noite, exit 0
.venv/bin/python scripts/eliminacao.py         # o veredito do caderno de ensaios
python3 scripts/check_paridade_transporte.py   # a dívida do mapa, em número
```

**A suíte entrou nesta lista de propósito, e é a mudança de 12/08 à noite:** por
dois dias ela saiu com código 1 por um defeito da guarda, não do produto (2.3).
Enquanto isso durou, ninguém aqui podia dizer *"a suíte passou"* e estar certo.

E leia, nesta ordem, se for tocar no aparelho: o
[`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md) — o checklist é o que
comprou esta bancada — e a
[CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md),
que é o que ele produziu numa noite.
