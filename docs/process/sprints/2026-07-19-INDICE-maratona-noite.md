# ÍNDICE — Maratona da noite 2026-07-19 (concluir TUDO hoje)

> Escrito pelo Fable 5 como CÉREBRO/coordenação; execução continua no **Opus 4** (main loop)
> com **TODOS os agentes em `model: 'sonnet'`**. Autorização da mantenedora: implementar todas
> as ondas + legados, validação ao vivo só no FINAL. Sudo: senha ***SENHA-REMOVIDA-DO-HISTORICO*** (pré-autorizada).
> Vigiar a barra de uso; limite da sessão Pro resetou/reseta ~20:50 America/Sao_Paulo.

## Estado do working tree AGORA (não commitado, além do HEAD 27b51d5)

- Fix **BLUEZ-UHID-01** aplicado: `_is_virtual_hidraw` (backend_pydualsense.py) e
  `_is_virtual_evdev` (evdev_reader.py) decidem por IDENTIDADE (phys `hefesto-vpad`/uniq `02:fe`)
  e não por `/devices/virtual/` — testes em test_backend_ignora_vpad_virtual.py e
  test_evdev_reader.py. NÃO reverter; âncoras de linha dos sprints são do HEAD (conferir offset).
- Scrub de MACs reais em 4 arquivos de docs/process/estudos/ (git diff mostra).
- Máquina: bluez **5.85** backport instalado (bonds antigos migraram fora; os 4 controles
  re-pareados e funcionando via BT); install.sh RODADO hoje (wrapper/regras 80-81/modprobe OK);
  main.conf com 2 blocos hefesto (FastConnectable + JustWorksRepairing); daemon saudável.

## Política de execução (regras do jogo desta noite)

1. **Modelos**: coordenador = Opus (você); `agent()`/workflows sempre `model: 'sonnet'`,
   `effort: 'medium'` (subir p/ 'high' só em auditor/verificador). Prompts curtos que APONTAM
   para o sprint .md (fonte da verdade) — nunca re-embutir contexto longo.
2. **Budget**: testes FOCADOS durante o dev; a suíte completa (pytest tests/ 0-skipped + ruff
   0.15.20 + mypy + check_anonymity.sh) roda UMA vez por onda no fechamento, e uma vez no gate
   final. Nada de re-pesquisar o que os estudos/memória já cravaram.
3. **Proibições vivas**: não reiniciar daemon/bluetoothd durante dev (controles em uso); não
   escrever em /dev|/sys reais em teste; restart do daemon só nos fechamentos (é barato e já
   validado). Testes GUI sem `import gi` no topo.
4. **Commits**: só no fechamento final — temáticos, ANÔNIMOS (check_anonymity é gate duro).
5. **Install**: EU rodo (método PTY validado hoje, ver memória reference_sudo_ticket_tty_notty):
   `script -qec "bash -c 'echo ***SENHA-REMOVIDA-DO-HISTORICO*** | sudo -S -v 2>/dev/null && ./install.sh --yes'" /dev/null`

## Ordem de execução (dependências reais de arquivo)

| # | Onda | Spec (fonte da verdade) | Arquivos-chave | Depois de |
|---|------|--------------------------|----------------|-----------|
| 1 | **N** numeração una | `2026-07-19-sprint-numeracao-una.md` | game_signal(novo), lifecycle, state_store, launch_env, hefesto-launch.sh, backend_pydualsense, sysfs_leds, external_leds, external_identity, identity, ipc_handlers, GUI card, doctor | — |
| 2 | **R** rádio/install | `2026-07-19-sprint-onda-r-radio-install.md` | install.sh, uninstall.sh, assets/bluetooth/**, assets/systemd novo, disable_steam_input.sh | — (paralela à N: arquivos disjuntos) |
| 3 | **HANG-01** | `2026-07-19-sprint-hang-01-tick-resiliente.md` | lifecycle, external_identity, evdev_reader | N (mesmos arquivos) |
| 4 | **G** gyro02+doctor | `2026-07-19-sprint-onda-g-gyro02-doctor.md` | external_identity/external_leds, doctor, state_full | N e HANG-01 |
| 5 | **U** GUI/regressões | `2026-07-19-sprint-onda-u-gui-regressoes.md` | gui/**, ipc_handlers, wp-fix | N (ipc/card) — triagem pode começar antes (read-only) |
| 6 | **S** broker fd-injection | `2026-07-19-sprint-broker-hide-hidraw-onda-dedicada.md` + `docs/process/future-broker/` | broker novo + backend/motion + install | TODAS (a mais invasiva) — ver ARMADILHA abaixo |
| 7 | Gate final + auditoria adversarial de TUDO + commits anônimos + install (PTY) + checklist de validação ao vivo | — | — | 1-6 |

**ARMADILHA nova para a Onda S**: com BlueZ 5.85 os hidraws BT físicos moram em
`/devices/virtual/misc/uhid/` — o validador de identidade do broker precisa da MESMA lógica do
fix BLUEZ-UHID-01 (HID_ID/HID_PHYS/HID_UNIQ do uevent do pai HID; jamais topologia).

## Workflows prontos para retomar (scripts em disco; editar antes: agentes → sonnet)

- Onda N: `.../workflows/scripts/impl-onda-n-numeracao-una-wf_4ad59664-204.js`
  (resumeFromRunId wf_4ad59664-204 — só o investigador HANG-01 tem cache; implementadores
  re-rodam). Adicionar `model: 'sonnet'` em TODOS os agent(); manter effort como está.
- Onda R: `.../workflows/scripts/impl-onda-r-radio-wf_3e56c7c8-25e.js`
  (resumeFromRunId wf_3e56c7c8-25e — zero cache; implementadores já são sonnet; trocar o
  auditor para sonnet+high).
- Diretório-base: `/home/vitoriamaria/.claude/projects/-home-vitoriamaria-Desenvolvimento-hefesto-dualsense4unix/089ae384-2e6d-491e-9882-d2dad1cdef19/workflows/scripts/`

## Checklist de validação ao vivo (fechamento, com a mantenedora)

1. Cliente Steam aberto SEM jogo: branco azul/player-1; UM só "player 3"; escrita estrangeira
   repintada ≤2s (aceite da Onda N).
2. Sackboy COM launch option `hefesto-launch %command%`: gyro + rumble + sem race
   hefesto×sony (U6); fechar o jogo com Steam viva → paleta volta ≤32s.
3. Nintendo Pro USB: gyro nativo ligando (GYRO-02, se entregue); journal `[JOYCON]` limpo.
4. GUI: os 13 sintomas U1-U13 do sprint da Onda U reverificados um a um.
5. Áudio da mantenedora funcionando (U12) — ela reportou gerenciamento de áudio travado.
6. `doctor.sh` 100% verde; kernel-watch sem [BT-ERR]/[JOYCON] novos; bluetoothd sem crash no
   journal do dia seguinte.
