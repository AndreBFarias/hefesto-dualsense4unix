# CR-05 — O NOTICE lista tudo que vem de fora, ou não vale nada

**Status:** ENTREGUE em 2026-07-31, com **uma caixa aberta** e **uma hipótese
refutada** (as duas nomeadas ao final)
**Depende de:** CR-01
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Fazer o `NOTICE` declarar **toda** a proveniência de terceiros do projeto, não
só a parte que foi lembrada.

## Por que isto importa mais do que parece

Um `NOTICE` incompleto é pior que nenhum. Ele afirma implicitamente "eis o que
vem de fora" — e cada omissão vira uma inconsistência que enfraquece o
documento inteiro, inclusive as partes corretas. A seção de recusa criada na
CR-01 perde força se o leitor encontrar material de terceiro não declarado três
diretórios adiante.

Não há suspeita de irregularidade aqui. GPL-2.0 é a licença mais conhecida do
mundo, os fontes DKMS trazem cabeçalho, e o projeto os mantém como patch sobre
baseline registrado — o que é a forma correta. O que falta é a **declaração**.

## O que precisa ser auditado e declarado

- [x] **`assets/dkms/hid-nintendo/`** — declarado no `NOTICE`. Medido:
      `hid-nintendo.c:1` traz `GPL-2.0+`, `hid-ids.h:1` traz `GPL-2.0-or-later`
      e `hid-nintendo.c:3299` traz `MODULE_LICENSE("GPL")`. Os quatro patches
      próprios estão nomeados, um a um, no `NOTICE`.
- [x] **`assets/dkms/hid-playstation/`** — declarado. `hid-playstation.c:1` e
      `hid-ids.h:1` trazem `GPL-2.0-or-later`; `:3132` traz
      `MODULE_LICENSE("GPL")`. Dois patches próprios, nomeados.
- [x] **`assets/dkms/rtw88-usb/`** — declarado, e **corrigindo o enunciado
      original desta sprint**: não é GPL-2.0 pura. `usb.c:1` e os onze
      cabeçalhos trazem `GPL-2.0 OR BSD-3-Clause`, e `usb.c:1504` traz
      `MODULE_LICENSE("Dual BSD/GPL")`. É licença **dupla** — quem redistribui
      escolhe um dos dois termos —, e escrever "GPL pura" no `NOTICE` seria uma
      declaração errada em documento que existe justamente para não errar.
- [x] **Os oito `.patch`** (item que a CR-SEQUÊNCIA-01 deixou anotado como não
      medido): nenhum tem cabeçalho SPDX próprio. Conferido arquivo a arquivo —
      são diffs sobre os fontes acima e seguem a licença do arquivo que
      modificam. Está escrito assim no `NOTICE`.
- [x] **Varredura do resto da árvore.** Feita em `assets/`, `scripts/`,
      `packaging/`, `flatpak/` e `src/`, por marcas de atribuição
      (`derivado de`, `adaptado de`, `based on`, `copyright (c)`,
      `SPDX-License`). Fora de `assets/dkms/`, o único material de terceiro é o
      `assets/70-ps5-controller.rules` — **que já estava declarado**. Também
      declarados agora, por completude: as fontes tipográficas (OFL 1.1,
      **não** vendoradas — `assets/fonts` não existe; o `install_fonts.sh` pega
      do pacote da distro ou baixa com commit pinado e SHA-256), os 38 SVG de
      `assets/glyphs/` (desenho próprio, os `_active` gerados por
      `scripts/generate_glyph_active.py`) e o crate do applet
      (`packaging/cosmic-applet/Cargo.toml:17`, MIT, sem vendorização).
- [x] **Dependências Python** (item que a CR-SEQUÊNCIA-01 apontou como não
      medido). Licenças lidas dos metadados instalados via `importlib.metadata`,
      não de memória. Todas MIT/BSD/Apache, **menos três**: `python-xlib` é
      LGPL-2.0-or-later e é **obrigatória**; `PyGObject` é LGPL-2.0-or-later
      (extra `[tray]`); e `python-uinput` é **GPL-3.0-or-later** (extra
      `[emulation]`). A `prometheus-client` (extra `[metrics]`) não estava
      instalada no ambiente da auditoria, então a licença dela **não foi
      medida** e o `NOTICE` diz isso em vez de afirmar.
- [x] **Verificar compatibilidade.** A separação está clara e agora está
      escrita: os módulos não são linkados ao Python, são fonte separada
      compilada no destino pelo DKMS, e o daemon fala com eles só pelas
      interfaces de espaço de usuário do kernel (`/dev/hidraw`, udev, sysfs).
      São obras separadas no mesmo meio de distribuição.

## O que esta sprint NÃO é

Não é caça a irregularidade. É higiene documental: o projeto usa material de
terceiro sob licenças que **permitem** esse uso, e o `NOTICE` deve refletir
isso por inteiro para que a seção de recusa (CR-01) tenha o peso que merece.

## Critério de conclusão

`grep` por qualquer arquivo de terceiro na árvore encontra a declaração
correspondente no `NOTICE`, com licença e modificações. Um leitor externo
consegue reconstruir a cadeia de proveniência sem abrir o histórico do git.

---

## A hipótese que a medição REFUTOU

A [CR-SEQUÊNCIA-01](2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md)
abriu a execução desta sprint com uma "medição que evita alarme falso":

> *"o vetor de redistribuição é o tarball mais o instalador —
> `packaging/arch/PKGBUILD` **não** empacota `assets/dkms` (só
> `optdepends 'dkms'`, linha 56), e `grep -rln dkms .github/workflows/` devolve
> vazio. Nenhum pacote binário publicado carrega os fontes GPL."*

**A conclusão está errada.** Os dois greps citados saem exatamente como
descrito, e mesmo assim a conclusão não se sustenta — os dois são falso
negativo:

- a linha 56 do `PKGBUILD` fala da **ferramenta** `dkms` em `optdepends`. Quem
  empacota os fontes são as linhas **156-169** do mesmo arquivo
  (`cp -a assets/dkms/hid-nintendo/.` e as outras duas);
- o `grep` em `.github/workflows/` sai vazio porque quem copia os fontes é o
  `scripts/build_deb.sh` **chamado** pelo workflow (`release.yml:155`), não o
  workflow.

O que a medição de 31/07 encontrou, alvo por alvo:

| Artefato publicado | Carrega `assets/dkms/`? | Como foi medido |
|---|---|---|
| sdist `.tar.gz` | **Sim, os 36 arquivos** | lista de arquivos pedida ao próprio `hatchling` (`SdistBuilder.recurse_included_files`) |
| tarball de fonte da tag `v0.4.0` | **Sim, os 36** | `git archive v0.4.0 \| tar -t` |
| `.deb` | **Sim** | `scripts/build_deb.sh:246-262`, publicado por `release.yml:155` e `:416-421` |
| `.flatpak` | **Sim** | `flatpak/br.andrefarias.Hefesto.yml:256-263` |
| `PKGBUILD` (Arch) | **Sim** | `packaging/arch/PKGBUILD:156-169` |
| `.spec` (Fedora) | **Sim** | `packaging/fedora/hefesto-dualsense4unix.spec:158-171` |
| wheel | Não | alvo `tool.hatch.build.targets.wheel` empacota só `src/` — zero arquivos, medido |
| AppImage | Não | `scripts/build_appimage.sh` não menciona `assets/dkms` |

**Isto não é um problema — é o contrário.** Redistribuir estes fontes é
precisamente o que a GPL-2.0 autoriza, e o projeto já fazia a parte difícil:
manter o SPDX intacto, registrar o commit de origem e o SHA-256 do fonte
original em cada `BASELINE`. O que faltava era a **declaração**, e é o que esta
sprint entregou.

O que muda com a refutação é o peso: a v0.4.0 não distribuiu os fontes GPL "por
acidente e sem alcance". Distribuiu em cinco dos sete alvos, dizendo `MIT` no
`LICENSE` e no `README`, sem ressalva. Por isso o texto entrou nos três
arquivos, e não só no `NOTICE`.

## A caixa que ficou ABERTA

- [ ] **Nenhuma cópia do texto da GPL-2.0 acompanha os fontes.** Medido: uma
      busca por `COPYING`/`*GPL*` na árvore não encontra nada — os únicos
      resultados estão dentro do `.venv`, que não é distribuído. A GPL-2.0, na
      seção 1, pede que quem distribui o fonte *"dê a qualquer outro
      destinatário do Programa uma cópia desta Licença junto com o Programa"*.
      Os avisos SPDX estão preservados, que é a outra metade da exigência; a
      cópia do texto, não.

      **Remédio, e é pequeno:** um `LICENSES/GPL-2.0.txt` (texto canônico, sem
      modificação) referenciado pelo `NOTICE`, mais uma linha em cada um dos
      cinco alvos de empacotamento que já copiam `assets/dkms/`.

      **Por que não foi feito aqui:** criar `LICENSES/` estava fora da lista de
      arquivos desta frente, e tocar nos cinco alvos de empacotamento também. É
      trabalho de outra frente, com o `check_packaging_parity.sh` para cobrar a
      simetria.
