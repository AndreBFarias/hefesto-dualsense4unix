# PROTOCOLO — o controle que cai sozinho

- **Escrito em:** 07/08/2026, depois de ela relatar *"o controle desconectou
  sozinho, conectei novamente"*. Relato, **não** queixa de defeito — e este
  documento não o promove a defeito.
- **Destino desta medição:** **nenhuma sprint nova de defeito**, e **nenhuma
  nota dizendo "é o hardware dormindo"**. As duas conclusões estão erradas, e a
  seção 2 mostra por quê com número.
- **O que este documento é:** o protocolo que **decide** o que sobra, com o
  controle na mão dela.
- **Formato:** o da fila de 06/08
  ([o que só fecha com o controle na mão dela](2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md))
  — **P0** tranca o cenário (com o destrancar embutido), **ANTES** é a foto
  numérica, **CONTRASTE** é o caso sem o qual nada se conclui, **PREVISÃO** é
  falsificável e derivada do código, **LEITURA** é a tabela escrita **antes** de
  medir.

---

## 1. O que já está MEDIDO, e não precisa dela

Entre 01/08 e 07/08 o daemon registrou **18** `controller_disconnected`, **todos**
com `reason=probe_offline` — não há outro motivo no journal. GRAU: MEDIDO
(contagem sobre o journal do serviço do usuário).

E os 18 **não são um fenômeno só**. São três, empilhados sob um nome só:

| quantos | o que é, de verdade | assinatura no kernel | GRAU |
|---|---|---|---|
| **8** | o **cabo USB saindo** | `USB disconnect` nos 40 s anteriores, com replug limpo 3 a 12 s depois na mesma porta | MEDIDO |
| **1** | o **`bluetoothd` morrendo** com core dump (03/08 23:58:07, `malloc_consolidate(): unaligned fastbin chunk`) | `code=dumped, status=6/ABRT` 2 s antes | MEDIDO |
| **9** | **perda de link Bluetooth com o kernel mudo** | nada: sem `USB disconnect`, sem `error -71`, sem reset de xhci, sem frame L2CAP corrompido | MEDIDO |

As **três** quedas de 05/08 são todas cabo — naquela madrugada o mesmo cabo saiu
três vezes em 37 minutos. GRAU: MEDIDO. E 05/08 tem **zero** reconexões de rádio
no kernel, o que confirma a classificação por outro caminho.

Três coisas que a contagem **não** diz, e precisam ficar escritas:

- **`primary_changed` (49) e `retarget` (20) não são motivos de desconexão.** São
  logs de reabertura do leitor de movimento (`motion_reader_reopen_requested`),
  emitidos em `core/backend_pydualsense.py` e `core/evdev_reader.py`, e nunca
  chegam a `CONTROLLER_DISCONNECTED`. GRAU: MEDIDO (só dois pontos do código
  publicam esse tópico: `daemon/connection.py:468` e `daemon/lifecycle.py:3618`).
- **`probe_offline` é o daemon PERCEBENDO, não causando.** O evento só nasce na
  borda `not is_connected and was_connected`, e `is_connected()` é apenas *"algum
  handle aberto tem `connected`"*. Na queda de 07/08 o kernel já devolvia ENODEV
  nos evdev às 14:37:11 e o daemon batizou o fato **1 segundo depois**, às
  14:37:12. ENODEV no evdev quer dizer que o **kernel removeu** o device — o
  broker escondendo daria EACCES ou ENOENT no hidraw, nunca ENODEV no evdev.
  GRAU: MEDIDO.
- **18 é PISO, não total.** Há **dois** DualSense nesta máquina e `is_connected()`
  é um `any()` sobre os handles: `probe_offline` só dispara quando o **último**
  some. Pelo kernel foram **26** (re)conexões Bluetooth de DualSense no mesmo
  período. GRAU: MEDIDO.

**Nenhum defeito do Hefesto foi medido na queda.** GRAU: MEDIDO para a ausência
de evidência; SEM PROVA para a afirmação forte de que não existe — ver a Q-2.

---

## 2. NOTA DATADA, 07/08/2026 — o sono por inatividade está REFUTADO

Registrado aqui para **ninguém gastar uma leva investigando isto de novo**.

A hipótese era: *"o controle dorme sozinho depois de alguns minutos parado"*.
Ela está **morta por medição**, por dois caminhos independentes.

**Caminho 1 — as durações de sessão não têm agrupamento nenhum.** Ancoradas no
kernel (registro do device Bluetooth até a queda do daemon):

| sessão | duração |
|---|---|
| 06/08 00:29:09 até 06/08 16:19:23 | **15h50m14s** |
| 06/08 21:06:01 até 07/08 13:30:12 | **16h24m11s** |
| 07/08 14:34:43 até 07/08 14:37:11 | 2m28s |
| 07/08 14:38:04 até 07/08 14:38:29 | 25s |

De **25 segundos a 16h24m**, sem nada perto de dez minutos. GRAU: MEDIDO. **Duas
sessões Bluetooth contínuas passaram de quinze horas** — impossível se o controle
desligasse por ficar ocioso, porque uma noite inteira é ociosa por definição.

**Caminho 2 — o host não manda ninguém dormir.** O `IdleTimeout` do perfil HID do
BlueZ está no **default 0 (desabilitado)** e **nenhum arquivo o sobrescreve**: as
duas únicas ocorrências em `/etc/bluetooth/` estão **comentadas**. GRAU: MEDIDO.
O `main.conf` efetivo tem três linhas vivas, e nenhuma é de tempo ocioso.

**E a distribuição pela hora do relógio é espalhada** — 00h:1, 02h:5, 03h:1,
13h:1, 14h:2, 16h:1, 17h:1, 19h:1, 20h:2, 21h:1, 23h:2. As cinco das 02h são a
madrugada dela, não um ciclo de hardware. GRAU: MEDIDO.

### O dado útil que esta nota **não** pode dar

Não há **nenhum** tempo ocioso medido em que este controle durma nesta máquina, e
o que existe **refuta** a existência de um dentro de 16h24m. Quem for repetir a
pergunta precisa saber disto: **medir "em quantos minutos ele dorme" é medir um
número que a evidência de 06/08 e 07/08 diz não existir** nessas condições. Se
alguém quiser medir mesmo assim, a única forma honesta é a Q-1 abaixo, porque a
carga é a variável que sobra.

**O que caduca com esta nota:** a hipótese de sono por inatividade, e só ela.
Nada mais deste projeto muda. Nenhuma decisão medida anterior é apagada — a
[RADIO-BOMBARDEADO-01](../sprints/2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)
continua valendo para o que ela mediu em 03/08; o que esta nota diz é que **ela
não alcança as nove quedas de link deste período**, porque o rádio destes dias
está limpo: **nove** frames corrompidos em ~43 horas de boot inteiro, e **zero**
na janela da queda de 07/08, contra os 44.718 em meia hora de 03/08. GRAU:
MEDIDO.

---

## 3. Por que isto não virou sprint de defeito

Quatro razões, e cada uma sozinha já bastaria:

1. **Ela relatou sem chamar de defeito.** Transformar relato em defeito sem prova
   cria trabalho que ninguém pediu, e a regra da casa é explícita: *não entregue
   mudança que ela não pediu*.
2. **O relato não é novo, e a casa já decidiu o que fazer com ele.** A
   [BORDA-DE-QUEDA-01](../sprints/2026-08-03-BORDA-DE-QUEDA-01-o-que-fica-para-tras-quando-um-controle-cai.md)
   registra, de 03/08, a frase dela *"desliga sozinho e o controle branco segue
   vibrando"*, e declara por escrito que **cair por Bluetooth é rotina** — a
   sprint trata as **consequências** (rumble preso), não a causa. Uma sprint nova
   não pode fingir que descobriu o fenômeno. GRAU: MEDIDO (leitura do documento).
3. **A [ESTADO-QUE-MENTE-01](../sprints/2026-08-03-ESTADO-QUE-MENTE-01-o-daemon-afirma-controle-conectado-com-a-mesa-vazia.md)
   é outro assunto.** Lá o `probe_offline` é só carimbo de hora; o defeito é o
   `daemon.state_full` continuar dizendo `connected: True` e `battery_pct: 85`
   **depois** da queda. É o estado obsoleto na descida, não a descida. GRAU:
   MEDIDO.
4. **A queda de 03/08 23:58:09 já tem dono:** o crash do `bluetoothd`, coberto
   pela
   [BT-SNAPSHOT-SANDBOX-01](../sprints/2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md).
   GRAU: MEDIDO.

O que **sobra** como custo de produto real, e não precisa de sprint para ser
nomeado: **`probe_offline` é um nome só para três coisas diferentes**, e é isso
que faz "três por dia" parecer um defeito único quando são cabo, `bluetoothd` e
link, em proporções diferentes.

---

## 4. A fila — três medições, nesta ordem

Convenção: **P0** tranca (com o destrancar embutido); **ANTES** é foto numérica;
**CONTRASTE** é o caso sem o qual nada se conclui; **PREVISÃO** é falsificável e
derivada do código; **ELA** / **ASSISTENTE** é a divisão de trabalho; **LEITURA**
é a tabela escrita antes de medir.

---

### Q-1. A bateria no fim explica as nove quedas de link? *(a que decide)*

**Pergunta.** Nas quedas em que o kernel fica mudo, a carga do controle estava no
fim?

**Por que é a primeira.** É a **única hipótese viva** para as nove, e hoje ela é
indecidível por falta de instrumento — não por falta de análise. Custo: uma noite
dela, sem atenção nenhuma durante.

**A hipótese, com o mecanismo.** O `upower` marcou o controle a 100%
`fully-charged` em 06/08 20:23:45; a sessão Bluetooth seguinte durou **16h24m** e
terminou em queda às 13:30:12 de 07/08; as duas retomadas depois duraram **2m28s**
e **25s**, e até 14h48 ele não voltou. Sessão longuíssima seguida de retomadas
cada vez mais curtas é a curva de uma carga acabando — e casa com a outra sessão
de 15h50m que também terminou em queda. GRAU: SUSPEITA COM MECANISMO.

E há uma consequência de produto embutida, que vale mesmo se a hipótese cair:
**nada nesta máquina deixa o controle dormir** (seção 2), então ele fica ligado a
noite inteira; a única pista que ela recebe é *"desligou sozinho"*.

**O estado do instrumento, conferido agora.** Ninguém grava carga ao longo da
sessão:

- o daemon **lê** a bateria por controle (`core/backend_pydualsense.py`, no
  handle do pydualsense) e publica `BATTERY_CHANGE` em `daemon/lifecycle.py:3744`
  e `:3825`, com debounce de `daemon/subsystems/poll.py`;
- e **não escreve uma linha no journal**: não há chamada de log de bateria em
  `daemon/lifecycle.py`, só o contador `battery.change.emitted` no store. GRAU:
  MEDIDO (busca direta no arquivo; e zero linhas de bateria no journal do daemon
  desde 06/08);
- o `upower` guardou **4 amostras** para este controle, nenhuma no fim da sessão,
  e o arquivo tem 116 bytes. GRAU: MEDIDO. **Não serve como régua.**

**P0 — trancar.**

1. Parar o `hefesto-bt-health-watchdog.timer`. Ele está `active` e dispara a cada
   ~2 min (GRAU: MEDIDO, 07/08 às 14h54), mexe em **trust e bond**, e chama
   `scripts/bt_active_mode.sh` a cada rodada. **Destrancar no fim:** religar o
   timer e conferir que voltou a `active`. Isto é passo do protocolo, não
   apêndice.
2. Garantir que a **suíte de testes não está rodando** — ela escreve no journal
   do sistema
   ([SUITE-QUE-SUJA-O-JORNAL-01](../sprints/2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md))
   e contamina a contagem.
3. **Não** parar o `hefesto-dualsense4unix.service`: aqui ele é o instrumento. O
   A/B com o daemon parado é a **Q-2**, e é outra janela, outra noite.
4. O controle **fora do cabo**. Com cabo, a medição responde outra pergunta — e
   oito das 18 quedas já são cabo.

**ANTES.** Com o controle recém-conectado por Bluetooth, gravar as **duas**
leituras no mesmo instante — regra da casa: todo instrumento declara contra o que
mede.

```bash
date -Is
hefesto-dualsense4unix battery
cat /sys/class/power_supply/ps-controller-battery-<mac>/capacity
cat /sys/class/power_supply/ps-controller-battery-<mac>/status
```

**O amostrador — não existe na árvore, e é uma linha.** Roda na janela `OS`, e
grava até o nó sumir:

```bash
mac=<o endereco real, sem mascara, SO na maquina dela>
no=/sys/class/power_supply/ps-controller-battery-$mac
while :; do
  printf '%s\t%s\t%s\n' "$(date -Is)" \
    "$(cat "$no/capacity" 2>/dev/null || echo AUSENTE)" \
    "$(cat "$no/status"   2>/dev/null || echo AUSENTE)"
  sleep 60
done | tee ~/queda-bateria-$(date +%F).tsv
```

**O arquivo resultante NÃO entra no repositório**: ele contém o endereço real. Se
virar evidência de documento, mascarar os octetos 4 e 5 — há portão, e ele
reprova.

**CONTRASTE.** Duas sessões, e sem as duas não se conclui nada:

- **(c1) carga cheia** — controle carregado até `fully-charged`, tirado do cabo, e
  deixado no rádio até cair;
- **(c2) carga baixa** — o **mesmo** controle deixado no rádio a partir de 20% ou
  menos.

Sem a (c1), uma queda com bateria baixa não distingue *"acabou a carga"* de *"cai
de qualquer jeito"*.

**PREVISÃO, falsificável.** Se a explicação for bateria: em (c1) a última amostra
antes da queda vem **abaixo de ~10%**, o `status` fica `Discharging` a sessão
inteira, e a duração de (c2) é **muito menor** que a de (c1). Se **não** for
bateria: (c1) cai com a última amostra **acima de 40%**, e as durações de (c1) e
(c2) ficam na mesma ordem de grandeza.

**A previsão que mata a hipótese de uma vez:** **uma** queda com `capacity` acima
de 40% na amostra imediatamente anterior **refuta** a bateria como explicação das
nove. Um caso basta — e por isso esta medição pode fechar numa noite.

**ELA.** Carrega o controle até o fim antes de (c1); tira do cabo; usa a noite
como sempre; e **avisa a hora** em que percebeu que caiu. **Não religa até
avisar** — o instante da volta é dado da Q-3.
**ASSISTENTE.** Deixa o amostrador rodando na janela `OS`, e **no instante** do
aviso dela colhe três coisas: `daemon.state_full`, as últimas 30 linhas do
amostrador, e o journal do kernel de -60 s a +10 s em torno da queda.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| última amostra abaixo de 10% e `Discharging`, e (c2) muito mais curta | bateria confirmada | a hipótese vira MEDIDA; a entrega passa a ser **avisar antes**, não curar queda |
| última amostra acima de 40% em (c1) | bateria REFUTADA | uma causa a menos; a **Q-2** sobe para primeira, e vira a única viva |
| última amostra entre 10% e 40% | inconclusivo | repetir a (c1); duas sessões, não uma |
| o nó `capacity` some **antes** da queda do daemon | o instrumento morre junto com o objeto | trocar para amostragem por `daemon.state_full`, que sobrevive ao sumiço do nó |
| não existe `ps-controller-battery` para este controle por Bluetooth | instrumento inexistente | usar só o `daemon.state_full` e **dizer isso no registro**; sem a segunda leitura, o resultado é de uma biblioteca só |
| nenhuma queda em duas noites | o fenômeno não apareceu | a janela é curta demais; **não concluir nada** — ausência aqui não é prova |

**Nota de instrumento.** O nó do kernel e o do daemon medem por caminhos
diferentes: o primeiro é do driver `hid-playstation`, o segundo é leitura própria
do handle. Se os dois discordarem em mais de um degrau, **o resultado é sobre o
instrumento**, não sobre a bateria — e a medição se refaz antes de qualquer
conclusão.

---

### Q-2. O daemon contribui para a instabilidade do link? *(hoje SEM PROVA)*

**Pergunta.** Com o Hefesto **parado**, o controle cai com a mesma frequência?

**Por que existe.** É a **única** pergunta desta lista em que o Hefesto pode ser
culpado, e hoje ela não tem medição nenhuma que a isole. GRAU: SEM PROVA — e é
assim que fica registrada, não como achado.

**O que se sabe, e não decide.** O daemon segura o hidraw físico aberto pelo
broker, reescreve o esconde a cada 30 s — `hidraw_broker_hidden` é o evento
**mais frequente** do journal, 14.105 ocorrências desde 01/08 — e escreve estado a
60 Hz. GRAU: MEDIDO. Mas na sessão que morreu em 07/08 o último re-esconde foi
**21 s antes** da morte, e os 19 a 21 s finais são de **silêncio total** no
journal. O desalinhamento **não apoia** a hipótese; também **não a mata**, porque
as escritas de 60 Hz não são logadas. GRAU: SEM PROVA, dos dois lados.

**Por que é a SEGUNDA.** Custa uma noite **sem o produto**. Se a Q-1 fechar em
bateria, esta janela não precisa existir.

**P0 — trancar.**

1. Parar o `hefesto-dualsense4unix.service` (do usuário) **e** o
   `hefesto-hidraw-broker.socket`. Sem o segundo, o broker sobe por ativação de
   socket no primeiro acesso e a janela deixa de ser limpa — o `.service` está
   `disabled` justamente porque quem o acorda é o `.socket`, que está `enabled`.
   GRAU: MEDIDO.
2. Parar também o `hefesto-bt-health-watchdog.timer`, pelo mesmo motivo da Q-1.
3. **Destrancar no fim:** religar os três e conferir `active` em cada um. Se
   algum não voltar, isso é o resultado mais importante da noite e vira sprint
   sozinho.

**ANTES.** A régua **não** é 18. É **9** — só as quedas de link, porque as de
cabo e a do `bluetoothd` não têm nada com o daemon. Nove em sete dias dá **1,3
por dia**. GRAU: MEDIDO.

**Instrumento, e ele MUDA de lado para lado.** Com o daemon parado **não existe**
`probe_offline`. A contagem passa a ser do **kernel**: cada volta registra uma
instância nova de device Bluetooth, e o número final sobe sempre (`.000C`,
`.000D`, `.0014`, `.001C`, `.001D`). GRAU: MEDIDO. Isso só é a mesma régua se o
lado **com** daemon for contado do mesmo jeito. **Contar pelo kernel nos dois
lados** — comparar `probe_offline` de um lado com registro de kernel do outro é o
erro que inventa o resultado.

**CONTRASTE.** A mesma duração de janela com o daemon **ligado**, no mesmo dia da
semana e na mesma faixa de horário. Sem isso, *"não caiu"* pode ser só uma noite
calma — e as quedas não são uniformes: 1, 1, 4, 3, 3, 3, 3 por dia. GRAU: MEDIDO.

**PREVISÃO, derivada do código.** Se o daemon contribui, com ele parado a taxa de
re-registro do kernel cai **para perto de zero** numa janela comparável. Se não
contribui, fica na mesma faixa — cerca de uma por noite.

**ELA.** Concorda com uma noite sem o produto, e usa o controle como sempre.
**ASSISTENTE.** Executa o P0, conta pelo kernel nos dois lados, e religa tudo no
fim conferindo o estado.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| zero re-registros sem o daemon, e 1 ou mais com ele, em janelas comparáveis | o daemon contribui | **vira sprint de defeito**, com faixa e causa; é o único caminho para isso |
| a mesma faixa dos dois lados | o daemon não contribui | a Q-2 fecha REFUTADA e sai da fila para sempre |
| zero dos dois lados | a janela não pegou o fenômeno | não concluir; repetir com janela maior ou esperar a Q-1 |
| o controle cai **mais** sem o daemon | o daemon estabiliza | registrar; é achado, e muda a conversa sobre o broker |
| algum serviço não volta no destrancar | defeito de ciclo de systemd | para tudo; o alvo passa a ser esse, e a regra da CURA-QUE-FERE-01 se aplica |

---

### Q-3. Quem reconecta — ela, ou o sistema? *(pega carona na Q-1)*

**Pergunta.** A volta do controle é ela apertando o PS, ou algo do host acordando
o aparelho?

**O estado, conferido agora.** O daemon **não tem caminho** para acordar controle
desligado: não há uma única chamada a `org.bluez` no código do daemon nem do
core, e o `connect()` que alimenta o probe é um `hidapi.enumerate()` puro. GRAU:
MEDIDO.

**Mas o host tem um caminho, e ele precisa ser contado.** O
`scripts/bt_health_watchdog.sh` **chama** `org.bluez.Device1.Connect()` — e só
atrás do portão `Connected == true` (`scripts/bt_health_watchdog.sh:161`), isto é,
com o ACL **já de pé**. GRAU: MEDIDO. Consequência exata: **não** é caminho para
acordar controle desligado, mas **é** caminho para completar uma volta que o
controle começou. Por isso ele é P0 na Q-1 — e por isso a Q-3 não pode ser
respondida com ele solto.

**O que se mede hoje, e não fecha.** Os tempos entre a queda e o próximo
`controller_connected` vão de **20 s a 15h29m**, com mediana perto de 2 min. GRAU:
MEDIDO. Que essa mediana seja *"o tempo de ela perceber e apertar o PS"* é GRAU:
SUSPEITA COM MECANISMO — o daemon **não registra a origem da volta**, e o
`ps_solo_released` só aparece com o controle **já** conectado, então o aperto que
o acorda é invisível.

**P0.** Nenhum além do da Q-1, com a qual esta compartilha a janela. O timer do
watchdog **já** está parado ali, e é isso que torna a Q-3 respondível.

**ANTES.** Anotar a hora do aviso dela e a hora do último `controller_connected`.

**CONTRASTE.** Uma queda em que ela **não encosta no controle por 10 minutos**.
Este é o passo inteiro: sem ele, "é ela" e "é o sistema" ficam colados.

**PREVISÃO, derivada do código.** Com ela sem tocar e o watchdog parado, **nenhuma**
volta acontece nesses 10 min — nenhum `BLUETOOTH HID` novo no kernel. Se aparecer
uma, a explicação *"quem reconecta é ela"* está **refutada**, e o próximo alvo é
descobrir quem chamou.

**ELA.** Ao perceber a queda, **avisa e não toca** por 10 min cronometrados.
**ASSISTENTE.** Observa o kernel na janela dos 10 min e registra o instante exato
do primeiro `BLUETOOTH HID` depois dela apertar.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| nada em 10 min, e a volta só depois do aperto | é ela | a suspeita vira MEDIDA; e o registro da borda de subida com origem passa a valer a pena |
| volta sozinho dentro dos 10 min, com o watchdog parado | não é ela | há um terceiro reconectando; achar quem é vira o alvo |
| volta sozinho **e** o watchdog estava vivo | medição inválida | o P0 falhou; refazer |
| ela não aguenta os 10 min | dado, não fracasso | anotar o tempo real esperado e repetir noutra queda |

---

## 5. O que falta de instrumento — e por que não virou entrega hoje

Três buracos, todos **MEDIDOS como ausência**, todos baratos. Ficam aqui como
**pendência**, não como entrega: a regra da casa é *não entregue mudança que ela
não pediu*, e ela relatou sem pedir conserto.

1. **Nenhuma linha de bateria no journal.** `daemon/lifecycle.py:3744` e `:3825`
   publicam `BATTERY_CHANGE` e incrementam `battery.change.emitted`, e **nada
   loga**. GRAU: MEDIDO. É por isso que a hipótese mais forte deste documento não
   pode ser nem fechada nem morta sem um amostrador externo.
2. **Um nome só para três fenômenos.** `daemon/connection.py:468` carimba
   `probe_offline` em cabo que saiu, `bluetoothd` que morreu e link que se perdeu.
   GRAU: MEDIDO. Separar os nomes é o que faria "três por dia" parar de parecer um
   defeito único — e nenhuma leva futura teria de refazer a classificação da seção
   1 à mão.
3. **A borda de subida não registra a origem.** GRAU: MEDIDO (ausência). É a única
   coisa que falta para a Q-3 fechar sem cronômetro.

---

## 6. Notas de instrumento — as armadilhas desta medição

- **`journalctl` sempre com data completa.** `--since "23:20"` sem data devolve
  zero em todas as janelas, e zero em todas é sinal de instrumento quebrado, não
  de ausência de defeito. GRAU: MEDIDO (custou uma medição inteira, registrado na
  fila de 06/08).
- **18 é piso.** Ver a seção 1. Quem repetir a contagem sem isto vai achar que
  mediu quedas de controle e terá medido quedas do **último** controle.
- **Endereços com a máscara da casa** — octetos 4 e 5 zerados — em **tudo** que for
  para o repositório. Há portão, e há furo conhecido: a forma compacta de 12
  dígitos corridos passa pelos dois portões (registrado na seção 6.4 da fila de
  06/08). GRAU: MEDIDO. O `.tsv` do amostrador da Q-1 **não é versionável** como
  está.
- **O `upower` não é régua.** Quatro amostras para este controle, nenhuma no fim
  da sessão. GRAU: MEDIDO.
- **O `bluetoothctl` está mudo nesta máquina** — `show`, `list` e `devices`
  devolvem vazio com saída 0 enquanto o D-Bus responde tudo. GRAU: MEDIDO para o
  sintoma, SEM PROVA para a causa. Nenhum passo pode depender dele; usar `busctl`.
- **`scripts/bt_active_mode.sh` não toca o DualSense** — só o Pro genuíno (OUI
  `e0:f6:b5`). GRAU: MEDIDO. Ele não é suspeito destas quedas; entra no P0 apenas
  porque o watchdog o chama junto com as vigias de bond.
- **A suíte de testes suja o journal do sistema.** Se ela estiver rodando, a
  contagem não vale.

---

## 7. O placar

- **18** quedas por `probe_offline` entre 01/08 e 07/08 — **piso**, não total; pelo
  kernel foram **26** (re)conexões Bluetooth de DualSense no mesmo período.
- **8** são o cabo USB saindo. **1** é o `bluetoothd` morrendo. **9** são perda de
  link com o kernel mudo.
- **0** defeitos do Hefesto medidos na queda. O daemon **percebe** um segundo
  depois do kernel.
- **1** hipótese refutada e datada nesta página: o sono por inatividade.
- **1** hipótese viva, com mecanismo e sem prova fechada: a bateria.
- **3** medições nesta fila; **1** delas decide, e cabe numa noite.

E a regra que este documento serve para lembrar: **hipótese tem de explicar o que
JÁ funcionava**. Duas sessões de mais de quinze horas são exatamente isso — o que
já funcionava — e é por elas que a explicação mais cômoda morreu.
