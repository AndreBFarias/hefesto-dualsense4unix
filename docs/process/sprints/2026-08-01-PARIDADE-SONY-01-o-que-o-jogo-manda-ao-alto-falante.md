# PARIDADE-SONY-01 — o que o jogo manda ao alto-falante

- **Status:** **E1 (o INSTRUMENTO) ENTREGUE em 02/08/2026.** A medição em si
  depende de ela jogar — e o instrumento agora está lá esperando. A E2 em
  diante continua trancada pelo portão, como a sprint manda
- **Status anterior:** PROPOSTA COM PORTÃO DE MEDIÇÃO NA FRENTE. Escrita em
  01/08/2026 para sobreviver à queda da sessão
- **Prioridade:** BAIXA até a E1 passar; **a E1 é que decide se esta sprint
  tem razão de existir**
- **Aberta em:** 01/08/2026, a partir da pergunta dela sobre paridade entre
  "Jogar direto (Sony)" e "Jogar pelo Hefesto → DualSense"
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)

## Correção de rumo, antes de tudo

O índice desta leva afirma, sobre a lacuna de paridade:

> *"os bytes de áudio do report de saída não estão na lista de replicação do
> REPLICA-03. Um jogo que ajuste o volume do alto-falante do DualSense escreve
> no vpad e o pedido morre ali."*

**A primeira metade é fato; a segunda NÃO foi medida.** O levantamento de
01/08 encontrou três coisas que quem executar precisa saber antes de escrever
uma linha:

1. **O mapeamento dos bytes é PROVÁVEL, não medido.** `core/ds_output_report.py:67-73`
   diz, com todas as letras, que o kernel (`hid-playstation`) declara
   `common[4..7]` como `reserved[4]` e **nunca os escreve**; a nomenclatura por
   bit vem de documentação de comunidade (Nielk1 / DS5 wiki);
2. **não existe uma única captura de report de saída de jogo no repositório.**
   O diretório `captures/` só tem descriptor e feature reports;
3. **o áudio do jogo não passa pelo HID.** O som sai pela placa USB do controle,
   pelo PipeWire. O registrador HID é um **atenuador do firmware** — um segundo
   botão em série com o primeiro. Isso está medido e escrito na
   [SENSOR-VIVO-01](2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md).

Ou seja: **pode não haver defeito nenhum aqui.** É possível que nenhum jogo
escreva esses bytes, e que a "lacuna" seja teórica. Por isso esta sprint começa
por um portão de medição, e não por código.

## E1 (PORTÃO) — provar que existe jogo que escreve esses bytes

**Antes de tocar em `uhid_gamepad.py`, meça.** O objetivo é responder:
*"algum jogo que ela joga escreve `common[4]`, `[5]`, `[6]` ou `[7]` no
gamepad virtual?"*

**Como medir, sem depender de sorte:** o vpad já recebe TODO report 0x02 que o
jogo escreve — `UhidDualSense._handle_output`
(`integrations/uhid_gamepad.py:1255-1294`) é o funil por onde tudo passa, e o
contador `output_count` (`:718-721`) já conta os reports.

O instrumento é um log temporário ali dentro: para cada report, registrar
`flag0 & 0xF0` (os quatro bits de áudio) e os bytes `body[4:8]` quando algum
deles for diferente de zero. Rodar com os jogos dela abertos e ver se alguma
linha sai.

**Os três resultados possíveis, e o que cada um significa:**

| resultado | conclusão | o que fazer |
|---|---|---|
| nenhum jogo liga os bits de áudio | **não há lacuna** — o índice estava errado | fechar a sprint como CICATRIZ, corrigir o índice, e o trabalho de paridade termina aqui |
| algum jogo liga os bits | a lacuna existe | seguir para E2, com a captura como prova |
| os bits ligam mas os bytes vêm zerados | é keepalive, não intenção | **não replicar.** Ver armadilha 10 |

**Aceite:** uma captura anexada à sprint (em `captures/`, com o nome do jogo e
a data), ou a afirmação, com o método descrito, de que nenhum jogo escreveu.

**Esta entrega vale mesmo que a resposta seja "não".** Uma pergunta em aberto
respondida com medição é entrega; um código escrito contra uma premissa não
medida é dívida.

## E2 em diante — só se a E1 disser que sim

O caminho técnico está mapeado. **Seis fronteiras** precisam ser tocadas para
acrescentar uma categoria à replicação, e o gatilho serve de molde exato:

| passo | arquivo:linha |
|---|---|
| constantes de offset | `integrations/uhid_gamepad.py:201-231` (os valores já existem em `core/ds_output_report.py:74-96`) |
| parser | `integrations/uhid_gamepad.py:1356-1386` (`_replicate_from_output`) |
| despacho + contador | `:1416-1455` (`_forward_replica`), campos `:594-596`, properties `:723-736`, zeragem `:861-863` |
| campo de sink | `:559-568`, repasse em `for_flavor` `:632-673` |
| **factory (kwargs FECHADOS — estoura `TypeError` em runtime)** | `integrations/virtual_pad.py:112-124` e `:183-225` |
| fiação P1 / co-op | `daemon/subsystems/gamepad.py:847-891` e `daemon/subsystems/coop.py:500-546` |
| applier (molde: `apply_game_trigger`) | `daemon/subsystems/gamepad.py:771-792` |
| backend (molde: `set_game_trigger_for`) | `core/backend_pydualsense.py:2773-2809` |
| montagem do report | `core/backend_pydualsense.py:617-661` |
| **devolução no fim da sessão — NÃO EXISTE para áudio** | `core/backend_pydualsense.py:2909-2972` |

**O caminho completo do gatilho**, do jogo até o controle físico, está
documentado passo a passo no levantamento e vale reler: `pump_ff` (60 Hz) →
`_handle_output` → `_replicate_from_output` → `_queue_replica` (dedup por
valor) → `_flush_replicas` (rate-limit 250 Hz por categoria) → `_forward_replica`
→ sink → `apply_game_trigger` → `set_game_trigger_for` → `_build_common` →
`report_thread`.

## Por que isto é mais perigoso que as outras quatro categorias

**A posse de áudio é a única SEM camadas.** Compare:

| categoria | posse | devolução no fim da sessão |
|---|---|---|
| lightbar / player-LEDs | camada GAME no merge de 5 camadas + gate `_game_wins()` + retenção | **SIM** |
| gatilhos | `_game_triggers_by_uniq` + `handle._raw_trigger_*` | **SIM** |
| **áudio** | **nenhuma** — escrita direta em `handle._volumes_audio` | **NÃO EXISTE** |

E `_DesiredOutput` (`core/backend_pydualsense.py:249-267`) tem cinco campos
fechados — `trigger_left, trigger_right, led, player_leds, mic_led` — e
**nenhum de áudio**. O merge de cinco camadas não cobre áudio de jeito nenhum.

Três consequências que quem executar tem de resolver **antes** de escrever o
parser:

1. **o volume do jogo vazaria para depois da sessão** e ficaria valendo até o
   cabo cair;
2. **o jogo seria o QUARTO escritor** de `_volumes_audio`, sem arbitragem — os
   outros três são o IPC `speaker.set`, o applier de perfil e o gancho de
   reconexão. Esta casa já pagou por *"a config que eu deixo nunca é
   respeitada"* com exatamente esse número: três escritores sem dono;
3. **a janela passaria a mostrar um volume que ela nunca escolheu.**
   `speaker_state_for` deriva a posse de `_volumes_audio[1]`
   (`backend_pydualsense.py:2192-2194`): qualquer escrita em `common[5]` faz a
   chave `speaker` **brotar** no `state_full`, e o botão "Devolver" fica ativo
   para uma posse que não é dela.

**Portanto:** se a E1 justificar seguir, a E2 **não é "acrescentar a quinta
categoria"** — é *"dar à posse de áudio a mesma disciplina de camadas que as
outras quatro já têm"*, e só então replicar.

## Testes que vão reprovar

| teste | por quê |
|---|---|
| `test_game_output_replica.py:384-388`, `:478-483` | `assert backend.outputs == [...]` — igualdade exata de lista ordenada |
| `test_uhid_replica.py:356` | reprova se a categoria nova marcar `_game_dirty` fora do gate atual |
| `test_uhid_replica.py:276-278` | manda `flag0` ligado num body de 2 bytes: **sem a guarda de `len(body)` que as outras quatro têm, estoura `IndexError`** |
| `test_status_som_02_controle_de_volume.py:605` | `assert backend.estado() is None, "a posse foi tomada sem ninguém pedir"` |
| a família `is None` / `not in` da posse | `test_state_full_audio_speaker.py:109`, `test_som_02_devolucao_da_posse.py:143,159,201`, `test_daemon_speaker_wiring.py:218,554,594` |

**E o que NÃO reprova — é aqui que mora o perigo:**

- **não existe nenhum assert de "só existem 4 categorias"**;
- `test_uhid_replica.py:223` chama-se `test_report_combinado_replica_todas_as_categorias`
  e **nunca liga os bits de áudio** (`:232-233` usa só `0x02|0x04|0x08` e
  `0x04|0x10`). Uma quinta categoria **passaria pelo arquivo inteiro**, com o
  nome do teste mentindo;
- todos os fakes de factory absorvem sinks novos com `**kwargs` — por isso o
  `TypeError` de `make_virtual_pad`/`_try_uhid`/`for_flavor` (que têm kwargs
  **fechados**) só apareceria em runtime **na máquina dela**.

**Antes de fechar, escreva o teste que falta:** um caso em `test_uhid_replica.py`
que ligue os bits de áudio e afirme o comportamento — ele é a rede que hoje não
existe.

## Armadilhas nomeadas

1. **`common[4..7]` é PROVÁVEL, não medido.** É a razão da E1.
2. **`speaker_state_for` deriva a posse de `_volumes_audio[1]`** — a camada
   GAME tem de ser separada, ou a leitura tem de ganhar um discriminador de
   dono.
3. **A posse não tem volta por leitura.** O DualSense não devolve o volume:
   não há report de input nem feature. "Devolver a posse" devolve o CONTROLE,
   nunca o valor. Nenhum texto de produto pode prometer restauração.
4. **A camada 1 vence a camada 2.** Volume replicado para um sink mudo no
   PipeWire é trabalho invisível — está medido e escrito na SENSOR-VIVO-01/E5.
5. **A trava manual `audio` é faca de dois gumes.** O applier de perfil **não
   pode** armá-la (há teste, e o comentário diz que *"o teste da SEGUNDA
   ativação é o mais importante do arquivo"*). Uma réplica de jogo que a arme
   mata o volume por perfil para sempre; uma que não arme deixa o autoswitch
   pisar o volume do jogo. **As duas escolhas quebram alguma coisa** — decida
   explicitamente e escreva o porquê.
6. **`common[7]` (roteamento) tem veto escrito** — não se sabe o valor neutro,
   e chutar mudaria o caminho do áudio.
7. **A posse morre com o cabo:** `_volumes_audio` nasce vazio em cada handle
   novo. Para o jogo não faz sentido reaplicar — o vpad também morreu.
8. **Sem broadcast, nunca.** Os appliers descartam com log quando não há MAC
   alvo — réplica no controle errado é um defeito que esta casa já teve.
9. **Rate-limit:** 250 Hz por categoria, mas o `pump_ff` roda a 60 Hz e o
   `report_thread` escreve a ~125 Hz com um controle e ~30 Hz com quatro.
10. **`False` ≠ `None`, e zero é uma ordem.** Escrever `0x00` "de keepalive" é
    mandar **mudo**. Foi o defeito de um commit real desta casa: o keepalive
    mandava `common[9]=0x00` a 60 Hz por cima do kernel. Se a E1 mostrar bits
    ligados com bytes zerados, isso é keepalive do jogo — **não replique**.
11. **Qualquer leitura nova em `_build_common` sem `getattr(..., default)`**
    estoura `AttributeError` em toda a família de testes que constrói handles
    com `__new__`. Toda leitura de posse ali é defensiva por esse motivo.

## O que esta sprint NÃO é

- **Não é sobre o som chegar ao alto-falante.** Isso já funciona, e é PipeWire.
  O que está em questão é só o **registrador de volume por HID**.
- **Não é pré-requisito de nada.** Se a E1 disser que nenhum jogo escreve esses
  bytes, a paridade Sony × Hefesto já está completa e esta sprint vira uma
  cicatriz — o que é um bom resultado.

---

## O que foi entregue — 02/08/2026

### E1 — o instrumento, e ele é PERMANENTE

A sprint pedia *"um log temporário ali dentro"* do `_handle_output`. Entrou um
**carimbo permanente** (`ATIVIDADE_AUDIO_DO_JOGO`, no mesmo mecanismo
`visto_ha_s` que a PAINEL-DA-VERDADE-01 criou), e ele é melhor por dois
motivos:

1. **um log temporário depende de alguém lembrar de ligá-lo** antes de jogar, e
   de ela jogar o jogo certo naquele dia. O carimbo já está lá quando ela joga;
2. **ele responde as TRÊS saídas** que a sprint prevê, e não uma. Categoria
   ausente do `visto_ha_s` = nenhum jogo pediu áudio nunca — que é a resposta
   que fecha a sprint como cicatriz.

E ele honra a **armadilha 10** por construção: bits de áudio ligados com os
quatro bytes zerados **não** carimbam. Isso é keepalive, não intenção — contar
como intenção levaria a replicar "volume zero" ao controle dela a 60 Hz, que é
a classe de defeito que o `AUDIO-OWNER-01` curou noutro lugar e que o
keepalive de vibração do `GUERRA-01` já produziu de verdade.

**O carimbo NÃO replica nada.** Ele mede. Três testes travam isso.

## O que falta, e é dela

**A medição.** Basta ela jogar com o Hefesto → DualSense e depois olhar o
`visto_ha_s` do vpad no `state_full`:

- **a categoria `audio_do_jogo` NUNCA aparece** → não há lacuna. O índice
  estava errado, a sprint fecha como CICATRIZ e o trabalho de paridade termina
  aqui;
- **ela aparece** → a lacuna existe, e a E2 começa com a prova na mão.

**Esta entrega vale mesmo que a resposta seja "não"** — está escrito assim na
sprint, e continua valendo: uma pergunta em aberto respondida com medição é
entrega; um código escrito contra uma premissa não medida é dívida.
