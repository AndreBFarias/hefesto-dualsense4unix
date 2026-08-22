# CONFIG-06 — controles que não são DualSense

**Depende de:** CONFIG-03.

> **Decisão registrada.** [D-A2](DECISOES-ABERTAS.md) foi respondida em
> 21/08/2026 pela manutenção da seção nesta leva — contra a recomendação, e com
> a decisão devidamente registrada. Esta sprint é escrita para essa escolha sair
> bem, não para revisitá-la.

## O que entrega

Um card por aparelho não-Sony conectado, com as declarações que o produto não
consegue deduzir sozinho:

| Declaração | Por que não dá para medir |
|---|---|
| Modo em que o controle foi ligado (XInput / DInput / Switch / macOS) | O modo é escolhido por chave física ou combo antes de conectar, e não é anunciado de forma confiável |
| Rótulo dos botões (Xbox A/B/X/Y ou Nintendo B/A/Y/X) | É preferência de quem joga, não propriedade do aparelho |
| Tratar aparelho não reconhecido como um modelo conhecido | Escape para clones e modelos fora da lista |
| **Cor do plástico, quando não foi lida** | O firmware entrega o código por cabo e por rádio, mas nem todo modelo responde — e nenhum controle não-Sony tem esse campo |

## A regra que mantém a seção honesta

**Onde a medição está pendente, o campo nasce em "não sei" e a tela diz que não
sabe.** Nada de valor default chutado — um default errado aqui é pior que campo
vazio, porque parece informação.

## As quatro medições — aceite desta sprint

Cada uma cabe em minutos, e nenhuma bloqueia a leva. Sem elas, a seção entrega
menos; com elas, entrega o que promete.

1. **O modelo do 8BitDo desta casa é SN30 Pro ou SN30 Pro+?** Decide qual índice
   de firmware vale e qual PID de X-input por rádio se aplica. Já está eliminado
   que seja um Pro 2 (que troca de modo por combo, não por chave física).
2. **Qual o default da Steam para `SteamController_SwitchSupport` quando a chave
   não existe?** Dela depende saber se a cura de Switch/8BitDo do produto já
   rodou alguma vez.
3. **Em modo D-input, o Hefesto vê o controle?** A previsão diz que não, com grau
   MÉDIO. Se não vir, a seção precisa do estado *"não estou vendo nada e sei por
   quê"* — que é entrega, não falha.
4. **Ao pintar a lightbar do 8BitDo em modo DS4, as quatro luzes do plástico
   acendem ou ignoram?** Cinco segundos de olho. Sem a resposta,
   `write_lightbar_slot` (`external_leds.py:338-361`) pode estar escrevendo num
   lugar que não chega a lugar nenhum.

## Rastro obrigatório

`external_controllers.py:11-14` guarda a fala que limitava o escopo:

> *"só uma aba pra ver como os controles aparecem, não uma super central"*

Essa linha **não sai**. Ganha uma nota datada logo abaixo, apontando para
[D-A2](DECISOES-ABERTAS.md), registrando que em 21/08/2026 o escopo foi
reaberto e por quem. É o padrão que o projeto já usa para decisão revogada:
NOTA DATADA dentro do próprio docstring, nunca apagar o que estava lá.

## O que continua fora

`EXTERNAL_PLAYER_LED_ENABLED` **não volta** nesta sprint. A docstring fixa a
condição de retorno (E3 da `LUGAR-À-MESA-01`, autorizada só depois da
`MÁSCARA-01`) e diz explicitamente que não é *"quando alguém achar que já dá"*.
Além disso, o defeito do `:blue:player-5` (LED HOME, escala 0-15) teria de ser
corrigido antes.

## A altura dos cards é invariante

Um 8BitDo pede dois campos que um DualSense não pede (modo e rótulo dos botões).
Isso não pode deixar os cards desencontrados na tela: **todos os cards têm a mesma
largura e a mesma altura**, e o seletor de jogador ancora no rodapé de cada um.

No GTK isso é `Gtk.Grid` com `row_homogeneous=True` mais um espaçador expansível
antes do último bloco. Não é detalhe estético — uma fileira de cards de alturas
diferentes lê como erro de montagem.

## Prova de trabalho

```bash
pytest tests/unit/ -k "external or mascara" -q
# com um 8BitDo e um Pro conectados, um card para cada, e "não sei" onde falta medição
```

**Aceite:** com nenhum controle externo conectado, a seção mostra estado vazio
explicativo em vez de sumir. Com um conectado e modelo desconhecido, aparece o
card genérico. As quatro medições estão respondidas ou registradas como
pendentes **na própria tela**, não só no documento.
