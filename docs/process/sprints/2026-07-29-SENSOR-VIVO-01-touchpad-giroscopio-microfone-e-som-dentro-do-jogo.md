# SENSOR-VIVO-01 — touchpad, giroscópio, microfone e som dentro do jogo

- **Status:** LEVANTAMENTO MEDIDO — nenhuma linha de código nesta rodada. O que
  esta página faz é responder, com caminho e linha, quais dos quatro já chegam
  ao jogo e o que falta para os outros
- **Prioridade:** ALTA para o item 3 (o microfone da máquina dela **não grava
  ela agora**, e a medição está abaixo); MÉDIA para o item 2; nenhuma para o
  item 1, que já funciona
- **Aberta em:** 29/07/2026, com um DualSense no cabo, o daemon em execução e o
  vpad `P1` de pé
- **Medida ao vivo nesta máquina, hoje.** Nenhuma afirmação foi copiada de
  sprint antiga sem reconferir no hardware
- **Relacionada:**
  [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md) (o bloco do
  alto-falante na tela),
  [MIC-PRESENTE-01](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md),
  [MIC-USB-01](2026-07-25-MIC-USB-01-tres-mutes-empilhados.md) (as três camadas
  de mudo) e
  [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md).
  A [SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md), aberta na mesma
  rodada, é a irmã desta: ela decide o desenho do alto-falante **na interface**,
  enquanto esta responde pelo caminho **até o jogo**. As duas mediram o mesmo
  sink e chegaram ao mesmo número
- **Rodada:** é um dos seis documentos de 29/07; a ordem de leitura está no
  [índice da documentação da v0.3.0](../estudos/2026-07-29-INDICE-a-documentacao-da-v030.md)

## A pergunta dela, literal

> *"como vamos fazer o autofalante, o touchpad, microfone, e giroscopio
> funcionar no jogo ao vivo?"*

## A resposta, em quatro linhas

| O quê | Chega ao jogo hoje? | O que falta |
|---|---|---|
| **Giroscópio** (e acelerômetro, e o relógio do sensor) | **SIM.** Medido agora: `motion_streaming=true`, `motion_hz=189,2` | **Nada.** Está pronto desde a GYRO-01 e a aba Status não está mentindo |
| **Touchpad — o dedo** (posição, dois dedos, o rastreio de cada toque) | **SIM.** Vai junto com o giroscópio, na mesma janela de bytes | **Nada** |
| **Touchpad — o clique** (apertar o touchpad como botão) | **NÃO** | Uma linha de fiação. O descritor está pronto, o codificador está pronto, e o nome do botão existe — ele só nunca é entregue ao caminho do jogo |
| **Microfone** | **Não é assunto do gamepad** — o jogo pega o microfone pelo PipeWire, nunca pelo vpad | Hoje a fonte padrão do sistema é o **monitor do alto-falante do controle**: quem gravar pega o áudio de SAÍDA. E o perfil da placa está preso numa entrada que não capta |
| **Alto-falante** | **Não é assunto do gamepad** — o áudio sai pela placa USB do controle, pelo PipeWire | Quem manda no volume é o PipeWire, e agora ele diz `Mute: yes` a 40 % |

**Dois dos quatro já funcionam e a sprint não vai propor trabalho para eles.**
Os outros dois nunca passaram pelo controle virtual — e essa é a informação que
faltava escrita em algum lugar.

---

## Antes de tudo: por onde o jogo enxerga o controle

Três peças, e a ordem entre elas explica todo o resto:

1. **O broker esconde o hidraw do controle FÍSICO.** É a cura da guerra de
   escritores: com daemon, Steam e jogo no mesmo uid, o dono do arquivo não
   separa ninguém, então o nó do físico perde a permissão. `broker/hidraw_broker.py:29`
   diz que o validador só aceita hidraw de DualSense físico (`054c:0ce6`) e que
   **o vpad `0df2` é rejeitado de propósito** — é por ele que o jogo fala.
2. **O vpad é um DualSense Edge virtual criado por `/dev/uhid`**
   (`integrations/uhid_gamepad.py`, PID `0x0DF2` em `uhid_gamepad.py:110`). Ele
   é o controle que o jogo enumera.
3. **O que o jogo recebe é o que entra no report 0x01 do vpad.** Se um dado não
   entra ali, ele não existe para quem está jogando.

Medido agora, com `getfacl` e `stat`:

```
hidraw5  perm=600 root:root  HID_NAME=Sony ... DualSense Wireless Controller   (ESCONDIDO)
hidraw4  perm=660 root:root  HID_NAME=Hefesto Virtual DualSense P1
         + ACL  user:vitoriamaria:rw-                                          (ABERTO)
```

O físico está escondido e o virtual está aberto para ela — exatamente o desenho.
E os quatro nós de entrada que o `hid_playstation` criou para o vpad estão
vivos, com as mesmas capacidades do controle real:

```
Hefesto Virtual DualSense P1                  event21 js0
Hefesto Virtual DualSense P1 Motion Sensors   event22 js1
Hefesto Virtual DualSense P1 Touchpad         event23 mouse2
Hefesto Virtual DualSense P1 Headset Jack     event24
```

O nó de touchpad do vpad e o do controle físico declaram **os mesmos eixos, os
mesmos limites e o mesmo número de dedos**:

```
ABS_X 0..1919   ABS_Y 0..1079   ABS_MT_SLOT 0..1
ABS_MT_POSITION_X 0..1919       ABS_MT_POSITION_Y 0..1079
ABS_MT_TRACKING_ID 0..65535     BTN_LEFT  BTN_TOUCH  BTN_TOOL_FINGER  BTN_TOOL_DOUBLETAP
```

**Ou seja: o lado do descritor está resolvido para os dois sensores.** O que
resta a discutir é só o que o daemon coloca dentro do report.

---

## 1. Giroscópio — JÁ FUNCIONA, e não há trabalho a propor

A aba Status escreve *"Giroscópio: fluindo para o jogo (~N Hz)"* em
`app/widgets/controller_card.py:600`, e ela **não escreve isso de graça**: o
texto só aparece quando `motion_streaming` é `True` **e** a taxa é maior que
zero (`controller_card.py:596-601`). Não é rótulo fixo.

A frase está certa. Resposta crua do `daemon.state_full` desta máquina, agora:

```
rumble_ff.per_vpad[0] = {
  "player": 1, "backend": "uhid",
  "motion_streaming": true,
  "motion_hz": 189.2
}
```

E o nó de sensores do vpad entregou **61 224 bytes em 3 segundos** de leitura
direta — cerca de 850 eventos por segundo, contra 1 033 do controle físico no
mesmo intervalo.

### Como o dado chega lá

A cura tem nome (GYRO-01) e mora em `core/physical_report_reader.py`. O desenho,
em três fatos:

- Uma thread abre um **segundo fd somente-leitura** no hidraw do físico — obtido
  do broker por injeção de descritor, sem reabrir por caminho — e copia
  **verbatim** a fatia `payload[15:40]` de cada report cru
  (`physical_report_reader.py:66-71`). Zero matemática no caminho: o
  `sensor_timestamp`, que o SDL usa como passo de integração e que o evdev não
  expõe, vem junto de graça.
- A fatia é entregue em `vpad.forward_motion(window)`
  (`physical_report_reader.py:554`), e no vpad ela é escrita inteira no corpo do
  report em `uhid_gamepad.py:1010` (`body[_MOTION_WINDOW] = self._motion_window`).
- **O leitor vira o relógio**: com o espelho de pé, os repasses do laço de 60 Hz
  viram só cache e quem emite é a janela nova (`uhid_gamepad.py:943`), com teto
  de 250 Hz e coalescência para não afogar o `/dev/uhid` com quatro controles.

A memória de que *"o vpad emitia zero e a cura foi o `forward_motion`"* está
certa, e a cura está no ar. Quem sobe o espelho é
`daemon/subsystems/gamepad.py:1425` (`start_motion_reader`), logo depois de o
vpad nascer; no co-op **cada jogador ganha o seu**
(`daemon/subsystems/coop.py:767`), então isto vale para P1 a P4.

Um detalhe que ainda está escrito errado e vale corrigir de passagem: a
docstring do blueprint diz *"o vpad emite motion neutro e não repassa gyro/accel
do físico"* (`integrations/uhid_blueprint.py:45`). Isso era verdade antes da
GYRO-01 e hoje é falso — e a mesma docstring avisa que, havendo passagem de
giroscópio, a calibração congelada volta a importar. Ela **já volta a importar**,
e o projeto já resolveu: o vpad recebe o feature 0x05 lido do controle daquele
jogador (`daemon/subsystems/gamepad.py:1389`), caindo no canônico só quando não
há leitura.

**Entrega desta seção: nenhuma.** Está pronto.

---

## 2. Touchpad — o dedo chega, o clique não

Este é o item que rende trabalho, e ele é menor do que parece: **dois terços já
estão prontos** e a parte que falta não é o descritor.

### O que já chega

Os **dois pontos de toque** do DualSense moram nos bytes 32 a 39 do payload —
e o intervalo copiado pelo espelho é `15..39`. Ou seja: **o touchpad viaja
dentro da mesma janela do giroscópio**, byte a byte, sem conversão.

Está declarado nos dois lados, e travado por teste:

- `integrations/uhid_gamepad.py:299-315` — os pontos ficam em 32 e 36, o byte de
  contato é **invertido** (`0x80` ligado significa dedo FORA), e sem carimbar
  esse bit o vpad nasceria com dois toques fantasma presos no canto;
- `integrations/uhid_gamepad.py:324-326` — a janela é `slice(15, 40)`, 25 bytes;
- `core/physical_report_reader.py:63-67` — os mesmos números, com o comentário
  dizendo que estão travados um no outro por teste;
- `tests/unit/test_uhid_gamepad.py:607-609` — o teste que cobra os deslocamentos
  32 e 36 e exige que o report nasça com os dois pontos inativos.

Conferido no vpad vivo agora, lendo o hidraw dele: **241 reports em 1,5 segundo**
(cerca de 160 Hz), com o byte de contato em `0x80` — ninguém com o dedo no
touchpad, que é o esperado com o controle na mesa.

### O que NÃO chega: o clique

O clique do touchpad **não está na janela de motion**. Ele é um bit de botão,
no byte 9 do payload (`_BUTTONS2_OFFSET` em `uhid_gamepad.py:264`, bit `0x02` em
`uhid_gamepad.py:302`) — fora do intervalo `15..39` que o espelho copia.

O codificador do vpad sabe montá-lo. Provado agora, chamando o codificador com o
nome do botão na mão:

```
nada                     buttons2=0x00  contato[32]=0x80
touchpad_middle_press    buttons2=0x02  contato[32]=0x80
cross                    buttons2=0x00  contato[32]=0x80
```

**O bit acende. O nome é que nunca chega até lá.** A cadeia, medida:

1. Quem produz os nomes `touchpad_left_press` / `touchpad_middle_press` /
   `touchpad_right_press` é o `TouchpadReader`
   (`core/evdev_reader.py:1244-1250`), que lê o **nó separado** do touchpad —
   `BTN_LEFT` correlacionado com o último `ABS_X`.
2. O comentário do `BUTTON_MAP` diz isso com todas as letras:
   *"touchpad_\*_press: device separado (name contém 'Touchpad'); lido por
   `TouchpadReader`"* (`core/evdev_reader.py:785-786`). O mapa do nó principal
   **não tem** entrada de touchpad.
3. O único ponto do projeto que junta as duas coisas é
   `_combine_with_touchpad`, em `daemon/subsystems/keyboard.py:210` — e ele é
   chamado em exatamente dois lugares, `keyboard.py:242` e `keyboard.py:262`:
   **o teclado virtual e só ele**.
4. O caminho do jogo não passa por ali. `dispatch_gamepad` recebe o conjunto de
   botões cru e o repassa intacto (`daemon/subsystems/gamepad.py:1531`), e esse
   conjunto vem de `evdev_buttons_once` (`daemon/subsystems/poll.py:63`), que lê
   só o nó principal do controle. O mesmo vale para o co-op
   (`daemon/subsystems/coop.py:1326`).

Portanto: **o descritor está pronto, a replicação do dedo está pronta, o
codificador está pronto. Falta entregar o nome do botão ao caminho do jogo.**

### Duas armadilhas que precisam entrar na conta

- **O cursor não pode dobrar.** Enquanto o vpad está de pé, o daemon
  deliberadamente **descarta** o movimento do touchpad para o mouse
  (`daemon/lifecycle.py:3183-3188`), e a regra `assets/76-dualsense-touchpad-libinput-ignore.rules:18`
  tira do libinput qualquer nó cujo nome case `*DualSense*Touchpad` — o que
  inclui o nó do **vpad**, pelo motivo escrito na própria regra: *"o espelho de
  report copia o touchpad físico pro vpad, então cada toque movia o cursor EM
  DOBRO dentro do jogo"*. Qualquer fiação nova tem que preservar as duas coisas.
- **No co-op, o leitor de touchpad é um só.** `daemon._touchpad_reader` é do
  primário. Existe um leitor por controle no `daemon/sensor_hub.py:321`, mas ele
  é **sob demanda** (`sensor_hub.py:110`, o carimbo `_demanda[uniq]`): ele só
  abre quando a aba Status pede. Amarrar o clique do jogo a ele faria o botão do
  jogador 2 depender de a janela estar aberta — que é exatamente a classe de
  dependência escondida que esta casa não aceita.

---

## 3. Microfone — não passa pelo gamepad, e hoje está quebrado por outro caminho

### O fato que precisa ficar escrito

**O microfone do DualSense é uma placa de som USB (ou um túnel Opus por
Bluetooth). Ele não passa pelo gamepad, não passa pelo vpad e não tem como
passar.** O jogo pega o microfone pelo PipeWire, como pegaria o de qualquer
outro aparelho. Não existe, e nunca vai existir, um "repasse de microfone do
físico para o vpad" — o report HID não tem onde pôr áudio.

Medido: a placa está lá, e é um `alsa_card` comum.

```
alsa_card.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00
alsa.driver_name = "snd_usb_audio"
device.product.id = "0x0ce6"
```

O que o vpad tem é um nó chamado **"Headset Jack"** (`event24`). Ele carrega
só as chaves de detecção de fone/microfone plugado — nenhum áudio. Confundir os
dois é fácil, e por isso está escrito aqui.

**O que o Hefesto pode fazer, então, é uma coisa só: garantir que a fonte certa
esteja publicada, disponível e não mutada.** É disso que o resto desta seção
trata.

### O que está errado agora, medido hoje

```
Default Source: alsa_output.usb-...DualSense...analog-surround-40.monitor
```

**A fonte padrão do sistema é o MONITOR do alto-falante do próprio controle.**
Quem gravar — o chat de voz do jogo, o Discord, um gravador qualquer — pega o
**áudio de saída**, não a voz dela. É a mesma medição que motivou o commit
`28bf718` de ontem, e ela continua verdadeira hoje.

A cadeia inteira, medida arquivo por arquivo:

| Onde | O que diz | Consequência |
|---|---|---|
| `~/.local/state/wireplumber/default-nodes` | `default.configured.audio.source = alsa_input...DualSense...analog-stereo` | alguém elegeu o microfone do controle como padrão |
| `~/.local/state/wireplumber/default-profile` | perfil fixado em `output:analog-surround-40+input:analog-stereo` | e fixou o perfil junto |
| `pactl list cards` | esse perfil é `available: no`, e sua única porta de entrada, `analog-input-headset-mic`, é `not available` | **a fonte eleita existe mas não tem porta viva** |
| `pactl info` | o padrão efetivo caiu no `.monitor` do alto-falante | quem grava, grava a saída |

O perfil que o ALSA declara **disponível** para entrada nesta máquina, agora, é
o outro: `output:analog-surround-40+input:iec958-stereo`.

### O que `doctor --fix-mic` cura, e o que ele NÃO cura

`scripts/doctor.sh` trata o microfone em duas camadas
(`fix_mic_dualsense`, `doctor.sh:713`):

- **Camada 1 — o mudo persistido por rota.** O WirePlumber guarda mudo e volume
  **por rota de placa** em `~/.local/state/wireplumber/default-routes` e
  restaura a cada conexão, sem nada no log. O doctor tira esse mudo, e desde
  ontem só considera rota de **captura**: a única rota muda desta máquina é
  `:output:analog-output`, o **alto-falante**, e o portão antigo reprovava o
  microfone por causa da caixa de som (`doctor.sh:539-546`). Essa parte está
  curada e é boa.
- **Camada 2 — o perfil da placa.** Esta é a que está errada nesta árvore.
- **Camada 3 — o mudo no FIRMWARE do controle.** O doctor **não cura** e nem
  tenta: isso vive no `daemon.state_full` e só se resolve por
  `hefesto-dualsense4unix mic unmute` / `mic release`.

E há duas coisas que ele **não cura de jeito nenhum**, e que precisam estar
ditas para ninguém procurar no lugar errado:

- **não decide quem é a fonte padrão** — isso é do
  `scripts/fix_wireplumber_default_source.sh` e do arquivo
  `assets/wireplumber/51-hefesto-dualsense-no-default-source.conf`, que
  **rebaixa** a prioridade do microfone do controle de propósito (a queixa que
  originou o arquivo era o controle virando entrada padrão sozinho). A subida é
  explícita: `hefesto-dualsense4unix mic promote`;
- **não devolve a posse do registrador de mudo.** Depois de um `mic unmute`, o
  botão físico do controle **para de responder** até um `mic release` — está no
  `--help` do comando e ninguém lê.

### O defeito medido: esta árvore tem a versão REFUTADA da camada 2

Este é o achado desta sprint, e ele é reproduzível em dois comandos.

Em 26/07 mediu-se que o perfil analógico — o que a MIC-USB-01 mandava escolher —
entrega **327 680 bytes de silêncio digital**, enquanto o `iec958-stereo`, que a
sprint mandava evitar, grava com pico 4 606. A cura silenciava o microfone de
quem a rodasse. O conserto foi para a `main` no commit `84d9f4e`, com o critério
certo: **só perfil que oferece fonte e que o ALSA declara `available: yes`**.

**Esse commit não está na árvore que roda nesta máquina.**

```
git merge-base --is-ancestor 84d9f4e HEAD   ->  84d9f4e NAO esta em HEAD
git branch --contains 84d9f4e               ->  main
```

E o efeito é direto. Rodando o **mesmo decisor puro** das duas versões sobre a
**mesma** saída de `pactl list cards` capturada desta máquina agora:

| Versão do decisor | Perfil alvo devolvido |
|---|---|
| `restauro/inicio-da-sessao` (o que roda) | *vazio* — veredito: "está tudo bem" |
| `main` (com o `84d9f4e`) | `output:analog-surround-40+input:iec958-stereo` |

O comentário desta árvore ainda diz, em `doctor.sh:599-601`, que *"a busca NÃO
filtra por `available`"* e que a entrada analógica *"é exatamente a que o
WirePlumber marca indisponível, e é essa que faz a source nascer RUNNING"*. É a
premissa que a medição de 26/07 derrubou.

Agravante, e por isso a prioridade é ALTA: **o `install.sh` desta árvore passou
a chamar essa cura**. `install.sh:2192` roda
`bash scripts/doctor.sh --fix-mic --quiet` no passo de áudio. Ou seja, a
instalação de ontem fixou o perfil que não capta — e é por isso que o estado
medido hoje é exatamente esse.

Que a árvore de trabalho é o que roda está confirmado: o executável instalado
aponta para o venv do repositório, com instalação editável.

```
head -1 ~/.local/bin/hefesto-dualsense4unix
#!/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/.venv/bin/python
```

### Um efeito colateral que ninguém liga ao microfone

O botão de microfone do controle, quando `mic_button_toggles_system` está ligado
(medido agora: `true`), chama `toggle_default_source_mute`
(`integrations/audio_control.py:72`), que executa
`pactl set-source-mute @DEFAULT_SOURCE@ toggle` (`audio_control.py:99`).

Com a fonte padrão sendo o **monitor do alto-falante**, apertar o botão do
microfone **muta e desmuta o monitor da saída** — não o microfone. O botão
parece não fazer nada, ou fazer coisa estranha. É consequência do item acima, e
some junto com ele.

---

## 4. Alto-falante — quem manda no volume

Mesma família do item 3, do lado da saída: **o áudio do jogo vai para o
alto-falante do controle pelo PipeWire**, através do sink USB da placa do
controle. Não passa pelo vpad, não passa pelo report HID.

Se o jogo mandar áudio para o alto-falante do controle, **quem manda no volume é
o PipeWire** — e a resposta dele agora é:

```
Sink: alsa_output.usb-...DualSense...analog-surround-40
Mute:  yes
Volume: 40 % (-23,88 dB) nos quatro canais
Active Port: analog-output
```

E o estado persistido concorda: em `default-routes`, a rota
`...:output:analog-output` está com `"mute": true`. **O alto-falante do controle
está mudo, e vai continuar mudo depois de reiniciar** — é a camada 1 do
microfone, aplicada à saída. O doctor **vê e não conserta de propósito**
(`doctor.sh:665-673`): silenciar a caixa de som pode ter sido escolha dela, e
uma cura de microfone não pode ser disparada pelo alto-falante. A linha sai como
informação, nunca como reprovação. Essa decisão está certa e fica.

### O segundo botão de volume, o que ninguém vê

Existe um **segundo** controle de volume, independente do PipeWire: um
registrador no report de saída do próprio controle. Ele é a trava de posse
AUDIO-OWNER-01.

- Os quatro bytes de áudio (fone, alto-falante, microfone, roteamento) ficam em
  `common[4..7]` e cada um tem o seu bit de autorização no `flag0`
  (`core/backend_pydualsense.py:232-235`).
- Antes da posse, **os bits de áudio saem todos zerados e o firmware conserva o
  que tinha** (`backend_pydualsense.py:624-629`). Isso existe porque a
  biblioteca de origem mandava `flag0=0xFF` sem nunca escrever os bytes — ou
  seja, mandava "volume 0" a cada report, e mandava "desmuta o microfone" por
  cima do kernel.
- A posse só é assumida quando alguém deste projeto escreve um valor, via
  `speaker.set` (`daemon/ipc_handlers.py:2506`).

E o preço dessa posse é **irreversível por leitura**: o DualSense não devolve o
volume. Não há report de entrada nem feature que leia esse registrador. Por isso
`daemon.state_full` só passa a trazer a chave `speaker` **depois** de um
`speaker.set` — e medido agora ela vem `null`, o que quer dizer que **ninguém
nunca escreveu**, e o firmware segue dono.

**A resposta à pergunta, então, é em duas partes:**

1. Para o áudio do jogo, quem manda no volume é o **PipeWire** — sink, mudo, e o
   mixer ALSA da placa (`PCM` e `Headset` no `amixer -c`). É onde ela deve mexer,
   e é o que qualquer aplicativo respeita.
2. O registrador HID é um **atenuador do firmware**, um segundo botão em série
   com o primeiro. Ele existe, o protocolo o suporta, e o produto
   deliberadamente não o toca — porque o primeiro clique tira o volume do
   firmware para sempre, sem caminho de volta por leitura. Essa decisão já está
   escrita na [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md) e **não
   muda aqui**.

---

## Entregas

Critério de aceite escrito como **o que ela vê ou sente**, não como o que o
código faz.

### E1. O microfone volta a gravar ela — trazer o decisor corrigido para esta árvore

Portar para `restauro/inicio-da-sessao` o critério do `84d9f4e`: o alvo de perfil
só sai quando o ativo **não serve** (sem fonte de captura, ou `available: no`) e
existe alternativa que o ALSA declare disponível; sem alternativa de verdade, não
troca nada.

Depois disso, desfazer o estado que a instalação de ontem deixou: o perfil
fixado em `default-profile` e a fonte eleita em `default-nodes`.

- **Aceite 1:** ela grava três segundos falando e **ouve a própria voz**. Pico
  maior que zero no medidor, e não os 327 680 bytes de zeros.
- **Aceite 2:** o medidor de microfone da aba Status **se mexe quando ela fala** —
  hoje ele se mexeria com a música tocando, porque está olhando a saída.
- **Aceite 3:** rodar `install.sh` de novo **não** reintroduz o defeito.
- **Prova de que o teste morde:** com o `84d9f4e` arrancado, o decisor devolve
  alvo vazio para a captura desta máquina — e o teste tem que reprovar por isso.

### E2. A fonte padrão do sistema deixa de ser o monitor de um alto-falante

Um monitor de saída **nunca** é resposta certa para "qual é o microfone". A
eleição da fonte padrão passa a recusar qualquer nó terminado em `.monitor`, e a
promoção explícita (`mic promote`) passa a conferir que a fonte que ela está
elegendo **tem porta de captura viva** antes de gravar a escolha — senão ela
elege algo que o WirePlumber vai descartar no próximo settle, que é exatamente o
que aconteceu aqui.

- **Aceite:** `pactl info` não mostra `.monitor` na fonte padrão, nem logo depois
  de instalar, nem depois de desconectar e reconectar o cabo do controle.

### E3. O botão do microfone para de mexer no volume da música

Consequência direta de E2, mas com aceite próprio porque o sintoma é outro e ela
sente separado.

- **Aceite:** com música tocando, ela aperta o botão de microfone do controle e
  **a música não muda**. O que muda é o microfone — e o LED do controle
  acompanha.

### E4. O clique do touchpad chega ao jogo

Entregar ao caminho do jogo o nome do botão de touchpad que hoje só o teclado
virtual recebe, preservando as duas armadilhas da seção 2: o movimento do dedo
continua descartado para o cursor enquanto o vpad está de pé, e o nó do vpad
continua fora do libinput.

Para o co-op, o leitor tem que ser do caminho do jogo — **não** o do
`sensor_hub.py`, que é sob demanda da janela.

- **Aceite 1:** num jogo que usa o touchpad como botão (mapa, inventário,
  placar), apertar o touchpad **abre a coisa**. Hoje não abre.
- **Aceite 2:** o clique funciona para o jogador 2 **com a janela do Hefesto
  fechada**.
- **Aceite 3:** o cursor do mouse **não** anda enquanto ela desliza o dedo dentro
  do jogo — nem uma vez, nem duas.
- **Prova de que o teste morde:** arrancar a fiação e o teste tem que reprovar
  contando cliques em zero num report em que o dedo aparece.

### E5. A faixa do alto-falante para de dizer "não ajustado" quando o sistema é quem mutou

Hoje o bloco só sabe falar do registrador HID, do qual ninguém tomou posse — e
então diz "não ajustado" mesmo com o PipeWire dizendo `Mute: yes` a 40 %. São
duas verdades diferentes, e a que importa para ela é a do PipeWire, porque é a
que decide se sai som.

- **Aceite:** com o sink do controle mudo, a faixa diz que **o sistema** está com
  o alto-falante mudo, e diz onde desfazer. Não diz "não ajustado".
- **O que NÃO entra NESTA sprint:** o controle deslizante de volume do
  registrador HID. Não é veto — é divisão de trabalho. O preço da posse (o
  primeiro clique tira o volume do firmware e não há leitura para confirmar a
  devolução) foi levantado pela SOM-01, e o **desenho** desse controle, com o
  preço medido byte a byte e as quatro armadilhas executadas, é a
  [SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md), aberta na mesma
  rodada. As duas se encaixam: a E5 aqui faz a faixa dizer a verdade da
  **camada 1** (o PipeWire, que é quem decide se sai som), e a SOM-02 decide o
  que fazer com a **camada 2** (o registrador HID). A ordem importa — mexer na
  camada 2 com a camada 1 muda não produz som nenhum, e é a armadilha que a
  SOM-02 põe como primeiro passo do roteiro de validação dela. A decisão sobre
  a camada 2 é dela, e continua sem código nas duas páginas.

### E6. Giroscópio e posição do dedo: nada a fazer

Declarado como entrega para que ninguém proponha de novo. Os dois já chegam ao
jogo. O único débito é de **texto**: a docstring do
`integrations/uhid_blueprint.py:45` ainda afirma que o vpad não repassa
giroscópio, o que é falso desde a GYRO-01.

- **Aceite:** a docstring passa a dizer a verdade, e diz que a calibração por
  unidade **já** importa e **já** é lida por jogador.

---

## Como provar — quatro experimentos, um comando cada

Todos são de leitura. Nenhum escreve em nada.

### Giroscópio — o vpad está entregando IMU?

```sh
E=$(grep -A5 "Hefesto Virtual DualSense P1 Motion" /proc/bus/input/devices | grep -om1 'event[0-9]*'); timeout 3 cat /dev/input/$E | wc -c
```

Aqui devolveu **61 224**. Zero significaria gyro morto no jogo. Qualquer número
grande significa que está fluindo.

### Touchpad — o dedo chega e o clique não

```sh
H=$(for h in /sys/class/hidraw/*; do grep -qx 'HID_NAME=Hefesto Virtual DualSense P1' "$h/device/uevent" && basename "$h"; done); timeout 10 python3 -c "import sys,time;f=open('/dev/$H','rb',buffering=0);n=c=d=0;t=time.time()
while time.time()-t<8:
    r=f.read(64)
    if len(r)<40: continue
    n+=1; c+= bool(r[10]&2); d+= not (r[33]&0x80)
print('reports:',n,'com clique:',c,'com dedo:',d)"
```

Passe o dedo pelo touchpad e **aperte** durante os oito segundos. O resultado que
esta sprint prevê é `com dedo` maior que zero e **`com clique` igual a zero**.
Quando a E4 estiver entregue, os dois têm que subir.

### Microfone — quem está sendo gravado

```sh
LC_ALL=C pactl info | grep "Default Source"
```

Aqui devolveu `alsa_output...DualSense...analog-surround-40.monitor`. Se aparecer
`.monitor`, quem grava está gravando o som que **sai**, não a voz dela.

E, para medir se a fonte do controle realmente capta:

```sh
timeout 3 parec --device=alsa_input.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.analog-stereo --format=s16le --rate=48000 --channels=1 | od -An -tu2 -v | awk '{for(i=1;i<=NF;i++){v=$i+0;if(v>32767)v=65536-v;if(v>m)m=v}}END{print "pico:", m+0}'
```

Fale durante os três segundos. **Pico 0 é silêncio digital** — a fonte abre e
entrega zeros, que é o defeito da camada 2. Pico nas milhares é o microfone
funcionando.

### Alto-falante — quem está segurando o volume

```sh
LC_ALL=C pactl list sinks | grep -A9 "Name: alsa_output.usb.*DualSense" | grep -E "Mute:|Volume:|Active Port:"
```

Aqui devolveu `Mute: yes` e 40 %. É o PipeWire, não o firmware — e o registrador
do firmware segue sem dono, o que se confirma pela chave `speaker` vindo `null`
no `daemon.state_full`.

---

## O que fica de fora, e por quê

- **Gatilhos adaptativos e vibração** não entram aqui. Eles já têm caminho
  próprio, nos dois sentidos: o jogo escreve no vpad e o REPLICA-03 leva o bloco
  cru até o controle físico daquele jogador
  (`integrations/uhid_gamepad.py:1286`). Não é assunto de sensor.
- **O microfone por Bluetooth** não entra. Por rádio não existe placa de som:
  é Opus tunelado dentro do HID, e isso tem sprint própria
  ([MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md)).
  O que esta página afirma sobre o cabo não foi medido por rádio hoje.
- **O controle deslizante de volume do alto-falante** não entra, pelo motivo já
  decidido e já escrito na SOM-01: o preço da posse é dela para pagar, não
  minha para cobrar. O desenho desse controle, se ela quiser, é assunto da
  [SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md).
- **A calibração por unidade** não vira trabalho aqui. Ela já está lida por
  jogador (`daemon/subsystems/gamepad.py:1389`); só a docstring do blueprint
  ficou para trás, e isso é a E6.
- **Nada foi testado dentro de um jogo nesta rodada.** As medições são do daemon
  vivo, dos nós de entrada, do hidraw do vpad e do PipeWire desta máquina. O
  aceite dos quatro é ela abrindo o jogo — e para o item 2 o aceite exige o dedo
  dela no touchpad, que nenhuma medição minha substitui.
