# EMULACAO-NO-JOGO-01 — o R1 troca de aplicativo em vez de jogar

- **Status:** **PARCIAL — as E1, E1(b) e E2 estão ENTREGUES EM CÓDIGO,
  AGUARDANDO A PALAVRA DELA; as E3 e E5 seguem ABERTAS.** Remarcada em
  09/08/2026: entraram em `2bbfa22` (30/07/2026), com o interruptor do teclado
  persistido. **Rótulo anterior: "ABERTA — medida ponta a ponta, nenhuma linha
  de código escrita"**, preservado aqui, porque descrevia com exatidão a rodada
  de abertura. Ver a nota datada no fim
- **O que falta ela validar, em uma linha:** abrir o jogo, apertar R1 durante a
  partida e ver que **não troca mais de aplicativo** — e que o interruptor do
  teclado continua como ela deixou depois de fechar e reabrir a janela
- **Prioridade:** CRÍTICA — não é cosmético e não é "estranho": o controle dela
  arranca o foco do jogo no meio da partida, e o único jeito que ela achou de
  parar é um botão que a própria janela deixa cinza na hora em que ele resolve
- **Faixa:** 1 — o produto atrapalha o uso que ele existe para servir
- **Aberta em:** 29/07/2026, a partir da queixa dela de hoje
- **Pedido dela:** *"inicio o jogo e ele quando aperto r1 muda de app ao invés de
  funcionar no jogo"* — transcrição literal completa na seção abaixo, sem
  correção de grafia
- **Impacto para ela:** o controle arranca o foco do jogo no meio da partida, e
  o Alt esquerdo chega a ficar **segurado por 33 segundos** com o trocador de
  aplicativos aberto na tela dela (medido no journal). O único jeito que ela
  achou de parar é um botão que a janela deixa **cinza** exatamente quando ele
  resolve
- **Medido no daemon vivo desta máquina** (PID 2430, de pé desde 16:50 de hoje),
  no journal do usuário dela e nos arquivos de configuração em
  `~/.config/hefesto-dualsense4unix/`. Nada foi executado do projeto: nem
  instalação, nem suíte, nem reinício de daemon.

## O sintoma, nas palavras dela

Transcrito **literalmente**, sem correção de grafia nem de acento — é o que ela
escreveu:

```
inicio o jogo e ele quando aperto r1 muda de app ao invés de funcionar no jogo
```

E, no mesmo relato, o raciocínio dela — que está **correto** e é o que aponta o
defeito:

```
eu abro a aba emulacao e ativo o modo jogo e ele volta a funcionar, mas e
estranho pq se eu to com o modo mouse teclado desligado nao deveria impactar ne?
```

Não deveria. E o motivo de impactar é que o interruptor que ela desligou governa
**só o mouse**. O teclado emulado nunca teve interruptor nenhum.

## O esclarecimento dela que fecha uma ambiguidade antiga do projeto

Ela disse hoje, com todas as letras: quando ela fala **"modo jogo"**, ela quer
dizer **suspender mouse e teclado** — o `_emulation_suppressed`.

Isso resolve um vocabulário que o projeto arrastava. Hoje "modo jogo" nomeia
**três coisas diferentes** dentro da mesma janela:

| Onde | O que o texto chama de "modo jogo" | O que é de verdade |
|---|---|---|
| `gui/main.glade:2465` (rótulo da linha) + `:2505` (botão) | "Modo jogo:" / "Suspender mouse e teclado" | `_emulation_suppressed` — **o que ela quer dizer** |
| `gui/main.glade:2485-2487` (comentário do BOTAO-QUE-NAO-MENTE-01) | *"este botão... NÃO liga o modo jogo... Quem liga o modo jogo é 'Jogar pelo Hefesto', na aba Início"* | o **vpad** (gamepad virtual) |
| `gui/main.glade:2270` | *"Modo jogo: segure o botão PS para suspender a emulação de mouse/teclado"* | um gesto que está **desligado por padrão** (`daemon/lifecycle.py:158`, `ps_long_press_ms: int = 0`) |

O projeto decidiu, por escrito em `gui/main.glade:2487`, que "modo jogo" é o
vpad. **Ela decidiu o contrário**, e ela é a dona. De agora em diante, nesta
sprint e nas que a citarem: **"modo jogo" = suspender mouse e teclado =
`_emulation_suppressed`**. O que liga o vpad se chama pelo nome — vpad, gamepad
virtual, ou máscara.

O rótulo de `gui/main.glade:2270` é o terceiro problema desse conjunto: ele
promete um gesto ("segure o botão PS") que `daemon/lifecycle.py:158` desliga por
padrão. O gesto vivo é PS+Options (`daemon/subsystems/hotkey.py:73-79`,
`build_ps_long_press_callback`, cujo callback só é armado com
`ps_long_press_ms > 0` em `daemon/subsystems/hotkey.py:189`).

## O que foi medido — a cadeia, elo por elo

### Elo 1 — ela abre um jogo que está na allowlist do Steam Input

Pragmata é o appid `3357650`, e ele está no arquivo dela:
`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`, **linha 16** (o outro
jogo medido hoje, Mullet Mad Jack `2111190`, está na linha 10). O arquivo tem
mtime 26/07 23:36 — foi escrito pelo DUPLO-REGISTRO-01.

### Elo 2 — o Hefesto arma a exceção do Steam Input

`daemon/subsystems/gamepad.py:465` grava
`daemon._steam_input_vpad_suspenso = True` e `:479` loga. No journal dela, hoje:

```
2026-07-29T18:53:01.426275 steam_input_vpad_suspenso appid=3357650 flavor=dualsense jogadores_coop=0
```

### Elo 3 — a exceção **derruba o vpad**, de propósito

`daemon/subsystems/gamepad.py:477` chama
`stop_gamepad_emulation(daemon, persist=False, release_grab=False)`. Dentro dele,
`gamepad.py:1473` zera o slot (`daemon._gamepad_device = None`),
`gamepad.py:1476` zera a config viva
(`daemon.config.gamepad_emulation_enabled = False`) e `gamepad.py:1492` loga:

```
2026-07-29T18:53:01.426254 gamepad_emulation_stopped
```

Isto **não é bug**: é a proteção que existe para o controle não aparecer
duplicado no jogo que o Steam Input já cuida. Ela é a porta, não o culpado.

### Elo 4 — sem vpad, o despacho do gamepad não acontece

No laço de leitura, `daemon/lifecycle.py:3181` gateia o despacho em
`self._gamepad_device is not None`. Com o slot `None`, a variável local
`gamepad_dispatched` (inicializada `False` em `daemon/lifecycle.py:3180`, só
viraria `True` em `:3189`) fica **False** no tique inteiro.

### Elo 5 — a exclusão mútua está escrita ao contrário do que ela precisa

`daemon/lifecycle.py:3266`:

```python
if not gamepad_dispatched:
```

A **ausência** do vpad é lida como **permissão** para a emulação de desktop
entrar. O comentário logo acima, em `daemon/lifecycle.py:3262-3264`, declara a
intenção certa — *"com o gamepad ligado, o controle vai pro jogo, não pro
cursor/teclado"* — mas o predicado não distingue **"vpad desligado porque ela
está no desktop"** de **"vpad desligado porque o JOGO assumiu"**.

### Elo 6 — o mouse não passa, e é por isso que ela acredita que está tudo desligado

`daemon/lifecycle.py:3267` exige `self._mouse_device is not None and emu_active`.
O device não existe: `daemon/subsystems/mouse.py:35` recusa criá-lo
(`if not cfg.mouse_emulation_enabled: return`), o default é `False` em
`daemon/lifecycle.py:125`, e o boot só o liga quando o arquivo em disco diz
`on` (`daemon/lifecycle.py:574-576`, via `load_mouse_emulation()`; o start em
`daemon/lifecycle.py:616-617`).

O arquivo dela, lido do disco:

```
~/.config/hefesto-dualsense4unix/mouse_emulation.flag
{"enabled": false, "speed": 9, "scroll_speed": 1}
```

**O mouse está honestamente desligado.** O cursor não se mexe, e ela conclui —
corretamente, pelo que a interface lhe diz — que "o modo mouse teclado está
desligado".

### Elo 7 — o teclado passa, porque o device dele nunca é `None`

`daemon/lifecycle.py:3278` exige `self._keyboard_device is not None and
emu_active`. Os dois gates são **simétricos**; a assimetria mora um nível acima,
na criação do device:

| | mouse | teclado |
|---|---|---|
| default na config | `False` — `daemon/lifecycle.py:125` | **`True`** — `daemon/lifecycle.py:149` |
| gate na criação | `daemon/subsystems/mouse.py:35` recusa sem o flag | `daemon/subsystems/keyboard.py:128-160` não consulta nada |
| arquivo em disco | `mouse_emulation.flag` | **não existe** |
| par save/load | `utils/session.py:285`/`:346`/`:357`/`:367` | **não existe** |
| chave no `state_full` | `daemon/ipc_handlers.py:1436-1441` | **não existe** |
| `GtkSwitch` na janela | `mouse_emulation_toggle`, `gui/main.glade:2677` | **não existe** |

O próprio subsystem admite a assimetria por escrito, em
`daemon/subsystems/keyboard.py:4-7`:

> *"Ativado por padrão (não depende de toggle explícito como
> `mouse_emulation_enabled`)"*

E `daemon/lifecycle.py:149` diz o motivo histórico:

> *"Default True: infraestrutura já sobe com os bindings default
> (Options/Share/L1/R1). Sub-sprints futuras expõem UI+persist."*

**As sub-sprints futuras nunca vieram.** `grep -rn keyboard_emulation_enabled
src/` devolve cinco linhas, todas de leitura interna:
`daemon/subsystems/keyboard.py:12` (docstring), `daemon/lifecycle.py:149` (o
default), `:620` (o boot), `:964-965` (o reload). Nenhum IPC dedicado, nenhuma
CLI, nenhum arquivo.

### Elo 8 — o perfil dela tem `key_bindings: null`, e `null` significa HERDAR TUDO

O perfil ativo é `Pragmata2` (`~/.config/hefesto-dualsense4unix/session.json` =
`{"last_profile": "Pragmata2"}`), e ele tem `"key_bindings": null`.

`profiles/manager.py:737-738`:

```python
if raw is None:
    return dict(DEFAULT_BUTTON_BINDINGS)
```

A docstring acima diz a regra em três linhas (`profiles/manager.py:733-735`):
`None` herda o mapa default completo, `{}` é teclado silencioso, dict parcial é
override isolado. **Ela nunca escolheu `null`** — é o que o "Salvar Perfil"
grava (ver a sprint irmã, PERFIL-SALVA-TUDO-01).

Dos 15 perfis dela, **apenas um** tem `key_bindings` próprio:
`point_and_click.json`. Os outros 14 herdam o mapa default inteiro.

### Elo 9 — no mapa default, R1 é um atalho de trocar de aplicativo

`core/keyboard_mappings.py:41-63`, na letra:

| botão | teclas | o que faz no compositor |
|---|---|---|
| `r1` (`:45`) | `KEY_LEFTALT` + `KEY_TAB` | **troca de aplicativo** |
| `l1` (`:44`) | `KEY_LEFTALT` + `KEY_LEFTSHIFT` + `KEY_TAB` | troca de aplicativo, para trás |
| `options` (`:42`) | `KEY_LEFTMETA` | abre o lançador do COSMIC |
| `create` (`:43`) | `KEY_SYSRQ` | captura de tela |
| `touchpad_left_press` (`:60`) | `KEY_BACKSPACE` | apaga |
| `touchpad_middle_press` (`:61`) | `KEY_ENTER` | confirma |
| `touchpad_right_press` (`:62`) | `KEY_DELETE` | apaga |

Os dois botões de ombro — que praticamente todo jogo usa — carregam atalhos
**globais do compositor**.

### Elo 10 — quem emite é o teclado virtual, e só ele

`grep -rn key_binding_emit src/` devolve **duas** linhas, ambas em
`integrations/uinput_keyboard.py` (`:230` e `:254`). Não há terceiro emissor.

No journal dela, nos últimos 7 dias, o conjunto **completo** de emissões:

```
$ journalctl --user --since '7 days ago' -o cat \
    | grep -oE "key_binding_emit +button=[a-z0-9_]+ +keys=\[[^]]*\]" \
    | sort | uniq -c
     18 key_binding_emit  button=r1      keys=['KEY_LEFTALT', 'KEY_TAB']
      2 key_binding_emit  button=options keys=['KEY_LEFTMETA']
```

Duas linhas. Nenhum outro botão em sete dias. **O R1 é o único gesto que ela de
fato dispara** — 18 emissões, que são 9 pressionamentos e 9 soltas.

### Elo 11 — o Alt+Tab arranca o foco, e o jogo "não funciona"

Efeito relatado por ela: *"muda de app ao invés de funcionar no jogo"*.

### Elo 12 — a correlação: 9 de 9, nenhuma fora

**Todos** os 9 pressionamentos de R1 dos últimos 7 dias caem **dentro** de uma
janela de `steam_input_vpad_suspenso`. Zero fora. A linha do tempo pareada, lida
do journal dela:

```
28/07 23:03:36.661  steam_input_vpad_suspenso appid=3357650
28/07 23:03:49.737    key_binding_emit r1  phase=press
28/07 23:03:49.789    key_binding_emit r1  phase=release
28/07 23:04:47.991    key_binding_emit r1  press
28/07 23:04:48.516    key_binding_emit r1  release
28/07 23:04:48.709    key_binding_emit r1  press          <-- Alt fica SEGURADO
28/07 23:04:48.742  steam_input_vpad_retomado
28/07 23:04:50.892  steam_input_vpad_suspenso appid=3357650
28/07 23:04:50.897    key_binding_emit r1  release
28/07 23:04:54.578    key_binding_emit r1  press          <-- Alt fica SEGURADO
28/07 23:04:55.899  steam_input_vpad_retomado
28/07 23:05:27.946    key_binding_emit r1  release        <-- 33 SEGUNDOS depois
28/07 23:05:27.946  emulation_suppressed_changed suppressed=True
28/07 23:16:39.454  steam_input_vpad_suspenso appid=3357650
28/07 23:16:44.752    key_binding_emit r1  press
28/07 23:16:44.908    key_binding_emit r1  release
28/07 23:16:45.030    key_binding_emit r1  press
28/07 23:16:45.115    key_binding_emit r1  release
28/07 23:16:45.202    key_binding_emit r1  press
28/07 23:16:45.325    key_binding_emit r1  release
28/07 23:16:45.462  steam_input_vpad_retomado
29/07 01:47:38.024  steam_input_vpad_suspenso appid=3357650
29/07 01:52:17.267    key_binding_emit r1  press
29/07 01:52:17.407    key_binding_emit r1  release
29/07 01:52:17.653  steam_input_vpad_retomado
29/07 01:52:19.785  steam_input_vpad_suspenso appid=3357650
29/07 01:52:20.448    key_binding_emit r1  press          <-- Alt fica SEGURADO
29/07 01:52:21.787  steam_input_vpad_retomado
29/07 01:52:38.681    key_binding_emit r1  release        <-- 18 SEGUNDOS depois
29/07 01:52:38.681  emulation_suppressed_changed suppressed=True
```

A cadeia não é teórica. **É o único regime em que o defeito ocorre, e ele ocorre
sempre.**

### O achado dentro do achado — a "cura" dela, capturada duas vezes

Olhe as duas linhas marcadas com "SEGUNDOS depois". Em **28/07 23:05:27** e em
**29/07 01:52:38** aconteceu a mesma coisa, e ela é o instante exato em que ela
viu "ele volta a funcionar":

```
2026-07-29T01:52:38.681396  key_binding_emit button=r1 keys=['KEY_LEFTALT','KEY_TAB'] phase=release
2026-07-29T01:52:38.681464  emulation_suppressed_changed suppressed=True
```

**68 microssegundos de distância.** O `release` aparece **antes** do log porque
`set_emulation_suppressed` chama `_flush_emulation_devices()` em
`daemon/lifecycle.py:1394`, **antes** do `logger.info` de `daemon/lifecycle.py:1395`
— e o `_flush` existe exatamente para isso (o comentário de
`daemon/lifecycle.py:1389-1392` diz: *"senão um modificador... fica preso, já que
o poll loop para de despachar e nunca envia o release"*).

Tradução: o R1 estava **pressionado desde 01:52:20.448**. O Alt ficou segurado
por **18 segundos**, com o trocador de aplicativos aberto na tela dela — e o
clique no "modo jogo" foi o que **soltou a tecla presa**. Na noite anterior, o
mesmo, por **33 segundos**.

E o caminho completo do clique dela: `daemon/ipc_handlers.py:2752` chama
`set_emulation_suppressed(True)`; `daemon/lifecycle.py:1385` põe
`_emulation_suppressed = True`; `daemon/lifecycle.py:3265` passa a calcular
`emu_active = False`; o gate de `daemon/lifecycle.py:3278` **fecha**. O R1 para
de trocar de aplicativo — e continua parado quando ela volta ao jogo, porque a
supressão é transitória em memória e ninguém a solta (o motivo de ninguém soltar
está em "O que NÃO fazer").

### A janela de exposição, medida em minutos

Hoje o `_gamepad_device` ficou `None` por **~97 minutos**, em três episódios,
todos com jogo aberto:

| entrada | saída | duração | appid |
|---|---|---|---|
| 18:53:01 | 20:14:33 | 81 min | 3357650 (Pragmata) |
| 16:59:26 | 17:12:30 | 13 min | 3357650 (Pragmata) |
| 17:49:49 | 17:52:49 | 3 min | 2111190 (Mullet Mad Jack) |

Durante esses 97 minutos, o gate de `daemon/lifecycle.py:3278` estava **aberto** e
o teclado de desktop dela era o consumidor do R1.

## A causa

**Três ausências que se somam num quarto lugar.**

1. **A emulação de teclado não tem interruptor.**
   `daemon/lifecycle.py:149` fixa `keyboard_emulation_enabled: bool = True` e não
   existe superfície nenhuma que o desligue de forma persistente: nem arquivo
   (`utils/session.py` tem o par para mouse em `:285`/`:346` e para gamepad em
   `:386`/`:444`, e **nada** para teclado), nem `GtkSwitch` (as **três** do
   projeto são `profile_advanced_switch` em `gui/main.glade:1629`,
   `daemon_autostart_switch` em `:1924` e `mouse_emulation_toggle` em `:2677` —
   nenhuma de teclado), nem chave no `state_full`. A aba Teclado
   (`gui/main.glade:2911`, `tab_keyboard`) não tem interruptor nenhum: só o
   editor de "Atalhos de teclado do perfil ativo".

2. **O rótulo mente.** `gui/main.glade:2670` diz **"Emular mouse+teclado"** e o
   tooltip de `:2678` diz *"Liga o controle como mouse e teclado do
   computador"* — mas o handler `on_mouse_toggle_set`
   (`app/actions/mouse_actions.py:190`) só emite `mouse.emulation.set`. O
   interruptor promete duas coisas e entrega uma.

3. **A exclusão mútua é formulada pela ausência do vpad em vez da presença do
   jogo.** `daemon/lifecycle.py:3266` (`if not gamepad_dispatched:`). Por isso a
   proteção do Steam Input — que derruba o vpad **de propósito**
   (`daemon/subsystems/gamepad.py:465`, `:477`, `:1473`) — vira a porta de
   entrada da emulação de desktop **dentro** da partida.

E o quarto lugar, que é onde as três se encontram: **o único caminho automático
de supressão nunca roda para ela.** A supressão por perfil
(`suppress_desktop_emulation`, `profiles/schema.py:444`, aplicada em
`daemon/lifecycle.py:1462-1465` via o applier injetado em
`profiles/manager.py:463-480`) depende de um perfil ser **ativado** sobre a
janela do jogo. Os cinco perfis que competem na máquina dela são todos
`match: {"type": "any"}` — e o veto R-21 recusa autoridade a catch-all sobre
janela de jogo. Journal de hoje:

```
2026-07-29T18:53:00.631528 profile_select_catch_all_sem_autoridade_em_jogo \
  candidatos=['Pragmata', 'Pragmata2', 'fallback', 'meu_perfil', 'vitoria'] \
  wm_class=steam_app_3357650
2026-07-29T18:53:00.631621 autoswitch_congelado_pelo_cadeado candidate= current= wm_class=steam_app_3357650
```

Candidato **vazio**. Nenhum perfil ativado. Logo `apply_profile_suppression`
(`daemon/lifecycle.py:1399`) **nunca é chamado** e o campo nunca é lido.

E o "modo jogo padrão" que existe justamente para tapar esse buraco
(`daemon/lifecycle.py:1785`, `aplicar_modo_jogo_padrao`) só aplica
`ProfileModeConfig(kind="gamepad")` (`daemon/lifecycle.py:1856-1861`) — ele mexe
no **vpad** e não toca em `_emulation_suppressed`. Medido, no mesmo segundo:

```
2026-07-29T18:53:01.136495 profile_mode_aplicado flavor=dualsense kind=gamepad \
  ligou_gamepad=False origin=game_signal wm_class=steam_app_3357650
2026-07-29T18:53:01.426198 launch_env_materializado arquivos=4 backends=[] emulacao=False mascara=dualsense
```

Ele sai com `ligou_gamepad=False` (o vpad já vivia) e, três décimos de segundo
depois, o Steam Input derruba o vpad de qualquer jeito.

## O que NÃO é a causa

Cada item abaixo tem a medição que o descarta. **Esta seção existe para a próxima
pessoa não percorrer o mesmo beco.**

### O gate do teclado NÃO está escrito diferente do gate do mouse

Hipótese natural: "o gate do teclado checa `not _emulation_suppressed` mas não
checa a flag de habilitado". **REFUTADA na letra.** Lado a lado:

```
daemon/lifecycle.py:3267   if self._mouse_device is not None and emu_active:
daemon/lifecycle.py:3278   if self._keyboard_device is not None and emu_active:
```

Os dois são **simétricos**: os dois checam device-existe **e** `emu_active`. O
gate está certo. **O que nunca fica `None` é o device** — e isso se decide um
nível acima, em `daemon/subsystems/mouse.py:35` (que recusa criar) contra
`daemon/subsystems/keyboard.py:128-160` (que não consulta nada além do default
`True`).

### NÃO é o `HotkeyManager`, nem o gamepad virtual, que gera o Alt+Tab

**REFUTADA.** `grep -rn key_binding_emit src/` devolve duas linhas, ambas em
`integrations/uinput_keyboard.py` (`:230`, `:254`) — a emissão do journal dela
nasce comprovadamente do teclado virtual de **desktop**. Os combos do
`HotkeyManager` são PS+Options e PS+dpad, e ele só **subtrai** botões do
despacho (`daemon/lifecycle.py:3256-3262`), nunca emite tecla. E no gamepad
virtual `r1` é `BTN_TR` (`integrations/uinput_gamepad.py:162`) — botão de
gamepad, não tecla.

### NÃO é o interruptor dela escrevendo num lugar que o daemon não lê

**REFUTADA para o mouse.** O caminho fecha inteiro:
`app/actions/mouse_actions.py:190` -> IPC `mouse.emulation.set` ->
`daemon/subsystems/mouse.py` -> `save_mouse_emulation_enabled`
(`utils/session.py:357`) -> `mouse_emulation.flag`, e o daemon lê no boot em
`daemon/lifecycle.py:574-576`. **O flag dela (`enabled: false`) está sendo
obedecido** — é por isso que o mouse realmente não emula.

A variante **viva** desta hipótese é outra e mais grave: para o teclado **não há
lugar nenhum para escrever**, logo não há o que ler.

### NÃO é o cadeado de autoswitch

**REFUTADA.** O cadeado dela está ligado
(`~/.config/hefesto-dualsense4unix/autoswitch_locked.flag` = `1`, mtime 28/07
18:18) e congela a decisão de **perfil**. O despacho de teclado em
`daemon/lifecycle.py:3278` não o consulta em nenhum ponto. Mesmo com o cadeado
desligado o R1 sairia igual, porque o veto R-21 recusaria os catch-all dela sobre
janela de jogo de qualquer modo.

### NÃO resolve pôr `suppress_desktop_emulation: true` no Pragmata2

**REFUTADA na prática.** `Pragmata2` é `match: {"type": "any"}` (medido no
arquivo). O veto R-21 não dá autoridade a catch-all sobre janela de jogo, o
candidato sai **vazio** (`profile_select_catch_all_sem_autoridade_em_jogo`, no
journal de hoje) e o perfil não é ativado — logo `apply_profile_suppression`
(`daemon/lifecycle.py:1399`) nunca é chamado e o campo nunca é lido. Só
funcionaria com um perfil `criteria` por appid, feito à mão. Comparação medida:
os **únicos dois** perfis dela com `suppress_desktop_emulation: true` são
`sackboy_nativo.json` e `coop_local.json`, e os dois casam por `criteria`, não
por `any`.

### NÃO é o "modo jogo padrão" que já cobre isso

**REFUTADA.** `daemon/lifecycle.py:1785` só aplica
`ProfileModeConfig(kind="gamepad")` (`:1856-1861`) e **nunca** toca
`_emulation_suppressed`. Medido sete vezes hoje no journal dela, sempre igual:
`profile_mode_aplicado ... kind=gamepad ligou_gamepad=False origin=game_signal`.

### PREMISSA DESTA SESSÃO CORRIGIDA — o vpad NÃO "já vive sempre ligado por flag"

Esta sessão começou com a premissa de que o vpad dela vive permanentemente ligado
porque `gamepad_emulation.flag` diz `dualsense`. **REFUTADA por medição.** O
`_gamepad_device` ficou `None` por ~97 minutos **hoje**, em três episódios (tabela
acima), sempre por `steam_input_vpad_suspenso`.

Pior: `stop_gamepad_emulation` zera `config.gamepad_emulation_enabled`
(`daemon/subsystems/gamepad.py:1476`) **mesmo com `persist=False`** — o flag em
disco continua dizendo `dualsense`, mas a config viva vai a `False`. É exatamente
nesses 97 minutos que a emulação de desktop esteve solta.

**Regra que sai daqui:** ao medir estado de vpad, ler o **journal**
(`gamepad_emulation_started`/`_stopped`, `steam_input_vpad_suspenso`/`_retomado`),
nunca o flag em disco.

## As entregas

Ordenadas por preço crescente. **E0 não é código.**

### E0 — a decisão de vocabulário, e ela é dela

**O que faz:** fixa, num ADR ou no glossário do projeto, que "modo jogo"
significa **suspender mouse e teclado** (`_emulation_suppressed`), como ela
esclareceu hoje. O que liga o vpad passa a se chamar vpad/gamepad virtual/máscara
em toda superfície.

**Os arquivos:** `docs/adr/` (decisão nova); `gui/main.glade:2270` (o rótulo que
promete um gesto desligado por padrão); `gui/main.glade:2485-2503` (o comentário
que decidiu o contrário, e que precisa ser corrigido para não contradizer o ADR);
os rótulos de `app/actions/emulation_actions.py:664` e `:667`, que já usam o
sentido dela.

**Como provar:** portão de texto que varre as superfícies de usuária
(`gui/main.glade` e os `_toast_*`) e reprova a expressão "modo jogo" aplicada ao
vpad. Arrancar a decisão faz o portão perder o critério — e é por isso que ela
tem de estar escrita, não combinada.

**Risco:** BAIXO em código, e é a entrega que **impede** as outras de brigarem
entre si. Sem ela, E3 e E4 vão inventar nomes novos para as mesmas três coisas.

### E1 — enquanto o vpad estiver suspenso pelo Steam Input, o desktop não entra

**O que faz:** fecha a fresta **medida**. Hoje `daemon/lifecycle.py:3266` lê a
ausência do vpad como permissão; a entrega acrescenta o único termo que faltava:

```python
if not gamepad_dispatched and not steam_input_vpad_suspenso(self):
```

O predicado público **já existe** — `daemon/subsystems/gamepad.py:310-326` — e a
docstring dele diz, com todas as letras, que foi escrito para responder *"por que
a emulação aparece desligada com o jogo aberto?"*. É leitura de atributo em
memória (`gamepad.py:326`), sem I/O, própria para caminho quente.

Cobre **9 de 9** episódios medidos no journal dela. Não muda mapa, não muda
perfil, não muda estado persistido.

**Os arquivos:** `daemon/lifecycle.py:3266` (o predicado); o import de
`steam_input_vpad_suspenso` de `daemon/subsystems/gamepad.py:310`; teste novo em
`tests/unit/`.

**Como PROVAR (o teste que morde):** daemon dublado com
`_gamepad_device=None`, `_steam_input_vpad_suspenso=True`,
`_emulation_suppressed=False`, `_keyboard_device` = espião que registra cada
`dispatch()`, e um tique do laço com `r1` pressionado. Asserção **dupla**:

1. o espião recebeu **zero** chamadas; **e**
2. o espelho legítimo — mesmo tique com `_steam_input_vpad_suspenso=False` —
   recebeu `frozenset({"r1"})`.

**Morde:** arrancando o novo termo do predicado, o assert (1) quebra na hora — o
espião recebe `r1`. E o assert (2) é o que impede a cura de virar "desligar o
teclado para sempre": um teste que só olhasse o caso suspenso passaria com o gate
quebrado ao contrário.

**Risco:** BAIXO. Risco residual: se a exceção do Steam Input ficar pendurada sem
o vigia devolver o vpad, o mouse/teclado de desktop fica morto até o vpad voltar.
Mitigado no código que já existe: `daemon/subsystems/gamepad.py:449-457` **recusa
suspender** sem vigia armado (loga `steam_input_vpad_mantido_de_pe`), e o vigia
roda a 1 Hz (`daemon/subsystems/gamepad.py:329+`). **Confirmar na tela dela** que
o desktop volta ao fechar o jogo.

### E2 — generalizar para QUALQUER jogo, não só os da allowlist

**O que faz:** gateia a emulação de desktop por `display_authority == "game"`
(`daemon/lifecycle.py:2802-2811`), o sinal do NUMA-01 que já correlaciona janela
+ marcador do wrapper + pid vivo. Cobre jogo nativo, Lutris, Heroic e jogo Steam
**fora** da allowlist — casos em que o vpad continua de pé e portanto E1 não se
aplica, mas em que a emulação de desktop também não deveria ter voz.

**Importante:** é um gate de **leitura no despacho**, não uma escrita em
`_emulation_suppressed`. O porquê está em "O que NÃO fazer" — escrever ficaria
**preso** justamente na máquina dela.

**Os arquivos:** `daemon/lifecycle.py:3265-3266` (compor a autoridade no cálculo
de `emu_active`, ou num predicado nomeado ao lado dele); `tests/unit/`.

**Como PROVAR (o teste que morde):** três casos num daemon dublado:

| caso | `display_authority` | `_gamepad_device` | espião de teclado |
|---|---|---|---|
| jogo fora da allowlist, vpad de pé | `"game"` | não-`None` | **zero** |
| jogo nativo sem vpad | `"game"` | `None` | **zero** |
| desktop de verdade | `"daemon"` | `None` | **recebe `r1`** |

**Morde:** com o termo de autoridade arrancado, o segundo caso passa a despachar
e o teste falha. E o terceiro caso é o que impede a cura de virar "desligar o
teclado para sempre" — arrancar o teclado inteiro **também** reprova.

**Risco:** MÉDIO, e o risco é de **percepção**, não de código.
`display_authority` é **sticky** na queda — `daemon/lifecycle.py:1607` diz por
escrito que ele é *"sticky por 30 s"*, e `daemon/lifecycle.py:1995-1999` explica
por que a histerese existe (fail-safe para operação destrutiva). Ao fechar o
jogo, o mouse/teclado de desktop pode ficar mudo por até 30 s — **ela vai sentir
isso como "o controle morreu"**. Se incomodar, a saída é a assimetria que o R-02
já usa: **a janela crua LIBERA, a sticky BLOQUEIA** (o predicado cru já existe:
`_janela_de_jogo_em_foco`, `daemon/lifecycle.py:1603-1612`, cuja docstring
descreve exatamente essa escolha).

### E3 — a janela para de mentir durante a partida

**O que faz:** hoje, com o vpad suspenso, `mode_of_state`
(`app/actions/mode_transition.py:233-247`) devolve `MODE_DESKTOP`, porque lê
`gamepad_emulation.enabled` (`daemon/ipc_handlers.py:1443-1447`) — que
`stop_gamepad_emulation` zerou em `daemon/subsystems/gamepad.py:1476`.
Consequências medidas por leitura:

- a aba Início diz **"Controlar o PC" no meio do jogo**;
- e, pior, `_sync_gamemode_button`
  (`app/actions/emulation_actions.py:491-493`) faz
  `blocked = mode is None or mode in {MODE_DESKTOP, MODE_NATIVE}` e
  **desabilita** o botão "Suspender mouse e teclado" (`gui/main.glade:2505`)
  exatamente em `MODE_DESKTOP`. **O único botão que curava o problema dela fica
  cinza na hora em que ela precisa dele.**

O comentário de `gui/main.glade:2491-2494` já registrava essa inversão em outro
contexto: *"este aqui NASCE CINZA justamente em 'Controlar o PC', que é onde ela
mais espera que funcione"*.

A entrega: expor `steam_input_vpad_suspenso` no `daemon.state_full` (a docstring
de `daemon/subsystems/gamepad.py:313-325` já descreve esse payload como pendência
da Entrega 2 do JOGO-01, e diz que quem ligar a frase lê **o par** "exceção
ativa" + "vpad suspenso"); fazer `mode_of_state` não chamar isso de desktop;
manter o botão sensível; e trocar o rótulo "Emular mouse+teclado"
(`gui/main.glade:2670`) por "Emular mouse" enquanto o teclado não tiver
interruptor próprio (E4).

**Os arquivos:** `daemon/ipc_handlers.py:1443-1447` (o bloco
`gamepad_emulation` do `state_full`);
`app/actions/mode_transition.py:233-247` (`mode_of_state`);
`app/actions/emulation_actions.py:491-493` (`_sync_gamemode_button`) e
`:544-559` (o label de estado); `gui/main.glade:2670` e `:2678` (rótulo e
tooltip); `tests/unit/`.

**Como PROVAR (o teste que morde):** testes de função **pura**, sem GTK:

1. `mode_of_state({"native_mode": False, "gamepad_emulation": {"enabled": False},
   "steam_input_vpad_suspenso": True})` **não** devolve `MODE_DESKTOP`;
2. o mesmo payload com `steam_input_vpad_suspenso: False` **devolve**
   `MODE_DESKTOP` (o desktop de verdade continua sendo desktop);
3. o predicado de bloqueio do botão devolve "sensível" para o payload de
   jogo-com-vpad-suspenso;
4. teste de **texto**: nenhum rótulo da janela promete "teclado" num controle que
   só governa mouse — a busca por `mouse+teclado` junto do id
   `mouse_emulation_toggle` no `gui/main.glade` tem de dar zero.

**Morde:** revertendo `mode_of_state`, (1) e (3) quebram; revertendo o rótulo, (4)
quebra; e (2) impede a cura de virar "nunca mais existe modo desktop".

**Risco:** MÉDIO-BAIXO em código, **ALTO em precisar do olho dela**.
`mode_of_state` é ponto **único** de leitura de modo, e a docstring de
`app/actions/mode_transition.py:236-238` diz por que ele existe: *"a Início e a
Emulação derivavam o modo do mesmo payload com regras próprias e podiam
discordar"*. Inventar um terceiro estado ad-hoc em um dos consumidores reabre a
divergência entre abas que o HARM-01 curou. **Não inventar um quarto valor na
enum de modos sem decisão dela.**

### E4 — dar ao teclado o interruptor que ele nunca teve

**O que faz:** persistência **simétrica** à do mouse — `keyboard_emulation.flag`
em `~/.config/hefesto-dualsense4unix/`, escrito por IPC
`keyboard.emulation.set`, lido no boot, exposto no `state_full`, e com uma
`GtkSwitch` própria na aba Teclado (que hoje não tem nenhuma —
`gui/main.glade:2911`). Depois disso o rótulo "Emular mouse+teclado" volta a
poder dizer a verdade, e a frase dela — *"estou com o modo mouse teclado
desligado"* — passa a descrever uma configuração que **existe** e é obedecida.

**Os arquivos:** `utils/session.py` (par save/load ao lado de `:285`/`:346`/
`:357`/`:367`); `daemon/lifecycle.py:149` (o default deixa de ser constante),
`:620-621` (boot) e `:964-968` (o reload, que **já** sabe ligar e desligar o
subsystem em resposta a uma mudança — só nunca recebe uma);
`daemon/subsystems/keyboard.py:128-160` (gate de criação, espelhando
`daemon/subsystems/mouse.py:35`); `daemon/ipc_handlers.py` (método novo + bloco
`keyboard_emulation` no `state_full`); `gui/main.glade:2911+` e um
`app/actions/keyboard_actions.py` <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->
a criar; `tests/unit/`.

**Como PROVAR (o teste que morde):**

1. round-trip em disco: escreve `False`, lê `False`;
2. teste de boot: com o flag em `{"enabled": false}`, depois de
   `start_keyboard_emulation` o `_keyboard_device` é `None` **e** um tique com
   `r1` pressionado não emite nada;
3. **o teste de simetria, que é o que morde de verdade:** uma tabela que afirma
   que mouse e teclado têm o **mesmo conjunto de cinco superfícies** — default na
   config, gate de criação no subsystem, flag em disco, chave no `state_full`,
   interruptor na janela. **Arrancar qualquer uma das cinco do teclado reprova**;
4. não-regressão do `point_and_click`: com o flag ligado, `r1` continua saindo
   como `KEY_DOT` (o binding próprio do perfil dela, resolvido em
   `profiles/manager.py:738-739`), não como Alt+Tab.

**Risco:** MÉDIO, e **a decisão do default de instalação nova é dela**: deixar
`True` preserva o comportamento histórico; deixar `False` torna o teclado opt-in
como o mouse.

Cuidado medido, que a janela **tem** de dizer: desligar o teclado não desliga só
o Alt+Tab. Desliga também o teclado virtual do sistema em L3/R3
(`core/keyboard_mappings.py:53-54`, executado pelo `_OSKController` de
`daemon/subsystems/keyboard.py:46-125`, cujo callback é registrado em
`keyboard.py:150`) e as três regiões do touchpad
(`core/keyboard_mappings.py:60-62`). **Quem usa o controle como teclado de
acessibilidade perde tudo isso de uma vez.**

### E5 — revisitar o DEFAULT, que é a escolha de projeto por trás do sintoma

**O que faz:** `r1 = KEY_LEFTALT+KEY_TAB` e
`l1 = KEY_LEFTALT+KEY_LEFTSHIFT+KEY_TAB` (`core/keyboard_mappings.py:44-45`)
põem **atalhos globais de compositor** nos dois botões de ombro — os botões que
praticamente todo jogo usa. `options = KEY_LEFTMETA`
(`core/keyboard_mappings.py:42`) é da mesma família. A entrega propõe um default
que não colida com o compositor (ou **nenhum** default nos ombros) e uma migração
que só toque perfis com `key_bindings: null`, preservando os explícitos.

**Os arquivos:** `core/keyboard_mappings.py:41-63`; uma migração em
`profiles/` (padrão dos marcadores `.modo_jogo_nos_presets_migrated` /
`.coop_default_on_migrated` que já existem no config dela); `docs/adr/` para
registrar a decisão; `tests/unit/`.

**Como PROVAR (o teste que morde):**

1. invariante: nenhum valor de `DEFAULT_BUTTON_BINDINGS` é um atalho global de
   troca de janela — uma lista negra explícita
   (`{KEY_LEFTALT, KEY_TAB}`, `{KEY_LEFTALT, KEY_LEFTSHIFT, KEY_TAB}`,
   `{KEY_LEFTMETA}`) confrontada com cada binding default. **Morde:** revertendo
   `core/keyboard_mappings.py:45` para Alt+Tab, o teste reprova **nomeando o
   botão**;
2. migração: perfil com `key_bindings` explícito (o `point_and_click` dela,
   `r1 -> KEY_DOT`) sai da migração **byte-idêntico**; perfil com `null`
   continua `null` (a herança é resolvida em `profiles/manager.py:737-738`, não
   materializada em disco).

**Risco:** **ALTO em produto**, baixo em código. Muda o que os botões fazem para
quem já usava o Alt+Tab de propósito no desktop — e alguém usa: o mapa está aí
desde o FEAT-KEYBOARD-EMULATOR-01. **Não entregar sem decisão explícita dela.**

## O que NÃO fazer

### NÃO curar escrevendo em `_emulation_suppressed` a partir do sinal de jogo

É o caminho **obvio** e ele ficaria **preso justamente na máquina dela**.

O release automático é `apply_profile_suppression(False)`
(`daemon/lifecycle.py:1466-1487`), e ele tem **duas** guardas que a configuração
dela dispara:

- `daemon/lifecycle.py:1472-1478` recusa liberar quando o perfil é catch-all sem
  opinião (retorna `IGNORADO_CATCH_ALL`, `daemon/lifecycle.py:204`);
- `daemon/lifecycle.py:1479-1485` recusa com janela de jogo em foco (retorna
  `IGNORADO_JANELA_DE_JOGO`, `daemon/lifecycle.py:205`).

Como os **cinco** perfis que competem na máquina dela são `match: {"type":
"any"}` — `pragmata`, `pragmata2`, `meu_perfil`, `vitoria`, `fallback`, medidos
nos arquivos — **nada teria autoridade para soltar**. Ela sairia do jogo com o
mouse e o teclado **mortos** e sem caminho de volta pela interface.

Curar no gate de despacho (E1/E2) não tem esse problema, porque **não há estado
para ficar preso**.

### NÃO gatear o teclado atrás de `mouse_emulation_enabled`

Parece a simetria óbvia e a economia de uma flag. Apaga junto o teclado virtual
do sistema em L3/R3 (`core/keyboard_mappings.py:53-54` +
`daemon/subsystems/keyboard.py:46-125`) e as três regiões do touchpad
(`core/keyboard_mappings.py:60-62`). Quem usa o controle como teclado de
acessibilidade **sem** querer o cursor perde tudo de uma vez, em silêncio.

### NÃO remover nem afrouxar o `if not gamepad_dispatched:` de `daemon/lifecycle.py:3266`

Ele existe **contra um bug já curado**. O comentário de
`daemon/lifecycle.py:3262-3264` e o bloco de `:3164-3179` registram o custo da
versão anterior: com o vpad e o desktop despachando juntos, o controle físico
fica EVIOCGRAB-grabado (fonte única) e o virtual para de receber — **controle
morto no jogo**, no texto do próprio código: *"real escondido + virtual mudo"*.

A cura é **estreitar** o predicado (acrescentar termos), nunca alargá-lo.

### NÃO mexer em `mode_of_state` sem cuidado

`app/actions/mode_transition.py:233-247` é ponto único por decisão, e a docstring
de `:236-238` diz por quê: Início e Emulação **já divergiram** por derivar o modo
com regras próprias. Inventar um terceiro estado ad-hoc num dos consumidores em
vez de no ponto único reabre a divergência entre abas.

### NÃO tocar nos perfis dela em disco de carona

`point_and_click.json` depende de `r1 -> KEY_DOT` e `mouse.enabled: true` — é o
**único** dos 15 perfis dela com `key_bindings` próprio. `sackboy_nativo.json` e
`coop_local.json` são os **únicos dois** com `suppress_desktop_emulation: true`.
Qualquer migração de E5 tem de deixar esses três byte-idênticos.

### NÃO confiar no `gamepad_emulation.flag` como prova de que o vpad está vivo

O flag dela diz `dualsense` e o `_gamepad_device` ficou `None` por ~97 minutos
hoje. `stop_gamepad_emulation` zera `config.gamepad_emulation_enabled`
(`daemon/subsystems/gamepad.py:1476`) mesmo com `persist=False`.

### Exige o olho dela na tela — três provas, e nenhuma é opcional

1. **Depois de E1/E2:** abrir Pragmata e apertar **R1 dentro do jogo**.
   Confirmar que a ação do jogo acontece e o compositor **não** troca de
   aplicativo. Medição paralela que confirma sem depender de impressão:
   `journalctl --user -f | grep key_binding_emit` tem de ficar **silencioso**
   durante a partida (hoje sai `button=r1 keys=['KEY_LEFTALT', 'KEY_TAB']`).
2. **Depois de E2:** **fechar** o jogo e cronometrar quanto tempo o
   mouse/teclado de desktop leva para voltar. A sticky de ~30 s
   (`daemon/lifecycle.py:1607`) vai parecer "o controle morreu". Se incomodar, é
   decisão dela entre aceitar a folga ou usar a janela crua para liberar.
3. **Depois de E3:** com o jogo **aberto**, olhar a aba Início e a aba Emulação
   lado a lado e confirmar que (i) nenhuma das duas diz "Controlar o PC", (ii) o
   botão "Suspender mouse e teclado" **não** está cinza, e (iii) a frase sobre a
   emulação é verdadeira.

### NÃO rodar nada do projeto na fase de levantamento

Este defeito foi levantado inteiro por leitura de código, dos arquivos de
configuração dela e do journal. Instalar, reiniciar o daemon ou rodar a suíte
mexeria no estado vivo que **produziu** a evidência: a sessão do daemon PID 2430
está de pé desde 16:50 e é ela que contém os 97 minutos medidos.

## O que fica sem medição

- **Não vi a tela dela.** Toda afirmação sobre o que a janela mostra vem de
  leitura do `gui/main.glade` e do Python que o preenche, não de captura. As três
  provas de tela acima existem por isso.
- **Não abri o jogo.** A correlação 9/9 é do journal dela jogando, não de
  experimento controlado meu. Nunca vi o Alt+Tab acontecer.
- **Não sei se ela usava o Alt+Tab do R1 de propósito no desktop.** O journal
  mostra 9 pressionamentos em 7 dias e **todos** dentro de janela de jogo — o que
  sugere que não, mas ausência de evidência no desktop é ausência de evidência.
  É a pergunta que E5 precisa fazer a ela antes de mudar o default.
- **Não medi o efeito real do Alt+Tab no compositor.** Que o `KEY_LEFTALT` +
  `KEY_TAB` chega ao uinput está medido; que o cosmic-comp trocou de janela por
  causa dele é **inferência** a partir do relato dela ("muda de app"). Plausível,
  não medido.
- **Não sei quanto tempo a sticky de `display_authority` custa na prática nesta
  máquina.** O código diz ~30 s (`daemon/lifecycle.py:1607`); não cronometrei.
  É a segunda prova de tela.
- **Nenhum teste foi escrito.** Todos os "como PROVAR" desta sprint são projeto
  de teste, não teste existente. Nenhum deles foi executado — a fase foi somente
  leitura.
- **Não sei o que acontece com o co-op.** `suspend_vpads_for_steam_input`
  desmonta os jogadores secundários junto (`daemon/subsystems/gamepad.py:474-476`,
  `coop.disable()`), e todos os episódios medidos hoje têm
  `jogadores_coop=0`. O comportamento de E1 com quatro controles na mesa não foi
  raciocinado.

---

## NOTA DATADA — 09/08/2026: três entregas saíram, e o "nenhuma linha escrita" caducou

**Nada acima foi apagado.** A medição ponta a ponta, o Alt segurado por 33
segundos e as seis entregas continuam inteiros — inclusive as duas que **ainda
devem**.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **E1** — com o vpad suspenso pelo Steam Input, o desktop não entra | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/daemon/lifecycle.py:169` — *"o campo deixou de ser config MORTA"* |
| **E1(b)** — o interruptor que o teclado nunca teve, na tela | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/gui/main.glade:3444` |
| **E2** — generalizar para QUALQUER jogo, não só os da allowlist | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/daemon/lifecycle.py:423` — o motivo pelo qual a emulação de desktop fica calada |
| a escolha dela sobrevive ao fechar a janela | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/utils/session.py:375` (`save_keyboard_emulation`) |

**Commit:** `2bbfa22`, 30/07/2026.

### O que continua ABERTO nesta sprint — e não foi remarcado

- **E3** — a janela para de mentir durante a partida.
- **E5** — revisitar o DEFAULT, que é a escolha de projeto por trás do sintoma.

A **E0** é decisão de vocabulário dela e não é entrega de código. A **E4** é a
mesma coisa que a E1(b) e sai junto com ela.

### Por que o rótulo não é ENTREGUE e sim ENTREGUE EM CÓDIGO

Porque a própria sprint escreveu, na seção *"Exige o olho dela na tela — três
provas, e nenhuma é opcional"*, que **nenhuma delas é opcional** — e nenhuma foi
feita. O sintoma que abriu esta sprint só se declara curado com ela jogando.
