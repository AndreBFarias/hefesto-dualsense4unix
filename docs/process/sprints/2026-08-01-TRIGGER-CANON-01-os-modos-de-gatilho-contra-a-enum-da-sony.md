# TRIGGER-CANON-01 — os modos de gatilho contra a enum da Sony

- **Status:** PROPOSTA **com portão de medição na frente**, escrita em
  01/08/2026 para sobreviver à queda da sessão
- **Prioridade:** **ALTA se a E0 confirmar** — a suspeita é que 3 dos 19
  presets não fazem nada e vários fazem coisa diferente do nome
- **Fonte:** [a referência canônica do protocolo](../../protocol/dualsense-referencia-canonica.md),
  seções 1 e 4
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)

## O fato que abre a sprint

A tabela de modos desta árvore herdou a nomenclatura opaca de uma engenharia
reversa de 2020 (`Rigid_A/B/AB`, `Pulse_A/B/AB`). Decodificada contra a **enum
oficial da Sony** (que a Valve redistribui no Steamworks SDK) e contra três
engenharias reversas independentes que concordam entre si:

| `TriggerMode` daqui | valor | o firmware entende |
|---|---|---|
| `RIGID` | 0x01 | Simple_Feedback (legado) |
| `PULSE` | 0x02 | Simple_Weapon (legado) |
| `RIGID_A` | 0x21 | **Feedback (oficial)** |
| `RIGID_B` | **0x05** | **OFF** |
| `RIGID_AB` | 0x25 | **Weapon (oficial)** |
| `PULSE_A` | 0x22 | Bow |
| `PULSE_B` | 0x06 | Simple_Vibration |
| `PULSE_AB` | 0x26 | **Vibration (oficial)** |
| `CALIBRATION` | 0xFC | **Debug — corrompe o estado** |

**Cruzando com os 19 presets** (medido no código em 01/08):

| preset | modo que manda | o que o firmware faria |
|---|---|---|
| `rigid`, `simple_rigid`, `feedback` | `RIGID_B` = **0x05** | **OFF — nada** |
| `resistance`, `slope_feedback`, `multi_position_feedback` | `RIGID_AB` = 0x25 | Weapon |
| `weapon` | `PULSE_B` = 0x06 | Simple_Vibration — **vibra** |
| `vibration`, `pulse_a`, `multi_position_vibration` | `PULSE_A` = 0x22 | Bow |
| `bow`, `galloping`, `semi_auto_gun`, `auto_gun`, `machine` | `PULSE_AB` = 0x26 | Vibration — **os cinco iguais** |
| `pulse` | `PULSE` = 0x02 | Simple_Weapon |
| `off` | `OFF` = 0x00 | — |

**E há um segundo erro, ortogonal ao modo.** Os modos oficiais **não recebem
posições cruas**: recebem um **bitmask de zonas ativas** (u16 LE) e **forças de
3 bits com valor `força − 1`** (u32 LE). O `AMPLITUDE_SCALE = 32` desta árvore
(0-8 → 0-255) **não se aplica a nenhum modo oficial**. Sem o bitmask, o firmware
provavelmente vê "nenhuma zona ativa" — o que faria `multi_position_*` e
`slope_feedback` não fazerem nada **independentemente do modo**.

**E isso refuta um bug registrado como medido.** O
`BUG-TRIGGER-MULTIPOS-FORCA8-01` concluiu *"o campo tem 3 bits, logo o máximo
real é 7 e a força 8 satura"*. A codificação real é `(strength − 1) & 0x07` com
`strength` em 1..8, e `strength == 0` significa **zona inativa**. **Os 8 níveis
são expressáveis.**

## E0 (PORTÃO) — medir antes de tocar em uma linha

**Nada abaixo se executa antes desta entrega.** A decodificação é triangulação
de três fontes com a enum da Sony — **não foi medida no hardware desta casa**.

### A armadilha que já custou uma tentativa

Em 01/08 tentou-se medir com `hefesto-dualsense4unix test trigger --raw` e
**os comandos não chegaram ao controle**. A causa está escrita no próprio
código (`cli/cmd_test.py`):

> *"O caminho `--raw` não tem contrato IPC (`trigger.set` exige nome de preset,
> não mode inteiro), então segue direto no hardware."*

Com o daemon vivo, o `--raw` abre um **segundo** controlador e briga pelo
hidraw; o `report_thread` do daemon sobrescreve em ≤ 0,5 s (o keepalive).
**Toda medição por `--raw` com o daemon no ar é inválida.** Isso é defeito
próprio — ver E4.

### O experimento que funciona, e é o mais barato de todos

Pela **GUI**, que passa pelo daemon. Duas perguntas fecham a conta:

1. escolher **"Rígido"** e aplicar → **previsão: o gatilho não muda** (0x05 é
   OFF);
2. escolher **"Bow"**, sentir, depois **"Galope"**, sentir → **previsão: são
   idênticos** (os dois mandam 0x26).

Se as duas previsões se confirmarem, a decodificação está provada e a sprint
inteira se justifica. Se qualquer uma falhar, **pare** e remeça a tabela.

**Alternativa com bancada** (se quiser o bit exato): parar o daemon
(`systemctl --user stop hefesto-dualsense4unix`), usar `--raw`, e reiniciar. Aí
o `--raw` tem o hidraw só para ele.

**Aceite:** o resultado das duas perguntas registrado neste documento.

## E1 — a enum passa a nomear o que a Sony nomeia

`TriggerMode` deixa de ser `RIGID_A/B/AB` e passa a:

```
OFF = 0x05, FEEDBACK = 0x21, WEAPON = 0x25, VIBRATION = 0x26,
BOW = 0x22, GALLOPING = 0x23, MACHINE = 0x27
```

Os legados (`0x01`, `0x02`, `0x06`, `0x11`, `0x12`) ficam, marcados como
legado. Os de depuração (`0xFC`, `0xFD`, `0xFE`) ficam **proibidos** — eles
corrompem o estado do gatilho, e hoje `CALIBRATION = 0xFC` está exposto.

**Onde:** `src/hefesto_dualsense4unix/core/trigger_effects.py`.

**Armadilha:** o `name` de cada preset é **contrato** — perfis salvos no disco
dela guardam esses nomes. Só o **rótulo** de tela pode mudar; o `name`, não.
Regra já registrada nesta casa.

## E2 — os parâmetros passam a ser empacotados como o firmware espera

```
Feedback  (0x21): [1,2] activeZones u16LE ; [3..6] forceZones u32LE (3 bits, força-1)
Weapon    (0x25): [1,2] (1<<start)|(1<<end) ; [3] força-1
Vibration (0x26): [1,2] activeZones ; [3..6] amplitudeZones ; [9] frequência
Bow       (0x22): [1,2] (1<<start)|(1<<end) ; [3,4] (força-1) | (snap-1)<<3
Galloping (0x23): [1,2] zonas ; [3] pé2 | pé1<<3 ; [4] frequência
Machine   (0x27): [1,2] zonas ; [3] ampA | ampB<<3 ; [4] frequência ; [5] período
```

**Boa notícia de fiação:** o caminho já alcança tudo. O backend escreve
`forces[0..5] → param[0..5]` e **`forces[6] → param[8]`** — e `param[8]` é
exatamente onde mora a `frequency` do `Vibration` oficial. **Nenhuma mudança de
protocolo é necessária**, só de empacotamento.

**Onde:** `core/trigger_effects.py` e `docs/protocol/trigger-modes.md`.

## E3 — a nota de refutação do `FORCA8-01`

O bug registrado como medido está errado na causa. Escrever a refutação no
lugar onde ele foi registrado, com a codificação real — **não apagar o
registro**, que é a regra da casa: decisão medida não se reescreve, ganha nota.

## E4 — o `--raw` da CLI para de mentir

Duas saídas, e a segunda é a recomendada:

- **mínima:** o `--raw` detecta o daemon vivo e **recusa**, dizendo para parar o
  daemon ou usar a GUI. Melhor um erro honesto que um sucesso falso;
- **recomendada:** o IPC ganha contrato para modo cru (`trigger.set_raw`), e o
  `--raw` passa pelo daemon como todo o resto. Aí a bancada volta a existir.

**Aceite:** `test trigger --raw` com o daemon vivo ou funciona de verdade, ou
falha dizendo por quê. Nunca imprime "trigger aplicado" sem ter aplicado.

## E5 — ler o que o gatilho está sentindo (diagnóstico grátis)

O **nibble alto** do byte de status de cada gatilho, no report de entrada, diz o
estado: sem carga, carga aplicada, arma pronta, disparando, disparada,
vibrando — mais a posição do braço. A Apple expõe esses mesmos estados com nome
no `GCDualSenseAdaptiveTriggerStatus`.

Isso torna a validação da E1/E2 **verificável sem a mão dela**: manda o efeito,
lê o estado, compara.

## Testes que vão reprovar

`pytest tests/unit -k "trigger"`. Os testes-muralha que travam **texto e valores
dos presets** vão reprovar em massa — adequá-los é parte do trabalho, e cada um
deve passar a medir a regra nova com a mordida escrita no docstring.

Atenção especial a `test_gatilho_palavra_rotulos.py` (rótulos com teto de 22
caracteres) e `test_trigger_presets.py`.

## O que NÃO fazer

- **Não executar E1 em diante sem a E0.** A tabela é convergência de fontes, não
  medição.
- **Não medir com `--raw` e o daemon vivo.** Ver E0.
- **Não trocar o `name` dos presets** — é contrato com os perfis dela.
- **Não expor os modos `0xFC`-`0xFE`** — corrompem o estado do gatilho.
- **Não copiar o header da Sony** para dentro do repositório. Citar a URL.
