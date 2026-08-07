# painel de decisoes (workflow as-decisoes-que-so-ela-pode-tomar)

- candidatas: 92
- sobreviveram a depuracao: 3

# Painel de decisões — 07/08/2026

Três coisas esperam a sua palavra. Duas fecham hoje com uma frase; uma pode esperar. Abaixo delas, o que eu começo sem resposta nenhuma.

---

## RESPONDER AGORA

### 1. Os controles externos ganham lugar próprio na partida? (E3/E4 do LUGAR-À-MESA-01)

**Pergunta:** o Pro Controller e o 8BitDo passam a entrar no jogo por dentro do Hefesto — cada um virando um jogador de verdade — sabendo o preço que isso cobra?

**Contexto:**
- Você mediu em 06/08 às 22h40: três controles ligados, os três no jogador 1. A meta que você definiu ("cada um controla o próprio personagem") e a realidade se contradizem.
- O que falta não é você querer: é aceitar o preço, que nunca lhe foi mostrado. E há uma decisão sua anterior, de 19/07, dizendo o contrário ("externo não ganha controle virtual"), gravada em três lugares do código.
- Desempate entre duas falas suas é seu. O preço: quem segurar o Pro vê botão de PlayStation na tela do jogo (A/B e X/Y trocados no plástico) até a MÁSCARA-01 existir; a vibração dos externos é a única parte do desenho sem prova; e o rádio ganha tráfego novo na direção do firmware mais frágil da mesa, o clone.

**Opções:**
- **Autorizar E3 e E4 agora** — cada controle ganha lugar na partida; você aceita o botão errado na tela e a vibração sem garantia.
- **Autorizar só depois da máscara por controle** — ninguém vê botão errado, e a queixa dos três no jogador 1 fica de pé por mais uma leva inteira.
- **Manter o veto** — o produto para de afirmar o que não entrega e os externos ganham nome e número honestos, mas chegam ao jogo como hoje.
- **Autorizar só para o Pro, deixando o 8BitDo de fora** — reduz o risco no firmware frágil, mas cria regra por aparelho, que é justamente o que você derrubou ("a cura tem de ser regra, não registro").

**Sem a sua palavra:** E3 e E4 não começam, e o jogo continua enxergando os três controles como jogador 1 — a queixa de 06/08 fica exatamente onde está.

---

### 2. As três palavras da aba Gatilhos

**Pergunta:** como devem se chamar, no botão, o modo "Personalizado (avançado)", o "Arco (Bow)" e o "Arma (Weapon)"?

**Contexto:**
- São 19 modos na grade. Dezoito cabem no botão; "Personalizado (avançado)" tem 24 caracteres contra 22 que a grade aguenta na janela encolhida — quebra a linha e estica a grade inteira.
- "Arco" sozinho é ambíguo em português (arco de círculo, arco elétrico) e "Arma" não separa das outras três armas da lista. A sprint sugere "Montar do zero", "Arco de flecha (Bow)" e "Disparo (Weapon)".
- É só texto de tela e é reversível: seus perfis (ação, corrida, esportes, pragmata) abrem igual, seja qual for a palavra — o disco guarda outro nome.

**Opções (para o modo comprido):**
- **"Montar do zero"** — cabe, é verbo do seu vocabulário e diz o que o modo faz; é a única que não pede nenhum ajuste de largura. *Recomendada.*
- **"Personalizado"** — cabe e mantém a palavra que está na tela hoje; perde a dica de que ali você monta o efeito na mão.
- **"Avançado"** — cabe com folga, mas repete o nome da seção "Avançado" da aba Sistema.
- **Outro nome seu** — vale qualquer coisa com até 22 caracteres; eu meço antes de aplicar e devolvo a foto da aba.

**Sem a sua palavra:** o rótulo continua quebrando a linha, e a isenção `PENDENCIA_DE_LARGURA = {"Custom"}` segue no teste — qualquer rótulo novo pode se esconder nela sem ninguém notar.

---

## PRECISA DO CONTROLE NA MÃO

Nenhuma destas é decisão de mesa: são medições que só existem com você na cadeira. A fila inteira (41 medições, protocolo pronto) está em `docs/process/estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md`.

- **A primeira da fila, e a única cujo pior caso não é "um controle que não funciona":** com `JustWorksRepairing=confirm` no disco, um re-pareamento legítimo seu ainda completa? Protocolo (20 min): paro o watchdog, aplico a cura, você re-pareia um controle antes e o mesmo controle depois, e eu leio o journal do agente no instante em que você avisar.
- **Só se você autorizar a decisão 1:** os quatro no rádio com o jogo aberto — se o `EVIOCGRAB` segura de fato num Pro e num 8BitDo, se o clone sobrevive à vibração escrita de volta, e se o jogo vê três jogadores distintos com e sem o `hefesto-launch`. É o pressuposto central da E3, hoje SEM PROVA.

---

## PODE ESPERAR

### 3. A janela do Hefesto fala só português, ou também inglês?

**Contexto:**
- O encanamento de tradução está pronto e correto; o texto é que não passa por ele: 15 dos 18 arquivos que montam as abas escrevem português direto no widget.
- Três páginas do projeto (CONTRIBUTING, flatpak.md, troubleshooting.md) convidam gente a traduzir — e a tradução não alcançaria quase nada. A promessa está falsa há meses.
- Nada disso trava trabalho desta semana; o que cresce é a dívida, porque todo texto novo nasce cravado.

**Opções:**
- **Português é a língua do produto** — apago o convite dos três documentos e ponho um portão; é o que o produto já é, e assumir é mais honesto. *Recomendada.*
- **Inglês passa a valer** — uma leva converte 73+ frases em nove arquivos de ação (toca a sua tela, só fecha com foto antes e depois), e toda sprint de interface fica um pouco mais cara.
- **Adiar de novo** — a conta de converter cresce a cada leva e a promessa continua falsa.

**Sem a sua palavra:** o bloco F da PROMESSA-NÃO-CUMPRIDA-01 e a E6 da DOC-VERDADE-02 ficam abertos, e cada sprint de interface decide sozinha se envolve o texto na tradução.

---

## O QUE EU EXECUTO SEM VOCÊ

Tudo abaixo está liberado e não toca nenhuma das três perguntas.

- **E0a** — `coop status` passa a imprimir os dois números nomeados ("jogadores pelo Hefesto: 1 / controles na mesa: 3, sendo 2 externos"); hoje ele só diz "jogadores ativos". Com daemon antigo imprime `—`, nunca `0`.
- **O teste que a sua medição de 22h40 exigiu** — nenhum par de aparelhos pode acender o mesmo número, inclusive quando um deles é o nosso próprio controle virtual. Esse teste não existe hoje.
- **E1** — o inventário de externos passa a ser guardado e publicado com guarda de frescor (sem enumeração nova no caminho quente). A parte visível, os cartões na tela, eu preparo mas só fecho com a sua foto antes e depois.
- **E2** — descoberta unificada, normalizador de eixo e reencontro depois do replug, tudo provado por dublê, sem adoção nenhuma: o co-op continua não pegando ninguém.
- **As quatro notas datadas que a LUGAR-À-MESA-01 deve** — o `README.md` e o `docs/usage/modos.md` dizem que os externos "entram na contagem como jogadores", o que é verdade sobre a luz e falso sobre o jogo. As frases não se apagam: ganham a data e o que caducou.
- **O portão anti-recaída** — nenhuma das quatro superfícies (daemon, CLI, interface, applet) pode emitir número de jogador sem a palavra que o qualifica, porque no Linux quem numera é o jogo, não nós.
