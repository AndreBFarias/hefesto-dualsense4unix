# Leva de 26/07/2026 — o que falta, depois do rollback

> **A frase que define o escopo**, dita pela mantenedora depois de olhar a tela:
>
> > "veja os elementos como analógicos, área do mic, os botões do dsx como
> > triângulo x bola minúsculos, o desalinhamento dos analógicos, a área do mic
> > que deveria ficar à direita dos analógicos. no caso era ali que era pra
> > mexermos apenas."
>
> A leva da madrugada mexeu em muito mais do que isso. É por causa disso que
> existe este índice.

## Como esta leva nasceu

Não de uma auditoria. Nasceu de um rollback. Na madrugada de 26/07 saiu uma leva
de quinze commits e uma versão, `v0.1.2`. Pela manhã ela abriu a janela, olhou, e
disse quatro coisas:

| # | O que ela disse | O que isso quer dizer |
|---|---|---|
| 1 | "interface tá quebrada e na hora do jogo tá um caos legal" | O que ela viu na tela não é o que ela esperava ver |
| 2 | "agora na hora de jogar o jogo o perfil do controle muda e sai as configs que eu deixei" | **A mais grave** — desfaz trabalho que ela já tinha feito |
| 3 | "agora eu não sei quando é pra ativar entrada steam e quando não é. pensei que tivéssemos superado isso" | Uma resposta que ela já dava por resolvida voltou a faltar |
| 4 | "era ali que era pra mexermos apenas" | O escopo autorizado era a faixa de baixo do card da aba Status. Foi extrapolado |

A árvore dela foi então devolvida ao estado do início da sessão. É desse ponto
que esta leva parte.

## O rollback: o que ele fez, e o que ele NÃO fez

Isto é o mais importante deste documento, porque é o que costuma dar medo:
**nada foi perdido.** Medido agora, na árvore dela:

```
git merge-base --is-ancestor restauro/inicio-da-sessao main   →  verdadeiro
git merge-base restauro/inicio-da-sessao main                 →  4dd4652
git rev-list --count restauro/inicio-da-sessao..main          →  15
```

Traduzindo:

- A sua árvore está no ramo **`restauro/inicio-da-sessao`**, no commit **4dd4652**
  (25/07, 22:36). É esse código que está rodando na sua máquina agora.
- A leva da madrugada está inteira no ramo **`main`**, no commit **84d9f4e**,
  **quinze commits à frente**, e a tag **`v0.1.2`** aponta para `a46941d`, dentro
  dela.
- O commit em que você está é **ancestral direto** de `main`. Ou seja: o rollback
  foi uma **troca de ramo**, não um `revert` e não um `reset --hard`. Nenhum
  commit foi reescrito, nenhum trabalho foi apagado, nada precisa ser refeito do
  zero. O que a madrugada escreveu está guardado e pode voltar peça por peça,
  pela porta certa, quando cada peça tiver documento e caixa de validação.

A diferença entre os dois lados, medida: **60 arquivos, 8.902 linhas inseridas e
543 removidas**.

## O que a madrugada entregou, e onde está

Tudo abaixo está em `main`, não na sua árvore.

| commit | o que entregou |
|---|---|
| `d1177c2` | **PLAYER-LED-01** — o número que o jogo atribui passa a chegar ao controle físico |
| `0c08e77` | **CONTAGEM-01** — a janela deixa de dizer "dois" com quatro controles na mesa |
| `bc827cb` | a aba Status dizia quatro e **desenhava** dois (defeito criado pelo conserto anterior) |
| `ef4b8bc` | **faixa de microfone permanente** no rodapé da aba Status + **SLOT-JOGADOR-01** (os dois números de jogador que nunca se falaram) |
| `b39fec9` | **VÃO-01** — os botões passam a ocupar o vão vertical das abas |
| `9c944a8` | simetria do instalador: o ciclo `uninstall`+`install` desligava **seis** curas de módulo em silêncio |
| `84d9f4e` | conserto do `doctor --fix-mic`, que aplicava a cura que a própria medição tinha refutado |
| `a46941d` | **release `v0.1.2`** |
| `3a41cdf`, `6f15759`, `a3b5b63` | a CI estava vermelha havia cinco commits; typelib parcial derrubava a coleta em vez de virar skip |
| `52e4c4c`, `d2cc854` | a premissa da camada 2 do microfone caiu por medição — registrada em documento |
| `10739bd`, `c98efd7` | AUTO-02, AUTO-03 e AUTO-04 materializadas; nove sprints que mentiam o próprio estado |

Três dessas entregas são exatamente as que você viu e reprovou: **a faixa do
microfone que mudou de lugar** (`ef4b8bc`), **os dois números de jogador**
(`ef4b8bc`) e **os botões ocupando o vão** (`b39fec9`).

## Por que a quebra não foi pega antes de chegar em você

Não foi azar. São três buracos medidos, e os três têm o mesmo formato.

1. **O checklist de validação em hardware tem 43 caixas e zero marcadas.**
   Medido: `grep -c -- "- [x]"` = 0 e `grep -c -- "- [ ]"` = 43 em
   [`2026-07-25-CHECKLIST-validacao-em-hardware.md`](2026-07-25-CHECKLIST-validacao-em-hardware.md).
   O próprio `CHANGELOG.md:81-85` declara a seção "Sem validação em hardware", e o
   índice anterior fecha com "Nada desta leva noturna foi visto em hardware".

2. **MIC-FAIXA-01, SLOT-JOGADOR-01 e VÃO-01 não têm documento de sprint nenhum.**
   Medido: `grep -rn "MIC-FAIXA-01\|SLOT-JOGADOR-01\|VAO-01" docs/` devolve
   **zero** linhas. Os três identificadores existem só na mensagem do commit
   `ef4b8bc` e dentro do código (por exemplo
   `src/hefesto_dualsense4unix/app/widgets/segmented_selector.py:241`). Não havia
   documento dizendo o que era esperado, então **não havia caixa para você
   reprovar item por item**. A única coisa que pegou a quebra foi você olhar a
   tela.

3. **O desenho exato que você pediu para a aba Status não está escrito em lugar
   nenhum.** Medido: `grep -rn -iE "direita dos anal|desalinhamento|triangulo"
   docs/` devolve **zero** linhas. O mais próximo é um parágrafo genérico em
   [`2026-07-25-LEGIBILIDADE-01`](2026-07-25-LEGIBILIDADE-01-texto-legivel-alvo-clicavel.md)
   (linhas 116-126) que pede para *agrupar* microfone, lightbar e analógicos — e
   a madrugada fez o contrário, **separou**, mandando o microfone para o rodapé
   (`CHANGELOG.md:70-72`). A caixa 138 do checklist ficou pedindo uma coisa que o
   código entrega ao contrário, e ninguém percebeu porque a caixa nunca é
   marcada.

**A regra de método que este episódio deixa:** mudança que a pessoa vê na tela
não entra sem caixa escrita **antes** do código. Um pedido que não está escrito é
um pedido que a próxima leva vai extrapolar de novo.

## A lista completa do que falta, por prioridade

### Crítico — desfaz ou impede o seu trabalho

| # | o que falta | onde está medido |
|---|---|---|
| 1 | **O perfil muda ao abrir o jogo e as configurações que você deixou saem.** Sua queixa 2 | `profiles/autoswitch.py:237` chama `_sincronizar_modo_jogo_padrao` **antes** do cadeado, de propósito, e `daemon/lifecycle.py:1812` registra por escrito que o cadeado não é consultado nesse caminho. `profiles/manager.py:200-203`: `activate` reaplica gatilhos, LEDs, teclado e máscara de emulação por cima do que você deixou. Journal desde 25/07 18:00: **12** `profile_mode_aplicado` e **10** `modo_jogo_padrao_solto` |
| 2 | **Não há na tela nenhuma frase que responda quando ligar a entrada Steam.** Sua queixa 3 | O botão só oferece **desligar**. O "dá para desfazer" prometido no tooltip de `gui/main.glade:1881` não existe: `remove_appid_from_steam_input_allowlist` está definida em `integrations/steam_launch_options.py:821` e tem **zero** chamadores em `src/` (medido) |
| 3 | **A rede de segurança do Steam Input está parada.** | Medido agora: `hefesto-steam-input-guard.timer` está `ActiveState=active`, mas com `NextElapseUSecMonotonic=infinity` e último disparo em 25/07 23:43:05. Há mais de cinco horas o guarda não roda |
| 4 | **As 43 caixas do checklist de hardware, todas vazias.** | `2026-07-25-CHECKLIST-validacao-em-hardware.md:34-181` |
| 5 | **O escopo que você autorizou está invertido em relação ao que você pediu.** | `controller_card.py:693` empacota o microfone dentro da coluna de sensores, e essa coluna entra **antes** dos sticks (`:700` contra `:702`). Medido na tela: microfone em x=116, analógicos em x=203 — ele está à **esquerda**, o oposto do pedido |
| 6 | **Três mudanças visuais sem documento e sem caixa** (MIC-FAIXA-01, SLOT-JOGADOR-01, VÃO-01) | `grep -rn` em `docs/` → zero linhas |

### Alto — custa tentativa e erro, ou morde numa noite de quatro controles

| # | o que falta | onde está medido |
|---|---|---|
| 7 | **A janela usa três denominadores diferentes para contar controles.** | `app/actions/status_actions.py:1391` e `:1504` usam `len(conectados)` (só DualSense); `:1063` usa `len(conectados) + len(externals)`; `app/actions/home_actions.py:325-331` usa `len(controllers)` com `len(players)`. Com 2 DualSense e 2 externos, os três dão números diferentes na mesma tela. Sobreviveu ao rollback — conferido nesta árvore |
| 8 | **Entrar na exceção de Steam Input de um jogo derruba o co-op sem avisar.** | `daemon/subsystems/gamepad.py:473-475` e `:423-427`. No Mullet Mad Jack o jogador 1 passa a jogar pelo controle físico e os outros três somem |
| 9 | **AUTO-03.1 e AUTO-03.2** — o perfil do jogo nasce em prioridade 0 e perde para os presets de fábrica; o que você acabou de ajustar não entra no perfil novo | [`2026-07-25-AUTO-03`](2026-07-25-AUTO-03-configurar-um-jogo-em-um-clique.md):164 e :193; a própria sprint chama isso de "o defeito histórico desta casa" (:7-10) |
| 10 | **AUTO-03.5 e AUTO-03.6** — cinco botões para o lado Steam e nenhum é "este jogo"; três portas para o mesmo interruptor | `2026-07-25-AUTO-03`:271 e :295; complemento em `2026-07-25-AUTO-02`:250 |
| 11 | **AUTO-02 e AUTO-04** — o instalador fecha a Steam duas vezes e o terceiro passo vira uma corrida; 53 capacidades que só existem no terminal | [`AUTO-02`](2026-07-25-AUTO-02-uma-janela-de-steam-nao-tres.md), [`AUTO-04`](2026-07-25-AUTO-04-o-que-so-existe-no-terminal.md) |

### Médio — abertas, sem urgência

| # | o que falta | onde |
|---|---|---|
| 12 | **IDENT-01** — um controle, duas identidades (o 8BitDo muda de MAC ao mudar de modo e vira dois controles no registro) | [`2026-07-25-IDENT-01`](2026-07-25-IDENT-01-um-controle-duas-identidades.md) |
| 13 | **MÁSCARA-01** — como este controle aparece nos jogos. Depende de IDENT-01 | [`2026-07-25-MASCARA-01`](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) |
| 14 | **MIC-BT-01** — o medidor do microfone por Bluetooth | [`2026-07-25-MIC-BT-01`](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) |
| 15 | **PLAYER-LED-01, metade da entrega 4** — o buraco do sinal de jogo, declarado em aberto no próprio documento | [`2026-07-25-PLAYER-LED-01`](2026-07-25-PLAYER-LED-01-o-numero-do-jogo-chega-ao-controle.md):137-141 |
| 16 | **RUMBLE-PRESO-01 sem documento** — existe só como duas linhas de commit | `2026-07-25-INDICE-leva-quatro-controles.md`:112-114 |
| 17 | **Os outros vãos da interface** — 307 px de preto abaixo dos cards da aba Status com um ou dois controles, e 618 px na aba Gatilhos que empurram "Aplicar em L2/R2" e "Desligar" para 830 px de distância do "Modo:" | `gui/main.glade:503-513`, scroller com `vexpand=True` |

### Fora do escopo, por decisão

- **As seis sprints de sala limpa** (CR-01 a CR-06). Decisão dela, mantida.
- **Arquitetura**: camadas de saída, broker, BlueZ, DKMS, initramfs. Nada disso
  muda uma noite de jogo.
- **Reentregar a leva da madrugada como estava.** Foi ela que você mandou tirar.
  O que sobrevive volta pela porta certa: a contagem volta como sprint 4, com
  caixa escrita antes. O resto só volta se você pedir.
- **Qualquer release nesta leva.**

## As sprints desta leva, em ordem de ataque

```
STATUS-SIMETRIA-01   a aba Status, e SÓ ela          ← o único escopo autorizado
   │
PERFIL-JOGO-01      o que você deixou continua lá   ← o de maior impacto
   │
STEAM-INPUT-01   uma frase responde a pergunta   ← depende de uma medição
   │
CONTAGEM-E-COOP-01   um número só, e um aviso antes

PROVA-DE-TELA-01     dez minutos de olho             ← última a construir,
                                                       PRIMEIRA a usar
```

| sprint | prioridade | estado | como você valida |
|---|---|---|---|
| [**STATUS-SIMETRIA-01**](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md) — a faixa de baixo do card, do jeito que você pediu | primeira | ABERTA | de olho, em dois minutos, sem terminal |
| [**PERFIL-JOGO-01**](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) — as configurações que você deixou continuam depois de abrir o jogo | crítica | ABERTA | com um jogo aberto, item por item contra um papel |
| [**STEAM-INPUT-01**](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) — a tela diz quando ligar a entrada Steam, e dá para desfazer | alta | ABERTA | lendo uma frase e decidindo sozinha |
| **CONTAGEM-E-COOP-01** — um número só na janela inteira, e aviso antes de derrubar o co-op | alta | ABERTA — **sem documento ainda** | com os quatro na mesa |
| **PROVA-DE-TELA-01** — a folha de dez minutos que precede qualquer leva | obrigatória | ABERTA — **sem documento ainda** | ela é a própria validação |

> **Duas linhas sem documento, registradas em vez de parecerem prontas.**
> CONTAGEM-E-COOP-01 e PROVA-DE-TELA-01 existem por enquanto só como as seções 4
> e 5 abaixo. É exatamente o buraco que causou o rollback — sprint sem documento
> é sprint sem caixa de validação —, então fica escrito aqui até ganharem arquivo
> próprio. **Nenhuma das duas entra em código antes disso.**

### 1. STATUS-SIMETRIA-01 — a aba Status, e só ela

**Por que é a primeira.** Não porque seja a mais grave — não é. É a primeira
porque é a **única coisa que você autorizou**, e a última coisa que aconteceu foi
eu extrapolar. Entregar exatamente isso, e nada além, é o pagamento da dívida que
causou o rollback. É também a única da lista com risco zero para uma noite de
jogo: um arquivo, a faixa de baixo de um card, e não encosta no daemon que roda
enquanto você joga.

**O que está errado hoje, medido nesta árvore:**

- Os dois analógicos ficam **20 px desalinhados** na vertical, e a causa não é o
  desenho: é o rótulo. `"Analógico Esquerdo (L3)"` quebra em três linhas e
  `"Analógico Direito (R3)"` em duas, por `set_line_wrap(True)` +
  `set_max_width_chars(_TITULO_STICK_MAX_CHARS=10)` em
  `app/widgets/controller_card.py:818-821` (a constante em `:115`, os dois
  títulos em `:851` e `:861`). Nada amarra as duas cápsulas pelo desenho: o
  desenho do L3 cai em y=245 e o do R3 em y=225; o X/Y do L3 em y=319 contra 299.
  Cápsula esquerda com 180 px de altura contra 160 na direita, igual nos dois
  cards.
- Os **16 botões do DSX** (triângulo, X, bola, quadrado e os outros) têm 20x20 px
  reais e **não crescem com a escala de fonte** — é pixel cru em
  `controller_card.py:97` (`GLYPH_SIZE: Final[int] = 20`), passado em `:882`. O
  A/B com escala de fonte 0 e 3 devolveu os mesmos 20x20. O grid inteiro ocupa
  86x86 px num card de 931x382: **9,2% da largura** do card para os dezesseis
  botões.
- O **microfone está à esquerda** dos analógicos, o oposto do que você pediu
  (`controller_card.py:693`, `:700` contra `:702`; medido: microfone em x=116,
  analógicos em x=203).
- Há **448 px de vazio** no meio do card, entre o fim dos sticks (x=369) e o
  começo do grid de botões (x=817, ancorado à direita em `:706-708`). É
  exatamente a largura que falta para os analógicos e os botões crescerem.

**As entregas:**

1. Ordem nova da faixa de baixo:
   `[ Touchpad / Lightbar / Alto-falante | Analógico Esquerdo | Analógico Direito | Microfone | botões 4x4 ]`
   — microfone **à direita** dos analógicos.
2. Os dois analógicos alinhados **pelo desenho**, com um `Gtk.SizeGroup` vertical
   amarrando as duas linhas de título. Encurtar o texto é cinto de segurança, não
   é a cura: se amanhã alguém trocar um rótulo, o degrau volta. O SizeGroup é a
   cura.
3. Botões do DSX maiores e crescendo junto com a escala de fonte, ocupando parte
   dos 448 px que hoje são vazio.
4. Um teste que **morde**: reprova se o Y do desenho do L3 diferir do Y do R3 em
   1 px, se a ordem horizontal não for a de cima, ou se o glifo não crescer
   quando a escala muda. Arrancar o SizeGroup tem de fazer o teste falhar — o
   precedente do rumble, em que o teste passou com a cura arrancada, não pode
   repetir.
5. **Escopo trancado:** nada fora da faixa de baixo do card da aba Status. Sem
   tocar em Início, Emulação, Gatilhos, Perfis, Sistema, rodapé, abas ou
   instalador.

**Como você valida, de olho, em dois minutos:** abre a aba Status com um
controle. Os dois analógicos na mesma altura, sem degrau, e os X/Y também. O
microfone à direita deles. Lê triângulo, X e bola a um braço de distância.
Aumenta a escala de fonte e vê os botões crescerem junto. Depois abre Início,
Emulação, Gatilhos, Perfis e Sistema: **se alguma coisa mudou de lugar nelas, a
sprint extrapolou e reprova.**

### 2. PERFIL-JOGO-01 — o que você deixou configurado continua lá

**Por que é a segunda, e não a primeira.** Ela é a de maior impacto — a única que
desfaz trabalho que você já fez. Não é a primeira por três razões:

- **O rollback não a causou nem a curou.** Medido:
  `git diff --stat 4dd4652 main` restrito a `profiles/`,
  `daemon/subsystems/autoswitch.py`, `app/draft_config.py` e
  `daemon/subsystems/game_signal.py` devolve **saída vazia** — byte a byte
  idênticos nos dois lados. Isso já estava no ar antes da madrugada e continua no
  ar depois do rollback. Não é corrida contra o relógio; é dívida antiga, que
  pede cuidado e não pressa.
- **É a única que mexe no daemon que roda enquanto você joga.** Errar aqui não é
  uma tela feia: é a noite acabar.
- **É a única que não se valida de olho em minutos.** Precisa de jogo aberto,
  alt-tab de verdade e conferência item por item. Não pode ser a coisa que está
  pela metade quando você senta para jogar.

**O que está acontecendo, medido no journal da sua máquina** (desde 25/07 18:00):

- **12** `profile_mode_aplicado` e **10** `modo_jogo_padrao_solto`. O flapping é
  visível: 03:06:36, 03:07:23, 03:08:06, 03:08:26, 03:09:08, 03:22:52, 03:30:04 —
  sempre `wm_class=steam_app_3357650` (Pragmata) aplicando e `wm_class=steam`
  soltando. Toda vez que o foco volta para a janela da Steam o Hefesto **solta** o
  modo; volta ao jogo, **aplica** de novo. A causa está declarada no código:
  `profiles/autoswitch.py:237` chama `_sincronizar_modo_jogo_padrao` **antes** do
  cadeado, de propósito, e `daemon/lifecycle.py:1812` escreve que o cadeado não é
  consultado nesse caminho — "e isso é a decisão, não um esquecimento".
- Uma troca de perfil real aconteceu: 25/07 21:19:51,
  `profile_activated name=sackboy_nativo origin=autoswitch priority=80`, pela
  regra própria do jogo. E `activate` não é inócuo: `profiles/manager.py:200-203`
  chama `apply` (gatilhos e LEDs), `apply_keyboard` e `apply_emulation` — reaplica
  gatilhos, lightbar, teclado e máscara de emulação **por cima do que você
  deixou**. É esse o mecanismo do "sai as configs que eu deixei".
- Risco identificado que **não disparou** nesta janela: o cadeado agora cede
  também a `perfil_declara_modo_de_jogo` (`profiles/autoswitch.py:252-261`), e a
  migração de 25/07 18:28 reescreveu os cinco presets no seu disco
  (`~/.config/hefesto-dualsense4unix/profiles/{fps,acao,aventura,corrida,esportes}.json`)
  com `"mode": gamepad/xbox`. Esses presets casam por `window_title_regex`
  frouxo. Se um casar, o cadeado cede e a máscara vira **xbox** sozinha. Não vi
  acontecer no journal — é risco medido no código, não causa medida.

**O que muda a história:** os 12 `profile_mode_aplicado` todos registram
`ligou_gamepad=False`, e `grep -c "ligou_gamepad=True"` na mesma janela dá
**zero** (medido). Nesta janela o modo entrou e saiu 22 vezes, mas **a máscara de
emulação virando não foi medida**. O provado é o flapping e a reaplicação via
`activate`; o resto é mecanismo, não flagrante.

**As entregas:**

1. O modo de jogo entra **uma vez por sessão** e não é solto quando o foco volta
   para a janela da Steam.
2. Nenhuma aplicação automática troca máscara, gatilhos, lightbar ou vibração sem
   gesto seu — o cadeado volta a ceder só à regra específica do jogo
   (`perfil_e_regra_de_jogo`), não a preset casado por título frouxo.
3. Uma linha na aba Status, em português claro: *"Modo jogo ligado às 21:04 por
   Sackboy"*. Você passa a ver o que ele mudou sozinho, quando e por causa de
   qual jogo.
4. Um botão **"Voltar ao que eu deixei"** ao lado dessa linha, que restaura na
   hora, sem fechar o jogo.
5. Teste que morde: arrancar o congelamento ou o botão tem de reprovar a suíte.

**Como você valida:** anota num papel os gatilhos, a cor e a vibração que deixou.
Abre o Pragmata, entra na partida, faz alt-tab para a Steam e de volta três
vezes. Volta ao Hefesto e confere item por item contra o papel. Se mudou, a linha
nova tem de dizer o quê e por quê, e o botão tem de desfazer na hora. Repete
fechando e reabrindo o jogo.

### 3. STEAM-INPUT-01 — uma frase responde quando ligar a entrada Steam

**Por que é a terceira.** É a sua queixa 3, sobre um assunto que você já dava por
resolvido. Vem depois das duas primeiras porque não desfaz trabalho seu e não
impede o jogo de rodar — custa tentativa e erro na hora de jogar. Mas vem antes
da contagem porque a resposta hoje **não existe na tela**, e sem ela toda noite
recomeça do zero.

**O que está errado, medido:**

- Não existe nenhuma frase que diga a regra padrão. O único parágrafo da aba cita
  a entrada Steam uma vez, e só como exceção por jogo. O botão só oferece
  **desligar** — a interface nem sugere que ligar seja opção legítima.
- Os rótulos de estado recebem 15 px de largura contra 23 de mínimo
  (`emulation_steam_input_status_label`, e igual nos de gamepad, gamemode e mic).
  Hoje o texto é só `—` e já não cabe.
- O "dá para desfazer" prometido no tooltip de `gui/main.glade:1881` **não
  existe**: `remove_appid_from_steam_input_allowlist` está em
  `integrations/steam_launch_options.py:821` e tem **zero** chamadores em `src/`
  (medido agora) — só em `tests/unit/test_steam_launch_options_vdf.py`.
- A rede de segurança está morta: `hefesto-steam-input-guard.timer` está
  `ActiveState=active` mas com `NextElapseUSecMonotonic=infinity` e último
  disparo em 25/07 23:43:05. O estado que você vê **não** é o que o Hefesto acha
  que impôs, e vai mudar sozinho no próximo boot.
- Há um conflito vivo: o `localconfig.vdf` tem `UseSteamControllerConfig "2"` no
  bloco do Pragmata, mas a allowlist
  (`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`) só tem o Mullet Mad
  Jack. Quando o guarda voltar, ele desfaz o Pragmata sem avisar.

**As entregas, nesta ordem:**

0. **Portão da sprint.** Antes de escrever qualquer frase, medir com um jogo
   aberto se a Steam moderna honra o `UseSteamControllerConfig` por jogo com o
   `SteamController_PSSupport` global em `0` (que é como o instalador deixa,
   `scripts/disable_steam_input.sh:265-272`). Se não honrar, a exceção por jogo é
   decorativa e a frase seria promessa falsa na sua tela.
1. A regra em uma frase, no topo do cartão: *"Por padrão a entrada Steam fica
   desligada em tudo. Se UM jogo não responder ao controle, abra o jogo e clique
   aqui — o Hefesto liga só naquele jogo."*
2. Lista **por nome de jogo**, não contagem: "Pragmata — controle entregue pelo
   Hefesto", "Mullet Mad Jack — controle entregue pela Steam".
3. Botão "Desfazer" ligado de verdade em
   `remove_appid_from_steam_input_allowlist`, sem fechar a Steam.
4. Rótulos de estado que cabem.
5. O guarda voltando a ter próximo disparo.

**Como você valida:** lê a frase e decide sozinha, sem perguntar a ninguém. Vê os
dois jogos pelo nome, com o estado legível e inteiro. Clica "Desfazer" num deles
e ele sai da lista na hora. Roda
`systemctl --user list-timers | grep steam-input-guard` e vê um próximo disparo,
não `n/a`.

### 4. CONTAGEM-E-COOP-01 — um número só, e ninguém derruba três jogadores sem perguntar

**Por que é a quarta.** Não destrói trabalho seu e só morde numa noite de quatro
controles. Mas é real e sobreviveu ao rollback — os três denominadores foram
conferidos agora, nesta árvore restaurada: `status_actions.py:1391` e `:1504`
(`len(conectados)`, só DualSense), `status_actions.py:1063`
(`len(conectados) + len(externals)`, no seletor) e `home_actions.py:325-331`
(`len(controllers)` com `len(players)`). Com 2 DualSense e 2 externos, os três
dão números diferentes na mesma tela. E entrar na exceção de Steam Input de um
jogo derruba o co-op inteiro sem aviso (`daemon/subsystems/gamepad.py:473-475` e
`:423-427`).

**As entregas:** um só número na janela inteira; aviso **antes** de entrar na
exceção (*"Este jogo vai receber o controle físico — o co-op de quatro cai para
UM jogador. Continuar?"*) com Cancelar que cancela de verdade; uma linha por
controle na aba Status com número e via, sem depender de `/sys/class/leds` do
vpad, que já provou mostrar o número do kernel e não o do jogo.

**Como você valida:** liga os quatro. Status, Início e seletor têm de dizer
**quatro**. Confere controle por controle que o número aceso é o que a tela
mostra. Abre o Mullet Mad Jack, clica "Este jogo não funciona": o aviso aparece
**antes** de qualquer coisa acontecer. Cancela e confere que os quatro continuam
de pé.

### 5. PROVA-DE-TELA-01 — dez minutos de olho antes de qualquer leva chegar

**Por que é a quinta, e por que mesmo assim é obrigatória.** É a única que você
não sente — não muda nada na sua tela. Mas é a dívida que causou o rollback: 43
caixas vazias, e três mudanças que você viu e reprovou sem nem ter documento onde
reprovar item por item.

**A entrega é uma folha só, de dez minutos, com seis perguntas** — todas
respondíveis olhando a janela, sem terminal e sem log:

1. A janela diz o mesmo número de controles em todo lugar?
2. O número aceso no controle é o que a tela mostra?
3. O que eu configurei continua lá depois de abrir e fechar o jogo?
4. O microfone está onde eu pedi?
5. Dá para ler os botões do DSX de longe?
6. A tela me diz quando ligar a entrada Steam?

Mais uma regra e um hábito: **mudança visível sem caixa não entra** — toda sprint
que mexe em algo que você vê escreve a caixa antes de escrever o código; e um
print de cada aba guardado junto, porque foi comparando tela que a quebra
apareceu.

**Ela só rende se for adotada antes de as quatro anteriores chegarem na sua
máquina.** Por isso é a última a ser construída e a primeira a ser usada.

## A ordem de ataque, e o porquê

**1 → 2 → 3 → 4, com a 5 valendo antes de qualquer uma delas encostar na sua
árvore.**

O eixo da ordem não é gravidade pura. Se fosse, PERFIL-JOGO-01 seria a primeira.
O eixo é: **primeiro o que reconstrói a confiança e não pode dar errado, depois o
que dá mais retorno e precisa de cuidado.**

- **STATUS-SIMETRIA-01 é primeira** porque é a única coisa que você pediu, custa
  um arquivo, e você aprova ou reprova de olho em dois minutos. Ela também limpa
  a mesa: enquanto ela não sair, qualquer outra entrega parece de novo eu
  decidindo sozinho o que é importante.
- **PERFIL-JOGO-01 é segunda** porque é a de maior impacto, mas o rollback
  provou que ela não é urgência da madrugada — os arquivos que decidem perfil são
  idênticos nos dois lados. Ela ganha o resto da noite de trabalho, não os quinze
  minutos entre duas coisas.
- **STEAM-INPUT-01 é terceira** porque a resposta que falta é uma frase, mas
  essa frase depende de uma medição que ninguém fez ainda (o portão do item 0).
  Colocá-la antes seria arriscar escrever na sua tela uma regra que a Steam não
  cumpre.
- **CONTAGEM-E-COOP-01 é quarta** porque, das quatro, é a única que não custa
  nada enquanto você joga com um ou dois controles — e porque o aviso de co-op
  mora no mesmo cartão que a sprint 3 acabou de mexer. Fazer as duas nesta ordem
  evita abrir o mesmo cartão duas vezes.

**Se você for jogar antes de a sprint 2 sair:** nas últimas doze horas o único
perfil que trocou sozinho foi o `sackboy_nativo`, às 21:19:51 de 25/07, pela
regra própria do jogo. O flapping de modo é do Pragmata, e nas 12 vezes
registradas ele saiu com `ligou_gamepad=False` — a máscara virando não foi vista.
Isso não é garantia; é o que está medido.

## O que foi descartado, e por quê

- **A granularidade de fatiar a aba Status em três micro-sprints** (uma para o
  alinhamento, uma para os glifos, uma para o microfone). O instinto é bom, mas
  três sprints mexendo nas mesmas trinta linhas do mesmo arquivo significam três
  reconstruções e três reinícios da sua janela para uma conferência que você faz
  de uma vez só, com o olho. Fundidas em STATUS-SIMETRIA-01 — e a melhor ideia
  delas foi enxertada: **alinhar pelo `Gtk.SizeGroup`, não encurtando o texto**.
  Consertar o rótulo faz o degrau voltar no dia em que alguém trocar uma palavra.
- **Reentregar a leva da madrugada como estava** — PLAYER-LED-01, CONTAGEM-01,
  MIC-FAIXA-01, SLOT-JOGADOR-01 e VÃO-01. Foi essa leva que você mandou tirar. A
  contagem volta como sprint 4, com caixa escrita antes; o resto só volta se você
  pedir.
- **AUTO-03.1 e AUTO-03.2** do caminho crítico. São a mesma queixa 2 por um
  mecanismo diferente, e exigem mexer no formato e na prioridade dos perfis —
  risco alto. PERFIL-JOGO-01 cura o mecanismo que está **medido acontecendo** na
  sua máquina. Se depois dela você ainda vir config sumindo, essas duas são a
  próxima leva, imediatamente.
- **Os outros vãos da interface** (item 17 da lista). Irritam de verdade, mas
  mexer neles agora é exatamente a extrapolação que você reclamou. Voltam à mesa
  depois que você aprovar a sprint 1 — e só se você quiser.
- **Unificar as três portas do Steam Input e os cinco botões do lado Steam**
  (AUTO-03.5 e AUTO-03.6) por inteiro. STEAM-INPUT-01 entrega a frase, a
  lista por nome e o desfazer — o que você sente. Unificar as portas é conserto
  de encanamento e pode vir depois, sem você ver.
- **Tudo que é arquitetura** e **qualquer release nesta leva**.

## O que NÃO foi medido

Escrito aqui de propósito, para não virar afirmação por omissão.

- **Se a Steam honra `UseSteamControllerConfig` por jogo com
  `SteamController_PSSupport` global em `0`.** Se não honrar, a exceção por jogo é
  decorativa e a frase da sprint 3 seria mentira na sua tela. Por isso virou o
  item 0 daquela sprint, com jogo aberto.
- **A máscara de emulação virando sozinha.** O flapping do modo foi medido (12
  aplicações, 10 solturas) e a reaplicação via `activate` está no código
  (`profiles/manager.py:200-203`). Mas os 12 registros dizem
  `ligou_gamepad=False` e não há nenhum `ligou_gamepad=True` na janela. Mecanismo
  provado; flagrante não.
- **Os presets migrados casando na prática.** O risco está no código
  (`profiles/autoswitch.py:252-261` mais os cinco JSON no seu disco), mas nenhum
  casamento de `window_title_regex` foi observado no journal desta janela.
- **Nada desta leva foi visto em hardware**, porque nada dela foi construído
  ainda. As 43 caixas do checklist continuam vazias, e é justamente isso que
  PROVA-DE-TELA-01 existe para mudar.
- **Uma das três propostas que alimentaram esta síntese não chegou inteira.** Se
  ela tinha algo que não está aqui, ficou de fora por ausência, não por decisão.

## Estado

Todas as sprints desta leva nascem **ABERTAS**. Este índice é atualizado conforme
cada uma fecha, com o commit que a fechou — e nenhuma fecha sem a caixa de
validação escrita **antes** do código.
