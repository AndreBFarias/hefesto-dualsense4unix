# O Bluetooth de primeira classe — índice da leva de 03/08/2026

- **Escrito em:** 03/08/2026, sobre a `v0.8.0` publicada, na branch
  `restauro/inicio-da-sessao` (HEAD `19acbeb`, com trabalho não commitado)
- **Por que esta leva existe:** ela jogou em 02/08 com os controles no
  Bluetooth e disse:

  > *"Ontem fui jogar com os 4 controles no bt. Todos os problemas antigos
  > voltaram e outros notei que foram regressões."*

- **O requisito, na frase dela:**

  > *"deixar o projeto robusto de tal forma que eu não note que estou no bt ou
  > cabo, a ideia é termos tudo funcionando via bt principalmente."*

- **O que este índice é:** o ponto de entrada. Quem retomar lê **este arquivo**
  e depois a sprint que for executar. **Nenhuma sprint desta leva precisa de
  auditoria nova para ser executada** — cada uma traz a causa-raiz com
  `arquivo:linha`, o critério de aceite, os testes que vão reprovar, as
  armadilhas nomeadas e o que **não** fazer

---

## COMECE POR AQUI

> **[As ondas — a ordem de execução](2026-08-03-ONDAS-a-ordem-de-execucao-da-leva-do-bluetooth.md)**
> é o roteiro: as 19 sprints divididas em oito ondas, com as dependências
> **provadas** (não supostas) e o caminho crítico em uma linha. Quem for
> executar lê aquele arquivo; este aqui é o catálogo.

## LEIA ISTO PRIMEIRO

**A base factual da leva inteira é o estudo
[a sessão de quatro controles e o que o journal provou](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md).**
Ele é a medição da noite dela, tirada do journal, sem tocar no daemon. Nenhuma
sprint daqui se executa sem ele aberto ao lado.

**E antes de planejar qualquer coisa, leia
[o backlog real, conferido contra o código](../estudos/2026-08-03-o-backlog-real-conferido-contra-o-codigo.md)**
— o que está aberto de fato, o que já foi entregue sem o documento dizer, os 13
itens que ficaram pelo caminho e a dívida documental inteira. É ele que impede
a próxima leva de refazer trabalho pronto.

E a base técnica continua sendo
[a referência canônica do DualSense](../../protocol/dualsense-referencia-canonica.md),
com o grau de confiança de cada linha.

### Os três números que enquadram tudo

| medida | valor | o que quer dizer |
|---|---|---|
| testes | **6829**, 1 skip, **0 vermelhos** (medido 05/08) | o vermelho do SVG do logo já não existe; era 6792/1 vermelho em 03/08 |
| erros no journal da sessão | **zero** | nada levanta exceção |
| avisos na sessão | **35** | é aqui que a noite dela está |

**O produto falha por composição de comportamentos corretos.** É por isso que
6792 testes verdes e uma noite de jogo ruim convivem — e por isso três sprints
desta leva entregam **bancada de integração**, não só correção.

### As três lições de método desta leva

1. **A ordem dos milissegundos decide a causa.** No journal, os devices morrem
   *antes* do botão PS ser solto — o botão é a reação dela à queda, não a causa.
   Inverter isso mandaria a cura para o lugar errado;
2. **Teste que mede o artefato não mede a entrega.** Três entregas declaradas
   nesta casa não estão de pé, e as três têm teste verde: o teste mede o método
   que o commit escreveu, nunca se alguém o chama;
3. **Medir antes de afirmar, inclusive contra si mesmo.** Uma hipótese desta
   leva (o casador do microfone não casaria o nome real do nó) foi **medida e
   refutada** na máquina dela. O registro da refutação está na sprint.

---

## O PLACAR — como ler, e o aviso que vem antes

> **Os índices anteriores estão defasados PARA MENOS.** A varredura de 03/08
> cruzou cada sprint com o código: **16 dos 17 itens da ONDA 1** do índice de
> 31/07 estão pagos, a divergência da `main` **zerou**, e pelo menos seis
> pendências do índice de 30/07 já foram entregues. **Planejar pelos índices
> antigos significa refazer trabalho pronto.** A recontagem é a E5 da
> `DOC-QUE-NÃO-MENTE-03`.

| # | sprint | prioridade | causa-raiz | precisa dela? |
|---|---|---|---|---|
| 1 | [BT-SURDO-01](2026-08-03-BT-SURDO-01-o-controle-parado-no-radio-nao-recebe-ordem.md) | ~~MÁXIMA~~ **MÉDIA** | premissa **refutada** (E0 medida); E2/E3/E4 seguem | **não** — já medida |
| 2 | [COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md) | ALTA | **provada**, 3 elos | não |
| 3 | [PS-TOQUE-CURTO-01](2026-08-03-PS-TOQUE-CURTO-01-o-gesto-de-religar-o-controle-abre-a-steam.md) | ALTA | **provada** | não |
| 4 | [ÁUDIO-QUE-TRANCA-01](2026-08-03-AUDIO-QUE-TRANCA-01-um-toque-no-volume-congela-a-troca-de-perfil.md) | ALTA | **provada**, 3 defeitos | só a E5 (decisão) |
| 5 | [BORDA-DE-QUEDA-01](2026-08-03-BORDA-DE-QUEDA-01-o-que-fica-para-tras-quando-um-controle-cai.md) | ALTA | **os 3 provados** — o rumble preso foi reproduzido | **não** — livre para executar |
| 6 | [POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md) | ALTA | **provada**, 4 defeitos | só a E2 (decisão) |
| 7 | [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md) | ALTA | **provada** por `grep`; defeito 2 **refutado** em 05/08 | **não** — o tato foi pago |
| 8 | [DOC-QUE-NÃO-MENTE-03](2026-08-03-DOC-QUE-NAO-MENTE-03-a-foto-vazia-a-env-negada-e-a-tag-velha.md) | MÉDIA (E5 ALTA) | **medida** | não |
| 9 | [WRAPPER-EM-TODOS-01](2026-08-03-WRAPPER-EM-TODOS-01-a-invariante-duplicado-melhor-que-zero-com-quatro.md) | **ALTA e urgente** | **provada** | confirmação em campo |
| 10 | [BT-FURO-FINO-01](2026-08-03-BT-FURO-FINO-01-os-sete-caminhos-que-so-degradam-no-radio.md) | ALTA (def. 1-2) | **provada**, 7 defeitos | não |
| 11 | [QUATRO-NA-MESA-01](2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md) | MÉDIA-ALTA | 2 provados + 2 corridas | não |

### E as cinco que nasceram da NOITE DE MEDIÇÃO (03/08, com a mão dela)

Estas cinco não vieram de leitura de código: vieram de **medir com os controles
ligados**, e duas delas **curaram defeito de verdade na mesma noite**.

| # | sprint | prioridade | estado |
|---|---|---|---|
| 12 | [LIGHTBAR-BT-CULPADO-01](2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md) | **MÁXIMA** | **CURA APLICADA** — as duas barras acenderam |
| 13 | [LED-SEM-DONO-01](2026-08-03-LED-SEM-DONO-01-o-common8-ganha-dono-e-os-textos-param-de-mentir.md) | ALTA | proposta — **é pré-requisito de aceite da 14** |
| 14 | [MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md) | ALTA | proposta — o mic **voltou** por comando, falta o ciclo de vida |
| 15 | [QUATRO-NO-RÁDIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md) | é o **destino** da leva | checklist — consome as outras |
| 16 | [DOC-QUE-NÃO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md) | ALTA | proposta — **9 mecanismos, 6 portões** |

### E o roteiro dos pedidos dela

| # | documento | o que é |
|---|---|---|
| 17 | [PEDIDOS-DELA-01](2026-08-03-PEDIDOS-DELA-01-o-roteiro-dos-seis-pedidos-da-interface.md) | **roteiro**, não execução: onde cada um dos seis pedidos mora. **Cinco dos seis já tinham dona** |
| 18 | [NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md) | a única sprint **nova** que os seis pedidos justificaram |

**A 9 é urgente por uma questão de janela:** o passo que abre o risco está na
árvore de trabalho **agora, não commitado**.

**A 12 é a única com código aplicado nesta leva.** Todas as outras são PROPOSTA.

---

## A ordem de execução, e por que ela é essa

### Antes de tudo: as medições de dez segundos — TODAS PAGAS EM 05/08

> **NÃO PEÇA ESTAS MEDIÇÕES A ELA DE NOVO.** Esta seção mandava fazer quatro,
> e em 05/08 a conferência contra as próprias sprints mostrou que **as quatro
> já estavam respondidas** — três delas desde 03/08. Um planejamento por este
> índice ia gastar o tempo dela refazendo o que já estava pago, que é o
> mecanismo exato que a `DOC-QUE-NÃO-MENTE-03` catalogou, reincidindo **neste
> arquivo**.

| medição | resultado | onde está o registro |
|---|---|---|
| **O rádio emudece?** (`BT-SURDO-01`/E0) | **REFUTADA** — ~300 Hz com o controle parado; 1.402.128 bytes em 60 s | topo da `BT-SURDO-01` |
| **"Desligar" desfaz "Rígido"?** (`ENTREGA-QUE-NÃO-LIGOU-01`/E2) | **REFUTADA** — `Rigid` *"duro"*, `Off` (`0x00`) *"soltou"* | defeito 2 da `ENTREGA-QUE-NÃO-LIGOU-01` |
| **O rumble para quando o controle sai?** (`BORDA-DE-QUEDA-01`) | **CONFIRMADA** — *"desliga sozinho e o controle branco segue vibrando"* | topo da `BORDA-DE-QUEDA-01` |
| **A lightbar por BT** (`LIGHTBAR-BT-CLAIM-01`) | **CADUCOU** — e a cura proposta lá **apaga** a barra: não execute | topo da `LIGHTBAR-BT-CLAIM-01` |

**O que cada refutação mudou:**

- a `BT-SURDO-01` perdeu a prioridade máxima e a E1; sobraram E2, E3 e E4, que
  são defeitos de código independentes da premissa;
- a `ENTREGA-QUE-NÃO-LIGOU-01` teve o defeito 2 encolhido a símbolo órfão — e a
  medição **pagou o aceite** que a `TRIGGER-CANON-01` deixou em aberto (os sete
  presets curados foram sentidos);
- a `BORDA-DE-QUEDA-01` está **livre para executar**, sem depender de mais nada.

**A medição de 05/08 rendeu um defeito novo, achado fora do roteiro:** a
[TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md)
— os dois gestos explícitos de troca de perfil limpavam a trava manual **depois**
de aplicar o perfil, e por isso aplicavam o perfil pela metade. **Cura aplicada,
com teste que morde.**

### Depois, na ordem

**1º — `BT-SURDO-01`.** Se o output realmente não sai com o controle parado,
**todas as outras sprints estão medindo sintomas de um controle surdo.** É a
única com prioridade máxima, e a única que pode mudar o diagnóstico das demais.

**2º — `COOP-QUE-NÃO-DESMONTA-01` e `PS-TOQUE-CURTO-01`.** São o ciclo que ela
viveu: o controle cai, ela segura o PS para religar, a Steam abre, o grab dá
`EBUSY`, o Jogador 2 sai. As duas juntas fecham o ciclo; separadas, cada uma
cura metade.

**3º — `ÁUDIO-QUE-TRANCA-01` e `POSSE-POR-CONTROLE-01`, nesta ordem.**
**As duas mexem no mesmo `manual_override_categories`** — a primeira no eixo das
categorias, a segunda no eixo dos controles. Executá-las juntas evita duas
migrações do mesmo campo.

**4º — `BORDA-DE-QUEDA-01`.** Depende da bancada da sprint 2 (o mesmo enumerador
com roteiro de queda).

**5º — `ENTREGA-QUE-NÃO-LIGOU-01`.** Independente. Pode ser feita a qualquer
momento, e a E5 dela (o portão contra símbolo órfão) protege todas as outras.

**6º — `DOC-QUE-NÃO-MENTE-03`.** A E5 (recontagem dos índices) vale ser feita
**antes** de tudo, se alguém for planejar a leva seguinte por índice.

**Fora de ordem, e por motivos próprios:**

- **`WRAPPER-EM-TODOS-01` (9) é a mais urgente da lista** apesar de não ser a
  mais grave: o passo `11b-bis` está na árvore não commitada, e resolver depois
  do commit custa mais. **Se for fazer uma coisa hoje, faça esta;**
- **`BT-FURO-FINO-01` (10)** vai junto com a `BT-SURDO-01` — o defeito 5 dela é
  irmão da E2 daquela (as duas fecham o `hidapi.Device` que vaza), e o defeito 2
  fecha a "hipótese 1" que a `LIGHTBAR-BT-CLAIM-01` deixou aberta;
- **`QUATRO-NA-MESA-01` (11)** depende da mesma bancada da 2 e da 5, e por isso
  vem depois delas.

---

## Se for executar UMA só

> **Atualizado em 05/08.** Esta seção mandava a `BT-SURDO-01` *"só depois da
> E0"*. **A E0 foi feita e refutou a premissa** — então vale a instrução que a
> própria seção já dava para esse caso, com uma anterior a ela.

**`RADIO-ABERTO-01`**, do adendo de 04/08, e sem discussão: é a única desta leva
inteira cujo pior caso não é um controle que não funciona.

**Depois dela, `COOP-QUE-NÃO-DESMONTA-01`** — que é o que esta seção já mandava
fazer se a E0 refutasse: causa-raiz provada em três elos, e o ciclo inteiro no
journal.

---

## O que esta leva NÃO cobre — e é decisão, não esquecimento

- **Por que o controle cai.** As oito sprints curam o que o daemon faz **em
  volta** da queda: a reação ruim, o desmonte, o que fica preso. **A queda em si
  é outra investigação** (`BT-QUE-NÃO-CAI-01`, ainda não escrita), e ela é de
  rádio, BlueZ e coexistência — não do daemon. A `BT-SDP-VAZIO-01` já cobre uma
  causa conhecida;
- **A lightbar apagada no Bluetooth.** Diagnóstico fechado e cura proposta na
  `LIGHTBAR-BT-CLAIM-01`, esperando o experimento dela. **Não foi reaberta aqui**
  — uma leitura independente confirmou o diagnóstico linha a linha e não
  acrescentou nada;
- **Os controles externos no co-op.** Eles ganham número e luz, nunca vpad
  (`coop.py:334-338` só enumera `discover_dualsense_evdevs`). **Isso é o
  desenho**, não regressão — foi assim que os quatro controles jogaram em 25/07.
  O que é defeito é a **promessa** do README, que diz a mesma frase para duas
  coisas diferentes. Vira sprint quando ela decidir se quer vpad para externos;
- **O aceite em jogo real.** Nenhuma destas fecha sem ela jogar.

---

## As quinze assimetrias que PARECEM defeito e NÃO são

Cada uma tem um defeito medido atrás. **Mexer nelas é regressão**, e quem chegar
agora vai querer "consertar" pelo menos três. A lista completa, com
`arquivo:linha` e o motivo de cada uma, está no
[estudo desta leva](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md).
As que ficam mais perto das sprints daqui:

- **`hide` falha aberto, o validador do broker falha fechado** — doutrina
  *"duplicado é melhor que zero controles"*;
- **debounce do autoswitch: 0,5 s para entrar, 12 s para sair** — com 0,5 s dos
  dois lados, o journal mostrava troca de perfil a cada 18-28 s no meio do jogo;
- **a camada do co-op fica FORA de `_desired_by_uniq`** — no mesmo slot, o revert
  restauraria o número do próprio co-op para sempre;
- **`_suppress_leds` nasce `True` e a escrita de LED da pydualsense é
  permanentemente suprimida no BT** — `LIGHTBAR-BT-ADOPT-01` e
  `LIGHTBAR-BT-NEVER-01`, pagos com a barra latcheada até o power-off;
- **o tique de LEDs externos vaza o worker de propósito** — travar o poll loop é
  pior que vazar uma thread;
- **o rumble não entra em `_desired`** — ressuscitar rumble antigo num controle
  novo seria pior;
- **`apply_output_defaults` ignora o seletor da GUI** — sem isso, ativar perfil
  com um alvo escolhido aplicava só no alvo.

---

## Como retomar do zero

1. leia este índice;
2. leia o [estudo](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md) —
   ele tem a medição, as refutações e a linha do tempo da noite dela;
3. leia a sprint que for executar: cada uma é auto-suficiente;
4. rode a linha de base:
   ```bash
   git add -A                       # os portões são cegos a arquivo novo
   .venv/bin/python -m pytest -q    # 6792 hoje; 1 vermelho conhecido (ícones)
   .venv/bin/ruff check src/ tests/
   .venv/bin/mypy src/hefesto_dualsense4unix
   ```
5. para olhar a interface: **`.venv/bin/python scripts/gui-captura/retratar_abas.py <destino>`**
   — o interpretador **importa** (ver `DOC-QUE-NÃO-MENTE-03`, defeito 1), e o
   destino evita sobrescrever a documentação;
6. a regra de aceite de interface continua sendo a
   [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
   foto antes e depois, e o olho dela no fim.

---

## O caminho até a 1.0, na leitura de hoje

Esta leva não entrega a 1.0 — **ela remove o que impede de chamá-la assim.** O
que falta, depois destas oito:

1. **a queda do Bluetooth em si** (`BT-QUE-NÃO-CAI-01`);
2. **a lightbar por BT** (`LIGHTBAR-BT-CLAIM-01`, esperando dez segundos dela);
3. **o aceite em jogo real** dos sete presets de gatilho e dos nove recursos;
4. **a validação em mais de uma máquina** — hoje é uma só, e o README já o diz;
5. **a bancada de integração** que as sprints 2, 5 e 6 começam a construir. Sem
   ela, o projeto continua com 6792 testes verdes e noites ruins.

---

## Adendo de 04/08/2026 — o que a madrugada acrescentou

Quatro sprints novas e um estudo, nascidos da sessão ao vivo com ela. As três
primeiras são **curas já aplicadas** e estão aqui pelo registro; as quatro
sprints abaixo estão **abertas**.

### Curado nesta madrugada (com teste que morde)

| defeito | onde estava |
|---|---|
| o seletor "Sons do jogo" **silenciava** o alto-falante | `speaker_set(rota=)` sem `volume` nem `uniq` |
| pedir som no controle com o sink **mudo** produzia silêncio calado | ninguém agia sobre a camada 1 do PipeWire |
| o daemon **não morria** e custava 90 s de SIGKILL | `report_thread.join()` do upstream, sem teto, sobre um `read` bloqueante |
| a instalação podia terminar com cura desarmada | o `install.sh` agora roda o `doctor.sh` no fim, por padrão |

O relato inteiro, com o que eu errei no caminho, está em
[A noite em que o som do controle voltou](../estudos/2026-08-04-a-noite-em-que-o-som-do-controle-voltou.md).

### Abertas

| sprint | do que trata | onde entra nas ondas |
|---|---|---|
| [RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md) | 44.718 frames L2CAP corrompidos em 28 min; **duas hipóteses refutadas por medição**, e o experimento que decide **não precisa dela** | **antes** da onda do rádio — é a queda em cascata |
| [BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md) | **CURADA** — o `bt-agent` segurava o restart do BlueZ por 90 s a cada crash; é a explicação do *"tá pedindo senha"* | registro |
| [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md) | **CURADA** — o snapshot de bonds falhava **só no crash**, por sandbox herdado | registro |
| [SUITE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md) | a suíte cria uinput real e escreve linhas de produção no journal | **antes de tudo** — contamina o instrumento de diagnóstico |
| [DROPIN-AMBIGUO-01](2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md) | a ausência do drop-in 51 é lida como escolha dela | onda dos portões |
| [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md) | o 8BitDo tem dois MACs e come um slot de co-op | junto de `QUATRO-NO-RADIO-01` |

**A ordem que eu recomendo**, e a razão de cada uma:

1. **SUITE-QUE-SUJA-O-JORNAL-01** primeiro. Enquanto a suíte escrever no
   journal, toda medição desta casa é suspeita — e o método desta casa é medir
   pelo journal;
2. **RADIO-BOMBARDEADO-01** em seguida, porque ela **já sabe medir** (M1-M4 são
   quatro janelas de 15 minutos) e porque é o defeito que ela sente jogando;
3. **IDENTIDADE-DUPLA-01** depois, que se apoia numa medição de 2 minutos do
   item anterior;
4. **DROPIN-AMBIGUO-01** por último das quatro — é código de portão, não toca no
   rádio, e a conferência final do install já fechou o caso prático mais comum.

### O que a auditoria de 04/08 corrigiu

Oito agentes conferiram estas sprints contra o código e o journal, com um
critério só: *um Claude sem nenhum contexto abre o arquivo e começa a
trabalhar?* O que eles acharam, e que já está aplicado:

1. **A `RADIO-BOMBARDEADO-01` mandava 50 minutos de bancada para testar uma
   hipótese que o journal já tinha matado.** Os 26.884 erros de CRC do clone
   ocorreram entre 23:51:44 e 23:58:07 — janela com **zero** frames
   corrompidos; e a janela da tempestade teve **zero** erros de CRC. Os dois
   fenômenos são **disjuntos no tempo**;
2. **a refutação da hipótese topológica era inválida** — a "janela de controle"
   não continha o objeto testado (o que estava no cabo era um `054c:05c4`
   full-speed, sem endpoint isócrono). A hipótese voltou à mesa, e a janela de
   controle **válida** (19:35→20:04) sugere um refinamento: não é enumerar, é
   **streamar**;
3. **duas causas-raiz medidas e curadas nesta madrugada não tinham documento
   nenhum** — viviam só em comentário de arquivo de unit. Viraram as duas
   sprints acima. É o mecanismo "entregue e sem documento" que a
   `DOC-QUE-NAO-MENTE-03` catalogou, reincidindo;
4. **os bloqueios de medição manual não estavam no topo dos arquivos.** Agora
   estão, em destaque, com o que dá para fazer **sem ela** em cada caso — regra
   dela: *"as que precisam de testes manuais só podem ser executadas com os
   testes de eliminação"*.

---

## Adendo da MADRUGADA de 04/08 — a noite em que o Bluetooth caiu de verdade

Ela jogou, os quatro controles caíram, o `bluetoothd` fez core dump **três
vezes** e comeu **todos** os pareamentos. E o produto, que tinha o remédio na
mão, não o deu.

### O que foi CURADO na hora

| defeito | mecanismo |
|---|---|
| o `bt-agent` ficava `failed` e **o BlueZ parava de aceitar conexão entrante** | o `SendSIGKILL=yes` da cura das 00:09 marcava a unit como falha; `SuccessExitStatus=SIGKILL` conserta. Regressão MINHA, e ela a apontou duas horas antes do meu diagnóstico |
| o Pro Controller *"conectava, demorava e morria"* | estava com **`sniff`** — a cura de 23/07 desta casa, apagada pelos três reinícios do `bluetoothd`. Reaplicado o `bt_active_mode.sh` |

### As quatro sprints novas

| sprint | do que trata | quando executar |
|---|---|---|
| [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md) | **o `install.sh` instala, por padrão, a combinação que anula a autenticação do Bluetooth** — e o caminho termina em injeção de teclas | **PRIMEIRO, e sem discussão** |
| [BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md) | ninguém aciona a restauração; a poda apaga o snapshot bom; o restaurador sobrescreve chave nova com velha | logo depois |
| [CURA-QUE-FERE-01](2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md) | verificar que o campo entrou **não é** verificar que a cura funciona | em paralelo — é teste e portão |
| [SUITE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md) | a suíte cria uinput real e escreve no journal do sistema | antes de qualquer medição nova |

### Por que a `RADIO-ABERTO-01` vem primeiro

Ela é a única desta leva inteira cujo pior caso **não é um controle que não
funciona** — é alguém ao alcance do rádio digitando na máquina de quem instalou
isto. E ela saiu de uma auditoria que investigava **outra coisa**: nenhum dos
sete agentes tinha segurança como tarefa; um deles tinha a **lente**.

### A prova que fecha a BONDS-QUE-SOBREVIVEM-01

Medido às 03:04 de 04/08: **o snapshot das 23:51 com os quatro controles — o
mesmo de onde a restauração daquela noite saiu — já tinha sido podado.** Uma
hora depois de salvar o Bluetooth dela, o registro que o salvou não existia
mais. E seis dos doze lugares do acervo estavam ocupados por snapshots de 1 ou
2 bonds.

Não é hipótese. É o mecanismo destruindo a própria prova, com os dados dela.
