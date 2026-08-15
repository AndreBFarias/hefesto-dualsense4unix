# ÍNDICE — a madrugada que quase não virou página

- **Escrito em:** 15/08/2026, entre 01h e 02h da manhã, na branch
  `restauro/inicio-da-sessao`, sobre `97c2cbf` **com a árvore suja**.
- **Grau:** **REGISTRO DE EXECUÇÃO + índice das sprints novas.** Não é plano: a
  seção 1 é só o que **já rodou**, e a seção 2 aponta para as sete sprints que
  este documento abre.
- **Por que ele existe, nas palavras dela** (15/08, 04:27):

  > *"antes que percamos o contexto tanto vc quanto eu pode mandar um agente pra
  > ele revisar tudo o que ocorreu seja na nossa conversa ou de outros agentes e
  > materializar tudo em sprints pra ver se não deixamos nada passar?"*

- **O que este documento cobre:** a sessão de **14/08 de manhã até 15/08 de
  madrugada**, com mais de quarenta subagentes, sete commits, e uma quantidade
  de medição que nunca tinha chegado a uma página.
- **O irmão dele:** o
  [índice da leva da cor e do som](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
  é **PLANO** (as dezessete perguntas dela). Este é o oposto: o que virou, e o
  que ficou aberto com dono.

---

## Como ler

1. **O que já rodou** — se o item que você ia abrir está aqui, ele está feito.
2. **As sete sprints novas** — uma linha cada, e o que cada uma cobre.
3. **O que continua sendo dela** — as decisões novas de 14-15/08, com as palavras
   dela.
4. **O que quase se perdeu** — a seção que ela pediu ao mandar escrever isto. É a
   mais importante do documento.

---

## 1. O que já rodou, e não se refaz

### 1.a Os sete commits

| commit | hora | o que fechou |
|---|---|---|
| `48e7fd5` | 14/08 06:38 | três nomes e duas ordens para a mesma mesa, vistos na foto |
| `5dcd222` | 19:40 | o applet acompanha a versão da casa; o portão do `sudo` passa a morder |
| `4d9e992` | 19:40 | **MESA-CHEIA-09**: o daemon para de dizer "aplicado" quando nenhum byte saiu. Nasce `app/textos_de_aplicacao.py` (266 linhas), o vocabulário do *guardado* num lugar só |
| `410d1e1` | 19:40 | **MESA-CHEIA-11**: a janela fala no plural de quatro e para de mirar no controle errado. 7297 inserções, 23 arquivos, três testes novos |
| `b3d4434` | 19:41 | o veredito de áudio do doctor **conta placas** em vez de casar substring, e o denominador chega na tela |
| `c48eda8` | 19:41 | o mapa deixa de chamar de impossível o que ele mesmo já mediu funcionando — 32 células |
| `97c2cbf` | 19:41 | a décima aba medida (693 linhas) + o índice da leva da cor e do som (995 linhas) |

### 1.b A onda 1 da MESA CHEIA — onze entregas, três rodadas de ceticismo

Cada entrega foi julgada por um cético independente que **refazia as mordidas por
conta própria**, com saída de terminal colada. Placar final:

| sustentadas | refutadas |
|---|---|
| **1.1** (a décima aba medida) · **1.2** (trava manual sem lado) · **1.6** (o rumble mira) · **1.7** (ramo sem mesa + plural do doctor) | **1.4** (`_destinos_do_broadcast`) · **1.5** (a frase somada) · **1.11** (o portão de frases) |

As três refutadas continuam abertas e agora têm sprint —
[TRÊS-REFUTADAS-01](2026-08-15-TRES-REFUTADAS-01-o-que-a-terceira-rodada-de-ceticismo-deixou-de-pe.md).

**Números que valem guardar:** a suíte cheia medida por um cético no fim da tarde
deu **9541 passed, 1 skipped, 4 xfailed, 0 failed em 276 s**, com `ruff` limpo,
`mypy` em 174 arquivos, e acentuação/glifos/referências/anonimato saindo zero.

### 1.c As curas de Bluetooth — na máquina dela, NÃO commitadas

Duas, e a segunda é um defeito nosso: `SuccessExitStatus` não cobria o
`Result: timeout`, e o `bt_bonds_restore.sh` derrubava o agente de pareamento
sem religá-lo. **Oito horas sem agente**, que é a queixa *"conectam sozinhos e
desligam em sequência"*. Os quatro controles foram resetados de fábrica por ela e
re-pareados; os quatro estão com `LinkKey` no disco.

Registro completo:
[BONDS-QUE-SUMIAM-01](2026-08-15-BONDS-QUE-SUMIAM-01-o-agente-de-pareamento-que-nos-mesmos-derrubamos.md).

### 1.d A MESA-CHEIA-12 — na árvore, NÃO commitada

Medido em 15/08 às 01h00, com os quatro no rádio: o `state_full` publicava
jogador **1/2/3/4** e as barras acendiam **1/4/2/3**. Três dos quatro diziam uma
coisa na tela e outra no plástico. `player_indexes()` passou a sair de
`numeros_de_jogador()`, a mesma função da lâmpada.

**O que a cura NÃO resolveu está em
[ORDEM-DE-CHEGADA-01](2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md)**,
e é a metade que ela decide.

### 1.e O crash do Mortal Kombat 1 — curado, e FORA deste repositório

`Assertion failed: "!status && vkAllocateMemory"`. A causa: `NV_ERR_NO_MEMORY` em
`system_mem.c` — **RAM de sistema, não VRAM** (havia 7,1 dos 8 GB de VRAM
livres). Curado em **duas camadas globais, nenhuma por appid**:
`vm.min_free_kbytes` 159→512 MB, `vm.extfrag_threshold` 500→100, e
`VKD3D_CONFIG=no_upload_hvv` no ambiente do login gráfico.

**A cura mora na casa dela (`~/.config/zsh/`), não aqui, e já está registrada
lá.** Não duplicar. O que é deste repositório é a licença de desenho dela:

> *"pra todo e qualquer jogo não deveríamos ter essa limitação"*

— receita por appid deixa todo jogo novo desprotegido. **Isso vale para o
`hefesto-launch`**, que é o wrapper que estava no meio daquela linha de comando
quando o jogo quebrou, e é onde a tentação de "uma exceção para este appid" vai
aparecer.

### 1.f Medido NO APARELHO em 14-15/08, e cujo dono é o mapa

**Este bloco é uma rede, não um registro.** O dono destas linhas é o mapa de
canais e a canônica, e havia um agente escrevendo lá enquanto isto era digitado.
**Se elas não estiverem no mapa na próxima sessão, estão aqui** — foi
exatamente assim que o achado da cor de 10/08 se perdeu por cinco dias.

- **A cor está no serial de fábrica.** `SET_FEATURE 0x80` com payload
  `[0x01, 0x13]`, depois `GET_FEATURE 0x81`; o serial tem 17 caracteres ASCII e a
  cor está nos **caracteres 5 e 6**. Três implementações independentes
  concordam. **Exige uma ESCRITA**, na mesma família de comandos de fábrica em
  que `[1,1]` reseta e `[12,1,…]` grava calibração na NVS — por isso é a **D-15**
  e é decisão dela.
- **`hardware_version` do sysfs distingue os quatro de graça** — mas **NÃO é
  cor**: é revisão de placa, e dois controles da mesma cor comprados juntos
  teriam o mesmo valor. Serve de âncora de diagnóstico.
- **`GET_FEATURE` por Bluetooth exige RETRY** (o `REPORT_REQ_TIMEOUT` de 3 s do
  BlueZ; cada falha custa 3,2-3,7 s) **e validação de `buf[0] == report_id`** —
  um dos controles devolveu um report com id `0x80` no lugar do `0x20`. Com as
  duas coisas, **os dezessete feature reports declarados foram lidos nos
  quatro**, o que derruba a linha *"catorze que ninguém nunca leu"*.
- **O acelerômetro por Bluetooth foi MEDIDO e passa**: `|v|` de 0,9945 g e
  0,9823 g contra a régua `res = 8192` do `absinfo`, que é o
  `DS_ACC_RES_PER_G` do driver. **Nenhum byte foi enviado ao controle.**
- **O feature `0x22` nunca foi lido por este projeto** e carrega identidade: o
  MAC em little-endian e **dois blocos de 8 bytes distintos por unidade**.
- **O feature `0xf6` tem 546 bytes — o mesmo tamanho de payload do OUTPUT
  `0x39`**, e não é nomeado em documento nenhum. **Corrigido em 15/08/2026:**
  esta linha dizia *"o gêmeo exato do OUTPUT `0x39` do áudio por rádio"*, e as
  duas metades prometiam demais — igualdade de tamanho é observação, não
  parentesco, e **nenhum degrau da escada está provado carregar áudio**. O que
  se mediu foi o canal: o firmware executa o `common` de 47 bytes no `0x32` e no
  `0x39`, e o conteúdo do payload segue não identificado.

### 1.g O que os agentes derrubados voltaram a fazer

Quatro agentes caíram por limite de sessão em 14/08 (dois em cada workflow). Ela
pediu *"relança os agentes que caíram"* às 19:11. **Os quatro voltaram e
entregaram** — o mapa de canais virou `c48eda8`, o índice da leva virou parte de
`97c2cbf`, e a 1.6 e a 1.7 foram julgadas e sustentadas. **Não relançar de
novo.**

---

## 2. As sete sprints que este índice abre

| sprint | grau | o que cobre |
|---|---|---|
| [TRÊS-REFUTADAS-01](2026-08-15-TRES-REFUTADAS-01-o-que-a-terceira-rodada-de-ceticismo-deixou-de-pe.md) | MEDIDO | 1.4 (três estados opostos com a mesma resposta), 1.5 (a frase é cortada: cabem 127 caracteres, ela tem 182) e 1.11 (o quarto andar da escotilha do portão de frases) |
| [A-LINHA-QUE-DISPENSA-01](2026-08-15-A-LINHA-QUE-DISPENSA-01-o-defeito-mora-onde-a-autora-escreveu-que-nao-precisava-olhar.md) | MEDIDO (processo) | seis vezes em nove refutações o defeito estava na linha do `o_que_ficou_de_fora` — o único parágrafo do relatório que ninguém confere |
| [SOM-DE-CADA-JOGADOR-01](2026-08-15-SOM-DE-CADA-JOGADOR-01-o-botao-que-nunca-funcionou-com-a-mesa-cheia.md) | MEDIDO | o botão que nunca funcionou com 2+ controles, o mute que vai para o microfone errado, a cura por sysfs já provada, e um fato errado no drop-in do WirePlumber |
| [ORDEM-DE-CHEGADA-01](2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md) | MEDIDO | o número de jogador sai da fila gravada por MAC, e ela pediu a ordem de conexão do momento. Colide com R-15/R-23 |
| [QUEM-É-QUEM-01](2026-08-15-QUEM-E-QUEM-01-o-estado-publicado-nao-diz-qual-vpad-e-de-qual-controle.md) | MEDIDO | `coop.players` é um número, `per_vpad` não carrega o nó, e depois da MESA-CHEIA-12 o `player` publicado já não é o número no nome do vpad |
| [A-PORTA-QUE-A-CASA-CONSTRUIU-01](2026-08-15-A-PORTA-QUE-A-CASA-CONSTRUIU-01-os-instrumentos-batem-na-porta-errada.md) | MEDIDO | os quatro DualSense físicos estão `0600` sem ACL porque o produto os esconde de propósito; os instrumentos abrem o nó direto em vez de pedir ao broker |
| **este índice** | REGISTRO | o dia, as decisões dela, e o que quase se perdeu |

**A ordem de execução sugerida**, se houver de escolher:

1. **A-PORTA-QUE-A-CASA-CONSTRUIU-01** — é a única que **bloqueia o que ela vai
   fazer em seguida** (o ENSAIO 2+2);
2. **ORDEM-DE-CHEGADA-01 §E1** — dez minutos dela, e trava as outras duas
   entregas daquela sprint;
3. **SOM-DE-CADA-JOGADOR-01 §E1** — a cura por sysfs é pré-requisito de tudo o
   que ela pediu de áudio;
4. o resto.

---

## 3. O que continua sendo dela — as decisões novas de 14-15/08

Com as palavras dela, porque a paráfrase já custou caro uma vez hoje (§4.1).

| # | ela disse | o que trava |
|---|---|---|
| **1** | *"deve ser lembrado por ordem de conexão naquele momento apenas. **Não uma imagem fixa salva por mec**, o bond mesmo se desfaz com facilidade"* (15/08 03:54) | ORDEM-DE-CHEGADA-01 inteira |
| **2** | *"a nossa ordem deveria sobrescrever a parte da steam inclusive igual quando descobrimos como fazer junto ao lightbar"* (mesma fala) | frente própria, **não medida** nesta sessão |
| **3** | *"vamos conectar dois controles por cabo e 2 sem cabo, vamos usar isso pra irmos isolando o canal exato do cabo e o canal exato via rádio"* (04:20) | o ENSAIO 2+2 — desenho dela, instrumentos em construção |
| **4** | *"o canal 3 do dualsense tem uma saída de som pra efeitos sonoros sfx de cada joguinho… a ideia é conseguirmos usar os 3 mic e os 3 saídas de som de cada controle"* (18:36) | D-26 e D-28 |
| **5** | *"isso inclusive precisamos mapear até nos specs, a parte do microfone, saída de som sfx e, giroscópio, acelerômetro também. **todos via cabo e bt**"* (18:44) | o escopo do mapa — é o que o 2+2 mede |
| **6** | *"pra todo e qualquer jogo não deveríamos ter essa limitação"* (sobre o crash do MK1) | princípio de desenho: nada por appid |
| **7** | *"se no playstation via bt tudo isso funciona é pq tem um meio físico pra isso funcionar e ainda não descobrimos… só falta mapear cientificamente pra tirarmos os achismos nossos do projeto"* (18:48) e *"não faria sentido a sony fazer comercial mostrando essas features no playstation se não existisse e eu mesmo conferi isso várias vezes"* (18:51) | **a regra de prova da leva inteira** — foi ela que produziu a *FALÁCIA DO PERFIL AUSENTE* |

**A nº 7 é a mais valiosa e a mais fácil de perder**, porque não parece uma
decisão: parece conversa. É o princípio que diz *"não anunciar o perfil padrão X
não é prova de não fazer Y"*, e foi ele que derrubou quatro células do mapa que
diziam **IMPOSSÍVEL** sobre coisas que o próprio mapa registra funcionando.

E as **dezessete perguntas D-13 a D-29** continuam **todas abertas**, no índice da
leva da cor e do som. **Nenhuma foi respondida.**

---

## 4. O QUE QUASE SE PERDEU

Esta é a seção que ela pediu. São **onze** coisas que estavam só no transcrito, ou
que dois relatórios diziam diferente, ou que eu afirmei e não conferi.

### 4.1 — A decisão dela sobre a ordem foi citada pela METADE, e a metade que caiu é a que o código contraria

A cura MESA-CHEIA-12 justifica a escolha assim, em dois lugares
(`daemon/subsystems/coop.py:1196` e
`tests/unit/test_mesa_cheia_12_o_desenho_e_o_numero.py:40`):

> *"por decisão dela (`2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador`:
> **"a ordem deve ser por ordem de conexão daquele momento"**)"*

**Duas coisas erradas nessa linha:**

1. **A citação não existe naquele documento.** `grep` por "ordem de conexão" nas
   1289 linhas dele devolve **nada**. A frase só aparece nos dois arquivos que a
   citam. É uma **referência que não resolve** — e o portão de referências da
   casa confere caminhos de arquivo, não citações dentro deles.
2. **A paráfrase perde a segunda metade da frase dela.** O que ela escreveu foi:
   *"deve ser lembrado por ordem de conexão naquele momento apenas. **Não uma
   imagem fixa salva por mec**"*. A cura implementa exatamente a imagem fixa
   salva por MAC (o `rank` do `controllers.json`).

**Por que quase se perdeu:** a frase está no transcrito da conversa e em lugar
nenhum mais. Sem esta página, a próxima sessão leria a justificativa no código,
iria ao índice conferir, não acharia, e teria de escolher entre acreditar no
comentário ou desconfiar dele.

### 4.2 — O que ela pediu foi arrancado desta casa em 23/07, com motivo medido

`daemon/subsystems/identity.py:15-23` registra, sobre a **R-15**, que a
renumeração por ordem de wake foi **REMOVIDA** porque *"trocava cor/número de dono
conforme a ORDEM DE WAKE — desligar os dois DualSense e religar em ordem
invertida devolvia o 1 ao que voltasse primeiro"*, e abria janela de duplicata:
*"a queixa 'dois player 1, dois player 2'"*.

**A decisão nova dela é literalmente o comportamento que a R-15 arrancou.** Isso
não a torna errada — torna o preço real, e é a razão de ORDEM-DE-CHEGADA-01 pôr a
pergunta na mesa em vez de eu escolher.

### 4.3 — A hipótese do "P3 duplicado" não se confirmou, e ninguém escreveu isso

O enunciado que abriu a investigação do LED dizia *"o vpad P3 acende o desenho do
P1 — **DUPLICADO**"*, com o raciocínio *"número repetido costuma vir de índice
que não foi atribuído"*.

**A medição achou outra coisa:** uma **transposição**, não uma duplicata. Os
quatro desenhos foram `[3]`, `[1,2,4,5]`, `[2,4]`, `[1,3,5]` — ou seja **1, 4, 2,
3**: uma bijeção, sem repetição nenhuma. A causa foram **dois espaços de
numeração**, não um índice perdido.

**Por que importa:** quem ler só o enunciado vai caçar um número repetido que não
existe.

### 4.4 — A largura da barra de status está medida ERRADA dentro do repositório

`tests/unit/test_mesa_cheia_09_toasts_honestos.py:315-323` afirma que *"cabem
~183 caracteres"* e que *"a de duas pendências cabe raspando (1123 px de 1156
px)"* — **com a instrução explícita de que serve "para a decisão não precisar ser
remedida"**.

O rótulo real tem **703 px** e cabem **127 caracteres**. **Erro de 1,64x, sempre
para o lado otimista**, porque os 415 px dos quatro botões do rodapé nunca foram
descontados.

**Uma medição errada que se anuncia como definitiva é pior que nenhuma medição.**
Pela regra dela de 11/08, sai por substituição.

### 4.5 — Um relatório de hoje conclui que a regra udev não cobre o Bluetooth. Não é verdade

A conclusão foi: *"a regra `70-ps5-controller.rules` linha 10 deveria cobrir, e só
a linha do vpad pegou"*. Conferido agora:

```
udevadm info -q all -n /dev/hidraw6  →  E: CURRENT_TAGS=:seat:uaccess:
```

**A regra pegou.** Quem tira a ACL é o **próprio Hefesto**, de propósito —
`broker/hidraw_broker.py:417-425`, o `hide` que esconde o físico do Steam Input.

**Por que quase custou caro:** consertar a regra seria consertar o lugar errado, e
a casa já nomeou esse defeito de processo. O conserto certo é outro, e está em
A-PORTA-QUE-A-CASA-CONSTRUIU-01.

### 4.6 — O canal 3: dois modelos, zero prova, e um deles quase virou fato

Um relatório afirmou como **correção assertiva** ao modelo dela que *"canais 3-4 =
os motores voice-coil — não são um segundo destino de som"*, citando
`docs/data/mapa-controles-v1.csv:148` e `:190`.

**Três outros agentes mediram que aquela linha do mapa não tem prova nenhuma:**
ela está sob `aparelho_confianca = inferido-do-codigo`, e a evidência dela é a
**ausência** — a busca na árvore por `voicecoil`, `VCM`, `PCM` e `Surround`
devolve *"apenas comentários… nenhuma linha de implementação"*.

**Os dois modelos estão empatados em zero prova**, e o `chmap FL FR RL RR` não
desempata (é o mapa genérico de surround da USB Audio Class). Só a **D-28**, o
ensaio às cegas, resolve.

**Por que quase se perdeu:** se a afirmação assertiva tivesse entrado no mapa como
fato, o modelo dela — que vem de uso real no PlayStation — teria sido enterrado
por uma linha que não tem mais evidência que ele.

### 4.7 — Dois agentes deram contas opostas sobre o degrau do 0x39, e uma é verificável

Sobre onde cabe o report de áudio por Bluetooth:

- um mediu **1 + 8 + 130 + 402 = 541 B de dados + 4 de CRC = 545**, e concluiu
  que **não cabe** nos 525 do `0x38`, só nos 546 do `0x39` — com **um byte de
  folga**;
- outro afirmou que *"só cabem a partir do `0x38`"*.

**A primeira conta é explícita e refazível; a segunda parece ter omitido os 130 B
do bloco háptico.** Fica registrado qual das duas mostra o cálculo.

### 4.8 — Os tamanhos dos feature reports diferem em ±1 entre agentes, e ninguém declarou a régua

`0x08` = 48 ou 47? `0x0b` = 42 ou 41? `0x22` = 64 ou 63? **As duas leituras estão
certas em réguas diferentes** — com e sem o byte do Report ID —, e **nenhum
relatório declarou qual usou**. Um agente contou 27 report IDs no descritor;
outros dois contaram 17 FEATURE.

É a armadilha nº 1 da casa (*"todo instrumento tem de declarar qual biblioteca
está usando"*) na sua versão mais barata: declarar a **unidade**.

### 4.9 — A mesa mudou durante o dia, e uma medição de áudio virou lenda

O agente do áudio mediu **quatro placas**, com **dois DualSense no cabo**
(`card1` e `card3`). **Quatro horas depois** havia **três placas**, nenhum
DualSense no cabo, e **`card1` era a webcam**.

Um único agente nomeou a armadilha por escrito. **Sem essa linha, "o `card1` tem
4 canais de playback" seria citado amanhã como propriedade do DualSense.**

Nota de contexto para quem ler isto depois: **agora, 15/08 por volta da 01h45,
há de novo dois no cabo e dois no rádio** — a configuração do ENSAIO 2+2. A
numeração de placa mudou outra vez.

### 4.10 — Um estudo de 693 linhas está órfão, e uma sprint velha ainda ensina o errado

`docs/process/estudos/2026-08-14-A-DECIMA-ABA-MEDIDA-…md` foi commitado em
`97c2cbf` e **nenhum documento da casa o cita** — `grep -rln` devolve só ele
mesmo. As onze fotos da mesa cheia em `docs/process/estudos/assets/mesa-cheia/`
estão órfãs do mesmo jeito.

E `docs/process/sprints/2026-08-13-MESA-CHEIA-07-*.md` continua carregando, por
extenso, **duas mordidas que já foram refutadas** (linhas 129 e 139). Quem as
seguir vai escrever um teste que não morde.

### 4.11 — O achado da cor completou CINCO DIAS enterrado, e a página ainda o negava

O caminho da cor (`SET_FEATURE 0x80 [0x01,0x13]` + `GET_FEATURE 0x81`, serial de
17 caracteres, cor nos caracteres 5 e 6) **foi achado nesta casa em 10/08** e
ficou num transcrito de subagente. A sprint `UNIDADE-COR-01` abriu e **não
começou**. E a **D-15**, escrita em 14/08, afirmava o contrário: *"a leitura a
partir do aparelho nunca foi tentada, e eu não achei campo HID que a reporte"*.

**Cinco dias entre saber e a página dizer que não se sabia** — e uma decisão dela
quase foi tomada em cima da negação.

Isso já está registrado no índice da leva (§12.3) e entra aqui porque **é o
motivo de este documento existir**: a cura é de processo, e a Vitória a inventou
sozinha ao mandar escrever esta página.

---

## 5. A conferência — a prova de que este registro não afirma o que não foi feito

Cada item da seção 1 foi reaberto na árvore de agora:

| afirmação | como foi conferida |
|---|---|
| os sete commits | `git log --format='%h %ad %s'` e `git show --stat` nos seis de 19:40-19:41 |
| as curas de BT estão na árvore e não commitadas | `git status --short` e `git diff` nos dois arquivos |
| as curas de BT estão **na máquina dela** | `systemctl cat hefesto-bt-agent.service` traz `KillSignal=SIGKILL`; `diff` contra a fonte sai limpo |
| os quatro bonds com LinkKey | leitura de `/var/lib/bluetooth/*/*/info` |
| a MESA-CHEIA-12 está na árvore | `git diff` de `coop.py`, `ipc_handlers.py`, `base.py` e o teste novo não rastreado |
| a citação inexistente (§4.1) | `grep` nas 1289 linhas do índice da leva |
| a regra udev pegou (§4.5) | `udevadm info -q all -n /dev/hidraw6` |
| os quatro físicos em `0600` sem ACL | `ls -la /dev/hidraw*` + `getfacl` nos doze nós |
| as larguras da frase (§4.4) | `frase_de_guardado` importada do pacote e medida em caracteres |
| o `rank` persistido por MAC | leitura do `controllers.json` dela (mascarado) + `identity.py:588-620` |

**O que este documento NÃO conferiu:** não rodei a suíte (o número de 9541 é de
um cético em 14/08 à tarde, e a árvore mudou desde então), não abri janela
nenhuma, não reiniciei o daemon e não toquei no Bluetooth — ela está com quatro
controles na mesa e um ensaio manual começando.
