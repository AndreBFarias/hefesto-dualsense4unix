# Agente: v2:a3ca4718c60ff1c1366045491189d99f2e52f2eedac5a5250b943b323cf2fd1d

## report

## MAPA DO WRAPPER hefesto-launch (DEDUP-04)

### String constante e instalação
- `src/hefesto_dualsense4unix/integrations/steam_launch_options.py:61` `WRAPPER_HOME_RELPATH=".local/share/hefesto-dualsense4unix/bin/hefesto-launch"`; `:69-72` `_WRAPPER_INNER` = `sh -c 'W="$HOME/..."; [ -x "$W" ] && exec "$W" "$@"; exec env "$@"'` (degrada sozinho se o wrapper faltar — jogo SEMPRE abre); `:76` `WRAPPER_PREFIX`; `:82` `WRAPPER_LAUNCH = WRAPPER_PREFIX + " %command%"`. Instalado ao vivo: `~/.local/share/hefesto-dualsense4unix/bin/hefesto-launch` (4456 B, 2026-07-17 02:07, executável).
- Botão da GUI: `src/hefesto_dualsense4unix/app/actions/daemon_actions.py:189-215` `compose_launch()` devolve a string CONSTANTE (params flavor/backend deliberadamente ignorados, linha 210); `:249` `on_storm_copy_launch` copia; `:217-225` `_wrapper_installed()`.

### Fluxo de execução do wrapper (assets/hefesto-launch.sh)
1. `:38-42` — `$SteamAppId` ausente/0/não-numérico → nenhuma env.
2. `:44-47` — lê `~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_<appid>.env`, fallback `default.env`; ausente → nenhuma env.
3. `:51-80` — gate de vida: connect+ping JSON-RPC `daemon.status` no socket de PRODUÇÃO por nome exato (`$XDG_RUNTIME_DIR/hefesto-dualsense4unix/hefesto-dualsense4unix.sock`), timeout 1 s, python3 com `LD_LIBRARY_PATH/LD_PRELOAD/PYTHONPATH/PYTHONHOME` limpos só para o helper. Daemon morto/stale → nenhuma env.
4. `:84-92` — allowlist de 5 vars (SDL_GAMECONTROLLER_IGNORE_DEVICES, SDL_JOYSTICK_HIDAPI, PROTON_ENABLE_HIDRAW, __GL_SHADER_DISK_CACHE[_SKIP_CLEANUP]); espelhada em `daemon/launch_env.py:58-64`.
5. `:96-109` — prepende `VAR=VAL` como args e `exec env "$@"` (nunca `exec "$@"` — LaunchOptions pré-existentes `VAR=VAL %command%` viram assignment do env(1)).
Fail-safe por construção: pior caso = controle duplicado, nunca zero controles.

### Env dinâmica materializada pelo daemon (`src/hefesto_dualsense4unix/daemon/launch_env.py`)
- `compose_env()` `:71-106`: nativo→`PROTON_ENABLE_HIDRAW=1` SEM IGNORE; xbox→`SDL_JOYSTICK_HIDAPI=0`+IGNORE `0x054c/0x0ce6`; dualsense com TODOS vpads uhid→`PROTON_ENABLE_HIDRAW=1`+IGNORE; dualsense com QUALQUER vpad uinput/emulação off→só shader preload (sem IGNORE).
- `materialize_launch_env()` `:261-330`: regrava `default.env` + `steam_app_<appid>.env` por perfil com `steam_app_*` no window_class (`_steam_profiles` :143-152, `_env_for_profile` :189-241); omite IGNORE do default se existe perfil nativo/desktop fora da antecipação (`_nativos_fora_da_antecipacao` :155-186 — evita ZERO controles quando autoswitch ativar esse perfil); apaga steam_app_*.env stale (:317-320); loga `dedup_broken` (:285) e `launch_env_materializado` (:321).
- Gatilhos de regravação: `daemon/subsystems/gamepad.py:75,521,550,593` (start/stop/promote da emulação), `daemon/subsystems/coop.py:467-476` (spawn/teardown de vpad co-op), `daemon/ipc_handlers.py:264-267` e `:1248-1251` (profile.switch/daemon.reload), `:1254-1273` (`launch_env.refresh` — a GUI avisa após save/delete/import de perfil), registrado em `daemon/ipc_server.py:116`.
- ESTADO AO VIVO (20:15 de hoje): `default.env` e `steam_app_1599660.env` ambos com `PROTON_ENABLE_HIDRAW=1` + `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` + shader cache; estado `native=False emulacao=True mascara=dualsense backends=['uhid','uhid']`. Ou seja: para jogo lançado PELO wrapper a dedup está armada; P2 (plug direto sem wrapper) é o degradê projetado "duplicado > zero" — o jogo dela não tem a launch option aplicada.

## DIÁLOGO "JOGO NÃO MAPEADO" (DEDUP-05)

NÃO é o wrapper que abre o diálogo, nem zenity, nem processo separado: é a PRÓPRIA GUI (mesmo processo GTK3, PID 10464). O wrapper roda mudo. Detecção e exibição moram em `src/hefesto_dualsense4unix/app/actions/launch_wrapper_dialog.py` (mixin `LaunchWrapperDialogMixin`), enganchado no tick lento de 2 Hz: `app/app.py:328-339` `_render_slow_state()` chama `_maybe_prompt_wrapper_dialog(state)`.

Fluxo: `extract_steam_appid()` :81-93 extrai o appid do `state_full.window_detect_last_class` (regex `steam_app_(\d+)`, vindo do detector de janela do daemon) → `wrapper_dialog_decision()` :96-151 (gates: sem diálogo aberto, emulação ativa `mode_of_state==MODE_GAMEPAD`, anti-spam 1x/appid/sessão, dispensa persistida, sem popup GTK aberto) → `_wrapper_dialog_read_vdf()` :324-353 lê o vdf 1x por appid em worker chamando `appid_needs_wrapper()` (`integrations/steam_launch_options.py:351-374` — True se nenhum localconfig.vdf elegível não-sandbox contém `WRAPPER_PREFIX` nas LaunchOptions do appid; jogo sem entrada = precisa) → `_show_wrapper_dialog()` :388-393.

Construção: `_build_wrapper_dialog()` :357-386 — `Gtk.MessageDialog` (GTK3; o arquivo faz `gi.require_version("Gtk","3.0")` na linha 46 — a GUI inteira é GTK3, NÃO GTK4/libadwaita; Adw.StyleManager não existe aqui), NÃO-modal, `transient_for=window`, botões "Copiar opções"(101)/"Não perguntar para este jogo"(102)/"Fechar", labels do message area viram selecionáveis (:378-381). Dispensa persiste em `launch_dialog_dismissed.json` no config dir (:158-224).

## P5 — POR QUE O DIÁLOGO ABRE CLARO (causa-raiz CONFIRMADA com provas ao vivo)

O escuro do app NÃO vem do tema GTK do sistema; vem do CSS Drácula:
1. `app/theme.py:46-62` carrega `src/hefesto_dualsense4unix/gui/theme.css` screen-wide com `PRIORITY_APPLICATION`, mas TODAS as regras de superfície são ESCOPADAS à classe `.hefesto-dualsense4unix-window` (theme.css:4-7 fundo `#282a36`/texto `#f8f8f2`; :13 botões; :191-196 boxes). A classe é adicionada SÓ à janela principal (`theme.py:63`).
2. `_build_wrapper_dialog()` NUNCA adiciona essa classe ao MessageDialog (toplevel separado) → nenhuma regra Drácula casa → o diálogo cai no tema-base do processo.
3. E o tema-base do processo é CLARO por uma cadeia específica: `app/main.py:14-48` FORÇA `GDK_BACKEND=x11` (XWayland) em sessão COSMIC (workaround cosmic-epoch#2497 dos popups; confirmado no environ do PID 10464: `GDK_BACKEND=x11`, `DISPLAY=:1`). Probes ao vivo com o venv do projeto: sob Wayland o GTK3 resolve `gtk-theme-name=adw-gtk3-dark` (escuro, instalado); sob X11 resolve `gtk-theme-name=Yaru` (via XSettings do `cosmic-settings-daemon`, PID 2584) com `prefer-dark=False` — e **Yaru NÃO está instalado** (`/usr/share/themes` = adw-gtk3, adw-gtk3-dark, Default, Emacs, Raleigh) → GTK cai no Adwaita builtin CLARO.
4. `theme.py:40-44` seta `gtk-application-prefer-dark-theme=True` como "camada defensiva", mas sob X11 o XSettings é dono das propriedades do GtkSettings (re-asseveração do cosmic-settings-daemon pode clobrar o valor) e o bug é empiricamente conhecido no repo: `app/gui_dialogs.py:245-247` documenta "sem isso o diálogo herdava o tema claro do sistema (branco no COSMIC)".

Precedente do fix NO PRÓPRIO CÓDIGO: `show_external_controller()` (`app/gui_dialogs.py:239-249`) resolve o mesmo bug com `dialog.get_style_context().add_class("hefesto-dualsense4unix-window")` dentro de `contextlib.suppress(Exception)`.

Opções de fix (em ordem de preferência):
(a) 1 linha em `_build_wrapper_dialog` (`launch_wrapper_dialog.py`, após a construção na linha 365-371): `dialog.get_style_context().add_class("hefesto-dualsense4unix-window")` — fundo/texto pelo root rule, botões pela :13, boxes internos pela :191-196; labels herdam a cor. Atualizar `tests/unit/test_launch_wrapper_dialog.py` para afirmar a classe.
(b) Complementar/estrutural: bloco top-level `messagedialog`/`window.dialog` no theme.css (mesmo padrão dos menus toplevel, theme.css:138-182) — cobriria qualquer diálogo futuro sem classe; não vaza para outros processos (provider é por-screen deste processo, argumento já documentado em theme.css:142-144).
(c) NÃO confiar em prefer-dark/GTK_THEME como fix: sob XWayland + cosmic-settings-daemon o XSettings manda, Yaru ausente, e o app é GTK3 (sem Adw.StyleManager).

## HIPÓTESE CRUZADA PARA O AGENTE DE LIGHTBAR (P1: verde-limão alternando com azul)

A nota de memória "autoswitch desliga a emulação quando a janela vira unknown" está DESATUALIZADA: UX-01 implementou histerese em `src/hefesto_dualsense4unix/profiles/autoswitch.py:101-121` — leitura SEM informação (`_tick_sem_informacao` :149-167: wm_class ''/'unknown' E wm_name vazio E exe_basename vazio) pula o tick INTEIRO e retém o perfil corrente, sem TTL. PORÉM há caminho residual documentado (:153-158): janela X com wm_class vazio mas COM título/exe NÃO conta como "sem informação" → entra no `select_for_window` → fallback MatchAny pode ativar após debounce 500 ms (:137,146-147) → `_activate` → `apply_profile_mode` → stop/start da emulação → teardown/rebuild do vpad → re-assert de lightbar. Cada transição dessas TAMBÉM regrava launch_env (`gamepad.py:521/550/593`), então o journal tem marcadores temporais: correlacionar `autoswitch_window_info_unavailable`, `profile_activated`, `launch_env_materializado` com os instantes dos flips. Azul = default de firmware do hid_playstation (reset de claim/rebind); verde-limão = cor de palette/slot escrita pelo daemon → dois escritores plausíveis: reassert do daemon (PALETA-NO-WAKE reassert-on-connect) vs. driver/firmware no rebind. Se o journal mostrar flips SEM eventos de autoswitch, o race é interno ao subsistema de LED (fora do meu escopo).

## key_files

- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/launch_wrapper_dialog.py:357-386, 289-322, 96-151 — Constrói o Gtk.MessageDialog do P5 (_build_wrapper_dialog) SEM add_class('hefesto-dualsense4unix-window') — causa-raiz do tema claro; gatilho e decisão pura do diálogo
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/gui_dialogs.py:239-249 — Precedente do fix: show_external_controller adiciona a classe ao dialog com comentário documentando o mesmo bug (branco no COSMIC)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/theme.py:22-77 — apply_theme: CSS Drácula screen-wide PRIORITY_APPLICATION escopado à classe; prefer-dark=True é só camada defensiva (clobrada sob X11/XSettings)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/gui/theme.css:4-7, 13-19, 138-182, 191-196 — Todas as regras de superfície escopadas a .hefesto-dualsense4unix-window; bloco de menus top-level é o padrão para toplevels sem classe (opção b do fix)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/main.py:14-48 — Força GDK_BACKEND=x11 em COSMIC ANTES dos imports — é o que faz o processo resolver tema Yaru (não instalado) → Adwaita claro em vez de adw-gtk3-dark
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/assets/hefesto-launch.sh:35-109 — O wrapper inteiro: decide_envs (appid → envfile → gate de vida IPC 1s → allowlist) e exec env; instalado em ~/.local/share/hefesto-dualsense4unix/bin/hefesto-launch
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/launch_env.py:58-106, 155-186, 261-330 — Allowlist espelhada, compose_env (regras IGNORE/HIDRAW por máscara+backend) e materialize_launch_env (default.env + por-appid, omissão de IGNORE por perfil nativo)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/steam_launch_options.py:61-114, 351-374 — WRAPPER_LAUNCH/WRAPPER_PREFIX (string constante com degradação embutida) e appid_needs_wrapper (detecção de jogo não mapeado lendo localconfig.vdf)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/app.py:328-339 — _render_slow_state (tick 2 Hz) chama _maybe_prompt_wrapper_dialog — único ponto de engate do diálogo
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/profiles/autoswitch.py:94-167 — Histerese UX-01 (unknown retém perfil) + caminho residual :153-158 que ainda permite MatchAny→troca de perfil→rebuild de vpad — hipótese cruzada para a lightbar alternando
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:75, 88-98, 521, 550, 593 — Pontos onde start/stop da emulação regravam launch_env — marcadores no journal para correlacionar com flips de lightbar
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/daemon_actions.py:189-269 — compose_launch devolve a string constante do wrapper; on_storm_copy_launch e _wrapper_installed
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/tests/unit/test_launch_wrapper_dialog.py — Testes do diálogo — precisam ganhar asserção da classe CSS quando o fix (a) for aplicado

## hypotheses

- P5 causa-raiz (CONFIRMADA): _build_wrapper_dialog (launch_wrapper_dialog.py:357-386) não adiciona a classe .hefesto-dualsense4unix-window ao Gtk.MessageDialog; todo o CSS Drácula (gui/theme.css) é escopado a essa classe, então o diálogo cai no tema-base do processo — que é Adwaita CLARO porque main.py:14-48 força GDK_BACKEND=x11 em COSMIC e sob X11 o XSettings do cosmic-settings-daemon aponta gtk-theme-name=Yaru, que NÃO está instalado (provado por probe ao vivo: Wayland resolve adw-gtk3-dark, X11 resolve Yaru+prefer-dark=False). Fix de 1 linha já tem precedente idêntico em gui_dialogs.py:239-249.
- P5 secundária: o gtk-application-prefer-dark-theme=True de theme.py:42 não segura o escuro sob X11 porque valores vindos de XSettings re-asseveram as propriedades do GtkSettings (e mesmo valendo, Yaru ausente cai em Adwaita, não nos tons Drácula) — por isso confiar em prefer-dark não é fix; a classe CSS é determinística.
- Cruzada para P1 (lightbar verde-limãoazul): flips podem coincidir com ativações de perfil pelo caminho residual do autoswitch (autoswitch.py:153-158 — janela X com wm_class vazio mas título/exe presentes escapa da histerese UX-01 e ativa MatchAny após 500 ms) → apply_profile_mode → stop/start da emulação → rebuild do vpad → re-assert de LED; azul = default de firmware hid_playstation no rebind, verde-limão = cor de slot/palette do daemon. Verificável no journal correlacionando autoswitch_window_info_unavailable/profile_activated/launch_env_materializado com os instantes dos flips.
- P2 é comportamento projetado, não bug do wrapper: sem a launch option aplicada no jogo, o wrapper nem roda e o default.env (que hoje carrega IGNORE 0x054c/0x0ce6 + PROTON_ENABLE_HIDRAW=1, backends ['uhid','uhid']) nunca é lido — 'duplicado > zero controles' é o degradê deliberado documentado em launch_env.py:6-9 e no próprio texto do diálogo DEDUP-05.

## open_questions

- O journal do daemon mostra profile_activated/autoswitch_window_info_unavailable/launch_env_materializado nos instantes exatos dos flips de lightbar do DualSense branco USB? (correlação decide se o autoswitch é o gatilho ou se o race é interno ao subsistema de LED)
- O cosmic-settings-daemon re-assevera XSettings em runtime clobrando o prefer-dark setado pelo app? (irrelevante se o fix da classe CSS for adotado, mas explica por que a 'camada defensiva' de theme.py nunca funcionou para toplevels sem classe)
- O jogo que ela está jogando hoje tem a launch option do wrapper aplicada no localconfig.vdf? (appid_needs_wrapper diria; steam_app_1599660.env existe só para o Sackboy — P2 sugere que o jogo atual NÃO está mapeado)
- Vale instalar o tema Yaru ou trocar o XSettings para adw-gtk3-dark como mitigação de sistema? (fora do repo; a classe CSS resolve sem tocar no sistema)
