# RADAR-01 — as três superfícies que ninguém nunca olhou

- **Status:** **PARCIAL — a E4 está ENTREGUE EM CÓDIGO (é portão, e portão se
  valida sozinho); as E1, E2 e E3 seguem ABERTAS, e o D1 continua ABERTO por
  medição do próprio teste.** Remarcada em 09/08/2026: o portão de vocabulário
  das quatro superfícies entrou em `c10adaf` (01/08/2026). **Rótulo anterior:
  "ABERTA — documento de MEDIÇÃO. Na rodada de abertura (31/07, madrugada)
  nenhuma linha de código, teste ou configuração foi tocada. Na rodada de 31/07
  06h entrou uma mudança de código, e só ela: o cabeçalho de
  `compact_window.py`"**, preservado aqui integralmente. Ver a nota datada no
  fim
- **O que falta ela validar, em uma linha:** abrir o applet do painel e a
  bandeja e dizer se eles falam a mesma língua da janela — é a única superfície
  que ela usa todo dia e que nunca teve o olho dela por cima
- **Prioridade:** ALTA — não pelo tamanho do conserto, que ainda não sabemos
  qual é, mas porque a superfície que ela usa TODO DIA no painel nunca entrou em
  índice nenhum, e o custo disso é exatamente o que está escrito abaixo
- **Aberta em:** 31/07/2026, depois da auditoria de áreas do HEAD `7bd0cb7`, que
  achou três superfícies de interface fora de todo levantamento
- **Sucede:** as cinco sprints de janela —
  [PALAVRA-01](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md),
  [LEGIBILIDADE-01](2026-07-25-LEGIBILIDADE-01-texto-legivel-alvo-clicavel.md),
  [VÃO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md),
  [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) e
  [STATUS-SIMETRIA-02](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md).
  As cinco mediram a MESMA superfície: a janela GTK. Esta pega as outras três
- **Relacionada:**
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
  (a folha de seis perguntas, cujo escopo é a janela e não as quatro
  superfícies — é o buraco que a E4 fecha) e
  [DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md)
  (que não cobre nenhuma das três: conferido por grep, zero menções a
  `compact`, `bandeja`, `tray` ou `applet`)
- **Identificador que ela paga:** `SEGUNDA-JANELA-01`, prometido desde 29/07 e
  nunca escrito

## Esta sprint MEDE. O conserto vem depois, e com o aval dela

Está dito com todas as letras na abertura porque é a diferença entre esta
sprint e as cinco que vieram antes: **as entregas aqui são de radar, não de
cura.** Nenhuma delas muda um pixel do que ela vê antes de ela decidir.

E o custo de nunca ter medido é este, e é concreto: **ninguém neste projeto
sabia, até hoje, se o applet contradiz a janela na frente dela.** Duas
superfícies mostram o mesmo estado do mesmo daemon com dois códigos diferentes,
em duas linguagens diferentes, e a pergunta 6 da folha da PROVA-DE-TELA-01 —
*"está tudo dizendo a verdade ao mesmo tempo?"* — nunca foi feita entre elas,
porque a folha pergunta *"em toda a janela"*
([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md),
linha 47), e o painel não é a janela.

Este documento mede primeiro. Onde a medição contradiz a suspeita que abriu a
sprint, quem manda é a medição — e ela contradisse em dois pontos grandes.

## O que eu medi na máquina dela, agora, sem encostar em nada

Tudo abaixo é leitura: `ps`, `ls`, `cat` de config, `md5sum`, `strings`. Zero
mutação, zero clique, zero chamada ao socket do daemon (que está vivo, PID 3615,
`daemon.pid` de 31/07 01:10).

**1. O applet está rodando no painel dela neste instante.**

```
$ ps -eo pid,etime,cmd | grep hefesto-dualsense4unix-applet
   4505       50:07 hefesto-dualsense4unix-applet
```

E está no painel por configuração dela, não por acidente —
`~/.config/cosmic/com.system76.CosmicPanel.Panel/v1/plugins_wings` lista, na asa
esquerda, quarta posição:

```
"dev.cappsy.CosmicExtAppletLogoMenu",
"com.system76.CosmicAppletBattery",
"io.github.cosmic_utils.cosmic-ext-applet-external-monitor-brightness",
"com.vitoriamaria.HefestoDualsense4Unix",
"com.system76.CosmicAppletWorkspaces",
```

**2. A bandeja GTK está MORTA nesta sessão.** O arquivo que a própria
`tray.py:282-286` escreve quando o probe do `StatusNotifierWatcher` esgota as
três tentativas existe, e é de hoje:

```
$ ls -la /run/user/1000/hefesto-dualsense4unix/
-rw-rw-r-- 1 vitoriamaria vitoriamaria  45 jul 31 01:13 cosmic_tray_warned.flag
-rw------- 1 vitoriamaria vitoriamaria   5 jul 31 01:10 daemon.pid
-rw------- 1 vitoriamaria vitoriamaria   5 jul 31 01:13 gui.pid
```

A causa é a de sempre e está medida: `cosmic-applet-status-area` **não está no
painel dela** (`grep -rl StatusArea ~/.config/cosmic/` devolve vazio) e **não
está rodando** (`ps ... | grep cosmic-applet-status-area | grep -v grep | wc -l`
devolve `0`). Sem ele não há watcher no D-Bus, e sem watcher o `AppIndicator`
que a `tray.py:152` cria não é desenhado por ninguém.

**3. A janela compacta está desligada, como o código manda.** O processo vivo da
GUI é o PID 7271 (`python3 -m hefesto_dualsense4unix.app.main`, e
`/run/user/1000/hefesto-dualsense4unix/gui.pid` diz `7271`). O ambiente dele não
tem a variável:

```
$ tr '\0' '\n' < /proc/7271/environ | grep -i COMPACT
(vazio)
```

### O que essas três medições fazem com a premissa desta sprint

A suspeita que abriu a sprint dizia que a bandeja é *"a que ela realmente vê"*.
**A medição REFUTA.** O que ela realmente vê no painel é o applet Rust. A
bandeja é criada sempre (`app/app.py:996-1004`, sem condição), mas criar não é
aparecer: nesta sessão ela não apareceu, e a notificação de aviso já foi emitida
às 01h13.

Isso inverte a ordem de importância das três superfícies e é por isso que a E1
(applet) vem antes da E2 (bandeja). Não é preferência de escopo: é a foto da
máquina dela.

## As quatro superfícies, e quem já olhou cada uma

| Superfície | Onde mora | Tamanho | Alcançável hoje? | Sprint que a mediu |
|---|---|---:|---|---|
| Janela GTK | `src/hefesto_dualsense4unix/gui/main.glade` (3269 linhas) + `app/` | 9 abas | sim (PID 7271) | PALAVRA-01, LEGIBILIDADE-01, VÃO-01, LARGURA-01, STATUS-SIMETRIA-02, CARD-OCUPA-01 |
| Applet COSMIC | `packaging/cosmic-applet/src/` | `app.rs` 1032 + `ipc.rs` 705 + `main.rs` 8 | **sim, e é a que está no painel** (PID 4505) | **nenhuma** |
| Bandeja | `src/hefesto_dualsense4unix/app/tray.py` | 463 linhas | **não nesta sessão** (sem watcher) | **nenhuma** |
| Janela compacta | `src/hefesto_dualsense4unix/app/compact_window.py` | 317 linhas | **não** (opt-in desligado) | **nenhuma** |

As contagens de `tray.py` (463) e `compact_window.py` (317) batem exatamente com
as de 29/07 — os dois arquivos não mudaram uma linha desde então. (A
`compact_window.py` passou a 327 na rodada das 06h, quando o cabeçalho mentiroso
foi reescrito; a `tray.py` segue em 463 e segue sem ninguém a ter visto.)

### A correção que eu faço no achado do auditor, e por quê

O achado de origem diz que o applet está *"fora de todo radar"*. **Não está, e a
diferença importa** — é o mesmo método que o verificador independente aplicou ao
achado do cadeado nesta mesma rodada: antes de chamar de buraco, confira se a
cadeia documental já o fecha por outro lado.

Conferido hoje, o applet está DENTRO de três portões:

| Portão | Onde | O que ele trava do applet |
|---|---|---|
| `check_version_consistency.py` | `scripts/check_version_consistency.py:66` | o `version =` do `Cargo.toml` contra a versão canônica — reprova a release se divergir |
| `check_packaging_parity.sh` | `scripts/check_packaging_parity.sh:49` e `:151` | o `Icon=` do `.desktop` do applet e o `X-HostWaylandDisplay=true` |
| Paridade de comportamento | `tests/unit/test_flavor_parity_superficies.py:30-46` e `tests/unit/test_applet_paridade_modo.py:53-74` | dois testes Python que LEEM o `app.rs` como texto e reprovam quando a máscara padrão ou o plano de modo divergem da GUI |

O que está fora de radar é outra coisa, mais estreita e mais verdadeira: **o
TEXTO que o applet mostra e os FATOS que ele deixa de mostrar.** Nenhum índice,
nenhuma sprint e nenhum gate olham para isso. É esse o alvo da E1, e é sobre
esse precedente — teste Python lendo Rust como texto — que a E4 se apoia, porque
a técnica já está provada nesta casa.

---

## (a) O applet COSMIC — a superfície que mora na barra dela

### O artefato, medido

| O quê | Medida de hoje |
|---|---|
| `Cargo.toml`, linha 9 | `version = "0.4.0"`, arquivo com mtime 30/07 12:58 |
| Motivo do retoque | comentário `APPLET-VERSAO-RANCOSA-01` nas linhas 3-8 do próprio `Cargo.toml`: ficou em 0.1.0 enquanto o projeto ia à 0.3.0 |
| Fonte | `src/app.rs` e `src/ipc.rs` com mtime 25/07 14:27 — intactos desde então, árvore limpa em `7bd0cb7` |
| Binário compilado | `target/release/hefesto-dualsense4unix-applet`, 23.652.184 bytes, 30/07 13:04 |
| Binário instalado | `/usr/local/bin/hefesto-dualsense4unix-applet`, root:root, mesmos bytes e mesma data |
| Os dois são o mesmo arquivo | `md5sum` idêntico nos dois: `c26926050a851b12600f93754aca6eea` |
| `.desktop` instalado | `/usr/share/applications/com.vitoriamaria.HefestoDualsense4Unix.desktop`, 30/07 13:04 |

E o binário instalado **carrega o texto do fonte de hoje** — não é um resto
antigo. Nove frases de tela do `app.rs` aparecem dentro dele:

```
$ sudo strings /usr/local/bin/hefesto-dualsense4unix-applet > /tmp/.../applet_strings.txt
$ for t in "Jogando pelo Hefesto" "Controlando o PC" "PlayStation" "Xbox 360" \
           "Daemon desconectado" "desligar Hefesto" "CONTROLE-ALVO" "jogadores" \
           "O QUE O CONTROLE FAZ"; do grep -c -F -- "$t" ...; done
1 1 1 1 1 1 1 1 1
```

Isso paga uma das linhas do "não medi" do auditor de origem, que declarou não
ter comparado o binário instalado com o fonte. Está comparado, por duas vias.

### O Rust fala português. E fala o português DELA

Resposta direta à pergunta que abriu a sprint: **sim.** O `app.rs` não tem uma
frase de tela em inglês. Mais que isso, ele usa o vocabulário que a
UX-MODE-TERMS-01 e a LEIGO-02 escolheram para a aba Início, e o comentário em
`app.rs:584` diz isso por extenso (*"mesmos termos da aba Início da GUI (sem
jargão)"*).

Confirmado par a par, arquivo contra arquivo:

| Conceito | Janela GTK | Applet | Bate? |
|---|---|---|---|
| Modo, no comutador | `app/actions/home_actions.py:72-76` — "Controlar o PC" / "Jogar pelo Hefesto" / "Jogar direto (Sony)" | `app.rs:656-660` — as três, na mesma ordem | sim |
| Modo, no estado | `app/actions/profiles_actions.py:122-124` | `app.rs:585-594`, com o "(pelo perfil)" quando a origem é o perfil | sim |
| Máscara, texto | `home_actions.py:83-86` — "Xbox 360" e "DualSense (botões PlayStation)" | `app.rs:696-699` — as duas frases idênticas | sim |
| Máscara padrão | `integrations/uinput_gamepad.py:136` — `DEFAULT_FLAVOR = "xbox"` | `app.rs:51` — `const DEFAULT_FLAVOR: &str = "xbox"` | sim, e travado por teste |
| Marca do item ativo | `app/tray.py:47` — `ACTIVE_MARKER = "> "` | `app.rs:666`, `:702`, `:731`, `:786` — `"> "` | sim |
| Microfone, leitura do estado | `emulation_actions.py:530-533` — drop-ins 52/53 | `app.rs:951-956` — os mesmos dois nomes | sim |
| Ícone do painel | — | `app.rs:40` pede `hefesto-dualsense4unix`; os 10 PNGs existem em `~/.local/share/icons/hicolor/*/apps/` | sim |

**Sete paridades conferidas e sete passando.** Isso não é resultado nulo: é a
medida de quanto trabalho de vocabulário já foi replicado à mão no Rust, e é o
que torna as divergências abaixo interessantes em vez de esperadas.

### As sete divergências que eu medi

Nenhuma delas é opinião. Cada uma é um par de linhas.

**D1 — A ordem das máscaras está invertida, e o comentário do applet afirma o
contrário.**

`home_actions.py:83-86` lista `("xbox", ...)` primeiro e `("dualsense", ...)`
depois. `app.rs:696-699` lista `("dualsense", ...)` primeiro e `("xbox", ...)`
depois. O comentário logo acima, em `app.rs:685-688`, diz: *"a ordem e os textos
agora espelham a aba Início"*. Os textos espelham. A ordem não.

**D2 — O applet não sabe que o cadeado do autoswitch existe.**

O daemon publica o fato: `daemon/ipc_handlers.py:1151` põe `"autoswitch_locked"`
dentro do `state_full`. A janela consome e explica em uma frase de duas metades
(`home_actions.py:131-152`, usada em `:858` e `:925`). O applet não tem o campo:
`grep -in "autoswitch\|cadeado\|lock" packaging/cosmic-applet/src/*.rs` não
devolve uma linha de código, só nomes de função sem relação.

E o cadeado está LIGADO agora:

```
$ ls -la ~/.config/hefesto-dualsense4unix/autoswitch_locked.flag
-rw-rw-r-- 1 vitoriamaria vitoriamaria 2 jul 28 18:18 autoswitch_locked.flag
```

Ou seja: hoje, clicar num perfil pela lista do applet troca o perfil sem uma
palavra sobre a política que está em vigor, enquanto a janela, a dois cliques
dali, explica.

**D3 — A lista de perfis do applet tem os dados da disputa e joga fora.**

`ipc.rs:224-234` deserializa `priority` e `match_type` do `profile.list` e marca
os dois com `#[allow(dead_code)]`, com o comentário honesto *"a UI atual só
consome `name`"*. O `profiles_block` (`app.rs:763-799`) lista só o nome.

Os perfis dela, contados hoje em `~/.config/hefesto-dualsense4unix/profiles/`,
são **15**, e **cinco** são catch-all (`match: any`): `fallback` (prio 0),
`meu_perfil` (1), `Pragmata` (5), `Pragmata2` (5), `vitoria` (0). O applet
mostra os quinze numa lista rolável, todos com o mesmo peso visual. A janela ao
menos traduz o tipo — `profiles_actions.py:141-143` mapeia `"any"` para
`"Sempre"` e `"criteria"` para `"Só neste programa"`.

Isto é a mesma queixa da EMPATE-01/E2 (*"a aba Perfis não mostra a disputa"*),
com a diferença de que na aba Perfis o dado chega e não é usado, e no applet ele
chega, é deserializado, e é explicitamente marcado como não usado.

**D4 — O aviso da CONTAGEM-E-COOP-01 não chegou a superfície nenhuma.**

O daemon emite as duas chaves em `ipc_handlers.py:1661-1662`
(`coop.derrubado_por_steam_input` e `coop.secundarios_derrubados`), com um
comentário de 16 linhas explicando por que são duas perguntas distintas. O
`CoopState` do applet (`ipc.rs:166-179`) tem exatamente dois campos: `enabled` e
`players`. A janela também não consome — `grep` das duas chaves fora de
`daemon/` devolve zero em `src/`, e as únicas referências no repositório estão
em `tests/unit/test_coop_nao_cai_em_silencio.py:334,340`.

Conclusão medida, e ela é pior que o achado original: **o fato existe, tem
teste, e não tem nenhum consumidor.** A CONTAGEM-E-COOP-01 não está "metade
entregue em código"; está entregue no daemon e ausente das DUAS superfícies que
poderiam contá-lo.

**D5 — A contagem de jogadores é calculada de dois jeitos diferentes.**

`home_actions.py:325-342` conta **jogadores distintos numerados pelo daemon**
(o conjunto dos campos `player` dos controles), e o docstring diz por quê:
*"enquanto o segundo jogador não subiu, o jogo ainda vê um gamepad só e a frase
seria mentira"*. `app.rs:838-845` usa `state.coop.players`, o número que o
`CoopManager` reporta (`ipc_handlers.py:1616`).

Nos dois casos a frase final é a mesma — `"{n} controles = {n} jogadores"`. O
que não medi é se os dois números podem divergir na prática; está no fim do
documento, na lista honesta.

**D6 — O applet não vê o número de controles EXTERNOS.**

`ipc_handlers.py:1638` acrescenta `coop.externals` ao estado, com um comentário
(`EXT-COUNT-01`) que explica exatamente o risco: *"com 2 DualSense e 2 Pro vivos
ele diz '2', e quem lê de fora conclui que só há 2 controles"*. O `CoopState` do
applet não tem o campo. Ou seja, o applet é literalmente o "quem lê de fora" que
o comentário previu.

**D7 — Ligar o microfone pelo applet joga fora o aviso que a janela faz questão
de dar.**

Os dois caminhos terminam no mesmo script, e isso está certo:

- janela: `emulation_actions.py:620` chama `_run_mic("--enable-mic", ...)`, que
  roda `scripts/fix_wireplumber_default_source.sh`;
- applet: `app.rs:961-970` roda `hefesto-dualsense4unix mic on`, e
  `cli/cmd_mic.py:58` mapeia `"on"` para o mesmo `--enable-mic`.

A diferença é o aviso. O script imprime, em `stderr`
(`scripts/fix_wireplumber_default_source.sh:290-291`):

```
[wp-fix] AVISO: ligar o mic do DualSense SEM o quirk de áudio USB ativo nesta
         sessão pode REABRIR o storm -71 (o controle cai no meio do jogo).
```

A janela **não vê esse stderr** e resolveu duplicando a checagem em Python:
`emulation_actions.py:562-575` (`_usb_quirk_active`, lendo `/proc/cmdline` e
`/sys/module/usbcore/parameters/quirks`) e `:612-619`, que troca a mensagem
final por um aviso longo quando o quirk não está ativo. O comentário em `:606-611`
conta a história inteira.

O applet manda `stderr` para `Stdio::null()` (`app.rs:968`) e não tem checagem
própria: `grep -in "quirk\|storm\|0ce6"` no `packaging/cosmic-applet/src/`
devolve **uma linha só, e é comentário** (`app.rs:481`). O aviso morre.

E há uma consequência de segunda ordem que vale escrever, porque o número surpreende:
`--enable-mic` remove **três** drop-ins, não dois — `fix_wireplumber_default_source.sh:297`
itera sobre `DROPIN_DST` (51), `DROPIN_DISABLE_DST` (52) e `DROPIN_OUTPUT_DST` (53).
O 51 é o `51-hefesto-dualsense-no-default-source.conf`, e é o único que está
instalado na máquina dela hoje (mtime 30/07 13:07), posto pela cura do commit
`84c0f83`. Um ciclo "Desligar microfone" seguido de "Ligar microfone" pelo
applet apaga essa cura em silêncio.

### O que o applet mostra, bloco a bloco

Para que a próxima sprint não precise reler 1032 linhas de Rust. Ordem de cima
para baixo, de `app.rs:413-539`:

| Bloco | Linhas | Aparece quando | O que diz |
|---|---|---|---|
| Cabeçalho | `:418-419` | sempre | `Hefesto - Dualsense4Unix` |
| Estado | `:543-637` | sempre | `Daemon desconectado` **ou** `Nenhum controle conectado` **ou** `Consultando…`; senão Bateria / Perfil ativo / Modo, mais `Controles` com 2+, `Modo jogo` se suprimido e `Estado: Pausado` se pausado |
| O QUE O CONTROLE FAZ | `:643-712` | daemon online | três modos exclusivos; no modo Jogo acrescenta a frase de jogadores e as duas máscaras |
| CONTROLE-ALVO | `:719-760` | 2+ controles conectados | `Todos (broadcast)` + `Controle N — USB/BT`, pelo `player_slot` com fallback posicional |
| PERFIS | `:763-799` | sempre | lista rolável, só o nome |
| Modo jogo | `:446-479` | sempre | `Modo jogo` / `Sair do modo jogo`, com o gate HARM-03 replicado |
| Microfone | `:481-498` | sempre | `Ligar microfone` / `Desligar microfone` |
| Abrir painel | `:501-511` | sempre | roda `hefesto-dualsense4unix-gui` |
| Fechar painel | `:514-524` | sempre | `pkill -f hefesto-dualsense4unix-gui` |
| Sair (desligar Hefesto) | `:527-537` | sempre | `systemctl --user stop` + `pkill -TERM -f "... daemon start"` |

Uma coisa em que o applet é **melhor** que as outras superfícies, e é justo
registrar: ele só consulta o daemon com o popover aberto
(`app.rs:382-390`, `Subscription::none()` quando fechado). A bandeja consulta a
cada 3 s para sempre (`tray.py:191`) e a janela escondida na bandeja mantém os
três pollers vivos (achado da área de GUI, `status_actions.py:1269-1271` e
`:1306-1347`). O applet é o único dos três que não custa nada quando ninguém
está olhando.

---

## (b) A bandeja — 463 linhas que ninguém auditou e que hoje não aparecem

### O que é certo, e é decisão registrada

A bandeja é criada **incondicionalmente** em `app/app.py:996-1004`. Em COSMIC, a
criação do indicator é adiada 1500 ms (`tray.py:54`, aplicado em `:125-140`), e
o número tem motivo escrito: `BUG-TRAY-COSMIC-MISSING-NOTIFY-SPAM-01`, porque em
COSMIC 1.0.6+ o watcher pode levar ~1 s para registrar depois do login. Depois
vêm três tentativas de probe com 1 s entre elas (`:59-60`, `:212-232`) e uma
flag persistente para nunca repetir o aviso (`:234-286`). Isso é uma decisão
tomada contra uma queixa real dela (*"ele fica falando que tem algo não
instalado"*, comentário em `:200`), e esta sprint **não propõe desfazer**.

### O que a bandeja mostra — a lista inteira, pela primeira vez

São cinco textos e um sufixo. É tudo:

| Texto | Onde | Observação |
|---|---|---|
| `Hefesto - Dualsense4Unix` | `tray.py:156` | título do indicator |
| `Hefesto - Dualsense4Unix (carregando...)` | `:160` | item de status, insensível |
| `Abrir painel` | `:164` | mesma frase do applet (`app.rs:505`) |
| `Perfis` | `:170` | submenu |
| `Sair do Hefesto - Dualsense4Unix` | `:181` | encerra o processo da GUI |
| `(nenhum perfil)` | `:407` | submenu vazio |
| `Hefesto - Dualsense4Unix - perfil: %s` / `- %d perfis` | `:433-437` | item de status já carregado |
| ` · %(n)d controles (%(t)s)` | `:387` | sufixo, só com 2+ conectados |

Comparada às outras duas superfícies, a bandeja **não mostra bateria, não mostra
modo e não mostra o controle-alvo**. Ela mostra perfil e contagem de controles.
Se isso é o certo para um menu de bandeja ou se é defeito é decisão de produto,
e é dela — está na E2, não neste parágrafo.

### As três divergências que eu medi na bandeja

**B1 — Duas palavras sem acento e um anglicismo, na frase que ela recebe como
notificação do sistema.**

`tray.py:273-276`:

> `"Tray icon indisponivel no COSMIC. Habilite o applet 'Area de status' no cosmic-panel (Configurações > Painel) ou use a janela principal. Este aviso só aparece uma vez."`

`indisponivel` é `indisponível`. `Area` é `Área`. `Tray icon` é o mesmo tipo de
jargão que a PALAVRA-01/E3 tirou da janela. A frase reaparece em `:53` (comentário)
e em `:460` (`RuntimeError("AppIndicator indisponivel")`).

Esta é a frase que ela recebeu hoje às 01h13.

**B2 — O portão de acentuação não pega, e eu provei por que.**

```
$ python3 scripts/validar-acentuacao.py --check-file src/hefesto_dualsense4unix/app/tray.py
exit=0
```

Não é bug do gate: é lacuna de dicionário. Provado isolando as palavras num
arquivo `.py` de uma linha só:

```
$ printf '# Tray icon indisponivel no COSMIC. Habilite o applet Area de status.\n' > prova3.py
$ python3 scripts/validar-acentuacao.py --check-file prova3.py
exit=0

$ printf '# a emulacao nao esta disponivel\n' > prova4.py
$ python3 scripts/validar-acentuacao.py --check-file prova4.py
1 violação(es): nao -> sugestão não
exit=1
```

Ele conhece `nao`, `configuracao` e `usuario`; não conhece `indisponivel`,
`Area` nem `emulacao`.

**B3 — Dois timers criados e nenhum guardado.**

`tray.py:191` chama `GLib.timeout_add_seconds(PROFILE_REFRESH_SEC, self._tick_refresh)`
e descarta o id. O `stop()` (`:288-296`) só põe o indicator em `PASSIVE`. Hoje
isso é inócuo porque `stop()` coincide com o fim do processo, e o achado da área
de GUI já diz isso; fica aqui só para a E2 não redescobrir.

---

## (c) A janela compacta — inalcançável, e com TRÊS textos contando a história errada

### A decisão vigente, que é boa e está escrita

`compact_window.py:54-58` e `:61-69`: a janela é **opt-in**, default desligado,
e o motivo está no comentário — *"a versão flutuante always-on-top no COSMIC era
intrusiva"*. `app/app.py:1005-1010` repete a decisão e aponta o caminho certo
para quem não tem bandeja: o applet. **Isto não é lapso, é decisão**, e a E3
trabalha com ela, não contra.

### As três contradições

**C1 — O cabeçalho do módulo descreve o gating ANTIGO.**

`compact_window.py:9-12`:

> *"Gating (decisão UX 2026-05-16): AUTO por default quando `AppTray.start()`
> retorna False (sem AppIndicator) OU quando estamos em COSMIC sem
> StatusNotifierWatcher. Opt-out via `HEFESTO_DUALSENSE4UNIX_COMPACT_WINDOW=0`."*

Quarenta linhas abaixo, `:61-69` diz o inverso, e é o código que roda. Quem
abrir o arquivo e ler só o cabeçalho conclui exatamente o contrário do real.

**C2 — O log da própria função culpa a variável errada.**

`compact_window.py:104`: `logger.info("compact_window_opt_out", env=f"{ENV_OPT_OUT}=0")`.
O motivo real de não subir não é `=0`; é a ausência de `=1` (`:69`). Quem for
depurar por log procura uma variável que ninguém setou.

**C3 — E a pior das três: a documentação de usuária ensina o comportamento
antigo, na página exata do problema que ela tem hoje.**

`docs/usage/troubleshooting.md`, seção **"3. Tray icon oculto no Pop!_OS COSMIC"** —
que é literalmente a situação medida no começo deste documento — diz, nas linhas
122-128:

> *"**Janela compacta (default v3.3.0+)**: o Hefesto detecta automaticamente e
> abre uma janela 320×90 sempre-on-top com bateria + perfil + botões. Se ela não
> aparecer, garantir que não há `HEFESTO_DUALSENSE4UNIX_COMPACT_WINDOW=0` no
> ambiente:"*
>
> ```
> env | grep COMPACT_WINDOW          # esperado: vazio (default ligado)
> ```

E na linha 136:

> *"**Desativar janela compacta** se preferir só GUI principal:
> `HEFESTO_DUALSENSE4UNIX_COMPACT_WINDOW=0 hefesto-dualsense4unix-gui`."*

Os dois estão errados hoje. Vazio significa **desligado**, e o `=0` da linha 136
é uma operação sem efeito. Se ela seguir esse documento no estado em que a
máquina dela está agora, ela vai rodar `env | grep COMPACT_WINDOW`, ver vazio,
concluir que está tudo certo e continuar sem janela nenhuma além da principal.

O item 2 da mesma seção (linhas 129-134), por outro lado, está **certo** e é o
que de fato a salvou: diz que o projeto traz um applet COSMIC nativo instalado
por padrão em sessões COSMIC — e o `install.sh:2232` confirma (passo 9/11,
*"applet COSMIC nativo (padrão em COSMIC; --no-cosmic-applet desativa)"*).

E vale a nota de honestidade: **isto não é uma das nove contradições da
DOC-VERDADE-01.** Conferido por grep hoje — aquele documento não menciona
`compact`, `bandeja`, `tray` nem `applet`. É contradição nova.

---

## O gate que deixou tudo isso passar

Quatro achados de portão, todos medidos hoje.

**G1 — O validador de acentuação não enxerga `.rs`.**

`scripts/validar-acentuacao.py:432-436`:

```python
EXTENSOES_ALVO = (
    ".py", ".sh", ".zsh", ".bash",
    ".md", ".yml", ".yaml", ".toml",
    ".cfg", ".ini", ".txt",
)
```

Não há `.rs`. E `.glade` está na whitelist explícita (`:427`), o que significa
que **nem o Rust do applet nem o XML da janela** passam pelo gate. Prova, com o
mesmo texto em duas extensões:

```
$ printf '// A configuracao do usuario e a emulacao nao funcionam.\n...' > prova2.rs
$ printf '# A configuracao do usuario e a emulacao nao funcionam.\n'      > prova2.py

$ python3 scripts/validar-acentuacao.py --check-file prova2.py
3 violação(es): configuracao, usuario, nao      exit=1

$ python3 scripts/validar-acentuacao.py --check-file prova2.rs
exit=0
```

**Nota de honestidade que a E4 precisa carregar:** hoje o applet **passaria**. Eu
copiei `app.rs` e `ipc.rs` para `.txt` (extensão que o gate aceita) e rodei — os
dois saem com exit 0. O risco é prospectivo, não corrente: o dia em que alguém
escrever `configuracao` numa frase de tela do Rust, ninguém vai reclamar.

**G2 — O CI nunca compila o applet.**

`grep -rn "cargo\|rust\|applet" .github/` nos quatro workflows
(`anonymity-check.yml`, `ci.yml`, `flatpak.yml`, `release.yml`) devolve **uma
linha**, e é `release.yml:434`, *"Publicar no PyPI"*, casada por acidente na
palavra `publicar`. O applet é o único artefato compilado da casa e nenhum
runner o compila. O `Cargo.lock` é de 30/07 13:04, da compilação local dela.

**G3 — O pre-commit tem quatro portões, e nenhum é sobre texto de tela.**

`.pre-commit-config.yaml`: `acentuacao-strict` (`:28`), `glifos` (`:40`),
`anonimato` (`:46`), `ruff-check` (`:51`). A PALAVRA-01/E5 pedia um quinto —
capitalização e jargão banido — e ele não existe. Sem ele, `Daemon offline`
(`compact_window.py:275`), `Daemon desconectado` (`app.rs:548`) e
`Indisponível (daemon offline)` (`app.rs:775`) convivem com a janela principal,
que já diz `O Hefesto está desligado` (`emulation_actions.py:741` e
`home_actions.py:871`).

**G4 — A folha da PROVA-DE-TELA-01 tem escopo de janela.**

As seis perguntas (linhas 41-48 daquele documento) falam em *"as nove abas"* e
*"em toda a janela"*. A pergunta 5 — *"a mesma coisa tem o mesmo nome e o mesmo
número em toda a janela?"* — é exatamente a pergunta que pegaria a D1 e a D5,
e ela para na borda da janela.

---

## Entregas

Ordem por valor medido, não por facilidade. A E1 vem primeiro porque o applet é
o que está no painel dela agora.

### E1. O applet, medido contra a janela — e as sete divergências decididas uma a uma

Não é "consertar o applet". É levar as sete divergências (D1 a D7) para a mesa
dela como perguntas de produto, com a medida ao lado, e registrar a decisão de
cada uma neste documento. Três delas provavelmente são conserto de uma linha
(D1); duas são decisão de desenho (D2, D3); uma é dívida de daemon que ninguém
consome (D4); uma é risco de hardware (D7).

Sugestão de ordem, pelo que custa contra o que rende:

1. **D1** (ordem das máscaras) — inverter duas linhas em `app.rs:696-699`, ou
   corrigir o comentário de `:685-688` se a ordem do applet for a preferida. Uma
   das duas coisas TEM de mudar: hoje o comentário mente.
2. **D7** (aviso do quirk) — o applet precisa da mesma checagem que a janela tem
   em `emulation_actions.py:562-575`, ou precisa parar de oferecer o botão. Esta
   é a única das sete com consequência de hardware: ligar o mic sem o quirk pode
   derrubar o controle no meio da partida.
3. **D2** (cadeado) — uma linha no bloco PERFIS quando `autoswitch_locked` é
   verdadeiro. Exige acrescentar o campo ao `DaemonState` (`ipc.rs:113-164`).
4. **D3** (prioridade e tipo do perfil) — os dados já chegam; é decidir se a
   lista do painel os mostra.
5. **D4, D5, D6** — as três dependem de decisão fora do applet (a D4 é
   CONTAGEM-E-COOP-01, que precisa do documento dela primeiro).

**Aceite:** este documento ganha uma tabela com sete linhas, cada uma com a
decisão dela por extenso (`muda` / `fica como está, e por quê`), e nenhuma
divergência sai daqui sem uma das duas. Onde a decisão for `muda`, a mudança
entra sozinha, com o painel aberto na frente dela — regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
**O olho dela é obrigatório aqui**, porque o popover é a única superfície deste
projeto que não dá para fotografar com `Gtk.OffscreenWindow`: quem desenha é o
`cosmic-panel`.

**Risco:** baixo para a medição, médio para o conserto — e o médio tem nome.
Mexer no `app.rs` obriga a recompilar (`cargo build --release`) e reinstalar em
`/usr/local/bin`, que é root. O binário de hoje está provado idêntico ao fonte
(md5 + as nove frases); qualquer edição desfaz essa prova até a próxima
compilação. Enquanto o CI não compila o applet (G2), a única compilação que
existe é a da máquina dela.

### E2. A bandeja, medida — e a pergunta de produto que ninguém fez

A bandeja mostra perfil e contagem de controles. O applet mostra bateria, modo,
controle-alvo, máscara, microfone e perfis. A janela mostra tudo. **A pergunta
que nunca foi feita é se as três precisam mostrar as mesmas coisas** — e a
resposta provavelmente é não, mas ela tem de ser escrita, porque hoje a
diferença é resultado de ninguém ter comparado, não de alguém ter escolhido.

O que entra, medido:

1. A tabela de textos da bandeja (acima) vira a lista canônica, e cada linha
   ganha um veredito: fica, muda, ou some.
2. **B1** — as duas palavras sem acento e o `Tray icon` da notificação de
   `tray.py:273-276`. Esta é a única da E2 com defeito objetivo: a frase é
   português e está escrita errado.
3. **B3** — os timers sem `source_remove` viram nota, não entrega. Hoje são
   inócuos e o achado já está registrado.
4. Uma decisão explícita sobre o parágrafo mais desconfortável desta sprint: a
   bandeja **não aparece na máquina dela**, e não aparece por configuração do
   painel COSMIC, não por bug nosso. Vale manter 463 linhas para um caminho que
   ela não usa? A resposta pode muito bem ser sim (outras distribuições, GNOME
   com extensão, KDE) — mas hoje ninguém a deu.

**Aceite:** a lista de textos da bandeja fica neste documento com um veredito por
linha; a frase de `tray.py:273-276` é reescrita com acentuação completa e sem
`Tray icon`; e o documento registra, com a palavra dela, se a bandeja continua.

**Risco:** baixo. Nada aqui muda comportamento. A única mudança de texto é numa
notificação que, pela flag persistente (`:258-260`), só aparece uma vez por
máquina — o que significa que ela **não vai ver a correção** até apagar
`/run/user/1000/hefesto-dualsense4unix/cosmic_tray_warned.flag` ou rodar com
`HEFESTO_DUALSENSE4UNIX_RESET_TRAY_WARNING=1`. Isso precisa estar dito no
momento de validar, senão a validação reprova por engano.

### E3. O destino da janela compacta — e o cabeçalho mentiroso corrigido de qualquer jeito

Duas decisões, e a segunda depende da primeira.

**A decisão grande:** documentar a variável para ela, ou aposentar o módulo. Os
dados para decidir estão medidos: 317 linhas, sete testes
(`tests/unit/test_compact_window.py`), inalcançável desde que virou opt-in,
zero menções em qualquer índice, e um caminho de fallback que a própria
`app/app.py:1005-1010` já resolveu de outro jeito (o applet). Se aposentar, o
`app.py:1011-1020` e o import saem junto.

**O mínimo que entra em QUALQUER cenário**, porque é dívida pura:

1. `compact_window.py:9-12` — o cabeçalho passa a descrever o gating opt-in
   vigente, o mesmo que `:61-69` implementa.
2. `compact_window.py:104` — o log deixa de dizer `=0`.
3. `docs/usage/troubleshooting.md:120-136` — os itens 1 e 3 da seção "Tray icon
   oculto no Pop!_OS COSMIC" param de prometer uma janela que não vem. O item 2
   (o applet) está certo e fica.

**O terceiro é o mais urgente dos três**, e é o que muda a ordem em relação ao
achado original: o cabeçalho do módulo engana quem lê código, mas o
`troubleshooting.md` engana **ela**, na página do problema que ela tem hoje.

**Aceite:** os três textos passam a dizer o que o código faz; e se a decisão for
aposentar, o módulo, o gate de `app.py:1011` e os testes saem na mesma entrega,
sem sobra.

**Mordida do teste, se o módulo ficar:** `test_compact_window.py:133-152` já tem
os três testes de `is_enabled` (default falso, opt-in por `=1`, só o `1`
explícito ativa) — eles mordem. O que falta e precisa nascer é um teste de
**coerência do texto**: o cabeçalho do módulo não pode conter a string
`Opt-out`, e a seção 3 do `troubleshooting.md` não pode conter `default ligado`.
Arrancada a cura (voltando o cabeçalho antigo ou o texto do troubleshooting), o
teste tem de ficar vermelho — se ele passar com o texto velho, ele não testa
nada.

### E4. Uma regra que impeça a próxima renomeação de esquecer as outras três superfícies

Este é o item que faz a sprint valer para o futuro. Duas metades, e as duas são
baratas porque o precedente já existe nesta casa.

**Metade 1 — o portão automático.** Um teste no molde exato do
`tests/unit/test_flavor_parity_superficies.py:30-46`, que já lê `app.rs` como
texto de dentro de um teste Python, e do `test_applet_paridade_modo.py:53-74`,
que já extrai um ramo do Rust por regex. A técnica está provada e comentada:
*"O default do applet é Rust e não dá para importar: este teste lê o fonte e casa
a constante. É feio de propósito"* (linhas 14-16 daquele arquivo).

O teste novo trava **vocabulário compartilhado**: uma lista nomeada de conceitos
que aparecem em mais de uma superfície, com a frase canônica e onde ela vive.
Começa pequena e honesta, com os pares já medidos:

| Conceito | Dono da frase | Tem de aparecer também em |
|---|---|---|
| Os três modos | `home_actions.py:72-76` | `app.rs:656-660`, na **mesma ordem** |
| As duas máscaras | `home_actions.py:83-86` | `app.rs:696-699`, na **mesma ordem** |
| Máscara padrão | `uinput_gamepad.py:136` | `app.rs:51` (já travado hoje) |
| Marca do item ativo | `tray.py:47` | `app.rs`, `compact_window.py:241` |
| "O Hefesto está desligado" | `emulation_actions.py:741` | nenhuma superfície pode dizer `Daemon offline` / `Daemon desconectado` no lugar |

**Mordida:** com a lista de hoje, o teste **já reprova antes de qualquer
conserto** — a linha da ordem das máscaras (D1) falha contra `app.rs:696-699`, e
a linha do "Hefesto está desligado" falha contra `app.rs:548`, `app.rs:775` e
`compact_window.py:275`. É a prova de que ele morde: um teste de paridade que
nasce verde não testa nada. Depois da E1 e da E3 ele fica verde; reintroduzir
`Daemon offline` em qualquer das quatro superfícies tem de deixá-lo vermelho de
novo.

**A segunda mordida, contra o furo do G1:** acrescentar `.rs` ao
`EXTENSOES_ALVO` de `scripts/validar-acentuacao.py:432-436`. Prova de que morde:
o `app.rs` de hoje passa (medido — copiado para `.txt` e rodado, exit 0), então
a mordida é injetar `configuracao` numa frase do Rust e ver reprovar; com a
extensão fora da lista, a mesma injeção passa em silêncio.

**Metade 2 — a linha na folha humana.** A folha da PROVA-DE-TELA-01 ganha uma
sétima pergunta, e ela é curta:

> **7. A mudança de texto ou de contagem chegou às outras superfícies que a
> mostram?** Reprova quando um nome, uma frase de estado ou uma contagem muda na
> janela e continua diferente no applet do painel, na bandeja ou na janela
> compacta.

O motivo de ser pergunta humana e não só teste está medido nesta sprint: a
lista canônica do teste cobre o que alguém pensou em listar. A ordem invertida
das máscaras (D1) só apareceu porque eu abri os dois arquivos lado a lado — o
teste de paridade de modo, que já existe há dias, passa em cima dela sem ver.

**Aceite:** o teste novo existe, reprova no HEAD de hoje pelos motivos escritos
acima, e fica verde depois da E1 e da E3; `.rs` entra no `EXTENSOES_ALVO`; e a
sétima pergunta está na folha da PROVA-DE-TELA-01 com a data e o motivo do
acréscimo, como aquele documento manda nas linhas 90-93.

**Risco:** médio-baixo, com uma armadilha nomeada. Teste que casa **texto de
código-fonte** é frágil por natureza: um `rustfmt` que quebre a linha
`("dualsense", "DualSense (botões PlayStation)"),` em duas faz o regex errar e o
teste reprovar sem defeito nenhum. Os dois testes que já existem contornam isso
casando pedaços curtos e ancorados (uma constante, um nome de função), e o novo
tem de seguir a mesma disciplina: **casar a frase, nunca a formatação em volta
dela.** A segunda armadilha é de escopo — a lista tem de começar com cinco
linhas e crescer por evidência. Uma lista de trinta conceitos vira ruído e
alguém a desliga.

---

## Como você valida na tela

Sem terminal onde dá, e este é um dos raros casos em que dá quase tudo.

1. **Clique no ícone do Hefesto na barra do sistema** (asa esquerda, entre a
   bateria e o brilho do monitor). O popover que abrir é o applet — é a
   superfície desta sprint.
2. **Compare com a aba Início da janela, lado a lado.** Olhe a ordem dos dois
   botões de máscara. Na janela, `Xbox 360` vem primeiro. No painel, `DualSense
   (botões PlayStation)` vem primeiro. É a divergência D1, e é a única desta
   sprint que dá para ver sem saber nada de código.
3. **Ainda no popover, olhe a lista de PERFIS.** São quinze nomes, todos com o
   mesmo peso. Cinco deles valem para qualquer janela. Nada ali diz isso, e nada
   ali diz que o cadeado está ligado — a janela diz, na aba Início.
4. **Procure o ícone da bandeja no painel.** Não tem. Não é defeito de hoje: o
   `cosmic-applet-status-area` não está no seu painel, e sem ele a bandeja do
   Hefesto não tem onde aparecer. A notificação que você recebeu hoje às 01h13
   dizendo *"Tray icon indisponivel no COSMIC"* é exatamente isso — e é a frase
   que a E2 vai reescrever, porque `indisponivel` e `Area` estão sem acento.
5. **A janela compacta você não vai encontrar**, e está certo: ela é opt-in e
   está desligada. O que está errado é o `docs/usage/troubleshooting.md` dizer
   que ela aparece sozinha. Se você seguir aquela página hoje, ela te manda
   procurar uma janela que não vem.
6. **Nada mudou de lugar em lugar nenhum.** Esta sprint não tocou em código. Se
   alguma coisa mudou na sua tela entre ontem e hoje, não foi daqui.

E a nota que a E2 precisa: **para rever a notificação da bandeja corrigida**, a
flag persistente tem de sair — `/run/user/1000/hefesto-dualsense4unix/cosmic_tray_warned.flag`,
ou a GUI aberta com `HEFESTO_DUALSENSE4UNIX_RESET_TRAY_WARNING=1`. Sem isso a
frase nova nunca aparece e a validação reprova por engano.

---

## O que fica de fora desta sprint, por escrito

- **Qualquer conserto.** É radar. As sete divergências do applet, os três
  achados da bandeja e as três contradições da janela compacta viram decisão
  dela antes de virarem commit. O único conserto que a E3 admite sem decisão é
  texto que contradiz o próprio código ao lado.
- **A TUI.** É uma quinta superfície, tem o próprio defeito medido na auditoria
  de GUI (`tui/app.py:151-174`, o painel de preview que mostra `0` e `centro`
  como se fosse leitura viva) e é chamada pela CLI, não pelo painel. Merece
  documento próprio; misturá-la aqui transformaria quatro superfícies em cinco e
  a sprint em levantamento sem fim.
- **A geometria do popover.** Largura, vão, comprimento de linha — tudo o que a
  VÃO-01 e a LARGURA-01 mediram na janela. O popover é desenhado pelo
  `cosmic-panel` com o tema do sistema, `Gtk.OffscreenWindow` não o alcança, e a
  bancada de medição desta casa (CR-03) não cobre `libcosmic`. Fica para quando
  houver régua.
- **O deferimento de 1500 ms e o probe de três tentativas da bandeja.** São
  decisão registrada contra uma queixa dela (`tray.py:196-203`), e esta sprint
  não os discute.
- **A decisão de instalar o applet por padrão em COSMIC.** Está no
  `install.sh:2232` com identificador próprio
  (`BUG-INSTALL-APPLET-OPT-IN-SKIPPED-01`, `:2225-2229`) e é o que faz o painel
  dela funcionar hoje. Não é alvo.
- **Compilar o applet no CI (G2).** É entrega de infraestrutura, custa minutos
  de runner e um `rev` de `libcosmic` fixado por git (`Cargo.toml:27-33`, rev
  `1d7113a`). Vira achado para o índice, não entrega daqui.
- **Trazer as renomeações da PALAVRA-01 que a própria janela ainda não fez.**
  Medido de passagem: `Restaurar Default` continua no rodapé global
  (`gui/main.glade:3251`, `btn_footer_restore_default`) e `Gamepads:` continua
  na aba **Emulação** (`:2323`, dentro do `emulation_box` que começa em `:2255`),
  enquanto `Voltar ao padrão` já entrou no botão de atalhos da aba Navegação
  (`:3160`, `key_binding_restore_btn`) e a aba `Navegação DSX` já virou
  `Navegação` (rótulo em `:3174`, com o `id` `tab_navegacao_dsx` preservado em
  `:2768`, como a E2 daquela sprint exigiu). Isso é dívida da PALAVRA-01, não
  desta.

---

## O que eu NÃO medi

- **Não abri o popover do applet.** O daemon dela está vivo (PID 3615) e a
  janela também (PID 7271); a regra desta rodada proíbe encostar. Tudo o que
  digo sobre o que o applet mostra vem de ler `app.rs` e de confirmar as frases
  dentro do binário instalado — não de ver na tela. **O olho dela é o único
  aceite** dessa parte.
- **Não compilei o applet.** A identidade binário/fonte está provada por duas
  vias indiretas (md5 igual entre `/usr/local/bin` e `target/release`; nove
  frases de tela do fonte presentes no binário) e por uma cronologia
  consistente (`Cargo.toml` 12:58, build 13:04, fontes intactos desde 25/07).
  Não é o mesmo que reconstruir e comparar.
- **Não medi se a D5 chega a divergir.** A janela conta jogadores distintos
  numerados; o applet lê `coop.players`. Saber se os dois números podem
  discordar exige dois controles na mesa e o co-op montado — é medição de
  hardware, e o checklist da casa tem 31 caixas vazias.
- **Não rodei a suíte.** Nenhum número de teste deste documento vem de execução;
  os arquivos de teste foram lidos. A máquina dela está com o daemon vivo e uma
  coleta de cobertura já rodando.
- **Não li `app.rs` inteiro.** Das 1032 linhas, li os blocos 1-130, 382-395,
  396-540, 540-860 e 886-985. O `update()` (o que cada mensagem faz ao chegar,
  aproximadamente `:130-382`) foi lido por grep dirigido, não linha a linha. Se
  houver contradição escondida ali, ela não está neste documento. Do `ipc.rs`
  (705 linhas) li 108-237, o resto por grep.
- **Não medi a bandeja em outro ambiente.** Tudo o que digo sobre ela ser
  invisível vale para esta sessão COSMIC, com este painel. Em GNOME com a
  extensão de appindicators, ou em KDE, a bandeja provavelmente aparece — e é
  parte do que a E2 tem de pesar antes de propor aposentá-la.
- **Não conferi se a `compact_window` ainda desenha certo.** Ela não sobe desde
  que virou opt-in; ninguém a viu. Os sete testes de `test_compact_window.py`
  cobrem `is_enabled` e `_render_state`, que são funções puras — não cobrem a
  janela montada.
- **Não recontei as nove contradições da DOC-VERDADE-01.** Conferi só que
  nenhuma delas é sobre estas três superfícies, por grep dos quatro termos.

---

## O que a medição de 31/07 06h achou

Esta seção é da rodada RADAR-01 da Onda 2, com a mantenedora fora do jogo e o
controle do PC cedido por escrito. Diferente do corpo acima, aqui **houve tela**:
capturas de verdade, a janela compacta SUBIU pela primeira vez desde que virou
opt-in, e o estado do daemon foi lido pelo mesmo socket que o applet lê.

O que continuou proibido: **clique cego por coordenada**. A lição de 28/07 desta
casa (o `ydotool` relativo desligou o `autoswitch_locked` dela duas vezes) vale
mais que a foto do popover, então o popover do applet **segue sem foto** — o
olho dela continua sendo o único aceite dessa parte, como a E1 já dizia. Em
troca, o que o popover mostra neste instante está reconstruído abaixo linha a
linha a partir do estado vivo, o que é mais exato que uma foto.

Capturas em `docs/process/estudos/assets/2026-07-31-onda2/`.

### O estado vivo com que tudo abaixo foi medido

Leitura do socket às 06h16, `daemon.state_full` + `profile.list`, zero mutação
(daemon PID 3615 intacto, `etime` contínuo antes e depois):

```
connected=true  transport=usb  battery_pct=95  active_profile="Pragmata2"
autoswitch_locked=true  native_mode=false  paused=false  emulation_suppressed=false
gamepad_emulation={enabled: true, flavor: "dualsense"}
coop={enabled: true, players: 1, externals: 0,
      derrubado_por_steam_input: false, secundarios_derrubados: 0}
controllers=[{index:0, connected:true, transport:"usb", player_slot:1, battery_pct:95}]
profile.list -> 15 perfis
```

### T1 — o applet APARECE no painel. Foto: `04-icone-hefesto-no-painel-zoom12x.png`

Ele está na asa esquerda, quarta posição, exatamente onde o `plugins_wings`
manda — entre o brilho do monitor e os espaços de trabalho. A asa direita tem
sete ícones e nenhum é dele. Isso fecha a pergunta que a E1 abriu: **não é caso
de "roda mas não aparece"**.

O que ele mostra no painel é **só o ícone**, e é decisão registrada
(`app.rs:34-40`, `ICON_APP` usado SEMPRE, em qualquer estado, para a logo nunca
sumir em transições). Daí a primeira consequência medida: **o ícone não muda
com o estado**. Daemon morto, controle fora, bateria em 3% — o painel mostra o
mesmo desenho. Todo o estado vive dentro do popover, que só existe com o clique.

**Achado novo, que nenhuma sprint tinha:** o ícone dele é um PNG **colorido**
num painel onde todos os vizinhos são símbolos monocromáticos que herdam a cor
do tema. Na captura ampliada 12x isso é evidente: bateria, monitor, bluetooth,
áudio e energia são traços brancos; o do Hefesto é um martelo colorido dentro de
um disco escuro, com contraste baixo contra o painel escuro dela. Não é defeito
de código — é o `Icon=hefesto-dualsense4unix` do `.desktop` sendo o mesmo da
janela. É decisão de produto que ninguém tomou, e cabe na mesma mesa da E1.

### O que o popover mostra NESTE instante, reconstruído do estado vivo

Aplicando o estado acima às funções de `app.rs`, na ordem de
`popup_content()` (`:412-539`). Isto é derivação de código com entrada medida,
não suposição:

| Linha do popover | De onde sai | O que diz agora |
|---|---|---|
| Cabeçalho | `:418` | `Hefesto - Dualsense4Unix` |
| Bateria | `:565-573` | `95% (USB)` |
| Perfil ativo | `:575-580` | `Pragmata2` |
| Modo | `:584-596` | `Jogando pelo Hefesto` |
| Controles | `:602-618` | **não aparece** (1 controle, exige 2+) |
| Modo jogo / Pausado | `:622-636` | **não aparecem** (ambos falsos) |
| `O QUE O CONTROLE FAZ` | `:652` | título |
| Os três modos | `:656-671` | `  Controlar o PC` / `> Jogar pelo Hefesto` / `  Jogar direto (Sony)` |
| Frase de jogadores | `:677-679` + `:836-845` | **não aparece** (`players=1`) |
| As duas máscaras | `:696-711` | `> DualSense (botões PlayStation)` / `  Xbox 360` |
| `CONTROLE-ALVO` | `:719-760` | **não aparece** (1 controle) |
| `PERFIS` | `:763-799` | 15 nomes, `> Pragmata2` marcado, sem prioridade e sem tipo |
| Botões | `:446-537` | `Modo jogo` (clicável) / `Ligar microfone` / `Abrir painel` / `Fechar painel` / `Sair (desligar Hefesto)` |

**Resposta direta à pergunta "ele contradiz a janela em algum número?": NÃO.**
Com a janela aberta no mesmo minuto (foto `05`), bateria, transporte, perfil
ativo e modo batem os quatro. As divergências que existem **não são de número —
são de ORDEM, de FORMATO e de OMISSÃO**, e é isso que as três subseções
seguintes medem.

### As três formas de escrever o mesmo 95

Este é achado desta rodada, e é da família da pergunta 5 da PROVA-DE-TELA-01
("a mesma coisa tem o mesmo nome e o mesmo número?"), que para na borda da
janela — mas aqui nem dentro da janela ela é respeitada:

| Onde | Código | Na tela agora |
|---|---|---|
| Janela, aba Início, card do controle | `home_actions.py:372` — `f"{battery_pct}%"` | `95%` |
| Janela, aba Status, barra | `status_actions.py:1655` — `f"{battery} %"` | `95 %` |
| Janela compacta | `compact_window.py:319` — `{battery} %` em monoespaçada | `95 %` (com o vão da fonte, vira `95   %`) |
| Applet | `app.rs:570` — `format!("{pct}% ({transport})")` | `95% (USB)` |

Quatro superfícies, três grafias, e duas delas **dentro da mesma janela**. A
foto `06` mostra o vão do `95 %` da compacta; a foto `05` mostra o `95%` do card
da Início na mesma tela e no mesmo segundo.

### D1 confirmado NA TELA — foto `09-janela-ordem-das-mascaras-xbox-primeiro.png`

A janela lista **`Xbox 360` primeiro** e `DualSense (botões PlayStation)` depois,
com a DualSense em destaque (é a máscara ativa: `flavor="dualsense"` no estado
vivo). O applet lista **`DualSense` primeiro** (`app.rs:696-699`). A divergência
que o corpo da sprint deduziu de dois arquivos abertos lado a lado está agora
fotografada de um dos dois lados. Segue valendo o que a E1 diz: **uma das duas
coisas tem de mudar**, a ordem ou o comentário de `app.rs:685-688`.

Junto veio uma diferença menor, medida de passagem: o título do bloco é
`O que o controle faz agora` na janela e `O QUE O CONTROLE FAZ` no applet, sem o
`agora`. Cabe na lista de vocabulário da E4.

### D2 confirmado com o cadeado LIGADO no estado vivo — foto `10`

`autoswitch_locked=true` no JSON de 06h16. A janela explica em uma frase inteira
e nomeia o perfil: *"Cadeado ligado: o perfil não troca sozinho — vale o perfil
'Pragmata2'. Jogos com perfil próprio ainda entram; qualquer outra janela é
ignorada."* O applet, no mesmo instante, oferece quinze perfis clicáveis e não
diz uma palavra sobre a política em vigor. Confirmado como estava escrito.

### D4 confirmado com as chaves NA MÃO — e é a confirmação mais forte da rodada

O corpo da sprint deduziu por leitura de código. Agora está medido no dado: o
JSON que o daemon devolveu às 06h16 **contém literalmente**
`"derrubado_por_steam_input": false` e `"secundarios_derrubados": 0`. O
`CoopState` do applet (`ipc.rs:166-179`) tem exatamente dois campos. E o grep
das duas chaves fora de `daemon/`, em `src/` e `packaging/`, devolve **zero**:

```
$ grep -rn "derrubado_por_steam_input\|secundarios_derrubados" src packaging | grep -v "/daemon/" | wc -l
0
```

O daemon fala, tem teste, e não há ninguém do outro lado da linha. Confirmado.

**Correção ao D6, para ser justa:** o `externals` — a outra chave, do
EXT-COUNT-01 — **tem** consumidor na janela: 33 ocorrências em
`status_actions.py`, e são de HEAD (conferido com `git show HEAD:` — mesmo
número, não é mudança desta onda). Quem não vê `externals` é só o applet. O D6
está certo como escrito; anoto porque a leitura rápida da sprint pode juntar as
três chaves numa só, e elas não têm o mesmo estado.

### D3 — REFUTAÇÃO PARCIAL: hoje são QUATRO catch-alls, não cinco

O corpo desta sprint diz cinco: `fallback` (0), `meu_perfil` (1), `Pragmata` (5),
`Pragmata2` (5) e `vitoria` (0). O `profile.list` de 06h16 diz outra coisa:

```
Pragmata2  ->  priority 85, match_type "criteria"
```

`Pragmata2` **deixou de ser catch-all** — virou regra com prioridade 85, e é o
perfil ativo agora. Os catch-alls de hoje são **quatro**: `fallback` (0),
`meu_perfil` (1), `Pragmata` (5), `vitoria` (0). A mudança é de horas atrás,
desta madrugada, e não invalida o D3 — o applet continua jogando `priority` e
`match_type` fora (`ipc.rs:224-234`, `#[allow(dead_code)]`) e continua listando
os quinze com o mesmo peso. Só o número da frase muda: **quatro valem para
qualquer janela, e nada no painel diz isso.**

### T2 — a bandeja: invisível, confirmado por medição própria. E o log MENTE

Confirmado por três medidas independentes, todas desta rodada:

1. `cosmic-applet-status-area` **não está no painel** (ausente do
   `plugins_wings`, `grep -rl StatusArea ~/.config/cosmic/` devolve zero) e
   **não está rodando** (zero processos).
2. `statusnotifierwatcher_available()` — a função da própria `tray.py`, chamada
   direto no interpretador — devolve **`False`**, com `_desktop_is_cosmic()`
   devolvendo `True`.
3. A foto `01-tela-inteira-painel.png` não tem ícone de bandeja em canto nenhum:
   sete ícones na asa direita, todos com dono identificado no `plugins_wings`.

**O achado novo, e ele é sobre o log, não sobre a bandeja.** Subi a GUI inteira
às 06h17 e o log dela tem exatamente DUAS linhas sobre a bandeja:

```
06:17:52.120 [info] apptray_deferred_for_cosmic  delay_ms=1500 ...
06:17:53.632 [info] apptray_started              icon=hefesto-dualsense4unix
```

`apptray_started`. **Com zero pixels na tela.** O motivo está em `tray.py:110-118`:
`start()` devolve `True` quando o `probe_gi_availability()` passa — ou seja,
quando a typelib existe —, e `is_available()` (`:110-112`) pergunta a mesma
coisa. Nenhum dos dois pergunta pelo watcher. O probe do watcher roda depois,
falha as três vezes, e o aviso é engolido pela flag de 01h13
(`tray_warning_ja_avisado_em_sessao_anterior`, nível `debug`, invisível num log
em `info`). Resultado: **quem for depurar isso pelo log conclui que a bandeja
está no ar.** Isso pertence à E2 e não estava medido.

**E uma pista concreta para a decisão da E2:** o binário existe na máquina dela.

```
$ ls -la /usr/bin/cosmic-applet-status-area
lrwxrwxrwx root root /usr/bin/cosmic-applet-status-area -> cosmic-applets
$ cat /usr/share/dbus-1/services/com.system76.CosmicStatusNotifierWatcher.service
Name=com.system76.CosmicStatusNotifierWatcher
Exec=/usr/bin/cosmic-applet-status-area --status-notifier-watcher
```

O barramento de sessão lista `com.system76.CosmicStatusNotifierWatcher` como
**ativável** — mas o nome que o libayatana procura é `org.kde.StatusNotifierWatcher`,
e esse não existe. Ou seja: as 463 linhas da `tray.py` **funcionariam** nesta
máquina com uma linha a mais no `plugins_wings` dela. A E2 decide se vale pedir
isso a ela ou se a bandeja sai; o que esta medição acrescenta é que o custo de
ligar não é instalar nada.

Enquanto isso o número segue de pé, e agora com prova de execução: **463 linhas
que nunca foram vistas nesta máquina.** A janela rodou 40 segundos com a bandeja
"iniciada" e nenhum ser humano poderia ter interagido com ela.

### T3 — a janela compacta SUBIU. É a primeira foto dela desde que virou opt-in

**O cabeçalho foi corrigido** — é a única mudança de código desta frente:
`compact_window.py:1-33` agora descreve o gating OPT-IN vigente, o mesmo que
`is_enabled()` (`:71-79`) implementa, e guarda o gating antigo como histórico
datado em vez de descrevê-lo como se fosse o atual. A C2 (o log de `:114` que
culpa `=0`) e a C3 (o `troubleshooting.md`) **não foram tocadas** — estão fora
da lista de arquivos desta frente.

Prova de que o cabeçalho novo é verdadeiro e o antigo era falso, executada:

```
variável AUSENTE       -> is_enabled() = False
variável =0            -> is_enabled() = False
variável =1            -> is_enabled() = True
variável =true         -> is_enabled() = False
```

A ausência desliga tanto quanto o `=0` — que é exatamente o que o cabeçalho
antigo negava ao chamar o `=0` de opt-out. E só o `1` literal liga, nem `true`.
Os sete testes de `test_compact_window.py` seguem verdes (7 passed em 0,17 s).

Depois disso a janela subiu de verdade, com a variável ligada
(`compact_window_started size=320x90` no log, 06:17:52). **Fotos `05`, `06` e
`07`.** Quatro achados, e nenhum deles é "ela mente":

**1. Ela NÃO mente e NÃO contradiz.** Mostra `USB · Pragmata2` e `95 %` — os
mesmos transporte, perfil e bateria da janela principal aberta atrás dela, no
mesmo segundo. O que ela faz é **repetir em uma terceira grafia** (a tal do
`95 %`, tabela acima).

**2. Ela nasce no TEMA CLARO num desktop escuro.** Fundo branco, texto cinza,
enquanto a janela principal e o painel inteiro estão escuros — visível na foto
`06`. É consequência de ela ser uma `Gtk.Window` crua (`:147-217`), sem o
provider de CSS que a janela principal carrega. Os três botões (`Painel`,
`Perfil`, `Sair`) ficam cinza-claro sobre quase-branco: contraste baixo, do tipo
que a LEGIBILIDADE-01 mediria se soubesse que esta janela existe.

**3. Ela cai EM CIMA da barra de abas da janela principal.** Foto `07`: a caixa
tapa a aba `Início` inteira (só a sublinha rosa da aba ativa escapa por baixo) e
parte da `Status`. O código pede canto inferior-direito (`:166`,
`set_gravity(SOUTH_EAST)`), mas gravity sem `move()` não posiciona nada — no
XWayland do COSMIC quem escolhe é o compositor, e ele escolheu o topo. Somado ao
`set_keep_above(True)` (`:161`) e ao `set_decorated(False)` (`:164`), isso é,
por medição e não por opinião, exatamente a palavra que `app.py:1071-1075` usa
para justificar o opt-in: **intrusiva**. A decisão de manter opt-in está certa,
e agora tem foto.

**4. O achado sério: a única saída visível dela DESLIGA O HEFESTO INTEIRO.** Sem
moldura não há X. O que sobra é o botão `Sair` (`:210-211`), que chama
`self.on_quit()` — e `app.py:1079` passa `on_quit=self.quit_app`, que dispara o
`_shutdown_backend` (`:492-552`): `systemctl --user stop` da unit **mais**
`SIGTERM` no PID de `daemon.pid`. Fechar a janelinha pelo `delete-event`
(`:219-225`) faz a mesma coisa. Quem abrir a compacta achando que é um widget e
clicar em `Sair` para tirá-la da frente **para o controle**, não fecha a caixa.
Se a decisão da E3 for manter o módulo, isto entra junto.

**Nota de método, e ela vale para quem repetir isto:** a GUI que eu subi foi
encerrada com `SIGKILL`, nunca `SIGTERM`. `SIGTERM` na GUI cai no
`_on_term_signal` (`app.py:171-194`), que agenda `quit_app` — o mesmo caminho
acima — e **teria derrubado o daemon dela**. Medido antes de matar, e conferido
depois: daemon 3615, broker 4455 e applet 4505 seguem vivos, com `etime`
contínuo, e o socket responde com o mesmo estado de antes.

**Ruído de fundo registrado sem culpado:** os 40 segundos de GUI produziram 84
`Gtk-CRITICAL: gtk_box_gadget_distribute: assertion 'size >= 0' failed in
GtkNotebook`, cerca de dois por segundo, enquanto a janela estava só parada na
Início. Não atribuo à compacta nem à minha edição (mexi em docstring): outras
frentes editavam `app.py` e `status_actions.py` no mesmo minuto. Fica como
achado para quem for medir o custo da janela parada. Log em
`assets/2026-07-31-onda2/log-gui-compacta-06h17.txt`.

### O que esta rodada NÃO mediu

- **O popover aberto.** Proibido clicar por coordenada; é o único jeito de abrir.
  A reconstrução acima é derivação de código com estado medido, não foto.
- **A geometria do popover.** Segue sem régua, como o corpo da sprint já dizia.
- **A D5.** Continua precisando de dois controles na mesa. Com um controle só,
  `players_hint()` devolve `None` e a frase nem aparece.
- **A bandeja com o watcher ligado.** Não mexi no painel dela. Saber o que a
  bandeja desenha de fato continua dependendo de uma linha no `plugins_wings`,
  e isso é decisão dela.
- **O teste de coerência de texto que a E3 pede.** `tests/` está fora da lista
  de arquivos desta frente. Registrado: **a correção do cabeçalho entrou sem
  teste que a guarde** — hoje nada impede alguém de escrever o gating antigo
  de volta. É exatamente o portão que a E4 propõe, e ele continua devendo.

---

## NOTA DATADA — 09/08/2026: a E4 saiu, e o D1 continua aberto POR MEDIÇÃO

**Nada acima foi apagado.** As três superfícies medidas, as quatro entregas e os
quatro achados continuam inteiros — inclusive o parágrafo logo acima, que dizia
que a E4 devia. **Esta nota é a resposta a ele.**

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **E4.** Uma regra que impeça a próxima renomeação de esquecer as outras três superfícies | ENTREGUE EM CÓDIGO | `tests/unit/test_vocabulario_das_quatro_superficies.py:1` — *"a mesma coisa tem de ter o mesmo nome nas QUATRO superfícies"*; a mensagem de reprovação em `:268` diz, por extenso, o que fazer quando *"RADAR-01 foi curada"* |

**Commit:** `c10adaf`, 01/08/2026.

### Por que a E4 é ENTREGUE EM CÓDIGO e não ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA

Porque **portão não pede validação dela**: ele reprova ou não reprova, e quem o
valida é o CI. Este é o único caso desta remarcação em que a distinção entre
*entregue no código* e *validado por ela* não se aplica.

### O D1 continua ABERTO — e quem registra isso é o próprio teste

O `tests/unit/test_vocabulario_das_quatro_superficies.py:230` grava, em
comentário: *"D1 da RADAR-01, remedida em 01/08/2026 e AINDA ABERTA"* — e a
remedição achou **uma terceira lista** que esta sprint não tinha aberto: a aba
**Perfis** concorda com o applet e discorda da aba **Início**. Não é o applet
contra a janela; é a janela contra si mesma.

**Quem decide a ordem canônica das máscaras é ela, com o painel aberto na
frente** — o teste diz isso com todas as letras, e é por isso que o D1 não
entra nesta remarcação como entregue.

### E as E1, E2 e E3 continuam ABERTAS

O applet, a bandeja e o destino da janela compacta seguem sem decisão. A E3
recebeu, em 31/07, apenas o conserto de cabeçalho já registrado no corpo deste
documento — e **sem teste que o guarde**, como o parágrafo acima diz.
