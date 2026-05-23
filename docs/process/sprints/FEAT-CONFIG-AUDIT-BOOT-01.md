# FEAT-CONFIG-AUDIT-BOOT-01 — auditoria de perfis no boot + notificação

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** M · **Dependências:** FEAT-DOCTOR-CLI-AND-CHECKS-01 · **Status:** DONE

## Contexto

`load_all_profiles()` já pula perfis corrompidos com um WARN no log (PROFILE-LOADER-UX-01), mas o
usuário não vê logs — um perfil danificado some silenciosamente do fallback. Faltava AVISAR de
forma visível no boot.

## Decisão / Entrega

- `profiles/loader.py`: nova `audit_profiles()` que valida todos os perfis sem carregá-los para uso
  e retorna [(nome, erro)] dos inválidos (nunca levanta).
- `integrations/desktop_notifications.py`: `notify_config_errors(invalid)` — notificação D-Bus uma
  vez por boot (`once_key`), opt-in, listando os perfis ignorados e sugerindo `doctor`.
- `daemon/lifecycle.py`: `_audit_config_on_boot()` chamado no fim do boot — log + notificação se
  houver corrompidos. Best-effort (nunca derruba o boot).

## Critérios de aceite

- Perfil corrompido é detectado e reportado (log + notificação) no boot, sem derrubar o daemon.
- ruff + mypy --strict + pytest (suíte completa, 1414) verdes.

## Arquivos tocados

- `src/hefesto_dualsense4unix/profiles/loader.py`, `integrations/desktop_notifications.py`,
  `daemon/lifecycle.py`
- `tests/unit/test_config_audit_boot.py` (novo)
