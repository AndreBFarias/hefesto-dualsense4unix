# DOC-QUE-NÃO-MENTE-03 — a foto vazia, a env negada e a tag velha

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** MÉDIA para os defeitos; **ALTA para a E5** (os índices
  defasados), porque é ela que impede a próxima leva de refazer trabalho pronto
- **Faixa:** 3 — a documentação afirma o que a árvore não faz
- **Causa-raiz:** **PROVADA e MEDIDA** nos cinco casos
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Sucede:** `DOC-VERDADE-01` e `DOC-VERDADE-02`, e usa o mesmo método delas —
  o fato sai do **código**, nunca de outro documento

---

## Defeito 1 — a foto da aba Início publicada na documentação está VAZIA

**O mais grave da sprint**, porque a foto é a promessa central do
`retratar_abas.py`: *"rodar e a documentação deixa de mentir"*.

`scripts/gui-captura/retratar_abas.py` injeta **duas** coisas: o card do
controle na aba Status (`_injetar_card`, linha 213) e os 19 modos de gatilho
(`_injetar_modos_de_gatilho`, linha 177).

**A aba Início é 100% montada em código.** `app/actions/home_actions.py:19-21`:

> *"Todo widget é montado em código dentro de `tab_home_box` (Glade só reserva o
> container) — padrão dos widgets dinâmicos, imune ao bug de popup do
> cosmic-comp."*

Resultado, conferido nos PNGs versionados em 03/08: `readme_inicio.png` mostra
**apenas** o rótulo "Jogar acompanhada" e um botão "Preparar co-op". O resto da
imagem é vazio.

**E dois documentos a publicam descrevendo o que ela não mostra:**

- `README.md:206` — legenda **"Início — o que o controle faz agora"**;
- `docs/usage/interface.md:16-22` — a foto, e logo abaixo: *"Tem o seletor **O
  que o controle faz agora** com os três modos (Controlar o PC · Jogar pelo
  Hefesto · Jogar direto (Sony)), o seletor de máscara **O jogo vê o controle
  como:**, o cadeado **Não trocar de perfil sozinho ao abrir um jogo**, e um
  card por controle conectado"*.

**Nada disso está na imagem.** É o mesmo defeito que o
[COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md) atribui ao `retrato_offscreen.py`
(*"a aba Status sem o card do controle"*) — agora na aba que o README chama de
*"a de decisão"*.

### E o script degrada em silêncio, com código de saída zero

**Medido em 03/08**, rodando com o interpretador errado:

```
tema indisponível (No module named 'platformdirs')
card não injetado (No module named 'structlog') — a aba Status sai vazia
...
9 aba(s) em <destino>              <- e sai ZERO
```

Ele imprime o aviso, **gera os nove PNGs assim mesmo** e sai com sucesso. **Sem
argumento, ele sobrescreve `docs/usage/assets/`** — ou seja, uma execução com o
interpretador errado troca as imagens da documentação por versões incompletas, e
nada reprova.

**Qual é o interpretador certo:** só `.venv/bin/python` (é o que tem
`--system-site-packages` e enxerga o `gi`). Esta árvore tem **dois** ambientes, e
o que está no `PATH` (`venv/`, sem system-site-packages) **nem importa `gi`**. O
`CLAUDE.md` e o `COMO-OLHAR-A-TELA.md` mandam rodar o script **sem interpretador
explícito** — que resolve pelo shebang e cai no errado.

---

## Defeito 2 — três documentos negam uma funcionalidade que existe e é testada

**MEDIDO em 03/08**, contra a árvore:

```
HEFESTO_DUALSENSE4UNIX_METRICS_ENABLED=1  ->  is_enabled(DaemonConfig()) == True
(sem a env)                               ->  is_enabled(DaemonConfig()) == False
```

A env existe (`daemon/subsystems/metrics.py:47`), é honrada
(`:388`), o `_start_metrics` do daemon respeita o mesmo portão
(`daemon/lifecycle.py:2746`), e a suíte a trava
(`tests/unit/test_metrics.py:258,273`).

**E três documentos dizem o contrário:**

| documento | o que afirma |
|---|---|
| `README.md:285-293` | *"não existe hoje variável de ambiente, flag de linha de comando nem arquivo de configuração que ligue esse campo… subir as métricas exige mexer no código"* |
| `docs/usage/metrics.md` | bloco inteiro: *"Não há caminho de usuário para ligar isto"*, e *"O que falta… Nenhum dos dois foi feito."* |
| `docs/adr/016-prometheus-metrics.md:157-163` | a **Nota de verificação de 2026-08-01** — *"Corrige um número da nota anterior, e só ele. O veredito de 25/07 continua de pé: não há chave de usuário para as métricas"* |

**A nota da ADR é datada do mesmo dia em que a env nasceu.** Ela corrigiu a
contagem de parâmetros e **reafirmou o veredito que acabara de caducar**.

### Por que os dois portões deixaram passar — e é a parte que interessa

1. **O teste `test_doc_verdade_02_contagens_derivadas.py` trava a PREMISSA, não a
   CONCLUSÃO.** Ele deriva do AST quantos parâmetros o `DaemonConfig` recebe em
   `daemon/main.py` e cobra que as três páginas digam o mesmo número. Funciona
   perfeitamente. Mas a frase que ficou falsa é a **conclusão** que as páginas
   tiram dessa contagem — *"logo, nada liga as métricas"* — e a env foi criada
   **fora** do `daemon/main.py`, portanto fora do alcance do teste;
2. **O escape do portão de referências silencia exatamente a linha que virou
   mentira.** `docs/usage/metrics.md` traz
   `<!-- ref-externa: a variável é citada aqui JUSTAMENTE por não existir -->`
   nas duas linhas que citam a env. O escape entrou **porque** ela não existia —
   e **ficou** depois que passou a existir.

A própria ADR-016 escreve a moral certa e aplica a cura pela metade:
*"A cura não é voltar a ser vago — é o teste que conta os parâmetros no código e
cobra o mesmo número aqui."* O teste conta. **Ninguém confere o veredito.**

---

## Defeito 3 — o README manda instalar a versão anterior

`README.md:75` e `:91`, com a **v0.8.0 publicada**:

```
> O ponto recomendado é a tag da versão corrente, hoje a **`v0.7.0`**.
...
git checkout v0.7.0
```

As três páginas de uso já dizem `v0.8.0` (`instalacao.md:40`,
`quickstart.md:38`, `flatpak.md:42`).

**É a regressão exata da `PUBLICAÇÃO-FIEL-01`, com o alvo invertido:** naquela,
o `instalacao.md` estava atrasado e as outras duas certas; nesta, o README está
atrasado e as três certas.

**A causa-raiz é uma lista:**
`tests/unit/test_versao_publicada_data_e_paginas_de_uso.py:48`

```python
PAGINAS_DE_USO = (INSTALACAO_REL, "docs/usage/quickstart.md", "docs/usage/flatpak.md")
```

**O README está fora** — embora esteja **dentro** da lista vizinha
`ARQUIVOS_COM_URL_DO_FORK` (linha 53), no mesmo arquivo, três linhas abaixo. O
`scripts/check_version_consistency.py` cobre o README só na prosa
(`Versão: X.Y.Z`) e no emblema; o alvo do `git checkout` aponta para
`docs/usage/instalacao.md`.

E é **o arquivo que mais gente copia e cola** — frase do próprio `ci.yml`, sobre
outra regra.

---

## Defeito 4 — a dívida documental é maior do que o índice registra

O índice de 01/08 nomeia quatro IDs sem documento (`SOM-CANAL-01`,
`EMPILHA-01`, `EMPILHA-02`, `STATUS-GRID-2COL-01`). **A varredura de 03/08
confirmou os quatro e achou muito mais.**

Os órfãos totais — citados em `src/`/`tests/`, **zero** menção em `docs/`,
nenhum arquivo de sprint:

| ID | citações | nasceu |
|---|---|---|
| **`GUARDA-GI-REAL-01`** | **54** | 28/07 |
| `SOM-CANAL-01` | 19 | 02/08 |
| `HONESTIDADE-STEAM-01` | 15 | 25/07 |
| `CLONE-01` | 14 | 25/07 |
| `LOCK-CEDE-01` | 11 | 25/07 |
| `SALVAR-NAO-REBAIXA-01` | 11 | 28/07 |
| `MIC-REGISTRY-01` | 9 | 25/07 |
| `RUMBLE-PRESO-01` | 9 | herdado |
| `AUDIO-STATUS-01` | 6 | 25/07 |
| `EMPILHA-01` / `STATUS-GRID-2COL-01` / `FONTE-PADRAO-01` | 6 cada | 02/08 · 25/07 · 30/07 |
| `EMPILHA-02` / `GYRO-BT-SILENCIO-01` | 5 cada | 02/08 · 25/07 |
| `ALLOWLIST-SUPRESSAO-01` | 4 | 25/07 |
| `HOTKEY-EXPOSE-01`, `TYPELIB-PARCIAL-01` | 3 cada | 25/07 |
| `BROADCAST-QUE-NAO-MENTE-01` | 2 | 02/08 (não commitado) |

**`GUARDA-GI-REAL-01` é o maior de todos: 54 citações, e é a maior mudança de
confiabilidade da suíte** (o `exigir_gi_real` que matou os 737 falsos-verdes).
Vive só em mensagem de commit. O índice de 29/07 já a batizara
`TESTE-QUE-MEDE-01`; nunca virou arquivo.

**Nota de método:** o `validar-referencias-docs.py` acha **link morto**, não **ID
órfão**. É cego a esta classe inteira.

---

## Defeito 5 — os índices estão defasados PARA MENOS, e isso custa mais caro

**O achado que muda o planejamento.** A varredura de 03/08 cruzou cada sprint com
o código de hoje:

| Onde | O índice diz | A árvore diz |
|---|---|---|
| `2026-07-31-INDICE:70-88` | ONDA 1 = 17 itens por fazer | **16 pagos**, só o 1.10 aberto |
| `2026-07-31-INDICE:108` | CONTAGEM-E-COOP-01 falta | entregue (`status_actions.py:184,1569,1923`) |
| `2026-07-31-INDICE:122` | `main` divergente, 17 commits | **divergência zerada** (`main` é ancestral de HEAD) |
| `2026-07-30-INDICE:187` | LARGURA-01 "E2 a E9" | só E7 e E8 |
| `2026-07-30-INDICE:188` | SOM-02 "E1 a E5 inteiras" | entregue |

E várias sprints dizem `Status: ABERTA` na linha 3 com o código **de pé**:
`PERFIL-SALVA-TUDO-01`, `EMULACAO-NO-JOGO-01`, `SENSOR-VIVO-01` (E4/E5),
`AUTO-01`, `LEGIBILIDADE-01`, `MIC-USB-01`, `NUM-01`, `PLAYER-01`,
`UI-SELETOR-01`, `MODO-01` (B1/B2/B3/B5), `PERFIL-NASCE-CERTO-01` (E1/E2).

**Planejar pelo índice significaria refazer trabalho pronto** — que é o oposto
do que ela pediu ao mandar materializar as sprints.

---

## As entregas

### E1 — o retratador passa a montar a aba Início (ou a recusar a foto)

Duas saídas, e a sprint recomenda a primeira:

- **(a) injetar a aba Início**, como já se injeta o card e os gatilhos. O
  `home_actions.py` monta tudo dentro de `tab_home_box`; o script precisa
  chamar esse montador com dublês, do mesmo jeito que faz com o
  `ControllerCard`. **Recomendado** — é o que cumpre a promessa do script;
- **(b) o script recusa gerar** a foto de uma aba cujo conteúdo ele não sabe
  montar, e **falha**. Mais barato, e deixa o README sem a imagem da aba
  principal.

**Aceite:** `readme_inicio.png` mostra os três modos, o seletor de máscara e o
cadeado — o que o `interface.md` descreve.

### E2 — o retratador deixa de sair zero quando degradou

Hoje ele imprime `card não injetado (…) — a aba Status sai vazia` e **sai com
sucesso**, sobrescrevendo a documentação.

**A regra:** degradação em injeção é **erro**, não aviso. Sem argumento (o modo
que sobrescreve `docs/usage/assets/`), qualquer injeção que falhe deve abortar
**antes de escrever qualquer PNG**.

**E o interpretador deixa de ser adivinhação:** o script confere na entrada que
`gi`, `platformdirs` e `structlog` estão todos disponíveis, e se não estiverem
diz **qual comando rodar** (`.venv/bin/python scripts/gui-captura/retratar_abas.py`).

**Aceite:** rodar com `/usr/bin/python3` **falha** com a mensagem certa e **não
toca** em `docs/usage/assets/`.

### E3 — as três páginas passam a dizer a verdade sobre as métricas

Corrigir `README.md:285-293`, `docs/usage/metrics.md` (o bloco inteiro) e a nota
de 01/08 da `ADR-016`.

**A ADR não se reescreve — ganha nota nova datada**, é a regra da casa. A nota de
03/08 registra que o veredito de 25/07 e 01/08 **caducou**, com o nome da env e a
data em que ela nasceu.

**E os dois escapes `<!-- ref-externa -->` do `metrics.md` saem**, porque a
variável agora existe e o portão deve passar a vigiá-la.

**Aceite:** `docs/usage/metrics.md` ensina
`HEFESTO_DUALSENSE4UNIX_METRICS_ENABLED=1`, e o portão de referências **confere**
que essa env existe em `src/`.

### E4 — o portão cobre a CONCLUSÃO, não só a contagem

O teste que já existe é bom e fica. **Ao lado dele, um teste que derive o fato
inverso:** se `MetricsSubsystem.is_enabled` honra alguma variável de ambiente,
então nenhuma das três páginas pode conter a frase "não existe variável de
ambiente".

**A mordida:** apagar a env do `metrics.py` e o teste continua verde (porque a
frase volta a ser verdade); acrescentar uma env nova sem tocar nos documentos e
**ele reprova**.

**E o README entra em `PAGINAS_DE_USO`** — a correção do defeito 3 é uma linha
em `tests/unit/test_versao_publicada_data_e_paginas_de_uso.py:48`, e ela vale
mais que o conserto do texto, porque impede a terceira vez.

### E5 — a recontagem dos índices, e a regra que a torna desnecessária

**A parte cara e a que mais economiza.** Atualizar os placares dos índices de
30/07, 31/07 e 01/08 com o estado real, e o `Status:` das sprints que estão
entregues e não dizem.

**E a regra que evita a próxima defasagem:** o `Status:` de uma sprint é **a**
fonte de verdade; o placar do índice é **derivado**. Um teste que leia o
`Status:` de cada sprint e cobre que o índice que a linka diga o mesmo torna a
divergência impossível de sobreviver a um commit.

**Aceite:** nenhum índice lista como aberto um item cujo `Status:` diz entregue.

### E6 — os IDs órfãos ganham documento ou lápide

**Não é escrever 20 sprints retroativas.** É:

1. **`GUARDA-GI-REAL-01` ganha documento próprio** — 54 citações e a maior
   mudança de confiabilidade da suíte merecem mais que uma mensagem de commit.
   O índice de 29/07 já lhe deu nome (`TESTE-QUE-MEDE-01`);
2. **os demais entram num documento único de registro** —
   `docs/process/estudos/`, uma seção por ID, com o que ele significa e onde
   está no código. Uma linha por ID já resolve o problema real: quem lê
   `# SOM-CANAL-01` no código descobre o que é;
3. **o portão passa a achar ID órfão**, não só link morto — uma regra no
   `validar-referencias-docs.py` que reprove ID **novo** (nascido depois da data
   de corte) sem documento.

**Aceite:** `grep -rl 'GUARDA-GI-REAL-01' docs/` devolve um arquivo.

---

## Testes que vão reprovar

```
pytest tests/unit -k "retrato or versao or doc_verdade or metrics or referencias"
```

E `python3 scripts/validar-referencias-docs.py --all` depois da E3 — a retirada
dos escapes muda o que ele varre.

## O que NÃO fazer

- **Não apagar as notas antigas da ADR-016.** Decisão medida não se apaga —
  ganha nota datada. Vale para a de 25/07 e a de 01/08;
- **Não "consertar" o README trocando só o número.** Sem a linha em
  `PAGINAS_DE_USO`, a terceira vez é questão de tempo;
- **Não gerar as fotos com `/usr/bin/python3`** — é exatamente o defeito da E2;
- **Não reescrever as sprints antigas na E5.** Só o campo `Status:`, com a data.
  O corpo delas é registro histórico;
- **Não fazer o portão de ID órfão varrer os ~300 IDs legados** (`FEAT-*`,
  `BUG-*`, `AUDIT-FINDING-*`) — são tags de commit de outra era, e um portão que
  reprova 300 coisas é desligado no mesmo dia.

## O que fica ABERTO

- **a decisão (a)/(b) da E1**, que é dela;
- **os 438 `replace refs` do `filter-repo`** (`git replace -l` devolve 438):
  toda arqueologia por hash antigo devolve conteúdo diferente em silêncio. Foi
  registrado no índice de 31/07 e sumiu depois. Não é desta sprint, mas some de
  novo se ninguém o escrever.
