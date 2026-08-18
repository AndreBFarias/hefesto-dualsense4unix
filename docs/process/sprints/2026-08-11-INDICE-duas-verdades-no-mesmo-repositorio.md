# ÍNDICE — duas verdades no mesmo repositório

- **Escrito em:** 11/08/2026, na branch `restauro/inicio-da-sessao`
- **Rótulo:** `ROTEIRO` — não é sprint de execução. É a fila de reconciliação,
  com o que cada sprint entrega e como se prova que funcionou
- **Nasceu de:** *"O que isso vai mudar na nossa guia de specs e do projeto como
  um todo, podemos materializar isso em sprints de correções estruturais? Aposto
  que deve ter muita coisa errada que os agentes notaram, info incorretas e todo
  o mais."*
- **E de uma correção de rumo dela, no meio deste documento:** *"substituir pela
  info certa não seria melhor? Seria menos texto pros agentes lerem e pros devs
  também. seria um passo rumo a simplificação do produto e a
  descomplexificação"* — que virou a regra da seção 1 e reescreveu a família A
  inteira

**Grau, por bloco, como manda a casa:** **MEDIDO** = há `caminho:linha`, `grep`
ou teste que fecha a conta; **SUSPEITA COM MECANISMO** = o caminho foi lido e
fecha, o efeito não foi observado; **SEM PROVA** = está dito e ninguém
verificou; **DECISÃO DELA** = não se repropõe. Cada bloco declara o seu e **não
herda** do bloco de cima.

**Ela estava certa sobre o tamanho do problema.** A encomenda listava oito
contradições conhecidas. A apuração fechou em **quarenta e uma**, três delas
dentro dos próprios documentos novos — e a mais cara não é de protocolo: é uma
frase na página que a usuária lê, errada desde 09/08.

---

## 1. A regra que esta leva fixa: substituir o fato errado, datar a decisão medida

**GRAU: DECISÃO DELA**, tomada em 11/08/2026.

A casa tinha uma regra só — *não se apaga decisão medida* — e ela vinha sendo
aplicada a tudo, inclusive a número errado. O resultado é o que este índice
existe para pagar: páginas em que a informação certa chega depois de três
parágrafos explicando a errada.

**Decisão medida não é a mesma coisa que fato desatualizado.** São dois casos:

| caso | o que se faz | por quê |
|---|---|---|
| **FATO ERRADO** | **substituir.** O texto errado sai, o certo entra. Sem nota, sem tarja, sem histórico | não há decisão a preservar. Manter `P4 = x-xx-` ao lado de `P4 = xx-xx` obriga a próxima pessoa a escolher entre duas afirmações, e ela pode escolher errado |
| **DECISÃO MEDIDA** | **datar.** A nota fica, com o que caducou e o preço que se pagou | é o registro que impede alguém de desfazer sem saber o custo |

**O teste que separa os dois, e é uma pergunta só:**

> Se a informação errada fosse apagada hoje, alguém repetiria um trabalho ou
> pagaria um custo já pago?

Se **sim**, é decisão medida e leva data. O exemplo canônico é *"o envio
automático do `0x08` foi removido em 03/08 porque era a causa do defeito que
veio curar"*: apagar isso faz alguém reintroduzir o `0x08` daqui a dois meses
achando que está curando. Se **não** — se é só um número errado, uma afirmação
que a medição derrubou — é fato errado, e sai.

**Na dúvida, datar.** Errar para o lado de guardar é reversível; errar para o
lado de apagar não é. Toda linha deste índice em que houve dúvida está na
família B, e a dúvida está dita.

**Isto vale para todas as levas seguintes.** É simplificação de produto, não
faxina de documento: página menor é página que se lê inteira, e página que se lê
inteira é a que impede a próxima regressão.

---

## 2. O que entrou em 11/08, e a régua de quem tem razão

**GRAU: MEDIDO** (`git status` da árvore de trabalho de 11/08/2026).

Oito documentos novos, e **nenhum deles está commitado**: todos aparecem como
`A` no índice do git. Quem executar este roteiro trabalha sobre a árvore, que é
o que roda.

| documento | linhas | o que traz |
|---|---:|---|
| [`docs/protocol/driver-hid-playstation.md`](../../protocol/driver-hid-playstation.md) | 883 | o fonte do DKMS do DualSense, lido linha a linha |
| [`docs/protocol/driver-hid-nintendo-por-dentro.md`](../../protocol/driver-hid-nintendo-por-dentro.md) | 828 | o mesmo, para o Pro e o clone 8BitDo |
| [`docs/protocol/pilha-steam-input-xpad-sdl.md`](../../protocol/pilha-steam-input-xpad-sdl.md) | 992 | Steam Input, `xpad`, SDL e o gamepad virtual |
| [`docs/protocol/externos-firmware-e-modos.md`](../../protocol/externos-firmware-e-modos.md) | 972 | firmware e os modos do 8BitDo |
| [`docs/process/2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md`](../2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md) | 478 | o que só existe nesta máquina |
| [`docs/process/2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md`](../2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md) | 430 | o plano até a versão final |
| [`docs/usage/versoes-validadas.md`](../../usage/versoes-validadas.md) | 81 | a matriz de versões |
| [`docs/process/estudos/2026-07-19-estudo-bluez-backport-onda-r.md`](../estudos/2026-07-19-estudo-bluez-backport-onda-r.md) | — | a receita do backport de BlueZ, que faltava |

Junto vieram dois testes novos
(`tests/unit/test_versoes_validadas_batem_com_o_codigo.py` e
`tests/unit/test_receita_do_backport_esta_na_arvore.py`) e **119 linhas líquidas novas no
`install.sh`**. **Não reproponha nada disso:** já está no disco, e três seções
dos próprios documentos novos já caducaram por causa dele (seção 3.6).

**A régua que decide quem tem razão**, e vale para a seção 3 inteira:

1. **O fonte do driver vence documentação**, quando o assunto é o que o kernel
   manda ao aparelho. É o grau `FONTE DESTA MÁQUINA`: não é *"o kernel faz
   assim"*, é *"este kernel, o que compilou o módulo carregado agora, faz
   assim"*.
2. **Medição vence suposição**, quando a régua está declarada e foi validada
   contra contagem independente.
3. **O fonte do driver NÃO vence o aparelho.** Ele prova o que o Linux manda,
   não o que o firmware faz com aquilo.
4. **O disco vence os dois.** Onde um documento afirma que um arquivo existe, ou
   que um passo não é dado, quem decide é `ls` e `grep`.
5. **Onde nada foi medido, isso fica escrito** — e vira uma linha da família E.

---

## 3. As contradições

**GRAU: MEDIDO** — cada `caminho:linha` dos dois lados foi aberto e conferido na
árvore de 11/08/2026. A coluna **trato** aplica a régua da seção 1: `SUBST` (fato
errado, substituir) ou `DATAR` (decisão medida, nota datada).

### 3.1 O protocolo do DualSense

| # | onde | o que diz | o que a fonte nova diz | quem tem razão | trato |
|---|---|---|---|---|---|
| P-1 | `docs/protocol/dualsense-referencia-canonica.md:533` e `:540` | player LED P4 = `x-xx-` | `player_ids[3] = BIT(4)\|BIT(3)\|BIT(1)\|BIT(0)` = `0b11011` = `xx-xx` (`assets/dkms/hid-playstation/hid-playstation.c:1836-1842`) | **o fonte do driver.** O código desta casa sempre esteve certo (`core/led_control.py:105-114`); o `x-xx-` é, byte a byte, o `_PLAYER_LED_OVERFLOW` de `:119` | SUBST |
| P-2 | o mesmo, `:45` (índice do que caducou) e `:743` (fila de perguntas) | *"CONTRADIÇÃO doc x código — não medido"*, e a pergunta 3 aberta | resolvida pelo fonte, para o que o Linux manda | idem, com o limite de que o console PS5 não foi observado | SUBST, com a ressalva escrita |
| P-3 | o mesmo, `:491-494` e a nota de `:496-521` | *"a taxa NUNCA foi medida, em transporte nenhum"* | cabo **250,0 Hz** por duas réguas, e o descritor concorda (`bInterval 6` em High Speed = 4000 us); rádio **em rajadas**, 38,3 a 392,4 Hz de média, nunca 1000 Hz | **a medição.** As duas réguas concordam entre si e com o descritor | SUBST o *"nunca medido"*; DATAR o que sobra |
| P-4 | o mesmo, `:192` | *"o fonte do `hid-playstation` não foi relido nesta passagem"* | foi relido, é o desta máquina, e as citações têm número de linha | **o disco** | SUBST |
| P-5 | o mesmo, `:124`, `:764`; e `externos-referencia-canonica.md:1198`, `:1200` | citam `github.com/torvalds/linux/blob/**master**/...` | `master` é alvo móvel, e estava em `7.2.0-rc7` no dia — numeração diferente da `v7.0` | **a régua nova** (`pilha-steam-input-xpad-sdl.md:62-65`): quem cita fonte **declara a tag** | SUBST |
| P-6 | o mesmo, `:176`, `:227`, `:647` | raciocinam sobre o **kernel 6.18**, e `:647` declara **grau ALTA** com base nele | o que roda aqui é `7.0.11-76070011-generic`, e é um DKMS, não o vanilla | **o disco.** Grau ALTA declarado contra um kernel que não é o desta máquina é a colisão mais direta com a régua P-5 | SUBST |
| P-7 | `docs/adr/008-bt-vs-usb-polling.md:7-8` | *"USB: 1000Hz possível"* e *"BT: 250Hz típico"* | USB é 250 Hz exatos, imposto pelo endpoint; o rádio não tem taxa típica | **a medição.** Esta linha **nunca foi conferida**: as notas de 25/07 e 31/07 do ADR corrigiram o `poll_hz` e a fixture e passaram ao largo dos dois números | SUBST |
| P-8 | o mesmo, `:14` | afirma que `tests/fixtures/hid_capture_bt.bin` existe e que *"Testes W1.3 cobrem ambos"* | nunca existiu | **o disco.** A nota de `:35-52` já dizia isso desde 31/07, e a frase errada continua na Decisão logo acima — duas verdades na mesma página | SUBST a frase; DATAR a nota de `:35-52` |
| P-9 | `docs/protocol/paridade-bluetooth-versus-cabo.md:50` e `:84` | rádio *"~300 Hz"*, cabo sem número | rádio entre 38 e 392 Hz conforme a janela; cabo 250,0 Hz | **a medição nova**, que corrobora a antiga em faixa e a corrige em estabilidade | SUBST o número; DATAR a régua antiga |
| P-10 | o mesmo, `:145` | *"o SDL atribui 1000 Hz a um Edge por **USB** enquanto o espelho entrega ~300"* | os ~300 Hz são do **rádio**; por USB são ~250, e a razão é 4 | **a medição.** A frase mistura os dois transportes num par único | SUBST |
| P-11 | `docs/protocol/driver-hid-playstation.md:756-757` | chama `GYRO-EDGE-RATE-01` de **"sprint"** | não existe arquivo com esse nome; é **nome de divergência** | **o disco.** É a quarta página com o vício, e a única que a nota do documento irmão não lista | SUBST |
| P-12 | `src/hefesto_dualsense4unix/core/physical_report_reader.py:8`, `:26`, `:176`, `:191`, `:803`, `:842`; `integrations/uhid_gamepad.py:949`, `:962`; `core/evdev_reader.py:121`, `:842` | *"o BT desta máquina entrega ~765 Hz por controle"*, como taxa **sustentada** | 765 Hz é a taxa **instantânea dentro da rajada** (o p05 do intervalo é 1255 us); a sustentada fica entre 38 e 392 Hz | **a medição.** O número não some: muda de significado | SUBST o número; DATAR a decisão do teto |

### 3.2 Os externos — Pro Controller e 8BitDo

| # | onde | o que diz | o que a fonte nova diz | quem tem razão | trato |
|---|---|---|---|---|---|
| X-1 | `docs/protocol/externos-referencia-canonica.md:807-811` | *"Não está na mesa"*, *"Nada do que esta página afirma sobre o 8BitDo foi medido naquele modo"* | em 11/08 ele esteve na mesa em modo Switch **pelo cabo** e completou a probe inteira: dois inputs, `hidraw7`, cinco LEDs, bateria, calibração de fábrica | **a medição** | SUBST o estado; DATAR a advertência de método, que vale para o **rádio** |
| X-2 | `docs/usage/troubleshooting-8bitdo.md:190-192` | **PROVADO**: *"no bind aparece `unknown main item tag 0x0` — descriptor HID malformado, típico de firmware clone; o original não produz isso"* | zero linhas no `journalctl -k` do boot inteiro, e os 203 bytes do descritor parseados item a item sem um item malformado | **a medição**, para a **generalização**. Em que modo a linha de 25/07 apareceu continua **SEM PROVA** | SUBST o `PROVADO` e a generalização; DATAR a observação de 25/07 |
| X-3 | `docs/usage/troubleshooting-8bitdo.md:49` (e `:10`, `:29`, `:42`, `:75`, `:80`, `:199`); `docs/usage/bluetooth.md:110`, `:116`; `docs/usage/modos.md:131`; `docs/usage/troubleshooting.md:776`; `docs/protocol/externos-referencia-canonica.md:8`, `:80`, `:88`, `:560`, `:639`, `:988`, `:1001` | chamam `Start + A` / `054c:05c4` de **"modo DirectInput/PS4"** | na nomenclatura do fabricante isso é o **modo macOS**; o D-input de verdade é `B + Start`, `2dc8:6001` | **o fabricante**, e a própria árvore já sabia: `externos-referencia-canonica.md:753` lista `D-input` e `macOS` como modos distintos | SUBST o nome nas 17 ocorrências |
| X-4 | o mesmo vício em código e assets: `app/actions/external_controllers.py:62`; `daemon/subsystems/external_identity.py:53`, `:123`; `daemon/launch_env.py:233`; `assets/dkms/hid-playstation/README.md:10`, `:328`, `:470`; `assets/modprobe.d/hefesto-hid-playstation.conf:69`; `assets/72-hefesto-touchpad-motion-uaccess.rules:105` | idem | idem | idem. **Uma das ocorrências vai para o upstream** (o cabeçalho de `assets/dkms/hid-playstation/patch/0002-*.patch`), e é a que mais importa acertar | SUBST |
| X-5 | `docs/usage/troubleshooting-8bitdo.md:33` e `:169` | X-input por Bluetooth marcado `EXPERIMENTO`, *"PID provável `02e0`/`02fd`"*, driver `hid-microsoft`/`hid-generic` | `02e0` **confirmado**, e o driver é o `hid-microsoft` | **a medição** | SUBST |
| X-6 | `docs/protocol/externos-referencia-canonica.md:1043-1048` (P-2) e `:825-831` | *"que o 8BitDo mantenha o mesmo endereço de rádio nos dois modos nunca foi medido aqui. GRAU: BAIXA"*, e a regra `82-nintendo-pro-nosniff.rules` *"pode estar acertando por sorte"* | **já estava respondida** desde 25/07, medida em `docs/usage/troubleshooting-8bitdo.md:104-117` e na [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md), que mediu **dois endereços, um por modo** | **o disco.** Uma pergunta aberta na canônica que outra página do mesmo repositório já respondia há duas semanas | SUBST a P-2; DATAR o achado da IDENT-01 no lugar certo |
| X-7 | `assets/dkms/hid-nintendo/README.md:173` | o patch `0003` foi *"escrito e compilado, mas nunca carregado — nada foi instalado"* | está no ar, e foi ele que fez o clone probar inteiro | **o disco** | SUBST |
| X-8 | `docs/protocol/externos-referencia-canonica.md:415-453` (seção 3.6, os LEDs do Pro) | não traz o aviso do sysfs | o aviso existe na mesma página, em `:750`, escrito só para a lightbar do `ds4` | **a doutrina da casa**, que está incompleta no lado Nintendo | SUBST (propagar o aviso) |
| X-9 | `docs/protocol/externos-firmware-e-modos.md:731-752` contra `docs/data/mapa-controles.csv`, chave `identidade.firmware@sn30` | *"Firmware de 8BitDo se atualiza pela ferramenta do fabricante — fora do repositório"* | o `fwupd` **está instalado** (1.9.32, plugin `ebitdo`) e o `builtin.quirk` desta máquina **já reconhece** `2DC8:6001`/`6002` | **a medição** | SUBST |

### 3.3 A pilha Steam Input, o SDL e o gamepad virtual

| # | onde | o que diz | o que a fonte nova diz | quem tem razão | trato |
|---|---|---|---|---|---|
| S-1 | `docs/process/sprints/2026-08-10-TRES-CONTROLES-01-o-espelho-do-espelho-no-pragmata.md:39-42`; a cópia em `src/hefesto_dualsense4unix/daemon/launch_env.py:123-125`; a docstring de `tests/unit/test_tres_controles_no_pragmata_01.py:24-27` | a causa declarada: *"os espelhos da Valve nunca estiveram em lista nenhuma deste projeto, e o jogo ficava com três"* | o SDL **retorna antes** de consultar `SDL_GAMECONTROLLER_IGNORE_DEVICES` para o par `28de:11ff`. Com a variável `SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD` ausente ou 0 a cura é **redundante**; com ela em 1 é **inerte** | **ninguém ainda.** O ramo foi lido e fecha; o valor da variável no ambiente do jogo **NÃO FOI MEDIDO** — a Steam estava fechada. **GRAU: SUSPEITA COM MECANISMO** | fica como está até E-4 |
| S-2 | o agravante de S-1 | — | a variável **não está** na `ENV_ALLOWLIST` (`daemon/launch_env.py:80-87`), então, se a Steam a puser em 1, **o produto não tem como sobrescrever** | **o fonte.** Isto torna E-4 bloqueante, não só diagnóstico | — |
| S-3 | `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:117-122` | *"duas ressalvas honestas"* sobre escolher o PID `0x0DF2` | são **cinco** efeitos: `enhanced_rumble` forçado (muda o formato do rumble), nome trocado, **17 botões anunciados em vez de 13**, taxa declarada 1000 Hz por USB, e o banco de mapeamentos da SDL3 dela só ter entrada de **Bluetooth** para o Edge, enquanto o vpad nasce `BUS_USB` | **o fonte**, com a última consequência em **BAIXA** | SUBST (as ressalvas passam a ser cinco) |
| S-4 | `src/hefesto_dualsense4unix/daemon/launch_env.py:186-188` e [MASCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md)`:517-519` | citam `proton:1828` só como prova de **formato** da lista | a lista da Valve **contém `0x054C/0x0DF2`**, que é o PID do nosso vpad, e é **atribuição**, não acréscimo: se disparar, substitui o que o wrapper exportou | **o fonte.** Não dispara nesta máquina (exige `SteamDeck == "1"`), e é exatamente o que `launch_env.py:293-299` proíbe em caixa alta | SUBST (a citação ganha o que faltava) |
| S-5 | `src/hefesto_dualsense4unix/daemon/launch_env.py:903` e 22 outros arquivos | citam **`GUERRA-01 (estudo 2026-07-18)`** | **não existe arquivo com esse nome nem com essa data.** É a mesma doença do `GYRO-EDGE-RATE-01`, em 23 arquivos | **o disco.** E o documento novo **propagou** a citação em vez de a diagnosticar | SUBST (ou o estudo nasce, ou a citação diz o que é) |
| S-6 | `assets/84-nintendo-pro-variant.rules:2`; `scripts/install_udev.sh:151`; `scripts/install-host-udev.sh:217` | citam a sprint `NINTENDO-VARIANT-01 (2026-07-25)` | **não existe** arquivo de sprint com esse nome | **o disco.** Terceira ocorrência do mesmo vício | SUBST |
| S-7 | `docs/process/sprints/2026-08-10-ESTADO-DA-NOITE-01-o-que-ela-achou-com-o-controle-na-mao.md:100-103` | *"cinco suspeitos caíram"* no defeito do rumble | são **seis**: o sexto (o vpad descartar o rumble do SDL por falta do bit `0x01`) **cai também**, com grau ALTA | **a leitura de fonte** | SUBST a contagem |

### 3.4 As páginas que ela lê — e esta é a família mais cara

**GRAU: MEDIDO.** Uma correção de produto que nunca desce para `docs/usage/` é
meia correção: a próxima pessoa a abrir a página aprende o comportamento antigo.

| # | onde | o que diz | o que vale | trato |
|---|---|---|---|---|
| U-1 | `docs/usage/jogos-e-mascaras.md:43-45` | *"Com a exceção ativa (…) **o gamepad virtual sai de cena: nesse jogo vale só o controle 1, sem co-op**"* | **falso desde 09/08.** A [ESCONDER-EM-VEZ-DE-SAIR-01](2026-08-09-ESCONDER-EM-VEZ-DE-SAIR-01-o-duplicado-cura-pelo-outro-lado.md) matou esse ramo: hoje o jogo marcado recebe a mesma env de qualquer outro, e **o vpad continua de pé**, justamente para não derrubar o jogador 2. O obituário está em `daemon/launch_env.py:47-58` | SUBST |
| U-2 | o mesmo, `:49-50` | a nota datada de 06/08 repete *"tira o virtual de cena"* | idem. A nota corrigiu a metade da **saída** (cor e gatilho) e deixou a metade da **entrada** errada | SUBST a frase; DATAR o resto da nota, que continua certo |
| U-3 | `src/hefesto_dualsense4unix/cli/cmd_coop.py:76-78` | *"O co-op também sai de cena sozinho nos jogos com Steam Input"* | os vpads dos **secundários** também deixaram de ser recolhidos | SUBST |
| U-4 | `tests/unit/test_a_frase_refutada_da_allowlist.py:36-37` | isenta a frase acima como *"verdade medida: os vpads dos secundários são recolhidos"* | **a isenção caducou em 09/08**, e é ela que impede o portão de pegar U-3 | SUBST |
| U-5 | `docs/usage/jogos-e-mascaras.md:31-32` | com a máscara Xbox *"o que se perde é o giroscópio (a API do XInput não tem canal de movimento) e os gatilhos adaptativos"* | são **cinco** perdas — giroscópio, touchpad, lightbar RGB, gatilhos adaptativos e bateria — e a causa não é a API do XInput: **é o protocolo**, demonstrado por três camadas independentes | SUBST (contagem e causa) |
| U-6 | `docs/usage/quickstart.md:10` | promete *"Pop!_OS, Ubuntu, Fedora, Arch, Debian, Mint"* | o `install.sh` nativo só sabe `apt-get` (`install.sh:354`), e a matriz nova valida **uma** bancada | SUBST |
| U-7 | `docs/usage/instalacao.md:28-29` e `:143-146` | `dkms` e headers como **"Opcionais"**, *"sem eles o instalador só avisa e segue"* | desde 11/08 o instalador **oferece instalar**, com `ask_yn` (`install.sh:1317-1344`), e `build-essential` entrou na conta | SUBST |
| U-8 | `docs/usage/bluetooth.md:84-85` | *"subir de 5.72 para 5.86 **não reduziu a taxa** nesta máquina: quatro abortos em cinco dias no 5.86, contra cinco em cinco dias no 5.72. GRAU: MEDIDO"* | `docs/usage/versoes-validadas.md:22` e `scripts/doctor.sh:2487` **reprovam** abaixo de 5.79 por *"6 em 5 dias"* | **as duas são MEDIDO, e apontam para lados opostos.** Nenhuma é fato errado: é a mesma medição com amostra que não decide tendência — e é o `fail` do doctor que decide a viagem | DATAR, nas duas, com a reconciliação escrita |
| U-9 | `docs/usage/versoes-validadas.md:20` | Python `>= 3.10`, *"quem confere: `pyproject.toml`"*, e fora da faixa *"a instalação não começa"* | quem barra é o `pip`. O `install.sh:1154` só faz `require python3`, e `require()` (`:362`) é `command -v`; o `doctor.sh` **não confere Python em lugar nenhum** | SUBST |
| U-10 | `docs/usage/versoes-validadas.md`, o arquivo inteiro | — | **é página órfã**: a única referência no repositório é o próprio teste. Nem o `README.md`, nem `instalacao.md`, nem `quickstart.md` apontam para ela | SUBST (ganhar entrada) |

### 3.5 Os instrumentos, o código e o mapa

| # | onde | o que diz | o que vale | trato |
|---|---|---|---|---|
| I-1 | `scripts/doctor.sh:497` | `pass` com *"cor por-controle via sysfs OK (regra 77 valendo)"* | o que foi conferido é `[[ -w ... ]]` (`:489`) — **permissão**, não efeito. O comentário do próprio check, em `:476-477`, já diz *"Só `test -w`: este check NUNCA escreve no nó"* — **o comentário sabe, e a mensagem não** | SUBST |
| I-2 | `src/hefesto_dualsense4unix/core/sysfs_leds.py:239` e `:265` | *"Padrão **ACESO** dos LEDs de player"* e *"estado **físico** via classe"* | não existe leitura de estado: no `hid-playstation` o `brightness_get` devolve um `u8` em RAM (`hid-playstation.c:1348-1354`); no `hid-nintendo` não há `brightness_get` nenhum, e o `GET_PLAYER_LIGHTS` (`0x31`) é definido e jamais chamado. A nota datada equivalente já existe em `core/external_leds.py:202-206`, e **este arquivo não a recebeu** | SUBST |
| I-3 | `src/hefesto_dualsense4unix/core/external_leds.py:45-56`, `:109-112`, `:253-256` e a escrita de `:135` | o `:blue:player-5` é tratado como **bit "+5" da numeração**, e o clone é descrito como *"hardware SEM o nó azul"* | é o **LED HOME**: `LED_FUNCTION_PLAYER5` sob `jc_type_has_right()`, subcomando `0x38`, escala **0 a 15**. E o clone **tem** o nó, com `max_brightness=15` — o ramo `tem_azul == False` nunca dispara neste hardware. A escrita de `:135` manda `1` num nó de 0-15, ou seja **1/15 de brilho no anel de Home** | é **defeito de código**, não de página. Ver D-2 |
| I-4 | `src/hefesto_dualsense4unix/app/actions/external_controllers.py:63`, `:79`, `:114` | *"por cabo o `uniq` vem vazio e caímos no VID"*, e a marca por OUI *"só desambigua no transporte BT"* | por cabo, em modo Switch, o `hid-nintendo` **preenche** o `hdev->uniq` e o `brand_of` acerta "8BitDo". E por cabo no modo macOS o `hid-playstation` entrega um `uniq` **sintético** começando em `02:`, que cai em `"054c": "Sony"` — o caso real não é `uniq` ausente, é `uniq` **fabricado** | SUBST os três comentários; ver D-3 |
| I-5 | `assets/84-nintendo-pro-variant.rules` + `scripts/doctor.sh:186`, `:196` + `install.sh:1449` | a regra é escrita, instalada, conferida e **anunciada** (*"separa o Pro genuíno do 8BitDo clone"*) | **ninguém no produto lê a marca**: `grep -rn HEFESTO_CONTROLLER_VARIANT src/` devolve zero. É [a cura escrita e nunca ligada](../estudos/2026-08-07-O-QUE-EXISTE-E-NAO-CHEGA-a-cobertura-do-install.md), e o `doctor` só confere a **presença do arquivo** | a dívida é antiga; o que 11/08 acrescenta são as três medições que a destravam (a marca está viva no `hidraw`, não está no device `hid`, e **por Bluetooth é impossível**) |
| I-6 | `docs/data/mapa-controles.csv`, 291 linhas, 97 chaves | zero citações às quatro páginas novas de protocolo; zero ocorrências de `250,0`, `bInterval`, `firmware_version`, `blink_set`, `feature_retries` | as quatro páginas respondem, por fonte, células que o mapa declara *"ninguém respondeu"*. Ver a seção 4 | SUBST |
| I-7 | `docs/data/mapa-controles.csv`, chave `plataforma.taxa_relatorios@sn30` | `existe = nao-tem` | medido: **200,5 amostras/s**, duas vezes, por duas réguas — e a IMU do clone é **real e calibrada na mesma unidade** do genuíno (eixo Z parado em ~4200 nos dois) | SUBST |

### 3.6 Os documentos novos que já nascem errados

**GRAU: MEDIDO.** Isto não desqualifica os oito documentos — qualifica a
velocidade da leva. Três frentes trabalharam no mesmo dia, e a que consertava o
`install.sh` andou mais rápido que a que o auditava.

| # | onde | o que diz | o que vale |
|---|---|---|---|
| N-1 | ~~os dois documentos de processo, em toda citação de `install.sh`~~ | ~~citam a numeração de `HEAD`~~ | **CURADO em 11/08, depois desta auditoria.** 128 citações foram realinhadas por diff, em 30 documentos — não só nos dois de processo, porque os históricos também apontavam para a numeração antiga. O `install.sh` fechou o dia com **+119 líquidas** e os blocos novos subiram para antes do desvio de formato |
| N-2 | `PRODUTO-EM-MÁQUINA-NOVA:110` e a ETAPA 1.1 (`:204`) | *"o `install.sh` **não garante** `dkms`, nem `linux-headers`, nem `build-essential`"*, com 3 h de custo | **já garante**: `install.sh:1317-1344` detecta os três, pergunta com `ask_yn` e instala. O conserto foi feito lendo este mesmo documento, e o documento não soube |
| N-3 | `O-DELTA-DA-MÁQUINA-LIMPA:172-174` e `:183-184` | *"a receita para regerar os `.deb` (…) vive **fora da árvore de trabalho**, num ramo arquivado"* | **vive na árvore desde 11/08**, e há portão (`tests/unit/test_receita_do_backport_esta_na_arvore.py`) que proíbe a forma antiga voltar. O `PRODUTO`, do mesmo dia, afirma o contrário no `:27` |
| N-4 | `PRODUTO-EM-MÁQUINA-NOVA:20-37` (as três perguntas dela) | trata as três como perguntas em aberto para ela responder no PC novo | **as três já são checadas pelo instalador**, no passo 1, pelo voo de reconhecimento (`install.sh:1171-1212`) — e `docs/usage/versoes-validadas.md:69-78` já documenta isso |
| N-5 | `O-DELTA-DA-MÁQUINA-LIMPA:413` | *"li as **33** condições de `fail` de `scripts/doctor.sh`"* | são **36** |
| N-6 | ~~`PRODUTO-EM-MÁQUINA-NOVA:125`~~ | ~~o `install.sh` tem *"2826 linhas"*~~ | **RETRATADO em 11/08.** `git show HEAD:install.sh | wc -l` devolve exatamente **2826** — o documento acusado estava certo contra `HEAD`. Executar este item como escrito trocaria um número certo por um errado. Fica como lápide: a auditoria também erra, e o portão dela é a mesma medição que ela cobra dos outros |
| N-7 | `PRODUTO-EM-MÁQUINA-NOVA:154` | *"zero ocorrência de `dkms` em todo o `src/`"* | são três (`core/external_leds.py:347`, `core/evdev_reader.py:295`, `daemon/subsystems/external_identity.py:115`), todas em comentário. **A conclusão se sustenta; a contagem, não** |
| N-8 | `driver-hid-nintendo-por-dentro.md:519-522` | atribui à seção 1.2 da canônica dos externos a frase *"com o link de pé e sem HID nenhum"* sobre o modo Switch | a seção 1.2 (`externos-referencia-canonica.md:117`, `:122-123`) é sobre o **modo PS4 por Bluetooth**, outro device |
| N-9 | `driver-hid-nintendo-por-dentro.md:751-753` | lista como *"não consegui verificar"* se o clone responde `REQ_DEV_INFO` e se a identidade foi sintetizada | **o documento irmão do mesmo dia fechou os dois** (`externos-firmware-e-modos.md:90-122`): responde, e a identidade é real (`E4:17:D8`) |
| N-10 | `driver-hid-nintendo-por-dentro.md:549` | *"IMU de verdade: sim — 200,5 amostras/s medidas"* | **corrigido pelo irmão** (`externos-firmware-e-modos.md:700-729`): a taxa sozinha não prova sensor real; o que prova é a distribuição por eixo |
| N-11 | `pilha-steam-input-xpad-sdl.md:699-700` | *"a taxa real do vpad nunca foi medida em transporte nenhum"* | `driver-hid-playstation.md:758-759`, do mesmo dia, afirma *"o cabo agora está medido e é exatamente 250 Hz"*. A frase só é literalmente verdadeira se *"do vpad"* excluir *"do físico que o vpad espelha"* — distinção que o documento não faz |
| N-12 | `pilha-steam-input-xpad-sdl.md:473` | cita `GUERRA-01` como documento existente | **propaga** o defeito de S-5 em vez de o registrar |

**Trato de toda a seção 3.6: SUBST.** São números e estados, não decisões. As
três frentes de 11/08 se cruzaram; o conserto é reconciliar, não guardar.

### 3.7 O que NÃO é contradição, e por que está aqui

Sem isto, a próxima pessoa refaz o trabalho.

| item | o que a apuração achou |
|---|---|
| **o IMU do Pro, 8 ms** | **já estava refutado** antes desta leva: `docs/protocol/externos-referencia-canonica.md:361` diz `refutado nesta mesa` desde 07/08, e as sete outras citações do número no repositório já vêm rotuladas *"declarado"*. Varridos `docs/`, `src/`, `scripts/`, `assets/` e os dois CSV: **nenhum lugar afirma 8 ms como taxa real**. O que 11/08 acrescenta é a terceira rota (11,27 ms), que sobe a confiança e não muda o lado. **Nada a substituir** |
| **o P4 na guia de specs** | **já corrigido na árvore**: a célula `luz.led_jogador@dualsense` do CSV traz o veredito com `hid-playstation.c:1836-1842`. O que falta é a canônica, e é a A-1 |
| **"a rota sysfs de player LED não chega ao aparelho"** | **impreciso, e a imprecisão importa.** A **escrita** chega: agenda o `output_worker` no DualSense e chama `joycon_set_player_leds` no Nintendo. O que não chega é a **leitura**. E nesta máquina há um caminho a mais para divergir, ligado de propósito: com `register_leds_on_set_failure=Y` o fork registra o nó **mesmo quando o único `set` falhou com `-ETIMEDOUT`**, e o nó passa a afirmar um padrão que o aparelho nunca recebeu. A frase certa é a da página nova: **fonte de intenção, nunca de estado** |
| **a cura da TRES-CONTROLES-01** | **não está refutada, está sob suspeita.** Ver S-1: o ramo foi lido e fecha, o efeito não foi observado. Quem a marcar como errada hoje está fazendo exatamente o que a casa proíbe |

---

## 4. O que isto muda na guia de specs

**GRAU: MEDIDO** — contado sobre `docs/data/mapa-controles.csv` da árvore de
11/08/2026: 291 linhas, 97 chaves, 3 controles.

A guia é `specs.html`, e ela não se edita: é gerada do CSV por
`scripts/gerar-mapa.py`, com `--check` no CI (`.github/workflows/ci.yml:139`) e
no `.pre-commit-config.yaml:106`. **Mudar a guia é mudar células do CSV e rodar
o gerador** — qualquer outra coisa reprova no portão.

**As onze células do DualSense que saem de dedução para fonte.** Nenhuma precisa
do controle na mão.

| chave | o que a célula diz hoje | o que a fonte nova responde |
|---|---|---|
| `identidade.firmware@dualsense` | `existe = desconhecido`, confiança `afirmado-no-doc` | o driver **expõe** `firmware_version` e `hardware_version` em `/sys`, do feature `0x20` lido uma vez na probe, e os quatro valores foram lidos nesta máquina. `existe = tem` para **ler** |
| `luz.led_jogador.pisca@dualsense` | `existe = desconhecido`, sem confiança | `ps_led_info` tem `blink_set` (`hid-playstation.c:132`) e o `player_leds_info` do DualSense passa **`NULL`** nos cinco (`:1858-1869`). O DualShock4 usa; o DualSense não. `existe = nao-tem` |
| `plataforma.link_parametros@dualsense` | `existe = desconhecido`, sem confiança | três parâmetros de módulo, `0644`, lidos **na probe**: `feature_retries` (padrão 0), `ds4_short_pairing_info`, `ds4_synthetic_mac`. Os dois últimos não tocam o DualSense |
| `plataforma.probe.retry@dualsense` | `inferido-do-codigo` | é a **única** coisa que o fork muda no caminho do DualSense: quantas vezes um feature report é tentado |
| `luz.led_jogador.padrao_driver@dualsense` | *"QUAL padrão o driver acende não está escrito em lugar nenhum do repositório"* | está: `player_ids[5]`, enviado uma vez em `:2000`, pela ordem de registro num IDA global do módulo — que conta **qualquer** dispositivo PlayStation, inclusive o gamepad virtual desta casa |
| `luz.led_jogador.leitura@dualsense` | `inferido-do-codigo`; *"por HID, ninguém respondeu"* | confirmado por fonte: `dualsense_player_led_get_brightness` (`:1348-1354`) devolve um `u8` em RAM |
| `luz.lightbar.brilho@dualsense` | `inferido-do-codigo` | pela rota sysfs os player LEDs são **binários**: `max_brightness = 1`, e o bit que autoriza `led_brightness` (`flag2` bit0) **não existe no driver** |
| `plataforma.taxa_relatorios@dualsense` | repete *"~765 Hz no Bluetooth"* como fato do aparelho | cabo 250,0 Hz por duas réguas; rádio em rajadas |
| `movimento.giroscopio.taxa@dualsense` | *"a TAXA nunca foi medida"* | a taxa do **aparelho** está medida nos dois transportes. O que continua não medido é o que o **SDL declara ao jogo** |
| `movimento.imu.calibracao@dualsense` | `inferido-do-codigo` | feature `0x05`, 41 bytes, lido uma vez na probe |
| `plataforma.crc32@dualsense` | `inferido-do-codigo` | `ps_check_crc32`, por fonte |

**E sete células dos externos que a medição de 11/08 responde ou derruba:**

| chave | hoje | passa a ser |
|---|---|---|
| `plataforma.taxa_relatorios@sn30` | `existe = nao-tem` | **falso**: 200,5 amostras/s medidas, duas réguas |
| `plataforma.probe@sn30` | ressalva *"nesta máquina, AGORA, `hid_nintendo` não está carregado"* | está: os onze parâmetros vivos foram lidos em `/sys/module/hid_nintendo/parameters/` |
| `entrada.stick.calibracao@sn30` | `desconhecido` | respondido: `using factory cal for left/right stick` no boot atual |
| `movimento.imu.calibracao@sn30` | `desconhecido`, grau `afirmado-no-doc` | respondido pelo log do boot atual |
| `luz.led_home@sn30` e `luz.led_jogador.quinto@sn30` | `desconhecido` | **o nó existe**, `max_brightness=15` — medido. **A lâmpada continua SEM PROVA**, e é a P-4 dela |
| `identidade.firmware@sn30` | *"fora do repositório"* | há caminho Linux de **leitura**: o `fwupd` está instalado e já reconhece os PIDs |
| `identidade.firmware@pro` | `desconhecido` | o mecanismo está respondido: a versão **chega ao kernel e é jogada fora** — `joycon_read_info` lê `data[4..9]` e `data[2]`, e nunca os offsets 0 e 1 |

**Uma pergunta que só ela responde antes de A-4 rodar:** a régua de `provado_por`
que ela fixou hoje tem três valores — `teste`, `aparelho`, `descritor` — e
**leitura de fonte de driver não é nenhum dos três**. Está na seção 8.

---

## 5. As sprints

Cinco famílias. Nenhuma existe sem um defeito datado que a justifique, e cada
uma diz **como se prova que funcionou**. Os rótulos são os de
[RÓTULOS-DE-SPRINT-01](2026-08-09-ROTULOS-DE-SPRINT-01-entregue-no-codigo-nao-e-validado-por-ela.md);
nenhum rótulo novo foi inventado. Todas nascem `ABERTA`.

### Família A — substituição de fato errado

**GRAU: MEDIDO.** Cada uma tem `caminho:linha` na seção 3. **Estas sprints
apagam texto**, e é para isso que existem.

| sprint | o defeito | o que entrega | custo | como se prova |
|---|---|---|---|---|
| **A-0 `SIMPLIFICA-01`** | a regra da seção 1 não existe escrita: hoje o repositório aplica *"não se apaga"* a fato errado, e as páginas crescem | a regra e o teste que separa os dois casos entram no `CLAUDE.md` da raiz, na seção *"As regras desta casa"* | 1 h | o `CLAUDE.md` traz as duas regras juntas, e a próxima leva as cita |
| **A-1 `CANÔNICA-P4-01`** | P-1, P-2 | o `x-xx-` sai dos três lugares; entra `xx-xx` com a citação do fonte; a pergunta 3 sai da fila e vira ressalva sobre o console | 2 h | `grep -c 'x-xx-'` na canônica devolve **1**, e a ocorrência que sobra é a do `_PLAYER_LED_OVERFLOW` |
| **A-2 `CANÔNICA-TAXA-01`** | P-3, P-4, P-9, P-10, P-11 | os números do cabo e do rádio entram com a régua declarada; o *"limite honesto"* sai; o par transporte-número da paridade é desfeito; `GYRO-EDGE-RATE-01` deixa de ser chamado de sprint na quarta página | 4 h | as páginas não contêm mais *"nunca medido em transporte nenhum"*; e `grep -rn 'sprint .GYRO-EDGE-RATE' docs/` devolve zero |
| **A-3 `ADR-008-VERDADE-01`** | P-7, P-8 | os dois números do Contexto trocados; a frase da fixture na Decisão trocada pelo estado real; a nota de `:35-52` **fica** | 2 h | o ADR não afirma mais que os dois replays existem; `pytest tests/unit/test_paridade_transporte_envelope.py` verde |
| **A-4 `RÉGUA-DE-FONTE-01`** | P-5, P-6 | as quatro URLs `blob/master` ganham tag; as três afirmações sobre o *"kernel 6.18"* passam a dizer contra que fonte foram feitas, e `:647` perde o grau ALTA emprestado | 2 h | nenhuma página de `docs/protocol/` cita `blob/master` sem tag |
| **A-5 `MODO-QUE-TEM-NOME-01`** | X-3, X-4 — 17 ocorrências em `docs/`, 9 em `src/` e `assets/`, e uma no cabeçalho de um patch que vai ao upstream | o modo `Start + A` passa a se chamar pelo nome do fabricante em toda a árvore; o D-input verdadeiro ganha linha própria | 4 h | `grep -rn 'DirectInput/PS4' .` devolve só ocorrências que **explicam** a troca de nome |
| **A-6 `EXTERNOS-NA-MESA-01`** | X-1, X-5, X-6, X-7, X-8, X-9 | a §5 da canônica passa a dizer o que o cabo respondeu; a P-2 sai da fila (foi respondida em 25/07); o `EXPERIMENTO` do X-input vira medido; o `README.md` do DKMS para de dizer que o patch nunca carregou; o aviso do sysfs desce para a §3.6 | 5 h | a §5 não afirma mais *"nada foi medido naquele modo"* sem qualificar transporte; e a fila de perguntas abertas encolhe em uma |
| **A-7 `CLONE-SEM-GENERALIZAÇÃO-01`** | X-2 | o `PROVADO` sai da linha 190; a frase passa a dizer em que escopo vale | 1 h | a linha não contém mais `PROVADO`, e contém a ressalva |
| **A-8 `A-PÁGINA-QUE-ELA-LÊ-01`** | U-1 a U-7, U-9, U-10 — **a mais cara da leva** | as sete páginas de `docs/usage/` passam a descrever o produto de hoje; `versoes-validadas.md` ganha entrada a partir do `README.md` e de `instalacao.md` | 6 h | um teste que reprove se `jogos-e-mascaras.md` voltar a dizer que o virtual sai de cena; e `python3 scripts/validar-referencias-docs.py --all` limpo |
| **A-9 `NOME-QUE-NÃO-EXISTE-01`** | S-5, S-6, P-11 — três nomes citados como documento (`GUERRA-01`, `NINTENDO-VARIANT-01`, `GYRO-EDGE-RATE-01`) em 23, 3 e 5 arquivos | cada nome ou vira arquivo, ou a citação passa a dizer que é **nome de divergência**, não documento | 3 h | um portão que reprove citação de sprint ou estudo inexistente — é o irmão da regra 4 proposta na [RÓTULOS-DE-SPRINT-01](2026-08-09-ROTULOS-DE-SPRINT-01-entregue-no-codigo-nao-e-validado-por-ela.md), seção 5 |
| **A-10 `A-LEVA-QUE-SE-CRUZOU-01`** | N-1 a N-12 | as citações de `install.sh` reancoradas na árvore; as três seções que caducaram no mesmo dia corrigidas; os três números errados; as cinco imprecisões internas dos documentos novos | 4 h | um script que confira, para cada `install.sh:N` citado em `docs/`, que a linha N contém o que o texto diz — e ele fica no CI |
| **A-11 `MAPA-FONTE-DE-DRIVER-01`** | I-6, I-7, P-12 e a seção 4 inteira | as onze células do DualSense e as sete dos externos preenchidas, com `cabo_codigo_ref` apontando `assets/dkms/*/*.c:LINHA`; `specs.html` regerado | 8 h | `python3 scripts/gerar-mapa.py --check` passa; `python3 scripts/check_paridade_transporte.py` não piora; o censo de células sem resposta cai em dezoito, contado antes e depois |

**Preço honesto da família A:** ela apaga texto, e uma dessas sprints vai apagar
a coisa errada mais cedo ou mais tarde. A rede é o `git`: nada some de verdade,
e **toda substituição entra em commit próprio, com a frase antiga no corpo da
mensagem**. Quem quiser o texto de ontem tem `git log -p`.

### Família B — nota datada de decisão medida

**GRAU: MEDIDO** para os defeitos; **DECISÃO DELA** para a régua que separa esta
família da A. **Estas sprints não apagam nada.**

| sprint | a decisão que se preserva | o que entrega | custo | como se prova |
|---|---|---|---|---|
| **B-1 `TETO-DE-EMISSÃO-01`** | P-12 — o teto de 250 Hz no espelho de motion foi posto por medição (sem ele, quatro vpads em co-op seriam milhares de escritas por segundo em `/dev/uhid`). Quem só ler *"o rádio é mais lento que 250 Hz"* vai **remover o teto** | o número errado é substituído; e ganha nota datada dizendo **por que o teto continua**: o pico dentro da rajada é ~797 Hz | 2 h | um teste que reprove se `MOTION_EMIT_MAX_HZ` sumir ou subir; e o comentário citando a medição com a régua |
| **B-2 `PARIDADE-RÉGUA-01`** | P-9 — a medição de `~300 Hz` por contagem de bytes é de outra data e outra régua, e foi ela que primeiro mostrou que o rádio não é 1000 Hz | o número é atualizado; a **régua antiga** ganha nota datada, porque é reutilizável e barata | 1 h | a página cita as duas réguas e diz qual mediu o quê |
| **B-3 `ESCOPO-DO-CLONE-01`** | X-2 — a observação de 25/07 foi real; o que caiu foi a generalização | nota datada registrando as duas datas e os dois modos | 1 h | a nota existe |
| **B-4 `BLUEZ-DUAS-MEDIÇÕES-01`** | U-8 — **as duas são MEDIDO e apontam para lados opostos.** Apagar qualquer uma faz alguém refazer a medição para descobrir o que já se sabe | nota datada nas duas páginas dizendo que amostras de cinco dias não decidem tendência, e por que o piso do `doctor` continua em 5.79 assim mesmo | 2 h | as duas páginas se citam, e o `doctor` não muda |
| **B-5 `MEDIÇÃO-DO-8BITDO-01`** | X-1 — *"qualquer medição daquele modo começa por um pareamento novo"* é o item mais caro daquela página, e continua verdade **para o rádio** | nota datada separando o que o cabo respondeu do que o rádio ainda deve | 1 h | a §5 distingue os dois transportes em toda afirmação |

**Em dúvida, e por isso aqui e não na A:** B-2 e B-3. Nos dois, a informação
antiga é medição com régua declarada, e apagá-la faria alguém refazer trabalho.
Se, ao executar, ficar claro que ninguém repetiria nada, elas migram para a
família A — e a migração se registra.

### Família C — correção de instrumento

**GRAU: MEDIDO.** O defeito de fundo é o mesmo dos quatro: **o instrumento
afirma mais do que mediu.**

| sprint | o defeito | o que entrega | custo | como se prova |
|---|---|---|---|---|
| **C-1 `LED-QUE-NÃO-AFIRMA-01`** | I-1 | o veredito passa a dizer que conferiu **permissão**. O que a luz faz continua sendo do olho dela | 3 h | teste que reprove se o texto do `pass` voltar a afirmar efeito |
| **C-2 `SYSFS-NÃO-É-PROVA-01`** | I-2 e a mesma família em todo lugar que lê sysfs como prova. O arquivo **já tem o hábito certo** em outro assunto: `scripts/doctor.sh:1957-1964` avisa que a policy de ASPM mente e não deve ser usada como prova | varredura de `scripts/` e `src/`; cada ocorrência ou ganha a ressalva, ou vira leitura de intenção declarada | 3 h | inventário no corpo da sprint, com `caminho:linha` e veredito de cada uma |
| **C-3 `DOCTOR-NA-MESA-VAZIA-01`** | o `doctor` dá **quase verde** numa máquina sem applet — `check_applet` (`scripts/doctor.sh:670`) e `check_service` (`:132`) dão `warn`, não `fail`. Verde de mesa vazia é indistinguível de verde de tudo funcionando | o resumo final conta **o que não pôde ser medido**, e por quê | 2 h | rodar o `doctor` sem controle na mesa e ver a contagem no resumo |
| **C-4 `MARCA-QUE-NINGUÉM-LÊ-01`** | I-5 — a marca `HEFESTO_CONTROLLER_VARIANT` é escrita, instalada, conferida e anunciada, e **nenhuma linha de `src/` a lê** | o leitor, a partir do nó `hidraw` (o `hid_instance_for_hidraw` de `core/external_leds.py` já resolve o caminho), com o desempate de `friendly_type()` corrigido junto; e o `doctor` passa a conferir **efeito**, não presença de arquivo | 6 h | um teste que reprove se a marca voltar a não ter leitor; e o `doctor` distinguindo os dois `057E:2009` |

**C-1, C-2 e C-3 já estão previstas como ETAPAS 2.1, 2.2 e 2.3** do
[plano de máquina nova](../2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md),
com os mesmos custos. **Não são sprints novas: são as mesmas, indexadas aqui
pela contradição que as gerou.** Este índice não abre frente paralela; ele diz
**por que** aquelas etapas existem. A C-4 é a única da família que o plano não
tem, e ela é antiga: nasceu no [estudo de
07/08](../estudos/2026-08-07-O-QUE-EXISTE-E-NAO-CHEGA-a-cobertura-do-install.md),
item 8.

### Família D — correção de código

**GRAU: MEDIDO** para D-1 a D-3; **SUSPEITA COM MECANISMO** para D-4.

A resposta curta à pergunta *"onde o código está errado?"* mudou durante a
apuração. Nas contradições de **protocolo**, o código estava certo — o P4 e a
escolha do overflow. Nas de **externos**, não: há um defeito medido que acende a
lâmpada errada.

| sprint | o defeito | o que entrega | custo | como se prova |
|---|---|---|---|---|
| **D-1 `COMENTÁRIO-QUE-MEDE-01`** | P-12 — dez comentários em três módulos afirmam `~765 Hz` como taxa sustentada. Comentário errado em código é pior que em documento: é o que a próxima pessoa lê antes de mexer | os dez trechos passam a dizer rajada e pico, com a data; nenhuma constante muda | 2 h | `grep -rn '765' src/` devolve só ocorrências qualificadas; suíte verde |
| **D-2 `A-QUINTA-LÂMPADA-01`** | I-3 — `write_player_number` usa o `:blue:player-5` como **bit "+5" da numeração**, e ele é o **LED HOME**: outro subcomando, escala 0-15, e a escrita manda `1` (1/15 de brilho). E o ramo *"hardware sem o nó azul"* **nunca dispara**: o clone tem o nó | a numeração de 5 a 9 ganha outro desenho, porque **só existem quatro lâmpadas de jogador**; o ramo morto sai ou vira lápide | 6 h | um teste que reprove se o Home voltar a ser usado como bit de numeração; e a foto dela do controle no slot 6 |
| **D-3 `UNIQ-QUE-NÃO-VEM-VAZIO-01`** | I-4 — três comentários afirmam que o `uniq` vem vazio por cabo, e por cabo ele vem **preenchido** (Nintendo) ou **fabricado** começando em `02:` (o `ds4_synthetic_mac` do nosso DKMS, que faz um 8BitDo virar "Sony") | os comentários corrigidos e o `brand_of` ciente dos dois casos | 3 h | um teste que morda os dois caminhos de cabo, com o `uniq` real e o sintético |
| **D-4 `ESPELHO-QUE-CHEGA-01`** | S-1, S-2 | a cura, **só se a medição pedir** | ver E-4 | **não se prova por leitura** |

**D-4 não entra sem E-4.** Escrever cura para um caminho não medido é
exatamente a cura escrita e nunca ligada, que o `CLAUDE.md` da raiz registra
como o defeito mais caro desta casa.

### Família E — medição que falta

**GRAU: SEM PROVA**, por definição: é o que só o aparelho, a Steam aberta ou uma
máquina limpa respondem.

| sprint | a pergunta | o ensaio, com a régua | custo | o que ela decide |
|---|---|---|---|---|
| **E-1 `TAXA-SOB-MOVIMENTO-01`** | o colapso do rádio de ~334 para ~55 Hz entre duas janelas de 8 s é economia de energia do enlace com o controle parado? | repetir as cinco janelas com o controle em movimento contínuo, mesma régua, **variável única** | 10 min | se a hipótese de `sniff` fica de pé. Hoje é **GRAU BAIXA**, e está dita como tal |
| **E-2 `TAXA-QUE-O-JOGO-VÊ-01`** | o que o SDL **declara** ao jogo para o vpad Edge: 250 ou 1000 Hz? | medir contra a **SDL3 que a Steam distribui** — nunca contra a `libSDL2` do sistema, que já produziu um alarme falso inteiro nesta casa | 2 h | fecha a última metade da pergunta 4 da §8 da canônica. A metade do **aparelho** já está fechada por A-2 |
| **E-3 `ESPELHO-DA-STEAM-01`** | a Steam põe `SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD=1` no ambiente do jogo? | com a Steam **aberta** e um jogo na frente: `tr '\0' '\n' < /proc/<pid>/environ \| grep -i SDL_`. **Trinta segundos**, e o mesmo comando responde outras duas perguntas | 30 s dela | destrava ou arquiva D-4. É a única linha desta leva que pode virar defeito de partida — e, se a resposta for 1, o produto **não tem como sobrescrever**, porque a variável está fora da `ENV_ALLOWLIST` |
| **E-4 `BITS-DE-AUTORIZAÇÃO-01`** | de quantos bits de autorização o firmware do DualSense precisa para o rumble? São quatro na mesa; o SDL entrega dois, o kernel entrega dois, e **os conjuntos são diferentes** | bancada, um bit por vez | 2 h | é a porta mais promissora do defeito de rumble, que continua **sem causa provada** depois de seis suspeitos caírem |
| **E-5 `P4-NO-PLÁSTICO-01`** | o console PS5 desenha o P4 como o Linux manda? | numerar quatro controles e **olhar** | 5 min dela | nada do produto depende disso; está aqui para a ressalva de A-1 não virar pergunta esquecida |
| **E-6 `A-LÂMPADA-DO-CLONE-01`** | o anel de Home do 8BitDo **acende**? O nó existe, com `max_brightness=15`; a lâmpada é pergunta de olho | cinco segundos de olho dela | 5 min dela | é a P-4 da canônica dos externos, e ela decide metade da D-2 |
| **E-7 `8BITDO-NO-RÁDIO-01`** | o clone em modo Switch **pelo rádio** — o que a probe faz? | pareamento novo em modo Switch e leitura | uma sessão dela | é o que separa *"o cabo respondeu"* de *"o aparelho respondeu"*, e a canônica precisa disso para fechar a §5 |
| **E-8 `INSTALL-EM-MÁQUINA-VIRGEM-01`** | o `install.sh` faz numa máquina limpa o que a leitura do código diz que faz? | o ciclo real, com os pareamentos copiados para fora antes | ver ETAPA 5 do plano | é **o limite mais importante** que o delta declara sobre si mesmo: *"ler não é provar"*. Nada foi executado — nem `install.sh`, nem `uninstall.sh`, nem `doctor.sh` |

---

## 6. A ordem, por DEPENDÊNCIA

Não é ordem de importância. É a ordem em que uma coisa **não pode** ser feita
antes da outra.

```
  A-0  a regra escrita
   |     (sem ela, quem executar a família A não sabe o que pode apagar)
   |
   +--> A-1  P4              --+
   +--> A-3  ADR-008           |
   +--> A-4  a régua de fonte  |
   +--> A-5  o nome do modo    +--> A-11  o mapa e a guia de specs
   +--> A-6  os externos       |      (as células vão CITAR as páginas)
   +--> A-7  o clone           |
   +--> A-9  os nomes fantasma |
   |                           |
   +--> A-2  as taxas       ---+
   |      |
   |      +--> B-1  o teto de emissão --> D-1  os comentários
   |      +--> B-2
   |
   +--> A-10  a leva que se cruzou
          |     (reancora as citações; A-8 depende dela para não citar linha velha)
          |
          +--> A-8  as páginas que ela lê   --> B-4  as duas medições de BlueZ

  B-3 e B-5 andam junto com A-7 e A-6, no mesmo commit

  C-1 --> C-2 --> C-3        (a ETAPA 2 do plano, em paralelo)
  C-4                        depende de A-5 (o nome do modo entra no leitor)

  E-3 --> D-4                (a cura só depois da medição)
  E-6 --> D-2                (o desenho da numeração depende de a lâmpada acender)
  E-1, E-2, E-4, E-5, E-7    independentes, a qualquer momento
  E-8                        depende da ETAPA 1 do plano, não deste índice
```

**As seis travas, uma linha cada:**

1. **A-0 antes de toda a família A.** Quem apaga texto sem a regra escrita apaga
   a coisa errada, e essa é a única perda irreversível deste roteiro.
2. **A-1 a A-9 antes de A-11.** As células do mapa vão **citar** as páginas;
   citar página que ainda mente é multiplicar o erro em três controles.
3. **A-10 antes de A-8.** Reancorar as citações de `install.sh` primeiro; senão a
   página que a usuária lê nasce apontando para a linha errada.
4. **B-1 depois de A-2, nunca antes.** A nota do teto explica por que o teto
   fica; escrevê-la antes do número certo produz nota que defende número que vai
   mudar.
5. **E-3 antes de D-4, e E-6 antes de D-2.** Sem medição não há cura — há
   palpite com endereço de memória.
6. **C-4 depois de A-5.** O leitor da marca vai escrever nome de modo na tela; se
   o nome ainda estiver errado, ele nasce errado.

**O que corre em paralelo sem travar nada:** a família C (é a ETAPA 2 do plano) e
as sete medições independentes da família E.

---

## 7. O que NÃO entra, e por quê

| o que fica de fora | por quê |
|---|---|
| **reescrever a canônica do DualSense do zero** | ela tem oito notas datadas de 11/08 que **são** decisão medida, e a família A só toca as linhas da seção 3. Reescrever é apagar o que a seção 1 manda guardar |
| **transformar o índice de "o que caducou" da canônica em página própria** | a `§0` daquela página é o atalho que funciona. Mover cria mais um lugar para procurar, que é o oposto do que ela pediu |
| **o IMU do Pro** | não é contradição: **já estava refutado** desde 07/08, com o número certo já propagado a três páginas vizinhas. Corrigir o que já está certo produz risco e zero valor |
| **marcar a TRES-CONTROLES-01 como errada** | ela está **sob suspeita**, não refutada. Trinta segundos de medição decidem (E-3); declarar antes é o vício que a casa proíbe |
| **a fixture `hid_capture_bt.bin`** | só nasce de gravação num DualSense real por Bluetooth. Forjar bytes sintéticos daria um replay que passa e não representa o transporte |
| **as linhas de combinação do mapa** | trabalho de bancada com hardware, e o plano de máquina nova já as excluiu desta versão pelo mesmo motivo |
| **desligar o `continue-on-error` do censo de paridade no CI** | é a ETAPA 6.1 do plano, e depende de as células sem mordida ganharem teste **ou** baixarem a confiança. Antecipar trava o CI por uma dívida que este índice não paga |
| **mexer no `MOTION_EMIT_MAX_HZ`** | o número que o justifica estava errado; **a decisão de capar, não**. Ver B-1 |
| **mexer no PID `0x0DF2`** | a escolha continua certa, e agora se sabe o preço: quatro botões fantasmas, outro nome, outro caminho de rumble e uma taxa declarada 4x maior. Preço medido não é motivo para trocar — é motivo para escrever |
| **propor de novo o que já está no disco** | o voo de reconhecimento do `install.sh`, o bloco de `dkms`/headers, o teto de versão do BlueZ, a receita do backport na árvore, a régua de `provado_por` e os dois testes novos entraram em 11/08. Repropor é o desperdício que este índice existe para evitar |
| **`1.0.0`** | decisão já registrada no plano: `ENTREGUE EM CÓDIGO` não é `VALIDADO POR ELA`. O `1.0.0` é o número que se põe **depois** de o PC novo passar |

---

## 8. O que continua sendo dela

**GRAU: DECISÃO DELA.** Nenhuma se responde por quem executa.

| # | a pergunta, pronta |
|---|---|
| 1 | *"Leitura do fonte do driver é `provado_por` o quê? A régua que você fixou hoje tem três valores — `teste`, `aparelho`, `descritor` — e ler o C que compilou o módulo não é nenhum dos três. Crio um quarto (`fonte`), ou as dezoito células ficam com a confiança que já têm e só ganham a citação?"* |
| 2 | *"A família A apaga texto. É a sua regra de hoje, e eu quero confirmar o alcance: vale para as páginas de protocolo, os ADR e as páginas de uso — ou também para as sprints antigas, que são registro do que se pensava naquele dia?"* |
| 3 | *"O nome do modo do 8BitDo está errado em 26 lugares, e um deles é o cabeçalho de um patch que vai para o kernel. Corrijo o patch junto, ou o upstream é leva separada?"* |
| 4 | *"O 8BitDo respondeu tudo pelo cabo. Pelo rádio, cada medição começa por um pareamento novo, e é o item mais caro daquela página. Vale a sessão, ou o cabo basta para o que você usa?"* |

---

## 9. A conta

**GRAU: ESTIMATIVA**, em horas de bancada. O que depende dela ou de hardware
está em minutos e sessões dela, e não se soma ao resto.

| família | sprints | custo |
|---|---:|---:|
| A — substituição | 12 | ~42 h |
| B — nota datada | 5 | ~7 h |
| C — instrumento | 4 | ~14 h (três delas são as ETAPAS 2.1 a 2.3 do plano, não trabalho novo) |
| D — código | 4 | ~11 h + o que E-3 decidir |
| E — medição | 8 | ~4 h de bancada; 40 min dela nas quatro mais baratas; duas sessões nas duas mais caras |

**O caminho mínimo, se o tempo for curto** — cerca de **13 h**, mais **30
segundos dela**:

| item | por quê |
|---|---|
| **A-0** | sem a regra escrita, nada da família A pode ser executado com segurança |
| **A-8** | é a página que **ela** lê, e ela afirma há dois dias um comportamento que o produto não tem mais. É a contradição mais barata de consertar e a mais cara de deixar |
| **A-1, A-2, A-3** | matam as duas verdades nas três páginas mais citadas do repositório |
| **C-1** | tira do `doctor` a única afirmação que ele faz além do que mede |
| **E-3** | trinta segundos que destravam ou arquivam a D-4, e respondem outras duas perguntas de graça |

Tudo o mais espera sem produzir dano novo.

**O que este roteiro não sabe:** se alguma das dezoito células da seção 4 tem
contra-exemplo no aparelho dela. Fonte de driver prova o que o Linux manda — não
o que o firmware faz com aquilo. Onde essa diferença importa, a linha está na
família E, e em nenhuma outra.
