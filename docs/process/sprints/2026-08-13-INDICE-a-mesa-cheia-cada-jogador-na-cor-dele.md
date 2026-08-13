# ÍNDICE — as ondas da mesa cheia: cada jogador na cor dele

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Reescrito no mesmo dia**, depois do **censo das dez abas** — dez agentes
  mediram a janela aba por aba, e o censo mudou o mapa que a primeira versão
  deste índice desenhou. As correções estão na seção 2, cada uma com o endereço
  que a sustenta.
- **Nasceu de**, olhando a aba Gatilhos com um controle só na mesa:
  *"aqui só tenho o player 1, mas caso os outros controles estivessem
  instalados, cada seleção deles com cada estilo ficaria marcado na cor do
  lightbar deles, igual jogo quando selecionamos um personagem, aí cada player
  poderia escolher o seu estilo de gatilho. isso valeria pra todas as abas."*
- **E da correção dela, que foi o que mandou medir:** *"todas as abas vão ter
  problemas nesse sentido, acho que a aba status é outra. deve ter mais."*
  **Ela estava certa nas três afirmações** — a contagem está na seção 2.
- **Grau:** **PLANO.** Nenhuma linha desta leva virou código. O que está
  **MEDIDO** aqui é o levantamento: cada `caminho:linha` abaixo foi aberto na
  árvore de 13/08/2026. O que a tela vai parecer é proposta, e a palavra é dela
  ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).

## Como ler este índice

**As ondas são separadas por quem precisa estar presente**, não por assunto —
é a forma que a casa fixou em
[31/07](2026-07-31-INDICE-as-ondas-depois-da-auditoria.md) e a única divisão que
muda o que dá para fazer hoje à noite e o que espera ela sentar na frente da
tela.

- **ONDA 1 — o que eu faço sozinha, hoje.** Zero pixel novo. É a onda da
  **verdade**: a janela para de afirmar o que não aconteceu.
- **ONDA 2 — precisa do olho dela.** É a onda em que **os quatro jogadores
  aparecem**.
- **ONDA 3 — o que trava esperando decisão dela.** São perguntas, não tarefas.
  **A D-1 é a primeira, e o motivo está na seção 5.**

**Uma sprint pode aparecer em duas ondas**, com a entrega numerada — é o caso da
07 (medir na 1, colorir na 2) e da 05 (o defeito na 1, o mecanismo depois da
D-4). Isso não é desorganização: é o critério "quem precisa estar presente"
aplicado a cada entrega em vez de a cada documento.

---

## 1. A tradução, para ela conferir

Eu li o pedido dela como quatro afirmações. Se alguma estiver errada, a leva
inteira muda de forma — por isso elas vêm primeiro:

1. A tela mostra os **quatro jogadores ao mesmo tempo**, não um alvo por vez.
2. **A escolha de cada um fica marcada na cor do lightbar dele.**
3. Cada jogador tem **o seu** gatilho, a sua luz, o seu rumble — e a tela mostra
   os quatro estados **de uma vez**, em vez de trocar de alvo e perder de vista
   os outros.
4. Vale para **todas as abas**.

**A quarta é a que precisa de qualificação, e o censo a afiou.** *"Marca"* eram
duas coisas o tempo todo, e elas têm alcances muito diferentes:

| a marca | o que ela afirma | onde cabe |
|---|---|---|
| **a COR por jogador** (o swatch) | *"este pedaço da tela é do jogador N, e a barra dele está desta cor"* — é **identidade** | **NOVE abas de dez.** Só a Sistema fica de fora, porque ali o alvo é systemd/Steam/PipeWire, e mesmo ela ganha **contagem** no lugar do singular |
| **as QUATRO ESCOLHAS** (a marca `■N` num botão) | *"o jogador N escolheu esta opção"* — é **ajuste** | **TRÊS abas:** Gatilhos, Lightbar e Rumble. Nas outras o ajuste é da sessão ou do perfil, e quatro marcas ali seriam mentira |

**A primeira versão deste índice tratou as duas como uma só** e concluiu "três
abas de dez". A conclusão estava certa para a escolha e **errada para a cor** —
e é a diferença entre atender e não atender o *"isso valeria pra todas as
abas"*.

**Isto continua sendo decisão dela.** Se ela quiser escolha marcada nas sete
restantes, o preço não é tela: é reabrir decisões que ela mesma tomou em 10/08.
A [MESA-CHEIA-06](2026-08-13-MESA-CHEIA-06-o-portao-contra-a-marca-que-mente.md)
existe para que a leva não invente esse alcance por descuido.

---

## 2. O que o censo corrigiu neste índice

Cinco correções, cada uma com o endereço. **Onde eu tinha um fato errado, ele foi
SUBSTITUÍDO** — número errado não é decisão a preservar. Onde havia decisão
medida, ela ficou com a nota datada.

### 2.1 São DEZ abas, e a terceira nunca foi medida

`main_notebook` (`src/hefesto_dualsense4unix/gui/main.glade:212`) tem dez
páginas. A terceira é a **"No jogo"** — `tab_no_jogo_box`, `gui/main.glade:678`,
rótulo em `:685` — montada por `install_no_jogo_tab`
(`app/actions/status_actions.py:541`).

**Nenhum dos agentes a mediu, porque a lista que eu entreguei tinha nove nomes.**
É lacuna declarada, não achado. Virou a
[MESA-CHEIA-07](2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md), e é
o primeiro item da onda 1: medir antes de planejar.

### 2.2 A aba Status não é problema — é o MOLDE, e a casa já o copiou uma vez

Ela disse *"acho que a aba status é outra"*. É outra, e por um motivo mais forte
do que ela disse: **a Status já resolveu o problema inteiro.** Um card por
controle, e o card **não tem alvo a escolher — ele É o alvo**, porque carrega o
próprio MAC dentro do widget. A cor vem do `state_full`, não da paleta.

**E a "No jogo" é a cópia inacabada:** ela reusa `titulo_do_card`
(`app/widgets/painel_no_jogo.py:468`, com o import em `:84`), usa as mesmas
chaves (`_status_card_keys_for` + `zip(..., strict=True)`,
`app/actions/status_actions.py:766` e `:1095`), e o cabeçalho do módulo
(`:1-46`) promete *"Este módulo **chama** aquela função; não reimplementa nem uma
linha dela."* — e `grep -c 'lightbar\|accent\|swatch\|player_slot'` no arquivo de
667 linhas devolve **0**.

```
   A Status  →  título + swatch colorido + accent + o MAC dentro do widget
   No jogo   →  título                                          (e mais nada)
                        ↑
                 a casa copiou o molde uma vez
                 e deixou a cor para trás
```

**Consequência operacional, e ela barateia a leva:** isto não é "inventar um
desenho de quatro jogadores". É **terminar uma cópia que a casa já começou**, e
repeti-la nas demais.

> **ATENÇÃO DE MÉTODO, medida em 13/08, e ela é a armadilha mais concreta desta
> leva: DOIS arquivos citados aqui estão se movendo HOJE.**
>
> - **`app/widgets/controller_card.py`** está no índice com **190 linhas a mais**
>   que o commit. Por isso este índice cita as peças do card **por símbolo**
>   (`titulo_do_card`, `rotulo_lightbar`, `accent_do_card`, `_on_draw_swatch`) e
>   não por número de linha.
> - **`src/hefesto_dualsense4unix/gui/main.glade`** ganhou **27 linhas** a partir
>   de `:2153` enquanto esta página estava sendo escrita. **Toda citação ao
>   `.glade` acima de 2153 foi refeita depois disso** e vale para a árvore de
>   13/08 às 20h; abaixo de 2153 nada se moveu.
>
> Regra que sai daí, e que serve à próxima leva: **arquivo em edição se cita por
> símbolo, não por linha.** Endereço podre não é erro de digitação — é uma
> afirmação que deixou de abrir no que promete.

### 2.3 A mentira que vale por SEIS abas não é de aba nenhuma

A fita *"Ajustes vão para: …"* (`app/actions/status_actions.py:1497`) e o selo
*"Editando: {alvo}"* (`:1858`) moram no `header_bar`
(`gui/main.glade:136`), **acima** do notebook, e **nunca sabem em que aba
estão**.

A prova é de contagem: `_set_target_strip_visible`
(`app/actions/status_actions.py:1673`) tem **exatamente três chamadores** —
`:2094`, `:2177` e `:2505` — e os três decidem por **contagem de controles** ou
por **daemon offline**. O `_on_notebook_switch_page` (`app/app.py:957`) **não a
menciona**. Não existe um único `if` de aba em todo o caminho.

**A fita é VERDADE em 4 abas** (Status, Gatilhos, Lightbar, Rumble em parte) e
**FALSA em 6** (Início, No jogo, Perfis, Sistema, Emulação, Navegação). A
ressalva existe e mora onde ninguém lê: o tooltip
(`app/actions/status_actions.py:1484-1487`) enumera o escopo real — *"Controle
alvo das ações (lightbar, gatilhos, LEDs, rumble)"* —, a lista está **certa**, e
é tooltip.

Virou a
[MESA-CHEIA-10](2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md),
e ela anda colada na 01: **pintar uma promessa falsa a torna mais convincente,
não mais verdadeira.**

### 2.4 Três defeitos que ninguém tinha escrito

Nenhum destes estava em lugar nenhum do repositório antes de 13/08:

1. **O rumble fixado MIGRA de controle quando o alvo muda.** `rumble_active` é
   uma tupla global (`daemon/lifecycle.py:195`, escrita em
   `daemon/ipc_handlers.py:3248`), e o `reassert_rumble` a 5 Hz a relê
   (`daemon/subsystems/rumble.py:150`) e chama `set_rumble` (`:176`), que resolve
   o alvo pelo ponteiro **de agora**
   (`core/backend_pydualsense.py:2336-2338`). Ela fixa 160/220 no Controle 2,
   troca o seletor para o 3 por outro motivo, e 200 ms depois o **3** leva o
   valor do **2**.
2. **O comando do PC troca de dono em silêncio.** Se o primário cai,
   `_recompute_primary` (`core/backend_pydualsense.py:1934`) promove o próximo
   mais antigo (`:1944`), re-atrela o evdev (`:1955`) e escreve um `logger.info`
   que ninguém lê (`:1969`).
3. **O "Desligar" dos gatilhos RE-ARMA a trava 300 ms depois** — a cura **R-19**
   está desfeita, e **o teste que a protege não morde**. Virou a
   [MESA-CHEIA-08](2026-08-13-MESA-CHEIA-08-o-desligar-que-re-arma-a-trava.md),
   com a cadeia degrau a degrau.

### 2.5 Eu errei sobre o rumble, e o erro estava neste índice

> **NOTA DATADA (13/08/2026).** A primeira versão desta página afirmava, na
> seção *"O buraco central"*, que *"`rumble_set` **não aceita `uniq`** — é a
> única função de saída do arquivo que não aceita"*, e que com "Sony 2"
> escolhido a aba Rumble **vibrava os quatro**. **As duas afirmações são
> falsas**, e o texto foi substituído porque um número errado ao lado do certo
> obriga a próxima pessoa a escolher entre dois.

| a afirmação | veredicto | a evidência |
|---|---|---|
| *"o `OutputSpec` não tem campo de rumble"* | **certa e IRRELEVANTE** | `core/controller.py:63-67` tem cinco campos e nenhum de rumble. Mas rumble é **transitório** e nunca entra no desejado — pôr campo ali seria consertar o lugar errado |
| *"então `rumble.set` não consegue mirar por MAC"* | **ERRADA** | ele **mira**. O endereço viaja por fora da chamada: o chip do cabeçalho arma `_output_target_key` (`app/actions/status_actions.py:2194` → `daemon/ipc_handlers.py:3152`) e `_for_each_com_key` o honra (`core/backend_pydualsense.py:2336-2338`). Feio, e funciona |
| *"`rumble_set` é a única saída do bridge sem `uniq`"* | **ERRADA** | contado por AST em 13/08: **as seis funções de rumble** não aceitam (`:398`, `:409`, `:415`, `:421`, `:435`, `:446`), mais o invólucro fino `trigger_set` (`:342`). E dois nomes da lista antiga não existem: `led_player_set` chama-se `player_leds_set` (`:511`), e o que aceita `uniq` é o `trigger_set_checked` (`:327`) |
| *"travaria a aba Rumble e liberaria as outras"* | **ERRADA, e é o erro caro** | **nove das dez abas têm trabalho**, e **zero** delas está travada pelo `OutputSpec` |

**O que trava de verdade é a INTENSIDADE.** O mesmo clique grava a política no
rascunho **da peça** (`app/actions/rumble_actions.py:429` → `:551`) e manda ao
daemon um `rumble.policy_set` **sem endereço** (`:433` →
`daemon/ipc_handlers.py:3314-3336`, escrevendo `daemon_cfg.rumble_policy` em
`:3329`) — enquanto o selo diz *"Editando: Controle 2"*. **É a pior mentira das
dez abas**, e a razão é precisa: é a única em que o alvo **existe**, a tela o
**afirma**, e o código o **desobedece**.

---

# ONDA 1 — o que eu faço sozinha, hoje

Nada aqui precisa dela na frente da tela. **Zero pixel novo.** Tudo prova sem
aparelho, com `state_full` de mentira e `Gtk.OffscreenWindow`, sem tocar no
daemon vivo dela.

| # | Entrega | Sprint | Por que aqui | Custo |
|---|---|---|---|---|
| 1.1 | **Medir a aba "No jogo"** — a décima, que nenhum agente viu | [MESA-CHEIA-07/E1](2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md) | planejar a leva sem ela é planejar contra um mapa incompleto | 60 min |
| 1.2 | **O "Desligar" que RE-ARMA a trava**, e o dublê que precisa passar a emitir | [MESA-CHEIA-08](2026-08-13-MESA-CHEIA-08-o-desligar-que-re-arma-a-trava.md) | é regressão de cura, e ela sente como *"a config que eu deixo não fica"* | 40 min |
| 1.3 | **`apply_output_for` para de ser silencioso** | [MESA-CHEIA-09/E1](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md) | é a raiz das quatro mentiras de "aplicado" | 45 min |
| 1.4 | **`trigger.set`/`trigger.reset` devolvem `aplicado_em`**, como o `led.set` do mesmo arquivo já devolve | [MESA-CHEIA-09/E2](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md) | é copiar o padrão do arquivo ao lado (`daemon/ipc_handlers.py:1061`) | 30 min |
| 1.5 | **Os toasts honestos da Lightbar** — alvo desconectado e co-op ligado | [MESA-CHEIA-09/E3](2026-08-13-MESA-CHEIA-09-aplicado-sem-byte-nenhum.md) | mata a tela que se contradiz sozinha (`app/actions/lightbar_actions.py:986` × `:163-167`) | 60 min |
| 1.6 | **O rumble deixa de MIGRAR de dono** | [MESA-CHEIA-05/E0](2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md) | é conserto de defeito sob **qualquer** resposta à D-4 — não espera decisão | ≈ 2 h |
| 1.7 | **`native_bt_fragil` por controle** | [MESA-CHEIA-11/E1](2026-08-13-MESA-CHEIA-11-a-janela-conta-um-quando-sao-quatro.md) | falso negativo: com o P1 no cabo, o aviso cala para os três frágeis | 55 min |
| 1.8 | **O banner do co-op nomeia o jogador** | [MESA-CHEIA-11/E2](2026-08-13-MESA-CHEIA-11-a-janela-conta-um-quando-sao-quatro.md) | o daemon já sabe qual (`daemon/subsystems/gamepad.py:1206`); a janela diz *"um dos jogadores"* | 20 min |
| 1.9 | **`check_snd_audio_healthy` conta em vez de `re.search`** | [MESA-CHEIA-11/E3](2026-08-13-MESA-CHEIA-11-a-janela-conta-um-quando-sao-quatro.md) | *"áudio presente em 3 de 4"* com zero aparelho — o `cards_text` já é injetável | 60 min |
| 1.10 | **Guarda do card sem MAC na Status** — desligar o bloco de áudio quando o card não tem endereço, e dizer por quê | *(neste índice, §7)* | hoje escreve no **primário** com o título de outro controle | 30 min |
| 1.11 | **As oito frases no singular** | [MESA-CHEIA-11/E4](2026-08-13-MESA-CHEIA-11-a-janela-conta-um-quando-sao-quatro.md) | a correção mais barata e mais honesta do censo | 65 min |
| 1.12 | **O portão contra a marca que mente** | [MESA-CHEIA-06](2026-08-13-MESA-CHEIA-06-o-portao-contra-a-marca-que-mente.md) | é teste sobre código-fonte: ninguém precisa estar presente. **Mas SAI por último** — ver a ordem abaixo | 3 h |

**Ordem sugerida dentro da onda 1:** 1.1 primeiro (é medição, e o resto se
planeja melhor com ela); depois 1.2 (regressão de cura, e a mais barata com dano
medido); depois o bloco da verdade (1.3 → 1.6); depois os avisos cegos
(1.7 → 1.10); as frases (1.11) por último **porque são as mais fáceis de refazer
se a D-3 mudar o vocabulário**; e a **1.12 depois de a onda 2 entregar o primeiro
caso real** — um portão escrito contra uma API imaginária cobra a API
imaginária, que é o que a casa chama de contorno.

**Total (sem a 1.12): ≈ 8 h.**

**O que dá para VER no fim da onda 1:** a janela para de dizer "aplicado" quando
nada saiu; o "Desligar" volta a soltar a trava, e a troca automática de perfil
volta a acontecer depois dele; a vibração fixada num controle deixa de pular para
outro; o aviso de Bluetooth frágil acende para os controles 2, 3 e 4; o banner do
co-op diz **qual** jogador perdeu a vibração; a saúde do sistema diz *"áudio
presente em 3 de 4"*; e nenhuma frase da janela fala *"o controle"* quando são
quatro. **Zero pixel novo — e a janela para de mentir em oito lugares.**

---

# ONDA 2 — precisa do olho dela

Cada item só vira commit com foto antes e depois, pela regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
**É a onda em que os quatro jogadores aparecem.**

| # | Entrega | Sprint | O que ela precisa fazer | Depende de | Custo |
|---|---|---|---|---|---|
| 2.1 | **A FITA COLORIDA** — o chip de cada controle ganha o swatch com a cor viva da barra dele | [MESA-CHEIA-01](2026-08-13-MESA-CHEIA-01-a-fita-do-alvo-ganha-a-cor-de-cada-um.md) | olhar as quatro cores lado a lado na TV e dizer se são distinguíveis | **D-1** | 90 min |
| 2.2 | **A FITA CALAR** nas seis abas em que não vale | [MESA-CHEIA-10](2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md) | escolher entre **esconder** e **requalificar** | **D-2** | 60 min |
| 2.3 | **A "No jogo" ganha cor** — terminar a cópia do molde | [MESA-CHEIA-07/E2](2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md) | é a aba que ela olha **durante a partida**; com quatro e sem cor são quatro painéis iguais | 1.1 + **D-1** | 45 min |
| 2.4 | **Os cards da Início ganham cor** — `lightbar_rgb` já chega no mesmo payload e é descartado em `_render_home_controllers` (`app/actions/home_actions.py:1646`); mais `Gtk.FlowBox` no lugar da `Gtk.Box` homogênea | *(neste índice, §7)* | ver se quatro cards cabem sob o tiling do COSMIC | **D-1** | 70 min |
| 2.5 | **A Gatilhos DIZ o alvo dentro dela** — rótulo do controle corrente + swatch ao lado de cada moldura L2/R2, e o toast nomeando o controle | [MESA-CHEIA-02](2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md) §1.1 | hoje a aba é **byte-idêntica** com um ou com quatro controles | 1.4 + **D-1** | 125 min |
| 2.6 | **"Quem comanda o PC agora: Controle N"** na Navegação, com a cor dele, e o aviso quando o comando troca de dono | *(neste índice, §7; medido na [MESA-CHEIA-04](2026-08-13-MESA-CHEIA-04-a-marca-vira-gesto.md) §2)* | é a informação que explica por que o controle do P2 *"não faz nada"* fora do jogo | **D-10** | 105 min |
| 2.7 | **Marcar no card da Status qual é o alvo de edição** | *(neste índice, §7)* | com quatro cards e quatro chips, nada diz qual as outras abas estão editando | 2.1 | 45 min |
| 2.8 | **AS QUATRO MARCAS na aba Gatilhos** — a grade mostra onde cada jogador está | [MESA-CHEIA-02](2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md) | **é a aba em que ela estava olhando quando pediu** | 2.5 + **D-3** | 6 h |
| 2.9 | **A FAIXA DOS QUATRO na Lightbar** — uma prévia por jogador, com o número dentro, e a verdade sobre "cores automáticas" | [MESA-CHEIA-03](2026-08-13-MESA-CHEIA-03-a-mesma-marca-na-aba-lightbar.md) | **é a leitura literal do pedido dela** | 2.8 + **D-11** | 390 min |
| 2.10 | **A marca vira gesto** — clicar na marca de um jogador o torna o alvo | [MESA-CHEIA-04](2026-08-13-MESA-CHEIA-04-a-marca-vira-gesto.md) | é o que transforma a tela em escolha de personagem — e tem um NÃO medido dentro | 2.8 + **D-3** | 3 h |
| 2.11 | **`rumble_ff.per_vpad` por jogador** na linha de estado da Rumble — mostra **quem pediu** vibração, sem uma linha de daemon nova | *(neste índice, §7)* | responde *"por que o meu não vibra?"* sem esperar a D-4 | 2.1 | 90 min |
| 2.12 | **A vitrine das faces na Perfis** — *"este perfil tem ajustes próprios para N controles"*, com N chips coloridos. O mecanismo está **100% pronto e invisível** | *(neste índice, §7)* | é onde as quatro faces já MORAM: `grep -c uniq` em `profiles_actions.py` é **0** em 3357 linhas, e o mapa só atravessa a aba | 2.1 | 150 min |
| 2.13 | **Os quatro cards da Status CABEREM** | *(neste índice, §7)* | **reabre uma decisão dela** — ver a nota abaixo | 2.7 | 120 min |

**Ordem sugerida:** **2.1 e 2.2 primeiro — são uma peça só**, mexem no mesmo
widget, custam 150 minutos somadas e servem as dez abas de uma vez. Depois as
abas baratas, que só param de descartar dado que já chega (2.3, 2.4, 2.6, 2.7).
Depois as que pedem desenho novo (2.5, 2.8 → 2.12). E a 2.13 por último, porque
reabre uma decisão dela.

**Total: ≈ 21 h 30.**

> **NOTA DATADA (13/08/2026) sobre a 2.13 — a decisão EMPILHA-01 pode ter
> caducado, e quem decide é ela.**
>
> Em **02/08/2026**, olhando a tela com **dois** controles, ela decidiu:
> *"os dois blocos não deveriam estar lado a lado mas um em cima do outro de
> forma que o scroll surgisse pra comportar os diferentes controles"*
> (`app/actions/status_actions.py:1217-1233`).
>
> **O que mudou:** medido offscreen em 13/08, quatro cards pedem **1626 px** de
> altura numa janela que abre com **830** (`gui/main.glade:110`), menos
> cabeçalho, tira de abas e o frame Estado. **Ela veria ~1,5 card.**
>
> **A decisão dela não se apaga** — a premissa (dois controles) é que mudou. Com
> quatro, "uma coluna com rolagem" e "ver a mesa de relance" deixam de ser
> compatíveis. É pergunta nova sobre a mesma tela, não revogação da resposta
> antiga.

> **ATENÇÃO DE MÉTODO para as fotos desta onda, medida em 13/08:**
> `install_profiles_tab` é código de **produção** e chama
> `_sync_selection_with_active_profile`, que fala com o **daemon vivo**
> (`tests/unit/test_a_aba_perfis_na_foto.py:30-38`; a primeira rodada saiu com
> `perfis_selecao_automatica_recusada` no log dela). **Todo instrumento novo
> dessa aba tem de desviar essa chamada** — senão o "teste sem aparelho" cutuca
> a sessão dela.

---

# ONDA 3 — o que trava esperando decisão dela

Nada disto anda sem ela responder. **São perguntas, não tarefas** — e cada uma
tem o preço dos dois lados.

## Por que a D-1 vem primeiro, e por que ela é urgente

**Já existem DOIS donos da verdade sobre "a cor dele" dentro da janela**, e as
duas fontes divergem sempre que ela pinta um controle à mão ou desliga as cores
automáticas:

- **a cor VIVA:** `lightbar_rgb` do `state_full`, que o card da Status pinta
  (a regra é `rotulo_lightbar`, em `app/widgets/controller_card.py`) — é a
  decisão **D8**;
- **a PALETA:** `player_slot_color` (`core/led_control.py:158-164`), que a aba
  Lightbar consulta direto para a prévia
  (`app/actions/lightbar_actions.py:409-411`) — e o comentário ali registra que
  isso nasceu de um achado ao vivo: *"a prévia ficava roxa enquanto o controle
  estava azul"*.

Paleta canônica, conferida em `core/led_control.py:146-155`:
**1 azul (0,0,255) · 2 vermelho (255,0,0) · 3 verde (0,255,0) · 4 rosa
(255,0,128)**; 5..8 amarelo/ciano/laranja/roxo (R-25); ≥9 branco.

**Toda marca colorida que nascer antes da D-1 herda essa divergência no dia
um** — e essa é a família de erro que esta casa já pagou duas vezes. É por isso
que a D-1 encabeça a onda, e não porque seja a mais difícil: é a mais barata de
responder e a mais cara de responder tarde.

| # | A pergunta | O que trava | Custo do lado caro |
|---|---|---|---|
| **D-1** | **Que cor é "a cor dele"?** | **tudo o que é colorido** nas ondas 1 e 2 | 0 — é escolha. Escolher errado cria o segundo dono da verdade |
| **D-2** | A fita **esconde** ou se **requalifica** nas seis abas globais? | 2.2 | 0 |
| **D-3** | **Quatro painéis lado a lado** × **um painel com quatro marcas** × **híbrido** | 2.5, 2.8, 2.10, 2.13 e todo o desenho | é a pergunta que decide 500+ min de tela |
| **D-4** | A **intensidade** da vibração é da PEÇA ou da MÁQUINA? | [MESA-CHEIA-05/E1](2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md) | 660 min |
| **D-5** | A **máscara do gamepad** é do JOGO ou do JOGADOR? | Início e Emulação | 480 min — e metade já está escrita e desligada |
| **D-6** | O **MODO** é da máquina ou do jogador? | o quadro "Quando o jogo abrir" | 480 min, ou o item cai inteiro |
| **D-7** | *"Cada player escolhe o seu"* inclui quem **não é DualSense**? | a faixa dos quatro | 120 min |
| **D-8** | O que **"Todos"** significa quando os quatro estão na tela? | 2.1, 2.9 | 0 |
| **D-9** | Aplicar num controle **DESCONECTADO** é "aplicado" ou "guardado"? | o texto de 1.3, 1.4 e 1.5 | 0 |
| **D-10** | A **Navegação** é *"cada um escolhe o seu"* ou *"quem comanda o PC agora"*? | 2.6, e 960 min de mecanismo | ver abaixo |
| **D-11** | Na **Lightbar**, a marca **É** a cor — quatro prévias, ou uma prévia com quatro marcas? | 2.9 | 0 |

### D-1 — Que cor é "a cor dele"?

| Opção | O que ganha | O que custa |
|---|---|---|
| **A cor VIVA do lightbar** | segue o controle de verdade: se um jogo pinta o P2 de branco, a marca fica branca. **É o léxico já decidido** (D8), e não cria dono novo | dois controles da mesma cor ficam com marcas iguais. E quando a fonte é `"desconhecida"` **não há cor para mostrar** — a casa proíbe chamar isso de "apagada" |
| **A paleta do slot** | sempre quatro cores distintas e previsíveis — que é literalmente *"igual jogo quando selecionamos um personagem"*, a frase dela | cria o **segundo dono da verdade**: a marca diz vermelho e a barra na mão dela está branca. O erro que esta casa já pagou duas vezes |
| **Viva com paleta de reserva** | resolve o caso `"desconhecida"` | é a mais difícil de explicar numa tela, e ainda pode dar duas iguais |

**Três perguntas de borda que vêm junto:** (a) e quando a cor é desconhecida — a
marca some ou fica cinza? (b) e no Modo Nativo, em que o jogo é dono do LED — o
card mostra a última cor conhecida e avisa; a marca faz o mesmo? (c) o chip
*"Todos"* ganha alguma marca, ou fica só texto?

### D-2 — A fita, nas seis abas em que não vale

| Opção | Preço |
|---|---|
| **Esconder** | limpo; mas o contexto some ao trocar de aba e volta ao voltar — **pisca** |
| **Requalificar** (*"esta aba vale para todos"*) | mantém o contexto e ensina; mas é mais texto numa fita que já é densa |

O gancho é o mesmo nos dois casos: gate por **id de página** no
`_on_notebook_switch_page` (`app/app.py:957`), que já identifica a aba por id e
nunca por índice.

### D-3 — Quatro painéis × um painel com marcas × híbrido

```
   OPÇÃO A — quatro painéis lado a lado
   ┌───────────┬───────────┬───────────┬───────────┐
   │ ■ Sony 1  │ ■ Sony 2  │ ■ Sony 3  │ ■ Sony 4  │
   │  azul     │  vermelho │  verde    │  rosa     │
   ├───────────┼───────────┼───────────┼───────────┤
   │ Desligado │ Desligado │[Rígido]   │ Desligado │
   │[Rígido]   │ Rígido    │ Rígido s. │ Rígido    │
   │ Rígido s. │[Pulso]    │ Pulso     │ Pulso     │
   │ ...       │ ...       │ ...       │[Galope]   │
   └───────────┴───────────┴───────────┴───────────┘

   OPÇÃO B — um painel, quatro marcas na cor de cada um
   ┌─────────────────────────────────────────────────┐
   │ L2 (gatilho esquerdo)          ■1 ■2 ■3 ■4      │
   ├─────────────────────────────────────────────────┤
   │  Desligado ■2■4  │ Rígido ■1     │ Rígido simples│
   │  Pulso           │ Pulso (curva A)│ Pulso (curva B)│
   │  Resistência     │ Arco de flecha │ Galope ■3     │
   │  ...                                            │
   └─────────────────────────────────────────────────┘

   OPÇÃO C — híbrida: a faixa MOSTRA os quatro, e clicar num troca o alvo
   (é a MESA-CHEIA-04; usa `_sync_edit_target`, que já existe)
```

**O preço da A, medido:** a grade de modos de gatilho tem 19 botões em 3 colunas
e pede **~480 px** (`app/widgets/segmented_selector.py:31-36`: *"3 colunas em
~480px, cada botão tem ~150px"*). A aba Gatilhos já mostra **dois** painéis (L2 e
R2). Quatro jogadores viram **oito** painéis, ou 3840 px de largura mínima. A
tela dela é de **1920 px** (`scripts/gui-captura/retratar_abas.py:104`) e o piso
da janela é de **760 px** (`gui/main.glade:114`). **A opção A, nesta aba, não
cabe** sem rolagem horizontal ou sem quebrar a grade em 1 coluna (19 linhas de
altura por jogador).

**E a conta se inverte na Status:** ali sobra largura e falta **altura** — 1626 px
de card numa janela de 830 (a nota da 2.13). Na Gatilhos sobra altura (~600 px
vazios abaixo das grades) e falta largura. **Não há uma resposta que sirva às
duas abas por geometria** — a resposta tem de ser de produto.

**O preço da B:** a marca é pequena, e cor sozinha exclui quem não distingue
cores. A regra da casa para isto já existe e é da paleta:
`core/led_control.py:135-138` escolheu o rosa `(255, 0, 128)` em vez do magenta
puro *"para não confundir com o azul em brilho baixo"*. A proposta é a marca carregar **cor E
número** (`■1`), nunca cor sozinha.

**O preço da C:** ela vê as quatro e mexe numa por vez. É a mais barata e é a
que responde ao *"perder de vista os outros"* sem responder ao *"cada player
poderia escolher o seu"*.

### D-4 — A intensidade da vibração: da peça ou da máquina?

| Opção | Preço |
|---|---|
| **Da peça** (o que o rascunho já grava) | `rumble_active` vira mapa por `uniq`, `rumble.set` aceita endereço, o `state_full` expõe os quatro estados: **≈ 660 min**. Em troca, morrem os defeitos do §2.4 |
| **Da máquina** (o que o daemon vivo faz) | **20 min**: trocar o rótulo *"Intensidade global:"* (`gui/main.glade:1571`). Mas então o rascunho está gravando por peça um número que ninguém lê — e isso é **dívida, não conserto** |

**O que NÃO muda em nenhum dos dois casos**, e é decisão de 10/08 que continua
valendo: o **passthrough continua sendo um só** (*"não descreve a peça: descreve
quem manda na vibração agora"*), e o `rumble.policy = "auto"` continua global
porque escala pela bateria do controle **primário**.

### D-5 — A máscara do gamepad: do jogo ou do jogador?

**Do jogador** custa ≈ 480 min — campo novo em `ControllerOverrides` (que hoje
tem leds/triggers/rumble/speaker e nenhum campo de modo ou máscara), o `flavor`
resolvido por `uniq`, e a rota de emulação aceitando alvo — **e metade já está
escrita e desligada**: `ExternalMaskRegistry`
(`daemon/subsystems/external_mask.py:157`) guarda, valida e **persiste** máscara
por identidade, com **zero chamadores fora do próprio módulo**, e o portão da
casa já a acusa por nome
(`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`).

**Do jogo** custa uma frase declarando o escopo. **Risco não medido, e é dela
decidir se aceita:** um jogo pode não aceitar controles heterogêneos na mesma
sessão.

### D-6 — O MODO é da máquina ou do jogador?

**Ela já decidiu "da máquina", por escrito e com data** — `profiles/schema.py:637`:
*"`mode` e a máscara do gamepad são da SESSÃO, não da peça"*.

**Se a resposta continuar sendo essa, o pedido dela não se aplica ao quadro
"Quando o jogo abrir", e o item cai inteiro** — o que sobra ali é declarar o
escopo. Se mudar: ≈ 480 min, porque o modo nativo é estado do daemon inteiro e
toda a fiação de transição é global.

### D-7 — "Cada player" inclui quem não é DualSense?

O 8BitDo e o Pro Controller **não têm card na Status** — decisão de produto
**EXT-COUNT-01** (`app/actions/status_actions.py:1110`) — e não entram em
`state["controllers"]` (`:2379-2391`). Se o jogador 3 estiver num Pro, ele
**existe** no cabeçalho, **existe** no LED de número, e **some** de toda faixa
que a onda 2 desenhar.

Incluir custa ≈ 120 min. Não incluir custa a pergunta *"cadê o jogador 3?"* na
primeira vez que ela jogar com um externo.

### D-8 — O que "Todos" significa quando os quatro estão na tela?

Some (as quatro marcas o tornam redundante) ou vira *"marcar os quatro de uma
vez"*? Hoje *"Todos"* é um **estado real e distinto**
(`app/actions/lightbar_actions.py:639` parte o fluxo em três) e só aparece com
2+ controles. Com os quatro cards marcados, **o que fica marcado quando o alvo é
"Todos" — os quatro ou nenhum?**

### D-9 — Aplicar num controle desconectado é "aplicado" ou "guardado"?

Hoje a tela diz *"aplicado"* e o aparelho não recebeu nada: o override fica
registrado e pega no hotplug (`core/backend_pydualsense.py:3417-3423`), e o alvo
é **mantido de propósito** quando o controle some (**R-16**). É vocabulário puro,
custo zero, e decide o texto de 1.3, 1.4 e 1.5.

### D-10 — A Navegação: "cada um escolhe o seu" ou "quem comanda o PC"?

**Esta é a que eu diria com a evidência, e a palavra continua sendo dela.**
Gatilho, luz e vibração acontecem **no controle**: quatro escolhas, quatro
aparelhos, nenhum conflito. Mouse e teclado acontecem **no PC**, que tem um
cursor e um foco de teclado.

| Opção | Preço |
|---|---|
| **"Quem comanda o PC agora"** — mostrar o dono, avisar quando troca, e deixar escolher | 105 min de tela + 180 min para poder **escolher** o primário (hoje não existe rota: `next(iter(self._handles))`, `core/backend_pydualsense.py:1944` — é **ordem de plugar**, não número de jogador) |
| **"Cada um escolhe o seu"** — N leitores, N devices | ≈ 960–1200 min, e esbarra no compositor. Quatro mouses virtuais somariam no **mesmo** ponteiro — **INFERIDO, não medido:** não há uma linha neste repositório que o prove, e Wayland/COSMIC não tem multi-cursor |

**E há uma decisão dela no caminho:** o perfil **proíbe** `mouse` e
`key_bindings` por unidade (`profiles/schema.py:642-649`, 10/08). Mexer aqui é
reabrir aquela decisão, com o preço na mesa. **A parte que aguenta por jogador é
a tabela de atalhos** — o botão de cada controle digitando coisa diferente.

### D-11 — Na Lightbar, a marca É a cor

Marcar *"o jogador 2 escolheu vermelho"* com um quadradinho vermelho **em cima de
um seletor de vermelho** não se lê: o sinal e o fundo são a mesma coisa. Ali a
marca vira **número** com a cor como preenchimento da própria prévia — quatro
prévias numeradas — ou uma prévia só com quatro marcas ao lado.

**E o terceiro estado, que é o que mais engana:** com *"Cores automáticas por
controle"* ligado — que é o padrão do esquema — **ninguém escolheu cor nenhuma**.
A tela tem de saber dizer isso, ou as quatro marcas ficam em cima da cor manual
global e nenhuma delas é verdade.

*(Esta era a pergunta 3.2.4 da primeira versão deste índice; a numeração foi
alinhada com as dez decisões do censo, e o texto é o mesmo.)*

---

## 4. As dívidas de fundo — grandes demais para uma onda

**Nenhuma entra em onda como está.** São reforma, não conserto. Ficam
registradas para não virarem surpresa.

**O leitor único.** Existe **UM** `EvdevReader` no backend, re-atrelado ao
primário a cada hotplug (`core/backend_pydualsense.py:1955`), e o `read_state`
declara em comentário próprio: *"INPUT vem SEMPRE do controle PRIMÁRIO … é,
portanto, single-controller por construção"* (`:2192-2195`). Mouse, teclado,
touchpad e **todos** os combos PS+X são privilégio exclusivo do controle 1. Isto
não é ajuste, é arquitetura — e barateia por o co-op **já** criar um
`EvdevReader` por MAC, com grab, em produção.

**A máscara por controle já está escrita e desligada.** É a metade paga e parada
da **D-5** (`daemon/subsystems/external_mask.py:157`).

**`rumble_active` é uma tupla e devia ser mapa.** É o corpo da **D-4**. O
`set_rumble_for(uniq, weak, strong)` de que ele precisa **já existe e tem
mordida** (`core/backend_pydualsense.py:3642`) — usado hoje só pelo co-op
(`daemon/subsystems/coop.py:571`) e pelo force-feedback do jogo
(`daemon/subsystems/gamepad.py:992`). **É, de novo, a classe de defeito mais
cara desta casa: a cura escrita e nunca ligada.**

**O alvo não sobrevive ao restart.** `_output_target_key` só vive na RAM do
backend (`core/backend_pydualsense.py:1165`) e ninguém o persiste. Os botões
"Ligar"/"Desligar o Hefesto" da aba Sistema (`daemon_start_button`,
`gui/main.glade:2470`, e `daemon_stop_button`, `:2483`) devolvem o daemon a
broadcast **enquanto a janela mantém o alvo antigo de
propósito** (R-16). Janela e daemon divergem sem aviso.

---

## 5. As armadilhas desta leva, cada uma com endereço

1. **O espelho do Steam já está resolvido, e eu conferi.** O Steam Input cria um
   Xbox virtual para cada controle que vê, inclusive do nosso vpad
   ([TRES-CONTROLES-01](2026-08-10-TRES-CONTROLES-01-o-espelho-do-espelho-no-pragmata.md)).
   A lista que a janela usa **já exclui os virtuais**: `discover_gamepads` corta
   tudo sob `/devices/virtual/` (`core/evdev_reader.py:659`, com a regra em
   `_is_virtual_evdev`, `:167`), e a docstring de `discover_external_gamepads`
   (`:739-742`) nomeia os vpads do Steam Input explicitamente. **Não há sprint
   para isto**; há uma asserção na 06 para que continue assim.
2. **A cor da paleta não é a cor da barra.** É a **D-1**, e as sprints 01, 02 e
   03 têm mordida escrita exatamente contra trocar uma pela outra.
3. **Pintar em aba escondida custa CPU medida.** O tique de 10 Hz só trabalha com
   a Status à vista, e o motivo está escrito: *"um poller cego já custou 104% de
   um núcleo nesta casa"* (`app/actions/status_actions.py:766-779`). Toda marca
   desta leva pinta no tique LENTO de 2 Hz e só com a aba à vista — **nenhum
   `GLib.timeout_add` novo**.
4. **Sob Xvfb não há gerenciador de janelas:** `Gtk.Window` fica 1x1 para
   sempre. Toda foto desta leva é `Gtk.OffscreenWindow`
   ([COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md)).
5. **O daemon vivo é mais velho que o código.** Com install editable, cura de
   daemon só vale no **próximo start**, e o sintoma de esquecer isso é a
   **AUSÊNCIA** de dado novo, não um erro. Vale para a 05 e para a 09.
6. **Interface só fecha com o olho dela.** Nenhuma sprint desta leva se declara
   pronta sem foto antes e depois e a palavra dela.
7. **Este índice envelhece em minutos.** O índice de 31/07 registrou um item como
   pendente e ele foi entregue **três minutos e vinte e dois segundos depois** —
   e ninguém voltou para riscar a linha, que ficou nove dias na fila. Quem
   entregar qualquer item desta lista, **volte aqui**.

---

## 6. A regra dos quatro, e como esta leva a cumpre

Ela fixou quatro regras em 09/08. Cada uma, aqui:

| a regra dela | como esta leva cumpre |
|---|---|
| **a vontade da GUI prevalece** | a marca mostra o EFETIVO de cada peça (`effective_triggers_for`, `app/draft_config.py:871`; `effective_leds_for`, `:841`; `effective_rumble_for`, `:932`), que é o que a GUI gravou — nunca o que o daemon acha que aplicou. E a onda 1 existe para o daemon **parar** de afirmar o que não fez |
| **tudo tem que chegar na interface e no install** | as sprints de tela não têm nada a instalar; a **05** muda o daemon e por isso carrega a prova de ciclo `uninstall` → `install` que a [CICLO-QUE-PROVA-01](2026-08-08-CICLO-QUE-PROVA-01-desinstalar-instalar-e-comparar-o-que-o-produto-recria-sozinho.md) fixou |
| **universal** | a marca é por `uniq` e por cor de lightbar, não por marca de aparelho. Um externo sem lightbar entra com o contorno neutro e o número, nunca some da conta — **e a D-7 é a pergunta de se ele entra na faixa também** |
| **o rumble em todos os modos** | é o assunto da 05, e a onda 1 já mata o defeito em que ele **muda de dono sozinho** |

---

## 7. O que este índice NÃO mediu, e o que ainda não tem sprint própria

**Não mediu:**

- **A janela não foi aberta.** Toda afirmação sobre interface vem de código, do
  `.glade` e dos PNG de `docs/usage/assets/`. O aceite continua sendo o olho
  dela.
- **Nada foi provado com dois ou mais controles.** Ela tem **um** DualSense por
  USB agora. Os veredictos de "mira certo" são leitura de código mais o ensaio
  dela de 12/08 (`docs/data/ensaios.csv`).
- **Nenhum número de custo foi medido.** Os custos são estimativa; as alturas e
  larguras vieram de medição **offscreen**, e estão marcadas onde aparecem.
- **A aba "No jogo" não foi auditada — foi descoberta.** O item 1.1 existe para
  isso.

**Sem sprint própria** (a medição está neste índice, e cada uma cabe numa
entrega): **1.10** (guarda do card sem MAC), **2.4** (cor nos cards da Início),
**2.6** ("quem comanda o PC agora"), **2.7** (marcar o alvo no card da Status),
**2.11** (`rumble_ff.per_vpad` por jogador), **2.12** (a vitrine das faces na
Perfis) e **2.13** (os quatro cards caberem). Se alguma crescer ao ser
executada, ela vira arquivo — e volta aqui como link.
