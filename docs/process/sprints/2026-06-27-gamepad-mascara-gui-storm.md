# Checkpoint 2026-06-27 — gamepad com máscara, GUI auto-suficiente, storm-watch

Onde paramos nesta sessão (para retomar após reboot).

## O que ficou PRONTO (código + testes verdes: 1538 passam, ruff limpo, anonimato OK)

1. **B4 — touchpad move o cursor** (`FEAT-DSX-TOUCHPAD-CURSOR-B4`): o daemon lê o
   `event14` (ABS_X/Y + BTN_TOUCH) e move o cursor (carry sub-pixel, sem engasgo;
   respeita modo-jogo). Fonte única (a regra 76 tira o touchpad do libinput).

2. **Gamepad virtual com máscara, integrado ao daemon** (`FEAT-DSX-GAMEPAD-FLAVOR-01`):
   - Duas máscaras: **DualSense** (VID/PID Sony `054c:0ce6` → prompts de PlayStation,
     default) e **Xbox 360** (fallback p/ jogos XInput-only).
   - Virou subsystem do daemon: **1 leitor** do controle → fan-out. Acabou o
     **input dobrado** do antigo `emulate xbox360` (processo avulso = 2 leitores).
   - Faz **EVIOCGRAB** do controle real enquanto ativo → o jogo vê só o virtual
     (sem duplicação). `find_dualsense_evdev` agora **ignora devices virtuais**
     (uinput) p/ o daemon nunca ler a própria saída.
   - Mutuamente exclusivo com a emulação de mouse; liga/desliga + máscara
     **persistem no boot**.
   - Validado AO VIVO: `gamepad on --flavor dualsense` cria `jsN` Sony, faz grab
     do real (event12), `off` limpa tudo.

3. **GUI auto-suficiente** (`FEAT-DSX-GUI-SELF-SUFFICIENT-01`): aba Emulação ganhou
   - **Gamepad p/ jogos**: Desligado / DualSense (PS) / Xbox 360.
   - **Modo jogo**: Pausar / Retomar (via `daemon.pause`/`resume`).
   - **Steam Input**: Verificar / Desligar (ele conflita com o daemon).
   (já existiam: daemon start/stop/restart/autostart, mouse on/off+velocidade, mic,
   gatilhos, lightbar, rumble, perfis, teclado.)

4. **Storm-watch opt-in** (`FEAT-DSX-STORM-WATCH-01`): `--with-storm-watch` (ou modo
   "tudo"/`--yes`) instala um serviço de usuário que loga o `-71` num arquivo
   dedicado (`~/.local/state/hefesto-dualsense4unix/storm.log`), replicável e
   sobrevivente a reboot. Uninstall simétrico.

## Comandos novos (CLI)

- `hefesto-dualsense4unix gamepad on --flavor dualsense|xbox`
- `hefesto-dualsense4unix gamepad off`
- `hefesto-dualsense4unix gamepad status`

(Tudo também pela aba **Emulação** da GUI.)

## Estado pós-reboot esperado

- Daemon está **enabled** (autostart). Sobe com **nenhuma emulação ligada** (flags
  de mouse e gamepad ausentes) → controle cru = gamepad PS para os jogos que
  aceitam Sony. Sem mouse-maluco.
- Quirk do storm persiste no kernelstub (`054c:0ce6:gn`). Storm: várias janelas de
  30 min limpas (-71=0) com mic ON.
- Para jogar: abrir a GUI → aba Emulação → escolher **DualSense (PS)** (ou Xbox
  para jogo teimoso). Ou `gamepad on`.

## Applet COSMIC (#23) — RESOLVIDO no que dependia do código

- Trocada a logo do applet para a **mesma do app** (martelo/forja, o PNG
  `hefesto-dualsense4unix`), igual ao `.desktop`. Removidos os ícones
  `ICON_OFFLINE/ICON_ALERT/LOW_BATTERY_PCT`; `panel_icon()` retorna `ICON_APP`
  fixo. Rebuild Rust + reinstalado em `/usr/local/bin`; `cosmic-panel`
  re-hospedou o applet com o binário novo.
- **Confirmado VISUALMENTE** (screenshot + zoom): o 5º ícone do painel é a logo
  do Hefesto (gradiente ciano→rosa/roxo, silhueta do martelo). Antes ficava o
  símbolo monocromático que não renderizava direito.
- Sobre o "some ao clicar" / SIGKILL 137: investigação anterior mostrou que os
  137 eram **restart em massa do `cosmic-panel`** num evento de display, não um
  crash do nosso applet. O teste do clique/popup fica para a validação ao vivo.

## Bug pego na validação: botões da aba Emulação não aplicavam (RESOLVIDO)

Sintoma da Vitória: "clico nos botões e nem se aplicam, nem ficam selecionados".
Causa: o app fia sinais por **dict explícito** (`HefestoApp._signal_handlers()`),
não por `self`. Os `<signal handler=...>` novos do glade (gamepad off/dualsense/
xbox, pausar/retomar, Steam Input check/disable, mic on/off) **não tinham chave**
no dict → o GTK não achava o callback → clique = no-op. O backend (IPC
`gamepad.emulation.set`) já funcionava (testado via CLI: liga/desliga ok).

Fix: adicionadas as 9 entradas faltantes em `app.py` + teste estático
`tests/unit/test_glade_signal_handlers.py` (todo `handler` do glade tem de estar
registrado — trava a regressão). 1540 testes verdes, ruff limpo. GUI reiniciada
pra carregar o código novo (o processo tinha o dict velho em memória).
"Não fica selecionado" = são botões de ação; o estado ativo aparece no **label de
status** de cada bloco ("ligado — DualSense (PS)" etc.).

## Realce do modo ativo (FEITO)

A pedido da Vitória, o seletor de gamepad agora **realça o modo ativo**: o botão
atual (Desligado / DualSense (PS) / Xbox 360) fica destacado em roxo (classe CSS
`.hefesto-active-mode`, mesmo visual da política de rumble). Aplicado em
`emulation_actions.py` (`_highlight_gamepad`, chamado no refresh do `state_full`)
+ `theme.css`. 1540 testes verdes, ruff limpo.

## Esclarecimentos da validação ao vivo (madrugada 02:00–02:30)

- **O "storm" das 02:18 foi a Vitória reconectando o cabo USB** ("tirei e reconectei
  pra ver se ligava"). O journal mostra `USB disconnect` + reenumerações (device
  20→31) com `-71`, estabilizando em ~26s (`Registered DualSense`). NÃO é storm
  espontâneo nem HW — é a reenumeração normal de tirar/pôr o cabo; o quirk segurou.
  Os vigias (`bn33ua9z2`, `btytgkkbu`) dispararão a CADA reconexão física.
- **"Nada funcionou pela interface" = mal-entendido do grab, não bug.** Ligar o
  gamepad (DualSense/Xbox) faz **EVIOCGRAB** do controle real → ele vira exclusivo
  do jogo. **Sem jogo aberto, o controle "some" do desktop e parece morto.** O modo
  gamepad só tem efeito DENTRO de um jogo. Teste certo: **abre o jogo primeiro,
  depois liga DualSense.** (TODO de UX: a GUI avisar "controle capturado para o
  jogo" ao ligar — pendente, sob demanda.)
- O **mic foi desligado pela GUI e aplicou** (drop-ins 52/53 presentes) → prova de
  que os handlers estão fiados.
- **02:57 — storm CONTÍNUO (+22, total ~41), diferente dos bursts:** o controle
  entrou em **loop de reenumeração** (device 52→59 em ~23s, SEM `Registered
  DualSense`, `-71` subindo, sumido do `lsusb`). Começou logo após a Vitória ter
  mexido no cabo ("tirei e reconectei pra ver se ligava") → **suspeita nº1: cabo
  mal encaixado / contato intermitente** (loop contínuo casa mais com conexão
  física ruim do que com o storm-de-áudio, que o quirk costuma estabilizar em
  poucos ciclos). Quirk `054c:0ce6:gn` segue ativo. NÃO intervim (vai parar no
  shutdown). **AO RELIGAR: encaixar bem o cabo USB (ou trocar de cabo/porta) antes
  de concluir que é storm.** Se com cabo firme ainda entrar em loop, aí sim é o
  storm-de-áudio — ver [[storm-dualsense-e-config-nossa-nao-hardware]].
- Estado no fim da sessão: daemon **foreground avulso** (não o serviço), gamepad
  **off**, sem flags, controle **livre** (sem grab). Vitória vai **reiniciar** para
  recomeço limpo (serviço systemd assume no boot). Nada a perder — código no disco.

## PENDENTE (precisa de você)

1. **Validação ao vivo conjunta** — DO JEITO CERTO: **abrir o jogo PRIMEIRO**, então
   na aba Emulação ligar **DualSense** (ver o botão realçar) e testar (vs Xbox + mic
   + touchpad + PS+Options). Aproveitar para clicar no applet (popup abre/fecha).
2. **Sprint de múltiplos controles** (NOVA, pedida pela Vitória): hoje o daemon
   gerencia 1 só DualSense (`find_dualsense_evdev` → 1 device). Um 2º controle não
   recebe gatilhos adaptativos. **Sprint CRIADA** (com levantamento técnico completo
   do agente embutido) em
   `docs/process/sprints/2026-06-27-suporte-multiplos-controles.md`. Falta a Vitória
   escolher o caminho: A (múltiplas instâncias, ~200 LOC) / B (dict MVP, ~500 LOC) /
   C (N-controle pleno, ~2 meses). Não entra na v3.8.4.
3. **Release no GitHub (ÚLTIMO PASSO)**: bump de versão (pyproject + README +
   `__init__.py` + CHANGELOG) → push origin → `gh workflow run release.yml` v3.8.4.
   Só após validar tudo acima.

## Monitoramento de storm

journald já persiste tudo: `journalctl -k --grep ' -71'` (histórico) /
`journalctl -k -b -1` (boot anterior). O storm-watch é só um recorte legível extra.
