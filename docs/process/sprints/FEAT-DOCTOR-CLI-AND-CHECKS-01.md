# FEAT-DOCTOR-CLI-AND-CHECKS-01 — doctor no CLI + checks do daemon via IPC

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** M · **Dependências:** FEAT-DOCTOR-HEALTHCHECK-01, FEAT-DAEMON-PAUSE-RESUME-01 · **Status:** DONE

## Contexto

A mantenedora pediu para generalizar a "sacada do doctor" para as demais features. Até a v3.7 o
doctor era só um script shell (`scripts/doctor.sh`), focado em infra (daemon instalado, udev,
uinput, applet, WirePlumber). Faltava (a) expô-lo como subcomando do CLI e (b) cobrir o que só o
daemon sabe em runtime (responde ao IPC? pausado? perfis carregam?).

## Decisão / Entrega

- Novo `cli/cmd_doctor.py` + comando `hefesto-dualsense4unix doctor [--fix] [--quiet]`.
- Reusa `scripts/doctor.sh` (localiza em layouts editable e `.deb`) para os checks de infra, com
  passagem de `--fix`/`--quiet`, e propaga o exit code.
- Adiciona uma seção "daemon (via IPC)": IPC responde, daemon pausado (WARN), perfis listáveis —
  features que só o daemon conhece em runtime, degradando para WARN se o daemon estiver offline.

## Critérios de aceite

- `hefesto-dualsense4unix doctor` roda os checks de infra + os do daemon.
- Offline-safe: sem daemon, os checks de runtime viram WARN, sem explodir.
- ruff + mypy --strict + pytest (2 testes) verdes; subcomando registrado no CLI.

## Arquivos tocados

- `src/hefesto_dualsense4unix/cli/cmd_doctor.py` (novo), `src/hefesto_dualsense4unix/cli/app.py`
- `tests/unit/test_cmd_doctor.py` (novo)

## Notas / futuro

- Checks de portas (UDP 6969 / metrics 9090) e saúde por subsystem podem ser somados ao
  `doctor.sh`/IPC numa próxima iteração; o gancho (seção via IPC) já existe.
