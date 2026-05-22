# CHORE-PURGE-ALL-INSTALL-FORMS-01 — Descontaminação total (deb + flatpak + nativo + applet)

**Tipo:** chore (novo script de descontaminação).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — novo `scripts/purge.sh` envelopando o uninstall.
**Dependências:** [[BUG-UNINSTALL-COSMIC-APPLET-CONFIG-PATH-01]].
**Status:** DONE (implementado; usado na recuperação da máquina).

---

## Contexto

A mantenedora instalou de 3 formas (.deb + flatpak + nativo) — "isso deve ter
zuado algo". O provável "desconecta/reconecta" foi contenção entre múltiplos
daemons disputando `/dev/hidraw`. Faltava um botão único de limpeza total.

## Decisão / Entrega

Novo `scripts/purge.sh`, idempotente, com `--yes`/`--dry-run`/`--with-config`
(default = **preservar** perfis + backup):

1. **Backup** dos perfis (curto + longo) antes de tudo.
2. Chama `uninstall.sh --udev {--keep-config|--purge-config} --yes` (reaproveita
   toda a lógica testada: nativo/.deb/flatpak/AppImage/locale/runtime/applet).
3. **Reforço** de rastros que versões antigas do uninstall não removiam: applet
   em `/usr/local`+`/usr/share`, regra udev 74, `modules-load`, e o **ghost** do
   hotplug systemd --user.
4. `.deb`: `apt-get purge` (não só remove) p/ limpar conffiles, se instalado.
5. Flatpak: `flatpak uninstall` se presente.

## Critérios de aceite

- [ ] `bash -n scripts/purge.sh` ok.
- [ ] `--dry-run` imprime ações sem executar.
- [ ] Após `purge.sh --yes`: `scripts/doctor.sh` não acha rastros (applet/udev/ghost),
      perfis preservados + backup criado.

## Arquivos tocados

- `scripts/purge.sh` (novo)

## Notas para o executor

- Sequência de recuperação: `purge.sh --yes` → `install.sh --native ...` →
  `doctor.sh`. A descontaminação remove a contenção multi-daemon (causa provável
  do desconecta/reconecta).

## Proof-of-work runtime

```bash
bash -n scripts/purge.sh
./scripts/purge.sh --dry-run
./scripts/purge.sh --yes && ./scripts/doctor.sh
```

## Fora de escopo

- Remover o runtime GNOME do flatpak (gerenciado pelo flatpak).
