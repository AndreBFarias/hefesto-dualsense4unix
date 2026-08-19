# O que precisa de você — 19/08/2026

Fechei a **0.9.4.5** e rodei o install. Esta lista é só o que **não dá para eu
fazer sozinha**: ou depende do seu olho, ou é decisão sua.

Sete itens. Os três primeiros são de dez minutos cada; os quatro últimos são
decisões, e você responde em uma linha.

---

## Agora está de pé, sem você fazer nada

Para você saber o que já mudou antes de gastar tempo:

- **A allowlist do Steam Input está ligada nos quatro**: DON'T SCREAM, Duskfade,
  Grim Fandango e Pragmata. Fiz agora, com a Steam fechada — que é a única
  janela em que dá — e com salvaguarda ao lado do `localconfig.vdf`. Era o
  bloco B1 do roteiro de quarenta minutos; **pode pular ele**.
- **O daemon vivo já recusa vibração em Modo Nativo**, com a frase. Conferido
  contra o daemon que está rodando na sua máquina, não em dublê.
- **O install trava para sempre em quem não tem Bluetooth** — curado. Os três
  contêineres (Arch, Debian, Fedora) instalam como usuária comum.

---

## 1. O roteiro de quarenta minutos, sem o bloco B1  (~30 min)

[`PROVA-NO-PLASTICO-01`](2026-08-19-PROVA-NO-PLASTICO-01-o-roteiro-de-quarenta-minutos-com-o-controle-na-mao.md)
— **nada desta leva foi visto em hardware.** A piscada, o `PS + R3`, o carimbo
da ponte e a recusa do rumble foram todos construídos com dublê.

O bloco B1 já está feito. Sobram o A (a piscada nas cinco cores, nos dois
transportes, com a Steam aberta e fechada) e o C.

## 2. Abra o Grim Fandango uma vez  (~3 min)

Preciso ler o `wm_class` real dele com o jogo de pé. O casamento do perfil
point-and-click está apontando para um palpite (`steam_app_316790`) que nunca
foi conferido contra a janela viva. Abra, me avise, eu leio e conserto.

## 3. Olhe as cinco cores  (~5 min)

Steam Input **azul claro**, Xbox **verde claro**, Modo Nativo **branco**,
máscara DualSense **rosa**, mouse e teclado **âmbar**. Escolhi as duas últimas
sozinha. Se alguma não servir, é trocar uma linha.

---

## 4. Decisão: o «Parar» dentro do Modo Nativo

Medi que `(0,0)` **não** é `None`, e por isso o «Parar» desarmava a cura que
impede o controle de sair vibrando — a porta mais traiçoeira das três, porque
você clica achando que está silenciando.

Hoje ele **solta o par** (volta ao passthrough, e a cura fica armada). A
alternativa é **recusar igual aos outros dois**.

- **Soltar** (o que está no código): você pede silêncio, recebe silêncio do lado
  do Hefesto, e o que o jogo estiver tocando continua — mas o hardware zera na
  saída do modo.
- **Recusar**: coerente com os outros dois gestos, e a frase explica; o preço é
  que um par fixado ANTES do modo continua armado apesar de você ter pedido
  silêncio.

## 5. Decisão: ligar a allowlist do Steam Input sozinho, em quais jogos?

O produto **sabe** ligar (`ligar_no_texto`, testada) e **nunca liga** — mais um
caso de cura escrita e nunca chamada. Liguei nos quatro à mão hoje.

Para virar automático no install, falta você dizer em quais:

- **só nos que têm perfil do Hefesto** — conservador, e cobre o que você joga;
- **em todos os 63 que têm o wrapper** — cobre jogo novo sozinho, mas o Steam
  Input faz um espelho Xbox de CADA controle que vê, inclusive do nosso vpad;
- **só quando a escada pedir** — o mais inteligente e o mais lento: a escada só
  descobre que precisa com o jogo aberto, e a allowlist só se escreve com a
  Steam fechada. Na prática vira "da próxima vez que você abrir".

## 6. Confirmação: "abrir mão de outras distros"

Você disse *"vamos abrir mão de outras distros. só cósmic e gnome por hora"*.
Li de forma conservadora: **parei de investir** em Fedora e Arch, mas **não
arranquei** o que já existe e está testado — inclusive porque foi justamente o
job do Arch que revelou o travamento do install que atingia qualquer distro.

Se a intenção era arrancar, eu arranco. Se era só parar de investir, está feito.

## 7. O PR #114 continua aberto no repo dele

Dezessete commits mais tudo de hoje. Os portões passam. Falta a palavra dele —
ou a sua, se você quiser que eu peça.

---

## O que ficou aberto e NÃO precisa de você agora

- A cadeia *Proton trocado → sem captura → mic mudo* continua **não provada**.
  O que está provado é que nosso pin atropelou sua escolha em três jogos, e isso
  foi curado.
- Nenhuma célula nova foi preenchida no mapa de canais: esta onda foi construída
  com dublê, e preencher sem ensaio é o que o arquivo proíbe. As colunas
  `O JOGO RECEBEU` e `O JOGO REAGIU` existem e esperam o item 1 desta lista.
