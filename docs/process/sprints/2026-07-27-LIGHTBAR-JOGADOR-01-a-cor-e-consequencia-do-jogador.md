# LIGHTBAR-JOGADOR-01 — a cor é consequência do jogador, não uma escolha à parte

- **Status:** ABERTA
- **Prioridade:** ALTA — é queixa direta dela, olhando a tela
- **Aberta em:** 27/07/2026, com a janela aberta na aba Lightbar
- **Frase dela, literal:** *"na lightbar eu preferia o modo anterior que era pra
  escolher o player daquele controle e não essas cores que não fazem sentido. área
  de desenho das 5 luzes é meio nonsense."*
- **Regra da casa que isto aplica:** **R-C — um nome, um conceito**

## O que ela pediu, e por que o código concorda com ela

A aba oferece **três superfícies diferentes para dizer a mesma coisa**: qual
jogador é este controle.

| Superfície | Onde | O que faz |
|---|---|---|
| Seletor de cor RGB | coluna esquerda, protagonista | escolhe uma cor arbitrária |
| `Cores automáticas por controle` | caixa de marcar logo acima | liga a derivação correta: cor = função(jogador) |
| `Desenho das 5 luzes`, com `Desenho do P1..P4` | coluna direita inteira | o número do jogador, dito de novo, com outro nome |

E o código já tem a resposta certa: `core/led_control.py:158`,
`player_slot_color(slot)`, com a paleta canônica

```
1 = azul     2 = vermelho     3 = verde     4 = rosa
```

Ou seja: **a cor já é consequência do jogador.** O que a interface fez foi
promover a exceção (cor livre) a protagonista e esconder a regra (jogador) numa
caixa de marcar — e depois oferecer o jogador de novo, do outro lado da tela,
chamado de "desenho".

Ela não está pedindo uma feature. Está pedindo que a tela mostre o que o código
já faz.

## A prova de que a superfície atual mente

Medido na captura de 27/07, 21:24, com um controle conectado:

- a aba **Status** diz `Lightbar: #0000ff` — azul, que é a cor canônica do
  jogador 1;
- a aba **Lightbar**, ao mesmo tempo, mostra **laranja** no seletor e na prévia.

Duas telas do mesmo programa discordando sobre o mesmo estado, no mesmo instante.
É exatamente a pergunta 6 da folha da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
*"está tudo dizendo a verdade ao mesmo tempo?"*

O laranja é rascunho não aplicado. Nada na tela diz isso — e é a mesma classe de
defeito que a `BOTÃO-QUE-NÃO-MENTE-01` chama de **adiamento silencioso**.

## A causa da dessincronia, medida — e ela é de projeto

`app/actions/lightbar_actions.py:294`, `_refresh_lightbar_from_draft`. A
docstring diz, com todas as letras, na linha 299:

> *"exibe os LEDs EFETIVOS do alvo de edição atual [...] lido do PERFIL, **não do
> backend**"*

Ou seja: **a aba Lightbar mostra o rascunho do perfil; a aba Status mostra o que
está aceso.** As duas estão certas sobre coisas diferentes, e nenhuma diz qual é
qual.

O veredito dela, e ele procede: *"ele não deveria mostrar a que tá aplicada? Pq
não faz sentido."*

A defesa do desenho atual é que a aba é um **editor de perfil**. É internamente
coerente — e não sobrevive ao que está escrito na própria tela:

| O que a tela diz | O que ela sugere |
|---|---|
| título `Lightbar (barra de LED)` | controle do hardware |
| `Escolha a cor da barra de LED do DualSense` | controle do hardware |
| o campo chamado **Prévia** | isto é o que está valendo |
| botão `Aplicar no controle` | (único sinal de que não está aplicado) |

Três sinais dizem "hardware" e um sinal, por dedução, diz "rascunho".

**Decisão desta sprint:** o padrão passa a ser mostrar **o que está aplicado**. O
modo editor-de-perfil é o caso especial, e é ele que tem de se anunciar.

### E0. A aba parte do que está aceso

Ao abrir, o seletor e a prévia mostram a cor **real** do controle
(`lightbar_rgb`, a mesma fonte que a aba Status já usa). Se o perfil em edição
divergir do que está aceso, a tela mostra as duas, nomeadas:

```
Aceso agora:  azul (jogador 1)
Neste perfil: laranja  -- ainda não aplicado
```

Enquanto as duas divergirem, o rótulo `Prévia` não pode ser usado para o valor
não aplicado: prévia de algo que já está valendo em outro lugar é a origem da
confusão.

## Entregas

### E1. O jogador vira o protagonista da aba

No lugar do seletor de cor cru, um seletor de **jogador** para este controle,
com a cor canônica desenhada em cada opção:

```
Este controle é o:   [ 1 azul ]  [ 2 vermelho ]  [ 3 verde ]  [ 4 rosa ]
```

Escolher o jogador define, de uma vez: a cor da barra **e** o desenho das cinco
luzes. Um gesto, um conceito.

**Cuidado duro, e ele não é negociável:** este seletor tem de escrever no **mesmo
`player_slot`** que a aba Início já usa em `Renumerar agora`. Se criar um quarto
lugar que diz o número do jogador, esta sprint terá feito exatamente o que veio
consertar. Antes de escrever qualquer linha, medir onde o `player_slot` é
gravado e reutilizar esse caminho.

### E2. Cor livre deixa de ser o caminho principal

Continua existindo — ela não pediu para tirar, e há quem queira. Mas vai para
trás de uma opção explícita, do tipo `usar outra cor neste controle`, e a tela
diz o que se perde ao escolher isso: a cor deixa de acompanhar o número do
jogador.

### E3. "Desenho das 5 luzes" some como painel próprio

Ela chamou de nonsense e a medição concorda: os quatro botões `Desenho do P1..P4`
são o número do jogador com outro nome, e o `Aplicar o desenho` ao lado é um
clique redundante — os presets **já enviam por IPC** (`lightbar_actions.py:822`),
então aquele botão só reenvia o que já aconteceu, ensinando que o clique anterior
não bastou.

O que **fica**, porque tem uso real e não é o número do jogador:

- `Todas acesas` e `Todas apagadas`;
- a explicação de que, com co-op ligado, quem manda no desenho é o co-op.

### E4. A prévia para de mentir

Enquanto houver rascunho não aplicado, a tela diz. Some com o silêncio das duas
pontas: ou aplica ao soltar (é o que a `BOTÃO-QUE-NÃO-MENTE-01` está fazendo com
cor e brilho), ou marca como pendente com o botão que completa ao lado.

### E5. Teste que morde

- Escolher o jogador N tem de produzir **a cor canônica de N** — arrancar a
  ligação com `player_slot_color` tem de reprovar.
- A aba Lightbar e a aba Status têm de reportar **a mesma cor** para o mesmo
  controle. Este teste, escrito hoje contra o estado atual, **reprova** — e essa
  reprovação é a prova de que ele morde.
- Não pode existir mais de uma superfície que grave `player_slot`.

## Como você valida

De olho, sem terminal:

1. Aba Lightbar: escolher `jogador 2` e o controle **fica vermelho na hora**.
2. As cinco luzes do controle mudam junto, sem segundo clique.
3. Abrir a aba Status: a cor mostrada é a mesma. **Sem discordância entre as duas
   telas.**
4. Abrir a aba Início: o número do jogador lá é o mesmo. Um número, um lugar.
5. Escolher `usar outra cor`, pegar um roxo: funciona, e a tela avisa que a cor
   parou de acompanhar o jogador.
6. Reconectar o controle: a cor volta certa sozinha.

## O que esta sprint NÃO resolve

- **Não muda a ordem dos controles.** Qual controle é o jogador 1 na hora de
  ligar é assunto da numeração, que tem sprint própria e duas âncoras distintas
  (`player_slot` da fila de preferência contra o índice cru do co-op). Aqui só se
  escolhe, à mão, quem é quem.
- **Não mexe no co-op.** Com o co-op ligado, quem manda no desenho continua sendo
  ele — a tela já diz isso e continua dizendo.
- **Não foi medido** se existe perfil salvo dela com cor livre gravada. Se
  existir, ele tem de continuar valendo depois desta sprint — migração silenciosa
  de perfil é a classe de defeito que causou o rollback de 26/07.
