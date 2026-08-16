# A linha que a Steam come — o censo dos campos, e a árvore errada

- **Escrito em:** 16/08/2026, entre 04h30 e 06h, com ela dormindo. Steam fechada,
  nenhum controle tocado, nenhum jogo aberto
- **A pergunta que o gerou:** o `LaunchOptions` foi o campo que quebrou ontem.
  **Quais OUTROS campos têm a mesma forma?** — isto é, o produto escreve, a Steam
  pode sobrescrever, e ninguém percebe
- **O que este documento é:** o censo de uma classe — *campo de configuração que
  o produto escreve num arquivo de outro dono*. Para cada um: quem escreve, quem
  vigia, o que a Steam faz, e o que o buraco custa
- **O que ele NÃO é:** não fecha nada e não substitui a sprint
  `SENTINELA-WRAPPER-01`. Duas curas saíram junto com ele (`scripts/doctor.sh` e
  `install.sh`); tudo o mais está nomeado com dono e preço
- **Leitura obrigatória antes de agir na seção 3:** o achado central **não é o
  Pragmata**. É que o instrumento que o vigia **confirma a si mesmo**

> **Grau de cada afirmação**, na convenção da casa: **MEDIDO** = arquivo lido ou
> comando rodado nesta sessão; **RECONSTRUÍDO** = derivado de backups datados e
> leitura de código; **SEM PROVA** = está dito e ninguém verificou.
>
> Nenhum endereço de rádio aparece aqui. Os appids aparecem porque já estão em
> páginas versionadas desta casa e são públicos da Steam.

---

## 0. A régua: o que faz um campo entrar neste censo

> O produto escreve um valor num arquivo **de outro dono**. O outro dono
> reescreve esse arquivo por conta própria, em momentos que o produto não
> controla, e **não avisa**. O valor volta ao que era — ou some — e o produto
> continua afirmando que está tudo certo, porque ele nunca releu.

O `LaunchOptions` é o exemplar perfeito, e por isso custou uma noite dela. Mas a
forma é genérica, e há sete campos com ela.

Uma segunda régua, que só apareceu ao medir, e que vale mais que a primeira:

> Um instrumento que lê **a própria escrita** do produto de volta não mede nada.
> Ele confirma. E confirma com mais convicção quanto mais o produto escreveu.

---

## 1. O censo dos campos

Arquivos envolvidos: `~/.steam/…/userdata/<id>/config/localconfig.vdf` (por
usuário), `~/.steam/…/config/config.vdf` (global), e dois arquivos NOSSOS em
`~/.config/hefesto-dualsense4unix/`.

| # | Campo | Onde | O produto escreve? | Vigiado? | O que a Steam faz | Preço do buraco |
|---|---|---|---|---|---|---|
| 1 | `LaunchOptions` (por app) | `localconfig.vdf`, `Software/Valve/Steam/apps/<appid>` | **Sim** — `apply_wrapper_to_all_games`, botão da GUI, passo 11b do install | **Parcialmente, desde hoje** — censo read-only no doctor e reparo no install; **nenhum guard periódico** | Guarda **uma linha por jogo**; qualquer texto novo (variável de vídeo, mod, a própria pessoa) **substitui** o wrapper em silêncio | O defeito de 15/08: jogo sem controle nenhum no rádio, com o controle vivo e o perfil aceso |
| 2 | `SteamController_PSSupport` (global) | `localconfig.vdf`, `Software/Valve/Steam` | **Sim** — `1|2 → 0` | **Sim** — `hefesto-steam-input-guard.path` + `.timer` (30 min) | Reescreve ao sair e após update, reativando | Steam toma o hidraw do DualSense: touchpad vira mouse, botões em background |
| 3 | `SteamController_SwitchSupport` (global) | idem | **Sim** — `1|2 → 0` | **Sim** — mesmo guard | idem, para os controles Switch/8BitDo | **Buraco medido**: ver 2.4 — a chave não existe no vdf dela, e o script só REESCREVE, nunca INSERE |
| 4 | `UseSteamControllerConfig` (por app) | `localconfig.vdf`, `UserLocalConfigStore/apps/<appid>` — **outra árvore, não a do 1** | **Sim** — `1|2 → 0`, exceto os appids da allowlist | **Sim** — mesmo guard | Escreve `2` quando a pessoa liga o Steam Input daquele jogo | — |
| 5 | `steam_input_apps.txt` (allowlist, arquivo NOSSO) | `~/.config/hefesto-dualsense4unix/` | Sim (GUI e CLI) | — | — | **Buraco medido**: ver 2.3 — a lista **só preserva, nunca liga**; entrada posta tarde demais fica inerte para sempre |
| 6 | `SteamControllerRumble` / `SteamControllerRumbleIntensity` (por app) | `localconfig.vdf`, junto do 4 | **Não** | Não | Escreve `-1` / `320` em todo jogo cujo painel de controle ela abriu (11 jogos) | **SEM PROVA**: ninguém mediu se o caminho de rumble da Steam disputa com o nosso |
| 7 | `CompatToolMapping` (por app + global) | `config.vdf` | **Sim** — `proton_pin.py --lock`, passo 11c do install | Não periodicamente; só no install | Reescreve `config.vdf` ao sair | Upgrade de Proton devolve o controle duplicado (é a razão do pin) |
| 8 | `jogos_sem_wrapper.txt` (arquivo NOSSO) | `~/.config/hefesto-dualsense4unix/` | Sim | — | — | Sai **de propósito** do reparo. Correto: é a vontade dela, e o produto não briga com a dona da máquina |

**A assimetria que este censo revela:** os campos 2, 3 e 4 têm **guard periódico
desde 19/07** — um `.path` que acorda quando o `userdata` muda e um `.timer` a
cada 30 minutos. O campo 1, que é o que quebrou, **nunca teve nenhum**. Um
`localconfig.vdf` que muda dispara o guard, o guard roda
`disable_steam_input.sh --apply-quiet`, e o `LaunchOptions` não é olhado.

> **A cura mais barata deste documento inteiro** é fazer o guard que já existe,
> já está instalado e já roda a cada 30 minutos, olhar também o campo 1. Não é
> unidade nova nem timer novo: é uma linha a mais no `ExecStart`. Fica **aberta**
> aqui porque `assets/` não era o território desta frente — e porque, sem a cura
> da seção 3, ela repararia com a régua errada.

---

## 2. Os buracos, um a um

### 2.1 O portão que contava — e o teste que o nome fez parecer culpado

O `check_launch_wrapper` do `doctor.sh` contava ocorrências do caminho do wrapper
no vdf e dizia *"60 jogo(s) com o wrapper aplicado"*. Com o Pragmata quebrado, ele
diz **60**, e passa em verde. Contar responde *"quantos?"*; ninguém nunca precisou
saber quantos. Curado às 04h desta madrugada.

**E o `WRAPPER-EM-TODOS-01`, deveria ter pego?** **Não** — e isso importa dizer,
porque o nome acusa. `tests/unit/test_wrapper_em_todos_cobertura.py` não olha vdf
nenhum: ele testa `compose_env`, isto é, se o `SDL_GAMECONTROLLER_IGNORE_DEVICES`
sai quando há **um vpad vivo por DualSense físico**. É um bom teste do que testa.
O nome é que promete outra coisa — *"wrapper em todos [os jogos]"* quando o
assunto é *"o IGNORE cobre todos [os físicos]"*. E o defeito de ontem estava
**fora** do alcance dele por construção: sem o wrapper rodando, a env que o
`compose_env` monta com perfeição **nunca é lida por ninguém**.

> A lição não é "o teste falhou". É que **um nome que promete cobertura maior que
> a real produz o mesmo conforto falso que um contador** — e mais barato, porque
> não precisa nem rodar.

### 2.2 O portão que contava, segunda ocorrência — e o defeito que ele escondeu por 24 dias

`check_steam_input_allowlist` (doctor, desde 23/07) dizia
*"allowlist do Steam Input com 1/1 appid(s) sem `.env` materializado"*. Nunca dizia
qual.

Ao trocar o contador por nomes, o defeito apareceu **na primeira execução**: a
extração dos appids era

```sh
sed 's/#.*$//' "${arquivo}" | tr -d '[:space:]' | grep -E '^[0-9]+$'
```

e `tr -d '[:space:]'` apaga **também as quebras de linha**, sobre o fluxo inteiro.
A allowlist de três appids virava **um** appid de 21 dígitos —
`211119033576501599660` — que obviamente nunca tem `.env`. O check nunca examinou
jogo nenhum. **MEDIDO**, e curado nesta leva.

> Vinte e quatro dias. `1/1` é plausível, e ninguém desconfia de um número. O
> appid-monstro, escrito por extenso, se denuncia em um segundo. **É o argumento
> mais forte deste documento a favor de nomear:** a contagem não só esconde o
> defeito do produto, ela esconde o defeito **do próprio portão**.

### 2.3 A allowlist do Steam Input só PRESERVA — ela nunca LIGA

**MEDIDO.** `add_appid_to_steam_input_allowlist` escreve uma linha no nosso
`.txt` e **nada mais**. A única coisa que o arquivo faz é impedir o
`disable_steam_input.sh` de zerar um `UseSteamControllerConfig` que **já estava**
em `1|2`.

Consequência: se o guard passou por aquele jogo **antes** de ele entrar na lista,
o valor já foi a zero — e não volta sozinho nunca mais. A entrada fica na lista
para sempre, inerte, e a casa acha que cumpriu o pedido dela.

No vdf dela, agora: **Sackboy: A Big Adventure (1599660) está na allowlist com
`UseSteamControllerConfig "0"`**, e o comentário na própria allowlist diz
*"marcado no editor de perfil"* — ela pediu, e não aconteceu.

Curado do lado do diagnóstico (o doctor passa a nomear o jogo e a explicar o que
fazer). **Fica aberto** do lado do produto: ou o clique passa a **ligar** o
Steam Input no vdf, ou a interface precisa dizer que ligar é com ela, na Steam.
É decisão dela, não minha — o preço de escolher errado é o produto escrever em
mais um campo que a Steam manda de volta.

### 2.4 O `SwitchSupport` que o script não consegue escrever

**MEDIDO:** a chave `SteamController_SwitchSupport` **não existe** no
`localconfig.vdf` dela. **MEDIDO (leitura do awk):** `_transform_vdf` só faz
`gsub` sobre a linha existente — ele **reescreve, nunca insere**.

Logo: enquanto a Steam não escrever a chave (o que ela só faz quando alguém mexe
naquela opção), a cura do Switch/8BitDo **não roda**, e o que vale é o default da
Steam. **SEM PROVA:** qual é esse default. Medir é abrir a Steam com um controle
Switch na mesa e ler a chave depois — trabalho de dez minutos, que ninguém fez.

### 2.5 O que NÃO é buraco, e por que fica escrito

O `--status` do `disable_steam_input.sh` **imprime contagens** por vdf, o que a
esta altura do documento parece a mesma cegueira. Não é: quem decide o veredito é
`needs_real_fix`, que aplica a transformação num temporário e compara — ou seja,
ele pergunta *"a edição mudaria alguma coisa?"* em vez de *"quantas linhas
casam?"*. Com dois jogos da allowlist em `2`, ele responde **"tudo limpo"**, e
está certo. **É o molde de como se conta sem cegar**, e vale copiar.

---

## 3. O achado central: o censo lê a própria sujeira de volta

Este é o defeito que vale mais que todos os acima juntos, e ele é **da noite de
hoje** — nasceu junto com a cura.

### 3.1 O `localconfig.vdf` tem TRÊS árvores chamadas `apps`

**MEDIDO** às 05h07 de 16/08, no arquivo dela:

| Caminho | linhas de `LaunchOptions` |
|---|---|
| `UserLocalConfigStore/Software/Valve/Steam/apps/<appid>` | **63** |
| `UserLocalConfigStore/apps/<appid>` | 11 |
| `UserLocalConfigStore/WebStorage/apps/<appid>` | 3 |

A primeira é a viva — a que a Steam lê e escreve. Isso não é palpite: quando ela
digitou `VKD3D_CONFIG=no_upload_hvv %command%` nas Opções de Inicialização do
Pragmata pela janela da Steam, **foi a primeira que mudou, e só ela**. As outras
duas seguem com a linha antiga até agora.

A segunda árvore é a das configurações de controle: é lá que moram
`UseSteamControllerConfig`, `SteamControllerRumble` e `SteamControllerRumbleIntensity`
(os 11 blocos batem exatamente com os 11 jogos cujo painel de controle ela abriu).
**A âncora certa depende da chave** — `LaunchOptions` numa árvore,
`UseSteamControllerConfig` na outra.

### 3.2 As duas árvores extras foram escritas por NÓS

**RECONSTRUÍDO com precisão de minuto**, dos backups `.bak.hefesto-launch-*` que o
próprio produto deixou ao lado do vdf:

| backup | canônica | `UserLocalConfigStore/apps` | `WebStorage/apps` |
|---|---|---|---|
| 13/06 13:36 (antes do Hefesto) | 2 | 0 | 0 |
| 16/07 22:39 | 4 | 0 | 0 |
| 21/07 20:20 | 6 | 0 | 0 |
| **21/07 20:26 — a primeira aplicação em massa** | **55** | **9** | **2** |
| 16/08 05:03 (agora) | 63 | 11 | 3 |

Antes da primeira aplicação em massa **não havia uma única** `LaunchOptions` fora
da árvore viva. Elas nascem no mesmo minuto em que a canônica salta de 6 para 55.

O mecanismo, lido no fonte: tanto `read_apps_by_appid` quanto
`apply_wrapper_vdf_text` decidem se um bloco é um jogo com

```python
stack[-1].isdigit() and stack[-2].lower() == "apps"
```

— o **nome do pai**, nunca o caminho inteiro. Qualquer bloco numérico dentro de
qualquer coisa chamada `apps` entra. O escritor então **insere** uma linha
`LaunchOptions` em blocos que a Steam usa para outra finalidade.

Reproduzido numa fixture nesta sessão: um vdf com um único jogo `111` presente nas
duas árvores devolve `applied` com **o appid 111 duas vezes**, e a segunda escrita
cai no bloco de configuração de controle.

### 3.3 O estrago não é a linha a mais — é que o censo a lê de volta

`read_apps_by_appid` funde as três árvores num dicionário só, por appid, e faz
`out[appid] = valor`: **a última leitura vence**, e a última é a secundária.

**MEDIDO, agora, na máquina dela:**

```
$ python3 …/sentinela_do_wrapper.py --censo
com_wrapper: 64   faltantes: []   erros: []
3357650 em com_wrapper?  True
```

e, no mesmo arquivo, no mesmo segundo:

```
UserLocalConfigStore/Software/Valve/Steam/apps/3357650
    "LaunchOptions"    "VKD3D_CONFIG=no_upload_hvv %command%"
```

> **O Pragmata continua quebrado neste instante**, depois de a sentinela ter sido
> entregue às 04h e de um reparo ter rodado às 04h07 — e a sentinela jura que está
> tudo certo, porque está lendo de volta a linha que **nós mesmos** escrevemos numa
> árvore que a Steam nunca abre.

É a armadilha nº 1 do `COMO-OLHAR-A-TELA.md`, na sua forma mais pura: *o
instrumento mente mais que o produto*. E mente **para o lado do conforto**, que é
o pior lado.

Há ainda um segundo sintoma da mesma causa, menor e igualmente medido: o appid
**413080** tem `LaunchOptions` **só** nas árvores secundárias — não existe na
viva. O produto escreveu uma linha de lançamento para um jogo que a Steam nunca
vai lançar com ela, e o censo conta esse jogo como coberto.

### 3.4 A régua independente, e a mordida que prova que ela morde

A cura da fusão é do dono de `steam_launch_options.py` (o arquivo está em edição
por outra frente nesta mesma leva). O que entrou **agora** é uma segunda régua, no
doctor, que **não importa o parser sob suspeita**: ela reimplementa a pilha de
blocos em vinte linhas e exige o **caminho inteiro**
(`check_arvore_canonica_do_wrapper`). Só o nome do jogo vem emprestado, e vem dos
`.acf`, não do vdf.

Com a âncora de caminho:

```
total=63
sem=PRAGMATA (appid 3357650)
orfaos=appid 413080
```

Com a âncora **arrancada** — trocada pelo mesmo `pilha[-2] == "apps"` do censo:

```
total=64
sem=
orfaos=
```

Verde, e a resposta exata que a sentinela dá hoje. **A cura é a âncora, e ela
carrega o veredito inteiro.**

Na tela dela, as duas réguas passam a aparecer uma embaixo da outra, discordando —
que é exatamente o que se quer que apareça:

```
[ OK ] nenhum jogo perdeu as Opções de Inicialização do Hefesto
[FAIL] na árvore que a Steam de fato lê (Software/Valve/Steam/apps),
       ESTE(S) jogo(s) NÃO chamam o wrapper: PRAGMATA (appid 3357650) — …
```

---

## 4. O reparo no install, e o ciclo que o prova

O passo `11b-ter` rodava `--relatorio`, que só **anota**. Anotar um defeito e
deixá-lo em pé é o defeito mais caro desta casa. Agora ele roda `--reparar`, sem
flag — e o precedente estava trinta linhas abaixo no mesmo arquivo: o `11c` nunca
"relatou" o Proton fora do pin, ele roda `--ensure` e `--lock`.

O que o reparo garante, **medido em fixture** (a Steam dela não foi tocada):

| passo | resultado |
|---|---|
| install | `reparado`; o `VKD3D_CONFIG` dela **preservado** ao lado do wrapper |
| install de novo | `nada_a_fazer` — idempotente |
| Steam ou jogo aberto | `adiado_*`, rc=3, **nada é escrito**; o install avisa com o comando na mão e **não falha** |
| `uninstall --strip` | tira o wrapper das três árvores; o `VKD3D_CONFIG` dela sobrevive |
| install seguinte | motivo `novo`, **nunca** `regressao`; wrapper de volta, `VKD3D_CONFIG` intacto |

A última linha só é verdade porque o uninstall apaga o `wrapper-visto.json`.
**A mordida, rodada:** mantendo o registro através do `--strip`, o install seguinte
anuncia *"2 jogos perderam as Opções de Inicialização do Hefesto"* — um alarme de
regressão sobre a remoção que ela mesma pediu. A linha do uninstall é
carga, não enfeite.

E o que o reparo **não** alcança, dito no próprio comentário do passo: enquanto a
fusão das árvores existir, o censo responde "nada a fazer" para o Pragmata e o
reparo passa batido. Quem nomeia o jogo é o doctor no fim do install.

---

## 5. O que ficou aberto, com dono e preço

| # | O quê | Dono | Preço de não fazer |
|---|---|---|---|
| A | **Ancorar o caminho** em `read_apps_by_appid` e `apply_wrapper_vdf_text` (`UserLocalConfigStore/Software/Valve/Steam/apps`), e **limpar** as linhas que já escrevemos nas duas árvores secundárias | dono de `steam_launch_options.py` | O censo, o reparo, a GUI e o install continuam todos cegos ao mesmo tempo — e continuam **concordando entre si**, que é o que faz o defeito durar |
| B | Fazer o `hefesto-steam-input-guard` (que já roda a cada 30 min) olhar também o `LaunchOptions` | `assets/` + `install.sh` | Entre um install e o seguinte, qualquer variável nova apaga o wrapper e ninguém nota até um jogo abrir sem controle. **Depende de A**, ou o guard reparará com a régua errada |
| C | Decidir se marcar um jogo na allowlist deve **ligar** o `UseSteamControllerConfig` na Steam | **dela** | Pedido dela que não acontece, silenciosamente (o Sackboy, hoje) |
| D | Medir o default do `SteamController_SwitchSupport` com a chave ausente | quem tiver um 8BitDo na mesa | A cura do Switch pode nunca ter rodado em máquina nenhuma |
| E | Medir se `SteamControllerRumble`/`RumbleIntensity` disputam com o nosso caminho de vibração | frente do rumble | Um sintoma de rumble com causa fora do nosso código, procurado dentro dele |

---

## 6. A regra que este documento pede que a casa adote

Três defeitos independentes desta noite têm a mesma forma, e nenhum deles é sobre
a Steam:

1. o contador do wrapper dizia **60** e não dizia **Pragmata**;
2. o check da allowlist dizia **1/1** e escondeu, por 24 dias, que estava lendo um
   appid de 21 dígitos;
3. o censo dizia **64 com wrapper** somando árvores que a Steam não lê.

> **Portão que responde "quantos" está cego. Portão tem de responder "qual".**
>
> E, quando o portão lê algo que o próprio produto escreveu: **ele tem de dizer de
> qual lugar leu.** Um instrumento sem endereço não é instrumento — é eco.

---

## 7. Onde está cada coisa

- `scripts/doctor.sh` — `check_arvore_canonica_do_wrapper` (régua independente,
  ancorada no caminho), `check_steam_input_allowlist` (nomeia, cruza com o vdf, e
  perdeu o `[FAIL]` caduco), `_rotulo_do_appid`, `_steam_input_do_appid`
- `install.sh` — passo `11b-ter`, agora `--reparar`
- `uninstall.sh` — remoção do `wrapper-visto.json` (já existia; a mordida está na
  seção 4)
- `src/hefesto_dualsense4unix/integrations/sentinela_do_wrapper.py` — a sentinela,
  **não tocada** por esta frente
- `docs/process/sprints/2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md`
  — a sprint do defeito de ontem
