# As ondas — a ordem de execução da leva do Bluetooth

- **Escrito em:** 03/08/2026, ao fim da noite de medição
- **O que é:** o **roteiro de execução** das 19 sprints da leva, em ondas, com as
  dependências que foram **provadas** (não supostas)
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **A meta, na voz dela:** *"deixar o projeto robusto de tal forma que eu não
  note que estou no bt ou cabo"* e *"jogar com os 4 ao mesmo tempo via bt"*

---

## As regras que ordenaram as ondas

Três critérios, nesta prioridade:

1. **dependência dura** — B não pode ser aceito antes de A (não "seria melhor",
   mas *"o aceite de B nasce inválido sem A"*);
2. **janela** — o que fica mais caro se esperar;
3. **o que ela sente** — entre duas sprints do mesmo custo, primeiro a que
   aparece no próximo uso.

E uma regra de método que a noite de 03/08 impôs:

> **Medição antes de código.** Três sprints desta leva foram **refutadas por
> medição de dez segundos** — duas delas escritas horas antes. A ONDA 0 é medição
> pura, e ela não custa quase nada.

---

## ONDA 0 — o que JÁ ESTÁ FEITO (03/08)

Fica registrado para ninguém refazer.

| entrega | estado |
|---|---|
| **[LIGHTBAR-BT-CULPADO-01](2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md)** — o `0x08` saiu | **APLICADA**, e ela viu as duas barras acenderem |
| **ÍCONE-VIVO-01** — hook + job de CI + comentário corrigido + ícones regerados | **APLICADA** (dentro da `DOC-QUE-NÃO-MENTE-04`/E2-bis) |
| dois testes invertidos (`test_lightbar_reset.py`) | **APLICADA** — travam a ausência do `0x08` |
| notas datadas de refutação (`BT-SURDO-01`, `LIGHTBAR-BT-CLAIM-01`) | **APLICADA** |

**Estado da árvore:** 6792 testes verdes, `ruff` e `mypy` limpos.

---

## ONDA 1 — as medições de dez segundos (não bloqueiam código)

**Rodam em paralelo com tudo.** Cada uma pode **matar ou confirmar** uma sprint
inteira, e três já mataram.

| # | medição | destrava | custo |
|---|---|---|---|
| 1.1 | **"Desligar" desfaz "Rígido"?** — aplicar Rígido forte no L2, sentir, aplicar Desligado, sentir | `ENTREGA-QUE-NÃO-LIGOU-01`/E2 — se continuar duro, a cura é **uma linha** | só o tato |
| 1.2 | **o rumble para quando o controle sai?** — dois no BT com jogo vibrando, desligar um | `BORDA-DE-QUEDA-01` | só o tato |
| 1.3 | **os quatro no rádio ao mesmo tempo** — nunca foi feito desde a noite ruim | `QUATRO-NO-RÁDIO-01` (bloco d) | conectar |
| 1.4 | **o 8BitDo em `X+Start` (PS4) por BT sobrevive?** | `QUATRO-NO-RÁDIO-01`, pedido 6 | conectar |
| 1.5 | **o botão do mic acende o LED e FICA?** | é o aceite da `LED-SEM-DONO-01` | um toque |

> **1.5 tem de ser feita ANTES da ONDA 3** — é o aceite "antes" que prova a cura
> depois.

---

## ONDA 2 — a janela que fecha (urgente por prazo, não por gravidade)

### [WRAPPER-EM-TODOS-01](2026-08-03-WRAPPER-EM-TODOS-01-a-invariante-duplicado-melhor-que-zero-com-quatro.md)

**Sozinha nesta onda, e o motivo é a janela:** o passo `11b-bis` está **no índice
do git, não commitado**, e roda `--apply --stop-steam`. Pela regra da casa, *a
árvore de trabalho é o que roda* — se ela rodar o `install.sh` antes desta cura,
o `IGNORE` pode esconder os dois DualSense físicos e devolver só um vpad.

**Resolver antes do commit custa uma linha; depois, custa uma sessão de jogo.**

---

## ONDA 3 — o ciclo que ela viveu (o maior valor sentido)

As três juntas curam **a noite de 02/08** inteira.

| ordem | sprint | por quê nesta posição |
|---|---|---|
| 3.1 | **[LED-SEM-DONO-01](2026-08-03-LED-SEM-DONO-01-o-common8-ganha-dono-e-os-textos-param-de-mentir.md)** | **dependência dura**: enquanto o LED for forçado apagado, o aceite da 4.1 **nasce inválido**. E é o aceite mais barato da leva (um toque + um cronômetro) |
| 3.2 | **[COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md)** | **é o gargalo dos quatro no rádio**: com o Jogador 2 durando dois segundos, "os quatro jogando" é impossível por construção |
| 3.3 | **[PS-TOQUE-CURTO-01](2026-08-03-PS-TOQUE-CURTO-01-o-gesto-de-religar-o-controle-abre-a-steam.md)** | a outra metade do mesmo ciclo: o controle cai, ela segura o PS, a Steam abre |

> **3.2 e 3.3 são o mesmo ciclo visto de dois lados.** Separadas, cada uma cura
> metade e ela continua sentindo a outra.

---

## ONDA 4 — o áudio ganha dono

| ordem | sprint | dependência |
|---|---|---|
| 4.1 | **[MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md)** | **exige a 3.1** (o LED como instrumento). Ordem interna obrigatória: E1 → E2 → E3 → **E4 → E5** → E6 |
| 4.2 | **[ÁUDIO-QUE-TRANCA-01](2026-08-03-AUDIO-QUE-TRANCA-01-um-toque-no-volume-congela-a-troca-de-perfil.md)** | o clear da categoria `audio` + o `speaker_set(rota=)` que trava em zero |
| 4.3 | **[POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md)** | **mexe no MESMO campo** que a 4.2 (`manual_override_categories`) — juntas evitam duas migrações |

> **Por que E4 antes de E5 na 4.1:** sem o `uniq` no evento de botão, a posse
> tomada no Controle 2 **desfaz o gesto físico dela em ≤0,5 s, em silêncio** — que
> é a opção que a `BT-E-VPAD-01` recusou, entrando pela porta dos fundos.

> **A 4.1 NÃO promete 0% de mudo.** O alvo é 55-75%; o `BT-MIC-GATING-01` segue
> aberto. Prometer 0% é prometer o que a casa já mediu como não obtido.

---

## ONDA 5 — as bordas e os furos finos

Depois que o ciclo principal está curado, o que aparece com quatro controles.

| ordem | sprint | nota |
|---|---|---|
| 5.1 | **[BORDA-DE-QUEDA-01](2026-08-03-BORDA-DE-QUEDA-01-o-que-fica-para-tras-quando-um-controle-cai.md)** | usa a **mesma bancada** da 3.2 (o enumerador com roteiro de queda) |
| 5.2 | **[BT-FURO-FINO-01](2026-08-03-BT-FURO-FINO-01-os-sete-caminhos-que-so-degradam-no-radio.md)** | o **defeito 1** (áudio virando input) é **pré-requisito duro** para mic BT e giroscópio coexistirem |
| 5.3 | **[QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md)** | depende da bancada da 3.2 e da 5.1 |
| 5.4 | **[BT-SURDO-01](2026-08-03-BT-SURDO-01-o-controle-parado-no-radio-nao-recebe-ordem.md)** — **só E2/E3/E4** | a premissa caiu; E1 morreu. As três restantes são defeitos de código independentes |

> **O defeito 1 da 5.2 sobe para a ONDA 4 se ela ligar a ponte de mic** — sem o
> filtro do bit de áudio, o Opus vira giroscópio e clique de touchpad.

---

## ONDA 6 — o produto para de mentir sobre si mesmo

| ordem | sprint | por quê |
|---|---|---|
| 6.1 | **[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)** | três entregas declaradas que **não estão de pé**; a E5 (portão contra símbolo órfão) **protege todas as ondas seguintes** |
| 6.2 | **[ESTADO-QUE-MENTE-01](2026-08-03-ESTADO-QUE-MENTE-01-o-daemon-afirma-controle-conectado-com-a-mesa-vazia.md)** | a aba Status mostra 85% de bateria com a mesa vazia |
| 6.3 | **[DOC-QUE-NÃO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md)** | **os seis portões são a entrega**; as correções sem eles reabrem na próxima leva |
| 6.4 | **[DOC-QUE-NÃO-MENTE-03](2026-08-03-DOC-QUE-NAO-MENTE-03-a-foto-vazia-a-env-negada-e-a-tag-velha.md)** | a foto vazia da aba Início e a recontagem dos índices |

> **A 6.4/E5 (recontagem dos índices) vale ser feita ANTES de tudo** se alguém
> for planejar a próxima leva por índice — eles estão defasados **para menos**.

> **A 6.4/E1 (a foto da aba Início) é pré-requisito da PROVA-DE-TELA-01** de
> qualquer sprint de interface: a aba é 100% código e sai vazia na foto.

---

## ONDA 7 — os pedidos dela (interface)

Roteados em [PEDIDOS-DELA-01](2026-08-03-PEDIDOS-DELA-01-o-roteiro-dos-seis-pedidos-da-interface.md).
**Cinco dos seis melhoram sprints existentes.**

| ordem | pedido | destino | nota |
|---|---|---|---|
| 7.1 | o `doctor` para de mandar para o modo que mata | `DOC-VERDADE-02` | **o item mais barato do plano inteiro**, e hoje ele empurra ela para o modo instável |
| 7.2 | o nome do 8BitDo | **[NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md)** | única sprint nova; alto valor de uso, custo baixo |
| 7.3 | co-op sempre ativo | `AUTO-01` | **depende da 6.4/E1** (a foto) para a prova de tela |
| 7.4 | remover "Ouvir no controle" | `SOM-ROTA-01`/E6 | **a ordem interna é a entrega** — tirar o botão antes de migrar mata a rota em silêncio |
| 7.5 | áudio no BT não mentir | `SOM-02`/E6 + `MIC-BT-01` | depende da ONDA 4 |
| 7.6 | máscara do externo | `MÁSCARA-01` | **zero código nesta leva** — só o documento |

---

## ONDA 8 — o destino

### [QUATRO-NO-RÁDIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md)

**Não é sprint de código — é o checklist de aceite da leva inteira.** Ela consome
as ondas 2 a 7 e fecha com a medição na mesa dela:

> os quatro controles no rádio, os quatro como jogadores distintos, os dois
> DualSense com lightbar, gatilhos, rumble e sensores, **nenhum caindo**, e a
> numeração **não mudando sozinha**.

---

## O caminho crítico, em uma linha

```
ONDA 1 (medições, em paralelo)
   └─► ONDA 2 (janela) ─► 3.1 LED ─► 3.2 co-op ─► 3.3 PS ─► 4.1 mic ─► ONDA 8
                                        └─► 5.x bordas
```

**Se for fazer uma coisa hoje:** a ONDA 2 (janela que fecha).
**Se for fazer uma coisa que ela sinta:** a 3.2 (o Jogador 2 que dura dois
segundos).
**Se tiver dez segundos:** a ONDA 1 inteira, que pode matar sprint antes de ela
custar código.

## O que NÃO cabe em onda nenhuma

- **o aceite em jogo real** — nenhuma sprint fecha sem ela jogar;
- **o `BT-MIC-GATING-01`** — segue aberto, com o principal suspeito eliminado;
- **a ponte de saída de áudio por BT** (o alto-falante) — é sprint inteira, e
  antes da primeira linha é preciso resolver a contradição `0x39` × `0x32`;
- **a queda do Bluetooth em si** — as sprints daqui curam o que o daemon faz *em
  volta* da queda; a queda é de rádio, BlueZ e coexistência.
