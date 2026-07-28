# PROVA-DE-TELA-01 — dez minutos de olho antes de qualquer leva

- **Status:** ABERTA
- **Prioridade:** ALTA
- **Aberta em:** 27/07/2026. Existia desde 26/07 **só como seção de índice**, sem
  documento — e a regra nascida do rollback diz que sprint sem documento não entra
  em código. Este arquivo paga essa dívida
- **Natureza:** portão **humano**. Não é teste, não é gate de CI, e não substitui
  nenhum dos dois
- **Par obrigatório de** [PORTÃO-VIVO-01](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md)

## Por que um portão humano, se estamos construindo dez automáticos

Porque nenhum dos dez teria pego o que quebrou.

A leva revertida de 26/07, medida agora contra o ponto de restauro
(`git diff --shortstat 4dd4652 main`):

```
79 arquivos alterados, 10795 insercoes, 549 remocoes
```

Suíte verde. `mypy --strict` limpo. Quatro gates lidos. **E reprovada em dois
minutos de olho**, com três frases:

1. *"interface tá quebrada e na hora do jogo tá um caos legal"*
2. *"agora na hora de jogar o jogo o perfil do controle muda e sai as configs que
   eu deixei"*
3. *"agora eu não sei quando é pra ativar entrada Steam e quando não é. Pensei que
   tivéssemos superado isso"*

Cada mudança daquela leva era defensável isoladamente. O que reprovou foi o
**conjunto**, e conjunto não tem asserção. Automação pega regressão mecânica; não
pega *"isso ficou pior"*.

## A folha

Seis perguntas. Toda leva que toca a janela responde as seis, com a janela
maximizada, **antes** do commit. Resposta é sim ou não — não há "mais ou menos".

| # | Pergunta | Reprova quando |
|---|---|---|
| 1 | **Abri as nove abas, uma por uma?** | qualquer aba não foi aberta |
| 2 | **Alguma coisa mudou de lugar numa aba que a sprint não nomeia?** | mudou |
| 3 | **O que eu pedi está onde eu pedi?** | está em outro lugar, mesmo que melhor |
| 4 | **Dá para ler os rótulos e acertar os botões sem mirar?** | algum texto corta, ou algum alvo exige pontaria |
| 5 | **A mesma coisa tem o mesmo nome e o mesmo número em toda a janela?** | dois nomes para um conceito, ou dois números para uma contagem |
| 6 | **Está tudo dizendo a verdade ao mesmo tempo?** | duas frases sobre o mesmo estado discordam na mesma tela |

A pergunta 6 não é abstrata. Nas capturas de 26/07, a janela dizia
**"Controle Desconectado"** em vermelho enquanto dois cards abaixo mostravam
bateria de 67% e 74%; e dizia **"Lightbar: apagada"** a 20 px de uma barra
colorida mostrando a cor.

## O procedimento

1. **Antes de escrever código:** print de cada aba que a sprint declara tocar.
2. **Depois:** print das **mesmas** abas, mais as **outras**, para responder a
   pergunta 2.
3. Os dois conjuntos vão para `docs/process/estudos/assets/<data>-<sprint>/` e
   são citados no commit.
4. A folha respondida entra no documento da sprint, não em mensagem de commit.

Os prints são da **janela real, maximizada, com controle conectado** — não de
render offscreen. Render offscreen serve para medir geometria; não serve para
responder *"ficou pior?"*, porque não tem os dados vivos que produzem a maior
parte dos defeitos de contradição.

## O limite de tamanho, que é a parte que ninguém gosta

Uma leva que muda 79 arquivos **não é validável de olho**. A folha é necessária e
insuficiente se o pedaço for grande demais para caber na cabeça de quem olha.

Regra proposta, e é dela a palavra final sobre o número: **uma leva que toca a
janela vai até uma aba por vez.** Se a sprint precisa de duas, são duas sprints.

Não é sobre disciplina de commit. É que a pergunta 2 — *"mudou de lugar algo que
a sprint não nomeia?"* — **só é respondível se a sprint nomear pouca coisa**.

## Prova de que esta folha morde

O teste é retroativo e não custa código nenhum:

> **Aplicar as seis perguntas à leva revertida de 26/07. Ela tem de reprovar.**

Pela leitura das três frases dela, a leva reprova em pelo menos 2, 3 e 6. Se
alguém aplicar a folha àquela leva e ela **passar**, a folha está errada e precisa
de mais perguntas — não a leva.

Segunda prova, para a folha não virar carimbo: **uma leva que passa nas seis e
mesmo assim é reprovada por ela ao olhar obriga a acrescentar a pergunta que
faltava**, no mesmo dia, neste arquivo. A folha é viva; o registro de cada
acréscimo fica aqui com a data e o motivo.

## O que esta sprint NÃO resolve

- **Continua sendo uma máquina só.** O checklist de hardware tem 43 caixas e
  quase nenhuma marcada. Esta folha cobre a janela, não o hardware.
- **Não substitui os testes de layout.** Alinhamento em pixel e escala de fonte
  são para asserção, não para olho — e é justamente por isso que a
  STATUS-SIMETRIA-01 pede teste que reprova quando a cura é arrancada.
- **Não protege o que não é visível.** Perfil que troca sozinho no meio da
  partida não aparece em print nenhum. Para isso existe a validação de partida,
  que é outra coisa e mora nas sprints de perfil.
- **Depende de ela olhar.** É o portão mais forte que este projeto tem e o único
  que não posso rodar sozinho. Registrar isso é honestidade, não desculpa.
