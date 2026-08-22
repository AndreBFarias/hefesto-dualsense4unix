# COMO EXECUTAR — a leva da aba Configurações

Documento único para quem vai implementar as nove sprints sem ter acompanhado o planejamento.
Escrito a partir dos nove relatórios de reconciliação de 21/08/2026, todos com veredito
`precisa_ajuste`. Onde dois relatórios se contradizem, isto está dito com todas as letras e os
dois estão citados — não escolha por conta própria.

---

## 1. O QUE É ESTA LEVA

Uma aba nova, a décima primeira, chamada **Configurações**, no fim da tira do `main_notebook`.

A tese: **o que o produto não mede, a pessoa declara.** A janela hoje só sabe mostrar o que
consegue ler do aparelho; tudo que depende do mundo físico — onde está o dongle, se há um hub,
qual é a cor do plástico, em que modo o controle foi ligado — some. A aba dá lugar a essas
declarações, com duas salvaguardas: todo campo nasce em "não sei", e onde a medição existe é a
medição que preenche.

Cinco seções, na ordem do mockup: **Está tudo certo?**, **Os controles**, **A mesa**,
**Orçamento**, **A janela**.

Mockup aprovado: [mockup/aba-configuracoes.html](mockup/aba-configuracoes.html) — e leia o
[mockup/README.md](mockup/README.md), que avisa que os endereços, os `831 / 1600` e os VID:PID
são ilustração, nenhum lido de máquina.

---

## 2. ANTES DE COMEÇAR

### 2.1 Onde o trabalho nasce

O trabalho nasce na `dev`. O commit de referência dos nove relatórios é `70d28762`
("ci(fluxo): o trabalho passa a nascer na `dev`, e os portões vão junto", FLUXO-DEV-01,
21/08 20:03). Antes de qualquer coisa:

```sh
cd /home/andrefarias/Desenvolvimento/hefesto-dualsense4unix
git rev-parse --abbrev-ref HEAD    # tem de dizer: dev
git rev-parse --short HEAD         # 70d28762 ou um descendente
git switch -c sprint/config-01     # o CI cobre main, dev, restauro/**, sprint/**, onda/**
```

Se disser `main`, pare. As duas histórias divergiram: rebase contra a `main` local reverte curas.

> **Contradição registrada.** CONFIG-01 mediu "a `main` está 531 commits à frente por outro
> caminho"; CONFIG-07 mediu "584 à frente / 531 atrás"; o contexto desta leva fala em "584
> commits novos". Os três números descrevem a mesma divergência de história por ângulos
> diferentes. Nenhum deles autoriza rebase.

### 2.2 O comando que levanta o ambiente

```sh
export GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache
```

Exporte isso **na sessão inteira**, não só antes da captura — ver 2.3.

Interpretador: use `.venv/bin/python` para tudo que importa o produto ou o `gi`. O `python3`
desta máquina é o pyenv 3.12.1, sem `gi`, sem `shellingham` e sem o produto instalado — com ele
`pytest tests/unit` aborta com 14 erros de coleta (CONFIG-02, CONFIG-06).

> **Contradição registrada.** CONFIG-08 mediu o oposto para UM script: o `.venv` é Python 3.10,
> sem `tomllib`, e por isso `scripts/check_version_consistency.py` morre com
> `ModuleNotFoundError: No module named 'tomllib'` no venv e passa com o `python3` do sistema
> (3.12). CONFIG-08 também registra que numa chamada o `python3` resolveu para 3.12.1 e noutra
> caiu no venv. Regra prática: produto e `gi` -> `.venv/bin/python`; validadores de shell e de
> TOML -> `python3` do sistema; e fixe o caminho absoluto do interpretador
> (`/home/andrefarias/.pyenv/versions/3.12.1/bin/python3`) antes de acreditar em qualquer
> reprovação.

Geometria roda **sempre** sob Xvfb:

```sh
xvfb-run -a --server-args="-screen 0 1920x1080x24" \
  .venv/bin/python -m pytest tests/unit/test_layout_orcamento_altura.py -q
```

> **Contradição registrada** sobre o que acontece sem Xvfb. CONFIG-01 mediu `3 failed, 4 passed`
> ("o conteúdo pede 1203px de largura e a janela abre com 1180px"), causado pela fixture
> `_tema_na_escala_que_sai` (`tests/unit/test_layout_orcamento_altura.py:150-181`) somar o delta
> 3 ao `gtk-font-name` da sessão (`Fira Mono 12` aqui contra `Sans 10` num Xvfb limpo).
> CONFIG-02 e CONFIG-05 mediram **core dump** contra `DISPLAY=:1` — o interpretador cai, não
> reprova. As duas medições levam à mesma cura: `xvfb-run -a` em todo pytest de geometria.

As fontes **Space Grotesk** e **JetBrains Mono** precisam estar instaladas, ou a régua mente —
é o que o job `gtk-real` faz (`.github/workflows/ci.yml:551-568`). Confira com
`fc-list | grep -ci space.grotesk`.

### 2.3 A armadilha do snap, e a cura

Reproduzida em 21/08 neste terminal, e não atinge só o `retratar_abas.py`: atinge **qualquer
processo GTK lançado daqui**.

```
Gtk:ERROR:../../../../gtk/gtkiconhelper.c:494: Failed to load
/usr/share/icons/Dracula-Icones/scalable/apps/image-missing.svg:
Unable to load image-loading module:
/snap/ghostty/820/.../libpixbufloader-svg.so: /lib/x86_64-linux-gnu/libm.so.6:
version 'GLIBC_2.38' not found
```

Causa: `$GDK_PIXBUF_MODULE_FILE` do ambiente vale
`/home/andrefarias/snap/ghostty/common/.cache/gdk-pixbuf-loaders.cache`, o cache do
confinamento. Cura: a variável de 2.2, apontando para
`/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache` (existe, 3362 bytes).

O **produto** já se defende: `src/hefesto_dualsense4unix/app/main.py`,
`_sanear_loaders_do_gdk_pixbuf` (linhas 48-95 por CONFIG-07, 48-102 por CONFIG-08 — divergência
de fecho de faixa, não de endereço). O **script de captura** não:
`grep GDK_PIXBUF scripts/gui-captura/retratar_abas.py` devolve vazio. Portar a função para o
topo do `retratar_abas.py`, antes de qualquer `import gi`, é escopo opcional de CONFIG-01 ou de
CONFIG-08 — são as duas únicas que abrem esse arquivo.

### 2.4 Os portões

**CI** (`.github/workflows/ci.yml`), os que mordem esta leva:

| Job | O que cobra | Endereço |
|---|---|---|
| `acentuacao` | PT-BR completo em `.py`, `.sh`, `.md`, `.yml`, `.toml`; o `.glade` é isento (`scripts/validar-acentuacao.py:434` vs `:439-441`) | `ci.yml:46` |
| `glifos` | emoji fora do texto; o sinal de conferido U+2713 e o triângulo de aviso U+26A0 passam, o U+2705 (WHITE HEAVY CHECK MARK) reprova | `ci.yml:71` |
| `palavra-de-tela` | **só o `main.glade`** (`scripts/validar-palavra-de-tela.py:14-18`, `:61`): maiúscula inicial (`:67-83`), `JARGAO_BANIDO` (`:85-94`), exceção que envelheceu (`:232-245`) | `ci.yml:88` |
| `referencias-docs` | arquivo citado entre crases que não existe, em `docs/**` mais o `README.md`; e `gerar-contrato-ipc.py --check` | `ci.yml:111` e `:154` |
| `shellcheck` | `-S error` sobre `scripts/*.sh`, `install.sh`, `uninstall.sh` | `ci.yml:233` |
| `promessa-sem-caminho` | símbolo público de `src/` sem chamador em produção; `tests/` NÃO conta | `ci.yml:268-288` |
| `lint-test` | a suíte mais o **censo de coleta**, piso 8100 e ZERO erro de coleta | `ci.yml:327`, `:470-491` |
| `gtk-real` | descobre alvos por `grep -rlE 'exigir_gi_real\|skip_sem_gi_real' tests/unit`; "pulei porque não tenho GTK" é REPROVAÇÃO | `ci.yml:513`, `:551-568` |
| `pre-commit` | os hooks com `--all-files` | `ci.yml:644` |
| `typecheck` | `mypy` strict | `ci.yml:679` |
| `anonymity` | server-side; pega commit que passou por cima do hook | `anonymity-check.yml` |

**pre-commit**: os hooks **não rodam nesta máquina** — o `core.hooksPath` global desvia o git e
o `pre-commit` recusa instalar (`.pre-commit-config.yaml:1-16`). Quem protege é o job do CI.
Rode `pre-commit run --all-files` à mão antes de empurrar.

> **Contradição registrada** sobre quantos hooks existem. CONFIG-03 e CONFIG-08 listam **dez**,
> com id e linha: `acentuacao-strict` (:28), `glifos` (:40), `anonimato` (:46),
> `referencias-docs` (:59), `palavra-de-tela` (:75), `ruff-check` (:81),
> `icones-refletem-o-svg` (:102), `mapa-de-canais-publicado` (:122),
> `contrato-ipc-publicado` (:140), `citacoes-de-linha-abrem` (:149). CONFIG-07 escreve
> "esperado: os 5 hooks passam". Os dez estão medidos com endereço; os cinco, não.

**E, pela memória desta máquina: os hooks globais REESCREVEM o conteúdo dos arquivos staged no
commit** (trocam palavras, redigem identidade). Confira o `git show` DEPOIS de commitar, não só
o diff antes. Nunca `--no-verify`.

### 2.5 Três regras de redação que reprovam CI

1. **Nunca escreva a palavra "sprint" colada a um ID `CONFIG-0X` em nenhum `.md` sob `docs/`.**
   O portão `tests/unit/test_nome_citado_como_sprint_existe.py` descobre sprints com
   `glob("*.md")` NÃO-recursivo em `docs/process/sprints`, exigindo prefixo de data no nome do
   arquivo (`:67-79`); esta leva mora em subpasta e sem data, então **nenhum `CONFIG-0X` é
   conhecido** (sonda de CONFIG-08: `CONFIG-01 DESCONHECIDO`, `CONFIG-08 DESCONHECIDO`). O regex
   `_CITADO_COMO_DOC` (`:38-41`) casa a forma `a sprint NOME-NN`. Use link markdown ou o ID
   sozinho. `CHANGELOG.md` e `README.md` escapam — o teste só varre `docs/`.
2. **Arquivo que ainda não existe não se cita entre crases.** `validar-referencias-docs.py`
   acusou `CONFIG-01-a-aba-existe-e-esta-vazia.md:22` por citar
   `src/hefesto_dualsense4unix/app/actions/config_actions.py`. A cura foi escrever <!-- ref-externa: arquivo que esta leva cria -->
   "**A CRIAR** — src/..." (sem crases). A alternativa é marcar a linha com
   `<!-- ref-externa -->` (`validar-referencias-docs.py:87`, `:170`).
3. **`validar-citacoes-de-linha.py` NÃO cobre `docs/process/`** — o alcance declarado é só
   `docs/protocol/` (`:63-66`, e `PASTA = Path("docs") / "protocol"` em `:82`). Os endereços
   envelhecidos desta leva **não derrubam CI nenhum**. Corrigi-los é para a próxima pessoa não
   se perder. O que morde é a REGRA 1 do `validar-referencias-docs.py` (o arquivo existe), que
   alcança `docs/process/`.

---

## 3. A ORDEM

| ID | O que entrega | Bloqueada por | Tamanho estimado |
|---|---|---|---|
| **CONFIG-01** — **O PORTÃO** | A 11ª aba existe, vazia, com as cinco seções só como títulos; o mixin, a fiação em `app.py` (dois sítios) e a fita de alvo esmaecida | nada | Pequena-média: ~330 a 420 linhas, 6 arquivos de código/script mais 12 binários de documentação |
| CONFIG-02 | Leitura de sysfs: adaptadores, rádios do barramento, hub, painel, vizinhança apertada | CONFIG-01 | 850 a 1000 linhas, 6 arquivos |
| CONFIG-03 | A camada de persistência de mesa (`maquina.json`), método IPC e ponte | CONFIG-01 (e CONFIG-02, pelo passo 0 do relatório) | ~620 linhas, 9 arquivos, 2 novos |
| CONFIG-04 | O medidor de rádio: ocupação por adaptador, barra de duas fatias | CONFIG-01, 02, 03 | ~600 linhas, 8 arquivos |
| CONFIG-05 | Orçamento como teto (vibração e, se ficarem no escopo, giroscópio e microfone) | CONFIG-01, CONFIG-03 | 700 a 950 linhas, 12 a 15 arquivos |
| CONFIG-06 | Cards de controles externos com as declarações | CONFIG-01, CONFIG-03 | 700 a 1100 linhas, 8 a 11 arquivos |
| CONFIG-07 | A seção "A janela": escala do texto, ambiente, bandeja, autostart | CONFIG-01 | 600 a 750 linhas, 7 arquivos |
| CONFIG-08 | A aba entra na documentação: fotos, `interface.md`, `README.md`, `CHANGELOG.md`, notas datadas | **todas** — é a última a commitar | 120 a 170 linhas de prosa mais 10 a 60 de código |
| CONFIG-09 | A seção 0 "Está tudo certo?": o exame e o selo | CONFIG-01, CONFIG-02 | ~950 a 1100 linhas, 8 arquivos |

**O portão é CONFIG-01.** Enquanto
`grep -c '<child type="tab">' src/hefesto_dualsense4unix/gui/main.glade` der 10 e
`find . -name config_actions.py` não achar nada, nenhuma das outras oito tem onde morar.
CONFIG-02 registra isto como parada obrigatória no passo 0.

**O que pode correr em paralelo:**

- Depois de CONFIG-01: **CONFIG-02** e **CONFIG-07** são independentes entre si (a 07 só encosta
  em `app/theme.py`, num módulo novo de ambiente e na seção 5 do glade).
- Depois de CONFIG-03: **CONFIG-05** e **CONFIG-06** são independentes entre si.
- **CONFIG-09** depende de CONFIG-02 (consome a leitura de vizinhança) e corre em paralelo com
  04, 05 e 06.
- **CONFIG-08 é serial e é a última.** Motivo medido:
  `tests/unit/test_as_fotos_acompanham_a_versao.py:94-116` compara TOPOLOGIA de commits — o
  commit que tocou `src/.../app` ou `src/.../gui` tem de ser ancestral do commit que tocou
  `docs/usage/assets`. Todas as outras oito tocam `app/` ou `gui/`.

**Regra que vale para as nove:** todo commit que toca `src/.../app` ou `src/.../gui` tem de
carregar as fotos refeitas no mesmo commit, ou a suíte reprova por procedência. Enquanto os PNGs
estiverem sujos na árvore o teste passa por construção (`fotos_sendo_refeitas_agora`, `:119-140`);
a mordida só aparece depois do commit.

---

## 4. UMA SEÇÃO POR SPRINT

Cada seção tem três blocos: **roteiro** (arquivo, o que fazer, molde a copiar), **prova de
trabalho** (comandos, com o esperado) e **armadilhas**. O roteiro não está resumido de propósito.

---

### CONFIG-01 — a aba existe e está vazia (O PORTÃO)

Arquivo da sprint:
[CONFIG-01-a-aba-existe-e-esta-vazia.md](CONFIG-01-a-aba-existe-e-esta-vazia.md)

O que ela existe para descobrir já está descoberto, e é um não-evento: **a 11ª aba vazia custa
ZERO de largura e ZERO do orçamento de altura.** Medido com o glade real, sob Xvfb, com o tema
na escala que sai (delta 3), comparando o arquivo de hoje com uma cópia em memória que ganha
`scroll_tab_config_box`/`tab_config_box` mais o rótulo: HOJE `root_box` pede 1140px de largura,
teto por aba 657px, aba mais larga Lightbar 1138px; COM A 11ª, os MESMOS 1140px, os MESMOS
657px, a MESMA Lightbar 1138px. A soma das larguras dos rótulos de aba vai de 601px para 714px;
somando o `padding: 8px 14px` de `theme.css:692-698` (28px por aba) e os `padding: 0 14px` do
header (`:687-691`), a tira pede ~1050px numa janela de 1180 — sobram ~130px e nenhuma seta de
rolagem aparece. **O aceite passa a ser negativo e verificável: "os números não se mexeram".**

#### Roteiro

**0. Confira em que commit você está, antes de qualquer coisa.**
`git rev-parse --abbrev-ref HEAD` tem de dizer `dev` e `git rev-parse --short HEAD` tem de dizer
`70d2876`. Crie `git switch -c sprint/config-01`. NÃO parta da `main` local nem rebase contra
ela. O CI cobre `dev`, `sprint/**` e `onda/**`.

**1. Exporte a cura do snap na sessão inteira.**
`export GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache`.
Sem ela, qualquer processo GTK lançado deste terminal morre com
`Failed to load ... image-missing.svg` — reproduzido, e não é só o `retratar_abas.py`.

**2. `src/hefesto_dualsense4unix/gui/main.glade` — a página nova.**
Ancore por CONTEÚDO, não por número: procure o bloco `<child type="tab">` cujo rótulo é
`Navegação` (hoje `:3951-3953`) e insira DEPOIS dele, antes do `</object>` que fecha o
`main_notebook` (hoje `:3955`; o `<object class="GtkNotebook" id="main_notebook">` abre em
`:218`, e o arquivo tem 4047 linhas). Copie a estrutura de `scroll_tab_home_box` (`:234-247`),
trocando os ids: um `<object class="GtkScrolledWindow" id="scroll_tab_config_box">` com
`visible=True`, `can-focus=False`, `hscrollbar-policy=never`, `vscrollbar-policy=automatic`,
`propagate-natural-height=True`, `propagate-natural-width=True`, `shadow-type=none`, contendo um
único `<object class="GtkBox" id="tab_config_box">` com `orientation=vertical`, `spacing=12`,
`margin=12`. Depois, um `<child type="tab">` com um `GtkLabel id="tab_config_label"` cujo
`label` traduzível é `Configurações`.
**O `id` no box interno não é opcional**:
`test_toda_aba_continua_sendo_reconhecida_pelo_id_do_glade`
(`tests/unit/test_largura_a_mesma_em_todas_as_abas.py:355-381`) assere `None not in nomes` para
TODAS as páginas. Como saber que deu certo: o comando da prova de trabalho imprime
`paginas: 11` e a lista termina em `'Configurações'`.

**3. Arquivo novo — A CRIAR: src/hefesto_dualsense4unix/app/actions/config_actions.py.**
Espelhe `install_home_tab` em `src/hefesto_dualsense4unix/app/actions/home_actions.py:1394`,
dentro de `class HomeActionsMixin(WidgetAccessMixin)` (`:1383`). Conteúdo mínimo:
(a) docstring de módulo em PT-BR **com acentuação completa** (o `.glade` é isento do portão de
acento, o `.py` não — `scripts/validar-acentuacao.py:434` vs `:439`);
(b) `ABA_CONFIG = "tab_config_box"` como constante de módulo, no molde de `ABA_INICIO`
(`home_actions.py:76`) e `ABA_STATUS` (`status_actions.py:96`);
(c) `class ConfigActionsMixin(WidgetAccessMixin):` — importe `WidgetAccessMixin` de
`hefesto_dualsense4unix.app.actions.base`, que é de onde vem o `_get`
(`src/hefesto_dualsense4unix/app/actions/base.py:325`);
(d) `def install_config_tab(self) -> None:` idempotente — pega `box = self._get(ABA_CONFIG)`,
sai cedo se for `None` ou se `getattr(self, "_config_installed", False)`, e então marca
`self._config_installed = True` (molde literal: `home_actions.py:1397-1399`).
**Nada de função pública solta no topo do módulo**: o job `promessa-sem-caminho` varre nós de
topo (`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:1119-1128`) e `tests/` não conta
como chamador. Helper de módulo nasce com `_` na frente, ou nasce chamado.

**4. Ainda no arquivo novo — as cinco seções vazias.**
Para cada uma, um `Gtk.Label` com `set_xalign(0.0)` e
`get_style_context().add_class("hefesto-titulo-secao")` (a classe existe,
`src/hefesto_dualsense4unix/gui/theme.css:114`), empacotado com
`box.pack_start(rotulo, False, False, 0)`. Os cinco textos, na ordem do mockup e com maiúscula
inicial (o portão `palavra-de-tela` cobra maiúscula,
`scripts/validar-palavra-de-tela.py:67`): "Está tudo certo?", "Os controles", "A mesa",
"Orçamento", "A janela". A dica de cada uma sai do `title=` do `<h2>` correspondente em
[mockup/aba-configuracoes.html](mockup/aba-configuracoes.html), aplicada com
`rotulo.set_tooltip_text(...)`. Nenhum widget de conteúdo, nenhum IPC, nenhuma leitura de disco.

> **Contradição registrada** sobre as linhas dos `<h2>` do mockup. CONFIG-01 cita 197, 217, 326,
> 400, 423. CONFIG-06 cita `:196` "0. SAÚDE", `:216` "1. OS CONTROLES", `:325` "2. A MESA",
> `:399` "3. Orçamento", `:422` "4. A janela" — uma linha a menos em cada. Abra o arquivo e
> confira antes de copiar.

**5. `src/hefesto_dualsense4unix/app/app.py` — TRÊS edições, não duas.**
(a) Import do `ConfigActionsMixin`, que por ordem alfabética entra entre `:29`
(`carona_do_wrapper`) e `:30` (`daemon_actions`) — o bloco de imports do pacote vai de `:29` a
`:57`, e `:29-42` é só a fatia dos mixins de `actions/`.
(b) Base da classe: acrescente `ConfigActionsMixin,` à lista de `class HefestoApp(...)`,
`:155-167`. Sem a base, `install_config_tab` não existe no objeto e o `show()` estoura.
(c) **Duas chamadas**: `self.install_config_tab()` no bloco de `show()` (`:1171-1179`, depois de
`install_input_tab()` e ANTES de `self._envolver_paginas_em_teto_elastico()`) **e** no bloco
idêntico dentro de `run()`, no ramo `if start_hidden and self.tray.is_available():`
(`:1435-1443`). Esquecer a segunda repete o BUG-HOME-TAB-HIDDEN-INSTALL-01, cujo comentário
está em `:1432-1434`, e **não existe teste guardando isso** —
`grep -rln start_hidden tests/unit/` é vazio; o teste do passo 8 passa a ser o guarda.

**6. A fita de alvo esmaecida (D4), no arquivo novo mais um gancho em `app.py`.**
A faixa é criada em `src/hefesto_dualsense4unix/app/actions/status_actions.py:1556-1568` e
guardada em `self._target_strip` (`:1568`); `_set_target_strip_visible` está em `:1734-1752` e
só mostra/esconde. Copie o precedente que já existe em `_on_notebook_switch_page`
(`app.py:960-983`), que chama `set_status_tab_visivel(nome == self._ABA_STATUS)` a CADA troca:
acrescente, logo abaixo, a chamada simétrica ao método do mixin novo — algo como
`inativar = getattr(self, "set_alvo_inativo", None)` e `inativar(nome == ABA_CONFIG)`. No mixin,
implemente `def set_alvo_inativo(self, inativo: bool) -> None:` que pega
`strip = getattr(self, "_target_strip", None)`, faz `strip.set_sensitive(not inativo)` e
mostra/esconde um `Gtk.Label` com a razão ("Esta aba vale para a mesa inteira, não para um
controle"), tudo dentro de `contextlib.suppress(Exception)` (restrição 4 da sprint).
**NÃO use `_REFRESH_POR_ABA`** (`app.py:920-957`): aquele mapa só dispara ao ENTRAR na aba
destino, e a fita ficaria esmaecida para sempre depois da primeira visita.

**7. `scripts/gui-captura/retratar_abas.py` — o 11º nome.**
Acrescente `"readme_configuracoes",` ao fim da tupla `NOMES` (`:213-224`; CONFIG-09 cita a mesma
tupla como `:212-224` — abra e confira). Sem isso, `main()` (`:1079-1088`) só imprime um AVISO
em stderr, grava a foto como `aba_10.png` (`:1097`) e sai com 0 — o aceite "as onze abas
fotografam sem erro" sairia verde e errado. Considere plantar aqui também a cura do pixbuf
(`os.environ.setdefault("GDK_PIXBUF_MODULE_FILE", ...)` antes de importar `gi`).

**8. Escreva o portão — A CRIAR: tests/unit/test_config_01_a_aba_nasce_vazia.py.**
A PRIMEIRA linha de import tem de ser `from tests.conftest import exigir_gi_real` seguida de
`exigir_gi_real("aba configurações")`, ANTES de qualquer `import gi` — o padrão está em
`tests/unit/test_layout_orcamento_altura.py:27-33`, e sem ele o passo "Censo de coleta" do job
`lint-test` (`.github/workflows/ci.yml:470-491`) acusa erro de coleta e reprova. O arquivo entra
sozinho no job `gtk-real`. Ele assere quatro coisas:
(a) por `ElementTree` sobre `MAIN_GLADE`, que existe um objeto com `id="tab_config_box"` e um
`<child type="tab">` com rótulo `Configurações`;
(b) por `ast` sobre `app.py`, que `install_config_tab` é chamado DENTRO de `show` **e** dentro
de `run` — a mordida é apagar a segunda chamada e ver reprovar;
(c) que `ConfigActionsMixin` está em `HefestoApp.__mro__`;
(d) que `set_alvo_inativo(True)` deixa `_target_strip` insensível e `set_alvo_inativo(False)` a
devolve — a mordida é trocar o booleano por `True` fixo.

**9. Corrija a própria sprint** com os endereços da seção 5 deste documento: `:212` vira `:218`,
`:219-222` vira `:234-247`, `29-42` vira "29-42 (import) mais 155-167 (base)", Lightbar 1110
vira 1138, teto 1166 vira 1180 de largura e 657 de altura, "26 oficiais" vira "os 20 tokens de
`theme.css:21-54`", e a lista de jargão passa a apontar para
`scripts/validar-palavra-de-tela.py:85`. Nenhum desses erros derruba CI.

**10. Refaça as fotos NO MESMO commit.** `scripts/gui-captura/retratar_abas.py` **sem destino**
(grava em `docs/usage/assets/`) e acrescente uma linha em `docs/usage/assets/CONFERIDO-EM.md` no
formato das de 15/08 e 18/08. Motivo: `tests/unit/test_as_fotos_acompanham_a_versao.py` compara
TOPOLOGIA (`:93-116`) e CONFIG-01 toca `src/.../app` e `src/.../gui`. Isto NÃO estava previsto
na sprint.

**11. Commit.** Formato do `.github/CONTRIBUTING.md`: tipo, ID da sprint, descrição — por
exemplo `feat: CONFIG-01 — a décima primeira aba nasce vazia`. Nunca `--no-verify`: o job
`anonymity` é server-side e pega commit que passou por cima do hook. Confira o arquivo DEPOIS do
commit.

#### Prova de trabalho

```sh
git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD   # dev, descendente de 70d2876
```

As onze páginas e a largura, sob Xvfb (é o ambiente do job `gtk-real`):

```sh
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
xvfb-run -a ./.venv/bin/python -c "
import gi; gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from hefesto_dualsense4unix.app.constants import MAIN_GLADE
b=Gtk.Builder(); b.add_from_file(str(MAIN_GLADE))
nb=b.get_object('main_notebook')
print('paginas:', nb.get_n_pages())
print([nb.get_tab_label_text(nb.get_nth_page(i)) for i in range(nb.get_n_pages())])
"
```

Esperado ANTES: `paginas: 10`, lista terminando em `'Navegação'`. DEPOIS: `paginas: 11`, lista
terminando em `'Configurações'`.

```sh
xvfb-run -a ./.venv/bin/python -m pytest \
  tests/unit/test_layout_orcamento_altura.py \
  tests/unit/test_largura_a_mesma_em_todas_as_abas.py \
  tests/unit/test_paleta_unica.py tests/unit/test_contraste_css.py \
  tests/unit/test_janela_cortada_01_o_rodape_nao_sai_pela_borda.py -q
```

Esperado: verde antes e depois. Baseline de `test_layout_orcamento_altura.py` sozinho em
`dev @ 70d28762`: `7 passed` sob Xvfb, `3 failed, 4 passed` sem. Se você vir as três falhas de
largura, esqueceu o `xvfb-run`.

```sh
xvfb-run -a ./.venv/bin/python -m pytest \
  tests/unit/test_notebook_switch_page.py \
  tests/unit/test_pollers_identificam_aba_por_id.py \
  tests/unit/test_app_scroll_wrap.py \
  tests/unit/test_aba_no_jogo_entra_e_sai_da_tira.py -q
```

Os portões de texto e documento, exatamente como o pre-commit os roda:

```sh
python3 scripts/validar-acentuacao.py --all       # exit 0
python3 scripts/validar-glifos.py --all           # exit 0
python3 scripts/validar-palavra-de-tela.py --all  # exit 0
python3 scripts/validar-referencias-docs.py --all # "OK: N documento(s) sem referência morta."
bash scripts/check_anonymity.sh                   # "OK: anonimato preservado."
```

Baseline medido: os cinco saem 0, e o de referências diz
`OK: 372 documento(s) sem referência morta.`

```sh
./.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
xvfb-run -a ./.venv/bin/python -m pytest tests/unit/test_config_01_a_aba_nasce_vazia.py -q
```

A captura das onze abas:

```sh
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/config01
```

Esperado: a última linha diz `11 aba(s) em /tmp/config01`, existe
`/tmp/config01/readme_configuracoes.png`, e **nada** sai em stderr. Se aparecer
`AVISO: o notebook tem 11 abas e este script conhece 10 nomes`, o passo 7 não foi feito.

As dez abas antigas continuam idênticas (antes de regerar as fotos oficiais):

```sh
diff <(cd /tmp/config01 && sha256sum readme_*.png | grep -v configuracoes | sort) \
     <(cd docs/usage/assets && sha256sum readme_*.png | sort)
```

Esperado: sem saída. Qualquer diferença é a aba nova mexendo em aba antiga — pare e descubra
por quê.

```sh
./.venv/bin/python -m pytest tests/unit/test_as_fotos_acompanham_a_versao.py -q
./.venv/bin/python -m pytest tests/unit -q -x --continue-on-collection-errors 2>&1 | tail -5
ruff check src/ tests/ && mypy src/hefesto_dualsense4unix
pre-commit run --all-files
```

#### Armadilhas

- **A prova de trabalho da sprint começa vermelha, e não é culpa sua.** Ver 2.2. Cura:
  `xvfb-run -a` em todo pytest de geometria. Sem isso você passa a primeira hora consertando um
  layout que está certo.
- **O terminal é um snap e mata todo processo GTK antes do primeiro pixel.** Ver 2.3.
- **`install_config_tab()` em um só lugar entrega uma aba que abre vazia** quando o Hefesto sobe
  minimizado na bandeja — o caminho normal de quem tem autostart. As duas listas são
  `app.py:1171-1179` e `:1435-1443`; o comentário em `:1432-1434` nomeia o defeito já pago.
- **Página sem `id` no widget de conteúdo reprova, e o erro não é onde você vai olhar.**
  `id_da_pagina` (`home_actions.py:79-105`) desce pelo `ScrolledWindow` e pelo `Viewport`. Um
  `Gtk.Bin` nosso devolve `None` mesmo depois de `set_name` — medido em `app.py:1050-1053`.
- **Envolver a página POR FORA quebra os pollers em silêncio.** Lição escrita em
  `app.py:1046-1056` e `:1170`: `_envolver_paginas_em_teto_elastico` entra DENTRO da página. Se
  quiser teto elástico na aba nova (não é necessário aqui), acrescente o nome a
  `_PAGINAS_COM_TETO_ELASTICO` (`app.py:1037-1044`).
- **Pendurar a fita esmaecida em `_REFRESH_POR_ABA` a deixa esmaecida para sempre**, e o seletor
  de alvo do cabeçalho morre no primeiro clique em "Configurações".
- **Commit que toca a tela sem levar as fotos reprova a suíte.**
- **O `retratar_abas.py` não reclama de verdade: avisa em stderr e continua**, com exit 0.
- **Módulo de teste de interface sem `exigir_gi_real()` derruba o CI inteiro na coleta.**
  `pytest.importorskip("gi")` não serve, porque aceita o stub que outro arquivo planta em
  `sys.modules` (`tests/conftest.py:210-245`).
- **O portão de altura não vai ver a sua aba, e isso é o buraco, não o alívio.** `_montar()`
  (`tests/unit/test_layout_orcamento_altura.py:237-252`) carrega o `main.glade` cru e não roda
  `install_*_tab` nenhum; a aba Início é "100% montada em código" por escrito
  (`main.glade:265-266`). Os 1729px do mockup nunca serão medidos por esse portão. É
  literalmente o defeito que PONTO-A-PONTO-01 nomeia: "um portão que olha para o lugar errado é
  pior que portão nenhum, porque encerra a busca". **Cura: o teste novo desta sprint monta a aba
  pelo mixin e mede o conteúdo, não o glade.**
- **Função pública de topo em `config_actions.py` sem chamador reprova um job inteiro.** <!-- ref-externa: arquivo que esta leva cria -->
- **Citar `config_actions.py` num documento antes de ele existir reprova o portão de <!-- ref-externa: arquivo que esta leva cria -->
  referências.** Ver 2.5, regra 2.
- **Rótulo novo no glade começando em minúscula reprova sem perdão**, e o portão também reprova
  exceção que envelheceu (`scripts/validar-palavra-de-tela.py:232-245`).
- **Os hooks locais não rodam nesta máquina.** Ver 2.4.

---

### CONFIG-02 — o que a mesa já sabe dizer

Arquivo da sprint:
[CONFIG-02-o-que-a-mesa-ja-sabe-dizer.md](CONFIG-02-o-que-a-mesa-ja-sabe-dizer.md)

#### Roteiro

**PASSO 0 — confira o terreno antes de escrever uma linha.** `git rev-parse --short HEAD` tem de
ser `70d28762` ou descendente, em `dev`. CONFIG-02 depende de CONFIG-01: se
`find . -name config_actions.py` não achar nada e
`grep -c '<child type="tab">' src/hefesto_dualsense4unix/gui/main.glade` der 10, **pare aqui**.

**PASSO 1 — resolva a decisão de fonte, por escrito, antes de codar.** O sysfs **não entrega o
MAC do adaptador** nesta casa. Medido como usuário 1000, kernel 7.0.11-76070011-generic:
`/sys/class/bluetooth/hci0/` contém apenas `device`, `power`, `reset`, `rfkill2`, `subsystem`,
`uevent`; NÃO existe o arquivo `address`, e o `uevent` traz uma linha só (`DEVTYPE=host`). Prova
com o código do próprio projeto: importar `_adapter_addresses` de
`src/hefesto_dualsense4unix/broker/hidraw_broker.py` e chamá-lo sobre `/sys/class/bluetooth`
devolve `set()`. O docstring de `hidraw_broker.py:166-172` já registrava o sintoma ("hci sem
address legível — visto ao vivo"). O endereço EXISTE via BlueZ no D-Bus de sistema, sem root
(`busctl get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Address`).
Escolha e escreva na sprint: **(a)** nomear pela IDENTIDADE FÍSICA que o sysfs dá e é estável
entre boots — VID:PID mais barramento/porta mais painel ("0489:e0e4, barramento 3, porta 3,
painel traseiro") —, o que cumpre o espírito do aceite ("nunca por `hciN`, que inverte entre
boots") melhor do que o MAC porque também responde "onde está"; ou **(b)** ler o MAC do BlueZ
pelo D-Bus de sistema com `Gio` (PyGObject já é dependência, não é subprocess), aceitando que
HOJE isso não funciona no Flatpak — `flatpak/br.andrefarias.Hefesto.yml:24-47` não tem
`--socket=system-bus` nem `--system-talk-name=org.bluez`. Recomendação do relatório: (a) como
nome, (b) como enriquecimento que degrada calado.

**PASSO 2 — crie A CRIAR: src/hefesto_dualsense4unix/integrations/mesa_de_radio.py.**
Espelhe `src/hefesto_dualsense4unix/integrations/usb_pai.py` (233 linhas): funções de módulo, sem
classe, todas as raízes e leitores como argumentos com default do sistema real, `""` e lista
vazia como resposta legítima. Três funções públicas e nada mais: `adaptadores_bluetooth`,
`radios_do_barramento` e `vizinhancas_apertadas`, com `raiz_bt`, `raiz_usb`, `listar`, `ler` e
`real` injetáveis. Dois dataclasses frozen (`Adaptador`, `RadioUsb`) com campos só de string,
int e bool. NÃO use constante de módulo resolvida por `Path.home()` nem caminho fixo fora de
default de argumento — CANARIO-FS-01, `tests/conftest.py:339-359`, custou duas refatorações.

**PASSO 3 — as regras medidas nesta bancada, cada uma com o motivo em comentário:**
(a) o nó do adaptador sai do `realpath` de `raiz_bt/hciN`, que aponta para a INTERFACE USB
(medido: termina em `usb3/3-3/3-3:1.0`) — suba com `dispositivo_usb_pai` de
`integrations/usb_pai.py:68` em vez de reimplementar;
(b) hub é `bDeviceClass == '09'` **E** nome que NÃO casa `^usb[0-9]+$` — os hubs-raiz `usb1` a
`usb9` também são classe 09 e marcariam a mesa inteira como "em hub";
(c) painel vem de `physical_location/panel` (`back`, `front`, `unknown`) e some atrás de hub —
ausência é "não sei", nunca chute;
(d) "mesmo controlador" é o último `0000:xx:xx.x` do realpath (algoritmo de
`scripts/doctor.sh:4834`), e "colado no vizinho" é mesmo `busnum` com `devpath` numericamente
adjacente; **NÃO porte `pci_label`** (`doctor.sh:4823-4830`), que só conhece os PCI de outra
máquina;
(e) rádio candidato é dispositivo USB com `idVendor` e `idProduct` legíveis que não é hub e não
é o adaptador BT.

**PASSO 4 — se a escolha do PASSO 1 foi ler o BlueZ**, isole a leitura numa função só,
`mac_do_adaptador_por_dbus(caminho: str) -> str`, com `try/except` largo devolvendo `""` e um
comentário dizendo que no Flatpak ela devolve sempre `""`. Ela é a ÚNICA porta de D-Bus do
produto (grep por `Gio.`, `import dbus`, `DBusProxy`, `bus_get_sync` em
`src/hefesto_dualsense4unix/` é vazio); mantenha-a assim, para que o dia da mudança de manifesto
tenha um endereço só.

**PASSO 5 — em A CRIAR: src/hefesto_dualsense4unix/app/actions/config_actions.py** (nascido em
CONFIG-01), acrescente ao `ConfigActionsMixin`: `_instalar_secao_da_mesa()` chamada de dentro de
`install_config_tab()`, e `_reexaminar_a_mesa()` ligada ao botão. Molde de estrutura:
`src/hefesto_dualsense4unix/app/actions/input_actions.py:270` (`install_input_tab()`) mais
`:280` (`_install_key_bindings_treeview()`) — pega o widget por `self._get(id)`
(`actions/base.py:325`), sai cedo com `if widget is None: return`, é idempotente por checar
`get_model() is not None`, monta `Gtk.ListStore` e `Gtk.TreeViewColumn`. Guarda de idempotência
no estilo de `home_actions.py:1394-1400`. `from gi.repository import Gtk` DENTRO da função,
como as duas fazem. O `theme.css` já estiliza `treeview` (`:435-443`) e tem `@elevated` descrito
como "cabeçalho de tabela" (`:45`).

**PASSO 6 — em `src/hefesto_dualsense4unix/gui/main.glade`**, declare dentro da página de
Configurações: os dois `GtkTreeView` (ids `config_mesa_adaptadores_tree` e
`config_mesa_radios_tree`), o rótulo de cabeçalho da seção, o rótulo "Outros rádios que dividem
a faixa" e o botão "Reexaminar a mesa" (id `config_mesa_reexaminar_btn`) — no rodapé DA ABA, ao
lado de "Descartar mudanças", como o mockup mostra em `aba-configuracoes.html:451-455`; o
"Aplicar" continua sendo o do rodapé da janela (`main.glade:3988`). Declarativo e não montado em
Python porque `scripts/validar-palavra-de-tela.py:14-18` só varre o glade — rótulo montado em
código fica fora do portão de propósito. Todo texto com `translatable="yes"`. As dicas saem
literais de [TOOLTIPS.md](TOOLTIPS.md), linhas 98-105; não reescreva na hora.

**PASSO 7 — em `src/hefesto_dualsense4unix/app/app.py`**, acrescente ao `_REFRESH_POR_ABA`
(`:920`) a entrada com o id do `GtkBox` interno e não o do `GtkScrolledWindow` —
`id_da_pagina` (`home_actions.py:79-106`) desembrulha o scroller e o Viewport antes de comparar.
É o que faz a leitura acontecer "ao abrir a aba", como o aceite pede. NÃO ligue a leitura em
`GLib.timeout_add`: os tiques da casa são de 100 ms, 500 ms e 2 s
(`status_actions.py:507-510`) e a sprint proíbe o tique rápido.

> **Contradição registrada.** CONFIG-02 mediu que acrescentar entrada ao `_REFRESH_POR_ABA` é
> livre: "o comentário do código que diz o contrário está errado" — `app/app.py:947-951` afirma
> que `tests/unit/test_notebook_switch_page.py` congela a lista com `==`, mas a única asserção
> sobre o mapa é `test_todo_id_do_mapa_existe_no_glade` (`:128-142`), e os `==` do arquivo
> (`:68`, `:83`, `:92`) são sobre listas de chamadas. CONFIG-09 afirma o oposto, no passo 14:
> "`tests/unit/test_notebook_switch_page.py` congela o `_REFRESH_POR_ABA` com `==` e reprova
> qualquer acréscimo — a linha nova tem de entrar lá também". **Abra o arquivo de teste e decida
> com ele na frente antes de editar o mapa.** Nos dois relatórios a obrigação comum é a mesma:
> a chave tem de ser o id do GLADE do box interno.

**PASSO 8 — ensine `scripts/gui-captura/retratar_abas.py` a montar a aba:**
`_montar_aba_configuracoes(builder)`, espelhando `_montar_aba_inicio` (`:366-405`) — classe
`_Host` mínima herdando `ConfigActionsMixin`, com `_get` resolvendo pelo builder e nenhum IPC.
Alimente-a com raízes **FALSAS** (um dicionário de árvore em memória, pelos mesmos parâmetros
injetáveis do PASSO 2), jamais com `/sys` real. Chame-a ao lado de `_montar_aba_inicio` em
`:1074-1077`. E confira `NOMES` (`:213-224`): com dez nomes, a foto da aba nova sai como
`aba_10.png` e o script só avisa em stderr (`:1081-1088`).

**PASSO 9 — escreva A CRIAR: tests/unit/test_a_mesa_le_o_barramento.py.** Sem árvore de
arquivos: injete `listar`, `ler`, `existe` e `real`, como
`tests/unit/test_a_placa_e_o_controle_pelo_usb_pai.py:271-345` faz. Um teste por linha:
(a) uma mesa de um adaptador lista um; (b) uma de dois lista dois, com nomes distintos e nenhum
"hci"; (c) hub-raiz não conta como hub; (d) aparelho atrás de hub, sem `physical_location`, sai
como "não sei" e não como "frente"; (e) dois aparelhos no mesmo PCI com `devpath` adjacente
geram UM aviso; (f) sysfs vazio ou ilegível devolve lista vazia sem levantar; (g) nenhum caminho
absoluto de `/sys` é lido quando as raízes são injetadas — **este é o teste que protege a
foto.**

**PASSO 10 — meça a geometria ANTES de considerar pronto.** Se estourar, o corte é estrutural
("Os controles" talvez pertença ao cabeçalho da janela) — não é cosmética e não se resolve com
margem menor. Largura: nada de `GtkBox` com `homogeneous` e rótulo longo (a cicatriz de 1004px
em `tests/unit/test_layout_orcamento_altura.py:359-363`); se a tabela não couber em 1180,
embrulhe-a num `GtkScrolledWindow` próprio — nunca com hscroll `AUTOMATIC` no nível da página,
que é `NEVER` por decisão (`app/app.py:1155`, precedente `main.glade:654-658`).

#### Prova de trabalho

```sh
git rev-parse --short HEAD    # 70d28762 ou descendente, em dev
ls /sys/class/bluetooth/hci0/ # a listagem NÃO contém "address"
```

Refaça a medição de `_adapter_addresses` na máquina de quem for implementar antes de aceitar a
decisão de fonte: hoje ela imprime `set()`.

```sh
.venv/bin/python -m pytest tests/unit/test_a_mesa_le_o_barramento.py -q     # N >= 7 passed
xvfb-run -a --server-args="-screen 0 1920x1080x24" \
  .venv/bin/python -m pytest tests/unit/test_layout_orcamento_altura.py -q  # 7 passed
.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
.venv/bin/python -m pytest tests/unit/test_retrato_das_abas_nao_vaza_dado_real.py \
  tests/unit/test_notebook_switch_page.py -q
.venv/bin/python scripts/validar-palavra-de-tela.py
.venv/bin/python scripts/validar-acentuacao.py --all
.venv/bin/python scripts/validar-referencias-docs.py --all
.venv/bin/python -m mypy src/hefesto_dualsense4unix && .venv/bin/python -m ruff check src/ tests/
```

O `validar-referencias-docs.py` sobre a leva inteira já passa hoje: medido, "OK: 13 documento(s)
sem referência morta" — número da pasta, contra os 372 da varredura `--all`.

```sh
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
xvfb-run -a --server-args="-screen 0 1920x1080x24" \
  .venv/bin/python scripts/gui-captura/retratar_abas.py /tmp/config02 --mesa-cheia
```

Esperado: onze linhas na tabela de saída, `11 aba(s) em /tmp/config02`, NENHUM aviso de stderr
sobre quantidade de nomes, e a foto da aba Configurações mostrando os endereços do fixture —
nunca o endereço real que o `busctl` devolve nesta máquina.

**Aceite manual, com o hardware desta bancada:** desplugue um dos receptores 2,4 GHz e reabra a
aba pelo botão "Reexaminar a mesa" — a lista de rádios tem de encolher de três para dois sem
reiniciar a janela, e a linha de vizinhança apertada entre `3-1` e `3-3` (mesmo controlador
`0000:75:00.4`) tem de continuar amarela.

#### Armadilhas

- **A FOTO VAI PUBLICAR O ENDEREÇO BLUETOOTH DELA, e nenhum portão vai avisar.**
  `tests/unit/test_retrato_das_abas_nao_vaza_dado_real.py` abre dizendo que "uma foto da
  interface já vazou endereço Bluetooth real uma vez, e a cura foi um borrão feito à mão". Os
  quatro testes de lá inspecionam o SCRIPT (literais `.json` em `:118-145`, nomes de IPC em
  `:91`) — nenhum enxerga uma aba que lê `/sys` durante o install. Cura: raízes injetáveis
  (PASSO 2) e o `_montar_aba_configuracoes` do PASSO 8 com árvore falsa. Se a foto for tirada
  antes disso, o PNG entra em `docs/usage/assets` sem revisão humana.
- **`bDeviceClass == 09` marca TODO adaptador como "em hub".** Medido: `usb1` a `usb9` (os
  hubs-raiz xHCI) têm classe 09, e todo aparelho pendura sob um deles.
- **`bMaxPower` não distingue hub com fonte própria.** Medido: o hub USB3.1 alimentado (`9-1`)
  reporta `0mA` e o USB2.1 sem fonte (`8-1`) reporta `100mA` — o oposto do palpite. Sem fonte
  medida, o campo nasce em "não sei".
- **Não porte `pci_label` do doctor.** `scripts/doctor.sh:4823-4830` traduz só `*0c:00.3` e
  `*02:00.0`, e nenhum dos dois casa a bancada de hoje (`0000:75:00.4`, `0000:76:00.3`,
  `0000:76:00.4`). O algoritmo de subir até o PCI é portável; a tabela de rótulos é armadilha de
  universalidade.
- **Constante de módulo congela o caminho no import.** CANARIO-FS-01. Molde certo:
  `usb_pai.py:143-160` ou `storm_doctor._allowlist_path` (`:38-52`).
- **O portão de orçamento mede o CONTEÚDO, não o rolador**, e quase nasceu cego
  (`tests/unit/test_layout_orcamento_altura.py:268-292`: com as páginas dentro de
  `ScrolledWindow`, a aba Rumble engordada em 900px deixou os sete testes verdes). A barra de
  rolagem NÃO é licença para crescer.
- **Símbolo público sem chamador reprova um job inteiro.** Entregar o leitor "pronto para
  CONFIG-03 ligar" é entregar um job vermelho.
- **Rolagem horizontal não existe em lugar nenhum desta janela** (`app/app.py:1155` fixa
  `NEVER`; até o rolador aninhado dos cards é `never`, `main.glade:655`). Uma tabela com quatro
  colunas e endereço MAC em fonte mono estoura fácil. Meça a largura da seção antes de escolher
  quantas colunas cabem.
- **Duas colunas do mockup não têm fonte, e a tentação é preenchê-las.** "Firmware: Certo" por
  adaptador não tem check equivalente em `scripts/doctor.sh`; "2 com microfone" não é derivável
  (`state_full` publica `bt_mic` global, `daemon/ipc_handlers.py:2937-2940`, e o DualSense sequer
  implementa A2DP/HFP, `integrations/dualsense_bt_audio.py:8-14`).
- **O `python3` do sistema não serve, e o DISPLAY real derruba o GTK.** Ver 2.2.

---

### CONFIG-03 — a declaração persiste

Arquivo da sprint: [CONFIG-03-a-declaracao-persiste.md](CONFIG-03-a-declaracao-persiste.md)

**A premissa da sprint está errada, e isso encolhe o trabalho.** A camada de configuração fora de
perfil EXISTE e tem três inquilinos, todos em `config_dir()` e todos lidos pelo daemon:
`controllers.json` (`src/hefesto_dualsense4unix/daemon/subsystems/external_identity.py:102`),
`controller_masks.json` (`src/hefesto_dualsense4unix/daemon/subsystems/external_mask.py:173`) e
os sete arquivos-flag de `src/hefesto_dualsense4unix/utils/session.py`, lidos no boot em
`src/hefesto_dualsense4unix/daemon/lifecycle.py:729-791`. O que não existe é lugar para
configuração **de mesa**. A sprint deixa de "criar a camada" e passa a "acrescentar o terceiro
arquivo dessa camada, no molde já pago" — `external_mask.py:89-116`.

#### Roteiro

**PASSO 0 — confira em que commit você está, e ramifique da `dev`.**
`git switch -c sprint/config-03`. Confirme que CONFIG-01 e CONFIG-02 já entraram — CONFIG-03
depende das duas, e o lado da GUI encosta no `config_actions.py` que nasce em CONFIG-01. <!-- ref-externa: arquivo que esta leva cria -->

**PASSO 1 — crie A CRIAR: src/hefesto_dualsense4unix/utils/maquina.py.** Vizinho de
`utils/session.py` de propósito: é o único lugar da árvore que GUI, daemon e CLI importam sem
inverter camada. NÃO ponha em `daemon/` (a GUI passaria a importar daemon); NÃO ponha em `core/`
(que é hardware). Constantes no topo, molde `external_mask.py:173-198`: o nome do arquivo
`maquina.json`, uma versão de schema própria e um lock de módulo. Docstring copiando a estrutura
de `external_mask.py:89-116`: por que arquivo PRÓPRIO (os quatro fatos medidos que proíbem bump
do `controllers.json`), por que versão própria, e a regra "o save preserva o que não entende;
arquivo de versão que não é a nossa não se lê NEM se sobrescreve".

**PASSO 2 — os modelos pydantic no mesmo arquivo**, molde
`src/hefesto_dualsense4unix/profiles/schema.py:942-948` (`model_config = ConfigDict(extra="forbid")`
em `:945` e `version: Literal[1] = 1` em `:948`). Cinco classes, todas com `extra="forbid"` e
TODO campo opcional com default `None` ou vazio (invariante 1: todo campo nasce em "não sei").
`RadioDeclarado` (tipo entre wifi, teclado, mouse, webcam, caixa_de_som, outro; e descrição);
`MesaDeclarada` (altura da antena acima/abaixo; linha de visada livre/com_gente; `radios` como
dicionário chaveado por "vid:pid" em hex minúsculo); `ControleDeclarado` (modo entre xinput,
dinput, switch; rótulo dos botões entre xbox e nintendo; cor); `OrcamentoDeclarado` (política
entre economia, balanceado, max, auto); `MaquinaConfig` (versão, mesa, controles, orçamento,
ambiente entre cosmic, gnome, outro).
**TRÊS campos do mockup ficam FORA, e o comentário tem de dizer por quê:** número de jogador
(dono é `controllers.json`, via `identity.number.set`, `daemon/ipc_handlers.py:1513`), máscara
por aparelho (dono é `controller_masks.json`, `external_mask.py:173`) e tamanho do texto (dono é
`gui_preferences.json`, `src/hefesto_dualsense4unix/app/theme.py:39`).
A chave é `"max"`, nunca `"máximo"` — o rótulo de tela é mapeado em `_POLICY_LABEL`
(`src/hefesto_dualsense4unix/app/actions/rumble_actions.py:79-84`), e gravar o rótulo faz o
`extra="forbid"` recusar o documento inteiro.

**PASSO 3 — um `field_validator` que RECUSA chave de controle que não seja MAC de hardware**:
doze hex minúsculos, rejeitando explicitamente o primeiro octeto `02` (endereço sintetizado). O
motivo está medido em `daemon/subsystems/external_identity.py:104-133`: o `usb_probe_degrade` do
nosso DKMS forja `02` mais VID, PID e bus, e dois clones diferentes recebem o MESMO endereço —
persistir isso grava em disco uma FUSÃO de aparelhos. A canonização continua sendo do daemon;
aqui é só o portão do schema, para a camada não depender de o chamador lembrar.

**PASSO 4 — três funções de módulo, e só três.**
`caminho_da_maquina() -> Path`: import LAZY de `config_dir` dentro do corpo, molde exato de
`external_mask.py:406-411` — no topo do módulo o monkeypatch dos testes não pega, e
`src/hefesto_dualsense4unix/app/gui_prefs.py:21` é a cicatriz disso.
`carregar_maquina() -> MaquinaConfig`: NUNCA levanta; ausente, ilegível, truncado, não-objeto ou
de versão que não é a nossa devolvem tudo em "não sei", com `logger.debug`; molde de tolerância
em `utils/session.py:56-70` e em `external_mask._ler_documento` (`:413-425`).
`gravar_maquina(cfg) -> bool`: sob o lock, relê o disco; se houver documento com versão
diferente, devolve `False` e **NÃO TOCA NO ARQUIVO** (regra de `external_mask.py:266-268` —
escolha de alguém não se destrói para registrar outra); caso contrário escreve atômico
(`tempfile.mkstemp` no diretório de destino mais `os.replace`), molde de `utils/session.py:41-55`.

**PASSO 5 — o daemon lê no boot.** Em `src/hefesto_dualsense4unix/daemon/lifecycle.py`, declare o
campo junto dos irmãos de estado persistido (`_native_mode` em `:558`, `_native_emu_stash` em
`:561`, `_paused` em `:630`), com `field(default_factory=...)` porque é dataclass. Depois, no
`Daemon.run()`, dentro do bloco de leituras de disco de `:729` a `:791`, logo abaixo do
`load_native_mode()` de `:739-740`, importe e chame `carregar_maquina()`, com comentário
nomeando CONFIG-03 e a invariante 2 (a declaração ainda NÃO muda comportamento — quem consome é
CONFIG-04 e CONFIG-05).

**PASSO 6 — o método IPC.** Em `src/hefesto_dualsense4unix/daemon/ipc_server.py`, no dicionário
`_handlers` de `__post_init__` (`:106-183`), acrescente `"machine.declare"` com comentário de uma
linha nomeando a sprint. Em `src/hefesto_dualsense4unix/daemon/ipc_handlers.py`, escreva
`_handle_machine_declare`: valida com `MaquinaConfig.model_validate(...)` e converte
`ValidationError` em `ValueError` (o dispatcher já traduz para `CODE_INVALID_PARAMS`); chama
`gravar_maquina`; em sucesso atualiza o campo do daemon e devolve `{"status": "ok", ...}`; em
recusa devolve `{"status": "recusado", "reason": "versao_desconhecida"}` — recusa no CORPO, com
motivo, nunca erro JSON-RPC: é a doutrina do commit `d614d04f` e a razão de `_call_checked`
(`src/hefesto_dualsense4unix/app/ipc_bridge.py:286-307`) não bastar. **NÃO publique a declaração
no `daemon.state_full`** (`ipc_handlers.py:2165-2166`, 20 Hz).

**PASSO 7 — a ponte da GUI.** Em `app/ipc_bridge.py`, espelhe `identity_number_set`
(`:549-580`) linha a linha: um dicionário `_MOTIVOS_MAQUINA` acima da função (molde
`_MOTIVOS_NUMERO`, `:531-547`) traduzindo `"versao_desconhecida"` para a frase da janela, e
`machine_declare(maquina) -> tuple[bool, str | None]` chamando `_safe_call`. Devolve
`(False, None)` com daemon offline e `(False, motivo)` com recusa — a distinção existe porque a
tela diz coisas diferentes nos dois casos. Acrescente ao `__all__` (região de `:858`).

**PASSO 8 — o gesto de gravar.** Em
`src/hefesto_dualsense4unix/app/actions/footer_actions.py`, no TOPO de `on_apply_draft`
(`:208`), logo depois de `self.pegar_carona_no_gesto(GESTO_APLICAR)` (`:246`) e ANTES do
`pendente = getattr(...)` de `:247`, chame o método novo do `config_actions.py`, com saída cedo <!-- ref-externa: arquivo que esta leva cria -->
quando não há declaração pendente. Comente a escolha do lugar: `on_apply_draft` retorna cedo
para `_aplicar_escolha_pendente` em `:250`, e os três callbacks dele (`_done` `:360`, `_fail`
`:427`, `_sem_relancar` `:450`) chamam `_apply_draft_agora` (`:461`) cada um — pendurar lá
dentro gravaria duas vezes por clique. Do lado da leitura, `install_config_tab()` chama
`carregar_maquina()` uma vez ao montar a aba.

**PASSO 9 — regenere o contrato IPC e escreva a prosa.**
`.venv/bin/python scripts/gerar-contrato-ipc.py` reescreve o bloco gerado de
`docs/protocol/ipc-unix-socket.md` (hoje 38 métodos, depois 39). Além do bloco, escreva à mão
dois parágrafos de contrato citando o método novo entre crases FORA do bloco gerado — o gerador
tem uma coluna "Contrato em prosa" que marca como ausente todo método que só aparece na tabela.
Commite o documento no MESMO commit do método, senão reprova no hook `contrato-ipc-publicado`
(`.pre-commit-config.yaml:140`) e no job `referencias-docs` (`ci.yml:154`).

**PASSO 10 — a bateria.** Crie A CRIAR: tests/unit/test_maquina_a_declaracao_persiste.py,
copiando a bancada de `tests/unit/test_external_mask.py` (373 linhas): docstring nomeando as
propriedades vigiadas (`:1-20`), MACs da faixa forjada `aa:bb:cc:*` (`:47-49`) e a fixture
hermética `_hermetico` de `:62-77`, que faz `monkeypatch.setattr(xdg_paths, "config_dir", ...)`
sobre um `tmp_path`. Oito asserções: (1) sem arquivo, tudo em "não sei" e sem levantar; (2) ida
e volta; (3) arquivo com versão 2 não é lido NEM sobrescrito e os bytes do disco continuam
idênticos; (4) JSON truncado e JSON que não é objeto caem no default; (5) chave de controle
volátil é recusada pelo schema; (6) chave desconhecida dentro da v1 é recusada pelo
`extra="forbid"`; (7) `"máximo"` é recusado e `"max"` é aceito; (8) o daemon lê no boot. Se algum
teste importar `footer_actions.py` (que puxa `gui_dialogs`), chame `exigir_gi_real()`
(`tests/conftest.py:210`) ANTES do bloco de imports — `tests/**` tem `E402` e `I001` liberados
para isso (`pyproject.toml:106-107`).

#### Prova de trabalho

```sh
.venv/bin/python -m pytest tests/unit/test_maquina_a_declaracao_persiste.py -q   # 8 passed
.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
.venv/bin/python scripts/gerar-contrato-ipc.py --check   # 39 métodos; hoje diz 38
.venv/bin/mypy src/hefesto_dualsense4unix                # Success
.venv/bin/ruff check src/ tests/                         # All checks passed
bash scripts/check_test_data.sh                          # exit 0 (use aa:bb:cc:* no teste novo)
.venv/bin/python scripts/validar-referencias-docs.py --all
pre-commit run --all-files
```

**Ida e volta real, com o daemon de pé:** abrir a janela, declarar "Acima" em altura da antena e
"Economia" no orçamento, clicar Aplicar; conferir que o `maquina.json` em
`~/.config/hefesto-dualsense4unix/` tem `"version": 1`, `"altura_da_antena": "acima"` e
`"politica": "economia"`; fechar e reabrir a janela — as duas escolhas continuam marcadas;
apagar o arquivo e reabrir — a aba abre com tudo em "não sei", sem diálogo de erro e sem linha
de aviso no rodapé.

**Recusa por versão, à mão:** escrever `{"version": 2}` no arquivo, clicar Aplicar, e conferir
DUAS coisas — o rodapé mostra a frase de `_MOTIVOS_MAQUINA` (não "daemon offline?"), e o arquivo
continua `{"version": 2}` intacto.

**Boot:** reiniciar o daemon com o arquivo no disco e ler o log — a leitura do PASSO 5 aconteceu
sem exceção. Repetir com o arquivo corrompido à mão (metade de um JSON): o daemon tem de subir
igual.

#### Armadilhas

- **Resolver `config_dir()` no topo do módulo mata a bateria hermética.** `app/gui_prefs.py:21`
  faz isso e por isso é inisolável; `utils/session.py:88` e `:110` fizeram import LAZY com o
  comentário literal "preserva o ponto de monkeypatch nos testes".
- **Gravar o número de jogador no `maquina.json` cria dois donos do mesmo valor.** Mesma coisa
  com a máscara e com o tamanho do texto. Espelhar estado entre duas superfícies foi a classe de
  bug que ABAS-01 curou.
- **Persistir identidade volátil grava uma fusão de aparelhos.** Ver PASSO 3.
- **`extra="forbid"` recusa o documento INTEIRO, não o campo.** Por isso o portão é a VERSÃO, e
  nunca um bump silencioso.
- **Pendurar a gravação em `_apply_draft_agora` grava duas vezes por clique.**
- **Tentar empurrar a declaração por `daemon.reload` levanta.** O handler valida contra
  `set(DaemonConfig.__dataclass_fields__)` e faz `raise ValueError` em chave desconhecida
  (`ipc_handlers.py:4130-4135`). Método próprio é obrigatório. (Isso também desmente pela metade
  a linha de D-A3 que diz não existir nada parecido com `config.set`.)
- **Método IPC novo sem `docs/protocol/ipc-unix-socket.md` regenerado reprova duas vezes.** O
  `--check` compara CONTEÚDO, não mtime, de propósito (MAPA-CONTEUDO-01).
- **Função pública de módulo sem chamador de produção reprova em job próprio.** Auxiliar de teste
  leva `_` no nome — precedente `_zerar_registro_de_mascaras` (`external_mask.py:608`). E a saída
  de emergência (declarar lacuna) tem preço: o registro reprova razão sem data e lacuna que
  envelheceu (`portao_a_casa_sabe_e_o_produto_nao_faz.py:1325-1360`).
- **Publicar a declaração no `daemon.state_full` a põe no tique de 20 Hz**, contra o aceite
  escrito de CONFIG-02.
- **A prova de trabalho escrita na sprint mente por omissão.** `pytest tests/unit/ -k "maquina or config" -q`
  devolve `247 passed, 1 skipped, 10320 deselected` hoje, nenhum sobre `maquina.json`. É a
  família exata de PONTO-A-PONTO-01. Troque pelo caminho do arquivo novo antes de escrever a
  primeira linha de código.
- **O rótulo "Máximo" não é a chave.** `RumbleConfig.policy` grava `"max"`
  (`profiles/schema.py:336`); o mapa chave-para-rótulo vive em `rumble_actions.py:79-84`, nascido
  de LEIGO-06 porque o toast ecoava a chave interna. Gravar `"máximo"` faz o sintoma na tela ser
  "não consegui gravar", não "valor inválido".

---

### CONFIG-04 — o medidor de rádio

Arquivo da sprint: [CONFIG-04-o-medidor-de-radio.md](CONFIG-04-o-medidor-de-radio.md)

#### Roteiro

**PASSO 0 — antes de tocar em código, feche quatro decisões que a sprint não tem.** Sem elas o
medidor não é implementável, só desenhável.
**(a) QUANTOS SLOTS POR RELATÓRIO.** 1.600 slots/s vem de 625 µs por slot no Bluetooth Classic;
quantos slots um relatório HID de 78 B consome é a metade que falta, e ela **não está escrita em
lugar nenhum da árvore** (grep por `1600`, `625 µs`, "slot" e "fatia de tempo" em `src/`,
`scripts/`, `docs/protocol/` e `docs/data/` não acha nada com este sentido; o único lugar é o
próprio mockup, `aba-configuracoes.html:366-367`, e `TOOLTIPS.md:102`). Confira também que
`831 = 32,4% + 19,5% de 1600 = 518,4 + 312` e que esses dois valores NÃO se reconstroem a partir
do A/B medido nem a 1 slot por relatório (601,4 / 212,4) nem a 2 (1202,8 / 424,8) para os "3
controles, 2 com microfone" que a mesma tabela declara.
**(b) QUAL Hz POR CONTROLE.** As constantes honestas são as do A/B de 25/07
(`src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py:76-78`), mas o E-2/E-6 mediu
157,8-402,9 Hz de envelope. Decidir se o medidor usa o nominal do A/B (recomendado, porque é o
que o selo "derivado da especificação" promete) ou tenta medir.
**(c) O QUE CONTA COMO "COM MICROFONE":** só a ponte agente por HID, nunca a placa USB.
**(d) OS LIMIARES DA PALAVRA.** O mockup mostra "Folgada" (`aba-configuracoes.html:370`) sem
dizer a partir de quanto vira outra coisa. Escreva as três palavras e os dois cortes na sprint, e
escreva no mesmo lugar a frase de fronteira: **o medidor fala de ocupação, nunca de culpa.**

**PASSO 1 — crie A CRIAR: src/hefesto_dualsense4unix/integrations/radio_da_mesa.py**, módulo
puro, sem GTK e sem IPC. Espelhe a forma de `integrations/usb_pai.py` (cabeçalho que conta O
PROBLEMA QUE ESTE MÓDULO RESOLVE e O QUE ELE NÃO É; funções com `listar`, `ler`, `existe` e
`real` injetáveis). Conteúdo: (1) as constantes com procedência escrita na própria docstring —
1600 slots por segundo (especificação, 625 µs por fatia, NÃO medido aqui), 260.4 Hz de input sem
mic, 170.5 Hz de input com mic, 106.2 Hz de áudio com mic, todas com a citação
`integrations/dualsense_bt_audio.py:76-78` e a data 2026-07-25; (2) na MESMA docstring, o
envelope medido (354,4-402,9 Hz num controle e 173,2-232,3 Hz no outro,
`docs/data/ensaios-brutos/2026-08-15-E2-taxa-dos-oito-nos.csv:6` e `:8`) e a frase de que a
desigualdade é ABERTA — é ela que impede o próximo leitor de transformar a constante em
diagnóstico.

**PASSO 2 — no mesmo arquivo, escreva `adaptador_por_uniq(...)`.** Copie linha a linha
`usb_pai.usb_pai_por_uniq` (`integrations/usb_pai.py:161-201`): mesma normalização por
`_so_hex`, mesma chave devolvida COMO VEIO, mesmo `""` para ausência. A única troca é o que se
extrai do uevent: além de `HID_UNIQ=` (que vira a chave de busca), leia `HID_PHYS=` e devolva
esse valor. Justificativa a citar no docstring:
`src/hefesto_dualsense4unix/broker/hidraw_broker.py:281` (o comentário literal de que BT real tem
`HID_PHYS` igual ao MAC do adaptador) e `:282-284`. Regra de honestidade: controle em cabo tem
`HID_PHYS` de barramento USB, não MAC — devolva `""` para ele, porque controle no fio não ocupa
rádio nenhum. Valide o formato com a mesma regex de MAC que o broker usa
(`hidraw_broker.py:123`).

> **Tensão registrada.** CONFIG-02 mediu que `_adapter_addresses` devolve `set()` nesta máquina
> (o `hci` não publica `address` no sysfs). CONFIG-04 registra ressalva própria: não observou o
> `HID_PHYS` ao vivo, porque há um só `hci0` aqui e zero DualSense conectado; o fato está lido no
> código e nos comentários, não na bancada. O `HID_PHYS` do uevent do HID é um caminho diferente
> do `address` do `hci`, e CONFIG-02 confirmou que ele abre como uid 1000 — mas confirme com um
> controle na mão antes de fechar a sprint.

**PASSO 3 — a função pura do cálculo.**
`ocupacao_por_adaptador(controles, *, com_ponte_de_mic=frozenset()) -> dict[str, Ocupacao]`, onde
`controles` é a lista `state["controllers"]` como já chega (cada item com `transport` e `uniq`
sem dois-pontos, ver `tests/fixtures/state_full_quatro_controles.json`) e `com_ponte_de_mic` é o
conjunto de `uniq` com a ponte agente de pé. `Ocupacao` é um dataclass congelado com
`slots_input`, `slots_audio`, `slots_teto`, `fracao_input`, `fracao_audio` e `rotulo`. Regras:
controle com `transport != "bt"` é DESCARTADO; controle bt sem adaptador legível vai para uma
chave de ausência e a tela diz que não sabe, nunca empresta o adaptador do vizinho; fração é
limitada a 1.0 na barra, mas o NÚMERO cru continua sendo mostrado, porque estourar o teto é
justamente o que a barra precisa saber dizer.

**PASSO 4 — leve o dado por controle da ponte de microfone até a janela, editando DOIS pontos.**
(4a) Em `src/hefesto_dualsense4unix/daemon/subsystems/bt_mic.py`, acrescente à classe
`BtMicSubsystem` (que hoje termina no `_loop`, `:124-133`) uma property que devolva o conjunto de
`uniq` com ponte de pé, e `frozenset()` quando não há gerenciador. As peças existem:
`GerenciadorMicBluetooth.pontes` é `@property` em
`integrations/dualsense_bt_audio.py:1131-1133`, cada ponte guarda `self.no` em `:821`, e o `uniq`
está em `:327`.
(4b) Em `src/hefesto_dualsense4unix/daemon/ipc_handlers.py:2937-2940`, o bloco que já monta
`result["bt_mic"]` com `enabled` e `running` ganha uma terceira chave com a lista de `uniq`, lida
do subsystem por `getattr` com fallback para lista vazia — o mesmo estilo defensivo que o bloco
vizinho já usa. **NÃO crie método IPC novo**: é campo a mais num bloco existente. Assuma por
escrito que isso contraria o "sem IPC novo" de CONFIG-02, e lembre que passa pelo
`gerar-contrato-ipc.py --check` do job `referencias-docs` (`ci.yml:111`).

**PASSO 5 — escreva o widget em
`src/hefesto_dualsense4unix/app/widgets/sensor_widgets.py`**, no bloco que já existe para GTK
real (o mesmo que hospeda `LightbarBar` em `:429` e `SpeakerBar` em `:466`), e o gêmeo de stub no
bloco sem GTK (onde mora o `class SpeakerBar` de `:614`). `MedidorDeRadio(Gtk.DrawingArea)`,
molde literal do `SpeakerBar`: `__init__` com `set_size_request` e `connect("draw", ...)`; um
`set_ocupacao(fracao_input, fracao_audio)` que só chama `queue_draw()` quando algo mudou (a
guarda está em `SpeakerBar.set_volume`, `:475-481`, e é o que impede repintura a 10 Hz); e
`_on_draw` desenhando trilha, depois a fatia de entrada, depois a de áudio deslocada pela largura
da primeira, depois o contorno. Duas constantes de cor novas ao lado das que já existem em
`:26-49`: entrada em `#bd93f9` (o roxo do mockup) e áudio em `#8be9fd` (o ciano). As duas já
constam de `tests/unit/test_paleta_unica.py:19-35`. **NÃO use `#ff79c6`**:
`src/hefesto_dualsense4unix/gui/theme.css:28` reserva o rosa para marca e aba ativa, e o
`mockup/README.md:16-18` está desatualizado nesse ponto.

**PASSO 6 — ligue o medidor na seção "A mesa" que CONFIG-02 construiu.** Uma instância POR
ADAPTADOR, rotulada pelo endereço e nunca por `hciN`. O texto ao lado é montado em Python
(`831/1600 · derivado da especificação`), porque os números são dinâmicos e porque assim ele fica
fora do alcance do `validar-palavra-de-tela.py`, que só varre o glade (`:12-18`). A tooltip, essa
sim, é estática: copie a de `TOOLTIPS.md:102` sem mudar a primeira letra (ela começa com
"Aritmética", então está certa). Registre a aba no mapa de refresh por ID do Glade
(`app/app.py:920`) e identifique a página por `home_actions.id_da_pagina` (`:79`) — nunca por
índice, EST-10. Cadência: ao abrir a aba e no botão "Reexaminar a mesa", nunca no tique de 10 Hz.

**PASSO 7 — escreva A CRIAR: tests/unit/test_medidor_de_radio.py.** Se separar as regras puras
num arquivo próprio, ele coleta headless sem guarda nenhuma (e o censo de coleta agradece); se
tocar em widget, `exigir_gi_real()` no topo. O que ele assere: (1) controle em cabo não entra na
conta de nenhum adaptador; (2) dois controles bt no mesmo `HID_PHYS` somam no mesmo medidor, e em
`HID_PHYS` diferentes vão para medidores diferentes; (3) o mesmo controle, com e sem `uniq` no
conjunto de pontes, produz áudio maior que zero e input MENOR — e a soma quase não se move (a
invariante é a razão 276,7/260,4, menos de 7% de diferença); (4) sysfs ilegível não levanta e
devolve ausência, nunca um adaptador chutado; (5) `uniq` com e sem dois-pontos casam. **A mordida:
arranque a exclusão de `transport != "bt"` do PASSO 3 e pelo menos um nó tem de reprovar.**

**PASSO 8 — reescreva a própria sprint.** Trocar a fonte do A/B para
`integrations/dualsense_bt_audio.py:74-78` (o bloco literal NÃO está em
`daemon/subsystems/bt_mic.py`, que só tem a versão arredondada em prosa, `:14-21`) e acrescentar
a terceira linha da medição, que a sprint omite: `desligado again: input 274.3 Hz  audio 0.0 Hz
total 274.6 Hz`. Ela não é detalhe: é a prova de que o efeito é de BANDA e não estado preso no
firmware (`dualsense_bt_audio.py:86-88` diz isso com todas as letras), e é ela que sustenta o "a
soma quase não se move" do aceite. Acrescentar os endereços dos 381,54/191,40
(`docs/data/ensaios-brutos/2026-08-15-E2-taxa-dos-oito-nos.csv:6` e `:8`) e o envelope. Escrever
a aritmética decidida no PASSO 0. Reescrever o aceite como ensaio de terminal com o aviso do PS
preso. E corrigir de passagem `mockup/README.md:16-18` (o rosa não está mais no medidor) e o
limite falso de CONFIG-02 sobre a atribuição controle-para-adaptador.

#### Prova de trabalho

```sh
git rev-parse --abbrev-ref HEAD && git log --oneline -1
python3 -m pytest tests/unit/test_medidor_de_radio.py -q
python3 -m pytest tests/unit/test_paleta_unica.py -q
python3 -m pytest tests/unit/test_o_interruptor_do_mic_no_card.py \
  tests/unit/test_o_interruptor_do_mic_por_bluetooth.py -q
python3 -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q   # ~2 min
python3 -m pytest tests/unit/test_layout_orcamento_altura.py -q
python3 scripts/validar-palavra-de-tela.py --all
python3 scripts/validar-referencias-docs.py --all
python3 scripts/gerar-contrato-ipc.py --check
ruff check src/ tests/ && mypy src/hefesto_dualsense4unix
```

Se `test_o_interruptor_do_mic_por_bluetooth.py` reprovar, você fez `controller_card.py` falar com
`dualsense_bt_audio` de novo (`test_o_card_nao_fala_com_o_modulo_da_ponte`, `:101`) — o medidor
não pode ressuscitar o interruptor removido em 16/08.

**ACEITE NO APARELHO, e só ele fecha a sprint.** Com UM DualSense em rádio: (1) abrir a aba e
conferir que a barra daquele adaptador mostra folga larga e o rótulo diz o endereço do
adaptador, nunca `hci0`; (2) `HEFESTO_DUALSENSE4UNIX_BT_MIC=1 hefesto-dualsense4unix mic bt-status`
lista as pré-condições sem subir nada; (3) `HEFESTO_DUALSENSE4UNIX_BT_MIC=1 hefesto-dualsense4unix mic bt`
sobe a ponte, e a barra do MESMO adaptador passa a mostrar duas fatias, a de entrada menor que
antes e a soma quase parada. **LEIA A PRIMEIRA ARMADILHA ANTES DE FAZER ISTO.**

**CONTROLE NEGATIVO**, que é o que separa medidor de decoração: com todos os controles no CABO, a
barra de todo adaptador tem de ficar em zero.

#### Armadilhas

- **A ponte de microfone NÃO É SEGURA, e o aceite da sprint manda subi-la.** Medido duas vezes em
  16/08/2026
  (`docs/process/estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md`):
  com a ponte de pé o botão PS aparece pressionado em pulsos de ~17 ms (`held_ms=17.6 / 17.5 /
  17.9`), o daemon abre a Steam em laço, e o relato foi "o teclado, o mouse (tava teclando sem
  parar e o botão direito do mouse também) ... desliguei o controle e parou". A segunda rodada já
  tinha o filtro do bit de áudio e travou igual, em 10 segundos. **CURA: faça o aceite com a
  Steam fechada, com a janela do Hefesto em foco e com o dedo no botão de desligar o controle; e
  escreva esse aviso no texto do aceite antes de pedir o ensaio a ela.** Nunca ligue a ponte por
  padrão, nunca ofereça o gesto na tela.
- **O medidor promete diagnóstico que a medição não sustenta.** Dois controles no MESMO adaptador
  diferiram por quase o dobro com a mesa FOLGADA (381,54 contra 191,40 Hz), a desigualdade
  sobreviveu à troca de unidades ("não é defeito de um aparelho, é comportamento do braço") e o
  motivo é ABERTO em `docs/data/mapa-controles.csv`. CURA: escreva o limite como CÓDIGO — o
  rótulo da barra é uma de três palavras sobre ocupação e não aceita nenhuma frase de causa; e
  ponha um nó de teste que reprove se a string de saída contiver palavras de culpa.
- **Usar `motion_hz` porque ele já está no estado.** `core/physical_report_reader.py:246` fixa
  `MOTION_EMIT_MAX_HZ = 250.0`, e `:218-227` avisa que ler "o rádio é mais lento que 250 Hz, logo
  o cap sobrou" é a leitura ERRADA. O que `daemon/ipc_handlers.py:2810-2815` publica é a taxa de
  ENTREGA ao vpad (EMA, morre em 1 s de silêncio), não a taxa do rádio — e o rádio medido chega a
  402,9 Hz. Um controle a 381 Hz apareceria como 250, e a barra sairia do vermelho exatamente
  quando a mesa está cheia.
- **Contar o microfone errado.** A janela tem três coisas chamadas microfone e só uma custa
  rádio: `controllers[].audio.mic_mudo`/`mic_externo` é placa USB (e por rádio o DualSense não
  publica placa ALSA nenhuma, medido 15/08); `bt_mic` é do PROCESSO
  (`ipc_handlers.py:2937-2940`), não do controle — com quatro controles e uma ponte ele diz
  `running: true` e o medidor pintaria áudio nos quatro.
- **Pintar a fatia de microfone de rosa.** `test_paleta_unica` NÃO pega esse erro, porque
  `#ff79c6` é cor legítima da paleta — só está no papel errado.
- **Declarar o selo "derivado da especificação" como rótulo estático no glade** reprova por
  primeira letra minúscula (`scripts/validar-palavra-de-tela.py:174-186`, e `:62` mostra que ele
  varre também `tooltip_text`).
- **Entregar o cálculo sem a tela, "para a próxima sprint ligar".** Constantes escapam do
  `promessa-sem-caminho` (`portao_a_casa_sabe_e_o_produto_nao_faz.py:64-72`: "uma constante é um
  VALOR, não um comportamento"); funções e classes não.
- **Medir a altura da aba localmente sem as fontes do CI e acreditar no número.** Ver 2.2.
- **Identificar a aba nova por índice.** Já custou uma vez: `app/app.py:920` guarda o comentário
  de que a aba "Navegação DSX" renumerou as páginas e um mapa por índice teria passado a chamar o
  refresher errado em silêncio.
- **Ler o adaptador uma vez e guardar.** `broker/hidraw_broker.py:167-171` avisa que o sysfs de
  Bluetooth é instável ao vivo (adaptador down, rfkill, `hci` sem `address` legível). Leitura
  falha vira "não sei", nunca um adaptador chutado nem uma barra em zero fingindo folga.
- **Fazer o commit e confiar no que ficou no arquivo.** Ver 2.4.

---

### CONFIG-05 — orçamento como teto

Arquivo da sprint: [CONFIG-05-orcamento-como-teto.md](CONFIG-05-orcamento-como-teto.md)

#### Roteiro

**PASSO 0 — CONFIRME O TERRENO.** `git rev-parse --short HEAD` e `git rev-parse --abbrev-ref HEAD`:
esperado `70d28762` em `dev`. Ramo coberto pelo CI: `sprint/config-05` (`ci.yml:10-26`). Depois
confirme que CONFIG-03 entrou: se `maquina.json` não existir como schema em `src/`, **CONFIG-05
PARA AQUI** — não há onde a escolha do orçamento persista, e o daemon não a veria.

**PASSO 1 — CORRIJA O TEXTO DA PRÓPRIA SPRINT ANTES DE CODIFICAR.**
(a) Na seção "Vocabulário", substitua a lista de quatro rótulos por uma tabela CHAVE para RÓTULO
com as **cinco** chaves reais de `src/hefesto_dualsense4unix/profiles/schema.py:336`
(`economia`, `balanceado`, `max`, `auto`, `custom`), marcando `custom` como fora do orçamento —
é o deslizador livre, com teto `RUMBLE_CUSTOM_MULT_MAX = 2.0` (`schema.py:76`), que acima de 1.0
AMPLIFICA. Rótulos vêm de `_POLICY_LABEL`
(`src/hefesto_dualsense4unix/app/actions/rumble_actions.py:79-84`); importe, não redigite.
(b) Troque os dois "40 %" (linhas 20 e 33) por **30 %**:
`RUMBLE_POLICY_MULT` (`src/hefesto_dualsense4unix/daemon/subsystems/rumble.py:82-86`) é
`{"economia": 0.3, "balanceado": 1.0, "max": 1.5}`, e a tela JÁ diz 30 % hoje
(`src/hefesto_dualsense4unix/gui/main.glade:1654`). O mesmo em `TOOLTIPS.md:107` e no mockup
(linha 405 e a célula da tabela em `:410`).
(c) A célula "Vibração vezes Máximo" do mockup (`aba-configuracoes.html:411`) diz 100 % e é
**150 %**: `RUMBLE_POLICY_MULT["max"] = 1.5` amplifica meio a mais do que o jogo pediu e satura
em 255 a partir de 170. O glade escreve isso literalmente em `main.glade:1767-1770`. A dica do
botão Máximo tem de dizer a saturação (SATURA-01, 11/08/2026).
(d) Reescreva a seção "Auto" (linhas 40-43) com a escada real de bateria: `_effective_mult`
(`src/hefesto_dualsense4unix/core/rumble.py:51`, ramo do auto em `:100-121`) **não lê transporte
nenhum** — lê só `battery_pct`, com três degraus (acima de 50 %: 1.0; entre 20 e 50 %: 0.7;
abaixo de 20 %: 0.3). O docstring em `:78-86` registra a decisão de 11/08/2026: "o auto existe
para POUPAR bateria — amplificar seria fazer o oposto do que ele promete". **Ou** apague
"controle no cabo joga em Máximo", **ou** declare que CONFIG-05 está mudando a regra do Auto — e
nesse caso a sprint tem de listar como entrega obrigatória a edição de `rumble_policy_auto_label`
(`main.glade:1773-1774`), do tooltip do botão Auto (`main.glade:1678`) e do docstring de
`_effective_mult` (`core/rumble.py:73-86`), que são o dono único da frase.

**PASSO 2 — DECIDA E ESCREVA A SEMÂNTICA DO TETO ANTES DO CÓDIGO.** O produto tem hoje três
multiplicadores empilháveis sobre a mesma grandeza: a política global, o deslizador livre
`custom` até 2.0, e o fator por controle de `_controllers_to_rumble_scales`
(`src/hefesto_dualsense4unix/profiles/manager.py:1532-1580`, chamada em `:426`). A recomendação
verificada: `mult_final = min(mult_da_politica, teto_do_orcamento)` — `min` e não produto, porque
teto que multiplica um valor já amplificado a 2.0 não é teto, e porque `min` preserva o
denominador que `_controllers_to_rumble_scales` usa (o docstring de `manager.py:1541-1546`
explica por quê: o valor que chega ao backend já vem escalado pela política global, então o que a
unidade registra é RELATIVO). Escreva também a regra do orçamento em "Auto": o teto vira móvel e
a linha de teto na aba de origem NÃO pode exibir percentual — `manager.py:1556-1573` já resolveu
esse caso pulando com log `escala_de_vibracao_pulada_base_movel`, porque "prometer isso seria
pior do que não entregar".

**PASSO 3 — DAEMON, O ESTADO.** Em `src/hefesto_dualsense4unix/daemon/lifecycle.py`, dentro do
dataclass `DaemonConfig` (declarado em `:137`; os campos de rumble estão em `:251-252`),
acrescente o campo do orçamento com as mesmas quatro chaves e comentário datado no molde dos
vizinhos (`coop_enabled` em `:182` é o exemplo). NÃO invente uma quinta chave.

**PASSO 4 — DAEMON, O CÁLCULO.** Em `src/hefesto_dualsense4unix/core/rumble.py`, crie
`teto_do_orcamento(orcamento) -> float | None` (devolve `None` quando não há teto, incluindo
`"auto"` — teto móvel não é número) e aplique-a DENTRO de `_effective_mult` (`:51`),
imediatamente antes de cada `return` dos ramos de política fixa (`:96-99`) e de `custom`
(`:92-94`). Um só ponto, porque `_effective_mult` é o funil dos TRÊS caminhos de vibração do
produto: `apply_rumble_policy`
(`src/hefesto_dualsense4unix/daemon/ipc_rumble_policy.py:51-58`, que atende `rumble.set` e o
"Aplicar" do rodapé), `_game_rumble_mult`
(`src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:1129-1136`, o force-feedback do JOGO) e
`reassert_rumble` (`daemon/subsystems/rumble.py:263`, o tique de 200 ms do rumble fixado).
**NÃO escreva nada em `RumbleEngine`**: ele é lacuna declarada e não é instanciado em `src/`
(`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:692-707`).

**PASSO 5 — DAEMON, O MÉTODO IPC.** Espelhe `_handle_rumble_policy_set`
(`src/hefesto_dualsense4unix/daemon/ipc_handlers.py:4035-4056`): handler novo validando a chave
contra a mesma tupla, escrevendo no campo de `DaemonConfig` e devolvendo `{"status": "ok", ...}`.
Registre em `src/hefesto_dualsense4unix/daemon/ipc_server.py`, no dicionário `_handlers`
(`:106`), ao lado das cinco linhas de rumble (`:113-117`). Onde o pedido não puder ser atendido,
RECUSE NO CORPO — `{"status": "recusado", "motivo": <frase para pessoa>}` —, nunca erro
JSON-RPC: é a doutrina fixada por `d614d04f`, com o vocabulário em
`daemon/subsystems/rumble.py:369-388` e o exemplo de handler em `ipc_handlers.py:4726-4735`
(`coop.set`).

**PASSO 6 — GUI, A PONTE.** Em `src/hefesto_dualsense4unix/app/ipc_bridge.py`, espelhe
`rumble_set_checked` (`:432-443`): função que lê `resultado.get("status") == "recusado"` e
devolve o motivo por `_recusa_no_corpo` (`:425-430`). **NÃO use `_call_checked`** (`:286-315`):
ele só lê `CODE_INVALID_PARAMS` e deixaria a recusa no corpo chegar à tela como sucesso — foi
exatamente o defeito que `d614d04f` pagou.

**PASSO 7 — GUI, O SELETOR.** Na aba Configurações, monte o orçamento com `SegmentedSelector`
(`src/hefesto_dualsense4unix/app/widgets/segmented_selector.py`), nunca `GtkComboBox`.
`set_items([(chave, rótulo), ...])` (`:71`) com os rótulos vindos de `_POLICY_LABEL`, e
`set_tooltips({chave: dica})` (`:97-110`) para as dicas por opção do mockup. A tabela de cinco
linhas do mockup é um `Gtk.Grid`. Declare a página no glade como `GtkScrolledWindow` (padrão das
dez existentes) e identifique a aba por id do Glade, nunca por índice (molde: `id_da_pagina` em
`app/actions/home_actions.py:79`).

**PASSO 8 — GUI, O TETO VISÍVEL NA ABA DE ORIGEM** (a metade que a sprint chama de invariante).
Em `src/hefesto_dualsense4unix/gui/main.glade`, ao lado de `lightbar_brightness_scale`
(`:1299-1315`), acrescente um `GtkLabel id="lightbar_teto_label"` com `visible=False` e
`no-show-all=True` — molde literal: `rumble_policy_aviso` em `:1806-1813` (que também tem
`use-markup=True`). Em `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py`, escreva uma
função PURA `texto_do_teto_do_orcamento(state) -> str | None` no molde de
`texto_do_alcance_da_intensidade` (`app/actions/rumble_actions.py:194-273`): `None` quando o
campo não veio do daemon ou quando o orçamento é `auto` (teto móvel), texto quando há teto — e a
linha só aparece quando há texto. O docstring daquele molde dita a regra que o orçamento herda:
"Afirmar 'não alcança' com o campo ausente seria inventar um defeito — 'não sei' e 'não chega'
mandam caçar em lugares opostos". **O slider CONTINUA editável e sensível**: nada de
`set_sensitive(False)`, que é o caminho de `_sync_mouse_mode_gate`
(`src/hefesto_dualsense4unix/app/actions/mouse_actions.py:97`) e esconde a causa. Repita o mesmo
par rótulo mais função na aba Rumble, ao lado dos quatro botões de política.

**PASSO 9 — GIROSCÓPIO E MICROFONE: só depois de decidir se ficam.**
O giroscópio: **não existe ajuste de taxa em lugar nenhum de `src/`** (grep por `gyro_rate`,
`gyro_hz`, `sample_rate`, `report_rate` volta vazio; `profiles/schema.py` não tem campo de Hz). O
único teto real é `MOTION_EMIT_MAX_HZ = 250.0`
(`src/hefesto_dualsense4unix/core/physical_report_reader.py:246`), o cap de emissão ao gamepad
virtual, que vira `self._min_interval` no construtor (`:549`, cálculo em `:555`) e **não tem
setter ao vivo**. Se ficar, entra passando `max_hz=` nos dois únicos call sites
(`daemon/subsystems/gamepad.py:1726` e `daemon/subsystems/coop.py:1118`), a constante NÃO muda
(ou `tests/unit/test_teto_de_emissao.py:107-134` reprova), e a tela diz que o teto vale a partir
do próximo início do controle virtual. A linha "Vem de: No jogo" do mockup (`:414`) está errada
nos dois casos: a aba "No jogo" MEDE o giroscópio, não o configura.
O microfone por rádio: **não tem tela nenhuma.** É o subsystem
`src/hefesto_dualsense4unix/daemon/subsystems/bt_mic.py`, ligado por opt-in explícito (env
`HEFESTO_DUALSENSE4UNIX_BT_MIC=1` ou `config.bt_mic_enabled` lido por `getattr`, `:79` e
`:23-25` — o campo pode nem existir no `DaemonConfig`). Grep por `bt_mic` em `app/` e no
`main.glade` só acha um comentário (`app/widgets/controller_card.py:540-541`). Troque
"Vem de: Emulação" (mockup `:413`) por "Vem de: nenhuma aba ainda", ou corte a linha. Nota a
favor de mantê-la depois: é a ÚNICA linha da tabela com custo de recurso MEDIDO — `bt_mic.py:15-22`
registra que com o mic ligado os reports de input caem de ~260 para ~170/s e a mesma banda passa
a carregar ~106 quadros de áudio/s.

**PASSO 10 — DOCUMENTAÇÃO GERADA.** Rode `python3 scripts/gerar-contrato-ipc.py` (sem `--check`)
para regravar o bloco de métodos em `docs/protocol/ipc-unix-socket.md` a partir do `_handlers`. O
job `referencias-docs` (`ci.yml:111`) roda `--check`. Não edite a tabela à mão — o script existe
porque o número escrito à mão já saiu 15, 17, 18 e 14 em levantamentos diferentes
(`scripts/gerar-contrato-ipc.py:14-21`).

#### Prova de trabalho

```sh
# BASELINE, ANTES DE MEXER — resultados medidos hoje:
.venv/bin/python -m pytest tests/unit/test_politica_de_vibracao_a_escada_que_amplifica.py \
  tests/unit/test_teto_de_emissao.py tests/unit/test_rumble_mult_um_dono.py -q   # 39 passed
xvfb-run -a .venv/bin/python -m pytest tests/unit/test_layout_orcamento_altura.py -q  # 7 passed
```

**TESTE NOVO 1 — A CRIAR: tests/unit/test_orcamento_e_teto_nao_troca.py.** Molde de construção do
`DaemonConfig` em `tests/unit/test_politica_de_vibracao_a_escada_que_amplifica.py:56-60`. Assere:
(a) com orçamento `balanceado`, o mult de cada política é IDÊNTICO ao de hoje — derivado de
`RUMBLE_POLICY_MULT`, nunca escrito à mão; (b) com orçamento `economia` e política `max`, o mult
sai menor ou igual a `RUMBLE_POLICY_MULT["economia"]`; (c) voltar o orçamento para `balanceado`
devolve exatamente `RUMBLE_POLICY_MULT["max"]` — nenhum ajuste da pessoa foi apagado, que é a
prova de "teto, não troca"; (d) com `custom_mult = 2.0` e orçamento `economia`, o mult sai menor
ou igual a 0.3. **MORDIDA declarada no docstring: trocar `min` por produto faz (c) falhar.**

**TESTE NOVO 2 — A CRIAR: tests/unit/test_orcamento_dono_unico_do_valor_efetivo.py.** (a) a função
de texto da aba Lightbar devolve `None` quando o campo do orçamento não veio no `state`; (b)
devolve `None` com orçamento `auto`; (c) devolve texto contendo o percentual quando há teto; (d)
nenhum módulo de `app/` recalcula o mult — o grep por `RUMBLE_POLICY_MULT[` em
`src/hefesto_dualsense4unix/app/` só pode achar o `_POLICY_MULT` derivado de
`rumble_actions.py:65-68`.

**TESTE NOVO 3 — A CRIAR: tests/unit/test_orcamento_recusa_com_motivo.py.** O handler devolve
`{"status": "recusado", "motivo": ...}` (não `raise ValueError`) e a ponte traduz em
`(False, motivo)`. Molde: `tests/unit/test_nativo_rumble_01_a_recusa_chega_na_tela.py` e
`tests/unit/test_nativo_rumble_01_a_recusa_com_motivo.py`. Se tocar interface, `exigir_gi_real()`
no topo.

```sh
python3 scripts/validar-acentuacao.py --all
python3 scripts/validar-glifos.py --all
python3 scripts/validar-referencias-docs.py --all
python3 scripts/validar-palavra-de-tela.py
python3 scripts/gerar-contrato-ipc.py --check
.venv/bin/python -m pytest tests/unit -q     # não deixe a coleta cair abaixo do piso 8100
.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
.venv/bin/python -m ruff check src/ tests/ && .venv/bin/python -m mypy src/hefesto_dualsense4unix
```

**PROVA VISUAL** (exigida pelo `.github/PULL_REQUEST_TEMPLATE.md` para escopo GUI): captura PNG
da aba Configurações com a seção Orçamento e da aba Lightbar com a linha de teto acesa, mais
`sha256sum` de cada arquivo e descrição de 3 a 5 linhas.

#### Armadilhas

- **GRAVAR O RÓTULO EM VEZ DA CHAVE.** `RumbleConfig` tem `extra="forbid"`
  (`profiles/schema.py:333`) e `policy` aceita `"max"`, nunca `"Máximo"` (`:336`). Falha na
  PRÓXIMA carga, com o perfil inteiro recusado.
- **ESCREVER O NÚMERO DA ESCADA À MÃO.** HARM-19, contado em `profiles/schema.py:76-80`: a faixa
  valeu 2.0 no schema, 1.0 no handler e 200 % no slider ao mesmo tempo, e de 101 % em diante a
  usuária levava erro de validação que a aba reportava como "daemon offline?".
  `tests/unit/test_rumble_mult_um_dono.py` reprova quem reescrever o número.
- **IMPLEMENTAR O TETO NO `RumbleEngine`.** É o lugar que parece certo e é código morto. A lacuna
  está declarada com data em `portao_a_casa_sabe_e_o_produto_nao_faz.py:692-707`, inclusive
  acusando dois comentários da árvore de mentirem sobre ele (entre eles
  `daemon/ipc_rumble_policy.py:5`).
- **TETO QUE MULTIPLICA EM VEZ DE LIMITAR.** 0.3 sobre um valor já multiplicado por 2.0 entrega
  0.6 — mais forte que o Economia que ele prometeu.
- **QUATRO MULTIPLICADORES EMPILHADOS SEM NINGUÉM SOMAR.** Um orçamento aplicado fora de
  `_effective_mult` muda o denominador sem os overrides por controle saberem, e a peça que pediu
  "max" fica mais fraca que a que não opinou (`profiles/manager.py:1532`, `set_rumble_scales` em
  `core/backend_pydualsense.py:3414`).
- **ORÇAMENTO EM "AUTO" PROMETENDO UM PERCENTUAL.** Em Auto o teto muda com a bateria a cada
  tique. A casa já enfrentou o caso e escolheu não prometer (`manager.py:1556-1573`).
- **"O CONTROLE NO CABO JOGA EM MÁXIMO" REVERTE UMA CURA MEDIDA.** A decisão de 11/08/2026 é que
  o Auto NUNCA amplifica: está no código (`core/rumble.py:73-86`), no rótulo da tela
  (`main.glade:1763-1775`) e no tooltip do botão (`main.glade:1678`). Implementar a frase sem
  tocar os três deixa a tela prometendo 100 % enquanto o daemon entrega 150 % — o defeito exato
  que `7cd15e8d` e `d614d04f` pagaram.
- **O AUTO DECIDE PELA BATERIA DE UM CONTROLE SÓ.** `apply_rumble_policy` lê
  `store.snapshot().controller` (`daemon/ipc_rumble_policy.py:32-42`, com fallback 50) e o
  `StateStore` guarda um único `ControllerState` (`daemon/state_store.py:67`, `:718`); o espelho
  em `gamepad.py:1122-1128` faz o mesmo. Numa mesa de cinco controles — que é o caso que o mockup
  desenha — o orçamento "da mesa" decide olhando um.
- **O SLIDER DA LIGHTBAR INSENSÍVEL.** Parece limpo e contraria `d614d04f`, que com as três
  opções na mesa escolheu recusar no daemon porque "impedir o clique contraria a regra de que a
  vontade da GUI prevalece".
- **LER A RECUSA COM `_call_checked`.** A tela mostra sucesso para um pedido negado.
- **MEXER NO TETO DO GIROSCÓPIO PELA CONSTANTE.** O orçamento do `/dev/uhid` tem margem ZERO — 4
  vpads vezes 250 Hz igual a 1000 writes/s, aferido em `tests/unit/test_teto_de_emissao.py:117-125`,
  com `7cd15e8d` escrevendo "Margem zero, e ela sabia disso ao escolher".
- **MEDIR GEOMETRIA SEM DISPLAY OU SEM AS FONTES.** Ver 2.2. E o portão de altura já foi cego uma
  vez (`test_layout_orcamento_altura.py:268-292`).
- **ACRESCENTAR TEXTO EXPLICATIVO NA TELA.** A altura já é o gargalo: o mockup tem 1729px. Texto
  novo entra como dica via `SegmentedSelector.set_tooltips`, e a regra de [TOOLTIPS.md](TOOLTIPS.md)
  vale — se a opção não faz sentido sem a dica, o rótulo está errado.
- **JARGÃO EM RÓTULO NOVO DO GLADE.** Texto montado em Python passa livre, o que é pior, não
  melhor: os rótulos do orçamento só ficam protegidos se forem declarativos.
- **COMMITAR SEM CONFERIR O QUE FICOU GRAVADO.** Ver 2.4.

---

### CONFIG-06 — controles que não são DualSense

Arquivo da sprint:
[CONFIG-06-controles-que-nao-sao-dualsense.md](CONFIG-06-controles-que-nao-sao-dualsense.md)

> **Correção de numeração, antes de tudo.** D-A2, o INDICE e a própria sprint falam em "seção 4"
> para os controles externos e "seção 5" para a janela. O mockup numera **0 a 4**: `:196`
> "0. SAÚDE", `:216` "1. OS CONTROLES", `:325` "2. A MESA", `:399` "3. Orçamento", `:422`
> "4. A janela". **CONFIG-06 é a seção 1.** CONFIG-03 e CONFIG-07 continuam escrevendo "seção 5"
> para a janela; as duas convenções convivem nos relatórios e ninguém as unificou.

#### Roteiro

**PASSO 0 — DECIDIR ANTES DE CODAR, e é uma decisão só, com quatro respostas.** Abra
`docs/protocol/externos-firmware-e-modos.md:222-228` e leia a tabela do que o produto diz em cada
modo. Ela mostra que o modo **É** deduzido. Para CADA linha da tabela de entrega, responda por
escrito na própria sprint:
**(1) MODO** — vira exibição derivada (estender `input_mode`,
`src/hefesto_dualsense4unix/app/actions/external_controllers.py:230`, de dois estados para
quatro) ou declaração? Os quatro modos estão canonizados em
`docs/protocol/externos-firmware-e-modos.md:146-149` com combo, VID:PID por cabo, VID:PID por
rádio e driver, e a dedução tem grau ALTA em cinco dos sete pares modo por transporte.
Declaração colide com a salvaguarda de D-A1 e com o fato de o MAC mudar com o modo.
**(2) RÓTULO DOS BOTÕES** — fica; é preferência, o produto não mede. Não confunda com
`button_labels_for` (`external_controllers.py:186`), que monta o texto do BOTÃO DO SELETOR
("Nintendo 3 · cabo") e não o desenho A/B/X/Y.
**(3) TRATAR COMO MODELO CONHECIDO** — é MÁSCARA (`ExternalMaskRegistry.set_mask`,
`src/hefesto_dualsense4unix/daemon/subsystems/external_mask.py:320`, pronta e sem chamador de
produção) ou é conserto de IDENTIDADE (`friendly_type`/`brand_of`, `external_controllers.py:88`
e `:108`, que hoje erram em três casos MEDIDOS,
`docs/protocol/externos-firmware-e-modos.md:230-246`)? São coisas diferentes.
**(4) COR DO PLÁSTICO** — persiste em disco (reabre a D-16 de ONDE-A-COR-MORA-01, que recusou
"um arquivo por endereço" e que ela vetou em 12/08) ou vale só na sessão (recomendação (b)
daquela página)?
Sem estas quatro respostas você vai construir formulário para fato medido, que é o defeito que a
leva inteira existe para evitar.

**PASSO 1 — Rodar a linha de base e guardá-la.**
`.venv/bin/python -m pytest tests/unit/ -k "external or mascara" -q` sai hoje
`1 failed, 370 passed, 1 skipped, 10195 deselected, 1 xfailed`. O reprovado é
`tests/unit/test_docs_mac_anonimato.py::test_nenhum_mac_real_completo_sem_mascara_no_repo`,
acusando o arquivo **untracked** `GUIA-RADIO-DA-SALA.md` — e **não é seu**. Não conserte esse
arquivo dentro desta sprint; é dívida de CONFIG-08.

**PASSO 2 — A NOTA DATADA, primeiro**, porque é o "Rastro obrigatório" e não depende de mais
nada. Em `src/hefesto_dualsense4unix/app/actions/external_controllers.py`, o docstring de módulo
vai de `:1` a `:14`; a fala do escopo ("só uma aba pra ver como os controles aparecem, não uma
super central") está em `:9-10` e o parágrafo termina em `:13`. INSIRA depois de `:13` e antes do
fecho de `:14`. NÃO apague as linhas 9-13. O molde literal a copiar é
`src/hefesto_dualsense4unix/core/external_leds.py:337-347` — bloco `.. warning::` abrindo com
uma NOTA DATADA em negrito, dizendo o que mudou e quem decidiu. Conteúdo: em 21/08/2026 o escopo
foi reaberto por decisão dela (D-A2), contra a recomendação, e a decisão está em
[DECISOES-ABERTAS.md](DECISOES-ABERTAS.md).

> **Contradição menor registrada.** CONFIG-03 e CONFIG-06 dizem que a fala está em
> `external_controllers.py:9-10`; CONFIG-08 corrige para `:9-13`. Os três concordam que `:11-14`
> (o endereço que a sprint escreve) está errado.

**PASSO 3 — A lógica PURA, no arquivo que já é dela.** Ainda em `external_controllers.py`,
acrescente ao lado das existentes (o arquivo inteiro é puro, 351 linhas, testável sem GTK):
`declaracoes_do_aparelho(entry) -> list[tuple[str, str, str | None]]` devolvendo chave, rótulo e
valor declarado ou `None`; e `cores_do_plastico_items() -> list[tuple[str, str]]` devolvendo os
pares (id, rótulo) das seis cores do mockup. Os ids e nomes oficiais saem de
`scripts/ensaios/cor_do_plastico.py`, códigos `00` a `05`: 00 White/Branco, 01 Midnight
Black/Preto, 02 Cosmic Red/Vermelho, 03 Nova Pink/Rosa, 04 Galactic Purple/Roxo, 05 Starlight
Blue/Azul. NÃO copie a tabela — reescreva com o comentário dizendo de onde veio, porque as seis
são um recorte do mockup, não a tabela oficial.

> **Contradição registrada** sobre o tamanho dessa tabela. CONFIG-01 diz que o dicionário `CORES`
> abre em `cor_do_plastico.py:158` e tem "16+ nomes oficiais Sony (`00 White` até
> `12 Chroma Pearl`, `30`, `Z1` a `Z3`)", com as seis do mockup em `:159-164` e `:165` já sendo
> `"06": "Grey Camouflage"`. CONFIG-06 diz `:158-170`, "21 nomes", e cita "Volcanic Red" como
> código `07` em `:167`. Abra o arquivo e conte antes de escrever qualquer número.

**PASSO 4 — O card, em GTK, num arquivo novo — A CRIAR:
src/hefesto_dualsense4unix/app/widgets/external_card.py.** Molde de estrutura:
`src/hefesto_dualsense4unix/app/widgets/controller_card.py` (o padrão real mais stub por
`_GTK_DISPONIVEL`, `:2028-2053` — copie esse bloco de resolução condicional, é obrigatório para o
teste coletar sem PyGObject). Classe `ExternalCard(Gtk.Frame)` com
`add_class('hefesto-dualsense4unix-card')` (a classe CSS existe em
`src/hefesto_dualsense4unix/gui/theme.css:758`). Cada linha de declaração usa `SegmentedSelector`
(`src/hefesto_dualsense4unix/app/widgets/segmented_selector.py`) — NUNCA `GtkComboBox`. A
montagem exata a copiar é `src/hefesto_dualsense4unix/app/gui_dialogs.py:772-802`, que já faz
rótulo mais seletor mais subtítulo. Para "nasce em não sei": `seletor.limpar_ativo()`
(`segmented_selector.py:115`) deixa o seletor SEM botão marcado e NÃO emite `changed`. Para o
nome oficial de fábrica na dica de cada cor: `seletor.set_tooltips({id: nome_oficial})` (`:97`).
Para as seis cores mais "Outra" (sete itens), use `SegmentedSelector(wrap=True)`: ele monta grade
de 3 colunas FIXAS (`_WRAP_COLUNAS = 3`, `:33`), o que dá três linhas.

**PASSO 5 — A altura invariante, que é três coisas e não uma.**
(a) O container dos cards é `Gtk.Grid` com número FIXO de colunas — **nunca `Gtk.FlowBox`**; o
motivo medido está em `segmented_selector.py:216-231` (o FlowBox reportou 606px empilhado e virou
o piso da aba).
(b) Cada card recebe `set_valign(Gtk.Align.FILL)` e `set_vexpand(True)` — é ISTO que iguala a
altura de cards vizinhos, não `row_homogeneous`. O único grid de cards de hoje faz o oposto
(`src/hefesto_dualsense4unix/app/actions/status_actions.py:1307`, `set_valign(Gtk.Align.START)`),
então não copie de lá.
(c) Dentro do card, antes da última linha ("Jogador"), empacote um `Gtk.Box()` vazio com
`set_vexpand(True)` — é o equivalente do `margin-top:auto` do mockup
(`aba-configuracoes.html:94`).
Só se os cinco cards quebrarem em duas linhas é que `grade.set_row_homogeneous(True)` entra.
**`row_homogeneous=True` não faz o que a sprint diz que faz**, e não tem um único precedente na
árvore: grep por `row_homogeneous` e `set_row_homogeneous` em `src/` e `tests/` devolve ZERO.

**PASSO 6 — A linha "Jogador" fala com o daemon por caminho que já existe.** Chame
`identity_number_set` de `src/hefesto_dualsense4unix/app/ipc_bridge.py:549` com a chave externa e
o número; o handler é `daemon/ipc_handlers.py:1513`, recebe `external_registry` (`:1590`) e a
fila de numeração é ÚNICA entre DualSense e externos (`_set_number_locked`, `:1680`). O
`_norm_uniq` de `:1580` já cai no valor cru quando a identidade é volátil. Copie a disciplina de
`status_actions.py:1854-1897`, inteira: guarda `_numero_updating` para a marcação programática
não reenviar o pedido a cada tique; só o botão que ficou ATIVO age; e NADA é pintado na janela
por conta própria — quem repinta é o próximo `state_full` (o comentário de `:1866-1872` explica
que pintar antes cria a terceira verdade que PLAYER-01 existiu para matar).

**PASSO 7 — Registrar a seção na aba, pelo id do Glade e nunca por índice.** A página nova de
CONFIG-01 nasce `GtkScrolledWindow` no `main.glade` (o notebook está em `:218`). Identificação
por id: `app/actions/home_actions.py:79` (`id_da_pagina`) e `:109` (`id_da_pagina_corrente`). Se
a seção precisar reconciliar ao ser exibida, acrescente a entrada em `_REFRESH_POR_ABA`
(`app/app.py:920`) — e leia a contradição registrada em CONFIG-02, PASSO 7. O
`install_config_tab()` entra na lista de `install_*_tab` de `app/app.py:1171-1179` **E TAMBÉM** na
segunda lista em `:1435-1443`.

**PASSO 8 — Se e só se o PASSO 0 escolheu MÁSCARA para a linha 3:** o lado de escrita não existe.
Você precisa de (a) um método IPC novo em `daemon/ipc_server.py` mais handler em
`daemon/ipc_handlers.py` chamando `set_mask` (`external_mask.py:320`) ou `clear_mask` (`:366`)
para "como ele mesmo" — que é AUSÊNCIA, nunca um terceiro valor (`:209-215`); (b) o par em
`app/ipc_bridge.py`, no molde de `identity_number_set` (`:549`); (c) regenerar o contrato com
`scripts/gerar-contrato-ipc.py`. Valores válidos são só os de `mascaras_validas()`
(`external_mask.py:201`), hoje `{'dualsense','xbox'}`, derivados de
`src/hefesto_dualsense4unix/integrations/uinput_gamepad.py` `FLAVORS` (`:115-126`) — não escreva
uma segunda lista.

**PASSO 9 — A foto.** `scripts/gui-captura/retratar_abas.py:879-881` no-opa `_maybe_fetch_externals`
**de propósito** — o comentário literal é que o de produção pergunta ao daemon VIVO e "aqui,
nunca", e `:913-918` explica que sem isso a garantia de privacidade do cabeçalho quebraria no
primeiro `--mesa-cheia`, calada. Para o aceite visual existir, escreva a injeção por fixture no
molde de `_injetar_cards_da_mesa_cheia` (`:886-940`): um fixture novo de inventário externo ao
lado de `tests/fixtures/state_full_quatro_controles.json`, e um host que devolve esse fixture.
Mantenha o no-op do caminho de produção.

#### Prova de trabalho

```sh
# LINHA DE BASE, antes de tocar em qualquer arquivo:
.venv/bin/python -m pytest tests/unit/ -k "external or mascara" -q
#   hoje: 1 failed, 370 passed, 1 skipped, 10195 deselected, 1 xfailed  (o failed NÃO é seu)
.venv/bin/python -m pytest tests/unit/test_external_controllers.py \
  tests/unit/test_external_mask.py tests/unit/test_external_leds.py -q   # hoje: 95 passed
```

**TESTE NOVO 1, puro — A CRIAR: tests/unit/test_config_06_declaracao_nasce_em_nao_sei.py.**
Assere que `declaracoes_do_aparelho(entry)` devolve `None` no valor de TODO campo quando não há
declaração gravada, para três entradas (8BitDo em modo Switch, Pro genuíno, aparelho de VID
desconhecido); e que nenhum default é escolhido — o teste tem de reprovar se alguém trocar `None`
por `'xbox'`. Precedente do porquê: `external_mask.py:145-155`, o `or "xbox"` do editor de perfis
que apagava giroscópio e touchpad sem ninguém pedir.

**TESTE NOVO 2, geometria — A CRIAR: tests/unit/test_config_06_cards_tem_a_mesma_altura.py**,
começando com `exigir_gi_real()` (`tests/conftest.py:210`) na primeira linha do módulo. Assere:
montados dois cards de conteúdo diferente (um DualSense de duas linhas, um 8BitDo de quatro) no
mesmo `Gtk.Grid`, as alturas alocadas são iguais depois de `show_all()` e do assentamento do laço
de eventos. Só vale medido com as duas fontes instaladas.

```sh
.venv/bin/python -m pytest tests/unit/test_layout_orcamento_altura.py -q
python3 scripts/validar-palavra-de-tela.py --all
python3 scripts/validar-acentuacao.py --all
.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
python3 scripts/gerar-contrato-ipc.py --check     # só se o PASSO 8 for feito
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  .venv/bin/python scripts/gui-captura/retratar_abas.py /tmp/config06 --mesa-cheia
```

Se você ligar `short_button_label` (hoje declarado como lacuna em
`portao_a_casa_sabe_e_o_produto_nao_faz.py:801-808`), APAGUE a entrada — o portão também reprova
entrada de lacuna que envelheceu.

**MEDIÇÃO 3 (D-input), com o controle no modo a investigar, sem sudo** — o comando está escrito
em `docs/protocol/externos-firmware-e-modos.md:336-345` e usa `discover_external_gamepads` de
`src/hefesto_dualsense4unix/core/evdev_reader.py`. Se o aparelho não aparecer, a previsão de grau
MÉDIA está confirmada (o descritor do 8BitDo no cabo declara `Usage (Joystick)`, e
`discover_external_gamepads` só enxerga evdev com `BTN_GAMEPAD`/`BTN_SOUTH`,
`evdev_reader.py:628`) e a seção precisa do estado "não estou vendo nada e sei por quê". Se
aparecer, o `pid` da saída responde de graça a medição 1: `6001` é SN30 Pro e `6002` é SN30 Pro+
(`docs/protocol/externos-firmware-e-modos.md:506`).

#### Armadilhas

- **O MAC MUDA COM O MODO, e é medido.** `docs/usage/troubleshooting-8bitdo.md:130-143`: o mesmo
  8BitDo usa endereços Bluetooth diferentes em cada modo; no teste dela ele entrou no slot 5
  porque a identidade do modo Switch ainda ocupava o 4. Uma declaração gravada por identidade
  fica ÓRFÃ no instante em que a pessoa troca o modo que a declaração descreve. E
  `external_mask.py:130-135` diz que o lookup por grupo está "deliberadamente fora deste
  desenho". Escreva qual das duas saídas vale antes da primeira linha de código.
- **A LUZ DOS EXTERNOS ESTÁ CALADA POR DECISÃO, E VOLTAR CUSTA.**
  `EXTERNAL_PLAYER_LED_ENABLED = False` em
  `src/hefesto_dualsense4unix/daemon/subsystems/external_identity.py:194`, com a condição de
  volta em `:155-194` e a frase "Não é quando alguém achar que já dá". Custo medido de ligar: 348
  recusas de subcomando em 06-07/08 caíram para ZERO às 15:27:48 de 07/08 quando calaram.
- **O CAMINHO `ds4` NÃO PASSA PELO PORTÃO DA LUZ.**
  `docs/protocol/externos-referencia-canonica.md:1273-1276`: a escrita de `write_lightbar_slot`
  (`src/hefesto_dualsense4unix/core/external_leds.py:327-373`) é no caminho `ds4`, que não
  consulta o portão. A medição 4 é uma escrita no plástico dela. Decisão dela de 07/08 (resposta
  23): "preparar, e rodar quando ele estiver ligado". Prepare; não rode sem ela na sala.
- **O nó azul continua tratado como bit "+5" no código** (`core/external_leds.py:43-58`, R-25) e
  a canônica registra isso como defeito conhecido
  (`docs/protocol/externos-referencia-canonica.md:1123`). Não conserte de passagem: tem sprint
  própria.
- **UM PORTÃO VERDE QUE OLHA PARA O LUGAR ERRADO ENCERRA A BUSCA.**
  `tests/unit/test_layout_orcamento_altura.py:268-292` conta que a aba Rumble foi engordada em
  900px e os SETE testes continuaram verdes. Meça o CONTEÚDO, nunca o scroller.
- **MEDIR GEOMETRIA SEM AS FONTES CERTAS.** Ver 2.2. E `gtk-real` é job PRÓPRIO com
  `HEFESTO_EXIGE_GTK_REAL=1`.
- **`Gtk.FlowBox` PARA A GRADE DE CARDS É A ARMADILHA JÁ PAGA.** Vale para os cards e para os
  sete botões de cor.
- **EMPILHA-01 É DECISÃO DELA E DIZ O OPOSTO DO MOCKUP.** `status_actions.py:1278-1291`
  (02/08/2026): "os dois blocos não deveriam estar lado a lado mas um em cima do outro de forma
  que o scroll surgisse pra comportar os diferentes controles", e o código faz `colunas = 1`. O
  mockup usa `grade` de `repeat(auto-fit, minmax(212px,1fr))` (`aba-configuracoes.html:89-90`) —
  cinco cards lado a lado. **A invariante "a altura dos cards é invariante" só existe PORQUE eles
  são lado a lado.** Se EMPILHA-01 vale nesta aba, a seção inteira fica sem objeto; se não vale,
  é uma segunda decisão sobre o mesmo gesto e precisa ser registrada como tal.
- **DUAS DESCRIÇÕES DO MESMO FATO NA MESMA JANELA.** A ficha do controle externo já mostra o modo
  num `SegmentedSelector` INSENSÍVEL, com o tooltip "Só leitura: mostra o modo em que o controle
  está agora. A troca não é por software" (`external_controllers.py:246-249`, montado em
  `gui_dialogs.py:760` e `:772-802`). Um segmentado EDITÁVEL do mesmo modo na aba faz a janela
  dizer duas coisas opostas. Escolha qual sobrevive e apague o outro no mesmo commit.
- **GRAVAR A COR DO PLÁSTICO EM DISCO É LITERALMENTE O QUE FOI VETADO EM 12/08.** Ver PASSO 0,
  item 4.
- **O MOCKUP CONTRARIA A RECOMENDAÇÃO DE COR DO ANEL.** A dica do mockup diz "O anel roxo por
  dentro marca qual está selecionado" (`aba-configuracoes.html:217`); ONDE-A-COR-MORA-01 recomenda
  o rosa da marca, "porque o roxo colide com um dos seus quatro controles e o rosa não colide com
  nenhum DualSense que exista". E a restrição 6 de CONFIG-01 reserva o rosa para marca e aba
  ativa — então esta é uma exceção a registrar, não a inventar em silêncio.
- **O CAMPO LIVRE "Outra" DO MOCKUP PROPÕE DIGITAR UM NOME QUE JÁ EXISTE NA TABELA.** O card do
  Jogador 5 tem um campo com "Volcanic Red" (`aba-configuracoes.html:314`), que é um dos códigos
  da tabela oficial. "Outra" deve abrir os nomes restantes, não um campo de texto que convida a
  redigitar o que a casa já sabe.
- **A CAPTURA NÃO PROVA A SPRINT, E FALHA CALADA.** Ver PASSO 9.
- **O AMBIENTE MENTE DE DUAS FORMAS.** Ver 2.2 e 2.3. Nenhum dos dois é defeito seu — mas os dois
  fazem você perder meia hora achando que é.
- **OS HOOKS LOCAIS NÃO RODAM NESTA MÁQUINA.** Ver 2.4.

---

### CONFIG-07 — a janela

Arquivo da sprint: [CONFIG-07-a-janela.md](CONFIG-07-a-janela.md)

#### Roteiro

**1. Confirme onde você está.** `git rev-parse --short HEAD` tem de dar `70d28762` ou descendente
e `git branch --show-current` tem de dar `dev`. Os hashes `d6b9396` e `911d099` citados na leva
**não existem em `dev`** — `git merge-base --is-ancestor` reprova nos dois. Os equivalentes são
`b1093087` ("a janela nunca nasce maior do que a tela comporta", cura em
`src/hefesto_dualsense4unix/app/app.py:1230 _caber_na_area_util`, chamada em `:1189`) e
`78721e85` ("o ícone some da barra quando o terminal empresta o cache do snap", cura em
`src/hefesto_dualsense4unix/app/main.py`, `_sanear_loaders_do_gdk_pixbuf`).

**2. Verifique o pré-requisito.**
`grep -n "tab_config_box" src/hefesto_dualsense4unix/gui/main.glade` tem de devolver pelo menos
uma linha. Molde da página, se precisar conferir: `main.glade:3503-3512`
(`scroll_tab_navegacao_dsx`) e o rótulo da tira em `:3951-3953`. Se voltar vazio, pare.

**3. Declare a seção 5 NO GLADE, não em Python — é a decisão de forma que governa toda a
sprint.** Dois motivos medidos: (a) `tests/unit/test_layout_orcamento_altura.py:237-253
_montar()` carrega só o glade e não chama nenhum `install_*_tab`, então conteúdo de código não é
medido nem por orçamento de altura nem por largura; (b) `scripts/validar-palavra-de-tela.py:14-18`
declara alcance estreito — só o `main.glade`. Molde a copiar para as fileiras de botões:
`main.glade:1641-1686` (a fileira de política do Rumble): `GtkBox` horizontal, `spacing=6`, **SEM
`homogeneous`** (com o motivo escrito em `:1645-1650`), um `GtkToggleButton` por opção com
`label`, `tooltip-text` e `signal toggled`; handlers em
`src/hefesto_dualsense4unix/app/actions/rumble_actions.py:385-410`. **Não use `SegmentedSelector`
aqui**: ele é widget Python injetado em slot (`scripts/gui-captura/retratar_abas.py:748-757`) e
devolve os dois pontos cegos. A proibição de CONFIG-01 é ao `GtkComboBox`; um grupo de
`GtkToggleButton` declarativo a cumpre.

**4. Escreva os widgets da seção 5 dentro de `tab_config_box`, nesta ordem** (a do mockup,
`aba-configuracoes.html:422-450`): um `GtkLabel` "A janela" com a classe de estilo
`hefesto-titulo-secao` (`gui/theme.css:114`); a fileira "Tamanho do texto:" com
`config_escala_compacto` / `config_escala_normal` / `config_escala_grande` (rótulos `Compacto`,
`Normal`, `Grande`); a fileira "Ambiente:" com `config_ambiente_cosmic` / `config_ambiente_gnome`
/ `config_ambiente_outro`, e o `tooltip-text` LITERAL de `TOOLTIPS.md:111` ("O ícone na barra do
sistema depende do ambiente. No COSMIC aparece sozinho; no GNOME precisa de uma extensão
instalada."); um `GtkLabel id="config_ambiente_detectado"` com `xalign=0`, `wrap=True`,
`max-width-chars=84` e `dim-label`, que o código preenche com "Detectado: ..."; um
`GtkLabel id="config_bandeja_ajuda"` com as mesmas propriedades, para a instrução do GNOME. Tudo
com `translatable="yes"` e rótulo começando em maiúscula.

**5. `src/hefesto_dualsense4unix/app/theme.py` — os três degraus.** Ao lado de `ESCALA_PADRAO`
(`:46`, vale 3) e `ESCALA_MAXIMA` (`:50`, vale 8), acrescente um mapa de degraus
(compacto 0, normal `ESCALA_PADRAO`, grande 6) e `degrau_da_escala(delta) -> str`, que devolve o
degrau cujo valor está mais perto de `delta` — para a tela nascer marcando o que está valendo,
sem inventar um quarto estado. A gravação, no handler, é `set_pref` de
`src/hefesto_dualsense4unix/app/gui_prefs.py:63` com a `CHAVE_ESCALA` de `theme.py:39`.
**NÃO chame `apply_theme` de novo**: ele COMPÕE — `theme.py:150-156` soma ao `gtk-font-name` já
posto e `:177` acrescenta provider sem nunca chamar `remove_provider_for_screen`; e
`escala_fonte()` (`:69`) devolve o cache de `_escala_aplicada` (`:66`, `:76-78`). Escolha
explicitamente: **(a)** gravar e dizer na tela que vale ao reabrir o Hefesto — é o comportamento
que o repositório já documenta
(`docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md:481-486`: a chave
"só é alcançável editando JSON à mão, com reinício") e cabe nesta sprint; ou **(b)** escrever um
`reaplicar_escala(window, delta)` que guarde o provider num global do módulo, chame
`Gtk.StyleContext.remove_provider_for_screen` antes de adicionar o novo, reponha o
`gtk-font-name` ORIGINAL antes de somar e zere `_escala_aplicada` — isso é sprint própria.

**6. Crie A CRIAR: src/hefesto_dualsense4unix/app/ambiente.py** (~60 linhas). Hoje não há leitor
público: os únicos leitores de `XDG_CURRENT_DESKTOP` são `app/tray.py:90 _desktop_is_cosmic()`,
`app/tray.py:100 _painel_recolore_simbolico()`, `app/main.py:33-38` (que só decide `GDK_BACKEND`)
e `src/hefesto_dualsense4unix/integrations/window_backends/wayland_portal.py:149`. Três funções:
`ambiente_lido()` devolve a variável crua, string vazia inclusive; `ambiente_normalizado(bruto)`
devolve `"cosmic"`, `"gnome"` ou `"outro"`, casando por substring sem diferenciar maiúscula sobre
`XDG_CURRENT_DESKTOP` mais `XDG_SESSION_DESKTOP` — é o que `app/tray.py:92-97` já faz, copie a
concatenação; `ambiente_efetivo()` prefere a correção manual gravada em `gui_preferences.json`
(chave nova) e cai no normalizado quando ela não existe. **A correção vai para `gui_prefs`, NÃO
para `maquina.json`**: é preferência da janela, o daemon nunca precisa dela, e assim CONFIG-07
continua dependendo só de CONFIG-01. `app/gui_prefs.py:24-26` tem hoje uma única chave de padrão
(`advanced_editor`). Cada função nasce com chamador na aba.

**7. Na aba, sonde a bandeja FORA da thread do GTK.** Chame
`statusnotifierwatcher_available()` de
`src/hefesto_dualsense4unix/integrations/desktop_notifications.py:169-206` — não reimplemente
D-Bus; ela já é consumida em produção (`app/app.py:502`, `app/tray.py:275`) e o docstring diz que
em COSMIC quem reivindica é o `cosmic-applet-status-area` e em GNOME é o `gnome-shell` com a
extensão. Ela é síncrona com `_DBUS_TIMEOUT_SECONDS = 2.0` (`:34`), então despache por
`run_in_thread` (`src/hefesto_dualsense4unix/app/ipc_bridge.py:153-181`), cujos callbacks voltam
pela thread GTK via `GLib.idle_add` e DEVEM retornar `False`. No sucesso, escreva em
`config_bandeja_ajuda`: se o watcher respondeu, uma linha dizendo que o ícone está aparecendo; se
não respondeu e o ambiente é GNOME, a instrução da extensão — o texto já existe em
`docs/usage/troubleshooting.md:140-156` (sintoma, diagnóstico e cura, com o aviso de
logout/login) e a árvore de decisão em `install.sh:3090-3122`, com o nome literal
`ubuntu-appindicators@ubuntu.com`; se não respondeu e o ambiente é COSMIC, a frase que
`app/tray.py:289-341` já usa ("Habilite o applet 'Área de status' no cosmic-panel"). Ambiente
vazio ou "outro": diga o que foi lido e não afirme nada.

**8. Decida a caixa "Mostrar ícone na barra do sistema" ANTES de desenhá-la.** Ela não tem
backend: `AppTray` é sempre construída e iniciada (`app/app.py:1402-1410`) e não há chave nem env
que a desligue (`grep -rn "NO_TRAY\|no_tray" src/` é vazio). Ou (a) a sprint cria a chave, lida
em `run()` antes do `AppTray(...)` — e nesse caso `_has_persistent_access` (`app/app.py:486-503`)
tem de considerá-la, senão fechar a janela com a bandeja desligada esconde o app sem caminho de
volta; ou (b) a caixa sai do escopo e o mockup ganha nota.

**9. "Ligar junto com o computador": resolva a contradição.** CONFIG-07 diz espelho com link;
`mockup/aba-configuracoes.html:445` desenha uma **caixa editável**. O controle de origem existe:
rótulo em `main.glade:2609`, interruptor `daemon_autostart_switch` em `:2613` com dica em `:2614`,
handler `on_daemon_autostart_toggled` em
`src/hefesto_dualsense4unix/app/actions/daemon_actions.py:1933`, e o estado reconciliado sob
`_daemon_autostart_guard` em `:1573-1579` e `:2073-2075` a partir de `systemctl --user is-enabled`
lido em thread worker. Se for espelho, monte um `GtkLabel id="config_autostart_estado"` preenchido
pelo mesmo valor que `_apply_daemon_view` já calcula, mais um `GtkButton` "Abrir em Sistema" que
troque a página procurando o id `daemon_box` — nunca por índice fixo. Se for editável, o segundo
widget tem de entrar no mesmo guarda e no mesmo caminho de reconciliação, e isso é dono duplo.

**10. Registre a aba nos dois mapas do `app/app.py`.** Em `_REFRESH_POR_ABA` (`:920-950`),
acrescente a entrada da aba (ambiente e bandeja mudam por fora da janela);
`tests/unit/test_notebook_switch_page.py:128 test_todo_id_do_mapa_existe_no_glade` exige que o id
exista no glade. E decida sobre `_PAGINAS_COM_TETO_ELASTICO` (`:1037-1044`, seis nomes): ou a
página entra ali, ou entra em `PAGINAS_SEM_TETO` de
`tests/unit/test_largura_a_mesma_em_todas_as_abas.py:102-105` (duas, com o motivo escrito),
consumidos em `:377` e `:384`. Ficar fora das duas é ficar sem cobrança.

**11. `scripts/gui-captura/retratar_abas.py`:** acrescente `"readme_configuracoes"` ao fim de
`NOMES` (`:213-224`) se CONFIG-01 não fez. `CONTROLES_DA_MESA_CHEIA` (`:204`) continua 4: o
fixture de cinco controles que o [TODO-INTEGRACAO.md](TODO-INTEGRACAO.md) item 15 pede **não
existe** (só `tests/fixtures/state_full_quatro_controles.json`). Se você seguiu o passo 3, nada
precisa ser injetado no script — a seção 5 é declarativa e o `builder.add_from_file` (`:1053`) já
a traz.

**12. Teste novo 1, sem GTK — A CRIAR: tests/unit/test_config_a_janela_le_o_ambiente.py.**
Assere: `ambiente_normalizado("pop:GNOME")` é `"gnome"`; `ambiente_normalizado("COSMIC")` é
`"cosmic"`; `ambiente_normalizado("")` é `"outro"` sem levantar; `ambiente_normalizado(None)` é
`"outro"`; `ambiente_efetivo()` devolve a correção gravada quando existe e o normalizado quando
não (monkeypatch sobre `load_gui_prefs`); `degrau_da_escala(0)` é `"compacto"`,
`degrau_da_escala(3)` é `"normal"`, `degrau_da_escala(8)` é `"grande"`; e o degrau "grande" é
menor ou igual a `ESCALA_MAXIMA`.

**13. Teste novo 2, com GTK real — A CRIAR: tests/unit/test_config_a_janela_na_tela.py.**
Primeira linha executável: `from tests.conftest import exigir_gi_real` seguida de
`exigir_gi_real("aba configurações")`, ANTES de qualquer import de `gi` (GUARDA-GI-REAL-01,
`tests/conftest.py:210-222`) — sem ela o módulo derruba a coleta headless inteira em vez de
pular. Monte pelo glade como `test_layout_orcamento_altura.py:237 _montar()`. Assere: os oito ids
do passo 4 existem no builder; nenhum widget da página é `Gtk.ComboBox` nem `Gtk.ComboBoxText`; e
que a aba não deixa a mensagem de ajuda vazia com `XDG_CURRENT_DESKTOP` vazia.

**14. Teste novo 3, a mordida da bandeja.** Extraia a decisão para
`mensagem_da_bandeja(ambiente: str, watcher_presente: bool) -> str` em `app/ambiente.py` e assere <!-- ref-externa: arquivo que esta leva cria -->
os quatro casos: `("gnome", False)` contém `ubuntu-appindicators@ubuntu.com`;
`("cosmic", False)` contém "Área de status"; `("gnome", True)` e `("cosmic", True)` não contêm
instrução de instalação; `("outro", False)` não afirma o que falta. Assim a cura tem portão que
morde sem depender de sessão real — que é o único jeito de fechar o aceite "num GNOME sem a
extensão, a seção mostra a instrução" nesta máquina. Molde literal de monkeypatch da sonda:
`tests/unit/test_tray.py:369` e `:396`.

#### Prova de trabalho

```sh
git rev-parse --short HEAD && git branch --show-current
grep -n 'tab_config_box' src/hefesto_dualsense4unix/gui/main.glade          # antes: >= 1 linha
grep -n 'config_escala_\|config_ambiente_\|config_bandeja_' src/hefesto_dualsense4unix/gui/main.glade
grep -rn 'GtkComboBox' src/hefesto_dualsense4unix/gui/main.glade            # 1 linha, e é comentário (:2506)
python3 scripts/validar-palavra-de-tela.py --all
python3 scripts/validar-acentuacao.py --all && python3 scripts/validar-glifos.py --all
python3 scripts/validar-referencias-docs.py --all
pytest tests/unit/test_layout_orcamento_altura.py -q
pytest tests/unit/test_notebook_switch_page.py tests/unit/test_largura_a_mesma_em_todas_as_abas.py \
  tests/unit/test_app_scroll_wrap.py tests/unit/test_tray.py -q
pytest tests/unit/test_config_a_janela_le_o_ambiente.py tests/unit/test_config_a_janela_na_tela.py -q
pytest tests --collect-only -q --continue-on-collection-errors 2>&1 | grep -cE '^tests/.+::'
ruff check src/ tests/ && mypy src/hefesto_dualsense4unix
pre-commit run --all-files
```

O censo tem de dar 8100 ou mais e ZERO linhas `ERROR `. Se
`test_apptray_em_gnome_cria_indicator_imediato` (`tests/unit/test_tray.py:325`) reprovar, você
mexeu na guarda de `app/tray.py:258` — reescreva o teste junto, não o contorne.

**O aceite de portabilidade que UMA máquina consegue provar:**

```sh
for de in COSMIC 'pop:GNOME' GNOME ''; do
  XDG_CURRENT_DESKTOP="$de" \
  GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py "/tmp/config07-${de:-vazio}" || echo "FALHOU: ${de:-vazio}"
done
```

Esperado: nenhuma linha `FALHOU`, onze PNGs em cada pasta, e a MESMA largura e altura do
`readme_configuracoes.png` nas quatro (leia os bytes 16 a 24 do PNG). A diferença legítima entre
as quatro é só o botão marcado da linha "Ambiente:".

> **O aceite original da sprint se contradiz com a própria feature.** "As capturas saem iguais em
> COSMIC e em GNOME" é impossível se a seção mostra o ambiente detectado e o marca no seletor. E
> `retratar_abas.py` renderiza em `Gtk.OffscreenWindow` (`:1017`, `:1059`), com o docstring
> avisando que ela "não passa pelo compositor" (`:38-40`) — a foto não prova nada sobre a
> bandeja, que é onde COSMIC e GNOME de fato diferem.

#### Armadilhas

- **Montar a seção em Python parece mais fácil e desliga DOIS portões de uma vez.** Ver passo 3.
  A aba passaria verde com 900px de altura e com jargão nos rótulos.
- **`SegmentedSelector` parece a escolha óbvia e aqui é a errada.** Ver passo 3. Se insistir,
  aceite por escrito que a geometria daquelas linhas não é medida por portão nenhum.
- **`homogeneous` numa fileira de três botões.** Já custou 1004 dos 1066px de largura mínima da
  janela INTEIRA, com "Auto" (4 letras) recebendo os mesmos 459px de uma frase — está escrito no
  próprio glade (`main.glade:1645-1650`). E a rolagem horizontal é `NEVER` (`app/app.py:1155`).
- **Chamar `statusnotifierwatcher_available()` na thread do GTK** congela a janela por até dois
  segundos ao entrar na aba.
- **Reaplicar o tema para a escala valer na hora.** `apply_theme` COMPÕE: medido em 13/08, quatro
  chamadas no mesmo processo levaram o `gtk-font-name` de "Fira Sans" a 12,25, 14,5, 16,75 e 19
  pontos (`tests/unit/test_o_status_nao_samba_no_ritmo_do_giroscopio.py:41-46`; também em
  `tests/unit/test_gatilho_palavra_rotulos.py:48-52`). Um `apply_theme(self.window)` no clique
  produz fonte errada e provider empilhado, sem erro nenhum no log.
- **Tratar `XDG_CURRENT_DESKTOP` como se decidisse comportamento.** Ela vem VAZIA em sessão
  headless e COMPOSTA em Pop!_OS (`pop:GNOME`); o `install.sh:3095-3099` trata os dois casos
  separadamente. A regra — o ambiente informa a mensagem, nunca o comportamento — precisa virar
  teste.
- **Entregar a caixa da bandeja gravando uma preferência que ninguém lê.** Ver passo 8.
- **Espelhar "Ligar junto com o computador" como interruptor editável.** Ver passo 9.
- **Usar os hashes da leva.** Ver passo 1. E não tente rebase contra `main`.
- **Achar que a captura prova a portabilidade.** A bandeja NUNCA aparece numa foto de janela
  offscreen. A foto prova geometria e texto.
- **`retratar_abas.py` morre num terminal snap e não se defende sozinho.** Ver 2.3.
- **Contar com o CI para pegar jargão.** `JARGAO_BANIDO` (`scripts/validar-palavra-de-tela.py:85-95`)
  tem oito FRASES exatas — "daemon offline", "daemon pausado", "uinput disponível", "Restaurar
  Default", "Travar Proton validado", "Aplicar correções", "Testar criação de device virtual",
  "Gamepads:" — e não as seis palavras que a restrição 7 de CONFIG-01 lista ("daemon",
  "systemd", "uinput", "JSON", "polling", "throttle"), que são regra de casa SEM portão. Em
  compensação, a DIVIDA_DA_PALAVRA_01 (`:101-118`) reprova quando uma entrada envelhece.
- **Medir geometria sem as fontes do projeto.** Ver 2.2. Custou uma leva inteira em 19/08.
- **Abrir a leva sem confirmar com ela.** Ver seção 7.

---

### CONFIG-08 — a aba entra na documentação

Arquivo da sprint:
[CONFIG-08-a-aba-entra-na-documentacao.md](CONFIG-08-a-aba-entra-na-documentacao.md)

**É a última a commitar.** E ela começa com a suíte já vermelha por um arquivo que a própria
sprint manda versionar — resolva isso primeiro.

#### Roteiro

**PASSO 0 — confira onde você está.** `git rev-parse --abbrev-ref HEAD` tem de dizer `dev`.
Confirme que CONFIG-01 a CONFIG-07 já commitaram. Rode
`python3 -m pytest tests/unit/test_docs_mac_anonimato.py -q` e espere UMA reprovação, a do guia
(é o passo 1). Se houver outras, elas não são suas.

**PASSO 1 — mascare os endereços do guia.** Em `GUIA-RADIO-DA-SALA.md`, linhas 255 e 266, troque
o MAC de adaptador real pela máscara da casa (os três primeiros octetos ficam, os três últimos
viram `00:00:01`). Mesma coisa em `:37`, o teclado BT cujo OUI **não está** em
`_OUIS_REAIS_OCTETOS` (`tests/unit/test_docs_mac_anonimato.py:93-103`, oito OUIs) e por isso
passa hoje pelo buraco declarado do portão — a docstring em `:91-92` manda o contrário:
"controle novo na bancada, OUI novo aqui, no mesmo commit — antes de o endereço dele aparecer em
documento". O arquivo também nomeia a máquina e o sistema dela em `:8-9`. Como saber que deu
certo: `python3 -m pytest tests/unit/test_docs_mac_anonimato.py -q` fica `11 passed`.

**PASSO 2 — versione o guia.** `git add GUIA-RADIO-DA-SALA.md`. Ele NÃO está no `.gitignore`, tem
376 linhas e passa nos portões de acentuação, glifos e anonimato de shell. Deixe-o na raiz:
`validar-referencias-docs.py` só varre `docs/**` mais o `README.md`.

**PASSO 3 — a nota datada do D-A2, e ela entra ANTES das fotos.** Em
`src/hefesto_dualsense4unix/app/actions/external_controllers.py`, o docstring vai de `:1` a
`:14`; a fala do escopo está em `:9-10` e o parágrafo termina em `:13`. Acrescente depois de
`:13` e antes do fecho de `:14` um bloco no formato NOTA DATADA (molde literal em
`docs/usage/interface.md:22-32`): em 21/08/2026 o escopo foi reaberto por decisão dela, a fala de
06/08 continua registrada e não é apagada, e o link para [DECISOES-ABERTAS.md](DECISOES-ABERTAS.md),
seção D-A2. NÃO apague nada.

**PASSO 4 — a nota datada no VETO 3.** Em
`docs/process/sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md`,
o bloco do VETO está em `:488-502` e o item 3 em `:498-502`. O texto literal é: "Qualquer cura
que dependa de alguém DECLARAR, CONFIRMAR ou CLICAR em alguma coisa está fora de escopo DESTA
SPRINT. A pergunta dela é o critério: se não roda sozinha na máquina de um desconhecido, no
primeiro boot, não é esta cura." **A paráfrase da leva apaga o "desta sprint".** Acrescente logo
abaixo do item 3 uma nota datada de 21/08/2026 dizendo: (a) que a frase original já dizia "fora
de escopo DESTA SPRINT" e continua valendo inteira para a cura de identidade; (b) que a leva da
aba Configurações fixou o escopo por escrito — proibido declarar o que o produto PODE medir,
permitido declarar o que ele comprovadamente não mede; (c) as duas salvaguardas literais de D-A1;
(d) link para [DECISOES-ABERTAS.md](DECISOES-ABERTAS.md). Regra de redação: ver 2.5, item 1.

**PASSO 5 — `NOMES` do script de captura.** A tupla está em
`scripts/gui-captura/retratar_abas.py:213-224`, na ordem das abas. A aba nova nasce no FIM, então
acrescente `"readme_configuracoes",` depois de `"readme_navegacao_dsx",`. No mesmo commit corrija
as duas frases que caducam: `:2` ("Retrata as DEZ abas" vira ONZE) e `:211` ("O `interface.md`
cita os nove" — que já mente hoje, porque `NOMES` tem dez — vira "cita as onze").
`NOMES_MESA_CHEIA` (`:229-231`) é derivado e se ajusta sozinho. Como saber que deu certo:
`python3 -m pytest tests/unit/test_a_mesa_cheia_na_foto.py -q` continua verde (ele checa o
invariante de tamanho em `:429`).

**PASSO 6 (opcional, mas é o único momento em que alguém toca este script) — porte a cura do
pixbuf para dentro dele.** Copie `_sanear_loaders_do_gdk_pixbuf()` e `_de_outro_confinamento()`
de `src/hefesto_dualsense4unix/app/main.py` para o topo de `retratar_abas.py`, chamando-a ao lado
de `os.environ.setdefault("GDK_BACKEND", "x11")` (`:165`), antes de qualquer `import gi`. Como
saber que deu certo: `python3 scripts/gui-captura/retratar_abas.py /tmp/olhar` roda inteiro SEM a
variável de ambiente na frente.

**PASSO 7 — neutralize a escala do tema antes de fotografar.** Confira
`~/.config/hefesto-dualsense4unix/gui_preferences.json`: se houver `escala_fonte` com valor
diferente de 3, as fotos sairão numa escala que não é a padrão (`app/theme.py:46`). O script
neutraliza `load_gui_prefs` SÓ do módulo `profiles_actions` e só para `advanced_editor`
(`retratar_abas.py:706-716`) — o do tema passa direto. Ou remova a chave, ou faça o mesmo
monkeypatch para `escala_fonte`.

**PASSO 8 — tire as fotos do README, de verdade.**
`GDK_PIXBUF_MODULE_FILE=... scripts/gui-captura/retratar_abas.py` **sem argumento** (sobrescreve
`docs/usage/assets/`). Como saber que deu certo: a tabela impressa termina com a linha
`Configurações   readme_configuracoes.png   NN KB`, o rodapé diz `11 aba(s)`, e NÃO aparece
nenhum `AVISO` no stderr. Se aparecer `aba_10.png` na pasta, o passo 5 não pegou.

**PASSO 9 — tire as fotos da mesa cheia.** O mesmo comando com `--mesa-cheia` e sem destino
(grava em `docs/process/estudos/assets/mesa-cheia/`, que é versionado: `git ls-files` lista 12
PNGs lá). Como saber que deu certo: `mesa_cheia_configuracoes.png` nasce.

**PASSO 10 — `docs/usage/interface.md`, a seção nova.** Ela vai ENTRE `## Navegação` (que termina
em `:565`) e `## O cabeçalho` (`:567`), porque a ordem da página é a ordem da tira. Formato:
`## Configurações`, a imagem `assets/readme_configuracoes.png`, e a prosa. Espelhe o molde da
`## Início` (`:34-77`): uma frase de tese, os quadros em negrito com o nome literal da tela, e as
caixas de citação para o que tem data. As cinco seções, com o texto que o mockup fixa. Diga
também as três coisas que só a documentação explica: a fita "Ajustes vão para:" fica esmaecida
nesta aba e por quê (D4); nada vale antes do **Aplicar** (D-A4); e todo campo nasce em "não sei",
que é resposta válida (D-A1).

**PASSO 11 — `docs/usage/interface.md`, as duas frases que caducam.** Linha 3: "A janela
principal tem dez abas — nove sempre à vista e a **No jogo**..." vira **onze abas, dez sempre à
vista** (a **No jogo** entra e sai da tira conforme haja jogo da Steam aberto, por `hide()` e não
por `remove_page`). Linha 16: "O que estas dez fotos NÃO mostram: o cabeçalho" vira onze fotos.
Duas armadilhas de redação: ver 2.5 item 1; e ao falar do Aplicar, **não escreva que ele
persiste** — `tests/unit/test_aplicar_nao_persiste.py:158-176` reprova o padrão
"**Aplicar** ... persistem o que está editado" e exige que **Salvar Perfil** continue nomeado.

**PASSO 12 — `README.md`, a tabela de imagens em `:47-61`.** O README **não cita contagem de abas
em prosa nenhuma** — o alvo real é a tabela. A Navegação hoje ocupa uma fileira sozinha, com a
segunda célula vazia (`:59` e `:60`). Preencha essa célula com o título e a imagem da
Configurações. Não mexa nos emblemas do topo — há portão (`tests/unit/test_emblemas_do_readme.py`)
e o `README.md` já está com um diff não commitado (troca do emblema de CI), que não é seu.

**PASSO 13 — `docs/process/COMO-OLHAR-A-TELA.md`** (430 linhas, declarado "o primeiro arquivo a
ler nesta casa"). Corrija as três frases de contagem: `:67` ("nenhuma das dez fotos de aba
alcança"), `:168` ("as dez fotos são do `main_notebook`") e `:211` ("passaram a sair idênticas nas
dez"). Não mexa na tabela de scripts — ela é gatilho de
`tests/unit/test_a_tabela_dos_scripts_de_tela.py` (`:29`) e nenhum script novo nasceu nesta leva.

**PASSO 14 — `docs/usage/assets/CONFERIDO-EM.md`.** A tabela está em `:25-28`. Acrescente uma
linha: data 21/08/2026, o hash curto do commit da tela que você está conferindo
(`git log -1 --format=%h -- src/hefesto_dualsense4unix/app src/hefesto_dualsense4unix/gui`), e o
resultado — aqui será "**11 abas.** A aba Configurações entrou; as dez antigas saíram idênticas
(ou com as diferenças X e Y)". Se alguma das dez antigas mudou de pixel, isso é mudança de
DESENHO e é palavra dela, não sua (PROVA-DE-TELA-01, citado no próprio arquivo em `:9-11`).

**PASSO 15 — `CHANGELOG.md`.** A seção `## [Unreleased]` está em `:41`, vazia. Escreva ali a
entrada da leva, no formato das outras (molde literal em `:44-62`, a entrada da 0.9.4.5): um
parágrafo de tese, depois `### Adicionado` com subtítulos em linguagem de gente. **NÃO suba a
versão**: `scripts/check_version_consistency.py` roda verde hoje
(`OK: 12 alvo(s) versionado(s) em 0.9.4.5`) e entrada sob Unreleased não exige bump. Rode com o
`python3` do sistema (3.12), não com o `.venv` (3.10, sem `tomllib`).

**PASSO 16 — decida sobre versionar a pasta da leva.**
`docs/process/sprints/2026-08-21-ABA-CONFIGURACOES/` está untracked (13 arquivos `.md` mais
`mockup/`). Se for versionada, `validar-referencias-docs.py --all` passa a cobrar os arquivos que
ela cita (hoje está verde: `OK: 372 documento(s) sem referência morta`, depois que a citação de
`config_actions.py` em CONFIG-01 foi reescrita como "A CRIAR"). Antes de commitar, conserte os <!-- ref-externa: arquivo que esta leva cria -->
endereços podres que a seção 5 deste documento lista.

**PASSO 17 — commite na ordem.** Um commit só é o caminho seguro, porque o portão das fotos
compara topologia e a nota do passo 3 é uma mexida em `app/`. Mensagem:
`docs: CONFIG-08 — a aba Configurações entra na documentação`.

#### Prova de trabalho

```sh
git rev-parse --abbrev-ref HEAD                              # dev
python3 -m pytest tests/unit/test_docs_mac_anonimato.py -q   # 11 passed (hoje: 1 failed, 10 passed)
bash scripts/check_anonymity.sh                              # "OK: anonimato preservado."
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py
ls docs/usage/assets/readme_*.png | wc -l                    # 11
ls docs/usage/assets/aba_*.png                               # nada
grep '^abas:' docs/usage/assets/PROVA-DA-FOTO.txt            # abas:   13  (hoje diz 12)
GDK_PIXBUF_MODULE_FILE=... scripts/gui-captura/retratar_abas.py --mesa-cheia
ls docs/process/estudos/assets/mesa-cheia/mesa_cheia_configuracoes.png
python3 -m pytest tests/unit/test_as_fotos_acompanham_a_versao.py -q      # 4 passed, DEPOIS do commit
python3 -m pytest tests/unit/test_nome_citado_como_sprint_existe.py -q    # 4 passed
python3 -m pytest tests/unit/test_aplicar_nao_persiste.py -q              # 5 passed
python3 -m pytest tests/unit/test_a_tabela_dos_scripts_de_tela.py \
  tests/unit/test_a_mesa_cheia_na_foto.py \
  tests/unit/test_retrato_das_abas_nao_vaza_dado_real.py \
  tests/unit/test_emblemas_do_readme.py -q
python3 scripts/validar-referencias-docs.py --all
python3 scripts/validar-acentuacao.py --all && python3 scripts/validar-glifos.py --all
python3 scripts/validar-palavra-de-tela.py
python3 scripts/check_version_consistency.py
```

O recibo conta TODOS os PNGs da pasta, não só as abas: `retratar_abas.py:1170` monta a lista com
`saida.glob("*.png")`, então `social-preview.png` e `perfis-jogo-da-steam.png` entram na conta. O
recibo só é reescrito quando o destino é o padrão (`:1121-1123`).

**TESTE NOVO A ESCREVER (nenhum existe) — A CRIAR:
tests/unit/test_a_documentacao_conhece_todas_as_abas.py.** Sem GTK, lendo arquivo. Assere: (1)
para cada nome de `NOMES`, existe o PNG correspondente em `docs/usage/assets/`; (2) o
`docs/usage/interface.md` tem um `## <rótulo>` para cada aba, comparando contra os rótulos
`<child type="tab">` do `main.glade` — hoje NADA liga as duas listas, e a frase "dez abas" do
`interface.md:3` envelheceu sem portão nenhum reclamar; (3) o `README.md` aponta para todos os
`readme_*.png` da pasta. **A mordida:** apagar a seção `## Configurações` do `interface.md`, ou
tirar `readme_configuracoes` de `NOMES`, tem de reprovar nomeando o que ficou de fora.

#### Armadilhas

- **O portão das fotos morde pela ORDEM DOS COMMITS, não pelo conteúdo.** Ver passo 3 e passo 17.
- **Vai passar verde com a foto no nome errado.** O aceite é `ls docs/usage/assets/readme_configuracoes.png`,
  nunca "rodou sem erro".
- **As fotos carregam a preferência de escala da máquina de quem roda.** Ver passo 7. Como
  CONFIG-07 põe essa escala na tela, a primeira pessoa que brincar com ela e depois refotografar
  publica onze fotos fora do padrão, sem erro nenhum.
- **"Nos dois ambientes" não significa PNGs iguais nos dois ambientes.** `apply_theme` lê
  `gtk-font-name` e `gtk-theme-name` das `Gtk.Settings` do sistema (`theme.py:154-157` e `:188`),
  e o tema de ícones vem de fora. O aceite honesto é: roda limpo nos dois; os PNGs versionados
  saem de UM. Escreva isso no `CONFERIDO-EM.md`.
- **O guia que a sprint manda versionar reprova a suíte HOJE, antes de você começar.** O portão lê
  `git ls-files --cached --others --exclude-standard` (`test_docs_mac_anonimato.py:174-184`) —
  arquivo untracked já conta.
- **O `check_anonymity.sh` diz OK e mente por omissão.** A varredura de MAC dele é só de arquivo
  BINÁRIO; a de texto foi delegada ao pytest (comentários em `:201` e `:328`). O job `anonymity`
  passa e o `lint-test` reprova, pelo mesmo arquivo. É a família de defeito que PONTO-A-PONTO-01
  batizou.
- **Um endereço real sobrevive pelo buraco declarado do portão.** Ver passo 1.
- **Escrever a palavra "sprint" colada a um ID em `docs/` reprova o CI.** Ver 2.5, item 1.
- **O `interface.md` já é lido por um teste, e ele tem uma frase proibida.** Ver passo 11.
- **A cura do pixbuf não está no script, e sem ela nada roda.** Ver 2.3.
- **Não rode o script com destino em `/tmp` achando que está atualizando a documentação, e não
  rode sem destino achando que está "só olhando".** Sem argumento ele SOBRESCREVE
  `docs/usage/assets/`.
- **O interpretador local troca de baixo de você.** Ver 2.2.
- **Dois documentos com a contagem de abas ficam fora da lista de alvos da sprint e nenhum portão
  os cobra:** `docs/process/COMO-OLHAR-A-TELA.md` e o segundo conjunto de fotos versionado,
  `docs/process/estudos/assets/mesa-cheia/`. Por isso o teste novo vale mais do que parece.

---

### CONFIG-09 — "Está tudo certo?"

Arquivo da sprint: [CONFIG-09-esta-tudo-certo.md](CONFIG-09-esta-tudo-certo.md)

**A recomendação da sprint (`doctor.sh --json`) não sobrevive ao empacotamento e tem de ser
trocada.** O `scripts/doctor.sh` NÃO viaja nos pacotes: o `.spec` do Fedora
(`packaging/fedora/hefesto-dualsense4unix.spec:192-193` e `:237-238`) instala só
`scripts/install-host-udev.sh` e `scripts/dkms_lib.sh`; o manifesto flatpak não menciona o
doctor; o `install.sh:3064-3076` só copia `storm_watch.sh`. E `_find_doctor_sh`
(`src/hefesto_dualsense4unix/cli/cmd_doctor.py:36-38`) devolve `None` num pacote. A saída certa é
a terceira, que a sprint não considerou: **módulo Python dentro do wheel publicando JSON, mais um
`check_*` fino no doctor que o consome, sem tirar uma linha do que já está lá.** É o padrão que a
casa já usa três vezes: `src/hefesto_dualsense4unix/integrations/sentinela_do_wrapper.py:212`
(consumido por `scripts/doctor.sh:1612-1633`),
`src/hefesto_dualsense4unix/integrations/prontuario_dos_jogos.py:505` e
`src/hefesto_dualsense4unix/integrations/proton_pin.py:1225`.

#### Roteiro

**1. Confira em que commit você está e em que ramo.** `dev`, `70d28762` ou descendente.

**2. CONFIG-09 depende de CONFIG-02, que depende de CONFIG-01.** Confirme que existem, no glade, a
página `scroll_tab_config_box` com o `GtkBox id="tab_config_box"` dentro, e que
`config_actions.py` já tem `ConfigActionsMixin.install_config_tab()`. <!-- ref-externa: arquivo que esta leva cria -->

**3. CORRIJA A SPRINT ANTES DE CODAR.** Três blocos: (a) `:11-13` — trocar "4920 linhas e 26
funções" por **5136 linhas e 63 checagens** (`main()` em `:5009-5122` faz 64 chamadas de check; o
arquivo tem 130 funções de topo); (b) `:44-62` inteira — a citação de `ipc_handlers.py:2605-2612`
("Duas descrições do mesmo fato se afastam na primeira mudança") **está morta**: a frase não
existe em `src/`, e `daemon/ipc_handlers.py:2595-2620` hoje é o bloco de comentários sobre
contadores de rumble por vpad. Reescreva a decisão apoiada em `prontuario_dos_jogos.py:203-205`
("o que impede as duas de divergirem não é a disciplina de quem edita: é o portão
`test_ponte_confirmada_01`, que compara as DUAS leituras sobre a mesma pasta de perfis e reprova
se discordarem") e em `sentinela_do_wrapper.py:212`; (c) `:72-77` — a prova de trabalho.

**4. CRIE A CRIAR: src/hefesto_dualsense4unix/integrations/exame_da_mesa.py.** Molde, na ordem:
cabeçalho e disciplina de `src/hefesto_dualsense4unix/integrations/storm_doctor.py:1-19`
(read-only, sem root, cada função recebendo os paths por parâmetro com default igual ao sistema
real, para teste com fixture — o cabeçalho declara a regra em `:5-6`); forma JSON e CLI de
`sentinela_do_wrapper.py:205-225` e `:497-560`. Módulo 100% stdlib de propósito: ele roda pelo
`python3` do sistema quando o doctor o chama. `mypy` é `strict` (`pyproject.toml:116-119`).

**5. O vocabulário do exame como constantes de módulo, uma vez só:** `certo`, `atencao`,
`problema` e `nao_sei`. O quarto é obrigatório e não é enfeite — é o que a checagem devolve
quando precisaria de root. Um dataclass congelado `Item` com `chave`, `rotulo`, `estado`,
`porque` e `cura` opcional, mais `como_dicionario()` no molde de `sentinela_do_wrapper.py:211`.

**6. Escreva as CINCO checagens que têm origem verificada, uma função pura por linha da tela.**
Traduza a lógica, não a mensagem:
(a) energia do rádio, de `scripts/doctor.sh:2340-2356` (`check_btusb_autosuspend`: lê
`/sys/module/btusb/parameters/enable_autosuspend` e
`/etc/modprobe.d/hefesto-btusb-no-autosuspend.conf`);
(b) energia das portas, de `:2240-2260` (`check_usb_power_devices`, percorre
`/sys/bus/usb/devices/*/power/control`);
(c) suporte ao controle, de `:393-401` (`check_hid_playstation`, `/proc/modules` ou
`/sys/module/hid_playstation`);
(d) pareamentos, de `:3213-3231` (`check_bt_paired_sem_bonded`, pelo D-Bus via `busctl`) —
**NUNCA** pelo `/var/lib/bluetooth`: `check_bt_bonds_persistidos` (`:3050-3053`) e
`check_bt_sdp_cache_envenenado` (`:3086-3089`) começam com `sudo -n true` e desistem sem ele, e a
GUI é sudo-zero por doutrina. A linha da tela não pode afirmar "Todos os controles têm
pareamento salvo e válido"; o rótulo encolhe junto com a pergunta;
(e) vizinhança das portas **NÃO é sua** — ela consome a leitura de CONFIG-02; se CONFIG-02 ainda
não publicou, o item nasce em `nao_sei` e a tela diz que não sabe.

**7. "Firmware dos adaptadores" é decisão, não implementação.** Não há checagem correspondente no
doctor (grep por `firmware` só devolve texto de mensagem e o check de DKMS). Duas saídas honestas:
(i) tirar a linha e o exame passa a ter cinco; (ii) mantê-la e declarar que é diagnóstico NOVO,
lendo o journal do kernel por `Direct firmware load ... failed`, sem root, como
`check_bt_crc_counters` (`:2750-2760`) já faz. Não escolha em silêncio — a sprint afirma em `:18`
que não constrói diagnóstico novo. **"Vizinhança das portas" também não existe no doctor**: o que
existe é `suggest_port` (`:4904`), modo à parte que sai antes do `main` e diz explicitamente
"diagnóstico NEUTRO".

**8. `exame() -> list[Item]`** chamando as cinco na ordem da tela, e **`veredito(itens) -> str`**
derivando o selo do topo: verde só quando NENHUM item é `problema`; `atencao` quando há atenção e
nenhum problema; `problema` quando há um. Esta função é a resposta escrita ao commit `6c86e295`
(16/08/2026): "Nos últimos dias esse verde saía logo ACIMA do [FAIL] PRAGMATA. O dano não é errar
um diagnóstico: é a tela ensinar que verde-e-vermelho juntos são normais por aqui, que é como um
portão morre de descrédito." **O selo não pode ser calculado em outro lugar.**

**9. Feche o módulo com o CLI**, molde `sentinela_do_wrapper.py:526-560`: `--censo` imprime o
JSON, `--relatorio` imprime linhas para gente. Termine com `main(argv=None) -> int` e o guard
`if __name__ == "__main__":` — o guard é o que impede o `promessa-sem-caminho` de acusar `main`
de órfã.

**10. ACRESCENTE ao `scripts/doctor.sh` uma função `check_exame_da_mesa()`**, copiando a forma de
`check_sentinela_wrapper` (`:1612-1660`): resolve o caminho do módulo, sai calada se o arquivo ou
o `python3` faltarem, roda `--censo` e reduz o JSON com um heredoc Python curto. Chame-a em
`main()`, logo depois de `check_bt_paired_sem_bonded` (`:5077`). **NÃO REMOVA, NÃO REESCREVA e
NÃO MOVA nenhuma função existente**: 54 arquivos de teste leem este arquivo como TEXTO (só
`tests/unit/test_plataforma_wiring.py` tem 51 asserções `in DOCTOR`, com `DOCTOR` lido em `:32`),
e `tests/unit/test_doctor_cobra_as_duas_obrigatorias.py:33-37` extrai funções por regex e as roda
em bash com `bwrap` — sua função nova tem de nascer nessa mesma forma (nome na coluna 0, abertura
e `}` sozinho na coluna 0).

> **Correção de argumento.** A sprint diz que os testes fazem grep na SAÍDA do doctor
> (`test_plataforma_wiring.py:216`, `assert "RSSI" in DOCTOR`). É grep no TEXTO-FONTE. O efeito
> inverte o custo: acrescentar `--json` não ameaça esses testes; **tirar** checagens do doctor,
> como a opção 2 da sprint propõe, apagaria as strings que 54 arquivos asseram.

**11. NO GLADE**, dentro do `GtkBox id="tab_config_box"`, acrescente o cartão da seção 0
espelhando `storm_card` (`main.glade:2693-2713`): `GtkBox` vertical, `spacing=4`, com a classe de
card; um `GtkLabel` de título com `use-markup` e `xalign=0`; um `GtkBox` horizontal com o selo
(`GtkLabel id="config_saude_selo"`, `use-markup`), o `GtkButton id="btn_config_saude_examinar"`
rotulado `Examinar de novo` e um `GtkLabel id="config_saude_quando"` alinhado à direita; e um
`GtkLabel id="config_saude_itens"` com `use-markup` e `xalign=0` para as seis linhas.
**PROIBIDO nos textos do glade: `sudo`, `JSON`, `systemd`, `.service`, `throttle`** — a lista
completa está em `tests/unit/test_glade_vocabulario_leigo.py:39-63`, que reprova em `label` e
`tooltip-text`, e ela inclui ainda `systemctl`, `rc=`, `Unit:`, `Motor fraco`, `Motor forte`,
`weak`, `strong`, `Política de rumble`, `Preview do perfil` e `Anti-storm`. As mensagens de cura
do doctor são cheias de `sudo` — elas têm de ser traduzidas no Python.

**12. EM `config_actions.py`, acrescente ao `ConfigActionsMixin` três métodos**, espelhando <!-- ref-externa: arquivo que esta leva cria -->
`src/hefesto_dualsense4unix/app/actions/daemon_actions.py:731-776` linha por linha:
`_refresh_saude_da_mesa()` que submete um worker a `_get_executor()` (importado de
`app.ipc_bridge`, como em `daemon_actions.py:33`), importa `exame_da_mesa` DENTRO do worker,
monta o markup com as cores em hex e devolve por `GLib.idle_add`;
`_apply_saude_da_mesa(markup, selo, quando) -> bool` que escreve nos três rótulos por
`self._get(id)` com guarda `is None` e devolve `False`; e o handler do botão. Todo o corpo do
worker dentro de `try/except Exception` com `logger.warning` — é DIAGNÓSTICO-NAO-DERRUBA-A-ABA-01,
escrito em `daemon_actions.py:1878-1893`.

**13. Decida a cor do estado "atenção" e escreva a decisão no código.** Se seguir a casa, use o
mesmo dicionário de `daemon_actions.py:754`, que é quem já pinta linhas do doctor na janela:
`{"[ OK ]": "#50fa7b", "[WARN]": "#ffb86c", "[INFO]": "#8b8fa8"}`, com `#ff5555` para problema.
`src/hefesto_dualsense4unix/app/actions/profiles_actions.py:1461` e `:1842` chamam `#ffb86c` de
"o token de ALERTA da casa", e `gui/theme.css:13` fixa o vocabulário: "VERDE confirma, LARANJA
alerta, VERMELHO destrói, CIANO informa". O mockup usa `--yellow` (`aba-configuracoes.html:75-76`,
`:84-86`); `@yellow` (`theme.css:31`) é "alerta suave" e serve outro papel — "era para estar
valendo e não está" (`src/hefesto_dualsense4unix/app/widgets/painel_no_jogo.py:141-148`). As duas
passam no `test_paleta_unica.py`; **nenhum portão decide por você**, e hoje há duas descrições do
mesmo estado na mesma janela.

**14. LIGUE A ABA.** Em `app/app.py`: chame `_refresh_saude_da_mesa()` de dentro de
`install_config_tab()`; acrescente a entrada em `_REFRESH_POR_ABA` (`:920`, por ID DO GLADE,
nunca por índice — EST-10); e acrescente o handler do botão ao dicionário de `_signal_handlers()`
(`:308`), senão o botão nasce morto em silêncio (BUG-GUI-EMULATION-HANDLERS-UNWIRED-01, citado em
`daemon_actions.py:688-695`). Sobre o `_REFRESH_POR_ABA`, leia a contradição registrada em
CONFIG-02, PASSO 7.

**15. ESCREVA A CRIAR: tests/unit/test_exame_da_mesa.py** (sem GTK, sem root). Com fixtures em
`tmp_path`: energia do rádio devolve `certo` com `enable_autosuspend=N` e `atencao` com `Y`;
energia das portas devolve `atencao` quando algum `power/control` diz `auto`; pareamentos devolve
`nao_sei` quando `busctl` não existe (e nunca `problema`); `veredito` devolve verde SÓ com zero
itens em `problema`; e — **a mordida que importa** — trocar UM item para `problema` derruba o selo
do topo de verde para vermelho. Sem essa última, o teste é carimbo.

**16. ESCREVA A CRIAR: tests/unit/test_config_selo_de_saude.py** (GTK real). Primeira linha
executável: `from tests.conftest import exigir_gi_real` e `exigir_gi_real(...)`. Assere que os
quatro ids existem no glade e que nenhum texto de tela da seção contém `sudo`.

**17. ATUALIZE [TODO-INTEGRACAO.md](TODO-INTEGRACAO.md):** o item 6 (`doctor.sh --json`, com o
mesmo 4920/26) e a linha da tabela de scripts que promete o `--json` aditivo descrevem o caminho
que esta reconciliação descarta. Corrija também o endereço do `hci0` fixo — ver seção 5,
subitem D.

#### Prova de trabalho

```sh
.venv/bin/python -m pytest tests/unit/test_exame_da_mesa.py -q
python3 src/hefesto_dualsense4unix/integrations/exame_da_mesa.py --censo | python3 -m json.tool | head -40
bash scripts/doctor.sh --quiet 2>&1 | grep -c 'exame da mesa'    # >= 1
shellcheck -S error scripts/*.sh scripts/ci/*.sh install.sh uninstall.sh
.venv/bin/python -m pytest tests/unit/test_plataforma_wiring.py \
  tests/unit/test_doctor_nao_afirma_efeito.py \
  tests/unit/test_doctor_cobra_as_duas_obrigatorias.py -q
xvfb-run -a .venv/bin/python -m pytest tests/unit/test_config_selo_de_saude.py \
  tests/unit/test_layout_orcamento_altura.py tests/unit/test_glade_vocabulario_leigo.py \
  tests/unit/test_paleta_unica.py tests/unit/test_notebook_switch_page.py -q
python3 scripts/validar-glifos.py --all && python3 scripts/validar-acentuacao.py --all
python3 scripts/validar-palavra-de-tela.py --all && python3 scripts/validar-referencias-docs.py --all
.venv/bin/python -m pytest tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py -q
.venv/bin/python -m mypy src/hefesto_dualsense4unix/integrations/exame_da_mesa.py \
  src/hefesto_dualsense4unix/app/actions/config_actions.py
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  .venv/bin/python scripts/gui-captura/retratar_abas.py /tmp/config09
```

Notas medidas: `bash scripts/doctor.sh --quiet` leva **2,4 s** de relógio (1,59 s user, 0,82 s
sys) e sai com rc 1 enquanto houver qualquer FAIL — hoje devolve **2 FALHAS e 5 avisos** nesta
máquina, então o aceite "numa máquina saudável, selo verde" não é demonstrável aqui sem consertar
a máquina antes. A prova escrita na sprint (`scripts/doctor.sh --json | python3 -m json.tool`)
NÃO roda: o laço de argumentos (`:72-82`) só imprime `[doctor] aviso: argumento desconhecido` e
segue, e o `json.tool` morre com `Expecting value: line 1 column 2 (char 1)`.
`test_doctor_cobra_as_duas_obrigatorias` pode PULAR aqui por falta de `bwrap` — pulo é tolerável
nesta máquina, nunca no CI. Se o `promessa-sem-caminho` acusar o módulo novo, é porque a aba
ainda não o chama: **`doctor.sh` NÃO conta como chamador de produção**, porque o portão só varre
`*.py` dentro de `scripts/` (`portao_a_casa_sabe_e_o_produto_nao_faz.py:136-163`, `:972-973`).

#### Armadilhas

- **O caminho recomendado pela sprint entrega uma seção VAZIA para quem instalou por pacote.** Ver
  a abertura desta seção.
- **Tirar checagens de DENTRO do `doctor.sh` quebra 54 arquivos de teste.** Ver passo 10.
- **Selo verde com linha vermelha embaixo é o defeito que esta casa já pagou duas vezes em
  agosto.** `6c86e295` e `c3d3518f` (VERDE-MENTIROSO-01, com portão próprio em
  `tests/unit/test_doctor_cobra_as_duas_obrigatorias.py`).
- **Ecoar a mensagem do doctor num rótulo do glade reprova o CI e viola a doutrina sudo-zero na
  mesma linha.** Ver passo 11. E o `validar-palavra-de-tela.py` só varre o glade, então texto
  montado em Python passa livre e a disciplina fica só com você.
- **`_find_repo_file` copiado do lugar errado vira botão que finge funcionar.**
  `daemon_actions.py:712-729` carrega a cicatriz por escrito: BUG-GUI-REPO-ROOT-OFFBYONE-01 —
  `parents[3]` resolvia para `<repo>/src`, nenhum script era encontrado, e os botões eram no-op
  SILENCIOSO com toast de sucesso. De `app/actions/` a raiz é `parents[4]`; de `cli/` é
  `parents[3]`.
- **Rodar o exame na thread do GTK congela a janela.**
  BUG-GUI-SYSTEMCTL-SYNC-NA-THREAD-GTK-01, `daemon_actions.py:1817-1827`: um `subprocess.run`
  síncrono com timeout de 10 s bloqueava a UI inteira, e em D-state nem o kill chegava.
- **Uma exceção no diagnóstico não pode levar a aba junto.** Ver passo 12.
- **O módulo novo será acusado pelo `promessa-sem-caminho` se nascer sem a aba.**
- **Acrescentar a aba ao `_REFRESH_POR_ABA` sem tocar no teste que o congela reprova o
  `lint-test`** — segundo CONFIG-09; segundo CONFIG-02 o mapa é livre. Ver a contradição
  registrada em CONFIG-02, PASSO 7.
- **Medir a geometria da aba sem as duas fontes dá número que nenhuma instalação real produz.**
  Ver 2.2. Nesta máquina as duas estão instaladas (`fc-list | grep -ci space.grotesk` devolve 5).
- **O `retratar_abas.py` morre num terminal snap e não se defende sozinho**, e ainda tem DEZ nomes
  em `NOMES` se CONFIG-01 não fez o passo 7.
- **O pre-commit desta casa NÃO roda na sua máquina, e um hook global reescreve arquivo no
  commit.** Ver 2.4.
- **Não abra esta leva sem confirmar com quem manda.** Ver seção 7.
- **A janela passaria a ter DUAS telas de "saúde do sistema"**, uma na aba Sistema (o cartão
  `storm_card`, `main.glade:2694`, com o rótulo `storm_diag_label` em `:2706`, travado por
  `tests/unit/test_glade_vocabulario_leigo.py:75-96`) e outra na Configurações. Ou CONFIG-09
  estende o cartão existente, ou explica a divisão de assunto por escrito. D3 do INDICE diz que a
  aba nova não rouba controle das existentes; isto é o caso-limite dessa regra.

---

## 5. CORREÇÕES QUE O CÓDIGO NOVO IMPÔS

Tudo que veio como referência quebrada nos nove relatórios, consolidado por assunto. Cada item
tem três linhas: **o que a sprint dizia**, **o que é verdade hoje**, **o que mudar no plano.**

Lembrete de 2.5, item 3: **nenhum destes endereços errados derruba CI.** `validar-citacoes-de-linha.py`
não cobre `docs/process/`. Corrigi-los é para a próxima pessoa não se perder.

### A. A estrutura da aba: glade e `app.py`

**A1. A linha do notebook.**
Dizia: CONFIG-01:21, "página nova no `GtkNotebook id="main_notebook"` (linha 212)".
Hoje: o objeto está em `src/hefesto_dualsense4unix/gui/main.glade:218`; o arquivo tem 4047 linhas.
Mudar: `:218`, e ancorar a INSERÇÃO por conteúdo — o último `<child type="tab">` (rótulo
`Navegação`) está em `:3951-3953` e o `</object>` que fecha o notebook em `:3955`.

**A2. O molde da página.**
Dizia: CONFIG-01:21, "a página é um `GtkBox` vazio, `spacing=12`, `margin=12` — igual ao molde da
Início (`:219-222`)".
Hoje: `:219-222` é o miolo do próprio `<object class="GtkNotebook">`. O molde real é
`main.glade:243-246`; e desde JANELA-CORTADA-01 a PÁGINA não é mais o box cru: é um
`GtkScrolledWindow id="scroll_tab_home_box"` (`:234-243`) com o box dentro.
Mudar: `:234-247`, e a instrução vira "a página nova nasce `GtkScrolledWindow
id="scroll_tab_config_box"` (copiando as sete propriedades) com um único filho
`GtkBox id="tab_config_box"`".

**A3. O import no `app.py` era só metade do trabalho.**
Dizia: CONFIG-01:23, "importar o mixin (bloco de imports, linhas 29-42)".
Hoje: o bloco de imports vai de `app.py:29` a `:57`; `:29-42` é só a fatia dos mixins de
`actions/`. E falta a segunda metade: o mixin tem de entrar na lista de bases de
`class HefestoApp(...)`, em `:155-167`.
Mudar: escrever "import em `:29-42` (ordem alfabética, entre `carona_do_wrapper` em `:29` e
`daemon_actions` em `:30`) E base da classe em `:155-167`". Sem a base, `install_config_tab` não
existe no objeto e o `show()` estoura. O mesmo endereço aparece em CONFIG-03, que corrige para
`app.py:29-57`.

**A4. O molde de `install_home_tab`.**
Dizia: CONFIG-01:22 (versão anterior), "molde verificado: `home_actions.py:1055-1412`".
Hoje: já corrigido no documento em 21/08. O endereço real é `install_home_tab` em
`src/hefesto_dualsense4unix/app/actions/home_actions.py:1394`, dentro de
`class HomeActionsMixin(WidgetAccessMixin)` em `:1383`; a faixa `1055-1412` ficaria fora do
método.
Mudar: deixar o anchor exato — "espelhe `install_home_tab` em `home_actions.py:1394`; a guarda de
idempotência está em `:1397-1399` e o `_get` vem de `actions/base.py:325`".

**A5. `install_config_tab()` tem de ser chamado em DOIS lugares.**
Dizia: nada — a sprint só previa um.
Hoje: `app.py:1171-1179` (dentro de `show()`) e `app.py:1435-1443` (dentro de `run()`, ramo
`if start_hidden and self.tray.is_available():`) repetem a mesma lista de nove `install_*_tab`. O
comentário em `:1432-1434` diz por quê: BUG-HOME-TAB-HIDDEN-INSTALL-01. E
`grep -rln start_hidden tests/unit/` não devolve nada.
Mudar: as duas chamadas, mais o teste por AST de CONFIG-01, passo 8 — é o único guarda que vai
existir.

**A6. Toda página precisa de id no widget de conteúdo.**
Dizia: nada.
Hoje: `tests/unit/test_largura_a_mesma_em_todas_as_abas.py:355-381`
(`test_toda_aba_continua_sendo_reconhecida_pelo_id_do_glade`) assere `None not in nomes` para
todas as páginas; `id_da_pagina` (`home_actions.py:79-105`) desce pelo `ScrolledWindow` e pelo
`Viewport`.
Mudar: escrever na sprint que o `GtkBox` interno PRECISA de `id="tab_config_box"`. Um scroller com
filho anônimo derruba esse teste e o reconhecimento da aba pelos dois pollers, em silêncio.

### B. Geometria: o teto de altura e a largura

**B1. A aba mais larga e o teto por aba — os relatórios discordam.**
Dizia: CONFIG-01:33, "a aba mais larga hoje é Lightbar, com 1110px"; CONFIG-01:33-34, "teto para a
aba nova: ~1166px de largura mínima"; INDICE:317, "1729px contra os ~654px que uma página de aba
ocupa nesta casa".

> **Contradição registrada, e é a maior da leva.**
> **CONFIG-01** mediu, sob `xvfb-run`, com Space Grotesk e JetBrains Mono e delta 3 de escala:
> Lightbar pede **1138px**, o `root_box` inteiro pede **1140px**, e o teto derivado de altura é
> **657px** (janela 830 menos cabeçalho/rodapé 125 menos cromo do notebook 48), com a aba mais
> alta de hoje — Emulação — em **646px de 657**.
> **CONFIG-02 e CONFIG-09** mediram, no mesmo HEAD `70d28762`, sob xvfb 1920x1080x24, com as
> mesmas fontes, reproduzindo o cálculo de `tests/unit/test_layout_orcamento_altura.py`:
> teto por aba **718px** (janela 830 menos cabeçalho e rodapé **73** menos cromo do notebook
> **39**); aba mais larga **Status com 1064px**, Lightbar **1046**, Perfis 979, Navegação 944,
> Emulação 816, Sistema 790, Rumble 666, Gatilhos 528; janela inteira **1066px**; alturas
> Emulação **553**, Sistema 493, Navegação 448, Lightbar 439.
> **CONFIG-06 e CONFIG-07** repetem os ~654px de LEGIBILIDADE-01, anteriores à cura de 17/08.
> Os três números de teto (654, 657, 718) e as duas listas de largura são incompatíveis. **Meça
> você, sob `xvfb-run`, antes de decidir qualquer corte de conteúdo** — e trate o número como do
> dia, porque a régua é `tests/unit/test_layout_orcamento_altura.py`, não o texto de sprint
> nenhuma.

Hoje, o que os relatórios concordam: **o teto de LARGURA contra o qual o portão compara é 1180**,
lido do glade (`default-width`, `main.glade:103`, e `test_layout_orcamento_altura.py:80`). Não
existe portão que compare contra 1166 — o 1166 é o comentário de `app.py:1041` sobre o que as
páginas de HOJE pedem numa janela de 1920, e é observação, não teto. O teto elástico de página é
`LARGURA_CARD_ELASTICA = 1400` (`src/hefesto_dualsense4unix/app/widgets/controller_card.py:359`).
Mudar: escrever 1180 como teto de largura, medir o de altura no dia, e dizer de onde veio.

**B2. O portão de altura não vê conteúdo montado em código.**
Dizia: nada.
Hoje: `_montar()` (`tests/unit/test_layout_orcamento_altura.py:237-252`) faz só
`builder.add_from_file(str(MAIN_GLADE))`; nenhum `install_*_tab` roda. Idem `_montar` de
`tests/unit/test_largura_a_mesma_em_todas_as_abas.py:170-200`. E a aba Início é "100% montada em
código" por escrito (`main.glade:265-266`).
Mudar: escrever as duas consequências opostas na sprint. (a) CONFIG-01 passa nos portões de
geometria trivialmente. (b) Todo o conteúdo das sprints seguintes nasce INVISÍVEL para o portão
de altura. Ou a leva escreve o próprio teste de geometria montando a aba pelo mixin, ou o
orçamento de altura desta aba nunca vai ser medido por ninguém.

**B3. O portão mede o conteúdo, não o scroller — e quase nasceu cego.**
Dizia: nada.
Hoje: `tests/unit/test_layout_orcamento_altura.py:268-292` registra que, depois da
JANELA-CORTADA-01, `get_nth_page(i)` passou a devolver o scroller, e a aba Rumble engordada em
900px deixou os sete testes verdes. `_conteudo_da_pagina` desce ao conteúdo atravessando o
`Viewport`.
Mudar: nenhuma sprint pode tratar a barra de rolagem como licença para crescer.

### C. Paleta, vocabulário de tela e jargão

**C1. As 26 cores oficiais são 20.**
Dizia: CONFIG-01:47, "cor: só as 26 oficiais".
Hoje: `src/hefesto_dualsense4unix/gui/theme.css` declara **20** `@define-color` (`:21-31` e
`:43-54`). O portão é `tests/unit/test_paleta_unica.py`, cujo `PALETA` (`:19-35`) tem 20 hexes e
cujo `PERMITIDAS` (`:38-51`) tem mais 15 exceções escritas. O "26" vem de LEGIBILIDADE-01.
Mudar: "só os 20 tokens de `theme.css:21-54`, escritos como `@token`; o portão é
`tests/unit/test_paleta_unica.py`". A regra do rosa continua literal: `theme.css:28`.

**C2. O jargão banido tem oito frases, não seis palavras — e há uma terceira lista.**
Dizia: CONFIG-01:51-52, "jargão banido inclui daemon, systemd, uinput, JSON, polling, throttle".
Hoje: `scripts/validar-palavra-de-tela.py` conhece **oito frases** em `JARGAO_BANIDO` (`:85-94`):
"daemon offline", "daemon pausado", "uinput disponível", "Restaurar Default", "Travar Proton
validado", "Aplicar correções", "Testar criação de device virtual", "Gamepads:". O alcance é
declarado e estreito: **só o `main.glade`** (`:14-18`, `:61`) — rótulo montado em Python passa
livre, de propósito. E existe uma lista DIFERENTE, em
`tests/unit/test_glade_vocabulario_leigo.py:39-63`, que reprova em `label` e `tooltip-text`:
`systemctl`, `systemd`, `rc=`, `.service`, `Unit:`, `Motor fraco`, `Motor forte`, `weak`,
`strong`, `Throttle`, `throttle`, `Política de rumble`, `Preview do perfil`, `JSON`, `Anti-storm`
e **`sudo`**.
Mudar: citar as duas listas com endereço, dizer que a lista de seis palavras é regra de casa SEM
portão, e acrescentar o que o portão de fato cobra e a aba vai encostar: **rótulo do glade tem de
começar em maiúscula** (`EXCECOES_DE_MINUSCULA`, `:67-83`), e uma entrada de exceção que envelhece
também reprova (`:232-245`, DIVIDA_DA_PALAVRA_01 em `:101-118`).

**C3. `_("...")` no Python contradiz o molde.**
Dizia: CONFIG-01:50, "`_("...")` no Python".
Hoje: o molde que a sprint manda copiar NÃO usa `_()`: `home_actions.py` não importa
`utils.i18n`. Dos 21 módulos de `app/actions/`, só três importam (`lightbar_actions.py`,
`footer_actions.py`, `status_actions.py`).
Mudar: decidir e escrever — ou string crua como o molde, ou importar o `_`. Não deixar a sprint
pedir uma coisa e o molde mostrar outra.

**C4. O `.glade` é isento do portão de acentuação; o `.py` novo não.**
Dizia: nada.
Hoje: `scripts/validar-acentuacao.py:434` tem `.*\.glade$` em `WHITELIST_PATTERNS`;
`EXTENSOES_ALVO` (`:439-441`) inclui `.py`, `.sh`, `.md`, `.yml`, `.toml`.
Mudar: `config_actions.py` e o teste novo vêm com acentuação PT-BR completa, docstrings inclusive. <!-- ref-externa: arquivo que esta leva cria -->

**C5. O portão de glifos aceita os marcadores do mockup.**
Dizia: nada.
Hoje: testado — o sinal de conferido U+2713 e o triângulo U+26A0 passam; o U+2705 reprova com
`U+2705`. Critério em `scripts/validar-glifos.py:6-19` (propriedade `Emoji_Presentation` mais
preservação de Geometric Shapes).
Mudar: o selo pode usar os dois primeiros. Só não pode virar o terceiro na hora de "melhorar".

### D. `scripts/doctor.sh`

**D1. O tamanho e a contagem de funções.**
Dizia: TODO-INTEGRACAO:15 e CONFIG-09:11-13, "4920 linhas e 26 funções de diagnóstico, só em
texto".
Hoje: **5136 linhas**. CONFIG-01 contou **130** definições `nome() {`; CONFIG-09 contou 130
funções de topo, **63** com nome `check_*`, e 64 chamadas de check no `main()` (`:5009-5122`).
CONFIG-09 registra que não conseguiu reproduzir o 26 por nenhuma contagem, e que o subconjunto
"energia USB e rádio" mais "rádio e pareamento (G2)" mais DKMS soma 21.
Mudar: "5136 linhas e 63 checagens". E derrubar a frase "mexe em 4920 linhas" da opção 2 — o
custo real não é o tamanho, é a quantidade de portões que fazem grep de TEXTO no arquivo.

**D2. O `--json` não existe.**
Dizia: TODO-INTEGRACAO item 42, "modo `--json` aditivo"; CONFIG-09:74-77, a prova
`scripts/doctor.sh --json | python3 -m json.tool | head -40`.
Hoje: `grep -c -- '--json'` no arquivo devolve **0**. O laço de argumentos (`:72-82`) trata
desconhecido com `printf '[doctor] aviso: argumento desconhecido: %s\n'` e SEGUE rodando o
diagnóstico de texto; a prova morre com `Expecting value: line 1 column 2 (char 1)`, de um jeito
que parece defeito do pipe.
Mudar: `--json` é construção do zero, não "modo novo de saída" — e a recomendação de CONFIG-09
passa a ser módulo Python mais `check_*` fino. Se ainda assim alguém quiser `--json` no shell, o
aceite tem de incluir que argumento desconhecido passe a ABORTAR.

**D3. Os testes fazem grep no TEXTO-FONTE, não na saída — e isso inverte o custo.**
Dizia: CONFIG-09:56-57, "os testes fazem grep de texto na saída dele
(`test_plataforma_wiring.py:216` assere que a string `RSSI` aparece)".
Hoje: a linha existe, mas `DOCTOR` é o texto-fonte do script, lido em
`tests/unit/test_plataforma_wiring.py:32`. São 51 asserções `in DOCTOR` só nesse arquivo, e **54
arquivos de teste** leem `scripts/doctor.sh`. Além disso
`tests/unit/test_doctor_cobra_as_duas_obrigatorias.py:33-37` EXTRAI funções por regex e as roda
em bash com `bwrap`.
Mudar: inverter o argumento. Acrescentar não ameaça esses testes; **tirar** checagens do doctor
apagaria as strings que 54 arquivos asseram e quebraria o extrator por regex.

**D4. O `hci0` fixo — três relatórios discordam de quanto sobrou.**
Dizia: TODO-INTEGRACAO:43 e CONFIG-02, "`hci0` fixo em `:2555`, `:2563`, `:2823`".
Hoje: os três endereços não abrem no que prometem — `:2553-2556` é um helper de
`busctl get-property`, `:2558-2565` é o bloco MIGRACAO-BLUEZ-DEPRECIADOS-01 de 19/08 e
`:2821-2825` é `check_cmdline_platform`. O `hci0` de watchdog FOI curado: `:2723` e `:3008`
resolvem por `_bt_adaptadores | head -1` (`_bt_adaptadores` definida em `:2583-2603`), e `:2720`
registra `WATCHDOG-HCI-HARDCODE-01: hci1 já aconteceu nesta máquina`.

> **Contradição registrada.** **CONFIG-02 e CONFIG-03** dizem que o item está curado e mandam
> apagá-lo. **CONFIG-01** diz que sobraram DOIS caminhos D-Bus fixos: `/org/bluez/hci0` em
> `:2698` e em `:2704`. **CONFIG-09** diz que sobrou **UM**: `:2704` (`check_bt_radio`, fazendo
> `_dbus_bt_prop /org/bluez/hci0 org.bluez.Adapter1 Discovering`), e que `:2698` é **texto de
> mensagem de cura**, não código vivo — o grep por `hci0` devolve `:2698`, `:2704` e `:2720`.
> Abra as três linhas antes de escrever o item.

Mudar: reescrever o item com o que restar, apagar a parte já curada e citar `:2720` como a cura.

**D5. Duas linhas do exame não existem no doctor.**
Dizia: CONFIG-09:24-30, as seis linhas do exame; e `:18`, "esta sprint não constrói diagnóstico
novo".
Hoje: quatro têm origem (`check_btusb_autosuspend` `:2340`, `check_usb_power_devices` `:2240`,
`check_hid_playstation` `:393`, `check_bt_paired_sem_bonded` `:3213`). **"Firmware dos
adaptadores" não existe em lugar nenhum** (grep por `firmware` só devolve texto de mensagem e o
check de DKMS). **"Vizinhança das portas" também não**: o que existe é `suggest_port` (`:4904`),
modo à parte que sai antes do `main`, diz "diagnóstico NEUTRO" e ensina que o storm -71 é
port-independente.
Mudar: a sprint reaproveita quatro e CONSOME uma quinta de CONFIG-02. "Firmware" ou vira
diagnóstico novo declarado, ou sai da lista. Sem isso, CONFIG-09 promete seis e entrega quatro.

**D6. Duas checagens de pareamento precisam de sudo, e a GUI é sudo-zero.**
Dizia: nada.
Hoje: `check_bt_bonds_persistidos` (`:3050-3053`) e `check_bt_sdp_cache_envenenado` (`:3086-3089`)
começam com `sudo -n true` e desistem sem ele. E `/var/lib/bluetooth` é árvore 700 (medido:
`drwx------ root root`).
Mudar: a linha "Pareamentos salvos" não pode afirmar "Todos os controles têm pareamento salvo e
válido". O caminho sem root é `check_bt_paired_sem_bonded` (`:3213-3231`), que pergunta pelo
D-Bus se algum device está `Paired: yes` com `Bonded: no` — pergunta mais estreita e verdadeira.

**D7. Não porte a tabela de rótulos de PCI.**
Dizia: CONFIG-02, "a lógica de dois rádios no mesmo controlador USB já existe em shell".
Hoje: `bus_to_label()` (`:4834`) é portável; `pci_label()` (`:4823-4830`) traduz apenas
`*0c:00.3` para "CPU/Ryzen" e `*02:00.0` para "chipset", que são os controladores de OUTRA
máquina — nenhum dos dois casa a bancada de hoje.
Mudar: copiar o algoritmo, nunca a tabela.

### E. Vibração, orçamento e giroscópio

**E1. Quatro rótulos, cinco chaves.**
Dizia: CONFIG-05:7-10, "Economia / Balanceado / Máximo / Auto. `RumbleConfig.policy` já grava
esses valores".
Hoje: `src/hefesto_dualsense4unix/profiles/schema.py:336` grava
`Literal["economia", "balanceado", "max", "auto", "custom"] | None`. São CINCO chaves e a terceira
é `"max"`, não `"Máximo"` — que é rótulo de tela, mapeado em `_POLICY_LABEL`
(`app/actions/rumble_actions.py:79-84`). `extra="forbid"` está em `schema.py:333`. E existe
`custom` mais `custom_mult` com teto `RUMBLE_CUSTOM_MULT_MAX = 2.0` (`schema.py:76`), que acima
de 1.0 AMPLIFICA.
Mudar: tabela explícita CHAVE para RÓTULO, `custom` marcado como fora do orçamento, e a frase de
risco certa — gravar a string "máximo" faz o `extra="forbid"` recusar o perfil inteiro na carga.

**E2. Economia é 30 %, não 40 %.**
Dizia: CONFIG-05:32-34, `TOOLTIPS.md:107` e o mockup em `:405` e `:410`, "a vibração chega ao
controle com no máximo 40 % da força".
Hoje: `RUMBLE_POLICY_MULT` (`src/hefesto_dualsense4unix/daemon/subsystems/rumble.py:82-86`) é
`{"economia": 0.3, "balanceado": 1.0, "max": 1.5}`. A tela JÁ diz 30 % (`main.glade:1654`), e
`tests/unit/test_politica_de_vibracao_a_escada_que_amplifica.py:81` afirma o 0.3 com a nota "se
este voltar a 0,7, o tooltip do botão volta a mentir".
Mudar: 30 % nos três lugares, e nunca escrever o número à mão no código novo — derivar de
`RUMBLE_POLICY_MULT`, como `_POLICY_MULT` (`rumble_actions.py:65-68`) e
`tests/unit/test_por_unidade_01_todas_as_abas.py:191-196` já fazem.

**E3. Máximo é 150 %, e satura.**
Dizia: mockup `:411`, coluna Máximo igual a 100 %; `TOOLTIPS.md:109`, "tudo como o jogo pedir".
Hoje: `RUMBLE_POLICY_MULT["max"] = 1.5` — amplifica 50 % acima do que o jogo pediu, e satura em
255 a partir de 170. O glade escreve isso literalmente em `main.glade:1767-1770`, e
`test_politica_de_vibracao_a_escada_que_amplifica.py:85-88` morde.
Mudar: a célula vira **150 %**, e a dica do botão diz a saturação (SATURA-01, 11/08/2026).

**E4. O Auto não lê transporte.**
Dizia: CONFIG-05:40-43, `TOOLTIPS.md:110` e mockup `:408`, "controle no cabo joga em Máximo;
controle em rádio abaixo de 20 % de bateria cai para Economia".
Hoje: `_effective_mult` (`src/hefesto_dualsense4unix/core/rumble.py:51`, ramo do auto em
`:100-121`) lê só `battery_pct`: acima de 50 % vale 1.0, entre 20 e 50 % vale 0.7, abaixo de 20 %
vale 0.3. O docstring em `:78-86` registra a decisão de 11/08/2026 ("o auto existe para POUPAR
bateria — amplificar seria fazer o oposto do que ele promete", teto 1.0). O rótulo que promete
isso na tela tem dono único declarado: `rumble_policy_auto_label` (`main.glade:1762-1774`), cujo
comentário manda "quem mexer nesta escada mexe no texto que a promete na tela". A metade dos 20 %
está certa. E "controle no cabo" é legível — `Transport = Literal["usb","bt"]` em
`src/hefesto_dualsense4unix/core/controller.py:18`, campo em `:120`, método abstrato em `:197`.
Mudar: escada real 100/70/30, OU declarar que CONFIG-05 muda a regra e listar como entrega
obrigatória a edição de `main.glade:1773-1774`, `main.glade:1678` e `core/rumble.py:73-86`.

**E5. Não existe ajuste de taxa de giroscópio.**
Dizia: mockup `:414`, "Giroscópio | Vem de: No jogo | 60 Hz | 125 Hz | 250 Hz".
Hoje: grep por `gyro_rate`, `gyro_hz`, `sample_rate` e `report_rate` em `src/` volta vazio, e
`profiles/schema.py` não tem campo de Hz. O único teto real é `MOTION_EMIT_MAX_HZ = 250.0`
(`src/hefesto_dualsense4unix/core/physical_report_reader.py:246`), que vira `self._min_interval`
no construtor (`:549`, cálculo em `:555`), **sem setter**; os dois únicos construtores omitem o
argumento (`daemon/subsystems/gamepad.py:1726` e `daemon/subsystems/coop.py:1118`). A aba "No
jogo" MEDE o giroscópio, não o configura.
Mudar: cortar a linha, ou reescrevê-la como "o orçamento passa `max_hz` na construção, o Máximo
vale 250 (o default de hoje) e a mudança só vale no próximo start do gamepad virtual".
"Vem de: No jogo" está errado nos dois casos.

**E6. O microfone por rádio não tem tela.**
Dizia: mockup `:413`, "Microfone por rádio | Vem de: Emulação".
Hoje: é o subsystem `src/hefesto_dualsense4unix/daemon/subsystems/bt_mic.py`, ligado por opt-in
(env `HEFESTO_DUALSENSE4UNIX_BT_MIC=1` ou `config.bt_mic_enabled` lido por `getattr`, `:79` e
`:23-25` — o campo pode nem existir no `DaemonConfig`). Grep por `bt_mic` em `app/` e no
`main.glade` só acha um comentário (`app/widgets/controller_card.py:540-541`). A aba Emulação não
o toca.
Mudar: "Vem de: nenhuma aba ainda", marcada como dependente de um interruptor que não existe; ou
cortar. Nota a favor de mantê-la depois: é a única linha da tabela com custo de recurso MEDIDO
(`bt_mic.py:15-22`).

**E7. `_sync_mouse_mode_gate` deixou de ser o padrão.**
Dizia: DECISOES-ABERTAS D-A5:171-172, "o padrão de gate insensível já existe
(`_sync_mouse_mode_gate`), mas usá-lo aqui esconderia a causa".
Hoje: a função existe e está intacta (`src/hefesto_dualsense4unix/app/actions/mouse_actions.py:97`).
Mas o padrão que a casa fixou depois é outro: `d614d04f` (19/08/2026) decidiu, com as três opções
na mesa, que a GUI NÃO impede o clique — o daemon recusa no corpo da resposta. Vocabulário em
`daemon/subsystems/rumble.py:369-388`; e a GUI precisou de leitor próprio, `rumble_set_checked`
(`app/ipc_bridge.py:432-443`), porque `_call_checked` (`:286-315`) só lê `CODE_INVALID_PARAMS` e
a recusa no corpo chegava à tela como sucesso.
Mudar: D-A5 não muda de decisão, mas a sprint cita `d614d04f` como precedente de implementação e
**proíbe explicitamente** `set_sensitive(False)` no slider da Lightbar.

### F. Controles externos

**F1. O endereço de `write_lightbar_slot`.**
Dizia: CONFIG-06:44-45, "`write_lightbar_slot` (`external_leds.py:338-361`)".
Hoje: a função está em `src/hefesto_dualsense4unix/core/external_leds.py:327`, com corpo e
docstring indo até `:373`; `:338-361` cai no meio da docstring.
Mudar: `external_leds.py:327-373`, e acrescentar que a própria docstring (`:337-372`) já carrega a
pergunta da medição 4 com o endereço canônico dela
(`docs/protocol/externos-referencia-canonica.md:1243`).

**F2. A fala do escopo.**
Dizia: CONFIG-06:49, CONFIG-08:15 e D-A2, "`external_controllers.py:11-14` guarda a fala".
Hoje: a fala está em `src/hefesto_dualsense4unix/app/actions/external_controllers.py:9-10`; o
parágrafo termina em `:13` e `:14` é o fecho do docstring. CONFIG-03, CONFIG-06 e CONFIG-08
concordam que `:11-14` está errado; CONFIG-08 escreve o intervalo como `:9-13`, os outros dois
como `:9-10`.
Mudar: `:9-13` para o parágrafo, `:1-14` para o docstring inteiro, e a NOTA DATADA entra depois
de `:13`, antes do fecho de `:14`.

**F3. O modo do controle É deduzido.**
Dizia: CONFIG-06:17, "modo em que o controle foi ligado (XInput / DInput / Switch / macOS) — não é
anunciado de forma confiável".
Hoje: os quatro modos estão canonizados em `docs/protocol/externos-firmware-e-modos.md:146-149`,
cada um com combo, VID:PID por cabo, VID:PID por rádio e driver; e o produto já deduz —
`input_mode()` (`external_controllers.py:230`) devolve `nintendo`, `xbox` ou `outro` a partir de
`vid` mais `driver`, e `MODE_SELECTOR_ITEMS` (`:252`) só conhece DOIS ids. A tabela
`externos-firmware-e-modos.md:222-228` é MEDIDA (11/08/2026) e mostra o que o produto vê em cada
um dos quatro modos, com grau ALTA em cinco dos sete pares. Há ainda leitura visual (`:189-192`).
Mudar: o modo não é indeduzível; o que falta é vocabulário (`input_mode` colapsa macOS e D-input
em "outro"). A sprint tem de dizer se entrega rótulo derivado de quatro estados ou declaração — e
declaração é o que a salvaguarda de D-A1 passa a proibir.

**F4. Rótulo dos botões não é `button_labels_for`.**
Dizia: CONFIG-06:17, linha 2 da tabela de entrega.
Hoje: não existe função que escolha rótulo de botão por preferência. `button_labels_for`
(`external_controllers.py:186`) monta o texto do BOTÃO DO SELETOR ("Nintendo 3 · cabo"), não o
desenho A/B/X/Y. O mais próximo é a máscara, e `mascaras_validas()`
(`daemon/subsystems/external_mask.py:201`) devolve exatamente `{'dualsense','xbox'}`, derivadas de
`FLAVORS` em `src/hefesto_dualsense4unix/integrations/uinput_gamepad.py:115-126`.
Mudar: manter a linha (é preferência de pessoa, e a justificativa da sprint está certa), mas
nomear onde ela mora: campo novo do `maquina.json` ou o registro de máscara.

**F5. "Tratar como modelo conhecido" é ambíguo entre duas coisas que existem.**
Dizia: CONFIG-06:17, linha 3.
Hoje: (a) MÁSCARA é como o controle aparece nos jogos — `ExternalMaskRegistry.set_mask`
(`external_mask.py:320`), pronta e sem chamador de produção; (b) IDENTIDADE é como o produto
NOMEIA o aparelho — `friendly_type`/`brand_of` (`external_controllers.py:88` e `:108`), que hoje
erram em três casos MEDIDOS (`docs/protocol/externos-firmware-e-modos.md:230-246`).
Mudar: escolher uma e escrever qual. Se for (a), a sprint ganha o chamador que fecha a lacuna e
precisa de rota IPC nova, que não existe. Se for (b), é conserto de rótulo, não formulário.

**F6. A cor do plástico colide com uma decisão já tomada.**
Dizia: CONFIG-06:17, linha 4, "cor do plástico, quando não foi lida — declaração que persiste".
Hoje: colide com a D-16 de ONDE-A-COR-MORA-01 (`:12`), "da PEÇA, porque a cor mora no APARELHO.
Sem arquivo por endereço"; e a opção (c) daquela página está escrita como "um arquivo por
endereço, que é literalmente o que a D-16 recusou e o que você vetou em 12/08" (`:294-295`). A
recomendação de lá é (b), memória só enquanto o daemon vive.
Mudar: ou a sprint registra que D-16 foi reaberta (com data e por quem, no molde de D-A2), ou a
cor escolhida não persiste em disco e a tela diz isso.

**F7. A numeração das seções.**
Dizia: D-A2 e o INDICE falam em "seção 4" (controles externos) e "seção 5" (a janela).
Hoje: o mockup numera 0 a 4 — `:196` "0. SAÚDE", `:216` "1. OS CONTROLES", `:325` "2. A MESA",
`:399` "3. Orçamento", `:422` "4. A janela"; a tabela "As cinco seções" do INDICE usa a mesma
numeração. **Não existe "seção 5".**
Mudar: CONFIG-06 é a **seção 1**. Corrigir as três chamadas cruzadas antes que alguém implemente a
seção errada — o texto de D-A2 é o que autoriza a sprint, e aponta para um número que não existe.
(CONFIG-03 e CONFIG-07 continuam escrevendo "seção 5" para a janela; a convenção não foi
unificada.)

**F8. `row_homogeneous` não faz o que a sprint diz.**
Dizia: CONFIG-06:72-73, "no GTK isso é `Gtk.Grid` com `row_homogeneous=True` mais um espaçador
expansível antes do último bloco".
Hoje: `grep -rn 'row_homogeneous\|set_row_homogeneous' src/ tests/` devolve ZERO ocorrências em
toda a árvore. E sozinho não resolve: `row_homogeneous` iguala LINHAS entre si; o que iguala cards
LADO A LADO é o card ter `valign=FILL`. O único grid de cards de hoje faz o contrário
(`app/actions/status_actions.py:1307`, `set_valign(Gtk.Align.START)`).
Mudar: a receita são três coisas — `Gtk.Grid` com colunas FIXAS (molde
`app/widgets/segmented_selector.py:280`, `_WRAP_COLUNAS = 3`; nunca `Gtk.FlowBox`, cujo motivo
medido está em `segmented_selector.py:216-231`), cada card com `valign=FILL` e `vexpand=True`, e
um `Gtk.Box()` vazio com `vexpand` antes da última linha (o equivalente do `margin-top:auto` do
mockup, `aba-configuracoes.html:94`). `row_homogeneous=True` só entra se os cinco cards quebrarem
em duas linhas.

**F9. A tabela de cores tem mais nomes do que o mockup mostra — e os relatórios discordam de
quantos.**
Dizia: TODO-INTEGRACAO:31 e `:10`, "a lista de seis cores existe em `cor_do_plastico.py:159-165`".
Hoje: `scripts/ensaios/cor_do_plastico.py:158` abre o dicionário `CORES`. **CONFIG-01** conta
"16+ nomes oficiais Sony (`00 White` até `12 Chroma Pearl`, `30`, `Z1` a `Z3`)", com as seis do
mockup em `:159-164` e `:165` já sendo `"06": "Grey Camouflage"`. **CONFIG-06** conta **21 nomes**
(`:158-170`) e cita "Volcanic Red" como código `07` em `:167`.
Mudar: "a tabela oficial está em `cor_do_plastico.py:158`; as seis do mockup (Branco, Preto,
Vermelho, Rosa, Roxo, Azul) são um recorte próprio dos códigos `00` a `05` (`:159-164`)". Conte
os nomes com o arquivo aberto antes de escrever qualquer número. E o campo livre "Outra" do
mockup (`aba-configuracoes.html:314`) propõe digitar "Volcanic Red", que já está na tabela — ele
deve abrir os nomes restantes, não convidar a redigitar.

**F10. A prova de trabalho de CONFIG-06 já está vermelha, por outro motivo.**
Dizia: `pytest tests/unit/ -k "external or mascara" -q`.
Hoje: sai `1 failed, 370 passed, 1 skipped, 10195 deselected, 1 xfailed`. O reprovado é
`tests/unit/test_docs_mac_anonimato.py::test_nenhum_mac_real_completo_sem_mascara_no_repo`,
acusando `GUIA-RADIO-DA-SALA.md:255` e `:266` — arquivo **untracked** na raiz.
Mudar: registrar a linha de base ANTES de começar, e usar `.venv/bin/python`. Ver 2.2.

### G. A janela: bandeja, escala, autostart, commits

**G1. A bandeja viva não é a que a leva cita.**
Dizia: INDICE:212-213 e CONFIG-07:20-21, "`integrations/tray.py` usa AppIndicator, tentando
`AyatanaAppIndicator3` e depois `AppIndicator3` (`:50-61`)".
Hoje: a faixa existe e contém o par de tentativas
(`src/hefesto_dualsense4unix/integrations/tray.py:50` comentário, `:51` a tupla, `:59-61` a
mensagem de falta), mas isso é `probe_gi_availability()`, que só responde "a biblioteca importa?".
Quem a GUI usa é `src/hefesto_dualsense4unix/app/tray.py`: `app.py:49` importa `AppTray` e
`_desktop_is_cosmic` de lá; a detecção de COSMIC está em `app/tray.py:90-98` (CONFIG-01 escreve
`:91-98`, CONFIG-07 escreve `:90`) e o par de tentativas próprio está em `_resolve_indicator`
(`app/tray.py:559-571`). O `app/tray.py` tem 24 KB contra 6,6 KB do de `integrations`.
Mudar: citar os dois com papéis distintos. Todo o trabalho de CONFIG-07 (deferimento, sondagem do
watcher, aviso) mora em `app/tray.py`.

**G2. A bandeja só sonda o watcher em COSMIC.**
Dizia: nada.
Hoje: `app/tray.py:178` (`if _desktop_is_cosmic():` em `start()`, que defere) e `:258` (o mesmo no
fim de `_start_deferred()`) são o único caminho até `_probe_watcher_with_retries` (`:266`) e
`_maybe_notify_tray_missing` (`:289`). Em GNOME o indicator é criado e ninguém pergunta se há
watcher — é exatamente o "sumir calado" que a sprint quer curar. O comportamento está congelado
em `tests/unit/test_tray.py:325 test_apptray_em_gnome_cria_indicator_imediato`.
Mudar: a aba não precisa mudar `app/tray.py` para exibir a ajuda; se quiser também notificar no
GNOME, é ali que a guarda se abre — e o teste de `:325` tem de ser reescrito junto.

**G3. "Tamanho do texto" não é ligar fio.**
Dizia: CONFIG-07:11 e TODO-INTEGRACAO item 7, "backend pronto, escala 0-8, sem tela. É ligar fio,
não construir".
Hoje: a faixa 0-8 está certa (`app/theme.py:46 ESCALA_PADRAO = 3`, `:50 ESCALA_MAXIMA = 8`) e a
gravação é uma chave (`app/gui_prefs.py:63 set_pref`). Mas `escala_fonte()` guarda o valor em
`_escala_aplicada` (`:66`, `:76-78`) e devolve o cache nas leituras seguintes; `apply_theme()`
(`:124`) roda uma vez só (`app.py:246`), acrescenta o provider sem nunca chamar
`remove_provider_for_screen` (só há `add_provider_for_screen` em `:177`) e SOMA o delta ao
`gtk-font-name` que já está posto (`:150-156`). Chamar de novo **compõe** — medido em 13/08:
quatro chamadas levaram a fonte de "Fira Sans" a 12,25, 14,5, 16,75 e 19 pontos
(`tests/unit/test_o_status_nao_samba_no_ritmo_do_giroscopio.py:41-46`). O repositório já registra
que a chave "só é alcançável editando JSON à mão, com reinício"
(`docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md:481-486`).
Mudar: "backend de leitura pronto (0-8, padrão 3); a gravação é uma chave. Falta decidir se a
escolha vale ao reabrir o Hefesto (barato) ou na hora (exige um `reaplicar_escala` que remova o
provider anterior e reponha o `gtk-font-name` original antes de somar)."

**G4. "Ambiente da área de trabalho" não tem leitor público nem persistência.**
Dizia: CONFIG-07:13, "lido de `XDG_CURRENT_DESKTOP`, exibido, corrigível".
Hoje: os únicos leitores são privados ou de outro assunto — `app/tray.py:90 _desktop_is_cosmic()`,
`app/tray.py:100 _painel_recolore_simbolico()`, `app/main.py:33-38` (que só decide `GDK_BACKEND`)
e `integrations/window_backends/wayland_portal.py:149`. E `app/gui_prefs.py:24-26` tem exatamente
uma chave de padrão (`advanced_editor`) — não há chave de ambiente.
Mudar: "a construir: leitor público novo mais chave nova em `gui_preferences.json`". Não é fio
solto; são ~60 linhas de módulo novo.

**G5. "Ligar junto com o computador": a sprint e o mockup discordam.**
Dizia: CONFIG-07:14, "já existe na aba Sistema — aqui só espelha, com link".
Hoje: o controle de origem existe (rótulo `main.glade:2609`, interruptor
`daemon_autostart_switch` `:2613`, dica `:2614`, handler
`app/actions/daemon_actions.py:1933`, reconciliação sob `_daemon_autostart_guard` em `:1573-1579`
e `:2073-2075` a partir de `systemctl --user is-enabled` em thread worker). Mas o mockup aprovado
desenha uma caixa **EDITÁVEL** (`aba-configuracoes.html:445`).
Mudar: escolher antes de codar. Espelho somente-leitura mais botão "Abrir em Sistema" cumpre o
texto e o dono único de D-A5; caixa editável cria um segundo escritor para o mesmo fato.

**G6. A caixa "Mostrar ícone na barra do sistema" não tem backend.**
Dizia: o mockup a desenha.
Hoje: `app/app.py:1402-1410` constrói e inicia `AppTray` incondicionalmente dentro de `run()`;
`grep -rn "NO_TRAY\|no_tray" src/` volta vazio.
Mudar: é feature nova, não fio solto. E mexe em segurança de uso — `_has_persistent_access`
(`app/app.py:486-503`) decide se fechar a janela esconde ou encerra o app.

**G7. Em COSMIC há DOIS caminhos de bandeja.**
Dizia: "no COSMIC aparece sozinho".
Hoje: o AppIndicator (`app/tray.py`) e um applet COSMIC nativo em Rust instalado por padrão em
sessões COSMIC (`install.sh:3125-3134`, pasta `packaging/cosmic-applet/`). E quando o watcher
falta, `app/tray.py:289-341` já escreve a frase certa: "Habilite o applet 'Area de status' no
cosmic-panel (Configurações > Painel)".
Mudar: a ajuda do COSMIC não é "nada a fazer" — é "habilite o applet Área de status", e ela já
existe escrita.

**G8. Os hashes de commit citados não existem em `dev`.**
Dizia: INDICE (Portabilidade item 1), "já tratado por `d6b9396`"; CONFIG-01 e CONFIG-08, "o commit
`911d099` tratou".
Hoje: `git merge-base --is-ancestor` reprova nos dois. São commits do `main` do fork pessoal, e as
histórias divergiram (HEAD `70d28762`).
Mudar: em `dev` os equivalentes são **`b1093087`** ("a janela nunca nasce maior do que a tela
comporta"; cura em `app/app.py:1230 _caber_na_area_util`, chamada em `:1189`) e **`78721e85`** ("o
ícone some da barra quando o terminal empresta o cache do snap"; cura em `app/main.py`,
`_sanear_loaders_do_gdk_pixbuf`).

**G9. O aceite de portabilidade se contradiz com a própria feature.**
Dizia: CONFIG-07:31-33, "as capturas saem iguais em COSMIC e em GNOME".
Hoje: se a seção mostra o ambiente detectado e o marca no seletor, as capturas TÊM de diferir
naquela linha. E `retratar_abas.py` renderiza em `Gtk.OffscreenWindow` (`:1017`, `:1059`), com o
docstring avisando que ela "não passa pelo compositor" (`:38-40`) — a foto não prova nada sobre a
bandeja.
Mudar: aceite medível numa máquina só (as quatro capturas com `XDG_CURRENT_DESKTOP` diferente,
mesmas dimensões, diferença só no botão marcado) mais teste com monkeypatch da sonda (molde
literal em `tests/unit/test_tray.py:369` e `:396`).

### H. Rádio e mesa: sysfs, hub, `HID_PHYS`, microfone

**H1. O sysfs não entrega o MAC do adaptador.**
Dizia: CONFIG-02, "ler sysfs direto da GUI é o caminho... nomeia cada um pelo endereço, nunca por
`hciN`".
Hoje: medido — `/sys/class/bluetooth/hci0/` não tem `address`, o `uevent` traz só `DEVTYPE=host`,
e `_adapter_addresses` (`broker/hidraw_broker.py:165-188`) devolve `set()`. O docstring de
`:166-172` já registrava o sintoma. O endereço existe via BlueZ no D-Bus de sistema, sem root.
Mudar: a decisão de fonte precisa de uma terceira linha. O sysfs entrega TOPOLOGIA (porta, hub,
painel, controlador PCI, VID:PID) e NÃO entrega o MAC. Ver CONFIG-02, PASSO 1.

**H2. O vínculo controle-para-adaptador NÃO é inalcançável.**
Dizia: CONFIG-02:33-36, "o que amarra controle a adaptador é o bond, em `/var/lib/bluetooth` —
árvore 700, e a GUI é sudo-zero por doutrina... Fica registrada como limite".
Hoje: a premissa sobre o bond está certa (medido `drwx------ root root`), mas a conclusão é forte
demais. Para controle CONECTADO por rádio o vínculo está no `uevent` do HID, legível por usuário
comum: `broker/hidraw_broker.py:215-217` fixa a regra D3 ("BT real tem `HID_UNIQ` igual ao MAC do
controle e `HID_PHYS` igual ao MAC do adaptador"), `:281` rejeita nó com esse comentário literal e
`:282-284` compara contra os endereços dos adaptadores.
`src/hefesto_dualsense4unix/core/evdev_reader.py:255-259` reforça. Medido: os `uevent` de
`/sys/class/hidraw/*/device/` abrem como uid 1000.
Mudar: "o vínculo do controle PAREADO (mesmo desconectado) mora no bond e a GUI não alcança; o
vínculo do controle CONECTADO sai do `HID_PHYS` do `uevent`, e é ele que alimenta a coluna 'Em
uso'". Sem isso a coluna fica sem fonte e alguém a inventa. **É o que destrava CONFIG-04** — e
CONFIG-04 registra a ressalva de que não observou isso ao vivo (um só `hci0` e zero DualSense
conectado na hora).

**H3. `bDeviceClass == 09` é regra ampla demais.**
Dizia: CONFIG-02 e INDICE:304, "detectar hub é viável e preferível a perguntar:
`bDeviceClass == 09` no sysfs, com `maxchild` e `bMaxPower`".
Hoje: os hubs-raiz também têm `bDeviceClass=09` — `usb1` a `usb9` aparecem como "xHCI Host
Controller" com `maxchild` entre 1 e 4 e `bMaxPower=0mA`. Como todo aparelho pendura sob um
hub-raiz, a regra ingênua marca TODO adaptador como "em hub". Os hubs de verdade desta bancada
são `8-1` (05e3:0610, USB2.1, `maxchild=4`, `bMaxPower=100mA`) e `9-1` (05e3:0626, USB3.1,
`maxchild=4`, `bMaxPower=0mA`).
Mudar: excluir o hub-raiz pelo NOME do nó (`^usb[0-9]+$`) antes de olhar a classe. E `bMaxPower`
não distingue hub com fonte própria: aqui o USB3 alimentado reporta 0mA. Sem fonte medida, o
campo nasce em "não sei".

**H4. Três coisas se chamam microfone e só uma custa rádio.**
Dizia: CONFIG-04 fala em "o microfone" sem distinguir; o mockup escreve "Em uso: 3 controles · 2
com microfone" (`aba-configuracoes.html:335`).
Hoje: `controllers[].audio.mic_mudo` e `mic_externo` são placa USB e não tocam no rádio — e por
rádio o DualSense não publica placa ALSA nenhuma (medido 15/08); `bt_mic`
(`daemon/ipc_handlers.py:2937-2940`, com `enabled` e `running`) é do PROCESSO inteiro, não por
controle, e o `running` sequer olha as pontes (testa
`getattr(self.daemon, "_bt_mic_subsystem", None) is not None`); as pontes vivas estão em
`integrations/dualsense_bt_audio.py:1131-1133` (`GerenciadorMicBluetooth.pontes`, que é
`@property`), cada ponte guarda o nó em `:821` e o `uniq` está em `:327` — e **nenhum consumidor
em `src/` lê `pontes`**. O fixture confirma: `tests/fixtures/state_full_quatro_controles.json` tem
`bt_mic` no topo e `audio.*` por controle, e nada que amarre uma ponte a um `uniq`.
Mudar: escrever, com estas palavras, que só a ponte agente por HID entra na conta do rádio e que
microfone por cabo entra com ZERO; e a coluna do mockup tem de dizer de qual microfone fala.

**H5. Não existe caminho de interface para "ligar o microfone".**
Dizia: CONFIG-04:34-36, "com um controle sem microfone, a barra mostra folga larga. Ligando o
microfone, a fatia de áudio aparece".
Hoje: o interruptor da ponte FOI REMOVIDO do card em 16/08/2026 por ser perigoso —
`app/widgets/controller_card.py:520-563` explica, e dois portões o seguram fora
(`tests/unit/test_o_interruptor_do_mic_no_card.py` e
`tests/unit/test_o_interruptor_do_mic_por_bluetooth.py`, cujo
`test_o_card_nao_fala_com_o_modulo_da_ponte` em `:101` reprova qualquer linha de
`controller_card.py` que mencione `dualsense_bt_audio`). O único gesto que sobe a ponte hoje é
`HEFESTO_DUALSENSE4UNIX_BT_MIC=1` mais `hefesto-dualsense4unix mic bt`, no terminal
(`daemon/subsystems/bt_mic.py:49`, `src/hefesto_dualsense4unix/cli/cmd_mic.py:80`).
Mudar: reescrever o aceite como ensaio de terminal, com o aviso do PS preso escrito ANTES do
pedido. Ver a primeira armadilha de CONFIG-04.

**H6. `motion_hz` não serve de fonte.**
Dizia: nada — mas é a saída mais tentadora.
Hoje: `core/physical_report_reader.py:246` fixa 250 Hz de cap e `:218-227` avisa que ler "o rádio
é mais lento que 250 Hz, logo o cap sobrou" é a leitura ERRADA. O que
`daemon/ipc_handlers.py:2810-2815` publica é a taxa de ENTREGA ao vpad (EMA, morre em 1 s de
silêncio). `docs/data/mapa-controles.csv` já registrou: "hoje o produto publica `motion_hz` com
teto de 250 Hz e SEM dimensão de quantos controles estão na mesa". E o rádio medido chega a
402,9 Hz.
Mudar: o medidor é DERIVADO, e o selo "derivado da especificação" na tela é o que torna isso
honesto.

**H7. "o exame é caro" é o motivo errado.**
Dizia: CONFIG-09:66, "roda ao abrir a aba e no botão (o exame é caro)".
Hoje: medido — `bash scripts/doctor.sh --quiet` leva 2,4 s de relógio (1,59 s user, 0,82 s sys),
com 2 FAIL e 5 WARN. Não é caro do jeito que a sprint sugere; é caro o suficiente para nunca rodar
na thread GTK (BUG-GUI-SYSTEMCTL-SYNC-NA-THREAD-GTK-01,
`app/actions/daemon_actions.py:1817-1827`), e o subconjunto que a aba precisa é bem menor.
Mudar: "o exame nunca roda na thread da janela". A regra de não rodar a cada tique continua certa,
pela razão de sempre.

**H8. O estado "atenção": amarelo ou laranja.**
Dizia: CONFIG-09:34-38, "Atenção | Amarelo `@yellow`"; e o mockup usa `--yellow`
(`aba-configuracoes.html:75-76`, `:84-86`).
Hoje: `gui/theme.css:13` fixa o vocabulário canônico — "VERDE confirma, LARANJA alerta, VERMELHO
destrói, CIANO informa". `@yellow` (`#f1fa8c`, `theme.css:31`) é "alerta suave" e serve outro
papel — "era para estar valendo e não está" (`app/widgets/painel_no_jogo.py:141-148`). E a
superfície que JÁ pinta linhas do doctor na janela usa laranja:
`app/actions/daemon_actions.py:754` (`[ OK ]` `#50fa7b`, `[WARN]` `#ffb86c`, `[INFO]` `#8b8fa8`);
`app/actions/profiles_actions.py:1461` e `:1842` chamam `#ffb86c` de "o token de ALERTA da casa".
Mudar: decidir e escrever. As duas passam no `test_paleta_unica.py`, então o portão não decide por
ninguém — hoje há duas descrições do mesmo estado na mesma janela.

**H9. A regra do vermelho tem endereço.**
Dizia: CONFIG-09:40-42 cita "pintar de vermelho ensinaria ela a ver problema onde não há", sem
endereço.
Hoje: a frase é REAL e está viva em
`src/hefesto_dualsense4unix/app/widgets/painel_no_jogo.py:126-131`.
Mudar: só falta o endereço — `painel_no_jogo.py:130`. É a única citação de doutrina da sprint que
se sustenta sozinha; vale ancorá-la.

### I. Persistência: a camada, o `maquina.json`, a máscara

**I1. A camada de configuração fora de perfil já existe.**
Dizia: CONFIG-03:7-8 e o INDICE, "não existe lugar para configuração que não seja de perfil. Esta
sprint cria a camada, e por isso é a maior da leva".
Hoje: existe e tem três inquilinos, todos em `config_dir()` e todos lidos pelo daemon:
`controllers.json` (`daemon/subsystems/external_identity.py:102`, com
`CONTROLLERS_SCHEMA_VERSION` próprio), `controller_masks.json` (`external_mask.py:173`, com
`MASKS_SCHEMA_VERSION = 1` em `:180` e lock de módulo em `:198`) e os sete arquivos-flag de
`utils/session.py`, lidos no boot em `daemon/lifecycle.py:729-791`.
Mudar: a premissa vira "não existe lugar para configuração DE MESA"; a sprint passa a
"acrescentar o terceiro arquivo dessa camada, no molde já pago", citando `external_mask.py:89-116`.

**I2. `profiles/schema.py` não é molde de disco.**
Dizia: CONFIG-03:10-11, "schema pydantic com `version: 1`, no molde de `profiles/schema.py`".
Hoje: o arquivo existe (1308 linhas) e o molde do CAMPO está em `:942-948`, mas ele não lê nem
escreve arquivo nenhum. A escrita atômica mora em `src/hefesto_dualsense4unix/profiles/loader.py`
e o portão de versão mais read-modify-write mora em `external_mask.py`.
Mudar: citar os três moldes com o papel de cada um — `profiles/schema.py:942-948` (a forma do
modelo), `profiles/loader.py:1-12` (escrita atômica tmpfile mais rename com filelock),
`external_mask.py:89-116` e `:406-411` (arquivo próprio, versão própria, `_path` com import lazy).

**I3. `daemon.reload` existe, e está fechado.**
Dizia: D-A3, "não existe nada parecido com `config.set`".
Hoje: `daemon/ipc_handlers.py:4106-4138` faz override de config em runtime, mas
`known_fields = set(DaemonConfig.__dataclass_fields__)` em `:4130` e `raise ValueError` para chave
desconhecida em `:4132-4135`.
Mudar: desmente a linha pela metade e ao mesmo tempo fecha a porta do reaproveitamento — método
IPC novo é mesmo necessário.

**I4. `set_mask` sem chamador: o fato é verdadeiro, a expectativa de portão é falsa.**
Dizia: TODO-INTEGRACAO item 5, "`ExternalMaskRegistry.set_mask` pronto e sem chamador desde
15/08".
Hoje: CONFIRMADO sem chamador em produção — `grep -rn set_mask src/ scripts/` devolve só a
definição (`external_mask.py:320`) e uma menção em docstring (`:631`); os únicos consumidores são
`tests/unit/test_external_mask.py` e `tests/unit/test_mascara_por_jogador_01.py`. MAS a entrada de
lacuna foi **APAGADA** em 15/08 porque a máscara ganhou chamador do lado da LEITURA —
`mascara_efetiva()` é consultada na criação de todo gamepad virtual
(`integrations/uinput_gamepad.py:381` e `integrations/uhid_gamepad.py:1025`) — e
`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:706-716` é a lápide dela; o que resta com
lápide própria é `::vpad_ficou_para_tras` (`:718`). E o portão não acusa porque a varredura só
olha nós de TOPO de módulo (`:1120-1128`): método de classe não é candidato.
Mudar: manter o item, reescrevê-lo como "falta o lado da ESCRITA", apontar a lápide, e apagar a
expectativa de que algum portão cobre isso — **nenhum cobre**. O próprio módulo já declara
(`external_mask.py:74-76`) que quem grava a escolha dela é a rota IPC, que ainda só conhece a
máscara da sessão.

**I5. O número de jogador já tem dono e já persiste.**
Dizia: o mockup desenha "Jogador:" no card.
Hoje: handler `_handle_identity_number_set` em `daemon/ipc_handlers.py:1513`, ponte em
`app/ipc_bridge.py:549` (`identity_number_set`), arquivo em `external_identity.py:102`. O handler
ACEITA externo (recebe `external_registry` em `:1590`) e `_set_number_locked` opera "com os dois
registros juntos (a fila é ÚNICA entre DualSense e externos)" (`:1680`).
Mudar: o campo "Jogador" NÃO entra no `maquina.json`. E no card externo é fiação de ~15 linhas,
não trabalho novo. Nota: `app/actions/status_actions.py:1638-1640` diz que os externos NÃO entram
no grupo de rádio do seletor de número da aba Status, de propósito (8BIT-02) — o caminho existe,
mas a superfície de hoje não o oferece para externos.

**I6. A escala tipográfica já tem dono.**
Dizia: o mockup a põe na seção da janela, e CONFIG-03 a considerava campo do `maquina.json`.
Hoje: `app/theme.py:39` (`CHAVE_ESCALA = "escala_fonte"`, gravada em `gui_preferences.json`) e
`theme.escala_fonte()` em `:69`. As únicas chaves em uso hoje no `gui_preferences.json` são
`advanced_editor` (`app/actions/profiles_actions.py:1429`), `escala_fonte` (`theme.py:79`) e a
rota de áudio anterior (`app/audio_saida.py:967`).
Mudar: corta campo do schema de CONFIG-03 — "Tamanho do texto" fica fora. Da seção da janela, só
a correção manual do ambiente é declaração de máquina nova.

**I7. O `Aplicar` tem quatro caminhos até o fim.**
Dizia: nada.
Hoje: `app/actions/footer_actions.py`: `on_apply_draft` em `:208` sai cedo para
`_aplicar_escolha_pendente` em `:250`; `_aplicar_escolha_pendente` (`:307`) tem três callbacks
(`_done` `:360`, `_fail` `:427`, `_sem_relancar` `:450`) e os três chamam `_apply_draft_agora`
(`:461`), além do caminho direto em `:250`.
Mudar: a gravação de D-A4 vai no TOPO de `on_apply_draft`, uma vez. Pendurar em
`_apply_draft_agora` grava duas vezes por clique quando há escolha de modo pendente.

**I8. O `state_full` responde a 20 Hz.**
Dizia: nada.
Hoje: `daemon/ipc_handlers.py:2165-2166` — "Estado completo pra GUI consumir a 20Hz". E o aceite
de CONFIG-02 fixa que a leitura não pode rodar no tique rápido.
Mudar: a GUI lê o `maquina.json` direto do disco ao abrir a aba (função pura, sem IPC), e escreve
pelo daemon. Um escritor só, muitos leitores.

### J. A medição de rádio

**J1. O A/B está no arquivo errado, e falta a terceira linha.**
Dizia: CONFIG-04:15-21, "o que é medido vem do próprio projeto
(`daemon/subsystems/bt_mic.py`, A/B de 25/07/2026)", com o bloco literal
`mic DESLIGADO : input 260.4 Hz ... total 276.7 Hz`.
Hoje: o bloco literal está em `src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py:74-78`
("Medido ao vivo (2026-07-25, A/B no mesmo controle, 3 s por janela)"), com uma TERCEIRA linha que
a sprint omite: `desligado again: input 274.3 Hz  audio 0.0 Hz  total 274.6 Hz`. O `bt_mic.py` tem
só a versão arredondada em prosa (`:14-21`).
Mudar: trocar a fonte para `dualsense_bt_audio.py:74-78` e acrescentar a terceira linha. Ela não é
detalhe: é a prova de que o efeito é de BANDA e não estado preso no firmware (`:86-88` diz isso
com todas as letras), e é ela que sustenta o "a soma quase não se move" do aceite.

**J2. Os 1.600 slots não existem na árvore.**
Dizia: CONFIG-04:11-13, "o número de 1.600 slots/s é derivado da especificação do Bluetooth
Classic".
Hoje: grep por `1600`, `625 µs`, "slot" e "fatia de tempo" em `src/`, `scripts/`,
`docs/protocol/` e `docs/data/` não acha nada com este sentido — só
`app/mic_monitor.py:90 _TAXA_HZ = 16000` (outra coisa), um recorte de imagem, "~1600 linhas de
journal", `hid-nintendo.c:1600` e um teto de backoff em ms. O único lugar do repositório onde
1.600 aparece com este sentido é o mockup (`aba-configuracoes.html:366-367`) e `TOOLTIPS.md:102`
— e o `mockup/README.md:29-33` avisa que "os endereços, os `831 / 1600` e os VID:PID são
ilustração".
Mudar: a sprint tem de ESCREVER a aritmética. Ver CONFIG-04, PASSO 0.

**J3. Os 381,54 contra 191,40 têm endereço, e vêm com um envelope maior.**
Dizia: CONFIG-04:25-27, "dois controles no mesmo adaptador diferiram por quase o dobro na mesma
janela (381,54 contra 191,40 Hz); `mapa-controles.csv` registra como ABERTO".
Hoje: CONFIRMADO, e sem endereço na sprint. Os brutos estão em
`docs/data/ensaios-brutos/2026-08-15-E2-taxa-dos-oito-nos.csv:6` (hidraw9, 7631 relatórios em
20,000 s, 381.54 Hz) e `:8` (hidraw11, 3828, 191.40 Hz). O "mesmo adaptador" e o ABERTO estão nas
colunas `radio_detalhe` e `nota` da linha `combinacao.cabo_e_radio.taxa` de
`docs/data/mapa-controles.csv`.
Mudar: acrescentar os dois endereços, e acrescentar o dado mais duro contra um número único — o
ENVELOPE do dia: 354,4-402,9 Hz num controle e 173,2-232,3 Hz no outro em 12 janelas de 15 s
(E-6), e 157,8-402,9 Hz somando o dia depois da troca de braços de 19h32; e que a desigualdade
SOBREVIVEU à troca de unidades ("não é defeito de um aparelho, é comportamento do braço").

**J4. O rosa saiu do medidor, e um documento ficou para trás.**
Dizia: `mockup/README.md:16-18`, "o rosa aparece em exatamente dois lugares no mockup: o
sublinhado da aba ativa e a faixa de microfone no medidor de rádio".
Hoje: o HTML real, em `aba-configuracoes.html:368`, desenha as duas fatias em `var(--purple)` e
`var(--cyan)` — roxo e ciano, zero rosa. `theme.css:25` é cyan `#8be9fd`, `:28` é pink `#ff79c6`,
`:29` é purple `#bd93f9`. O INDICE:291-293 já registra a correção.
Mudar: corrigir `mockup/README.md:16-18` para "o sublinhado da aba ativa" e ponto. Quem
implementar lendo só o README pinta a fatia de áudio de rosa e reintroduz a violação já curada — e
`test_paleta_unica` não pega, porque `#ff79c6` é cor legítima, só no papel errado.

### K. Provas de trabalho que passam sem a sprint

**K1.** CONFIG-02: `pytest tests/unit/ -k config -q` coleta **233 testes que já existem hoje** (de
10350), nenhum da aba — o filtro casa `DaemonConfig`, `RumbleConfig`, `gui_prefs`,
`config_de_perfil`. Trocar por arquivo NOMEADO.
**K2.** CONFIG-03: `pytest tests/unit/ -k "maquina or config" -q` devolve
`247 passed, 1 skipped, 10320 deselected`, nenhum sobre `maquina.json`; `-k "maquina"` sozinho
seleciona 14 testes alheios. A prova passaria verde com a sprint entregue vazia.
**K3.** CONFIG-06: `pytest tests/unit/ -k "external or mascara" -q` sai **vermelho hoje por motivo
alheio** (ver F10).
**K4.** CONFIG-09: `scripts/doctor.sh --json | python3 -m json.tool` não roda (ver D2).
**K5.** CONFIG-01 e CONFIG-02: `retratar_abas.py ... --mesa-cheia` sai VERDE com a aba nova vazia
ou com a foto no nome errado (ver A5 do roteiro de CONFIG-01 e o PASSO 8 de CONFIG-02).
**Mudar, nos quatro casos:** prova por caminho de arquivo e por nome de artefato, nunca por
ausência de erro. É a família que PONTO-A-PONTO-01 nomeia: "um portão que olha para o lugar errado
é pior que portão nenhum, porque encerra a busca".

### L. O alcance real dos portões

**L1. `validar-citacoes-de-linha.py` só varre `docs/protocol/`.** `:63-68` declara a
conservadoria: "Em `docs/process/` uma sprint cita a árvore do dia em que foi escrita, e cobrá-la
seria pedir que o registro histórico se atualizasse sozinho"; `PASTA` em `:82` e `documentos_de()`
em `:193-195` fazem `glob("*.md")` de uma pasta só, e o modo por argumento (`:214-225`, `:218-225`)
descarta `.md` de outro pai. Rodado com a leva no disco: `OK: 122 citação(ões) em 11
documento(s)`, rc 0.
**L2. `validar-referencias-docs.py` cobre `docs/process/`** para existência de ARQUIVO (REGRA 1,
`:154`, valendo para `docs/` inteiro menos `docs/history/`, `docs/research/` e
`docs/process/agentes/`; alvo geral em `:578-598`, `docs/**` mais `README.md`). `.json` não está
na lista de sufixos, então `maquina.json` nunca é cobrado.
**L3. `validar-palavra-de-tela.py` só varre o `main.glade`** (`:14-18`, `:61`, `:288-289`,
`:293-294`) e cobre `label`, `title`, `text` e `tooltip_text` (`:62`), reprovando primeira letra
minúscula (`:174-186`).
**L4. `promessa-sem-caminho` só enxerga def/class de TOPO de módulo** (`:1104-1176`, `:1119-1128`),
pula nome que comece com `_`, isenta CONSTANTES de módulo (`:64-72`: "uma constante é um VALOR,
não um comportamento"), e **`tests/` NUNCA conta** (`:34-36`). `_TERRITORIOS_DE_PRODUCAO` só varre
`*.py` (`:136-163`, `:972-973`), então **`doctor.sh` não conta como chamador**; heredoc de shell só
vale em `install.sh` e `uninstall.sh` (`:163`).
**L5. `test_nome_citado_como_sprint_existe.py` não conhece nenhum ID desta leva** (ver 2.5, item 1).
**L6. `test_as_fotos_acompanham_a_versao.py` compara TOPOLOGIA de commits**
(`CODIGO_DA_TELA` em `:68-77`, `fotos_em_dia()` em `:93-116`), e passa de graça enquanto os PNGs
estiverem sujos (`fotos_sendo_refeitas_agora`, `:119-140`).
**L7. `test_retrato_das_abas_nao_vaza_dado_real.py` inspeciona o SCRIPT, não a aba** (`:91`,
`:118-145`).
**L8. `check_anonymity.sh` só varre MAC em arquivo BINÁRIO**; a varredura de texto foi delegada ao
pytest (comentários em `:201` e `:328`) — o job `anonymity` pode passar enquanto o `lint-test`
reprova, pelo mesmo arquivo.
**L9. O pre-commit tem dez hooks e não roda nesta máquina.** Ver 2.4.

---

## 6. O QUE FICOU FÁCIL

O que apareceu nos commits novos e já resolve ou encurta parte da leva.

**6.1. A pergunta que CONFIG-01 existe para responder já está respondida, e a resposta é
"não custa nada".** A 11ª aba vazia custa ZERO de largura e ZERO do orçamento de altura — medido
com o glade real, sob Xvfb, comparando o arquivo de hoje com uma cópia em memória que ganha a
página nova. Os dois riscos que justificam a sprint ("onze abas não cabem na tira", "a página nova
estoura o orçamento de largura") estão respondidos ANTES de qualquer código. A sprint continua
sendo o portão estrutural e a fiação, mas o aceite vira negativo: "os números não se mexeram".

**6.2. A aba "No jogo" entra e sai da tira por `hide()`, não por `remove_page`.**
`app/actions/status_actions.py:703-709` faz `alvo.show_all(); alvo.set_no_show_all(True);
alvo.hide()` sobre a página; `ABA_NO_JOGO = "tab_no_jogo_box"` (`:104`); testes em
`tests/unit/test_aba_no_jogo_entra_e_sai_da_tira.py`. Acrescentar uma página no FIM não renumera
nem esconde nada, e o `retratar_abas.py` (que carrega o glade cru) continua mapeando índice para
nome corretamente. Na tela real, com jogo fechado, a tira mostra 10 abas visíveis das 11 páginas.

**6.3. Já existe leitor de topologia USB por sysfs, com injeção de dependência pronta — meio
caminho de CONFIG-02 andado.** `src/hefesto_dualsense4unix/integrations/usb_pai.py`, 233 linhas:
`dispositivo_usb_pai()` em `:68` sobe a árvore até o nó que tem `busnum` e `devnum`, com `existe` e
`real` injetáveis "para o teste montar um sysfs de mentira sem precisar de controle plugado";
`usb_pai_por_uniq()` em `:161` varre `/sys/class/hidraw` com `listar` e `ler` injetáveis;
`RAIZ_SYSFS` em `:59`, `RAIZ_HIDRAW` em `:63`; a régua de universalidade em `:44-51`; o cabeçalho
`:29-32` conta que a lógica veio de `scripts/ensaios/audio_por_transporte.py` e foi PORTADA, não
importada. É o molde exato do módulo novo, resolve de graça o problema da foto (raiz falsa) e
serve de base para o `adaptador_por_uniq` de CONFIG-04 (troca `HID_UNIQ` por `HID_PHYS`). O teste
dele, `tests/unit/test_a_placa_e_o_controle_pelo_usb_pai.py`, injeta callables em vez de montar
árvore de arquivos.

**6.4. O kernel publica a localização física da porta.** Medido:
`/sys/bus/usb/devices/3-3/physical_location/{panel,horizontal_position,vertical_position,dock,lid}`
existe, com `panel=back` para o adaptador BT, para o receptor `6-1` e para os hubs `8-1` e `9-1`;
`panel=unknown` para `3-1`. Também existem `port/connect_type` (`hardwired` para o integrado,
`hotplug` para os de encaixe) e `removable`. "Frente"/"Trás" sai de leitura, não de pergunta —
reforça a tese da aba e encolhe o formulário. Duas ressalvas medidas: aparelho atrás de hub NÃO
tem `physical_location` (`8-1.4` não tem o diretório), e o campo depende de `_PLD` da ACPI.

**6.5. A bancada já tem o cenário que a seção 2 desenha, sem comprar nada.** Medido em
`/sys/bus/usb/devices`: um adaptador BT interno (`3-3`, 0489:e0e4, `panel=back`,
`connect_type=hardwired`), três receptores 2,4 GHz (`3-1` 25a7:fa08, `6-1` 25a7:fa07, `8-1.4`
25a7:fa70 atrás de hub), dois hubs reais (`8-1` USB2.1, `9-1` USB3.1) e a vizinhança apertada
`3-1` com `3-3` no mesmo controlador PCI `0000:75:00.4`. O aceite "numa máquina com um adaptador,
a seção lista um" é testável na hora, e a vizinhança apertada tem caso real.

**6.6. `external_mask.py` é o molde completo de persistência que CONFIG-03 precisa, pronto e
testado.** Arquivo próprio (`:175`), versão própria (`:182`), lock de módulo (`:199`), `_path()`
com import lazy (`:406-411`), save read-modify-write que **preserva o que não entende**
(`:114-118`, `:509-523`), recusa a gravar quando a versão do disco não é a nossa (`:502-508`), e
os quatro motivos de não fazer bump no arquivo irmão listados em `:96-108`. A bateria
correspondente, `tests/unit/test_external_mask.py` (373 linhas), vigia as quatro propriedades
listadas em `:8-15`. Copiar isso elimina a parte de projeto e traz de graça a decisão mais difícil
(o que fazer com um arquivo de versão futura).

**6.7. Existe um caminho de diagnóstico em Python com o contrato de escrita já fixado.**
`src/hefesto_dualsense4unix/integrations/storm_doctor.py:431` (`storm_report(home=None, *,
quirks_text=None, dropin_dir=None, rules_dir=None, snd_quirk_text=None)`), consumido por
`src/hefesto_dualsense4unix/cli/cmd_doctor.py:87-94`, com o cabeçalho declarando a regra em
`:5-6`: "cada função recebe os paths por parâmetro (default igual ao sistema real) para testes com
fixtures". É o contrato do módulo de CONFIG-09, palavra por palavra.

**6.8. O padrão "módulo Python publicando JSON que o doctor consome" já existe três vezes.**
`integrations/sentinela_do_wrapper.py:212` ("Forma JSON — é o que o `doctor.sh` consome
(`--censo`)"), consumido por `scripts/doctor.sh:1612-1633` (`check_sentinela_wrapper`) e pela
janela em `app/actions/carona_do_wrapper.py:286`;
`integrations/prontuario_dos_jogos.py:505` ("Forma JSON — o que a GUI e o `doctor.sh` consomem"),
com a doutrina em `:203-205` ("o que impede as duas de divergirem não é a disciplina de quem
edita: é o portão `test_ponte_confirmada_01`, que compara as DUAS leituras sobre a mesma pasta de
perfis e reprova se discordarem"); e `integrations/proton_pin.py:1225 --report`, consumido por
`scripts/doctor.sh:3234-3262`. CONFIG-09 não precisa desenhar nada: copia a forma, e o custo de
mexer no doctor cai para quase nada.

**6.9. A superfície que CONFIG-09 quer construir já existe funcionando na aba Sistema.** O cartão
"Saúde do sistema" (`main.glade:2694` `storm_card`, rótulo `:2706` `storm_diag_label`, id travado
por `tests/unit/test_glade_vocabulario_leigo.py:75-96`) é pintado por
`app/actions/daemon_actions.py:731 _refresh_storm_diag`, que roda `storm_doctor.storm_report()` em
thread worker, mapeia `[ OK ]`, `[WARN]` e `[INFO]` para cor (`:754`) e devolve por
`GLib.idle_add(self._apply_storm_diag, ...)` (`:772`). O molde de implementação está pronto e
testado — resta a decisão de produto (ver seção 7).

**6.10. O molde do "teto visível" já existe e funciona.** `rumble_policy_aviso`
(`main.glade:1806-1813`: `visible=False`, `no-show-all=True`, `use-markup=True`), preenchido por
`texto_do_alcance_da_intensidade(state) -> str | None` (`app/actions/rumble_actions.py:194-273`),
cujo docstring dita a ordem das perguntas e a regra que o orçamento herda: "afirmar 'não alcança'
com o campo ausente seria inventar um defeito — 'não sei' e 'não chega' mandam caçar em lugares
opostos". É o que CONFIG-05 copia para a linha "limitado a 25 % pelo orçamento".

**6.11. `_effective_mult` é o funil único dos três caminhos de vibração.**
`src/hefesto_dualsense4unix/core/rumble.py:51`, com os três chamadores em
`daemon/ipc_rumble_policy.py:51-58`, `daemon/subsystems/gamepad.py:1129-1136` e
`daemon/subsystems/rumble.py:263`, os três saturando com a mesma conta. Um teto escrito ali vale
para tudo: um só ponto, um só teste de mordida.

**6.12. O molde de tabela somente-leitura montada em código já existe e é pequeno.**
`app/actions/input_actions.py:270` (`install_input_tab()`) e `:280`
(`_install_key_bindings_treeview()`, 26 linhas inteiras): pega o `GtkTreeView` pelo id do glade,
sai cedo se for `None`, é idempotente, monta `Gtk.ListStore` e `append_column`. E o `theme.css` já
estiliza `treeview` (`:435-443`) e tem `@elevated` descrito como "cabeçalho de tabela" (`:45`).

**6.13. O molde da barra do medidor já existe, e as duas cores já estão na paleta autorizada.**
`app/widgets/sensor_widgets.py:1-14` fixa a anatomia ("as REGRAS moram em funções puras,
testáveis sem toolkit, e o desenho num `Gtk.DrawingArea` que só pinta o que a função pura
decidiu"), o módulo já tem o par real/stub para rodar sem GTK (`:209`, e o stub em `:614`), e
`SpeakerBar` (`:466-500`) é uma barra horizontal com trilha, preenchimento por fração e contorno —
a forma do `.trilho` do mockup (`aba-configuracoes.html:147-151`), só que com uma fatia em vez de
duas. `#8be9fd` e `#bd93f9` já constam de `tests/unit/test_paleta_unica.py:19-35`.

**6.14. O gancho certo para esmaecer a fita de alvo já existe, com precedente.** A faixa é criada
em `app/actions/status_actions.py:1556-1568` e guardada em `self._target_strip` (`:1568`);
`_set_target_strip_visible` está em `:1734-1752`. E `app.py:960-983` mostra o padrão: em
`_on_notebook_switch_page`, `nome = id_da_pagina(page)` e `set_status_tab_visivel(nome ==
self._ABA_STATUS)` a CADA troca — entrar liga, sair desliga.

**6.15. O `SegmentedSelector` já resolve as duas coisas que a leva mais pede.** `set_tooltips({id:
texto})` (`:97-110`) dá dica por opção, e `limpar_ativo()` (`:115`) deixa o seletor SEM botão
marcado e NÃO emite `changed` — que é literalmente o "nasce em não sei" de D-A1. O modo `wrap=True`
monta grade de 3 colunas FIXAS (`_WRAP_COLUNAS = 3`, `:33`), com o motivo do FlowBox rejeitado
escrito em `:216-231`.

**6.16. O seletor segmentado de modo já está montado em GTK, em dez linhas.**
`src/hefesto_dualsense4unix/app/gui_dialogs.py:760` (`_external_mode_row`) e `:772-802` fazem
rótulo mais `SegmentedSelector` mais `set_active_id` mais `set_sensitive(False)` mais tooltip. É
molde de montagem pronto para copiar em CONFIG-06 — e ao mesmo tempo o alerta de tela duplicada.

**6.17. O número de jogador do card externo é fiação, não construção.** Ver I5. O caminho de ponta
a ponta existe: `identity_number_set` (`app/ipc_bridge.py:549`), handler
(`daemon/ipc_handlers.py:1513`) que aceita externo (`:1590`), fila única (`:1680`), `_norm_uniq`
(`:1580`) que cai no valor cru quando a identidade é volátil. E a disciplina a copiar está em
`app/actions/status_actions.py:1795`, `:1816` e `:1854-1897`.

**6.18. A borda colorida por cor do plástico É construível hoje — o INDICE errou.** Ele afirma que
"não existe um único `CssProvider` por widget em todo o `app/`"; `utils/color_contrast.py:176`
(`tintar_progressbar`) monta um `Gtk.CssProvider` POR WIDGET (`:214`), com
`add_provider(..., STYLE_PROVIDER_PRIORITY_APPLICATION)`, cache anti-rebuild
(`_hefesto_tint_hex`), docstring dizendo "validado ao vivo por render offscreen", e é importado em
produção por `app/widgets/controller_card.py:141-146`. Cai um dos três motivos alegados. E o
terceiro encolheu: `src/hefesto_dualsense4unix/core/led_control.py:146` abre
`_PLAYER_SLOT_COLORS`, o P4 está em `:152` e vale `(255, 0, 128)` — que **não é** o `#ff79c6`
(255,121,198) do `theme.css:28`. São duas cores diferentes; não há colisão literal de token, e a
pergunta que sobra é só se a paleta de identidade da interface remapeia a de hardware.

**6.19. A medição 4 de CONFIG-06 já está metade respondida, com custo revisado e decisão dela
tomada.** `docs/protocol/externos-referencia-canonica.md:1256-1282`: ela olhou o aparelho ("não há
lightbar mas existe led de identificação de player nele também, igual o pro controller"), o SN30
Pro não tem lightbar RGB, e o que resta é "quando o daemon escreve uma cor conhecida na lightbar
do 8BitDo, as quatro luzes do plástico mudam?". Custo: trinta segundos. Trava: o aparelho tem de
estar ligado e no rádio. Decisão dela (resposta 23, 07/08): "preparar, e rodar quando ele estiver
ligado". Grau: SEM PROVA. A sprint pode reescrever a medição como "já preparada, esperando o
aparelho".

**6.20. A medição 3 de CONFIG-06 já tem mecanismo, grau e comando prontos — e responde a medição 1
de graça.** `docs/protocol/externos-firmware-e-modos.md:309-318` explica que
`discover_external_gamepads` só enxerga evdev com `BTN_GAMEPAD`/`BTN_SOUTH`
(`core/evdev_reader.py:628`), que o descritor do 8BitDo no cabo declara `Usage (Joystick)`, e
marca a consequência como previsão de grau MÉDIA com contraindício honesto (o SDL_GameControllerDB
tem entradas para `2dc8:6001/6002`). O comando está em `:336-345`, e o `pid` da saída responde a
medição 1: `6001` é SN30 Pro, `6002` é SN30 Pro+ (`:506`). Duas medições viram um gesto só.

**6.21. O texto que a seção da janela precisa mostrar no GNOME já está escrito e validado em três
lugares.** `docs/usage/instalacao.md:19` (a extensão `ubuntu-appindicators@ubuntu.com` no GNOME
42+), `docs/usage/troubleshooting.md:140-156` (sintoma, diagnóstico
`gnome-extensions list --enabled | grep ubuntu-appindicators`, cura
`gnome-extensions enable ubuntu-appindicators@ubuntu.com` e o aviso de logout/login) e
`install.sh:3090-3122`, que já separa os quatro casos (variável vazia, ambiente não-GNOME,
extensão não instalada, extensão instalada mas desabilitada). A redação já passou pelos portões.

**6.22. A sonda de bandeja que CONFIG-07 precisa já existe, é pública e vale nos dois ambientes.**
`integrations/desktop_notifications.py:169-206 statusnotifierwatcher_available()`, com o docstring
dizendo que em COSMIC quem reivindica é o `cosmic-applet-status-area` e em GNOME é o `gnome-shell`
com a extensão; já consumida em produção (`app/app.py:502`, `app/tray.py:275`). Zero detecção
nova. Único cuidado: `_DBUS_TIMEOUT_SECONDS = 2.0` (`:34`), então fora da thread do GTK.

**6.23. `run_in_thread` já entrega o padrão de worker mais `GLib.idle_add`.**
`src/hefesto_dualsense4unix/app/ipc_bridge.py:153-181`, com os callbacks voltando pela thread GTK
e devendo retornar `False`.

**6.24. A fileira de `GtkToggleButton` declarativa é molde pronto, e resolve os dois pontos cegos
de uma vez.** `main.glade:1641-1686`: `GtkBox` horizontal, `spacing=6`, sem `homogeneous` (com o
motivo escrito em `:1645-1650`), ids `rumble_policy_economia` (`:1653`), `_balanceado` (`:1661`),
`_max` (`:1669`), `_auto` (`:1677`), cada um com `label`, `tooltip-text` e `signal toggled`;
handlers em `app/actions/rumble_actions.py:385-410`. Sendo declarativa, ela é medida pelos dois
portões de geometria e varrida pelo `validar-palavra-de-tela.py`.

**6.25. O `hci0` do watchdog foi curado, e a cura está registrada.** `scripts/doctor.sh:2583-2603`
define `_bt_adaptadores()`, que varre `/sys/class/bluetooth/hci*` com filtro `^hci[0-9]+$` e cai
para `busctl tree org.bluez`; os consumidores resolvem por `_bt_adaptadores | head -1` (`:2723` e
`:3008`); `:2720` registra o motivo. Sobra pouco a fazer no item (ver D4).

**6.26. A máscara ganhou chamador do lado da leitura, e a lacuna encolheu.** `mascara_efetiva()` é
consultada na criação de todo gamepad virtual (`integrations/uinput_gamepad.py:381` e
`integrations/uhid_gamepad.py:1025`), e por isso a entrada de `ExternalMaskRegistry` saiu do
registro de lacunas em 15/08 (`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:706-716`). Se
CONFIG-06 ligar `set_mask`, não precisa mexer no registro.

**6.27. `NOMES_MESA_CHEIA` é derivado de `NOMES`.** `scripts/gui-captura/retratar_abas.py:229-231`
— a aba nova entra no segundo conjunto de fotos automaticamente, e o invariante de tamanho é
guardado por `tests/unit/test_a_mesa_cheia_na_foto.py:429`.

**6.28. O portão de glifos aceita os marcadores do mockup.** Ver C5.

**6.29. A pasta da leva está limpa no portão que de fato roda sobre ela.**
`validar-referencias-docs.py` sobre a leva devolveu "1 referência(s) morta(s) em 13 documento(s)",
a única era `config_actions.py` em CONFIG-01, já reescrita como "A CRIAR"; e a varredura `--all` <!-- ref-externa: arquivo que esta leva cria -->
volta a dizer `OK: 372 documento(s) sem referência morta.` A leva pode ser commitada sem reprovar
o hook nem o job.

**6.30. O VETO 3 nunca foi doutrina geral, o que encolhe a tarefa de D-A1.** O texto original já
dizia "fora de escopo **desta sprint**"
(`docs/process/sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md:498-503`);
foi a paráfrase de DECISOES-ABERTAS que apagou as três palavras. A edição prevista não é revogar
doutrina: é registrar que o veto sempre foi de escopo de sprint e que a leva de 21/08 fixa a regra
geral.

**6.31. Duas curas de portabilidade já entraram na `dev`.** `b1093087` (a janela nunca nasce maior
do que a tela comporta, `app/app.py:1230 _caber_na_area_util`) e `78721e85` (o ícone some da barra
quando o terminal empresta o cache do snap, `app/main.py _sanear_loaders_do_gdk_pixbuf`). A
segunda é a cura de 2.3 já escrita e testada — falta só portá-la para o script de captura.

---

## 7. PERGUNTAS QUE SÓ O DONO RESPONDE

Nenhum agente pode decidir estas. Elas estão agrupadas por sprint, e a primeira vale para todas.

### 7.0. Abrir a leva

O `.github/CONTRIBUTING.md` fixa que **sprint aberta segura a 0.9.5** e que **sprint nova zera o
relógio de duas semanas da 1.0.0**. Some-se a isso: `docs/process/2026-08-19-O-QUE-PRECISA-DE-VOCE`
pede ~40 min de bancada e tem quatro decisões dela pendentes (CONFIG-09 conta sete itens);
**nada da 0.9.4.5 foi visto em hardware**; e PONTO-A-PONTO-01 classifica reconexão de rádio como
P0. Esta é uma leva de NOVE sprints. **Confirme antes do primeiro commit, não depois de
CONFIG-03.**

Nota de fluxo: o `.github/CONTRIBUTING.md` ainda anuncia auto-merge em `main` sem PR (`:9`), o que
o commit `70d28762` (FLUXO-DEV-01) revogou — o trabalho nasce em `dev`. Corrigir o CONTRIBUTING
também é decisão dela.

### 7.1. D-A1 — o escopo da declaração

Confirmar por escrito a regra geral que a leva fixa: **proibido declarar o que o produto pode
medir; permitido declarar o que ele comprovadamente não mede**, com as duas salvaguardas (todo
campo nasce em "não sei"; onde a medição existe, ela pré-preenche). E confirmar que o VETO 3
sempre foi de escopo de sprint (ver 6.30). Isso governa CONFIG-06 inteira.

### 7.2. CONFIG-02 — a fonte do nome do adaptador

Nomear pela **identidade física** (VID:PID mais barramento/porta mais painel, tudo do sysfs, tudo
estável entre boots) ou ler o **MAC do BlueZ pelo D-Bus de sistema**? A segunda opção exige
`--socket=system-bus` e `--system-talk-name=org.bluez` em
`flatpak/br.andrefarias.Hefesto.yml:24-47`, abre a primeira porta de D-Bus do produto e traz risco
de regressão no Flatpak. É decisão de produto, não de implementação, e tem de estar escrita antes
de a sprint começar.

### 7.3. CONFIG-04 — as quatro decisões do medidor

(a) Quantos slots por relatório HID de 78 B (o número não existe na árvore); (b) o medidor usa o
nominal do A/B de 25/07 ou tenta medir, sabendo do envelope de 157,8 a 402,9 Hz; (c) o que conta
como "com microfone" (só a ponte agente por HID); (d) as três palavras de ocupação e os dois cortes
entre elas. E: **autorizar ou não o ensaio da ponte de microfone**, que faz o botão PS disparar
sozinho e a Steam abrir em laço (ver a primeira armadilha de CONFIG-04).

### 7.4. CONFIG-05 — o orçamento

(a) A semântica do teto: `min(mult_da_politica, teto)` ou produto? (b) A regra do Auto muda (cabo
joga em Máximo) ou fica a escada de bateria 100/70/30 decidida em 11/08? Se muda, os três donos da
frase entram na entrega. (c) Em Auto, o teto é móvel — a linha na aba de origem diz "varia com a
bateria" ou não aparece? (d) Numa mesa de cinco controles, qual bateria decide: a menor da mesa,
a do P1? Hoje o código responde a pergunta errada em silêncio. (e) As linhas de **giroscópio** e
**microfone por rádio** ficam no escopo? A primeira mexe num orçamento de `/dev/uhid` com margem
zero medida; a segunda exige um interruptor de GUI que não existe.

### 7.5. CONFIG-06 — os controles externos

(a) O modo é exibição derivada ou declaração? (b) "Tratar como modelo conhecido" é máscara ou
conserto de identidade? (c) A cor do plástico persiste em disco — o que **reabre a D-16** de
ONDE-A-COR-MORA-01 e o veto de 12/08 — ou vale só na sessão? (d) Os cards ficam **lado a lado**
(mockup) ou empilhados (**EMPILHA-01**, decisão dela de 02/08, com o código em
`app/actions/status_actions.py:1278-1291` fazendo `colunas = 1`)? Se ficarem lado a lado, é uma
segunda decisão sobre o mesmo gesto e precisa ser registrada como tal. (e) Qual seletor de modo
sobrevive: o insensível da ficha ou um editável na aba? (f) O anel de seleção é **roxo** (mockup
`:217`) ou **rosa** (recomendação de ONDE-A-COR-MORA-01, porque "o roxo colide com um dos seus
quatro controles")? A restrição 6 de CONFIG-01 reserva o rosa para marca e aba ativa, então é uma
exceção a registrar. (g) **Autorizar a medição 4** (escrever cor na lightbar do 8BitDo), que passa
por fora do portão que cala o LED dos externos.

### 7.6. CONFIG-07 — a janela

(a) A caixa "Mostrar ícone na barra do sistema" ganha backend de verdade (chave nova mais
`_has_persistent_access`) ou sai do escopo? (b) "Ligar junto com o computador" é **espelho com
link** (texto da sprint) ou **caixa editável** (mockup `:445`)? (c) A escala do texto vale **ao
reabrir o Hefesto** (barato) ou **na hora** (exige desfazer o compounding do `gtk-font-name`, que
é onde a casa já tropeçou)?

### 7.7. CONFIG-09 — o exame

(a) A cor do estado "atenção" é `@yellow` (mockup) ou `@orange` (todo `[WARN]` do produto e o
vocabulário de `theme.css:13`)? Nenhum portão decide. (b) "Firmware dos adaptadores" vira
diagnóstico NOVO declarado (lendo o journal do kernel) ou sai da lista das seis? (c) A janela passa
a ter **duas telas de saúde do sistema** — a da aba Sistema e a da Configurações. CONFIG-09
estende o cartão existente ou explica a divisão de assunto? D3 do INDICE diz que a aba nova não
rouba controle das existentes.

### 7.8. Documentação e higiene

(a) **Versionar a pasta da leva** (`docs/process/sprints/2026-08-21-ABA-CONFIGURACOES/`, hoje
untracked com 13 arquivos `.md` mais `mockup/`)? (b) **Versionar o `GUIA-RADIO-DA-SALA.md`**, que
hoje reprova a suíte por MAC real sem máscara e nomeia a máquina e o sistema dela em `:8-9`? (c)
Se alguma das dez fotos antigas mudar de pixel depois da aba nova, isso é mudança de DESENHO e é
**palavra dela** — PROVA-DE-TELA-01, citado em `docs/usage/assets/CONFERIDO-EM.md:9-11`.

---

## Contradições resolvidas na conferência final

A reconciliação foi feita por várias frentes em paralelo, e algumas discordaram
entre si. As que puderam ser decididas por medição direta ficam resolvidas aqui;
o resto segue aberto e está marcado como tal no corpo do documento.

### RESOLVIDO — `hci0` fixo em `scripts/doctor.sh`: sobrou **um**

Cinco ocorrências no arquivo, e só **uma é código em execução**:

| Linha | O que é | Ação |
|---|---|---|
| 2580, 2582, 2720 | Comentário | Nada a fazer |
| 2698 | Texto dentro da mensagem de erro (é a cura sugerida à pessoa) | Nada a fazer |
| **2704** | **Código: `_dbus_bt_prop /org/bluez/hci0 org.bluez.Adapter1 Discovering`** | **Corrigir** |

O comentário da linha 2720 registra que o adaptador *"também deixou de ser `hci0`
na unha (WATCHDOG-HCI-HARDCODE-01)"* — a cura já passou por aqui e deixou este
resto.

### RESOLVIDO — o `.pre-commit-config.yaml` tem **dez** hooks

Contagem direta: `grep -c "      - id: " .pre-commit-config.yaml` devolve `10`.

### RESOLVIDO — a tabela de cores do plástico tem **catorze** nomes

Em `scripts/ensaios/cor_do_plastico.py`. Nem dezesseis, nem vinte e um:

```
White · Midnight Black · Cosmic Red · Nova Pink · Galactic Purple
Starlight Blue · Grey Camouflage · Volcanic Red · (mais seis)
```

O mockup oferece as **seis** primeiras mais o campo livre — quem tiver uma
edição especial digita o nome.

### SEGUE ABERTO — o teto de altura de uma página de aba

Três valores foram medidos por frentes diferentes: **657px**, **718px** e
**~654px**. As decomposições também divergem (125+48 contra 73+39), o que sugere
que cada uma partiu de uma altura de janela ou de um conjunto de barras
diferente.

**Não decida no escuro.** Meça na sua máquina antes de usar como orçamento:

```bash
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/medir --mesa-cheia
```

A altura de cada PNG de aba é o teto real desta bancada. O que as três frentes
concordam: **a aba nova pede mais que qualquer aba existente**, e o corte que
resta é estrutural — provavelmente tirar "Os controles" desta aba e levá-lo para
o cabeçalho da janela.
