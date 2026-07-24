# Sprint: GUI × perfis × config por-controle × numeração de jogador

**Status**: plano FECHADO (23/07 noite) — 65 achados confirmados, agrupados em
**24 causas-raiz**. Execução iniciada; ver "Progresso" abaixo.
**Origem**: pedido da mantenedora com os 4 controles ligados — *"faça uma
auditoria completa na interação entre as abas, veja a questão dos perfis
pré-setados, e nas configs que o user faz e que parecem não impactar controle a
controle. Procure por bugs."*

## Como este plano foi produzido

Duas ondas de agentes, ambas com verificação adversarial (o agente que acha NÃO
é o que julga):

| | achados | método de julgamento | confirmados |
|---|---|---|---|
| 1ª onda | 100 brutos (14 dimensões em paralelo) | 3 lentes por achado (refutação / reprodução / impacto), maioria decide | 10 |
| 2ª onda | 85 pendentes da 1ª (cancelados por limite de sessão, **não** refutados) | 1 cético por achado, com contexto dos 10 já confirmados p/ marcar duplicata | 55 |

**29 achados foram REFUTADOS com prova** — estão no estudo, e alguns eram
armadilhas caras (ver §5 e a §5 do estudo: uma "correção" proposta teria sido
regressão, revertendo a escolha manual dela a cada boot).

Detalhamento dos achados, cenários de falha e falsos-positivos:
`docs/process/estudos/2026-07-23-auditoria-gui-perfis-4-controles.md`.
Frente Bluetooth da mesma noite:
`docs/process/estudos/2026-07-23-diagnostico-sdp-cache-e-controle-zumbi.md`.

## Progresso

| Raiz | Estado | Nota |
|---|---|---|
| **R-01** especificidade de match + "regra de jogo" | OK FEITO | `7c937f0`. Catch-all deixa de ser tratado como perfil do jogo; `select_for_window` ordena por (especificidade, prioridade). |
| **R-02** `mode=None` não reverte + C6 | OK FEITO | `19bc7e9`. Duas guardas: catch-all nunca reverte; janela de jogo em foco congela reversão. Gesto manual toma posse do eixo. |
| **R-07** persistir só com origin manual | OK FEITO | `19bc7e9`. Testes olham o ARQUIVO (a suíte antiga monkeypatchava e não veria). |
| **R-08** reconciliação de draft/perfil ativo | OK FEITO | `83e0a0f`. Com gate de edição pendente + guard de reentrância + alvo em campo separado. Inclui C9 (Restaurar Padrão). |
| **R-09** salvar sem densificar + perfil novo limpo | OK FEITO | `ecc2eb4`. Fonte = draft; instâncias reinjetadas; flag `_new_profile`. |
| **R-11** `to_profile` com `source_name` | OK FEITO | `ecc2eb4`. Regra só é reemitida para o MESMO perfil; `controllers` fica fora do gate (é config, não regra). |
| **R-16** alvo de edição por gesto | OK FEITO | `705b16f`. UI do SELETOR-UNO-01 preservada; muda só o índice que a linha carrega. |
| **R-19** botão de soltar a trava | PARCIAL | `705b16f` (item 2: "Desligar" usa `trigger.reset`). Faltam itens 1, 3, 4 e 5. |
| **R-13** numeração de jogador | PARCIAL | `a54af15` (itens 2 e 4). Item 1 (escritor único) depende do R-20. |
| **R-17** `uniq` em todo output | PARCIAL | `28cb252` ("Apagar" da Lightbar). Falta o rumble com dono. |
| **R-18** resultado honesto da escrita | OK FEITO | `28cb252`. `applied` passou a ser lido; `status:"ok"` mantido de propósito. |
| **R-23** SIG do snapshot com cache | OK FEITO | `2475df1`. O fix do SDP-CACHE-01 nascia INERTE sem isto. |
| **R-24** watchdog `hciN` derivado | PARCIAL | `2475df1` (parte `hci0`). Falta "zumbi não conta como sessão viva". |
| R-03, R-04, R-05, R-06, R-10, R-12, R-14, R-15, R-20, R-21, R-22 | a fazer | ordem em §2 |

**Todas as levas acima: suíte completa verde (4553 testes) e `ruff` limpo a cada commit.**

## Requisito (o que "resolvido" significa)

A mantenedora escolhe uma configuração — perfil, modo de jogar, cor/gatilho de
**um** controle — e ela **vale**, do primeiro frame do jogo até o último, sem
que nada a desfaça pelas costas. E os 4 controles são **1, 2, 3 e 4**, não dois
pares repetidos.

---

# PLANO DE CORREÇÃO CONSOLIDADO — hefesto-dualsense4unix
**Base:** 55 achados recém-confirmados + 10 confirmados na rodada anterior (65 no total), todos mapeados abaixo. Nenhum item propõe contorno: toda entrada ataca a raiz.

---

## 1. CAUSAS-RAIZ

> **Nota transversal — os três relógios.** Boa parte dos achados de queixa (1) e (5) vem de confundir três travas distintas que hoje ninguém documenta junto:
> - `_emu_manual_ts` (lifecycle.py) — carimbo de gesto de **emulação/co-op/mouse/nativo**; mora **dentro dos appliers**, não é visto pelo autoswitch, **não expira o gesto**, só a janela de 30 s;
> - `store.manual_profile_lock` (state_store) — carimbo de **troca de perfil** (só `profile.switch` e hotkey); **suprime `_activate` inteiro** e por isso se auto-cura;
> - `store.manual_override_categories` / `manual_trigger_active` — carimbo de **gatilho/LED/rumble/apply**; **global, sem TTL e sem botão de soltar**.
> A assimetria entre eles é a raiz de R-03 e R-19; a correção precisa manter os três com semânticas explícitas, não fundi-los.

---

### R-01 — Catch-all (`MatchAny`/critério vazio) é tratado como perfil legítimo do jogo
- **Achados cobertos:** `perfil-any-vence-perfil-do-jogo`; `autoswitch-cede-override-manual-a-perfil-catch-all` (dup); `autoswitch-f2-cede-override-para-perfil-catch-all` (dup); **C1** `autoswitch-fallback-vira-perfil-de-jogo`.
- **Arquivos:** `src/hefesto_dualsense4unix/profiles/manager.py:366-376`; `profiles/autoswitch.py:156,176,255-274`; `profiles/schema.py:42-65`; `daemon/lifecycle.py:2038-2042` (predicado já correto, hoje isolado).
- **O que mudar:**
  1. Extrair de `lifecycle._profile_rule_matches_game` um helper único `perfil_e_regra_de_jogo(profile, info)` que exige `match.type == "criteria"` **e** que a `wm_class` `steam_app_<id>` em foco esteja em `match.window_class` (regex de título solto — caso do `fps.json`, que casa "Pro Controller"/"Painel de Controle" — **não** conta como regra de jogo).
  2. `select_for_window` passa a devolver o **objeto `Profile`** (não só o nome) e a ordenar por `(nao_e_catch_all, priority)`: qualquer `MatchCriteria` que casou vence qualquer catch-all; entre iguais a prioridade continua decidindo (preserva o tuning 50-80 dos presets). **Não** introduzir a escada window_class > regex (reordenaria criteria hoje empatados).
  3. Gate F2 (`autoswitch.py:258`) só cede a trava manual quando `perfil_e_regra_de_jogo(cand, info)`.
- **Validar ao vivo:** com FPS ativo, ajustar um gatilho na GUI (arma a trava) e abrir Mullet Mad Jack → `daemon.state_full` deve manter `manual_override_categories` e o perfil ativo **não** deve virar `vitoria`; criar um perfil MadJack com `window_class=["steam_app_2111190"]` e prioridade 0 → ele deve vencer `vitoria` (prio 5).
- **Risco de regressão:** perfis que hoje ganham por número (`vitoria` prio 5 sobre `meu_perfil`/`fallback`) deixam de ganhar de qualquer criteria que case. É o comportamento desejado, mas confere `test_profile_manager.py:84-125` (só usa fallback prio 0 — continua passando) e some um teste novo any(5)×criteria(0).

---

### R-02 — "Sem opinião" (`mode=None`) é executado como ordem de reverter
- **Achados cobertos:** `presets-catch-all-derrubam-modo-do-jogo` (crítica); `jogo-sem-perfil-desliga-gamepad-e-libera-supressao`; `perfil-catchall-desliga-gamepad-em-jogo`; **C6** `gesto-manual-nao-limpa-mode-from-profile`.
- **Arquivos:** `profiles/manager.py:296-330` (`apply_emulation` chama `mode_applier(None)` sempre); `daemon/lifecycle.py:1231-1248` (ramo `kind is None`, `set_gamepad_emulation(False, origin="profile")` na 1246), `:1114-1129` (`apply_profile_suppression`), `:961/1023` (gesto manual).
- **O que mudar:**
  1. `apply_emulation` passa ao applier a **identidade do perfil** (`match.type`, nome, `origin` da ativação), com `getattr` defensivo para os dublês de teste.
  2. Ramo `kind is None`: **catch-all nunca reverte** (é ausência de opinião, não ordem). Só `mode.kind == "desktop"` explícito ou perfil `criteria` derruba modo. Mesma regra em `apply_profile_suppression` — senão o catch-all continua soltando a emulação de desktop dentro do jogo.
  3. Trava independente de perfil: **enquanto a janela em foco for `steam_app_*` (leitura crua de `wm_class`, não `display_authority`)** não reverter gamepad/co-op por `origin="profile"`.
  4. **C6:** gesto manual (`set_gamepad_emulation/set_native_mode` com `origin="manual"`) precisa **limpar `_mode_from_profile`**, senão a reversão errada continua armada uma hora depois.
- **Validar ao vivo:** ativar "Co-op Local" na GUI, esperar >30 s, abrir Mullet Mad Jack → os 4 vpads continuam vivos, `gamepad_emulation.flag` intacto, supressão de desktop **não** liberada. Depois fechar o jogo e focar o Firefox → o perfil "Navegação" (criteria) aplica normalmente e a reversão de modo acontece.
- **Risco de regressão:** perfil "grudado" (modo nunca volta). Mitigação: (a) manter reversão em `kind="desktop"`; (b) C6 limpando `_mode_from_profile`; (c) log explícito `profile_mode_revert_skipped` com o motivo, para o doctor.

---

### R-03 — Lock de gesto manual descarta a seção do perfil, mente sucesso e nunca reaplica
- **Achados cobertos:** `mode-do-perfil-pulado-sem-retry`; `lock-manual-engole-modo-do-perfil-para-sempre`; `modo-de-perfil-pulado-para-sempre-pelo-lock-manual`; `profile-switch-mente-modo-descartado`.
- **Arquivos:** `daemon/lifecycle.py:1216-1225` (mode), `:1156-1164` (mouse), `:1114` (supressão), `:1319-1328` (rumble policy); `profiles/manager.py:281-330`; `profiles/autoswitch.py:176,300`; `daemon/ipc_handlers.py:299-326`.
- **O que mudar:**
  1. **Propagar `origin`** de `activate()` até os appliers. `profile.switch`/hotkey com `origin="manual"` é gesto **mais novo** que a máscara: **fura o lock** e zera `_emu_manual_ts` ao aplicar (senão a máscara que o perfil acabou de pôr trava o perfil seguinte).
  2. Appliers passam a devolver `aplicado | adiado`; `ProfileManager.activate` propaga a lista de seções adiadas.
  3. Origem automática (autoswitch): **commitar `_current_profile` normalmente** e guardar **uma** pendência `(mode, perfil, deadline=_emu_manual_ts + MANUAL_PROFILE_LOCK_SEC)`, drenada no `_poll_loop` (que já tem cadências próprias). Drenar só se (i) o perfil ativo ainda for o que originou, (ii) nenhum gesto novo renovou o carimbo e (iii) **o gate de jogo de R-04 permitir** (não trocar máscara com jogo em foco). Pendência é **sobrescrita**, nunca enfileirada.
  4. `profile.switch` responde `{"active_profile":…, "mode_aplicado":bool, "motivo":"lock_manual", "expira_em":N}` e a GUI toasta a verdade.
- **Validar ao vivo:** (a) mexer na máscara e, em <30 s, "Ativar" `sackboy_nativo` → máscara vira dualsense **na hora**, resposta com `mode_aplicado:true`. (b) mexer na máscara e abrir o Sackboy em <30 s → journal mostra **um** `profile_mode_deferred` e **uma única** aplicação ao vencer o lock, sem repetição a 2 Hz.
- **Risco de regressão:** flap a 2 Hz se alguém implementar a variante "não gravar `_current_profile`" (**rejeitada**, ver §5); aplicar modo obsoleto (mitigado pela revalidação do perfil ativo). Sem teste hoje: `rg profile_mode_skipped_manual_lock tests/` = vazio — os três testes novos são obrigatórios.

---

### R-04 — O modo do perfil só existe quando a JANELA aparece; a troca mid-game destrói os vpads
- **Achados cobertos:** `troca-de-mascara-no-meio-do-jogo-com-env-congelada`; `perfil-troca-mascara-com-jogo-aberto` (crítica).
- **Arquivos:** `assets/hefesto-launch.sh` (handshake/ping já existente); `daemon/ipc_handlers.py` (novo `profile.arm_for_appid`); `daemon/launch_env.py:127,395-404,519-578`; `daemon/lifecycle.py:1180-1281,976-998`; `daemon/subsystems/gamepad.py:820-828`; `daemon/subsystems/coop.py:311-321`.
- **O que mudar:**
  1. **Arming síncrono no launch:** o ping de vida que o wrapper já faz vira `profile.arm_for_appid {appid}`. O daemon resolve o perfil cujo `match.window_class` contém `steam_app_<appid>`, aplica `apply_profile_mode` **antes de o jogo executar**, rematerializa o env e só então responde. Timeout curto + fail-safe (sem resposta → caminho atual), porque travar o launch é inaceitável.
  2. **Gate destrutivo:** `apply_profile_mode` não executa `set_gamepad_emulation` destrutivo (flavor diferente, ou os `False` dos ramos `kind=None`/`desktop`) enquanto `display_authority == "game"`; guarda pendência e aplica na primeira borda em que a autoridade sair de `game`. Passa o caso idempotente (mesmo flavor) e as partes não destrutivas (co-op, gatilhos, LEDs).
  3. Com (1) feito, o `apply_profile_mode` disparado pela janela vira no-op pela idempotência de `gamepad.py:820-825` — o jogo enumera **uma vez**.
- **Validar ao vivo:** abrir o Sackboy e ler o journal na ordem: `arm_for_appid` → máscara `dualsense` → `materialize_launch_env` → wrapper lendo o `.env` já com `IGNORE` → janela aparece → **nenhum** `stop_gamepad_emulation`/`coop sync(force=True)` depois disso. Os 4 jogadores permanecem no menu do jogo.
- **Risco de regressão:** (a) launch travado se o IPC pendurar → timeout obrigatório; (b) gate largo demais faz o perfil **nunca** ser aplicado (agrava a queixa 1) — por isso o gate só existe **junto** com o arming; (c) o marker `last_run` sozinho perde a corrida com o `exec` do wrapper — **não** usar leitura assíncrona do marker como substituto do arming.

---

### R-05 — `launch_env` antecipa o backend do vpad **vigente** quando o perfil pede outro flavor
- **Achados cobertos:** `launch-env-dualsense-usa-backend-do-vpad-xbox`; `launch-env-backends-de-flavor-errado` (gêmeos, mesma linha).
- **Arquivos:** `daemon/launch_env.py:474-492` (`_env_for_profile`), `:347-350` (`compose_env`), `:407-438` (`_nativos_fora_da_antecipacao`).
- **O que mudar:** no ramo `dualsense`, quando `flavor != flavor_atual` (ou não há vpad vivo), **prognosticar** o backend com os mesmos gates da factory — `uhid_available()` **e** `controller_allows_uhid(daemon)` → `backends=["uhid"]`; senão manter o conservador. Carimbar o motivo no cabeçalho do `.env` ("prognóstico uhid" × "backends reais"). Manter a checagem de perfis nativos fora da antecipação também para o arquivo por-appid.
- **Validar ao vivo:** com a máscara global em `xbox`, `cat ~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_1599660.env` deve conter `SDL_GAMECONTROLLER_IGNORE_DEVICES` **e** `PROTON_DISABLE_HIDRAW` (hoje o arquivo por-appid é estritamente pior que o `default.env`). Abrir o Sackboy e confirmar que não aparece controle duplicado.
- **Risco de regressão:** prognóstico errado → o vpad cai para uinput Edge `0x0DF2`, que **não** está na lista do IGNORE (`0x054c/0x0ce6`); logo o pior caso é mapeamento SDL menos validado, nunca "zero controles". Assimetria a favor.

---

### R-06 — A allowlist do Steam Input não existe no caminho de lançamento nem no broker
- **Achados cobertos:** `steam-input-allowlist-ignorada-pelo-lancamento-e-pelo-broker`.
- **Arquivos:** `daemon/launch_env.py` (materialização); `daemon/subsystems/gamepad.py:158-165` (hide via broker) e `:99-118` (EVIOCGRAB); `broker/hidraw_broker.py:416-425`; `app/actions/emulation_actions.py:545-569`; `scripts/doctor.sh`.
- **O que mudar:**
  1. `steam_input_apps.txt` vira fonte de verdade do launch: gera `steam_app_<appid>.env` para cada appid da allowlist **mesmo sem perfil**, **sem** `IGNORE`/`PROTON_DISABLE_HIDRAW`; a allowlist entra no gatilho de regravação.
  2. **Modo nativo por-appid:** com o appid da allowlist detectado (marker `last_run` **ou** janela), suspender o `hide` do broker e o `EVIOCGRAB` daquele controle, restaurando ao sair. O gate de `gamepad.py:163` deixa de ser só `is_native_mode()`.
  3. Status honesto: distinguir "exceção configurada" de "exceção **efetiva**" (hidraw do físico legível pelo uid da usuária) na GUI e no doctor.
- **Validar ao vivo:** com o MMJ na allowlist, durante a sessão `getfacl` do hidraw do DualSense mostra a ACL da usuária e o broker **não** loga `node_hidden`; ao fechar, o hide volta.
- **Risco de regressão:** para os appids da allowlist o jogo passa a ver físico **e** vpad. É o preço do opt-in explícito — a alternativa correta ali é o Hefesto sair de cena para aquele appid (nativo), o que o item (2) implementa. **Depende de R-04** (marker/arming).

---

### R-07 — Persistência do estado global de emulação feita pelo caminho de perfil
- **Achados cobertos:** `perfil-persiste-flavor-e-onoff-global` (dup); **C7** `perfil-reescreve-flag-persistida-do-gamepad`.
- **Arquivos:** `daemon/subsystems/gamepad.py:897-901` (`save_gamepad_emulation(True,…)`), `:943` (`save_gamepad_emulation(False)`); `daemon/lifecycle.py:1006,1246,1264,1282,1523-1527,775`.
- **O que mudar:** persistir **só** com `origin == "manual"` — a mesma regra já escrita em `set_coop_enabled` (lifecycle.py:1022-1029) e em HARM-06 no mouse. `stop_gamepad_emulation(self, persist=(origin=="manual"))`. Cuidados que a proposta original não cobria: `_start_gamepad_emulation` (restore de boot) hoje cai no default `"manual"` — passar `origin="profile"`; `_restore_emulation_from_stash` deixa de persistir (correto).
- **Validar ao vivo:** escolher máscara Xbox → abrir e fechar o Sackboy → `~/.config/hefesto-dualsense4unix/gamepad_emulation.flag` continua `"xbox"` e sobrevive a reboot.
- **Risco de regressão:** boot sem restaurar nada se o `origin` do restore ficar errado. Cobrir com teste do par (`profile` → flag intocado / `manual` → reescrito): os testes atuais **monkeypatcham** `save_gamepad_emulation` e não veriam a regressão.

---

### R-08 — A GUI não reconcilia com o perfil ativo: draft e nome só carregam no boot; recargas pisam na edição
- **Achados cobertos:** **C2** `draft-nunca-recarrega-ao-trocar-perfil`; `draft-da-gui-nunca-recarrega-perfil-ativo` (dup); `draft-da-gui-preso-no-perfil-do-boot` (dup); **C9** `restaurar-default-nao-atualiza-nome-do-perfil-ativo`; **C10** `reload-profiles-store-clobbera-o-editor-da-aba-perfis`.
- **Arquivos:** `app/app.py:654-678,799,880`; `app/actions/status_actions.py:~1015-1030` (tick lento que já lê `state["active_profile"]`); `app/actions/footer_actions.py:221-255,426`; `app/actions/profiles_actions.py:736-759`.
- **O que mudar:** no tick lento, comparar `state["active_profile"]` com `_active_profile_name`; divergindo **e sem edição pendente**, re-executar `_bootstrap_draft_async()`; **havendo** edição pendente, aviso persistente no rodapé ("o perfil ativo mudou para X; suas edições são de Y") com botão explícito de descartar/recarregar — nunca troca silenciosa. `on_save_profile` resolve o nome ativo **no clique** (`ipc_bridge.active_profile_name()`), não no boot, e o diálogo diz em qual perfil vai gravar. "Restaurar padrão" atualiza `_active_profile_name`. `_reload_profiles_store` não sobrescreve o editor com edição pendente.
- **Validar ao vivo:** abrir a GUI com FPS ativo, abrir o Sackboy (autoswitch troca), voltar à GUI, ajustar Lightbar e clicar "Salvar Perfil" → o diálogo tem de propor `sackboy_nativo`, e o JSON gravado é o dele.
- **Risco de regressão:** recarregar draft por baixo de uma edição = perda de trabalho (por isso o gate de dirty é obrigatório, não opcional).

---

### R-09 — "Salvar" da aba Perfis constrói o `Profile` da fonte errada e **densifica** seções parciais
- **Achados cobertos:** **C3** `perfis-salvar-reconstroi-do-disco-e-descarta-o-draft`; `gui-salvar-densifica-overrides-por-controle`; `novo-perfil-herda-config-do-selecionado`.
- **Arquivos:** `app/actions/profiles_actions.py:475-502,880-948,120`; `cli/cmd_profile.py:254-258` (mesmo defeito).
- **O que mudar:**
  1. **Fonte:** ao editar o perfil ativo, a base é o **draft**, não o disco (C3).
  2. **Esparsidade:** trocar `source.model_dump()` + `model_validate` por `source.model_copy(update={...})`, ou no mínimo reinjetar as instâncias validadas (`base["controllers"] = source.controllers`) antes de revalidar — é a guarda que `draft_config.py:425-426` já tem e falta aqui. Perder `model_fields_set` é o que faz um override parcial (só brilho) virar `lightbar:[0,0,0]` e **apagar a lightbar** daquele controle.
  3. **Novo perfil:** flag `_new_profile` setada em `on_profile_new`, zerada em `_populate_editor`/`on_profile_duplicate`/após salvar; `source = existing or _duplicate_source or (None if _new_profile else selected_source)`. Preserva rename (BUG-RENAME-DROPS-CONFIG-01) e duplicação. **Não** usar `unselect_all()` (dispara repopulação do editor).
- **Validar ao vivo:** editar só o brilho de um DualSense numa aba por-controle, ir à aba Perfis, salvar → o JSON **não** ganha a chave `lightbar` no override e a cor continua herdando o global. Criar "Novo perfil" com "Navegação" selecionado → o JSON novo nasce **sem** `controllers` e sem `suppress_desktop_emulation`.
- **Risco de regressão:** `model_copy(update=)` muda o caminho de validação — cobrir com round-trip de perfil com override parcial (hoje `test_profile_editor_roundtrip.py` não tem um único `controllers`).

---

### R-10 — Identidade do arquivo é o **slug**, mas a GUI compara nome de exibição; rename não migra
- **Achados cobertos:** `guarda-de-sobrescrita-por-nome-arquivo-por-slug`; `renomear-perfil-cria-arquivo-novo-e-deixa-o-antigo`.
- **Arquivos:** `app/actions/profiles_actions.py:588-615,600`; `app/actions/footer_actions.py:231`; `profiles/loader.py:310-318,451-461`; `profiles/manager.py:375`.
- **O que mudar:** `_find_profile_by_slug()` (com `try/except ValueError` — `slugify` levanta em nome vazio e o editor chama isso a cada tecla) usado nas duas guardas (sobrescrita **e** downgrade para MatchAny), nomeando no diálogo o perfil **realmente** afetado. Mesmo tratamento no rodapé (`footer_actions.py:231`), onde a perda é integral porque grava o draft. **Rename:** comparar `slugify(nome_novo)` com `slugify(selecionado)`; divergindo, perguntar "Renomear" × "Salvar como cópia" e, no renomear, `delete_profile(antigo)` após o save bem-sucedido + migração do marker de perfil ativo. Não afrouxar `_find_cached_profile` global (ele também resolve a base do editor).
- **Validar ao vivo:** com "Navegação" no disco, criar perfil "Navegacao" (sem cedilha/acento) → tem de pedir confirmação nomeando "Navegação", e cancelar não pode tocar o arquivo. Renomear `sackboy_nativo` → não podem sobrar dois perfis com o mesmo `match`+`priority`.
- **Risco de regressão:** `delete_profile` do preset antigo é definitivo (o marker `.seeded_presets` respeita deleção). Só executar após save OK. `on_profile_save` hoje **não tem nenhum teste** — cobrir antes de mexer.

---

### R-11 — `DraftConfig.to_profile` reemite `match`/`priority`/`mode` do bootstrap para qualquer nome
- **Achados cobertos:** **C4** `rodape-salvar-reescreve-mode-match-prioridade-do-bootstrap`; `footer-salvar-copia-match-do-perfil-ativo` (dup).
- **Arquivos:** `app/draft_config.py:346,349,396-402`; `app/actions/footer_actions.py:220-246`; `app/gui_dialogs.py:32-72`.
- **O que mudar:** guardar `source_name` em `from_profile` e só reemitir `source_match`/`source_priority`/`source_mode` quando `name == source_name` (que é exatamente o caso que BUG-FOOTER-SAVE-DROPS-SECTIONS-01 quis proteger). Para nome novo, o rodapé precisa produzir regra própria: o `state_full` já expõe `window_detect_last_class` — o diálogo oferece "aplicar à janela atual (`steam_app_<id>`)" gerando `match={criteria, window_class:[…]}`, com opção explícita "sem regra (manual)". Prioridade do perfil novo acima dos catch-all e **sem empatar** com perfil de mesmo match (maior existente + 10, ou pedir na UI). Enquanto o campo de match não existir na GUI, **bloquear** o save com erro explicativo em vez de herdar em silêncio.
- **Validar ao vivo:** com FPS ativo, abrir o MMJ, ajustar algo e "Salvar Perfil" com nome "MadJack" → o JSON nasce com `window_class=["steam_app_2111190"]`, **não** com o regex de título do FPS nem com prioridade 60.
- **Risco de regressão:** salvar o próprio perfil ativo por cima dele mesmo tem de continuar preservando match/priority/mode (é o caso `name == source_name`).

---

### R-12 — Editor simples não expressa "jogo da Steam"; perfil de fábrica inalcançável; degradação muda para MatchAny
- **Achados cobertos:** `editor-simples-cria-matchany-e-nunca-perfil-por-appid`; `coop-local-nunca-casa-com-janela-nenhuma`.
- **Arquivos:** `profiles/simple_match.py:11-21,36-39`; `app/actions/profiles_actions.py:51,95-101,576-607,776,824-878`; `assets/profiles_default/coop_local.json`; `profiles/loader.py:145-190` (migração de presets + `audit_profiles`); `scripts/doctor.sh`; `assets/main.glade:1387`.
- **O que mudar:**
  1. Nova opção "Jogo da Steam" no editor simples → `MatchCriteria(window_class=["steam_app_<appid>"])`, com o appid vindo da **janela em foco/último jogo visto** (a GUI já sabe extrair) ou da biblioteca instalada — é a única chave confiável em XWayland **e** a única porta para o `.env` por appid. `detect_simple_preset` reconhece o formato para o round-trip não saltar para o avançado.
  2. "Jogo específico" vazio **nunca** degrada em silêncio: `ValueError` com frase de gente (o `on_profile_save` já toasta ValueError) ou a mesma confirmação de downgrade também para perfil novo.
  3. Campo "nome do executável": comparar case-insensitive (hoje `.lower()` no helper × basename cru no matcher) e rotular honestamente como "processo Linux nativo" — para jogo Proton o basename é o binário do wine.
  4. `coop_local` de fábrica: dar alvo real **ou** introduzir `{"type":"manual"}` como sentinel de "só ativação manual"; migrar a cópia em `~/.config` pela rotina de migração de presets já existente. **Nunca** convertê-lo em MatchAny (pioraria R-01).
  5. Coluna "Quando usar" mostra "só manual (nunca ativa sozinho)" para criteria vazio; `audit_profiles` + `doctor.sh` passam a listar "perfis inalcançáveis pelo autoswitch".
- **Validar ao vivo:** criar perfil pelo editor simples para o MMJ → o `.json` nasce com `steam_app_2111190` **e** o `steam_app_2111190.env` passa a existir; `coop_local` aparece rotulado como manual.
- **Risco de regressão:** transformar critério vazio em erro pode recusar perfis já salvos — tratar leitura como tolerante e validação só na escrita.

---

### R-13 — Duas autoridades escrevendo o mesmo player-LED e **dois espaços de numeração**
- **Achados cobertos:** `coop-e-slot-brigam-pelo-mesmo-led`; `coop-forca-player-1-no-primario`; `coop-vs-slot-numeracao`; `externos-crus-fora-do-broker-e-do-coop`; `reassert-sobrescreve-player-led-coop`; `externos-consomem-numero-de-jogador`; `coop-ativo-com-um-so-controle`; `coop-ativo-sem-segundo-controle`.
- **Arquivos:** `daemon/subsystems/coop.py:126-134,227-261,333,341-351,717-741,748-785,898-900`; `core/backend_pydualsense.py:926-971,1297,2436-2445,2008-2028`; `core/sysfs_leds.py:228-238`; `daemon/subsystems/identity.py:29-32,210-224,498-537`; `daemon/subsystems/external_identity.py:527-537,584,627`.
- **O que mudar (quatro invariantes):**
  1. **Escritor único.** O co-op **para** de escrever sysfs cru e passa a publicar seu padrão como **camada por-uniq** no `desired` do backend (acima da camada automática), limpa no `disable()`. Assim o `reassert_resolved_outputs` — que roda em **todo** `connect()`, a cada ≤30 s — reafirma o **mesmo** valor em vez de brigar. (A docstring de `identity.py:512-514`, "o co-op vence por construção", está **invertida** — corrigir junto.)
  2. **Numeração de exibição única.** O `ControllerIdentityRegistry` é a autoridade; o co-op **alimenta** o registry com sua ordem (`pin_slot(mac, player_index)`) para que o DualSense primário fique com 1 e os secundários 2..N; `_ds_reserve()` passa a devolver `max(maior slot DualSense, coop.player_count())`, empurrando Pro Nintendo e 8BitDo para N+1. Todo mundo (LED, card da GUI, LED dos externos) lê **só** o registry.
  3. **`player_index` continua sendo só alocação de vpad** (vira o MAC `02:fe:…:0N` do uhid; repetido = `-EEXIST`). Não tocar em `_next_player_index`.
  4. **Sem secundário não há co-op:** `if self._players:` antes de `_apply_coop_player_leds()` (coop.py:333) e revert quando `_players` esvazia — hoje `_teardown_player` reverte só o secundário e deixa o primário preso em P1. **Não** mexer em `should_be_active()` (enumerar `/dev/input` por tick é o que o PERF-MULTI-CONTROLLER-01 removeu, e faria o co-op piscar a cada blip de link). Corrigir a docstring de `coop.py:28-32`, que promete um gate de "2+ controles" que nunca existiu.
- **Validar ao vivo:** com Pro Nintendo + DualSense branco + 8BitDo + DualSense roxo ligados e co-op ativo: os quatro padrões formam exatamente {1,2,3,4}, o número do card da GUI bate com o LED do mesmo controle, e o conjunto **não muda** ao ativar/trocar de perfil, ao reconectar um controle nem depois de 60 s parado (dois ciclos de `reassert`). Com um único DualSense: o co-op não emite nenhum `set_players`.
- **Risco de regressão:** (a) `reset_output_overrides` da ativação de perfil (`manager.py:217`) **substitui o mapa por-uniq** e apagaria a camada do co-op → resolver junto com **R-20** (camadas com dono) ou reprogramar o co-op ao fim da aplicação; (b) mexer no `player_index` mata o probe uhid (`-EEXIST`) — proibido; (c) a escrita depende da regra udev `77-dualsense-leds.rules` (sem ela o co-op já logava `coop_player_led_indisponivel`).

---

### R-14 — `auto_player_colors` é um flag único que acopla **cor**, **numeração** e **externos** — e a GUI o desliga por engano
- **Achados cobertos:** `d4-desliga-identidade-global`; `auto-off-congela-numeracao-externos`.
- **Arquivos:** `app/actions/lightbar_actions.py:99-120,425-441`; `app/draft_config.py:203-207,404`; `profiles/schema.py:168`; `profiles/manager.py:208-216,249`; `daemon/subsystems/identity.py:152,524-537`; `daemon/subsystems/external_identity.py:611-618`.
- **O que mudar:**
  1. Separar **ATRIBUIÇÃO** de slot (sempre acontece) de **APARÊNCIA** automática (governada pelo flag). Em `identity.make_auto_output_provider` e em `external_identity.tick`, o `slot_for(..., assign=True)` roda **antes** do early-return do flag; com o auto desligado só as **escritas de LED** são puladas (contrato NUMA-03c preservado).
  2. Desdobrar o flag em `auto_player_colors` (cor) e `auto_player_numbers` (padrão de player-LED/numeração), para que mexer em player-LED nunca mate a paleta nem a numeração dos externos.
  3. Cor única aplicada em "Todos" **não desliga o auto**: grava override por-uniq em cada controle conectado (override vence auto no merge por campo — D5), preservando a numeração.
  4. `player_leds` global do perfil sem escrita explícita é "sem opinião" — parar o broadcast denso idêntico em `manager.py:214`.
- **Validar ao vivo:** com FPS ativo (que hoje está no disco com `auto_player_colors:false`), ligar o 8BitDo → ele recebe número e a GUI mostra o slot; escolher o preset "P1" com alvo "Todos" → a numeração automática dos outros **continua** e nenhum JSON ganha `auto_player_colors:false`.
- **Risco de regressão:** perfis já salvos com `auto_player_colors:false` (o `fps.json` dela) mudam de comportamento — migração explícita mapeando o campo antigo para os dois novos, com default compatível.

---

### R-15 — Expiração de slot assimétrica e compactação sobre reservas offline
- **Achados cobertos:** `expiracao-assimetrica-troca-cores`; `renumerar-inclui-desconectados`.
- **Arquivos:** `daemon/subsystems/identity.py:139,323-333,361-384`; `daemon/subsystems/external_identity.py:193-212`; `daemon/lifecycle.py:2167-2169`; `daemon/ipc_handlers.py:658-679`; `app/actions/home_actions.py:795-801`; `tests/unit/test_identity_registry.py:109-113,227-238`.
- **O que mudar:**
  1. **Dentro do boot, número é do MAC e ninguém expira** (entre boots o `boot_id` já renumera). Remover o ramo `elif self._saw_connected:` e o campo `_saw_connected`, deixando `sync_connected` só reconciliar e persistir — igual ao lado externo. Isso elimina a corrida de ordem de wake **e** fecha a janela de duplicata em que `_ds_reserve()` devolve 0 no meio do tick externo.
  2. `snapshot_connected()` nos dois registros (dando finalmente uso ao `_connected`, hoje escrito e nunca lido). `_renumber_locked` compacta **os conectados** em 1..N e anexa as reservas ausentes em N+1..M no mesmo mapping (preserva a promessa D2 sem deixar a reserva bloquear a faixa baixa).
  3. `renumbered` passa a conter só as chaves que **mudaram** — hoje um no-op total responde "4 controle(s) renumerado(s)".
  4. Trocar os dois testes que congelam o comportamento antigo por um de estabilidade intra-boot (dois DualSense somem juntos, voltam em ordem invertida, cada um recupera o próprio número) e um de renumeração entre boots.
- **Validar ao vivo:** desligar os dois DualSense, religar em ordem invertida → cada um volta com a **própria** cor/número. Com o 8BitDo offline segurando um slot baixo, clicar "Renumerar agora" → os conectados descem para 1..N e o toast diz o número certo (ou "já estava compacta").
- **Risco de regressão:** dois testes existentes falham **de propósito** — trocar deliberadamente, com nota no commit. Não dropar reserva (quebraria o motivo declarado em `external_identity.py:196-199`).

---

### R-16 — Alvo de edição por-controle derivado da **contagem**, não do **gesto**
- **Achados cobertos:** **C8** `edit-target-cai-para-global-com-menos-de-2-dualsense`; `seletor-colapsa-para-global-com-1-dualsense`; `por-controle-desligado-com-1-dualsense`; `edicao-por-controle-exige-2-dualsense`; `override-por-controle-apagado-quando-alvo-some`; `race-state-full-stale-reverte-alvo-edicao`.
- **Arquivos:** `app/actions/status_actions.py:544-586,609-611,632-633,637-648,660-696`; `app/actions/triggers_actions.py:283-302`; `app/actions/lightbar_actions.py:99-122`; `app/draft_config.py:559-604`.
- **O que mudar:**
  1. `editavel = len(conectados) >= 1`; o ramo de 1 controle emite a linha com o **índice real** e `_sync_edit_target(index)` — override por-MAC é o valor certo mesmo com um só controle. `None` fica **reservado ao clique explícito em "Todos"**.
  2. `_edit_target_uniq` **só muda por gesto**: queda de controle não zera o alvo; o badge continua visível dizendo "Editando: Controle N (desconectado)" ou "Editando: todos os controles". Nunca conviver rótulo "Controle N" com escrita global.
  3. `with_override_fields_cleared` (gatilhos e LEDs) só roda com **escopo explícito** (`aplicar_a_todos=True` vindo do handler do botão "Todos"), nunca inferido de `uniq is None`.
  4. Corrida do `state_full` stale: `_target_pending = index` antes do `controller.target.set`; o `on_success` limpa comparando com o `target_index` que o daemon **já devolve**; o refresh descarta payloads anteriores à escrita. Como o executor é FIFO de 1 worker, isso fecha a janela sem timeout (mantendo limpeza no `on_failure`, que hoje é mudo).
- **Validar ao vivo:** com só o DualSense branco vivo, selecionar o controle e ajustar cor → o JSON grava override por-MAC (não global) e nenhum override existente perde campo. Com dois DualSense, clicar "Controle 2" e arrastar o slider imediatamente → a cor vai para o Controle 2 mesmo se um snapshot antigo chegar no meio.
- **Risco de regressão:** usuária achando que edita "todos" quando edita um só → o badge sempre visível é parte da correção, não enfeite.

---

### R-17 — Escritas de saída sem `uniq` caem na rota global mutável (broadcast) e apagam overrides
- **Achados cobertos:** `apagar-lightbar-ignora-controle-selecionado`; `apagar-lightbar-ignora-uniq` (gêmeos); `rumble-fixado-vira-broadcast-nos-4`; (parte de) `sucesso-falso-sem-dualsense-conectado`.
- **Arquivos:** `app/actions/lightbar_actions.py:344`; `app/ipc_bridge.py:306-325`; `daemon/ipc_handlers.py:371-373,441-448,1611-1691`; `daemon/subsystems/rumble.py:50-76,95`; `daemon/lifecycle.py:160`; `daemon/subsystems/gamepad.py:298,305-310`; `core/backend_pydualsense.py:973-1008,1657-1706,1970-1978,2030`.
- **O que mudar:**
  1. **Todo** output da GUI leva `uniq` — o "Apagar" da Lightbar é o único que não leva: `led_set((0,0,0), uniq=self._edit_uniq())`. (Não passar `brightness`: preto × fator continua preto e sugeriria uma persistência que não existe.) Com `uniq`, o caminho é `apply_output_for`, imune ao seletor global.
  2. **Rumble ganha dono:** `DaemonConfig.rumble_active` vira `dict[str|None, tuple[int,int]]`; `rumble.set/stop/passthrough` aceitam `uniq` espelhando `trigger.set`/`led.set`; `_reassert_rumble` itera o mapa usando `set_rumble_for(uniq,…)`. O gate global de `gamepad.py:298` (que hoje faz um rumble fixado esquecido matar o FF do jogo **nos quatro**) vira gate por-uniq. Rótulo da aba passa a dizer em qual controle está travado.
  3. **`_for_each`/`_for_each_led` não degradam para broadcast** quando o alvo sumiu de `_handles`: no-op + log. Para rumble, alvo ausente **encerra** a entrada (zerar/dropar) — efeito contínuo não pode migrar de controle.
- **Validar ao vivo:** com dois DualSense, selecionar o Controle 2, "Apagar" → só ele apaga e o override de cor do outro continua no `state_full`. Fixar rumble no roxo, derrubar o BT dele → o branco **não** começa a vibrar e o FF do jogo continua funcionando nos demais.
- **Risco de regressão:** trocar broadcast por no-op pode "esconder" escritas em hotplug — o `reassert_resolved_outputs` já cobre isso ao reconectar; logar `output_target_ausente` para o doctor.

---

### R-18 — A fronteira daemon→GUI perde o resultado real da escrita (sucesso cego)
- **Achados cobertos:** `apply-draft-status-ok-sempre`; `sucesso-falso-sem-dualsense-conectado`.
- **Arquivos:** `daemon/ipc_draft_applier.py:88-92`; `daemon/ipc_handlers.py:356-357,402-404,1631-1636`; `app/ipc_bridge.py:243-273,408-410`; `app/actions/footer_actions.py:146-152`; `app/actions/triggers_actions.py:566-568`; `core/backend_pydualsense.py:1664-1706,1997-2003`.
- **O que mudar:**
  1. `_for_each`/`_for_each_led` devolvem **`int`** (handles em que a operação rodou sem exceção — hoje o `except` por handle também vira "sucesso"); `set_trigger/set_rumble/set_led` propagam; `apply_output_for` distingue "escrito no hardware" de "só registrado como override (controle offline)".
  2. Handlers devolvem `{"status":"ok", "applied":[...], "falhas":{secao:motivo}, "aplicado_em":n}`. **Aditivo:** manter `status:"ok"` — trocar para `"partial"`/`"failed"` faria a GUI atual imprimir "daemon offline", que é outra mentira.
  3. GUI: toast "Aplicado, exceto: gatilhos — Fim (3) precisa ser maior que Início (8)" reusando `humanizar_erro_gatilho`; "guardado — vai valer quando o controle conectar" para registro-sem-hardware; aviso persistente de incompatibilidade quando só há externos (Pro Nintendo/8BitDo não têm gatilho adaptativo nem lightbar). `_clear_mouse_dirty()` só se `"mouse" in applied`.
  4. **Não armar a trava manual em no-op** (`aplicado_em == 0`) — hoje um gesto que não escreveu em ninguém deixa o sistema "armado" (liga R-19).
  5. Origem: acoplar os sliders de gatilho (Fim.lower = Início+1) para o payload inválido nem nascer.
- **Validar ao vivo:** desconectar todos os DualSense, aplicar um preset de gatilho → a GUI diz "nenhum DualSense conectado", **não** "aplicado", e `manual_override_categories` continua vazio.
- **Risco de regressão:** GUI antiga × daemon novo (e vice-versa) — por isso só campos aditivos.

---

### R-19 — Trava manual global, sem TTL, sem botão de soltar, armada até pelo preview
- **Achados cobertos:** `override-manual-armado-sem-expiracao`; `aba-gatilhos-arma-trava-sem-botao-de-soltar`.
- **Arquivos:** `daemon/ipc_draft_applier.py:51-63`; `daemon/ipc_handlers.py:382-416,1635,1691`; `daemon/state_store.py:72,132-158,285-288,364-372`; `profiles/autoswitch.py:227,255-274`; `app/ipc_bridge.py` (`__all__`); `app/actions/triggers_actions.py:209,217-235,345-348,390-397,534-539`; `app/draft_config.py:745-768`.
- **O que mudar:**
  1. **Supressão alvejada:** a trava manual bloqueia apenas a **reaplicação do perfil já ativo** (a Causa A da Onda U, no-op útil zero) e deixa passar a troca para perfil **diferente** — jogo ou não. Isso conserta o "desktop congelado com o modo do jogo" **sem** TTL cego (TTL reabriria o "perfil eterno" U3/U4/U9/U11) e **torna a exceção F2 desnecessária** (ver R-01 §5).
  2. **Botão de soltar:** expor `trigger_reset(side)` no `ipc_bridge` (o RPC `trigger.reset` já existe e já está roteado) e ligar o botão "Desligar" nele — hoje ele manda outro `trigger.set` e **re-arma** a trava. Manter o clear total do `trigger.reset` (contrato deliberado e testado em `test_onda_u_trava_por_categoria.py:113-121`); estreitar exigiria mudar o contrato de propósito.
  3. **Preview não arma:** `trigger.set` ganha `preview: true` e nesse caso não chama `mark_manual_trigger_active` — passear pelos modos não pode congelar o autoswitch.
  4. **Granularidade real:** `to_ipc_dict` emite triggers/leds/rumble **incondicionalmente**, então a granularidade por categoria do applier é letra morta no "Aplicar" — marcar dirty por seção (como `MouseDraft.dirty` já faz) e armar só o que mudou.
  5. **Visibilidade:** expor `manual_override_categories` no `state_full` (já viaja no snapshot) e mostrar badge "ajuste manual ativo — troca automática pausada" com clique para liberar.
- **Validar ao vivo:** aplicar uma cor durante o Sackboy, fechar o jogo e ir ao Firefox → o perfil "Navegação" **entra**; passear pelos modos de L2 sem clicar Aplicar → `manual_override_categories` continua vazio; clicar "Desligar" → a trava é **liberada**, não re-armada.
- **Risco de regressão:** afrouxar demais reabre o "perfil eterno" da Onda U — a regra tem de ser exatamente "bloqueia reaplicar o mesmo, libera trocar para outro", combinada com R-20 (a troca legítima não pode apagar a edição).

---

### R-20 — Saída resolvida por **substituição** e materialização precoce, em vez de camadas esparsas com dono
- **Achados cobertos:** **C5** `ativacao-de-perfil-apaga-overrides-por-controle`; `brilho-por-controle-materializa-cor-global`.
- **Arquivos:** `profiles/manager.py:208-220,440-467`; `core/backend_pydualsense.py:926-971,2008-2028`; `app/draft_config.py:671-684`; `daemon/subsystems/identity.py:526-537`; `daemon/ipc_draft_applier.py`.
- **O que mudar:**
  1. **Camadas com dono declarado** (default do perfil → automático/identidade → override por-controle do perfil → edição manual da usuária → co-op) e `reset_output_overrides` passa a substituir **só a camada do perfil**, não o mapa inteiro — hoje ativar perfil apaga o que a usuária ajustou por controle **e** apagaria a camada do co-op de R-13.
  2. **Brilho deixa de materializar cor:** emitir `led` no `OutputSpec` só quando `"lightbar" in campos`; o brilho vira campo próprio (`led_brightness`) aplicado **depois** do merge, ou registrado por-uniq no registry para escalar a cor **resolvida** (automática quando o auto está ligado). Espelhar em `DraftConfig._controllers_to_ipc`, senão o caminho ao vivo diverge da ativação.
- **Validar ao vivo:** perfil com auto ligado, ajustar **só o brilho** de um DualSense e reativar o perfil → ele continua na cor **do slot**, escalada; ajustar cor de um controle e trocar de perfil e voltar → o ajuste manual sobrevive conforme a precedência declarada.
- **Risco de regressão:** camadas mal delimitadas ressuscitam override de perfil antigo — cada camada precisa ser limpa pelo seu dono, com teste por camada.

---

### R-21 — Cache anti-reescrita do sysfs é descartado a cada `connect()`
- **Achados cobertos:** `cache-sysfs-descartado-a-cada-reconcile`.
- **Arquivos:** `core/backend_pydualsense.py:1281,1297,1398-1495`; `core/sysfs_leds.py:64,182-186,228-238`.
- **O que mudar:** em `_refresh_sysfs_leds`, **reusar `prev[key]`** quando o `indicator_dir` não mudou (a comparação já existe para `new_keys`); ou mover `_last_write`/`_skip_logged` para um dicionário do backend indexado por `(key, indicator_dir)`. **Pré-condição obrigatória:** a reescrita incondicional de hoje é a única recuperação contra escritor por hidraw (Steam/winedevice pintam sem que `get_rgb` enxergue). Junto com o cache, decidir de propósito: `verify=True` no reassert do `connect()` aceitando que o vetor hidraw fica com `defend_display`, **ou** repaint forçado periódico bem mais lento (invalidate a cada N ticks / só sob autoridade `daemon`). **Se essa decisão não for tomada, não aplicar o item** — o ganho é só tráfego HID poupado e o custo é lightbar presa na cor do jogo.
- **Validar ao vivo:** com o daemon parado em regime, contar escritas no journal por 5 min (deve cair a ~zero) e, em seguida, abrir um jogo que pinta a lightbar e fechar → a cor tem de voltar ao perfil.
- **Risco de regressão:** L-03 da auditoria pós-leva; regressão da Onda L/N se aplicado sozinho.

---

### R-22 — I/O bloqueante (socket do broker + ioctl HID) na thread do event loop
- **Achados cobertos:** `broker-open-bloqueante-no-event-loop`.
- **Arquivos:** `daemon/subsystems/coop.py:506,560-578`; `daemon/subsystems/gamepad.py:631-647,858`; `daemon/lifecycle.py:2287,500,1993`; `core/backend_pydualsense.py:742,787,110`; `integrations/hidraw_broker_client.py:153-154,202,289`.
- **O que mudar:** a calibração 0x05 é **imutável por unidade** → virar cache por MAC (`daemon._calibration_by_uniq`), preenchido no caminho de `connect`/hotplug, que já roda fora do loop (`await self._run_blocking(...)`) ou no `broker_executor_for(daemon)`. `coop._read_player_calibration` e `gamepad.read_primary_calibration` leem **só** o cache; miss devolve `None` (0x05 canônico, fail-safe que o contrato já prevê) e agenda o preenchimento. Isso resolve as duas fontes (socket do broker **e** `HIDIOCGFEATURE` em BT ocioso, que sozinho segura o loop até o timeout do hidp). **Não** mover `coop.sync` para outra thread (criaria a corrida em `_players` que os handlers documentam); encurtar o timeout do `open_fd` seria paliativo (não cobre o ioctl).
- **Validar ao vivo:** ligar co-op com 4 controles e cronometrar o intervalo entre ticks de `forward_all` no journal — sem buracos de segundos; a GUI continua respondendo durante `gamepad.emulation.set`.
- **Risco de regressão:** cache servindo dado de outro controle — a chave é o MAC, estável por unidade.

---

### R-23 — Snapshot de bonds hasheia só os `info`: a foto com cache SDP nunca nasce
- **Achados cobertos:** `snapshot-dedup-so-info-anula-sdp-cache`.
- **Arquivos:** `scripts/bt_bonds_snapshot.sh:61-87,109-127`; `scripts/doctor.sh`.
- **O que mudar:** calcular o `SIG` sobre **exatamente o conjunto que o script copia** (os `info`, os `attributes` dos devices, `settings`/`attributes` do adaptador e as entradas `cache/<MAC>` dos devices com bond), ordenado, **prefixado por um marcador de versão** (`FMT=2`). O marcador é o que destrava a primeira foto após a mudança de formato mesmo com estado idêntico; a inclusão do cache é o que faz curas futuras do SDP (o `Connect()` do `vigia_sdp_cache`) serem fotografadas. Manter os `info` como fonte única do guard "zero bonds = recusa" e do log de contagem. **Não** usar mtime (os `info` são reescritos com conteúdo idêntico → churn a cada 15 min, exatamente o que a dedup existe para evitar). `doctor.sh` avisa quando o snapshot mais recente não tem `cache/` apesar de haver bond com `[ServiceRecords]`.
- **Validar ao vivo:** rodar o snapshot → nasce diretório novo **com** `cache/`; rodar de novo sem mudar nada → volta a ser no-op; curar um cache por `Connect()` → o snapshot seguinte grava.
- **Risco de regressão:** churn de disco se alguém incluir campo volátil no `SIG`.

---

### R-24 — Watchdog BT: caminho D-Bus com `hci0` fixo e "sessão viva" contando zumbi
- **Achados cobertos:** `vigia3-hci0-hardcoded`; `vigia1-conta-zumbi-como-sessao-viva`.
- **Arquivos:** `scripts/bt_health_watchdog.sh:47-56,134,192-225,279,287`.
- **O que mudar:**
  1. Derivar `OBJ` da árvore real (`_dbus_device_paths | grep -im1 "/dev_<MAC-underscore>$"`, chamado **uma vez** por tick), e, quando não houver objeto, **logar** em vez de `continue` mudo. O dongle já re-enumerou como `hci1` nesta máquina (medido 23/07 09:22) — com `hci0` fixo a cura vira no-op silencioso.
  2. A vigia 3 grava carimbo `zumbi-<MAC>` ao concluir que o device não resolve SDP após as 6 tentativas, e o **apaga** quando `[ServiceRecords]` aparece ou o hidraw sobe. A vigia 1 desconta de `CONECTADOS` **apenas** devices que satisfaçam **todas**: perfil HID no `info`, sem hidraw com aquele `HID_UNIQ`, e carimbo de zumbi de ≥2 ticks. Nunca devices não-HID (áudio BT não tem hidraw) e nunca zumbi visto uma única vez — é assim que se evita reintroduzir o falso-positivo do WATCHDOG-FP-01. Log explícito "N conectado(s), M zumbi(s) descontado(s)".
- **Validar ao vivo:** forçar `hci1` (replug do dongle) e confirmar que a vigia 3 loga tentativa de `Connect()`; com um zumbi persistente + recusas em loop, confirmar que o restart acontece **depois** de 2 ticks e nunca com áudio BT conectado.
- **Risco de regressão:** FP do watchdog derrubando sessão viva — as três condições combinadas são a mitigação; manter a frase/invariante "nunca derrubo sessão viva" e o rate-limit.

---

## 2. ORDEM DE EXECUÇÃO

**Três trilhas paralelizáveis por arquivo disjunto:** **T1 = daemon/core**, **T2 = GUI (`app/`)**, **T3 = scripts BT**. O único acoplamento entre T1 e T2 é o contrato IPC (R-18/R-19) — fazer o lado daemon primeiro, com campos **aditivos**, e o lado GUI depois.

| # | Item | Trilha | Queixa | Sev. | Depende de |
|---|------|--------|--------|------|-----------|
| 1 | **R-05** prognóstico uhid no launch_env | T1 | (1) | alta | — (independente, barato) |
| 2 | **R-01** especificidade de match + helper de "regra de jogo" | T1 | (1)(2) | alta | — |
| 3 | **R-02** `mode=None` não reverte + C6 | T1 | (1) | **crítica** | R-01 |
| 4 | **R-07** persistir só com origin manual | T1 | (1) | alta | — |
| 5 | **R-04** arming no launch + gate destrutivo | T1 + wrapper | (1)(3) | **crítica** | R-02 (semântica do applier) |
| 6 | **R-03** lock: manual fura, automático adia com pendência | T1 | (1) | alta | R-02, R-04 (gate de drenagem) |
| 7 | **R-16** alvo de edição por gesto | T2 | (2) | alta | — |
| 8 | **R-17** `uniq` em todo output + rumble com dono | T1+T2 | (2)(5) | alta | — |
| 9 | **R-09** salvar sem densificar + perfil novo limpo | T2 | (2)(5) | alta | R-08 (fonte = draft) |
| 10 | **R-08** reconciliação de draft/perfil ativo | T2 | (1)(2) | alta | — |
| 11 | **R-15** slot estável no boot + renumerar só conectados | T1 | (3) | média | — |
| 12 | **R-13** escritor único + numeração única do player-LED | T1 | (3) | alta | R-15; coordenar com R-20 |
| 13 | **R-20** camadas de saída com dono + brilho separado | T1 | (2)(3) | alta | R-13 (a camada do co-op precisa sobreviver) |
| 14 | **R-14** desacoplar auto (cor × numeração × externos) | T1+T2 | (3) | alta | R-13 |
| 15 | **R-18** resultado honesto da escrita | T1→T2 | (5)(2) | média | — |
| 16 | **R-19** trava alvejada + botão de soltar + preview | T1+T2 | (5) | alta | R-01, R-18 (não armar em no-op) |
| 17 | **R-11** `to_profile` com `source_name` + regra pela janela | T2 | (1)(2) | alta | R-08 |
| 18 | **R-10** slug como identidade + rename com migração | T2 | (5) | média | R-09 |
| 19 | **R-12** editor simples "Jogo da Steam" + coop_local + audit | T2 + dados | (1) | média | R-01, R-11 |
| 20 | **R-06** allowlist Steam Input efetiva | T1 | (1) | média | **R-04** |
| 21 | **R-23** SIG do snapshot com cache + `FMT=2` | T3 | — | alta | — |
| 22 | **R-24** watchdog: `hciN` + zumbi não é sessão viva | T3 | (4) parcial | média/baixa | — |
| 23 | **R-22** calibração 0x05 em cache fora do loop | T1 | (5) parcial | média | — |
| 24 | **R-21** cache sysfs cross-tick | T1 | — | baixa | **decisão do repaint anti-hidraw** |

**Podem começar já, em paralelo, sem tocar nada em comum:** R-05, R-01, R-07 (T1); R-16, R-08 (T2); R-23, R-24 (T3).
**Gargalos:** R-02 é pré-requisito de R-03 e de metade da queixa (1); R-13 é pré-requisito de R-14 e coordena com R-20; R-04 é pré-requisito de R-06.
**Último da fila:** R-21, e só se a decisão sobre o repaint anti-hidraw for tomada explicitamente.

---

## 3. SEGURO AGORA × EXIGE REINÍCIO

**A) Seguro com controles conectados e jogo aberto** (não toca processo do daemon nem vpad):
- **Dados/JSON:** correção do `coop_local` de fábrica e migração de presets (R-12, parte dados) — só vale na próxima ativação.
- **Scripts BT (R-23, R-24):** editar e recarregar timer/serviço do watchdog e rodar o snapshot na mão. **Não** tocar em `bluetooth.service` com jogo aberto.
- **Documentação/audit/doctor** (R-12 §5, R-06 §3, R-23 complemento).

**B) Exige reiniciar apenas a GUI** (o daemon e os vpads seguem vivos; jogo aberto **não** é afetado):
- R-08, R-09, R-10, R-11, R-16, parte GUI de R-12/R-14/R-17/R-18/R-19.
- Validação: fechar e reabrir a janela do Hefesto; nenhuma reconexão de controle necessária.

**C) Exige reiniciar o daemon** — **derruba vpads e grabs**, portanto **nunca com jogo aberto** (regra já medida: recriar vpad mid-game invalida os handles do jogo):
- R-01, R-02, R-03, R-04, R-06, R-07, R-13, R-14 (lado daemon), R-15, R-17 (lado daemon), R-18 (lado daemon), R-19 (lado daemon), R-20, R-21, R-22.
- Roteiro: fechar o jogo → reiniciar o daemon → reconectar/replugar os controles se a numeração for parte da validação → reabrir o jogo.

**D) Exige relançar o jogo (env congela no `exec` do wrapper), mas não reconectar controle:**
- R-05 (o `.env` por appid só vale no próximo launch), R-04 (arming), R-06 (env da allowlist).

**E) Exige re-parear / mexer no BlueZ:** **nada** neste plano. R-23/R-24 não apagam bond nem cache (a vigia 3 já foi reescrita para curar por `Connect()`), e nenhuma correção pede re-pareamento.

**Gate humano obrigatório antes de fechar a leva:** sessão de co-op real com os 4 controles (Pro Nintendo, 8BitDo, DualSense branco, DualSense roxo) validando, na ordem: numeração 1-2-3-4 estável (R-13/R-14/R-15) → abrir Sackboy e conferir que a máscara e o co-op do perfil valem desde o primeiro frame (R-04/R-05/R-03) → abrir Mullet Mad Jack e conferir que **nada** é desligado (R-01/R-02) → ajustar um controle na GUI e conferir que só ele muda (R-16/R-17/R-20).

---

## 4. QUEIXAS × EXPLICAÇÃO

### (1) "quando eu escolho o sackboy e o madjack, a config dos controles ou o modo de jogar NUNCA é respeitado quando abro o jogo" — **EXPLICADA, com sobreposição de 7 raízes**
Há **duas histórias distintas** e ambas terminam na mesma frase:

**Sackboy (tem perfil):** o `.env` por appid é gerado **sem** dedup porque `_env_for_profile` usa os backends do vpad Xbox vigente (**R-05**) → o jogo abre vendo o DualSense físico; o modo do perfil só é aplicado quando a **janela** aparece (**R-04**), e quando aplica, troca de flavor e **recria os vpads com o jogo já rodando**, invalidando os handles; se ela mexeu na máscara/co-op nos 30 s anteriores, o modo é **descartado silenciosamente e nunca reaplicado** (**R-03**); a máscara que o perfil pôs (ou removeu) é **persistida por cima da escolha manual** e some no boot seguinte (**R-07**); e a edição feita na GUI depois que o autoswitch trocou de perfil vai para o **perfil errado** (**R-08**, **R-11**).

**Mullet Mad Jack (não tem perfil):** o catch-all `vitoria` (MatchAny, prio 5) **vence** e é tratado como perfil do jogo (**R-01**); ele tem `mode=null`, e "sem opinião" é executado como **ordem de reverter** — `set_gamepad_emulation(False, origin="profile")` **com o jogo em foco** e com o `IGNORE` já congelado no processo = zero controles / co-op desmontado (**R-02**); a exceção per-app de Steam Input que ela configurou é **inerte**, porque o broker esconde o hidraw do físico e nada no launch consulta a allowlist (**R-06**); e ela **não consegue** criar o perfil que resolveria: o editor simples não expressa "jogo da Steam" (**R-12**), um perfil novo nasce com prioridade 0 atrás do catch-all (**R-01**) e o "Salvar Perfil" do rodapé herda o match do perfil ativo (**R-11**).

### (2) "as configs que o user faz parecem não impactar controle a controle" — **EXPLICADA**
- **R-16** — com menos de 2 DualSense (estado corrente: o roxo está sem hidraw) o alvo de edição **vira global** enquanto o rótulo continua dizendo "Controle N"; e a queda de um controle zera o alvo **sem aviso**, fazendo a mexida seguinte **apagar** o override por-MAC dos outros.
- **R-09** — salvar na aba Perfis **densifica** o override parcial: um ajuste só de brilho vira `lightbar:[0,0,0]` (a lightbar daquele controle **apaga**) e o override para de herdar o global para sempre; e "Novo perfil" clona os overrides por-MAC do perfil selecionado.
- **R-17** — "Apagar" da Lightbar é o único output da GUI sem `uniq` (cai na rota global que o PERFIL-05 abandonou) e o rumble fixado **não tem dono**: migra ou vira broadcast nos quatro.
- **R-20** — ativar perfil **substitui** o mapa de overrides por-uniq (C5), e um override que só mexe no brilho **materializa a cor global**, matando a cor automática do slot.
- **R-18** — quando nada é escrito, a GUI ainda diz "aplicado".

### (3) "dois 'player 2' e dois 'player 1' em vez de 1,2,3,4" — **EXPLICADA**
A combinação exata do estado medido: os externos ocupam os slots **1 (Pro Nintendo)** e **3 (8BitDo)**, o DualSense branco é slot **2**, e o co-op crava **1 fixo no primário** e 2..N nos secundários (**R-13**) → o branco acende como jogador 1 **junto** com o Pro Nintendo ("dois player 1"); quando o roxo entra como secundário do co-op ele recebe 2 enquanto o branco ainda exibe o padrão do slot 2 vindo do `reassert` → **"dois player 2"**. Somam-se: o `reassert_resolved_outputs` de todo `connect()` (≤30 s) **repinta por cima** do co-op e vice-versa, num pisca-pisca sem fim (**R-13**); a expiração assimétrica de slots faz cor/número **trocarem de dono** entre os dois DualSense conforme a ordem de wake (**R-15**); um clique em cor/preset com alvo "Todos" **desliga a identidade automática de todo mundo** e persiste isso no perfil, o que ainda **congela a numeração dos externos** (**R-14**); "Renumerar agora" não conserta porque compacta incluindo reservas offline (**R-15**); e a recriação de vpads mid-game reembaralha a atribuição de jogadores do próprio jogo (**R-04**).

### (4) "8BitDo só conecta manualmente" — **SEM CAUSA CONFIRMADA**
Nenhum achado fecha o caminho. O único item adjacente é **R-24** (`vigia1-conta-zumbi-como-sessao-viva`), que explica por que a **remediação automática** — o restart do `bluetooth.service` quando ele entra no estado de recusa em loop ("Refusing connection: unknown device", 47 min medidos em 21/07) — **nunca dispara** enquanto houver um zumbi contando como sessão viva; isso mantém o 8BitDo dependente de gesto manual **depois** que o serviço adoece, mas não explica a reconexão que nunca parte sozinha em estado saudável.

**Falta investigar (ordem proposta, tudo medição, zero código):**
1. **Quem deve iniciar a reconexão:** ler o atributo SDP `HIDReconnectInitiate` (0x0205) no `cache/<dispositivo>` do 8BitDo e comparar com o do Pro Nintendo e o do DualSense. Se for `false`, quem tem de paginar é o **host** — e aí a pergunta vira "o BlueZ tenta?".
2. **Estado do bond:** `Trusted`, `Blocked`, `ReconnectMode` no `info` do 8BitDo, e se o `cache/` dele tem `[ServiceRecords]` (o zumbi de 23/07 é exatamente a ausência disso). Comparar com um bond que reconecta sozinho.
3. **Page scan do adaptador:** confirmar que o dongle fica `connectable`/em page scan após o wake e após o `link policy` do `hefesto-bt-active` (que hoje remove SNIFF) — capturar `btmon` durante uma tentativa de reconexão pelo botão do 8BitDo.
4. **A/B do doc de arqueologia (`docs/process/estudos/2026-07-23-arqueologia-8bitdo-bt`)**, que já tem plano de 7 passos e a hipótese "nome Nintendo" marcada como INDETERMINADA (nome + no-sniff entraram no mesmo commit). Preparação já anotada: **parar o `watchdog.timer` antes**, para o watchdog não poluir o experimento.
5. Só depois disso decidir se existe correção de software no Hefesto (ex.: agente D-Bus que chama `Connect()` em bond conhecido ao ver page/advertising) ou se é característica do firmware do controle.

### (5) "bugs não notados, conflitos entre abas, estado 'armado' que nunca é liberado" — **EXPLICADA**
- **Estado armado:** **R-19** — a trava manual é global, **sem TTL**, e o botão "Desligar" da aba Gatilhos **re-arma** em vez de soltar; passear pelos modos (live-preview) já arma; nada na GUI mostra que a troca automática está pausada nem oferece como liberar.
- **Conflitos entre abas:** **R-08** (o draft e o nome do perfil ativo congelam no boot; abas editam o perfil errado; recargas pisam no editor), **R-16** (o alvo de edição muda sozinho a 2 Hz), **R-10** (salvar "Navegacao" sobrescreve "Navegação" **sem aviso**, porque a guarda compara nome de exibição e o arquivo é por slug).
- **Bugs não notados:** **R-18** (`apply_draft` sempre responde `ok`, mesmo com **zero** seções aplicadas; gatilho/rumble sem nenhum DualSense conectado viram no-op com toast de sucesso), **R-15** ("Renumerar agora" no-op respondendo "4 controle(s) renumerado(s)"), **R-09** ("Novo perfil" nasce clonando o selecionado, inclusive `suppress_desktop_emulation`), **R-22** (o poll loop congela por segundos com I/O bloqueante no event loop — input dos 4 jogadores e a GUI param, sem nenhuma mensagem).

---

## 5. CONTRADIÇÕES ENTRE ACHADOS (e a decisão adotada)

1. **Retry do modo × não gravar `_current_profile`** — `mode-do-perfil-pulado-sem-retry` e `modo-de-perfil-pulado-para-sempre-pelo-lock-manual` divergem sobre o mecanismo; a variante "não marcar `_current_profile`" faria `_activate` rodar ~60× em 30 s, re-escrevendo gatilhos/LEDs e `reset_output_overrides` a 2 Hz — exatamente o flap que MISC-08 evita. **Decisão (R-03):** commitar `_current_profile` e agendar **uma** re-ativação/pendência drenada no poll loop.
2. **Retry × "nunca trocar máscara depois do launch"** — `profile-switch-mente-modo-descartado` argumenta que qualquer retry assíncrono pode trocar a máscara com o jogo **já aberto** (recriar vpad mid-game invalida handles). **Decisão:** o retry de R-03 é **gated** pelo gate de jogo de R-04; e o caminho principal deixa de precisar dele porque o modo passa a ser aplicado **no launch**, antes do jogo executar.
3. **`display_authority == "game"` × leitura crua de `wm_class`** — `perfil-troca-mascara-com-jogo-aberto` quer o sinal sticky; `perfil-catchall-desliga-gamepad-em-jogo` mostra que ele é sticky por 30 s e congelaria a reversão legítima. **Decisão:** dois sinais para duas decisões — **operação destrutiva** (recriar/parar vpad) usa o sinal **sticky** (fail-safe: na dúvida, não destrói); **reversão de modo para desktop** usa a leitura **crua** da janela em foco.
4. **Quem alimenta quem na numeração** — `externos-consomem-numero-de-jogador` quer o provider lendo `coop.player_indexes()`; `coop-e-slot-brigam-pelo-mesmo-led`/`coop-vs-slot-numeracao` querem o co-op lendo `slot_for`. Ler dos dois lados mantém **dois escritores**. **Decisão (R-13):** o **registry é a autoridade de exibição**; o co-op **publica** sua ordem nele (pin) e depois **todos leem o registry**; `player_index` fica só como alocação de vpad (mexer nele = `-EEXIST` no uhid).
5. **Camada do co-op × `reset_output_overrides`** — `reassert-sobrescreve-player-led-coop` propõe override por-uniq para o co-op, mas `manager.apply` **substitui o mapa inteiro** a cada ativação (C5). **Decisão:** R-13 e R-20 são um **par**; camadas com dono, e `reset_output_overrides` só substitui a camada do perfil.
6. **Gate do co-op** — a proposta antiga de exigir "2+ controles" em `should_be_active()` conflita com PERF-MULTI-CONTROLLER-01 (enumerar `/dev/input` por tick) e faria o co-op piscar a cada blip de link. **Decisão (R-13 §4):** corrigir o **efeito** (não escrever LED sem secundário), não o gate.
7. **TTL na trava manual** — `override-manual-armado-sem-expiracao` mostra que um TTL cego reabre o "perfil eterno" da Onda U (U3/U4/U9/U11). **Decisão (R-19):** supressão **alvejada** (bloqueia reaplicar o mesmo perfil, libera trocar para outro), sem TTL.
8. **Estreitar `trigger.reset`** — `aba-gatilhos-arma-trava-sem-botao-de-soltar` alerta que limitar o clear à categoria "trigger" quebra contrato **deliberado e testado** (`test_onda_u_trava_por_categoria.py:113-121`). **Decisão:** manter o clear total; o que muda é a GUI passar a **usar** o `trigger.reset` em vez de mandar outro `trigger.set`.
9. **R-19 torna a exceção F2 de R-01 desnecessária** — não é conflito, é ordem: aplicar **R-01 primeiro** (fecha o sangramento hoje) e, ao concluir R-19, **remover** o ramo F2 em vez de mantê-lo remendado.
10. **`status` do `apply_draft`** — a proposta de trocar para `"partial"`/`"failed"` faria a GUI atual imprimir "daemon offline". **Decisão (R-18):** manter `status:"ok"` e adicionar `falhas`/`aplicado_em` (aditivo).
11. **Allowlist × dedup** — R-05 empurra `IGNORE` para os `.env` por appid; R-06 exige `.env` **sem** `IGNORE` para os appids da allowlist. **Decisão:** a allowlist é opt-in explícito e **vence** para os appids listados; para todos os outros, vale R-05.
12. **`coop_local` para MatchAny** — descartado explicitamente: mais um catch-all agravaria R-01. **Decisão (R-12):** alvo real ou sentinel `{"type":"manual"}`.
13. **Cache sysfs × recuperação anti-hidraw** — R-21 melhora tráfego mas remove a única recuperação contra escritor por hidraw. **Decisão:** só aplicar **junto** com a decisão sobre `verify=True`/repaint lento; caso contrário, **não aplicar**.
14. **Expiração de slot × testes existentes** — `test_identity_registry.py:109-113,227-238` **assertam** o comportamento que R-15 remove. **Decisão:** trocar os testes de propósito, com o par novo (estabilidade intra-boot + renumeração por `boot_id`).
15. **`renomear-perfil-cria-arquivo-novo`** depende da ordem alfabética do filename como desempate — R-01 substitui esse desempate por especificidade. **Decisão:** implementar R-01 **antes** de R-10, e o rename passa a ser corrigido pela migração explícita, não pela ordem do `glob`.
