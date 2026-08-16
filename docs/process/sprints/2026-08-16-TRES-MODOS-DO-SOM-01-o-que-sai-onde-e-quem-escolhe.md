# TRÊS MODOS DO SOM 01 — o que sai onde, e quem escolhe

> **O QUE ISTO CUSTA DE VOCÊ:** **quinze minutos de leitura e cinco decisões**
> (seção 11). **Zero de bancada** — tudo o que esta página afirma sobre o
> aparelho já foi medido com a sua orelha na madrugada de 15-16/08. A única
> coisa que pode voltar à bancada é o ensaio do FPS, e só se ninguém tiver mais
> o transcrito em que ele aconteceu (§7.1).

- **Escrito em:** 16/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `58ca918`, com a árvore suja.
- **Grau:** **REQUISITO + DESENHO.** Nada aqui foi executado. Nenhum
  `/dev/hidraw` foi aberto, nenhum byte foi escrito em controle nenhum, o daemon
  não foi reiniciado e o hardware não foi tocado. Toda afirmação sobre o
  aparelho vem do caderno de ensaios; toda afirmação sobre o produto vem de
  leitura do fonte, com endereço.
- **Nasceu de:** o item **A.1** do censo
  [O QUE ELA PEDIU E O QUE VIROU CÓDIGO](../2026-08-16-O-QUE-ELA-PEDIU-E-O-QUE-VIROU-CODIGO.md)
  — o único pedido dela desta sessão que não existia em arquivo nenhum.
- **Depende de:** as cinco decisões da §11 para tudo o que é palavra de tela.
  A ONDA 2 (o L+R) **não depende de nada**. A ONDA 5 depende da frente do rádio
  ([ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
  e [E-5 O TERRENO](2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md)).
- **Custo mínimo estimado:** 6 h 20 de execução, somando as quatro ondas que não
  dependem do rádio. **Estimado, não medido.**

---

## 1. O que ela pediu, e por que é requisito e não sugestão

Textual, 16/08/2026, 00h05 (local):

> *"entendi, então ao final do projeto, eu espero três modos, trazer o som do
> hdmi e sfx pro controle, só sfx ou só hdmi (pra usar a tela mas não usar o
> output sonoro da tela)."*

**"ao final do projeto, eu espero"** é a formulação que ela usa para fixar
requisito, não para propor ideia. E a razão de existir desta página é que, até
agora, a **única** menção dos três modos em toda a árvore era um comentário
dizendo que outra cura *não os atrapalha*
(`assets/wireplumber/54-hefesto-dualsense-alto-falante-nunca-dorme.conf`, seção
"POR QUE CONFIGURAÇÃO", motivo 3, e o teste
`tests/unit/test_o_alto_falante_nunca_dorme_01.py`). Um requisito que só existe
como ressalva de outro trabalho é um requisito que a próxima sessão não vai
encontrar.

A frase tem um antecedente de 14/08 que explica de onde ela vem, e é dela também:

> *"o canal 3 do dualsense tem uma saída de som pra efeitos sonoros sfx de cada
> joguinho (diferente da saída padrão do hdmi) (...) sackboy por exemplo no
> playstation funciona assim"*

**Esse antecedente foi respondido por medição na mesma madrugada, e a resposta
muda o desenho dos três modos.** Ver §3.2.

---

## 2. Confira a minha leitura — os três modos, e as duas chaves

A tradução que eu faço do pedido dela:

| modo | nome que eu leio | o que entra no controle | o que sobra na TV |
|---|---|---|---|
| **1** | HDMI **e** SFX | o som do sistema **e** os efeitos do jogo | nada |
| **2** | só SFX | só os efeitos do jogo | o resto |
| **3** | só HDMI | o som que hoje vai para a TV | **nada — é o ponto** |

O modo 3 tem a razão escrita no próprio pedido: *"pra usar a tela mas não usar o
output sonoro da tela"*. Não é sobre jogo. É sobre olhar a TV e ouvir pelo
controle.

### 2.1 Os três modos são todos decisões da MESMA camada, e não é a que o produto governa

Há três camadas no caminho do som, e confundi-las é o que faz a tela prometer o
que o byte não entrega:

| camada | quem manda | o que ela decide | o produto governa? |
|---|---|---|---|
| **1 — o destino padrão** | PipeWire (`default sink`) | para onde vai o som de quem não escolheu destino | **sim** — `app/audio_saida.py:757`, `RotaDeSaida` |
| **1b — o destino de UM fluxo** | PipeWire (`sink-input`) | para onde vai o som de **um processo** | **não** — zero linhas na árvore |
| **2 — a rota dentro do controle** | firmware (`OUTPUT_PATH_SEL`) | se o canal que chegou sai no fone ou no alto-falante | **sim** — `core/backend_pydualsense.py:259-287` |

**Os três modos dela são todos perguntas da camada 1.** *"O que entra no
controle"* é escolha de destino de fluxo, e acontece antes de o som chegar ao
aparelho. A camada 2 só decide o que fazer com o que **já chegou**.

E é aqui que está o defeito de fundo desta sprint: **o produto governa bem a
camada 2, governa a camada 1 pela metade, e não governa a 1b — que é justamente
a que o modo 2 exige.**

### 2.2 O quadro das duas chaves, e o que ele revela

Cada modo é uma combinação de duas chaves independentes:

```
                          o SFX do jogo
                     TV                 CONTROLE
              ┌────────────────────┬────────────────────┐
   o som   TV │  (o padrão de hoje)│      MODO 2        │
   geral      │   nada no controle │     "só sfx"       │
  (HDMI)      ├────────────────────┼────────────────────┤
     CONTROLE │      MODO 3        │      MODO 1        │
              │    "só hdmi"       │   "hdmi e sfx"     │
              └────────────────────┴────────────────────┘
```

**E aqui está a leitura que pode estar errada, e por isso ela vira a pergunta
P-1 da §12:** as duas colunas só são colunas diferentes **se o SFX for um fluxo
separado do som geral**. Quando o jogo manda tudo por um caminho só — que é o
caso em praticamente todo jogo de Linux —, a coluna some, e o quadro vira uma
chave só:

- **MODO 1 e MODO 3 são o MESMO gesto**, e o gesto já existe: trocar o sink
  padrão.
- **MODO 2 não tem gesto nenhum**, porque não há o que separar.

Isto não é um detalhe de implementação: é o formato da tela. Oferecer três
portas que dão em dois quartos é exatamente o tipo de coisa que esta casa chama
de inventar dado na interface.

---

## 3. O que já existe MEDIDO — o terreno, com a fonte de cada linha

### 3.1 O mapa dos quatro canais, e as três saídas físicas

Medido com a orelha dela, em teste cego, 15-16/08, no cabo, um canal por vez,
com o nó do PipeWire mantido em `RUNNING` e conferido antes de cada passada
(`docs/data/ensaios.csv`, ensaios `sfx-canal1-e-o-alto-falante`,
`sfx-canal0-nao-alimenta`, `sfx-canal2-nao-alimenta`, `sfx-canal3-nao-alimenta`,
`sfx-tres-saidas-quatro-canais`):

```
    canal 0   front-left    ->  fone L                     · NÃO chega ao alto-falante
    canal 1   front-right   ->  fone R (com fone)          · ALTO-FALANTE (sem fone)
    canal 2   rear-left     ->  nada, em passada nenhuma
    canal 3   rear-right    ->  nada, em passada nenhuma
```

**Três saídas físicas, quatro canais ALSA. Dois não têm destino.**

### 3.2 O que isso responde da hipótese dela de 14/08 — e o que NÃO responde

A hipótese *"o canal 3 do DualSense tem uma saída de som pra SFX"* tinha, em
14/08, **zero prova dos dois lados** (era a D-28, e está na
[SOM-DE-CADA-JOGADOR-01](2026-08-15-SOM-DE-CADA-JOGADOR-01-o-botao-que-nunca-funcionou-com-a-mesa-cheia.md)
§4). **O ensaio às cegas que ela pediu foi feito, e a resposta é a §3.1:** neste
aparelho, nesta máquina, os canais traseiros não alimentam nada. **Não existe um
canal dedicado a SFX no DualSense.**

**E o que isto NÃO diz, porque a formulação errada aqui vira fato falso amanhã:**
não diz que ela viu errado no PlayStation. Diz que, se o Sackboy manda efeito
para o alto-falante do controle no PS5, ele **não** faz isso por um quarto canal
de placa de som. Faz por o jogo **declarar** um destino ao sistema — e isso é
API, não fio. **GRAU: o lado do DualSense é MEDIDO; o lado do PS5 é RACIOCÍNIO,
e ninguém aqui mediu um PS5.**

Essa distinção é o assunto inteiro da §4.

### 3.3 As cinco causas isoladas na madrugada, cada uma com par com/sem

| # | o que foi isolado | ensaio | consequência para os modos |
|---|---|---|---|
| 1 | **A posse do volume.** Sem ela o daemon escreve ZERO em todo report e tudo cala. Dose-resposta: nunca escrito = mudo · 85 = soa · 0 = mudo | `sfx-cabo-sem-posse`, `sfx-cabo-com-posse`, `sfx-cabo-volume-zero` | **já curado** — `VOLUME_PADRAO_DO_SOM` em `core/backend_pydualsense.py:319`, tomado na adoção |
| 2 | **O nó suspenso come o começo do som.** O bipe da interface tem 67 ms; o começo comido é o som inteiro | `sfx-no-suspenso-come-o-comeco`, `sfx-no-acordado-nao-come` | **já curado** — o drop-in 54 do WirePlumber, sem flag no `install.sh` |
| 3 | **O fone manda por cima da rota.** Mesma rota, mesmo canal, o destino troca conforme o fone. Confirmado três vezes | `sfx-o-fone-manda-por-cima` | **aberto** — é a pergunta **P-2** |
| 4 | **A rota 2 funciona**, e foi exercida pela primeira vez em 16/08 (só a 3 tinha sido, em 02/08) | `sfx-rota2-sem-fone` | é o mais próximo do modo 2 que o aparelho oferece — e não é a mesma coisa (§4) |
| 5 | **Só o canal R chega ao alto-falante.** Com 4 canais nativos o L se perde; com estéreo ele chega, e **quem soma L+R é o PipeWire**, não o firmware | `sfx-so-o-R-chega`, `sfx-o-pipewire-e-que-misturava` | **aberto** — é a ONDA 2, e vale para os três modos |

### 3.4 O que a tela oferece HOJE, com endereço

Não são três botões. É **um seletor de dois estados** mais um botão de mudo, e
os três respondem perguntas diferentes:

| na tela | endereço | o que faz de verdade |
|---|---|---|
| `O que sai no controle:` | `app/widgets/controller_card.py:583` | a pergunta do seletor |
| **"Sons do jogo"** | `:593`, `:607-610`, rota **2** em `:638-641` | escreve `OUTPUT_PATH_SEL=2` **e devolve o sink padrão ao que era** |
| **"Todo o som do PC"** | `:594`, rota **3** em `:638-641` | escreve `OUTPUT_PATH_SEL=3` **e troca o sink padrão para o do controle** |
| **"Silenciar"** | `:655` | manda volume zero ao firmware. Responde *se* há som, não *onde* |
| **"Ouvir no controle" / "Voltar ao anterior"** | `app/audio_saida.py:612-613`, `:820`, `:865` | o par da aba Status, camada 1 pura |

E o perfil já guarda a rota (`profiles/schema.py:466`), com o **LIMITE
DECLARADO** escrito em `:456`: o sink padrão *"é um fato GLOBAL do sistema e não
é campo de perfil"*. Esse limite é a pergunta **P-4**.

---

## 4. O modo 2 é o difícil, e a razão não está no controle

**"Só o SFX" pressupõe que o jogo mande o efeito por um caminho separado do som
geral.** No PS5 há esse conceito. No Linux não há: o jogo abre um fluxo e manda
tudo por ele. Nenhum produto fora do jogo consegue separar trilha de efeito
dentro de um fluxo já misturado — e tentar seria adivinhação, não roteamento.

Existem **três aproximações** do modo 2. Nenhuma é ele, e a diferença entre elas
é por onde cortam:

| aproximação | corta por | existe? | o que entrega |
|---|---|---|---|
| **(a) a rota 2 do firmware** — `L -> fone, R -> ALTO-FALANTE` | **CANAL** | **sim, medido** (`sfx-rota2-sem-fone`) | metade do estéreo no alto-falante e metade no fone. É o caso Zelda, e só faz sentido **com fone plugado** |
| **(b) mover o fluxo do jogo** para a placa do controle | **PROCESSO** | **não** — zero linhas na árvore | *"só o jogo"*, com trilha e tudo. Não é *"só o SFX"* |
| **(c) o jogo declarar dois destinos** | **TIPO DE SOM** | **não, e não depende de nós** | o modo 2 de verdade |

### 4.1 O defeito que este quadro revela: o modo 2 tem o byte e não tem o fluxo

**"Sons do jogo" é um botão da camada 2 com nome de camada 1.** Leia o que ele
faz, em ordem (`app/widgets/controller_card.py:3756` em diante):

1. escreve `OUTPUT_PATH_SEL=2` no controle endereçado;
2. chama `pedir_rota_do_sistema(False)` — que **devolve** o sink padrão ao
   anterior, isto é, à TV.

Ou seja: o som do jogo continua indo para a TV, a placa de som do controle não
recebe fluxo nenhum, e o byte da rota decide o destino de um som que não chega.
**O resultado audível é silêncio no controle** — e o byte está certo.

O botão só cumpre o que promete se **outra pessoa** já tiver movido o jogo para
a placa do controle (à mão, no pavucontrol ou no painel do sistema). Isto é, ele
depende exatamente da aproximação **(b)**, que o produto não faz.

A dica de tela já admite metade disso — *"Depende do jogo ter essa opção"*
(`controller_card.py:616-621`) —, mas atribui ao jogo uma falta que hoje é
**nossa**: mover o fluxo é trabalho de camada 1b, e é possível sem ajuda de jogo
nenhum. O que **depende do jogo** é separar SFX de trilha. São duas faltas
diferentes, e a frase de hoje mistura as duas.

**Registrado, e não consertado aqui:** a frase é palavra de tela, e por
PROVA-DE-TELA-01 é dela. Está na ONDA 3.

### 4.2 A honestidade que a sprint tem de sustentar

A frase que pode ser copiada daqui para qualquer outro documento:

> **O modo 2, do jeito que ela o descreveu, não é entregável sem o jogo.** O que
> é entregável é *"só o jogo no controle"* (mover o fluxo do processo) e *"o
> estéreo repartido entre fone e alto-falante"* (a rota 2). Os dois são úteis,
> nenhum dos dois é *"só o SFX"*, e chamar qualquer um dos dois de modo 2 seria
> prometer o que não se cumpre.

---

## 5. O modo 3 é o mais fácil, e ninguém tinha pensado nele

**Ele já funciona, e foi medido.** Trocar o sink padrão para o do controle leva
o som do sistema inteiro ao alto-falante — e, como a TV deixa de receber fluxo,
ela cala sozinha. É exatamente *"usar a tela mas não usar o output sonoro da
tela"*.

Medido no caso 3 da bancada (`sfx-cabo-todo-o-som`, 15/08 23h12): o mesmo
arquivo que 20 minutos antes saíra pela TV, tocado **sem alvo**, e ela relatou,
sem saber o que fora enviado: *"tuc hmmmmmm no controle"*. O par negativo está
ao lado (`sfx-cabo-o-mesmo-som-troca-de-lugar`): com o padrão no HDMI, o mesmo
arquivo saiu pela TV e o controle ficou mudo. **Só o sink padrão mudou entre as
duas passadas.**

E o gesto está no produto desde antes: é o `CANAL_TODO_O_PC` do card e o par
`RotaDeSaida.mandar_para_o_controle` / `voltar_ao_anterior`
(`app/audio_saida.py:820`, `:865`), com o sink anterior guardado em preferência
(`CHAVE_PREF_ROTA_ANTERIOR`, `:84`) para a volta não depender de memória.

**O que falta no modo 3 não é mecanismo. É nome.** Hoje ele se chama "Todo o som
do PC", que descreve o que entra e não o que ela quer dele. Ela pediu o modo
pelo **efeito**: a TV cala. Um nome que diga isso é palavra de tela — P-1.

**E há um detalhe medido que o modo 3 herda de graça:** o `tuc` inicial do
relato dela **não está explicado**. Pode ser o despertar do alto-falante, pode
ser a troca de sink, e não foi medido (está escrito assim no próprio ensaio).
Com o drop-in 54 instalado, a hipótese do despertar deixa de valer — o que faz
disso um ensaio de repetição barato, e ele está na ONDA 1.

---

## 6. O L+R — a cura de produto que os três modos exigem

Isto vale para **qualquer** modo que leve som ao alto-falante, e por isso não
depende de decisão nenhuma dela.

**Medido em 16/08 00h40, com par com/sem:**

- arquivo de **quatro canais nativos** (grave só no front-left, pulsado só no
  front-right): ela ouviu **só o pulsado**. O canal esquerdo **não chega**.
- arquivo **estéreo** no mesmo sink de quatro canais: ela ouviu **os dois**.

A única diferença entre as passadas é o número de canais do arquivo. Logo **quem
somou L+R foi a conversão 2->4 do PipeWire**, não o firmware. A pergunta dela,
textual, ao ver isso: *"então quem faz funcionar é o pipewire? isso tá
registrado?"*. Está — na `cabo_ressalva` de `audio.alto_falante.rota@dualsense`
(`docs/data/mapa-controles.csv`), que também nomeia os três casos em que o
acidente feliz some, e nenhum é exótico:

1. jogo que emita **quatro canais nativos** — não há conversão, e o L cai;
2. política de upmix diferente noutra distro ou noutra versão do PipeWire;
3. áudio que chegue por caminho que não passe por essa conversão.

**O requisito:** o que chegar ao canal que alimenta o alto-falante tem de ser
**L+R somado**, e a soma tem de ser nossa. Dois desenhos possíveis, com o preço
de cada um:

| desenho | o que é | preço |
|---|---|---|
| **(A) regra de sistema** | um drop-in de WirePlumber que apresente o sink do DualSense com um mapa de canais em que o alto-falante receba a soma, em vez de deixar a política de upmix decidir | mexemos no áudio da máquina dela — **mas é o diretório que o produto já governa** desde 25/07 (drop-ins 51, 52, 53, 54), instalado e removido pelo mesmo caminho. É a mesma escolha, e pelas mesmas razões, que a `SOM-QUE-NAO-DORME-01` já fez e escreveu |
| **(B) caminho próprio do produto** | um nó de conversão nosso entre quem toca e a placa do controle | o produto vira dono do caminho de saída — que é **exatamente** o motivo pelo qual o aquecedor foi recusado por escrito no cabeçalho do drop-in 54, motivo 3. Repetir aqui a decisão que já foi tomada lá seria contradizer a casa |

**Recomendação:** (A), pela coerência com a decisão já escrita. **Não é decisão
minha se ela custar um comportamento visível na tela dela** — e é a pergunta
**P-5**.

**O que NÃO fazer, e é o mais importante desta seção:** deixar como está. Hoje o
áudio do controle funciona por política de upmix de uma versão do PipeWire, e o
próprio mapa chama isso de **acidente feliz**. Um produto não se apoia em
acidente.

---

## 7. O caso do FPS — o que é possível hoje, o que depende do jogo

Ela foi explícita, 15/08 23h59:

> *"o som da arma do coleguinha deve sair no controle dele e o meu no meu"*
> — *"pq no ps5 é assim, no sackboy também."*

### 7.1 Metade disto está MEDIDA, e a medição não está no caderno

Em 16/08 às 00h08, com **dois controles no cabo**, dois timbres diferentes
saíram **ao mesmo tempo**, cada um no seu controle, **sem vazar**: ela ouviu
`hmmmmmm` no azul e `bipbipbip` no roxo. O casamento foi feito pelo **dispositivo
USB pai** — não por MAC, não por nome, não por ordem de enumeração —, o que faz
o mecanismo valer em qualquer PC, com qualquer controle.

**E este ensaio não está em `docs/data/ensaios.csv`.** Os dezesseis ensaios de
áudio da madrugada vão de `sfx-cabo-sem-posse` a `sfx-o-pipewire-e-que-misturava`
e nenhum é o do FPS; o único vestígio na árvore é uma frase na coluna `fonte` de
**outro** ensaio (`som-no-radio-observado-nao-replicado`). É o item **A.8** do
censo, e é o mais caro dele: a medição aconteceu, funcionou, e não foi escrita.

**A ONDA 1 é escrever esse ensaio**, e há uma condição honesta: **quem o
escrever precisa do transcrito em que ele aconteceu.** Reconstruir o protocolo
de memória seria inventar medição. Se o transcrito não estiver mais disponível,
o ensaio volta à bancada — dois controles no cabo, dois timbres opostos, teste
cego — e custa **cerca de 6 minutos de ouvido dela**. **Estimado.**

### 7.2 O mecanismo está no produto, e tem teste

`src/hefesto_dualsense4unix/app/usb_pai.py` sobe o sysfs a partir do hidraw e a
partir da placa ALSA até o nó que declara `idVendor`, e casa os dois pelo
dispositivo em comum (`dispositivo_usb_pai`, `:68`; `usb_pai_por_uniq`, `:161`).
`tests/unit/test_a_placa_e_o_controle_pelo_usb_pai.py` trava inclusive o caso
cruzado, em que o nome e o número do card estão em ordens opostas.

**Logo: o produto sabe, hoje, qual placa de som é de qual controle.** Isso é
metade do caso do FPS, e é a metade difícil de descobrir.

### 7.3 A outra metade depende do jogo, e a fronteira é nítida

| o que o caso do FPS exige | quem faz |
|---|---|
| existir uma placa de som por jogador | o **aparelho**, e só no cabo (§8) |
| saber qual placa é de qual controle | **o produto**, e já sabe (§7.2) |
| o som sair no controle certo quando alguém manda para aquela placa | **medido**, 16/08 00h08 (§7.1) |
| **o jogo mandar o som do jogador 2 para a placa do jogador 2** | **o jogo** |

A última linha é a que não é nossa, e vale dizer por quê: num co-op local, os
dois jogadores estão **no mesmo processo**, e um processo abre um fluxo de áudio.
Roteamento por processo — a aproximação (b) da §4 — **não separa dois jogadores
que compartilham o processo**. Não há corte fora do jogo que separe o tiro dele
do tiro dela.

**O que o produto pode entregar, e é o alvo honesto desta frente:** a mesa
pronta. Uma placa por jogador, endereçada, acordada, com volume sob posse e o
L+R somado — de modo que, no dia em que um jogo oferecer "saída de áudio por
jogador", ele encontre tudo no lugar. Hoje o produto entrega isso pela metade
(falta o L+R, falta a tela dizer quem é quem para o áudio).

### 7.4 O que a escada por rádio mudaria nisto — e o que não mudaria

**Muda:** hoje o caso do FPS **só existe no cabo**, porque só no cabo existe
placa de som por controle. Numa mesa de quatro, isso significa quatro cabos. A
escada de output por rádio (`0x32` a `0x39`), se um dia levar PCM, daria destino
de áudio aos controles do rádio — e o caso do FPS deixaria de depender de fio.

**Não muda:** a escada é um **destino a mais**, não um **fluxo a mais**. Ela não
faz o jogo separar jogador, nem separar SFX de trilha. A fronteira da §7.3
continua exatamente onde está.

**E o grau é o que a frente do rádio já escreveu, palavra por palavra:** *"o
canal existe, o firmware responde, e o conteúdo do payload ainda não foi
identificado"*. A hipótese de que o excedente é áudio é **forte** e continua
**hipótese** — e o E-1 mediu o campo `reserved`, não o excedente
([E-5 O TERRENO](2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md)
§1). Nada nesta sprint depende de a escada dar certo.

---

## 8. O rádio — nenhum dos três modos existe ali, e a tela tem de dizer isso

**Medido:** os controles no rádio **não publicam placa ALSA nenhuma** — nem de
captura nem de saída. O ensaio é `mic-radio-sem-placa-alsa-0727`
(`docs/data/ensaios.csv`), da mesa 2+2: os dois do cabo têm placa (`card2` e
`card3`), **os dois do rádio não têm nenhuma**. E o mapa registra, para o
alto-falante por rádio, `radio_aciona = não` e **zero linhas de implementação**
(`audio.alto_falante@dualsense`).

**Consequência direta, e ela é dura:** os três modos são todos decisões de
camada 1, e camada 1 é sink. **Sem placa não há sink, e sem sink não há modo
nenhum.** No rádio, hoje, os três modos não são "difíceis": são inexistentes.

O caminho é a frente da escada
([O ALTO-FALANTE POR RÁDIO 01](2026-08-15-O-ALTO-FALANTE-POR-RADIO-01-a-casa-ja-tinha-o-mapa.md)
e a [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)),
e ele é trabalho novo, não conserto.

### 8.1 A dívida de tela que isto cria, e ela já existe errada

Um modo indisponível tem de dizer **por quê**, e o texto que existe hoje diz a
coisa errada:

`app/audio_saida.py:1006`

    TEXTO_SONO_SEM_PLACA = "Sem placa de som do controle (no rádio não existe alto-falante)"

**O alto-falante existe no aparelho** — medido com a orelha dela em 02/08, com
controle negativo, e é a razão pela qual ela derrubou a mesma confusão em 22h41
de 15/08: *"no próprio projeto já fizemos isso, deveria tá mapeado inclusive no
specs"*. O que não existe no rádio é a **placa ALSA**, que é exatamente o que o
comentário três linhas acima diz certo. E **há um teste segurando a frase
errada** (`tests/unit/test_o_alto_falante_nunca_dorme_01.py`).

É o item **D.1** do censo, é palavra de tela, e por isso entra aqui como ONDA 3
e não como conserto silencioso.

---

## 9. O que falta, em ondas

| onda | o que é | grau | depende de | custo estimado |
|---|---|---|---|---|
| **1.1** | **O ensaio do FPS vai ao caderno** — dois controles no cabo, dois timbres, sem vazar, casamento por USB pai | medição perdida | o transcrito, ou 6 min de ouvido dela | 40 min |
| **1.2** | **O fato errado sai do mapa** — a `cabo_ressalva` de `audio.alto_falante.rota@dualsense` ainda promete o aquecedor como cura do sono, e ele foi **recusado por escrito**; a cura que entrou é outra (item **D.2** do censo) | substituição | nada | 20 min |
| **1.3** | **O `tuc` do modo 3 medido de novo**, agora com o drop-in 54 instalado: some ou não? Barato, e fecha uma frase que hoje diz "não foi medido" | ensaio | nada | 15 min |
| **2** | **O L+R explícito** (§6) — o desenho (A) ou o (B), conforme a **P-5** | cura de produto | **nada** | 2 h 10 |
| **3** | **Os três modos na tela** — os nomes, o que cada um faz, e a frase da recusa por transporte (§8.1). Nasce das decisões **P-1**, **P-2** e **P-3** | palavra de tela | dela | 1 h 40 |
| **4** | **Mover o fluxo do jogo** (a camada 1b, §4) — é o que faz "Sons do jogo" deixar de ser um byte sem fluxo. **Só depois da P-1**, porque muda o que o modo 2 promete | trabalho novo | P-1 | 1 h 55 |
| **5** | **O rádio** — os três modos deixam de ser inexistentes ali | trabalho novo | a escada (§7.4) | não estimado |

**A ONDA 2 é a única que se pode começar agora sem perguntar nada a ninguém**, e
é também a que vale para os três modos ao mesmo tempo.

---

## 10. O teste que MORDE

### Mordida 1 — o alto-falante recebe L+R, e não metade (ONDA 2)

**Arrancar:** a soma, seja ela regra de sistema ou nó do produto.

**Por que reprova:** o teste alimenta o caminho com um sinal em que **o conteúdo
está só no canal esquerdo** e exige que o que chega ao canal que alimenta o
alto-falante seja **não-nulo**. Sem a soma, o esquerdo se perde — que é
exatamente o `sfx-so-o-R-chega` medido na orelha dela — e o teste cai.

É a principal, porque é a única que impede o produto de voltar a depender do
upmix do PipeWire sem ninguém perceber.

### Mordida 2 — a soma não pode dobrar o volume

**Arrancar:** somar sem normalizar.

**Por que reprova:** com o **mesmo** conteúdo nos dois canais (que é o caso
comum: som mono duplicado), a soma crua satura. O teste exige que o nível de
saída de um estéreo idêntico seja o mesmo de um mono, dentro de tolerância
declarada no próprio teste.

### Mordida 3 — o modo indisponível diz o transporte, não uma falsidade (ONDA 3)

**Arrancar:** deixar `TEXTO_SONO_SEM_PLACA` como está (`audio_saida.py:1006`) e
o teste que hoje o trava.

**Por que reprova:** o teste exige que a frase da recusa **não** afirme que o
controle não tem alto-falante, e **sim** que aquele transporte não publica placa
de som. É aviso com lista, e a lista nasce das frases que ela escrever na P-1.

**Atenção de portão:** esta mordida **conserta um teste existente**, não só
adiciona um. Hoje há um teste segurando a frase errada — arrancar a cura significa
restaurar a frase antiga, e o teste novo tem de cair com ela.

### Mordida 4 — o modo 2 não promete fluxo que ninguém move (ONDA 4)

**Arrancar:** deixar "Sons do jogo" chamando `pedir_rota_do_sistema(False)` sem
mover o fluxo do jogo (`controller_card.py:3756` em diante).

**Por que reprova:** o dublê põe o sink padrão na TV e um fluxo de jogo tocando
nele. O teste escolhe "Sons do jogo" e exige que **alguma coisa passe a alimentar
a placa do controle**. Hoje nada passa, e o byte da rota é escrito para um som
que não chega.

### O que estes testes NÃO provam

**Que o som sai.** Nenhuma mordida aqui aciona alto-falante nenhum, e nenhuma
substitui a orelha dela. Que os modos soam como ela espera é bancada, e é a §11.

---

## 11. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **P-1** — os nomes e o número de portas na tela (§12) | escrever o que ela disser, com a mordida 3 |
| **P-2** — o que o produto faz quando o fone está plugado | implementar |
| **P-3** — o modo é do controle ou da mesa | implementar |
| **P-4** — o modo entra no perfil | implementar |
| **P-5** — o L+R por regra de sistema ou por caminho próprio | ONDA 2, com as mordidas 1 e 2 |
| **A palavra final da tela**, por PROVA-DE-TELA-01 | foto antes e depois |
| — | ONDA 1 inteira, ONDA 2, as quatro mordidas |

---

## 12. As perguntas que sobram, com o preço dos dois lados

### P-1 — três portas para dois quartos: a tela oferece três modos, dois, ou duas chaves?

Hoje, sem jogo que separe, **o modo 1 e o modo 3 são o mesmo gesto** (§2.2).

| opção | preço |
|---|---|
| **(a) três nomes desde já** | duas portas dão no mesmo quarto até o dia em que um jogo separar. A casa tem regra contra oferecer na tela distinção que o produto não faz |
| **(b) dois nomes agora**, o terceiro nasce quando houver o que separar | o requisito dela fica escrito e invisível — e ela vai procurar o terceiro. Foi o que já aconteceu uma vez com este mesmo pedido |
| **(c) duas chaves em vez de três botões** — *"o som geral: TV / controle"* e *"os sons do jogo: TV / controle"* | os três modos viram três das quatro combinações, e a quarta ("nada no controle") é o padrão de hoje, que a tela passa a nomear. **Deriva do léxico que já existe** ("Todo o som do PC", "Sons do jogo"), o que é o critério desta casa para nome novo. Preço: duas chaves ocupam mais que um seletor na linha mais apertada do card — e essa linha **já foi medida** uma vez (155px para o seletor, 241px com o `Silenciar`, teto de 258), então a medida vale para o desenho de hoje e **não** para este |

**Recomendação:** (c), com a medida de largura refeita antes de qualquer pixel.

### P-2 — o fone plugado manda por cima da rota. O produto avisa, obedece, ou corrige?

Medido três vezes: mesma rota, mesmo canal, o som troca de destino conforme o
fone (`sfx-o-fone-manda-por-cima`).

| opção | preço |
|---|---|
| **obedecer calado** | ela escolhe "no controle", pluga o fone, e o alto-falante cala sem explicação. É o comportamento de hoje |
| **avisar** | uma frase a mais na tela num bloco que já é denso |
| **corrigir a rota sozinho** quando o fone aparece | o produto passa a desfazer a escolha dela. Contra a regra de 09/08 — *a vontade da GUI prevalece* |

### P-3 — o modo é POR CONTROLE ou DA MESA?

Há **um** sink padrão na máquina. Com quatro controles, escolher "todo o som no
controle" no card do jogador 2 **tira o som da TV de todo mundo**.

| opção | preço |
|---|---|
| **por controle, último clique vence** | é o que o produto faz hoje. Barato, e mente: o card sugere que a escolha é daquele jogador |
| **a camada 1 sobe para o bloco da mesa** e o card governa só a camada 2 | honesto, e é a leitura que o próprio código já tem (`controller_card.py` diz que o card *pede* e a aba *executa*). Custa mexer no card, na aba e no que o perfil guarda |

### P-4 — o modo sobrevive a fechar a janela?

A rota já entra no perfil (`profiles/schema.py:466`). O sink padrão **não**, e o
limite está declarado em `:456`.

| opção | preço |
|---|---|
| **guardar o modo inteiro no perfil** | ativar um perfil passa a mexer num fato global da máquina dela. O próprio código já diz que restaurá-lo *"é decisão dela, não efeito colateral de trocar de janela"* |
| **não guardar** | ela reescolhe o modo a cada sessão — e "ao final do projeto eu espero três modos" soa como coisa que se configura uma vez |

### P-5 — o L+R por regra de sistema ou por caminho do produto?

Os dois desenhos e os dois preços estão na §6. A recomendação é a regra de
sistema, pela coerência com a decisão já escrita no drop-in 54.

**A pergunta que fica é só uma, e é dela:** aceitar mais um arquivo do produto no
áudio da máquina — hoje são quatro — em troca de o alto-falante nunca mais
perder metade do som.

---

## 13. O que esta sprint NÃO resolve, e por quê

1. **Não mediu nada.** Foi escrita com o hardware na mesa dela, em uso, às duas
   da manhã. Toda medição citada é do caderno, com o nome do ensaio.
2. **Não sabe o que o PS5 faz.** A §3.2 raciocina sobre o Sackboy a partir do que
   o DualSense oferece no Linux, e diz isso na cara. Ninguém aqui mediu um PS5.
3. **Não estimou o rádio.** A ONDA 5 depende de uma hipótese que continua
   hipótese, e pôr número nela seria fingir plano.
4. **Não tocou no fluxo do co-op.** A §7.3 afirma que dois jogadores no mesmo
   processo compartilham o fluxo de áudio; isso é **raciocínio sobre como jogos
   abrem áudio**, não medição desta casa. Se um jogo provar o contrário, é a
   §7.3 que cai.
5. **Não conferiu a tela.** Nenhuma foto foi tirada. Por PROVA-DE-TELA-01,
   nenhuma linha da ONDA 3 fecha sem o olho dela.
