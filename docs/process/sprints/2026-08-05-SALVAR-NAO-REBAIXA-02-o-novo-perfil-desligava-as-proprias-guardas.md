# SALVAR-NÃO-REBAIXA-02 — o "Novo perfil" desligava as próprias guardas

- **Achado em:** 05/08/2026, na madrugada de perfis, ao reproduzir em bancada
  os sete cenários de salvamento. É o **cenário F** da matriz
- **Estado:** **CURA APLICADA**, com nove mordidas verificadas uma a uma
  (05/08, neste documento)
- **Gravidade:** **ALTA** — reproduz **exatamente** o estado do disco dela
  (`match=any, prio=191, suppress=true`), e o efeito é o perfil do jogo
  perdendo dentro do jogo
- **Causa-raiz:** **PROVADA no código e REPRODUZIDA em bancada**; a atribuição
  do arquivo dela a **este** caminho continua **SUSPEITA** (ver DIV-1)
- **Síntese da leva:**
  [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  — defeito **D-02**, cenário **F** do D-03
- **Índice:** **não existe.** A faixa de perfis está órfã desde 30/07, e isso é
  parte do achado (ver *"Por que ninguém estava olhando"*)

---

## NOTA DATADA — 06/08/2026: o aviso desta sprint matou a janela dela

**Nada aqui está errado, e nada aqui foi apagado.** O diagnóstico, a cura e as
nove mordidas continuam valendo: baixar prioridade em silêncio custava
configuração dela, e o aviso tem de existir. **O que esta sprint não previu foi
o CANAL.**

Em 06/08/2026, às 20h22, ela baixou a prioridade do perfil "Vitória" de 78 para
0 — o gesto que o `profiles/sanidade.py` desta casa **recomenda por escrito** —
e a janela inteira parou de responder: *"interface travou legal aqui. nem
consigo fazer nada nem fechar"*. O `py-spy` pegou a thread principal parada no
`dialog.run()` do `confirm_downgrade_priority` (nascido nesta sprint, na leva 2)
e a foto da tela dela **não tinha diálogo nenhum**.

O defeito não era o aviso: era ele ser um `Gtk.MessageDialog` **modal e
bloqueante** que, se nascer sem foco, prende a janela para sempre. Valia
igualmente para os outros **dez** diálogos de `app/` — o `confirm_downgrade_...`
só teve o azar de ser o que ela usou. Desde então **todos** passam pelo envelope
`gui_dialogs.executar_dialogo`, que mostra o diálogo de verdade e devolve a
janela a ela se ele não conseguir aparecer.

A conta inteira — pilha, causa, alcance e as sete mordidas — está em
[DIÁLOGO-QUE-MATA-A-JANELA-01](2026-08-06-DIALOGO-QUE-MATA-A-JANELA-01-o-aviso-que-deixou-a-janela-dela-morta.md).
O item *"o aceite de tela"* do **O que fica ABERTO** continua aberto para os
diálogos ainda não fotografados; os dois desta sprint já foram (05/08).

---

## Aviso de origem: esta página nasce sobre um vazio

**A SALVAR-NÃO-REBAIXA-01 nunca virou documento.** São **11 citações** em
`src/` e `tests/`, **zero** em `docs/` — está catalogada como órfã total em
duas listas independentes desta casa
([o backlog real conferido contra o código](../estudos/2026-08-03-o-backlog-real-conferido-contra-o-codigo.md),
[DOC-QUE-NÃO-MENTE-03](2026-08-03-DOC-QUE-NAO-MENTE-03-a-foto-vazia-a-env-negada-e-a-tag-velha.md)).
A 02 tem **15**, e escrever a 02 sem a 01 seria documentar a emenda sem o
tecido.

Então o resumo abaixo é **reconstruído das docstrings e da mensagem de commit**,
não de uma página que não existe. **Grau: MEDIDO** (o texto-fonte está no
repositório; o commit é `8d7fd45`, 28/07 19:44).

### O que foi a SALVAR-NÃO-REBAIXA-01, em cinco linhas

- **O defeito:** o `base.update` de `_build_profile_from_editor` reescrevia
  `match` e `priority` **sempre**, com o que estivesse nos widgets. Como o
  editor simples mostra *"Qualquer"* para todo match que ele não reconhece, e a
  escala tinha teto, **salvar a cor pela aba Perfis apagava a regra do jogo**.
- **A datação no disco dela** (`profiles_actions.py:2090-2096`): `Pragmata` era
  regra de jogo com prioridade 100 em **26/07 às 23h40** e amanheceu catch-all
  em **27/07 às 23h04**; `vitoria` caiu de 100 para 0.
- **A cura:** duas fotografias tiradas na abertura do editor — `_regra_do_disco`
  / `_assinatura_da_regra_ao_abrir` e `_prioridade_do_disco` /
  `_prioridade_ao_abrir` (`profiles_actions.py:468-475`) — e duas guardas no
  salvamento: *regra e prioridade só são reescritas quando ela **mexeu** nelas*.
- **A decisão fina, e ela importa para a 02:** mexer conta pelo **gesto**
  (`_regra_tocada`, `_prioridade_tocada`), não pela coincidência de valor. Um
  perfil acima do teto abre **clampado**, e arrastar a escala até o teto de
  propósito **precisa valer** — senão a guarda vira o mesmo cadeado que ela
  existe para impedir, no sentido contrário (`:476-486`).
- **O que ela cobre:** o caminho `_populate_editor` → editar → Salvar. **Só
  ele.**

**A frase que a 02 vem corrigir** está escrita na própria 01
(`profiles_actions.py:2100-2103`): *"num perfil novo (sem fotografia) nada muda:
os widgets seguem sendo a fonte"*. Era verdade pela metade — e a outra metade é
esta sprint.

---

## O sintoma

Ela clica **"Novo perfil"**, digita o nome de um perfil que **já existe**, e
salva. O único aviso é o `prompt_overwrite_existing`, que fala em **substituir**
e não em **rebaixar**.

O perfil bom vira um catch-all de prioridade baixa. E o efeito não é cosmético:
**catch-all não tem autoridade nenhuma numa janela de jogo** (veto R-21,
`profiles/manager.py:773-796`), então o perfil que ela fez para o jogo passa a
perder **dentro do jogo** e a ganhar em **todo o resto** — que é a frase
*"está tudo quebrado"* traduzida para código.

## A prova

**MEDIDO** (reprodução em bancada, 05/08, sobre o harness de
`tests/unit/test_perfil_salva_tudo_abas.py`):

```
ANTES   prio=200  match=criteria window_class=['steam_app_1599660']  mode=native
DEPOIS  prio=0    match=any                                          mode=None
```

E o cenário **F** da matriz de sete salvamentos — *"Novo perfil" + nome de um
perfil existente* — produz `match=any, prio=191, suppress=True`, que é o estado
do `sackboy_nativo.json` dela **campo a campo, inclusive o `suppress`**.

**Honestidade sobre o que isso prova e o que não prova.** Reproduzir o estado
não prova que **foi este** o gesto: a DIV-1 da síntese registra **três**
explicações incompatíveis para o 191 (a catraca do rodapé, o polegar dela no
slider, este cenário F), e o instrumento que decide — a linha `profile_salvo`
no journal — só passou a existir nesta mesma leva. **Grau da atribuição:
SUSPEITA COM MECANISMO.** **Grau do defeito: MEDIDO.**

## A causa-raiz: a guarda desligava a si mesma

`on_profile_new` chamava `_esquecer_a_fotografia_do_editor()`
(`profiles_actions.py:1829-1842`), que zera as quatro fotografias. E as duas
guardas da 01 têm a forma:

```python
if <do_disco> is not None and not <foi_mexida>():
    <preserva o valor do disco>
```

Com as fotografias em `None`, **os dois `if` são pulados** e os widgets vencem
— inclusive quando o Salvar vai por cima de um arquivo que **existe**. A escala
acabou de ir a 0 e o seletor a *"Qualquer"*, porque é assim que um perfil novo
nasce.

**A guarda de 27/07 não falhou: ela foi desligada por um botão vizinho.**

### E havia um segundo defeito, dentro do primeiro

Achado na LEVA 2, ao escrever a cura: `_esquecer_a_fotografia_do_editor` estava
no **topo** de `on_profile_new`, **antes** do `set_value(0)` e do
`set_active_id("any")`. Esses dois disparam os sinais que marcam gesto
(`_on_prioridade_tocada`, `_on_aplica_a_changed`) — então **o próprio
nascimento do perfil levantava `_prioridade_tocada` e `_regra_tocada`**.

Isso é pior que o primeiro defeito, porque **sobrevive à cura dele**: com a
fotografia relida mas as marcas levantadas, a guarda funcionaria e ainda assim
rebaixaria, agora **acreditando numa escolha que ela não fez**. O
`_populate_editor` sempre zerou as marcas **por último**, exatamente por isto
(`:1742-1744`, *"Zeradas por ÚLTIMO: as seleções feitas acima são de abertura,
não dela"*). **O `on_profile_new` era o único lugar que fazia ao contrário.**

## O furo na rede de segurança

Dois diálogos deveriam ter avisado. **Nenhum dos dois tinha o que dizer:**

| diálogo | por que ficou calado |
|---|---|
| `prompt_overwrite_existing` | dispara, mas fala em **substituir** — genérico, e ela **quer** substituir |
| `confirm_downgrade_match_to_any` | só disparava com `isinstance(original.match, MatchCriteria)` — e os perfis dela **já estão em `MatchAny`**, rebaixados pelo defeito de 27/07. **Não há match a rebaixar** |
| *(um terceiro)* | **não existia**: nenhum diálogo desta casa avisava sobre queda de **prioridade** |

E é a prioridade que importa nos perfis dela: com todos em `MatchAny`, ela é
**o único termo que ainda decide qual dos "Sempre" vence**
(`explicacao_da_disputa`, `profiles_actions.py:264`).

## A cura aplicada

### 1. A releitura da fotografia na hora de salvar

`_perfil_que_o_salvar_sobrescreve` (`profiles_actions.py:1814-1827`), novo, e
`_build_profile_from_editor` (`:2127-2135`) o consulta quando a fotografia está
ausente **e o alvo existe em disco**:

```python
if prioridade_do_disco is None or regra_do_disco is None:
    alvo_no_disco = self._perfil_que_o_salvar_sobrescreve(name)
    if alvo_no_disco is not None:
        if prioridade_do_disco is None:
            prioridade_do_disco = alvo_no_disco.priority
            prioridade_mexida = self._prioridade_tocada
        if regra_do_disco is None:
            regra_do_disco = alvo_no_disco.match
            regra_mexida = self._regra_tocada
```

Três decisões, cada uma com motivo:

1. **a busca é por SLUG**, nunca por nome de exibição — a lição do **R-10**, e a
   mesma pergunta que `on_profile_save` já faz com `find_by_slug` para decidir o
   diálogo de sobrescrita. `Navegação` e `Navegacao` são **o mesmo arquivo**;
2. **a evidência de intenção passa a ser o gesto puro** (`_prioridade_tocada`,
   `_regra_tocada`) em vez da comparação com a assinatura de abertura — porque
   **não há abertura**: o editor nunca mostrou este perfil;
3. **lê o cache em memória, nunca o disco** — este caminho roda na thread do
   GTK (PERF-GUI-PROFILE-LOAD-NONBLOCKING-01).

**E a cura é de ESCOPO, não de remoção.** `_esquecer_a_fotografia_do_editor`
continua certa e continua existindo: perfil que não existe não tem valor de
disco a preservar. O veto nº 13 da síntese diz isso com todas as letras.

### 2. O `_esquecer` desce para o fim de `on_profile_new`

`profiles_actions.py:1084` — depois de posicionar **todos** os widgets, na mesma
ordem que `_populate_editor` sempre teve. Com uma exceção deliberada: o prefill
do jogo em foco (`_aplicar_nascimento_com_jogo`, assíncrono, logo abaixo) marca
os gestos **de verdade** e continua vencendo — ali a escolha **é** do editor,
que é a entrega da PERFIL-NASCE-CERTO-01.

### 3. A guarda do match: de `MatchCriteria` para "não é `MatchAny`"

`profiles_actions.py:1386-1401`. A pergunta passou a ser a certa: **o perfil
deixa de ter alvo? Então avisa.**

**Precisão sobre o que era o furo** — os três `Match` são classes irmãs
(`profiles/schema.py:51`, `:97`, `:108`), nenhuma herda da outra:

- **`MatchManual`** (o sentinel de *"só entra quando eu mandar"*, R-12 item 3):
  **passava calado pela guarda antiga**. Este era o furo de verdade;
- **`MatchCriteria` com os três campos vazios** (o caso do preset `coop_local`
  de fábrica): a guarda antiga **pegava** — mas o diálogo dizia *"vale só em
  programas específicos"*, e não há programa nenhum. O furo aqui era a **frase**,
  não a guarda.

Por isso a segunda metade: `confirm_downgrade_match_to_any` ganhou
`regra_atual` (`app/gui_dialogs.py:105-150`), e o chamador passa
`_match_label(original.match)` — **o mesmo rótulo da coluna "Quando usar"**. O
diálogo não pode chamar de *"programas específicos"* um perfil que a lista
chama de *"Só manual (nunca ativa sozinho)"*.

### 4. O aviso de queda de prioridade, que não existia

`app/gui_dialogs.py:154-195` (`confirm_downgrade_priority`) e a regra **pura**
em `profiles_actions.py:311-318`:

```python
QUEDA_DE_PRIORIDADE_QUE_PEDE_AVISO = 10

def queda_de_prioridade_pede_aviso(antes: int, depois: int) -> bool:
    return int(depois) < int(antes) and (
        int(antes) - int(depois)
    ) >= QUEDA_DE_PRIORIDADE_QUE_PEDE_AVISO
```

**O limiar não é arbitrário:** dez é a mesma folga com que um perfil de jogo
nasce acima do catch-all (`_FOLGA_ACIMA_DO_CATCH_ALL`, `:83`). Abaixo disso a
queda não muda quem vence disputa nenhuma desta casa, e **um diálogo por ponto
perdido é o ruído que se aprende a clicar sem ler** — o que mataria também o
aviso que importa. Há teste para o limiar e para o ruído.

Ser **função pura** é decisão de testabilidade: a regra é verificável sem GTK,
sem disco e sem daemon, e é onde moram cinco das mordidas.

## O teste que morde

`tests/unit/test_salvar_nao_rebaixa_02_o_novo_perfil_desligava_as_guardas.py` —
**19 casos**, bancada hermética (widgets falsos com a mesma API por-ID da aba,
nenhum GTK real, nenhum daemon, nenhuma escrita no `~/.config` dela). O dublê
`_FakeScale` **reproduz a condição em vez de escondê-la**: o `GtkScale` de
verdade só emite `value-changed` quando o valor **muda**, e é por isso que o
`set_value(0)` do nascimento marcava gesto **às vezes**.

**Mordidas verificadas em 05/08, neste documento** — cinco mutações cirúrgicas,
uma cura por vez, arrancada, rodada e devolvida:

| cura arrancada | reprovam |
|---|---|
| `_perfil_que_o_salvar_sobrescreve` devolvendo `None` | **3** — `test_salvar_por_cima_preserva_regra_e_prioridade_do_disco`, `test_olhar_o_perfil_antes_de_clicar_novo_nao_o_rebaixa`, `test_o_alvo_e_achado_pelo_slug_e_nao_pelo_nome_de_exibicao` |
| `_esquecer` de volta ao topo de `on_profile_new` | **2** — `test_o_nascer_do_novo_perfil_nao_conta_como_gesto`, `test_olhar_o_perfil_antes_de_clicar_novo_nao_o_rebaixa` |
| guarda do match de volta a `isinstance(..., MatchCriteria)` | **1** — `test_so_manual_virando_vale_para_tudo_avisa_com_a_palavra_certa` |
| o `if` do aviso de prioridade desligado (a **fiação**) | **1** — `test_baixar_a_prioridade_pergunta_e_cancelar_nao_toca_o_disco` |
| o limiar levado a um número inalcançável (a **regra**) | **3** — `test_a_queda_medida_no_disco_dela_avisa`, `test_a_folga_do_perfil_de_jogo_e_o_limiar`, `test_baixar_a_prioridade_pergunta_e_cancelar_nao_toca_o_disco` |

Devolvidas as cinco curas: **19 verdes** (41 com a ATIVAR-NÃO-MENTE-01 no mesmo
comando).

**`test_olhar_o_perfil_antes_de_clicar_novo_nao_o_rebaixa` morde as duas metades
ao mesmo tempo** — é a sequência real dela: estava olhando o perfil bom, clica
"Novo perfil", digita o mesmo nome, salva.

**As duas últimas linhas da tabela são de propósito.** A regra pura e a fiação
que a chama são mutações **diferentes**, e cada uma tem quem a acuse: constante
certa com chamada errada não cura nada, e é exatamente a forma de meia-entrega
que a
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
existe para catalogar.

**Honestidade sobre o que NÃO morde este defeito.** **Oito** dos 19 mordem;
os **onze** restantes passam com o produto quebrado, em três famílias, todas
declaradas:

- **guardas anti-correção-demais** (a cura não pode virar cadeado):
  `test_a_escolha_dela_no_perfil_novo_continua_vencendo`,
  `test_perfil_novo_com_nome_inedito_nasce_dos_widgets` (o R-09),
  `test_nascer_com_o_jogo_em_foco_vence_o_que_esta_no_disco` (a
  PERFIL-NASCE-CERTO-01), `test_editar_um_perfil_da_lista_segue_pela_fotografia_de_abertura`
  (o caminho da 01), `test_regra_especifica_continua_avisando_com_a_frase_de_sempre`
  (a COR-A não regride) e `test_confirmar_a_queda_grava_o_que_ela_pediu`
  (confirmar não pode virar cancelar);
- **anti-ruído**, que é metade do valor do limiar: `test_subir_nunca_avisa`,
  `test_ficar_igual_nunca_avisa`, `test_queda_pequena_nao_vira_ruido`,
  `test_queda_pequena_salva_sem_incomodar`;
- **tema do diálogo** (`test_o_dialogo_novo_nasce_com_o_tema_do_app`) — GUI-05/P5,
  um defeito de outra família: diálogo sem `_apply_app_theme` abre **claro** no
  COSMIC sob XWayland.

## Por que ninguém estava olhando

**A faixa de perfis está órfã desde 30/07.** As menções a
`PERFIL-SALVA-TUDO | AUTOMATISMO-MORTO | PERFIL-NASCE-CERTO | EMPATE-01 |
ABAS-01 | PERFIL-JOGO-01` caem de **15** no índice de 30/07 para **4** em 31/07
e **0** em 01/08, 03/08 e nas ONDAS.

**É a explicação estrutural de por que meias-entregas passaram nesta área** — e
esta sprint é o exemplo perfeito: a cura de 27/07 foi escrita, testada, e
**desligada por um botão vizinho** sem que nada reclamasse por oito dias.
Somado ao fato de a 01 nunca ter virado página, o resultado é uma decisão
medida que **só existia como comentário de código**.

## O que fica ABERTO

- **a origem do 191 continua indeterminada** (DIV-1). O instrumento que decide
  já existe — o `profile_salvo` no journal, criado nesta mesma leva pela
  [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md)
  — e já capturou uma linha: `match_antes=criteria match_depois=any
  priority_antes=10 priority_depois=191`. **Falta o próximo gesto dela**;
- **o `match` ainda não é herdado do disco no funil do rodapé** — resíduo
  declarado da cura irmã (o DEFEITO A). Salvar por cima de um perfil que existe
  **e é diferente do ativo** continua gravando `MatchAny()`. Mexer ali brigaria
  com o **R-11**, e o veto nº 14 da síntese o protege: *o defeito é o segundo
  save, não o primeiro*;
- **`importar` continua comparando nome cru** (I-1), sem a guarda de slug que
  este Salvar acabou de ganhar. Cinco dos quinze arquivos dela colidem por
  acento ou caixa;
- **a escala satura no teto** (D-26): com qualquer catch-all acima de 190, todo
  perfil novo nasce em 200 e o desempate cai na ordem alfabética do `glob`. E
  **três números convivem** para o mesmo conceito de *"nascer acima dos
  catch-all"*: 15, `max(catch-all)+10`, e os defaults 5/0 (DIV-7). **Ninguém
  reconciliou os três**;
- **o destino do `sackboy_nativo.json` é decisão DELA.** É o perfil **ativo**,
  catch-all, 191, com supressão ligada. **Não escrever nos `.json` dela sem
  autorização explícita, inclusive "só para normalizar"** — veto repetido em
  cinco documentos desta casa;
- **o aceite de tela.** Os dois diálogos novos **nunca foram fotografados**.
  Nenhuma afirmação aqui é sobre aparência, e interface não fecha sem o olho
  dela ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).
