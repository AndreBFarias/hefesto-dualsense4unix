# REGRA-NÃO-SE-PERDE-01 — o rodapé gravava por fora do funil

- **Achado em:** 06/08/2026, por **auditoria de materialização** — varredura dos
  códigos de sprint que existem na árvore e **não têm página** em `docs/`.
  Nenhum destes quatro veio de queixa dela nesta data; o defeito que três deles
  curam, sim, e é o de sempre: *"a config que eu deixo nunca é respeitada"*.
  Dois já haviam sido nomeados como página faltante em 05/08, na E3 da
  [FIAÇÃO-QUE-FALTA-01](2026-08-05-FIACAO-QUE-FALTA-01-o-verificador-que-ela-nao-tem-como-ver.md)
- **Estado:** **CURA APLICADA e commitada** nos quatro. Esta sprint é
  **materialização atrasada**: o código está na árvore, os testes mordem, e
  **só o documento faltava**. Os commits são `c3829c7` (05/08, a leva dos sete
  mecanismos — `REGRA-NÃO-SE-PERDE-01/02` e `UNIFICA-CONSTANTE-01`), `10f4818`
  (05/08, o irmão `UNIFICA-PREDICADO-01`) e `9946a8b` (**28/06**,
  `PERF-FOOTER-ASYNC-IO-01` — ver a correção de registro abaixo)
- **Gravidade:** **ALTA** na `REGRA-NÃO-SE-PERDE-02` (o perfil que ela acabava
  de salvar **com o jogo em foco** nunca ativava dentro do jogo); **MÉDIA** no
  `PERF-FOOTER-ASYNC-IO-01` (fluidez) com **agravante ALTO** de portão ausente;
  **BAIXA hoje** no `UNIFICA-CONSTANTE-01`, **MÉDIA** no que ele desarma. E
  **ALTA no fato de faltar a página**: quatro decisões vivendo só em docstring
  são quatro decisões que a próxima pessoa reabre por não saber que existem
- **Causa-raiz:** **MEDIDA** na `REGRA-NÃO-SE-PERDE-02` (o veto R-21 e a chave
  de seleção reproduzidos em teste) e no `UNIFICA-CONSTANTE-01` (por `git grep`,
  reconferido hoje). **SUSPEITA COM MECANISMO** no `PERF-FOOTER-ASYNC-IO-01`:
  o caminho bloqueante foi lido e fecha, mas **ninguém cronometrou** o
  congelamento da janela
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md)
    — esta sprint é a **continuação** dela, e a `REGRA-NÃO-SE-PERDE-01` **já
    está documentada lá**, como seção nomeada. Aqui não se repete: ver a
    primeira seção;
  - [FIAÇÃO-QUE-FALTA-01](2026-08-05-FIACAO-QUE-FALTA-01-o-verificador-que-ela-nao-tem-como-ver.md)
    — é ela quem **pede** esta página, na E3, e quem deixou escrito o que a
    página precisava registrar e o índice não registrava;
  - [a leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)
    — o índice que traz o **desenho** da `REGRA-NÃO-SE-PERDE-02` antes de ela
    virar código. Esta sprint é a transcrição **conferida contra a árvore**, e
    não contra o desenho;
  - [PERFIL-NASCE-CERTO-01](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md)
    — de onde vem o número da prioridade, que aqui é o **irmão simétrico** da
    regra;
  - [PERFIL-SALVA-TUDO-01](2026-07-29-PERFIL-SALVA-TUDO-01-salvei-todas-as-abas-e-so-parte-ficou.md)
    — os vetos que a `REGRA-NÃO-SE-PERDE-02` tinha de respeitar, e respeitou
    sem afrouxar nada;
  - [NUNCA-TROCA-O-ALVO-01](2026-08-06-NUNCA-TROCA-O-ALVO-01-a-janela-trocava-o-nome-e-o-salvar-ia-para-o-arquivo-errado.md)
    — mesmo botão, defeito vizinho e **distinto**: lá o "Salvar" mirava o
    arquivo errado; aqui ele mira o certo e grava a regra errada;
  - [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
    — a classe de que o `PERF-FOOTER-ASYNC-IO-01` é o caso invertido: não é
    código sem chamador, é **cura sem portão**.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O que esta página cobre — e o que ela NÃO repete

O título é o nome da **família**, e a família tem quatro códigos com uma frase
só por trás: **a gravação de perfil da janela tem de passar por UM funil, e o
funil tem de decidir a regra e o número com a mesma disciplina.**

A `REGRA-NÃO-SE-PERDE-01` **já tem página**. Ela é seção nomeada da
[GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md),
com a decisão dela de 05/08, a consequência medida no `sackboy_nativo` e a linha
de cura citada. **Não se duplica aqui.** O que fica desta página sobre o 01 é
só o que aconteceu **depois** dela:

1. o 01 deixou de ser uma linha condicional e virou o **degrau 1 de uma escada
   de três**, em `_regra_do_save`;
2. a testemunha independente que faltava ao 01 **existe hoje** —
   `test_o_disco_vence_a_fotografia_quando_os_dois_tem_regra` mede exatamente o
   caso em que a cura do 02 poderia atropelar a do 01;
3. a linha da tabela da `GRAVA-POR-UM-FUNIL-01` que dizia *"mordida DECLARADA
   na docstring; sem registro de execução independente"* **caducou** — ver a
   nota datada no fim desta página.

As outras três **nunca tiveram página nenhuma**, e são o corpo do documento.

| código | uma frase | onde vive |
|---|---|---|
| `REGRA-NÃO-SE-PERDE-01` | quem **já existe** em disco herda o próprio `match` | `footer_actions.py`, degrau 1 de `_regra_do_save` |
| `REGRA-NÃO-SE-PERDE-02` | o nome **NOVO** nascia sem regra nenhuma | `footer_actions.py`, degraus 2 e 3 |
| `PERF-FOOTER-ASYNC-IO-01` | o I/O de disco dos três botões saiu da thread do GTK | `footer_actions.py` + `profile_writer.py` |
| `UNIFICA-CONSTANTE-01` | o teto `200` morava em três lugares, com fio entre dois | `profiles/schema.py` |

---

## REGRA-NÃO-SE-PERDE-02 — o nome NOVO nascia sem regra nenhuma

**Decisão dela, 05/08/2026. Gravidade: ALTA. Grau da causa: MEDIDO.**

### O gesto, e o que ele produzia

Ela está **dentro do jogo**. Ajusta a cor, os gatilhos, a vibração. Clica
"Salvar Perfil" e digita um nome que ainda não existe — "MadJack".

O perfil ia para o disco com `{"type": "any"}`, e a razão estava escrita desde
23/07, em `draft_config.py`: *"o diálogo do rodapé não tem campo de regra, então
o perfil nasce valendo sempre e a regra específica se define na aba Perfis"*.
Era conservador de propósito, e a alternativa que ele recusava era pior —
herdar o regex do jogo **anterior** faria o perfil novo casar com o jogo errado
(medido em 25/07: "Salvar como MadJack" com o FPS ativo produzia um perfil com o
regex do FPS e prioridade 60).

### Por que a frase caducou: `MatchAny` não é neutro

**Grau: MEDIDO**, e é o coração desta sprint. Catch-all nesta base tem **duas
propriedades opostas ao mesmo tempo**:

- **invisível onde deveria valer.** A chave de seleção do daemon é
  `(não é catch-all, prioridade)` — **especificidade antes de prioridade** — e
  o veto R-21 recusa candidato catch-all numa janela `steam_app_*`, devolvendo
  `MOTIVO_JOGO_SEM_PERFIL_PROPRIO`. O perfil que ela acabou de salvar era o
  **único no disco** e ainda assim **não valia dentro do jogo**;
- **soberano onde não deveria.** Ao mesmo tempo ele nasce com
  `max(catch-all) + folga` de prioridade e ganha o **desktop inteiro**,
  carregando junto o `suppress_desktop_emulation`, que suspende mouse e teclado.

É exatamente a forma do `sackboy_nativo` dela em 05/08 — **invisível onde
deveria valer, soberano onde não deveria** — só que agora **fabricada de
fábrica**, por um gesto novo, em vez de herdada de um arquivo corrompido.

Duas consequências que essa medição derruba de uma vez:

- *"nasce sempre e a regra se define depois"* **não era conservador**. Nascer
  "sempre" é nascer **no lugar errado**;
- e é por isso que **subir a prioridade não resolvia nada**: prioridade é o
  **segundo** termo da chave. Enquanto o `match` for catch-all, o primeiro termo
  já perdeu.

### A cura: uma escada de três degraus, no rodapé

`footer_actions._regra_do_save`. A regra tem de **vir de algum lugar**, porque o
diálogo não a pergunta — então cada degrau é uma fonte, da mais autoritária para
a menos:

| degrau | pergunta | resposta |
|---|---|---|
| **1** | o perfil **já existe em disco**? | herda `existente.match` — a `REGRA-NÃO-SE-PERDE-01` |
| **2** | há perfil de **origem**, e ele **não** é catch-all? | herda `draft.source_match` |
| **3** | nenhum dos dois | **`MatchManual()`** |

```python
if existente is not None:
    return existente.match
origem = getattr(draft, "source_match", None)
if origem is not None:
    candidato = Profile(name="sonda", match=origem)
    if candidato.e_catch_all is False:
        return candidato.match
return MatchManual()
```

**Três decisões de desenho, e nenhuma é estética.**

**A herança mora no RODAPÉ, não no `to_profile`.** **Grau: MEDIDO**, reconferido
na árvore de hoje: `DraftConfig.to_profile` tem **exatamente dois chamadores em
produção** — `footer_actions.py:514` e `profiles_actions.py:2320`. Mexer no gate
`mesmo_perfil` de lá atingiria os dois caminhos e as testemunhas de ambos, e uma
delas é justamente a guarda que impede o perfil novo de nascer com o regex de
**outro** jogo. A herança entra **onde a prioridade já tinha entrado**: no
`_construir` do rodapé, ao lado do `_prioridade_do_save`. Um arquivo só, e o
veto nº 2 da `PERFIL-SALVA-TUDO-01` (R-11) continua fechado — **nada foi
afrouxado em `draft_config.py`**.

**O órfão nasce `MatchManual()`, e não `MatchAny()`.** `MatchManual` é o sentinel
de *"só entra quando eu mandar"*: `matches()` é sempre `False` (nunca vira
candidato), `e_catch_all` é `False` para ele (não dispara o veto R-21 nem a
reversão de modo), a `sanidade.py` o isenta, e ele é a **tradução literal** do
que o diálogo do rodapé significa — *"guarde o que eu tenho agora; quando usar,
eu digo"*. Ele nasce **sem opinião e sem estrago**, que é o que o `MatchAny`
prometia e não entregava.

**O degrau 2 pergunta `e_catch_all`, não tipo.** Este é o ponto fino, e ele tem
um caso real por trás. Os três `Match` são classes **irmãs** e nenhuma herda da
outra; e um `MatchCriteria` com os três campos vazios é catch-all na prática —
foi assim que o preset `coop_local` de fábrica saiu inalcançável e ninguém
percebeu. Um predicado por `isinstance(..., MatchAny)` deixaria esse segundo
caso passar, e o perfil novo nasceria com um critério que **nunca casa**: o
acidente do `coop_local`, agora fabricado pelo rodapé. **Herdar "vale sempre"
não é herdar regra.**

### O que o degrau 3 custa, e está escrito

**RESSALVA de downgrade, a mesma que o `MatchManual` carrega no esquema:** um
perfil gravado com `{"type": "manual"}` é **rejeitado por binário antigo**, que
não conhece o discriminador. O tipo é aditivo — perfis já gravados com
`any`/`criteria` validam sem migração — mas o caminho de volta cobra.

### As mordidas

**Grau: MEDIDO**, com a ressalva de proveniência escrita junto. As mutações
estão declaradas uma a uma no topo de
`tests/unit/test_regra_nao_se_perde_02_o_nome_novo_nascia_sem_regra.py`, e a
execução delas está **registrada em documento**, não nesta sprint: a E3a da
`FIAÇÃO-QUE-FALTA-01` conta *"nove testes, com seis mutações verificadas"*.
Conferido hoje: são nove testes, e a suíte deles passa (78 verdes junto dos
arquivos irmãos do rodapé).

| mutação | o que fica vermelho |
|---|---|
| degrau 2 fora | `test_nome_novo_herda_a_regra_do_perfil_de_origem`, `test_o_perfil_do_rodape_nunca_nasce_catch_all`, `test_o_perfil_que_ela_acabou_de_salvar_vale_dentro_do_jogo` |
| degrau 3 devolvido a `MatchAny()` | `test_sem_origem_nasce_so_manual`, `test_a_origem_catch_all_nao_e_regra_a_herdar`, `test_a_sanidade_nao_acusa_depois_de_tres_saves_pelo_rodape` e o portão estático |
| degrau 1 fora (a cura do 01) | `test_o_disco_vence_a_fotografia_quando_os_dois_tem_regra` |
| predicado trocado por `isinstance` | nada — e **é por isso** que o caso do `MatchCriteria` vazio está escrito dentro de `test_a_origem_catch_all_nao_e_regra_a_herdar` |

O teste que fecha a queixa inteira num gesto é
`test_o_perfil_que_ela_acabou_de_salvar_vale_dentro_do_jogo`: ela salva com o
jogo em foco, o daemon é consultado com a janela do **mesmo** jogo, e o motivo
tem de ser `selecionado` — não `jogo_sem_perfil_proprio`.

E há um segundo que vale por ser **de segunda ordem**:
`test_a_sanidade_nao_acusa_depois_de_tres_saves_pelo_rodape`. Três "Salvar
Perfil" e o verificador semântico continua calado. Antes, cada save somava um
catch-all e um degrau de prioridade, e a `sanidade.py` acusava
`catch_all_demais` — **o disco dela de 05/08, montado por três gestos.**

### O portão, e o canário que prova que ele morde

`test_o_rodape_nao_constroi_catch_all_por_conta_propria` reprova qualquer
`MatchAny(` **construído** dentro de `footer_actions.py`, lendo por **AST e não
por texto** — as docstrings desta cura citam `MatchAny()` dezenas de vezes ao
explicar por que ele saiu, e um portão textual acusaria justamente a explicação.

O portão é deliberadamente **estreito**: veta a construção **no rodapé**, não a
existência do tipo. Quem precisa de catch-all de verdade tem a aba Perfis e o
editor avançado, onde ela **vê** o que está escolhendo.

E ele tem uma coisa que a casa raramente escreve e devia escrever sempre:
**um canário próprio.** `test_o_portao_enxerga_a_construcao_que_ele_veta` monta
um fonte de mentira num `tmp_path`, com um `MatchAny()` real e um `MatchAny()`
dentro de docstring, e exige que o extrator ache **só** os dois de verdade. Sem
ele, `ofensoras == []` também passaria com o extrator quebrado — que é o modo de
falha mais comum de portão estático. **Grau: MEDIDO** (o canário roda e passa).

---

## PERF-FOOTER-ASYNC-IO-01 — o I/O de disco saiu da thread do GTK

**Gravidade: MÉDIA no efeito, ALTA no que ele arrasta. Grau da causa: SUSPEITA
COM MECANISMO.**

### Correção de registro, antes de tudo

Este código **não é de 05 nem de 06/08**. Ele nasceu em **28/06/2026**, no
commit `9946a8b`, dentro de uma leva de interface (*"rodapé cortado no COSMIC +
UI mais fluida"*). **Grau: MEDIDO** — `git log -S` sobre a sigla devolve
`9946a8b` como primeira aparição, e o `c3829c7` de 05/08 só a **cita** ao mover
a gravação para o funil. Fica registrado porque a auditoria que gerou esta
sprint o classificou como código de 05/08, e **caducou na primeira medição**.

### O que ele fez

Antes, os três handlers do rodapé faziam I/O de disco **na thread do GTK**, que
é a thread que desenha. O `on_save_profile` era assim:

```python
existentes = [p.name for p in load_all_profiles()]   # disco, na thread do GTK
...
path = save_profile(profile)                          # disco, na thread do GTK
```

Depois, cada um dos três passou a despachar o trabalho para um worker via
`ipc_bridge.run_in_thread`, com o resultado renderizado num callback re-postado
por `GLib.idle_add`:

| botão | o que foi para o worker |
|---|---|
| **Salvar Perfil** | listar os perfis do disco para checar conflito, e gravar |
| **Importar** | ler e validar o JSON, e listar os perfis do disco |
| **Restaurar Padrão** | ler o asset, gravar, e **reler o rascunho inteiro** |

Os diálogos ficaram onde tinham de ficar — o de nome, o de sobrescrita, o
`FileChooser` e a confirmação **rodam na thread do GTK**, porque é a única onde
podem rodar.

**Uma decisão que veio junto e vale por si:** a checagem de conflito passou a
ser feita **no disco**, dentro do worker, e **nunca no cache em memória**. Sair
da thread do GTK pagava o custo de ler o disco, e ler o disco é o que impede a
decisão *"este perfil já existe?"* de ser tomada com estado ranço.

### O que ele arrasta hoje — e é isto que faltava estar escrito

O `PERF-FOOTER-ASYNC-IO-01` deixou de ser um item de fluidez e virou **premissa
de todo o resto**:

- o funil da `GRAVA-POR-UM-FUNIL-01` é construído **em cima dele**: o
  `_gravar_perfil_async` só existe na forma que tem porque há um worker e um
  callback, e a docstring do módulo declara, por gancho, **em qual das duas
  threads cada passo roda**;
- **cinco arquivos de teste do rodapé abrem com a mesma fixture**, que substitui
  `run_in_thread` por uma versão síncrona. Não é preferência de estilo: **sem um
  laço do GTK rodando, os callbacks nunca executariam**, e a suíte mediria um
  gesto que termina no meio.

### O que ele NÃO tem: portão

**Grau: MEDIDO** (por leitura da suíte inteira, hoje). **Nenhum teste exige que
o rodapé continue assíncrono.** Os testes que citam a sigla apenas a
**neutralizam** para poder medir outra coisa. Ou seja: quem devolver
`load_all_profiles()` para dentro do handler, na thread do GTK, **não reprova
nada** — e a suíte fica ainda mais verde, porque a fixture deixa de ter o que
substituir.

É o espelho da [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md):
lá era código com zero chamadores; aqui é **cura com zero guardas**.

---

## UNIFICA-CONSTANTE-01 — o teto 200 em três lugares, com fio entre dois

**Decisão dela, 05/08/2026:** *"preciso que as constantes apontem pros arquivos
reais do import"*. **Grau da causa: MEDIDO** por `git grep`, reconferido hoje.

### O triângulo aberto

O número `200` — o teto da faixa de prioridade que a **janela** oferece — morava
em três lugares:

| lugar | o que era |
|---|---|
| `app/actions/profiles_actions.py` | `PRIORIDADE_MAXIMA = 200`, a "fonte" que os outros **citavam** |
| `profiles/sanidade.py` | `PRIORIDADE_MAXIMA = 200`, **cópia declarada de propósito** |
| `gui/main.glade` | o `upper` do `profile_priority_adj`, XML que não importa nada de ninguém |

E **só um par tinha portão** (o glade contra `profiles_actions`). O lado sem fio
era o pior dos três: o verificador semântico **acusa** prioridade fora da faixa
e manda a usuária *"reabrir na aba Perfis"* — então ele podia divergir da faixa
que a aba Perfis realmente oferece, e o achado passaria a **mentir**, com a cura
impressa junto, sem que nada reprovasse.

### A cura: a constante DESCEU, não subiu

A saída óbvia seria `sanidade.py` importar de `profiles_actions.py`. **Está
proibida, e a proibição continua certa** — a nota antiga em `sanidade.py` dizia,
com todas as letras: *"`profiles/` não pode depender de `app/` (a GUI importa o
loader, nunca o contrário), e o CLI carregaria GTK atrás dela"*.

O que caducou não foi a proibição: foi a **conclusão de que a cópia era a única
saída**. A constante desceu para `profiles/schema.py`, e o critério da eleição é
o **import**:

- `schema.py` depende só de stdlib e pydantic — `profiles/`, `app/` e o CLI leem
  a faixa **sem nenhum deles puxar GTK**;
- é de onde `draft_config.py` já lia o **default** de `priority`
  (`Profile.model_fields["priority"].default`). Quem manda na **faixa** e quem
  manda no **default** passam a morar juntos.

`profiles_actions.PRIORIDADE_MAXIMA` virou **reexport** em vez de sumir, porque
`pa.PRIORIDADE_MAXIMA` é o nome que as asserções da aba Perfis já usavam:
**unificar não pode virar churn** — o nome fica onde estava, só muda de dono. O
glade **continua sendo cópia**, porque XML não importa nada; quem o segura é o
portão.

### O portão do triângulo, e a ordem em que ele foi escrito

`tests/unit/test_teto_da_prioridade_tem_uma_fonte_so.py`. Duas camadas, e a
segunda é a que interessa:

- os três lugares dizem o mesmo número (**e o piso também**, pelo `lower` do
  mesmo adjustment);
- e **não existe cópia nenhuma**: `sanidade.PRIORIDADE_MAXIMA is
  schema.PRIORIDADE_MAXIMA` (identidade, não igualdade), e uma asserção por AST
  que reprova se `profiles_actions` voltar a escrever o literal `200` na mão.
  *"Os testes de cima seguiriam verdes com três cópias sincronizadas na mão;
  estes exigem que não haja cópia nenhuma."*

**Por que AST e não `import profiles_actions`:** o módulo faz
`gi.require_version("Gtk", "3.0")` no topo, e importá-lo mataria o portão no CI
headless. A casa tem duas saídas — a guarda `exigir_gi_real` (que **pula** o
módulo inteiro sem GTK) e a leitura por AST. Aqui **tem de ser** a AST: um
portão que confere se três números batem não pode ser um portão que **some
justamente onde não há GTK**, porque é lá que roda o CI.

**A mordida é a ORDEM, e ela está registrada no commit `c3829c7`:** *"o portão
do triângulo criado ANTES de mover o número"*. Um portão escrito depois da cura
prova que a cura está lá; escrito antes, ele **reprova o estado velho** — é a
diferença entre uma afirmação e uma medição. **Grau: MEDIDO** pelo registro do
commit; a execução em vermelho não foi reproduzida nesta sprint.

### O irmão de mesmo dia: UNIFICA-PREDICADO-01

**Correção de registro:** *"cinco jeitos de perguntar 'isto é um jogo?' viram um
só"* (commit `10f4818`) **não é** o `UNIFICA-CONSTANTE-01`. É o
`UNIFICA-PREDICADO-01`, e ele tem página própria a escrever — está pedido na E3b
da [FIAÇÃO-QUE-FALTA-01](2026-08-05-FIACAO-QUE-FALTA-01-o-verificador-que-ela-nao-tem-como-ver.md),
com o material levantado. **Esta sprint não o cobre**, e o registra aqui só para
que os dois não sejam confundidos de novo.

O que se pode dizer sem invadir a página dele, porque é o mesmo método desta:
a fonte única (`profiles/steam_app.py`) **desceu** para a camada que não importa
nada — exatamente como a constante desceu para `schema.py` — e pelo mesmo motivo
estrutural, que é impedir um ciclo de import que estava a **um commit** de
distância. **Duas unificações no mesmo dia, com o mesmo critério de eleição:
manda quem não depende de ninguém.**

---

## Cura, teste e mordida — a tabela honesta

| cura | onde | teste | mordida | grau |
|---|---|---|---|---|
| degrau 1: quem existe herda o `match` do disco | `footer_actions.py`, `_regra_do_save` | `test_salvar_por_cima_de_perfil_que_ja_existe_herda_a_regra`; `test_o_disco_vence_a_fotografia_quando_os_dois_tem_regra` | declarada nas duas docstrings | **MEDIDO** pelo registro da E3a; execução não reproduzida aqui |
| degrau 2: nome novo herda a regra da origem | idem | três testes (ver tabela de mutações) | declarada | **MEDIDO** pelo mesmo registro |
| degrau 3: órfão nasce `MatchManual()` | idem | quatro testes + portão | declarada | **MEDIDO** pelo mesmo registro |
| predicado estrutural (`e_catch_all`) | idem | `test_a_origem_catch_all_nao_e_regra_a_herdar` | **não morde** — é guarda, e está escrito | **declarado** |
| portão do `MatchAny` no rodapé | `test_regra_nao_se_perde_02_o_nome_novo_nascia_sem_regra.py` | `test_o_rodape_nao_constroi_catch_all_por_conta_propria` | **canário próprio**, sem tocar no produto | **MEDIDO** |
| fonte única do teto | `profiles/schema.py` | `test_teto_da_prioridade_tem_uma_fonte_so.py` | a ordem: portão antes do número | **MEDIDO** pelo commit |
| I/O do rodapé fora da thread do GTK | `footer_actions.py`, `profile_writer.py` | **nenhum** | **não existe** | **SEM PROVA** de que a cura sobreviva a quem a desfizer |

**O que NÃO morde, e está dito porque a casa exige:** o predicado estrutural é
guarda (passa nos dois estados; existe para que o `MatchCriteria` vazio não
volte pela porta dos fundos), e **portão estático verde não é prova de que a
gravação funciona** — ele mede a **forma** do código, e só.

---

## Notas datadas — o que caducou

**06/08/2026, na `GRAVA-POR-UM-FUNIL-01`.** A tabela *"Cura → teste"* daquela
sprint marca a linha do `match` herdado (`REGRA-NÃO-SE-PERDE-01`) como *"mordida
DECLARADA na docstring; sem registro de execução independente"*. **Isto
caducou**: a testemunha independente nasceu no mesmo dia, com a
`REGRA-NÃO-SE-PERDE-02` — `test_o_disco_vence_a_fotografia_quando_os_dois_tem_regra`
monta o único cenário em que os **dois** lados têm regra e cobra que o **disco**
vença. A afirmação anterior não é apagada: ganha esta nota.

**05/08/2026, em `draft_config.py`.** O parágrafo que decidia `MatchAny()` para
nome novo **caducou como contrato e sobrevive como default de conversão**. Quem
chama `to_profile` direto continua recebendo `MatchAny()`, e é isso que as
testemunhas daquele ramo ainda medem — a decisão **mudou de lugar**, para o
rodapé, e não mudou de valor onde não devia.

**05/08/2026, em `profiles/sanidade.py`.** A justificativa da cópia deliberada
*"`profiles/` não pode depender de `app/`"* **continua certa e continua
valendo**. O que caducou foi a conclusão de que a cópia era a única saída.

**05/08 a 06/08/2026, nos testes do funil.** Duas docstrings caducaram **sem o
código mudar** — as que diziam *"o perfil nasce `MatchAny` no primeiro save de
propósito"* e *"a decisão de que nome NOVO nasce `MatchAny()` continua de pé"*.
Nos dois casos o teste **segue medindo a mesma coisa** e só a premissa mudou;
nos dois a nota datada foi escrita dentro do próprio teste. E um teste foi
**reescrito no lugar**: `test_perfil_novo_pelo_rodape_continua_nascendo_sempre`,
testemunha da frase oposta, virou
`test_perfil_novo_pelo_rodape_herda_a_regra_da_origem`, com a data de validade
da premissa antiga (**23/07 a 05/08/2026**) escrita na docstring.

---

## O que fica ABERTO

**Do `PERF-FOOTER-ASYNC-IO-01`:**

- **a cura não tem portão.** Devolver o I/O de disco para a thread do GTK não
  reprova nada. **Grau: MEDIDO** (a ausência foi conferida em toda a suíte).
  Um portão por AST, no molde do que a `REGRA-NÃO-SE-PERDE-02` já usa, custa o
  mesmo que os que já existem;
- **os três botões que gravam NÃO congelam a interface.** `_freeze_ui` só é
  chamado pelo "Aplicar". Entre o clique em "Salvar Perfil" e o diálogo de
  sobrescrita — que hoje abre num callback, depois de uma volta pelo worker —
  a janela está **viva e clicável**, e nada impede um segundo clique.
  **Grau: SUSPEITA COM MECANISMO** — o caminho foi lido e fecha, o caso não foi
  construído;
- **o executor do `ipc_bridge` tem UM worker só.** Toda gravação de perfil
  entra na mesma fila das chamadas de IPC da janela. **Grau: SUSPEITA COM
  MECANISMO** para o efeito; **MEDIDO** para o fato (`max_workers=1`);
- **duas fontes no mesmo gesto.** No "Salvar Perfil", a pergunta *"este perfil
  já existe?"* é respondida **pelo disco** (dentro do worker), mas o número de
  um perfil **novo** sai de `_prioridade_acima_dos_catch_all`, que lê o
  **cache em memória** — e o faz de propósito, porque roda na thread do GTK. Se
  o cache estiver ranço (um perfil criado fora da janela), o perfil novo pode
  nascer **abaixo** de um catch-all que existe em disco e não está no cache.
  **Grau: SUSPEITA COM MECANISMO.**

**Do funil, herdado e não fechado:**

- **`_conferir_invariante_de_gravacao` não morde, e é feito de `assert`.**
  Nenhum teste viola a invariante para vê-lo disparar, e `assert` **some sob
  `python -O`**. A invariante central do módulo **não tem guarda executável em
  produção**, enquanto o texto promete que tem. **Grau: MEDIDO**, e a decisão
  (virar exceção de verdade, ou dizer na docstring que é rede de teste) está
  pedida desde a E4.2 da `FIAÇÃO-QUE-FALTA-01`;
- **`app/actions/profiles_actions.py` continua gravando fora do funil**, como
  exceção datada de 04/08. O que segura é o portão que impede a lista de
  autorizados de **crescer**. **Grau: MEDIDO.**

**Da `REGRA-NÃO-SE-PERDE-02`:**

- **a tela não diz qual regra o perfil recebeu.** A escada decide entre três
  fontes e **nenhuma aparece no diálogo**; o toast é o mesmo *"Perfil salvo
  em …"* nos três casos. A `DIV-2` do índice de 05/08 perguntava se o
  `MatchAny()` merecia aviso; a resposta mudou o valor gravado, **não** a
  informação na tela. **Grau: em aberto, decisão dela** — e é texto de
  interface, então a palavra final é dela
  ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md));
- **o degrau 3 grava um tipo que binário antigo recusa.** A ressalva de
  downgrade está escrita no esquema e **em nenhum lugar que ela veja**.
  **Grau: SEM PROVA** de que o caso tenha ocorrido; **MEDIDO** de que o esquema
  antigo recusa;
- **nada disto foi visto na tela dela.** Nenhuma afirmação desta sprint é sobre
  aparência, e todas as medições saíram de bancada com `HOME` temporário. Que o
  gesto dela, na máquina dela, produza o perfil certo, **só o olho dela fecha**.

**Do `UNIFICA-CONSTANTE-01`:**

- **a escala satura no teto.** Com qualquer catch-all em 190 ou acima, todo
  perfil novo nasce exatamente em **200** e empata; o desempate cai no
  incumbente ou na **ordem alfabética do nome do arquivo**. Unificar o número
  não mexe nisso — só garante que os três lugares saturem no mesmo ponto.
  **Grau: MEDIDO** (o cálculo é `min(PRIORIDADE_MAXIMA, base + folga)`);
- **três números ainda convivem** para o conceito *"nascer acima dos
  catch-all"*: **15** (`_PISO_ACIMA_DOS_CATCH_ALL`, o piso do caminho
  degradado), **`max(catch-all) + 10`** (o cálculo real) e os dois caminhos de
  "criar perfil". A `DIV-7` está aberta desde 25/07 e **esta sprint não a
  fecha** — ela unificou o **teto**, não a **folga**;
- **o glade continua sendo cópia**, por natureza do XML. O portão a segura, e é
  o único elo que não pode virar import. **Grau: MEDIDO.**

**Do registro:**

- **`UNIFICA-PREDICADO-01` continua sem página** (E3b da `FIAÇÃO-QUE-FALTA-01`).
  O material está levantado ali; **esta sprint não o escreve**;
- **a origem da prioridade `191` no disco dela segue indeterminada.** O
  instrumento que decide já existe — o `profile_salvo` carimbado com
  `origem=janela:<botão>`, da
  [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md)
  — e falta **o próximo gesto dela** para lê-lo. **Grau: SEM PROVA**, e é
  proposital que continue assim até haver linha de journal;
- **os arquivos de perfil dela não são tocados por nenhuma linha desta leva**,
  inclusive o `sackboy_nativo.json`, inclusive *"só para normalizar"*. O destino
  daquele arquivo é **decisão dela** — veto repetido em cinco documentos, e
  repetido aqui.
