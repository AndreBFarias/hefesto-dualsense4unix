# PUBLICAÇÃO-FIEL-01 — o que a release conta de errado

- **Status:** ABERTA — documento de medição e plano. Nada de código nesta rodada
- **Prioridade:** MÉDIA. Nenhuma entrega conserta a v0.4.0 que já saiu: o que foi
  baixado está baixado. Todas evitam que a próxima repita, e duas fecham defesa
  que hoje **não está armada**
- **Aberta em:** 31/07/2026, a partir da auditoria de treze agentes sobre o
  `HEAD 7bd0cb7` da branch `restauro/inicio-da-sessao`, com a **v0.4.0
  publicada** em 30/07 e os seis artefatos no ar
- **Tudo remedido hoje:** cada linha citada abaixo foi reconferida no arquivo de
  hoje, e cada `gh api` foi rodado de novo em 31/07. Onde o número do auditor
  não bateu, ele está corrigido **e a correção está dita**
- **Relacionada:**
  [auditoria geral de 31/07](../estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md),
  que classificou esta área como *"motor bom, metadado mentindo"*
- **Também relacionada:**
  [PORTÃO-VIVO-01](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md) (a
  sprint que ensinou esta casa a rodar os portões que ela escreve),
  [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md)
  (a `main` local que aponta para o repositório de outra pessoa) e
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
- **Rodada:** faz parte da leva de sprints de 31/07, junto com a
  [CARD-OCUPA-01](2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md)

## Antes de tudo: o motor está bom, e isso muda a leitura das entregas

Nada nesta sprint diz que a máquina de publicar está quebrada. Ela não está, e
os quatro fatos abaixo foram medidos hoje, não copiados de um documento antigo.

| O que | Onde | Medido em 31/07 |
|---|---|---|
| A matriz de Python é 3.10 / 3.11 / 3.12 nos **dois** jobs | `.github/workflows/ci.yml:53-56` (acentuação) e `:184-186` (lint-test) | as três versões veem exatamente a mesma coisa |
| A cegueira do gate de acentuação a f-string do 3.12 está **curada** | `scripts/validar-acentuacao.py:619-621` — `getattr(tokenize, "FSTRING_MIDDLE", None)` entra em `tipos_texto` quando existe | o erro que reprovava no 3.11 e passava no 3.12 não volta em silêncio |
| O job `Interface com GTK REAL (python3-gi + Xvfb)` existe e **prova a typelib antes de coletar** | `ci.yml:277-393`; a prova em `:336-353` reprova com `typelib PARCIAL, ausentes: ...` | a armadilha do typelib parcial derrubando a coleta inteira está fechada por um passo que fala |
| O guarda de CI é **fail-closed** e recusou 4 runs vermelhos da v0.4.0 | `release.yml:296-361`; runs `30561655419`, `30561901703`, `30562674307`, `30564059482` | nos quatro, o job `Guarda — o ci.yml desta SHA tem de estar verde` saiu `failure` e o `github-release` saiu `skipped` |
| Os **seis** artefatos saíram | `gh release view v0.4.0` | AppImage, flatpak, dois `.deb` (py310 e py312), wheel e sdist, publicados em 30/07 às 17h24 UTC |

E o portão de versão passa hoje: `python scripts/check_version_consistency.py`
devolve `OK: 9 alvo(s) versionado(s) em 0.4.0`, exit 0.

**As seis entregas abaixo são metadado que mente e defesa que não está armada.**
Nenhuma delas toca no motor. Duas são de uma linha.

## O que a release de 30/07 conta, e o que é verdade

| Peça publicada | O que ela conta | O que é verdade |
|---|---|---|
| `flatpak/br.andrefarias.Hefesto.metainfo.xml:20` | a 0.4.0 saiu em **28/07** e trouxe o desempate de perfis, o teto de prioridade e a aba Status | isso é a **0.3.0** (`CHANGELOG.md:75`). A 0.4.0 saiu em 30/07 (`CHANGELOG.md:8`; tag anotada `v0.4.0` de 2026-07-30 14:16:31 -0300) |
| a série de releases do mesmo arquivo | 0.4.0, 0.2.0, 0.1.1, 0.1.0 | a 0.3.0 existe, foi publicada, e **sumiu da série** |
| `README.md:14` | um badge de CI | uma imagem quebrada: a URL tem colchetes literais |
| `README.md:89` | o comando de clone | endereço impossível — ninguém copia e cola |
| `docs/usage/instalacao.md:29-30` e `:40` | *"A versão corrente é a alfa 0.3.0"*, `git checkout v0.3.0` | a corrente é a 0.4.0, e as outras duas páginas de uso já dizem isso |
| `README.md:13` | `testes-6089` | 6097 coletados hoje |

## E1. O AppStream anuncia a 0.4.0 com a data e o texto da 0.3.0

`flatpak/br.andrefarias.Hefesto.metainfo.xml:20` é, literalmente:

```
<release version="0.4.0" date="2026-07-28">
```

e a descrição dela, `:21-35`, começa com *"A leva do que desfazia o trabalho
dela"* — que é a frase de abertura da seção `## [0.3.0] — 2026-07-28` do
`CHANGELOG.md:75-77`, com o desempate alfabético, o teto da escala subindo de
100 para 200 e a aba Status reorganizada. Nada disso é a 0.4.0, cuja seção mora
em `CHANGELOG.md:8-72` e fala do R1 que trocava de aplicativo, do interruptor de
teclado e do caminho do `.deb`.

`grep '<release ' ` no arquivo devolve quatro entradas: `:20` (0.4.0), `:37`
(0.2.0), `:48` (0.1.1) e `:57` (0.1.0). **A 0.3.0 não está lá.**

### A arqueologia, porque ela diz o que consertar

Dois commits do dia 30/07, com três minutos entre eles:

| Commit | Hora | O que fez no metainfo |
|---|---|---|
| `665aff7` | 12h57 | criou o bloco 0.x inteiro, e a primeira entrada era `<release version="0.3.0" date="2026-07-28">` — **correta naquele momento** |
| `1534f7c` | 13h00 | o commit do bump para 0.4.0. Tocou 13 arquivos. No metainfo mudou **uma linha**: `version="0.3.0"` virou `version="0.4.0"`. A data ficou. A descrição ficou. Nenhuma entrada nova nasceu |

O diff do `1534f7c` neste arquivo é `1 insertion(+), 1 deletion(-)`.

**E dá para ver por que a edição foi essa e não outra.** O portão lê só o
primeiro casamento de `<release\s+version="([^"]+)"` e compara o **número** com
o `pyproject.toml` (`scripts/check_version_consistency.py:59-63`). Trocar o
número na entrada que já existia é a menor edição possível que deixa o portão
verde. **A régua desenhou o conserto.**

### Onde eu corrijo o auditor

O auditor chamou a régua de `METAINFO-VERSAO-RANCOSA-01`. Esse identificador não
existe nesta árvore. O nome real é **`VERSOES-RANCOSAS-01`**, escrito em
`scripts/check_version_consistency.py:15` e em
`tests/unit/test_versoes_rancosas_e_seed_flatpak.py:3`, e ele nasceu em 30/07
justamente porque o metainfo anunciava a 3.13.3 de 14/07 para a loja. A régua
curou o atraso de **duas semanas** e deixou passar o de **dois dias** — porque
ela confere número, e só.

### O CI valida este arquivo, e não pega isto

`.github/workflows/flatpak.yml:44-47` roda `appstreamcli validate --no-net`
sobre o metainfo, e o job dispara quando `flatpak/**` muda. Rodei o mesmo
comando nesta máquina em 31/07:

```
I: br.andrefarias.Hefesto:152: developer-name-tag-deprecated
I: br.andrefarias.Hefesto:~: developer-info-missing
Validação bem sucedida: infos: 2, pedante: 1
```

exit 0. Ele valida **sintaxe**. Não tem como saber em que dia a versão saiu.

### A entrega

1. Escrever a entrada própria da 0.4.0: data `2026-07-30` (a da tag anotada) e
   resumo tirado do `CHANGELOG.md:8-72`.
2. Devolver a 0.3.0 à série, com `date="2026-07-28"` e o texto que já esteve
   ali — recuperável inteiro com `git show 665aff7:flatpak/br.andrefarias.Hefesto.metainfo.xml`.
3. Estender `scripts/check_version_consistency.py` para comparar também a
   **data** da primeira `<release>` com a data da seção correspondente do
   `CHANGELOG.md`.

**Aceite:** a primeira entrada é `<release version="0.4.0" date="2026-07-30">`,
a segunda é a 0.3.0 com `2026-07-28`, a série tem cinco entradas,
`appstreamcli validate --no-net` continua exit 0, e o portão de versão continua
exit 0.

**Mordida:** com o número certo e a data errada — exatamente o estado do disco
hoje — o portão estendido tem de **reprovar**. Está medido que o portão de hoje
dá verde neste estado: `python scripts/check_version_consistency.py` sai 0 com
`date="2026-07-28"` na entrada da 0.4.0. Segunda mordida: apagar a entrada da
0.3.0 da série faz reprovar um teste que exige, para cada título `## [X.Y.Z]` do
`CHANGELOG.md` a partir da 0.1.0, uma `<release version="X.Y.Z">` no metainfo.

**Risco:** baixo. É XML de metadado, fora do caminho de execução do daemon e da
janela. **Isto não passa pela tela dela:** o metainfo é o que uma loja de
software mostra a quem instala pelo Flatpak, e ela instala nativo. Se quiser
conferir com o olho, o arquivo é o citado acima e o texto é legível.

## E2. O `[REDACTED]` literal no README publicado — decisão dela

> **MEDIDO EM 31/07, 09h45, e isto muda a entrega inteira: o `[REDACTED]` não é
> erro de ninguém. É produzido por um hook global, a cada commit.**
>
> Ela decidiu nesta madrugada pela URL real do fork. A cura foi escrita, o
> `README.md` passou a trazer `github.com/[REDACTED]/...` nas três
> ocorrências — e o primeiro commit da leva devolveu tudo para `[REDACTED]`,
> com o aviso `[sanitizer] 4 arquivos: 7 identidade redactada`.
>
> A causa, lida no código: `~/.config/git/hooks/pre-commit` chama
> `~/.config/zsh/scripts/universal-sanitizer.py`, que em `:316-321` troca cada
> termo de identidade por `[REDACTED]` **em todo arquivo cuja extensão não
> esteja em `safe_config_ext`** (`.cfg`, `.ini`, `.toml`, `.yaml`, `.yml`,
> `.json`) **e cujo nome não esteja em `safe_names`** (`LICENSE`, `AUTHORS`,
> `CONTRIBUTORS`, `pyproject.toml`, `setup.cfg`). O `README.md` é `.md`: entra
> na peneira.
>
> **Prova executada, sem tocar no repositório:** copiei o `README.md` para o
> scratchpad e rodei o sanitizador nele. Saída: `1 arquivos: 4 identidade
> redactada`; `grep -c [REDACTED]` devolveu **0**, e as três URLs voltaram
> a `[REDACTED]`.
>
> **Consequência para esta entrega:** ela é **inexecutável dentro do
> repositório**. Editar o `README.md` é trabalho que o próximo commit desfaz em
> silêncio — e "silêncio" é a parte grave, porque a árvore fica dizendo uma
> coisa e o commit outra.
>
> **E editar o hook não resolve sozinho:** o self-heal do Ritual da Aurora
> reinstala os hooks globais de hora em hora (achado de 27/07, registrado como
> *"o autosync do `~/.config/zsh` mutila arquivos a cada 10 minutos"*). O hook
> tem dono, e o dono não é este projeto.
>
> **Os três caminhos reais, e a escolha é dela:**
>
> 1. **Acrescentar `README.md` ao `safe_names` do sanitizador** — é uma linha,
>    mas mexe em ferramenta de outra casa, e precisa sobreviver ao self-heal.
> 2. **Aceitar o marcador e parar de chamá-lo de defeito** — o `[REDACTED]` vira
>    comportamento declarado, com uma nota no README explicando que o dono real
>    aparece na própria página do repositório, e a entrega vira "documentar",
>    não "corrigir".
> 3. **Tirar a URL do caminho do sanitizador** — mover badge e comando de clone
>    para um arquivo `.yml`/`.json` incluído, ou usar link relativo onde o
>    GitHub permitir. Custa desenho e não cobre o badge.
>
> Enquanto ela não escolher, **o `README.md` fica como está**, e este bloco é a
> explicação de por quê. Fingir a cura seria a janela que mente, na versão
> repositório.

Sete ocorrências do literal `[REDACTED]` dentro de URL, em quatro arquivos:

| Arquivo:linha | O que quebra |
|---|---|
| `README.md:14` | o badge de CI da primeira tela do repositório: imagem quebrada |
| `README.md:89` | o `git clone` da seção de instalação: endereço impossível |
| `README.md:311` | o `git remote add fork` de quem clonou do repositório de origem |
| `docs/usage/instalacao.md:30` | a frase que nomeia o fork |
| `docs/usage/instalacao.md:38` | o `git clone` |
| `docs/usage/quickstart.md:36` | o `git clone` |
| `docs/usage/flatpak.md:40` | o `git clone` |

Conferido na tag publicada: `git show v0.4.0:README.md` traz as três de lá.
**O auditor listou cinco e citou `quickstart.md` e `flatpak.md`; as duas de
`docs/usage/instalacao.md` ficaram de fora da conta dele.**

### Onde eu discordo do auditor, com medida

O auditor escreveu que isto é *"o custo de a anonimização do owner vazar dos
docs de processo para o artefato público, sem decisão registrada"*. Medida a
árvore, a política **está** registrada, e é o contrário disso:

- `packaging/cosmic-applet/Cargo.toml:18-19` publica, em texto puro,
  `https://github.com/[REDACTED]/hefesto-dualsense4unix` — no `homepage` e
  no `repository`. Está na árvore **e dentro da tag v0.4.0**
  (`git show v0.4.0:packaging/cosmic-applet/Cargo.toml`).
- O comentário logo acima, `Cargo.toml:11-14`, escreve o padrão da casa: *"no
  mesmo padrão do `packaging/arch/PKGBUILD` (`Maintainer: Vitoria Maria
  <[REDACTED]>`): havia um e-mail pessoal real aqui"*. Ou seja, o marcador
  protege o **e-mail**.
- O nome real dela está publicado em pelo menos seis artefatos rastreados:
  `packaging/arch/PKGBUILD:1`, `packaging/cosmic-applet/Cargo.toml:15`,
  `packaging/fedora/hefesto-dualsense4unix.spec`, e os `.po`/`.mo` de `po/` e
  `locale/`.
- E **nenhum portão exige a redação da URL**. A lista de termos proibidos está
  em `scripts/check_anonymity.sh:25` e não tem nada parecido com um usuário do
  GitHub. Passei a URL real pela própria regex do portão: passa. E
  `bash scripts/check_anonymity.sh` sai 0 hoje, com o endereço já dentro do
  `Cargo.toml`.

Então não é vazamento de política: é o marcador que protege um e-mail aplicado a
uma URL, num repositório que já publica essa URL em outro arquivo. O custo é
concreto — badge quebrado na primeira tela e comando de instalação que ninguém
consegue copiar.

**Mesmo assim, a escolha é dela**, e não há ADR nos 19 de `docs/adr/` que
resolva. Dois caminhos honestos:

- **(A) URL real** no `README.md` e nas três páginas de uso, coerente com o que
  o `Cargo.toml:18-19` já publica. O badge volta a renderizar, o clone funciona.
- **(B) Marcador honesto** tipo `<SEU-FORK>` com uma linha dizendo onde achar o
  endereço. O badge continua quebrado e o clone continua não copiável, mas nada
  muda em exposição — o `Cargo.toml` já disse.

Seja qual for, **registrar num ADR novo em `docs/adr/`**, porque hoje a prática
existe em três formatos diferentes no mesmo repositório.

**Aceite:** zero ocorrências do literal `[REDACTED]` dentro de uma URL em
`README.md` e em `docs/usage/`. Se for o caminho (A), o badge de CI renderiza
verde na primeira tela do repositório — **e essa é a verificação de olho dela**,
abrir a página e ver a imagem, regra `PROVA-DE-TELA-01`.

**Mordida:** um teste que reprova `[REDACTED]` dentro de `https://github.com/`
em `README.md` e em `docs/usage/*.md`. Arrancada: devolver o marcador a uma URL
qualquer deixa vermelho. E a mordida tem de ser **estreita** — `[REDACTED]`
dentro de um campo de e-mail (`PKGBUILD:1`, `Cargo.toml:15`) precisa continuar
passando, senão o teste mata justamente a política que deveria proteger.

**Risco:** baixo tecnicamente e alto de escopo: **nada entra antes de ela dizer
(A) ou (B).** É a única entrega desta sprint que é decisão, não conserto.

## E3. A página de instalação manda instalar a v0.3.0 — e um teste VERDE proíbe consertar

`docs/usage/instalacao.md:29-30` diz *"A versão corrente é a alfa **0.3.0**
(29/07/2026) e o ponto de instalação é a **tag `v0.3.0`**"*, e `:40` manda
`git checkout v0.3.0`. Enquanto isso `docs/usage/quickstart.md:38` e
`docs/usage/flatpak.md:42` já dizem `git checkout v0.4.0`.

E esta é a página canônica: o `README.md:136` e o `README.md:279` apontam para
ela como *"instalação em detalhe"*.

O commit do bump, `1534f7c`, tocou `quickstart.md` e `flatpak.md` — uma linha em
cada, `v0.3.0` para `v0.4.0`. **Não tocou em `instalacao.md`.**

### O que reconferi e reenquadra a entrega

Existe um teste que **exige** a versão velha:

```python
    def test_aponta_a_versao_corrente_e_nao_a_branch_antiga(self) -> None:
        assert "sprint/harmonia-uhid" not in DOC
        assert "alfa 0.1.1" not in DOC
        assert "git checkout v0.3.0" in DOC
```

`tests/unit/test_install_respeita_o_nao_e_help_completo.py:276-279`, com `DOC` =
`docs/usage/instalacao.md` (`:38` e `:40` do mesmo arquivo de teste). Rodado
hoje: `pytest -k versao_corrente` devolve `1 passed`. **Quem atualizar a página
para v0.4.0 deixa este teste vermelho.**

É a classe de defeito que a auditoria de 25/07 chamou de teste-muralha: asserção
que congela o TEXTO de um artefato e passa a proibir a correção dele. As duas
primeiras linhas do teste são a metade honesta — elas proíbem a branch morta e a
versão antiga. A terceira congela.

Não dá para provar que o teste é a **razão** de a página ter ficado para trás; o
commit do bump simplesmente não a tocou. O que dá para provar é o que vale
daqui em diante: **a correção, hoje, reprova.**

### A entrega, em três partes

1. Atualizar as três linhas de `docs/usage/instalacao.md` para 0.4.0 e
   `v0.4.0` — inclusive a data na frase de `:29`.
2. Reescrever `test_install_respeita_o_nao_e_help_completo.py:276-279` para
   derivar a versão corrente do `pyproject.toml` (a mesma fonte de verdade do
   portão), mantendo os dois `not in`, que são a parte que morde de verdade.
3. Acrescentar as páginas de uso aos alvos de
   `scripts/check_version_consistency.py`. `instalacao.md` entra **duas vezes**,
   porque a versão aparece na prosa (`:29`) e no comando (`:40`), e o portão usa
   uma regex por alvo. Com `quickstart.md` e `flatpak.md` juntas, `_TARGETS` vai
   de 9 para 13.

**Aceite:** `python scripts/check_version_consistency.py` imprime
`OK: 13 alvo(s) versionado(s) em 0.4.0`, e as três páginas de uso dizem a mesma
versão que o `pyproject.toml`.

**Mordida:** devolver `v0.3.0` a qualquer uma das três páginas faz o portão sair
1 **nomeando o arquivo**. E a mordida do teste-muralha é o inverso: com a
asserção antiga restaurada, atualizar a página deixa a suíte vermelha — é essa
reprovação que prova que a muralha existia.

**Risco:** baixo no texto. O cuidado é o teste. Mexer numa asserção que está
**verde** é a forma que a trapaça tem nesta casa, então o corpo do commit
precisa dizer por que: a linha congelava a string de um artefato, e a nova
deriva da mesma fonte de verdade que o portão usa. Sem essa frase escrita, a
mudança parece o que ela não é.

## E4. O job `pypi` é o único caminho de publicação fora do guarda

`.github/workflows/release.yml:424-428`:

```yaml
  pypi:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    if: ${{ vars.PYPI_PUBLISH == 'true' }}
```

Compare com quem publica no GitHub, `release.yml:363-364`:
`needs: [build, appimage, deb, deb-install-smoke, flatpak, guarda-ci]`. O `pypi`
não depende do guarda nem do `github-release`.

Medido por mim em 31/07, e é o que segura a coisa hoje:
`gh api repos/.../actions/variables` devolve `{"variables":[],"total_count":0}`
— a variável `PYPI_PUBLISH` **não existe**; e `gh api repos/.../environments`
devolve `{"total_count":0,...}` — o `environment: pypi` também não.

### A prova de que isto não é hipótese

Run `30564059482`, de 30/07, na tag `v0.4.0`. Jobs, um por um:

| Job | Conclusão |
|---|---|
| `build` | success |
| `appimage` | success |
| `deb (ubuntu-22.04)`, `deb (ubuntu-24.04)` | success |
| `Build Flatpak bundle` | success |
| `Smoke install do .deb` (as duas) | success |
| `Guarda — o ci.yml desta SHA tem de estar verde` | **failure** |
| `github-release` | **skipped** — o guarda fez o trabalho dele |
| `pypi` | **skipped** |

O `pypi` foi pulado, mas **não pelo guarda**: o único `needs` dele, o `build`,
estava verde. O que segurou o wheel foi uma variável de repositório que ninguém
criou. Naquele dia, com `PYPI_PUBLISH` definida, o pacote teria ido para o PyPI
a partir de um run cujo guarda de CI havia **reprovado**.

E o teste estrutural que trava o desenho não acusaria: ele pergunta só pelo
`JOB_PUBLICACAO`, que é `"github-release"`
(`tests/unit/test_release_workflow_nomes_e_portoes.py:38`, usado em `:195-209`).

### A entrega

`needs: [build, guarda-ci]` no job `pypi`, e generalizar
`test_github_release_depende_do_guarda_de_ci` para exigir um guarda de CI em
**todo** job que publica para fora. O critério de "publica para fora" precisa
ficar escrito, não adivinhado: job cujos passos citam `gh release create`, ou
que usa uma action de `pypa/`, ou que declara `environment:`.

**Aceite:** o teste generalizado passa com `guarda-ci` no `needs` do `pypi`; e
ele afirma, além disso, que o conjunto de jobs "que publicam para fora" contém
pelo menos `github-release` e `pypi` — senão um dia o conjunto fica vazio por
renomeação e o teste passa medindo nada.

**Mordida:** tirar `guarda-ci` do `needs` do `pypi` reprova, **nomeando o
`pypi`**. Contraprova obrigatória: tirar `guarda-ci` do `needs` do
`github-release` continua reprovando — a generalização não pode perder o que o
teste de hoje já cobre.

**Risco:** baixo. Uma linha de YAML e um teste. O efeito colateral real e
desejado: o guarda espera até 45 minutos (`release.yml:319`,
`LIMITE_SEG=2700`), então o `pypi` passa a esperar o mesmo muro. É o preço, e é
o ponto. **Não dá para observar isto num run enquanto `PYPI_PUBLISH` não
existir** — o aceite é estrutural, medido pelo teste, e está dito.

## E5. O gate server-side de anonimato não bloqueia nada, e é fail-open no pior evento

O cabeçalho de `.github/workflows/anonymity-check.yml:7-9` promete:

> *"Quando marcado como required check em branch protection, falha do job
> bloqueia merge no main mesmo que o commit tenha sido criado com `--no-verify`
> localmente. Defesa server-side ultima."*

Medido por mim em 31/07, no fork:

```
gh api repos/[REDACTED]/hefesto-dualsense4unix/branches/main/protection
  -> 404 {"message":"Branch not protected"}
gh api repos/[REDACTED]/hefesto-dualsense4unix/rulesets
  -> []
```

Nada é required. O job reprova **depois** do push; não impede o push.

### E o segundo furo é pior, porque acontece no evento mais arriscado

`anonymity-check.yml:60-64`:

```bash
MAPFILE=$(git log --pretty=format:'%H' "$RANGE" 2>/dev/null || true)
if [ -z "$MAPFILE" ]; then
  echo "Nada a auditar (intervalo vazio)."
  exit 0
fi
```

O `$RANGE` vem de `:45` e é `${PUSH_BEFORE}..${PUSH_AFTER}`. Num force-push que
descarta história, o `before` pode virar um commit órfão que o checkout não tem
— aí o `git log` falha, o `|| true` engole, `MAPFILE` fica vazio e o job **sai
0 sem olhar commit nenhum**. Esta casa praticou force-push na `main` duas vezes:
a purga de MAC de 20/07 e a sobrescrita da main de 29/07.

Terceiro: o workflow só dispara em push e PR de `main` (`:11-15`). A varredura
de mensagens **nunca** roda em `restauro/**`, em `sprint/**` nem em tag — e a
tag é o que a release publica.

### A cura já existe nesta casa, sessenta linhas adiante

O guarda de CI usa o **mesmo** idioma `|| true`, e é fail-**closed**:
`release.yml:322-330` engole o erro da API, cai em `STATUS="ausente"` e, no
limite de tempo, `exit 1` (`release.yml:349-357`). Mesmo idioma, polaridade
oposta, mesmo repositório. Esta entrega é copiar a polaridade.

### A mitigação, medida, porque muda a prioridade

Hoje a história está limpa. `bash scripts/check_anonymity.sh` sai 0 na árvore de
31/07, e a varredura de autores, committers e taggers das 45 tags não achou
identidade nem trailer. **A defesa está desarmada; a casa não está suja.** Por
isso isto é MÉDIA e não urgência.

### A entrega

1. Criar um ruleset na `main` do fork exigindo o check `scan-commits`.
2. Tratar intervalo não resolvível como **erro**: se o `git log "$RANGE"` falhar,
   auditar `git log "$PUSH_AFTER"` (o mesmo tratamento que `:42-43` já dá ao
   primeiro push) e, se nem isso resolver, `exit 1` nomeando o intervalo.
3. Estender o gatilho para `branches: ['**']` e `tags: ['v*']`.

**Aceite:** `gh api .../rulesets` deixa de devolver `[]` e nomeia o check; um
push com trailer proibido é **recusado pelo servidor**, não reprovado depois; e
um intervalo não resolvível faz o job sair 1 com o intervalo escrito na
mensagem.

**Mordida:** a metade do fail-open é testável sem GitHub — extrair o passo de
intervalo para um script e testá-lo com `PUSH_BEFORE` apontando para uma SHA que
não existe no repositório: o script tem de sair diferente de zero. Hoje a linha
equivalente sai 0 com `Nada a auditar (intervalo vazio).`. Arrancada: devolver o
`|| true` seguido de `exit 0` reprova o teste. **A metade do ruleset não tem
teste — tem medição**, o `gh api` acima, e ela entra no documento da leva.

**Risco:** MÉDIO, e é a única entrega desta sprint que pode **travar ela**. Um
ruleset exigindo check na `main` significa: check quebrado ou run que não começa
e o push para a `main` não sai. Numa casa que trabalha em branch e publica por
tag o custo é baixo, mas tem de estar dito, e o ruleset precisa deixar bypass de
administradora — senão o primeiro falso positivo vira porta trancada. Vale
lembrar o que a [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md)
mediu: a `main` local desta máquina mira o `upstream`, que é o repositório de
outra pessoa. O ruleset não conserta isso e não é afetado por isso.

## E6. O badge de testes é pintado à mão, e já defasou

`README.md:13` é um shields.io estático:
`https://img.shields.io/badge/testes-6089-brightgreen.svg`.

Coleta medida hoje, 31/07, com o `.venv` da casa:
`pytest --collect-only -q` devolve `6097 tests collected in 1.94s`. **Oito de
diferença, um dia depois do lançamento.**

E o número é repintado a cada release, à mão:

| Commit | Badge |
|---|---|
| `ee1b309` | 1856 |
| `b92b5ad` | 2022 |
| `26456fa` | 4867 |
| `5115aac` | 5256 |
| `2597807` | 5529 |
| `464b7a2` | 5783 |
| `1534f7c` (o bump da 0.4.0) | 6089 |

Nenhum teste lê esse número: `grep` por badge em `tests/unit/*.py` só encontra o
badge de alvo de edição da janela, que é outra coisa.

**A entrega:** derivar, como já se faz com a versão. Duas rotas honestas — (i)
o badge para de carregar número exato (`6000+`) e ninguém repinta mais; ou (ii)
o badge vira alvo de portão, comparado contra `pytest --collect-only -q`.

**Cuidado medido, e ele escolhe a rota:** o número de coleta depende do
ambiente. Aqui são 6097 com GTK real; no `lint-test` do CI cerca de 210 testes
de interface PULAM — recuo consciente, documentado em `ci.yml:199-211` como
*"Estado HONESTO"*. Teste pulado ainda é teste **coletado**, então o número deve
se sustentar; mas "coletado" e "passou" são números diferentes, e o badge diz
`testes`. Qualquer rota exige que o badge diga o que conta.

**Aceite:** ou o badge deixa de carregar número exato, ou o portão reprova
quando `README.md:13` diverge da coleta em mais de zero.

**Mordida:** na rota (ii), trocar o badge para `6000` sem mexer na suíte faz o
portão reprovar. Na rota (i), a mordida é outra: um teste que reprova qualquer
número de quatro dígitos no badge de testes — senão alguém repinta de novo e a
rota se desfaz sozinha.

**Risco:** o mais baixo da lista. É uma linha do `README.md`.

## Registrado como risco latente, sem entrega obrigatória

Duas coisas verdadeiras que **não** viram entrega nesta sprint, e a razão está
escrita.

### As actions, todas pinadas por tag móvel

Censo dos quatro workflows, feito hoje:

| Action | Ocorrências |
|---|---|
| `actions/checkout@v4` | 24 |
| `actions/setup-python@v5` | 13 |
| `actions/upload-artifact@v4` | 8 |
| `actions/download-artifact@v4` | 8 |
| `pypa/gh-action-pypi-publish@release/v1` | 1 |

Zero pins por SHA. Tag maior é mutável, e o `release.yml:14-16` concede
`contents: write` e `id-token: write`. **Por que não vira entrega:** são todas
actions oficiais do GitHub e da pypa, e pinar por SHA cria dívida de manutenção
recorrente (cada bump precisa de um SHA novo) numa casa em que 41 de 50
cabeçalhos de sprint já mentem sobre o próprio estado. Fica registrado e volta à
mesa **no dia em que entrar uma action de terceiro**.

### O `flatpak.yml` divergente do `release.yml`

`.github/workflows/flatpak.yml:86-93` roda `flatpak-builder` **sem**
`--default-branch=stable`, e `:95-100` exporta `Hefesto-Dualsense4Unix.flatpak`
sem versão e sem a branch posicional. O `release.yml:248-256` e `:261-269` fazem
os dois: `--default-branch=stable` e o nome versionado com `stable` no fim. O
smoke de instalação do CI valida um bundle com ref `master` enquanto a release
publica `stable`.

**Correção ao auditor:** ele datou o arquivo como *"intocado desde 15/05"* pelo
`mtime`, e `mtime` num checkout é a hora do checkout. Pelo git, o último commit
que tocou `.github/workflows/flatpak.yml` é `bd6e6bf`, de **27/04/2026** —
três meses, não dois e meio.

**Por que não vira entrega:** o conteúdo construído é o mesmo, o risco é drift
futuro, e o teste estrutural só lê `RELEASE_YML`
(`tests/unit/test_release_workflow_nomes_e_portoes.py:35`). Se a E4 for feita, o
teste generalizado varrer os **dois** workflows custa quase nada — e é aí que
esta linha deve ser resolvida, de carona.

## Como você valida na tela

Quase nada desta sprint aparece na janela do Hefesto, e isso precisa estar dito.
O que aparece, aparece no navegador:

1. Abra a página do repositório no GitHub. **O badge de CI, no topo, é uma
   imagem quebrada** — é a E2. E a escolha entre a URL real e um marcador
   honesto é sua: nada entra antes de você dizer qual.
2. Na mesma tela, ao lado: o badge `testes-6089`. Hoje são 6097. É a E6.
3. Abra `docs/usage/instalacao.md` (no GitHub ou no editor). A primeira frase da
   seção "Do código-fonte" diz *"a alfa 0.3.0"*. Você publicou a 0.4.0. É a E3 —
   e as outras duas páginas de uso já dizem 0.4.0, então a página que está
   errada é justamente a que o README chama de "instalação em detalhe".
4. **Único passo que precisa de terminal:** copie o comando de clone do README e
   cole. Ele não funciona; o endereço tem colchetes literais.

E o que **não** dá para ver na tela, por natureza:

- A **E1** é o que uma loja de software mostra a quem instala pelo Flatpak. Você
  instala nativo, então essa tela não é a sua. A prova está no arquivo
  `flatpak/br.andrefarias.Hefesto.metainfo.xml`, linha 20.
- A **E4** e a **E5** são defesas, não telas. A prova da E4 é o run
  `30564059482` de 30/07, tabelado acima. A prova da E5 é o `gh api` que devolve
  `404` e `[]`.

## O que fica de fora, por escrito

- **Consertar a v0.4.0 que já saiu.** A tag é história e os seis artefatos já
  foram baixados. Nada aqui reescreve tag nem republica release. O que está
  publicado fica; o que muda é a próxima.
- **O `[REDACTED]` nos documentos de processo** e em `docs/tags-arquivo-pre-1.0.txt`.
  O `scripts/check_anonymity.sh` exclui `docs/process/**` de propósito, e
  ninguém clona a partir de uma sprint. O escopo da E2 é só o artefato público:
  `README.md` e `docs/usage/`.
- **O e-mail pessoal.** `packaging/arch/PKGBUILD:1` e
  `packaging/cosmic-applet/Cargo.toml:15` mantêm `<[REDACTED]>` e continuam
  assim. Essa é a política que esta sprint **lê**, não uma que ela mude.
- **Pinar actions por SHA** e **alinhar o `flatpak.yml`**: as duas pendências
  acima, com a razão escrita.
- **Os ~210 testes de interface que pulam no CI.** Recuo consciente e declarado
  em `ci.yml:199-211`, com o job `gtk-real` cobrindo sob Xvfb os arquivos que
  carregam a guarda. É assunto de outra sprint, não desta.
- **O `github-release` apagar a release antes de recriar** (`release.yml:412-415`).
  É idempotência deliberada e comentada, para o re-run da mesma tag não falhar
  com "release already exists". A consequência conhecida — se o `create` falhar
  depois do `delete`, a release fica fora do ar até um re-run verde — é decisão
  registrada, não lapso. Fica anotada, sem entrega.
- **Mexer no guarda de CI.** Ele funciona, está medido funcionando quatro vezes
  e é a peça que impediu a v0.4.0 de sair vermelha. A E4 **acrescenta** quem
  depende dele; não mexe nele.

## O que eu não medi

- **O conteúdo dos seis artefatos publicados.** Não baixei nem instalei o
  `.deb`, o AppImage, o flatpak ou o wheel. O que conferi foi a lista de nomes e
  a data de publicação, por `gh release view v0.4.0`.
- **Como o metainfo aparece de fato numa loja de software.** Rodei o
  `appstreamcli validate --no-net` aqui e ele sai 0 — isso diz que o XML é
  válido, não o que o GNOME Software desenha na tela.
- **O fail-open do anonimato sob um force-push real.** Li o script e percorri o
  caminho linha a linha; **não** empurrei nada contra o GitHub para ver o runner
  se comportar. A regra desta rodada é leitura, e force-push é mutação.
- **Se alguma variável de organização define `PYPI_PUBLISH` por herança.** Medi
  só as do repositório, e estão vazias.
- **O guarda de CI sob erro transitório prolongado da API do GitHub.** Está lido
  no código (cai em "ausente" e retenta até 45 minutos, `release.yml:319-357`);
  não simulei.
- **Se a política do `[REDACTED]` tem registro fora do repositório.** Dentro
  dele não há ADR — são 19 em `docs/adr/`, nenhum sobre isso. E não perguntei a
  ela: a E2 **é** essa pergunta.
- **Os logs passo a passo dos runs.** Medi conclusões por job com
  `gh run view`; não abri o log de cada passo.
- **Se o número de coleta se sustenta no runner do CI.** Os 6097 são desta
  máquina, com GTK real. A E6 depende disso e o cuidado está escrito lá.
