# PERFIL-JOGO-01 — as configurações que ela deixou somem quando o jogo abre

- **Status:** ABERTA
- **Prioridade:** CRÍTICA — é a queixa que motivou o rollback da leva da
  madrugada de 26/07. Desfaz trabalho dela, sozinho, no pior momento possível
- **Aberta em:** 26/07/2026, depois de ela olhar a tela e pedir o rollback

## O relato dela

> *"agora na hora de jogar o jogo o perfil do controle muda e sai as configs que
> eu deixei"*

E, na mesma leva de queixas:

> *"interface tá quebrada e na hora do jogo tá um caos legal"*

## Aviso de honestidade, antes de qualquer coisa

**A causa não está isolada.** Existe um defeito medido, com hora, no journal da
máquina dela — e ele explica *uma* das coisas que somem. Mas **não consegui
provar** que o que ela chama de "o perfil muda" seja esse defeito: pode ser o
número do jogador, pode ser a cor, podem ser os gatilhos, pode ser o nome do
perfil trocando na janela. São quatro sintomas diferentes com causas diferentes,
e a frase dela cabe em todos.

Esta sprint registra o que foi medido, diz explicitamente o que ficou de fora, e
propõe o experimento que separa os quatro. **Uma sprint que finge saber a causa é
pior do que uma sprint honesta**: fecharia o caso no defeito errado e deixaria o
verdadeiro no ar.

## O que foi medido — o defeito que existe e tem hora

### O código que mudou na madrugada

Na `main` (leva da madrugada), o portão de autoridade de saída deixou de ser
tudo-ou-nada e passou a proteger **só a cor**:

```
core/backend_pydualsense.py:122    _GAME_LAYER_GATED_FIELDS = frozenset({"led"})
core/backend_pydualsense.py:1183   _game_layer_admitida(...)
core/backend_pydualsense.py:1277   admitida = self._game_layer_admitida(game)
core/backend_pydualsense.py:2877   set_game_output_for(...)
core/backend_pydualsense.py:2949   log "game_output_retido_sem_jogo"
core/backend_pydualsense.py:2971   log "game_output_aplicado"
```

Consequência direta: sob autoridade `daemon` — ou seja, **sem jogo reconhecido**
— a camada do jogo não é mais barrada inteira. A cor fica retida, mas o
`player_leds` que o cliente Steam escreve **passa por cima** da camada do co-op e
da camada dela (a que R-20 criou para o que a usuária configura) e vai para o
hardware na hora.

### O journal da máquina dela, 26/07

```
02:49:26  game_output_aplicado        campos=['player_leds'] destino=sysfs_preferido uniq=143a9a13ebab
02:49:26  game_output_retido_sem_jogo campos=['led']                                 uniq=143a9a13ebab
02:49:26  game_output_aplicado        campos=['player_leds'] destino=sysfs_preferido uniq=a0fa9cc311f0
02:49:26  game_output_retido_sem_jogo campos=['led']                                 uniq=a0fa9cc311f0
03:04:19  game_output_aplicado        campos=['player_leds','led'] ...
03:09:08  game_output_aplicado        campos=['player_leds','led'] ...
```

No **mesmo milissegundo** o daemon reteve a cor por não haver jogo, e escreveu o
número do jogo no controle físico dela. Isso é literalmente "saiu a config que eu
deixei" — para o número, que PLAYER-01 acabara de tornar coisa dela.

### O discriminador que data o rollback

Em `main`, `player_leds` **não pode** aparecer como retido, porque não está no
conjunto de `backend_pydualsense.py:122`. Logo estas duas linhas só podem ter
sido escritas pelo código do rollback:

```
03:24:09  game_output_retido_sem_jogo campos=['player_leds'] uniq=143a9a13ebab
03:27:29  game_output_retido_sem_jogo campos=['player_leds'] uniq=143a9a13ebab
```

Isto data a troca sem inferência: a `main` esteve no ar de ~02:49 a ~03:23, e o
rollback entrou entre 03:23 e 03:26 — o que bate com o mtime de
`~/.config/hefesto-dualsense4unix/profiles/.seeded_presets` (26/07 03:26).

**O rollback cura este defeito.** Se a queixa 2 dela sumir com o rollback no ar,
era isto. Se persistir, não era — e as duas seções seguintes dizem onde ela mora.

## O que foi descartado, com a medição que descarta

### O autoswitch NÃO trocou de perfil na madrugada

Os arquivos que decidem qual perfil vale são **byte-idênticos** entre `4dd4652`
(rollback) e `main` (madrugada):

```
git diff --stat 4dd4652 main -- \
  src/hefesto_dualsense4unix/profiles/ \
  src/hefesto_dualsense4unix/daemon/subsystems/autoswitch.py \
  src/hefesto_dualsense4unix/app/draft_config.py \
  src/hefesto_dualsense4unix/daemon/subsystems/game_signal.py
→ saída vazia
```

E no journal, de 25/07 18:00 até agora, há **um único** `profile_autoswitch`:
25/07 21:19:51, `to=sackboy_nativo`, pela regra antiga do próprio jogo. Todas as
outras janelas de jogo registraram `autoswitch_congelado_pelo_cadeado` com
candidato **vazio** — o cadeado dela segurou. Nenhum `profile_activated` na
madrugada.

Ou seja: **o rollback não pode ser a cura de uma troca de perfil**, porque a
troca de perfil não mudou de comportamento entre os dois commits.

### O efeito colateral da numeração é cosmético

`daemon/subsystems/coop.py:1431-1436` (na `main`): com o co-op desligado, só o
controle primário recebe `player=1`; os demais viram `None`. Único consumidor:
`daemon/ipc_handlers.py:1350`, que é o rótulo do cartão. Não toca em perfil nem
em saída para o hardware.

## Os dois defeitos que o rollback NÃO cura — e nasceram ANTES da madrugada

Estes dois estão **dentro** do rollback. Se a queixa continuar, é aqui.

### 1. O cadeado cede a perfil casado por título de janela

`profiles/autoswitch.py:252-261`: o cadeado ("não trocar sozinho", que ela pediu
em 24/07) agora cede não só à regra própria do jogo, mas também a qualquer perfil
que **declare** ser de jogo:

```python
if not (
    perfil_e_regra_de_jogo(profile, info)
    or perfil_declara_modo_de_jogo(profile)
):
```

E `profiles/loader.py:384` (`migrate_modo_jogo_nos_presets`) **reescreveu os
presets dela em disco** — cinco arquivos com mtime **25/07 18:28**, cada um
carregando agora `"mode": {"kind": "gamepad", "gamepad_flavor": "xbox"}`:

```
~/.config/hefesto-dualsense4unix/profiles/fps.json
~/.config/hefesto-dualsense4unix/profiles/acao.json
~/.config/hefesto-dualsense4unix/profiles/aventura.json
~/.config/hefesto-dualsense4unix/profiles/corrida.json
~/.config/hefesto-dualsense4unix/profiles/esportes.json
```

O marcador `.modo_jogo_nos_presets_migrated` é do mesmo minuto.

Esses presets casam por `window_title_regex` **frouxo** — `|Metro)`, `|Control)`,
`|LEGO |`, `|Portal 2|`. Existe, portanto, um caminho em que o cadeado cede a um
perfil casado só pelo título da janela e o `manager.activate`
(`profiles/autoswitch.py:547`) reaplica gatilhos, LEDs e emulação por cima do que
ela deixou — inclusive trocando a máscara para **xbox**.

**Não disparou no journal desta janela.** É risco identificado por leitura, não
causa medida. Data de nascimento: commit `54f1f3b`, 25/07 18:29, confirmado
ancestral de `4dd4652` por `git merge-base --is-ancestor`.

### 2. O modo jogo liga e solta sozinho a cada alt-tab

`profiles/autoswitch.py:237` chama `_sincronizar_modo_jogo_padrao` **antes** do
cadeado, de propósito, e `daemon/lifecycle.py:1812` diz por escrito que "o
cadeado de autoswitch não é consultado". Medido, com flapping:

```
26/07 03:06:36  profile_mode_aplicado   origin=game_signal kind=gamepad wm_class=steam_app_3357650
26/07 03:07:23  modo_jogo_padrao_solto  motivo=janela_fora_do_jogo wm_class=steam
26/07 03:08:06  profile_mode_aplicado   ...
26/07 03:08:26  modo_jogo_padrao_solto  ...
26/07 03:09:08  profile_mode_aplicado   ...
```

Toda vez que o foco volta para a janela da Steam o Hefesto **solta** o modo; volta
ao jogo, **aplica** de novo. Nesta máquina os efeitos foram brandos
(`ligou_gamepad=False`, `desligou_gamepad=False`, `flavor=dualsense`), mas esta é
a assinatura mais próxima de *"na hora do jogo tá um caos"* — e está no rollback.

## O experimento que isola a causa

Enquanto não soubermos **qual** dos quatro sintomas ela chama de "o perfil muda",
qualquer correção é chute. O experimento abaixo separa os quatro em uma sessão de
jogo, e ela só precisa abrir o jogo — a leitura é nossa.

1. **Antes de abrir o jogo**, anotar o estado visível: nome do perfil na janela,
   número do controle, cor da lightbar, e uma configuração de gatilho que ela
   reconheça.
2. Abrir o jogo. **Não** alt-tabar ainda.
3. Perguntar a ela, com estas quatro perguntas separadas — não "mudou?", mas *o
   que* mudou:
   - o **nome do perfil** na janela do Hefesto virou outro?
   - o **número** do controle (o LED de jogador) virou outro?
   - a **cor** virou outra?
   - os **gatilhos** ficaram diferentes na mão?
4. Alt-tab para a Steam e de volta ao jogo, duas vezes. Repetir as quatro
   perguntas. Este passo separa o defeito 2 (flapping do modo) de todos os
   outros: só ele acompanha o alt-tab.
5. Ler o journal do usuário da janela inteira, procurando os quatro eventos que
   já existem e são discriminantes:

   | evento no journal | significa |
   |---|---|
   | `profile_autoswitch` / `profile_activated` | o perfil trocou de verdade |
   | `autoswitch_cadeado_cedeu_a_regra_de_jogo` | o cadeado cedeu (defeito 1) |
   | `profile_mode_aplicado` / `modo_jogo_padrao_solto` | o modo ligou/soltou (defeito 2) |
   | `game_output_aplicado` com `player_leds` | o jogo escreveu o número (defeito da madrugada) |

6. Se a resposta for **gatilhos**, nenhuma das causas acima explica: o gatilho de
   jogo (`set_game_trigger_for`) tem comportamento idêntico nos dois commits, e a
   investigação recomeça daí.

Este experimento é a **entrega zero** desta sprint. Nada deve ser corrigido antes
dele.

## Entregas

1. **Rodar o experimento acima e nomear o sintoma.** Sem isso, as entregas 2 a 6
   são apostas. O resultado entra nesta sprint, com hora e linhas de journal.
2. **O número dela nunca é sobrescrito sem autoridade de jogo.** Quando o portão
   estiver fechado, `player_leds` da camada do jogo é retido junto com a cor — a
   correção certa não é "voltar tudo", é o portão valer para todo campo que a
   usuária pode definir. Com um teste que **morde**: chamar `set_game_output_for`
   com `led` **e** `player_leds` sob `_game_wins() == False` e afirmar que o
   número **não** chega ao `_write_partial_output`. Arrancar a cura tem de
   reprovar o teste.
3. **O cadeado deixa de ceder a perfil casado por título.** Ceder à regra própria
   do jogo é o que ela pediu; ceder a um preset genérico que casa `|Portal 2|` no
   título não é. `profiles/autoswitch.py:261` volta a exigir a regra do jogo, ou
   ganha um critério que ela consegue enxergar e desligar.
4. **O modo jogo para de soltar no alt-tab.** Voltar o foco para a janela da
   Steam não é sair do jogo. `profiles/autoswitch.py:237` +
   `daemon/lifecycle.py:1812` precisam de histerese, ou de tratar a janela da
   Steam como parte da sessão de jogo.
5. **A tela diz quando alguém mexeu no que ela deixou.** Hoje o perfil, o modo, o
   número e a cor mudam em silêncio. Qualquer escrita por cima da camada dela
   tem de aparecer na janela, com quem escreveu e por quê — "o jogo pediu o
   número 3", "o preset FPS entrou pelo título da janela". Sem isso, ela só
   descobre jogando.
6. **Desfazer a migração de 18:28 nos presets dela, ou assumi-la.** Os arquivos
   em `~/.config/hefesto-dualsense4unix/profiles/` continuam com
   `mode: gamepad, flavor: xbox` gravados em disco. **Reverter código não reverte
   arquivo de configuração** — isso precisa de decisão dela, não nossa.

## Como validar

Tudo abaixo é olhando a tela, com o controle na mão.

1. Com o Hefesto aberto, configurar uma coisa reconhecível: um gatilho, uma cor,
   um número de jogador.
2. Abrir um jogo da Steam. **Nada** do que ela configurou muda na janela nem no
   controle.
3. Alt-tab para a Steam e de volta ao jogo, três vezes. Nada muda em nenhuma das
   idas e voltas.
4. Fechar o jogo. Nada muda.
5. Abrir um jogo cujo título case com um dos presets (`Portal 2`, por exemplo).
   O perfil **não** troca sozinho, porque o cadeado está ligado.
6. Se em algum momento alguma coisa mudar, a janela **diz o que mudou e quem
   mudou** — em vez de ela descobrir pelo controle.

**Critério que resume:** nada que ela configurou pode mudar sem que ela mande —
e se o jogo mandar, a tela tem de dizer que foi o jogo.

## O que NÃO foi medido

- **Não sei qual sintoma ela chama de "o perfil muda".** É a lacuna central desta
  sprint, e a entrega 1 existe para fechá-la.
- **Não abri nenhum jogo.** Nada aqui foi observado com sessão de jogo em
  andamento; a prova é journal da máquina dela, não experimento controlado.
- **Não reproduzi por teste.** O teste que mordia — `set_game_output_for` com o
  portão fechado — não foi escrito. Está na entrega 2.
- **Não vi a tela.** Não houve captura nesta sessão; toda afirmação sobre a
  janela vem de código, não de renderização.
- **Não sei se algum jogo dela roda fora da Steam.** É exatamente onde o defeito
  1 (cadeado cedendo por título) tem maior chance de disparar, e é o falso
  positivo conhecido do sinal de jogo.
