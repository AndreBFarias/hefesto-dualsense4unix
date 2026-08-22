# GRAB-DOBRADO-01 — o P1 perdia o `EVIOCGRAB` e ninguém tentava de novo

**Estado:** CONCLUÍDA — a retomada periódica do `EVIOCGRAB` está em
`daemon/lifecycle.py:84`, `:4203` e `:4393`, a detecção do P1 dobrado em
`daemon/subsystems/gamepad.py:440`, e o portão em
`tests/unit/test_grab_dobrado_01_o_primario_nao_tentava_de_novo.py`
(verificado em 21/08/2026)

**15/08/2026.** É a **D-29.1** do índice de 14/08, a que ela mandou abrir frente
própria: *"o grab do controle primário está FALHANDO agora"*.

---

## 1. O defeito ainda acontece? **Não agora — e a resposta importa**

Medido às 14:19 de 15/08, com o daemon reiniciado às 14:15:57:

| o que medi | resultado |
|---|---|
| `daemon.state_full` → `primary_grab_state` | **`held`** |
| `EVIOCGRAB` dos quatro nós físicos (sonda que só pode levar EBUSY) | os quatro **PEGOS** — pelo próprio daemon |
| `journalctl` desde o restart, procurando `evdev_grab_failed` | **nenhuma ocorrência** |
| co-op | 4 jogadores, 4 vpads, todos promovidos |

**Foi o restart que curou.** O defeito é **intermitente**, e a frente muda de
forma exatamente como ela previu: a pergunta não é *"por que falha"*, é
**"por que fica falhado"**.

O histórico do journal mostra quatro ocorrências em três dias, todas com o
mesmo texto e nenhuma seguida de recuperação:

```
ago 13 03:03:14  evdev_grab_failed  [Errno 16] ... path=/dev/input/event29
ago 13 03:03:17  evdev_grab_failed  [Errno 16] ... path=/dev/input/event265
ago 14 15:54:58  evdev_grab_failed  [Errno 16] ... path=/dev/input/event265
ago 15 01:48:39  evdev_grab_failed  [Errno 16] ... path=/dev/input/event265
```

As quatro vêm do `_reapply_grab` (a frase *"grab falhou ao reabrir o device"*),
nunca do `set_grab` — ou seja: **sempre no (re)open de um nó**, nunca num
pedido da GUI.

---

## 2. Quem segura o dispositivo

**Não está provado, e digo isso em vez de inventar.** A linha do tempo de 14/08
às 15:54:58, lida inteira, é esta:

```
15:54:54–56  evdev_read_lost [Errno 19]  (os nós antigos morreram: re-enumeração)
15:54:56.78  coop_player_removed         identity=444648……03  players=3
15:54:58.38  evdev_reopen_requested      reason=retarget      <- o PRIMÁRIO mudou
15:54:58.63  controller_primary_bound    transport=bt
15:54:58.91  evdev_started               path=/dev/input/event265
15:54:58.91  evdev_grab_failed           [Errno 16]  path=/dev/input/event265
```

O que eu **descartei com evidência**:

- **não era o leitor de co-op zumbi.** Todo `EvdevReader` loga `evdev_started`
  ao abrir, e no intervalo inteiro há **uma só** abertura de `event265` — a do
  primário. O leitor do co-op daquele MAC nunca reabriu no nó novo;
- **não é uma segunda instância do daemon.** Há um PID só na unit, e hoje
  `/proc/*/fd` confirma **um fd por nó** no daemon.

O que **sobra**, e é candidato sem prova: a Steam. Medido hoje em `/proc`:

```
610430 steam  /dev/input/event21     (aberto 14:12, ANTES do daemon subir)
610430 steam  /dev/input/event25
610430 steam  /dev/hidraw6,7,8,9,10,11
```

A Steam **abre** os evdev dos controles que enxerga. Abrir não é grabar — hoje
ela tem `event21` aberto **e o daemon tem o grab dele**, então neste instante
ela não está grabando. Se ela graba durante uma partida com Steam Input ativo,
isso explicaria a recusa; **não medi isso**, e medir exige a partida dela
aberta. Fica registrado como o próximo passo desta frente.

**Mas a identidade do terceiro não muda o conserto**, e é isso que o próximo
item explica.

---

## 3. Por que só o primário — e isto explica o que JÁ funcionava

A pergunta certa não é *"por que o primário perde o grab"* (qualquer um pode
perder, num instante de re-enumeração). É **"por que só o primário FICA sem
ele"**. A resposta está no código, e é uma assimetria de recuperação:

| | secundário (P2+) | primário (P1) |
|---|---|---|
| quem tenta de novo | `CoopManager.sync`, a cada ciclo: acha `grab_state == "failed"`, derruba o jogador (`coop_player_grab_failed_retry`) e o respawna | **ninguém** |
| o vpad nasce sem grab? | **não** — `_promote_pending` exige `"held"` (BUG-COOP-GRAB-PENDING-VPAD-01) | **sim** — o vpad do P1 já está de pé quando o grab é recusado |
| resultado de uma recusa transitória | some em um tique | **fica até o próximo replug ou restart** |

O grab do P1 só era pedido em dois lugares: `_set_controller_grab(daemon, True)`
no **start** da emulação, e `_reapply_grab` no **(re)open** do nó. Nenhum dos
dois roda periodicamente. Sem troca de nó e sem toggle da emulação, `"failed"`
era um estado **absorvente**.

É por isso que o restart cura, é por isso que parece intermitente, e é por isso
que o P2 dela nunca apareceu com este defeito — o co-op já tinha, desde julho, a
cura que o P1 nunca ganhou. **A casa sabia e o produto não fazia.**

---

## 4. O conserto

`reconciliar_grab_do_primario`, em
[`daemon/subsystems/gamepad.py`](../../../src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py)
— o irmão que faltava do retry do co-op —, chamada pelo poll loop de
[`daemon/lifecycle.py`](../../../src/hefesto_dualsense4unix/daemon/lifecycle.py)
a cada `GRAB_RECONCILE_SEC` (2 s, o mesmo ritmo do `coop.sync`, ao lado do
watchdog de evdev que já morava ali).

Três propriedades, e cada uma nasceu de uma cicatriz desta casa:

1. **Sem poder destrutivo.** Não reabre, não derruba e não recria device nenhum
   — no molde de `esconder_o_fisico_para_o_jogo`, cuja regra veio da
   PARTIDA-PICOTADA-01 (oito ciclos de suspender/retomar vpad no meio da partida
   dela). Um `ioctl` idempotente, e só.
2. **Os gates são os do estado canônico**: Modo Nativo, emulação desligada ou
   vpad morto ⇒ não pega nada. *Duplicado > zero controles* — grabar o físico
   sem virtual vivo para devolvê-lo ao jogo é o estrago da GUERRA-01.
3. **Barata no caso normal**: uma comparação de string quando o grab está de pé.

E a **detecção**, que é o que o produto não tinha: `grab_do_primario_dobrado`
faz a conta das **duas** metades (grab recusado **e** vpad vivo) num dono só —
`primary_grab_state == "failed"` sozinho não é o estrago, e a aba Início já
fazia esse `and` na mão. A cura usa a detecção como gate, de propósito: escrever
a mesma condição duas vezes seria a próxima divergência.

Além disso, o journal deixou de ficar mudo. Antes havia **uma** linha, no
instante da recusa, e silêncio depois — meia hora de input dobrado era
indistinguível de meio segundo. Agora:

| sinal | quando |
|---|---|
| `gamepad_grab_dobrado_persiste` (warning, com `tentativas=N`) | na 1ª falha e a cada `GRAB_AVISO_A_CADA` (≈1 min) |
| `gamepad_grab_recuperado` (info, com quantas tentativas custou) | quando volta |
| contadores `gamepad.grab.retry_failed` / `gamepad.grab.recovered` | sempre, no store |

### O aviso na interface já existia — e foi conferido

A aba Início já mostra **"Grab falhou — input pode dobrar no jogo"** no card do
primário quando `primary_grab_state == "failed"` **e** a emulação está ligada
(`app/actions/home_actions.py`, `_render_home_controllers`). Está fiado ao
`daemon.state_full`. **Não dupliquei**: com o retry de pé, esse aviso passa a
significar *"está acontecendo AGORA e o produto está tentando"*, em vez de
*"aconteceu em algum momento e ninguém vai fazer nada"*.

---

## 5. O teste que MORDE

`tests/unit/test_grab_dobrado_01_o_primario_nao_tentava_de_novo.py`, nove
mordidas. **Arranquei cada uma, RODEI, vi reprovar e devolvi:**

| o que arranquei | o que reprovou |
|---|---|
| a chamada no poll loop | `test_o_poll_loop_reconcilia_o_grab_do_primario` |
| o `set_grab` de dentro da reconciliação | `test_o_grab_do_primario_e_retomado_quando_o_no_libera` (`dev.grabs == 0`) |
| os gates de emulação/vpad da detecção | 3 testes, incluindo o do vpad **morto** |
| o gate do Modo Nativo | `test_nao_graba_em_modo_nativo` |
| o atalho de `set_grab` crescido para `"failed"` | 2 testes |

A mordida do laço é a que importa mais no longo prazo: sem ela, apagar **uma
linha** de `lifecycle.py` devolveria o defeito inteiro com a suíte toda verde —
que é a forma exata do defeito-mãe desta casa.

O portão `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py` já pegou isso na
prática durante esta entrega: `grab_do_primario_dobrado` nasceu **sem chamador
em produção** e o portão reprovou por nome. Foi fiada, não declarada como
dívida.

---

## 6. O que fica aberto

1. **Quem é o terceiro.** Só se mede com a partida dela aberta: com um jogo
   Steam Input rodando, ler `primary_grab_state` e sondar o `EVIOCGRAB`. Se for
   a Steam, a causa é **externa** e o retry é o teto do que dá para fazer — mas
   aí o warning periódico passa a datar a duração do estrago, que hoje ninguém
   conseguia.
2. **O `doctor` não fala de grab.** O comentário do `state_full` afirma que
   *"a GUI/doctor avisam"* — a GUI avisa, o `doctor` não tem uma linha sobre
   isso. É uma linha em `src/hefesto_dualsense4unix/cli/cmd_doctor.py`, que
   estava fora do território desta leva.
3. **`primary_grab_dobrado` no `state_full`.** A detecção tem dono agora, mas o
   estado publicado continua entregando só `primary_grab_state` e deixando o
   `and` para cada superfície repetir. `ipc_handlers.py` também estava fora do
   território.

---

## 7. O que é decisão dela

| decisão dela | execução minha |
|---|---|
| **Nada.** Não muda pixel, não muda vocabulário, não escolhe entre dois caminhos — devolve um comportamento que o co-op já tinha | o retry, a detecção, os avisos e as nove mordidas |
