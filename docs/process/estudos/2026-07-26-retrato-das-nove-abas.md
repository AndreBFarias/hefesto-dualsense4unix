# 26/07/2026 — Retrato das nove abas (árvore restaurada)

Registro visual pedido pela mantenedora: *"abra cada aba, printa e documenta
tudo"*. Cada uma das nove abas foi renderizada, fotografada e medida widget a
widget. Para cada aba este documento diz **o que ela mostra**, **onde está o
PNG**, **o que está medido de errado** (desalinhamento, corte de texto, vão
sobrando, tamanho de alvo de clique) e **o que já está certo** — porque uma
lista só de defeitos não serve para decidir o que mexer.

---

## De qual árvore é este retrato — e por quê

Os nove PNGs são do estado **RESTAURADO**, não da `main`:

- árvore: `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix`
- ramo: `restauro/inicio-da-sessao`
- commit: `4dd4652`, de 25/07/2026 22:36:44 -0300, cujo assunto é (sem acentos
  porque o higienizador do fluxo de commit os remove):

```
docs(sprints): o indice fechava a leva mas nao listava as quatro sprints que a validacao abriu
```

Este é o código que ela tem **instalado e rodando agora**. A `main` seguiu em
frente durante a madrugada de 26/07 (PLAYER-LED-01, CONTAGEM-01, faixa
permanente de microfone, SLOT-JOGADOR-01, botões ocupando o vão da barra de
abas, simetria do instalador, conserto do `doctor --fix-mic`, release v0.1.2), e
foi justamente essa leva que motivou o rollback. As palavras dela depois de
olhar a tela:

1. *"interface tá quebrada e na hora do jogo tá um caos legal"*
2. *"agora na hora de jogar o jogo o perfil do controle muda e sai as configs
   que eu deixei"* — o mais grave, porque desfaz o que ela configurou
3. *"agora eu não sei quando é pra ativar entrada Steam e quando não é. Pensei
   que tivéssemos superado isso"*

E o escopo, que ela repetiu e que foi extrapolado: mexer **só na aba Status** —
*"veja os elementos como analógicos, área do mic, os botões do DSX como
triângulo X bola minúsculos, o desalinhamento dos analógicos, a área do mic que
deveria ficar à direita dos analógicos. No caso era ali que era pra mexermos
apenas."*

Fotografar a `main` não ajudaria: a `main` é o estado que ela rejeitou. O
retrato precisa ser do que está na máquina dela, para que qualquer conserto
futuro parta do que ela realmente vê.

---

## Como o retrato foi feito

Um script carrega `src/hefesto_dualsense4unix/gui/main.glade` dentro de um
`GtkOffscreenWindow` de **1900x1040**, aplica o tema do projeto
(`hefesto_dualsense4unix.app.theme.apply_theme`), percorre as nove páginas do
`main_notebook` e, para cada uma, salva o PNG e mede três coisas:

- altura **mínima** e **natural** que a página pede, contra o que ela **recebe**;
- todo widget mapeado cuja alocação é menor que o próprio mínimo (isto é: texto
  ou conteúdo cortado);
- na aba Status, a geometria peça a peça dos dois cards de controle.

O script **não escreve nada** na árvore do projeto — só lê o `.glade` e o
pacote. Ele vive no scratchpad da sessão, junto com os PNGs:

```
.../scratchpad/retrato_abas.py          # gera PNGs + relatorio.json
.../scratchpad/medir_barra_abas.py      # mede a barra de abas
.../scratchpad/relatorio.json           # números citados aqui
.../scratchpad/retrato-abas/aba-*.png   # os nove retratos
```

Caminho completo do diretório de retratos:

```
assets/2026-07-26-abas/
```

**Aviso**: esse diretório é volátil (scratchpad de sessão). Os PNGs não foram
copiados para dentro do repositório porque a tarefa autorizava escrever apenas
este arquivo. Para refazê-los basta rodar `retrato_abas.py` apontando para a
mesma árvore restaurada.

### O que o retrato offscreen NÃO reproduz

Isto está aqui para que nenhum número abaixo seja lido como mais forte do que é:

1. **Widgets montados em código, não no `.glade`.** O seletor segmentado de
   modos dos gatilhos (`trigger_left_mode_slot`, `main.glade:455`) é preenchido
   em tempo de execução por `triggers_actions.install_triggers_tab`; o mesmo
   vale para `profile_mode_slot` (`main.glade:1681`) e para a lista de perfis
   salvos. No retrato esses espaços aparecem **vazios**, então o vão que se vê
   ali é maior do que o vão real na tela dela.
2. **Sem daemon vivo.** Todos os estados aparecem como `—` ou
   `Consultando…`. Onde um rótulo já está cortado com `—`, ele fica **pior**
   com o texto verdadeiro (`Ligado`, `Desligado`, `Ativo (Xbox 360)`).
3. **Cards de Status falsos.** Foram injetados **dois** `ControllerCard`
   sintéticos para que a aba não ficasse vazia. Com **um** controle a geometria
   muda (o card usa `STICK_SIZE_SINGLE = 88` em vez de
   `STICK_SIZE_COMPACT = 70`); com **quatro**, o grid vira 2x2 e o vão
   vertical fecha.
4. **Sem compositor.** Não passa pelo `cosmic-comp` nem pelo fator de escala do
   monitor dela; não há decoração de janela. A janela real dela pode não ser
   exatamente 1900x1040 — as proporções valem, os pixels absolutos são
   aproximados.
5. **Sem interação.** Tooltip, popover, dropdown aberto, foco e *hover* não
   aparecem. Defeitos que só se manifestam ao clicar não estão neste retrato.
6. **Nada de comportamento.** Este documento é **geometria de tela**. A queixa
   mais grave dela — *"na hora de jogar o perfil do controle muda e sai as
   configs que eu deixei"* — é comportamento em jogo e **não foi medida aqui**.

---

## Resumo das nove abas

Todos os números vêm de `relatorio.json`, medidos com a página alocada em
1874x910 px (a área útil dentro da janela de 1900x1040).

| # | Aba | Altura pedida (natural) | Vão vertical sobrando | Widgets abaixo do próprio mínimo |
|---|---|---|---|---|
| 0 | Início | 132 px | **778 px** | 1 |
| 1 | Status | 627 px | 283 px | 3 |
| 2 | Gatilhos | 292 px | **618 px** | 2 |
| 3 | Lightbar | 440 px | 470 px | 4 |
| 4 | Rumble | 420 px | 482 px | 2 |
| 5 | Perfis | 442 px | 472 px | 2 |
| 6 | Sistema | 460 px | 450 px | 2 |
| 7 | Emulação | 606 px | 304 px | **12** |
| 8 | Navegação DSX | 531 px | 379 px | 1 |

Duas leituras saltam da tabela:

- **Nenhuma aba usa a tela.** A que mais pede (Emulação) pede 606 px de 910.
  Sobra tela em todas as nove. Só que a folga tem dois destinos diferentes: ou
  ela vira **faixa preta** (Início, Status, Rumble, Emulação, metade de Perfis
  e de Navegação DSX), ou ela vira **contêiner esticado e vazio** que empurra os
  botões para longe do controle que os comanda (Gatilhos, Lightbar, Sistema).
  O segundo caso é pior, porque parece proposital.
- **Emulação concentra 12 dos 19 cortes.** É a aba da queixa 3 dela, e o corte
  cai exatamente em cima dos rótulos que dizem o estado.

---

## Aba 0 — Início

**PNG**: `assets/2026-07-26-abas/aba-0-inicio.png`

**O que mostra.** Um único quadro, *"Jogar acompanhada"*, com um único botão:
**Preparar co-op**. Nada mais.

**O que está certo.** É a aba mais honesta do aplicativo: uma decisão, um botão,
sem jargão. O botão tem 143x38 px de alvo de clique — confortável.

**O que está errado, medido.**

- **778 px de tela vazia**, o maior vão do aplicativo. A página pede 132 px de
  altura e recebe 910. O quadro termina por volta de `y=243` no PNG e o resto é
  preto até o rodapé. Numa janela cheia, a primeira aba que ela vê é 85% vazia.
- `home_coop_box` recebe altura **64 px contra 84 px de mínimo** — 20 px a
  menos do que ele mesmo pede (`main.glade:211`). O botão não chega a ser
  cortado visualmente, mas o contêiner está espremido por baixo do mínimo, o
  que é o mesmo padrão que aparece em mais cinco abas.

---

## Aba 1 — Status

**PNG**: `assets/2026-07-26-abas/aba-1-status.png`

**Esta é a única aba que ela autorizou mexer.** Por isso é a única com medição
peça a peça.

**O que mostra.** Em cima, o quadro *"Estado"* (Conexão, Transporte, Bateria,
Perfil ativo, Hefesto). Embaixo, um card por controle lado a lado — no retrato,
*"Controle 1 — USB"* (quadrado vermelho) e *"Controle 2 — BLUETOOTH"* (quadrado
azul). Dentro de cada card: barra de bateria com percentual, cor da lightbar,
barras de L2 e R2 com valor bruto, giroscópio em três eixos e, na linha de
baixo, os módulos ao vivo — Touchpad, Microfone, Analógico Esquerdo, Analógico
Direito, Lightbar, Alto-falante — e, encostado na borda direita, o grid 4x4 dos
16 botões.

**O que está certo.**

- Os dois cards ficam **lado a lado sem barra de rolagem** (`status_players_slot`
  é um `GtkGrid`, `main.glade:405`) — foi um conserto pedido por ela e ele
  sobreviveu ao rollback.
- A identificação por cor funciona: o quadradinho do cabeçalho tem a cor da
  lightbar daquele controle, e o número bate com o texto.
- O selo do microfone (`ATIVO` em verde no card 1, `MUDO` em cinza no card 2) é
  legível de longe — é o elemento mais bem resolvido do card.
- Os valores numéricos (`40 / 255`, `X: 128`, `+3.5`) usam campo de largura
  fixa, então o painel não "respira" a 10 Hz.

**Defeito 1 — os analógicos estão desalinhados em 20 px.** É literalmente a
queixa dela, e a causa é a quebra de linha do rótulo.

| Peça | Esquerdo (L3) | Direito (R3) | Degrau |
|---|---|---|---|
| Rótulo (altura / linhas) | 60 px / **3 linhas** | 40 px / **2 linhas** | 20 px |
| Desenho do analógico (y) | 245 | 225 | **20 px** |
| Rótulo X/Y (y) | 319 | 299 | **20 px** |
| Cápsula inteira (altura) | 180 px | 160 px | 20 px |

O texto `"Analógico Esquerdo (L3)"` quebra em três linhas e
`"Analógico Direito (R3)"` em duas, porque ambos passam por
`set_line_wrap(True)` (`controller_card.py:818`) com
`set_max_width_chars(_TITULO_STICK_MAX_CHARS)` (`:820`), e
`_TITULO_STICK_MAX_CHARS = 10` (`:115`). Os títulos entram em `:851` e `:861`.
Como as duas cápsulas são empilhadas de cima para baixo e **nada alinha os
desenhos entre si**, a linha extra do rótulo esquerdo empurra tudo o que vem
depois dele. O degrau é idêntico nos dois cards — não é acidente de conteúdo, é
estrutural.

**Defeito 2 — os botões do DSX têm 20x20 px reais.** Cruz, círculo, quadrado,
triângulo e os outros doze medem exatamente **20x20 px** cada
(`cross` em x=817, `circle` 839, `square` 861, `triangle` 883, todos em y=228).
O grid 4x4 inteiro ocupa **86x86 px dentro de um card de 931x382** — 9,2% da
largura do card para os 16 botões. A causa é uma constante em pixel cru:
`GLYPH_SIZE: Final[int] = 20` (`controller_card.py:97`), passada em `:882`. Por
ser px e não CSS, **não cresce com a escala de fonte**: o A/B com escala 0 e
com a escala 3 (a dela) devolveu os mesmos 20x20.

**Defeito 3 — o microfone está à ESQUERDA dos analógicos.** Ordem horizontal
real medida na linha de baixo do card:

| x | bloco |
|---|---|
| 28 | Touchpad (e, abaixo, Lightbar) |
| 103 | Alto-falante |
| **116** | **Microfone** |
| 203 | Analógico Esquerdo, depois o Direito (faixa de 166 px) |
| 817 | grid 4x4 dos botões |

Ou seja: o oposto do que ela pediu (*"a área do mic que deveria ficar à direita
dos analógicos"*). A causa é a ordem de empacotamento: o microfone é montado
dentro da coluna *sensores* (`controller_card.py:693`, módulo em `:712-753`), e
essa coluna inteira entra na linha com `pack_start` em `:699`, enquanto os
analógicos só entram em `:701`.

Registro importante: **a área do microfone EXISTE nesta árvore restaurada.** Ela
aparece no PNG, com medidor e selo `ATIVO`/`MUDO`. O rollback não a apagou — o
que a leva da madrugada fez foi transformá-la numa faixa permanente, e isso é
outra coisa.

**Defeito 4 — 448 px de vazio horizontal dentro do card.** A faixa dos
analógicos termina em `x=369` e o grid de botões só começa em `x=817`, dentro
de uma linha de 875 px de largura: **448 px de nada no meio**. A causa é que os
glifos estão ancorados à direita (`glyphs.set_halign(Gtk.Align.END)` em
`controller_card.py:707`, `linha.pack_end(...)` em `:708`) e **nenhum bloco
entre eles expande**. É exatamente a largura que faltaria para os analógicos e
os glifos crescerem — o vão e o "tudo minúsculo" são o mesmo defeito visto de
dois lados.

**Defeito 5 — os cards recebem menos altura do que pedem.** Cada card é alocado
com **338 px de altura contra 358 px de mínimo** (20 px a menos), e o
`status_grid` do quadro *"Estado"* recebe **161 px contra 185 px** (24 px a
menos). Ninguém corta texto visível ainda, mas a página está apertando os
próprios filhos enquanto sobra tela.

**Defeito 6 — 283 px de folga vertical desperdiçada.** A página pede 627 px e
recebe 910. Na leitura do PNG, o conteúdo acaba por volta de `y=740` e o preto
vai até o fim da área de página (~`y=1045`), o que dá pouco mais de 300 px de
faixa morta. Com **quatro** controles em 2x2 esse vão fecha; com **um ou dois**
— o caso comum dela — é a metade de baixo da tela.

---

## Aba 2 — Gatilhos

**PNG**: `assets/2026-07-26-abas/aba-2-gatilhos.png`

**O que mostra.** Duas colunas simétricas, *"L2 (gatilho esquerdo)"* e
*"R2 (gatilho direito)"*, cada uma com o rótulo **Modo:**, a área de parâmetros
do modo e, no pé, os botões **Aplicar em L2** / **Desligar** (e o par espelhado
à direita).

**O que está certo.** A simetria é perfeita e imediata de entender: o lado
esquerdo da tela comanda o gatilho esquerdo. Os botões têm alvo generoso
(~450 px de largura por 34 px de altura) e a ação destrutiva (*Desligar*) está
visualmente separada da confirmação (*Aplicar*, com borda verde).

**O que está errado, medido.**

- **618 px de vão vertical** — o segundo maior do aplicativo. A página pede
  292 px e recebe 910. E aqui a folga **não** vira faixa preta: ela é engolida
  pelo `GtkScrolledWindow` de parâmetros, que tem `vexpand=True` e
  `min-content-height=110` (`main.glade:508-513`). O efeito prático é que os
  botões **Aplicar em L2** e **Desligar** são empurrados para o rodapé, a mais
  de 800 px do rótulo **Modo:** que eles obedecem. Quem escolhe o modo no topo
  precisa atravessar a tela inteira para confirmar.
- `trigger_left_desc` e `trigger_right_desc` (a linha que explica o modo
  escolhido) recebem **22 px de altura contra 26 px de mínimo** — a descrição
  do modo é cortada por 4 px.

**Ressalva de medição.** O seletor segmentado de modos não é montado offscreen
(`trigger_left_mode_slot`, `main.glade:455`), então o vazio do PNG é maior do
que o da tela dela. Mas o `vexpand=True` do scroller garante que a folga
continue existindo mesmo com todos os parâmetros carregados — o defeito não
depende do que falta na foto.

---

## Aba 3 — Lightbar

**PNG**: `assets/2026-07-26-abas/aba-3-lightbar.png`

**O que mostra.** À esquerda, *"Lightbar (barra de LED)"*: caixa de cor, prévia,
os botões **Aplicar no controle** / **Apagar**, **Voltar ao automático** /
**Voltar todos ao automático**, e o slider de Luminosidade. À direita,
*"Desenho das 5 luzes"*: os presets **Desenho do P1..P4**, **Todas acesas**,
**Todas apagadas**, **Aplicar o desenho**, a linha *"Aceso agora: consultando…"*
e dois parágrafos explicando quem vence quem.

**O que está certo.** É a aba com a melhor escrita do aplicativo. Os dois
parágrafos respondem exatamente a pergunta que a interface costuma deixar no ar:
*"o desenho que você escolhe aqui vence o automático neste controle... Com o
co-op ligado, quem manda no desenho é o co-op."* Isso é o oposto do que acontece
na aba Emulação. Os quatro presets de player têm ~330 px de largura cada.

**O que está errado, medido.**

- A coluna esquerda inteira é **espremida 21 px abaixo do próprio mínimo**:
  recebe **447 px de largura contra 468 px** que ela pede. É a coluna que tem a
  prévia da cor e os quatro botões de texto longo.
- Três elementos da coluna direita ficam **8 px abaixo do mínimo em altura**: o
  rótulo *"Presets rápidos:"* (22 px contra 30), a fileira de botões
  **Desenho do P1..P4** (38 px contra 46) e a linha
  *"Aceso agora: consultando…"* (22 px contra 30).
- **470 px de folga vertical**, aqui gastos esticando os dois quadros até o
  rodapé. O resultado é o conteúdo todo aglomerado no terço de cima com dois
  retângulos vazios embaixo.

**Medido e REFUTADO como defeito.** Os checkboxes `player_led_1..5` não
aparecem no retrato (`visible=false`, alocação `[-1,-1,1,1]`). **Isso é
intencional**, não regressão: `main.glade:920-925` marca a caixa com
`visible=False` e `no-show-all=True`, e o comentário logo acima (`:913-919`)
registra o motivo — LEDS-SO-PLAYER-01, pedido dela em 22/07, porque escolher
LED a LED confundia ("player 1 acende o LED 3" parecia bug, mas é o padrão
oficial do PS5). Os checkboxes seguem existindo como estado interno.

---

## Aba 4 — Rumble

**PNG**: `assets/2026-07-26-abas/aba-4-rumble.png`

**O que mostra.** Em cima, *"Intensidade da vibração dos jogos"*: quatro opções
segmentadas (**Economia**, **Balanceado**, **Máximo**, **Auto**, com Balanceado
marcado) e o slider *Intensidade global* em 70. Embaixo, *"Testar motores
(enquanto testa, o jogo não controla a vibração)"*: sliders de Vibração leve e
forte, os botões **Testar por 500 ms**, **Aplicar**, **Parar**, **Deixar o jogo
controlar a vibração**, e a linha *"Estado da vibração: —"*.

**O que está certo.** Os rótulos explicam o efeito, não o mecanismo:
*"Multiplica a vibração que o JOGO pede — é aqui que se aumenta ou diminui a
força sem tirar o controle dele"*. O aviso entre parênteses no título do
segundo quadro previne exatamente a confusão de achar que o teste quebrou o
jogo. As quatro opções segmentadas têm ~460 px de largura cada — alvo enorme.
E há um botão **Parar** explícito, o que importa depois do incidente do rumble
preso.

**O que está errado, medido.**

- Os **dois quadros ficam 28 px abaixo do próprio mínimo em altura**: o de cima
  recebe 82 px contra 110 px de mínimo; o de baixo, 190 px contra 218 px. É o
  maior aperto proporcional do aplicativo fora da aba Emulação — e acontece
  numa aba com **482 px de folga sobrando**. A página aperta os filhos e deixa
  meia tela preta ao mesmo tempo.
- Abaixo de `y≈530` no PNG não há nada até o rodapé.

---

## Aba 5 — Perfis

**PNG**: `assets/2026-07-26-abas/aba-5-perfis.png`

**O que mostra.** À esquerda, *"Perfis salvos"* (lista, vazia no retrato) com a
fileira **Novo / Duplicar / Remover / Ativar / Recarregar** no pé. À direita,
*"Editor do perfil"* com o interruptor **Modo avançado**, campo **Nome**,
slider **Prioridade** (0–100), a área **Aplica a:**, o quadro *"Modo (o que
este perfil liga ao ativar)"* e o botão **Salvar**.

**O que está certo.** Os cinco botões de gerência da lista são homogêneos
(~175 px cada) e ficam colados na lista que comandam. O slider de prioridade
tem marcas em 0, 50 e 100, o que torna o número compreensível sem
documentação.

**O que está errado, medido.**

- O quadro *"Modo (o que este perfil liga ao ativar)"* **colapsa para 1 px de
  altura**: `profile_mode_slot` é alocado `[974 x 1]` contra um mínimo de
  `[16 x 16]`, e `profile_mode_frame` recebe `[992 x 40]` contra `[286 x 48]` —
  8 px abaixo do próprio mínimo. Na foto, o quadro vira um risco vazio no meio
  da coluna direita.
- A área **Aplica a:** fica com cerca de 190 px de altura sem nada dentro.
- **472 px de folga vertical**: a lista da esquerda estica até o rodapé, mas a
  coluna da direita termina o conteúdo em `y≈550` e o resto é preto.

**Ressalva de medição.** `profile_mode_slot` (`main.glade:1681`) é preenchido em
tempo de execução pelas ações de perfil, então **na tela dela pode haver
conteúdo ali**. O que continua valendo sem ressalva é que o `frame` já é alocado
8 px abaixo do próprio mínimo **antes** de qualquer conteúdo entrar.

**Nota de escopo.** Esta é a aba mais próxima da queixa mais grave dela (*"na
hora de jogar o perfil do controle muda"*), mas **nada aqui mede isso**. O que
troca de perfil é o autoswitch, não a geometria desta tela.

---

## Aba 6 — Sistema

**PNG**: `assets/2026-07-26-abas/aba-6-sistema.png`

**O que mostra.** No topo, *"O Hefesto está: —"*, o interruptor *"Ligar junto
com o computador"* e cinco botões largos: **Ligar o Hefesto**, **Desligar o
Hefesto**, **Atualizar**, **Ver detalhes**, **Reiniciar o Hefesto**. Depois
*"Saúde do sistema"*, o bloco **Jogos da Steam** (**Deixar tudo pronto** /
**Este jogo não funciona**), o bloco **Avançado — só se você quiser controlar
cada passo** (**Aplicar correções**, **Copiar opções p/ jogos**, **Aplicar aos
jogos da Steam**, **Travar Proton validado**) e, ocupando o resto da tela, o
campo *Detalhes técnicos*.

**O que está certo.** A separação simples/avançado é a resposta certa à queixa
dela sobre QoL: **Deixar tudo pronto** e **Este jogo não funciona** são frases
de usuária, e os quatro botões de mecanismo estão rebaixados sob um rótulo que
avisa que ali é opcional. Os cinco botões do topo têm ~175 px de largura por
34 px de altura.

**O que está errado, medido.**

- Os dois rótulos de seção são cortados: `steam_simples_label`
  (*"Jogos da Steam"*, `main.glade:1854`) e `steam_avancado_label`
  (*"Avançado — só se você quiser controlar cada passo"*, `main.glade:1892`)
  recebem **22 px de altura contra 28 px de mínimo**. São exatamente as duas
  frases que fazem a hierarquia da aba funcionar, e são as duas apertadas.
- **450 px de folga**, aqui integralmente absorvidos pelo campo *Detalhes
  técnicos*, que fica vazio até alguém pedir diagnóstico. Metade da tela é uma
  caixa de texto em branco.

---

## Aba 7 — Emulação

**PNG**: `assets/2026-07-26-abas/aba-7-emulacao.png`

**Esta é a aba da queixa 3 dela.** É também a aba com mais cortes: 12 dos 19
do aplicativo inteiro.

**O que mostra.** Dois painéis de leitura no topo (UINPUT, Device, VID:PID,
Gamepads; e Modo jogo com os atalhos PS + D-pad). Três botões de diagnóstico.
Depois, quatro linhas de decisão, cada uma no formato
`Rótulo: <estado> [botões]`:

- `Gamepad p/ jogos: —` -> **Desligado** / **DualSense (PS)** / **Xbox 360**
- `Modo jogo: —` -> **Modo jogo** / **Sair do modo jogo**
- `Steam Input: —` -> **Verificar** / **Desligar Steam Input**
- `Microfone do DualSense: —` -> **Ligar** / **Desligar**

Entre a primeira e a segunda há o parágrafo-guia de quatro linhas sobre qual
máscara serve para qual jogo.

**O que está certo.** O parágrafo de máscaras é bom conteúdo: nomeia jogos reais
(Sackboy, Pragmata, Mad King Redemption, Mullet Mad Jack), dá o sinal
diagnóstico (*"o controle navega na Steam, mas fica morto dentro do jogo"*) e
aponta o guia completo. Os três botões de máscara são grandes e mutuamente
exclusivos.

**Defeito 1 — o rótulo que diz o estado tem 15 px de largura.** Medido:

| Rótulo | Alocado | Mínimo |
|---|---|---|
| `emulation_steam_input_status_label` | **15 x 38** | 23 x 22 |
| `emulation_gamepad_status_label` | **15 x 38** | 23 x 22 |
| `emulation_gamemode_status_label` | **15 x 38** | 23 x 22 |
| `emulation_mic_status_label` | **15 x 38** | 23 x 22 |

Hoje o texto é só `—` e **já não cabe**. Com `Ligado` / `Desligado` o corte
piora. Os quatro contêineres-pai também estão abaixo do mínimo — por exemplo
`emulation_steam_input_box` (`main.glade:2258`) recebe `[1854 x 38]` contra um
mínimo de `[439 x 42]`. Isto é a queixa 3 batendo em geometria: ela não sabe se
a entrada Steam está ligada porque **a interface literalmente não tem largura
para dizer**.

**Defeito 2 — nada na tela responde "quando eu ligo a entrada Steam".** A linha
inteira é `Steam Input: — [Verificar] [Desligar Steam Input]`, sem uma palavra
ao lado. O único parágrafo da aba cita a entrada Steam **uma vez**, e só como
exceção por jogo: *"Quando o suporte a DualSense do jogo vem PELA Steam (é o
caso do Mullet Mad Jack), o jogo precisa enxergar o controle físico: use a
exceção por jogo em 'Steam Input' na aba Emulação"*. Não existe frase que diga o
**caso padrão**. E o botão só oferece **Desligar** — não há **Ligar** —, então a
interface nem sugere que ligar seja uma opção legítima.

**Registro que importa para o rollback:** esta queixa **sobreviveu** ao
rollback. Ela não foi introduzida na madrugada de 26/07; ela está aqui, no
estado restaurado, exatamente como estava. Voltar para `4dd4652` não a
resolveu — e nada na leva revertida a resolvia tampouco.

**Defeito 3 — os blocos de diagnóstico ficam bem abaixo do mínimo.**
`emulation_diagnostico_row` recebe `[1293 x 174]` contra `[947 x 256]` (82 px a
menos); `emulation_info_grid` recebe `[603 x 154]` contra `[277 x 256]` (102 px
a menos); `emulation_combo_grid` recebe `[634 x 154]` contra `[654 x 174]` —
abaixo do mínimo **nas duas dimensões**.

**Defeito 4 — 304 px de faixa preta** abaixo da última linha, enquanto tudo
acima está comprimido.

---

## Aba 8 — Navegação DSX

**PNG**: `assets/2026-07-26-abas/aba-8-navegacao-dsx.png`

**O que mostra.** À esquerda, o interruptor **Emular mouse+teclado**, os sliders
*Velocidade do cursor* (6) e *Velocidade da rolagem* (1), e o quadro
**Mapeamento** com oito linhas (`Cruz (X) ou L2 -> Botão esquerdo`,
`Triângulo ou R2 -> Botão direito`, `R3 -> Botão do meio`, `Círculo -> Enter`,
`Quadrado -> Esc`, `D-pad -> Setas do teclado`, `Analógico esquerdo -> Movimento do
cursor`, `Analógico direito -> Rolagem`). À direita, *"Atalhos de teclado do
perfil ativo"* com a explicação do formato `KEY_*`, uma lista e os botões
**Adicionar / Remover / Restaurar defaults**.

**O que está certo.** A tabela de mapeamento é o melhor bloco informativo do
aplicativo inteiro: duas colunas alinhadas, uma linha por botão, seta no meio,
sem jargão. É o modelo que a aba Emulação deveria seguir. O rodapé explicativo
diz a dependência real (*"requer módulo uinput carregado e regra udev — ver aba
Emulação"*), que é o tipo de ligação entre abas que ela pediu.

**O que está errado, medido.**

- O quadro **Mapeamento** recebe **235 px de altura contra 255 px de mínimo** —
  20 px a menos. As oito linhas cabem, mas sem folga nenhuma.
- **379 px de folga vertical**: a coluna esquerda encerra em `y≈665` e o preto
  vai até o rodapé; a coluna direita estica a lista de atalhos vazia até
  `y≈1005`.
- A explicação do formato (`KEY_*`, `__OPEN_OSK__`, combos com `+`) está acima
  de um campo vazio, sem nenhum exemplo já preenchido. Não é corte de pixel —
  é a mesma doença da aba Emulação: a tela documenta a sintaxe e não o caso de
  uso.

---

## Transversal — a barra de abas

Medido com `medir_barra_abas.py`, na mesma janela de 1900x1040:

| Aba | x | largura |
|---|---|---|
| Início | 33 | 42 |
| Status | 111 | 51 |
| Gatilhos | 198 | 63 |
| Lightbar | 297 | 65 |
| Rumble | 398 | 57 |
| Perfis | 491 | 43 |
| Sistema | 570 | 61 |
| Emulação | 667 | 75 |
| Navegação DSX | 778 | 120 |

A última aba termina em `x=898`. Sobram **1002 px** de barra vazia — mais da
metade da largura da janela.

**Este vão fica como está.** Foi exatamente ele que a leva da madrugada
preencheu com botões, e foi um dos itens que ela apontou como **fora do
escopo**: *"no caso era ali que era pra mexermos apenas"*, falando da aba
Status. O registro existe aqui para que o vão seja reconhecido como **conhecido
e deliberadamente não mexido**, e não redescoberto como novidade na próxima
auditoria.

Uma observação de altura, essa sim possivelmente acionável no futuro: os
rótulos de aba têm **30 px de altura** dentro de uma célula de 32 px. É um alvo
de clique baixo para uma barra que é o principal meio de navegação do
aplicativo.

---

## O que este documento NÃO diz

Dito de forma explícita, para não virar autoridade indevida:

- **Não mede comportamento.** A queixa mais grave dela — o perfil trocando
  sozinho durante o jogo e desfazendo as configurações — é do autoswitch, e
  **não foi investigada aqui**.
- **Não mede a `main`.** Nenhum PNG, nenhum número deste documento vem do estado
  pós-madrugada. Comparação entre restaurado e `main` **não foi feita**.
- **Não mede a janela real dela.** É render offscreen, sem `cosmic-comp`, sem
  fator de escala, sem decoração. As proporções e as relações (quem está acima
  do quê, quem é menor que o próprio mínimo) valem; os pixels absolutos são
  aproximados.
- **Não mede com 1 nem com 4 controles.** A aba Status foi fotografada com dois
  cards sintéticos. Com um controle o card fica mais alto
  (`STICK_SIZE_SINGLE = 88` contra `STICK_SIZE_COMPACT = 70`,
  `controller_card.py:109-110`); com quatro, o grid 2x2 fecha o vão vertical.
- **Não mede estados carregados.** Todos os rótulos de estado estão em `—`. Os
  cortes reportados são o **piso**: com texto de verdade eles pioram.
- **Não mede interação.** Tooltip, dropdown aberto, foco, `hover` e diálogos
  ficaram fora.
- **Nada foi alterado.** Nenhum arquivo da árvore
  `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix` foi tocado — o
  retrato é leitura pura, e o Hefesto instalado roda direto dali.
