# JOGO-01 — o jogo enxerga quatro controles onde existe um

- **Status:** ENTREGUE em 25/07/2026 pelo commit `a343ff6`
- **Prioridade:** MÁXIMA — impede jogar, que é o propósito do projeto
- **Aberta em:** 25/07/2026, a partir de relato com o jogo em execução

## O relato

> "no cabo, na hora de jogar ele fica como player 1, mas ao abrir o jogo em si
> ele automaticamente muda a cor e vai pro player 2 e não funciona."

Cada pedaço da frase corresponde a um fato medido, e o conjunto tem uma causa só.

## A medição

Com o Mullet Mad Jack (`steam_app_2111190`) em execução e **um** DualSense no
cabo, o sistema apresentava **quatro** dispositivos de joystick:

```
/dev/input/js0  →  Hefesto Virtual DualSense P1        (nosso gamepad virtual)
/dev/input/js2  →  DualSense Wireless Controller       (o controle físico dela)
/dev/input/js4  →  Microsoft X-Box 360 pad 0           (Steam Input)
/dev/input/js5  →  Microsoft X-Box 360 pad 1           (Steam Input)
```

O ambiente entregue ao jogo explica por quê:

```
# ~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_2111190.env
# estado: allowlist Steam Input (sem dedup) | ...
__GL_SHADER_DISK_CACHE=1
__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1
SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0
```

Compare com o de qualquer outro jogo (`steam_app_1599660`, Sackboy):

```
PROTON_DISABLE_HIDRAW=0x054C/0x0CE6          ← ausente no 2111190
SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6   ← ausente no 2111190
__GL_SHADER_DISK_CACHE=1
...
```

**O Mullet Mad Jack está na allowlist do Steam Input, e a allowlist desliga a
deduplicação inteira** — `daemon/launch_env.py:906`, que rotula esse ramo
literalmente como `"allowlist Steam Input (sem dedup)"`.

## A cadeia, do arquivo ao sintoma

1. `steam_input_apps.txt` lista `2111190`. A razão é legítima e está documentada
   no próprio arquivo: o suporte a DualSense desse jogo vem da API da Steam
   (`SetDualSenseTriggerEffect`), então o Steam Input **precisa** enxergar o
   controle físico.
2. Para isso, o `launch_env` deixa de emitir `SDL_GAMECONTROLLER_IGNORE_DEVICES`
   e `PROTON_DISABLE_HIDRAW`.
3. Mas o gamepad virtual **continua de pé** — o vpad não é desligado por estar
   na allowlist.
4. O jogo então enumera o virtual **e** o físico. A Steam ainda acrescenta os
   dois pads Xbox 360 dela.
5. O jogo atribui jogador 1 ao primeiro que encontra e jogador 2 ao seguinte.
   A ordem não é a nossa — é a da enumeração.
6. **"muda a cor"**: com o `hidraw` do físico exposto, a Steam/o jogo escreve a
   lightbar direto no aparelho, por cima do que o Hefesto pôs.
7. **"e não funciona"**: o input dela entra pelo caminho que o jogo tratou como
   jogador 2, enquanto o jogo espera o jogador 1 — ou o oposto. Metade dos
   comandos vai para um controle que o jogo não está lendo.

A allowlist é **tudo-ou-nada**: ou o Hefesto some inteiro do caminho, ou o jogo
não recebe os gatilhos adaptativos da Steam. Não existe meio-termo hoje, e o
meio-termo é exatamente o que essa classe de jogo precisa.

## Por que isso é pior no co-op

Com quatro jogadores, o número de dispositivos concorrentes multiplica: quatro
vpads + quatro físicos + os pads da Steam. O jogo escolhe quatro entre doze, sem
critério que possamos prever. **Enquanto JOGO-01 estiver aberta, o co-op de
quatro em jogos da allowlist é loteria.**

## O conserto

O princípio: **um controle físico deve produzir exatamente um dispositivo de
jogo**. A allowlist muda *qual* dispositivo, nunca *quantos*.

### Entrega 1 — allowlist desliga o vpad daquele jogo, não só o dedup

Quando o app está na allowlist, o caminho correto é o físico ser o único
dispositivo: o Steam Input fala com ele, e o Hefesto sai do caminho **inclusive
retirando o gamepad virtual** enquanto aquele jogo estiver em foco. Hoje o
`launch_env` só omite variáveis; precisa também sinalizar ao subsistema de
gamepad para não manter o vpad de pé para aquele app.

Ponto de implementação: `daemon/launch_env.py` (o ramo da allowlist) e
`daemon/subsystems/gamepad.py`, com o estado já disponível em `game_signal`.

### Entrega 2 — a decisão precisa aparecer na tela

Hoje a usuária não tem como saber que este jogo tem tratamento diferente. A aba
Emulação deve dizer, para o jogo em foco, qual dos dois caminhos está valendo:

> *"Mullet Mad Jack usa o Steam Input — o Hefesto está fora do caminho neste
> jogo. Gatilhos e luz vêm da Steam."*

### Entrega 3 — desfazer pela interface

`add_appid_to_steam_input_allowlist` (`integrations/steam_launch_options.py:765`)
só acrescenta. Tirar um jogo da allowlist exige editar `steam_input_apps.txt` na
mão. O botão que põe precisa do gêmeo que tira.

### Entrega 4 — os pads da Steam

Os dois `Microsoft X-Box 360 pad` são criados pelo Steam Input. Investigar se são
resíduo de configuração antiga (a memória do projeto registra "pad Steam órfão"
como fantasma já visto) ou consequência normal do Steam Input ativo neste app. Se
forem órfãos, o `doctor` deve detectá-los e oferecer limpeza.

## Como validar

Com o jogo aberto e **um** controle no cabo:

```bash
for j in /dev/input/js*; do
  echo "$j -> $(udevadm info -a -n $j 2>/dev/null | grep -m1 'ATTRS{name}')"
done
```

**Critério de aceite:** exatamente **um** dispositivo de jogo por controle
físico. Com quatro controles em co-op, exatamente quatro.

E o teste que realmente importa é o dela: abrir o jogo e o controle funcionar,
com a cor que o Hefesto pôs, no jogador certo.

## Nota de método

Este defeito estava documentado como *funcionalidade* desde 22/07
(`STEAM-INPUT-ALLOWLIST-01`) e o rótulo `"sem dedup"` no código descreve
exatamente o que ele faz. O que faltou foi perceber que "sem dedup" e "com vpad
ligado" juntos produzem duplicata — cada metade estava correta isoladamente.
