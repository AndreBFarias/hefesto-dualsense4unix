# RADIO-BOMBARDEADO-01 — quarenta mil frames corrompidos em meia hora

- **Medido em:** 03→04/08/2026, na sessão de quatro controles dela
- **Gravidade:** alta — é a queda em cascata que ela vem reportando
- **Estado:** aberta. **DUAS hipóteses refutadas por medição**; uma terceira em
  pé, e o experimento que a decide **não precisa dela**
- **Pré-requisito:** nenhum. O primeiro bloco é forense de journal.

> ### O QUE DÁ PARA FAZER HOJE, SEM ELA
>
> **Tudo do bloco F** (forense de journal). O experimento que decide a hipótese
> em pé é um A/B de dez minutos que um Claude monta sozinho — só o bloco M4
> (trocar o modo físico do 8BitDo) exige a mão dela, e ele é o **último**
> recurso, não o primeiro.
>
> Esta sprint **já custou uma versão errada**: a primeira redação mandava 50
> minutos de bancada para testar uma hipótese que o journal já tinha matado.

---

## O que está medido (e como conferir cada linha)

| janela | no CABO | no RÁDIO | frames L2CAP corrompidos |
|---|---|---|---|
| 03/08 19:35 → 20:04 | **DualSense high-speed** (`054c:0ce6`, `usb 3-3`) | DualSense BT + Pro BT | **0** |
| 03/08 23:20 → 23:49 | clone `054c:05c4` **full-speed** (`usb 3-4`) | DualSense BT + Pro BT | **0** |
| 03/08 23:51 → 23:59 | idem | idem, **+26.884 erros de CRC do clone** | **0** |
| 03/08 23:59 → 04/08 00:28 | **DualSense high-speed** (`054c:0ce6`, `usb 3-4`, desde 23:59:55) | DualSense BT + clone BT + **Pro BT** | **44.718** |

Comandos que produzem a tabela:

```bash
# frames corrompidos numa janela (a DATA COMPLETA é obrigatória — ver "o erro do relógio")
journalctl -k -b --since '2026-08-03 19:35' --until '2026-08-03 20:04' --no-pager \
  | grep -cE 'Unexpected start frame|Frame is too long'

# o que entrou no cabo, e em que velocidade
journalctl -k -b --no-pager | grep -E 'usb 3-[0-9]: (new|New USB device found)'

# os erros de CRC do clone, e QUANDO
journalctl -b -k --no-pager | grep 'DualShock4 input CRC' | head -1
journalctl -b -k --no-pager | grep 'DualShock4 input CRC' | tail -1
```

Cerca de **26 frames corrompidos por segundo** durante 28 minutos, nas duas
formas que o kernel emite:

    Bluetooth: Unexpected start frame (len 17)
    Bluetooth: Frame is too long (len 17, expected len 4)

**O adaptador não vê erro nenhum:** `hciconfig hci0` reporta `errors:0`. A
corrupção é de remontagem **L2CAP**, acima do HCI.

---

## F1 JÁ EXECUTADO (04/08) — e são DOIS fenômenos, não um

A forense de comprimentos foi feita, e ela **reparte a tempestade em dois**:

| forma | comprimento | quando | volume |
|---|---|---|---|
| `Unexpected start frame` | **len 17** | 00:18:18 → 00:27:52 | **42.763** (~4300/min, constante) |
| `Unexpected start frame` | **len 83** | 00:00:48 → 00:18:23 | **1.954** — gotejamento de 1/min, e uma rajada de 1951 no minuto 00:18 |
| `Frame is too long` | — | — | 255 (0,6% do total) |

```bash
journalctl -k -b --no-pager | grep -oE '\(len [0-9]+' | sort | uniq -c | sort -rn
journalctl -k -b --no-pager -o short-iso | grep '(len 17' | awk '{print substr($1,12,5)}' | uniq -c
```

**Duas consequências, e as duas mexem no resto do documento:**

1. **A tempestade de verdade é o `len 17`, e ela começou às 00:18:18** — não às
   00:00:48, quando o DualSense high-speed entrou no cabo. São **18 minutos** de
   intervalo entre a causa suposta e o efeito. Isso enfraquece muito a hipótese
   2 na forma simples ("plugou, corrompeu") e **reforça a hipótese 3**: o que
   importa não é o dispositivo estar lá, é alguma coisa começar a acontecer;
2. **o `len 83` é outro bicho** e merece nome próprio. Gotejamento de 1 por
   minuto durante 18 minutos não é congestionamento — é evento raro e
   repetitivo. A rajada de 1951 no minuto 00:18 é o momento em que os dois se
   cruzam, e é o único instante do boot em que isso acontece.

### A pista de 00:18, e por que NÃO é conclusão

No minuto da virada havia uma execução da suíte de testes em voo (teclados
uinput nascendo em 00:17:56 e 00:18:28). E o `input-remapper` da máquina dela
**reage a cada um deles enumerando TODOS os dispositivos de entrada** —
incluindo os controles no rádio:

    00:18:29 input-remapper-service: Request to autoload for "Hefesto - ... Virtual Keyboard"
    00:18:29 input-remapper-service: Found "Pro Controller", "DualSense ... (Hefesto P2)",
                                     "Sony Interactive Entertainment DualSense ...", ...

Dezessete teclados por execução, cada um disparando uma varredura de todos os
controles. É um mecanismo de amplificação plausível.

**MAS a hipótese não fecha, e é honesto dizer por quê:** houve execuções da
suíte às 22:29, 23:34 e 23:39, com controles no rádio, e elas produziram
**zero** frames. Suíte sozinha não basta.

**O experimento que discrimina** (dez minutos, e só precisa de um controle no
rádio): rodar a suíte com um controle no Bluetooth e o cabo VAZIO, contar; depois
com o cabo ocupado pelo DualSense high-speed, contar. Se só a segunda produzir
frames, a suíte é o gatilho e a topologia é o meio — e as duas coisas viram uma
só explicação.

Ver [SUITE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md),
que sobe de "suja o diagnóstico" para "pode estar derrubando os controles dela".

---

## Hipótese 1 — o clone DS4 bombardeia o rádio: **REFUTADA**

O `doctor.sh` aponta *"DualShock4 com 26884 erros de CRC neste boot — clone DS4
bombardeando o rádio"*, e os números têm ordem de grandeza parecida com a da
tempestade. Parecia fechado.

**Está refutada porque os dois fenômenos são DISJUNTOS no tempo:**

| | erros de CRC do clone | frames L2CAP corrompidos |
|---|---|---|
| 23:51:44 → 23:58:07 | **26.884** | **0** |
| 23:59 → 00:28 | **0** | **44.718** |

O argumento *"mesma ordem de grandeza, no mesmo boot"* é coincidência de
**boot**, não de janela. É exatamente o tipo de raciocínio que a hipótese
seguinte já tinha derrubado — e que eu repeti sem perceber.

**A linha 23:51→23:59 é, sozinha, o controle negativo do clone**: ele
despejando ~700 erros por minuto no rádio, e **zero** frames corrompidos.

---

## Hipótese 2 — a topologia USB: **a refutação anterior era INVÁLIDA**

A hipótese: o dongle Bluetooth é um **full-speed de 12 Mbit/s** atrás do mesmo
root hub (Bus 003) de um DualSense que acende **dois endpoints isócronos**
(392 e 196 bytes, `bInterval=4`) e reserva banda de microquadro. Split
transaction faminta explica corrupção de ACL com elegância.

Na primeira redação desta sprint eu a declarei morta pela janela 23:20→23:49
("cabo dentro, zero frames"). **Essa refutação não vale:** o que estava no cabo
naquela janela era o clone `054c:05c4` **full-speed, só com interface HID** —
nenhum endpoint isócrono. O objeto testado não estava no experimento.

O DualSense high-speed com os dois isócronos entrou às **23:59:55**, e o
primeiro frame corrompido é **00:00:48** — 50 segundos depois. É a única
hipótese cujo início casa com o relógio.

**Mas ela também não se sustenta como está**, porque existe uma janela de
controle **válida** que a contradiz: 19:35→20:04, com o mesmo DualSense
high-speed no cabo, no mesmo Bus 003, com controles no rádio — e **zero**
frames.

---

## Hipótese 3 (EM PÉ) — não é enumerar, é **streamar**

O que reconcilia a janela de controle válida com a da tempestade: **banda
isócrona só é reservada quando o alt-setting de áudio está ATIVO.** Um
DualSense enumerado no cabo com o áudio parado não tira microquadro de ninguém;
o mesmo DualSense com captura ou reprodução aberta, sim.

**O indício medido, e o que ele NÃO prova:**

| janela | escritas de áudio do daemon |
|---|---|
| 19:35 → 20:04 (0 frames) | **0** |
| 23:59 → 00:28 (44.718 frames) | **24** (`speaker_volume_set` + `mic_hotkey_toggle`) |

```bash
journalctl --user -u hefesto-dualsense4unix --since '2026-08-03 23:59' \
  --until '2026-08-04 00:28' --no-pager | grep -c 'speaker_volume\|audio_'
```

**Isto é correlação, não prova.** `speaker_volume_set` é escrita de registrador
HID, não fluxo de áudio — serve como indício de que o bloco de áudio estava
sendo usado, e nada além. Um Claude que tratar esta tabela como conclusão
repete o erro que já custou duas hipóteses nesta sprint.

**E há um agravante que fecha o círculo com o resto da leva:** o drop-in
`51-hefesto-dualsense-no-default-source.conf` esteve **ausente a noite inteira**
(criado só às 00:37:38 de 04/08). Sem ele o DualSense era a **fonte E o destino
padrão do sistema** — ou seja, o PipeWire tinha motivo permanente para manter os
fluxos isócronos abertos. Ver
[DROPIN-AMBIGUO-01](2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md).

---

## O experimento que decide — bloco F, **sem ela**

**F1. A forense que falta.** A distribuição dos comprimentos dos frames
corrompidos (`len 17` domina? há outros?) e a correlação minuto a minuto com
qualquer atividade de áudio no journal. Barato, e pode sozinho matar ou
confirmar a hipótese 3.

**F2. O A/B do áudio ativo** — dez minutos, um DualSense no cabo e um no rádio,
tudo pilotável por linha de comando:

| fase | o que fazer | duração |
|---|---|---|
| repouso | DualSense no cabo, **nenhum** fluxo de áudio aberto | 5 min |
| carga | `parec` contínuo na captura do controle **e** `pw-play` em laço no sink dele | 5 min |

Contar os frames de cada fase com o comando da tabela acima. **Se a fase de
carga produzir frames e a de repouso não, a hipótese 3 está confirmada** — e a
cura é de produto, não de hardware.

**F3. O controle negativo da topologia.** Repetir F2 com o dongle Bluetooth
numa porta de **outro** barramento (Bus 001, 002 ou 004 — todos livres de
isócrono; `lsusb -t` confirma). Se a carga deixar de produzir frames, a
topologia é o mecanismo e a cura é o `doctor.sh` **detectar e dizer**.

> **F3 exige alguém mexer no cabo do dongle** — é o único ponto desta sprint
> que precisa de mão humana, e vem **depois** de F1 e F2 terem decidido que
> vale a pena.

**M4 (opcional, e só se F1-F3 não decidirem).** O 8BitDo em modo Switch, para
separar "clone" de "Nintendo-class". Custa o pareamento e a casa já mediu que
o modo Switch por Bluetooth é instável. **Não comece por aqui.**

---

## O que NÃO é hipótese: o fim da tempestade

O último frame é `04/08 00:27:52 Unexpected start frame (len 12)` — **o mesmo
segundo** em que o `bluetoothd` fez core dump (`malloc_consolidate(): unaligned
fastbin chunk detected`). O crash derrubou todos os links L2CAP de uma vez.

A primeira redação desta sprint dizia *"a tempestade parou junto com o último
controle que saiu do rádio"*. **Não parou** — foi interrompida pelo crash, e o
`coop_player_removed` só aparece às 00:27:54, **depois**. O zero posterior
também não decide nada: os controles estavam desligados
(`control_connect_cb ... Host is down (112)`).

---

## A cura, conforme o que F1-F3 disserem

**Se for o áudio ativo (hipótese 3):** a cura é de produto e já tem meio
caminho andado — o drop-in 51 armado impede o DualSense de virar fonte padrão,
e o medidor de microfone só abre captura com a aba Status visível. Falta o
produto **saber** que essa combinação é cara e **dizer** enquanto ela joga.

**Se for a topologia (hipótese 2):** o `doctor.sh` passa a ler `lsusb -t`,
reconhecer o dongle full-speed dividindo root hub com isócrono, e **nomear a
porta** para onde mudar.

**Nos dois casos, e independente:** o `bluetoothd` 5.86 caiu duas vezes em meia
hora. Isso é bug upstream, e a casa já encurtou o prejuízo — ver
[BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md).
O que **não** está resolvido é o produto **contar** para ela o que aconteceu:
hoje ela vê os quatro controles caírem e o Bluetooth pedir senha, sem uma
palavra.

---

## O erro do relógio, que já custou uma medição

`journalctl --since "23:20"` **sem data** é lido pelo systemd como *"23:20 de
hoje"* — que às 00:30 é **futuro**, e devolve zero. Deu zero em TODAS as
janelas, e zero em todas era o sinal de instrumento quebrado, não de ausência
de defeito. **Use sempre a data completa.**

---

## Aceite

1. F1 e F2 executados e escritos **neste documento**, com as contagens;
2. um mecanismo nomeado, ou a declaração honesta de que F1-F2 não decidiram —
   e o que se mede a seguir;
3. se a hipótese 3 vencer: a tela avisa **durante** a sessão, não no
   diagnóstico;
4. quando o `bluetoothd` cair, a janela dela diz que caiu e que voltou;
5. teste que morde: para a cura que for, arrancar a detecção faz reprovar um
   caso construído a partir dos números desta sprint.

---

## Relacionado

- [BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md)
- [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md)
- [DROPIN-AMBIGUO-01](2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md)
- [BT-FURO-FINO-01](2026-08-03-BT-FURO-FINO-01-os-sete-caminhos-que-so-degradam-no-radio.md)
- [QUATRO-NO-RADIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md)
