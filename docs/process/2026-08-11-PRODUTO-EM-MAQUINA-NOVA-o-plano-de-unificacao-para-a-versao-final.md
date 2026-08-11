# PRODUTO EM MÁQUINA NOVA — o plano de unificação para a versão final

- **Escrito em:** 11/08/2026, na branch `restauro/inicio-da-sessao`
- **Rótulo:** `ROTEIRO` — não é sprint de execução. É a ordem em que as sprints
  entram, e o critério que decide quando parar
- **Grau:** as medições da seção 2 são **MEDIDO**, por leitura de
  `caminho:linha` na árvore de trabalho de 11/08 — que é o que roda. As
  estimativas de custo são **ESTIMATIVA**, em horas de bancada. O que depende de
  medição que não existe está nomeado na seção 8, com o nome da medição que falta
- **O pedido dela, literal:** *"a forma inteligente de unificarmos tudo com o
  projeto de forma que consigamos uma versão final de produto, a ponto de eu
  testar em outro PC que nem esse e tudo funcionar lá."*
- **A régua que este plano não pode contrariar:** a resposta 17 de
  [DECISÕES DELA](2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md) —
  *"produto — tem que funcionar em máquina limpa"* — e a regra de 09/08:
  *tudo tem que focar em funcionar na interface do app e no install*

---

## 0. As três perguntas que são dela, e que mudam o plano inteiro

Nenhuma se responde com código. Cada uma muda o que está escrito abaixo.

| # | pergunta | o que ela decide |
|---|---|---|
| 1 | **Qual distro e qual sessão tem o PC novo?** | Se for Pop!_OS + COSMIC, este plano vale como está. Se for outra família, o `install.sh` nativo **morre** no passo do GTK: ele só sabe `apt-get` (`install.sh:354`, `run_apt`). Fedora, Arch e Nix têm pacote, mas nenhum foi validado em hardware |
| 2 | **Qual versão de BlueZ vem nele?** | O `doctor` aceita `[5.79, 5.87)` (`scripts/doctor.sh:2451-2452`). Abaixo de 5.79 ele **REPROVA**, e a cura exige `.deb` de backport já presentes em cache — que numa máquina limpa **não existem**. A receita passou a viver na árvore em 11/08 ([estudo](estudos/2026-07-19-estudo-bluez-backport-onda-r.md)), mas gerar os pacotes continua sendo trabalho |
| 3 | **O Secure Boot está ligado nele?** | Com SB ativo e a chave MOK não enrolada, o kernel **RECUSA** o `.ko` de `updates/dkms` e **não cai no in-tree** (`scripts/doctor.sh:3923`). O resultado é uma máquina **sem `hid-nintendo`**, que é pior do que sem a cura |

Os três comandos que respondem, e que ela pode rodar no PC novo **antes** de
qualquer instalação:

```bash
cat /etc/os-release | head -3 ; echo "$XDG_CURRENT_DESKTOP / $XDG_SESSION_TYPE"
bluetoothctl --version
mokutil --sb-state 2>/dev/null || echo "sem mokutil (provavelmente sem Secure Boot)"
```

---

## 1. O que "versão final de produto" significa aqui — em critérios que se CHECA

A regra é a da casa: **ela decide vendo, não lendo.** Cada critério diz **onde
ela olha** e **o que reprova**. Nenhum é adjetivo.

### Bloco A — A máquina (o que se lê no terminal, uma vez só)

| # | critério | onde ela olha | o que REPROVA |
|---|---|---|---|
| **A-1** | O `./install.sh` chega ao fim sem ela digitar nada além de Enter e da senha uma vez | a última tela do instalador | qualquer passo que peça um comando manual depois. *Cura à mão não existe para quem instala* |
| **A-2** | A conferência final imprime `nenhuma FALHA` | as últimas linhas do instalador (`install.sh:2891`) | uma linha `[FAIL]` |
| **A-3** | O `bash scripts/doctor.sh` sai **0** e o resumo diz quantos itens **não puderam ser medidos** por falta de hardware | a linha de diagnóstico | sair diferente de 0 — **ou** sair 0 escondendo cura ausente (o defeito medido na seção 2.1) |
| **A-4** | O `doctor` nomeia os **três** módulos DKMS da casa e o veredito de cada um | o bloco de kernel do `doctor` | qualquer um aparecer como `info` quando o `install.sh` prometeu instalá-lo |

### Bloco B — A janela (o que ela vê sem terminal nenhum)

| # | critério | onde ela olha | o que REPROVA |
|---|---|---|---|
| **B-1** | A janela abre **pelo menu de aplicativos** | o menu do sistema | ter de digitar o comando |
| **B-2** | A janela diz **qual versão** ela está vendo | um canto fixo da janela | não dizer. Hoje não diz (medido: zero ocorrência de versão em `src/hefesto_dualsense4unix/gui/main.glade`) |
| **B-3** | A aba **Sistema** diz, em texto que ela lê sem saber o que é DKMS, o estado das curas de kernel | o cartão *Saúde do sistema* | o cartão falar só de storm e detecção de janela, como hoje |
| **B-4** | Com os quatro controles ligados, os **quatro** aparecem na aba **Status** | a aba Status | um card faltando |
| **B-5** | O **touchpad** e o **giroscópio** respondem, **sem `sudo`** e sem mexer em grupo de usuário | a aba Status, com o dedo no touchpad | não responderem |
| **B-6** | Nenhum controle acende número de jogador, e a janela **diz por quê** | a aba Início e o plástico | um controle acender número. A decisão 12 vale inteira |
| **B-7** | Com um jogo aberto, ela sabe dizer **o que está valendo naquela sessão** — Hefesto ou nativo, Steam Input ligado ou não, quantos jogadores — sem terminal | a aba **No jogo** | ter de perguntar. Foi assim que este critério nasceu, em 11/08 |

### Bloco C — O plástico (com o controle na mão)

| # | critério | onde ela olha | o que REPROVA |
|---|---|---|---|
| **C-1** | Ela escolhe uma cor e **a barra muda**, no cabo e no rádio | o controle | a barra não mudar; ou o aviso da tela afirmar mais do que aconteceu |
| **C-2** | O teste de vibração vibra | o controle | não vibrar |
| **C-3** | Dois DualSense sobem pelo rádio **ao mesmo tempo** e os dois aparecem | a aba Status | um sumir. É o defeito que o `hefesto-hid-playstation` existe para curar, e hoje o `doctor` **não tem check nenhum** para esse módulo |

### Bloco D — A partida

| # | critério | onde ela olha | o que REPROVA |
|---|---|---|---|
| **D-1** | Um jogo de co-op abre com dois controles e **entram dois jogadores** | a tela do jogo | entrar um só, ou o jogador 2 cair no meio |

### O critério que vale mais que todos, e é negativo

> **N-1 — nada do que a fez funcionar veio de fora do `install.sh`.**
> Se em qualquer ponto ela precisou de um comando que não estava no instalador,
> aquele ponto **não está pronto** — e o comando vira passo do instalador, não
> linha de documentação.

---

## 2. O que hoje impede cada critério — MEDIDO em 11/08

### 2.1 O verde do `doctor` não prova o que o `install.sh` prometeu

O `install.sh` instala **três** módulos DKMS por padrão, sem flag. O `doctor`
tem check para **dois**: `check_hefesto_hid_nintendo_dkms` (`scripts/doctor.sh:3993`)
e `check_hefesto_rtw88_usb_dkms` (`:4053`). **Não existe check para o
`hefesto-hid-playstation`** — o módulo que carrega a cura da contenção de
Bluetooth, que é o defeito do critério C-3.

Pior: quando o módulo **não está instalado**, o veredito é `info`
(`scripts/doctor.sh:4002`), e `info()` (`:88`) apenas imprime — não conta falha.
**Numa máquina limpa onde os três falharam, o `doctor` sai verde.**

A falha é silenciosa por desenho: `scripts/dkms_lib.sh:269` e `:273` pulam o
módulo com aviso quando `dkms` ou os headers faltam — comportamento certo
(fail-safe, o in-tree continua) e **aviso errado**, porque some entre 46 passos.

### 2.2 O `install.sh` não garante o que os módulos precisam

Ele garante GTK3 (`install.sh:1225-1243`) e as bibliotecas do mic por Bluetooth
(`:1141-1157`). **Não garante `dkms`, nem `linux-headers-$(uname -r)`, nem
`build-essential`.** Consequência na máquina nova: os três forks não entram, o
`doctor` fica verde, e o comportamento diferente não tem explicação visível.

### 2.3 Os parâmetros viajam, mas só três aparecem no diagnóstico

O fonte tem **onze** `module_param`; a conf arma **dez**
(`assets/modprobe.d/hefesto-hid-nintendo.conf:81`); o `doctor` imprime **três**
(`scripts/doctor.sh:4030`). A paridade de escrita **já é portão**
(`tests/unit/test_paridade_quente_dos_instaladores.py`) e não precisa ser
refeita — o buraco é do lado do diagnóstico.

### 2.4 O `install.sh` nunca é executado por portão nenhum

Ele aparece nos workflows **uma vez**, no shellcheck (`.github/workflows/ci.yml`).
2826 linhas e 46 passos com zero cobertura de execução. Os testes que existem
**leem o texto** dele — bons, e cegos ao tempo de execução. É por isso que o
ensaio em casa (etapa 5) não é opcional.

### 2.5 O F-7 encolheu, e a conta continua desigual

`install.sh:1062` desvia todo formato que não é `native`, e `:1035` dá `exit 0`.
Das **46** chamadas de `step`, **34 estão depois da linha 1035**.

Fica de fora do caminho de pacote: toda a camada de Bluetooth de sistema, o
cmdline do kernel, a unit do daemon, o hotplug, a bandeja, o applet, o áudio, os
quatro passos da Steam e **a conferência final** — que é a linha que ela lê.

Já foi corrigido, e é justo registrar: o quirk de áudio, o broker, os três DKMS,
o initramfs, o teclado na tela e o WirePlumber **passaram** a rodar em todo
formato (`install.sh:1079-1139`).

### 2.6 O instrumento de LED afirma mais do que sabe

`scripts/doctor.sh:497` imprime que a cor por controle via sysfs está OK a
partir de um teste de **permissão de escrita** no nó.

Medido em 11/08: a **leitura** por sysfs de player LED não reflete o aparelho — o
`brightness_get` devolve uma variável em RAM do kernel, sem ida ao aparelho
(`hid-playstation.c:1348-1354`). A **escrita** sai no report; o que não existe é
releitura ([driver-hid-playstation](../protocol/driver-hid-playstation.md)).
O veredito é verdadeiro sobre a **permissão** e falso sobre o **efeito**.

### 2.7 A janela não sabe dizer o que ela é

Zero ocorrência de versão em `src/hefesto_dualsense4unix/gui/main.glade`; zero
ocorrência de `dkms` em todo o `src/`. No PC novo ela não terá como distinguir
"instalei a versão certa" de "instalei outra coisa".

### 2.8 O mapa ainda promete o que não morde

`python3 scripts/check_paridade_transporte.py` contra `docs/data/mapa-controles.csv`:
291 linhas, 37 afirmações fortes, **15 sem teste que morda**, 39 linhas com
mordida, 14 assimetrias não declaradas. O passo está no CI com
`continue-on-error`. **Isto não bloqueia o produto funcionar** — bloqueia o mapa
poder ser citado como prova numa nota de versão.

---

## 3. A ordem de execução, por DEPENDÊNCIA

```
  ETAPA 1  a verdade da instalação
     |        (o doctor passa a saber reprovar o que o install prometeu)
     |
     +---> ETAPA 2  os instrumentos param de afirmar demais
     |        |
     |        +---> ETAPA 3  a janela publica o que a máquina é
     |
     +---> ETAPA 4  os outros formatos param de prometer o que não fazem
                          |
  ETAPA 3 + ETAPA 4 ------+---> ETAPA 5  o ensaio em casa
                                    |
                                    +---> ETAPA 6  o lacre (versão e tag)
                                              |
                                              +---> ETAPA 7  a viagem
```

- **A ETAPA 1 é pré-requisito de tudo.** Enquanto o `doctor` sair verde com três
  curas ausentes, nenhum critério do Bloco A significa nada.
- **A ETAPA 2 é pré-requisito da 3.** Publicar na janela um veredito que o
  instrumento não sustenta é a armadilha que esta casa já pagou três vezes.
- **A ETAPA 4 depende da 1**, porque quem diz "este formato não tem a camada X"
  é o `doctor`.
- **A ETAPA 5 depende de 3 e 4**; a **6** depende da **5** (tag antes do ensaio
  é tag que se refaz); a **7** depende da **6** e das respostas da seção 0.

Correm em paralelo, sem travar nada: o censo do mapa (6.1) e a prova de tela (5.3).

---

## 4. As etapas, uma a uma

### ETAPA 1 — A verdade da instalação (~2 dias)

**1.1 O `install.sh` garante `dkms` e os headers — 3 h.** Bloco no molde do GTK3
(`install.sh:1225-1243`): detecta, pergunta com `ask_yn`, instala com `run_apt`,
e segue se ela recusar. Roda **antes** do passo `3i`, e vale no ramo de pacote.
*Pode dar errado:* headers podem não existir na distro. O bloco **avisa e segue**,
nunca aborta. *Prova:* teste exigindo a chamada acima do primeiro `install_dkms_*`.

**1.2 A sentinela de DKMS — 3 h.** O `install.sh` grava o que prometeu, no molde
que a casa já usa para o teclado na tela (`scripts/doctor.sh:3061`). Sem ela,
"ela pediu `--no-dkms`" e "o build falhou" são indistinguíveis no disco — e o
`doctor` reprovaria a escolha dela.

**1.3 O `doctor` REPROVA quando prometeu e não entregou — 4 h.**
`scripts/doctor.sh:4002` deixa de ser `info` quando a sentinela diz `prometido`
e o disco diz ausente. *Prova:* teste novo montando a sentinela nos quatro
estados, com a costura que já existe (`HEFESTO_DKMS_SRC_ROOT`, `scripts/dkms_lib.sh:33`).

**1.4 O check que falta: o `hefesto-hid-playstation` — 3 h.** É o módulo do
critério C-3. Hoje não tem veredito nenhum.

**1.5 O `doctor` imprime os dez parâmetros, não três — 1 h.**

### ETAPA 2 — Os instrumentos param de afirmar demais (~1 dia)

**2.1 O veredito do LED diz o que mediu — 3 h.** `scripts/doctor.sh:497` passa a
dizer que conferiu **permissão**, não efeito. *Quem prova que a luz acendeu é o
olho, não o `cat`.*

**2.2 Varredura de todo lugar que lê sysfs como prova — 3 h.** O arquivo já tem
o hábito certo em outro assunto (`scripts/doctor.sh:1957-1964`).

**2.3 O resumo conta o que não pôde medir — 2 h.** Sem controle na mesa, o verde
é verde de mesa vazia, e ela precisa saber sem ler 200 linhas.

### ETAPA 3 — A janela publica o que a máquina é (~2 dias)

**3.1 A versão na janela — 2 h.** No cabeçalho ou rodapé, **não** dentro de um
cartão de aba: a altura tem teto medido (`gui/main.glade:2446-2467`).

**3.2 O cartão *Saúde do sistema* ganha "Esta instalação" — 1,5 dia.** Uma linha
por eixo, em português de gente: o formato e a versão; o kernel e se as curas
estão em vigor — **nomeadas pelo que fazem**, não pelo nome do módulo; a versão
do BlueZ; e o veredito da última conferência. Texto de função **pura**, no molde
de `app/actions/daemon_actions.py:513`. *Prova:* funções puras testadas, foto das
dez abas, e **a palavra dela**.

**3.3 A janela diz o que está valendo NAQUELE jogo — 4 h.**

**Achado por ela, em 11/08, pelo caminho mais caro que existe: perguntando.**
Com quatro controles funcionando e um jogo aberto, ela perguntou *"esse é o modo
nativo ou é o modo steam input?"* — e a resposta só existia rodando um script no
terminal. A janela não dizia.

O que ela tinha na tela naquele momento, e que estava certo: a aba **Início**
mostrava **"Jogar pelo Hefesto"** e **"DualSense (botões PlayStation)"**, e no
perfil daquele jogo a caixinha **"Esconder o controle físico neste jogo"**
estava marcada. Três informações verdadeiras, em dois lugares diferentes, e
nenhuma delas responde a pergunta que ela fez — que é sobre a **sessão de
agora**, não sobre a configuração.

**O que falta aparecer, e é o que o terminal respondeu:**

- que **o Steam Input está ligado** para o jogo em sessão (consequência da
  caixinha, mas invisível depois de marcada);
- que **o wrapper injetou** as variáveis naquele processo — hoje só
  `scripts/medir_steam_virtual_gamepad.sh` sabe;
- **quantos controles virtuais existem** agora (P1, P2, ...), que é a resposta
  direta de "tenho co-op?";
- que **não há espelho** da Steam em cena — ou que há, se houver.

**Onde:** o painel da aba **No jogo** já é o lugar certo. Ele nasceu para dizer
o que o jogo está pedindo ao controle (giroscópio, vibração, luz), e esta é a
mesma pergunta um andar acima: *o que está no caminho entre o meu controle e o
jogo, agora*. A aba já aparece só quando há jogo aberto, o que é exatamente
quando a pergunta faz sentido.

**Por que 4 h e não mais:** o daemon já sabe tudo isso. O `state_full` publica os
controles e o `gamepad_emulation`; a leitura do ambiente do processo do jogo é a
mesma que o instrumento faz, e já está escrita. O trabalho é de tela e de
redação, não de mecanismo.

**Prova:** a pergunta dela, refeita. Com um jogo aberto, ela olha a aba **No
jogo** e sabe responder *"nativo ou Steam Input?"* sem terminal. Se precisar
perguntar de novo, não está pronto.

**Depende de:** 3.2 (o mesmo cartão e o mesmo molde de função pura). Não é
pré-requisito de nada — se o tempo apertar, cai, e o preço é ela continuar sem
saber o que está valendo sem chamar alguém.

### ETAPA 4 — Os formatos param de prometer o que não fazem (~1 dia)

**4.1 O aviso do `exit 0` diz o número — 2 h.**
**4.2 O portão que impede um passo mudar de lado sem ninguém ver — 2 h.** Conta
as chamadas de `step` dos dois lados da linha 1035 e fixa os números. É a
regressão do F-7, que aconteceu por acidente de posição.
**4.3 A decisão dos três níveis, escrita — 3 h.** Ver seção 7.

### ETAPA 5 — O ensaio em casa (~1,5 dia)

Existe porque o `install.sh` não é executado por portão nenhum (2.4).

**5.1 Usuária nova nesta máquina — 4 h.** Config vazia, primeira execução — o
caminho menos coberto do produto.
**5.2 O ciclo `uninstall` → `install` → comparar — 4 h.** Com o seguro que já
provou ser necessário: copiar os pareamentos para fora antes.
**5.3 A prova de tela das dez abas — 2 h.**

### ETAPA 6 — O lacre (~1,5 dia)

**6.1 O censo do mapa a zero — 1 dia.** As 15 células ou ganham a mordida, ou
**baixam a confiança para o que de fato são**. As duas saídas são honestas.
**6.2 Versão, CHANGELOG e tag — 4 h. Recomendação: `0.9.4`, não `1.0.0`.** O
motivo é a doutrina da casa: `ENTREGUE EM CÓDIGO` não é `VALIDADO POR ELA`. O
`1.0.0` é o número que se põe **depois** de o PC novo passar.

### ETAPA 7 — A viagem (~4 h dela)

**7.1 O roteiro de uma folha.** Com a linha mais importante de todas:

> **Reinicie depois de instalar, antes de julgar.** O passo do cmdline
> (`install.sh:1589`) só vale no próximo boot, e é ele que segura o storm com o
> microfone ligado. A primeira sessão pós-instalação **não** tem essa cura em
> vigor, e julgar ali é julgar outra máquina.

**7.2 A execução — ~3 h dela.**
**7.3 O retrato e a comparação — 1 h**, com a lista de diferenças esperadas
escrita **antes**, senão toda diferença de hardware vira suspeita de defeito.

---

## 4-bis. O caminho mínimo, se o tempo for curto

**Dois dias e meio**, não nove:

| item | por quê |
|---|---|
| **1.1 a 1.4** | sem isso o `doctor` mente na máquina nova, e o teste dela não decide nada |
| **2.1** | sem isso ela acredita que a cor chegou porque o `doctor` disse |
| **4.1** | sem isso, ao escolher um formato de pacote, ela não sabe o que não instalou |
| **5.2** | o único ensaio de execução que existe |
| **7.1 e 7.2** | o roteiro e a viagem |

O preço dos cortes: sem a **ETAPA 3**, ela precisa do terminal para saber o
estado. Sem o **6.1**, a nota de versão não pode citar o mapa. Sem o **5.1**, o
caminho de primeira execução é estreado por ela, no PC novo, ao vivo.

---

## 5. O que NÃO entra nesta versão, e por quê

| o que fica de fora | por quê |
|---|---|
| **F-2 — serializar a subida de dois controles no mesmo adaptador** | É **decisão de desenho dela**, não de código. Nesta versão entra o **diagnóstico** (1.4) |
| **F-6(a) — a aba Estado que afirma com a mesa vazia** | Refatorar o payload com 8.863 testes em volta, às vésperas de uma viagem. Risco alto |
| **B-1 — restauro automático de bonds** | Custo alto, mexe com credenciais |
| **Os externos como jogadores** | A resposta 3 os condicionou à máscara por controle, que não existe |
| **A luz de jogador voltar** | Decisão 12, confirmada pela 22. Não se repropõe |
| **Redesenhar os três SVG do zero** | Risco de licença aberto, mas **não bloqueia nada** |
| **As linhas de combinação do mapa** | Trabalho de bancada com hardware |
| **Validar Fedora, Arch e Nix em hardware** | Outra viagem |
| **Publicar no PyPI e no Flathub** | Não é necessário para o teste dela |
| **Fazer o `install.sh` rodar em CI** | É o furo estrutural certo de apontar, e é sprint própria: precisa de contêiner privilegiado, systemd e headers |
| **O `rtw88-usb` em kernel diferente** | Ele é pinado de propósito (`assets/dkms/rtw88-usb/dkms.conf:30`); em outro kernel o in-tree fica. Comportamento certo |

---

## 6. Os riscos que só aparecem na máquina nova

**R1 — O DKMS não compila lá.** Três sub-casos, todos terminando na mesma frase:
*a máquina se comporta diferente e ninguém entende por quê*. (a) `dkms` ou
headers ausentes: pulo silencioso hoje. (b) Presentes, mas o fonte não constrói —
só o `rtw88-usb` tem `BUILD_EXCLUSIVE_KERNEL`; os outros dois são fonte do 7.0.11
sem pino. (c) Constrói e **mascara um in-tree mais novo** — o pior, porque parece
sucesso. *Medição que falta:* ninguém nunca construiu os três contra um kernel de
outra série.

**R2 — BlueZ de versão diferente.** Abaixo de 5.79 é `fail`, e a cura exige `.deb`
que a máquina limpa não tem. Mitigação: pergunta 2 da seção 0, antes da viagem.

**R3 — Secure Boot.** O kernel recusa o `.ko` e **não** volta ao in-tree. Os
avisos existem e chegam **depois** da instalação. *Medição que falta:* ninguém
testou o produto com SB ligado.

**R4 — Distribuição diferente.** O `install.sh` nativo é família Debian
(`install.sh:354`). E a sessão muda quatro coisas de uma vez: bandeja, applet,
teclado na tela e detecção de janela.

**R5 — Hardware ausente na hora.** Verde de mesa vazia. Mitigação: item 2.3.

**R6 — O cmdline só vale no próximo boot.** É o risco mais provável de gerar um
falso "não funcionou lá". Mitigação: a linha em destaque do roteiro.

**R7 — Configuração vazia.** O caminho menos exercitado. Mitigação: item 5.1,
que o estreia **aqui**, onde dá para consertar.

**R8 — A Steam de lá é outra.** O critério D-1 é o último do roteiro; se falhar,
não invalida A, B e C.

**R9 — Sessão, assento e `uaccess`.** A regra que paga o F-8 depende de a sessão
ser do assento local e ativa. **Nunca foi medido fora desta bancada** — é o que
o critério B-5 existe para descobrir.

---

## 7. A recomendação de entrega: um canônico e três níveis

Hoje são sete formatos, e sustentar sete é parte do problema: cada cura nova
precisa ser costurada à mão em seis instaladores.

**A recomendação não é apagar quatro. É declarar níveis.**

### O canônico, para o teste dela: `native`

1. **É o único que roda o produto inteiro** — 34 das 46 chamadas de `step` estão
   depois do `exit 0`.
2. **É o único que roda a conferência final**, que é a linha que ela lê.
3. **É o que a casa já recomenda por escrito** (`README.md:177`).
4. **É o único com simetria de desinstalação.**

### Os três níveis

| nível | formatos | o que promete | o que o portão cobra |
|---|---|---|---|
| **1 — canônico** | `native` | tudo. O verde do `doctor` significa alguma coisa **aqui** | tudo, mais o ensaio da ETAPA 5 |
| **2 — empacotado e testado** | `.deb` | o aplicativo, as regras udev, os três DKMS e o broker. **Não** a camada de Bluetooth de sistema, nem o cmdline, nem a Steam | paridade **mais** construção e ciclo instalar/desinstalar |
| **3 — empacotado, sem validação** | Flatpak, AppImage, Arch, Fedora, Nix | o aplicativo. O resto depende de rodar `scripts/install-host-udev.sh` à mão | só paridade por texto. E a página onde alguém os escolhe **diz isso** |

O que muda na prática: uma cura nova passa a **bloquear** os níveis 1 e 2 e a
**registrar dívida datada** no nível 3, em vez de travar seis instaladores de uma
vez. A honestidade aumenta e o atrito cai.

**O que não se faz:** apagar os quatro do nível 3. Eles funcionam, custaram
trabalho, e removê-los para provar um ponto é destruir trabalho bom — a mesma
razão pela qual o encanamento de i18n ficou de pé quando a resposta 10 desfez a
promessa de tradução.

---

## 8. O que este plano NÃO sabe

1. **Ninguém construiu os três forks de DKMS contra outro kernel** que não o
   `7.0.11-76070011-generic`. É o furo com maior chance de decidir a viagem.
2. **Ninguém rodou o produto com Secure Boot ligado.**
3. **Ninguém abriu a janela com a configuração vazia** recentemente.
4. **Nada aqui foi executado.** Não se rodou `install.sh`, `uninstall.sh` nem
   `doctor.sh` — mudam o estado da máquina. Tudo vem de leitura de `caminho:linha`.
5. **A leitura por sysfs de player LED** está medida como cache, não como retrato
   do aparelho, e o fonte do driver explica por quê. A escrita é outra história:
   ela sai no report. O que se confirmou foi a leitura do fonte.
6. **O comportamento do `.deb` em máquina limpa** foi medido pelo `release.yml`
   (instalar e desinstalar em contêiner) e **nunca com hardware**. A frase "o
   `.deb` funciona" vale para instalar, não para jogar.

---

## 9. A conta

| etapa | custo | depende de | o que ela vê no fim |
|---|---|---|---|
| 1. A verdade da instalação | ~2 dias | — | o `doctor` reprova o que o install prometeu e não fez |
| 2. Instrumentos honestos | ~1 dia | 1 | nenhum veredito afirma efeito a partir de permissão |
| 3. A janela publica o estado | ~2,5 dias | 1, 2 | a versão e as curas de kernel, na aba Sistema |
| 4. Formatos honestos | ~1 dia | 1 | o aviso do install diz quantos passos pula |
| 5. O ensaio em casa | ~1,5 dia | 3, 4 | o ciclo comparado e as dez abas fotografadas |
| 6. O lacre | ~1,5 dia | 5 | a tag `v0.9.4`, com o CI verde na mesma SHA |
| 7. A viagem | ~4 h dela | 6 e a seção 0 | os quatro blocos de critérios, no PC novo |

**Total:** cerca de nove dias e meio de bancada e quatro horas dela. **Caminho mínimo:**
dois dias e meio.

E o `1.0.0` vem depois — não como promessa, como consequência da viagem ter dado
certo.
