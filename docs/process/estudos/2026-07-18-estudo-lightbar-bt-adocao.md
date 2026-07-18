# Estudo 2026-07-18 — a lightbar do DualSense por BT apaga na ADOÇÃO (e a cura)

**Contexto:** co-op misto (2× DualSense BT + 8BitDo). Sintoma reportado pela
mantenedora: a lightbar do secundário não acendia por BT ("um tá azul e o
outro era pra ter a cor dele também"); depois, nos ciclos de teste, as DUAS
apagaram. Player-LEDs, gatilhos adaptativos e rumble sempre funcionaram nos
mesmos controles — só a lightbar morria.

Metodologia: testes ao vivo dirigidos (com a mantenedora olhando os controles)
+ 2 workflows de agentes (design do fix, 4 frentes; estudo rigoroso, 5 agentes
com kernel liberado — desmontagem do `hid-playstation.ko` desta máquina).

## Linha do tempo dos fatos provados ao vivo

1. Estado inicial: P1 (primário) azul aceso; P2 apagado. Em AMBOS:
   player-LEDs brancos + gatilhos + rumble OK (mesma rota kernel/sysfs!).
2. 330 mil escritas em `multi_intensity` do P2 (nó gravável, valores certos,
   toggle de brightness) → NUNCA acendeu por BT. **Via cabo USB acende na
   hora** (o mesmo valor sysfs).
3. Re-parear BT não curou (o controle ficou LIGADO durante o processo).
4. P2 sozinho no adaptador → não acendeu (não é contenção de banda).
5. Tentativa "suprimir só o primário e pintar o secundário via pydualsense"
   → apagou AS DUAS (a rota pydualsense de LED por BT não funciona e a
   interferência derruba até a entrega do kernel). Revertida.
6. Rebind do driver (unbind/bind) → re-probe, cores re-escritas → não acendeu
   (o daemon re-adotou em seguida e re-envenenou).
7. **POWER-OFF completo** (PS ~10s) + reconectar → a lightbar ACENDE no
   connect **e APAGA no instante em que o daemon ADOTA o controle**.
   Reproduzido nos dois controles, com o código original.
8. Fix "nascer suprimido" + política "BT nunca escreve LED pela pydualsense"
   → o sintoma persistiu ("liga, fica azul e depois desliga") → o veneno NÃO
   é o conteúdo dos writes do report_thread: é a **abertura/feature-reads da
   adoção em si**.

## Causa-raiz (síntese do estudo)

A lightbar do DualSense tem uma **máquina de estados própria no firmware**
(claim). A adoção pelo daemon (abertura do hidraw pela pydualsense +
feature reads do `init`) **derruba o claim por BT**: a lightbar apaga e passa
a ignorar as escritas de cor do kernel (rota sysfs/classe LED) — enquanto
player-LEDs/gatilhos, sem máquina de estados, continuam. O estado ruim
persiste até o power-off físico (sobrevive a re-parear e a rebind; USB não
tem o claim, por isso o cabo "curava").

O SDL conhece esse comportamento: em toda conexão BT ele espera a animação
de connect e envia `valid_flag1 = 0x08` ("Reset LED state") antes de
qualquer cor. O driver do kernel define `DS_OUTPUT_VALID_FLAG1_RELEASE_LEDS`
e **nunca o usa** — o kernel assume que ninguém mais toca o device.

Achado colateral (estudo, frente kernel): o report BT da pydualsense 0.7.5
tem layout divergente do kernel/SDL (sem o byte de tag `0x10`; seq fixo).
Rumble/gatilhos funcionam por ele, mas ele é inadequado para LED por BT — e
a política "por BT a pydualsense nunca escreve LED" (LIGHTBAR-BT-NEVER-01)
ficou como defesa em profundidade.

## A cura — LIGHTBAR-BT-RESET-01

`core/lightbar_reset.py`: monta o report 0x31 **bem-formado** no layout
validado por desmontagem do módulo desta máquina —
`[0]=0x31, [1]=seq<<4, [2]=tag 0x10, [4]=flag1 0x08, CRC-32 (seed 0xA2) LE
em [74..77]` — e o envia pelo device hidapi que a adoção acabou de abrir.

Integração (`backend_pydualsense.connect()`): para **todo DualSense BT
recém-adotado**, envia o Reset LED state logo após abrir o handle (pós
feature-reads) e **antes** do reassert de cor. Best-effort; journal:
`lightbar_reset_enviado`.

Defesas que ficam junto (mesma onda):
- `_suppress_leds` **nasce True** (LIGHTBAR-BT-ADOPT-01): nenhum report com
  flags de LED sai na janela da adoção (nem no zumbi do init-timeout).
- **Política BT** (LIGHTBAR-BT-NEVER-01): por BT a pydualsense fica sempre
  suprimida, coberta ou não pelo sysfs (em USB o fallback histórico segue).
- Falha de UM device não aborta o `connect()` (o refresh sempre roda).
- Telemetria `sysfs_led_cobertura` em INFO (cobertos + sem_no_sysfs) — a
  próxima regressão terá timestamp (a de 17/07 não tinha).

## Validação

- Hermética: suíte completa **3136/0** (novos: `test_lightbar_reset.py`,
  `TestSupressaoDeLedPorTransporte`, contrato novo do connect resiliente).
- Ao vivo (parcial, madrugada): cura crua aceita pelo firmware (78/78 bytes
  no hidraw, sem erro) + pipeline integrado disparando na adoção real
  (`lightbar_reset_enviado` no journal às 01:33:27).
- **Pendente (gate humano):** power-off dos 2 DualSense + reconectar + ver
  as lightbars acenderem E PERMANECEREM (azul/vermelho por slot) após a
  adoção. É o critério de aceite do fix.

## Armadilhas para o futuro

- "Cards azul/vermelho na GUI" NÃO provam lightbar física: os cards leem o
  sysfs/paleta, que aceita a escrita mesmo com o firmware ignorando.
- O journal não tinha NENHUM evento de lightbar (logging era debug-only) —
  por isso a regressão de 17/07 ficou sem timestamp. Mantida a telemetria.
- Um clone DS4 (054C:05C4) em BT gerou um storm de 211 mil CRC fails no
  kernel em 17/07 17:03 — degrada o link do adaptador para TODOS os
  controles; suspeitar dele em instabilidades futuras.
