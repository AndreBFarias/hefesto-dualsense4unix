# GRAVA-POR-UM-FUNIL-01 — o rodapé gravava e o rascunho não ficava sabendo

- **Achado em:** 04/08/2026, medindo o que o "Salvar Perfil" do rodapé escreve
  em disco. Ninguém procurava por isto: procurava-se por que os perfis dela
  tinham prioridade alta
- **Estado:** **CURA APLICADA**, com funil, três portões estáticos e testes de
  comportamento que mordem
- **Gravidade:** ALTA — cada gesto de **preservar** o trabalho dela empurrava o
  perfil um degrau para cima e apagava a regra de janela no caminho
- **Causa-raiz:** **PROVADA no código e MEDIDA em bancada** (bancada isolada e
  janela real sob Xvfb, HOME temporário). **Não** medida na máquina dela
- **Índice:** **nenhum.** A faixa de perfis está órfã de índice desde 30/07 — e
  a síntese de 05/08 aponta isso como a explicação estrutural de por que
  meias-entregas desta faixa passaram batido
  ([o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md),
  seção 5.7, item 5)
- **Parentes, e distintas:** `ABAS-01` (25/07) escreveu a cura e ligou em um
  lugar só; `PERFIL-NASCE-CERTO-01` deu o número da prioridade;
  `PERFIL-SALVA-TUDO-01` deu os vetos que esta sprint tinha de respeitar;
  [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
  nomeou o padrão do qual este defeito é mais um caso

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal ou teste que reprova; **SUSPEITA** = o caminho de código foi lido, o
efeito não foi provado; **SEM PROVA** = está escrito em algum lugar e ninguém
verificou. Cada seção declara o seu.

---

## O sintoma

Ela abre a janela, mexe na cor, no gatilho, no rumble, e clica **"Salvar
Perfil"**. Digita um nome. O toast responde *"Perfil salvo em …"*.

Ela mexe em mais alguma coisa e clica **"Salvar Perfil"** de novo, com o
**mesmo nome** — o gesto mais banal que existe.

O segundo save não guarda o trabalho dela por cima do primeiro: ele **reescreve
o perfil inteiro**, com a regra de janela virada em `"vale sempre"` e com uma
prioridade **nova, mais alta**. O terceiro sobe mais. Nada na tela diz que a
regra mudou — o toast é o mesmo *"Perfil salvo em …"* das duas vezes.

É a queixa crônica dela — *"a config que eu deixo nunca é respeitada"* —
entrando por uma porta nova, e por um gesto cujo propósito literal é **não
perder** o que ela fez.

## A evidência medida

**Grau: MEDIDO**, em duas bancadas independentes, ambas com HOME temporário.
Registrado em `docs/process/estudos/2026-08-05-…-dezessete-agentes-mediram.md`,
seção 1.1/D-01.

A catraca, em bancada isolada:

```
1º "Salvar Perfil" como "MadJack"  ->  priority = 10
2º "Salvar Perfil" como "MadJack"  ->  priority = 20
3º "Salvar Perfil" como "MadJack"  ->  priority = 30
```

E a mesma coisa numa **janela real sob Xvfb**, cinco cliques em "Salvar Perfil"
sem mudar mais nada entre eles:

```
prio = 11, 21, 31, 41, 51      match = any em TODOS os cinco
```

Os dois números da folga (10 e 11) são o mesmo cálculo com discos de partida
diferentes — `max(prioridade dos catch-all) + 10`. O que interessa é o
**degrau**: cada save soma uma folga inteira.

**O que NÃO está medido, e não pode ser afirmado:** que foi esta catraca que
produziu o `sackboy_nativo` com prioridade **191** e `match: any` no disco dela.
A síntese registra **três explicações incompatíveis** para aquele número
(DIV-1), e a única linha de journal que existe hoje —
`match_antes=criteria match_depois=any priority_antes=10 priority_depois=191` —
é compatível com **um único save que salta de 10 para 191**, o que não é a
catraca de +10 nem só o controle deslizante. **Grau: SEM PROVA.** A origem do
191 segue indeterminada, e esta sprint não a decide.

## A causa-raiz: a fotografia que envelhece

O `DraftConfig` guarda uma **fotografia** do perfil de onde o rascunho veio — os
campos `source_name`, `source_match`, `source_priority`, `source_mode`,
`source_suppress`. Quem decide o que vai para o disco é o `to_profile`
(`app/draft_config.py:463`), e ele decide **por essa fotografia**, num gate:

```python
# app/draft_config.py:562
mesmo_perfil = self.source_name is not None and (
    name == self.source_name or mesmo_slug(name, self.source_name)
)
```

Se `mesmo_perfil` é `True`, o perfil sai **reemitindo** a regra e a prioridade
da fotografia — que é o comportamento certo, e é o que a
`BUG-FOOTER-SAVE-DROPS-SECTIONS-01` protegeu. Se é `False`, o perfil sai com
`MatchAny()` e com a prioridade **calculada** pelo chamador.

O `_on_saved` do rodapé, antes desta sprint, atualizava `_active_profile_name` e
`_draft_baseline` e **nunca tocava `self.draft`**. Portanto:

| passo | o que acontece |
|---|---|
| ela salva como "MadJack" | grava certo — `mesmo_perfil` era `False`, e nome novo **deve** nascer `MatchAny` |
| a janela **não** reaponta o rascunho | `source_name` continua no perfil ANTERIOR |
| ela salva como "MadJack" de novo | `mesmo_perfil` responde **`False` outra vez** |
| o `to_profile` conclui "nome novo" | grava `MatchAny()` e **recalcula** a prioridade |

**A fotografia envelhece e nunca mais bate.** O gate responde `False` **para
sempre**, e cada save seguinte é, para o `to_profile`, um perfil nascendo do
zero — sobre um arquivo que já existia.

A cadeia, linha a linha (**MEDIDO**, conferida na árvore de hoje):
`footer_actions.on_save_profile` (`:285`) → `_prioridade_acima_dos_catch_all`
(`profiles_actions.py:1844`, `_FOLGA_ACIMA_DO_CATCH_ALL = 10` em `:83`,
`PRIORIDADE_MAXIMA = 200` em `:78`) → `save_profile(draft.to_profile(...))` →
`draft_config.py:562` `mesmo_perfil` **False** → prioridade calculada + `MatchAny()`.

## Por que disciplina não bastava — o argumento do funil

Esta é a parte que justifica o tamanho da cura, e ela é curta.

**A cura já existia, com nome e endereço, desde 25/07:**
`DraftConfig.with_profile_identity` (`app/draft_config.py:629`). E não é uma
coincidência feliz — **a docstring dele descreve o caminho do rodapé como um
dos dois defeitos que ele cura**, textualmente:

> *"rodapé 'Salvar Perfil' como 'MadJack' → `source_name` continuava apontando
> para o perfil anterior, então o SEGUNDO 'Salvar Perfil' com o mesmo 'MadJack'
> caía no ramo 'nome novo' de `to_profile` e zerava regra, prioridade e modo do
> perfil que ela acabara de criar."*

**E tinha UM único chamador em produção** (`profiles_actions.py:1943`, a aba
Perfis). **Grau: MEDIDO** — `git grep` fecha a conta.

O rodapé grava por **três botões diferentes** — Salvar, Importar, Restaurar
Padrão — e **nenhum dos três** chamava. A cura foi escrita para o rodapé e
ligada só na aba Perfis.

Daí o argumento, e ele é o núcleo desta sprint:

> **Lembrar de chamar não é engenharia.** Quem escrever o quarto botão que grava
> perfil vai esquecer de novo — e não por descuido: porque nada no caminho de
> quem escreve o quarto botão menciona que existe uma fotografia a reapontar.

A resposta não podia ser "adicionar a linha nos três lugares". Isso conserta
2026 e deixa 2027 aberto. A resposta é **tirar a possibilidade**: um caminho de
gravação só, que se lembra por todo mundo, e um portão que impede o quinto botão
de gravar por fora.

Nota de desenho, registrada porque ela é contraintuitiva: **um portão de "zero
chamadores" — o instrumento da `ENTREGA-QUE-NÃO-LIGOU-01` — não teria pego este
defeito.** `with_profile_identity` **tem** chamador; estava meio-ligado. O
aceite daquele portão precisa incluir este caso.

## Por que a suíte era verde

**Grau: MEDIDO.** Dois testes cobriam esta área e os dois ficavam verdes com o
produto quebrado:

- **`test_footer_salvar_nasce_acima_dos_catch_all.py`** afirma o vínculo
  **lendo o texto-fonte** (`assert "_prioridade_acima_dos_catch_all" in texto`).
  Ele prova que a chamada está escrita, não o que ela produz em disco;
- **`test_abas01_conflito_entre_abas.py`** só exercita o rodapé com o nome
  **igual** ao do perfil ativo — o único caso em que `mesmo_perfil` responde a
  verdade.

**Nenhum teste cobria dois saves consecutivos.** É a *"mordida na metade errada
da cadeia"*, o padrão que a `ENTREGA-QUE-NÃO-LIGOU-01` catalogou.

## A cura aplicada

### 1. O funil

`src/hefesto_dualsense4unix/app/actions/profile_writer.py` (novo, 232 linhas) —
**o único ponto por onde a janela grava perfil em disco**. A invariante está no
topo do módulo, escrita uma vez para valer em todo botão:

> Toda gravação de perfil feita pela janela termina com o rascunho apontando
> para o que ficou em **DISCO** — `draft.source_name == profile.name` e os
> demais `source_*` iguais aos do perfil gravado.

`ProfileWriterMixin._gravar_perfil_async` (`:69`) faz, nesta ordem e sem
exceção: construir → `save_profile` (no worker) → gancho pós-gravação do
chamador → toast e log → **reapontar o rascunho** → recarregar a lista →
`launch_env.refresh` → gancho de janela do chamador → **assert de invariante**.

A linha que faltava (`:191`):

```python
self.draft = draft.with_profile_identity(profile)
```

com `_active_profile_name` e `_draft_baseline` (R-08) acompanhando — o que
estava em memória virou disco, então a edição deixa de ser "pendente" e a
reconciliação com o perfil ativo volta a rodar pelo resto da sessão.

`_conferir_invariante_de_gravacao` (`:195`) é um assert barato que cobra a
invariante ao fim de cada gravação: **o lugar de descobrir que alguém trocou a
ordem dos passos é a suíte, não o disco dela.**

Herdar de um mixin, em vez de importar uma função solta, é o que dá ao funil o
`self.draft`, o `_active_profile_name` e os irmãos de mixin — exatamente os
estados que o defeito atravessava.

### 2. A prioridade só é calculada para quem NÃO existe

`footer_actions._prioridade_do_save` (`:334`):

```python
if existente is not None:
    return int(existente.priority)          # :367
```

O `alvo` que o `on_save_profile` já resolvia por slug (`find_by_slug`, `:319`)
passou a **viajar junto** até a gravação, porque ele é a resposta à pergunta
*"este perfil JÁ existe em disco?"*.

O `to_profile` protegia só o caso mais comum — salvar por cima do **mesmo**
perfil de onde o rascunho veio. Mas essa guarda depende da fotografia estar
fresca, e **é ela que envelhecia**; e não cobria salvar por cima de um perfil
**diferente do ativo**, onde o número calculado entrava por cima do dela do
mesmo jeito. **Perguntar ao DISCO fecha os dois, sem depender da fotografia.**

`PERFIL-NASCE-CERTO-01` continua valendo para o perfil **novo**: o número sai de
`_prioridade_acima_dos_catch_all` (`max(catch-all) + folga`, hoje 15 no disco
dela), porque o default do **esquema** é `0` e faria o perfil recém-salvo perder
para o `Pragmata`.

### 3. Os três botões passaram pelo mesmo caminho

| botão | `adotar_como_ativo` | por quê |
|---|---|---|
| **Salvar Perfil** (`:423`) | `True` | o gesto **é** trocar o que a janela edita: depois de salvar como "MadJack", o rascunho descreve o MadJack |
| **Importar** (`:531`) | `False` | importar um arquivo **não** é dizer "passei a editar este perfil" — roubar o rascunho aqui deixaria a janela mostrando uma configuração e o nome de outra |
| **Restaurar Padrão** (`:611`) | `True` | rascunho e nome trocam como **unidade** (R-08/C9) |

O **Importar** tem um detalhe que é o defeito inteiro visto de outro ângulo: se
o arquivo importado é o do perfil **ATIVO** (mesmo slug), o funil reaponta o
rascunho **mesmo** com `adotar_como_ativo=False`. O disco mudou debaixo dele, e
manter a fotografia velha faria o "Salvar Perfil" seguinte **desfazer o import
inteiro** — foi assim que o defeito I-2 foi medido (importar, salvar, e o
importado voltar ao que era).

O **Restaurar Padrão** ganhou um conserto de borda no mesmo movimento: quando a
releitura do perfil restaurado falha, o gancho devolve
`DraftConfig.from_profile(profile)` em vez de `None`. Devolver `None` — o que
este caminho fazia — deixava o rascunho com a **identidade** do `meu_perfil` e o
**conteúdo** antigo, e o "Salvar Perfil" seguinte desfazia a restauração em
silêncio.

## REGRA-NÃO-SE-PERDE-01 — a herança do `match` no salvar por cima

**Seção nomeada desta sprint, e não arquivo próprio:** a auditoria contou
**duas** citações da sigla na árvore (`footer_actions.py:388` e o teste que a
prova), e duas citações não sustentam um documento separado. Fica aqui, com data
e com o mesmo peso.

**Decisão dela, 05/08/2026.** Grau da causa: **MEDIDO** no disco dela; grau da
atribuição do gesto: **SEM PROVA** (ver DIV-1, acima).

### O que aconteceu

O `sackboy_nativo.json` dela tinha a regra `window_class: steam_app_1599660`. No
meio de uma sessão de jogo, virou `{"type": "any"}`.

E a consequência **não é estética**. A chave de seleção do daemon é
`(não é catch-all, prioridade)` — **especificidade antes de prioridade**. Logo,
com o `match` apagado:

```
janela steam_app_1599660  ->  coop_local (75, específico) VENCE sackboy_nativo (191, catch-all)
janela Alacritty / code   ->  sackboy_nativo (191) vence tudo  ->  no DESKTOP
```

**O perfil do Sackboy passou a perder DENTRO do Sackboy e a ganhar em todo o
resto do desktop** — carregando junto o `suppress_desktop_emulation`, que
suspende mouse e teclado. É o inverso exato do que ela pediu, e é *"está tudo
quebrado"* traduzido para código.

E é por isso que **subir a prioridade dele para 191 não resolveu nada**:
prioridade é o segundo termo da chave. Enquanto o `match` for `any`, o primeiro
termo já perdeu.

### O conflito que a decisão resolve

Havia **duas curas medidas desta casa** que, neste ponto, se contradiziam:

- `draft_config.py:562-584` decidiu — **e continua certo** — que **nome NOVO
  pelo rodapé nasce `MatchAny()`**. O diálogo do rodapé **não tem campo de
  regra**, e herdar a regra do perfil de origem fazia um perfil novo nascer com
  o regex de janela de **outro jogo**. Medido na época: "Salvar como MadJack"
  com o FPS ativo produzia um perfil com o regex do FPS e prioridade 60. O veto
  nº 2 da `PERFIL-SALVA-TUDO-01` proíbe, com todas as letras, afrouxar
  `mesmo_perfil` a ponto de reabrir isso (R-11);
- **mas o rodapé aplicava esse mesmo ramo a nome que JÁ EXISTE** — e aí ele não
  estava "nascendo" coisa nenhuma. Estava **apagando** a regra de um perfil que
  já tinha uma.

### A decisão

> **"Nasce sempre" vale para quem nasce.** Quem já existe tem regra, e **regra
> não se perde** por um gesto que a tela nem sabe nomear.

`footer_actions.py:420`, dentro do `_construir` que o funil recebe:

```python
if existente is not None:
    perfil = perfil.model_copy(update={"match": existente.match})
```

Três coisas que essa linha faz de propósito:

1. **a herança sai do DISCO, não da fotografia** — pelo mesmo motivo do
   `_prioridade_do_save`: a fotografia é justamente o que envelhecia;
2. **o gate `mesmo_perfil` não é tocado.** O R-11 continua fechado e o veto nº 2
   da `PERFIL-SALVA-TUDO-01` continua respeitado — nada foi afrouxado no
   `draft_config`;
3. **é simétrica à prioridade.** Quem já existe herda o próprio `match` do mesmo
   jeito que já herdava a própria prioridade. Uma regra, dois campos.

**NOTA DATADA (05/08/2026).** A síntese consolidada da madrugada
([o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md))
registra, na seção 5.1, um **resíduo declarado** desta sprint: *"o `match` ainda
não é herdado do disco"*, e a seção 5.7 o lista como defeito aberto. **Isto
caducou** — a `REGRA-NÃO-SE-PERDE-01` fechou o resíduo em 05/08, depois de a
síntese ser escrita. A decisão medida não foi apagada de lá: ganha esta nota. O
que **continua** aberto daquele item é a `DIV-2` — se o `MatchAny()` do rodapé
merece **também** um aviso no diálogo ("este perfil vai passar a valer sempre").
**Grau: em aberto, decisão dela.**

## Os três portões estáticos

`tests/unit/test_gravacao_de_perfil_passa_pelo_funil.py` guarda **duas** coisas:
os testes que mordem o comportamento (a seção seguinte) e os portões que impedem
a recaída. Os portões não medem comportamento — eles medem a **forma** do
código, e é para isso que servem.

### Portão 1 — nenhum `save_profile` novo em `app/` fora do funil

`test_nenhuma_gravacao_de_perfil_fora_do_funil` varre `app/**/*.py` **por AST**
(não por texto — texto acusaria o import, a docstring e o nome do parâmetro, e
portão com falso positivo em massa vira portão desligado) atrás de chamadas a
`save_profile`, e reprova qualquer uma fora da lista de autorizados.

A mensagem de falha diz o que fazer, porque a tentação óbvia é a errada:

> *"Se este teste reprovar, a resposta **NÃO** é acrescentar o arquivo à lista:
> é chamar `_gravar_perfil_async`."*

**Este é o portão que fecha o argumento do funil.** Quem escrever o quinto botão
não precisa saber que `with_profile_identity` existe — **não consegue gravar por
fora.**

### Portão 2 — a lista de autorizados só ENCOLHE

`test_a_lista_de_autorizados_nao_cresce_em_silencio` trava o conteúdo exato de
`_AUTORIZADOS_A_GRAVAR`:

```python
assert sorted(_AUTORIZADOS_A_GRAVAR) == [
    "actions/profile_writer.py",
    "actions/profiles_actions.py",
]
```

Sem ele, o Portão 1 **se dissolveria por acréscimo**: bastaria escrever o nome
do arquivo novo na lista para voltar a gravar por fora, e o portão continuaria
verde enquanto o defeito voltava.

Portão companheiro, no mesmo arquivo:
`test_quem_esta_autorizado_cumpre_a_invariante_por_conta_propria` exige que
**todo** autorizado contenha `with_profile_identity` no fonte — *autorizado a
gravar não é autorizado a esquecer o rascunho*.

### Portão 3 — o funil carimba `origem=`

`test_o_funil_carimba_a_origem_da_gravacao` exige que a chamada seja
`save_profile(profile, origem=f"janela:{evento}")`.

Este portão fecha uma lacuna que **custou uma madrugada inteira**: em 05/08 o
disco dela tinha `sackboy_nativo` com prioridade 191 e **não havia como decidir**
entre duas explicações igualmente plausíveis — a catraca do rodapé
(`191 = 1 + 10×19`) ou o controle deslizante da aba Perfis, cuja faixa é 0-200.
**Cinco agentes leram código e journal e nenhum conseguiu provar**, porque o
produto **não registrava gravação de perfil**.

Sem a `origem`, o campo cai no basename do processo — que para toda a janela é
o mesmo, e a pergunta *"qual botão fez isto?"* continua sem resposta. Com ela, a
resposta passa a estar na linha do journal, junto de `match_antes`/`match_depois`
e `priority_antes`/`priority_depois`.

## Cura → teste, com a mordida declarada

| cura | onde | teste que morde | o que se vê com a cura arrancada | grau |
|---|---|---|---|---|
| reapontar o rascunho | `profile_writer.py:191` | `test_salvar_com_nome_novo_reaponta_o_rascunho`, `test_os_source_batem_com_o_perfil_gravado`, `test_importar_por_cima_do_perfil_ativo_atualiza_a_fotografia` **+ 4 pelo assert de invariante** | **7 vermelhos** | **MEDIDO** |
| prioridade herdada de quem existe | `footer_actions.py:367` | `test_salvar_por_cima_de_perfil_que_ja_existe_herda_a_prioridade` | reprova com **`10 != 50`** | **MEDIDO** |
| **as DUAS juntas** | — | `test_a_prioridade_e_a_regra_do_primeiro_save_sobrevivem` | *"o segundo save subiu a prioridade para 20"* — **a catraca medida, reproduzida** | **MEDIDO** |
| `match` herdado de quem existe (REGRA-NÃO-SE-PERDE-01) | `footer_actions.py:420` | `test_salvar_por_cima_de_perfil_que_ja_existe_herda_a_regra` | fica vermelho com `match.type == "any"` | mordida **DECLARADA** na docstring; sem registro de execução independente |
| `origem=` no `save_profile` do funil | `profile_writer.py:116` | `test_o_funil_carimba_a_origem_da_gravacao` | fica vermelho | mordida **DECLARADA** na docstring |
| restore devolve o perfil gravado quando a releitura falha | `footer_actions.py` (gancho `_rascunho_restaurado`) | `test_restaurar_padrao_deixa_o_rascunho_no_meu_perfil` | — | não verificada isoladamente |

**Honestidade sobre o que NÃO morde**, pela mesma regra da casa que a
`TRAVA-QUE-SOLTA-TARDE-01` seguiu:

- **`test_perfil_novo_pelo_rodape_continua_nascendo_sempre` é GUARDA, não
  mordida.** Ele passa nos dois estados. Existe para impedir que a
  `REGRA-NÃO-SE-PERDE-01` vire licença para o perfil **novo** herdar o regex de
  outro jogo — o defeito que a decisão do `draft_config` fechou. As duas
  decisões convivem, e este teste é a prova de que continuam convivendo;
- **`test_importar_outro_perfil_nao_rouba_o_rascunho`** também é guarda: protege
  a borda que a *cura* introduziu (reapontar o rascunho não pode virar "todo
  import sequestra a janela");
- os **três portões estáticos** não medem comportamento nenhum. Eles medem a
  forma do código, e isso está declarado — um portão estático verde **não** é
  prova de que a gravação funciona.

**A bancada é o `HefestoApp` de verdade, montado dos DOIS mixins** que o
aplicativo compõe (`ProfilesActionsMixin` + `FooterActionsMixin`): o cálculo da
prioridade mora na aba Perfis e o gesto mora no rodapé, e testar o rodapé sem o
irmão mediria uma composição que não existe — o rodapé cairia no piso de
fallback e **a catraca não apareceria**.

## O que o funil arrastou (e por que está anotado)

Mover a gravação para um módulo novo mudou **onde o dublê de disco tem de ser
plantado**. Três arquivos ganharam nota, para que ninguém reaprenda isso:

- `tests/unit/test_abas01_conflito_entre_abas.py:99` e
  `tests/unit/test_perfil_salva_tudo_abas.py:90` — o `monkeypatch` do
  `save_profile` mudou de `footer_actions` para `profile_writer`, *"o dublê de
  disco tem de ser plantado onde a gravação acontece de verdade"*;
- `tests/unit/test_dedup_guard.py:171` — **NOTA DATADA (04/08/2026)**: aquele
  teste exigia `>= 3` chamadas de `launch_env.refresh` no rodapé, uma por botão.
  Os três botões passaram a avisar o daemon **pelo mesmo funil**, que avisa uma
  vez por gravação; contar chamadas no rodapé passou a medir a **forma antiga**
  do código, não a garantia. A garantia continua a mesma e é o que se cobra
  agora: **o funil avisa, e os três botões passam pelo funil.** A decisão
  anterior não foi apagada — ganhou a nota.

## O que fica ABERTO

**Da própria lista de autorizados:**

- **`app/actions/profiles_actions.py` é EXCEÇÃO DATADA (04/08/2026)** e continua
  gravando fora do funil. A razão está escrita na lista: a aba Perfis grava
  dentro de uma **transação própria** — confirma sobrescrita, apaga o perfil
  antigo no rename, migra o marker de ativo no daemon — e cumpre a invariante
  por conta própria, pelo `_reconciliar_rascunho_com_perfil_salvo`. **Convertê-la
  é trabalho de outra leva.** Enquanto não for, o Portão 2 garante o essencial:
  **essa lista só pode ENCOLHER.** Acrescentar um terceiro nome reprova a suíte.

**Defeitos do rodapé que esta sprint NÃO toca** (todos **MEDIDOS**, todos na
seção 1.1 da síntese):

- **Importar compara nome CRU** (I-1): `on_import_profile` não usa slug, ao
  contrário do irmão `on_save_profile`. Importar um `Navegacao.json` por cima da
  `Navegação` dela **não dispara diálogo nenhum** e sobrescreve o arquivo.
  **Cinco dos quinze perfis dela colidem por acento ou caixa;**

> **NOTA DATADA — 06/08/2026: o número caducou; a frase, não.** São **13**
> arquivos hoje e **nove** nomes cujo slug difere; e "colidir" aqui nunca
> significou perfil contra perfil — significa que uma variante digitada cai
> em cima do arquivo que já existe. A conta e o porquê estão em
> [JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md).

- **Importar não recarrega as abas** (I-8) — o restaurar chama `_refresh_all_tabs`,
  o importar não;
- **"Salvar" não aplica** (I-6): a aba Perfis reaplica o perfil quando o salvo é
  o ativo (`PERFIL-SAVE-APPLY-01`); **o rodapé nunca recebeu essa cura**;
- **o `MatchAny()` do rodapé continua sem aviso na tela** — a `DIV-2`, acima.

**Da faixa de prioridade, que esta sprint encostou e não fechou:**

- **três números convivem** para o mesmo conceito "nascer acima dos catch-all":
  **15** (`_PISO_ACIMA_DOS_CATCH_ALL`, `footer_actions.py:131`),
  **`max(catch-all) + 10`** (o cálculo real) e **5 / 0** (os dois caminhos de
  "criar perfil"). **Ninguém reconciliou os três** — DIV-7, aberta desde 25/07;
- **a escala satura no teto:** com qualquer catch-all ≥ 190, todo perfil novo
  nasce exatamente em **200** e empata; o desempate cai no incumbente ou na
  **ordem alfabética do nome do arquivo** (D-26). O funil não muda isso.

**Do processo:**

- **nada disto está commitado.** A leva inteira está no índice; um
  `git stash`/checkout a perde;
- **a origem do 191 segue indeterminada** (DIV-1). O instrumento que decide já
  existe — o `profile_salvo` com `origem=janela:<botão>` — e falta **o próximo
  gesto dela** para lê-lo;
- **os arquivos de perfil dela não podem ser tocados** para "normalizar" o
  `sackboy_nativo`, inclusive por esta cura. Veto repetido em cinco documentos;
  o destino daquele arquivo é **decisão dela**;
- **o aceite na tela.** Nenhuma afirmação desta sprint é sobre aparência —
  **ninguém olhou a tela**. Que o gesto de salvar duas vezes preserve o perfil
  dela, no uso dela, só o **olho dela** fecha (`PROVA-DE-TELA-01`);
- **esta faixa continua sem índice.** Esta sprint não tem `INDICE` que a liste,
  e é isso que deixou meias-entregas passarem por aqui desde 30/07.
