# ESCONDER EM VEZ DE SAIR — o controle duplicado curado pelo outro lado

- **Estado:** CONCLUÍDA — o rótulo de 09/08 abaixo tem coordenadas velhas; hoje `esconder_o_fisico_para_o_jogo` está em `gamepad.py:544` (chamada em `:517`) e a caixinha em `main.glade:2359`, com doze arquivos de `tests/` citando a sprint (verificado em 21/08/2026)
- **Escrito em:** 09/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **Grau:** o defeito é **MEDIDO**; o desenho é **DECISÃO DELA**, tomada hoje
- **O que é:** a caixinha *"Deixar a Steam entregar o controle neste jogo"* passa
  a curar o duplicado **sem desligar o Hefesto** — e para de derrubar o
  jogador 2
- **Estado (09/08/2026, fim do dia):** **ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA
  DELA E MENOS O APARELHO.** O desenho da seção 3 e os textos da seção 4
  entraram em `7a0a655` (09/08/2026): `esconder_o_fisico_para_o_jogo` em
  `daemon/subsystems/gamepad.py:339`, chamada na borda da exceção em `:312`, com
  os vpads do co-op de pé (`:832` e `:841`) e a caixinha rebatizada em
  `gui/main.glade:2101`. Conferência na
  [nota datada no fim](#nota-datada-09082026--o-que-entrou-hoje-e-o-que-so-a-mesa-dela-fecha)
- **O que falta ela validar, em uma linha:** é a seção 6 deste documento, e ela
  não mudou — **abrir o jogo marcado com dois controles e contar quantos o jogo
  lista e quantos jogadores entram**; o alvo é um controle por pessoa, dois
  jogadores
- **E falta a palavra dela sobre o texto novo da caixinha** — *"Esconder o
  controle físico neste jogo"* está escrito no código, mas quem decide o texto é
  ela (PROVA-DE-TELA-01)

---

## 1. O que a caixinha resolve, na palavra dela

> *"eu conecto uma unidade de controle e na hora do jogo ele aparece como inputs
> duplicados em um segundo controle virtual"*

Um controle na mão, **dois** na tela do jogo: o físico e o virtual do Hefesto.

**E não tem nada a ver com o rumble.** Ela corrigiu isso duas vezes, e a segunda
com a medição na mão: *"o rumble já funcionou no modo nativo e no modo xbox e no
modo dualsense"*. Fica escrito aqui porque eu misturei as duas coisas três vezes
nesta noite.

---

## 2. Como o produto cura hoje — e o preço que ninguém declarou

Marcar o jogo arma a exceção (`daemon/subsystems/gamepad.py:282-284`), e a
exceção faz o Hefesto **sair da frente**:

1. solta o controle físico (`gamepad_controller_grab grab=False`);
2. reexpõe o hidraw físico ao jogo (`hidraw_broker_restored_all`);
3. **suspende os gamepads virtuais** (`suspend_vpads_for_steam_input`, `:447`).

Sobra o físico, sozinho. Duplicado resolvido — **com um controle**.

**O preço, MEDIDO na máquina dela em 08/08:** o jogador 2 **é** um gamepad
virtual. Desligar os virtuais para resolver o duplicado do jogador 1 derruba o
jogador 2 junto — `coop_derrubado_pela_excecao_steam_input`, **20 ocorrências**.

E o texto da caixinha (`gui/main.glade:2102`) promete o oposto do que entrega:

> *"Marcado: o jogo passa a ver o controle de verdade e lista UM só — e a sua
> cor, os seus gatilhos e a sua vibração continuam valendo"*

**Não diz uma palavra sobre perder o segundo jogador.**

---

## 3. O desenho dela: esconder, em vez de sair

Duplicado é o jogo enxergando **os dois**. Há duas formas de acabar com isso, e o
produto escolheu a que custa mais:

| saída | o que o jogo vê | co-op |
|---|---|---|
| **hoje** — o Hefesto sai: solta o físico, desliga os virtuais | só o físico | **quebra**: o jogador 2 era virtual |
| **decisão dela** — o Hefesto fica: **esconde o físico**, mantém os virtuais | só o virtual | **funciona**: cada controle tem o seu |

> **A regra, na frase dela, de 08/08:** *"a allowlist do Steam Input NÃO tira o
> Hefesto da frente."*

E o mecanismo **já existe**: o broker de hidraw tem `hide`/`restore`
(`broker/hidraw_broker.py:416-446`) e é ele que a exceção chama hoje — só que na
direção contrária. A cura é inverter o sentido, não escrever mecanismo novo.

**Ganho colateral, e não é pequeno:** com os virtuais de pé, cor, gatilhos,
vibração e numeração continuam sendo do Hefesto no jogo marcado. Hoje, marcar
entrega tudo isso ao jogo.

---

## 4. O que muda na tela

A caixinha deixa de dizer o que o produto **deixa de fazer** e passa a dizer o
que ele **faz**. Direção do texto (a palavra final é dela — PROVA-DE-TELA-01):

> **[ ] Esconder o controle físico neste jogo**
> *"Para jogos que mostram o seu controle DOBRADO — um Xbox e um Sony. Marcado,
> o jogo vê só o controle do Hefesto, e a sua cor, os seus gatilhos, a sua
> vibração e os seus jogadores continuam valendo."*

O nome antigo descrevia a **implementação** ("deixar a Steam entregar"); o novo
descreve o **efeito**, que é o léxico desta casa.

---

## 5. O que NÃO muda

- **os dois appids medidos ficam** — `2111190` (Mullet Mad Jack) e `3357650`
  (Pragmata) entraram com medição de duplicado real e continuam válidos;
- **a decisão de marcar continua dela.** Nada é marcado ou desmarcado por
  dedução nossa;
- **o `1599660` (Sackboy)** continua marcado até ela dizer o contrário — com
  esta cura, marcar deixa de custar o jogador 2, e a pergunta perde a urgência.

---

## 6. O que precisa ser medido depois de pronto

A prova é dela, com o aparelho: **abrir o jogo marcado com dois controles e
contar quantos o jogo lista, e quantos jogadores entram.** O alvo é *um controle
por pessoa, dois jogadores* — hoje é *um controle, um jogador*.

---

## NOTA DATADA (09/08/2026) — o que entrou hoje, e o que só a mesa dela fecha

Conferido no código de hoje. **O texto acima não foi reescrito** — ele é o
desenho como ela o decidiu, e continua sendo o contrato.

**Tudo o que esta sprint desenhou está commitado em `7a0a655` (09/08/2026).**
Não sobrou nada na árvore suja.

| o que a sprint pediu | onde está hoje |
|---|---|
| esconder o físico em vez de sair da frente | `daemon/subsystems/gamepad.py:339` `esconder_o_fisico_para_o_jogo`, chamada na borda da exceção em `:312` |
| **não** suspender os vpads | `daemon/subsystems/gamepad.py:832` e `:841`: `suspend_vpads_for_steam_input` deixou de ser chamada na borda de entrada |
| **não** soltar o grab do físico | mesma borda, `:312` — o `gamepad_controller_grab grab=False` saiu do caminho |
| a caixinha muda de nome e de promessa | `gui/main.glade:2101` — o rótulo passou a descrever o efeito, não a implementação |
| os dois appids medidos ficam | `2111190` e `3357650` intocados |

A inversão é a que a seção 3 previu: o mecanismo `hide`/`restore` do broker
(`broker/hidraw_broker.py:416-446`) passou a ser chamado **na direção
contrária**. Nenhum mecanismo novo foi escrito, exatamente como a sprint disse
que seria.

### Por que isto NÃO é "entregue" no sentido pleno

Duas coisas seguram, e as duas são dela:

1. **O aparelho.** A prova desta sprint é contar controles na tela de um jogo de
   verdade. Nenhum teste desta casa consegue contar quantos controles um jogo
   lista. É a seção 6, e ela continua aberta.
2. **A tela.** O texto novo da caixinha é uma **direção** proposta, e o próprio
   documento escreveu isso: *"a palavra final é dela — PROVA-DE-TELA-01"*.

### O grau, como manda a casa

**MEDIDO** para o código: há símbolo, chamador e commit. **SEM PROVA** para o
efeito — ninguém abriu o jogo marcado com dois controles depois da cura.
