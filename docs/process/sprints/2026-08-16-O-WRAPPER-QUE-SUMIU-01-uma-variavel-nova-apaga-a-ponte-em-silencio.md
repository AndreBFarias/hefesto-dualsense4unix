# O WRAPPER QUE SUMIU-01 — uma variável nova apaga a ponte, em silêncio

- **Escrito em:** 16/08/2026, ~03h40, com o defeito pego ao vivo às 02h30 dela.
- **Estado:** **diagnóstico FECHADO, cura NÃO ESCRITA.** Nenhuma linha de código
  foi tocada por esta sprint — o produto dela é a página. As entregas da seção 9
  estão propostas, não construídas.
- **Grau:** a cadeia é **MEDIDA** (arquivo por arquivo, nesta máquina, nesta
  madrugada); o **cabo × rádio** é o único pedaço que continua **SEM PROVA**, e
  está dito assim na seção 6.
- **Faixa:** 1 — o pior caso é *"o jogo não vê controle nenhum"*, que é
  exatamente o que aconteceu.
- **A palavra final na tela é dela**
  ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).

---

## 1. O sintoma, na voz dela — é assim que ele volta

> *"no inicio travou alguns inputs mas logo em sequencia ele parou de ser
> reconhecido no jogo, mas o perfil de pragmata segue ativo no controle com tudo
> funcionando só não sendo reconhecido. não alterei nada nada na steam."*

Traduzido para o que a próxima pessoa vai ver na mesa:

| o que se observa | o que a cabeça conclui (errado) |
|---|---|
| funcionou no **cabo**, quebrou no **rádio** | "é o Bluetooth" |
| o **controle continua vivo** — luz, gatilhos, perfil | "o daemon está bom, então não é nosso" |
| o **perfil do jogo segue ativo**, trocando sozinho | "a detecção de jogo funciona, logo o jogo abriu certo" |
| **só o jogo** não enxerga | "é o jogo / é a Steam / é o Proton" |
| *"não alterei nada na Steam"* | "então a Steam não mudou" |

**As cinco leituras estão erradas pelo mesmo motivo:** todas olham para o lado
vivo. O que quebrou foi uma **linha de texto num arquivo de configuração** que
ninguém abriu, e que continuou errada enquanto tudo o mais funcionava.

Eu caí em todas. Passei pelo daemon, pelo `EVIOCGRAB` e pelo `launch_env`
inteiro antes de olhar a única linha que importava.

---

## 2. O diagnóstico de trinta segundos

Antes de qualquer outra coisa, **um `cat`**:

```bash
cat ~/.local/state/hefesto-dualsense4unix/launch_env/last_run
```

Nesta máquina, com ela jogando Pragmata (appid `3357650`), o arquivo dizia:

```
appid=2542020
epoch=1786822035
pid=866606
```

- `2542020` é **Duskfade**, não Pragmata;
- `1786822035` é **15/08/2026 16:27:15** — horas antes da sessão dela;
- `866606` é um pid **morto**.

Quem grava esse arquivo é o **próprio wrapper**, em
`assets/hefesto-launch.sh:97` (`record_last_run`), **antes** do `exec`. Se o
appid ali não é o do jogo que acabou de abrir, a conclusão é única e não admite
discussão:

> **O `hefesto-launch` NÃO RODOU para este jogo.**

Tudo o que vem depois é consequência disso. **Este `cat` é a primeira coisa a
fazer** quando um jogo não enxerga o controle — vem antes do journal, antes do
`--status`, antes de olhar o daemon.

---

## 3. A cadeia completa, com endereços

### 3.1 O elo quebrado: uma linha de texto no `localconfig.vdf`

A Steam guarda as opções de inicialização em

```
~/.steam/steam/userdata/<steamid>/config/localconfig.vdf
    → Software/Valve/Steam/apps/<appid>/LaunchOptions
```

*(nesta máquina o `.steam/steam` é symlink para `.steam/debian-installation`; o
`discover_vdfs` já deduplica — `integrations/steam_launch_options.py:293`.)*

Às 02h30, o campo do Pragmata era:

```
VKD3D_CONFIG=no_upload_hvv %command%
```

E o dos outros sessenta jogos era o nosso:

```
sh -c 'W="$HOME/.local/share/hefesto-dualsense4unix/bin/hefesto-launch"; \
[ -x "$W" ] && exec "$W" "$@"; exec env "$@"' hefesto-launch %command%
```

**A Steam guarda UMA linha por jogo.** Não há lista, não há merge, não há
histórico. Quem escreve por último apaga quem escreveu antes, sem aviso — o
campo aceita qualquer texto e a Steam não valida nada.

### 3.2 O `launch_env` materializado, e nunca lido

O daemon fez a parte dele, e fez certo. Está no disco, com carimbo:

```
~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_3357650.env
```

```
# estado: perfil gamepad dualsense (prognóstico uhid) | ... | 2026-08-16T03:33:50
PROTON_DISABLE_HIDRAW=0x054C/0x0CE6
SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6,0x28de/0x11ff
__GL_SHADER_DISK_CACHE=1
__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1
SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0
```

Repare no que **não** está nessa lista: `0x054c/0x0df2`. A nossa lista **nunca**
esconde o nosso próprio vpad — está escrito como lei em
`daemon/launch_env.py`: *"o vpad Edge 0df2 PRECISA do hidraw … NUNCA incluir
0x0DF2"*.

O arquivo existia, estava correto, e **ninguém o leu**. Quem lê é o wrapper.
Wrapper que não roda = arquivo que é lixo.

### 3.3 O que chegou ao jogo, no lugar do nosso

Medido no `/proc` do processo vivo do jogo, às 02h30:

1. **`PROTON_DISABLE_HIDRAW` — ZERO ocorrências.** Só o Hefesto escreve essa
   variável nesta máquina. Ausência dela é prova negativa de que o wrapper não
   rodou (é a segunda confirmação independente do `last_run`);
2. o `SDL_GAMECONTROLLER_IGNORE_DEVICES` que chegou ao jogo **não era o nosso** —
   era a lista da própria pilha da Steam, com centenas de pares;
3. e dentro dela estava **`0x054c/0x0df2`** — o PID do **nosso vpad**. Somado ao
   `0x054c/0x0ce6` (o DualSense físico), que também estava lá, **o jogo foi
   instruído a ignorar os dois**;
4. resultado no censo de descritores: `event21` (o vpad) — **ninguém abriu**;
   `event25` (o físico) — a Steam abriu para si. **O jogo ficou sem nenhum.**

**Corroboração independente, no nosso próprio código:** o `daemon/launch_env.py`
já documenta uma lista de terceiros com esse exato conteúdo — o contorno do God
of War Ragnarok que o **Proton** escreve em `proton:1828`:

```
0x054C/0x05C4,0x054C/0x09CC,0x054C/0x0BA0,0x054C/0x0CE6,0x054C/0x0DF2
```

O `0x0DF2` está lá. Ou seja: **existem pelo menos duas listas de terceiros, fora
do nosso controle, que mandam ignorar o vpad do Hefesto** — a da Steam e a do
Proton. Quando o wrapper roda, ele sobrescreve a variável e o nosso valor vence.
Quando não roda, o valor deles é o único que existe.

### 3.4 A cadeia, em uma linha

> alguém reescreveu o `LaunchOptions` → o `hefesto-launch` não rodou → o
> `.env` materializado nunca foi lido → o jogo herdou a lista de terceiros →
> a lista de terceiros contém `0x0df2` → o jogo ignorou o vpad **e** o físico →
> zero controles.

O daemon esteve **saudável do começo ao fim**: vpad P1 com os quatro nós, grab
retido (`gamepad_controller_grab grab=True ok=True state=held`), `.env`
materializado no horário certo, com o conteúdo certo. **Nada nele estava errado,
e é por isso que investigá-lo custou a noite.**

---

## 4. Quem reescreveu o campo — e a premissa que a medição corrigiu

A hipótese com que esta sessão começou era: *"o `VKD3D_CONFIG` foi posto para
curar o crash de VRAM de 14/08, e substituiu o wrapper"*. A hipótese está
**certa no mecanismo e errada no autor e na data**. Os backups por execução que o
nosso próprio `--apply` deixa ao lado do vdf (`localconfig.vdf.bak.hefesto-launch-<ts>`,
trinta e um arquivos, de 16/07 a 15/08) permitem reconstruir a linha do tempo:

| data | Pragmata (`3357650`) |
|---|---|
| 16/07 22:39 | `VKD3D_CONFIG=no_upload_hvv %command%` — **anterior ao Hefesto** |
| 21/07 20:20 | idem |
| **21/07 20:26** | o primeiro `--apply` em massa (56 jogos) — **wrapper, sem o VKD3D** |
| 22/07 … 15/08 16:26 | wrapper, em **todas** as trinta e uma amostras |
| ~15/08, noite | **volta a `VKD3D_CONFIG=no_upload_hvv %command%`** — o defeito |
| 16/08 03:33 | wrapper de novo (a Steam gravou; ver seção 10) |

Ou seja: o `VKD3D_CONFIG` **não é** a cura de 14/08 recém-colada. Ele é uma
receita **de julho**, que voltou sozinha vinte e cinco dias depois.

### O segundo escritor, e ele mora na casa dela

```
~/.config/zsh/scripts/aurora-steam-launchopts.conf
```

```
3357650	VKD3D_CONFIG=no_upload_hvv %command%
```

Essa tabela é lida pelo `aurora-steam-launchopts.sh` → `aurora-steam-launchopts.py`, <!-- ref-externa: moram em ~/.config/zsh/scripts/ (a casa dela), fora deste repositório — é justamente o ponto do parágrafo -->
e o motor **substitui o valor inteiro** (`edits.append((b["lo"], 'r', …desired…))`) —
não prefixa, não preserva, não sabe que o wrapper existe. E é chamado pelo
`ritual-aurora-self-heal.sh:1959`, cujo timer é: <!-- ref-externa: ~/.config/zsh/scripts/, fora deste repositório -->

```
ritual-aurora-self-heal.timer — 2min pós-boot e A CADA 1 HORA
```

**Portanto:** de hora em hora, sempre que a Steam está fechada, um processo em
segundo plano reescreve o `LaunchOptions` do Pragmata e apaga a nossa ponte.
Cada escritor é idempotente sozinho; **os dois juntos não são idempotentes
coisa nenhuma** — são um pêndulo, e quem escreveu por último antes do jogo abrir
decide se a noite dela funciona.

Isto é a causa raiz de verdade, e ela é melhor que a hipótese original em três
sentidos: explica **por que só o Pragmata** (é o único appid da tabela), explica
**por que voltou sozinho** (timer horário) e explica **por que ela disse a
verdade** ao afirmar *"não alterei nada nada na steam"* — ela não alterou. Um
timer alterou.

---

## 5. O censo, e o que fazer quando o número mudar

Às 02h30: **60 com o wrapper, 1 sem** — e o único sem era o Pragmata.

Refeito às 03h40, com o comando abaixo (somente leitura, seguro com a Steam
aberta):

```bash
python3 - <<'EOF'
import sys; sys.path.insert(0, "src")
from hefesto_dualsense4unix.integrations import steam_launch_options as s
for v in s.discover_vdfs():
    d = s.read_launch_options_by_appid(v.read_text(encoding="utf-8", errors="replace"))
    com = [a for a, val in d.items() if s.WRAPPER_PREFIX in val]
    print(v, f"{len(com)}/{len(d)} com wrapper")
    for a, val in d.items():
        if s.WRAPPER_PREFIX not in val:
            print("   SEM ->", a, s.rotulo_do_jogo(a), repr(val)[:120])
EOF
```

Resultado às 03h40: **64/64**. O número mudou enquanto eu escrevia esta página —
o que é, por si só, a demonstração de que **este número é volátil e ninguém o
vigia**.

**O que fazer quando ele mudar:**

- **denominador menor que o esperado** (jogos novos sem linha `LaunchOptions`):
  normal — a Steam só cria a chave quando alguém digita algo. O `apply` insere a
  linha; o `appid_needs_wrapper` (`steam_launch_options.py:550`) já trata "sem
  entrada" como *precisa*;
- **numerador menor que o denominador:** **isto é o defeito desta sprint.** Rode
  o censo acima, olhe o valor da linha que sobrou e **procure quem o escreveu** —
  a pergunta certa não é *"por que falta o wrapper"*, é *"que ferramenta escreve
  exatamente esse texto"*. Nesta máquina a resposta estava a um `grep` de
  distância: `grep -rn "<o texto>" ~/.config`;
- **numerador zero:** o `--apply` nunca rodou, ou o `uninstall` passou. Caso
  conhecido, e o doctor já grita.

---

## 6. Por que funcionou no cabo — e a parte honesta

Esta é a pergunta que mais confunde, e a resposta tem duas metades: uma
**medida**, que derruba a explicação fácil, e uma **em aberto**.

### A metade medida: o wrapper faltou nos DOIS transportes

O `LaunchOptions` é **um campo por jogo, sem noção de transporte**. Ele estava
quebrado quando ela jogou no cabo **e** quando ela passou para o rádio — foi o
mesmo texto o tempo todo. E o `daemon/launch_env.py` **não tem uma única
referência a cabo, rádio, USB ou Bluetooth**: `compose_env` decide por modo
nativo, emulação, máscara, backends e cobertura — nunca por transporte. As envs
que o wrapper exportaria seriam **byte a byte idênticas** nos dois casos.

**Consequência dura, e é ela que fecha a pergunta:** a diferença cabo × rádio
**não pode** ter vindo do wrapper, porque o wrapper esteve ausente dos dois
lados. Repor o wrapper conserta o defeito desta sprint — **e não explica, nem
promete consertar, a assimetria de transporte.** São dois assuntos.

### A metade em aberto: então o que difere?

Com o wrapper fora, o que chega ao jogo é o ambiente da Steam sozinho, e o que
sobra de diferente entre os dois transportes está **fora** do nosso alcance:

1. **quem já segurava o aparelho.** No censo do momento da falha, o `event25`
   (físico) estava aberto **pela Steam** e o `event21` (vpad) estava fechado por
   todos. O caminho `hidraw`/`hidapi` do SDL para o DualSense **não é o mesmo
   código** do caminho `evdev`, e a exclusividade que cada um exige difere;
2. **a nossa própria disputa.** O `EVIOCGRAB` do daemon sobre o físico e o
   momento em que a Steam abre o dispositivo têm ordens de chegada diferentes
   quando o aparelho aparece por USB (no boot, junto com tudo) e quando ele
   aparece por rádio (no meio da sessão, com a Steam já viva).

**Grau: SUSPEITA, sem mecanismo isolado.** Nenhuma das duas foi medida. **O
ensaio que decide** — e ele é barato, dura quatro minutos e não exige código:

> Com o wrapper **reposto e conferido** (`last_run` mostrando o appid certo),
> abrir o mesmo jogo duas vezes — uma no cabo, uma no rádio — e capturar, nos
> dois casos: `tr '\0' '\n' < /proc/<pid>/environ | grep -E 'SDL_GAMECONTROLLER|HIDRAW'`
> e o censo de quem tem cada `/dev/input/event*` aberto. Se o jogo enxergar nos
> dois, a assimetria **era** o wrapper e esta seção se apaga com data. Se não,
> a assimetria é real, e aí sim ela merece sprint própria.

**Enquanto esse ensaio não for feito, ninguém pode escrever "o wrapper conserta
o Bluetooth".** É exatamente o tipo de frase que a próxima pessoa herdaria como
fato.

---

## 7. A classe do defeito: campo único, escritor único, silêncio

Este caso é uma instância. A classe é maior:

> **Qualquer configuração que a Steam guarde num campo de valor único pode ser
> apagada em silêncio por qualquer outro escritor — nosso, dela, ou de
> terceiros. Escrever não é possuir.**

O `localconfig.vdf` tem pelo menos quatro campos assim que nos interessam. O
quadro abaixo é o resultado do levantamento pedido, medido no código:

| campo | o produto **escreve**? | o produto **lê**? | o produto **vigia**? |
|---|---|---|---|
| `SteamController_PSSupport` | sim — `scripts/disable_steam_input.sh`, global, `→ "0"` | sim (`--status`) | **SIM** — `hefesto-steam-input-guard.path` + `.timer` (30 min) |
| `SteamController_SwitchSupport` | sim — mesmo script, mesmo tratamento (Onda R, 19/07) | sim | **SIM** — mesmo guard |
| `UseSteamControllerConfig` | sim — `→ "0"`, **exceto** appids da allowlist (`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`) | sim | **SIM** — mesmo guard |
| **`LaunchOptions`** | sim — `install.sh:2823` (11b, migra) e `install.sh:2869` (11b-bis, aplica a todos), mais o botão da GUI | sim — `appid_needs_wrapper` (diálogo) e a contagem do doctor | **NÃO — e é o buraco desta sprint** |

**A casa já resolveu este problema exato, para os três primeiros campos.** O
guard instalado por default, sem flag, em `install.sh:2791-2805`, tem
precisamente o contrato que falta ao quarto:

- roda a cada 30 min **e** ao mudar o diretório `userdata`;
- usa `--apply-quiet`, que **nunca fecha a Steam**: se ela está viva, **adia**;
- é `--user`, sem `sudo`, e entra sozinho no install.

Isto é o padrão *"a casa sabe e o produto não faz"* na sua forma mais cara: a
cura está escrita, testada e instalada — para o vizinho de linha. Ninguém a
estendeu para o campo que quebra o jogo inteiro.

**Uma ressalva de desenho, e ela é séria:** um guard de `LaunchOptions` **não
pode** reafirmar cegamente como o do PSSupport. Se ele sobrescrever, ele e o
`aurora-steam-launchopts.py` viram dois pêndulos de 30 e 60 minutos brigando <!-- ref-externa: ~/.config/zsh/scripts/, fora deste repositório -->
pelo mesmo campo. Ele tem de **mesclar** — que é o que o `migrate_value`
(`steam_launch_options.py:226`) já faz e já tem teste: ele **prefixa** o
`WRAPPER_PREFIX` preservando as opções da usuária byte a byte. Com merge, o
resultado convergente é

```
sh -c '…' hefesto-launch VKD3D_CONFIG=no_upload_hvv %command%
```

— que satisfaz os **dois** escritores ao mesmo tempo. Sem merge, é guerra.

**Nota de higiene, achada de passagem:** as três units do guard apontam, no
comentário, para `docs/process/sprints/FEAT-STEAM-INPUT-SELF-HEAL-01.md`, que <!-- ref-externa: a AUSÊNCIA deste arquivo é o assunto da frase -->
**não existe** nesta árvore. Ponteiro morto em arquivo que é instalado na
máquina dela.

---

## 8. O portão que passou verde — e deveria ter pego

**Sim, deveria.** E o modo como ele falhou é pior que não existir.

### 8.1 Onde ele está

O portão de cobertura do wrapper é o `check_launch_wrapper`, em
`scripts/doctor.sh:1470`. O trecho que conta (linhas 1505-1520):

```bash
n_wrapper=$((n_wrapper + $(grep -o '.local/share/…/hefesto-launch' "${vdf}" | wc -l)))
…
if [[ "${n_wrapper}" -gt 0 ]]; then
    pass "${n_wrapper} jogo(s) com o wrapper hefesto-launch aplicado nas LaunchOptions"
else
    warn "NENHUM jogo com o wrapper nas LaunchOptions — …"
fi
```

### 8.2 Por que passou verde a noite toda

**Porque o portão não tem denominador.** O predicado é `n_wrapper > 0`. Com
sessenta jogos cobertos e um descoberto, ele imprimiu:

```
[ OK ] 60 jogo(s) com o wrapper hefesto-launch aplicado nas LaunchOptions
```

— um **`[ OK ]` verde exibindo o próprio número que era a prova do defeito**. Faltava
uma comparação: 60 **de** 61. O mesmo vale para o `--status` do CLI
(`steam_launch_options.py:1217`), que imprime `chamadas do wrapper: N` e nunca
diz *de quantos*.

**Reproduzido, não deduzido.** Um vdf sintético de dois apps — um com o wrapper,
um com `VKD3D_CONFIG=no_upload_hvv %command%` — submetido ao predicado **exato**
do `doctor.sh` (o mesmo `grep -o … | wc -l` das linhas 1505-1515):

```
predicado do doctor.sh:1515  ->  n_wrapper=1 > 0 ?
  VEREDITO: pass  "1 jogo(s) com o wrapper hefesto-launch aplicado nas LaunchOptions"
denominador que o portão NÃO olha: 2 apps com LaunchOptions  ->  cobertura real 1/2
```

**Grau: MEDIDO.** O portão dá `pass` sobre um vdf com metade dos jogos
quebrados, e imprime o numerador como se fosse boa notícia. É esta noite, em
duas linhas de vdf.

Um portão que só distingue "zero" de "não-zero" é cego a **toda** regressão
parcial — e regressão parcial é a única forma que este defeito tem de aparecer,
porque nenhum escritor apaga sessenta e um campos de uma vez. Cada escritor
apaga **um**.

### 8.3 A armadilha de nome, que fez eu procurar no lugar errado

Há **duas coisas diferentes chamadas "cobertura"** neste repositório, e a sprint
que tem o nome certo protege a errada:

| nome | o que é | onde |
|---|---|---|
| cobertura do **WRAPPER-EM-TODOS-01** | *"existe um vpad vivo para cada DualSense físico na mesa?"* | `daemon/launch_env.py:913` `cobertura_total`, testado em `tests/unit/test_wrapper_em_todos_cobertura.py` |
| cobertura **desta sprint** | *"existe a chamada do wrapper em cada jogo da Steam?"* | **em lugar nenhum** |

A [WRAPPER-EM-TODOS-01](2026-08-03-WRAPPER-EM-TODOS-01-a-invariante-duplicado-melhor-que-zero-com-quatro.md)
está **verde e correta** — ela nunca prometeu vigiar o campo do vdf, e não
falhou em nada. O que a derrubou foi eu ler o nome dela e assumir que o assunto
estava coberto. **Nomes iguais para invariantes diferentes é dívida de portão**,
e vale registrar em separado.

### 8.4 O veredito

**Isto é um buraco de portão, e vale mais que a cura em si.** Um guard que repõe
o wrapper conserta esta noite. Um portão com denominador impede que a próxima
noite exista — inclusive para escritores que ainda não foram inventados, que é a
única defesa que sobrevive ao tempo.

---

## 9. As entregas — propostas, nenhuma construída

### E1 — o portão ganha denominador (a mais barata e a mais valiosa)

`check_launch_wrapper` passa a contar **os dois lados** e reprova em desacordo:

- `n_wrapper` (hoje) **e** `n_apps_com_LaunchOptions` (novo, o denominador);
- `n_wrapper == n_apps` → `pass "N/N"`;
- `0 < n_wrapper < n_apps` → **`fail`**, listando **appid e valor** de cada
  jogo descoberto (é o valor que aponta o culpado, como apontou aqui);
- `n_wrapper == 0` → o `warn` de hoje, intacto.

O mesmo denominador entra no `_report_status` (`steam_launch_options.py:1217`).

**A mordida:** um vdf sintético com dois apps, um com wrapper e um com
`VKD3D_CONFIG=no_upload_hvv %command%` → asserção de **reprovação** com o appid
descoberto na mensagem. *Arranque o denominador, deixe `n_wrapper > 0`, e veja
o teste passar verde sobre o vdf quebrado — é literalmente esta noite,
reproduzida em quatro linhas.*

**Por que é raiz:** o defeito não é a ausência do wrapper; é **a ausência não
ter sido notada por doze horas**.

### E2 — o guard de `LaunchOptions`, por MERGE, adiando com a Steam viva

Espelho exato do `hefesto-steam-input-guard`, que já existe e já funciona:

- `hefesto-launch-options-guard.path` (vigia `userdata`) + `.timer`;
- executa um `--apply-quiet` novo, que **usa `migrate_value`** (prefixa,
  preserva) e **nunca fecha a Steam** — Steam viva ⇒ **adia**, `rc=0`,
  mensagem clara;
- entra no `install.sh` **por default, sem flag**, ao lado do guard irmão;
- `uninstall` simétrico.

**A mordida:** com um `steam_running()` falso positivo, o guard **não pode**
escrever uma linha — asserção sobre o vdf byte a byte inalterado *e* sobre a
mensagem de adiamento. *Arranque o gate da Steam e veja o teste reprovar com o
vdf reescrito.*

**Por que merge e não reafirmação:** seção 7. Sem merge, o guard vira o terceiro
pêndulo.

### E3 — chega na interface (regra dela, 09/08)

Hoje a interface só sabe avisar **de dentro do jogo**: o
`wrapper_dialog_decision` (`app/actions/launch_wrapper_dialog.py:106`) exige a
GUI viva, emulação de gamepad ligada, a janela do jogo em foco, e mostra **uma
vez por sessão**. Ele é reativo e chega tarde — e **não tem como** perceber um
campo apagado por um timer uma hora depois.

O que falta é o estado, não mais um aviso: na aba Sistema, ao lado do botão
"Aplicar aos jogos da Steam", **a fração** — *"wrapper em 60 de 61 jogos"* — em
vermelho quando `< 100%`, com a lista dos descobertos e o valor de cada um. É a
mesma frase do E1, na tela em vez do terminal. E, com a Steam aberta, o botão
diz **por que** está desabilitado, em vez de só estar cinza.

### E4 — a nota de conflito, e ela não é código deste repositório

A tabela `~/.config/zsh/scripts/aurora-steam-launchopts.conf` tem **uma** linha,
e ela carrega uma cura que **já é global desde 14/08**: o self-heal v3.59 grava
`VKD3D_CONFIG=no_upload_hvv` em `/etc/environment` (conferido: linha 9), lido
pelo `pam_env` em todo login gráfico. A entrada por appid virou **redundante** —
foi exatamente essa a decisão dela, escrita no
[índice de 15/08](2026-08-15-INDICE-a-madrugada-que-quase-nao-virou-pagina.md):

> *"pra todo e qualquer jogo não deveríamos ter essa limitação"*

Logo, o reparo imediato é **`jogo rm 3357650`** na casa dela — uma linha,
zero custo, e o pêndulo para. **Mas isso não é a cura**, é o curativo: o próximo
`jogo set` rearma a bomba, para qualquer appid. A cura é E1+E2.

**Isto fica registrado aqui e não é feito por mim:** é a casa dela, fora deste
repositório, e é decisão dela.

---

## 10. O custo dela

**Já pago:** uma noite de jogo, e a sessão inteira de diagnóstico.

**Para reparar, e é o preço mínimo de qualquer conserto neste campo:**

| ação | custo | precisa da Steam fechada? |
|---|---|---|
| conferir (`cat …/last_run`, censo da seção 5) | 30 s | **não** |
| `jogo rm 3357650` (para o pêndulo) | 1 min | não (a tabela); a aplicação sim |
| reaplicar o wrapper (`--apply`) | 2 min | **SIM** |
| E1 + E2 + E3 (código) | não estimado — não construídas | não, para escrever |

**A Steam estava ABERTA e ela estava jogando durante toda esta sessão. Nada foi
escrito no `localconfig.vdf`, por regra e por instrução.** A Steam mantém a
própria cópia em memória e regrava o arquivo ao sair, engolindo qualquer edição
feita por baixo — é por isso que os dois escritores desta máquina, o nosso e o
dela, **já** recusam agir com a Steam viva (`apply_wrapper_to_all_games` devolve
`steam_aberta`; o `aurora-steam-launchopts.sh` imprime *"Steam ABERTA — <!-- ref-externa: ~/.config/zsh/scripts/, fora deste repositório -->
pulando"*). Essa disciplina está certa e não se mexe nela.

**O que o produto deve à interface:** hoje, "adiado porque a Steam está aberta" é
uma mensagem de terminal. Ela não usa terminal para jogar. É o E3.

---

## 11. O que fica ABERTO

- **cabo × rádio** — seção 6. O ensaio de quatro minutos está escrito; ninguém o
  fez. **Nenhuma frase deste repositório pode afirmar que o wrapper conserta o
  Bluetooth** até que ele seja feito;
- **quem gravou o vdf às 03h33 de 16/08** — a Steam gravou (mtime confirmado), e
  o campo do Pragmata voltou a ter o wrapper **e perdeu o `VKD3D_CONFIG`**. A
  leitura mais provável é que a string constante foi colada no campo pela
  interface da Steam. **Se foi ela, é a mesma falha na direção oposta** — o
  campo único apagou a outra receita — e só não custa nada porque a cura já é
  global desde 14/08 (E4). **Pergunta dela, não minha;**
- **o `.env` do prognóstico com `backends=[]`** — o
  `steam_app_3357650.env` de 03:33 traz `SDL_GAMECONTROLLER_IGNORE_DEVICES` e
  `PROTON_DISABLE_HIDRAW` **sem nenhum vpad vivo** no cabeçalho de estado. O
  `compose_env` (`daemon/launch_env.py:933`) tem a guarda
  `… and emulation_enabled and backends`, então esse arquivo veio do caminho de
  **prognóstico de perfil**, que monta env antes de haver controle na mão. Se um
  jogo abrisse nesse instante e o wrapper rodasse, ele exportaria "esconda o
  DualSense físico" **sem vpad para repor** — que é o "zero controles" que a
  doutrina desta casa proíbe por escrito. **Grau: SUSPEITA COM MECANISMO**, não
  medida em jogo; merece uma linha de ensaio antes de virar sprint;
- **o ponteiro morto** das três units do guard para
  `FEAT-STEAM-INPUT-SELF-HEAL-01.md` (seção 7).

---

## 12. A frase para levar

**O daemon estar saudável não é evidência de nada.** Neste defeito, tudo o que
se pode observar em tempo real — luz, gatilhos, perfil, grab, journal — estava
perfeito, e o jogo tinha zero controles. A prova viva não estava num processo:
estava numa linha de texto que ninguém tinha motivo para abrir, e num arquivo de
três linhas que o próprio wrapper escreve para dizer *"eu estive aqui"*.

Quando o jogo não vê o controle, **comece pelo `last_run`**.
