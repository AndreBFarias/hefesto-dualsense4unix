# Divergências nomeadas — os apelidos que NÃO são sprints

- **Criado em:** 11/08/2026, pela sprint `A-9 NOME-QUE-NÃO-EXISTE-01`
- **Grau:** MEDIDO — a varredura que achou os três está em
  [INDICE duas verdades](sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md),
  itens S-5, S-6 e P-11

## Por que este arquivo existe

Esta casa batiza defeitos. É bom: um nome curto viaja bem por comentário de
código, mensagem de commit e conversa. O problema aparece quando o nome é citado
como *"ver a sprint X"* ou *"o estudo X"* — e **não existe arquivo nenhum com
esse nome**. Quem lê vai procurar, não acha, e ou perde tempo ou conclui que a
página está velha.

Medido em 11/08/2026: três apelidos estavam nessa situação, somando **26
citações em 19 arquivos**, incluindo `src/` e um cabeçalho de patch que vai para
o upstream.

**A regra, daqui em diante:** um apelido é uma de duas coisas.

- **Sprint ou estudo** — tem arquivo em `docs/process/sprints/` ou
  `docs/process/estudos/`, e se cita com link.
- **Divergência nomeada** — é só um apelido para uma discordância entre fontes,
  registrada **aqui**. Cita-se dizendo o que é: *"a divergência `NOME` (ver
  DIVERGENCIAS-NOMEADAS.md)"*, nunca *"a sprint `NOME`"*.

Não há terceira opção. Um nome que não é nenhum dos dois é um nome que mente.

---

## As divergências registradas

### `GUERRA-01` — quem manda no hidraw quando o Proton entra

**O que nomeia:** a disputa entre o `winebus.sys` do Proton, o SDL e o nosso
gamepad virtual pelo mesmo controle. O nome nasceu em 18/07/2026 num estudo que
**nunca virou arquivo**; o que existe do assunto está espalhado em comentários
de código e, desde 11/08, em
[pilha-steam-input-xpad-sdl.md](../protocol/pilha-steam-input-xpad-sdl.md).

**Estado:** o mecanismo está **medido e com grau ALTA** — o fonte do Proton
(`main.c`, `unixlib.h`) confirma que o `winebus` casa VID/PID por texto e trata
`0x0df2` explicitamente, e que `SDL_GAMECONTROLLER` tem **zero ocorrências**
naquele caminho. É por isso que `PROTON_DISABLE_HIDRAW` existe: a variável do
SDL não cobre o winebus.

**Onde ler:** a página da pilha, seção do `winebus`. **Não procure por um
estudo de 18/07 — ele não existe.**

### `GYRO-EDGE-RATE-01` — a taxa que o vpad declara e a que ele entrega

**O que nomeia:** o gamepad virtual se declara DualSense Edge, e o SDL trata o
Edge como 1000 Hz por USB (`SDL_hidapi_ps5.c`, decisão por tabela, sem medir).
O que ele entrega é a taxa do controle físico.

**Estado, medido em 11/08:** o cabo entrega **250,0 Hz exatos** — duas réguas
independentes concordando, e batendo com o descritor USB. O rádio é **variável,
em rajadas** (363, 240, 334, 55 e 70 Hz em cinco janelas), e **nunca 1000 Hz**.

**O que continua sem medição:** o que de fato quebra num jogo que integre pela
taxa declarada em vez de medir os intervalos. A conta sugere erro de escala de
4x; ninguém observou o efeito.

**Onde ler:** [driver-hid-playstation.md](../protocol/driver-hid-playstation.md).

### `NINTENDO-VARIANT-01` — distinguir o Pro genuíno do clone em runtime

**O que nomeia:** o produto escreve e o `doctor` confere uma marca
`HEFESTO_CONTROLLER_VARIANT`, e **nenhum arquivo de `src/` a lê**. É a
`ENTREGA-QUE-NÃO-LIGOU` na forma clássica.

**Estado, medido em 11/08:** o discriminador que funciona é o `bcdDevice` do
descritor USB — `0210` no genuíno, `0200` no clone. A marca **vive no `hidraw`**,
**não persiste no device `hid`** (o udev só guarda propriedade de device com nó
em `/dev`), e **é impossível por Bluetooth**: o Pro por rádio pendura em `uhid`,
e a cadeia inteira não tem `bcdDevice`.

**O caminho barato, se alguém for fechar:** ler a marca do `hidraw`, onde
`src/hefesto_dualsense4unix/core/external_leds.py` já resolve o caminho.

**Onde ler:**
[driver-hid-nintendo-por-dentro.md](../protocol/driver-hid-nintendo-por-dentro.md).

---

## Como acrescentar uma

Batizou uma discordância entre fontes e não vai escrever sprint para ela? Uma
entrada aqui, com quatro coisas: **o que nomeia**, **o estado** (com grau), **o
que continua sem medição**, e **onde ler**. Se depois virar sprint de verdade, a
entrada aponta para o arquivo novo e some daqui.
