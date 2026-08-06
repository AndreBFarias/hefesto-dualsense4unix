# A leva dos perfis que se reescreviam sozinhos — índice de 05/08/2026

- **Escrito em:** 05/08/2026, na branch `restauro/inicio-da-sessao`, sobre uma
  árvore de trabalho **inteiramente não commitada** (ver o alerta abaixo, que
  vem antes de qualquer outra coisa)
- **Por que esta leva existe:** ela perguntou duas coisas, nesta ordem, e as
  duas viraram sprint:

  > *"a config que eu deixo nunca é respeitada"*

  > *"como sabemos se algum teste ou algo a mais corrompeu algo?"*

- **O que este índice é:** o ponto de entrada da **faixa de perfis** — que até
  hoje não tinha um. Quem retomar lê **este arquivo** e depois a sprint que for
  executar. Nenhuma sprint desta leva precisa de auditoria nova para ser lida:
  cada uma traz a causa-raiz com `arquivo:linha`, o grau de cada afirmação, o
  teste que morde e o que **não** fazer

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, teste que reprova ou `git grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou. Este índice declara o seu em cada
seção, e **não herda** o grau das sprints que cita.

---

## ANTES DE TUDO: a leva inteira está SEM COMMIT

> **NOTA DATADA — 05/08/2026, 22h. CADUCOU: a leva FOI COMMITADA.** Quatro
> commits no `restauro/inicio-da-sessao`, nesta ordem: `c3829c7` (o código e os
> testes), `2342743` (as sete sprints e este índice), `10f4818` (a unificação do
> predicado `steam_app_`) e `bb98278` (a ferramenta de fotografar diálogo e as
> cinco fotos). Árvore limpa, **7017 verdes / 1 skipped**, e os oito validadores
> da casa em zero.
>
> O texto abaixo **não se apaga** porque a lição dele não caducou: a leva passou
> horas a um `git reset --hard` de sumir, e só foi descoberta porque ela
> perguntou *"tudo foi salvo?"*. Um `git status` com tudo em `A `/`M ` **parece**
> trabalho salvo, e não é — é o índice, não a história.
>
> **O bloqueante nº 2 também caducou, e melhor do que o previsto:** o daemon foi
> reiniciado em 05/08 às 22:39:45 (PID 298882), sem jogo em curso e com um
> DualSense na mesa. O journal do primeiro segundo já traz
> `profile_suppression_skipped motivo=catch_all_sem_opiniao` — o item 2 da
> `PERFIL-REESCRITO-NA-PARTIDA-01` trabalhando na máquina dela, MEDIDO, não
> inferido. **O que sobrou não é código, é DADO:** ver a seção nova
> "O estrago que ficou no disco dela", ao fim deste índice.

> **Grau: MEDIDO**, por `git diff --cached --shortstat` em 05/08, ao escrever
> este arquivo.

| medida | valor |
|---|---|
| branch | `restauro/inicio-da-sessao` |
| último commit | **`5f1b588`**, de **04/08 às 03:19** |
| estado da leva | **tudo no índice do git (`git add`), NADA commitado** |
| tamanho quando a síntese foi escrita | 50 arquivos, +7137 / -233 (seção 5.0 do estudo) |
| tamanho ao começar este índice | 56 arquivos, +9442 / -233 |
| tamanho ao fechá-lo | **61 arquivos, +11391 / -235** |

**Os dois números estão certos e a diferença é o próprio trabalho da
madrugada** — o total cresce a cada documento novo, inclusive por causa deste
índice. O que não muda é o risco:

> **Um `git stash` ou um `git checkout` perde a leva inteira.** Seis sprints,
> um estudo de 89 KB, o funil de gravação, o histórico de perfis, o canário do
> `$HOME` e a cura dos seis itens do daemon.

**Commitar é o item 1 dos bloqueantes de processo, e vem antes de qualquer
entrega nova.** É também o motivo de **nenhuma sprint desta leva usar `git
stash` para verificar mordida**: as duas que verificaram (`ATIVAR-NÃO-MENTE-01`
e `PERFIL-REESCRITO-NA-PARTIDA-01`) arrancaram as curas à mão e devolveram com
`git checkout --` a partir do índice, e uma delas conferiu a árvore **byte a
byte** contra cópia de segurança ao fim.

**Bloqueante nº 2, e ele é decisão DELA:** o daemon vivo na máquina dela é o
**PID 1670, no ar desde 04/08 23:39:46**, e o install é *editable*. **Nenhuma
cura de daemon desta leva está valendo lá.** Havia sessão de jogo viva quando
isto foi medido; reiniciar é escolha dela, não nossa.

---

## POR QUE ESTE ÍNDICE EXISTE — a faixa estava órfã

**Grau: MEDIDO**, e é a única constatação desta casa que explica um padrão em
vez de um defeito.

O `CLAUDE.md` manda ler *"o índice de sprints aberto mais recente"*. Até hoje,
esse índice era o
[do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
— que é excelente e **não menciona perfis**. Quem seguisse a instrução da casa
à risca **não achava esta faixa**.

A medição do estudo, contando menções a
`PERFIL-SALVA-TUDO | AUTOMATISMO-MORTO | PERFIL-NASCE-CERTO | EMPATE-01 |
ABAS-01 | PERFIL-JOGO-01` nos índices:

| índice | menções |
|---|---|
| 30/07 | **15** |
| 31/07 | **4** |
| 01/08, 03/08 e as ONDAS | **0** |

**É a explicação estrutural de por que meias-entregas passaram batido nesta
área — ninguém estava olhando.** E o exemplo perfeito está na
`SALVAR-NÃO-REBAIXA-02`: a guarda de 27/07 foi escrita, testada e **desligada
por um botão vizinho**, sem nada reclamar por **oito dias**.

Este arquivo é o item 5 dos bloqueantes de processo da seção 5.7 do estudo,
pago.

### As sprints da faixa que este índice readota

Nenhuma delas foi reaberta aqui — entram porque **precisam de casa**, e porque
a leva nova as toca:

| sprint | por que está aqui |
|---|---|
| [PERFIL-NASCE-CERTO-01](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md) | a **E4 foi paga em 05/08** — ver a nota datada no topo daquele arquivo |
| [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | o sintoma no daemon, do qual a `NASCE-CERTO` é a causa |
| [ABAS-01](2026-07-25-ABAS-01-as-abas-brigam-pelo-mesmo-estado.md) | escreveu `with_profile_identity` e ligou **em um lugar só** — é o defeito que o funil fecha |
| [PERFIL-SALVA-TUDO-01](2026-07-29-PERFIL-SALVA-TUDO-01-salvei-todas-as-abas-e-so-parte-ficou.md) | os **vetos** que a leva nova teve de respeitar (R-11, o nº 2 e o nº 3) |
| [EMPATE-01](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md) | o desempate por ordem alfabética que a saturação do teto (D-26) ressuscita |
| [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md) | o pano de fundo: os perfis dela viraram catch-all |
| [SALVAR-NÃO-REBAIXA-01](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md) | **nunca virou documento** — 11 citações em `src/` e `tests/`, zero em `docs/`. O resumo em cinco linhas está no topo da 02 |

---

## LEIA ISTO PRIMEIRO

**A base factual da leva inteira é
[o sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md).**
São 37 defeitos numerados (D-01 a D-37), 11 divergências entre agentes (DIV-1 a
DIV-11) e 15 vetos consolidados. **Nenhuma sprint daqui se executa sem ele
aberto ao lado**, e as referências `D-nn` / `DIV-n` deste índice são todas dele.

Para o protocolo, a base continua sendo
[a referência canônica do DualSense](../../protocol/dualsense-referencia-canonica.md);
para interface, a regra de aceite continua sendo a
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).

### Os números que enquadram a leva

| medida | valor | grau |
|---|---|---|
| suíte | **6968 passed, 1 skipped**, medido em 05/08 com o canário do `$HOME` armado | MEDIDO (`CANÁRIO-FS-01`) |
| deltas no `~/.config` dela durante a suíte | **zero**, pela primeira vez medidos em vez de supostos | MEDIDO |
| perfis dela em disco | **15 arquivos**; **cinco colidem por acento ou caixa** | MEDIDO |
| o perfil ATIVO dela | `sackboy_nativo`: prioridade **191**, `match: any`, `suppress: true` | MEDIDO |
| origem daquele 191 | **indeterminada** — três teses incompatíveis (DIV-1) | **SEM PROVA**, e agora **decidível** |

**A frase que resume a leva:** o produto tinha três caminhos que escreviam no
disco dela e **nenhum** que registrasse quem escreveu. Três agentes
independentes chegaram a três culpados diferentes para o mesmo número, e nenhum
podia ser confirmado nem descartado.

### As três lições de método desta leva

1. **Lembrar de chamar não é engenharia.** A cura do defeito do rodapé existia
   desde 25/07, com nome, endereço e docstring descrevendo **este** defeito — e
   um único chamador. A resposta não foi "adicionar a linha nos três lugares";
   foi **tirar a possibilidade** de gravar por fora (o funil e os três portões);
2. **Sem rastro, a perícia é opinião.** A `PERFIL-SEM-RASTRO-01` não cura
   comportamento nenhum: ela cria o instrumento que decide todos os outros. Antes
   dela, gravar perfil era **o único caminho do projeto que mudava o disco da
   usuária sem deixar uma linha dizendo o quê**;
3. **Um portão que grita no primeiro dia é um portão que alguém desliga no
   segundo.** O canário do `$HOME` nasceu comparando `(mtime, tamanho)`, acusou
   **15 falsos positivos na estreia** (todos `.lock`, tocados pelo daemon e pela
   janela **dela**, vivos ao lado da suíte) e foi redesenhado para `sha256`. A
   refutação está registrada como DIV-11 e **fica**.

---

## O PLACAR

**Sete sprints, seis delas escritas nesta madrugada.** Todas com **cura
aplicada** — esta leva é, ao contrário da do Bluetooth, uma leva de **código já
na árvore**. O que está aberto é o que cada uma **declara não ter pago**.

| # | sprint | estado | causa-raiz | o que ela entrega |
|---|---|---|---|---|
| 1 | [GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md) | **CURA APLICADA** | **MEDIDA** em duas bancadas (a catraca `10 → 20 → 30`) | o funil de gravação, três portões estáticos e a **REGRA-NÃO-SE-PERDE-01** |
| 2 | [SALVAR-NÃO-REBAIXA-02](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md) | **CURA APLICADA** | **PROVADA e REPRODUZIDA** (o cenário F reproduz o disco dela campo a campo) | a fotografia relida no salvar, o `_esquecer` no fim, e o aviso de queda de prioridade que **não existia** |
| 3 | [ATIVAR-NÃO-MENTE-01](2026-08-05-ATIVAR-NAO-MENTE-01-o-botao-que-parecia-falhar-e-ativava-duas-vezes.md) | **CURA APLICADA** | **PROVADA e MEDIDA no journal** (~1,2 s de resposta contra 0,25 s de paciência) | a folga própria do `profile.switch` **dos dois lados da fronteira Python/Rust**, a leitura do relatório e o refresh das abas |
| 4 | [PERFIL-REESCRITO-NA-PARTIDA-01](2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md) | **CURA APLICADA nos seis itens** | **PROVADA nos seis**; **MEDIDA no journal** em quatro | a crença do autoswitch, a simetria da supressão, as guardas do rumble, o relatório e o log honestos, e a saída do Modo Nativo |
| 5 | [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md) | **CURA APLICADA** | **PROVADA** (`os.replace` sem cópia; zero linhas de journal) | o `.historico/`, o `profile_salvo` com `origem=`, e a CLI que devolve o backup **a ela** |
| 6 | [CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md) | **CURA APLICADA** | **PROVADA** (`Path.home()` avaliada no import) | o canário de sessão, e as duas constantes que viraram função **por decisão dela** |
| 7 | [TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md) | **CURA APLICADA** | **PROVADA e MEDIDA ao vivo** | o `clear` da trava manual sobe para **antes** do `activate`, nos dois gestos explícitos dela |

**A 7 é anterior às outras seis e nasceu no índice do Bluetooth** — está aqui
porque é da faixa de perfis, e continua listada lá. Ela é a única desta leva que
já tinha casa.

### O que cada uma NÃO pagou, em uma linha

Isto é o que sobra depois de a cura entrar, e é o material da próxima leva:

- **1** — o `match` de **nome novo** (ver a decisão dela, abaixo); o importar
  comparando nome cru (I-1) e sem recarregar as abas (I-8); o "Salvar" do rodapé
  que não reaplica (I-6);
- **2** — a origem do 191 (DIV-1); a escala que satura no teto (D-26); os **três
  números** que convivem para *"nascer acima dos catch-all"* (DIV-7);
- **3** — o applet continua **ignorando** o `secoes` (`app.rs:223`); o
  `ipc_bridge.apply_draft()` continua estreitando a verdade para `bool`;
- **4** — a trava manual continua **sem afordância na tela**; o `secoes=` novo
  ainda **não tem leitor** de journal; o modo jogo padrão continua ligando e
  soltando por foco dentro da partida (D-24);
- **5** — a dívida `DOC-VERDADE-01` (seção própria, abaixo) e a lacuna de
  traversal nos caminhos de **escrita** (idem);
- **6** — **isolar o `HOME` no autouse**, a única cura que fecha a classe da
  **leitura**; o canário vê escrita, não leitura;
- **7** — o `clear_manual_trigger_active("audio")` continua não existindo
  (`ÁUDIO-QUE-TRANCA-01/E1`).

---

## A DECISÃO DELA DE 05/08 — e o trabalho que ela ABRE

> **Grau da decisão: declarada por ela em 05/08.** Grau do desenho abaixo:
> **MEDIDO** onde há `git grep` citado; **proposta** no resto, e dito assim.

Ela decidiu duas coisas no mesmo dia, e as duas mudam o que a casa considerava
contrato:

1. **o `match` TEM de ser herdado no rodapé;**
2. **as constantes têm de apontar para os arquivos reais** — *"preciso que as
   constantes apontem pros arquivos reais"*, que é a decisão registrada nas duas
   docstrings da `CANÁRIO-FS-01`. **Esta metade está PAGA**: o
   `_ALLOWLIST_PATH` e o `_WP_DROPIN_DIR` viraram função, e o chamador de teste
   acompanhou.

**É a metade 1 que abre trabalho**, e ela caduca uma decisão desta casa.

### O que caducou, e não se apaga

**NOTA DATADA (05/08/2026).** O veto nº 14 da síntese diz, com todas as letras:
*"O `MatchAny()` do PRIMEIRO save com nome novo (R-11) — o defeito é o segundo
save"*. A `DIV-2` registrava a mesma pergunta em aberto: *"o `MatchAny()` do
rodapé é defeito ou decisão?"*, com um relatório de auditoria defendendo
explicitamente que era **decisão deliberada** e que a cura bastava ser um aviso
no diálogo.

**A decisão dela fecha a DIV-2 no outro sentido.** O `MatchAny()` por nome novo
**deixou de ser contrato e virou defeito a corrigir**. As duas linhas acima
ficam onde estão — eram verdade quando foram escritas, e o registro de que
deixaram de ser é esta nota.

**O que a `REGRA-NÃO-SE-PERDE-01` já pagou** (seção nomeada da sprint 1, não
arquivo próprio): quem **já existe em disco** herda o próprio `match`, lido do
**disco** e não da fotografia (`footer_actions.py:420`). O gate `mesmo_perfil`
do `to_profile` **não foi tocado**, e o R-11 continua fechado.

**O que fica ABERTO é a outra metade: o nome NOVO nascia sem regra.**

### REGRA-NÃO-SE-PERDE-02 — a próxima sprint a escrever

**Ainda não existe como arquivo.** Este índice é o único lugar onde ela está
registrada, e o desenho abaixo é o que a decisão dela implica — **é proposta, e
tem de virar sprint com causa-raiz e mordida declarada antes de virar código.**

**Decisão de desenho nº 1 — a herança mora no RODAPÉ, não no `to_profile`.**

**Grau: MEDIDO** (`git grep -n "to_profile(" -- src/`, 05/08): o `to_profile`
tem **exatamente dois chamadores em produção** —
`app/actions/footer_actions.py:418` e `app/actions/profiles_actions.py:2034` —
e **dezessete arquivos de teste** que o exercitam. Mexer no gate de lá atinge
**cinco asserções contra uma**, e uma delas é a guarda que impede o perfil novo
de nascer com o regex de **outro jogo** (o defeito medido de 25/07: *"Salvar
como MadJack"* com o FPS ativo produzia um perfil com o regex do FPS e
prioridade 60).

Portanto a herança entra **onde a prioridade já entrou**: no `_construir` do
rodapé, ao lado de `footer_actions.py:420`. É simétrico, é um arquivo só, e
**não afrouxa `mesmo_perfil`** — o veto nº 2 da `PERFIL-SALVA-TUDO-01` continua
respeitado.

**Decisão de desenho nº 2 — perfil sem origem nenhuma nasce `MatchManual()`.**

Não `MatchAny()`. Um perfil que não existe em disco **e** não veio de perfil
nenhum não tem regra a herdar — e o catch-all é justamente a forma que **não
tem autoridade** numa janela de jogo (veto R-21) e **ganha em todo o desktop**.
`MatchManual()` é o sentinel de *"só entra quando eu mandar"* (R-12, item 3):
nasce sem opinião **e sem estrago**, e a regra específica continua sendo
definida na aba Perfis, como o contrato do diálogo do rodapé sempre disse.

**Decisão de desenho nº 3 — o degrau 2 pergunta `e_catch_all`, não tipo.**

A escada fica assim:

| degrau | pergunta | resultado |
|---|---|---|
| 1 | o perfil **já existe em disco**? | herda o `match` **do disco** — **já pago** pela `REGRA-NÃO-SE-PERDE-01` |
| 2 | há perfil de **origem**, e ele **não** é catch-all (`e_catch_all`)? | herda o `match` da origem |
| 3 | nenhum dos dois | **`MatchManual()`** |

**Perguntar `e_catch_all` e não `isinstance(..., MatchAny)` é o ponto fino.**
Os três `Match` são classes irmãs (`profiles/schema.py:51`, `:97`, `:108`) e
**nenhuma herda da outra**; e um `MatchCriteria` com os três campos vazios é
catch-all na prática — é o caso do preset `coop_local` de fábrica, que passou
meses inalcançável por isso. O `Profile.e_catch_all` (`schema.py:626`) já é a
pergunta certa, e é a mesma que a chave de seleção do daemon usa
(`(not e_catch_all, priority)`). Perguntar pelo tipo repete o furo que a
`SALVAR-NÃO-REBAIXA-02` acabou de fechar no diálogo.

**O que a 02 tem de provar, no mínimo:** herdar não pode reabrir o R-11. O
`test_perfil_novo_pelo_rodape_continua_nascendo_sempre` da sprint 1 é hoje uma
**guarda** contra exatamente isso — ele vai precisar ser reescrito **junto com**
a cura, e a sprint tem de dizer qual asserção substitui qual, uma a uma. Sem
isso, esta entrega troca um defeito medido por outro já medido.

---

## AS LACUNAS DE TESTE QUE AS AUDITORIAS ACHARAM

Três, e as três são de **classe conhecida** nesta casa. **Grau: MEDIDO**, por
`git grep` em 05/08, ao escrever este índice.

### 1. `sanidade.verificar_perfis_do_disco()` — código nascendo morto

`src/hefesto_dualsense4unix/profiles/sanidade.py:353`, exportada em `__all__`
(`:392`), com **zero chamadores** e **zero testes**. A conta fecha em uma linha:

```
git grep -n "verificar_perfis_do_disco" -- src/ tests/ scripts/ packaging/ docs/
  -> só a definição e o próprio __all__
```

O irmão dela, `verificar_perfis(perfis)` (`:345`), **tem** chamador
(`cli/cmd_doctor.py:98`) e tem os 25 casos de `tests/unit/test_profiles_sanidade.py`.
A versão que lê o disco sozinha **não tem nenhum dos dois**.

**Isto é a [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
em estado puro, e nascendo na mesma madrugada que a catalogou de novo.** As
duas saídas honestas são **ligar** (é a função que o daemon usaria para avisar
*"na subida"*, que é literalmente o que a `PERFIL-NASCE-CERTO-01/E4` pede) ou
**apagar**. Deixar exportada e morta é a terceira, e é a que a casa proibiu.

### 2. `_conferir_invariante_de_gravacao` — sem mordida, e feito de `assert` puros

`app/actions/profile_writer.py:195`. **Zero testes citam o nome** (`git grep -l`
em `tests/` devolve vazio), e o corpo são **dois `assert` da linguagem**.

Duas consequências, e a segunda é a séria:

- **não há teste que morda:** a sprint 1 declara que o assert derruba
  *"4 pelo assert de invariante"* quando a cura do rascunho é arrancada — ou
  seja, ele é **instrumento de outros testes**, e ninguém verifica que **ele
  próprio** ainda cobra o que promete. Trocar os dois `assert` por `pass`
  mantém a suíte verde para a invariante e só reduz o vermelho alheio;
- **`assert` da linguagem SOME sob `python -O`.** Em produção, com otimização
  ligada, a invariante do funil **não existe**. A docstring diz *"o lugar de
  descobrir isso é a suíte, não o disco dela"* — o que é a decisão certa, e é
  exatamente por isso que a checagem não pode depender de uma construção que a
  suíte pode estar rodando e o produto não.

**A entrega é um teste que arranque a linha `self.draft = draft.with_profile_identity(profile)`
(`:191`) e exija que a invariante acuse**, mais a decisão declarada sobre `-O`:
ou vira `if ... raise AssertionError`, ou a docstring passa a dizer que a
garantia é de suíte e **só** de suíte.

### 3. `_reject_traversal` — nenhum caso nos caminhos de ESCRITA novos

**A `PERFIL-SEM-RASTRO-01` já corrigiu, no próprio texto, um briefing que dizia
que a função não tinha caso nenhum:** ela tem **seis** em
`tests/unit/test_profile_loader.py:245-275` e mais dois de boundary no IPC. A
correção fica registrada; a afirmação errada não foi apagada.

**A lacuna real é mais estreita e mais séria:** os oito casos existentes passam
todos por caminhos de **LEITURA**. A sprint deu à função **dois chamadores
novos** (`historico_dir:650` e `_slug_para_historico:682`) e, atrás deles, três
caminhos de **escrita** que não existiam:

| caminho | o que ele faz |
|---|---|
| `_arquivar_versao` → `historico_dir(slug, ensure=True)` | **`mkdir` + escrita** |
| `restaurar_do_historico` → `profiles_dir()/f"{slug}.json"` | **escrita no perfil** |
| a poda | **`unlink`** |

**Nenhum dos três tem caso de traversal**, e `_reject_traversal` é a **única**
barreira entre o identificador de um perfil e uma escrita fora de `profiles/`.
Agrava: `_slug_para_historico` prefere o identificador **literal** quando
`(raiz / identifier).is_dir()` (`:684-685`) — seguro **porque** a linha `:682`
já rodou. Tirar aquela linha abre o buraco inteiro e **nenhum teste avisaria**.

**A entrega:** um teste que chame `historico_dir("../../etc")`,
`listar_historico("..")` e `restaurar_do_historico("../x")` exigindo
`ValueError`, e que **reprove** com o `_reject_traversal` arrancado dos dois
chamadores novos.

**E o que NÃO se deve "consertar":** o `carimbo` de `restaurar_do_historico`
**não** passa por `_reject_traversal` (`:912-921`) — e não precisa, porque é
comparado contra o `v.name` de uma lista já produzida por `glob`. Está
registrado para que a próxima pessoa não conserte o que está certo.

---

## A DÍVIDA DOC-VERDADE-01 — três comandos que ela não tem como descobrir

**Grau: MEDIDO por `grep` em 05/08, ANTES desta leva de documentação.** Três
comandos entregues, testados, com **zero menção** na documentação de uso:

| comando | `docs/usage/cli.md` | `README.md` |
|---|---|---|
| `profile historico` | ausente | ausente |
| `profile restore [--em]` | ausente | ausente |
| `doctor --perfis` | ausente | ausente |

Onde a falta estava (números de linha da medição, **antes** da correção — hoje
deslocados pelo próprio conserto):

- `cli.md:23` listava `profile list/show/activate/create/delete/apply/save` — a
  linha não conhecia os dois novos;
- `cli.md:106-119` repetia a lista em blocos de exemplo;
- `cli.md:212` documentava o `doctor` com `--fix`, `--fix-safe` e `--quiet`,
  **sem `--perfis`**;
- no `README.md`, *"histórico"* só aparecia na linha 316, e era o `CHANGELOG`.

**Por que é grave e não cosmético:** é o caso exato da
[DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md)
visto de outro ângulo. **Um mecanismo de recuperação que a dona da máquina não
consegue descobrir é, do ponto de vista dela, um mecanismo que não foi
entregue** — e o `profile restore` é justamente o que devolve os perfis dela se
a próxima gravação errar de novo.

**Estado em 05/08:** o `docs/usage/cli.md` **foi pago** nesta mesma leva de
documentação (os três comandos entraram no resumo, no bloco de exemplos e na
lista de *Demais comandos*, com a assinatura conferida contra
`cli/cmd_profile.py` e `cli/cmd_doctor.py`). **O `README.md` continua ABERTO** —
é uma linha, e é entrega desta faixa, não da seguinte.

---

## A ORDEM DE EXECUÇÃO, e por que ela é essa

### 0º — commitar

Não é entrega, é preservação. **Antes de qualquer linha nova.** Ver o alerta do
topo.

### 1º — `REGRA-NÃO-SE-PERDE-02`

É a única decisão **dela** em aberto nesta faixa, e é a que fecha o mecanismo
que produziu a queixa de origem. Vem antes das lacunas de teste porque é a
única cujo custo cresce com o tempo: cada dia sem ela é mais um dia em que um
perfil novo pelo rodapé nasce sem regra.

**Não confundir com a `REGRA-NÃO-SE-PERDE-01`, que está paga.** A 02 é só o
nome novo.

### 2º — as três lacunas de teste, na ordem 3 → 2 → 1

O traversal primeiro porque é **escrita fora do diretório de perfis** e a
barreira é única; a invariante depois, porque protege o funil que tudo o mais
desta leva atravessa; a `verificar_perfis_do_disco` por último, porque a decisão
(ligar ou apagar) é barata e não bloqueia ninguém.

### 3º — o `README.md`

Uma linha. Fecha a `DOC-VERDADE-01` desta faixa.

### Fora de ordem, e por motivos próprios

- **`AUTOMATISMO-MORTO-01/E2`** — *"usar este perfil sempre neste jogo"*, o
  um-clique que fecharia a raiz das três queixas dela. **Não pode vir antes**
  das curas de escrita, senão o perfil promovido volta a catch-all no save
  seguinte. Com esta leva na árvore, ela **destravou**;
- **`ÁUDIO-QUE-TRANCA-01/E1` e `/E2`** — o `clear` da categoria `audio` e a
  granularidade da trava. Três sprints desta leva as citam como dívida e
  **nenhuma as toca**. Vão junto com a `POSSE-POR-CONTROLE-01/E1`, que mexe no
  **mesmo** `manual_override_categories` no eixo por controle, e nesta ordem
  (categoria primeiro, controle depois) — é a mesma recomendação do índice do
  Bluetooth, e o ponto de colisão está registrado como M-13;
- **isolar o `HOME` no autouse** (`CANÁRIO-FS-01`) — é a única cura que fecha a
  classe da **leitura**, e a própria sprint explica por que não entrou: o `HOME`
  é lido por muito mais coisa que os diretórios XDG (Steam, Proton, WirePlumber,
  glifos, locale), e trocá-lo em toda a suíte é superfície larga. **É entrega
  própria, e precisa de medição própria.**

### Se for executar UMA só

**`REGRA-NÃO-SE-PERDE-02`** — depois de commitar. É a decisão dela, é a última
metade do defeito que abriu a leva, e é a única cujo desenho já está escrito
(acima) esperando alguém transformá-lo em sprint.

---

## O QUE ESTA LEVA NÃO COBRE — e é decisão, não esquecimento

- **A origem do `191`** (DIV-1). **Continua indeterminada, e agora é
  decidível:** o `.historico/` e o `profile_salvo` com `origem=janela:<botão>`
  nasceram nesta madrugada, e o instrumento já capturou **uma** linha real —
  `match_antes=criteria match_depois=any priority_antes=10 priority_depois=191`,
  que é **um único save saltando de 10 para 191**: não é a catraca de +10 (daria
  20) e não é só o slider (que não mexe no `match`). **Falta o próximo gesto
  dela**;
- **Os arquivos de perfil dela.** Nenhuma linha desta leva os reescreve,
  inclusive o `sackboy_nativo.json`, inclusive *"só para normalizar"*. É o perfil
  **ATIVO**, catch-all, 191, com supressão ligada, e é o dado que arma quatro dos
  seis itens da sprint 4. **O destino dele é decisão DELA** — veto repetido em
  cinco documentos desta casa;
- **A tela.** **Ninguém olhou.** Nenhuma afirmação desta leva é sobre aparência,
  e há **três diálogos novos** (`confirm_downgrade_priority`,
  `confirm_downgrade_match_to_any` com `regra_atual`, e
  `confirm_discard_pending_edits`) que **nunca foram fotografados**. Interface
  não fecha sem o olho dela;
- **O aceite em uso real.** As bancadas provam o `OutputSpec`, o `relatorio`, os
  estados e o disco. Que o controle pare de mudar de cor sozinho no meio da
  partida, que o "Ativar" pare de mentir **na primeira vez** e que salvar duas
  vezes preserve o perfil dela — **só o uso dela fecha**;
- **O Steam Input.** O estudo tem uma seção inteira (D-31 a D-34, com um
  `--apply` que vai **apagar a decisão dela sobre o Sackboy**, provado em
  dry-run). **Nenhuma sprint desta leva o toca**, e o "portão zero" daquela faixa
  (M-04) **nunca foi rodado**. É leva própria, e é urgente por conta própria.

---

## O QUE NÃO DEVE SER TOCADO

Consolidado da seção 5.8 do estudo, com o que as sprints desta leva
acrescentaram. **Cada item foi pago com um defeito real, e mexer é regressão:**

1. **os arquivos de perfil dela, sem a mão dela** — inclusive dentro de script
   de instalação. *"Migração silenciosa de perfil é a classe de defeito que
   causou o rollback de 26/07"*;
2. **o veto R-21** (`manager.py:759-767`) — nem revogar, nem afrouxar. Sem ele
   volta o ping-pong de 18-28 s;
3. **o debounce assimétrico 0,5 s / 12 s** (`autoswitch.py:41-58`). E note que
   a cura do item 1 da sprint 4 **mexe no que arma o lado lento**: na divergência
   de crença ela assume `True` justamente para **não** encurtar a saída;
4. **o gate R-02 no ramo de LIBERAR** de `apply_profile_suppression` — o buraco
   era o ramo de **LIGAR**, e foi esse que se corrigiu;
5. **a ordem `clear` → `activate`** — acabou de ser corrigida; reverter reabre a
   `TRAVA-QUE-SOLTA-TARDE-01`;
6. **o `adiado=` do `profile_autoswitch`** — é o campo que a leitura de journal
   desta casa já procura. O `secoes=` **acrescenta**, não substitui;
7. **`_esquecer_a_fotografia_do_editor` não deve simplesmente sumir** — perfil
   que não existe não tem valor de disco a preservar. A cura foi de **escopo**;
8. **não tirar `"audio"` da lista de categorias** como cura da
   `ÁUDIO-QUE-TRANCA-01` — falta o clear e a granularidade, não a remoção;
9. **NÃO dar TTL à trava manual** como atalho para o eixo por controle;
10. **não esticar o `IPC_TIMEOUT` de leitura** do applet (`ipc.rs:31`, 250 ms)
    para "curar" o switch — a chamada que **muda o mundo** ganha folga própria; a
    leitura, não. Há teste só para impedir essa cura preguiçosa;
11. **não marcar nada como entregue de novo sem chamador em produção.** É a
    regra que a `ENTREGA-QUE-NÃO-LIGOU-01` institui, e esta madrugada achou
    **três casos novos** dela. **Nota de desenho registrada:** um portão de
    *"zero chamadores"* **não teria pego** o defeito do funil, porque
    `with_profile_identity` **tinha** chamador e ainda assim estava meio-ligado.

---

## Como retomar do zero

1. leia este índice;
2. **confira que a leva ainda está lá** — `git diff --cached --shortstat`. Se o
   índice estiver vazio e não houver commit novo, **pare e recupere antes de
   qualquer outra coisa**;
3. leia [o estudo dos dezessete agentes](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md) —
   os `D-nn` e `DIV-n` deste índice são todos dele;
4. leia a sprint que for executar: cada uma é auto-suficiente e declara o grau
   de cada afirmação;
5. rode a linha de base:
   ```bash
   git add -A                       # os portões são cegos a arquivo novo
   .venv/bin/python -m pytest -q    # 6968 passed, 1 skipped em 05/08
   .venv/bin/ruff check src/ tests/
   .venv/bin/mypy src/hefesto_dualsense4unix
   ```
   O canário do `$HOME` roda junto e **reprova a sessão** se a suíte tocar a
   configuração real dela. Se o daemon ou a janela dela estiverem de pé mexendo
   no `session.json`, a escotilha declarada é `HEFESTO_SEM_CANARIO_FS=1` —
   **melhor que comentar código**;
6. para conferir os perfis **dela** sem tocar em nada:
   ```bash
   hefesto-dualsense4unix doctor --perfis
   hefesto-dualsense4unix profile historico <nome>
   ```
7. a regra de aceite de interface continua sendo a
   [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
   foto antes e depois, e a palavra final é dela.

---

## O ESTRAGO QUE FICOU NO DISCO DELA — a cura não desfaz o passado

> **Grau: MEDIDO**, por `hefesto-dualsense4unix doctor --perfis` rodado contra a
> pasta de perfis real dela em 05/08/2026 às 22h40, com o daemon já reiniciado
> no código curado. Saída **1**, como o comando promete quando há achado grave.

Esta é a lição que a leva inteira quase deixou passar: **as sete curas impedem
que o estrago volte a acontecer, e nenhuma delas conserta o estrago já feito.**
O código está são; os arquivos dela, não.

O que o verificador acusa hoje, na máquina dela:

| grau | perfil | achado |
|---|---|---|
| **FAIL** | `sackboy_nativo` | vale para QUALQUER janela em prioridade **191** — igual ou acima de dez perfis que têm alvo próprio |
| WARN | `sackboy_nativo` | catch-all que ainda pede modo de jogo — o retrato de um perfil que PERDEU a regra |
| WARN | `vitoria` | idem |
| WARN | `Pragmata` | catch-all com nome de programa — perdeu a regra |
| WARN | — | **quatro** perfis casam com qualquer janela e disputam a mesma vaga: `Pragmata` (5), `meu_perfil` (1), `sackboy_nativo` (191), `vitoria` (0) |
| WARN | — | três empates de prioridade: `fallback`/`vitoria` em 0, `Corrida`/`Esportes` em 55, `FPS`/`point_and_click` em 60 |

O `sackboy_nativo` é o caso exemplar, e o asset de fábrica prova o que ele era:
`assets/profiles_default/sackboy_nativo.json` é `criteria` com
`window_class: ["steam_app_1599660"]` e prioridade 80. No disco dela virou
`MatchAny` com 191. **É literalmente o inverso do que ela pediu:** perde dentro
do Sackboy (o veto R-21 recusa catch-all em janela de jogo) e vence no desktop
inteiro, carregando a supressão de emulação junto.

### Por que não se conserta por script

Três caminhos, e o terceiro é o único honesto:

1. **Restaurar do asset de fábrica** — apagaria os ajustes que ela fez desde
   então (gatilhos, lightbar, som). O perfil está corrompido na REGRA, não no
   resto.
2. **Adivinhar a regra pelo nome** — `sackboy_nativo` sugere o appid, mas
   `vitoria` e `Pragmata` não sugerem nada verificável. Adivinhar aqui é
   inventar configuração dela, que é a raiz da queixa original.
3. **`profile historico`** — a cura certa, e ela existe desde a
   `PERFIL-SEM-RASTRO-01` desta mesma leva. As versões anteriores de cada perfil
   estão em `profiles/.historico/<slug>/`, e `profile restore --em <carimbo>`
   devolve os bytes originais. **Mas o histórico só grava a partir de 05/08** —
   as versões de antes da cura não existem. Para os perfis já corrompidos, o
   histórico não alcança.

**Então isto é trabalho DELA, com a janela aberta, e não trabalho de script.** A
receita que o próprio verificador imprime já diz o que fazer perfil a perfil, em
português: dar o alvo de volta na aba Perfis, ou declarar
`"match": {"type": "manual"}` para quem ela só ativa na mão, ou baixar para a
prioridade 0 quem é de desktop.

**O que a casa deve a ela aqui, e ainda não pagou:** o verificador só existe no
terminal. Nada no daemon o chama, nada na janela o mostra — é a entrega 4 da
`PERFIL-NASCE-CERTO-01`, marcada como PARCIALMENTE PAGA justamente por isso. Uma
pessoa que não abre terminal **não tem como descobrir** que quatro perfis dela
perderam a regra.
