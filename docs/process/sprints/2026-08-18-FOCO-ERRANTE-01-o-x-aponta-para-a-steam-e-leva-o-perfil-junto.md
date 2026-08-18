# FOCO-ERRANTE-01 — o X aponta para a Steam, e leva o perfil dela junto

- **Escrito em:** 18/08/2026, madrugada, com o jogo aberto na máquina dela e o
  defeito acontecendo **enquanto eu tirava as amostras**.
- **O que ela pediu, textual:** *"precisa virar sprint"*. E o sintoma, nas
  palavras dela: *"os gatilhos, a lightbar e o rumble do perfil do jogo estão
  saindo do ar enquanto você joga."*
- **Estado:** defeito **reproduzido ao vivo, com mecanismo nomeado e endereço no
  código**. Cura **projetada, nenhuma linha escrita**. Nada de `src/` foi tocado
  por esta passagem.
- **ATUALIZAÇÃO 18/08/2026 — a ONDA 1 está ESCRITA E TRAVADA** (passos 3, 4 e 5
  da §5). Ver a §5.1: o que entrou, onde, e a prova de mordida de cada trava.
  Falta o ensaio no aparelho (§8) e a decisão dela sobre a tela (passo 8).
- **Grau desta página:** as §1, §2 e §3 são **medidas nesta máquina hoje**, com o
  comando ao lado de cada número. A §4 em diante é projeto, e cada afirmação
  carrega o grau dela.

**Se você tem dois minutos:** leia a §1 e a §7. A §1 diz o que acontece; a §7
diz as quatro coisas que parecem a cura e não são — três delas estão medidas
como falsas.

---

## 1. O defeito, em cinco linhas

Ela joga. Uma janela **invisível do cliente Steam** — `WM_CLASS` de instância
`steamwebhelper`, **classe `steam`**, `WM_NAME` vazio — toma o foco do X por
alguns segundos. O detector de janela do daemon lê `steam`, o perfil
**Navegação** dela casa com `steam` no `window_class`, e o autoswitch troca o
perfil **no meio da partida**. Gatilhos e lightbar do jogo são reescritos pelos
do desktop. Segundos depois o foco volta para o jogo e tudo troca de novo.

**Treze trocas de perfil hoje**, entre 00:15 e 01:09, todas entre `Dont Scream`
e `Navegação` — e **toda** troca para `Navegação` traz `wm_class=steam`:

```
 1  00:15:17  None      -> Navegação      (steam)
 2  00:15:37  Navegação -> 'Dont Scream'  (steam_app_2497900)
 3  00:19:16  'Dont Scream' -> Navegação  (steam)
 4  00:24:12  None      -> Navegação      (steam)
 5  00:31:43  Navegação -> 'Dont Scream'  (steam_app_2497900)
 6  00:53:14  'Dont Scream' -> Navegação  (steam)
 7  00:56:33  Navegação -> 'Dont Scream'  (steam_app_2497900)
 8  01:03:30  'Dont Scream' -> Navegação  (steam)
 9  01:03:46  Navegação -> 'Dont Scream'  (steam_app_2497900)   <- 16 s depois
10  01:03:57  'Dont Scream' -> Navegação  (steam)               <- 11 s depois
11  01:04:41  Navegação -> 'Dont Scream'  (steam_app_2497900)   <- 44 s depois
12  01:04:46  'Dont Scream' -> Navegação  (steam)               <-  5 s depois
13  01:09:42  Navegação -> 'Dont Scream'  (steam_app_2497900)
```

**Cinco segundos** entre a linha 11 e a 12. Cada uma dessas linhas reescreve os
gatilhos e a barra do controle na mão dela.

O comando que reproduz a lista:

```bash
journalctl --user -u hefesto-dualsense4unix.service --since today -o short-iso \
  | grep profile_autoswitch
```

### 1.1 O que exatamente ela perde, e o que NÃO perde

Os dois perfis, lidos do disco dela agora (`~/.config/hefesto-dualsense4unix/profiles/`):

| seção | `Dont Scream` (prioridade 97) | `Navegação` (prioridade 50) | o que acontece na troca |
|---|---|---|---|
| gatilho esquerdo | `MultiPositionFeedback` | `Pulse` | **PERDIDO** — reescrito |
| gatilho direito | `Pulse` | `Pulse` | igual por acaso |
| lightbar | `129,61,156` brilho **1.0** | `97,53,131` brilho **0.4** | **PERDIDO** — cor e brilho |
| `mode` | `gamepad` + co-op | ausente | **PROTEGIDO** (`mode=ignorado_janela_de_jogo`) |
| `rumble.policy` | `balanceado` | `null` | **PROTEGIDO** (`rumble_policy=ignorado_janela_de_jogo`) |
| `speaker` | volume 99, rota 3 | ausente | não reaplicado na volta ao desktop |

E é isto que o próprio journal diz, na linha da troca:

```
secoes=['mode=ignorado_janela_de_jogo', 'modo_jogo_padrao=aplicado',
        'rumble_policy=ignorado_janela_de_jogo', 'suppression=aplicado']
```

> **Nota de honestidade, e ela corrige metade do enunciado:** o journal mostra
> que a **política de rumble sobreviveu** a todas as trocas de hoje — a guarda
> de 17/08 segurou. Gatilho e lightbar **não** têm guarda nenhuma e são
> reescritos. Se ela sentiu o rumble sumir também, isso é **outra medição**, e o
> suspeito de estante é o defeito do rádio já catalogado (vibração zero por BT,
> §1.2 de [ONDE PARAMOS](../2026-08-16-ONDE-PARAMOS-a-sessao-de-vinte-horas.md)).
> Esta sprint **não** afirma que a troca de perfil mata o rumble.

---

## 2. A medição que nomeia o culpado

Sonda **somente-leitura**, escrita para reproduzir linha a linha o que o
`XlibBackend` faz — `get_input_focus()`, subida na árvore até o primeiro
`WM_CLASS`, comparação com `_NET_ACTIVE_WINDOW`. Trinta amostras a 2 Hz, com o
jogo aberto, em 18/08 por volta de 01h04:

```
00..08  foco=0x26000e3 ('steamwebhelper','steam') nome=''            -> BACKEND: wm_class=steam
09..14  foco=0x5400001 ('steam_app_2497900',...) nome="DON'T SCREAM" -> BACKEND: wm_class=steam_app_2497900
15..19  foco=0            net_active=0x5400001                       -> BACKEND: None (sem_foco_x)
20..29  foco=0x26000e3 ('steamwebhelper','steam') nome=''            -> BACKEND: wm_class=steam
```

Três estados, e só o do meio é o certo. As duas janelas, medidas no mesmo
minuto:

```
0x26000e3  classe=('steamwebhelper','steam')  nome=''            1280x800+0+0   mapeada
0x5400001  classe=('steam_app_2497900', ...)  nome="DON'T SCREAM" 1920x1080+0+0 mapeada, FULLSCREEN
```

**O achado:** a janela que rouba o foco tem `WM_CLASS` de **instância**
`steamwebhelper` e de **classe** `steam`. O backend usa a **classe**
(`window_backends/xlib.py:318`, `wm_class_tuple[1]`) — logo o daemon recebe
literalmente `"steam"`, indistinguível da janela principal da loja. O `WM_NAME`
vazio é a assinatura: é uma janela CEF de serviço, não a loja que ela abriu.

### 2.1 As três causas de cegueira, e qual delas machuca

| leitura | quantas hoje | o que o produto faz | machuca? |
|---|---|---|---|
| `x11_focus_gate_no_x_focus` (`focus=0`) | **27 episódios** | histerese UX-01 retém o perfil corrente | **não** |
| `autoswitch_window_info_unavailable` | **18 episódios** | mesmo caminho, tick pulado inteiro | **não** |
| leitura ÚTIL, mas da janela ERRADA (`steam`) | **7 trocas** | troca de perfil, reescreve gatilho e barra | **SIM** |
| `x11_foco_discorda_do_net_active` | **zero** | — | — |

Contagem: `journalctl --user -u hefesto-dualsense4unix.service --since today | grep -oE '<evento>' | wc -l`.

> **O enunciado que chegou até mim dizia *"o daemon não enxerga a janela do
> jogo"*. Ele enxerga — de forma intermitente. O que faz o estrago é o
> contrário: ele enxerga uma janela e ela é a errada.** A cegueira (`focus=0`)
> é real, está medida, e é **inofensiva**: a histerese UX-01
> (`profiles/autoswitch.py:304`) pula o tique inteiro e retém o perfil. Foi
> desenhada em 16/07 exatamente para isto.

### 2.2 A hipótese, e ela explica o que JÁ funcionava

**Enunciado (grau: medido para a metade observável, `inferido` para a causa):**

> Sob XWayland no cosmic-comp, o **foco de entrada do X** não responde à
> pergunta que o autoswitch faz. Ele responde *"qual cliente X receberia a tecla
> se o mundo X tivesse o foco"*. Quando a superfície focada no compositor é
> **Wayland nativa** (o terminal, a janela do Hefesto, o navegador), o foco do X
> ou é `0` — e aí o produto se protege — ou é **um cliente X qualquer**, e aí o
> produto acredita.

**Por que funciona a maior parte do tempo:** enquanto a superfície focada É a
janela do jogo (que é um cliente X), o foco fica preso nela, a leitura é
correta, e todo o autoswitch por jogo funciona como sempre funcionou. Foi assim
às 00:15:37, 00:31:43, 00:56:33, 01:03:46, 01:04:41 e 01:09:42 — seis entradas
corretas no perfil do jogo, hoje. **A hipótese não derruba nada que funcionava:
ela explica por que o mesmo mecanismo acerta e erra no mesmo minuto.**

**O que falta medir para fechar a hipótese (é o E-1 da §8):** não consigo, dos
dados de hoje, separar *"o foco passeia sozinho"* de *"ela alternou de janela"*.
Ela estava usando a máquina o tempo todo enquanto eu amostrava — inclusive com o
diálogo **Testar Entradas do Dispositivo** da Steam aberto, que é uma janela
`steamwebhelper`. O ensaio que separa os dois custa **dois minutos com as mãos
fora do teclado**.

---

## 3. O endereço no código, linha a linha

| o que | onde | o que faz |
|---|---|---|
| o gate de foco do X | `integrations/window_backends/xlib.py:273-278` | `focus in (X.NONE, X.PointerRoot)` → `None` + `x11_focus_gate_no_x_focus` |
| a subida na árvore até o `WM_CLASS` | `integrations/window_backends/xlib.py:183` | acha o top-level do foco REAL |
| a classe que sai daí | `integrations/window_backends/xlib.py:318` | `wm_class_tuple[1]` — a **classe**, nunca a instância |
| a corroboração com `_NET_ACTIVE_WINDOW` | `integrations/window_backends/xlib.py:308` | discordância vira `None` (zero ocorrências hoje) |
| quem escolhe o backend | `integrations/window_detect.py:194` | **`DISPLAY` presente vence sempre** — a cascata Wayland nunca é construída nesta máquina |
| o tique cego | `profiles/autoswitch.py:304-319` | `_tick_sem_informacao` / `_janela_propria` → pula o tique |
| o predicado do tique cego | `profiles/autoswitch.py:532` | `unknown` + sem título + sem processo |
| o debounce de entrada | `profiles/autoswitch.py:43` | **0,5 s** — dois tiques bastam |
| o debounce lento | `profiles/autoswitch.py:59` e `:492` | 12 s, **só** para sair rumo a um catch-all. `Navegação` é `criteria`, não catch-all: **não paga** |
| a ativação | `profiles/autoswitch.py:583` (`_activate`) → `profiles/manager.py:208` (`activate`) | |
| quem reescreve gatilho e LED **sem guarda nenhuma** | `profiles/manager.py:274` (`apply`) | só a trava manual dela sobrevive |
| a guarda que SEGUROU o modo | `daemon/lifecycle.py:1970` (`_janela_de_jogo_em_foco`) | consultada em `:2237` (modo) e `:2693` (rumble) |
| o predicado da janela do cliente | `profiles/steam_app.py:61` (`e_janela_do_cliente_steam`) | reconhece `steam` **e** `steamwebhelper` |
| o log da troca | `profiles/autoswitch.py:683` | `profile_autoswitch` com `secoes=` |

**A ironia que orienta a cura:** a guarda de 17/08
(`VPAD-NA-JANELA-DA-STEAM-01`) já sabe que *"a janela da Steam durante a partida
não autoriza voltar ao desktop"*. Ela é consultada **depois** da troca, para
salvar o modo e o rumble. **Ninguém a consulta ANTES, para não trocar.**

---

## 4. As opções de cura, com preço — e três já estão medidas como falsas

### Opção A — usar `_NET_ACTIVE_WINDOW` no lugar do foco do X

**REFUTADA HOJE, nesta máquina.** Amostragem de 60 s, imprimindo só as
transições:

```
+   0.0s  foco=(sem foco X)  net_active=steam      <- 54 segundos assim
+  54.5s  foco=steam         net_active=steam
+  57.0s  foco=(sem foco X)  net_active=None
+  58.6s  foco=steam         net_active=steam
```

Com o jogo vivo, o `_NET_ACTIVE_WINDOW` apontou para a **janela do cliente
Steam** por 54 segundos seguidos. Trocar o gate por ele daria a resposta
**errada de forma mais estável** — o daemon leria `steam` continuamente em vez
de intermitentemente. E some-se o que a casa já tinha medido duas vezes, ao
vivo, e escreveu em `window_backends/xlib.py:245-255`: o `_NET_ACTIVE_WINDOW`
fica **rançoso** no cosmic-comp, chegando a apontar para janela X **morta**.

**Preço:** 3 linhas. **Risco:** reabre o pingue-pongue de 18-28 s de 22-23/07,
que foi o que originou o gate. **Veredito: não fazer.**

### Opção B — perguntar ao compositor (protocolo wlr / COSMIC)

**Metade REFUTADA HOJE.** O `wlrctl` **está instalado** (`/usr/bin/wlrctl`) e o
cosmic-comp responde:

```
$ WAYLAND_DISPLAY=wayland-1 wlrctl toplevel list
Foreign Toplevel Management interface not found!
```

Ou seja: `window_backends/wlr_toplevel.py` está correto e **morto nesta
máquina** — o marcador que ele procura (`:48`) é exatamente esta frase, e ele se
marca indisponível de vez (`:132`). Sobra o protocolo próprio do COSMIC,
`zcosmic_toplevel_info_v1`, que **é** a régua certa: quem sabe qual toplevel
está ativado é o compositor, e a resposta dele vale para janela X e Wayland
igualmente.

**Preço:** alto. Não há `pywayland` na máquina (`ModuleNotFoundError`), o
protocolo é XML próprio do COSMIC, e entra dependência nova no
`install.sh`/empacotamento — que é justamente o que o item **I-3** de
[ONDE PARAMOS](../2026-08-16-ONDE-PARAMOS-a-sessao-de-vinte-horas.md) §6.4
manda declarar. Some-se o **PROCESSO-CEGO-01**: backend que não é o `xlib` não
entrega `exe_basename`, e perfil com `process_name` **nunca casa** nele
(`integrations/window_detect.py:62-63`).

**E o mais importante: ela não resolve a queixa dela sozinha.** Um compositor
perfeitamente honesto diria *"a janela ativada agora é a Steam"* — e o perfil
trocaria do mesmo jeito quando ela fosse conferir uma conquista no meio da
partida. **Veredito: vale, é a régua certa, mas é ONDA 2 — e depende de um
ensaio próprio antes de uma linha de código.**

### Opção C — o processo do jogo, pelo marcador do wrapper

A casa já tem o sinal: `launch_session_appid()`
(`daemon/launch_env.py:618`) devolve o appid do jogo lançado pelo wrapper que
**ainda está rodando** — marcador em disco + PID vivo, imune a alt-tab e a
restart do daemon.

**A ARMADILHA, e ela está medida:** essa função exige que o marcador `last_run`
seja **fresco**, com janela `WRAPPER_MARKER_WINDOW_SEC = 900` segundos
(`daemon/launch_env.py:320`). Lido do disco dela hoje:

```
$ cat ~/.local/state/hefesto-dualsense4unix/launch_env/last_run
appid=2497900
epoch=1787023898      <- 00:31:38, o lançamento
pid=38036
                       (last_exit: não existe)
```

O perfil foi roubado às **00:53:14**. Idade do marcador naquele instante:
**1296 s**, contra uma janela de 900 s. **`launch_session_appid()` teria
respondido `None` — a cura conservadora, construída de forma ingênua em cima da
função que já existe, NÃO teria evitado o defeito.** E aos 37,9 minutos de
partida ela continuaria respondendo `None`.

Os 900 s existem por um motivo bom (descartar o marcador do jogo de ontem), e a
correção é trocar o critério, não afrouxar o número: **quem descarta marcador
velho é o PID morto**, e a corroboração é de graça — a linha de comando do
processo do marcador contém `AppId=<appid>`:

```
38036 .../reaper SteamLaunch AppId=2497900 -- ... DontScream-Win64-Shipping.exe
```

**Preço:** uma função pura nova ao lado de `wrapper_game_running`
(`daemon/launch_env.py:498`), com leitura de `/proc/<pid>/cmdline` para matar o
risco de PID reciclado. ~40 linhas com docstring. **Risco:** jogo que trava sem
morrer segura o perfil — mitigado pela corroboração e pelo fato de o PID do
`reaper` morrer junto com a árvore do jogo.

### Opção D — não reverter enquanto houver jogo vivo (a conservadora)

É a opção C aplicada no ponto de decisão. Concretamente, em
`profiles/autoswitch.py`, antes da ativação: **se o candidato casou APENAS pela
janela do cliente Steam, e o perfil corrente é a regra própria de um jogo que
ainda está VIVO, não troca.**

**O falso positivo que ela não pode ter** — e é o que separa esta cura de uma
gambiarra: se a guarda fosse só *"a janela é a da Steam"*, ela fecharia o jogo,
ficaria na biblioteca da Steam e o perfil do jogo ficaria **preso para sempre**.
Por isso o termo de vitalidade é obrigatório, e por isso a mordida nº 2 da §6
existe.

**Preço:** ~15 linhas no autoswitch + a função da opção C + um evento de journal
deduplicado. **Risco:** com o jogo vivo, ir para a Steam mantém gatilho e cor do
jogo. É exatamente o que a decisão dela de 17/08 já escolheu para o modo — *"a
janela da Steam é o lugar mais comum de se estar durante a partida"*
(`daemon/lifecycle.py:1996`).

### A recomendação

**D + C agora (ONDA 1), B depois de um ensaio (ONDA 2).**

O que decide é a assimetria que esta casa já usa em três lugares — UX-04,
UX-01 e PARTIDA-PICOTADA-01: **barato para entrar no perfil do jogo, caro para
sair dele.** A ONDA 1 fecha o sangramento de hoje com material que já existe na
árvore, sem dependência nova e sem tocar no gate de foco (que está certo pelo
motivo pelo qual nasceu). A ONDA 2 troca a régua, e só ela sobrevive a um
desktop Wayland puro.

### A cura de ZERO linhas, e a decisão é dela

Tirar `steam` e `Steam` da lista `window_class` do perfil **Navegação**
(o arquivo é dela; **eu não edito perfil dela**) faria o defeito sumir hoje.
**Preço:** ela perde o perfil de desktop enquanto navega na loja da Steam.
Registro porque é honesto ter isso na mesa enquanto a cura de verdade é
construída — e porque a pergunta de produto que vem junto é dela: **um perfil de
desktop deveria poder casar com `steam`?**

---

## 5. A ordem de execução

Cada passo é pequeno, tem um comando que o valida, e nenhum depende do seguinte
para valer alguma coisa.

| # | o que fazer | o comando que valida |
|---|---|---|
| **1** | **O instrumento.** Portar a sonda desta sprint para `scripts/ensaios/foco_errante.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha -->: amostra `get_input_focus()`, sobe a árvore, compara com `_NET_ACTIVE_WINDOW`, imprime **só as transições**, e declara no cabeçalho que é **somente-leitura**. É a régua que faltou hoje | rodar com o jogo aberto: tem de imprimir pelo menos uma transição `steam`/`steam_app_*` |
| **2** | **A honestidade no journal.** `WindowInfo` (`integrations/window_backends/base.py`) ganha `wm_instance`, preenchido só pelo `xlib`. Sem ele, `steamwebhelper` e a loja da Steam são a mesma linha no journal e ninguém consegue ler o defeito sem uma sonda | `pytest -q tests/unit/test_window_backends.py` |
| **3** | **O sinal de vitalidade.** `jogo_do_wrapper_vivo()` em `daemon/launch_env.py`, ao lado de `wrapper_game_running` — PID vivo **e** `AppId=<n>` na linha de comando do processo, **sem** janela de frescor. Função pura + uma leitura de `/proc` | mordidas 5 e 6 da §6 |
| **4** | **A guarda.** No `_tick` de `profiles/autoswitch.py`, antes do bloco de estabilidade: candidato que casou só pela janela do cliente Steam, perfil corrente sendo a regra própria de um jogo vivo → **não troca**. Reusar `e_janela_do_cliente_steam` (`profiles/steam_app.py:61`) — nada de sexta implementação do mesmo predicado | mordidas 1 a 4 da §6 |
| **5** | **O rastro.** Evento `autoswitch_recusou_a_janela_da_steam` com `candidato`, `perfil_corrente`, `appid`, **1x por episódio** (mesmo padrão de `_log_suppressed_once`, `profiles/autoswitch.py:706`). O poll é 2 Hz: sem dedup são 7 200 linhas/hora | mordida 7 da §6 |
| **6** | **Os portões.** `git add -A` **antes**, porque os portões são cegos a arquivo novo | o bloco inteiro de "Antes de fechar qualquer leva" do `CLAUDE.md` |
| **7** | **O ensaio no aparelho** | §8 |
| **8** | **A tela.** Só depois do ensaio, e é decisão dela: a aba No jogo mostrar *"o perfil do jogo está protegido"*. [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md) — foto antes e depois, e a palavra final é dela | `scripts/gui-captura/retratar_abas.py` |

## 5.1 O que a ONDA 1 entregou — 18/08/2026

**Passos 3, 4 e 5, escritos e travados.** Dois arquivos, mais nada de `src/`:

| o que | onde | nota |
|---|---|---|
| `jogo_do_wrapper_vivo()` | `profiles/autoswitch.py` | **não** em `daemon/launch_env.py`, como a §5 previa: aquele arquivo estava em edição por outra frente na mesma árvore. Reusa `wrapper_game_running` com `window_sec=inf` — a janela de frescor é o ÚNICO termo que sai, e a correlação por pid do NUMA-01 continua valendo byte a byte |
| `_cmdline_confirma_appid()` | `profiles/autoswitch.py` | a corroboração que ENTRA no lugar dos 900 s: `AppId=<n>` na `argv` do processo do marker, sem prazo de validade |
| `_appids_de_jogo_do_perfil()` | `profiles/autoswitch.py` | os appids de que o perfil corrente é a regra própria, pelo predicado ÚNICO (`steam_app.steam_appid_from_wm_class`) — nada de um sexto predicado |
| a guarda | `AutoSwitcher._recusa_a_janela_do_cliente_steam`, chamada no `_tick` antes do bloco de estabilidade | três termos obrigatórios: janela do cliente Steam (por `steam_app.e_janela_do_cliente_steam`) + perfil corrente é regra própria de um jogo + esse jogo está vivo |
| o rastro | evento `autoswitch_recusou_a_janela_da_steam` | `candidato`, `perfil_corrente`, `appid`, `wm_class`; 1x por episódio, mesma chave do `_log_cadeado_uma_vez` |
| as travas | `tests/unit/test_foco_errante_01_a_janela_da_steam_nao_tira_o_perfil.py` | 21 testes |

**Nenhuma rota de subida do daemon precisou de fio novo:** o campo
`jogo_vivo_reader` do `AutoSwitcher` nasce `None` e cai em
`jogo_do_wrapper_vivo()` com os diretórios reais. O campo existe só para o teste
apontar a leitura para um `tmp_path` — mesmo motivo do `base_dir` das funções de
marker do `launch_env`.

**A prova de mordida**, cura por cura (arrancar → reprovar → devolver):

| a cura arrancada | quantos reprovam | os que reprovam |
|---|---|---|
| a guarda inteira do `_tick` | **6** | o defeito de 18/08 volta: o perfil troca, a lightbar é reescrita, o journal registra a troca |
| o termo de VITALIDADE (guarda só por `wm_class`) | **6** | é a mordida nº 2 — o cadeado permanente, que é PIOR que o defeito |
| o predicado da janela da Steam (guarda para qualquer janela) | **1** | `test_janela_de_outro_app_troca_o_perfil_mesmo_com_o_jogo_vivo` |
| a igualdade de appid (guarda cruzada) | **1** | `test_a_guarda_so_vale_para_o_jogo_do_perfil_corrente` |
| `window_sec=math.inf` (volta aos 900 s, = `launch_session_appid`) | **2** | é a mordida nº 5, com o número medido de **1296 s** |
| a corroboração por `AppId=` | **2** | é a mordida nº 6 — um PID vivo qualquer passaria a valer por jogo |
| a chave de dedup da recusa | **2** | é a mordida nº 7 — 2 Hz viram uma linha por tique |
| o reset da chave no fim do episódio | **1** | dedup virando silêncio, o irmão do `BUG-AUTOSWITCH-LOG-KEY-STUCK-01` |

**O que NÃO entrou nesta passagem, e por quê:**

- **passo 1** (o instrumento, `scripts/ensaios/foco_errante.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha -->)
  e **passo 2** (`wm_instance` no `WindowInfo`) — moram em `integrations/`, fora
  da frente desta passagem;
- **passo 7** (o ensaio no aparelho) — precisa das mãos dela, e o daemon vivo é
  mais velho que o código: vale só depois de
  `systemctl --user restart hefesto-dualsense4unix` (armadilha nº 8 da §7);
- **passo 8** (a tela) e a **cura de zero linhas** (tirar `steam` do
  `navegacao.json`) — são decisão dela, e ela ainda não foi dada;
- **ONDA 2** (backend COSMIC) — inalterada, e continua dependendo de um ensaio
  próprio antes de uma linha de código.

---

## 6. As travas — o que cada teste MORDE

Arquivo: `tests/unit/test_foco_errante_01_a_janela_da_steam_nao_tira_o_perfil.py`.
Molde: `tests/unit/test_partida_picotada_01.py`, que já resolve esta mesma
família (tique cego não encerra a exceção) com dublês minúsculos.

> **ESCRITO em 18/08/2026** — as sete travas abaixo existem, mais catorze
> guardas, e a prova de mordida de cada uma está na §5.1.

| # | nome do teste | o que MORDE | arranque isto → tem de reprovar |
|---|---|---|---|
| 1 | `test_a_janela_do_cliente_steam_nao_troca_o_perfil_com_o_jogo_vivo` | o defeito inteiro | tire a guarda do `_tick`: com `wm_class="steam"`, jogo vivo e `Dont Scream` corrente, o perfil troca para `Navegação` |
| 2 | `test_sem_jogo_vivo_a_janela_da_steam_troca_normalmente` | **o falso positivo, que é pior que o defeito** | tire o termo de vitalidade (guarda só por `wm_class`): com o jogo MORTO o perfil fica preso no do jogo, e o teste reprova |
| 3 | `test_janela_de_outro_app_troca_o_perfil_mesmo_com_o_jogo_vivo` | a política de 23/07 | alargue a guarda para qualquer janela: `firefox` deixa de trocar o perfil e reprova. É o irmão do `test_perfil_especifico_fora_de_jogo_reverte_normalmente` |
| 4 | `test_a_guarda_so_vale_para_o_jogo_do_perfil_corrente` | guarda cruzada | marcador do appid A não pode segurar o perfil do jogo B |
| 5 | `test_o_jogo_vivo_nao_expira_aos_quinze_minutos` | **a armadilha da §4-C** | troque `jogo_do_wrapper_vivo()` por `launch_session_appid()`: com marcador de **1296 s** — o número medido às 00:53:14 — a guarda some e o teste reprova |
| 6 | `test_pid_reciclado_nao_segura_o_perfil` | o risco que a janela de 900 s cobria | tire a corroboração por `AppId=` na linha de comando: um PID vivo qualquer passa a valer por jogo |
| 7 | `test_a_recusa_loga_uma_vez_por_episodio` | inundação do journal | tire a chave de dedup: 2 Hz produzem uma linha por tique |

Para o passo 2, arquivo
`tests/unit/test_foco_errante_02_o_journal_nomeia_a_janela_que_roubou.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha -->:
o `xlib` preenche `wm_instance="steamwebhelper"` com `wm_class="steam"`, e os
outros backends o deixam vazio — arrancar o preenchimento faz as duas janelas da
Steam voltarem a ser indistinguíveis.

**A regra da casa vale inteira:** arranque, veja reprovar, devolva. Teste que
passa com a cura arrancada não testa nada.

---

## 7. O que NÃO fazer — as armadilhas deste código

1. **Não troque o gate de foco por `_NET_ACTIVE_WINDOW`.** Medido hoje: aponta
   para a janela da Steam por 54 s seguidos com o jogo vivo. E a casa já o
   mediu rançoso duas vezes (`window_backends/xlib.py:245-255`).
2. **Não use `launch_session_appid()` como está.** Ela expira em 900 s
   (`daemon/launch_env.py:320`) e já estava expirada no instante do defeito.
3. **Não use `display_authority == "game"` como guarda.** O sinal é sticky e tem
   defeito **conhecido e não corrigido** — cai para `daemon` ~30 s depois com o
   jogo aberto. A recusa está escrita, com o porquê, em
   `daemon/lifecycle.py:2039`.
4. **Não transforme a guarda em cadeado permanente.** Perfil de jogo preso para
   sempre é pior que o defeito. É a mordida nº 2, e ela não é opcional.
5. **Não escreva um sexto predicado de "isto é janela da Steam".**
   `profiles/steam_app.py` nasceu de cinco implementações que discordavam entre
   si. A resposta é importar de lá.
6. **Não conserte isto mexendo no perfil dela.** `navegacao.json` é dado dela.
   Tirar `steam` de lá é decisão dela, e está na §4.
7. **Não presuma que a cascata Wayland roda nesta máquina.**
   `integrations/window_detect.py:194` devolve `XlibBackend` sempre que há
   `DISPLAY` — e o daemon dela tem `DISPLAY=:1` **e** `WAYLAND_DISPLAY=wayland-1`
   (lido do `/proc/<pid>/environ` do serviço). O portal e o `wlrctl` nunca são
   nem construídos.
8. **O daemon vivo é mais velho que o código.** Instalação editable: a cura só
   vale no **próximo** `systemctl --user restart hefesto-dualsense4unix`, e o
   sintoma de esquecer isso é a **ausência** do evento novo no journal.
9. **Não clique por coordenada para focar janela.** Já caiu noutro aplicativo
   duas vezes e um clique cego já desfez configuração dela
   ([COMO-OLHAR-A-TELA](../COMO-OLHAR-A-TELA.md)).
10. **Rode os portões DEPOIS do `git add`** — eles são cegos a arquivo novo.

---

## 8. O ensaio no aparelho — UM gesto por vez

Regra da casa desde 16/08: **um ensaio mede um gesto**. Gesto composto produz
ausência falsa. Terminal deixado pronto antes de começar:

```bash
journalctl --user -u hefesto-dualsense4unix.service -f -o short-iso \
  | grep -E 'profile_autoswitch|autoswitch_recusou|x11_focus_gate|window_info_unavailable'
```

| # | o gesto | duração | o que tem de aparecer |
|---|---|---|---|
| **E-1** | **nenhum.** Jogo aberto em primeiro plano, **mãos fora do teclado e do mouse**. Rodar `scripts/ensaios/foco_errante.py` <!-- ref-externa: arquivo a CRIAR, é o assunto da linha --> por 120 s | 2 min | **É o ensaio que fecha a hipótese da §2.2.** Transição `steam_app_*` → `steam` **sem gesto nenhum** = o foco passeia sozinho. Zero transições = era alt-tab dela, e a cura continua a mesma, mas a página muda de tom |
| **E-2** | ela clica **uma vez** no jogo e não faz mais nada | 1 min | foco estável em `steam_app_2497900`; **zero** `profile_autoswitch` em 60 s |
| **E-3** | ela clica **uma vez** na janela da Steam, com o jogo vivo atrás | 1 min | **com a cura:** `autoswitch_recusou_a_janela_da_steam` e **zero** `profile_autoswitch`. E o olho dela decide: a barra tem de continuar no **roxo forte do jogo** (`129,61,156`, brilho 1.0) e não cair no roxo apagado do desktop (`97,53,131`, brilho 0.4) |
| **E-4** | ela **fecha o jogo** e depois foca a Steam | 1 min | **em ~1 s:** `profile_autoswitch to=Navegação`. É a prova de que a guarda **solta**. Sem esta linha, a cura virou cadeado |
| **E-5** | ela abre o Firefox com o jogo vivo | 1 min | `profile_autoswitch to=Navegação` **normalmente**. A guarda é só para a Steam |

O par que decide tudo é **E-3 contra E-4**: mesma janela da Steam, mesma
máquina, mesmo minuto, **uma variável só** — o jogo vivo ou morto.

---

## 9. O vizinho, e ele NÃO é escopo desta sprint

Medido hoje, mesma família (*"a casa sabe e o produto não faz"*), **sem dono**:

`_avisar_se_o_jogo_ja_congelou` (`daemon/launch_env.py:1201`) grita
`launch_env_mudou_depois_do_exec` no journal (`:1226`) quando a mesa muda depois
que o jogo já subiu — o jogo congelou a env no `exec` do wrapper e a regravação
só vale para o **próximo** lançamento. **Esse aviso nunca chega à janela.** Ela
não tem como saber que ligar um controle no meio da partida não alcança o jogo
que está rodando.

É a mesma classe do **G-1/G-2** de
[ONDE PARAMOS](../2026-08-16-ONDE-PARAMOS-a-sessao-de-vinte-horas.md) §6.4, e a
mesma regra dela de 09/08: *tudo tem que chegar na interface e no install.*
**Fica registrado aqui com endereço, e não entra nesta leva.**

---

## 10. O que esta página RECUSA afirmar

- **Que o foco passeia sozinho.** É a leitura mais provável dos dados, e o E-1
  a decide em dois minutos. Ela estava usando a máquina enquanto eu amostrava, com
  um diálogo `steamwebhelper` aberto — não dá para separar daqui.
- **Que a troca de perfil apaga o rumble.** O journal diz o contrário: a
  política de rumble foi **protegida** em todas as trocas de hoje. Gatilho e
  lightbar, sim.
- **Que o gate de foco do X está errado.** Ele está certo pelo motivo pelo qual
  nasceu, e removê-lo reabre um defeito medido em 22-23/07.
- **Que o backend do COSMIC resolve a queixa dela.** Ele resolve a **régua**.
  Com ele, alternar para a Steam continuaria trocando o perfil — a guarda da
  ONDA 1 continua necessária.
- **Que o `steamwebhelper` é o único ladrão de foco possível.** É o único que
  apareceu nas trinta amostras de hoje.
- **Que estes números valem fora desta máquina.** Tudo aqui é COSMIC +
  cosmic-comp + XWayland `:1` + GE-Proton10-34. O que vale em qualquer lugar é a
  forma do defeito, não os identificadores de janela.

---

## 11. A frase para levar

> **Cego, o produto se protege. Vendo a janela errada, ele obedece.**
> A histerese de 16/07 cobre a ausência de dado; nada cobre o dado errado.
