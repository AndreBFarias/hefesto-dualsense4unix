# O mapa da sessão de 28-29/07/2026 — e o que os agentes mediram

- **Levantado em:** 29/07/2026, sobre `restauro/inicio-da-sessao`, do commit
  `5489c2a` (fechamento da sessão anterior) até `2c18504` (`v0.3.0` publicada)
- **Por quê:** a sessão começou com *"estude o projeto"* e terminou com uma
  versão no ar. Entre as duas coisas houve uma auditoria de quatorze agentes
  cujo resultado, se não for escrito, some junto com a conversa
- **Como ler:** as seções 1 a 6 contam o que aconteceu, em ordem. A seção 7 é a
  que importa para quem chega depois: **o conhecimento sobre este projeto que a
  auditoria produziu e que não estava escrito em lugar nenhum**. As seções 8 a
  10 são o aceite, o que ficou de fora e o que continua sem medição
- **Regra de prova:** toda afirmação aqui tem caminho e linha, ou um comando de
  leitura que a devolve. Nada foi copiado de relatório de agente sem reconferir
  no repositório
- **Esta página é a primeira de seis.** As outras cinco saíram na mesma rodada e
  a ordem de leitura está no
  [índice da documentação da v0.3.0](2026-07-29-INDICE-a-documentacao-da-v030.md)

---

## 1. O contexto — de onde esta sessão partiu

A sessão anterior fechou em `e96dea8` com o índice
[o que ficou pelo caminho](../sprints/2026-07-27-INDICE-o-que-ficou-pelo-caminho.md),
que deixou a primeira da fila declarada e **não executada**: a `EMPATE-01`, a
sprint que diz que o desempate entre perfis é a ordem alfabética do nome do
arquivo. O motivo de não ter entrado estava escrito na própria página: mexe no
caminho que roda durante a partida, e a regra da casa é que isso entra sozinho,
com ela vendo.

O pedido de abertura desta sessão foi **estudar o projeto** antes de mexer em
qualquer coisa. Foi o que se fez, e o estudo é que produziu a leva.

---

## 2. A auditoria de quatorze agentes — como foi montada

O número está registrado no próprio changelog da versão: *"Quatorze agentes
leram o repositório inteiro e mediram a máquina em uso"* (`CHANGELOG.md:10`).
A montagem foi:

| Papel | Quantos | O que fizeram |
|---|---|---|
| Levantamento paralelo | 12 | Cada um com um recorte próprio do repositório, medindo em vez de ler documento antigo |
| Crítica de completude | 1 | Leu os doze relatórios contra a árvore e apontou o que **não** tinha sido olhado |
| Síntese | 1 | Juntou tudo e ordenou por dano |

O que valeu a pena e não estava previsto: **as contradições entre agentes foram
reconferidas à mão, uma a uma**. Duas passadas chegaram a conclusões opostas
sobre o microfone no mesmo dia, e a reconferência mostrou que as duas estavam
lendo o mesmo `grep` errado do `doctor.sh` — o que virou uma das correções da
leva (seção 3.5). Contradição entre agentes não é ruído a ser votado por
maioria; é sinal de que existe uma medição ambígua embaixo dos dois.

A prática de materializar achado de agente em documento já era regra desta casa
e tem precedente direto em
[o que os agentes acharam](2026-07-27-o-que-os-agentes-acharam.md) e no
[mapa do projeto](2026-07-27-INDICE-o-mapa-do-projeto.md), de 27/07.

---

## 3. Os quatro defeitos CRÍTICOS — e por que três são a mesma queixa

A queixa mais antiga desta casa é *"a config que eu deixo nunca é respeitada"*.
Ela nunca teve uma causa; tem **mecanismos**, e a auditoria achou três deles
vivos ao mesmo tempo, em camadas diferentes do produto.

### 3.1 O desempate entre perfis era a ordem alfabética do nome do arquivo

A chave de eleição de perfil é
`profiles/manager.py:640` — `return (not profile.e_catch_all, profile.priority)`.
Duas dimensões, e nada mais. Como o `sort` do Python é estável e o carregador
entrega os arquivos em `sorted(directory.glob("*.json"))`
(`profiles/loader.py:538`), **todo empate caía na ordem alfabética do nome do
arquivo** — que não é critério de ninguém, é acidente de `glob`.

Medido no disco dela, hoje, com leitura direta de
`~/.config/hefesto-dualsense4unix/profiles/`:

| Arquivo | `name` | `match` | `priority` |
|---|---|---|---|
| `fallback.json` | fallback | `any` | 0 |
| `vitoria.json` | vitoria | `any` | 0 |
| `meu_perfil.json` | meu_perfil | `any` | 1 |
| `pragmata.json` | Pragmata | `any` | 5 |
| `pragmata2.json` | Pragmata2 | `any` | 5 |

Cinco catch-alls. `pragmata.json` e `pragmata2.json` são idênticos fora o campo
`name`, empatam em prioridade 5, e quem vencia era `Pragmata` — enquanto
`~/.config/hefesto-dualsense4unix/session.json` diz `{"last_profile":
"Pragmata2"}`. **O perfil que ela deixou ativo perdia para um sósia, por causa
da letra `2`.** Só não mordia porque `autoswitch_locked.flag` está ligado.

A cura tem terceiro termo declarado, em `profiles/manager.py:658` — em empate de
(especificidade, prioridade), **o perfil que já está ativo continua**, e o
incumbente vem do `StateStore` (`manager.py:642`), não do `session.json`, porque
aquele arquivo guarda a última escolha manual e não o vigente. A regra vale nos
dois seletores; se valesse só no da aba, o alfabeto voltava pela porta dos
fundos.

Sprint: [EMPATE-01](../sprints/2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md).

### 3.2 Salvar pela janela rebaixava `match` e `priority`

Toda gravação pela aba Perfis reescrevia a regra e a prioridade com o que
estivesse nos widgets — e o editor simples mostra **"Qualquer"** para todo
`match` que ele não sabe representar. Salvar a cor, portanto, apagava a regra do
jogo.

O defeito tem data no disco dela. `pragmata.json` e `pragmata2.json` têm mtime
de `27/07 23:00` e `27/07 23:01` e hoje estão os dois em `match: any`;
`vitoria.json`, mtime `26/07 23:39`, está em prioridade 0. A leitura acima é a
fotografia depois do estrago.

A cura está em `app/actions/profiles_actions.py`: regra e prioridade só são
reescritas quando ela **mexeu** nelas, e "mexeu" conta pelo **gesto**, não pela
coincidência de valor — `_regra_tocada` é marcado pelo próprio widget do
"Aplica a" (`profiles_actions.py:570`), `_prioridade_tocada` pelo
`value-changed` da escala (`profiles_actions.py:324`), e os dois são zerados
**depois** de o `_populate_editor` posicionar os widgets
(`profiles_actions.py:1314-1315`), para que a abertura não conte como toque.

O motivo de o gesto ser necessário, e não bastar comparar valores, está escrito
no código (`profiles_actions.py:265-272`): um perfil com prioridade **acima do
teto** abre clampado na tela (`profiles_actions.py:1241`), então arrastar a
escala até o teto produziria um valor igual ao que já estava lá e seria
indistinguível de não ter tocado.

E o teto subiu: `PRIORIDADE_MAXIMA = 200` (`profiles_actions.py:74`). Com o
catch-all dela em 100, **não existia número escolhível pela janela que vencesse**.

### 3.3 `apply_draft` respondia sucesso incondicional

A cadeia inteira, medida:

1. `daemon/ipc_draft_applier.py:46` — `apply()` devolve a lista `applied` das
   seções que entraram, e as que falham vão para `self.failed`
   (`ipc_draft_applier.py:111`);
2. `daemon/ipc_handlers.py:456` — a resposta é
   `{"status": "ok", "applied": applied, "failed": dict(applier.failed)}`, e o
   `status` **é fixo em `"ok"` por contrato**, documentado como tal em
   `ipc_handlers.py:445-448` (applet, CLI e TUI decidem por ele e passariam a
   dizer "daemon offline" para uma seção que apenas falhou);
3. `app/actions/footer_actions.py` — a interface lia `result.get("status") ==
   "ok"` e chamava isso de sucesso. Ou seja: **o `status` responde "recebi", e a
   janela o lia como "apliquei"**.

O commit `e8f9060` curou a **frase** do rodapé. O que ficou de pé, e foi curado
em `b3e8b7f`, é a **contabilidade**: agora são duas perguntas separadas
(`footer_actions.py:173-178`) — `aceita` (o daemon respondeu; decide a frase) e
`aplicou` (alguma seção entrou; decide o `dirty` e o journal). Mais fino ainda:
a pendência da aba do mouse só cai se a seção **mouse** estiver no `applied`
(`footer_actions.py:183`), senão uma resposta com `applied=["leds"]` e
`failed={"mouse": ...}` apagaria a edição do mouse em silêncio.

Compatibilidade preservada de propósito: resposta **sem** `applied` (daemon
antigo, ou o `True` cru do bridge) continua contando como aplicada
(`footer_actions.py:541-550`) — a mesma regra que o texto já usava, porque as
duas não podem divergir.

### 3.4 737 testes de interface passavam contra um GTK falso

`pytest.importorskip("gi")` pergunta *"`import gi` funciona?"*. Um stub plantado
por **outro arquivo de teste** em `sys.modules` responde que sim. Vinte e um
arquivos plantavam `Gtk.Box = object`, e 737 testes de interface reportavam
`PASSED` contra um GTK de mentira — **com o verde dependendo da ordem alfabética
dos arquivos de teste** (commit `28bf718`).

O critério honesto está em `tests/conftest.py:33` — `_gtk_e_real()` não pergunta
se o módulo importa, pergunta se `Gtk.Box` é uma classe própria e não o `object`
embutido, e exige `Gtk.ListStore` junto, porque um `types.ModuleType` puro nunca
tem os dois reais ao mesmo tempo (`conftest.py:41-48`). Em cima disso,
`exigir_gi_real()` (`conftest.py:203`) faz três coisas que o `importorskip` não
fazia:

- reprova o stub;
- quando o **ambiente** tem PyGObject real e só o **processo** está envenenado,
  limpa o stub e segue (`conftest.py:221-229`), em vez de perder centenas de
  testes por culpa do arquivo anterior;
- torna o pulo **visível** (`conftest.py:232`), e sob `HEFESTO_EXIGE_GTK_REAL=1`
  o pulo vira **falha** (`conftest.py:233-238`).

Números medidos no cenário do CI (`gi` bloqueado), no commit `28bf718`: o `HEAD`
anterior tinha **24 erros de coleta e 65 falhas**; depois, **zero e zero**, com
5182 passando e 83 pulando com aviso.

### 3.5 O achado à parte — o detector de janela se declarava saudável mesmo cego

Não é da família "desfaz trabalho dela", e por isso está fora dos quatro: ele
**esconde** quando o perfil-por-jogo está morto.

`daemon/state_store.py:118` faz a flag nascer `False`; `state_store.py:271` a
recebe da semeadura do chamador; `state_store.py:325` a põe em `True` na
primeira leitura útil. **Nenhum caminho jamais a devolve para `False`** — é um
trinco de mão única, e a semeadura do backend `xlib` é uma presunção, não uma
medição. Um detector cego para sempre era, bit a bit, indistinguível de um
saudável.

A entrega separou as duas perguntas: `window_detect_healthy`
(`state_store.py:421`) continua sendo o trinco, **de propósito e documentado como
contrato**, porque tem consumidor de decisão — o `game_signal.classify`, onde
`healthy=False` sem evidência de jogo derruba a autoridade para `unknown` e a
transição repinta a lightbar com o resíduo retido do jogo. Quem responde "o
detector enxerga agora?" é `window_detect_seeing()` (`state_store.py:459`), que
**decai depois de `WINDOW_DETECT_BLIND_AFTER_SEC = 300.0`
(`state_store.py:43`) e volta na primeira leitura útil**, e não decide nada.

O teto é **tempo, não contagem**, e a justificativa é medida: o tique é de 2 Hz e
ficar minutos com um app Wayland nativo em foco é normal nesta máquina, então
contar leituras não-úteis mediria o uso dela, não o detector.

E o fato de plataforma que sai daqui: **em COSMIC o detector só enxerga
XWayland.** O `systemd --user` desta máquina exporta `DISPLAY=:1` e
`WAYLAND_DISPLAY=wayland-1` ao mesmo tempo, e a escolha de backend testa
`DISPLAY` primeiro — logo, COSMIC cai sempre no `XlibBackend`. Jogos Proton/Steam
**são** XWayland, então o perfil-por-jogo funciona; o que fica invisível é o
desktop e os aplicativos Wayland nativos.

Sprint: [JANELA-CEGA-01](../sprints/2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md).

---

## 4. A leva — oito commits

`git log --oneline 5489c2a..HEAD`:

| Commit | O que entregou |
|---|---|
| `e8f9060` | O rodapé para de dizer que aplicou o que não aplicou (a FRASE) |
| `8d7fd45` | O desempate deixa de ser o alfabeto; salvar para de rebaixar; teto da escala 100 -> 200; a semente do projeto para de opinar sobre cor; aba Status sem buraco |
| `28bf718` | O microfone grava ela e não o jogo; a janela fala português; e a guarda de GTK real |
| `acdae20` | A aba passa a se chamar só "Navegação" |
| `b3e8b7f` | SOM-01 (alto-falante, glifos, janela elástica), JANELA-CEGA-01 e APLICAR-VERDADE-02 |
| `464b7a2` | Versão 0.3.0, CHANGELOG e os badges do README |
| `18d61d8` | Os dois portões que reprovaram a estreia |
| `2c18504` | Versão nos pacotes, SVG no runner e o glifo que cabia por 12px |

Tag `v0.3.0`, publicada com **seis artefatos** (medidos via
`gh release view v0.3.0 --repo [REDACTED]/hefesto-dualsense4unix`):
AppImage (32,4 MB), Flatpak (9,8 MB), dois `.deb` (py310 e py312), a `.whl` e o
`.tar.gz`.

Um detalhe do processo que merece registro: a regra
[PROVA-DE-TELA-01](../sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md),
escrita em 27/07 e nunca aplicada, foi usada pela primeira vez — em todas as
levas desta sessão.

As três frases dela, literais, que dirigiram a última rodada de interface
(registradas em
[SOM-01](../sprints/2026-07-28-SOM-01-o-alto-falante-tem-lugar.md)):

> 1. *"dava pra colocar o auto falante abaixo do microfone"*
> 2. *"aumentar e espaçar mais os botões do controle tipo x quadrado bola e
>    triângulo e afins"*
> 3. *"permitir a expansão da janela"*

E, sobre a aba do mouse: *"a aba usar como mouse deixa só Navegação"* (commit
`acdae20`). A aba Status v2 tinha sido aprovada por ela com *"quase perfeito"* —
depois de a versão anterior ter sido reprovada com *"só distanciou as coisas"*.

---

## 5. A estreia falhou TRÊS vezes — e nenhuma foi de código

A tag foi publicada e os workflows reprovaram. Vale escrever porque **os três
motivos são de infraestrutura de portão, não de produto**, e os três eram
evitáveis antes do push.

### 5.1 `scripts/check_test_data.sh` — MACs de dublê fora das famílias neutras

O gate reprovou quatro linhas de `tests/unit/test_mic_captura_e_botao.py`. Ele
aceita três famílias sintéticas e só três (`scripts/check_test_data.sh:26`):
`OUI:00:00:NN` (a máscara imposta pelo gate de anonimato), `02:fe:*` (o vpad,
MAC localmente administrado por construção) e `aa:bb:cc:*` (faixa de
documentação). Qualquer MAC fora disso reprova, que é o ponto.

A correção teve uma sutileza: o sufixo do nome da fonte da ponte Bluetooth **é**
os três últimos octetos do MAC, então trocar só um lado quebraria o próprio
teste que prova a atribuição fonte-para-controle. Os dois lados foram casados
juntos.

A lição: o gate **estava na CI o tempo todo** (`.github/workflows/ci.yml:38` e
`.github/workflows/release.yml:59`) e não estava na lista local que se rodava
antes do push. **Portão que existe e não é rodado antes do push é portão que só
avisa tarde.**

### 5.2 `scripts/check_version_consistency.py` — seis alvos versionados, não dois

Subiram-se dois; o gate cobra seis (`scripts/check_version_consistency.py:33-44`):
`README.md`, `src/hefesto_dualsense4unix/__init__.py`,
`packaging/arch/PKGBUILD`, `packaging/fedora/hefesto-dualsense4unix.spec`,
`packaging/nix/package.nix` e `packaging/debian/control`. O histórico que
justifica o gate está no cabeçalho do próprio script: Arch, Fedora, Nix e Debian
já ficaram defasados em 3.4.0, **instalando versão antiga**.

### 5.3 O job de interface novo — OOM no runner, e um loader de SVG faltando

O job "Interface com GTK REAL" (`.github/workflows/ci.yml:278`) foi criado nesta
mesma sessão e falhou na estreia por duas razões independentes:

- **rodava a suíte inteira sob Xvfb** e morria aos 39% da coleta, **sem
  traceback**. A suíte completa já roda no `lint-test` com o piso de cobertura;
  repeti-la ali não respondia pergunta nova e custava a vida do processo. Agora
  ele seleciona **só** os testes de interface, pelo mesmo critério da guarda —
  `grep -rlE 'exigir_gi_real|skip_sem_gi_real' tests/unit`
  (`ci.yml:392-393`) —, de modo que a lista **não precisa ser mantida à mão** e
  um arquivo novo entra sozinho no dia em que ganhar a guarda. Medido agora:
  **31 arquivos**, 554 testes;
- **faltava o loader de SVG.** Entraram `librsvg2-2`, `librsvg2-common` e
  `gir1.2-rsvg-2.0` (`ci.yml:313`).

---

## 6. A lição de medição da sessão — doze pixels de folga não são folga

O pedido 2 dela era aumentar e espaçar os glifos dos botões. O fator escolhido
primeiro foi 13/8: levava o glifo de 36 para 58 px. Nesta máquina o card passou
a pedir **357 px de altura contra 369 px disponíveis** — **doze pixels de folga**
— e passou.

A máquina do CI **não tem as fontes do projeto** e portanto mede o texto com
métricas de fallback. Ela pediu **431 px** e reprovou. E estava certa: a mesma
coisa aconteceria na tela dela com outro tema ou outra escala de fonte.

O fator caiu para 12/8 (`GLYPH_FATOR_UNICO_OITAVOS = 12`,
`app/widgets/controller_card.py:195`): com a escala 3 desta casa,
`glyph_size(3) = 24 + 3*4 = 36` (`controller_card.py:158,163`) e
`glyph_size_unico` devolve `36 * 12 // 8 = 54` (`controller_card.py:231`). Isso
é um aumento de 50% sobre os 36 px, que é o que ela pediu, e devolve a altura do
card para 341 px, com 28 px de folga.

O aprendizado transferível, e é o que dá nome à seção:

> **Doze pixels de folga não são folga. Uma folga só é folga se sobrevive à
> máquina que mede com outras métricas de fonte.**

E a segunda metade, que é fácil de errar: **o teto de verdade daquele card é a
altura, não a largura** — o grid 4x4 dos botões manda nas duas dimensões, e a
largura o teto elástico paga sozinho.

---

## 7. O que os agentes mediram e que ninguém sabia

Esta é a seção que justifica o documento. Cada item abaixo é **uma coisa que
agora se sabe sobre este projeto** e que não estava escrita em nenhum lugar
antes desta sessão. Não é o relato de quem achou; é o conhecimento.

### 7.1 No GTK3 não existe largura máxima declarada

`set_size_request` declara o **MÍNIMO**, e `halign=CENTER` com um mínimo
declarado **trava o widget naquele número exato**. Era assim que o card ficava
em 960 px com a janela em 1920, sobrando cerca de 950 px de margem morta
(`app/widgets/controller_card.py:889-892`).

A consequência de projeto: **teto elástico só pode viver no `do_size_allocate`**
(`controller_card.py:886` e `controller_card.py:2008`), onde o widget aceita a
largura que o pai der até `LARGURA_CARD_ELASTICA = 1400`
(`controller_card.py:316`) e devolve o excedente como margem, centrando-se. E o
`halign` do card fica em `FILL`, não em `CENTER`, de propósito
(`controller_card.py:916-920`).

Corolário que custou uma medição: a alocação recebida **não pode ser mutada** —
ela é a variável local do `gtk_widget_size_allocate` do pai, usada depois para o
clip; o corte vai numa cópia (`controller_card.py:900-910`).

Segundo corolário: **um widget que veio do glade não tem onde receber esse
código**, porque `width-request` no glade é mínimo e subiria intacto até a
largura mínima da janela. Por isso o teto do frame "Estado" vem **de fora**, com
o app o envolvendo numa `CaixaDeTetoElastico` na montagem (`app/app.py:867`).
Sem isso, ele ficaria em 1040 px acima de um card de 1400 px — um degrau de 360
px, visível na captura.

### 7.2 `pytest.importorskip("gi")` aceita stub, e por isso não protege nada

Ele responde à pergunta errada. O critério honesto é olhar se **`Gtk.Box` é uma
classe de verdade** e não o `object` embutido, com `Gtk.ListStore` junto como
segunda âncora (`tests/conftest.py:33-48`). Esse é o único teste que separa o
PyGObject real do stub canônico dos testes, que faz `Gtk.Box = object` e passa em
qualquer `hasattr`.

O mesmo critério foi replicado do lado do CI, antes de coletar qualquer teste
(`.github/workflows/ci.yml:336-348`), de modo que o job morre com mensagem em vez
de coletar 5 mil testes contra um GTK pela metade.

### 7.3 Typelib parcial no CI derruba a COLETA inteira

Não é um teste que falha: é `Gtk.ResponseType` estourando `AttributeError` na
importação e levando junto a coleta. E o `importorskip("gi")` **não protege
disso**, porque `import gi` funciona perfeitamente com typelib incompleta
(`.github/workflows/ci.yml:299-303`).

A consequência prática está escrita na lista de pacotes do runner
(`ci.yml:304-313`): não basta `gir1.2-gtk-3.0`; entra o conjunto inteiro que a
interface toca — glib, gdkpixbuf, pango, atk, harfbuzz, freedesktop, notify,
ayatanaappindicator.

Fato vizinho, medido e escrito no mesmo lugar (`ci.yml:290-295`): **não usar
`actions/setup-python` neste job**. O Python que ele instala é isolado e não
enxerga `/usr/lib/python3/dist-packages`, onde o `python3-gi` do sistema mora;
instalar PyGObject pelo pip ao lado das typelibs do sistema já foi tentado nesta
casa e derrubava o interpretador no meio da suíte. O caminho que funciona é
Python do sistema mais venv com `--system-site-packages`.

### 7.4 SVG sem librsvg faz o pixbuf sair `None` — e isso muda a geometria

Os glifos dos botões são SVG carregados por
`GdkPixbuf.Pixbuf.new_from_file_at_scale`
(`src/hefesto_dualsense4unix/gui/widgets/button_glyph.py:290`), dentro de um
`try/except` que devolve `None` em qualquer falha (`button_glyph.py:293-294`).

Sem o loader do librsvg no runner, o pixbuf sai `None` — e a consequência **não**
é só um teste de tintura reclamando de `"NoneType has no get_pixels"`. O
fallback sem pixbuf **muda a geometria**: foi parte do porquê de o card pedir
431 px de altura na CI contra 357 px na máquina real (`ci.yml:314-319`).

A generalização: **um recurso gráfico que degrada para `None` em silêncio não
degrada só o desenho, degrada a medida** — e qualquer orçamento de layout
medido numa máquina com o loader instalado está medindo outro programa.

### 7.5 Um gate de texto que só varre o que está no git é cego a arquivo novo

`git ls-files -z` puro lista **só o índice**. Um gate `--all` construído sobre
ele dava verde exatamente no arquivo que ninguém tinha revisado ainda
(`scripts/validar-acentuacao.py:853-858`).

A cura, e é a forma canônica para qualquer gate desta casa:
`git ls-files -z --cached --others --exclude-standard`
(`validar-acentuacao.py:861-871`) — traz o não rastreado sem trazer o ignorado, e
duplicata não ocorre porque um caminho é `cached` **ou** `other`, nunca os dois.

### 7.6 Morte silenciosa aos ~40% da coleta, sem traceback, é assinatura de OOM

Não é bug de teste, não é bug de coleta: é o runner ficando sem memória. Está
registrado como assinatura em dois lugares independentes do mesmo arquivo
(`.github/workflows/ci.yml:290-295` e `ci.yml:379-384`), porque foi observado
duas vezes por caminhos diferentes — uma com PyGObject do pip ao lado das
typelibs do sistema, outra com a suíte inteira sob Xvfb com o GTK real
carregado.

A regra que sai disso: **carregar GTK real multiplica o custo de memória por
teste coletado**, então um job de interface tem de selecionar os arquivos de
interface, e não a suíte.

### 7.7 O `status` do IPC significa "recebi", não "apliquei" — e é contrato

`profile.apply_draft` devolve `status` fixo em `"ok"` **de propósito**
(`daemon/ipc_handlers.py:445-448`): applet, CLI e TUI decidem por ele, e
mudá-lo faria os três dizerem "daemon offline" para uma seção que apenas falhou.
A verdade nova é **aditiva** — quem quiser saber o que entrou lê `applied`, quem
quiser saber o que ficou de fora lê `failed` (`ipc_handlers.py:456`).

O que isso ensina para qualquer consumidor futuro do IPC: **existe uma diferença
entre "a chamada foi aceita" e "o efeito aconteceu", e neste protocolo ela é
explícita.** Quem colapsar as duas numa variável só vai reproduzir o defeito de
`footer_actions.py`.

### 7.8 O empate de perfis nunca teve terceiro critério, e o incumbente é a escolha conservadora

Ficou escrito, com a razão: o terceiro termo do desempate **não inventa
hierarquia nova** (nada de "data de modificação", nada de "perfil padrão" a mais
para ela administrar), não muda nada quando não há empate, e o que faz numa
frase é *"uma disputa sem critério deixa de derrubar o que estava valendo"*
(`profiles/manager.py:658-684`). Quando o incumbente não está entre os
empatados, o desempate segue sendo o histórico — mudar isso mudaria
comportamento já validado sem que ninguém tenha pedido.

E a fonte do incumbente é o `StateStore`, não o `session.json`
(`profiles/manager.py:642-657`): o arquivo guarda a última escolha **manual**
dela, que não é necessariamente o perfil vigente, e lê-lo ali somaria I/O de
disco a um caminho que roda a 2 Hz.

### 7.9 "Ela mexeu nisso?" não se responde comparando valores

O editor simples de perfis clampa a prioridade ao teto ao abrir
(`app/actions/profiles_actions.py:1241`). Logo, para um perfil que veio do disco
acima do teto, **arrastar a escala até o teto produz o mesmo número que já estava
na tela** — e uma guarda por comparação de valor concluiria "não tocou" e
descartaria o gesto dela.

A forma correta, e vale para qualquer campo desta janela: **marcar o gesto no
widget** (`profiles_actions.py:324` e `:570`) e **zerar a marca depois da
população programática** (`profiles_actions.py:1314-1315`). Comparação de valor
entra como reforço, nunca como critério único (`profiles_actions.py:1370-1375`).

### 7.10 Em COSMIC o backend de janela é sempre o xlib, e isso é escolha do ambiente

O `systemd --user` desta máquina exporta `DISPLAY=:1` **e**
`WAYLAND_DISPLAY=wayland-1`; a seleção testa `DISPLAY` primeiro. As 385 linhas
da cascata Wayland (`window_backends/wayland_portal.py` +
`window_backends/wlr_toplevel.py`) **nunca executam aqui**, e o `doctor.sh` já
mediu por outra via que elas não resolveriam: o cosmic-comp não expõe
`wlr-foreign-toplevel-management` e o portal XDG não tem `GetActiveWindow`.
Suporte real exigiria o protocolo próprio `zcosmic_toplevel_info_v1`.

O que se faz com esse conhecimento: **não tratar "sem foco X" como alarme**. É o
estado normal do desktop desta máquina. O honesto é a linha na tela dizendo que
o detector não vê janela Wayland nativa.

### 7.11 Um trinco de mão única pode ser contrato, desde que esteja escrito

`window_detect_healthy` **continua** sendo um trinco depois desta leva
(`daemon/state_store.py:421-440`), e a property agora carrega o aviso explicando
por quê: o único consumidor de decisão é o `game_signal.classify`, e fazer a
flag decair repintaria a lightbar dela com o resíduo retido do jogo a cada vez
que ela passasse cinco minutos num app Wayland nativo.

A lição de método, que vale além deste campo: **quando um valor observável e um
valor de decisão estão na mesma variável, a cura é separá-los, não fazer o de
decisão mentir menos.** Foi o que se fez — `seeing` responde sobre o agora e não
decide nada; `healthy` decide e está documentado como fail-safe.

### 7.12 Dois gates do mesmo repositório podem se contradizer, e vence o que alguém consegue satisfazer

`check_test_data.sh` já reprovou exatamente a convenção que o gate de anonimato
**exige** (`scripts/check_test_data.sh:11-25`): mascarar MAC como `OUI:00:00:NN`
caía como dado pessoal. **Um gate que ninguém pode satisfazer não protege nada;
só ensina a ignorar portão.** A allowlist de três famílias existe por causa disso.

### 7.13 O contador de testes de interface do CI se mantém sozinho

A seleção do job é `grep -rlE 'exigir_gi_real|skip_sem_gi_real' tests/unit`
(`.github/workflows/ci.yml:392-393`). Não há lista de arquivos em lugar nenhum
para alguém esquecer de atualizar: **um arquivo de teste novo entra no job no dia
em que ganhar a guarda**. Conferido agora, o `grep` devolve **31 arquivos**.

---

## 8. Como validar na tela

O aceite desta leva já foi dado por ela nas rodadas de interface; o que segue é o
roteiro para revalidar depois de qualquer mexida vizinha, na ordem em que a
`PROVA-DE-TELA-01` manda.

1. **A cor é dela.** Com o daemon vivo, `session.json` em `Pragmata2` e o
   cadeado ligado, abrir a aba Perfis: o ativo tem de ser **Pragmata2**, não
   Pragmata. Critério de aceite: o sósia não vence mais o incumbente.
2. **Salvar não rebaixa.** Abrir um perfil de jogo, mudar **só a cor**, salvar,
   e reler o JSON no disco: `match` e `priority` inalterados. Critério de
   aceite: nenhum campo que ela não tocou muda de valor.
3. **O rodapé não mente.** Aplicar um rascunho com uma seção que falha: a frase
   tem de nomear o que não entrou, e a pendência da aba do mouse **continua
   pendente** se a seção mouse não entrou.
4. **A janela expande.** Maximizar em 1920: o card cresce até 1400 px e o
   excedente vira margem, sem vão maior que 200 px entre os blocos da faixa
   (é o que `tests/unit/test_status_faixa_blocos.py:251` cobra).
5. **Os glifos.** X, bola, quadrado e triângulo visivelmente maiores (54 px na
   escala 3), com 10 px de respiro. Com dois ou mais controles, no tamanho de
   antes — e isso é decisão, não esquecimento.
6. **O som tem lugar.** Alto-falante logo abaixo do microfone, mesma largura,
   mesma moldura; à esquerda só touchpad e lightbar, alinhados pelo topo.
7. **Encolher.** Reduzir a janela ao tamanho de projeto: nada sai pela borda e
   não aparece rolagem horizontal.

---

## 9. O que ficou de fora desta sessão, e por quê

- **A troca do consumidor do `game_signal` de `healthy` para `seeing`.** É uma
  linha em `daemon/lifecycle.py`, e está declarada como leva própria em
  [JANELA-CEGA-01](../sprints/2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md),
  porque muda a cor do controle dela e tem de entrar com ela olhando.
- **A linha na aba Sistema** dizendo que o detector não vê janela Wayland
  nativa. Os campos novos já sobem no `state_full`; a aba não estava entre os
  arquivos liberados da leva.
- **`integrations/xlib_window.py`** continua no repositório: 111 linhas que
  nenhum código de produção importa e que leem `_NET_ACTIVE_WINDOW` **sem gate
  de foco** — ou seja, o defeito que o UX-02 e o FOCO-01 curaram, preservado
  inteiro num arquivo que ainda importa limpo. Mina armada para quem importar.
  Virou candidata a sprint (`CÓDIGO-MORTO-01`) no
  [índice do que falta depois da v0.3.0](../sprints/2026-07-29-INDICE-o-que-falta-depois-da-v030.md).
- **O frame "Estado" não cresce com a janela** — só o piso subiu. O motivo está
  na sprint [SOM-01](../sprints/2026-07-28-SOM-01-o-alto-falante-tem-lugar.md), e
  o miolo dele foi medido depois pela
  [LARGURA-01](../sprints/2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md),
  entrega E2: a coluna de valores recebe 1242px para no máximo 112px de tinta.
- **O alto-falante continua sem controle de volume.** É leitura, e é decisão
  escrita: o DualSense não devolve o volume, e inventar um controle que não lê
  de volta seria mentir. O desenho de um controle que **assuma** esse preço, com
  as quatro armadilhas executadas e o preço medido por byte, foi levantado
  depois na
  [SOM-02](../sprints/2026-07-29-SOM-02-o-alto-falante-que-funciona.md) — que
  também segue sem código, e depende da decisão dela.
- **O glifo do card compacto não cresceu.** Com dois ou mais cards a largura de
  cada um soma direto no mínimo da janela, sem rolagem horizontal para absorver
  (`app/widgets/controller_card.py:222-229`).
- **O CHANGELOG da 0.3.0 diz "36 para 58 px"** (`CHANGELOG.md:60`), número que
  o commit `2c18504` corrigiu para 54 px depois. É a única divergência conhecida
  entre o changelog publicado e a árvore, e fica registrada aqui em vez de ser
  reescrita à revelia.

---

## 10. O que continua sem medição

Herdado do índice
[o que ficou pelo caminho](../sprints/2026-07-27-INDICE-o-que-ficou-pelo-caminho.md)
e da [blindagem](../sprints/2026-07-27-INDICE-a-blindagem.md), com o estado de
hoje ao lado de cada item.

| Item | Estado em 29/07 |
|---|---|
| **Os números de flapping das sprints de perfil são de 26/07 e nunca foram reproduzidos** | **Continua valendo.** O daemon esteve vivo a sessão inteira e o journal foi consultado para datar o rebaixamento dos perfis, mas o flapping em si não foi remedido |
| **`autoswitch_locked.flag` está ligado, e nenhuma sprint de perfil diz o que muda com o cadeado ligado** | **Continua valendo, e ficou mais importante.** O arquivo tem mtime de 28/07 18:18; é a configuração real dela, e foi só por causa do cadeado que o defeito do desempate não mordeu antes |
| **A escala de fonte máxima (8) nunca foi medida** | **Continua valendo, e agora tem preço conhecido.** A escala dela é 3, que é o padrão e não uma escolha; o pior caso do orçamento é a 8, e a lição dos 12 px (seção 6) diz exatamente o que acontece quando o orçamento é medido só no caso favorável |
| **`app/compact_window.py` e a bandeja ficaram fora de todos os levantamentos** | **Continua valendo.** Se a segunda janela repete card ou rótulos, as renomeações da `PALAVRA-01` saem pela metade |
| **A aba Status com dois cards lado a lado** | **Parcialmente coberto.** Há teste de largura para dois cards, e a decisão de não crescer o glifo no compacto é escrita — mas a avaliação com o olho continua tendo sido feita com um controle só |
| **Os testes de interface pulavam no CI, em silêncio** | **RESOLVIDO nesta sessão.** O pulo virou visível, a guarda reprova stub, e há job dedicado rodando 31 arquivos de interface com GTK real e `HEFESTO_EXIGE_GTK_REAL=1` |

E três que nasceram agora:

- **A tela dela com tema claro, ou com fator de escala do compositor diferente de
  1.** Todo o orçamento de altura do card foi medido num só tema. A CI provou que
  métricas de fonte diferentes mudam o resultado em quase 80 px.
- **O `window_detect_reason` no daemon vivo.** A fiação entrou, mas o valor
  publicado com o daemon dela em operação por um período longo não foi observado
  — só em teste.
- **O comportamento do desempate por incumbente ao longo de uma partida
  inteira.** Foi provado por teste e por reprodução, não por uma sessão de jogo
  de ponta a ponta com troca de foco entre jogo e desktop.

---

## Anexo — os números desta sessão, conferidos hoje

| Medida | Valor | Como foi conferido |
|---|---|---|
| Commits da leva | 8 (`e8f9060`..`2c18504`) | `git log --oneline 5489c2a..HEAD` |
| Testes coletados | **5783** | `.venv/bin/python -m pytest --collect-only -q` |
| Arquivos de teste de interface | **31** | `grep -rlE 'exigir_gi_real\|skip_sem_gi_real' tests/unit` |
| Artefatos da release | **6** | `gh release view v0.3.0 --repo [REDACTED]/hefesto-dualsense4unix` |
| Alvos versionados cobrados pelo gate | **6** | `scripts/check_version_consistency.py:33-44` |
| Perfis catch-all no disco dela | **5** | leitura de `~/.config/hefesto-dualsense4unix/profiles/` |
| Perfil ativo dela | `Pragmata2` | `~/.config/hefesto-dualsense4unix/session.json` |
| Teto elástico do card | **1400 px** | `app/widgets/controller_card.py:316` |
| Glifo no card único, escala 3 | **54 px** | `controller_card.py:158,163,195,231` |
| Teto de cegueira do detector | **300,0 s** | `daemon/state_store.py:43` |
| Teto da escala de prioridade | **200** | `app/actions/profiles_actions.py:74` |
