# Mapa: as interfaces e a suíte de testes

- **Levantado em:** 26-27/07/2026
- **Escopo:** `gui/`, `app/`, `tui/`, `cli/`, `packaging/cosmic-applet/`, `po/`,
  e `tests/` inteiro

## São cinco superfícies de interface, não três

| Superfície | Toolkit | Entrada | Linhas |
|---|---|---|---|
| GUI principal | **GTK3 + Glade (PyGObject)** | `hefesto-dualsense4unix-gui` | ~13.500 py + 2.783 glade + 1.079 css |
| Tray / SNI | GTK3 + libayatana-appindicator | embutido na GUI e `cli/cmd_tray.py` | 463 |
| Janela compacta | GTK3 | fallback do tray | 317 |
| TUI | Textual | `hefesto-dualsense4unix tui` | 466 |
| Applet COSMIC | **Rust + libcosmic/iced** | painel do COSMIC | 1.745 rs |

## `gui/` é só recurso; a lógica mora em `app/`

`gui/` contém apenas o `main.glade` (2.783 linhas, 205 `id=`, 66 handlers), o
`theme.css` (1.079 linhas, paleta Drácula em `@define-color`), a logo e dois
widgets desenhados em Cairo.

Quem monta a janela é `app/app.py`: a classe `HefestoApp` herda **11 mixins**, um
por área, e o mapa de sinais Glade para método é um dicionário literal de ~100
entradas em `app/app.py:247-349`.

Módulos de apoio que valem conhecer:

- **`app/draft_config.py`** (930 linhas) — o *rascunho*: o estado editado na tela
  antes de ir ao daemon. É a peça central das quatro correções da ABAS-01, porque
  a aba Perfis era a única superfície que editava e persistia **sem nunca ler nem
  escrever** o rascunho.
- **`app/actions/mode_transition.py`** — dono único da troca de modo. Existe
  porque Início e Emulação tinham sequências divergentes de IPC.
- **`app/mic_monitor.py`** — captura de nível só com a aba Status visível.

## As nove abas

| # | Aba | Container | Mixin | Linhas |
|---|---|---|---|---|
| 1 | Início | `tab_home_box` | `home_actions.py` | 1.209 |
| 2 | Status | `tab_status_box` | `status_actions.py` | 1.607 |
| 3 | Gatilhos | `tab_triggers_box` | `triggers_actions.py` | 610 |
| 4 | Lightbar | `tab_lightbar_box` | `lightbar_actions.py` | 899 |
| 5 | Rumble | `tab_rumble_box` | `rumble_actions.py` | 577 |
| 6 | Perfis | `profiles_paned` | `profiles_actions.py` | 1.419 |
| 7 | Sistema | `daemon_box` | `daemon_actions.py` | 1.873 |
| 8 | Emulação | `emulation_box` | `emulation_actions.py` | 932 |
| 9 | Navegação DSX | `tab_navegacao_dsx` | `input_actions.py` + `mouse_actions.py` | — |

A aba **Início** tem só 6 widgets no glade; o resto é **construído em código**
(`home_actions.py:422-660`). A **Status** monta um `ControllerCard` por controle
conectado, em grade de 2 colunas.

**Navegação DSX** é a fusão das antigas abas Mouse e Teclado em duas colunas — e
o glade registra o porquê (`:2344-2366`): empilhadas, a soma inflava o mínimo do
`GtkNotebook`, que adota o maior mínimo entre todas as páginas, engordando
**todas** as abas.

## Como a janela fala com o daemon

Cadeia: **GUI -> `app/ipc_bridge.py` -> `cli/ipc_client.py` -> socket ->
`daemon/ipc_server.py` -> `daemon/ipc_handlers.py`**.

- `ipc_bridge.py` é o **único** ponto de contato. `_run_call` é bloqueante e
  **proibido na thread do GTK**; `call_async` despacha para um executor de **uma
  thread** e re-posta via `GLib.idle_add`. Tempo limite padrão de **0,25 s**,
  cobrindo conexão e leitura.
- `_safe_call` captura **só** `FileNotFoundError`, `ConnectionError`, `IpcError`
  e `OSError` — bug real propaga, de propósito.
- **33 métodos IPC** registrados (`daemon/ipc_server.py:99-144`); a tabela do
  documento de protocolo lista 10.
- Tray e janela compacta usam o **mesmo** caminho de dados. O applet COSMIC
  reimplementa o protocolo em Rust (`packaging/cosmic-applet/src/ipc.rs`, 705
  linhas), com paridade de modo travada por teste que lê o `.rs` **como texto**.

## A TUI é esquelética

Uma tela só (`MainScreen`), três widgets, dois atalhos. **`tui/screens/__init__.py`
tem 0 bytes** — o diretório de telas existe e está vazio. Cobertura: 1 arquivo,
17 testes.

## A árvore da CLI

**14 comandos raiz, 8 sub-apps, ~40 subcomandos.** Typer, tudo em português.

```
status · battery · doctor [--fix|--fix-safe] · led · version · tui · tray
mic <on|off|status|promote|demote|mute|unmute|release|bt|bt-status>
daemon <start|stop|restart|status|pause|resume|enable|disable|install-service|...>
profile <list|show|activate|create|delete|apply|save>
test <trigger|led|rumble>          (direto no hardware, pulando o daemon)
mouse|native|gamepad|coop <on|off|status>
controller <target|list> · plugin <list|reload>
```

Os cinco grupos de estado seguem o mesmo formato `on/off/status [--json]`, com um
`_call_sync` **duplicado em 6 arquivos**, mesma assinatura.

## i18n: infraestrutura completa, catálogos pela metade

A infraestrutura é correta — gettext, `set_translation_domain` no Glade, cinco
caminhos de fallback, catálogos `.mo` embutidos no wheel, extração que varre
`.py` **e** o glade.

O que falta é o texto passar por ela:

- `po/pt_BR.po` e `po/en.po`: 245 entradas cada; **59 vazias em `en`**, 60 em
  `pt_BR`;
- só **9 módulos** importam `_()`; os outros mixins de aba têm o português
  **fixo no código**;
- `utils/i18n.py` não é citado por teste nenhum.

## `novo-layout/` é especificação executável, e está cumprida

Não é mockup morto: é o guia do redesign, e a migração está concluída item a
item — paleta Drácula em `@define-color`, logo e título colorido, botões de rodapé
por papel, sensores na Status, altura dos gatilhos reduzida de 606 para 180 px,
"Detalhes técnicos" removido de Perfis, fusão em Navegação DSX, e teste de
orçamento de altura medindo com `GtkOffscreenWindow`.

**A exceção:** as duas fontes da identidade (`Space Grotesk`, `JetBrains Mono`)
são pedidas pelo CSS e **nunca instaladas** — `install_fonts.sh` existe e o
`install.sh` não o chama.

---

# A suíte de testes

## Números

- **4.926 funções `test_`** em **312 arquivos**, 96.262 linhas — mais teste que
  código (`src/` tem 65.811).
- **4.914 testes em `tests/unit/`** (99,76%), 12 em `tests/core/`.
- **`tests/integration/` e `tests/shell/` estão VAZIOS** desde maio.
- Nenhum marcador customizado; `asyncio_mode = "auto"`.

Distribuição por área dominante: `daemon` 1.042, `app` 903, `core` 680,
**656 testes que não importam nada de `src/`** (testam shell, assets e docs),
`profiles` 632, `integrations` 614.

**A taxonomia de diretórios é ficção**: tudo é `unit/`, inclusive testes que
sobem daemon com asyncio, montam janelas GTK offscreen e fazem grep num
`install.sh` de 133 KB.

## Fixtures de hardware falso

- **`skip_sem_gtk_response`** — o marcador é avaliado **uma vez, num subprocesso
  limpo**, porque o repositório mistura Gtk 3.0 (produção) e 4.0 (fixtures), e
  "Namespace already loaded" derrubava a **coleta**.
- **`_hefesto_fake_env`** (autouse) — força o modo falso e isola
  `XDG_CONFIG_HOME`/`DATA`/`CACHE`/`STATE` num diretório temporário. **Não isola
  `XDG_RUNTIME_DIR` de propósito**, e aponta o socket do broker para um caminho
  inexistente, para não tocar o broker real da máquina.
- **`src/.../testing/`** não é diretório de teste: é **pacote de produção**. O
  `FakeController` implementa `IController` sem hardware e é usado tanto pelos
  testes quanto pelo runtime real (`HEFESTO_DUALSENSE4UNIX_FAKE=1`), com replay
  de capturas HID. Usado por 77 arquivos de teste.

## As quatro lacunas, com número

1. **734 testes (14,9%) dependem de PyGObject e PULAM no CI.** Está escrito no
   próprio workflow, com a frase *"não finja que está coberto"*. É exatamente a
   camada onde a leva de 26/07 quebrou.
2. **479 asserts travam o TEXTO do código-fonte**, em 58 arquivos:
   - **346** grepam shell — defensável, `tests/shell/` está vazio e não há bats;
   - **~71 congelam Python de produção** (34 via `inspect.getsource`, 37 lendo
     `.py` como texto) — estes são a muralha real;
   - **25 asserts de `.count()`** que **proíbem deduplicar código**.

   Exemplo do que isso trava: `assert "led_set((0, 0, 0), uniq=self._edit_uniq())"
   in fonte` — renomear o método ou usar uma constante quebra o teste sem mudar
   comportamento.
3. **Viés de transporte:** apenas **9 ocorrências** de `transport="bt"` em 4
   arquivos, contra dezenas de `"usb"`. **Bugs de rádio são invisíveis por
   construção** — e o rádio é onde moram os defeitos mais caros deste projeto.
4. **11 módulos de `src/` sem citação em teste nenhum** — entre eles **6 dos 13
   módulos da CLI** e `utils/i18n.py` inteiro.

## O que a suíte protege bem

Não é só dívida: daemon e subsistemas, identidade e numeração, perfis e matching,
co-op, IPC por controle, backends de janela, broker, uhid/uinput, Bluetooth,
DKMS, e os três scripts grandes (`install.sh`, `uninstall.sh`, `doctor.sh`) têm
cobertura densa.

E a casa tem uma regra que vale mais que a contagem: **o teste tem de morder.**
Cada cura é arrancada, a suíte roda, a falha é observada e a cura é restaurada.
Nas últimas levas isso está registrado commit a commit — 12, 14, 21 mutações
aplicadas ao código real, todas reprovando.
