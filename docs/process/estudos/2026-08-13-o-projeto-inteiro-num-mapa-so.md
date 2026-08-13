# O projeto inteiro num mapa só — 13/08/2026

> **Como esta página nasceu.** Rodada de estudo em paralelo, **somente leitura**, na
> madrugada de **13/08/2026**, contra a árvore em **`cc768d4`** — a mesma que carrega a
> tag **`v0.9.4.2`** —, branch `restauro/inicio-da-sessao`, limpa. Nada foi escrito em
> hardware, nenhum serviço reiniciado, nenhum controle derrubado; os quatro DualSense
> dela seguiram na mesa e o daemon seguiu vivo durante a medição inteira.
>
> **Quantos agentes.** Doze, na contagem de quem conduziu a rodada. O corpo do estudo
> descreve **sete dimensões** de material recebido e o crítico de completude fala em
> **nove agentes**: os três números vêm de lugares diferentes e **nenhum foi recontado
> no transporte** — ficam os três na mesa, como manda a casa.
>
> **Como ler os graus.** Cada achado traz o seu, e graus não se misturam na mesma frase:
>
> | grau | significa |
> |---|---|
> | **medido** | saiu de um comando rodado nesta árvore, nesta data, ou de mutação que reprovou e foi devolvida |
> | **lido-no-código** | o caminho foi lido no fonte e fecha; o efeito não foi observado |
> | **inferido** | dedução a partir de duas leituras, sem execução que confirme |
>
> **O crítico de completude derrubou três afirmações desta página, e elas já estão
> corrigidas no texto abaixo.** Isso é decisão medida e não se apaga: as três eram a
> contagem de `observado_por` no caderno de ensaios (§1), a força da frase sobre o
> `diff -rq` do DKMS (D-7), e a régua não publicada das funções `test*` (§4.7). O
> relatório inteiro dele está em
> [o que ficou de fora — o crítico de completude](2026-08-13-o-que-ficou-de-fora-o-critico-de-completude.md),
> e vale lê-lo antes de agir a partir daqui: o que falta a esta página é **escopo**, não
> veracidade, e ele diz exatamente onde.
>
> **O que o transporte para o repositório corrigiu, em 13/08**, conferindo os
> `caminho:linha` um a um contra `cc768d4`:
>
> - **B-4** citava `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:726-734`; a
>   entrada de `strip_quirks_token` mora em **`:734-742`**. A afirmação continua
>   verdadeira; o endereço tinha apodrecido.
> - **D-1** dizia que o `.venv` vai para `/root` sob `sudo`. Não vai: `install.sh:191`
>   o ancora em `ROOT_DIR`, não em `HOME` — sob `sudo` ele nasce na árvore com dono
>   root, que é outro estrago. Os outros três alvos da frase estão certos.
> - **E-4** dizia "seis regras"; são **oito**
>   (`assets/84-nintendo-pro-variant.rules:55-68`).
>
> Nesta casa uma linha que não abre vale o mesmo que nenhuma — ver a armadilha 6.

Árvore em `cc768d4`, tag `v0.9.4.2` publicada, branch `restauro/inicio-da-sessao`, limpa.
Estudo em paralelo, somente leitura, sobre sete dimensões do projeto. Cada número
abaixo tem origem; onde dois agentes divergiram, os dois números estão na mesa com a
fonte de cada um.

---

## 1. O produto em dez linhas

O Hefesto é um daemon de sessão (systemd `--user`, laço asyncio a 60 Hz, `nice 5`) que
fica entre os controles dela e os jogos, em Linux, sem Steam Input no caminho. Ele lê a
entrada por `evdev` e escreve a saída por quatro canais diferentes — `hidraw`, `sysfs`,
`uhid` e `alsa-pipewire` —, cada um escolhido por regra, não por acaso. Ele forja um
DualSense Edge virtual (`054c:0df2`) para que a Launch Option da Steam possa esconder o
controle físico sem esconder o virtual junto: o pior caso é controle duplicado, nunca
zero controle. Ele acende a lightbar e os LEDs de jogador, aplica gatilho adaptativo,
vibra, roteia áudio, troca de perfil pela janela em foco, e tem co-op de até quatro
controles com identidade própria por jogador. Um segundo serviço, este de sistema e como
root, esconde o nó `/dev/hidrawN` do físico do próprio uid da sessão, porque daemon,
Steam e jogo rodam com o mesmo uid e o DAC não os separa. A interface é uma janela GTK3
de dez abas que nunca fala com o hardware: tudo passa por 37 métodos num socket Unix
JSON-RPC. O usuário é ela, com quatro DualSense, um Pro Controller, um 8BitDo SN30 Pro e
uma máquina Pop!\_OS sob COSMIC. E o que este projeto de fato produz, além do software, é
um caderno de campo: 293 linhas de mapa de canais, 77 ensaios de bancada — **73 pelo olho
dela, 4 por instrumento** (`observado_por`: 73 `olho-dela`, 4 `bancada`) —, e oito portões
que reprovam afirmação forte sem prova.

> **Ressalva de grau, do crítico:** a frase acima mistura um recorte do código (os quatro
> canais que o produto escreve) com uma contagem de CSV. O `docs/data/mapa-controles.csv`
> declara **sete** valores de canal, não quatro: `hidraw` 116, `outro` 86, `evdev` 56,
> `sysfs` 50, `uhid` 32, `alsa-pipewire` 4, `dbus` 3 (contagem por `csv.DictReader` sobre
> as 586 células, 13/08). As 86 células `outro` — o segundo valor mais comum do mapa —
> não aparecem em nenhuma linha deste estudo, e 16 delas dizem `aciona=sim`, todas da
> família `plataforma.*`, nenhuma com `teste_que_morde`.

---

## 2. O mapa dos subsistemas

> **Ressalva de escopo, do crítico:** são oito entradas, e a página não diz quantos
> subsistemas ficaram de fora. Ficaram, com zero menções: `tests/conftest.py`,
> `app/widgets/controller_card.py` (o maior arquivo de `src/`), a camada de entrada
> inteira, metade de `daemon/subsystems/` e quase toda a `integrations/`. A lista
> completa está no crítico.

**O daemon e o caminho do byte** — porta de entrada: `src/hefesto_dualsense4unix/daemon/lifecycle.py`.
Sobe em ordem escrita à mão em `Daemon.run` (`lifecycle.py:690-720`), cada subsystem
isolado por `_safe_start`, com dois pools de thread separados por cicatriz de bug real
(`hefesto-hid` com 2 workers para `read_state`, `hefesto-ext` com 1 só para o tique de
LED dos externos — juntos, dois timeouts consecutivos vazavam os dois workers do poll
loop). Antes de qualquer subsystem ele restaura a sessão anterior do disco, e o Modo
Nativo é o gate mais forte: se a sessão terminou nele, o daemon sobe solto. No `_poll_loop`
seis blocos subiram para antes do gate de conexão, e cada subida é uma cicatriz nomeada —
a mais cara é o co-op (JOGADOR-2-REFEM-01: o `continue` do gate levava o P2 junto). O
gamepad virtual é despachado **antes** dos gates de pausa e supressão, de propósito,
porque o físico está `EVIOCGRAB`-grabado e pausar deixava o controle morto no jogo. ADR-015
descreve um `lifecycle.py` de ~365 linhas com ordem vinda de registry; medido hoje: 4171
linhas e ninguém itera registry nenhum.

**A saída para o aparelho** — porta de entrada: `src/hefesto_dualsense4unix/core/backend_pydualsense.py`
(4230 linhas). O `report_thread` monta um report de 47 bytes idêntico nos dois transportes
e troca só o envelope: `0x02` de 47 B por cabo, `0x31` de 77 B por rádio com `seq_tag` e
CRC-32 (semente `0xA2` na saída, `0xA1` na entrada, `0xA3` nas features). O throttle
existe por medição: o laço do upstream roda a 250 Hz–1 kHz, com dois controles satura o
controlador USB, e o adaptador Bluetooth vive no mesmo controlador. O merge do desejado
tem cinco camadas por campo: GAME > CO-OP > override por-uniq > automática > default
global. E o `keepalive` — a reescrita do último report a cada 0,5 s — foi provado por
dose-resposta como sendo o cronômetro do defeito de rumble de terceiros; hoje ele só
sobrevive dentro de uma janela de 2,0 s depois de cada mudança real.

**A permissão e o broker** — porta de entrada: `src/hefesto_dualsense4unix/broker/hidraw_broker.py`.
Único serviço de sistema do projeto, root, hardened, socket-activated, 100% stdlib e
autocontido. Três comandos: `hide` (remove a ACL do `uaccess` e faz `chmod 0600` — o jogo
perde o `open(2)` em qualquer backend, o fd já aberto do daemon sobrevive), `restore`, e
`open` (abre como root e devolve o fd por `SCM_RIGHTS`, ortogonal ao hide). A conexão do
daemon **é** a lease: EOF restaura tudo, sem heartbeat, porque o kernel garante o EOF.
Faz `HIDIOCGRAWINFO` no próprio fd depois do open, contra minor-reuse entre validar e
abrir. E rejeita o vpad `0df2` explicitamente.

**O vpad** — porta de entrada: `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`
(2389 linhas). Cria um device por `/dev/uhid` e o `hid_playstation` constrói um DualSense
inteiro de graça: hidraw, lightbar, LEDs de jogador, motion, touchpad. Carimba `phys`
`hefesto-vpad`, `uniq` `02:fe:00:00:00:0N` (faixa localmente administrada) e produto
`0x0DF2` (Edge) — invariante VPAD-06, travado por teste: nenhum caminho produz `054c:0ce6`.

**A janela** — porta de entrada: `src/hefesto_dualsense4unix/app/app.py`. `HefestoApp` é a
costura de onze mixins de `app/actions/` (`app.py:154-166`), um por aba. Dez páginas no
notebook (Início, Status, No jogo, Gatilhos, Lightbar, Rumble, Perfis, Sistema, Emulação,
Navegação); nove embrulhadas em rolador, só a Sistema fora (o log dela já é rolador). Aba
se identifica por id do Glade, nunca por índice — inserir uma aba renumera todas, e um
gate por índice já pintou a aba errada duas vezes. Todas as abas editam um `DraftConfig`
imutável em memória; o rodapé tem quatro botões e **Aplicar não grava disco** (manda
`profile.apply_draft` pelo IPC). A ponte é um `ThreadPoolExecutor` de um worker, timeout
de leitura 0,25 s e uma exceção declarada: `PROFILE_SWITCH_TIMEOUT_S = 3.0`.

**Os perfis** — porta de entrada: `src/hefesto_dualsense4unix/profiles/schema.py`. Um perfil
é JSON validado por pydantic, `extra="forbid"`, no diretório de perfis do XDG config. O
`match` é união discriminada de três: `MatchCriteria` (AND entre `window_class`,
`title_regex`, `process_name`), `MatchAny` (sempre) e `MatchManual` (nunca sozinho). A
seleção é por **especificidade primeiro, prioridade depois, incumbente no empate** — por
isso um catch-all perde para qualquer regra dentro de um jogo, por mais alta que seja a
prioridade. O rodapé salva sem campo de regra, então a regra é herdada numa escada de três
degraus: disco > fotografia da origem (só se não for catch-all) > `MatchManual` para o
órfão, decisão dela de 05/08 com portão de AST guardando. Toda gravação arquiva a versão
anterior num diretório `.historico/<slug>/`, 10 versões — e isso nunca chegou à janela.

**O IPC** — porta de entrada: `src/hefesto_dualsense4unix/daemon/ipc_server.py`. Socket Unix
em `$XDG_RUNTIME_DIR`, `chmod 0600` logo após o bind (`ipc_server.py:199`), NDJSON JSON-RPC
2.0, teto de 32 KiB. Probe ativo antes do bind distingue socket vivo de resto morto; o
`stop()` compara `st_ino` antes do `unlink`. `ConnectionError` é tratado como cenário
normal, porque a GUI fecha o socket a cada timeout de 0,25 s e antes cada um virava
traceback com locals a ~5 conexões/s, fritando uma CPU e criando espiral. 37 métodos
registrados (`ipc_server.py:106-174`). Há um segundo canal de comando, UDP em
`127.0.0.1:6969`, que aceita dois dialetos na mesma porta (o do Hefesto e o do DSX real) e
decide por conteúdo, falhando alto quando o ordinal é irresolvível.

**O install e o empacotamento** — porta de entrada: `install.sh` (2951 linhas, 45 chamadas de
`step`). É um provisionador de sistema disfarçado de instalador: udev, três módulos DKMS
patchados, cmdline do kernel, broker root, resiliência do BlueZ, WirePlumber, Steam Input,
Proton pinado. Quatro formatos; fora do `native` entrega oito passos, todos ortogonais ao
formato do app. Nunca recarrega módulo em uso, nunca reinicia o `bluetoothd`, nunca aborta
por DKMS, nunca toca parâmetro de cmdline de terceiro. O `doctor` roda no fim por default e
**confere sem curar**, de propósito. `uninstall.sh` (1446 linhas) é simétrico por regra e
assimétrico por decisões escritas e datadas.

**O caderno e os portões** — porta de entrada: `docs/data/mapa-controles.csv` +
`scripts/check_paridade_transporte.py`. 293 linhas de feature × controle × transporte,
com grau por célula, 77 ensaios em `docs/data/ensaios.csv` (73 `olho-dela`, 4 `bancada`),
e onze regras que reprovam afirmação forte sem teste que morda. Isso não é documentação:
é portão, e nasceu de regressões cabo/BT reais.

---

## 3. O sistema do specs.html

**O que é.** `specs.html` (na **raiz** do repositório, não em `docs/data/`) é uma página
única gerada por `scripts/gerar-mapa.py` a partir de três fontes: o CSV do mapa
(`docs/data/mapa-controles.csv`), o caderno de ensaios (`docs/data/ensaios.csv`) e os três
SVGs de `assets/control-svg/`. Ela desenha os três controles e, ao passar o mouse numa
linha da tabela, acende a peça correspondente no desenho. É a superfície onde um fato
medido na bancada vira uma célula que alguém consegue olhar.

**Como o fato vira célula.** Uma linha do CSV declara, por transporte, se o canal
`aceita`, se `aciona`, com que `confianca` (`medido` / `inferido-do-codigo` /
`afirmado-no-doc`), com que `grau` (`MONTOU` < `SAIU NO FIO` < `O APARELHO OBEDECEU`),
quem provou (`provado_por`), qual teste morde (`teste_que_morde`) e quando a mordida foi
provada (`mordida_provada_em`). O campo `peca` casa a linha com um id do SVG, e é isso que
faz o hover acender. O `--check` do gerador regenera a página em memória, normaliza o
espaço no fim da linha e o selo do relógio, e compara por `difflib` — **conteúdo, não
mtime**.

**Quem julga.** `scripts/check_paridade_transporte.py`, onze regras, seis que reprovam e
cinco que avisam. A regra central: célula que afirma `aciona=sim` com `confianca=medido` e
sem `teste_que_morde` reprova — "se isso quebrar, a suíte inteira continua verde". E o grau
forte (`SAIU NO FIO`, `O APARELHO OBEDECEU`) exige ensaio do **mesmo transporte** no
caderno.

**O estado medido hoje** (recontado por script sobre `cc768d4`; a saída do portão é a do
censo rodado nesta sessão):

| medida | valor | origem |
| --- | ---: | --- |
| linhas do mapa | 293 | `csv.DictReader` sobre o CSV |
| por controle | 99 dualsense · 97 pro · 97 sn30 | idem |
| células de transporte | 586 | idem |
| células mudas (`aciona` vazio) | 185 | censo do portão |
| células mudas (`aceita` vazio) | **193** | rodapé do `specs.html` |
| linhas mudas dos dois lados | 84 | censo do portão |
| células que afirmam acionar | 160 | censo (125 `sim` + 35 `parcial`) |
| células com confiança `medido` | 98 | censo |
| afirmações fortes (`sim` + `medido`) | 48 | censo |
| dessas, **sem teste que morda** | **18** | censo — são as 18 reprovações |
| linhas com `teste_que_morde` | 40 | recontado |
| alvos de pytest apontados | 41 | censo |
| assimetrias não declaradas | 14 | censo |
| graus fortes | 15 | censo |
| desses, sem ensaio | 0 | censo |
| linhas com `mordida_provada_em` | **0 de 293** em `cc768d4`; **6 de 293** no commit que publica isto (ver B-6) | recontado |
| ensaios no caderno | 77 | recontado |
| linhas do mapa cobertas por ensaio | **12, todas `@dualsense`** | recontado |
| linhas sem `peca` (não acendem nada) | **168 de 293** | recontado |
| coluna `evdev` preenchida | 14 pro · 13 sn30 · **0 dualsense** | recontado |
| suspeitos inocentados no caderno de eliminação | **0** | rodapé do `specs.html` |
| `gerar-mapa.py --check` | **atualizado, exit 0** | rodado na minicópia |
| `check_paridade_transporte.py` | **exit 1** — 18 falhas, 21 avisos | rodado |

Os 21 avisos: 14 `assimetria-nao-declarada`, 6 `mordida-nao-provada`, 1
`grau-sem-ensaio-que-obedeca` (a linha 95, `gatilho.direito.adaptativo@dualsense`, declara
`O APARELHO OBEDECEU` no cabo e o único ensaio de cabo daquela linha diz "não obedece").

---

## 4. Os achados

Ordenados por importância. Cada um traz evidência e grau; graus não se misturam na mesma
frase.

### 4.1 A janela e o IPC dizem que fizeram o que não fizeram

**A-1. O `aplicado_em` do `led.set` tem duas semânticas dentro do mesmo handler, e uma
delas mente.** No ramo broadcast, `_registrar_em_todos` filtra por `_uniqs_conectados()` e
o campo é honesto. No ramo por-`uniq`, o valor é literalmente `[params["uniq"]]` — o eco do
pedido: `_apply_por_uniq` devolve True sem checar conexão, e `apply_output_for` com um MAC
desconectado **registra o override e pula a escrita**, em silêncio (log debug
`apply_output_for_desconectado_registrado`). Resultado: `led.set` com o `uniq` de um
controle desligado responde `aplicado_em` com aquele endereço e zero bytes no fio —
exatamente o "ok mentiroso" que o campo foi criado para eliminar, agora dentro do campo.
*Grau: lido-no-código.* `daemon/ipc_handlers.py:1026-1028` e `:821-840`;
`core/backend_pydualsense.py:3384-3426` (o ramo desconectado em `:3416-3423`); contraste em
`ipc_handlers.py:915-919`.

**A-2. O `trigger.set` não tem `aplicado_em`, e com a mesa vazia mente como o `led.set`
mentia.** Com nenhum handle aberto, `_for_each` registra o desejado, loga
`output_offline_noop` em DEBUG e volta; o handler devolve `{"status": "ok"}` e o cliente não
tem um campo por onde descobrir que zero bytes saíram. O `led.set` no mesmo caso responde
`aplicado_em: []`, que é detectável. Metade da assimetria é legítima e está no merge (o
provider automático só preenche `led` e `player_leds`, nunca `trigger_*`); a metade da mesa
vazia não é. *Grau: lido-no-código.* `daemon/ipc_handlers.py:936-957` × `:1026-1061`;
`core/backend_pydualsense.py:2313-2315`; `daemon/subsystems/identity.py:1013-1030`.

**A-3. A vibração mira certo e a INTENSIDADE não — a tela promete endereço para as duas.**
`OutputSpec` — o vocabulário da escrita por MAC — tem cinco campos e **nenhum de rumble**
(`core/controller.py:49-68`), e `_handle_rumble_set` de fato **não lê `uniq`**
(`daemon/ipc_handlers.py:3231-3256`). Mas o pulso **não** sai em broadcast por causa disso: o
endereço viaja **por fora da chamada**. `set_rumble` (`core/backend_pydualsense.py:2845`)
delega a `_for_each_com_key` (`:2320`), que resolve o alvo no ponteiro `_output_target_key`
(`:2336-2338`) — armado pelo chip do cabeçalho. Com um controle escolhido, o "Testar motores"
vibra **só ele**. O que age em todos é a **política de intensidade**: `rumble.policy_set`
grava em `daemon.config.rumble_policy`, um campo global sem `uniq` nenhum
(`daemon/ipc_handlers.py:3314-3336`), enquanto o rascunho grava por peça — que é exatamente o
que a docstring de `_gravar_intensidade_no_rascunho` já dizia ("o que ela ouve na hora é o
global; o que ela SALVA é da peça"). E há um segundo defeito que este estudo não viu: o valor
fixado **MIGRA de dono** quando ela troca o alvo, porque o re-assert do poll loop
(`daemon/lifecycle.py:2954`, a 200 ms) reescreve para o alvo **de agora**, não para o de quem
pediu. *Grau: lido-no-código.*

> **CORREÇÃO de 13/08/2026 — fato SUBSTITUÍDO, não guardado ao lado.** Este achado dizia
> "escreve direto no controller, que é broadcast", e a §7 propunha "mecanismo novo no
> backend". As duas são **falsas**, e a régua que as derrubou foi o censo das dez abas do mesmo
> dia — ver [o censo](2026-08-13-o-censo-das-dez-abas-o-que-a-janela-faz-com-quatro-controles.md)
> e [MESA-CHEIA-05](../sprints/2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md),
> que carrega a cadeia degrau a degrau. O "mecanismo novo" também já existia:
> `set_rumble_for(uniq, weak, strong)` está em `core/backend_pydualsense.py:3642` desde antes
> de `cc768d4`, e é usado por `daemon/subsystems/coop.py:571` e
> `daemon/subsystems/gamepad.py:992`. O que **fica de pé** do achado original é o essencial: a
> aba Rumble promete endereço e entrega endereço só em metade do que faz.

> **O crítico acrescenta:** a saída de cinco minutos já existe escrita, 1400 linhas ao lado
> — `app/actions/status_actions.py:1859` traz o texto "Editando: {alvo} — sem endereço
> fixo, vale para todos". Ela só não aparece porque `_update_edit_badge` (`:1955-1962`) a
> condiciona a `bool(self._edit_target_uniq)`, isto é, à identidade do CONTROLE e não à
> capacidade da FEATURE. O conserto barato não é escrever uma frase; é passar
> `com_endereco=False` quando a aba ativa for a Rumble.

**A-4. O contrato publicado do IPC descreve um daemon que não existe mais.**
`docs/protocol/ipc-unix-socket.md` tem uma tabela de 10 métodos; o dispatcher registra 37, e
**18 não aparecem em lugar nenhum** do documento — inclusive a família inteira do rumble,
`gamepad.emulation.set`, `keyboard.emulation.set`, `plugin.list`/`plugin.reload`,
`daemon.pause`/`daemon.resume`. E a tabela está factualmente errada em duas células: diz que
`led.set` devolve `{status}` (devolve `{status, aplicado_em}`) e que aceita
`player_leds?: [bool]*5` (não aceita; quem faz isso é `led.player_set`, que a tabela não
lista). *Grau: medido* (contagem por script sobre `daemon/ipc_server.py:106-174` ×
`docs/protocol/ipc-unix-socket.md:31-42`; recontado no transporte, 13/08: 37 registrados,
18 ausentes do documento).

> **FECHADO no commit de 13/08/2026 — e o endereço acima caducou junto.** A tabela deixou de
> ser mantida à mão: `scripts/gerar-contrato-ipc.py` a emite do dicionário `_handlers`
> (`daemon/ipc_server.py:106`), e o `--check` reprova a deriva. Hoje o documento publica os
> **37** e conta a dívida em vez de escondê-la (`docs/protocol/ipc-unix-socket.md:44`: "**37
> métodos** … Destes, **18** ainda não são citados"). A faixa `:31-42` que este achado citava
> agora é a nota que explica por que o arquivo é gerado, não a tabela de dez.

**A-5. `docs/usage/interface.md:373-374` afirma que Aplicar "persiste o que está editado
para o perfil corrente". Não persiste** — `on_apply_draft` manda `profile.apply_draft` pelo
IPC e não escreve arquivo nenhum. O tooltip do próprio botão no glade diz a verdade. É a
linha que a documentação usa para dizer a ela onde o trabalho fica salvo. *Grau: lido-no-código.*
`app/actions/footer_actions.py:207-241, 452-524`; `gui/main.glade:3751-3754`.

> **FECHADO no commit de 13/08/2026 — e o endereço acima caducou junto.** `docs/usage/interface.md`
> não tem mais a frase: a seção "O rodapé" abre hoje com "os quatro botões **não** fazem a mesma
> coisa" e traz uma tabela com a coluna "o trabalho fica salvo?", em que o **Aplicar** responde
> "**não.** Nada é escrito em disco". O que este achado apontava como `:373-374` é essa tabela
> agora. O teste que a segura é `tests/unit/test_aplicar_nao_persiste.py`.

### 4.2 Os portões que aprovam o que deviam reprovar

**B-1. O portão que guarda todos os outros portões está cego no CI, e ele mesmo diz isso.**
`test_portoes_da_casa_estao_ligados_no_ci.py` deriva a lista de portões do bloco "Antes de
fechar qualquer leva" do arquivo de instruções da raiz — e esse arquivo está no `.gitignore`
(`.gitignore:90`) e não é rastreado. Num clone limpo, que é o que o `actions/checkout` traz,
os 5 testes **pulam**. Ele só protege na máquina dela. *Grau: medido*
(`git ls-files` do arquivo devolve vazio; num clone: `SKIPPED [5]`).

**B-2. O mesmo portão tem quatro furos de casamento, medidos.** A régua é substring no `run`
inteiro (`tests/unit/test_portoes_da_casa_estao_ligados_no_ci.py:159-171`), então passam
verde: um `echo` que só menciona `bash scripts/check_anonymity.sh`, um comentário de shell
dentro de `run: |`, `bash x.sh || true`, e `if: false` no passo. A mensagem de erro do
próprio portão diz "o portão tem de rodar, não de ser mencionado"
(`:196`) — e é justamente o que ele não verifica. *Grau: lido-no-código.*

**B-3. O portão de artefato de sistema sem dono não morde onde promete.** O caminho 2
("diretório copiado inteiro") dá cobertura em bloco a `assets/systemd` (8 arquivos),
`assets/modprobe`, `assets/modprobe.d` e aos três `assets/dkms/*` (36 arquivos). O token de
`assets/systemd` vem de `scripts/install-host-udev.sh:144`, onde o diretório é **só candidato
de busca num `for`**, não instalação. Uma unit `.service` nova e órfã entra na árvore
aprovada — o oposto exato do que o cabeçalho da seção promete. *Grau: medido com régua
própria, não com o portão* (reprodução da extração de tokens do próprio script contra a
árvore, somente leitura; ver a ressalva do crítico).

**B-4. O portão da promessa sem caminho acusa como não-ligada uma cura que está ligada há
quase um mês.** `integrations/kernel_cmdline.py::strip_quirks_token` está em `_SEM_CAMINHO_HOJE`
com o texto "só `tests/` a chama" e "O QUE A FECHA: o `uninstall.sh` chamar este caminho" — e o
`uninstall.sh:1166` já o chama, desde 19/07. Causa: a varredura de símbolos só olha `src/` e
os `.py` de `scripts/`; `install.sh` e `uninstall.sh` estão fora do território de produção,
embora a metade dos interruptores os nomeie explicitamente como portas. *Grau: medido.*
`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:734-742` × `uninstall.sh:1166` (chamada
nasceu em `b4589a1`, 19/07).

**B-5. O portão do mapa é o único vermelho — e no CI ele é `continue-on-error: true`.** Exit 1
com 18 falhas `sem-mordida` e 21 avisos. No CI ele não é portão, é relatório. O próprio
`portao_a_casa_sabe_e_o_produto_nao_faz.py:52-55` cita esse fato como a razão de ter nascido
teste e não script. *Grau: medido* (`.venv/bin/python scripts/check_paridade_transporte.py`,
exit 1, reconferido em 13/08).

> **O crítico completa, e o complemento é mais grave que o achado:** o `continue-on-error`
> engole as **seis** regras duras do script, não só a de sem-mordida — `main` tem um exit
> code só (`scripts/check_paridade_transporte.py:1093`). O comentário do CI
> (`.github/workflows/ci.yml:150-154`) justifica manter o passo dizendo que "as outras
> regras dele já estão verdes — e é justamente por elas que o passo precisa estar aqui
> hoje". A razão escrita para manter o passo é exatamente a única coisa que o passo não
> entrega.

**B-6. `mordida_provada_em` continua vazia em 293 de 293 — e isso não é o que parece.** Seis
arquivos de teste trazem no docstring o bloco `MORDIDA PROVADA (11/08/2026, src/ copiado para
fora da árvore…)` com o número exato de reprovações, e quatro dos seis avisos do portão
apontam exatamente para esses arquivos. **A prova existe e nunca foi transcrita para a coluna
que o portão lê.** Enquanto a coluna estiver zerada, a regra 11 é estruturalmente incapaz de
distinguir "mordida provada e não anotada" de "mordida nunca tentada". *Grau: medido.*

> **NOTA de 13/08/2026 — o número segue verdadeiro sobre `cc768d4` e caducou no mesmo dia.**
> O commit que publica este estudo é o que fecha o item: `docs/data/mapa-controles.csv` traz
> hoje **287 de 293** vazias, isto é, **seis preenchidas** (recontado com `csv.DictReader`):
> `gatilho.adaptativo`, `gatilho.esquerdo.adaptativo`, `gatilho.direito.adaptativo` e
> `luz.lightbar.cor`, as quatro com "11/08/2026 — já registrado no bloco MORDIDA PROVADA",
> mais `combinacao.rumble_simultaneo` e `vibracao.rumble.ff` com "13/08/2026 — mordida feita
> agora". A medição de origem fica registrada porque é ela que explica **por que** o passo
> existia; o estado de hoje é este.

**B-7. Os testes mordem — conferido por mutação, num clone, com a árvore dela intocada.**
Zerar `common[2:4]` só quando `conType == BT` derruba exatamente 5 (`5 failed, 11 passed`:
os quatro ids `[bt]` mais o caso que cruza os dois lados; os `[usb]` verdes). Arrancar o
keepalive neutro derruba 3. Arrancar o escape do Pango derruba 1. Nenhuma passou com a cura
fora. *Grau: medido.* Descoberta lateral: `test_uhid_gamepad.py` (128 nós), que o mapa cita
como mordida do rumble por force-feedback, é **cego a transporte** — passou verde na mesma
mutação.

**B-8. O buraco que sobra no portão do mapa: `teste_que_morde` emprestado de outra feature
passa.** Reescrevi `audio.jack.deteccao@pro` com grau forte, zero ensaios e um
`teste_que_morde` copiado de uma linha de preamp de áudio: o portão foi de 18 para 20
reprovações (dois `grau-sem-ensaio` nominais — a mutação que passava inteira em 12/08 hoje
morde), mas **nenhum `mordida-fantasma` foi emitido** para o teste irrelevante. As regras 1 e
2 conferem existência e coletabilidade, jamais relevância. *Grau: medido.*

**B-9. Peça órfã no mapa nunca reprova nada.** Um id de `peca` que não existe no SVG produz
um aviso em stderr e o processo devolve 0, inclusive no `--check`; e o
`check_paridade_transporte.py` não tem uma única regra sobre `peca`. Um desenho reeditado que
leve um id embora apaga o hover daquela linha em silêncio, com o CI verde. *Grau: medido*
(mutação `peca='dpad_up_ERRADO'` na minicópia: aviso seguido de `specs.html: atualizado`, exit 0).

> **FECHADO no commit de 13/08/2026:** `reprova_por_orfas()` nasceu em `scripts/gerar-mapa.py:178`,
> com o comentário `PECA-ORFA-01 (13/08/2026) — a órfã deixa de ser aviso e vira reprovação`, e é
> chamada antes da comparação de conteúdo (`:1020`). Zero órfãs nas 293 linhas de hoje.

**B-10. Só um portão ainda é cego a arquivo novo.** A regra da casa ("rode-os depois do
`git add`") vale hoje para o `scripts/check_anonymity.sh`, que usa `git grep`: provado num
clone — arquivo não rastreado com texto proibido passa verde, e depois do `git add` reprova.
`scripts/validar-acentuacao.py:872-907` e `scripts/validar-glifos.py:316-341` já foram curados
com `git ls-files --cached --others --exclude-standard` e enxergam arquivo novo. *Grau: medido.*

> **FECHADO no commit de 13/08/2026:** o `check_anonymity.sh` era o **último** portão cego, e a
> cura está no próprio arquivo, com o comentário `ANONIMATO-CEGO-A-ARQUIVO-NOVO-01 (13/08/2026)`
> em `scripts/check_anonymity.sh:71` — a busca por `git grep` virou a **lista** de
> `git ls-files --cached --others --exclude-standard` (`:82`), a mesma que a acentuação e os
> glifos já usavam. A regra da casa ("rode-os depois do `git add`") deixa de ter exceção.

**B-11. `CORRIDA-DO-PIPEFAIL-01` é bomba-relógio declarada, e o número confere.** Um produtor
canalizado para `grep -q` com `set -o pipefail`: o grep sai no primeiro casamento, o produtor
morre de SIGPIPE (141) e o pipe inteiro devolve 141 mesmo tendo achado o que procurava. A
máquina dela ganhou a corrida 200 vezes em 200; o runner do CI perdeu e acusou o
`scripts/doctor.sh` de não chamar uma função viva na linha 4493. A cura cobre 2 das 11
ocorrências; restam **exatamente nove** vulneráveis por construção (linhas 78, 856, 857, 922,
924, 954, 976, 985, 987 de `scripts/check_packaging_parity.sh`). *Grau: medido.*

> **FECHADO no commit de 13/08/2026:** as nove viraram here-string — contadas no diff staged
> (`git diff --cached scripts/check_packaging_parity.sh | grep -c '^+.*<<<'` → **9**).

**B-12. 23 testes escapam do ritual da casa.** `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`
não se chama `test_*` de propósito (leva ~2 min), então nem o `pytest -q` do ritual nem o
`pytest tests/unit` do job `lint-test` o coletam. Só o job `promessa-sem-caminho` o aponta por
caminho. O portão mais novo da casa está fora do ritual que a casa manda rodar. *Grau: medido.*

### 4.3 As respostas que já existem e ninguém sabe

**C-1. A pergunta em aberto nº 1 da canônica já foi respondida em 11/08, e a resposta mora numa
célula de CSV.** "O áudio de saída por Bluetooth sai no 0x32 ou no 0x39?" estava **mal feita**.
O descritor HID lido do aparelho dela declara **nove** reports de output por rádio, numa escada
de +64 B: `0x31`=77 B, `0x32`=141, `0x33`=205, `0x34`=269, `0x35`=333, `0x36`=397, `0x37`=461,
`0x38`=525, `0x39`=546 (teto); por cabo existe **um único** output, `0x02` de 47 B. O degrau se
escolhe pelo tamanho do payload. Três lugares de `docs/protocol/` continuam declarando a
contradição aberta e prescrevendo o ensaio já pago. O que continua aberto é mais estreito e mais
honesto: **o descritor prova aceitação, não efeito**. *Grau: lido-no-código*
(`docs/data/mapa-controles.csv:2`, campos `radio_report_id`, `radio_evidencia`,
`radio_ressalva` × `docs/protocol/dualsense-referencia-canonica.md:67, :401, :417, :1063` e
`docs/protocol/paridade-bluetooth-versus-cabo.md:168, :175`).

**C-2. A VOLTA do ensaio da lightbar já foi feita, com instrumento melhor, e o
`ONDE-PARAMOS` ainda a lista como item nº 1 da fila.** O `scripts/eliminacao.py` de hoje fecha
`luz.lightbar.cor@dualsense [radio]` como **É-A-CAUSA** pelo suspeito "a Steam ESCREVER no fio
durante a probe (contado por btmon, não inferido)", com com="não obedece" e sem="obedece". A
própria §1.3 do `ONDE-PARAMOS` cita os 98 contra 6 pacotes: **o documento contradiz a si mesmo
entre a §1.3 e a §2.1**. *Grau: medido* (ensaios `btmon-probe-suja` / `btmon-probe-limpa` em
`docs/data/ensaios.csv:49-50`, 12/08T23:50; texto stale em
`docs/process/2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md:391`).

**C-3. A página da pilha do Steam ficou velha por cinco minutos e nunca foi corrigida.** Ela
afirma que "por Bluetooth o Hefesto suprime a rota `hidraw` de forma incondicional e por rádio
o `sysfs` é a única rota que sobra — justamente a que perde para a Steam". O commit que
escreveu isso é `0c4164e`, 12/08 00:38:35; o commit `34210b8`, 12/08 00:43:32, acrescentou
`core/lightbar_gatilho.py` e passou a escrever um `0x31` cru por Bluetooth. A rota existe
desde então, venceu a Steam na mesa dela, e teve aceite "perfeito". Quem ler a página hoje
conclui o contrário. *Grau: lido-no-código*
(`docs/protocol/pilha-steam-input-xpad-sdl.md:1079` × `core/lightbar_gatilho.py:110-160` e
`core/backend_pydualsense.py:2454-2480`; datas por `git show -s --format=%ci`).

**C-4. O `GATILHO-DA-COR-01` não tem página nenhuma.** Uma varredura por esse identificador em
`docs/` devolve zero; o commit que criou o subsistema tocou zero arquivos de `docs/`. E ele
guarda as duas coisas que os próprios gatilhos da casa mandam promover a documento: um número
que a bancada pagou (os 1,5 s de `ATRASO_APOS_A_ULTIMA_CONEXAO_S`, fixados por ela em
`core/lightbar_gatilho.py:87` — "muito tempo. desce pra um segundo e meio") e uma vontade dela
que um mantenedor futuro "consertaria" de boa-fé ("em Modo Nativo e em Conexão Nativa o gatilho
NÃO age"). *Grau: lido-no-código.*

**C-5. O §2 da canônica declara "FONTE DESTA MÁQUINA" sobre 29 bytes que a fonte não nomeia.**
`struct dualsense_output_report_common` nomeia 18 dos 47 bytes; os outros 29 são `reserved2[27]`
(`common[10..36]`) e `reserved3[2]` (`common[39..40]`), e dentro deles moram **os dois blocos
de gatilho adaptativo inteiros** — a feature-assinatura do produto. A página do driver, que a
casa declara vencedora, já registra isso ("do ponto de vista do driver os gatilhos adaptativos
não têm nome: são 27 bytes de reserva"); a canônica não ganhou a nota datada correspondente.
E a tabela pula o byte 40 sem dizer se é lacuna ou intenção. *Grau: lido-no-código.*
`assets/dkms/hid-playstation/hid-playstation.c:319-349` ×
`docs/protocol/dualsense-referencia-canonica.md:172-201`.

**C-6. Os bits `flag0` 0x04 e 0x08 — os que autorizam os blocos de gatilho — não existem no
driver, e a canônica os apresenta sem grau.** O fonte define exatamente cinco bits de
`valid_flag0`: BIT(0), BIT(1), BIT(5), BIT(6), BIT(7). Não há BIT(2), BIT(3) nem BIT(4). O que
sustenta 0x04 e 0x08 hoje não é fonte, é **bancada**: `gatilho-lado-nao-esta-invertido` (só o
direito autorizado → R2 duro, L2 solto) e `gatilho-esq-radio-1216` (só o esquerdo → L2 duro nos
quatro, R2 solto como controle negativo). O grau honesto dessas células é MEDIDO AQUI.
*Grau: lido-no-código* (`assets/dkms/hid-playstation/hid-playstation.c:206-211`; ensaios em
`docs/data/ensaios.csv:36, :63, :67`).

**C-7. `weapon()` e `vibration()` continuam mandando os bytes que a própria canônica chama de
errados.** `weapon()` manda `PULSE_B` = 0x06, que a tabela do §4 decodifica como
Simple_Vibration (legado); `vibration()` manda `PULSE_A` = 0x22, decodificado como Bow (não
oficial). Os oficiais seriam 0x25 e 0x26. Nenhum commit desde 11/08 tocou nisso. A nota da casa
é explícita: nada autoriza trocar os bytes sem a mão dela no gatilho, porque os modos não
oficiais não validam parâmetros e ela pode estar gostando do que sente. *Grau: lido-no-código*
(`core/trigger_effects.py:461-466`, `:469-481`, `:128-129`).

### 4.4 O que pode quebrar a máquina de alguém

**D-1. Não existe guarda nenhuma contra `sudo ./install.sh` — a regra mais citada da casa
não é executável.** `acquire_sudo()` trata `EUID==0` como caso feliz e devolve 0 sem uma palavra.
Sob sudo o `HOME` vira `/root`: o `~/.local/bin`, o `.desktop` e as units `systemctl --user` vão
todos para `/root`, e o `.venv` — que é ancorado em `ROOT_DIR`, não em `HOME` — nasce na árvore
com dono root. O `uninstall.sh` **tem** teste que impede sugerir rodar a si mesmo sob sudo; o
install não tem equivalente nem guarda. *Grau: lido-no-código.*
`install.sh:434` (`[[ "${EUID:-$(id -u)}" -eq 0 ]] && return 0`), `:191, :194, :197, :2408-2486`;
`tests/unit/test_uninstall_simetrico_ao_install.py:310-329`.

**D-2. Um arquivo versionado e empacotado manda fazer exatamente o que a regra proíbe.**
`assets/dkms/hid-nintendo/README.md:204` manda rodar o instalador inteiro sob sudo, e ele viaja
para dentro do `.deb` (`scripts/build_deb.sh:271`), do PKGBUILD do Arch
(`packaging/arch/PKGBUILD:172`) e do RPM (`packaging/fedora/hefesto-dualsense4unix.spec:182`)
por `cp -a`. Chega à máquina de quem instala por pacote. *Grau: lido-no-código.*

**D-3. Dois workflows não rodam há treze dias e ninguém percebeu.** `anonymity-check.yml` e
`flatpak.yml` disparam só em `main`, e todo o trabalho desde 31/07 vive em
`restauro/inicio-da-sessao`. O último run de cada um é de 31/07. Consequência dupla: o portão
server-side de coautoria de IA nunca viu nenhum commit da série 0.9.x, e a validação do
manifesto Flatpak nunca rodou — mesmo assim o `release.yml` constrói e **publica** um bundle
`.flatpak`, porque o `guarda-ci` só pergunta pelo `ci.yml`. *Grau: medido*
(`gh run list --workflow=…`; gatilhos em `.github/workflows/anonymity-check.yml:12-15` e
`.github/workflows/flatpak.yml:4-5`).

**D-4. `origin/main` está em `670315d`, de 31/07 — 144 commits atrás.** Tudo desde então (o mapa
de canais, a bancada, os portões, as curas de rumble, lightbar e co-op, o install) vive só
nesta branch. É a causa mecânica de um defeito que todos os relatórios de 12/08 reclamaram: 14
das 16 worktrees de agente nasceram em `670315d`, e cada agente teve de dar reset antes de
trabalhar. *Grau: medido* (`git rev-list --count origin/main..HEAD` = 144, reconferido em 13/08).

**D-5. O job `pypi` ficou `skipped` na v0.9.4.2, e o motivo não é o guarda.** Medido hoje: o
repositório tem **zero** variáveis e **zero** environments, logo `vars.PYPI_PUBLISH` não existe
e o `environment: pypi` declarado no workflow também não existe do lado do GitHub. O workflow já
está pronto (`id-token: write`, action sem token). Falta ação dela em dois lugares: no pypi.org
(registrar o projeto e criar um Trusted Publisher OIDC apontando para este repositório,
workflow `release.yml`, environment `pypi`) e no GitHub (criar o environment e a variável).
*Grau: medido* (`gh api repos/:owner/:repo/actions/variables` → `total_count: 0`; idem
environments).

**D-6. Quatro versões estão no CHANGELOG e nunca viraram release publicada:** 0.9.0, 0.9.1 e
0.9.2 (têm tag, não têm release) e **0.9.4, que não tem nem tag** — apesar de ser a leva de
12/08, a maior do arquivo. Como o `github-release` extrai do CHANGELOG a seção da versão
publicada, as notas dessas quatro nunca chegaram a ninguém. *Grau: medido*
(`git tag -l 'v0.9*'` → v0.9.0, v0.9.1, v0.9.2, v0.9.3, v0.9.4.2 — sem v0.9.4; reconferido em 13/08).

**D-7. O que um PC novo não recebe está medido, e a boa notícia é maior que a má.** Os três
módulos DKMS e os onze parâmetros estão **inteiros no repositório** — `diff -rq` contra
`/usr/src/` não acusa **nenhum arquivo de conteúdo divergente** nos três módulos; ele acusa
só duas assimetrias de pasta já nomeadas como esperadas em
`docs/process/2026-08-11-O-DELTA-DA-MAQUINA-LIMPA-o-que-so-existe-nesta-maquina.md:76-79`
(`LICENSES/` só em `/usr/src`, `patch/` só em `assets/`). *Corrigido em 13/08 pelo crítico de
completude: a frase anterior dizia "não acusa um arquivo", mais forte que a fonte; o
`diff -rq` foi refeito no transporte, nos três módulos, e devolve exatamente essas duas
linhas por módulo.* O buraco de verdade é o BlueZ: esta máquina roda 5.86 por backport local,
um PC novo roda 5.72, e o instalador **não consegue mais entregar o 5.86 nem aqui** porque o
cache de `.deb` que o passo 3f lê não existe. Num PC novo o `doctor` reprova logo após o
install. Segundo buraco: o applet COSMIC — que é o que aparece no painel dela — depende de um
`cargo` que ninguém instala. *Grau: lido-no-documento para o BlueZ e o applet* (as medições de
estado de máquina são de 11/08 e não foram reconferidas), *medido em 13/08 para o `diff -rq`*.

### 4.5 O que a casa sabe e o produto não faz

**E-1. O histórico de perfis grava sozinho e nunca chega à interface.** Toda gravação arquiva a
versão anterior num `.historico/<slug>/` dentro do diretório de perfis, guardando 10 versões por
perfil. As únicas portas são `hefesto profile historico` e `profile restore`; em `app/` não há
uma referência a `listar_historico`/`restaurar_do_historico` (varredura em 13/08: zero). A rede
de segurança contra o gesto que estraga um perfil — a mesma coisa que os quatro diálogos de
confirmação existem para evitar — só se alcança por terminal. *Grau: lido-no-código.*
`profiles/loader.py:635-671`; `cli/cmd_profile.py:233-296`.

**E-2. Seis interruptores de ambiente que o produto promete e nada liga.** O mais desconfortável:
`install.sh` **tem** a flag `--keep-dualsense-mic`, e ela só faz `WITH_WIREPLUMBER_FIX=0` — a env
de intenção nunca é escrita, e a única ocorrência no instalador é um comentário mandando a
operadora exportá-la à mão. Quem instala com essa flag continua sendo alarmado pelo doctor e
aconselhado a rodar `doctor --fix`, que desfaz a escolha que ela acabou de fazer. Os outros
cinco: os plugins (decisão dela), o microfone por BT, as notificações de desktop, os avisos de
sistema (o daemon calcula os avisos, escreve no log e **descarta** a notificação) e as métricas.
*Grau: lido-no-código*, registro em
`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:351-437`.

**E-3. O restauro de bonds continua sem gatilho.** `install.sh:1707` diz, no próprio comentário,
que "restauração é MANUAL". Isso contradiz a decisão dela de 08/08 ("restauro tem de ser
automático; manual com sudo não é produto"), e a sprint `BONDS-QUE-SOBREVIVEM-01` segue aberta
desde 04/08. As duas posições estão escritas e nenhuma foi retirada. *Grau: lido-no-código*
(correção do crítico: ler um comentário é leitura de fonte, não medição — e o comentário
declara a RAZÃO técnica da escolha, "automática poderia restaurar chave que o controle
rotacionou → loop de auth", o que muda o achado de "dívida esquecida" para "decisão escrita que
contradiz a decisão dela").

**E-4. `NINTENDO-VARIANT-01`: o produto escreve a marca e ninguém a lê.** A variável
`HEFESTO_CONTROLLER_VARIANT` é gravada por **oito** regras de
`assets/84-nintendo-pro-variant.rules` (`:55-68`) e uma varredura em `src/` devolve **zero**
(reconferido em 13/08 — o estudo original dizia seis regras). *Grau: lido-no-código.*

**E-5. `mic.button_toggles_system` é um campo de perfil que nenhuma das duas frentes escreve.**
Modelado no `Profile` (`profiles/schema.py:401`) e no `DraftConfig` (`app/draft_config.py:167`),
sem widget nenhum no glade (varredura em `gui/main.glade`: zero); e como o `to_ipc_dict` só
emite a seção quando `mic.dirty`, e nada liga `dirty`, ela nunca sai da janela. No CLI, `hefesto
mic` mexe no mudo do firmware, não neste flag. Só editando o JSON à mão. *Grau: lido-no-código.*

**E-6. Os plugins (ADR-017) são a única API pública que o projeto promete a terceiros e não têm
uma linha de janela** — `plugin.list` e `plugin.reload` só existem no CLI, e o interruptor que os
liga é uma env que nada escreve. *Grau: medido* (cruzamento dos 37 métodos contra `app/` e `cli/`).

### 4.6 A tela que a documentação publica

> **Ressalva do crítico, que vale para a seção inteira:** as fotos publicadas em
> `docs/usage/assets/` são de **11/08 23:06**, e depois delas três commits tocaram `app/` e
> `gui/` (`f1279a1`, `0b010bd`, `973c92c`) antes de a tag `v0.9.4.2` ser cortada em `cc768d4`,
> 13/08 02:26. A regra da casa manda re-fotografar antes de gerar release. **F-1 e F-2 criticam
> o conteúdo das fotos e não perguntam de que versão elas são. Não são da versão publicada.**
> (Reconferido no transporte, 13/08: os três commits e as datas conferem.)

**F-1. A foto da aba Perfis que a documentação publica é uma casca vazia — e é a aba mais
editada.** `scripts/gui-captura/retratar_abas.py` monta o glade e injeta em código só a aba
Início, a No jogo, o card do Status e os seletores de modo de gatilho (`:505-508`). A aba Perfis
tem **em código** o seletor "Aplica a", a seção "Modo" inteira e a caixinha do Steam Input —
nada disso é montado, então a foto sai com "Aplica a:" sem um botão e a moldura "Modo" oca. É
literalmente o defeito de que o próprio docstring do script acusa o antecessor ("mostra a janela
VAZIA: combos sem itens"), reproduzido no script que deveria ser a cura. *Grau: medido* (leitura
do PNG; `scripts/gui-captura/retratar_abas.py:485-530` ×
`app/actions/profiles_actions.py:977-1067`; `docs/usage/interface.md:246-248`).

**F-2. O diálogo mais novo da aba Perfis nunca foi visto por ninguém.**
`confirm_downgrade_match_to_manual` (`app/gui_dialogs.py:508`) nasceu em 10/08 e é o par exato do
que já é fotografado; `scripts/gui-captura/retratar_dialogos.py` continua com as mesmas cinco
cenas de três funções, e `docs/usage/interface.md:265` continua dizendo "Três perguntas existem"
quando são quatro. A janela tem ~12 estados de diálogo e 5 fotografados. PROVA-DE-TELA-01 está
em aberto para o diálogo que decide se um perfil de jogo vira "só manual". *Grau: medido para os
5 fotografados e para a frase de `interface.md`; **inferido** para o "~12 estados" — o til é a
confissão de que ninguém contou, e a régua desta casa é "conte estados, não diálogos".*

**F-3. P1 das três decisões da caixinha (06/08) não foi cumprido, e não há nota datada dizendo que
caducou.** A decisão era: "o mesmo arquivo passa a se chamar **lista de exceções** nas três abas", e
o botão da aba Sistema deixa de ser "Este jogo não funciona". Hoje a aba Sistema ainda tem "Este
jogo não funciona", a caixinha da aba Perfis se chama "Esconder o controle físico neste jogo", e
"lista de exceções" só aparece em toast montado em Python. **Três vocabulários para o mesmo
arquivo** — o `steam_input_apps.txt` do XDG config —, que é exatamente a confusão que o P1
existia para fechar. P2 e P3 foram cumpridos. *Grau: lido-no-código.*

**F-4. 168 das 293 linhas do mapa não acendem nada no hover** (45 no DualSense, 60 no Pro, 63 no
SN30): `peca` vazia, logo `alvo` vazio. O mecanismo que faz o mapa ser mapa e não planilha está
desligado em 57% das linhas. E o DualSense tem **zero** `data-evdev` no desenho, então a coluna
`evdev` só existe de fato para o Pro (14) e o SN30 (13). *Grau: medido* (reconferido em 13/08).

**F-5. O gerador e o portão discordam sobre o que é uma célula muda.** O desenho chama de muda a
célula com `aceita` vazio (**193**, o número que o rodapé do `specs.html` publica); o censo chama
de muda a com `aciona` vazio (**185**). A diferença são exatamente 8 células — e entre elas está
`combinacao.cabo_e_radio.saida@dualsense` nos dois lados, com `aciona=sim` e `confianca=medido`
(a bancada de 12/08 à noite). **O resultado da mesa dela está invisível no símbolo do mapa**,
pintado como "ninguém respondeu". *Grau: medido.*

**F-6. O caderno de eliminação tem hoje zero suspeitos inocentados.** Dos 586 lados, 567 são
`nunca-investigado`, 13 `inconclusivo` e 6 `e-a-causa` — nenhum `nao-e-a-causa`. O rodapé publicado
imprime "0 suspeito(s) já inocentado(s)" logo abaixo da prosa que celebra "quatro dos cinco canais"
inocentados no estudo da lightbar. *Grau: medido* (a frase do rodapé foi reconferida no
`specs.html` commitado, 13/08).

**F-7. O SVG do 8BitDo tem o id `led-jogador` duplicado** — `assets/control-svg/8bitdo-sn30-pro.svg`
nas linhas 229 e 252. Depois do prefixo do `svg_inline` os dois viram `sn30__led-jogador`, e
`getElementById` devolve só o primeiro — o segundo grupo nunca acende. *Grau: medido* (reconferido
em 13/08).

### 4.7 Achados de menor peso, que valem para quem chegar

- **A quinta lâmpada dos externos é o LED HOME**, não um quinto jogador: o driver registra
  `:blue:player-5` sob o rótulo `home_led:`, e escrever nele dispara `JC_SUBCMD_SET_HOME_LIGHT`
  (0x38), um programa de PWM com escala 0..15 — não o `0x30` dos player LEDs. O
  `core/external_leds.py` o acende como se fosse a quinta lâmpada. *Lido-no-código.*
- **D-Bus não é canal de saída para o controle em lugar nenhum do código**, apesar de figurar no
  domínio do portão de paridade; as três linhas do CSV que o usam são todas do 8BitDo e apontam
  para documento ou script de shell. *Medido* (reconferido em 13/08: `identidade.pareamento`,
  `plataforma.transporte_radio` e `plataforma.vigia_zumbi`, todas `@sn30`).
- **A janela de confirmação do keepalive é reaberta por qualquer mudança do report**, não só de
  vibração: um perfil que troque a cor ou o gatilho reabre por 2,0 s a janela em que o keepalive
  volta a zerar `common[2]`/`common[3]`. O comentário de 60 linhas ali só discute o caso do rumble.
  *Lido-no-código* (`core/backend_pydualsense.py:611-612` e `:641-648`).
- **`hefesto test trigger|led|rumble` só sabe falar com todos** — nenhum aceita `--uniq` (varredura
  em `cli/cmd_test.py`, 13/08: a palavra não aparece no arquivo). Com quatro DualSense na mesa, a
  janela consegue mirar um e o comando de bancada não. *Lido-no-código.*
- **O número de 14.105 ocorrências de `hidraw_broker_hidden` em sete dias está cravado num
  docstring marcado MEDIDO e não há script versionado que o reproduza.** *Lido-no-código*
  (`daemon/battery_journal.py:55`).
- **Régua de teatro aplicada e reportada com honestidade:** ~7775 funções `test*`, 95 sem
  `assert`/`raises`/`fail` no próprio corpo — e a régua **superestima**: a amostra que conferi ou
  afirma "não explode" ou delega a asserção a um helper. Não achei teatro por esta régua.
  *Medido com régua própria, não publicada — uma segunda régua, um `grep -rhoE` por definição de
  função `test` em `tests/`, devolve 7800. Enquanto o script não for versionado, o número não é
  reprodutível e o grau honesto é `medido com régua própria`.*
- **O piso de coleta do CI é 5100 contra 9130 reais** (`.github/workflows/ci.yml:334`) — 44% de
  folga, na qual cabe um módulo inteiro sumindo calado. *Medido.*

---

## 5. O que caducou desde 12/08

1. **"A VOLTA do ensaio da lightbar está aberta"** — fechada na mesma noite, por btmon. Ver C-2.
2. **"15 dos 37 métodos IPC não documentados"** (dossiê 12/08) → depois 17 (nota de lacunas) →
   **18** hoje, contado por script. Nem o código nem o documento receberam commit desde então. Os
   três números foram escritos à mão; passa a valer o script.
3. **"9007 testes coletados"** → **9130** hoje, mais 23 que a coleta padrão não vê. E o número do
   ritual da casa ("6645 verdes em 01/08") é o único que nunca foi atualizado.
4. **"ci.yml tem 15 jobs"** (relatório recuperado) → **18 declarados** (reconferido em 13/08) e
   **27 execuções** por causa das quatro matrizes; o job `promessa-sem-caminho` entrou e não está
   na lista deles.
5. **"O portão da promessa acusa 33 símbolos"** (docstring de 12/08) → o registro tem **23**
   entradas em `_SEM_CAMINHO_HOJE`; os outros 10 estão em `_NAO_E_PROMESSA` (reconferido por AST
   em 13/08). Ler o docstring sozinho leva a crer que são 33 dívidas.
6. **"Portões são cegos a arquivo novo"** como regra geral → em `cc768d4` valia para **um só**,
   e o commit de 13/08 curou esse último: hoje vale para **nenhum**. Ver B-10. A regra do
   `CLAUDE.md` ("rode-os depois do `git add`") continua boa prática — o `git add` também é o que
   torna o inventário estável —, mas deixou de ser a diferença entre reprovar e não reprovar.
7. **"`ruff check .` acusa 2 E402 em `scripts/gui-captura/`"** → hoje os dois comandos saem limpos.
   A diferença virou de **alcance** (27 `.py` a mais, entre eles os próprios oito portões, lintados
   só pelo job `pre-commit`), não de resultado.
8. **"A tag v0.9.4.2 subiu e não disparou release nenhum"** → curado: o gatilho aceita quatro
   componentes e o run concluiu success com seis artefatos. O `pypi` continua `skipped`, e por outro
   motivo (D-5).
9. **"O CI está vermelho há dois dias"** → verde. Os três defeitos de 13/08 (`UHID-DO-RUNNER-01`,
   `MARKUP-SEM-GLIB-01`, `FOTO-QUE-ESPERA-01`) estão os três na árvore, e os três eram do
   **instrumento**, nenhum do produto.
10. **"A leva da noite de 12/08 não está commitada"** → está (`0b010bd`), e `git status` devolve
    vazio. Não há leva a caçar.
11. **"O `[Unreleased]` do CHANGELOG não versionado"** → vazio; a 0.9.4.2 foi cortada e publicada.
    O que passou a valer no lugar é pior: quatro versões sem release (D-6).
12. **"O relatório da perna morta não foi commitado"** → entrou: `scripts/identidade_do_vpad.py`
    existe hoje (`0b010bd`). Quem reabrir aquele assunto parte da árvore, não do diff.
13. **"A frase 'o Hefesto sai da frente' está em ~25 lugares, refutada pela metade"** → hoje a
    varredura acha 8, e todas são notas datadas que declaram a frase refutada. Nenhuma é texto de
    produto.
14. **Ponteiros que derivaram em menos de seis horas:** as citações de `docs/usage/interface.md`
    (o commit `0b010bd` inseriu 32 linhas), as de `app/actions/profiles_actions.py`,
    `app/actions/status_actions.py` e `app/widgets/painel_no_jogo.py` (o `973c92c` trocou o escape do Pango
    nos três) e as da canônica para `core/backend_pydualsense.py` (o laço de áudio está em
    `:930-940`, não em `:780-790`). **As afirmações continuam verdadeiras; só os endereços
    apodreceram** — e nesta casa uma linha que não abre vale o mesmo que nenhuma.
15. **A justificativa da sprint E-4 (`BITS-DE-AUTORIZAÇÃO-01`)** dizia que o rumble "continua sem
    causa provada". Tem causa provada desde 11/08 à noite, por dose-resposta. A pergunta de protocolo
    sobrevive; o argumento não.

---

## 6. O que está aberto

### 6.1 Trabalho de assistente (não precisa da mão dela)

Ordenado por "o que impede a próxima regressão de voltar".

> **LEIA ISTO ANTES DE ESCOLHER UM ITEM — 13/08/2026.** Esta tabela foi medida contra
> `cc768d4` de manhã e **o mesmo commit que a publica fechou sete dos quinze**: os itens
> **1, 4, 6, 9, 12, 13 e 14**, marcados `FECHADO` abaixo, conferidos um a um no diff
> staged. Não é desonestidade do estudo — ele se declara instantâneo de `cc768d4` — é que
> a leva da tarde foi **pagar exatamente o que ele mediu de manhã**. O que continua aberto
> são os oito restantes. A tabela fica inteira, com os fechados marcados, porque apagar a
> linha apagaria o motivo de o trabalho ter sido feito.

| # | o quê | custo |
| ---: | --- | ---: |
| 1 | **`FECHADO` (13/08).** Transcrever as seis mordidas já provadas** para `mordida_provada_em` (a prova está no docstring de seis arquivos de teste, datada 11/08) — ou fazer o portão ler o bloco `MORDIDA PROVADA` do arquivo apontado por `teste_que_morde`. | 60–90 min |
| 2 | **Fechar os quatro furos do P0**: casar por linha não-comentada, com o script em posição de comando, e reprovar `\|\| true` / `\|\| :`. Provar por mutação nos quatro. | 60 min |
| 3 | **Fechar o vácuo do P1**: exigir que o token de diretório apareça num comando de cópia/instalação, não em qualquer linha. Teste que largue um órfão numa cópia da árvore real e exija reprovação. Custo do conserto medido em 12/08: zero, os 8 arquivos já são citados por nome. | 60 min |
| 4 | **`FECHADO` (13/08, +679/−42).** Criticar e commitar o diff do guia v2** (+552/−41, aplica limpo, nunca commitado). Antes: apontar a referência morta a um script de exemplo chamado `pintar_por_rota` — que não existe nesta árvore — para um exemplo que existe no produto, e conferir que cada nota datada tem linha em `docs/data/ensaios.csv`. **Cuidado: existe um rascunho rival ao lado que a crítica de 12/08 demoliu** — aplicá-lo reintroduz quatro defeitos, entre eles um fato já substituído. | 90 min |
| 5 | **Consertar o `ONDE-PARAMOS`**: marcar o item 1 como fechado com o É-A-CAUSA do caderno, e trazer as famílias B/C/D/E do índice de 11/08 (21 sprints hoje invisíveis) para a página. | 45 min |
| 6 | **`FECHADO` (13/08).** Substituir `MSG_RAW_COM_DAEMON`** (`cli/cmd_test.py:36-47`): a recusa continua certa, o mecanismo citado ("o keepalive sobrescreve em menos de 0,5 s") caducou. É texto que ela lê. | 15 min |
| 7 | **Corrigir a divergência 193 × 185** entre o desenho e o censo, e fazer o símbolo do mapa mostrar as 8 células com `aciona` respondido e `aceita` vazio. | 45 min |
| 8 | **Acrescentar `if`, `while`, `until` e `!` às aberturas do P2** e ancorar `_carona_tem_guarda` na linha da chamada. Portão que acusa quem está certo morre em uma semana. | 30 min |
| 9 | **`FECHADO` (13/08).** Fazer o `--check` do gerador reprovar peça órfã (hoje avisa e sai 0). | 30 min |
| 10 | **Declarar o que o `doctor --fix` faz no `.deb`** — hoje ele compila dois módulos DKMS e habilita um socket dizendo "regras udev reaplicadas". | 30 min |
| 11 | **Excluir os diretórios de build do empacotamento do laço do P3** (18 GB varridos por chamada, e um binário de build pode calar o portão). | 20 min |
| 12 | **`FECHADO` (13/08).** Reescrever a tabela do IPC como arquivo gerado** a partir do dicionário `_handlers`, como o `specs.html` é gerado do CSV. A deriva chegou a 18 de 37 e o número já errou três vezes. | 90 min |
| 13 | **`FECHADO` (13/08).** Montar a aba Perfis em código no `scripts/gui-captura/retratar_abas.py`** (o seletor "Aplica a", a seção Modo, a caixinha), como já se faz com a Início e a No jogo. | 60 min |
| 14 | **`FECHADO` (13/08).** Curar as nove ocorrências restantes do padrão de pipe com `grep -q`** em `scripts/check_packaging_parity.sh`, por here-string. | 45 min |
| 15 | **Fechar as três lacunas do estudo de 12/08** que continuam abertas: `profiles/`, `daemon/subsystems/coop.py`, `daemon/subsystems/identity.py` e `daemon/subsystems/external_mask.py` lidos no fonte; a camada de entrada e detecção de janela; as ADRs 002/016/017 e o i18n (338 msgid em pt_BR contra 349 em en, assimetria de 11 sem explicação). | horas |

### 6.2 Decisão ou mão dela

**Bancada, com o controle na mão:**

| o quê | custo | o que decide |
| --- | ---: | --- |
| **Ver a cura da lightbar acender pelo PRODUTO, com a Steam viva de propósito** — Steam aberta, quatro controles subindo juntos, olhar se os quatro pegam cor e número. | **2 min** | Converte `luz.lightbar.cor` de MONTOU para O APARELHO OBEDECEU. É a maior cura da semana e ninguém a viu acender. Se algum ficar para trás, o rearme não está esperando a sequência sossegar — e aí é código. |
| **O LED do mudo (AUDIO-OWNER-01)**: daemon vivo, um DualSense no cabo, apertar o botão do microfone. | 3 min | Prova no olho dela que o kernel muta e acende, e que o nosso report apagava a luz sem desmutar. |
| **O elemento específico do gatilho, um bit por vez** (`flag0` 0x04 e 0x08). O instrumento existe e nunca produziu um ensaio: `scripts/ensaio_rumble_um_bit_por_vez.py`. | 30–45 min | É onde o rumble estava na manhã de 11/08 — e o rumble só encolheu o produto depois de responder isso. |
| **Os sete modos de gatilho que nunca foram tocados** (os onze ensaios de gatilho do caderno são todos `Rigid`). | 30 min | Sete oitavos da feature nunca foram ao plástico. |
| **O ensaio que decide se `_suppress_leds` pode ser levantado** — reenviar, a 2 Hz por 20 s, um report com o bit de SETUP da lightbar ligado, num controle só. | **5 min, com preço** | Se a medição de 22/07 estiver certa, a barra trava apagada até desligar o controle no botão. Se não travar, aquela medição (feita com a Steam viva, o que contamina retroativamente) caducou e a rota do fluxo inteiro volta. |
| **O report estreito dentro da janela de ~3,4 s** — o risco que a cura da rota introduziu e que ninguém mediu. | 3 min | Se travar, a cura precisa de portão de janela. |
| **`E-3 ESPELHO-DA-STEAM-01`**: com a Steam aberta e um jogo na frente, ler o ambiente do processo do jogo e procurar as variáveis `SDL_`. | **30 s** | Destrava ou arquiva a sprint D-4. |
| **`E-6`: o anel de Home do 8BitDo acende?** | 5 min | Decide metade de `A-QUINTA-LÂMPADA-01` — e se corrigir o `write_player_number` é conserto ou regressão. |
| **A captura de Bluetooth** (a fixture `hid_capture_bt.bin`, que ainda não existe em `tests/fixtures/`), devendo desde 31/07. O gravador está consertado; falta o modo guiado com as mãos dela. | 20 min | Fixture que a suíte usa. |
| **O ciclo `uninstall → install` numa máquina limpa**, e os três DKMS contra outro kernel, e o produto com Secure Boot ligado. | horas | É o critério do `1.0.0`. Com a chave MOK não enrolada, o kernel recusa o `.ko` e **não volta ao in-tree** — a máquina fica pior do que sem a cura. |

**Decisão de produto:**

- **A aba Rumble promete endereço para as duas metades e entrega para uma só.**
  **SUBSTITUÍDO em 13/08/2026** — a versão anterior desta linha dizia "acrescentar `rumble` ao
  `OutputSpec` (mecanismo novo no backend)", e as duas metades da frase caíram: o pulso já mira
  (ver A-3), e `set_rumble_for` já existe. O `OutputSpec` **não deve** ganhar campo de rumble, e
  isso é decisão e não esquecimento: ele é o mapa do que **fica**, e rumble é transitório por
  desenho (`core/backend_pydualsense.py:2845`, "NÃO entra em `_desired`"). O que sobra para
  decidir é o que fazer com a **intensidade**, que é global de verdade: dar `uniq` a
  `rumble.policy_set`, ou a aba **dizer** que a intensidade vale para todos — e essa frase já
  existe no produto, basta passar `com_endereco=False`
  (`app/actions/status_actions.py:1857-1861` e `:1959-1962`). A regra da casa é informar antes
  de corrigir o que ela escolheu. **5 min para decidir.** O desenho das duas saídas está em
  [MESA-CHEIA-05](../sprints/2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md).
- **O P1 da caixinha ainda vale?** Hoje há três vocabulários para o mesmo arquivo e nenhuma nota
  datada dizendo qual venceu. **5 min.**
- **O histórico de perfis vira tela** (uma linha "o que este perfil era ontem", com Restaurar), ou
  fica ferramenta de terminal? É a única volta que existe para um Salvar que estragou um perfil.
  **5 min.**
- **O arquivo de instruções da raiz está fora do git.** A opção "versiona o arquivo" **está
  proibida por escrito** e produziria CI vermelho — ver a contradição que o crítico levantou. O que
  sobra é mover a lista de portões para um arquivo versionado e o arquivo de instruções apontar
  para ele. Hoje o portão que guarda os portões pula no CI. **5 min.**
- **O `pypi` vale a pena?** Ligar `PYPI_PUBLISH` é irreversível por versão, e o wheel sozinho não
  instala nada do que faz o produto funcionar (udev, DKMS, broker, units). É distribuição ou vitrine?
  **10 min.**
- **Os workflows `flatpak.yml` e `anonymity-check.yml` passam a disparar em `restauro/**` e em tags?**
  Se sim, é uma linha em cada arquivo — **e o passo "Auditar arquivos de instrucao IA no tree"
  (`.github/workflows/anonymity-check.yml:142-171`) começa a valer nesta branch, o que amarra esta
  decisão à anterior.** Se não, o bundle publicado sai sem manifesto validado, e isso merece estar
  escrito ao lado do `guarda-ci`. **5 min.**
- **Quando `restauro/inicio-da-sessao` volta para `main`?** Hoje o branch padrão do repositório
  público não tem nada desde 31/07. **Decisão: minutos. Merge: dela.**
- **Quem enche o cache do backport do BlueZ?** É o único FAIL que um PC novo leva no caminho `native`.
  As saídas (o install construir os `.deb`; hospedá-los; ou aceitar 5.72 e mudar a faixa do doctor)
  são todas decisão de produto.
- **Plugins de terceiros e notificações nascem ligados ou desligados?** O portão sugere decidir as
  notificações de desktop e os avisos de sistema **juntos**, por um interruptor só de "me avise na
  tela" — dois interruptores para a mesma pergunta é superfície a mais na janela dela.
- **O restauro automático de bonds volta a ser desenhado, ou a decisão de 04/08 vence?** As duas
  posições estão escritas, nenhuma foi retirada, a sprint segue aberta.
- **As 21 sprints das famílias B/C/D/E continuam valendo, ou ganham nota datada?** As B são notas
  datadas de decisão medida, e apagá-las é o que a regra da casa proíbe.
- **A renumeração de jogador no meio da partida**: medido em 12/08 que quando um controle cai o
  produto renumera quem fica e devolve quando ele volta. Reversível, simétrico, de propósito — e num
  co-op em andamento isso troca quem é quem no meio do jogo.
- **A senha dela em cinco commits públicos desde 22/05.** Só ela pode trocar.

---

## 7. As armadilhas desta casa

1. **O instrumento mente mais que o produto.** Três medições falsas num único dia. Valide a régua
   contra contagem independente antes de acreditar nela.
2. **Medir contra a biblioteca errada produz alarme convincente e falso.** Todo instrumento tem de
   declarar qual biblioteca está usando.
3. **Sob Xvfb não há gerenciador de janelas** — uma `Gtk.Window` fica 1x1 para sempre, e widget sem
   alocação mede 1x1, então qualquer medida tirada dele passa com qualquer desenho. Use
   `Gtk.OffscreenWindow`, e **espere** a condição em vez de fotografar num instante (`FOTO-QUE-ESPERA-01`,
   13/08: a mesma SHA passou às 05:00 e reprovou às 05:11).
4. **O dublê não imita o produto.** Nenhum stub de `gi` da suíte define `markup_escape_text` — foi
   por isso que `utils/markup.py` nasceu. `hasattr` não teria resolvido: os testes afirmam que o
   escape acontece.
5. **O número escrito à mão apodrece; só o número que sai de um script sobrevive.** Os métodos IPC
   não documentados já foram 15, 17 e 18 contra o mesmo par de arquivos sem commit no meio.
6. **A citação `arquivo:linha` apodrece mais rápido do que se imagina** — seis horas, no caso de
   `docs/usage/interface.md`. Confira antes de reusar; a afirmação pode estar certa e o endereço
   errado. (O transporte desta página para o repositório, em 13/08, corrigiu três endereços que já
   tinham derivado — ver o cabeçalho.)
7. **Portões são cegos a arquivo novo** — hoje só o `scripts/check_anonymity.sh`, mas rodar depois do
   `git add` não custa nada.
8. **`grep -q` num pipe com `pipefail` é uma corrida**, e ela é ganha na máquina rápida e perdida no
   runner. O portão acusa um defeito que não existe.
9. **O documento de entrada erra do jeito mais caro: mandando trabalhar no lugar errado.** O
   `ONDE-PARAMOS` lista como aberto um item que a mesma página prova fechado.
10. **Um `0x31` cru com `seq 0` é descartado pelo firmware — e o sintoma é o pior de todos:** o log
    diz "escrito" e a barra não muda. Escreva pelo `writeReport` do handle, nunca por um `os.open`
    avulso.
11. **Antes de culpar o sistema, procure o produto no journal do sistema.** Quem tirava a permissão
    do `/dev/hidrawN` não era o `systemd-logind`: era o broker do próprio produto, de propósito. Duas
    horas teriam sido poupadas por um filtro de `hidraw` no journal.
12. **Controle negativo não é prova de obediência.** Numa rodada, "o lado não autorizado ficou solto"
    foi anotado por engano como prova de que o produto obedeceu. Ela pegou o erro.
13. **Hipótese tem de explicar o que já funcionava.** A hipótese grande de 11/08 — "a rota `hidraw`
    suprimida por BT é a causa-raiz compartilhada de rumble, gatilho e luz" — é **falsa**:
    `_suppress_leds` derruba só lightbar e player LED; `common[2..3]` e os blocos de gatilho saem
    sempre.

---

## Nota sobre este documento

O material recebido cobre sete dimensões (daemon, GUI e perfis, install e release, testes e
portões, protocolo, o que está aberto, e o sistema do `specs.html`); o último bloco chegou truncado
no fim, e as afirmações dele publicadas aqui foram **recontadas por script contra a árvore**
antes de entrarem — 293 linhas, 99/97/97 por controle, 0 de 293 com `mordida_provada_em` (**6 de
293** no commit que publica isto — ver a nota do B-6), 40 com
`teste_que_morde`, 168 sem `peca`, `evdev` só em pro (14) e sn30 (13), 193 células com `aceita`
vazio contra 185 com `aciona` vazio, 77 ensaios cobrindo 12 linhas, todas `@dualsense`.

E o que ele **não** cobre está listado, com nome e tamanho, em
[o que ficou de fora — o crítico de completude](2026-08-13-o-que-ficou-de-fora-o-critico-de-completude.md).
Quem for agir a partir desta página deve ler aquela primeiro: o veredicto dele é que o que falta
aqui é escopo, não veracidade — e escopo faltando é exatamente o que faz alguém concluir que uma
área foi auditada quando ninguém a abriu.
