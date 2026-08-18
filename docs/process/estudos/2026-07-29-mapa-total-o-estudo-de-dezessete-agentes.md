# O mapa total — o estudo de dezessete agentes de 29/07/2026

- **Levantado em:** 29/07/2026, sobre `restauro/inicio-da-sessao`, `v0.3.0`,
  HEAD `e8e18b9`. Árvore limpa, sem stash, um worktree
- **Por quê:** o pedido foi *"estude o projeto por completo, não execute nada
  apenas entenda ele"*, e depois *"estuda as próximas sprints sem ser as clean
  room"*. O estudo de quatorze agentes de 28/07 mapeou a árvore; este mapeou a
  árvore **contra a máquina dela**, lendo o journal do daemon vivo
- **Método:** 17 agentes somente-leitura em duas ondas (7 + 7), mais um crítico
  de lacunas e dois agentes de preenchimento sobre o que o crítico achou. Cerca
  de 4,5 milhões de tokens, 1.498 leituras de arquivo, **zero execução** — nem
  `pytest`, nem `install.sh`, nem `doctor.sh`, nem os portões. O que se mediu
  além do código veio de `journalctl --user`, de `pactl`, de `/proc` e dos
  arquivos de configuração dela
- **Como ler:** a seção 2 é a mais importante e contradiz a hipótese com que a
  sessão começou. As seções 3 a 5 são os defeitos e o achado de lambuja. A
  seção 6 é consulta por área. A seção 9 diz o que já tem dono
- **Portões:** `validar-glifos.py` e `validar-acentuacao.py --check-file`
  rodados sobre este arquivo com caminho explícito, porque ele é novo e o
  `--all` da acentuação só enxerga o que já está no git

---

## 1. O que este estudo é, em uma frase

Treze mapas de área, um crítico que os cruzou e apontou dois buracos, e dois
mapas que fecharam os buracos. O resultado não é "o projeto está quebrado": é
que **os três defeitos que ela relatou hoje têm três causas diferentes, todas
medidas, e nenhuma delas é a hipótese com que a sessão começou.**

---

## 2. O que este estudo CORRIGIU do que se supunha

A hipótese de partida da sessão — herdada do mapa de 28/07 e da memória — era
**"o detector de janela é cego em COSMIC, então nada dispara sozinho"**. O
journal dela refutou metade disso, e outras cinco suposições caíram junto.

| Suposição | O que a medição diz |
|---|---|
| "o detector é cego em COSMIC" | **METADE FALSA.** O backend é sempre o `XlibBackend` (`integrations/window_detect.py:144` testa `DISPLAY` primeiro, sem cascata) e ele **enxerga jogo**: o journal de hoje tem `wm_class=steam_app_3357650`, `steam_app_1553260` e `steam_app_2111190` em decisões reais. A cegueira é **só no desktop Wayland nativo**: 30 `x11_focus_gate_no_x_focus focus=0` e 17 `autoswitch_window_info_unavailable wm_class=unknown`. Jogo Proton é XWayland e aparece |
| "nada dispara sozinho — o código do modo jogo automático não roda" | **FALSO.** Rodou **seis vezes hoje**: `profile_mode_aplicado origin=game_signal` às 01:47:39, 01:52:18, 01:52:47, 16:55:25, 16:59:27 e 17:49:55. O que é verdade é que todas as seis saíram com `ligou_gamepad=False` — o caminho existe, dispara e não produz efeito |
| "o cadeado `autoswitch_locked` já foi curado; ele não explica o defeito 1" | **FALSO**, e este foi o único ponto em que cinco mapas contradisseram um sexto. O crítico foi ao código: `profiles/autoswitch.py:253-273` faz o tique dar `return` sem tocar perfil, zerando `_last_candidate`. A cura de MODO-01/B2 apenas moveu `_sincronizar_modo_jogo_padrao` para **antes** do gate (`profiles/autoswitch.py:237-238) — ela liberou o **modo**, nunca a troca de **perfil**. Journal: 14 a 15 `autoswitch_congelado_pelo_cadeado` e **zero** `profile_autoswitch` |
| "os perfis dela são cinco, todos catch-all" | **FALSO como contagem, VERDADEIRO como consequência.** São **15** JSONs: 5 `any` (fallback 0, vitoria 0, meu_perfil 1, Pragmata 5, Pragmata2 5) e 10 `criteria` (bow 10, navegacao 50, corrida 55, esportes 55, fps 60, point_and_click 60, `acao` 65, aventura 70, coop_local 75, sackboy_nativo 80). Em janela `steam_app_*` os dez `criteria` não casam, porque `MatchCriteria.matches` é AND entre os campos preenchidos (`profiles/schema.py:92-94`) e eles pedem `process_name` de `.exe` do Windows — sob Proton o `exe_basename` vem do loader do Wine. Sobram exatamente os cinco catch-all, que o veto R-21 recusa |
| "o empate de perfis é resolvido pelo alfabeto, e `fallback` vence `vitoria`" | **SUPERADO.** Existe um terceiro termo desde 28/07: o **incumbente** lido do `StateStore` (`profiles/manager.py:658-707`). Journal de hoje: 25 a 26 linhas de `profile_select_empate_resolvido empatados=['Pragmata','Pragmata2'] incumbente=Pragmata2 vencedor=Pragmata2`. O alfabeto só decide quando o incumbente não está entre os empatados (`profiles/manager.py:690` + `profiles/loader.py:568`) |
| "não há botão na janela para a allowlist do Steam Input" | **FALSO, e ao contrário.** O botão de **adicionar** existe: `gui/main.glade:2067` (`btn_steam_game_broken`, "Este jogo não funciona") ligado em código por `app/actions/daemon_actions.py:396-418` e escrevendo em `app/actions/daemon_actions.py:970`. O que não existe é o de **remover** — e o CLI **tem** (`cli/cmd_steam.py:196-215`). A tela nega um desfazer que existe |
| "a allowlist do Steam Input pode ter sido criada por clique acidental" | **REFUTADO, veredito seguro.** `~/.config/hefesto-dualsense4unix/steam_input_apps.txt` (721 bytes, criado 22/07 14:33) tem notas autorais dela por entrada, o cabeçalho antigo `(STEAM-INPUT-ALLOWLIST-01, 22/07)` e **não** contém a string que o botão escreve (`marcado pela GUI: 'este jogo não funciona'`, `app/actions/daemon_actions.py:1004`). A função que escreve nasceu em 25/07; o arquivo, em 22/07. **Foi decisão dela** |
| "a falta de `jeepney` no `.deb` explica o autoswitch dela" | **NÃO SE APLICA.** `integrations/window_detect.py:141-146` devolve `XlibBackend()` no primeiro teste e a sessão dela tem `DISPLAY=:1` — o backend do portal, que é quem usaria `jeepney`, nunca é instanciado. Ela instalou pelo caminho native. O achado do `.deb` continua real como dívida de empacotamento, não como causa |
| "o `sensor_hub.py` é novo, posterior ao mapa de 27/07" | **FALSO.** `git log --follow` tem UM commit: `8f90e96`, 24/07 22:37 — **três dias antes** dos mapas. Em 58 commits, incluindo a leva de 14 agentes de 28/07, o arquivo nunca foi tocado nem descrito |

---

## 3. Os três defeitos de 29/07

### 3.1 "O autoswitch das configurações não funciona"

**Duas causas somadas, as duas medidas, e a de cima é suficiente sozinha.**

Cadeia completa, elo por elo: `integrations/window_backends/xlib.py:238-339` lê
a janela com dois gates (foco X real **e** acordo com `_NET_ACTIVE_WINDOW`) ->
`integrations/window_detect.py:227-240` achata `None` em `wm_class='unknown'` ->
`daemon/subsystems/autoswitch.py:137-149` grava backend/classe/motivo no store ->
`profiles/autoswitch.py:210` pula o tique inteiro se a leitura for vazia ->
`profiles/manager.py:613` recarrega os 15 JSONs do disco ->
`profiles/manager.py:620-628` **veto R-21** -> `profiles/manager.py:658-707`
desempate -> `profiles/autoswitch.py:237` modo jogo padrão (antes do cadeado) ->
`profiles/autoswitch.py:252-275` **cadeado** -> debounce -> três supressores ->
`ProfileManager.activate`.

| Camada | Medição |
|---|---|
| **Causa 1 — o cadeado dela** | `~/.config/hefesto-dualsense4unix/autoswitch_locked.flag` contém `1`, mtime **28/07 18:18**. Lido no boot (`daemon/lifecycle.py:555-556`) e a cada tique (`profiles/autoswitch.py:188-189`). Journal de hoje: 14 a 15 `autoswitch_congelado_pelo_cadeado` (ex.: `18:11:49 candidate=Navegacao current= wm_class=steam`) e **zero** `profile_autoswitch`. O único `profile_activated` do dia é o restore de boot: `16:50:43 name=Pragmata2 origin=system priority=5` |
| **Causa 2 — o veto R-21** | Mesmo destravado, em janela de jogo a resposta é `None`: 12 linhas `profile_select_catch_all_sem_autoridade_em_jogo candidatos=['Pragmata','Pragmata2','fallback','meu_perfil','vitoria']` para três appids (`profiles/manager.py:620-628`) |
| **O cadeado cede — mas não para ela** | `perfil_e_regra_de_jogo` exige `window_class` com a `steam_app_<id>` em foco; `perfil_declara_modo_de_jogo` (`profiles/schema.py:666-702`) exige **não ser catch-all** e ter `mode.kind` em `{gamepad, native}`. O `vitoria.json` dela tem `mode.kind=gamepad` e é `match: any` — declara servir para jogar e cai no vão exatamente por ser catch-all |
| **O remendo de 26/07 foi desfeito** | `PERFIL-NASCE-CERTO-01` registra `pragmata.json` corrigido à mão para `{"type":"criteria","window_class":["steam_app_3357650"]}` prioridade 110. O disco de hoje diz `match: {"type":"any"}`, `priority: 5`, mtime 27/07 23:00. O defeito de "salvar rebaixa a regra" foi curado no código em 28/07 (`8d7fd45`) — **a cura não reescreve arquivo já rebaixado** |
| **O log delata duas noções de "perfil corrente"** | Todas as linhas do cadeado saem com `current=` vazio, porque `AutoSwitcher._current_profile` só é escrito no commit de `_activate` (`profiles/autoswitch.py:551`) e ele nunca rodou. Ao mesmo tempo `store.active_profile` = `Pragmata2`. É disso que dependem o debounce assimétrico de saída (`profiles/autoswitch.py:392-396`) e o desempate por incumbente |

**Supressor invisível que ninguém checou:** `store.manual_trigger_active` **não
tem TTL**. Aplicar uma cor na aba Lightbar (`daemon/ipc_handlers.py:590`, `:620`)
ou clicar Aplicar no rodapé (`daemon/ipc_draft_applier.py:57-69`) arma a
categoria `led`, e `profiles/autoswitch.py:505-518` passa a suprimir toda
ativação. Existe clear por categoria para `trigger` (`:539`) e `rumble`
(`:2366`), **não para `led`**. E o campo não aparece em `daemon.status` nem em
`daemon.state_full` — só em `StoreSnapshot` (`daemon/state_store.py:531`). A tela
não tem como dizer que a troca automática está congelada por causa de uma cor.

### 3.2 "O modo jogo não alterna ao abrir um jogo da Steam"

**O código existe, disparou seis vezes hoje, e não fez nada.** Três razões
empilhadas.

**Razão A — "modo jogo" nomeia duas coisas, e o automatismo mexe na outra.**

| Nome | O que é | Quem liga |
|---|---|---|
| `_emulation_suppressed` (`daemon/lifecycle.py:359`) | suspende o dispatch de mouse/teclado de desktop | `apply_profile_suppression` (`daemon/lifecycle.py:1462-1465`, só com `desired=True`), o combo PS+Options, o IPC `daemon.emulation.suppress`. **Nenhum caminho automático de sinal de jogo** |
| `aplicar_modo_jogo_padrao` (`daemon/lifecycle.py:1783`) | liga o **gamepad virtual** | o autoswitch, a cada tique com `MOTIVO_JOGO_SEM_PERFIL_PROPRIO`. Não toca `_emulation_suppressed` em nenhuma linha |

A dona **esclareceu hoje** que quando ela diz "modo jogo" quer dizer **suspender
mouse e teclado**, ou seja `_emulation_suppressed`. Para isso, o caminho
automático **não existe** sem um perfil por appid com
`suppress_desktop_emulation: true`. No disco dela só `coop_local.json` e
`sackboy_nativo.json` (appid 1599660) têm o campo `true`. Hoje ele mudou duas
vezes (`emulation_suppressed_changed suppressed=True` às 01:52:38 e 16:58:56) e
em nenhuma houve `hotkey_fired`: **ela ligou pela janela**, 2m46s depois de
tentar segurar o PS.

**Razão B — o automatismo que existe é um no-op na máquina dela.** As seis
ocorrências de `profile_mode_aplicado origin=game_signal` trazem
`ligou_gamepad=False`. Motivo em `daemon/lifecycle.py:1753-1769`: com
`gamepad_emulation.flag = dualsense` e o vpad de pé, `flavor == flavor_atual` e
`gamepad_on` é True, então `set_gamepad_emulation` nem é chamado; o co-op também
já está em 1. E `apply_profile_mode`, no ramo `kind=='gamepad'`, **ignora o
retorno** de `set_gamepad_emulation` e devolve APLICADO incondicionalmente
(`daemon/lifecycle.py:1761`) — combinado com a idempotência por episódio de
`daemon/lifecycle.py:1832-1833`, uma falha real de start é registrada como
sucesso e **nunca mais tentada naquele episódio**.

**Razão C — nos dois jogos dela o Hefesto sai de cena de propósito.**
`steam_input_apps.txt` lista 2111190 (Mullet Mad Jack) e 3357650 (Pragmata), e o
`localconfig.vdf` confirma `UseSteamControllerConfig="2"` nesses dois blocos.
Por desenho: `daemon/launch_env.py:933-945` sobrescreve os `.env` desses appids
com a variante sem dedup (conferido: os dois arquivos só têm `__GL_SHADER_*` e
`USE_BUTTON_LABELS`, com o rótulo "allowlist Steam Input (físico é o único
dispositivo)"); `arm_launch_profile` pula a seção `mode`
(`daemon/launch_env.py:551-563`); e `sync_steam_input_exception`
(`daemon/subsystems/gamepad.py:231-307`) suspende os vpads. Journal:
`16:59:26 steam_input_excecao_ativada appid=3357650` + `gamepad_controller_grab
grab=False` + `gamepad_emulation_stopped` + `steam_input_vpad_suspenso`, e um
segundo depois `16:59:27 gamepad_start_recusado_steam_input flavor=dualsense
origem=profile` (3 vezes hoje).

**Corrida de ~2 s que garante que o primeiro pedido sempre falha:**
`16:59:26 modo_jogo_padrao_adiado estado=ignorado_sem_jogo
motivo=sem_autoridade_de_jogo wm_class=steam_app_3357650`, e **só depois**
`16:59:26 game_signal_transition de=daemon para=game`. O gate de
`daemon/lifecycle.py:1828` exige `display_authority == 'game'`, e a autoridade é
recalculada no tique lento de 2 s (`daemon/lifecycle.py:3080-3082`), não no de
0,5 s do autoswitch.

**Flapping do alt-tab, ainda de pé:** seis `modo_jogo_padrao_solto
motivo=janela_fora_do_jogo wm_class=steam` hoje.
`assets/profiles_default/navegacao.json` lista `steam`/`Steam` em
`window_class`, então focar o **cliente** da Steam produz `MOTIVO_SELECIONADO` e
`profiles/autoswitch.py:371-377` solta o modo jogo. É a entrega 4 da
PERFIL-JOGO-01, não feita.

### 3.3 "Segurar o PS não vira modo jogo"

**Fechado por medição direta. Não é regressão: é default deliberado, e a janela
promete o gesto que o código desliga.**

A prova, em duas linhas do journal de hoje:

```
16:50:42  hotkey_manager_started  next_prev_combos='ps+dpad_up / ps+dpad_down'
                                  ps_button_action=steam  ps_long_press_ms=0
16:56:10  ps_solo_released  held_ms=5658.9
16:56:10  ps_button_action_steam  outcome=refocus_fallback_spawn
```

**Ela segurou o PS por 5,66 segundos e o projeto abriu a Steam.** É o único
`ps_solo_released` do dia, e `hotkey_fired` (que cobriria PS+Options e PS+dpad)
aparece **zero** vezes.

O gesto está desligado em três camadas: `DEFAULT_PS_LONG_PRESS_MS = 0`
(`integrations/hotkey_daemon.py:48`), `ps_long_press_ms: int = 0`
(`daemon/lifecycle.py:158`) e `os.getenv('HEFESTO_DUALSENSE4UNIX_PS_LONG_PRESS_MS', '0')`
(`daemon/main.py:97-99`). O ramo do hold exige `> 0`
(`integrations/hotkey_daemon.py:174`). O motivo está escrito: o toque de abrir a
Steam que passava de ~1 s alternava o modo por acidente
(FEAT-EMULATION-GAMEMODE-COMBO-01), e o gesto virou o combo PS+Options
(`integrations/hotkey_daemon.py:52`). Confirmado que a env **não** está no
ambiente do processo (`/proc/2430/environ`) nem no unit instalado.

**A janela mente.** `gui/main.glade:2270` diz, em negrito: *"Modo jogo: segure o
botão PS para suspender a emulação de mouse/teclado"*. O rótulo **não tem
`id`**, mora dentro do `emulation_combo_grid` e nenhum código Python o atualiza
— é uma promessa congelada no arquivo. O combo real aparece uma única vez, num
tooltip (`gui/main.glade:2506`). A documentação está do lado do código
(`docs/usage/hotkeys.md:102-107`, `docs/usage/cosmic.md:23`): **quem lê o código
acerta, quem lê a tela erra.**

**Três agravantes, todos medidos ou lidos:**

1. Mesmo o combo PS+Options morre em três estados. `_hotkey_manager.observe(...)`
   está **atrás** do gate `input_ready` (`daemon/lifecycle.py:3217`, `observe` em
   `:3282`): com o daemon pausado, em Modo Nativo, ou no grace de 0,3 s
   pós-conexão, nenhum combo é observado. **Em Modo Nativo não existe gesto de
   controle nenhum para sair do Modo Nativo** — só GUI/IPC.
2. **Mesmo religando o hold, o efeito seria quase nulo.**
   `build_ps_long_press_callback` (`daemon/subsystems/hotkey.py:77-79`) só chama
   `daemon.set_emulation_suppressed()`, e `daemon/lifecycle.py:3266`
   (`if not gamepad_dispatched:`) já exclui mouse e teclado enquanto o vpad está
   de pé. Com `mouse_emulation.flag = {"enabled": false}` no disco dela, não
   mudaria nada perceptível.
3. **Suspeita não provada:** durante os treze minutos de Pragmata (16:59:26 ->
   17:12:29) o journal não tem **um** evento de botão. Na borda de entrada da
   exceção o Hefesto solta o grab (`16:59:26 gamepad_controller_grab grab=False`,
   `daemon/subsystems/gamepad.py:271`) para a Steam poder falar com o físico — e
   o Steam Input, ao assumir, faz `EVIOCGRAB` exclusivo. Se for isso, **nenhum
   atalho funciona dentro desses dois jogos**. Ninguém inspecionou o dono do
   grab.

**O único lugar onde `ps_long_press_ms` seria configurável é o arquivo que o
daemon nunca lê.** `app/actions/emulation_actions.py:283-292` escreve
`ps_long_press_ms = 0  # 0 = desliga o modo jogo` num `daemon.toml` que o próprio
código declara morto (BUG-DAEMON-TOML-DEAD-01). O botão foi removido do glade;
o handler `on_emulation_open_toml` continua registrado em `app/app.py:320`.

---

## 4. O vpad recriado no meio da partida — o achado que ninguém procurava

Este é o achado mais grave da rodada e apareceu de lambuja. **A exceção de Steam
Input não tem histerese nenhuma e é dirigida pela leitura CRUA da janela.**

Janela do journal, com Pragmata aberto:

```
01:52:17  steam_input_excecao_encerrada
01:52:17  uhid_device_created
01:52:17  gamepad_controller_grab  grab=True
01:52:19  steam_input_excecao_ativada
01:52:19  gamepad_controller_grab  grab=False
01:52:19  uhid_game_session_end
01:52:19  gamepad_emulation_stopped
01:52:20  autoswitch_window_info_unavailable  wm_class=unknown     <- UM tique cego
01:52:21  steam_input_excecao_encerrada
01:52:21  uhid_device_created
01:52:48  steam_input_excecao_ativada
01:52:48  gamepad_emulation_stopped
```

**Três destruições e recriações do gamepad virtual em 31 segundos**, a cada
alt-tab jogo <-> cliente Steam. E **um único tique cego** às 01:52:20 bastou
para encerrar a exceção e recriar o device com o jogo aberto:
`steam_input_exception_appid` (`daemon/launch_env.py:446-450`) lê
`window_detect_current_class`, o valor cru, sem histerese.

A decisão de usar o cru está declarada em `daemon/launch_env.py:433-438` ("*enquanto
esta função disser um appid, a usuária está SEM vpad*") e é defensável para
apagar o sinal rápido. **O preço não está registrado em sprint alguma**, e é o
melhor candidato mecânico para "na hora do jogo tá um caos": recriar o vpad
invalida os handles e a Steam nunca reabre o hidraw do vpad do P1.

Cada `steam_input_vpad_suspenso` também devolve a saída retida do jogo:
`16:59:26 game_session_devolvida lightbar=True player_leds=True` — a cor e o
número do controle são repintados pelo jogo no instante em que ele abre.

Compare com o irmão: o `game_signal` **tem** 30 s de histerese na queda
(`daemon/subsystems/game_signal.py`), e `reverter_modo_jogo_padrao`
(`daemon/lifecycle.py:1884-1891`) é chamado por **evidência positiva de outra
janela**, nunca pela queda do sinal, porque desligar o vpad no meio da partida
"seria o pior desfecho possível". A mesma casa tomou as duas decisões opostas
para o mesmo risco, e só uma delas está documentada.

---

## 5. A árvore que roda não tem 17 commits

Medido nesta máquina, agora:

| Ref | Commit |
|---|---|
| `HEAD` (`restauro/inicio-da-sessao`) | `e8e18b9` |
| `main` (ref **local**) | `2d8527a` |
| `git rev-list --left-right --count main...HEAD` | **17 e 16** |
| `git config branch.main.remote` | **`upstream`** |

No remoto, `origin/main` e `origin/restauro/inicio-da-sessao` são o mesmo
`e8e18b9` — a main foi sobrescrita por decisão dela em 29/07 às 03h, registrada
na anotação da tag `arquivo/main-antes-da-v030`. **A ref local ficou para trás e
rastreia o upstream.** Quem fizer `git checkout main` nesta máquina cai na
árvore de 26/07, não no que roda. Não está escrito em documento nenhum se isso
foi decisão ou esquecimento.

**A consequência viva, medida em três pontos.** O commit `84d9f4e` — *"fix(doctor):
o `--fix-mic` aplicava a cura que a medição refutou — e silenciava o
microfone"* — é ancestral de `main` e **não** é ancestral de `HEAD`. Ou seja: a
cura está fora da árvore que roda.

1. `install.sh:2192` chama `bash "${ROOT_DIR}/scripts/doctor.sh" --fix-mic
   --quiet` a cada instalação, com a versão **sem** a cura — reaplicando o que a
   medição de 26/07 refutou (MIC-USB-01: o perfil analógico está
   `available: no` e nasce sem porta de captura; quem grava é o `iec958-stereo`).
2. `scripts/doctor.sh:438` dá **pass** quando o nome da fonte contém "monitor":
   `if [[ ! "${cur}" =~ [Dd]ual[Ss]ense ]] || [[ "${cur}" == *[Mm]onitor* ]]` ->
   `pass "microfone ativo não é o mic do DualSense"`. O comentário acima diz que
   o `.monitor` é "inofensivo".
3. `pactl get-default-source` devolve, agora:
   `alsa_output.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.analog-surround-40.monitor`

**A fonte de captura padrão da máquina dela é o monitor do alto-falante do
próprio controle.** O portão que deveria pegar isso passa verde por construção,
porque a linha que trata "monitor" como inofensivo é exatamente a que `84d9f4e`
corrigiu — do outro lado da divergência.

Outros fatos do estado do repositório que valem registro:

- `docs/tags-arquivo-pre-1.0.txt` se declara "o único mapa para reverter a
  renumeração" e ensina a recriar tags apagadas — **nenhuma tag foi apagada**
  (`git ls-remote --tags origin` devolve 44). E os SHAs do arquivo são objetos de
  **tag anotada**, não commits: comparar com `git rev-list -n1 <tag>` leva à
  conclusão errada de que a história foi reescrita.
- **Existem dois 0.1.0 e só o errado tem tag.** `v0.1.0` aponta para `86597a3`
  (20/04, release interna); o alfa de 24/07 que o `CHANGELOG.md:352` chama de
  "primeiro lançamento público" está em `43c3078`, cujo assunto diz "sem
  publicar" e que não tem tag.
- **O caminho de instalação documentado instala código pré-0.2.0.**
  `docs/usage/instalacao.md:29-36`, `docs/usage/quickstart.md:36` e
  `docs/usage/flatpak.md:38-39` mandam clonar `-b sprint/harmonia-uhid`; o badge
  de CI do `README.md:14` mede a mesma branch. Não existe documento que diga a
  alguém novo como obter a v0.3.0.
- O selo `Status:` das sprints é medidamente inútil: 50 arquivos `.md` em
  `docs/process/sprints/`, 43 com cabeçalho `Status:`, **37 dizendo ABERTA**,
  várias provadamente entregues.

---

## 6. Um mapa por área — os fatos que mudam decisão

Cada seção tem os fatos mais **não-obvios** daquela área. Não é resumo: é
seleção.

### 6.1 O daemon (`daemon/`, 18.633 linhas)

- **Não há um laço: há quatro.** `Daemon._poll_loop`
  (`daemon/lifecycle.py:3023`) a 60 Hz, `reconnect_loop`
  (`daemon/connection.py:289`), `AutoSwitcher.run`
  (`profiles/autoswitch.py:143`) a 2 Hz e `mic_button_loop`
  (`daemon/subsystems/hotkey.py:224`). Mais um quinto que não é task asyncio (ver
  6.8).
- **O padrão de subsistemas do ADR-015 não é usado em produção.**
  `SUBSYSTEM_REGISTRY` existe (`daemon/subsystems/__init__.py:41`) e **não é
  iterado**: quem sobe é `Daemon.run()` linha a linha
  (`daemon/lifecycle.py:610-634`). **Mina armada para quem "consertar":**
  `DaemonContext` não tem campo `daemon` (`daemon/context.py:19-34`), e
  `IpcSubsystem.start` (`daemon/subsystems/ipc.py:33`) e
  `AutoswitchSubsystem.start` (`daemon/subsystems/autoswitch.py:169`) fazem
  `getattr(ctx, "daemon", None)`. Iterar o registry faria o IpcServer nascer com
  `daemon=None` e o AutoSwitcher **sem appliers e sem
  `modo_jogo_padrao_applier`** — o modo jogo automático desapareceria em
  silêncio. Pior: `daemon/subsystems/gamepad.py:98` usa
  `getattr(ctx, "daemon", ctx)`, um fallback **diferente**.
- **Três fontes de verdade divergentes para a ordem de start:** o docstring de
  `daemon/subsystems/__init__.py:3-4` omite o `GamepadSubsystem` que está na
  lista de baixo (`:47`); `HotkeySubsystem` existe com `name` e não está no
  registry (`daemon/subsystems/hotkey.py:268`); `keyboard.py` não tem classe de
  subsistema nenhuma.
- **O timeout do tique de LED dos externos VAZA O WORKER DE PROPÓSITO**
  (`daemon/lifecycle.py:69-99`): um wedge de GIL do CPython sob debandada de
  `/dev/input` pode nunca devolver o controle a Python, a thread não é
  recuperável, e o trade-off aceito é vazar worker do pool `hefesto-ext`. A
  primeira versão do fix rodava no pool compartilhado e reproduzia o hang.
- **O UDP 6969 é o único caminho que escreve no controle direto do event loop**
  (`daemon/udp_server.py:365` -> `:518`), sem executor, sem autenticação:
  qualquer processo local que fale 6969 comanda o controle. `docs/protocol/udp-schema.md`
  fala de rate limit e não disso.
- **O IPC registra 33 métodos e o protocolo documenta ~18.** Os 15 ausentes
  incluem `autoswitch.lock`, `daemon.pause/resume`, `gamepad.emulation.set`,
  `profile.apply_draft` e os cinco de rumble. **O caso grave é
  `autoswitch.lock`**: é o comando que liga o cadeado que bloqueia a troca de
  perfil dela hoje, e não existe em documento de protocolo nenhum.
- **`_modo_jogo_padrao` não é exposto por IPC nenhum.** `daemon.status` e
  `daemon.state_full` publicam `autoswitch_locked`, `native_mode`,
  `emulation_suppressed`, `paused`, `display_authority` e sete campos
  `window_detect_*` (`daemon/ipc_handlers.py:1149-1214`) — nada sobre o modo jogo
  padrão. A única observabilidade é o journal.
- **Cinco travas temporais distintas podem barrar a mesma ativação**, e confundir
  duas é fácil: `autoswitch_locked` (persistente), `manual_override_categories`
  (por categoria, **sem prazo**), `manual_profile_lock_until` (30 s),
  `_suppress_manual_ts` (30 s) e `_emu_manual_ts` (30 s). Só a seção `mode` tem
  retry quando adiada (`ModoAdiado`, `daemon/lifecycle.py:210-246`).
- **Desconexão de cliente IPC foi rebaixada a debug por uma espiral medida**
  (`daemon/ipc_server.py:260-274`): GUI e applet usam timeout de 0,25 s, o
  `drain()` levantava ConnectionError, o renderizador imprimia traceback **com
  locals** (o grafo do daemon inteiro), e a ~5 conexões/s isso fritava uma CPU e
  despejava ~950 linhas/s no journal. **Zero linhas no journal hoje não é prova
  de zero timeouts.**
- **`window_detect_healthy` é trinco de mão única por CONTRATO**
  (`daemon/state_store.py:427-438`): sobe na primeira leitura útil e não desce,
  porque a transição `daemon -> unknown` dispararia
  `replay_retained_game_outputs()` e **repintaria a lightbar** dela no desktop.
  Quem responde "enxerga AGORA?" é `window_detect_seeing()`
  (`daemon/state_store.py:459`, decai em 300 s) e **ninguém pergunta**:
  `daemon/lifecycle.py:2952` continua lendo o trinco. É a "leva seguinte de uma
  linha" da JANELA-CEGA-01, não entrou.

### 6.2 O núcleo HID (`core/`, 7.871 linhas — intocado desde 25/07)

`git log -- src/hefesto_dualsense4unix/core/` para em `8f83897` (25/07). A
v0.3.0 não tocou uma linha. O mapa de 27/07 continua **corrente** para esta área.

- **Um relatório HID nunca vira estado por este caminho.** O input do jogador vem
  do **evdev do kernel**; `read_state` só empresta do HID a bateria, o transporte
  e **um** botão (o do microfone, que não tem keycode evdev). O gyro/accel vem de
  um **terceiro** caminho: um segundo fd O_RDONLY no mesmo hidraw que copia 25
  bytes verbatim. **Três leitores do mesmo controle, com donos diferentes.**
- **BUG LATENTE MEDIDO:** `_pack_strengths_bits` empacota cada posição em **3
  bits** (`bits |= (s & 0x7) << (i*3)`, `core/trigger_effects.py:347`) mas a
  validação aceita 0..8 (`:244`). **Força 8 — o máximo documentado — vira 0**, ou
  seja "sem força", em silêncio. E o teste que cobre isso
  (`tests/unit/test_trigger_effects.py:164-176`) reproduz o mesmo `& 0x7` no
  cálculo esperado: é tautológico e nunca morderia.
- **`_recompute_primary` retorna cedo quando o primário não mudou**
  (`core/backend_pydualsense.py:1586-1587`) — e é o **único** lugar do projeto
  que chama `_evdev.start()`. Se, no instante da eleição, o node evdev ainda não
  existir (corrida real na conexão BT), o daemon loga uma vez
  `controller_primary_bound with_evdev=False` e **a thread de evdev nunca mais é
  tentada**. O watchdog não salva: `heal_evdev_if_stale` sai False quando
  `is_available()` é False. **Explicaria os três sintomas de botão de uma vez** —
  não confirmado ao vivo.
- **A supressão de LED é forçada True por Bluetooth**, independente de haver nó
  sysfs (`core/backend_pydualsense.py:1717-1719`). Controle em BT sem a regra
  udev 77 aplicada **não tem como acender cor nem padrão de jogador**, e não há
  log de erro: parece "a cor não cola".
- **A malformação do 0x31 da pydualsense é de LAYOUT, não de CRC.**
  `outReport[1] = 0x02` onde devia ir `seq<<4` e `outReport[2] = 0xFF` onde o
  firmware exige o tag `0x10`, deslocando o common inteiro um byte. O CRC dela
  está certo em forma. O firmware descarta pelo envelope.
- **O keepalive de 0,5 s teve que virar NEUTRO campo a campo**
  (`core/backend_pydualsense.py:632-648`), e o mais desconcertante está no
  comentário `:601-603`: essa regressão só apareceu **depois** da cura do
  envelope — antes o keepalive era malformado e o firmware o descartava.
- **`mic.set` tem TRÊS estados** e confundir dois foi o defeito real: `True` muta,
  `False` é ORDEM de desmutar (e mata o botão físico), `None` devolve a posse ao
  kernel (`core/backend_pydualsense.py:515-530`).
- **O merge por camadas é a resposta a "a config que eu deixo nunca é
  respeitada" — e o preço é a face oposta.** `reset_profile_overrides` só ocupa
  campo **vago** (`core/backend_pydualsense.py:2556-2563`) e
  `clear_user_output_overrides` só é chamado com `origin == 'manual'`
  (`profiles/manager.py:306-309`); o autoswitch usa `origin='auto'`. **Depois que
  ela ajusta cor ou gatilho na mão, nenhuma troca automática mexe naquele
  campo** — do lado dela, "o autoswitch não funciona".
- **O timeout de `init()` pode deixar um ESCRITOR ZUMBI**
  (`core/backend_pydualsense.py:1320-1339`): a thread é abandonada aos 5 s, mas o
  `init()` do upstream sobe a thread de report no fim dele. O comentário da linha
  380 nomeia o caso e a defesa é `_suppress_leds` nascer True.
- **Ninguém fecha o fd de outra thread**, em nenhum leitor: `stop()` escreve 1
  byte num self-pipe (`core/physical_report_reader.py:131-144`). Fechar de
  fora libera o **número** do fd com a thread ainda no select, e qualquer `open`
  concorrente o recicla — input congelado e gyro-lixo no vpad.
- **`(0,0,0)` na classe LED do kernel NUNCA significa "apagada"**: o probe
  registra o LED zerado enquanto acende a lightbar por um caminho interno que não
  atualiza a classe (`core/sysfs_leds.py:92-105`). Daí `KERNEL_DEFAULT_BLUE`
  existir. E `record_sysfs_write` **não** é chamado pelos caminhos de escrita de
  cor dela (`core/backend_pydualsense.py:1766-1781`): a defesa `verify=True` cobre
  menos do que parece.

### 6.3 A janela (GUI GTK3, `app/` + `gui/`)

- **Zero `GtkComboBox` no projeto, por bug de compositor**: no cosmic-comp
  qualquer popup fecha no clique (cosmic-epoch#2497), então tudo virou
  `SegmentedSelector`. Por isso a contagem de widgets acionáveis é alta e **nenhum
  aviso é popover** — todos são `GtkLabel` inline com `no_show_all`.
- **No GTK3 não existe largura MÁXIMA.** `set_size_request` declara o mínimo, e
  `halign=CENTER` com mínimo declarado **trava** o widget naquele número — era
  assim que o card ficava em 960 px numa janela de 1920. A cura só cabe no
  `do_size_allocate` (`app/widgets/controller_card.py:886-911`), com
  `LARGURA_CARD_ELASTICA = 1400` (`:316`) e `halign` em `FILL` de propósito.
- **"Doze pixels de folga não são folga":** com fator 13/8 o glifo ia a 58 px e o
  card pedia 357 px contra 369 disponíveis **nesta** máquina — e a CI, sem as
  fontes do projeto, mediu **431 px** e reprovou. O fator caiu para 12/8
  (`app/widgets/controller_card.py:195`). Vizinho instrutivo:
  `gui/widgets/button_glyph.py:290-294` devolve `None` em qualquer falha de SVG, e
  sem librsvg o pixbuf `None` degrada a **medida**, não só o desenho.
- **A escala de fonte é o parâmetro mais influente do layout e não tem
  superfície na janela.** `theme.escala_fonte()` lê `gui_preferences.json`, cujo
  dicionário de defaults tem uma chave só (`app/gui_prefs.py:25`); nada em `app/`
  escreve `escala_fonte`. O comentário de `app/widgets/controller_card.py:150-157`
  chama isso de "o recurso que a mantenedora tem para enxergar melhor" — e ele só
  é alcançável editando JSON à mão, com reinício.
- **Dois pollers decidem se agem lendo o ÍNDICE da aba**
  (`app/actions/status_actions.py:1189`, `app/actions/home_actions.py:679`) no
  mesmo programa que documenta esse padrão como falha silenciosa
  (`app/app.py:774-778`). `grep -rn get_current_page tests/unit` devolve **zero**:
  reordenar as abas faria a aba Status parar de atualizar a 10 Hz sem erro, sem
  log e sem teste vermelho.
- **A statusbar é uma PILHA por contexto**, e apagar a mensagem de um contexto faz
  **ressurgir** a de outra aba (`app/actions/home_actions.py:728-749`). Foi por
  isso que o aviso do cadeado passou a ser escrito **por borda**, usando o
  contexto alheio de propósito.
- **A causa do cadeado só aparece na tela na página 0.** `autoswitch_lock_text`
  (`app/actions/home_actions.py:129-150`) é renderizada pelo `_tick_home_state`,
  que retorna cedo se `get_current_page() != 0`. **Em qualquer outra aba, o
  cadeado é uma caixinha marcada sem explicação.**
- **Os cinco checkboxes `player_led_1..5` estão invisíveis**
  (`gui/main.glade:1013-1016`) e continuam sendo o **único** lugar onde a GUI
  guarda o desenho das cinco luzes. `builder.get_object` de ID inexistente devolve
  `None` sem crash: apagá-los faria "Aplicar o desenho" gravar "tudo apagado" no
  perfil dela.
- **Três definições de "microfone" convivem na mesma janela**, com três fontes de
  verdade: a aba Emulação lê a presença de drop-ins do WirePlumber
  (`app/actions/emulation_actions.py:354-377`), o selo do card vem do mute do
  PipeWire, e o **botão** vem do byte de firmware `audio.mic_mudo`
  (`app/widgets/controller_card.py:698-743`). As três podem discordar
  legitimamente, e nada na tela explica que são camadas diferentes.
- **O `status` do `profile.apply_draft` significa "recebi", não "apliquei"**, e
  isso é contrato: fica fixo em `"ok"` porque applet, CLI e TUI decidiriam por ele.
  A verdade é aditiva (`applied`/`failed`). Quem colapsa as duas reproduz o
  defeito curado em `app/actions/footer_actions.py:163-183`.
- **A seção `mouse` do Aplicar não leva `enabled`, de propósito**
  (`app/draft_config.py:854-863`): o dono do liga/desliga é o MODO, e emitir
  `enabled` faria um Aplicar disparado por mexer num gatilho durante o jogo
  mandar o `enabled=True` de uma sessão de desktop anterior — o daemon aplicaria
  a exclusão mútua e **o vpad morreria no meio da partida**.
- **A aba Emulação — para onde a interface manda a usuária quando algo dá errado —
  é a única sem poller nenhum** (`app/actions/emulation_actions.py:137`).
- **O render de 10 Hz PAUSA enquanto qualquer popup detém grab GTK**
  (`app/actions/status_actions.py:1461-1479`): os sticks tremem em repouso e o
  re-layout fechava qualquer combo aberto. É a mesma razão pela qual o diálogo do
  wrapper é **não-modal**.
- **`app/compact_window.py` se contradiz dentro do próprio arquivo:** o docstring
  (`:14-18`) diz "AUTO por default com opt-out"; o código (`:61-69`) e o call site
  (`app/app.py:988-994`) dizem **opt-in, default desligado**.

### 6.4 Perfis e troca automática (`profiles/`)

- **A eleição não é só prioridade: especificidade vence prioridade.** A chave é
  `(not e_catch_all, priority)` (`profiles/manager.py:640`) — um perfil de jogo em
  prioridade 0 ganha de um catch-all em 100. `docs/usage/creating-profiles.md:97`
  ainda diz o contrário.
- **O debounce é ASSIMÉTRICO e a assimetria é medida:** 0,5 s para entrar num
  perfil específico, **12 s** para sair rumo a catch-all
  (`profiles/autoswitch.py:44-58`). Com 0,5 s nos dois lados, o journal de 22-23/07
  mostrava troca `vitoria` <-> `Navegação` a cada 18-28 s **no meio do jogo**. O
  ADR-006 não conta isso.
- **Leitura vazia PULA o tique inteiro e RETÉM o perfil**
  (`profiles/autoswitch.py:198-225`), ao contrário do que o ADR-007 descreve
  ("cai em MatchAny -> fallback"). A justificativa é boa (o EIO de BT mediu 5,1 s;
  loading dura minutos) e **o efeito colateral é que backend cego = autoswitch
  congelado para sempre, sem log por tique**.
- **A decisão não distingue "nenhuma janela" de "não sei olhar".**
  `_tick_sem_informacao` (`profiles/autoswitch.py:419-436`) colapsa info vazio e
  `wm_class` em `("", "unknown")` no mesmo ramo, com tratamento idêntico ao da
  própria GUI em foco. A distinção existe **só na observabilidade**: seis motivos
  no backend X11, três no leitor, um no NullBackend.
- **O laço do autoswitch NÃO protege o tique.** Só a leitura da janela está dentro
  do try (`profiles/autoswitch.py:152-156`); `self._tick(...)` está fora (`:158`).
  E **nada valida `window_title_regex`** — nem o schema (`profiles/schema.py:67`)
  nem o editor. Um regex inválido em qualquer perfil levanta `re.error` dentro de
  `MatchCriteria.matches`, sobe até o tique e **mata a task do autoswitch pela
  sessão inteira**, sem log e sem `set_exception_handler`. Dedução, não medição.
- **Custo escondido do caminho quente:** `select_for_window_ex` chama
  `load_all_profiles()` a cada tique (`profiles/manager.py:613`), que faz um
  `FileLock` e um `json.loads` por arquivo. Com 15 perfis, **dois** seletores e
  2 Hz, são ~60 aberturas de lock por segundo; os `.lock` no diretório dela têm
  mtime de hoje.
- **Existem DOIS `ProfileManager` vivos no daemon** (o do subsystem, com
  appliers, e o de leitura cacheado do lifecycle,
  `daemon/lifecycle.py:2878-2906`), com campos de dedup de **instância** — os dois
  logam empate e veto separadamente. O cache existiu porque um manager novo por
  tique fazia a dedup nunca valer.
- **O desempate por incumbente está sendo exercitado apenas pelo diagnóstico:**
  quase todas as 26 linhas de empate de hoje saem com `wm_class=unknown` ou
  `Hefesto-Dualsense4Unix`, ou seja vêm do caminho do **sinal de jogo**
  (`daemon/lifecycle.py:2908-2931`), não do autoswitch, que pula esses tiques.
- **O modo jogo padrão aplica a máscara `dualsense`, não `xbox`**
  (`daemon/lifecycle.py:1859`, lendo o flag do disco). Todo preset de jogo de
  fábrica usa `xbox`, e existe uma **migração one-shot inteira**
  (`profiles/loader.py:194-239`) só para tirar `dualsense` dos presets, porque essa
  máscara faz o jogo ignorar o vpad e matar a vibração. **O automatismo entrega
  justamente a máscara que o projeto abandonou.** Não achei sprint que justifique.
- **Cinco escritores de perfil não usam `save_profile`**: as quatro migrações
  fazem `path.write_text` cru, sem escrita atômica e **sem revalidar o schema**
  (`profiles/loader.py:230, 284, 363, 438`), mais a semeadura por `shutil.copyfile`
  (`:173`). Todas rodam no primeiro `load_*` de cada processo — daemon, GUI e CLI.
- **"Restaurar padrão" do rodapé não restaura o perfil selecionado:** sobrescreve
  especificamente `meu_perfil.json` (`app/actions/footer_actions.py:36-37, 453-455`).
- **`coop_local.json` é um risco ativo.** Casa por título frouxo (`|Portal 2|`,
  `|LEGO |`, `Stardew Valley`, `Cuphead`), prioridade 75,
  `mode: {kind: gamepad, gamepad_flavor: xbox}`, `suppress_desktop_emulation:
  true`. Por `perfil_declara_modo_de_jogo` ele **fura o cadeado**: abrir Portal 2
  com o cadeado ligado troca o perfil dela e a máscara de `dualsense` para
  **XBOX**. É a entrega 3 da PERFIL-JOGO-01, não feita.
- **Armadilha do sticky no nascimento do perfil:**
  `app/actions/profiles_actions.py:835` decide se o perfil novo nasce amarrado a
  um jogo lendo `window_detect_last_class` — o campo sticky que nunca decai. Com o
  detector cego e o sticky preso num `steam_app_*` de horas atrás, criar um perfil
  de **desktop** pode nascer amarrado ao appid do jogo anterior.
- **`integrations/xlib_window.py` continua na árvore**: 111 linhas que nenhum
  código de produção importa e que leem `_NET_ACTIVE_WINDOW` **sem gate de foco**
  — o defeito exato que UX-02/FOCO-01 curaram, preservado num arquivo que ainda
  importa limpo. Candidata CODIGO-MORTO-01, sem documento.

### 6.5 O vpad uhid e o broker root

- **O vpad é um DualSense de verdade, verificado ao vivo agora.** `/dev/hidraw5`
  é "Hefesto Virtual DualSense P1", `HID_ID=0003:0000054C:00000DF2`,
  `HID_PHYS=hefesto-vpad`, `HID_UNIQ=02:fe:00:00:00:01`, com `input46` (pad),
  `input47` Motion Sensors, `input48` Touchpad, `input49` Headset Jack e os LEDs.
  O descritor carregado tem 289 bytes e é **byte-idêntico** (`cmp`) a
  `captures/dualsense_usb_descriptor_054c0ce6.bin`.
- **O broker está funcionando, medido ao vivo:** `/dev/hidraw4` (o DualSense
  físico no cabo) está `crw------- root:root` **sem ACL** — a assinatura exata do
  hide (`removexattr` + `chmod 0600`) —, enquanto o vpad está `crw-rw----+` com
  `user:vitoriamaria:rw`. As duas units active.
- **O descritor e os features nunca são lidos do controle na hora de nascer**: vêm
  de constantes embutidas. O motivo é um modo de falha provado: por BT, com o
  controle ocioso, cada `GET_REPORT` estourava o timeout de 5 s do hidp com EIO
  **por minutos**, o vpad caía para uinput 0ce6 e ficava indistinguível do físico
  — a receita do "jogo com zero controles".
- **`UHID_START` não prova nada:** ele chega no **começo** do probe. Medido ao
  vivo com dois vpads de MAC igual, o segundo recebeu START, OPEN, GET_REPORT,
  GET_REPORT, CLOSE, STOP em 2 ms enquanto o kernel logava `probe failed -17`. A
  confirmação real é "vi START e o STOP não veio em 50 ms"
  (`integrations/uhid_gamepad.py:1053-1092`).
- **Payload zerado não é neutro em três lugares:** 0 é o **canto** do stick; o
  byte de contato do touchpad é **invertido**, então sem carimbar `0x80` o vpad
  nasce com dois dedos fantasma presos no canto; e o byte de status zerado anuncia
  5% descarregando para sempre (`integrations/uhid_gamepad.py:268-356`).
- **O gate de rumble é MÁSCARA `0x03`, não bit único**, porque com firmware
  >= 0x0215 o driver liga `use_vibration_v2` e deixa o `valid_flag0` com `0x02`
  sozinho — **os dois DualSense da máquina são 0x0630**, e testar só o `0x01`
  descartaria todo o rumble justamente no hardware alvo. O preço é "fica tremendo
  sem parar", mitigado por teto de silêncio de 3,0 s cujo número veio de medição:
  90 minutos de Stray em 25/07 deram 17 disparos.
- **HIDIOCGRAWINFO no próprio fd não é cinto extra: é o fechamento de uma
  primitiva de keylogger.** `rdev(fd)==sysfs(base)` prova `no==base`, não a
  identidade do device; no minor-reuse o broker serviria um fd O_RDWR **de root**
  de um hidraw alheio (um teclado BT) a um processo do mesmo uid
  (`broker/hidraw_broker.py:98-104, 471-485`).
- **O broker falha FECHADO e o daemon falha ABERTO**, e as duas escolhas derivam
  do mesmo "na dúvida, o lado seguro", porque os riscos são opostos: agir sobre nó
  errado versus auto-adoção com feedback loop
  (`broker/hidraw_broker.py:224-229` contra `core/backend_pydualsense.py:168-169`).
- **A fronteira de segurança declarada:** o cmd `open` não exige que o nó esteja
  escondido, então **qualquer processo do uid autorizado que alcance o socket
  obtém um fd O_RDWR root do DualSense físico**. "Mesmo uid = mesmo domínio de
  confiança", e o validador confina o dano ao DualSense.
- **Fato lateral que a arquitetura do broker não cobre:** `/dev/hidraw0` a
  `hidraw3` desta máquina estão `crw-rw-rw-` (0666), abertos ao mundo, por
  `/etc/udev/rules.d/60-openrgb.rules` — **não é regra do Hefesto**. São
  receptores 2.4G, não controles, mas é superfície do mesmo uid que nenhuma regra
  nossa fecha.
- **ACHADO:** `_reply_get_report`/`_reply_set_report` leem `self._fd` duas vezes e
  suprimem só `OSError` (`integrations/uhid_gamepad.py:1412-1431`) — exatamente a
  armadilha que `pump_ff` documenta e cura em `:1130-1134`. Um `stop()` concorrente
  faz `os.write(None, ...)` levantar **TypeError**, que em `wait_for_bind` subiria
  por `make_virtual_pad` até `set_gamepad_emulation`.
- **DOCSTRING QUE CONTRADIZ O CÓDIGO QUE A IMPLEMENTA:**
  `integrations/uhid_blueprint.py:44-46` afirma como limitação aceita que congelar
  a calibração é "inócuo hoje: o vpad emite motion neutro e não repassa gyro do
  físico", e que "se um dia houver passthrough, a calibração por unidade volta a
  importar". **Esse dia chegou** — o GYRO-01 espelha a janela verbatim
  (`integrations/uhid_gamepad.py:540-547`).

### 6.6 Integrações com o desktop (Steam, Proton, PipeWire, notificações)

- **O eixo Steam tem DOIS cadastros e é isso que explica a divergência:** o
  `localconfig.vdf` da Valve (reescrito pela Steam ao sair, daí o guard por
  `.path`/`.timer`) e a allowlist nossa `steam_input_apps.txt` (intenção dela, que
  o guard tem de **preservar**).
- **O projeto ENSINA o gesto morto.** `integrations/desktop_notifications.py:352`
  diz "Emulação de mouse/teclado desativada. Segure o PS de novo para reativar" —
  e essa é a **única** notificação de desktop que dispara sem opt-in (`:341-356`
  ignora `_notifications_enabled` de propósito). Todo o resto está atrás de
  `HEFESTO_DUALSENSE4UNIX_DESKTOP_NOTIFICATIONS`, que **não é definida em lugar
  nenhum do repo**: controle conectado, bateria, perfil ativado e avisos de infra
  são no-op garantido.
- **`notify_battery_low` e `notify_battery_recovered` não têm nenhum chamador em
  `src/`** — só o próprio módulo, o `__all__` e os testes. O cabeçalho anuncia
  bateria como "evento coberto". Função testada, documentada e nunca ligada.
- **TER um perfil para o jogo pode DESLIGAR o modo jogo automático.**
  `_sincronizar_modo_jogo_padrao` trata qualquer motivo diferente de
  `MOTIVO_JOGO_SEM_PERFIL_PROPRIO` como evidência positiva de outra janela e chama
  `reverter_modo_jogo_padrao` (`profiles/autoswitch.py:371-378`). Um perfil
  específico salvo com `mode = null` — **o default do editor**
  (`app/actions/profiles_actions.py:452-475`) — faz o autoswitch soltar o modo
  jogo e não ligar nada no lugar.
- **A evidência #2 do sinal de jogo é estruturalmente cega para os presets de
  fábrica.** `_profile_rule_matches_game` (`daemon/lifecycle.py:2920-2922`) chama
  `select_for_window({"wm_class": wm_class})` — sem `wm_name` nem
  `exe_basename`. Como `MatchCriteria.matches` é AND, todo perfil que casa por
  título ou processo **reprova sempre**. É exatamente o formato de
  acao/aventura/corrida/esportes/fps/coop_local, e é justo o caso que a docstring
  diz cobrir ("GOG/Heroic fora da Steam").
- **`sackboy_nativo.json` se chama "nativo" e entrega máscara `xbox`**,
  contradizendo `docs/usage/jogos-e-mascaras.md:57-61`, que classifica Sackboy
  como suporte nativo a DualSense e se declara "a fonte da verdade sobre
  compatibilidade". A cópia no HOME dela **já está com `dualsense`** — ela
  corrigiu na mão o que o preset do repo entrega errado.
- **A lista de IGNORE estendida pela usuária é INTOCÁVEL, e o motivo é
  cirúrgico:** remover o pedaço do Hefesto de `...0x0ce6,0x057e/...` deixaria
  `,0x057e/...` pendurado, que o `env(1)` tentaria **executar** — ENOENT, jogo que
  nunca mais abre (`integrations/steam_launch_options.py:138-145`).
- **`PROTON_DISABLE_HIDRAW` nunca inclui `0x0DF2`, e há comentário proibindo**
  (`daemon/launch_env.py:85-91`): o vpad se apresenta como Edge e **precisa** do
  hidraw. Esconder o 0df2 mataria rumble, gatilhos e lightbar vindos do jogo.
- **Instalar o Hefesto muda a versão de Proton de toda a biblioteca dela.**
  `install.sh:2303` roda `proton_pin.py --lock`, que trava o default **global**
  (entrada "0") mais todos os appids de `appmanifest_*.acf`. O opt-out existe
  (`--no-proton-pin`), o default é ON, e o registro em `proton-pin-lock.json`
  guarda 12 jogos com `previous_name` preservado.
- **O microfone por BT não é A2DP, e o custo foi medido em A/B de 3 s**
  (`integrations/dualsense_bt_audio.py:77-88`): mic off = 260,4 Hz de input; mic on
  = 170,5 Hz de input + 106,2 Hz de áudio. **O total não muda** — o áudio não abre
  canal, ocupa lugar na fila. ~35% dos relatórios, e quem paga é o espelho de
  motion.
- **A armadilha de PipeWire que custou uma hora** está em
  `integrations/dualsense_bt_audio.py:543-550`: sem `wireplumber.service` vivo, o
  `module-pipe-source` carrega, aparece em `pactl list sources` e fica SUSPENDED
  **para sempre**. O sintoma é indistinguível de "o protocolo está errado".
- **`docs/usage/bluetooth.md:102-105` afirma que áudio do DualSense por BT
  "continua fora de escopo".** Isso é FALSO na v0.3.0: são 1.286 linhas
  implementando exatamente isso, com subcomando e subsystem. E
  `docs/usage/cli.md:218` descreve a ponte corretamente e manda "ver
  bluetooth.md" — **o documento que diz que a feature não existe.**

### 6.7 A aba Sistema (`app/actions/daemon_actions.py`, 1.873 linhas) — a lacuna

Quinto maior arquivo do projeto, maior que `manager.py` + `autoswitch.py`
juntos, **não citado por nenhum dos treze mapas** — nem na lista de componentes
do mapa da GUI, que enumera 20 módulos de `app/actions/` e pula justamente esse.
É a única parte da janela que escreve em arquivos que não são do Hefesto.

- **MARCAR O JOGO ERRADO É O CENÁRIO NORMAL, NÃO O EXCEPCIONAL — medido agora.**
  `_appid_do_jogo_ativo` (`app/actions/daemon_actions.py:929-968`) resolve por três
  evidências em cascata, e elas estão em conflito neste instante: (1) o marker
  `last_run` diz `appid=2111190 pid=21917` de 17:49:48 e por isso devolve `None`
  (idade 6.290 s contra `WRAPPER_MARKER_WINDOW_SEC = 900`); (2) a próxima
  evidência é `window_detect_last_class`, o campo **sticky**, que aponta
  `steam_app_3357650` (Pragmata, última leitura útil às 18:53:00). **Se ela
  clicar agora pensando no Mullet Mad Jack, o botão marca PRAGMATA.** Hoje é
  invisível porque os dois já estão na allowlist; com qualquer terceiro jogo o
  clique gravaria o appid errado em silêncio, **com toast de sucesso**.
- **E o próprio projeto já proibiu esse sticky em outro lugar.**
  `daemon/state_store.py:496-506` e `daemon/subsystems/game_signal.py:29` dizem
  explicitamente que o sticky é **vetado** como evidência de jogo porque "nunca
  decai". A função gêmea `steam_input_exception_appid`
  (`daemon/launch_env.py:447`) usa o **cru** exatamente por isso, e comenta a
  escolha. Duas funções que decidem o MESMO appid, com critérios opostos.
- **A contradição de tela foi criada pelo mesmo commit que a refutou.** O tooltip
  `gui/main.glade:2069` diz "ainda não existe um botão para desmarcar" e o
  comentário `:2055-2066` afirma "**não há superfície de remoção nenhuma: nem
  aqui, nem na linha de comando**". Mas `git log -- cli/cmd_steam.py` tem UM
  commit: `e96dea8` (27/07) — o **mesmo** que reescreveu esse tooltip, e cuja
  mensagem diz "o desfazer do Steam Input passou a existir".
- **E há um portão que proíbe escrever a verdade.**
  `tests/unit/test_janela_sem_mentira.py:253` bane a palavra "desfazer" em texto
  de ajuda de widget clicável, e a válvula de escape `_contraparte_na_janela`
  (`:400-418`) só procura a função inversa dentro de `app/` — onde
  `remove_appid_from_steam_input_allowlist` não aparece. **Um tooltip honesto que
  use o verbo "desfazer" quebra a suíte.** A correção mínima viável usa
  "desmarcar", que não está em `_PALAVRA_DE_PROMESSA`.
- **O toast do Proton mente numa recusa real.** `integrations/proton_pin.py:837`
  mapeia `errors: 1 if status == "erro" else 0`, e `status="recusado"` (Steam ou
  jogo aberto) não é "erro". Com `locked=0, skipped=0, errors=0`, o formatador diz
  "**Nada a mudar — os jogos já estão no Proton validado**". O caminho é
  alcançável: ela clica no Hefesto justamente enquanto joga. O CLI do mesmo módulo
  é honesto no mesmo caso (rc=3). **É o único ponto da aba onde uma ação NÃO
  executada se anuncia como estado desejado alcançado.**
- **"Corrigir modo de execução" pode deixar a máquina pior e dizer que
  melhorou.** `on_daemon_migrate_to_systemd` (`:1571`) manda SIGTERM no daemon
  avulso **sem confirmação** — é o único botão de escrita da aba sem diálogo e o
  único que mata um processo funcional. Depois, quando cai no fallback
  `subprocess.Popen` (`:1369-1385`), anuncia "o Hefesto agora liga sozinho e volta
  sozinho se travar" (`:1619-1622`) sobre um **processo filho da GUI**, que não faz
  nem uma coisa nem a outra.
- **O painel "Detalhes técnicos" nunca contém o erro para o qual ele é
  apontado.** 14 mensagens mandam ela ver os Detalhes técnicos; as únicas coisas
  que chegam ao `daemon_status_text` são `systemctl status` e `journalctl` da
  unit. Os erros de Steam, Proton e allowlist vão para `logger.warning` do
  processo da GUI — outro journal, outro processo. **Todo apontamento de
  diagnóstico dessas cinco ações é um beco sem saída.**
- **Os backups se acumulam para sempre e ninguém poda.** Contados agora em
  `~/.steam/steam/`: **13** `localconfig.vdf.bak.hefesto-launch-<ts>` (~115 KB
  cada), **15** `config.vdf.bak.hefesto-proton-<ts>` e **5**
  `localconfig.vdf.bak.steam-input-<ts>`. Os diálogos prometem "fica um backup ao
  lado" sem dizer que cada clique cria um novo. Nada novo desde 26/07 — o que
  também diz que esses cinco botões não foram usados nos últimos três dias.
- **O censo de handlers do mapa da GUI não vê os dois botões que mexem na
  Steam.** `btn_steam_ready` (`gui/main.glade:2042`) e `btn_steam_game_broken`
  (`:2067`) **não têm `<signal>`**: são ligados em código por
  `_wire_steam_simple_buttons` (`app/actions/daemon_actions.py:396-418`). Um widget
  sem `<signal>` não entra em nenhum dos dois lados da conta "64 no glade x 66 no
  dicionário": a aritmética está certa e o diagnóstico é enganoso. Se o
  `contextlib.suppress(Exception)` de `:416` engolir o connect, **os dois ficam
  mortos e a métrica marca saúde perfeita**.
- **O `BUG-GUI-REPO-ROOT-OFFBYONE-01 não foi eliminado — foi duplicado.** O mesmo
  resolvedor existe quatro vezes com o índice cravado à mão:
  `app/actions/daemon_actions.py:431` usa `parents[4]`, `cli/cmd_doctor.py:25` e
  `cli/cmd_mic.py:91` usam `parents[3]`, `profiles/loader.py:102` usa
  `parents[3]`. E `app/constants.py:37` **já define** `ROOT_DIR`. O teste de
  regressão valida resolvendo arquivos reais do checkout: **ele não pode falhar no
  cenário que importa**.
- **O estado "Verificando..." pode ser permanente.** O `except Exception` de
  `_refresh_daemon_view_async` (`:1187-1189`) apenas loga e retorna — sem
  `GLib.idle_add`, sem toast, sem retry. Nada mais repinta o rótulo, e clicar
  "Atualizar" executa o mesmo caminho.

### 6.8 `daemon/sensor_hub.py` — o quarto laço, e a segunda lacuna

342 linhas, um commit desde 24/07, **zero fatos em treze mapas**. É o único laço
periódico do daemon que não é task asyncio e não tem parada no shutdown.

- **Ele nasce de dentro do `state_full`.** Quem o instancia é `_merge_sensores`
  (`daemon/ipc_handlers.py:1821-1826`), na primeira vez que um controle com bloco
  `inputs` aparece no payload. Sobe uma thread `hefesto-sensor-hub` a 1 Hz
  (`daemon/sensor_hub.py:164-170`) e abre nodes de evdev por controle sob demanda,
  com TTL de 5 s (`:48-56`).
- **O cabeçalho promete um ciclo de vida que o código não cumpre.**
  `daemon/sensor_hub.py:16-20` afirma que "fechar a GUI (ou só sair da aba Status)
  apaga as threads sozinho". **Não apaga**: o tique de 2 Hz da aba Status
  (`app/actions/status_actions.py:1225-1238`) não tem porteira de aba, e o tray
  bate `daemon.state_full` **a cada 3 s** (`app/tray.py:46, 191, 323-334`, ligado
  incondicionalmente em `app/app.py:979-987`). **3 s < 5 s do TTL.** O comentário
  de `:49-51` escolheu 5 s para cobrir "o tique de 10 Hz da GUI" e nunca contou o
  tray. O hub só morre quando o **processo** da GUI morre.
- **Medido agora, com o daemon de 2h34m:** `/proc/2430/fd` tem 4 fds de
  `/dev/input` — `event21` (gamepad principal), `event22` (Motion Sensors, **só o
  hub abre esse**) e **dois** em `event23` (Touchpad: o do cursor mais o
  observador do hub). Há 8 fds de `pipe:` = 4 self-pipes x 2, ou seja quatro
  readers vivos e nenhum órfão. **Metade dos leitores de evdev do daemon existe só
  para alimentar a aba Status.**
- **Custo medido em repouso:** as duas threads de tid mais alto têm utime de 616 e
  3 ticks — ~6,2 s e ~0,03 s de CPU em ~11,5 min. O observador de touchpad é
  grátis (o node só fala com o dedo apoiado); o de giroscópio custa **~0,9% de um
  núcleo continuamente**, porque o sensor reporta em repouso. Com quatro
  controles, multiplica por quatro.
- **RISCO, o mais grave: descoberta pesada sem timeout nem supervisão, na mesma
  janela de churn que gerou o wedge de GIL.** `_abrir_readers`
  (`daemon/sensor_hub.py:243-248`) faz **duas** enumerações completas de
  `/dev/input` mesmo quando falta um tipo só, e cada enumeração abre todos os
  nodes (o projeto mede 10-40 ms). `_garantir_manutencao` (`:154-169`) ressuscita a
  thread apenas se ela **morreu** (`is_alive()`), nunca se ela travou — **thread
  travada = `is_alive() == True` para sempre**, sem log acima de debug. E é
  exatamente o tipo de varredura que obrigou o daemon a isolar um pool inteiro e
  a **aceitar vazar worker** (`daemon/lifecycle.py:69-99`). Se o wedge for de
  processo, como o comentário afirma, estar fora do event loop **não protege**.
  Journal de hoje: `backend_hotplug_reconcile trigger=input_dir_change` às
  19:13:31 e 19:13:48, com o hub reabrindo às 19:13:46 — tudo em 20 s.
- **`stop_all()` não tem chamador em `src/`.** `connection.shutdown()`
  (`daemon/connection.py:489-588`) desmonta treze recursos à mão e não menciona o
  hub — nem o `_metrics_subsystem`, que tem `stop()` e também não é chamado. É a
  dívida "o registry não é iterado" se materializando de novo. **Armadilha para
  quem for curar:** `stop_all` seta `_parar` e **nunca o limpa** (`:138`), então o
  hub é de **uso único** — ligá-lo ao shutdown é seguro, ligá-lo a "a GUI fechou"
  mataria os sensores até o próximo restart, em silêncio.
- **O hub NÃO pode alterar o que o poll loop enxerga, e isso é verificável em três
  pontos independentes** (nenhum reader do hub graba; cada `open()` de node evdev
  recebe fila própria do kernel; `consume_motion()` tem um chamador que resolve
  outro objeto). **A suspeita "nenhum atalho funciona dentro do jogo" tem de ser
  investigada em outro lugar.**
- **A justificativa escrita do `acumular_movimento=False` está trocada.**
  `daemon/sensor_hub.py:28-31` diz que um segundo acumulador "viraria salto de
  cursor". Não viraria: o delta acumula no objeto do hub e o cursor sai do objeto
  do poll loop. **Decisão certa, motivo exagerado** — registrado porque um dia
  alguém vai "corrigir" isso achando que o acoplamento é real.
- **Os três pollers da aba Status ficam nos 0,25 s default**
  (`app/actions/status_actions.py:1196, 1232, 1260`) contra a declaração escrita de
  que 0,25 s **não basta** para `state_full` sob carga
  (`app/actions/mode_transition.py:39-44`). Quando estoura,
  `_on_live_state_failure` chama `_reset_live_widgets()` e **o card apaga com o
  daemon vivo**.

### 6.9 Empacotamento e o applet Rust

- **A v0.3.0 publica SEIS artefatos e existem QUATRO formatos no repositório que a
  release não publica** (Arch, Fedora, Nix e o applet COSMIC).
- **`ci.yml` e `release.yml` disparam os dois na mesma tag e não se conhecem.** O
  `release.yml` roda 7 portões; o `ci.yml` roda 16 jobs, entre eles
  `packaging-parity`, `shellcheck`, `gtk-real` e `smoke-multi-distro` — e
  **nenhum deles bloqueia a publicação**. Um `ci.yml` vermelho e uma release verde
  convivem.
- **O caminho de ativação do `.deb` está MORTO e nada na CI vê.**
  `packaging/debian/postinst:39` manda rodar `install-host-udev.sh`; esse script
  elege `/usr/share/hefesto-dualsense4unix/udev-rules` (`:33-41`) e exige as 14
  regras, senão `exit 1` (`:224-225`) **antes de qualquer instalação**. Mas
  `scripts/build_deb.sh` popula esse espelho com um glob que **para na 81**
  (`:251-253`), enquanto o diretório vivo recebe até a 84 (`:153-156`).
  Resultado: sem grupo `hefesto`, sem broker, sem nenhum dos três DKMS. **O gate
  de paridade passa verde por construção**, porque
  `scripts/check_packaging_parity.sh:111-113` só pergunta se o glob aparece em
  **algum** lugar do arquivo.
- **A ordem dos candidatos faz um pacote instalado SEQUESTRAR a execução a partir
  do repositório:** `/usr/share/...` vem **antes** de `${SCRIPT_DIR}/../assets`.
- **O terceiro DKMS não é desregistrado na remoção.**
  `hefesto-hid-playstation` tem **zero** ocorrências em `packaging/debian/prerm`,
  `postrm` e no `.install` do Arch, contra 7, 6 e 8 do `hefesto-hid-nintendo`. Com
  `AUTOINSTALL="yes"`, depois de `apt remove` o módulo patchado continua
  registrado e **vence o in-tree para sempre**. O gate é hardcoded por módulo e
  nunca ganhou o terceiro bloco.
- **O spec do Fedora não compila:** instala
  `%{_datadir}/%{app_id}/dkms/hid-playstation/` (`:145-147`) e o `%files` lista
  apenas os outros dois. Com o `%_unpackaged_files_terminate_build` default, o
  rpmbuild aborta. **Nada no CI executa rpmbuild** — provavelmente nunca foi
  construído.
- **O flake Nix quebra ANTES do `lib.fakeSha256` que o README admite:** o
  `postInstall` instala `assets/73-*.rules` e `74-*.rules`
  (`packaging/nix/package.nix:103-106`), **removidas do repositório em 18/07**.
- **O ícone do lançador está quebrado em três dos cinco formatos**, e o gate TEM
  um bloco de verificação de `Icon=` — que faz
  `grep -q '^X-CosmicApplet=true' || continue` (`:46`), **pulando justamente o
  `.desktop` do aplicativo principal**.
- **A numeração voltou de 4.0.0 para 0.1.0 e nenhum gerenciador recebeu epoch.**
  Para apt, dnf e pacman, **0.3.0 é um downgrade** e o upgrade é recusado. O
  `%changelog` do spec ainda termina em `3.4.0-1`, maior que o `Version:` do
  próprio arquivo.
- **Três arquivos carregam versão e nenhum gate os vê:** o metainfo AppStream do
  Flatpak (mais recente = 3.13.3), o `Cargo.toml` do applet (0.1.0) e o banner do
  AppImage, que imprime **"v3.0.0"** e sugere um `.deb` que não existe mais — é o
  primeiro texto que um usuário novo vê.
- **O bundle Flatpak não semeia perfis default.** O manifesto instala os glyphs
  mas **nunca** instala `assets/profiles_default` em nenhum dos três candidatos de
  `profiles/loader.py:102-106`. O `build_appimage_gui.sh:111-118` faz exatamente
  essa cópia com a tag `FIX-APPIMAGE-PRESET-SEED-01`: **o defeito foi
  diagnosticado e curado para o AppImage e nunca portado**.
- **`packaging/cosmic-applet/Cargo.toml:5` tem um e-mail pessoal real em
  `authors`.** O `check_anonymity.sh` não procura e-mails e o
  `check_test_data.sh`, que tem o regex, só varre `tests/`. O `PKGBUILD:1` foi
  redigido para `[REDACTED]` — a intenção existe, o applet ficou fora. E o
  `Cargo.toml` viaja no tarball da tag que Arch e Fedora baixam.
- **O applet está VIVO e instalado nesta máquina** (`/usr/local/bin/...`, 23,6 MB,
  28/07 23:23) e é o único componente com suíte própria que **não roda em lugar
  nenhum**: 17 testes Rust, zero menção a `cargo` nos quatro YAMLs. Dois deles são
  caros de perder: `troca_de_modo_nao_cabe_no_timeout_de_leitura` e
  `timeout_de_modo_espelha_o_da_gui` (`ipc.rs:638-685`), que travam o
  `MODE_IPC_TIMEOUT` contra o da GUI.
- **O applet não tem NENHUMA superfície de autoswitch** — zero menção nas 1.745
  linhas de Rust. Para os defeitos 1 e 2 ele não é parte do problema nem da
  solução, mas também não oferece a válvula de escape que a aba Início oferece.

### 6.10 Testes, portões e CI

- **330 arquivos `test_*.py`, 103.526 linhas de teste contra 67.902 de `src/`**,
  5.161 funções `def test_` que viram 5.783 coletados na máquina dela e 5.226 no
  CI. **Treze gates vivos hoje** — a PORTAO-VIVO-01 mediu "não há portão nenhum
  no caminho do commit" e isso **foi pago**.
- **`tests/integration/` e `tests/shell/` são andaimes VAZIOS** desde maio: só
  `__init__.py` de 0 bytes.
- **279 testes em 17 arquivos passam verdes contra um GTK deliberadamente falso e
  nunca rodam contra o real.** Eles plantam `Gtk.Box = object` mas **não** chamam
  `exigir_gi_real`, e o critério de seleção do job `gtk-real` é justamente esse
  grep (`ci.yml:387`). Logo: não pulam no `lint-test` (o stub satisfaz o import),
  não entram no `gtk-real`, e a GUARDA-GI-REAL-01 não os alcança. Os nomes
  preocupantes: `test_compact_window.py`, `test_status_actions_reconnect.py`,
  `test_profiles_gui_sync.py`, `test_daemon_status_matrix.py`.
- **A costura onde os três defeitos moram não é cruzada por UM teste.** Os 30
  pontos que instanciam um `AutoSwitcher` passam `window_reader=lambda: {}` ou um
  dicionário literal; os dois arquivos que exercitam o leitor de verdade
  monkeypatcham `build_window_reader`; e o teste do modo jogo injeta a autoridade
  direto (`d._game_signal = SimpleNamespace(authority='game')`,
  `tests/unit/test_modo01_o_modo_jogo_liga_sozinho.py:160`). **Os dois lados são
  densamente testados; a costura, nunca.**
- **O hook de acentuação checa UM arquivo por invocação e descarta o resto, em
  silêncio.** O entry é `--check-file` (`.pre-commit-config.yaml:23`) e o
  pre-commit apenda os nomes; o argparse consome o primeiro e joga os demais no
  positional `paths`, que `scripts/validar-acentuacao.py:939` ignora. **Com N
  arquivos staged, N-1 passam sem checagem.** Os 12 testes que exercitam
  `--check-file` passam exatamente UM caminho. O gate irmão de glifos **não** tem
  o defeito.
- **O gate de acentuação é cego ao arquivo com MAIS português visível do
  projeto:** `.*\.glade$` está na whitelist
  (`scripts/validar-acentuacao.py:426`), e o `main.glade` tem 2.783 linhas com os
  rótulos das nove abas. Junto vão `.json`, `.desktop`, `.service` e `.rules`; os
  `.po` nem entram por extensão.
- **O gate de glifos é cego a toda a família "Emoji sem Emoji_Presentation":** o
  critério é a propriedade `Emoji_Presentation` mais U+FE0F
  (`scripts/validar-glifos.py:198-213`), o que deixa passar U+26A0, U+2764,
  U+2714, U+2611 — que renderizam como emoji em muitas fontes.
- **`check_anonymity.sh` continua cego a arquivo novo não rastreado** (usa
  `git grep`) — a mesma classe de furo que os dois gates de texto curaram com
  `--cached --others --exclude-standard`. E **as exclusões são um vazamento
  real**: `docs/process/**` e `docs/history/**` estão na `EXCLUDE_PATHSPECS` e
  ambos são rastreados (92 e 7 arquivos), com **4 linhas medidas** contendo os
  termos que o gate proíbe.
- **O gate de dados de teste filtra por LINHA, não por ocorrência:** o
  `grep -vE "$ALLOWED_MAC"` remove a linha inteira, então uma linha com um MAC de
  vpad **e** um MAC real ao lado passa limpa. E o escopo é só `tests/`.
- **A matriz "cosmic" do CI testa um COSMIC que não existe na máquina dela**
  (`ci.yml:481-482` **remove** o `DISPLAY` de propósito), e `jeepney` está no
  extra `cosmic` enquanto o CI instala `.[dev]` — o job valida a escolha de uma
  cascata cuja **cabeça e cauda estão ambas mortas**.
- **A cobertura declarada de 70% é medida com os 491 testes de interface
  PULANDO** e sem nenhum `[tool.coverage]` no pyproject: as 20.308 linhas de
  `app/` entram no denominador quase inteiramente descobertas. **Um crescimento de
  `app/` derruba a porcentagem sem nenhum teste ficar pior.**
- **O smoke de runtime não afirma nada sobre trabalho realizado:** o CI apenas
  grepa o log por `AssertionError|Traceback`. Um daemon que sobe, **não poleia
  nada** e desce limpo passa nos quatro jobs da matriz.
- **O job `gtk-real` deixou de rodar a suíte inteira de propósito:** rodar tudo
  sob Xvfb com GTK real morria aos 39% da coleta **sem traceback** — assinatura de
  OOM no runner (`ci.yml:378-381`).
- **`importorskip("gi")` NÃO protege de typelib parcial:** o CI replica o critério
  de "GTK real" **antes** de coletar qualquer teste, num script inline
  (`ci.yml:320-353`), porque typelib parcial derruba a coleta inteira com
  `AttributeError` em `Gtk.ResponseType`.
- **Nenhum `xfail` na árvore inteira**, nenhum marcador customizado, nenhuma forma
  de selecionar subconjunto (sem "lento", "hardware", "bt"). E 364
  `pytest.mark.asyncio` redundantes com `asyncio_mode = 'auto'`.
- **O muro de texto cresceu:** 21 `inspect.getsource` em 8 arquivos, **27 asserts
  com `.count()`** (que literalmente proíbem deduplicar código), 36 arquivos que
  grepam os três scripts grandes, 10 que leem o `.rs` do applet como texto. E **38
  arquivos de teste não importam nada de `hefesto_dualsense4unix`**.
- **O teste que morde é minoria explícita e está rotulada:** 11 ocorrências da
  anotação `FALHA-SEM` em 7 arquivos. A prática existe e é forte onde existe, mas
  a disciplina de "a cura foi arrancada e a suíte reprovou" vive nas mensagens de
  commit, não no código do teste.

### 6.11 Linha de comando, i18n e utils

- **Duas pilhas de IPC na mesma CLI, e metade dos comandos pode pendurar para
  sempre.** `cli/ipc_client.py:47-73` aceita `timeout=None` como padrão e ninguém
  passa prazo nos usos crus: `status`, `battery`, `doctor`, `plugin`, `mic mute`,
  `daemon pause/resume`, o tray e a TUI **inteira**. Os grupos de estado usam o
  `ipc_bridge` da GUI **com** prazo.
- **A seta de dependência está invertida e o código sabe.**
  `cli/cmd_profile.py:403-404` escreve "CLI deveria depender do daemon, não o
  contrário" — e dez pontos de `cli/` importam `app.ipc_bridge`, que é o cliente
  da GUI GTK. Só funciona porque o import de GLib é adiado. Cadeia real:
  `cli -> app -> cli.ipc_client -> daemon.ipc_server`.
- **`profile activate` tem 250 ms para decidir se o daemon existe.** Estourado o
  prazo, `cli/cmd_profile.py:132-148` entra no ramo "offline", abre um **segundo**
  `PyDualSenseController` e **disputa o hidraw com o daemon vivo** — exatamente o
  que o docstring promete que só acontece com o daemon parado.
- **Não existe comando de CLI para o cadeado, para o modo jogo nem para reload.**
  Dos 33 métodos IPC, 12 não têm superfície de terminal, e os **três primeiros** da
  lista são `autoswitch.lock`, `daemon.emulation.suppress` e `daemon.reload` — os
  três caminhos dos defeitos de hoje. A única alavanca é `nc -U` na mão.
- **`utils/session.py` não tem nada de logind: são 9 arquivos de estado**, e o
  delicado é a ontologia de **três** estados — ausência = "nunca decidiu",
  presença = "ela decidiu". Nasceu de dois bugs em que apagar o arquivo para dizer
  "off" confundia decisão com ausência de decisão, e a automação religava em
  segundos o que ela acabara de desligar. Por isso existem **pares** de flags.
- **Os catálogos `.mo` estão rançosos e nenhum gate mede.** `git log -- po/` para
  em `28bf718` (28/07); `git log -- locale/` para em `69bed55` (22/07). Prova
  direta: os msgids "Testar o controle virtual" e "Voltar ao padrão", adicionados
  em 28/07, **não estão** dentro dos `.mo`. `scripts/i18n_compile.sh` não roda em
  CI e `grep -rln 'i18n|gettext' tests/` devolve **zero arquivos**. A tradução
  entregue pelo commit "a janela fala a língua dela" **não chegou a nenhuma
  instalação**.
- **Na máquina dela o catálogo que vale é o de `~/.local/share/locale`** —
  candidato 2 de `utils/i18n.py:60-61`, porque `XDG_DATA_HOME` está vazio.
  `_find_locale_dir` devolve o **primeiro** diretório com qualquer `.mo`, então a
  cópia que o `install.sh:1874-1889` deixou ali **sombreia para sempre** a do
  wheel: um upgrade por pip nunca troca o catálogo em uso.
- **`init_locale()` na CLI não tem como produzir efeito visível:** zero `_()` em
  `cli/` e em `tui/`. O que sobra da chamada são dois efeitos colaterais reais —
  `locale.setlocale(LC_ALL, "")` muda o locale do processo inteiro, e uma linha
  structlog `i18n_initialized` no stderr **a cada invocação da CLI**.
- **`configure_logging()` é idempotente por flag global**, e quem chega primeiro
  define nível, formato e stream. Como `utils/i18n.py:41` cria o logger no import
  do módulo, **a configuração real é feita por ele** e a chamada explícita em
  `daemon/main.py:61` é um no-op silencioso.
- **A defesa contra PID reciclado está neutralizada NESTE checkout.**
  `utils/single_instance.py:54` define o marcador como a substring `hefesto` em
  `/proc/<pid>/comm` **ou** em `cmdline` — e o caminho do repositório é
  `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/...`. Qualquer
  processo cuja linha de comando mencione o repo (um pytest, um editor, um grep)
  passa como Hefesto e volta a ser elegível ao SIGTERM. **O nome da pasta fura a
  guarda que foi criada exatamente para isso.**
- **`daemon start` e `daemon stop` não são simétricos:** `start` roda o daemon no
  **processo atual** (foreground); `stop`/`restart`/`status` despacham
  `systemctl --user`. Quem fizer stop e depois start ganha um processo em primeiro
  plano, não o serviço. `docs/usage/cli.md` se contradiz internamente sobre isso
  (`:160` contra `:171-173`).
- **Parser de cor com armadilha de comprimento:** `cmd_test.py:97` decide
  hex-vs-CSV por `len(color) == 6`, então `--color '9,9,99'` é roteado para
  `hex_to_rgb` e levanta `ValueError` cru — traceback. O mesmo valor com 8
  caracteres funciona.
- **Três dos widgets da TUI são decorativos:** `tui/app.py:151-174` abre uma
  conexão IPC nova a cada 100 ms (**10 por segundo**) e alimenta `TriggerBar` e
  `StickPreview` com literais. E `textual>=0.47` é dependência **obrigatória**:
  quem só quer o daemon paga por ela.
- **`migrate_legacy_paths()` roda no boot do daemon e da GUI, nunca pela CLI.**
  Numa máquina que só usa terminal, perfis do layout legado ficam invisíveis para
  `profile list`.

### 6.12 Instalação, udev, DKMS e o host

- **O `install.sh` (2.347 linhas) não instala um aplicativo: PROVISIONA O HOST.**
  Escreve em `/etc/udev/rules.d` (14 regras), `/etc/modules-load.d`,
  `/etc/modprobe.d` (4 confs), `/etc/bluetooth/main.conf.d`,
  `/etc/systemd/system`, `/etc/NetworkManager/conf.d`, `/usr/local/lib/...`,
  `/usr/src` + `/lib/modules/*/updates/dkms`, regenera o initramfs, mexe no
  cmdline via `kernelstub`, faz backport do `bluez` por apt e edita o
  `localconfig.vdf`/`config.vdf` da Steam. **O formato do app é ortogonal**: quase
  toda essa camada roda em todos.
- **`--no-systemd` NÃO impede a instalação da unit do daemon, e o "não" que ela
  responde no passo 6 é ATROPELADO.** O passo 7a (`install.sh:2006-2027`) copia,
  dá `enable` **e** `restart` — sem gate de flag e sem olhar a resposta. O
  cabeçalho do próprio install (linha 140) ainda afirma "a unit é COPIADA mas NÃO
  habilitada", falso desde que o 7a nasceu.
- **`--with-usb-quirk` é redundante com o default.** O cabeçalho promete "o
  install DEFAULT NÃO aplica", mas o passo 3e é default e
  `kernel_cmdline.plan_tokens` sempre planeja os mesmos IDs
  (`integrations/kernel_cmdline.py:34`). E o **mesmo token tem duas políticas de
  remoção opostas**: `uninstall.sh:1029` imprime "quirk preservado" e 30 linhas
  depois o bloco do registro de posse o **retira**.
- **Não há guarda contra rodar o install COM sudo, e o dano é silencioso.**
  `acquire_sudo` devolve 0 na hora se `EUID==0` (`install.sh:363`) — sem aviso. Com
  `sudo bash install.sh`, `HOME` vira `/root`: o `.venv` nasce root-owned, os
  symlinks vão para `/root/.local/bin`, as units de usuário para
  `/root/.config/systemd/user`. Curiosamente as duas partes que **mais**
  precisariam do uid certo se salvam, usando `SUDO_USER`/`SUDO_UID`.
- **O `doctor.sh` INSTRUI a instalar o amplificador do bug que o projeto curou.**
  `scripts/doctor.sh:2779` sugere instalar e habilitar o
  `hefesto-dsx-recover.service`, e `scripts/dsx_recover.sh:68-70` faz
  `echo 0 > authorized; sleep; echo 1 > authorized` — **re-enumeração por
  software, que é exatamente o gatilho do storm -71** que os passos 3b/3c existem
  para evitar. O `install.sh` nunca instala essa unit e o `uninstall.sh` a remove:
  **asset órfão que só pode chegar à máquina pela mão do doctor.**
- **A cura de autoswitch que o install oferece em COSMIC é medida como no-op pelo
  próprio projeto.** `install.sh:1764-1786` chama `wlrctl` de "caminho recomendado
  que cobre qualquer app Wayland"; `scripts/doctor.sh:1093` registra a medição
  contrária: o cosmic-comp não tem `wlr-foreign-toplevel-management` e "wlrctl
  instalado não ajuda aqui". **O veredito "saudável" do backend é hardcoded como
  `backend == "xlib"`** (`daemon/subsystems/autoswitch.py:99-101`) — em COSMIC,
  saúde = ver só XWayland.
- **A unit NÃO entrega o env gráfico; o fallback entrega.** O processo do daemon
  (pid 2430) **não tem** `DISPLAY` nem `WAYLAND_DISPLAY` em `/proc/2430/environ`,
  apesar do `ExecStartPre=-... import-environment`. Quem salva o dia é
  `_ensure_display_env` (`daemon/subsystems/autoswitch.py:25-61`): journal
  `16:50:41 autoswitch_display_env_imported var=DISPLAY`. **Se essa função
  morresse, o backend nasceria `null` e o perfil-por-jogo estaria morto a sessão
  inteira.**
- **As regras 82 e 83 chamam coisas que ainda não existem** (entram no passo 3, os
  scripts no 3e-bis) — e **sobrevivem à remoção delas**: o bloco que apaga os
  `bt_*.sh` **não** é gateado por `REMOVE_UDEV`, enquanto a remoção das regras é.
  `./uninstall.sh --keep-udev` deixa as duas regras disparando em toda conexão BT
  para caminho inexistente.
- **O initramfs só é regenerado quando vale**, comparando mtime do `.ko` contra a
  imagem (`scripts/dkms_lib.sh:209-215`), curando o bug de reescrever 141 MB em
  `/boot` a cada reexecução — e o critério é **auto-curativo**.
- **O aviso de Secure Boot existe porque a falha NÃO é fail-safe:** com SB
  enforcing e MOK não enrolada, o kernel **recusa** o `.ko` de `updates/dkms` e
  **não** cai no in-tree, porque o `modules.dep` aponta um caminho só.
- **O install é idempotente no `main.conf` do BlueZ por dois bugs pagos** (a linha
  vazia que empurrava o bloco uma linha por install — 10 acumuladas nesta máquina;
  e o backup só depois de `cmp -s` — 22 acumulados). **O uninstall não herdou
  nenhuma das duas curas:** cria até três backups numa só execução, sem comparar,
  e nunca limpa.
- **`--help` do install é truncado por `sed -n '2,128p'` e o cabeçalho tem 143
  linhas:** `--force-xwayland` fica invisível. Pior, `install.sh:1073` sugere
  `--disable-usb-audio`, flag que o parser **não conhece** e que faz o install
  abortar com código 2.
- **`purge.sh:37` só AVISA em argumento desconhecido e segue**, ao contrário de
  install e uninstall (que saem com 2, curado depois de `--help` ter desinstalado
  tudo). Num script de descontaminação, `--dry-runn` digitado errado vira execução
  real.
- **Os símbolos do formato native são todos PONTEIROS para o checkout git.**
  Mover ou renomear a pasta clonada mata daemon, atalho e launcher de uma vez, com
  a unit continuando "enabled".

### 6.13 ADRs, protocolos e sala limpa

- **O contrato escrito tem uma qualidade rara e um defeito estrutural, e os dois
  vêm da mesma prática:** quando o projeto descobre que errou, ele **emenda o
  documento no lugar** em vez de reescrever a história. Daí as notas de
  verificação datadas nos ADRs 003, 008 e 016, a Emenda que derrubou a parte 2 do
  ADR-018, e o ADR-019, que existe só para dizer que o critério de aceite do fix
  anterior mediu a coisa errada. **O defeito é que a varredura parou no meio em
  25/07:** os quatro documentos de `docs/protocol/` e os ADRs 001, 004, 005, 010,
  015 e 017 nunca foram conferidos.
- **Três documentos dão três caminhos diferentes para o mesmo socket, e o que erra
  é o canônico:** `docs/adr/010:7`, `docs/protocol/ipc-unix-socket.md:5` e
  `docs/usage/hotkeys.md:40`. **O terceiro é o que funciona** —
  `utils/xdg_paths.py:128`, com o subdiretório derivado, não digitado.
- **O gate construído para impedir que a documentação minta é arquitetonicamente
  cego ao exemplo canônico da mentira.** `scripts/validar-referencias-docs.py`
  nasceu da entrega 7 da DOC-VERDADE-01, e o próprio cabeçalho (`:20-26`) declara
  que ignora caminho de HOME e nome solto de configuração como `daemon.toml`. A
  frase falsa que **originou** a sprint é `docs/protocol/udp-schema.md:5`
  ("configurável em `~/.config/.../daemon.toml`"): cai nas **duas** isenções ao
  mesmo tempo. O gate roda na CI e nunca vai pegar aquilo.
- **O ADR-004 não apenas envelheceu: a unit em produção INVERTEU a justificativa
  dele.** O ADR decide `WantedBy=graphical-session.target` porque o daemon
  precisa "de acesso ao DISPLAY"; a unit é `WantedBy=default.target` e o
  comentário dela diz o oposto. **A inversão teve consequência:** foi preciso o
  `ExecStartPre` e o `_ensure_display_env()` de reforço para o autoswitch não
  nascer em NullBackend. O ADR-004 não está na lista de ninguém.
- **"19 modos" nomeia três conjuntos diferentes e o número coincidente esconde a
  lacuna.** Os 19 de `core/trigger_effects.py:361-381` incluem `Off` e `Custom`
  (escape hatch), logo são **17** efeitos; os "19 helpers do DSX" são outra lista;
  e 12 modos do DSX **não existem aqui**. `README.md:49` anuncia "19 modos" sem
  ressalva.
- **Colisão de nome que morde de verdade:** "Rigid" é ao mesmo tempo um modo HID
  legítimo do hardware da Sony (`core/trigger_effects.py:73`) e um dos doze modos
  prontos do DSX recusados por licença (`daemon/udp_server.py:151`). Um perfil com
  `"mode": "Rigid"` funciona; um mod DSX que peça Rigid falha. Mesma palavra, dois
  destinos — e o guarda proposto na CR-02, escrito como está, **reprovaria os dois**
  e também o "Medium" do exemplo da própria documentação.
- **O gate que protege o endereço Bluetooth dela não é o que se anuncia.**
  `check_anonymity.sh` só caça menção a provedores de IA e atribuição de autoria.
  Quem protege é um **teste**, `tests/unit/test_docs_mac_anonimato.py`, por lista
  de OUIs escrita à mão — e um MAC de `docs/process/sprints/2026-07-25-IDENT-01`
  usa um **quinto OUI** (`14:3a:9a`) ausente da lista. A proteção existe e tem um
  furo do tamanho de um prefixo.
- **A pesquisa de polling não sustenta a decisão que ela justifica:**
  `docs/adr/008` escolhe 60 Hz por "economia de CPU", e
  `docs/research/2026-04-20-polling-usb.csv` mostra a CPU **caindo** conforme a
  frequência sobe (9,1% a 60 Hz contra 4,7% a 1000 Hz). Nenhum documento comenta a
  inversão.
- **A sala limpa é a peça mais bem construída e a menos executada.** O NOTICE
  declara em voz alta que as curvas dos doze modos do DSX foram encontradas,
  avaliadas e **recusadas** por falta de licença, assume a consequência ("os doze
  modos prontos não funcionam no Hefesto") e aponta o caminho de substituição. Esse
  caminho não começou: `docs/protocol/curvas-proprias.md` continua vazio, CR-01 a
  CR-06 abertas, e Pesado/Macio/Trepidante não existem em `src/`. **Ficaram fora
  desta rodada por decisão dela.**
- **A convenção de commit é contrariada por 100% da prática recente:**
  `.github/CONTRIBUTING.md:99` exige "PT-BR acentuado" e dos últimos 30 assuntos
  **zero** tem acento. A causa está fora do repositório (o higienizador do fluxo de
  commit), e quem contribuir de fora vai seguir o CONTRIBUTING e ter o próprio
  texto alterado sem explicação.
- **`docs/research/` tem uma prática que vale copiar:** tabela de grau de certeza
  por afirmação (medido / inferido / hipótese / indeterminado) e a regra de método
  "medir a camada mais baixa primeiro custa um comando e economiza uma auditoria
  inteira na camada errada" — foi ela que refutou o relato de 25/07 com um
  `journalctl -k | grep -c idVendor=054c` devolvendo zero.

### 6.14 A periferia: plugins, métricas, glifos, diagnóstico

- **`plugin reload` NÃO PODE funcionar — nunca funcionou.**
  `PluginsSubsystem.reload` cria um loop novo e chama `run_until_complete`
  (`daemon/subsystems/plugins.py:273-277`), mas é invocado de dentro do loop que já
  roda. O CPython barra em `_check_running`: `RuntimeError('Cannot run the event
  loop while another loop is running')`. **Pior:** o `except Exception` genérico do
  `ipc_server` converte isso em erro de IPC e a CLI imprime "Daemon não acessível
  ou plugins não habilitados" — **a mensagem acusa exatamente o que não é o
  problema**. E `reload` limpa `self._entries` **antes** de tentar o start: o
  efeito colateral é ficar com zero plugins. Zero cobertura.
- **`profile_match` do plugin compara contra o NOME DE EXIBIÇÃO, não contra o slug
  que a própria API documenta.** Quem alimenta o parâmetro é
  `store.active_profile`, escrito com `profile.name` — o display name acentuado e
  com espaços. Um plugin que declare `profile_match=["navegacao"]` como manda a doc
  **nunca casa** o perfil chamado "Navegação". O teste não morde porque chama
  `ps.tick(active_profile="eldenring")` na mão.
- **"A primeira subclasse encontrada" é, de fato, a PRIMEIRA EM ORDEM ALFABÉTICA
  DE NOME DE CLASSE.** O loader usa `inspect.getmembers` (que ordena por nome) e
  depois `classes[0]`. **Este projeto já perdeu um dia com desempate por
  alfabeto** — a mesma armadilha está aqui, em código que carrega código de
  usuário. E `getmembers` enxerga classes **importadas**.
- **As métricas mentem em TRÊS das oito famílias, e o teste é verde porque fabrica
  a entrada.** Varridos os 34 `store.bump(...)` de `src/`: **`udp.accepted` não
  existe**, nenhuma chave começa com `ipc.` e nenhuma com `event.`. Logo três
  famílias ficam em 0 para sempre. E `tests/unit/test_metrics.py` injeta as três
  chaves à mão — **o teste prova o serializador e chama isso de provar a
  métrica.**
- **`server.allow_reuse_address = True` não faz nada:** é atribuído **depois** do
  construtor, e o atributo é consultado dentro do `__init__`. A intenção de
  SO_REUSEADDR está escrita e inerte, combinada com o único tratamento de falha
  ser "loga warning e vira no-op": **um TIME_WAIT na 9090 desliga as métricas em
  silêncio.**
- **O extra `metrics = ["prometheus-client>=0.19"]` instala uma dependência que o
  projeto NUNCA importa.** Extra morto que dá impressão de dependência.
- **As métricas não podem ser ligadas nem por `daemon.reload`:** `reload_config`
  (`daemon/lifecycle.py:947-973`) só reinicia o hotkey manager e reage a mudança de
  mouse e teclado. **Consequência lateral positiva:** `ps_long_press_ms` **sim** se
  aplica em runtime por esse caminho, porque o hotkey manager é reconstruído — só
  não persiste.
- **`novo-layout/` não está no repositório** (`.gitignore:108`) e **já foi
  consumido**: subtítulo, aba única "Navegação", tipografia e paleta estão no
  código vivo.
- **A logo divergiu do brief por um motivo que vale como regra geral:** o mockup
  usa `transform-origin`, que "navegadores honram e o **librsvg** — que é o
  renderizador do GTK — não", e o grupo do martelo ia parar fora do viewBox
  (`assets/hefesto-logo.svg:33-38`). **Mockup que renderiza no navegador não prova
  nada sobre o GTK.**
- **O literal `#bd93f9` dentro dos 19 `*_active.svg` é CONTRATO DE CÓDIGO, não
  decoração:** `_tintar_svg` troca esse literal exato pelo accent. Editar
  `FG_ATIVO` e regerar faz o tinting **silenciosamente parar de tintar**. Há
  guarda, e é um dos poucos testes desta área que realmente morde.
- **O `GLYPHS_DIR` é resolvido NO IMPORT do módulo, e o candidato de maior
  precedência é a cópia INSTALADA** (`~/.local/share/.../glyphs`). Editar um SVG na
  árvore de trabalho **não muda nada na janela** enquanto existir a cópia
  instalada. E `assets/glyphs` **não entra no wheel**: um `pip install` puro deixa
  `GLYPHS_DIR=None` e a janela sem glifo.
- **A unit `hefesto-dsx-recover.service` aponta para um documento que não existe**
  (`docs/process/sprints/FEAT-DSX-RECOVER-01.md`), <!-- ref-externa: a ausência deste arquivo É o assunto da frase -->
  e o portão de referências não vê
  porque varre **só markdown sob `docs/`**. Referência quebrada em `.service`,
  `.sh`, docstring de `.py` ou no `README.md` da raiz é invisível.
- **`captures/script_default.yaml` está órfão DUAS vezes:** o `ADR-008:14`
  documenta uma flag `--script` que o `parse_args` de hoje não aceita, e **PyYAML
  não está em nenhuma lista de dependências**.
- **`src/hefesto_dualsense4unix/testing/` NÃO é código de teste: é produção
  empacotada.** `FakeController` entra no wheel e é o backend que
  `build_controller` escolhe com `HEFESTO_DUALSENSE4UNIX_FAKE=1` — foi por isso
  que precisou existir o `BUG-FAKE-SOCKET-SYNC-01`: uma variável vazada fazia GUI,
  applet e CLI conversarem com um controle de mentira mostrando "Conectado Via
  USB" fantasma.
- **O plugin de exemplo pode desligar a si mesmo em hardware real:**
  `lightbar_rainbow.on_tick` chama `set_led` a ~60 Hz, e o watchdog desativa após
  3 lentidões acima de 5 ms. **Não medido em hardware** — registrado como risco
  plausível, não como fato.
- **O portão de glifos está VERDE hoje:** zero U+2B50, U+2705, U+274C e U+FE0F
  fora de `.git`/`.venv`. E a ordem das cláusulas em `e_proibido` é o coração do
  desenho — **preservação antes de proibição**, com teste que arranca a cláusula
  de propósito para provar que ela morde.
- **A ferramentaria de diagnóstico é a parte mais madura do repositório inteiro:**
  sete `bt_*.sh`, dois `storm_*.sh`, dois `medir_*.sh`, cada um com cabeçalho
  registrando a **medição que o justifica**, a premissa que caiu e o que ele
  deliberadamente **não** faz. Os `medir_*` são os mais raros: só medem, restauram
  o estado por trap EXIT e imprimem evidência — **a decisão fica para depois.**

---

## 7. Dois defeitos protegidos por teste-muralha

Este é o item mais acionável do estudo para quem for consertar, e vale antes de
qualquer linha ser tocada: **dois dos três defeitos relatados hoje estão travados
por teste. Curá-los REPROVA a suíte sem que nada esteja errado.**

| Defeito | O teste | O que ele exige |
|---|---|---|
| **3** — segurar o PS não vira modo jogo | `tests/unit/test_hotkey_ps_button.py:102` (`test_long_press_desligado_por_default`, bloco `:96-108`) | afirma que segurar 2 s **não dispara nada**, com o docstring citando FEAT-EMULATION-GAMEMODE-COMBO-01. Religar o gesto reprova |
| **1 e 2** — o backend cego no desktop | `tests/unit/test_window_detect_factory.py:123-137` (`TestDetectWindowBackendXWayland`, com `test_retorna_xlib_em_xwayland` em `:126` e `test_nao_usa_wayland_portal_em_xwayland` em `:132`) | duas classes cujo **único propósito** é exigir `XlibBackend` quando `DISPLAY` **e** `WAYLAND_DISPLAY` estão presentes — a configuração exata da sessão dela. Trocar a preferência para a cascata Wayland reprova |

Os dois testes estão **certos**: eles travam decisões deliberadas, com motivo
escrito. O que eles significam é que a cura não é "mudar o default" — é **mudar o
default e o teste na mesma leva, com o motivo novo escrito no lugar do antigo**.
Quem mexer num sem o outro vai achar que quebrou algo.

E há um terceiro caso, na aba Sistema:
`tests/unit/test_janela_sem_mentira.py:253` **bane a palavra "desfazer"** em texto
de ajuda de widget clicável, e a válvula de escape só procura a função inversa
dentro de `app/`. **Um tooltip honesto sobre o desfazer da allowlist quebra a
suíte** — a correção que passa hoje usa "desmarcar".

Vale registrar também o inverso, porque é a outra metade da mesma lição: há
**dois** lugares onde o defeito está protegido por um teste que **não** morde. O
`_pack_strengths_bits` (força 8 vira 0, `core/trigger_effects.py:347`) tem teste
que reproduz a máscara `& 0x7` no valor esperado. As três famílias de métrica que
ficam em zero têm teste que injeta as chaves inexistentes à mão. **Teste que
fabrica a entrada que a produção nunca produz é verde sobre código quebrado.**

---

## 8. O que este estudo NÃO mediu

Explícito, para ninguém tomar leitura por prova.

- **Nada foi executado.** Não rodou `pytest`, `install.sh`, `uninstall.sh`,
  `doctor.sh`, `run.sh` nem nenhum dos treze portões. Toda afirmação sobre gate
  ("existe", "está na CI") é leitura de configuração, **não prova de que ele passa
  hoje**. Em particular: não se sabe se `validar-referencias-docs.py --all` passa
  com os 92 arquivos de `docs/process` rastreados, nem se
  `check_packaging_parity.sh` passa.
- **A janela dela não foi aberta.** Nenhuma captura de tela, nenhum clique. As
  afirmações sobre o que a tela mostra vêm do `main.glade`, do código dos
  refreshers e do estado em disco. O aceite continua sendo o dela, pela regra da
  PROVA-DE-TELA-01.
- **`docs/history/` não foi cruzado item por item.** É documento declaradamente
  histórico: uma contradição ali pode ser registro correto de decisão superada —
  o oposto de defeito. Precisa de critério antes de varrer. Mesmo motivo que o
  índice de 27/07 já deu.
- **As CR-01 a CR-06 (sala limpa) ficaram fora por decisão dela**, no pedido
  literal *"estuda as próximas sprints sem ser as clean room"*. O que este estudo
  registra sobre elas é só o estado (todas abertas,
  `docs/protocol/curvas-proprias.md` vazio) e a dúvida de fronteira sobre "Rigid"
  e "Medium".
- **Quatro medições que só a máquina dela em uso responde, e que ninguém fez:**
  (a) quem detém o `EVIOCGRAB` do controle físico durante a exceção de Steam Input
  — a suspeita de que **nenhum atalho funciona dentro dos dois jogos dela** é
  circunstancial; (b) se `/proc/<pid>/exe` de um jogo Proton real produz um
  `exe_basename` que case com as listas `process_name` dos presets de gênero — se
  não casar, cinco dos seis presets com `mode: gamepad` são letra morta; (c) se o
  wrapper `hefesto-launch` está na Launch Option de **todos** os jogos dela, e não
  só do 2111190 que deixou marker hoje; (d) se o TypeError de
  `_reply_get_report`/`_reply_set_report` já aconteceu ou é teórico.
- **Não foi decidido nada.** Este documento não propõe entregas nem toca código.
  As ações listadas na seção 6.7 vieram do agente que leu a aba Sistema e estão
  registradas como leitura, não como plano aprovado.
- **A pergunta que fica, e não é de agente responder:** o cadeado
  `autoswitch_locked` foi ligado por ela em 28/07 18:18 de propósito, ou é resíduo
  do clique cego por coordenada daquele dia? O journal de 28/07 mostra o padrão
  que denuncia: `locked=False` às 18:16:01 e `locked=True` às 18:16:06;
  `locked=False` às 18:18:28 e `locked=True` às 18:18:33 — **desligado duas vezes
  e restaurado logo depois**. Desligar sem perguntar seria repetir o erro.

---

## 9. Onde cada achado virou trabalho

| Achado | Onde tem dono |
|---|---|
| O cadeado congela a troca de perfil; o modo jogo solta no alt-tab; o cadeado cede a preset casado por título | [PERFIL-JOGO-01](../sprints/2026-07-27-PERFIL-JOGO-01-o-modo-jogo-que-liga-e-solta.md) — faixa 1, **zero linhas entregues**, e a entrega ZERO (o experimento de cinco passos com ela abrindo o jogo) nunca foi executada |
| O detector só enxerga XWayland; `window_detect_seeing` existe e ninguém pergunta | JANELA-CEGA-01 (a "leva de uma linha" **não entrou**: `daemon/lifecycle.py:2952` ainda lê o trinco) + JANELA-CEGA-02, **sem documento** |
| Os dois cadastros de Steam Input divergem | [DUPLO-REGISTRO-01](../sprints/2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) — a cura R-D não entrou; o que segura hoje é o remendo de 26/07 |
| O desfazer da allowlist existe no CLI e a tela nega | STEAM-INPUT-01 (item 0 e "o desfazer dentro da janela") — e agora com a correção mínima medida: `gui/main.glade:2069`, verbo "desmarcar" |
| A aba Perfis não mostra que existe disputa de empate | EMPATE-01, entrega E2 — `app/actions/profiles_actions.py:139-146` ainda diz só "Sempre" |
| Handler órfão, botão que mentia, menos superfície | BOTÃO-QUE-NÃO-MENTE-01, entregas 5 e 6 — `on_emulation_open_toml` segue registrado em `app/app.py:320` |
| A documentação descreve outro programa (socket, ADRs, tabela de métodos) | DOC-VERDADE-01, as nove contradições — e três itens **foram curados de verdade** (gate de glifos existe, U+2B50 saiu, paridade entrou na CI) |
| Fontes nunca instaladas; unit órfã; gates que não rodavam | PROMESSA-NAO-CUMPRIDA-01 — A1/A3/A4 pagos; B1 (fontes) **vivo e verificável em um comando**: `grep -c fonts install.sh` = 0 |
| Um número único de contagem de controle; co-op derrubado sem aviso | CONTAGEM-E-COOP-01 — **sem documento** |
| **Segurar o PS: a janela promete o gesto que o default desliga** | **SEM DONO AINDA.** Não existe sprint sobre `ps_long_press_ms`; a única menção em `docs/process/` é um item de diagnóstico na BOTÃO-QUE-NÃO-MENTE-01:95. A queixa dela de hoje não está registrada em documento algum |
| **O vpad destruído e recriado três vezes em 31 s por alt-tab, e uma delas por um único tique cego** | **SEM DONO AINDA.** A decisão de usar leitura crua está escrita (`daemon/launch_env.py:433-438`); o preço não está registrado em sprint alguma. Melhor candidato mecânico para "na hora do jogo tá um caos" |
| **A cura do `--fix-mic` está fora da árvore que roda; a fonte padrão é o monitor do alto-falante** | **SEM DONO AINDA.** `84d9f4e` é ancestral de `main` e não de `HEAD`; `install.sh:2192` reaplica a cura refutada; `scripts/doctor.sh:438` dá pass |
| **A aba Sistema pode marcar o jogo errado por evidência sticky** | **SEM DONO AINDA.** `app/actions/daemon_actions.py:961` lê `window_detect_last_class`, que o próprio projeto veta como evidência em dois outros lugares |
| **O toast do Proton anuncia idempotência sobre uma recusa real** | **SEM DONO AINDA.** `integrations/proton_pin.py:837` |
| **`sensor_hub.py`: descoberta pesada sem timeout, `stop_all()` sem chamador, TTL que nunca expira por causa do tray** | **SEM DONO AINDA.** Nem o mapa de 27/07 nem o de 28/07 produziram um fato sobre este módulo |
| **`_pack_strengths_bits` faz força 8 virar 0, com teste tautológico** | **SEM DONO AINDA.** `core/trigger_effects.py:347` contra `:244` |
| **279 testes verdes contra GTK falso, fora do alcance da GUARDA-GI-REAL-01** | TESTE-QUE-MEDE-01, **sem documento** |
| **O hook de acentuação perde N-1 arquivos por commit** | **SEM DONO AINDA.** `scripts/validar-acentuacao.py:939` |
| **`.deb`: helper de ativação morto, DKMS não desregistrado, sem epoch** | **SEM DONO AINDA.** Parcialmente coberto por PACOTE-COM-NOME-01, **sem documento** |
| **Catálogos `.mo` três commits atrás dos `.po`, sem gate** | **SEM DONO AINDA.** A tradução do commit "a janela fala a língua dela" nunca chegou a nenhuma instalação |
| Código morto que importa limpo (`integrations/xlib_window.py`) | CODIGO-MORTO-01, **sem documento** |
| Os dezenove rótulos de gatilho com inglês entre parênteses | [GATILHO-PALAVRA-01](../sprints/2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md) — escrita em 29/07, **sem uma linha de código** |
| A largura da aba Status nas outras oito abas | [LARGURA-01](../sprints/2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) — idem |
| Alto-falante e sensores dentro do jogo | [SOM-02](../sprints/2026-07-29-SOM-02-o-alto-falante-que-funciona.md) e [SENSOR-VIVO-01](../sprints/2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md) — idem |
| As curvas próprias de gatilho | CR-01 a CR-06 — **fora de escopo por decisão dela** |

O índice vivo de tudo isso é
[o que falta depois da v0.3.0](../sprints/2026-07-29-INDICE-o-que-falta-depois-da-v030.md),
com a advertência que ele mesmo dá e que este estudo confirmou medindo: **o campo
`Status:` dos documentos não é fonte.**
