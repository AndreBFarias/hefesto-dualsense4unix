# LINGUA-DO-PRODUTO-01 — o convite a traduzir era falso

- **Achado em:** 31/07/2026, na entrega E6 da
  [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md),
  que mediu o alcance real do catálogo e deixou a saída em aberto por não ser
  dela a escolha
- **Decidido em:** 07/08/2026, resposta 10 do painel — **"não; português é a
  língua do produto"**
  ([as onze respostas](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md))
- **Estado:** **CURA APLICADA** nesta leva — o convite saiu das três páginas,
  a verdade entrou no lugar, e o portão que impede a volta existe e morde
- **Gravidade:** **MÉDIA** no efeito técnico e **ALTA** no custo alheio: o
  convite não quebrava nada nesta máquina; quebrava o fim de semana de quem o
  aceitasse. Traduzir os catálogos inteiros e ver a janela continuar em
  português é trabalho perdido que o projeto tinha prometido que valeria
- **Causa-raiz:** **MEDIDA**. Não é bug de código: é uma promessa que era
  verdadeira quando foi escrita (v3.4.0, quando o esqueleto era quase toda a
  interface) e que o crescimento das abas foi tornando falsa sem que ninguém
  tocasse na frase
- **Parentes, e distintas:**
  - [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md)
    — a E6 é a origem desta sprint. Ela ofereceu **duas** saídas (dizer o
    alcance, ou ligar o encanamento) porque não sabia qual delas era a dela.
    Esta sprint executa a terceira, que só ela podia escolher: **assumir o que
    o produto já é**;
  - [JANELA-QUE-RESPIRA-01](2026-08-01-JANELA-QUE-RESPIRA-01-os-consertos-de-largura-que-a-casa-ja-tinha-decidido.md)
    — mediu que `scripts/i18n_extract.sh` **destrói** tradução manual ao
    reextrair. É defeito do encanamento, continua **ABERTO**, e continua valendo:
    esta decisão não o cura nem o dispensa;
  - [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md)
    — o precedente de vocabulário: os dezenove rótulos de gatilho nasceram em
    português cravado, e foi decisão, não descuido.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há contagem
reproduzível ou teste que reprova com a cura arrancada; **SUSPEITA COM
MECANISMO** = o caminho foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou.

---

## O defeito: três páginas prometendo o que a quarta não entrega

Até 07/08/2026, três páginas do projeto convidavam gente de fora a acrescentar
um idioma, e duas delas traziam a receita completa:

| página | o que trazia |
|---|---|
| `.github/CONTRIBUTING.md` | seção "Contribuir traduções": cinco passos, glossário e convenções de tom |
| `docs/usage/troubleshooting.md` | seção "Adicionar idioma novo (comunidade)": receita de três linhas |
| `docs/usage/flatpak.md` | o ponteiro — *"Para adicionar um novo idioma (ES, FR, DE, etc.), ver..."* |

O que nenhuma das três dizia é **até onde a tradução chega**.

### A medição, refeita em 07/08/2026

**MEDIDO.** Contado por leitura de AST dos arquivos de
`src/hefesto_dualsense4unix/app/actions/` — os módulos que escrevem o texto vivo
das abas, o que a janela diz enquanto roda:

| medida | valor |
|---|---|
| módulos em `app/actions/` | **18** |
| que importam `_` de `utils/i18n.py` (ou `gettext`) | **3** |
| que **não** importam e ainda assim carregam prosa acentuada | **15** |
| literais com acentuação portuguesa nesses 15 | **561** |

Os três que traduzem são `footer_actions.py`, `lightbar_actions.py` e
`status_actions.py`. Os outros quinze — `daemon_actions.py` sozinho tem 151
literais acentuados, `emulation_actions.py` e `profiles_actions.py` têm 86 cada
— escrevem português direto.

**Como medi**, para quem quiser repetir sem acreditar em mim: percorro cada
`.py` do diretório com `ast.parse`, procuro um `ImportFrom` cujo módulo contenha
`i18n` importando o nome `_` (ou um `import gettext`), e conto os
`ast.Constant` de texto que casam com `[áàâãéêíóôõúüç]`. É exatamente o que o
portão faz a cada rodada — não há número digitado à mão em lugar nenhum.

**O número 15 confere com o que a DOC-VERDADE-02 mediu em 31/07** por um
critério mais frouxo (só "não importa gettext"). O critério de hoje é mais
estrito — exige também **ter prosa acentuada**, para não contar um módulo que
simplesmente não escreve texto — e chega ao mesmo 15. Duas medições
independentes, mesmo resultado.

**O número 561 é datado, e vai mudar.** Qualquer edição de frase em qualquer um
dos quinze o move. Está escrito nas páginas como medição de 07/08/2026, e o
portão o cobra como **piso**, não como igualdade — o motivo está na seção do
portão, abaixo.

### O outro lado: o que a tradução ALCANÇA

**MEDIDO.** `src/hefesto_dualsense4unix/gui/main.glade` tem **308**
`translatable="yes"`. O esqueleto fixo da janela traduz de verdade, e os
catálogos `po/en.po` e `po/pt_BR.po` funcionam. Quem forçasse `LANG=en_US.UTF-8`
veria os rótulos mudarem e o recado da janela continuar em português — meia
tela em cada idioma, que é pior que uma tela inteira num só.

*(A DOC-VERDADE-02 registrou 309 em 31/07; hoje são 308. Diferença de uma
string em uma semana de mexidas na janela, e nada mais que isso.)*

---

## A decisão dela, e o que ela NÃO autoriza

> **"não — português é a língua do produto"** — 07/08/2026, resposta 10.

O que isso autoriza: **tirar o convite** das páginas onde ele é falso, e pôr no
lugar a verdade, datada e medida.

O que isso **não** autoriza, e está escrito porque a tentação é real:

- **o encanamento de i18n não é removido.** `po/en.po`, `po/pt_BR.po`,
  `scripts/i18n_extract.sh`, `scripts/i18n_compile.sh`,
  `src/hefesto_dualsense4unix/utils/i18n.py`, os 308 `translatable="yes"` e os
  três módulos que já usam `_` continuam onde estão. Ele está **correto**;
  arrancá-lo seria destruir trabalho bom para provar um ponto, e a palavra dela
  na hora de decidir foi exatamente essa;
- **o inglês não é proibido.** Forçar o catálogo EN continua documentado em
  `docs/usage/flatpak.md`, porque funciona para o que funciona. O que saiu foi a
  promessa de que ele entrega uma **janela** em inglês;
- **o convite não é proibido para sempre.** Ele é proibido **enquanto** for
  falso. A condição é medida, não opinada — ver abaixo.

---

## A cura, arquivo por arquivo

### `.github/CONTRIBUTING.md`

A seção "Contribuir traduções" (com a receita, o glossário de tradutor e a
subseção "Atualizar uma tradução existente") deu lugar a **"A língua do
produto"**, que carrega: a decisão datada, a medição que a sustenta, a promessa
explícita de que o encanamento fica, a condição de retorno do convite, e o
nome do portão.

**O que foi preservado da seção antiga, e por quê:** as três linhas do glossário
que dizem *lightbar*, *rumble* e *daemon* **não** se traduzem. Aquilo nunca foi
convenção de tradutor — é **vocabulário do produto em português**, decisão viva,
e a regra da casa é que decisão medida não se apaga. Ficaram, numa tabela que
agora diz o que de fato são.

O resto do glossário (as linhas `perfil/profile`, `atalho/shortcut`,
`controle/controller`, `bateria/battery`, `gatilho adaptativo/adaptive trigger`)
saiu: eram equivalências PT-BR para EN, úteis só a quem traduz, e não descrevem
nenhuma escolha do produto que não esteja já no próprio produto.

### `docs/usage/flatpak.md`

A seção "Localização (i18n)" ganhou, **no topo**, o quadro com a decisão e a
medição. O ponteiro final para a receita da `CONTRIBUTING` virou a afirmação de
que o encanamento continua vivo e correto. O corpo técnico — os caminhos
`/app/share/hefesto-dualsense4unix/locale/`, o motivo do path próprio, o
`BUG-FLATPAK-LOCALE-SYMLINK-01` — **não foi tocado**: é registro medido de um
bug real e continua valendo inteiro.

### `docs/usage/troubleshooting.md`

A seção 11 ganhou o mesmo quadro no topo, com uma frase a mais que é a razão de
alguém abrir uma página de solução de problemas: *"se você chegou aqui esperando
uma janela inteiramente em inglês, o problema não é a sua instalação"*. Os três
sintomas (A, B e C) continuam intactos — são defeitos de **carregamento de
catálogo**, medidos e curados, e a decisão da língua não os revoga. A receita
"Adicionar idioma novo (comunidade)" saiu, e no lugar dela ficou o registro do
que saiu e por quê.

---

## O portão

`tests/unit/test_lingua_do_produto_01_o_convite_a_traduzir.py`.

### O critério, pensado ANTES de escrever

Um portão que procurasse a palavra `traduzir` reprovaria
`docs/usage/integrating-mods.md`, que fala de *"modo de gatilho sem tradução"*
noutro sentido, e o `README.md`, que diz que as curvas prontas *"ainda não têm
tradução"*. Reprovaria também esta própria sprint. Portão que reprova o inocente
é desligado na terceira vez, e a partir daí é decoração.

O que caracteriza o convite **não é o vocábulo — é a receita**. E receita tem
forma: comando, arquivo-alvo, cabeçalho imperativo, ponteiro. Daí as quatro
marcas, cada uma prova sozinha:

| marca | o que é | por que não é ruído |
|---|---|---|
| 1 | `i18n_extract.sh --add` | ninguém escreve o comando que cria idioma sem estar ensinando a usá-lo |
| 2 | um `po/<algo>.po` que **não existe** em `po/` | citar catálogo inexistente é mandar o leitor criá-lo; a lista do que existe é lida do disco, não digitada |
| 3 | cabeçalho markdown na forma *adicionar/criar/contribuir + idioma/tradução* | cabeçalho é o índice de um procedimento; prosa que menciona tradução não vira seção |
| 4 | *"para adicionar um novo idioma..."* e o nome da seção removida | é como a `flatpak.md` empurrava o leitor, sem trazer comando nenhum |

**Escopo:** só os documentos que ENSINAM (`README.md`, `.github/CONTRIBUTING.md`,
`docs/usage/`, `docs/adr/`, `docs/protocol/`). `docs/process/` fica de fora **por
escrito**, pelo mesmo motivo que `scripts/validar-referencias-docs.py` já o
deixa: sprint é registro, e registrar a remoção de uma receita exige
transcrevê-la. Este arquivo aqui é a prova viva disso.

### A metade que a maioria dos portões não tem

O portão é **condicional de verdade**. Ele mede, do código, quantos módulos de
`app/actions/` escrevem português fora da função de tradução; se a resposta for
**zero**, ele libera o convite sozinho, sem que ninguém edite uma linha de
teste. A decisão dela foi contra a **promessa falsa**, não contra traduzir — e
um portão que proibisse para sempre estaria mentindo sobre a decisão que diz
guardar.

O `assert` de volume entrou como **piso** (`>= 400`), não como igualdade. O
valor exato de hoje (561) se move a cada frase editada em qualquer um dos
quinze módulos, e um portão que exigisse o número exato reprovaria trabalho
alheio inocente. O que precisa doer é o volume **desabar** — aí a premissa
mudou e a decisão precisa ser remedida.

### A MORDIDA (07/08/2026)

Três arrancadas, todas verificadas nesta bancada:

1. **Devolvi a receita** ao fim da seção 11 de
   `docs/usage/troubleshooting.md`, com as mesmas linhas que tinham saído.
   `test_nenhuma_pagina_que_ensina_convida_a_traduzir` reprovou apontando
   **três** linhas — o cabeçalho (641), o comando (644) e o `po/fr_FR.po`
   (645) —, cada uma com o motivo por extenso. Devolvi então a linha final,
   que era a que citava a seção pelo nome, e a reprovação virou **quatro**
   (651, ponteiro para a receita);
2. **Devolvi só o ponteiro** da `docs/usage/flatpak.md` — *"Para adicionar um
   novo idioma (ES, FR, DE, etc.), ver o guia de contribuição"* —, uma frase
   sem comando nenhum, que é a forma mais fraca do convite e a que um portão
   preguiçoso deixaria passar. Reprovou sozinha, na linha 266;
3. **Arranquei a condição**: com o ponteiro do passo 2 ainda no lugar, fiz a
   medição do encanamento devolver vazio, como se os 18 módulos já
   traduzissem. Os 43 testes passaram — o portão **ACEITOU** o convite. É a
   metade condicional funcionando; sem isso eu teria escrito um "não"
   permanente e chamado de condição.

Depois das três, devolvi os três arquivos byte a byte a partir das cópias que
tinha feito antes de sabotar, e conferi que nenhuma marca de sabotagem
sobreviveu na árvore.

Além disso, o critério é medido contra si mesmo em dois testes que não olham
para o repositório:
`test_o_criterio_reconhece_o_encanamento_ligado` monta três módulos de mentira
em `tmp_path` (um com `_`, um com prosa crua, um sem prosa) e cobra que só o do
meio conte; `test_o_criterio_enxerga_a_receita_e_ignora_quem_so_fala_de_traducao`
cobra as quatro marcas contra a receita real e o **silêncio** contra um
cabeçalho e seis frases honestas tiradas do próprio repositório — entre elas
*"modo de gatilho sem tradução"*, *"ainda não têm tradução"* e a própria frase
que anuncia esta decisão.

---

## O que fica ABERTO

1. **`scripts/i18n_extract.sh` destrói tradução manual** — medido na
   [JANELA-QUE-RESPIRA-01](2026-08-01-JANELA-QUE-RESPIRA-01-os-consertos-de-largura-que-a-casa-ja-tinha-decidido.md):
   rodar o caminho documentado custou 37 traduções, das quais 34 eram de levas
   anteriores. **Continua aberto.** Esta decisão não o cura, e é bom que se diga:
   se um dia o encanamento for ligado às telas, este defeito é o primeiro
   obstáculo do caminho, não o último.
2. **Ligar o encanamento às telas continua sendo trabalho legítimo** — e agora
   tem um número para perseguir e um portão que percebe quando ele chega a zero.
   Ninguém foi autorizado a começar: é sprint futura, não tarefa desta.
3. **A janela não foi fotografada nesta leva.** Nenhuma linha de
   `src/` foi tocada — a decisão dela não manda mexer no encanamento — então não
   há mudança de tela a mostrar. Se alguém ligar o i18n depois, aí vale a
   [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
   inteira.
4. **`packaging/arch/README.md` e `packaging/nix/README.md`** citam
   `scripts/i18n_compile.sh` como passo de build. Estão **certos** e ficaram
   como estavam: compilar catálogo que existe é encanamento, não convite. O
   portão não os cobre de propósito — não são páginas que ensinam o usuário.

---

## A lição, para a próxima promessa

Esta não era mentira de ninguém. Cada frase era verdadeira no dia em que foi
escrita, e ficou falsa por fora — pelo produto crescendo em volta dela. É a
mesma forma da E7 da DOC-VERDADE-02, onde um campo novo no `DaemonConfig`
tornou três páginas falsas sem que ninguém as tocasse.

A cura, das duas vezes, é a mesma: **a página que afirma um número não pode
guardar o número; tem de derivá-lo do código, ou ter um portão que o derive por
ela.** Aqui o portão deriva, e é por isso que ele solta o convite sozinho no dia
em que a promessa virar verdade.
