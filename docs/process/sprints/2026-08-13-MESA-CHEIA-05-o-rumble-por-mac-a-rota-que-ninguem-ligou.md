# MESA-CHEIA-05 — o rumble por MAC: a rota existe e ninguém a ligou

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código.** O diagnóstico da seção 1 foi
  **substituído em 13/08** pelo censo das dez abas — ver a caixa lá dentro
- **Duas entregas, em duas ondas:** a **E0** (o rumble que migra de dono) é
  conserto de defeito e **não depende de decisão nenhuma**; a **E1** (a
  intensidade por peça) **trava na D-4** dela
- **Custo mínimo:** E0 ≈ 2 h · E1 ≈ 11 h (660 min, estimativa do censo)
- **É a única sprint desta leva que mexe no daemon vivo dela.**

---

## 1. O defeito, medido

> **CORREÇÃO DE 13/08/2026, pelo censo das dez abas — o diagnóstico desta seção
> estava errado, e o texto errado foi SUBSTITUÍDO.**
>
> A versão anterior abria com *"Com «Sony 2» escolhido no cabeçalho, a aba
> Rumble vibra os quatro"* e afirmava que **`rumble_set` era a única função de
> saída do `ipc_bridge.py` sem `uniq`**. As duas afirmações são falsas, e o
> conserto que elas pediam mirava o lugar errado. O que está abaixo é o que foi
> reaberto na árvore. Nenhuma decisão dela caducou aqui — caducou um fato meu.

**O pulso MIRA. O que erra é a intensidade — e o que é pior, o pulso fixado
MIGRA de controle sozinho.**

### 1.a — Por que o pulso mira, apesar de o pedido não levar endereço

`rumble_set` (`app/ipc_bridge.py:398`) realmente **não aceita `uniq`**, e o
handler (`daemon/ipc_handlers.py:3231`) realmente **não chama `_apply_por_uniq`**
— vai direto em `self.controller.set_rumble(...)` (`:3251`).

**O endereço viaja por fora da chamada.** `set_rumble`
(`core/backend_pydualsense.py:2845`) não escreve em ninguém diretamente: delega a
`_for_each_com_key` (`:2320`), que resolve o alvo assim
(`core/backend_pydualsense.py:2336-2338`):

    target = self._output_target_key
    if not broadcast and target is not None and target in self._handles:
        handles = [(target, self._handles[target])]

E `_output_target_key` foi armado pelo próprio chip do cabeçalho, via
`controller.target.set` (`app/actions/status_actions.py:2194` →
`daemon/ipc_handlers.py:3152`).

**Consequência:** com "Sony 2" escolhido, *"Testar motores"* vibra **só o 2**.
Feio — o alvo é um ponteiro global mutável, e não um parâmetro — mas funciona.

### 1.b — O que erra de verdade: a intensidade não tem endereço nenhum

O **mesmo clique** faz duas coisas incompatíveis:

| o que ele faz | onde | escopo |
|---|---|---|
| grava a política no rascunho **da peça** | `app/actions/rumble_actions.py:429` → `:551` (`with_controller_rumble(uniq, ...)`) | **por controle** |
| manda `rumble.policy_set` ao daemon **sem endereço** | `app/actions/rumble_actions.py:433` → `daemon/ipc_handlers.py:3314-3336`, que escreve `daemon_cfg.rumble_policy` em `:3329` | **da máquina inteira** |

E a tela afirma o alvo enquanto isso: o selo diz *"Editando: Controle 2 (USB)"*
(`app/actions/status_actions.py:1858`) e o toast diz *"Intensidade da vibração:
Máximo"* (`app/actions/rumble_actions.py:435`).

**Esta é a pior mentira das dez abas**, e a razão é precisa: é a única em que o
alvo **existe**, a tela o **afirma**, e o código o **desobedece**.

### 1.c — E o achado novo: o rumble fixado MIGRA de dono

Ninguém tinha escrito isto em lugar nenhum do repositório.

```
   Ela aplica 160/220 no Controle 2.
        daemon.config.rumble_active = (160, 220)     ipc_handlers.py:3248
        _output_target_key = <key do 2>

   Ela troca o seletor para o Controle 3, por outro motivo qualquer.
        _output_target_key = <key do 3>              (rumble_active INTACTO)

   200 ms depois, e a cada 200 ms para sempre:
        reassert_rumble (subsystems/rumble.py:134)
          active = cfg.rumble_active                 (:150) → (160, 220)
          daemon.controller.set_rumble(...)          (:176)
                    └─ _for_each_com_key honra o alvo DE AGORA
                       └─ marreta o CONTROLE 3 com o valor do 2
```

`rumble_active` é **um par para o daemon inteiro** (`daemon/lifecycle.py:195`) e
o destino dele é um **ponteiro mutável**. O valor foi fixado para um controle e
passa a valer para quem estiver no seletor.

### 1.d — A contagem do `ipc_bridge.py`, refeita por AST

A afirmação antiga (*"a única sem `uniq`"*) não sobrevive à contagem. Rodada em
13/08 sobre `src/hefesto_dualsense4unix/app/ipc_bridge.py`:

| aceita `uniq` | **não** aceita |
|---|---|
| `trigger_set_checked` (`:327`), `trigger_reset` (`:348`), `led_set` (`:378`), `identity_number_set` (`:479`), `player_leds_set` (`:511`), `mic_set` (`:604`), `speaker_set` (`:641`) | **as seis de rumble** — `rumble_set` (`:398`), `rumble_stop` (`:409`), `rumble_passthrough` (`:415`), `rumble_policy_set_checked` (`:421`), `rumble_policy_set` (`:435`), `rumble_policy_custom` (`:446`) — mais o invólucro fino `trigger_set` (`:342`), que repassa sem endereço |

**O rumble não é a exceção de uma função: é a família inteira.** E dois nomes da
lista antiga não existem — `led_player_set` chama-se `player_leds_set`, e o
`trigger_set` que aceita `uniq` é o `trigger_set_checked`.

### A parte boa: a rota por MAC EXISTE, e é usada

`set_rumble_for(uniq, weak, strong)` está em
`core/backend_pydualsense.py:3642-3669`. Ela resolve o handle pelo MAC, aplica
a escala por peça (`_escalar_rumble`, `:3663`) e devolve `False` quando o MAC
não casa — o chamador decide o fallback. Quem já a usa:

- o co-op, para mirar a vibração do jogador certo (`daemon/subsystems/coop.py:571`);
- o force-feedback do jogo (`daemon/subsystems/gamepad.py:992`).

Esta é, de novo, **a classe de defeito mais cara desta casa**: a cura escrita e
nunca ligada. A POR-UNIDADE-01 já tinha achado a mesma coisa em 10/08 e a
listou numa tabela de quatro linhas com o título *"as curas que já estavam
escritas e nunca ligadas"*.

### E a parte que muda o preço: o obstáculo não é o `OutputSpec`

A suspeita de partida era que faltasse campo de rumble no `OutputSpec`
(`core/controller.py:63-67`, que tem `trigger_left`, `trigger_right`, `led`,
`player_leds` e `mic_led`). **Não é isso, e o campo NÃO deve nascer:** o
`OutputSpec` é o mapa do que **fica** — o desejado que sobrevive ao reassert —
e o próprio `set_rumble_for` diz que *"o rumble segue transitório (nunca entra
no desejado)"*.

**O obstáculo é o cronômetro** — e a correção de 13/08 mudou **qual** é o
sintoma dele. Não é *"vibrou só o 2 e logo em seguida todos"*: o
`reassert_rumble` não reescreve broadcast, reescreve **para o alvo de agora**
(`daemon/subsystems/rumble.py:150` lê o par global, `:176` chama `set_rumble`,
que resolve o alvo em `core/backend_pydualsense.py:2336-2338`). O sintoma real é
o da §1.c: **o valor fixado num controle passa a valer para outro**, e só na
troca do seletor.

---

## 2. O que muda — e são DUAS entregas, não uma

**A correção de 13/08 partiu esta sprint em duas**, e a partição importa porque
**uma delas não espera decisão nenhuma**.

### E0 — o rumble deixa de MIGRAR (não depende da D-4)

O par fixado passa a carregar **junto** o alvo em que foi fixado. O
`reassert_rumble` reescreve naquele alvo, não no ponteiro de agora.

```
   HOJE                                   DEPOIS (E0)
   rumble_active = (160, 220)             rumble_active = (160, 220)
   alvo = "o que estiver no seletor"      alvo = <a key de quando foi fixado>
        │                                      │
        ▼ troca de seletor                     ▼ troca de seletor
   o P3 passa a receber o valor do P2      o P2 continua sendo o dono
```

**Isto é conserto de defeito, não escolha de produto** — sob **qualquer**
resposta à D-4, um valor fixado num controle não deve migrar para outro por um
gesto que não fala de vibração. Por isso a E0 é onda 1 e a E1 é onda 3.

### E1 — a intensidade por peça (só depois da D-4)

**No daemon:** `rumble_active` deixa de ser um par e passa a ser um par
**mais um mapa de exceções por MAC** — o mesmo vocabulário de camadas que o
backend já usa em `_led_scale_by_uniq` / `_rumble_scale_by_uniq`
(`core/backend_pydualsense.py:1081` e `:1091`):

```
   HOJE                                  DEPOIS (E1)
   rumble_active = (60, 200)             rumble_active      = (60, 200)  <- a casa
   alvo = _output_target_key             rumble_active_por_uniq = {
        │  (UM ponteiro, mutável)            "aabbcc000002": (0, 0),     <- o 2 calado
        ▼                                 }
   reassert 5 Hz                               │
   set_rumble -> _for_each_com_key             ▼
        │                                 reassert 5 Hz
        ├─ alvo == None ("Todos")         para cada conectado:
        │   ┌────┬────┬────┬────┐           tem exceção? set_rumble_for(uniq, ...)
        │   │ P1 │ P2 │ P3 │ P4 │           não tem?    entra no par da casa
        │   └────┴────┴────┴────┘         ┌────┬────┬────┬────┐
        │    os quatro, com o MESMO par   │ P1 │ -- │ P3 │ P4 │
        │                                 └────┴────┴────┴────┘
        └─ alvo == <key>                   quatro pares independentes,
            ┌────┬────┬────┬────┐          cada um com o seu dono
            │ -- │ P2 │ -- │ -- │
            └────┴────┴────┴────┘
             UM só — mas o alvo é o
             DE AGORA, não o de quando
             o par foi fixado (§1.c)
```

**Na tela:** a aba Rumble deixa de ser a única em que "Ajustes vão para:" vale
para **metade** do gesto — o pulso obedece, a intensidade não. E a marca da leva
passa a poder dizer a verdade ali; hoje ela só poderia mostrar o que o **perfil
guarda**, com a ressalva que a própria aba já escreve, e que é a frase mais
honesta desta casa sobre o assunto: *"o que ela ouve na hora é o global; o que
ela SALVA é da peça"* (`app/actions/rumble_actions.py:529-535`).

### O que NÃO muda, e é decisão de 10/08 que continua valendo

O **passthrough continua sendo um só**. A POR-UNIDADE-01 recusou `rumble.passthrough`
por peça com um motivo que sobrevive ao mapa: ele *"não descreve a peça:
descreve quem manda na vibração agora"*. Um mapa de valores não transforma
"quem é o dono da vibração" numa propriedade de plástico.

O `rumble.policy = "auto"` também continua global, pelo motivo já medido lá: ele
escala pela **bateria do controle primário**.

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_05_o_rumble_mira.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 0 — o rumble que MIGRA de dono (E0, e é a que vale mais barato)

**Arrancar:** deixar o `reassert_rumble` como está hoje — lendo `cfg.rumble_active`
(`daemon/subsystems/rumble.py:150`) e chamando `set_rumble` (`:176`), que resolve
o alvo pelo ponteiro **de agora**.

**Por que reprova:** o teste (a) arma o alvo no controle 2 via
`controller.target.set`, (b) manda `rumble.set` com 160/220, (c) **troca o alvo
para o controle 3**, (d) roda três ciclos de `reassert_rumble`. Com o reassert de
hoje, o controle 3 recebe 160/220 — o teste exige que ele continue em zero e que
o 2 continue recebendo.

**Sem esta mordida a sprint passa e o produto continua com o defeito**, porque o
defeito é **temporal**: aparece 200 ms depois da troca de seletor, nunca na
chamada. E ela é a única mordida da sprint que **não espera decisão nenhuma**.

### Mordida 1 — a intensidade sem endereço (E1)

**Arrancar:** deixar o `rumble.policy_set` escrevendo `daemon_cfg.rumble_policy`
sem olhar `uniq` (`daemon/ipc_handlers.py:3329`).

**Por que reprova:** o `FakeController` registra as chamadas; o dublê tem o
rascunho com política `"max"` para o controle 2 e `"economia"` no global. O teste
exige que o par efetivo do 2 saia escalado por `"max"` e o dos outros por
`"economia"`. Com o campo único da máquina, os quatro saem iguais — que é
exatamente o que a tela promete não fazer (`app/actions/status_actions.py:1858`,
o selo *"Editando: Controle 2"*).

### Mordida 2 — o mapa que não é lido no cronômetro (E1)

**Arrancar:** montar o mapa por `uniq` e **não** iterá-lo no `reassert_rumble`.

**Por que reprova:** mesma armadilha da mordida 0, um andar acima. O teste liga
uma exceção para o controle 2, roda três reasserts e exige que a exceção
sobreviva aos três. Um mapa que só vale na chamada dura 200 ms.

### Mordida 3 — o mapa que não limpa

**Arrancar:** não remover a entrada do mapa em `rumble.passthrough` /
`rumble.stop`.

**Por que reprova:** o teste liga uma exceção para o controle 2, chama
`rumble.passthrough(True)` e exige que o mapa esvazie. Sem a limpeza, o
jogador 2 fica **permanentemente calado** e nem devolver ao jogo o traz de
volta — a versão de rumble da "trava sem fim" que a ONDA-U já curou uma vez
(`daemon/ipc_handlers.py:3286-3296`).

### Mordida 4 — o controle que sai da mesa

**Arrancar:** não descartar entradas de MAC desconectado.

**Por que reprova:** o teste desconecta o controle 2 e exige que o mapa não
cresça sem fim entre replugs. `set_rumble_for` já devolve `False` para MAC que
não casa — o teste usa isso.

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **D-4 — a intensidade da vibração é da PEÇA ou da MÁQUINA?** É o que trava a **E1**, e hoje o produto responde as duas ao mesmo tempo (§1.b). Da peça: ≈ 660 min, e morrem os três defeitos do censo. Da máquina: 20 min de rótulo, e o rascunho fica gravando por peça um número que ninguém lê — o que é dívida, não conserto | montar o lado que ela escolher |
| **~~"Testar motores" com um alvo escolhido vibra SÓ ele, ou continua vibrando todos?~~** — **a pergunta caducou em 13/08**, e o motivo é medição: ele **já vibra só ele**. `set_rumble` honra o `_output_target_key` em `core/backend_pydualsense.py:2336-2338`. Fica registrada porque foi a pergunta que abriu esta sprint | — |
| **A intensidade global continua sendo a escada dela de 11/08** (30% / 100% / 150%, `daemon/subsystems/rumble.py:29-32`)? Esta sprint não a toca | não tocar |
| **O passthrough continua um só?** Eu recomendo manter a recusa de 10/08 — mas quem revoga decisão dela é ela | manter, salvo palavra dela |
| — | o mapa, a limpeza nos dois gestos de soltura, o descarte de MAC morto, e o `uniq` no `rumble_set` do bridge |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** as quatro mordidas, todas com `FakeController` — inclusive a
do cronômetro, que roda o reassert em laço sem tocar em hardware.

**Só a bancada dela**, e aqui é mais do que nas outras sprints:

- **que o controle 1 fica quieto enquanto o 2 vibra.** É a prova inteira, e ela
  exige dois controles na mão;
- **e a metade que vale tanto quanto a ida:** que o motor **para**. É a regra
  desta casa desde 10/08 — *"a volta ao neutro vale tanto quanto a ida"*
  ([CANETA-NA-MÃO-01](2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md),
  seção 2.2). Uma feature que liga e não desliga passaria por aprovada;
- **e o suspeito de 11/08 continua de pé**: o keepalive de 0,5 s
  (`OUT_REPORT_KEEPALIVE_SEC`, `core/backend_pydualsense.py:228`) **cancela
  rumble de terceiros**, medido por dose-resposta. Esta sprint mexe no
  cronômetro DA CASA, não naquele — mas quem for medir o rumble por MAC no
  aparelho vai encontrar os dois efeitos na mesma janela de tempo, e precisa
  saber disso antes de atribuir causa.

**Ela não consegue ver nada disto hoje.** Com um controle só, "vibra um" e
"vibra todos" são a mesma coisa. Esta sprint espera a mesa cheia — e é a razão
de ela ser paralela: nada nas outras cinco depende dela.

---

## 6. A regra dos quatro, nesta sprint

Esta é a única sprint da leva que muda o daemon, então é a única que carrega a
obrigação do **install**: a cura entra sem flag, sem opt-in e sem passo manual
(a prova de ciclo da [CICLO-QUE-PROVA-01](2026-08-08-CICLO-QUE-PROVA-01-desinstalar-instalar-e-comparar-o-que-o-produto-recria-sozinho.md)),
e a prova é o ciclo `uninstall` -> `install` mostrando o daemon novo de pé.

E a armadilha que já custou uma sessão inteira: **o daemon vivo é mais velho que
o código.** Com install editable, cura de daemon só vale no **próximo start** —
o sintoma de esquecer isso é a AUSÊNCIA de dado novo, não um erro.
