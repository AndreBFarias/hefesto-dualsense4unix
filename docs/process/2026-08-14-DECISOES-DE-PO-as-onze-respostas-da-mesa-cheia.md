# DECISÕES DE PO — as onze respostas da mesa cheia

- **Escrito em:** 14/08/2026, na branch `restauro/inicio-da-sessao`, sobre `7673cd7`.
- **Por que existe:** a ONDA 3 do
  [índice da mesa cheia](sprints/2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
  são **onze perguntas, não tarefas** — e nenhuma delas anda sem resposta. Ela
  delegou a resposta por escrito, em 14/08: *"atue como PO por mim"* — e disse
  que **dentro do projeto há tudo para decidir**: os eventos, o histórico e as
  preferências dela já registrados aqui.
- **Grau: DECISÃO DELEGADA.** Não é decisão dela, e não se disfarça de uma. Cada
  linha abaixo diz **com que evidência do próprio repositório** foi decidida, e
  **o que custa desfazer**. A
  [PROVA-DE-TELA-01](sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
  continua valendo inteira: **a palavra final sobre a tela é dela**, e as fotos
  existem para que ela vete em dez minutos.
- **O critério que guiou as onze**, tirado do que ela já decidiu antes e não do
  meu gosto: **o princípio ganha da conveniência**, **o preço dos dois lados fica
  na mesa**, e **o que ela já decidiu por escrito não se reabre por descuido**.

---

## O que mudou no dia em que isto foi escrito

**Ela conectou os quatro controles.** O índice inteiro foi escrito declarando, na
seção 7: *"Nada foi provado com dois ou mais controles. Ela tem **um** DualSense
por USB agora."*

Essa limitação caiu em 14/08. O que era estimativa offscreen agora tem foto e
`state_full` de verdade. **Onde a mesa cheia contradisser uma decisão abaixo, a
medição ganha** — e a decisão volta para esta página com nota datada.

---

## As onze, em uma tabela

| # | A pergunta | A resposta | O que custa desfazer |
|---|---|---|---|
| **D-1** | Que cor é *"a cor dele"*? | **A cor VIVA do lightbar**, e a marca carrega **sempre cor E número** | baixo — é uma função de resolução de cor, num lugar só |
| **D-2** | A fita esconde ou se requalifica nas seis abas? | **Requalifica** | baixo — é o texto de um rótulo |
| **D-3** | Quatro painéis × um painel com marcas × híbrido | **B+C: um painel com as quatro marcas, e clicar na marca troca o alvo** | alto — é o desenho de 500+ min de tela |
| **D-4** | A intensidade da vibração é da peça ou da máquina? | **Da peça** | alto — ≈ 660 min, e é reforma de daemon |
| **D-5** | A máscara do gamepad é do jogo ou do jogador? | **Do jogador**, com a máscara do jogo como padrão herdado | alto — ≈ 480 min, e metade já está escrita |
| **D-6** | O MODO é da máquina ou do jogador? | **Da máquina — ela já decidiu, e continua valendo** | — (não se reabre aqui) |
| **D-7** | *"Cada player"* inclui quem não é DualSense? | **Inclui** | médio — ≈ 120 min |
| **D-8** | O que *"Todos"* significa com os quatro na tela? | **Marca os quatro**, e continua sendo estado distinto | baixo |
| **D-9** | Aplicar num controle desconectado é *"aplicado"* ou *"guardado"*? | **Guardado** | zero — é vocabulário |
| **D-10** | A Navegação é *"cada um escolhe o seu"* ou *"quem comanda o PC"*? | **Quem comanda o PC agora** | alto — a outra rota custa ≈ 960–1200 min |
| **D-11** | Na Lightbar, a marca É a cor | **Quatro prévias numeradas**, e a tela sabe dizer o terceiro estado | médio |

---

## D-1 — Que cor é "a cor dele": a VIVA, sempre com número

**A cor viva do lightbar** (`lightbar_rgb` do `state_full`), que é o que o card
da Status já pinta pela regra `rotulo_lightbar`
(`app/widgets/controller_card.py`). **Nunca** a paleta `player_slot_color`
(`core/led_control.py:158-164`).

**O motivo é o princípio que esta casa já pagou duas vezes para aprender: um
dono da verdade.** A paleta é sedutora porque garante quatro cores distintas —
que é literalmente a frase dela, *"igual jogo quando selecionamos um
personagem"*. Mas ela cria o **segundo dono**: a marca diz vermelho e a barra na
mão dela está branca. O comentário em `app/actions/lightbar_actions.py:409-411`
registra que isso já aconteceu ao vivo — *"a prévia ficava roxa enquanto o
controle estava azul"*. Escolher a paleta é escolher recriar esse defeito em
toda marca nova da leva.

**A paleta não morre — ela muda de papel.** Ela continua sendo quem **escreve**
a cor quando o produto pinta automaticamente. Deixa de ser quem **afirma** a cor
na tela. Gerador e afirmação passam a ser coisas diferentes, e é isso que
resolve a divergência.

**As três bordas, respondidas:**

1. **Cor desconhecida** (a fonte é `"desconhecida"`): a marca fica com
   **contorno neutro e o número dentro**. Não some — sumir apagaria o jogador da
   tela — e não inventa cor. A casa proíbe chamar isso de "apagada".
2. **Modo Nativo**, em que o jogo é dono do LED: a marca faz o **mesmo que o
   card já faz** — última cor conhecida, com o aviso. O léxico é o de dentro de
   casa, não um novo.
3. **O chip *"Todos"***: fica **só texto**, sem cor própria. Ver a D-8.

**E a marca carrega SEMPRE cor E número (`■1`), nunca cor sozinha.** Isso não é
enfeite: dois controles podem estar na mesma cor viva, e cor sozinha exclui quem
não distingue cores. A própria paleta da casa já decidiu por esse princípio
quando escolheu o rosa `(255, 0, 128)` em vez do magenta puro *"para não
confundir com o azul em brilho baixo"* (`core/led_control.py:135-138`).

---

## D-2 — A fita se requalifica, não esconde

Nas seis abas em que a fita *"Ajustes vão para: …"* é falsa (Início, No jogo,
Perfis, Sistema, Emulação, Navegação), ela **muda de texto** em vez de sumir.

**Motivo:** esconder faz o contexto **piscar** — some ao trocar de aba e volta ao
voltar. Uma tira que aparece e desaparece conforme a aba ensina que ela é
instável; uma que muda de frase ensina o que cada aba faz. E o gancho é o mesmo
nos dois casos: gate por **id de página** no `_on_notebook_switch_page`
(`app/app.py:957`), que já identifica a aba por id e nunca por índice.

O texto sai do léxico que já existe na tela — a lista certa do escopo já está
escrita, e mora onde ninguém lê: o tooltip em
`app/actions/status_actions.py:1484-1487` enumera *"Controle alvo das ações
(lightbar, gatilhos, LEDs, rumble)"*. **A requalificação é esse tooltip subindo
para a fita**, não vocabulário novo.

---

## D-3 — Um painel com as quatro marcas, e a marca é clicável

**A opção A (quatro painéis lado a lado) está eliminada por medição, não por
gosto:** a grade de modos de gatilho tem 19 botões em 3 colunas e pede ~480 px
(`app/widgets/segmented_selector.py:31-36`); a aba Gatilhos já mostra **dois**
painéis (L2 e R2); quatro jogadores viram **oito** painéis, ou **3840 px** de
largura mínima. A tela dela tem **1920** e o piso da janela é **760**
(`gui/main.glade:114`). **Não cabe.**

Fica **B com C**: um painel, com a marca `■N` colorida em cima da opção que cada
jogador escolheu — e **clicar na marca de um jogador o torna o alvo** (é a
[MESA-CHEIA-04](sprints/2026-08-13-MESA-CHEIA-04-a-marca-vira-gesto.md), que usa
`_sync_edit_target`, já existente).

**Por que as duas juntas, e não uma:** o pedido dela tem duas metades. *"sem
perder de vista os outros"* é atendido pelo B — as quatro escolhas ficam
visíveis ao mesmo tempo. *"cada player poderia escolher o seu"* é atendido pelo
C — a marca deixa de ser enfeite e vira o gesto de escolher quem se edita. **B
sozinho mostra e não deixa mexer; C sozinho deixa mexer e não mostra.** Separá-las
entregaria metade do pedido com a aparência de inteiro.

---

## D-4 — A intensidade da vibração é da PEÇA

O caro (≈ 660 min): `rumble_active` deixa de ser tupla e vira mapa por `uniq`,
`rumble.set` passa a aceitar endereço, e o `state_full` expõe os quatro estados.

**Escolhi o caro, e o motivo é uma regra dela, não uma preferência minha.** Em
09/08 ela fixou **"o rumble em todos os modos"** e **"a vontade da GUI
prevalece"**. Hoje o mesmo clique grava a política no rascunho **da peça**
(`app/actions/rumble_actions.py:429` → `:551`) e manda ao daemon um
`rumble.policy_set` **sem endereço** (`:433` →
`daemon/ipc_handlers.py:3314-3336`) — enquanto o selo diz *"Editando: Controle
2"*. O barato (20 min) é trocar o rótulo para *"Intensidade global"* e **assumir
que a GUI mente por desenho**. Isso não é conserto, é dívida com rótulo novo.

**E a metade cara já está paga:** `set_rumble_for(uniq, weak, strong)` existe e
**tem mordida** (`core/backend_pydualsense.py:3642`), usado hoje só pelo co-op
(`daemon/subsystems/coop.py:571`) e pelo force-feedback
(`daemon/subsystems/gamepad.py:992`). É de novo a classe de defeito mais cara
desta casa — **a cura escrita e nunca ligada**.

**O que NÃO muda, e é decisão dela de 10/08 que continua valendo:** o
passthrough continua sendo **um só** (*"não descreve a peça: descreve quem manda
na vibração agora"*), e `rumble.policy = "auto"` continua **global**, porque
escala pela bateria do controle primário.

**Sequenciamento:** a D-4 **não entra nesta leva**. O que entra é a E0 — o rumble
fixado deixar de **migrar de dono** —, que é conserto de defeito sob qualquer
resposta a esta pergunta.

---

## D-5 — A máscara do gamepad é do JOGADOR, com o jogo como padrão

**Do jogador** (≈ 480 min), pela regra **"universal"** que ela fixou em 09/08, e
porque **metade já está escrita e desligada**: `ExternalMaskRegistry`
(`daemon/subsystems/external_mask.py:157`) guarda, valida e **persiste** máscara
por identidade, com **zero chamadores fora do próprio módulo** — e o portão da
casa já a acusa por nome
(`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`).

**Com um limite explícito, porque há risco NÃO MEDIDO:** um jogo pode não aceitar
controles heterogêneos na mesma sessão. Por isso a máscara **do jogo é o padrão
herdado** e a do jogador é **override por unidade** — o mesmo desenho que o
`ControllerOverrides` já usa para leds/triggers/rumble/speaker. Ninguém precisa
escolher por jogador para o produto funcionar; quem escolher, assume.

**Antes de a D-5 virar código, o risco tem de ser medido com a mesa cheia** — é
exatamente o tipo de coisa que só se sabe com quatro controles conectados.

---

## D-6 — O MODO continua sendo da MÁQUINA: ela já decidiu

**Esta pergunta não é minha para responder.** Ela já respondeu, por escrito e com
data, e está no esquema: `profiles/schema.py:637` — *"`mode` e a máscara do
gamepad são da SESSÃO, não da peça"*.

**Consequência, e ela é boa:** o pedido dela sobre os quatro jogadores **não se
aplica** ao quadro *"Quando o jogo abrir"*, e o item **cai inteiro**. O que sobra
ali é **declarar o escopo na tela** — uma frase dizendo que aquele quadro vale
para a sessão, não por jogador. Custa minutos e evita a pergunta *"por que aqui
não tem as quatro marcas?"*.

> **NOTA:** a metade da D-5 que é *máscara* e a D-6 que é *modo* estão na mesma
> frase daquele esquema. A D-5 muda **a máscara por unidade** e **não toca o
> modo**. Se ao executar a D-5 ficar claro que separar as duas exige reescrever
> aquela decisão dela, **a D-5 para e volta para ela** — não se contorna decisão
> escrita.

---

## D-7 — "Cada player" inclui o 8BitDo e o Pro Controller

**Inclui** (≈ 120 min), pela mesma regra **"universal"** de 09/08.

O 8BitDo e o Pro Controller não têm card na Status por decisão de produto
**EXT-COUNT-01** (`app/actions/status_actions.py:1110`) e não entram em
`state["controllers"]` (`:2379-2391`). Se o jogador 3 estiver num Pro, ele
**existe** no cabeçalho, **existe** no LED de número, e **sumiria** de toda faixa
que a onda 2 desenhar.

**A EXT-COUNT-01 não se reabre.** Ela decidiu que o externo não tem *card* — e
não tem mesmo: card carrega bateria, áudio, lightbar, coisas que o externo não
tem. **Marca não é card.** O externo entra na faixa com **contorno neutro e o
número**, exatamente como o caso "cor desconhecida" da D-1, que já é o desenho
decidido para "não há cor para mostrar".

---

## D-8 — "Todos" marca os quatro, e continua sendo estado distinto

Hoje *"Todos"* é um **estado real e distinto** — `app/actions/lightbar_actions.py:639`
parte o fluxo em três — e só aparece com 2+ controles. **Isso não muda.**

Com os quatro na tela, *"Todos"* selecionado deixa **os quatro marcados**. Não
desmarca todos (o que leria como "nada selecionado", que é falso) e não some (o
que tiraria a única forma de agir sobre os quatro de uma vez). O chip *"Todos"*
em si fica **sem cor própria**, pela D-1: ele não é um jogador, e dar cor a ele
inventaria um quinto dono de cor.

---

## D-9 — Num controle desconectado, é "GUARDADO"

Custo zero, e decide o texto de 1.3, 1.4 e 1.5 da onda 1.

Hoje a tela diz *"aplicado"* e o aparelho não recebeu nada. O override fica
registrado e pega no hotplug (`core/backend_pydualsense.py:3417-3423`), e o alvo
é **mantido de propósito** quando o controle some (**R-16**).

**A palavra passa a ser "guardado", e a frase diz quando vale:** *"Guardado — vai
valer quando o Controle N voltar."* O mecanismo está certo; era só a palavra que
mentia. **A onda 1 inteira existe para a janela parar de afirmar o que não
aconteceu** — dizer "aplicado" para algo guardado é a mesma mentira em outra
casa.

**Regra de execução que sai daí:** as três entregas põem esse vocabulário **num
lugar só**, para que trocá-lo seja uma linha, e não uma caçada por strings.

---

## D-10 — A Navegação é "quem comanda o PC agora"

**105 min de tela + 180 min** para poder **escolher** o primário — hoje não
existe rota: `next(iter(self._handles))` (`core/backend_pydualsense.py:1944`) é
**ordem de plugar**, não número de jogador.

**Contra ≈ 960–1200 min** da outra rota, que esbarra no compositor: quatro mouses
virtuais somariam no **mesmo** ponteiro. **Isso é INFERIDO, não medido** — não há
uma linha neste repositório que prove, e Wayland/COSMIC não tem multi-cursor. É a
afirmação mais fraca desta página, e está marcada como tal.

**E há decisão dela no caminho, que esta resposta respeita:** o perfil **proíbe**
`mouse` e `key_bindings` por unidade (`profiles/schema.py:642-649`, 10/08).
"Quem comanda o PC agora" **não reabre** aquela decisão — mostra o dono, avisa
quando ele troca, e deixa escolher qual controle é o dono. **A parte que aguenta
por jogador é a tabela de atalhos**, e ela fica para depois, separada.

Gatilho, luz e vibração acontecem **no controle**: quatro escolhas, quatro
aparelhos, nenhum conflito. Mouse e teclado acontecem **no PC**, que tem um
cursor e um foco de teclado. **A assimetria é do mundo, não da tela** — e a tela
tem de dizer isso, porque é o que explica por que o controle do P2 *"não faz
nada"* fora do jogo.

---

## D-11 — Quatro prévias numeradas, e a tela sabe dizer o terceiro estado

Marcar *"o jogador 2 escolheu vermelho"* com um quadradinho vermelho **em cima de
um seletor de vermelho** não se lê: sinal e fundo são a mesma coisa. Na Lightbar
a marca é **o número**, e a cor é o preenchimento da própria prévia — **quatro
prévias numeradas**.

**E o terceiro estado é a parte que mais engana, e tem de aparecer:** com *"Cores
automáticas por controle"* ligado — que é o **padrão do esquema** — **ninguém
escolheu cor nenhuma**. Quatro marcas em cima da cor manual global, nesse estado,
seriam **quatro afirmações falsas ao mesmo tempo**. A tela tem de dizer, com
todas as letras, que as cores estão sendo escolhidas pelo produto.

Isto é a D-1 aplicada à aba em que ela dói mais: a marca mostra o que **está
vivo**, e quando ninguém escolheu, ela diz *ninguém escolheu*.

---

## O que estas onze respostas destravam, e o que continua parado

**Destravam** a ONDA 1 inteira (a D-9 dá o texto de 1.3, 1.4 e 1.5) e as
entregas 2.1, 2.2, 2.3, 2.4 e 2.7 da ONDA 2 (a D-1 e a D-2 dão a cor e a fita).

**Continuam parados, e por decisão consciente:**

- **2.13 — os quatro cards da Status caberem.** Reabre uma decisão que ela tomou
  em **02/08** olhando a tela com **dois** controles: *"os dois blocos não
  deveriam estar lado a lado mas um em cima do outro de forma que o scroll
  surgisse"* (`app/actions/status_actions.py:1217-1233`). A premissa mudou — com
  quatro cards são 1626 px numa janela de 830, e ela veria ~1,5 card. **Premissa
  mudada é pergunta nova, e a pergunta é dela.**
- **2.5, 2.8, 2.9, 2.10, 2.12** — as de desenho novo. A D-3 diz **qual** desenho;
  ela ainda tem de **ver** o desenho. São 500+ min de tela, e a PROVA-DE-TELA-01
  existe exatamente para que ninguém gaste isso contra um desenho que ela vetaria
  em dez segundos.
- **D-4 e D-5 como código.** Decididas aqui, não executadas aqui: são ≈ 1140 min
  de daemon, e a D-5 tem risco não medido que a mesa cheia agora permite medir.

---

## Como desfazer qualquer uma destas onze

Cada decisão acima tem a coluna *"o que custa desfazer"* na tabela. **Nenhuma
delas se apaga desta página** — se ela mudar uma, a linha ganha **nota datada com
o que caducou**, como manda a regra da casa. O que **se substitui** é fato
errado: se a mesa cheia mostrar que um número aqui está errado, o número certo
entra no lugar, sem guardar o errado ao lado.
