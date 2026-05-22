# BUG-COSMIC-APPLET-PANEL-VISIBILITY-01 — applet não aparece em Miniaplicativos

**Tipo:** BUG · **Wave:** V3.8 · **Estimativa:** P · **Dependências:** — · **Status:** DONE

## Contexto

Depois de a v3.7.0 integrar o applet COSMIC ao instalador (`FEAT-INSTALL-COSMIC-APPLET-INTEGRATION-01`)
e corrigir o ícone para `-symbolic`, a mantenedora relatou que o applet ainda **não aparece** na guia
*Configurações → Painel → Miniaplicativos* do COSMIC. O guia de referência do applet X-Kill
(`extra-cosmic-xkill-applet`) revelou as causas.

## Diagnóstico

1. **Falta `X-HostWaylandDisplay=true` no `.desktop`.** Applets que interagem com o sistema (áudio,
   janelas, IPC) precisam compartilhar o display Wayland do compositor. Os applets oficiais do COSMIC
   têm essa chave; o nosso não tinha.
2. **Falta ícone PNG 256×256.** Só existia o `-symbolic.svg` (usado no painel). A lista de
   Miniaplicativos mostra o ícone colorido — sem o PNG, fica genérico.
3. **`killall cosmic-panel` ausente.** O `cosmic-panel` só relê a lista de applets ao reiniciar. Sem
   recarregá-lo após instalar/remover, o applet fica "fantasma" — não aparece na lista (ou persiste
   após a remoção). Faltava no `justfile`, e o `uninstall.sh` removia os arquivos sem recarregar.

`Categories=COSMIC;`, `X-CosmicApplet=true`, `NoDisplay=true` e `Comment=` em PT já estavam corretos.

## Decisão / Entrega

- `.desktop`: adicionada a chave `X-HostWaylandDisplay=true`.
- Novo ícone `data/icons/hicolor/256x256/apps/com.vitoriamaria.HefestoDualsense4Unix.png` (256×256,
  derivado do ícone do AppImage).
- `justfile` (`install`/`uninstall`): instala/remove o PNG **e** roda `killall cosmic-panel` ao fim.
- `uninstall.sh`: remove também o PNG e recarrega o `cosmic-panel`. (`install.sh` delega ao
  `just install`, que já recarrega — por isso não foi duplicado lá.)
- `doctor.sh`: novos checks de `X-HostWaylandDisplay` e do PNG 256×256.
- `check_packaging_parity.sh`: passa a exigir `X-HostWaylandDisplay=true` em todo `.desktop` de applet.

## Critérios de aceite

- `check_packaging_parity.sh` verde, incluindo a nova regra.
- `doctor.sh` reporta o applet com `X-HostWaylandDisplay` e PNG presentes após reinstalar.
- Na máquina: após reinstalar + `killall cosmic-panel`, o applet aparece em *Miniaplicativos*.

## Notas / fora de escopo

- O `killall cosmic-panel` roda **sem** sudo (o `cosmic-panel` é processo do usuário) e tolera
  ausência (`|| true`). Se a lista ainda persistir após remover, o caminho é logout/login.
- Não mexe no código Rust do applet — a visibilidade depende só do `.desktop` + ícone + recarga do painel.
