# SINAL-DE-JOGO-01 — o daemon desiste do jogo antes do jogo acabar

- **Status:** ABERTA — documento de medição e plano. Nada de código nesta rodada
- **Prioridade:** MÉDIA — e a prioridade é uma **correção** deste documento sobre
  o achado que o originou. O auditor abriu como ALTA; o verificador independente
  reenquadrou, e este documento segue o verificador. O porquê está na seção
  *"O que o verificador derrubou"*
- **Faixa:** 2 — o produto mente sobre o próprio estado
- **Aberta em:** 31/07/2026, sobre a branch `restauro/inicio-da-sessao`, HEAD
  `7bd0cb7`, com o daemon dela **vivo** (pid 3615, no ar desde 01:10:50 de hoje) e
  **PRAGMATA.exe rodando durante a medição**. Leitura apenas: nada foi executado
  contra o daemon, nada foi reiniciado, nenhum arquivo dela foi tocado
- **Paga:** as dívidas **2 e 3** do
  [índice de 30/07](2026-07-30-INDICE-as-tres-faixas-depois-da-v040.md), linhas
  310-324, que registram por extenso que este defeito *"continua vivo e não tem
  documento nenhum"*. **Este é esse documento.** As duas dívidas viram uma sprint
  só porque são o mesmo defeito visto de dois lados: a dívida 2 é o sintoma
  (a autoridade cai), a dívida 3 é metade da causa (a linha `lifecycle.py:3163`)
- **Sucede:** [JANELA-CEGA-01](2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md)
  (que pagou duas das três pendências e deixou esta), e
  [MODO-01](2026-07-25-MODO-01-o-modo-jogo-liga-sozinho.md) §B4, que foi quem
  escreveu a frase pela primeira vez
- **Relacionada:**
  [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md)
  (o cadeado e os cinco catch-all são o outro eixo do mesmo estado da máquina) e
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
  (a E5 desta sprint não entra sem o olho dela na lightbar)

## O que este documento diz em uma frase

O daemon tem um sinal de três estados — `game`, `daemon`, `unknown` — que decide
**quem pinta o controle** enquanto ela joga. Esse sinal se apoia hoje, na máquina
dela, em **uma única perna**: enxergar a janela do jogo. E a perna que ele usa
para dizer *"não tem jogo nenhum"* é uma flag que **sobe e nunca desce**.

## A medição que faltava, e ela estava na frente da gente

Enquanto eu escrevia este documento — **31/07/2026, 01:57:42**, medido com `date`
— a máquina dela estava, sozinha, exatamente no cenário que o achado descreve.
Isto não é reconstituição de journal: é o estado vivo.

| O que | Como medi | Valor |
|---|---|---|
| O jogo está aberto | `ps -eo pid,etimes,comm` | `PRAGMATA.exe` pid **32069**, vivo há **1223 s** (20 min) |
| Quem lançou | `ps -eo pid,args` | `steam-launch-wrapper -- .../reaper SteamLaunch AppId=3357650` |
| O wrapper do Hefesto está no meio? | mesma linha de comando | **NÃO.** A opção de lançamento dela é `VKD3D_CONFIG=no_upload_hvv %command%` |
| Marker do wrapper | `ls ~/.local/state/hefesto-dualsense4unix/launch_env/` | só os 4 `.env`. **`last_run` e `last_exit` NÃO EXISTEM** |
| Autoridade agora | journal | `game` desde **01:37:58.428466**, sem nenhuma transição em 20 min |
| Episódios de cegueira nesta sessão | `grep -c x11_focus_gate` desde 01:10 | **13** |

Leia a terceira e a quarta linha juntas. **A evidência nº 3 do sinal — o marker do
wrapper — está estruturalmente ausente do jeito que ela joga hoje.** Não é que o
marker expirou: ele nunca foi escrito, porque o jogo não passa pelo wrapper.

E a evidência nº 2 — a regra de perfil — **também não conta**, pelo motivo medido
mais abaixo. Ou seja: neste exato momento, com o jogo vivo há vinte minutos, a
autoridade `game` está pendurada em **uma evidência só**, a janela. É a definição
de ponto único de falha, e é o gate de foco do `xlib` que a derruba.

### E há um episódio de hoje que mostra o gate negando na prática

```
01:37:57.102834  modo_jogo_padrao_adiado  estado=ignorado_sem_jogo
                 motivo=sem_autoridade_de_jogo  wm_class=steam_app_3357650
01:37:57.450600  steam_input_excecao_ativada  appid=3357650
01:37:58.428466  game_signal_transition  de=daemon  evidencia=game  para=game
01:37:58.465662  profile_mode_aplicado   kind=gamepad origin=game_signal
                 wm_class=steam_app_3357650
```

A janela do jogo **já estava na frente** (`wm_class=steam_app_3357650`) e o modo
jogo padrão foi **recusado** porque a autoridade ainda era `daemon`
(`daemon/lifecycle.py:2039-2042`). Um tique depois — 1,3 s — o sinal subiu e o
modo entrou. Aqui foi transitório e inofensivo. É o mesmo gate, pela mesma porta,
que fica negado enquanto a autoridade estiver errada.

## O mecanismo, linha a linha, conferido hoje

### As três evidências de jogo, e só três

`daemon/subsystems/game_signal.py:109-126`. A função `classify` é pura, sem I/O, e
tem exatamente três portas para responder `game`:

| # | Evidência | Onde | O que a sustenta |
|---|---|---|---|
| 1 | **Janela** | `game_signal.py:109-112` | `wm_class` corrente casa `steam_app_\d+`, **ou** a idade de `game_window_seen_at` cabe em `HYSTERESIS_SEC` |
| 2 | **Regra de perfil** | `game_signal.py:113` | `profile_rule_match`, calculado em `lifecycle.py:3119-3142` |
| 3 | **Marker do wrapper** | `game_signal.py:114-121` | `wrapper_game_running` (`daemon/launch_env.py:264-314`), TTL de 900 s em `launch_env.py:106` |

Sem nenhuma das três (`game_signal.py:122-126`):

```python
if ev_janela or ev_perfil or ev_marker:
    return "game"
if window_healthy:
    return "daemon"
return "unknown"
```

`HYSTERESIS_SEC = 30.0` (`game_signal.py:62`) faz dois papéis: é o teto da idade da
janela na evidência 1 **e** o tempo de espera da queda na casca com estado.

### A queda espera 30 s a mais, e só com sessão aberta

`game_signal.py:157-180`. Subir para `game` e cair para `unknown` são imediatos
(≤1 tique). Só a queda para `daemon` passa pela histerese, e ela exige
`session_open=True` — sem sessão uhid aberta não há réplica de exibição a
proteger, e a queda é imediata (`:171-174`).

O tique é de **2,0 s** (`lifecycle.py:3291-3293`). Somando: para a autoridade cair
com o jogo vivo é preciso **mais de 60 s contínuos** sem nenhuma das três
evidências — 30 s para a idade da janela decair, mais 30 s de histerese.

### O gate de foco do `xlib` é quem apaga a evidência 1

`integrations/window_backends/xlib.py:244-279`. O comentário no próprio arquivo
(`:245-255`) conta a história: o `_NET_ACTIVE_WINDOW` fica rançoso no
`cosmic-comp` e aponta até para janela X morta enquanto o foco real está numa
superfície Wayland nativa. A cura foi perguntar ao servidor X quem tem o foco
(`:256`) e devolver `None` quando a resposta é `X.NONE`/`X.PointerRoot` (`:273-278`)
ou quando nem vem um id (`:267-272`).

Medido no journal: **403 episódios** de `x11_focus_gate` desde 25/07, **13** só
nesta sessão do daemon. A MODO-01 §B4 cita 47 episódios e a linha `xlib.py:248`;
**a linha mudou de número** — hoje o `get_input_focus()` está em `:256` e as saídas
do gate em `:267-278`. O fato é o mesmo, a citação é que envelheceu.

Cada `None` do backend vira uma leitura NÃO-útil no store
(`daemon/subsystems/autoswitch.py:144-148` chamando
`state_store.py:279-334`): `window_detect_current_class` é regravada como `None`
(`state_store.py:320-322`), e o carimbo de `game_window_seen_at` **não** é
renovado (`:331-334`). A evidência 1 começa a envelhecer.

### O trinco de mão única — a dívida 3, encontrada viva hoje

`daemon/lifecycle.py:3163`, lido hoje, palavra por palavra:

```python
window_healthy = self.store.window_detect_healthy
```

`window_detect_healthy` (`state_store.py:420-441`) nasce `True` por **presunção**
quando o backend é `xlib` (`daemon/subsystems/autoswitch.py:99-103`, e o journal de
hoje confirma: `window_detect_diag_seeded backend=xlib healthy=True` às
01:10:50), e **nunca desce** dentro do mesmo episódio do detector. O campo que
responde *"o detector enxerga AGORA?"* existe e se chama `window_detect_seeing`
(`state_store.py:459-472`), decai depois de `WINDOW_DETECT_BLIND_AFTER_SEC = 300.0`
(`state_store.py:43`) e volta na primeira leitura útil.

**E isto não é lapso.** O próprio `state_store.py:427-438` avisa por escrito, com
todas as letras, que o trinco é contrato e não descuido, que o único consumidor de
decisão é o `game_signal`, e — a frase que governa esta sprint —

> *"Trocar o consumidor do `game_signal` de `healthy` para `seeing` é uma leva
> própria, com ela vendo."*

O resultado prático é que a docstring de `classify` promete uma coisa
(`game_signal.py:102-104`: `daemon` exige *"evidência POSITIVA de detector são"*) e
recebe outra: um booleano que é presunção de boot, não medição. Com o detector
cego e sem evidência de jogo, o sinal responde `daemon` onde o fail-safe escrito
manda responder `unknown`.

## O que o verificador derrubou, e por que este documento segue ele

O achado que originou esta sprint veio como ALTA e trazia **seis transições de
journal** como prova de que a autoridade cai *"com o jogo aberto"*. O verificador
independente foi atrás do contexto de cada uma. **Nenhuma das seis prova isso:**

- **29/07 16:56:49 e 17:53:48** — o marker do wrapper estava **fresco** naquelas
  janelas (`launch_arm_sem_perfil appid=1553260` às 16:54:50; `launch_arm_pulado_allowlist
  appid=2111190` às 17:49:49 — idades de 119 s e 239 s contra um TTL de 900 s). Com
  marker fresco, a única forma de a evidência 3 não segurar o sinal é
  `pid_alive=False` (`launch_env.py:308-309`). Ou seja: nessas duas quedas o
  processo do jogo estava **morto**. A queda estava certa.
- **29/07 17:13:29 e 20:15:35, e 30/07 02:30:00** — vêm 60 a 90 s depois de
  `steam_input_excecao_encerrada`, e são seguidas de 36 min a 2 h 24 **sem
  nenhuma evidência de jogo e sem nenhum outro appid**. Isso é fechamento real, e
  fechamento real é o comportamento **projetado**: o comentário em
  `core/backend_pydualsense.py:1164-1169` diz que neutralizar a sessão uhid
  rançosa do cliente Steam é o objetivo, e que *"fechar o jogo devolve a paleta em
  ≤ ~32 s"*.
- **28/07 23:17:49** — fica sem contexto suficiente para decidir.

O verificador também mediu o episódio inverso, e vale registrar: em **28/07
23:16:22-23:16:39** houve perda de foco com o jogo comprovadamente vivo (exceção
encerrada sob `x11_focus_gate`, jogo de volta ao foco 16 s depois) — e **o sinal
não caiu**, porque 16 s é menos que os 30+30 s exigidos. A histerese fez o trabalho
dela.

**O falso negativo é real. O cenário é mais estreito do que foi alegado:**

> jogo vivo **e** mais de 60 s contínuos sem foco X **e** (marker expirado, TTL de
> 900 s, **ou** jogo lançado sem o wrapper).

E há autocorreção, que o achado original omitiu: a **subida é imediata** (≤1 tique,
`game_signal.py:167-170`) e a transição `daemon → game` dispara
`replay_retained_game_outputs()` (`lifecycle.py:3224-3228`), que repinta o que o
jogo escreveu; a retenção nunca cessa (o journal registra
`game_output_retido_sem_jogo`, `backend_pydualsense.py:2799`).

Por isso a prioridade desta sprint é **MÉDIA**, e por isso a **E1 é um
experimento, não um conserto**: em nenhum momento, em nenhum documento desta casa,
alguém mediu a queda com jogo comprovadamente vivo. A frase da MODO-01 §B4 e a
frase do índice de 30/07 descrevem um mecanismo correto sobre uma medição que
ninguém fez.

## O que a autoridade errada custa, medido

Quando o sinal cai para `daemon`, `lifecycle.py:3219-3223` chama
`controller.defend_display()`. E `defend_display` (`backend_pydualsense.py:3109-3132`)
invalida os caches de sysfs e faz reassert verificado — ou seja, **repinta**. Sob
autoridade `daemon` a camada do jogo é excluída do merge
(`backend_pydualsense.py:1170-1172`): a cor que o jogo escreveu deixa de valer.

E os gates que exigem `authority == "game"` passam a negar:

| Gate | Onde | O que ela vê |
|---|---|---|
| Modo jogo padrão | `lifecycle.py:2039-2042` | `modo_jogo_padrao_adiado ... sem_autoridade_de_jogo` — medido hoje às 01:37:57 |
| Gate do teclado no jogo | recusado por escrito no commit `2bbfa22` | o índice de 30/07:310-313 registra que **não** condicionaram o gate a este sinal justamente por causa deste defeito |
| Aviso do "Renumerar agora" | `app/actions/home_actions.py:287-304` | o aviso *"Feche o jogo para renumerar"* **some** da aba Início com o jogo aberto |

O terceiro é o que mais interessa a esta sprint, e não pelo dano: **é o único
lugar da janela dela onde este sinal aparece.** Serve de mostrador. Está descrito
na seção de validação.

## A segunda metade do defeito: o probe que só recebe a wm_class

Esta é a entrega própria que o índice não previu, e é a que mais mexe no caso
dela.

`lifecycle.py:3131-3133`, conferido hoje:

```python
profile = self._manager_de_selecao().select_for_window(
    {"wm_class": wm_class}
)
```

Só `wm_class`. Mas o matcher aceita três campos
(`profiles/schema.py:70-94`): `window_class`, `window_title_regex` (por `wm_name`,
`:76-87`) e `process_name` (por `exe_basename`, `:88-90`) — e ele é um **E** entre
os campos preenchidos (`:92-94`). Pior: alvo vazio **nunca casa**, por decisão
escrita em `profiles/schema.py:42-47` (*"ausência de evidência, não igualdade com
uma entrada vazia"*).

Consequência: qualquer perfil que dependa de título ou de nome de processo
devolve `False` neste probe **sempre**, sem erro nenhum.

O dado bruto está lá em cima, no `AutoSwitcher` — `profiles/autoswitch.py:434-435`
lê `wm_name` e `exe_basename` do mesmo `info` — mas o `StateStore` só guarda a
classe (`state_store.py:279-334` recebe `wm_class` e mais nada; a property é
`window_detect_current_class`, `:496-506`). **Não é uma linha de conserto: o store
precisa passar a carregar os outros dois campos.**

### Medido nos 15 perfis reais dela, hoje

Carreguei os arquivos de `~/.config/hefesto-dualsense4unix/profiles/` com o
`MatchCriteria` do próprio projeto e rodei `matches()` com três formas de janela.
São **15** arquivos hoje (o achado dizia 14), **5** deles catch-all — `fallback`,
`meu_perfil`, `pragmata`, `pragmata2`, `vitoria` — exatamente os cinco que o
journal de hoje nomeia em `profile_select_catch_all_sem_autoridade_em_jogo` às
01:51:04.

| Perfil | prio | casa por | `mode.kind` | probe **hoje** | + `wm_name` | + `wm_name` e `exe_basename` |
|---|---:|---|---|---|---|---|
| `sackboy_nativo` | 80 | `window_class` (`steam_app_1599660`) | gamepad | **True** | — | — |
| `coop_local` | 75 | **só título** | gamepad | False | **True** | True |
| `aventura` | 70 | título **e** processo | gamepad | False | False | **True** |
| `acao` | 65 | título **e** processo | gamepad | False | False | **True** |
| `fps` | 60 | título **e** processo | gamepad | False | False | **True** |
| `corrida` | 55 | título **e** processo | gamepad | False | False | **True** |
| `esportes` | 55 | título **e** processo | gamepad | False | False | **True** |
| `point_and_click` | 60 | `window_class` | — | False | — | — |
| `navegacao` | 50 | `window_class` | — | False | — | — |
| `bow` | 10 | só título | — | False | — | — |

Três leituras saem daqui, e as três importam:

1. **A evidência nº 2 é letra morta na máquina dela.** O único perfil que o probe
   consegue casar é o `sackboy_nativo` — e ele casa por uma `wm_class`
   `steam_app_1599660`, que a **evidência nº 1 já teria pego sozinha**. Em 15
   perfis, a evidência 2 não cobre **nenhum** caso que a evidência 1 não cubra.
2. **Passar só o título não basta.** Cinco dos seis perfis de jogo dela têm
   `process_name` preenchido junto com o título, e o matcher é um E: sem
   `exe_basename` eles continuam falsos. É a armadilha que quase entrou aqui como
   conserto de uma linha.
3. **Isto amarra na AUTOMATISMO-MORTO-01.** O cadeado do autoswitch cede por dois
   predicados (`profiles/autoswitch.py:252`, `:260-263`), e o segundo —
   `perfil_declara_modo_de_jogo`, `profiles/schema.py:666-702` — aceita match por
   título. Ou seja: o mesmo `coop_local` que **fura o cadeado** por título é o
   perfil que **nunca vira evidência de jogo** por título. O produto trata a
   mesma regra como forte num lugar e inexistente no outro.

## Entregas, na ordem em que devem entrar

A ordem é por risco crescente, e a última entra **sozinha**.

### E1. O experimento que ninguém fez: derrubar a autoridade com o jogo vivo

Nenhuma medição desta casa provou a queda com jogo comprovadamente vivo. As seis
transições que o achado apresentou como prova foram derrubadas uma a uma pelo
verificador. Antes de mexer em qualquer linha, **a queda precisa existir numa
medição**.

O roteiro é curto porque a máquina já está no cenário (jogo sem wrapper, sem
marker, autoridade pendurada só na janela):

1. Jogo aberto e a autoridade em `game` — confirmar pelo aviso da aba Início
   (seção de validação abaixo).
2. Alt-tab para uma janela **Wayland nativa** (a própria janela do Hefesto serve —
   é ela que aparece como `Hefesto-Dualsense4Unix` nos logs da JANELA-CEGA-01) e
   **ficar lá 90 s**, sem tocar no teclado, com o jogo rodando atrás.
3. Anotar: o `x11_focus_gate_no_x_focus` aparece? O
   `game_signal_transition de=game para=daemon evidencia=daemon_histerese_expirada`
   aparece? Quantos segundos depois?
4. Voltar ao jogo e cronometrar a subida.

Três resultados possíveis, e **os três são entrega**: a queda acontece (o defeito
está provado e as E3/E4 ganham urgência); a queda não acontece porque o
compositor mantém foco X mesmo com janela nativa na frente (o defeito é menor do
que o documento supõe e isso precisa ficar escrito); ou o gate dispara mas alguma
outra evidência segura o sinal (e aí descobrimos qual, o que muda o desenho da
cura).

**Aceite:** um bloco de journal com carimbo de tempo, colado neste documento, que
mostre o estado do processo do jogo (`ps`, com `etimes`) no instante da transição
— ou a ausência dela. Sem a prova do processo vivo ao lado, a medição não vale:
foi exatamente essa omissão que fez as seis transições anteriores não provarem
nada.

**Risco:** zero de código. O único custo é o tempo dela com o jogo aberto. Não
precisa de terminal para ela: quem lê o journal sou eu, e o mostrador dela é a aba
Início.

### E2. A telemetria que falta: qual evidência caiu

Hoje a transição loga `evidencia=daemon_histerese_expirada`
(`game_signal.py:179`) — uma string que diz **que** caiu e não diz **por quê**. É
por isso que auditor e verificador leram as mesmas seis linhas e chegaram a
conclusões opostas: no journal, *"o detector cegou com o jogo aberto"* e *"o jogo
fechou"* são **byte a byte iguais**.

A entrega é acrescentar ao log da transição o retrato das três evidências no
tique da queda: janela (classe corrente e idade do carimbo), perfil (bool) e
marker (presente/expirado/pid morto), mais o `window_detect_seeing` do momento.

**Aceite:** uma queda no journal permite dizer, sem `ps` e sem adivinhação, se o
jogo tinha morrido ou se o detector tinha cegado.

**Risco:** baixo. É acrescentar campos a um `logger.info` que já existe. Nada
muda de comportamento.

**Mordida:** o teste monta dois cenários que hoje produzem a **mesma** linha de
log — (a) marker morto e detector enxergando o desktop, (b) marker ausente e
detector cego com a janela do jogo lida 40 s atrás — e exige que os dois logs
sejam **distinguíveis**. Com a cura arrancada (volta à string única), os dois
retratos ficam idênticos e o teste reprova. Um teste que só verificasse "o log
tem um campo novo" passaria com a cura pela metade e não vale.

### E3. O probe de perfil recebe a janela inteira, não só a classe

`lifecycle.py:3131-3133` passa a receber `wm_name` e `exe_basename`, e o
`StateStore` passa a carregá-los (`state_store.py:279-334`, alimentado por
`daemon/subsystems/autoswitch.py:144-148`, que já tem os dois no `info`).

**Aceite:** medido contra os 15 perfis reais dela, a coluna *"probe hoje"* da
tabela acima deixa de ter um único `True`. Alvo: `coop_local`, `aventura`, `acao`,
`fps`, `corrida` e `esportes` passam a poder valer como evidência de jogo quando a
janela deles estiver na frente.

**Risco:** médio-baixo, e o risco tem nome. O `select_for_window` fica mais
permissivo, e um regex solto de título — o `|Control)`, `|Metro)` do `fps.json`
que a `profiles/schema.py:685-691` cita como armadilha conhecida — passa a poder
declarar "é jogo" a partir de uma aba de navegador. **Aqui isso é menos grave que
no cadeado**, porque o consumidor é o sinal de exibição e não a troca de perfil;
mas é o mesmo buraco por outra porta, e precisa ficar escrito no commit. O
tradeoff correto está na AUTOMATISMO-MORTO-01, não aqui.

**Mordida:** dois testes, e o segundo é o que morde de verdade.
1. Perfil no formato do `coop_local` (só `window_title_regex`, `mode: gamepad`):
   com a janela trazendo `wm_name`, `_profile_rule_matches_game` devolve `True`.
   Arrancar a cura (voltar a `{"wm_class": wm_class}`) reprova.
2. Perfil no formato do `fps.json` (título **e** `process_name`): passar **só** o
   `wm_name` tem de continuar dando `False`, e só com `exe_basename` junto vira
   `True`. **Este é o teste que uma cura pela metade não passa** — e a cura pela
   metade é o caminho natural de quem lê "perfil casado por título" e conclui que
   basta o título. Os testes que existem hoje
   (`tests/unit/test_game_signal_wiring.py:282-343`) cobrem só perfil casado por
   `window_class` e passariam intactos com o defeito no lugar.

### E4. O processo do jogo vivo como evidência que não depende de foco

É a cura de raiz: hoje as três evidências dependem, na máquina dela, de o detector
de janela enxergar (1 e 2) ou de o jogo ter passado pelo wrapper (3). Medido hoje:
**o jogo dela não passa pelo wrapper**. Sobra uma perna.

A evidência nova é o processo do jogo estar vivo — pelo pid do marker quando ele
existe, ou por uma varredura barata de `/proc` quando não existe. O detector cegar
deixa de derrubar o sinal.

**Aceite:** com o detector cego (gate de foco ativo), sem marker e sem perfil
casado, mas com o processo do jogo vivo, o sinal permanece `game`. Com o processo
morto, cai — dentro dos mesmos 60 s de hoje.

**Risco:** médio, e é o risco do incidente que criou este subsistema. O
`game_signal.py:5-10` conta que *"sessão uhid aberta"* já foi tratada como jogo e
que o **cliente Steam sem nenhum jogo rodando** escreveu lightbar e player-LEDs
com o daemon defendendo a cor do cliente. Uma varredura de `/proc` mal calibrada
repete isso: `steam`, `steamwebhelper`, `reaper` e `wineserver` **não** são jogo.
O critério tem de ser o executável do jogo, não a árvore da Steam. E há custo por
tique a medir — o tique é de 2 s (`lifecycle.py:3291-3293`) e a varredura roda no
executor, junto com o resto do `_gather_game_signal_inputs`.

**Mordida:** dois testes, em espelho.
1. Detector cego, sem marker, sem perfil, **processo do jogo vivo** → `game`.
   Arrancar a evidência nova → `daemon` e reprova.
2. Detector cego, sem marker, sem perfil, e vivos **apenas** `steam`,
   `steamwebhelper` e `reaper` → **não** pode ser `game`. Este é o teste que
   reprova a implementação preguiçosa (varrer a árvore da Steam inteira), e é
   literalmente o incidente das 14:42 escrito como teste.

### E5. `healthy` vira `seeing` — sozinha, e com ela olhando a lightbar

A dívida 3 do índice, e a última porque é a mais perigosa.

`lifecycle.py:3163` passa a ler `self.store.window_detect_seeing()` no lugar de
`self.store.window_detect_healthy`. Com isso, detector cego e sem evidência de
jogo passa a classificar `unknown` — o fail-safe que a docstring de
`classify` (`game_signal.py:102-104`) promete — em vez de `daemon`.

**Esta entrega entra SOZINHA, num commit só, e com ela olhando o controle.** O
motivo está escrito no código desde 28/07, em `state_store.py:427-438`: a
transição `daemon → unknown` dispara `replay_retained_game_outputs()`
(`lifecycle.py:3224-3228`), que **repinta a lightbar** com o que o jogo deixou
retido. Mudar isso de lambuja é mudar a cor do controle dela no desktop, em
silêncio. Regra
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
sem o olho dela, não entra.

Ordem obrigatória: **E5 depois de E3 e E4.** Com as duas anteriores no ar, o sinal
tem outras pernas e a mudança de `healthy` para `seeing` deixa de ser a única coisa
segurando a autoridade. Entrar antes é trocar um defeito conhecido por um
comportamento novo sem rede.

**Aceite:** o desktop com detector **enxergando** continua respondendo `daemon`
(nada muda para ela no uso normal); o detector cego por mais de 300 s
(`WINDOW_DETECT_BLIND_AFTER_SEC`, `state_store.py:43`) sem evidência de jogo passa
a responder `unknown`; e **ela olha a lightbar** nas duas situações e diz se a cor
mudou.

**Risco:** o mais alto da sprint, e o único item da lista cujo efeito ela vê na
mão. Também é o único que muda uma decisão do daemon a partir de um campo que
**decai**, ou seja: passa a existir uma transição que hoje é impossível.

**Mordida:** três testes, e o terceiro é o que impede a cura de virar regressão.
1. `seeing=False` (mais de 300 s sem leitura útil), sem nenhuma evidência de jogo
   → `unknown`. Arrancar a cura (voltar a `healthy`) devolve `daemon` e reprova.
2. `seeing=True` no desktop vazio, sem evidência → continua `daemon`. **Sem este
   teste, uma cura que sempre devolvesse `unknown` passaria no primeiro** — e o
   `defend_display` nunca mais rodaria, que é o defeito que o NUMA-03 curou.
3. A transição `daemon → unknown` chama `replay_retained_game_outputs()` exatamente
   uma vez (`lifecycle.py:3224-3228`). É o repintar que ela vai ver; se o teste não
   o fixa, um refactor futuro o remove sem ninguém perceber.

## Como você valida na tela

Sem terminal, e o mostrador já existe na janela — só não estava sendo usado para
isto.

**O mostrador:** aba **Início**, o botão *"Renumerar agora"*. Quando a autoridade
é `game`, ele mostra o aviso **"Feche o jogo para renumerar"**
(`app/actions/home_actions.py:281-284` e `:287-304`). Quando a autoridade cai para
`daemon`, **o aviso some**. Ou seja: com o jogo aberto, o aviso sumir É o defeito
acontecendo, na sua frente.

Dois cuidados, medidos: a aba Início só se reconcilia quando **ela é a aba
visível** (`home_actions.py:794-798` testa `get_current_page() == 0`) e o ritmo é
de 2 s (`HOME_POLL_INTERVAL_MS = 2000`, `:49`). Então: **deixe a janela na aba
Início** durante o teste. Numa outra aba, o aviso mente.

1. Abra o jogo. Vá para a aba **Início** e confirme que o aviso *"Feche o jogo para
   renumerar"* está lá. Isso é a autoridade em `game`.
2. Aba **Sistema**: a linha da detecção de janela tem de dizer **"funcionando"**,
   com a classe da janela entre parênteses
   (`app/actions/daemon_actions.py:142-160`). Essa linha entrou na leva de 29/07 e
   é ela que denuncia a cegueira.
3. Agora o teste da E1: com o jogo rodando, clique na janela do Hefesto (que é
   Wayland nativa) e **fique nela por 90 s**, na aba Início, sem tocar em nada.
4. Olhe as duas coisas ao mesmo tempo: a linha da aba Sistema muda de
   "funcionando" para o motivo da cegueira? O aviso da aba Início some com o jogo
   ainda aberto? **Se o aviso sumir, o defeito está provado, e a data e a hora
   valem mais que este documento inteiro.**
5. Volte para o jogo. O aviso tem de voltar em poucos segundos — a subida é
   imediata, por desenho.
6. **Depois da E5, e só dela:** repita o passo 3 **olhando a lightbar do
   controle**. Se a cor mudar em algum momento, a entrega reprova e sai. É o único
   aceite desta sprint que não é meu.

## O que fica de fora desta sprint, por escrito

- **O furo do cadeado por título.** `profiles/autoswitch.py:252` e `:260-263`
  cedem por `perfil_e_regra_de_jogo` **ou** `perfil_declara_modo_de_jogo`
  (`profiles/schema.py:666-702`), e o segundo aceita match por título — o
  `coop_local` dela (prioridade 75, sem `process_name`) pode, em tese, ligar
  gamepad e co-op a partir de um título de navegador. Isso é da
  [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md),
  não daqui. Medido: **zero** ocorrências no journal desde 25/07 (as 3 cessões
  registradas são todas por `steam_app_*`, legítimas). Fica registrado aqui só
  porque a E3 mexe no mesmo `select_for_window` — e porque uma das curas
  propostas lá é exigir `display_authority == "game"` no predicado do cadeado, o
  que **depende deste sinal ser confiável**. A ordem certa é esta sprint primeiro.
- **Fazer o `window_detect_healthy` decair.** Não é isso que a E5 propõe, e a
  diferença importa: o trinco continua sendo trinco (é contrato, e a JANELA-CEGA-01
  o justificou), o que muda é **quem o sinal de jogo consulta**. Mexer na property
  quebraria os outros leitores dela.
- **Pôr o wrapper na opção de lançamento dela.** Medido hoje: ela joga
  `VKD3D_CONFIG=no_upload_hvv %command%`, sem o wrapper do Hefesto. Trocar a opção
  de lançamento dela é configuração da máquina dela, não entrega de código — e a
  memória desta casa registra que opção de lançamento mal posta já custou caro
  ("launch option é veneno", 16/07). O desenho correto é o daemon **não precisar**
  do wrapper, que é a E4.
- **Baixar a histerese de 30 s.** Ela é do desenho da Onda N, está travada por
  teste e tem uma razão medida: alt-tab curto não pode derrubar a posse. O
  episódio de 28/07 23:16 (16 s de perda de foco, sem queda) é a prova de que ela
  funciona. Encurtar trocaria um falso negativo raro por um falso positivo
  frequente.
- **A reescrita do god-object.** A classe `Daemon` tem ~3280 linhas e ~95 métodos,
  e o aglomerado "sinal de jogo + gather" é um dos candidatos naturais a sair para
  módulo próprio. É trabalho de estrutura e não entra numa sprint de defeito.
- **O gate do teclado.** O commit `2bbfa22` recusou por escrito condicioná-lo a
  este sinal, e a recusa continua correta enquanto o sinal não for confiável.
  Reabrir o assunto é consequência das entregas daqui, não parte delas.

## O que eu não medi

- **A queda com o jogo vivo.** É a E1, e é a razão de ela ser a primeira entrega.
  Nenhuma das seis transições do achado original a prova, e eu não a reproduzi:
  o daemon dela está vivo com o jogo aberto, e forçar o cenário significaria
  mexer no foco da máquina dela no meio de uma partida.
- **Se a janela do jogo dela em tela cheia dispara o gate de foco.** Os 47
  episódios da MODO-01 são medição de 25/07, num contexto de desktop. Os 403
  episódios que contei desde 25/07 não estão separados entre "no jogo" e "no
  desktop" — e a memória desta casa registra, de 30/07, que o detector **não** é
  cego dentro do jogo. As duas coisas convivem: cego no desktop, enxergando no
  jogo. É exatamente por isso que a E1 precisa acontecer com o jogo aberto e o
  foco fora dele.
- **O custo por tique de varrer `/proc`** (E4). O tique é de 2 s e roda no
  executor; nunca medi quanto custa uma varredura em 400 processos nesta máquina.
- **A vida do processo do jogo nas quedas de 29/07 20:15:35, 30/07 02:30:00 e
  28/07 23:17:49.** O marker expirado não desambigua. O verificador inferiu
  fechamento pelo contexto — inferência, não medição.
- **A suíte da área.** A auditoria foi só-leitura com o daemon vivo; não rodei
  `pytest` nesta rodada. As mordidas descritas acima são desenho de teste, não
  testes rodados.
- **Se algum perfil dela mudou de mão.** A tabela dos 15 perfis é do disco de
  hoje, 31/07, 01h. Ela edita perfis pela janela; se editar entre esta medição e a
  entrega, os números da tabela mudam — o mecanismo, não.
