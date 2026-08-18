# BT-E-VPAD-01 — o que só existe no cabo, e os seis furos do gamepad virtual

- **Status:** o defeito 1 e os furos 1, 2 e 6 ENTREGUES em 02/08/2026. Os
  defeitos 2 e 3 (a lightbar no BT) e os furos 4 e 5 seguem ABERTOS — ver o fim
- **Status anterior:** PROPOSTA, escrita em 01/08/2026
- **Prioridade:** ALTA para os dois defeitos de Bluetooth (ela os encontrou
  usando); MÉDIA para os furos
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)
- **Referência:** [o protocolo canônico](../../protocol/dualsense-referencia-canonica.md)

## A hipótese dela, confirmada por medição

Com o controle no Bluetooth, ela notou que a lightbar estava apagada e que o
botão do microfone não obedecia. E disse:

> *"engraçado que os gatilhos funcionam no BT. Talvez algo não esteja pareado
> pra tudo funcionar via BT — cada uma das features esteja setada pra funcionar
> só via cabo, o que é um erro de design nosso."*

**Está certa.** Esta casa já tem isso registrado com nome: *"a premissa
USB-é-o-mundo"*, listada como bug recorrente. Os dois defeitos abaixo são duas
instâncias novas dela.

## Defeito 1 — o botão do microfone alterna o microfone ERRADO no Bluetooth

**Medido em 01/08:** com o controle no BT, `pactl list short cards | grep -i
dualsense` devolve **zero**. No Bluetooth o DualSense **não tem placa de som
nenhuma** — o áudio vai dentro dos reports HID e depende da ponte deste projeto
(que é opt-in e estava desligada).

O código do botão (`daemon/subsystems/hotkey.py`, `mic_button_loop`) faz:

```python
muted = await daemon._run_blocking(audio.toggle_default_source_mute)
await daemon._run_blocking(daemon.controller.set_mic_led, muted)
```

Ou seja: alterna o mudo da **fonte padrão do sistema** e acende o LED do
controle para refletir esse estado. **No cabo isso funciona** porque a fonte
padrão é o próprio controle. **No Bluetooth a fonte padrão é outra coisa** —
nesta máquina, o microfone da placa-mãe.

**A prova no log**, três toques dela:

```
20:15:54  mic_hotkey_toggle  muted=True
20:16:31  mic_hotkey_toggle  muted=True
20:16:43  mic_hotkey_toggle  muted=True
```

Sempre `True`, porque não é o microfone do controle que está sendo alternado.

**A cura tem de decidir o que o botão significa**, e são três opções com preços
diferentes:

- **(a)** o botão só age quando a fonte padrão **é** o controle; fora disso,
  não mexe em nada e o LED não mente. É a mais honesta e a mais barata;
- **(b)** o botão passa a mutar o **registrador do firmware** (o
  `power_save_control` bit4), que existe nos dois transportes — mas isso **toma
  a posse** e o botão físico para de valer, que é o oposto do que ela espera de
  um botão físico;
- **(c)** no Bluetooth, o botão comanda a **ponte de mic por BT**, se ela
  estiver de pé.

**Aceite:** com o controle no BT, apertar o botão do mic ou faz algo verdadeiro
no microfone do controle, ou não faz nada — nunca muta outro dispositivo.

## Defeito 2 — a lightbar apagada no Bluetooth

**Medido no mesmo log:**

```
lightbar_reset_enviado    key=a0:fa:9c:00:00:f0
sysfs_led_cobertura       cobertos=[]  sem_no_sysfs=['a0:fa:9c:00:00:f0']
```

O daemon manda o reset de LED e **acredita ter aplicado** — o `state_full`
reporta `lightbar_rgb: [255,128,0], on: True, source: desired`. A luz está
apagada.

A pista está na segunda linha: **no Bluetooth o LED não tem nó em sysfs**. O
caminho de escrita por sysfs, que é o normal no cabo, não existe ali — e o
caminho por report HID (que funciona, como os gatilhos provam) ou não está
sendo usado, ou está sendo desfeito.

**Contexto que esta casa já tem**, e que precisa ser relido antes de mexer:
`LIGHTBAR-BT-ADOPT-01`, `LIGHTBAR-BT-RESET-01`, `LIGHTBAR-BT-RESET-03` e
`LIGHTBAR-BT-KEEPALIVE-01` — todos em `core/backend_pydualsense.py`, todos
provados ao vivo em 17-22/07. **A cura não pode desfazer nenhum deles.**

**A primeira entrega é diagnóstica, não corretiva:** descobrir se o report de
cor está sendo escrito no BT e sendo ignorado, ou se não está sendo escrito.
São duas causas diferentes com curas opostas.

**Aceite:** com o controle no BT, aplicar uma cor na aba Lightbar acende o LED —
ou a tela diz por que não pode.

## Defeito 3 — a tela mente sobre a lightbar

Independente da causa acima: o `state_full` diz `source: desired` e a GUI mostra
a cor aplicada, com o rodapé escrevendo *"Cor aplicada no controle (100% de
brilho)"*. **Isso é afirmar o que não se mediu** — a mesma família da
`APLICAR-VERDADE-01`.

**Cura:** `desired` significa "mandamos", não "está aceso". A tela precisa
distinguir os dois, como o rodapé aprendeu a fazer com as seções do perfil.

## Os seis furos do gamepad virtual

Levantados em 01/08 cruzando o que os jogos esperam com o que o vpad entrega.

### Furo 1 — o nome não contém "Wireless Controller"

O vpad se chama `Hefesto Virtual DualSense P1`. Sob Proton esse nome vira o
`FriendlyName` do lado Windows, e **jogos casam por essa substring** para achar
o controle e o device de áudio.

Incoerência interna: o fallback uinput **acerta**
(`Sony Interactive Entertainment DualSense Edge Wireless Controller`), o uhid
não.

**Cura barata:** `DualSense Wireless Controller (Hefesto P1)` — mantém a
distinção humana e contém a substring. O `phys` (`hefesto-vpad`) e o `uniq`
(MAC forjado) continuam sendo o discriminador real do daemon, então nada quebra.

### Furo 2 — o byte 53 nunca é escrito

`_encode_body` escreve o byte 52 (bateria) e **nunca o 53**, que carrega
`HP_DETECT`, `MIC_DETECT` e `MIC_MUTE`.

Com zero fixo, **o vpad anuncia "fone e microfone sempre plugados"** — e esse é
o **pior default possível** para o caso do alto-falante que ela quer: um jogo
que só roteia som para o alto-falante quando não há fone vai achar que sempre
há.

**Cura:** espelhar o byte 53 do físico. O dado está fora da janela de motion
(15..39), então precisa de caminho próprio — igual ao que já foi feito para o
clique do touchpad.

### Furo 3 — os bytes de áudio do jogo são descartados em silêncio

O `_replicate_from_output` replica quatro categorias (gatilhos, lightbar,
player-LEDs) e ignora os sete campos de áudio. Ver a
[PARIDADE-SONY-01](2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md),
que trata disso com portão de medição.

### Furo 4 — o PID do Edge é invisível para uma classe de jogos

O vpad usa `0x0DF2` (Edge) para desduplicar do físico. Jogos que fixam
`0x0CE6` (o DualSense comum) **não o reconhecem** — é um defeito documentado no
hardware real do Edge também.

**Não é argumento para voltar a `0x0CE6`** (o motivo do Edge continua válido),
mas é um limite que precisa estar **documentado** e, idealmente, configurável
por perfil.

### Furo 5 — o vpad se declara Edge e entrega a taxa do comum

O SDL, ao ver um Edge por USB, anuncia giroscópio a **1000 Hz**. O espelho
entrega os ~250 Hz do físico. Um jogo que integre velocidade angular pela taxa
declarada teria **escala 4× errada** na mira por movimento.

**Não medido.** Verificação barata: comparar a taxa que o SDL reporta com a
medida.

### Furo 6 — a causa-raiz do rumble preso

Está documentada na
[referência canônica](../../protocol/dualsense-referencia-canonica.md), §8, com
o discriminador exato que separa "parada do SDL" de "report de gatilho". O
comentário no código diz *"isto é MITIGAÇÃO, não a cura"* — a cura existe agora.

## Testes que vão reprovar

`pytest tests/unit -k "lightbar or mic or hotkey or uhid or replica"`.

Atenção aos que travam as curas de BT já pagas (`LIGHTBAR-BT-*`) — elas foram
provadas ao vivo e **não podem ser desfeitas** por esta leva.

## O que NÃO fazer

- **Não desfazer as curas de lightbar por BT** de 17-22/07. Releia os quatro
  comentários antes de tocar.
- **Não fazer o botão do mic tomar a posse do registrador** sem decidir
  explicitamente — é o oposto do que se espera de um botão físico.
- **Não voltar o PID para `0x0CE6`** sem resolver a desduplicação.
- **Não medir taxa de giroscópio contra a `libSDL2` do sistema.** Ver a lição
  de método no estudo de 01/08.

---

## O que foi entregue — 02/08/2026

### Defeito 1 — o botão do mic parou de mutar o microfone errado

Escolhida a saída **(a)**, a mais honesta e barata: `fonte_padrao_e_o_controle`
pergunta ao PipeWire se o microfone padrão é o do DualSense, e o
`mic_button_loop` **não age** quando não é.

A **(b)** (mutar o `power_save_control` bit4, que existe nos dois transportes)
foi recusada pelo motivo escrito na sprint: ela **toma a posse** e faz o botão
físico parar de valer — o oposto do que se espera de um botão físico.

Em caso de dúvida a resposta é `False` e o botão não mexe em nada: não fazer
nada é sempre melhor que mutar o microfone errado.

### Furo 1 — o nome do vpad

`Hefesto Virtual DualSense P1` → **`DualSense Wireless Controller (Hefesto P1)`**.

A distinção humana fica, e nada quebra: o discriminador do daemon nunca foi o
nome — é o `phys` (`hefesto-vpad`) e o `uniq` (MAC forjado por jogador).

### Furo 2 — o byte 53

`forward_jack` espelha `HP_DETECT`, `MIC_DETECT` e `MIC_MUTE` do físico. Só os
**três bits conhecidos** passam: repassar bit desconhecido é a mesma classe de
erro que autorizar um campo de áudio sem escrever valor nele.

### Furo 6 — a CURA do rumble preso

O comentário do `uhid_gamepad.py` dizia, desde 25/07: *"isto é MITIGAÇÃO, não a
cura. A cura seria descobrir por que o stop se perde"*. **Descobriu-se.**

No `SDL_hidapi_ps5.c`, o SDL liga `ucEnableBits1 |= 0x02` só quando há rumble;
ao PARAR, deixa os bits desligados para restaurar os haptics de áudio — e o
report de parada sai com `valid_flag0 == 0`, `valid_flag1 == 0` e os motores
zerados. **O gate de `_VIBRATION_FLAGS` descartava exatamente esse report.**

O gate continua certo pelo motivo certo (report de gatilho traz motores
zerados). O que faltava era o discriminador, e ele é limpo — três testes o
travam, um por caso.

**O teto de silêncio FICA**, e não é redundância: o log de 25/07 registrou 17
disparos em 90 minutos de jogo, com valores presos que desenham um fade-out
cujo último passo se perdeu. A cura tira a causa conhecida; a rede continua
para as desconhecidas.

## O que ficou ABERTO, e por quê

- **Defeitos 2 e 3 (a lightbar apagada no BT, e a tela que mente sobre ela).**
  A própria sprint diz que *"a primeira entrega é diagnóstica, não corretiva:
  descobrir se o report de cor está sendo escrito no BT e sendo ignorado, ou
  se não está sendo escrito — são duas causas diferentes com curas opostas"*.
  **Isso exige o controle dela no Bluetooth, ao vivo.** E o risco é alto: há
  quatro curas de BT provadas ao vivo em 17-22/07 (`LIGHTBAR-BT-ADOPT-01`,
  `-RESET-01`, `-RESET-03`, `-KEEPALIVE-01`) que não podem ser desfeitas;
- **Furo 4 (o PID do Edge).** É um limite conhecido, não um defeito — e a
  sprint mesma diz que não é argumento para voltar ao `0x0CE6`. Falta
  documentar e, idealmente, tornar configurável por perfil;
- **Furo 5 (a taxa declarada do Edge).** **Não medido**, e a verificação
  precisa da SDL3 que a Steam distribui — medir contra a `libSDL2` do sistema
  é o erro de método que esta casa cometeu em 01/08.

## A MEDIÇÃO do defeito 2 — feita em 02/08/2026, com o hardware dela

Ela avisou: *"um controle tá no cabo e o outro tá no bt"*. Era exatamente a
condição que faltava, e a primeira entrega desta sprint era **diagnóstica**.

### O que foi medido

Com o daemon vivo, os dois controles ligados, e a leitura direta do sysfs:

| nó de LED | controle | `multi_intensity` | o que é |
|---|---|---|---|
| `input180:rgb:indicator` | `a0:fa:9c:00:00:f0` | **255 0 0** | o controle no **Bluetooth** |
| `input832:rgb:indicator` | `14:3a:9a:00:00:ab` | **0 0 255** | o controle no **cabo** |
| `input239:rgb:indicator` | `02:fe:00:00:00:01` | 0 0 0 | o gamepad **virtual** P1 |
| `input836:rgb:indicator` | `02:fe:00:00:00:02` | o gamepad **virtual** P2 | |

E o journal, no mesmo minuto:

```
sysfs_led_cobertura  cobertos=['a0:fa:9c:00:00:f0']  sem_no_sysfs=[]
sysfs_led_cobertura  cobertos=['14:3a:9a:00:00:ab', 'a0:fa:9c:00:00:f0']  sem_no_sysfs=[]
```

### O veredito: **o defeito 2 NÃO se reproduz, e a premissa dele caducou**

> **CADUCOU NA MESMA TARDE — 02/08/2026.** O defeito 2 **SE REPRODUZ**. O
> sintoma novo é pior que o descrito aqui: o nó sysfs **existe**, tem o valor
> certo, o valor **persiste**, e a barra fica apagada. Nem mudar a cor cura — o
> que **refuta** a previsão do comentário `LIGHTBAR-BT-RESET-03` (*"apagada até
> a cor MUDAR"*). Ver a sprint própria: `2026-08-02-LIGHTBAR-BT-CLAIM-01`.
>
> **A primeira hipótese desta nota — "a condição que faltava eram os DOIS
> DualSense no BT" — está REFUTADA, e o registro fica.** A linha do tempo do
> journal mostra que o primeiro controle a apagar foi o `a0:fa:9c:00:00:f0` às
> 14:13, **quando ele era o ÚNICO da máquina**. "Dois por BT" era coincidência
> do instante em que se olhou.
>
> **O gatilho real é o REINÍCIO DO DAEMON**, e ele foi provocado pela própria
> investigação: cada reinício fabrica handle NOVO para controle VELHO, dispara
> o `0x08` (Reset LED state) num controle adotado horas antes, solta a lightbar
> que o kernel tomara no probe — e **nada do lado do host volta a tomá-la**,
> porque quem toma é o `lightbar_setup` (`valid_flag2` bit1), que o kernel manda
> uma vez por conexão e que nós nunca mandamos.
>
> Lição de método, e é a terceira do dia: **o instrumento apagou a luz que
> tinha ido medir.** Quatro reinícios do daemon foram feitos para instrumentar
> o áudio e ler o DEBUG da própria lightbar.
>
> A previsão da seção "o que a medição deixa em aberto", logo abaixo, estava
> **certa** no essencial — ela dizia *"se for isso, o defeito é de CORRIDA e
> vai voltar"*. Voltou; só que a corrida é com o ciclo de vida do HANDLE, não
> com o do nó sysfs.

A sprint foi escrita sobre esta linha de log, de 01/08:

```
sysfs_led_cobertura  cobertos=[]  sem_no_sysfs=['a0:fa:9c:00:00:f0']
```

e concluía, com razão para aquele momento: *"no Bluetooth o LED não tem nó em
sysfs"*.

**Hoje ele tem** (`input180:rgb:indicator`), o `sem_no_sysfs` sai vazio, e a
lightbar do controle no Bluetooth está **ACESA em vermelho** — o que bate com
o print que ela mandou no mesmo dia, onde o card do Controle 2 (BT) mostra
`#ff0000`.

**Isto NÃO é uma cura**: nada foi mudado no caminho da lightbar por BT nesta
leva, e as quatro curas de 17-22/07 seguem intactas. É uma medição que diz que
o sintoma não está presente nesta configuração.

### O que a medição deixa em aberto, e é a próxima pergunta

O nó do BT **existe agora e não existia em 01/08**. As duas explicações
possíveis levam a lugares diferentes, e nenhuma delas foi medida:

1. **o nó demora a aparecer** depois do pareamento/conexão, e a captura de
   01/08 pegou a janela em que ele ainda não existia. Se for isso, o defeito é
   de CORRIDA e vai voltar — e a cura é o daemon reobservar o sysfs quando o
   `sem_no_sysfs` não estiver vazio, em vez de decidir uma vez;
2. **alguma coisa entre 01/08 e 02/08 mudou o caminho** (uma reconexão, um
   ciclo do BlueZ, o próprio reinício do daemon).

**Para fechar:** da próxima vez que ela vir a lightbar apagada no BT, a
pergunta é uma só — `ls /sys/class/leds/ | grep rgb` e o `sem_no_sysfs` do
journal. Se o nó não estiver lá, é a hipótese 1.

### E um achado de brinde, não previsto na sprint

**Os gamepads VIRTUAIS também têm nó de LED em sysfs** (`input239` e
`input836`, com os MACs forjados `02:fe:...`), e os dois estão em `0 0 0`.

Isso não é defeito — o vpad não tem lightbar física —, mas é uma superfície
que ninguém tinha olhado: um jogo que leia a cor do controle pelo sysfs do
device que ele abriu vai ler **preto** no vpad, e não a cor que o físico está
mostrando. Fica registrado para quem for mexer na REPLICA-03.

## A MEDIÇÃO da cura do defeito 1 — 02/08/2026, no hardware dela

Com um controle no cabo e outro no Bluetooth, a cura foi exercitada contra o
PipeWire real:

```
fonte padrão do sistema:
  alsa_input.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.iec958-stereo

placas de som com "dualsense":  1   (a do controle no CABO)
backend detectado:              wpctl
fonte_padrao_e_o_controle():    True
```

**Duas coisas ficam provadas:**

1. **a cura não quebrou o caso que sempre funcionou.** Com a fonte padrão
   sendo o controle, ela responde `True` e o botão age — que é o
   comportamento de sempre no cabo;
2. **a premissa do defeito se confirma no mesmo instante**: há UMA placa de
   som de DualSense na máquina, e é a do controle no **cabo**. O controle no
   Bluetooth não tem placa nenhuma — exatamente como a sprint mediu em 01/08.

O caso negativo (fonte padrão sendo outro aparelho, com o botão recusando)
**não foi exercitado no hardware de propósito**: provar isso exigiria trocar a
fonte padrão de áudio dela, e mexer na configuração dela para validar código é
o que esta casa já pagou caro uma vez. Ele está coberto por teste
(`test_a_fonte_padrao_de_outro_dispositivo_nao_e_confundida`), com a mordida
escrita.
