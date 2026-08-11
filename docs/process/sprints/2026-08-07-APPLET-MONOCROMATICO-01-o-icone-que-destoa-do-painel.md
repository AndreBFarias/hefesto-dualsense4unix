# APPLET-MONOCROMÁTICO-01 — o ícone que destoa do painel

- **Achado em:** 07/08/2026, por **ela**, olhando a própria barra. Não veio de
  auditoria, não veio de teste vermelho: veio do olho dela na tela que usa todo
  dia
- **Estado:** **EXECUTADA em 07/08/2026, MENOS a palavra final dela.** O texto
  abaixo foi escrito antes da execução e **não foi reescrito** — é o roteiro
  como estava. O que a execução mediu, contrariou e entregou está na seção
  [O que a execução de 07/08 mediu e entregou](#o-que-a-execução-de-0708-mediu-e-entregou),
  no fim. Quando este documento e aquela seção discordarem, **a seção vale**:
  ela tem os comandos e os números de depois
  - **A E0.1 foi respondida por ela na mesma tarde**, e o símbolo foi
    redesenhado: ver
    [O redesenho de 07/08 à tarde](#o-redesenho-de-0708-à-tarde--a-decisão-14-executada),
    a última seção, que é a mais nova de todas e vale sobre as anteriores
  - *(estado original, preservado: "SPRINT DE FUTURO — ABERTA. Em 07/08
    nenhuma linha de código, ícone, instalador ou configuração foi tocada.
    Este documento é medição e roteiro. Quem executar não terá tido esta
    conversa, e é para essa pessoa que ele está escrito")*
- **Gravidade:** **BAIXA** no funcionamento — nada quebra, nada deixa de
  responder. **ALTA** na coerência do que ela vê: entre os sete ícones da asa
  direita do painel dela, o do Hefesto é **o único cromático**, e isso está
  medido em número, não em impressão
- **Causa-raiz:** **MEDIDA**, e **não é a que o pedido sugere**. O ícone não é
  "colorido por escolha de desenho": o **formato** em que ele é servido hoje
  torna a recoloração pelo tema **impossível**. Está em destaque na seção
  *"A causa-raiz"*
- **Segunda armadilha, também MEDIDA:** o ícone que ela fotografou **não é o
  applet nativo**. Mexer só no fonte do applet COSMIC não muda nada no que ela
  vê hoje. Está em destaque na seção *"A primeira armadilha"*
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
  — é o índice aberto mais recente; esta sprint nasce depois dele e não estava
  na lista de lá
- **Parentes, e distintas:**
  - [RADAR-01](2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md)
    — é a sprint que **descobriu** que o painel é uma superfície de interface
    que ninguém tinha olhado. Esta é sobre **como o ícone dessa superfície é
    desenhado**. Atenção: a medição de 31/07 daquela sprint **caducou**, e a
    nota datada está na seção *"O que não se apaga"*;
  - [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
    — é o regime de validação desta sprint inteira. Isto é interface: fecha com
    o olho dela, foto antes e depois, e a palavra final é dela;
  - [DOC-QUE-NÃO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md)
    — a seção E2-bis registra o **ÍCONE-VIVO-01**, o portão que trava os PNGs
    contra `assets/hefesto-logo.svg`. Esse portão vai **reprovar** metade das
    entregas ingênuas desta sprint, e a seção *"Os portões"* explica como não
    brigar com ele;
  - [NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md)
    — mesma família de defeito noutra camada: a tela afirmando uma coisa que o
    sistema por baixo já sabe ser outra.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há comando
reproduzível, pixel contado, arquivo lido ou teste que reprova com a cura
arrancada; **SUSPEITA COM MECANISMO** = o caminho foi lido inteiro e fecha, o
efeito não foi observado; **SEM PROVA** = está dito e ninguém verificou.

**Aviso de execução, e ele não é formalidade.** As medições deste documento
foram feitas com a máquina dela **viva e em uso**: só leitura de `/etc`, `/sys`,
D-Bus e arquivos de configuração. Nada foi reiniciado, nenhum controle foi
tocado. Quem executar as entregas **vai** precisar reiniciar a barra dela
(`packaging/cosmic-applet/justfile` termina em `killall cosmic-panel`) — isso
faz o painel dela sumir e voltar. **Combine antes.**

---

## O pedido, na língua dela

07/08/2026, literal:

> *"o applet do hefesto deve ficar em preto e branco, talvez só o círculo com
> borda preta e a borda do martelo ao centro. no cosmic todos os applet são
> assim"*

Três coisas estão ditas aí, e as três são critério de aceite:

1. **"em preto e branco"** — sem cor. É o pedido principal;
2. **"só o círculo com borda preta e a borda do martelo ao centro"** — uma
   proposta de desenho, oferecida com um **"talvez"**. É sugestão dela, não
   ordem, e colide com uma decisão medida anterior (ver *"O que não se
   apaga"*). **Quem executar tem de levar a colisão de volta para ela.**
3. **"no cosmic todos os applet são assim"** — a justificativa. E ela está
   **certa**: a regra existe, está escrita nos arquivos da máquina dela, e a
   medição está na seção *"A regra do COSMIC é real"*.

O critério dela, portanto, não é "fica bonito". É **"igual aos outros"**. Isso
é bom: dá para medir.

---

## O que a barra dela mostra hoje, em número

**Grau: MEDIDO.** Captura de tela de 07/08/2026 às 14h43, 1920x1080, recorte da
asa direita do painel. Saturação HSL medida ícone a ícone, caixa de 26x26 px:

| ícone (esquerda para direita) | x na foto | saturação máxima (de 255) | média |
|---|---|---|---|
| Spotify | 1622 | 30,0 | 15,7 |
| **Hefesto** | **1663** | **255** | **37,2** |
| área de transferência | 1708 | 33,5 | 20,9 |
| Bluetooth | 1755 | 34,2 | 21,6 |
| som | 1794 | 37,2 | 25,3 |
| rede | 1838 | 36,4 | 22,6 |
| energia | 1880 | 37,2 | 26,5 |

Os 30 a 37 dos vizinhos **não são o desenho**: são o próprio azulado do fundo
do painel entrando no recorte. O desenho deles é acromático de verdade —
histograma do recorte do Bluetooth: `#F7F7F8`, `#BDBDC1`, `#A0A0A5`, todos com
R=G=B. O do Hefesto: `#634F6E` roxo, `#6B6490` roxo, `#8E6B93` roxo, `#DEA26E`
laranja, `#6A8EA9` azul, `#F2F1ED` branco.

**Ela é o único ícone cromático da barra.** É exatamente o que ela relatou, e
agora tem número.

**As imagens desta medição são efêmeras** (viveram no diretório temporário da
sessão de 07/08 e não estão versionadas — o repositório não guarda foto da área
de trabalho dela). Para refazer, sem clique nenhum, com a ferramenta de captura
da máquina dela descrita em
[COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md):

```
# recorte ampliado da asa direita, para olhar
convert <foto.png> -crop 320x36+1600+0 +repage -filter point -resize 400% zoom.png

# saturação de um ícone, para medir
convert <foto.png> -crop 26x26+1663+11 +repage -colorspace HSL \
    -channel G -separate +channel -format "%[fx:maxima*255] %[fx:mean*255]" info:
```

As coordenadas valem para o painel dela como estava em 07/08 (tamanho `S`,
âncora `Top`). Se ela mudar o tamanho do painel, recalcule — não confie no `x`.

---

## A primeira armadilha: o ícone que ela fotografou NÃO é o applet

**Grau: MEDIDO. Esta seção decide o escopo da sprint inteira.**

Existem **duas** superfícies do Hefesto que podem aparecer na barra do COSMIC, e
elas não são a mesma coisa:

| | quem desenha | de onde vem o nome do ícone | está no ar em 07/08? |
|---|---|---|---|
| **Bandeja (tray)** | a GUI GTK, via `StatusNotifierItem`, servido pelo `cosmic-applet-status-area` | `TRAY_ICON_NAME` em `src/hefesto_dualsense4unix/app/tray.py:44` | **SIM — é o que ela vê** |
| **Applet COSMIC nativo** | binário Rust próprio, `hefesto-dualsense4unix-applet` | `ICON_APP` em `packaging/cosmic-applet/src/app.rs:40` | **NÃO** — compilado, instalado, fora do painel |

A medição, com a sessão dela viva:

```
$ busctl --user call org.kde.StatusNotifierWatcher /StatusNotifierWatcher \
    org.freedesktop.DBus.Properties Get ss \
    org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems
v as 2 ":1.6184/org/ayatana/NotificationItem/spotify_client" \
       ":1.7791/org/ayatana/NotificationItem/hefesto_dualsense4unix"

$ ps -eo pid,comm,args | grep -i "hefesto\|cosmic-applet"
797776 cosmic-applet-s  cosmic-applet-status-area
792339 python3          python3 -m hefesto_dualsense4unix.app.main
  -> nenhum processo hefesto-dualsense4unix-applet

$ cat ~/.config/cosmic/com.system76.CosmicPanel.Panel/v1/plugins_wings
  -> "com.vitoriamaria.HefestoDualsense4Unix" não aparece em nenhuma das
     duas asas, nem no Dock

$ ls -la /usr/local/bin/hefesto-dualsense4unix-applet
-rwxr-xr-x 1 root root 23650568 ago  6 20:53   (instalado, só não adicionado à barra)
```

**A consequência prática, e ela é dura:** quem abrir
`packaging/cosmic-applet/src/app.rs`, trocar a constante do ícone, recompilar e
declarar a sprint entregue **não terá mudado nada no que ela vê**. O applet
nativo não está no painel dela.

Isso **não** significa que o applet deva ser ignorado. Significa que a sprint
tem **duas frentes**, e que a ordem importa: primeiro a bandeja (o que ela vê
hoje), depois o applet (o que ela pode voltar a pôr na barra amanhã). O desenho
é o mesmo para as duas; o encanamento não.

---

## A causa-raiz: o formato de hoje IMPEDE a recoloração

**Esta é a seção que explica por que o ícone é colorido, e por que "mudar o
desenho" sozinho não resolve.**

O ícone do Hefesto não é cromático por teimosia de desenho. Ele é cromático
porque **três coisas somadas** tiram dele qualquer chance de ser recolorido pelo
tema.

### 1. O nome pedido não tem o sufixo `-symbolic`

**Grau: MEDIDO.**

```
$ busctl --user get-property :1.7791 \
    /org/ayatana/NotificationItem/hefesto_dualsense4unix \
    org.kde.StatusNotifierItem IconName
s "hefesto-dualsense4unix"

$ busctl --user get-property :1.6184 \
    /org/ayatana/NotificationItem/spotify_client \
    org.kde.StatusNotifierItem IconName
s "com.spotify.Client-symbolic"        <- o vizinho PEDE simbólico; o Hefesto NÃO
```

O mesmo nome sem sufixo aparece em três lugares do nosso código:
`src/hefesto_dualsense4unix/app/tray.py:44` (`TRAY_ICON_NAME`),
`src/hefesto_dualsense4unix/app/main.py:187`
(`Gtk.Window.set_default_icon_name`) e `packaging/cosmic-applet/src/app.rs:40`
(`ICON_APP`).

### 2. Sob esse nome só existe PNG — e PNG nunca é recolorido

**Grau: MEDIDO** nos arquivos; **MEDIDO** no mecanismo, que foi lido no fonte.

```
$ find ~/.local/share/icons/hicolor -iname "*hefesto*"
  -> ONZE PNGs (16, 22, 24, 32, 48, 64, 96, 128, 192, 256, 512), ZERO SVG
$ ls ~/.local/share/icons/hicolor/scalable/apps/hefesto-dualsense4unix.svg
  -> não existe
```

E não é acidente: `install.sh:1959` **apaga** qualquer SVG que exista sob esse
nome (linha herdada da v3.4.2, que instalava um placeholder ali).

O mecanismo, lido no libcosmic — é um desvio de duas pernas, e a perna do PNG
não tem cor nenhuma:

```
src/widget/icon/mod.rs:106-110
    match self.handle.data {
        Data::Image(handle) => from_image(handle),   <- PNG: sem .class(), sem cor
        Data::Svg(handle)   => from_svg(handle),     <- SVG: com .class() e .symbolic()
    }
```

**Um PNG colorido é incurável por tema.** Nenhuma configuração de ícone,
nenhum tema escuro, nenhum ajuste de painel o deixa em preto e branco. É a
causa-raiz, e é por isso que a entrega **tem** de trocar o formato, não só o
desenho.

### 3. O tema ativo dela serve um SVG colorido, de fundo OPACO

**Grau: MEDIDO** nos arquivos; **SUSPEITA COM MECANISMO** na consequência.

```
$ cat ~/.config/cosmic/com.system76.CosmicTk/v1/icon_theme
"MeowSystem-Icons"

$ find ~/.local/share/icons/MeowSystem-Icons -iname "*hefesto*" -o -iname "*Hefesto*"
.../MeowSystem-Icons/scalable/apps/hefesto-dualsense4unix.svg
.../MeowSystem-Icons/scalable/apps/com.vitoriamaria.HefestoDualsense4Unix.svg
   (ambos de 04/08 23:09, 2612 bytes, iguais entre si)

$ diff assets/hefesto-logo.svg \
       ~/.local/share/icons/MeowSystem-Icons/scalable/apps/hefesto-dualsense4unix.svg \
  && echo IDENTICOS
IDENTICOS
```

Ou seja: **o tema de ícones dela carrega uma cópia byte a byte da nossa logo
canônica**, sob o mesmo nome que o código pede. E o tema ativo é procurado
**antes** dos herdados (`cosmic-freedesktop-icons`, `src/lib.rs:305-322`), e
dentro de `MeowSystem-Icons/scalable/apps` só existe `.svg` — então o PNG do
`hicolor` **nunca é alcançado**.

A logo canônica é colorida por construção, e o que importa não é só a cor:

```
assets/hefesto-logo.svg (medido)
  <linearGradient id="ring">      #8be9fd -> #bd93f9 -> #ff79c6
  <linearGradient id="flameOut">  #bd93f9 -> #ff79c6
  <linearGradient id="flameIn">   #ffb86c -> #f1fa8c
  <circle cx="101.72" cy="99.838" r="94" fill="#282a36"><title>Background</title></circle>
  <path d="M100 6 A94 94 0 1 1 43 25" fill="none" stroke="url(#ring)" stroke-width="6" .../>
```

**Repare no que isso significa para o pedido dela:** a logo **já é** "o círculo
com borda" que ela descreveu. O que sobra é (a) tirar a cor e (b) **tornar o
fundo transparente**.

O (b) não é detalhe estético. Recolorir, nesta pilha, quer dizer isto:

```
iced/wgpu/src/image/vector.rs:171-181
    rgba.chunks_exact_mut(4).for_each(|rgba| {
        if rgba[3] > 0 { rgba[0]=color[0]; rgba[1]=color[1]; rgba[2]=color[2]; }
    });
  -> substitui o RGB e PRESERVA o alfa
```

O desenho passa a ser **o recorte**, e nada mais. Um
`<circle r="94" fill="#282a36">` opaco, recolorido, vira um **disco chapado** da
cor do tema — a logo inteira desaparece dentro dele. **Grau: SUSPEITA COM
MECANISMO** (o binário do applet não foi executado; a máquina dela estava viva e
subir o applet mexeria na barra).

---

## A regra do COSMIC é real, e está escrita na máquina dela

**Grau: MEDIDO.** Ela disse *"no cosmic todos os applet são assim"*. Os
arquivos concordam:

```
$ for f in /usr/share/applications/*.desktop; do
    grep -q '^X-CosmicApplet=true' "$f" && \
      printf '%-48s %s\n' "$(basename "$f")" "$(sed -n 's/^Icon=//p' "$f" | head -1)"
  done | sort
```

| `.desktop` de applet | `Icon=` |
|---|---|
| CosmicAppletA11y | `preferences-desktop-accessibility-symbolic` |
| CosmicAppletAudio | `com.system76.CosmicAppletAudio-symbolic` |
| CosmicAppletBattery | `com.system76.CosmicAppletBattery-symbolic` |
| CosmicAppletBluetooth | `com.system76.CosmicAppletBluetooth-symbolic` |
| CosmicAppletInputSources | `com.system76.CosmicAppletInputSources-symbolic` |
| CosmicAppletNetwork | `com.system76.CosmicAppletNetwork-symbolic` |
| CosmicAppletNotifications | `com.system76.CosmicAppletNotifications-symbolic` |
| CosmicAppletPower | `com.system76.CosmicAppletPower-symbolic` |
| CosmicAppletTiling | `com.system76.CosmicAppletTiling-symbolic` |
| CosmicAppletTime | `com.system76.CosmicAppletTime-symbolic` |
| CosmicAppletMinimize | `com.system76.CosmicAppletMinimize` |
| CosmicAppletStatusArea | `com.system76.CosmicAppletStatusArea` |
| CosmicAppletWorkspaces | `com.system76.CosmicAppletWorkspaces` |
| **HefestoDualsense4Unix** | **`com.vitoriamaria.HefestoDualsense4Unix`** |

**Dez em treze** dos applets do System76 declaram `-symbolic`. **Os três que
não declaram desenham conteúdo dinâmico** — número do workspace, a própria
bandeja, lista de janelas — e não um glifo fixo.

**O Hefesto é o único applet de glifo fixo sem `-symbolic`.** A regra dela não
é impressão: é a única exceção da lista, e é a nossa.

---

## O vizinho que já faz certo — a receita, copiável

**Grau: MEDIDO.** Este é o achado mais útil desta sprint para quem executar: um
vizinho na mesma barra, servido pelo **mesmo** `cosmic-applet-status-area`, com
um ícone de origem **colorida**, aparece **branco**. Dá para copiar a receita
inteira dele.

O Spotify é Flatpak, pede `com.spotify.Client-symbolic`, e o arquivo que
satisfaz esse nome é:

```
~/.local/share/flatpak/exports/share/icons/hicolor/symbolic/apps/com.spotify.Client-symbolic.svg
```

O que ele tem, medido:

| propriedade | valor |
|---|---|
| diretório | `hicolor/**symbolic/apps**/`, não `scalable/apps/` |
| `viewBox` | `0 0 16 16`, com `width="16" height="16"` |
| cores no arquivo inteiro | **uma só**: `#bebebe`, duas ocorrências |
| `currentColor` | **zero** ocorrências |
| fundo | transparente; o desenho é **recorte** |

E o resultado na barra dela, medido na foto: silhueta acromática, as três ondas
do Spotify aparecendo como o **fundo do painel** através do recorte — enquanto
os dois arquivos **coloridos** que existem para o mesmo aplicativo continuam
coloridos no disco:

```
$ grep -oE '#[0-9a-fA-F]{6}' /usr/share/icons/Papirus/22x22/apps/com.spotify.Client.svg | sort -u
#1ed760   #3f3f3f   #ffffff        <- o verde do Spotify
$ identify ~/.local/share/icons/MeowSystem-Icons/512x512/apps/com.spotify.Client.png
PNG 512x512                        <- também colorido (renderizado e olhado)
```

Ou seja: **pedir um nome com sufixo `-symbolic` é o que muda o resultado**, e o
vizinho prova que a bandeja honra o sufixo. O caminho exato dentro do
`cosmic-applet-status-area` **não** foi lido (é outro binário, não o libcosmic
que medimos) — **grau: MEDIDO no efeito, SEM PROVA no caminho**, e fechar essa
lacuna é a entrega **E1**.

E o diretório `symbolic/apps` **é declarado pelo tema `hicolor`**, não é
invenção do Flatpak:

```
$ sed -n '/^\[symbolic\/apps\]/,+5p' /usr/share/icons/hicolor/index.theme
[symbolic/apps]
MinSize=8
Size=16
MaxSize=512
Context=Applications
Type=Scalable
```

### As duas convenções de cor, e por que a nossa tem de ser a clara

**Grau: MEDIDO** nos arquivos, **calculado** nos contrastes.

Há **duas** escolas entre os vizinhos, e elas não são equivalentes para nós:

| escola | cor no arquivo | depende de quê | se NÃO for recolorido |
|---|---|---|---|
| applets do System76 | `#232323` cravado (e `#808080` com `fill-opacity="0.01"` no retângulo de recorte) | de o libcosmic recolorir | **some** — 1,6:1 no painel dela |
| vizinho Flatpak (Spotify) | `#bebebe` cravado | de nada | **aparece** — cerca de 7,1:1 |
| o SVG simbólico que já temos no repositório | `currentColor` | de haver contexto de cor | **fica PRETO** e some |

Nenhum dos oito arquivos do System76 conferidos usa `currentColor`
(`grep -c currentColor` devolve zero em Audio, Battery, Bluetooth,
InputSources, Network, Power, Tiling e Time). Dentro do libcosmic tanto faz — o
RGB é sobrescrito. **Fora dele, faz toda a diferença.**

E o Hefesto precisa aparecer em **duas** superfícies com pilhas diferentes: a
bandeja (GTK/`librsvg`, via `cosmic-applet-status-area`) e o applet nativo
(libcosmic). **A cor clara cravada é a única que sobrevive às duas**: se for
recolorida, vira `#CACACA`; se não for, continua legível. A escura e o
`currentColor` só sobrevivem a uma.

---

## A armadilha do tema: "preto e branco" não pode virar "preto"

**Grau: MEDIDO no tema; calculado no contraste.**

O tema dela é escuro, e não por acaso do momento:

```
$ cat ~/.config/cosmic/com.system76.CosmicTheme.Mode/v1/is_dark
true
$ cat ~/.config/cosmic/com.system76.CosmicTheme.Mode/v1/auto_switch
false
```

O fundo do painel, medido no pixel da foto: `#2F2F3A`, sRGB (47,47,58) —
luminância relativa 0,0293. A cor que o COSMIC efetivamente aplica a um ícone
simbólico é o `background.on` do tema escuro dela:

```
$ ~/.config/cosmic/com.system76.CosmicTheme.Dark/v1/background   (bloco "on")
    on: ( red: 0.79136145, green: 0.791362, blue: 0.79136163, alpha: 1.0 )
  -> sRGB (202,202,202) = #CACACA, cinza claro e ACROMÁTICO (R=G=B)
```

Contraste WCAG sobre esse fundo:

| cor do glifo | contraste | veredito |
|---|---|---|
| preto `#000000` | **1,59 : 1** | **some** |
| `#232323` (a escola do System76, sem recoloração) | cerca de 1,6 : 1 | **some** |
| `#bebebe` (a escola do vizinho Flatpak) | cerca de 7,1 : 1 | legível |
| `#CACACA` (o que o COSMIC aplica) | 8,07 : 1 | legível |
| branco `#FFFFFF` | 13,22 : 1 | legível |

**Isto é o coração do pedido dela, e é onde uma execução ingênua erra.** Ela
pediu *"preto e branco"* e até sugeriu *"borda preta"*. Se alguém entregar um
ícone **preto fixo**, ele desaparece no painel dela — e a pessoa terá cumprido
a letra do pedido e destruído o propósito.

**O que "simbólico" resolve que cor fixa nenhuma resolve:** o arquivo simbólico
não carrega cor própria, carrega **forma**. Quem escolhe a tinta é o tema — no
escuro, cinza claro; no claro, escuro. Um ícone preto fixo acerta um tema e erra
o outro; um ícone branco fixo faz o inverso. Só o simbólico acerta os dois **sem
ninguém precisar tocar em nada quando ela trocar de tema**.

Traduzindo o pedido dela sem trair: **"preto e branco" quer dizer ACROMÁTICO,
não PRETO.**

### E o ícone vai ENCOLHER — conte com isso na foto

**Grau: MEDIDO.**

```
$ cat ~/.config/cosmic/com.system76.CosmicPanel.Panel/v1/size
S

cosmic-panel-config/src/panel_config.rs:145
    pub fn get_applet_icon_size(&self, is_symbolic: bool) -> u32 {
        if is_symbolic { XS=>16, S=>20, M=>28, L=>32, XL=>48 }
        else           { XS=>24, S=>32, M=>40, L=>48, XL=>56 }
    }
```

Com o painel dela em `S`, passar a simbólico troca **32 px por 20 px**. O ícone
vai ficar **menor**, além de acromático. Se quem executar não avisar, a foto do
depois vai parecer errada e ela vai reprovar por um motivo que ninguém explicou.
**Diga antes de mostrar.**

---

## O que não se apaga: três decisões medidas, com data

Regra da casa: decisão medida não se apaga, ganha nota datada com o que
caducou. São três, e as três atrapalham quem chegar sem saber.

### 1. Em 27/06/2026 o applet SAIU do simbólico — de propósito

**Grau: MEDIDO.**

```
$ git log -p --follow -- packaging/cosmic-applet/src/app.rs | grep -E "^[-+]const ICON" | sort -u
+const ICON_ALERT: &str = "battery-caution-symbolic";
+const ICON_APP: &str = "com.vitoriamaria.HefestoDualsense4Unix-symbolic";
-const ICON_APP: &str = "com.vitoriamaria.HefestoDualsense4Unix-symbolic";
+const ICON_APP: &str = "hefesto-dualsense4unix";
+const ICON_OFFLINE: &str = "action-unavailable-symbolic";

$ git log -1 --format="%h %ad %s" --date=short 13898ca
13898ca 2026-06-27 feat(v3.9.0): controle vivo no jogo, GUI auto-suficiente, ...
```

Até 27/06 o applet usava o **nome simbólico** e **trocava o glifo por estado**
(offline, bateria baixa). O commit `13898ca` trocou para o PNG colorido, e a
justificativa está gravada no cabeçalho de `packaging/cosmic-applet/src/app.rs`,
linhas 34-40:

> *"Antes o applet trocava o glifo para um SVG symbolic que não renderizava de
> forma confiável no tema (parecia sumir)."*

**Esta sprint propõe desfazer essa decisão.** Ela não pode ser desfeita por
gosto: a regra da casa diz que **hipótese tem de explicar o que já funcionava**.
Então a nota datada é esta:

> **Nota de 07/08/2026.** A decisão de 27/06 continua válida como registro do
> que se viu. O que caducou é a explicação: *"o SVG symbolic não renderizava de
> forma confiável"* nunca teve causa estabelecida. O arquivo existia e **era
> instalado** naquela data —
> `git show 13898ca:packaging/cosmic-applet/justfile` mostra as duas linhas que
> copiam o `-symbolic.svg` para `/usr/share/icons/hicolor/scalable/apps/`. Logo,
> "não existia o arquivo" **não** é a explicação. **O sumiço continua SEM
> PROVA**, e há hoje **dois** mecanismos candidatos, ambos SUSPEITA COM
> MECANISMO, ambos compatíveis entre si porque descrevem desfechos diferentes
> da mesma busca de ícone:
>
> **(a) O disco chapado.** O tema ativo dela serve, sob o nome pedido, um SVG
> colorido de **fundo opaco**; com `symbolic=true` forçado pelo
> `icon_button()`, o recolorir-por-alfa transforma a logo num disco liso da cor
> do tema. Some por virar mancha.
>
> **(b) O preto sobre preto.** O nosso `-symbolic.svg` usa `currentColor`, e
> vive em `scalable/apps/` e não em `symbolic/apps/`. Renderizado por
> `rsvg-convert` sem contexto de cor, sai **preto** — 1,59:1 no painel escuro
> dela. Some por não ter contraste. Isto foi **renderizado e olhado** em 07/08,
> a 16, 20, 24 e 48 px sobre o fundo medido do painel: a bigorna é quase
> indistinguível do fundo.
>
> **Reproduzir qual dos dois é a entrega E1.** Sem isso, refazer o simbólico é
> repetir 27/06 e esperar outro resultado.

### 2. O simbólico que já existe desenha uma BIGORNA — e o martelo já foi testado e descartado

**Grau: MEDIDO** (está escrito no cabeçalho do arquivo).

O arquivo
`packaging/cosmic-applet/data/icons/hicolor/scalable/apps/com.vitoriamaria.HefestoDualsense4Unix-symbolic.svg`
existe, é o único simbólico do projeto, e diz de si mesmo:

> *"Ícone SYMBOLIC do applet COSMIC — a BIGORNA da logo, em silhueta. [...] A
> logo cheia (`assets/hefesto-logo.svg`) a 16 px vira borrão; a bigorna é a
> forma mais reconhecível da marca e sobrevive ao tamanho da barra. [...]
> Desenhado direto na grade 16x16 (padrão symbolic), com o chifre à DIREITA
> [...] Coordenadas cruas, sem `transform-origin` (CSS SVG2 que o librsvg —
> renderizador do GTK e do COSMIC — ignora, jogando a forma para fora do
> viewBox). Validado com `rsvg-convert -w N -h N` em 16, 24 e 48 px, no claro e
> no escuro. Variante com martelo por cima foi testada e DESCARTADA: a 16 px o
> cabo virava um risco diagonal colado no topo da bigorna."*

Corpo: dois `<path fill="currentColor">` (mesa e chifre; cintura e base). **Sem
círculo, sem borda.**

> **Nota de 07/08/2026.** Isto **colide de frente** com a proposta de desenho
> dela — *"só o círculo com borda preta e a borda do martelo ao centro"*. A
> decisão antiga não se apaga: ela mediu que **martelo a 16 px vira risco**. Mas
> duas coisas mudaram e precisam entrar na conta antes de dar a decisão por
> encerrada:
>
> 1. **O alvo não é 16 px, é 20** (painel `S`, medido acima) — e o `viewBox`
>    16x16 continua sendo o certo, mas a renderização final tem 25% mais pixel
>    do que a que reprovou o martelo;
> 2. **A proposta dela não é "a logo inteira em silhueta"**, é uma composição
>    nova e mais simples: **círculo com borda** (que a logo já tem) **mais o
>    contorno do martelo ao centro** — contorno, não sólido. Não é a variante
>    que foi testada em junho.
>
> **A escolha é dela, e tem de voltar para ela com as duas versões
> renderizadas lado a lado a 20 px, no painel, ao lado dos vizinhos.** Ver a
> entrega E2. Quem decidir sozinho vai errar: ou desobedece o pedido dela, ou
> repete um borrão que já foi medido.

### 3. Em 31/07 a foto era o inverso da de hoje

**Grau: MEDIDO** nas duas datas.

A [RADAR-01](2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md)
mediu, em 31/07, que **o applet nativo estava no painel** (PID 4505, e
`com.vitoriamaria.HefestoDualsense4Unix` listado na asa esquerda do
`plugins_wings`) e que **a bandeja GTK estava morta** — sem
`cosmic-applet-status-area`, sem watcher, com o `cosmic_tray_warned.flag`
escrito. Aquela medição inverteu a premissa da própria sprint, e por isso a E1
de lá veio antes da E2.

> **Nota de 07/08/2026.** Aquela medição **caducou, e inverteu**. Hoje o
> `cosmic-applet-status-area` **está** no painel e **está** rodando (PID
> 797776); a bandeja GTK **está viva e registrada** no watcher; e o applet
> nativo **não está** no `plugins_wings` **nem em processo nenhum**. Não se
> sabe quando nem por que a troca aconteceu — **SEM PROVA** — e é plausível que
> tenha sido um ajuste dela no painel, o que é direito dela e não defeito de
> ninguém.
>
> **A lição de método é a que importa:** qual das duas superfícies ela está
> vendo **não é constante**, e nenhuma sprint pode presumir. Quem executar
> **mede antes** — o comando está na E1 — em vez de herdar a foto de outra
> semana. E, pela mesma razão, a entrega precisa deixar **as duas** superfícies
> corretas: a que ela vê hoje e a que pode voltar amanhã.

---

## As entregas, em ordem, com o que cada uma custa

**E0 e E2 dependem de decisão dela.** As outras não.

### E0 — a pergunta que é dela, e vai antes de tudo

**Custo: uma conversa. Bloqueia E2.**

Duas perguntas, e nenhuma delas é nossa para responder:

1. **O desenho.** A bigorna em silhueta que já existe, ou o círculo com borda e
   o contorno do martelo que ela propôs? (Ver a nota 2 acima — há medição
   antiga contra o martelo, e ela merece saber disso antes de escolher.)
2. **O applet nativo volta para a barra?** Hoje ele não está lá. Se ela não
   quiser de volta, a sprint é só sobre a bandeja, e as entregas do lado Rust
   viram higiene de código em vez de conserto do que ela vê.

### E1 — medir o caminho da bandeja antes de escrever qualquer coisa

**Custo: baixo — só leitura e um arquivo de teste descartável. Não toca no
painel dela.**

O que precisa ficar sabido, porque hoje é SEM PROVA:

- **o `cosmic-applet-status-area` recolore, ou só desenha o que acha?** O
  vizinho Flatpak não distingue os dois casos: o arquivo dele já é acromático
  (`#bebebe`) **e** o nome dele é simbólico. Um teste que separa: pôr um SVG
  **colorido** em `hicolor/symbolic/apps/` sob um nome `-symbolic` de brinquedo,
  registrar um item de bandeja de mentira e olhar. Se sair acromático,
  recolore; se sair colorido, quem tem de ser acromático é o **arquivo**;
- **`~/.local/share/icons/hicolor/symbolic/apps/` é alcançado?** O `hicolor`
  do sistema declara `symbolic/apps` no `index.theme`, mas o `hicolor` do HOME
  dela **não tem** esse subdiretório hoje. Pela especificação os diretórios do
  mesmo tema se somam entre as bases XDG — **SUSPEITA COM MECANISMO**, não
  verificado. Se não somar, o destino da E3 muda;
- **qual dos dois mecanismos do "sumiço" de 27/06 é o verdadeiro** (nota 1
  acima). Reproduzir **é a condição** para desfazer aquela decisão sem repetir
  o erro.

**Sem E1, E2 e E3 são chute com aparência de conserto.**

### E2 — desenhar o símbolo

**Custo: médio, e é o único trabalho de desenho da sprint. Depende de E0 e E1.**

Contrato do arquivo, todo ele copiado do vizinho que já funciona:

- `viewBox="0 0 16 16"`, com `width="16" height="16"` — grade simbólica;
- **uma cor só**, acromática e **clara**, cravada — a escola do vizinho
  Flatpak, pelo motivo da seção *"As duas convenções"*. **Não** `currentColor`:
  fora do libcosmic ele cai para preto e some;
- **fundo transparente**. O desenho é o **recorte**. Sem `<circle>` opaco de
  fundo, ou o recolorir-por-alfa devolve um disco chapado;
- **sem `transform-origin`** — o `librsvg` ignora e joga a forma para fora do
  `viewBox`. Está registrado no cabeçalho do simbólico que já existe, e é
  armadilha medida, não teoria;
- validado com `rsvg-convert -w N -h N` em **16, 20, 24 e 48 px**, no claro e no
  escuro. O **20** é novo nesta lista e é o tamanho real do painel dela.

**Entregar as duas versões renderizadas para ela escolher** (E0.1), montadas
sobre o fundo `#2F2F3A` medido e **ao lado do recorte real dos vizinhos**. O
critério dela é comparativo — a foto tem de deixar comparar.

### E3 — instalar sob o nome certo, no diretório certo

**Custo: médio. Toca os dois instaladores, que são independentes e não se
conhecem.**

Hoje **nenhum dos dois** instala um SVG simbólico sob o nome que o código pede:

| instalador | o que faz hoje | destino |
|---|---|---|
| `install.sh` | gera 11 PNGs de `assets/appimage/Hefesto-Dualsense4Unix.png`, copia o pixmap, e **apaga** (`:1840`) qualquer `.svg` sob `${APP_ID}` | `~/.local`, **sem** `sudo` |
| `packaging/cosmic-applet/justfile` | instala `com.vitoriamaria.HefestoDualsense4Unix-symbolic.svg` — **sob um nome que o código não pede desde 27/06** | `/usr`, **com** `sudo` |

O que a entrega precisa fazer:

1. instalar o simbólico novo em `hicolor/symbolic/apps/` (destino a confirmar
   pela E1), sob o nome **que o código vai pedir**;
2. **rever a linha `install.sh:1959`** — ela apaga `${APP_ID}.svg`. Se o nome
   novo for `${APP_ID}-symbolic.svg`, ela não o alcança; mas deixar uma linha
   que apaga SVG num diretório onde agora existe SVG de propósito é armadilha
   para a próxima pessoa. **Comente o porquê ou restrinja o alvo**;
3. **`uninstall.sh` precisa de linha nova.** Hoje ele remove `${APP_ID}.png`
   por tamanho (`:424`), `${APP_ID}.svg` de `scalable/` (`:426`), o pixmap
   (`:427`) e, com `sudo`, os arquivos do applet (`:451`). **Nada em
   `symbolic/apps/`.** Sem essa linha, desinstalar deixa lixo — e lixo de ícone
   é o tipo que reaparece em instalação futura e produz "não mudou nada" sem
   explicação;
4. **os quatro alvos de empacotamento** que o portão de paridade cobra
   (`scripts/build_deb.sh`, `packaging/arch/PKGBUILD`,
   `packaging/fedora/hefesto-dualsense4unix.spec`, `packaging/nix/package.nix`)
   precisam instalar o mesmo arquivo, ou o portão reprova. Ver *"Os portões"*.

**`install.sh` nunca com `sudo`** (o `HOME` vira `/root`), e sem TTY use
`--yes`. Regra da casa, e ela vale aqui.

### E4 — o código passa a pedir o nome novo

**Custo: baixo em linhas, alto em atenção — são quatro lugares e eles não se
conhecem.**

| onde | o que muda |
|---|---|
| `src/hefesto_dualsense4unix/app/tray.py:44` | `TRAY_ICON_NAME` — **é este que muda o que ela vê hoje** |
| `packaging/cosmic-applet/src/app.rs:40` | `ICON_APP` |
| `packaging/cosmic-applet/data/com.vitoriamaria.HefestoDualsense4Unix.desktop` | `Icon=` — é o ícone da lista *Configurações > Painéis > Miniaplicativos* |
| `src/hefesto_dualsense4unix/app/main.py:187` | `Gtk.Window.set_default_icon_name` — **provavelmente NÃO muda** |

**A última linha é uma armadilha e merece parágrafo.** O ícone da **janela** e
o ícone do **painel** têm requisitos opostos: a janela quer a logo cheia e
colorida (é assim que ela reconhece o aplicativo na troca de janelas), o painel
quer a silhueta acromática. **Trocar os dois "por coerência" estraga a janela
para consertar a barra.** Ela não pediu isso. Não faça.

E há rede de segurança do lado da bandeja, que também tem de continuar
funcionando: `src/hefesto_dualsense4unix/app/tray.py:443-444` só usa o nome se
`theme.has_icon()` responder que ele existe; senão cai em `input-gaming`, um
joystick genérico. **Se o nome novo não for instalado direito, o sintoma não
será "ícone feio": será um joystick genérico na barra dela.** Vale um teste que
morda exatamente isso.

### E5 — os portões, para que isto não volte

**Custo: médio. Sem esta entrega, a próxima pessoa desfaz tudo sem perceber.**

1. **`scripts/gerar_icones.sh` precisa aprender o simbólico.** Hoje ele deriva
   dois PNGs de `assets/hefesto-logo.svg` e compara **pixel a pixel** com
   `compare -metric AE`. O simbólico **não** é derivável por escala da logo
   colorida — é desenho próprio. As saídas honestas são: (a) deixá-lo fora do
   gerador e travá-lo por outro portão; ou (b) ensinar o gerador a tratá-lo como
   fonte independente. **O que não pode é ficar sem dono**, que é como o
   `-symbolic` atual chegou a 07/08 instalado sob um nome que ninguém pede;
2. **um teste que morde**, em arquivo novo sob `tests/unit/` <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->,
   com pelo menos quatro asserções: o SVG simbólico existe; tem `viewBox`
   16x16; **não** contém `currentColor`; e **não** contém mais de uma cor.
   Arranque cada uma e veja reprovar antes de devolver — teste que passa com a
   cura arrancada não testa nada;
3. **um teste de contrato de nome:** o nome que `tray.py` pede e o nome que
   `app.rs` pede **terminam em `-symbolic`**, e existe arquivo instalado para
   cada um. Isto é o que impede a regressão de 27/06 de voltar em silêncio.

### E6 — a prova de tela, com ela

**Custo: dez minutos dela. É o que fecha a sprint.**

Sem isto a sprint **não fecha**, por regra da casa. Detalhe na seção seguinte.

---

## Como validar: o critério dela é "igual aos outros"

Regime:
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
— foto antes, foto depois, e **a palavra final é dela**.

Mas aqui dá para ir além do olho, porque o critério que ela deu é comparativo e
**mensurável**. A prova é a **mesma tabela de saturação** desta sprint, refeita
depois:

| medida | antes (07/08, medido) | critério de aceite |
|---|---|---|
| saturação máxima do Hefesto | **255** | **na faixa dos vizinhos**, cerca de 30 a 37 |
| histograma do recorte | seis matizes (roxo, laranja, azul, branco) | **R=G=B** nos pixels do desenho |
| contraste do glifo sobre `#2F2F3A` | — | **acima de 4,5:1** |
| tamanho da caixa | cerca de 26 px | vai **encolher** (32 px para 20 px) — avise antes |

**A foto tem de mostrar os vizinhos.** Um recorte só do ícone do Hefesto não
responde à pergunta dela, que é de **comparação**. O enquadramento é a asa
direita inteira, como o recorte `320x36+1600+0` desta sprint.

**E a prova tem de cobrir os dois temas.** O simbólico existe justamente para
sobreviver à troca; se ninguém olhar no claro, a metade não verificada é
exatamente a que uma cor fixa quebraria.

**Sequência sugerida, para não atrapalhar o uso dela:** foto do antes; aplicar;
reiniciar a barra (ela **vai** sumir e voltar — combine); foto do depois; medir
a tabela; **só então** mostrar. Chegar com a medição pronta poupa o tempo dela e
respeita o que a casa aprendeu sobre clique cego em janela alheia.

---

## Os portões que vão reprovar, e como não brigar com eles

**Grau: MEDIDO** — os quatro foram lidos em 07/08.

**1. ÍCONE-VIVO-01 — o PNG é travado pixel a pixel, por três caminhos.**
`scripts/gerar_icones.sh --check` compara os derivados com
`assets/hefesto-logo.svg` usando `compare -metric AE`, e roda em **três**
lugares: o hook `icones-refletem-o-svg` do `.pre-commit-config.yaml`, o job
`icones` do `.github/workflows/ci.yml`, e `tests/unit/test_icones_refletem_o_svg.py`.
**Consequência:** quem "resolver" o pedido dela editando o PNG à mão, ou
descolorindo `assets/hefesto-logo.svg`, reprova nos três. E descolorir a logo
canônica seria pior que reprovar — ela é a fonte do ícone da **janela**, do
lançador e do AppImage, que **devem** continuar coloridos.

**2. O portão de paridade tem uma regra que vai bater de frente com a E4.**
`scripts/check_packaging_parity.sh` lê os nomes pedidos em `main.py` e
`tray.py` e exige, para **cada** um, a string `apps/${icon}.png` nos quatro
alvos de empacotamento. Se `TRAY_ICON_NAME` passar a terminar em `-symbolic`, o
portão vai cobrar um **PNG** chamado `...-symbolic.png` — que é exatamente o
que **não** se deve criar. **O portão precisa aprender a exceção junto com a
entrega:** nome terminado em `-symbolic` se satisfaz com `.svg` em
`symbolic/apps/`. Alterar o portão é parte da E5, não desvio dela — e a
alteração tem de **continuar reprovando** o caso que ele nasceu para pegar
(nome pedido pelo código sem arquivo instalado). O comentário de
`scripts/check_packaging_parity.sh:105-114` conta por que essa regra existe:
alinhar tudo num nome só já consertou o lançador e **quebrou a janela e a
bandeja**. Não afrouxe.

**3. O portão de referências é cego a arquivo novo.** Rode os portões **depois**
do `git add`. Regra da casa, e esta sprint cria arquivo novo em pelo menos dois
diretórios.

**4. Acentuação, glifos e idioma.** Português do Brasil com acentuação correta
em código, comentário, documentação e mensagem de commit. Nada de emoji. O
cabeçalho do SVG novo é documentação como qualquer outra.

**A leva fecha com a lista do `CLAUDE.md`**, na ordem de lá, depois do
`git add -A`.

---

## O que fica ABERTO

1. **O desenho é dela** (E0.1). Bigorna em silhueta, ou círculo com borda mais
   contorno do martelo? Há medição de junho contra o martelo a 16 px, e o alvo
   real é 20 px. **Não decida sozinho.**
2. **O applet nativo volta para a barra?** (E0.2) Hoje ele está compilado,
   instalado e fora do painel. Se não voltar, metade das entregas é higiene, não
   conserto.
3. **Por qual caminho o `cosmic-applet-status-area` acromatiza o vizinho?**
   **SEM PROVA.** Decide se o arquivo precisa ser acromático por si ou se basta
   o sufixo no nome. É a E1.
4. **Qual dos dois mecanismos explica o sumiço de 27/06?** **SEM PROVA**, dois
   candidatos com mecanismo lido. Enquanto não se reproduzir um, desfazer
   aquela decisão é apostar.
5. **`~/.local/share/icons/hicolor/symbolic/apps/` é alcançado pela busca de
   ícones?** **SUSPEITA COM MECANISMO.** O `hicolor` do sistema declara o
   diretório; o do HOME dela não o tem. Se a soma entre bases XDG não valer, o
   destino da E3 muda.
6. **A cópia da logo dentro do tema dela não é nossa, e pode sombrear tudo de
   novo.** `~/.local/share/icons/MeowSystem-Icons/scalable/apps/hefesto-dualsense4unix.svg`
   é byte a byte igual à nossa logo canônica, tem data de 04/08 23:09, e **quem
   a pôs ali é SEM PROVA**. O tema ativo é procurado **antes** de todos os
   herdados: se um dia alguém copiar para lá um `...-symbolic.svg` colorido, o
   defeito volta e **nenhum portão deste repositório vai ver**, porque o arquivo
   não é versionado aqui. Pedir um nome **novo** (com sufixo) é o que hoje
   contorna o sombreamento — não é blindagem.
7. **Ninguém mediu o tema CLARO.** Toda a aritmética de contraste desta sprint é
   sobre o painel escuro dela (`is_dark=true`, `auto_switch=false`). O simbólico
   deve resolver os dois por construção — **mas isso é a promessa, não a
   medição**.
8. **Esta sprint não entrou em índice nenhum.** Nasceu depois do índice de
   06/08. Quem executar deve pendurá-la no índice aberto do dia.

---

## O que a execução de 07/08 mediu e entregou

Escrito **depois** de executar, no mesmo dia, com a máquina dela viva e em uso.
Nada foi reiniciado: nem o daemon, nem a GUI dela, nem a barra. Os testes na
tela foram feitos com **processos descartáveis**, que sobem, aparecem na barra
e saem sozinhos — o processo dela (PID 792339) não foi tocado.

**Grau de cada afirmação, como manda a casa.**

### A condição que a sprint pôs foi cumprida: o "sumiço" de 27/06 foi REPRODUZIDO

A regra da casa diz que hipótese tem de explicar o que já funcionava, e esta
sprint proibia refazer o simbólico sem antes reproduzir o que fez 27/06
desistir dele. Reproduzido, e **é o mecanismo (b)**, o "preto sobre preto":

```
$ rsvg-convert -w 20 -h 20 -o /tmp/bigorna.png \
    <o simbólico de 27/06, com fill="currentColor">
$ convert /tmp/bigorna.png -alpha off -format "%[pixel:p{10,4}]" info:
srgb(0,0,0)
```

**MEDIDO.** `currentColor` sem contexto de cor resolve para **preto**, e preto
sobre o `#2F2F3A` do painel escuro dela dá **1,59:1**. O glifo não "sumia" por
bug de tema, nem por arquivo faltando: **ele era desenhado preto sobre preto.**
A justificativa de 27/06 — *"não renderizava de forma confiável no tema"* —
está agora com causa, e a causa é uma linha do arquivo, não uma
imprevisibilidade da pilha.

O mecanismo (a) da nota 1 (*"o disco chapado"*, o tema dela servindo uma cópia
colorida de fundo opaco) **não foi o de 27/06** — a cópia dentro de
`MeowSystem-Icons` é de **04/08**, cinco semanas depois. Mas o disco chapado
**existe**, é real, e apareceu por outro caminho — o de baixo.

### A armadilha nova, e ela ia estragar exatamente o desenho que ela pediu

**Grau: MEDIDO**, com imagem renderizada e olhada.

Ela pediu *"só o círculo com borda"* — ou seja, **contorno**. O jeito óbvio de
desenhar contorno em SVG é `stroke` com `fill="none"`. **Não pode.**

O GTK recolore ícone simbólico injetando CSS no arquivo:

```
rect,circle,path {fill: <cor do tema> !important;}
```

O `!important` **atropela** o `fill="none"`. Montado um tema de ícones de
prova com dois arquivos — o mesmo aro em `stroke` e em preenchimento vazado —
e carregados os dois por `Gtk.IconTheme.lookup_icon(...).load_symbolic(...)`:
o de `stroke` saiu um **disco liso**, com o desenho inteiro sumido dentro dele;
o de preenchimento saiu perfeito.

**É o "disco chapado" da nota 1, por um caminho que a sprint não previu.** Uma
execução que atendesse o pedido dela ao pé da letra — `stroke`, como qualquer
um desenharia — teria entregue uma bolota branca na barra dela, e a causa
levaria horas para achar. Por isso o arquivo entregue faz **todo contorno com
`fill-rule="evenodd"`** e dois subcaminhos, e há teste que reprova o `stroke`.

### As duas perguntas SEM PROVA da E1 foram fechadas, com a barra dela

**1. O `cosmic-applet-status-area` recolore, ou só desenha o que acha?**
**RECOLORE — MEDIDO.** Foi feito exatamente o teste que a E1 propunha: dois
itens de bandeja de mentira, registrados por um processo descartável, pedindo
dois arquivos com o **mesmo desenho** e nomes `-symbolic`, um em `#ff00ff`
(magenta) e outro em `#bebebe`. Na foto da barra dela os dois saíram
**idênticos e acromáticos**:

| ícone na barra | saturação máxima (de 255) |
|---|---|
| Spotify (vizinho que já funciona) | 30,6 |
| **prova em `#ff00ff`** | **30,6** |
| **prova em `#bebebe`** | 34,2 |
| Hefesto (o de verdade, colorido) | **255** |

Os ~30 são o azulado do fundo do painel entrando no recorte, exatamente como a
medição da manhã já dizia. **O magenta desapareceu por completo.**

Consequência prática: **dentro do painel, a cor do arquivo não importa** — o
que importa é o sufixo `-symbolic` no nome. A cor clara cravada continua sendo
a escolha certa, mas pelo motivo de **fora** do painel (a bandeja GTK, o
`rsvg-convert`, qualquer consumidor que não recolore), não pelo de dentro.

**2. `~/.local/share/icons/hicolor/symbolic/apps/` é alcançado?**
**SIM — MEDIDO, e por dois caminhos independentes.** A dúvida era boa: o
`index.theme` do `hicolor` **do HOME dela** (que existe, é de 04/08 e **não é
nosso** — nenhum script deste repositório o escreve) **não lista**
`symbolic/apps` em `Directories=`. Mesmo assim:

- `Gtk.IconTheme.get_default().lookup_icon()` acha um arquivo posto lá, com ou
  sem `gtk-update-icon-cache` rodado;
- e o **painel dela desenhou** os dois itens de prova acima, servidos desse
  diretório.

O destino da E3 fica sendo `symbolic/apps/`, como a sprint queria.

### O que ela vai ver, medido na barra dela

Foto tirada com um `AppTray` **de verdade** — o código de hoje, a classe de
produção, `_preferred_icon()` incluído — num processo descartável ao lado do
processo dela. Por isso a foto tem **os dois ao mesmo tempo**: o antigo
(colorido, do processo dela, que ainda pede o nome velho) e o novo (simbólico),
lado a lado, com os vizinhos.

```
nome pedido: hefesto-dualsense4unix-symbolic
apptray_started  icon=hefesto-dualsense4unix-symbolic
```

| medida | antes | depois | critério |
|---|---|---|---|
| saturação máxima | **255** | **20,7** | faixa dos vizinhos (22 a 40) — **cumpre** |
| pixels do desenho | seis matizes | acromáticos | **cumpre** |
| tamanho | 32 px | 20 px | encolheu, como previsto |

**As fotos são efêmeras** e não entram no repositório — o projeto não versiona
imagem da área de trabalho dela. Para refazer, os comandos estão na seção *"O
que a barra dela mostra hoje, em número"*; as coordenadas mudaram (a asa é
ancorada à direita, então cada ícone a mais empurra tudo para a esquerda).

### O que foi entregue

| entrega | estado |
|---|---|
| **E0.1** o desenho | **PENDENTE — é dela.** As duas opções estão desenhadas e renderizadas a 20 px, lado a lado |
| **E0.2** o applet volta à barra? | **PENDENTE — é dela.** O lado Rust foi consertado de qualquer forma |
| **E1** medir o caminho | **FEITO**, acima |
| **E2** desenhar o símbolo | **FEITO** — `assets/simbolico/hefesto-dualsense4unix-symbolic.svg` |
| **E3** instalar sob o nome certo | **FEITO** — `install.sh`, `uninstall.sh`, `purge.sh`, o `justfile` do applet e os quatro alvos de empacotamento |
| **E4** o código pede o nome novo | **FEITO** — `tray.py`, `app.rs` e o `.desktop` do applet. O `main.py` **não** foi tocado, de propósito: o ícone da janela continua a logo colorida |
| **E5** os portões | **FEITO** — `tests/unit/test_simbolico_do_painel.py` (17 asserções) e duas guardas novas em `check_packaging_parity.sh` |
| **E6** a prova de tela com ela | **PENDENTE — é o que fecha a sprint** |

O desenho entregue é o **dela**: aro (círculo com borda) e a **borda** da
cabeça do martelo ao centro, com o cabo cheio. O cabo é a única concessão, e
tem número: vazado, a 20 px o furo teria **0,9 px** e viraria borrão.

A bigorna de 27/06 **não foi apagada**: virou
`assets/simbolico/opcao-b-bigorna-symbolic.svg`, com nota datada no cabeçalho
explicando o que caducou (o `currentColor`) e o que continua valendo (a medição
contra o martelo a 16 px). Se ela escolher a bigorna, **o encanamento já está
pronto** — troca-se o desenho e nada mais.

### O defeito que a própria execução criou, e que virou portão

**Grau: MEDIDO.** O cabeçalho do SVG novo ganhou uma linha de traços de
separação, como todo cabeçalho deste projeto. Em XML, `--` **fecha
comentário**: o arquivo virou XML inválido e o `rsvg-convert` passou a recusá-lo
inteiro. **O painel continuou desenhando** (o renderizador dele é mais
tolerante), então o defeito era invisível na tela — e teria aparecido só na
bandeja GTK, que usa librsvg, em alguma máquina que não a dela.

Nenhum dos outros dezesseis testes pegava, porque **todos leem o SVG como
texto**. Agora há `test_o_simbolico_e_xml_valido`, que faz o parse de verdade.

### A mordida

Dezesseis curas arrancadas, uma por vez, **dezesseis reprovas** —
`currentColor` de volta, aro feito de `stroke`, cor escura, segunda cor,
`viewBox` fora da grade, fundo opaco, desenhos divergentes entre bandeja e
applet, `tray.py` voltando ao nome sem sufixo, a queda direto no joystick
genérico, `app.rs` voltando ao PNG, o `.desktop` voltando ao colorido, o
`install.sh` deixando de copiar, o `uninstall.sh` deixando de remover, o `rm`
do `install.sh` virando curinga, o `--` no comentário, e um alvo de
empacotamento sem o arquivo.

Uma delas **não mordeu na primeira tentativa**, e está registrada no próprio
teste: a asserção do `install.sh` procurava o **caminho do arquivo** no texto
do script, e passava com a linha de cópia arrancada — o caminho continuava lá,
na variável e na mensagem de aviso. Foi reescrita para asserir a **linha que
copia**. Teste que passa com a cura arrancada não testa nada.

### O que continua ABERTO

1. **O desenho é dela** (E0.1). As duas opções estão prontas e renderizadas;
2. **O applet nativo volta para a barra?** (E0.2) Continua compilado, instalado
   e fora do painel. O binário **não foi recompilado** nesta execução: a
   primeira build do libcosmic é longa e a máquina dela está em uso. Enquanto
   não recompilar, `app.rs` está certo no fonte e velho no binário;
3. **A prova de tela com ela** (E6) — foto, os dois temas, e a palavra final;
4. **O tema CLARO só foi SIMULADO.** Renderizado com a cor que o tema claro
   dela aplicaria (`#272727`, lida de `CosmicTheme.Light/v1/background`) sobre
   fundo claro: legível, com folga. Mas ela não trocou de tema, e ninguém
   olhou a barra clara de verdade — **SUSPEITA COM MECANISMO**;
5. **A cópia da logo dentro do tema dela continua lá**, e continua não sendo
   nossa. Pedir um nome com sufixo contorna o sombreamento; não o blinda. Se um
   dia aparecer um `...-symbolic.svg` colorido dentro de `MeowSystem-Icons`, o
   defeito volta e nenhum portão deste repositório vai ver;
6. **O arquivo instalado na máquina dela foi posto à mão**, no mesmo caminho e
   com o mesmo conteúdo que o `install.sh` instala
   (`~/.local/share/icons/hicolor/symbolic/apps/hefesto-dualsense4unix-symbolic.svg`).
   Ele fica **inerte** até a GUI dela reiniciar — o processo vivo pediu o nome
   antigo quando subiu, e ícone de bandeja não se troca sozinho.

---

## O redesenho de 07/08 à tarde — a DECISÃO 14, executada

Escrito **depois** de executar, no mesmo dia, com a máquina dela viva e em uso.
Nada foi reiniciado e **nada foi instalado**: esta leva mexe em arquivo do
repositório e em teste, e mais nada. O desenho novo **não** foi copiado para o
tema dela — a palavra final é dela, e instalar antes seria decidir por ela.

**O que ela decidiu**, e é o que manda aqui:
[DECISÕES DELA de 07/08](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md),
resposta 14 — *"redesenhar o símbolo mais parecido com a logo, mantendo a grade
pequena"*. Isso **fecha a E0.1** de um jeito que o painel de opções não previa:
nem a bigorna de 27/06, nem o desenho da manhã como estava. Redesenhar.

A leitura desta execução, e ela é o contrato do trabalho: **a legibilidade a 16
e 20 px é inegociável, e dentro dessa restrição o desenho se aproxima da logo o
máximo que der.**

### A medição que mudou o desenho mais do que o pedido

**Grau: MEDIDO.** Antes de desenhar qualquer coisa, os vizinhos da barra dela
foram renderizados a 320 px (20 vezes a grade de 16) e tiveram o **traço**
medido por varredura de alfa na linha do meio, em unidades da grade de 16:

| ícone | largura | altura | traço no meio |
|---|---|---|---|
| energia | 12,00 | 13,00 | **2,05** |
| som | 15,50 | 11,90 | **2,00** |
| Bluetooth | 11,00 | 15,10 | massa (4,45 e 4,75) |
| Spotify | 16,00 | 16,00 | massa |
| **o simbólico da manhã** | 14,80 | 14,80 | **1,15** |

Reproduzir, para qualquer arquivo:

```
rsvg-convert -w 320 -h 320 <arquivo.svg> -o /tmp/med.png
convert /tmp/med.png -alpha extract -depth 8 txt:- | \
  awk -F'[,:( ]+' '$2==160 && $3>60 {print $1}' | sort -n
```

**O traço mínimo da barra dela é 2,0 unidades, e o nosso tinha 1,15.** O ícone
não estava só com o desenho errado: estava com **metade do peso** dos vizinhos.
Isso não aparece em nenhuma foto isolada — só na comparação, que é justamente o
critério dela (*"no cosmic todos os applet são assim"*).

O aro novo, medido no arquivo entregue pelo mesmo comando: **1,70**, com o cabo
do martelo em 1,40 e a caixa do desenho em 14,80 por 15,20.

**E 1,70 não é 2,00, de propósito — vale dizer em vez de esconder.** Com 2,00 o
furo do aro cai para raio 5,4, o canto da cabeça do martelo passa a ficar a 0,70
dele, e a 20 px essa folga some no antisserrilhado: o martelo encosta no aro e
vira mancha. **1,70 é o mais grosso que ainda deixa o martelo respirar.** Na
outra ponta, o aro da logo é proporcionalmente muito mais fino (equivalente a
0,47 nesta grade), então 1,70 já é 3,6 vezes ele. Aqui **a barra ganhou da
fidelidade**, e é a única troca desta leva em que isso aconteceu.

### O que o redesenho trouxe da logo, item por item

**Grau: MEDIDO** (cada número saiu de `assets/hefesto-logo.svg`).

| o que | na logo | no símbolo novo | antes |
|---|---|---|---|
| o aro | arco **aberto** de 323 graus, falha de 232 a 269 graus, uma **conta** em cada ponta | idêntico nos ângulos; contas de raio 1,25 | círculo fechado, sem contas |
| a cabeça | **cheia**, canto arredondado de 25% da espessura | cheia, canto 0,65 sobre espessura 2,60 | vazada (moldura) |
| o cabo | cápsula (`rx` igual a metade da largura) | cápsula, ponta de baixo redonda | barra de canto vivo |
| cabeça sobre cabo | 25,8 por 11,7 = **2,20** | 2,60 por 1,35 = **1,93** | 3,40 por 1,20 = 2,83 |
| peso do traço | irrelevante a 512 px | 1,70 (barra pede 2,00) | 1,15 |

A falha do aro com as duas contas é **a marca mais reconhecível da logo e a mais
barata em pixel**: aparece inteira já a 16 px, e é o que faz o ícone novo parecer
o Hefesto e não um martelo genérico.

### A bigorna e o martelo juntos NÃO cabem — três tentativas, três borrões

**Grau: MEDIDO**, com imagem renderizada e olhada nas três.

A composição inteira da logo (aro, martelo e bigorna) foi tentada **três vezes**,
com geometrias diferentes e as partes engrossadas até o limite da grade. As três
viraram borrão a 20 px. O motivo é aritmético, e é o que faltava no registro de
27/06: **na logo, a cabeça do martelo ENCOSTA na mesa da bigorna** (a cabeça
termina em y=120,1 e a mesa começa em y=119,5, medido depois da matriz de cada
grupo), e quem separa as duas é a **cor** — cinza contra branco. Em monocromia
não há cor para separar, e o vão precisaria de 1 px que não existe.

> **Nota de 07/08/2026.** A decisão de 27/06 (*"variante com martelo por cima da
> bigorna foi testada e DESCARTADA"*) **continua válida, e agora tem causa**: não
> é o tamanho da grade sozinho, é a falta de vão entre as duas peças na própria
> logo. Aumentar a grade não resolveria; separar as peças deixaria de ser a logo.

### A medição que favorece a bigorna, e o quanto ela favorece

**Grau: MEDIDO**, e os números abaixo são dos **arquivos que estão no disco**,
não dos rascunhos do caminho. Reduzindo a logo a 20 px e recortando a **mancha
clara** (o que sobra dela no tamanho do painel: o aro com a falha, a bigorna
branca e o risco do cabo), dá para medir quanto cada candidato **cobre** dessa
mancha:

| candidato | interseção sobre união | cobre da mancha da logo |
|---|---|---|
| **opção C, a bigorna no aro** | **0,211** | 46,9% |
| **o entregue, o martelo no aro** | 0,205 | 46,9% |
| o símbolo da manhã | 0,200 | 41,7% |

Reproduzir: renderizar `assets/hefesto-logo.svg` a 20 px sobre preto, tomar como
mancha os pixels com luminância acima de 110, e comparar com o alfa de cada
candidato a 20 px.

**A bigorna ganha por três centésimos, e isso é uma diferença pequena que vale
dizer em voz alta.** Numa versão intermediária do caminho, com o aro FINO da
manhã, a bigorna abria muito mais vantagem (0,285 contra 0,212). O aro grosso,
que a barra exigiu, ocupa mais pixel e passa a dominar a conta dos dois lados —
então a peça do meio pesa menos do que parecia. **Registrado porque é fácil citar
o 0,285 achando que ele descreve o arquivo entregue: não descreve.**

**E mesmo com a bigorna à frente, não foi ela a entregue.** O motivo é regra da
casa, não gosto: ela **nomeou o martelo** em 07/08 pela manhã, e a decisão 14
pediu **redesenhar** o símbolo mais parecido com a logo — não trocar o motivo
dele. Trocar a peça central é mudança que ela não pediu, e três centésimos de
cobertura não compram essa troca. Então a bigorna foi desenhada, renderizada, e
**entregue como opção pronta** em
`assets/simbolico/opcao-c-bigorna-no-aro-symbolic.svg`: se ela preferir, é copiar
um arquivo por cima de outro, e nada no encanamento muda.

### O que foi entregue

| arquivo | o que é |
|---|---|
| `assets/simbolico/hefesto-dualsense4unix-symbolic.svg` | o símbolo redesenhado: aro aberto da logo, com as contas, e o martelo cheio ao centro |
| `packaging/cosmic-applet/data/icons/hicolor/symbolic/apps/com.vitoriamaria.HefestoDualsense4Unix-symbolic.svg` | a mesma coisa, byte a byte (há teste) |
| `assets/simbolico/opcao-c-bigorna-no-aro-symbolic.svg` | a bigorna dentro do mesmo aro, para ela escolher |
| `tests/unit/test_simbolico_do_painel.py` | 18 asserções (eram 17) |

A bigorna de 27/06 (`assets/simbolico/opcao-b-bigorna-symbolic.svg`, sem aro)
**continua onde estava**: não se apaga decisão medida.

### O teste que caducou, e o que entrou no lugar

**Grau: MEDIDO** (arrancado e visto reprovar).

O aro novo é **aberto**, e um arco aberto é um caminho fechado simples: não
precisa de `fill-rule="evenodd"`, porque não tem furo. A asserção antiga
`assert 'fill-rule="evenodd"' in corpo` passaria a travar **uma técnica**, não um
defeito — e a técnica mudou. Ela saiu, e no lugar entrou
`test_o_aro_e_faixa_e_nao_disco`, que lê os raios dos comandos de arco e exige
**dois raios distintos** com o furo valendo pelo menos 60% do raio de fora.

Isso trava o defeito de verdade, que é o **disco chapado** reproduzido pela
manhã: um disco tem um raio só. A asserção contra o `stroke` **não foi tocada**,
palavra por palavra.

### A mordida

Sete curas arrancadas, uma por vez, **sete reprovas**:

| cura arrancada | quem reprovou |
|---|---|
| o aro virou disco (um raio só) | `test_o_aro_e_faixa_e_nao_disco` |
| a faixa engordou até o furo cair para 3,0 | `test_o_aro_e_faixa_e_nao_disco` |
| o aro voltou a ser `stroke` com `fill="none"` | `test_contorno_e_preenchimento_nunca_stroke` **e** `test_o_aro_e_faixa_e_nao_disco` |
| `currentColor` de volta | `test_uma_cor_so_acromatica_e_clara` |
| bandeja e applet com desenhos diferentes | `test_bandeja_e_applet_servem_o_mesmo_desenho` |
| uma segunda cor no desenho | `test_uma_cor_so_acromatica_e_clara` |
| linha de traços no comentário | `test_o_simbolico_e_xml_valido` |

### A foto, e o que ela mostra

**As fotos continuam efêmeras** e não entram no repositório. A desta leva põe,
**a 20 px e nos dois temas**: a logo, o símbolo antigo, o novo e a opção C, mais
a faixa com os vizinhos reais da barra (Spotify, Bluetooth, som, rede, energia).

Um detalhe de método que evita alarme falso: no tema claro o arquivo **não** pode
ser fotografado com a cor que ele carrega (`#bebebe` sobre fundo claro fica
lavado). A foto tinge cada ícone com a cor que o COSMIC aplica em cada tema —
`#CACACA` no escuro, `#272727` no claro, ambas lidas do tema dela. Quem refizer
a foto sem tingir vai concluir, errado, que o ícone some no claro.

### O que continua ABERTO

1. **A palavra final é dela** (E6), e agora ela tem três desenhos para olhar: o
   novo, a opção C e o antigo. **Nada foi instalado** — o que está no tema dela
   continua sendo o desenho da manhã;
2. **O tamanho da conta do aro é o limite do desenho.** As contas alcançam 7,80
   de 8,00 a partir do centro; maiores, encostam na borda do `viewBox`. Na logo
   a proporção é ainda mais apertada (99 de 100), então isto é fidelidade, não
   descuido — mas quem for mexer precisa saber que não há folga ali;
3. **O applet nativo continua sem recompilar**, como na execução da manhã;
4. **O tema claro continua só SIMULADO** — renderizado com a cor lida do tema
   dela, nunca olhado na barra clara de verdade.
