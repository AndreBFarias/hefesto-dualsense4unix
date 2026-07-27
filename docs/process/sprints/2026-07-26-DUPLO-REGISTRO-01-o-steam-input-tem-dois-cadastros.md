# DUPLO-REGISTRO-01 — o Steam Input tem dois cadastros, e eles não se falam

- **Status:** ABERTA
- **Prioridade:** ALTA — produz input duplicado dentro do jogo, medido ao vivo
- **Aberta em:** 26/07/2026, durante uma partida de Pragmata
- **Relação:** é o mecanismo que faltava em
  [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md).
  Aquela sprint trata do que a tela **diz**; esta trata de dois registros do
  mesmo fato que divergem em silêncio

## O relato dela

> *"agora mesmo tá quase perfeito mas inputs duplicados e pra piorar o dualsense
> mudou de perfil e virou o player 2"*

E a informação que orienta a cura:

> *"jogos com conexão nativa, devemos usar o ativar steam pra ele funcionar"*
>
> *"eu tava com a steam ativada e tava funcionando perfeitamente, lightbar,
> trigger, vibração tudo"*

Ela está certa, e isso é o que `docs/usage/jogos-e-mascaras.md` já registra:
jogos cujo suporte a DualSense vem **pela Steam** precisam enxergar o controle
físico, e por isso pedem a exceção por jogo.

## O que foi medido — quatro joysticks para um controle

Com o Pragmata aberto e **um** DualSense na mesa:

```
js0  Hefesto Virtual DualSense P1                  <- o vpad do Hefesto
js2  Sony Interactive Entertainment DualSense ...  <- o controle FÍSICO, visível
js4  Microsoft X-Box 360 pad 0                     <- Steam Virtual Gamepad
js5  Microsoft X-Box 360 pad 1                     <- Steam Virtual Gamepad
```

Este é exatamente o quadro que a JOGO-01 fechou em 25/07 — e ele voltou por uma
porta que aquela sprint não cobria.

### A causa: dois cadastros do mesmo fato

O fato é **"o Steam Input está ligado para o Pragmata"**. Ele está escrito em
dois lugares, e só um é consultado:

| Onde | Conteúdo medido | Quem escreve |
|---|---|---|
| `localconfig.vdf`, bloco `3357650` | `UseSteamControllerConfig "2"` — **ligado** | a Steam, pela interface dela |
| `~/.config/hefesto-dualsense4unix/steam_input_apps.txt` | só `2111190` — o Pragmata **ausente** | só o botão "Este jogo não funciona" (`app/actions/daemon_actions.py:994`) |

O Hefesto decide se sai da frente olhando **apenas o segundo**. Como o Pragmata
não estava lá, ele manteve o vpad de pé, e o jogo passou a ver o vpad **e** o
que a Steam entrega.

E o controle físico também ficou visível, porque o grab não fechou:

```
23:26:22  gamepad_controller_grab  grab=True  ok=True  state=pending
```

`state=pending` — pedido feito, não confirmado. O físico continua em `js2`.

### Por que ela caiu nisso sem errar nada

Porque o próprio Hefesto ensina o caminho que produz a divergência.
`app/actions/daemon_actions.py:313-317`, no toast do produto:

> *"...na Steam: botão direito no jogo → Propriedades → Controle → 'Ativar'
> (agora o Hefesto respeita essa escolha em vez de desfazê-la)."*

Seguir essa frase liga o Steam Input **na Steam** e não escreve nada na allowlist
do Hefesto. A frase só é verdadeira para um appid que já esteja na allowlist —
para qualquer outro jogo ela é falsa.

### Hipótese que foi levantada e REFUTADA por medição

Antes de medir, a suspeita era que o guarda (`hefesto-steam-input-guard`) tivesse
desligado o Steam Input do Pragmata no boot, porque o timer estava morto
(`NextElapse=infinity`) e um reboot o ressuscita com `OnBootSec=3min`. O journal
confirma que o guarda **rodou e editou** o arquivo às 22:48:05, três minutos
depois do boot das 22:45.

Mas o campo não mudou. Comparando o backup que o próprio guarda criou com o
arquivo atual:

```
app=3357650  valor=2   (no backup, antes)
app=3357650  valor=2   (agora, depois)
```

**O guarda preservou a escolha dela.** A hipótese cai. O que ele editou foram
outros blocos. Fica registrado porque era a explicação mais plausível e teria
fechado o caso no lugar errado.

## O conserto aplicado hoje, à mão

```
+ 3357650   em ~/.config/hefesto-dualsense4unix/steam_input_apps.txt
```

Isto faz o Hefesto reconhecer que o jogo é da exceção, retirar o vpad e sair de
cena. É remendo: o registro continua duplicado, e a próxima divergência acontece
do mesmo jeito no próximo jogo.

## Entregas

### 1. Um cadastro só — a Steam é a fonte da verdade

O estado "este jogo usa Steam Input" já está no `localconfig.vdf`, escrito pela
Steam. O Hefesto passa a **ler** esse arquivo para decidir se sai da frente, em
vez de manter uma lista paralela.

A allowlist não some — ela muda de papel. Deixa de ser *a verdade* e passa a ser
*a intenção declarada pelo Hefesto*, usada só pelo guarda para saber o que **não**
desfazer. As duas param de poder divergir porque só uma decide.

### 2. Enquanto houver duas listas, a divergência é visível e tem um clique

Se o item 1 for grande demais para uma leva, o piso é:

- na subida e a cada varredura do guarda, comparar as duas listas;
- quando divergirem, dizer na aba Sistema, com nome de jogo:
  > **Pragmata** está com a entrada Steam ligada na Steam, mas o Hefesto não
  > sabia. Enquanto isso, o jogo enxerga dois controles.
  > [ Registrar no Hefesto ]  [ Desligar na Steam ]
- e registrar no journal.

### 3. O toast para de ensinar o caminho que quebra

`daemon_actions.py:313-317` passa a dizer a verdade inteira: ligar pela Steam
sozinho **não** basta, porque o Hefesto precisa saber para sair da frente. Com o
item 1 entregue, a frase some — vira verdade automaticamente.

### 4. Grab pendente deixa de ser silencioso

`state=pending` significa que o controle físico continua visível para o jogo, que
é metade do duplicado. Hoje isso só aparece no journal. Passa a:

- ser retentado enquanto a sessão de jogo estiver de pé;
- e, se não fechar, aparecer na aba Status como aviso legível — "o controle
  físico não pôde ser escondido do jogo; você pode ver comandos duplicados".

### 5. Teste que morde

- Cenário: `localconfig.vdf` com `UseSteamControllerConfig=2` e allowlist sem o
  appid. O produto tem de detectar a divergência. Arrancar o comparador reprova.
- Cenário: appid registrado. O vpad tem de ser retirado — e o teste conta os
  dispositivos, não chama o método privado.
- `state=pending` que nunca fecha tem de virar aviso.

## Como você valida

1. Abra o Pragmata. Nos controles do jogo, **um** controle é listado, não dois.
2. Nenhum comando anda em dobro (o analógico não move o dobro, o botão não conta
   duas vezes).
3. Ligue a entrada Steam de outro jogo **pela Steam**, e volte ao Hefesto: ele
   avisa que soube, com o nome do jogo, e oferece o clique que resolve.
4. Lightbar, gatilhos e vibração continuam funcionando — o Hefesto sai do
   caminho do **input**, não do controle.

## O que NÃO foi medido

- **Não confirmei ao vivo que o duplicado sumiu.** A allowlist foi corrigida com
  ela jogando, e reiniciar o daemon no meio da partida contraria as regras da
  casa. A validação é a próxima sessão.
- **Não medi por que o grab ficou `pending`.** Sei que ficou, e sei o efeito.
  Não sei se é corrida com a Steam abrindo o dispositivo, se é o `EVIOCGRAB`
  recusado, ou se é o caminho da allowlist retirando o vpad no meio.
- **Os dois `X-Box 360 pad` da Steam não foram investigados.** Aparecem em par,
  e não sei se é comportamento normal do Steam Input com um controle, ou se é
  outro duplicado dentro do próprio Steam Input.
- **Não sei se ler o `localconfig.vdf` em runtime é seguro** com a Steam aberta.
  A casa já tem regra de nunca escrever com a Steam viva; **ler** é outra coisa,
  mas o arquivo é reescrito pela Steam e pode ser lido no meio de uma escrita.
  A entrega 1 depende de responder isso antes.
