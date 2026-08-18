# BT-SDP-VAZIO-01 — o bond sem serviços, e o laço de reconexão

- **Status:** **CURADO E MEDIDO em 02/08/2026**, na máquina dela, com o 8BitDo
  na mão. Esta sprint nasce já fechada — é registro de causa-raiz, não plano
- **Aberta por:** queixa dela, literal: *"houve alguma regressão no controle
  8bitdo que deveria ser conectado como controle do dualsense 4 do ps4, ele tá
  se conectando automaticamente sem me permitir conectar ele aqui nessa tela
  (só funciona se eu conectar ele manualmente, hoje tá automático e algo apaga
  a conexão (isso é uma regressão))"*
- **Veredito sobre a palavra "regressão":** **não era regressão do nosso
  código.** Nenhuma linha do projeto causou o defeito. Mas uma cura NOSSA
  (o watchdog de trust) é o que transformou um defeito silencioso num laço
  visível — e isso importa, porque é o que ela sentiu mudar

## O sintoma, e por que ele engana

Três queixas numa só frase, e elas parecem contraditórias:

1. *"conecta automaticamente"* — sem ela pedir;
2. *"sem me permitir conectar nessa tela"* — o botão Conectar do COSMIC não
   resolvia;
3. *"algo apaga a conexão"* — e ela cai sozinha.

Parecem três defeitos. **São um só**, e a ordem causal explica as três.

## A causa-raiz, medida

O `info` do BlueZ dos dois controles, lado a lado — o Pro Controller
(funcionando) e o 8BitDo (quebrado):

| campo | Pro Controller | 8BitDo |
|---|---|---|
| `[LinkKey]` (o bond) | presente | **presente** |
| `Services=` com HID `0x1124` | presente | **AUSENTE** |
| `[DeviceID]` | presente | **AUSENTE** |
| `cache/<MAC>` → `[ServiceRecords]` | 1360 bytes | **35 bytes, só o nome** |
| `UUIDs` no D-Bus | preenchido | **`as 0` — vazio** |
| `ServicesResolved` | true | **false** |

**O bond existia; o registro de serviços SDP, não.** E o BlueZ recusa conexão
ENTRANTE de quem não tem o perfil HID registrado — literalmente, no journal:

```
profiles/input/server.c:confirm_event_cb() Refusing connection from E4:17:D8:00:00:83: unknown device
profiles/input/server.c:connect_event_cb() Refusing input device connect: No such file or directory (2)
src/device.c:search_cb() E4:17:D8:00:00:83: error updating services: Host is down (112)
```

E a conexão SAINTE também estava morta, por outra razão da mesma família:

```
$ busctl call org.bluez /org/bluez/hci0/dev_E4_17_D8_... org.bluez.Device1 Connect
Call failed: br-connection-key-missing
```

**A LinkKey estava no disco e não no kernel.** Um bond que existe em arquivo e
não existe para quem precisa dele é um bond que não existe.

### As três queixas, explicadas por essa única causa

1. **"conecta automaticamente"** — o controle chama, o BlueZ aceita o rádio
   (ACL). Isso é o rádio, não o perfil;
2. **"algo apaga a conexão"** — o BlueZ tenta resolver os serviços, falha, o
   perfil de input recusa (`unknown device`), o link cai. Nada "apaga": ele
   nunca chegou a subir;
3. **"só funciona se eu conectar manualmente"** — o gesto manual às vezes
   pegava uma janela em que o browse SDP completava.

## O papel da cura nossa — e é aqui que a palavra "regressão" tem razão

O `bt_health_watchdog.sh` (vigia 2b, de 23/07) aplica `Trusted=true` a todo
device com bond. Ele existe por um motivo bom e medido: sem trust, **reconexão
entrante é recusada como "unknown device"** — e o comentário do próprio script
nomeia o 8BitDo e o Pro como os casos que o motivaram.

O journal mostra o watchdog agindo, às 13:55:24:

```
device E4:17:D8:00:00:83 tinha bond mas estava SEM trust
(reconexão entrante recusada como 'unknown device') — Trusted=true aplicado
```

**Com `Trusted=false`**, o device não tentava reconectar sozinho: ela conectava
na mão, e o defeito ficava escondido atrás do gesto dela.
**Com `Trusted=true`**, o BlueZ passa a aceitar a reconexão entrante — e num
device de registro SDP vazio, o resultado é o laço.

**A cura não criou o defeito. Ela o tornou visível, e contínuo.** É a razão
honesta de ela ter sentido "regressão": o que mudou no comportamento dela
mudou por causa nossa, mesmo que a doença fosse anterior.

## A cura, e por que só ela serve

Testado primeiro o caminho barato, e ele falhou COM PROVA
(`br-connection-key-missing` acima). Só então o destrutivo, com autorização
dela:

1. `RemoveDevice` no adaptador — apaga `info` e a LinkKey morta;
2. **apagar também `cache/<MAC>`** — e este passo não é acessório. A lição
   `SDP-CACHE-01` (23/07) já custou o quarto controle a esta casa: é do
   `cache/<MAC>`, seção `[ServiceRecords]`, que o BlueZ tira o descritor HID.
   Um cache vazio sobrevivente faria o pareamento novo nascer igualmente sem
   serviços;
3. pareamento novo, com o 8BitDo em modo PS4.

### O resultado, medido

| | antes | depois |
|---|---|---|
| `UUIDs` | `as 0` | **`0x1124` (HID) + `0x1200`** |
| `ServicesResolved` | false | **true** |
| `Services=` no disco | ausente | **presente** |
| `[DeviceID]` | ausente | **`Vendor=0x054C Product=0x05C4`** |
| `cache/<MAC>` | 35 bytes | **1485 bytes** |
| hidraw | nenhum | **`0005:054C:05C4`** |

O `[DeviceID]` confirma de quebra o achado de 25/07: o 8BitDo por BT tem de
estar em **modo PS4** (`054c:05c4`), que é o que cai no `hid-playstation`.

E o watchdog aplicou `Trusted=true` 10 segundos depois — desta vez sendo a cura
que ele sempre pretendeu ser, porque agora existe perfil HID para o BlueZ
aceitar.

## O que fica em aberto, e é trabalho de verdade

**Por que o bond nasceu sem serviços?** Não medido. O `search_cb` falhando com
`Host is down (112)` sugere que o controle se cala antes de o browse completar
— plausível num 8BitDo, que economiza rádio agressivamente. Mas plausível não
é medido, e esta casa já pagou caro por confundir os dois.

**As três lacunas que este caso expôs. A primeira já está CURADA nesta leva:**

1. ~~**Nada detecta um bond sem serviços.**~~ **ENTREGUE em 02/08.** Ver "O
   check que existia e era cego", logo abaixo — é o achado de método desta
   sprint, e vale mais que a cura.
2. **O watchdog não sabe dizer "este device não".** Ele aplica `Trusted=true`
   a todo bond, sem exceção possível. Num device doente isso troca um defeito
   silencioso por um laço — e não há como pedir que ele pule um MAC.
3. **O snapshot de bonds fotografou o estado quebrado sete vezes** (todos os
   snapshots de 02/08 têm o `cache` de 35 bytes). Ele não tem como saber que o
   que está guardando não presta. Um snapshot que valide `[ServiceRecords]`
   antes de gravar guardaria só o que serve para restaurar.

## O CHECK QUE EXISTIA E ERA CEGO — o achado de método

A primeira reação, ao ver a queixa, foi *"o doctor devia ter apontado isso"*.
E ele **tem** um check exatamente para a família certa —
`check_bt_sdp_cache_envenenado`, escrito para a SDP-CACHE-01 de 23/07. Ele
rodou na máquina dela, no meio do defeito, e imprimiu:

```
[ OK ] cache SDP íntegro em todos os controles com bond (todos têm [ServiceRecords])
```

**Um "OK" sobre o controle que estava quebrado.** A razão está numa linha só,
o filtro de elegibilidade dele (`doctor.sh:2063`):

```bash
# Só device de perfil HID (0x1124 = HumanInterfaceDevice).
grep -qi '^Services=.*00001124-...' "${info_f}" || continue
```

**Ele só examina quem JÁ TEM `Services=` no `info`.** O 8BitDo não tinha
`Services=` nenhum — e por isso era descartado *antes* de ser olhado. O filtro
não estava errado para o que ele foi escrito (a SDP-CACHE-01 é justamente o
caso `info` COM serviços × cache SEM registros); ele é cego ao caso pior.

**A forma geral, e ela vale para muito além do Bluetooth:**

> Um check que primeiro filtra "só devices sadios o bastante para me
> interessarem" fica **cego na proporção da gravidade** — quanto pior o
> defeito, menos ele o enxerga. E o silêncio dele não é neutro: sai como um
> `[ OK ]` verde, que é pior que nenhuma linha.

É prima da lição de 01/08 (*"medir contra a biblioteca errada produz alarme
convincente e falso"*) e da refutação da PARIDADE-SONY-01 no mesmo dia (*"o
instrumento estava certo e respondia a pergunta errada"*). As três são a mesma
doença: **o instrumento passou no próprio teste e mediu outra coisa.**

### A cura, e por que ela não mexeu no check antigo

Um check NOVO em `check_bt_radio`, que pergunta ao D-Bus em vez de ao disco:
device `Paired` cujos `UUIDs` não contêm `0x1124` vira `[FAIL]`, com a cura
escrita na mensagem (incluindo o `rm` do `cache/<MAC>`, sem o qual o
pareamento novo nasce igual).

Deixar o antigo intacto é deliberado: ele responde bem a pergunta dele, e
alargá-lo para cobrir os dois casos faria um check com duas razões de existir —
que é como se perde a capacidade de dizer o que cada `[FAIL]` significa.

Três testes herméticos (`tests/unit/test_doctor_bond_sem_servicos.py`), com
`busctl` fake, e as duas mordidas conferidas: inverter a condição e tirar a
guarda de `Paired` reprovam.

## O que NÃO fazer

- **Não desligar a vigia 2b do watchdog.** Ela cura um defeito real e medido
  em 23/07. O problema nunca foi ela — foi o device doente por baixo.
- **Não remover bond sem remover o `cache/<MAC>` junto.** Ver passo 2 acima;
  é a lição `SDP-CACHE-01` e ela já custou um controle.
- **Não concluir "conectou sozinho, logo está curado"** sem olhar `UUIDs` e
  `ServicesResolved`. O rádio subir não é o perfil subir — foi exatamente essa
  confusão que fez o defeito parecer três defeitos.
