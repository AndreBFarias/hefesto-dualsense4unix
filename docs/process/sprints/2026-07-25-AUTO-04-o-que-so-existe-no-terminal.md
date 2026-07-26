# AUTO-04 — o que só existe no terminal

- **Status:** ABERTA
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026

## O pedido

> "preciso de verdade que veja as features do projeto (…) à procura de facilidade
> do usuário: ao clicar em tal coisa, ele não precisar alterar 10 coisas em abas,
> fechar a Steam, abrir, aplicar x, y e z, tudo de forma manual mas de forma
> automática, o máximo que der."

AUTO-01 (ENTREGUE, `8fe735d`) pegou o que impedia **os quatro jogadores** e
delegou o resto a AUTO-02 (Steam), AUTO-03 (fluxo de jogo) e **AUTO-04 — o que
só existe no terminal**. Esta é a AUTO-04.

O critério de valor é um só, e é o dela: **a mantenedora é a usuária-alvo e não
quer terminal.** Uma capacidade que só se alcança por linha de comando é, para
ela, uma capacidade que não existe.

## Correção de registro: os "29 pontos de fricção" nunca foram escritos

AUTO-01 abre dizendo *"Vinte e nove pontos de fricção foram mapeados"*
(`2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md:14`). O mapeamento em si **não
existe em lugar nenhum do repositório**. Só o número sobreviveu:

```
$ grep -rn "29 pontos\|fricção\|friccao" docs/
docs/history/DUVIDAS_V2.md:121:- **Recomendação:** `search`. Menos fricção pra criador de perfil. (…)
docs/process/sprints/2026-07-25-INDICE-leva-quatro-controles.md:24:| 6 | "não precisar alterar 10 coisas em abas, fechar a Steam..." | 29 pontos de fricção; (…) | AUTO-01 |
docs/process/sprints/2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md:14:Vinte e nove pontos de fricção foram mapeados. Esta sprint pega os que **impedem
```

Duas ocorrências e as duas são o mesmo número citado de memória; a terceira é de
outro assunto. **Esta sprint remede do zero, a partir do código** — não herda a
contagem, e não afirma que são vinte e nove. O que segue é o que foi medido em
25/07/2026, com o comando ao lado de cada afirmação.

Registrar isso importa por um motivo prático: se alguém tentar fechar AUTO-02 ou
AUTO-03 procurando "os pontos 12 ao 20", não vai achar. Cada uma dessas sprints
vai ter de medir o seu próprio escopo, do jeito que esta mediu.

## O achado que resume a sprint: existem dois `doctor`, e a nossa documentação
manda rodar o que não existe

O checklist de validação em hardware, na seção "6. O microfone (MIC-USB-01)",
manda a mantenedora rodar isto
(`docs/process/sprints/2026-07-25-CHECKLIST-validacao-em-hardware.md:109`):

```bash
hefesto-dualsense4unix doctor --fix-mic
```

O comando **não existe**. Rodado:

```
$ hefesto-dualsense4unix doctor --fix-mic
Usage: hefesto-dualsense4unix doctor [OPTIONS]
Try 'hefesto-dualsense4unix doctor --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────╮
│ No such option: --fix-mic (Possible options: --fix, --fix-safe)              │
╰──────────────────────────────────────────────────────────────────────────────╯
$ echo $?
2
```

A cura existe — mora no **outro** doctor, o de shell:

```
$ grep -n "fix-mic\|fix_mic" scripts/doctor.sh
28:# Uso: scripts/doctor.sh [--fix] [--fix-mic] [--quiet] [--watch-dropout] [--suggest-port]
33:#   --fix-mic         SÓ o microfone (camadas 1 e 2) — cura, mostra o veredito
62:        --fix-mic)        FIX_MIC=1 ;;
681:# Cura das camadas 1 e 2. Chamada pelo --fix (junto das demais) e pelo --fix-mic
684:fix_mic_dualsense() {
2815:    fix_mic_dualsense
2827:        fix_mic_dualsense
```

E esse script **não está no PATH**:

```
$ which doctor.sh
doctor.sh not found
$ ls ~/.local/bin/ | grep -i hefesto
hefesto-dualsense4unix
hefesto-dualsense4unix-applet
hefesto-dualsense4unix-gui
hefesto-launch
```

`install.sh` instala quatro binários e **nenhum** deles é o `doctor.sh`. Para
rodar a cura curta do microfone é preciso saber que o repositório existe, saber
onde ele está, e digitar `bash scripts/doctor.sh --fix-mic` de dentro dele.

### Por que a CLI não repassa a opção

A CLI é uma casca por cima do script de shell — `cli/cmd_doctor.py:3` diz
literalmente *"Reusa `scripts/doctor.sh`"* — mas ela repassa **só duas** das
cinco opções que o script aceita (`cli/cmd_doctor.py:99-107`):

```python
    sh = _find_doctor_sh()
    if sh is not None:
        args = ["bash", str(sh)]
        if fix:
            args.append("--fix")
        if quiet:
            args.append("--quiet")
```

Ficaram de fora `--fix-mic`, `--watch-dropout` e `--suggest-port`. Não é uma
decisão registrada em lugar nenhum — a assinatura de `doctor_cmd`
(`cli/cmd_doctor.py:83-87`) simplesmente tem três parâmetros, e dois deles são
os que passam adiante.

### O que a rota errada custa

A alternativa que existe hoje na CLI, `doctor --fix`, **também** cura o
microfone: `apply_fixes` chama `fix_mic_dualsense` no fim (`scripts/doctor.sh:2815`).
Mas o `--fix` faz muito mais do que a mantenedora pediu — no mesmo caminho ele
reaplica udev, instala o drop-in do WirePlumber e roda
`disable_steam_input.sh --apply` em **todos** os `localconfig.vdf`
(`scripts/doctor.sh:2805-2810`). O `--fix-mic` existe justamente para não fazer
isso; o comentário no próprio script diz o porquê (`scripts/doctor.sh:2821-2823`):

```
    # MIC-USB-01: rota curta para quem só quer o microfone de volta agora —
    # cura as camadas 1 e 2, mostra o veredito das duas e sai.
```

Ou seja: a rota curta foi escrita de propósito, documentada no checklist, e é
inalcançável pela porta que o checklist manda usar. **Quem seguir o checklist ao
pé da letra recebe um erro; quem improvisar o `--fix` recebe um efeito colateral
que ninguém pediu.**

### E a janela não cura nenhuma das três camadas

Verificado por completo, porque era a pergunta óbvia seguinte. O botão
"Aplicar correções" da aba Sistema (`gui/main.glade:1904`, `btn_storm_fix_safe`)
roda dois scripts e só (`app/actions/daemon_actions.py:487-489`):

```python
                ("scripts/disable_steam_input.sh", ["--apply-quiet"]),
                ("scripts/fix_wireplumber_default_source.sh", ["--install"]),
```

`--install` é um modo **diferente** de `--unmute-routes`
(`scripts/fix_wireplumber_default_source.sh:54` e `:59`), que é o que a camada 1
precisa. E os botões "Ligar"/"Desligar" do microfone na aba Emulação
(`gui/main.glade:2315` e `:2322`) chamam `--enable-mic` / `--disable-source`
(`app/actions/emulation_actions.py:445` e `:448`) — a supressão do WirePlumber,
que é uma quarta coisa.

Resultado medido: **não existe caminho na janela que desfaça o mute persistido
por rota (camada 1), o perfil da placa preso em S/PDIF (camada 2) ou o mudo no
firmware do controle (camada 3).** As camadas em si são território de MIC-USB-01
e não são redescritas aqui; o que pertence a AUTO-04 é o fato de a cura das três
morar **fora da janela e fora do PATH**.

## O mapa: CLI × janela

A CLI tem **17 grupos** e **44 comandos-folha** (`hefesto-dualsense4unix --help`
mais um `--help` por grupo, todos rodados em 25/07). O `mic` sozinho aceita
**dez** ações no argumento posicional, então o total de capacidades endereçáveis
por linha de comando é **53**.

Legenda do veredito: **TEM** = há caminho equivalente na janela; **NÃO TEM** =
não há; **DIFERENTE** = há um botão parecido, mas ele faz outra coisa.

### Leitura e estado

| comando | janela | veredito |
|---|---|---|
| `status` | aba Status, cartão por controle (`app/widgets/controller_card.py`) | TEM |
| `battery` | linha "Bateria:" no cartão (`controller_card.py:528`) | TEM |
| `controller list` | seletor de controle da aba Status (`status_actions.py:458`) | TEM |
| `controller target <n\|all>` | mesmo seletor (`status_actions.py:403`) | TEM |
| `version` | nenhuma — `grep -rn "__version__" src/hefesto_dualsense4unix/app/` volta vazio, e a `main.glade` não tem rótulo de versão | NÃO TEM |
| `doctor` (sem flag) | a aba Sistema mostra só o bloco anti-storm (`daemon_actions.py:444-446`, `storm_doctor.storm_report()`); o `doctor.sh` inteiro — daemon, udev, uinput, applet, WirePlumber, microfone — nunca roda pela janela | DIFERENTE |
| `doctor --fix-safe` | "Aplicar correções" (`main.glade:1904`) roda os mesmos dois scripts (`daemon_actions.py:487-489`), menos o quirk (comentário BUG-C, `daemon_actions.py:490-497`) | TEM |
| `doctor --fix` | nenhuma | NÃO TEM |
| `doctor --quiet` | não se aplica (é formatação de saída) | fora de escopo |

### Modo, máscara e co-op

| comando | janela | veredito |
|---|---|---|
| `gamepad on/off/status` | botões segmentados da aba Emulação (`main.glade:2177`, `:2184`, `:2191`) e "Jogar pelo Hefesto" na Início (`home_actions.py:63`) | TEM |
| `native on/off/status` | **"Jogar direto (Sony)"** é um dos três botões de modo da aba Início (`home_actions.py:64`), e o plano emite `native.mode.set` (`mode_transition.py:89`) | TEM |
| `mouse on/off/status` | "Controlar o PC" (`home_actions.py:62`) + aba Mouse | TEM |
| `coop on` | "Preparar co-op (N jogadores)" (`main.glade:216`, `home_actions.py:337`), que encadeia modo jogo + `coop.set` + renumeração (`mode_transition.py:204`) | TEM |
| `coop off` | nenhuma — sair de "Jogar pelo Hefesto" **preserva** a preferência de propósito (`mode_transition.py`, comentário FEAT-COOP-DEFAULT-ON-01) | NÃO TEM |
| `coop status` | rótulo do botão + `status_actions.py:991` | TEM |

**Nota sobre o Modo Nativo.** A hipótese de que ele só apareceria numa dica de
ferramenta (`main.glade:2179`) foi **refutada pela medição**: aquela linha é o
tooltip do botão "Desligado" do gamepad, que apenas menciona o Modo Nativo. O
caminho de verdade é o terceiro botão de modo da aba Início, e ele liga e desliga
o modo **sem criar perfil nenhum** — `plan_mode_transition` devolve
`[("native.mode.set", {"enabled": True})]` (`mode_transition.py:89`). O modo
`native` como opção de perfil (`profiles_actions.py:110`) é um segundo caminho,
não o único. Fica registrado que o item entrou nesta sprint como suspeita e saiu
como não-defeito.

### Daemon

| comando | janela | veredito |
|---|---|---|
| `daemon status` | aba Sistema (`daemon_actions.py:1185`, `systemctl is-enabled`) | TEM |
| `daemon start` (gerenciado) | "Ligar o Hefesto" (`main.glade:1767`) | TEM |
| `daemon stop` | "Desligar o Hefesto" (`main.glade:1779`) | TEM |
| `daemon restart` | "Reiniciar o Hefesto" (`main.glade:1804`) | TEM |
| `daemon install-service` | "Corrigir modo de execução" (`main.glade:1811`) — mas ele é `visible=False` por padrão (`main.glade:1814`) e só aparece no estado `online_avulso` (`daemon_actions.py:1571-1581`) | DIFERENTE |
| `daemon uninstall-service` | nenhuma | NÃO TEM |
| `daemon enable` (auto-start no boot) | nenhuma — a janela **lê** `is-enabled` (`daemon_actions.py:1695`) e nunca escreve | NÃO TEM |
| `daemon disable` | nenhuma | NÃO TEM |
| `daemon pause` / `daemon resume` | "Modo jogo" / "Sair do modo jogo" (`main.glade:2233`, `:2240`) chamam `daemon.emulation.suppress`, **não** `daemon.pause` — e a troca foi deliberada, com o porquê escrito em `emulation_actions.py:653-660` (o `pause` persistia `paused.flag` e o daemon renascia pausado no boot) | DIFERENTE |
| `daemon start --foreground --poll-hz --headless --reconnect` | nenhuma | NÃO TEM (e não deve ter — ver "a linha de corte") |

O `daemon pause` é o caso mais traiçoeiro da tabela: há um botão com o nome
certo, ele faz uma coisa **melhor**, e mesmo assim o kill-switch amplo que o
`pause` oferece (parar gatilhos, LED e edges de uma vez) continua sem porta na
janela. Quem ler a CLI e a janela lado a lado vai achar que são a mesma coisa.

### Perfis

| comando | janela | veredito |
|---|---|---|
| `profile list` | aba Perfis (`main.glade:1388`+) | TEM |
| `profile create` | "Novo" (`main.glade:1388`) | TEM |
| `profile delete` | "Remover" (`main.glade:1406`) | TEM |
| `profile activate` | "Ativar" (`main.glade:1418`) | TEM |
| `profile save --from-active` | "Salvar" (`main.glade:1705`) / "Salvar Perfil" (`main.glade:2746`) | TEM |
| `profile apply --file` | "Importar" (`main.glade:2755`, `footer_actions.py:350-366`) | TEM |
| `profile show` (JSON bruto) | nenhuma — não há visualizador de JSON de perfil na janela | NÃO TEM |

### Microfone

| comando | janela | veredito |
|---|---|---|
| `mic on` / `mic off` | "Ligar"/"Desligar" da aba Emulação (`main.glade:2315`, `:2322` → `emulation_actions.py:445`, `:448`) | TEM |
| `mic status` | rótulo `emulation_mic_status_label` (`main.glade:2307`) | TEM |
| `mic promote` / `mic demote` | nenhuma — `grep -rn "promote\|demote" src/hefesto_dualsense4unix/app/` volta vazio | NÃO TEM |
| `mic mute` / `mic unmute` / `mic release` | nenhuma. A ponte existe (`app/ipc_bridge.py:526`, `mic_set`) e o ponto exato de fiação está **escrito e não fiado**: `ipc_bridge.py:544` diz *"PONTO EXATO DE FIAÇÃO (deixado pronto, não fiado…): o botão de microfone da aba Status, ao lado do medidor"*. O selo que existe hoje é rótulo, não botão — `sensor_widgets.py:91`, `selo_mic()`, e `grep -rln "Gtk.Button" src/hefesto_dualsense4unix/app/widgets/` volta vazio | NÃO TEM |
| `mic bt` / `mic bt-status` | nenhuma — **delegado a MIC-BT-01**, não redescrito aqui | NÃO TEM (outra sprint) |

O selo é o pior dos mundos: a janela **diz** MUDO (`sensor_widgets.py:100`) e não
oferece o desmute. Ela informa o problema e esconde a cura.

### Efeitos e hardware

| comando | janela | veredito |
|---|---|---|
| `led --color` | "Aplicar no controle" da aba Lightbar (`main.glade:796`) | TEM |
| `led --brightness` | `lightbar_brightness_scale` (`main.glade:871`) | TEM |
| `test led` | mesmo caminho da Lightbar | TEM |
| `test rumble --weak --strong` | "Testar por 500 ms" (`main.glade:1280`) usa a intensidade da aba, não `weak`/`strong` crus | DIFERENTE |
| `test trigger --side --mode --params` | "Aplicar em L2"/"Aplicar em R2" (`main.glade:530`, `:661`) aplicam preset; a janela não manda `--params` arbitrário | DIFERENTE |
| `test trigger --raw` (7 bytes HID) | nenhuma | NÃO TEM (e não deve ter) |

### Plugins

| comando | janela | veredito |
|---|---|---|
| `plugin list` | nenhuma | NÃO TEM |
| `plugin reload` | nenhuma | NÃO TEM |

Confirmado, como pedido:

```
$ grep -rlni "plugin" src/hefesto_dualsense4unix/app/
(vazio)
$ grep -cni "plugin" src/hefesto_dualsense4unix/gui/main.glade
0
$ hefesto-dualsense4unix plugin list
Nenhum plugin carregado.
```

Nenhuma ocorrência da palavra em toda a camada de aplicação, e zero na descrição
da janela. O subsistema de plugins é invisível para quem não abre um terminal.

### Interfaces alternativas

| comando | janela | veredito |
|---|---|---|
| `tui` | não se aplica — é outra interface inteira (Textual), não uma capacidade | fora de escopo |
| `tray` | não se aplica — ícone de bandeja, requer extra de instalação | fora de escopo |

## O que só roda por `python3 <caminho absoluto>`

Duas capacidades reais do produto **não são subcomandos de nada**. São módulos
executáveis chamados por caminho:

```
$ grep -n "add_argument" src/hefesto_dualsense4unix/integrations/proton_pin.py | head -4
1143:        "--ensure",
1148:        "--lock",
1153:        "--unlock",
1158:        "--report",
```

```
$ grep -n "add_argument" src/hefesto_dualsense4unix/integrations/steam_launch_options.py | head -3
974:        "--status",
977:        "--migrate",
982:        "--strip",
```

O instalador os invoca por caminho absoluto (`install.sh:2227` e `:2256`) e,
quando falha, **manda a usuária copiar o comando**:

```
install.sh:2238  rode depois: python3 ${LAUNCH_MIGRATE_PY} --migrate
install.sh:2271  rode: python3 ${PROTON_PIN_PY} --ensure
install.sh:2278  Steam (ou um jogo) aberta — trava ADIADA; feche a Steam e rode: python3 ${PROTON_PIN_PY} --lock
install.sh:2281  trava do Proton falhou — rode manualmente: python3 ${PROTON_PIN_PY} --lock
```

`LAUNCH_MIGRATE_PY` e `PROTON_PIN_PY` expandem para caminhos completos dentro do
repositório. É literalmente o que ela descreveu: *aplicar x, y e z, tudo manual*.

Duas dessas quatro linhas já melhoraram. A `install.sh:2279` acrescenta
*"(ou use o botão 'Travar Proton validado' na aba Sistema da GUI)"* — o botão
existe (`main.glade:1925`, `btn_proton_lock`), e "Aplicar aos jogos da Steam"
(`main.glade:1918`) cobre o lado do wrapper. Mas o mapeamento é **parcial e só de
ida**:

| ação do módulo | janela | veredito |
|---|---|---|
| `proton_pin --lock` | "Travar Proton validado" (`main.glade:1925`) | TEM |
| `proton_pin --ensure` | nenhuma (é passo do instalador) | NÃO TEM |
| `proton_pin --unlock` | nenhuma — `grep -rn "unlock" src/hefesto_dualsense4unix/app/` volta vazio | NÃO TEM |
| `proton_pin --report` (read-only) | nenhuma | NÃO TEM |
| `steam_launch_options --migrate` | coberto por "Aplicar aos jogos da Steam" (`main.glade:1918`) | TEM |
| `steam_launch_options --status` | nenhuma | NÃO TEM |
| `steam_launch_options --strip` | nenhuma | NÃO TEM |

O padrão é o mesmo dos dois lados: **a janela sabe fazer, não sabe desfazer nem
mostrar o que fez.** `--unlock` e `--strip` estão descritos no próprio argparse
como o caminho do `uninstall` (`proton_pin.py:1155`, `steam_launch_options.py:984`),
o que quer dizer que hoje desfazer só acontece desinstalando o projeto inteiro.

## O terceiro dono da máscara: o applet COSMIC

O commit de AUTO-01 registra o que ficou de fora:

> *"o applet COSMIC tem um terceiro dono da máscara, pela mesma porta, e ficou
> fora do escopo."*

Confirmado e medido. AUTO-01 estabeleceu que **o dono da máscara é o daemon**: a
janela só manda o campo `flavor` quando houve escolha explícita, e sem ele o
daemon preserva a que está valendo (`app/actions/mode_transition.py:92-97`):

```python
        ligar: dict[str, Any] = {"enabled": True}
        if flavor:
            ligar["flavor"] = flavor
```

O applet **sempre** manda o campo (`packaging/cosmic-applet/src/app.rs:866`):

```rust
            ipc::set_gamepad_emulation(true, Some(&flavor)).await
```

E quando o estado do daemon ainda não chegou, o valor vem de uma constante local
(`app.rs:332-336`, com `DEFAULT_FLAVOR` em `app.rs:51`). Nesse instante — popover
aberto antes do primeiro refresh, que roda a cada 700 ms (`app.rs:42`) — o applet
**impõe** `xbox` em vez de preservar. É o mesmo defeito de AUTO-01.5, com o
mesmo mecanismo, numa terceira porta.

Vale dizer o que o applet já acertou, porque explica por que isto é resíduo e não
regressão: o comentário em `app.rs:47-50` conta que a constante já foi `dualsense`
enquanto daemon e janela usavam `xbox`, e o HARM-08 unificou o valor. O que
sobrou não é o valor divergente — é a **regra** divergente: janela omite, applet
afirma.

Isto é fricção do mesmo tipo que o resto da sprint, embora do lado avesso: aqui a
mesma decisão mora em **três** lugares em vez de nenhum. As duas formas custam o
mesmo à mantenedora — ela não consegue prever o que um clique faz.

## O gate de acentuação cego a f-string

Descoberto por outra frente enquanto esta sprint era medida, e registrado aqui
porque é **exatamente a classe de coisa que esta sprint trata**: uma verificação
que só existe no terminal, cujo veredito local diverge do veredito real.

O validador local (`scripts/validar-acentuacao.py`) mascara `COMMENT` e `STRING`
ao varrer um `.py`. Sob **Python 3.12** desta máquina, a PEP 701 quebrou as
f-strings em tokens novos — o miolo vira `FSTRING_MIDDLE`, que não é `STRING` e
portanto **não é mascarado nem enxergado**. A CI roda **3.11**, onde a f-string
ainda é um `STRING` inteiro, e enxerga. Resultado: a CI da `main` reprovou em
cinco commits seguidos com o gate local verde.

Este documento é `.md` e não é atingido — a medição acima não passou por f-string
nenhuma. Mas o achado pertence a esta leva por dois motivos:

1. É uma capacidade que **só existe no terminal** e cujo resultado **depende da
   versão do interpretador que a pessoa tem instalada** — informação que não
   aparece em lugar nenhum da saída do gate.
2. Reforça a regra que a casa já tem (nunca suprimir saída de gate): aqui nem
   suprimir foi preciso, o gate mentiu com a saída à vista.

**Escopo:** o conserto do validador **não é desta sprint** — é do gate, não da
interface, e não tem relação com "o que a mantenedora alcança sem terminal".
Pertence a uma sprint própria de ferramental (sugestão de nome: `GATE-FSTRING-01`),
ou à sprint que já for dona do `validar-acentuacao.py`. O que AUTO-04 registra é
o fato medido e a recomendação: **o gate deve declarar a versão de Python em que
rodou**, e a versão local deve ser a mesma da CI. Um gate que passa aqui e falha
lá é um gate que não serve para decidir nada.

## O que fica no terminal, e por quê

Espelhar tudo seria trocar um defeito por outro. A janela tem custo de atenção:
cada botão a mais é uma decisão a mais que ela precisa entender antes de jogar.
O corte é por **quem é a pessoa que precisa daquilo**.

### Família A — pertence à janela (é da usuária)

São capacidades que decidem **como o produto se comporta na sessão dela**:

- `mic mute` / `unmute` / `release` — desmutar o próprio microfone. O ponto de
  fiação já está escrito (`ipc_bridge.py:544`).
- `mic promote` / `demote` — "usar este microfone como o padrão do sistema" é
  uma escolha de uso, não de manutenção.
- a rota curta do microfone (`doctor.sh --fix-mic`) — hoje sem porta em lugar
  nenhum, nem na CLI.
- `coop off` — se "Preparar co-op" é um botão, desligar tem de ser também.
- `daemon enable` / `disable` — "o Hefesto liga sozinho quando eu entro" é
  decisão de produto. A janela já **lê** esse estado (`daemon_actions.py:1695`) e
  não deixa mudá-lo.
- `proton_pin --unlock` e `--report`, `steam_launch_options --status` e `--strip`
  — desfazer e ver o que foi feito, do lado do que a janela já sabe fazer.
- `version` — quando ela reportar um problema, é o primeiro dado pedido.

### Família B — é de quem desenvolve, fica no terminal

São capacidades cujo público é quem mexe no código, e cujo mau uso quebra a
sessão:

- `daemon start --foreground --poll-hz --headless --reconnect` — rodar o daemon
  no terminal em primeiro plano é depuração. Um botão "rodar em primeiro plano"
  na janela produziria dois daemons disputando o socket, que é justamente o que
  `daemon/main.py:39` existe para impedir.
- `test trigger --raw` (sete bytes HID crus) e `test rumble --weak/--strong` —
  são bancada de teste do protocolo. Os presets da janela cobrem o uso real, e
  `--raw` escreve HID arbitrário no controle.
- `plugin list` / `reload` — plugins são extensão de terceiros. Enquanto não
  houver nenhum instalável pela janela, uma lista vazia é ruído. **Ressalva
  registrada:** se plugins virarem produto para ela, isto muda de família na
  hora, e a sprint que os tornar instaláveis herda a superfície.
- `profile show` (JSON bruto) e `profile create` (perfil mínimo para editar à
  mão) — o editor da aba Perfis é a superfície da usuária; o JSON cru é para
  quem escreve perfil na unha.
- `doctor --quiet`, `--watch-dropout`, `--suggest-port` — diagnóstico de sessão
  de investigação.
- `daemon install-service` / `uninstall-service` — instalação. O botão condicional
  já cobre o caso em que a instalação saiu torta.
- `tui` e `tray` — são interfaces alternativas, não capacidades ausentes.

O critério, em uma frase: **vai para a janela o que muda como o controle se
comporta enquanto ela joga; fica no terminal o que só faz sentido com o código
aberto do lado.**

## Entregas

1. **Corrigir o checklist.** `2026-07-25-CHECKLIST-validacao-em-hardware.md:109`
   deixa de mandar rodar um comando inexistente. É uma linha, e é a entrega mais
   barata desta sprint — hoje o procedimento oficial de validação do projeto
   falha no passo 6.

2. **A CLI passa a repassar `--fix-mic` ao `doctor.sh`.** Três linhas em
   `cli/cmd_doctor.py:99-107`, no mesmo molde de `--fix` e `--quiet`. Enquanto o
   `doctor.sh` não estiver no PATH, a CLI é a única porta que existe — e ela
   fecha a porta certa. Rever, no mesmo passo, se `--watch-dropout` e
   `--suggest-port` também devem passar (são diagnóstico, família B, mas hoje
   estão inalcançáveis por qualquer porta instalada).

3. **O microfone ganha botão na aba Status.** Camada 3 (`mic mute`/`unmute`/
   `release`) ao lado do medidor, no ponto que `ipc_bridge.py:544` já especifica,
   incluindo a releitura do `daemon.state_full` que aquele comentário exige —
   jamais guardar o valor mandado como se fosse leitura. Hoje o selo diz MUDO
   (`sensor_widgets.py:100`) e não oferece saída.

4. **A cura das camadas 1 e 2 ganha caminho na janela.** O botão "Aplicar
   correções" (`main.glade:1904`) passa a rodar também
   `fix_wireplumber_default_source.sh --unmute-routes`, ou ganha um botão
   próprio. Medido: nenhum caminho da janela chega lá hoje
   (`daemon_actions.py:487-489` roda `--install`, que é outro modo).

5. **Desfazer, do lado de quem fez.** `proton_pin --unlock` e
   `steam_launch_options --strip` ganham botão ao lado dos que já existem
   (`main.glade:1925` e `:1918`); `--report` e `--status` viram a leitura que
   informa esses botões. Hoje desfazer só acontece desinstalando o projeto.

6. **O auto-start no boot vira decisão dela.** `daemon enable`/`disable` ganham
   interruptor na aba Sistema, ao lado do estado que a janela já lê
   (`daemon_actions.py:1695`).

7. **`coop off` e a versão aparecem.** Duas ausências pequenas e óbvias: o
   contrário do botão que AUTO-01 criou, e o número que toda conversa sobre um
   problema começa pedindo.

8. **O applet para de impor a máscara.** `app.rs:332-336` passa a omitir o campo
   quando não há escolha explícita, exatamente como `mode_transition.py:92-97`.
   Fecha o terceiro dono que o commit de AUTO-01 deixou anotado.

9. **Os dois módulos por caminho viram subcomandos.** `proton_pin` e
   `steam_launch_options` entram na CLI (`hefesto-dualsense4unix proton …`,
   `… steam-launch …`), e o `install.sh` passa a citar o subcomando em vez do
   caminho absoluto (`install.sh:2238`, `:2271`, `:2278`, `:2281`). Não é a cura
   — a cura é o botão — mas é a diferença entre "copie este caminho de 78
   caracteres" e "rode este comando".

10. **Escrever o mapa, para AUTO-02 e AUTO-03 não precisarem remedi-lo.** A
    tabela CLI × janela desta sprint é o mapa que os "29 pontos" nunca tiveram.
    Ela vive aqui; quem fechar AUTO-02 ou AUTO-03 atualiza esta tabela em vez de
    começar de novo.

## Ordem de execução

1. **Entrega 1** — uma linha, e o checklist volta a funcionar.
2. **Entregas 2 + 3 + 4** — o microfone deixa de exigir terminal. É o buraco mais
   fundo medido: três camadas de mute e zero portas.
3. **Entregas 6 + 7** — as ausências baratas.
4. **Entregas 5 + 8** — desfazer e o terceiro dono da máscara.
5. **Entrega 9** — os módulos por caminho.

## Como validar

1. `bash scripts/doctor.sh --fix-mic` (dentro do repositório) e
   `hefesto-dualsense4unix doctor --fix-mic` produzem **o mesmo resultado**. Hoje
   o segundo sai com `exit=2` e `No such option`.
2. Seguir a seção 6 do checklist de hardware do começo ao fim, **copiando e
   colando**, sem improvisar: nenhum comando falha.
3. Com o microfone mudo pelas três camadas: desmutar **só pela janela**, sem
   terminal, e o medidor da aba Status se mexer quando ela falar.
4. Ligar e desligar o auto-start no boot pela janela; confirmar por
   `systemctl --user is-enabled hefesto-dualsense4unix.service`.
5. Desligar o co-op pela janela (hoje só há como ligar).
6. Travar e **destravar** o Proton pela janela; `python3 …/proton_pin.py --report`
   confirma os dois estados.
7. Abrir o popover do applet **antes** do primeiro refresh e escolher "Jogar pelo
   Hefesto" com a máscara do daemon em `dualsense`: a máscara **continua**
   `dualsense`. Hoje vira `xbox` (`app.rs:336`).
8. `hefesto-dualsense4unix --version` e a janela dizem o mesmo número.
9. Rodar o instalador do começo ao fim: nenhuma mensagem manda copiar
   `python3 /caminho/longo/....py --alguma-coisa`.

## O que não foi medido

Registrado por honestidade, para ninguém tratar como verificado:

- **Não rodei nada que altere o sistema.** Nenhum `--fix`, `--apply`, `--migrate`,
  `--lock`, `--unlock`, `--strip`, nem o instalador. As afirmações sobre o que
  esses caminhos fazem vêm de leitura de código com `arquivo:linha`, não de
  execução.
- **Não abri a janela.** A coluna "janela" desta tabela é leitura de
  `gui/main.glade` e de `app/actions/*.py`; um botão presente no arquivo mas
  escondido em tempo de execução apareceria aqui como existente. O caso do
  `btn_migrate_to_systemd` (`main.glade:1814`, `visible=False`) foi pego por
  leitura — pode haver outros.
- **Não medi o applet em execução**, só o código-fonte
  (`packaging/cosmic-applet/src/app.rs`). A janela de tempo em que ele impõe
  `xbox` é uma leitura do fluxo (`app.rs:332-336` com `REFRESH_MS = 700`), não uma
  medição cronometrada.
- **Não medi a TUI** (`hefesto-dualsense4unix tui`). Ela pode cobrir capacidades
  que a janela GTK não cobre; se cobrir, isso muda o veredito de alguns itens de
  "só existe no terminal" para "existe em outra interface, também de terminal" —
  o que, para a mantenedora, dá no mesmo.
- **Não medi o `--help` do `install.sh`**, apontado por AUTO-01 como truncado.
- **O gate de acentuação cego a f-string** foi reportado pela coordenação, não
  reproduzido por mim. O que registro é o relato e a recomendação; a
  reprodução pertence à sprint que herdar o conserto.

## Critério que resume

**Nada que decida como o controle se comporta enquanto ela joga pode exigir um
terminal — e nenhum documento do projeto pode mandar rodar um comando que não
existe.**
