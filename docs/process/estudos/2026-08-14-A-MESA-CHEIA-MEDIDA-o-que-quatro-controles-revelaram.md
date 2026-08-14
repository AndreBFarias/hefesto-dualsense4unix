# A MESA CHEIA, MEDIDA — o que quatro controles revelaram e um só escondia

- **Medido em:** 14/08/2026, com **quatro DualSense conectados ao mesmo tempo** —
  dois no cabo, dois por Bluetooth —, daemon vivo, sobre `7673cd7`.
- **Por que existe:** o
  [índice da mesa cheia](../sprints/2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
  declara na seção 7: *"Nada foi provado com dois ou mais controles. Ela tem
  **um** DualSense por USB agora."* **Essa limitação caiu**, e o que ela revelou
  não era previsível por leitura de código.
- **Como foi medido:** `daemon.state_full` pelo `IpcClient` — a rota do produto.
  **Leitura pura:** nenhuma escrita no aparelho, nenhum `hidraw` cru, nenhum
  reinício de daemon. O motivo está registrado na casa: o instrumento que disputa
  o `hidraw` com o daemon imprime *"aplicado"* sem ter aplicado.
- **O dado está versionado:** `tests/fixtures/state_full_quatro_controles.json`
  (commit `6d2346a`), com a máscara que os portões de `tests/` exigem.
- **Grau: MEDIDO**, com duas amostras separadas por minutos. Onde há correlação
  sem prova, está marcado como **SUSPEITA**.

---

## 1. A mesa, como ela estava

| # | transporte | primário | `player` | `player_slot` | cor viva | fonte | bateria |
|---|---|---|---|---|---|---|---|
| 0 | **USB** | **sim** | 1 | **4** | rosa `(255,0,128)` | `sysfs` | 100% |
| 1 | **USB** | não | 2 | **1** | azul `(0,0,255)` | `sysfs` | 95% |
| 2 | **BT** | não | 3 | **3** | verde `(0,255,0)` | `sysfs` | 100% |
| 3 | **BT** | não | 4 | **2** | vermelho `(255,0,0)` | `sysfs` | 100% |

Quatro cores **distintas**, **nenhuma** com fonte `"desconhecida"`, e cada uma
bate exatamente com `player_slot_color(player_slot)`
(`core/led_control.py:147-155`). Co-op ligado com quatro jogadores e **zero
externos** — `controller.list {external: true}` devolve lista vazia. Nenhum
controle sem driver. `rumble_ff.per_vpad` com quatro entradas, todas `uhid`.

**A D-1 sai desta medição mais forte, não mais fraca.** A decisão foi *"a cor
viva, nunca a paleta"*, e a borda que mais preocupava — *"e quando a cor é
desconhecida?"* — **não ocorreu em nenhum dos quatro**. As duas fontes
concordaram nos quatro casos, porque ninguém tinha pintado nada à mão. **Isso não
prova que a paleta serviria**: prova que, no estado de repouso, as duas dizem o
mesmo — e é exatamente por isso que escolher a errada passa despercebido até o
dia em que um jogo pinta o P2 de branco.

---

## 2. O achado central: a cor diz um número e a interface diz outro

**`player` e `player_slot` são coisas diferentes, e divergiram em TRÊS dos
quatro controles.**

Rodando os formatadores **reais** do produto sobre o payload capturado, os cards
da aba Início dela diriam, naquele momento:

```
   Controle 4 — P1     USB · primário · 100%     ROSA
   Controle 1 — P2     USB · 95%                 AZUL
   Controle 3 — P3     BT  · 100%                VERDE
   Controle 2 — P4     BT  · 100%                VERMELHO
```

**O controle AZUL — a cor que o mundo inteiro lê como jogador 1 — está rotulado
P2. O ROSA, que no PS5 é a cor do jogador 4, é o P1 e é o primário.**

**Nenhum dos dois lados está errado, e é isso que torna o problema difícil:**

- *"Controle N"* é o **`player_slot`**, e é identidade **estável** — a decisão
  está escrita em `app/actions/base.py:21-43`. É ele que manda na cor.
- *"— P{N}"* é o **`player`**, o número **do co-op** — acrescentado em
  `app/actions/home_actions.py:615-634`.

**Com um controle só, os dois números coincidem e a contradição é invisível.**
Ela nunca poderia ter aparecido antes de hoje.

### Por que isto atinge a leva inteira

A entrega **2.4** dá cor aos cards da Início. **Dar cor sem resolver este par
coloca duas afirmações contraditórias no mesmo card**: o quadradinho rosa
dizendo *"jogador 4"* pela convenção do PlayStation, ao lado do texto dizendo
*"P1"*.

E atinge a **D-1** num ponto que ela não previu. A decisão diz que a marca
carrega *"sempre cor E número"* — **mas não diz QUAL número**, porque em 13/08
não havia como saber que existiam dois.

---

## 3. D-12 — que número vai dentro da marca?

**Esta pergunta é nova. Ela nasceu da medição de hoje e não estava em lugar
nenhum do repositório.**

| Opção | O que ganha | O que custa |
|---|---|---|
| **O `player_slot`** | é quem **manda na cor** — a marca fica internamente coerente (rosa e `4` sempre juntos), e é identidade estável entre sessões | contradiz o *"— P1"* que o mesmo card mostra hoje |
| **O `player`** | casa com o que o co-op faz e com o que ela vê **no jogo** | a marca rosa mostraria `1`, e cor e número passariam a discordar dentro do mesmo símbolo |
| **Os dois, explicitados** | não esconde nada | é mais texto numa marca que precisa ser pequena |

**Recomendação de PO, e ela é fraca de propósito:** a marca leva o
**`player_slot`**, porque a marca é **cor + número** e a cor já é o `player_slot`
— pôr o outro número dentro faria o símbolo se contradizer sozinho. **Mas a
contradição do card não se resolve na marca; ela se resolve dizendo o que cada
número é.**

> **ISTO É PERGUNTA PARA ELA, e o motivo é específico:** a casa já registrou que
> **ela lê o aparelho melhor do que eu leio o código**, e esta é uma pergunta
> sobre o que o **aparelho** mostra. O LED de número aceso na frente de cada
> controle é a resposta — e ela tem os quatro na mão agora.
>
> **A pergunta exata:** *"olhando os quatro controles agora, o LED de jogador
> aceso em cada um bate com o `player_slot` (a cor) ou com o `player` (o co-op)?"*
>
> Enquanto ela não responde, **o desenho não trava**: a marca usa o
> `player_slot`, que é o único número que a cor já afirma. Se a resposta dela
> for o contrário, o que muda é uma função de resolução, num lugar só.

---

## 3-bis. O que a FOTO mostrou e nenhum relatório disse: três nomes e duas ordens

> **Esta seção foi escrita depois, olhando os PNGs.** O instrumento da seção 4
> passou a existir horas depois desta medição, e o que ele revelou não estava em
> relatório nenhum — **estava só na imagem**.

**A mesma mesa tem TRÊS nomes na mesma janela:**

| onde | como o mesmo controle aparece |
|---|---|
| **card da Status** | `Controle 4 — USB · Jogador 1` |
| **card da Início** | `Controle 4 — P1` |
| **fita do cabeçalho** | `Sony 1 · USB` |

*"Jogador 1"* por extenso, *"P1"* abreviado, e *"Sony N"* — que **nem é o mesmo
número**: a fita numera pelo `player_slot`, e o *"P1"* da Início numera pelo
`player`.

**E a mesma mesa tem DUAS ordens:**

- a **fita** ordena `Sony 1 · Sony 2 · Sony 3 · Sony 4` — crescente por
  `player_slot`;
- os **cards** (Status e Início) ordenam `4 · 1 · 3 · 2` — que é a ordem em que
  os controles chegaram no payload.

**Ela vê a mesma mesa em duas ordens diferentes, com três nomes, sem sair da
janela.**

**Por que isto importa mais do que parece:** a leva inteira quer que ela
*"escolha o personagem"*. Escolher personagem exige que o jogador **1 seja o
mesmo em toda a tela**. Hoje, clicar em `Sony 2` na fita edita um controle que o
card ao lado chama de `Controle 2 — P4`.

**Isto não é entrega nova; é a D-12 com um segundo corpo.** A D-12 pergunta
*qual número vai na marca*; esta seção mostra que **a pergunta vale para a janela
inteira**, não só para a marca — e que a resposta tem de vir junto com **um nome
só** e **uma ordem só**.

---

## 4. O instrumento oficial não consegue fotografar a mesa cheia — e isso é decisão da casa

**`scripts/gui-captura/retratar_abas.py` é cego aos quatro controles por
construção.** O cabeçalho do script (linhas 59-75) declara isso como **garantia
de privacidade**: ele **nunca** fala com o daemon, e lista *"pedir estado ao
daemon vivo (`daemon.state_full`)"* entre o que não fazer. Ele alimenta as abas
com dublês fixos — **Início e "No jogo" com dois controles sintéticos, Status com
um card**.

**Isso foi provado, não suposto:** rodado com os quatro na mesa, **nove dos dez
PNGs saíram byte-idênticos** aos commitados em `874fdda`, de quando ela tinha
**um** controle.

> **RESOLVIDO NO MESMO DIA, horas depois desta medição.** O modo
> `retratar_abas.py --mesa-cheia` passou a existir: ele alimenta o dublê com o
> **fixture versionado**, e por isso **continua sem falar com o daemon** — a
> garantia de privacidade fica intacta, porque a diferença entre os modos é
> apenas a **fonte do dublê**. As doze fotos estão em
> `docs/process/estudos/assets/mesa-cheia/`, e entre elas está a **primeira foto
> do cabeçalho que esta casa já teve**. O parágrafo abaixo fica como registro do
> que estava travado, e do porquê.
>
> **E ele mediu o que faltava:** os quatro cards pedem **1844 px** e a aba
> inteira pede **2055 px**, contra os 1080 disponíveis. *(O número era 1774 nesta
> página; foi **substituído** pelo medido no caminho de produção — a diferença é
> o que o card real traz a mais.)* **Não cabem nem com a janela maximizada.**

**A consequência para a ONDA 2 é grande e tem de ser dita antes de alguém tentar:
não existe hoje instrumento que fotografe a janela dela com quatro controles.**
As fotos que a
[PROVA-DE-TELA-01](../sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
exige, para uma leva cujo assunto **é** a mesa cheia, precisam de um caminho novo.
E ele **não pode** ser "fazer o script falar com o daemon" — isso desfaria uma
garantia deliberada.

**O caminho que respeita as duas coisas:** o dublê do script passa a poder ser
**alimentado pelo fixture** commitado em `6d2346a` — que é payload real, já
anonimizado pelos portões de `tests/`. A privacidade fica preservada (nada sai do
daemon na hora da foto) e a foto passa a mostrar quatro controles.

> **Efeito colateral medido, e vale para quem rodar o script:** ele **sempre**
> suja `docs/usage/assets/readme_inicio.png`, mesmo sem nenhuma mudança. São 2998
> pixels de 2,07 M, com delta máximo de **1** por canal — jitter de antialiasing,
> não conteúdo. Um `git status` sujo depois de rodar o script oficial **não** é
> sinal de que a tela mudou.

---

## 5. Os números que esta medição corrigiu

**Fato errado se substitui.** Os dois abaixo já foram corrigidos no índice.

| onde | dizia | é | por quê |
|---|---|---|---|
| índice, nota da 2.13 | *"quatro cards pedem **1626 px**"* | **1774 px** | medido offscreen reproduzindo o que o produto monta (`status_actions.py:1216,1239`, com `compact=False` e `mostrar_estado_global=False` a partir de 2 controles): 439 px por card + 6 de espaço; 439×4+18 = 1774, estável entre 760 e 1920 px de largura |
| índice, entrega 2.5 | *"a aba Gatilhos é **byte-idêntica** com um ou com quatro controles"* | **impreciso** | o **cromo** não nomeia controle nenhum, mas `app/actions/triggers_actions.py:150-167` repinta o modo selecionado a partir de `effective_triggers_for(_edit_target_uniq)`. **O botão aceso muda ao trocar de alvo — e nada na tela diz de quem ele é.** A conclusão da 2.5 fica de pé; a palavra não |

**E 1774 é PISO**, não teto: não inclui o frame *"Estado"* (que volta a aparecer
com 2+ controles), a fita de chips nem o seletor de número. **A decisão de 02/08
sobre empilhar os cards ficou ainda mais cara do que a nota da 2.13 calculava** —
o que reforça que a 2.13 é pergunta dela, não tarefa.

---

## 6. Duas suspeitas, marcadas como suspeitas

**SUSPEITA-A — o giroscópio só flui pelo cabo.** Nas duas amostras, os dois
controles USB tinham `motion_streaming: true` a 162-184 Hz, e os dois Bluetooth,
`false` e `0,0 Hz`. **Divisão perfeita por transporte — e é n=2 contra n=2.**
Cabe uma linha no `docs/data/mapa-controles.csv` como **suspeita a testar**,
nunca como afirmação forte: com quatro aparelhos, "todos os do cabo" e "todos os
que eu liguei primeiro" são a mesma amostra.

**SUSPEITA-B — `native_bt_fragil` veio `false` com dois BT na mesa.** A entrega
**1.7** existe porque esse aviso é **global** e cala para os controles 2, 3 e 4
quando o primário está no cabo. **A medição de hoje é consistente com o defeito
descrito** — havia dois no BT e o aviso estava desligado —, mas **não o prova**:
`false` também é o valor correto se nenhum dos dois estivesse frágil. Quem
executar a 1.7 tem esse caso real para conferir.

---

## 7. O que esta medição NÃO mediu

- **Nada foi escrito no aparelho.** Todo veredicto é sobre o que o produto
  **relata**, não sobre o que ele **faz** quando ela clica.
- **A janela não foi aberta na frente dela.** As fotos saíram do caminho
  offscreen, com o dublê do script — que, como a seção 4 mostra, não é a mesa
  cheia.
- **Nenhum externo estava na mesa.** A **D-7** decidiu que o 8BitDo e o Pro
  Controller entram na faixa; isso **continua não medido**.
- **Ninguém tinha pintado cor à mão.** As duas fontes de cor concordaram por
  repouso, não por acordo — ver a seção 1.
