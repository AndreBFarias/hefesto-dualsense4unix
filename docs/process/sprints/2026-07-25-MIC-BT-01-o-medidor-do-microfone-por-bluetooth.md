# MIC-BT-01 — O medidor de microfone só funciona no cabo, e o alvo é Bluetooth

**Status:** ABERTA
**Prioridade:** alta — o alvo declarado do projeto é **quatro controles por
Bluetooth**, e nesse cenário o medidor **nunca** aparece. São dois motivos
empilhados: a ponte de áudio nasce desligada (opt-in, e por bons motivos), e
**mesmo ligada** a GUI recusa atribuir a source ao controle. O segundo motivo é
o que a seção "Correção do diagnóstico" mede.

## O achado (medido em 2026-07-25, com os 4 controles por BT)

A área do microfone **existe** na aba Status: `MicMeter` de 14 barras com cor
por amplitude, selo ATIVO/MUDO, montada em `controller_card.py:712`
(`_montar_mic_e_touchpad`, empacotada na linha de sensores em
`controller_card.py:693`). Ela é dado real — `MicMonitor` captura por `parec` e
calcula RMS.

Mas ela se esconde quando não há microfone, e por Bluetooth — com a ponte
desligada, que é o padrão — **não há**:

```
pactl list sources short | grep -i dualsense   ->  (vazio)
pactl list cards   short | grep -i dualsense   ->  (vazio)
```

Por Bluetooth o DualSense **não expõe placa de áudio USB**. Ele não implementa
A2DP/HFP/HSP — o SDP traz só HID (`1124`) e PnP (`1200`), e isso está correto
(confirmado pelo mantenedor do BlueZ). O áudio dele trafega como **Opus
tunelado em reports HID** (`0x31`/`0x32`).

Consequência: `MicMonitor`, que trabalha em cima do PipeWire (`pactl`/`parec`),
não tem o que ver **enquanto a ponte estiver desligada**. O medidor funciona
**no cabo** e some no Bluetooth — que é justamente onde a mantenedora vai usar.

Ligar a ponte não basta, e é aí que o diagnóstico original errou: a source
passa a existir, o filtro da GUI a reconhece, e ela mesmo assim não chega ao
card. A seção seguinte mostra onde ela para.

## O que já existe e não está ligado

- `integrations/dualsense_bt_audio.py` — **1286 linhas**, a ponte Opus completa,
  validada ao vivo gravando WAV. Publica uma source virtual no PipeWire
  (`module-pipe-source`).
- `daemon/subsystems/bt_mic.py` — `BtMicSubsystem`, **agora registrado** no
  lifecycle (entregue em 2026-07-25), atrás do gate
  `HEFESTO_DUALSENSE4UNIX_BT_MIC=1`.
- `cli/cmd_mic.py` — `mic bt` e `mic bt-status`.

Ou seja: a ponte existe, o subsystem sobe, e a GUI não liga uma coisa na outra.

## Correção do diagnóstico (25/07, medido lendo e executando o código)

A primeira versão desta sprint dizia que **o filtro da GUI não reconheceria o
nome da source publicada pela ponte**. Isso está **errado**, e o registro fica à
vista em vez de sumir: o filtro reconhece, sim. Quem recusa é a **atribuição**,
um passo depois — e apontar o filtro teria feito a gente consertar a peça que
não estava quebrada.

**O que a ponte publica.** O nome da source é
`hefesto_dualsense_bt_<6 hex>` (`dualsense_bt_audio.py:824`), montado a partir
de `NoDualSenseBT.nome_curto` (`dualsense_bt_audio.py:330`), que devolve os
**seis últimos** dígitos hex do MAC (`:338-340`) ou, quando o controle não tem
`HID_UNIQ`, o nome do nó de hidraw (`:341`). Esse nome vai literal para o
`source_name=` do `module-pipe-source` (`dualsense_bt_audio.py:614`), então é
exatamente o que aparece em `pactl list sources short`.

**O filtro casa esse nome.** `_MARCADORES_DUALSENSE` (`mic_monitor.py:42`) tem
`"dualsense"` e `fontes_dualsense()` compara por substring (`mic_monitor.py:99`)
— `hefesto_dualsense_bt_c311f0` contém `dualsense`. Rodando as duas peças de
verdade, com quatro pontes de MACs `aa:bb:cc:c3:11:f0` a `…f3`:

```
fontes_dualsense(...) -> ['hefesto_dualsense_bt_c311f0',
                          'hefesto_dualsense_bt_c311f1',
                          'hefesto_dualsense_bt_c311f2',
                          'hefesto_dualsense_bt_c311f3']
```

As quatro **entram** na lista. O filtro não precisa aprender nada.

**Quem recusa é `escolher_fonte()`** (`mic_monitor.py:104`). Ela liga uma source
a um controle por duas regras, e nenhuma vale no cenário-alvo:

1. **O nome carrega o MAC** (`mic_monitor.py:127-129`) — exige
   `fonte.lower().startswith("bluez")`. O nome da ponte começa com `hefesto`.
2. **Um para um** (`mic_monitor.py:130`) — exige exatamente **uma** source e
   **um** controle candidato. `reconciliar()` passa `list(controles)`
   (`mic_monitor.py:315`), e `controles` é a lista de **todos** os controles
   conectados com `uniq` (`status_actions.py:322-328`). Com quatro na mesa, a
   regra 2 nunca dispara.

```
escolher_fonte(4 sources, aabbccc311f0, [4 uniqs]) -> None   (idem f1, f2, f3)
escolher_fonte(1 source,  aabbccc311f0, [1 uniq])  -> hefesto_dualsense_bt_c311f0
```

A segunda linha é o refinamento que a medição trouxe e que a versão anterior
desta sprint não tinha: **com um controle só, o medidor já funcionaria hoje**
pela regra do um para um. O defeito não é do transporte Bluetooth — é da
**contagem**. Ele aparece a partir de dois controles na aba Status, mesmo que só
um deles tenha ponte de pé. Com quatro, que é o alvo declarado, é garantido.

E o sumiço é **decisão deliberada do código**, não esquecimento: a docstring de
`escolher_fonte` (`mic_monitor.py:120-123`) diz que exibir o mic do controle
errado é pior que não exibir nenhum. A regra está certa; o que falta é ela saber
ler o nome que a nossa própria ponte escreve.

**Os 12 contra os 6.** `_so_hex()` (`mic_monitor.py:135`) devolve os **doze**
dígitos hex do MAC do controle, e o nome da ponte carrega só os **seis**
últimos. Então nem afrouxar a regra 1 para aceitar o prefixo `hefesto` resolveria:

```
_so_hex('aabbccc311f0')                = aabbccc311f0
_so_hex('hefesto_dualsense_bt_c311f0') = efedaeebc311f0
alvo in _so_hex(fonte)                 -> False
```

**A armadilha que isso descobre.** `_so_hex('hefesto_dualsense_bt_')` vale
`efedaeeb` — oito dígitos hex de lixo que o **próprio prefixo** produz. Uma
comparação ingênua ("os 6 hex do controle aparecem no hex da fonte") casaria por
acaso com um controle cujo MAC terminasse em `efedae`, `fedaee` ou `edaeeb`. É a
mesmíssima armadilha que a docstring já descreve para nomes ALSA, onde
"Interactive" vira `eac` (`mic_monitor.py:113-116`). A regra nova tem que casar
o **nome literal**, não hex solto.

**O que NÃO foi medido.** Nada disso é medição ao vivo: são as funções do
produto executadas com MAC e sysfs dublados. O comportamento com quatro pontes
de pé no PipeWire de verdade, e o custo delas no rádio com quatro controles,
continua sem medição.

## Entregas

- [ ] **`escolher_fonte()` aprende o nome que a nossa ponte escreve.** Regra
      nova, antes do um para um: source cujo nome seja o prefixo
      `hefesto_dualsense_bt_` seguido de **exatamente seis dígitos hex** casa
      com o controle cujos seis últimos hex do `uniq` sejam esses. Casamento
      pelo nome literal — nunca por `_so_hex()` da fonte inteira, pelo motivo
      do parágrafo acima. `fontes_dualsense()` fica como está: ela já
      reconhece, mexer nela seria consertar o que não está quebrado.
      A recusa honesta continua valendo em dois casos: source cujo sufixo não
      é hex (controle sem `HID_UNIQ`, que vira `hefesto_dualsense_bt_hidraw9` —
      medido) e dois controles que terminem nos mesmos seis hex. Neste segundo
      caso a ambiguidade nasce na própria ponte, que publicaria o mesmo nome
      para os dois (`dualsense_bt_audio.py:332-337` já avisa disso) — a GUI
      devolve `None` em vez de escolher.
      Cuidado com o teste: ele tem que morder. Exercitar `reconciliar()` com
      quatro controles, e não só chamar `escolher_fonte()` — arrancada a regra
      nova, o teste precisa reprovar.
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
