# NAVEGAR ESTA JANELA-01 — a decisão já está tomada, e o dado já está no fio

- **Escrito em:** 15/08/2026, entre 17h40 e 18h10, na branch
  `restauro/inicio-da-sessao`, sobre `4422245`.
- **Grau:** **PROPOSTA DE TELA.** Não é entrega. A
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
  governa esta fase: interface só fecha com o olho dela. O que esta página
  entrega é o estado de hoje fotografado, o desenho do que a decisão pede, o
  preço medido, e **as duas perguntas que sobraram**.
- **A frente:** a **D-19** e o que sobrou da **onda C** (interface).
- **O que ele NÃO faz:** nenhuma linha de código foi escrita, nenhum arquivo de
  produto foi tocado, nenhuma foto do repositório foi sobrescrita.

---

## 0. A correção que economiza a próxima busca

A tarefa que abriu esta frente dizia que a **D-19 aparece no bloco das sete mas
NÃO está na tabela de respostas**. **Está.** É a **linha 21** de
[AS DECISÕES — RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md), a segunda
linha da tabela, logo abaixo da D-30.

Fica registrado para ninguém repetir a busca: a D-19 foi respondida às
**16:46:42 de 15/08/2026**, na mesma rodada de quatro perguntas que respondeu a
D-30, a D-31 e a máscara do gamepad.

---

## 1. A resposta dela, literal

A pergunta, como foi feita:

> **D-19** — *"Navegar a janela do Hefesto" e "comandar o PC" são a mesma coisa
> ou duas? A resposta "duas" derruba de 960 a 1200 min de trabalho.*

A resposta dela, literal:

> **"Duas coisas (Recomendado)"**

E o texto da opção que ela escolheu, que é o que ela leu ao escolher — é ele que
define o escopo, não a minha prosa depois:

> *"A aba Navegação ganha duas seções: 'Comandar o PC' (as colunas de hoje,
> intactas) e 'Navegar esta janela'. Os QUATRO navegam a janela ao mesmo tempo.
> Navegar a janela não passa por uinput, então a objeção dos quatro cursores não
> se aplica."*

Ela confirmou o fechamento da leva na mesma conversa, às 16:46:55:

> *"Leva 1 fechada. D-30 = (b), D-19 = duas coisas, D-31 = série inteira,
> máscara = por jogador."*

**A metade que a D-19 NÃO tocou:** *"comandar o PC"* continua exatamente como a
[D-10](../2026-08-14-DECISOES-DE-PO-as-onze-respostas-da-mesa-cheia.md) deixou —
cursor e teclado do sistema, um só, para todos. Os ~960 a 1200 min que caíram
caíram **só** da metade de dentro da janela.

---

## 2. O estado de hoje, fotografado

![A aba Navegação hoje](../../usage/assets/readme_navegacao_dsx.png)

**A foto é a tela de agora, e isso foi provado duas vezes:**

1. nenhum commit e nenhum arquivo sujo tocou `src/…/gui/` ou `src/…/app/` desde
   que os PNGs foram gerados (03:12 de hoje);
2. rodei `retratar_abas.py` às 17:53 **para um diretório de rascunho**, sem
   sobrescrever nada, e comparei byte a byte: **as dez abas saíram idênticas**
   às versionadas.

Por isso não disputei a captura com as outras frentes que rodam agora — a
resposta já estava no disco, e conferi que estava certa em vez de supor.

**O que a aba tem hoje, duas colunas lado a lado:**

| coluna | conteúdo |
|---|---|
| **Emular mouse** (esquerda) | interruptor, Velocidade do cursor (6), Velocidade da rolagem (1), e a caixa **Mapeamento** com oito linhas |
| **Emular teclado** (direita) | interruptor, *Atalhos de teclado do perfil ativo*, a lista (vazia) e três botões: Adicionar, Remover, Voltar ao padrão |

**As oito linhas do Mapeamento, como estão na tela:** Cruz (X) ou L2 → Botão
esquerdo · Triângulo (△) ou R2 → Botão direito · R3 → Botão do meio · Círculo
(○) → Enter · Quadrado (□) → Esc · D-pad → Setas do teclado · Analógico esquerdo
→ Movimento do cursor · Analógico direito → Rolagem vertical e horizontal.

**As duas medidas de geometria, e elas decidem o desenho:**

| medida | valor | como foi medida |
|---|---|---|
| altura que a aba **pede** | **454 px** | `get_preferred_height()` num `Gtk.OffscreenWindow` no enquadramento dela |
| faixa **vazia** no pé da foto | **487 px** (45% da imagem) | última linha com conteúdo em `readme_navegacao_dsx.png` é `y=591`; abaixo dela só o fundo `(33,34,44)` até a borda da janela em `y=1079` |

**Ou seja: quase metade da aba não mostra nada hoje.** A seção nova cabe onde já
há espaço, sem empurrar uma linha do que existe — que é exatamente o que a
resposta dela exige (*"as colunas de hoje, intactas"*).

**O que a foto NÃO mostra**, e é honesto dizer: o `header_bar` fica fora do
recorte das dez fotos (armadilha registrada em
[COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md)). O badge *"Navegando: …"* da
entrega 3.5 moraria lá, e **nenhuma foto desta casa o alcança** — só o
`--mesa-cheia`, que fotografa o cabeçalho à parte.

---

## 3. O que a decisão pede, em desenho

A aba passa a ter **duas seções empilhadas**, com o mesmo nome de aba. Nada do
que está hoje se move: as duas colunas viram o conteúdo da primeira seção.

```
┌─ Navegação ──────────────────────────────────────────────────────────────┐
│                                                                          │
│  COMANDAR O PC                          (intacto — é a aba de hoje)      │
│  ┌────────────────────────┬───────────────────────────────────────────┐  │
│  │ Emular mouse      [ ]  │ Emular teclado                      [x]   │  │
│  │  Velocidade do cursor  │  Atalhos de teclado do perfil ativo       │  │
│  │  Velocidade da rolagem │  ┌─────────────────────────────────────┐  │  │
│  │  ┌──────────────────┐  │  │                                     │  │  │
│  │  │ Mapeamento       │  │  └─────────────────────────────────────┘  │  │
│  │  │  X/L2 → esquerdo │  │  [Adicionar] [Remover] [Voltar ao padrão] │  │
│  │  │  … 8 linhas …    │  │                                           │  │
│  │  └──────────────────┘  │                                           │  │
│  └────────────────────────┴───────────────────────────────────────────┘  │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────   │
│                                                                          │
│  NAVEGAR ESTA JANELA                    (novo — os 487 px que sobram)    │
│                                                                          │
│   Os quatro controles navegam esta janela ao mesmo tempo.                │
│   Não passa pelo mouse nem pelo teclado do sistema.                      │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐     │
│   │  R1          →  aba da direita     (dá a volta na última)      │     │
│   │  L1          →  aba da esquerda    (dá a volta na primeira)    │     │
│   │  D-pad       →  anda pelos campos desta aba                    │     │
│   │  Cruz (X)    →  escolhe            (não chega ao jogo)         │     │
│   │  Círculo (○) →  volta à tira de abas                           │     │
│   └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
│   Fora desta janela, R1 e L1 voltam a ser Alt+Tab e Alt+Shift+Tab.       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Cada linha do quadro novo é uma decisão dela já tomada**, não invenção minha:

| linha do desenho | de onde vem |
|---|---|
| existir a seção separada | **D-19** — *"duas coisas"* |
| os quatro ao mesmo tempo | **D-19** — *"os QUATRO navegam a janela ao mesmo tempo"* |
| R1/L1 em carrossel | **D-21** — *"R1 vai para a aba da direita, L1 para a esquerda, em CARROSSEL (dá a volta)"* |
| círculo volta à tira de abas | **D-21** — *"círculo volta à tira de abas"* |
| a frase do rodapé sobre Alt+Tab | **D-20** — *"dois significados, decididos pelo foco"*, e ela pediu que isso **esteja dito na tela** |
| X escolhe e não chega ao jogo | **D-22** — *"roubado, só os quatro botões, só do dono da navegação"* |

**A coerência entre D-20 e D-21 está medida, não suposta.** Hoje, em
`core/keyboard_mappings.py` linhas 44-45, os padrões são literalmente:

```python
"l1": ("KEY_LEFTALT", "KEY_LEFTSHIFT", "KEY_TAB"),
"r1": ("KEY_LEFTALT", "KEY_TAB"),
```

Ou seja: **o L1 que a D-21 quer para "aba da esquerda" já tem dono** — é o
Alt+Shift+Tab, irmão do R1 que a D-20 nomeia. As duas decisões dela se encaixam
sem sobra: dentro da janela os dois são abas, fora são troca de aplicativo. Não
há pergunta aberta aqui.

---

## 4. O que torna isto barato: o dado JÁ ESTÁ no fio

**Medido hoje às 17:50, com os quatro controles dela na mesa e o daemon vivo
desde 14:15:57.** Não é estimativa.

O `daemon.state_full` **já publica os botões de cada controle, separadamente**,
e já publica os quatro:

```
idx=0 primary=True  slot=1 transport=usb  tem_inputs=True  buttons=[]
idx=1 primary=False slot=4 transport=usb  tem_inputs=True  buttons=[]
idx=2 primary=False slot=2 transport=bt   tem_inputs=True  buttons=[]
idx=3 primary=False slot=3 transport=bt   tem_inputs=True  buttons=[]
```

(`buttons` vazio porque ninguém estava com a mão nos controles às 17:50 — o
campo existe e a CLI já o consome; o que se prova aqui é que **há um bloco
`inputs` por controle**, nos dois transportes.)

| medida | valor |
|---|---|
| tamanho de uma resposta `daemon.state_full` | **11 631 bytes** |
| latência da chamada (10 amostras) | **mín 1,0 ms · mediana 1,2 ms · máx 1,6 ms** |
| taxa de renovação **efetiva por controle**, medida sem `sleep` na fronteira do IPC (2 295 chamadas em 2,00 s) | **cabo: 242 e 250 Hz** · **rádio: 177 e 141 Hz** |

**A conclusão que isso autoriza, e é a que barateia a leva:** a metade cara de
*"navegar a janela"* — um leitor por controle, botões separados por endereço,
nos dois transportes — **já existe e já está de pé**. A D-19 não pede um canal
novo; pede que a GUI **consuma** o que o daemon publica há tempo, e que a aba
diga isso na tela.

E confirma a premissa que sustentou a recomendação: **nada disto passa por
uinput.** A GUI mexe na própria página e na própria cadeia de foco. Os quatro
cursores virtuais que custariam 960-1200 min não aparecem em lugar nenhum deste
caminho.

---

## 5. Os três preços que a foto não mostra

Estes são os custos reais, e nenhum deles estava escrito antes desta página.

### 5.1 O tique de 10 Hz **só existe na aba Status** — e este é o bloqueio

`app/actions/status_actions.py`, no `_tick_live_state`:

```python
notebook = self._get("main_notebook")
if notebook is not None and id_da_pagina_corrente(notebook) != ABA_STATUS:
    return True
```

É a cura `BUG-STATUS-TICK-HIDDEN-TAB-01`, e o comentário dela diz por quê:
*"com outra aba à vista, 10 Hz de state_full só saturam o worker
compartilhado"*. Fora da aba Status sobra o poller lento de **2 Hz**
(`STATE_POLL_INTERVAL_MS = 500`).

**Consequência direta para a D-19:** hoje, se ela estiver na aba Lightbar, **o
estado de botão dos controles não chega à GUI a 10 Hz**. Navegar a janela exige
o contrário exato do que essa otimização faz — o feed tem de existir **em toda
aba**, porque é justamente para sair da aba corrente que o R1 serve.

Isto não é um detalhe de implementação: é a diferença entre a seção nova
funcionar e ela ser um quadro de texto bonito que não obedece.

### 5.2 A 10 Hz, um toque cabe inteiro entre dois tiques

Os números da §4 põem o gargalo num lugar claro: **o fio anda a 141-250 Hz e a
GUI lê a 10 Hz.** Uma janela de tique dura 100 ms. Um toque de botão curto —
apertar e soltar dentro dos mesmos 100 ms — **é invisível** para quem lê nível
em vez de borda, e some sem erro nenhum.

Há duas saídas, e elas têm preços muito diferentes:

| saída | custo medido | o que quebra |
|---|---|---|
| **subir o tique da GUI** para 30-60 Hz | 11 631 B × 30 = **349 kB/s**; × 60 = **698 kB/s** no socket, e o mesmo worker único que a cura de 5.1 protegia | reabre exatamente o defeito que `BUG-STATUS-TICK-HIDDEN-TAB-01` fechou |
| **o daemon publicar um contador de bordas** por botão e por controle, e a GUI ler a diferença | o daemon já vê os 141-250 Hz; o contador cabe no bloco `inputs` que já existe | nada — a GUI pode ficar nos 10 Hz e **não perde um toque**, porque conta em vez de olhar |

**Recomendação: o contador de bordas.** É a única das duas que respeita a cura
de 5.1 em vez de desfazê-la, e é a mais barata das duas no fio.

### 5.3 Não existe chamada leve — só o `state_full` inteiro

O registro de métodos do IPC (`daemon/ipc_server.py`) tem **`daemon.state_full` e
mais nada** que carregue `inputs`. Quem quiser o botão de um controle paga os
11 631 bytes inteiros, com varredura de sysfs, bateria, áudio e o resto.

Isso **não bloqueia** a D-19 (a 10 Hz, 116 kB/s é barato e a mediana é 1,2 ms),
mas é o que torna a saída "subir o tique" cara de verdade — e é por isso que ela
está escrita aqui, e não descoberta por alguém em 349 kB/s.

---

## 6. O custo em arquivos, e o risco

| # | onde | o que muda | risco |
|---|---|---|---|
| 1 | `src/…/gui/main.glade` | a aba `tab_navegacao_dsx` vira duas seções; as duas colunas de hoje descem inteiras para dentro da primeira, **sem uma propriedade alterada** | **baixo** — é remanejo de contêiner; há 487 px livres, nada é espremido |
| 2 | `src/…/app/actions/` (arquivo novo, `navegacao_actions.py`) <!-- ref-externa: o arquivo ainda NÃO existe; propô-lo é o assunto desta linha --> | a máquina que lê `inputs.buttons` por controle e mexe em página e foco | **médio** — é o código novo da leva |
| 3 | `src/…/app/actions/status_actions.py` | o tique rápido deixa de ser exclusivo da aba Status (§5.1) | **médio-alto** — mexe numa cura existente; a mordida de regressão é obrigatória |
| 4 | `src/…/daemon/ipc_handlers.py` | contador de bordas por botão no bloco `inputs` (§5.2) | **baixo** — campo novo, aditivo; nenhum consumidor de hoje o lê |
| 5 | `src/…/daemon/subsystems/coop.py` **linha 1549** | `forward_buttons(snap.buttons_pressed)` passa a subtrair os quatro botões de face do dono da navegação (D-22) | **baixo** — é literalmente uma linha, e o índice de 14/08 já a tinha localizado |
| 6 | `src/…/daemon/subsystems/gamepad.py` **linha 2039** | o irmão da 5, para o controle primário | **baixo** |
| 7 | `docs/usage/interface.md` + `docs/usage/assets/` | a foto nova da aba, gerada por `retratar_abas.py` | **zero** |

**O que este custo NÃO inclui:** o badge *"Navegando: …"* da entrega 3.5, que
mora no `header_bar` e **depende da pergunta 8.1 abaixo**. Não estimei o que
ainda não tem desenho.

---

## 7. As mordidas, e cada uma tem de reprovar com a cura arrancada

Teste que passa com a cura arrancada não testa nada. Estas são as quatro que
esta frente precisa, com o que se arranca em cada:

| # | a mordida | arranque isto e ela tem de reprovar |
|---|---|---|
| 1 | **a borda, não o nível**: três estados seguidos com o R1 pressionado avançam a aba **exatamente uma vez** | a detecção de borda — sem ela a aba dispara 10 vezes por segundo |
| 2 | **o foco manda**: com a classe de janela `"unknown"` (o valor medido quando o jogo está em foco), o predicado **não** libera a navegação | a comparação de classe — é o Alt+Tab dentro do jogo de que ela reclamou em 29/07 |
| 3 | **o tique vive fora da Status** (§5.1): com a aba Lightbar corrente, o estado de botão continua chegando | o `return True` novo — e o teste irmão tem de garantir que a **saturação** que a cura antiga evitava não voltou |
| 4 | **o X não vaza** (D-22): com o jogador 2 como dono da navegação, o vpad **dele** não recebe `cross` e o do jogador 3 recebe | a subtração na linha 1549 do `coop.py` |

A mordida 3 é a mais importante e a que ninguém escreveria sozinho: ela é a
única que protege a cura que esta leva mexe.

---

## 8. As duas perguntas que sobraram para ela

A D-19 está respondida. Estas duas **nascem dela** e não estavam em nenhuma
lista — são o que aparece quando se tenta desenhar a resposta.

### 8.1 Os quatro navegam juntos. Então o que a tela mostra: um dono, ou quatro?

**Por que a pergunta existe, e não é fabricada:** três decisões dela falam do
mesmo pixel e não dizem a mesma coisa.

- a **D-19** diz *"os QUATRO navegam a janela ao mesmo tempo"*;
- a **D-22** diz *"só do dono da navegação"* — **no singular**;
- a **entrega 3.5** do índice de 14/08 desenha um badge *"Navegando: Sony 3 ·
  BT"* — **também no singular**.

As três **cabem juntas** com uma leitura: *"ao mesmo tempo"* quer dizer que
ninguém precisa de vez nem de permissão, e o *"dono"* é só o rótulo de **quem
agiu por último**, usado para decidir de quem roubar os quatro botões. Mas essa
leitura é minha, e ela decide o que a tela mostra.

| resposta | o que aparece na tela | custo | o que se perde |
|---|---|---|---|
| **(a) nenhum badge** | ninguém é anunciado; os quatro simplesmente agem | **zero** — a entrega 3.5 sai da leva | quem apertou não recebe confirmação nenhuma de que foi ele |
| **(b) badge de quem agiu por último** | *"Navegando: Sony 3 · BT"*, trocando de nome conforme quem mexe | **baixo** — o molde do *"Editando: …"* já está no `header_bar` | com dois mexendo junto o badge pisca entre dois nomes, e vira ruído |
| **(c) quatro marcas, uma por controle, na cor de cada um** | a mesa inteira presente; acende a marca de quem acabou de agir | **médio** — widget novo, mas **deriva do léxico que já existe**: é a mesma ideia da D-17 (os botões 1 2 3 4 na cor de quem ocupa) e da D-18 (a cor é identidade) | nada que eu tenha medido |

**Recomendação: (c)**, e o motivo é a coerência com o que ela já decidiu. A D-18
fixou que **cor = identidade** e a D-17 que os quatro números mostram **a mesa
inteira em quatro cores**. Um badge singular na mesma janela diria o contrário
das duas. E (c) é a única das três que **mostra** o que a D-19 decidiu — que são
quatro, juntos.

**Depende da D-15/D-16 estarem em pé:** sem a cor por unidade na tela, (c) não
tem com que pintar. Se a cor não chegar, (b) é o rebaixamento honesto.

### 8.2 Dois apertam no mesmo instante e mandam para lados opostos. Qual ganha?

A janela tem **uma** aba corrente. Se o P1 manda R1 (direita) e o P3 manda L1
(esquerda) dentro do mesmo tique de 100 ms, alguma coisa tem de acontecer.

| resposta | o que ela vê | custo | o preço |
|---|---|---|---|
| **(a) os dois valem, na ordem em que chegam** | a aba anda e volta — **parece travada**, e ninguém entende por quê | zero | é o único dos três que produz um defeito que ela vai relatar |
| **(b) o primeiro do tique ganha, o resto do tique é ignorado** | a aba anda uma vez, na direção de quem chegou antes | zero | um aperto some sem aviso, mas nada trava |
| **(c) quem mexe primeiro trava a navegação por ~250 ms** | previsível, e ninguém disputa no meio do gesto | baixo | é *"um dono por vez"* por 250 ms — a única coisa que a D-19 recusou, ainda que por um quarto de segundo |

**Recomendação: (b).** É a mais barata, não trava nada, e **não reintroduz o
dono por vez** que a D-19 derrubou. O preço — um aperto perdido em colisão
exata — só aparece quando duas pessoas mandam para lados opostos no mesmo
décimo de segundo, e nesse caso não existe resposta certa mesmo.

**Honestidade sobre esta pergunta:** eu **não medi** com que frequência isso
acontece de verdade, porque medir exige quatro mãos na mesa. Se ela achar a
pergunta pequena demais para gastar tempo, **(b) é o padrão que eu implemento
sem perguntar de novo** — é reversível numa linha.

---

## 9. O CENSO da onda de interface — D-16 a D-22

Este censo existe para que a próxima sessão **não recomece do zero**. Estado
real, conferido no código e no disco em 15/08 às 18h00.

**Legenda de "tem código?":** *nenhum* = zero linha em `src/`.

| # | a decisão | respondida? | tem código? | tem sprint? | tem foto? |
|---|---|---|---|---|---|
| **D-16** | onde a cor mora: **da PEÇA, porque a cor mora no APARELHO**, sem arquivo por endereço | **sim** (tabela, linha 25) | **nenhum** em `src/` — `grep` por `cor_do_plastico`/`colorway` em `src/` dá zero; o que existe é o instrumento `scripts/ensaios/cor_do_plastico.py` (45 KB), que é bancada | sim, junto da D-15 em [UNIDADE-COR-01](2026-08-15-UNIDADE-COR-01-o-controle-sabe-de-que-cor-ele-e.md) | **não** — nenhuma foto mostra cor por unidade |
| **D-17** | os botões 1 2 3 4 com **a cor de quem ocupa** | **sim** (linha 26) | **nenhum** — os chips e a faixa *"Número deste controle"* são montados em Python (`app/actions/status_actions.py`), sem id de widget e **sem cor por unidade** | só a entrega 3.2 do [índice de 14/08](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md) | **não** — moram no `header_bar`, fora do recorte das dez fotos |
| **D-18** | **anel por dentro** para a seleção; borda = identidade | **sim** (linha 26) | **nenhum** — o `theme.css` ainda tem `button:checked { border-color: @purple }` (linha 209), que é a colisão que a decisão resolve | só a entrega 3.1 do índice de 14/08 | **não**, pelo mesmo motivo da D-17 |
| **D-19** | **duas coisas** — os quatro navegam a janela ao mesmo tempo | **sim** (linha 21, e literal na §1 desta página) | **nenhum** — a aba tem só as duas colunas de *"comandar o PC"*. **Mas o dado já está no fio**: `inputs.buttons` por controle, quatro na mesa, 141-250 Hz (§4) | **esta página** | **sim** — `readme_navegacao_dsx.png`, conferida byte a byte hoje às 17:53 |
| **D-20** | o R1 com **dois significados, decididos pelo foco** | **sim** (linha 33) | **metade** — o R1 = Alt+Tab existe e é padrão (`core/keyboard_mappings.py:45`); o **segundo** significado não existe, e o predicado de foco que ele precisa **já existe** em `daemon/subsystems/game_signal.py` (leitura crua, nunca a pegajosa) | só a entrega 3.4 do índice de 14/08 | **sim** — a coluna Mouse da foto, que mostra que R1/L1 **não estão** no Mapeamento |
| **D-21** | círculo volta à tira de abas; **R1/L1 em carrossel** | **sim** (linha 34) | **metade** — o L1 = Alt+Shift+Tab é padrão (`keyboard_mappings.py:44`) e o círculo = Enter está na tela; nenhum dos dois verbos novos existe | só a entrega 3.4 | **sim** — as oito linhas do Mapeamento estão legíveis na foto |
| **D-22** | **roubado, só os quatro botões, só do dono da navegação** | **sim** (linha 32) | **nenhum** — o que existe é `_emulation_suppressed`, que é **da sessão** e desliga mouse/teclado, não é máscara de botão por jogador. O ponto exato da cura está localizado: `coop.py:1549` (`forward_buttons`) e `gamepad.py:2039` | só a entrega 3.6 | **não** — é comportamento, não desenho |

**As três leituras que o censo autoriza:**

1. **As sete estão respondidas. Nenhuma das sete tem código.** O bloco continua
   sendo o maior parado da leva — mas por falta de execução, não de decisão.
2. **A D-19 é a mais barata das sete**, e é a única cujo dado já está de pé e
   medido. As outras seis dependem de coisa que ainda não existe (a cor no
   produto, para D-16/17/18) ou de uma máquina que ainda não foi escrita (para
   D-20/21/22, que só ganham sentido **dentro** da seção que a D-19 cria).
3. **A ordem que isso impõe é uma só:** a D-19 primeiro, porque D-20, D-21 e
   D-22 são o **conteúdo** da seção que ela abre. Fazer qualquer uma das três
   antes é escrever verbo sem lugar onde morar. E o trio D-16/17/18 anda em
   paralelo, porque depende da cor e não da navegação.

---

## 10. Como cada afirmação desta página foi conferida

| afirmação | como foi conferida |
|---|---|
| a D-19 está na tabela de respostas, linha 21 | `Read` de `docs/process/2026-08-15-AS-DECISOES-RESPONDIDAS.md` |
| a resposta literal e a hora | extrator do transcrito `3706fe35-…jsonl`, entradas de 16:44:55 (a pergunta com as opções) e 16:46:42 (o `toolUseResult` com a escolha) |
| a foto é a tela de agora | `git log --since` e `git status` em `src/…/gui/` e `src/…/app/` (ambos vazios) **mais** `cmp` das dez PNGs contra uma captura nova em diretório de rascunho — dez idênticas |
| 454 px pedidos / 487 px vazios | `get_preferred_height()` em `Gtk.OffscreenWindow` com animações desligadas; e varredura de linhas do PNG com `GdkPixbuf`, fundo medido em `(33,34,44)`, última linha com conteúdo `y=591` |
| 11 631 bytes, 1,2 ms, 141-250 Hz, quatro controles com `inputs` | dez e depois 2 295 chamadas a `daemon.state_full` via `app/ipc_bridge.py`, com o daemon vivo desde `Sat 2026-08-15 14:15:57` |
| o tique de 10 Hz é exclusivo da aba Status | leitura de `_tick_live_state` em `app/actions/status_actions.py` e de `LIVE_POLL_INTERVAL_MS`/`STATE_POLL_INTERVAL_MS` em `app/constants.py` |
| não existe chamada IPC leve | leitura do registro de métodos em `daemon/ipc_server.py` |
| R1/L1 já têm dono | `core/keyboard_mappings.py`, linhas 44-45, lidas no fonte |
| a linha única do D-22 | `coop.py:1549` (`forward_buttons(snap.buttons_pressed)`) e `gamepad.py:2039`, lidas no fonte |
| "nenhum código" nas sete | `grep` em `src/` por `cor_do_plastico`, `colorway`, `box-shadow: inset` de seleção, e leitura de `theme.css:204-219` |

**O que esta página NÃO conferiu, e ninguém deve supor que sim:** não apertei
botão nenhum (o campo `buttons` saiu vazio nas 2 295 amostras porque ninguém
estava com a mão nos controles); não medi a frequência real de colisão da
pergunta 8.2; não abri janela de verdade; não toquei em aparelho; não reiniciei
serviço nenhum.
