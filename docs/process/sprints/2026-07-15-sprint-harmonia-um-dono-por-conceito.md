# Sprint SPRINT-HARMONIA-01 — um dono por conceito

Pedido da mantenedora (2026-07-15): *"já descobrimos a solução pra todos os problemas,
só não cuidamos da harmonia e coexistência entre o todo… fizemos todas as alterações na
raiz mas não foi pensado no conflito entre todas elas em si."*

Diagnóstico da auditoria (9 áreas lidas por agentes + tour ao vivo das 10 abas): cada
fix foi correto **isolado**. O que quebra é a **coexistência** — o mesmo conceito tem
dois ou três donos, cada um com sua semântica, e eles se sobrescrevem em silêncio.

Este sprint não inventa features. Ele elege **um dono por conceito** e faz todo o resto
obedecer.

## Conceito 1 — Modo do sistema

**Dono: aba Início.** Ninguém mais decide modo.

- `HARM-01` — **Aba Emulação perde o seletor de máscara/vpad.** Hoje ela é um segundo
  dono, com semântica divergente: seus botões **não saem do Modo Nativo** antes de ligar
  o vpad → grab do físico + vpad congelado = **jogo sem controle nenhum**, com as duas
  abas mostrando modos contraditórios.
  Arquivos: `app/actions/emulation_actions.py:399-406`, `app/actions/home_actions.py:407-449`,
  `daemon/lifecycle.py:722-765`.
  **Aceite**: não existe mais nenhum caminho de UI que ligue o vpad sem passar pela
  transição de modo da Início; alternar InícioEmulação nunca mostra estados diferentes.

- `HARM-02` — **A aba Emulação deixa de existir como aba.** O que é útil (saúde do
  uinput/uhid, teste de device virtual) vira um cartão de diagnóstico dentro de
  "Sistema"; o resto é jargão exposto (UINPUT/VID:PID/Buffer/Passthrough/`daemon.toml`
  que o daemon nem lê, lista crua `js0..js5`).
  **Aceite**: 10 abas → 8; nenhuma função perdida; nada que a Início já resolva aparece
  duas vezes.

- `HARM-03` — **"Modo jogo" some como conceito concorrente.** Hoje "Modo jogo"
  (suspender mouse/teclado) fica em laranja permanente ao lado de "Jogar pelo Hefesto" —
  dois "modos de jogo" diferentes na mesma tela. Pior: ligá-lo em "Controlar o PC" deixa
  o controle **sem função nenhuma** e o tooltip afirma o contrário.
  Arquivos: `app/actions/emulation_actions.py:425-434`, `gui/main.glade:1948`,
  `daemon/subsystems/hotkey.py:73-80`, `packaging/cosmic-applet/src/app.rs:459`.
  **Aceite**: a suspensão de mouse/teclado passa a ser consequência automática do modo
  "Jogar pelo Hefesto"/"Jogar direto"; o toggle manual só existe (se existir) como
  "Pausar mouse/teclado", nunca oferecido em modo desktop.

- `HARM-04` — **Perfil vs escolha manual: precedência explícita e visível.** Hoje o lock
  da escolha manual dura **30 s** e expira **sem nenhum feedback** — o autoswitch retoma
  em silêncio e derruba o que a usuária escolheu. Um perfil `desktop` derruba até isso.
  Arquivos: `app/actions/profiles_actions.py`, `daemon/subsystems/autoswitch.py`,
  aba Início.
  **Aceite**: escolha manual **não expira sozinha**; quando um perfil muda o modo, a
  Início diz qual perfil fez isso e oferece "manter meu modo".

## Conceito 2 — Emulação de mouse/teclado

**Dono: o modo "Controlar o PC".** As abas Mouse/Teclado são só ajustes dele.

- `HARM-05` — **Exclusão mútua explícita, não silenciosa.** Ligar o switch da aba Mouse
  durante "Jogar pelo Hefesto" **derruba o vpad e o co-op sem aviso**; e um "Aplicar" do
  rodapé com `draft.mouse.dirty` **religa o mouse e mata o vpad no meio do jogo**
  (`draft.mouse.dirty` nunca é limpo → a aba re-aplica estado velho pelo resto da sessão).
  **Aceite**: o switch fica desabilitado com explicação fora do modo desktop; nenhum
  "Aplicar" muda o modo do sistema; o dirty é limpo após aplicar.

- `HARM-06` — **"Controlar o PC" liga de fato o mouse.** Hoje ele só **desliga**
  gamepad/nativo — o controle fica sem função até a pessoa achar a aba Mouse. E o
  round-trip desktop→gamepad→desktop **apaga a preferência persistida** do mouse.
  **Aceite**: entrar em "Controlar o PC" deixa o cursor funcionando; sair e voltar
  preserva a preferência.

- `HARM-07` — **Teclado emulado deixa de vazar para jogos.** Default-on manda
  Alt+Tab/Super para dentro do jogo no modo desktop e é **impossível silenciá-lo pela
  GUI** (store vazia ressuscita os defaults). Além disso R3 dispara clique-do-meio **e**
  fecha o teclado-na-tela no mesmo aperto.
  **Aceite**: dá para desligar o teclado pela GUI e a escolha persiste; nenhum binding
  duplo no mesmo botão.

## Conceito 3 — Máscara do gamepad

**Dono: o estado do daemon.** (Ver `SPRINT-UHID-VPAD-01`, que remove o trade-off.)

- `HARM-08` — **Um único default em todas as superfícies.** Hoje: daemon/GUI = `xbox`,
  **CLI = `dualsense`**, applet (fallback) = `dualsense`. O mesmo gesto liga máscaras
  diferentes conforme a porta de entrada — e a CLI **mata o rumble** de quem tinha Xbox.
  Arquivos: `cli/cmd_gamepad.py:47`, `packaging/cosmic-applet/src/app.rs:332`,
  `app/actions/home_actions.py:416`, `daemon/lifecycle.py:103`.
  **Aceite**: `gamepad on` sem argumento **preserva** a máscara atual; os três defaults
  coincidem; teste de paridade cobrindo as três superfícies.

- `HARM-09` — **Uma única apresentação.** O mesmo seletor tem **3 formas** (Início:
  "Xbox 360 (vibra)"/"DualSense (botões PS, sem vibrar)"; Perfis: outra; Emulação:
  "Desligado | DualSense (PS) | Xbox 360"), e um toast chama de **"fallback"** a máscara
  que o resto da UI chama de **"recomendada"**.
  **Aceite**: um widget, um texto, um vocabulário — em GUI, applet e CLI.

## Conceito 4 — Qual controle recebe os ajustes

**Dono: um seletor único e visível em toda aba que escreve no controle.**

- `HARM-10` — **O alvo deixa de ser global e invisível.** Hoje o seletor mora só no
  banner da aba Status, mas redireciona **tudo** — inclusive a aplicação de perfis pelo
  autoswitch (2 Hz) — e **envenena o estado desejado do backend**: um ajuste feito "só no
  Controle 2" é re-aplicado a **qualquer** controle no hotplug/replug.
  Arquivos: `core/backend_pydualsense.py` (`_reapply_desired`, `_refresh_sysfs_leds`),
  `app/actions/status_actions.py`, `daemon/ipc_handlers.py`.
  **Aceite**: o estado desejado é **por controle**; perfis nunca são redirecionados pelo
  seletor; toda aba que escreve mostra em qual controle está escrevendo.

- `HARM-11` — **Modo Nativo silencia sem mentir.** Hoje o mute do nativo faz
  Rumble/Lightbar/Gatilhos/Mic-LED virarem **no-op mudo**: a UI aceita o clique e nada
  acontece (inclusive "Ativar perfil" durante "Jogar direto" parece funcionar e não muda
  nada).
  **Aceite**: no modo nativo os controles de output aparecem desabilitados com a razão
  em texto simples ("o jogo está no comando do controle").

## Conceito 5 — Desligar

- `HARM-12` — **"Sair"/"Parar"/"Desligar" significam três coisas em quatro lugares**
  (applet, tray da GUI, tray da CLI, janela compacta; e "Parar" da aba Daemon é desfeito
  em silêncio pelo `ensure_daemon_running`).
  **Aceite**: um vocabulário único; nenhum botão desliga o daemon sem dizer que vai.

- `HARM-13` — **Um tray só.** Hoje há **dois trays paralelos** (AppTray da GUI e
  TrayController da CLI) com menus e comportamentos divergentes.
  **Aceite**: um tray; o outro é removido.

## Conceito 6 — Sincronização entre superfícies

- `HARM-14` — **Fim da dessincronização por polling.** A aba Emulação **não faz poll**;
  o applet usa timeout de **250 ms** e a CLI **1,0 s** para trocas de modo que a GUI já
  descobriu precisarem de **2,0 s** → falsos "Daemon desconectado"/"daemon recusou" com o
  modo **já aplicado**; e `profile.list` não devolve `active`, então tray/applet nunca
  marcam o perfil ativo.
  **Aceite**: timeout unificado; `profile.list` devolve `active`; mudança feita em
  qualquer superfície aparece nas outras em ≤ 1 s.

## Conceito 7 — A UI não pode mentir

Achados HIGH da auditoria que não são "conflito entre abas", mas **a tela afirmando o
que o daemon não fez**. Entram aqui porque a cura é a mesma: um dono, uma verdade.

- `HARM-15` — **"Daemon desligado" com o daemon vivo.** O refresh da aba Início chama
  `call_async("daemon.state_full", …)` **sem `timeout_s`** (`home_actions.py:266`) → usa
  o default de **0,25 s**; qualquer resposta mais lenta cai no `_fail` e a aba se pinta
  de "Daemon desligado — religue na aba Daemon". A própria aba já sabe que trocas de modo
  precisam de 2,0 s (`_MODE_IPC_TIMEOUT_S`).
  **Aceite**: nenhuma tela declara o daemon morto sem ter esperado o suficiente.

- `HARM-16` — **Rumble fixado ao sair do "Jogar direto (Sony)"**: o controle **vibra sem
  parar** e o jogo perde a vibração. É a pior cara possível para "todas as opções
  funcionam".
  **Aceite**: sair de qualquer modo zera os motores; teste de regressão.

- `HARM-17` — **Autoswitch congela o input**: faz D-Bus **síncrono com timeout de 2 s no
  event loop principal, a cada 0,5 s**. Quando o D-Bus demora, o controle trava.
  **Aceite**: nenhuma chamada bloqueante no loop de input; medição antes/depois.

- `HARM-18` — **Controles que ensinam gestos desligados**: a UI manda "segure o botão PS"
  em **três lugares** e a notificação anuncia "Modo jogo ligado", mas o long-press está
  **desligado por default** — a pessoa aperta e não acontece nada.
  **Aceite**: ou o gesto existe, ou a UI não o ensina.

- `HARM-19` — **Sliders que pedem o que o daemon recusa**: "Intensidade global" vai até
  **200%**, o daemon rejeita acima de 100% **em silêncio**; erro de validação de gatilho
  (Fim ≤ Início) é reportado como **"daemon offline?"**.
  **Aceite**: nenhum controle oferece faixa inválida; erro de validação diz o que está
  errado.

- `HARM-20` — **Input dobrado em USB+BT**: com o mesmo controle nos dois transportes, o
  **segundo nó evdev nunca é grabado** → o jogo recebe cada botão duas vezes.
  **Aceite**: um controle = um input, em qualquer combinação de transporte.

## Validação ao vivo (obrigatória, 1 USB + 1 BT)

Roteiro que precisa passar inteiro, sem toast mentiroso:
1. Início: desktop → gamepad → nativo → gamepad, com jogo aberto. Nenhum estado
   contraditório entre abas; controle nunca fica sem função.
2. Ligar mouse durante gamepad: bloqueado com explicação (não derruba o co-op).
3. Trocar máscara pela CLI e pelo applet: GUI reflete em ≤ 1 s; rumble continua.
4. Ajustar lightbar no Controle 2, desplugar/replugar o Controle 1: o ajuste **não**
   vaza para o Controle 1.
5. Perfil com modo ativa por jogo: Início mostra quem mudou; escolha manual não expira.

## Ordem

HARM-08/09 (baratos, param de mentir) → HARM-01/02/03 (dono do modo) →
HARM-05/06/07 (mouse/teclado) → HARM-10/11 (alvo e mute) → HARM-04 →
HARM-12/13/14.
