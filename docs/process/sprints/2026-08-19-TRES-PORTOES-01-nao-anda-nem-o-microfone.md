# TRÊS PORTÕES — 01

*"não anda. nem o microfone."*

- **Escrito em:** 19/08/2026, de madrugada, depois de a noite inteira ter sido
  gasta procurando **um** defeito onde havia **três**.
- **Grau desta página:** as §1 a §4 são **medidas nesta máquina hoje**, com o
  comando ou o arquivo ao lado de cada número. A §5 relata o que seis frentes
  entregaram, com a mordida de cada uma **e o veredito do cético de cada uma**.
  A §6 e a §7 são projeto, e cada afirmação carrega o grau dela.
- **O que esta página é:** a página que existe para a próxima sessão **não
  reaprender** o que esta noite custou. Se você tem cinco minutos, leia a §2 (os
  três portões) e a §3 (o que o diagnóstico errou) — as duas juntas são a lição
  cara.

> **AVISO DE INFRAESTRUTURA, e é o primeiro porque contamina tudo abaixo.**
> As seis frentes desta noite nasceram em `git worktree` apontando para
> **`670315d`** (31/07/2026 10:26). O topo da sessão é **`2706aaa`**
> (19/08/2026 02:12). São **258 commits e 19 dias** de distância —
> `git rev-list --count 670315d..2706aaa` = 258. Consequência medida pelos
> céticos: patches que **não aplicam** na árvore que roda, contagens de teste
> que não batem (as frentes relataram `mypy` sobre *157 source files*; a árvore
> de hoje tem **180** arquivos `.py` em `src/hefesto_dualsense4unix`), e pelo
> menos uma entrega que, aplicada inteira, **reverteria curas medidas** de 06,
> 08, 09 e 18/08.
>
> **Antes de qualquer coisa, confira em que commit você está.** Esta página foi
> escrita depois de `git reset --hard` para o topo da sessão, e todos os números
> abaixo são da árvore que roda.

---

## 1. A queixa dela

Textual, e é o cabeçalho desta página:

> *"não anda. nem o microfone."*

Duas frases curtas, dois defeitos diferentes, e nenhum deles era o que eu fui
procurar. O DON'T SCREAM (appid `2497900`) é um jogo cuja mecânica inteira é o
microfone: se o controle não anda **e** o microfone não entra, não sobra jogo.

---

## 2. Os três portões, em série

O que fez esta noite custar horas não foi a dificuldade de nenhum dos três. Foi
estarem **em série**: cada um, sozinho, bastava para o jogo continuar
injogável. Consertar um deixava o sintoma **idêntico** — e um conserto certo
que não muda o sintoma parece um conserto errado. Foi assim que passamos a noite
desfazendo o que estava certo.

**A regra que sai daqui, e ela é geral:** com portões em série, *"o jogo
funcionou?"* não é instrumento — ele não sabe atribuir. Cada portão precisa da
**sua própria régua**, medida separadamente, antes de qualquer tentativa de
ponta a ponta.

### 2.1 Portão 1 — o produto trocou o Proton que ela tinha escolhido

**Medido**, e já **curado e commitado** nesta sessão (`2706aaa`).

O recurso *"Travar Proton validado"* (`install.sh:2980`, **ligado por padrão**,
opt-out `--no-proton-pin`) rodava sobre a biblioteca inteira e **substituía**
qualquer jogo que já tivesse ferramenta de compatibilidade escolhida. Em
**14/08/2026 03:04** ele tocou 19 jogos: 16 eram `added` (não tinham nada), e
**3 eram `replaced`** — três escolhas deliberadas dela, apagadas sem pergunta:

```
appid 2497900 (DON'T SCREAM):        proton_11  ->  GE-Proton10-34
appid 3357650:              proton_experimental  ->  GE-Proton10-34
appid 4046520:                       proton_11  ->  GE-Proton10-34
```

O estado de hoje, lido agora do disco dela
(`~/.steam/debian-installation/config/config.vdf`, bloco `CompatToolMapping`):

```
"2497900"
{
    "name"        "proton_11"
    "config"      ""
    "priority"    "250"
}
```

**A cura:** entrada DE JOGO que já aponta para outra ferramenta vira
`action="preservado"`; a entrada global `"0"` fica fora da guarda de propósito
(travar o padrão do Steam Play é a função declarada do recurso, e ela tem
caminho de volta). E a contagem parou de mentir: `locked` conta o que travou,
`skipped` conta o que preservou — antes somava tudo, e foi assim que o atropelo
de 14/08 passou despercebido por quatro dias.

**Por que isolado parecia não adiantar:** devolver o Proton certo não fazia o
controle aparecer (portão 2) nem parava o vpad de morrer no meio da partida
(portão 3). O jogo continuava injogável, e a conclusão fácil — errada — era que
o Proton não era o problema.

> **Ressalva importante, e é minha, não da cura:** que a troca de Proton tenha
> sido o que matou o microfone **não está provado pelos logs que estão no
> disco**. Ver a §3.2. A cura se sustenta sozinha por outro motivo, que basta:
> **o produto apagou uma escolha deliberada dela e não avisou.**

### 2.2 Portão 2 — com o Steam Input desligado, o jogo não via controle nenhum

**Medido pela observação dela** (fonte primária nesta casa): com o Steam Input
**desligado** o DON'T SCREAM não via controle nenhum; com ele **ligado**, ela
conseguiu usar o controle.

O que está no disco dela agora, `localconfig.vdf`, bloco do appid na árvore
viva:

```
"2497900"
{
    "UseSteamControllerConfig"     "2"
    "SteamControllerRumble"        "-1"
    "SteamControllerRumbleIntensity"  "320"
    "LaunchOptions"  "sh -c '…/hefesto-launch' … %command%"
}
```

Ela ligou à mão. E o produto **não sabe ligar isso**: nenhuma linha deste
repositório LIGA o Steam Input — o guarda o **desliga**, e a allowlist
(`steam_input_apps.txt`) só **preserva** o que já estava ligado. O próprio
`integrations/prontuario_dos_jogos.py` já nomeava esse buraco, com todas as
letras, desde 16/08: o estorvo **`excecao_inerte`**, *"A lista só preserva o
que já estava ligado — ela nunca liga."*

E o que o produto entrega ao jogo, lido do arquivo que o wrapper injeta
(`~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_2497900.env`):

```
PROTON_DISABLE_HIDRAW=0x054C/0x0CE6
SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6,0x28de/0x11ff
__GL_SHADER_DISK_CACHE=1
__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1
SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0
```

Repare no segundo par: `0x28de/0x11ff` é **o espelho Xbox que o Steam Input
cria**. O produto manda o jogo **ignorar** exatamente o aparelho que, medido por
ela, era o que fazia o jogo andar.

**O wrapper rodou** — não é o caso do Pragmata. O marker do próprio wrapper,
lido agora:

```
$ cat ~/.local/state/hefesto-dualsense4unix/launch_env/last_run
appid=2497900
epoch=1787115106     # = 2026-08-19 01:51:46
```

**Por que isolado parecia não adiantar:** ligar o Steam Input devolvia um
controle, mas o vpad continuava sendo destruído no meio da partida (portão 3), e
o microfone continuava fora (portão 1 aparente). O ganho real ficava escondido
atrás dos outros dois.

**O mecanismo NÃO está fechado**, e a §3.3 explica por que a explicação que
circulou esta noite é pior do que a que a casa já tinha guardada.

### 2.3 Portão 3 — o perfil pedia uma máscara, o aparelho tinha outra, e o vpad morria

**Medido no journal dela.** O perfil dizia `gamepad_flavor="xbox"`, o estado
vivo dizia `dualsense`, e o daemon passou a noite tentando convergir. A §4 tem
as linhas.

**Por que isolado parecia não adiantar:** trocar a máscara à mão funcionava por
alguns minutos e depois desfazia sozinho — o que se parece exatamente com *"a
troca de máscara não é a cura"*. Não era a troca que falhava: era ela ser
**desfeita** pelo caminho automático, e o produto **dizer que tinha aplicado**
quando não aplicou.

---

## 3. O que o diagnóstico errou, e por quê

Esta seção existe porque **errar de forma rastreável é o que permite não
repetir**. As três correções abaixo são contra o meu próprio diagnóstico desta
noite.

### 3.1 Eu afirmei que a máscara Xbox tinha curado o jogo. Ela não estava lá.

**Medido, e derruba a afirmação.** Na sessão em que ela jogou por último
(01:51:45 → 01:54:16, ver §4), a máscara **viva** era `dualsense`:

```
2026-08-19T01:51:25.364689 [info] gamepad_emulation_started      flavor=dualsense
```

e o arquivo por appid que o jogo leu foi materializado no mesmo instante com
`mascara=dualsense`. O pedido de `xbox` do perfil tinha sido **recusado quatro
vezes** pelo gate R-04 entre 01:37 e 01:45.

Ou seja: quando eu disse *"a máscara Xbox curou"*, a máscara Xbox **não estava
no aparelho**. Eu li o pedido e não conferi o aparelho — que é exatamente o
defeito que a frente `a-mascara-que-nunca-chega` foi consertar no código (o
applier passou a conferir o `_snapshot` depois de aplicar, em vez de acreditar
no retorno).

**A lição, e ela é velha nesta casa:** *o instrumento mente mais que o produto.*
Ler o que foi PEDIDO e chamar de MEDIDO é a forma mais fácil de produzir um
laudo convincente e falso.

### 3.2 A substituição também está errada: "quem curou foi o Proton 11" não se sustenta nos logs

Este é o achado mais desconfortável da página, e a regra da casa manda
**substituir o fato errado**, não guardá-lo ao lado do certo.

A régua que circulou esta noite foi: *"no GE-Proton10-34 o motor Unreal registra
`No Audio Capture implementations found` e ZERO `WasapiCapture`; no Proton 11 o
`WasapiCapture` inicializa."* Os logs do jogo que estão no disco dela **não
sustentam essa régua**. Censo dos 11 logs de sessão do DON'T SCREAM desta noite
(`…/common/DON'T SCREAM/DontScream/Saved/Logs/`), contando as duas linhas:

| log (abertura, hora local) | `WasapiCapture` | `No Audio Capture implementations found` |
|---|---|---|
| 18/08 23:33:08 | 0 | 2 |
| 18/08 23:35:09 | 0 | 2 |
| 18/08 23:45:05 | **3** | 2 |
| 19/08 00:02:07 | 0 | 2 |
| 19/08 00:32:00 | **2** | 2 |
| 19/08 00:36:41 | **3** | 2 |
| 19/08 01:37:12 | **2** | 2 |
| 19/08 01:44:15 | **2** | 2 |
| 19/08 01:45:47 | 0 | 2 |
| 19/08 01:48:43 | **4** | 2 |
| 19/08 01:51:51 (a última) | **0** | 2 |

Duas conclusões, e as duas são medidas:

1. **`No Audio Capture implementations found` aparece exatamente DUAS vezes em
   TODOS os logs** — inclusive nos que abriram captura com sucesso. Ela **nunca
   discriminou nada**. Usá-la como sinal de defeito é a armadilha nº 1 desta
   casa em roupa nova: *medir contra a régua errada produz alarme convincente e
   falso*.
2. **O `WasapiCapture` oscila dentro da MESMA noite** — 0, 0, 3, 0, 2, 3, 2, 2,
   0, 4, 0. A captura de áudio do jogo é **intermitente**, e a última sessão, a
   que ela jogou por 2 min 31 s, teve **ZERO**.

O que sobra de pé sobre o portão 1, e basta: **o pin substituiu uma escolha
deliberada dela em três jogos, sem perguntar e sem avisar.** Isso é medido
(commit `2706aaa`) e a cura é correta por si. O que **não** está provado é a
cadeia causal *Proton trocado → sem `WasapiCapture` → microfone morto*.

**A medição que fecharia isso, e que ninguém tomou:** abrir o jogo cinco vezes
no `proton_11` e cinco no `GE-Proton10-34`, sem mexer em mais nada, e contar
`WasapiCapture` em cada log. Quinze minutos. Enquanto ela não roda, o honesto é
o par: a escolha dela foi atropelada (medido), e o efeito disso sobre o
microfone continua **em aberto**.

### 3.3 O mecanismo do portão 2 foi re-derivado pior do que a casa já o tinha

Esta noite afirmou-se que *"o `SDL_GAMECONTROLLER_IGNORE_DEVICES` governa só o
SDL e não alcança o XInput da Unreal"*. A casa já tinha, guardado e melhor:

- **SDL-ATALHO-01 (11/08/2026)**, lido no fonte do SDL2/SDL3 e registrado em
  `scripts/medir_steam_virtual_gamepad.sh`: `SDL_ShouldIgnoreGamepad` tem um
  atalho —

  ```c
  if (SDL_IsJoystickSteamVirtualGamepad(...))
      return !allow_steam_virtual_gamepad;
  ```

  — que decide o par `0x28de/0x11ff` **antes** de consultar a lista de
  ignorados. Para aquele par, a lista **nunca é lida**. Isto é mais simples e
  mais forte do que a hipótese do XInput, e explica por que o espelho da Steam
  sobrevive ao nosso `IGNORE_DEVICES`.
- **A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01 (16/08/2026)** já mediu a classe inteira
  no Duskfade: Unreal 5.6, **`XInputDevice` é o único backend de gamepad
  montado**, e `find` por `*SDL*` na pasta do jogo devolve **0 arquivos**. E a
  mesma página já traz a **nota de honestidade** que esta noite não trouxe: que
  o `XInputDevice` sob Proton exija especificamente o VID `045e` é **média, não
  medida** — falta ler por qual critério o `winebus.sys` marca um aparelho como
  XInput-capaz.

**A lição, e ela já está na memória desta casa:** *a casa sabe e o produto não
faz.* Antes de derivar mecanismo do zero, procure — o defeito mais caro daqui é
a cura escrita e nunca ligada, e o segundo mais caro é a medição feita duas
vezes.

**O que fecha o portão 2, e custa quatro minutos:** rodar
`bash scripts/medir_steam_virtual_gamepad.sh` com a Steam aberta e o jogo em
sessão. Ele lê `/proc/<pid>/environ` dos processos dela e responde se a Steam
exporta `SDL_GAMECONTROLLER_ALLOW_STEAM_VIRTUAL_GAMEPAD=1`. Nunca foi rodado com
jogo em sessão.

### 3.4 E o instrumento mentiu mais uma vez: o cache do `ruff`

Um dos céticos concluiu que os avisos `Invalid # noqa` do `ruff` **não eram
pré-existentes** — *"aqui imprime uma linha só, sem nenhum Invalid"* — e daí que
o código novo de uma frente os teria introduzido. Medido agora, nesta árvore,
com **zero** linhas de Python alteradas por mim:

```
$ .venv/bin/ruff check . | grep -c Invalid
0
$ .venv/bin/ruff clean
Removing cache at: .ruff_cache
$ .venv/bin/ruff check . | grep -c Invalid
9
```

**O cache do `ruff` esconde os avisos.** Numa segunda passada, os arquivos que
não mudaram não são relidos, e os avisos deles não saem. São **nove**, são
**pré-existentes**, e ninguém os introduziu esta noite.

A regra prática, para quem for usar `ruff` como régua de comparação entre duas
árvores: **`ruff clean` antes**, senão você está comparando dois caches
diferentes e não dois códigos.

---

## 4. O laço que matava o controle

### 4.1 As linhas, do journal dela

```bash
journalctl --user -u hefesto-dualsense4unix.service --since "2026-08-18 22:00" \
  -o short-iso | grep -E "vpad_recriacao_bloqueada_por_jogo|gamepad_emulation_"
```

```
00:36:07.945  [info ] gamepad_emulation_stopped
00:36:08.593  [info ] gamepad_emulation_started      flavor=xbox
00:38:49.369  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
00:38:54.559  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
00:40:07.282  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
00:40:07.943  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
00:40:15.192  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
00:40:31.993  [info ] gamepad_emulation_stopped
00:40:32.268  [info ] gamepad_emulation_started      flavor=dualsense
01:37:07.405  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:dualsense->xbox origem=profile
01:37:13.984  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:dualsense->xbox origem=profile
01:44:11.097  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:dualsense->xbox origem=profile
01:45:41.792  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:dualsense->xbox origem=profile
01:48:38.977  [info ] gamepad_emulation_stopped
01:48:39.605  [info ] gamepad_emulation_started      flavor=xbox
01:50:58.403  [warn ] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:xbox->dualsense origem=profile
01:51:25.090  [info ] gamepad_emulation_stopped
01:51:25.364  [info ] gamepad_emulation_started      flavor=dualsense
```

**Dez recusas** do gate R-04 na noite, e **quatro** destruições-e-recriações do
vpad. O motivo alterna nos dois sentidos (`xbox->dualsense` e
`dualsense->xbox`), que é a assinatura de duas autoridades brigando, não de um
componente insistindo sozinho.

### 4.2 A mentira, com sete milissegundos de distância

Esta é a linha que vale a página inteira:

```
01:37:13.984091 [warn] vpad_recriacao_bloqueada_por_jogo motivo=troca_de_mascara:dualsense->xbox origem=profile
01:37:13.991412 [info] profile_autoswitch  adiado=[] from_='Big Walk'
        secoes=['mic=aplicado', 'mode=aplicado', 'modo_jogo_padrao=aplicado',
                'rumble_policy=aplicado', 'speaker=aplicado', 'suppression=aplicado']
        to='Dont Scream' wm_class=steam_app_2497900 wm_name=DontScream
```

**Sete milissegundos** depois de o gate RECUSAR a troca de máscara, o applier
registrou `mode=aplicado` e `adiado=[]`. O produto mentiu para si mesmo — e
essa mentira é a raiz do laço: quem chamou acreditou que convergiu, e tentou de
novo. É exatamente o defeito que a frente `a-mentira-do-retorno` foi fechar.

### 4.3 A destruição que o gate deixou passar, e por quê

O caso das 01:51:25 é o mais instrutivo, porque o gate R-04 **existe** para
impedi-lo e mesmo assim ele aconteceu. A janela inteira:

```
01:50:58.403  [warn ] vpad_recriacao_bloqueada_por_jogo  ... origem=profile
01:50:58.410  [info ] profile_activated      name='Dont Scream' origin=manual priority=97
01:51:21.779  [info ] launch_env_materializado  emulacao=True mascara=xbox backends=['uinput']
01:51:25.084  [warn ] rumble_sem_dono        emulacao=False motivo=sem_vpad_e_sem_modo_nativo
01:51:25.090  [info ] gamepad_emulation_stopped
01:51:25.292  [info ] uhid_device_created    name='DualSense Wireless Controller (Hefesto P1)' player=1
01:51:25.364  [info ] gamepad_emulation_started  flavor=dualsense
01:51:26.148  [info ] autoswitch_congelado_pelo_cadeado  candidate=Navegação wm_class=steam
01:51:28.856  [info ] autoswitch_janela_propria_ignorada  wm_class=Hefesto-Dualsense4Unix
```

Às **01:50:58** o gate bloqueou (logo, a autoridade do jogo estava de pé).
**Vinte e sete segundos depois**, às 01:51:25, a mesma troca passou e o vpad foi
destruído e recriado.

O gate lê `display_authority` (`daemon/subsystems/gamepad.py:1353`), que é
**sticky por ~30 s**. E a árvore já documenta o defeito, por escrito, em
`daemon/lifecycle.py:2043-2047`:

> *"o sinal é sticky e tem defeito CONHECIDO E NÃO CORRIGIDO (cai de `game` para
> `daemon` ~30 s depois com o jogo ainda aberto)"*

Às 01:51:28 o foco estava na **janela do próprio Hefesto**
(`wm_class=Hefesto-Dualsense4Unix`). Ela tinha saído do jogo para a interface
para tentar consertar — e ~30 s depois disso o sinal que protege o vpad decaiu,
e a proteção caiu junto. **O portão que existe para não arrancar o controle da
mão dela abriu porque ela foi mexer na janela do produto.**

> **Honestidade sobre o que NÃO consigo fechar:** as linhas
> `gamepad_emulation_stopped` e `gamepad_emulation_started` **não carregam a
> origem**. Há dois caminhos que produzem esta destruição — a autoridade
> decaindo (acima) ou um `origin="manual"` vindo da interface, que o gate nunca
> bloqueia por decisão de produto. Os dois são compatíveis com o journal, e
> **nenhum campo gravado os separa**. Ver §6, item 1: é um `origem=` numa linha
> de log, e sem ele este parágrafo não fecha.

### 4.4 A última sessão, minuto a minuto

Fontes: `autocloud` da Steam (`lastlaunch`/`lastexit`), o marker do wrapper, o
log do jogo e o journal do daemon.

| hora | o que aconteceu | fonte |
|---|---|---|
| 01:51:25 | vpad destruído e recriado como `dualsense` | journal |
| 01:51:45 | Steam lança o jogo | `autocloud/lastlaunch=1787115105` |
| 01:51:46 | o wrapper roda e grava o marker | `launch_env/last_run` |
| 01:51:51 | o log do jogo abre | `DontScream.log` |
| 01:51:56 | mapa carregado (`DS_Start`) | log do jogo |
| 01:52:09 | o jogo **enumera** aparelhos de entrada de áudio | `LogAudioCapture: GetAvailableAudioInputDevices` |
| 01:52:10 | última linha que o jogo escreve; `WasapiCapture` = **0** na sessão inteira | log do jogo |
| 01:52:27 → 01:52:29 | **três** `mic_hotkey_toggle` em **2,77 s** | journal |
| 01:54:16 | o jogo sai. Sessão: **2 min 31 s** | `autocloud/lastexit=1787115256` |

Isto reordena a história do microfone e vale ser dito sem rodeio: **na última
sessão o jogo enumerou os aparelhos de entrada e não abriu captura nenhuma.**
Com zero `WasapiCapture`, nenhum estado de mudo — nem do sistema, nem do
firmware — poderia ter feito diferença. O repique do botão do microfone é real
e merece a cura (1) da §5.5 — a janela de sossego —, mas **não foi ele que calou
o jogo dela nesta sessão**. Quem quiser atribuir o microfone mudo a um culpado
precisa explicar antes por que o motor não abriu captura; ver §3.2.

O repique, literal:

```
01:52:27.202774 [info] mic_hotkey_toggle   muted=False
01:52:27.935053 [info] mic_hotkey_toggle   muted=True
01:52:29.969405 [info] mic_hotkey_toggle   muted=False
```

Três bordas, 2,77 s, espaçadas por 0,73 s e 2,03 s — os espaçamentos são da
**duração do próprio toggle** (dois `subprocess.run` com `timeout=2.0` cada), o
que é a assinatura do debounce ancorado no INÍCIO da chamada
(`integrations/audio_control.py`): a janela efetiva é
`max(0, 0,2 − duração_do_toggle)`, isto é, **zero** sempre que o áudio demora.

---

## 5. O que cada conserto fez, e a mordida de cada um

Seis frentes trabalharam em paralelo, cada uma com um cético independente.
**O veredito do cético está em cada item**, porque três das seis entregas têm
problema de integração e uma foi reprovada — omitir isso faria esta página
repetir o erro que ela documenta.

### 5.1 `a-mentira-do-retorno` — o retorno que fundia três desfechos num `True`

`set_gamepad_emulation` devolvia **`True`** para três desfechos diferentes:
aplicou, já-estava e **foi bloqueado**. O trabalho real virou
`start_gamepad_emulation_desfecho` / `Daemon.set_gamepad_emulation_desfecho`,
que devolvem o vocabulário `EMU_*` (`aplicado`, `ja_estava`,
`bloqueado_por_jogo`, `recusado_steam_input`, `falhou`, `desligado`) — o mesmo
dialeto dos appliers de perfil que já existia. As funções antigas viraram
fachadas e o IPC não mudou. `apply_profile_mode` passou a devolver
`ADIADO_JOGO_ABERTO` quando o gate recusa, e o laço morreu num latch
(`MascaraAdiada`): com jogo na autoridade, o primeiro bloqueio vira estado
**estável**, dito uma vez no journal e sem repetir o pedido.

**Mordida (literal), arrancando o latch em `lifecycle.py`:**

```
E   AssertionError: o pedido recusado foi repetido — é este o laço que matou o
    controle dela no meio da partida (pedidos=['xbox','xbox','xbox','xbox','xbox'])
E   assert ['xbox','xbo...xbox','xbox'] == ['xbox']
FAILED tests/unit/test_verdade01_o_retorno_que_mentia.py::test_o_applier_diz_adiado_e_nao_repete_o_pedido
FAILED tests/unit/test_verdade01_o_retorno_que_mentia.py::test_o_pingue_pongue_de_duas_janelas_tambem_para
FAILED tests/unit/test_verdade01_o_retorno_que_mentia.py::test_modo_jogo_padrao_nao_vira_laco_com_a_mascara_divergente
```

**Cético:** reproduziu a mordida de forma independente — é honesta. Mas achou
**dois defeitos fatais**: (a) a entrega é sobre a base de 31/07 e **reverte três
decisões datadas** (co-op 06/08, origin-sem-default 08/08, JOGO-01 09/08); (b) o
latch roda **antes** de consultar o gate, e por isso engole dois casos que o
gate deixava passar de propósito — a recriação de um vpad **morto** (*"é a única
chance de o jogo ter controle"*) e **o gesto dela** pelo `profile.switch`. Os
dois provados por teste. **Rebase obrigatório, e o latch precisa perguntar ao
gate antes de segurar.**

### 5.2 `a-mascara-que-nunca-chega` — o arquivo por appid que colava duas verdades

O arquivo `steam_app_<appid>.env` era renderizado com
`_render(env, f"{motivo} | {estado}")`, onde `motivo` é a opinião **do perfil** e
`estado` é o snapshot **global** do daemon — duas verdades diferentes na mesma
linha, e a do perfil sequer tinha um `mascara=`. Foi essa a contradição das
00:40 (*"perfil gamepad xbox"* ao lado de *"mascara=dualsense"*). O modo do
perfil virou dado (`ModoAntecipado`), a divergência virou decisão pura com
evento nomeado, e o arming passou a **conferir o aparelho** depois de aplicar em
vez de acreditar no retorno.

E achou o buraco de determinismo: `arm_launch_profile` só era chamado por
`_reconciliar_launch` ← `dispatch_gamepad`, que o poll loop gateia em
`self._gamepad_device is not None` — **com a emulação desligada não há vpad,
logo não há dispatch, logo o modo do perfil nunca era armado**.

**Mordida (literal), devolvendo o estado global à linha do arquivo:**

```
FAILED tests/unit/test_mascara_do_perfil_no_launch.py::test_env_do_jogo_materializa_a_mascara_do_perfil
>       assert "mascara=xbox" in linha
E       assert 'mascara=xbox' in "# estado: perfil gamepad xbox | native=False
        emulacao=True mascara=dualsense backends=['uhid'] | 2026-08-19T02:16:55"
```

A linha reprovada **é** a contradição das 00:40.

**Cético:** as três mordidas são reais e reprovam pelo motivo certo; a hipótese
explica o que já funcionava; o gate R-04 não foi enfraquecido. Mas o patch **não
aplica** na árvore de hoje (5 de 8 hunks falham em `launch_env.py`) e o código
novo desempacota `_snapshot` em **quatro** campos onde a árvore que roda devolve
**cinco** — o que faria a conferência de convergência morrer calada dentro de um
`contextlib.suppress(Exception)`. **Rebase obrigatório.**

### 5.3 `a-ponte-que-a-lista-nunca-liga` — a allowlist passou a ligar

Nasceu `integrations/steam_input_ponte.py`, que escreve <!-- ref-externa: o módulo é entrega desta noite e NÃO está commitado, logo não existe nesta árvore — é o que o item 7 da §6 registra -->
`UseSteamControllerConfig = 2` para os appids da lista dela.
 A armadilha das
três árvores `apps` foi **medida** no `localconfig.vdf` vivo, e o resultado é o
contrário do que se supunha: as 11 ocorrências de `UseSteamControllerConfig`
estão em `UserLocalConfigStore/apps`, **zero** na árvore canônica das
`LaunchOptions` — **cada chave tem a sua árvore viva**. O módulo por isso
**procura** a árvore por duas âncoras e **recusa escrever** quando não a prova.
O prontuário foi ligado: `_CURAS` despacha todo estorvo com `automatica=True`.

**Mordida (literal), arrancando o ramo que LIGA:**

```
_________ TestAListaLiga.test_o_jogo_da_lista_desligado_passa_a_ligado _________
>       assert ligados == [_SACKBOY]
E       AssertionError: assert [] == ['1599660']
```

**Cético:** o núcleo do desenho está certo, e a premissa (`2` por jogo honrado
com `SteamController_PSSupport` global em `0`) **já estava medida** em 06/08 —
o módulo não cita essa página. Reproduziu **dois defeitos novos**: o `--restore`
deixou de desfazer o guarda (o `restore_vdf` casa `*.bak.steam-input-*` e o
backup novo se chama `.bak.steam-input-ponte-<ts>`, sempre mais novo), e o
`--apply-quiet` carimba `resultado=nada-a-fazer` **depois de escrever no vdf
dela**. E corrigiu a manchete: `curar_o_que_e_automatico` **não tem chamador**
fora do teste — quem foi ligado é o módulo, pelo shell.

### 5.4 `o-gesto-que-troca-de-ponte` — PS + direita cicla a ponte

O `_fire` do `HotkeyManager` era uma cadeia de ifs terminada em
`else: cb = self.on_prev` — **qualquer** combo desconhecido trocava o perfil para
trás. Virou despacho por dicionário. Entrou `PS + dpad_right` = próxima ponte,
ciclando `dualsense -> xbox -> mouse+teclado`, lendo a ponte **atual do estado
vivo**, com `origin="manual"` e aviso pela lightbar **antes** de aplicar.

**Mordida (literal), devolvendo a cadeia de ifs:**

```
FAILED tests/unit/test_hotkey_ponte_cycle.py::test_combo_da_ponte_nao_dispara_o_perfil_anterior
E       AssertionError: o combo da ponte não pode disparar next/prev
E       assert ['prev'] == ['ponte']
```

**Cético:** as quatro mordidas são reais, mas achou **um bloqueio**: o D-pad é
decodificado em **dois eixos independentes**, então a diagonal produz
`{dpad_up, dpad_right}` no mesmo snapshot — `PS + diagonal` satisfaz ao mesmo
tempo o combo `next` e o combo `ponte`, e quem dispara depende da ordem do
dicionário. Também: o passo *mouse+teclado* do ciclo apaga a **preferência em
disco** por R-07 (um gesto de dois segundos deixa a máquina sem vpad no próximo
boot), e o gesto **não grava** a ponte no perfil, o que re-arma a divergência
perfil≠vivo que produziu o laço. E substituiu um fato errado: o combo vazio
dispara **uma** vez e depois latcha, não *"a cada tick"*.

### 5.5 `o-microfone-mudo` — a rajada de bordas e os dois donos do mudo

Duas causas no caminho do microfone: (1) o `mic_button_loop` não tinha defesa
contra rajada, com toda a proteção terceirizada para um debounce ancorado no
início da chamada (§4.4) — entrou uma janela de sossego de 1 s contada do FIM do
toggle; (2) um toque move **dois** mudos, o do firmware (que o `hid-playstation`
alterna na borda do botão físico) e o do sistema, e um número ímpar de bordas os
deixa em fase oposta.

**Mordida (literal), arrancando a janela de sossego:**

```
FAILED …::TestARajadaDeBordas::test_cinco_bordas_seguidas_viram_um_toggle_so
E       AssertionError: uma rajada de bordas tem de virar UM toggle
E       assert 5 == 1
```

**Cético: a cura (2) foi REPROVADA, e a recusa é antiga.** Mutar o registrador
do firmware **toma a posse** e faz o botão físico parar de valer — recusado por
escrito na BT-E-VPAD-01 (medido 01/08), reafirmado na MIC-BT-DONO-01 (03/08), na
linha `audio.microfone.mudo` do mapa de canais e no `controller_card.py`, que
chama isso de *"sequestro silencioso que esta sprint foi fechar"*. No rádio nem
se sustenta: **a posse EVAPORA** (medido 03/08: mudo = 100% → 46% → 100%), porque
`_mic_mute_desejado` é atributo de instância de um handle que morre a cada
reconexão. E em co-op escreve no controle errado: o `BUTTON_DOWN` não carrega
`uniq`, então o jogador 2 mutaria o firmware do jogador 1.

**A cura (1) — a janela de sossego — é aproveitável** depois de rebase, e é a
que a §4.4 sustenta.

### 5.6 `a-gui-que-nao-esconde` — a aba Início parou de esconder a divergência

Duas linhas novas sob *"O jogo vê o controle como:"*: **"Ponte com o jogo:"**
(por onde o jogo recebe o controle agora) e **"Sua escolha:"** (só quando o que
ela pediu diverge do que o aparelho faz, com o motivo e o caminho). O rodapé
parou de dizer *"aplicado"* sobre recusa. E a foto offscreen revelou uma
armadilha de CSS: `.hefesto-dualsense4unix-status-warn` (especificidade 0,1,0)
**perde** para `.hefesto-dualsense4unix-window label` (0,1,1), e o aviso saía
branco — a cor passou a vir por markup `<span>`.

**Cético:** a parte de CSS está certa e bem medida — e **dois banners antigos
desta aba provavelmente saem brancos na tela dela desde sempre**, pela mesma
armadilha. Mas a "MORDIDA 1" **não é mordida**: o toast *"O jogo agora vê:"* não
existe em `src/` desde 08/08 (apagado pelo commit `1c75a1a`, decisão dela:
*"Nenhum IPC sai de um seletor da aba Início"*) — não houve cura devolvida, houve
handler novo introduzido. E o ramo do Steam Input depende de `vpad_suspenso`,
estado que nenhum caminho vivo produz desde 09/08.

---

## 6. O que ficou ABERTO

Sem maquiagem. Cada item diz **por que** não fechou.

1. **A linha que fecharia a §4.3 é um `origem=`.** `gamepad_emulation_stopped` e
   `gamepad_emulation_started` não gravam a origem da operação. Sem esse campo
   não dá para separar *"a autoridade decaiu"* de *"ela clicou"* — e são curas
   diferentes. É uma palavra em duas chamadas de `logger.info`
   (`daemon/subsystems/gamepad.py:1953` e `:2000`), e é o melhor retorno por
   linha escrita desta página inteira.

2. **O gesto PS + direita ainda executa a recriação que o R-04 mediu como fatal
   para a partida.** Trocar de máscara é destruir e recriar o vpad no **slot
   único** (`gamepad.py:1867` para, `:1892` cria), e a medição de 23/07 diz que
   isso invalida o handle que o jogo abriu — a Steam não reabre o hidraw do vpad
   do P1. O gesto avisa antes (dois pulsos vermelhos na lightbar), o que é
   honesto, mas **aviso não é cura**. Trocar de ponte ao vivo sem risco pede um
   vpad com **dois slots**, e ver o item seguinte.

3. **A sobreposição de dois vpads foi investigada e é insuficiente sozinha.**
   Criar o novo antes de matar o velho resolveria **metade** do problema. A outra
   metade é que boa parte de cada ponte é **variável de ambiente congelada no
   `exec`**: o `SDL_GAMECONTROLLER_IGNORE_DEVICES` e o `PROTON_DISABLE_HIDRAW`
   que o jogo leu (§2.2) foram lidos **uma vez**, no lançamento, e não há como
   reescrevê-los num processo vivo. Um vpad novo com identidade diferente
   apareceria para um jogo cuja lista de ignorados foi escrita para o vpad
   **antigo**. Sobrepor os dois slots é necessário e **não é suficiente**.

4. **Ninguém registrou os valores literais dos bytes que o vpad zera.** Medido
   agora, estaticamente, sobre `integrations/uhid_gamepad.py` (payload do report
   `0x01`, `_INPUT_PAYLOAD_SIZE = 63`): `_encode_body` escreve **37** posições e
   deixa **26** que **nunca recebem escrita**, em três faixas:

   | faixa | quantos | o que o DualSense real põe ali |
   |---|---|---|
   | 10 – 14 | 5 | **não registrado** |
   | 40 – 51 | 12 | **não registrado** |
   | 54 – 62 | 9 | **não registrado** |

   (O número que circulou esta noite foi *"24 bytes"*; a contagem acima é **26**,
   com os offsets ao lado para qualquer pessoa recontar. Substituído pela regra
   do fato errado — um número sem endereço não é medição.)

   **O que falta, e é uma tarde de bancada:** capturar N reports `0x01` do
   DualSense **físico** parado na mesa e tabelar o que ele põe em cada uma
   dessas 26 posições. Enquanto isso não existir, não se sabe se algum jogo lê
   alguma delas — e "o vpad manda zero" é uma afirmação que ninguém pode
   qualificar de inofensiva.

5. **O portão 2 continua sem mecanismo.** Ver §3.3: a medição custa quatro
   minutos (`scripts/medir_steam_virtual_gamepad.sh`, com a Steam aberta e o jogo
   em sessão) e nunca foi tomada.

6. **A cadeia causal do microfone continua aberta.** Ver §3.2: o `WasapiCapture`
   oscila dentro da mesma noite, e a última sessão teve zero. A medição que
   fecha são dez lançamentos, cinco por Proton, contando a linha.

7. **Três entregas precisam de rebase e uma foi reprovada.** §5.1, §5.2 e §5.5
   nasceram sobre `670315d`; a cura (2) de §5.5 está recusada por decisão medida
   e **não deve ser reproposta**. Nada disso está commitado.

8. **`ProfileManager.activate` tem `origin="manual"` por DEFAULT.** Hoje nenhuma
   rota automática esquece o parâmetro, mas um caminho automático **novo** que
   esquecer passa a atravessar o gate R-04 como se fosse gesto dela.

---

## 7. Os dois degraus que faltam na escada

### 7.1 A escada de hoje mede só a ida

O mapa de canais (`docs/data/mapa-controles.csv`, coluna `ate_onde_foi`) tem
três degraus, definidos em `docs/process/METODO-DE-ISOLAMENTO.md` e cobrados
pelo portão `scripts/check_paridade_transporte.py`:

```
MONTOU  ->  SAIU NO FIO  ->  O APARELHO OBEDECEU
```

Censo de hoje: **36** células com grau forte (`SAIU NO FIO` ou
`O APARELHO OBEDECEU`), e **zero** delas sem ensaio no caderno. A rede funciona.

**Mas os três degraus são da direção de SAÍDA** — do Hefesto para o aparelho.
"Montei o report", "o byte saiu e algo voltou", "acendeu, girou, saiu som". Esta
noite inteira aconteceu na direção **oposta**, e a escada não tem uma palavra
para ela. É por isso que o mapa podia estar todo verde enquanto ela não
conseguia jogar: **nenhuma célula do mapa fala sobre o jogo.**

### 7.2 Os dois degraus novos

```
… O APARELHO OBEDECEU  ->  O JOGO RECEBEU  ->  O JOGO REAGIU
```

- **O JOGO RECEBEU** — o processo do jogo abriu o nó e está lendo dele. É
  verificável de fora, sem a pessoa: o inode do nó aparece em
  `/proc/<pid>/fd`. (Identidade de nó é o **inode** (`stat -c %i`), nunca o
  caminho — o minor é reciclado: `event22` foi vpad DualSense às 01:40 e vpad
  Xbox às 01:50 — e nunca o carimbo de tempo do fd, que marca quando alguém
  **olhou** e ainda fica cacheado.)
- **O JOGO REAGIU** — o personagem andou, o gatilho endureceu **dentro do jogo**,
  o grito entrou. Isto **não** é verificável de fora. Nenhum instrumento desta
  casa lê o estado interno de um jogo Unreal sob Proton, e nenhum vai ler.

### 7.3 Por que o gesto dela é o instrumento do degrau que falta

O degrau **O JOGO REAGIU** só tem um sensor possível: **ela**. E é exatamente
isso que o desenho da noite pede — *o produto tenta em ordem, ela confirma UMA
vez qual ponte pegou com um gesto no controle, e o produto grava para sempre.*

O gesto não é conveniência de interface. Ele é **o instrumento de medida**:

1. **É o único sensor que enxerga o degrau.** "O jogo reagiu" é uma afirmação
   sobre a experiência dela, e a régua da casa já diz isso para o degrau de cima
   (`provado_por = olho-dela` é o único que sustenta *O APARELHO OBEDECEU*). O
   gesto estende a mesma disciplina um degrau adiante.
2. **Ele mede sem tirar a mão do controle.** Um instrumento que exige Alt+Tab
   destrói o que mede — foi assim que a autoridade decaiu e o vpad morreu
   (§4.3). O gesto é medido de dentro da partida.
3. **Ele custa uma vez por jogo.** O aprendizado mora no perfil, que já casa por
   `steam_app_<appid>`. Ela paga o gesto uma vez; a partir daí o produto sabe.
4. **Ele fecha a malha que a §3.1 abriu.** Hoje o produto pede uma ponte e
   escreve "aplicado". Com o gesto, o que fica gravado não é o que o produto
   **pediu**, é o que **funcionou** — que é a diferença entre `MONTOU` e
   `O APARELHO OBEDECEU`, aplicada ao jogo.

**O que ainda NÃO existe, e por isso os dois degraus não entraram no CSV:** o
domínio da coluna `ate_onde_foi` é fechado por design
(`check_paridade_transporte.py`, `DOMINIO_POR_SUFIXO`), e um valor novo reprova
de propósito — *"acrescentar um valor ao mapa é acrescentá-lo aqui, no mesmo
gesto, senão a régua passa a aprovar o que não sabe ler."* Acrescentar
`O JOGO RECEBEU` e `O JOGO REAGIU` exige, no mesmo gesto: (a) os dois valores no
domínio; (b) a regra que cobra ensaio para eles, como a regra 6 já faz para os
dois degraus fortes de hoje; (c) o vocabulário do caderno de ensaios para
registrá-los. **É trabalho de portão, e portão não se mexe numa página de
documentação.** Fica proposto aqui, com o desenho pronto, para a leva que o
implementar.

### 7.4 A prova de que isto não é opinião — a mordida do portão

> **NOTA DATADA — 19/08/2026, à tarde.** A primeira saída desta seção **não se
> reproduz mais**, e a razão é boa: os dois degraus ENTRARAM no domínio na
> mesma tarde, e `scripts/check_paridade_transporte.ESCADA` passou a ser o dono
> único do vocabulário (o `bancada.py` importa de lá; antes tinha a própria
> cópia, e era por isso que o portão podia aceitar um degrau que o formulário
> não oferecia).
>
> A medição abaixo **fica** porque explica por que a célula ficou em `MONTOU`
> naquele dia, e porque é ela que sustenta o desenho do que veio depois: hoje o
> portão exige ensaio no caderno para os dois degraus novos, igual aos de saída,
> e `O JOGO REAGIU` só fecha com `observado_por = olho-dela` — não existe régua
> nesta casa que leia o estado interno de um jogo sob Proton.
>
> A segunda saída (a do `grau-sem-ensaio`) continua valendo palavra por palavra.

Não basta afirmar que o degrau novo não cabe: dá para **ver o portão recusar**.
Escrevi `O JOGO RECEBEU` na linha `plataforma.vpad@dualsense` e rodei
`scripts/check_paridade_transporte.py`. Saída literal:

```
FALHA: 2 reprovação(ões) em mapa-controles.csv:
  FALHA integridade: linha 266 (plataforma.vpad@dualsense) [cabo]: `cabo_ate_onde_foi` fora do domínio: 'O JOGO RECEBEU'
  FALHA integridade: linha 266 (plataforma.vpad@dualsense) [radio]: `radio_ate_onde_foi` fora do domínio: 'O JOGO RECEBEU'
```

E, para provar que a rede está viva na linha que eu de fato editei, escrevi ali
o degrau mais forte que o domínio ACEITA — `O APARELHO OBEDECEU`, que seria a
tentação óbvia, já que o vpad demonstravelmente funciona:

```
FALHA: 2 reprovação(ões) em mapa-controles.csv:
  FALHA grau-sem-ensaio: linha 266 (plataforma.vpad@dualsense) [cabo]: declara
  `cabo_ate_onde_foi = O APARELHO OBEDECEU` e não há UM ensaio de cabo para
  `plataforma.vpad@dualsense` em docs/data/ensaios.csv. Registre o ensaio que você
  fez (uma linha: `linha_id`, `transporte`, `suspeito`, `presente`, `resultado`,
  `observado_por`) ou baixe o grau para `MONTOU`, que é o que a suíte sozinha
  sustenta
```

Cura devolvida (`MONTOU` nos dois lados), portão de volta em **exit 0**, e o
`git diff` do CSV voltou a ser exatamente as duas linhas que esta página
pretendia mudar. **É por isso que o degrau que ficou escrito é `MONTOU`:** não
por modéstia, mas porque é o único que a casa consegue provar hoje — e a régua
disse isso na minha cara duas vezes.

---

## 8. A ordem de atacar, se você pegou esta página primeiro

1. **`git log -1`.** Se você não está em `2706aaa` ou depois, pare e rebase.
2. **O `origem=` nas duas linhas de log** (§6.1). Uma palavra, e fecha a §4.3.
3. **Os quatro minutos do `medir_steam_virtual_gamepad.sh`** (§3.3, §6.5).
4. **Os dez lançamentos do jogo, cinco por Proton** (§3.2, §6.6).
5. **Rebase das três entregas e o corte da cura (2) do microfone** (§6.7).
6. Só então os dois degraus novos da escada (§7.3), que dependem de portão.

---

## 9. As páginas que esta noite deveria ter lido antes

Todas já existiam. Nenhuma foi consultada até o diagnóstico já estar errado.

- [A MÁSCARA QUE O PRODUTO ESCOLHE — 01](2026-08-16-A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01-o-jogo-nao-enxerga-e-a-culpa-nao-e-da-pessoa.md)
  — os dois defeitos que parecem um só, a medição do Unreal e a nota de
  honestidade sobre o `winebus`.
- [SENTINELA-WRAPPER-01](2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md)
  — a Steam guarda uma linha de `LaunchOptions` por jogo.
- [FOCO-ERRANTE-01](2026-08-18-FOCO-ERRANTE-01-o-x-aponta-para-a-steam-e-leva-o-perfil-junto.md)
  — a janela invisível da Steam que troca o perfil no meio da partida. É a mesma
  janela do `autoswitch_congelado_pelo_cadeado` da §4.3.
- [A pilha do Steam Input, do xpad e do SDL](../../protocol/pilha-steam-input-xpad-sdl.md)
  — o que fica ENTRE o controle e o jogo.
- `scripts/medir_steam_virtual_gamepad.sh` — o atalho do SDL, lido no fonte em
  11/08.
