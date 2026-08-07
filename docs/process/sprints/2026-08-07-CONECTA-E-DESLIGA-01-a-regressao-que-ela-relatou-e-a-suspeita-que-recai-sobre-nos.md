# CONECTA-E-DESLIGA-01 — a regressão que ela relatou, e a suspeita que recai sobre nós

- **Achado em:** 07/08/2026, **por relato dela**, com os quatro controles na mesa
- **Estado:** **REGISTRADA, NÃO CURADA.** Ela pediu para esperar os trabalhos em
  voo terminarem antes de mexer — e a decisão está respeitada
- **Gravidade:** **ALTA** — atinge o uso dela agora, e a suspeita principal recai
  sobre uma cura **nossa**, de ontem
- **Causa-raiz:** **SUSPEITA COM MECANISMO.** O caminho fecha; o gatilho não foi
  reproduzido
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
    — é a sprint que **mandou** o `JustWorksRepairing=confirm`, e que **previu
    por escrito** este efeito colateral;
  - [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
    — o aviso do doctor sobre o agente morto nasceu exatamente deste risco.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal ou teste que reprova; **SUSPEITA COM MECANISMO** = o caminho de código
foi lido e fecha, o efeito não foi observado; **SEM PROVA** = está dito e
ninguém verificou.

---

## O relato dela, palavra por palavra

07/08/2026, à noite:

> *"o 8 bitdo voltou a conectar automaticamente na tela de bt ao invés de eu
> clicar lá. quando rola essa regressão ele conecta e desliga em sequencia. Não
> sei se foi por teste dos agentes, vamos esperar eles concluírem primeiro mas
> não posso esquecer de falar isso"*

Três coisas nessa frase, e as três importam:

1. **"voltou a"** — é regressão, não novidade. Ela já viu isto antes.
2. **"conecta e desliga em sequência"** — o sintoma tem forma, e a forma é cíclica.
3. **"não sei se foi por teste dos agentes"** — a desconfiança é legítima, e a
   primeira coisa que este documento faz é responder a ela.

---

## NÃO foram os agentes de hoje — e isso está medido

**Grau: MEDIDO.**

| conferência | resultado |
|---|---|
| escrita em `/etc/bluetooth` ou `/etc/udev/rules.d` hoje | **nada** (`find -newermt` vazio) |
| arquivos de BT tocados nos commits de hoje | só documentação e **um** teste |
| código de produto de Bluetooth alterado hoje | **nenhum** |
| serviço de BT reiniciado por agente | **nenhum** |

Os agentes de hoje trabalharam com **leitura pura** no que toca o rádio, e a
instrução estava escrita em cada prompt. A árvore confirma.

---

## A suspeita que sobra, e ela é sobre uma cura NOSSA

**Grau: SUSPEITA COM MECANISMO.**

O que mudou na máquina dela, e chegou **ontem**:

```
/etc/bluetooth/main.conf  ->  JustWorksRepairing=confirm
```

Isso entrou pela [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md),
é uma cura de **segurança** — fecha uma janela em que qualquer aparelho podia
re-parear sem autenticação — e o commit que a levou à máquina foi o `53f6d8b`,
de 06/08 às 22h02.

**E a própria sprint previu o preço, por escrito:** com `confirm`, o
re-pareamento passa a **depender de um agente registrado**. Sem agente que
responda, o BlueZ **recusa** — e a recusa aparece no journal exatamente assim:

```
profiles/input/server.c:confirm_event_cb() Refusing connection from <endereço>
```

**Medido no journal dela, hoje:**

| aparelho | recusas hoje |
|---|---|
| DualSense roxo | 2 |
| 8BitDo | 1 |

E o 8BitDo registrou **quatro** conexões no dia — o que é compatível com o
"conecta e desliga em sequência" que ela descreve.

### Por que isto ainda é SUSPEITA, e não MEDIDO

O agente está **vivo** (`hefesto-bt-agent.service`, escopo de sistema, `active`)
e o `AgentManager1` responde no D-Bus. Se o agente está de pé, a recusa não
deveria acontecer — **e acontece**.

Isso deixa três possibilidades, e nenhuma foi fechada:

1. o agente está vivo mas **não registrado** para o tipo de capacidade que o
   `confirm` exige;
2. o agente responde, mas **depois** do prazo do BlueZ;
3. a recusa vem de outro caminho (`connect_event_cb` com `No such device`
   aparece **antes** das confirmações, e pode ser a causa e não a consequência).

**Nenhuma das três foi medida.** Escolher uma agora seria o erro que esta casa
já pagou caro: hipótese que explica o sintoma mas não explica o que **já
funcionava**.

---

## O que NÃO explica, e por isso não pode ser a resposta fácil

- **Não é bateria.** Ela disse que o 8BitDo caiu **no carregador**, hoje mais
  cedo. Isso mata a hipótese mais confortável.
- **Não é o storm de USB.** Este é rádio; o storm é cabo, e a última ocorrência
  foi 04/08 (ver o estudo do dia).
- **Não é a luz.** O bombardeio de LED que matava o Pro está em **zero** desde
  as 15h27 de hoje.

---

## O protocolo — e ele custa cinco minutos dela

**Não execute sem ela**: mexer no agente de pareamento com quatro controles
conectados pode derrubar os quatro.

**P0 — trancar o cenário.** Anotar quais controles estão conectados e o horário.

**ANTES.** Com o 8BitDo desligado:

```
systemctl is-active hefesto-bt-agent.service
busctl call org.bluez /org/bluez org.bluez.AgentManager1 ...   (ler o agente registrado)
journalctl -u bluetooth -f    (deixar rodando)
```

**O GESTO.** Ela liga o 8BitDo e **não toca na tela de Bluetooth**.

**CONTRASTE.** Repetir com `JustWorksRepairing` temporariamente em `always`
(o valor antigo), **com o rádio dela em casa e sem ninguém por perto** — porque
`always` é justamente a janela que a `RADIO-ABERTO-01` fechou, e reabri-la tem
custo de segurança real, ainda que por dois minutos.

**PREVISÃO.** Se a recusa sumir com `always` e voltar com `confirm`, a causa é
nossa e a cura de segurança precisa de um acompanhante — não de ser desfeita.
Se a recusa continuar nos dois, a causa é outra e a `RADIO-ABERTO-01` está
inocente.

---

## NOTA DATADA — 07/08/2026, 20h: uma causa, quatro sintomas

**Grau: MEDIDO** na correlação, **SUSPEITA COM MECANISMO** na cadeia.

Uma hora de medição por minuto, com instrumento **validado contra contagem
direta** (53 = 53), mudou o quadro inteiro. A tabela:

| janela | estado do rádio | perda de IMU do Pro |
|---|---|---|
| 19h10 a 19h43 | quatro controles **estáveis** | **14,6** por minuto |
| 19h44 a 19h53 | o 8BitDo **saindo e tentando voltar** | **48,4** por minuto |

E no meio da segunda janela, o `bluetoothd`:

```
19:48:21  confirm_event_cb() Refusing connection from <8BitDo>
19:49:03  search_cb() <8BitDo>: error updating services: Connection refused
20:00:18  confirm_event_cb() Refusing connection from <8BitDo>
```

### A hipótese que isso monta, e ela liga tudo

**Não é a quantidade de aparelhos — é o aparelho que não consegue entrar.**
O ciclo de tentativa (busca de página, consulta de serviços, recusa, repetir)
consome o canal, e quem paga é o vizinho que está usando o rádio de verdade.

Isso explica, com **um** mecanismo, quatro coisas que pareciam separadas:

1. **o que ela vê** — *"conecta e desliga em sequência"*: é o ciclo, visto de fora;
2. **o estado fantasma** — `Connected=true` com zero aparelhos HID: é o meio do
   ciclo, quando o rádio subiu e o perfil de entrada não;
3. **a perda de pacotes do Pro** — sobe 3,3 vezes durante o ciclo e cai quando
   ele para;
4. **a recusa no journal** — o `Refusing connection from`, que é o motivo do
   ciclo não terminar.

### O que isto NÃO fecha

Por que a confirmação é recusada **com o agente vivo**. Essa continua sendo a
pergunta central, e as três hipóteses da seção anterior seguem de pé.

E derruba a leitura anterior deste mesmo dia: eu havia dito, ao vivo, que três
controles custavam 40 perdas por minuto e dois custavam zero. **Aquilo veio de
um medidor quebrado** — ele formatava a data em português e o `journalctl` não
entende `ago`, então devolvia zero sempre. A correlação com a **quantidade**
está derrubada; a correlação com a **instabilidade** é que se sustenta.

## O que fica ABERTO

1. **A causa.** Três hipóteses vivas, nenhuma medida (acima).
2. **Se a `RADIO-ABERTO-01` cobra um preço que ninguém aceitou.** A sprint
   previu o efeito e o registrou como risco; ninguém perguntou a ela se o preço
   era aceitável. Se for este o caso, a pergunta é dela e vem antes da cura.
3. **O aviso do doctor não bastou.** Ele avisa quando o agente está *morto*.
   Aqui o agente está **vivo** e a recusa acontece assim mesmo — logo o critério
   do aviso está incompleto, e isso é um defeito do diagnóstico, não só do rádio.
