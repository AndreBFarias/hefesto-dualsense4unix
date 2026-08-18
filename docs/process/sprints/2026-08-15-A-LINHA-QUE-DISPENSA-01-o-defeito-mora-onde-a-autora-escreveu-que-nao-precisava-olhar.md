# A-LINHA-QUE-DISPENSA-01 — o defeito mora onde a autora escreveu que não precisava olhar

- **Escrito em:** 15/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `97c2cbf`.
- **Grau:** **MEDIDO — sobre o PROCESSO, não sobre o produto.** As seis
  ocorrências abaixo saíram de três rodadas de ceticismo adversarial em 14/08,
  com trinta e cinco agentes, e cada uma tem a citação literal da linha que
  dispensou o resto e a medição que a derrubou.
- **Por que ele existe:** a casa já nomeou *"a casa sabe e o produto não faz"* e
  *"o instrumento mente mais que o produto"*. Este é o terceiro da família e é o
  mais barato de explorar: **quando alguém escreve por que não precisa olhar
  algo, é ali que o defeito está.**
- **Depende de:** nada. Nenhuma linha de `src/`.

---

## 1. O achado, em uma frase

Toda entrega desta casa fecha com um campo `o_que_ficou_de_fora` — a autora
declara o que não olhou e **por quê**. Em três rodadas de ceticismo, **o defeito
que derrubou a entrega estava, seis vezes, exatamente naquela linha.**

Não é coincidência de amostra: é o único parágrafo do relatório que **ninguém
verifica**. O resto do relatório é uma afirmação sobre o que foi feito, e o
cético a confere. A linha que dispensa é uma afirmação sobre o que **não** foi
feito — e ela chega ao leitor como uma decisão já tomada.

---

## 2. As seis ocorrências, com a citação e a medição que a derrubou

### 2.1 — A 1.5, primeira rodada: o pior caso que não era o pior

> *"Nenhuma foto de tela. PROVA-DE-TELA-01 pede o olho dela, e **a frase somada é
> longa (~185 caracteres no pior caso: co-op + alvo fora)**… se a frase composta
> não couber no toast, o corte natural é largar os MOTIVOS"*

**A medição:** o pior caso real é a **trinca** (co-op + Modo Nativo + alvo fora),
**256 caracteres** — e **314** com o prefixo `_AVISO_D4` que o próprio método
compõe (`app/actions/lightbar_actions.py:816-817` e `:1109-1110`). Erro de 70%.

**O custo:** a pergunta foi escalada à PO **dimensionada contra uma frase que o
produto não emite**.

### 2.2 — A 1.5, terceira rodada: o mesmo erro, uma casa decimal adiante

> *"**A de duas pendências cabe raspando (1123 px de 1156)** e deixa de caber
> quando o aviso do D4 entra na frente."*

**A medição:** rótulo real **703 px**, não 1156. A autora mediu a largura da
**janela** e a chamou de largura da **barra de status** — os 415 px dos quatro
botões do rodapé (`gui/main.glade:3756-3833`) nunca foram descontados. **Erro de
1,64x, para o lado otimista.** Cabem **127** caracteres; a de duas pendências tem
182 e **é cortada**.

**O custo:** a decisão foi escalada à PO enquadrada como *"problema exclusivo da
trinca"*, quando o estado que quebra é o que a própria docstring chama de **"o
estado NORMAL da mesa dela"**.

### 2.3 — A 1.4: a impossibilidade declarada que era uma linha de código

> *"por isso **`guardado_em` fica SEMPRE vazio nesta rota: sem carimbo por
> controle não há promessa por-controle a publicar**, e prometer 'vale quando
> voltar' sem dono seria a quinta mentira."*

**A medição, duas vezes:** com o seletor mirando um controle, `_for_each(record=)`
**grava** override por-uniq com dono `usuaria`; e em Modo Nativo e com a mesa
vazia o valor **fica guardado e vale depois** (`_desired_default.trigger_left`
preenchido; depois do desmute o gatilho chega nos dois; depois do hotplug o
controle novo chega armado). A lista verdadeira estava **a uma linha** — é a que
a própria função já calcula em `_uniqs_conectados()`.

**O custo:** a afirmação virou **asserção de teste** —
`tests/unit/test_conserto_1_4_a_rota_classica_diz_onde_pegou.py:224-236`, com a
mensagem *"não há promessa POR CONTROLE a publicar"*. Quem consertar terá de
apagar uma linha que se apresenta como decisão medida.

### 2.4 — A 1.2: o comentário que a autora declarou ter escrito e não escreveu

> *"**Gravei isso como comentário medido e datado em cima da tupla do
> `_build_mixin`**, com as duas contagens, para a próxima pessoa não reaprender."*

**A medição:** `grep` por `"AttributeError"`, `"KeyError"`, `"26 passed"`,
`"29 failed"` na árvore, **no índice e no HEAD**, não devolve nada. O `git diff`
na região da tupla acrescenta **exatamente uma linha**: `+ "_adiantar_live_preview",`.
**O comentário nunca existiu.**

**O custo:** é o **defeito original daquela entrega repetido dentro do conserto
dele** — a entrega existia para acabar com conhecimento que não sobrevive à
sessão, e o relatório afirmou tê-lo gravado sem gravar.

### 2.5 — A 1.11: o andar declarado morto que estava vivo

> *"[o `marca in unidade`] **é o terceiro andar do mecanismo, e o ÚNICO QUE
> SOBRAVA**"* (`tests/unit/test_mesa_cheia_11_a_janela_conta_quatro.py:735-736`)

**A medição:** há um **quarto andar**. `_justificado` (`:676-680`) continua sendo
`marca in oração` sobre a oração **crua**, e uma frase unida por conjunção nua
(`e`, `mas`, `porque`) compra silêncio para a metade vizinha. Provado plantando
quatro frases idênticas no `.glade`, mudando só o conector: **reprovou uma de
quatro** — a da vírgula.

**O custo:** setenta e uma verdes com a mentira na tela.

### 2.6 — A 1.1: a substituição declarada que deixou a linha de pé

> *"Todos os números foram **substituídos** pelo que a régua acima devolve"*

**A medição:** o §10 do documento (linha 624) continuava com *"A medida de **~780
px** diz que cabem"* — a mesma linha do índice e do backup da própria autora. O
valor certo é **764**.

**O custo:** a linha **atravessou as três rodadas** de ceticismo.

---

## 3. Os contra-exemplos, e eles importam tanto quanto

Duas entregas resistiram ao ataque exatamente porque a linha que dispensa
estava honesta:

- **1.11, segunda rodada** — o cético escreveu: *"o `o_que_ficou_de_fora` está
  honesto desta vez"*. As 28 orações e as 24 marcas declaradas conferiam. **O
  defeito estava no mecanismo, não numa linha do relatório** — e por isso a
  refutação foi útil em vez de ser só um flagrante.
- **1.6** — quatro dos cinco itens reproduzem, **dois byte a byte**, e o resíduo
  aberto (a janela de um tique) está **declarado como resíduo**, não dispensado.

**A regra que sai daí:** a linha honesta descreve **o que não foi feito**; a
linha perigosa explica **por que não precisava ser feito**. As duas parecem
iguais no relatório e não são.

E o corolário que dois céticos escreveram no mesmo dia, sem se falar:

> **"quando um docstring novo se gaba de uma capacidade, é ali que o teste
> falta."**

A soma de três pendências, anunciada com todas as letras na docstring de
`frase_de_guardado`, era **a única combinação sem mordida** —
`grep -rn "coop=True.*nativo=True" tests/` devolvia **zero linhas** na suíte
inteira.

---

## 4. As três entregas

Todas de processo. Nenhuma toca `src/`.

| # | entrega | custo |
|---|---|---|
| **E1** | **O cético lê o `o_que_ficou_de_fora` PRIMEIRO.** Hoje o roteiro manda conferir as mordidas e depois olhar o que sobrou. Inverter é grátis e é onde estava o defeito em seis de nove refutações | 10 min |
| **E2** | **Separar os dois campos.** `o_que_ficou_de_fora` (fatos: não rodei X) e `por_que_nao_precisou` (juízos: X não se aplica porque…). Só o segundo é o campo perigoso, e hoje os dois vivem misturados | 20 min |
| **E3** | **Todo número num `por_que_nao_precisou` carrega o comando que o refaz** — a mesma regra que o `ONDE-PARAMOS` já usa (`[COLETA]` x `[APARELHO]`). Um "~185 caracteres" sem comando é um palpite com cara de medida | 20 min |

**A E3 é a que teria pegado quatro das seis.** Os erros de 2.1, 2.2, 2.5 e 2.6
são todos números afirmados sem a receita que os produz.

---

## 5. O teste que MORDE

Este é o item honesto desta sprint: **não há teste automático que morda um juízo
escrito em prosa.** O que dá para morder é a **forma**.

### Mordida 1 — o campo sem receita

**Arrancar:** escrever um `por_que_nao_precisou` com um número e sem comando.

**Por que reprova:** o portão de relatório — que hoje não existe — varre os
campos e cobra que todo `\d+ *(px|caracteres|Hz|ms|bytes)` num campo de
dispensa venha acompanhado de uma linha `refaz:`. É aviso com lista, não portão
cego, e a lista de exceções nasce vazia.

**A ressalva, e ela é real:** isto mora fora do repositório (é formato de
relatório de agente, não código). A entrega honesta é escrever a regra em
`CLAUDE.md` ou no roteiro do cético, **não** fingir que um `pytest` a cobre.

### O que esta sprint NÃO prova

Que o padrão vale fora destas três rodadas. **Seis ocorrências em nove
refutações** é um sinal forte, não uma lei. O que ele já justifica é a E1, que
custa dez minutos e inverte uma ordem de leitura.

---

## 6. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **Se isto vira regra da casa** (uma linha em `CLAUDE.md`, ao lado de *"teste tem de MORDER"*), ou fica sendo só um registro medido | escrever a linha, se ela quiser |
| — | as três entregas, que são de roteiro de agente e não pedem palavra dela |
