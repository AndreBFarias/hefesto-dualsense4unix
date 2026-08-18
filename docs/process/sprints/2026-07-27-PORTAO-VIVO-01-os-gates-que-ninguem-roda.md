# PORTÃO-VIVO-01 — os gates que ninguém roda

- **Status:** **ENTREGUE — os gates rodam no CI desde `f319c6f`** (medido em
  31/07: os sete portões executados direto pelos scripts saem **exit 0**, e o job
  `pre-commit` do `ci.yml` os roda a cada push). Ressalva registrada, não defeito:
  `core.hooksPath` global desta máquina aponta para `~/.config/git/hooks`, então
  **commit local nunca é barrado por portão** — quem barra é o CI
- **Prioridade:** ALTA
- **Aberta em:** 27/07/2026, a pedido dela: *"quero que vc melhore as sprints de
  tal forma que seja impossível o projeto quebrar novamente"*
- **Natureza:** guarda-chuva de proteção. Cada bloco é independente e pode entrar
  sozinho
- **Regra que a governa, já escrita nesta casa:** *"um gate que ninguém pode
  satisfazer não protege nada — só ensina a ignorá-lo"* (`845295b`). E a irmã
  dela: **um gate que ninguém roda não é gate, é arquivo**

## O fato que resume a sprint

**Não há portão nenhum rodando no caminho do commit deste repositório.**

```
ls .git/hooks/ | grep -v sample   ->  0 arquivos
command -v pre-commit             ->  AUSENTE
.pre-commit-config.yaml           ->  3 hooks declarados, 0 executados
```

Os três hooks declarados — `acentuacao-strict`, `anonimato`, `ruff-check` — nunca
rodaram nesta máquina. A única coisa que toca os arquivos no commit é o
higienizador do ambiente, que é justamente a que **não reprova** (ver
[GATE-EMOJI-01](2026-07-27-GATE-EMOJI-01-o-higienizador-apaga-o-que-o-adr-protege.md)).

E há uma armadilha a mais, medida no hook global: a **mera existência** do
`.pre-commit-config.yaml` faz `~/.config/git/hooks/pre-commit:51` marcar
`HAS_FRAMEWORK=true`, e `:165` desligar as próprias checagens dele (compilação
Python e espaço em branco) para delegar a um framework **que não está instalado**.
O arquivo de configuração desliga a proteção que deveria substituir.

## Bloco A — o gate de acento é cego a f-string, e a máquina fica verde

**Reproduzido nesta sessão, 27/07, com o gate real.** Arquivo de teste com o
mesmo erro em duas linhas:

```python
msg   = f"a configuracao nao tem acao"    # linha 2 — f-string
outra =  "a configuracao nao tem acao"    # linha 3 — string normal
```

Saída de `scripts/validar-acentuacao.py` no Python 3.12.3 desta máquina:

```
3 violação(es) de acentuação PT-BR encontrada(s).
  /tmp/teste_fstring.py:3:acao -> sugestão ação
  /tmp/teste_fstring.py:3:nao -> sugestão não
  /tmp/teste_fstring.py:3:configuracao -> sugestão configuração
```

**Três violações na linha 3. Zero na linha 2.** O texto errado é idêntico.

**Causa:** `scripts/validar-acentuacao.py:604` só considera tokens `COMMENT` e
`STRING`. A partir do Python 3.12 o `tokenize` emite `FSTRING_START`,
`FSTRING_MIDDLE` e `FSTRING_END` para f-strings — que escapam do filtro. O
conteúdo volta mascarado como espaços e o gate não vê nada.

**Por que isso já custou caro:** `ci.yml:32` pina **3.11** no job de acentuação,
onde f-string ainda é um `STRING` único e o gate enxerga. Resultado: verde na
máquina dela, vermelho na main. Foi essa assimetria que produziu seis commits
corretivos em 29 minutos em 25/07.

**Entrega:** corrigir `:604` para aceitar os tokens de f-string, e pôr o job de
acentuação na **mesma matriz de versões** que o job de teste já usa
(`ci.yml:83`), em vez de uma versão pinada.

**Prova de que morde:** a linha 2 do exemplo acima tem de reprovar no 3.12.

**Bônus no mesmo passe:** `validar-acentuacao.py:833` chama `git ls-files -z`
sem `--others --exclude-standard`. O modo `--all` é **cego a arquivo novo** ainda
não adicionado ao índice — ou seja, dá verde justamente no arquivo que ninguém
revisou ainda.

## Bloco B — o caminho do commit não tem portão, e `pre-commit install` não é a saída

`git config --get core.hooksPath` devolve `~/.config/git/hooks`. Com isso setado,
**o git nunca executa `.git/hooks/*`** — o próprio hook global documenta isso em
`:227-228` — e a ferramenta `pre-commit` recusa instalar.

Então o caminho não é instalar a ferramenta e torcer. São dois, e o segundo é o
que realmente protege:

1. **Delegação:** o hook global já tem o mecanismo em `:235`, com guarda
   anti-recursão. O que falta é ele detectar a **instalação** de verdade
   (`grep -q pre-commit .git/hooks/pre-commit`) em vez da mera existência do YAML
   — hoje a existência do arquivo desliga as checagens próprias dele sem ligar
   nenhuma outra.
2. **Rede no servidor:** um job `pre-commit run --all-files` no CI. É o único que
   sobrevive a qualquer mudança no ambiente da máquina, e é a razão pela qual ele
   é obrigatório mesmo se a delegação funcionar.

**Prova de que morde:** commitar um `.py` com acentuação errada. Hoje passa.

## Bloco C — o CI não vê este ramo

`ci.yml:4-5` dispara em `push` apenas para `main`. Há `pull_request:` sem filtro
(`:6`), o que **cobriria** qualquer ramo — mas o fluxo declarado da casa é merge
direto em `main` sem PR (`.github/CONTRIBUTING.md:9`). Na prática: nada roda até
já estar na `main`.

Medido: este ramo tem commits desde a `v0.2.0` e **zero workflow** rodou sobre
eles.

**Entrega:** ou acrescentar os ramos de trabalho ao gatilho de `push`, ou adotar
PR para as levas. As duas resolvem; a escolha é de fluxo, não técnica.

## Bloco D — o workflow que produz o artefato é o que verifica menos

`release.yml:46-52` roda `check_anonymity.sh`, `ruff` e `pytest tests/unit`.
Não roda: `mypy` (que o `ci.yml:140` roda), `validar-acentuacao --all`
(`ci.yml:34`), `check_test_data.sh` (`:23`), `check_version_consistency.py`
(`:43`) nem `pytest tests/core`. E como o `ci.yml` não dispara em tags, o push da
tag não chama o CI.

**Prova de que morde:** dessincronizar de propósito a versão do fallback em
`__init__.py` contra o `pyproject.toml` e tentar publicar. O release tem de
reprovar. Hoje passa — e a `v0.2.0` saiu exatamente por esse caminho.

## Bloco E — gates escritos que não estão em workflow nenhum

| Gate | Tamanho | Onde roda hoje |
|---|---|---|
| `scripts/check_packaging_parity.sh` | 312 linhas | **em lugar nenhum** |
| `shellcheck` sobre `scripts/` | — | não existe |

O primeiro é a guarda mais forte contra regressão de empacotamento. Travá-lo
agora é barato **porque ele está verde hoje**; depois que alguém acrescentar uma
regra udev nova, o custo de descobrir a divergência sobe.

O segundo cobre cerca de 40 scripts que rodam com `sudo` na máquina dela —
`doctor.sh` sozinho tem 150 KB. Zero linters passam por eles hoje. É a classe de
furo do `uninstall.sh --help` que desinstalava tudo. Começar em `-S error` para
não afogar em avisos, e apertar depois.

## Bloco F — o gate que faltava: documento que cita o que não existe

Esta é a classe de defeito que já infectou o próprio processo:

- `docs/adr/011-glyphs-vs-emojis.md:18` afirma que *"o hook `guardian.py` cobre os <!-- ref-externa: a ausência deste arquivo é o achado do bloco F -->
  proibidos"*. `find . -name guardian.py` devolve **zero**.
  **Pago em 2026-07-27**, depois de o portão ter reprovado com isto no lugar: o
  ADR-011 passou a citar `scripts/validar-glifos.py`, que existe e faz o que o
  nome imaginário prometia.
- Três sprints são citadas no índice com prioridade e número de linha e **não têm
  arquivo** nesta árvore.
- Três identificadores existem só em mensagem de commit — `MIC-FAIXA-01`,
  `SLOT-JOGADOR-01`, `VÃO-01` (este documento resolve o terceiro).

Um script varrendo `docs/` atrás de caminhos, comandos e métodos que não existem
no repositório.

**Prova de que morde:** ele tem de reprovar **hoje**, sem nenhuma alteração, nas
duas primeiras linhas desta lista. Se passar no repositório como está, está cego.

## O limite honesto desta sprint

**Nenhum gate desta lista teria pego o rollback de 26/07.** Aquela leva tinha 60
arquivos e 8902 inserções, cada mudança defensável isoladamente, e o que reprovou
foi ela olhando por dois minutos. Automação pega regressão mecânica; não pega
"isso ficou pior".

É por isso que esta sprint tem um par obrigatório:
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
Sem ela, o conjunto de portões dá uma sensação de segurança que os números não
sustentam.

## O que NÃO foi medido

- **Se `check_packaging_parity.sh` continua verde.** Rodou verde num levantamento
  desta sessão; não repeti a execução.
- **Quantos avisos o `shellcheck` produz.** Sem rodar, não sei se `-S error` é
  piso confortável ou se já reprova hoje.
- **Se ligar o CI em ramos estoura minuto de Actions.** A matriz atual é larga.
- **Os 734 testes de interface que pulam no CI.** Continuam pulando depois desta
  sprint. A camada onde a leva de 26/07 quebrou segue sendo a menos coberta — e
  os testes de layout usam `importorskip("gi")`, o que faz o pulo ser **silencioso**
  em vez de falha.
