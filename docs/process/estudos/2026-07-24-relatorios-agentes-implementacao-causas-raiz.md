# 2026-07-24 — Relatórios dos agentes: implementação das causas-raiz R-03..R-22

Materialização dos relatórios técnicos que as 4 ondas de agentes produziram ao
implementar as 9 causas-raiz restantes da auditoria (ver a sprint
`2026-07-23-sprint-gui-perfis-por-controle.md` para o plano; este doc guarda o
que os agentes DECIDIRAM e o que ficou pendente, que o resumo da sprint não
cabe).

Cada agente: rodou a suíte antes, implementou a raiz, escreveu testes que pegam
a regressão (revert/restore verificado), deixou o working tree para integração.
A verificação final adversarial morreu de erro de conexão — a integração foi
verificada manualmente depois (4719 testes verdes, mypy limpo).

>  Este doc preserva os relatórios BRUTOS dos agentes. Onde eles citam
> "pendências" ou "decisões diferentes do plano", isso é o roteiro para a
> próxima sessão.

---

## Onda 1 — R-10/R-12, R-14/R-15, R-22 (arquivos disjuntos)

### Agente 1

Trabalho concluído. Relatório:

## O que mudou, por arquivo

**`/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/profiles/slug.py`** (R-10)
- `mesmo_slug(a, b)` e `find_by_slug(name, candidates) -> objeto | None`, ambos tolerantes a `ValueError` do `slugify` (o editor chama a cada tecla). `find_by_slug` devolve o **objeto**, não o nome, porque o diálogo tem de citar o perfil realmente afetado ("Navegação"), não o digitado ("Navegacao").

**`.../app/actions/profiles_actions.py`** (R-10 + R-12)
- `on_profile_save`: as duas guardas (sobrescrita e downgrade→`MatchAny`) passaram a resolver por **slug** e a nomear a vítima real. `editando_em_lugar` exige `not _new_profile and not duplicando` — era por aí que "Novo perfil" chamado "Navegacao" comia `navegacao.json` com uma linha selecionada.
- **Rename**: slug novo ≠ slug do selecionado → pergunta "Renomear" × "Salvar como cópia" × Cancelar; em "Renomear", `delete_profile(antigo)` **só depois** do `save_profile` OK, e migração do marker de perfil ativo (`profile_switch(novo)` quando o ativo era o antigo). Diálogo em `dialogo_renomear_ou_copiar` no próprio módulo (não em `gui_dialogs.py`, que é do R-11), com `_prompt_rename_or_copy` como ponto único de override.
- R-12: opção **"Jogo da Steam"** no seletor (`_RADIO_IDS`/`_APLICA_A_ITEMS`), campo livre compartilhado com placeholder/tooltip trocados por escolha, `_prefill_steam_appid()` (lê `window_detect_last_class` do `daemon.state_full`, só preenche campo vazio, best-effort assíncrono), `_populate_editor` usa `simple_extra` (round-trip sem duplicar o prefixo `steam_app_`), `_refresh_preview` mostra a frase de gente em vez de `<preview indisponível>`, `_humanize_profile_error` repassa `MENSAGENS_DE_GENTE`.
- `_match_label` aceita o **objeto** `profile.match` (contrato antigo por string preservado) e devolve `LABEL_SO_MANUAL` = "Só manual (nunca ativa sozinho)" para `criteria` vazio.

**`.../profiles/simple_match.py`** (R-12)
- `from_simple_choice("steam_game", appid|steam_app_appid)` → `MatchCriteria(window_class=["steam_app_<id>"])`; `detect_simple_preset`/`simple_extra`/`normalize_appid`.
- Campo obrigatório vazio **levanta `ValueError`** com frase de gente (antes degradava para `MatchAny` em silêncio). Leitura continua tolerante (`detect_simple_preset(MatchCriteria())` → `None`), conforme o risco anotado no plano.
- Removido o `.lower()` de `"game"`: o matcher compara com o basename **cru** de `/proc/PID/exe` (`Cyberpunk2077.exe`), então o helper garantia o não-casamento.

**`.../cli/cmd_profile.py`** (R-10 + extra)
- `_guarda_slug()` em `create`, `apply --save` e `save --from-active`, com `--force`. Antes `profile create "Navegacao"` apagava a "Navegação" e imprimia "perfil criado" em verde.
- **Extra deliberado**: `cmd_save` reinjeta `payload["controllers"] = source.controllers` — é o mesmo defeito R-09 (`cli/cmd_profile.py:254-258` no plano) que ficou sem dono; o clone densificado virava `lightbar:[0,0,0]` e apagava a lightbar do controle.

**`assets/profiles_default/coop_local.json`** (R-12 item 4)
- `criteria` vazio (inalcançável) → `window_title_regex` de jogos de co-op local, idioma dos presets de gênero (`acao`/`aventura`/`corrida`). Prioridade **45**: abaixo de `Navegação` (50, porque o título da janela do *cliente* Steam pode citar um jogo de co-op) e muito abaixo de `sackboy_nativo` (80). **Não** virou `MatchAny` (contradição 12 do plano).

## Prova de que os testes pegam a regressão

Seis micro-reverts cirúrgicos (backup/restore por arquivo — `git checkout` global era proibido, outros agentes estão com o working tree sujo):

| revert | efeito | testes que caem |
|---|---|---|
| A: guarda volta a `_find_cached_profile` (nome de exibição) | 2 | `test_navegacao_sem_acento_pergunta_nomeando_a_vitima`, `test_downgrade_para_any_pergunta_mesmo_com_nome_sem_acento` |
| B: bloco de rename removido | 3 | `test_renomear_apaga_o_antigo_depois_do_save`, `test_cancelar_o_rename_nao_grava_nada`, `test_marker_do_perfil_ativo_acompanha_o_rename` |
| C: `from_simple_choice` volta a `MatchAny`+`.lower()`, sem `steam_game` | 18 | os 4 arquivos de R-12 + os 2 existentes atualizados |
| D: `_match_label` sem o ramo de criteria vazio | 1 | `test_criteria_vazio_diz_so_manual` |
| E: `coop_local.json` do `HEAD` | 3 | `test_tem_alvo_de_verdade`, `test_nao_virou_catch_all`, `test_casa_com_jogo_de_coop_pelo_titulo` |
| F: `_guarda_slug` no-op + clone denso | 3 | os 3 do CLI |

Todos restaurados; os 49 testes novos voltaram a passar.

## Testes

Novos: `tests/unit/test_r10_slug_e_rename.py` (15), `tests/unit/test_r10_cli_guarda_slug.py` (6), `tests/unit/test_r12_editor_simples_jogo_steam.py` (19), `tests/unit/test_r12_editor_simples_gui.py` (9). Os de GUI têm `pytest.importorskip("gi")` no topo + stubs de `gi.repository`.

Contratos mudados **de propósito** (documentado no próprio teste): `test_simple_match.py` (`..._normalizado_para_lowercase` → `..._preserva_as_maiusculas`; `..._retorna_match_any` → `..._levanta`) e `test_profile_editor_roundtrip.py` (idem + `test_steam_game_roundtrip` novo). Os testes antigos **congelavam os defeitos**.

## Resultado

- Suíte completa: **4637 passed, 0 failed** (linha de base 4561).
- `ruff check` nos meus arquivos: **All checks passed**.
- `ruff check src/ tests/` global: **1 erro RUF002 em `tests/unit/test_auto_player_colors.py:201`** (`×` numa docstring) — arquivo de **outro agente** (R-14), não toquei.

## Decisões diferentes do plano (com motivo)

1. **Sentinel `{"type":"manual"}` descartado** — exige `profiles/schema.py`, que está com o agente do R-14 (`schema.py:168`, `auto_player_colors`). Usei a alternativa explicitamente sancionada pelo plano ("alvo real").
2. ** Migração da cópia em `~/.config` NÃO feita** — mora em `profiles/loader.py`, fora da minha lista. **Isto importa para a máquina dela**: `~/.config/hefesto-dualsense4unix/profiles/coop_local.json` (14/07, criteria vazio) está no `.seeded_presets`, então a semeadura nunca o sobrescreve e o preset continua inalcançável lá. Spec pronta para quem for dono do `loader.py`: one-shot no molde de `migrate_game_presets_to_xbox`, marker `.coop_local_target_migrated`, conservadora — só reescreve `match` se ele estiver **exatamente** em `{"type":"criteria"}` com os três campos vazios/ausentes e o `mode.kind == "gamepad"` com `coop: true` (isto é: intocado), copiando `match` e `priority` do asset; qualquer edição da usuária = não toca. Chamada em `_maybe_seed_presets`, dentro do `contextlib.suppress` como as outras duas.
3. **`audit_profiles` / `doctor.sh` listando "perfis inalcançáveis" NÃO feito** — `loader.py` e `scripts/doctor.sh` fora da lista. A visibilidade ficou no que eu controlo: a coluna "Quando usar" agora diz "Só manual (nunca ativa sozinho)".
4. **`main.glade` não tocado** (fora da lista): em vez de reescrever o rótulo "Nome do jogo:", troco **placeholder + tooltip** por escolha em `_on_aplica_a_changed`. O tooltip de "Jogo específico" agora diz honestamente "basename de /proc/PID/exe … em Proton é o binário do wine — use 'Jogo da Steam'".
5. **`gui_dialogs.py` não tocado** (R-11 está nele): o diálogo de rename mora em `profiles_actions.py`, com a mesma assinatura/estilo (parent + strings, `run/destroy`, tema aplicado, sem IPC).
6. **Case-insensitive no matcher não feito** — a cura completa é em `MatchCriteria.matches` (`schema.py`, ocupado). Fiz a metade que é minha e que era o dano garantido: parar de corromper o dado com `.lower()`. Fica registrado como pendência de uma linha para quem tocar o schema.
7. **`_find_cached_profile` não foi afrouxado** (ele resolve a base do editor), conforme o plano manda.

### Agente 2

**R-14 e R-15 implementados. Suíte: 4645 passed (baseline 4561, 0 falhas). `ruff check src/ tests/`: All checks passed. Nada commitado.**

## O que mudou, por arquivo

**`/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/identity.py`**
- **R-14 §1**: `make_auto_output_provider` chama `slot_for(uniq)` **antes** de qualquer flag — atribuir número é identidade, não aparência. Antes o early-return deixava o DualSense fora do registro com `auto_player_colors:false` (o `fps.json` dela), e o piso que os externos leem (`_ds_reserve`) mentia.
- **R-14 §2 (lado daemon)**: estado do automático desdobrado em dois eixos — `_auto_colors` (paleta) e `_auto_numbers` (padrão de player-LED / número). `configure(enabled=…)` mapeia o campo **antigo** do perfil só para COR; novo `configure(numbers=…)` e propriedade `auto_numbers_enabled` (default `True` = migração compatível: perfil salvo com `auto_player_colors:false` perde a paleta, nunca a numeração). O provider emite `led` e `player_leds` **separadamente**; nenhum eixo ligado ⇒ `None` (sem opinião, merge cai no global).
- **R-15 §1**: removidos o campo `_saw_connected` e o ramo de expiração por "sessão esvaziou" em `sync_connected` (que agora só reconcilia + persiste); `mark_disconnected` idem. Novo `snapshot_connected()` — o `_connected` era escrito e nunca lido.
- Docstrings de módulo/métodos reescritas com o porquê medido (assimetria com o registro dos externos, dependência da ordem de wake, janela de duplicata via `_ds_reserve`).

**`.../daemon/subsystems/external_identity.py`**
- **R-14 §1**: laço de **atribuição** (`slot_for` para todo o inventário) movido para **antes** do gate do automático; o laço de escrita consome a lista já atribuída.
- **R-14 §2**: `_auto_player_colors_enabled` → `_auto_numbers_enabled` (lê `auto_numbers_enabled`, fallback `True`). O que este tick escreve é `apply_player_number` — número, não cor; gateá-lo pelo flag de cor era a raiz de "auto OFF congela a numeração dos externos".
- **R-15 §2**: `ExternalIdentityRegistry.snapshot_connected()`.
- `_ds_reserve` (R-13) **intocado**.

**`.../daemon/ipc_handlers.py`**
- **R-15 §2**: `_renumber_locked` ordena por `(está_offline, slot_antigo)` — conectados descem para 1..N, reservas ausentes vão para N+1..M no mesmo mapping (reserva **não** é dropada, D2 preservado). Novo helper `_connected_keys` com degradação para registro sem `snapshot_connected` (dublê antigo → tudo conta como conectado, comportamento do HEAD).
- **R-15 §3**: `renumbered` passa a conter **só as chaves que mudaram**; um no-op responde `{}` e o handler pula reassert/repaint. A GUI (`home_actions`, que conta as chaves) já tinha o ramo "Numeração já estava compacta" — nenhuma mudança lá foi necessária.

**`.../app/actions/lightbar_actions.py`**
- **R-14 §3**: novo `_uniqs_conectados()` (lê o mapa `_target_uniq_by_index` que a aba Status mantém do `state_full`). Em "Todos" com conectados conhecidos, cor e player-LED viram **override por-MAC** em cada um (override vence a camada automática — D5) e o automático **não** é desligado. Ordem deliberada e comentada: overrides gravados **antes** do global, porque `with_controller_leds` só guarda o que **diverge** do global (se o global já tivesse o valor novo, o override seria podado e a paleta voltaria a vencer).
- IPC: novos `_enviar_led_em_todos` e `_enviar_player_leds` — "Todos" manda um pedido **por MAC** (`led_set`/`player_leds_set` com `uniq`), sem curto-circuito e com sucesso só se todos aceitarem. Usado por `on_lightbar_apply`, `on_lightbar_off` e pelos três caminhos de player-LED.
- Brilho continua global (escala a paleta, D11 — nunca disputou com o auto).

## Prova de que os testes pegam a regressão (revert → falha → restore → passa)

| Fix revertido | Testes que falharam |
|---|---|
| expiração por sessão esvaziada reintroduzida em `sync_connected` | `test_identity_registry.py::test_sessao_esvaziar_nao_expira_dentro_do_boot`, `::test_sessao_esvaziada_sobrevive_ao_restart_e_so_o_boot_renumera` (2 failed) |
| plano do renumber sem separar conectados + relatório inteiro | `test_identity_numeracao_r14_r15.py::test_conectados_descem_para_1_a_n_e_reserva_vai_para_o_fim`, `::test_ja_compacto_responde_vazio`, `test_identity_renumber_ipc.py::test_compacta_1_a_n_preservando_ordem`, `::test_ja_compacto_e_no_op_idempotente` (4 failed) |
| provider com early-return do flag + campos acoplados | `test_auto_player_colors.py::test_cor_desligada_mantem_numero_e_atribui_slot`, `::test_numero_desligado_mantem_a_cor`, `::test_os_dois_eixos_desligados_devolvem_none`, `::test_resolved_player_leds_for_devolve_o_padrao_do_slot`, `test_identity_numeracao_r14_r15.py::test_dualsense_ganha_slot_com_a_cor_desligada` (5 failed) |
| externos gateados na cor + atribuição depois do gate | `test_external_identity.py::test_auto_numbers_off_para_de_escrever_e_limpa_cache`, `::test_auto_colors_off_nao_congela_a_numeracao_dos_externos`, `::test_numeracao_off_ainda_atribui_o_slot` (3 failed) |
| GUI sem o caminho por-MAC (D4 sempre) | 6 dos 8 casos de `test_lightbar_todos_por_mac_r14.py` |

Após restaurar tudo: 157 passed nos arquivos afetados; suíte completa verde.

## Testes: novos e trocados de propósito

Novos: `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/tests/unit/test_identity_numeracao_r14_r15.py` (5) e `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/tests/unit/test_lightbar_todos_por_mac_r14.py` (8, com pin `gi`/Gdk 3.0 — o `importorskip` sozinho envenenava o processo com Gdk 4.0).

Contratos trocados **de propósito**, cada um com o porquê no docstring:
- `test_identity_registry.py`: `test_sync_expira_ao_esvaziar` → `test_sessao_esvaziar_nao_expira_dentro_do_boot` (estabilidade intra-boot, os dois somem e voltam em ordem invertida); `test_expiracao_regrava_o_arquivo_vazio` → `test_sessao_esvaziada_sobrevive_ao_restart_...` + `test_boot_novo_renumera_do_1` (renumeração por `boot_id`).
- `test_identity_renumber_ipc.py`: `renumbered` só com o que mudou; `test_ja_compacto_e_no_op_idempotente` agora exige `{}` na segunda passagem.
- `test_auto_player_colors.py`: `test_auto_desligado_devolve_none` → trio cor/número/ambos + o ponta-a-ponta `resolved_player_leds_for`.
- `test_external_identity.py`: `test_auto_player_colors_off_...` → `test_auto_numbers_off_...` (mesmo invariante NUMA-03c, no eixo certo) + dois casos novos.

## O que decidi diferente do plano (e por quê)

1. **R-14 §2 só no lado daemon.** Desdobrar o flag no *schema* exigiria `profiles/schema.py`, `app/draft_config.py` e `profiles/manager.py` — arquivos de outros agentes. Implementei os dois eixos no registro (com `configure(numbers=…)` pronto) e mapeei o campo antigo para COR; `auto_numbers` nasce `True`, que é a "migração de default compatível" que o plano pede. **Pendente para quem for dono do schema**: expor `auto_player_numbers` no perfil/GUI e passá-lo em `manager.apply` → `registry.configure(numbers=…)`.
2. **R-14 §4 (parar o broadcast denso de `player_leds` em `manager.py:214`) não foi feito** — `profiles/manager.py` não é meu.
3. **R-14 §3 com fallback explícito.** Quando a GUI ainda não sabe quem está conectado (nenhum tick do daemon / host parcial), o D4 antigo permanece — sem alvo não existe override e a cor única seria invisível. Está documentado no código como caminho degradado e coberto por teste, e é o que mantém os 29 casos de `test_lightbar_auto_colors.py` intactos.
4. **Canto conhecido, deliberado**: se a cor escolhida em "Todos" for *idêntica* à global vigente, `with_controller_leds` poda o override (regra COR-04 já existente em `draft_config.py`, arquivo de outro agente) e a paleta segue vencendo **na persistência** — a escrita ao vivo continua indo por MAC e vence. Corrigir isso exigiria um `with_controller_leds(force_fields=…)` em `draft_config.py`.
5. **`daemon/lifecycle.py:2167-2169`** (citado na lista do R-15): inspecionado — o único ponto que fala com o registro é `sync_connected(uniqs)` na linha 1915, e ele já envia só os conectados. Nada a mudar (e não é meu arquivo).

### Agente 3

**R-22 implementado.** A leitura da calibração 0x05 saiu da thread do event loop.

## O que mudou por arquivo

**`/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/coop.py`** (+200/-14)

- `calibration_cache(daemon)` (módulo, público, no `__all__`): cache por MAC vivo em `daemon._calibration_by_uniq` — o nome que o plano especifica, para que o lado do P1 (`gamepad.read_primary_calibration`, arquivo de outro agente) adote o mesmo dicionário sem repagar a leitura. Chave = MAC porque o 0x05 é imutável por unidade. Daemon que recusa `setattr` degrada para "sem cache, mas também sem I/O no loop".
- `_calibration_pronta(identity) -> tuple[bool, bytes | None]`: substitui a leitura inline. HIT devolve na hora; MISS agenda a leitura via `broker_call_nonblocking` (executor dedicado do broker, 1 worker FIFO — o mesmo despachante que `hide`/`restore` do co-op já usam, nunca o pool `hefesto-hid` banido pelo HANG-01) e devolve `(False, None)` = "adie".
- `_read_player_calibration` vira a vista fail-safe (adiamento → `None`), preservando o contrato que `tests/unit/test_motion_wiring.py:249-250` já assertava.
- `_fill_calibration`: roda na thread do executor; publica no cache sem lock (`dict.__setitem__`/`set.add` atômicos sob o GIL; o leitor só faz `get`/`in`).
- `_promote_player`: consome o cache e **adia** a promoção (jogador segue sem vpad, exatamente como no grab pendente) em vez de nascer com calibração errada. `_promote_pending` já roda a cada `forward_all`, então a retentativa é o tick seguinte.
- `_prefetch_calibration` chamado no `_spawn_player`: esquenta o cache assim que o jogador é registrado — como o grab normalmente só confirma um tick depois, na prática o adiamento nem acontece.
- `_CALIB_PRAZO_S = 2.0`: teto do adiamento. Estourou, o vpad nasce com o 0x05 canônico + `logger.warning("coop_calibracao_prazo_estourado")`. Ninguém fica sem controle esperando rádio mudo.
- `_teardown_player`: limpa `_calib_prazo`/`_calib_sem_leitura` da identidade (falha típica é transitória — BT ocioso, broker reiniciando; replug merece tentativa nova). O cache **positivo** fica.

**`/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/tests/unit/test_coop_calibracao_sem_io_no_loop.py`** (novo, 10 testes).

## Prova de que o teste pega a regressão

Com `coop.py` restaurado de `HEAD` (fix revertido), rodando o arquivo novo: **7 failed, 3 passed**. O teste-cabeça falha com a mensagem certa:

```
>       assert gasto < 0.3, f"promoção bloqueou o event loop por {gasto:.2f}s"
E       AssertionError: promoção bloqueou o event loop por 1.00s
E       assert 1.0010095340039697 < 0.3
```

Restaurado o fix: **10 passed**. Os 3 que passam sem o fix são os fail-safe que já valiam antes (`path:` não toca no backend, off-loop continua síncrono, resolvido-sem-bytes) — estão lá como guarda-corpo, não como prova.

O teste também prova a *thread*: `read_calibration` é anotada com `threading.current_thread().name` e o assert exige que seja diferente da thread do loop e comece com o prefixo do executor do broker.

## Suíte e ruff

- `ruff check` nos **meus** dois arquivos: limpo. `mypy` no `coop.py`: limpo (por isso `_calibration_pronta` devolve tupla tipada em vez de sentinela `object()` — a sentinela obrigaria um `type: ignore` no `make_virtual_pad`).
- `ruff check src/ tests/` acusa **6 erros, todos fora dos meus arquivos** (`app/actions/profiles_actions.py`: 1 F401 + 3 RUF002; `cli/cmd_profile.py`: 2 F401) — trabalho em voo de outro agente (R-10/R-12).
- Suíte completa: **linha de base era 4561 passed**. Agora há falhas em `test_auto_player_colors.py`, `test_corretora_final_cross_cutting_20260720.py`, `test_external_identity.py`, `test_identity_registry.py`, `test_identity_renumber_ipc.py`, `test_profile_editor_roundtrip.py`, `test_simple_match.py` — **nenhuma minha**. Verificado por A/B: rodando esses arquivos com `coop.py` no estado `HEAD` e com o meu fix, o conjunto de falhas é o mesmo (a contagem oscila entre execuções porque os outros agentes estão editando os arquivos durante a corrida).
- Fatia que me pertence: `pytest -k "coop or motion or calib or broker or gamepad or vpad or uhid"` → **905 passed**.

## Decisões diferentes do plano (e por quê)

1. **O preenchimento não foi para `connect`/hotplug em `lifecycle.py`/`connection.py`** — esses arquivos não estão na minha lista (outro agente está neles). Agendar do próprio `coop.py` via `broker_call_nonblocking` atinge o mesmo invariante (a leitura roda fora do loop) e é reversível: quando o lado do P1 for feito, basta ele preencher `calibration_cache(daemon)` no caminho de `connect` e o co-op passa a ter HIT já no primeiro tick. Deixei `calibration_cache` público exatamente para isso.
2. **O plano diz "miss devolve `None` (canônico) e agenda o preenchimento". Não fiz assim.** `None` no miss significaria que todo vpad de co-op nasceria com a calibração canônica no primeiro tick e **nunca mais** teria a da unidade — o 0x05 é carimbado no blueprint na *criação* do uhid e não é retrofitável, e recriar o vpad depois é a operação destrutiva que o plano proíbe (contradição 2/3). Isso trocaria o congelamento do loop por drift permanente de gyro nos 4 controles, matando o GYRO-01. Em vez disso a promoção **adia um tick** (o jogador já estava invisível ao jogo — mesma janela do grab pendente) e o `_CALIB_PRAZO_S` garante o fail-safe que o plano pedia: passou de 2 s, nasce canônico e loga.
3. **Cache negativo não vai para o dicionário do daemon.** Lá só entra o que é imutável de verdade; a falha (EIO de BT ocioso, CRC corrompido) fica numa marca por-manager que o teardown limpa — senão um blip de rádio condenaria aquele controle a gyro canônico pelo resto da vida do daemon.

Não toquei em `should_be_active()` e o guard do R-13 item 4 (`if not self._players`) continua intacto — e não é afetado pelo adiamento, porque o jogador adiado já está registrado em `_players` (o player-LED sai no mesmo ciclo de `sync`, como antes).


---

## Onda 2 — R-03 (lock manual x seções do perfil)

R-03 implementado. Suíte completa verde (4659 passed, +14 novos sobre a linha de base de 4645), `ruff check src/ tests/` limpo e `mypy` (gate rígido do CI) sem erros.

## O que mudou, por arquivo

**`src/hefesto_dualsense4unix/daemon/lifecycle.py`** (núcleo)
- Vocabulário único de retorno dos appliers de perfil: `APLICADO`, `ADIADO_LOCK_MANUAL`, `IGNORADO_CATCH_ALL`, `IGNORADO_JANELA_DE_JOGO`, `FALHOU`. Antes todos devolviam `None` — a seção descartada não deixava rastro em lugar nenhum.
- `ModoAdiado` (dataclass): pendência **única** `(mode, profile, profile_name, origin, carimbo_manual, nao_antes_de)`, guardada em `Daemon._mode_pendente`. Sempre sobrescrita, nunca enfileirada.
- Os 4 appliers (`apply_profile_mode`, `apply_profile_suppression`, `apply_profile_mouse`, `apply_profile_rumble_policy`) recebem `origin=` por keyword (default conservador `"autoswitch"` — quem esquecer respeita o lock) e devolvem o estado da seção. **Preservei integralmente as guardas do R-02** (catch-all não reverte; janela de jogo congela reversão; `profile=` por keyword) e o 3º parâmetro `Profile` do R-01 no autoswitch.
- `_furar_lock_de_emulacao(secao)`: `origin="manual"` (profile.switch/PS+D-pad) fura o lock **e consome o carimbo** (`_emu_manual_ts = -inf`) — senão a máscara que o próprio perfil acabou de pôr travaria o perfil seguinte por mais 30 s.
- `_agendar_modo_adiado` + `_drenar_modo_pendente` + `_modo_seria_destrutivo`. O dreno tem 4 guardas: lock ainda vigente → espera; carimbo mudou (gesto novo dela) → descarta; perfil ativo mudou → descarta; jogo com `display_authority == "game"` **e** aplicação destrutiva → segura até a borda (log 1x, sem flood a 1 Hz).
- `_poll_loop`: dreno a ~1 Hz, **depois** do `_sync_game_signal` (a guarda precisa da autoridade deste tick) e **antes** do gate de conexão (um blip de BT não pode matar o modo do perfil).

**`profiles/manager.py`** — `activate(..., origin=, relatorio=)` propaga o origin até os appliers e preenche `relatorio` com `seção → estado`; `apply_emulation` idem e devolve o dict; helper `_estado_da_secao` (applier de dublê que devolve `None` conta como "aplicado" — dublê não fabrica adiamento). Tipos dos appliers viraram `Callable[..., object]`.

**`profiles/autoswitch.py`** — passa `relatorio=` e loga `adiado=[...]` no `profile_autoswitch`; commit de `_current_profile` **preservado** (contradição nº 1).

**`daemon/ipc_handlers.py`** (só `profile.switch`) — resposta aditiva: `mode_aplicado`, `secoes`, e `motivo`/`expira_em_sec` quando não aplicou. `active_profile` intacto (GUI antiga não quebra). O toast da GUI é R-18/R-19 — `app/` não está na minha lista.

**`daemon/protocols.py`** (fora da lista, ver ressalvas) — 3 assinaturas de applier atualizadas; sem isso `mypy --strict`, que é gate rígido no CI, falharia com o retorno `str` × `None`.

## Prova de que os testes pegam a regressão

`tests/unit/test_r03_lock_manual_adia_modo.py` (novo, 14 testes). Reverti cada pedaço do fix, rodei, restaurei:

| Revert | Falhas |
|---|---|
| A — lock volta a descartar em silêncio e devolver "aplicado" | **13 de 14** |
| B — poll loop sem a chamada do dreno | `test_poll_loop_drena_a_pendencia` |
| C — dreno sem o gate de jogo | `test_dreno_nao_troca_mascara_com_o_jogo_na_autoridade` |
| D — dreno sem as guardas 2 e 3 | `test_dreno_descarta_apos_gesto_manual_novo`, `test_dreno_descarta_quando_o_perfil_ativo_mudou` |
| E+F — manager sem `origin=` e IPC sem a verdade | `test_ativacao_manual_aplica_o_modo_mesmo_com_a_mascara_recem_mexida`, `test_profile_switch_responde_a_verdade` |

Restaurado: 14/14 passam. O teste do poll loop é integração real (`Daemon.run()` com `FakeController`), não mock de fiação.

## Decisões diferentes/mais explícitas que o plano (com motivo)

1. **O gate de jogo do dreno é meu, não do R-04.** O plano diz "gated pelo gate de R-04"; R-04 não existe ainda e `apply_profile_mode` é território dele. Implementei o gate **dentro do dreno** (`display_authority == "game"` sticky + `_modo_seria_destrutivo`), sem tocar no corpo do applier. Destrutivo = parar/recriar vpad (`kind` None/desktop/native com algo de pé; `gamepad` só com flavor diferente); mesmo flavor e co-op passam mesmo com jogo aberto — senão o gate viraria "o perfil nunca é aplicado", que é a própria queixa.
2. **Pendência só para `mode`** (como o plano manda). Mouse/supressão/rumble **reportam** `adiado_lock_manual` (relatório + IPC + journal) mas não têm retry: um caminho assíncrono por eixo multiplicaria as escritas sem gesto dela. Documentado no docstring de `ModoAdiado`.
3. **`relatorio` como out-param** em vez de mudar o tipo de retorno de `activate` (que quebraria todos os callers) ou de guardar estado no manager (a hotkey ativa de outra thread — o relatório de uma ativação seria lido como o de outra).
4. **Gesto manual novo mata a pendência** (não só adia): aplicar o modo do perfil 30 s depois de ela ter mexido na máscara de novo desrespeitaria a escolha mais recente.
5. **Renomeei `expira_em` → `expira_em_sec`** na resposta IPC (unidade explícita, padrão dos outros campos do daemon).

## Arquivos fora da minha lista que precisei tocar (todos documentados no código com "R-03")

- `daemon/protocols.py` — motivo acima (mypy é gate).
- 8 testes existentes, por mudança **deliberada** de contrato, sem afrouxar asserção nenhuma: `test_profile_mouse_section.py`, `test_profile_rumble_policy.py`, `test_ipc_profile_switch_propaga_teclado.py` (dublês de applier ganham `origin=`), `test_profile_activate_origin.py`, `test_onda_u_trava_por_categoria.py` (dublês de manager ganham `relatorio=`; asserção de call passa a usar `ANY` só nesse argumento), `test_ipc_server.py`, `test_ipc_profile_switch_persist.py` (igualdade exata da resposta → asserção por campo, para não congelar o contrato aditivo), `test_profile_mode.py` (dublê + asserção nova de que o `origin` chega ao applier).

Nada commitado, nada em `git add` — tudo no working tree. Verifiquei que os hunks dos outros agentes em `manager.py` (PERFIL-MANUAL-VENCE-01) e em `ipc_handlers.py` (renumeração) continuam intactos.

Validação ao vivo que ainda falta (exige reiniciar o daemon, nunca com jogo aberto): (a) mexer na máscara e, em <30 s, "Ativar" o `sackboy_nativo` → máscara vira na hora e a resposta traz `mode_aplicado: true`; (b) mexer na máscara e abrir o Sackboy em <30 s → journal com **um** `profile_mode_deferred` e **uma** `profile_mode_pendencia_aplicada` (ou `profile_mode_pendencia_aguardando_jogo` enquanto o jogo tiver a autoridade), sem repetição a 2 Hz.


---

## Onda 3 — R-04/R-06 (launch/broker)

R-04 e R-06 implementados. Relatório:

## O que mudou, por arquivo

**`/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/launch_env.py`** (+237)
- `LAUNCH_ARM_WINDOW_SEC = 60.0` — frescor do marker para contar como "launch agora" (distinto do `WRAPPER_MARKER_WINDOW_SEC` de 15 min, que responde outra pergunta).
- `steam_input_appids()` — lê `steam_input_apps.txt` reusando `storm_doctor.steam_input_allowlist`, mas resolvendo o caminho por `config_dir()` (XDG, como o `disable_steam_input.sh`) em vez do `Path.home()` fixo do storm_doctor — isso deixa os testes herméticos pelo isolamento que o `tests/conftest.py` já faz.
- `launch_session_appid()` — appid do jogo do wrapper ainda vivo, reusando a decisão pura `wrapper_game_running` (NUMA-01) em vez de reinventar critério.
- `steam_input_exception_appid()` — marker **ou** janela em foco (leitura crua), com allowlist injetável.
- `arm_launch_profile()` — **R-04(a)**: lê o marker `last_run` (gravado pelo wrapper antes do `exec`), resolve o perfil com `steam_app_<appid>` e chama `apply_profile_mode(..., origin="launch")`; idempotente por `(appid, epoch)`; appid da allowlist **não** é armado (contradição 11).
- `materialize_launch_env`: laço novo **depois** do de perfis grava `steam_app_<appid>.env` sem `IGNORE`/`PROTON_DISABLE_HIDRAW` para cada appid da allowlist, mesmo sem perfil, sobrescrevendo de propósito o arquivo derivado de perfil (**R-06 item 1**). `_env_for_profile` (R-05) intocado.

**`daemon/subsystems/gamepad.py`** (+253/-24)
- `_autoridade_do_jogo` + `_recriacao_bloqueada_por_jogo` — **R-04(b)**, sinal **sticky** (`display_authority == "game"`), `origin="manual"` nunca bloqueado, ausência/"unknown" nunca bloqueia (risco (b) do plano). Warning + `store.bump("gamepad.recreate.blocked_by_game")`.
- Gate aplicado em `start_gamepad_emulation` (só quando o vpad existente está **vivo** — vpad morto pode ser recriado) e em `upgrade_primary_vpad_to_uhid` (antes de consumir o cooldown; o revive do VPAD-09 com `device is None` continua livre).
- `_set_evdev_grab` extraído de `_set_controller_grab`; gates da exceção de Steam Input em `_set_controller_grab`, `_broker_sync_grab` (hide) e `rehide_physical_hidraw`.
- `steam_input_excecao_ativa` (flag em memória, zero I/O nos gates) + `sync_steam_input_exception` (só age nas bordas: entra → ungrab + `restore_all`; sai → regrab + rehide, com os mesmos gates do rehide).
- `_reconciliar_launch` + `LAUNCH_RECONCILE_INTERVAL_SEC = 1.0`, chamado no topo de `dispatch_gamepad` (o `device` é lido **depois**, porque o arming pode ter recriado o vpad). Throttle com `try/except` próprio: dispatch de input nunca cai por causa do extra.

**`broker/hidraw_broker.py`** (+47) — `physical_nodes_exposure(uid, ...)`: espelho read-only de `restore_all_physical` que responde "o hidraw do físico está legível por este uid agora?" (**R-06 item 3**, base do status honesto).

**`app/actions/emulation_actions.py`** (+55/-…) — `_steam_input_excecao_status()` e `_refresh_steam_input_status` passam a distinguir "configurada" (appids no arquivo) de "efetiva" (físico legível): `controle liberado agora` × `só valendo durante o jogo` × `sem controle físico visível` (não afirma nada sem físico).

**`scripts/doctor.sh`** (+48) — `check_steam_input_allowlist`, registrado no `main()` sob "Steam Input": FAIL quando o `.env` do appid ainda carrega o dedup, WARN quando falta o `.env`, PASS quando a exceção é efetiva. Exercitei os três ramos com `HOME`/`XDG_CONFIG_HOME` falsos; na máquina dela hoje sai o WARN correto (o `.env` só nasce no próximo restart do daemon).

## Prova de que os testes pegam a regressão

Reverti o fix no source, rodei, restaurei, rodei de novo.

1. **Gate destrutivo** — troquei as duas chamadas de `_recriacao_bloqueada_por_jogo` por `if False`: `2 failed, 6 passed` — `test_perfil_nao_troca_mascara_com_o_jogo_na_autoridade` e `test_promocao_por_hotplug_nao_recria_vpad_com_jogo_na_autoridade`. Restaurado: `8 passed`. (Os 6 que passam nos dois lados são de propósito: asseguram que o gate **não** bloqueia manual/fora-de-jogo/vpad-morto/apply-idêntico.)
2. **R-06** — neutralizei o laço da allowlist no `materialize_launch_env` e os três gates: `3 failed, 10 passed` — `test_appid_da_allowlist_ganha_env_sem_dedup_mesmo_sem_perfil`, `test_allowlist_vence_o_perfil_do_mesmo_appid`, `test_com_excecao_ativa_o_broker_nao_reesconde`. Restaurado: `13 passed`.
3. **Arming** — `TestFiacaoNoPollLoop` prova a fiação (sem ela o arming existiria e nunca rodaria, que é o defeito original) e o throttle (50 ticks → 1 chamada). `test_mesmo_launch_arma_uma_vez_so` fecha o flap de 1 Hz.

Arquivos novos: `tests/unit/test_r04_gate_destrutivo_vpad.py`, `test_r04_arming_no_launch.py`, `test_r06_allowlist_steam_input.py`, `test_r06_status_honesto.py` (este com `pytest.importorskip("gi")`).

## Suíte e ruff

- Linha de base: `4659 passed`. Final: **`4695 passed`** (+36 novos, zero teste existente alterado).
- `ruff check src/ tests/` → **All checks passed!**
- `bash -n scripts/doctor.sh` → OK.

## Decisões diferentes do plano (e por quê)

1. **O arming não usa `profile.arm_for_appid` nem muda o wrapper.** O plano pedia um RPC novo chamado sincronamente pelo ping de vida — mas `daemon/ipc_handlers.py`, `daemon/lifecycle.py` e `assets/hefesto-launch.sh` estão fora da minha lista (outros agentes). Usei o marker `last_run`, como a tarefa instruiu. **O aviso "(c)" do plano (marker perde a corrida com o `exec`) não se aplica ao que ficou aqui**: o que corria contra o `exec` era a `.env`, e ela **não** depende do arming — já nasce com a opinião do perfil e, desde o R-05, com o backend prognosticado. O que o arming conserta é a **máscara**, que o jogo só consulta segundos depois, ao enumerar controles. O arming é disparado ≤1 s após o marker.
2. **O driver da reconciliação mora em `dispatch_gamepad`, não no `_poll_loop`.** O lugar canônico é a cadência do `_poll_loop` ao lado de `_drenar_modo_pendente` (mesma semântica, mesmo 1 Hz); ficou em `dispatch_gamepad` por ser o ponto de 1 Hz alcançável a partir dos meus arquivos. Está escrito assim no docstring. **Consequência conhecida:** o call site do poll loop gateia por `self._gamepad_device is not None`, então com a emulação **globalmente desligada** o arming não roda. Mover a chamada para o `_poll_loop` (3 linhas, ao lado do dreno do R-03) fecha esse buraco.
3. **Estendi o gate ao `upgrade_primary_vpad_to_uhid`**, que o plano não citava. A docstring dele já admitia "o jogo aberto PERDE o vpad por um instante" e julgava aceitável; a medição de 23/07 mostra que não é um instante (a Steam não reabre o handle). Reconexão BT é frequente nesta máquina — recuperar vibração não pode custar o controle inteiro. O revive do VPAD-09 (`device is None`) segue **não** gateado: sem vpad o jogo já está com zero controles.
4. **Gap deliberado que não pude fechar:** `stop_gamepad_emulation` não tem parâmetro `origin`, então o ramo `kind == "desktop"` de `apply_profile_mode` ainda pode desligar o vpad com o jogo em foco. Adicionar `origin` lá é dead code sem a mudança correspondente em `lifecycle.set_gamepad_emulation` (`stop_gamepad_emulation(self, persist=..., origin=origin)`) — fora dos meus arquivos. O ramo `kind is None` já está coberto pelo R-02.
5. **Custo de I/O:** com a allowlist **vazia** a reconciliação faz 1 `open` que falha por segundo (a checagem de allowlist é a primeira e corta tudo); com allowlist, 4 leituras de arquivos de ~40 B por segundo na thread de poll. Ordens de grandeza abaixo do que o R-22 ataca (socket do broker com timeout de 2 s e `HIDIOCGFEATURE` em BT ocioso), mas registro aqui como candidato a cache se a R-22 padronizar um.


---

## Onda 4 — R-20 + R-13 item 1 (camadas de saída)

The hotplug merge-por-campo invariant (PERFIL-01/04/05) holds. Everything is complete and verified.

---

## Relatório final — R-20 + R-13 item 1

### O que mudou, por arquivo

**`src/hefesto_dualsense4unix/core/backend_pydualsense.py`** (o coração da mudança)
- `_merged_desired_for_key` passou de 4 para **5 camadas** com dono declarado: `game > co-op > override por-uniq (perfil/usuária) > automática > default`. A escala de brilho por-uniq entra depois do merge do daemon e antes da camada game. Ganhou o kwarg `incluir_coop` (default True) — `resolved_player_leds_for` chama com `incluir_coop=False` para o revert do co-op não enxergar a própria camada.
- Estado novo: `_desired_owner_by_uniq` (procedência `{uniq:{campo:camada}}`), `_desired_coop_by_uniq` (camada do co-op), `_led_scale_by_uniq` (fator de brilho).
- `reset_output_overrides` agora carimba tudo como camada da **usuária** (único chamador real é o "Aplicar" da GUI).
- **`reset_profile_overrides`** (novo): republica só a camada do perfil — solta o que era do perfil, escreve o perfil novo **só no slot vago** (cede o campo que a usuária travou), e **converge o hardware ao resolvido** dos conectados com override (repara o stomp do broadcast global — o `apply_output_defaults` roda antes e pinta o global por cima do por-uniq).
- **`clear_user_output_overrides`** (novo): botão de soltar, chamado só na troca **manual** de perfil.
- **`set_led_scales`** (novo): registra o fator de brilho por-uniq (R-20 item 2).
- **`set_coop_outputs`** (novo): substitui a camada do co-op e converge os controles afetados; vocabulário restrito a `player_leds`.
- Helpers `_scaled_led`, `_clear_layer_locked`, `_stamp_owner_locked`, `_prune_overrides_locked`.

**`src/hefesto_dualsense4unix/profiles/manager.py`** (só overrides/apply)
- `apply(profile, *, origin="auto")` e `activate` propaga o `origin`. `origin=="manual"` chama `clear_user_output_overrides`; autoswitch/boot nunca chamam.
- Usa `reset_profile_overrides` (camada) quando o backend a tem; fallback ao caminho histórico (`reset_output_overrides` + `apply_output_for`) para backends sem camadas.
- Brilho por-controle vira **escala** via `_controllers_to_led_scales` + `set_led_scales`; `_controllers_to_specs` não materializa mais cor no caso brilho-only (exceto o degenerado `_brilho_materializa_cor`, brilho global 0).

**`src/hefesto_dualsense4unix/daemon/subsystems/coop.py`** (só publicação da camada)
- `_apply_coop_player_leds` publica o padrão via `_publicar_camada_coop` (novo) → `set_coop_outputs`; cai no sysfs cru só em backend legado.
- Reverts (`_revert_single_player_led`, `_revert_player_leds`) revogam a camada em vez de reescrever sysfs cru. Espelho `_camada_coop`.

**`src/hefesto_dualsense4unix/core/sysfs_leds.py`**: **não tocado** (deliberado — a camada reusa `_write_partial_output`→`node.set_players`).

### Prova de que os testes pegam a regressão (revert/restore feito e relatado)
- **C5 (R-20)**: revertendo `apply` para a substituição do mapa → **3 testes** de `test_r20_camadas_de_saida.py` falham (o override da usuária some do hardware). Restaurado.
- **Brilho materializa cor (R-20 item 2)**: revertendo `_brilho_materializa_cor` para o antigo (sempre materializa) → **2 testes** falham (o controle recebe o roxo global escalado, não a cor do slot). Restaurado.
- **R-13 item 1**: forçando `_publicar_camada_coop` a devolver False (co-op volta ao sysfs cru) → **6 testes** de `test_r13_coop_camada.py` falham. Restaurado.

### Contrato de teste mudado (documentado, não afrouxado)
`test_coop_player_leds.py::test_jogador_desconectado_tem_o_por_uniq_dele_restaurado`: a asserção do primário mudou de `player_led_pattern(1)` para `DEFAULT_BITS`. Motivo no comentário: R-13 item 4 nomeia "primário preso em P1 quando o último secundário sai" como bug ("dois player 1"). Com a camada, esvaziar `_players` revoga a camada e o primário volta ao padrão do perfil. A asserção-núcleo do teste (o secundário que sai recupera **seu** override) segue intacta.

### Resultado
- Suíte completa: **4710 passed** (baseline 4695 + 15 testes novos), 0 falhas.
- `ruff check src/ tests/`: **All checks passed!**
- Invariante de maior risco (merge-por-campo no hotplug, PERFIL-01/04/05): 11 testes de hotplug verdes. O merge core (`_merge_desired`) é intocado; co-op e escala são aditivos e só afetam `player_leds`/escala de `led`.

### Decisões diferentes do plano (com motivo)
1. **`app/draft_config.py`, `daemon/ipc_draft_applier.py`, `daemon/subsystems/identity.py`** estão nos "arquivos" do R-20/R-13 no plano, mas **não** na minha lista de arquivos (são de outros agentes, trilha T2/GUI). Não os toquei. Consequência: o espelhamento de `_controllers_to_ipc` na GUI (R-20 item 2, caminho ao vivo do "Aplicar") fica para o agente da GUI; o meu lado (ativação de perfil) está completo e o `ipc_draft_applier._apply_controllers` já usa `reset_output_overrides` (camada da usuária), que é o correto para o "Aplicar".
2. **Não adicionei os métodos novos à interface `IController`** (`core/controller.py` fora da minha lista). Usei o padrão `getattr` defensivo já estabelecido no repo (igual a `reassert_resolved_outputs`), então FakeController/backends legados degradam sem crash.
3. **`apply` default `origin="auto"`** (não `"manual"`): caller que esqueça o parâmetro **preserva** o ajuste da usuária (o erro seguro). Só `activate`/GUI passam `"manual"` explícito para soltar a camada.

### Nota de risco residual para o gate humano
A precedência "usuária vence perfil" (R-20) significa que, depois de ela ajustar um controle na GUI, os overrides por-controle **daquele campo** de perfis ativados por autoswitch são adiados até ela **trocar de perfil manualmente** (ou aplicar "Todos"). É o contrato declarado do R-20/R-19 e o que conserta a queixa (2), mas vale confirmar ao vivo que o "botão de soltar" (troca manual de perfil) está intuitivo — o log `override_do_perfil_cedeu_ao_ajuste_manual` existe para o doctor explicar o que está segurando.


---
