# CHORE-CONFIG-MIGRATE-LEGACY-SHORT-PATH-01 — Perfis órfãos no caminho de config legado (curto)

**Tipo:** chore (config/migração) + fix (escritor hardcoded).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — módulo de migração + 2 hooks + correção de 1 caminho + testes.
**Dependências:** nenhuma (pré-requisito: protege dados antes de purge/reinstall).
**Status:** DONE (implementado + testes unit; gates/smoke na recuperação da máquina).

---

## Contexto

Auditoria (mantenedora, Pop!_OS COSMIC, 2026-05-22): após instalar de 3 formas
(.deb + flatpak + nativo) e rodar `uninstall.sh`, os perfis customizados
(`acao, aventura, bow, corrida, esportes, fps, navegacao, meu_perfil, fallback`)
sumiriam ao reinstalar e rodar o daemon.

## Diagnóstico (causa-raiz)

1. `src/hefesto_dualsense4unix/utils/xdg_paths.py:13` usa
   `PlatformDirs("hefesto-dualsense4unix")` → caminho **longo**
   `~/.config/hefesto-dualsense4unix`. Mas os dados reais estão no **curto**
   `~/.config/hefesto` (+ `~/.local/share/hefesto`), criados por versão
   pré-rename (commits 7f4687a..08e92b8). O longo está ausente → daemon lê config
   vazia → perfis "somem".
2. `src/hefesto_dualsense4unix/app/gui_prefs.py:16` tinha `Path("~/.config/hefesto")`
   **hardcoded** (curto) — único escritor que ainda gravava no curto
   (`gui_preferences.json`, 22/05), divergindo de perfis/sessão.

## Decisão / Entrega

1. **Corrigir o escritor:** `gui_prefs.py` passa a usar `xdg_paths.config_dir()`
   (longo); removido o `Path` hardcoded.
2. **Migração idempotente no boot:** novo `utils/migrate_legacy_paths.py` —
   `migrate_legacy_paths()` copia **arquivo por arquivo, só o ausente**,
   `~/.config/hefesto`→`config_dir()` e `~/.local/share/hefesto`→`data_dir()`,
   sem sobrescrever, mantendo o curto como backup. Chamado no boot do **daemon**
   (`daemon/main.py:run_daemon`) e da **GUI** (`app/main.py:main`) → todas as
   formas (nativo/.deb/Arch) herdam sem reimplementar.
3. **Belt-and-suspenders no install:** `install.sh` chama a migração via venv
   ANTES de `install_profiles.sh` popular defaults (não mascara perfis).

## Critérios de aceite

- [ ] Reinstalar e rodar o daemon **mantém** os perfis customizados.
- [ ] `gui_preferences.json` lido/escrito no caminho longo.
- [ ] Migração não sobrescreve arquivos já existentes no destino; idempotente.
- [ ] Testes unit (`tests/unit/test_migrate_legacy_paths.py`): copia ausentes,
      não sobrescreve, no-op sem legado.
- [ ] Gates: ruff, mypy --strict, pytest, validar-acentuacao.py --all, check_anonymity.sh.

## Arquivos tocados

- `src/hefesto_dualsense4unix/utils/migrate_legacy_paths.py` (novo)
- `src/hefesto_dualsense4unix/app/gui_prefs.py`
- `src/hefesto_dualsense4unix/daemon/main.py`, `src/hefesto_dualsense4unix/app/main.py`
- `tests/unit/test_migrate_legacy_paths.py` (novo)
- `install.sh` (migração antes de install_profiles)

## Notas para o executor

- Migração é COPY (não move): o curto fica como backup. `uninstall --purge-config`
  faz backup adicional antes de apagar ambos.
- Flatpak só enxerga o curto com `--filesystem=home`; lá é best-effort
  (ver [[CHORE-PACKAGING-PARITY-ALL-FORMS-01]]).

## Proof-of-work runtime

```bash
.venv/bin/pytest tests/unit/test_migrate_legacy_paths.py -q
.venv/bin/ruff check src/ && .venv/bin/mypy --strict src/hefesto_dualsense4unix
```

## Fora de escopo

- Renomear o app-id flatpak (`br.andrefarias.*`).
