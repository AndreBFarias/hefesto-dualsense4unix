# As três faixas, depois da v0.4.0 — levantamento de 30/07/2026

- **Levantado em:** 30/07/2026, sobre `HEAD e74077c`, com a **v0.4.0 publicada**
  hoje (`pyproject.toml:7`), na branch `restauro/inicio-da-sessao`
- **Pedido dela, literal:** *"materializa as 3 faixas pra atacarmos depois de
  reiniciarmos"*
- **Serve para:** ela escolher, depois do reinício, sabendo o que ficou de pé, o
  que foi fechado ontem e o que nunca teve uma linha de código
- **Faixa medida:** `git log e8e18b9..HEAD` — oito commits, de `f319c6f` a
  `e74077c`

## A regra de leitura deste índice

**O campo `Status:` dos documentos não é fonte.** Medido agora nos 52 arquivos
de `docs/process/sprints/`: 48 têm o campo, **40 dizem ABERTA** e só 3 dizem
ENTREGUE. Entre os que dizem ABERTA estão EMPATE-01, PALAVRA-01, PORTÃO-VIVO-01,
MIC-PRESENTE-01 e STATUS-SIMETRIA-02 — todas provadamente fechadas antes desta
sessão. Nos oito commits de ontem apenas **três** documentos de sprint foram
tocados (`git log --name-only e8e18b9..HEAD -- docs/process/sprints/`):
JANELA-CEGA-01, EMULAÇÃO-NO-JOGO-01 e PERFIL-SALVA-TUDO-01. Nenhum cabeçalho foi
atualizado.

O estado deste índice vem de cruzar cada pedido com a árvore de hoje, arquivo por
arquivo e linha por linha. Onde eu não medi, está escrito que não medi.

## O que a v0.4.0 fechou, em uma tela

Isto **não precisa ser reaberto**. Cada linha tem onde conferir.

| O que fechou | Onde está hoje | Commit |
|---|---|---|
| O R1 parou de virar Alt+Tab dentro do jogo: o teclado emulado ganhou interruptor próprio, flag persistida, `keyboard.emulation.set` e bloco no `state_full` | `utils/session.py`, `daemon/ipc_handlers.py`, `daemon/subsystems/keyboard.py`, `app/actions/emulation_actions.py` (nove módulos marcam `EMULACAO-NO-JOGO-01`) | `2bbfa22` |
| A exclusão mútua do poll loop parou de ler "vpad ausente" como permissão | `daemon/lifecycle.py:1813` (`_liberar_emulacao_de_desktop`, com flush da tecla presa) | `2bbfa22` |
| O perfil novo salvo pelo rodapé voltou a nascer vencendo (a prioridade havia caído para 0) | `tests/unit/test_footer_salvar_nasce_acima_dos_catch_all.py` | `2bbfa22` |
| O perfil passou a guardar modo, máscara, co-op e modo jogo, com portão por AST provando que registrar não aplica | escritores nas abas Início e Emulação; portão AST no teste da leva | `665aff7` |
| O microfone: o `doctor.sh` reprova fonte padrão que seja MONITOR e filtra entrada sem porta usável | `scripts/doctor.sh:605` (`check_default_source_monitor`), `:660` (`fix_default_source_monitor`), `:505` (classificação pelo sufixo `.monitor`) | `665aff7`, `84c0f83` |
| A cura do `--fix-mic` de `84d9f4e`, que só existia na `main`, foi portada | `scripts/doctor.sh` mais 113 testes de microfone | `665aff7` |
| Empacotamento: caminho de ativação do `.deb`, regras 82/83/84 no Arch e no Fedora, `hid-playstation` desregistrado na remoção, `%files` do Fedora, flake Nix, epoch nos três, Flatpak com versão no nome e semeando perfis, guarda de CI no release | `packaging/arch/PKGBUILD:129-131`, `packaging/fedora/hefesto-dualsense4unix.spec:137-139` e `:339-341`, `.github/workflows/release.yml` | `f319c6f` |
| As fontes da identidade visual passaram a ser instaladas (bloco B1 da PROMESSA-NÃO-CUMPRIDA-01) | `install.sh:2085` e `:1969` chamam `scripts/install_fonts.sh`; `--no-fonts` documentado em `:130` | `665aff7` |
| Portões: hook de acentuação lendo N arquivos, força 8 do gatilho deixando de virar 0, `--no-systemd` honrando a resposta dela, `--help` completo, lápide do `xlib_window`, paridade DKMS sem falso-verde, portão contra Gtk falso | `install.sh`, `integrations/xlib_window.py` (lápide), `tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py` | `f319c6f`, `665aff7` |
| Janela: três rótulos de gatilho em português, linha do detector na aba Sistema, texto do PS+Options, barras de vibração contidas, interruptor do teclado | `app/actions/trigger_specs.py:161`, `app/actions/daemon_actions.py:142-160`, `gui/main.glade:1281`/`:1374`/`:1400` | `2bbfa22` |
| Documentação: README, quickstart e flatpak apontando para a tag; seção do controle no cabo USB | `README.md`, `docs/` | `665aff7` |
| CI: a linha do detector deixou de derrubar três testes do estado do daemon; o teste do gate do R1 deixou de depender do relógio | `a49b687`, `e74077c` | — |

---

# FAIXA 1 — o que ainda desfaz o trabalho dela

| Sprint | O que falta hoje | Evidência | Impacto |
|---|---|---|---|
| [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | entregas 1, 3, 4 e 6 inteiras; a 5 está **parcial** | `profiles/manager.py:206-208`; `profiles/autoswitch.py:237`; `app/actions/home_actions.py:981-989` | a queixa de maior impacto da casa, e a única que apaga trabalho já feito |
| **AUTOMATISMO-MORTO-01** (documento de outro agente) | o autoswitch continua travado, pelos dois lados | `~/.config/hefesto-dualsense4unix/autoswitch_locked.flag` existe, 2 bytes, conteúdo `1`, mtime 28/07 18:18; **5 dos 15 perfis dela são catch-all** | ela desligou o automatismo em 24/07 e ninguém religou; e mesmo desligado o empate já mordia |
| **ÁRVORE-DIVERGENTE-01** (documento de outro agente) | 17 commits vivos na `main` que **não estão** na árvore que roda | `git rev-list --left-right --count main...HEAD` devolve `17 24` | a máquina dela roda o lado direito; metade das curas de 25-26/07 está só no lado esquerdo |
| [DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) | a cura R-D; o remendo de 26/07 continua sendo o que segura | nenhum arquivo desta sprint aparece em `git log --name-only e8e18b9..HEAD` | entra em cena quando ela liga a exceção de Steam Input de um jogo |
| [EMPATE-01](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md), só a **E2** | a aba Perfis não mostra que existe disputa | `app/actions/profiles_actions.py:140` traduz `"any"` para `"Sempre"` e nada mais | três perfis empatados aparecem idênticos na coluna *Quando usar* |

## PERFIL-JOGO-01 — o que continua aberto, entrega por entrega

**Entrega 1 (rodar o experimento e nomear o sintoma): ABERTA.** Continua sem
reprodução controlada. Os números de flapping que sustentam a sprint são de
26/07.

**Entrega 2 (o número dela nunca é sobrescrito sem autoridade de jogo): NÃO
MEDIDA por mim.** O portão existe e é consultado — `core/backend_pydualsense.py:1095`
define `_game_wins()` e `:2793` o consulta dentro de `set_game_output_for` — mas
eu **não** conferi se `player_leds` é retido junto com `led` quando o portão
fecha, nem se existe o teste que morde que a entrega pede. Fica como medição
pendente, não como afirmação.

**Entrega 3 (o cadeado deixa de ceder a perfil casado por título): ABERTA.**
`profiles/autoswitch.py:260` continua chamando `perfil_e_regra_de_jogo(profile, info)`
como a exceção do cadeado, e o predicado continua aceitando o que casa por título
de janela. Um preset genérico que case `|Portal 2|` no título ainda fura o
cadeado dela.

**Entrega 4 (o modo jogo para de soltar no alt-tab): ABERTA, com o alvo
reclassificado.** A linha `profiles/autoswitch.py:237`
(`self._sincronizar_modo_jogo_padrao(motivo, info)`) continua rodando **antes** do
cadeado — mas ela deixou de ser defeito acidental: `:234-238` traz a justificativa
escrita (MODO-01/B3, *"o cadeado congela a decisão de PERFIL, não a de MODO"*).
O que falta é a **histerese**: nada nessa cadeia trata a janela da Steam como
parte da sessão de jogo. Quem for atacar isto vai mexer numa decisão já tomada e
documentada, então a entrega precisa ser reescrita antes de virar código.

**Entrega 5 (a tela diz quando alguém mexeu): PARCIAL, e a parte que existe é
antiga.** `app/actions/home_actions.py:981-989` monta `origin_bits` e escreve
"nativo ligado pelo perfil ativo" e "gamepad ligado pelo perfil ativo" num rótulo
(`self._home_origin_label`, criado em `:672-676`). Isso cobre **modo**, e só.
Cuidado com a tentação de creditar isto ao trabalho de modo desta sessão:
`git log -S "_home_origin_label"` e `git log -S "gamepad ligado pelo perfil ativo"`
apontam para `646cadf`, `c106ee3` e `26456fa` — nenhum dos oito commits de ontem.
Continuam **sem** frase na tela: a cor da lightbar, o número de jogador, e qual
preset entrou pelo título da janela. A entrega 5 não está paga.

**Entrega 6 (desfazer ou assumir a migração de 18:28): ABERTA, e é decisão dela.**
Medido agora nos arquivos dela: `acao.json`, `aventura.json`, `corrida.json`,
`esportes.json`, `fps.json` e `coop_local.json` continuam com
`mode: {kind: gamepad, gamepad_flavor: xbox}` gravado em disco, com mtime de
25/07 18:28. `sackboy_nativo.json` e `vitoria.json` gravam `dualsense`. Reverter
código não reverte arquivo de configuração.

**O que a v0.4.0 NÃO mudou aqui:** `profiles/manager.py:206-208` continua fazendo
`apply` mais `apply_keyboard` mais `apply_emulation` em sequência a cada ativação,
ou seja, reaplicando gatilhos, teclado e emulação por cima do que ela deixou. O
`relatorio` de out-param (`:200-206`) conta a verdade para o IPC, mas ninguém a
mostra na janela.

## AUTOMATISMO-MORTO-01 — os dois lados, medidos

O documento próprio está sendo escrito por outro agente. Aqui fica só a linha do
índice, com os números para ele não ter de remedir.

**Lado (a) — o cadeado.** `~/.config/hefesto-dualsense4unix/autoswitch_locked.flag`
existe, tem **2 bytes**, conteúdo `1`, mtime **28/07 18:18**. Enquanto ele estiver
ligado, o `_tick` só cede à regra específica do jogo (`profiles/autoswitch.py:260`).

**Lado (b) — os perfis dela.** São **15** arquivos `.json` em
`~/.config/hefesto-dualsense4unix/profiles/`. Destes, **5 são catch-all**
(`match: {"type": "any"}`):

| Perfil | Prioridade | Modo gravado |
|---|---|---|
| `fallback.json` | 0 | nenhum |
| `vitoria.json` | 0 | `gamepad` / `dualsense` / `coop: true` |
| `meu_perfil.json` | 1 | nenhum |
| `pragmata.json` | 5 | nenhum |
| `pragmata2.json` | 5 | nenhum |

Os outros **10** casam por critério, com prioridades de 10 a 80:
`bow` (10), `navegacao` (50), `corrida` (55), `esportes` (55), `fps` (60),
`point_and_click` (60), `acao` (65), `aventura` (70), `coop_local` (75),
`sackboy_nativo` (80).

O que isto significa: os cinco catch-all disputam **toda** janela que não case
com um dos dez específicos, e `pragmata` e `pragmata2` empatam em 5 — são dois
arquivos **idênticos byte a byte fora o campo `name`** (medido: o `diff` dos dois
JSON normalizados devolve exatamente uma diferença, na linha 36). O desempate por
incumbente entrou em `8d7fd45` e o alfabeto deixou de decidir, mas dois arquivos
gêmeos disputando a mesma prioridade continuam sendo uma armadilha que a tela não
mostra (ver EMPATE-01/E2, abaixo).

## ÁRVORE-DIVERGENTE-01 — quantos, e quais importam

Medido: `git rev-list --left-right --count main...HEAD` devolve **17 24**. Ou
seja, 17 commits vivos só na `main` e 24 vivos só na árvore que roda na máquina
dela. O documento é de outro agente; aqui ficam os números e a triagem.

Dos 17 da `main` (`git log --oneline main --not HEAD`), os que carregam código
que ela sente:

- `84d9f4e` — o `--fix-mic` que a medição refutou. **Já portado** nesta sessão
  (`665aff7`), então este perdeu urgência.
- `9c944a8` — o ciclo `uninstall` mais `install` desligava seis curas de módulo em
  silêncio. `grep -c hefesto-hid-playstation install.sh` no HEAD devolve **5**
  ocorrências, o que sugere que parte da cura existe aqui — **não conferi
  equivalência**, só presença.
- `0c08e77` — CONTAGEM-01. `grep -rn "CONTAGEM-01" src/` no HEAD devolve **zero**;
  o que existe aqui é a CONTAGEM-E-COOP-01, que é outra coisa.
- `d1177c2` — PLAYER-LED-01. No HEAD existe `FEAT-COOP-PLAYER-LED-01`
  (`daemon/subsystems/coop.py:22`, `:47`, `:115`), que **não é** o mesmo
  identificador. Precisa de comparação real.
- `a3b5b63` — o higienizador apagou o desenho dos LEDs; a cura era `chr(0x25CF)`.
  `grep -rn "0x25CF" src/` no HEAD devolve **zero**. Provável regressão viva.
- `bc827cb`, `ef4b8bc`, `b39fec9` — contagem da aba Status, faixa do microfone e
  layout dos botões. Não conferidos um a um.

Os demais são a release da v0.1.2, correções de CI daquela linha e documentação.

## EMPATE-01, entrega E2 — continua aberta

`app/actions/profiles_actions.py:140` mapeia `"any"` para `"Sempre"` e a coluna
*Quando usar* termina aí. Procurei texto de tela que diga que há disputa:
`grep -rn "empate|disputa" src/hefesto_dualsense4unix/app/` devolve cinco
ocorrências, e **nenhuma** é sobre concorrência entre catch-all — `:191` e `:211`
falam de perfil renomeado, `:983` é comentário, e as de `lightbar_actions.py` são
sobre a camada automática de cor. Com `pragmata`, `pragmata2`, `fallback`,
`vitoria` e `meu_perfil` todos dizendo "Sempre", a aba não tem como explicar por
que um vence.

---

# FAIXA 2 — o que ela vê

| Sprint | O que falta hoje | Evidência | Impacto |
|---|---|---|---|
| [LIGHTBAR-JOGADOR-01](2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | E0 a E5, inteiras | `gui/main.glade:957` ainda rotula "Desenho das 5 luzes"; `app/actions/lightbar_actions.py:907` e `app/app.py:271` seguem vivos | a aba de cor é a que ela mais abre depois da Status, e mostra intenção em vez de realidade |
| [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | E2 a E9; a E1 entrou **só na aba Rumble** | `gui/main.glade:1281`, `:1374`, `:1400` (teto de 400px em três barras); `:1311-1312` declara por escrito que as demais ficaram de fora | a queixa era "a mesma largura em todas as abas" e uma aba foi atendida |
| [SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md) | E1 a E5, inteiras | `grep -rn "SOM-02" src/` devolve **zero** | o alto-falante continua sem volume, sem mudo e sem devolução de posse |
| [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) | três das quatro caixas | a primeira foi paga: `app/mic_monitor.py:58` reconhece `hefesto_dualsense_bt_`; ligar e desligar a ponte, dizer a verdade quando está desligada e mostrar o custo continuam sem código | com quatro controles por rádio, que é o cenário-alvo, ela vê o nível e não manda na ponte |
| [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md) | só o rótulo `Custom` | três rótulos entraram (`trigger_specs.py:161` "Ponto duro" e os dois irmãos); `:209` continua `"Personalizado (avançado)"`, **24 caracteres contra teto de 22** | é decisão de palavra dela; enquanto isso, um modo quebra a linha e sobe o mínimo da grade |
| [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) | o item 0, a frase da regra padrão e o desfazer **dentro da janela** | `remove_appid_from_steam_input_allowlist` (`integrations/steam_launch_options.py:821`) tem um único chamador, e é `cli/cmd_steam.py:215` — terminal, não janela | toda noite ela recomeça a decisão do zero |
| [BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) | entregas 5 e 6 | `on_emulation_open_toml` continua registrado em `app/app.py:320` e implementado em `app/actions/emulation_actions.py:449`, com o glade em `:2483-2489` registrando que o botão saiu e passando a decisão adiante | não morde hoje; vira armadilha quando alguém religar o botão |
| **CONTAGEM-E-COOP-01** | o **aviso** antes de derrubar o co-op | metade paga: a conta única existe (`app/actions/status_actions.py:1444` `_contagem_de_controles`, `:126` `texto_de_contagem`) e o fato é emitido (`daemon/subsystems/gamepad.py:514`, `:525`, `:537`); mas `grep -rn "coop_derrubado" app/` devolve **zero** — a janela não mostra | entrar na exceção de um jogo ainda derruba três jogadores sem ela ver |
| **FONTE-PADRÃO-01, o residual** | a cura só roda no `install` e no `--fix-mic` | medido agora nesta máquina: `pactl get-default-source` devolve `alsa_output.pci-0000_0c_00.4.iec958-stereo.monitor` — a fonte padrão **é um monitor** neste instante | o que qualquer aplicativo gravar agora é o áudio de saída |

## LIGHTBAR-JOGADOR-01 — nenhuma linha entrou

A sprint pede que a aba parta do que **está aceso** e não do rascunho (E0), que o
jogador vire o protagonista (E1), que cor livre saia do caminho principal (E2),
que "Desenho das 5 luzes" deixe de ser painel próprio (E3), que a prévia pare de
mentir (E4) e um teste que morde (E5). Nenhuma foi tocada: o painel continua
rotulado em `gui/main.glade:957` e o handler `on_player_led_toggled`
(`app/actions/lightbar_actions.py:907`) continua vivo e registrado em
`app/app.py:271`.

## LARGURA-01 — o que sobrou, com o preço já medido

A E1 entrou parcialmente e o próprio glade declara o corte:
`gui/main.glade:1305-1312` registra o custo medido (a largura mínima da aba
Rumble sobe de 684px para 707px e a altura de 420px para 430px, contra teto de
1180 e 654) e diz por que **só** a aba Rumble entrou — é a que tem mais folga,
473px. As demais barras da lista *ficaram de fora por escrito*.

Sobram: E2 (miolo do frame Estado), E3 (comprimento de linha do texto corrido),
E4 (teto elástico nas duas abas de coluna única), E5 (teto elástico nas quatro
abas de duas colunas), E6 (Sistema, com o log de fora), E7 (os dois cartões do
topo da Emulação com a mesma largura — hoje 715px de vão), E8 e E9 (Gatilhos).

## GATILHO-PALAVRA-01 — o único rótulo que sobrou tem dono

Os três rótulos de jargão saíram (`trigger_specs.py:161` "Ponto duro", mais
"Rampa de força" e "Curva de força"), e o portão que faltava foi construído:
`tests/unit/test_gatilho_palavra_rotulos.py` trava os dezenove `name` como
contrato de disco, IPC e DSX, e cobra o teto de 22 caracteres.

**"Personalizado (avançado)" tem 24 caracteres** (`trigger_specs.py:209`) e está
dispensado por exceção nomeada, `PENDENCIA_DE_LARGURA = frozenset({"Custom"})`
(`test_gatilho_palavra_rotulos.py:66`). O teste reprova se a lista crescer **e**
reprova se o rótulo passar a caber sem a exceção ser retirada — ou seja, a dívida
não apodrece em silêncio. A sprint recomenda "Montar do zero" (14 caracteres),
com "avançado" descendo para a descrição. **Escolher a palavra é dela.**

## FONTE-PADRÃO-01 — a cura existe, o estado atual não

Isto merece nota porque é fácil confundir com pendência fechada. A cura foi
construída e provada no hardware (`84c0f83`: forçou o monitor, rodou
`doctor.sh --fix-mic`, elegeu `alsa_input.usb-...DualSense...iec958-stereo` e
grudou por cinco leituras em 15 s, com pico 441 e RMS 73 em 6 s de gravação).
Mas, medido agora, com o controle fora da lista de fontes do PipeWire, a fonte
padrão voltou a ser um monitor. A cura não é um vigia: ela roda no `install` e
quando alguém chama `--fix-mic`. **Não medi** se um `--fix-mic` agora corrigiria,
porque isso exige rodar o script com o controle no cabo, e o daemon está vivo.

---

# FAIXA 3 — o que protege a casa

| Item | O que falta hoje | Evidência |
|---|---|---|
| [CHECKLIST de validação em hardware](2026-07-25-CHECKLIST-validacao-em-hardware.md) | **31 caixas vazias, 0 marcadas** — contado agora, não herdado | `grep -c "\- \[ \]"` devolve 31; `grep -c "\- \[x\]"` devolve 0; o último commit que tocou o arquivo é `14cd31b` |
| [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md) | virar rotina; nesta sessão foi cumprida **pela metade** | `84c0f83` rodou `uninstall` mais `install` de verdade com o DualSense no cabo e mediu a gravação; mas `2bbfa22` e `665aff7` dizem, por extenso, que nada foi validado com o olho dela |
| [DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md) | as nove contradições | `git log --name-only e8e18b9..HEAD -- docs/adr/ docs/protocols/` devolve **vazio** — nenhum ADR foi tocado |
| [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md) | B2, B4, C, metade do D, E e F | detalhado abaixo |
| [PALAVRA-01](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md), só a **E5** | o gate que impede a minúscula e o jargão de voltarem | `.pre-commit-config.yaml` declara quatro hooks — `acentuacao-strict` (`:28`), `glifos` (`:40`), `anonimato` (`:46`) e `ruff-check` (`:51`) — e nenhum olha capitalização de texto de tela |
| **As dívidas que a sessão declarou e não pagou** | seis, listadas abaixo | corpos dos oito commits |

## PROMESSA-NÃO-CUMPRIDA-01 — o placar de hoje

**Pagos antes desta sessão:** A1 (gate de emoji, pela GATE-EMOJI-01), A3 (gates
no CI, pela PORTÃO-VIVO-01), A4 (`exigir_gi_real` e o job "Interface com GTK
REAL").

**Pagos NESTA sessão:**

- **B1 — as fontes.** `grep -c install_fonts install.sh` devolve **9**, contra
  zero em 29/07. As chamadas estão em `install.sh:2085` e `:1969`, com
  `--no-fonts` documentado em `:130` e o racional escrito em `:189-190` e
  `:1942-1943`. O bloco B1 está **fechado**.
- **B3 — a ajuda truncada.** O `sed -n '2,128p'` saiu e o `--disable-usb-audio`
  parou de ser sugerido (`f319c6f`).
- **Metade do D — as regras nos manifestos.** `packaging/arch/PKGBUILD:129-131` e
  `packaging/fedora/hefesto-dualsense4unix.spec:137-139` e `:339-341` agora
  empacotam a 82, a 83 e a 84.

**Continuam abertos, medidos hoje:**

- **B2 — a unidade que só existe para ser removida.** `assets/hefesto-dsx-recover.service`
  continua sem ser instalado por nenhum caminho, e continua sendo conhecido por
  `uninstall.sh:250` e `:358-361` e por `scripts/doctor.sh:3101-3105`, que até
  ensina a instalar à mão.
- **B4 — a janela de ordem no install.** As regras 82 e 83 são gravadas no passo 3
  (`install.sh:1219-1220`) e os scripts que elas invocam chegam no passo 3e-bis
  (`install.sh:1547`, `:1454`). Inócuo, mas real.
- **C1 — as métricas sem chave.** `metrics_enabled` continua só como campo de
  dataclass (`daemon/lifecycle.py:190`); `grep -n metrics daemon/main.py` devolve
  **zero**. Não há flag, variável de ambiente nem arquivo que ligue.
- **C2 — os plugins pelo mesmo caminho impossível.**
- **C3 — `SUBSYSTEM_REGISTRY` não é iterado.** `daemon/subsystems/__init__.py:41`
  declara a lista e `:13` avisa, no próprio arquivo, que ninguém a itera em
  produção; `daemon/lifecycle.py:2675` confirma que quem sobe subsistema é o
  `run()`.
- **D, a outra metade — `lib.fakeSha256`.** `packaging/nix/package.nix:79`
  continua com o marcador na derivação do `pydualsense`. O `nix build`
  documentado não funciona sem edição manual, mesmo com o flake que entrou nesta
  sessão.
- **E — a dívida de teste.** `grep -rn "inspect.getsource" tests/` devolve **21**
  ocorrências.
- **F — a janela só fala português.** `grep -c 'msgstr ""'` devolve **107** em
  `po/en.po` e **106** em `po/pt_BR.po`; apenas **9** módulos de `src/` importam
  o `_()`.

## As dívidas que a própria sessão declarou, e não pagou

Cada uma está escrita por extenso no corpo do commit que a deixou. Nenhuma é
surpresa.

1. **O checklist de 22 itens do que ela precisa olhar existe só na conversa.**
   O commit `2bbfa22` registra que o checklist do que ela precisa olhar está na
   conversa desta sessão. Não virou arquivo. Quando a conversa fechar, ele some.
2. **O `display_authority` é grudento e cai sozinho com o jogo aberto.** O
   `2bbfa22` recusou por escrito condicionar o gate do teclado a esse sinal,
   porque ele cai sozinho cerca de 30 s depois com o jogo ainda aberto — defeito
   conhecido e não corrigido. Ele continua vivo e **não tem documento nenhum**.
3. **`window_detect_healthy` no sinal de jogo — a linha que precisa entrar
   sozinha.** `daemon/lifecycle.py:3163` continua lendo
   `self.store.window_detect_healthy` em `_gather_game_signal_inputs`, quando o
   campo que responde "está enxergando AGORA" é `window_detect_seeing`
   (`daemon/state_store.py:459`). Das três pendências da JANELA-CEGA-01, **duas
   foram pagas**: a fiação do motivo existe (`daemon/subsystems/autoswitch.py:144-148`)
   e a linha na aba Sistema entrou nesta sessão
   (`app/actions/daemon_actions.py:142-160`). Sobrou esta, e ela é uma linha que
   não pode entrar de lambuja: a transição de `daemon` para `unknown` chama
   `replay_retained_game_outputs()` e repinta o controle. Precisa dela olhando a
   lightbar.
4. **A lista `DIVIDA_GI_FALSO` tem 17 arquivos.**
   `tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py:50` nomeia os 17
   arquivos de teste que plantam Gtk falso sem `exigir_gi_real`, e o próprio
   comentário diz que é dívida a pagar e não permissão. Medido: 26 arquivos em
   `tests/unit/` plantam `sys.modules["gi"]` e 38 usam `exigir_gi_real`.
5. **Uma leva inteira sem verificador independente.** O `665aff7` abre dizendo
   que o agente verificador da leva caiu duas vezes com erro 529 e que a
   verificação foi feita à mão — e essa verificação achou um defeito que teria
   ido para produção. O processo depende de um agente que pode cair.
6. **"Verde aqui" é afirmação fraca.** O `7a58f1c` deixa a lição escrita: o gate
   de acentuação é cego a f-string no 3.12 e a CI roda 3.10 e 3.11; e um import
   de interface no topo de um teste derruba a **coleta** no runner sem PyGObject,
   em vez de virar skip. Nenhum dos dois seria pego pela validação local. Isto
   ainda não virou regra escrita em lugar nenhum de `docs/`.

Junto, herdada e não encolhida: **as 385 linhas da cascata Wayland** foram
mantidas por decisão escrita em `f319c6f` (são a única matéria-prima para o
detector enxergar janela Wayland nativa), e continuam sem executar nesta máquina.

---

# A ordem que eu atacaria, e por que

**Critério declarado:** primeiro o que apaga trabalho dela, depois o que ela vê
todo dia, depois o que impede a próxima leva de desfazer. Dentro de cada faixa, o
que **não** exige o olho dela vem antes, porque pode ser feito enquanto ela joga.

**Barato, e não precisa dela na frente da tela:**

1. **EMPATE-01/E2** — a coluna *Quando usar* dizer que há disputa. É texto e uma
   função pura em `profiles_actions.py`, e ela tem cinco perfis empatados em
   disco agora. A melhor relação entre esforço e o que ela entende.
2. **CONTAGEM-E-COOP-01, a metade que falta** — o fato já é emitido em
   `gamepad.py:514-537`; falta só a janela consumir. Meia entrega.
3. **PROMESSA-NÃO-CUMPRIDA-01, B2 e a outra metade do D** — apagar a unidade
   fantasma e trocar o `fakeSha256`. Duas linhas cada, risco próximo de zero.
4. **PALAVRA-01/E5** — o quinto hook do pre-commit. Barato, e é o que impede a
   próxima leva de desfazer a janela em português.
5. **BOTÃO-QUE-NÃO-MENTE-01, entregas 5 e 6** — o handler órfão. Faxina pura.

**Precisa dela na frente da tela:**

6. **ÁRVORE-DIVERGENTE-01** — antes de qualquer coisa grande, saber o que ainda
   está só na `main`. É leitura, mas a decisão do que trazer é dela.
7. **A linha de `healthy` para `seeing`** (dívida 3 acima) — uma linha, sozinha,
   com ela olhando a lightbar.
8. **LARGURA-01, E4 e E5** — o teto elástico nas seis abas. É o que ela pediu com
   a frase "a mesma largura em todas as abas", e a SOM-01 já provou que geometria
   medida em `Gtk.OffscreenWindow` não substitui o olho.
9. **PERFIL-JOGO-01** — a mais cara e a de maior impacto. A entrega 1 (o
   experimento) é obrigatória antes de qualquer código, e a entrega 4 precisa ser
   **reescrita** primeiro, porque o alvo dela virou decisão declarada em
   `autoswitch.py:234-238`.
10. **LIGHTBAR-JOGADOR-01** — seis entregas numa aba que ela abre todo dia. Só
    depois da PERFIL-JOGO-01, porque as duas mexem em quem manda na cor.

**Fica por último, e por escolha:** SOM-02 (não entra sem ela decidir o preço da
posse), MIC-BT-01 (cenário de quatro controles por rádio, que não é o de hoje) e
o bloco F da PROMESSA (tradução — trabalho grande e independente).

# O que é decisão dela, e por isso ninguém faz sozinho

1. **O que o R1 deve fazer.** Hoje `core/keyboard_mappings.py` mapeia `r1` para
   `(KEY_LEFTALT, KEY_TAB)` — R1 é Alt+Tab por padrão. O interruptor agora existe
   e o Alt+Tab parou de vazar para dentro do jogo, mas o **padrão** continua sendo
   trocar de aplicativo. Ninguém escolhe outro mapeamento no lugar dela.
2. **Religar ou não o hold do PS.** O gesto está desligado por padrão:
   `integrations/hotkey_daemon.py:47` registra que quem quiser o gesto de volta
   usa `ps_long_press_ms>0`, e o modo jogo hoje é só pelo combo PS+Options
   (`daemon/main.py:94`). Foi desligado porque provocava modo-jogo acidental. A
   aba Emulação já ensina PS+Options; religar o hold é decisão dela, não efeito
   colateral de leva nenhuma.
3. **O que fazer com `pragmata.json` e `pragmata2.json`.** Medido: os dois são
   **idênticos byte a byte fora o campo `name`**, os dois são catch-all
   (`match: {"type": "any"}`) e os dois têm prioridade **5** — a maior entre os
   catch-all dela. Ou um dos dois vira regra específica do jogo, ou um dos dois
   sai, ou eles ficam e a tela passa a mostrar o empate (EMPATE-01/E2). Apagar
   perfil dela sem ela mandar não está em discussão.
4. **A fonte de captura padrão.** O único microfone de verdade desta máquina é o
   do controle. O drop-in 51 existe porque ela reclamou do DualSense virar
   microfone padrão sozinho — mas, sem nenhum outro microfone plugado, rebaixá-lo
   deixa só MONITOR na disputa, e foi exatamente isso que se mediu agora
   (`pactl get-default-source` devolve
   `alsa_output.pci-0000_0c_00.4.iec958-stereo.monitor`). A cura de `84c0f83`
   prefere a entrada do controle; se ela plugar um microfone na placa-mãe, a cura
   passa a preferi-lo sozinha. Manter, afrouxar ou remover o drop-in 51 é decisão
   dela.
5. **A migração de 25/07 18:28 nos presets** (entrega 6 da PERFIL-JOGO-01): seis
   arquivos dela têm `gamepad` e `xbox` gravados em disco. Reverter código não
   reverte arquivo de configuração.
6. **O rótulo `Custom`.** "Personalizado (avançado)" tem 24 caracteres contra
   teto de 22. A sprint recomenda "Montar do zero"; a palavra é dela.

# O que este índice NÃO mediu

Escrito de propósito, para não virar afirmação por omissão.

- **Não rodei a suíte completa.** Os números de teste citados (6.097 em
  `84c0f83`, 6.089 no emblema do `README.md:13`) vêm dos commits e do README, não
  de execução minha.
- **Não abri a janela e não vi a tela.** Toda afirmação sobre interface aqui vem
  de código e de `.glade`, não de renderização. O daemon está vivo e a janela
  dela está aberta; não encostei em nenhum dos dois.
- **Não li o journal do daemon.** Nada aqui é comportamento em execução, exceto
  as duas medições de sistema declaradas: o `autoswitch_locked.flag` e o
  `pactl get-default-source`.
- **PERFIL-JOGO-01, entrega 2:** não conferi se `player_leds` é retido junto com
  `led` quando `_game_wins()` é falso, nem se existe o teste que morde. Sei que o
  portão existe (`core/backend_pydualsense.py:1095`, `:2793`) e nada além disso.
- **ÁRVORE-DIVERGENTE-01:** medi a contagem e li os assuntos dos 17 commits, mas
  **não** fiz `git diff` de nenhum deles contra o HEAD. Onde escrevi "provável
  regressão viva" (o `chr(0x25CF)`) isso é ausência de `grep`, não equivalência
  de comportamento provada.
- **DOC-VERDADE-01:** conferi só que nenhum arquivo de `docs/adr/` nem de
  `docs/protocols/` foi tocado nos oito commits. **Não** recontei as nove
  contradições item a item.
- **As sprints CR-01 a CR-06** continuam fora de escopo por decisão dela e não
  foram cruzadas com o código.
- **A janela compacta (`app/compact_window.py`) e a bandeja (`app/tray.py`)** não
  foram abertas — continuam sendo a candidata SEGUNDA-JANELA-01, herdada do
  índice de 29/07.
- **O applet Rust** e as sprints IDENT-01, MÁSCARA-01, JOGO-01 e LEGIBILIDADE-01
  não foram medidos nesta rodada.
- **Não rodei nenhum portão além dos dois validadores de texto sobre este
  arquivo.** Os códigos de saída de CI citados são os dos commits.
