# O rádio meio mudo — o que atravessa e o que não

**16/08/2026, bancada com ela, ~5 horas de medição ao vivo.** Este documento
registra o que foi MEDIDO com o aparelho na mão dela, e o que cada medição
derrubou. Vários dos meus palpites caíram no caminho; estão aqui também, porque
saber o que já foi eliminado vale tanto quanto saber a causa.

---

## O sintoma dela, textual

> *"duskfade reconheceu 3 input e parou de reconhecer"*
> *"o dontscream foi igual ao pragmata: recebeu um pouco de input e morreu"*

E a correção dela, que reorientou tudo:

> *"a falha não pode ser o jogo. (…) o dont scream e o pragmata funcionavam no
> rádio, o duskfade que nunca funcionou no cabo e no radio teve input que
> funcionou."*

---

## DEFEITO 1 — o daemon não se recupera da reconexão BT

**É o que quebrava o input, e está reproduzido de ponta a ponta.**

Quando o controle cai e volta no rádio — ou sai do cabo para o rádio — o daemon
registra a perda e **nunca reabre os leitores**:

```
19:15:29  evdev_read_lost            errno 19 (dispositivo inexistente)  event25
19:15:30  motion_reader_open_failed  errno 2   /dev/hidraw5
19:15:30  controller_disconnected    reason=probe_offline
          … e depois disso, NADA.
```

O controle reconecta, o link BT fica **autenticado e criptografado**, o daemon
diz `connected=True` — e os eixos ficam **congelados no último valor lido**.

**A mentira é o detalhe caro.** O vpad continua emitindo:

| medido | valor |
|---|---|
| reports no `hidraw4` (vpad) | 396 em 8 s, ID `0x01`, 64 bytes |
| sequência (`byte[7]`) | perfeita, **zero saltos** |
| eixos nesses reports | **LX travado em 128** |

Para o jogo isso é um controle **vivo que nunca se mexe**. Ele enumera, mostra
"PlayStation" nas opções, abre o `hidraw4` pelo `winedevice.exe` — e nada
acontece. Daí "3 inputs e para": os 3 chegaram antes do leitor estagnar.

O daemon **já detecta** e só emite um aviso que ninguém lê:

```
[warning] state_stale_neutral_warning
          hint='evdev_reader pode não ter conectado; HID-raw fallback estagnado'
```

**Cura hoje:** `systemctl --user restart hefesto-dualsense4unix`. Verificado: o
input volta na hora.

**Cura de produto (a fazer):** reabrir os leitores quando o controle reconecta.
Há um gancho de sobra — `evdev_read_lost` **não tem tratador nenhum**, só é
logado. E o `state_stale_neutral_warning` já sabe dizer que está estagnado: ele
devia disparar a reabertura, não um aviso.

## DEFEITO 2 — no rádio, metade do controle não atravessa

Depois de curado o defeito 1 (input voltou, jogo respondendo), ela mediu o resto
com a mão. O padrão é nítido:

| | rádio |
|---|---|
| lightbar (cor do perfil) | **funciona** |
| LED do número do jogador | **funciona** |
| gatilhos adaptativos | falha |
| vibração | falha (zero) |
| som no controle | falha |
| touchpad | falha |
| giroscópio / mira por movimento | falha (**no cabo a mira responde**) |

**A pista dela que reorientou:** *"engraçado que o touch tá funcionando fora do
jogo no modo bt mas no jogo não."* Se funciona fora do jogo, o leitor lê — a
suspeita passa para o repasse.

**E o repasse foi medido, e está ÍNTEGRO.** Duas réguas independentes, com o
controle na mão dela:

| canal | vpad (evdev) | físico (evdev) |
|---|---|---|
| gamepad | 286 ev/10 s | 0 (grab, correto) |
| giroscópio | **7 231** | 19 435 |
| touchpad | **2 807** | 3 660 |

E no report HID de 64 bytes do `hidraw4` — que é por onde o **jogo** lê, via
`winedevice.exe` — os bytes que variam são:

```
2,3 (eixos) · 7 (sequência) · 16–27 (giro/acel) · 28–32 (timestamp) · 33–36 (touchpad)
```

**O vpad entrega tudo, pelos dois caminhos.** A hipótese dos `VALID_FLAG*` e a de
"o vpad está meio mudo" **caíram as duas**.

> **Erro meu, registrado de propósito.** Num teste anterior pedi "gire o controle
> E passe o dedo" ao mesmo tempo, o touchpad saiu `0/8 bytes variam`, e eu quase
> escrevi aqui que o produto não preenchia o touchpad no report HID. Com o gesto
> ISOLADO, os bytes 33–36 variam normalmente. **Gesto composto num ensaio produz
> ausência falsa** — a régua tem de medir uma coisa por vez, como a metodologia
> da casa já manda para tudo o mais.

Um sintoma segue sem explicação e **fica aberto honestamente**: o leitor de
movimento vive num ciclo de reabertura,

```
motion_reader_silencio_reabrindo  limite_s=30.0
motion_reader_started             path=/dev/hidraw5
   … 30 s de silêncio, e repete
```

e ainda assim o giroscópio chega ao vpad. Os dois fatos não se contradizem
necessariamente (pode haver dois caminhos de leitura), mas **ninguém mediu qual
alimenta qual**. É o próximo fio.

## DEFEITO 3 — o vpad pode nascer morto, e o daemon diz que está ótimo

Medido às 13:42:42, durante o autoswitch com o jogo subindo:

```
0003:054C:0DF2.0038   driver: NENHUM   input: NENHUM   hidraw: NENHUM
```

O uhid foi criado e o `hid_playstation` **nunca o adotou**. Ao recriar (toggle da
emulação), nasceu adotado com 4 nós de input. É uma **corrida** na criação
durante o autoswitch, não um defeito permanente.

O agravante é o de sempre: o daemon reportava
`{"enabled": true, "degraded": false}` sobre um dispositivo sem driver. Existe
`wait_for_bind()` no `uhid_gamepad`, com um comentário que descreve este caso
exato — *"sem esta espera o fallback seria desonesto: 'deu certo' com o jogo sem
controle nenhum"*. **Falta descobrir por que ele não segurou aqui.**

## O que foi ELIMINADO — cada um com a medição que o derrubou

Isto é metade do valor do dia: são becos que ninguém precisa percorrer de novo.

| suspeito | como caiu |
|---|---|
| **o jogo / o Proton** | ela: os três funcionavam antes. E o controle **não respondia nem no desktop** — jogo nenhum envolvido |
| **o wrapper `hefesto-launch`** | presente e correto no ambiente do processo do jogo: `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` |
| **o vpad ser pego pelo próprio IGNORE** | o vpad é Edge `054c:0df2`; o IGNORE é `054c:0ce6`. Esconde só o físico, como projetado |
| **o jogo não enxergar o vpad** | o `winedevice.exe` tinha o `hidraw4` (vpad) aberto, e o jogo mostrava "Estilo de entrada: PlayStation" |
| **CRC do BT** | 97 no dia, ~1/min; e **zero** durante 12 s de movimento contínuo. O kernel não reclamou |
| **o grab oscilando** | `grab=held`, `regrab=0` em 7 amostras; `poll.tick` subindo ~59/s |
| **o gate de foco X11** | `x11_focus_gate_no_x_focus` é do autoswitch (troca de perfil), não do despacho de input |
| **o daemon parar de emitir** | o vpad emitia 500 eventos/8 s e 525 reports/6 s. Emitia — só que **neutros** |
| **a supressão de emulação** | `emulation_suppressed` é da emulação de desktop (mouse/teclado); `gamepad_emulation.enabled` seguia `true` |
| **o perfil não entrar** | `active_profile: Pragmata`, autoswitch pegou, `supressao=aplicado` |
| **`launch_arm_pulado_allowlist_steam_input`** | intencional: para jogo na allowlist pula-se **só** a seção `mode` |

## Os erros de instrumento do dia — e por que importam

Três vezes a régua mentiu antes do produto, e as três custaram tempo:

1. **`quem_o_jogo_abre.py` dizia "o WRAPPER rodou? NÃO"** para os dois jogos. Ele
   lia o environ do PRIMEIRO processo da árvore — o `reaper` da Steam, que roda
   *antes* do wrapper. O `/proc` do processo do jogo tinha a variável. *Um
   instrumento que acusa a própria cura de não existir manda a investigação para
   o lugar mais caro possível.* Corrigido com critério **estrutural** (o processo
   mais fundo que casa com o padrão), nunca por conteúdo.
2. **Comparei o wrapper sem desescapar o VDF** e vi "0 jogos com wrapper" onde
   havia 62.
3. **Usei `parece_infraestrutura` achando que filtrava jogos** — ela filtra
   executáveis.

Nas três, conferir o contrato antes de acusar o código foi o que evitou um
diagnóstico falso. É barato conferir e caro acusar errado.

## O par que fechou

O ensaio mais limpo do dia, e o que reorientou tudo:

- mesma sessão do jogo (não reabriu)
- mesmo vpad (`003C` dos dois lados, não recriado)
- mesmo daemon (não reiniciou)
- **única variável: cabo → rádio**

**Funciona no cabo. Para no rádio.** Uma variável, um veredito.

## A pergunta dela, e o que a medição responde

> *"isso não ajuda a entender e a explicar o problema no dontscream e no
> duskfade?"*

**Ajuda, e separa os casos** — que é o mais valioso, porque estavam sendo
tratados como um só:

- **DON'T SCREAM e Pragmata** — funcionavam no rádio e pararam. O **defeito 1**
  explica inteiro: o controle deixa de entregar input depois de uma reconexão, e
  não é sobre jogo nenhum (não respondia nem no desktop). Curado com restart, e
  o Pragmata voltou a jogar.
- **Duskfade** — **não** é o mesmo caso. Nunca funcionou em transporte nenhum, e
  em 16/08 deu os primeiros inputs da vida dele. Para ele o defeito 1 era um
  agravante, não a causa.
- **O que o touchpad revelou** não explica o input básico de nenhum dos três: o
  repasse está íntegro nos dois caminhos. Ele derrubou uma hipótese, que é
  trabalho feito.

## O que fazer a seguir, em ordem

1. **Curar o defeito 1** — reabrir os leitores na reconexão. É o que estraga a
   sessão dela, e o gancho já existe: `evdev_read_lost` **não tem tratador**, e o
   `state_stale_neutral_warning` já sabe dizer que estagnou. Hoje só avisam.
2. **Medir quem alimenta o quê no rádio** — o `motion_reader` cicla a cada 30 s
   em silêncio e o giroscópio chega ao vpad assim mesmo. Um dos dois fatos está
   mal entendido.
3. **Achar por que o `wait_for_bind` não segurou** o vpad natimorto (defeito 3).
4. **Duskfade** — caso próprio, ainda sem causa. O par com o DON'T SCREAM está
   montado e o instrumento (`quem_o_jogo_abre.py`) agora não mente mais.

## Regra que este dia acrescenta à metodologia

**Um ensaio mede UM gesto.** Pedir "gire o controle e passe o dedo no touchpad"
produziu um zero falso que quase virou acusação ao produto. A casa já exigia par
com/sem o suspeito e uma variável por vez no ESTADO; passa a exigir também no
GESTO que se pede a ela.
