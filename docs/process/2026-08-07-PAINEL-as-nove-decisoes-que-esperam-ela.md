# Painel de decisões — 07/08/2026

Nove coisas esperam você. Seis fecham lendo, uma pede a janela aberta, uma pede o
controle na mão, uma pode esperar. Responda assim: `1-a, 2-c, ...`

---

## RESPONDER AGORA

### 1. Onde, na aba Perfis, mora a caixinha que TIRA um jogo do Steam Input?

**Contexto:**
- O botão "Este jogo não funciona" (aba Sistema) marca e não desmarca. O aviso está
  na tela hoje: *"ainda não existe um botão para desmarcar"*.
- O código já existe (`remove_appid_from_steam_input_allowlist`) e já tem linha de
  comando; falta só o lugar na janela. A semântica é a que você mediu em 06/08.
- O índice de 06/08 já fixou a aba (Perfis). Falta o ponto exato.

**Opções:**
- **a) No editor do perfil, logo abaixo do jogo escolhido** — a marca é por jogo, e é
  ali que o jogo já tem nome. *Recomendada: o desfazer nasce onde você escolheu o jogo.*
- **b) Uma coluna na lista de perfis** — você vê quais jogos estão marcados sem abrir nada.
- **c) Um botão no rodapé, ao lado do Salvar** — age sobre o perfil selecionado.

**Sem sua palavra:** a janela continua avisando que não dá para desfazer, e a JOGO-01/E3
fica aberta com o código pronto na gaveta.

---

### 2. As três palavras da aba Gatilhos

**Pergunta:** como se chamam, no botão, o "Personalizado (avançado)", o "Arco (Bow)" e o
"Arma (Weapon)"?

**Contexto:**
- São 19 modos na grade. Dezoito cabem; "Personalizado (avançado)" tem 24 caracteres
  contra 22 que a grade aguenta encolhida — quebra a linha e estica a grade inteira.
- "Arco" é ambíguo em português; "Arma" não separa das outras três armas da lista.
- É texto de tela e é reversível: seus perfis abrem igual, o disco guarda outro nome.

**Opções (para o modo comprido):**
- **a) "Montar do zero"** — cabe, é verbo do seu vocabulário e diz o que o modo faz.
  *Recomendada: é a única que não pede nenhum ajuste de largura.*
- **b) "Personalizado"** — cabe e mantém a palavra de hoje; perde a dica de que ali se monta.
- **c) "Avançado"** — cabe com folga, mas repete o nome da seção Avançado da aba Sistema.
- **d) Outro nome seu** — até 22 caracteres; eu meço antes de aplicar e devolvo a foto.

Para os outros dois, a sprint sugere **"Arco de flecha (Bow)"** e **"Disparo (Weapon)"** —
diga só se discordar.

**Sem sua palavra:** o rótulo segue quebrando a linha e a isenção
`PENDENCIA_DE_LARGURA = {"Custom"}` segue no teste, escondendo qualquer rótulo novo.

---

### 3. Onde mora o interruptor do microfone por Bluetooth?

**Contexto:**
- Você pediu em 03/08. A ponte existe e o subsistema sobe, mas **não há uma linha dela
  no `main.glade`** — verifiquei: só a variável de ambiente `..._BT_MIC=1`.
- Com quatro controles por rádio o medidor simplesmente some, e "sumiu" é indistinguível
  de "não existe".

**Opções:**
- **a) No card do controle, junto do medidor** — ligar fica onde o efeito aparece; com
  quatro controles são quatro interruptores. *Recomendada: é onde o nível já aparece.*
- **b) Na aba Emulação, junto do "Microfone do DualSense" que já existe** — um lugar só,
  longe de onde o nível aparece.

**Sem sua palavra:** as caixas 2, 3 e 4 da MIC-BT-01 não têm onde nascer.
*Ligar por padrão é decisão à parte — ela espera a medição dos quatro no rádio (abaixo).*

---

### 4. O bloco "ESCOPO" fica no `LICENSE`, ou sai dele?

**Contexto:**
- Hoje o bloco ocupa as linhas 1-19 do `LICENSE`, antes do texto MIT. Foi posto ali de
  propósito, e o preço foi registrado para você pesar.
- O `NOTICE` já tem uma seção "ESCOPO DESTE ARQUIVO" dizendo a mesma coisa, com a
  auditoria arquivo por arquivo.

**Opções:**
- **a) Sai do `LICENSE` e o `NOTICE` fica sendo o dono da ressalva** — o rótulo de licença
  volta à vitrine do GitHub. *Recomendada: o `NOTICE` já carrega esse texto, e a vitrine
  é o que faz alguém clicar agora que o alvo é a comunidade.*
- **b) Fica no topo** — quem abre o arquivo lê a ressalva antes do juridiquês; o GitHub
  provavelmente segue mostrando "View license" em vez de "MIT".
- **c) Desce para o rodapé** — o rótulo volta, e a ressalva vira o que a sprint chama de
  "ressalva depois do juridiquês, que ninguém lê".

**Sem sua palavra:** o repositório continua sem rótulo de licença na vitrine.

---

### 5. Que licença o Hefesto tem — e as curvas medidas por você seguem a mesma?

**Contexto:**
- É a última caixa `[ ]` da CR-01, aberta desde 25/07. Sua fala de 06/08 ("ficar pra
  comunidade") confirmou o rumo, não escolheu a licença.
- A licença das curvas (CR-06) é a mesma pergunta com outras palavras — respondo as duas
  com uma frase sua.
- Hoje, com uma contribuidora só, trocar é uma linha; com o projeto crescido exige a
  concordância de todos. **A própria CR-01 diz que isto NÃO bloqueia as outras sprints.**

**Opções:**
- **a) MIT no código + CC0 nas curvas** — nada publicado quebra, e o dado entra em
  qualquer projeto sem pedir permissão. *Recomendada: é o que faz a curva ser adotada,
  que é o objetivo declarado da CR-06.*
- **b) MIT nos dois** — quem usar a curva tem de nomear o Hefesto.
- **c) Copyleft (GPL/LGPL) nos dois** — quem distribuir derivado devolve o fonte; coerente
  com os DKMS que já viajam em cinco dos sete artefatos.
- **d) Dupla** — MIT no código, copyleft nos dados.

**Sem sua palavra:** a CR-01 e a CR-06 ficam abertas, e cada contribuidor novo encarece
a troca.

---

### 6. A fonte +3 está aceita? (precisa da janela aberta, não do controle)

**Contexto:**
- O código está em produção: `app/theme.py:ESCALA_PADRAO = 3`, com o comentário dizendo
  "medido e aprovado no orçamento de largura e altura".
- Só que o critério que a própria sprint declara não é o orçamento: é **você ler o rodapé
  sem se aproximar da tela**. Essa caixa nunca foi marcada.

**Opções:**
- **a) Aceito o +3** — a LEGIBILIDADE-01 fecha.
- **b) Quero mais** — o teto seguro é +8; acima disso a janela deixa de caber em 1080p.
- **c) Volto para +2** — a sprint registra +2 como o degrau seguro.

**Sem sua palavra:** a sprint fica aberta indefinidamente com o código já rodando, e
ninguém sabe se a queixa original ("fontes minúsculas") foi resolvida.

---

### 7. Os controles externos ganham lugar próprio na partida? (E3/E4 do LUGAR-À-MESA-01)

**Contexto:**
- Você mediu em 06/08 às 22h40: três controles ligados, os três no jogador 1 — a meta e a
  realidade se contradizem. Há uma decisão sua de 19/07 dizendo o contrário, em três
  lugares do código; desempatar duas falas suas é seu.
- O preço: quem segurar o Pro vê botão de PlayStation na tela até a MÁSCARA-01 existir; a
  vibração dos externos é a única parte do desenho **sem prova**; e o rádio ganha tráfego
  na direção do firmware mais frágil da mesa.

**Opções:**
- **a) Autorizar E3 e E4 agora** — cada controle vira jogador; você aceita o botão errado
  na tela e a vibração sem garantia.
- **b) Autorizar só depois da máscara por controle** — ninguém vê botão errado, e a queixa
  dos três no jogador 1 fica de pé por mais uma leva inteira.
- **c) Manter o veto** — o produto para de afirmar o que não entrega; os externos ganham
  nome e número honestos, mas chegam ao jogo como hoje.
- **d) Só para o Pro, sem o 8BitDo** — reduz risco, mas cria regra por aparelho, que é o
  que você derrubou ("a cura tem de ser regra, não registro").

**Sem sua palavra:** E3 e E4 não começam, e o jogo continua vendo três controles como
jogador 1. *Mesmo um "sim" hoje espera a medição dos quatro no rádio (abaixo).*

---

## PRECISA DO CONTROLE NA MÃO

### 8. Qual lista come a próxima sessão de hardware?

**Contexto:**
- Existem duas listas concorrentes para o mesmo hardware e a mesma sessão sua: as **31
  caixas do CHECKLIST de 25/07** (conferi: zero marcadas em treze dias) e as **41 medições
  do protocolo de 06/08**.

**Opções:**
- **a) O protocolo de 06/08 primeiro** — é descoberta; cada item destrava sprint parada.
  *Recomendada: o aceite ficaria contaminado se o protocolo mudar o produto no meio.*
- **b) O CHECKLIST de 25/07 primeiro** — é aceite; confirma que oito sprints entregues
  funcionam na sua mão.
- **c) As duas, nesta ordem** — mais longo.
- **d) Aposentar o CHECKLIST** — assumir que treze dias sem uma caixa marcada é a resposta.

**Sem sua palavra:** as 31 caixas seguem `[ ]` e ninguém sabe se as curas de 25/07 valem
fora do teste.

**As três medições da frente, uma linha cada:**
- **Bluetooth (20 min, e a única cujo pior caso não é "um controle que não funciona"):**
  paro o watchdog, aplico `JustWorksRepairing=confirm`, você re-pareia um controle antes e
  o mesmo depois, e eu leio o journal no instante em que você avisar.
- **Os quatro no rádio com o jogo aberto (pressuposto da decisão 7, hoje SEM PROVA):**
  se o `EVIOCGRAB` segura num Pro e num 8BitDo, se o clone sobrevive à vibração escrita de
  volta, e se o jogo vê três jogadores distintos com e sem o `hefesto-launch`.
- **Mic por Bluetooth sair do opt-in (depende da decisão 3):** com os quatro conectados,
  medir o custo antes de ligar por padrão — ~35% dos reports de entrada, firmware mudo
  entre 55% e 75% do tempo, e disputa do contador de sequência do report `0x32`.

---

## PODE ESPERAR

### 9. A janela do Hefesto fala só português, ou também inglês?

**Contexto:**
- O encanamento de tradução está pronto; o texto é que não passa por ele — 15 dos 18
  arquivos que montam as abas escrevem português direto no widget.
- Três páginas do projeto convidam gente a traduzir, e a tradução não alcançaria quase
  nada. A promessa está falsa há meses.
- Nada disso trava esta semana; o que cresce é a dívida, porque todo texto novo nasce cravado.

**Opções:**
- **a) Português é a língua do produto** — apago o convite dos três documentos e ponho um
  portão. *Recomendada: é o que o produto já é, e assumir é mais honesto.*
- **b) Inglês passa a valer** — uma leva converte 73+ frases em nove arquivos (toca sua
  tela, só fecha com foto antes e depois), e toda sprint de interface fica mais cara.
- **c) Adiar** — a conta cresce a cada leva e a promessa continua falsa.

**Sem sua palavra:** cada sprint de interface decide sozinha se envolve o texto na tradução.

---

## O QUE EU DERRUBEI DA LEVA NOVA

- **"A vibração nasce a 70% sem avisar."** Falso, e medi: a aba Rumble tem os quatro
  botões (Economia 0,3× / Balanceado 0,7× / Máximo / Auto), o multiplicador em régua, e
  `docs/usage/interface.md:74` documenta os valores. A tela diz, e trocar é um clique. Se
  ainda assim quiser outro padrão de fábrica, é uma palavra — não gastei um número com isso.
- **A licença das curvas (CR-06) virou parte da decisão 5**, porque a opção "a mesma do
  projeto" já responde as duas. Uma pergunta a menos, mesma substância.
- **A caixinha do Steam Input** aparecia em duas fontes; é a decisão 1, uma vez só.
- **Os quatro no rádio** aparecia como decisão e como medição; ficou só como medição,
  amarrada à decisão 7.

---

## O QUE EU EXECUTO SEM VOCÊ

Nada abaixo toca as nove perguntas.

- **A bancada de medição inteira (CR-03)**, a maior peça de código do trilho — a própria
  CR-01 escreve que a licença **não é pré-requisito das demais sprints**.
- **A CR-05**: criar `LICENSES/` com o texto canônico e a linha em cada um dos cinco
  alvos. A sprint escreve o remédio inteiro; é trabalho com resposta certa.
- **E0a** — `coop status` passa a imprimir os dois números nomeados ("jogadores pelo
  Hefesto: 1 / controles na mesa: 3, sendo 2 externos"). Com daemon antigo imprime `—`.
- **O teste que a sua medição de 22h40 exigiu** — nenhum par de aparelhos pode acender o
  mesmo número, inclusive o nosso controle virtual. Não existe hoje.
- **E1 e E2** — inventário de externos com guarda de frescor; descoberta unificada,
  normalizador de eixo e reencontro depois do replug, tudo por dublê, sem adoção nenhuma.
  Os cartões na tela eu preparo, mas só fecho com a sua foto antes e depois.
- **As quatro notas datadas da LUGAR-À-MESA-01** — `README.md` e `docs/usage/modos.md`
  dizem que os externos "entram na contagem como jogadores": verdade sobre a luz, falso
  sobre o jogo. As frases ganham data e o que caducou.
- **O portão anti-recaída** — nenhuma das quatro superfícies pode emitir número de jogador
  sem a palavra que o qualifica, porque no Linux quem numera é o jogo.
- **O gêmeo que tira** já está pronto por baixo (`remove_appid_from_steam_input_allowlist`
  + `hefesto-dualsense4unix steam`); assim que você responder a 1, é só pendurar na tela.
