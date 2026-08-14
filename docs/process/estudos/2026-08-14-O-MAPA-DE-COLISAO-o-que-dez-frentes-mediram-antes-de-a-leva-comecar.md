# O MAPA DE COLISÃO — o que dez frentes mediram antes de a leva começar

- **Medido em:** 14/08/2026, sobre `7673cd7`, por **dez frentes somente-leitura**
  que abriram cada `arquivo:linha` citado nos documentos da leva
  [mesa cheia](../sprints/2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md).
- **Por que existe:** duas coisas. A primeira é operacional — **dois agentes não
  podem editar o mesmo arquivo ao mesmo tempo**, e sem este mapa a leva de
  dezesseis entregas é *"uma faixa, dezesseis itens em fila"*. A segunda é mais
  cara: as frentes descobriram que **vários documentos da leva mandam consertar
  o lugar errado**, e quem seguir o documento sem conferir paga o preço.
- **Grau: MEDIDO.** Cada linha abaixo saiu de um arquivo aberto, não de um
  documento lido.

> **A REGRA QUE SAI DESTE ESTUDO, e ela vale para toda sessão futura:**
> **`arquivo:linha` em documento de processo tem meia-vida de MINUTOS quando há
> mais de uma sessão trabalhando.** Durante esta medição o `HEAD` andou **quatro
> commits em vinte minutos**. **Citar por SÍMBOLO é a única forma que
> sobrevive** — e é por isso que este documento cita por símbolo, deixando os
> números só como conferência do dia.

---

## 1. A linha de base, carimbada

**Onze de onze portões verdes**, medidos em sequência num único instante:

| portão | resultado |
|---|---|
| `pytest -q` | **9336 passed**, 1 skipped, 4 xfailed — 312,91 s |
| `ruff check src/ tests/` | All checks passed |
| `validar-acentuacao.py --all` | silencioso |
| `validar-glifos.py --all` | silencioso |
| `validar-referencias-docs.py --all` | 294 documentos sem referência morta |
| `check_anonymity.sh` | anonimato preservado |
| `check_version_consistency.py` | 12 alvos em 0.9.4.2 |
| `check_packaging_parity.sh` | 26 artefatos com dono, 0 lacuna |
| `check_test_data.sh` | dados de teste neutros |
| `mypy src/hefesto_dualsense4unix` | 173 arquivos, nenhum problema |

> **Anote isto, porque já custou uma investigação:** os validadores de
> **acentuação** e **glifos** **não imprimem nada quando passam**. Silêncio ali é
> aprovação. **Confira pelo código de saída, não pela saída.**

**A suíte esteve vermelha entre 13/08 e a manhã de 14/08, e o motivo é
instrutivo:** não era defeito de produto — era o **portão do `sudo` reprovando o
registro do próprio conserto**. O documento que registra que o README do DKMS
*parou de ensinar* a invocação proibida precisava **citá-la** para dizer que a
removeu, e o portão casa a forma sem distinguir **ensinar** de **contar que
parou de ensinar**.

---

## 2. Zero das dezesseis entregas estava no código

Confirmado por três frentes independentes, por caminhos diferentes:
`ls tests/unit | grep mesa_cheia` devolve vazio; `grep -c 'swatch\|DrawingArea'`
em `status_actions.py` devolve **0**; `grep -c
'lightbar\|accent\|swatch\|player_slot'` em `painel_no_jogo.py` devolve **0**;
e `apply_output_for` tem os dois `-> None`.

**A peneira contra o registro das doze levas não derrubou nenhum item.** É raro
nesta casa — o normal é que documentos deem como aberto o que o código já
fechou.

---

## 3. Os podres de PROMESSA — os mais caros deste estudo

**Endereço podre é chato. Promessa podre é cara**: o endereço abre, e o que ele
promete não existe. Quem seguir o documento **conserta o lugar errado e acha que
terminou.**

### 3.1 O gate de timers NÃO cobre a aba "No jogo" — e o próprio código jura que sim

O `PainelNoJogo` afirma, em comentário próprio, que *"o gate de timers da
`status_actions` conta as ocorrências de `GLib.timeout_add` no fonte — este
widget não acrescenta nenhuma, de propósito"*.

**É falso.** O gate (`tests/unit/test_status_cards.py`,
`test_gate_timers_nenhuma_ocorrencia_nova_vs_baseline`) faz `read_text()` de
**dois** arquivos: `status_actions.py` e `controller_card.py`. **`painel_no_jogo.py`
não é lido por gate nenhum.**

**Um `GLib.timeout_add` posto em `PainelNoJogo` hoje passa em 100% da suíte** —
numa casa onde *"um poller cego já custou 104% de um núcleo"*.

**Isto é a classe de defeito mais cara daqui, na sua forma mais traiçoeira: não
é a cura escrita e nunca ligada, é a cura que ANUNCIA estar ligada.**

### 3.2 "Espelho exato do `led.set`" reproduziria a mentira

A entrega 1.4 manda copiar o padrão do `led.set` do mesmo arquivo. **Mas o
`led.set` monta `aplicado_em` sem checar conexão** — ele é uma das quatro
mentiras que a onda 1 existe para matar.

**O espelho exato reproduz o defeito, e o mesmo documento proíbe o defeito numa
mordida sua.** O desenho limpo é `aplicado_em` = *escreveu de verdade*, mais um
**`guardado_em` novo** — em vez de esvaziar um campo que já tem contrato
publicado.

### 3.3 O toast do gatilho não passa por onde o documento manda olhar

O documento manda culpar o `_safe_call` do `ipc_bridge.py`. **`trigger.set` e
`trigger.reset` não passam por ali:** vão por `_call_checked`, que **descarta o
resultado**. Consertar o `_safe_call` não mudaria nada na tela.

### 3.4 A fita NUNCA foi vista numa foto desta casa

A mordida da MESA-CHEIA-01 manda *"assertar na foto que a fita tem quatro
chips"*. **Impossível com o instrumento de hoje:** o `main()` do
`retratar_abas.py` arranca o `main_notebook` do `root_box`, e o **`header_bar`
não entra em nenhuma das dez fotos**. A fita e o selo moram no `header_bar`.

**Duas entregas da onda 2 (2.1 e 2.2) têm a fita como assunto, e a
PROVA-DE-TELA-01 exige foto.**

### 3.5 Duas mordidas que não podem existir como escritas

- *"A mordida injeta um `state` com quatro controles"* (1.9): **não existe
  caminho** — `check_snd_audio_healthy` recebe **um** argumento, e o relatório
  do doctor não recebe estado.
- *"A mordida reprova hoje com o dublê honesto"* (1.2): **medido falso** —
  faltam duas pernas; o corpo do teste precisa **disparar o timer pendente**.

---

## 4. Onde duas frentes discordaram, e em quem acreditar

**O critério não foi votação — foi quem abriu o arquivo.**

| a divergência | veredicto | o desempate |
|---|---|---|
| A 1.3 edita quais arquivos? | **a UNIÃO de três**: `core/controller.py`, `core/backend_pydualsense.py` e `daemon/ipc_handlers.py` | mecânico: os dois `apply_output_for` são `-> None`; **sem mudar a base, o `mypy` do CI reprova por override incompatível**, e o `_apply_por_uniq` descarta o retorno. Quem seguir só uma frente quebra o portão 11 ou deixa o veredito parado no backend |
| `set_rumble_for` tem quantos chamadores? | **UM**, não dois | a linha citada para o co-op é **docstring**. Muda a conta de risco: a 1.6 vira o **segundo** chamador real, e o `getattr`+`callable` que a protege é obrigação, não estilo — `IController` não declara o método |
| Como a 1.9 conta o áudio? | **por linha de card**, não por ocorrência | medido ao vivo: cada card ocupa **duas** linhas em `/proc/asound/cards`, e o `re.findall` devolve **4 para dois controles**. A proposta óbvia é exatamente o modo de errar — **a régua mentindo mais que o produto**. E o denominador não é *"conectados"*: é *"no cabo"* |
| Quantas frases no singular? | **sete frases em ONZE endereços** | a frase nº 7 tem **quatro sedes vivas**. Não é contradição, é refinamento — mas muda a conta de arquivos da entrega |
| A 1.1 está feita? | **as duas estão certas** | o **trabalho** existe, o **artefato** não. Registrado para ninguém refazer sessenta minutos de leitura |

---

## 5. O contêiner dos cards da Início: o índice pede o widget que esta casa já removeu duas vezes

A entrega 2.4 propõe **`Gtk.FlowBox`** no lugar da `Gtk.Box` homogênea.

**`Gtk.FlowBox` é o widget que esta casa removeu DUAS vezes por *"Negative
content width"* sob o COSMIC** — o registro está no `main.glade` e no
`segmented_selector.py`.

**A forma aprovada é `Gtk.Grid` com colunas explícitas.** E há um comentário
mentindo sobre isso dentro do arquivo da própria 2.4: ele diz *"wrap=True:
FlowBox"* enquanto o `SegmentedSelector` monta **Grid**.

**Entrar com FlowBox é repetir um defeito já pago.**

---

## 6. Os fatos do presente que estavam errados dentro do código

**Saem por substituição** — número errado não é decisão a preservar.

`status_actions.py` e `home_actions.py` afirmam, em comentário, que o wrap
*"envolve oito das nove páginas"*. E o `retratar_abas.py` diz *"o interface.md
cita os nove"* — com uma tupla de **dez** nomes ao lado.

**Medido hoje:** `grep -c '<child type="tab">'` no `.glade` devolve **10**, e o
wrap pula só o `daemon_box` — **nove embrulhadas**. O `docs/usage/interface.md`
já diz *"dez abas"*.

> **O que NÃO se toca, e é tentador:** as frases do `theme.css` e do `app.py`
> que narram **medição datada** ficam. Corrigi-las seria apagar medição, não
> substituir fato.

---

## 7. As duas regras de execução que não são itens

**REGRA DA FOTO.** `retratar_abas.py` reescreve **as dez imagens** numa única
execução. Nenhum documento declara isso, e é a colisão mais fácil de não ver:
**nenhuma faixa regenera fotos** — a regeneração é passo de fechamento, sozinho.

**E o script SEMPRE suja `readme_inicio.png`**, mesmo sem mudança nenhuma: 2998
pixels de 2,07 M, delta máximo de **1** por canal — jitter de antialiasing. **Um
`git status` sujo depois de rodar o instrumento oficial não é sinal de que a tela
mudou.**

**REGRA DO PORTÃO.** `git add` antes de rodá-los, porque são cegos a arquivo
novo — e `scripts/gerar-contrato-ipc.py --check` é obrigatório para quem tocar o
`ipc_handlers.py`, porque o contrato publicado é **gerado** e compara conteúdo.

---

## 8. O mapa, para a próxima leva reusar

**Arquivos com mais de um dono** — são estes que decidem as faixas:

| arquivo | entregas que o editam |
|---|---|
| `daemon/ipc_handlers.py` | 1.3, 1.4, 1.6, 1.7 |
| `core/backend_pydualsense.py` | 1.3, 1.6 |
| `app/actions/home_actions.py` | 1.7, 1.8, 1.11, 2.4 |
| `app/actions/status_actions.py` | 2.1, 2.2, 2.7 |
| `app/widgets/controller_card.py` | 1.10, 2.1, 2.3, 2.7 |
| `app/widgets/painel_no_jogo.py` | 1.11, 2.3 |
| `app/actions/triggers_actions.py` | 1.2, 1.5 |
| `integrations/storm_doctor.py` | 1.9, 1.11 |

**E o mapa que ninguém tinha desenhado: os ARQUIVOS DE TESTE colidem igual.**
Dois deles são cruzados por quatro e cinco entregas de faixas diferentes, e
**têm de ser partidos** — senão duas agentes escrevem no mesmo arquivo de teste
achando que estão em faixas separadas.

**A entrega que liga tudo é a das frases no singular.** Ela sozinha toca os
arquivos de três faixas — pô-la **por último e sozinha** é o que quebra o
componente conexo e permite quatro faixas em paralelo. Os documentos já a
mandavam por último **por outro motivo** (*"a D-3 pode mudar o vocabulário"*), e
as duas razões apontam para o mesmo lugar.
