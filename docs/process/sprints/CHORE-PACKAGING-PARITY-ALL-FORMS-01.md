# CHORE-PACKAGING-PARITY-ALL-FORMS-01 — Mesmas correções em todas as formas de empacotamento

**Tipo:** chore (paridade + guarda anti-regressão).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — verificação + 1 guard + ajuste de mensagem do postrm.
**Dependências:** as demais sprints da wave (corrige na fonte compartilhada).
**Status:** DONE (verificado; guard verde).

---

## Contexto

Pedido explícito da mantenedora: "as demais formas de instalação precisam ser
atualizadas pra não termos os bugs nelas também". Formas: nativo, `.deb`, Arch,
flatpak, AppImage, applet COSMIC.

## Diagnóstico (verificado)

- O nome de unit errado do hotplug vivia **só** em `assets/73,74` → o conserto
  ([[BUG-UDEV-HOTPLUG-UNIT-NAME-MISMATCH-01]]) é herdado por quem copia de
  `assets/`: `scripts/build_deb.sh:144-145` (.deb), `packaging/arch/PKGBUILD:94-99`
  (Arch), e o bundle flatpak (`flatpak/...yml`).
- A migração curto→longo roda no **boot do app** → `.deb`/Arch herdam sem mexer
  no postinst.
- `packaging/debian/postrm` citava só o caminho longo de config.
- Faltava uma guarda automática contra regressão.

## Decisão / Entrega

1. **Verificação** (sem mudança necessária): `build_deb.sh` e `PKGBUILD` copiam
   `assets/70..74-*.rules`; o flatpak copia os rules do source no build → todos
   herdam a correção do hotplug ao rebuildar.
2. **`packaging/debian/postrm`:** mensagem alinhada — config preservada, cobrindo
   curto **e** longo.
3. **Guard anti-regressão** `scripts/check_packaging_parity.sh`: falha se o nome
   de unit errado reaparecer em `assets/`/`packaging/`/`flatpak/`, ou se um
   `.desktop` de applet tiver `Icon=` sem o arquivo de ícone versionado ao lado.
   Rodável local e em CI.

## Critérios de aceite

- [ ] `scripts/check_packaging_parity.sh` retorna 0. **Validado**.
- [ ] `.deb`/Arch/flatpak, ao rebuildar, trazem regras 73/74 com a unit correta.

## Arquivos tocados

- `scripts/check_packaging_parity.sh` (novo)
- `packaging/debian/postrm`

## Notas para o executor

- **Flatpak:** sandbox não enxerga o caminho curto legado por padrão → migração é
  best-effort lá; documentado. Empacotar o binário do applet no .deb/Arch fica
  fora de escopo (exige Rust no build).
- **Namespace flatpak `br.andrefarias.*`** vs `com.vitoriamaria.*`: divergência
  conhecida; renomear app-id quebra updates → fora de escopo (só documentado).
  O `purge.sh`/`uninstall.sh` já cobrem a remoção do `br.andrefarias.Hefesto`.

## Proof-of-work runtime

```bash
bash scripts/check_packaging_parity.sh
grep -rn '7[0-4]-ps5\|71-uinput' scripts/build_deb.sh packaging/arch/PKGBUILD
```

## Fora de escopo

- Renomear o app-id flatpak; empacotar o applet Rust no .deb/Arch.
