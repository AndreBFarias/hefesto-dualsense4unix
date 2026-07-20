# Sprint Onda U — GUI: 13 sintomas relatados ao vivo (19/07 noite)

> Relato direto da mantenedora testando com 2 DualSense no CABO (antes das ondas N/R desta
> noite). MUITOS sintomas podem ser consequência da guerra de autoridade (cliente Steam
> escrevendo LEDs/perfil "eterno") — **triagem manda re-testar cada U após a Onda N entrar**.
> Ela avisou: "pode ser decorrência das configs da interface ou de algum teste que deixamos
> ligado". EXECUTAR: triagem read-only pode começar já; fixes de GUI após Onda N (colisão em
> ipc_handlers/card). Cada fix exige teste (GUI sem `import gi` no topo — padrão
> `_install_gi_stubs`).

## Sintomas (numerados; citar o U# no fix e no teste)

- **U1 (P0)** Ligar/desligar Hefesto: com o daemon DESLIGADO, a aba Início mostra botão
  "Desligar Hefesto" e um aviso mandando ir na aba Sistema. Pedido dela: o botão deve virar
  "Ligar o Hefesto" ali mesmo (toggle in-place; nada de mandar pra outra aba). E: "o desligar
  e ligar hefesto não funciona" — investigar o handler (journal na hora do clique, IPC
  system.enable/disable) antes de redesenhar.
- **U2 (P0)** Com SÓ 2 DualSense no cabo, a GUI mostra "sony 1 usb" e "sony 4 usb".
  Explicação conhecida: slots persistentes do registry (D2) herdados da tempestade de hoje
  (roxo=1, branco=4 em controllers.json). Fix de produto: botão "Renumerar agora" (IPC novo
  `identity.renumber`, SÓ com sessão de jogo fechada; renumera compactando 1..N e re-pinta) +
  investigar por que `identity_sessao_esvaziou_reservas_expiradas` (16:08) não devolveu o
  branco pro slot 2 (ler identity.py: expiração × re-atribuição).
- **U3 (P0)** "Aplicar" ignora o que ela configurou e aplica um perfil pré-selecionado.
  Investigar o fluxo do botão Aplicar: coleta dos widgets × autoload de perfil por-controle
  (8e59601, origin) atropelando; race entre `profile.activate` e edição não-salva.
- **U4 (P0)** Configurações NÃO sobrevivem à troca de aba (tem que reaplicar tudo). Provável
  reload do estado do daemon no on_show de cada aba descartando ediçãO local — decidir e
  implementar: estado de edição pendente por aba (dirty flag) que sobrevive à navegação.
- **U5 (P1)** Launch option por jogo ainda é manual ("pensei que aplicasse em tudo"). Feature
  LAUNCH-ALL: botão na aba Sistema "Aplicar wrapper a todos os jogos" usando a máquina do
  passo 11b do install (localconfig.vdf; guard `steam -shutdown`; backup; só adiciona
  `hefesto-launch %command%` onde não há launch option conflitante; relatório do que tocou).
- **U6 (P1)** Sackboy: race visível entre "Jogar pelo Hefesto" × "Jogar direto (Sony)" — os
  dois funcionando ao mesmo tempo. FORTE candidato a causa-raiz já curada: o teste dela foi
  ANTES do install de hoje (wrapper hefesto-launch NEM EXISTIA no PATH ⇒ duplicado clássico).
  Re-testar pós-install+launch-option; se persistir: lsof nos hidraws durante o jogo + journal
  do autoswitch (manual_override).
- **U7 (P1)** Aba Gatilhos não aplica (ou conflita). Re-testar pós-N (autoridade); se
  persistir, tracejar IPC triggers.apply → daemon → hidraw.
- **U8 (P1)** Aplicar perfil só num controle (dsx 1) não persiste ao reconectar/trocar de
  controle; "Salvar Perfil" de efeito incerto. Ver desired por-uniq (PERFIL-01/4P-01) e
  autoload origin — definir e TESTAR a semântica: aplicar-por-controle grava desired_by_uniq
  persistente; reconectar re-aplica.
- **U9 (P0)** Aba Lightbar: "perfil eterno sempre aplicando e zuando tudo" (cura esperada =
  Onda N; re-testar); player LEDs via GUI não funcionam; presets rápidos não funcionam;
  brightness default deveria ser 100% e não é. Tracejar cada botão → IPC → backend (com o
  gate de autoridade novo em mente).
- **U10 (P2)** Pedido de feature: no topo da GUI, refresh + "remap automático" da enumeração
  (casa com o botão Renumerar do U2 — mesma entrega).
- **U11 (P1)** Aba Rumble: validar todos os botões (aplicar/parar/deixar o jogo controlar)
  pós-N com teste automatizado do fluxo IPC.
- **U12 (P0, RESOLVIDO ao vivo 20:4x)** "Gerenciamento de áudio não deixa colocar nada" —
  causa: sink padrão (HDMI NVidia) estava MUTED global. Desmutado via wpctl; drop-in 51 do
  mic INOCENTE (só rebaixa prioridade do mic do DualSense). Ação restante: doctor ganha check
  "sink padrão mutado" com dica (1 linha); investigar QUEM mutou (tecla/applet/mic-hotkey do
  daemon — conferir se o mic_hotkey mexe em SINK por engano em vez de SOURCE).
- **U13 (P2)** input-remapper roda na máquina (devices "input-remapper * forwarded" no
  /proc/bus/input). Verificar coexistência: os forwarded NÃO devem entrar em enumeração/
  contagem nossa (são uinput ⇒ o filtro os exclui; confirmar com teste) e documentar no
  doctor/README de convivência.

## Aceite
- Cada U com: causa raiz anotada (ou "cura pela Onda N confirmada por re-teste"), fix com
  teste falha-sem/passa-com quando for código nosso, e entrada no checklist de validação ao
  vivo do ÍNDICE da maratona.
- U1/U2/U3/U4/U9/U12 são P0 — sem eles a validação em família não flui.
