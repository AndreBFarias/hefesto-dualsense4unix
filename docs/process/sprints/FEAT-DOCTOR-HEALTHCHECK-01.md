# FEAT-DOCTOR-HEALTHCHECK-01 — Diagnóstico de saúde (scripts/doctor.sh)

**Tipo:** feat (ferramenta de diagnóstico).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — novo `scripts/doctor.sh`.
**Dependências:** consolida verificação das demais sprints da wave.
**Status:** DONE (implementado + validado no estado atual da máquina).

---

## Contexto

A mantenedora não sabia "se o daemon tá funcionando". Faltava um comando único
para diagnosticar o estado de ponta a ponta e sugerir/aplicar correções.

## Decisão / Entrega

Novo `scripts/doctor.sh` com saída `PASS/FAIL/WARN` (marcadores ASCII, compat
sanitizer de anonimato — ver commit 9153cb3), `--fix` e `--quiet`; exit != 0 se
houver FAIL. Checks:

1. Daemon/CLI instalado; serviço `is-active`; socket IPC presente.
2. 5 regras udev presentes **e** 73/74 com o nome de unit correto (detecta
   [[BUG-UDEV-HOTPLUG-UNIT-NAME-MISMATCH-01]] em instalações antigas).
3. `/dev/uinput` presente.
4. Applet `.desktop` + `X-CosmicApplet=true` + **ícone resolvível** + validate.
5. WirePlumber NÃO fixando o DualSense como source (lê `default-nodes`).
6. Controle alcançável (hidraw/USB/BT) + transporte.
7. WARN (não FAIL) para `/dev/hidraw*` em 0666 (ajuste manual).

`--fix` reaplica udev (`scripts/install_udev.sh`) e instala/reseta o fix de
áudio (`scripts/fix_wireplumber_default_source.sh --install`).

## Critérios de aceite

- [ ] `bash -n scripts/doctor.sh` ok.
- [ ] No estado pré-recuperação, reporta FAIL para: CLI ausente, ícone do applet,
      WirePlumber, e 73/74 (nome de unit). **Validado** em 2026-05-22.
- [ ] Pós-recuperação (`--fix` + reinstalar): tudo PASS.

## Arquivos tocados

- `scripts/doctor.sh` (novo)

## Notas para o executor

- A checagem de hotplug exige casar a sintaxe udev `ENV{...}="..."` (com `}`);
  bug corrigido durante a implementação (o grep sem `}` não detectava).
- Fase 2 (opcional): subcomando `hefesto-dualsense4unix doctor` no CLI (Python),
  focado no que o daemon sabe via IPC. O shell continua a fonte canônica para o
  usuário rodar pós-purge, antes de o CLI existir.

## Proof-of-work runtime

```bash
bash scripts/doctor.sh            # antes: FAILs esperados
bash scripts/doctor.sh --fix      # aplica correções seguras
```

## Fora de escopo

- Subcomando CLI Python (fase 2).
