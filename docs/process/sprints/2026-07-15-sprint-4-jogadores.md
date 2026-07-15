# Sprint SPRINT-4P-01 — quatro jogadores de verdade

Pedido da mantenedora (2026-07-15): *"a ideia é que ao final possamos ter 4 controles
dsx conectados ao mesmo tempo seja 2 por bt ou usb e todas as features de cada aba devem
funcionar pra todos."*

Estado real hoje (51 lacunas levantadas pela auditoria): o **co-op funciona** — cada
controle físico vira um jogador com seu vpad. Mas **todo o resto do programa é
mono-controle**: as abas configuram o "primário" e mostram o "primário"; o estado
desejado é global; a identidade dos controles é posicional.

Regra deste sprint: **nenhuma tela pode falar de "o controle" no singular.**

## Fundação (precisa vir antes)

- `4P-01` — **Estado desejado por controle.** `_desired` é hoje **um único perfil
  global** (`core/backend_pydualsense.py`): é impossível ter cor/gatilho/rumble
  diferentes por jogador, e um ajuste feito "só no Controle 2" **vaza para qualquer
  controle** no hotplug (mesmo achado do `HARM-10`).
  **Aceite**: 2 controles com cores e gatilhos diferentes; desplugar/replugar um não
  contamina o outro.

- `4P-02` — **Identidade estável, não posicional.** "Controle N" é o índice na lista de
  handles: com hotplug, o Controle 2 vira 1 e leva junto os ajustes do outro.
  Ancorar em MAC/serial, com o slot de jogador **preservado** entre reconexões.
  **Aceite**: desplugar o P1 e replugar → ele volta como P1 (não vira P2).

- `4P-03` — **Identidade visível.** Hoje os cards P1–P4 são só texto e o único
  identificador é `…c311f0`. Casar **cor da lightbar** + **LED de jogador** + chip
  colorido na UI: o Controle 2 é "o azul".
  **Aceite**: dá para saber qual controle é qual **sem** ler MAC.

## Por aba (todas hoje mono-controle)

- `4P-04` — **Status**: a linha Conexão/Transporte/Bateria/Perfil é **fixa no glade** e
  todo o live-view (sticks, botões, gatilhos, bateria) vem só do primário. Com 4
  controles, os outros 3 são invisíveis.
  **Aceite**: sticks/gatilhos/bateria de cada controle, selecionável.

- `4P-05` — **Gatilhos, Rumble, Lightbar**: nenhuma tem seletor de controle — configuram
  implicitamente o primário/alvo global e escondem isso.
  **Aceite**: cada aba diz e escolhe em qual controle escreve (padrão: todos).

- `4P-06` — **Microfone por controle.** O botão do mic só é lido do primário e os
  drop-ins do WirePlumber suprimem **todos** os DualSense de uma vez.
  **Aceite**: mutar o mic do P3 não muta o do P1.

- `4P-07` — **Touchpad e mouse por controle.** Existe **um** `TouchpadReader` global,
  ancorado num device; mouse/teclado leem só o primário.
  **Aceite**: definir qual controle move o cursor; os demais não interferem.

- `4P-08` — **Perfis com alvo.** O esquema não permite "este perfil configura o controle
  N". E — crítico — **co-op default `False` no esquema sabota o 4P**: qualquer perfil de
  jogo salvo com a seção Modo desliga o co-op ao ativar (mesmo achado do `LEIGO-01`).
  **Aceite**: perfil pode ter ajuste por jogador; nenhum perfil desliga o co-op.

- `4P-09` — **Applet, CLI, TUI e tray.** O daemon **já envia** `controllers[]` com
  bateria/uniq/player — e nenhuma dessas superfícies usa: o applet mostra uma linha de
  bateria (a do primário), a CLI `status` traz um único transporte, a TUI ignora
  multi-controle inteiro, o tray mostra só a contagem.
  **Aceite**: as quatro superfícies listam os 4 controles com bateria e jogador.

## Escala (o que quebra em 4, não em 2)

- `4P-10` — **Throttle no teto.** Com 4 controles o output roda no limite
  (`0.008*4 = 0.032s`, capado em `REPORT_THREAD_THROTTLE_MAX_S`) — e o GIL já é gargalo
  conhecido. Medir antes de prometer.
  **Aceite**: bench com 4 vpads publicado; latência de rumble dentro do aceitável.

- `4P-11` — **Layout com 4.** Os cards da Início estão num `GtkBox` **horizontal
  homogêneo sem wrap nem scroll** (estouram com 4); o seletor de alvo vira 5 toggles
  empilhados.
  **Aceite**: 4 controles cabem na janela, inclusive estreita/tiling do COSMIC.

- `4P-12` — **Timeout do applet.** 250 ms fixo, enquanto ligar o modo com co-op cria N
  vpads — piora linearmente com 4 (a GUI já usa 2,0 s).
  **Aceite**: sem falso "Daemon desconectado" ao ligar o modo com 4 controles.

## Higiene de dispositivos (a raiz da duplicação)

- `4P-13` — **O jogo enxerga o dobro do que deveria.** Medido ao vivo com **2**
  controles: **6 joysticks** (`js0` físico USB, `js1` Motion Sensors USB, `js2` físico
  BT, `js3` Motion Sensors BT, `js4`/`js5` vpads). Com 4 controles, até 12.
  O grab de evdev **não** esconde o nó `js` (joydev é outro handler) e o hidraw físico
  segue visível ao SDL/HIDAPI. A aba Emulação ainda **exibe essa lista crua**.
  Ver `SPRINT-UHID-VPAD-01` (`UHID-04`): com o vpad tendo nome e MAC próprios, dá para
  esconder o físico e os sensores por udev — sem launch options.
  **Aceite**: 4 controles em modo vpad → o jogo vê **exatamente 4** gamepads.

- `4P-14` — **USB+BT do mesmo controle.** Input e output podem acabar em **transportes
  diferentes**, escolhidos por ordem de enumeração e não por política (plugar o cabo
  para carregar durante o jogo é o caso clássico). Há ainda o **handle zumbi**: se a
  thread morre com a chave ainda enumerada, o reconcile **nunca repara** — rumble/LED
  daquele controle morrem em silêncio para sempre.
  **Aceite**: política explícita de transporte; teste que mata a thread e verifica o
  reparo.

## Validação ao vivo

- Agora (hardware disponível): **2 controles, 1 USB + 1 BT** — todo item acima que couber.
- Meta: **4 controles** (2 USB + 2 BT). Sem esse teste, o sprint **não fecha** — a
  auditoria mostrou que tudo até hoje foi provado com 2, e 3P/4P nunca foi exercitado.
- Roteiro: 4 conectados → 4 jogadores no jogo, 4 cores diferentes, 4 LEDs corretos,
  vibração independente, bateria de cada um, desplugar o P2 no meio (os outros seguem),
  replugar (volta como P2).

## Ordem

4P-13 (a duplicação é o que dói) → 4P-01/02/03 (fundação) → 4P-04/05 → 4P-08 → 4P-09 →
4P-06/07 → 4P-10/11/12 → 4P-14.
