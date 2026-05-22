# BUG-UDEV-HOTPLUG-UNIT-NAME-MISMATCH-01 — Hotplug nunca abriu a GUI (nome de unit errado)

**Tipo:** fix (udev/systemd).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** XS — troca de string em 2 arquivos de regra.
**Dependências:** nenhuma.
**Status:** DONE (assets corrigidos; reaplicar via install/doctor).

---

## Contexto

A mantenedora relatou que conectar o controle não abria a GUI ("nosso mini
aplicativo não funcionou"). O hotplug-GUI nunca funcionou em nenhuma forma.

## Diagnóstico (causa-raiz)

`assets/73-ps5-controller-hotplug.rules:16-17` e
`assets/74-ps5-controller-hotplug-bt.rules:22-23` setavam
`ENV{SYSTEMD_USER_WANTS}="hefesto-gui-hotplug.service"` (nome **curto**), mas a
unit real instalada é `hefesto-dualsense4unix-gui-hotplug.service` (longo, ver
`assets/hefesto-dualsense4unix-gui-hotplug.service` e `install.sh`). O systemd
--user tentava encadear uma unit inexistente → hotplug silenciosamente falhava.
Os comentários das regras também citavam o nome curto e um arquivo companheiro
inexistente.

## Decisão / Entrega

Trocar `hefesto-gui-hotplug.service` → `hefesto-dualsense4unix-gui-hotplug.service`
nas 4 linhas de regra (USB 0ce6/0df2 + BT 0CE6/0DF2) e nos comentários. Como a
correção vive **só** em `assets/`, todas as formas que copiam de lá
(nativo via `scripts/install_udev.sh`, `.deb` via `scripts/build_deb.sh`, Arch via
`PKGBUILD`, flatpak via bundle) herdam o conserto.

## Critérios de aceite

- [ ] `grep -rn 'hefesto-gui-hotplug' assets/` retorna vazio.
- [ ] `scripts/check_packaging_parity.sh` passa.
- [ ] `scripts/doctor.sh` mostra `[ OK ] 73/74: hotplug aponta para hefesto-dualsense4unix-gui-hotplug.service` após reaplicar as regras.
- [ ] Smoke real: conectar o DualSense abre a GUI (hotplug habilitado).

## Arquivos tocados

- `assets/73-ps5-controller-hotplug.rules`
- `assets/74-ps5-controller-hotplug-bt.rules`

## Notas para o executor

- Reaplicar nas instalações existentes: `sudo bash scripts/install_udev.sh`
  (idempotente, sobrescreve) — ou via reinstalação / `scripts/doctor.sh --fix`.
- O `doctor.sh` ganhou uma checagem dedicada que detecta o nome errado em regras
  já instaladas (ver [[FEAT-DOCTOR-HEALTHCHECK-01]]).

## Proof-of-work runtime

```bash
sudo bash scripts/install_udev.sh && bash scripts/doctor.sh | grep hotplug
journalctl --user -u hefesto-dualsense4unix-gui-hotplug.service -n 20
```

## Fora de escopo

- Política de autosuspend BT (a regra 72 cobre só USB).
