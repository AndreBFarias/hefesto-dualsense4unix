# SOM-02 — o alto-falante que funciona

- **Status:** PROPOSTA (nada de código nesta rodada — é o documento que decide o
  desenho antes de mexer no produto)
- **Prioridade:** MÉDIA-ALTA — não há defeito aberto, mas há um método de
  protocolo com superfície pela metade e um bloco de tela que só sabe dizer
  "não sei"
- **Aberta em:** 29/07/2026, a partir do pedido dela, com um DualSense por USB
  ligado nesta máquina
- **Sucede:** [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md), que
  resolveu o LUGAR do alto-falante na aba Status e registrou por que ele é só
  leitura
- **Relacionada:**
  [MIC-USB-01](2026-07-25-MIC-USB-01-tres-mutes-empilhados.md) (decidiu que o
  `speaker.set` FICA no protocolo e ganha superfície) e
  [MIC-PRESENTE-01](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md)
  (o vizinho de coluna, e o desenho do botão que esta sprint copia)
- **Irmã, aberta na mesma rodada:**
  [SENSOR-VIVO-01](2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md).
  Ela responde pelo caminho do som **até o jogo** (a camada 1, o PipeWire) e
  esta responde pelo **desenho na interface** (a camada 2, o registrador HID).
  As duas mediram o mesmo sink no mesmo dia e chegaram ao mesmo número:
  `Mute: yes` a 40 %. A E5 da SENSOR-VIVO-01 — a faixa dizer que **o sistema**
  mutou, em vez de `"não ajustado"` — é a mesma entrega que a E5 desta página,
  vista do outro lado; entrar uma sem a outra deixa metade da verdade na tela
- **Rodada:** é um dos seis documentos de 29/07; a ordem de leitura está no
  [índice da documentação da v0.3.0](../estudos/2026-07-29-INDICE-a-documentacao-da-v030.md)

## A frase dela, literal

> *"temos que fazer a sprint do autofalante, inclusive, como vamos fazer ele
> funcionar na interface"*

## O fato que resume a sprint

**O alto-falante do controle tem TRÊS camadas de volume, e a janela só alcança
a do meio — que é justamente a única sem leitura e com preço.** Medido ao vivo
nesta máquina hoje: a camada de cima (a rota do PipeWire) está **muda**, com o
volume persistido em 40 %. Um controle deslizante ligado só na camada do meio
seria movido, obedecido pelo firmware, e **nenhum som sairia** — o mesmo enredo
das três camadas empilhadas do microfone, agora do lado da saída.

## O que já existe, medido

| O que | Onde | Estado |
|---|---|---|
| contrato do método | `daemon/ipc_server.py:26` | `speaker.set {volume?: 0-255, muted?: bool, uniq?} -> {status, speaker}` |
| registro no dispatcher | `daemon/ipc_server.py:125` | vivo desde a D4 |
| handler | `daemon/ipc_handlers.py:2506-2543` | valida, escreve, relê e devolve |
| escrita no backend | `core/backend_pydualsense.py:2200-2245` | `set_speaker_volume` |
| leitura do backend | `core/backend_pydualsense.py:2175-2198` | `speaker_state_for` |
| posse por byte | `core/backend_pydualsense.py:532-556` | `set_audio_volumes` |
| devolução da posse | `core/backend_pydualsense.py:557-559` | `release_audio_volumes` — existe no HANDLE e **não** tem porta acima dele |
| publicação no estado | `daemon/ipc_handlers.py:1883-1907` | a chave `speaker` só entra quando o backend responde |
| ponte da janela | `app/ipc_bridge.py:563-607` | `speaker_set`, com o ponto de fiação escrito em `:588-592` |
| bloco na tela | `app/widgets/controller_card.py:1423-1455` | barra + rótulo, sem nenhum controle |
| leitura do payload | `app/widgets/controller_card.py:652-680` | `speaker_do_entry` |
| rótulo sem dado | `app/widgets/controller_card.py:408` | `"não ajustado"` |

**Chamadores do `speaker_set` no produto: nenhum.** A função está exportada em
`app/ipc_bridge.py:652` e não aparece em nenhuma ação da janela nem em nenhum
comando de linha — `cli/app.py:143-168` registra o comando `mic` (com
`mute`/`unmute`/`release`, ver `cli/cmd_mic.py:72-76`) e não há contraparte de
alto-falante. É o mesmo diagnóstico que a MIC-USB-01 fez do `mic.set`, um mês
antes de ele ganhar botão.

## O que o `speaker.set` faz hoje — e as quatro armadilhas medidas

Parâmetros (`daemon/ipc_handlers.py:2520-2530`): `volume` inteiro 0-255 ou
ausente, `muted` booleano ou ausente, `uniq` string ou ausente (ausente = o
controle primário). Resposta (`:2536-2543`): `status` `"ok"` ou `"sem_controle"`
e `speaker` com o estado relido, ou `null`.

As armadilhas abaixo foram **executadas**, com o `set_speaker_volume` real e um
handle de mentira no lugar do controle:

### Armadilha 1 — `speaker.set {}` toma a posse e manda ZERO

```
antes:  volumes=[None, None, None, None]   state=None
speaker.set {}  ->  True
depois: volumes=[0, 0, None, None]  pref=0
estado publicado: {'volume': 0, 'muted': True}
```

A conta está em `core/backend_pydualsense.py:2231-2238`: sem `volume` e sem
preferência guardada, `pref` cai para `0` e o efetivo vai a `0`. Chamada vazia
não é consulta: é "assuma a posse e emudeça".

### Armadilha 2 — `muted: false` antes de qualquer volume não desmuta nada

```
1o clique "mudo":   volumes=[0, 0, None, None]   {'volume': 0, 'muted': True}
depois "desmudo":   volumes=[0, 0, None, None]   {'volume': 0, 'muted': True}
```

Porque o `muted=False` restaura a preferência (`:2236-2237`) — e a preferência é
`0`. Um botão de mudo que seja a PRIMEIRA escrita tranca o alto-falante em zero
e o próprio botão não tem como soltá-lo. Com um volume de verdade antes, o par
funciona: com `volume=180`, o `muted=True` manda 0 e guarda 180, e o
`muted=False` devolve os 180 (medido).

### Armadilha 3 — a escrita é de DOIS bytes, e o roteamento fica de fora

`core/backend_pydualsense.py:2238` manda o MESMO valor para o fone (`common[4]`)
e para o alto-falante (`common[5]`). O byte de roteamento (`common[7]`) não é
tocado de propósito (`:2219-2222`: *"não sabemos o valor neutro dele e chutar
mudaria o caminho do áudio"*), e o volume de microfone (`common[6]`) também não.
Quem toca só o alto-falante na interface está, de fato, tocando o fone junto —
e isso precisa aparecer no rótulo, não numa nota de rodapé.

### Armadilha 4 — a posse morre com o cabo, e o volume também

`_volumes_audio` nasce vazio em cada handle (`core/backend_pydualsense.py:436`)
e cada conexão cria um handle novo (`:1314`). Desconectar e reconectar o
controle, ou reiniciar o daemon, apaga a posse e o volume: a chave `speaker`
some do estado e o rótulo volta a `"não ajustado"`. **O preço tem validade de
sessão** — o que é uma boa notícia para o medo, e uma má notícia para a
persistência (entrega 4).

## A TRAVA — a posse, e o que ela custa de verdade

> **O bloco de áudio do report de saída não tem dono por padrão. A primeira
> escrita nossa toma a posse, e a partir dali quem manda somos nós, em todo
> report, até alguém devolver.** Esse é o preço, e ele tem que estar escrito na
> tela ANTES do clique, não depois.

A disciplina inteira é o AUDIO-OWNER-01. Ela vive em quatro pontos:

- `core/ds_output_report.py:79-98` — a máscara `VALID_FLAG0_AUDIO_MASK` e os
  offsets `common[4..7]`. O comentário é explícito: enquanto não houver valor
  para mandar, a máscara sai **zerada**, porque autorizar um campo que
  escrevemos como `0x00` a 60 Hz é mandar "volume zero" com cara de keepalive;
- `core/backend_pydualsense.py:604-616` — o registro do defeito que originou a
  regra: o upstream mandava `flag0=0xFF` e ninguém escrevia os bytes;
- `core/backend_pydualsense.py:624-640` — os bits de áudio caem TODOS e voltam,
  um a um, só para os bytes de que alguém assumiu a posse;
- `docs/protocol/ipc-unix-socket.md:45-56` — o contrato publicado, que trata
  `mic.set` e `speaker.set` como o mesmo bloco de posse (`common[4..9]`).

### A correção medida: a posse é POR BYTE, e o alto-falante não sequestra o mic

O documento de protocolo fala do bloco `common[4..9]` como uma coisa só, e para
efeito de disciplina está certo. Mas **no report a posse é por byte e por bit**,
e isso muda o preço que a interface tem de declarar:

| Campo | Byte | Bit de autoridade | Quem toma |
|---|---|---|---|
| volume do fone | `common[4]` | `flag0 0x10` | `speaker.set` |
| volume do alto-falante | `common[5]` | `flag0 0x20` | `speaker.set` |
| volume do microfone | `common[6]` | `flag0 0x40` | ninguém hoje |
| roteamento | `common[7]` | `flag0 0x80` | ninguém hoje |
| mudo do microfone | `common[9]` | `flag1 0x02` | `mic.set` |

Fontes: `core/ds_output_report.py:74-101` e `core/backend_pydualsense.py:232-235`;
a aplicação por byte em `core/backend_pydualsense.py:636-640`, e o mudo do
microfone em ramo separado, `:654-660`.

Consequência prática, e ela precisa estar no rótulo do jeito certo: **mexer no
volume pela janela NÃO mata o botão de microfone do controle.** São bits
diferentes. O que a MIC-USB-01 viveu (`mic unmute` toma a posse e o botão físico
para de valer até `mic release`) vale para o microfone, e o alto-falante tem um
preço próprio, menor e diferente — que é o de baixo.

### O preço do alto-falante, dito por inteiro

1. a partir do primeiro clique o hefesto manda o volume do fone e do
   alto-falante em **todo** report, e o valor que o firmware tinha é
   sobrescrito;
2. **não existe leitura**: nada pode dizer qual era o volume antes, então nada
   pode restaurá-lo. Devolver a posse (entrega 3) devolve o CONTROLE, não o
   valor — o firmware conserva o último número que mandamos
   (`core/backend_pydualsense.py:552-556`, `:610-616`);
3. quem toca o alto-falante toca o fone junto (armadilha 3);
4. o preço acaba quando o controle desconecta (armadilha 4).

## As três camadas do volume — e por que a de cima está muda agora

Isto é o que faltava para a resposta à pergunta dela ("como vamos fazer ele
funcionar"). Medido nesta máquina, hoje, com o controle no cabo:

| Camada | Quem manda | Tem leitura? | Preço | Vale por BT? |
|---|---|---|---|---|
| 1. rota/sink do PipeWire | `wpctl`/`pactl`, e o estado persistido do WirePlumber | **SIM** | nenhum | não |
| 2. registrador de volume no HID | `speaker.set` | **NÃO** | posse dos bytes | sim |
| 3. fluxo de áudio por Bluetooth | ninguém — não implementado | — | — | — |

**Camada 1, ao vivo.** O controle publica sink próprio
(`alsa_output.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.analog-surround-40`,
perfil 4.0), e a leitura de agora é:

```
Volume: front-left: 26214 / 40% ... (quatro canais)
Mute: sim
```

E o mudo está **persistido**, não é do momento: em
`~/.local/state/wireplumber/default-routes` a rota
`alsa_card.usb-...DualSense...-00:output:analog-output` traz `"mute":true` com
`channelVolumes` de `0.063997` (que é 40 % elevado ao cubo). O `doctor` já sabe
disso e o reporta como INFO de propósito — `scripts/doctor.sh:660-673` diz com
todas as letras que *"o alto-falante do controle mudo é um FATO sobre a saída, e
a usuária pode tê-lo escolhido"*, e a separação por direção do filtro
(`:542-556`) foi curada em 28/07 justamente porque o alto-falante mudo estava
reprovando o microfone.

**Camada 3.** Por Bluetooth o DualSense não implementa A2DP/HFP/HSP
(`integrations/dualsense_bt_audio.py:1-15`, com a confirmação do mantenedor do
BlueZ) — não há sink nenhum. O áudio de saída viajaria nos blocos `0x13`/`0x16`
do report 0x39, que estão mapeados no módulo e **não são usados**
(`integrations/dualsense_bt_audio.py:215-223`). Por BT, portanto, subir o volume
da camada 2 não faz som sair: não há fluxo.

**A leitura honesta disso:** a camada 2 é a única que a janela pode oferecer nos
dois transportes, e é a única sem leitura. A camada 1 tem leitura, escrita e
persistência de graça — e é ela que está muda hoje. As entregas abaixo tratam as
duas, e a 1 vem primeiro na ordem de validação.

## Entregas

### E1. Controle deslizante de volume no card, com o preço na própria interface

Um `Gtk.Scale` horizontal no bloco "Alto-falante", **abaixo** da barra que já
existe (`app/widgets/controller_card.py:1436-1455`), no mesmo lugar em que o
microfone pôs o botão dele (`:1336-1378`) e pelo mesmo motivo: ali o custo é de
altura, que sobra, e não de largura, que é a restrição dura da aba.

Regras de construção, todas vindas de medição:

- o valor mandado é SEMPRE explícito. Nunca chamar `speaker_set()` sem `volume`
  (armadilha 1). O mapeamento é 0-100 % na tela, 0-255 no protocolo, com a mesma
  conta que a barra já usa (`app/widgets/sensor_widgets.py:148-161`);
- o clique não bloqueia a thread do GTK: o pedido vai por
  `ipc_bridge.run_in_thread`, exatamente como `_on_mic_clicado`
  (`app/widgets/controller_card.py:1380-1399`), e quem repinta é o tique de
  10 Hz relendo `daemon.state_full` — nunca o valor mandado;
- arrastar o controle deslizante não pode virar uma rajada de IPC: mandar no
  `button-release-event` e no fim de um repouso curto, não a cada pixel;
- **o preço fica na dica do próprio controle deslizante**, no formato que a
  MIC-USB-01 já escreveu para o microfone
  (`app/widgets/controller_card.py:384-400`). Texto proposto: *"Mover isto faz o
  hefesto assumir o volume do alto-falante E do fone do controle. O DualSense
  não devolve esse valor: depois disso, quem manda é a janela até você clicar em
  Devolver ou desconectar o controle."*

**Critério de aceite**

1. com o bloco sem dado, o controle deslizante existe, está habilitado e o
   rótulo continua `"não ajustado"` — mover é a única forma de saber, e ele é o
   convite;
2. um teste que arranque o `volume` da chamada (mandando `speaker.set` vazio)
   tem de reprovar, com a mensagem citando a armadilha 1;
3. o orçamento de largura continua de pé: a aba Status com dois controles pede
   hoje **1064px de 1180px** (medido nesta bancada, folga de 116px) e não pode
   passar de 1180. O botão do microfone custou **zero** largura porque o mínimo
   dele (38px) fica abaixo do mínimo do bloco (72px) — o controle deslizante
   tem de passar no mesmo teste;
4. o orçamento de altura: no card de um controle a coluna do som mede 210px e a
   faixa mede 246px (fim em y=356 contra y=320) — há **36px** de folga antes de
   a coluna do som virar a mais alta. No card compacto a coluna do som já está
   empatada com a faixa (154px, fim em 284), então **todo pixel cresce o card**;
   o teto por aba medido é de 719px e a aba Status pede 239px, então cabe — mas
   o número tem de ser reaferido, não presumido.

**Como validar na tela**

1. Antes de tudo, desmutar a camada 1 (o sink do controle está mudo agora);
2. aba Status, um controle no cabo, tocar qualquer som pelo sink do controle;
3. arrastar o controle deslizante: o som muda de volume e a barra do bloco
   acompanha **no tique seguinte**, não instantaneamente (é releitura, não eco);
4. o rótulo sai de `"não ajustado"` e passa a mostrar a porcentagem;
5. com dois ou mais controles, os cards continuam lado a lado, sem barra de
   rolagem horizontal.

### E2. Botão de mudo do alto-falante

Mesmo desenho do botão do microfone: um botão só, cujo rótulo diz o que o
clique faz — o padrão `AcaoMic`/`acao_mic`
(`app/widgets/controller_card.py:683-743`), replicado como uma ação de
alto-falante.

| Estado | Rótulo | Manda |
|---|---|---|
| sem posse (nenhum volume conhecido) | `sem dado`, **insensível** | nada |
| tocando, posse nossa | `Silenciar` | `{muted: true}` |
| mudo por nossa ordem | `Ativar` | `{muted: false}` |

**A insensibilidade da primeira linha é a entrega, não um detalhe.** Sem ela, o
primeiro clique tranca o alto-falante em zero e o próprio botão não solta
(armadilha 2, medida). A dica nesse estado explica o caminho: *"ainda não há
volume conhecido — use o controle deslizante primeiro"*.

**Critério de aceite**

1. é impossível, pela interface, mandar um `muted` antes de um `volume`;
2. `Silenciar` seguido de `Ativar` devolve o MESMO volume de antes (medido:
   180 -> mudo -> 180);
3. arrancar a guarda da primeira linha tem de reprovar um teste com a sequência
   mudo/desmudo terminando em `{'volume': 0, 'muted': True}`.

**Como validar na tela:** com um volume ajustado, clicar em `Silenciar` — o som
some e o rótulo vira `mudo` sem perder a porcentagem preferida; `Ativar`
devolve o som no mesmo volume.

### E3. Devolução da posse — o equivalente do `mic release`

Sem isto, o primeiro uso sequestra o volume do controle até a próxima
desconexão, e não há como sair pela interface. Falta a porta inteira: o
`release_audio_volumes` existe no handle
(`core/backend_pydualsense.py:557-559`) e **nada acima dele o chama** — o
serviço não tem método, o IPC não tem chave, a ponte não tem função e a janela
não tem botão.

O que a entrega precisa ter:

1. método no serviço, irmão do `set_speaker_volume`, que chame o
   `release_audio_volumes` do handle escolhido por `uniq` **e limpe também a
   preferência** (`_speaker_volume_pref`). Sem limpar, um `muted: false`
   posterior ressuscita um volume antigo e retoma a posse sem ninguém pedir;
2. chave nova no `speaker.set`: `release: true`. **Não reaproveitar
   `muted: null`** — aqui `muted` é opcional e a ausência já significa "não
   mexer" (`daemon/ipc_handlers.py:2520-2528`); o `mic.set` pôde usar `null`
   porque lá a chave é OBRIGATÓRIA e a ausência é erro
   (`daemon/ipc_handlers.py:2547-2552`). Reusar o `null` aqui criaria duas
   leituras para o mesmo payload;
3. terceiro estado do botão da E2: com posse nossa, o ciclo passa por
   `Devolver`, igual ao do microfone;
4. contraparte de linha de comando, para haver saída sem a janela — hoje existe
   `mic release` (`cli/app.py:143-168`) e nada equivalente para o alto-falante;
5. **o rótulo tem de ser honesto sobre o que a devolução faz**: ela para de
   mandar, e o firmware fica com o ÚLTIMO valor que mandamos — não com o valor
   original, que ninguém pode saber. Texto proposto: *"Devolver faz o hefesto
   parar de mandar o volume. O que estiver valendo continua até você
   desconectar o controle."*

**Critério de aceite**

1. depois de `Devolver`, o `daemon.state_full` **para** de trazer a chave
   `speaker` e o rótulo volta a `"não ajustado"` — a cadeia já garante isso
   (`core/backend_pydualsense.py:2192-2194` devolve `None` com o byte sem dono, e
   `daemon/ipc_handlers.py:1889` só publica dicionário);
2. depois de `Devolver`, os bits de áudio do `flag0` saem zerados no report
   (é a asserção que o teste do AUDIO-OWNER já sabe fazer em
   `tests/unit/test_audio_owner_report.py`);
3. arrancar a limpeza da preferência tem de reprovar: um `muted: false` depois
   do release não pode reabrir a posse.

**Como validar na tela:** ajustar o volume, clicar em `Devolver` — o rótulo
volta a `"não ajustado"`, o controle deslizante volta ao estado de convite, e o
som continua no volume em que estava (o que a dica prometeu).

### E4. Persistência por perfil

Seção opcional nova no perfil, no molde exato das duas que já existem —
`ProfileMouseConfig` (`profiles/schema.py:306-319`) e `ProfileMicConfig`
(`profiles/schema.py:322-346`): campo `speaker` em `Profile`
(`profiles/schema.py:411-455`), com `volume` 0-255 e `muted` booleano, default
`None`.

**O que acontece com perfil antigo que não tem o campo:** `None` significa **sem
opinião** — ativar o perfil não toca no volume e, principalmente, **não toma a
posse**. Tomar posse por um perfil que não pediu nada é exatamente o hábito que
produziu "a config que eu deixo nunca é respeitada".

Três coisas medidas que a entrega tem de resolver, e que não são óbvias:

1. **a compatibilidade para trás quebra em TODO perfil, não só nos que usam a
   seção.** O `save_profile` só omite `controllers`
   (`profiles/loader.py:629-637`); o `model_dump` emite todos os campos
   declarados. Medido agora, um perfil recém-criado já sai com
   `"mouse": null, "mic": null, "mode": null`. Acrescentar `speaker` faz todo
   save gravar `"speaker": null`, e binário antigo com `extra="forbid"`
   (`profiles/schema.py:414`) rejeita **todos** os perfis no downgrade. **Cura:
   omitir a chave quando `None`, como o `controllers` já faz** — é requisito, não
   estética;
2. **a trava manual não cobre áudio.** As categorias são
   `frozenset({"trigger", "led", "rumble"})`
   (`daemon/state_store.py:48`, uso em `:198-211`). No dia em que o perfil passar
   a escrever o volume, o autoswitch reaplicando perfil por troca de janela pode
   pisar o volume que ela acabou de ajustar na mão — a classe de defeito de
   sempre. Ou o `speaker.set` arma uma quarta categoria (`audio`), ou o
   `speaker_applier` só roda em troca EXPLÍCITA de perfil. A decisão tem de
   ficar escrita antes do código;
3. **a posse morre na reconexão** (armadilha 4). Persistir por perfil sem
   reaplicar no `connect` faz o volume voltar ao do firmware ao trocar o cabo,
   em silêncio. Reaplicar no `connect` **só** quando o perfil ativo tem a seção —
   caso contrário, voltamos a tomar posse sem pedido.

O caminho de injeção já está pronto: os appliers do `ProfileManager`
(`profiles/manager.py:88-117`) e o ponto de aplicação do `mouse`
(`profiles/manager.py:446-461`) são o molde; a GUI já sabe ler seção de perfil
para o rascunho (`app/draft_config.py:374-377`, que faz isso com o `mic`).

**Critério de aceite**

1. perfil antigo (sem a chave) continua carregando, e ativá-lo **não** produz
   nenhuma escrita de áudio — teste que conta as chamadas ao backend;
2. `load -> save` de um perfil sem a seção não acrescenta a chave ao arquivo;
3. com a seção presente, trocar de perfil muda o volume, e a chave `speaker`
   aparece no estado logo depois;
4. arrancar a omissão do `None` no `save_profile` reprova o teste de
   compatibilidade.

**Como validar na tela:** criar dois perfis com volumes diferentes, alternar
entre eles e ouvir a mudança; abrir um perfil antigo e conferir que o bloco
continua dizendo `"não ajustado"`.

### E5. O que a tela diz quando não há leitura

Hoje o rótulo diz `"não ajustado"`
(`app/widgets/controller_card.py:408`, aplicado em `:1786`), e a frase é
**verdadeira** — vale mantê-la. O que falta não é trocar a palavra: é ela parar
de ser a única coisa que o bloco sabe dizer.

O comportamento honesto proposto, e a razão de cada parte:

1. **a barra continua sendo LEITURA e o controle deslizante é COMANDO.** Duas
   peças, dois significados: sem posse, a barra fica vazia (não sabemos) e o
   controle deslizante fica em repouso sem afirmar posição — pôr o cursor no meio
   com o rótulo `"não ajustado"` seria desenhar 50 % e negá-lo por escrito;
2. **o bloco nunca se esconde**, pela regra da MIC-PRESENTE-01: esconder muda a
   largura dos vizinhos e some com o bloco inteiro, e sumir é indistinguível de
   "este controle não tem alto-falante";
3. **uma linha de explicação no lugar do silêncio**, na dica do bloco: *"o
   volume é do firmware do controle e ele não o devolve; mover o controle
   deslizante passa a mandá-lo"*. É a diferença entre "a janela não sabe" e "a
   janela está quebrada";
4. **quando a camada 1 estiver muda, dizer isso.** É a informação que faz o
   bloco parar de parecer mentiroso: com o sink do controle mudo, mover o volume
   não produz som nenhum, e o `doctor` já sabe detectar a condição
   (`scripts/doctor.sh:465-476` para a saída desligada por drop-in, `:493-506`
   para o sink padrão mudo, `:660-673` para a rota de saída muda). Proposta
   mínima e sem inventar: um selo `saída muda` no bloco quando a leitura da
   camada 1 disser isso, e nada quando não houver como saber.

**Critério de aceite**

1. sem posse, o rótulo é `"não ajustado"` e NUNCA uma porcentagem — os testes
   que já travam essa frase continuam valendo
   (`tests/unit/test_status_faixa_blocos.py`,
   `tests/unit/test_status_cards_sensores.py`);
2. depois de `Devolver`, a tela volta ao estado de "não sei" em um tique;
3. o bloco não some em nenhum caminho, com ou sem dado.

## Teste que morde

As mordidas que esta leva precisa ter, cada uma arrancada de verdade e
devolvida — o padrão da casa:

| Cura arrancada | O que reprova |
|---|---|
| mandar `speaker.set` sem `volume` | estado publicado vira `{'volume': 0, 'muted': True}` |
| botão de mudo sensível sem volume conhecido | a sequência mudo/desmudo tranca em zero |
| release sem limpar a preferência | um `muted: false` depois do release reabre a posse |
| release sem porta acima do handle | a chave `speaker` não some do estado |
| `save_profile` sem omitir a seção `None` | perfil antigo passa a gravar `"speaker": null` |
| perfil sem a seção passando a escrever | o backend recebe escrita de áudio sem ninguém pedir |
| controle deslizante sem teto de largura | a aba com dois cards passa dos 1180px |

Toda medida de geometria tem de ser feita com o card **montado e alocado** numa
`Gtk.OffscreenWindow`, como a SOM-01 fez: widget sem alocação devolve 1x1 e um
teste de layout sobre ele passa com qualquer desenho.

## Como você valida (roteiro na tela, na ordem)

1. **Primeiro a camada 1**, senão nada do resto faz som: o sink do controle está
   mudo hoje, em 40 %. Desmutar e conferir que sai áudio pelo alto-falante do
   controle;
2. aba Status, um controle no cabo: o bloco "Alto-falante" está abaixo do
   microfone (herança da SOM-01), agora com barra, controle deslizante e botão;
3. passar o cursor no controle deslizante **antes** de mexer: a dica diz o preço
   com todas as letras;
4. mover o controle deslizante: o som muda, a barra acompanha no tique seguinte,
   o rótulo vira porcentagem;
5. `Silenciar` e `Ativar`: o volume preferido sobrevive;
6. `Devolver`: o rótulo volta a `"não ajustado"` e o som fica onde estava;
7. apertar o botão de microfone do controle **depois** de tudo isso: ele
   continua funcionando — o volume não tomou o mudo do microfone (a correção
   medida acima);
8. desconectar e reconectar o controle: o bloco volta a `"não ajustado"`
   sozinho;
9. com dois e com quatro controles: nada muda de lugar, sem barra de rolagem
   horizontal.

## O que NÃO fazer

1. **Não mandar `speaker.set` sem `volume`** — medido: toma a posse e manda
   zero. Se algum dia for preciso um "toma a posse sem mudar nada", isso é uma
   chave nova e explícita, não a chamada vazia;
2. **não usar o botão de mudo como primeira escrita** — medido: tranca em zero e
   o próprio botão não solta;
3. **não reaproveitar `muted: null` como devolução** — aqui `muted` é opcional e
   a ausência já quer dizer "não mexer"; o `mic.set` pôde porque lá a chave é
   obrigatória;
4. **não tocar `common[6]` (volume do microfone) nem `common[7]` (roteamento)** —
   o segundo está descartado com motivo escrito no código: não sabemos o valor
   neutro e chutar muda o caminho do áudio;
5. **não prometer que a devolução restaura o volume anterior** — não há leitura,
   logo não há restauração. Prometer isso é a mesma família de mentira que a
   SOM-01 recusou ao não publicar `0 %`;
6. **não esconder o bloco quando não houver dado** — MIC-PRESENTE-01 mediu o
   custo: esconder na faixa horizontal move todos os vizinhos, e sumir é
   indistinguível de "não tem alto-falante";
7. **não guardar o valor mandado e pintá-lo como leitura** — quem repinta é a
   releitura de `daemon.state_full`. O estado publicado é legítimo porque diz o
   que NÓS mandamos; um número sem posse seria chute;
8. **não bloquear a thread do GTK no clique** — o IPC é bloqueante, e foi assim
   que esta interface já congelou;
9. **não ligar a persistência por perfil ao autoswitch sem resolver a trava
   manual** — as categorias existentes não cobrem áudio, e o resultado seria o
   perfil pisando o ajuste dela na troca de janela;
10. **não tentar controlar a camada 1 escrevendo direto no estado do
    WirePlumber** — o mudo persistido é dela e o `doctor` o trata como escolha
    legítima. O caminho é `wpctl`/`pactl` no momento, com aviso, ou nada;
11. **não prometer som por Bluetooth** — não há A2DP e o bloco de alto-falante do
    túnel HID não é usado. Por BT o controle deslizante muda um registrador que
    não tem o que tocar. Ou o bloco diz isso, ou não deve prometer.

## O que fica de fora desta sprint, e por quê

- **A ponte de áudio de saída por Bluetooth** (os blocos `0x13`/`0x16` do report
  0x39). É uma sprint inteira, do tamanho da ponte do microfone, e nada nas
  entregas acima depende dela;
- **um comando de linha completo para o alto-falante** (o irmão do `mic`): a
  entrega 3 pede só o `release`, que é a saída de emergência. O resto pode vir
  depois, se ela quiser;
- **cura automática do mudo da camada 1**: o `doctor` reporta e não conserta, de
  propósito — o alto-falante mudo pode ser escolha dela. Transformar isso em
  `--fix` é decisão dela, não minha;
- **volume separado para fone e alto-falante**: o backend manda o mesmo valor
  para os dois e o registro diz por quê (para quem usa o controle é um volume
  só, e qual toca depende do fone estar plugado). Separar exige dois controles
  na tela e um critério para "qual está tocando" que hoje só existe como
  leitura de `fone_plugado`;
- **nada foi validado na tela dela**: esta rodada é documento. As medidas de
  geometria são de `Gtk.OffscreenWindow` e as de áudio são desta máquina hoje,
  mas o aceite é o dela.
