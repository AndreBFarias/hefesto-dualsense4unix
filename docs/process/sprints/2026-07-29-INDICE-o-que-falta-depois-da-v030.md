# O que falta, depois da v0.3.0 — levantamento de 29/07/2026

- **Aberto em:** 29/07/2026, a pedido dela: *"veja as sprints que faltam por
  fazer, e veja o que podemos melhorar delas ou adicione as novas sprints"*
- **Faixa medida:** `git log 5489c2a..HEAD` — oito commits, de `e8f9060` a
  `2c18504`, publicados em `restauro/inicio-da-sessao`
- **Serve para:** ela escolher a próxima leva sabendo o que está de pé, o que
  ficou pela metade, e o que ainda nem tem documento

## A regra de leitura deste índice

**O campo `Status:` dos documentos não é fonte.** Medido agora, nos 45 arquivos
de `docs/process/sprints/`: 39 têm o campo, e **36 deles dizem ABERTA** — entre
os quais EMPATE-01, PORTÃO-VIVO-01, PALAVRA-01, MIC-PRESENTE-01 e
STATUS-SIMETRIA-02, todas provadamente entregues. Só três dizem ENTREGUE
(VÃO-01, SOM-01 e a parcial JANELA-CEGA-01), e a única razão é que esses três
foram escritos ou editados na mesma leva que os fechou.

O estado real deste documento vem de cruzar cada sprint com o código da árvore e
com o corpo dos commits desta sessão, que declaram as pendências por extenso.

## O que entrou nesta sessão, em uma linha

O rodapé parou de mentir; o desempate entre perfis deixou de ser o alfabeto; a
aba Status ganhou moldura, microfone permanente e coluna do som; a janela expande
até 1400 px; o microfone grava ela e não o jogo; o medidor por Bluetooth voltou a
existir; 737 testes de interface deixaram de passar contra um GTK falso; e o
detector de janela passou a poder adoecer. Publicada a **v0.3.0**
(`pyproject.toml:7`), com **5783 testes** (`README.md:13`).

## Faixa 1 — o que ainda desfaz trabalho dela

| Sprint | O que falta | Evidência no código | Impacto para ela |
|---|---|---|---|
| [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | as cinco entregas inteiras: modo de jogo entrando uma vez por sessão, cadeado cedendo só à regra do jogo, a linha em português dizendo o que mudou sozinho, o botão "Voltar ao que eu deixei" e o teste que morde | `profiles/autoswitch.py:237` continua chamando `_sincronizar_modo_jogo_padrao` antes do cadeado; `daemon/lifecycle.py:1812` continua escrevendo que o cadeado não é consultado nesse caminho; `profiles/manager.py:206-208` continua reaplicando gatilhos, teclado e emulação por cima do que ela deixou | É a queixa de maior impacto da casa e a única que apaga trabalho já feito. Nenhuma linha desta sprint entrou nesta sessão |
| [EMPATE-01](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md) | **só a E2** — a aba Perfis não mostra que existe disputa | `app/actions/profiles_actions.py:140` ainda traduz `"any"` para `"Sempre"` e nada mais; três perfis empatados aparecem idênticos na coluna *Quando usar* | A cor voltou a ser dela, mas a tela continua sem explicar por que um perfil vence o outro. É a mesma cegueira que fez esta sprint ser rebaixada por engano em 27/07 |
| [DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) | a cura R-D; o remendo de 26/07 continua sendo o que segura | quatro joysticks para um controle, medido na leva de 26/07; nenhum arquivo desta sprint foi tocado em `git log 5489c2a..HEAD` | Entra em cena quando ela liga a exceção de Steam Input de um jogo |

## Faixa 2 — o que ela vê

| Sprint | O que falta | Evidência no código | Impacto para ela |
|---|---|---|---|
| [LIGHTBAR-JOGADOR-01](2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | E0 a E5 inteiras: a aba parte do rascunho e não do que está aceso; o painel "Desenho das 5 luzes" continua sendo caixa própria | `gui/main.glade:957` ainda rotula o painel; `app/actions/lightbar_actions.py:907` (`on_player_led_toggled`) segue vivo e registrado em `app/app.py:271` | A aba de cor é a que ela mais abre depois da Status, e ainda mostra intenção em vez de realidade |
| **CONTAGEM-E-COOP-01** (sem documento) | o número único na janela inteira e o aviso antes de derrubar o co-op | três denominadores vivos e divergentes: `app/actions/status_actions.py:1063` soma `conectados + externals`, `:1391` e `:1504` usam só `len(conectados)`, e `app/actions/home_actions.py:340` usa `len(controllers)`; `daemon/subsystems/gamepad.py:473-475` chama `coop.disable()` sem perguntar nada antes | Com dois DualSense e dois externos a mesma tela diz números diferentes; e entrar na exceção de um jogo derruba três jogadores em silêncio |
| [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) | o item 0 (medir se a Steam honra a exceção por jogo), a frase da regra padrão e o desfazer **dentro da janela** | `grep` por "entrada Steam fica desligada" no `gui/main.glade` e nas actions devolve zero; `remove_appid_from_steam_input_allowlist` já tem chamador, mas em `cli/cmd_steam.py:215` — terminal, não janela | Toda noite ela recomeça a decisão do zero. O guarda, esse sim, voltou a ter próximo disparo (`hefesto-steam-input-guard.timer`, medido hoje com disparo em 12 minutos) |
| [BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) | entregas 5 (menos superfície) e 6 (o terceiro teste, o que morde) | o handler `on_emulation_open_toml` continua registrado em `app/app.py:320` e implementado em `app/actions/emulation_actions.py:274`, embora `gui/main.glade:2374` registre que o botão saiu | Não morde hoje; é dívida de limpeza que vira armadilha quando alguém religar o botão |
| [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) | três das quatro caixas: ligar e desligar a ponte pela interface, dizer a verdade quando ela está desligada, e mostrar o custo antes de ligar | a primeira caixa foi paga nesta sessão — `app/mic_monitor.py:58` reconhece o prefixo `hefesto_dualsense_bt_`; as outras três continuam sem código | Com quatro controles por Bluetooth, que é o cenário-alvo declarado, ela vê o nível mas não manda na ponte |

## Faixa 3 — o que protege a casa

| Sprint | O que falta | Evidência | Impacto para ela |
|---|---|---|---|
| [PALAVRA-01](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md) | **só a E5** — o gate que impede a minúscula e o jargão de voltarem | `.pre-commit-config.yaml` declara quatro hooks (`acentuacao-strict`, `glifos`, `anonimato`, `ruff-check`) e nenhum olha capitalização de texto de tela | A janela está certa hoje; nada impede a próxima leva de desfazer |
| [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md) | virar rotina, não regra escrita | foi aplicada pela primeira vez nesta sessão, declarado em `464b7a2`; o [CHECKLIST de hardware](2026-07-25-CHECKLIST-validacao-em-hardware.md) continua com **zero** caixas marcadas e 31 vazias | É o único portão que pega "isso ficou pior", que é a classe que causou o rollback de 26/07 |
| [DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md) | as nove contradições entre documento e código | nada dela foi tocado nesta sessão | Não morde numa noite de jogo; morde em quem for ler o projeto |
| [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md) | os blocos B, C, D e F. Os blocos A1, A3 e A4 foram pagos | A1 pago pela GATE-EMOJI-01; A3 pago pela PORTÃO-VIVO-01; **A4 pago nesta sessão** (`tests/conftest.py:203`, `exigir_gi_real`, mais o job "Interface com GTK REAL" em `.github/workflows/ci.yml:277`). **B1 continua de pé**: `grep -c fonts install.sh` devolve **zero**, e `gui/theme.css:65` pede `Space Grotesk` | Na máquina dela as duas fontes existem (`fc-list` acha 4 faces de Space Grotesk e 16 de JetBrains Mono) — então B1 não morde nela, morde em instalação nova |

## Faixa 4 — abertas, sem urgência

| Sprint | Estado real |
|---|---|
| [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md) | aberta desde 25/07, intacta. O 8BitDo muda de MAC ao mudar de modo e vira dois controles no registro |
| [MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) | aberta, depende da IDENT-01 |
| [PLAYER-LED-01](2026-07-25-PLAYER-LED-01-o-numero-do-jogo-chega-ao-controle.md) | metade da entrega 4 continua declarada em aberto no próprio documento |
| [CONTAGEM-01](2026-07-25-CONTAGEM-01-a-tela-diz-dois-com-quatro-na-mesa.md) e [UI-SELETOR-01](2026-07-25-UI-SELETOR-01-ordem-dos-controles-no-seletor.md) | absorvidas pela CONTAGEM-E-COOP-01, que continua sem documento |
| [CR-01](2026-07-25-CR-01-posicao-juridica.md) a [CR-06](2026-07-25-CR-06-devolver-ao-ecossistema.md) | fora de escopo por decisão dela, mantida |

## O que ficou PARCIAL nesta sessão — exatamente o que sobrou

Cada item abaixo está declarado por extenso no corpo do commit que o deixou para
trás. Nenhum é surpresa; todos são dívida assumida na hora.

### 1. JANELA-CEGA-01 — a linha de uma linha

O commit `b3e8b7f` entrega a observabilidade e deixa **três** coisas escritas:

- **A fiação do motivo.** `window_detect_reason` sai `null` no daemon vivo
  porque quem chama o store é `daemon/subsystems/autoswitch.py`, que não estava
  no escopo. O ponto exato está transcrito na própria sprint.
- **A troca de `healthy` por `seeing`** em `_gather_game_signal_inputs`. É uma
  linha, e ela **precisa entrar sozinha**, com ela olhando a lightbar: hoje a
  transição `daemon -> unknown` chama `replay_retained_game_outputs()`, que
  repinta o controle com o resíduo do jogo. Entregar de lambuja seria dar um
  vaivém de cor no controle dela.
- **A linha na aba Sistema** dizendo *"o detector não vê janela Wayland
  nativa"*. Barata agora que os campos existem no `state_full`, mas a aba não
  estava entre os arquivos liberados.

### 2. SOM-01 — o que foi decidido ficar de fora

- O frame "Estado" do glade **não** cresce com a janela; só o piso subiu para
  1040 px. Dar-lhe o mesmo corte elástico exige código próprio.
- O glifo do card **compacto** não cresceu. Decisão declarada, com preço medido:
  o grid maior custa 112 px por card e a folga da aba com dois cards é de 116 px.
- O alto-falante continua **sem controle de volume**, e o item que trava isso é
  decisão dela: o primeiro clique tira do firmware o controle do volume e não há
  leitura para confirmar a devolução.
- **Nada da SOM-01 foi validado na tela dela.** As medidas são de
  `Gtk.OffscreenWindow`.

### 3. STATUS-SIMETRIA-02 e MIC-PRESENTE-01 — a moldura que não cabe

Registrado em `8d7fd45`: com dois cards lado a lado a moldura dos blocos não
entra, porque o orçamento de largura da aba nesse caso é de 26 px. É decisão
escrita, com teste que a trava — e é o tipo de coisa que ela pode querer reverter
pagando uma janela mais larga.

### 4. APLICAR-VERDADE — fechada em duas etapas, e a segunda tem nome só no commit

`e8f9060` curou a frase do rodapé e declarou que o `ok` interno continuava
sempre `True`. `b3e8b7f` fechou isso, separando "o daemon aceitou" de "algo
entrou de fato". A entrega está completa; o que ficou de fora é **documento** —
ver a dívida de processo, no fim.

## O que virou obsoleto nas sprints abertas

Esta seção é a resposta ao *"veja o que podemos melhorar delas"*. São trechos que
descrevem uma máquina que não é mais a dela.

### EMPATE-01 raciocina sobre uma janela de desktop que nunca chega

O documento simula e conclui: *"vencedor em janela de desktop: fallback"*, e o
item 0 explica a ausência de mordida pelo cadeado do autoswitch. **Medido agora,
a explicação é outra e é mais forte.**

Nesta máquina o backend de janela é sempre o `xlib`, e o COSMIC é Wayland nativo:
a JANELA-CEGA-01 mediu dez de dez amostras sem foco X nenhum. Quando a leitura
não traz evidência, `profiles/autoswitch.py:210` (`_tick_sem_informacao`) faz o
`_tick` **retornar antes de qualquer seleção** — não mexe no candidato, não
reinicia o debounce, não ativa nada. Ou seja: **no desktop dela o seletor de
perfil nem é chamado.** O empate só decide alguma coisa quando há janela X ou
XWayland em foco, que na prática é o jogo.

Isso não invalida a sprint — o desempate estava errado e foi curado em `8d7fd45`
com o incumbente como terceiro termo (`profiles/manager.py:674` e o evento
`profile_select_empate_resolvido` em `:700`). Invalida o **raciocínio de
gravidade**: o parágrafo "vence em toda janela que não seja de jogo" descreve um
X11 que ela não usa. A E2 continua valendo, e a redação precisa passar a dizer
que a disputa acontece na troca para o jogo, não no desktop.

### EMPATE-01, entrega E-1: já paga, e o documento não sabe

O `assets/profiles_default/fallback.json` **não tem mais o campo `lightbar`** — o
arquivo agora vai de `"leds"` direto para `"player_leds"` e
`"lightbar_brightness"`. A semente parou de opinar sobre cor, exatamente como a
sprint pedia, e o `player_leds: [false,false,true,false,false]` ficou como estava.

### PORTÃO-VIVO-01: entregue inteira, e os blocos merecem nota de rodapé

Os seis blocos estão no ar e são conferíveis em `.github/workflows/ci.yml`:
acentuação em matriz de três versões (`:40`), glifos (`:65`), referências mortas
(`:82`), shellcheck (`:104`), paridade de empacotamento (`:127`) e
`pre-commit run --all-files` (`:395`); e o `release.yml:56-66` passou a rodar os
mesmos gates de texto que o CI. **O que a sprint não previu e esta sessão
descobriu:** existiam gates na CI que a lista local não continha —
`check_test_data.sh` reprovou a estreia da v0.3.0 (`18d61d8`) e o
`check_version_consistency.py` reprovou de novo (`2c18504`). A lição, escrita
nos dois commits, cabe na sprint: *portão que existe e não é rodado antes do push
só avisa tarde*.

### PROMESSA-NÃO-CUMPRIDA-01, bloco A4: pago, e o número mudou de sentido

O documento fala em "734 testes de interface pulam no CI", e o índice de 27/07
repetiu isso. **Não é mais verdade, e nunca foi só isso:** 21 arquivos plantavam
um `gi` falso em `sys.modules`, e 737 testes reportavam PASSED contra um GTK de
mentira, com o verde dependendo da ordem alfabética dos arquivos. Rodando com
`gi` bloqueado, o HEAD anterior tinha 24 erros de coleta e 65 falhas; hoje são
zero e zero. Quem quiser reescrever o bloco A4 tem que trocar "pulam" por
"passavam sem medir".

### MIC-USB-01: a entrega 7 saiu, e o veredito do doctor mudou de critério

`install.sh:2311` chama `scripts/doctor.sh --fix-mic --quiet` no passo de áudio,
em best-effort, e respeita quem desligou a source de propósito. A seção
"O instalador NÃO chama a cura — e devia" descreve um passado.

Junto veio uma correção de critério que a sprint não previu: o check casava
qualquer rota com "dualsense" no nome, e a única rota muda era a de **saída**.
O portão reprovava o microfone por causa da caixa de som.

## Sprints novas que faltam ser escritas

Só o identificador e uma linha de escopo. A escolha do que vira código é dela.

**Uma delas saiu do papel na mesma rodada deste índice:** a **SOM-02** foi
escrita e está em
[SOM-02](2026-07-29-SOM-02-o-alto-falante-que-funciona.md). Fica na tabela
abaixo com o link, porque continua sem uma linha de código. As outras sete
continuam sendo só identificador. Duas sprints que este índice não previu também
nasceram nesta rodada, a pedido dela, e estão no
[índice da documentação da v0.3.0](../estudos/2026-07-29-INDICE-a-documentacao-da-v030.md):
a [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md),
a [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) e a
[SENSOR-VIVO-01](2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md).

| Identificador | Escopo, em uma linha |
|---|---|
| **FONTE-PADRÃO-01** | A fonte de captura padrão do sistema é o **monitor do alto-falante do próprio controle** — medido agora: `pactl get-default-source` devolve `alsa_output.usb-...DualSense...analog-surround-40.monitor`, enquanto o microfone de verdade (`alsa_input.usb-...analog-stereo`) está ali, disponível e não escolhido. O `--fix-mic` **não** cura isso e nem reclama: `scripts/doctor.sh:438` dá `pass` explícito para qualquer nome que contenha "monitor". Efeito: o que qualquer aplicativo grava é o áudio de saída. **A medição inteira, com a cadeia arquivo por arquivo e a causa (o decisor refutado da camada 2 que roda nesta árvore), está na [SENSOR-VIVO-01](2026-07-29-SENSOR-VIVO-01-touchpad-giroscopio-microfone-e-som-dentro-do-jogo.md), seção 3 e entregas E1 a E3** |
| **CONTAGEM-E-COOP-01** | O documento que a casa promete desde 26/07 e nunca escreveu: um número só na janela inteira (hoje três, em `status_actions.py:1063`, `:1391` e `home_actions.py:340`) e um aviso antes de `daemon/subsystems/gamepad.py:473-475` derrubar o co-op |
| **CÓDIGO-MORTO-01** | `integrations/xlib_window.py` são 111 linhas que nenhum código de produção importa e que leem `_NET_ACTIVE_WINDOW` sem gate de foco (`:61`) — exatamente o defeito que o UX-02 curou, preservado inteiro num arquivo que ainda importa limpo. Ou vira `raise ImportError` explícito, ou some. Junto: as 385 linhas da cascata Wayland que nunca executam nesta máquina |
| **PACOTE-COM-NOME-01** | O bundle Flatpak é publicado **sem versão no nome**: `.github/workflows/release.yml:249` e `:255` fixam `Hefesto-Dualsense4Unix.flatpak`, e o `build-bundle` sem `--default-branch` grava a branch `master`. O AppImage (`:123`) e o `.deb` (`:190`) carregam a versão no nome; só o Flatpak não. Dois releases publicam o mesmo arquivo, e quem baixou não sabe qual tem |
| **SEGUNDA-JANELA-01** | `app/compact_window.py` (317 linhas) e a bandeja (`app/tray.py`, 463 linhas) ficaram fora de **todo** levantamento — as três únicas menções em `docs/` são de passagem, nos índices e na VÃO-01. Se a janela compacta repete cards ou rótulos, as renomeações da PALAVRA-01 e da STATUS-SIMETRIA-02 saíram pela metade |
| **SOM-02** — [ESCRITA nesta rodada](2026-07-29-SOM-02-o-alto-falante-que-funciona.md) | O alto-falante vira controle: volume, mudo, devolução da posse e a decisão dela sobre o preço (o item 3 da seção "o que faltaria" da [SOM-01](2026-07-28-SOM-01-o-alto-falante-tem-lugar.md)). O documento existe e mede o preço por byte; **nenhuma linha de código entrou**, e não entra sem ela decidir |
| **JANELA-CEGA-02** | As três pendências declaradas da [JANELA-CEGA-01](2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md): a fiação do motivo, a troca de `healthy` por `seeing` no `game_signal` (uma linha, sozinha, com ela olhando a lightbar) e a linha honesta na aba Sistema |
| **TESTE-QUE-MEDE-01** | O `exigir_gi_real` (`tests/conftest.py:203`) e o job "Interface com GTK REAL" (`ci.yml:277`) entraram sem documento nenhum. É a maior mudança de confiabilidade da suíte nesta sessão e existe só em mensagem de commit |

## Dívida de processo

### O que a casa combinou e passou a cumprir

- **A PROVA-DE-TELA-01 foi aplicada pela primeira vez.** Está declarado em
  `464b7a2`: *"a regra PROVA-DE-TELA-01, escrita em 27/07 e nunca aplicada, foi
  usada pela primeira vez em todas as levas"*. Era a dívida de processo número um
  do índice anterior, e é a única desta lista que saiu do papel.
- **Os portões existem e reprovam.** A prova é que a estreia da v0.3.0 foi
  reprovada duas vezes seguidas por gates que ninguém tinha rodado, e os dois
  commits de reparo entraram antes de qualquer coisa chegar nela.
- **Teste que morde virou rotina.** Nas três levas de código houve verificação
  independente em árvore pristina: 15 mutações em `8d7fd45`, 16 em `b3e8b7f`,
  23 vermelhas em `e8f9060`.

### O que ainda não é rotina

- **O campo `Status:` continua mentindo em 36 dos 39 documentos.** Nesta sessão
  foram fechadas EMPATE-01 (menos a E2), PERFIL-NASCE-CERTO-01,
  STATUS-SIMETRIA-02, MIC-PRESENTE-01, PALAVRA-01 (menos a E5) e a entrega 7 da
  MIC-USB-01 — e **nenhum** desses arquivos teve o cabeçalho atualizado. Só três
  documentos de sprint foram tocados em `git log 5489c2a..HEAD --name-only`.
- **Sprint fechada sem commit anotado.** O índice de 25/07 registra o commit ao
  lado de cada entrega; nenhuma das entregas desta sessão tem isso escrito no
  documento da própria sprint.
- **Identificadores que existem só em mensagem de commit.** A lista cresceu, não
  encolheu. Herdados: `MIC-FAIXA-01`, `SLOT-JOGADOR-01`, `RUMBLE-PRESO-01`.
  Novos desta sessão: `APLICAR-VERDADE-01`, `AVISO-VIVO-01`, `IPC-SEM-TRAVA-01`
  — os três medidos com a janela aberta e curados em `e8f9060`, sem uma linha em
  `docs/`. `APLICAR-VERDADE-02` escapou por acaso, porque virou anexo da
  JANELA-CEGA-01.
- **O checklist de validação em hardware continua com zero caixas marcadas** —
  31 vazias hoje, contra 43 em 26/07, e a diferença é o documento ter encolhido,
  não ela ter marcado nada.
- **A aba Status com dois ou mais cards continua sem olho dela.** Toda a
  avaliação da SOM-01 foi com um controle só, em janela offscreen.
- **A escala de fonte máxima (8) nunca foi medida.** O episódio dos 12 px de
  folga em `2c18504` é a prova de que o pior caso importa: a CI, sem as fontes do
  projeto, pediu 431 px onde a máquina dela pedia 357.

## Alertas de ambiente, fora deste repositório

Continuam valendo os dois do índice anterior, porque moram fora da árvore: o
`andromeda-autosync` commita `~/.config/zsh` a cada dez minutos e apaga qualquer
linha com o token de co-autoria, inclusive dentro de código; e o self-heal
reinstala o hook de commit de hora em hora a partir de uma fonte canônica.
Qualquer edição futura nesses dois precisa ser propagada nas duas pontas.

## O que NÃO foi medido neste levantamento

Escrito de propósito, para não virar afirmação por omissão.

- **O journal do daemon.** Os números de flapping que sustentam a PERFIL-JOGO-01
  são de 26/07 e continuam sem reprodução. O que foi conferido hoje é o
  **código**, não o comportamento em execução.
- ~~Se o cadeado `autoswitch_locked` ainda está ligado.~~ **Medido depois, e
  fica registrado aqui em vez de na lista do que falta:** o arquivo
  `autoswitch_locked.flag` existe em `~/.config/hefesto-dualsense4unix/`, com
  mtime de 28/07 18:18. As duas explicações valem ao mesmo tempo — o cadeado
  impede a reativação, e o `_tick_sem_informacao` faz o seletor nem ser chamado
  no desktop dela. O que continua sem medição é qual dos dois morderia primeiro
  se o outro saísse. Ver o
  [mapa da sessão](../estudos/2026-07-29-mapa-da-sessao-e-o-que-os-agentes-mediram.md),
  seção 10.
- **As sprints CR-01 a CR-06** não foram cruzadas com o código. Estão fora de
  escopo por decisão dela e foram lidas só pelo cabeçalho.
- **A janela compacta e a bandeja** não foram abertas — é justamente por isso
  que viraram candidata a sprint, e não linha de tabela.
