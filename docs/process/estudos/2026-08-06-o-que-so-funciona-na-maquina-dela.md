# O que só funciona na máquina dela

Varredura de portabilidade da árvore de **06/08/2026** (`ae32c10`). Todo
`caminho:linha` foi reconferido depois da última mudança do dia. Nada foi
editado em `src/`, em `tests/` ou nos `assets/` — este documento é inventário,
não cura.

---

## A pergunta em aberto, que só ela responde

Em 06/08/2026 ela perguntou:

Citação **literal**, sem correção de acentuação. Citação não se corrige.

> *"to mapeando os meus controles fisicos, mas se por exemplo outro amigo meu
> com os 4 controles iguais aos meus (deles, nao os meus de fato) — ele vai usar <!-- noqa-acento -->
> o mesmo app e vai funcionar la tambem?"* <!-- noqa-acento -->

A pergunta tem uma resposta técnica (está adiante, item por item). Mas ela
abre uma pergunta **de produto** que nenhuma medição responde, e que este
documento não vai responder por ela:

> **O Hefesto é a ferramenta DELA, ou é um produto para outras pessoas?**

As duas respostas são legítimas, e as duas são caras de fingir. O que muda:

**Se for ferramenta dela**, quase tudo aqui vira **acervo**, não dívida. A
tabela de OUI com um item está certa — ela tem aquele aparelho. O preset
`sackboy_nativo` está certo — é o jogo dela. O `hci0` fixo no doctor está certo
— o adaptador dela é o `hci0`. O que sobra de trabalho de verdade é curto: o
caminho absoluto do instrumento de captura, a assimetria dos layouts de Steam
(que já a atinge se ela migrar para Flatpak) e o vazamento de MAC do
repositório, que é dano a **ela**, não a terceiros. O resto vira uma nota:
*"isto foi calibrado para esta bancada"*. **E o custo dessa escolha é que a
cura genérica do 8BitDo perde metade da urgência** — ela viraria só mais um
conserto, não uma promessa.

**Se for produto para outras pessoas**, a lista abaixo deixa de ser inventário
e vira **backlog com ordem**, e três coisas mudam de natureza:

1. **degradar em silêncio deixa de ser aceitável.** Hoje, quando uma tabela de
   um item não casa, o produto não avisa — ele responde outra coisa com a mesma
   confiança de sempre. Numa máquina que ninguém pode inspecionar, isso é
   indistinguível de defeito;
2. **toda constante calibrada nesta bancada precisa declarar o que faz quando
   não casa.** Não necessariamente cair fora: mas dizer, em log ou em tela, que
   não reconheceu;
3. **as fotos, os presets e os exemplos da interface passam a falar de jogos e
   de aparelhos que a pessoa do outro lado não tem.**

Não há terceira via barata. O meio-termo honesto existe e tem nome: *"funciona
para quem tem hardware parecido, e diz quando não reconhece"* — mas ele custa o
item 2 acima, que é trabalho real em pelo menos cinco lugares desta lista.

**Esta pergunta está em aberto e é dela.** Tudo abaixo está organizado para que
a resposta dela possa ser aplicada de uma vez, sem reler o código.

---

## Como ler as três categorias

| categoria | definição operacional |
|---|---|
| **QUEBRA** | na máquina de outra pessoa, alguma coisa para de funcionar de um jeito visível, e a pessoa percebe |
| **DEGRADA EM SILÊNCIO** | o produto responde **outra coisa**, com a mesma confiança de sempre, e ninguém fica sabendo. É a categoria perigosa |
| **COSMÉTICO** | fica esquisito, inerte ou desnecessário, mas nada mente e nada quebra |

Cada item declara o GRAU: **MEDIDO** / **SUSPEITA COM MECANISMO** / **SEM PROVA**.

---

## 1. QUEBRA na máquina de outra pessoa

### 1.1 O instrumento de captura de tela tem o caminho da casa dela cravado

`scripts/gui-captura/retrato_offscreen.py:21` —
`_RAIZ_PADRAO = "/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix"`, e
a linha seguinte lê `HEFESTO_RAIZ` do ambiente com esse valor como padrão.

**GRAU: MEDIDO.** Sem `HEFESTO_RAIZ` no ambiente, o instrumento aponta para um
diretório que não existe. É o **único** `/home/<usuária>` literal em arquivo
executável da árvore (o resto mora em log e em estudo).

E ele **já está errado para ela**: a árvore viva é `/mnt/Apate/...`; o caminho em
`/home` é um link que resolve para lá. Funciona por acidente do link, não por
desenho.

Isto quebra o gesto que o `CLAUDE.md` manda rodar **antes de commitar** e
**antes de gerar release** (`scripts/gui-captura/retratar_abas.py`). Ou seja:
quebra a regra da casa, não só o script.

**É o item mais barato da lista inteira** — derivar a raiz do próprio arquivo
(`Path(__file__).resolve().parents[N]`) resolve, e não muda comportamento nenhum
para ela.

---

## 2. DEGRADA EM SILÊNCIO

Esta é a seção que muda de gravidade conforme a resposta dela lá em cima.

### 2.1 As duas tabelas de OUI com UM item — e a prova de que "um OUI por fabricante" é falsa

- `src/hefesto_dualsense4unix/app/actions/external_controllers.py:64` —
  `_BRAND_BY_OUI`, **um** item: o OUI da 8BitDo, `e4:17:d8`;
- `src/hefesto_dualsense4unix/daemon/subsystems/external_identity.py:160` —
  `NINTENDO_REAL_OUI = "e0f6b5"`, consumido no **portão estrito** de `:859`
  (`if key[:6] != NINTENDO_REAL_OUI: continue`).

**GRAU: MEDIDO.** Os dois valores são os OUIs dos aparelhos **desta bancada**.

**E a refutação de "um OUI por fabricante" está na mesa dela mesma:** os DOIS
DualSense do registro têm OUIs **diferentes**. Dois aparelhos do mesmo modelo,
do mesmo fabricante, dois OUIs. Medido também: o `systemd-hwdb` desta máquina
resolve o OUI da 8BitDo e o da Nintendo, mas **não conhece nenhum dos dois OUIs
dos DualSense** — então nem "consultar o banco público de OUI" seria regra
confiável.

Consequências na máquina de outra pessoa, as duas silenciosas:

| aparelho | o que acontece | por quê |
|---|---|---|
| 8BitDo de outro lote, em modo PS4 | a aba chama ele de **Sony** | `brand_of` (`external_controllers.py:108`) cai no `_VENDOR_BY_VID["054c"]`, porque o OUI não casa. É o `NOME-HONESTO-01` renascendo por lote de fábrica |
| Pro Controller genuíno de outro lote | o giroscópio fica em **STANDBY** | o portão de `external_identity.py:859` nunca casa, o enable-IMU nunca é enviado, e **não há uma linha de log no ramo do `continue`** |

O segundo é o pior da seção: um recurso do produto simplesmente não existe
naquela máquina, e não há nada — nem tela, nem journal — que diga por quê.

**Este item é pré-requisito de honestidade da cura genérica do 8BitDo**
([REGRA-NAO-REGISTRO-01](../sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md)):
aquela cura funciona sem saber o nome do fabricante, mas a linha que ela põe na
ficha vai **mentir** o fabricante enquanto estas duas tabelas tiverem um item.

Nota de escopo: a cura do `NOME-HONESTO-01` para o **caminho USB** (onde não há
`uniq`, logo não há OUI) **ainda não está na árvore**. Não existe tabela por
nome de produto em `external_controllers.py`; a ordem em `friendly_type`
(`:88-105`) é VID:PID, depois OUI, depois VID, depois nome cru.

### 2.2 O doctor olha só o `hci0` — e o irmão dele já foi consertado

`scripts/doctor.sh:1899` (`_dbus_bt_prop /org/bluez/hci0 ...`) e `:1907`
(`hciconfig hci0 ...`).

**GRAU: MEDIDO.** Num adaptador em `hci1` — dongle USB externo, que é comum, e
que **já aconteceu nesta própria máquina** — os dois checks de rádio do doctor
devolvem vazio **sem dizer que não olharam**. Um doctor que não olha e não avisa
é pior que um doctor ausente.

O irmão dele já registra este exato defeito como corrigido:
`scripts/bt_health_watchdog.sh:137-140`, sob o ID `WATCHDOG-HCI-HARDCODE-01`
(23/07), com o motivo escrito no comentário. **O doctor ficou para trás.** A
cura já existe na casa, na função `_dbus_device_paths` do watchdog.

Menor, mesma família: `scripts/medir_w3_coex.sh:46` (`HCI=hci0`) — é bancada de
medição, não produto. **GRAU: MEDIDO / gravidade baixa.**

Nota: `scripts/doctor.sh:1893` também constrói uma instrução de cura para a
pessoa copiar, com `/org/bluez/hci0` embutido. Ali o dano é a **instrução**
estar errada, não a leitura.

### 2.3 Uma decisão deliberada sobre Proton vazou para um lugar onde o motivo dela não vale

`src/hefesto_dualsense4unix/integrations/proton_pin.py:152-165` —
`default_steam_root` conhece **só** `~/.steam/steam` e `~/.local/share/Steam`. E
o docstring explica por quê, com razão: *"Flatpak/Snap ficam DE FORA de
propósito: o Proton extraído no host é invisível dentro da sandbox — travar
jogos lá num tool inexistente quebraria o launch"*.

**Esse motivo está certo, e vale para o pino de Proton. Ele não vale para
traduzir um appid em nome de jogo — e é exatamente aí que a função foi
reusada.**

`src/hefesto_dualsense4unix/integrations/steam_launch_options.py:792-800` —
`pastas_steamapps` importa `default_steam_root` e monta a lista de bibliotecas a
partir dela; `nome_do_appid` (`:814`) depende disso. **GRAU: MEDIDO.**

Efeito para quem usa Steam por Flatpak ou por Snap: `nome_do_appid` devolve
`None` e **toda mensagem passa a dizer "appid 1599660" em vez do nome do jogo** —
e o doctor de Proton diz "nenhum jogo fora do pino" quando o que houve foi não
ter olhado.

**A assimetria que prova que é dívida e não desenho:** o **mesmo produto**
conhece os QUATRO layouts em dois lugares —
`steam_launch_options.py:111-115` (`_VDF_GLOB_PATTERNS`: nativo,
`.local/share/Steam`, Flatpak e Snap) e `storm_doctor.py:146-149` — e só DOIS
aqui.

### 2.4 A aba Emulação e o doctor discordam sobre o mesmo Steam, na mesma janela

`src/hefesto_dualsense4unix/app/actions/emulation_actions.py:1262` e `:1292` —
os dois `glob` de `localconfig.vdf` montam
`Path.home() / ".steam" / "steam" / "userdata" / "*" / "config" / "localconfig.vdf"`,
**um layout só**.

**GRAU: MEDIDO.** O doctor, na mesma instalação, usa `find_localconfig_vdfs`
(`storm_doctor.py:144-149`) e enxerga os quatro. Resultado para quem usa Flatpak
ou Snap: **a aba Emulação nunca vê o Steam Input, e o doctor vê** — duas
verdades sobre o mesmo arquivo, na mesma janela, para a mesma pessoa.

O conserto é trocar a construção local pelo helper que já existe.

### 2.5 O matcher de perfis fala inglês, e a heurística de sanidade fala português

**(a) Os presets de gênero casam por título em inglês e por `.exe`.**
`assets/profiles_default/acao.json` (prioridade 65) casa
`window_title_regex` com nomes em inglês e `process_name` com nove executáveis
`.exe`; os irmãos `aventura`, `corrida`, `esportes`, `fps` e `coop_local` seguem
o mesmo molde. **GRAU: MEDIDO.**

Para quem roda a Steam em outro idioma, ou títulos nativos de Linux (sem
`.exe`), o automatismo simplesmente não entra — e o produto não diz que não
entrou. Isto não é "dela": é dívida de internacionalização do matcher, e atinge
ela também no dia em que um jogo mudar de nome de janela.

**(b) `src/hefesto_dualsense4unix/profiles/sanidade.py:77-98` —
`VOCABULARIO_GENERICO` é uma lista de 17 palavras em português** (com quatro em
inglês por acidente: `fallback`, `default`, `desktop`, `video`).

A heurística de nome está **declarada como heurística** no próprio módulo
(`:200-205`, com a gravidade rebaixada a "aviso" e a cura de silenciamento
documentada) — isso é desenho honesto. O que não é portável é a **lista**:
alguém que nomeie o catch-all dele `main`, `everything` ou `general` recebe um
achado falso *"catch-all com nome próprio"*.

**GRAU: MEDIDO (a lista) / SUSPEITA COM MECANISMO (o falso alarme — derivado da
lista, não observado em campo).** Degrada em **falso alarme**, que é a forma
menos danosa desta seção: ruído, não mentira.

### 2.6 Um teste lê o `$HOME` de verdade — sem mudar de resultado, ainda

**Medido, não deduzido.** Em 06/08 o subconjunto sensível a `$HOME` foi rodado
com um `HOME` vazio (`test_storm_doctor`, `test_steam_input_ponteiros`,
`test_steam_input_honestidade`, `test_proton_pin`, `test_system_check`,
`test_button_glyph`, `test_service_install`, `test_steam_launch_options_vdf`,
`test_mic_monitor`): **265 passaram, nenhum mudou de resultado.**

Mas um **lê o disco dela**: `tests/unit/test_storm_doctor.py:16-31` chama
`sd.check_steam_input(tmp_path)`; o `home` viaja, mas `storm_doctor.py:171`
resolve a allowlist chamando `steam_input_allowlist()` **sem argumento**, que cai
em `_allowlist_path()` (`:34-50`) e lê `Path.home()`. O `conftest` isola os XDG,
**não o `HOME`**.

Hoje o resultado não muda (o vdf da bancada só tem a chave GLOBAL, que ignora a
allowlist). O irmão `tests/unit/test_steam_input_ponteiros.py:194` já se protege
com `monkeypatch.setattr(sd, "_allowlist_path", ...)`; este não.

**GRAU: MEDIDO (a leitura) / SEM PROVA (efeito no resultado).** É exatamente a
classe que o
[CANARIO-FS-01](../sprints/2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md)
documenta — e o canário vigia **escrita**, não leitura.

---

## 3. Só COSMÉTICO

Nada aqui mente e nada aqui quebra. Fica esquisito, inerte ou desnecessário.

### 3.1 Presets de fábrica que nasceram do uso dela

`scripts/install_profiles.sh` (e o espelho `seed_default_presets` em
`profiles/loader.py`) semeia os **12** JSONs de `assets/profiles_default/` na
máquina de quem instalar. Três são biografia:

| preset | o que carrega | efeito fora daqui | GRAU |
|---|---|---|---|
| `sackboy_nativo.json` | `window_class: ["steam_app_1599660"]`, prioridade **80** — a mais alta dos presets | **inerte**: a regra nunca casa. O custo é ver na lista um perfil que não faz nada | MEDIDO |
| `point_and_click.json` | `window_class: ["GrimFandango", "grim"]`, com `key_bindings` e `mouse` afinados para aquele jogo | inerte | MEDIDO |
| `bow.json` | prioridade 10, gatilho `Bow` para cinco títulos por regex de título — invenção dela | inerte até a pessoa ter um daqueles jogos | MEDIDO |

**O quarto é cosmético com cheiro de dívida:** `meu_perfil.json` tem
`match: {"type": "any"}` e prioridade **1**, ou seja **acima** do `fallback`
(prioridade 0). **GRAU: MEDIDO.** Na máquina de outra pessoa o catch-all efetivo
do desktop passa a ser `meu_perfil` — lightbar azul `[40, 80, 180]`, LED de
jogador 3 — e não o `fallback`. É deliberado (`scripts/install_profiles.sh`
explica: *"o slot da usuária deve sempre existir"*), mas **o nome e as cores são
as dela**, e a pessoa não tem como saber que aquele é o slot dela para editar.

### 3.2 Vocabulário e imagens de tela

| onde | o que carrega | GRAU |
|---|---|---|
| `src/hefesto_dualsense4unix/gui/main.glade:2845` (e o espelho em `po/`) | o texto de ajuda das máscaras nomeia Sackboy, Pragmata, Mad King Redemption e Mullet Mad Jack — a biblioteca dela vira exemplo universal. É o único lugar da **interface** onde isso acontece | MEDIDO |
| `docs/usage/assets/` | as fotos do `README.md` mostram a fila de controles DELA | MEDIDO |
| `src/hefesto_dualsense4unix/app/actions/status_actions.py:1095` | `label.replace("Controle ", "Sony ")` — a justificativa (`:1085-1092`) é correta: o backend só **adota** DualSense. **Portável.** Fica esquisito só para quem tem um DualSense e três externos: o seletor mistura "Sony 1" com "8BitDo 3" e, num clone de outro lote, com "Sony 3" (ver 2.1) | MEDIDO |
| `src/hefesto_dualsense4unix/core/led_control.py:146-157` | paleta de 8 slots — **portável**, é convenção do PS5 estendida pela casa, com o motivo escrito (R-25) | MEDIDO |

### 3.3 Coisas que parecem dívida e NÃO são

Vale registrar, porque custam tempo toda vez que alguém varre a árvore:

- **VID/PID e nomes USB da Sony** —
  `broker/hidraw_broker.py:81-83`, `integrations/uinput_gamepad.py:57-78`,
  `core/backend_pydualsense.py`. É identidade de **modelo**, não de aparelho.
  **Portável, sem dívida.** GRAU: MEDIDO;
- **os 15 arquivos `assets/*.rules` e os três `assets/wireplumber/*.conf`** —
  casam por VID/PID e por regex de nome. **Portáveis.** GRAU: MEDIDO;
- **`captures/*.bin`** — descritor, calibração `0x05` e firmware `0x20` do
  controle dela. São fósseis de procedência, comparados só em teste hermético
  (`tests/unit/test_uhid_blueprint.py`); a produção lê a calibração viva.
  Conferido em 06/08 por varredura hexadecimal: **nenhum dos seis OUIs desta
  bancada aparece dentro dos três arquivos**. GRAU: MEDIDO;
- **`assets/hefesto-launch.sh:214`** — `GM_BUS_DEST="com.system76.PowerDaemon"`.
  Best-effort explícito: sem uma máquina System76, o script simplesmente não
  pede o perfil de energia Performance. **Cosmético.** GRAU: MEDIDO;
- **`packaging/`, `install.sh`, `uninstall.sh`** — tudo derivado de `${HOME}` e
  de `ROOT_DIR`. **Portáveis.** GRAU: MEDIDO;
- **AppIDs de jogo:** **não há allowlist versionada.** O arquivo
  `steam_input_apps.txt` nasce vazio no `$HOME` (`storm_doctor.py:34-50`);
  `grep` em `install.sh` e em `profiles/loader.py` não devolve nada. O appid do
  Mullet Mad Jack aparece só em docstring, comentário e bancada de teste.
  **Sem dívida.** GRAU: MEDIDO;
- **as strings de topologia PCI dela** em `tests/unit/test_external_gamepads_inventory.py`
  e em `tests/unit/test_backend_ignora_vpad_virtual.py` são dados **forjados e
  monkeypatchados**, não leituras da máquina. **Cosmético.** GRAU: MEDIDO.

---

## 4. Fora das três categorias, e mais urgente que todas: o repositório publica a identidade de rádio dos aparelhos da casa

Esta seção não é sobre a máquina do amigo. **O dano é dela.** É regra da casa —
*"nada de MAC real em arquivo versionado"* — e está sendo violada **hoje**, em
três formas, e os portões são cegos às três.

O portão é `tests/unit/test_docs_mac_anonimato.py`. O contrato dele está escrito
no próprio docstring: MAC completo cujo prefixo seja um OUI real desta bancada
precisa ter os **octetos 4 e 5 zerados**. O regex (`:34-38`) exige separador
`[:_-]` entre todos os octetos e um dos OUIs listados em `OUIS_REAIS`
(`:26-32`).

### (a) Forma 12-hex contígua — o portão exige separador, o registro grava colado

O `controllers.json` guarda o endereço **colado** (12 hex, sem separador), e foi
assim que endereços foram colados nos estudos. `MAC_COMPLETO_RE` não vê essa
forma.

**Contagem de hoje, por `git grep` sobre arquivos rastreados: 20 linhas em 7
arquivos** — seis sprints em `docs/process/sprints/` e um estudo em
`docs/process/estudos/`. Os quatro OUIs afetados são os **quatro aparelhos da
casa**. **GRAU: MEDIDO.**

(Este documento não reproduz nenhuma das linhas, por motivos óbvios. A lista de
arquivos sai de `git grep -icE '(<oui>)[0-9a-f]{6}'` com os quatro OUIs.)

### (b) Forma com o prefixo elidido, numa página de USUÁRIA

`docs/usage/troubleshooting-8bitdo.md:96` mostra os três últimos octetos dos
**dois** endereços do 8BitDo **e nomeia o OUI na mesma linha**. O endereço
inteiro se remonta lendo a frase. Conferido: **são os endereços reais**.

O portão não vê porque o regex exige o OUI **adjacente** ao sufixo, e ali ele
está a meia frase de distância.

**É o pior dos três**, porque é o único que está numa página que a casa publica
para quem instala. **GRAU: MEDIDO.**

### (c) O portão não conhece um dos aparelhos

`OUIS_REAIS` (`tests/unit/test_docs_mac_anonimato.py:26-32`) lista **cinco**
OUIs, e **não lista o do primeiro DualSense** — que aparece em pelo menos oito
documentos rastreados. **Um MAC real desse aparelho, na forma canônica com
dois-pontos, passa verde hoje.** GRAU: MEDIDO.

Este buraco já havia sido registrado em 29/07, no
`docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md`.
**Segue aberto sete dias depois** — o que, por si só, diz que registrar não
basta.

### Por que os outros dois portões não pegam

- `scripts/check_test_data.sh` só varre `tests/`;
- `scripts/check_anonymity.sh` é **cego a MAC** — ele caça menções a provedores
  de IA, e ainda exclui `docs/process/` inteiro por pathspec.

GRAU: MEDIDO. O conserto é regex mais máscara, não desenho — e é o único item
desta lista que não depende da resposta dela lá em cima.

---

## Ordem proposta

Independe da resposta "ferramenta ou produto":

1. **Seção 4 (a), (b) e (c)** — vazamento vivo, dano a ela, conserto mecânico.
   O (b) primeiro, porque é página de usuária.
2. **Item 1.1** — o caminho absoluto no instrumento de captura. Quebra a regra
   da casa e o conserto é uma linha.

Só faz sentido se a resposta for "produto":

3. **Item 2.1** — as duas tabelas de OUI com um item. É pré-requisito de
   honestidade da cura genérica do 8BitDo, e o ramo silencioso do enable-IMU é
   o pior tipo de degradação que a árvore tem hoje.
4. **Itens 2.3 e 2.4** — a assimetria dos layouts de Steam. Quatro caminhos em
   dois módulos, dois caminhos em dois outros. Hoje, quem usa Flatpak é usuária
   de segunda classe **sem aviso**, e vê duas verdades na mesma janela.
5. **Item 2.2** — `hci0` fixo no doctor. A cura já existe no watchdog irmão.
6. **Itens 2.5 e 3.1** — falso alarme e presets inertes. Ruído, não dano.

Nada disto foi corrigido nesta varredura, por instrução: outros agentes estão
escrevendo na árvore.
