# Síntese consolidada — o sistema de perfis, madrugada de 05/08/2026

> **Como este documento nasceu.** A sessão da madrugada de 05/08 foi compactada, e
> com ela sumiu do contexto o que dezessete subagentes tinham medido. Os relatórios
> não se perderam: cada subagente tem transcrito próprio, e eles foram recuperados e
> consolidados aqui em 05/08/2026, a pedido dela — *"não sei se consegue restaurar as
> pesquisas deles e tal"*. O que estava em `/tmp` é volátil; esta página é o que dura.

**Origem:** 17 relatórios de subagentes (~362 KB) recuperados de sessão compactada, sob
`.../scratchpad/pesquisa-madrugada/`. Sete são LEVA 1 (entender), quatro são LEVA 2
(implementar), seis são leituras integrais do acervo de sprints.

**Aviso de método, herdado da casa e reconfirmado aqui:** *"o campo `Status:` dos documentos
não é fonte"* (`docs/process/sprints/2026-07-30-INDICE-as-tres-faixas-depois-da-v040.md:14-21`;
repetido em `2026-08-01-APLICAR-VERDADE-01-...md:198-199`). Toda afirmação abaixo diz de onde vem.

**Aviso de números de linha:** a árvore mudou durante a madrugada, com agentes irmãos escrevendo
em paralelo. As linhas citadas pelas *sprints* são de datas anteriores; só as verificações por
grep desta madrugada valem contra a árvore de hoje. Onde os relatórios discordam de linha, isso
está marcado na seção 4 (DIV-10).

---

## 1. Defeitos MEDIDOS

Critério: há journal, execução ao vivo, reprodução em bancada ou teste que reprova.

### 1.1 A escrita de perfil pela janela

#### D-01 — O "Salvar Perfil" do rodapé nunca reaponta o rascunho (o DEFEITO A)

- **Onde:** `src/hefesto_dualsense4unix/app/actions/footer_actions.py:352-368` (`_on_saved`)
  atualiza `_active_profile_name` (:356) e `_draft_baseline` (:361), e **não** toca `self.draft`.
  O método que existe para isso — `app/draft_config.py:629` `with_profile_identity` — tinha
  **um único chamador em produção**: `app/actions/profiles_actions.py:1719`.
- **O que ela sente:** salva um perfil, salva de novo, e ele vira "vale sempre" com a prioridade
  subindo de dez em dez. O toast diz "Perfil salvo em …" e nunca diz que a regra virou "Sempre".
- **Evidência:**
  - reprodução ao vivo (janela real sob Xvfb, HOME temporário): cinco cliques em "Salvar Perfil"
    sem mudar nada → `prio=11, 21, 31, 41, 51`, `match=any` em todos;
  - bancada independente em HOME temporário: 1º save `priority=10`, 2º save `priority=20`;
  - o agravante que fecha o caso: a docstring do próprio método (`draft_config.py:644-650`)
    descreve **textualmente o caminho do rodapé** como um dos dois defeitos que ele cura.
    *A cura foi escrita para o rodapé e ligada só na aba Perfis.*
- **Cadeia verificada linha a linha:** `footer_actions.py:344-347` → `_prioridade_acima_dos_catch_all()`
  (`profiles_actions.py:1620-1634`, `_FOLGA_ACIMA_DO_CATCH_ALL = 10` em `:82`,
  `PRIORIDADE_MAXIMA = 200` em `:77`) → `footer_actions.py:350` `save_profile(draft.to_profile(...))`
  → `draft_config.py:562-563` `mesmo_perfil` responde **False** porque `source_name` está velho →
  `:573-574` grava a prioridade calculada e `:580-584` grava `MatchAny()`.
- **Por que a suíte era verde:** `tests/unit/test_footer_salvar_nasce_acima_dos_catch_all.py:136-152`
  afirma o vínculo **lendo o texto-fonte** (`assert "_prioridade_acima_dos_catch_all" in texto`);
  `test_abas01_conflito_entre_abas.py:437` só exercita o rodapé com o nome igual ao perfil ativo.
  Nenhum teste cobria dois saves consecutivos. É a mordida na metade errada da cadeia, o padrão
  que a `ENTREGA-QUE-NÃO-LIGOU-01` catalogou.
- **Datação da causa:** commit `2bbfa22` (30/07 01:41) landou `mesmo_slug` em `draft_config.py`
  **e**, no mesmo commit, ligou `_prioridade_acima_dos_catch_all` no rodapé. Antes dele havia o
  bug do `MatchAny`, **mas não havia catraca**. As duas metades juntas é que escalam.
- **Estado:** CURADO na árvore (seção 5-A), com resíduo declarado.

#### D-02 — "Novo perfil" desliga as guardas SALVAR-NAO-REBAIXA-01 (o DEFEITO B)

- **Onde:** `profiles_actions.py:944-955` `on_profile_new` chama `_esquecer_a_fotografia_do_editor()`
  (`:1607-1618`), que zera `_regra_do_disco`, `_prioridade_do_disco`, `_assinatura_da_regra_ao_abrir`
  e `_prioridade_ao_abrir`. Em `_build_profile_from_editor` (`:1878-1887`) as duas guardas são
  `if <do_disco> is not None and not <foi_mexida>()` — com `None`, ambas são puladas e os widgets
  vencem. A escala acabou de ir a 0 (`:957`) e o seletor a "Qualquer" (`:958`).
- **O que ela sente:** clica "Novo perfil", digita o nome de um perfil que já existe, salva — e o
  perfil bom é substituído por um catch-all de prioridade 0. O único aviso é
  `prompt_overwrite_existing`, genérico, que fala em substituir e não em rebaixar.
- **Evidência (reprodução):** `ANTES prio=200, match=criteria window_class=['steam_app_1599660'], mode=native`
  → `DEPOIS prio=0, match=any, mode=None`.
- **Furo verificado na rede de segurança:** `confirm_downgrade_match_to_any`
  (`profiles_actions.py:1196-1213`) só dispara se `original.match` for `MatchCriteria` — com os
  perfis dela já em `MatchAny`, **o diálogo nunca aparece**. E **não existia diálogo nenhum para
  rebaixamento de prioridade** (só `prompt_overwrite_existing` e o acima, em `app/gui_dialogs.py`).
- **Detalhe achado na LEVA 2:** o `_esquecer` no *topo* de `on_profile_new` fazia o próprio
  nascimento contar como gesto dela — `set_value(0)` / `set_active_id("any")` levantavam
  `_prioridade_tocada` / `_regra_tocada`.
- **Estado:** CURADO na árvore (seção 5-B).

#### D-03 — Sete cenários de save, três que corrompem (matriz reproduzida)

Rodados sobre o harness de `tests/unit/test_perfil_salva_tudo_abas.py`:

| cenário | resultado |
|---|---|
| A — aba Perfis, arrastar prioridade, Salvar | preservado, prio 191 |
| B — abrir e Salvar sem tocar | preservado |
| C — rodapé, mesmo nome, rascunho coerente | preservado |
| **D — rodapé com rascunho STALE** | **`match=any, prio=10, mode=None, suppress=False`** |
| **E — aba Perfis, editor em outro perfil, nome digitado por cima** | **`match=any, prio=0`** |
| **F — "Novo perfil" + nome de um perfil existente** | **`match=any, prio=191, suppress=True`** |
| G — dois Salvar seguidos | preservado |

O cenário **F reproduz o disco dela exatamente**. A guarda SALVAR-NAO-REBAIXA-01
(`profiles_actions.py:1866-1896`) funciona no caminho normal e **não cobre os três caminhos que
não passam por `_populate_editor`**.

#### D-04 a D-09 — os seis defeitos do rodapé, medidos em bancada com HOME temporário

| # | Defeito | Caminho | Evidência medida |
|---|---|---|---|
| **I-1** | **"Importar" come o perfil dela sem perguntar** | `footer_actions.py:424` e `:430` comparam **nome cru**; o irmão `on_save_profile` já usa slug (`:308`, `find_by_slug`) | disco com `Navegação` (criteria `process_name=['nav']`, prio 7); importar um `.json` chamado `Navegacao` → gate `nome in existentes` False, **nenhum diálogo**; `navegacao.json` vira `match=any priority=99`. Cinco dos quinze arquivos dela colidem por acento/caixa |
| **I-2** | **Importar por cima do ativo é desfeito pelo próximo "Salvar"** | import não toca o rascunho | depois de importar: `match=any priority=88 lightbar=[7,7,7]`; depois de um "Salvar Perfil": `match=criteria(['nav']) priority=7 lightbar=[0,0,0]`. **O import foi integralmente revertido** |
| **I-3** | **Salvar com nome novo: a janela abandona o perfil que ela acabou de criar** | `_on_saved` escreve `_active_profile_name` sem reapontar o rascunho; o daemon não é avisado | depois do save: `_active_profile_name='Pragmata2'`, `source_name='Pragmata'`, cor `(255,0,255)`; **após o tique de 2 Hz**: recarregou de `['Pragmata']`, cor `(0,0,0)`. Nenhuma mensagem |
| **I-5** | **"Restaurar Default" mente sobre o perfil ativo** | `footer_actions.py:539` grava `_active_profile_name="meu_perfil"` sem `profile.switch` | depois do restore as abas mudam; após o tique voltam a `Pragmata`. **O hardware seguiu com o perfil anterior o tempo todo** |
| **I-6** | **"Salvar" não aplica e "Aplicar" não salva** | `Aplicar → IPC ['profile.apply_draft']`, disco intacto; `Salvar → IPC ['launch_env.refresh']`, daemon intacto | a aba Perfis resolve isso (`profiles_actions.py:1260-1265`, `profile_switch` quando o salvo é o ativo, PERFIL-SAVE-APPLY-01). **O rodapé nunca recebeu essa cura** |
| **I-8** | **Importar não recarrega aba nenhuma** | `_import_save_async` (`:459-483`) chama `_reload_profiles_store` e não `_refresh_all_tabs` | restaurar chama; importar não |

**Diagnóstico estrutural que amarra os seis:** *"Que perfil eu estou editando?" tem hoje três
respostas independentes* — `draft.source_name`, `HefestoApp._active_profile_name` e
`state["active_profile"]` do daemon — e cada consumidor pergunta a uma diferente: `to_profile`
à primeira (`draft_config.py:562`), o pré-preenchimento do diálogo à segunda
(`footer_actions.py:289`), a reconciliação compara a segunda com a terceira (`app/app.py:849`).

#### D-10 — O texto do aviso de divergência está errado em dois pontos

`app/app.py:864-869` diz *"Salve ou use 'Restaurar Padrão' para acompanhar o perfil novo."*
Medido: (a) não existe botão com esse nome — o glade diz **"Restaurar Default"**
(`gui/main.glade:3603`); (b) ele **não acompanha o perfil novo**, carrega `meu_perfil`. Seguindo
o conselho com `Sackboy` ativo, o resultado medido é `_active_profile_name='meu_perfil'` e a
edição dela (cor `9,9,9`) trocada por `(40,80,180)`. **O conselho perde o trabalho dela e não faz
o que promete.**

### 1.2 A ativação de perfil pela janela

#### D-11 — O timeout de 0,25 s faz todo "Ativar" parecer falha

- **Onde:** `profiles_actions.py:1107-1112` chama `call_async` **sem** `timeout_s`, caindo no
  default `app/ipc_bridge.py:104` `timeout_s: float = 0.25`. O handler
  `daemon/ipc_handlers.py:374-492` só responde depois de `clear_manual_trigger_active` →
  `manager.activate` → gatilhos, LEDs, teclado, emulação, alto-falante → `save_active_marker` →
  `materialize_launch_env`.
- **O que ela sente:** clica "Ativar", lê **"Falha (daemon offline?)"**
  (`profiles_actions.py:1124-1128`), a linha não fica em negrito, e clica de novo — e **cada clique
  é uma ativação real e completa**.
- **Evidência (journal dela):**
  ```
  02:40:22.106  profile_activated        name=Pragmata origin=manual
  02:40:23.323  launch_env_materializado                       (+1,217 s)
  02:40:23.378  profile_activated        name=Pragmata          (clicou de novo)
  02:40:24.195  launch_env_materializado                       (+0,817 s)
  02:40:24.201  profile_activated        name=Pragmata          (e de novo)
  ```
  A resposta chega em ~1,2 s; o cliente desiste aos 0,25 s. Sem retry em `cli/ipc_client.py:136-144`
  (o `readline()` vira `IpcError(-1, "conexão timeout")`).
- **O mesmo defeito no applet COSMIC:** `packaging/cosmic-applet/src/ipc.rs:30` `IPC_TIMEOUT = 250 ms`,
  usado em `:348-350`; no timeout `Message::ProfileSwitched(Err)` limpa `self.switching`
  (`src/app.rs:223-232`) e o botão continua clicável (`app.rs:788-792`).
- **Contraste no mesmo repositório:** `footer_actions.py:236-242` usa `timeout_s=1.5` para
  `profile.apply_draft`; `ipc_bridge.py:523` usa `1.0`. **`profile.switch`, de longe o handler mais
  pesado, era o único em 0,25.**
- **Estado:** CURADO na árvore (seção 5-B).

#### D-12 — A janela descarta o `relatorio` que o daemon devolve

- **Daemon monta e envia:** `ipc_handlers.py:403` (`relatorio: dict[str, str]`), `:437-439`
  (`activate(..., relatorio=relatorio)`), `:470-491` (resposta com `active_profile`,
  `mode_aplicado`, `secoes`, `motivo`, `expira_em_sec`); preenchido em `profiles/manager.py:187`,
  `:213-223`, `:444`, `:462-473`, `:574`, `:583`, `:613-617`.
- **Janela descarta:** `profiles_actions.py:1110` `on_success=lambda _result: ...`;
  `ipc_bridge.py:254-256` `ok, _ = _safe_call(...)`, devolve `bool`.
- **Consumidores no repositório inteiro:** **só testes** —
  `tests/unit/test_ipc_server.py:102-106`, `test_r03_lock_manual_adia_modo.py:507-508`,
  `test_ipc_profile_switch_persist.py:117`, `test_ipc_profile_switch_propaga_teclado.py:145`.
  O applet também ignora (`packaging/cosmic-applet/src/app.rs:223-232`).
- **O que ela sente:** *"Perfil ativado: X"* mesmo quando modo, alto-falante e gatilhos foram pulados.
- **Estado:** CURADO na árvore (seção 5-B e 5-C).

#### D-13 — "Ativar" não refaz as abas, e o caminho alternativo tem um portão que desiste

- `on_profile_activate` (`profiles_actions.py:1099-1112`) faz `profile.switch` + toast + destaque
  de linha + `_sync_selection_with_active_profile`. **Não chama `_refresh_all_tabs`** (os dois
  únicos chamadores em produção eram `app/app.py:796` e `footer_actions.py:549`).
- As abas só seguiam pelo tique de 2 Hz — `_reconciliar_draft_com_perfil_ativo`
  (`app/app.py:827-878`, ligado em `:433`) — **e esse caminho recusa em quatro casos**, sendo o
  quarto `draft != baseline`: `if self._tem_edicao_pendente(): <toast>; return` (`:863-873`).
- **Com qualquer edição pendente, as abas nunca acompanham.** É a queixa dela verbatim:
  *"o perfil que eu ativei não aplica imediatamente as features das abas nele."*
- **Efeito colateral medido:** é exatamente esse caso 4 que faz `source_name` ficar velho e
  **sobreviver** — sem edição pendente ele seria apagado por um recarregamento silencioso.
- **Estado:** CURADO na árvore (seção 5-B).

### 1.3 O que impede o perfil de entrar (o daemon)

#### D-14 — `manual_override_categories` não tem TTL e atravessa a ativação como `None`

- **Estrutura:** `daemon/state_store.py:102` `self._manual_override_categories: set[str] = set()`;
  categorias válidas em `:63-65` `MANUAL_OVERRIDE_CATEGORIES = frozenset({"trigger","led","rumble","audio"})`;
  `mark_` `:220-233`, `clear_` `:235-253`, propriedades `:424-428` e `:441-445`.
- **Efeito na aplicação:** `profiles/manager.py:341-348` converte os campos travados em `None`
  ("não mexe"):
  ```python
  trigger_left = None if "trigger" in travadas else left,
  led          = None if "led"     in travadas else effective.lightbar,
  player_leds  = None if "led"     in travadas else settings.player_leds,
  ```
- **Evidência (journal dela):**
  ```
  02:40:22  profile_apply_respeita_override_manual categorias=['audio','led','rumble','trigger'] profile=Pragmata
  02:48:56  profile_apply_respeita_override_manual categorias=['led','rumble','trigger'] profile=sackboy_nativo
  02:51:10  profile_apply_respeita_override_manual categorias=['led','rumble','trigger'] profile=sackboy_nativo
  ```
  **Na ativação do Pragmata, as quatro seções foram puladas — a ativação não escreveu nada visível.**
- **TTL: NENHUM.** Ao contrário de `_emu_manual_ts` e `_manual_profile_lock_until`, as categorias
  só somem por gesto explícito (cinco locais de clear).
- **Quem arma, a partir da janela:** `trigger.set` → `ipc_handlers.py:673`; `led.set` → `:769`;
  `led.player_set` → `:817`; `rumble.set` → `:2649`; `rumble.stop` → `:2666`; `speaker.set` →
  `:3009` via `_marcar_audio_manual`; `profile.apply_draft` → `ipc_draft_applier.py:57-69`
  (**payload sem seção mapeável arma as três**). A pré-visualização ao vivo dos Gatilhos
  (`triggers_actions.py:241-260`, 300 ms) **re-arma `trigger` a cada mexida de slider**.
- **Nenhuma afordância na interface:** `daemon.state_full` (`ipc_handlers.py:1549-1625`) **não
  exporta** o campo; grep em `app/`, `tui/`, `cli/` e no applet acha só **dois comentários**
  (`ipc_bridge.py:329`, `triggers_actions.py:553`). Somado ao D-12, **os dois canais que poderiam
  contar isso a ela estão fechados**.

#### D-15 — A trava era limpa DEPOIS do `activate` (TRAVA-QUE-SOLTA-TARDE-01)

- **Prova (journal, sprint `:36-40`):**
  ```
  00:02:06  profile_apply_respeita_override_manual categorias=['audio','trigger']
  00:02:06  profile_activated name=vitoria origin=manual      (pulou seções)
  00:03:22  profile_activated name=vitoria origin=manual      (aplicou tudo)
  ```
  **A mesma ação repetida dava resultados diferentes.**
- **Alcance:** `ipc_handlers.py` (janela e CLI) — defeito; `daemon/subsystems/hotkey.py`
  (**PS + D-pad, que ela usa dentro do jogo**) — defeito; `profiles/autoswitch.py:505-518`
  (troca automática) — **correto, limpa antes**. *"a paridade copiou a ordem errada"*.
- **Mordida verificada:** com a cura arrancada, **4 dos 6 casos** de
  `tests/unit/test_trava_que_solta_tarde_01.py` reprovam, inclusive
  `test_duas_ativacoes_seguidas_sao_indistinguiveis`.
- **Estado:** CURADO e staged, **não commitado** (seção 5-E).

#### D-16 — A cura da TRAVA não está rodando na máquina dela

- Daemon vivo: PID **1670**, no ar desde **04/08 23:39:46**, sem restart.
- Os dois arquivos alterados têm mtime **05/08 00:38:41** — depois do start. O install é *editable*
  (`_editable_impl_hefesto_dualsense4unix.pth` → `src/` do repo), então só vale no próximo start.
- **Prova de que o código vivo é o antigo:** às **02:51:10** o journal traz
  `profile_apply_respeita_override_manual categorias=['led','rumble','trigger']` **seguido de**
  `profile_activated ... origin=manual`. Essa assinatura é **impossível** no código novo — os dois
  chamadores manuais limpam antes, e não há outro `activate` com `origin="manual"` (os outros são
  `lifecycle.py:970` `origin="system"` e `autoswitch.py:547` `origin="autoswitch"`).
- **Consequência:** o que ela está vendo hoje é o defeito antigo. Reiniciar o daemon é
  **pré-requisito** de qualquer verificação — e é decisão dela, porque havia sessão de jogo viva.

#### D-17 — A crença do autoswitch é cega aos gestos dela

- `AutoSwitcher._current_profile` é escrito **num único lugar**: `profiles/autoswitch.py:551`,
  dentro do próprio `_activate`. **Nada** o sincroniza com `store.active_profile` (grep no `src/`
  inteiro confirma). O gate é `autoswitch.py:303-307`
  (`if stable and candidate and candidate != self._current_profile:`).
- **Prova no journal:** `02:24:42 profile_autoswitch from_=None to=sackboy_nativo` — com `vitoria`
  ativo **desde o boot, 23:40:18**. O autoswitch decide contra uma crença desatualizada.
- **Estado:** CURADO na árvore (seção 5-C).

#### D-18 — O ping-pong com a janela da Steam, dentro da partida

- **Mecanismo:** `navegacao.json` casa `window_class` `"steam"` e `"Steam"`, prioridade 50,
  `criteria`. A chave de seleção é `(not e_catch_all, priority)` (`manager.py:772-779`, `:786-787`)
  — **especificidade antes de prioridade**. Logo, na janela `steam`, `Navegação (True, 50)` vence
  `sackboy_nativo (False, 191)`. Na janela `steam_app_1599660`, só catch-all casa → veto R-21 →
  retém o corrente.
- **Sequência real (journal):**
  ```
  02:29:33.1  profile_activated  name=sackboy_nativo origin=manual        (ela escolhe, 4a vez)
  02:30:45.9  profile_activated  name=Navegação origin=autoswitch priority=50
  02:30:45.9  profile_autoswitch adiado=['suppression'] from_=sackboy_nativo to=Navegação wm_class=steam
  ```
  **O perfil dela foi reescrito 72 s depois de ela escolher**, e ao voltar ao jogo o veto retém
  `Navegação` — o jogo roda com o perfil do navegador.
- **Confirmação física:** `Navegação` pinta `(97,53,131)`; `sackboy_nativo` pinta `(80,60,220)`.
  ```
  02:46:43 / 02:46:46 / 02:50:52   lightbar_reassert_skip_cache rgb=(97, 53, 131)
  ```
  Às 02:50:52 ela já tinha clicado "Ativar sackboy_nativo" **quatro vezes** (02:48:56, 02:49:43,
  02:49:44, 02:50:19) e **o controle ainda estava roxo do Navegação**.
- **E o debounce de 12 s não a protege:** `_saida_para_catch_all` (`autoswitch.py:379-396`) exige
  `self._current_especifico`, gravado em `:554` a partir do perfil que entrou pelo autoswitch. Com
  os perfis dela catch-all, `_current_especifico = False` e **o lado lento nunca arma — toda
  transição custa 0,5 s (um tique)**. Isto não é a assimetria falhando; é consequência de o perfil
  ter perdido a regra.

#### D-19 — A armadilha de mão única da supressão de mouse e teclado

- `daemon/lifecycle.py:1564-1567` **LIGA** `suppress_desktop_emulation` **sem** o gate
  `_perfil_tem_opiniao`; só o ramo que **LIBERA** tem gate (`:1574-1580`, `IGNORADO_CATCH_ALL`,
  `motivo=catch_all_sem_opiniao`).
- **Estado medido no disco dela:** `sackboy_nativo` é catch-all, prioridade 191, com
  `suppress_desktop_emulation: true`, **e é o perfil ativo**. Resultado: um catch-all ligou a
  supressão no desktop e **nenhum outro catch-all consegue desligar**.
- Duas fontes já avisavam por escrito: `draft_config.py:704-712` e o veto nº 3 da
  `PERFIL-SALVA-TUDO-01`. **A escrita da janela produziu exatamente a configuração que dois
  documentos proibiram.**
- **Estado:** CURADO na árvore (seção 5-C).

#### D-20 — `apply_profile_rumble_policy` não tem as guardas que os irmãos têm

`lifecycle.py:2296-2412`; o ramo de reversão (`:2350-2366`) **não tem** guarda de catch-all nem de
janela de jogo, ao contrário de `mode` (`:1931-1946`) e `suppression` (`:1574-1587`). Evidência:
`profile_rumble_policy_reverted` no journal às **02:48:56, dentro da sessão de jogo**.
**Estado:** CURADO (seção 5-C).

#### D-21 — O filtro do log do autoswitch escondia metade

`autoswitch.py:565-569` filtra `estado.startswith("adiado")` → **`ignorado_*` e `falhou` nunca
apareciam**. O `adiado=['suppression']` de 02:30:45 estava escondendo o resto.
**Estado:** CURADO (seção 5-C).

#### D-22 — `_reapply_last_profile` monta o gerenciador sem três appliers

`lifecycle.py:964-967` monta o `ProfileManager` **sem** `mode_applier`, `rumble_policy_applier` nem
`speaker_applier` → **sair do Modo Nativo não restaura essas seções**. **Estado:** CURADO (seção 5-C).

#### D-23 — Lista completa das razões pelas quais uma seção NÃO entra

Levantada duas vezes, por dois agentes independentes, com resultado convergente. Dezessete
motivos, cada um com o log que emite:

| # | Seção | Motivo | Log | `relatorio` |
|---|---|---|---|---|
| 1 | trigger/led | categoria travada → `None` | `profile_apply_respeita_override_manual` (`manager.py:326-332`) | **não aparecia** |
| 2 | speaker | `audio` travado | `profile_speaker_ignorado_trava_manual` (`manager.py:621-626`) | `ignorado_trava_manual` |
| 3 | mouse | gesto manual < 30 s | `profile_mouse_skipped_manual_lock` (`lifecycle.py:1658-1666`) | `adiado_lock_manual` |
| 4 | suppression | gesto manual < 30 s | `profile_suppression_skipped_manual_lock` (`:1555-1563`) | `adiado_lock_manual` |
| 5 | suppression | reverter, perfil catch-all | `..._revert_skipped motivo=catch_all_sem_opiniao` (`:1574-1580`) | `ignorado_catch_all` |
| 6 | suppression | reverter, janela de jogo | `..._revert_skipped motivo=janela_de_jogo_em_foco` (`:1581-1587`) | `ignorado_janela_de_jogo` |
| 7 | mode | gesto manual < 30 s (**silencioso se `mode=None`**) | `profile_mode_skipped_manual_lock` + `profile_mode_deferred` (`:1892-1902`, `:2199`) | `adiado_lock_manual` |
| 8 | mode | `kind=None` + catch-all | `profile_mode_revert_skipped motivo=catch_all_sem_opiniao` (`:1931-1938`) | `ignorado_catch_all` |
| 9 | mode | `kind=None` + janela de jogo | `profile_mode_revert_skipped motivo=janela_de_jogo_em_foco` (`:1939-1946`) | `ignorado_janela_de_jogo` |
| 10 | rumble_policy | gesto manual < 30 s (**silencioso se `policy=None`**) | `profile_rumble_policy_skipped_manual_lock` (`:2339-2348`) | `adiado_lock_manual` |
| 11 | rumble_policy | política inválida | `profile_rumble_policy_invalida` (`:2368-2372`) | `falhou` |
| 12 | speaker | `volume=None` | `profile_speaker_sem_volume_recusado` (`:2493-2497`) | `falhou` |
| 13 | speaker | backend sem suporte / sem handle | `profile_speaker_backend_sem_suporte` / `_sem_controle` (`:2498`, `:2514`) | `ignorado_sem_controle` |
| 14 | qualquer | applier levantou exceção | `profile_<x>_apply_failed` (`manager.py:485,506,529,551`) | `falhou` |
| 15 | modo jogo padrão | sem autoridade de jogo | `modo_jogo_padrao_adiado estado=ignorado_sem_jogo motivo=sem_autoridade_de_jogo` (`:2046-2049`) | — |
| 16 | modo jogo padrão | gesto manual < 30 s | `... estado=adiado_lock_manual motivo=gesto_manual_recente` (`:2052-2055`) | — |
| 17 | modo jogo padrão | modo nativo manual | `... estado=ignorado_gesto_dela motivo=modo_nativo_manual` (`:2063-2069`) | — |

**Os casos 1 e 15-17 não entravam no `relatorio` de forma alguma.** O caso 1 foi curado (seção 5-C);
15-17 entram agora pelo autoswitch.

#### D-24 — A pendência de `mode` tem quatro formas de morrer

`ModoAdiado` (`lifecycle.py:232-305`), slot único **sempre sobrescrito, nunca enfileirado**
(`:421`, `:2188-2197`), drenado a ~1 Hz (`:3414-3420`, `_drenar_modo_pendente` `:2233-2294`):
1. espera `carimbo_manual + 30 s` (`:2195`, `:2252-2253`);
2. **descartada** se `_emu_manual_ts` mudou (`:2254-2261`) — **qualquer `profile.switch` manual no
   meio mata a pendência**;
3. **descartada** se `store.active_profile` mudou (`:2262-2271`) — trivial com autoswitch a 2 Hz;
4. **segurada indefinidamente** enquanto `display_authority == "game"` e a mudança for destrutiva
   (`:2272-2282`).

E `lifecycle.py:1911-1913`: **toda ativação com `origin != "game_signal"` zera `_modo_jogo_padrao`**,
de modo que o tique seguinte re-arma o ciclo do zero. Medido no journal:
```
02:44:31.7  modo_jogo_padrao_adiado  estado=ignorado_sem_jogo motivo=sem_autoridade_de_jogo
02:44:33.0  game_signal_transition   de=daemon -> game
02:44:33.2  profile_mode_aplicado    kind=gamepad origin=game_signal
02:45:43.5  modo_jogo_padrao_solto   de=steam_app_1599660 motivo=janela_fora_do_jogo
02:46:25.3  game_signal_transition   de=game -> daemon (histerese expirada)
```
**Liga vpad / solta vpad por foco de janela, dentro da partida.**

#### D-25 — Frequências reais (todas medidas no código)

| Constante | Valor | Onde |
|---|---|---|
| poll do autoswitch | **0,5 s (2 Hz)** | `profiles/autoswitch.py:41` |
| debounce para ENTRAR | **0,5 s** | `autoswitch.py:42` |
| debounce para SAIR rumo a catch-all | **12,0 s** | `autoswitch.py:58` |
| lock manual de perfil | **30,0 s** | `state_store.py:31` (`MANUAL_PROFILE_LOCK_SEC`) |
| lock de gesto de emulação (`_emu_manual_ts`) | **30,0 s** | `lifecycle.py:418`; lido em `:1892`, `:2052`, `:2339` |
| histerese do sinal de jogo | **30,0 s**, avaliada a cada **2 s** | `game_signal.py:62`; `lifecycle.py:3412` |
| dreno da pendência de `mode` | **1 Hz**, não antes de 30 s | `lifecycle.py:3414-3420`, `:2195` |
| `_reassert_rumble` | **200 ms** | `lifecycle.py:3475` |
| timeout do IPC da janela | **0,25 s** (era) | `app/ipc_bridge.py:104` |

### 1.4 Prioridade e seleção

#### D-26 — A escala satura no teto e o desempate vira acidente de `glob`

- `_prioridade_acima_dos_catch_all` = `max(0, min(200, max(prio dos catch-all) + 10))`
  (`profiles_actions.py:1620-1634`). **Com qualquer catch-all ≥ 190, todo perfil novo nasce
  exatamente em 200** e empata no teto. O desempate cai no incumbente (`manager.py:828-835`) ou,
  sem incumbente entre os empatados, em `empatados[0]` (`:829`) — **a ordem alfabética do nome do
  arquivo** (`loader.py:568` `sorted(glob("*.json"))`).
- **Journal:** `sackboy_nativo` e `vitoria` os dois em 200.
- **Piso do rodapé é um terceiro número:** `footer_actions.py:119` `_PISO_ACIMA_DOS_CATCH_ALL = 15`.

#### D-27 — Divergência de predicados de "isto é jogo"

O veto R-21 usa `_STEAM_APP_WM_CLASS_RE` com `re.IGNORECASE` (`manager.py:43`); já
`perfil_e_regra_de_jogo` usa `wm_class.startswith("steam_app_")` **case-sensitive**
(`schema.py:692`). Medido:
```
STEAM_APP_1599660   veto-vê-como-jogo=True   matches=True   regra_de_jogo=False
```
Uma `wm_class` com caixa diferente **é jogo para o veto e não é regra de jogo para o cadeado** —
exatamente o buraco que a docstring de `schema.py:694-698` diz existir para fechar (corrigiu só a
comparação da lista, não o prefixo).

#### D-28 — O disco dela hoje, e o que ele faz

| perfil | prioridade | match | de fábrica era |
|---|---|---|---|
| **sackboy_nativo** | **191** | **`any`** | 80 / `criteria: steam_app_1599660` |
| Pragmata | 5 | any | — |
| meu_perfil | 1 | any | — |
| fallback | 0 | any | — |
| vitoria | 0 | any | — |

Rodando a seleção **real** contra os quinze perfis dela:
```
steam_app_1599660  ->  coop_local(75, específico) VENCE sackboy_nativo(191, catch-all)
Alacritty / code   ->  sackboy_nativo(191) vence tudo -> gamepad+dualsense+suppress no DESKTOP
```
**O perfil do Sackboy perde dentro do Sackboy e ganha em todo o resto.** É o inverso do que ela
pediu, e é a frase *"está tudo quebrado"* traduzida para código. `FPS` também perdeu a seção `mode`
no save de 02:42.

E o achado que muda a escala do problema: **`sackboy_nativo` era o último perfil do disco capaz de
abrir a Porta 1 do cadeado** — por isso o automatismo passou de "morto no Pragmata" para "morto em tudo".

#### D-29 — Outras surpresas concretas, medidas

- **`coop_local` casa por título** (`.*(Sackboy|Overcooked|It Takes Two|…)`, sem `window_class`):
  uma **aba de navegador** chamada "Sackboy" casa `coop_local` (75) e vence `Navegação` (50). O
  próprio `lifecycle.py:3237-3241` registra o tradeoff.
- **"Recarregar" perde a seleção dela:** `on_profile_reload` (`profiles_actions.py:1130`) chama
  `_reload_profiles_store()` **sem** `select_name`; `_populate_profiles_store:1409-1411` seleciona
  a **primeira** linha e repovoa o editor.
- **O reapply pós-save compara nome cru:** `profiles_actions.py:1262-1265` usa
  `ativo_antes == profile.name` em vez de `mesmo_slug` — com "Navegação"/"Navegacao" o perfil salvo
  não é reaplicado e ela lê como "não salvou".
- **A coluna "Quando usar" reimplementa o desempate e discorda do daemon:** `vencedor_da_disputa`
  (`profiles_actions.py:220-237`) só considera `match.type == "any"` e ignora o veto R-21 e o
  primeiro termo da chave — **hoje discorda**, porque não sabe que `sackboy_nativo` é o vencedor
  real no desktop.
- **`_on_profile_switch_success` descarta a edição em curso:** `:1121` →
  `_sync_selection_with_active_profile` → `_populate_editor`. Só em runtime.

#### D-30 — A documentação de prioridade está errada em quatro pontos

- `docs/usage/creating-profiles.md:103` — *"perfil com maior `priority` vence em empate"*: **falso
  como enunciado geral**; especificidade vem antes (`manager.py:779`), o veto R-21 ignora prioridade,
  e o terceiro termo (incumbente / ordem alfabética) não está documentado em lugar nenhum.
- `docs/adr/005-profile-schema-v1.md:16` — mesma omissão; nunca anotada com R-01/R-21/EMPATE-01.
- `creating-profiles.md:36` — *"fallback é obrigatório"*: **não é**; e com o veto R-21 ele é inútil
  dentro de jogo.
- `creating-profiles.md:121` mostra `--priority 10`; o default real da CLI é **5**
  (`cli/cmd_profile.py:154`) e o do esquema é **0** (`schema.py:467`). **Três defaults diferentes.**
  `README.md`: zero menção a prioridade. Comentário obsoleto em `profiles_actions.py:197-204`.

### 1.5 Steam Input

#### D-31 — O guarda vai apagar a decisão dela sobre o Sackboy (PROVADO em dry-run)

- `localconfig.vdf` real dela tem **três** jogos com `UseSteamControllerConfig "2"`:
  linha 1236 appid 3357650 (Pragmata, **na allowlist**), **linha 1257 appid 1599660 (Sackboy, NÃO
  está)**, linha 1264 appid 2111190 (Mullet Mad Jack, na allowlist).
- `_transform_vdf` do `scripts/disable_steam_input.sh` rodado contra o arquivo real, **sem escrever**:
  ```
  1257: "UseSteamControllerConfig"  "2"    ->    "UseSteamControllerConfig"  "0"
  ```
- Regra em `disable_steam_input.sh:269-273` (per-app zerado exceto allowlist, lida em `:226`).
- **A bomba está armada:** `hefesto-steam-input-guard.timer` ativo, ciclo de 30 min. Journal:
  `02:13:13 resultado=aplicado`, `02:43:17 resultado=adiado-steam-aberta`,
  `03:13:25 resultado=adiado-steam-aberta`. **No instante em que ela fechar a Steam, o Sackboy é
  zerado — sem aviso, sem toast, sem nada na tela.**

#### D-32 — O pré-voo do `--apply` fecha a Steam à toa e mente "aplicado"

`disable_steam_input.sh:415-424` usa `needs_fix` (que casa a allowlist também) em vez de
`needs_real_fix` (`:339`, que já existe e serve só ao `--status`). Com **só** appids da allowlist
ligados, o `--apply` **fecha e reabre a Steam dela para não mudar nada** e emite
`resultado=aplicado`, que a janela traduz para *"a Steam não sequestra mais o seu controle"*
(`daemon_actions.py:319-320`). **Foi literalmente o que aconteceu às 02:13:13.** Correção de uma linha.

> **CURADO em 05/08/2026.** O pré-voo passou a usar `needs_real_fix` — nos **dois** modos que
> aplicam, não só no `--apply`: a medição refeita mostrou que a tag `resultado=aplicado` das
> 02:13:13 saiu do **`--apply-quiet`** (é o modo do `hefesto-steam-input-guard.timer`, e o único
> que emite `adiado-steam-aberta`, tag das 02:43 e 03:13). Corrigir só o `--apply` deixaria de pé
> a metade que chega à janela pelo botão "Aplicar correções". Bancada e mordida em
> `tests/unit/test_steam_input_honestidade.py::TestPreVooNaoFechaSteamAToa` (com a contraprova de
> que um appid FORA da allowlist ainda fecha a Steam e ainda é zerado).

#### D-33 — As três mensagens contam arquivos, não jogos

- `integrations/storm_doctor.py:151-155`: *"Steam Input LIGADO em 1 perfil(is) fora da allowlist —
  clique 'Aplicar correções' na aba Sistema para desligar"*. **"1 perfil(is)" conta arquivos `vdf`.**
- `app/actions/emulation_actions.py:1246-1248`: *"Ligado — conflita com o Hefesto"*.
- `daemon_actions.py:301-321`: *"Controle: a Steam não sequestra mais o seu controle."*

Nenhuma sabe **de qual jogo** fala; todas chamam a escolha dela de *conflito*; e mandam clicar num
botão que **apaga exatamente a escolha que ela tomou**. É a queixa dela, provada.

> **CURADO em 05/08/2026.** As três nomeiam o jogo por appid, e pelo NOME quando a Steam tem o
> `appmanifest_<appid>.acf` em disco — a tradução existia (`cli/cmd_steam.nome_do_appid`) mas
> morava atrás do `import typer`, inalcançável para o doctor e para a janela; mudou para
> `integrations/steam_launch_options` (`rotulo_do_jogo`, `lista_de_jogos`). Sem manifest, o appid
> **cru** é a resposta — nome inventado, nunca. A palavra "conflito" saiu das três, e a mensagem do
> doctor passou a apontar, para caso de JOGO, o botão que **preserva** a escolha dela ("Este jogo
> não funciona"); o `'Aplicar correções'` continua sendo o ponteiro do ajuste **global** da Steam,
> que não é escolha por jogo. Mordidas em `tests/unit/test_steam_input_d33_nomeia_o_jogo.py` e nos
> dois testes de fio em `tests/unit/test_steam_modo_simples.py`.
>
> Duas coisas que a cura teve de respeitar e que não estavam neste estudo: (1) o toast do "Deixar
> tudo pronto" não pode pronunciar o jargão *"Steam Input"* (FEAT-STEAM-SIMPLES-01), então a frase
> nova fala em *"o controle de X voltou a ser entregue pelo Hefesto"*; (2) o script não relata
> appid nenhum na saída — quem mede é a GUI, **antes** de rodar, porque depois o `vdf` já foi
> zerado. Nota datada do que caducou: o `assert "não sequestra mais" in msg` de
> `test_steam_modo_simples.py::test_aplicado_relata_o_que_mudou`.

#### D-34 — Não existe critério técnico por jogo, e a lista tem um escritor só

- Existe granularidade por appid, mas quem entra na lista é decidido só pelo botão "Este jogo não
  funciona" (`daemon_actions.py:1158`; toast em `:461`). **`grep` por
  `suporte nativo|entende DualSense|xinput_only|xbox_only|native_dualsense` em `src/` e `assets/`
  retorna zero.** O único lugar com esse conhecimento é prosa: `docs/usage/jogos-e-mascaras.md:61-67`.
- **Ligar o Steam Input pela janela da Steam — o gesto natural, e o que ela fez — não escreve nada
  na allowlist.** É o DUPLO-REGISTRO-01, aberto desde 26/07: dois cadastros do mesmo fato,
  divergindo em silêncio.
- Escritores: `add_appid_to_steam_input_allowlist` (`integrations/steam_launch_options.py:772`,
  chamador vivo `daemon_actions.py:1182`) e `remove_appid_from_steam_input_allowlist` (`:828`).
- **`remove_...` tem chamador só na CLI** (`cli/cmd_steam.py:206,215`). **Zero em `app/` ou `gui/`.**
  O tooltip do glade já foi tornado honesto (`gui/main.glade:2431-2443`), **mas o comentário desse
  mesmo bloco ficou velho** — afirma "nem na linha de comando", e o caminho de CLI existe hoje.

> **NOTA DATADA — 06/08/2026, 19:56, sobre a seção 1.5 inteira. O experimento
> rodou, e ele dá o critério técnico que o D-34 dizia não existir.** Nada acima
> é apagado: o D-31, o D-32 e o D-33 continuam valendo palavra por palavra, e o
> D-34 continua certo sobre o **código** (não há campo, não há constante, e o
> único escritor é o botão). O que ele não podia saber é qual seria o critério.
>
> **O critério, medido em 06/08/2026 (grau MEDIDO quanto ao comportamento):**
>
> - **A allowlist NÃO é "a lista dos jogos com DualSense nativo".** É **"a lista
>   dos jogos cujo DualSense passa pela Steam"**. O **Sackboy** (`1599660`) tem
>   suporte nativo, **não** está na lista, e funcionou completo — um controle,
>   botões de PlayStation, controle andando. O **Mullet Mad Jack** (`2111190`)
>   precisa da lista porque o pedido dele (`SetDualSenseTriggerEffect`) passa pela
>   **API da Steam**, e sem o Steam Input daquele jogo o pedido não tem por onde
>   chegar.
> - **Grau da atribuição:** *Steamworks contra HID direto* é **SUSPEITA COM
>   MECANISMO** — ninguém leu os símbolos dos dois binários. O que é **MEDIDO** é
>   o comportamento contrastado dos dois jogos, e a **ausência** da distinção no
>   repositório (`grep` por "HID direto" devolve zero em `.py`, `.md`, `.sh` e
>   `.txt`).
> - **E a doutrina que a casa escrevia pela metade:** *"o Hefesto sai da frente"*
>   descreve só a **ENTRADA**. Durante a exceção o Hefesto **mantém a saída
>   inteira** — no Mullet, os gatilhos dela seguraram e a cor dela ficou. **Fora**
>   da allowlist é que a saída dela perde: o jogo escreve no vpad, a réplica
>   chega ao físico e a camada GAME vence (`core/backend_pydualsense.py:1253-1259`).
>   No **rumble** a política é a inversa e a usuária vence (`gamepad.py:747-748`).
>
> **Consequência para o D-34, e é concreta:** o `steam_input_apps.txt` dela já
> tem **duas entradas com justificativas incompatíveis** — `2111190` por
> Steamworks e `3357650` por *"suporte nativo entregue PELA Steam"*, registrado
> em 26/07 depois de medir quatro joysticks para um controle. Uma entrou pelo
> critério certo, a outra pelo **duplicado**. E o cabeçalho do arquivo define a
> lista de um jeito só. **Nenhum agente reescreve esse arquivo:** ele é dela.
> Registro completo em
> [CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md).

### 1.6 Integridade dos dados dela

#### D-35 — Nenhum teste e nenhum script tocou os perfis. Foi a janela.

**Prova negativa (as duas janelas da suíte estão vazias):**
```
find ~/.config/hefesto-dualsense4unix -newermt "00:44:43" ! -newermt "00:48:07"  -> VAZIO
find ~/.config/hefesto-dualsense4unix -newermt "01:14:03" ! -newermt "01:16:50"  -> VAZIO
```
Os mtimes dos perfis alterados são **02:33:31, 02:42:39, 02:43:06, 02:43:19, 02:49:55, 02:51:09** —
todos ≥ 77 min depois da segunda janela.

**Por que a suíte não podia:** `tests/conftest.py:347-391` (autouse `_hefesto_fake_env`) isola
`XDG_CONFIG_HOME/DATA/CACHE/STATE`. Isso só funciona se `platformdirs` reler o env a cada acesso —
`utils/xdg_paths.py:12` constrói `_DIRS = PlatformDirs(...)` **no import**. **Medido: é lazy**
(platformdirs 4.11.0). Portanto `config_dir()` nunca resolve para o diretório real sob teste.

**Detalhe que confunde e quase virou alarme falso:** os `.lock` mudam de mtime a cada ~70 s
(`03:29:27 → 03:30:37 → 03:33:51`). Não é escrita: `loader.py:499-502` pega `FileLock` **para ler**;
é o daemon (PID 1670) recarregando.

#### D-36 — Nem validação semântica, nem backup, nem registro de gravação

- `profiles/loader.py:499-502` `_read_profile` faz só `Profile.model_validate(raw)` — sintaxe e tipo.
- `profiles/schema.py:467` `priority: int = 0`, **sem `ge`/`le`**: 191, 200, -5 e 10⁹ passam iguais.
- Catch-all com prioridade 191 e perfil de jogo sem `window_class` **passam calados**.
- **Backup automático não existia.** O `backup-20260726-233630/` interno que ela tem é **órfão**,
  manual, sem criador no repositório (`scripts/purge.sh:86` e `uninstall.sh:1262` criam um irmão
  *externo*). **Por sorte, é a única testemunha do estado pré-corrupção.**
- `doctor` (`cli/cmd_doctor.py`, `cli/app.py:82`) é infra pura — **não olha perfil nenhum**.
- **Zero registro no journal de gravação de perfil** — `grep -cE 'footer_|gui_'` = **0**; e o
  `stderr` da janela não chega ao journal (JANELA-FIEL-01 `:626-634`: *"zero linhas da janela nos
  últimos sete dias"*). **Foi essa lacuna que impediu decidir se o 191 veio de catraca ou de slider.**
- `save_profile` (`loader.py:621`, escrita em `:724-738`) é atômica (`mkstemp` + `os.replace`) —
  protege contra truncamento, **não** contra sobrescrita semanticamente errada.

#### D-37 — O `HOME` da suíte não é isolado

Isolado: XDG config/data/cache/state, `FAKE=1`, seed de presets, socket do broker. **Não isolado:
`HOME`** — zero `setenv("HOME")` no autouse. Consequências medidas:
- `integrations/storm_doctor.py:34-36` `_ALLOWLIST_PATH = Path.home() / ".config/hefesto-dualsense4unix/steam_input_apps.txt"`,
  **constante de módulo avaliada no import**, apontando para o arquivo REAL dela (721 bytes).
  Leitura, mas o resultado dos testes passa a depender do conteúdo dela; 3 arquivos tocam `storm_doctor`.
- `app/actions/emulation_actions.py:718` `_WP_DROPIN_DIR = Path.home() / ".config/wireplumber/wireplumber.conf.d"`
  — mesma forma, e aqui **é diretório de escrita em produção**.
- Outros: `core/system_check.py:37`, `gui/widgets/button_glyph.py:74`, `utils/i18n.py:61`,
  `integrations/steam_launch_options.py:295,752`, `integrations/proton_pin.py:159,176,189`,
  `app/actions/daemon_actions.py:752`, `emulation_actions.py:1193`.
- **uinput real:** 9 instanciações diretas de `UinputKeyboardDevice()` em 6 arquivos
  (`test_keyboard_emulator.py:34,71,231,240`, `test_keyboard_tokens.py:56,93`,
  `test_daemon_connect_grace.py:427,452`, `test_profiles_preset.py:406`) — para 17 dispositivos
  observados, logo ~8 nascem por fiação indireta do daemon. Isto responde parcialmente o item 1 da
  lista "ainda não medido" da `SUITE-QUE-SUJA-O-JORNAL-01`.
- 18 arquivos citam `systemctl`; 58 usam `subprocess` real. Só 4 arquivos protegem `HOME` por conta
  própria.

---

## 2. Defeitos com MECANISMO, mas SEM medição

Suspeita fundamentada: o caminho de código foi lido, mas ninguém provou o efeito. Para cada um, o
que falta medir.

| # | Suspeita | Mecanismo lido | O que falta para fechar |
|---|---|---|---|
| M-01 | **A rajada de cliques é consequência do toast de falha** | `profiles_actions.py:1124-1128` mostra "Falha (daemon offline?)"; o espaçamento de ~1 s bate com re-clique humano | **não há log do lado da janela que prove o gesto**. Falta instrumentar a janela (o `stderr` não chega ao journal) — declarado HIPÓTESE bem apoiada pelo próprio agente |
| M-02 | **Foi o "Salvar Perfil" do rodapé que apagou o `match` do `sackboy_nativo` entre 02:24 e 02:27** | `draft_config.py:578-581` é o único caminho que escreve `MatchAny()` por cima de perfil existente | **o journal não registrava gravações de perfil**. O instrumento foi criado nesta leva (`profile_salvo`, seção 5-D) e já capturou uma linha; falta reproduzir o gesto |
| M-03 | **Seis saves seguidos produzem um catch-all de prioridade 70, acima de todo preset de gênero (50-80)** | aritmética direta do medido (10 → 20 → 30) | é extrapolação, não observação. Declarada HIPÓTESE pelo agente |
| M-04 | **A exceção per-app de Steam Input pode ser decorativa** | o portão zero da `STEAM-INPUT-01`: *"não testei se `UseSteamControllerConfig="2"` per-app funciona com `SteamController_PSSupport="0"` global"* | **o experimento nunca foi feito**, e ele vem antes de escrever qualquer linha de Steam Input. Se a Steam moderna não honrar o per-app, **o botão "Este jogo não funciona" nunca funcionou de verdade** |
| M-05 | **Ler o `localconfig.vdf` em runtime com a Steam viva** (entrega 1 da DUPLO-REGISTRO-01) | a regra da casa é *"nunca escrever com a Steam viva"* (`:173`); ler é outra coisa | falta responder se é seguro. **A entrega 1 inteira depende disso** |
| M-06 | **O input duplicado sumiu com o remendo de 26/07** | `+ 3357650` no `steam_input_apps.txt` | não confirmado ao vivo — *"reiniciar o daemon no meio da partida contraria as regras da casa"* |
| M-07 | **`start_gamepad_emulation` devolve `True` mesmo com o gate recusando** → o relatório do `profile.switch` mente | `daemon/subsystems/gamepad.py:1433-1434` vs. `_recriacao_bloqueada_por_jogo` (`:1008-1039`) | lido no código (ESCOLHA-DELA-VENCE-01/D3), **sem medição ao vivo** |
| M-08 | **A máscara do perfil não sobrevive ao reboot** | `daemon/connection.py:220-224` roda o restore com `mode_applier=None`; quem manda é `gamepad_emulation.flag` | o roteiro obrigatório (`git log -S "mode_applier"`) **não foi executado**, e não dava para reiniciar o daemon na máquina dela |
| M-09 | **O daemon desiste do jogo antes do jogo acabar** | histerese de 30 s (`game_signal.py:62`), queda em `:157-180` | **o experimento de 90 s com jogo vivo e foco fora nunca foi feito** (SINAL-DE-JOGO-01/E1). E o verificador **derrubou** as seis transições apresentadas como prova (ver C-19) |
| M-10 | **`window_detect_reason` sai `null` no daemon vivo** | o motivo chega ao `WindowReaderDiag.last_reason`, o store sabe guardá-lo, mas a fiação em `daemon/subsystems/autoswitch.py::_build_diag_window_reader` ficou fora de escopo | declarado pela própria sprint (JANELA-CEGA-01 `:152-166`); **não medido no daemon vivo** |
| M-11 | **A paleta automática por slot (COR-03) mascara o automatismo morto** | P1 nasce azul, P2 vermelho; não há nada na tela dizendo *"nenhum perfil ativo; a cor que você vê é automática"* | nota de 03/08 da AUTOMATISMO-MORTO-01; **efeito sobre a percepção dela não medido** |
| M-12 | **A trava manual global congela os quatro controles** | `state_store.py:102` é `set[str]` único, sem chave por MAC; obedecido em `manager.py:342-346` | POSSE-POR-CONTROLE-01: os defeitos 1, 2 e 4 são **provados no código**; só o 3-bis foi medido ao vivo. **O efeito por controle não foi medido** |
| M-13 | **A E1 da POSSE quebra o restore por categoria que a TRAVA acabou de introduzir** | a cura de 05/08 lê `getattr(store, "manual_override_categories", ())` e restaura com `mark_manual_trigger_active(categoria)` **sem MAC** (`ipc_handlers.py:426`/`:451`, `hotkey.py:166`/`:186`); a união dos baldes resolve a **leitura**, não a **reescrita** | raciocínio de código, sem execução. **É o ponto de colisão concreto a vigiar** |
| M-14 | **`set_speaker_volume` assume zero quando não recebe volume** | *"o `pref = 0` transforma 'não me disseram' em 'me disseram zero'"*; há guarda em `ipc_handlers.py:2932` e nota em `lifecycle.py:2483-2498` | a raiz em `backend_pydualsense.py:2371` **merece leitura direta** — declarado parcial |
| M-15 | **Os botões de microfone dos controles 2, 3 e 4 nunca veem evento** | `core/backend_pydualsense.py:1920-1926` lê `micBtn` só do primário | lido no código; **sem medição ao vivo com quatro controles** |
| M-16 | **`profile.switch` com nome inexistente congela o autoswitch por 30 s** | o `except` (`ipc_handlers.py:439-446`) restaura a trava mas **não** o `_manual_profile_lock_until` anterior | borda introduzida pela cura da TRAVA; **benigna, não medida, e não documentada na sprint** |
| M-17 | **O tooltip do glade contradiz o preset embarcado** | `gui/main.glade:2861` lista o Sackboy como "funciona completo com DualSense (PS)", mas `sackboy_nativo.json` pede `xbox` e `profiles/loader.py:191` migrou `dualsense→xbox` de propósito | **não medido em jogo** qual dos dois está certo hoje |
| M-18 | **`on_emulation_open_toml` continua vivo depois de o botão sair** | registrado em `app/app.py:320`, implementado em `emulation_actions.py:449`, e o glade (`:2483-2489`) registra que o botão saiu | dívida residual das entregas 5 e 6 da BOTÃO-QUE-NÃO-MENTE-01; **sem efeito medido** |

> **NOTA DATADA — 06/08/2026, 19:56. O M-04 SAI DESTA TABELA: ele foi medido, e
> a suspeita está REFUTADA.** A linha fica onde está, porque decisão medida não
> se apaga e porque a suspeita era legítima quando foi escrita. O que caducou é o
> *"o experimento nunca foi feito"*: ele foi feito em 06/08/2026, das 19:34 às
> 19:56, com ela, um DualSense físico e três jogos abertos de verdade.
>
> **Veredito, grau MEDIDO:** `UseSteamControllerConfig "2"` por jogo **é honrado**
> com `SteamController_PSSupport "0"` global — o `Microsoft X-Box 360 pad 1`
> apareceu **só** no jogo da allowlist e **não existiu** no jogo fora dela. **A
> exceção per-app não é decorativa, e o botão "Este jogo não funciona" entrega o
> que promete.** Registro completo em
> [CONTROLE-SONY-MEDIDO-01](../sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
> seção *O RESULTADO*.
>
> **O M-06 não fecha junto**, e é bom não confundir: o experimento mediu o
> Pragmata em zero jogadas. O que ele mediu é o **Mullet Mad Jack** listando
> **um** controle na tela, sem input duplicado — o que é evidência a favor da
> mesma cura, num jogo diferente.

---

## 3. Premissas que CADUCARAM

Cada linha é uma refutação com medição. **Nada aqui deve ser reaberto sem nova medição.**

### 3.1 Sobre o autoswitch e o cadeado

| # | Premissa | Refutação |
|---|---|---|
| **C-01** | *"O cadeado `autoswitch_locked.flag` está ligado"* (AUTOMATISMO-MORTO-01 lado (a), 30/07; nota de 03/08 dizendo `autoswitch_locked: True` há seis dias) | **MEDIDO em 05/08: o arquivo NÃO EXISTE** em `~/.config/hefesto-dualsense4unix/` (só `gamepad_/keyboard_/mouse_emulation.flag`); `daemon.state_full` confirma `autoswitch_locked: False`. **O cadeado caiu. O autoswitch está VIVO** — e é por isso que a situação dos catch-all virou aguda |
| **C-02** | *"A prioridade é a causa de o perfil do jogo não entrar"* | **REFUTADO** em `AUTOMATISMO-MORTO-01:348-357` e reconfirmado no código: `_chave_de_selecao` devolve `(not e_catch_all, priority)` (`manager.py:772-779`) — **especificidade antes de prioridade** — e o veto R-21 **nem lê `priority`**. *"Subir `Pragmata2` de 5 para 200 não muda absolutamente nada dentro do jogo."* **Consequência para agora: quem for consertar vai olhar para o 191 e querer corrigir o número. O número é sintoma; o que quebrou o jogo foi `criteria → any`** |
| **C-03** | *"É o detector de janela"* | **REFUTADO** em 30/07 (`:302-329`): `window_detect_diag_seeded backend=xlib healthy=True` e 40 linhas com `wm_class=steam_app_*`. *"Não gaste a próxima leva no detector."* |
| **C-04** | *"É desligar o cadeado"* | **REFUTADO** (`:331-346`): soltaria `Navegação` por cima da configuração dela 18 vezes em 3 dias |
| **C-05** | *"É o modo jogo padrão"* | **REFUTADO** (`:359-366`): funciona; MODO-01/B3 entregue |
| **C-06** | *"O autoswitch trocou de perfil na madrugada de 26/07"* | **REFUTADO** (PERFIL-JOGO-01 `:88-109`): `git diff --stat 4dd4652 main` sobre `profiles/` = **vazio**; **um único** `profile_autoswitch` no journal (25/07 21:19:51); todas as demais janelas de jogo com `autoswitch_congelado_pelo_cadeado` e candidato vazio; nenhum `profile_activated`. *"O rollback não pode ser a cura de uma troca de perfil"* |
| **C-07** | *"'Perfil ativo: Nenhum' prova que nenhum perfil forneceu os LEDs"* | **REFUTADO** (EMPATE-01, confirmação de 27/07 21h45, `:61-73`). Armadilha de medição nomeada: **"quando a tela é suspeita, ela não pode ser a testemunha"** |
| **C-08** | *"A prioridade 5 foi escolha dela no slider"* | **REFUTADO** (PERFIL-SALVA-TUDO `:322-346`): `grep -rn 'priority: int = 5'` = **uma** ocorrência, `draft_config.py:399` — um default de assinatura |
| **C-09** | *"A cura de 28/07 (`8d7fd45`) resolve"* | **REFUTADO**: cobre **só** `match`/`priority` e **só** na aba Perfis (`profiles_actions.py:1637-1652`); `draft_config.py` não está entre os 12 arquivos do commit |
| **C-10** | *"É o autoswitch sobrescrevendo (29/07)"* | **REFUTADO**: cadeado ligado à época; journal com `autoswitch_congelado_pelo_cadeado`. Quem desfazia era **a ativação** lendo o arquivo empobrecido |
| **C-19** | *"As seis transições de journal provam que o sinal cai com jogo vivo"* (SINAL-DE-JOGO-01) | **O verificador derrubou** (`:163-205`): 29/07 16:56:49 e 17:53:48 → processo morto; 29/07 17:13:29, 20:15:35 e 30/07 02:30:00 → fechamento real, comportamento projetado; 28/07 23:17:49 → sem contexto. **E o episódio inverso** de 28/07 23:16:22-23:16:39: 16 s sem foco com jogo vivo e **o sinal não caiu** — a histerese funcionou |
| **C-30** | *"A evidência nº 2 (`profile_rule_match`) é um sinal útil"* | **Letra morta na máquina dela**: em 15 perfis, o único que o probe casa é `sackboy_nativo`, por uma `wm_class` que a evidência 1 já pegaria sozinha. E o paradoxo registrado: *"o mesmo `coop_local` que fura o cadeado por título é o perfil que nunca vira evidência de jogo por título"* |
| **C-31** | *"A evidência nº 3 (wrapper) está disponível"* | **Estruturalmente ausente**: ela joga com `VKD3D_CONFIG=no_upload_hvv %command%`, sem o wrapper; `last_run` e `last_exit` **não existem** em `~/.local/state/hefesto-dualsense4unix/launch_env/` |

### 3.2 Sobre o estado das entregas

| # | Premissa | Refutação |
|---|---|---|
| **C-11** | *"EMPATE-01: só a E2 falta"* (índice de 30/07) | **VERIFICADO ENTREGUE, todas as três**: E1 (log `profile_select_empate_resolvido`, `manager.py:836-845`), E2 (`profiles_actions.py:179-280`, `vencedor_da_disputa` com dois chamadores, commit `cd5eaf1` de 31/07 09:47), E3 (desempate por incumbente, `manager.py:828-835`). **O documento mente ao contrário — confiar no cabeçalho custaria retrabalho** |
| **C-12** | *"PERFIL-SALVA-TUDO-01: ABERTA, nenhuma linha de código escrita"* | **VERIFICADO: quatro de seis de pé.** E1a PAGA (`draft_config.py:562`), E2 PAGA (`priority: int = 5` não existe mais em `src/`), E3 PAGA (`emulation_actions.py:438` `with_suppress`; `home_actions.py:598` `with_mode`), E5 PAGA (campos mortos removidos). **E1b EM ABERTO — é o DEFEITO A.** E4 (mic) e E6 (painel) seguem abertas |
| **C-13** | *"STEAM-INPUT-01/E7: o timer do guarda está parado"* | **CADUCOU em 27/07** (`2026-07-27-INDICE-a-blindagem.md:146-150`): `hefesto-steam-input-guard.timer` **active**, disparou há menos de um minuto, ciclo de 30 min. Reconfirmado em 29/07 |
| **C-14** | *"STEAM-INPUT-01/E6: `steam_input_vpad_suspenso` é órfão"* | **DEIXOU DE SER**: consumidores fora do módulo em `daemon/lifecycle.py:1762-1765` e `ipc_handlers.py:1445`; superfície de tela em `emulation_actions.py:329` e `status_actions.py:175,242,248` |
| **C-15** | *"STEAM-INPUT-01/E3: não existe desfazer"* | **Parcialmente paga, no lugar errado**: `remove_appid_from_steam_input_allowlist` tem chamador — `cli/cmd_steam.py:206,215`, **terminal, não janela**. Zero em `app/` ou `gui/` |
| **C-23** | *"A janela é maquete / mockup puro"* | **REFUTADO** (BOTÃO-QUE-NÃO-MENTE-01 `:19-43`): 66 handlers no glade, 66 no dicionário de sinais, 66 com `def`, **0** com corpo vazio, **0** órfãos. *"Confuso demais"* **CONFIRMADO**: 145 controles acionáveis, 6 "Aplicar", 6 "Desligar", 2 "Salvar" com semânticas diferentes visíveis ao mesmo tempo |
| **C-32** | *"AUTO-01 está entregue"* / *"AUTO-01 está aberta"* | **Contradição de estado no acervo**: o índice da leva marca `ENTREGUE 8fe735d` (`2026-07-25-INDICE-leva-quatro-controles.md:99`), mas `PEDIDOS-DELA-01` de 03/08 ainda a trata como *"(25/07, ABERTA)"* e acrescenta um item novo **AUTO-01.2-b**. Entregue em parte, reaberta por pedido novo |

### 3.3 Sobre hipóteses de causa já derrubadas

| # | Premissa | Refutação |
|---|---|---|
| **C-16** | *"O guarda desligou o Steam Input do Pragmata no boot"* | **REFUTADA por journal** (DUPLO-REGISTRO-01 `:75-93`): o guarda **rodou e editou** às 22:48:05, **e o campo não mudou** (`app=3357650 valor=2` antes e depois). *"O guarda preservou a escolha dela."* Fica registrada *"porque era a explicação mais plausível e teria fechado o caso no lugar errado"* |
| **C-17** | *"`"dualsense" in saida.lower()` não casa o nome real do nó de áudio"* | **MEDIDA COMO FALSA em 03/08**: `alsa_input.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.iec958-stereo` contém "DualSense". *"A hipótese está refutada e não deve ser reaberta."* Fica dívida menor de robustez: o casador canônico da casa usa **três** marcadores (`app/mic_monitor.py:55-60`) |
| **C-18** | *"O `.deb` não embala `profiles_default`"* / *"morto no AppImage e no Flatpak"* | **REFUTADO** (`scripts/build_deb.sh:133`; `build_appimage_gui.sh:112-117`; `flatpak/br.andrefarias.Hefesto.yml:170-183`). *"O botão morre mesmo assim — mas por causa do resolvedor, não do pacote."* Só o **wheel puro** não embala |
| **C-20** | *"O campo `aplicado_em` diz onde a intenção pegou"* | **MEDIDO AO VIVO em 03/08**: `led.player_set` respondeu `{"status":"ok","aplicado_em":["143a9a0000ab"]}` e o **sysfs não mudou** (`player-3 = 1` antes e depois). *"O campo acrescentado justamente para o daemon parar de mentir ainda mente"* — informa onde foi **registrada**, não **onde pegou**. E a docstring de `gamepad.py:744-745` também: *"não é broadcast"* |
| **C-21** | *"O ciclo PS+D-pad limpa as categorias travadas e portanto aplica o volume do perfil que entra"* (justificativa da SOM-02/E4, `hotkey.py:132-135`) | **"Não aplicava."** Derrubado pela TRAVA-QUE-SOLTA-TARDE-01; catalogado pela `ENTREGA-QUE-NÃO-LIGOU-01` |
| **C-22** | *"`test_onda_u_trava_por_categoria.py` e `test_perfil_respeita_trava_manual.py` cobrem a ordem do clear"* | **REFUTADO**: o primeiro (`:144-155`) chama `clear_manual_trigger_active()` **à mão**, com o comentário `# o que profile.switch chama`, e **nunca chama `_handle_profile_switch`**; o segundo (`:122-132`) *"documenta a ordem certa que o produto não executava"*. **Ambos verdes com o produto quebrado** — mordida na metade errada da cadeia |
| **C-24** | *"Tirar a prioridade numérica da tela e substituí-la por um seletor"* | **DESCARTADO por decisão dela, 27/07** (PERFIL-NASCE-CERTO-01 `:133-141`): *"o lance da lista de perfis, depois que vc explicou entendi como usar e vi que funcionam bem, talvez só deixar intuitiva, não precisamos desativar ela."* Princípio final: **"o número não é o problema; o número sem consequência visível é"** |
| **C-25** | *"Os perfis viraram `match=any` com prioridades escaladas"* (a premissa do briefing) | **PARCIALMENTE REFUTADA** pelo agente de Integridade, com o `backup-20260726-233630/`: `pragmata.json` **já era `{"type":"any"}` em 26/07 e está inalterado**; `vitoria` teve a prioridade **reduzida** (100 → 0), **não escalada**. Ver a divergência DIV-1 |
| **C-26** | *"Um teste ou script corrompeu os dados dela"* | **REFUTADO** (D-35): as duas janelas da suíte estão vazias, e os mtimes são ≥ 77 min depois |
| **C-27** | *"O campo `Status:` dos documentos é fonte"* | **REFUTADO por contagem**: 40 dizem ABERTA e só 3 dizem ENTREGUE (`INDICE-as-tres-faixas:14-21`). *"Não confiar no campo `Status:` de nenhum documento citado"* |
| **C-28** | *"As âncoras de linha do `main.glade` são estáveis"* | **CADUCARAM** (JANELA-FIEL-01 `:63-68`): a LARGURA-01 cita `profiles_paned` em `:1481`; hoje é `:1527`; tudo depois de Rumble deslocou ~46 linhas |
| **C-29** | *"SINAL-DE-JOGO-01 é ALTA"* | O auditor abriu como ALTA; **o verificador independente reenquadrou para MÉDIA** — e a correção do próprio documento sobre o achado que o originou está registrada no cabeçalho |
| **C-33** | *"O canário de sistema de arquivos deve comparar `(mtime_ns, size)"* (proposta da LEVA 1) | **REFUTADO na prática pela LEVA 2**: a primeira versão acusou **15 arquivos na estreia**, todos `*.json.lock` — o daemon e a janela estão de pé e o `filelock` toca o lock a cada aquisição. *"Um portão assim seria desligado na primeira semana."* A foto passou a guardar `(mtime_ns, tamanho, sha256)` |

### 3.4 Correção honesta de escopo

*"Correção honesta ao enunciado da faixa: **não são todos catch-all**. São catch-all exatamente
cinco"* (AUTOMATISMO-MORTO-01 `:93-94`).

---

## 4. Divergências entre agentes

Esta seção é a mais importante do documento. **Onde dois relatórios discordam, nenhum deles é
autoridade sozinho.**

### DIV-1 — A ORIGEM DO 191 (e do 200, e do 22). Três explicações incompatíveis.

Esta é a divergência central da madrugada, e ela decide **qual cura importa**.

**Tese A — a catraca do rodapé** (relatórios *Botões da aba Perfis* e *Sprints mapeadas e integração*):
- aritmética: `191 = 1 + 19×10`, base `meu_perfil` = 1; `191 mod 10 == 1` fecha;
- `_FOLGA_ACIMA_DO_CATCH_ALL = 10` (`profiles_actions.py:82`) e `PRIORIDADE_MAXIMA = 200` (`:77`);
- reprodução de 5 cliques: 11, 21, 31, 41, 51;
- o "200" do briefing seria o vigésimo save, batendo no clamp.

**Tese B — o slider dela** (relatório *Integridade e corrupção*):
- `gui/main.glade:49-51` define `profile_priority_adj` com `lower=0, upper=200`; a tooltip (`:2017`)
  diz "(0-200)";
- **200 é o fim do curso; 191 e 22 são posições de arrasto**;
- *"191 não é corrupção — é o polegar dela parando ali"*;
- **e o `match=any` é ANTERIOR e deliberado**: o backup interno de 26/07 mostra `pragmata.json` já
  com `{"type":"any"}` e prioridade 5, **inalterado**; e `vitoria` foi de 100 para **0** — movimento
  **para baixo**, não escalada;
- `draft_config.py:555-568` tem comentário explícito dizendo que `MatchAny()` para nome novo é
  **deliberado** e casa com o contrato do diálogo do rodapé, que não tem campo de regra.

**Tese C — o cenário F (DEFEITO B)** (relatório *Prioridades de perfil*):
- o cenário "Novo perfil + nome de um perfil existente" reproduz o disco dela **exatamente**:
  `match=any, prio=191, suppress=True` — inclusive o `suppress=true`, que a catraca sozinha não
  explicaria bem;
- aponta para `on_profile_new` desligando as guardas, **não** para o rodapé.

**Onde os três concordam:** foi a **janela** que escreveu; não foi teste, script nem autoswitch.

**O que os três não tinham:** o instrumento que decide. **Não existia `profile_salvo` no journal.**
Ele foi criado nesta leva (seção 5-D) e **já capturou uma linha real**:

```
profile_salvo ... match_antes=criteria match_depois=any priority_antes=10 priority_depois=191
```

**Esta linha é compatível com um único save que salta de 10 para 191** — o que não é a catraca de
+10 nem só o slider. **A questão continua aberta**, e agora é decidível: basta ler o `.historico/`
e o `profile_salvo` do próximo gesto dela.

**Consequência prática, e ela é grande:** o `sackboy_nativo` mudou de `criteria` para `any` **no
meio da sessão de jogo** — o journal prova a transição (às 02:24:41 o cadeado cedeu a
`sackboy_nativo`, o que **exige** `not e_catch_all`; às 02:27:05 ele já aparece na lista de
catch-all). Qual gesto produziu isso continua indeterminado.

### DIV-2 — O `MatchAny()` do rodapé é defeito ou decisão?

- **Vários relatórios** (*Conflito de perfis*, *Prioridades*, *Botões e modelo de rascunho*) tratam
  `draft_config.py:578-581` como **o mecanismo que apaga a regra** e propõem ler o `match` do disco
  antes de gravar por cima.
- **O relatório de Integridade discorda explicitamente e marca isso como HIPÓTESE:** *"que o
  `MatchAny()` do rodapé seja **o** defeito a curar. É deliberado e resolveu um bug pior. O que os
  dados sustentam é mais modesto e mais útil — o rodapé cria catch-all **sem avisar**, e nada
  depois disso reclama. A cura pode ser só um aviso no diálogo."*
- **E o acervo dá razão à cautela:** o veto nº 2 da `PERFIL-SALVA-TUDO-01` diz, com todas as letras,
  **NÃO afrouxar `mesmo_perfil` a ponto de nome novo herdar a regra de origem no PRIMEIRO save** —
  reabre o R-11 (`draft_config.py:448-462`; "Salvar como MadJack" com o FPS ativo produzia o regex
  do FPS e prioridade 60).
- **Estado da resolução:** a LEVA 2 costurou o meio-termo — o funil **herda a prioridade** de quem
  já existe em disco, e o **`match` continua não herdado**. O agente do funil declarou isso como
  **defeito residual medido**, não como decisão fechada.

### DIV-3 — A rajada de `profile_activated`: timeout ou autoswitch?

- **Map GUI profile activation path** e **Conflito de perfis em jogo**: *"não há timer, poll ou
  reconstrução de lista que reenvie `profile.switch`"* — todos os relógios da janela foram
  verificados um a um (`status_actions.py:386-388`, `home_actions.py:896`, `tray.py:191`,
  `compact_window.py:132`, `triggers_actions.py:249`); as abas são instaladas **exatamente uma vez**
  (`app.py:1130-1138` vs. `:1220-1228`, ramos mutuamente exclusivos). A rajada é **re-clique humano**
  depois do toast de falha causado pelo timeout de 250 ms.
- **Botões da aba Perfis** atribui a mesma evidência a outro mecanismo: *"`profile.switch` arma um
  lock manual de 30 s; passados os 30 s o autoswitch reelege `sackboy_nativo` (191) e desfaz a
  escolha dela em silêncio. **Os cliques repetidos são a assinatura disso**"*.
- **Resolução:** não são excludentes — o espaçamento de ~1 s (02:40:22 / :23 / :24) casa com
  re-clique após toast; o espaçamento de dezenas de segundos (02:48:56 → 02:49:43 → 02:50:19) casa
  com a escolha sendo desfeita. **Mas a atribuição de cada rajada específica não foi fechada**, e o
  próprio relatório de Conflito classifica a primeira como **HIPÓTESE bem apoiada** por não haver
  log do lado da janela.

### DIV-4 — `healthy` → `seeing`: uma linha ou uma leva?

- **JANELA-CEGA-01** (`:146-148`): *"A leva seguinte é de uma linha: trocar `window_healthy` de
  `healthy` para `seeing` em `daemon/lifecycle.py:_gather_game_signal_inputs`."*
- **SINAL-DE-JOGO-01/E5** (`:423-464`) diz o contrário sobre o tamanho: **ordem obrigatória, E5
  depois de E3 e E4, num commit só, com ela olhando a lightbar** — porque a transição
  `daemon → unknown` dispara `replay_retained_game_outputs()` (`lifecycle.py:3224-3228`), que
  repinta a lightbar.
- **Concordam no risco, divergem no tamanho.** A leitura de que "é uma linha" é a arriscada.

### DIV-5 — O estado declarado de EMPATE-01 e PERFIL-SALVA-TUDO-01

- Os agentes de **leitura de sprint** reportam fielmente o `Status:` declarado (EMPATE-01 PARCIAL
  com E2 aberta; SALVA-TUDO "ABERTA, nenhuma linha de código escrita").
- O agente de **cruzamento com o código** verificou por grep que **as duas estão erradas** — a
  EMPATE-01 subestima o que foi feito, a SALVA-TUDO também.
- **Regra que sai daqui:** quando um relatório de leitura de sprint e um relatório de verificação de
  código discordarem sobre estado de entrega, **o de verificação vence** — desde que ele cite o grep.

### DIV-6 — `window_detect_reason` está fiado?

- **JANELA-CEGA-01** declara que a fiação em `daemon/subsystems/autoswitch.py::_build_diag_window_reader`
  **ficou fora do escopo**, e que enquanto não entrar `window_detect_reason` **sai `null`**.
- **AUTOMATISMO-MORTO-01/E0** diz que a linha da aba Sistema (`app/actions/daemon_actions.py:126-160`)
  *"já sabe dizer `window_detect_seeing` e `window_detect_reason`"*.
- **Não é contradição estrita** — a tela sabe **exibir**, o daemon não **preenche**. Mas lido
  isoladamente, o segundo dá a impressão de entrega completa. **Marcar.**

### DIV-7 — Qual é o número certo para "nascer acima dos catch-all"?

Três números convivem para o mesmo conceito:
- **15** — `JANELA-FIEL-01:647-649` e `AUTOMATISMO-MORTO-01` (*"prioridade vira
  `_prioridade_acima_dos_catch_all()`, hoje 15"*), e é o `_PISO_ACIMA_DOS_CATCH_ALL`
  (`footer_actions.py:119`);
- **`max(catch-all) + 10`** — o cálculo real de hoje (`profiles_actions.py:1620-1634`);
- **5 e 0** — os dois caminhos de "criar perfil", já registrados como divergentes por **ABAS-17**
  em 25/07 (*"os dois caminhos usam prioridades padrão diferentes para o mesmo conceito"*).

**Ninguém reconciliou os três.** E ABAS-16 registra oito donos do valor padrão de máscara — o mesmo
padrão de doença, noutro campo.

### DIV-8 — O que fazer com o autoswitch durante a partida

- **Conflito de perfis** propõe (b7): *"enquanto `display_authority == "game"`, o autoswitch **não
  troca de perfil**, ponto"*; e (b8): tirar `steam`/`Steam` de `navegacao.json`, ou ensinar
  `select_for_window_ex` que a `wm_class` `steam` **durante** autoridade de jogo é o *chrome* do
  jogo.
- **Botões da aba Perfis** recomenda como mitigação imediata **marcar o cadeado da aba Início**.
- **AUTOMATISMO-MORTO-01** veta **desligar** o cadeado (item 3), veta **afrouxar o veto R-21**
  (item 4) e veta **`perfil_e_regra_de_jogo` aceitar regex de título** (item 5).
- **Não há conflito direto** — ligar o cadeado não é desligá-lo, e a proposta (b7) age noutro eixo.
  **Mas (b8) encosta perigosamente no veto 5**, e (b7) é uma regra nova de autoridade que nenhuma
  sprint pediu. **Tensão a resolver com ela, não a decidir por conta própria.**

### DIV-9 — A ordem de execução da trava manual

- **Read Steam Input/override**: as três sprints são **ortogonais**; a ordem prescrita pelas próprias
  sprints é **ÁUDIO E1/E2 → POSSE E1**, na mesma leva (para uma migração só do campo); a TRAVA é
  independente e **já foi executada antes das duas**.
- **Sprints mapeadas**: prescreve **TRAVA primeiro (e o primeiro passo é commitá-la)** → ÁUDIO →
  POSSE.
- **Convergem no essencial** (POSSE por último, porque reescreve os dez callsites), **divergem no
  ponto de partida**. E ambas apontam o mesmo risco: **fazer a POSSE E1 sem reconciliar o restore
  por categoria de `ipc_handlers.py:451` e `hotkey.py:186` reintroduz a globalidade que a E1 existe
  para matar** (M-13).

### DIV-10 — Números de linha que não batem entre relatórios

A árvore foi escrita durante a madrugada por agentes irmãos. Exemplos concretos:

| símbolo | citado como | citado como | árvore de hoje |
|---|---|---|---|
| `with_profile_identity` | `draft_config.py:514` (sprint 29/07) | `:629` | `:629`, corpo `:636-660` |
| `mesmo_perfil` | `draft_config.py:463` (sprint) | — | `:562-564` |
| `_prioridade_acima_dos_catch_all` | `profiles_actions.py:1398-1412` (sprint 29/07) | `:1425-1439` (sprint 30/07) | `:1620-1634` |
| `PRIORIDADE_MAXIMA` | `:74` (sprint) | — | `:77` |
| `_FOLGA_ACIMA_DO_CATCH_ALL` | `:78` (sprint) | — | `:82` |
| `_chave_de_selecao` | `manager.py:632-640` (sprint) | `:772-779` | `:772-779` |
| `_melhor_candidato` | `manager.py:668-706` (comentário do código) | `:797-846` | `:797-846` |
| veto R-21 | `manager.py:620-628` | `:759-767` | `:759-767` |
| `_marcar_audio_manual` | `ipc_handlers.py:2960-2975` (sprint) | `:2974` | `:2974`, docstring `:2994-3007` |

**Regra prática ao usar este documento: só as verificações por grep desta madrugada valem contra a
árvore atual. Linhas vindas de sprints são de datas anteriores.**

### DIV-11 — Um desenho proposto e refutado na prática

O agente da LEVA 1 propôs o canário de sistema de arquivos comparando `(mtime_ns, size)`; o agente
da LEVA 2 implementou, **mediu 15 falsos positivos na estreia** (todos `.lock`, causados pelo daemon
e pela janela vivos), e trocou por `(mtime_ns, tamanho, sha256)`. **Não é discordância de fato — é
um desenho refutado por execução, e o registro fica.**

---

## 5. O que já foi CURADO na árvore vs. o que segue aberto

### 5.0 Estado do repositório

Branch `restauro/inicio-da-sessao`, `HEAD` = `5f1b588`. **Tudo abaixo está no índice (`git add`),
NADA está commitado.** 50 arquivos, +7137 / -233.

**Alerta operacional, repetido por dois relatórios:** *"enquanto ficar só no índice, qualquer
`git stash`/checkout a perde"*.

**Alerta operacional nº 2:** o daemon vivo (PID 1670, 04/08 23:39:46) **é anterior a tudo isto**.
Nenhuma cura do daemon está valendo na máquina dela. Reiniciar é **decisão dela** — havia sessão de
jogo viva.

### 5.1 CURADO — A. O funil de gravação de perfil (DEFEITO A)

**`src/hefesto_dualsense4unix/app/actions/profile_writer.py` (novo, 232 linhas)**
- `ProfileWriterMixin._gravar_perfil_async` (`:69`) — **o único ponto de gravação da janela**:
  constrói → `save_profile` (worker) → toast/log → `_reapontar_rascunho` → recarrega a lista →
  `launch_env.refresh` → gancho do chamador → assert de invariante.
- `_reapontar_rascunho` (`:159`) com **a linha que faltava**: `self.draft = draft.with_profile_identity(profile)`
  (`:185`), mais `_active_profile_name` e `_draft_baseline`.
- `_conferir_invariante_de_gravacao` (`:189`) — o assert barato.
- A invariante está escrita no topo do módulo, com a medição (10 → 20 → 30) e a linhagem ABAS-01:
  **"toda gravação de perfil feita pela janela termina com o rascunho apontando para o que ficou em disco."**

**`app/actions/footer_actions.py`**
- base virou `ProfileWriterMixin` (`:113`);
- `_prioridade_do_save` (`:334`) — **prioridade só é calculada para perfil que não existe em disco**;
  `:367` herda `existente.priority`;
- os três call sites convertidos: save (`:397`), import (`:505`), restore (`:585`). O restore agora
  cai em `from_profile(profile)` quando a releitura falha (antes devolvia `None` e deixava identidade
  nova com conteúdo velho).

**Portão — `tests/unit/test_gravacao_de_perfil_passa_pelo_funil.py` (novo, 11 testes)**
- `test_nenhuma_gravacao_de_perfil_fora_do_funil` varre `app/**/*.py` **por AST** atrás de
  `save_profile(` e reprova qualquer chamada fora da lista;
- `_AUTORIZADOS_A_GRAVAR` tem 2 entradas (o funil e `profiles_actions.py`, exceção datada), com dois
  testes companheiros travando a lista contra crescimento;
- **é isto que impede o quinto botão de repetir o erro** — quem o escrever não precisa saber que
  `with_profile_identity` existe; simplesmente não consegue gravar por fora.

**Mordidas verificadas:** só `with_profile_identity` arrancado → **7 vermelhos**; as duas curas
arrancadas → *"o segundo save subiu a prioridade para 20"* — a catraca medida, reproduzida.

**Resíduo declarado pelo próprio agente:** **o `match` ainda não é herdado do disco.** Salvar por
cima de um perfil que já existe **e é diferente do ativo** continua gravando `MatchAny()` — quem
gateia é `mesmo_perfil` no `to_profile`, e mexer ali brigaria com o R-11.

### 5.2 CURADO — B. As guardas da aba Perfis, os diálogos, o timeout, o refresh e o relatório

**DEFEITO B**
- `profiles_actions.py:1044,1072` — `_esquecer_a_fotografia_do_editor()` saiu do topo de
  `on_profile_new` e foi para **depois** de posicionar os widgets (a ordem que `_populate_editor`
  sempre teve). Antes, o nascimento levantava `_prioridade_tocada`/`_regra_tocada`;
- `profiles_actions.py:1814` — `_perfil_que_o_salvar_sobrescreve(name)`, busca **por slug**;
- `profiles_actions.py:2118-2140` — `_build_profile_from_editor` **relê a fotografia do disco quando
  o alvo já existe**, com nota datada dizendo o que caducou na SALVAR-NAO-REBAIXA-01.

**Os dois avisos de rebaixamento**
- `app/gui_dialogs.py:152` — `confirm_downgrade_priority(parent, name, de, para)`, novo;
- `gui_dialogs.py:105` — `confirm_downgrade_match_to_any` ganhou `regra_atual`;
- `profiles_actions.py:1379-1417` — a guarda do match virou `not isinstance(original.match, MatchAny)`
  (**cobre `MatchManual` e o `criteria` vazio, que eram o furo**); regra pura testável
  `queda_de_prioridade_pede_aviso` + `QUEDA_DE_PRIORIDADE_QUE_PEDE_AVISO = 10`.

**O timeout**
- `app/ipc_bridge.py:34` — `PROFILE_SWITCH_TIMEOUT_S = 3.0`, fonte única; `profile_switch()` (`:283`)
  passou a usá-lo — **isso corrigiu também a CLI e o Salvar da aba Perfis**, que liam `False` de uma
  troca que tinha acontecido;
- `profiles_actions.py:1220` — `on_profile_activate` usa a constante;
- `packaging/cosmic-applet/src/ipc.rs:40` — **`SWITCH_IPC_TIMEOUT` (3 s) como constante própria**,
  `switch_profile` (`:392`) usa `call_raw_with_timeout`. **O `IPC_TIMEOUT` de leitura NÃO foi
  esticado de propósito** — ele cobre todo refresh do painel e penduraria 3 s num daemon morto.

**Ativar refaz as abas**
- `profiles_actions.py:1247,1252,1281` — `_refazer_as_abas_apos_ativar`, que recarrega via
  `_bootstrap_draft_async` (fallback `_refresh_all_tabs`). **Com edição pendente, PERGUNTA**
  (`gui_dialogs.confirm_discard_pending_edits`, default = MANTER) em vez de ignorar em silêncio.

**A janela lê o relatório**
- `profiles_actions.py:297-388` — `relato_da_ativacao` traduz `secoes` para `applied`/`failed`, e
  `mensagem_de_ativacao` **delega o texto a `footer_actions._mensagem_de_aplicacao`** — vocabulário
  reusado, não reescrito (a regra RADAR-01/E4 de não criar uma quarta frase de estado).

**Testes novos:** `tests/unit/test_salvar_nao_rebaixa_02_o_novo_perfil_desligava_as_guardas.py`,
`tests/unit/test_ativar_nao_mente_01_o_botao_que_parecia_falhar.py`. Nove mordidas verificadas uma a
uma. Portões: 1004 passed no recorte, `ruff`/`mypy` OK, `cargo test ipc::` 16 passed (4 novos).

### 5.3 CURADO — C. O daemon: crença, supressão, rumble, relatório, log, appliers

- **Crença do autoswitch** (`profiles/autoswitch.py:200` `_store_de_estado()`, `:215`
  `_perfil_corrente()`): adota `store.active_profile`, chamado no topo de `_tick` (`:274`) e de
  `_activate` (`:574`). **Zero I/O** — a primeira versão relia o disco via `manager.get()` e **o
  CANÁRIO-FS-01 flagrou escrita de `.lock` no diretório de perfis REAL dela**; trocado por palpite
  conservador com correção de graça em `_tick:315`.
  - Colateral declarado na docstring: o autoswitch deixa de "entrar" no perfil que o boot restaurou —
    o que **respeita** o `BUG-BOOT-RESTORE-FLIPS-EMULATION-01`.
- **Simetria da supressão** (`lifecycle.py:1621`): gate `catch_all_sem_opiniao` no ramo que **LIGA**,
  via `_perfil_e_catch_all` (`:1783`), de evidência **positiva** (irmão de `_perfil_tem_opiniao`; a
  diferença é a resposta na dúvida, documentada).
- **Guardas da política de rumble** (`lifecycle.py:2464-2493`): `catch_all_sem_opiniao` +
  `janela_de_jogo_em_foco`; exigiu `profile=` na assinatura (`:2403`) e no callsite (`manager.py:582`).
- **Relatório na origem** (`manager.py:360`): `trigger`/`led` → `ignorado_trava_manual` (constante
  `IGNORADO_TRAVA_MANUAL` + `_CATEGORIAS_SILENCIADAS_NO_APPLY`, **só o que o `apply` de fato
  silencia**). O **modo jogo padrão** entra como seção própria pelo autoswitch (`autoswitch.py:472/671`).
- **Log completo** (`autoswitch.py:683`): campo `secoes=["secao=estado", …]` com o relatório inteiro;
  `adiado=` fica onde estava (é o campo que a leitura de journal já procura).
- **Appliers ao sair do Nativo** (`lifecycle.py:964-984`): `rumble_policy_applier`, `speaker_applier`
  e `mode_applier` **embrulhado** por `_mode_applier_ao_sair_do_nativo` (`:990`), que barra só
  `kind="native"` — a decisão da FEAT-PROFILE-MODE-01 continua de pé, sem o preço colateral.

**Teste:** `tests/unit/test_perfil_reescrito_na_partida_01.py`, 18 casos, bancada hermética; cada
cura arrancada isoladamente e devolvida. Os casos que passam nos dois estados estão **declarados
como guardas** na docstring — honestidade sobre o que não morde.

**Nota do agente para a GUI:** `resposta["secoes"]` pode trazer `trigger`/`led` = `ignorado_trava_manual`;
na rota manual raramente aparecem (a TRAVA limpa antes), então materializam sobretudo em ativações
do autoswitch e no restore de boot. `modo_jogo_padrao` só existe no relatório do autoswitch.

### 5.4 CURADO — D. Integridade: histórico, journal, verificador, canário

**Backup versionado** — `profiles/loader.py`
- `:635` `HISTORICO_DIR_NAME = ".historico"`, `:639` `HISTORICO_MAX_VERSOES = 10`;
- `:642` `historico_dir()`, `:662` `listar_historico()`, `:692` `_podar_historico()`, `:703`
  `_arquivar_versao()` (best-effort: falha loga `profile_backup_failed` e **não impede o save**);
- `:787` `save_profile(profile, *, origem=None)` — dentro do `FileLock` que já existia, lê os bytes
  atuais **uma vez** (servem ao backup e ao "antes" do journal), arquiva, e só então `os.replace`;
- `:890` `restaurar_do_historico()` — valida contra o esquema, escreve os **bytes originais** e
  arquiva a versão atual antes de pisar;
- `:948` `delete_profile` também arquiva.
- **O `.historico/` é invisível às varreduras** — todas usam `glob("*.json")` não recursivo ou
  `find -maxdepth 1` (conferido em loader, `doctor.sh:1479`, `_perfis_inalcancaveis`).
- CLI: `cli/cmd_profile.py:233` `profile historico <nome>`, `:267` `profile restore <nome> [--em <carimbo>]`.

**Journal de toda gravação** — `loader.py:855` `_registrar_gravacao` emite **`profile_salvo`** com
`nome`, `arquivo`, `criado`, `match_antes`/`match_depois`, `priority_antes`/`priority_depois`,
`origem`, `pid`, `backup`. Também `profile_apagado` e `profile_restaurado`. **Nunca levanta.**
Linha real capturada: `match_antes=criteria match_depois=any priority_antes=10 priority_depois=191`
— **exatamente a transição que não dava para provar** (ver DIV-1).

**Verificador semântico** — `profiles/sanidade.py` (novo, 393 linhas), 5 regras em `REGRAS:336`:
`catch_all_vence_especifico` (erro), `prioridade_fora_da_faixa` 0-200 (erro),
`catch_all_com_cara_de_jogo` (aviso), `prioridades_empatadas` (aviso), `catch_all_demais` (aviso).
Todo `Achado` carrega **`cura`** e sai como `mensagem — Cura: ...`.
- **Dispensa nomeada:** `CATCH_ALL_LEGITIMOS = {"fallback"}` (`:48`) vale **enquanto ele está no
  piso** (`_tem_dispensa:128`) — um "fallback" que sobe a 100 volta a ser acusado, que é **a forma
  exata da corrupção**.
- Duas decisões contra fadiga de alarme, ambas com teste: o sinal de *nome* só dispara acima da
  prioridade 0; o sinal *declarado* (modo gamepad / supressão) dispara em qualquer prioridade.
- Exposto em `cli/cmd_doctor.py:83`/`:102` como **`doctor --perfis`** (exit 1 com achado grave) e no
  `doctor` completo. Exigiu **uma linha em `cli/app.py:90-99`**.

**Portão de hermeticidade** — `tests/conftest.py:333-510` (CANÁRIO-FS-01): `pytest_sessionstart`
fotografa `~/.config/hefesto-dualsense4unix`, `~/.config/wireplumber` e
`~/.local/share/hefesto-dualsense4unix`; `pytest_sessionfinish` refaz e **reprova a sessão**
(`session.exitstatus = 1`) listando `CRIADO/APAGADO/MUDADO`. Foto com **`(mtime_ns, tamanho, sha256)`**
(ver DIV-11). Escotilha `HEFESTO_SEM_CANARIO_FS=1`; selo `_CANARIO_ARMADO`. Custo: 93 arquivos, 356 KB.

**Resposta direta à pergunta dela:** com o canário armado, **a suíte inteira (6968 passed, 1 skipped)
terminou sem um único delta** nos três diretórios. **Hoje nenhum teste escreve no `~/.config` dela.**

**Testes novos:** `test_profile_historico.py` (16), `test_profiles_sanidade.py` (30),
`test_conftest_canario_fs.py` (9), `test_cli_profile_historico.py` (9). Onze mordidas verificadas.

### 5.5 CURADO — E. TRAVA-QUE-SOLTA-TARDE-01

- Em **ambos** os caminhos, `clear_manual_trigger_active()` + `mark_manual_profile_lock(now + MANUAL_PROFILE_LOCK_SEC)`
  passaram para **antes** do `manager.activate(...)`: `ipc_handlers.py:426` (`travadas_antes`),
  `:430` (clear), `:434` (lock), `:451` (restore); `hotkey.py:166,168,169,186,187`.
- Três decisões registradas: **o lock sobe junto com o clear** (não pode existir janela sem trava e
  sem lock — seria trocar um defeito por outro); **restore no `except`** (*"ativação que falhou não é
  gesto cumprido"*); **`getattr` na leitura** (dublês e stores parciais continuam funcionando).
- `tests/unit/test_trava_que_solta_tarde_01.py` — 6 casos, bancada hermética. **Com a cura arrancada,
  4 dos 6 reprovam.** Honestidade registrada: `test_falha_na_ativacao_devolve_a_trava` passa nos dois
  estados — protege a borda que a **cura** introduziu, não o defeito original.
- Sprint em `docs/process/sprints/2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-...md` (nova, no índice).
- **Verificação independente:** um agente auditou a subida do `mark_manual_profile_lock` e concluiu
  **NÃO há regressão, confiança alta** — os dois "locks de 30 s" desta casa têm o mesmo nome de
  constante e **estados completamente separados**. `mark_manual_profile_lock` escreve só
  `_manual_profile_lock_until` (`state_store.py:385-395`), cujo único leitor
  (`manual_profile_lock_active`, `:397-405`) tem **exatamente dois chamadores, ambos no `AutoSwitcher`**
  (`autoswitch.py:468` e `:522`) — **nenhum no caminho de `ProfileManager.activate`**. Prova empírica:
  lock armado antes e depois produz `OutputSpec` idêntico e `relatorio` idêntico.

### 5.6 Também no índice, fora do tema de perfis

Leva anterior (Bluetooth / rádio aberto), **não atribuída a nenhum relatório desta madrugada**:
`assets/bluetooth/*`, `scripts/bt_bonds_restore.sh`, `scripts/bt_crash_capture.sh`,
`docs/process/POLITICA-core-nunca-sai-da-maquina.md`, `docs/.../RADIO-ABERTO-01`,
`docs/.../ENTREGA-QUE-NAO-LIGOU-01`, `docs/.../INDICE-o-bluetooth-de-primeira-classe`,
`docs/protocol/dualsense-referencia-canonica.md`, `tests/unit/test_radio_aberto_*.py`,
`tests/unit/test_bt_resilience_assets.py`. Mais `integrations/storm_doctor.py` e
`app/actions/emulation_actions.py`, que já apareciam modificados **antes** desta leva.

### 5.7 O que segue ABERTO

**Bloqueantes de processo**

| # | Pendência | Por quê |
|---|---|---|
| 1 | **Commitar** | tudo está só no índice; um `git stash`/checkout perde a leva inteira |
| 2 | **Reiniciar o daemon dela** | PID 1670 é de 04/08 23:39:46; nenhuma cura do daemon vale hoje. **Decisão dela** — havia sessão de jogo |
| 3 | **Decidir com ela o destino de `sackboy_nativo.json`** | é o perfil **ATIVO**, catch-all/191/`suppress=true`. **Não escrever nos `.json` dela sem autorização explícita, inclusive "só para normalizar"** — veto repetido em `PERFIL-SALVA-TUDO-01` (1), `EMPATE-01` (`l.142-147`), `PERFIL-NASCE-CERTO-01` (E4), `PERFIL-JOGO-01` (E6), `AUTOMATISMO-MORTO-01` (item 7) |
| 4 | **Nota datada de que o cadeado caiu** | a regra da casa é nota datada, não apagamento (C-01) |
| 5 | **Índice novo para a faixa de perfis** | órfã desde 30/07: menções a `PERFIL-SALVA-TUDO\|AUTOMATISMO-MORTO\|PERFIL-NASCE-CERTO\|EMPATE-01\|ABAS-01\|PERFIL-JOGO-01` caem de **15** (índice de 30/07) para **4** (31/07) e **0** (01/08, 03/08 e ONDAS). **É a explicação estrutural de por que meias-entregas passaram: ninguém estava olhando esta faixa** |
| 6 | **Notas datadas de caducidade** nos documentos | EMPATE-01 (E1/E2/E3 entregues), PERFIL-SALVA-TUDO-01 (quatro de seis), MODO-01 (B2/B3), AUTOMATISMO-MORTO-01 (cadeado), e o comentário de `main.glade:2436-2438` (o desfazer existe na CLI hoje) |

**Defeitos abertos, por área**

*Escrita de perfil*
- **o `match` não é herdado do disco** no funil (resíduo declarado);
- **importar sem guarda de slug** (I-1) e **sem recarregar abas** (I-8);
- **texto do aviso de divergência** (`app/app.py:864-869`);
- `on_profile_reload` sem `select_name`; reapply pós-save por nome cru; `vencedor_da_disputa`
  discordando do daemon;
- `profiles_actions.py` ainda grava fora do funil (na lista de autorizados, com razão escrita e
  trava contra crescimento).

*Trava manual e posse*
- **`clear_manual_trigger_active("audio")` não existe** em `src/` nem em `tests/` — ÁUDIO-QUE-TRANCA-01/E1;
- **`_marcar_audio_manual` ainda ARMA no `release`** (`ipc_handlers.py:2974`, docstring `:2994-3007`
  ainda diz *"a devolução da posse também arma"*);
- **`manual_trigger_active` continua booleano de tudo-ou-nada** (`state_store.py:425-428`;
  `autoswitch.py:466` e `:505` leem o booleano) — ÁUDIO/E2;
- **`manual_override_categories` continua `set[str]` global** (`state_store.py:102`) — POSSE/E1, com
  o ponto de colisão M-13;
- **não é exportado por `daemon.state_full`** e **não há afordância na tela** dizendo "esta seção
  está travada";
- `mode`, `mouse`, `rumble`, `key_bindings` e `speaker` continuam **globais no perfil**
  (`schema.py:468-500`); só `leds` e `triggers` têm eixo por controle.

*Steam Input*
- **o portão zero nunca rodado** (M-04) — vem antes de qualquer linha;
- o guarda vai zerar o Sackboy (D-31); pré-voo `needs_fix` → `needs_real_fix` (D-32); mensagem que
  conta arquivos (D-33); `remove_appid_...` sem superfície de janela (D-34);
- DUPLO-REGISTRO-01 entrega 1 (a Steam como fonte da verdade) e entrega 4 (grab `pending` silencioso).

*Seleção e prioridade*
- divergência de caixa `steam_app_` entre veto e `perfil_e_regra_de_jogo` (D-27);
- a escala saturando no teto (D-26) e os três números para o mesmo conceito (DIV-7);
- **`AUTOMATISMO-MORTO-01/E2 — "usar este perfil sempre neste jogo"**, o um-clique que fecharia a
  raiz das três queixas dela. **Não pode vir antes** das curas de escrita, senão o perfil promovido
  volta a catch-all no save seguinte;
- `PERFIL-NASCE-CERTO-01/E4` — parcialmente pago pelo `sanidade.py`, mas **sem detecção na aba
  Perfis nem "na subida e ao salvar"**, e **sem o botão que resolve**;
- `ESCOLHA-DELA-VENCE-01` E2 (reboot), E3 (recusa com jogo aberto que reporta sucesso), E5
  (`empatados[0]`, **aberta por decisão declarada** — `manager.py:820-824`: *"mudaria comportamento
  já validado sem que ninguém tenha pedido"*);
- `APLICAR-VERDADE-01/E2` — `ipc_bridge.apply_draft()` ainda estreita a verdade para `bool`;
- `PERFIL-SALVA-TUDO-01` E4 (destino de `Profile.mic`) e E6 (painel de leitura na aba Perfis).

*Hermeticidade*
- **`HOME` continua não isolado**; `_ALLOWLIST_PATH` (`storm_doctor.py:34`) e `_WP_DROPIN_DIR`
  (`emulation_actions.py:718`) continuam constantes de módulo avaliadas no import — **não foram
  movidas de propósito**, por serem arquivos de agentes irmãos e porque
  `tests/unit/test_steam_input_ponteiros.py:193` monkeypatcha uma delas pelo nome.

*Documentação*
- `creating-profiles.md:103`, `:36`, `:121`; `adr/005-profile-schema-v1.md:16`; README; comentário
  obsoleto em `profiles_actions.py:197-204`.

### 5.8 O que NÃO deve ser tocado

Consolidado das quatro listas de veto, cada item pago com defeito real:

1. **Os arquivos de perfil dela, sem a mão dela** — inclusive `sackboy_nativo.json`, inclusive "só
   para normalizar", inclusive dentro de script de instalação. *"Migração silenciosa de perfil é a
   classe de defeito que causou o rollback de 26/07."*
2. **O veto R-21** (`manager.py:759-767`) — nem revogar, nem afrouxar. Sem ele volta o ping-pong de
   18-28 s.
3. **`perfil_e_regra_de_jogo` aceitando regex de título** — o segundo consumidor é o furo da trava
   manual em `_activate`.
4. **O debounce assimétrico 0,5 s / 12 s** (`autoswitch.py:41-58`) — com 0,5 s dos dois lados o
   journal mostrava troca a cada 18-28 s no meio do jogo. **A observação de que o lado lento nunca
   arma hoje não é a assimetria falhando** — é consequência de o perfil ter virado catch-all, e some
   com a cura da escrita.
5. **`apply_output_defaults` ignorando o seletor** (`manager.py:248-255`) — broadcast real de
   propósito, e a POSSE-POR-CONTROLE-01 o veta por escrito.
6. **A camada do co-op fora de `_desired_by_uniq`** (R-13, `backend_pydualsense.py:335-341`) e **o
   rumble fora de `_desired`**.
7. **O gate R-02 no ramo de LIBERAR** de `apply_profile_suppression` — o buraco era o ramo de LIGAR,
   e foi esse que se corrigiu.
8. **`vencedor = empatados[0]`** (`manager.py:829`) — aberto por decisão declarada.
9. **`window_detect_healthy` decaindo** — a JANELA-CEGA-01 mede o custo: vaivém na cor do controle dela.
10. **A ordem `clear` → `activate`** — acabou de ser corrigida; reverter reabre a TRAVA-QUE-SOLTA-TARDE-01.
11. **NÃO dar TTL à trava manual** como atalho para o eixo por controle — *"o tempo não é o eixo
    errado por acaso: a trava existe para sobreviver ao autoswitch, que dispara a cada troca de janela."*
12. **Não tirar `"audio"` da lista de categorias** como cura do defeito 1 da ÁUDIO — a justificativa
    de `c10adaf` está certa; falta o clear e a granularidade.
13. **`_esquecer_a_fotografia_do_editor` não deve simplesmente sumir** — ela existe porque perfil
    novo não tem valor de disco a preservar. A cura do DEFEITO B é de **escopo**, não de remoção.
14. **O `MatchAny()` do PRIMEIRO save com nome novo** (R-11) — o defeito é o segundo save.
15. **Não marcar nada como entregue de novo sem chamador em produção.** É a regra que a
    `ENTREGA-QUE-NÃO-LIGOU-01` existe para instituir, e esta madrugada achou **três casos novos**
    dela. Nota de desenho registrada: **um portão de "zero chamadores" não teria pego o DEFEITO A**,
    porque `with_profile_identity` **tem** chamador e ainda assim estava meio-ligado. O aceite do
    portão precisa incluí-lo.

---

## Nota final de honestidade

Registrada pelos próprios agentes, e vale para este documento:

- **Ninguém olhou a tela.** Nenhuma afirmação aqui sobre aparência. As entregas de interface **não
  fecham sem o olho dela** (PROVA-DE-TELA-01: foto antes e depois, e a palavra final é dela).
- **A suíte completa e os portões foram rodados** pelos agentes da LEVA 2 (6968 e 6979 verdes em
  execuções distintas, `ruff` e `mypy` limpos), **mas em árvore viva, com agentes irmãos escrevendo
  em paralelo** — houve vermelhos transitórios que sumiram sozinhos. **Rodar tudo de novo, com
  `git add -A` antes, é obrigatório.**
- **O "200" do briefing não está no disco hoje** — só o 191. Não se sabe se foi corrigido ou se
  estava noutro lugar. **Vale confirmar com ela antes de qualquer conta.**
- **A origem do 191 continua indeterminada** (DIV-1). O instrumento que decide já existe; falta o
  próximo gesto dela.agentId: a06023383079193b5 (use SendMessage with to: 'a06023383079193b5', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 273641
tool_uses: 19
duration_ms: 819240</usage>
