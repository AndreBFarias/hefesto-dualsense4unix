# RÓTULOS DE SPRINT-01 — "entregue no código" não é "validado por ela"

- **Escrito em:** 09/08/2026, a pedido dela
- **Grau:** o inventário de rótulos é **MEDIDO** (varredura dos cabeçalhos
  `Status:` e `Estado:` de todas as sprints); a consolidação é **DECISÃO**
- **O pedido dela, literal:** *"precisamos inclusive que um agente procure as
  sprints em aberto que acabamos desenvolvendo e marque elas como concluída (se
  de fato forem), mas aguardando validação manual do user"*

---

## 1. O que a frase dela pede, e por que um rótulo só não bastava

A frase tem **duas afirmações**, e elas não são a mesma coisa:

- *"marque elas como concluída (se de fato forem)"* — o código está de pé;
- *"mas aguardando validação manual do user"* — **ela ainda não viu**.

Um rótulo que diga só a primeira mente por omissão: quem ler `ENTREGUE` para de
olhar, e a sprint some da fila sem nunca ter passado pelos olhos dela. Um rótulo
que diga só a segunda esconde trabalho feito, e a próxima pessoa reescreve o que
já existe. **O rótulo tem de dizer as duas ao mesmo tempo.**

## 2. O vocabulário que a casa já tinha — inventário medido

Varridos os cabeçalhos de todas as sprints em `docs/process/sprints/` em
09/08/2026:

| rótulo | o que significa | exemplo |
|---|---|---|
| `ABERTA` | nada feito, ou feito e não medido | o mais comum |
| `PROPOSTA` | documento de desenho; nenhuma linha tocada | as sprints de 03/08 |
| `LEVANTAMENTO MEDIDO` | medição sem plano de execução | SENSOR-VIVO-01 |
| `ROTEIRO` | não é sprint de execução | PEDIDOS-DELA-01 |
| `PARCIAL` / `PARCIALMENTE PAGA` | parte entrou, parte não | EMPATE-01, PERFIL-NASCE-CERTO-01 |
| `ENTREGUE` | entrou e está fechada | NUM-01, PORTÃO-VIVO-01 |
| `ENTREGUE EM CÓDIGO` | entrou, **falta o aceite dela** | ALINHA-DUAS-LINHAS-01, APLICAR-VERDADE-01, JANELA-QUE-RESPIRA-01 (01/08) |
| `CURADO E MEDIDO` | entrou e foi medido no hardware dela | BT-SDP-VAZIO-01 |
| `CICATRIZ` | o defeito passou; fica a lápide | CÓDIGO-MORTO-01 |
| `REFUTADA` | a hipótese caiu por medição | LIGHTBAR-BT-CLAIM-01 |
| `FECHADA` | encerrada, sem resto | CR-05 |

**O rótulo que ela pediu já existia pela metade:** `ENTREGUE EM CÓDIGO` nasceu em
01/08 e sempre veio acompanhado de uma frase solta — *"falta o olho dela na
tela"*, *"com um aceite pendente"*, *"menos a palavra final dela"*. Três
redações para a mesma ideia, e nenhuma pesquisável.

## 3. O rótulo consolidado — o único criado nesta rodada

```
ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA
```

**Não é nome novo: é a junção dos dois pedaços que a casa já usava**
(`ENTREGUE EM CÓDIGO`, de 01/08, mais o *"menos a palavra final dela"* que a
ESCONDER-EM-VEZ-DE-SAIR-01 escreveu em 09/08). Segue a regra dela sobre
vocabulário: nome novo que não deriva do que há é sinal de conceito errado.

**Quando usar:** o símbolo existe, tem chamador, tem teste — e o aceite da
sprint depende de a Vitória ver, ouvir ou jogar.

**Quando NÃO usar:**

- **portão** (`ENTREGUE EM CÓDIGO`, sem sufixo): quem valida é o CI, não ela.
  Foi o caso da RADAR-01/E4 e da DOC-VERDADE-02/E10;
- **código escrito e sem chamador**: isso não é entrega, é
  [ENTREGA-QUE-NÃO-LIGOU](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md);
- **hardware nunca medido**: continua `ABERTA`, por mais bonito que esteja o
  código.

## 4. Toda sprint remarcada ganha três coisas, e nenhuma é opcional

1. **O rótulo anterior preservado por extenso** no próprio cabeçalho. Regra da
   casa: *não se apaga decisão medida — ela ganha nota datada com o que caducou*.
2. **Uma linha em português leigo** dizendo o que ela precisa validar — no campo
   `O que falta ela validar, em uma linha:`. Sem isso a marca vira burocracia:
   ninguém sabe o que fazer com ela.
3. **Uma nota datada no fim**, com `caminho:linha`, commit e data — e **a lista
   nominal do que continua aberto**. Sprint parcial que não nomeia o resto vira
   sprint esquecida.

## 5. A regra que falta no portão — proposta, não entrega

**O defeito, medido:** o campo `Status:` é o único lugar do repositório que
afirma o estado de uma sprint, e **nada o confere**. Em 31/07 a auditoria contou
41 de 50 cabeçalhos errados; em 09/08, 17 sprints diziam `ABERTA` ou `PROPOSTA`
com o código de pé, algumas desde 25/07. Isso não é descuido: é **um campo sem
portão**, e todo campo sem portão apodrece.

**A regra proposta para `scripts/validar-referencias-docs.py` (regra 4):**

> Reprova o documento em `docs/process/sprints/` cujo cabeçalho declare
> `ABERTA` ou `PROPOSTA` **e** que cite, entre crases, um símbolo Python
> (`funcao_assim`, `ClasseAssim`) que exista em `src/` **com pelo menos um
> chamador fora do arquivo em que é definido**.

**Por que o chamador, e não a mera existência:** símbolo definido e não chamado é
exatamente a `ENTREGA-QUE-NÃO-LIGOU` — código escrito e desconectado, que **não é
entrega**. Cobrar a existência marcaria como pronta uma sprint que ainda deve
tudo. O chamador é a diferença entre *escrito* e *ligado*, e é ela que o portão
tem de medir. Hoje, por exemplo, `esconder_o_fisico_para_o_jogo`
(`daemon/subsystems/gamepad.py:339`) tem chamador em `:312` e conta; já
`external_mask.py` não tem nenhum importador em `src/` e não conta.

**O escape, e ele é obrigatório:** a **nota datada**. Se o documento tem um
cabeçalho `NOTA DATADA` que menciona o símbolo, ele fica isento — é o mesmo
padrão que as regras 2 e 3 já usam para ADR, e pela mesma razão escrita lá:
*"um gate que castiga a honestidade é pior que gate nenhum"*. Uma sprint que
explica, com data, por que continua aberta apesar do símbolo de pé (o caso da
CARD-OCUPA-01, cuja E4 **é** o olho dela) está certa, não errada.

**A restrição de escopo, que não pode ser esquecida:** as regras 2 e 3 excluem
`docs/process/` de propósito — *"sprint é registro de proposta, e propor um
método que ainda não existe é o trabalho dela, não defeito"*. A regra 4 é a
**inversa** e só faz sentido dentro de `docs/process/sprints/`: ela não cobra
que o citado exista, cobra que o **rótulo** acompanhe o que já existe. Por isso
ela precisa de lista de prefixos própria, e não da `PREFIXOS_QUE_ENSINAM`.

**Custo estimado:** o portão já lê `src/` por AST para a regra 3
(`_handlers` de `daemon/ipc_server.py`). Contar chamadores é a mesma leitura,
alargada — nenhum mecanismo novo.

**Esta seção é PROPOSTA.** Nenhuma linha de `scripts/` foi tocada nesta rodada:
a rodada era de rótulos, e portão novo é decisão que pede a palavra dela.

## 6. O que foi remarcado em 09/08/2026

**Dezessete remarcadas** — a tabela abaixo. Mais **duas recontadas**: a
[A-NOITE-DOS-QUATRO-INVENTÁRIOS-01](2026-08-09-A-NOITE-DOS-QUATRO-INVENTARIOS-01-o-que-a-casa-sabe-e-o-que-o-produto-faz.md)
(três correções, entre elas o F-5, que **estava entregue** e a busca anterior não
achou por procurar a palavra errada) e a
[AGORA-E-DEPOIS-01](2026-08-08-AGORA-E-DEPOIS-01-o-plano-executavel-da-separacao-dos-dois-tempos.md)
(o passo 6 reconferido: continua aberto). E **uma conferida sem mudança**, a
[ESCONDER-EM-VEZ-DE-SAIR-01](2026-08-09-ESCONDER-EM-VEZ-DE-SAIR-01-o-duplicado-cura-pelo-outro-lado.md),
que já nasceu com o rótulo certo — foi dela que saiu metade da palavra.

Outras sprints foram remarcadas no mesmo dia por outra frente da leva
(MODO-01, AUTO-01, GATE-EMOJI-01, CONTAGEM-E-COOP-01, WRAPPER-EM-TODOS-01) e
não estão nesta tabela; o rótulo, medido depois, é o mesmo.

| sprint | rótulo novo |
|---|---|
| [ABAS-01](2026-07-25-ABAS-01-as-abas-brigam-pelo-mesmo-estado.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela |
| [MIC-USB-01](2026-07-25-MIC-USB-01-tres-mutes-empilhados.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela |
| [PLAYER-01](2026-07-25-PLAYER-01-um-numero-de-jogador.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela |
| [UI-SELETOR-01](2026-07-25-UI-SELETOR-01-ordem-dos-controles-no-seletor.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela (absorvida pela PLAYER-01) |
| [STATUS-SIMETRIA-01](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela |
| [SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md) | ENTREGUE EM CÓDIGO — aguardando a palavra dela (sprint inteira) |
| [BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) | PARCIAL — E2 entregue; E5 e E6 abertas |
| [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) | PARCIAL — E1, E3 e E9 entregues; E2 e E4 a E8 abertas |
| [EMULAÇÃO-NO-JOGO-01](2026-07-29-EMULACAO-NO-JOGO-01-o-r1-troca-de-app-em-vez-de-jogar.md) | PARCIAL — E1, E1(b) e E2 entregues; E3 e E5 abertas |
| [PERFIL-SALVA-TUDO-01](2026-07-29-PERFIL-SALVA-TUDO-01-salvei-todas-as-abas-e-so-parte-ficou.md) | PARCIAL — E3 entregue; E1, E2, E4, E5 e E6 abertas |
| [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md) | PARCIAL — a mecânica entregue; as dezenove palavras são escolha dela |
| [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | PARCIAL — E1 a E4 e E9 entregues; E5 a E8 abertas |
| [CARD-OCUPA-01](2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md) | PARCIAL — E1 a E3 entregues; **a E4 É a prova de tela dela** |
| [JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | PARCIAL — E1 a E4 entregues; E5 e E6 abertas |
| [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md) | PARCIAL — E10 entregue (portão); E1 a E9 abertas |
| [RADAR-01](2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md) | PARCIAL — E4 entregue (portão); E1 a E3 e o D1 abertos |
| [LIGHTBAR-BT-CULPADO-01](2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md) | PARCIAL — E1, E2 e E4 entregues; E3 aberta |

## 7. As que NÃO foram remarcadas — e a razão de cada uma

Estas foram conferidas e **continuam como estavam**. A razão importa mais que a
lista:

| sprint | por que continua aberta |
|---|---|
| [REGRA-NÃO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md) | **fiação faltante.** O código existe (`daemon/subsystems/external_mask.py:157`) e tem teste (`tests/unit/test_external_mask.py:34`, commit `7ffd205`), mas **nenhum arquivo de `src/` o importa**. É a ENTREGA-QUE-NÃO-LIGOU literal: escrito e desconectado |
| [TESTE-HONESTO-01](2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md) | os mesmos 17 arquivos continuam na lista de dívida (`tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py:52-68`). A E1 não foi paga |
| [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) | o interruptor existe (`app/widgets/controller_card.py:506`), mas o aceite é *"o medidor aparece por BT"* — e a [CONTROLE-INTEIRO-NO-RADIO-01](2026-08-07-CONTROLE-INTEIRO-NO-RADIO-01-o-mic-e-o-fone-que-nao-atravessam.md) ainda declara que o mic não atravessa o rádio |
| [BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md) | as citações no código descrevem a sprint como **pendente**, não como entrega |
| [SUÍTE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md) | idem |

**A régua que decidiu as cinco:** trabalho de **tela** ou de **hardware** que
ninguém mediu não é entregue — é escrito. E código sem chamador não é nem isso.
