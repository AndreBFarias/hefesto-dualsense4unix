# Sprint: redesign de identidade, layout e lançamento oficial 1.0.0

**Status**: plano FECHADO (24/07 noite). 10 frentes (S1–S10) + 4 gates humanos.
Execução em andamento; ver "Progresso".
**Origem**: pedido da mantenedora — *"o dono original vai me dar admin do repo
original e me deixou tocar em definitivo. Vamos dar rebase nos releases e lançar
oficialmente a 1.0.0. Antes preciso da sua ajuda com a mudança de layout"*.

**Auditoria que fundamenta**: `docs/process/estudos/2026-07-24-auditoria-redesign-1.0.md`
(10 achados A-1..A-10).
**Design de referência**: `novo-layout/GUIA_IMPLEMENTACAO.md` — valores exatos,
mockups em `novo-layout/screenshots/`, logo em `novo-layout/assets/hefesto-logo.svg`.

## Decisões da mantenedora (não reabrir)

| Tema | Decisão |
|---|---|
| Faxina | Raiz + `docs/process/` arquivado + enxugar `docs/usage` e CHANGELOG |
| Microfone | Selo ATIVO/MUDO **+ medidor de nível real** (captura PipeWire/ALSA) |
| Versão | Apagar as tags/releases antigas (upstream **e** fork) e lançar 1.0.0 como marco zero |
| Escopo | Redesign + 3 débitos técnicos + os gates G1–G4 **antes** de publicar |

## Progresso

| Frente | Estado | Nota |
|---|---|---|
| **Passo 0** salvaguardas | OK FEITO | Branches e tags pushadas; `docs/tags-arquivo-pre-1.0.txt` com as 46 tags; tag `arquivo/processo-pre-1.0` criada |
| **Fase 1** auditoria | OK FEITO | `6b7a3b7` |
| **Fase 2** esta sprint | OK FEITO | este doc |
| **S1** identidade | a fazer | |
| **S3** gatilhos compactos | a fazer | |
| **S4** perfis sem JSON | a fazer | |
| **S5** navegação DSX | a fazer | |
| **S2** sensores no Status | a fazer | a mais pesada — daemon + IPC + GUI |
| **S6** débitos técnicos | a fazer | |
| **S9** applet | a fazer | |
| **S7** faxina | a fazer | |
| **S8** README + prints | a fazer | exige hardware |
| **G1–G4** gates humanos | a fazer | exigem a mantenedora jogando |
| **S10** release 1.0.0 | BLOQUEADO | depende do admin no upstream |

**Ordem**: S1 → S3·S4·S5 (layout) → S2 (sensores) → S6 → S9 → S7 (faxina) →
S8 (prints do app final) → G1–G4 → S10.

A faxina vem antes do README para ele já descrever a estrutura definitiva; os
prints vêm depois de toda a GUI estar pronta.

---

## S1 — Identidade

**Objetivo**: logo nova, título colorido por trecho, subtítulo novo, paleta com
papéis semânticos.

**Arquivos**: `assets/hefesto-logo.svg`, `assets/appimage/*`,
`gui/main.glade` (70, 106, 114), `gui/theme.css`, e os 5 pontos do A-7.

1. `assets/hefesto-logo.svg` vira a logo canônica (já está no disco). Derivar
   PNG 256 e 512 para o AppImage e o `.desktop`.
2. **Título por trecho** em `main.glade:106`, markup Pango:
   `Hefesto` `#ff79c6` · `—` `#6272a4` · `DualSense` `#f8f8f2` · `4` `#50fa7b` ·
   `Unix` `#f8f8f2`.
3. **Subtítulo**: `daemon de gatilhos adaptativos para DualSense` →
   `Gerenciador DualSense para Linux`, cor `#6272a4`. Propagar nos 6 lugares do A-7.
4. **`theme.css`**: adicionar os tokens de superfície ausentes (`#21222c`,
   `#2b2d3a`, `#343746`, `#c8ccda`, `#8b8fa8`); aplicar os papéis do guia §1.3 e
   §3; remover as sete cores fora da paleta (A-2).
   - Aba ativa: texto `#f8f8f2` + borda inferior 2px `#ff79c6`.
   - Selecionado: borda `#bd93f9` + fundo `rgba(189,147,249,0.16)` — **nunca**
     roxo chapado em área grande.
   - Rosa é exclusivo de marca e aba ativa; não compete com o roxo.

**Aceite**: janela abre com o título tricolor, subtítulo novo e nenhuma cor fora
das 11 da paleta + 7 tokens de superfície.
**Reverter**: `git revert` do commit — mudança isolada em CSS + glade + strings.

## S2 — Sensores na aba Status *(a mais pesada)*

**Objetivo**: giroscópio, microfone e touchpad por controle na aba Status.

**Arquivos**: `core/evdev_reader.py`, novo leitor de motion,
`daemon/ipc_handlers.py` (1415-1445), `app/widgets/controller_card.py`,
`app/actions/status_actions.py`.

1. **Giroscópio** — thread leitora do nó evdev `…Motion Sensors` (o mesmo que
   `assets/78-dualsense-motion-not-joystick.rules` nomeia), espelhando o padrão de
   `EvdevReader`. Publica X/Y/Z em graus/s. Render: três barras bidirecionais com
   origem no centro, `X=#ff5555 · Y=#50fa7b · Z=#8be9fd`.
   - Convive com a linha `texto_motion` (`controller_card.py:205`): aquela diz se o
     gyro **flui para o jogo**, esta mostra o **valor**. Não substituir.
2. **Microfone** — selo `ATIVO` (fundo `#50fa7b`, texto `#21222c`) / `MUDO`
   (fundo `#2b2d3a`, texto `#6272a4`) a partir do `micBtn` já lido por HID-raw,
   mais medidor de nível por captura PipeWire/ALSA.
   - **Obrigatório**: thread própria, desligada quando a aba Status não está
     visível (gancho no `switch-page`), e degradação silenciosa se o device não
     existir. Um busy-loop aqui repete o incidente de 104% de CPU da v3.8.1.
3. **Touchpad** — retângulo com contorno `#44475a`, ponto(s) de toque em `#8be9fd`,
   rótulo "N toque" / "sem toque". Lê o estado do `DualSenseTouchpadReader`
   **sem** tocar em `consume_motion()` — ele drena o delta para o cursor e um
   segundo consumidor roubaria o movimento.
4. **IPC** — campos novos **opcionais** em `_inputs_from_state` e
   `_inputs_from_snapshot`, para daemon antigo + GUI nova não quebrar.

**Layout do card** (mockup): Estado → Bateria/L2/R2 → Analógicos → botões →
Giroscópio → Microfone + Touchpad. Dois controles lado a lado, sem rolagem.

**Aceite**: girar o controle move os três eixos; falar no mic sobe o medidor;
encostar no touchpad acende o ponto; CPU da GUI estável.
**Reverter**: os campos são opcionais e o render é aditivo — revert do commit
volta ao card anterior sem tocar no daemon.

## S3 — Gatilhos compactos

**Objetivo**: altura de cada botão de modo a ~1/3, tudo visível sem rolagem.

**Arquivos**: `app/widgets/segmented_selector.py`,
`app/actions/triggers_actions.py`, `gui/theme.css`.

1. Botões de modo a ~28–32px de altura, fonte 11px, grid de 3 colunas.
2. `_build_param_row` (`triggers_actions.py:449`): rótulo com `nowrap` e largura
   fixa ~150px — hoje são 200px e "Intensidade início (1-8)" quebra em duas linhas.
3. Rodapé do card: "Aplicar em L2/R2" (contorno `#50fa7b`) e "Desligar"
   (contorno `#6272a4`).

**Aceite**: grid + descrição do modo + 4 sliders + ações cabem nos 680px sem
ativar a barra de rolagem.

## S4 — Aba Perfis sem "Detalhes técnicos"

**Objetivo**: remover o bloco JSON; manter todo o resto.

**Arquivos**: `gui/main.glade` (1507, 1634, 1719),
`app/actions/profiles_actions.py`.

1. Remover o bloco "Detalhes técnicos" e o handler que o preenche.
2. Cabeçalho de tabela: fundo `#2b2d3a`, texto de coluna `#bd93f9`. Linha
   selecionada: fundo `rgba(189,147,249,0.16)`.
3. Ações do rodapé: Novo/Duplicar/Recarregar (`#6272a4`), Remover (`#ff5555`),
   Ativar (`#50fa7b`), Salvar (`#bd93f9`).

**Aceite**: a aba perde o JSON e não perde nenhuma função. Tabela e editor intactos.

## S5 — Navegação DSX (unificar Mouse + Teclado)

**Objetivo**: uma aba só, duas colunas, sem rolagem.

**Arquivos**: `gui/main.glade` (2342, 2420 e os containers das duas abas),
`app/app.py` (770-793), `app/actions/mouse_actions.py`, `app/actions/input_actions.py`.

1. Fundir `tab_mouse` + `tab_keyboard` numa aba `Navegação DSX` com **duas
   colunas lado a lado** — Mouse à esquerda, Teclado à direita.
   - **A-3 é a armadilha desta sprint.** As abas foram separadas de propósito
     porque, empilhadas, inflavam a altura mínima de **todas** as outras. Só a
     disposição horizontal resolve.
2. Migrar o `refresh_map` de índice numérico para lookup **por widget** (A-5),
   unindo `_refresh_mouse_tab` e `_refresh_key_bindings_from_draft`.

**Aceite**: medir a altura natural das abas **não tocadas** antes e depois — se
subir, a fusão foi feita errado. Nenhuma aba ativa a barra de rolagem.
**Reverter**: revert do commit devolve as duas abas.

## S6 — Débitos técnicos

Do `docs/process/2026-07-24-RETOMADA-por-onde-comecar.md` §Débitos:

1. Comparação **case-insensitive** em `MatchCriteria.matches` (`profiles/schema.py`)
   — o R-12 removeu o `.lower()` que corrompia o dado, mas a cura completa ficou
   pendente. É uma linha.
2. Check de "perfis inalcançáveis" no `doctor.sh` — a GUI já mostra
   "Só manual (nunca ativa sozinho)"; falta o diagnóstico de linha de comando.
3. Sentinel `{"type":"manual"}` no schema para perfis manuais-only, em vez de
   criteria vazio (hoje resolvido por regex real no `coop_local`).

## S7 — Faxina

**Raiz** — remover `CHECKLIST_MANUAL.md`, `CHECKLIST_VALIDACAO_v3.md`,
`CHECKLIST_VALIDACAO_v3.2.0.md`, `CHECKLIST_VALIDACAO_v3.4.0.md`,
`HEFESTO_PROJECT.md`. Avaliar `benchmarks/` (1 CSV) e `captures/` (4 binários de
descriptor) — movem para `docs/protocol/` ou saem.

**`docs/process/`** — sai inteiro da main (7,5 MB: 235 sprints, 33 estudos, 20
discoveries), preservado na tag `arquivo/processo-pre-1.0`. **Esta sprint e a
auditoria saem junto** — o processo fica no arquivo, a main fica pública.

**`docs/usage`** — revisar os 11 guias, remover o que caducou.
**CHANGELOG** — 2598 linhas: manter as versões recentes, apontar as antigas para
a tag de arquivo.

**Regra de segurança**: antes de remover qualquer caminho, confirmar que não é
referenciado por `install.sh`, `run.sh`, os 4 workflows ou o README.

**Recuperar**: `git checkout arquivo/processo-pre-1.0 -- docs/process`.

## S8 — README + prints

1. **Prints** — abrir a GUI redesenhada com controle conectado e capturar cada
   aba. Destino `docs/usage/assets/`.
2. **README** — de 705 linhas para ~200: o que é, o que instala, como usa, onde
   achar o resto. O detalhe técnico migra para `docs/usage/`.
3. Corrigir a badge de release (aponta para `AndreBFarias/hefesto`, sem o
   `-dualsense4unix`) e substituir o bloco "Versão:", hoje um parágrafo único que
   mistura release notes de várias versões.

## S9 — Applet COSMIC

1. Regenerar `…-symbolic.svg` — **monocromático de verdade**, silhueta da bigorna
   sem gradiente. Ícone symbolic é recolorido pelo tema; o colorido reduzido vira
   borrão na barra (A-8).
2. Regenerar o `256x256/apps/….png` a partir do SVG novo.
3. Conferir se as cores em `packaging/cosmic-applet/src/app.rs` seguem os mesmos
   tokens da GUI.

## S10 — Release 1.0.0 *(bloqueado até o admin chegar)*

1. Rebase/merge de `sprint/harmonia-uhid` na `main`.
2. Versão `4.0.0 → 1.0.0` em `pyproject.toml:7` e `__init__.py:13`.
3. Renumeração: apagar as 8 tags/releases do upstream e as do fork — com
   `docs/tags-arquivo-pre-1.0.txt` em mãos e **o dono original ciente**.
4. Publicar via `workflow_dispatch` (push de tag não dispara o release).

**Três fatos que a execução carrega** (do §Versionamento da auditoria): o upstream
tem 8 releases públicas do dono com 62 downloads; a permissão atual lá é só de
leitura; e a tag `v1.0.0` já existiu em 21/04/2026 — o número é reutilizado.

## Gates humanos G1–G4

Herdados do doc de retomada. Exigem a mantenedora jogando:

- **G1** — co-op real com os 4 controles (numeração 1-2-3-4, Sackboy do 1º frame,
  Mullet Mad Jack sem desligar nada, ajuste por-controle, cadeado do autoswitch).
- **G2** — R-03: lock manual × modo do perfil, com daemon reiniciado.
- **G3** — Bluetooth sob carga com o no-sniff por-conexão.
- **G4** — vigia 3 do watchdog (SDP), caminho (a) nunca reproduzido.

**Regra**: A/B de BT sempre com `hefesto-bt-health-watchdog.timer` **parado** — a
vigia 0 reaplica o modo ativo a cada 2 min e contamina a medição. Religar depois.

---

## Verificação (vale para todas as frentes)

- `pytest` (4724 testes hoje), `ruff check`, `mypy` — os três limpos a cada frente.
- **O critério que se repete em S3/S4/S5**: janela nos 680px padrão e **nenhuma**
  aba ativando a barra de rolagem — incluindo as não tocadas (é como a regressão
  do A-3 apareceu da última vez).
- Validação visual por aba contra o mockup de `novo-layout/screenshots/`.
- `bash scripts/check_anonymity.sh` antes de cada commit.
