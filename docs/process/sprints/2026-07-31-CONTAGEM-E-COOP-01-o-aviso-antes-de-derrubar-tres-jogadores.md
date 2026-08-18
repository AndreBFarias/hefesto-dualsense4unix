# CONTAGEM-E-COOP-01 — o aviso antes de derrubar três jogadores

- **Status (09/08/2026):** **E1 e E2 ENTREGUES EM CÓDIGO — AGUARDANDO A PALAVRA
  DELA.** As duas entraram em `cd5eaf1` (31/07/2026), **três minutos e vinte e
  dois segundos** depois do índice que as agendava como pendentes. **A E3
  continua ABERTA.** Conferência na
  [nota datada no fim](#nota-datada-09082026--o-aviso-existe-desde-o-dia-em-que-esta-sprint-foi-agendada)
- **O que falta ela validar, em uma linha:** montar o co-op, abrir um jogo com o
  Steam Input marcado, e ver se o aviso aparece no topo da janela — de qualquer
  aba — dizendo **quantos** jogadores caíram e que **não foi ela**
- **Status anterior:** *"ABERTA — documento de medição e plano. Nada de código
  nesta rodada"*. **Não se apaga**: era verdade quando foi escrito, e deixou de
  ser no mesmo dia
- **Prioridade:** MÉDIA-ALTA — não custa nada enquanto ela joga com um controle,
  e custa a noite inteira quando os quatro estão na mesa. A medição do journal
  mais abaixo mostra por que ela subiu de "MÉDIA" para cá: o caminho que derruba
  o co-op foi percorrido **20 vezes em três dias**, a última hoje às 01h51
- **Prometida em:** 26/07/2026 —
  [INDICE-o-que-falta](2026-07-26-INDICE-o-que-falta.md), seção 4, linha 373
  (*"um número só, e ninguém derruba três jogadores sem perguntar"*), com o
  aviso de que ela existia *"por enquanto só como as seções 4 e 5 deste índice"*
  (`:188`). Recobrada em 27/07 (`2026-07-27-INDICE-o-que-ficou-pelo-caminho.md:77`),
  em 29/07 ([INDICE-o-que-falta-depois-da-v030](2026-07-29-INDICE-o-que-falta-depois-da-v030.md),
  linhas 44 e 199) e em 30/07
  ([INDICE-as-tres-faixas](2026-07-30-INDICE-as-tres-faixas-depois-da-v040.md),
  linhas 193 e 357)
- **Aberta em:** 31/07/2026 — cinco dias depois da promessa. Este arquivo é ela
- **Absorve:** [CONTAGEM-01](2026-07-25-CONTAGEM-01-a-tela-diz-dois-com-quatro-na-mesa.md)
  e [UI-SELETOR-01](2026-07-25-UI-SELETOR-01-ordem-dos-controles-no-seletor.md),
  por declaração do índice de 29/07 (`:65`)
- **Irmã, e entra aqui:** [JOGO-01](2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md),
  **entrega 2** — a superfície da exceção de Steam Input na janela. É pendência
  declarada DENTRO do código, em dois arquivos, e está fora de todas as faixas
  dos índices de 29 e 30/07
- **Encosta em:** [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md)
  (a E3 de lá e a E2 daqui são **a mesma entrega**, vista dos dois lados),
  [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md)
  (o desfazer dentro da janela é de lá, e esta sprint não o rouba),
  [BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md)
  (a entrega 4 dela escreveu o único texto da tela que hoje diz o preço) e
  [EMULACAO-NO-JOGO-01](2026-07-29-EMULACAO-NO-JOGO-01-o-r1-troca-de-app-em-vez-de-jogar.md)
  (a E1(c) de lá é o precedente de vocabulário que a E3 daqui copia)
- **Regra da casa que se aplica:** [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
  As entregas E1 e E3 escrevem frase nova na tela dela — **não entram sem o olho
  dela**, com foto antes e depois

## A promessa mais antiga da casa

`CONTAGEM-E-COOP-01` é um identificador que existe em toda parte menos onde
deveria. Contado hoje, no HEAD `7bd0cb7`:

```
$ grep -rn "CONTAGEM-E-COOP-01" src/ tests/ | wc -l
15
$ ls docs/process/sprints/ | grep CONTAGEM-E-COOP
(nada)
```

As quinze menções são treze em `src/` — `daemon/ipc_handlers.py:1639`,
`daemon/subsystems/gamepad.py:332`, `:498`, `:565`, `:1401`, e oito em
`app/actions/status_actions.py` (`:89`, `:129`, `:358`, `:1138`, `:1445`,
`:1480`, `:1611`, `:1635`) — e duas em `tests/`, os cabeçalhos de
`tests/unit/test_coop_nao_cai_em_silencio.py:1` e
`tests/unit/test_contagem_um_numero_na_janela.py:1`.

Quatro índices mandam ler um documento que nunca foi escrito, e um deles diz
isso com todas as letras: *"O documento que a casa promete desde 26/07 e nunca
escreveu"* (índice de 29/07, `:199`). É a promessa de documento mais antiga
viva. Não é a maior dívida do projeto — é a mais velha, e é a única em que
**metade do trabalho já foi feita sem que houvesse onde registrá-la**.

Este documento faz três coisas: registra o que já está pago, com arquivo e
linha; mede o que falta; e propõe três entregas com aceite e mordida.

## Uma correção de citação, antes de tudo

Os índices de 26 e 29/07 apontam linhas que **não existem mais** — eles foram
escritos antes da cura de 29/07 e as linhas andaram. Quem atacar esta sprint com
o índice na mão erra o alvo. Reconferido hoje, arquivo por arquivo:

| O índice diz | Hoje é |
|---|---|
| `status_actions.py:1063` soma `conectados + externals` | `:1063` está dentro de `_sync_coop_governa_luzes` (`:1058`), que fala de lightbar. A soma virou a property `na_mesa` em `:120-123` |
| `status_actions.py:1391` e `:1504` usam `len(conectados)` | as duas viraram chamadas a `_contagem_de_controles` (`:1486` e `:1613`) |
| `home_actions.py:340` usa `len(controllers)` | `:340` é `if len(players) < 2:`; a frase com `len(controllers)` está em `:342` — e continua lá (ver *O que fica de fora*) |
| `gamepad.py:473-475` chama `coop.disable()` sem perguntar nada | `:473-475` hoje é o `logger.warning("steam_input_vpad_mantido_de_pe", …)`. O `coop.disable()` está em `:495` |

Nada disso enfraquece o achado — o `coop.disable()` continua sendo chamado sem
perguntar nada a ela. Só mudou de linha.

## O que JÁ está pago, medido no código de hoje

Metade desta sprint entrou em 29/07, sem documento. Está aqui para parar de ser
invisível.

### (a) A conta única da janela

| Peça | Onde | O que faz |
|---|---|---|
| `ContagemDeControles` | `app/actions/status_actions.py:85-123` | dataclass com os DOIS espaços: `adotados` e `externos`; `na_mesa` é a soma (`:120-123`) |
| a decisão, por escrito | `:87-115` | por que **não** se soma tudo num número só: externo não tem card nem bateria (EXT-COUNT-01, 25/07), mas divide o espaço de numeração (R-24/NUM-01). Inflar `adotados` regrediria as duas coisas |
| `texto_de_contagem` | `:126-154` | os três regimes: `""` com um controle, `"3 controles"` sem externos, `"2 do Hefesto + 2 externos"` com eles |
| `_contagem_de_controles` — a ÚNICA conta | `:1444-1460` | deriva de `_connected_controllers` (`:1430-1442`) mais `self._externals` |
| o cabeçalho consome | `:1480-1487` | antes era `len(conectados)`: dizia "2 controles" com quatro chips ao lado |
| a linha "Conectado (N controles)" consome | `:1611-1619` | mesma função, mesmo texto nomeado |
| a linha de bateria usa `adotados`, **não** `na_mesa` | `:1635-1640` | um externo na mesa não pode fazer a bateria do primário sumir |
| teste | `tests/unit/test_contagem_um_numero_na_janela.py` | 11 funções, 19 casos coletados |

**A decisão do cabeçalho `"N do Hefesto + M externos"` é decisão, não lapso**, e
está escrita em `:87-115` com as duas razões históricas. Esta sprint não a
revisita; ela a estende para o único lugar que ficou de fora (a aba Emulação,
entrega E2).

### (b) O fato da queda do co-op, emitido pelo daemon

| Peça | Onde | O que faz |
|---|---|---|
| a queda em si | `daemon/subsystems/gamepad.py:492-497` | sob `_emu_lock`: `coop.disable()` (`:495`) e `stop_gamepad_emulation(persist=False, release_grab=False)` (`:497`) |
| a contagem do estrago | `:508-514` | medida pelo **residual** (antes menos o que sobrou), não por `n_jogadores` — `disable()` roda sob `suppress` e um teardown que estoura no meio deixa jogador de pé |
| o log com nome próprio | `:521-529` | `coop_derrubado_pela_excecao_steam_input`, em **WARNING**, com `secundarios_derrubados` e `secundarios_restantes` |
| o contador do store | `:530-537` | `gamepad.steam_input.coop_derrubado`, com `suppress` próprio para um bump que estoura não engolir o outro |
| a leitura pública | `:329-346` | `steam_input_coop_derrubados` — conta SECUNDÁRIOS (P2+); o P1 tem observável próprio |
| as DUAS mortes do aviso | `:565-579` e `:1401-1411` | a borda de saída da exceção e o gesto manual de religar a emulação zeram o contador. Aviso pendurado depois de o co-op voltar seria mentira nova |
| a publicação | `daemon/ipc_handlers.py:1639-1662` | `coop.derrubado_por_steam_input` (bool, o gatilho) e `coop.secundarios_derrubados` (int, o tamanho) |
| teste | `tests/unit/test_coop_nao_cai_em_silencio.py` | 9 testes, três classes: o journal diz, o aviso morre quando o co-op volta, o `state_full` publica |

Linha de base rodada hoje, antes de escrever qualquer plano:

```
$ .venv/bin/python -m pytest tests/unit/test_coop_nao_cai_em_silencio.py \
      tests/unit/test_contagem_um_numero_na_janela.py -q
28 passed in 1.49s
```

## O que FALTA: a janela não consome o fato

```
$ grep -rn "coop_derrubado" src/hefesto_dualsense4unix/app/
(zero linhas)
$ grep -rn "derrubado_por_steam_input" src/ tests/
src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:503   (comentário)
src/hefesto_dualsense4unix/daemon/ipc_handlers.py:1646        (comentário)
src/hefesto_dualsense4unix/daemon/ipc_handlers.py:1661        (a escrita)
tests/unit/test_coop_nao_cai_em_silencio.py:334, :340         (os testes)
```

O daemon grita e ninguém escuta. As duas chaves saem no `state_full` a 10 Hz e
**nenhuma linha da janela as lê**.

Pior: enquanto a suspensão dura, o que a janela mostra é ativamente enganoso, e
isso é medível sem abrir jogo nenhum, só lendo o código:

- `CoopManager.disable()` (`daemon/subsystems/coop.py:1337-1345`) desmonta os
  secundários e **não toca em `coop_enabled`** — então o `state_full` segue
  publicando `coop.enabled = True` com `coop.players = 1`
  (`ipc_handlers.py:1613-1622`). Do lado de fora, isso é indistinguível de "ela
  desligou o co-op": exatamente o que o comentário de `:1639-1644` descreve;
- na aba Início, `coop_prep_hint` (`app/actions/home_actions.py:380-405`) cai no
  ramo final e escreve `COOP_PREP_HINT_CONVITE` (`:361-364`): *"Um clique faz
  tudo: entra no modo de jogo, dá um jogador para cada controle e arruma a
  numeração."* — um convite para clicar, com o jogo segurando o controle
  físico. O ramo "tudo pronto" (`:397-404`) exige `mode_of_state(state) ==
  MODE_GAMEPAD`, e durante a suspensão o modo lido é `MODE_DESKTOP`.

### O caminho está QUENTE — medido no journal dela

Não é defeito teórico à espera de uma noite hipotética. Medido hoje, no journal
da unidade que roda (`journalctl --user -u hefesto-dualsense4unix.service`):

| Janela | `steam_input_excecao_ativada` | `steam_input_vpad_suspenso` | `coop_derrubado_pela_excecao_steam_input` |
|---|---:|---:|---:|
| desde 24/07 | 40 | 26 | **0** |
| desde 28/07 | 20 | 20 | **0** |

Todas com `appid=3357650` — o **Pragmata**, registrado na allowlist dela em
26/07 (`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`, com a nota da
DUPLO-REGISTRO-01 no próprio arquivo). A mais recente:

```
jul 31 01:51:04  steam_input_vpad_suspenso  appid=3357650 flavor=dualsense jogadores_coop=0
```

Duas leituras honestas disso, e as duas mandam nesta sprint:

1. **O co-op nunca caiu** nas 26 suspensões — `jogadores_coop=0` em todas. Ela
   jogou sozinha. O defeito é real e ainda não mordeu, o que confirma a
   priorização do índice de 26/07 (*"a única que não custa nada enquanto você
   joga com um ou dois controles"*) e desmente qualquer urgência de madrugada;
2. **a exceção entra a toda hora** — 20 vezes em três dias. No dia em que os
   quatro estiverem na mesa e ela abrir o Pragmata, os três secundários caem, e
   hoje a janela não tem uma linha para dizer isso. A diferença entre 40
   entradas e 26 suspensões também é dado, e é da E3: em 14 delas a exceção
   estava ativa **sem** vpad suspenso (a suspensão só age se houver vpad ou
   jogador de pé — `gamepad.py:464-470`), que é o segundo dos dois estados que a
   entrega 2 da JOGO-01 precisa distinguir.

## A metade da contagem que ainda não tem dono: a aba Emulação

A conta única da entrega (a) cobre a aba Status, o cabeçalho e a faixa de
números. **Um lugar ficou de fora**, e ele conta outra coisa:

```python
# src/hefesto_dualsense4unix/app/actions/emulation_actions.py:514-522
js_nodes = sorted(glob.glob("/dev/input/js*"))
if js_nodes:
    n = len(js_nodes)
    palavra = "controle detectado" if n == 1 else "controles detectados"
    self._get("emulation_js_label").set_text(f"{n} {palavra} pelo sistema")
```

O rótulo é o `emulation_js_label` do glade (`gui/main.glade:2327`), campo
"Gamepads:" do cartão de diagnóstico, pintado por `_refresh_emulation_view`
(`:481`). Ele conta **nós**, e um controle rende vários.

**Medido agora, na máquina dela, com um DualSense no cabo e a Steam aberta**
(leitura de `/sys`, sem encostar em nada):

| nó | `name` | `uniq` | caminho real |
|---|---|---|---|
| `js0` | `Sony … DualSense Wireless Controller` | `<MAC do controle dela>` | `…/usb3/3-4/3-4:1.3/0003:054C:0CE6.0005/input/input21/js0` |
| `js1` | `Sony … DualSense Wireless Controller Motion Sensors` | **o mesmo MAC** | `…/0003:054C:0CE6.0005/input/input22/js1` |
| `js5` | `Microsoft X-Box 360 pad 1` | (vazio) | `/sys/devices/virtual/input/input61/js5` |

**A aba diz "3 controles detectados pelo sistema" com UM controle na mesa dela.**
Um aparelho dela rende dois nós (o gamepad e os sensores de movimento, mesmo
`uniq`), e o terceiro nó nem é controle: é um gamepad virtual criado por uinput
com a Steam aberta — o `Microsoft X-Box 360 pad` que a **entrega 4 da JOGO-01**
mandou investigar. Nenhum vpad do Hefesto estava de pé no momento da medição
(nenhum nó com nome `Hefesto Virtual`, `integrations/uhid_gamepad.py:661`).

É o "oito" da CONTAGEM-01 vivo, só que hoje dá três.

### A cura existe, e está fora da árvore que roda

`grep -rn "classificar_joysticks|rotulo_gamepads" src/ tests/` devolve **zero**.
As duas funções existem só no commit `0c08e77` da `main` descartada, catalogadas
como **entrega E3** da
[ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md)
(`:376-415`). Lidas hoje com `git --no-replace-objects show 0c08e77` — o `git
show` cru mente neste repositório, que carrega 438 `replace refs` do
`filter-repo` —, elas fazem três coisas:

1. `classificar_joysticks` agrupa **por aparelho** (chave = `uniq`; sem `uniq`,
   o diretório do device HID) e devolve `(físicos, nossos, de outros programas)`;
2. separa "nosso" pela **identidade** — o MAC forjado `02:fe:` do vpad —, e não
   pelo caminho no sysfs, porque desde o BLUEZ-UHID-01 o BlueZ cria o HID dos
   controles Bluetooth **físicos** em `/devices/virtual/misc/uhid/`, o mesmo
   lugar onde mora o nosso vpad;
3. `rotulo_gamepads` diz os dois números: os aparelhos por dono **e** os nós
   crus, para a diferença ser explicada em vez de escondida.

Na mesa medida acima, o rótulo viraria: *"1 controle físico, 1 gamepad virtual
de outro programa (Steam Input) — 3 nós em /dev/input/js*"*.

### E um buraco no porte, que eu medi e o commit de origem não tinha como prever

O `0c08e77` reconhece o vpad por duas assinaturas: `uniq` começando com `02:fe:`
ou nome começando com `Hefesto Virtual`. As duas valem para o vpad **uhid**
(`uhid_gamepad.py:661`). Não valem para o vpad **uinput**, que é o fallback
degradado do VPAD-05:

- máscara xbox: `XBOX360_NAME = "Microsoft X-Box 360 pad (Hefesto -
  Dualsense4Unix virtual)"` (`integrations/uinput_gamepad.py:55`, usado em
  `:121`) — contém "Hefesto", mas **não começa** com "Hefesto Virtual";
- máscara dualsense: `DUALSENSE_EDGE_NAME = "Sony Interactive Entertainment
  DualSense Edge Wireless Controller"` (`:77-79`, usado em `:116`) — **não
  contém "Hefesto" em lugar nenhum**, e um device de uinput não publica `uniq`.

Nos dois casos o aparelho cai no terceiro ramo (`/devices/virtual/input/`) e o
rótulo diria *"1 gamepad virtual de outro programa (Steam Input)"* **sobre o
nosso próprio vpad** — trocando o silêncio de hoje por uma acusação errada.
O porte não é literal: a E2 abaixo carrega essa quarta regra.

## JOGO-01, entrega 2: a pendência declarada DENTRO do código

O código pede esta entrega por escrito, em dois arquivos:

```
# daemon/subsystems/gamepad.py:318-324
Superfície pendente (Entrega 2 da sprint JOGO-01, fora desta frente porque a
GUI está com outro dono): quem for ligar a frase na aba Emulação lê ISTO
junto de `steam_input_excecao_ativa` …

# daemon/ipc_handlers.py:1450-1453
# JOGO-01 (Entrega 2, pendência da docstring de
# `steam_input_vpad_suspenso`): o par que explica "a emulação parece
# desligada com o jogo aberto". Ver `_steam_input_payload`.
"steam_input": self._steam_input_payload(),
```

O dado **já está publicado**: `_steam_input_payload` (`ipc_handlers.py:1221-1248`)
devolve `{"excecao_ativa": bool, "vpad_suspenso": bool}`. E a docstring dele diz,
sem rodeio, o que a janela faz com isso hoje:

> *"`mode_of_state` (app/actions) hoje chama de 'Controlar o PC' exatamente o
> primeiro caso — `stop_gamepad_emulation` zera `config.gamepad_emulation_enabled`
> mesmo com `persist=False` — e deixa CINZA o único botão que curava o problema
> dela."*

Conferido linha a linha, e é isso mesmo:

- o `state_full` publica `gamepad_emulation.enabled` a partir de
  `config.gamepad_emulation_enabled` (`ipc_handlers.py:1534-1537`), que a
  suspensão zerou em memória de propósito (`gamepad.py:451-453`: é o que cala os
  revivedores automáticos enquanto o jogo roda);
- `mode_of_state` (`app/actions/mode_transition.py:233-247`) devolve
  `MODE_DESKTOP`;
- a aba Emulação pinta `Desligado` em cinza
  (`app/actions/emulation_actions.py:707-710`);
- `_sync_gamemode_button` (`:652-681`) desabilita o botão "Modo jogo" e escreve
  a frase de `:671-675`: *"Em 'Controlar o PC' o controle só faz mouse/teclado —
  suspendê-los deixaria o controle sem função nenhuma."* **Com o jogo aberto e
  o controle físico jogando, essa frase é falsa.**

Ou seja: a janela não está calada, está errada — e esteve errada nas 26
suspensões medidas acima.

Há um precedente pronto para copiar, da mesma casa e do mesmo mês: a
EMULACAO-NO-JOGO-01/E1(c) traduziu o vocabulário fechado de `bloqueio` do teclado
em `BLOQUEIO_DO_TECLADO_EM_PORTUGUES` (`emulation_actions.py:145-165`), e o caso
`vpad_suspenso_pelo_steam_input` (`:158-161`, constante em
`daemon/lifecycle.py:296`) já diz a frase certa **para o teclado**:

> *"Ligado, em pausa agora: o jogo assumiu o controle. Não foi desligado — volta
> sozinho quando você fechar o jogo."*

O teclado dela já é honesto nesse estado. O gamepad, não.

> **NOTA DATADA — 07/08/2026: o teclado era honesto sobre a pausa e errado
> sobre a causa.** A frase citada acima **mudou** nesta data. A medição dela de
> 06/08
> ([CONTROLE-SONY-MEDIDO-01](2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
> seção *A INVERSÃO*, **grau MEDIDO**) **refuta** *"o jogo assumiu o controle"*
> como descrição do que acontece num jogo da lista: o jogo assume a **entrada**,
> e a cor e os gatilhos **dela** continuam valendo lá dentro. Quem assume o
> controle inteiro é o jogo que está **fora** da lista.
>
> **A metade que esta seção acerta continua acertando**, e é o precedente que
> ela veio buscar: a frase abre afirmando *"Ligado, em pausa agora"* e promete a
> volta. Foi só a **causa** que passou a ser nomeada — *"neste jogo quem entrega
> o controle é a Steam, e o controle virtual foi recolhido"*.

## A decisão já registrada que esta sprint NÃO trata como lapso

O índice de 26/07 pediu, na seção 4: *"aviso **antes** de entrar na exceção
(…) com Cancelar que cancela de verdade"*, e a validação proposta era *"clica
'Este jogo não funciona': o aviso aparece antes de qualquer coisa acontecer"*.

Só que o código de hoje tem **decisão escrita em sentido contrário**, no handler
desse botão:

```python
# app/actions/daemon_actions.py:1142-1150
def on_steam_game_broken(self, _btn: object = None) -> None:
    """Botão "Este jogo não funciona" — troca a estratégia DESTE jogo.

    Sem diálogo de confirmação de propósito: a ação não fecha nada, não
    edita arquivo da Steam e é reversível (uma linha num txt nosso). O
    que ela custa é o Hefesto sair da frente do jogo — que é justamente o
    que a usuária está pedindo ao clicar.
    """
```

**A decisão está certa no que ela afirma e incompleta no que ela mede.** O que a
ação custa não é só "o Hefesto sair da frente": com o co-op de quatro de pé, o
clique de hoje é a causa remota da queda de P2, P3 e P4 — que acontece minutos
depois, no daemon, na próxima vez que o jogo entrar em sessão
(`sync_steam_input_exception`, `gamepad.py:231-292`, a 1 Hz). Nenhum diálogo é
possível no instante da queda: ali não há usuária no laço, e um modal por cima
de um jogo rodando seria pior que o silêncio.

Duas consequências, e as duas moldam a E1:

1. **o "antes" possível é o clique dela**, não a borda do daemon;
2. **a confirmação só aparece quando existe preço**. Com um controle na mesa
   (`coop.players == 1`), a decisão de `:1146-1150` continua valendo inteira e
   o clique segue direto. Com dois ou mais jogadores de pé, a mesma decisão
   deixa de descrever a realidade — e é aí, e só aí, que se pergunta.

Vale registrar o que a casa **já** paga aqui, para ninguém reescrever: o tooltip
do botão (`gui/main.glade:2148`) é hoje o único texto da tela que diz o preço —
*"enquanto a marca estiver lá, esse jogo fica sem cor, gatilhos e co-op do
Hefesto"* —, e ele nasceu da entrega 4 da BOTÃO-QUE-NÃO-MENTE-01, cujo
comentário no glade (`:2132-2145`) explica por que o texto parou de prometer
desfazer. **Esse comentário envelheceu num ponto**, e a correção é de uma linha
quando alguém passar por lá: ele afirma que `remove_appid_from_steam_input_allowlist`
tem "ZERO chamadores em `src/`", e hoje tem um —
`cli/cmd_steam.py:215`, o comando `gamepad steam-input remove`. O tooltip
continua verdadeiro (não existe **botão**); o comentário, não.

## Entregas

> **NOTA DATADA — 07/08/2026: o PREÇO desta sprint foi remedido, e ele é menor
> do que estas entregas escrevem.** Todas as três falam do estrago como *"o
> Hefesto sai da frente do jogo"* — a docstring citada na E0, a frase *"o que a
> ação custa não é só 'o Hefesto sair da frente'"*, o diálogo proposto na E1b e
> a primeira linha da tabela da E3. A medição dela de 06/08/2026
> ([CONTROLE-SONY-MEDIDO-01](2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
> seção *A INVERSÃO*, **grau MEDIDO**) refutou a metade da saída: num jogo da
> lista os **gatilhos dela seguraram** e a **cor dela ficou**. O que a exceção
> entrega é a **entrada**.
>
> **O que esta sprint acerta, e a medição só reforça:** o preço que ela existe
> para nomear — **a queda de P2, P3 e P4** — é real, é consequência direta de
> recolher os gamepads virtuais, e continua sendo a coisa que ninguém pode
> descobrir sozinho. As três partes obrigatórias do aviso (o número, a negação
> e a promessa de volta) continuam obrigatórias.
>
> **O que caduca, item a item:**
>
> | Onde | O que dizia | O que vale desde 06/08 |
> |---|---|---|
> | E0, a docstring de `on_steam_game_broken` | *"o que ela custa é o Hefesto sair da frente do jogo"* | custa **a entrada** daquele jogo (e, por tabela, o co-op). Já corrigida em `app/actions/daemon_actions.py` |
> | E1b, o diálogo antes do clique | *"Neste jogo o Hefesto sai da frente, e 3 deles saem junto"* | a segunda metade está certa e é o ponto do diálogo; a primeira tem de dizer *"neste jogo quem entrega o controle é a Steam"* |
> | E3, a linha `true`/`true` da tabela | *"O jogo assumiu o controle — o Hefesto saiu da frente deste jogo"* | **invertida.** Quem "assume o controle" da luz e dos gatilhos é o jogo **fora** da lista, não dentro |
>
> **O que já foi feito com esta nota na mão (07/08):** o tooltip do badge —
> `app/actions/status_actions.tooltip_do_coop_derrubado`, que nasceu da E1a —
> deixou de abrir com *"O jogo assumiu o controle"* e passa a nomear a entrada,
> mantendo as três partes obrigatórias. A E1b e a E3 **continuam abertas**, e
> quem as escrever usa a tabela acima.

Ordem por risco crescente. As três são independentes: qualquer uma entra sozinha.

### E1. O aviso na janela, com o preço em palavras — não só o fato

Duas metades, e a ordem entre elas importa.

**E1a — o aviso passivo, enquanto o estrago dura.** Uma função pura
`texto_do_coop_derrubado(bloco_coop) -> str`, no mesmo módulo e no mesmo molde
de `texto_de_contagem` (`status_actions.py:126-154`), lendo as duas chaves que o
daemon já publica. O lugar do texto é o **banner**, pelo precedente exato do
badge de vibração: `status_actions.py:619-629` cria o `_rumble_badge` no
`header_bar` com a justificativa escrita — *"quem está jogando não tem essa aba
aberta e conclui que a vibração quebrou. Aqui ele fica no banner, visível de
qualquer aba"* —, e `_update_rumble_badge` (`:1078-1103`) o sincroniza dentro de
`_render_slow_state` (`:1603`). Um `_coop_badge` irmão custa o mesmo.

O texto tem de dizer o **preço**, não o fato. O fato é "o co-op caiu"; o preço é:

> *"O jogo assumiu o controle: 3 jogadores saíram (P2, P3, P4). Não foi você que
> desligou o co-op — eles voltam sozinhos quando você fechar o jogo."*

As três partes são obrigatórias e cada uma corrige uma mentira medida acima: o
número vem de `secundarios_derrubados` (não de `players`, que já voltou a 1); a
negação desfaz a ambiguidade que `coop.enabled=True` cria; e a promessa de volta
é verdadeira — `resume_vpads_after_steam_input` chama `coop.sync(force=True)`
(`gamepad.py:598-608`), e mesmo pelo caminho manual o ciclo normal do co-op
recria os secundários porque `disable()` não desliga `coop_enabled`
(`coop.py:1337-1345`, `should_be_active` em `:183-189`).

**E1b — a pergunta antes do clique que cobra o preço.** Em
`on_steam_game_broken` (`daemon_actions.py:1142`), antes de chamar
`add_appid_to_steam_input_allowlist` (`:1166-1180`): se o `state_full` corrente
disser `coop.players >= 2`, perguntar uma vez, com o número na frase — *"Você
tem 4 jogadores agora. Neste jogo o Hefesto sai da frente, e 3 deles saem junto
enquanto ele estiver aberto. Marcar assim mesmo?"* — e **Cancelar não escrever
nada**. Com `players == 1`, nada muda: nenhum diálogo, um clique só, exatamente
como `:1146-1150` decidiu.

**Aceite (E1a):** com o daemon publicando `coop.derrubado_por_steam_input =
true` e `secundarios_derrubados = 3`, o banner mostra o número **3** e as
palavras "voltam sozinhos", de qualquer aba; assim que a chave volta a `false`,
o banner some no mesmo tique — sem reiniciar a janela.
**Aceite (E1b):** com dois ou mais jogadores, o clique não escreve na allowlist
antes da resposta dela, e "Cancelar" deixa o arquivo byte a byte igual. Com um
jogador, o clique escreve direto, sem diálogo.

**Mordida.** Cinco mutações, todas com o teste pronto para reprovar:

1. fixar a leitura de `derrubado_por_steam_input` em `False` — o caso com 3
   derrubados tem de reprovar por ausência da frase;
2. trocar `secundarios_derrubados` por `coop.players` — o texto diria "1" (o
   `players` volta a 1 no tique seguinte, que é o defeito original); o teste
   exige "3" e reprova;
3. arrancar o ramo que esconde o badge — alimentar `derrubado_por_steam_input =
   false` e exigir badge oculto; sem o ramo, o aviso fica pendurado depois de o
   co-op voltar, que é exatamente o que as duas mortes do contador
   (`gamepad.py:565-579` e `:1401-1411`) existem para impedir;
4. trocar a frase por uma que diga só o fato ("o co-op caiu") — o teste de
   vocabulário exige as palavras do preço e da volta, no molde de
   `BLOQUEIO_DO_TECLADO_EM_PORTUGUES`;
5. (E1b) arrancar o gate e voltar a escrever direto — com o dublê de escrita
   registrando as chamadas, o teste com 4 jogadores exige **zero** chamadas
   quando a resposta é "não", e reprova. E o simétrico: fazer a pergunta
   **sempre**; o teste com 1 jogador exige escrita imediata e reprova.

A parte pura (o texto) mora em teste **sem GTK**, no molde de
`test_coop_nao_cai_em_silencio.py`, que declara no cabeçalho por que não importa
`gi` (`:15-16`); a fiação do widget vai no arquivo com `exigir_gi_real`
(`test_contagem_um_numero_na_janela.py:30-35`), pela regra GUARDA-GI-REAL-01.

**Risco:** baixo no dado, médio na palavra. Nenhuma linha da lógica de queda é
tocada — e não pode ser: o cabeçalho do teste (b) registra que "mexer no gatilho
encosta na exceção de Steam Input, que é o caminho do defeito do R1 curado na
onda 2". O risco real é a frase: ela é texto na tela dela, então **E1 não vira
commit sem o olho dela** (PROVA-DE-TELA-01).

### E2. A contagem honesta na aba Emulação

Porte de `classificar_joysticks`, `_atributos_do_joystick` e `rotulo_gamepads` do
`0c08e77` para `app/actions/emulation_actions.py`, substituindo `:514-522`.
**É a mesma entrega que a E3 da ÁRVORE-DIVERGENTE-01** (`:376-415`) — quem
executar, executa uma vez, e este parágrafo é o ponteiro para não fazer duas.

Duas coisas que este documento acrescenta ao porte:

- **a quarta regra**, medida acima: um vpad em uinput (fallback VPAD-05) não tem
  `uniq` e pode não ter "Hefesto" no nome (`uinput_gamepad.py:55` e `:77-79`).
  A classificação precisa reconhecer as três assinaturas de vpad que o projeto
  publica, não duas — senão troca o silêncio por uma acusação errada;
- **o teste vai em arquivo NOVO**, nunca o `test_contagem01_uma_contagem_so.py` <!-- ref-externa: vive só em 0c08e77, na main descartada; a ausência nesta árvore é o assunto do item -->
  inteiro do commit de origem: são 796 linhas que cobrem também o que já foi
  curado pela metade (a) desta sprint, e conflitariam.

**Aceite:** com a mesa de hoje (um DualSense no cabo, a Steam aberta, nenhum
vpad de pé) a aba diz *"1 controle físico, 1 gamepad virtual de outro programa
(Steam Input) — 3 nós em /dev/input/js*"*, e nunca mais "3 controles detectados
pelo sistema". Com o vpad do Hefesto de pé, ele aparece na coluna do Hefesto —
nos **dois** backends, uhid e uinput.

**Mordida.** Cinco mutações que têm de reprovar:

1. tirar o agrupamento por aparelho: `js0` e `js1` (mesmo `uniq`) voltam a
   contar 2 e o teste reprova;
2. trocar o prefixo `02:fe:` por outro: o vpad uhid vira "físico";
3. fazer o aparelho desconhecido cair em "nosso" em vez de "físico" — a leitura
   conservadora é o inverso, e inflar o que dizemos ter criado é o defeito;
4. arrancar a quarta regra: alimentar um nó com
   `name=DUALSENSE_EDGE_NAME`, `uniq=""` e caminho sob `/devices/virtual/input/`
   e exigir "nosso"; sem ela o classificador do `0c08e77` responde "de outro
   programa (Steam Input)" e reprova;
5. no rótulo: com nós > 0 e nenhum aparelho físico, o texto **não** pode dizer
   "controles detectados pelo sistema".

**Risco:** baixo. É rótulo de diagnóstico, sem efeito sobre o daemon. O risco
declarado é sobrecontar de novo, e a segunda metade do rótulo (os nós crus) é o
que impede: ela explica a diferença em vez de escondê-la.

### E3. A superfície da exceção de Steam Input (JOGO-01, entrega 2)

Traduzir o par que o daemon já publica (`ipc_handlers.py:1221-1248`) em frase, no
molde do vocabulário fechado do teclado (`emulation_actions.py:145-165`). Três
estados, três frases, e o par distingue os dois primeiros:

| `excecao_ativa` | `vpad_suspenso` | o que a aba Emulação diz hoje | o que precisa dizer |
|---|---|---|---|
| `true` | `true` | `Desligado` (cinza) | *"O jogo assumiu o controle — o Hefesto saiu da frente deste jogo. Não foi desligado; volta sozinho quando você fechar o jogo."* |
| `true` | `false` | `Ligado — DualSense (PS)` | *"Este jogo é entregue pela Steam, mas o gamepad virtual continua de pé — o jogo pode ver dois controles."* |
| `false` | `false` | o que já diz | nada muda |

Junto, três consertos do mesmo estado, todos medidos acima:

- a frase falsa do "Modo jogo" (`_sync_gamemode_button`, `:671-675`) não pode
  afirmar *"Em 'Controlar o PC' o controle só faz mouse/teclado"* durante a
  exceção;
- a dica de co-op da aba Início (`home_actions.py:380-405`) não pode convidar
  para "um clique faz tudo" com o jogo segurando o controle;
- e o preço do gesto manual. Um clique em "DualSense (PS)" nesse estado passa
  pelo IPC com `origin="manual"` (`lifecycle.py:1190-1196`, chamado por
  `ipc_handlers.py:2859`) e cai no ramo `gamepad.py:1392-1411`: o vpad volta na
  hora e a exceção morre. O próprio código diz o preço — *"o preço — este jogo
  volta a ver dois dispositivos — é escolha dela, e fica no journal"* (`:1395-1397`).
  Fica no journal, e **não** na tela: hoje o toast responde "Gamepad DualSense
  ligado — o jogo mostra os botões da Sony" (`emulation_actions.py:804-809`),
  sem uma palavra sobre o que ela acabou de desfazer.

**Aceite:** com o Pragmata aberto (o appid que a allowlist dela já tem), a aba
Emulação **não** diz "Desligado" e o botão "Modo jogo" não afirma que o controle
só faz mouse e teclado; fechado o jogo, as frases voltam ao que eram sozinhas.
Com o par `(true, false)`, a frase é **outra** — os dois estados nunca colapsam
num texto só.

**Mordida.** Quatro mutações que reprovam:

1. arrancar a leitura de `steam_input` do estado: com `excecao_ativa=true`,
   `vpad_suspenso=true` e `gamepad_emulation.enabled=false`, o rótulo volta a
   "Desligado" — o teste exige o contrário;
2. colapsar os dois casos numa frase só: o teste compara os dois textos e exige
   que difiram;
3. arrancar o ramo novo da dica do "Modo jogo": a frase de `:671-675` reaparece
   durante a exceção e reprova;
4. arrancar o aviso do gesto manual: o toast volta a ser só "Gamepad DualSense
   ligado" e o teste de vocabulário reprova.

O miolo é função pura (recebe o dict, devolve `(bool | None, str)`) no molde de
`descrever_teclado_emulado` (`:173-192`) — testável sem montar janela, que é a
razão de aquela função existir assim.

**Risco:** médio. É a entrega que mais muda o que ela lê num momento em que ela
está jogando, e é a que mais depende de palavra. Também é a que tem o retorno
mais alto por linha: aconteceu 26 vezes em uma semana. **Não entra sem o olho
dela** (PROVA-DE-TELA-01), com foto da aba Emulação com o jogo aberto e com o
jogo fechado.

## Como você valida na tela

De olho, sem terminal. Duas rodadas, porque o defeito tem dois tamanhos.

**Rodada de um controle — dá para fazer agora, com o que está ligado:**

1. Aba **Emulação**, cartão de diagnóstico, campo "Gamepads:". Hoje ele diz
   **"3 controles detectados pelo sistema"** com um controle na sua mesa. Depois
   da E2 ele diz quantos aparelhos são seus, quantos são nossos e quantos são de
   outro programa — e termina dizendo quantos nós existem, que é o número de
   hoje, explicado.
2. Abra o **Pragmata**. Enquanto ele estiver aberto, olhe a aba **Emulação**:
   hoje ela diz "Desligado" e o botão "Modo jogo" fica cinza afirmando que o
   controle "só faz mouse/teclado". Depois da E3, ela diz que o jogo assumiu o
   controle e que volta sozinho quando você fechar.
3. Feche o jogo e confira que as frases voltam ao normal **sozinhas**, sem você
   clicar em nada.

**Rodada de quatro controles — é onde a sprint cobra:**

4. Ligue os quatro e monte o co-op pela aba Início até ela dizer "4 controles =
   4 jogadores".
5. Abra o **Pragmata**. Hoje: os três jogadores extras somem e nada na janela
   diz uma palavra. Depois da E1a, o banner — visível de **qualquer** aba —
   avisa que 3 jogadores saíram, que não foi você e que eles voltam.
6. Feche o jogo. Os três voltam, e o aviso **some junto**. Aviso que sobrevive
   ao retorno é defeito novo.
7. Com os quatro de pé e sem jogo aberto, clique em **"Este jogo não funciona"**
   (aba Sistema). Depois da E1b, aparece uma pergunta com o número de jogadores
   na frase. Clique em **Cancelar** e confira, na aba Sistema, que nada foi
   marcado.
8. Repita o passo 7 com **um** controle só: aí não pode aparecer pergunta
   nenhuma — um clique, e pronto. É a decisão que já estava escrita e que esta
   sprint preserva.

## O que fica de fora, por escrito

- **O desfazer dentro da janela.** É a entrega 3 da JOGO-01 e a pendência
  declarada da STEAM-INPUT-01 no índice de 30/07 (`:193`, faixa 2). A função
  existe (`integrations/steam_launch_options.py:821`) e hoje só é chamada por
  `cli/cmd_steam.py:215`. O "Cancelar" da E1b cancela **antes** da escrita, que
  é barato; desmarcar depois é outra sprint, e roubá-la aqui deixaria as duas
  pela metade.
- **Mudar a lógica da queda.** Nenhuma linha de `suspend_vpads_for_steam_input`
  entra nesta sprint. O co-op cai porque tem de cair — o princípio da JOGO-01 é
  "um controle físico produz exatamente UM dispositivo de jogo"
  (`gamepad.py:428-434`). O que falta é a usuária saber.
- **Um modal no instante da queda.** Não existe usuária no laço ali: a borda é
  do daemon, na reconciliação de 1 Hz, com o jogo já rodando. Aviso passivo no
  banner (E1a) e pergunta no gesto dela (E1b) são as duas superfícies possíveis.
- **`_format_players_hint` (`home_actions.py:325-342`).** Ela escreve `"{N}
  controles = {M} jogadores"` com `N = len(controllers)`, que conta só os
  adotados — então com 2 DualSense e 2 externos a aba Início diz "2 controles" ao
  lado de um cabeçalho que diz "2 do Hefesto + 2 externos". Não é o defeito
  antigo (jogador **é** só quem tem vpad, e a função só fala quando o daemon
  numerou dois jogadores distintos — `:329-331`), é a mesma palavra com dois
  denominadores. A cura é de uma linha e cabe na próxima leva que abrir esse
  arquivo: nomear o número, `"2 controles do Hefesto = 2 jogadores"`. Fica
  registrado aqui para não se perder de novo.
- **Os `Microsoft X-Box 360 pad` da Steam.** A entrega 4 da JOGO-01 pergunta se
  são resíduo ou consequência normal. Medi **um** hoje, com a Steam aberta e
  nenhum jogo rodando (`js5`, `/sys/devices/virtual/input/input61`). É dado para
  aquela entrega, não é a resposta dela — e a E2 daqui só precisa classificá-lo
  certo, não explicá-lo.
- **O applet COSMIC, a janela compacta e a bandeja.** As três leem o mesmo
  `state_full` e nenhuma foi medida por esta sprint. Se o aviso do co-op tiver de
  chegar lá, é sprint de radar própria (a mesma que o índice desta rodada propõe
  para SEGUNDA-JANELA-01).

## O que eu não medi

- **A queda do co-op ao vivo.** Nas 26 suspensões do journal, `jogadores_coop=0`
  em todas — ela jogou sozinha. Tudo que este documento afirma sobre o caminho
  de quatro jogadores vem do código lido hoje e dos 28 testes verdes, não de uma
  noite observada. Quando a E1 for validada, ela precisa ser validada **com os
  quatro**, e é o passo 5 do roteiro acima.
- **A aparência do banner com o badge de vibração aceso ao mesmo tempo.** Os dois
  moram no mesmo `header_bar` (`status_actions.py:617` e `:628`) e podem
  coexistir; a LARGURA-01 mediu que a barra de abas e o rodapé têm orçamento
  próprio, mas ninguém mediu dois badges juntos na escala de fonte dela.
- **Quantos nós o co-op de quatro produz.** A tabela de `/dev/input/js*` acima é
  de um controle. Com quatro controles e quatro vpads o número cresce, e o
  aceite da E2 foi escrito para a mesa de hoje — quem executar deve remedir com
  os quatro antes de fixar o teste.
- **Se a frase da E1 é a frase certa.** Escrevi três; a escolha das palavras é
  dela. O documento fixa o que a frase precisa **conter** (o número dos
  secundários, a negação de "você desligou" e a promessa de volta), não o texto
  final.
- **O caminho de pacote.** Toda a medição é da árvore de trabalho em
  `restauro/inicio-da-sessao`, HEAD `7bd0cb7`. A cópia instalada em
  `~/.local/share/hefesto-dualsense4unix/` não foi conferida linha a linha.

---

## NOTA DATADA (09/08/2026) — o aviso existe desde o dia em que esta sprint foi agendada

Conferido no código de hoje. **O texto acima não foi reescrito.**

O relógio é o achado. O
[índice das ondas de 31/07](2026-07-31-INDICE-as-ondas-depois-da-auditoria.md)
entrou em `23c7c94` às **09:43:57** e agendou o item 2.6 como *"o fato já é
emitido pelo daemon; falta a janela mostrar"*. O banner entrou em `cd5eaf1` às
**09:47:19** — **três minutos e vinte e dois segundos depois**. A sprint e o
índice passaram nove dias dizendo que faltava o que já estava de pé.

| entrega | veredito | onde está hoje | commit |
|---|---|---|---|
| **E1** — o aviso na janela, com o preço em palavras | **ENTREGUE** | `app/actions/status_actions.py:257` `texto_do_coop_derrubado`; o rótulo nasce em `:1173-1182` (`_coop_badge`, no banner, visível de qualquer aba) e é atualizado por `_update_coop_badge` (`:1659`), chamado em `:2187`. O ramo que **esconde** é tão testado quanto o que mostra (`:1662`) | `cd5eaf1` 31/07/2026 |
| **E2** — a contagem honesta na aba Emulação | **ENTREGUE** | `app/actions/emulation_actions.py:48` — o campo "Gamepads:" parou de contar **nó** (`glob("/dev/input/js*")`, que dizia SEIS com um controle no cabo) e passou a contar **aparelho** | `cd5eaf1` 31/07/2026 |
| **E3** — a superfície da exceção de Steam Input | **ABERTA** | há uma superfície (`app/actions/emulation_actions.py:1380` `_steam_input_excecao_status`, consumida em `:1427`), mas ela é **anterior a esta sprint** — `git log -S` a data em `f191564`, **24/07/2026**, uma semana antes de a sprint ser escrita. Ou seja: o que existe hoje é o que já existia quando a E3 foi pedida |

Os testes que mordem: `tests/unit/test_coop_derrubado_aparece_no_banner.py`
(E1), `tests/unit/test_contagem_um_numero_na_janela.py`,
`tests/unit/test_contagem_emulacao_conta_aparelho.py` e
`tests/unit/test_contagem_emulacao_largura_do_rotulo.py` (E2).

### O grau, como manda a casa

**MEDIDO** para E1 e E2 — símbolo, chamador, teste, commit e hora.
**MEDIDO por datação** para a E3 estar aberta: a superfície citada é mais velha
que o pedido.

**SEM PROVA** para o efeito na tela dela: ninguém viu o banner aparecer numa
partida de verdade. É interface, e por PROVA-DE-TELA-01 a palavra final é dela.
