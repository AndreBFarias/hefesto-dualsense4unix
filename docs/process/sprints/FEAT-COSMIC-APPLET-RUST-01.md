# FEAT-COSMIC-APPLET-RUST-01 — Applet nativo COSMIC em Rust + libcosmic

**Tipo:** feat (integração nativa COSMIC — o "tray" da mantenedora).
**Wave:** V3.6 — acabamento COSMIC round 2 (promovida de V3.4 forward-looking).
**Estimativa:** XL — 5–10 iterações + toolchain Rust/libcosmic.
**Dependências:** IPC Unix socket estável (existe desde v2.x). Toolchain Rust.
**Status:** PROTOCOL_READY (subprojeto `packaging/cosmic-applet/` criado e
verde: `cargo build --release`, `cargo clippy --release -- -D warnings` e
`cargo fmt --check` passam; testes do cliente IPC verdes; `.desktop` com as 3
chaves COSMIC; ícone symbolic. Falta só o smoke visual manual no hardware COSMIC
da mantenedora — `just install` + adicionar aos Miniaplicativos. Era READY,
promovida por pedido direto da mantenedora, 2026-05-21).

---

## Contexto

A mantenedora reportou: **"nos miniaplicativos do COSMIC ele não aparece. isso
seria o nosso tray."** Hoje o Hefesto usa `AppIndicator`/SNI
(`app/tray.py`), que — quando aparece — fica **dentro** do applet "Área de status"
do painel, e **não** na lista "Miniaplicativos" das Configurações do COSMIC.

A mantenedora já resolveu exatamente isso em outro projeto dela,
**`extra-cosmic-xkill-applet`** (`~/Desenvolvimento/extra-cosmic-xkill-applet/`),
que **aparece** na lista (visto como "X-Kill / Adicionar"). Esta sprint replica
aquele padrão: um **applet nativo COSMIC em Rust + libcosmic**, fino, que mostra
um ícone no painel e um popover, e fala com o **daemon Python via o IPC existente**.

> Diferença-chave (confirmada na pesquisa): um *applet nativo COSMIC* registra-se
> via `.desktop` com `X-CosmicApplet=true` e aparece em Configurações → Painel →
> Miniaplicativos; um *ícone SNI/AppIndicator* depende do `cosmic-applet-status-area`
> e aparece dentro dele. A mantenedora quer o **primeiro**.

## Template de referência (espelhar)

Projeto `extra-cosmic-xkill-applet` (mesma autora, já validado no COSMIC dela):

- **Stack**: Rust 2021 + `libcosmic` (git pop-os/libcosmic, branch master,
  features `["applet", "tokio", "wayland", "winit", "multi-window"]`).
- **`main.rs`**: `cosmic::applet::run::<App>()` (NÃO `app::run`).
- **`app.rs`**: implementa `cosmic::Application`; `view()` usa
  `self.core.applet.icon_button("<icon-name-symbolic>").on_press(Message::...)`;
  popover via `core.applet`.
- **`data/<app-id>.desktop`** instalado em `/usr/share/applications/`:
  ```ini
  [Desktop Entry]
  Name=Hefesto - Dualsense4Unix
  Comment=Gatilhos, perfis e bateria do DualSense
  Type=Application
  Exec=hefesto-dualsense4unix-applet
  Icon=<app-id>
  Terminal=false
  NoDisplay=true
  Categories=COSMIC;
  Keywords=COSMIC;Applet;DualSense;Gamepad;Hefesto;
  StartupNotify=true
  X-CosmicApplet=true
  ```
  > Chaves obrigatórias para aparecer nos Miniaplicativos: `X-CosmicApplet=true`,
  > `NoDisplay=true`, `Categories=COSMIC;`. (O `X-HostWaylandDisplay=true` do xkill
  > NÃO é necessário aqui — o Hefesto applet não gerencia janelas, só fala IPC.)
- **`justfile`**: `cargo build --release` + `install -Dm755 target/release/...
  /usr/bin/` + `.desktop` em `/usr/share/applications/` + ícone em
  `/usr/share/icons/hicolor/scalable/apps/` + `gtk-update-icon-cache`.

Leia o projeto inteiro antes de começar: `Cargo.toml`, `justfile`, `data/*.desktop`,
`src/main.rs`, `src/app.rs`.

## Protocolo IPC (cliente em Rust)

O daemon Python expõe **JSON-RPC 2.0 newline-delimited (UTF-8) sobre Unix socket**.
Espelhar `src/hefesto_dualsense4unix/cli/ipc_client.py`:

- **Socket**: `ipc_socket_path()` → confirmar em
  `src/hefesto_dualsense4unix/utils/xdg_paths.py`; é
  `$XDG_RUNTIME_DIR/hefesto-dualsense4unix/hefesto-dualsense4unix.sock`.
- **Request** (1 linha + `\n`):
  `{"jsonrpc":"2.0","id":<int>,"method":"<m>","params":{...}}`
- **Response** (1 linha): `{"jsonrpc":"2.0","id":<int>,"result":{...}}` ou
  `{"jsonrpc":"2.0","id":<int>,"error":{"code":<int>,"message":"<s>"}}`
- **Métodos usados pelo applet** (ver `daemon/ipc_handlers.py`):
  - `daemon.status` → `{connected, transport, active_profile, battery_pct}`
  - `daemon.state_full` → estado completo (bateria, sticks, botões, perfil, rumble)
  - `profile.list` → `{profiles:[{name, priority, match_type}]}`
  - `profile.switch` `{name:"<perfil>"}` → `{active_profile}`
- **Sugestão Rust**: `tokio::net::UnixStream` + `BufReader::read_line` +
  `serde_json`. Timeout curto (~250 ms). Se o socket não existir, daemon offline →
  ícone "cinza/desconectado".

## UI mínima do applet

- Ícone no painel refletindo estado: cinza = daemon offline; normal = conectado;
  alerta = bateria < 15%.
- Click → popover com: bateria (% + USB/BT), perfil ativo, **lista clicável de
  perfis** (click → `profile.switch`), e um item "Abrir painel" que executa
  `hefesto-dualsense4unix-gui` (spawn).
- Refresh do estado a ~1–2 Hz via `daemon.state_full` enquanto o popover está
  aberto (e atualização leve do ícone em background).

## Estrutura proposta

```
packaging/cosmic-applet/
├── Cargo.toml                 # libcosmic feature "applet" + tokio + serde
├── justfile                   # build/install/uninstall (espelha xkill)
├── README.md                  # como compilar/instalar/adicionar ao painel
├── data/
│   ├── io.github.[REDACTED].HefestoDualsense4Unix.desktop
│   └── icons/hicolor/scalable/apps/<app-id>-symbolic.svg
└── src/
    ├── main.rs                # cosmic::applet::run::<App>()
    ├── app.rs                 # cosmic::Application (view/update/subscription)
    └── ipc.rs                 # cliente JSON-RPC newline sobre UnixStream
```

> App-id sugerido: `io.github.[REDACTED].HefestoDualsense4Unix` (ou o padrão
> `com.vitoriamaria.*` do xkill — manter consistência com o que já funciona no
> COSMIC dela). Bin: `hefesto-dualsense4unix-applet`. Ícone: derivar do ícone
> existente do app (martelo) em `assets/` para um `-symbolic.svg`.

## Critérios de aceite

1. `cargo build --release` em `packaging/cosmic-applet/` produz binário nativo
   x86_64-linux. `cargo clippy` sem warnings; `cargo fmt --check` limpo.
2. Após `just install`, o applet aparece em **Configurações → Painel →
   Miniaplicativos** como "Hefesto - Dualsense4Unix" com botão "Adicionar".
3. Adicionado ao painel: ícone visível; estado reflete daemon (offline→cinza).
4. Click abre popover com bateria + perfil ativo + lista de perfis clicável.
5. Click num perfil dispara `profile.switch` via IPC; popover atualiza < 500 ms.
6. "Abrir painel" lança a GUI.
7. Daemon offline (socket ausente) → applet degrada gracioso (sem crash).
8. `README.md` com passos de build/instalação e nota sobre `cargo` necessário.

## Notas para o executor

- **Toolchain**: confirme `cargo --version` (a mantenedora compila o xkill, então
  deve existir). Se faltar build-deps de `libcosmic`/Wayland, instale via apt —
  senha sudo local `***SENHA-REMOVIDA-DO-HISTORICO***` (use sem perguntar; só confirme ações destrutivas).
  A build de libcosmic é **longa** na primeira vez — rode em background e seja
  paciente; não aborte cedo.
- **Isolamento**: trabalhe **somente** em `packaging/cosmic-applet/` (diretório
  novo). **NÃO** edite `install.sh`, `packaging/debian/*`, `pyproject.toml`,
  `CHANGELOG.md` nem `SPRINT_PLAN_COSMIC.md` nesta sprint — integração ao
  empacotamento (.deb/Flatpak) e ao `install.sh` fica como follow-up
  (`FEAT-COSMIC-APPLET-PACKAGING-01`). Isso evita conflito com sprints paralelas.
- A validação de runtime (aparecer nos Miniaplicativos, popover, troca de perfil)
  é **manual no hardware COSMIC** — entregue o build verde + `.desktop` correto +
  README, e deixe o smoke visual documentado para a mantenedora rodar.
- Atualize só o `Status:` deste arquivo ao concluir (PROTOCOL_READY se faltar só o
  smoke manual; MERGED só após validação visual).

## Out-of-scope desta sprint

- Empacotamento (.deb/Flatpak/install.sh) — sprint `FEAT-COSMIC-APPLET-PACKAGING-01`.
- Widget de painel always-on (bateria/perfil sem clique) — sprint
  `FEAT-COSMIC-PANEL-WIDGET-01` (119, depende desta).
- Atalhos globais via cosmic-settings — `FEAT-COSMIC-GLOBAL-SHORTCUTS-01` (118).
- O tray GTK3/AppIndicator (`app/tray.py`) continua como fallback para GNOME/KDE.

---

*Promovida de stub (2026-05-16) para READY em 2026-05-21 com template do
`extra-cosmic-xkill-applet` + contrato IPC concreto.*
