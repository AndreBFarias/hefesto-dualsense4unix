# PROTOCOLO — as medições que decidem a leva

- **Escrito em:** 03/08/2026, para ela executar **de uma vez**, no ritmo dela
- **Por que existe:** o método que achou o `0x08` da lightbar em minutos, depois
  de duas sprints erradas, tem forma: **isolar um suspeito por vez, com controle
  positivo e negativo, e a confirmação dela em cada passo**
- **Como usar:** faça na ordem, anote a resposta de cada item (uma palavra
  basta), e me mande tudo junto no fim
- **Regra:** se um item não puder ser feito, **diga "pulei"** — item pulado é
  dado; item respondido no chute contamina tudo o que vem depois

---

## O MÉTODO (por que a ordem importa)

Cada bloco tem:

- **o controle positivo** — algo que **deve** funcionar. Se ele falhar, o
  problema é do instrumento, não do produto, e o resto do bloco não vale;
- **o suspeito isolado** — uma variável por vez;
- **o que observar** — em português do que se vê, não do que se supõe.

> **A armadilha que já custou tempo nesta casa:** medir **fora da janela**.
> Quatro suspeitos foram inocentados por engano em 03/08 porque o controle
> estava conectado havia minutos. **Quando o item disser "recém-conectado",
> isso é parte do teste.**

---

## BLOCO A — o que ficou pendente da noite (5 min)

### A1. O rumble para quando o controle sai? *(BORDA-DE-QUEDA-01)*

1. dois DualSense no Bluetooth, um jogo vibrando (ou me peça o rumble por IPC);
2. **desligue** o Controle 2 no meio da vibração (segure PS ~10 s).

**Observar:** o motor dele **para na hora**, ou continua vibrando ~3 s?

> `continua ~3 s` confirma que o rumble fica preso na borda de queda e que só o
> teto de silêncio o corta.

### A2. O LED do microfone acende e FICA? *(LED-SEM-DONO-01 — o aceite "antes")*

1. daemon **ligado**, controle no Bluetooth;
2. aperte o **botão do microfone** do controle;
3. **conte até três** olhando o LED.

**Observar:** o LED **acende e apaga sozinho** em menos de um segundo, ou
**fica aceso**?

> `acende e apaga` é o defeito: nós reescrevemos o LED apagado a cada 0,5 s.
> **Esta é a medição "antes"** — é ela que vai provar a cura depois.

---

## BLOCO B — o 8BitDo por Bluetooth (10 min)

**O que se quer saber:** ele sobrevive por rádio, e em que modo.

### B1. O combo — qual você usa?

A documentação da casa registra **`X+Start`** para DirectInput/PS4 e
**`Y+Start`** para Switch, *"segundo o manual da 8BitDo"* — mas **não** está
medido nesta máquina.

**Responda:** qual combo você usa para o modo PS4? *(se não souber, diga — não
se inventa gesto físico)*

### B2. Conectar em modo PS4 por Bluetooth

1. desligue o 8BitDo e **tire do cabo**;
2. ligue no modo **PS4/DirectInput**;
3. conecte por Bluetooth;
4. **espere 5 minutos** com os outros controles ligados.

**Observar:**
- ele aparece na tela de Bluetooth com que nome?
- **caiu** nesses 5 minutos? Se caiu, **quanto tempo durou**?
- ao cair, **levou outro controle junto**?

### B3. O controle negativo — o modo Switch

**Só faça se estiver disposta a perder o pareamento** (o modo Switch por BT está
**provado instável** nesta casa, e é o que derruba).

1. mesmo procedimento, no modo Switch;
2. observe por 2 minutos.

**Observar:** cai mais rápido que no PS4? Leva o Pro junto?

> Este é o **controle negativo** do bloco: se o PS4 sobrevive e o Switch não,
> está confirmado que a via boa é o `X+Start`, e o produto pode **avisar**.

---

## BLOCO C — o Pro Controller por Bluetooth (5 min)

### C1. Ele sobrevive sozinho?

Pro Controller no Bluetooth, **sem** o 8BitDo, com os dois DualSense.

**Observar:** cai em 5 minutos? Quanto dura?

### C2. Ele cai junto com o 8BitDo?

Agora com os dois externos no rádio ao mesmo tempo.

**Observar:** quando um cai, o outro cai junto? **Qual cai primeiro?**

> A memória da casa registra que o `bluetoothd` **crasha e come pareamentos**
> quando dois Nintendo-class reconectam em poucos segundos — o Pro genuíno e o
> 8BitDo em modo Switch se apresentam com **a mesma identidade**. Este bloco
> testa exatamente isso.

---

## BLOCO D — os quatro no rádio (10 min)

**O que se quer saber:** a mesa que você quer, medida.

1. os **quatro** controles por Bluetooth ao mesmo tempo (8BitDo em modo PS4);
2. **abra um jogo** — qualquer um que aceite quatro;
3. jogue 5 minutos.

**Observar:**
- o jogo enxerga **quantos** controles?
- os números batem com o que a janela do Hefesto mostra?
- **algum caiu?** Qual, e em quanto tempo?
- a numeração **mudou sozinha** durante a partida?
- os dois DualSense têm **luz, vibração e gatilho** dentro do jogo?

---

## BLOCO E — o áudio do DualSense (10 min)

**Atenção:** o microfone por BT hoje precisa de um comando meu para destravar. Se
quiser medir sozinha, me avise que eu subo a ponte antes.

### E1. O alto-falante, no CABO (o controle positivo)

1. um DualSense **no cabo**;
2. na aba Status, mova o volume do **Alto-falante** e clique em **"Sons do jogo"**;
3. toque qualquer som.

**Observar:** sai som **no alto-falante do controle**?

> É o controle positivo do bloco. Se não sair **no cabo**, o problema não é do
> Bluetooth.

### E2. O alto-falante, no Bluetooth

Mesmo procedimento, com o controle no rádio.

**Observar:** sai som?

> **Previsão da casa:** não sai — a ponte de saída de áudio por BT **não está
> implementada** (`BLOCO_SPEAKER` declarado e sem uso). Se **sair**, a previsão
> está errada e isso é achado grande.

### E3. O microfone, no cabo (controle positivo)

Grave sua voz pelo microfone do controle **no cabo** (qualquer gravador).

**Observar:** capta?

### E4. O microfone, no Bluetooth

Me peça a ponte (`mic bt`) e grave falando.

**Observar:** capta? *(medido em 03/08: capta, depois de `mic unmute`)*

---

## O QUE EU FAÇO ENQUANTO VOCÊ MEDE

Sem depender de você, e sem tocar no que está medindo:

1. **terminar a onda 2** — a cura do `IGNORE` por cobertura está escrita e
   testada (14 verdes, e reprova com a cura arrancada); falta rodar a suíte
   inteira;
2. **a onda 3.2** — o `COOP-QUE-NÃO-DESMONTA-01`, que é o Jogador 2 que dura
   dois segundos. É o gargalo dos quatro no rádio, e é código;
3. **a bancada dos quatro controles** — o enumerador com roteiro de queda, que
   três sprints precisam.

---

## O que JÁ FOI MEDIDO (não repetir)

*Atualizado em 04/08/2026, madrugada.*

| medição | resultado | consequência |
|---|---|---|
| **"Desligar" desfaz "Rígido"?** | **SOLTOU** (03/08) | **refuta** a suspeita da `ENTREGA-QUE-NÃO-LIGOU-01`/E2 |
| o rádio emudece com o controle parado? | **não** — ~300 Hz | refuta a `BT-SURDO-01` |
| a lightbar por BT obedece? | **sim**, depois da cura | o `0x08` era a causa |
| o mic por BT capta? | **sim**, depois de `mic unmute` | falta o ciclo de vida |
| gatilho e rumble por BT? | **sim**, os dois | paridade confirmada |
| **A1** — o rumble para quando o controle sai? | **NÃO** — *"desliga sozinho e o controle branco segue vibrando"* | **confirma** a `BORDA-DE-QUEDA-01` |
| **B1** — o combo do modo PS4 | **`Start + A`** nesta máquina | a doc dizia `X+Start`; **corrigida** em 03/08 |
| **B2** — 8BitDo em modo PS4 por BT | conecta; **entra como Jogador 1**, igual ao DualSense do cabo | alimenta `QUATRO-NA-MESA-01` e `IDENTIDADE-DUPLA-01` |
| **D** (parcial) — os 4 conectados ao mesmo tempo | **conectaram**, estáveis por minutos; caem em cascata quando um sai | alimenta `RADIO-BOMBARDEADO-01` |
| o `bluetoothd` cai sozinho? | **sim, 2x em meia hora** (corrupção de heap, 5.86) | bug upstream; `RestartSec=1` e `TimeoutStopSec=3s` curados em 04/08 |
| frames L2CAP corrompidos com 3 controles no rádio | **44.718 em 28 min** (~26/s); **zero** com o rádio vazio | `RADIO-BOMBARDEADO-01` |
| o cabo no mesmo barramento do dongle causa isso? | **NÃO** — janela com cabo dentro deu **zero** | hipótese **refutada** por medição |
| o 8BitDo tem quantas identidades BT? | **duas** (`…1c:66:1a` e `…1c:99:83`), ocupando 2 lugares na fila | `IDENTIDADE-DUPLA-01` |
| o mic do DualSense funciona? | **sim** — o defeito era a interface e o mute persistido | curado em 04/08 |
| o medidor de mic da aba Status funciona? | **sim**, depois da cura | confirmado por ela em 04/08 |
| o alto-falante do controle estava mudo no PipeWire? | **sim**, e era o sink **padrão** do sistema | `SOM-SAIDA-MUDA-01`, curado |
| o drop-in 51 do WirePlumber estava armado? | **NÃO** — ausente até o `doctor --fix` de 00:37 | `DROPIN-AMBIGUO-01` |
| o daemon desliga limpo quando um controle some do rádio? | **NÃO** — 90 s e SIGKILL | `QUEDA-QUE-PENDURA-01`, curado |
| **o seletor de canal volta a dar som?** | **SIM**, nos DOIS botões, e o **mic junto** (04/08, com o sink deixado MUDO de propósito) | `SOM-SAIDA-MUDA-01` **provada ao vivo**: o `MUTED` sumiu no clique dela, sem ninguém tocar no `pactl` |

---

## O QUE AINDA FALTA — e só você pode medir

Em ordem de valor. Todos cabem em 30 minutos somados.

### 1. ~~O som do controle~~ — **MEDIDO em 04/08, e a cura passou**

Ela clicou com o alto-falante deixado **mudo de propósito**, e o som voltou:
*"voltou a funcionar no controle com cabo"*, nos **dois** botões e com o
**microfone junto**. O `MUTED` sumiu do sink
**no clique**, sem ninguém tocar no `pactl` — que é a cura agindo.

**Falta só a metade do rádio**, e ela está no item 5 abaixo (E2).

### 2. O clone bombardeia o rádio? (15 min) — `RADIO-BOMBARDEADO-01`/M1

Os **dois DualSense** por Bluetooth, **sem o 8BitDo e sem o Pro**, por 15
minutos. Depois me diga a hora de início e fim; eu conto os frames.

> Este é o bloco que decide a queda em cascata. Se der **zero**, o clone está
> condenado e a cura é o produto **avisar**.

### 3. O Pro Controller sozinho (5 min) — BLOCO C

Pro + os dois DualSense, sem o 8BitDo. **Observar:** cai em 5 minutos?

### 4. Os quatro COM JOGO ABERTO (10 min) — BLOCO D completo

Falta a parte que importa: **abrir um jogo**. Os quatro conectaram, mas nenhum
jogo foi aberto.

**Observar:** o jogo enxerga quantos? os números batem com a janela? a numeração
muda sozinha durante a partida? os dois DualSense têm luz, vibração e gatilho
**dentro do jogo**?

### 5. O alto-falante no cabo x no BT (5 min) — E1/E2

Com o som já funcionando (item 1), repita **no cabo** e **no rádio**.

> A previsão da casa é que **não sai no BT** (a ponte de saída por BT não está
> implementada). Se **sair**, a previsão está errada e é achado grande.

---

## O que NÃO depende mais de você

- **A2** (o LED do microfone acende e fica?) está **bloqueado por código**, não
  por você: o daemon força `common[8] = 0` em todo report, então o LED não serve
  de instrumento. A `LED-SEM-DONO-01` tem de executar **antes** desta medição —
  registrado em 03/08, depois de eu gastar uma pergunta sua com ela.
- **B3** (modo Switch) é **opcional e arriscado** — pode custar o pareamento. Só
  vale se a `IDENTIDADE-DUPLA-01`/M3 precisar, e ela avisa quando precisar.
