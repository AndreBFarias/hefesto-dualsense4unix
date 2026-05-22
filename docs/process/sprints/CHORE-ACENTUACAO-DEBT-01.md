# CHORE-ACENTUACAO-DEBT-01 — Limpar findings pré-existentes do gate de acentuação

**Tipo:** chore (dívida técnica / CI).
**Wave:** V3.6.
**Estimativa:** S — mecânico, espalhado por ~15 arquivos.
**Dependências:** nenhuma.
**Status:** READY.

---

## Contexto

O gate `python3 scripts/validar-acentuacao.py --all` roda no CI
(`.github/workflows/ci.yml`) e, na varredura de 2026-05-22, acusa **51 violações
pré-existentes**. Confirmado via `git worktree` que já estavam no HEAD **antes** da
Wave V3.6 — não são regressão das sprints 120/121/116 (cujos arquivos passam o
validador com `exit 0`). Ou seja, esse passo do CI já vinha vermelho.

Os findings estão concentrados em (caminhos):

```
.github/workflows/anonymity-check.yml, ci.yml, release.yml
flatpak/br.andrefarias.Hefesto.yml
install.sh
packaging/arch/README.md, packaging/fedora/README.md, packaging/nix/README.md
scripts/build_appimage.sh, scripts/build_deb.sh
src/hefesto_dualsense4unix/app/app.py, app/main.py, app/theme.py
src/hefesto_dualsense4unix/integrations/desktop_notifications.py
src/hefesto_dualsense4unix/utils/i18n.py
tests/unit/test_desktop_notifications.py, tests/unit/test_tray.py
```

Palavras típicas detectadas (cruas, sem acento):

```
diretorio, unica, nao, usuario, proprio, instalacoes, versao, configuracao,
funcoes, repositorio, dependencias, limitacoes, modulo, binario, tambem,
necessario, pratica, dinamica, proxima, atualizacao
```

## Decisão / Entrega

Para cada finding:
- **Texto PT-BR real** (comentários, docstrings, mensagens, READMEs) → corrigir com
  o acento canônico.
- **Termos técnicos / tokens** que não são PT-BR (ex.: `@media`, nome de arquivo
  `acao.json`, exemplos crus) → marcar com `# noqa-acento` (Python/shell) ou mover
  para bloco de código cercado (Markdown), seguindo o padrão já usado no projeto.
- Rodar `validar-acentuacao.py --all` até `exit 0`.

## Critérios de aceite

- [ ] `python3 scripts/validar-acentuacao.py --all` → `exit 0`.
- [ ] Nenhuma mudança de comportamento (só texto/comentários/docs).
- [ ] Demais gates seguem verdes (`ruff`, `mypy --strict`, `pytest`).

## Notas para o executor

- O validador pula blocos ```` ``` ```` em `.md` e linhas com `# noqa-acento` /
  `# noqa: acentuacao`. Ver `scripts/validar-acentuacao.py` (docstring + regras).
- Decisão de design pendente: os READMEs de distro (`packaging/{arch,fedora,nix}`)
  e `flatpak/*.yml` devem ganhar acento ou entrar em `WHITELIST_PATTERNS` do
  validador? Alguns podem ficar em conteúdo técnico/inglês via whitelist.
- Reavaliar se o gate `--all` deveria excluir `.github/workflows/*` (o validador
  hoje varre os próprios YAMLs de CI).

## Fora de escopo

- Qualquer mudança funcional de código.
