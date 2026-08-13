# Como olhar a tela deste projeto

**Leia isto antes de tentar fotografar, medir ou entender a interface.**

Pedido dela, literal, em 01/08/2026:

> *"se tiver outro conhecimento desatualizado no repositório, ou que você usou
> e não funcionou e você descobriu a forma certa, isso deve ser materializado
> como conhecimento perpétuo pra evitar perdermos tempo reaprendendo sempre sem
> necessidade."*

Este arquivo é isso. Cada linha aqui custou tempo de alguém.

---

## A regra, em uma linha

```bash
scripts/gui-captura/retratar_abas.py
```

Uma execução. Nenhum clique, nenhuma janela aberta, nenhuma tela em foco. Sai
um PNG por aba, no tamanho da tela dela maximizada (1920x1080), **com o card do
controle vivo dentro**.

**Sem argumento, ele SOBRESCREVE as imagens da documentação**
(`docs/usage/assets/readme_*.png`) — que são as mesmas do `README.md` e do
`docs/usage/interface.md`. É o comportamento pedido: rodar e a documentação
deixa de mentir.

Com um caminho como argumento, ele só olha:

```bash
scripts/gui-captura/retratar_abas.py /tmp/olhar
```

## O logo e os ícones

Mesma ideia, outro comando:

```bash
scripts/gerar_icones.sh            # gera todos os PNGs a partir do SVG
scripts/gerar_icones.sh --check    # só confere (é o que o teste roda)
```

**A fonte canônica é uma só: `assets/hefesto-logo.svg`.** Mexeu no desenho?
Rode o gerador. Os PNGs do applet COSMIC e do AppImage nascem dele, e
`tests/unit/test_icones_refletem_o_svg.py` reprova se alguém mudar o SVG sem
regerar.

**O que isso curou** (medido em 01/08): havia **dois** caminhos de ícone e o
documentado era o quebrado. O `install.sh` copiava
`assets/appimage/Hefesto-Dualsense4Unix.png`, que **não existia** — o `cp`
falhava em silêncio — e o ícone que aparecia no sistema vinha, por acidente, do
PNG do applet, versionado à mão. E o comentário do instalador afirmava que o
SVG era um placeholder, o que **deixou de ser verdade** em algum momento sem
ninguém atualizar o texto.

## Quando rodar

| momento | por quê |
|---|---|
| **ao começar a trabalhar na interface** | você vê a tela de hoje, não a de seis dias atrás |
| **antes de commitar** mudança visual | a foto do commit é a foto do que ele fez |
| **antes de gerar release** | as imagens do README acompanham a versão |

Em 01/08 as imagens da documentação eram de **26/07** — seis dias e cinco levas
atrás. E `readme_status.png` e `readme_sistema.png` **eram referenciadas e não
existiam**. Rodar o script curou os dois problemas de uma vez.

## Para quem trabalha com o Claude Code

Esta é a parte que ela levantou e que muda o dia a dia:

> *"o melhor, ele funcionaria principalmente pro Claude, pq ficaria muito mais
> fácil pro Claude entender toda a tela, sem todas as vezes o Claude tomar
> sufoco nisso"*

**Está certa, e o sufoco é real e documentado.** Um assistente que precise
entender a interface deve rodar este script e **ler os PNGs** — a ferramenta de
leitura de arquivos enxerga imagens. É mais rápido, mais fiel e infinitamente
menos frágil que as alternativas, que já falharam assim:

- **clicar por coordenada** para focar a janela: aconteceu duas vezes, e nas
  duas o clique caiu noutro aplicativo e o trouxe para a frente. Pior: um
  clique cego já desfez configuração dela sem ninguém notar;
- **percorrer abas por teclado**: o compositor perde eventos em rajada, e a
  sequência inteira sai deslocada em uma aba — a foto chamada "gatilhos"
  mostrando "status". Aconteceu duas vezes antes de existir laço de
  verificação;
- **pedir para ela tirar o print**: funciona, mas custa o tempo dela para
  responder o que uma foto automática responde.

---

## Os cinco scripts desta pasta, e qual usar

| script | o que faz | quando |
|---|---|---|
| **`retratar_abas.py`** | monta o glade **+ injeta o card do controle**, offscreen | **rotina, sempre** |
| **`retratar_dialogos.py`** | fotografa os **diálogos** de confirmação, offscreen | quando a mudança está num diálogo — o `retratar_abas.py` não os alcança |
| `retrato_offscreen.py` | monta só o glade cru | medir vão/altura, quando o card não importa |
| `capturar_verificado.sh` | fotografa a tela **de verdade**, percorrendo por teclado | prova final, com a janela aberta e em foco |
| `aba_ativa.sh` | diz **qual aba está ativa** num PNG, medindo o sublinhado rosa | é o sensor do `capturar_verificado.sh`; sozinho, só para conferir uma foto |

Esta tabela tem portão: `tests/unit/test_a_tabela_dos_scripts_de_tela.py` cruza
as linhas acima com o `ls` da pasta e reprova quando divergirem. Ela já
envelheceu calada uma vez — dizia "os três scripts" com cinco no disco, e o que
faltava era justamente o `retratar_dialogos.py`, cujas imagens o
[`interface.md`](../usage/interface.md) publica.

### Por que o `retrato_offscreen.py` não basta

Ele renderiza o `.glade` **cru**: combos vazios, listas vazias e — o mais grave
— **a aba Status sem o card do controle**, que é montado em código, não no
glade. É justamente a aba mais densa da janela.

Já houve leva fotografada por ele em que o objeto que a leva mudava **não
aparecia na foto**. Ele continua útil para medir geometria de página (é o que
imprime `recebe / natural / vão`), mas não serve para entender a tela.

### Por que o `capturar_verificado.sh` não é rotina

Precisa da janela **aberta, maximizada e em foco**. E o COSMIC recusou
maximizar por atalho, por duplo clique e por F11 nesta máquina. Ele é a prova
final quando o assunto é *"ficou bonito?"* — e para isso não há substituto.

---

## O que a foto offscreen NÃO prova

Seja honesto sobre isto ao usá-la:

- **não passa pelo compositor** — não há sombra, canto arredondado nem o tema de
  janela do COSMIC;
- **não prova que a janela abre** — prova o que tem dentro dela;
- **não substitui o olho dela.** A regra da casa
  ([PROVA-DE-TELA-01](sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md))
  continua valendo: interface só fecha com ela olhando.

Para *"o que tem nesta aba, e onde?"*, a foto é fiel. É para isso que serve.

---

## Armadilhas de GTK que este projeto já pagou

Estas não são sobre foto — são sobre **medir** a interface, e cada uma custou
horas.

### Sob Xvfb não há gerenciador de janelas

Uma `Gtk.Window` de verdade **nunca é mapeada**, e o filho fica **1x1 para
sempre**, por mais que o laço de eventos rode. O `get_surface()` que destrava
uma `OffscreenWindow` não existe ali.

**Consequência:** todo teste de layout deve usar `Gtk.OffscreenWindow`, ou dar
o tamanho à janela por conta própria. Isso reprovou o CI de uma tag inteira.

### Widget sem alocação mede 1x1 — e o teste passa com qualquer desenho

Medir antes de o laço assentar dá 1x1, e uma asserção sobre 1x1 passa com
qualquer coisa. **Drene o laço mais de uma vez** antes de medir.

### `set_size_request` é MÍNIMO, nunca máximo

No GTK3 não existe "largura máxima" por pedido. Um `width-request` sozinho não
segura nada — ele precisa de `halign=start` para virar teto de fato. E com
`halign=center` ele **trava** o widget no número exato.

### `max-width-chars` sozinho não encolhe label nenhum

Ele limita a largura **natural** (o que o widget *pede*); o pai continua livre
para alocar mais, e um label esticado quebra na largura que **recebeu**. Precisa
de `halign=start` junto. Medido em 01/08: sem isso, um parágrafo de 1869px ficou
intacto.

### Uma célula de `GtkGrid` nunca é mais larga que suas colunas

Pedir largura inteira de dentro de uma grade faz **todas** as colunas
expandirem junto. Quem precisa da largura toda sai da grade, para uma caixa
própria.

### `GtkProgressBar` desenha o próprio texto CENTRADO

Numa barra larga, o número fica a centenas de pixels de cada borda. Se a barra
precisa ser larga, o texto sai dela e vira um rótulo ao lado.

### `column_homogeneous` dá metades IGUAIS

Se as duas metades reais do desenho não forem iguais, as divisórias não batem.
Para amarrar larguras entre linhas diferentes, o instrumento é `Gtk.SizeGroup`.

### O quadrado vermelho ao lado dos interruptores

Todo `GtkSwitch` do GTK3 tem dois nós `image` internos que pedem ícones que
**nenhum tema desta máquina resolve** — e o GTK pinta o "imagem faltando" do
tema ativo. `color: transparent`, `-gtk-icon-source: none` e `opacity: 0`
**não** funcionam (o fallback é ícone colorido, não simbólico). O que cura:
`-gtk-icon-transform: scale(0)`.

---

## Armadilhas de medição fora do GTK

### Medir contra a biblioteca errada produz alarme convincente e falso

Em 01/08 mediu-se o gamepad virtual contra a `libSDL2` **do Ubuntu** e
concluiu-se que ele não entregava quase nada ao jogo. A **SDL3 que a Steam
distribui** o enumera por completo. Nenhum jogo da Steam carrega a do sistema.

**Regra:** todo instrumento tem de declarar **qual biblioteca** está usando —
caminho absoluto e versão — no cabeçalho da saída.

### Struct incompleta em `ctypes` corrompe o resultado SEM erro

Faltavam três campos numa `SDL_hid_device_info`; o ponteiro de lista deslocou e
a enumeração saiu errada **em silêncio**, com aparência legítima. Confira campo
a campo contra o header da versão certa.

### O instrumento pode estar brigando com o produto

`hefesto-dualsense4unix test trigger --raw` abre um **segundo** controlador e
disputa o hidraw com o daemon, que sobrescreve em ≤ 0,5 s — **e imprime
"trigger aplicado" mesmo assim**. Testes de gatilho vão pela GUI/IPC, ou com o
daemon parado.

### Nome de recurso do kernel é POSIÇÃO, nunca semântica de produto

Registrado em **07/08/2026**, do commit `cf176d6`. **GRAU: MEDIDO.**

Em 06/08 às 22h40 a medição dos player-LEDs foi lida assim: cada nó aceso em
`/sys/class/leds/*:player-N` foi tomado como *"este aparelho é o jogador N"*.
É falso para o DualSense. O número do jogador é o **padrão das cinco lâmpadas**
(`core/led_control.py`, a tabela `_PLAYER_LED_PATTERNS`): jogador 1 é **só a do
meio**, que o kernel chama de `player-3`; jogador 3 são as duas pontas mais o
meio.

O que a leitura errada produziu foi um achado inteiro que **nunca existiu**
(*"DOIS aparelhos no MESMO jogador 3"*), commitado em dois lugares e citado em
duas mensagens de commit. Não houve colisão naquela mesa: o vpad acendia o
padrão do 1 e o DualSense físico o do 3.

**Quem leu certo foi ela, de olho, sem instrumento** — *"o dualsense branco
dessa vez conectado como player 3"*. A pessoa que USA o produto leu o plástico
melhor do que quem o escreve leu o `sysfs`.

**A regra, e ela é da mesma família do "medir contra a biblioteca errada":**
nome de recurso do kernel descreve **onde a lâmpada fica**, não o que ela
significa no produto. Antes de usar um nome de `sysfs` como valor de domínio,
confira contra a tabela do produto que traduz um no outro — aqui,
`core/led_control.py`. Se não existir essa tabela, o nome não é dado: é
coincidência.

**O que salvou a casa foi um teste que já sabia disso:**
`tests/unit/test_lugar_a_mesa_numero_de_jogador_nao_se_repete.py` compara o
**padrão**, nunca o nome do nó — era o único artefato da leva com a distinção
escrita, e por isso não herdou o erro.

### Instrumento que consulta o `journal` declara o locale, ou mente calado

Registrado em **07/08/2026**, do commit `6e04c57`. **GRAU: MEDIDO.**

Um medidor formatava a janela de tempo com a data **em português** e a passava
para o `journalctl --since`. O `journalctl` não entende `ago`, `set`, `dez` — e
não reclama: ele devolve **zero linha**, que é indistinguível de "não houve
nenhum evento". Foi daí que saiu a afirmação falsa dita **a ela, ao vivo**, de
que *"três controles custam 40 perdas por minuto e dois custam zero"*.

Refeita a medição com instrumento validado, o número **inverte a conclusão**:
quatro controles estáveis custam **14,6** perdas de IMU por minuto, e **três**
controles com o 8BitDo tentando voltar custam **48,4**. Não é a quantidade de
controles; é o que não consegue entrar. A retratação está na
[CONECTA-E-DESLIGA-01](sprints/2026-08-07-CONECTA-E-DESLIGA-01-a-regressao-que-ela-relatou-e-a-suspeita-que-recai-sobre-nos.md).

**A regra tem duas metades, e a segunda é a que faltava:**

1. **declare o locale.** `LC_ALL=C` no instrumento, ou monte a data com
   `strftime("%Y-%m-%d %H:%M:%S")` — nunca com nome de mês;
2. **prove a janela contra contagem direta antes de acreditar nela.** Foi assim
   que o medidor das 20h13 se validou: a contagem do instrumento bateu com a
   contagem à mão do mesmo intervalo, **53 = 53**. Sem essa conferência, um
   instrumento quebrado e uma janela limpa dão a mesma saída.

Vale a mesma advertência de data completa da armadilha seguinte: `--since
"21:34:39"` **sem data** também devolve zero em qualquer janela.

Esta foi a **segunda** vez no mesmo dia em que o instrumento enganou quem media.
A primeira é a armadilha logo acima, do nome de `sysfs`.

### O medidor pode estar INERTE — e inerte é indistinguível de "não houve nada"

Esta é a irmã da anterior, e é pior, porque a anterior mente e esta **cala**.

**O install deste projeto é *editable*** (o `.pth` da venv aponta para o `src/`
do repositório). Consequência que vale para **todo** código de daemon, sem
exceção: **o que você escreveu hoje só entra em vigor no PRÓXIMO start do
processo**. Um daemon vivo mais velho que a sua cura não a executa, não falha e
não avisa — ele simplesmente não a tem dentro dele.

Quando a cura é um **medidor**, o resultado é o pior que existe: a medição
devolve **zero**, e zero é exatamente o que uma medição bem-sucedida devolveria
se o defeito não tivesse acontecido. **Silêncio de instrumento morto é
indistinguível de ausência de defeito.**

A casa já pagou por isso **duas vezes**, com custo medido:

- **05-06/08/2026** — o daemon vivo era o PID 1670, de 04/08 23:39:46; as curas
  de perfil eram de 05/08 00:38:41. Ela trocava de perfil e a cor/gatilho/rumble
  não entravam. **Era o defeito já curado no disco**, e ela estava olhando para o
  produto de anteontem
  ([PERFIL-REESCRITO-NA-PARTIDA-01](sprints/2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md),
  linhas 43-47);
- **07/08/2026** — o diário da bateria (474 linhas, 49 testes verdes) ficou
  **5h49m** no disco sem escrever **uma linha** no journal, com o controle dela
  conectado o tempo todo. Uma noite de medição teria produzido nada, em silêncio.
  Reiniciado o serviço às 21:34:39 (autorização dela), a primeira amostra saiu
  35 segundos depois.

**A regra: antes de acreditar em qualquer medição feita pelo daemon, confira o
relógio do processo.** Os dois comandos, e o zero que condena:

```bash
systemctl --user show hefesto-dualsense4unix.service \
  -p ExecMainStartTimestamp --value            # desde quando o processo existe

journalctl --user -u hefesto-dualsense4unix.service \
  --since "AAAA-MM-DD HH:MM:SS" --no-pager \
  | grep -c <evento_que_a_sua_cura_emite>      # 0 = instrumento morto
```

A janela do `journalctl` tem de **começar depois** do start, e **sempre com data
completa** — `--since "21:34:39"` sem data devolve zero em qualquer janela, e
aqui o comando quebrado imita exatamente o defeito que ele deveria detectar.

E **reiniciar é decisão dela**, nunca sua: o restart derruba os handles de uma
partida em curso.

O caso inteiro, com a mordida (0 antes, 2 depois, mesmo código no disco) e o
desenho de um aviso no `doctor` que mediria isso sozinho, está em
[PROTOCOLO — o controle que cai sozinho](estudos/2026-08-07-PROTOCOLO-o-controle-que-cai-sozinho.md),
seções 8.1 e 9.

### `paplay --device=inexistente` sai ZERO e toca no padrão

Nunca aceite código de saída como prova de que o som saiu no dispositivo certo.

---

## Ferramentas de sistema, e o que não fazer com elas

- **`ydotool` exige `ydotoold` vivo** e só faz `mousemove` **relativo**. Clique
  por coordenada absoluta não existe — e clique cego já desfez configuração
  dela;
- **`wtype` cria e destrói um teclado virtual a cada chamada**; em rajada o
  compositor perde eventos;
- **o helper global de captura de tela dela** (fora deste repositório, em
  `/usr/local/bin`) fotografa a tela inteira e imprime o caminho do PNG. Serve
  para ver o que está na frente dela agora — não para percorrer abas.
