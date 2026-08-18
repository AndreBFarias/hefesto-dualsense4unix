# STATUS-SIMETRIA-01 — a aba que era pra mexer, e só ela

- **Status:** ABERTA
- **Prioridade:** PRIMEIRA DA FILA — não por gravidade, mas porque é a única
  coisa que ela autorizou, e a última coisa que aconteceu foi eu extrapolar
- **Aberta em:** 26/07/2026, depois do rollback para `restauro/inicio-da-sessao`
  (commit `4dd4652`, 25/07 22:36)

## O que ela pediu

> *"veja os elementos como analógicos, área do mic, os botões do dsx como
> triângulo x bola minúsculos, o desalinhamento dos analógicos, a área do mic
> que deveria ficar à direita dos analógicos. no caso era ali que era pra
> mexermos apenas."*

Quatro itens, uma aba, uma faixa de um card. E a frase final delimita o escopo
inteiro da sprint: **era ali que era pra mexermos apenas**.

## Por que esta sprint existe: a dívida do rollback

Ela pediu isso. A madrugada de 26/07 entregou outra coisa.

Medido no repositório, entre o ponto de restauro e o que a madrugada produziu:

```
git diff --stat 4dd4652 main
  60 arquivos alterados, 8902 inserções, 543 remoções
```

Quinze commits, entre eles PLAYER-LED-01, CONTAGEM-01, a faixa do microfone,
SLOT-JOGADOR-01, os botões ocupando o vão das abas, a simetria do instalador, o
conserto do `doctor --fix-mic` e o release v0.1.2. Nenhum deles foi pedido nesta
frase. E dois deles mexeram exatamente na área que ela nomeou, mas **na direção
oposta à que ela pediu**:

- `ef4b8bc` tirou o medidor de microfone do card e o mandou para o **rodapé da
  aba Status**, fora do scroll dos cards. Ela pediu o microfone **à direita dos
  analógicos**, dentro da faixa — não no rodapé.
- `b39fec9` mexeu no vão vertical da aba **Gatilhos**, que não estava no escopo.

O que ela relatou depois de olhar a tela, e que motivou o rollback:

1. *"interface tá quebrada e na hora do jogo tá um caos legal"*
2. *"agora na hora de jogar o jogo o perfil do controle muda e sai as configs que
   eu deixei"*
3. *"agora eu não sei quando é pra ativar entrada steam e quando não é. pensei
   que tivéssemos superado isso"*

As queixas 2 e 3 têm sprints próprias (PERFIL-FIRME-01 e STEAM-UMA-CHAVE-01) e
**não são desta**. Registro aqui porque o motivo de STATUS-SIMETRIA-01 vir
primeiro não é técnico: enquanto ela não sair, qualquer outra entrega parece de
novo eu decidindo sozinho o que é importante.

Esta sprint é o pagamento dessa dívida. Um arquivo, uma faixa, revertível
sozinha, conferível de olho em dois minutos, sem encostar em nada que rode
enquanto ela joga.

## Achado medido

Tudo abaixo foi medido no ramo restaurado `restauro/inicio-da-sessao`
(`4dd4652`), com a janela offscreen em 1900x1040 e a escala de fonte dela (3,
lida de `load_gui_prefs`). Card medido: 931x382. Faixa de baixo: largura 875.

### 1. Os dois analógicos ficam 20 px desalinhados na vertical

A causa não é o desenho — é o **rótulo**.

```
"Analógico Esquerdo (L3)"  ->  quebra em 3 linhas  (altura 60 px)
"Analógico Direito (R3)"   ->  quebra em 2 linhas  (altura 40 px)
```

Consequência medida, idêntica nos dois cards:

| elemento               | esquerdo | direito | degrau |
| ---------------------- | -------- | ------- | ------ |
| desenho do analógico   | y=245    | y=225   | 20 px  |
| rótulo X/Y             | y=319    | y=299   | 20 px  |
| altura da cápsula      | 180 px   | 160 px  | 20 px  |

Onde nasce:

- `src/hefesto_dualsense4unix/app/widgets/controller_card.py:818` —
  `label_titulo.set_line_wrap(True)`
- `:820` — `label_titulo.set_max_width_chars(_TITULO_STICK_MAX_CHARS)`
- `:115` — `_TITULO_STICK_MAX_CHARS: Final[int] = 10`
- `:851` e `:861` — os dois títulos, de tamanhos diferentes

E o ponto que decide a cura: **nada amarra as duas cápsulas pelo desenho**. Elas
só se alinham pelo topo do rótulo, então qualquer diferença de altura de rótulo
vira degrau no desenho.

### 2. Os botões do DSX têm 20x20 px e não crescem com a escala de fonte

Medido, glifo por glifo, na fileira de cima do grid:

```
cross    x=817  y=228  20x20
circle   x=839  y=228  20x20
square   x=861  y=228  20x20
triangle x=883  y=228  20x20
```

O grid 4x4 inteiro ocupa **86x86 px** dentro de um card de 931x382 — **9,2% da
largura do card** para os dezesseis botões.

Onde nasce: `controller_card.py:97` — `GLYPH_SIZE: Final[int] = 20`, passado em
`:882` (`ButtonGlyph(nome, size=GLYPH_SIZE, ...)`).

É **px cru, não CSS**. O A/B com escala de fonte 0 e escala 3 devolveu os mesmos
20x20 nos dois casos. Ou seja: aumentar a escala de fonte da interface, que é o
recurso que ela tem para enxergar melhor, **não tem efeito nenhum** sobre
triângulo, X, bola e quadrado.

### 3. O microfone está à esquerda dos analógicos — o oposto do pedido

Ordem horizontal real, medida dentro da faixa de baixo do card:

```
touchpad       x=28
lightbar       x=28   (y=273)
alto-falante   x=103  (y=273)
microfone      x=116  (73x86)
analógicos     x=203
botões 4x4     x=817
```

Onde nasce: o microfone é empacotado dentro da coluna "sensores" em
`controller_card.py:693` (`sensores.pack_start(self._montar_mic_e_touchpad(), ...)`),
e essa coluna inteira entra na faixa em `:699`, **antes** dos analógicos, que só
entram em `:701`. O módulo do microfone é montado em `:712-753`.

Registro de honestidade: **o microfone existe nesta árvore restaurada**, dentro
do card, à esquerda. O rollback não o apagou. O que a madrugada fez foi tirá-lo
do card e mandá-lo para o rodapé da aba — mais longe ainda do lugar pedido.

### 4. 448 px de vazio horizontal no meio do card

```
fim dos analógicos      x=369
início do grid 4x4      x=817
--------------------------------
vazio                   448 px, numa faixa de 875 de largura
```

Metade da faixa de baixo é buraco. Causa: os glifos são ancorados à direita
(`controller_card.py:706-708` — `glyphs.set_halign(Gtk.Align.END)` e
`linha.pack_end(glyphs, ...)`) e nenhum bloco entre eles expande.

Esses 448 px são exatamente a largura que falta para os analógicos e os botões
crescerem. Não é um quinto defeito — é o espaço que paga os três primeiros.

## Entregas

1. **Ordem nova da faixa de baixo do card**, com o microfone à direita dos
   analógicos:

   ```
   [ Touchpad / Lightbar / Alto-falante | Analógico Esquerdo | Analógico Direito | Microfone | botões 4x4 ]
   ```

   O microfone continua **dentro do card**, na faixa, não no rodapé da aba.

2. **Os dois analógicos alinhados pelo DESENHO**, com um `Gtk.SizeGroup`
   vertical amarrando as duas linhas de título. Encurtar o texto do rótulo é
   cinto de segurança, não é a cura: se amanhã alguém trocar uma palavra do
   rótulo, o degrau volta. O SizeGroup é a cura, porque o alinhamento passa a
   não depender do texto.

3. **Botões do DSX maiores e crescendo junto com a escala de fonte.**
   `GLYPH_SIZE` deixa de ser px cru: o tamanho passa a sair da escala que ela
   controla, e o grid ocupa parte dos 448 px que hoje são vazio. Alvo declarado:
   ler triângulo, X e bola a um braço de distância, sem aproximar o rosto da
   tela.

4. **Os 448 px do meio do card deixam de ser buraco** — a largura recuperada vai
   para os analógicos e para o grid de botões, dentro do mesmo card, sem alargar
   o card nem criar rolagem horizontal na aba Status.

5. **Um teste que morde.** Reprova se:
   - o Y do desenho do analógico esquerdo diferir do Y do direito em 1 px que
     seja;
   - a ordem horizontal da faixa não for a da entrega 1 (microfone depois dos
     dois analógicos);
   - o glifo não crescer quando a escala de fonte muda (A/B com escala 0 e 3).

   E a regra da casa: **arrancar o `Gtk.SizeGroup` tem de fazer o teste falhar.**
   O precedente do rumble — teste que passou com a cura arrancada, porque
   chamava a peça e não a fiação — não pode repetir aqui. O teste tem de exercer
   o layout montado, não a constante.

6. **Escopo trancado.** Ver a seção seguinte.

## O que NÃO deve ser tocado nesta sprint

Isto é entrega, não recomendação. Se alguma destas coisas mudar, a sprint
extrapolou e **reprova mesmo que os quatro itens acima estejam certos**.

- **Nenhuma aba além de Status.** Início, Emulação, Gatilhos, Perfis, Rumble e
  Sistema ficam byte a byte como estão.
- **Nada fora da faixa de baixo do card.** O cabeçalho do card, os selos de
  conexão, os contadores e o rodapé da janela ficam como estão.
- **Nenhuma faixa nova no rodapé da aba Status.** Foi o que a madrugada fez com
  o microfone, e é o oposto do pedido.
- **Os 307 px de vazio vertical abaixo dos cards** (medidos: conteúdo termina em
  y=738, a página vai até y=1045) ficam onde estão. Irritam de verdade, e são
  assunto de outra conversa — depois que ela aprovar esta.
- **Os 618 px de vão da aba Gatilhos** (`gui/main.glade:503-513`, scroller com
  `vexpand=True`) ficam onde estão. Foi o alvo de `b39fec9`, e não é daqui.
- **Nada do daemon.** Nenhum arquivo em `daemon/`, `profiles/`, `integrations/`.
  Esta sprint não pode ter como falhar durante uma partida, e a garantia disso é
  não encostar no que roda durante a partida.
- **Nada de contagem de controles, número de jogador, LED de jogador, máscara de
  emulação ou Steam Input.** Cada um tem sprint própria e volta pela porta certa.
- **Nenhum release.** Esta leva não publica versão.
- **Um arquivo.** O alvo é
  `src/hefesto_dualsense4unix/app/widgets/controller_card.py`, mais os testes em
  `tests/unit/test_status_cards.py` e
  `tests/unit/test_status_cards_sensores.py`. Qualquer arquivo além destes é
  sinal de que o escopo vazou.

## Como validar

Tudo de olho, na janela, sem terminal e sem log.

1. Abrir o Hefesto na aba **Status**, com um controle conectado.
2. **Os dois analógicos na mesma altura.** Os dois círculos alinhados, sem
   degrau. Os dois rótulos X/Y também na mesma linha.
3. **O microfone à direita dos dois analógicos**, dentro do card — não no rodapé
   da aba, não à esquerda.
4. **Ler triângulo, X, bola e quadrado a um braço de distância da tela**, sem
   inclinar o corpo.
5. **Aumentar a escala de fonte** nas preferências e ver os botões do DSX
   crescerem junto. Diminuir e ver encolherem.
6. **O meio do card não é mais um buraco** — os elementos ocupam a faixa, em vez
   de se espremerem nas duas pontas.
7. Repetir com **dois controles** conectados: os dois cards têm de se comportar
   igual, sem degrau em nenhum dos dois.
8. **Abrir Início, Emulação, Gatilhos, Perfis, Rumble e Sistema.** Se alguma
   coisa mudou de lugar em qualquer uma delas, a sprint extrapolou e **reprova**.
9. Fechar e reabrir a janela: nada volta a desalinhar.

**Critério que resume:** a aba Status entrega exatamente os quatro itens que ela
nomeou, e nenhuma outra tela do Hefesto muda um pixel.

## O que NÃO foi medido

- **Nada foi medido com o controle em uso, com os analógicos se mexendo.** As
  medições são de layout com a janela parada. Se o desenho do analógico mudar de
  tamanho quando o stick se move, o alinhamento pode voltar a divergir — não
  verifiquei.
- **Não medi o card com três ou quatro controles.** Com quatro, os cards vão
  para grade 2x2 e o modo `_compact` troca `STICK_SIZE_SINGLE` (88 px) por
  `STICK_SIZE_COMPACT` (70 px). O degrau de 20 px foi medido no caminho de um e
  de dois cards; presumo que valha nos quatro, porque a causa é o rótulo e não o
  desenho, mas **presumir não é medir**.
- **Não medi qual tamanho de glifo é "grande o suficiente" para ela.** A entrega
  3 diz "cresce com a escala de fonte" e "legível a um braço de distância"; o
  número final é decisão dela, olhando a tela, não minha.
- **Não medi se aumentar os glifos faz o card estourar a faixa que o
  `status_players_scroll` dá.** Existe teste na casa que tranca isso
  (`test_card_de_controle_cabe_na_faixa_que_a_aba_status_da` e
  `test_card_de_um_controle_so_tambem_cabe_na_faixa`, citados em
  `controller_card.py:99-108`), e é ele que manda no teto — mas o A/B com o
  glifo maior ainda não foi rodado.
- **Não rodei nada nesta árvore.** A árvore em
  `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix` é a que o Hefesto
  instalado executa; foi só lida.
