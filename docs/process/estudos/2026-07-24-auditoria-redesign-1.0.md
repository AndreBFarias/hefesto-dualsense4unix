# 2026-07-24 — Auditoria: redesign de identidade e layout para o 1.0.0

Auditoria do repositório e da GUI antes de aplicar o pacote de identidade visual
entregue em `novo-layout/`. Levanta o que muda, onde muda, o que **não** dá para
fazer do jeito ingênuo, e o que exige backend novo.

**Escopo do que foi pedido:** logo nova, título colorido, subtítulo novo, paleta
formalizada, sensores na aba Status, aba Gatilhos compacta, aba Perfis sem o JSON,
Mouse+Teclado unificadas, faxina da raiz, README enxuto e prints novos.

**Fonte da verdade do design:** `novo-layout/GUIA_IMPLEMENTACAO.md` (valores exatos),
`novo-layout/screenshots/*.png` (mockups renderizados),
`novo-layout/assets/hefesto-logo.svg` (logo final).

---

## Incidente que abriu a sessão (resolvido)

O pacote de design foi extraído **na raiz do repositório**. Ao limpar, a seleção
levou junto arquivos ocultos e do projeto: às 19:39:36 foram para a Lixeira o
`.git` inteiro (26 MB) e o `assets/` do projeto (as regras udev, as units systemd,
o DKMS e os glyphs de que o `install.sh` depende).

Ambos foram restaurados de `~/.local/share/Trash/files/` e validados: `git fsck`
sem corrupção (só *dangling objects* antigos do `filter-repo` de 20/07), HEAD em
`sprint/harmonia-uhid` no commit `c3a327b`, remotes `origin` e `upstream`
preservados, working tree limpa.

**Aprendizado operacional:** pacotes externos entram em subpasta própria
(`novo-layout/`), nunca na raiz. E o trabalho local passou a ser pushado — antes
deste incidente havia branches que existiam **só** nesta máquina.

---

## Os dez achados

### A-1 — A GUI é Glade, não código

`src/hefesto_dualsense4unix/gui/main.glade` tem 2516 linhas e define as 10 abas
(Início, Status, Gatilhos, Lightbar, Rumble, Perfis, Sistema, Emulação, Mouse,
Teclado). O Python em `app/actions/*.py` popula e reage.

**Consequência:** toda mudança de layout é XML + Python. Não existe atalho por CSS.

### A-2 — A paleta Drácula já está aplicada; o que falta é papel semântico

`gui/theme.css` (497 linhas) já usa as cores certas — `#bd93f9` 18×, `#f8f8f2` 17×,
`#282a36` 17×, `#44475a` 11×, `#6272a4` 10×.

O que falta são os **tokens de superfície** do guia (§1.2), hoje inexistentes:
`#21222c` (app bg), `#2b2d3a` (elevated), `#343746` (borda sutil), `#c8ccda` (texto
suave), `#8b8fa8` (texto mudo).

E o que sobra são as cores **fora da paleta** que já entraram: `#383a4a` (9×),
`#fff` (6×), `#000` (5×), `#ff0` (4×), `#2a2a2a` (2×), `#caa3fb` (2×), `#2f313d`.

**Consequência:** o trabalho é de disciplina, não de repintura. Cada cor recebe UM
papel (§1.3 do guia) e as sete intrusas saem.

### A-3 — ARMADILHA: Mouse e Teclado foram separadas de propósito

O comentário em `main.glade:2348` é explícito:

> Aba Teclado (FEAT-KEYBOARD-UI-01) separada de Mouse para enxugar min-size do
> notebook — antes ambas viviam numa única aba "Mouse e Teclado" e a soma de
> mapeamento + treeview inflava a altura natural de **todas as outras abas**.

O `GtkNotebook` pede como altura mínima o **maior** mínimo entre todas as páginas.
Uma aba gorda engorda o piso de todo mundo.

**Consequência:** unificar em "Navegação DSX" só é seguro em **duas colunas lado a
lado** — que é exatamente o que o mockup desenha. Empilhado, recria a regressão
que o projeto já pagou para consertar. O aceite da sprint tem que medir a altura
natural das abas **não tocadas**.

### A-4 — Toda aba já vive dentro de um ScrolledWindow

`_wrap_notebook_pages_in_scroll` (`app/app.py:800`) embrulha cada página para o
rodapé de ações nunca ser cortado sob o tiling do COSMIC — que ignora
`height-request` da janela.

**Consequência:** "sem barra de rolagem" **não** significa remover o scroller.
Significa fazer a altura natural caber nos 680px da janela (`main.glade:72`) para
que a barra nunca precise aparecer. O scroller continua como rede de segurança
para janelas menores.

### A-5 — Os índices de aba estão hardcoded

O `refresh_map` (`app/app.py:770-793`) casa página por **número**: `8` = Mouse,
`9` = Teclado. Unificar as duas desloca os índices em silêncio, e o refresh de aba
passa a rodar na página errada sem erro visível.

O próprio arquivo já registra essa lição em EST-10 (`app.py:818`), sobre o skip do
`_wrap_notebook_pages_in_scroll`:

> identificar a aba pelo WIDGET, não pelo texto visível […] o id do Glade não muda
> quando o rótulo muda.

**Consequência:** a fusão obriga a migrar o `refresh_map` de índice para lookup por
widget. É a mesma cura, aplicada ao lugar que ficou de fora.

### A-6 — Os três sensores da aba Status não existem no backend

`_inputs_from_state` e `_inputs_from_snapshot` (`daemon/ipc_handlers.py:1415-1445`)
entregam apenas `lx/ly/rx/ry/l2_raw/r2_raw/buttons`. Não há giroscópio, touchpad
nem microfone no estado que a GUI consome.

Cada sensor tem um caminho diferente:

| Sensor | Situação hoje | Caminho escolhido |
|---|---|---|
| **Giroscópio** | `extract_motion_window` (`core/physical_report_reader.py:127`) fatia gyro/accel dos bytes 15-26 do report cru, mas só **repassa opaco** ao vpad — e só roda quando há vpad ativo | Ler o nó evdev `…Motion Sensors`, que o projeto já conhece (`assets/78-dualsense-motion-not-joystick.rules` o nomeia exatamente). Dá graus/s decodificado e **funciona em todos os modos** |
| **Touchpad** | `DualSenseTouchpadReader` (`core/evdev_reader.py:944`) já lê `BTN_TOUCH` + `ABS_X` (0-1919) / `ABS_Y` (0-1079) | Expor posição e estado de toque a partir do reader existente, **sem** tocar em `consume_motion()` — ele drena o delta acumulado para o cursor e um segundo consumidor roubaria o movimento |
| **Microfone** | O botão já chega por HID-raw (`micBtn`, byte misc2 bit 0x04 — `evdev_reader.py:658`) e o glyph `mic` já existe (`gui/widgets/button_glyph.py:56`) | Selo ATIVO/MUDO sai de graça do que já existe. O **medidor de nível** é o único item genuinamente novo: captura PipeWire/ALSA do device de áudio do controle |

**Consequência:** a sprint dos sensores é a única que mexe em daemon, IPC e GUI ao
mesmo tempo. Os campos novos entram como **opcionais** no payload, para um daemon
antigo com GUI nova não quebrar.

Requisitos do medidor de nível, para não repetir erros conhecidos do projeto:
thread própria, **desligada quando a aba Status não está visível** (o `switch-page`
já dá o gancho), e degradação silenciosa se o device não existir — na linha do que
`app/theme.py` já faz com o CSS ausente. Um busy-loop aqui repetiria o incidente de
104% de CPU da v3.8.1.

### A-7 — O nome do produto vive em seis lugares

Trocar o subtítulo para "Gerenciador DualSense para Linux" exige tocar em:

- `gui/main.glade:70` — título da janela
- `gui/main.glade:106` — título grande (vira markup colorido por trecho)
- `gui/main.glade:114` — o subtítulo em si
- `cli/app.py:21` — help do CLI
- `__init__.py:1` — docstring do pacote
- `tui/app.py:123` — cabeçalho da TUI
- `packaging/hefesto-dualsense4unix.desktop:3` e
  `assets/appimage/Hefesto-Dualsense4Unix.desktop:5` — `Comment=`

### A-8 — Três famílias de ícone, uma delas monocromática

- `assets/appimage/Hefesto-Dualsense4Unix.png` — o que o README exibe e o AppImage usa
- `packaging/cosmic-applet/data/icons/hicolor/scalable/apps/…-symbolic.svg`
- `packaging/cosmic-applet/data/icons/hicolor/256x256/apps/….png`

**Consequência:** o `-symbolic.svg` não é redimensionamento do colorido. Ícone
symbolic no COSMIC é monocromático e recolorido pelo tema — precisa de uma silhueta
própria (a bigorna, sem gradiente), senão vira um borrão na barra.

### A-9 — README: 705 linhas, 5384 palavras, zero screenshots

Só badges. E a badge de release aponta para o repositório errado —
`AndreBFarias/hefesto`, sem o `-dualsense4unix`.

O bloco "Versão:" é um parágrafo único gigante que mistura release notes de várias
versões. Há 25 seções de nível `###` sem hierarquia intermediária.

### A-10 — Os prints e os gates exigem hardware

Nenhum DualSense conectado no momento da auditoria (`/dev/input/by-id` sem entrada
Sony, `arecord -l` sem o device de áudio do controle). Os prints da S8 e os gates
G1–G4 dependem de controle ligado.

---

## Versionamento: o que a auditoria encontrou

O lançamento pedido é **1.0.0 como marco zero**, com renumeração das tags antigas.
Três fatos levantados que a decisão precisa carregar:

1. **O upstream tem 8 releases públicas** (v0.1.0 → v3.0.0, abril/2026), publicadas
   pelo dono original, com **62 downloads** acumulados. Renumerar apaga o histórico
   público dele.
2. **A permissão atual no upstream é `pull`** (`admin: false`). A renumeração só é
   executável depois que o acesso de admin chegar.
3. **A tag `v1.0.0` já existiu** — 21/04/2026, "primeira release estável". A linha
   foi `v0.1.0 → v1.0.0 → v1.1.0 → v1.2.0 → v2.0.0 → … → v4.0.0`. O 1.0.0 do
   lançamento é uma **reutilização** do número, não estreia.

Efeito colateral aceito: o upstream já publicou 3.0.0, então um 1.0.0 posterior é
*menor* em semver — quem instalou o `.deb` v3.0.0 não recebe o 1.0.0 como
atualização por apt/pip.

**Decisão da mantenedora:** manter a renumeração completa. Salvaguarda executada
antes de qualquer deleção: `docs/tags-arquivo-pre-1.0.txt` registra as 46 tags
(38 do fork + 8 do upstream) com `tag → SHA → data`, e é o único mapa para
recriar qualquer uma. A execução fica condicionada ao admin em mãos e ao dono
original ciente.

---

## Faxina: o inventário

**Raiz** — 18 arquivos rastreados. Saem: `CHECKLIST_MANUAL.md`,
`CHECKLIST_VALIDACAO_v3.md`, `CHECKLIST_VALIDACAO_v3.2.0.md`,
`CHECKLIST_VALIDACAO_v3.4.0.md` e `HEFESTO_PROJECT.md` — este último é só um
apontador para docs que também saem. A avaliar: `benchmarks/` (1 CSV de polling) e
`captures/` (4 binários de descriptor USB), candidatos a `docs/protocol/`.

**`docs/`** — 9,2 MB, dos quais **7,5 MB são `docs/process/`**: 235 arquivos de
sprint, 33 estudos, 20 discoveries, 15 docs de processo, 2 sessions, 1 audit.
Sai inteiro da main, preservado na tag `arquivo/processo-pre-1.0`.

**Ficam na main:** `docs/usage` (11 guias, a revisar), `docs/adr` (19),
`docs/protocol` (3), `docs/research` (3), `docs/history` (6).

**`CHANGELOG.md`** — 2598 linhas / 172 KB.

**Regra de segurança:** antes de remover qualquer caminho, confirmar que não é
referenciado por `install.sh`, `run.sh`, os 4 workflows do CI ou o README.

---

## Restrição que atravessa todas as sprints

`scripts/check_anonymity.sh` roda no CI (`ci.yml:17`) e no release
ferramenta de IA — no código, nas mensagens de commit e nos docs.
