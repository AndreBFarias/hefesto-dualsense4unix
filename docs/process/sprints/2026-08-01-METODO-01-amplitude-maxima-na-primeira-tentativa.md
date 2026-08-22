# METODO-01 — amplitude máxima na primeira tentativa

**Estado:** CONCLUIDA — registro de método, sem código: a curva medida virou `SP_PREAMP_GAIN_MASK`/`SP_PREAMP_GAIN_PADRAO` em `core/ds_output_report.py:183-184`, e a lição está no CLAUDE.md (verificado em 21/08/2026)

Data: 2026-08-01. Escopo: método de medição, não código. Nada aqui altera a
SOM-02; o que ele registra é COMO quase se publicou um diagnóstico errado sobre
ela, e a medição instrumental que reabilitou a entrega.

## A lição, em uma frase

Experimento cujo instrumento é a percepção humana precisa nascer com a
**amplitude máxima**: 15 % contra 100 % quase reprovou uma entrega correta;
0 contra 255 a reabilitou em trinta segundos.

## O que aconteceu

O registrador de volume de alto-falante do DualSense (o byte `common[5]` do
report de saída, autorizado pelo bit `0x20` do `valid_flag0` — ver
`core/ds_output_report.py`) foi testado de ouvido, com o sink do PipeWire
travado em 80 %, variando o registrador entre **15 %** e **100 %**. Os três
sons soaram iguais. A conclusão tirada dali foi que a camada 2 da SOM-02 era
INERTE e que o controle deslizante da janela era decorativo.

Refeito o mesmo experimento entre **0** e **255**, a diferença foi inequívoca
ao ouvido, confirmada duas vezes e com a tela desligada (para excluir o HDMI
como fonte). O registrador funciona.

O erro não estava no ouvido dela nem no código: estava na **resolução do
experimento**. Alto-falante pequeno, curva de resposta comprimida e um
instrumento (o ouvido) sem escala absoluta — nessas condições, dois pontos
próximos no meio da curva não distinguem "não faz nada" de "faz pouco".

## A medição instrumental que fecha a conta

Para não depender do ouvido, o **microfone do próprio DualSense** foi usado
como instrumento: ele fica a poucos centímetros do alto-falante do controle e
o escuta sem nenhuma cadeia de software no meio.

Montagem (tudo em espaço temporário, nada entrou na árvore):

```
# grava o microfone do controle enquanto toca um tom de 1 kHz no alto-falante dele
parec --device=alsa_input.usb-Sony_..._DualSense_..._Controller-00.iec958-stereo \
      --format=s16le --rate=48000 --channels=2 > cap.raw &
paplay --device=alsa_output.usb-Sony_..._DualSense_..._Controller-00.analog-surround-40 tom.wav
```

A análise é um Goertzel no bin de 1 kHz (rejeita o ruído ambiente) comparando a
janela ANTES do tom com a janela DURANTE o tom, na MESMA gravação — assim
qualquer deriva de ganho do microfone se cancela.

Nenhum cancelamento de eco do firmware atrapalhou: o microfone ouve o
alto-falante com folga (magnitude de 1 kHz sobe de ~1 para ~8600).

### Curva medida do registrador (rodada limpa, sem escritor concorrente)

Sink do PipeWire fixo em 80 %, mixer ALSA do controle fixo em 95 %, só o
registrador HID variando:

| registrador (0-255) | fatia do controle deslizante | magnitude de 1 kHz |
|---|---|---|
| 0 | 0 % | 3,9 (silêncio) |
| 13 | 5 % | 5,3 (silêncio) |
| 26 | 10 % | 3,1 (silêncio) |
| 38 | 15 % | 6,2 (silêncio) |
| 51 | 20 % | 35 |
| 64 | 25 % | 172 |
| 76 | 30 % | 687 |
| 102 | 40 % | 8759 (saturado) |
| 128 | 50 % | 8488 (saturado) |
| 255 | 100 % | 8793 (saturado) |

Repetido em ordem alternada (5 %, 100 %, 5 %, 100 %) numa rodada auditada linha
a linha contra o log do daemon: 4,8 / 8611 / 4,6 / 8568. O registrador é
determinístico e repetível.

**O que a curva diz:** toda a faixa útil do registrador vive entre ~45 e ~102 de
255. Abaixo disso o alto-falante fica MUDO; acima, satura. Ou seja, no controle
deslizante de 0 a 100 % da janela, **a faixa audível inteira cabe entre 18 % e
40 %** — os primeiros 18 % são uma zona de mudo e os últimos 60 % não mudam
nada. Isso bate com a documentação de comunidade do report 0x02, que anota o
alto-falante como usando na prática a faixa 0x3D-0x64 (61-100) dos 255
possíveis.

Isso também explica por que 15 % contra 100 % pareceu nulo de ouvido em um
teste e por que 0 contra 255 foi óbvio: os dois primeiros pontos caem em
regiões PLANAS opostas da curva, e a transição inteira acontece entre eles.

## O caminho do áudio, para o registro

Por USB o DualSense é uma placa USB Audio Class independente do HID, e ela tem
mixer PRÓPRIO — o que faz do registrador HID o segundo de dois atenuadores em
série, não o único:

- `PCM Playback Volume` / `PCM Playback Switch` (card `Controller`, faixa 0-100,
  -100 dB a 0 dB) — é o volume da interface de áudio USB, o mesmo que o
  PipeWire manipula ao mexer no sink;
- `Headset Capture Volume` / `Headset Capture Switch` — o lado do microfone;
- saída com 4 canais (`FL FR RL RR`) a 48 kHz; o tom sai audível pelo
  alto-falante tanto pelo par frontal quanto pelo traseiro;
- entrada com 2 canais a 48 kHz.

Consequência de desenho: por USB existem TRÊS atenuadores em série (sink do
PipeWire, mixer ALSA da placa, registrador HID). Por Bluetooth não há placa de
áudio nenhuma — não foi medido nesta sessão se o registrador HID atua sozinho
lá, e este documento NÃO afirma que atua.

O byte de roteamento `common[7]` continuou fora de qualquer escrita, como o
código já decidia: não foi tocado, não foi testado, e a medição acima mostra
que o volume do alto-falante responde SEM ele. Não há motivo conhecido para
mexer nele.

## A armadilha nova: dois experimentadores no mesmo registrador

Durante a sessão, duas medições rodaram em paralelo sobre o MESMO controle. O
log do daemon mostra escritas de `volume=0` e `volume=255` intercaladas às
minhas, com 0,3 s de distância — uma delas caiu exatamente dentro de uma janela
de gravação e produziu um "silêncio" espúrio que, lido sem o log, teria virado
um segundo diagnóstico falso.

Regra que fica: **toda medição de registrador compartilhado tem de ser auditada
contra o log do daemon depois do fato**, conferindo linha a linha que só as
escritas do experimento aconteceram na janela. O que salva a medição não é a
gravação: é o log.

## O experimento de trinta segundos

Para confirmar de ouvido, sem instrumento nenhum, com o sink do PipeWire fixo:

```
python -m hefesto_dualsense4unix.cli.app speaker volume 0
paplay --device=alsa_output.usb-Sony_..._DualSense_..._Controller-00.analog-surround-40 \
       /usr/share/sounds/freedesktop/stereo/complete.oga
python -m hefesto_dualsense4unix.cli.app speaker volume 100
paplay --device=alsa_output.usb-Sony_..._DualSense_..._Controller-00.analog-surround-40 \
       /usr/share/sounds/freedesktop/stereo/complete.oga
```

Extremos, nunca meios. Se o do meio não for obviamente mais alto, o defeito é
real; se for, o registrador está vivo.
