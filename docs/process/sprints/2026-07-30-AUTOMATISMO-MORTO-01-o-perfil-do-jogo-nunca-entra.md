# AUTOMATISMO-MORTO-01 — o perfil do jogo nunca entra

**Aberta em:** 2026-07-30, sobre a árvore `restauro/inicio-da-sessao` em `e74077c`
(tag `v0.4.0`, publicada hoje).

**Pedido dela:** "materializa as 3 faixas pra atacarmos depois de reiniciarmos".
Esta é a faixa do automatismo de perfil — a queixa crônica desta casa, escrita
por ela em 23/07 como *"a config que eu deixo nunca é respeitada"* e, em 26/07,
como *"o perfil muda ao abrir o jogo"*.

**Impacto:** o autoswitch de perfil está MORTO na máquina dela. Não "instável",
não "lento": morto. Em três dias de journal, com Pragmata aberto 30 vezes,
`profile_autoswitch` aparece **zero** vezes. Nenhuma troca automática de perfil
aconteceu. O modo jogo padrão liga (isso funciona), mas gatilhos, lightbar,
LEDs de jogador, política de vibração e co-op continuam sendo os do perfil que
por acaso estava ativo quando ela entrou no jogo.

---

## O que foi medido

Tudo abaixo foi medido hoje, 30/07, com o daemon dela vivo e a GUI aberta.
Leitura apenas: nada foi executado, nada foi reiniciado, nenhum arquivo de
configuração dela foi tocado.

### 1. O cadeado existe, está ligado, e está ligado desde 28/07

```
-rw-rw-r-- 1 vitoriamaria vitoriamaria 2 2026-07-28 18:18:33
  /home/vitoriamaria/.config/hefesto-dualsense4unix/autoswitch_locked.flag
conteúdo: "1\n"  (2 bytes)
```

O conteúdo é irrelevante por contrato: quem lê é
`utils/session.py:195` (`load_autoswitch_locked`), e ele responde
`(config_dir() / "autoswitch_locked.flag").exists()` — **existir é estar
travado**, o mesmo idioma do `paused.flag` (`utils/session.py:198`). Escrever
`0` dentro do arquivo não destrava nada; só apagar o arquivo destrava
(`utils/session.py:189`).

O cadeado é consultado em **um único ponto** do tick:
`profiles/autoswitch.py:252` — `if self.travado():`. O predicado
`travado()` está em `profiles/autoswitch.py:165-189` e só lê
`store.autoswitch_locked`; nenhuma política mora nele.

E ele cede por **duas portas**, ambas avaliadas em
`profiles/autoswitch.py:259-262`:

- **Porta 1 — `perfil_e_regra_de_jogo(profile, info)`**
  (`profiles/schema.py:602-642`). Exige as duas coisas juntas: o `match` ser
  `MatchCriteria` com `window_class` **preenchido** (`schema.py:633`) e a
  `wm_class` em foco começar por `steam_app_` **e estar listada** naquele
  `window_class` (`schema.py:636-642`). Regex de título não conta, de
  propósito (`schema.py:620-624`).
- **Porta 2 — `perfil_declara_modo_de_jogo(profile)`**
  (`profiles/schema.py:666-702`). Exige que o perfil **não seja catch-all**
  (`schema.py:699-700`) **e** declare `mode.kind` em `{gamepad, native}`
  (`schema.py:701-702`).

As duas portas recebem o perfil **candidato**. Se o candidato for `None`, as
duas respondem `False` — `perfil_declara_modo_de_jogo` explicitamente
(`schema.py:697-698`), e `perfil_e_regra_de_jogo` porque
`getattr(None, "match", None)` não é `MatchCriteria` (`schema.py:632-634`).
Guarde isto: é o nó do defeito.

Posição do cadeado no tick, também medida: ele está **depois** do select
(`autoswitch.py:230`) e **depois** do modo jogo padrão (`autoswitch.py:237`).
Isso foi deliberado na MODO-01/B2 e continua certo — é por isso que o modo
jogo ainda liga com o cadeado fechado.

### 2. Os perfis dela — a tabela

Quinze arquivos em `~/.config/hefesto-dualsense4unix/profiles/`. "Catch-all"
é o predicado `Profile.e_catch_all` (`profiles/schema.py:569-599`): `MatchAny`,
ou `MatchCriteria` com os três campos vazios.

| arquivo | nome | tipo de match | prioridade | tem `mode`? | catch-all? | origem |
|---|---|---|---|---|---|---|
| `fallback.json` | fallback | `any` | 0 | não | **SIM** | preset |
| `vitoria.json` | vitoria | `any` | 0 | gamepad/dualsense/co-op | **SIM** | **dela** |
| `meu_perfil.json` | meu_perfil | `any` | 1 | `null` | **SIM** | preset semeado |
| `pragmata.json` | Pragmata | `any` | 5 | `null` | **SIM** | **dela** |
| `pragmata2.json` | Pragmata2 | `any` | 5 | `null` | **SIM** | **dela** (ativo) |
| `bow.json` | bow | criteria (só regex de título) | 10 | não | não | preset |
| `navegacao.json` | Navegação | criteria (`window_class`, 12 entradas) | 50 | `null` | não | preset editado |
| `corrida.json` | Corrida | criteria (regex + processo) | 55 | gamepad/xbox | não | preset |
| `esportes.json` | Esportes | criteria (regex + processo) | 55 | gamepad/xbox | não | preset |
| `fps.json` | FPS | criteria (regex + processo) | 60 | gamepad/xbox | não | preset |
| `point_and_click.json` | point_and_click | criteria (`window_class`: GrimFandango) | 60 | não | não | preset |
| `acao.json` | Ação | criteria (regex + processo) | 65 | gamepad/xbox | não | preset |
| `aventura.json` | Aventura | criteria (regex + processo) | 70 | gamepad/xbox | não | preset |
| `coop_local.json` | coop_local | criteria (só regex de título) | 75 | gamepad/xbox/co-op | não | preset |
| `sackboy_nativo.json` | sackboy_nativo | criteria (`window_class`: `steam_app_1599660`) | 80 | gamepad/dualsense/co-op | não | preset |

Correção honesta ao enunciado da faixa: **não são todos catch-all**. São
catch-all exatamente cinco — e os cinco são os que importam, porque são os
únicos que casam dentro do jogo (provado no item 3) e porque **quatro dos cinco
foram feitos por ela** (`vitoria`, `Pragmata`, `Pragmata2`, e o `meu_perfil`
que ela editou). Os presets específicos são todos de fábrica.

O detalhe que dói: `pragmata.json` e `pragmata2.json` são os perfis que ela
criou **para o Pragmata**, e são `"match": {"type": "any"}`, prioridade 5.
Um perfil chamado Pragmata que não sabe o que é o Pragmata.

**Um único perfil no disco dela consegue abrir a Porta 1 do cadeado:**
`sackboy_nativo.json` (`window_class: ["steam_app_1599660"]`). Nenhum outro
perfil tem `steam_app_*` em `window_class`. E ela não está jogando Sackboy.

### 3. O veto R-21 — por que o candidato sai VAZIO dentro do jogo

O veto está em `profiles/manager.py:620-628`, dentro de
`select_for_window_ex`:

```python
if e_janela_de_jogo and all(p.e_catch_all for p in candidates):
    ...
    return None, MOTIVO_JOGO_SEM_PERFIL_PROPRIO
```

`e_janela_de_jogo` vem de `_STEAM_APP_WM_CLASS_RE`
(`manager.py:43`, `^steam_app_\d+$`, case-insensitive) aplicado à `wm_class`
em foco (`manager.py:615`). `MOTIVO_JOGO_SEM_PERFIL_PROPRIO` está em
`manager.py:62`.

A doutrina (documentada em `manager.py:588-611`): um genérico de **desktop**
não tem autoridade sobre uma janela de **jogo**. Se os únicos candidatos são
catch-all, a resposta honesta é `None` — "nenhum perfil opina sobre este jogo"
— e o autoswitch retém o perfil corrente em vez de trocar. O veto tem razão
própria: sem ele volta o ping-pong de 18-28 s do journal de 22-23/07, com
lightbar e gatilhos mudando no meio da partida.

Com os perfis dela, dentro do jogo, os candidatos são **exatamente os cinco
catch-all** — o journal diz o nome de cada um:

```
2026-07-30T00:41:30 profile_select_catch_all_sem_autoridade_em_jogo
  candidatos=['Pragmata', 'Pragmata2', 'fallback', 'meu_perfil', 'vitoria']
  wm_class=steam_app_3357650
```

Logo `all(p.e_catch_all)` é verdadeiro, o veto dispara, e `select_for_window_ex`
devolve `(None, MOTIVO_JOGO_SEM_PERFIL_PROPRIO)`.

### 4. O journal — as contagens

`journalctl --user --since "3 days ago"` (27/07 23:02 até 30/07 13:52):

| evento | ocorrências |
|---|---|
| `profile_autoswitch` (troca efetiva de perfil) | **0** |
| `autoswitch_cadeado_cedeu_a_regra_de_jogo` | **0** |
| `profile_select_catch_all_sem_autoridade_em_jogo` (veto R-21) | **34** |
| `autoswitch_congelado_pelo_cadeado` | **32** |
| `x11_focus_gate_no_x_focus` | **135** |
| `autoswitch_window_info_unavailable` | 50 |
| `autoswitch_janela_propria_ignorada` | 7 |

Os dois eventos-chave, quebrados:

**Veto R-21, 34 vezes, sempre em janela de jogo** — 30 em
`steam_app_3357650` (Pragmata, confirmado por
`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`), 2 em
`steam_app_2111190` (Mullet Mad Jack, mesmo arquivo), 2 em
`steam_app_1553260`. Sempre a mesma lista de candidatos catch-all.

**Cadeado, 32 vezes, em DOIS formatos distintos** — e a diferença entre eles
é o achado desta sprint:

```
18x  autoswitch_congelado_pelo_cadeado candidate=Navegação current= wm_class=steam
14x  autoswitch_congelado_pelo_cadeado candidate=          current= wm_class=steam_app_XXXXXXX
```

Exemplos crus, com hora:

```
2026-07-30T13:04:36 ... candidate=Navegação current= wm_class=steam
2026-07-29T22:39:10 ... candidate=          current= wm_class=steam_app_3357650
2026-07-29T17:49:55 ... candidate=          current= wm_class=steam_app_2111190
2026-07-29T16:55:25 ... candidate=          current= wm_class=steam_app_1553260
```

O `current=` vazio em todas as 32 linhas tem significado próprio:
`_current_profile` (`autoswitch.py:111`) só é preenchido em `_activate`
(`autoswitch.py:551`). Vazio em todo o journal = **o autoswitch nunca ativou
perfil nenhum nesta instalação, em três dias**.

### 5. O detector ENXERGA o jogo — e o backend é o xlib

```
2026-07-30T13:04:15 window_detect_diag_seeded backend=xlib healthy=True
```

Três semeaduras no período, todas `backend=xlib healthy=True`
(`daemon/subsystems/autoswitch.py:99-108`). E as 40 linhas de journal com
`wm_class=steam_app_3357650` / `steam_app_2111190` / `steam_app_1553260`
provam que a leitura de janela de jogo funciona. Está na seção "O que NÃO é a
causa", com a medição inteira.

### 6. O furo do `window_detect_last_class` (sticky) segue aberto

`daemon/state_store.py:317` define útil como `bool(wm_class) and wm_class !=
"unknown"`, e `state_store.py:326` grava **qualquer** classe útil em
`_window_detect_last_class`. A gravação acontece em
`daemon/subsystems/autoswitch.py:144` (`store.record_window_detect_read`),
dentro do wrapper `_read` — que roda **antes** de `_tick`
(`profiles/autoswitch.py:153` chama o reader, `:158` chama o tick). O filtro
de janela própria (`_janela_propria`, `profiles/autoswitch.py:438-449`, com
`OWN_GUI_WM_CLASSES` em `:71-78`) mora **dentro** do `_tick`, tarde demais
para proteger o campo.

Consequência medida: focar a janela do Hefesto grava
`Hefesto-Dualsense4Unix` no sticky. O journal registra 7 episódios de
`autoswitch_janela_propria_ignorada`, e às 13:23:54 de hoje uma seleção
carregando `wm_class=Hefesto-Dualsense4Unix`.

Quem consome o sticky são justamente os caminhos de "nascer com o jogo":
`app/actions/profiles_actions.py:726` (prefill do appid) e
`app/actions/profiles_actions.py:862` (`_aplicar_nascimento_com_jogo`,
PERFIL-NASCE-CERTO-01), mais `app/actions/launch_wrapper_dialog.py:135` e
`daemon/ipc_handlers.py:2280`. Para clicar em "Novo perfil" ela precisa focar
o Hefesto — e nesse instante o campo deixa de apontar para o jogo.

Existe ao lado o carimbo `_game_window_seen_at` (`state_store.py:130`,
gravado em `state_store.py:331-334` só quando a classe casa `steam_app_\d+`),
mas ele guarda **o instante**, não **a classe**. O campo que faltava não
existe.

### 7. O rodapé ainda cria perfil catch-all

`app/draft_config.py:495-498`: com nome NOVO, `to_profile` monta
`MatchAny()` deliberadamente, porque o diálogo do rodapé não tem campo de
regra. A prioridade foi curada em 30/07
(`app/actions/footer_actions.py:283-315`, calculada por
`_prioridade_acima_dos_catch_all`, `profiles_actions.py:1425-1439`, hoje =
15). Mas prioridade alta num perfil **catch-all** não vence o veto R-21:
o veto olha `e_catch_all`, não `priority`. Este é o caminho que produziu
`pragmata.json` e `pragmata2.json`.

---

## A causa

São duas, e elas se somam em lugares **diferentes** da tela. A confusão de
tratá-las como uma só é o que fez esta faixa sobreviver a três sessões.

### Causa A — dentro do jogo: o veto R-21, sozinho, já basta

Sequência real de um tick com Pragmata em foco (`wm_class=steam_app_3357650`):

1. `autoswitch.py:230` — `_selecionar_com_motivo` devolve
   `(None, MOTIVO_JOGO_SEM_PERFIL_PROPRIO)`, pelo veto de `manager.py:620-628`.
   **`candidate = None`** (`autoswitch.py:231`).
2. `autoswitch.py:237` — `_sincronizar_modo_jogo_padrao` liga o modo jogo
   padrão. **Isto funciona** e é o que aparece no journal como
   `profile_mode_aplicado ... origin=game_signal`.
3. `autoswitch.py:252` — `travado()` é True. Com `profile = None`, as duas
   portas respondem False (`schema.py:632-634` e `schema.py:697-698`), e o
   tick loga `autoswitch_congelado_pelo_cadeado candidate=` e retorna.

O passo 3 é **redundante**. Mesmo com o cadeado apagado, a linha
`autoswitch.py:304` é `if stable and candidate and candidate != self._current_profile:`
— e `candidate` é `None`. Nada ativaria. Destravar não muda uma vírgula do
comportamento dentro do jogo.

**Dentro do jogo, o culpado é só o veto R-21 — porque os perfis dela são
catch-all.** As 14 linhas de `congelado ... candidate= wm_class=steam_app_*`
são um efeito colateral do log, não a causa.

### Causa B — no desktop: o cadeado é o único freio

Sequência com a janela da Steam em foco (`wm_class=steam`):

1. `navegacao.json` casa: `window_class` contém `"steam"` e `"Steam"`,
   prioridade 50, e ele **não é catch-all** (`window_class` preenchido).
   Como não é janela de jogo, o veto R-21 não se aplica.
   **`candidate = "Navegação"`.**
2. `travado()` é True. Porta 1: `wm_class` é `steam`, não `steam_app_*` →
   False (`schema.py:636-637`). Porta 2: `Navegação` tem `"mode": null` →
   `kind` é `None` → False (`schema.py:701-702`).
3. Congela. 18 vezes em três dias.

Ou seja: **o cadeado é a única coisa que impede o perfil de Navegação de entrar
por cima da configuração dela toda vez que ela abre a Steam.** Ele não está
atrapalhando o jogo; ele está segurando o desktop.

### O somatório

Dentro do jogo, nada entra porque nenhum perfil dela tem autoridade. Fora do
jogo, nada entra porque o cadeado (corretamente) segura o genérico. Resultado:
`profile_autoswitch` = 0. O automatismo não está quebrado em um ponto — ele
está sem caminho por onde passar, nos dois estados.

E a raiz comum das duas é uma só: **não existe, na interface, um caminho pelo
qual o perfil dela vire a regra do jogo.** O único perfil do disco que abriria
a Porta 1 é um preset de fábrica (`sackboy_nativo`), escrito por nós.

---

## O que NÃO é a causa

### ▲ NÃO é o detector de janela — ele enxerga o jogo

Esta sessão REFUTOU a hipótese com que a faixa começou. O backend `xlib` lê
janela de jogo sob XWayland, e a prova é direta:

```
2026-07-30T13:04:15 window_detect_diag_seeded backend=xlib healthy=True
```

e 40 linhas de journal em três dias carregando `wm_class=steam_app_3357650`,
`steam_app_2111190` e `steam_app_1553260` — os appids do Pragmata e do Mullet
Mad Jack, conferidos contra
`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`. Se o detector fosse
cego no jogo, o veto R-21 nem teria como disparar: ele só dispara quando a
`wm_class` casa `^steam_app_\d+$` (`manager.py:43` e `:615`). As 34
ocorrências do veto **são** a prova de que o detector enxerga.

O detector é cego em outro lugar: no **desktop Wayland nativo**. As 135
linhas de `x11_focus_gate_no_x_focus focus=0` vêm de
`integrations/window_backends/xlib.py:276` — o gate de foco recusa a leitura
quando o `get_input_focus()` do X devolve `X.NONE`/`PointerRoot`, que é o que
acontece quando a janela em foco é Wayland nativa (COSMIC, GTK4, aplicativos
do sistema). Isso vira `autoswitch_window_info_unavailable` (50 episódios) e a
histerese UX-01 (`autoswitch.py:198-225`) retém o perfil corrente. É o
comportamento correto e não tem nada a ver com esta faixa.

**Não gaste a próxima leva no detector.** Ele funciona exatamente onde
precisa funcionar.

### ▲ NÃO é desligar o cadeado

Medido: `navegacao.json` tem `"steam"` e `"Steam"` em `window_class`,
prioridade 50, `"mode": null`. Com o cadeado apagado, cada alt-tab para a
Steam ativa **Navegação** — que reescreve gatilhos (`Pulse`/`Pulse`), lightbar
(`[40, 80, 180]`, brilho 0.4), LEDs de jogador, e ainda carrega overrides
por-MAC para dois controles dela (`143a9a13ebab` e `a0fa9cc311f0`). É
literalmente "a config que eu deixo nunca é respeitada", agora automatizado.

O journal mostra que isso aconteceria **18 vezes em três dias**, e a última
seria hoje às 13:04:36.

E, como já dito na Causa A, destravar **não conserta o jogo**: com
`candidate = None`, `autoswitch.py:304` barra a ativação de qualquer jeito.
Destravar tem custo alto e benefício zero.

### ▲ NÃO é a prioridade

Refutado em 27/07 e reconfirmado hoje no código: `_chave_de_selecao`
(`manager.py:632-640`) devolve `(not profile.e_catch_all, profile.priority)` —
**especificidade vem antes de prioridade**. E o veto R-21 (`manager.py:620`)
testa `e_catch_all`, sem olhar `priority` uma única vez. Subir `Pragmata2` de
5 para 200 não muda absolutamente nada dentro do jogo.

Isto também derruba meia cura: a prioridade calculada que a v0.4.0 entregou no
rodapé (`footer_actions.py:283-315`) é necessária, mas sozinha não resolve —
ela conserta o empate entre catch-all, não a falta de autoridade.

### ▲ NÃO é o modo jogo padrão

Ele funciona. `profile_mode_aplicado ... flavor=dualsense kind=gamepad
origin=game_signal wm_class=steam_app_3357650` aparece no journal (29/07 às
18:53:01 e 22:39:11). A MODO-01/B3 entregou o que prometeu: o cadeado está
antes do modo de propósito (`autoswitch.py:234-237`). O que falta é tudo o
que **não** é modo — gatilhos, LEDs, cor, política de vibração, co-op.

---

## As entregas

Critério de aceite da faixa inteira, e ele é único:
**a dona não pode precisar saber o que é "prioridade" ou "catch-all" para o
perfil do jogo dela valer no jogo.** Uma entrega que exija dela entender a
tabela da seção 2 está reprovada por construção.

### E0 — a janela diz POR QUE o perfil não trocou

**O que faz.** Hoje o motivo da não-troca só existe no journal. `manager.py`
já calcula `MOTIVO_JOGO_SEM_PERFIL_PROPRIO` / `MOTIVO_SEM_CANDIDATO` /
`MOTIVO_SELECIONADO` (`manager.py:60-62`) e o autoswitch já os recebe
(`autoswitch.py:230`) — e **nenhum deles chega ao IPC**: medido, não há
nenhuma ocorrência de `motivo` em `daemon/ipc_handlers.py`. Esta entrega
carimba no `StateStore` o último motivo, a última `wm_class` julgada e o
último candidato, publica os três no `daemon.state_full`, e a aba Início
mostra uma frase.

Frases, decididas aqui para não sobrarem para o implementador:

- veto: *"O jogo em foco não tem perfil próprio — nenhum dos seus perfis vale
  só para ele. O perfil «Pragmata2» continua valendo."*
- cadeado no desktop: *"Cadeado ligado: «Navegação» combinaria com esta
  janela, mas o perfil não troca sozinho."* (o texto de
  `home_actions.py:131-152` já existe e cobre metade disso — falta dizer QUEM
  ficou de fora)
- detector cego: reaproveitar a linha da aba Sistema
  (`daemon_actions.py:126-160`), que já sabe dizer `window_detect_seeing` e
  `window_detect_reason`.

**Arquivos.** `daemon/state_store.py` (três campos + property, ao lado de
`_window_detect_*`, linhas 111-137), `profiles/autoswitch.py` (carimbar logo
depois de `:230`), `daemon/ipc_handlers.py` (bloco do `state_full`, junto de
`:1276-1298`), `app/actions/home_actions.py` (frase, junto de
`autoswitch_lock_text`, `:131`).

**Como PROVAR com teste que morde.** Teste de ponta a ponta sem GUI: monta
`ProfileManager` com os cinco catch-all dela em `tmp_path`, roda um `_tick`
com `{"wm_class": "steam_app_3357650"}`, e afirma que
`store.autoswitch_ultimo_motivo == MOTIVO_JOGO_SEM_PERFIL_PROPRIO` e que a
função pura da frase devolve texto contendo "não tem perfil próprio".
**Arrancar a cura**: remover a linha de carimbo em `autoswitch.py` tem de
deixar o teste VERMELHO — se ele passar sem o carimbo, ele testa o dublê.

**Risco.** Baixo, e é o único aqui que não muda comportamento nenhum. Duas
armadilhas conhecidas desta casa: (a) o carimbo roda a 2 Hz, então tem de ser
escrita simples sob o `_lock`, sem I/O — o mesmo cuidado de
`record_window_detect_read`; (b) a frase da aba Início tem de nascer dentro de
`try` e não pode importar `ipc_bridge` no topo, porque foi exatamente isso que
derrubou três testes no CI headless em `a49b687`.

### E1 — o campo próprio da janela de jogo (fecha o furo do sticky)

**O que faz.** Cria `_game_window_last_class` no `StateStore`, ao lado do
`_game_window_seen_at` que já existe (`state_store.py:130`), gravado **no
mesmo `if`** que já carimba o `seen_at` (`state_store.py:331-334`) — ou seja,
só quando a classe casa `steam_app_\d+`. Publica como
`game_window_last_class` no `state_full`. Os consumidores de "qual jogo está
em foco" passam a ler este campo, com fallback para o sticky antigo.

**Por que é entrega separada.** O sticky
(`_window_detect_last_class`, `state_store.py:119`) é usado hoje para outra
coisa — diagnóstico de detector, e capturar a última classe ÚTIL qualquer que
seja. Mudar a semântica dele quebraria a aba Sistema. O campo novo é aditivo:
o sticky continua sticky, e o jogo ganha um campo que só o jogo escreve.

**Decisão sobre decaimento:** o campo **não decai**, igual ao sticky. Quem
precisa de idade já tem `game_window_seen_at` (`state_store.py:509-518`), e o
`game_signal` continua consumindo o campo CRU
(`_window_detect_current_class`), como manda o veto documentado em
`state_store.py:120-127`. Consumidor que queira "só se recente" combina os
dois — a classe daqui, a idade de lá.

**Arquivos.** `daemon/state_store.py:130` e `:331-334` e uma property nova
perto de `:509`; `daemon/ipc_handlers.py:1276-1298`;
`app/actions/profiles_actions.py:726` e `:862`;
`app/actions/launch_wrapper_dialog.py:135`; `daemon/ipc_handlers.py:2280`.

**Como PROVAR com teste que morde.** Sequência exata do defeito, sem GUI:
`record_window_detect_read("xlib", "steam_app_3357650")`, depois
`record_window_detect_read("xlib", "Hefesto-Dualsense4Unix")`. Afirmar que
`window_detect_last_class == "Hefesto-Dualsense4Unix"` (o sticky continua
sticky, e é o comportamento que a aba Sistema depende) **e** que
`game_window_last_class == "steam_app_3357650"`. Segundo teste, sobre a GUI:
`_aplicar_nascimento_com_jogo({"window_detect_last_class":
"Hefesto-Dualsense4Unix", "game_window_last_class": "steam_app_3357650"})`
tem de devolver `True` e escrever `3357650` no campo. **Arrancar a cura**:
com a leitura do campo novo revertida para o sticky, os dois testes têm de
ficar VERMELHOS.

**Risco.** Baixo-médio. O risco real é o **stale**: um jogo fechado há duas
horas ainda responde. Mitigação decidida: quem oferece um gesto destrutivo
(E2) exige `game_window_seen_at` recente; quem só pré-preenche um campo
editável (E1 nos prefills existentes) aceita o valor sem prazo, porque
pré-preencher errado um campo que ela vê e pode corrigir é barato.

### E2 — UM CLIQUE: "fazer este perfil valer neste jogo"

**Esta é a entrega que resolve a faixa.** As outras são o caminho até ela.

**O que faz.** Um botão único, visível quando há jogo em foco, que pega o
perfil ATIVO e o reescreve como regra específica daquele jogo:

- `match` vira `MatchCriteria(window_class=["steam_app_<id>"])`;
- `priority` vira `_prioridade_acima_dos_catch_all()`
  (`profiles_actions.py:1425-1439` — hoje 15 no disco dela);
- `mode` vira coerente: se o perfil não declara modo (`Pragmata2` tem
  `"mode": null`), preenche com o modo VIVO do daemon — `kind: gamepad` e o
  flavor de `gamepad_emulation.flag` (hoje `dualsense`), pelo
  `normalizar_gamepad_flavor` (`schema.py:645-663`). Se ela já declarou modo,
  preserva.

O efeito é duplo e exato:
o perfil deixa de ser catch-all, então **o veto R-21 não dispara mais** para
aquele jogo (`manager.py:620` testa `all(p.e_catch_all)`); e ele passa a
satisfazer `perfil_e_regra_de_jogo` (`schema.py:633-642`), então **o cadeado
cede pela Porta 1** — sem que ela precise destravar nada, e sem que Navegação
ganhe autoridade nenhuma no desktop.

**O texto do botão importa tanto quanto o código.** Nada de "prioridade",
"catch-all", "match". A proposta:
*"Usar este perfil sempre neste jogo"*, e o toast de confirmação
*"«Pragmata2» agora vale sempre que você abrir este jogo."* Se o nome do jogo
estiver disponível, usar o nome; se só houver o número, usar
*"neste jogo (número 3357650)"*, como já faz `profiles_actions.py:877-880`.

**Onde fica.** Dois lugares, mesmo handler: o rodapé (que é onde ela está
quando joga — o rodapé já tem "Salvar Perfil" e já sabe o nome do perfil ativo,
`footer_actions.py:321`) e a aba Perfis, ao lado de "Ativar".

**Guardas obrigatórias** (aprendidas em `_aplicar_nascimento_com_jogo`,
`profiles_actions.py:842-851`):

- só age com `game_window_last_class` presente **e**
  `game_window_seen_at` com idade abaixo de um teto — aqui o gesto **é**
  destrutivo (reescreve o `match` de um perfil que existe), então stale não
  serve;
- se o perfil ativo já tem `window_class` com aquele `steam_app_<id>`, o botão
  fica desabilitado com a frase *"Já vale neste jogo"* — em vez de reescrever
  à toa;
- se o perfil ativo é um **preset de fábrica** (está em
  `profiles/.seeded_presets`), oferecer duplicar em vez de reescrever: mexer
  no `sackboy_nativo` dela por engano seria perder um preset;
- escrita atômica pelo `save_profile` de sempre, respeitando o `.lock` que
  todo perfil dela já tem.

**Arquivos.** `app/actions/footer_actions.py` (botão + handler, perto de
`:283`), `app/actions/profiles_actions.py` (botão gêmeo e reuso de
`_prioridade_acima_dos_catch_all`), `src/hefesto_dualsense4unix/gui/main.glade`
(os dois botões), e uma função PURA nova — `regra_de_jogo_para(profile,
wm_class, flavor) -> Profile` — em `profiles/schema.py` ou num módulo
`profiles/promocao.py`, para ser testável sem GTK.  <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

**Como PROVAR com teste que morde.** Três testes, e o terceiro é o que morde
de verdade:

1. **Puro**: `regra_de_jogo_para(Profile(match=MatchAny(), priority=5,
   mode=None), "steam_app_3357650", "dualsense")` devolve um perfil com
   `match.window_class == ["steam_app_3357650"]`, `priority == 15`,
   `mode.kind == "gamepad"`, `mode.gamepad_flavor == "dualsense"`, e com
   gatilhos/LEDs/rumble **byte-idênticos** ao original.
2. **Predicados**: sobre o perfil promovido,
   `perfil_e_regra_de_jogo(p, {"wm_class": "steam_app_3357650"})` é True e
   `p.e_catch_all` é False.
3. **Integração, reproduzindo o disco dela**: escrever em `tmp_path` os cinco
   catch-all reais (`fallback` 0, `vitoria` 0, `meu_perfil` 1, `Pragmata` 5,
   `Pragmata2` 5), afirmar que `select_for_window_ex({"wm_class":
   "steam_app_3357650"})` devolve `(None, MOTIVO_JOGO_SEM_PERFIL_PROPRIO)`;
   promover o `Pragmata2`; afirmar que agora devolve
   `(Pragmata2, MOTIVO_SELECIONADO)`; e rodar um `_tick` do `AutoSwitcher`
   **com `store.autoswitch_locked = True`** afirmando que
   `profile_autoswitch` acontece — isto é, que o cadeado cedeu pela Porta 1
   com a flag ainda ligada.

**Arrancar a cura**: reverter só a linha que preenche `window_class` (deixando
prioridade e modo) tem de deixar o teste 3 VERMELHO. Se ele passar, é porque
está medindo prioridade — e prioridade não é a cura (ver "O que NÃO é a
causa").

**Risco.** Médio, e é o único aqui que reescreve um perfil dela. Três
mitigações: (a) as guardas acima; (b) o gesto é explícito e nomeado — não é
automático, não roda no tick, não roda no boot; (c) **um backup do `.json`
antes de reescrever**, no mesmo idioma do
`profiles/backup-20260726-233630/` que já existe no disco dela. Esta casa já
levou um rollback por mexer em configuração; um arquivo a mais é barato.

### E3 — o rodapé para de criar perfil catch-all quando há jogo em foco

**O que faz.** Hoje, "Salvar Perfil" com nome NOVO monta `MatchAny()`
(`draft_config.py:495-498`) — foi assim que `pragmata.json` e
`pragmata2.json` nasceram sem saber o que é o Pragmata. Com `E1` no lugar, o
rodapé passa a fazer o que a aba Perfis já faz em
`_aplicar_nascimento_com_jogo` (`profiles_actions.py:830-884`): com jogo em
foco, o perfil nasce com `window_class: [steam_app_<id>]`, prioridade acima
dos catch-all, e o toast dizendo em português o que aconteceu.

Sem jogo em foco, nada muda — perfil de desktop deve mesmo nascer catch-all.

**Por que depois do E2, e não antes.** E3 só serve para perfis **futuros**.
E2 conserta o perfil que ela **já tem ativo agora** (`Pragmata2`). A queixa é
sobre o perfil que existe.

**Arquivos.** `app/draft_config.py:421-500` (aceitar um `match` do chamador,
sem mudar o default), `app/actions/footer_actions.py:283-315`.

**Como PROVAR com teste que morde.** Estender
`tests/unit/test_footer_salvar_nasce_acima_dos_catch_all.py` (já existe): com
`game_window_last_class = "steam_app_3357650"`, salvar "MadJack" produz
`match.window_class == ["steam_app_3357650"]`; **sem** jogo em foco, produz
`MatchAny` — os dois lados, senão a cura vira regressão para perfil de
desktop. **Arrancar a cura**: o teste sem jogo em foco tem de continuar verde
e o teste com jogo tem de ficar vermelho ao reverter.

**Risco.** Baixo-médio. A armadilha conhecida está documentada em
`draft_config.py:484-498` (R-11): reemitir `match` do perfil de ORIGEM com
nome novo é um defeito já medido — "Salvar Perfil como MadJack" com o FPS
ativo produzia o regex de título do FPS. A regra segue: com nome novo, o
`match` vem **da janela em foco ou de `MatchAny`**, nunca do perfil de origem.

### E4 — migrar os perfis dela ▲ ESPERA A PALAVRA DELA

**O que faz.** Reescreveria `pragmata.json` e `pragmata2.json` com
`window_class: ["steam_app_3357650"]` e prioridade acima dos catch-all, e
possivelmente reduziria os cinco catch-all a um só.

**Por que está aqui e não está pronta.** Isto mexe em **arquivo de
configuração dela**, e desfazer código não desfaz configuração. Esta casa já
levou um rollback exatamente por isso (26/07, madrugada). Nenhuma linha desta
entrega é escrita antes de ela dizer, com todas as letras, quais arquivos
podem ser reescritos.

O que **pode** ser feito sem autorização: mostrar a ela o que a migração faria.
Uma lista de "estes perfis nunca vão valer no jogo, e por quê", com um botão
por linha que executa o E2 sobre aquele perfil. Um clique por perfil, decidido
por ela, é migração com consentimento — e não precisa de entrega nova, é o E2
aplicado a uma lista.

**Como PROVAR.** Não se prova em teste automatizado: prova-se na tela dela,
com o jogo aberto, e com o `git diff` do diretório de perfis mostrado antes de
qualquer escrita.

**Risco.** Alto por natureza. Fica congelada.

---

## O que NÃO fazer

1. **Não apertar o predicado do cadeado.** Tirar a Porta 2
   (`perfil_declara_modo_de_jogo`, `schema.py:666-702`) ou exigir mais dela
   reabre o congelamento que a MODO-01/B2 curou: o preset `coop_local` (que
   casa por título e tem `mode: gamepad`) e todo jogo fora da Steam voltam a
   ficar presos por um cadeado que só prometia não trocar de perfil "ao abrir
   um jogo". O caminho certo é o oposto — dar a ela um perfil que **abre** a
   Porta 1.

2. **Não apagar a cascata Wayland de `integrations/window_backends/`.** Os
   arquivos `wayland_portal.py` e `wlr_toplevel.py` estão inertes hoje
   (`backend=xlib` nas três semeaduras do journal) e vão parecer código morto
   para a próxima leva. Eles são a **única matéria-prima** para o detector um
   dia enxergar janela Wayland nativa — que é a cegueira real das 135 linhas
   de `x11_focus_gate_no_x_focus`. Apagá-los fecha essa porta para sempre e
   não devolve nada em troca.

3. **Não desligar o cadeado** — nem por script, nem por "só para testar", nem
   apagando o `.flag`. Medido: não conserta o jogo (a Causa A independe dele) e
   solta Navegação por cima da configuração dela a cada alt-tab para a Steam,
   18 vezes em três dias. Se um teste manual precisar do cadeado desligado,
   desligue **pela interface** e ligue de volta — a flag é dela, e desligar
   configuração dela sem pedir é a lição de 28/07.

4. **Não revogar nem afrouxar o veto R-21** (`manager.py:620-628`). Ele tem
   razão própria e documentada: sem ele volta o ping-pong de 18-28 s do
   journal de 22-23/07. A cura não é remover o veto — é fazer existir um
   perfil que não seja catch-all.

5. **Não afrouxar `perfil_e_regra_de_jogo` para aceitar regex de título.**
   Está explicado em `schema.py:620-624`: o `fps.json` dela tem `|Control)` e
   `|Metro)` sem âncora, e o predicado tem um segundo consumidor — o furo da
   trava manual em `_activate` (`autoswitch.py:505-518`). Afrouxar aqui apaga
   a configuração que ela acabou de fazer na mão, por outra porta.

6. **Não mexer em prioridade achando que resolve.** Especificidade vem antes
   (`manager.py:632-640`) e o veto nem lê `priority` (`manager.py:620`).

7. **Não escrever nos `.json` dela sem autorização explícita** — inclusive
   "só para normalizar", "só para migrar" ou dentro de um script de instalação.
   O E4 existe exatamente para isso ficar por escrito.

---

## O que fica sem medição

Sou explícito: o que está abaixo eu **não medi**, e não vou fingir que medi.

- **Não rodei a GUI e não cliquei em nada.** O daemon dela está vivo e a
  janela aberta; a sessão é de leitura. Tudo o que digo sobre a interface vem
  de leitura de código e do `.glade`, não da tela.
- **Não chamei `daemon.state_full`.** Os valores vivos de
  `window_detect_last_class`, `game_window_seen_at` e `autoswitch_locked` no
  processo em execução não foram lidos por IPC — inferi do journal, dos
  arquivos-flag e do código. Em particular, **não vi com meus olhos** o sticky
  valendo `Hefesto-Dualsense4Unix` no store vivo; provei que o caminho de
  escrita existe e que a classe própria é lida (7 episódios de
  `autoswitch_janela_propria_ignorada`).
- **Não medi o comportamento com jogo fora da Steam** (GOG, Heroic, itch,
  nativo). Não há nenhum no journal dos três dias. Toda a análise da Porta 1
  vale para `steam_app_<id>`; para os outros, quem manda é a Porta 2, e nenhum
  perfil dela a satisfaz.
- **Não medi o TTL efetivo do sinal de jogo.** Vi
  `HYSTERESIS_SEC = 30.0` em `daemon/subsystems/game_signal.py:62` e a
  `window_seen_age` derivada em `lifecycle.py:3165-3166`, mas não medi qual
  teto de idade seria adequado para a guarda do E2. Fica para quem
  implementar, com medição.
- **Não confirmei o nome legível dos appids `steam_app_1553260`.** Os outros
  dois estão nomeados em `steam_input_apps.txt` (Pragmata e Mullet Mad Jack);
  este não.
- **Não medi por que `pragmata.json` e `pragmata2.json` existem os dois.**
  São byte-a-byte iguais exceto o nome e o mapa `controllers`. A hipótese é
  que ela salvou duas vezes pelo rodapé, mas é hipótese.
- **Não rodei a suíte de testes** desta área. Rodei apenas os dois validadores
  exigidos, sobre este documento.
- **Não estimei prazo de nenhuma entrega.** Preço é relativo (E0 < E1 < E2 <
  E3 < E4), não absoluto.

---

## Nota de medição — 03/08/2026: seis dias depois, e agora COM `daemon.state_full`

Esta nota paga duas das lacunas que a seção acima declarou ("não chamei
`daemon.state_full`", "não vi com meus olhos"). Medido com o daemon dela vivo,
os dois DualSense conectados por Bluetooth, e a mão dela nos controles.

### O cadeado continua ligado — agora há seis dias

```
autoswitch_locked: True                                    (daemon.state_full)
/home/vitoriamaria/.config/hefesto-dualsense4unix/autoswitch_locked.flag
```

A sprint mediu o arquivo em **28/07 18:18**. Em 03/08 ele continua lá e o
**store vivo confirma** o que antes era inferência do arquivo-flag: o valor no
processo em execução é `True`. A lacuna *"não vi com meus olhos"* está paga
para o `autoswitch_locked`.

### E o perfil ativo é NENHUM

```
active_profile: None
```

Com **15 perfis salvos** no disco (`acao`, `aventura`, `bow`, `coop_local`,
`corrida`, `esportes`, `fallback`, `fps`, `meu_perfil`, `navegacao`,
`point_and_click`, `pragmata`, `pragmata2`, `sackboy_nativo`, `vitoria`).

Isto reforça o veredito da sprint por um ângulo que ela não tinha: não é só que
o autoswitch **não troca** de perfil — é que, na conexão, **nenhum perfil
assume**. O daemon sobe, adota os controles, e o `active_profile` fica `None`.

### A consequência que ELA percebeu, e que motivou esta nota

Ela perguntou, olhando os controles recém-conectados:

> *"Quando eu conecto eles de início, qual o perfil assume?"* — e, sobre as
> cores que viu: *"só queria saber se o vermelho e azul eram dos perfis"*.

**Não eram.** As cores vinham da **paleta automática por slot** (`COR-03`):
P1 nasce azul, P2 nasce vermelho. Com `active_profile: None`, é ela que pinta.

Isso importa para o desenho da cura: **a paleta automática mascara o
automatismo morto.** O controle nasce colorido, parece configurado, e o
usuário não tem como distinguir "meu perfil entrou" de "nenhum perfil entrou,
e isto é o padrão de fábrica". A E4 desta sprint (dizer na tela o que está
valendo) deveria cobrir também este caso — hoje não há nada na interface que
diga *"nenhum perfil ativo; a cor que você vê é automática"*.

### O que esta nota NÃO mediu

- **não desliguei o cadeado**, e portanto não sei se, desligado, o autoswitch
  passaria a trocar. A sprint sustenta que **não** passaria (as duas portas
  estão quebradas independentemente do cadeado); isso continua sem prova ao
  vivo;
- **não abri jogo nenhum** nesta medição. A sessão foi de conexão de controles;
- **`pragmata.json` × `pragmata2.json` continuam os dois lá**, e a hipótese do
  "salvou duas vezes pelo rodapé" segue sem confirmação.
