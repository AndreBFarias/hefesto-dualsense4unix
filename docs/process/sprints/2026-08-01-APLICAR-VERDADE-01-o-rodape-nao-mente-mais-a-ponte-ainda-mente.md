# APLICAR-VERDADE-01 — o rodapé não mente mais, a ponte ainda mente

- **Estado:** CONCLUÍDA — **o resto medido FOI CURADO**:
  `apply_draft_detalhado()` (`app/ipc_bridge.py:597`) devolve a resposta inteira
  do daemon e a aba Lightbar já a consome (`app/actions/lightbar_actions.py:675`
  e `:785`); o `apply_draft` bool fica em `:659` por decisão escrita em
  `:603-611` (verificado em 21/08/2026)
- **Status em 01/08/2026, preservado:** ENTREGUE EM CÓDIGO, com **um resto
  medido**. Medido em 01/08/2026: a cadeia daemon -> IPC -> rodapé está
  completa e coberta por teste; o que ficou de fora é o segundo caminho da mesma chamada, o
  `ipc_bridge.apply_draft()`, que **estreita a verdade de volta para um `bool`**
  antes de ela chegar na aba Lightbar
- **Prioridade:** MÉDIA — nada aqui desfaz trabalho dela, mas o resto reproduz,
  numa aba que ela usa, exatamente a frase que esta sprint existiu para
  eliminar: mandar caçar o problema no lugar errado
- **Aberta em:** 01/08/2026, pela auditoria de 31/07 que contou treze
  identificadores sem documento
  (`docs/process/estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md:316`).
  O identificador é citado **de dentro de `src/`**, em
  `app/actions/footer_actions.py:65`, e apontava para o vazio
- **Relacionada:** `APLICAR-VERDADE-02` (28/07), que é o irmão de contabilidade
  e escapou de virar fantasma por acaso — virou anexo da
  [JANELA-CEGA-01](2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md),
  seção "Anexo — APLICAR-VERDADE-02, o irmão que entrou junto" (`:217`)
- **Não confundir com** a numeração 02: a **01** fez a falha SUBIR do daemon
  até a tela (o campo `failed`); a **02** consertou a *contabilidade* que
  decidia baixar o `dirty` e o que ia para o journal (`footer_actions.py:196`,
  `:604` e `:622`). São dois defeitos diferentes na mesma chamada

## O fato que resume a sprint

`profile.apply_draft` responde `{"status": "ok"}` **sempre** — e isso é decisão
registrada, não descuido (`daemon/ipc_handlers.py:445-448`: applet, CLI e TUI
decidem pelo `status`, e um `"failed"` ali faria os três dizerem *"daemon
offline"* para uma seção que simplesmente não entrou). Enquanto a resposta só
carregava `applied`, o rodapé decidia pelo `status` e anunciava
*"Perfil aplicado ao controle."* com as sete seções fora.

A cura foi **aditiva**: o daemon passou a devolver também `failed`, um mapa
`seção -> motivo curto`, e a janela passou a lê-lo. Hoje o rodapé diz
*"Aplicado, menos: luzes, gatilhos."* quando é isso que aconteceu.

O resto que este documento abre é de uma linha só, e é a fronteira por onde a
verdade escapa: **`ipc_bridge.apply_draft()` devolve `bool`.** Quem chama por
ali recebe True ou False e não tem como saber qual seção caiu — então a aba
Lightbar, que é a única que usa esse caminho, volta a dizer a frase errada.

## O que já existe, medido em 01/08/2026

A cadeia inteira, elo a elo:

| Elo | Arquivo:linha | O que faz hoje |
|---|---|---|
| O applier registra a falha | `daemon/ipc_draft_applier.py:40-44` | `self.failed: dict[str, str]`, com o comentário que cita o identificador |
| ...em vez de a engolir no log | `daemon/ipc_draft_applier.py:90-111` | `except` loga o warning **e** grava `self.failed[section] = motivo[:120]` |
| ...e zera a cada `apply` | `daemon/ipc_draft_applier.py:71-73` | o mesmo applier pode ser reusado; cada aplicação conta a história dela |
| O handler devolve o mapa | `daemon/ipc_handlers.py:456` | `{"status": "ok", "applied": applied, "failed": dict(applier.failed)}` |
| ...com o contrato explicado | `daemon/ipc_handlers.py:443-448` | por que `status` continua `"ok"` de propósito, e que a verdade nova é ADITIVA |
| A janela traduz o nome da seção | `app/actions/footer_actions.py:65-80` | `_NOMES_DE_SECAO`: `leds` -> `luzes`, `triggers` -> `gatilhos`, `rumble` -> `vibração`, `mic` -> `microfone`, `controllers` -> `ajustes por controle` |
| ...em PT-BR cru, traduzido no uso | `footer_actions.py:66-69` | o dicionário nasce no import, antes do `init_locale()`; traduzir ali congelaria o idioma errado |
| ...e cabe na statusbar | `footer_actions.py:80-82` e `:595-599` | acima de três seções vira "as três primeiras e mais N" |
| A frase final | `footer_actions.py:635-657` | `Nada foi aplicado ao controle.` / `Aplicado, menos: {secoes}.` / `Perfil aplicado ao controle.` |
| ...e o caminho que a vê | `footer_actions.py:235-241` | `on_apply_draft` usa `ipc_bridge.call_async`, que entrega o **dicionário** — é por isso que o rodapé enxerga o `failed` |
| A tradução | `po/en.po:1553` | `APLICAR-VERDADE-01: nomes das secoes do perfil, como a usuaria le nas abas` |
| O teste que morde | `tests/unit/test_aplicar_verdade_rodape.py` | 334 linhas; cobre os três elos e o contrato que não pode mudar |

Duas medições que decidem o veredito, e nenhuma vem de campo `Status:` — a
auditoria de 31/07 mediu 41 de 50 cabeçalhos dizendo ABERTA, incluindo entregas
provadas:

1. **A cobertura das seções está completa.** O applier aplica sete seções
   (`ipc_draft_applier.py:74-87`: `leds`, `triggers`, `controllers`, `rumble`,
   `mouse`, `keyboard`, `mic`) e o `_NOMES_DE_SECAO` tem exatamente essas sete
   chaves. Nenhuma seção cai na tela com o nome técnico por esquecimento — e
   quando cair (daemon mais novo que a janela), o `_lista_de_secoes`
   (`:578-584`) mostra o nome cru de propósito, *"melhor um termo estranho do
   que omitir que algo ficou de fora"*.
2. **Nenhuma outra superfície precisa do `failed`.** `grep -rn "apply_draft"`
   fora de `daemon/` devolve só a janela: `app/ipc_bridge.py`,
   `app/actions/footer_actions.py`, `app/actions/lightbar_actions.py` e
   `app/draft_config.py`. A CLI não chama `profile.apply_draft`, e o applet
   COSMIC também não (`grep -in "apply_draft" packaging/cosmic-applet/src/`
   devolve vazio). O escopo desta sprint é a janela, e sempre foi.

## O resto: onde a verdade ainda morre

`app/ipc_bridge.py:495-523` — a assinatura é `def apply_draft(draft_dict) ->
bool`. Ela faz a coisa certa até a metade: recusa `status != "ok"` e trata
`applied` vazio como no-op honesto (`:518-521`, a cura R-18 de 23/07). Mas o
`failed` **nunca sai da função**. O chamador recebe `False` e não tem como
distinguir *"o daemon está desligado"* de *"a seção de luzes falhou"*.

Quem paga são as duas chamadas da aba Lightbar:

| Chamada | Arquivo:linha | O que a tela diz quando volta `False` |
|---|---|---|
| "Aplicar" com a cor única (caminho degradado COR-04) | `app/actions/lightbar_actions.py:568-577` | `não consegui aplicar a cor — o Hefesto pode estar desligado (ligue na aba Sistema)` (`:586-590`) |
| "Apagar" pelo mesmo caminho | `app/actions/lightbar_actions.py:653` | `Falha (daemon offline?)` (`:669`) |

As duas frases mandam caçar o problema no lugar errado quando o daemon está
vivo e foi a seção `leds` que falhou — que é, palavra por palavra, o defeito
que esta sprint curou no rodapé. O rodapé escapou porque não usa a ponte: usa
`call_async` direto e recebe o dicionário.

**Isto é resto medido, não defeito novo.** A ponte foi escrita antes do campo
`failed` existir, e o `bool` era o contrato inteiro na época.

## Entregas

### E1. Este documento existe, e o código deixa de apontar para o vazio

Sete citações, em três arquivos de `src/`, e nenhuma tinha para onde apontar:
`footer_actions.py:65`, `:581` e `:638`; `ipc_handlers.py:443`;
`ipc_draft_applier.py:6`, `:40` e `:104`.

**Aceite:** `grep -rn "APLICAR-VERDADE-01" docs/process/sprints/` devolve este
arquivo. Nenhuma linha de `src/` muda nesta entrega.

### E2. A ponte para de estreitar a verdade

`ipc_bridge.apply_draft()` passa a devolver a resposta que recebeu, sem a
perder — e os dois chamadores da Lightbar passam a distinguir *"o Hefesto está
desligado"* de *"a seção de luzes não entrou"*, usando o mesmo
`_mensagem_de_aplicacao` que o rodapé já usa (`footer_actions.py:635`), para
não nascer um terceiro dono da frase.

A forma exata é decisão de quem implementar, e há duas com custo diferente:

- **Aditiva (mais barata):** um `apply_draft_detalhado()` ao lado, devolvendo o
  dicionário; a `apply_draft()` de hoje continua devolvendo `bool` e passa a
  ser um invólucro dela. Ninguém quebra, e o `__all__` do bridge (`:653`) ganha
  um nome.
- **Direta:** mudar o tipo de retorno de `apply_draft()` e ajustar os dois
  chamadores. Menos superfície no fim, mas mexe numa função exportada.

**Aceite:** com o daemon VIVO e a seção `leds` falhando, "Aplicar" na aba
Lightbar (caminho COR-04, sem controle selecionado no seletor) mostra uma frase
que fala da seção, não do daemon; e com o daemon desligado a frase continua
sendo a de hoje, palavra por palavra. As duas metades têm de ser conferidas —
consertar só a primeira troca uma mentira por outra.

**Risco:** baixo, com uma armadilha nomeada. `_algo_foi_aplicado`
(`footer_actions.py:603-618`) e `_mensagem_de_aplicacao` (`:635-657`) tratam
resposta SEM os campos novos como sucesso, de propósito (daemon antigo). Quem
mexer na ponte não pode fazer o `bool` cru virar `{"status": "ok"}` sintético —
isso apagaria a distinção que as duas funções documentam e que a
APLICAR-VERDADE-02 já pagou para manter.

### E3. O contrato do `status` fica travado por escrito

`status` é `"ok"` para sempre, e o motivo está em `ipc_handlers.py:445-448` e
em `ipc_bridge.py:509-512`. Quem "consertar" isso para `"partial"` faz o applet
e a CLI dizerem *"daemon offline"* para uma seção que falhou — o defeito trocado
de lugar, não curado.

**Aceite:** o teste que já existe cobre isso (ver abaixo) e ninguém precisa
lembrar. Esta entrega é a frase, não código.

## Teste que morde

**Já existe:** `tests/unit/test_aplicar_verdade_rodape.py`, 334 linhas, verde
em 01/08. Ele abre com a cadeia do defeito medida antes da cura — os três elos
— e cobre os três, mais o contrato que não pode mudar: `status` continua
`"ok"`, e resposta de daemon antigo, sem os campos novos, continua sendo lida
como sucesso.

Uma nota de portão que importa: o arquivo chama `exigir_gi_real()` nas linhas 20 e 26,
**antes de qualquer import de `gi`**, com o comentário explicando por quê. Isso
significa que ele **pula no CI** (que roda sem PyGObject, decisão registrada em
`.github/workflows/ci.yml`, `CI-GUI-PULAVA-CALADO-01`) e só morde na máquina de
desenvolvimento. Não é defeito deste teste; é a dívida declarada daquele job. É
honesto saber disso antes de contar com ele como rede.

**O teste que a E2 precisa criar**, e que não existe hoje:

> Com um dublê de `_safe_call` devolvendo
> `{"status": "ok", "applied": [], "failed": {"leds": "erro qualquer"}}`, o
> caminho da Lightbar tem de produzir uma frase que contenha o nome da seção
> (`luzes`) e **não** contenha `desligado` nem `offline`. Com o dublê
> devolvendo falha de transporte, a frase tem de continuar sendo a de hoje.

**A mordida:** arrancada a cura da E2 — voltando o `bool` na ponte — a primeira
metade fica vermelha, porque a informação da seção deixa de existir antes de
chegar na frase. Um teste que passe com a ponte antiga não está medindo a E2:
está medindo que a frase de daemon desligado continua no lugar, que é a segunda
metade.

## O que NÃO fazer

- **Não trocar o `status` por `"partial"`/`"failed"`.** Está explicado em dois
  arquivos e é a razão de a cura ter sido aditiva. Applet, CLI e TUI decidem
  pelo `status`.
- **Não traduzir o `_NOMES_DE_SECAO` no ponto de declaração.** Ele é construído
  no import, antes do `init_locale()`; traduzir ali congela o idioma errado. A
  tradução acontece no uso, em `_lista_de_secoes` (`footer_actions.py:592`).
- **Não fazer resposta sem `applied`/`failed` virar erro.** Daemon antigo tem
  de continuar sendo lido como sucesso — é o que `_algo_foi_aplicado`,
  `_secao_aplicada` e `_mensagem_de_aplicacao` afirmam nos três, e as três não
  podem divergir entre si.
- **Não criar uma quarta frase de estado.** A janela já tem
  `_mensagem_de_aplicacao`; a Lightbar tem de a chamar, não copiar. A
  RADAR-01/E4 existe justamente porque frase copiada entre superfícies diverge.
- **Não confiar no campo `Status:`** de nenhum documento citado aqui. Tudo
  nesta página foi derivado do código de 01/08/2026.

## O que eu NÃO medi

- **Não rodei a janela.** Nada aqui foi visto na tela: a cadeia foi lida no
  fonte e conferida contra o teste que já existe. O aceite da E2 é o olho dela,
  como manda a
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
- **Não provoquei uma falha de seção de verdade.** Saber QUAIS exceções o
  `_apply_section` pega na prática (hardware desconectado no meio, permissão de
  hidraw, seção com schema inválido) exigiria o controle na mesa e um daemon
  instrumentado. O motivo curto é cortado em 120 caracteres
  (`ipc_draft_applier.py:111`) e ninguém verificou se algum deles fica
  ilegível na statusbar.
- **Não medi o caminho `led_set` clássico.** As duas chamadas da Lightbar que
  passam pela ponte são as do caminho degradado COR-04 e do "Apagar" sem alvo;
  o caminho com um controle selecionado usa `led_set` e nunca tocou em
  `apply_draft`. Se ele mente também, mente por outro motivo e é outra sprint.
- **Não conferi o catálogo `.mo`.** A entrada existe no `po/en.po:1553`; o mapa
  de 29/07 registra que os `.mo` estavam três commits atrás dos `.po` e sem
  gate (`:1399`), então a frase traduzida pode não ter chegado a instalação
  nenhuma. Não é achado desta sprint, mas afeta o que ela vê em inglês.
