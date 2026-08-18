# ESPELHO-QUE-NÃO-NASCEU-01 — o jogador que perde a corrida do hotplug fica mudo

**15/08/2026.** Mesa de quatro DualSense. Um dos quatro vpads entregava ao jogo
entre **0,3 e 27,5 Hz** enquanto os outros três entregavam **165-196 Hz** — duas
a três ordens de grandeza abaixo, com o controle físico correspondente
perfeitamente vivo. A causa não é o aparelho, é uma corrida perdida na promoção
do jogador, e o defeito é **permanente** para quem a perde.

## Antes de tudo: a atribuição pelo LED estava ERRADA

A investigação chegou com uma atribuição vinda do **LED** (`quem_e_quem.py`
registra que a ligação vpad↔MAC não é observável sem apertar botão):

> "P4 = o controle do cabo `d4:2f:4b:00:00:d8`"

**Derrubada, com duas fontes independentes.**

1. `HID_UNIQ` do sysfs de cada nó (`/sys/class/hidraw/hidrawN/device/uevent`),
   cruzado com o `coop_player_added identity=…` do journal.
2. O `state_full` vivo do daemon.

O vpad faminto é o **`Hefesto P4` (`/dev/hidraw12`)**, e o físico por trás dele é
`14:3a:9a:00:00:ab` — um controle de **RÁDIO** em `/dev/hidraw11`. O
`d4:2f:4b:00:00:d8` do cabo é o **primário**, alimenta o vpad do P1 e era o mais
saudável dos quatro (196 Hz).

**Se a investigação tivesse acreditado no LED, teria apontado para o controle
exatamente oposto** — o melhor da mesa, e no transporte errado.

> **Cuidado com o número publicado.** O campo `player` de
> `rumble_ff.per_vpad` é a **fila de chegada do controle** (MESA-CHEIA-12), não o
> slot do vpad. O jogador faminto aparece ali como `player: 2`. Quem casa os dois
> lados é o MAC, nunca o inteiro.

## A causa

`daemon/subsystems/coop.py`, no `_start_player_motion_reader` — o método que dá a
cada jogador do co-op o seu `PhysicalReportReader` (o espelho de motion, GYRO-01).
Ele tinha um quarto gate, além dos três estruturais:

```python
try:
    if hidraw_fn(identity) is None:
        return  # externo/sem handle: gyro nativo, sem espelho
except Exception:
    return
```

Esse gate lia uma **amostra instantânea de um valor que muda**, e a lia no pior
instante possível: a promoção roda no tick do hotplug, enquanto o `_open_one` do
backend ainda está no ar para aquele MAC — até `INIT_TIMEOUT_SEC` = 5 s por
probe, e o rádio chega a estourar o teto. **Quem perdesse a corrida ficava sem
espelho para sempre**: `_start_player_motion_reader` tem **um único chamador**
(`coop.py`, no caminho feliz da promoção) e **nada o reexecuta**.

### A evidência, em quatro camadas

**1. O journal registra a corrida, com carimbo de hora:**

```
06:29:41  coop_player_grab_pending  identity=143a9a…  player=3   ← promoção
06:29:45  pydualsense_init_timeout  path=/dev/hidraw8  timeout_sec=5.0
```

A promoção perguntou pelo handle **4 segundos antes** de a abertura dele
terminar — e terminar em timeout.

**2. O jogador saudável e o faminto divergem em DUAS linhas, sempre as mesmas.**
Promoção de quem tinha handle (P3, `44:46:48:00:00:03`):

```
hidraw_broker_fd_recebido node=/dev/hidraw9 state=exposed
uhid_calibration_por_unidade  player=3
coop_motion_reader_spawned    identity=444648…  player=3
motion_reader_started         path=/dev/hidraw9
uhid_motion_streaming         on=True  player=3
```

Promoção de quem não tinha (`14:3a:9a:00:00:ab`, as **duas** vezes — como P3 às
06:29:41 e como P4 às 06:30:47): **nenhuma dessas cinco linhas**. Só
`uhid_device_created` → `uhid_bind_ok` → `vpad_uhid_ativo` →
`coop_player_added`. A calibração por unidade some junto porque
`read_calibration(identity)` depende do mesmo handle.

**3. Os descritores abertos do daemon provam que o handle chegou DEPOIS — e que
ninguém aproveitou.** Em `/proc/<pid-do-daemon>/fd`:

| nó | fds | quem |
| --- | --- | --- |
| `/dev/hidraw4` | 2 | handle do backend (`O_RDWR`) + reader servido pelo broker (`O_NOFOLLOW`) |
| `/dev/hidraw5` | 2 | idem |
| `/dev/hidraw9` | 2 | idem |
| **`/dev/hidraw11`** | **1** | **só o handle do backend — nenhum reader** |
| `/dev/hidraw8 (deleted)` | 1 | fd VAZADO pelo probe que estourou o timeout |

O handle do controle faminto **existe hoje**: `hidraw_path("143a9a…")`
resolveria agora mesmo. Faltou só alguém perguntar de novo.

**4. O `state_full` vivo fecha a conta:** o vpad alimentado por
`14:3a:9a:00:00:ab` reporta `motion_streaming: False, motion_hz: 0.0`; os outros
três, `True` a 165-196 Hz.

### Por que 0,4 Hz, e não "um pouco menos"

Sem reader, `_motion_streaming` fica `False` e a emissão do vpad cai no
**delta do poll loop de 60 Hz** (`uhid_gamepad.py`, `_emit_if_changed`). Mas a
janela 15..39 do report — gyro, accel, timestamp, touch — fica **congelada em
`_MOTION_NEUTRAL`**. Um controle em repouso não muda mais nada, então o delta
quase nunca dispara. Não é "input degradado": é input **parado**.

## Por que P1, P2 e P3 escaparam

Duas razões distintas, e as duas importam:

- **P2 e P3** simplesmente **ganharam** a corrida: o handle já estava aberto na
  promoção, o gate passou, o espelho nasceu. Com o reader como relógio, cada
  report cru do físico traz bytes de IMU novos, o corpo do report muda quase
  sempre, e a emissão bate no teto de 250 Hz do `MOTION_EMIT_MAX_HZ` — 165-196 Hz
  medidos depois do throttle e do delta.
- **O P1 nunca sofre disto, e por desenho.** O
  `subsystems/gamepad.start_motion_reader` **não olha o resultado** de
  `hidraw_path()` — só se o método existe. Ele cria o reader e deixa o
  `path_provider` re-resolver. Era a assimetria que explicava tudo.

## O que mudou às 07:25 (a mudança "espontânea" de patamar)

O vpad faminto pulou de ~0,4 Hz para ~26 Hz sem ninguém tocar em nada. O
journal do broker responde:

```
07:25:25  node_fd_servido  node=/dev/hidraw4   conn=104  peer_pid=223973
07:25:25  node_fd_servido  node=/dev/hidraw5   conn=105  peer_pid=223973
07:25:25  node_fd_servido  node=/dev/hidraw9   conn=108  peer_pid=223973
07:25:25  node_fd_servido  node=/dev/hidraw11  conn=110  peer_pid=223973
```

O pid 223973 é **o próprio instrumento de medição** pedindo os quatro nós ao
broker. Ao drenar `/dev/hidraw11`, ele **manteve o enlace de rádio quente** — e o
firmware do DualSense em BT *emudece em repouso* (é a premissa do
`_SILENCE_REOPEN_BT_S = 30.0` em `physical_report_reader.py`). Com o rádio
acordado, o evdev do daemon voltou a receber jitter analógico, e o delta do poll
loop passou a disparar em ~43% dos ticks de 60 Hz ≈ 26 Hz.

**Nada mudou no produto.** A régua acordou o que estava medindo. É a irmã
mais perigosa de *"o instrumento mente mais que o produto"*: aqui o instrumento
não mentiu — ele **alterou** o fenômeno. Medição de controle em rádio parado tem
de declarar se alguém mais está com o nó aberto.

## Regressão?

**Não.** `git log -L` sobre o bloco aponta um commit só: `b4589a1`
*"feat: co-op 4P misto pronto pra v1 — gyro no vpad…"*. O gate nasceu junto com o
espelho por jogador. Ficou invisível enquanto a mesa era pequena: precisa de
hotplug concorrente **e** de um probe lento (o rádio) para a corrida ser perdida.

## O conserto

O quarto gate saiu. Os três estruturais ficaram — são verdades que não mudam
enquanto o jogador existir: vpad em uhid, identidade com MAC, backend que expõe
`hidraw_path`.

Quem espera pelo handle agora é **o reader**, que já sabia fazer isso: `_run`
re-resolve o `path_provider` a cada volta e faz backoff de 0,5 s a 5 s enquanto
ele devolve `None`, **na thread dele, fora do event loop**. É exatamente o que o
espelho do P1 sempre fez.

### A decisão do 8BIT-02 continua de pé — só mudou onde ela é garantida

O gate se justificava com a decisão da mantenedora (estudo 2026-07-19): 8BitDo e
Nintendo passam direto ao jogo com o **gyro nativo** deles, sem espelho. **A
decisão não mudou.** O que se descobriu é que ela **nunca dependeu daquele
gate**: os secundários saem de `discover_dualsense_evdevs()`, fechada em
`DUALSENSE_VENDOR`/`DUALSENSE_PIDS` — um externo **nunca chega a `_players`** —
e um DualSense sem MAC legível já parava no gate `path:`. O gate inferia
"é externo" de um sinal que um DualSense legítimo também emite.

O teste que codificava a inferência antiga
(`test_externo_sem_handle_fica_sem_espelho`) montava um cenário que **não pode
ocorrer em produção**: um jogador em `_players` com MAC cujo `hidraw_path` é
`None`, chamado de "8BitDo". Ele foi substituído por dois que travam a coisa
certa:

- `test_externo_nunca_chega_a_pedir_espelho` — a descoberta é fechada em
  vendor/PID, então 8BitDo e Nintendo não viram chave de `_players`;
- `test_identidade_sem_mac_e_o_gate_do_externo_sem_driver` — DualSense sem MAC
  legível para no `path:`, mesmo sem handle nenhum.

### A mordida

`test_espelho_nasce_com_o_handle_ainda_fechado`. Com o gate devolvido ao código:

```
AssertionError: assert False
 +  where False = isinstance(None, _FakeReader)
1 failed, 14 passed
```

Cura devolvida: 15 passam.

## O que fica em aberto (é dela)

1. **O daemon vivo é mais velho que o código.** A cura só vale no próximo start
   — o jogador faminto de hoje continua faminto até o daemon reiniciar. **Não
   reiniciei**: a mesa de quatro é insubstituível e a decisão é dela.
2. **O fd vazado do `pydualsense_init_timeout`.** `/dev/hidraw8 (deleted)` segue
   aberto no daemon desde 06:29:45. A thread que estoura `INIT_TIMEOUT_SEC` é
   abandonada com o nó aberto, e o descritor nunca é recolhido. É outro defeito,
   menor, e não foi tocado aqui.
3. **A medição de taxa em rádio precisa declarar quem mais tem o nó aberto** —
   ver o achado das 07:25. Sem isso, dois ensaios do mesmo controle em BT não são
   comparáveis.
