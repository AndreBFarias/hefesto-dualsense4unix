# CONFIG-05 — orçamento como teto

**Depende de:** CONFIG-03. [D-A5 decidida](DECISOES-ABERTAS.md): espelhar com teto visível.

## Vocabulário: reusar, nunca renomear

Economia / Balanceado / Máximo / Auto. Não é preferência estética — é
compatibilidade de dados: `RumbleConfig.policy` já grava esses valores, e o
pydantic está com `extra="forbid"`. **Renomear quebra os perfis já gravados no
disco dela.**

## Teto, não troca

Escolher Economia não apaga nada. O jogo pede, a aba de origem manda, e o valor
chega ao controle limitado. Voltar para Balanceado devolve tudo.

## Dono único do valor efetivo

O orçamento **calcula**; a aba de origem **só exibe**. O slider da Lightbar
continua editável e ganha a linha ao lado: *"100 % · limitado a 25 % pelo
orçamento"*.

Isso é invariante de teste, não recomendação — espelhar estado entre abas foi a
classe de bug que a sprint `ABAS-01` curou.

## O que o orçamento NÃO promete

**Não existe medição de mA nem de horas de autonomia neste projeto.** O
multiplicador de rumble (0,3 / 1,0 / 1,5) é **força, não energia**, e o desconto
nunca foi convertido em minutos.

Então a tela **não diz "poupa bateria em X %"**. Diz o que faz: *"a vibração
chega ao controle com no máximo 40 % da força"*. Consequência verificável, não
promessa sem número.

> Nota: "poupar bateria" já é promessa feita na tela hoje, sem número por trás.
> Corrigir isso é sprint própria, não desta leva — mas a aba nova não pode
> aumentar a dívida.

## Auto

Controle no cabo joga em Máximo. Controle em rádio abaixo de 20 % de bateria cai
para Economia. A bateria já é lida e já aparece na aba Status.
