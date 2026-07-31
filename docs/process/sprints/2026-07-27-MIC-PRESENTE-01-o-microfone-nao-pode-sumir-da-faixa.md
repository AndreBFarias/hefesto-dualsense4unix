# MIC-PRESENTE-01 — o microfone não pode sumir da faixa

- **Status:** **ENTREGUE** (conferido em 31/07: `MIC-PRESENTE-01` aparece **sete
  vezes** em `app/widgets/controller_card.py`; os dois `hide()` viraram estado
  apagado com o motivo em palavras, e a largura do bloco é reservada por campo
  fixo — `_MIC_ESTADO_CHARS`, `:369`)
- **Prioridade:** MÉDIA
- **Aberta em:** 27/07/2026, olhando a aba Status
- **Frase dela, literal:** *"na aba status falta a presença permanente do
  microfone (mesmo que não esteja funcionando no bt, mas o espaço do icon sempre
  fica lá)"*
- **Depende de:** [STATUS-SIMETRIA-01](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md),
  que está pondo o microfone à direita dos analógicos. Esta sprint cuida do que
  acontece com aquele espaço **quando não há sinal**

## O que foi medido

`app/widgets/controller_card.py` esconde a caixa do microfone em dois caminhos:

| Linha | Quando |
|---|---|
| `:1129` | o nível chega indisponível — `self._mic_box.hide()` |
| `:1313` | o controle desconecta ou o card é limpo |

Esconder um widget de uma faixa horizontal **muda a largura de todos os
vizinhos**. Então, além de o microfone desaparecer, os analógicos e o grid de
botões pulam de lugar quando ele some ou volta.

E ele some com frequência: por Bluetooth o microfone é Opus tunelado dentro do
HID, e a captura é instável — a `MIC-BT-01` existe justamente por causa disso.

## Por que a correção não é só "não esconder"

Deixar o medidor visível e mudo comunica a coisa errada: parece que o microfone
está aberto e em silêncio. São estados diferentes e a tela precisa distingui-los:

| Estado | O que a faixa mostra |
|---|---|
| Captando | o medidor com nível |
| Ligado, sem sinal | o espaço, o ícone e a informação de que não chega sinal |
| Sem suporte agora (rádio) | o espaço, o ícone apagado e o motivo |
| Controle desconectado | o espaço reservado, tudo apagado |

**O espaço é sempre o mesmo em todos os quatro.** É isso que ela pediu: o lugar
do ícone não se mexe.

## Entregas

### E1. O espaço do microfone é reservado, sempre

O bloco deixa de ser escondido. Nos casos em que hoje some, ele fica com a mesma
largura, com o ícone em estado apagado.

Implementação: trocar `hide()` por um estado visual apagado, ou — se algum
caminho precisar mesmo remover o conteúdo — usar `Gtk.SizeGroup` horizontal para
que o espaço permaneça reservado.

### E2. O estado é dito, não deduzido

Um rótulo curto ao lado do ícone: `Captando`, `Sem sinal`, `Desligado`. Nunca um
medidor mudo sem explicação.

### E3. Teste que morde

- Reprova se a largura da faixa mudar entre o estado "captando" e o estado "sem
  sinal": **a diferença tem de ser zero pixel.**
- Reprova se algum caminho ainda chamar `hide()` no bloco do microfone.

**A mordida:** devolver o `hide()` a qualquer um dos dois caminhos tem de fazer o
primeiro teste reprovar. Se não reprovar, o teste está medindo o widget e não a
faixa.

## Como você valida

1. Aba Status com o controle por Bluetooth: o microfone está lá, no lugar, mesmo
   sem sinal.
2. Falar no microfone: o medidor se mexe **sem nada mudar de lugar**.
3. Desconectar o controle: o espaço continua reservado, apagado.
4. Reconectar: nada pula.

## Registro de um pedido que já estava atendido

No mesmo momento ela pediu: *"as cores de lá do lightbar e botões pressionados
serem as mesmas cores do perfil aplicado na lightbar"*.

Medido: **já é assim.** `controller_card.py:1012-1045` lê a cor real
(`lightbar_rgb`) e propaga para os dois analógicos, para **todos** os glifos de
botão e para a barra do L2.

Nas capturas os glifos aparecem cinza porque **nada estava pressionado** — a cor
só aparece no toque.

Fica um ponto em aberto, e é dela a decisão: a cor passa por
`ensure_min_contrast` antes de ser usada, para continuar legível no fundo escuro.
Um azul muito escuro na barra acende num azul mais claro no card. É desvio
proposital; se ela quiser a cor **exata**, é uma linha — com o custo de que cores
escuras ficam difíceis de ver contra o fundo.
