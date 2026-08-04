# POSSE-POR-CONTROLE-01 — a trava de um controle congela os quatro

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA** — um dos quatro defeitos aqui é **consequência do
  trabalho que está na árvore agora, não commitado**, e é melhor descobri-lo
  antes do commit do que depois
- **Faixa:** 2 — a configuração dela deixa de valer sem que nada avise
- **Causa-raiz:** **PROVADA no código** nos quatro casos
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **História:** esta casa já tem registrado *"a config que eu deixo nunca é
  respeitada"* — três escritores do perfil sem dono, curado em 23/07 pelo merge
  por campo com dono declarado. **Esta sprint é o mesmo defeito no eixo que
  aquela cura não cobriu: o eixo CONTROLE A CONTROLE.**

---

## O que os quatro casos têm em comum

O modelo de precedência de saída (`core/backend_pydualsense.py:273-341`) é
**por campo e por MAC** — seis camadas, cada campo com dono registrado. É bom, é
caro, e funciona.

**Mas quatro caminhos escapam dele e agem globalmente.** Com um controle na mesa
isso é invisível: "global" e "aquele controle" são a mesma coisa. Com quatro, é
a diferença entre o produto obedecer e o produto surpreender.

---

## Defeito 1 — a trava manual é global (mexeu no controle 3, congelou os quatro)

**Os dois lados:**

- **quem arma:** `daemon/state_store.py:102` —
  `manual_override_categories` é um `set[str]` **único**, sem TTL e **sem chave
  por MAC**. Armado por `daemon/ipc_handlers.py:735` (`led.set`) e
  `daemon/ipc_handlers.py:783` (`led.player_set`);
- **quem obedece:** `profiles/manager.py:342-346` —
  `led=None if "led" in travadas else effective.lightbar`. E `None` significa
  *"não mexe"* para **todos** os controles.

**O que ela veria:** *"mudei só a cor do controle 3, e desde então nenhum perfil
pinta nenhum controle"*.

**Duração:** permanente. Só sai por troca **manual** de perfil
(`daemon/ipc_handlers.py:412`), hotkey (`daemon/subsystems/hotkey.py:163`) ou
autoswitch (`profiles/autoswitch.py:508`).

**Por que já funcionava:** com um controle, "global" e "aquele controle"
coincidem. A granularidade por **categoria** (ONDA-U/F1) resolveu o eixo
aba-a-aba; ninguém abriu o eixo controle-a-controle.

---

## Defeito 2 — o `led.set` sem `uniq` carimba a camada da USUÁRIA nos quatro

**ATENÇÃO: este defeito está na árvore AGORA, não commitado**
(`daemon/ipc_handlers.py`, a função `_registrar_em_todos`). Ele é o **preço** da
cura `BROADCAST-QUE-NÃO-MENTE-01`, que resolveu um defeito real: `led.set` sem
`uniq` respondia `{"status": "ok"}` e o sysfs não mudava.

**Os dois lados:**

- **quem carimba:** `daemon/ipc_handlers.py:717` chama `_registrar_em_todos`,
  que percorre todos os conectados chamando `apply_output_for`
  (`daemon/ipc_handlers.py:605-607`); e `apply_output_for` faz
  `self._stamp_owner_locked(alvo, fields, _LAYER_USER)`
  (`core/backend_pydualsense.py:2627`);
- **quem obedece:** `core/backend_pydualsense.py:2729-2731` — o perfil só ocupa
  slot **vago**:
  ```python
  if getattr(override, nome) is not None:
      adiados.setdefault(alvo, []).append(nome)
      continue
  ```

**O que ela veria:** *"rodei `hefesto test lightbar` uma vez e depois disso os
perfis pararam de mudar a cor de qualquer controle — e a paleta automática por
jogador morreu junto"*.

**A cura não deve ser revertida.** O defeito que ela conserta é pior (um "ok"
que mente). O que falta é: **um broadcast tem de registrar na camada de
broadcast, não na camada de cada um.** Hoje ele desce um nível de granularidade
que não foi pedido, e com isso muda o alcance da camada da usuária de 1 para N.

---

## Defeito 3 — o rumble do jogo obedece ao seletor da janela

**Os dois lados:**

- **o alvo por MAC:** `daemon/subsystems/gamepad.py:756-763` chama
  `set_rumble_for(target_uniq, ...)`, que devolve `False` quando o MAC não casa
  handle nenhum (`core/backend_pydualsense.py:2870-2874`);
- **o fallback:** `daemon/subsystems/gamepad.py:765-766` chama
  `controller.set_rumble(...)` → `core/backend_pydualsense.py:2178`
  (`self._for_each(_do, what="set_rumble")`) **sem `broadcast=True`** →
  `core/backend_pydualsense.py:1996-1999`:
  ```python
  if not broadcast and target is not None and target in self._handles:
      handles = [(target, self._handles[target])]
  ```
  e `target` é `_output_target_key` — **o seletor de controle da aba**.

**A documentação interna está errada, e isso é parte do defeito.** A docstring
de `gamepad.py:744-745` promete: *"cai no broadcast histórico — limitação
documentada: TODOS os controles vibram juntos"*. **Não é broadcast.** Com um
controle escolhido na janela, o rumble do jogo inteiro vai **só para ele**.

**O que ela veria:** *"deixei o Controle 2 selecionado na janela e o rumble do
jogo saiu só no controle 2"* — ou, com "Todos" selecionado, o que a docstring
descreve.

**A janela em que isso morde é grande:** o `forward_all` bombeia o FF de cada
vpad a **60 Hz** (`daemon/subsystems/coop.py:1329-1331`), enquanto o teardown do
jogador só acontece no `sync` de 2 s. Um controle que perdeu o link mantém o
vpad recebendo rumble com o MAC já órfão por até dois segundos — e cada um
desses reports cai no fallback.

---

## Defeito 3-bis — MEDIDO AO VIVO em 03/08: o `aplicado_em` diz onde REGISTROU, não onde PEGOU

Este defeito foi **capturado no hardware dela**, e é a prova de que o campo
`aplicado_em` — acrescentado justamente para o daemon parar de mentir — ainda
mente, num caso que ninguém previu.

Com dois DualSense por Bluetooth e o co-op ativo, `led.player_set` respondeu:

```json
{"status": "ok", "bits": [true,false,true,true,false], "aplicado_em": ["143a9a13ebab"]}
```

E o sysfs **nem mudou**:

```
antes:  player-3 = 1   (padrão --x--, o P1)
depois: player-3 = 1   (idêntico)
```

**A camada do co-op vence no merge** (`R-13`,
`core/backend_pydualsense.py:335-341`) — e ela está acima da camada da usuária
**de propósito**, para que o revert do co-op reencontre o padrão intacto embaixo.
A decisão está certa.

**O que erra é a resposta.** O `aplicado_em` informa **em que MACs a intenção foi
registrada**, não **onde ela pegou**. Com o co-op ligado, registrar na camada da
usuária não muda nada — e o chamador recebe uma lista que parece confirmação.

**A cura:** a resposta precisa distinguir *registrado* de *vigente*. Se a camada
que venceu não é a da usuária, o daemon sabe disso no instante da resposta — e
deve dizer.

**Aceite:** com o co-op ativo, `led.player_set` responde que o valor foi
registrado **e** que ele **não está vigente**, com o motivo (`co-op`).

**Teste que morde:** co-op ativo + `led.player_set` → asserção de que a resposta
**não** afirma vigência. Hoje ela afirma.

---

## Defeito 4 — o seletor global sequestra outras escritas também

O mesmo `_output_target_key` é consultado por `_for_each`
(`core/backend_pydualsense.py:1995-2001`) e `_for_each_led`
(`core/backend_pydualsense.py:2033-2039`), com `broadcast=False` por padrão.
Caem ali, além do rumble: `set_trigger`
(`core/backend_pydualsense.py:2154`) e `set_led`
(`core/backend_pydualsense.py:2164`) — os caminhos **sem** `uniq`.

**A exceção prova a regra:** `apply_output_defaults` escapa de propósito, com
`broadcast=True` (`core/backend_pydualsense.py:2543-2547`), porque sem isso
ativar um perfil com um alvo escolhido aplicava só no alvo. **Alguém já viu esse
defeito e o curou em UM lugar.** Os outros três ficaram.

---

## As entregas

### E1 — a trava manual passa a ser por controle

`manual_override_categories` vira indexado por MAC, com um balde `None` para o
que é genuinamente global.

**Onde:** `daemon/state_store.py:102` e os dois pontos de armação
(`ipc_handlers.py:735,783`); o consumidor é `profiles/manager.py:342-346`.

**Compatibilidade — e ela não é opcional:** nenhum campo do `StateStore` é
indexado por uniq hoje (`daemon/state_store.py:82-166`). Esta entrega abre o
primeiro. O leitor `manual_override_categories` é API pública do store e tem
outros chamadores — mantenha a assinatura antiga devolvendo **a união** dos
baldes, e acrescente a consulta por MAC. Trocar a assinatura de uma vez é o
caminho de quebrar coisa que ninguém está olhando.

**Aceite:** ajustar a cor do Controle 3 na mão e ativar um perfil com cor
definida → **os controles 1, 2 e 4 recebem a cor do perfil**; o 3 mantém a dela.

### E2 — o broadcast registra na camada de broadcast

O caminho sem `uniq` volta a gravar em `_desired_default` (a camada de
broadcast, que é onde ele sempre morou) **e** passa a vencer a paleta automática
— sem descer para `_LAYER_USER` de cada MAC.

**O ponto exato do problema, e é ele que a entrega tem de resolver:** o
`_merged_desired_for_key` (`core/backend_pydualsense.py:1222`) põe a camada
automática do slot **acima** do `_desired_default` e **abaixo** do
`_desired_by_uniq`. Foi essa ordem que fez o broadcast não pintar, e foi por isso
que a cura de 02/08 escapou para o `_desired_by_uniq`.

**A cura de raiz é a ordem das camadas, não o desvio.** Um broadcast **explícito
da usuária** é um gesto dela e tem de vencer a paleta automática — que é uma
conveniência, não uma escolha. Duas saídas:

- **(a)** um quinto nível entre a automática e o `_desired_by_uniq`:
  "broadcast da usuária". **Recomendado** — é honesto sobre o que aconteceu, e
  o revert (`Voltar todos ao automático`) tem onde agir;
- **(b)** marcar o `_desired_default` com dono `usuaria` e ensinar o merge a
  respeitá-lo acima da automática. Menos código, e mistura duas coisas
  (o default do perfil e o gesto dela) no mesmo slot — foi assim que a camada
  do co-op teve de ser tirada de `_desired_by_uniq` (`R-13`).

**Aceite:** `led.set` sem `uniq` pinta os quatro **e** um perfil ativado em
seguida ainda consegue pintar. Hoje, o segundo não acontece.

**Este é o critério que separa a entrega da regressão:** as duas coisas ao mesmo
tempo. Uma cura que faça só a primeira é a de 02/08; uma que faça só a segunda é
o defeito que ela consertou.

### E3 — o rumble do jogo nunca passa pelo seletor

`daemon/subsystems/gamepad.py:765-766` passa a chamar o broadcast **explícito**
(`broadcast=True`), e a docstring das linhas 744-745 passa a dizer a verdade.

**Onde mais olhar antes de fechar:** `set_trigger` e `set_led` sem `uniq` estão
no mesmo barco (defeito 4). O gesto **da usuária** pelo seletor deve respeitar o
seletor — é para isso que ele existe. O que **nunca** deve passar por ele é o
que vem do **jogo**, porque o jogo não faz ideia de que existe um seletor na
janela.

**A regra a escrever no código, em uma linha:** *escrita originada da usuária
respeita o seletor; escrita originada do jogo, nunca.*

**Aceite:** com o Controle 2 escolhido na janela e dois controles vibrando no
jogo, os dois vibram.

### E4 — os testes que mordem

Uma bancada por defeito, e todas exigem **dois controles** — é por isso que
nenhuma existe hoje:

1. **a trava é de quem?** Dois MACs; `led.set` com `uniq` no primeiro; ativar
   perfil com cor. Asserção: o segundo recebe a cor do perfil. *Hoje reprova —
   e é essa a mordida.*
2. **o broadcast e o perfil convivem?** `led.set` sem `uniq`; conferir que os
   dois pintaram; ativar perfil; conferir que os dois pintaram de novo. Arranque
   a E2 e veja o segundo passo reprovar.
3. **o rumble do jogo ignora o seletor.** `set_output_target(MAC_A)`; disparar
   rumble de jogo com `target_uniq` inválido; asserção: **os dois** handles
   receberam.
4. **o seletor continua valendo para o gesto dela.** O contrário do 3, para a
   cura não virar "o seletor parou de funcionar".

---

## Testes que vão reprovar

```
pytest tests/unit -k "led or rumble or profile or manual or override or target"
```

O `led.set`/`led.player_set` têm testes-muralha travando a resposta `{"status":
"ok"}` e a lista `aplicado_em` recém-criada. A E2 muda **onde** o registro cai,
não o formato da resposta — mas confira antes de assumir.

## O que NÃO fazer

- **Não reverter a cura `BROADCAST-QUE-NÃO-MENTE-01`.** O defeito que ela
  conserta é pior. O que se corrige é o **alcance**;
- **Não tirar a camada automática do merge.** Ela é a cor por jogador (`COR-03`)
  e é o que faz cada controle nascer com uma cor distinta;
- **Não mover a camada do co-op para `_desired_by_uniq`** ao mexer nas camadas.
  Ela está fora **de propósito** (`R-13`, `core/backend_pydualsense.py:335-341`):
  no mesmo slot, o revert do co-op restauraria o número dele para sempre;
- **Não dar TTL à trava manual** como atalho para o eixo por controle. O tempo
  não é o eixo errado por acaso — a trava existe para sobreviver ao autoswitch,
  que dispara a cada troca de janela;
- **Não mexer no `apply_output_defaults`**, que já escapa do seletor de
  propósito.

## O que fica ABERTO

- **a escolha (a)/(b) da E2** — decisão de arquitetura, e vale escrever a nota
  datada do que foi escolhido e por quê;
- **`mode`, `mouse`, `rumble`, `key_bindings` e `speaker` continuam globais no
  perfil** (`profiles/schema.py:468-500`); só `leds` e `triggers` têm eixo por
  controle (`profiles/schema.py:447-448`). Isso não é defeito desta sprint — é a
  superfície que falta, e é o que faz estes quatro defeitos existirem. Registrado
  para não se procurar bug onde há **ausência**.
