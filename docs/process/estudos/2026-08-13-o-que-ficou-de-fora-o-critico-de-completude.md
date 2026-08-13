# O que ficou de fora — o crítico de completude do estudo de 13/08/2026

> **Como esta página nasceu.** Agente independente, rodado **depois** da síntese, na
> madrugada de **13/08/2026**, contra a mesma árvore: **`cc768d4`**, tag **`v0.9.4.2`**,
> branch `restauro/inicio-da-sessao`. Somente leitura, como a rodada inteira. **A tarefa
> dele não era elogiar: era achar buraco** — e ele é a metade que reprova de uma rodada
> de doze agentes cuja outra metade está em
> [o projeto inteiro num mapa só](2026-08-13-o-projeto-inteiro-num-mapa-so.md).
>
> **Ele derrubou três afirmações daquele estudo, e as três já estão corrigidas lá.**
> Isso não apaga o registro: decisão medida ganha nota datada, e as notas estão no
> cabeçalho e no corpo daquela página. As três: a contagem de `observado_por` no caderno
> de ensaios, a força da frase sobre o `diff -rq` do DKMS, e a régua não publicada das
> funções `test*`.
>
> **Como ler os graus.** Iguais aos do estudo irmão: **medido** (saiu de um comando
> rodado nesta árvore, nesta data), **lido-no-código** (o caminho foi lido no fonte e
> fecha, o efeito não foi observado), **inferido** (dedução de duas leituras, sem
> execução que confirme). Boa parte desta página é *medido*, porque a tarefa dele era
> exatamente refazer as contas.
>
> **O que o transporte para o repositório corrigiu, em 13/08**, conferindo os
> `caminho:linha` um a um:
>
> - O passo "Auditar arquivos de instrucao IA no tree" está em
>   `.github/workflows/anonymity-check.yml:142-171`, não em `:141-169`.
> - A referência ao delta da máquina limpa ganhou o caminho completo e a linha certa
>   (`:76-79`).
> - **"106 estudos" não confere: são 33** (`find docs/process/estudos -name '*.md'`,
>   13/08). Os outros números da mesma frase conferem — 174 sprints, 58 agentes, 10
>   audits, 19 ADRs, 17 arquivos de `docs/usage/`, 6 de `docs/research/`, 64 scripts.
> - **O estudo de 20/07 sobre a injeção de fd, que ele cita como auditoria anterior do
>   broker, NÃO existe nesta árvore.** As duas units apontam para ele
>   (`assets/systemd/hefesto-hidraw-broker.socket:14` e
>   `assets/systemd/hefesto-hidraw-broker.service:21`) e o arquivo não está aqui. O
>   achado dele sobrevive e fica maior: não é só que ninguém releu a auditoria do único
>   serviço root — é que ela não está no repositório.

---

## Veredicto

**O documento é honesto e quase todo confere — o que falta nele é escopo, não veracidade.**
Amostrei 14 afirmações com número ou `caminho:linha` e conferi cada uma contra a árvore em
`cc768d4`: **11 conferem exatamente, 2 não conferem como escritas, 1 não consegui
reproduzir.** Para um estudo com centenas de números, essa taxa é alta, e vale dizer isso
antes de bater.

**As três que caem:**

1. **§1 — "77 ensaios de bancada com o olho dela".** São 73. A coluna `observado_por` de
   `docs/data/ensaios.csv` traz 4 marcados `bancada` (instrumento: btmon por timestamps,
   ACL do udev, permissão do hidraw). Numa casa cuja regra 12 é *"controle negativo não é
   prova de obediência"* e cujo caderno inteiro existe para separar quem observou o quê,
   atribuir quatro observações de instrumento ao olho dela é o erro que o caderno foi
   feito para impedir. Conferi que os dois ensaios de btmon de que C-2 depende estão
   corretamente marcados `olho-dela` — a nota deles traz a fala literal dela e o btmon só
   contou o suspeito. O caderno está certo; a frase de abertura do estudo é que
   arredondou. *Medido* (reconferido no transporte: 73 `olho-dela`, 4 `bancada`, sobre 77
   linhas).

2. **D-7 — "`diff -rq` contra `/usr/src/` não acusa um arquivo".** Rodei agora, somente
   leitura: **acusa** — `LICENSES/` só em `/usr/src`, `patch/` só em `assets/`, nos três
   módulos. Nenhum arquivo de conteúdo difere (0 nos três), então a conclusão sobrevive;
   a frase, não. E o documento-fonte de 11/08
   (`docs/process/2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md:76-79`)
   nomeia essas duas assimetrias como esperadas. O estudo comprimiu a fonte e publicou uma
   afirmação mais forte que ela. *Medido* (refeito no transporte, nos três módulos:
   `hid-playstation`, `hid-nintendo`, `rtw88-usb` — duas linhas cada, exatamente essas).

3. **§4.7 — "7775 funções `test*`", declarado *Medido*.** Minha régua devolve 7800. Não é
   refutação, é régua diferente — e é exatamente a doença que o próprio documento
   diagnostica na armadilha 5 ("só o número que sai de um script sobrevive"). O script não
   foi publicado.

**O que dentro dele não se sustenta como raciocínio (mais grave que os números):**

- **A decisão sobre o arquivo de instruções da raiz oferece a ela uma opção que já está
  proibida.** O estudo propõe "ou versiona o arquivo, ou move a lista de portões".
  Versionar reprova: `.github/workflows/anonymity-check.yml:142-171` tem um passo que
  falha o build se aquele arquivo estiver rastreado, e `.gitignore:89-104` o coloca num
  bloco rotulado `# --- anti-IA (anonimato local) ---`. E o mesmo estudo propõe, três
  itens depois, ligar esse workflow em `restauro/**`. As duas propostas juntas produzem CI
  vermelho.
- **A saída proposta para a mentira da aba Rumble já existe escrita, 1400 linhas ao lado.**
  O estudo oferece "mecanismo novo no backend, ou uma linha de texto nova". A linha de
  texto já está no produto: `app/actions/status_actions.py:1859` traz
  `"Editando: {alvo} — sem endereço fixo, vale para todos"`. Ela só não aparece porque
  `_update_edit_badge` (`:1955-1962`) a condiciona a `bool(self._edit_target_uniq)` — ou
  seja, à identidade do CONTROLE, não à capacidade da FEATURE. Como o rumble nunca honra o
  MAC, um controle COM MAC recebe o selo curto e mentiroso. O conserto de 5 minutos não é
  escrever uma frase; é passar `com_endereco=False` quando a aba ativa for a Rumble. Isso é
  o léxico existente, que é como ela pede que se proponha interface.
- **B-5 para na metade.** O `continue-on-error: true` do censo do mapa engole as SEIS regras
  duras do script, não só a de sem-mordida — `main` tem um exit code só
  (`scripts/check_paridade_transporte.py:1093`). O comentário do CI
  (`.github/workflows/ci.yml:150-154`) justifica manter o passo dizendo que "as outras
  regras dele já estão verdes — e é justamente por elas que o passo precisa estar aqui
  hoje": a razão escrita é a única coisa que o passo não entrega.

**O buraco de escopo maior:** o §2 se chama "O mapa dos subsistemas" e tem oito entradas,
sem dizer em lugar nenhum quantos ficaram fora. Ficaram fora, com zero menções:
`tests/conftest.py` (1463 linhas, com um `autouse=True` que liga o modo FAKE em toda a
suíte), `app/widgets/controller_card.py` (4630 linhas — o **maior arquivo de `src/`**), a
camada de entrada inteira (`core/evdev_reader.py` 1929, `integrations/window_detect.py`,
`integrations/xlib_window.py`, `integrations/window_backends/`,
`daemon/subsystems/autoswitch.py`), metade de `daemon/subsystems/`, quase toda a
`integrations/`, 174 sprints, 33 estudos, 17 das 19 ADRs, e 16 dos 17 arquivos de
`docs/usage/`. Detalhe que fecha o argumento: **as fotos que a documentação publica são de
11/08 23:06, e três commits tocaram `app/` e `gui/` antes da tag `v0.9.4.2` de 13/08** — a
regra da casa manda re-fotografar antes de gerar release, e nem o agente que estudou as
fotos perguntou de que versão elas eram.

---

## As afirmações amostradas

**11 de 14 conferem.** As que caem:

- **§1: "77 ensaios de bancada com o olho dela"**
  ACHADO. `docs/data/ensaios.csv`, coluna `observado_por`: 73 são `olho-dela` e 4 são
  `bancada` (btmon por timestamps, ACL do udev, permissão do hidraw). Numa casa onde a
  proveniência é o produto, atribuir quatro observações de instrumento ao olho dela é o
  erro que ela mesma pegou uma vez (armadilha 12). Confiro que os dois ensaios de que C-2
  depende — `btmon-probe-suja` e `btmon-probe-limpa`, em `docs/data/ensaios.csv:49-50` —
  estão corretamente marcados `olho-dela`: a nota traz a fala dela ("todos ligados e todos
  apagados" / "os 3 ligaram e os três azuis"), com o btmon fornecendo só a contagem do
  suspeito. O caderno está certo; o resumo do estudo é que arredondou.

- **D-7: "`diff -rq` contra `/usr/src/` não acusa um arquivo"**
  ACHADO, de dois lados. (a) Rodei agora, somente leitura, nos três módulos: o `diff -rq`
  ACUSA — `LICENSES/` só em `/usr/src`, `patch/` só em `assets/`. Nenhum arquivo de
  CONTEÚDO difere (0 nos três), então a conclusão sobrevive. (b) O documento-fonte,
  `docs/process/2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md:76-79`,
  é preciso e nomeia essas duas assimetrias como esperadas; o estudo comprimiu e perdeu a
  ressalva, publicando uma frase mais forte que a fonte.

- **§4.7: "7775 funções `test*`, 95 sem `assert`/`raises`/`fail` no próprio corpo".
  *Medido.***
  NÃO REPRODUZI. Minha régua crua — um `grep -rhoE` por definição de função `test` em
  `tests/` — devolve 7800, não 7775. Não é refutação, são réguas diferentes, mas o
  documento não publica a régua, e ele mesmo escreve na armadilha 5 que "só o número que
  sai de um script sobrevive". Um número declarado MEDIDO que outra pessoa não consegue
  repetir é a doença que o próprio parágrafo diagnostica.

---

## O que ficou de fora do estudo

- **`tests/conftest.py` — 1463 linhas, ZERO menções.** É por onde passam os 9130 nós, é
  onde mora o stub de `gi` que a armadilha nº 4 do próprio documento discute, e tem um
  fixture `autouse=True` (`tests/conftest.py:1109`) que liga o modo FAKE em toda a suíte.
  Ver "a pergunta que ninguém fez", adiante.

- **O maior arquivo de `src/` inteiro: `app/widgets/controller_card.py`, 4630 linhas —
  ZERO menções.** É o card do Status, a tela que ela mais olha. Maior que o
  `core/backend_pydualsense.py` (4230) e que o `daemon/lifecycle.py` (4171), os dois que
  ganharam parágrafo próprio no §2.

- **A camada de entrada e a detecção de janela — ZERO.** `core/evdev_reader.py` (1929),
  `integrations/window_detect.py`, `integrations/xlib_window.py`,
  `integrations/window_backends/`, `daemon/subsystems/autoswitch.py`,
  `profiles/autoswitch.py` (731), `daemon/sensor_hub.py`. O §1 vende "troca de perfil pela
  janela em foco" na segunda frase e nenhum agente abriu o código que faz isso. Está
  reconhecido, mas só como uma frase no item 15 de 15 da tabela de 6.1, custo "horas".

- **Metade de `daemon/subsystems/` e quase toda a `integrations/` — ZERO.** Mudos:
  `daemon/subsystems/hotkey.py`, `daemon/subsystems/game_signal.py`,
  `daemon/subsystems/metrics.py`, `daemon/subsystems/keyboard.py`,
  `daemon/subsystems/mouse.py`, `daemon/subsystems/poll.py`, `daemon/subsystems/bt_mic.py`;
  `daemon/launch_env.py` (1635), `daemon/connection.py` (956), `daemon/state_store.py`
  (732), `daemon/udp_server.py` (677); `integrations/steam_launch_options.py` (1506),
  `integrations/proton_pin.py` (1194), `integrations/dualsense_bt_audio.py` (1286),
  `integrations/storm_doctor.py`, `integrations/tray.py`, `integrations/uinput_gamepad.py`,
  `integrations/uinput_keyboard.py`, `integrations/uinput_mouse.py`. O
  `steam_launch_options` e o `proton_pin` são exatamente o que o §2 diz que o install
  entrega.

- **O corpo de `docs/` — 174 sprints, 33 estudos, 58 agentes, 10 audits: NENHUM caminho
  citado.** O documento cita IDs de sprint (BONDS-QUE-SOBREVIVEM-01, PROVA-DE-TELA-01…) mas
  uma varredura por `docs/process/sprints`, `docs/process/estudos` e `docs/process/agentes`
  devolve zero. Das 19 ADRs, duas são citadas (015 e 017). `docs/research/` (6 arquivos,
  incluindo `firmware-dualsense-2026-04-survey.md` com 33 KB e `firmware-update-protocol.md`)
  e `docs/history/` (6 no topo, mais a pasta `sprints-canceladas`): zero.

- **`docs/usage/` — 17 arquivos, 1 examinado.** O estudo achou deriva documento↔código duas
  vezes (A-4 no protocolo do IPC, A-5 no `docs/usage/interface.md`) e não procurou a mesma
  deriva onde há mais texto: `docs/usage/troubleshooting.md` (40 KB), `docs/usage/modos.md`
  (17 KB), `docs/usage/cli.md` (16 KB), `docs/usage/troubleshooting-8bitdo.md` (18 KB),
  `docs/usage/instalacao.md`, `docs/usage/flatpak.md`, `docs/usage/quickstart.md`,
  `docs/usage/hotkeys.md`.

- **As FOTOS PUBLICADAS NÃO ACOMPANHAM A TAG — e nem o agente que estudou as fotos viu.** A
  regra da casa manda: *"Antes de gerar release, rode de novo: as imagens acompanham a
  versão."* Medido: as fotos de `docs/usage/assets/` são de 11/08 23:06; DEPOIS disso três
  commits tocaram `app/` e `gui/` (`f1279a1`, `0b010bd`, `973c92c`), e a tag `v0.9.4.2` foi
  cortada em `cc768d4`, 13/08 02:26. F-1 e F-2 criticam o CONTEÚDO das fotos e não perguntam
  se elas são da versão publicada. Não são. *(Reconferido no transporte: os três commits, as
  datas e o mtime das fotos.)*

- **64 arquivos em `scripts/` — dois citados de passagem** (`scripts/doctor.sh`,
  `scripts/install-host-udev.sh`). Ficaram mudos justamente os do assunto de E-3
  (`scripts/bt_bonds_restore.sh`, `scripts/bt_bonds_snapshot.sh`,
  `scripts/bt_health_watchdog.sh`), os de empacotamento (`scripts/build_deb.sh`,
  `scripts/build_appimage.sh`, `scripts/build_flatpak.sh`), os de i18n, o
  `scripts/faxina-de-testes.py`, o `scripts/sanitizar_saida_de_agente.py` e o
  `scripts/record_hid_capture.py` — este último é o instrumento da fixture de Bluetooth que
  a tabela 6.2 diz estar devendo desde 31/07.

- **A TUI (489 linhas, ADR-002) e o `plugin_api/` (423 linhas, ADR-017).** E-6 declara que
  "os plugins são a única API pública que o projeto promete a terceiros" sem abrir o pacote
  que define essa API.

- **A superfície de ataque do broker root.** O §2 descreve o desenho (`SO_PEERCRED`,
  `SCM_RIGHTS`, o uid autorizado por env) e ninguém audita. Existe auditoria anterior citada
  nos comentários das próprias units — `assets/systemd/hefesto-hidraw-broker.socket:14` e
  `assets/systemd/hefesto-hidraw-broker.service:21` apontam para um estudo de 20/07 sobre o
  desenho da injeção de fd. **Ela não foi lida nesta rodada, e o transporte descobriu por
  quê: esse arquivo não existe nesta árvore.** As duas units apontam para um documento
  ausente. É o único serviço de sistema, como root, com `DeviceAllow=char-hidraw rw`.
  *Medido em 13/08.*

- **CONTRADIÇÃO INTERNA — a decisão sobre o arquivo de instruções da raiz colide com um
  portão que o próprio estudo cita.** O item de 6.2 diz: *"Ou versiona o arquivo, ou move a
  lista de portões para um arquivo versionado."* A opção A está proibida por escrito:
  `.gitignore:89-104` põe esse arquivo num bloco rotulado `# --- anti-IA (anonimato local) ---`
  ao lado dos equivalentes de outras ferramentas; e
  `.github/workflows/anonymity-check.yml:142-171` tem um passo *"Auditar arquivos de
  instrucao IA no tree"* que REPROVA o build se `git ls-files --error-unmatch` casar com
  qualquer um deles. Pior: três linhas abaixo o mesmo estudo propõe fazer o
  `anonymity-check.yml` disparar em `restauro/**`. As duas propostas juntas dão CI vermelho
  no primeiro push. Ela precisa ver isso ANTES de escolher.

- **B-5 para na metade.** O estudo diz "no CI ele não é portão, é relatório". O comentário
  logo acima (`.github/workflows/ci.yml:150-154`) declara a razão do `continue-on-error`:
  *"as outras regras dele já estão verdes — e é justamente por elas que o passo precisa
  estar aqui hoje."* Mas `scripts/check_paridade_transporte.py` tem UM exit code (`main`
  devolve 1 em `:1093` para qualquer regra dura), então o `continue-on-error` engole as seis
  regras duras igualmente. A razão escrita para manter o passo é exatamente a única coisa
  que o passo não faz. Isso é mais grave que "é relatório" e não foi dito.

---

## Graus declarados errados

- **D-7 é o pior caso: documento de 11/08 republicado sob grau próprio.** A linha de
  evidência é literalmente
  `docs/process/2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md` —
  nenhuma das medições (o `diff -rq`, o `apt-cache policy` do BlueZ, o `command -v cargo`)
  foi refeita hoje. São todas medições de ESTADO DE MÁQUINA, o tipo que caduca sem commit
  nenhum. O grau honesto é `lido-no-documento` (ou `medido em 11/08, não reconferido`).
  Provei que importa: refiz o `diff -rq` e ele acusa duas entradas que a frase publicada
  nega.

- **E-3 ("O restauro de bonds continua sem gatilho") vem marcado *Grau: medido* e é leitura
  de comentário.** A evidência é `install.sh:1707`, que li: é um comentário de bloco dizendo
  "restauração é MANUAL (`bt_bonds_restore.sh`; automática poderia restaurar chave que o
  controle rotacionou → loop de auth)". Ler um comentário é `lido-no-código`. Pior: o
  comentário não só declara o estado como declara a RAZÃO técnica da escolha — o que muda o
  achado de "dívida esquecida" para "decisão escrita que contradiz a decisão dela de 08/08",
  que é uma coisa diferente e mais interessante.

- **F-2 publica um til dentro de um grau medido:** "A janela tem ~12 estados de diálogo e 5
  fotografados. *Grau: medido.*" Ou os estados foram contados — e aí é 11, ou 12, ou 13 —,
  ou não foram, e aí o grau é `inferido`. A régua desta casa para esse assunto é "conte
  estados, não diálogos"; o til é a confissão de que ninguém contou.

- **B-3 chama de *medido* uma REIMPLEMENTAÇÃO do portão, não a execução dele.** A evidência
  é "reprodução da extração de tokens do próprio script contra a árvore". Reproduzir a lógica
  de um instrumento é construir um segundo instrumento, e a armadilha nº 1 do próprio
  documento é que o instrumento mente. O grau honesto é `medido com régua própria, não com o
  portão`. O conserto é barato e não foi feito: rodar `scripts/check_packaging_parity.sh`
  numa cópia e ler a saída dele.

- **§1 e §3 misturam graus na mesma frase, que é justamente o que §4 promete não fazer.**
  "77 ensaios de bancada com o olho dela" (73, ver acima) e "quatro canais diferentes —
  hidraw, sysfs, uhid e alsa-pipewire" convivem com a tabela do §3, que é toda derivada de
  script. O CSV declara SETE valores de canal, não quatro: `hidraw` 116, `outro` 86, `evdev`
  56, `sysfs` 50, `uhid` 32, `alsa-pipewire` 4, `dbus` 3. As 86 células com canal `outro` —
  o segundo valor mais comum do mapa — não aparecem em nenhuma linha do estudo; 16 delas
  dizem `aciona=sim` (todas da família `plataforma.*`, nenhuma com `teste_que_morde`).
  *(Reconferido no transporte, sobre as 586 células.)*

- **Onde o grau está CERTO e merece registro:** B-7 (mutação em clone), B-1 (`git ls-files`
  + clone limpo), A-1/A-3 (lido-no-código, e são), C-5/C-6 (lido-no-código sobre o fonte do
  driver), D-3/D-5 (saída do `gh`). A disciplina de grau do documento é boa; os seis desvios
  acima são a exceção, não a regra.

---

## A pergunta que ninguém fez

**"Sob que condições os 9130 nós rodam — e o que o produto NUNCA executa por causa disso?"**

O documento tem 13 armadilhas e a de número 1 é *"o instrumento mente mais que o produto"*.
Nenhum dos agentes abriu o instrumento-mãe: `tests/conftest.py`, 1463 linhas, zero menções
no documento inteiro. E ele não é passivo. Medido agora:

- `tests/conftest.py:1109-1132` é um fixture `autouse=True` (o ÚNICO `autouse=True` do
  arquivo) que liga o modo FAKE em **todo** teste que não o tenha definido, e isola os
  diretórios XDG de config, data, cache e state num tmp por teste.
- Em `src/`, essa env é lida em 9 pontos, 4 arquivos — e um deles é
  `daemon/main.py:18`, o ponto de entrada do daemon, que **troca o backend** conforme o
  valor. Outro é `daemon/subsystems/keyboard.py:322`.

Ou seja: o ramo não-fake do ponto de entrada do produto não é exercido pela coleta padrão, e
ninguém mapeou o que mais fica inalcançável. Isso importa porque o achado de bandeira do
documento — **B-7, "os testes MORDEM, conferido por mutação"**, o grau `medido` mais forte
que ele publica — foi medido dentro desse fixture. A mordida provada vale para as três curas
mutadas; o que ela não prova é que a régua alcança o produto que roda na máquina dela. O
próximo agente deveria: (1) enumerar, por leitura do fonte, cada ramo de `src/` alcançável só
com o FAKE ausente; (2) rodar a suíte com o autouse desligado numa cópia e contar quantos nós
mudam de resultado; (3) responder se algum dos 40 `teste_que_morde` do mapa vive num ramo que
o FAKE desvia. Se algum viver, aquela célula do mapa tem grau forte sustentado por um teste
que nunca tocou o caminho real — e isso é a doença que o mapa inteiro existe para impedir.

Segundos lugares, se houvesse mais dois agentes: (a) **a camada de entrada** —
`core/evdev_reader.py` (1929 linhas), `integrations/window_detect.py`,
`integrations/xlib_window.py`, `integrations/window_backends/`,
`daemon/subsystems/autoswitch.py`, `profiles/autoswitch.py` (731): a troca de perfil por
janela em foco é vendida na segunda frase do §1 e não foi lida por ninguém; (b)
**`docs/usage/`** — o documento provou duas vezes (A-4, A-5) que a deriva documento↔código é
o defeito mais comum desta casa, e depois procurou essa deriva em 2 dos 17 arquivos, deixando
de fora `docs/usage/troubleshooting.md` (40 KB), `docs/usage/modos.md`, `docs/usage/cli.md` e
`docs/usage/troubleshooting-8bitdo.md`.
