# GATE-EMOJI-01 — o higienizador apaga o que o ADR-011 manda preservar

- **Status (09/08/2026):** **ENTREGA 2 ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA
  DELA.** O portão existe, roda no CI e no pre-commit, e tem teste de
  mordida. Entregue por `e96dea8` (27/07/2026) — **o mesmo commit que escreveu
  esta sprint**. A **Entrega 1 continua ABERTA e é indeterminável daqui**: mora
  no `$HOME` dela, fora do repositório. Conferência item a item na
  [nota datada de 09/08/2026](#nota-datada-09082026--o-portão-que-esta-sprint-diz-faltar-nasceu-com-ela), no fim
- **O que falta ela validar, em uma linha:** colar um emoji num arquivo do
  projeto, salvar pelo editor dela, e ver se o higienizador do zsh **deixou** os
  glifos que o ADR-011 protege em pé — é o lado de fora do repositório, e só a
  máquina dela responde
- **Status anterior:** ABERTA (assim desde 27/07/2026). O rótulo **não se
  apaga**: ele é o próprio assunto da nota datada. Sprint marcada como aberta é
  lida como dependência viva, e esta passou treze dias anunciando a falta de um
  portão que nasceu junto com ela
- **Prioridade:** ALTA
- **Aberta em:** 27/07/2026, a pedido dela: *"temos a parte dos anti emojis que
  tá quebrando o projeto pq o zsh não tá funcionando corretamente"*
- **Decisão dela, 27/07:** curar os **dois** lados — o higienizador do ambiente
  **e** o portão do repositório
- **Sucede:** o bloco A1 de
  [PROMESSA-NAO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md),
  que diagnosticou a ausência do gate. Esta sprint mede o outro lado do defeito e
  fecha os dois

> **Aviso de escrita, e ele é parte do conteúdo.** Nenhum glifo deste documento
> aparece desenhado — todos estão citados por codepoint. Escritos como caractere,
> o higienizador apagaria a própria tabela que documenta o que ele apaga. Isso já
> aconteceu três vezes em 26/07, e a terceira apagou a frase que narrava as duas
> primeiras.

## A frase dela está certa, e o mecanismo é mais estreito do que "não funciona"

O `zsh` não está quebrado. O que existe é uma **inversão exata**, em uma única
expressão regular:

> O higienizador **apaga o que o ADR-011 manda preservar** e **deixa passar o que
> o ADR-011 proíbe.**

## A medição

### O que o ADR-011 protege, por escrito

`docs/adr/011-glyphs-vs-emojis.md:14` lista os blocos **permitidos**, e nomeia os
exemplos canônicos do projeto:

| Bloco | Faixa |
|---|---|
| Geometric Shapes | U+25A0 a U+25FF |
| Block Elements | U+2580 a U+259F |
| Box Drawing | U+2500 a U+257F |
| Arrows | U+2190 a U+21FF |

Exemplos que o próprio ADR nomeia: U+25CF, U+25CB, U+25AE, U+25AF, U+25D0.

### O que o higienizador apaga

`~/.config/zsh/scripts/universal-sanitizer.py:40-69` define `EMOJI_RE`. Duas
faixas dele caem **dentro** dos blocos protegidos:

| Faixa no regex | Linha | Invade | Veredito |
|---|---|---|---|
| U+2194 a U+21AA | :60 | Arrows | apaga o permitido |
| U+25AA a U+25FE | :61 | Geometric Shapes | apaga o permitido |

A segunda faixa cobre **os cinco codepoints que o ADR-011 nomeia um a um**.

E o inverso, medido: **U+2B50 (WHITE MEDIUM STAR) não está em faixa nenhuma do
`EMOJI_RE`.** É Emoji_Presentation, é proibido pelo critério objetivo do ADR-011,
e está commitado vivo em `docs/usage/troubleshooting-8bitdo.md`, linhas 29 e 48.

### O estrago potencial, contado

Varredura sobre `git ls-files`, contando só ocorrências que o `EMOJI_RE` apagaria
**e** que o ADR-011 protege:

```
ARQUIVOS versionados atingidos:   5
OCORRENCIAS apagadas em silencio: 222

  172  docs/history/glyph-strip-regression-2026-04-23.diff
   20  src/hefesto_dualsense4unix/tui/widgets/__init__.py
   20  tests/unit/test_tui_widgets.py
    9  tests/unit/test_validar_acentuacao_glyphs_defense.py
    1  tests/unit/test_touchpad_keyboard.py

por codepoint:  U+25AE 56   U+25CF 48   U+25AF 48   U+25CB 40
                U+25D0 21   U+25B3  8   U+2194  1
```

Os três primeiros arquivos dessa lista são, nesta ordem: **o registro histórico
do incidente que originou o ADR-011**, **o código de produção que o ADR protege**
e **o teste que existe para detectar essa regressão**.

### O pior caso não é hipotético

`src/hefesto_dualsense4unix/tui/widgets/__init__.py` e
`tests/unit/test_tui_widgets.py` guardam **os mesmos literais**. Se as duas
alterações entrarem no mesmo commit — que é o caso normal, porque quem mexe no
`BatteryMeter` mexe no teste dele —, o higienizador muta os dois no mesmo passe:

1. a função passa a devolver string vazia;
2. o valor esperado do teste passa a ser string vazia;
3. **o teste fica verde com a função quebrada.**

É a reencenação automática do incidente de 21/04/2026, com uma diferença: em
abril foi um diff humano, revisável. Agora é uma ferramenta que reescreve o
arquivo, faz `git add` do resultado e **sempre sai com código 0**.

## Por que ele conseguiu fazer isso sem ninguém ver

Três propriedades do higienizador, todas medidas em
`universal-sanitizer.py`:

| Propriedade | Linha | Consequência |
|---|---|---|
| Reescreve o arquivo no disco | :184-186 | a alteração é fato consumado antes de qualquer revisão |
| Sempre retorna 0 | :224 | não é portão: nunca reprova nada |
| Só imprime um resumo agregado | :222 | diz *"3 emojis removidos"*, nunca **qual** nem **onde** |

E o hook global `~/.config/git/hooks/pre-commit:206` o chama com `2>/dev/null` e
re-adiciona todos os arquivos ao índice logo em seguida (`:208-210`).

> Um **gate** reprova e diz o que está errado, e a pessoa corrige. Um
> **higienizador** altera e segue, e ninguém fica sabendo. Para conteúdo escrito,
> a diferença entre os dois é a diferença entre revisar e ser reescrito.

## As duas entregas

### Entrega 1 — cirurgia no higienizador do ambiente

Arquivo: `~/.config/zsh/scripts/universal-sanitizer.py`. **Fora do repositório.**

1. **Recortar as duas faixas invasoras.** U+2194 a U+21AA sai inteira. U+25AA a
   U+25FE sai inteira. O que se perde de cobertura real é próximo de nada: os
   emojis de verdade dessas vizinhanças moram em U+1F300 e acima, que outras
   faixas já cobrem.
2. **Acrescentar o que falta.** U+2B50 e os demais Emoji_Presentation isolados
   fora de U+1F000, que hoje passam.
3. **Deixar de reescrever; passar a reprovar.** Sair com código diferente de zero
   e imprimir **arquivo, linha e codepoint** de cada achado. O modo que reescreve
   pode continuar existindo atrás de uma flag explícita, nunca como padrão.
4. **Trocar `content.splitlines()` (:166) por `content.split("\n")`.**
   `splitlines()` também quebra em U+000B, U+000C e U+2028 — ou seja, reescreve
   bytes em silêncio num repositório que manipula relatório HID.
5. **Fazer o hook global olhar o código de saída — sem isto o item 3 é inócuo.**
   `~/.config/git/hooks/pre-commit:206` chama o higienizador assim:

   ```
   python3 "$SANITIZER" $FILES 2>/dev/null
   ```

   Sem `||`, sem testar `$?`, e re-adicionando tudo ao índice em `:208-210`.
   **O código de saída é descartado hoje.** Fazer o higienizador reprovar sem
   mexer nesta linha não muda absolutamente nada — some o `2>/dev/null` e trate
   a saída diferente de zero como bloqueio.

**Risco declarado:** este arquivo é descrito nas instruções globais como fonte
canônica mantida pelo self-heal do Ritual da Aurora. **Não foi medido se o
self-heal o sobrescreve depois de editado.** Medir isso é o item 0 da entrega —
se sobrescrever, a Entrega 1 se desfaz sozinha e só a Entrega 2 protege.

### Entrega 2 — o portão que o projeto anuncia e nunca teve

`.github/CONTRIBUTING.md:44` promete que o pre-commit bloqueia *"emojis gráficos
em commits, docs e código"*. `docs/adr/011-glyphs-vs-emojis.md:18` diz que *"o
hook `guardian.py` cobre os proibidos"*. Medido: `find . -name guardian.py` <!-- ref-externa: a ausência deste arquivo é o achado desta sprint -->
devolve **zero**. O `.pre-commit-config.yaml` tem exatamente três hooks
(`acentuacao-strict`, `anonimato`, `ruff-check`), nenhum de emoji.

Construir `scripts/validar-glifos.py`, com o critério do ADR-011 e não com uma
lista de faixas escrita à mão:

- **reprova** Emoji_Presentation;
- **preserva** os quatro blocos do ADR-011:14;
- imprime arquivo, linha, coluna e codepoint;
- entra no `.pre-commit-config.yaml` **e** num job do `ci.yml`, porque o
  `core.hooksPath` global pode sequestrar o hook local a qualquer momento.

## Como você valida

Nada aqui se valida olhando a janela. Valida-se rodando e vendo reprovar o que
deve reprovar.

### Prova de que o gate morde

Os dois casos de teste **já existem no repositório**, sem precisar fabricar nada:

| Caso | Arquivo | O gate tem de |
|---|---|---|
| U+2B50 vivo, proibido | `docs/usage/troubleshooting-8bitdo.md:29` e `:48` | **REPROVAR hoje mesmo**, sem alterar uma linha |
| Glifos U+25AE e U+25AF, permitidos | `src/hefesto_dualsense4unix/tui/widgets/__init__.py` | **PASSAR** |

**A mordida:** arrancar do script a cláusula que preserva os quatro blocos do
ADR-011. O segundo caso tem de passar a reprovar. Se continuar verde, o gate não
está lendo o que acha que lê.

### Prova de que o higienizador foi curado

Um arquivo com quatro U+25AE seguidos de um U+2B50:

| | hoje | depois |
|---|---|---|
| os quatro U+25AE | viram string vazia | voltam intactos |
| o U+2B50 | fica | faz sair com código diferente de zero |
| a saída | `[sanitizer] 1 arquivos: 5 emojis removidos` | arquivo, linha e codepoint de cada um |

### Terceira prova, e é a que fecha o buraco

Trocar os literais de `tests/unit/test_tui_widgets.py` por construção via
`chr(0x25AE)` — o valor esperado deixa de ser um desenho que uma ferramenta possa
mutar. **Então arrancar a cura da função** (fazer `_icon_for_level` devolver
string vazia): o teste **tem de reprovar**. Hoje, com código e teste mutados
juntos, ele passa — e é essa passagem que prova que o teste atual não testa nada.

## O que NÃO foi medido

- **Se o self-heal da Aurora sobrescreve o `universal-sanitizer.py`.** É o maior
  risco desta sprint e é o item 0.
- **Quantos emojis proibidos existem no repositório.** Achei o U+2B50 porque um
  estudo passou por aquele arquivo. Sem gate não há número, e produzir esse número
  é a primeira coisa que o gate faz quando existir.
- **Se o gate de emoji já existiu e foi removido.** Medi a ausência hoje; não fui
  ao histórico. A resposta muda o texto do ADR-011, não a entrega.
- **O efeito da redação de identidade** (`universal-sanitizer.py:177-182`), que
  troca `user.name` e `user.email` por `[REDACTED]` em qualquer arquivo que não
  seja de configuração. Não medi ocorrência nenhuma; fica registrado porque é a
  mesma classe — reescrita silenciosa de conteúdo escrito.

---

## NOTA DATADA (09/08/2026) — o portão que esta sprint diz faltar nasceu com ela

Conferido no código de hoje, item a item. **O texto acima não foi reescrito** —
ele é o roteiro como estava, e é justamente por isso que esta nota existe.

**O achado que dói:** `git log` sobre os dois caminhos devolve **um único
commit**, `e96dea8` (27/07/2026), e o `--name-status` marca `A` (adicionado)
para os dois. O documento que acusa *"o portão que o projeto anuncia e nunca
teve"* e o `scripts/validar-glifos.py` que o entrega **entraram na árvore no
mesmo commit**. A acusação era verdadeira no instante anterior ao commit e falsa
no instante em que ele pousou — e ninguém voltou para dizer isso.

### Entrega 2 — o portão do repositório: PAGA, integral

| # | o que a sprint pediu | onde está hoje |
|---|---|---|
| 2.1 | reprovar `Emoji_Presentation` | `scripts/validar-glifos.py:184` `tem_apresentacao_emoji`; tabela de 81 faixas em `:77-159` |
| 2.2 | preservar os quatro blocos do ADR-011 | `scripts/validar-glifos.py:167-172` `BLOCOS_PRESERVADOS_ADR_011`, consultado antes da proibição em `:209-210` |
| 2.3 | imprimir arquivo, linha, coluna e codepoint | `scripts/validar-glifos.py:416`; teste `tests/unit/test_validar_glifos.py:159` |
| 2.4 | entrar no pre-commit | `.pre-commit-config.yaml:40-45`, `id: glifos` |
| 2.5 | entrar num job do CI | `.github/workflows/ci.yml:65-80`, job `glifos`, com `--all` |
| 2.6 | não reescrever arquivo, sair diferente de zero | `scripts/validar-glifos.py:419-429`; nenhuma escrita no módulo |
| 2.7 | `split` em vez de `splitlines` | `scripts/validar-glifos.py:306`, com o porquê em `:302-305` |

**A mordida existe e foi verificada:** `tests/unit/test_validar_glifos.py:255` e
`:282` mutilam o próprio script (arrancam a cláusula de preservação marcada em
`scripts/validar-glifos.py:204-210`) e exigem que o caso protegido passe a
reprovar. É teste que morde, no sentido da casa.

**Uma ressalva honesta, e ela é nova:** o `exclude` do pre-commit
(`.pre-commit-config.yaml:45`) isenta `tests/fixtures/`, `docs/history/`,
`docs/research/` e o `CHANGELOG.md` — enquanto o comentário do próprio script
(`scripts/validar-glifos.py:227-228`) afirma que o proibido vale *"em qualquer
arquivo de texto, inclusive fixture, CHANGELOG e registro histórico"*. O CI roda
sem `exclude`, então a divergência não deixa buraco de verdade; mas o script e o
gancho **discordam por escrito**, e isso é dívida de uma linha.

### Entrega 1 — o higienizador do ambiente: ABERTA, e não dá para fechar daqui

O alvo é `~/.config/zsh/scripts/universal-sanitizer.py` e o gancho global do
git. **Nenhuma leitura deste repositório confirma ou refuta.** O item 0 — se o
self-heal da Aurora sobrescreve a cura — está na mesma condição.

Por isso esta sprint **não vira ENTREGUE inteira hoje**: metade dela mora numa
máquina que o `git log` não enxerga.

### O grau, como manda a casa

**MEDIDO** para a Entrega 2 — há `grep`, teste e job de CI que fecham a conta.
**SEM PROVA** para a Entrega 1: está dito e ninguém verificou.
