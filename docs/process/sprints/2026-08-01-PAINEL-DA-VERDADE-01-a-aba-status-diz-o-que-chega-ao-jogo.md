# PAINEL-DA-VERDADE-01 — a aba Status diz o que chega ao jogo

- **Status:** ENTREGUE em 01/08/2026 (noite) — E1, E2 e a base das E3/E4/E5.
  Ver "O que foi entregue", no fim
- **Status anterior:** PROPOSTA, escrita em 01/08/2026 **para sobreviver à queda da
  sessão**. Tudo o que é preciso para executar está aqui
- **Prioridade:** ALTA — é o requisito dela: *"naquela aba de Status podemos ver
  o funcionamento de tudo, e o funcionamento de lá obviamente impacta o
  funcionamento real do controle na hora de jogar"*
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)
- **Irmã:** [JOGO-COMPLETO-01](2026-08-01-JOGO-COMPLETO-01-os-nove-recursos-dentro-do-jogo.md),
  que trata dos recursos em si. Esta trata do que a TELA afirma sobre eles

## O fato que resume a sprint

A aba Status escreve hoje, com todas as letras: **"Giroscópio: fluindo para o
jogo (~194 Hz)"**.

Esse número é real, e mede o daemon **entregando** o dado ao gamepad virtual.
Ele não mede ninguém **recebendo**. A frase afirma mais do que o dado sustenta —
e foi exatamente essa confusão que produziu, em 01/08, um diagnóstico errado
que quase virou trabalho grande em cima de premissa falsa.

Ela pediu que a aba fosse o painel da verdade. Hoje ela é o painel do que nós
fazemos, o que é outra coisa.

## O levantamento: o que o daemon sabe dizer, recurso a recurso

Medido em 01/08 contra `daemon.state_full`. **Três colunas importam** — a
terceira é a que decide o desenho:

| recurso | campo que existe | "existe/está ligado" ou "está chegando AGORA"? |
|---|---|---|
| giroscópio | `inputs.gyro`; `per_vpad.motion_streaming`; `per_vpad.motion_hz` | **os dois últimos dizem AGORA** — são os únicos campos de todo o payload com noção de recência (`motion_hz` volta a 0.0 se o fluxo parar) |
| touchpad (dedo) | `inputs.touchpad` | só "está tocando" — vem de um leitor evdev paralelo que continuaria desenhando com o vpad morto |
| touchpad (clique) | `per_vpad.touchpad_clicks` | "já chegou desde que o vpad nasceu" — **contador cumulativo**, zera só no `start()` |
| gatilho adaptativo | `per_vpad.trigger_replicas` | idem, cumulativo. **Não existe campo de estado do efeito em vigor** |
| lightbar / player-LEDs | `per_vpad.lightbar_replicas`, `player_led_replicas` | idem |
| vibração | `per_vpad.ff_play_count`; `rumble_ff.plays` | idem |
| microfone | `audio.mic_mudo`, `mic_mudo_desejado`, `bt_mic.*` | leitura real do firmware — mas **nada diz "chega ao jogo"**, e não pode: o mic é PipeWire, não passa pelo gamepad |
| alto-falante | `speaker.{volume,muted}` | diz "o hefesto tomou a posse e mandou este valor". A pergunta "o som está saindo aqui?" é da camada PipeWire, que **o daemon não conhece** |

**E o que a GUI consome hoje:** só o giroscópio tem indicador de "chega ao
jogo" (`texto_motion`). `touchpad_clicks`, `trigger_replicas`,
`lightbar_replicas`, `player_led_replicas` e `output_count` são publicados e
**não têm um único consumidor** em `app/`.

## As duas armadilhas de desenho

**1. Contador cumulativo não é "agora".** Um painel construído sobre
`trigger_replicas` diria "já funcionou uma vez", que é a mentira mais
confortável de todas — ela fica verde para sempre depois do primeiro acerto.

O molde certo já existe no repositório: `emit_hz` em
`core/physical_report_reader.py` — média móvel **com morte por inatividade**
(`_HZ_STALE_S`). E há um carimbo pronto e desperdiçado: `_rumble_visto_em` em
`integrations/uhid_gamepad.py`, com `_RUMBLE_STALE_SEC = 3.0`, que hoje só vira
log e nunca sobe ao payload.

**2. "Chega ao jogo" depende da API que o jogo usa, e isso não é opinião.**
Medido em 01/08: a `libSDL2` 2.30.0 do Ubuntu **não enumera** o gamepad virtual;
a SDL3 3.4.10 que a Steam distribui **enumera**. Uma tela que diga "chega ao
jogo" sem saber qual biblioteca o jogo carregou está adivinhando.

## Entregas

### E1 — o daemon ganha recência, não só contagem

Acrescentar, ao lado de cada contador cumulativo que já existe, um carimbo de
"visto pela última vez em" ou uma taxa com morte por inatividade.

**Onde:** `daemon/ipc_handlers.py`, o bloco por vpad (procure `per_vpad`,
`trigger_replicas`, `touchpad_clicks`); as fontes em
`integrations/uhid_gamepad.py` (as properties dos contadores).

**Molde:** `physical_report_reader.emit_hz`. **Não invente um segundo
mecanismo** — dois jeitos de dizer "agora" no mesmo payload derivam.

**Armadilha nomeada:** `test_emulacao_no_jogo_teclado.py` trava o bloco
`steam_input` por **igualdade exata de dicionário**. É o único bloco do
`state_full` assim — chave nova ali reprova.

### E2 — cada recurso do card diz o seu estado

O card ganha, por recurso, um indicador com três estados possíveis:

| estado | quando | exemplo de frase |
|---|---|---|
| chegando | há dado recente | *"fluindo para o jogo (~194 Hz)"* |
| parado | o caminho existe, sem tráfego | *"pronto — nenhum jogo pediu ainda"* |
| impossível | a máscara ou o modo não suportam | *"a máscara Xbox não tem giroscópio"* |

**O terceiro estado é o mais valioso** e é o que hoje não existe: com máscara
Xbox, o card mostra um sensor apagado como se estivesse quebrado, quando na
verdade a API do Xbox não tem giroscópio. O texto já existe pronto e testado —
`texto_do_custo_da_mascara` em `app/actions/home_actions.py`. **Reuse; não
escreva um segundo.**

**Onde:** `app/widgets/controller_card.py`. O molde de como fazer certo está no
próprio arquivo: `texto_motion` só afirma com `motion_streaming` **e** `hz > 0`.

**Armadilha de orçamento:** o card tem teto de **467px de altura**
(`test_layout_orcamento_altura.py`) e o desenho atual pede 367. Há folga, mas
ela não é infinita — cada indicador novo mede aqui.

### E3 — o alto-falante mostra a camada que decide

Hoje o card mostra a camada 2 (o registrador HID). Quem decide se **sai som** é
a camada 1 (o sink do PipeWire e a rota) — e essa vive no processo da GUI
(`app/audio_saida.py`, `app/mic_monitor.py`), não no daemon.

**A decisão a tomar, e ela é de arquitetura:** ou o dado da rota sobe ao IPC, ou
fica escrito que essa linha é lida pela GUI direto do PipeWire. **As duas são
defensáveis; o que não pode é ficar implícito.**

**Fato medido a registrar:** a rota está LIGADA hoje — o sink padrão do sistema
é o alto-falante do controle, a 40%, com o HDMI guardado como anterior.

### E4 — o mic diz a verdade dele, que é outra

O microfone não passa pelo gamepad e **não pode passar** — medido: existe **uma**
placa ALSA, a do controle físico; um dispositivo `uhid` não tem placa de som.

Então a pergunta certa para o mic não é "chega ao jogo?", é **"a fonte padrão do
sistema é a do controle, e ela não está muda?"**.

**Fato medido em 01/08, e é um defeito ativo:** o mic está **mudo** — 4 s de
captura deram RMS 0,00, silêncio digital absoluto, com o `doctor` apontando
estado persistido do WirePlumber. **A tela não diz isso.** Ela mostraria o mic
como presente enquanto ele não capta nada.

**Onde:** o card já lê o nível pelo `MicMonitor` (fora do IPC, como 3º argumento
de `card.update`). Falta a linha que diz "a fonte padrão não é esta" ou "está
muda no sistema".

### E5 — o `doctor` e a tela param de afirmar o que não mediram

Compartilhada com a [JOGO-COMPLETO-01](2026-08-01-JOGO-COMPLETO-01-os-nove-recursos-dentro-do-jogo.md),
entregas E2 e E3. **Faça as duas juntas** — são a mesma frase em dois lugares, e
consertar um só cria divergência.

## Testes que vão reprovar

| teste | por quê |
|---|---|
| `test_motion_telemetry.py` | trava `motion_streaming`/`motion_hz` e as **strings exatas** de `texto_motion` |
| `test_layout_orcamento_altura.py` | o teto de altura do card. **Não afrouxe** — se estourar, o desenho é que muda |
| `test_emulacao_no_jogo_teclado.py` | igualdade exata do dicionário `steam_input` |
| `test_status_cards*.py`, `test_status_faixa_blocos.py` | a geometria do card, recém-acertada na ALINHA-DUAS-LINHAS-01 |
| `test_doctor_vpad_motion.py` | a saída do bloco do doctor |

Linha de base: `pytest tests/unit -k "status or card or largura or layout or som"`
→ 550 verdes; suíte inteira 6645.

## O que NÃO fazer

- **Não construir o painel sobre contadores cumulativos.** Ver armadilha 1.
- **Não afirmar "chega ao jogo" sem saber qual SDL o jogo carrega.** Ver
  armadilha 2 — foi o erro medido de 01/08.
- **Não tentar levar áudio pelo gamepad virtual.** Não há placa de som ali.
- **Não escrever um segundo texto de custo da máscara.** Reuse a função pura.
- **Não encostar nos dois `Gtk.SizeGroup`** que alinham as duas linhas do card —
  são a entrega dela de 01/08.

---

## O que foi entregue — 01/08/2026, noite

### E1 — o daemon ganha recência

Cada vpad carimba `visto_ha_s` por categoria (`trigger`, `lightbar`,
`player_leds`, `rumble`, `touchpad_click`, `output`) e o `state_full` publica
a IDADE em segundos. **Categoria que nunca aconteceu fica AUSENTE** — "o jogo
ainda não pediu" e "o jogo pediu e parou" levam a ações diferentes de quem lê.

Três decisões que os testes travam:

1. **carimbo, não taxa.** O molde citado na sprint (`emit_hz`) resolve fluxo
   CONTÍNUO; estas categorias são eventos ESPARSOS, e uma taxa sobre evento
   esparso mede o silêncio entre dois acertos, não o acerto. O giroscópio, que
   é fluxo, continua no `motion_hz` — e é por isso que ele não tem carimbo:
   dois jeitos de dizer "agora" no mesmo payload derivam;
2. **o carimbo vem DEPOIS do guarda de sink.** Uma categoria sem sink termina
   em `return` e não chegou a lugar nenhum;
3. **a idade sai resolvida do vpad**, e não o instante cru: quem lê é a GUI,
   noutro processo, e ela não tem o relógio monotônico do daemon.

### E2 — uma linha, e não cinco selos

**O desenho da sprint (um indicador por bloco) foi descartado por MEDIDA.** As
colunas do Touchpad e da Lightbar têm ~180px na tela dela, e o próprio
comentário do `_montar_touchpad` já registrava que um "sem toque" ao lado do
título fazia a coluna pedir 105px para desenhar um painel de 76.

O que entrou é uma linha só, na faixa larga do topo do card:

```
No jogo agora: giroscópio (~194 Hz), vibração, luz · sem pedido ainda: gatilho, clique do touchpad.
```

Ela responde a pergunta como ela a fez — sobre o CONJUNTO, não sobre cada peça.
E ocupa o lugar ao lado da bateria, que é onde ela pediu o hertz do giroscópio:
a linha da verdade **contém** o hertz, então o `_motion_label` saiu do card
único para não dizer a mesma coisa duas vezes (ele continua sendo o dono do
texto no card compacto).

**Os dois estados que não existiam:**

| situação | a frase |
|---|---|
| máscara Xbox | *"giroscópio e touchpad não chegam ao jogo — o controle de Xbox não tem esses dois. Vibração, luz e gatilho vão."* |
| Modo Nativo | *"o jogo fala direto com o controle — tudo chega."* |

O primeiro é o mais valioso: **seis dos oito perfis dela usam máscara Xbox**, e
até aqui o card mostrava os dois sensores desenhados e sem tráfego —
indistinguível de "quebrado".

### O vocabulário, e por que ele tem teste próprio

`test_a_frase_nunca_afirma_que_o_jogo_recebeu` reprova as frases "o jogo
recebeu", "o jogo está recebendo" e "confirmado pelo jogo". O daemon sabe que
o dado saiu daqui e que alguém escreveu de volta; ele **não** sabe se o jogo
consumiu, porque isso depende de qual SDL o jogo carregou. Foi essa confusão
que produziu o diagnóstico errado de 01/08.

### O teto de altura: 467 caducou, e foi REMEDIDO (não afrouxado)

O card estourou o literal de 467px. A sprint proíbe afrouxar o teste — então
mediu-se, com a janela em 1180x830 e a escala de fonte da sessão:

| condição | faixa que a aba dá |
|---|---|
| frame "Estado" visível | **550px** |
| frame "Estado" escondido (um controle) | **708px** |

**467 já estava defasado ANTES desta leva** — é anterior à
ESTADO-TRES-LINHAS-01, que levou o frame de cinco linhas para três e devolveu
essa altura aos cards sem que ninguém remedisse. Os três arquivos que
repetiam o número foram atualizados para 550 (o pior caso, com o frame na
tela) e cada um carrega a nota datada.

## Uma armadilha NOVA do método, medida aqui

**Uma mordida que troca a ORDEM de duas linhas envenena o `__pycache__`.** O
arquivo mutado tem o MESMO tamanho do original; se a mutação, o teste e a
restauração couberem no mesmo segundo, o par `(mtime, size)` não muda e o
Python considera o `.pyc` **mutado** válido. Os testes seguintes rodam contra
código que já não está no disco — e reprovam sem defeito nenhum.

Custou uma investigação de dez minutos, com um `traceback` mostrando um
`if ...:` chamando uma função que não estava naquela linha. **O laço de
mordidas passou a apagar `__pycache__` ao restaurar.**

## O que ficou de fora, e por quê

- **E3 (a camada do PipeWire no alto-falante)** e **E4 (o mic mudo)** dependem
  da decisão de arquitetura que a própria sprint levanta — se o dado da rota
  sobe ao IPC ou se a linha é lida pela GUI direto do PipeWire. A E1 desta
  entrega é a fundação dos dois, e a SOM-ROTA-01 é onde a posse do áudio já
  vai ser mexida: fazer as duas juntas evita mexer duas vezes na mesma regra;
- **E5 (o `doctor`)** é compartilhada com a JOGO-COMPLETO-01, e a sprint manda
  fazer as duas juntas — está lá.
