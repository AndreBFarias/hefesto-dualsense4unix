# LIGHTBAR-BT-CULPADO-01 — o report que "curava" é o que trava

- **Status:** PROPOSTA, escrita em 03/08/2026 **depois da medição no hardware**.
  Nenhuma linha de código tocada
- **Prioridade:** **MÁXIMA DA LEVA.** É a regressão que ela descreve como
  *"sempre arrumamos mas sempre volta"*, e a causa-raiz está **provada**
- **Faixa:** 1 — o produto quebra o que deveria consertar
- **Causa-raiz:** **PROVADA por correlação perfeita em 7 eventos**, com o olho
  dela confirmando cada estado. **Não precisa de medição nova para executar**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Evidência:** [a noite em que medimos a lightbar do Bluetooth](../estudos/2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md)
- **SUBSTITUI:** a causa-raiz e a cura da
  [LIGHTBAR-BT-CLAIM-01](2026-08-02-LIGHTBAR-BT-CLAIM-01-a-barra-apagada-com-o-sysfs-certo.md),
  **refutadas por medição** (ver "O que caducou")

---

## O veredito

> **O `0x08` (`VALID_FLAG1_RELEASE_LEDS`), enviado dentro da janela de ~3,4 s
> após a conexão por Bluetooth, trava a lightbar até o power-off físico do
> controle.**
>
> **Ele existe desde 18/07/2026 e foi acrescentado como a CURA da lightbar por
> Bluetooth.**

## A prova

Sete eventos do journal de 03/08, cruzados com o estado que ela confirmou:

| # | evento | `0x08` depois de conectar? | barra |
|---|---|---|---|
| 1 | branco `17:48:24.266` | sim — mesmo milissegundo | travou |
| 2 | roxo `17:48:36.709` | sim — **53 ms** | travou |
| 3 | roxo `19:34:45.476` | sim — mesmo ms | travado |
| 4 | roxo `19:53:17.904` | sim | travado |
| 5 | roxo `19:56:08.022` | sim — **695 ms** | travado |
| 6 | **roxo `20:03:56`** | **NÃO** | **OBEDECE** |
| 7 | branco `20:04:20.989` | sim — **515 ms** | travou |

Sete de sete. **Os dois controles estavam no mesmo rádio, na mesma mesa, no
mesmo minuto** — e o único que não recebeu o report é o único que obedece.

**Controle negativo, no mesmo teste:** o `0x08` enviado num controle conectado
havia **dez minutos** (fora da janela) **não travou a barra**. É a mesma
assimetria que separa o evento 6 do 7.

## E isso explica o que JÁ funcionava — a regra da casa

- **o cabo nunca teve o problema:** o report `0x02` do USB não tem janela nem
  máquina de estados de lightbar. Medido de novo hoje: com o daemon parado, o
  mesmo comando pintou o USB e não pintou o rádio;
- **às vezes funciona no BT:** quando o handle é reaproveitado, o
  `adopt_candidates` não dispara e o `0x08` **não sai** — é o evento 6. Essa
  intermitência é exatamente a queixa *"sempre arrumamos mas sempre volta"*;
- **os player-LEDs e os gatilhos continuam funcionando** com a barra travada,
  como o `LIGHTBAR-BT-ADOPT-01` registrou em julho. O latch é **da barra**.

## O que caducou (e por que é importante registrar)

### A `LIGHTBAR-BT-CLAIM-01` está refutada em três pontos

Escrita em 02/08, um dia antes desta medição:

1. *"o gatilho é o reinício do daemon"* — **não é.** O evento 6 é uma reconexão
   com o daemon **vivo** e não travou; o 7 é outra, e travou;
2. *"o `0x08` devolve o claim ao firmware e ninguém retoma"* — **não fatalmente.**
   Evento 4: enviado, e a barra obedeceu à cor seguinte;
3. **a cura proposta APAGA a barra.** Ela manda `common[41] = LIGHT_OUT`. O
   driver desta máquina diz:
   ```c
   report.common->lightbar_setup = DS_OUTPUT_LIGHTBAR_SETUP_LIGHT_OUT; /* Fade light out. */
   ```
   Testado ao vivo: **nenhum efeito.** Quem a executasse escreveria código para
   apagar a barra acreditando que a acendia.

**A sprint não se apaga** — ganha nota datada apontando para cá. É a regra da
casa, e neste caso ela é o próprio conteúdo: *o registro de uma cura errada vale
tanto quanto o da certa.*

### O `LIGHTBAR-BT-ADOPT-01` acertou a janela e errou o culpado

Julho identificou a janela de ~3,4 s e culpou **o report malformado da
pydualsense 0.7.5**. A cura foi `_suppress_leds = True` no nascimento do handle.

A janela ficou fechada para a pydualsense — **e o daemon passou a mandar,
deliberadamente, dentro dela, um report que solta os LEDs.** A cura de um
defeito virou o veículo do outro.

---

## As entregas

### E1 — parar de enviar o `0x08`

**Onde:** `core/backend_pydualsense.py:1524-1546` (o bloco `adopt_candidates` →
`send_release_leds`).

**Por que é remoção e não ajuste** — os três fatos que sustentam:

1. **ele não cura.** O evento 6 prova: sem `0x08`, a barra obedece;
2. **ele causa o latch** dentro da janela (7/7);
3. **ele apaga os player-LEDs**, sempre — medido isoladamente: `--x--` antes,
   tudo escuro depois. E o projeto o manda em **toda** adoção de handle novo,
   ou seja, todo reconnect por Bluetooth apaga o número do jogador.

**O kernel nunca o envia:** `grep RELEASE_LEDS` no `hid-playstation.c` desta
máquina devolve **só a definição** (`:189`), zero usos.

**Aceite:** conectar um DualSense por Bluetooth com o daemon vivo → a barra
acende na cor do perfil e **continua obedecendo**. Medível pelo olho dela em dez
segundos, e no journal pela ausência de `lightbar_reset_enviado`.

**Se houver receio de remover de uma vez:** o meio-termo medido é **adiar** o
`0x08` para fora da janela de 3,4 s. Mas isso conserva um report sem função
conhecida e mantém o custo dos player-LEDs. **A sprint recomenda a remoção**, e
recomenda que a nota datada explique por que ele existiu.

### E2 — o `RESET-02` e o `RESET-03` saem junto

Com o `0x08` fora, morrem os dois satélites dele:

- **`RESET-02`** (`should_reclaim_on_wake`, `core/lightbar_reset.py:91-122`) —
  a `LIGHTBAR-BT-CLAIM-01` já provou que é **código morto em regime** (a
  condição `current == (0,0,128)` nunca casa, porque o priming repõe a cor antes).
  E hoje sabemos o porquê mais fundo: **o sysfs mostra o valor pedido, não o
  aceso** — a condição certa está sendo medida no lugar errado;
- **`RESET-03`** (a invalidação de cache no `connect`,
  `backend_pydualsense.py:1542-1546`) — no-op por construção: opera num objeto
  que o `discover()` descarta 70 linhas adiante.

**Armadilha nomeada:** `tests/unit/test_lightbar_reset.py:122-129` é um
**teste-muralha** — lê o texto-fonte do backend e exige as strings
`should_reclaim_on_wake` e `lightbar_reset_reenviado_wake`. Quem for aposentar o
`RESET-02` **tem de encarar esse teste primeiro**. Ele trava a correção, que é a
definição de muralha.

### E3 — a tela para de afirmar o que não mediu

Provado hoje da forma mais limpa que já se conseguiu: **depois do power-off, o
nó de LED nasceu `0 0 0` com a barra acesa em azul**; e travado, ele aceita
qualquer valor sem que a barra mude.

O `multi_intensity` **não é a verdade do hardware** — está escrito em
`core/sysfs_leds.py:92-105` (`STATUS-01`), e a aba Status inteira depende dele.

**Aceite:** a tela distingue *"mandamos esta cor"* de *"esta cor está no
controle"*. É o defeito 3 da `BT-E-VPAD-01`, que segue aberto e ganhou hoje a
prova mais forte que já teve.

### E4 — o teste que morde

O caminho do `0x08` tem testes que verificam **que ele é enviado**. Depois desta
sprint, o teste tem de verificar o contrário — e não basta afirmar a ausência:

1. **adoção por Bluetooth não emite `RELEASE_LEDS`.** Arranque a remoção e veja
   reprovar;
2. **os player-LEDs sobrevivem à adoção.** Estado antes == estado depois. É o
   efeito colateral provado, e o que mais aparece com quatro controles;
3. **o teste de janela** — o protocolo de medição que faltou a esta casa duas
   vezes: um dublê que registre **quando** cada report sai em relação ao
   `controller_connected`. Sem isso, um `0x08` reintroduzido por engano dentro
   da janela passa despercebido de novo.

**A armadilha que este estudo pagou, e que o teste tem de impedir:** quatro
suspeitos foram inocentados por engano porque foram testados **fora da janela**.
A janela precisa fazer parte do protocolo, não do acaso.

---

## Testes que vão reprovar

```
pytest tests/unit tests/core -k "lightbar or reset or adopt or release"
```

Espere reprovações **legítimas**: há testes travando o comportamento que esta
sprint remove. Cada um precisa ser lido para decidir se trava **a regra** (some
com o `0x08`) ou **o sintoma** (fica, invertido).

## O que NÃO fazer

- **Não mandar `LIGHT_OUT` para "retomar a barra"** — ele apaga. Testado ao
  vivo, sem efeito;
- **Não religar a escrita de LED da pydualsense por BT** — `LIGHTBAR-BT-NEVER-01`,
  pago com a barra latcheada até o power-off;
- **Não reenviar o `0x08` por timer** — o `RESET-02` já proíbe, com motivo
  (pisca a barra de quem está bem);
- **Não mexer no cache do `sysfs_leds`** — a escrita acontece; o cache é pista
  falsa, e a `LIGHTBAR-BT-CLAIM-01` já provou isso;
- **Não medir cor com o daemon vivo por escrita direta no sysfs** — ele desfaz
  em ≤30 s (`NUMA-03`) e você mede a defesa, não o firmware. Use o IPC.

## O que fica ABERTO

- **por que o `0x08` trava dentro da janela** — a correlação é 7/7; o mecanismo
  interno do firmware não é mensurável daqui, e **para a cura não é preciso**;
- **quando o handle é reaproveitado** (o evento 6) — entender isso explica a
  intermitência, que é a queixa dela. `adopt_candidates` sai de `new_handles`
  (`backend_pydualsense.py:1524-1526`);
- **o `8BitDo` e a renumeração dos externos** — capturados no mesmo journal
  (`external_led_repintado intruso=3` / `intruso=2`, o Pro renumerado duas vezes
  em 24 s), e são de outra sprint.
