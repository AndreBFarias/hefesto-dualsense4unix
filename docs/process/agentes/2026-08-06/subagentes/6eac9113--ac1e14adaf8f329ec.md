# agente ac1e14adaf8f329ec (sessao 6eac9113)

**tipo:** general-purpose
**tarefa:** Integridade: backup, verificador, log
**profundidade:** 1  **pai:** -

## O QUE FOI PEDIDO

Repositório /mnt/Apate/Desenvolvimento/hefesto-dualsense4unix. LEVA 2 — IMPLEMENTAR. Você PODE e DEVE alterar arquivos.

SEUS ARQUIVOS (não toque em outros de src/, para não colidir com agentes irmãos):
- `src/hefesto_dualsense4unix/profiles/loader.py`
- `src/hefesto_dualsense4unix/profiles/sanidade.py` (NOVO)
- `src/hefesto_dualsense4unix/cli/cmd_doctor.py` e `cli/cmd_profile.py`
- `tests/conftest.py`
- testes novos em `tests/unit/`

Agentes irmãos estão em `app/actions/*`, `app/draft_config.py`, `daemon/lifecycle.py` e `profiles/autoswitch.py` — NÃO toque nesses.

CONTEXTO (medido, não reinvestigue): os perfis da usuária foram corrompidos pela GUI — perderam a regra (`match` virou `{"type":"any"}`) e as prioridades escalaram até 191. Não existe hoje: validação semântica ao carregar, backup automático, verificador, nem qualquer registro no journal de que um perfil foi gravado. A pergunta dela foi: *"como sabemos se algum teste ou algo a mais corrompeu algo?"*

TAREFAS, na ordem de prioridade (a 1 é a que para o sangramento):

**1. BACKUP VERSIONADO em `save_profile`** (`loader.py:621`, escrita em `:724-738`). Dentro do `FileLock` que já existe, antes do `os.replace`: copiar o alvo atual para `profiles/.historico/<slug>/<timestamp>.json`, retendo os últimos N (sugestão 10, constante nomeada). Perfis têm ~1 KB, o custo é um `copyfile`.
   Some a isso um comando de restauração em `cli/cmd_profile.py`: `profile historico <slug>` (lista) e `profile restore <slug> [--em <ts>]`.
   TESTE QUE MORDE: salvar 3 vezes, conferir 3 versões, restaurar e comparar byte a byte; arrancar o backup e ver reprovar.

**2. REGISTRO NO JOURNAL de toda gravação de perfil.** Hoje não existe — foi a lacuna que impediu decidir se o `191` veio de catraca ou do slider. Emitir, em `save_profile`, um `profile_salvo` estruturado com pelo menos: `nome`, `match_antes`/`match_depois` (o discriminador, ex. "any"/"criteria"), `priority_antes`/`priority_depois`, e a origem se disponível. Use o `logger` estruturado do projeto (`utils/logging_config.py`), no padrão dos eventos existentes.
   TESTE QUE MORDE: gravar por cima de um perfil `criteria` com um `any` e assertar que a linha registra a transição.

**3. VERIFICADOR SEMÂNTICO** — `profiles/sanidade.py`, exposto como `doctor --perfis` (`cli/cmd_doctor.py`). Regras, todas com caso real no disco dela:
   - catch-all com prioridade >= a de algum perfil específico (é a `PERFIL-NASCE-CERTO-01/E4`, que nunca foi feita);
   - perfil cujo nome suger

## RESULTADO FINAL

Tudo pronto. Relatório da LEVA 2.

## 1. Backup versionado em `save_profile` — feito

`src/hefesto_dualsense4unix/profiles/loader.py`
- `:635` `HISTORICO_DIR_NAME = ".historico"`, `:639` `HISTORICO_MAX_VERSOES = 10`
- `:642` `historico_dir()`, `:662` `listar_historico()`, `:692` `_podar_historico()`, `:703` `_arquivar_versao()` (best-effort: falha loga `profile_backup_failed` e NÃO impede o save)
- `:787` `save_profile(profile, *, origem=None)` — dentro do `FileLock` que já existia, lê os bytes atuais **uma vez** (servem para o backup e para o "antes" do journal), arquiva, e só então `os.replace`
- `:890` `restaurar_do_historico()` — valida contra o schema, escreve os **bytes originais** via `_atomic_write_bytes` (`:1007`), e arquiva a versão atual antes de pisar (restaurar por engano também tem volta)
- `:948` `delete_profile` também arquiva (apagar é a gravação mais destrutiva)

O `.historico/` é subdiretório: todas as varreduras do projeto usam `glob("*.json")` não-recursivo ou `find -maxdepth 1` (conferi loader, `doctor.sh:1479`, `_perfis_inalcancaveis`) — nada o enxerga como perfil.

CLI em `cli/cmd_profile.py:233` `profile historico <nome>` (tabela com data legível, `match`, prioridade, arquivo — versão ilegível aparece marcada em vez de sumir) e `:267` `profile restore <nome> [--em <carimbo>]`.

## 2. Journal de toda gravação — feito

`loader.py:855` `_registrar_gravacao` emite `profile_salvo` com `nome`, `arquivo`, `criado`, `match_antes`/`match_depois`, `priority_antes`/`priority_depois`, `origem`, `pid`, `backup`. `match_antes="ilegivel"` quando o arquivo anterior não decodifica. `origem` vem do parâmetro ou de `_origem_do_processo()` (`:773`, basename do `argv[0]`). Também há `profile_apagado` e `profile_restaurado`. Nunca levanta.

Linha real capturada: `profile_salvo ... match_antes=criteria match_depois=any priority_antes=10 priority_depois=191 origem=... pid=... backup=.../20260805T041057_402048.json` — exatamente a transição que não dava para provar.

## 3. Verificador semântico — feito

`src/hefesto_dualsense4unix/profiles/sanidade.py` (novo, 5 regras em `REGRAS:336`): `catch_all_vence_especifico` (erro), `prioridade_fora_da_faixa` 0-200 (erro), `catch_all_com_cara_de_jogo` (aviso), `prioridades_empatadas` (aviso), `catch_all_demais` (aviso). Todo `Achado` carrega `cura` e sai como `mensagem — Cura: ...`.

Dispensa nomeada: `CATCH_ALL_LEGITIMOS = {"fallback"}` (`:48`) vale **enquanto ele está no piso** (`_tem_dispensa:128`) — um "fallback" que sobe a 100 volta a ser acusado, que é a forma exata da corrupção. Duas decisões contra fadiga de alarme, ambas com teste: (a) o sinal de *nome* só dispara acima da prioridade 0, senão o perfil de desktop dela levaria aviso perpétuo insilenciável; (b) o sinal *declarado* (modo gamepad / supressão) dispara em qualquer prioridade.

Exposto em `cli/cmd_doctor.py:83` `_linhas_perfis` / `:102` `_print_bloco_perfis`, como `doctor --perfis` (sem `doctor.sh`, sem storm, sem IPC; **exit 1** se houver achado grave) e também no `doctor` completo (sem mexer no rc, mesma política do bloco storm). Isso exigiu **uma linha nova em `cli/app.py:90-99`** (a opção `--perfis`) — arquivo fora da minha lista mas de nenhum agente irmão; sem ela o comando não existiria.

## 4. Portão de hermeticidade — feito, e já mediu

`tests/conftest.py:333-510` — CANARIO-FS-01: `pytest_sessionstart` fotografa os três diretórios reais, `pytest_sessionfinish` refaz e reprova (`session.exitstatus = 1`) listando `CRIADO/APAGADO/MUDADO`.

**Achado importante, medido**: a primeira versão comparava `(mtime_ns, size)` como pedido e acusou 15 arquivos logo na estreia — todos `*.json.lock` no `~/.config` dela. Não era a suíte: o daemon (pid 1670) e a janela (`app.main`, pid 8306) estão de pé e o `filelock` toca o lock a cada aquisição (confirmei com `stat` fora do pytest, 4s de intervalo). Um portão assim seria desligado na primeira semana. A foto passou a guardar `(mtime_ns, tamanho, sha256)` e o delta é **mudança de conteúdo** — mtime sozinho não conta. Custo: 93 arquivos, 356 KB.

**Resposta à pergunta dela**: com o canário armado, a suíte de unidade inteira (**6968 passed, 1 skipped**) terminou **sem um único delta** nos três diretórios. Hoje nenhum teste escreve no `~/.config` dela.

Escotilha `HEFESTO_SEM_CANARIO_FS=1` e selo `_CANARIO_ARMADO` (sem foto inicial o canário fica quieto em vez de acusar o `$HOME` inteiro).

**Não movi as constantes de módulo, como instruído**: `app/actions/emulation_actions.py:718` (`_WP_DROPIN_DIR`, dir de **escrita**) é de agente irmão. `integrations/storm_doctor.py:34` (`_ALLOWLIST_PATH`, só leitura) não é meu e mover obrigaria a editar `tests/unit/test_steam_input_ponteiros.py:193`, que monkeypatcha a constante pelo nome — também fora do meu escopo. As duas continuam avaliadas no import.

## Provas de mordida (arranquei, vi reprovar, devolvi)

| Cura arrancada | Resultado |
|---|---|
| `_arquivar_versao` em `save_profile` | 10 reprovados |
| `_podar_historico` | `test_historico_retem_apenas_as_ultimas_n` reprova |
| `_registrar_gravacao` | 4 testes de journal reprovam |
| `_atomic_write_bytes` → reserialização | `test_restore_devolve_a_versao_byte_a_byte` reprova (perfil de partida escrito à mão, recuo de 4 espaços) |
| cada uma das 5 regras de `REGRAS` | 2 a 5 reprovados, sempre nomeando a regra |
| `CATCH_ALL_LEGITIMOS` vazio | 4 reprovados |
| folga do piso no sinal de nome | `test_catch_all_de_nome_proprio_no_piso_nao_e_nagueado` reprova |
| canário voltando a comparar mtime | `test_mtime_sozinho_nao_acusa_ninguem` reprova |
| `session.exitstatus = 1` | `test_sessionfinish_reprova_a_sessao_com_delta` reprova |
| selo `_CANARIO_ARMADO` | `test_canario_desarmado_nao_acusa_o_home_inteiro` reprova |
| `raise typer.Exit` do `--perfis` | 2 testes de doctor reprovam |

## Portões

`pytest -k "loader or sanidade or profile or doctor"` **776 passed**; suíte de unidade inteira **6968 passed, 1 skipped**; `ruff check src/ tests/` limpo; `mypy src/hefesto_dualsense4unix` limpo (162 arquivos); acentuação, glifos, referências-docs, `check_test_data.sh`, `check_anonymity.sh`, paridade de empacotamento e consistência de versão: todos OK. MACs de teste na faixa `AA:BB:CC:00:00:02`. Nada commitado; os arquivos novos estão no índice (os portões são cegos a arquivo novo).

Testes novos: `tests/unit/test_profile_historico.py` (16), `test_profiles_sanidade.py` (30), `test_conftest_canario_fs.py` (9), `test_cli_profile_historico.py` (9).

Duas notas para quem coordenar: (1) `save_profile` agora aceita `origem=` — o funil novo do agente irmão (`app/actions/profile_writer.py:110`) é o lugar exato para passar `origem="janela"` e fechar a rastreabilidade da GUI; (2) o único erro de mypy que vi durante o trabalho estava em `app/actions/footer_actions.py:392`, de agente irmão, e já sumiu.
