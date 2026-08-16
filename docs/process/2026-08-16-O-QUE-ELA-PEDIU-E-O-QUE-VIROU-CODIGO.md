# O que ela pediu, e o que virou código — o censo da madrugada de 15-16/08/2026

- **Escrito em:** 16/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`.
- **Por que existe:** pedido dela, textual, às 00h24 (local): *"manda outro agente
  ver se tudo que conversamos foi transformado em sprints ou solução."*
- **Grau:** este documento é **censo**, não medição. Cada linha aponta um arquivo
  desta árvore, e cada frase dela veio do transcrito da sessão. Nada aqui é
  memória minha.
- **Território:** só este arquivo. Nenhuma outra linha da árvore foi tocada para
  escrevê-lo — o produto desta frente é o censo, e ele não conserta nada.

---

## O placar, em uma tela

| estado | itens |
|---|---|
| **SÓ FICOU NO PAPO** — pedido dela, zero lastro na árvore | **7** |
| **MEDIDO E PERDIDO** — a medição aconteceu e não foi escrita | **1** |
| **VIROU CÓDIGO** — com teste que morde | **9** |
| **VIROU MEDIÇÃO NO CADERNO**, sem código (e é o certo) | **3** |
| **ENTROU HOJE E JÁ ESTÁ ERRADO** — contradição nova | **3** |

A ordem abaixo é a que ela pediu implicitamente ao mandar auditar: **o que se
perde quando a sessão fechar vem primeiro.**

---

# BLOCO A — SÓ FICOU NO PAPO

Sete pedidos explícitos dela que **não existem em arquivo nenhum** desta árvore.
Se o terminal cair agora, isto some.

## A.1 Os TRÊS MODOS de áudio — o requisito de produto que ela fixou

**O que ela pediu**, textual (23h31 local):

> *"entendi, então ao final do projeto, eu espero três modos, trazer o som do
> hdmi e sfx pro controle, só sfx ou só hdmi (pra usar a tela mas não usar o
> output sonoro da tela)."*

**O que existe hoje:** duas menções de passagem, as duas escritas nesta
madrugada e as duas dizendo apenas *"a minha cura não atrapalha os três
modos"* — `assets/wireplumber/54-hefesto-dualsense-alto-falante-nunca-dorme.conf`
(seção "POR QUE CONFIGURAÇÃO") e
`tests/unit/test_o_alto_falante_nunca_dorme_01.py:31`.

**Nenhuma sprint. Nenhuma célula do mapa. Nenhum requisito escrito. Nenhum
código.**

**E há uma armadilha de vocabulário que precisa de decisão dela**, e é
exatamente o tipo de coisa que a casa já aprendeu a não improvisar: o bloco
"Alto-falante" da aba Status **já tem três botões** — "Sons do jogo", "Todo o
som do PC" e "Silenciar" (`profiles/schema.py:440-441`). Eles **não são** os três
modos dela. Os botões dizem *qual rota do firmware está ativa*; ela pediu *o que
entra no controle*:

| o que ela pediu | existe hoje? |
|---|---|
| HDMI **e** SFX no controle | parcialmente — é o que "Todo o som do PC" faz na prática |
| só SFX | parcialmente — é o que "Sons do jogo" faz |
| **só HDMI** (usar a tela sem o som da tela) | **não existe em lugar nenhum** |

Traduzir o pedido dela para o léxico existente é decisão de produto, e não é
minha. **Estado: SÓ FICOU NO PAPO.**

## A.2 O caso do FPS — o som de cada jogador no controle dele

**O que ela pediu**, textual (23h59 local, e ela repetiu a razão):

> *"o som da arma do coleguinha deve sair no controle dele e o meu no meu"*
> — *"pq no ps5 é assim, no sackboy também."*

**O que existe hoje:** o **mecanismo** está no produto e tem teste —
`src/hefesto_dualsense4unix/app/usb_pai.py` casa placa de som e controle pelo
dispositivo USB pai (não por nome, não por MAC, não por ordem), e
`tests/unit/test_a_placa_e_o_controle_pelo_usb_pai.py` trava inclusive o caso
cruzado, em que o nome e o número do card estão em ordens opostas.

**Mas a MEDIÇÃO dela sumiu**, e é o item mais caro deste censo. Ver A.8.

## A.3 Somar L+R antes de mandar ao alto-falante

**Onde nasceu:** ela desconfiou da tabela antes de qualquer medição — *"mas tem
certeza que estamos lendo isso certo? pq não me parece que só o som right sairia
do controle, acho que tá errado a leitura dos bits"* — e a bancada lhe deu razão
às 00h40: com quatro canais nativos ela ouviu só o pulsado do canal direito; com
estéreo no mesmo sink ela ouviu os dois. **Quem somava L+R era o PipeWire, não o
firmware.**

**O que existe hoje:** os dois ensaios estão no caderno (`docs/data/ensaios.csv`,
linhas 173 e 174: `sfx-so-o-R-chega` e `sfx-o-pipewire-e-que-misturava`) e a
consequência está escrita, em prosa, na `cabo_ressalva` da célula
`audio.alto_falante.rota@dualsense` (`docs/data/mapa-controles.csv`, linha 8):
*"quem levar áudio ao alto-falante tem de SOMAR L+R no canal que chega lá."*

**O que NÃO existe:** código, teste, sprint. Eu mesmo disse a ela, textualmente,
*"isso vira uma quarta cura, junto com as três que os agentes já estão fazendo"*
— e as três nasceram, a quarta não. Enquanto isso, o áudio do controle funciona
por política de upmix de uma versão do PipeWire, o que a própria ressalva chama
de **acidente feliz**. **Estado: SÓ FICOU NO PAPO** (a medição está guardada; o
requisito de produto não virou nada).

## A.4 O defeito novo: o leitor de movimento reabrindo a cada 30 segundos

**Onde nasceu:** caçando o som que ela ouviu vindo do lado direito da sala, o
log do daemon mostrou, em 30 segundos de silêncio absoluto, três ciclos de
`motion_reader_silencio_reabrindo` no `hidraw8` — o controle vermelho, no
rádio, com o co-op segurando o grab dele. Ritmo exato de 30,2 s, para sempre, e
cada reabertura desliga e religa o `uhid_motion_streaming`.

**O que existe hoje:** o contador existe no produto
(`core/physical_report_reader.py:805`), mas **o defeito não está registrado em
lugar nenhum**. A única menção na árvore inteira é dentro da `nota` do ensaio
`som-no-radio-observado-nao-replicado` (`docs/data/ensaios.csv:175`), e lá ele
aparece como **não-explicação de outra coisa** — *"que é OUTRO defeito e não
explica 6 s de som contínuo"*. Ou seja: está escrito só o que ele **não** é.

Eu perguntei a ela *"registro o defeito e disparo um agente para ele?"* e a
conversa seguiu para o som antes da resposta. **Estado: SÓ FICOU NO PAPO** — e é
defeito de produto, com custo de bateria e de rádio, num controle que está na
mesa dela agora.

## A.5 O Duskfade — diagnóstico medido, solução recusada, nada escrito

**O que ela pediu** (16h28 local): *"veja o jogo duskfade criei até um perfil pra
ele, tentei mil coisas diferentes mas o jogo não reconhece os controles, sabe o
pq?"*

**E o que ela recusou** (16h44), que é a parte que fixa o rumo:

> *"isso não é solução é gambiarra. o jogo tem reconhecimento nativo do
> dualsense. e mesmo que fosse apenas xbox o produto em si existe pra que as
> mascaras funcionem sempre."*

**O que foi medido:** o binário monta 162 plugins e o **único** de gamepad é
`XInputDevice` — zero SDL, zero RawInput, zero plugin de DualSense — e o
`localconfig` traz `UseSteamControllerConfig = 0`. O vpad é Sony `054c:0df2`, e
o XInput não o enxerga.

**O que existe hoje:** `grep -ri duskfade docs/ src/ scripts/ tests/` devolve
**zero ocorrências**. Nem o diagnóstico, nem o caminho que ela escolheu
("descobrir a engine"), nem uma linha. **Estado: SÓ FICOU NO PAPO**, e é o único
item deste bloco em que a **medição** também se perde junto com o pedido.

## A.6 Os oito "X-Box 360 pad" que mudam o diagnóstico do Duskfade

**Achado de passagem, meu, às 22h56 local:** existem **8** dispositivos
`Microsoft X-Box 360 pad` (`28de:11ff`) nesta máquina agora. A referência
canônica registra uma medição de 11/08 dizendo **"zero espelhos"**.

Isso importa porque muda a conclusão de A.5: se havia o que o XInput enumerar
quando ela testou, a causa da recusa é outra. **Estado: SÓ FICOU NO PAPO** — nem
o número novo entrou na canônica, nem o fato velho foi marcado como caduco. Pela
regra da casa (*"fato errado se SUBSTITUI"*), este é um caso de substituição, não
de nota datada: é contagem, e a contagem mudou.

## A.7 A purga do histórico público, que ela autorizou

**O estado real, conferido agora:**

- A purga **local** foi feita: cinco vazamentos saíram do histórico, com prova
  forte (a árvore ficou byte a byte idêntica) e salva-vidas em
  `refs/salvavidas/2026-08-15-antes-do-filter-repo`.
- A purga **pública** não. Os dois commits de 01/08 com o endereço do controle
  roxo continuam alcançáveis a partir de `origin/restauro/inicio-da-sessao`, e
  eu disse a ela, textualmente, *"a purga do histórico público que você
  autorizou (...) deixei por último de propósito"*.
- **E não há nenhum arquivo desta árvore que registre a pendência.** Procurei os
  dois hashes em `docs/` inteiro: zero ocorrências.

**Estado: SÓ FICOU NO PAPO.** É a mesma classe da senha sudo já registrada na
memória da casa — com a diferença de que aquela está documentada e esta não.

## A.8 (MEDIDO E PERDIDO) O ensaio do FPS deu certo e não foi ao caderno

Este é o item que mais dói, porque não é uma coisa que faltou fazer: **foi
feita, funcionou, e não foi escrita.**

Às 00h08 locais, com dois controles no cabo, dois timbres diferentes saíram
simultaneamente, cada um no seu controle, sem vazar um no outro, com o
casamento feito por dispositivo USB pai. Eu relatei a ela: *"o caso do FPS
funciona no cabo (...) funciona em qualquer PC, com qualquer controle, sem
conhecer MAC."*

**O que existe hoje:** nada em `docs/data/ensaios.csv` — os dezesseis ensaios de
áudio da madrugada vão de `sfx-cabo-sem-posse` (linha 157) a
`sfx-o-pipewire-e-que-misturava` (linha 174), e **nenhum é o do FPS**. Nada em
`docs/data/mapa-controles.csv`. Nada em `specs.html` (zero ocorrências de
"FPS"). O único vestígio na árvore inteira é uma frase na coluna `fonte` de
**outro** ensaio: *"durante o ensaio do FPS (som diferente em cada um dos dois
controles do CABO)"*.

O mecanismo sobreviveu (A.2). A medição, que é o que responde a pergunta dela
sobre o PS5 e o Sackboy, **não**.

## A.9 O touchpad, que ela aceitou medir e ninguém mediu

Às 22h30 locais eu propus e ela respondeu **"vamos fazer esse"**: quatro linhas
do mapa paradas em cabo medido / rádio inferido, e o touchpad é a única peça que
não se mede sem o dedo dela.

O ensaio começou, foi interrompido pela destroca de braços dos controles, e
depois a mesa virou para o áudio e nunca voltou. **Conferido agora:** zero
ensaios de touchpad em `docs/data/ensaios.csv`, e as quatro células
(`toque.touchpad`, `.clique`, `.cursor`, `.escrita`) continuam exatamente como
estavam. **Estado: SÓ FICOU NO PAPO**, com a agravante de que ela estava com os
dois controles na mão e a janela se fechou.

---

# BLOCO B — VIROU CÓDIGO, com teste que morde

Nove pedidos dela que atravessaram inteiros. Todos ainda **sem commit** no
momento em que este censo foi escrito (a árvore tinha 74 arquivos mexidos).

## B.1 "setar o som sempre em todos os controles no 100%"

Frase dela, 23h45 local, e é a mais consequente da noite porque **explica o
silêncio**: sem posse dos bytes de volume, o daemon escrevia zero em todo
report.

- `core/backend_pydualsense.py:319` — `VOLUME_PADRAO_DO_SOM`
- `core/backend_pydualsense.py:2176` e `:3543` — a posse é tomada **na adoção**
  de cada controle, sem clique
- `tests/unit/test_som_sempre_01_o_volume_nasce_em_cem.py` — seis travas

**Detalhe que vale registrar:** o número escolhido foi **102**, não 100 nem 255,
por medição (com 255 o byte do fone grampeia em 127 e fone e alto-falante
divergiriam em silêncio). **Estado: VIROU CÓDIGO.**

## B.2 "garantir que sempre fique acordado"

- `assets/wireplumber/54-hefesto-dualsense-alto-falante-nunca-dorme.conf` — a
  regra que zera o `session.suspend-timeout-seconds` só dos nós de saída do
  DualSense
- `install.sh:1146` — entra **sem flag**, como manda a regra da casa
- `uninstall.sh:141` e `:511` — sai pelo mesmo caminho
- `tests/unit/test_o_alto_falante_nunca_dorme_01.py`

O aquecedor (fluxo inaudível) foi **recusado por escrito**, com os três motivos
no cabeçalho do arquivo. **Estado: VIROU CÓDIGO.**

## B.3 "ligar isso a interface na aba de status (config default)"

- `app/audio_saida.py` — leitura do estado dos sinks e os textos do sono
- `app/actions/status_actions.py:920`, `:1030`, `:1237`
- `tests/unit/test_som_acordado_01_os_dois_estados_na_aba_status.py`

**Ressalva de processo:** por PROVA-DE-TELA-01, isto **ainda não fechou** — a
palavra final é dela, e ela não viu a tela depois da mudança.

## B.4 A regressão do bipe na interface

Frase dela, 23h03 local: *"vc conseguiu resolver um problema tenso pq hj em dia
na interface nem por cabo esse bip tá saindo viu"* — e, quando duvidei, *"mas já
funcionou antes"*.

A causa foi achada e curada: o som de confirmação tem 67 ms, e num nó suspenso
o religar do hardware come exatamente o começo. `app/audio_saida.py:537` documenta
`REGRESSÃO-DO-BIPE-01` e o degrau 6.5 (acordar o sink depois das recusas
baratas, usando a lista que já foi lida). **Estado: VIROU CÓDIGO — e falta o
ouvido dela na janela**, que é onde ela relatou o defeito.

## B.5 O eixo que chega ao jogo como 128

Ela leu o achado e cobrou: *"isso virou trabalho já inserido na nossa interface e
no install? caso contrário dispara agentes pra isso."*

- `core/evdev_reader.py:158` — `posicoes_de_eixo`, o irmão do `faixas_de_eixo`
- `core/evdev_reader.py:1345` — a semeadura no `_on_device_opened`
- `tests/unit/test_semente_do_repouso_o_eixo_parado_chega_como_128.py`

**Estado: VIROU CÓDIGO.**

## B.6 A lista MAC para vpad no estado publicado

Mesma cobrança dela, mesma leva.

- `daemon/subsystems/coop.py:378` e `daemon/ipc_handlers.py`
- `tests/unit/test_quem_e_quem_01_o_estado_diz_qual_vpad.py`
- `tests/unit/test_quem_e_quem_01_na_tela.py`
- Sprint: [QUEM-E-QUEM-01](sprints/2026-08-15-QUEM-E-QUEM-01-o-estado-publicado-nao-diz-qual-vpad-e-de-qual-controle.md)

**Estado: VIROU CÓDIGO.**

## B.7 Os atalhos de jogo duplicados

Pedido dela, 21h51 local: *"no .desktop todos os jogos tão duplicados pode mandar
um agente resolver na origem também?"*

Curado **na origem**, e a premissa que eu tinha estava errada — os duplicados não
eram da Steam, eram resquício do resgate do BleachBit de 14/08. Conferido agora:
zero `steam_app_*` e 24 `meow-steam-*` na pasta de atalhos.

**A cura está FORA deste repositório** — o gerador é o
`jogos_steam.sh` do repositório `MeowSystem` dela <!-- ref-externa: a ausência dele NESTA árvore é o assunto do parágrafo -->
e por isso **nada aqui registra que ela existe**. É o mesmo padrão do
BleachBit de 14/08, que só sobreviveu por estar na memória da casa.


## B.8 O teste que sujava o journal dela

Ela citou de memória: *"temos histórico de testes que seguem impactando mesmo
após rodar a suíte"*. Estava certa. A suíte escrevia 3.221 linhas no journal do
sistema, 36 delas mentindo que o `bluetooth.service` tinha morrido — e essas
linhas falsas me custaram vinte minutos de investigação errada na mesma noite.

Curado em `tests/conftest.py` e nos seis `scripts/bt_*.sh`, com fail-safe para
que nenhum teste futuro precise lembrar. **Estado: VIROU CÓDIGO.**

## B.9 O Glade que ficou para trás

Ela pegou, 22h41 local: *"O agente corrigiu o código (...) Esqueceu o Glade"*, e
completou com a correção de fato: *"falso, no próprio projeto já fizemos isso,
deveria tá mapeado inclusive no specs"*.

Conferido: `gui/main.glade` tem **zero** ocorrências de "placa". Corrigido. Mas
ver **D.1** — a mesma confusão voltou por outra porta na mesma madrugada.

## B.10 (não era pedido, era pergunta) O mypy no install

*"esse tipo de coisa não deveria tá nos requirements e install?"* — já estava, e
já era um defeito nomeado e curado (`pyproject.toml:48`, extra `[dev]` por
padrão em `install.sh`). **Nada a fazer**, e está aqui só para a pergunta não
parecer esquecida.

---

# BLOCO C — VIROU MEDIÇÃO NO CADERNO, e é o certo

## C.1 Os três casos de som que ela desenhou

Desenho dela: *"façamos um teste de som sair pela tv tipo AAAAAA e no controle
apenas um BBêeee. Sons diferentes."* E o pedido de guardar: *"Salva esse teste no
specs, não podemos perder."*

- `scripts/ensaios/tres_casos_de_som.py` — o instrumento, com o desenho dela
  citado no cabeçalho e a razão dos dois timbres opostos
- `docs/data/ensaios.csv` — `sfx-cabo-hdmi-negativo`, `sfx-cabo-todo-o-som`,
  `sfx-cabo-caso3-os-dois-juntos`

**Cumprido.**

## C.2 O mapa dos quatro canais de áudio — a primeira vez que existe

Dezesseis ensaios com a orelha dela, em teste cego, das 23h05 às 00h40. O canal 1
alcança o alto-falante; o 0 vai para o fone esquerdo; o 2 e o 3 não vão a lugar
nenhum. Tudo em `docs/data/ensaios.csv:157-174` e na célula
`audio.alto_falante.rota@dualsense` do mapa.

## C.3 A observação NÃO replicada do som no rádio

Ela ouviu, do lado direito da sala, o timbre exato que eu mandava a outro
controle — e o único aparelho daquele lado estava no rádio, sem placa de som
nenhuma. Quatro tentativas de réplica, todas negativas.

Está guardado exatamente como ela quer que se guarde a observação dela:
`docs/data/ensaios.csv:175`, resultado **inconclusivo**, com as quatro tentativas
nomeadas, o que foi descartado, e o que falta capturar se voltar a acontecer.
**Cumprido — e este é o item que mais me preocupava perder.**

---

# BLOCO D — entrou hoje e já está errado

Três coisas que **nasceram nesta madrugada** e já contradizem o que ela decidiu
ou o que a árvore mede. Não são pedidos dela; são dívidas que a leva criou.

## D.1 A interface voltou a dizer que o controle não tem alto-falante

Ela corrigiu isso às 22h41: um agente tinha trocado "alto-falante" por "placa de
som" nos textos achando que era mais honesto, e ela derrubou — o alto-falante
está medido com a orelha dela desde 02/08, com controle negativo.

**E o texto novo escrito depois disso, nesta mesma madrugada, repete a
confusão:**

`app/audio_saida.py:1006`

    TEXTO_SONO_SEM_PLACA = "Sem placa de som do controle (no rádio não existe alto-falante)"

O alto-falante **existe** no aparelho. O que não existe no rádio é a **placa
ALSA** — que é o que o próprio comentário três linhas acima diz corretamente. O
texto que vai para a tela dela diz outra coisa. É `str` exportado, usado em
`:1058` e travado por `tests/unit/test_o_alto_falante_nunca_dorme_01.py:580`, ou
seja: **há um teste segurando a frase errada.**

## D.2 O mapa ainda promete a cura que já entrou, e é outra cura

A `cabo_ressalva` de `audio.alto_falante.rota@dualsense` termina dizendo:

> *"A cura é manter o canal aquecido (fluxo inaudível de 1 LSB), e ela ainda NÃO
> está no produto."*

Caducou na mesma madrugada, e nos dois sentidos: a cura **entrou** (B.2), e **não
é essa** — o aquecedor foi analisado e **recusado por escrito**, em favor da
regra do WirePlumber. Pela regra da casa isto é fato errado, e sai; a decisão
medida que fica é o porquê da recusa, que já está no cabeçalho do drop-in 54.

## D.3 O susto do touchpad do vpad foi alarme falso, e ninguém escreveu isso

Quando ela relatou que algo estava *"digitando e mudando o som direto"*, eu
afirmei, com convicção, que os quatro touchpads dos vpads estavam expostos ao
desktop e que `ID_INPUT_IGNORE` não estava setado em nenhum — e cheguei a propor
mexer em `/etc/udev/rules.d/` com sudo, na máquina dela, de madrugada.

**Medido agora, nos quatro nós vivos:** os quatro têm
`LIBINPUT_IGNORE_DEVICE=1`, posto pela regra
`assets/76-dualsense-touchpad-libinput-ignore.rules`, que **já está instalada**
em `/etc/udev/rules.d/`. Eu tinha conferido a variável errada.

A hipótese foi abandonada quando ela me corrigiu (*"não tinha toque algum nos
controles"*), mas **a retratação nunca foi escrita** — e o que ficou na memória
da conversa é o alarme, não o desmentido. Fica aqui.

---

# O que este censo NÃO varreu, e por quê

Honestidade sobre a cobertura, porque um censo que não declara os próprios
buracos vale menos que nenhum:

1. **Só varri o transcrito desta sessão** (a que começou às 18h46 UTC de 15/08 e
   seguiu pela madrugada). A sessão que morreu às 14h50 e a madrugada anterior
   foram lidas só pelas falas dela, não integralmente — e a primeira é curta e
   trata da lightbar do controle branco, que já virou o estudo
   [A-LIGHTBAR-TRAVADA](estudos/2026-08-15-A-LIGHTBAR-TRAVADA-o-que-ja-caiu-e-o-que-nunca-foi-tentado.md).
2. **Não auditei os relatórios dos subagentes um a um.** Onze workflows rodaram
   nesta sessão; conferi o que eles **entregaram na árvore**, não o que eles
   **disseram** ter entregado. Onde o agente relatou uma pendência no campo
   `naoFeito`, ela pode não estar neste censo.
3. **Não conferi o commit final.** Enquanto eu escrevia, outro agente estava
   fechando a leva em commits — os itens do BLOCO B podem já estar commitados
   quando você ler isto, e os do BLOCO A não estarão, porque não existem.
4. **Não toquei no hardware.** A mesa estava em uso. Toda afirmação sobre
   aparelho neste documento vem do caderno de ensaios ou do transcrito, nunca de
   medição minha. As duas exceções são leituras puras de `udev` e da pasta de
   atalhos, feitas para conferir D.3 e B.7.
5. **Uma coisa segue sem explicação, e não é pedido dela:** os applets do painel
   do COSMIC morreram todos com SIGKILL às 18h11 locais, e a hipótese de falta de
   memória que construí em cima disso **eu mesmo derrubei** depois (o
   `earlyoom` registrava 52-55% de memória livre; os oito "oom-kill" eram as
   linhas falsas do B.8). Fica sem causa.

---

## Se você só tiver dez minutos

Os três que somem e custam mais caro:

1. **O ensaio do FPS** (A.8) — funcionou, ela viu, e não está escrito.
2. **Os três modos** (A.1) — é o requisito de produto que ela fixou para o fim do
   projeto, e a única coisa que existe dele é um teste dizendo que não o
   atrapalha.
3. **O leitor de movimento em laço** (A.4) — defeito de produto vivo, num
   controle na mesa dela, cutucando o aparelho a cada 30 segundos.
