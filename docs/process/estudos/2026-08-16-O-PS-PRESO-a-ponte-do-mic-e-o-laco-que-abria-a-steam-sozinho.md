# O PS preso — a ponte do mic, e o laço que abria a Steam sozinho

**16/08/2026, 20:16–20:19.** Defeito NOVO, grave, causado por mim durante a
bancada. Registrado com a sequência inteira porque ele tem três partes, e cada
uma sozinha já é um problema.

> *"tive que desligar o controler pq o teclado, o mouse (tava teclando sem parar
> e o botão direito do mouse também), cara, foi muito mas muito estranho,
> desliguei o controle e parou fiquei com medo"* — ela
>
> *"esse problema dessa forma em especifico eu não tinha visto antes. storm ok,
> mas mouse e teclado funcionando com vida própria foi novo."*

**Não era storm, e não era o teclado.** Era o daemon tentando abrir a Steam em
laço, disparado por um botão PS que ficou preso.

---

## A sequência, do log

**20:16:00** — subi a ponte do mic BT à mão (`GerenciadorMicBluetooth`), para
medir o custo de banda. A ponte pegou o `/dev/hidraw5` pelo broker:

```
20:16:00  hidraw_broker_fd_recebido   node=/dev/hidraw5 state=hidden
20:16:00  bt_mic_source_publicada     source=hefesto_dualsense_bt_…
20:16:00  bt_mic_pedido               ligar=True no=/dev/hidraw5 seq=1
```

**20:19:26** — o botão PS começa a disparar sozinho, várias vezes por segundo:

```
ps_button_action_steam   outcome=refocus_fallback_spawn
steam_spawn_requested
ps_solo_released         held_ms=295.0
wmctrl_binary_not_found
ps_button_action_steam   outcome=refocus_fallback_spawn
steam_spawn_requested
ps_solo_released         held_ms=331.7
…
```

**20:19:27** — o controle cai inteiro, todos os leitores de uma vez:

```
touchpad_reader_read_lost   errno 19   event28
motion_sensors_read_lost    errno 19   event27
evdev_read_lost             errno 19   event26
motion_reader_open_failed   errno 2    /dev/hidraw5
controller_disconnected     reason=probe_offline
```

## As três partes, e cada uma é um defeito

### 1. A ponte do mic disputa o hidraw com os leitores do daemon

A ponte lê `/dev/hidraw5` — o MESMO nó de onde o `motion_reader` lê. Não há
arbitragem entre os dois: o broker entrega o fd para quem pedir. O resultado
medido foi estado de botão corrompido.

É a armadilha nº 3 desta casa (*o instrumento briga com o produto*), agora entre
dois pedaços do próprio produto.

**Nota honesta:** a correlação temporal é forte (3 minutos entre subir a ponte e
o laço, e nada mais mudou na máquina), mas **o mecanismo exato não foi isolado**
— não sei dizer se a ponte consome bytes que faltam ao reader, se corrompe o
offset, ou se a carga derruba o link. Ficam as duas coisas registradas: a
correlação, e o que ainda não se sabe.

### 2. O PS preso vira um laço de spawn, sem nenhum freio

Com o botão presumido pressionado, cada leitura dispara
`ps_button_action_steam`. Não há debounce, nem limite de tentativas, nem
"já pedi isso há 200 ms". **Um botão preso vira uma enxurrada de janelas.**

### 3. `wmctrl_binary_not_found` transforma foco em spawn

O caminho feliz é *trazer a Steam para frente*. Sem o `wmctrl`, ele cai no
fallback de **abrir a Steam** — que é uma ação muito mais cara e visível. Numa
máquina sem `wmctrl` (esta), todo pedido de foco vira um lançamento.

O binário faltando é logado como `warning` e nunca é apresentado a ela.

## O que fica curado agora

- ponte parada, módulo do PipeWire descarregado, `bt_mic: enabled=false`;
- nenhum source `hefesto_dualsense` no sistema;
- a emulação de mouse/teclado do daemon **já estava desligada** e não teve parte
  nisso (medido: `mouse_emulation.enabled=false`,
  `keyboard_emulation.despachando=false`).

## O que fazer, em ordem

1. **Arbitrar o hidraw.** A ponte do mic e o `motion_reader` não podem abrir o
   mesmo nó sem se conhecerem. O broker já é o dono da posse — é ele que tem de
   recusar o segundo pedido, ou multiplexar.
2. **Debounce no PS.** Nenhum botão deve poder disparar ação de janela mais de
   uma vez por N ms. Vale para o PS e para qualquer atalho que abra programa.
3. **`wmctrl` ausente tem de aparecer para ela**, não ficar num warning: sem
   ele, "focar" vira "abrir", e a diferença é enorme.
4. **A ponte do mic não volta a subir sem o item 1.** O gate dela caducou por
   dois motivos (o storm foi curado no kernel; a banda não caiu — medido hoje,
   131 → 339 reports/s), mas **ganhou um motivo novo e melhor**: ela não é
   segura enquanto disputar o hidraw.

## O que este episódio custou, e o que ensinou

Custou o susto dela e uma sessão interrompida. Ensinou que **medir também é
mexer**: subi uma ponte de produção à mão, no meio de uma bancada, para colher
um número — e a régua virou o defeito.

A regra que fica, irmã da de hoje mais cedo (*um ensaio mede um gesto*):

> **Instrumento que ESCREVE ou que toma posse de um recurso não é instrumento —
> é mudança de estado.** Só entra com o mesmo cuidado de uma cura: uma variável
> por vez, e com o caminho de volta pronto ANTES.
