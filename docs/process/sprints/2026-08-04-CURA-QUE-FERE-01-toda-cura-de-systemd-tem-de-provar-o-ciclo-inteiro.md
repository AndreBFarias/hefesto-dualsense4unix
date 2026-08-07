# CURA-QUE-FERE-01 — toda cura de systemd tem de provar o ciclo inteiro

- **Nasceu de:** uma regressão minha, medida com ela às 02:45 de 04/08/2026
- **Gravidade:** alta — é um padrão, não um caso
- **Estado:** o caso individual está **CURADO**; o **padrão** está aberto
- **Pré-requisito:** nenhum. É código de teste e de portão.

> ### PODE EXECUTAR HOJE, SEM ELA
>
> Tudo aqui é arquivo de unit, teste e portão. Nenhum bloco precisa de hardware
> nem de medição na bancada.

---

## O que aconteceu, em uma frase

Curei um defeito de 90 segundos e criei outro que deixava o Bluetooth **sem
aceitar ninguém** — e o novo era pior que o velho.

---

## A cadeia, medida

Às 00:09:44 de 04/08 entrou `SendSIGKILL=yes` + `TimeoutStopSec=3s` no
`hefesto-bt-agent.service`, para curar um defeito real e medido: o agente não
responde ao SIGTERM quando o `bluetoothd` morre, e segurava o restart do BlueZ
por 90 segundos ([BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md)).

A cura funcionou: o restart caiu de 90 s para ~4 s.

**E abriu um buraco que ninguém viu por duas horas e meia:**

1. o systemd mata o agente ao fim dos 3 s;
2. morrer de `SIGKILL` **não é saída limpa**, então a unit vai para
   `failed (Result: timeout)`;
3. `Restart=on-failure` **não a traz de volta** — `on-failure` não cobre a morte
   durante um `stop` pedido por **outro** serviço (o `bluetooth.service`
   reiniciando);
4. a unit fica parada em `failed`, e **sem o agente de pareamento o BlueZ
   RECUSA toda conexão entrante**:

       profiles/input/server.c:confirm_event_cb() Refusing connection from <MAC>

Ela viu isso como *"o 8BitDo tá conectando automaticamente (e morre)"*, e
diagnosticou a causa antes de mim: *"desde que mexemos no storm hoje quebramos
alguma coisa e assim fica sem condições"*.

Medido: `failed` desde 02:32:41. Duas horas e meia de Bluetooth que conecta e
não aceita.

---

## Por que ninguém pegou — e é aqui que está o valor desta sprint

A cura foi **verificada**, e a verificação passou:

```bash
systemctl show hefesto-bt-agent.service -p TimeoutStopUSec   # 3s   OK
systemctl show bluetooth.service -p RestartUSec              # 1s   OK
```

**O campo estava lá. O comportamento não estava.** Conferi que a configuração
tinha entrado, e chamei isso de verificação — quando verificar uma cura de
systemd é exercitar o **ciclo que ela muda**, e olhar o estado da unit **depois**.

O teste que teria pego cabe em três linhas:

```bash
systemctl restart bluetooth.service
sleep 5
systemctl is-active hefesto-bt-agent.service    # tem de ser 'active', nunca 'failed'
```

E foi exatamente isso que provou a cura, quando finalmente rodei.

---

## A cura do caso (já aplicada)

`SuccessExitStatus=SIGKILL` no `hefesto-bt-agent.service`. Diz ao systemd o que
é verdade: para **este** serviço, ser morto no desligamento é o desfecho
**esperado** — ele é um agente sem estado em disco, e nós escolhemos matá-lo de
propósito. A unit para em `inactive`, e o `Wants=`/`After=` do drop-in do BlueZ
a religa junto com o `bluetoothd`.

Provado ao vivo: `bluetooth.service` reiniciado, o agente parou e voltou no
**mesmo segundo**, com `Agent registered`.

---

## A cura do PADRÃO — que é o trabalho desta sprint

**E1. Um teste de ciclo por unit que a casa instala.** Para cada unit em
`assets/systemd/`, um teste que a exercite de verdade: `start`, `stop`,
`restart`, e — quando ela tem `Wants=`/`After=` de outra — o **restart da
outra**. O aceite é sempre o mesmo e é simples: **a unit termina `active` ou
`inactive`, nunca `failed`**.

Este teste precisa de systemd de verdade, então tem de ser marcado e pulado com
recado honesto onde não houver (o CI). O que **não** pode é não existir.

**E2. O portão dos campos que se contradizem.** Um analisador dos arquivos de
unit que reprove combinações que a casa já pagou para descobrir:

| combinação | por que é armadilha |
|---|---|
| `SendSIGKILL=yes` sem `SuccessExitStatus=SIGKILL` | ser morto vira `failed`, e a unit não volta |
| `Restart=on-failure` numa unit que outra derruba | `on-failure` não cobre morte durante `stop` alheio |
| `ExecStopPost=` que escreve, em unit de terceiro com `ProtectSystem=strict` | o `ReadWritePaths` não é herdado — ver [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md) |
| `TimeoutStopSec` curto sem plano para o que sobra | a thread/processo morto pode deixar recurso preso |

A tabela **nasce destes dois incidentes e cresce a cada um novo**. É o mesmo
desenho da lista de armadilhas da `COMO-OLHAR-A-TELA`, para arquivos de unit.

**E3. O `doctor.sh` reprova unit da casa em `failed`.** Hoje ele emite `[WARN]`
(*"hefesto-bt-agent.service instalado mas failed"*), e foi assim que finalmente
achei o defeito — mas depois de duas horas e meia, e só porque eu estava lendo
a saída inteira por outro motivo. **Unit nossa em `failed` é FALHA, não aviso.**

**E4. O que a tela dela diz.** Com o agente de pareamento morto, a janela do
Hefesto não mudou uma linha — e o sintoma dela era do produto. A aba Sistema
tem de dizer, em português de quem usa: *"o agente de pareamento não está no ar
— controles novos não vão conseguir conectar"*.

---

## A lição de método, que vale além do systemd

**Verificar que a configuração entrou não é verificar que a cura funciona.**

A casa já tem a regra em outra forma — *"teste tem de MORDER: arranque a cura,
veja reprovar, devolva"* — e ela vale igual para configuração: **arranque o
`SuccessExitStatus`, reinicie o BlueZ, e veja a unit ir para `failed`.** Se
isso não acontecer, o teste não testa nada.

E a segunda lição, essa dela: **quem usa percebe antes de quem mede.** Ela
disse *"quebramos alguma coisa hoje"* com duas horas de antecedência sobre o
meu diagnóstico, e eu gastei parte desse tempo defendendo a hipótese errada (a
chave velha do 8BitDo, que a medição depois refutou — ele já tinha re-pareado
com chave nova por conta própria).

---

## Aceite

1. existe teste de ciclo para **toda** unit em `assets/systemd/`, e ele reprova
   se alguma terminar em `failed`;
2. arrancar o `SuccessExitStatus=SIGKILL` do `hefesto-bt-agent.service` faz
   esse teste **reprovar** — a mordida;
3. o portão de E2 existe, com a tabela, e reprova as quatro combinações;
4. `doctor.sh` trata unit nossa em `failed` como **FALHA**;
5. a janela diz, sem jargão, quando o agente de pareamento não está no ar.

---

---

## NOTA DATADA — 06/08/2026: a cura desta sprint **não faz o que diz**

Decisão medida não se apaga, e esta caducou pelo mecanismo. O texto acima
afirma que, com `SuccessExitStatus=SIGKILL`, *"a unit para em `inactive`, e não
em `failed`"*. **REFUTADO, MEDIDO, oito vezes desde que a cura entrou:**

```
ago 04 02:45:30  hefesto-bt-agent.service: Failed with result 'timeout'   <- 3 s DEPOIS do cp da cura
ago 04 04:06:00 / 11:26:48 / 14:12:37 / 23:19:09
ago 05 14:22:50 / 20:07:18
ago 06 21:04:38  hefesto-bt-agent.service: Failed with result 'timeout'
```

**Por quê:** `SuccessExitStatus=` reclassifica o **status de saída do
processo**. Aqui o resultado é `timeout`, gravado pelo systemd quando o estado
`stop-sigterm` estoura — **antes** de a morte do processo ser avaliada — e um
resultado de falha já posto não é limpo pelo `SuccessExitStatus`. A cura acerta
um alvo que não é o que produz o `failed`.

**E a "prova ao vivo" citada acima é um falso positivo, com carimbo.** Às 02:45
de 04/08:

```
02:45:26.938  sudo cp assets/systemd/hefesto-bt-agent.service /etc/systemd/system/...
02:45:27.132  sudo systemctl restart hefesto-bt-agent.service      <- o restart EXPLÍCITO
02:45:30.351  hefesto-bt-agent.service: Failed with result 'timeout'   <- a cura JÁ estava lá
02:45:30.363  Started hefesto-bt-agent.service                      <- voltou pelo restart
```

O agente voltou porque havia um job de start **explícito** na fila. Em 06/08 ele
voltou porque o `Requires=bluetooth.service` propagou o restart automático. Em
nenhum dos dois casos o `SuccessExitStatus` participou. **É exatamente a
armadilha que esta sprint nomeia — cometida dentro dela.** Quem devolve o
agente é a propagação de restart, e é isso que precisa ser dito no
`assets/systemd/hefesto-bt-agent.service` (linhas 66-70, que repetem a
afirmação refutada).

**Acrescenta (MEDIDO):** o `bt-agent` **nunca** responde ao SIGTERM — nem com o
`bluetoothd` vivo e são (o restart manual das 02:45:27 é a prova). A
[BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md)
atribui isso a *"quando o `bluetoothd` morre"*; a condição é mais larga.

**Ressalva honesta, para não inflar a gravidade:** seis das oito ocorrências
são no **desligamento da máquina**, onde não custam nada. As duas de dentro de
sessão recuperaram em 0,35 s e 3,0 s. O risco medido em 04/08 (2h30 sem agente)
**não voltou a acontecer** — mas também não foi curado pelo que esta sprint diz
tê-lo curado.

**Estado dos aceites em 06/08:** 1 e 2 **abertos** (`grep -rn 'systemctl
restart' tests/` só devolve `test_plataforma_wiring.py`, que **proíbe** a
string; não existe teste de ciclo). 3 **aberto**. 4 **aberto** (`doctor.sh`
segue `warn` para unit nossa em `failed`). A mordida prometida também não
existe: `TimeoutStopSec`, `SuccessExitStatus` e `SendSIGKILL` não aparecem em
`tests/` nem em `scripts/check_packaging_parity.sh` — nada pode reprovar por um
campo que ninguém lê. **DECLARADO:** não arranquei a cura para ver reprovar,
porque a ausência total da string nos testes e no portão já é conclusiva, e
mutar `assets/systemd/` numa árvore com outros agentes escrevendo é risco sem
ganho.

E a primeira linha da tabela de combinações desta sprint (`SendSIGKILL=yes` sem
`SuccessExitStatus`) precisa da mesma nota: o remédio que ela indica está agora
medido como **remédio que não cura**.

---

## Relacionado

- [BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md) — a cura que abriu este buraco
- [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md) — o outro caso de unit com comportamento que o ambiente não permite
- [DOC-QUE-NAO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md) — a família dos portões que dão `[OK]` no meio do defeito
