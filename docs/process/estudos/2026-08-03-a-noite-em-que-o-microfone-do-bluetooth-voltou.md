# A noite em que o microfone do Bluetooth voltou

- **Medido em:** 03/08/2026, das 21:00 às 21:40, no hardware dela, com dois
  DualSense por Bluetooth
- **Método:** um suspeito de cada vez, com gravação de áudio real e leitura do
  hidraw cru. Nenhuma linha do produto foi alterada durante a medição
- **Companheiro:** [a noite em que medimos a lightbar do Bluetooth](2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md)
  — as duas descobertas são da mesma sessão e têm **a mesma forma**

---

## O VEREDITO

> **O microfone por Bluetooth parou de funcionar em 25/07/2026 às 14:20, e a
> causa foi uma cura CORRETA.**
>
> Até aquele instante o daemon mandava, em **todo** report BT,
> `valid_flag1` com `POWER_SAVE_CONTROL_ENABLE` e `common[9] = 0x00` — ou seja,
> **"desmuta"**, a cada 0,5 s pelo keepalive. Era um *escritor sem dono*, e o
> commit `3d9bb7e` (`AUDIO-OWNER-01`) o removeu — **corretamente**.
>
> **Só que era ele que mantinha o microfone vivo.** Desde então nada, em lugar
> nenhum da árvore, limpa aquele bit. O firmware **retém** o mudo.

### A ironia das doze horas

| hora (25/07) | commit | o que aconteceu |
|---|---|---|
| **02:08** | `43d0f0a` | **o WAV que provou o mic BT foi gravado** — dos dois controles |
| **14:20** | `3d9bb7e` | a cura do `AUDIO-OWNER-01` removeu o escritor sem dono |
| **14:24** | `5115aac` | o README publicou *"~40% do sinal, causa em aberto"* |

**A medição foi feita doze horas antes de ser invalidada, e o número foi
publicado quatro minutos depois.** Ninguém tinha como notar: quem mediu não
sabia que a cura viria, e quem curou não sabia que a medição dependia do que
estava removendo.

---

## O que foi MEDIDO em 03/08

### 1. O silêncio era digital, não fraco

Duas gravações pelo `parec`, na source que a ponte publica:

| condição | duração | pico | zeros |
|---|---|---|---|
| daemon vivo | 8,9 s | **0** / 32767 | **100%** |
| daemon **parado** | 10,2 s | **0** / 32767 | **100%** |

Não é sinal fraco nem ruído: é **zero absoluto**.

### 2. O firmware afirmava "mudo", com o LED apagado

Lidos 40 reports crus do hidraw do controle:

```
byte 55 = 0x04  em 40 de 40 reports      (MIC_MUDO ligado, CONSTANTE)
```

E o LED do botão de microfone estava **apagado** — ver a ressalva do item 5,
que é o que torna essa observação inútil como prova.

**Os offsets estão certos, e isto foi conferido:** o byte vizinho (54) vale
`0x08`, que decodifica como bateria 85% — batendo com o que o daemon reporta.
**Não há off-by-one** entre `states[54]` (`core/backend_pydualsense.py:234`) e
`raw[55]` (`integrations/dualsense_bt_audio.py:235`): a pydualsense descarta um
byte no BT.

### 3. O A/B que o próprio código pedia — e o resultado inverte o suspeito

`integrations/dualsense_bt_audio.py:123-131` registrava, antes desta noite:

> *"**Principal suspeito não testado**: existe um SEGUNDO escritor de `0x31`
> neste device — o próprio daemon do hefesto […] O A/B decisivo — medir o ciclo
> de trabalho do MUDO com o poll do daemon parado — **NÃO foi feito** porque
> parar o daemon estava fora do que esta tarefa podia tocar. **É o primeiro
> experimento a rodar quando alguém retomar isto.**"*

**Executado em 03/08:**

| condição | `mudo` |
|---|---|
| daemon **vivo** | 46% → 66% |
| daemon **parado** | **100%** |

**O daemon não é a causa — ele estava aliviando por acidente.** O loop do
`mic_hotkey_toggle` (ver item 5) desmutava parte do tempo; sem ele, o mudo é
total. **Os "cerca de 40% de sinal" do README eram subproduto de um defeito.**

### 4. O bit CEDE a uma ordem nossa — e o áudio volta

O experimento decisivo, com o daemon vivo:

```
antes            byte55 = 0x04 0x04 0x04 0x04 0x04
$ hefesto-dualsense4unix mic unmute
depois           byte55 = 0x00 0x00 0x00 0x00 0x00
```

E a gravação imediatamente seguinte, com ela falando:

```
10,2 s | pico = 32768/32767 | 40% das amostras com sinal
RMS/0,5 s: 2791 171 209 144 122 110 118 235 211 176 125 …
```

**O microfone por Bluetooth voltou.** Pico em escala cheia, RMS variando ao
longo do tempo — áudio de verdade, não ruído de fundo.

E o log da ponte conta o resto: `mudo = 100% → 46% → 100%`. **Ninguém mantém a
posse**, e o firmware volta a mutar.

### 5. O LED não serve como instrumento — e por culpa nossa

`common[8]` (o LED do microfone) é escrito como **zero em todo report**, com o
`valid_flag1` bit `0x01` ligado e **sem dono declarado**
(`core/backend_pydualsense.py:690`, `:732`).

**Consequência:** *"o LED está apagado, logo o botão físico não está mutado"*
**não se sustenta** com o daemon vivo — nós forçamos o LED apagado. Durante esta
investigação essa observação foi usada como evidência e **não valia nada**.

É órfã do mesmo tipo que o `AUDIO-OWNER-01` matou, e ficou.

### 6. O loop do botão — defeito real, causa errada

Ela viu, e descreveu: *"o botão do mic tá se apertando e desligando
infinitamente"*, e depois *"não foi aperto físico meu"*. O journal prova:

```
21:01:40.696  mic_hotkey_toggle  muted=False
21:01:40.930  mic_hotkey_toggle  muted=True
21:01:41.177  mic_hotkey_toggle  muted=False
...           ~25 alternâncias em 2 segundos
```

**O daemon alternava o mute ~12 vezes por segundo enquanto a ponte estava no
ar** — dois donos do mesmo registrador (a ponte liga o mic; o `mic_button_loop`
lê a mudança como se fosse o botão e alterna de volta).

**É defeito real e independente**: o A/B do item 3 provou que ele **não** é a
causa do silêncio.

---

## O que foi REFUTADO (não reabrir)

### A hipótese dela sobre as gambiarras do storm — refutada, e o registro fica

Ela levantou, com boa razão histórica:

> *"a causa dos storms era a questão do áudio […] criamos formas de mutar o
> áudio do mic no passado pra parar o storm, mas depois conseguimos via kernel
> resolver na raiz mas acho que não desfizemos as gambiarras do passado"*

**As gambiarras existem** — e a caçada as encontrou:

| mecanismo | o que faz | instalada? |
|---|---|---|
| `assets/75-ps5-controller-disable-usb-audio.rules` | apaga o áudio USB inteiro | **não** |
| `assets/wireplumber/52-…disable-source.conf` | `node.disabled` na source do mic | **não** (opt-in, `install.sh:202` = 0) |
| `assets/wireplumber/53-…disable-output.conf` | mata sink + `.monitor` | **não** |

**Nenhuma explica o mudo por Bluetooth, e por dois motivos independentes:**

1. **nenhuma está instalada** nesta máquina;
2. **nenhuma alcançaria o BT de qualquer forma** — são `monitor.alsa.rules` e
   regra `SUBSYSTEM=="usb"`; por rádio **não há placa de som**, e um
   `node.disabled` do WirePlumber não escreve um único byte de HID.

**A intuição estava certa sobre elas serem órfãs; errada sobre serem a causa.**
E a causa real é o oposto: **não sobrou um mute — caiu um desmute.**

### A cura de raiz do storm está de pé, e é limpa

Confirmado nesta máquina em 03/08:

```
[ativo nesta sessão]        sim — /sys/module/snd_usb_audio/parameters/quirk_flags
[persistente / próximo boot] sim — /etc/modprobe.d/hefesto-dualsense-storm.conf
    054c:0ce6:ignore_ctl_error|ctl_msg_delay_1m
```

O storm era `-71` (EPROTO): o `snd-usb-audio` sondava o mixer UAC e martelava o
EP0, colidindo com o `usbhid`. A cura **tolera o erro do mixer** e **espaça os
control-transfers** — e o próprio script diz que ela *"PRESERVA mic + fone (NÃO
desliga áudio)"*, sendo a alternativa à regra 75.

---

## As três linhas de base do projeto que este estudo derruba

Todas foram medidas **com o desmutador acidental rodando por baixo**:

1. `tests/unit/test_audio_owner_report.py:12-17` — diz, verbatim, *"daemon
   rodando"*, logo *"ninguém escreve → MicMuted 0,0%"*;
2. *"sem o `0x32` estável em False (1183 reports)"*
   (`integrations/dualsense_bt_audio.py:105-108`);
3. *"ao desligar volta a False e fica"* (idem).

**A medição de 03/08 é a primeira do projeto sem contaminação** — e o resultado
limpo é: **sem ninguém escrevendo, o firmware fica MUDO.**

---

## As armadilhas desta investigação

1. **o LED como prova** — inútil, porque nós o forçamos apagado (item 5). Custou
   uma pergunta inteira e uma resposta dela que não podia decidir nada;
2. **medir com o daemon vivo** — ele desfaz escrita de sysfs alheia em ≤30 s
   (`NUMA-03`) e alterna o mute pelo hotkey. Toda medição de áudio precisa
   declarar se o daemon estava no ar;
3. **o CLI mente por antecipação** — `mic unmute` imprime *"o controle declara
   MUDO"* porque relê antes de o firmware convergir, e a mensagem manda a
   usuária para o WirePlumber, que é o lugar errado. O hidraw cru, um segundo
   depois, mostra `0x00`;
4. **a ponte não persiste** — morre com o processo do CLI. Uma medição que
   dependa dela precisa mantê-la viva.

---

## O que fica ABERTO

- **falta o caminho de devolução** — o desmute existe como *comando*, não como
  *ciclo de vida*: quem liga a ponte deve assumir o registrador, e quem a
  desliga deve devolver. É a sprint `MIC-BT-DONO-01`;
- **o `common[8]` sem dono** — a órfã do LED (item 5). É a `LED-SEM-DONO-01`;
- **quem repõe o mudo depois** — medido que volta (`100% → 46% → 100%`), não
  medido **quem** o repõe: o firmware por conta própria, ou o kernel;
- **os textos que afirmam o contrário** — `README.md:270-280` (os 40%),
  `docs/usage/bluetooth.md:104-105` (*"áudio por BT fora de escopo"*, falso desde
  25/07), `cli/cmd_mic.py:15` (afirma que o install instala os drop-ins 52/53 —
  não instala) e `integrations/dualsense_bt_audio.py:123-131` (o *"suspeito não
  testado"*, testado hoje).

---

## A lição de método, e ela vale mais que o achado

**As duas descobertas desta noite têm a mesma forma:**

| | lightbar | microfone |
|---|---|---|
| o que quebrou | o `0x08` **entrou** como cura (18/07) | o desmute **saiu** numa cura (25/07) |
| a cura era certa? | não — nunca curou nada | **sim**, o escritor sem dono tinha de sair |
| quem mediu depois? | ninguém | ninguém |
| o texto acompanhou? | não | não — e publicou o número inválido 4 min depois |

> **Uma cura sem medição posterior é uma aposta.** As duas custaram duas semanas
> de sintoma cada, e as duas foram resolvidas em minutos quando alguém mediu com
> o hardware na mão, um suspeito de cada vez.
