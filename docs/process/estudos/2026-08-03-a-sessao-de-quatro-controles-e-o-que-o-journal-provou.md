# A sessão de quatro controles — e o que o journal provou

- **Levantado em:** 03/08/2026, sobre a branch `restauro/inicio-da-sessao`
  (HEAD `19acbeb`, v0.8.0 publicada), com trabalho não commitado na árvore
- **Natureza:** medição de campo + auditoria. **Nada foi executado contra o
  daemon dela, nada foi reiniciado, nenhum arquivo dela foi tocado.** A leitura
  é do journal do usuário, que guarda a sessão inteira
- **Por que existe:** ela jogou em 02/08/2026, à noite, com os controles no
  Bluetooth, e disse:

  > *"Ontem fui jogar com os 4 controles no bt. Todos os problemas antigos
  > voltaram e outros notei que foram regressões."*

  Este documento é a resposta medida a essa frase. **A sessão está inteira no
  journal**, e ela conta uma história mais precisa do que qualquer leitura de
  código conseguiria — inclusive corrigindo o que se supunha.

- **Regra de uso:** as sprints de 03/08 derivam **deste** documento. Quem for
  executá-las não precisa remedir nada do que está aqui.

---

## A janela: onde a sessão está no journal

O daemon dela loga ~240 eventos por hora quando ocioso. A sessão de jogo salta
para milhares:

| hora (02/08) | eventos | o que é |
|---|---:|---|
| 12h–13h | 240 | ocioso |
| 13h–16h | 154–637 | a investigação da `LIGHTBAR-BT-CLAIM-01` (quatro reinícios do daemon) |
| 16h–21h | 42 | máquina parada |
| **21h** | **2064** | **ela começa a jogar** |
| **22h** | **3519** | o pico |
| **23h** | **1681** | até `23:37`, quando o último controle cai |

**A sessão de jogo é `21:05` → `23:37` de 02/08.** Tudo que segue foi medido
nessa janela.

### O placar de níveis

```
6947  [info]
  35  [warning]
   0  [error]     <- nenhum erro
   0  [critical]
```

**Zero erros.** Isso importa: o que a machucou **não levanta exceção** — são
avisos e transições de estado que, somados, tornam o Bluetooth inutilizável.
Uma suíte de 6792 testes verdes e um journal sem `error` convivem com uma noite
de jogo ruim. É exatamente por isso que este documento existe.

### Os 35 avisos, agrupados

| evento | vezes | o que significa |
|---|---:|---|
| `motion_reader_open_failed` | 10 | o giroscópio não abriu — `/dev/hidrawN` sumiu |
| `uhid_rumble_preso_expirado` | **4** | **o rumble preso VOLTOU**, nos dois jogadores |
| `touchpad_reader_read_lost` | 4 | o touchpad perdeu o device (`Errno 19`) |
| `motion_sensors_read_lost` | 4 | idem, sensores |
| `evdev_read_lost` | 4 | idem, o device principal |
| `evdev_grab_failed` | 2 | **EBUSY** — *"o controle pode dobrar input"* |
| `system_check_warning` | 2 | WirePlumber fixou o DualSense como mic padrão |
| `state_stale_neutral_warning` | 2 | o `evdev_reader` pode não ter conectado |
| `x11_query_failed` / `x11_connect_failed` | 2 | o display `:1` caiu às 23:37 |
| `wmctrl_binary_not_found` | 1 | **binário ausente na máquina** |

---

## O achado principal: o gesto de religar o controle abre a Steam

Este é o achado de melhor relação causa/sintoma da noite, e ele **não estava em
nenhuma hipótese anterior**.

### O que o log mostra, duas vezes

Primeiro episódio, `21:09:57`:

```
21:09:57.118  uhid_motion_streaming      on=False player=1
21:09:57.123  touchpad_reader_read_lost  [Errno 19] path=/dev/input/event256
21:09:57.132  motion_sensors_read_lost   [Errno 19] path=/dev/input/event31
21:09:57.153  evdev_read_lost            [Errno 19] path=/dev/input/event30
21:09:57.163  ps_solo_released           held_ms=5038.2          <-- CINCO SEGUNDOS
21:09:57.196  steam_spawn_requested
21:09:57.196  ps_button_action_steam     outcome=spawned
21:09:57.219  motion_reader_open_failed  [Errno 2] /dev/hidraw5
        (a Steam sobe: "Steam is not running: No such device or address")
21:09:59.348  evdev_started              path=/dev/input/event257
21:09:59.348  evdev_grab_failed          [Errno 16] EBUSY
                                         hint='o controle pode dobrar input'
```

Segundo episódio, `21:10:41`, 44 segundos depois:

```
21:10:41.479  uhid_motion_streaming      on=False player=1
21:10:41.486  touchpad_reader_read_lost  [Errno 19] path=/dev/input/event259
21:10:41.495  motion_sensors_read_lost   [Errno 19] path=/dev/input/event258
21:10:41.519  evdev_read_lost            [Errno 19] path=/dev/input/event257
21:10:41.525  ps_solo_released           held_ms=5032.8          <-- CINCO DE NOVO
21:10:41.538  wmctrl_binary_not_found
21:10:41.538  ps_button_action_steam     outcome=refocus_fallback_spawn
21:10:41.538  steam_spawn_requested                              <-- abriu OUTRA VEZ
...
21:10:43.700  controller_primary_bound   transport=usb           <-- ELA FOI PRO CABO
21:10:43.754  evdev_grab_failed          [Errno 16] EBUSY
21:10:44.116  coop_player_removed        players=1
```

### A ordem dos milissegundos é o achado

Repare: **os devices morrem ANTES do PS ser solto** — `.479` o motion desliga,
`.486/.495/.519` os três readers perdem o device, e só em `.525` vem o
`ps_solo_released`. A sequência não é *"ela apertou PS e as coisas quebraram"*.
É o contrário:

> **O controle caiu. Ela segurou o botão PS por cinco segundos para religá-lo —
> que é como se liga um DualSense. E o Hefesto, ao ver o botão ser solto, abriu
> a Steam.**

Duas vezes em 45 segundos. Na segunda, com a Steam já aberta, o `wmctrl` não
existe nesta máquina, o refocus caiu no fallback e ele **abriu a Steam de
novo**.

### A causa-raiz, provada no código

`integrations/hotkey_daemon.py:212-224`:

```python
if long_press_fired:
    # Long-press ja disparou neste hold — o release não abre Steam.
    ...
    return None

# Release sem combo nem long-press — considera PS solo (toque curto).
held_ms = (t - pressed_at) * 1000
logger.info("ps_solo_released", held_ms=round(held_ms, 1))
self._fire_ps_solo()
```

**Não existe teto de duração.** O comentário diz *"toque curto"* e o `README.md`
promete *"PS (toque curto) → abre a Steam"* — mas a única coisa que impede um
hold longo de virar "toque" é o `long_press_fired`, que depende de
`ps_long_press_ms`. E esse campo nasce **`0` = desligado**, por decisão
deliberada em `daemon/main.py`:

> *"Default 0 = long-press DESLIGADO (evita o modo-jogo acidental); quem quiser
> o gesto seta `HEFESTO_DUALSENSE4UNIX_PS_LONG_PRESS_MS>0`."*

Com o long-press desligado, `long_press_fired` é **sempre `False`** — e
**qualquer** duração cai no ramo do toque curto. Um hold de 5.038 ms abre a
Steam.

**E isso explica o que já funcionava** (a regra da casa): no cabo o controle não
cai, então ninguém segura o PS para religar; e quando ela dá um toque curto de
verdade, o comportamento é o desejado. O defeito só aparece na combinação
*"Bluetooth instável + o gesto natural de recuperação"* — que é precisamente a
noite dela.

### O elo seguinte: EBUSY derruba o jogador

O `evdev_grab_failed` não é cosmético. `daemon/subsystems/coop.py:264-271`
documenta que o `sync` **derruba o jogador** quando o grab falha:

> *"Derruba e recria um jogador quando: o controle sumiu; o node evdev do MESMO
> controle mudou; ou o EVIOCGRAB falhou (`BUG-COOP-GRAB-SILENT-FAIL-01` — sem
> grab confirmado o físico dobraria o input no jogo; derrubar aqui garante retry
> a cada ciclo)."*

A decisão está certa — input dobrado é pior. Mas o efeito na mesa dela é que
**o Jogador 2 dura dois segundos**.

---

## O segundo achado: o primário e o co-op disputam o MESMO device

No segundo episódio, o `event30` aparece duas vezes com dois donos:

```
21:10:41.866  evdev_started            path=/dev/input/event30
21:10:41.867  coop_player_grab_pending path=/dev/input/event30  player=2   <-- co-op
...
21:10:43.700  controller_primary_bound transport=usb                       <-- o primário MUDOU
21:10:43.754  evdev_started            path=/dev/input/event30             <-- primário
21:10:43.754  evdev_grab_failed        [Errno 16] EBUSY                    <-- colisão
21:10:44.116  coop_player_removed      players=1
```

O co-op pegou o `event30` como Jogador 2 às `.867`. Dois segundos depois o
primário foi rebindado e apontou para o **mesmo** `event30` — e o grab do
primário bateu no grab do co-op. `EBUSY` não veio da Steam nem do jogo: **veio
de dentro do próprio daemon.**

O `sync` do co-op tem uma guarda para isto (`coop.py:326-333`,
`BUG-COOP-BOOT-PRIMARY-DUP-01`): ele adia o spawn enquanto o primário não
resolveu o MAC. A guarda cobre o **boot**. **Não cobre a troca de primário em
runtime**, que é o que a reconexão por Bluetooth provoca o tempo todo.

---

## O terceiro achado: o rumble preso voltou — e a cura de 02/08 está funcionando

Os dois fatos convivem, e é isso que torna o achado útil.

```
5922  uhid_parada_do_sdl_honrada     <- a cura de 02/08 (commit 5801de9) FUNCIONA
   4  uhid_rumble_preso_expirado     <- e mesmo assim o rumble prendeu
```

Os quatro travamentos:

```
21:52:05  player=2  silencio_s=5.69  teto_s=3.0  ultimo=(12, 0)
21:52:15  player=1  silencio_s=3.36  teto_s=3.0  ultimo=(230, 230)
21:52:15  player=2  silencio_s=3.29  teto_s=3.0  ultimo=(114, 114)
21:52:33  player=2  silencio_s=3.9   teto_s=3.0  ultimo=(127, 0)
```

Numa janela de 50 segundos em torno deles, **43** paradas do SDL foram honradas.
O discriminador da `BT-E-VPAD-01` (furo 6) está reconhecendo as paradas — e
ainda assim `(230, 230)` ficou pendurado até o teto de 3 s cortar.

**Logo: existe uma segunda causa, e ela não é a do SDL.** A pista está a um
segundo de distância:

```
21:52:05  uhid_rumble_preso_expirado  player=2
21:52:06  sensor_hub_reader_iniciado  identity=14:3a:9a:00:00:ab  tipo=motion
21:52:06  sensor_hub_reader_iniciado  identity=a0:fa:9c:00:00:f0  tipo=motion
21:52:15  uhid_rumble_preso_expirado  player=1 e player=2 no MESMO milissegundo
```

Os readers dos **dois** controles reiniciaram entre o primeiro e o segundo
travamento, e os dois jogadores travaram juntos. A hipótese que sobrevive é:
**quando o device do jogo desaparece — reconexão de Bluetooth, vpad recriado,
jogador derrubado — o jogo nunca chega a mandar a parada, e o último valor fica
no motor até o teto.** A cura de 02/08 trata o caso em que o jogo *manda* a
parada; este é o caso em que ele *não chega a mandar*.

A própria `BT-E-VPAD-01` previu isto ao manter o teto: *"A cura tira a causa
conhecida; a rede continua para as desconhecidas."* Esta é uma das
desconhecidas, e agora tem nome.

---

## O quarto achado: o daemon desistiu do jogo no meio da partida

```
21:26:15  game_signal_transition   de=daemon  evidencia=game                  para=game
21:28:14  game_signal_transition   de=game    evidencia=daemon_histerese_expirada  para=daemon
21:28:16  uhid_game_session_end          player=2
21:28:16  game_session_devolvida   lightbar=True player_leds=True triggers=['left','right']
21:28:16  uhid_game_session_end          player=1
21:28:16  game_session_devolvida   lightbar=True player_leds=True triggers=['left','right']
```

O jogo foi detectado às `21:26:15` e **dois minutos depois** a autoridade voltou
para o daemon por *histerese expirada* — e o daemon **tomou de volta a lightbar,
os LEDs de jogador e os dois gatilhos** dos dois jogadores, com o jogo ainda
aberto.

Isso não é novidade: é exatamente a
[`SINAL-DE-JOGO-01`](../sprints/2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md),
**ABERTA desde 31/07**. O que este documento acrescenta é **a prova de que ela
acontece em partida real, com dois jogadores, e de que o custo é visível**: os
gatilhos adaptativos que o jogo tinha configurado foram devolvidos no meio.

Às `23:37` a mesma sequência se repete, agora com `triggers=[]`.

---

## O quinto achado: os controles externos nunca viram jogador do co-op

Na fila dela havia **três** controles externos, restaurados do disco:

```
21:05:07  external_fila_restaurada  ordem={'e0:f6:b5:00:00:53': 3,
                                           'e4:17:d8:00:00:1a': 4,
                                           'e4:17:d8:00:00:83': 5}
```

(`E4:17:D8` é o OUI da 8BitDo — dois deles. O terceiro é o outro externo.)

Eles ganham número, ganham LED (`external_led_written slot=3`, nove vezes na
sessão) — e **nunca aparecem em `coop_player_added`**. O contador `players`
nunca passou de **2** na noite inteira.

A causa está em `daemon/subsystems/coop.py:334-338`:

```python
want = {
    mac: str(path)
    for mac, path in discover_dualsense_evdevs().items()   # <-- SÓ DualSense
    if mac != primary
}
```

**Isto não é regressão — é o desenho.** Os externos chegam ao jogo pelo caminho
direto (o próprio evdev, que o SDL enxerga), sem vpad e sem passar pelo co-op.
Foi assim que os quatro controles jogaram em 25/07.

**O que é defeito é a promessa.** O `README.md` diz *"Com mais de um controle
plugado, cada um vira um jogador — co-op local sem configurar nada"* e
*"Controles de outras marcas entram como jogadores adicionais"*. Para o
DualSense isso quer dizer *"ganha um controle virtual próprio"*; para o externo
quer dizer *"ganha um número e uma luz"*. São duas coisas diferentes ditas com
a mesma frase — e com quatro controles na mesa a diferença aparece.

---

## O sexto achado: `wmctrl` não existe, e ninguém pede

```
21:10:41.538  wmctrl_binary_not_found
21:10:41.538  ps_button_action_steam  outcome=refocus_fallback_spawn
```

Conferido na máquina: **`wmctrl` não está instalado**. E:

- o `install.sh` **não o instala** — zero ocorrências;
- o `packaging/debian/control` **não o declara** — zero ocorrências;
- o `scripts/doctor.sh` **não o confere** — zero ocorrências;
- só o `integrations/steam_launcher.py` o usa (`WMCTRL_BINARY = "wmctrl"`,
  linha 30), para trazer a janela da Steam ao foco.

O degradar é honesto (cai para `spawn`), mas o efeito é o pior possível no
contexto: em vez de focar a Steam que já está aberta, **abre outra**.

---

## O que ficou REFUTADO nesta medição

Vale tanto quanto os achados, e evita que a próxima sessão persiga fantasma.

### O nó de sysfs da lightbar NÃO sumiu

A hipótese 1 que a `BT-E-VPAD-01` deixou aberta (*"o nó demora a aparecer no BT
— se for isso, é corrida e vai voltar"*) **não se reproduziu**. Todas as oito
coberturas da sessão saem limpas:

```
21:06:58  sysfs_led_cobertura  cobertos=['14:3a:9a:00:00:ab']  sem_no_sysfs=[]
21:07:44  ...                  cobertos=[os dois]              sem_no_sysfs=[]
21:09:59  ...                  cobertos=['a0:fa:9c:00:00:f0']  sem_no_sysfs=[]
21:10:23  ...                  cobertos=[os dois]              sem_no_sysfs=[]
21:10:43  ...                  cobertos=['14:3a:9a:00:00:ab']  sem_no_sysfs=[]
21:19:09  ...                  cobertos=[os dois]              sem_no_sysfs=[]
21:28:23  ...                  cobertos=[os dois]              sem_no_sysfs=[]
23:37:04  ...                  cobertos=['14:3a:9a:00:00:ab']  sem_no_sysfs=[]
```

**`sem_no_sysfs` vazio em todas.** A hipótese continua aberta como
possibilidade, mas perdeu a prioridade: em duas horas e meia de uso pesado, com
reconexões constantes, ela não apareceu uma vez.

### O `ps_solo` NÃO derrubou os controles

A leitura ingênua do primeiro episódio seria *"o botão PS derrubou tudo"*. A
ordem dos milissegundos refuta: os `read_lost` vêm **antes** do
`ps_solo_released`. O botão é a **reação** dela à queda, não a causa. Inverter
isso mandaria a cura para o lugar errado.

### Não houve erro, crash nem exceção

Zero `[error]`, zero `[critical]`, zero `Traceback` na sessão inteira. Quem
procurar stack trace não vai achar. **O produto falha por composição de
comportamentos corretos**, e é por isso que 6792 testes unitários verdes não
contradizem a noite dela.

---

## A linha do tempo que resume a noite

```
21:05  ela liga tudo — 2 DualSense + 3 externos na fila
21:06  o 14:3a:9a:00:00:ab conecta por BT e vira o primário
21:07  o a0:fa:9c:00:00:f0 entra como Jogador 2          <- 2 jogadores
21:09  os dois caem · ela segura PS 5 s · a STEAM ABRE · grab EBUSY
21:10  o Jogador 2 sai                                   <- 1 jogador
21:10  volta · ela segura PS 5 s · a STEAM ABRE DE NOVO (sem wmctrl)
21:10  ELA PLUGA O CABO (transport=usb) · grab EBUSY · o Jogador 2 sai
21:19  o Jogador 2 volta                                 <- 2 jogadores
21:26  o jogo é detectado
21:28  o daemon DESISTE do jogo (histerese) e devolve lightbar/LEDs/gatilhos
21:28  ELA PLUGA O CABO DE NOVO (transport=usb)
21:52  RUMBLE PRESO em P1 e P2, quatro vezes em 28 s
23:37  o último controle cai · o X11 do display :1 morre · fim
```

**Em 22 minutos: quatro ciclos de entra-e-sai do co-op, duas aberturas
indesejadas da Steam, dois `EBUSY`, e ela indo para o cabo duas vezes.**

Essa é a resposta medida para *"todos os problemas antigos voltaram"* — e para
o requisito que ela definiu:

> *"deixar o projeto robusto de tal forma que eu não note que estou no bt ou
> cabo, a ideia é termos tudo funcionando via bt principalmente."*

Hoje o Bluetooth não é uma variante do cabo. É um modo em que o controle cai, o
gesto de recuperação abre a Steam, o jogador dura dois segundos e o rumble fica
preso.

---

## O que este documento NÃO mediu

Honestidade sobre os limites, para ninguém tratar suposição como fato:

- **por que o controle cai** — os `Errno 19` provam que o device sumiu, não
  dizem se foi o rádio, o BlueZ, o firmware ou a coexistência com o Wi-Fi. A
  `BT-SDP-VAZIO-01` cobre uma causa conhecida (bond sem SDP); pode não ser esta;
- **se a lightbar estava apagada** durante a partida. Os `sem_no_sysfs` limpos
  dizem que o nó existia; a `LIGHTBAR-BT-CLAIM-01` já provou que **nó certo não
  quer dizer barra acesa**, e essa medição exige o olho dela;
- **se o input dobrou de fato.** O `evdev_grab_failed` traz o `hint` de que
  *pode* dobrar; ela é quem sabe se dobrou;
- **o que aconteceu no display `:1`** às 23:37;
- **a taxa do giroscópio** (o furo 5 da `BT-E-VPAD-01`) — continua não medida, e
  só pode ser medida contra a SDL3 que a Steam distribui.
