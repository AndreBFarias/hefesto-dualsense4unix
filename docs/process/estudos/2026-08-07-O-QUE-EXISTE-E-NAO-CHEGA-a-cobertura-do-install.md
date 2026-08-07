# O que existe e não chega — a cobertura do install

Auditoria de **07/08/2026**, branch `restauro/inicio-da-sessao`. Leitura pura:
nada foi escrito em `/etc`, nenhum serviço reiniciado, o `install.sh` não foi
rodado. A máquina dela estava **viva e em uso** durante toda a medição, com três
controles conectados e um DualSense carregando.

Este documento é inventário, não cura.

---

## A pergunta dela

Citação **literal**, sem correção de acentuação. Citação não se corrige.

> *"voce tinha me falado que ja existem solucoes pra muitos dos problemas que eu <!-- noqa-acento -->
> relato mas eles nao foram integrados a maquina pq nao foram inseridos no <!-- noqa-acento -->
> install por exemplo"* <!-- noqa-acento -->

**A resposta em uma frase:** de 40 curas auditadas, **13 não chegam inteiras à
máquina dela** — e apenas 4 delas são o caso que ela imaginou (o install nem
tenta); as outras 9 são piores, porque **parecem instaladas**.

GRAU: MEDIDO para as treze, cada uma com o comando e a saída colados adiante.
A proporção 27/40 é subtração dentro do conjunto auditado. O inventário total é
de 134 curas, então **94 nunca foram olhadas** — nada aqui diz que elas estão
bem. GRAU: SEM PROVA sobre as 94.

A intuição dela está certa, e é mais grave do que ela formulou. Ela supôs
esquecimento no `install.sh`. O que se mediu foi outra coisa: **o install quase
sempre faz a parte dele**. Copia o arquivo, recarrega o udev, habilita a unit.
O que falha é o **segundo pedaço** de cada cura — o gatilho que combina com a
regra, o script que o `RUN+=` chama, o leitor da marca, a linha que esvazia o
buffer. E como todo portão desta casa pergunta *"o arquivo está lá?"* em vez de
*"a cura está agindo?"*, o conjunto fica verde com a cura morta dentro.

---

## As quatro categorias, e por que o remédio de cada uma é diferente

| Categoria | Quantas | O que significa | Remédio |
|---|---|---|---|
| **CHEGA MAS NÃO VALE** | **6** | O arquivo é copiado, o passo de ativação existe — e a cura não age | Consertar o **par**: o artefato e o que o aciona têm de concordar |
| **NÃO CHEGA** | **4** | O install nem tenta, porque não há o que instalar | Escrever o artefato (2 são desenho puro; 1 é recusa deliberada) |
| **JÁ ESTÁ NA MÁQUINA POR FORA** | **3** | Funciona **nesta** máquina por algo que não está no repositório | Trazer a cura para dentro, ou declarar por escrito que é bancada dela |
| Chegam inteiras | 27 | O install entrega e a cura age | Nada |

A categoria de destaque é a primeira, e ela merece o destaque por um motivo
único: **é a que engana**. Uma cura que não chega deixa rastro — o sintoma
continua e alguém investiga. Uma cura que chega e não vale produz `[OK]` no
doctor, verde no CI e a doença de pé. Foi assim que seis defeitos sobreviveram
a semanas de portões verdes.

A terceira categoria tem um agravante que não é técnico. **O Hefesto é open
source.** Uma cura que só funciona nesta máquina, por causa de um programa
vizinho ou de um arquivo no self-heal pessoal dela, **falha em toda máquina que
não é a dela** — e ninguém do outro lado terá como saber por quê.

---

## Ordenado por gravidade: o que ela sente primeiro

Gravidade aqui significa **o que ela sente**, não o que é difícil de consertar.

### ALTA — quatro curas, e ela sente três delas hoje

#### 1. O caderno que devia explicar a queda está vazio

*"o controle desconectou e reconectou sozinho e eu não sei por quê"* — existe
uma vigia instalada justamente para guardar a explicação num arquivo dela. Ela
está **ligada, ativa e escrevendo em lugar nenhum**.

O install faz tudo certo: copia o script, copia a unit, faz `daemon-reload` e
`enable --now`. GRAU: MEDIDO (`install.sh:2262-2284`). Na máquina dela a unit
está `enabled` e `active`.

Falta **uma linha** em `scripts/storm_watch.sh`: o `awk` do `classify()`
(linhas 50-72, conferidas hoje) não tem `fflush()`. A saída fica presa num
buffer de 256 KiB que o `SIGTERM` descarta. Os 348 eventos de 05 a 07/08 estão
no buffer, não no arquivo dela. GRAU: SUSPEITA COM MECANISMO — o mecanismo do
buffer foi medido e o `fflush` está ausente; o experimento com a unit
reiniciada não foi feito, porque exigiria reiniciar serviço.

O teste atual passa com a cura arrancada, porque em teste o processo termina e
o EOF descarrega o buffer sozinho. GRAU: MEDIDO.

#### 2. O Bluetooth que demora quase um minuto para voltar

*"o Bluetooth demorou quase um minuto pra voltar"* — no travamento de 06/08 às
21:03, o gancho que fotografa os pareamentos consumiu **42,8 dos 57,25 segundos**
de rádio fora do ar, esperando um cadeado. O mesmo script rodado à mão custa
0,03 s — 1.400 vezes menos. GRAU: MEDIDO (registro em
`docs/process/sprints/2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md:178-183`).

A cura foi **desenhada e nunca virou linha de código**. Conferido hoje nos dois
lados: `scripts/bt_bonds_snapshot.sh:106` tem `flock -w 30`, e a versão
instalada em `/usr/local/lib/hefesto-dualsense4unix/bt_bonds_snapshot.sh:106`
tem a mesma linha. GRAU: MEDIDO.

**A armadilha, e é o ponto mais importante desta auditoria:** o parsing de
argumentos do script é posicional e de **uma vaga só** (`:38-39`). Quem
acrescentar `--quiet --sem-espera` ao `ExecStopPost` vai ver a segunda bandeira
ser ignorada em silêncio — a cura ficaria instalada e **inerte**, que é
exatamente o "parece instalado" que esta casa teme. O parsing tem de virar laço
**no mesmo commit**, ou a cura nasce morta. GRAU: MEDIDO.

#### 3. O Bluetooth preso desligando, sem teto nenhum

*"o Bluetooth ficou preso desligando"* — nenhum gancho nosso tem limite de
tempo. Medido hoje na máquina dela:

```
$ systemctl show bluetooth.service -p TimeoutStopUSec
TimeoutStopUSec=1min 30s
$ grep -c TimeoutStopSec assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf
0
```

O drop-in chega e o `daemon-reload` roda (`install.sh:1513-1521`) — o cano está
sadio. O conteúdo é que não tem a cura. GRAU: MEDIDO.

**Não entregar sozinho.** Sem o `flock -n` do item 2, o teto só troca "rádio
morto por 43 s" por "retrato degolado no meio da escrita". Os dois juntos, e o
teto vira rede de segurança em vez de guilhotina.

#### 4. A janela não sabe dizer qual Pro Controller é qual

A regra `84-nintendo-pro-variant.rules` pinta a marca em quatro camadas do
aparelho. Ela chega inteira: arquivo em `/etc` (conferido hoje, `ago 6 21:01`),
idêntico ao repositório, `udevadm verify` com `Success: 1 Fail: 0`.

E **nenhuma linha de Python do projeto lê essa marca**:

```
$ grep -rn "HEFESTO_CONTROLLER_VARIANT" src/ | wc -l
0
```

GRAU: MEDIDO. A cura de sistema está perfeita e o produto não a usa. Pior: o
`install.sh:1141` **imprime a promessa** de que a regra "separa o Pro genuíno do
8BitDo clone" — e é essa frase que faz a cura parecer entregue.

Junto disso, duas coisas que quem for integrar precisa saber ou vai curar pela
metade: o desempate em `friendly_type()` consulta `_TYPE_BY_VIDPID` antes do
OUI, então hoje os dois Pro devolvem a mesma string; e a regra 84 **só marca por
cabo** — por Bluetooth o aparelho nasce sem pai `usb_device` e nenhuma das oito
linhas casa. Cabo e rádio são sinais complementares, não substitutos. GRAU:
MEDIDO.

---

### MÉDIA — cinco curas, mordida diferida ou invisível

#### 5. O Pro Controller que cai na janela dos dois minutos

*"o Pro Controller cai quando tá todo mundo jogando"* — a regra 82 deveria tirar
o rádio do modo de economia **no instante** em que a conexão nasce, em vez de
esperar até dois minutos pela vigia. A janela entre um e outro era exatamente
onde ele caía.

As duas metades chegam. A regra dispara. E o resultado, medido no journal desta
máquina:

```
$ journalctl -t hefesto-bt --since "-14 days" | grep -c "no-sniff aplicado na borda"
0
$ journalctl -t hefesto-bt --since "-14 days" | grep -c "no-sniff na borda falhou"
15
```

**Zero acertos, quinze falhas.** GRAU: MEDIDO. Quem segura o Pro hoje é a vigia
de 2 minutos, não a cura de borda — que nunca valeu nesta máquina. O doctor dá
`[OK]` porque olha se o arquivo existe (`doctor.sh:161`).

Este caso **não é o vão que ela descreveu**: o install está correto e mexer nele
seria perder tempo. É falha de execução, não de integração.

#### 6. A rede de segurança dos sensores dos controles virtuais, morta desde um rename

A regra 78 protege os sensores de movimento contra uma regressão do kernel que
os faria voltar a poluir a lista de gamepads. A linha dos controles **virtuais**
procura um nome que não existe mais:

```
assets/78-...rules:20   ATTRS{name}=="Hefesto Virtual DualSense P* Motion Sensors"
uhid_gamepad.py:876     return f"DualSense Wireless Controller (Hefesto P{self.player})"
```

GRAU: MEDIDO. O produto renomeou o aparelho e a regra ficou com o nome antigo.

O efeito visível **hoje é nulo** — o kernel já classifica certo por conta
própria. O que se perdeu é a rede, e ela valia justamente no cenário de quatro
jogadores, onde cada controle virtual dobra o número de nós de sensor.

Ninguém percebeu por um motivo que vale mais que o defeito: **o teste da casa
verifica que a frase está no arquivo, não que ela casa com alguma coisa**
(`tests/unit/test_udev_kernel07_path06.py:88`). A regra irmã 80 sobreviveu ao
mesmo rename porque casa por `*Motion Sensors*`, e é o precedente a seguir.

#### 7. O touchpad-como-mouse e o giroscópio só funcionam por causa de outro programa

Esta é a cura que impediria o projeto de depender do grupo `input`. A decisão
está escrita em `docs/history/RESPOSTAS_V1.md:24` — *não* pôr a usuária no grupo
`input`, por ser primitiva de keylogger; criar em vez disso uma regra seletiva.
**A regra nunca foi escrita.** Não existe arquivo em `assets/` que dê acesso a
nós de entrada. GRAU: MEDIDO.

Hoje funciona porque ela está no grupo `input` **por causa do Ritual da Aurora**,
cujo comentário diz que existe para outro programa e pode sair a qualquer
versão. GRAU: MEDIDO (`id` confirma o grupo).

Numa máquina limpa, seguindo a própria doutrina desta casa, o touchpad e o
giroscópio **falham em silêncio** e o doctor diz que está tudo bem. Três
gatilhos reais: máquina nova, reinstalação do sistema, ou o dia em que a Aurora
largar o `usermod`.

O arquivo novo tem de ser numerado **abaixo de 73** — é o `73-seat-late.rules` do
systemd quem converte a etiqueta em permissão, e a casa já pagou por esse erro
antes (notas ONDA-R em `assets/77-dualsense-leds.rules:23-28`).

#### 8. A cura que está na máquina dela e não está no repositório

Era isto que fazia o doctor acusá-la de um `chmod` que ela nunca deu, quatro
vezes seguidas — e deixava teclado e mouse dela legíveis por qualquer processo
local. **Já está curado na máquina dela** desde 06/08 às 21:21.

O arquivo curado **não vive neste repositório**: vive em
`~/.config/zsh/scripts/60-openrgb.rules`, o self-heal pessoal dela. GRAU:
MEDIDO — `/etc/udev/rules.d/60-openrgb.rules` está lá com data de 06/08, e
`grep -rn -i openrgb install.sh scripts/*.sh` devolve **uma** ocorrência, que é
comentário no doctor.

O buraco que sobra: **a máquina está curada e o repositório não sabe disso.** Se
ela reinstalar o sistema, ou levar o Hefesto para outro computador com OpenRGB,
o teclado volta a ficar legível. O doctor é, hoje, a única coisa que viaja.
GRAU: SUSPEITA COM MECANISMO.

Destravou hoje um passo que estava bloqueado: o motivo declarado para não
estreitar a regra por VID/PID era que o OpenRGB não estava no ar para enumerar
os aparelhos. Ele está ativo agora. GRAU: MEDIDO que ficou possível; SEM PROVA
da lista de aparelhos, porque `--list-devices` abre i2c e hidraw com três
controles conectados e eu sou leitor.

#### 9. O portão verde que não vê o que falta

O `check_packaging_parity.sh:267-315` cobra, para cada regra de `assets/`,
presença nos dois instaladores, no `.deb`, no PKGBUILD, no spec do Fedora, no
Flatpak e no uninstall. Ele roda no CI (`ci.yml:169`, job `packaging-parity`) e
está **verde hoje**.

Primeiro, uma nota datada: a acusação registrada em
`PROMESSA-NAO-CUMPRIDA-01:117-120` de que este portão "não roda em workflow
nenhum do CI" **caducou em 27/07**. GRAU: MEDIDO.

O achado é o verde. O portão imprime `[OK] 82-nintendo-pro-nosniff.rules:
coberta em todos os instaladores` — e o `bt_nosniff_now.sh`, que é o **alvo do
`RUN+=` sem o qual a regra não faz nada**, não aparece em `build_deb.sh`, no
PKGBUILD, no `.spec`, no `package.nix` nem no Flatpak. O portão cobra o arquivo
de regra e **não cobra o resto da camada**: nem o alvo do `RUN+=`, nem o
`groupadd hefesto`, nem os gatilhos seletivos. GRAU: MEDIDO.

O extrator necessário **já existe e está testado**
(`_alvos_run_das_regras`, em `tests/unit/test_uninstall_simetrico_ao_install.py`)
— é reaproveitá-lo no sentido do install.

---

### BAIXA — quatro curas, nenhuma dela dói hoje

#### 10. O controle no cabo que "cai sozinho": a regra certa, o gatilho errado

A regra 72 manda o DualSense nunca dormir. O install copia e recarrega. Mas a
regra escuta `ACTION=="add"` e o install dispara `--action=change`:

```
assets/72-...rules:14-15    ACTION=="add", SUBSYSTEM=="usb", ...
scripts/install_udev.sh:169 sudo udevadm trigger --action=change --subsystem-match=usb
```

GRAU: MEDIDO. O passo de ativação imediata é um **no-op silencioso** — e o
`ADR-013:33` documenta esse mesmo comando errado como se fosse a cura.

O conserto certo é alinhar a 72 à forma já provada da irmã 81: `ACTION=="add|change"`.
Isso faz o gatilho que o install **já dispara** passar a valer, sem comando novo
e sem raio de ação novo.

O conserto **errado**, e vale registrar para ninguém tentar: acrescentar
`udevadm trigger --action=add --subsystem-match=usb` ao install. Isso reexecuta
as regras `add` de **todas** as regras USB da máquina dela, incluindo as de
terceiros com `RUN+=`. É um estrago que ela não pediu.

Gravidade baixa por um motivo específico: esta cura é hoje um **duplicata mais
fraco da 81**, que cobre o mesmo aparelho com `add|change` e mais quatro
fabricantes. Pela regra da casa, a saída não é apagar a 72 — é uma **nota
datada** no ADR-013 dizendo que a 81 a subsumiu, e corrigindo a linha 33.

#### 11. A página que manda ela colar uma receita que não funcionaria

`docs/usage/troubleshooting.md:605-620` manda ela colar um `sudo tee` para criar
a regra 95 à mão. O arquivo não existe em `assets/` — a única ocorrência na
árvore inteira é a própria prosa. GRAU: MEDIDO.

**Mas o conserto certo não é pôr a 95 no install.** A receita, do jeito que está
escrita, **não funcionaria na máquina dela**: casa por `ENV{ID_VENDOR_ID}` e
`ENV{ID_MODEL_ID}`, que são chaves de USB e estão ausentes em todos os controles
dela (Bluetooth via uhid e virtuais). Se ela seguir a página numa noite ruim,
gasta sudo, cria arquivo em `/etc`, nada muda, e conclui que "nem isso resolveu"
— o pior desfecho possível, porque queima a confiança na página.

O vão de verdade é o inverso do que ela perguntou: **a cura chegou** — a regra
76 está instalada e medida funcionando agora, com `LIBINPUT_IGNORE_DEVICE=1` nos
dois touchpads vivos — **e a documentação não sabe disso**, e continua oferecendo
uma contingência obsoleta. O tempo que ela perderia não seria por falta de cura;
seria por a página mandar aplicar a cura errada.

#### 12 e 13. As duas recusas deliberadas — o contra-exemplo que salva o método

Duas curas não chegam **de propósito**, e é importante não confundi-las com as
outras onze:

**A regra 75** (desligar a placa de som do controle) tem um preço que ela precisa
saber: o controle **perde o microfone e o fone**. Ela está excluída do laço do
install por linha explícita (`install.sh:1120`), e a retenção está escrita em
**quatro lugares que concordam entre si**. Nada falta aqui. E o problema que ela
sentia já está curado por outro caminho, que preserva o microfone: zero
tempestades desde 20/07. GRAU: MEDIDO.

**A opção `--restaurar-hidraw-uaccess`** não existe (`grep` devolve zero fora da
prosa que a desenha). Falta **por decisão escrita**: um projeto de gamepad não
legisla a política de segurança da máquina inteira. E o sintoma que a motivou já
teve as duas metades fechadas — o aviso mentiroso foi curado e commitado
(`53f6d8b`), e o vazamento foi fechado em 06/08.

Estas duas são o **contra-exemplo**, e é por isso que valem uma seção: elas
provam que esta casa **sabe** reter uma cura direito, com a razão escrita em
lugar que outra pessoa encontra. As onze restantes não têm isso.

---

## O que é seguro integrar agora

Nove curas não precisam da palavra dela. Nenhuma delas muda comportamento que
ela escolheu; todas consertam algo que já foi decidido e não está agindo.

**Prontas, e cada uma cabe numa leva pequena:**

1. **`fflush()` no `awk` do `storm_watch.sh`.** Uma linha. Consequência que a
   leva precisa cobrir: depois da correção, a unit precisa de restart, e nesse
   restart o buffer atual (348 eventos) **é perdido** — extraí-los do journal
   antes é melhor que esperar.
2. **`flock -n` no gancho de parada** — com o **parsing em laço no mesmo
   commit**, ou a cura nasce inerte. Alternativa a registrar para ela decidir:
   `flock -w 1` custa 1 s em vez de 42,8 e preserva a tentativa de retrato.
3. **`TimeoutStopSec=` no drop-in do BlueZ**, junto do item 2. O valor sai de
   número, não de chute: a parada limpa custou 29 ms e o retrato à mão 0,03 s —
   poucos segundos é folgado por três ordens de grandeza. Não invente 90 s "por
   segurança", que é justamente o padrão do qual se quer sair.
4. **`ACTION=="add|change"` na regra 72**, mais a nota datada no ADR-013.
5. **O nome de hoje na regra 78**, derivado de `UhidDualSense.name` e não
   copiado à mão, mais o mesmo padrão em `scripts/doctor.sh:2700`.
6. **A regra nova de acesso aos nós de entrada**, numerada abaixo de 73, casando
   por `ATTRS{name}` e não por `ENV` — as regras 76 e 78 já provaram esse idioma
   nesta máquina.
7. **As duas asserções que faltam no portão de paridade**: alvo de `RUN+=` e
   `groupadd hefesto`.
8. **O leitor da marca `HEFESTO_CONTROLLER_VARIANT` no produto**, com o desempate
   de `friendly_type()` corrigido junto — senão a marca continua sem efeito.
9. **O parágrafo que falta na página de solução de problemas**: conferir a regra
   76 **antes** de qualquer contingência.

**E, em todas as nove, o teste que morde.** Não é acessório: é a única coisa que
impede o retorno. Hoje `grep -rn "72-ps5-controller-autosuspend" tests/` devolve
vazio, nenhum teste cita `flock`, e o teste da 78 verifica uma frase.

## O que precisa da palavra dela

Quatro coisas. Nenhuma é código; todas são escolha.

1. **A regra 75 (perder microfone e fone do controle).** Não proponho integrá-la
   em forma nenhuma — nem atrás de flag, nem com detecção automática. Fica
   registrada porque, se um dia a tempestade voltar, esta é a escalada, e o
   preço é dela.
2. **A opção `--restaurar-hidraw-uaccess`.** Desenho guardado, não dívida.
3. **Estreitar a regra do OpenRGB por aparelho.** Destravou hoje, mas exige o
   OpenRGB no ar e a presença dela: estreitar às cegas apaga o RGB de um
   periférico que ninguém listou. É trabalho no self-heal **dela**, não no
   install do Hefesto.
4. **A pergunta de fundo, que decide a prioridade de tudo na terceira
   categoria:** o Hefesto é a ferramenta dela, ou é um produto para outras
   pessoas? Se for ferramenta dela, "já está na máquina por fora" é acervo. Se
   for produto, é dívida com data.

---

## A lição de método

Se houver uma coisa a guardar deste documento, não é a lista — é isto. A lista
tem treze itens e envelhece. O padrão explica por que existiriam **outros
treze** na próxima auditoria.

### O padrão: o portão mede o artefato, e a cura é sempre um par

Toda cura desta camada é um **par**, e as duas metades moram em arquivos
diferentes, escritas em sprints diferentes:

| A cura | Metade A | Metade B |
|---|---|---|
| Regra de udev | o casador (`ACTION`, `ATTRS{name}`) | o gatilho que o install dispara |
| Regra com `RUN+=` | o arquivo em `/etc` | o script alvo em `/usr/local/lib` |
| Unit de systemd | a unit | o script que o `ExecStart` chama |
| Marca de udev | quem escreve | quem lê |

**Nenhum portão desta casa afirma que as duas metades concordam.** Todos medem a
metade A: o arquivo existe, o nome aparece nos sete instaladores, a frase está
no `.rules`. É por isso que as seis curas de "chega mas não vale" passaram —
todas têm a metade A impecável.

E o portão de paridade **institucionaliza** metade disso: ele varre sete
caminhos de empacotamento cobrando o arquivo de regra, e não cobra o alvo do
`RUN+=` da mesma regra. Ele imprime `[OK]` para a 82 exatamente enquanto a 82
falha 15 vezes em 15 na máquina dela.

### O corolário mais caro: a documentação certifica o defeito

Em três casos, o documento que descreve a cura **registra a versão quebrada como
se fosse a certa** — e por isso quem vai conferir lendo a documentação *confirma*
o defeito:

- o `ADR-013:33` documenta o `udevadm trigger` que não aciona a regra 72;
- o `install.sh:1141` **imprime** que a regra 84 separa os dois Pro, e o produto
  não lê a marca;
- a página de solução de problemas ensina uma receita que não casaria com
  nenhum controle dela.

Uma cura sem documentação alguém eventualmente descobre. Uma cura cuja
documentação afirma que ela funciona é invisível até que alguém meça o **efeito**
— o que, nestes casos, levou de três dias a sete meses.

### O segundo padrão: a sprint termina no diagnóstico

Cinco das treze são **prosa que nunca virou artefato**: E4, E5, a decisão 3.3, a
regra 95 e a opção de hidraw. O documento da sprint foi o entregável, e o passo
"isto exige uma ação no sistema" ficou sem dono e sem portão.

O agravante é que **o repositório não distingue um "não" deliberado de um "não"
esquecido**. E4 e E5 (esquecidas) parecem, para quem varre a árvore, exatamente
iguais à 75 e à opção de hidraw (recusadas de propósito). A diferença existe só
na cabeça de quem escreveu. Foi isso que custou 40 curas de leitura para
redescobrir hoje.

A 75 mostra que dá para fazer certo: a retenção dela está escrita em quatro
lugares que concordam entre si, incluindo um comentário no arquivo que já está
na máquina. Quem tropeça nela **entende em trinta segundos** que é deliberada.

### O terceiro padrão: a máquina dela é o teste de integração, e está contaminada

Três curas funcionam aqui por razões que não estão no repositório: o grupo
`input` que vem do Ritual da Aurora, o `60-openrgb.rules` do self-heal pessoal
dela. A máquina que valida o projeto é **a única máquina onde o vão é
invisível**. Num projeto open source isso é um defeito de método, não uma
conveniência: cada uma dessas curas falharia em toda máquina que não é esta, em
silêncio.

### As três regras que impedem os próximos treze

1. **Todo portão que hoje pergunta "o arquivo está lá?" ganha um irmão que
   pergunta "a cura agiu?"** — e o aferidor honesto costuma estar de graça: o
   journal (contar aplicados contra falhados), o `sysfs` (ler
   `power/autosuspend_delay_ms`), o `getfacl`. Nos três casos onde isso foi
   medido hoje, a resposta apareceu em um comando.
2. **Toda cura de par ganha uma asserção de que as metades concordam**, e essa
   asserção tem de **morder**: arrancar uma metade precisa deixar vermelho.
3. **Toda sprint que termina sem artefato deixa uma marca que diz qual dos dois
   "nãos" ela é** — desenhada e não construída, ou desenhada e recusada. Sem
   isso, a próxima auditoria paga de novo o preço desta.

---

## O que este documento não mediu

Registrado de propósito, para ninguém ler mais garantia do que há:

- **94 das 134 curas inventariadas não foram auditadas.** GRAU: SEM PROVA.
- **O `fflush` não foi provado na máquina dela** — exigiria reiniciar a unit.
  GRAU: SUSPEITA COM MECANISMO.
- **A causa da falha 15/15 do no-sniff de borda não foi isolada.** O experimento
  que decide exige root: rodar o script à mão com o Pro conectado. Se acertar à
  mão, a causa é a janela e o conserto é o gatilho; se falhar, a abordagem do
  `RUN+=` está errada e o gatilho tem de virar unit. GRAU: SEM PROVA.
- **Não se verificou se o padrão `journalctl -f | awk >> arquivo` aparece em
  outra vigia da casa.** GRAU: SEM PROVA.
- **O `i2c` que continua `0666` no arquivo do OpenRGB não tem detector nenhum**
  (`grep -c i2c scripts/doctor.sh` = 0). GRAU: SUSPEITA COM MECANISMO.
