# Índice — onda "Harmonia" (2026-07-15)

Pedido da mantenedora, madrugada de 2026-07-15, com dois controles conectados
(1 USB + 1 BT) e o programa aberto na tela:

> "estude o projeto e veja o que fizemos. A interface, nome dos botões está de difícil
> entendimento para um leigo. resolvemos muita coisa, mas os botões, conflitos tão
> aparecendo. esse quadrado do click não deveria aparecer, ninguém conecta dois
> controles no pc esperando que os dois controles controlem a mesma pessoa. ele deveria
> ficar confirmado por default mas não aparecer pro user. fora que ao vivo só se o
> controle xbox 360 tiver selecionado que ele funciona. todas as opções deveriam
> funcionar, inclusive jogar direto pelo da sony. fizemos todas as alterações na raiz
> mas não foi verificado conflito de melhoria de cada aba da interface por palavras mais
> simples e direta e não foi pensado no conflito entre todas elas em si. […] a ideia é
> que ao final possamos ter 4 controles dsx conectados ao mesmo tempo seja 2 por bt ou
> usb e todas as features de cada aba devem funcionar pra todos, precisamos vender melhor
> o programa. […] tá permitido linguagem baixa a nível kernel pra resolvermos tudo, e
> tudo deve funcionar via script install e afins."
>
> "já descobrimos a solução pra todos os problemas só não cuidamos da harmonia e
> coexistência entre o todo. além da estética e qualidade."

## Como esta onda foi levantada

- **9 áreas do código lidas por agentes** (uma por aba/subsistema): 84 bugs, 44
  conflitos entre abas, 51 lacunas de multi-controle, 270 textos de interface.
- **Tour ao vivo das 10 abas** com os 2 controles reais (screenshots por aba).
- **PoC de kernel** executado na máquina de teste — que mudou o plano (ver abaixo).

## O achado que reorganizou tudo

A queixa *"só funciona se o Xbox 360 estiver selecionado"* **não é um bug de UI**. É uma
consequência da fundação: o gamepad virtual nasce de `/dev/uinput`, que **não tem
hidraw** — e o SDL, ao ver a máscara DualSense, procura o hidraw para vibrar e não acha.

O mesmo defeito explica as células "MORTO/IMPOSSÍVEL" da matriz de paridade
(`2026-07-13-sprint-paridade-de-features.md`): gatilhos adaptativos, lightbar,
giroscópio, touchpad e bateria no vpad.

**PoC provado ao vivo nesta máquina**: criando o vpad por **`/dev/uhid`**, o driver
`hid_playstation` do kernel faz bind e registra um **DualSense completo** — com hidraw,
lightbar, LEDs de jogador, motion sensors, touchpad — e o **rumble do jogo chega até
nós** (`UHID_OUTPUT`). Uma troca de fundação cura a queixa nº 3 inteira e meia dúzia de
"limitações" documentadas.

## Os sprints

| # | Sprint | O que entrega | Por que nessa ordem |
|---|---|---|---|
| 1 | [`SPRINT-UHID-VPAD-01`](2026-07-15-sprint-uhid-dualsense-de-verdade.md) | O vpad vira um DualSense de verdade: **as duas máscaras vibram**, lightbar/gatilhos/gyro/touchpad no vpad, fim do controle duplicado sem launch options | Cura a raiz. Vários itens dos outros sprints **desaparecem** depois dele — fazer antes evita trabalho jogado fora |
| 2 | [`SPRINT-HARMONIA-01`](2026-07-15-sprint-harmonia-um-dono-por-conceito.md) | Um dono por conceito: modo, mouse/teclado, máscara, alvo, desligar, sincronização | É a queixa central ("harmonia e coexistência"). Depende do 1 para saber o que sobra |
| 3 | [`SPRINT-LEIGO-01`](2026-07-15-sprint-leigo-fala-de-gente.md) + [anexo (270 textos)](2026-07-15-anexo-inventario-de-textos.md) | O checkbox de co-op some; a interface fala português de gente | Reescrever texto de tela que o 1 e o 2 vão apagar é desperdício |
| 4 | [`SPRINT-4P-01`](2026-07-15-sprint-4-jogadores.md) | 4 controles USB+BT com **todas** as features de **todas** as abas | Depende da fundação por-controle e da higiene de dispositivos |
| 5 | [`SPRINT-INFRA-01`](2026-07-15-sprint-infra-o-install-garante.md) | O install garante tudo: paridade nos 5 formatos, `doctor.sh` cobrindo o que o install faz, feature morta "abrir GUI ao plugar", flags contraditórias, BT e 4 controles | Fecha *"tudo fácil a nível de no install garantirmos o funcionamento de tudo"*. Pode andar **em paralelo** — quase não toca a GUI |
| 6 | [`SPRINT-ESTETICA-01`](2026-07-15-sprint-estetica-um-so-sistema.md) | A interface parece um sistema só: tokens, um padrão de título/margem, contraste AA, foco, e os 4 controles cabendo na tela | Polimento sobre telas já estáveis. **Exceção**: `EST-10` (código acoplado a texto de UI) e `EST-11` (i18n) têm de vir **antes** do `LEIGO-03`, que renomeia a aba "Daemon" |

## O que já foi feito nesta sessão (2026-07-15, madrugada)

Fundação do sprint 1 entregue e **provada no hardware**, não só em teste:

- **`integrations/uhid_gamepad.py`** (novo): `UhidDualSense` + `capture_dualsense_blueprint`.
  Interface espelhando a do `UinputGamepad` (`start`/`stop`/`is_active`/`pump_ff`/
  `ff_last_sent`/`ff_play_count`) para o co-op trocar de backend sem cirurgia.
  Verificado ao vivo: `Registered DualSense controller`, hidraw próprio, `leds/rgb:indicator`
  + `white:player-1..5`, Motion Sensors, Touchpad, Headset Jack, e o **rumble do jogo
  chegando ao `rumble_sink`** — `(200,100)` → `(0,255)` → `(0,0)` escritos no hidraw do vpad
  chegaram intactos. 16 testes herméticos (`tests/unit/test_uhid_gamepad.py`, fd falso).
- **`assets/71-uhid.rules`** + wiring nos **três** caminhos de instalação (native, flatpak,
  deb) e no uninstall. Provado: `getfacl /dev/uhid` → `user:vitoriamaria:rw-`, e o vpad é
  criado **sem sudo**.
  - Achado no caminho: a regra **precisa** ser < 73. Quem vira a tag `uaccess` em ACL é a
    `/usr/lib/udev/rules.d/73-seat-late.rules`; numerada 79, o `MODE` aplicava e a **ACL
    não** — `/dev/uhid` continuava root-only. Renomeada 79 → 71.
  - Corrigido de brinde um achado da auditoria: faltava
    `udevadm trigger --subsystem-match=misc` — sem ele as regras de `/dev/uinput` e
    `/dev/uhid` só valiam **no próximo boot** (co-op de 4 jogadores morto até reiniciar).
- **Dois HIGH da aba Início** (`HARM-15` e o card fantasma), com testes
  (`tests/unit/test_home_render_state.py`).

- **Dois fixes de harmonia com teste**: a CLI `gamepad on` **preservava** a máscara em vez
  de forçar `dualsense` (`HARM-08` — matava o rumble de quem tinha Xbox), e o applet parou
  de ter o mesmo default divergente. Um teste de paridade trava os três defaults (Python,
  Rust, daemon) — verificado que ele **falha** quando o bug é reintroduzido.
- **O `doctor.sh` passou a ver o que o install faz** (`INFRA-05`): conhece a
  `71-uhid.rules`, checa `/dev/uhid` e o driver `hid_playstation`. E o `check_uinput`
  deixou de dar **falso positivo** — ele só olhava se o nó *existia*, então dizia "presente"
  com o nó root-only e o daemon incapaz de criar vpad nenhum; agora checa se é **gravável**.
  Verificado ao vivo: com o `/dev/uhid` em 0600 o doctor avisa e explica o que se perde; o
  trigger do install cura.

**O review adversarial (41 agentes) achou um defeito grave no meu próprio fix** e vale
registrar, porque é a lição da noite: eu havia checado o `valid_flag0` com `& 0x01`
(COMPATIBLE_VIBRATION). Os dois DualSense desta máquina têm firmware **0x0630**, que ativa
o `use_vibration_v2` do driver — nele o rumble chega com **HAPTICS_SELECT (0x02) sozinho**.
O fix descartaria **100% da vibração** no hardware alvo, e a suíte ficava **verde** porque o
fixture do teste mandava justamente o bit que o hardware nunca manda. Corrigido para a
máscara `0x03`, com o teste parametrizado nos três firmwares.

Gate: **2080 testes**, `ruff` 0.15.20 e `mypy` limpos.
Prova final end-to-end, no hardware: force-feedback via evdev no vpad (o caminho que o jogo
usa) com `strong=0x8000/weak=0x4000` → o `rumble_sink` recebeu **`(64, 128)`**, exatamente
o esperado.

Falta, no sprint 1: `UHID-02` (encoder de input report + ligar o passthrough ao rumble do
daemon; o backend ainda não tem call site — falta `for_flavor`/`forward_analog`/
`forward_buttons` e um `Protocol` comum com o `UinputGamepad`), `UHID-03` (lightbar/LED por
jogador via os LEDs do próprio vpad), `UHID-04` (esconder o físico por udev), `UHID-05` (UI),
`UHID-06` (fallback) e `UHID-07` (validação em jogo).

## Invariantes da onda (valem para todo sprint)

1. **Nenhuma opção visível pode não funcionar.** Se não funciona, não é oferecida — ou
   diz, em português simples, por que está desabilitada.
2. **Um conceito, um dono, um nome** — em GUI, applet, CLI, TUI e documentação.
3. **Nada de singular**: nenhuma tela fala de "o controle" quando podem ser quatro.
4. **Sem jargão na tela**: `daemon`, `uinput`, `hidraw`, `máscara`, `vpad`, `co-op`,
   `unit`, `rc=`, `KEY_*`, `regex`, `JSON` só no modo avançado.
5. **Validação ao vivo obrigatória** por sprint, com os controles reais (1 USB + 1 BT
   hoje; 4 na meta). Teste verde sem validação ao vivo não fecha item.
6. **Gate antes de qualquer tag**: `pytest` + `ruff check src/ tests/` (pinado 0.15.20).
7. **Tudo pelo `install.sh`**: nada de passo manual (regra da casa: se pip/apt ad-hoc for
   preciso, vira dependência declarada).

## Evidências ao vivo coletadas (2026-07-15, 2 controles)

- **6 joysticks para 2 controles**: `js0` físico USB, `js1` Motion Sensors USB, `js2`
  físico BT, `js3` Motion Sensors BT, `js4`/`js5` vpads. O grab de evdev **não** esconde
  o nó `js`; os sensores viram joystick; os vpads têm o **mesmo nome** dos físicos.
- **Estado inicial da máquina da mantenedora**: modo "Jogar pelo Hefesto" com a máscara
  **DualSense (sem vibrar)** selecionada — ou seja, o default real dela era justamente o
  que não vibra. Enquanto isso a aba Emulação exibia "Modo jogo LIGADO — mouse/teclado
  suspensos": dois conceitos de "modo" na tela ao mesmo tempo.
- **PoC uhid**: `playstation 0003:054C:0CE6.000C: Registered DualSense controller` +
  `hidraw6` + `leds/rgb:indicator` + `leds/white:player-1..5` + Motion Sensors +
  Touchpad + Headset Jack + `UHID_OUTPUT` (rumble) recebido.
