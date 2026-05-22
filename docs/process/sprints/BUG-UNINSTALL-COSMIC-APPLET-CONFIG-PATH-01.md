# BUG-UNINSTALL-COSMIC-APPLET-CONFIG-PATH-01 — uninstall deixava rastros e mirava o config errado

**Tipo:** fix (uninstall/limpeza) + segurança de dados.
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — edições no `uninstall.sh`.
**Dependências:** [[CHORE-CONFIG-MIGRATE-LEGACY-SHORT-PATH-01]] (caminhos).
**Status:** DONE (implementado; smoke na recuperação).

---

## Contexto

A mantenedora rodou `uninstall.sh` "pra ver se resolvia mas não resolveu":
sobravam o applet COSMIC e regras, e o "PC ficou sujo".

## Diagnóstico (causa-raiz)

1. **Applet órfão:** o applet é instalado à parte por `packaging/cosmic-applet`
   (`just install`) em `/usr/local/bin/...-applet`,
   `/usr/share/applications/com.vitoriamaria.HefestoDualsense4Unix.desktop` e o
   ícone em `/usr/share/icons/...`. O `uninstall.sh` **não conhecia** esses
   caminhos → sobreviviam.
2. **Caminho de config errado:** `uninstall.sh:174` só removia o **longo**
   `~/.config/hefesto-dualsense4unix`; o config real estava no **curto**
   `~/.config/hefesto` → nunca limpo.
3. **Regra 74 esquecida:** o bloco `--udev` removia 70/71/72/73 + `.conf`, mas
   não a `74-ps5-controller-hotplug-bt.rules`.
4. **Wipe de config por padrão:** sem `--keep-config`, apagava os perfis sem
   backup — risco de perda de dados.

## Decisão / Entrega

- **Remover artefatos do applet** (gated por `command -v sudo` e "só se existir")
  + `gtk-update-icon-cache`/`update-desktop-database` de sistema.
- **Incluir a regra 74** no bloco `--udev`.
- **Inverter o default:** config **preservada por padrão**; novo `--purge-config`
  apaga, sempre com **backup** (`~/.config/hefesto-dualsense4unix.backup-<epoch>/`),
  cobrindo curto **e** longo (`hefesto` + `hefesto-dualsense4unix`).
- **Remover o drop-in do WirePlumber** (só o arquivo, nunca o dir).

## Critérios de aceite

- [ ] Após `uninstall.sh --udev --yes`: sem applet em `/usr/local`+`/usr/share`,
      sem regras 70-74 em `/etc/udev/rules.d`, perfis **preservados**.
- [ ] `--purge-config` apaga curto+longo e cria backup antes.
- [ ] `bash -n uninstall.sh` ok.

## Arquivos tocados

- `uninstall.sh`

## Notas para o executor

- `scripts/purge.sh` chama `uninstall.sh --keep-config --udev --yes` e reforça
  (ver [[CHORE-PURGE-ALL-INSTALL-FORMS-01]]).

## Proof-of-work runtime

```bash
bash -n uninstall.sh
./uninstall.sh --udev --yes   # conferir ausência de rastros + perfis intactos
```

## Fora de escopo

- Remover deps pip --user (mantido como nota informativa, como antes).
