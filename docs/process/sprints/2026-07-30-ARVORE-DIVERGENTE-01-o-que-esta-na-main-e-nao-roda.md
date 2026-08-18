# ÁRVORE-DIVERGENTE-01 — o que está na `main` e não roda

- **Status:** ABERTA
- **Aberta em:** 30/07/2026, depois da publicação da v0.4.0, a pedido dela:
  *"materializa as 3 faixas pra atacarmos depois de reiniciarmos"*
- **Pedido dela:** saber o que ficou do outro lado da divergência entre a ref
  local `main` e a árvore que roda, e o que ainda vale trazer
- **Impacto:** MÉDIO-ALTO. Um dos commits perdidos é a simetria do instalador,
  e as curas que ele rearma estão **desligadas nesta máquina agora** (medido
  abaixo). Os outros três são função que a interface promete e não entrega. E a
  ref local é uma armadilha armada: `git checkout main` aqui devolve a árvore de
  26/07, não a de hoje

---

## O que foi medido

Todos os números desta seção saíram de comandos rodados nesta máquina em
30/07/2026, depois da tag v0.4.0.

### A divergência, em números

```
git rev-list --left-right --count main...HEAD   ->  17    24
git merge-base main HEAD                        ->  4dd4652
git rev-parse main                              ->  2d8527a
git rev-parse HEAD                              ->  e74077c
git rev-parse origin/main                       ->  e74077c
```

| Ref | Commit | Data |
|---|---|---|
| ponto comum (`merge-base`) | `4dd4652` | 25/07/2026 22:36 |
| `main` — ref **local** | `2d8527a` | **26/07/2026 05:36** |
| `HEAD` (`restauro/inicio-da-sessao`) | `e74077c` | 30/07/2026 14:16 |
| `origin/main` (o remoto dela) | `e74077c` | 30/07/2026 14:16 |
| `upstream/main` (AndreBFarias) | `398d3ed` | 05/05/2026 |

**17 commits estão só na `main` local. 24 estão só aqui.** A árvore andou 24
commits desde o ponto comum — é esse o número que decide o método de porte.

### A ref local rastreia o upstream, não o repositório dela

```
git config branch.main.remote   ->  upstream
git config branch.main.merge    ->  refs/heads/main
git branch -vv                  ->  main  2d8527a [upstream/main: ahead 315]
```

`upstream` é `https://github.com/AndreBFarias/hefesto-dualsense4unix.git`;
`origin` é `git@github.com-personal:[REDACTED]/...`. Três consequências,
todas medidas:

1. **`git checkout main` nesta máquina entrega a árvore de 26/07/2026, 05h36** —
   quatro dias e vinte e quatro commits atrás do que ela usa. E a árvore de
   trabalho é o que roda: o daemon e a GUI dela leem daqui.
2. **`git push` a partir de `main` mira o repositório de outra pessoa.** Não há
   `push.default` nem `remote.pushDefault` configurados (`git config` devolve
   vazio nos dois), então o destino é o `branch.main.remote` — `upstream`.
3. `git pull` na `main` não é o risco: `upstream/main` (`398d3ed`, 05/05) é
   **ancestral** de `HEAD` (`git merge-base HEAD upstream/main` devolve o
   próprio `398d3ed`). O upstream está 315 commits atrás, não à frente.

### Nada ficou inalcançável

```
git tag --points-at 2d8527a  ->  arquivo/main-antes-da-v030
```

A tag anotada `arquivo/main-antes-da-v030` aponta exatamente para o topo da
`main` local, e a anotação registra a decisão dela de 29/07 às 03h. Ou seja: a
ref local `main` não é a única coisa que segura esses 17 commits — a tag segura.

### O reflog diz que a ref nunca foi tocada depois

```
git reflog show main | head -1  ->  2d8527a main@{0}: commit: fix(release): a
                                    v0.1.2 saiu com cinco arquivos de
                                    empacotamento dizendo 0.1.1
```

A última entrada do reflog de `main` é o **próprio commit** de 26/07. Não há
`checkout`, `reset` ou `branch -f` depois disso. A ref não foi movida para lugar
nenhum de propósito; ela simplesmente parou onde estava.

### As curas de módulo estão desligadas AGORA

Lido em 30/07, com o daemon vivo e o controle no cabo:

```
/sys/module/hid_playstation/parameters/ds4_short_pairing_info  =  N
/sys/module/hid_playstation/parameters/ds4_synthetic_mac       =  N
/sys/module/hid_playstation/parameters/feature_retries         =  0
/sys/module/rtw88_usb/parameters/hang_reset                    =  N
/sys/module/hid_nintendo                                       =  não existe
```

E o portão que deveria reaplicá-las é falso para ela:

```
ls -l /sys/module/hid_playstation/parameters/
   -rw-r--r-- 1 root root  ds4_short_pairing_info
id -un                                            ->  vitoriamaria
[ -w /sys/module/hid_playstation/parameters/ds4_short_pairing_info ]
                                                  ->  falso
```

### A assimetria do instalador, medida no texto dos dois scripts

Reproduzindo em `.venv/bin/python` a regra que o commit `9c944a8` cobrava
(casar a **escrita** `| sudo tee /sys/module/...`, não a menção):

```
portões `-w` em /sys/module no install.sh:
  /sys/module/hid_nintendo/parameters/bt_probe_retries        (install.sh:620)
  /sys/module/hid_playstation/parameters/feature_retries      (install.sh:686)
  /sys/module/hid_playstation/parameters/ds4_short_pairing_info (install.sh:696)
  /sys/module/hid_playstation/parameters/ds4_synthetic_mac    (install.sh:700)

params que o uninstall DESARMA e o install NUNCA rearma:
  hid_nintendo/parameters/usb_cmd_pad_to_report   (uninstall.sh:821)
  hid_nintendo/parameters/usb_send_conn_status    (uninstall.sh:822)
  hid_nintendo/parameters/usb_probe_degrade       (uninstall.sh:823)
  rtw88_usb/parameters/hang_reset                 (uninstall.sh:860)
```

São **quatro órfãos** (sem uma linha de rearme no `install.sh`) mais **cinco
params atrás de portão morto** — o bloco de `install.sh:620` escreve dois
(`bt_probe_retries` e `skip_tx_on_rate_exceeded`), e `:686`, `:696` e `:700`
escrevem um cada. Nove params ao todo. O commit original contava seis; a conta
subiu porque o `uninstall.sh` de hoje desarma mais coisa do que o de 26/07.

### O que a árvore de hoje já tem, e que eu confirmei antes de escrever

- **`3a41cdf` (acentos que deixavam a CI vermelha):** presente.
  `src/hefesto_dualsense4unix/daemon/udp_server.py:238` já diz *"não
  implementado"*, com os três acentos.
- **`84d9f4e` (`doctor --fix-mic`):** **portado**.
  `git diff 84d9f4e:tests/unit/test_doctor_mic_camada2.py
  HEAD:tests/unit/test_doctor_mic_camada2.py` devolve **vazio** — o arquivo é
  idêntico byte a byte. E o `scripts/doctor.sh` foi além: o critério virou a
  **porta de captura** (`:1003`, `:1010`, `:1017`) e o veredito do monitor saiu
  do `pass` de `:446` para o portão próprio `check_default_source_monitor`
  (`:605`).
- **`d309e79` (o retrato das nove abas e as três sprints):** presente. Os cinco
  documentos chegaram aqui por `7364da8`
  (`git log --diff-filter=A -- docs/process/estudos/2026-07-26-retrato-das-nove-abas.md`).
- **A cegueira do gate de acentuação a f-string:** curada.
  `scripts/validar-acentuacao.py:595-619` trata `FSTRING_MIDDLE`. A sprint que
  pedia isso (AUTO-04 / GATE-FSTRING-01) nunca chegou aqui, e a cura chegou
  assim mesmo.
- **`a46941d` + `2d8527a` (release v0.1.2 e a versão nos pacotes):** superados.
  `pyproject.toml:7` diz `0.4.0` e existe `scripts/check_version_consistency.py`
  como portão.
- **A contradição de contagem entre cabeçalho, chips e aba Status:** curada por
  outro caminho, em 29/07, como CONTAGEM-E-COOP-01 —
  `src/hefesto_dualsense4unix/app/actions/status_actions.py:85` (a dataclass
  `ContagemDeControles`) e `:126` (`texto_de_contagem`).
- **A faixa de microfone:** entregue na direção que ela pediu, e não na do
  `ef4b8bc`. Hoje o microfone está **dentro** do card, à direita dos analógicos
  — `src/hefesto_dualsense4unix/app/widgets/controller_card.py:24` e `:36`.

---

## A causa

Não é acidente de merge. São dois eventos separados, e é importante não
confundi-los.

**O primeiro é um rollback pedido por ela, em 26/07.** A branch se chama
`restauro/inicio-da-sessao` e começa exatamente em `4dd4652`, o último commit de
25/07 às 22h36. O motivo está escrito em
`docs/process/sprints/2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md:36-47`:
duas das quinze entregas mexeram na área que ela nomeou, **na direção oposta à
que ela pediu**, e ela relatou *"interface tá quebrada e na hora do jogo tá um
caos legal"*. O rollback foi para trás de todas as quinze, e não só das duas.

**O segundo é a decisão de 29/07 às 03h**, registrada na anotação da tag
`arquivo/main-antes-da-v030`: a `main` remota passa a ser o que roda e foi
validado na tela. Foi feita no remoto (`git ls-remote origin refs/heads/main`
devolve `e74077c`) e **a ref local ficou onde estava**.

A causa mecânica de a ref local ainda apontar para 26/07 é banal: ela nunca foi
tocada de novo (reflog acima). E a causa de ela rastrear o upstream é anterior a
tudo isto — `branch.main.remote` foi escrito quando o repositório ainda era um
fork acompanhando o de origem.

O que sobra depois de descontar os dois eventos é o assunto desta sprint: dentro
dos 17 commits há trabalho que **não** foi rejeitado por ninguém e que
simplesmente ficou do outro lado.

---

## O que NÃO é a causa

- **Não é história reescrita.** `4dd4652` é ancestral dos dois lados; nenhuma
  das duas pontas foi rebaseada por cima da outra.
- **Não é uma tag apagada nem um commit perdido.** `git tag --points-at 2d8527a`
  devolve `arquivo/main-antes-da-v030`. Todos os 17 são alcançáveis por
  `cherry-pick` a partir dela.
- **Não é o upstream estando à frente.** `upstream/main` (`398d3ed`) é
  ancestral de `HEAD`; está 315 commits atrás.
- **Não é "ninguém documentou".** A divergência **está** documentada em dois
  lugares —
  `docs/process/sprints/2026-07-26-INDICE-o-que-falta.md:44` e `:62-68`, que já
  lista commit a commit, e
  `docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md:260-296`,
  que já mede `17 e 16` e já avisa que `git checkout main` cai na árvore de
  26/07. O que não existe é a **decisão** sobre a ref, e é isso que esta sprint
  fecha.
- **Não é verdade que a cura do `--fix-mic` continua fora.** O mapa-total de
  29/07 afirma isso em `:278` e `:1391`; a afirmação **envelheceu**. O
  `84d9f4e` foi portado em 30/07 e o critério de hoje é mais forte que o dele.
- **Não é que os 17 sejam todos entrega perdida.** Dois foram rejeitados por
  escrito e três consertam código que só existe se os rejeitados entrarem.

---

## Os 17, classificados

### Grupo (a) — já refeito nesta árvore por outro caminho

| Commit | O que entregava | Onde está hoje |
|---|---|---|
| `3a41cdf` | acentos em `udp_server.py` que deixavam a CI vermelha | `udp_server.py:238` |
| `84d9f4e` | `doctor --fix-mic` deixa de aplicar a cura refutada | `scripts/doctor.sh:1003-1017`; teste idêntico byte a byte |
| `d309e79` | retrato das nove abas + INDICE-o-que-falta + PERFIL-JOGO-01 + STATUS-SIMETRIA-01 + STEAM-INPUT-01 | trazidos por `7364da8` |
| `a46941d` | release v0.1.2 | superado pela v0.4.0 |
| `2d8527a` | versão nos cinco arquivos de empacotamento | superado; há portão (`scripts/check_version_consistency.py`) |
| `bc827cb` | a aba Status dizia quatro e desenhava dois | a contradição de contagem foi curada por CONTAGEM-E-COOP-01 (`status_actions.py:85`) |

### Grupo (b) — trabalho REAL que continua faltando

| Commit | O que falta, e como saber |
|---|---|
| `9c944a8` | simetria do instalador. **Como saber:** `grep -n -- '-w /sys/module' install.sh` devolve quatro linhas (`:620`, `:686`, `:696`, `:700`) e `grep -n usb_cmd_pad_to_report install.sh` não devolve nada |
| `d1177c2` | PLAYER-LED-01. **Como saber:** `grep -rn "cmd_numbers\|player_leds_game\|_GAME_LAYER_GATED_FIELDS" src/` devolve **zero** |
| `ef4b8bc`, metade SLOT-JOGADOR-01 | os dois números de jogador. **Como saber:** `grep -rn "sufixo_de_jogador" src/ tests/` devolve **zero**; e `grep -rn "numero_do_padrao_de_jogador" src/` também |
| `0c08e77`, o resto | o campo "Gamepads" da aba Emulação. **Como saber:** `grep -rn "classificar_joysticks\|rotulo_gamepads" src/` devolve **zero**, e `emulation_actions.py:514` ainda conta `glob("/dev/input/js*")` |
| `52e4c4c` + `d2cc854` | a refutação da camada 2 dentro da própria MIC-USB-01. **Como saber:** `grep -n REFUTADO docs/process/sprints/2026-07-25-MIC-USB-01-tres-mutes-empilhados.md` não devolve nada, e a linha `:55` ainda descreve `input:iec958-stereo` como *"sem sinal"* |

### Grupo (c) — o que NÃO vale portar

| Commit | Por quê |
|---|---|
| `b39fec9` (o vão dos botões) | **rejeitado por escrito, três vezes:** `2026-07-27-VAO-01-...:89` (*"a aba Gatilhos foi o alvo do commit `b39fec9`, rejeitado"*), `2026-07-29-LARGURA-01-...:355` e `2026-07-26-STATUS-SIMETRIA-01-...:39`. E a VÃO-01 foi entregue por outro caminho em 27/07 |
| `ef4b8bc`, metade MIC-FAIXA-01 | direção oposta à que ela pediu — mandou o medidor para o rodapé, ela queria à direita dos analógicos (`STATUS-SIMETRIA-01:36`). Hoje está dentro do card (`controller_card.py:24`) |
| `6f15759` (typelib parcial) | conserta o `from gi.repository import Pango` que só existe se MIC-FAIXA-01 entrar. `status_actions.py:36` hoje importa só `GLib, Gtk` |
| `a3b5b63` (o higienizador comeu o desenho dos LEDs) | conserta código que só existe com `d1177c2`. A lição — escrever glifo por `chr(0x25CF)` — deve entrar **junto** com E5, não sozinha |
| `10739bd` e `c98efd7` (docs) | trazem AUTO-02/03/04 (1517 linhas de sprint não implementada) e ajustes de índice de uma leva que não existe mais. O único item deles com valor vivo, o GATE-FSTRING-01 da AUTO-04, **já foi entregue** (`scripts/validar-acentuacao.py:619`) |

---

## As entregas

Ordem de preço crescente. **Uma por vez, cada uma no seu commit.**

### E0 — decidir o que fazer com a ref local `main`

**O que faz.** Tira a armadilha do caminho. Não é decisão minha; as opções, com
o custo de cada uma:

| Opção | Comando | O que ganha | O que custa |
|---|---|---|---|
| **A — mover a local para o remoto** | `git branch -f main origin/main && git branch main --set-upstream-to=origin/main` | `git checkout main` passa a entregar o que roda; `git push` da `main` passa a mirar o repositório dela | o nome `main` deixa de apontar para 26/07 — mas a tag `arquivo/main-antes-da-v030` já aponta, então nada fica inalcançável |
| **B — renomear** | `git branch -m main arquivo/main-antiga` | o nome deixa de mentir | fica sem `main` local nenhuma, e o nome duplica uma tag que já existe |
| **C — deixar como está, com aviso no README** | edição de `README.md` | zero risco de git | a armadilha continua armada, e quem digita `git checkout main` não passa pelo README antes |

**Recomendo a A**, por dois motivos medidos: `git tag --points-at 2d8527a` já
devolve `arquivo/main-antes-da-v030` (o custo da opção A é zero em termos de
alcançabilidade), e `git ls-remote origin refs/heads/main` já devolve `e74077c`
(a ref local é a **única** coisa nesta máquina que ainda diz outra coisa). O
`--set-upstream-to` é a metade que interessa mais que a primeira: enquanto
`branch.main.remote` for `upstream`, um `git push` distraído a partir da `main`
mira o repositório de outra pessoa.

**A escolha é dela.** Nenhuma das três deve ser executada sem ela dizer qual.

**Os arquivos.** Nenhum arquivo do projeto na opção A (é config de git); na C,
`README.md`.

**Como PROVAR.** Depois da A: `git rev-parse main` devolve `e74077c` e
`git config branch.main.remote` devolve `origin`; e
`git rev-list --left-right --count main...HEAD` devolve `0 0`. A prova de que
nada se perdeu: `git rev-parse arquivo/main-antes-da-v030^{commit}` continua
devolvendo `2d8527a` e `git log --oneline arquivo/main-antes-da-v030 --not HEAD`
continua listando os 17.

**O risco.** Baixo e reversível: a tag guarda o commit antigo. O risco de
verdade é fazer isto **antes** de portar E1 a E5 e alguém concluir que "a
divergência acabou". Por isso E0 vem primeiro na ordem de preço, mas o texto do
commit tem de dizer que os 17 continuam por portar.

---

### E1 — a refutação da camada 2 volta para dentro da MIC-USB-01

**O que faz.** O documento
`docs/process/sprints/2026-07-25-MIC-USB-01-tres-mutes-empilhados.md` ainda
ensina, em `:48` e `:55`, que `input:iec958-stereo` é *"entrada digital S/PDIF —
sem sinal"* e que a cura é trocar para `input:analog-stereo`. Isso foi refutado
por medição em 26/07: no perfil analógico a source nasce **sem porta de
captura** e entrega 327.680 bytes de silêncio digital; quem grava é o
`iec958-stereo`. O aviso existe hoje só em
`2026-07-29-SENSOR-VIVO-01-...:320` e no mapa-total — **não** no documento que
alguém abre quando vai mexer no microfone.

**Os arquivos.**
`docs/process/sprints/2026-07-25-MIC-USB-01-tres-mutes-empilhados.md` (o bloco
de 28 linhas de `52e4c4c` mais o conserto de negrito de `d2cc854`).

**Cuidado que vem de graça com este porte:** o bloco original começa com
`** REFUTADO POR MEDIÇÃO...` — o higienizador de emojis **já comeu** o glifo que
abria aquela linha, e foi por isso que `d2cc854` existiu. Escrever o glifo, se
houver, por codepoint, ou abrir a linha sem glifo nenhum.

**Como PROVAR (teste que morde).** Um teste de documento em
`tests/unit/test_docs_mic_usb_01_refutacao.py`: o arquivo tem de conter a  <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->
palavra `REFUTADO` **acima** da linha que descreve `input:iec958-stereo`, e a
frase que manda trocar para `input:analog-stereo` não pode aparecer sem um aviso
antes dela. Prova de mordida: apagar o bloco derruba o teste; apagar só o glifo
de abertura **não** derruba (é isso que queremos — o teste não pode depender de
glifo, senão o higienizador o quebra de novo).

**O risco.** Nenhum sobre código. O risco é escrever "está refutado" e alguém
ler como "o microfone não funciona" — o bloco tem de manter a última frase do
original, a que declara em aberto por que a medição de 25/07 e a de 26/07
discordam.

---

### E2 — o ciclo `uninstall` + `install` para de desligar cura em silêncio

**O que faz.** Reaplica o `9c944a8`: os portões `-w` sobre `/sys/module` viram
`-e`, e os quatro params órfãos ganham rearme explícito. O `-w` pergunta pela
permissão de quem **não** vai escrever — a escrita logo abaixo é `sudo tee` —, e
os arquivos são `root:root 0644`, então o portão é sempre falso para ela.
Medido nesta máquina: os quatro params legíveis estão em `N`/`0` agora.

**Os arquivos.**
- `install.sh:620`, `:686`, `:696`, `:700` — `-w` vira `-e`;
- `install.sh`, no bloco do `hid_nintendo` — rearme de `usb_cmd_pad_to_report`,
  `usb_send_conn_status`, `usb_probe_degrade`;
- `install.sh:787` — rearme de `rtw88_usb/parameters/hang_reset` (hoje o ramo só
  imprime que o módulo patchado está carregado);
- `tests/unit/test_install_dkms_default.py` — a classe de simetria.

**Como PROVAR (teste que morde).** Os dois testes do `9c944a8`, que são
autocontidos e portáveis sem conflito:

1. `re.findall(r"-w\s+(/sys/module/\S+)", INSTALL)` tem de vir **vazio**;
2. casando a **escrita** (`\|\s*sudo tee\s+/sys/module/(\w+/parameters/\w+)`),
   todo param que o `uninstall.sh` desarma tem de aparecer rearmado no
   `install.sh`, com uma única exceção declarada
   (`snd_usb_audio/parameters/quirk_flags`, que é da toolchain pessoal dela via
   cmdline).

Prova de que morde, e ela **já foi feita**: rodando essas duas regras contra a
árvore de hoje, a primeira devolve quatro achados e a segunda devolve quatro
órfãos. O teste reprova antes da cura e passa depois. A armadilha registrada no
commit original vale de novo: casar o caminho em qualquer lugar do script
**não** morde — apagar o `printf` deixando o portão com o mesmo caminho passaria
verde. Tem de casar `| sudo tee`.

**O risco.** Mexe no `install.sh`, que é o arquivo de maior alcance do projeto.
Mitigação: as mudanças são todas dentro de blocos best-effort que já terminam em
`|| true`, nenhuma delas recarrega módulo (proibido: derrubaria os controles por
BT), e o efeito só aparece na próxima conexão do controle. **Não validar rodando
o ciclo enquanto ela estiver jogando.** E há um detalhe desta máquina que o
teste não cobre: `/sys/module/hid_nintendo` **não existe** agora, o que quer
dizer que o módulo patchado não está carregado — o rearme dos três params do
patch 0003 não vai ter efeito visível aqui até um boot com o DKMS no lugar.

---

### E3 — a aba Emulação para de contar nós e passa a contar aparelhos

**O que faz.** Hoje
`src/hefesto_dualsense4unix/app/actions/emulation_actions.py:514-522` faz
`glob("/dev/input/js*")`, conta os nós e escreve `f"{n} {palavra} pelo sistema"`.
Medido agora, com **um** DualSense na mesa:

```
/dev/input/js2  ->  name=Hefesto Virtual DualSense P1                 uniq=02:fe:00:00:00:01
/dev/input/js3  ->  name=Hefesto Virtual DualSense P1 Motion Sensors  uniq=02:fe:00:00:00:01
```

A aba diz **"2 controles detectados pelo sistema"**, e os dois nós são o **nosso
próprio** gamepad virtual e o nó de sensores dele. O controle físico dela não
está nessa lista. É o "oito" da CONTAGEM-01, vivo, só que hoje dá dois.

**Os arquivos.**
- `src/hefesto_dualsense4unix/app/actions/emulation_actions.py` — trazer
  `classificar_joysticks` (pura, recebe os atributos já lidos),
  `_atributos_do_joystick` (a leitura de sysfs, tolerante a nó que sumiu) e
  `rotulo_gamepads`, do `0c08e77`;
- `tests/unit/` — arquivo novo, **não** o `test_contagem01_uma_contagem_so.py`  <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->
  inteiro (796 linhas que cobrem também o que já foi curado por
  CONTAGEM-E-COOP-01 e conflitariam).

**Como PROVAR (teste que morde).** `classificar_joysticks` é pura: alimentar com
a mesa medida acima (dois nós, mesmo `uniq` `02:fe:...`) e exigir
`(0 físicos, 1 nosso, 0 outros)` — o agrupamento **por aparelho** é o que impede
o nó de sensores de virar um segundo controle. Três mutações que têm de
reprovar: (1) tirar o agrupamento por aparelho, (2) trocar o prefixo
`02:fe:` por qualquer outro, (3) fazer o desconhecido cair em "nosso" em vez de
"físico". E um teste do rótulo: com `nos > 0` e nenhum aparelho físico, o texto
**não** pode dizer "controles detectados pelo sistema".

**O risco.** Baixo — é um rótulo, sem efeito sobre o daemon. O risco real é
sobrecontar de novo: um controle pode render vários nós, e o rótulo do `0c08e77`
resolve isso dizendo os dois números (aparelhos por dono **e** nós crus). Manter
essa segunda metade; ela é o que explica a diferença em vez de escondê-la.

---

### E4 — os dois números de jogador voltam a se falar (SLOT-JOGADOR-01)

**O que faz.** Três coisas, e uma delas é defeito de daemon, não de tela.

1. **O defeito de daemon.**
   `src/hefesto_dualsense4unix/daemon/subsystems/coop.py:1373` faz
   `return [1 if ok else None for ok in connected]`: com o co-op **desligado**,
   **todo** controle conectado é "jogador 1". Mas o input vem sempre do
   primário — um segundo DualSense com o co-op desligado não move nada no jogo,
   e a tela põe dois cartões com o mesmo número. A cura do `ef4b8bc` é a máscara
   `_primarios()`, com três fontes em ordem (`is_primary` da entrada,
   `primary_uniq` do backend, e "ninguém" — nunca a posição na lista).
2. **A regra tem dois donos.** `app/actions/home_actions.py:423-427` escreve
   `"Controle 2 — P3"`; `app/widgets/controller_card.py:490-509` escreve
   `"Controle 2 — USB · Jogador 3"`. Duas implementações, dois formatos, nenhum
   dono. O `ef4b8bc` cria `app/actions/base.sufixo_de_jogador` e faz as duas
   chamarem.
3. **O número passa a dizer de quem ele é** — "P1 no co-op", "P4 no jogo" —
   porque são duas perguntas diferentes: qual aparelho é este (fila de
   preferência, `player_slot`, é o que **acende na lâmpada**) e que jogador ele
   alimenta (índice de alocação de vpad, ancorado no primário do backend, que é
   a ordem crua do hidapi). Nenhuma renumeração faz os dois coincidirem — isso
   já está medido e registrado.

**Os arquivos.** `daemon/subsystems/coop.py` (o `_primarios` e o
`resolve_player_numbers`), `app/actions/base.py` (`sufixo_de_jogador`),
`app/actions/home_actions.py`, `app/widgets/controller_card.py`,
`core/led_control.py` (`numero_do_padrao_de_jogador`, a inversa da tabela — só
se E5 vier junto; sozinha ela não tem chamador), e um teste novo a partir de
`test_slot_jogador_01_dois_numeros.py` do `ef4b8bc`.  <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

**Como PROVAR (teste que morde).** `resolve_player_numbers` com o co-op
desligado, dois controles conectados, um deles carimbado `is_primary`: o
resultado tem de ser `[1, None]`, não `[1, 1]`. Mutação que reprova: devolver
`[1] * n`, que é literalmente o código de hoje. E, para o dono único, um teste
que importa `_format_controller_title` e `titulo_do_card` e exige que **as duas**
produzam o mesmo sufixo para a mesma entry — arrancar `sufixo_de_jogador` de uma
delas derruba.

**O risco.** Médio, e é o de sempre nesta casa: um card que hoje mostra "P1"
passa a não mostrar número nenhum, e isso **parece** regressão para quem olha.
Tem de entrar com print antes e depois. Há teste existente que muda de valor
esperado — `tests/unit/test_numero_do_controle_unico.py:79-99` grava hoje
`"Controle 2 — P3"` e `"Controle 2"`; a atualização dele é legítima, mas
atualizar valor esperado é exatamente como esta casa já escondeu bug duas vezes,
então o teste novo tem de ser escrito **antes** e cobrir a propriedade (o sufixo
declara a autoridade), não o literal.

---

### E5 — o número que o jogo atribui chega ao controle (PLAYER-LED-01)

**O que faz.** O commit `d1177c2` é o mais caro dos cinco (1670 linhas). O
mecanismo do defeito está vivo em
`src/hefesto_dualsense4unix/core/backend_pydualsense.py:1163-1171`:

```python
game = self._game_output_by_uniq.get(uniq) if uniq is not None else None
...
if game is not None and self._game_wins():
    resolved = _merge_desired(resolved, game)
```

Sob autoridade `daemon`, a camada do jogo sai do merge **inteira** — cor e
número junto — e a repintura reescreve o nosso número por cima do que o jogo
acabou de pedir. Sinal de jogo sobe, vale o número do jogo; sinal cai, volta o
nosso. É o flip-flop que ela viu na partida.

A decisão do commit original, que continua valendo: o gate passa a ser **por
campo**, num ponto único (`_GAME_LAYER_GATED_FIELDS = frozenset({"led"})`). A
**cor** fica gateada, porque o gate nasceu de um incidente medido (o cliente da
Steam repintando a paleta sem jogo nenhum) e o dano ali é visível e persistente.
O **número** sai do gate: o falso positivo custa a função inteira, e o falso
negativo custa quase nada.

Vem junto: a trava de log por controle (hoje um campo único do backend faz o
primeiro controle retido silenciar os outros três), `uhid_replica_ativa` emitido
só quando a réplica chega ao sink com o par honesto `game_output_aplicado`, e o
diagnóstico `hefesto-dualsense4unix controller numbers`.

**Os arquivos.** `core/backend_pydualsense.py`, `cli/cmd_controller.py`,
`core/sysfs_leds.py` (só o aviso de armadilha na docstring de `get_players`,
hoje em `:238` sem ele), `daemon/lifecycle.py`,
`integrations/uhid_gamepad.py`, mais os testes.

**A lição do `a3b5b63` entra aqui, no mesmo commit:** os glifos do desenho de
LED (`chr(0x25CF)`, `chr(0x25CB)`) escritos por **codepoint**, e o teste
cobrando **propriedades** (cinco posições, aceso diferente de apagado, desenho
não vazio) em vez de comparar com literal. Da última vez o higienizador apagou
os glifos do código **e** do valor esperado no mesmo passe, e a suíte ficou
verde com a função quebrada.

**Como PROVAR (teste que morde).** O critério afiado, e que o próprio commit
corrigiu depois de medir: **não** é retenção de `led` (essa continua possível e é
benigna) — é retenção de `player_leds`. O teste entra pela fiação real: escreve
o report no fd do vpad, chama o que o poll loop chama, usa os sinks e o backend
reais, e assere na escrita do nó do controle físico. Mutação que tem de
reprovar: pôr `player_leds` de volta no `_GAME_LAYER_GATED_FIELDS`.

**Nota de método, e é armadilha desta casa:** o cabeçalho do `.pyc` guarda mtime
em segundos inteiros, então mutante do mesmo tamanho aplicado no mesmo segundo
reaproveita bytecode velho e dá falso "o teste não morde". Rodar com
`PYTHONDONTWRITEBYTECODE=1`.

**O risco.** O maior dos cinco. Toca o caminho de escrita no controle físico,
com a GUI dela aberta e o daemon vivo. Duas coisas ficaram declaradas em aberto
pelo commit original e continuam abertas: o buraco do sinal de jogo em
`daemon/subsystems/game_signal.py` (depois desta decisão ele deixa de custar o
número e afeta só a cor), e o fato de que a leitura de `/sys/class/leds` **não
identifica quem escreveu** o padrão — a tabela do kernel é idêntica à nossa em
1..4. Quem for validar de olho tem de usar o log, não o sysfs.

---

## O método de porte — e por que não é `cherry-pick`

A árvore andou **24 commits** desde `4dd4652`. Nesse intervalo entraram a v0.2.0,
a v0.3.0, a v0.4.0, o redesenho da aba Status, a CONTAGEM-E-COOP-01, a VÃO-01, a
LARGURA-01 e a leva do microfone — todos nos **mesmos arquivos** dos 17.
`status_actions.py`, `home_actions.py`, `controller_card.py` e `doctor.sh`
mudaram dos dois lados.

A regra, então:

1. **Um por vez, um commit por entrega.** Nunca em bloco, nunca "os quatro do
   grupo (b) de uma vez".
2. **Entender e reaplicar, não `cherry-pick`.** O `cherry-pick` de `ef4b8bc`
   traria junto a faixa de microfone que ela rejeitou; o de `0c08e77` traria uma
   contagem que já foi curada por outro caminho e conflitaria com a
   `ContagemDeControles`. Ler o commit, entender a **regra**, escrever a regra
   contra o código de hoje.
3. **O teste primeiro, e ele tem de reprovar antes.** Em E2 isso já está feito
   (as duas regras reprovam contra a árvore de hoje). Nas outras, escrever o
   teste, ver vermelho, então curar.
4. **E4 e E5 exigem aval visual dela antes do commit** — os dois mudam o que
   aparece no card e no controle. Print antes e depois.
5. **Nada de E1 a E5 depende de E0.** Se ela decidir deixar a ref como está, os
   cinco continuam válidos.

---

## O que NÃO fazer

- **Não rodar `git checkout main` nesta máquina sem saber o que ela é.** A
  árvore de trabalho **é** o que roda para ela: o daemon está vivo e a GUI está
  aberta. Trocar a árvore por baixo deles devolve o código de 26/07 — sem o
  interruptor do teclado emulado, sem o perfil guardando as outras abas, sem a
  cura do microfone. Se for mesmo preciso olhar aquele código, `git worktree add`
  numa pasta separada, ou `git show arquivo/main-antes-da-v030:<arquivo>`.
- **Não fazer `git push` a partir da `main`.** `branch.main.remote` é `upstream`,
  e não há `push.default` nem `remote.pushDefault` para salvar de um engano.
- **Não portar em bloco.** `git cherry-pick 0c08e77 bc827cb ef4b8bc b39fec9` é a
  forma mais rápida de trazer de volta as duas coisas que ela mandou tirar em
  26/07 junto com as que ela quer.
- **Não portar `b39fec9`.** Está rejeitado por escrito em três documentos.
- **Não portar a metade MIC-FAIXA-01 do `ef4b8bc`.** O medidor está no lugar que
  ela pediu desde 28/07; trazê-lo para o rodapé é desfazer trabalho validado.
- **Não apagar a tag `arquivo/main-antes-da-v030`**, em nenhuma das três opções
  de E0. Ela é o que torna a opção A barata.
- **Não usar o campo `Status:` dos documentos como fonte.** Nesta leva ele
  errou nos dois sentidos: a CONTAGEM-01 e a PLAYER-LED-01 dizem `ABERTA` e
  parte delas foi entregue por outro caminho; e o mapa-total de 29/07 afirma em
  `:278` e `:1391` que a cura do `--fix-mic` está fora da árvore — estava, e não
  está mais desde 30/07.
- **Não concluir "a divergência acabou" depois de E0.** Mover a ref não porta
  uma linha de código.

---

## O que fica sem medição

- **Não rodei o ciclo `uninstall` + `install`.** A regra da sessão proíbe, e o
  daemon dela está vivo. O que medi é o **estado atual** dos params (quatro
  desligados) e o **texto** dos dois scripts (quatro portões `-w` mortos e
  quatro órfãos). A ligação causal entre um e outro é a que o `9c944a8`
  descreve; eu não a reproduzi.
- **Não medi por que `hang_reset` está em `N`.** O default do `.ko` é `Y` pela
  documentação do próprio `install.sh:97`. Pode ser o desarme do `uninstall.sh`,
  pode ser outra coisa.
- **Não medi o defeito de altura que o `b39fec9` diz ter achado de brinde** — o
  modo `MultiPositionVibration` pedindo 646px numa faixa de 630px. Ele nasce em
  runtime e `tests/unit/test_layout_orcamento_altura.py` mede só o Glade. Como o
  commit está rejeitado, isso fica como pergunta em aberto para quem for mexer
  na aba Gatilhos, não como entrega.
- **Não conferi os outros 14 branches locais** que `git branch -vv` lista
  (`wip/emulacao-untracked`, `restauro/v0.1.1`, `backup/pre-reword-dsx` e mais
  onze). Alguns podem esconder trabalho não portado também; não é escopo desta
  sprint.
- **Não abri os 17 commits linha a linha.** Li a mensagem e o `--stat` de todos,
  e o diff completo de `9c944a8`, `d1177c2`, `0c08e77`, `ef4b8bc`, `b39fec9`,
  `6f15759`, `a3b5b63`, `52e4c4c` e `3a41cdf`. Dos de documentação (`10739bd`,
  `c98efd7`, `d309e79`) li só a lista de arquivos e conferi quais existem aqui.
- **Não validei nada na tela.** Todas as afirmações sobre a interface vêm do
  código e do sysfs, não de captura.
- **Não sei se a ref local foi deixada assim de propósito.** O reflog diz que
  ela não foi tocada depois de 26/07, o que é evidência de esquecimento e não
  prova de nada. Só ela pode dizer.
