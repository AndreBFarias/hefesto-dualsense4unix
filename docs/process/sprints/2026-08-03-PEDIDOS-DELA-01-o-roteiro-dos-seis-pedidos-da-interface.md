# PEDIDOS-DELA-01 — o roteiro dos seis pedidos da interface

- **Status:** ROTEIRO, escrito em 03/08/2026. **Não é sprint de execução** — é o
  documento que diz **onde cada pedido dela mora**
- **Por que existe:** ela pediu, literal — *"materializa isso em sprints também
  e **verifica se já temos sprints anteriores criadas pra isso e não executadas
  ainda (melhoramos se já existir)**, caso contrário criamos as novas"*
- **Método:** quatro agentes varreram as ~90 sprints e o código, com refutação
  adversarial. **Cinco dos seis pedidos já têm dona.** Só um justificou sprint
  nova
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)

---

## O roteiro, em uma tabela

| # | pedido dela | destino | por quê |
|---|---|---|---|
| 1 | co-op sempre ativo, tirar o botão | **melhorar `AUTO-01`** (25/07, ABERTA) | é a sprint do "um clique em vez de dez" |
| 2 | remover "Ouvir no controle" | **melhorar `SOM-ROTA-01`** (01/08, E2/E4/E5 abertas) + **adotar o ID órfão `SOM-CANAL-01`** | é a sprint da rota de som |
| 3 | áudio funcionar no BT | **melhorar `SOM-02`** (alto-falante) e **`MIC-BT-01`** (microfone) | as duas já têm as caixas certas, vazias |
| 4 | o nome do 8BitDo não é "Sony" | **SPRINT NOVA: `NOME-HONESTO-01`** | `grep` por `friendly_type\|brand_of` nas sprints devolve **zero** |
| 5 | máscara do externo (Pro / PS4) | **melhorar `MÁSCARA-01`** (25/07, ABERTA) | **zero código nesta leva** — só o documento fica correto |
| 6 | garantir o modo PS4 do 8BitDo | **distribuir em 3 sprints existentes** | `grep -ril 8bitdo` devolve **16** arquivos |

---

## Pedido 1 — o co-op perde o interruptor

**Melhora a `AUTO-01`** (`2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md`), com o
item **AUTO-01.2-b (03/08)**.

**A decisão dela, literal:** *"quando uma pessoa conecta dois controles não é q
ela quer que os 2 virem somente input pra um controle reconhecido. Significa
sempre que ela quer jogar com outra pessoa."*

**E o cabeçalho de `app/actions/home_actions.py:8-9` já dizia isso:** *"LEIGO-01:
não há mais toggle de co-op — cada controle é um jogador, sempre; a aba só
INFORMA quantos"*. **A decisão já tinha sido tomada e o botão sobreviveu.**

### As sete entregas, na ordem — e a ordem é a entrega

1. **o piso vira ligado** — `daemon/lifecycle.py:145` (`coop_enabled: bool = False`)
   → `True`, com nota datada dizendo que o motivo escrito ("reserva/troca de
   controle para a mesma pessoa") **caducou por decisão dela**;
   **Aceite:** `DaemonConfig()` recém-construído, **sem `run()`**, tem
   `coop_enabled is True`.
   > **Armadilha nomeada:** `lifecycle.py:651-656` já força `True` no boot — um
   > teste de boot **passa com a cura arrancada**. O aceite tem de ser sobre o
   > dataclass.
2. **`coop.set {enabled:false}` recusa em voz alta** — mantendo a **forma** do
   retorno (`cli/cmd_coop.py` lê `result["players"]`);
3. **a persistência do opt-out vira lápide**, não borracha —
   `utils/session.py:529` (`coop_disabled.flag`). **Não** escrever varredura
   nova: o arquivo **não existe** no disco dela;
4. **perfil deixa de governar** (`lifecycle.py:1984-1985`) — o campo continua
   sendo lido para não quebrar arquivo antigo;
5. **o gesto perdido ganha dono ANTES de o botão sair** — `lifecycle.py:1315`
   (`coop.sync(force=True)`) é o **único** ciclo cheio fora de hotplug. O botão
   "Renumerar agora" vira **"Reconciliar jogadores"**;
6. **só então o botão sai** (`gui/main.glade:212-240` e os handlers);
   **Aceite:** `'id="home_coop_prep_btn"' not in fonte` — **não**
   `grep -ci coop main.glade == 0`, que proibiria a própria lápide;
7. **a frase entra no lugar** — e **a contagem vem do `state_full`**
   (`ipc_handlers.py:1782`), **não** de `status_actions.py:1923`, que soma um
   cache assíncrono da **outra aba** e reintroduziria o defeito que a
   `CONTAGEM-01` denunciou.

> **A frase não pode dizer "4 jogadores"** com 2 do Hefesto + 2 externos:
> externo **nunca** vira jogador de co-op.

**O que NÃO fazer:** não tocar `CoopManager.disable()` (é a suspensão por Steam
Input); **não prometer que isto cura o P2 de dois segundos** — com o botão fora,
o gesto de recuperação some, o que **sobe** a prioridade da
[COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md).

**Mão dela:** a `PROVA-DE-TELA-01` vem **depois** da cura do retratador — a aba
Início é 100% código, e o frame que sai é o **único conteúdo Glade** dela.

---

## Pedido 2 — o botão "Ouvir no controle" sai

**Melhora a `SOM-ROTA-01`** com a entrega **E6**, e nela **adota o ID órfão
`SOM-CANAL-01`** (19 citações no código, zero documento).

### A ordem é a entrega, e inverter mata a camada 1 em silêncio

1. **migrar a criação preguiçosa** de `RotaDeSaida` para
   `_aplicar_rota_do_sistema`. Hoje a **única** instanciação está em
   `status_actions.py:535-544`, dentro de uma função que **retorna cedo quando o
   botão não existe no Glade**;
   > **Tirar o botão antes disto mata a camada 1 sem avisar** — e
   > `test_status_som_04_rota.py:586` **passa verde nesse estado**, porque só
   > verifica que não quebra.
2. **o clique para de confirmar o que não fez** — `controller_card.py:3010-3013`:
   o `ok` é o **byte**, e o retorno da camada 1 é engolido;
3. **o `uniq` do seletor** (pode ir sozinho, antes de tudo):
   `speaker_set(rota=rota)` **sem `uniq`** contra os três irmãos que o passam.
   **Com dois controles, clicar no card 2 escreve no controle 1** — *o teste
   reprova hoje, antes da entrega*;
4. **só então o botão sai**;
5. **lápides obrigatórias** — `test_status_som_04_rota.py` contém a medição de
   geometria que **é o próprio aceite** de não-regressão.

---

## Pedido 3 — o áudio por Bluetooth

Três donos distintos. **Uma sprint nova só se necessário; hoje, nenhuma.**

**3a — a tela para de prometer som por BT** → **`SOM-02`**, entrega **E6**.
Paga a armadilha 11 que a própria sprint escreveu: *"ou o bloco diz isso, ou não
deve prometer"*. O `CANAL_TODO_O_PC` fica **insensível** por BT, com a razão na
dica. Âncora em `controller_card.py:3528` (`_update_speaker`), que recebe o
`transport` — **não** em código de montagem.

> **Nota datada obrigatória:** `2026-08-01-INDICE:99` diz *"alto-falante
> FUNCIONA"* — foi medido **no cabo**.

**3b — ligar a ponte de mic pela tela** → **`MIC-BT-01`**, caixas 2, 3 e 4, que
são *"o pedido dela ao pé da letra"*.

> **Armadilha grave, e ela é de reentrância:** `lifecycle.py:2759-2790` cria
> instância nova a cada chamada e **sobrescreve `self._bt_mic_subsystem` sem
> parar a anterior** — duas threads, dois `module-pipe-source`, **dois
> escritores de `0x32` no mesmo link**. Só o `_stop_bt_mic` é idempotente.

**3c — o desmute com dono** → já é a
[MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md).

---

## Pedido 4 — SPRINT NOVA: `NOME-HONESTO-01`

A única que justificou documento próprio. Ver
[NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md).

**E a `IDENT-01` NÃO é a dona deste pedido:** "apelido" ali significa **vincular
dois endereços**, não nome legível.

---

## Pedido 5 — a máscara do externo

**Melhora a `MÁSCARA-01`, e nesta leva é ZERO CÓDIGO** — só o documento fica
correto. Quatro fatos que a sprint não sabia:

1. **impedimento novo:** por cabo o externo **não tem identidade estável** —
   `external_identity.py:270-322` cai em `dev:<instância HID>`, que **incrementa
   a cada replug**. A dependência sobre a `IDENT-01` é mais dura do que ela supunha;
2. **`_IGNORE_VALUE` é um par cravado** (`launch_env.py:83`): esconder
   `0x054c/0x05c4` para mascarar o clone esconderia **todo DualShock4 genuíno**;
3. **não existe sabor `pro`** — `uinput_gamepad.py:114-136` tem `dualsense` e
   `xbox`, e só. As opções honestas são **"como ele mesmo"**, **"como
   DualSense"** e **"como Xbox 360"**;
4. **mascarar custa o giroscópio** — `physical_report_reader.py:295` encaminha o
   motion como **cópia byte a byte** do DualSense; mascarar um Pro exige escrever
   um **tradutor**, não ligar um caminho.

---

## Pedido 6 — o 8BitDo e o modo PS4

**Nenhuma sprint nova.** Distribuído em três, e o primeiro item é o **mais barato
do plano inteiro**.

**6.1 — documento, paga hoje, zero código.** E corrige a premissa:

> **O modo é do CONTROLE, não do transporte.** `troubleshooting-8bitdo.md:29`
> registra **Switch por cabo** como PROVADO estável. **O cabo não troca modo
> nenhum.**

E fecha três "não medidos" que a medição de 03/08 respondeu de graça: o ramo
`ds4_synthetic_mac`, o probe completando, e a nota ³ (*"pergunta em aberto —
ninguém mediu"*) — **há giroscópio no modo PS4 no cabo, sem calibração**.

**Falta o combo do modo PS4** — não está no repositório, e **não se inventa**: é
gesto dela.

**6.2 — o `doctor` para de mandá-la para o modo que mata.**
`scripts/doctor.sh:1718` imprime *"troque o modo (Switch) ou use no cabo"* — **o
inverso da cura medida em 25/07**. E `test_plataforma_wiring.py:187` **trava a
string em verde**. Dono: `DOC-VERDADE-02`.

**6.3 — o aviso antes da queda** → `CONTAGEM-E-COOP-01`, que é a dona do
cabeçalho onde o aviso deve morar. **Quatro sinais, não três:** OUI `e417d8` +
`057e:2009` + bus BT + **presença de um Nintendo-class genuíno** — o gatilho
medido do crash é a reconexão de **dois** Nintendo-class em poucos segundos.

---

## O que este roteiro prova sobre o processo

**Cinco dos seis pedidos já tinham dona**, e três delas dizem `ABERTA` com parte
do código **de pé**. Sem esta varredura, a leva teria criado seis sprints novas e
duplicado trabalho — que é exatamente o que ela pediu para evitar.

E o padrão que aparece: **a decisão certa já tinha sido tomada** (o co-op sem
interruptor está escrito no cabeçalho do `home_actions.py` desde a LEIGO-01), **e
o artefato sobreviveu à decisão.** É a mesma família do `0x08` e do `common[8]` —
código que ficou depois de o motivo morrer.
