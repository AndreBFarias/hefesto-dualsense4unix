# PROMESSA-NAO-CUMPRIDA-01 — o que o projeto anuncia e não entrega

- **Status:** ABERTA
- **Prioridade:** MÉDIA, com **dois itens ALTOS** marcados abaixo
- **Aberta em:** 26/07/2026, a partir de um estudo do repositório inteiro
- **Natureza:** guarda-chuva. Cada bloco é independente e pode virar sprint
  própria; ficam juntos porque têm a **mesma forma** — algo declarado que não
  acontece

## A forma comum

Todos os itens abaixo são a mesma coisa em superfícies diferentes: **um portão
que se anuncia fechado e está aberto, ou um recurso que se anuncia pronto e não
tem como ser ligado.** É a classe de defeito que esta casa já nomeou:

> *"Um gate que ninguém pode satisfazer não protege nada — só ensina a
> ignorá-lo."* (`845295b`)

E a irmã dela, do mesmo commit: um gate que ninguém roda não é gate, é arquivo.

---

## Bloco A — gates que não veem o que prometem ver

### A1. O gate de emoji nunca foi construído — ALTO

Não é que ele falhe. **Ele não existe.**

Medido:

```
grep -rlin "emoji" scripts/            ->  nenhum arquivo
.pre-commit-config.yaml                ->  3 hooks: acentuacao, anonimato, ruff
```

O `.pre-commit-config.yaml` tem exatamente três hooks, e nenhum deles varre
emoji. O que existe em `scripts/validar-acentuacao.py:514` é
`_contem_glyph_protegido`, que faz o **oposto**: impede o higienizador de apagar
glifos *permitidos* pelo ADR-011. É a defesa contra o erro de excesso, não contra
o de falta.

Enquanto isso, `.github/CONTRIBUTING.md:44` anuncia, na lista do que o pre-commit
bloqueia:

> *"Emojis gráficos em commits, docs e código."*

E a prova de que a ausência é real: `docs/usage/troubleshooting-8bitdo.md`, linhas
29 e 48, contém **U+2B50 WHITE MEDIUM STAR** — Emoji_Presentation, proibido pelo
critério objetivo do ADR-011. Está no repositório, commitado, passou por
pre-commit e CI.

É alto por causa da assimetria: o ADR-011 nasceu de um episódio caro em que um
higienizador leu "zero emojis" como "zero não-ASCII", apagou os glifos de estado
do código **e adaptou o teste à regressão**. A casa construiu a defesa contra
aquele erro específico e **anunciou** a defesa contra o erro oposto sem
construí-la. Quem lê o CONTRIBUTING acredita estar protegido nas duas direções.

#### O flagrante — este documento foi vítima do defeito que descreve

No commit que criou este arquivo, a saída do `git commit` trouxe:

```
[sanitizer] 2 arquivos: 3 emojis removidos
```

Existe, portanto, um higienizador no fluxo de commit. Ele **não** está no
`.pre-commit-config.yaml` e **não** está em `.git/hooks/` (vazio) — vem do
ambiente de trabalho, não do repositório. E o que ele fez, medido no diff:

| Codepoint | Nome | Bloco Unicode | ADR-011 diz | O higienizador fez |
|---|---|---|---|---|
| `U+26A0` | WARNING SIGN | Miscellaneous Symbols | proibido | removeu — **correto** |
| `U+2194` | LEFT RIGHT ARROW | **Arrows** | **permitido** | removeu — **errado** |

> Os dois glifos estão citados aqui **por codepoint, não por desenho**, de
> propósito: escritos como caractere, o higienizador apagaria a própria tabela
> que documenta o que ele faz de errado. Este parágrafo é a segunda prova.

O `U+2194` estava numa tabela do índice desta leva, ligando as palavras `doc` e
`código` para dizer "contradições entre os dois". Com a seta apagada, as duas
palavras se colaram e a célula passou a dizer `doccódigo` — que não é palavra
nenhuma, dentro de um documento sobre coisas que o projeto afirma e não confere.
Foi preciso reparar à mão.

E houve uma **terceira** mordida: a frase acima, na sua primeira versão, citava a
seta pelo desenho para mostrar o antes e o depois. O higienizador a apagou também
— transformando a narração do apagamento numa frase circular, que dizia que
`doccódigo` havia virado `doccódigo`. Está reescrita sem nenhum glifo literal.
Três passes, três remoções, zero avisos.

Isso fecha o argumento melhor do que qualquer análise:

1. **O que o projeto promete (bloquear emoji) não existe** — nada no pre-commit
   varre isso, e há um U+2B50 commitado provando.
2. **O que existe no lugar (remover em silêncio) faz demais** — apaga glifo que
   o ADR-011 protege explicitamente, sem avisar, dentro do commit.
3. E as duas coisas juntas produzem o pior desfecho possível: quem escreve
   confia no gate que não existe, e tem o texto alterado por um higienizador que
   não deveria ter tocado ali.

Um **gate** reprova e diz o que está errado, e a pessoa corrige. Um
**higienizador** altera e segue, e ninguém fica sabendo. Para conteúdo escrito,
a diferença entre os dois é a diferença entre revisar e ser reescrito.

### A2. Duas convenções de commit em vigor, contraditórias

- `.github/CONTRIBUTING.md:99-118` prescreve **"PT-BR acentuado"**.
- A prática desde ~24/07 é assunto **sem acento**, porque o higienizador do fluxo
  de commit os remove — registrado em
  `docs/process/estudos/2026-07-26-retrato-das-nove-abas.md`.

Nada no repositório reconcilia as duas. Quem contribuir de fora vai seguir o
CONTRIBUTING e ver o próprio texto alterado sem explicação.

### A3. Gates que existem e não rodam

- `scripts/check_packaging_parity.sh` (312 linhas) é a guarda mais forte contra
  regressão de empacotamento — verifica que toda regra udev em `assets/` está
  coberta pelos três instaladores **e** pelo uninstall. **Não roda em workflow
  nenhum.**
- O applet COSMIC (Rust, 1.745 linhas) **não é compilado no CI**. A paridade dele
  com a GUI é verificada por testes Python que leem o `.rs` **como texto**.

### A4. 734 testes de interface pulam no CI

Está escrito com todas as letras em `.github/workflows/ci.yml:88-104`, e a
honestidade é exemplar: *"não finja que está coberto"*. A causa é real (instalar
PyGObject por pip matava o interpretador no meio da suíte).

Fica registrado como dívida, não como acusação: **14,9% da suíte só é exercida na
máquina de desenvolvimento.** E foi exatamente na interface que a leva de 26/07
quebrou sem nenhum teste reclamar.

---

## Bloco B — o instalador anuncia o que não faz

### B1. As fontes da identidade visual nunca são instaladas — ALTO

`scripts/install_fonts.sh` existe, foi escrito em `fc9a9f6` justamente porque as
duas fontes não estavam na máquina (0 de 797; o `fc-match` caía em Noto Sans). E
**`install.sh` não o chama** — zero ocorrências.

É alto porque afeta o que ela vê: `gui/theme.css:56-144` pede Space Grotesk e
JetBrains Mono, o fontconfig substitui em silêncio, e a janela nunca teve a
tipografia que o desenho especifica. Toda discussão de legibilidade até hoje
aconteceu com as fontes erradas.

### B2. Uma unit que só existe para ser removida

`assets/hefesto-dsx-recover.service` não é instalado por **nenhum** caminho
(zero ocorrências em `install.sh`). Mas `uninstall.sh:358-362` e `doctor.sh:2742`
a conhecem e a tratam. É resíduo de uma feature removida: sobrou só o código de
limpeza.

### B3. A ajuda do instalador está truncada e cita flag que não existe

- `install.sh:217` imprime a ajuda com `sed -n '2,128p'`, cortando a
  documentação de `--force-xwayland` e as notas de default (linhas 129-144).
- `--no-snd-quirk` é parseado em `install.sh:203` e **não aparece** no cabeçalho,
  logo não aparece no `--help`.
- `install.sh:1186` sugere `--disable-usb-audio` como se fosse flag do
  instalador. É do `scripts/install_udev.sh`; passada ao `install.sh`, aborta com
  código 2.

### B4. Uma janela de ordem entre dois passos

As regras `82-nintendo-pro-nosniff.rules` e `83-hefesto-bond-snapshot.rules` são
gravadas no passo 3, e invocam scripts em `/usr/local/lib/hefesto-dualsense4unix/`
que só chegam lá no passo 3e-bis. Numa instalação limpa há uma janela em que um
`ACTION=="add"` dispara um `RUN+=` para caminho inexistente. Inócuo (o udev loga
e segue), mas é assimetria real.

---

## Bloco C — funcionalidade entregue sem chave para ligar

### C1. As métricas não têm chave

`docs/adr/016-prometheus-metrics.md` já ganhou nota de verificação, e ela é
clara: não existe variável de ambiente, flag ou arquivo que ligue
`metrics_enabled`. O `DaemonConfig` é construído com três parâmetros. Subir as
métricas exige mexer no código.

### C2. Os plugins caminham para o mesmo lugar

`docs/adr/017-plugin-system.md` manda ativar por `~/.config/hefesto/config.toml`
— caminho impossível, mesma razão. A variável de ambiente funciona; o arquivo,
não. O ADR não tem nota de verificação.

### C3. `SUBSYSTEM_REGISTRY` não é iterado por ninguém

`daemon/subsystems/__init__.py:41` declara o registro dos subsistemas, e o
próprio arquivo avisa (linhas 10-17) que **ele não é iterado em produção** —
quem sobe subsistema é `Daemon.run()`, linha a linha. Foi assim que o
`BtMicSubsystem` nasceu órfão: registrado na lista e nunca iniciado.

Há teste travando a paridade entre as duas listas, o que impede a repetição. Mas
continuam sendo **duas fontes de verdade** para o mesmo fato.

**Nota de produto:** C1, C2 e a porta UDP de
[DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md)
são o mesmo buraco. Um arquivo de configuração lido de verdade resolveria os três
— e apagaria a contradição do `daemon.toml`, que hoje é citado por três
documentos e por um botão da janela.

---

## Bloco D — empacotamento

- `packaging/arch/PKGBUILD` e o spec do Fedora **não empacotam** as regras udev
  82, 83 e 84. O Flatpak empacota as três. `check_packaging_parity.sh` não pega
  porque verifica cobertura pelos *instaladores*, não pelos *manifestos*.
- `packaging/nix/package.nix:74-76` tem `sha256 = lib.fakeSha256` na derivation
  do `pydualsense` — **placeholder**. O `nix build` documentado não funciona sem
  edição manual.

---

## Bloco E — dívida de teste, já diagnosticada e não paga

Tudo aqui já está registrado em
`docs/process/estudos/2026-07-25-leva-causas-raiz.md`. Entra nesta sprint só para
ter dono e número:

- **479 asserts travam o texto do código-fonte**, em 58 arquivos. Destes, ~346
  grepam shell — defensável, `tests/shell/` está vazio e não há bats no
  repositório. Os problemáticos são os **~71 que congelam Python de produção**
  (34 via `inspect.getsource`, 37 lendo `.py` como texto), mais 25 asserts de
  `.count()` que proíbem deduplicar código.
- **Viés de transporte:** 9 ocorrências de `transport="bt"` contra dezenas de
  `"usb"`. Bugs de rádio são invisíveis por construção — e o rádio é onde moram
  os defeitos mais caros deste projeto.
- **`tests/integration/` e `tests/shell/` estão vazios** desde maio. A taxonomia
  de diretórios não descreve nada.
- **11 módulos de `src/` sem citação em teste nenhum** — entre eles 6 dos 13
  módulos da CLI e `utils/i18n.py` inteiro.

---

## Bloco F — a janela fala português, e só português

- `po/pt_BR.po` e `po/en.po` têm 245 entradas cada; **59 vazias em `en`**, 60 em
  `pt_BR`.
- Só **9 módulos** importam `_()`. As nove abas em `app/actions/` têm o texto
  PT-BR **fixo no código**, fora do gettext.
- `utils/i18n.py` não é citado por nenhum teste.

A infraestrutura está completa e correta (`Gtk.Builder.set_translation_domain`,
cinco caminhos de fallback, catálogos embutidos no wheel). O que falta é o texto
passar por ela.

---

## Ordem sugerida

| # | Item | Por quê primeiro |
|---|---|---|
| 1 | **B1** — instalar as fontes | Afeta o que ela vê hoje. Uma linha no instalador |
| 2 | **A1** — gate de emoji | Portão que se anuncia fechado e está aberto |
| 3 | **C1+C2** — um arquivo de configuração lido de verdade | Resolve três buracos e uma contradição |
| 4 | **A3** — pôr os gates existentes no CI | Já estão escritos; falta rodá-los |
| 5 | **D** — paridade dos manifestos | Silencioso até alguém instalar por pacote |
| 6 | **B2, B3, B4** — faxina do instalador | Baixo risco, baixo ganho imediato |
| 7 | **E** — migrar os ~71 asserts de texto | Trabalho grande e independente |
| 8 | **F** — i18n | Só quando houver alguém para ler em outra língua |

## Como você valida

Nenhum item aqui se valida olhando a janela, com **uma exceção**: depois de B1,
a tipografia da janela muda visivelmente — é a fonte do desenho, pela primeira
vez. Todo o resto se valida rodando gate e vendo reprovar o que deve reprovar.

## O que NÃO foi medido

- **Não rodei o `check_packaging_parity.sh`.** Sei que ele não está em workflow
  nenhum; não sei se ele **passa** hoje. Pode haver mais divergência do que os
  dois casos do bloco D.
- **Não conferi os manifestos de Arch e Fedora item a item** além das regras
  udev. Pode faltar mais coisa.
- **Não medi o custo de ligar as fontes.** `install_fonts.sh` existe e tem plano
  A e plano B, mas nunca foi executado nesta máquina — não sei se funciona.
- **Não sei se o gate de emoji já existiu e foi removido**, ou se nunca foi
  escrito. Medi a ausência hoje; não fui ao histórico procurar um commit que o
  tivesse apagado. A resposta muda o texto do ADR-011, não a entrega.
- **Não varri o repositório inteiro atrás de outros emojis.** Achei o U+2B50 em
  dois lugares porque o estudo passou por aquele arquivo. Sem gate, não há
  número — e produzir esse número é a primeira coisa que o gate faz quando
  existir.
