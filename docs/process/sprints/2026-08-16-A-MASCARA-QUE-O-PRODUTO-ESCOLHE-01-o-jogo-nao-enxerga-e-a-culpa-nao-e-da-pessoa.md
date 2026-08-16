# A MÁSCARA QUE O PRODUTO ESCOLHE — 01

*o jogo não enxerga, e a culpa não é da pessoa*

**16/08/2026, madrugada.** Sprint de diagnóstico. Nenhuma linha de código
entrou por aqui: o que entra é o **desenho** e a **medição** que ele precisa
para não nascer errado.

---

## 0. O cabeçalho é a decisão dela

Quando o Duskfade ficou sem controle, a saída óbvia era pedir a ela que
trocasse a máscara na aba Início — dois cliques, `DualSense (PS)` vira
`Xbox 360`, e pronto. Foi o que lhe ofereci. A resposta, no dia:

> *"isso não é solução é gambiarra... o produto em si existe pra que as
> mascaras funcionem sempre."* <!-- noqa-acento -->

E quando pus três caminhos na mesa, ela escolheu **"descobrir a engine do
jogo"**.

Essas duas frases são o escopo desta sprint, e nenhuma das duas é negociável:

1. **A escolha da máscara não é trabalho da pessoa.** Um interruptor que ela
   precisa achar sozinha, depois de o jogo já ter ficado mudo, é o defeito —
   não a cura. Hoje `docs/usage/jogos-e-mascaras.md` **ensina** a fazer essa
   escolha à mão ("o controle funciona na Steam mas fica morto dentro do jogo →
   use Xbox 360"), e é exatamente esse parágrafo que o produto tem de tornar
   desnecessário.
2. **A decisão sai do jogo, não de uma lista.** "Descobrir a engine" quer dizer
   olhar para o que está no disco daquele jogo e concluir. Não quer dizer
   manter um `appid → máscara` mantido à mão, que é receita, e receita deixa
   todo jogo lançado amanhã descoberto.

**Estado da escolha dela, medido:** `grep -rn "XInputDevice\|unreal\|UE[45]"`
em `src/` devolve **zero**. A escolha nunca virou código. É por isso que esta
página existe.

---

## 1. São DOIS defeitos, e eles são diferentes

Este é o parágrafo mais importante da página, porque eu quase os confundi — e
quem os confunde conserta o lugar errado e jura que curou.

| | **(A) Pragmata** | **(B) Duskfade** |
|---|---|---|
| appid | `3357650` | `2542020` |
| sintoma | o jogo para de reconhecer o controle no Bluetooth | o jogo nunca reconhece o controle |
| o wrapper `hefesto-launch` | **sumiu** da linha de `LaunchOptions` | **está lá, intacto** |
| o `launch_env` do daemon | materializado e **nunca lido** | materializado e **lido** |
| quem venceu | a lista de ignorados da própria Steam, com o `0x054c/0x0df2` do nosso vpad dentro | ninguém: o jogo procura um aparelho que não existe na mesa |
| causa | **infraestrutura** — a Steam guarda uma linha por jogo e ela foi sobrescrita | **compatibilidade** — o jogo só fala XInput e a máscara é PlayStation |
| estado | **CURADO** — [SENTINELA-WRAPPER-01](2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md) | **SEM CURA** — é esta sprint |

O que os faz parecer o mesmo defeito: **em ambos o controle continua vivo**. A
luz acesa, o perfil ativo, a vibração respondendo no menu da Steam — e só o
jogo cego. Do lado de fora é idêntico. Por dentro não tem nada a ver.

### 1.1 (A) O Pragmata, em três linhas — não refaça

Uma variável nova (`VKD3D_CONFIG=no_upload_hvv`, posta para curar o crash de
14/08) **substituiu** o wrapper na única linha de `LaunchOptions` que a Steam
guarda por jogo. Sem o wrapper, o `launch_env` do daemon nunca é lido, e quem
chega ao jogo é o `SDL_GAMECONTROLLER_IGNORE_DEVICES` **da Steam** — que traz
`0x054c/0x0df2`, o PID do nosso vpad, dentro. O jogo foi mandado ignorar o
controle que o produto criou para ele.

A cura entregou detecção, aviso com o nome do jogo e reparo que **preserva** o
que já estava na linha. Confirmado no disco agora, com a Steam fechada:

```
UserLocalConfigStore/apps/3357650/LaunchOptions =
  sh -c 'W="$HOME/.local/share/hefesto-dualsense4unix/bin/hefesto-launch"; \
  [ -x "$W" ] && exec "$W" "$@"; exec env "$@"' \
  hefesto-launch VKD3D_CONFIG=no_upload_hvv %command%
```

**As duas coisas na mesma linha** — o wrapper e a cura do crash. É o desenho
certo, e está de pé. Censo da biblioteca dela neste momento: **77 linhas de
`LaunchOptions`, 75 com o wrapper**.

**Não refaça este trabalho.** Se o sintoma que você está perseguindo é "parou
de funcionar de repente, num jogo que funcionava", ele é (A) e já tem dono.

---

## 2. (B) O Duskfade — a evidência, com endereço

Tudo abaixo foi lido no disco dela em 16/08/2026, com a Steam fechada, o daemon
parado e nenhum jogo aberto. **GRAU: MEDIDO AQUI.**

### 2.1 O jogo é Unreal Engine 5.6, e o único plugin de gamepad é o XInput

`~/.steam/debian-installation/steamapps/common/Duskfade/Duskfade/Saved/Logs/Duskfade.log`
(gravado em 13/08 14:35, 342 KB):

```
LogInit: Build: ++UE5+Release-5.6-CL-44394996
LogCsvProfiler: Display: Metadata set : engineversion="5.6.1-44394996+++UE5+Release-5.6"
...
:215  LogPluginManager: Mounting Engine plugin XInputDevice
```

São **165 linhas `Mounting … plugin`** naquele log. Filtrando por qualquer
palavra que possa significar entrada — `input`, `pad`, `controller`, `device`,
`joy`, `steam`, `sdl`, `raw` — sobram oito, e sete delas não são caminho de
gamepad:

| plugin montado | o que é |
|---|---|
| `EnhancedInput` | o sistema de *bindings* da UE, não um backend de aparelho |
| `InputDebugging` | ferramenta de depuração |
| `OnlineSubsystemSteam`, `SteamShared` | Steamworks (conquistas, rede) — não entrada |
| `ExampleDeviceProfileSelector`, `WindowsDeviceProfileSelector` | perfil de *renderização* por aparelho |
| `GooglePAD` | *Play Asset Delivery*, Android |
| **`XInputDevice`** | **o único backend de gamepad montado** |

### 2.2 Não há SDL na pasta do jogo

```
find …/common/Duskfade -iname "*SDL*"   →   0 arquivos
```

Zero. O jogo não carrega SDL, então nada do que este projeto faz **pelo caminho
do SDL** o alcança. E o que o produto entrega para o Duskfade hoje é,
literalmente, duas variáveis de SDL — veja 2.4.

### 2.3 O Steam Input está desligado para este appid

`~/.steam/debian-installation/userdata/<conta>/config/localconfig.vdf`,
bloco `UserLocalConfigStore/apps/2542020`:

```
"UseSteamControllerConfig"    "0"
```

Logo, **não há espelho Xbox da Steam para este jogo** — que seria a outra
maneira de um aparelho `045e`-ish aparecer na frente dele. (E há uma reviravolta
sobre **quem** desligou isso: seção 5.)

### 2.4 O que o produto entrega ao Duskfade, e por que não basta

`~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_2542020.env`,
escrito às 03:33 de 16/08:

```
# estado: perfil gamepad dualsense (prognóstico uhid) | native=False
#         emulacao=False mascara=dualsense backends=[] | 2026-08-16T03:33:50
PROTON_DISABLE_HIDRAW=0x054C/0x0CE6
SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6,0x28de/0x11ff
__GL_SHADER_DISK_CACHE=1
__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1
SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0
```

Três das cinco variáveis são do SDL, e o jogo não tem SDL (2.2). A quarta,
`PROTON_DISABLE_HIDRAW`, esconde o `hidraw` do **físico** — o desenho correto
para o caminho `winebus`, mas ele não faz nascer nada que o XInput reconheça.
E o perfil dele, `~/.config/hefesto-dualsense4unix/profiles/duskfade.json`,
diz:

```json
"mode": { "kind": "gamepad", "gamepad_flavor": "dualsense", "coop": true }
```

Máscara `dualsense`, escolhida **à mão**, como todo `gamepad_flavor` hoje
(`profiles/schema.py:525`).

### 2.5 O par que não se encontra

Com a máscara `dualsense`, o vpad nasce **`054c:0df2`** — Sony, PS5 Edge
(`integrations/uhid_gamepad.py`). Com a máscara `xbox`, ele nasce
**`045e:028e`** com o nome `Microsoft X-Box 360 pad (…)`
(`integrations/uinput_gamepad.py:54-56`) — que é a identidade que o mundo
XInput procura.

O Duskfade monta o `XInputDevice` e mais nada. **O jogo procura um aparelho que
o produto, naquele perfil, não oferece.** O wrapper está intacto, o
`launch_env` foi lido, o daemon fez tudo certo — e não havia nada a fazer,
porque o problema não é de canal: é de **identidade**.

**Nota de honestidade sobre o mecanismo.** Que o Duskfade só monte o
`XInputDevice` é **MEDIDO**. Que o `XInputDevice` da UE, rodando sob Proton,
exija especificamente o VID `045e` é **MÉDIA, não medida**: sob Proton quem
apresenta o aparelho ao lado Windows é o `winebus.sys`, e a canônica desta casa
leu o `winebus` para `hidraw` (`docs/protocol/pilha-steam-input-xpad-sdl.md`,
§3.2–3.3) mas **não** leu por qual critério ele marca um aparelho como
XInput-capaz. Essa leitura falta, e ela é o primeiro item do §7.

---

## 3. O preço da máscara Xbox — cinco coisas, e é por isso que a decisão é difícil

Se a máscara Xbox fosse grátis, o produto podia usá-la sempre e esta sprint não
existiria. Ela não é.

Com `Xbox 360` **a vibração continua**. O que se perde são **cinco coisas**,
medidas e escritas em [jogos-e-mascaras.md](../../usage/jogos-e-mascaras.md):

| perdido | por quê |
|---|---|
| giroscópio | o pacote do Xbox 360 não tem eixos de movimento |
| touchpad | nem pontos de toque |
| cor da lightbar | nem campo de cor |
| gatilhos adaptativos | nem canal de efeito de gatilho |
| leitura de bateria | nem campo de carga |

A causa não é o Linux nem falta de trabalho aqui: o relatório de um Xbox 360
tem **vinte bytes, treze usados**, e não sobra lugar. A demonstração está em
três camadas independentes na canônica
([a pilha do Steam Input](../../protocol/pilha-steam-input-xpad-sdl.md), §1.5):
(a) o protocolo não carrega o dado; (b) o `xpad` não declara a capacidade —
`xpad_init_input` percorre cinco tabelas e não há um `input_set_capability` de
`EV_ABS` fora delas (`xpad.c:1958`, `xpad.c:439-493`); (c) o `hid-playstation`
registra **quatro** nós de entrada para um DualSense, o `xpad` registra **um**
(`xpad.c:2053`).

**Consequência de desenho, e ela é o coração do problema:** trocar a máscara
sozinho não é um botão neutro que o produto pode apertar por precaução. É
**pagar cinco recursos** para comprar um. Um produto que trocasse por via das
dúvidas roubaria giroscópio e lightbar de dezenas de jogos dela que funcionam
hoje. A cura tem de ser **certeira**, não preventiva — e é essa exigência que
transforma "trocar a máscara" em "descobrir o jogo".

**A hipótese tem de explicar o que já funcionava.** Ela funciona: os jogos que
andam bem hoje com `DualSense (PS)` ou falam SDL, ou falam HID direto, ou pedem
os recursos do DualSense à API da Steam. Nenhum deles é XInput-only. A cura que
esta sprint pede só age onde o sinal do disco disser XInput-only — e onde não
disser, nada muda.

---

## 4. O que o produto precisaria saber para decidir sozinho — e o que ele não tem

A pergunta que a cura tem de responder é uma só:

> **Este jogo consegue enxergar um `054c:0df2`?**

Se sim, a máscara DualSense fica e as cinco coisas ficam junto. Se não, a
máscara Xbox é a única que entrega controle — e aí o produto troca, avisa o
preço, e não pede nada a ninguém.

### 4.1 O que o produto TEM hoje

- **a biblioteca da Steam**: `integrations/jogos_locais.py:143`
  (`jogos_da_biblioteca_steam`) varre todo `appmanifest_*.acf` de toda
  biblioteca configurada e devolve `appid` + `nome`;
- **a linha de `LaunchOptions` de cada jogo** e o resto do `localconfig.vdf`:
  `integrations/steam_launch_options.py`, com `pastas_steamapps()` já
  resolvendo o `libraryfolders.vdf`;
- **o casamento janela → jogo**: o perfil casa por `window_class`
  `steam_app_<id>`, que é o campo que funciona nos dois mundos (X11 e Wayland
  puro) — medido em 10/08 na
  [PERFIL-MUDO-01](2026-08-10-PERFIL-MUDO-01-o-perfil-do-jogo-que-nao-entrou.md);
- **o interruptor**: `gamepad_flavor: Literal["dualsense","xbox"]`
  (`profiles/schema.py:525`) já existe e o daemon já sabe montar o env dos dois
  jeitos (`daemon/launch_env.py`, `compose_env`, ramo `flavor == "xbox"`).

Ou seja: **o atuador está pronto**. Falta o sensor.

### 4.2 O que o produto NÃO tem — os quatro buracos

1. **A pasta do jogo.** `JogoLocal` é `(appid, nome, fonte)` e mais nada
   (`jogos_locais.py:86-99`); `_campos_do_acf` lê **só** `appid` e `name`
   (`jogos_locais.py:124-142`), por decisão explícita de não escrever um segundo
   parser de VDF. O `installdir` está no mesmo `.acf`, a uma chave de
   distância, e sem ele não há como olhar para dentro do jogo.
2. **O leitor do disco do jogo.** Nada em `src/` procura por `XInputDevice`,
   por `Engine/Binaries`, por `*.pak`, por `libSDL*`, por `steam_api64.dll`.
   Zero ocorrências, conferido.
3. **O lugar onde essa conclusão mora.** Um veredito de compatibilidade
   descoberto ao abrir o jogo não é o mesmo que uma preferência gravada pela
   pessoa: se o produto escrever `gamepad_flavor: "xbox"` por cima do perfil
   dela, ele apaga uma escolha; se não escrever em lugar nenhum, redescobre
   tudo a cada abertura. Falta um campo **derivado**, separado do escolhido, e
   uma regra de precedência — *a vontade dela vence sempre*, como em 09/08.
4. **A frase na tela.** A regra de 09/08 é *tudo chega na interface*. Trocar a
   máscara sozinho e não dizer nada é o pior dos mundos: ela perde giroscópio e
   lightbar sem saber por quê, e volta a caçar o interruptor — só que agora
   contra o produto. Precisa de uma linha na aba Início dizendo **o quê**,
   **por quê** e **como desfazer**.

### 4.3 As três regras que a cura tem de respeitar

- **Universal.** O sinal vem do disco do jogo, nunca de um `appid` cravado nem
  de lista mantida à mão. Um jogo lançado amanhã tem de nascer coberto porque a
  pasta dele será lida do mesmo jeito.
- **Sem flag, no install.** Sem opção nova para ligar, sem passo manual.
- **Reversível e visível.** A pessoa tem de conseguir dizer "não neste jogo", e
  essa recusa tem de sobreviver ao próximo `./install.sh` — o mesmo desenho do
  `jogos_sem_wrapper.txt` da SENTINELA-WRAPPER-01, que já provou o padrão.

**O que a cura NÃO pode ser:** "quando o jogo não responder em 10 segundos,
troca a máscara". Isso é adivinhação com custo de cinco recursos, e ainda por
cima quebraria jogos que demoram a inicializar.

---

## 5. ACHADO DESTA LEVA — quem desligou o Steam Input do Duskfade fomos NÓS

Isto não estava no diagnóstico de origem e muda o desenho.

O `UseSteamControllerConfig = 0` do Duskfade (§2.3) **não é escolha dela**. O
guard desta casa reescreve `1`/`2` → `0` em todo appid que **não** esteja na
allowlist: `scripts/disable_steam_input.sh:293-297`.

A prova é o censo do `localconfig.vdf` dela agora:

| `UseSteamControllerConfig` | appids |
|---|---|
| `"2"` (preservado) | `3357650` (Pragmata), `2111190` (Mullet Mad Jack) |
| `"0"` | os outros **nove**, Duskfade entre eles |

E os dois preservados são **exatamente** os dois appids que têm bloco de
configuração e estão em
`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`. Não é coincidência: é a
allowlist funcionando como projetada. No nível global,
`SteamController_PSSupport = "0"` — também do guard, que sempre o zera.

**Por que isto importa para o Duskfade.** O Steam Input, quando ligado para um
appid, cria um **espelho** `28de:11ff` chamado `Microsoft X-Box 360 pad N` —
que é, nome e forma, a coisa que um jogo XInput-only procura. Existe portanto
uma **quarta via** para o Duskfade que não passa por trocar a nossa máscara:
ligar o Steam Input daquele jogo.

**E ela tem preço próprio, medido:** o guard reaplica Steam Input OFF, e a
descrição do conflito já está escrita em
[troubleshooting-8bitdo.md](../../usage/troubleshooting-8bitdo.md) (§ *Gyro ×
Steam Input × o guard do hefesto*) — hoje **não há configuração que dê as duas
coisas ao mesmo tempo**, e o Steam Input ligado num jogo vale para **todos** os
controles daquele jogo. Trocar "a pessoa escolhe a máscara à mão" por "a pessoa
gerencia a allowlist do Steam Input à mão" é a mesma gambiarra com outro nome —
e é por isso que esta via **não é o caminho padrão** desta sprint. Ela fica
registrada como alternativa que existe, com o preço na mesa.

---

## 6. O ACHADO EM ABERTO — 8 espelhos contra "zero espelhos"

**Isto é um fato a verificar, não uma conclusão.** Escrito assim de propósito,
porque das duas medições uma está errada e a resposta muda o diagnóstico do
Duskfade.

### As duas medições que não fecham

- **11/08/2026, canônica, §2.4-bis, item 4** — com um jogo em sessão
  (`AppId 1599660`), varredura de `/sys/class/input`: *"nenhum dispositivo
  `X-Box 360 pad` nem `Steam Virtual`"*. Conclusão registrada com **GRAU:
  MEDIDO AQUI**: o par `0x28de/0x11ff` do nosso `IGNORE_DEVICES` é redundante
  porque **não há espelho**.
- **16/08/2026, nesta madrugada, antes de a Steam fechar** — **8** dispositivos
  `28de:11ff`, `Microsoft X-Box 360 pad 0` a `7`, vivos na máquina dela.

### O que consegui medir agora, com a Steam fechada

**Zero.** `grep -c 28de /proc/bus/input/devices` → `0`. Nenhum processo
`steam`, nenhum jogo, daemon parado. Isso não decide nada: o espelho é da
Steam, e a Steam não está de pé. Confirma apenas que os espelhos **não
sobrevivem** ao fechamento dela.

### O que consegui medir e **muda o quadro**

O arquivo que a Steam usa para dizer ao jogo quem é cada espelho —
`~/.steam/debian-installation/config/virtualgamepadinfo.txt`, **mtime 16/08
03:24**, ou seja, escrito nesta madrugada — tem **dois slots**:

```
[slot 0]  name=DualSense Edge Wireless Controller   VID=0x054c PID=0x0df2  type=ps5
[slot 1]  name=DualSense Wireless Controller        VID=0x054c PID=0x0ce6  type=ps5
```

Três coisas saem daí, e nenhuma é pequena:

1. **O subsistema de gamepad virtual da Steam estava ATIVO em 16/08.** Ele não
   escreve esse arquivo à toa. Isso é compatível com os 8 dispositivos e
   **incompatível** com "a Steam não cria espelho nesta máquina".
2. **O slot 0 é o NOSSO vpad** (`054c:0df2`). O terceiro-controle de 10/08 está
   vivo: a Steam espelha o gamepad virtual do Hefesto como se fosse hardware.
3. **Os dois slots ocupados são `type=ps5`, e são só dois — mas os
   dispositivos eram oito.** A leitura mais econômica é que a Steam cria um
   **conjunto fixo de oito** nós no `/dev/uinput` ao subir e só **descreve** os
   que estão realmente ocupados. Se for isso, "quantos nós existem" e "quantos
   controles a Steam vê" são perguntas diferentes, e a varredura de 11/08 pode
   ter respondido a segunda achando que respondia a primeira.

### O que NÃO explica a divergência

Descartado por medição: **não houve atualização do cliente Steam entre 11/08 e
16/08.** `logs/bootstrap_log.txt` mostra `Download skipped … version
1785799196, installed version 1785799196` nas verificações de 16/08, e o
`package/steam_client_ubuntu12.installed` é de **10/08 23:30** — anterior à
medição de 11/08. O mesmo binário produziu as duas leituras.

### O ensaio que decide, e ele é de um minuto

Com a Steam **aberta** e nenhum jogo rodando:

```bash
grep -c '28de' /proc/bus/input/devices
grep -B4 'Vendor=28de' /proc/bus/input/devices | grep -E '^N:'
cat ~/.steam/debian-installation/config/virtualgamepadinfo.txt
```

Depois, com **um jogo aberto**, repita — e some
`scripts/medir_steam_virtual_gamepad.sh`, que já existe no repositório
justamente para isto e lê `/proc/<pid>/environ` do jogo.

**Por que isto muda o diagnóstico do Duskfade.** Se os oito espelhos existem
sempre que a Steam está aberta, então **o XInput tem o que enumerar** mesmo com
`UseSteamControllerConfig=0`, e a causa do Duskfade pode não ser "não há
aparelho Xbox na mesa" — pode ser "há, e o jogo não o alcança", que é outro
defeito, com outra cura. Construir a troca automática de máscara **antes** de
responder isto é arriscar-se a pagar as cinco perdas do §3 para curar algo que
tinha outra causa.

**E há uma segunda consequência, para a canônica.** Se o ensaio confirmar os
espelhos, a linha de §2.4-bis que diz *"o par `0x28de/0x11ff` é redundante"*
deixa de valer: com o
`SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD=1` já medido no ambiente do
jogo (mesma seção, item 1), o SDL **usa** os espelhos, e o ramo de
`SDL_gamepad.c:3273-3331` retorna antes de consultar a lista de ignorados — o
par volta a ser o problema que a leitura do fonte previu em 11/08 e que a
medição do mesmo dia arquivou por falta de alvo. Pela regra da casa, o número
errado se **substitui**; mas só depois de medido, e por enquanto ele é
**suspeito**, não refutado.

---

## 7. O que isto NÃO resolve

Escrito antes de existir código, para que ninguém prometa mais do que a cura
entrega.

1. **Falta a leitura do `winebus` sobre XInput.** A canônica leu o `winebus`
   para `hidraw` (§3.2–3.3) e **não** leu por qual critério ele marca um
   aparelho como XInput-capaz do lado Windows. Sem isso, "a máscara `045e`
   resolve o Duskfade" é **hipótese**, e o ensaio que a julga é abrir o jogo com
   `gamepad_flavor: "xbox"` — nenhuma linha de código necessária, e é o teste
   mais barato desta página inteira. **Faça-o antes de construir.**
2. **Um jogo que não fale nem XInput, nem SDL, nem HID direto continua fora.**
   Um título com backend de entrada próprio, ou que só aceite um aparelho por
   nome exato, não é alcançado por nenhuma máscara que o produto saiba montar.
   Este sprint aumenta a cobertura; não a fecha.
3. **A detecção por disco erra nos dois sentidos, e os dois erros têm custo.**
   Um jogo que monte o `XInputDevice` **e** carregue SDL (a UE aceita ambos, e
   muitos títulos empacotam os dois) seria marcado XInput-only e pagaria as
   cinco perdas do §3 sem precisar. Um jogo que resolva o backend em tempo de
   execução, sem deixar rastro na pasta, não seria marcado e continuaria mudo.
   O sinal tem de ser **conservador**: na dúvida, mantém-se `dualsense`, porque
   errar para o lado de não trocar preserva o que já funciona.
4. **O Steam Input é uma quarta via, e ela tem dono e preço.** Ver §5: o guard
   desta casa a desliga de propósito, e ligá-la por jogo é mexer numa allowlist
   — trabalho manual, que é o que ela recusou. Enquanto o conflito
   guard × Steam Input não tiver desenho próprio, essa via não é resposta.
5. **Nada aqui toca no defeito (A).** Se o wrapper sumir de novo, é a sentinela
   que age. As duas curas não se substituem.

---

## 8. O que ficou pronto nesta página, e o que fica para quem escrever o código

**Pronto aqui:** a separação dos dois defeitos; a evidência do Duskfade com
endereço e data; o preço da máscara Xbox com a demonstração em três camadas; o
inventário do que o produto tem e dos quatro buracos; o achado de que o
Steam Input do Duskfade foi desligado por nós; e o ensaio de um minuto que
julga a contradição dos espelhos.

**Para quem escrever o código, na ordem:**

1. rodar o ensaio de §6 com a Steam aberta — **antes de qualquer linha**;
2. rodar o ensaio de §7.1: Duskfade com `gamepad_flavor: "xbox"` à mão, uma
   vez, só para saber se a máscara resolve. Se não resolver, esta sprint inteira
   muda de alvo;
3. só então: `installdir` no `_campos_do_acf`, o leitor do disco do jogo, o
   campo derivado com precedência da vontade dela, a frase na aba Início, e a
   recusa por jogo que sobrevive ao install.

**Estado final:** nenhum arquivo de código foi tocado. Nenhum comando foi
executado contra a Steam, o daemon ou os controles — todas as medições desta
página são leituras de disco e de `/proc`, com a máquina em repouso.

---

## Ver também

- [SENTINELA-WRAPPER-01](2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md)
  — o defeito (A), curado
- [O WRAPPER QUE SUMIU 01](2026-08-16-O-WRAPPER-QUE-SUMIU-01-uma-variavel-nova-apaga-a-ponte-em-silencio.md)
  — como o defeito (A) foi achado
- [TRES-CONTROLES-01](2026-08-10-TRES-CONTROLES-01-o-espelho-do-espelho-no-pragmata.md)
  — o espelho do Steam Input, medido pela primeira vez
- [a pilha do Steam Input](../../protocol/pilha-steam-input-xpad-sdl.md) — §1.5
  (o preço), §2 (o espelho), §3.2–3.3 (o `winebus`)
- [jogos-e-mascaras.md](../../usage/jogos-e-mascaras.md) — o texto que hoje
  exige a escolha à mão, e que esta sprint quer tornar desnecessário
- [troubleshooting-8bitdo.md](../../usage/troubleshooting-8bitdo.md) — o
  conflito guard × Steam Input
