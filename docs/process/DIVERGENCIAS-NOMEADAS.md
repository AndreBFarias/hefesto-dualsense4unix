# Divergências nomeadas — os apelidos que NÃO são sprints

- **Criado em:** 11/08/2026, pela sprint `A-9 NOME-QUE-NÃO-EXISTE-01`
- **Emendado em:** 12/08/2026 — [a terceira classe](#a-emenda-de-12082026--a-terceira-classe-e-quando-um-apelido-vira-documento)
- **Grau:** MEDIDO — a varredura que achou os três está em
  [INDICE duas verdades](sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md),
  itens S-5, S-6 e P-11

## Por que este arquivo existe

Esta casa batiza defeitos. É bom: um nome curto viaja bem por comentário de
código, mensagem de commit e conversa. O problema aparece quando o nome é citado
como *"ver a sprint X"* ou *"o estudo X"* — e **não existe arquivo nenhum com
esse nome**. Quem lê vai procurar, não acha, e ou perde tempo ou conclui que a
página está velha.

Medido em 11/08/2026: três apelidos estavam nessa situação, somando **26
citações em 19 arquivos**, incluindo `src/` e um cabeçalho de patch que vai para
o upstream.

**A regra, daqui em diante:** um apelido é uma de duas coisas.

- **Sprint ou estudo** — tem arquivo em `docs/process/sprints/` ou
  `docs/process/estudos/`, e se cita com link.
- **Divergência nomeada** — é só um apelido para uma discordância entre fontes,
  registrada **aqui**. Cita-se dizendo o que é: *"a divergência `NOME` (ver
  DIVERGENCIAS-NOMEADAS.md)"*, nunca *"a sprint `NOME`"*.

> **Nota de 12/08/2026 — esta regra tinha dois terços.** O texto de 11/08
> fechava aqui com: *"Não há terceira opção. Um nome que não é nenhum dos dois
> é um nome que mente."* A varredura de 12/08 contou **540 apelidos em `src/`**
> e **298 sem página em `docs/`**; a maioria esmagadora não mente nem promete
> documento nenhum — é citação de comentário, não declaração. A frase caducou
> como regra geral e foi **substituída** pela [emenda de
> 12/08](#a-emenda-de-12082026--a-terceira-classe-e-quando-um-apelido-vira-documento),
> que acrescenta a terceira classe e diz quando um apelido de `src/` **deve**
> virar documento. As duas classes acima continuam valendo, sem mudança.

---

## A emenda de 12/08/2026 — a terceira classe, e quando um apelido vira documento

- **Grau:** MEDIDO — a régua está declarada abaixo, e os números são
  reprodutíveis com ela.

### A régua, declarada

Todo instrumento desta casa declara com o que mediu. Um apelido, aqui, é:

```
\b([A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9]{1,}(?:-[A-ZÀ-ÖØ-Þ0-9]{1,}){0,8}-\d{2})\b
```

O primeiro pedaço **tem de começar por letra**. Sem essa cláusula a régua colhe
data (`2026-07-16`), faixa (`40-80`) e versão como se fossem apelidos, e
infla a conta em cerca de 12%. A varredura roda sobre `git ls-files src docs
tests`, e separa `docs/process/agentes/` do resto: transcrito de agente é
registro de conversa, **não é página onde alguém procura**.

### O que a varredura de 12/08/2026 achou

| medida | número |
| --- | ---: |
| apelidos únicos em `src/` | 540 |
| apelidos únicos em `docs/`, fora de transcrito de agente | 512 |
| apelidos únicos em `tests/` | 565 |
| união das três árvores | 885 |
| **em `src/` e em nenhuma página de `docs/`** | **298** |
| destes, os que só existem em transcrito de agente | 4 |

Distribuição dos 298 pelo número de citações em `src/`: **108** aparecem uma
vez só, **95** de duas a quatro, **54** de cinco a nove, **41** dez ou mais.
Por família: 97 são `BUG-*` (42 com teste citando o mesmo apelido), 51 são
`FEAT-*` (45 com teste), e 52 são apelidos-frase do tipo
`ORIGEM-QUE-MENTE-01`.

**Onde este número diverge do primeiro que se falou (276).** A régua acima dá
294 contando qualquer arquivo de `docs/`, e 298 quando transcrito de agente
não conta como página. A diferença para 276 é de régua, não de repositório: os
limites de acento e o começar-por-letra mudam a colheita em poucos por cento.
A divergência é pequena e não move a conclusão — **a ordem de grandeza é
trezentos, não três**, e é isso que derruba a regra de 11/08. Guardado aqui
porque medida que muda com a régua é medida que merece a régua escrita ao lado.

### A terceira classe: **apelido de código**

Um apelido é uma de **três** coisas. Às duas de 11/08 acrescenta-se:

- **Apelido de código** — um fio, não uma promessa. Ele existe para que
  `grep -rn APELIDO src/ tests/` reúna num só resultado as linhas espalhadas
  que resolvem a mesma coisa. Não diz *"existe uma página com este nome"*; diz
  *"estas dez linhas em seis arquivos são o mesmo assunto"*.

**Como se reconhece.** Os três sinais, e basta um:

1. Aparece **dentro** de comentário, docstring ou nome de teste — não em prosa
   que manda o leitor a algum lugar.
2. Não vem precedido de *"a sprint"*, *"o estudo"* ou *"a divergência"*. Um
   apelido de código se cita nu: `# PERFIL-04: as seções globais...`.
3. Não há uma citação "definidora" entre as demais. `SOM-02` aparece **99
   vezes em `src/`** e nenhuma delas é a definição — todas são a mesma marca
   pregada em lugares diferentes. Isso é o normal da classe, não um defeito.

**Por que ela NÃO precisa de página própria.** Porque a página não teria o que
dizer. O conteúdo de um apelido de código é o conjunto das linhas que ele
marca; um arquivo que repetisse aquilo ficaria velho no primeiro `git commit`,
e o `grep` continuaria sendo a fonte melhor. E porque a conta não fecha: 298
apelidos são 298 páginas, e a regra viraria um dever que ninguém paga — regra
que ninguém paga não é regra, é dívida escrita na parede.

**O que ela DEVE, então.** Três deveres, todos baratos:

- **Ser achável.** Uma grafia só. Medido em 12/08:
  `DIÁLOGO-QUE-MATA-A-JANELA-01` mora em **quatro** arquivos de `src/`, e
  `DIALOGO-QUE-MATA-A-JANELA-01` — o mesmo apelido, sem o acento — mora em
  `app/actions/home_actions.py` e num teste. Do mesmo jeito,
  `ESCOLHA-DELA-VENCE-01` convive com `ESCOLHE-DELA-VENCE-01`. Quem procura por
  uma grafia não acha as citações da outra — que é exatamente o serviço que a
  classe existe para prestar, quebrado. Ao batizar, prefira a forma **sem
  acento**: ela sobrevive a copiar-e-colar de terminal.
- **Ser honesto.** Nunca ser citado como *"a sprint"* ou *"o estudo"*. Esta é a
  regra de 11/08 inteira, e a emenda não a afrouxa em nada.
- **Ser datado na primeira citação.** `# BATERIA-QUE-NAO-CHEGOU-01 (09/08/2026)`
  custa nove caracteres e diz de que época é o assunto.

### Quando um apelido de `src/` **deve** virar documento

Três gatilhos. **Basta um** disparar, e a promoção é obrigatória. Nenhum
disparou: o apelido fica onde está.

**G1 — segura um número que a bancada pagou.**
O comentário carrega uma medição que o código não recalcula: uma taxa, uma dose,
um byte de `status`, um comportamento do aparelho, um número que só apareceu
porque alguém ligou quatro controles na mesa.
*O teste:* **apagar esta linha obrigaria alguém a montar a bancada de novo?**
Se sim, o número não pode morar em comentário — comentário se apaga numa
refatoração distraída, e o custo se paga duas vezes. É a regra da casa
(*"apagar isto faria repetir trabalho ou pagar custo já pago?"*) aplicada a
apelido.

**G2 — governa uma vontade dela, não um mecanismo.**
O apelido nomeia algo que **ela decidiu**: uma preferência, uma escolha de
produto, uma regra de comportamento que não decorre de nenhuma restrição
técnica.
*O teste:* **um mantenedor futuro poderia "consertar" isto de boa-fé, e estaria
errado?** Se sim, vira documento. Mecanismo se defende sozinho — quem o quebra
vê o teste ficar vermelho. Decisão dela não tem essa defesa: ela só existe
enquanto alguém lembra, e comentário de código não é lugar de lembrar.

**G3 — o nome sai de casa.**
O apelido aparece em `src/` **e** em algo que atravessa a fronteira do
repositório: cabeçalho de patch para o upstream, `install.sh`, arquivo de
empacotamento, mensagem que a usuária lê na tela, comando de CLI documentado.
*O teste:* **alguém que não tem este repositório encontra este nome?** Se sim,
essa pessoa não pode dar `grep`, e o nome sem página é um beco.

#### A cláusula que impede a inflação

**Contagem de citação nunca promove.** Nem 99, nem 500. O par medido em 12/08
diz o porquê melhor que qualquer argumento:

| apelido | em `src/` | em `docs/` (antes desta emenda) | em `tests/` | gatilho | veredito |
| --- | ---: | ---: | ---: | --- | --- |
| `PERFIL-04` | 28 | 0 | 10 | nenhum | fica como apelido de código |
| `A-VONTADE-DA-GUI-PREVALECE-01` | 1 | 0 | 0 | **G2** | **deve virar documento** |

O apelido mais citado de `src/` sem página não deve nada: quem lê qualquer uma
das 28 linhas entende o assunto, e as outras 27 dizem o mesmo. O apelido citado
**uma vez só** é uma decisão dela de 09/08 pendurada num comentário de
`footer_actions.py`, sem página e sem teste — se aquela linha sumir, a decisão
some com ela. A contagem é o inverso da dívida neste par, e por isso não serve
de critério.

> A coluna diz *antes desta emenda* por um motivo que prova a tese: ao citar os
> dois apelidos na tabela acima, esta página passou a ser o único arquivo de
> `docs/` que os contém — e **não quitou dívida nenhuma**. Continua faltando a
> página do `A-VONTADE-DA-GUI-PREVALECE-01`. Aparecer numa lista não é ter
> página; **citação não é sede**, e é exatamente por isso que contar citações
> nunca respondeu à pergunta.

#### O caso `BUG-*`: a promoção é um TESTE, não uma página

Um `BUG-*` cuja cura já está na árvore **não pede documento**. O defeito
acabou; o que precisa sobreviver não é a história dele, é a **garantia de que
não volta** — e isso um teste faz, uma página não. O teste é executável, é
verificado a cada `pytest`, e **morde**: arranque a cura e ele reprova.

Medido em 12/08: dos 97 `BUG-*` sem página, **42 já têm teste citando o mesmo
apelido**. Esses estão fechados, e nada devem. Os **55 restantes devem um
teste**, não uma página — dívida mais barata e mais útil que a que a regra de
11/08 teria cobrado deles. O mesmo vale para `FEAT-*`: 45 dos 51 já têm teste.

A exceção é quando `BUG-*` dispara **G1**: se o conserto só foi possível depois
de uma medição da bancada, a medição vira página **e** o conserto vira teste.
Dois deveres diferentes, porque protegem coisas diferentes.

### Um portão barato, se ela quiser — não implementado

O critério acima é humano nos gatilhos G1 e G2: nenhuma máquina julga se um
número é recalculável ou se uma escolha foi dela. **G3 e o dever da honestidade
são checáveis por `grep`**, e o mais barato dos dois já tem material hoje:

> Reprovar toda prosa que diga *"a sprint `X`"* ou *"o estudo `X`"* quando não
> existe arquivo em `docs/process/sprints/` ou `docs/process/estudos/` que
> carregue `X` no nome ou no corpo.

É exatamente o defeito que criou este arquivo em 11/08, e não tem falso
positivo contra as três classes: um apelido de código nunca se anuncia como
sprint. Medido em 12/08: **34 afirmações desse tipo fora de transcrito, 27 com
arquivo e 7 sem** — entre elas `UI-GLOBAL-FOOTER-ACTIONS-01` em
`app/draft_config.py` e `FEAT-POINT-AND-CLICK-01` em
`tests/unit/test_profiles_preset.py`.

**Não implementado de propósito.** Portão novo sem ela pedir é escopo que
vazou, e há trabalho em cima dos portões nesta mesma sessão.

---

## As divergências registradas

### `GUERRA-01` — quem manda no hidraw quando o Proton entra

**O que nomeia:** a disputa entre o `winebus.sys` do Proton, o SDL e o nosso
gamepad virtual pelo mesmo controle. O nome nasceu em 18/07/2026 num estudo que
**nunca virou arquivo**; o que existe do assunto está espalhado em comentários
de código e, desde 11/08, em
[pilha-steam-input-xpad-sdl.md](../protocol/pilha-steam-input-xpad-sdl.md).

**Estado:** o mecanismo está **medido e com grau ALTA** — o fonte do Proton
(`main.c`, `unixlib.h`) confirma que o `winebus` casa VID/PID por texto e trata
`0x0df2` explicitamente, e que `SDL_GAMECONTROLLER` tem **zero ocorrências**
naquele caminho. É por isso que `PROTON_DISABLE_HIDRAW` existe: a variável do
SDL não cobre o winebus.

**Onde ler:** a página da pilha, seção do `winebus`. **Não procure por um
estudo de 18/07 — ele não existe.**

### `GYRO-EDGE-RATE-01` — a taxa que o vpad declara e a que ele entrega

**O que nomeia:** o gamepad virtual se declara DualSense Edge, e o SDL trata o
Edge como 1000 Hz por USB (`SDL_hidapi_ps5.c`, decisão por tabela, sem medir).
O que ele entrega é a taxa do controle físico.

**Estado, medido em 11/08:** o cabo entrega **250,0 Hz exatos** — duas réguas
independentes concordando, e batendo com o descritor USB. O rádio é **variável,
em rajadas** (363, 240, 334, 55 e 70 Hz em cinco janelas), e **nunca 1000 Hz**.

**O que continua sem medição:** o que de fato quebra num jogo que integre pela
taxa declarada em vez de medir os intervalos. A conta sugere erro de escala de
4x; ninguém observou o efeito.

**Onde ler:** [driver-hid-playstation.md](../protocol/driver-hid-playstation.md).

### `NINTENDO-VARIANT-01` — distinguir o Pro genuíno do clone em runtime

**O que nomeia:** o produto escreve e o `doctor` confere uma marca
`HEFESTO_CONTROLLER_VARIANT`, e **nenhum arquivo de `src/` a lê**. É a
`ENTREGA-QUE-NÃO-LIGOU` na forma clássica.

**Estado, medido em 11/08:** o discriminador que funciona é o `bcdDevice` do
descritor USB — `0210` no genuíno, `0200` no clone. A marca **vive no `hidraw`**,
**não persiste no device `hid`** (o udev só guarda propriedade de device com nó
em `/dev`), e **é impossível por Bluetooth**: o Pro por rádio pendura em `uhid`,
e a cadeia inteira não tem `bcdDevice`.

**O caminho barato, se alguém for fechar:** ler a marca do `hidraw`, onde
`src/hefesto_dualsense4unix/core/external_leds.py` já resolve o caminho.

**Onde ler:**
[driver-hid-nintendo-por-dentro.md](../protocol/driver-hid-nintendo-por-dentro.md).

---

## Como acrescentar uma

Batizou uma discordância entre fontes e não vai escrever sprint para ela? Uma
entrada aqui, com quatro coisas: **o que nomeia**, **o estado** (com grau), **o
que continua sem medição**, e **onde ler**. Se depois virar sprint de verdade, a
entrada aponta para o arquivo novo e some daqui.

**Antes de escrever a entrada, confira que é mesmo uma divergência.** Desde
12/08 há três destinos possíveis para um apelido, e o desvio mais comum é
registrar aqui o que era só marca de comentário:

| o apelido nomeia... | vai para |
| --- | --- |
| um trabalho com começo e fim | sprint ou estudo, com arquivo e link |
| uma **discordância entre fontes** | uma entrada aqui |
| um assunto espalhado por linhas de código | fica onde está: **apelido de código** |

E se for apelido de código, passe-o pelos [três
gatilhos](#quando-um-apelido-de-src-deve-virar-documento) antes de decidir que
não deve nada.
