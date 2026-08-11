# QUATRO-NO-RÁDIO-01 — o checklist dos quatro controles por Bluetooth

- **Status:** PROPOSTA, escrita em 03/08/2026
- **Prioridade:** é o **destino da leva**, não uma sprint isolada — ela consome
  as outras
- **A meta, na voz dela:** *"a ideia é jogar com os 4 ao mesmo tempo via bt e
  com as features do hefesto nos dois da sony"*
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Referência:** [paridade Bluetooth × cabo](../../protocol/paridade-bluetooth-versus-cabo.md)

> ### **MEDIÇÃO DELA** — os quatro controles no rádio, com JOGO ABERTO.
>
> Os quatro já conectaram (03/08), mas **nenhum jogo foi aberto** — e é dentro do jogo que a numeração e os recursos importam. Item 4 do protocolo.


---

## (a) O que JÁ FUNCIONA — não mexer, e escrever no README

| item | prova |
|---|---|
| o externo chega ao jogo pelo kernel; **não** o grabamos nem escondemos | `EVIOCGRAB` só no P1 (`daemon/subsystems/gamepad.py:127-166`) e no co-op (`coop.py:410+`); o broker **recusa por construção** (`reject_not_physical_dualsense`, `broker/hidraw_broker.py:598-609`). O hidraw do Pro e do 8BitDo é **inesconderível** |
| as envs do wrapper **não** escondem os externos | `_IGNORE_VALUE = "0x054c/0x0ce6"` (`daemon/launch_env.py:83`) é **um par**, não lista — `05c4` e `057e:2009` não casam. Travado em `tests/unit/test_steam_launch_options_vdf.py:98-108` |
| numeração 1..N única na mesa, e LED de posição nos dois modos | `daemon/subsystems/external_identity.py:473-517`; `core/external_leds.py:98-134` (Pro) e `:291-312` (8BitDo em DS4) |
| disciplina anti-bombardeio | cache por valor + `LED_MIN_INTERVAL_SEC = 2.0` (`external_identity.py:154`) + telemetria `external_led_written` |
| o externo é **read-only por decisão de produto** | `coop.py:770-776` (*"dar-lhe vpad reverteria o 8BIT-02"*) e `ipc_handlers.py:1790-1796` |

> **A consequência que precisa estar escrita:** *"os quatro jogam"* já é verdade
> hoje — foi assim em 25/07. O que **não** é verdade é *"os quatro com as
> features do Hefesto"*: os externos ganham número e luz, nunca vpad. É desenho,
> não defeito. **O defeito é a promessa do README**, que usa a mesma frase para
> as duas coisas.

## (b) O que é DEFEITO NOSSO — em ordem de execução

**B1. [COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md) — o gargalo real.**
O `EBUSY` vem de **dentro** do daemon (o primário é re-apontado ao `event` que o
co-op já grabou); o Jogador 2 dura **dois segundos**, quatro ciclos em 22 minutos
no journal dela.

> **Enquanto isto não cair, "os quatro jogando" é impossível por construção —
> dois deles são o mesmo jogador.** E nenhuma medição de rádio feita antes disso
> mede a mesa que ela quer.

**B2. [PS-TOQUE-CURTO-01](2026-08-03-PS-TOQUE-CURTO-01-o-gesto-de-religar-o-controle-abre-a-steam.md)** —
o gesto de religar o controle **abre a Steam**, e sem `wmctrl` abre uma segunda.
É a outra metade do ciclo que ela viveu.

**B3. [WRAPPER-EM-TODOS-01](2026-08-03-WRAPPER-EM-TODOS-01-a-invariante-duplicado-melhor-que-zero-com-quatro.md) —
antes do PRÓXIMO `install.sh` nesta máquina.** O passo `11b-bis` está **no
índice** e roda `--apply --stop-steam` (`install.sh:2586`); pela regra da casa,
*a árvore de trabalho é o que roda*. Com 2 DualSense e 1 vpad, o `IGNORE` esconde
**os dois** físicos e só **um** volta: a mesa cai de 4 para 3, e o que some é um
DualSense.

**B4. [QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md), defeito 1 —
o número dos externos dança quando um DualSense pisca.** `_connected` tem dois
escritores: o tique lento **substitui** o conjunto a cada 2 s
(`identity.py:686`) e o provider de cor o **adiciona** a 10 Hz (`:583`, chamado
em `:1016`).

**Cura de raiz:** separar os eixos —
`slot_for(uniq, assign=True, mark_present=False)`. Hoje os dois efeitos estão sob
a mesma flag.

**Medido no journal dela:** `external_led_repintado intruso=3` e `intruso=2` — o
Pro Controller renumerado **duas vezes em 24 segundos**.

**B5.** Antes de estender qualquer detector de "intruso": **estender um detector
que mente é importar o falso positivo em vez de curá-lo.**

**B9. A [MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md) inteira** —
o checklist não fecha sem ela, e ela não pode ser refeita aqui dentro.

## (c) O que é LIMITE DE HARDWARE (ou de decisão registrada)

- **o 8BitDo em modo Switch por Bluetooth é instável, e não é defeito nosso.**
  `docs/usage/troubleshooting-8bitdo.md:29-31` tem a tabela dos modos, e o modo
  Switch por BT está **PROVADO instável** (`joycon_enforce_subcmd_rate: exceeded
  max attempts`). **A via boa é DirectInput/PS4** (`054c:05c4`), combo
  **`X+Start`** ao ligar (`:44`);
- **o modo é troca FÍSICA no controle** — o cabo não escolhe; ele transporta o
  modo em que o controle já está. Foi o que a mantenedora corrigiu em 03/08,
  contra uma afirmação apressada do assistente;
- **os externos não têm as features do Hefesto** porque não têm vpad — e dar-lhes
  vpad reverteria o `8BIT-02`;
- **áudio de sistema por BT é impossível** — sem A2DP/HFP/HSP.

## (d) O que precisa da MÃO DELA — medições de dez segundos, em paralelo

Não bloqueiam código:

1. **os quatro no rádio ao mesmo tempo** — nunca foi feito desde a noite ruim.
   Medir: quantos `evdev_grab_failed` e `coop_player_removed` no journal;
2. **o 8BitDo em `X+Start` (PS4) por BT** — ele sobrevive à sessão? A tabela diz
   que sim, e nunca foi revalidado com os outros três no ar;
3. **o Pro Controller em modo Switch por BT** — está na mesa agora, e a tabela o
   marca como instável. Ele cai junto?
4. **o rumble no rádio** — *"um motor girando por BT nunca foi medido nesta
   casa"*; **medido em 03/08 e funcionou**, mas com dois controles, não quatro;
5. **a contenção com quatro** — o `dmesg` acusa `DualSense input CRC's check
   failed` já com dois.

---

## O aceite final da sprint

Ela abre um jogo, os quatro controles estão no rádio, e:

- os **quatro** aparecem como jogadores distintos no jogo;
- os **dois DualSense** têm lightbar, gatilhos, rumble e sensores;
- os **dois externos** têm input e número de jogador coerente;
- **nenhum** cai durante a partida;
- a numeração **não muda sozinha** quando alguém pisca.

## O que NÃO fazer

- **não dar vpad aos externos** sem reabrir o `8BIT-02` explicitamente;
- **não medir a mesa antes do B1** — com o Jogador 2 durando dois segundos, a
  medição não mede o que se quer;
- **não pedir a ela que use o 8BitDo em modo Switch por BT** — está provado
  instável, e a alternativa é um combo ao ligar;
- **não estender o detector de intruso** antes de curar o B4.
