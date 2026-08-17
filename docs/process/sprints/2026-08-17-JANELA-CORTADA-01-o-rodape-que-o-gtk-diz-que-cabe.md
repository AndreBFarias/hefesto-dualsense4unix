# JANELA-CORTADA-01 — o rodapé que o GTK diz que cabe

**17/08/2026, 02h44.** Ela fotografou a janela e marcou três coisas. Uma foi
resolvida na hora; **duas ficam aqui, porque medir o layout no GTK disse que
está tudo certo — e a tela dela diz que não.**

Este sprint existe para que a próxima pessoa não repita a medição que eu já fiz
e não conclua nada a partir dela.

---

## O que ela marcou na foto

| # | o que ela escreveu | estado |
|---|---|---|
| 1 | *"remover guia dos status em tempo real"* | **feito** — commit `0153e9d` |
| 2 | (retângulo azul em volta de **"Saída muda"**) | **aberto**, mas com a porta achada — ver §CAUSA/item 2 |
| 3 | *"altura e largura dos botões, em todas as abas, ficam quebrados e não aparecem corretamente em qualquer resolução que seja. nem com tela maximizada"* | **CURADO** em 17/08 — ver §CAUSA/item 3 |

O retângulo verde grande, no rodapé da foto, cerca a faixa em que os quatro
botões (Aplicar / Salvar Perfil / Importar / Restaurar Default) aparecem
**cortados ao meio**, junto com a statusbar.

---

## §CAUSA — o que foi achado em 17/08, e como

**As hipóteses da §HIPÓTESES abaixo continuam escritas como estavam.** A H2 foi
confirmada com uma correção; a H1 não precisou ser testada; a H3 caiu.

### Os dois cegos que faziam o defeito parecer invisível

**1. Nenhuma foto desta casa jamais mostrou o rodapé.** O `main` do
`retratar_abas.py` arranca o `main_notebook` do `root_box` e fotografa pelo
notebook (`scripts/gui-captura/retratar_abas.py:1058-1060`). O cabeçalho tinha
o mesmo problema e ganhou o `_fotografar_o_cabecalho` em 14/08; **o rodapé
continuou fora de todas as dez imagens**, e é justamente a região que ela
marcou. Procurar o defeito nas fotos era impossível por construção.

**2. `set_size_request()` funciona na `OffscreenWindow`; `resize()` é que não.**
A §MEDIÇÃO concluiu "não conclua a partir da OffscreenWindow, ela não
redimensiona" a partir de tentativas com `resize()`. Mas o próprio
`retratar_abas.py` usa `set_size_request(1920, 1080)` e as fotos saem nesse
tamanho. **A OffscreenWindow serve** — e serve ainda melhor com
`size_allocate()`, que força a alocação diretamente e é o que fechou o caso.

### Item 3 — CURADO: o miolo não cedia, e o rodapé saía pela borda

Forçando a alocação da raiz (`root_box.size_allocate`), com o card na tela:

| altura da janela | header | notebook | rodapé | veredito |
|---|---|---|---|---|
| 560 (o `height-request`) | 73 | 697 | 52 | **FORA por 262px** |
| 650 | 73 | 697 | 52 | **FORA por 172px** |
| 750 | 73 | 697 | 52 | **FORA por 72px** |
| 822 (o mínimo real) | 73 | 697 | 52 | inteiro |
| 830, 900, 1080 | 73 | 705/775/955 | 52 | inteiro |

**É a H2, com uma correção que muda a cura:** o rodapé **não** é esmagado a
zero. O `main_notebook` trava no mínimo dele (697px) e **empurra o rodapé para
fora da borda de baixo, inteiro, com os 52px dele**. Daí o sintoma ser "cortado
ao meio" e não "sumiu" — e daí a cura ser "fazer o miolo ceder", não "dar altura
ao rodapé", que ele já tinha.

**E o glade autorizava.** `height-request = 560` numa janela cujo conteúdo pedia
822: ninguém mentiu para o GTK. Isso explica o *"em qualquer resolução"* — não
depende da tela, depende da altura da JANELA, e qualquer valor abaixo de 822
cortava.

**Por que a §MEDIÇÃO viu 743 e não 822:** ela mediu **só o notebook**, pela
mesma razão do cego nº 1. Os 73px do cabeçalho e os 52px do rodapé ficaram fora
da conta.

**A cura, decidida por ela (17/08), foi dupla:**

1. cada página do notebook virou um `GtkScrolledWindow` (`scroll_tab_*`), com
   `propagate-natural-height` — sem essa propriedade as dez fotos da
   documentação sairiam cortadas, porque o `retratar_abas.py` estica cada aba
   pela altura NATURAL dela;
2. `height-request` de 560 → **620**, um piso honesto agora que o miolo cede: a
   janela não corta mais em altura nenhuma, e este número existe só para ela não
   nascer num tamanho inútil.

Medido depois: rodapé inteiro em 560, 620, 650, 750, 822, 830 e 1080; o miolo
acompanha (435 → 955); **nenhuma aba rola na janela de abertura** (a mais alta,
Emulação, pede 646px e tem 705); e as dez fotos saíram idênticas em dimensão e
peso.

**Portão:** `tests/unit/test_janela_cortada_01_o_rodape_nao_sai_pela_borda.py`,
4 testes. Ele mede ALOCAÇÃO, não tamanho preferido, e cobre alturas abaixo do
mínimo do conteúdo — que é o regime em que o defeito vivia. Morde: desligados os
scrollers, reprova em 560/620/650 nomeando quantos pixels o rodapé ficou fora.

**E um portão que a própria cura quase deixou cego.** Com as páginas dentro de
scrollers, `notebook.get_nth_page(i)` passou a devolver o scroller — cujo mínimo
é pequeno de propósito. O `test_layout_orcamento_altura.py` continuou verde com
uma aba engordada em 900px. Corrigido descendo ao conteúdo (`_conteudo_da_pagina`)
e mantendo o cromo como subtração entre grandezas comparáveis; agora reprova com
`Rumble (932px)` acima do teto de 654px. **A cura criou o portão cego e quase o
entregou junto** — é o defeito que o `O-QUE-FICOU-ABERTO-01` chama de mais caro.

### Item 2 — a porta foi achada; o defeito de layout, NÃO

**A pergunta que a §HIPÓTESES deixou** (*"a condição que revela o selo está em
`_update_speaker`, e descobri-la é parte da tarefa"*) tem resposta, e ela
explica por que a bancada falhou:

    speaker={"muted": True}          -> saida_muda_do_entry = None   (selo apagado)
    speaker={"saida_muda": True}     -> saida_muda_do_entry = True   (selo ACESO)

`muted` é a **camada 2** (o registrador HID); o selo lê a **camada 1** (o sink do
PipeWire). Chaves diferentes, camadas diferentes. A docstring de
`saida_muda_do_entry` afirmava que *"hoje nenhuma das duas fontes existe"*
(medido em 01/08) e **isso caducou sem que ninguém percebesse**: o `MicMonitor`
ganhou a thread supervisora do sink (`app/mic_monitor.py:461`, `:622`, `:510`) e
a `LeituraMic` passou a carregar o campo. A docstring foi substituída.

**O que eu NÃO consegui provar, e por isso não entreguei cura:** montei o card
fora da aba para medir se o selo escapa do bloco, e a bancada não é fiel — o
card pedia 1064–1145px de largura mínima onde o projeto o limita a 590, e o selo
aparecia com alocação `x=-1 y=-1 1x1` (a assinatura de widget que nunca recebeu
`size_allocate` de verdade), **aceso ou apagado**. Cheguei a escrever um
`set_hexpand(True)` no selo e a reverti: não havia medição que a sustentasse.

**O que falta, e agora é barato:** medir o selo aceso **dentro da aba Status
montada**, pelo caminho do `retratar_abas.py`, com o card no limite de 590px —
e não num `OffscreenWindow` avulso. A chave para acendê-lo está acima.

---

## O QUE JÁ FOI MEDIDO — e por que não conclui

Tudo abaixo foi medido em `Gtk.OffscreenWindow` (a `Gtk.Window` fica 1x1 sem
gerenciador de janelas — armadilha nº 2 do `COMO-OLHAR-A-TELA.md`).

### A geometria está SÃ

```
footer_box           h_min= 36  h_nat= 36  | alocado y=715  h=36
footer_buttons_box   h_min= 34  h_nat= 34  | alocado y=716  h=34
btn_footer_apply     h_min= 34  h_nat= 34  | alocado y=716  h=34
status_bar           h_min= 36  h_nat= 36  | alocado y=721  h=24

raiz alocada: 1180 x 751
altura MÍNIMA do conteúdo: 743px   —   a janela abre com 830px
```

**O rodapé cabe, com 87px de folga.** `y + altura = 751`, exatamente o fim da
raiz. Nenhum widget pede mais do que há.

### O que isso elimina

- **não** é `default-height` pequeno demais (830 > 743);
- **não** é o `footer_box` sem altura (36px, alocado);
- **não** é o `GtkFlowBox` que já derrubou três dos quatro botões uma vez
  (`FIX-GUI-COSMIC-REMEDIATION-01`) — hoje é `GtkBox` e os quatro têm alocação;
- **não** é escala de fonte: `text-scaling-factor = 1.0`, sem `escala_fonte`
  gravada no `gui_preferences.json`, tela 1920x1080.

### O que NÃO foi medido, e é o que falta

**A janela REAL na tela dela.** Duas tentativas falharam e as duas por motivo
declarado:

1. `OffscreenWindow.resize()` **não redimensiona** — a raiz ficou em 1180x751
   nos cinco tamanhos testados (1180x830, 1920x1040, 1920x780, 1280x720,
   1180x743). O teste que eu quis fazer não mediu o que eu quis medir;
2. abrir a janela de verdade jogaria ela na tela dela, e a casa proíbe
   (`CLAUDE.md`: nunca uma janela na frente dela). Além disso a janela não
   estava aberta na hora.

**Conclusão honesta: o corte não vem do layout que o GTK calcula.** Vem de algo
que só aparece na janela real.

---

## AS HIPÓTESES, e como cada uma cai

Nenhuma foi testada. Estão em ordem de quanto explicariam a frase *"nem com tela
maximizada"* — que é a parte mais estranha do relato, porque maximizado sobra
espaço.

### H1 — o compositor do COSMIC corta a janela

**Por que é a primeira:** explica "em qualquer resolução" e "nem maximizada". Se
o COSMIC entrega uma área de cliente menor do que a janela pensa ter, o rodapé
sai pela borda sem que o GTK saiba.

**Como cai:** com a janela aberta, comparar o que o GTK acha
(`window.get_allocation()`) com o que o compositor deu
(`window.get_window().get_geometry()`). Se divergirem, é H1.

### H2 — o conteúdo cresce e empurra, e o rodapé não é o último a ceder

**Por que:** o `footer_box` entra com `expand=False`, o que lhe dá o natural —
mas num `GtkBox` vertical, se um irmão acima expande sem teto, o filho sem
expansão pode ser espremido a zero em vez de forçar rolagem.

**Como cai:** com a janela aberta e um card na tela, ler a alocação do
`footer_box` e do irmão de cima. Se o de cima passar do que a raiz tem, é H2 — e
a cura é dar ao rodapé `valign=END` num overlay, ou pôr o miolo num
`GtkScrolledWindow` que ceda antes.

### H3 — o "Saída muda" e os botões são o MESMO defeito

**Por que:** o selo escapa do bloco do alto-falante na foto, exatamente como o
rodapé escapa da janela. Os dois são filhos sem expansão de caixas verticais.

**Como cai:** se a cura de H2 consertar o selo junto, era um só. Se não,
são dois.

**Nota:** eu não consegui reproduzir o selo visível em bancada — montei um card
com `speaker={"volume":255,"muted":True,"rota":3}` e ele continuou escondido. A
condição que o revela está em `_update_speaker`, e descobri-la é parte da
tarefa.

---

## O ENSAIO QUE RESOLVE, e ele é curto

Precisa da janela ABERTA, e portanto do olho dela (PROVA-DE-TELA-01):

1. ela abre o Hefesto e deixa como está;
2. medir, de fora, sem tocar na janela:
   - `get_allocation()` da raiz **contra** `get_window().get_geometry()`;
   - a alocação do `footer_box` (`y`, `height`) contra a altura da raiz;
   - o mesmo para o irmão imediatamente acima do rodapé;
3. se `y + height > altura da raiz`, o rodapé está fora — e o número diz por
   quantos pixels;
4. repetir com a janela **maximizada**, que é o caso que ela diz que também
   falha.

**Um ensaio, um gesto:** ela só abre a janela. Nada de "redimensione enquanto eu
meço" — isso mistura duas variáveis e já produziu dado ruim ontem.

---

## O QUE NÃO FAZER

- **Não afrouxe os limites de largura** (1180px de janela, 590px de card). Eles
  são o projeto, e existem porque dois cards lado a lado somam direto no mínimo
  da janela. Ontem eu quase os estourei acrescentando um controle deslizante sem
  tirar nada, e o portão `test_a_coluna_do_som_nao_e_a_mais_alta_da_faixa`
  reprovou na hora — estava certo.
- **Não conclua a partir da OffscreenWindow.** Ela não redimensiona, e usar o
  número dela para afirmar coisa sobre a janela real é o erro de método que este
  documento existe para evitar.
- **Não mexa nos quatro botões separadamente.** Se três abas têm o mesmo
  sintoma, a causa é do contêiner, não de cada botão.

---

## PARA A GUI, quando a causa aparecer

Regra dela de 09/08: **a cura chega na interface e no install**. Aqui a cura é
na interface, e o portão que ela pede é um teste de alocação — não de tamanho
preferido:

> reprovar se, com a janela no tamanho de abertura E maximizada, a soma
> `footer_box.y + footer_box.height` passar da altura alocada da raiz.

O teste de HOJE mede `get_preferred_height`, que é o que o widget **pede**. O
defeito está no que ele **recebe**. É a mesma distinção que separou "o daemon
tem o fd" de "o daemon recebe eventos" ontem, e é onde a bancada inteira quase
se perdeu.
