# NUNCA-TROCA-O-ALVO-01 — a janela trocava o nome, e o Salvar ia para o arquivo errado

- **Achado em:** 06/08/2026, por **queixa literal dela** — não por auditoria
- **Estado:** **CURA APLICADA**, em três camadas, com testes que mordem
- **Gravidade:** **ALTA** — o defeito **destrói trabalho dela em silêncio**, e o
  agravante composto o torna **permanente pelo resto da sessão**
- **Causa-raiz:** **MEDIDA** em bancada com `Gtk.TreeView` real, antes de
  qualquer linha de cura
- **Índice:** [A leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)
- **Parentes, e distintas:**
  - [PERFIL-REESCRITO-NA-PARTIDA-01](2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md)
    — lá quem reescrevia era o **daemon**; aqui é a **janela**;
  - [ATIVAR-NÃO-MENTE-01](2026-08-05-ATIVAR-NAO-MENTE-01-o-botao-que-parecia-falhar-e-ativava-duas-vezes.md)
    — mesma aba, e a cura dela é **pré-requisito** desta (ver *"O que fica ABERTO"*);
  - [GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md)
    — o funil que esta sprint usa para explicar o **agravante composto**.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O sintoma, nas palavras dela

06/08/2026:

> *"Ainda tá confuso a aba Perfis, nada indica que eu tô alterando o perfil pra
> jogar na hora. Clico em ativar perfil vitória, altero todas as abas esperando
> que esse perfil fique salvo e seja usado no atual momento. Abro o jogo e muda.
> Ou pior: clico em salvar e ele salva com um nome aleatório ou de outro
> perfil."*

Três frases, e cada uma é um defeito diferente. A terceira — *"salva com um
nome aleatório ou de outro perfil"* — parecia a mais improvável das três, e é a
que se reproduziu **por três caminhos independentes**.

## A causa-raiz comum: o editor obedece a um sinal que ninguém emitiu

`_populate_editor` (`app/actions/profiles_actions.py:1901`) reescreve o editor
inteiro, **campo Nome incluído**. Quem o dispara é o sinal `changed` do
`GtkTreeSelection` da lista, ligado em `install_profiles_tab`.

E `changed` **não sabe distinguir quem o emitiu**. O dedo dela e o
`select_iter()` do próprio código chegam pelo mesmo sinal, com a mesma cara.

O `on_profile_save` então lia a **linha selecionada** para responder *"que
perfil eu estou gravando?"*. Resultado: toda vez que a janela mexia na lista por
conta própria, ela **movia o alvo do botão Salvar** — e o campo Nome ia junto,
para que a tela ficasse coerente com a mentira.

**Grau: MEDIDO** (bancada com `Gtk.TreeView` e `Gtk.ListStore` de verdade — um
dublê de lista não emite `changed`, e mediria o dublê em vez da janela).

## Os TRÊS caminhos medidos

### Caminho 1 — o autoswitch, e a volta para a aba Perfis

O mais caro, porque é o uso normal dela:

1. ela ativa `vitoria` na mão;
2. edita a Lightbar, o Rumble, os Gatilhos — as abas gravam **só em
   `self.draft`** (R-08), nada vai para o disco ainda;
3. abre o jogo; o autoswitch do daemon troca o perfil ativo para
   `sackboy_nativo`;
4. ela **volta para a aba Perfis**. O `switch-page` chama
   `_sync_selection_with_active_profile` (`app/actions/profiles_actions.py:787`,
   registrado em `app/app.py:913`), que chama `_select_profile_by_name`, que
   fazia `select_iter()` — e o campo Nome virava `sackboy_nativo`;
5. ela clica **"Salvar este perfil"** achando que salva o que estava editando.

O que acontecia então tem duas metades, e a segunda é pior que a primeira:

- **o arquivo do jogo era regravado.** `sackboy_nativo.json` recebia um save que
  ela não pediu;
- **a cor dela não ia para lugar nenhum.** `_edita_o_perfil_do_rascunho`
  (`app/actions/profiles_actions.py:2113`) compara com `_active_profile_name`,
  que ainda era `vitoria` — então a base do save veio do **DISCO**, não do
  rascunho. O verde dela **evaporou**.

Medido na bancada, com a pergunta escrita em português: *"o VERDE dela foi
parar em algum arquivo? **NÃO** — evaporou"*.

**Grau: MEDIDO.**

### Caminho 2 — o "nome aleatório": o primeiro da lista

`_populate_profiles_store` (`app/actions/profiles_actions.py:1801`) tinha este
fallback:

```python
target = select_iter if select_iter is not None else first_iter
```

Sem `select_name`, ele selecionava o **primeiro perfil em ordem de carga do
loader**. E `_reload_profiles_store()` é chamado **sem alvo** por três caminhos:
`on_profile_reload` (o botão "Recarregar lista"), `on_profile_remove` e o
`install_profiles_tab`.

No disco dela o primeiro arquivo em ordem de carga é `acao.json` — **"Ação"**.

**É este o "nome aleatório" da queixa.** Não era aleatório: era o primeiro
arquivo do diretório, que para ela não tinha relação nenhuma com o que estava
fazendo. Um clique em "Recarregar lista" bastava.

**Grau: MEDIDO.**

E há uma segunda entrada pela mesma porta, que só apareceu ao instrumentar:
**`store.clear()` apaga as linhas uma a uma**, e o `GtkTreeView` emite `changed`
**no meio disso**, com a seleção ainda resolvendo para uma linha viva. O editor
era repintado **antes** de a função chegar a selecionar coisa alguma. Marcar só
o `select_iter` do fim curava o caminho errado e deixava o mesmo defeito entrar
pela porta do `clear`.

**Grau: MEDIDO em 06/08** — é a razão de a repintura INTEIRA correr marcada.

### Caminho 3 — o pré-preenchimento do rodapé

O diálogo do botão **"Salvar Perfil"** (rodapé) nascia pré-preenchido com
`_active_profile_name` — uma **segunda variável**, escrita pela janela com a
resposta do **daemon**, que descreve o perfil **tocando no controle**, não o que
as abas estão mostrando.

As duas divergem. Com o jogo abrindo, a reconciliação do tique de 2 Hz
(`app/app.py:827`) movia `_active_profile_name` sozinha, e o diálogo nascia
perguntando *"substituir 'sackboy_nativo'?"* — um nome que ela nunca digitou nem
escolheu.

Pior, e é o que fecha a queixa: **os dois botões de salvar da mesma janela, no
mesmo instante, miravam arquivos diferentes.** O "Salvar este perfil" da aba
Perfis lia a linha; o "Salvar Perfil" do rodapé lia `_active_profile_name`.

**Grau: MEDIDO.**

## O agravante composto: por que não bastava acontecer uma vez

Este é o pedaço que transforma um susto em **perda permanente**, e ele só
aparece quando se lê os três caminhos junto com o funil de gravação.

Ela cai no caminho 3, lê *"substituir 'sackboy_nativo'?"*, e clica OK — porque
a janela acabou de lhe dizer que é esse o perfil. O rodapé grava por
`_persist_profile_async` (`app/actions/footer_actions.py:464`) com
`adotar_como_ativo=True`, e o funil chama `_reapontar_rascunho`
(`app/actions/profile_writer.py:165`), que faz **três coisas**:

```python
self.draft = draft.with_profile_identity(profile)
self._active_profile_name = profile.name      # <- passa a ser o nome ERRADO
self._draft_baseline = self.draft             # <- e o baseline é ZERADO
```

As consequências se somam:

1. **`_active_profile_name` passa a ser o perfil errado.** É a variável que
   `_edita_o_perfil_do_rascunho` consulta para decidir se a base do save é o
   rascunho ou o disco. **Todos os saves seguintes** — dos DOIS botões — vão
   para lá;
2. **`_draft_baseline` é zerado**, então `_tem_edicao_pendente()`
   (`app/app.py:822`) passa a responder `False`. E é essa resposta que segura o
   tique de 2 Hz (`app/app.py:863`) **e** a guarda desta sprint. Com ela em
   `False`, a lista volta a se mover sozinha e o editor volta a ser repintado;
3. **não há mensagem de erro em lugar nenhum.** O arquivo foi gravado com
   sucesso — só que o errado.

**O defeito, depois do primeiro save, se auto-sustenta.** Não é um episódio: é
um estado em que a janela entra e do qual não sai sozinha.

**Grau: MEDIDO no código (os três efeitos são leitura direta de
`_reapontar_rascunho`); SUSPEITA COM MECANISMO na sequência completa vivida por
ela** — a bancada mediu os caminhos separadamente, não a cascata inteira numa
sessão só.

## A cura, em três camadas — e por que as três eram necessárias JUNTAS

O princípio que a cura escreve, e que dá nome à sprint: **a janela nunca troca o
alvo do Salvar sem gesto dela.** Seleção programática atualiza a LISTA e para
por aí.

### Camada 1 — a lista não se move sozinha

`_select_profile_by_name` (`app/actions/profiles_actions.py:825`) passa a
consultar `_selecao_pode_se_mover_sozinha` e **recusa** quando há trabalho não
salvo, registrando `perfis_selecao_automatica_recusada` no journal.

Recusar é o **menor espanto possível**, e a informação não se perde: quem diz
*"este é o perfil ativo agora"* é o **negrito** de `_mark_active_profile_row`,
que roda logo antes e **não depende da seleção**. Mover a barra azul arrastaria
junto o editor, o "Ativar", o "Duplicar" e o "Remover" — os quatro leem a linha
selecionada.

### Camada 2 — o editor não é repintado por seleção que não é dela

`_mover_selecao_sem_gesto` (`app/actions/profiles_actions.py:871`) levanta a
marca `_selecao_programatica` num `try/finally`, e
`on_profile_selection_changed` (`app/actions/profiles_actions.py:1193`) para
antes do `_populate_editor` quando a marca está de pé **e** há trabalho a
proteger. Mesmo padrão, e mesma razão, do `_suppress_advanced_toggle` que já
existia.

E `_populate_profiles_store` passa a **preservar a linha anterior**: o primeiro
da lista vira fallback só quando não havia nada selecionado (o boot) ou quando o
que estava selecionado sumiu do disco (a remoção).

### Camada 3 — o Salvar mira o alvo MEMORIZADO

`_alvo_do_salvar` é escrito **só** por `_populate_editor` (que agora só roda por
gesto dela ou com o editor limpo) e pelo próprio Salvar.
`_alvo_do_salvar_do_editor` (`app/actions/profiles_actions.py:966`) passa a ser
a resposta para *"que perfil eu estou editando?"*, no `on_profile_save` e no
`_edita_o_perfil_do_rascunho`.

E o rodapé ganha `_perfil_que_as_abas_editam`
(`app/actions/footer_actions.py:331`), que pergunta ao **rascunho**
(`draft.source_name`) em vez de a `_active_profile_name`. Uma fonte só, e ela
**viaja junto do dado** que vai para o disco em vez de ao lado dele.

### Por que as três, e não só a primeira

Esta é a parte que custou a bancada, e vale escrever: **suprimir só o sinal
`changed` teria produzido um defeito novo.**

A barra azul ficaria numa linha e o editor em outra. E `on_profile_save` lê **as
duas**: a linha responde *"quem estou editando?"* e o campo Nome responde *"com
que nome vou gravar?"*. Divergentes, elas viram um **RENAME** aos olhos da
guarda R-10 — a janela perguntaria *"renomear 'sackboy' para 'vitoria'?"* por
causa de um sinal que ninguém emitiu, e se ofereceria para apagar um perfil que
ela não tocou.

Por isso as três camadas se sustentam mutuamente: a lista não se move, o editor
não repinta, e o Salvar tem uma fonte de verdade própria que sobrevive às duas.

### E a janela passou a dizer quando ela mesma troca o alvo

`app/app.py:878`: a reconciliação do tique de 2 Hz é **legítima** — no instante
do tique não havia nada a perder. Mas ela move o alvo dos dois botões de salvar
sem que ela tenha encostado em nada, **e em silêncio**.

**O silêncio era a metade não medida do defeito.** Recarregar em silêncio é
seguro para os DADOS e enganoso para ELA: era isso que fazia o diálogo do rodapé
parecer que tinha inventado um nome. A janela passa a anunciar, com o
vocabulário do outro ramo, para onde o Salvar aponta agora.

## M2 — o portão da cura falhava ABERTO

Achado por **revisão adversarial em 06/08**, depois da cura aplicada, e curado
nesta mesma sprint.

`_ha_trabalho_no_editor` consulta `_tem_edicao_pendente` dentro de um
`try/except`, e o `except` respondia `return False`:

```python
except Exception:
    return False        # "nao sei" virava "nao ha trabalho a proteger"
```

**Para uma guarda cujo único trabalho é proteger trabalho não salvo, o default
tem de FECHAR.** Foi medido: forçando `_tem_edicao_pendente` a estourar, **o
defeito inteiro volta** — o editor pula para o perfil do jogo, o Salvar grava
lá, e a cor dela some sem diálogo nenhum. O journal do teste mostra
`sackboy_nativo.json` sendo regravado, com backup no histórico.

A assimetria decide sozinha: um falso *"sim"* custa uma seleção que não
acompanha o perfil ativo até ela clicar; um falso *"não"* custa **o trabalho
dela**.

O `except` passa a responder `True` e a registrar
`perfis_edicao_pendente_indeterminada` no journal — porque uma guarda que fecha
no escuro sem dizer nada vira um cadeado misterioso.

**Grau do alcance: LATENTE.** Não há gatilho conhecido em produção — a resposta
sai de comparar dois pydantic (`self.draft != baseline`), e nenhum caminho atual
faz isso estourar. É exatamente por ser barato que o default certo não tem
desculpa.

## O defeito vizinho I-1 — o importar comparava nome cru

Medido junto, no mesmo dia, e é **destruição de perfil sem uma palavra na tela**.

`on_import_profile` (`app/actions/footer_actions.py:533`) decidia se havia
conflito assim:

```python
if nome in existentes:
```

Comparação por **nome de exibição** — enquanto os **DOIS** botões de salvar já
perguntavam por **SLUG** (é a lição da R-10: `save_profile` grava
`<slugify(nome)>.json`, então o slug é a identidade em disco). O importar era o
último que ainda comparava outra coisa.

Consequência medida: importar um `Navegacao.json` **destruía a "Navegação" dela
em silêncio** — os dois nomes ocupam o mesmo `navegacao.json`, e o diálogo de
conflito nunca abria. Vale igual para `"AÇÃO"` contra `"Ação"` e `"fps"` contra
`"FPS"`.

A cura tem duas metades, e a segunda só apareceu ao escrever o teste:

1. quem responde *"quem eu apago?"* passa a ser `find_by_slug`, e o diálogo cita
   o perfil **realmente afetado** (`alvo.name`), não o nome que veio no arquivo;
2. **o nome NOVO do "renomear" responde à mesma pergunta.** Sem isso, renomear
   `"Navegacao"` para `"AÇÃO"` cairia em cima de `acao.json` **pela porta dos
   fundos** — e a importação para com uma frase que explica por quê, em vez de
   gravar calada.

**Grau: MEDIDO.**

## A tabela cura → teste, com a MORDIDA

`tests/unit/test_nunca_troca_o_alvo_01_o_salvar_que_mirava_outro_perfil.py` —
**18 casos**, com `Gtk.TreeView` e `Gtk.ListStore` **de verdade** (o defeito É o
sinal `changed` da seleção; um dublê de lista não o emite e mediria o dublê).

**Mordida verificada em 06/08**, camada por camada: cada cura foi **arrancada**
da árvore, a suíte rodada, e devolvida.

| camada da cura | onde | teste que reprova sem ela | reprovam |
|---|---|---|---|
| a lista não se move sozinha | `_select_profile_by_name` / `_selecao_pode_se_mover_sozinha` | `test_o_campo_nome_nao_troca_sozinho` | **2** |
| o editor não repinta em seleção do código | `on_profile_selection_changed` + `_mover_selecao_sem_gesto` | `test_uma_edicao_pendente_sobrevive_a_recarga_da_lista` | **2** |
| a repintura preserva a linha | `_populate_profiles_store` | `test_o_botao_recarregar_lista_nao_troca_o_perfil_do_editor` | **2** |
| o Salvar mira o alvo memorizado | `_alvo_do_salvar_do_editor` | `test_o_salvar_nao_segue_a_linha_quando_o_arquivo_dela_some` | **1** |
| o rodapé pergunta ao rascunho | `_perfil_que_as_abas_editam` | `test_o_prefill_vem_do_rascunho_e_nao_do_perfil_ativo` | **1** |
| **M2: o portão FECHA no escuro** | `_ha_trabalho_no_editor` | `TestNaoSeiEHaTrabalhoAProteger` (classe inteira) | **3** |
| I-1: o importar pergunta pelo slug | `on_import_profile` | `TestOImportarPerguntaPeloSlug` (4 casos) | — |

**A cura não pode virar cadeado**, e há um teste para isso:
`test_sem_edicao_pendente_a_selecao_acompanha_o_perfil_ativo`. Sem trabalho a
perder, a aba continua abrindo no perfil ATIVO — que é a
`FEAT-GUI-LOAD-LAST-PROFILE-01` inteira. **Se ele reprovar, a guarda parou de
perguntar e passou a recusar sempre.**

**Honestidade sobre o teste do negrito:**
`test_a_lista_continua_dizendo_qual_perfil_esta_ativo` não morde o defeito
original — ele protege a borda que a *cura* introduziu (a recusa não podia
virar cegueira sobre qual perfil está ativo). Está registrado como tal na
própria docstring.

## A armadilha da bancada — e a regra que ela deixa

A primeira bancada de reprodução (scratchpad, fora do repositório) imprimia
`>>> REPRODUZIDO` **contra a árvore JÁ CURADA**.

A causa: a `Janela` da bancada compõe `ProfilesActionsMixin` e
`FooterActionsMixin`, mas **`_tem_edicao_pendente` não mora em nenhum dos dois**
— mora em `HefestoApp` (`app/app.py:822`). Sem declará-lo, o
`getattr(self, "_tem_edicao_pendente", None)` devolve `None`, o
`if callable(checar)` é falso, e a guarda inteira responde *"não há trabalho a
proteger"* **para sempre**. A bancada não estava medindo o produto: estava
medindo a própria montagem incompleta.

**Regra que fica:** toda bancada que compõe mixins precisa **declarar de onde
vêm os atributos que o `HefestoApp` fornece**. O `getattr` defensivo do produto
— que existe por bons motivos, para dublês e caminhos degradados — **silencia a
medição em vez de a denunciar**. É a mesma família da armadilha nº 1 da casa:
*medir contra a biblioteca errada produz alarme convincente e falso*.

**Grau: MEDIDO em 06/08**, e corrigido na bancada.

## O que fica ABERTO

### M3 — a doutrina divergiu de si mesma (o mais urgente daqui)

Duas funções respondem **a MESMA pergunta** — *"que perfil as abas estão
editando?"* — e depois desta sprint elas respondem com **fontes diferentes**:

| onde | fonte | desde |
|---|---|---|
| `_perfil_que_as_abas_editam` (`app/actions/footer_actions.py:331`) | `draft.source_name` | esta sprint |
| `_edita_o_perfil_do_rascunho` (`app/actions/profiles_actions.py:2113`) | `_active_profile_name` | ABAS-03 (25/07) |

E o pior não é a divergência: é que **a docstring de `_edita_o_perfil_do_rascunho`
ainda afirma a doutrina antiga como regra** —

> *"Quem responde 'qual perfil o rascunho é' é `_active_profile_name`, não o
> campo Nome."*

— enquanto a docstring da função nova argumenta, com medição, que
`_active_profile_name` é **a fonte errada** para essa pergunta, por ser a
resposta do **daemon** e não o que as abas mostram.

**Grau: SUSPEITA COM MECANISMO.** A revisão adversarial **não conseguiu
construir cenário de perda** com as duas fontes divergindo — o
`_reapontar_rascunho` mantém as duas em passo na maioria dos caminhos, e o
`mesmo_slug` absorve as diferenças de acentuação. Não há defeito demonstrado.

**Fica registrado como inconsistência de DOUTRINA a resolver antes que as duas
divirjam de verdade.** O trabalho não é escolher a fonte no escuro: é decidir
qual das duas é canônica, escrever isso num lugar só, e fazer a outra chamá-la —
e **não se apaga decisão medida**, então a docstring da ABAS-03 ganha nota
datada em vez de sumir.

### O segundo `except` que ainda falha ABERTO

`_refazer_as_abas_apos_ativar` (`app/actions/profiles_actions.py:1444`, da
ATIVAR-NÃO-MENTE-01) faz a mesma pergunta com
`contextlib.suppress(Exception)` e um default de `pendente = False`. Se
`_tem_edicao_pendente` estourar ali, as abas são **recarregadas em silêncio** e
o que ela não salvou some — **sem o diálogo** que aquela sprint criou justamente
para dar a decisão a ela.

**Grau: SUSPEITA COM MECANISMO** (leitura de código; nenhum efeito observado, e
o mesmo alcance latente do M2). **Não foi tocado nesta sprint**, por ser cura de
outra e por a regra da casa ser não entregar mudança que ela não pediu. Deve ser
avaliado junto com o M2 quando aquela sprint for retomada.

### O resto

- **a primeira frase da queixa continua em aberto.** *"Nada indica que eu tô
  alterando o perfil pra jogar na hora"* é um pedido de **informação na tela**,
  não de comportamento. Esta sprint entrega **uma** frase (o anúncio da
  reconciliação); a aba continua sem dizer, de forma permanente e visível, qual
  perfil o editor está editando e para onde cada um dos dois botões de salvar
  grava;
- **os dois botões de salvar continuam sendo dois.** Eles agora concordam sobre
  o alvo, mas ter "Salvar este perfil" e "Salvar Perfil" na mesma janela é
  ambiguidade de desenho que nenhuma das duas curas resolve;
- **o aceite em uso real.** A bancada e os 18 testes provam o mecanismo. Que o
  nome pare de trocar sozinho **no uso dela**, com o jogo abrindo de verdade, só
  o uso dela fecha — e vale a **PROVA-DE-TELA-01**: foto antes e depois, e a
  palavra final é dela.
