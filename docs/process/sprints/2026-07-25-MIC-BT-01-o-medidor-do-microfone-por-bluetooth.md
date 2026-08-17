# MIC-BT-01 — O medidor de microfone só funciona no cabo, e o alvo é Bluetooth

> **Nota de 16/08/2026 — o interruptor da interface caducou, e voltou a ser
> caixa aberta.** A caixa 2 desta sprint ("ligar e desligar a ponte pela
> interface") foi paga em 07/08 com o interruptor **"Pelo rádio"** no card do
> controle, e foi **desfeita hoje**. Dois motivos:
>
> 1. **desenho dela**, olhando a aba Status: *"esse botão de silenciar some. dá
>    espaço a um slicer de microfone pra definir o volume do microfone real
>    (independente de saber se tá via bt ou via cabo), o app deve ser
>    inteligente pra saber qual caminho usar"*. Escolher o transporte é decisão
>    do aplicativo, não dela;
> 2. **a ponte não é segura** — medido duas vezes em 16/08. Com ela de pé, o
>    botão PS dispara em pulsos de ~17 ms e o daemon abre a Steam em laço; ela
>    desligou o controle com medo. Log e análise em
>    [O PS preso](../estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md).
>
> **A ponte NÃO foi removida** — módulo, subsystem, `mic bt` e o gate
> `HEFESTO_DUALSENSE4UNIX_BT_MIC` continuam de pé, e ela publicou o source no
> PipeWire em 16/08. O que saiu foi o BOTÃO. A caixa 2 só reabre depois de
> arbitrada a posse do `/dev/hidraw` entre a ponte e o `motion_reader`, e o
> contador de sequência do report `0x32` ter um dono só. Portões que seguram
> isso: `tests/unit/test_o_interruptor_do_mic_no_card.py` e
> `tests/unit/test_o_interruptor_do_mic_por_bluetooth.py`.

**Status:** ABERTA
**Prioridade:** alta — o alvo declarado do projeto é **quatro controles por
Bluetooth**, e nesse cenário o medidor **nunca** aparece.

## O achado (medido em 2026-07-25, com os 4 controles por BT)

A área do microfone **existe** na aba Status: `MicMeter` de 14 barras com cor
por amplitude, selo ATIVO/MUDO, montada em `controller_card.py:681`
(`_montar_mic_e_touchpad`). Ela é dado real — `MicMonitor` captura por `parec` e
calcula RMS.

Mas ela se esconde quando não há microfone, e por Bluetooth **nunca há**:

```
pactl list sources short | grep -i dualsense   ->  (vazio)
pactl list cards   short | grep -i dualsense   ->  (vazio)
```

Por Bluetooth o DualSense **não expõe placa de áudio USB**. Ele não implementa
A2DP/HFP/HSP — o SDP traz só HID (`1124`) e PnP (`1200`), e isso está correto
(confirmado pelo mantenedor do BlueZ). O áudio dele trafega como **Opus
tunelado em reports HID** (`0x31`/`0x32`).

Consequência: `MicMonitor`, que trabalha em cima do PipeWire (`pactl`/`parec`),
não tem o que ver. O medidor funciona **no cabo** e some no Bluetooth — que é
justamente onde a mantenedora vai usar.

## O que já existe e não está ligado

- `integrations/dualsense_bt_audio.py` — **1286 linhas**, a ponte Opus completa,
  validada ao vivo gravando WAV. Publica uma source virtual no PipeWire
  (`module-pipe-source`).
- `daemon/subsystems/bt_mic.py` — `BtMicSubsystem`, **agora registrado** no
  lifecycle (entregue em 2026-07-25), atrás do gate
  `HEFESTO_DUALSENSE4UNIX_BT_MIC=1`.
- `cli/cmd_mic.py` — `mic bt` e `mic bt-status`.

Ou seja: a ponte existe, o subsystem sobe, e a GUI não sabe de nada disso.

## Entregas

- [ ] **A GUI descobre a source virtual da ponte.** Hoje `mic_monitor.py:82`
      filtra sources cujo nome casa `wireless_controller`/`dualsense`; a source
      publicada pela ponte precisa ser reconhecida pelo mesmo caminho (ou o
      filtro precisa aprender o nome dela).
- [ ] **Ligar/desligar a ponte pela interface**, não só por CLI. Onde: avaliar
      se no card do controle (perto do medidor) ou na aba Emulação, junto do
      controle de mic que já existe.
- [ ] **Dizer a verdade quando está desligada.** Hoje o módulo simplesmente
      some, e "sumiu" é indistinguível de "não existe". Com a ponte disponível
      mas desligada, o certo é mostrar o estado e o caminho — não esconder.
- [ ] **Custo à vista.** A ponte consome ~35% dos reports de entrada e o
      firmware emudece 55-75% do tempo (causa em aberto). Isso precisa estar
      visível na hora de ligar, não escondido na documentação.

## Cuidado

O gate opt-in existe por uma razão: a ponte disputa o contador de sequência do
report `0x32` com o driver. Ligá-la por padrão sem medir essa disputa com quatro
controles é o tipo de coisa que derruba tudo em partida. Manter opt-in até haver
medição com os 4 conectados.

## Critério de conclusão

Com quatro controles por Bluetooth, a mantenedora vê o nível do microfone de
quem está falando — ou entende, olhando a tela, por que não vê.
