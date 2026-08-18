# A LUZ QUE CUROU-01 — calar parou o bombardeio, e voltar tem preço

- **Achado em:** 07/08/2026, entre **15h27** e **20h53**, na **máquina dela
  viva**, com **três** controles no rádio no momento da leitura (o Pro
  `E0:F6:B5:00:00:53` e os dois DualSense `14:3a:9a:00:00:ab` e
  `a0:fa:9c:00:00:f0`; o 8BitDo `e4:17:d8:00:00:83` **saiu do rádio** durante a
  tarde). Todos os números deste documento foram **recontados agora**, não
  copiados
- **Estado:** **DIAGNÓSTICO. Nenhuma linha de código tocada.** Leitura pura:
  nada escrito em `hidraw`, nenhum serviço reiniciado, nenhum controle
  derrubado, nenhum arquivo dela alterado. O que só fecha medindo virou
  **protocolo**, no fim deste documento
- **Gravidade:** **ALTA**, e por três razões distintas: (1) o produto martelou o
  firmware do controle dela **348 vezes** e nunca soube; (2) o defeito de
  desenho por trás disso é uma **classe**, não um caso — vale para qualquer
  aparelho em que a escrita possa falhar no meio; (3) a cura que está de pé
  hoje é **acidental**, e a casa não pode confiar num remédio que ninguém
  receitou para esta doença
- **Causa-raiz:** **MEDIDA — e não é a que a casa tinha escrito.** A cadeia
  registrada na seção 4.2 do
  [estudo dos externos de 07/08](../estudos/2026-08-07-ISOLAR-os-externos-o-metodo-da-lightbar-no-pro-e-no-8bitdo.md)
  está **certa no desfecho e errada no meio**. Três dos cinco passos dela caem
  com medição, e o que sobra no lugar é maior: o produto pinta, num LED físico
  caro e lento, uma grandeza **derivada e volátil**, calculada de um conjunto
  que dois escritores em cadências diferentes fazem oscilar
- **Índice:** [A ordem de execução do que o diagnóstico abriu](2026-08-07-INDICE-a-ordem-de-execucao-do-que-o-diagnostico-abriu.md)
  — **e ATENÇÃO:** aquele índice foi escrito às 21h01 de 07/08, **antes** desta
  sprint existir, e por isso **não a cita**. Quem for executar a fila tem de
  encaixar esta sprint nela; a seção 5 daqui diz em que posição, e por quê.
  O índice anterior é
  [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md),
    **defeito 1** — **a mãe desta, e ela é de 03/08.** Nomeou a causa-raiz com
    caminho e linha (`_connected` com dois escritores) e **previu o sintoma na
    voz dela**, quatro dias antes de o storm existir. Continua **ABERTA**;
  - [QUATRO-NO-RÁDIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md),
    **B4 e B5** — já trazia `external_led_repintado intruso=3` e `intruso=2`
    medidos, já desenhou a cura de raiz
    (`slot_for(uniq, assign=True, mark_present=False)`) e já escreveu a regra
    que esta sprint herda inteira: *"estender um detector que mente é importar o
    falso positivo em vez de curá-lo"*. Continua **ABERTA**;
  - [DUAS CONTABILIDADES-01](2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md)
    — **a metade que falta**. Esta sprint trata do **custo** de escrever; aquela
    trata do **número** a escrever. As duas se encontram na ordem que este
    documento impõe, e nenhuma das duas resolve a outra;
  - [LUGAR À MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)
    — a dona da `E0` (a luz calada) e da `E3` (o externo virar jogador de
    verdade). **Esta sprint não mexe em entrega nenhuma daquela**, e a `E3`
    segue atrás da [MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md)
    por decisão dela;
  - [REGRA-NÃO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md)
    — a doutrina que mata a saída *"não escreve no Pro, escreve só no 8BitDo"*:
    a cura tem de ser **regra**, não **registro**;
  - [os externos — a referência canônica](../../protocol/externos-referencia-canonica.md)
    — a seção 3.4 (o limitador), a 3.6 (os cinco subcomandos por chamada) e a
    dívida 7.2, itens 5 e 6. Esta sprint **paga** o item 6 e **enfileira** o 5.

> **Grau de cada afirmação**, como manda a casa: **MEDIDO** = há leitura ao
> vivo, linha de journal, arquivo lido ou teste que reprova com a cura
> arrancada; **SUSPEITA COM MECANISMO** = o caminho de código foi lido ponta a
> ponta e fecha, o efeito não foi observado; **SEM PROVA** = está dito e
> ninguém verificou.
>
> **Endereços de rádio:** todos **mascarados** pela convenção da casa (octetos 4
> e 5 zerados). Há portão que reprova o contrário.

---

## O pedido dela, palavra por palavra

07/08/2026, sobre o fato de que calar a luz curou, por acidente, o bombardeio
que ninguém sabia que existia:

> *"materializa isso com calma, essa complexidade deve ser considerada"*

Ela não pediu um resumo. Pediu que a complexidade **não fosse simplificada para
caber numa resposta**. Este documento obedece a isso literalmente: onde a
medição contradiz o que a casa já escreveu, a contradição fica escrita; onde
duas frentes discordaram, as duas ficam com o número que cada uma trouxe; e
onde não há prova, está dito que não há.

---

## 1. O FATO — os números, e o que aconteceu às 15h27:48

**GRAU: MEDIDO. Tudo nesta seção foi recontado em 07/08/2026 às 20h53**, na
máquina dela, com os comandos citados.

### 1.1 O A/B que aconteceu sozinho

Não foi experimento. Foi um reinício de serviço que levou uma **decisão dela**
à máquina, e o antes e o depois ficaram gravados no journal.

| métrica | **lado A** — a luz falando | **lado B** — a luz calada |
|---|---|---|
| janela | 06/08 00h00 até **07/08 15:27:48** (19h04m de daemon vivo) | **15:27:48** até 20h53 = **5h25m** |
| escritas de LED externo (`external_led_written`) | **36** — 18 no Pro, 18 no 8BitDo | **0** |
| repinturas (`external_led_repintado`) | **11** — **todas** no Pro | **0** |
| recusas do kernel (`joycon_enforce_subcmd_rate: exceeded max attempts`) | **348** — 146 em 06/08, **202** em 07/08 | **0** |
| falhas de escrita (`Setting an LED's brightness failed (-110)`) | **83** — 34 em 06/08, **49** em 07/08 | **0** |
| avisos **do daemon** sobre falha de LED | **0** | **0** |
| última linha de storm do boot inteiro | **15:24:04.932358** | — |

Comandos: `journalctl -k` com janela por dia e `grep -c`; `journalctl --user -u`
da unidade `hefesto-dualsense4unix` para as escritas e repinturas.
`NRestarts=0` e `ActiveEnterTimestamp=Fri 2026-08-07 15:27:48 -03` (`systemctl
--user show`), portanto o cronômetro do lado B **não foi reiniciado** e vale
inteiro.

### 1.2 O que aconteceu às 15h27:48 — e a honestidade sobre isso

O reinício levou à máquina o `EXTERNAL_PLAYER_LED_ENABLED = False`, que é a
**décima segunda decisão dela**, de 07/08, registrada em
`docs/process/2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md`:

> *"calar a luz até a entrega existir."*

**Ela tomou essa decisão por HONESTIDADE, não por custo.** O critério dela,
transcrito no painel, é *"o produto não pode AFIRMAR jogador"* enquanto o
controle externo não for jogador de verdade dentro do jogo. A casa tem
registrado que **ela distingue os controles pela cor da luz e pelo LED de
jogador**, e ela aceitou **perder o próprio instrumento** para que o produto
pare de afirmar o que não cumpre. GRAU: MEDIDO (o texto do painel, o comentário
em `daemon/subsystems/external_identity.py` e o valor da constante).

**E a decisão curou, por acidente, um defeito técnico que ninguém sabia que
existia.** O gate faz `return` **antes** do laço de escrita, e o laço de escrita
era o único caminho que alimentava o storm. Os dois contadores zeraram no mesmo
minuto e não voltaram em 5h25m.

**A frase que a casa tem de guardar desta seção:** *o remédio funciona, e
ninguém o receitou para esta doença*. Uma cura acidental é uma cura que se
desfaz sem aviso — no dia em que a `E3` existir e a constante voltar para
`True`, **o storm volta com ela**, a não ser que o que está descrito na seção 2
seja curado antes.

### 1.3 O preço por escrita, e ele é grande

Com 18 escritas no Pro e 348 recusas no lado A:

| conta | valor | GRAU |
|---|---|---|
| recusas do kernel por escrita no Pro | **19,3** | MEDIDO (aritmética sobre os dois contadores recontados) |
| falhas `-110` por escrita no Pro | **4,6** | MEDIDO |
| custo de uma cascata, ponta a ponta (episódio de 15:23:01.116 a 15:23:06.481) | **5,365 s**, com 20 recusas e 5 `-110` | MEDIDO |
| custo de uma cascata de três lâmpadas (15:24:01.573 a 15:24:04.932) | **3,359 s**, com 13 recusas e 3 `-110` | MEDIDO |
| tempo que o daemon leva para fazer as **cinco** escritas de `sysfs` do Pro | **373 microssegundos** | MEDIDO (a escrita do 8BitDo às 15:23:00.852898 e a do Pro às 15:23:00.853271) |

**O "12 recusas em 3,7 s" do estudo de 07/08 e o "20 recusas em 5,4 s" desta
página são o MESMO fenômeno**, medido em episódios de tamanho diferente: um de
três lâmpadas e outro de cinco. A aritmética é a mesma, **quatro recusas por
lâmpada**, que é exatamente o `sync_send_tries=4` do módulo DKMS desta casa.
GRAU: MEDIDO (a régua está na seção 1.1 da referência canônica dos externos).

### 1.4 O `-110` NÃO vem do rádio — e quem ler errado inverte a conclusão

**GRAU: ALTA** (segue do código, dado o parâmetro medido), e já está registrado
na seção 3.4 da referência canônica dos externos.

`-110` é `ETIMEDOUT`. Com `skip_tx_on_rate_exceeded=Y` — que é o que a máquina
dela carrega, porque o módulo é o DKMS desta casa e não o vanilla — o
`joycon_enforce_subcmd_rate` devolve `-EAGAIN` ao estourar as 25 tentativas, o
envio síncrono converte em `-ETIMEDOUT`, e **nenhum byte vai ao ar**
(`assets/dkms/hid-nintendo/hid-nintendo.c`, o limitador e o envio síncrono).

**Consequência para a leitura desta sprint:** o storm era de **CPU, de mutex e
de log**, não de rádio. Quem disser "o bombardeio degradou o Bluetooth dela"
está lendo errado — **no vanilla estaria certo**, e é justamente por isso que o
remendo desta casa existe.

E há um segundo custo, que não aparece em contador nenhum: cada tentativa
recusada segura o `output_mutex` do controle. Uma cascata de 5,4 s é 5,4 s em
que **rumble e qualquer outro subcomando para aquele Pro ficam na fila**.
GRAU: SUSPEITA COM MECANISMO (o caminho fecha no driver; o efeito não foi
observado em jogo).

---

## 2. O ACHADO QUE VALE MAIS QUE O NÚMERO — o defeito de desenho

Esta é a seção que ela pediu que não fosse simplificada.

### 2.1 O detector está ligado ao sensor errado

**A afirmação, em uma linha:** o `read_player_pattern` **não enxerga lâmpada
nenhuma**. Ele lê o eco do nosso próprio pedido.

**GRAU: MEDIDO, agora, na máquina dela.** Os cinco nós do Pro leem:

```
0005:057E:2009.0017:green:player-1/brightness = 1
0005:057E:2009.0017:green:player-2/brightness = 1
0005:057E:2009.0017:green:player-3/brightness = 0
0005:057E:2009.0017:green:player-4/brightness = 0
0005:057E:2009.0017:blue:player-5/brightness  = 0
```

`read_player_pattern` sobre isso devolve **2** — que é exatamente o slot que o
daemon pediu às 15:24:01. **E a escrita do `player-2` daquela chamada FALHOU**,
com `-110` às 15:24:02.394511, junto com `player-3` às 15:24:03.519485 e
`player-4` às 15:24:04.663528. **Três dos cinco nós falharam no hardware, e os
cinco leem o valor pedido.**

**O mecanismo, e ele é do kernel, não nosso:** a classe LED grava o valor pedido
em `brightness` **antes** de tentar o hardware e **nunca o reverte** quando o
`brightness_set_blocking` falha. No `hid-nintendo` a escrita ainda é
**assíncrona** — o `joycon_player_led_brightness_set` só enfileira o trabalho —,
então o `write(2)` do `sysfs` **volta com sucesso antes de o erro existir**.
GRAU: ALTA (o caminho no driver) + MEDIDO (o resultado acima).

**A aritmética do atraso, medida:** as cinco escritas de `sysfs` do Pro
couberam em **373 microssegundos**; a primeira recusa do kernel apareceu
**355 ms** depois; o primeiro `-110`, **1,18 s** depois; o último, **3,45 s**
depois. GRAU: MEDIDO.

**Corolário duro:** `_set_brightness` (`core/external_leds.py`) só devolve
`False` se o `open`/`write` levantar `OSError`. Como o erro do driver nunca
chega ao `write(2)`, **não existe em ponto nenhum da árvore um caminho que saiba
que a escrita falhou**. E isso está confirmado do outro lado: **83** falhas no
kernel e **ZERO** avisos do daemon no mesmo período (`grep external_led` no
journal da unidade devolve só `external_led_written` e `external_led_repintado`,
os dois de sucesso). GRAU: MEDIDO.

### 2.2 A cadeia que a casa escreveu — o que cai, com medição

A seção 4.2 do estudo dos externos de 07/08 descreveu um laço em cinco passos.
**O desfecho dela está certo — a escrita é nossa e o storm é dela.** Três dos
cinco passos caem.

| passo, como está escrito | desfecho | GRAU |
|---|---|---|
| 1. o NUMA-03 manda reler o padrão antes de pular por cache, e repintar se divergir | **de pé** | MEDIDO (o código, e as 11 linhas de `external_led_repintado`) |
| 2. *"a primeira lâmpada passa, as outras morrem em `-110`"* | **REFUTADO** | MEDIDO |
| 3. *"a releitura devolve SEMPRE um número diferente do pedido"* | **REFUTADO, e é o achado mais importante** | MEDIDO |
| 4. o tick conclui "escritor estrangeiro" e repinta | **de pé, mas o rótulo é falso** | MEDIDO |
| 5. *"volta ao passo 2, para sempre"* | **REFUTADO** | MEDIDO |

**Passo 2 — o subconjunto que passa é arbitrário, e não é prefixo.** Em **16**
episódios no kernel desde 06/08, em **11** deles **todas as cinco** lâmpadas
falharam. Nos cinco restantes: em 06/08 21:07:11 a primeira passou; em 07/08
13:30:15 as **duas últimas** passaram; em 07/08 14:38:10 passou **só a
segunda**; em 07/08 15:22:13 falhou **só a `player-2`**; em 07/08 15:24:02
passaram a primeira e a última. GRAU: MEDIDO.

**Passo 3 — a releitura devolve o número PEDIDO, com ou sem falha no rádio.**
É a seção 2.1 inteira. Este passo não é "impreciso": ele é o **oposto** do que
acontece.

**Passo 5 — o laço não se realimenta. E a aritmética o mata sozinha.** Um laço
travado no piso de `LED_MIN_INTERVAL_SEC = 2,0 s` produziria da ordem de
**34 000** escritas nas 19h04m do lado A. **Foram 18 no Pro** — uma a cada
**63,6 minutos**. GRAU: MEDIDO.

### 2.3 O que sobra no lugar — e por que é pior

**A cegueira do detector é exatamente o que impediu o laço infinito.**

O caminho, lido ponta a ponta em `daemon/subsystems/external_identity.py`:
depois de uma repintura, `_last_value[key] = slot`; a releitura devolve o valor
**pedido**, que é `slot`; logo `padrao == slot`, não há `intruso`, e o cache por
valor pula. **O laço termina porque o detector não enxerga a falha.**
GRAU: SUSPEITA COM MECANISMO (o caminho fecha inteiro; o que está MEDIDO é o
efeito — 18 escritas, não 34 000).

> **A consequência é a linha mais importante desta sprint, e ela inverte a
> intuição:**
>
> **Curar o detector para que ele ENXERGUE a falha da escrita, sem antes tornar
> a escrita barata, LIGA o laço infinito que hoje não existe.** Um detector
> honesto veria "pedi 2, o hardware está em outra coisa", repintaria, falharia
> de novo, e repintaria de novo — a cada 2 s, para sempre, a 5,4 s de trabalho
> no kernel por rodada.
>
> Esta é a razão técnica pela qual a ordem da seção 5 não é preferência.

**E o que realmente bombeia o sistema é a renumeração.** As 18 escritas do Pro,
com hora e slot, do journal da unidade:

```
06/08 20:23:18  slot=2   (sem repintura — daemon novo, cache vazio)
06/08 20:50:19  slot=2   (sem repintura)
06/08 20:50:49  slot=2   (sem repintura)
06/08 20:53:40  slot=2   (sem repintura)
06/08 20:54:10  slot=2   (sem repintura)
06/08 21:07:09  slot=2   (sem repintura)
06/08 22:21:14  slot=2   (sem repintura)
07/08 01:56:53  slot=2   repintado intruso=0     <- a ÚNICA que só o NUMA-03 causou
07/08 13:30:14  slot=1   repintado intruso=2
07/08 14:34:48  slot=2   repintado intruso=1
07/08 14:37:13  slot=1   repintado intruso=2
07/08 14:38:09  slot=2   repintado intruso=1
07/08 14:38:29  slot=1   repintado intruso=2
07/08 15:22:12  slot=2   repintado intruso=1
07/08 15:23:00  slot=1   repintado intruso=2
07/08 15:23:31  slot=2   repintado intruso=1
07/08 15:23:41  slot=1   repintado intruso=2
07/08 15:24:01  slot=2   repintado intruso=1
```

**GRAU: MEDIDO.** Duas leituras saem daí, e as duas importam:

1. **O `intruso` é SEMPRE o slot que o próprio daemon escreveu na vez
   anterior.** Em **11 de 11** ocorrências. O rótulo *"escritor estrangeiro"* da
   docstring do `ExternalLedSync` é **literalmente falso** em todas elas. O
   detector compara o padrão lido contra o slot **novo** (`padrao != slot`), e
   não contra o que nós escrevemos por último — então ele acusa intruso **toda
   vez que o número muda**.
2. **Em 10 das 11, o cache por valor teria escrito de qualquer jeito**, porque o
   slot mudou. **Só uma** (07/08 01:56:53, `slot=2` com `intruso=0`, quando a
   escrita anterior no mesmo aparelho também tinha sido `slot=2`) foi disparada
   **exclusivamente** pelo detector. A causa de o padrão ter ido a zero naquela
   hora **não foi identificada** — não há linha de suspend/resume na janela
   01h50-02h05. GRAU: **SEM PROVA** para a causa; MEDIDO para as linhas.

**Portanto: o NUMA-03 não é o motor do custo — ele custou UMA escrita em 19
horas.** O dano dele é de outra natureza, e é dupla: **epistêmico** (envenenou o
diagnóstico da casa, que passou dias acreditando num laço que não existia) e
**estrutural** (é uma defesa que fura o cache por valor com base numa leitura
que mente, e que está **morta por construção** no 8BitDo — seção 2.5).

### 2.4 A CLASSE, com nome — e é isto que sobrevive a este aparelho

Retirando o Pro, o Nintendo e o Bluetooth da frase, o que sobra é:

> **O produto pinta, num atuador físico caro e lento, uma grandeza DERIVADA e
> VOLÁTIL — "colocação entre quem está presente AGORA" —, calculada de um
> conjunto que dois escritores em cadências diferentes fazem oscilar; e verifica
> o resultado por um sensor que é o eco do próprio pedido.**

São **quatro** defeitos independentes, e cada um tem cura própria:

| # | o defeito | onde | GRAU |
|---|---|---|---|
| **D1** | o valor escrito é **derivado da presença**, não do lugar na fila — muda sem que nada do aparelho mude | `slot_for` devolve `_posicao_locked`, que soma os DualSense presentes | MEDIDO |
| **D2** | a fonte da presença tem **dois escritores em cadências diferentes** — o tick **substitui** o conjunto a cada 2,0 s, o provider de cor **adiciona** a 10 Hz | `daemon/subsystems/identity.py`, com a fiação em `daemon/subsystems/external_identity.py` | MEDIDO — e **já estava escrito em 03/08** |
| **D3** | a escrita **não sabe se falhou**: `escreveu = _set_brightness(...) or escreveu` declara sucesso com **uma** lâmpada de cinco, e o cache guarda o valor como se tudo tivesse ido | `core/external_leds.py`, em `write_player_number` e em `write_lightbar_slot` | MEDIDO |
| **D4** | o **verificador** lê o eco do pedido, não o aparelho — e chama de estrangeiro a nossa própria escrita anterior | `read_player_pattern` + a comparação no tick | MEDIDO |

**A assinatura de D2, medida no journal de 07/08:** o Pro alterna **2, 1, 2, 1,
2** e o 8BitDo alterna **3, 2, 3, 2, 3** nos **mesmos instantes** (15:22:12,
15:23:00, 15:23:31, 15:23:41, 15:24:01). Os dois deslocam **em trava**, somando
sempre 3. É exatamente o que um DualSense entrando e saindo de `_connected`
produz: o piso muda de 0 para 1 e volta. GRAU: MEDIDO.

**E isto não é descoberta de hoje.** A
[QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md),
de **03/08**, defeito 1, nomeou D2 com caminho e linha, registrou que
`mark_disconnected` não tem chamador de produção — o que fecha o argumento — e
**previu o sintoma na voz dela**:

> *"com a janela do Hefesto aberta, quando um controle pisca os outros trocam de
> cor e de número sozinhos, e voltam"*

E a
[QUATRO-NO-RÁDIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md),
no mesmo dia, item B4, já trazia `external_led_repintado intruso=3` e
`intruso=2` medidos — *"o Pro Controller renumerado duas vezes em 24 segundos"*
— e a cura de raiz desenhada: **separar os eixos**, com
`slot_for(uniq, assign=True, mark_present=False)`. **As duas continuam
ABERTAS.** GRAU: MEDIDO (os dois documentos, lidos).

**O que esta sprint acrescenta a elas** é o preço em plástico: aquilo que em
03/08 era "o número dança na tela" virou, com o Pro na mesa, **348 recusas de
firmware e 83 falhas de escrita**.

### 2.5 O 8BitDo NÃO tem este laço — e tem o defeito irmão, invisível

Isto muda o desenho da `E3`, e por isso está aqui e não numa nota de rodapé.

**Ele não tem o laço. Três medições independentes:**

1. **ZERO** linhas de erro de LED para o `054C` no `journalctl -k` do boot
   inteiro, contra **83** no Nintendo. Nenhuma escrita de lightbar falhou nunca.
2. **ZERO** `external_led_repintado` para ele, contra **11** no Pro — com
   **18** `external_led_written` para **cada um**. Mesma quantidade de escritas,
   custo radicalmente diferente.
3. O `hid-playstation` **não tem limitador de taxa nenhum**: a escrita da
   lightbar grava um campo sob spinlock e agenda o trabalho, devolvendo 0
   sempre (`assets/dkms/hid-playstation/hid-playstation.c`).

GRAU: MEDIDO para (1) e (2); ALTA para (3). Já está na seção 4.3 da referência
canônica dos externos.

**E tem o defeito irmão, que é pior porque é invisível por construção:**

- **não existe leitor espelho de `write_lightbar_slot`.** O `read_player_pattern`
  só sabe ler a barra verde; no caminho `ds4` esses nós não existem e ele
  devolve `None` na primeira falha de `open`. O tick trata `None` como skip
  explícito. **A defesa NUMA-03 está estruturalmente MORTA no 8BitDo.**
  GRAU: MEDIDO (o código, lido nos dois lados);
- **`write_lightbar_slot` descarta o retorno da escrita do nó `:global`** e
  devolve `True` se **qualquer um** de vermelho/verde/azul aceitou — o mesmo D3,
  com uma agravante: o mestre da lightbar pode ter falhado e o produto declara
  sucesso. GRAU: MEDIDO;
- **consequência medida:** o 8BitDo foi renumerado **18 vezes** pelo mesmo
  `_connected` que dança, o que na lightbar significa a cor indo de vermelho
  para verde e de volta — **sem uma linha de log** dizendo que houve disputa.

**E há uma pergunta anterior a tudo isso, e ela é dela:** a **P-4** da
referência canônica dos externos ainda não respondeu se aquele plástico tem
lâmpada colorida física, ou se os quatro LEDs azuis dele são só indicadores de
modo. **Se não houver lâmpada, o caminho `ds4` inteiro é escrita em nó que não
acende.** Custo: cinco segundos de olho dela. GRAU da pergunta: MÉDIA, por nunca
ter sido olhada.

### 2.6 Um terceiro laço, latente, que a `E3` tem de fechar antes de religar

**GRAU: SUSPEITA COM MECANISMO. Não ocorreu na máquina dela, e o motivo está
medido.**

`write_player_number` **capa** o slot em 4 quando não há nó azul; o tick compara
o padrão lido contra o slot **não capado**. Num aparelho sem a quinta lâmpada,
em slot 5 ou maior, a comparação é `4 != 7` **para sempre** — e aí sim há um
laço de repintura genuíno, a cada 2 s.

Não aconteceu aqui porque o Pro `.0017` **tem** o nó azul
(`blue:player-5/max_brightness` = 15, lido agora). GRAU: MEDIDO para a ausência
do efeito; SUSPEITA COM MECANISMO para o laço.

**E este item encosta na dívida 7.2, item 5, da referência canônica dos
externos**, que diz com todas as letras *"não voltar sem corrigir"*: o
`blue:player-5` **não é um quinto jogador — é o LED HOME**, escala 0-15,
subcomando `0x38` e não `0x30`. O produto escreve `1` num nó que vai a 15, e
gasta um subcomando por chamada para afirmar uma coisa errada.

---

## 3. A TENSÃO, honesta, sem escolher por ela

Ela quer os quatro controles numerados. Isso está registrado, é legítimo, e é
para isso que a lâmpada existe. **Voltar a numerar custa três coisas
diferentes, e elas não se misturam.**

| | o que é | quem decide | o que a resolve |
|---|---|---|---|
| **(a)** | a luz está **calada por decisão dela** (decisão 12, 07/08) | **ela, e só ela** | a `E3` da LUGAR À MESA-01 existir — e a `E3` está atrás da MÁSCARA-01, também por decisão dela |
| **(b)** | reacender **reabre o bombardeio**: 348 recusas e 83 falhas medidas | engenharia | escrita que não custe cinco subcomandos por número, e que saiba se falhou |
| **(c)** | o número **é o errado**: a lâmpada conta a mesa inteira, o co-op conta só os DualSense adotados, e as duas nunca se falam | engenharia, **com o olho dela** | uma só conta |

**(b) e (c) são independentes.** A cura de (b) não toca um número. A cura de (c)
não escreve um byte em externo nenhum.

**E (c) se mede HOJE, sem tocar na luz dos externos.** A luz dos **DualSense**
nunca foi calada. A
[DUAS CONTABILIDADES-01](2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md)
mediu, às 19h10 de 07/08: **o co-op registrou o roxo como segundo jogador, logo
o branco é o Jogador 1 do jogo — e a fila da casa faz o branco acender 4**,
porque conta os dois externos presentes à frente dele. **As duas lâmpadas
mentem, e mentem trocadas.** GRAU: MEDIDO (naquela sprint).

**A frase que fecha a tensão, com todas as letras:**

> **Curar (b) sem curar (c) devolve número ERRADO ao plástico, mais barato e com
> mais confiança.**

E é pior do que isso para os externos: **hoje não existe número certo nenhum
para eles.** Eles não são jogadores dentro do jogo, e a conta que o jogo enxerga
não os inclui. Acender qualquer número neles antes da `E3` é afirmar o que não
se cumpre — que é exatamente o que a decisão 12 proibiu.

---

## 4. AS SAÍDAS, com o preço de cada uma

Dez saídas foram desenhadas e avaliadas. Quatro entram, quatro são recusadas
com motivo escrito, duas ficam **enterradas com data** para ninguém gastar leva
nelas de novo.

### S1. Remover a releitura (matar o NUMA-03 no caminho do daemon)

- **Código.** Tirar do tick o bloco que, sob autoridade `daemon`, chama
  `read_player_pattern` antes do skip por valor.
- **Custo.** Perde-se a detecção de escritor estrangeiro, que existe por um
  motivo real: a Steam pinta padrões como "player 1+3" no mesmo `sysfs`.
- **Ganho: praticamente nulo, e isso está MEDIDO.** A releitura custou **36
  microssegundos** entre o `external_led_written` e o `external_led_repintado`,
  e **zero** subcomando. Ela causou **uma** escrita em 19 horas.
- **VEREDITO: NÃO recomendo como cura.** É a saída mais óbvia e a que menos
  entrega. Ela mata um sintoma de diagnóstico, não um custo.

### S2. Detector que distingue pelo código de erro da própria escrita

- **VEREDITO: IMPOSSÍVEL pelo caminho `sysfs`, com prova.** O `write(2)` volta
  **antes de o erro existir** — 1,18 s a 3,45 s antes, medido. O erro só existe
  no log do kernel, num trabalho assíncrono, e o produto não tem como lê-lo sem
  virar monitor de journal.
- **Fica ENTERRADA COM DATA (07/08/2026).** Só existiria pelo caminho `hidraw`
  cru, que é a S6.

### S3. Detector que compara contra o que NÓS escrevemos *(correção de uma linha)*

- **Código.** No mesmo bloco do tick, trocar a comparação contra o `slot` **novo**
  pela comparação contra o **último valor escrito por nós** (`_last_value`).
- **Custo.** Zero. Uma linha.
- **Risco, e ele tem de ir para a docstring:** o detector continua **cego ao
  firmware**. Ele passa a enxergar só escrita de **outro processo** pelo mesmo
  `sysfs` — que é tudo o que ele sempre pôde enxergar. Escrita que morreu no
  rádio permanece invisível, **para sempre**. Hoje a docstring de
  `read_player_pattern` sugere o contrário, e isso é o que enganou a casa.
- **Ganho.** `external_led_repintado` volta a significar o que o nome diz. As 11
  ocorrências do lado A deixam de contaminar toda contagem futura.
- **VEREDITO: ENTRA**, junto com a S4. É correção de correção, não desenho novo.
- **O teste que morde** já tem meia casa em `tests/unit/test_external_identity.py`
  (bloco NUMA-03.4): falta o caso em que o padrão lido é igual ao **nosso
  último valor** e diferente do **slot novo** — hoje isso vira `intruso`, e não
  deveria.

### S4. Escrita DIFERENCIAL — só o nó cujo valor muda *(a cura de custo)*

- **Código.** Em `core/external_leds.py`, `write_player_number` e
  `write_lightbar_slot` leem cada `brightness` antes e escrevem **só** os que
  diferem.
- **Custo.** Uma leitura de `sysfs` por nó — memória do kernel, **zero** rádio.
- **Ganho, e é o único ganho grande da lista.** Hoje a chamada custa **cinco**
  subcomandos **sempre**, mesmo quando nada muda (referência canônica dos
  externos, 3.6, item 3, GRAU ALTA: escrever um nó verde reescreve os quatro, e
  o azul é subcomando separado). Com a diferencial: reescrever o **mesmo**
  número custa **zero**; passar de 1 para 2 custa **um**; o pior caso realista
  com quatro controles custa **dois**. Contra 19,3 recusas por escrita, é a
  diferença entre uma cascata de vários segundos e nada.
- **RISCO, e é o risco real desta saída — declarado:** como o `sysfs` guarda o
  **pedido** e não o **resultado** (seção 2.1), uma escrita que morreu no rádio
  fica **indistinguível** de uma que funcionou, e o escritor diferencial **nunca
  mais tenta**. A lâmpada fica errada até o aparelho reconectar. **Hoje, a
  reescrita cega é a única segunda chance que existe.**
- **MITIGAÇÃO, e ela é doutrina, não gambiarra:** reafirmar em **borda**, nunca
  em laço — instância HID nova (o aparelho voltou) e o gesto explícito
  "Renumerar agora". Uma borda por conexão custa cinco subcomandos **uma vez**,
  não 348 em dois dias.
- **VEREDITO: ENTRA.**

### S5. Tirar o azul da conta *(obrigatória, independente de tudo)*

- **Código.** O `blue:player-5` deixa de ser o bit "+5"; `write_player_number`
  capa em 4 e **não escreve o azul**; `read_player_pattern` acompanha bit a bit
  (a regra que a própria docstring dele já manda, e que existe para não abrir o
  laço da seção 2.6).
- **Custo.** Perde-se a distinção dos slots 5 a 9 no Pro. Com quatro controles
  na mesa isso **nunca é exercido**.
- **Ganho.** Menos **um** subcomando por chamada, sempre. E o produto para de
  escrever `1` num nó de escala 0-15 que é o **LED HOME** e usa outro
  subcomando. Paga a dívida 7.2, item 5, da referência canônica dos externos.
- **Não se apaga decisão medida:** a regra R-25 (o azul como "+5") **ganha nota
  datada**, não sumiço. Três testes travam hoje o comportamento antigo em
  `tests/unit/test_external_leds.py` e têm de mudar **junto**, com a nota.
- **VEREDITO: ENTRA.**

### S6. Escrever o subcomando `0x30` cru no `hidraw`

- **Ganho.** O mínimo teórico: **um** subcomando para as quatro lâmpadas.
- **RISCO: ALTO, e nomeado.** (i) sai de baixo do `joycon_enforce_subcmd_rate`,
  que é a proteção que existe **para o link não cair** — o comentário do próprio
  driver diz que transmitir sem ritmo derruba o Bluetooth; (ii) disputa o
  `packet_num` que o firmware usa para deduplicar; (iii) é a **armadilha 3 do
  `CLAUDE.md`** — instrumento brigando com o produto, imprimindo "aplicado" sem
  ter aplicado; (iv) a próxima escrita de `sysfs` do próprio kernel reescreve
  por cima.
- **VEREDITO: NÃO. Fica ENTERRADA COM DATA (07/08/2026).**

### S7. Subir o `LED_MIN_INTERVAL_SEC`

- **O diagnóstico primeiro:** o limite de 2,0 s **não segura nada**, por quatro
  razões independentes, e as quatro estão MEDIDAS. (a) ele é **igual** ao
  período do tick, e limite igual ao período de amostragem remove zero ticks;
  (b) uma cascata custa **5,4 s**, ou seja **2,7 vezes** o limite; (c) o daemon
  **carimba o relógio antes de escrever**, com o instante do início do tick, e a
  escrita volta em microssegundos — ele nunca sente o custo; (d) **a unidade
  está errada**: ele conta **chamadas**, e o rádio paga **subcomandos**, cinco
  por chamada, cada um com até quatro tentativas.
- **Código.** Subir para acima da cascata medida (ordem de 10 s) e documentar de
  onde saiu o número.
- **Custo.** O LED fica errado até o ciclo seguinte.
- **VEREDITO: complemento barato, NÃO é cura.** Sozinho não resolve: as escritas
  do lado A foram espaçadas de **63,6 minutos em média**, e o rate-limit quase
  nunca é o que segura. **Entra junto com a S4, não no lugar dela.**

### S8. Não escrever no Pro, escrever só no 8BitDo

- **Duas objeções, e a primeira é factual e medida agora:** **não há onde
  escrever no 8BitDo.** Ele **saiu do rádio** — `hcitool con` às 20h53 mostra
  **três** ACL, e nenhum é ele — e já estava sem instância HID desde cerca das
  19h33 (a terceira forma de zumbi da seção 1.2 da referência canônica dos
  externos). A assimetria entregaria **zero** na mesa de hoje.
- **A segunda é doutrina da casa, e tem sprint com nome:**
  [REGRA-NÃO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md)
  — *a cura tem de ser regra, não registro*.
- **VEREDITO: NÃO.**

### S9. Curar (c) — UMA SÓ CONTA *(a que entrega o que ela pediu)*

Nenhuma das oito acima faz o plástico dizer a verdade. Esta faz.

- **O defeito** está medido na DUAS CONTABILIDADES-01: o branco é o Jogador 1 do
  jogo e acende **4**; o roxo é o Jogador 2 e acende **1**.
- **Código — dois caminhos, e a escolha é desenho, logo é dela:** (1) a
  **exibição** passa a ler a conta do co-op quando o co-op está ativo (a lâmpada
  obedece ao jogo); ou (2) o **co-op** passa a eleger o primário pela fila
  persistida em vez de "o primeiro que entrou e ainda está presente" (o jogo
  obedece à fila).
- **Custo.** Mexe em `daemon/subsystems/identity.py` e
  `daemon/subsystems/coop.py` ao mesmo tempo. Não é mudança que esta casa
  entrega sem o olho dela.
- **Risco.** O caminho (2) muda quem é o Jogador 1 no meio da sessão, e a casa
  já mediu o preço de derrubar e recriar jogador —
  `tests/unit/test_vpad_anti_recreate.py` existe por isso.
- **E o que a torna a PRIMEIRA:** ela se mede **hoje**, com os dois DualSense,
  **sem tocar na luz dos externos**. **A decisão 12 não a bloqueia.** O teste que
  morde já tem meia casa em
  `tests/unit/test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py`; falta o
  caso de **dois** DualSense com o co-op ligado, que é literalmente a mesa dela.
- **VEREDITO: ENTRA, e vai na frente.**

### S10. Parar a renumeração-churn — prender o número ao lugar persistido

- **O que é.** As escritas do lado A não vinham de laço: vinham de
  **renumeração**, e a renumeração vinha do `_connected` que dança (D2). Prender
  o número **exibido** ao lugar persistido, recompactando só no gesto explícito
  "Renumerar agora", derrubaria as escritas para **uma por conexão**.
- **Custo.** **Buracos na numeração** quando alguém desliga o controle. É
  exatamente a troca que ela já discutiu na resposta 1 da DUAS CONTABILIDADES-01,
  e sobre a qual a casa registrou *"é dela a palavra"*.
- **VEREDITO: não é engenharia, é DESENHO. Vai para a PERGUNTA, não para a
  leva.**
- **A cura parcial que É engenharia** já está desenhada desde 03/08 e não
  depende dela: separar os eixos no provider de cor, para que **ler cor não
  marque presença** (a B4 da QUATRO-NO-RÁDIO-01). Isso não muda a política de
  numeração; só para de **fabricar** oscilação de presença a 10 Hz.

---

## 5. A ORDEM QUE ISSO IMPÕE

> ## NENHUMA CURA DE LUZ ENTRA ANTES DA CURA DA NUMERAÇÃO
>
> **A ordem é: S9 (o número certo) → S3 + S4 + S5 + S7 (a escrita barata e
> honesta) → a PERGUNTA que é dela.**
>
> **E não é preferência de estilo. São três razões, e as três estão medidas:**
>
> 1. **Curar a escrita antes do número é preparar o cano para devolver o número
>    ERRADO com mais confiança e mais barato.** Hoje o produto acende 4 no
>    plástico que o jogo chama de Jogador 1. Uma escrita idempotente e verificada
>    faria isso de forma mais eficiente, mais estável e mais convincente.
> 2. **Curar o DETECTOR sem curar a ESCRITA liga o laço infinito que hoje não
>    existe.** A cegueira do `read_player_pattern` é o que faz a repintura
>    terminar (seção 2.3). Um detector honesto, sobre uma escrita que ainda custa
>    cinco subcomandos e falha no meio, repinta a cada 2 s, para sempre.
> 3. **S9 é a única que não custa NADA à decisão 12.** Ela se mede e se prova
>    com os dois DualSense, com a luz dos externos calada, hoje, na mesa dela.
>
> **E a honestidade que fecha a ordem: nenhuma destas saídas reacende coisa
> alguma.** Elas fazem o número ficar certo e a escrita ficar barata **enquanto a
> luz continua calada**. No dia em que ela mandar reacender, o cano estará
> pronto. Até lá, o plástico não muda um lúmen.

**As três exigências que a `E3` herda, e nenhuma existe hoje.** GRAU: SUSPEITA
COM MECANISMO (derivação direta dos achados; nenhuma foi executada nem medida):

1. **um número ESTÁVEL para escrever** — enquanto `_connected` tiver dois
   escritores, o valor a pintar oscila sozinho;
2. **uma escrita que saiba se falhou** — hoje o `or escreveu` declara sucesso
   com uma lâmpada de cinco, e o cache grava como se tudo tivesse ido;
3. **um limite cuja unidade seja o SUBCOMANDO**, não a chamada, e cujo valor
   seja maior que o custo medido de uma repintura.

---

## 6. O PROTOCOLO que decide entre as saídas — **CURA-A/B-01**

Convenção da casa: **P0** tranca (com o destrancar embutido); **ANTES** é a foto
numérica; **CONTRASTE** é o caso sem o qual nada se conclui; **PREVISÃO** é
falsificável e derivada do código; **LEITURA** é a tabela escrita **antes** de
medir.

O A/B natural (luz falando contra luz calada) **já aconteceu** e é o E-1 do
estudo dos externos. **Falta o A/B da CURA:** a escrita diferencial custa mesmo
zero subcomando quando nada muda?

**E o desenho é o achado:** o padrão que está no plástico agora
(`1,1,0,0` + azul `0`) **é exatamente o que o slot pediria**. Então os dois
primeiros braços escrevem **o que já está lá** — nenhuma lâmpada muda, nada novo
é afirmado, e **a decisão 12 fica intacta**. A medição inteira acontece **sem
que a tela dela mude e sem que o plástico mude**.

### P0 — trancar

1. **Não reiniciar o daemon.** O de 15:27:48 é o lado B e o cronômetro dele
   vale (`NRestarts=0`, MEDIDO). Reiniciar não invalida nada, mas zera 5h25m.
2. **O portão continua `False`.** A medição **não passa pelo produto**: é
   bancada, chamando `write_player_number` da árvore diretamente. O produto
   segue calado.
3. **Suíte parada** — ela suja o journal, e este protocolo lê o journal
   (SUITE-QUE-SUJA-O-JORNAL-01, e a nota de instrumento 9 do estudo dos
   externos).
4. **Anotar o denominador do rádio**, porque ele mudou: quantos ACL (**três**
   agora), `Discovering`/`Discoverable`, e se a tela de Bluetooth do COSMIC está
   aberta. Sem isso a rodada não é comparável com nenhuma anterior.
5. **Destrancar:** os braços 1 e 2 não mudam nada — o padrão escrito é o que já
   estava. O braço 3, se rodar, termina devolvendo `1,1,0,0`. Conferir os cinco
   nós no fim.

### ANTES — a foto numérica (MEDIDA em 07/08/2026 às 20h53)

| métrica | valor |
|---|---|
| nós do Pro | `player-1=1, player-2=1, player-3=0, player-4=0, blue=0`; padrão lido = **2** |
| storm de hoje | **202** recusas, **49** `-110`; **última linha às 15:24:04.932358** |
| storm desde 06/08 | **348** recusas, **83** `-110` |
| lado B | **5h25m**, com **0** escritas, **0** repinturas, **0** recusas, **0** `-110` |
| Pro | instância `.0017` desde 06/08 22:21:11 — **22h32m** de link ininterrupto |
| rádio | **três** ACL: Pro `E0:F6:B5:00:00:53`, DualSense `14:3a:9a:00:00:ab`, DualSense `a0:fa:9c:00:00:f0`. O 8BitDo `e4:17:d8:00:00:83` **fora** |

### Braço 1 — a escrita de hoje, com o valor que já está lá

`write_player_number(inst, 2)` **como está na árvore**: cinco escritas de
`sysfs`, todas com o valor que o nó já tem.

- **PREVISÃO** (ALTA pelo código, MEDIDO pelo episódio de 15:24:01): cinco
  subcomandos ao rádio; ordem de **12 a 20** recusas e até **5** `-110`, numa
  cascata de **3,4 a 5,4 s** que começa cerca de **350 ms** depois de o `write()`
  voltar.
- **O QUE A DERRUBA:** **zero** recusas. Aí o kernel **não** reemite subcomando
  para valor igual, o custo é só por lâmpada **mudada**, e a economia da S4 é
  muito menor que a estimada — **o alvo passa a ser a S10**, que é pergunta para
  ela, e não a escrita.

### Braço 2 — a cura

`write_player_number` diferencial: lê os cinco nós e, como **nenhum** difere,
escreve **zero**.

- **PREVISÃO:** zero escrita, zero subcomando, zero recusa. **Determinístico**,
  não estatístico.
- **O QUE A DERRUBA:** **qualquer** recusa nesta janela. Aí existe **segundo
  escritor** — e essa é a linha mais grave possível, porque a referência
  canônica dos externos (3.7) já nomeou o mecanismo: **qualquer jogo ou a
  Steam, via `ff_memless`, produz as mesmas linhas de `exceeded max attempts`
  sem nenhuma escrita nossa no journal**. O E-1 concluiu "não há segundo
  escritor **nesta janela**"; a janela dele não tinha jogo com rumble no Pro.

### Braço 3 — o custo de uma mudança de verdade *(SÓ com o sim dela)*

De `1,1,0,0` para `1,1,1,0` (padrão 2 para 3) e de volta.

- **PREVISÃO:** **um** subcomando por sentido; recusas na ordem de 2 a 4, e
  **provavelmente zero** `-110`, porque o limitador tem as 25 tentativas
  inteiras para **um** envio, em vez de cinco disputando o `output_mutex`.
- **O QUE A DERRUBA:** 12 recusas para uma lâmpada só. Aí o custo **não** é por
  subcomando, e a hipótese inteira cai — remedir antes de mexer em código.
- **ATENÇÃO:** este braço **acende uma lâmpada nova por alguns segundos**. É
  escrita que muda o plástico, e a decisão 12 diz zero escritas. **Ele só roda
  com ela dizendo sim, e devolve o padrão no fim.** Se ela disser não, **os
  braços 1 e 2 bastam** para decidir entre as saídas — o braço 3 só refina o
  número.

### CONTRASTE

Os **dois DualSense** na mesma janela: eles não passam pelo `hid-nintendo` e não
recebem subcomando nenhum. Se a taxa de instâncias novas deles mudar junto, foi
o rádio, e a rodada não diz nada. E o contraste temporal está de graça:
**5h25m de lado B com zero** — qualquer recusa que apareça é atribuível ao
braço, não ao ambiente.

### LEITURA — a tabela, escrita ANTES de medir

| desfecho | leitura | consequência |
|---|---|---|
| braço 1 com ordem de 12 a 20 recusas, braço 2 com zero | a escrita **redundante** É o custo | **S4 é a cura**; S3+S4+S5+S7 entram na leva, **depois da S9** |
| braço 1 com zero recusas | o kernel não reemite para valor igual | o custo é só por lâmpada mudada; **o alvo vira a S10**, que é pergunta para ela |
| **qualquer** recusa no braço 2 | **segundo escritor** na mesa | achado maior que o defeito original; o alvo muda inteiro, e a S6 fica ainda mais proibida |
| braço 3 com 12 recusas | o custo não é por subcomando | a hipótese cai; remedir antes de mexer em código |
| **o Pro cai em qualquer braço** | 22h32m de link perdidas | **PARAR.** E a refutação *"o storm não derruba o Pro"* do E-1 — medida com dois a três links — deixa de valer para a mesa de quatro |
| o DualSense muda de taxa junto | o contraste falhou | queda geral de rádio; **descartar a rodada** |

### Divisão de trabalho

- **ELA:** nada nos braços 1 e 2. No braço 3, **só o sim** — o gesto é do
  assistente, não dela.
- **ASSISTENTE:** conta pelo **kernel**, com data completa em toda janela, nunca
  pelo daemon. É a armadilha que já inventou resultado nesta casa.

### O que este protocolo NÃO decide

Ele decide **(b)**. **Não decide (c)**, e não pode: (c) fecha com a S9 e com o
olho dela, no protocolo da DUAS CONTABILIDADES-01 — apertar um botão no plástico
branco e conferir que quem se mexe é o Jogador 1 **enquanto o branco acende 4**.

---

## 7. A PERGUNTA QUE É DELA — pronta para ser feita

A decisão 12 é *"calar a luz **até a entrega existir**"*. **Nenhuma saída deste
documento reacende nada**, e a sprint não pede que ela mude de ideia. O que a
sprint faz é pôr na mesa **uma etapa intermediária que não existia quando ela
decidiu**, porque a medição de hoje a tornou possível.

> ### A pergunta
>
> **Ela mantém a decisão 12 inteira — luz calada em todos, até a `E3` existir —
> ou aceita uma etapa intermediária, em que a luz volta SÓ nos DualSense (que
> não têm este defeito) enquanto os externos seguem calados?**

### O preço de cada caminho, sem escolher por ela

**Caminho 1 — manter a decisão 12 inteira.**

| | |
|---|---|
| **o que ela ganha** | coerência total: o produto não afirma jogador em ninguém que não seja jogador de verdade. Zero risco de storm. Zero afirmação nova. |
| **o que ela perde** | continua **sem o instrumento** pelo qual distingue os controles, nos quatro. E o Pro e o 8BitDo seguem com **resíduo congelado** no plástico — o Pro está com dois verdes acesos desde 15:24:01 de 07/08, que é a nossa última escrita, não uma escolha. |
| **o custo escondido** | **não existe estado "sem número" no Pro** (referência canônica dos externos, 3.6): o que fica aceso é o padrão do kernel ou o nosso resíduo. Calar não apaga — e apagar seria afirmar. |

**Caminho 2 — a luz volta só nos DualSense.**

| | |
|---|---|
| **o que ela ganha** | recupera o instrumento **onde ele nunca esteve em disputa**: a luz dos DualSense **nunca foi calada** pela decisão 12, e eles **não têm** nenhum dos quatro defeitos desta sprint (não passam pelo `hid-nintendo`, não têm limitador de subcomando, não têm o detector cego). |
| **o que ela perde** | **nada de coerência com a decisão 12** — ela nunca falou dos DualSense. Mas **ganha uma assimetria visível**: dois controles numerados e dois apagados, na mesma mesa. |
| **o custo REAL, e é este que decide** | **hoje esse número está ERRADO**, e está medido: o branco é o Jogador 1 do jogo e acende **4**; o roxo é o Jogador 2 e acende **1**. **Voltar a luz nos DualSense antes da S9 é acender, com confiança, o número trocado.** |
| **a condição que torna o caminho 2 honesto** | a **S9 primeiro**. Com uma só conta, a luz dos DualSense passa a dizer a verdade, e a etapa intermediária deixa de ser uma afirmação falsa. |

**A terceira forma, que existe e tem de estar na mesa:** a luz volta nos
externos **significando outra coisa** — não *"o seu jogador no jogo"*, mas *"o
seu lugar na mesa do Hefesto"*. **Preço:** é uma afirmação **nova**, e é
exatamente o tipo de afirmação que a decisão 12 recusou. **Só ela pode dizer se
o significado novo é honesto.**

**Eu não escolho nenhuma das três.** O que a leva pode entregar sem ela é o
cano: **número certo (S9)** e **escrita barata e honesta (S3+S4+S5+S7)**, com a
luz calada o tempo todo.

---

## 8. O que fica ABERTO

1. **Duas notas datadas ficam DEVENDO, e não foram escritas aqui** — esta sprint
   escreve **um** arquivo, e a casa não edita documento que outra mão pode estar
   segurando:
   - na seção 4.2 do
     [estudo dos externos de 07/08](../estudos/2026-08-07-ISOLAR-os-externos-o-metodo-da-lightbar-no-pro-e-no-8bitdo.md):
     os passos **2, 3 e 5** do mecanismo caducaram (seção 2.2 desta página). O
     **desfecho** daquela seção continua de pé;
   - onde estiver documentado o significado de `external_led_repintado`: ele
     **não** significa escritor estrangeiro. Significou **a nossa própria
     escrita anterior** em 11 de 11 ocorrências.
2. **A causa do `intruso=0` de 07/08 01:56:53 NÃO foi identificada.** O padrão
   foi a zero sem que houvesse suspend/resume no journal na janela 01h50-02h05.
   **SEM PROVA.** Não se inventa a causa.
3. **A QUATRO-NA-MESA-01 (defeito 1) e a QUATRO-NO-RÁDIO-01 (B4, B5) continuam
   ABERTAS desde 03/08** — e são a raiz medida disto tudo. Esta sprint não as
   fecha; **aponta que o preço delas subiu** de "o número dança na tela" para
   "348 recusas de firmware".
4. **A refutação do E-1 (*"o storm não derruba o Pro"*) NÃO atravessa para a
   mesa de quatro links.** Foi medida com dois a três, e a referência canônica
   dos externos (3.5) registra a perda de IMU do Pro subindo de dezenas para
   **439** episódios por dez minutos no minuto em que a mesa foi a quatro.
   GRAU: MEDIDO para os números; **SUSPEITA COM MECANISMO** para a consequência.
5. **A previsão de 24 h do E-1 continua não cumprida:** são **5h25m** de lado B.
   Recontar custa zero e a régua é a mesma.
6. **A P-4 da referência canônica dos externos segue aberta** — ninguém nunca
   olhou se o 8BitDo tem lâmpada colorida física. **Cinco segundos de olho
   dela**, e o desfecho muda o valor de metade da `E3`.

   > **NOTA DATADA — 07/08/2026 21h06: ela olhou, e esta metade FECHOU.** Nas
   > palavras dela: *"não há lightbar mas existe led de identificação de player
   > nele também, igual o pro controller"*. **Não há lâmpada colorida física**,
   > logo o caminho `ds4` de LED externo escreve cor em nó que não acende cor —
   > e a metade da `E3` que dependia disso está decidida. GRAU: MEDIDO (o olho
   > dela no plástico).
   >
   > **O que sobra da `P-4`** é quem acende as quatro luzes de jogador que o
   > plástico tem: o firmware traduzindo a cor que escrevemos, ou o aparelho por
   > conta própria. **GRAU: SEM PROVA.** É a **resposta 23** dela — *"preparar,
   > e rodar quando ele estiver ligado"* —, e a pergunta reescrita está na seção
   > 8.4 de
   > [os externos, a referência canônica](../../protocol/externos-referencia-canonica.md).
7. **O 8BitDo saiu do rádio e continua sem HID** — a terceira forma de zumbi da
   seção 1.2 da referência canônica dos externos, que **não tem cura em lugar
   nenhum** e sobre a qual a vigia de `scripts/bt_health_watchdog.sh` não diz uma
   palavra. Não é desta sprint, mas **muda a mesa** em que qualquer medição de
   externo acontece.
8. **A EXT-04 não existe como documento.** O rótulo aparece em docstrings de
   `src/` e de `tests/`, e a medição original dele **não sobreviveu em lugar
   nenhum**. O que se sabe está na docstring de `daemon/ipc_handlers.py`: *"esta
   função NUNCA MAIS escreve LED (a escrita a cada poll de 4s da GUI bombardeava
   o firmware clone do 8BitDo até o `hid-nintendo` desregistrá-lo)"*. **Fica
   registrado que é um IRMÃO, não o mesmo defeito:** aquele era escrita **demais
   por frequência** (poll de 4 s) num aparelho que **morria**; este é escrita
   **rara com o número instável** num aparelho que **não morre** — o Pro
   atravessou as 348 recusas com o link de pé por 22h32m. Mesmo território, causas
   distintas. GRAU: SUSPEITA COM MECANISMO (as docstrings não trazem a medição
   original).
9. **O terceiro laço, latente, não foi exercido** (seção 2.6): hardware sem a
   quinta lâmpada em slot 5 ou maior repinta para sempre. Não ocorreu porque o
   Pro dela **tem** o nó azul. A S5 o fecha de passagem.
10. **Nada nesta sprint foi executado.** É diagnóstico. A árvore não foi tocada,
    nenhuma escrita foi feita em `hidraw`, nenhum serviço foi reiniciado, nenhum
    controle foi derrubado, e o arquivo de configuração dela não foi lido nem
    escrito.
