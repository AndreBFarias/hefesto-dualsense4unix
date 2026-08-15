# ÍNDICE — a cor do controle, e o som de cada jogador

- **Escrito em:** 14/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `48e7fd5` (*"três nomes e duas ordens para a mesma mesa, vistos na foto"*).
- **Nasceu do pedido dela**, em cinco partes: *"cada controle com a guia na cor
  física dele e mostrando a escolha do user"*; *"x pra escolher, bola pra
  desescolher, r1 pra ir pra próxima aba, l1 pra voltar pra aba da esquerda"*;
  tudo salvo **dentro do perfil ativo, para cada controle**; *"o canal 3 do
  DualSense tem uma saída de som pra efeitos sonoros SFX de cada joguinho,
  diferente da saída padrão do HDMI"*; e **mapear cientificamente** microfone,
  saída de som, giroscópio e acelerômetro, **no cabo e por Bluetooth**.
- **E da regra de método que ela fixou hoje**, que vale acima de tudo o que
  está escrito aqui: *"se no playstation via bt tudo isso funciona é pq tem um
  meio físico pra isso funcionar e ainda não descobrimos, pq a documentação
  oficial é focada no cabo... só falta mapear cientificamente pra tirarmos os
  achismos nossos do projeto"*. E: *"só mapeamos de verdade 5 coisas nas
  specs... áudio mesmo, touch, e afins nada mapeado oficialmente. mic também
  não"*.
- **Grau:** **MISTO, e cada linha diz qual é o dela.** O que está marcado
  **MEDIDO** foi lido do aparelho dela, do descritor vivo, do fonte do driver ou
  do socket do daemon **hoje**, e traz o comando que produziu o número. O que
  está marcado **PLANO** é proposta e não virou código. Nenhum byte foi escrito
  em controle nenhum **na medição de 14/08**.
- **ATUALIZADO EM 15/08/2026, de madrugada, e a atualização move linhas deste
  índice de grau.** Na mesa 2+2 dela — dois controles no cabo e dois no rádio ao
  mesmo tempo — **bytes foram escritos em controle, com ela presente e olhando a
  lightbar**, e o firmware **executou** reports de output de 142 B (`0x32`) e
  547 B (`0x39`) por rádio. O que isso prova e o que **não** prova está no
  [estudo](../estudos/2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md),
  e o próximo ensaio está desenhado na
  [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md).
  **A frase honesta, e é a única a copiar daqui:** *o canal existe, o firmware
  responde, e o conteúdo do payload ainda não foi identificado.*
- **Seis frentes mediram em paralelo** para escrever este índice, e nenhuma
  editou a árvore. As duas leis de método delas estão na seção 3.
- **A leva anterior continua aberta e não se sobrepõe a esta:**
  [a mesa cheia, cada jogador na cor dele](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md),
  com as decisões **D-1 a D-12** já respondidas em
  [as onze respostas](../2026-08-14-DECISOES-DE-PO-as-onze-respostas-da-mesa-cheia.md).
  **As perguntas deste índice começam em D-13.**

---

## Como ler este índice

**As ondas são separadas por quem precisa estar presente**, e não por assunto —
é a forma que a casa fixou em 31/07 e é a única divisão que muda o que dá para
fazer hoje à noite e o que espera ela sentar.

- **ONDA 1 — o que eu faço sozinha.** Zero pixel novo, zero byte escrito no
  aparelho. É a onda da **verdade**: o mapa para de afirmar o que ninguém
  mediu, e os instrumentos de medição passam a existir.
- **ONDA 2 — o que precisa das mãos e da orelha dela.** É a onda que **tira os
  achismos**: o canal 3, o jack por rádio, o cabo, o censo de cor. Nada aqui se
  decide lendo código.
- **ONDA 3 — o que precisa do olho dela.** É a onda em que **a cor aparece na
  tela** e o controle passa a navegar a janela. Fecha com foto e com a palavra
  dela ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).
- **ONDA 4 — o que trava esperando decisão dela.** São perguntas, não tarefas:
  **D-13 a D-33**, na seção 8. As **D-30 a D-33** nasceram em 15/08.

**Uma frente pode aparecer em duas ondas**, com a entrega numerada — é o caso do
áudio por rádio (o instrumento na 1, o som na 2) e da cor (o dado na 2, a
pintura na 3).

---

## 1. A tradução, para ela conferir

Eu li o pedido dela como cinco afirmações. Se alguma estiver errada, a leva
muda de forma — por isso vêm primeiro, e por isso cada uma vem com o que a
medição de hoje **confirmou** e o que ela **corrigiu**.

| o que ela pediu | o que a medição de hoje diz |
|---|---|
| 1. **A guia de cada controle na cor física dele** | A **paleta** existe desde 10/08 (cinco cores nos SVG). A **leitura da cor a partir do aparelho nunca foi tentada** — nem uma linha, em lugar nenhum. Ela lembrou certo que *"tínhamos mapeado isso no passado"*: mapeamos **metade**. E a metade que falta é a que decide |
| 2. **Navegar a interface pelo controle** | O controle **já navega** hoje, com o vocabulário trocado: `cross` é clique, `circle` é Enter, `square` é Esc, `r1` é Alt+Tab. Falta o verbo certo e o gate de foco — e o gate já existe e já está saudável |
| 3. **Tudo salvo no perfil ativo, para cada controle** | Vale para todo **ajuste**. Mas a **cor do plástico não é ajuste, é fato da peça** — e o perfil já excluiu identidade visível de propósito. Isto é uma contradição real, não invenção minha: é a **D-16** |
| 4. **Som SFX por jogador, "o canal 3"** | **O endereço está errado e a coisa que ela quer existe.** Os quatro canais do sink USB são 2 de som + 2 de motor — e isso mesmo **NÃO está medido**, é inferência. Por rádio não passa por canal PCM nenhum: é o bloco `0x13` do report `0x39`, cujo caminho está inteiro documentado e **nunca foi escrito**. **15/08: o REPORT `0x39` já foi escrito e executado** — o **bloco `0x13`**, esse continua sem uma linha |
| 5. **Mapear cientificamente mic, som, giro e acelerômetro, cabo e BT** | Das **oito** células (4 peças x 2 transportes), **duas** têm medição que sustenta o rótulo. **Uma foi medida hoje** (acelerômetro por BT, e passa). As outras cinco dizem `medido` sobre coisa diferente da que o rótulo promete |

**A quarta é a que precisa de qualificação, e ela vai gostar do motivo.** O
"canal 3" que ela descreve do Sackboy existe — só não é um canal PCM. O DualSense
tem **três caminhos de som separados** e o produto usa **um**:

```
   CABO                                     RÁDIO
   sink USB "analog-surround-40"            report OUTPUT 0x39 (546 B)
   ┌──────────────────────────┐             ┌───────────────────────────┐
   │ canal 1-2  som           │  <- usamos  │ bloco 0x11  controle      │  <- nunca
   │ canal 3-4  ???           │  <- NAO     │ bloco 0x12  háptico       │     escrito
   └──────────────────────────┘   MEDIDO    │ bloco 0x13  alto-falante  │
                                            │ bloco 0x16  fone          │
   registrador HID OUTPUT_PATH_SEL          └───────────────────────────┘
   escolhe fone x alto-falante,
   POR CONTROLE, ja implementado
```

O pedaço **difícil** do SFX por jogador não é rotear — a rota já é por controle e
por registrador HID, endereçada por `uniq`. O difícil é **ter o que rotear**, e é
disso que trata a onda 2.

---

## 2. O que foi MEDIDO hoje, e o que continua sendo plano

Cada linha traz o comando ou o endereço. **Nada aqui é opinião.**

### 2.1 Medido no aparelho dela, hoje

| o que | o número | como |
|---|---|---|
| **O acelerômetro por Bluetooth funciona, e chega calibrado** | módulo do vetor em repouso = **0,9945 g** e **0,9823 g** nos dois controles (erro de 0,6% e 1,8% contra `DS_ACC_RES_PER_G` = 8192) | `python-evdev` do `.venv`, nós "DualSense Wireless Controller Motion Sensors", bus 0005. **Nenhum comando de "ligar IMU" foi enviado por ninguém** |
| **A escada de OUTPUT por rádio** | `0x31`=77 B, `0x32`=141, `0x33`=205, `0x34`=269, `0x35`=333, `0x36`=397, `0x37`=461, `0x38`=525, `0x39`=**546** (teto). Passo de +64 | parser próprio sobre `/sys/class/hidraw/hidraw8/device/report_descriptor` e `hidraw10` — 320 B, **descritores idênticos**, firmware `0x0110002a` nos dois |
| **A escada é de áudio, e o 0x39 é o degrau do alto-falante** | 1 (seq) + 8 (bloco `0x11`) + 130 (`0x12` duplo) + 402 (`0x13` duplo, dois quadros Opus de 200 B) + 4 (CRC) = **545 B**. Cabe nos 546 do `0x39` com **um byte de folga**, e **não cabe** nos 525 do `0x38` | aritmética sobre o Report Count medido acima. **Isto fecha sozinho a "contradição interna em aberto" de 11/08** |
| **O CRC do 0x39 é o que a casa já tem** | as três formas devolvem `0xa238ce60` para a mesma amostra: `bt_crc32` com semente `0xA2`, a do SAxense, e `zlib.crc32(b"\xa2" + dados)` | comparação lado a lado no `.venv`. **Nenhuma linha de CRC nova a escrever** |
| **O rádio dela comporta o report inteiro** | ACL MTU **1021:6**; o `0x39` no ar é 548 B com o cabeçalho HIDP `0xA2`. Cabe em **um** pacote ACL. Teto do kernel para escrita em hidraw: 16384 | `hciconfig -a`; `grep HID_MAX_BUFFER_SIZE` nos headers instalados |
| **A libopus da máquina já tem o codificador** | libopus **1.4**, com `opus_encoder_create`, `opus_encode_float` e `opus_encoder_ctl` presentes. O produto hoje só usa o decodificador | `ctypes.CDLL("libopus.so.0")` |
| **O descritor declara DEZESSETE feature reports e o driver conhece TRÊS** | `0x05`(40 B) `0x08`(47) `0x09`(19) `0x0b`(41) `0x20`(63) `0x22`(63) `0x80`(63) `0x81`(63) `0x82`(9) `0x83`(63) `0xf0`(63) `0xf1`(63) `0xf2`(15) `0xf4`(63) `0xf5`(7) `0xf6`(**546**) `0xf7`(7). O driver nomeia `0x05`, `0x09` e `0x20` | mesmo parser de descritor. O `0xf6` de 546 B é o **gêmeo exato** do OUTPUT `0x39` e não é nomeado em lugar nenhum deste repositório nem do driver |
| **Existe um feature `0x22` que ninguém nunca leu** | 64 B; repete a versão do `0x20`; carrega o **MAC em little-endian** (conferido contra o `uniq` do sysfs); e traz **dois blocos de 8 B completamente distintos por unidade** (off 35..42 e 45..52), de significado desconhecido | sonda de leitura pura pelo broker, `HIDIOCGFEATURE`, zero escrita, nos dois controles |
| **Os dois controles diferem no `0x20` em quatro bytes** | off 20 (`0x03` x `0x02`), off 24 (**hw_version** `0x0710` x `0x0711`), off 32-33 (`0x00d8` x `0x01a8`). Todo o resto idêntico, inclusive a build `Jul  4 2025 10:10:32` | mesma sonda. **Nenhum desses quatro se sabe carregar cor — e nenhum foi descartado** |
| **O feature `0x08` é o mesmo nos dois** | 48 B, **todo zero**, idêntico. Descartado **com prova** como candidato a cor | mesma sonda |
| **O daemon já sabe quando a janela dele está em foco** | `window_detect_backend="xlib"`, `healthy=true`, `seeing=true`, `last_class="Hefesto-Dualsense4Unix"` | `daemon.state_full` no socket. A GUI roda em XWayland porque o produto força `GDK_BACKEND=x11` em COSMIC |
| **O gate por foco é fail-closed** | com janela Wayland nativa em foco (o jogo), a leitura vira `wm_class="unknown"`, motivo `sem_foco_x` — e **"unknown" nunca casa** com a classe da janela dela | leitura direta de `get_active_window_info()` sob `DISPLAY=:1` |
| **Polling é barato: a objeção "não dá a 30 Hz" não se sustenta** | `daemon.state_full` mediana **0,4 ms**, p90 0,6 ms, 7107 B — conexão nova a cada chamada. A 30 Hz dá ~1,2% de uma thread | 20 iterações por método sobre o socket AF_UNIX |
| **Os botões dos secundários já são publicados** | `controllers[1]` (não primário) veio com `inputs.buttons`, `inputs.lx=123` e `inputs.gyro` preenchidos | `daemon.state_full` ao vivo, com dois controles na mesa |
| **Um provider de CSS por widget vence o tema e pinta a borda** | com o tema carregado, `(189,147,249)`; com o provider, `(0,255,0)`. E `box-shadow: inset` **não muda um pixel** de tamanho: 67x38 com e sem | render offscreen com `Gtk.OffscreenWindow` |
| **A borda de hoje é o pior contraste da janela** | `@current_line` rende **1,34:1**; a diferença entre marcado e não marcado por fundo sozinho é **1,28:1**. Qualquer cor passada por `ensure_min_contrast` fica melhor: preto 1,71 vira 3,02; azul puro 1,43 vira 3,02 | `razao_contraste` contra `PIOR_FUNDO` |
| **Pintar custa quase nada** | `load_from_data` = **4,2 us**; o ciclo criar+instalar+remover = **7,6 us**. Oito widgets a 2 Hz sem guarda nenhuma = 0,012% de um núcleo | 2000 e 500 iterações com `perf_counter` |
| **Achado lateral e caro: o grab do primário está falhando** | `primary_grab_state="failed"`, com `[Errno 16] Dispositivo ou recurso está ocupado` no `/dev/input/event265` às 15:54. Com o vpad de pé isso é **input dobrado** no jogo para o P1 | `daemon.state_full` + `journalctl --user -u hefesto-dualsense4unix` |

### 2.2 Medido no fonte, não no aparelho

- O **jack por Bluetooth chega**: o `hid_playstation` lê o **mesmo struct** nos
  dois transportes (só muda o offset e o CRC), e descarta o estado do jack por
  rádio em **dois portões**, ambos comentados como *"Bluetooth audio is
  currently not supported"*. Isso é **política do driver, não ausência no
  aparelho** — e o projeto já tem o endereço: byte 55, bit 0.
- O **relógio do próprio controle** vem em toda janela de motion
  (`sensor_timestamp`, 32 bits, unidade de 0,33 us) e **nunca foi parseado**. É
  a única régua desta leva que não depende do relógio do host, nem do
  escalonador, nem de biblioteca nenhuma.
- **`BLOCO_SPEAKER = 0x13` está declarado no código, com o comentário certo ao
  lado, e não é referenciado por nenhum caminho de escrita.** Quem escreveu a
  ponte do microfone em julho já sabia como acender o alto-falante. Só não
  escreveu. É *"a casa sabe e o produto não faz"*, o defeito mais caro daqui, em
  estado puro.
- O controle **já navega** a janela hoje: `cross` = BTN_LEFT, `triangle` =
  BTN_RIGHT, `circle` = KEY_ENTER, `square` = KEY_ESC, `r1` = Alt+Tab, `l1` =
  Alt+Shift+Tab. Mas **está desligado agora**: medido `mouse_emulation.enabled =
  false` e `keyboard_emulation.enabled = false`, com `gamepad_emulation` ligada.

### 2.3 O que continua sendo PLANO, e não se disfarça de outra coisa

- **O aparelho DISSE SIM ao `0x39` — em 15/08/2026, e a linha anterior desta
  lista foi substituída por isto.** Até 14/08 ela dizia *"o aparelho nunca disse
  sim ao `0x39`"*, e essa frase virou fato errado em horas: na mesa 2+2 o mesmo
  `common` de 47 bytes pedindo cor foi mandado por `0x31` (78 B), `0x32` (142 B)
  e `0x39` (547 B), e **ela viu a lightbar obedecer nos três**, com o `0x31`
  apagando entre um e outro como controle positivo.
  **O que isso prova:** o firmware lê e executa reports de output de 142 e 547
  bytes por rádio, o canal os transporta (`ACL Data TX dlen 552` no `btmon`), e
  o `common` vale igual em todos.
  **O que isso NÃO prova, e é a metade que importa:** que os bytes **além** do
  `common` sejam áudio. Continua **hipótese** — forte, e hipótese.
  A aritmética de 14/08 (545 necessários contra 546 declarados) segue de pé como
  aritmética, e continua **não sendo** medição do payload. Detalhe no
  [estudo](../estudos/2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md);
  o ensaio que decide, na
  [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md).
- **Nenhuma linha desta leva virou código.**
- **Nenhum custo em minutos foi medido.** Onde houver estimativa, ela está
  marcada como estimativa.

---

## 3. Onde o mapa mente — as duas leis dela, aplicadas linha a linha

### 3.1 O mapa JÁ TEM a coluna honesta, e ela concorda com a Vitória

Este é o achado que reorganiza tudo o mais. O mapa tem **duas** colunas de
confiança com nomes que se confundem:

| coluna | quantas fortes | o que é preciso para ganhar |
|---|---|---|
| **`confianca` = `medido`** | **98 células** | um teste que afere **o byte que o Hefesto monta**. Não exige aparelho, não exige data, não exige quem provou |
| **`grau` = `O APARELHO OBEDECEU`** | **15 células** | **ensaio de bancada**, com observador. É a escada `MONTOU` -> `SAIU NO FIO` -> `O APARELHO OBEDECEU` |

**As 15 células fortes cobrem oito chaves em cinco assuntos** — lightbar, rumble,
gatilho adaptativo e duas combinações. **Áudio, microfone, toque e movimento têm
ZERO.** É exatamente o *"só mapeamos de verdade 5 coisas"* dela, **medido**.

E o caderno de bancada confirma pelo outro lado: `docs/data/ensaios.csv` tem **77
ensaios** e **nenhum** de áudio, toque ou movimento.

**Quem mente não é uma pessoa, é o nome de uma coluna.** É a **D-13**.

### 3.2 As quatro células que declaram impossibilidade sem prova de impossibilidade

**A LEI 1 dela:** *"impossível" só se declara com prova de impossibilidade*. Não
ter achado o caminho não é prova de que ele não existe.

**Eu nomeio a forma de erro, para ela poder cobrar de mim e de qualquer agente
futuro pelo nome: a FALÁCIA DO PERFIL AUSENTE** — tomar *"o aparelho não anuncia
o perfil padrão X"* (medição verdadeira e estreita) como prova de *"o aparelho
não faz a coisa Y"* (afirmação forte e falsa). **Esta casa já pagou por esse erro
uma vez e já o derrubou uma vez**: o microfone por BT funciona hoje **porque
alguém recusou o salto**.

| célula | o que ela diz hoje | por que está errado | a redação proposta |
|---|---|---|---|
| **`audio.saida_dedicada`, rádio** | *"IMPOSSÍVEL por A2DP/HFP: zero cards"* | O mapa se refuta **quarenta linhas adiante**: o microfone por BT já atravessa, e **não por A2DP** — é túnel HID, Opus no input `0x31`, ligado por output `0x32` com TLV tag `0x11`, medido ao vivo em 25/07 | *"NÃO É POR A2DP/HFP — medido em 07/08: o controle não anuncia perfil de áudio. Isso **descarta A2DP e HFP** e **não descarta áudio por rádio**. O caminho é HID: report `0x39` (546 B, o único degrau que comporta o conjunto — re-medido em 14/08 nos dois controles dela), bloco TLV `0x13` (alto-falante) ou `0x16` (fone), dois quadros Opus de 200 B, estéreo 48 kHz, 10 ms, CBR 160 kbps. **Não implementado e não medido neste aparelho.** Descartado: A2DP, HFP. Não descartado: o túnel HID pelo `0x39`."* |
| **`audio.leitura_de_volta`** | `existe = nao-tem`: *"não há report de entrada nem feature que devolva volume, rota, pré-amp ou o mudo"* | Medi: o descritor declara **dezessete** feature reports e o driver conhece **três**. **Catorze nunca foram lidos por ninguém** | `existe = desconhecido`. *"Descartados: os reports de ENTRADA `0x01` e `0x31`. **Não descartados: os catorze FEATURE que ninguém leu.** Medido em 14/08 nos dois controles dela"* |
| **`toque.touchpad.escrita`** | `existe = nao-tem`, evidência: *"Não localizei report, offset nem bit de saída de touchpad em `src/`"* | **A busca foi no NOSSO código.** Ausência de implementação nossa não é ausência de capacidade do aparelho. É a forma de erro exata que a LEI 1 nomeia | `existe = desconhecido`, com a lista do que foi descartado (o `TouchpadColor` da pydualsense, que é a cor da lightbar) e do que não foi (os catorze features, os degraus altos da escada) |
| **`movimento.imu.ligar`** | `existe = nao-tem` — **e a própria ressalva da célula diz:** *"Se houver feature report capaz de ligar ou desligar a IMU, ninguém procurou"* | A ressalva está certa e o veredicto da coluna a contradiz. **E hoje eu li a gravidade dos dois controles sem enviar um único byte** | `existe = desconhecido`, promovendo a ressalva já escrita ao lugar do veredicto |

> **ATENÇÃO, 15/08/2026 — a redação de `audio.saida_dedicada`, rádio, PODE
> SUBIR DE GRAU, e a subida é pequena de propósito.** A linha da tabela acima
> termina em *"não implementado e não medido neste aparelho"*. Metade disso
> caiu: **o degrau foi medido.** O `0x32` (142 B) e o `0x39` (547 B) foram
> escritos por rádio e o firmware os executou, com ela olhando a lightbar. A
> redação certa hoje acrescenta **uma** frase, e nenhuma a mais:
> *"MEDIDO em 15/08/2026: o firmware ACEITA e EXECUTA os degraus `0x32` e `0x39`
> por rádio, processando neles o mesmo `common` de 47 bytes. O conteúdo do
> payload além do `common` NÃO foi identificado — que seja áudio continua
> hipótese."* **Não escreva que o áudio por rádio foi descoberto, nem que a
> ponte funciona: não funciona e não há ponte.**

> **ATENÇÃO, 15/08/2026 — duas destas redações propostas JÁ ENVELHECERAM, e
> quem for aplicá-las no mapa tem de atualizar antes.** As frases *"os catorze
> FEATURE que ninguém leu"* (linhas de `audio.leitura_de_volta` e
> `toque.touchpad.escrita`) descrevem um estado que acabou: **os dezessete foram
> lidos, nos quatro controles dela, por rádio, em 15/08/2026** — ver a entrega
> 2.6 e a
> [canônica](../../protocol/dualsense-referencia-canonica.md). A redação certa
> hoje é *"os dezessete features foram lidos em 15/08/2026 e nenhum devolve
> volume, rota, pré-amp ou mudo; o que não foi descartado são os degraus altos
> da escada de OUTPUT e as respostas da família `0x80`-`0x83` **com comando
> prévio**"*. **Copiar a coluna antiga para o CSV põe um fato morto num portão.**
> A célula em si é de outro agente desta leva; esta nota existe para que ele não
> a aplique às cegas.

**A regra que a redação nova obedece:** *"não encontramos o caminho, e aqui está
o que já descartamos"* é informação útil e datável. *"É impossível"* fecha a
porta e é afirmação forte sem prova. **A diferença entre as duas é a diferença
entre este projeto existir e não existir** — a cor da lightbar por BT, o
microfone em processador AMD e o storm dos canais de áudio já foram chamados de
impossíveis nesta casa, e os três funcionam.

### 3.3 As seis células que dizem `medido` sobre coisa diferente

**A LEI 2 dela:** o rótulo `medido` não é confiável. Ela avisou; o censo
confirma. Das 16 células `medido` de áudio e toque: **9 são medição de verdade,
6 medem outra coisa, 1 não tem evidência nenhuma.**

| célula | o que a evidência realmente mede | proposta |
|---|---|---|
| `audio.alto_falante.preamp`, cabo | o que o **kernel 6.18** escreve. E o documento que a célula cita diz **por escrito**: *"Não medido"* e *"O aceite que falta é o dela"* | rebaixar para `inferido-do-codigo` |
| `audio.alto_falante.volume`, cabo | um **comentário** do kernel (*"the accepted range seems to be..."*) | rebaixar |
| `audio.jack.deteccao`, cabo | **a data em que a nossa cura entrou** | rebaixar |
| `audio.microfone`, cabo | **a inversão de um drop-in do WirePlumber** — mede o arquivo, não o aparelho captar som | rebaixar |
| `audio.microfone.volume`, cabo | uma busca em `src/` que devolve **zero chamadas** — mede o nosso produto | rebaixar |
| `audio.saida_dedicada`, rádio | o **registro SDP do BlueZ**, e conclui coisa diferente do que mediu | manter `medido`, mover a evidência para *"medido o registro SDP; NÃO medida a ausência de áudio"* |

**E quatro células dizem `medido` com o campo de evidência VAZIO** ou com um
aviso no lugar da prova: `audio.microfone.mudo` (cabo),
`movimento.giroscopio` do 8BitDo (rádio), `identidade.pareamento` do 8BitDo
(rádio), e `movimento.imu.perda` do Pro, cujo texto inteiro é *"o número CRESCE
enquanto se mede"* — que é uma ressalva, não um número.

**O buraco que deixou isso acontecer, medido:** de **19 linhas** com célula
`medido` nessas famílias, apenas **três** carregam `provado_em` **e**
`provado_por`. O portão não cobre isso de propósito — ele exige ensaio só para a
coluna `grau`.

### 3.4 A premissa que a tarefa mandou conferir, e que NÃO se sustenta

*"Canais 1-2 = fone/alto-falante; canais 3-4 = motores voice-coil"* — a
afirmação que contradiz o modelo dela de *"canal 3 = SFX"*.

**Ela NÃO é medida.** No v1 mora sob `aparelho_confianca = inferido-do-codigo`, e
a evidência da própria linha é a **ausência**: *"Busca em toda a árvore por
voicecoil, VCM, PCM e Surround devolve APENAS comentários... Não há UMA linha de
implementação."* Na canônica aparece com grau ALTA e sem ensaio por trás.

**O que está medido é só que a placa tem quatro canais.** O `chmap FL FR RL RR` é
o mapa genérico de surround da USB Audio Class — seria o mesmo se os traseiros
fossem motores **ou** se fossem uma segunda saída de som.

```
   O modelo do mapa     "canais 3-4 sao os motores"   -> zero prova
   O modelo dela        "canal 3 tem saida de SFX"    -> zero prova
                                    |
                        empatados, e so a orelha
                        e a mao dela desempatam
```

**Isto é a entrega 2.1 da onda 2, e custa cinco minutos.**

### 3.5 A contradição interna que governa uma decisão de código

Duas células da mesma família se contradizem, e a que perde ainda justifica o
teto de silêncio de 30 s por rádio contra 1 s no cabo:

- `movimento.giroscopio.jogo`, rádio: *"Medido 03/08 com os controles PARADOS:
  ~300 Hz. O DualSense por BT **NÃO** emudece em repouso — a premissa
  BT-SURDO-01 caiu."*
- `movimento.imu.ligar`, rádio, e o comentário em
  `src/hefesto_dualsense4unix/core/physical_report_reader.py`: *"o firmware
  emudece quando o controle está em repouso"*.

**O teto de 30 s continua certo** — as rajadas com p95 de 187 ms o justificam
sozinhas. **O que está errado é a frase que o acompanha.** Pela regra da casa
isto é **fato errado**, não decisão medida: substitui-se, não se datam os dois.

---

## 4. A assimetria cabo x rádio, na cara

**Dois dos quatro controles dela estão em Bluetooth agora**, e no momento da
medição **nenhum** estava no cabo — `/proc/asound/cards` traz só NVidia, a
webcam C920 e a Generic. Isso não é detalhe: metade das perguntas desta leva **só
se responde no cabo**, e metade **só se responde no rádio**.

| peça | cabo | rádio |
|---|---|---|
| **Microfone** | `medido` — **mas a evidência é o arquivo do WirePlumber**. Rebaixar | **medido de verdade**: protocolo conferido byte a byte, Opus decodificado, A/B de taxa em três janelas. É a única célula desta família com medição que sustenta o rótulo |
| **Saída de som** | medido o **nome do sink**. Qual canal faz o quê: **não medido** | declarado `nao-tem` por falácia do perfil ausente. **O caminho existe, está escrito neste repositório, e tem zero linhas de implementação.** **15/08: o CANAL foi medido** — o firmware executa `0x32` e `0x39` por rádio. **O payload continua não identificado** |
| **Giroscópio** | **legítimo**: 250,0 Hz por duas réguas independentes mais o `bInterval` 6 do descritor | **legítimo** (rajadas de 38 a 392 Hz), mas contradiz a célula irmã (3.5) |
| **Acelerômetro** | `inferido-do-codigo`. **Continua não medido** — não há controle no cabo | **MEDIDO HOJE**: 0,9945 g e 0,9823 g. Funciona, chega calibrado, sem comando de ligar |
| **Jack (fone plugado)** | curado por nós | o bit **chega** e o driver o descarta por política. Endereço conhecido: byte 55, bit 0 |
| **Escolha fone x alto-falante** | registrador HID `OUTPUT_PATH_SEL`, **por controle**, endereçado por `uniq`, **já implementado** | mesma coisa, e por rádio nem depende de sink: é a tag do bloco (`0x13` x `0x16`) |

**A conclusão honesta da assimetria:** o rádio não é o transporte pobre que o
mapa desenha. **Ele tem um caminho de áudio próprio, de saída E de entrada, que a
documentação oficial não cobre porque a documentação oficial é focada no cabo —
exatamente o que ela disse hoje.** A metade de entrada desse caminho **já roda em
produção aqui desde 25/07**. A de saída tem o transporte provado pelo descritor
**e, desde 15/08, a ACEITAÇÃO provada no firmware** — e **zero implementação, e
zero conhecimento do formato do payload**.

---

## 5. ONDA 1 — o que eu faço sozinha

Zero pixel novo, zero byte escrito no aparelho, zero decisão dela.

### 1.1 A redação honesta nas quatro células que fecham a porta sem prova

Substituir os quatro textos da tabela 3.2, cada um **com a lista do que já foi
descartado** — é isso que faz a redação honesta ser **mais** útil que a antiga, e
não menos. Trocar `existe = nao-tem` por `existe = desconhecido` nas três que
cabem.

**Mordida:** portão de texto que reprova a palavra "impossível" em qualquer
célula do mapa sem um campo irmão que diga **como** a impossibilidade foi
provada; e que reprova `existe = desconhecido` com o campo de comando vazio (o
que descartamos é obrigatório). Arranque a cura, devolva o texto antigo, veja
reprovar.

### 1.2 Rebaixar as seis células que medem outra coisa, e esvaziar as quatro vazias

**Conserto, não trabalho novo.** O produto não muda uma linha; só o mapa passa a
dizer a verdade. **Depende da D-14** — porque o preço é o mapa parecer que sabe
menos do que ontem.

**Mordida:** com as seis rebaixadas, o censo do portão tem de sair de **48** para
**42** afirmações fortes. Um teste que trava esse censo reprova quem repromover
sem ensaio.

### 1.3 A regra `medido-sem-quem-provou`, no portão

`confianca = medido` passa a exigir `provado_em` (data) **e** `provado_por` em
{`aparelho`, `olho-dela`, `descritor`}. `fonte-do-driver` e `inferido-do-codigo`
**não** sustentam `medido`.

**Sem esta regra o defeito volta**, porque `medido` continua ganhável por um
teste unitário que afere o nosso próprio byte. Rodar primeiro **em modo AVISO**,
como a casa já fez, e **publicar o número de reprovações antes de promover** — o
número é a dívida.

**Mordida:** uma linha sintética com `confianca=medido` e `provado_em` vazio tem
de reprovar; arranque a regra e ela passa.

### 1.4 Uma regra a mais, que é a que deixou o defeito nascer

Célula cuja **evidência é a AUSÊNCIA de algo** (*"a busca devolve ZERO"*, *"não
há uma linha"*, *"nenhuma ocorrência"*) **não pode** ter confiança `medido`. Foi
assim que *"canais 3-4 = voice-coil"* passou por medição por três semanas.

### 1.5 Registrar o `0x22`, o `0x0b` e o `0x08` — o mapa não sabe que eles existem

Linhas novas na canônica e no CSV, com o grau de cada campo separado: `medido`
**só** para o que eu medi (existência, tamanho, o MAC em little-endian conferido
contra o sysfs) e **não sei** para os dois blocos de oito bytes. Mais a lista
datada do que **não** foi sondado e **por quê**: `0x80`-`0x83` (comandos de
teste, risco não medido) e `0xf0`-`0xf7` (canal de atualização de firmware, não
tocar sem decisão dela).

### 1.6 Fechar a nota de 11/08 da canônica: não era contradição, era aritmética

A canônica registra uma *"CONTRADIÇÃO INTERNA EM ABERTO"* entre `0x32`/tag `0x12`
e `0x39`/tags `0x13`-`0x16`, e manda *"não escolher um lado"*. **Não há lado a
escolher:** o TLV é o mesmo em toda a escada e o report ID escolhe só o
**tamanho** do envelope. Um projeto manda 75 B de blocos e por isso usa o `0x32`;
o outro manda 540 B e por isso **precisa** do `0x39`.

**Isto não apaga decisão medida** — a nota de 11/08 registrou uma dúvida honesta,
e a dúvida foi resolvida. A data de 11/08 fica citada como o dia em que a dúvida
se abriu. A nota nova tem de conter os offsets, ou falhou: quem ler a página
precisa saber montar o `0x39` sem abrir o navegador.

### 1.7 Tirar a premissa derrubada de dentro da justificativa do teto de silêncio

O teto de 30 s fica; a frase que o justifica troca (3.5). Dois lugares: o
comentário em `src/hefesto_dualsense4unix/core/physical_report_reader.py` e a
célula do mapa.

### 1.8 Pôr o caminho do broker dentro dos instrumentos

**Medido hoje:** `/dev/hidraw8` e `/dev/hidraw10` (os DualSense reais por BT)
estão `crw------- root:root`, **sem ACL** — enquanto os vpads estão 0660 com ACL
para ela. Por isso `scripts/capture_blueprint.py` **falha hoje** com
`Permission denied`, e por isso toda medição de feature report nesta casa passou
a exigir `sudo` sem ninguém perceber.

O caminho que funciona **sem sudo** já existe no produto e não está em nenhum
script de medição: pedir o fd ao `hefesto-hidraw-broker`, que roda como root e o
passa por `SCM_RIGHTS`. Foi assim que todas as sondas de hoje rodaram.

**Mordida:** rodar o script com o nó escondido pelo broker. Hoje devolve
"inacessível"; depois tem de devolver os três features. Arranque o fallback e o
teste volta a reprovar.

### 1.9 Os dois helpers de cor, que a onda 3 consome

**Um dono só da cor:** uma função pura, irmã da que já resolve o destaque do
card, devolvendo `None` quando não há cor conhecida (desconhecida, apagada,
Nativo sem última cor). E **um mecanismo de pintura**, no molde do que já tinta a
barra de progresso: passa por `ensure_min_contrast`, instala um `Gtk.CssProvider`
**por widget**, guarda o hex para ser no-op quando a cor não mudou.

**Armadilha medida, e ela morde calada:** o tema do **sistema** anima
`border-color`. Medir logo depois de instalar o provider devolve um valor de
meio-caminho — na primeira tentativa eu li `(188,147,248)` e quase escrevi que o
provider não funcionava. **Um teste que afira a cor renderizada sem bombear o
laço principal será intermitente.** Por isso o teste afere **o hex devolvido**,
nunca `get_border_color`.

**Mordida:** arranque o `ensure_min_contrast` e a chamada com preto tem de
devolver `#7e7e7e` (3,02:1), não `#000000` (1,71:1).

### 1.10 Os instrumentos de medição, escritos e prontos para ela apertar play

Nenhum roda sozinho — todos são da onda 2. O que a onda 1 entrega é **o
instrumento**, com o cabeçalho declarando **qual biblioteca e qual transporte**
(armadilha 1 da casa) e recusando rodar quando disputaria o hidraw com o daemon
(armadilha 3):

1. **Censo de GET_FEATURE** — ler os catorze features desconhecidos, no cabo e
   por rádio, gravando o dump cru. Depois procurar nos bytes devolvidos os
   valores que acabamos de escrever (volume, rota, pré-amp, mudo). **Se algum
   ecoar, `audio.leitura_de_volta` deixa de ser `nao-tem`.**
2. **Censo de cor** — os mesmos features nos **quatro** controles, tabelados
   contra a cor que **ela** declara olhando o plástico.
3. **Sonda do byte 55** — leitura pura pelo broker, contando também os reports
   por segundo com o controle parado (o que desempata a contradição 3.5, e que o
   evdev **não** consegue desempatar por causa do filtro `fuzz=16`).
4. **Gerador dos quatro WAV de quatro canais** — um tom em um canal por vez.
5. **EXP-SPK-01** — o montador do `0x39`, que **não roda sem a D-24**.
   **Em 15/08 ele ganhou cinco irmãos mais baratos que vêm ANTES dele**, na
   [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md):
   variar os bytes extras, subir os degraus `0x33`-`0x38`, decidir o byte `[2]`
   do envelope, ler o `0xF6` e replicar no cabo. O instrumento dos seis mora em
   `scripts/ensaios/`, ao lado dos quatro que já existem.

**A mordida que vale para todos:** o instrumento tem de dizer **qual controle
respondeu**, e o casamento `hidrawN` -> `uniq` vem do `uevent`, nunca da ordem de
enumeração. Rode com os nós trocados na linha de comando: se o relatório não
trocar de endereço junto, ele está lendo a ordem e não o aparelho — que é
*"o instrumento mente mais que o produto"*, a armadilha que já produziu três
medições falsas num dia só nesta casa.

---

## 6. ONDA 2 — o que precisa das mãos e da orelha dela

**É a onda que tira os achismos.** Nada aqui se decide lendo código.

### 2.1 Cinco minutos que decidem o canal 3 — e eu quero que ela responda às cegas

**A de melhor razão valor/custo da leva inteira**, e a que responde ao item 4 do
pedido dela.

- **Precisa:** um DualSense **no cabo**; nenhum fone plugado no controle; o
  controle **na mão dela**, não na mesa. O daemon pode ficar de pé — nada aqui
  toca hidraw.
- **Biblioteca declarada:** ALSA/PipeWire. Nenhuma SDL envolvida.
- **Passo 0, confirmar o instrumento:** o `stream0` da placa tem de dizer
  `Playback: Channels 4` e `Channel map: FL FR RL RR`. Se não disser, **pare** —
  o resto não vale.
- **Controle positivo, obrigatório e primeiro:** os canais 1 e 2 **têm** de sair
  pelo alto-falante. Se não saírem, o instrumento está errado e nada do resto
  conta.
- **O gesto:** um tom de 440 Hz em **um canal por vez**, e ela diz, para cada um:
  **OUVIU**, **SENTIU na mão**, ou **nada**. Depois repete com o fone plugado.

| o que ela sentir no canal 3 | o que fica provado |
|---|---|
| sentiu vibração fina e não ouviu | canais 3-4 **são** os motores. A célula do mapa vira `medido` e o modelo dela cai |
| ouviu o tom pelo alto-falante | **o canal 3 é saída de som e ela está certa** |
| nem ouviu nem sentiu, com volume no máximo | o `chmap` declara quatro canais e **não há transdutor atrás de 3-4** — e isso também é resposta, e também é `medido` |

**Por que às cegas:** se eu contar a expectativa antes, contamino a única medição
desta leva que depende do corpo dela. É a **D-28**.

### 2.2 Dez minutos que podem curar o defeito mais caro do microfone por BT

O autor da ponte escreveu, em 25/07, qual era o próximo experimento **e por que
não pôde rodá-lo**: *"parar o daemon estava fora do que esta tarefa podia
tocar"*. **Ele continua não rodado.** O instrumento já existe e já imprime o
número.

Três janelas de 60 s: **A** com o daemon vivo, **B** com o daemon parado, **C**
de volta ao estado A — e a terceira é o que prova que o efeito é reversível e não
um estado preso no firmware. Foi exatamente a terceira janela que salvou a
medição de taxa de 25/07 de virar conclusão errada.

**Critério:** se o `mudo%` cair de ~60% para perto de zero, o culpado é o
**segundo escritor** — o daemon, que escreve `common[9]` a 60 Hz com
`POWER_SAVE_CONTROL_ENABLE` sempre asserido — e a cura é **dar dono ao byte**, um
padrão que esta casa já aplicou. Se não mudar nada, o gating é do firmware, três
hipóteses já caíram, e a quarta terá de ser desenhada.

**Armadilha a dizer em voz alta:** com install editable, **o daemon vivo é mais
velho que o código**. Meça primeiro, edite depois.

### 2.3 Cinco minutos para derrubar (ou confirmar) "não há jack por Bluetooth"

Ela pluga e despluga um fone P2 enquanto a sonda roda. **O bit 0 do byte 55
alterna com o gesto** -> o aparelho reporta o jack por rádio e a célula vira
`medido`. **Não alterna em 20 plugadas** -> aí sim isto é **prova de
impossibilidade para este bit**, datável, e vale escrever com essas palavras.

**O daemon pode ficar de pé, e é importante dizer por quê** para ninguém
"consertar" isto depois: no Linux cada fd aberto de um hidraw tem a **própria
fila de entrada**, então um leitor a mais não rouba report do daemon. A disputa
que esta casa já pagou era de **escrita**. Aqui não se escreve nada.

### 2.4 O acelerômetro no cabo — o espelho do que eu já medi por rádio

Mesmo método, mesma régua. **Critério de sucesso:** módulo entre 7800 e 8600.
**Critério de fracasso interessante:** se o módulo der certo mas os **eixos**
estiverem trocados em relação ao rádio, isso é uma assimetria de transporte real
— e é exatamente o tipo de coisa que o mapa existe para pegar. E o passo que
fecha a peça: girar 90 graus e ver o eixo que era -8192 ir a zero. **Sem isso
você mediu que chega um número; com isso você mediu que o número significa
aceleração.**

### 2.5 O censo de cor: os quatro na mesa, zero escrita

**A única medição que decide o item 1 do pedido dela.** Ler os features `0x20`,
`0x22` e `0x0b` dos **quatro** e tabelar contra a cor que ela declara.

A pergunta é falseável e binária: **existe algum byte em que controles da mesma
cor coincidem e os de cor diferente divergem?**

- **Sim** -> candidato a código de cor, e vira hipótese testável.
- **Não** -> a casa passa a poder escrever, **com data e tamanho de amostra**,
  *"quatro unidades, quatro cores, nenhum byte de `0x20`/`0x22`/`0x0b`
  correlaciona com a cor"*. **Que é informação útil, e não é "impossível".**

**Já medi dois:** diferem em quatro bytes no `0x20` e em dois blocos de oito
bytes no `0x22`. **Faltam os outros dois e o rótulo de cor de cada um — que só
ela pode dar.** É a **D-27**.

> **FEITO EM 15/08/2026, e a resposta foi "não" — com a ressalva que importa.**
> Os quatro foram lidos, por rádio. **Nenhum byte de `0x20`, `0x22` ou `0x0b`
> correlaciona com a cor.** O que parecia candidato tem explicação melhor: os
> offsets 45-51 do `0x22` mudam com a **`sw_series`**, não com a cor (ASCII nos
> dois de série 11, binário nos outros dois), e o `device_info[12]` do `0x20`
> difere por unidade mas **ninguém no mundo decifrou** o que ele é.
>
> **E a ressalva é o achado:** *"não está no `0x20`/`0x22`/`0x0b`"* **não** é
> *"não está no aparelho"*. Está — no serial, por `0x80`/`0x81`, com uma escrita
> antes. Ver a **D-15** reescrita e a
> [canônica](../../protocol/dualsense-referencia-canonica.md).

### 2.6 O censo de GET_FEATURE: os dezessete reports que o aparelho declara

> **ENTREGUE EM 15/08/2026.** Esta entrega dizia *"catorze reports que o
> aparelho declara e ninguém leu"*. **Os dezessete foram lidos, nos quatro, por
> rádio** — e a tabela do que cada um trouxe, com tamanho declarado pelo próprio
> descritor, mora na
> [canônica](../../protocol/dualsense-referencia-canonica.md), em *"Os feature
> reports — o censo dos dezessete"*. Qualquer célula do mapa que ainda diga
> *"catorze que ninguém leu"* está desatualizada a partir desta data.
>
> **Três coisas saíram de lá, e as três são caras:**
>
> 1. **Por rádio se REPETE a leitura.** O timeout de 3 s do BlueZ custa 3,2-3,7 s
>    por falha, e **um dos quatro só respondeu na quinta tentativa**. Ler uma vez
>    e concluir *"não tem"* é a FALÁCIA DO PERFIL AUSENTE com nome e endereço.
> 2. **Valide `buf[0] == report_id`.** Um dos quatro devolveu `0x80` no lugar do
>    `0x20` pedido — resposta trocada, não erro. Sem a validação se parseia o
>    report errado com o layout certo, e o tamanho ainda bate.
> 3. **`0x80`-`0x83` e `0xf0`-`0xf7` devolvem constante idêntica nos quatro
>    quando lidos SEM comando prévio.** Não é que estejam vazios — é que essa
>    família responde ao que foi pedido antes. É a chave da D-15.

Leitura pura, mas mexe no hidraw que o daemon segura. Era a medição **mais
barata e mais decisiva** que ficou na mesa em 14/08.

### 2.7 EXP-SPK-01 — fazer o alto-falante tocar por Bluetooth. **Depende da D-24.**

> **REDESENHADO EM 15/08/2026, e ele deixou de ser o primeiro passo.** O ensaio
> desta seção continua válido inteiro e virou o **E-5** da
> [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
> — o **último** de seis, e não o primeiro. O motivo é medido: o `0x39` já foi
> escrito e **executado** pelo firmware em 15/08, e isso **não** disse nada
> sobre o formato do payload. Escrever um codificador Opus antes de saber onde o
> payload mora é gastar bancada dela contra um formato que ninguém sabe se está
> naquela posição. Os cinco ensaios que vêm antes custam 55 minutos somados e um
> deles (o `0xF6`) **não escreve byte nenhum**.

Um script de bancada, **fora de `src/`**, que monta **um** report `0x39` de 547 B
e o escreve a 50 Hz por 3 segundos.

**Três controles obrigatórios, porque "achei que ouvi" não é medição:**

1. o mesmo report **com o bloco `0x13` removido** — não pode sair som;
2. o mesmo report **com o CRC deliberadamente errado** — não pode sair som, o que
   prova que o firmware está de fato **consumindo** o nosso pacote;
3. **gravar pelo microfone da webcam C920** e conferir o pico em 440 Hz por FFT,
   em vez de confiar no ouvido.

**Por que o risco de brick é nulo, e isto tem de estar escrito no cabeçalho do
script:** é um output report HID **de tamanho declarado pelo próprio descritor do
aparelho**, pelo canal de interrupção, com CRC válido. Não é feature report, não
escreve NVS, não toca firmware, e o firmware descarta em silêncio qualquer report
BT com CRC errado. **É a mesma classe de escrita que a ponte do microfone já faz
nesta casa desde 25/07.**

**Critério de sucesso: a orelha dela.** Nada de log, nada de "aceito sem erro" —
o `write` devolver 547 não prova coisa nenhuma. É exatamente o que
`test trigger --raw` fazia quando imprimia "aplicado" sem ter aplicado.

**Critério de parada honesta:** se nada sair depois de esgotar as variações, a
redação certa é *"não encontramos o formato do bloco `0x13`; descartamos A, B e
C; o transporte está provado e o descritor declara o degrau"* — e **nunca**
*"não dá"*.

**Três resultados, e os três são informação:** ouviu (o caminho é esse); não
ouviu mas o report foi aceito (SAIU NO FIO, falta o formato do payload); report
recusado (o degrau ou o bloco estão errados).

### 2.8 O relógio do próprio controle, que ninguém leu

O `sensor_timestamp` de 32 bits, em unidades de 0,33 us, vem em toda janela de
motion. **Se o relógio do controle disser 250 Hz constantes enquanto o host vê
rajadas de 38 a 392 Hz, então o firmware amostra parelho e é o RÁDIO que
agrupa** — e aí *"o BT entrega menos gyro"* é afirmação sobre o link, não sobre o
sensor. Se o relógio do controle também variar, é outra história inteiramente.

**Critério de fracasso:** se o delta der constante entre reports que o host
recebeu em rajada, **confira antes de comemorar** que você não está lendo os
mesmos quatro bytes duas vezes. Valide a régua contra contagem independente.

---

## 7. ONDA 3 — o que precisa do olho dela

**Nada aqui começa antes das decisões da seção 8.** Onda de tela é a mais cara de
refazer, e a PROVA-DE-TELA-01 existe exatamente para que ninguém gaste 500
minutos contra um desenho que ela vetaria em dez segundos.

### 3.1 A borda de identidade nas guias do alvo. **Depende da D-15 e da D-18.**

**Medido, e é o que torna a entrega barata:** os dois seletores **não existem no
Glade** — a fita *"Ajustes vão para:"* e a faixa *"Número deste controle:"* são
montadas em Python e penduradas no `header_bar`. Não há id de widget para os
chips nem para os botões 1 2 3 4. Logo a entrega é toda em
`src/hefesto_dualsense4unix/app/actions/status_actions.py`.

**Medido também:** a caixa `linked` **não funde** as bordas — chips vizinhos
mantêm cada um a sua, produzindo uma costura de 2 px com as duas cores. **Cada
controle fica com o contorno fechado na cor dele, nos quatro lados, que é
literalmente o que ela pediu.**

**A colisão principal, e ela é de produto:** hoje a **borda é a marca de
SELEÇÃO** em toda a janela. Se a borda passar a dizer identidade, a seleção fica
só com o fundo — que separa marcado de não marcado por **1,28:1**, abaixo de
qualquer piso. **A cura medida:** um anel `box-shadow: inset` de 2 px por dentro,
que **não muda um pixel de tamanho** e por isso é imune ao defeito de tremor de
borda que a casa já proibiu.

**Armadilha de implementação, e ela morde calada:** a função que redesenha a fita
tem um **early-return de idempotência** que dispara no caso comum (mesmos
rótulos, mesma posição). **Se a pintura ficar depois dele, a cor nunca acompanha
ela repintando a lightbar** — só mudaria quando um controle entra ou sai. A
pintura tem de ficar **antes**, no mesmo lugar onde a faixa de número já foi
posta exatamente por este motivo, com comentário escrito.

**Mordida:** mover a pintura para depois do early-return e mandar dois estados
seguidos em que **só** a cor muda. O teste exige que a borda tenha mudado — e
reprova. **Esse é o defeito que ninguém veria em foto estática.**

### 3.2 O seletor de jogador 1 2 3 4 na cor de quem ocupa cada número. **Depende da D-17.**

**Mordida:** o fixture dos quatro já tem `player_slot` **desalinhado** do índice
de propósito (slots 4, 1, 3, 2 nos índices 0 a 3). Trocar o mapa por índice de
enumeração faz as cores saírem na ordem errada e o teste reprova. É a mesma
família de defeito que a PLAYER-01 já curou no rótulo.

### 3.3 A foto que prova a metade que hoje **nenhuma foto mostra**

**Medido:** o fixture da mesa cheia tem `output_target_index` nulo, então a faixa
*"Número deste controle"* fica **escondida em toda foto do repositório**. Sem
consertar isso, a prova de tela cobre só as guias e **metade desta onda não tem
prova**.

Junto: acrescentar ao dublê um quinto caso com a fonte de cor **desconhecida** —
o desenho de borda neutra que a D-1 mandou fazer **não aparece em foto nenhuma
hoje**.

**Mordida:** contar cores distintas na primeira linha do PNG do cabeçalho. Sem a
pintura, saem todas iguais e reprova. E o portão de privacidade das fotos já
existe e o fixture novo tem de passar por ele.

### 3.4 O verbo certo nos quatro botões, dentro da janela. **Depende da D-19, D-20, D-21.**

**A distinção que barateia a leva inteira, e ela precisa da palavra dela:**
*"navegar a janela do Hefesto"* **não passa por uinput**. A GUI move a própria
página e a própria cadeia de foco, consumindo estado de botão que o daemon **já
publica**. Logo **não precisa de N cursores virtuais** — e a objeção que
sustentava os ~960 a 1200 min da rota *"cada um escolhe o seu"* (quatro mouses
virtuais somando no mesmo ponteiro) **não se aplica a esta metade**. Continua
valendo inteira para a outra metade: cursor e teclado do sistema.

**Isto não contradiz a resposta dela à D-10** — ela respondeu sobre **comandar o
PC**. Consequência: a aba Navegação passa a ter duas seções sob o mesmo nome,
*"Comandar o PC"* (as duas colunas de hoje, intactas) e *"Navegar esta janela"*.

**O gate, em duas pontas, e as duas precisam existir:**

- **na GUI:** aceitar input de controle só com a janela ativa — a GUI sabe o
  próprio foco nativamente, sem daemon e **sem cegueira em Wayland nativo**;
- **no daemon:** um termo novo no predicado que **já existe** para exatamente
  esta pergunta, lendo a classe da janela em foco **crua**, nunca a pegajosa.

**Mordida:** montar o store com a classe `"unknown"` — **o valor medido quando o
jogo está em foco** — e afirmar que o predicado **não** libera a navegação.
Arrancar a comparação reprova, e esse é literalmente o caso do Alt+Tab dentro do
jogo que ela reclamou em 29/07.

**Segunda mordida:** dois snapshots em sequência têm de avançar a aba
**exatamente uma vez**; um terceiro com o botão ainda pressionado não pode
avançar de novo. Sem a detecção de borda, a aba dispara **30 vezes por segundo**.

### 3.5 A tela dizer quem está navegando, com a cor dele

Um badge no cabeçalho, no molde exato do *"Editando: Controle N"* que já está lá,
com o léxico que já existe: **"Navegando: Sony 3 · BT"**. **Como se entra:** o
controle que apertar um botão de navegação com a janela em foco vira o dono.
**Como se sai:** o botão PS, ou a janela perder o foco — e nos dois casos o badge
some na hora.

**Mordida:** dois controles, o 3 navegando — o texto **não pode** conter o rótulo
do outro. Arrancar o carimbo do endereço no badge (deixando-o mostrar o alvo de
**edição**, que é outro estado) faz o teste reprovar.

### 3.6 Enquanto um navega, o botão dele não chega ao jogo. **Depende da D-22.**

Há **uma linha só** para isso no co-op, e o irmão dela para o primário. Mascarar
**só os quatro botões** e não o snapshot inteiro — os analógicos continuam indo
ao jogo, que é o que evita o personagem travar na tela. E **soltar o que estiver
preso na borda de entrada**, pelo mesmo motivo já pago: fechar o portão com um
botão segurado deixa a tecla presa (18 s numa noite, 33 s na outra, medidos no
journal dela).

**Mordida:** com o jogador 2 como dono da navegação, o vpad **dele** não recebe
`cross` e o do jogador 3 recebe. **Esse assert é a diferença entre "apertei X
para escolher na tela" e "apertei X e meu personagem pulou".**

---

## 8. ONDA 4 — as perguntas que são dela: D-13 em diante

Cada uma com **o que muda em cada resposta**. As D-1 a D-12 estão em
[as onze respostas](../2026-08-14-DECISOES-DE-PO-as-onze-respostas-da-mesa-cheia.md)
e continuam valendo.

### D-13 — As duas colunas do mapa dizem coisas diferentes com nomes parecidos

`confianca` tem **98 células** `medido` e é ganhável por um teste unitário do
nosso próprio byte. `grau` tem **15 células** `O APARELHO OBEDECEU` e exige
ensaio de bancada. **A segunda concorda exatamente com o que você disse hoje.**

| resposta | o que muda |
|---|---|
| **`confianca` vira derivada do `grau`** | uma coluna só, o mapa **encolhe**, e o rótulo para de mentir por construção |
| **ficam as duas, com o cabeçalho dizendo em uma linha que uma mede o CÓDIGO e a outra mede o APARELHO** | nada quebra, mas a confusão continua possível para quem não ler o cabeçalho |

**Manter as duas com nomes que se confundem é o que fez o mapa mentir sem
ninguém mentir.**

### D-14 — Rebaixar seis células de `medido` para `inferido-do-codigo`

O censo do portão sai de **48** para **42** afirmações fortes. **O produto não
muda uma linha.**

**O preço, e é real:** o mapa passa a parecer que sabe **menos** do que ontem —
mesmo sabendo que algumas dessas coisas provavelmente **funcionam** (o volume do
alto-falante no cabo, por exemplo). A regra da casa diz que sim, é para rebaixar.
**Confirma?**

### D-15 — Que cor é "a cor física dele"?

> **REESCRITA EM 15/08/2026, e a versão anterior estava ERRADA.** Até hoje esta
> decisão dizia que a cor do plástico *"não existe em lugar nenhum do código"* e
> que *"a leitura a partir do aparelho nunca foi tentada, e eu não achei campo
> HID que a reporte"*. **A segunda metade é falsa desde 10/08/2026:** o caminho
> foi achado naquele dia, ficou enterrado num transcrito de subagente, e nunca
> virou página — a sprint UNIDADE-COR-01 está aberta e não começada desde
> então. O censo dos dezessete feature reports, feito nos quatro aparelhos em
> 15/08, fechou o resto. **Se você decidisse com a redação antiga na mesa,
> decidiria com informação errada**, e é por isso que a linha foi substituída em
> vez de anotada — número errado sai, medição cara leva data. Esta é a data.

São **duas coisas diferentes** e você usou a palavra "física", o que aponta para
a segunda:

| resposta | o que muda |
|---|---|
| **a cor VIVA da lightbar** (o que a D-1 já decidiu para a marca do jogador) | **chega na janela a 2 Hz e é só pintar.** Mas dois controles com a mesma luz ficam com guias iguais |
| **a cor do PLÁSTICO** (o colorway de fábrica) | **o caminho existe e está identificado** — não é mais "não achei". O que falta é a sua palavra sobre percorrê-lo, e é isso que a pergunta abaixo pede |
| **as duas, em superfícies diferentes** | a viva no **miolo** (D-1 intacta, mesmo dono da verdade) e o plástico no **contorno**. Cada uma responde a uma pergunta: *"que luz está acesa agora?"* e *"que peça é essa na minha mão?"* |

#### O caminho da cor, como ele realmente está hoje

A cor de fábrica está no **serial impresso na traseira**, de 17 caracteres, nos
**caracteres 5 e 6**. Lê-se assim:

```
SET_FEATURE 0x80, payload [0x01, 0x13]     (base = 1, num = 19)
GET_FEATURE 0x81 -> 64 bytes
    buf[1] == 1, buf[2] == 19, buf[3] == 2      (senão é erro, não dado)
    buf[4..20] = 17 caracteres ASCII = o serial da traseira
    cor = serial[4:6]        '00' White · '02' Cosmic Red · '04' Galactic Purple
                             '05' Starlight Blue · '09' Cobalt Blue · e mais dez
```

**Três fontes independentes concordam** (`dualshock-tools.github.io`, com o
mantenedor confirmando na issue #210; `nsfm/dualsense-ts`; `TechAntohere/Senshi`).
A tabela completa e os graus estão na
[canônica](../../protocol/dualsense-referencia-canonica.md), em *"O caminho da
cor do plástico"*.

**E aqui está o preço, que é a parte que a decisão precisa ver:**

1. **Ler exige ESCREVER.** O `GET_FEATURE 0x81` só devolve o serial depois de um
   `SET_FEATURE 0x80`. Sem o comando prévio, `0x80` a `0x83` devolvem a mesma
   constante nos quatro aparelhos — **medido em 15/08 nos seus quatro**.
2. **A escrita é da família de comandos de FÁBRICA.** É a mesma família em que
   `[1, 1]` **reseta o controle** e `[12, 1, ...]` **grava calibração na NVS**.
   O par `[1, 19]` é leitura pura — mas **byte errado no payload escreve onde
   não devia**, e não há desfazer.
3. **Só está provado POR CABO.** O `dualshock-tools` **recusa Bluetooth de
   saída**. Por rádio ninguém demonstrou — o que **não** é o mesmo que
   impossível, e é justamente o que o **ENSAIO 2+2** (seção 11) mede.
4. **O que já foi descartado**, para você não pagar de novo: PID, `info` do
   BlueZ, `iSerialNumber` USB (é o MAC, não o serial do produto), part number,
   prefixo de MAC, e os offsets 45-51 do `0x22` (mudam por `sw_series`, não por
   cor). O `hardware_version` do sysfs **separa os seus quatro hoje, mas por
   acaso de lote** — dois controles da mesma cor comprados juntos teriam o mesmo
   valor.

**A pergunta, então, não é mais "existe?". São três caminhos, e o preço de cada
um:**

| caminho | o que custa | o que entrega |
|---|---|---|
| **(a) não fazer** | **zero risco.** Você escolhe a cor de cada controle na interface **uma vez**, e ela fica salva por MAC (D-16 já decidiu que é da PEÇA) | a tela pinta certo hoje à noite, e nunca escreve nada no aparelho |
| **(b) fazer POR CABO, um de cada vez** | é o **caminho provado**, e ainda assim é escrita na família de fábrica. Um controle no cabo por vez, com o daemon parado ou pelo broker | a cor sai do próprio aparelho, sem você digitar nada — inclusive para controle que você comprar depois |
| **(c) tentar POR RÁDIO** | **território não demonstrado.** Some ao risco da escrita o transporte que já mostrou timeout e resposta trocada no censo de hoje | o mesmo de (b), sem cabo — se funcionar |

**A minha recomendação é (a) agora e (b) depois**, nesta ordem e por este
motivo: (a) entrega a tela hoje e não toca no aparelho; (b) vira melhoria
opcional, medida no ENSAIO 2+2, **sem que a interface dependa dela**. Assim
nenhuma escrita de fábrica fica no caminho crítico de um recurso visual.
**A palavra é sua.**

### D-16 — A cor do plástico é do PERFIL ou da PEÇA?

**Esta contradiz o item 3 do seu pedido, e a contradição é real.** Você pediu
*"tudo salva dentro do perfil ativo pra cada controle"*.

**Eu recomendo a PEÇA**, e o motivo é medido, não estético:

- o perfil **já excluiu identidade visível de propósito** — os overrides por
  controle têm quatro campos e o rótulo ficou de fora com a justificativa
  escrita;
- **a sua própria decisão de 10/08** diz que a cor da unidade vale *"hoje,
  amanhã, e com qualquer outro controle ligado ao lado"* — se morar no perfil,
  **trocar de perfil repinta o plástico na tela**;
- o arquivo por endereço já existe, é atômico, atravessa boot, e hoje lista os
  seus quatro DualSense.

**O que continua valendo para o perfil:** tudo que é **ajuste**. A cor do
plástico não é ajuste — é fato da peça.

### D-17 — Nos botões 1 2 3 4: a cor de quem OCUPA o número, ou a do escolhido?

| resposta | o que muda |
|---|---|
| **de quem ocupa** | a leitura vira *"a mesa inteira em quatro botões"*, e trocar o número **troca as cores de lugar** — que é a confirmação visual do gesto. Mais informativa |
| **a do controle escolhido no cabeçalho** | é a leitura literal do seu pedido, e os quatro botões ficam da mesma cor |

### D-18 — A borda pode ficar SÓ com a identidade?

Hoje **borda roxa = selecionado em toda a interface**. Medi que o anel por dentro
não muda um pixel de tamanho.

| resposta | o que muda |
|---|---|
| **sim, a seleção vira anel por dentro** | muda o vocabulário visual **em um lugar só** da janela, e as duas informações nunca disputam o mesmo pixel |
| **não, a seleção fica só com o fundo** | marcado e não marcado se separam por **1,28:1**, que é pouco |

**Duas de borda vêm junto:** (a) no modo de **alto contraste** do sistema, a
borda colorida some (o tema manda tudo amarelo sobre preto) ou vence? **Eu
deixaria o alto contraste vencer** — é o modo de quem mais precisa dele —, mas
isso significa que nesse modo os quatro ficam iguais de novo. (b) os botões de
controles **externos** na mesma fita ganham borda? A **D-7** já disse que *"cada
player"* inclui quem não é DualSense, mas **não medi se existe cor por unidade
para eles**.

### D-19 — "Navegar a janela do Hefesto" e "comandar o PC" são a MESMA coisa ou DUAS?

**É a pergunta que decide o preço da leva inteira.** Hoje são a mesma — é a aba
Navegação — e a resposta que você deu à **D-10** foi dada sobre a **segunda**.

| resposta | o que muda |
|---|---|
| **duas coisas** | os quatro controles podem navegar a janela **ao mesmo tempo, sem cursor virtual nenhum**, e os ~960 a 1200 min da rota *"cada um escolhe o seu"* **caem** — porque a objeção que os sustentava não se aplica a nada que não passe por uinput |
| **a mesma coisa** | a D-10 governa inteira, e a navegação por controle tem um dono por vez |

### D-20 — O R1 já tem dono

Hoje o padrão é `r1` = Alt+Tab e `l1` = Alt+Shift+Tab. **É o mesmo R1 que em
29/07 trocava de aplicativo dentro do jogo.**

| resposta | o que muda |
|---|---|
| **dois significados, decididos pelo foco** | dentro da janela do Hefesto é "aba", fora é Alt+Tab. **Nada quebra**, mas isso tem de estar dito na tela |
| **"aba" em todo lugar** | o Alt+Tab perde o botão dele, e quem usa o controle como teclado perde um atalho |

### D-21 — O verbo do círculo, e a volta do carrossel

**"Bola pra desescolher"** pode ser: desmarcar o que está selecionado; **voltar**
(devolver o foco à tira de abas); ou **sair** (fechar a janela). No PS5 o círculo
é sair; aqui "sair" pode ser voltar à tira em vez de fechar.

E: **R1 na última aba para, ou dá a volta para a primeira?** (No PS5 o carrossel
dá a volta; num aplicativo de desktop, normalmente para.)

### D-22 — Com o jogo aberto atrás, o X que escolhe na tela também chega ao jogo?

**Minha proposta é roubado** — e roubado **só nos quatro botões**, com os
analógicos ainda indo ao jogo, para o personagem não travar. **Mas isso significa
que, durante um segundo, o seu personagem não pula quando você aperta X.**

E: **os outros três seguem jogando normalmente** (é o que eu proponho, e a
supressão é por jogador, numa linha só) **ou tudo congela junto?**

### D-23 — A tabela de navegação por controle entra no perfil?

Isto **reabre uma decisão sua de 10/08**: o perfil **proíbe** mouse e atalhos de
teclado por unidade. A justificativa escrita lá é **a dívida do leitor único** —
que eu medi hoje e **ela caiu pela metade**: o co-op já cria um leitor por
endereço, e o `state_full` já publica os botões de cada controle separadamente.

**Proposta:** reabrir **só** para a tabela de navegação, mantendo mouse e
teclado proibidos — esses dois esbarram no cursor único e no foco único do PC,
que continuam sendo **um só**. É o que você mesma deixou aberto na D-10: *"a
parte que aguenta por jogador é a tabela de atalhos"*.

### D-24 — Autoriza o EXP-SPK-01, que escreve no controle?

> **ATUALIZADA EM 15/08/2026: a frase "é a única proposta desta leva que escreve
> no aparelho" deixou de ser verdade, e por decisão sua.** Na madrugada de 15/08
> você autorizou parar o daemon e escrever output reports por rádio, e foi assim
> que a escada foi medida — `0x31`, `0x32` e `0x39`, com você olhando a
> lightbar. **A classe de escrita, portanto, já foi exercida e nada quebrou.**
> O que a D-24 ainda pergunta é o que **muda** em relação àquilo: taxa (50 Hz
> por 3 s, contra alguns pacotes soltos) e conteúdo (payload de áudio, contra
> `common` de cor). É a **D-31**, que separa as duas coisas.

Escrever em `/dev/hidraw` de um controle seu **em Bluetooth**, a 50 Hz por 3
segundos, para tocar um seno de 440 Hz. O argumento de risco nulo está em 2.7.

| resposta | o que muda |
|---|---|
| **autoriza** | a pergunta do SFX por jogador sai do plano e vira medição, numa tarde |
| **não autoriza agora** | o mapa fica com a redação honesta de 5.1 (*"não encontramos, e aqui está o que descartamos"*) e o item 4 do seu pedido fica **plano** |

**E junto:** prefere que eu **pare o daemon** antes, ou que eu use o **broker**?

### D-25 — O alto-falante por rádio nasce LIGADO ou opt-in? E quem decide fone x alto-falante?

O microfone nasceu opt-in por privacidade **e** por banda. O alto-falante **não
tem problema de privacidade nenhum**, mas custa cerca de **três vezes mais
rádio** que o mic (~27 kB/s contra ~8 kB/s), **no sentido de saída**. Com quatro
controles na mesa isso é um orçamento novo, **e ele ainda não foi medido**.

E o segundo lado: **quando o fone está plugado no controle, quem decide?** O
protocolo separa por **um byte** (`0x13` = alto-falante interno, `0x16` = fone).
O firmware de referência tem três modos: segue o jack automaticamente, trava no
fone, ou desliga. **Isso vira escolha no perfil de cada controle, ou o Hefesto
segue o jack sozinho e pronto?**

### D-26 — O SFX do Sackboy sai do ALTO-FALANTE do controle ou do FONE plugado nele?

**A resposta muda o alvo, e muda muito:**

| resposta | o que muda |
|---|---|
| **do fone** | boa parte do caminho **já existe**: o registrador de rota é por controle, endereçado por `uniq`, já implementado |
| **do alto-falante por rádio** | é o EXP-SPK-01 inteiro (D-24), hoje o **E-5** da [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md) — e ele só começa depois que os ensaios de payload disserem onde o formato mora |

E, na interface, isso deve aparecer como *"SFX do jogador 1"*, *"Alto-falante do
controle 1"*, ou outro nome? **Você já me corrigiu que nome novo que não deriva
do léxico existente é sinal de conceito errado, e aqui eu não sei qual é o léxico
certo.**

### D-27 — O censo de cor, e as portas que eu deixei fechadas de propósito

**Três coisas numa:**

1. **Quantos DualSense você tem, e qual é a cor de cada um?** Sem esse rótulo o
   censo não decide nada — eu leio os bytes, **só você lê o plástico**.
2. **Posso sondar os reports `0x80` a `0x83`** (comandos de teste)? São leituras
   puras, mas **o risco de efeito colateral não está medido**. Eu **não** toco em
   `0xf0` a `0xf7` (canal de firmware) sem a sua palavra.
3. **Se o censo dos quatro der "nenhum byte correlaciona com a cor"**, você quer
   que a casa registre isso como **amostra fechada de quatro unidades**, ou quer
   que eu procure uma quinta unidade emprestada antes de escrever?

### D-28 — O ensaio do canal 3, às cegas

São dez minutos com o controle na sua mão, no cabo. **Eu quero que você diga o
que percebeu ANTES de eu dizer o que esperava** — vibração na palma, som pelo
alto-falante, ou nada. Se eu contar a expectativa primeiro, contamino a única
medição desta frente que depende do seu corpo. **Topa?**

**E uma de borda:** o acelerômetro passou a ser medido hoje. A célula do mapa
registra que ninguém nunca respondeu *"alguém quer o acelerômetro em número na
interface?"*. **Quer o número na tela, ou basta que ele chegue no jogo pelo vpad
(que já chega)?**

### D-29 — Duas coisas que eu medi de raspão e que são caras se ficarem sem dono

1. **O grab do controle primário está FALHANDO agora** —
   `primary_grab_state="failed"`, com `[Errno 16] recurso ocupado` no
   `/dev/input/event265` às 15:54. **Com o vpad de pé isso é input dobrado no
   jogo para o P1.** Abro frente própria?
2. **Os `/dev/hidraw` dos DualSense por BT estão `root:root` 0600, sem ACL**,
   enquanto os vpads têm ACL para você. O produto não sofre porque o broker passa
   o fd. **Isso é assim de propósito** (o broker é o dono único, e a regra 0660 é
   resto de uma era anterior), **ou é um portão que caiu sem ninguém ver?** A
   resposta muda se eu proponho conserto ou se eu proponho apagar a linha da
   regra.

### D-30 — A ordem de jogador: a que o produto GUARDA, ou a de chegada do momento?

**Acrescentada em 15/08/2026.** É decisão sua, você já a escreveu por extenso, e
ela ainda não estava numerada em lugar nenhum — que é exatamente o defeito que
esta casa nomeou como *"a casa sabe e a página não diz"*.

Às 03:54 de 15/08, depois de resetar e re-parear os quatro na ordem vermelho,
azul, branco, roxo, você escreveu:

> *"não, to falando que deve ser lembrado por ordem de conexão daquele momento
> apenas. **Não uma imagem fixa salva por mec**, o bond mesmo se desfaz com
> facilidade. Mas por exemplo conectamos hoje. Vermelho, deveria ser o player 1,
> azul, o player 2, branco o player 3, roxo o player 4. mas tá agora, vermelho
> 1, branco 2, roxo 3, azul 4 e a nossa ordem deveria sobrescrever a parte da
> steam inclusive igual quando descobrimos como fazer junto ao lightbar"*

**Há DUAS ordens no produto, e elas não são a mesma coisa:**

| ordem | onde mora | quando muda |
|---|---|---|
| **a persistida** (`rank`) | `controllers.json`, gravada **por MAC** na primeira vez que aquele endereço aparece | nunca, enquanto o arquivo existir |
| **a de chegada da sessão** | não existe hoje | a cada conexão |

**O produto guarda.** O que você viu — *"vermelho 1, branco 2, roxo 3, azul 4"* —
é o produto funcionando exatamente como projetado, com uma imagem fixa salva por
MAC. **Não é bug: é a decisão antiga que a sua decisão nova contradiz.**

| resposta | o que muda |
|---|---|
| **ordem de chegada do momento, e só ela** | o `rank` persistido deixa de decidir o número; quem chega primeiro é P1 hoje e pode ser P3 amanhã. É a leitura literal do que você escreveu |
| **ordem de chegada, com o arquivo só como desempate** | mesmo comportamento no caso comum, e o arquivo resolve empate de dois que conectam no mesmo instante |
| **continua persistida** | nada muda, e a sua frase de 03:54 fica sem efeito |

O mecanismo, lido no fonte, e o preço de cada caminho estão na
[ORDEM-DE-CHEGADA-01](2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md).
**E a terceira parte da sua frase — *"a nossa ordem deveria sobrescrever a parte
da steam"* — é pergunta separada e ainda não medida nesta sessão.**

### D-31 — A bateria de escritas da escada: autoriza?

**Acrescentada em 15/08/2026, e ela separa o que a D-24 juntava.**

Você já autorizou, nesta madrugada, escrever output report por rádio com o
daemon parado — e foi assim que se mediu que o firmware **executa** o `0x32` e o
`0x39`. O que os
[seis ensaios da escada](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
pedem agora é **mais do mesmo, em série**: cerca de 60 escritas de output, todas
com CRC válido e tamanho declarado pelo descritor do próprio aparelho, mais uma
rajada de 3 s a 50 Hz no ensaio final.

| resposta | o que muda |
|---|---|
| **autoriza a série inteira** | os seis ensaios rodam numa sessão de bancada de 1 h 25, e a escada sai medida degrau a degrau |
| **autoriza só o que NÃO manda payload** (E-1, E-2, E-3, E-6) | 45 minutos, e responde *"onde o payload mora"* sem tentar tocar som ainda |
| **só o E-4** | 10 minutos, leitura pura, zero escrita — e mesmo assim a casa aprende o que é o `0xF6` |

**O que não muda em resposta nenhuma:** nada disso é feature report, nada escreve
NVS, nada toca firmware. O risco de brick continua sendo o mesmo da ponte do
microfone, que roda aqui desde 25/07.

### D-32 — O `0xF6` e a família `0xF0`-`0xF7`: até onde?

**Acrescentada em 15/08/2026.** O `0xF6` é um FEATURE de 546 bytes que **só
existe no rádio** e é o gêmeo exato do OUTPUT `0x39`. A suspeita é que ele seja
**negociação** — dizer ao controle qual codec e qual taxa vêm a seguir.

**Ele mora na família `0xF0`-`0xF7`, que é o canal de atualização de firmware.**

| resposta | o que muda |
|---|---|
| **ler o `0xF6` (GET_FEATURE), e só ler** | é a minha recomendação. Leitura pura, sem escrita nenhuma, e responde se o conteúdo é constante (capacidade) ou por unidade (identidade) |
| **ler a família inteira `0xF0`-`0xF7`** | mais informação, mesma classe de risco — **desde que continue sendo só leitura** |
| **escrever (`SET_FEATURE`) em qualquer um deles** | **eu não faço isso sem a sua palavra explícita, e recomendo que você não a dê agora.** É o canal por onde o firmware é atualizado |

### D-33 — O nome da falácia gêmea

**Acrescentada em 15/08/2026, e é a mais barata da lista.** Esta casa nomeou em
14/08 a **falácia do perfil ausente** (*não achei, logo não existe*), e o nome
tem se pagado — foi ele que fez a palavra "impossível" cair da célula do áudio
por rádio.

A gêmea nasceu com o achado de hoje e eu proponho **FALÁCIA DO CANAL QUE
RESPONDE**: *respondeu, logo faz o que eu queria*. O nome deriva do léxico que já
existe, e as duas erram na mesma junta — confundir a medição estreita que se tem
com a afirmação larga que se quer.

**A palavra é sua**, e ela vale mais do que parece: nome errado não pega, e uma
forma de erro sem nome volta a acontecer.

---

## 9. As armadilhas desta leva, cada uma com endereço

1. **O instrumento mente mais que o produto.** Três medições falsas num dia só
   nesta casa. **Todo instrumento desta leva declara qual biblioteca e qual
   transporte no cabeçalho**, e o casamento `hidrawN` -> `uniq` vem do `uevent`,
   nunca da ordem de enumeração. Rode com os nós trocados e veja o relatório
   trocar junto.
2. **O instrumento pode estar brigando com o produto.** `test trigger --raw`
   disputava o hidraw com o daemon e imprimia "aplicado" sem ter aplicado.
   **Regra desta leva: leitura pode conviver com o daemon** (cada fd tem a
   própria fila de entrada); **escrita, não** — o EXP-SPK-01 exige o daemon
   parado ou o broker.
3. **`os.open` no hidraw dos DualSense por BT falha hoje**, `root:root` 0600 sem
   ACL. Quem "consertar" isso com `sudo` cria um **segundo dono do nó**. O
   caminho é o broker, que já existe no produto e não estava em nenhum script de
   medição (entrega 1.8).
4. **O daemon vivo é mais velho que o código.** Com install editable, cura de
   daemon só vale no **próximo start**, e o sintoma de esquecer isso é a
   **AUSÊNCIA** de dado novo, não um erro. Vale para a 2.2 inteira: **meça
   primeiro, edite depois.**
5. **O tema do sistema anima `border-color`.** Medir a cor renderizada logo
   depois de instalar o provider devolve valor de meio-caminho — eu caí nisso
   hoje e quase escrevi que o mecanismo não funcionava. **O teste afere o hex
   devolvido, nunca o pixel, a menos que bombeie o laço.**
6. **O early-return de idempotência da fita.** Pintura depois dele nunca
   acompanha a cor mudando (3.1). **É o defeito que nenhuma foto estática
   revela.**
7. **Sob Xvfb não há gerenciador de janelas:** `Gtk.Window` fica 1x1 para
   sempre. Toda foto desta leva é `Gtk.OffscreenWindow`
   ([COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md)).
8. **Pintar em aba escondida custa CPU medida.** Um poller cego já custou 104% de
   um núcleo nesta casa. **Nenhum `GLib.timeout_add` novo** — há portão que
   conta. O timer da navegação nasce **gateado pelo foco da janela**.
9. **Descritor prova DECLARAÇÃO, nunca ACEITAÇÃO.** A escada de OUTPUT existe no
   descritor dos dois controles dela; **isso não quer dizer que o firmware aceita
   qualquer degrau**. É a diferença entre a seção 2.1 e a seção 2.3 deste índice.
   **Atualizado em 15/08:** a aceitação passou a ser medida para `0x31`, `0x32` e
   `0x39`; `0x33` a `0x38` continuam **declarados e não testados** (é o E-2 da
   [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)).
10. **Este índice envelhece em minutos.** O de 31/07 registrou como pendente um
    item entregue **três minutos e vinte e dois segundos depois**, e a linha
    ficou nove dias na fila. **Quem entregar qualquer item daqui, volte aqui.**
    Em 15/08 este índice envelheceu em **horas**: quatro linhas dele afirmavam
    que ninguém tinha escrito no `0x39`.
11. **ACEITAÇÃO prova execução, nunca FINALIDADE** — a gêmea da armadilha 9,
    nascida em 15/08 junto com o achado. *"O firmware executou o report"* não é
    *"o report faz o que a gente esperava dele"*. A forma de erro é a **FALÁCIA
    DO CANAL QUE RESPONDE**, irmã da falácia do perfil ausente da seção 3.2: uma
    **nega** demais a partir do silêncio, a outra **afirma** demais a partir do
    eco. O nome está proposto na
    [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
    e a palavra sobre ele é dela (**D-33**).
12. **`os.write()` num hidraw devolve sucesso quando o KERNEL aceita a
    entrega** — ele **não** espera veredito do firmware. Em 15/08 ele disse
    "aceitou" para os quatro pacotes de um ensaio, **inclusive para o controle
    negativo de tamanho errado**, que tinha de ser recusado. **Todo ensaio desta
    família nasce com controle positivo E negativo**, e quem observa a lightbar é
    ela — o `write` devolver 547 não prova coisa nenhuma.

---

## 10. O que este índice NÃO mediu

**Escrito por extenso, porque nesta casa "não medi" é resposta legítima e "achei
que" não é.**

- ~~**O aparelho obedecendo o `0x39`.**~~ **MEDIDO EM 15/08/2026**, na mesa 2+2
  dela: o `0x32` (142 B) e o `0x39` (547 B) foram escritos por rádio e o firmware
  **executou** o `common` de 47 bytes dos dois — ela viu a lightbar acender verde
  e azul, com o `0x31` apagando entre um passo e outro.
  **E a lista não encolhe por isso, ela TROCA de item.** O que continua não
  medido, e é o que importa:
  **o CONTEÚDO do payload além do `common`.** Nem um byte dos 469 excedentes foi
  identificado. Que sejam áudio é **hipótese**, e o
  [ensaio que a decide](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
  está desenhado e não rodou. **Não se escreve, em documento nenhum desta casa,
  que o áudio por rádio foi descoberto ou que a ponte funciona — não funciona, e
  não há ponte.**
- **Os degraus `0x33` a `0x38`.** Declarados no descritor do rádio, **nunca
  tocados**. É o E-2 da sprint acima.
- **O `0xF6`** — FEATURE de 546 B que **só** existe no rádio, gêmeo exato do
  OUTPUT `0x39`, suspeito de negociação de codec e taxa. **Nunca lido.** É o
  E-4, e é leitura pura: roda sem autorização nenhuma.
- **Qualquer coisa que exija CABO.** No momento da medição não havia nenhum
  DualSense no cabo — os dois estão por rádio, e as três placas de áudio da
  máquina são NVidia, a webcam e a Generic. **A medição de "card1 com 4 canais FL
  FR RL RR" que outro agente citou hoje é de outro momento, com outra numeração
  de placa** — o `card1` de agora é a webcam. Portanto: mic no cabo, SFX no cabo,
  giro no cabo e acelerômetro no cabo continuam exatamente como estavam.
- ~~**O censo de GET_FEATURE dos catorze desconhecidos.**~~ **FEITO EM
  15/08/2026** — os dezessete lidos nos quatro, por rádio, com retry e validação
  de id. Resultado na
  [canônica](../../protocol/dualsense-referencia-canonica.md) e na entrega 2.6.
- **Se o aparelho OBEDECE ao que escrevemos** no volume, na rota por rádio e no
  pré-amp. Os dez testes que rodam verdes nessas células **são todos de unidade**
  — aferem o nosso byte, nenhum toca controle.
- **A diferença entre "o firmware está calado" e "o valor não mudou o bastante".**
  Zero eventos de evdev em 10 s com os controles parados **e** o vetor da
  gravidade correto e congelado são compatíveis com as **duas** hipóteses, porque
  o nó de sensores tem `fuzz=16`. **O evdev é a régua errada para esta pergunta**
  — só a contagem no hidraw desempata (entrega 2.3).
- **A cor de cada controle dela.** Ela tem quatro registrados e só dois estavam
  ligados, ambos por rádio. **Não sei qual endereço é o vermelho e qual é o
  azul**, e sem esse rótulo o censo não decide nada.
  **Em 15/08 os quatro estavam ligados e foram lidos**, mas o mapeamento
  endereço-cor daquele dia é **INFERÊNCIA pela ordem de pareamento**, não
  rótulo dela. Continua sendo dela a palavra.
- ~~**O USB como via de identidade.**~~ **RESPONDIDO EM 15/08/2026, e a resposta
  é "não serve":** o `iSerialNumber` do descritor USB **não é o serial do
  produto** — é o MAC em 12 dígitos hexadecimais (`SDL_hidapi_ps5.c:391-403`).
  A via independente que sobrou é o serial de fábrica por `0x80`/`0x81`, que é
  outra coisa e está na D-15.
- **A cor renderizada sob o tema de alto contraste do sistema.** Li a regra; não
  provei quem vence.
- **A latência de ponta a ponta "apertar X, a tela reagir".** Medi só o
  transporte (0,4 ms de IPC), não o caminho completo.
- **Se `next_page()` pula páginas escondidas.** Importa porque a aba "No jogo"
  some e volta em runtime: se não pular, R1 leva a uma página invisível e a
  interface trava sem explicação.
- ~~**Se a Sony grava a cor em algum lugar do aparelho.**~~ **RESPONDIDO EM
  15/08/2026: grava, sim** — no serial de fábrica de 17 caracteres, caracteres 5
  e 6, alcançável por `SET_FEATURE 0x80` + `GET_FEATURE 0x81`. Três fontes
  independentes concordam. **Continua NÃO MEDIDO por nós**, porque exige uma
  escrita da família de fábrica que só ela autoriza — ver a D-15.
  *(A redação antiga — "não achei fonte pública que afirme nem que negue" — já
  estava desatualizada quando foi escrita: o achado é de 10/08/2026 e ficou
  enterrado num transcrito de subagente. É o custo de achado que não vira
  página.)*

### O que precisa de equipamento que não há aqui, e o substituto de cada um

| falta | substituto |
|---|---|
| **Analisador de Bluetooth** | **não é necessário, e o substituto é melhor:** o firmware de dongle publicado sob licença MIT **é** um analisador congelado — alguém já fez a captura e publicou o resultado em C. Foi de lá que a metade de **entrada** saiu byte a byte e funcionou de primeira |
| **Um PS5, para conferir "o Sackboy usa três saídas"** | **não há substituto para ver o console fazendo.** Mas a pergunta que importa não é *"o PS5 faz?"* — ela já respondeu isso, e **a observação dela é fonte primária nesta casa**. A pergunta é *"por qual report?"*, e essa **o descritor do aparelho responde sozinho**: o degrau `0x39` existe no controle **dela**, não no console |
| **Osciloscópio, para separar som de vibração no canal 3** | **a mão e a orelha dela** (2.1). Nesta casa a observação dela já corrigiu três leituras minhas de código num dia só |
| **Segundo host, para isolar "é o daemon ou é o firmware"** | **parar o daemon** (2.2). Custa dez minutos e é o A/B que faltava desde 25/07 |
| **Um DualSense Edge** | **não tem substituto.** A resposta honesta é *"não sabemos"*, e o mapa **não deve afirmar paridade Edge x padrão nesta família**. Lacuna, não igualdade presumida |

---

## 11. O ENSAIO 2+2 — dois no cabo e dois no rádio, no mesmo minuto

**Acrescentado em 15/08/2026. É desenho dela**, decidido depois de ver o censo
dos dezessete: em vez de medir a mesa toda por rádio hoje e a mesa toda por cabo
outro dia, **medir os dois transportes ao mesmo tempo, com os mesmos quatro
aparelhos, o mesmo instrumento e o mesmo relógio**.

### 11.1 O que este desenho decide que a mesa toda-rádio NÃO decide

A mesa de hoje mediu quatro unidades **e um transporte só**. Toda diferença que
ela encontrar entre "o que se mediu hoje" e "o que se mediu em outro dia por
cabo" tem **pelo menos quatro explicações concorrentes**, e nenhuma medição
sequencial consegue separá-las:

| explicação concorrente | por que a medição sequencial não a descarta |
|---|---|
| **o transporte** | é a hipótese que interessa, e é a única que o desenho 2+2 isola |
| **o momento** | firmware, versão do daemon, carga do BlueZ e do host mudam entre um dia e outro. O daemon vivo desta casa é **mais velho que o código** — cura só vale no próximo start |
| **a unidade** | os quatro **não são iguais**: três BDM-050 e um BDM-060M, com quatro `hardware_version` diferentes e duas `sw_series` diferentes |
| **o instrumento** | *"medir contra a biblioteca errada produz alarme convincente e falso"* — o instrumento de terça pode não ser o de quinta |

**O 2+2 mata as três últimas de uma vez:** mesmo minuto (mata o momento), mesmo
processo de medição (mata o instrumento), e **dois aparelhos por braço** (dá
réplica interna — uma diferença que aparece em **um** dos dois é efeito de
unidade, não de transporte).

**E o passo que fecha o desenho é a TROCA.** Rodar duas vezes, invertendo os
braços: os dois que estavam no cabo vão para o rádio e vice-versa. Sem a troca,
*"o transporte"* continua confundido com *"quais duas unidades foram para qual
braço"* — que é exatamente o erro que o `hardware_version` deste censo deixou
óbvio. **Com a troca, o efeito de unidade vira número em vez de dúvida.**

**O que se segura fixo nas duas rodadas:** o host, o kernel, a versão do daemon
(e ele **iniciado depois** da última edição de código), o instrumento com a
biblioteca declarada no cabeçalho, e a bateria dos quatro acima do mesmo piso —
controle em bateria baixa muda comportamento de rádio e não avisa.

### 11.2 As quatro perguntas que este desenho responde, em ordem de valor

**1. A cor, `0x80`/`0x81` lado a lado nos dois caminhos.** É a pergunta da
**D-15**, e o 2+2 é a única forma de respondê-la sem ambiguidade. O
`dualshock-tools` **recusa Bluetooth de saída**, e daí veio a leitura de que o
caminho *"só funciona por cabo"* — mas **recusar não é medir**, e ninguém
publicou a tentativa por rádio. Com dois no cabo e dois no rádio, o mesmo
`SET_FEATURE 0x80 [0x01, 0x13]` seguido de `GET_FEATURE 0x81` sai nos dois
braços no mesmo minuto, e há três resultados possíveis — **os três úteis**:

- **funciona nos dois** -> a leitura de cor não precisa de cabo, e a alínea (c)
  da D-15 deixa de ser território não demonstrado;
- **só no cabo** -> a casa passa a poder escrever *"medido: o serial de fábrica
  não atravessa o rádio"*, com data e amostra, em vez de repetir a leitura de
  terceiro;
- **falha nos dois** -> o problema não é o transporte, é o comando ou o firmware
  destas unidades — e isso só se sabe **porque o braço do cabo estava lá**.

**Depende da D-15**, porque envolve escrita da família de fábrica. **Sem a
palavra dela, este item não roda** — os outros três rodam.

**2. O áudio, que é a assimetria mais grosseira dos dois transportes.** O cabo
expõe uma **placa de som USB de 4 canais** associada ao controle; o rádio **não
expõe placa nenhuma**. Hoje isso é afirmado por literatura e por aritmética do
descritor, e a seção 10 registra por escrito que *"a medição de card com 4
canais que outro agente citou hoje é de outro momento, com outra numeração de
placa"* — **o `card1` de agora é a webcam**. Com dois controles no cabo, a
numeração de placa é conferida **no mesmo instante** em que o braço do rádio
mostra a ausência dela, e a assimetria deixa de depender de memória de
numeração. É o que separa *"o rádio não tem alto-falante"* de *"o rádio não tem
**placa de som**, e o alto-falante, se existir, chega por outro degrau"* — que
é a pergunta do canal 3 e do `0x39`.

> **ESTE ITEM JÁ RENDEU, na primeira noite em que a mesa 2+2 existiu.** Com os
> quatro na mesa, os descritores foram lidos lado a lado no mesmo minuto: **cabo
> 289 bytes com UM output (`0x02`, 47 B); rádio 320 bytes com NOVE, em escada de
> +64 B, mais um FEATURE `0xF6` de 546 B que o cabo não tem.** E, no mesmo
> ensaio, o firmware **executou** o `0x32` e o `0x39` por rádio. **A assimetria
> deixou de ser leitura de código e virou medição de transporte** — e é
> literalmente o que este desenho dela existia para produzir. O que ele **não**
> produziu: qualquer conhecimento sobre o **conteúdo** do payload.

**3. A taxa do giroscópio e do acelerômetro, por transporte.** Já está medido
que o cabo entrega **250,0 Hz exatos** e que o rádio entrega **em rajadas**, com
taxa variável. O que **não** está medido é se isso vale para as quatro unidades
ou se foi a unidade que estava no cabo naquele dia — e o driver desta máquina
**não pede taxa nenhuma** ao DualSense, nem por cabo nem por rádio, então quem
decide é o par aparelho + transporte. Com 2+2 e a troca, sai a tabela quatro por
dois inteira, e ela responde de uma vez se a rajada do rádio é do transporte
(esperado) ou se tem componente de unidade (que ninguém procurou). **Régua:
`MSC_TIMESTAMP` do nó `Motion Sensors` — o relógio do controle — e a contagem de
`SYN_REPORT` sobre tempo de parede, as duas juntas**, como em 11/08.

**4. O custo e o comportamento da leitura de feature, medido nos dois braços.**
O censo de hoje pagou 3,2-3,7 s por falha no braço do rádio, e um aparelho só
respondeu na quinta tentativa. **Não se sabe qual é esse custo no cabo** — a
suspeita óbvia é "nenhum", e suspeita óbvia é exatamente o que esta casa exige
medir. Sai daqui o número que sustenta o `feature_retries` do DKMS, e sai a
resposta para *"a resposta trocada (`0x80` no lugar de `0x20`) é do rádio ou é
do aparelho?"* — se acontecer também no cabo, a validação de `buf[0]` vira regra
de leitura em qualquer transporte, e não macete de Bluetooth.

### 11.3 As armadilhas específicas deste ensaio

1. **Plugar o cabo pode não trocar o transporte.** Um DualSense pareado por
   Bluetooth que recebe o cabo pode continuar falando por rádio e só carregar.
   **O braço de cada aparelho se confere no `uevent`/`hidraw`, nunca na
   suposição de que "está plugado, logo é USB"** — e é uma conferência que entra
   no relatório, não no comentário.
2. **Quatro controles em dois transportes é o cenário em que o co-op mais
   embaralha.** Os evdev físicos ficam **mudos** para leitor externo, porque o
   co-op faz `EVIOCGRAB` neles — medido em 15/08, em dois ensaios, e é
   comportamento **correto**. Instrumento ingênuo mede zero evento e conclui que
   o aparelho está calado. **Meça no `hidraw`, ou meça no vpad sabendo que é o
   vpad.**
3. **O `state_full` não diz qual vpad é qual MAC** (seção 12). Enquanto essa
   dívida existir, a correspondência vpad-aparelho neste ensaio se estabelece
   **apertando botão**, um de cada vez, e se escreve no relatório como o que é:
   um passo manual.
4. **Escrita exige daemon parado ou o broker.** Vale para o item 1. Leitura
   convive com o daemon; escrita, não.

---

## 12. Dívidas registradas nesta leva, e NÃO consertadas

**Registro, não conserto.** Cada uma tem dono fora desta página, e mexer aqui
atropelaria trabalho alheio. A regra da casa é que **dívida sem endereço vira
retrabalho**, então elas ficam escritas.

### 12.1 O `uhid_blueprint.py` fossiliza `hw_version = 0x0710` em TODO vpad

`src/hefesto_dualsense4unix/integrations/uhid_blueprint.py` forja todo gamepad
virtual com `hw_version = 0x0710`. **Medido em 15/08/2026:** esse é o
`hardware_version` do DualSense **roxo** dela — os quatro vpads afirmam ao
kernel serem a mesma placa daquela unidade.

- **Não é defeito hoje.** Nada no produto lê esse campo do vpad, e nenhum jogo
  observado o consulta.
- **É impressão digital duplicada**, e o custo aparece no dia em que alguém usar
  `hardware_version` como chave de diagnóstico — que é exatamente o uso que o
  censo de hoje recomenda para os aparelhos **físicos**. Quatro vpads com o
  mesmo valor, e um deles igual ao de um físico da mesa, é a receita de uma
  medição que se acredita e está errada.
- **Não consertar por aqui:** `src/` é de outro agente nesta leva.

### 12.2 O `state_full` não publica qual vpad corresponde a qual MAC

**Medido em 15/08/2026.** O campo `coop.players` é um **número** (`4`), não uma
lista. Não há, no estado publicado, nada que ligue *"vpad Hefesto P2"* a um
endereço.

**A consequência é de método, e foi paga hoje:** a pergunta *"o vpad e o físico
correspondem?"* **não pôde ser respondida por leitura** — foi respondida
apertando o botão X em cada controle e vendo qual `/dev/input/event*` emitia
(`EV_KEY`, code 304, value 1). A correspondência estava **certa** nos quatro,
com o branco confirmado isoladamente em quatro eventos.

Enquanto o `state_full` não publicar a lista, **todo ensaio com mais de um
controle paga esse passo manual de novo** — inclusive o ENSAIO 2+2 da seção 11.
Dono: `src/`, outro agente.

### 12.3 O achado de 10/08 que ficou num transcrito de subagente

O caminho da cor (`0x80`/`0x81`, serial nos caracteres 5 e 6) **foi achado nesta
casa em 10/08/2026** e não virou página. Ficou no transcrito de um subagente, a
sprint `UNIDADE-COR-01` abriu e não começou, e **a D-15 deste índice foi escrita
em 14/08 afirmando o contrário** — *"a leitura a partir do aparelho nunca foi
tentada, e eu não achei campo HID que a reporte"*.

**Cinco dias de distância entre saber e a página dizer que não se sabia.** É a
mesma classe de defeito que a casa já nomeou: *"a casa sabe e o produto não
faz"*. Aqui foi *"a casa sabe e a página nega"*, que é pior, porque uma decisão
dela quase foi tomada em cima da negação.

**A dívida não é o achado — é o caminho do achado até a página.** Fica
registrada aqui sem conserto proposto, porque a cura é de processo e é dela.
