# FEAT-INSTALL-COSMIC-APPLET-INTEGRATION-01 — Applet COSMIC no install.sh + ícone corrigido

**Tipo:** feat (instalação) + fix (ícone do .desktop).
**Wave:** V3.7 — Recuperação de instalação + áudio COSMIC.
**Estimativa:** S — flag + etapa no install.sh + 1 linha do .desktop + justfile.
**Dependências:** nenhuma.
**Status:** DONE (implementado; smoke visual na recuperação).

---

## Contexto

O applet não aparecia na lista "Adicionar miniaplicativo" do COSMIC (capturas da
mantenedora), e instalá-lo exigia um `just install` manual à parte.

## Diagnóstico (causa-raiz)

1. **Ícone não resolvível:** `packaging/cosmic-applet/data/...desktop:9` tinha
   `Icon=com.vitoriamaria.HefestoDualsense4Unix` (sem sufixo), mas só
   `...-symbolic.svg` é instalado. Os applets nativos do COSMIC (ex.:
   `com.system76.CosmicAppletAudio`) usam `Icon=<id>-symbolic`. Ícone não
   resolvido → o COSMIC não lista/renderiza o applet.
2. **Sem integração:** `install.sh` não compilava/instalava o applet; o `just
   install` não rodava `update-desktop-database` (necessário para o COSMIC
   reindexar `/usr/share/applications`).

## Decisão / Entrega

1. **`.desktop`:** `Icon=com.vitoriamaria.HefestoDualsense4Unix-symbolic`.
2. **`justfile`:** alvos `install`/`uninstall` rodam também
   `update-desktop-database /usr/share/applications`.
3. **`install.sh`:** nova flag `--enable-cosmic-applet` (e `--no-cosmic-applet`)
   + etapa 9/10 (opt-in; em COSMIC pergunta). Pré-checa `cargo`+`just`; se
   faltar, `warn` com instrução e **não** aborta. Avisa que a 1ª build do
   libcosmic é longa. Renumeração dos passos para `X/10`.
4. **README** do applet: recomenda `./install.sh --enable-cosmic-applet`.

## Critérios de aceite

- [ ] `scripts/check_packaging_parity.sh` confirma o ícone resolvível.
- [ ] `./install.sh --native --enable-cosmic-applet` compila e instala o applet,
      roda `update-desktop-database`.
- [ ] `scripts/doctor.sh` mostra `[ OK ] ícone do applet resolvível`.
- [ ] Smoke: applet aparece em Configurações → Painel → Miniaplicativos.

## Arquivos tocados

- `packaging/cosmic-applet/data/com.vitoriamaria.HefestoDualsense4Unix.desktop`
- `packaging/cosmic-applet/justfile`
- `packaging/cosmic-applet/README.md`
- `install.sh`

## Notas para o executor

- O applet fala com o daemon via IPC; precisa do CLI instalado e do daemon
  rodando (ou hotplug-GUI) para não ficar "offline".
- Se não listar de primeira: logout/login (o COSMIC cacheia a lista).

## Proof-of-work runtime

```bash
bash scripts/check_packaging_parity.sh
./install.sh --native --enable-cosmic-applet --yes
bash scripts/doctor.sh | grep applet
```

## Fora de escopo

- Empacotar o binário do applet no .deb/Arch (exige Rust no build) — ver
  [[CHORE-PACKAGING-PARITY-ALL-FORMS-01]].
