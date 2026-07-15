# Anexo — inventário de textos da interface (auditoria 2026-07-15)

Levantado pelos agentes que leram as 15 áreas do projeto. Cada linha traz o texto ATUAL, o
problema para quem é leigo, e a PROPOSTA em português simples. É o checklist do
[`SPRINT-LEIGO-01`](2026-07-15-sprint-leigo-fala-de-gente.md) — os números de linha podem ter
deslocado; confira o texto antes de trocar.

**405 textos em 45 arquivos.**

## `src/hefesto_dualsense4unix/gui/main.glade` (90)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 109 | daemon de gatilhos adaptativos para DualSense | Jargão 'daemon' logo no banner, primeira coisa que o leigo lê; começa em minúscula. | **Seu controle PlayStation no Linux — gatilhos, luz e vibração** |
| 120 |  Controle Desconectado | Espaço sobrando no início da string e Title Case fora do padrão. | **Nenhum controle conectado** |
| 191 | Transporte: | Jargão de rede/USB; leigo não sabe o que é 'transporte' | **Ligado por:** |
| 237 | Daemon: | Jargão técnico (queixa nº 1 da mantenedora) | **Serviço:** |
| 305 | Sticks e botões | 'Sticks' é jargão gamer em inglês; o resto da aba já diz 'Analógico' | **Analógicos e botões** |
| 411 | Status | Aba 'Status' vs 'Início' confunde (as duas mostram estado); o conteúdo é leitura ao vivo de gatilhos/sticks. | **Ao vivo** |
| 465 | Preset: | Anglicismo técnico. | **Efeito pronto:** |
| 528 | Desligar (Off) | Redundância bilíngue ('Desligar' já diz tudo). Idem linha 650. | **Desligar** |
| 684 | Lightbar (barra de LED) | Mistura inglês+tradução; 'LED' dispensável. | **Cor da luz do controle** |
| 694 | Escolha a cor da barra de LED do DualSense. | 'barra de LED' é o mesmo estrangeirismo traduzido ao pé da letra. | **"Escolha a cor da luz que fica em volta do touchpad."** |
| 738 | Aplicar no controle | Terceiro botão 'Aplicar...' da mesma tela (com 'Aplicar LEDs' e o 'Aplicar' do rodapé) — a usuária relatou exatamente isso: 3 jeitos de aplicar. E é o único jeito de a cor chegar ao controle, ao contrário das caixinhas (BUG-8). | **Melhor: aplicar a cor na hora (como as caixinhas) e ELIMINAR o botão. Se mantido: "Acender esta cor".** |
| 766 | Luminosidade (%) | Palavra formal; todo aparelho doméstico chama de brilho. | **Brilho (%)** |
| 801 | 5 indicadores inferiores do controle. | Descrição abstrata; o usuário não sabe onde ficam. | **As 5 luzinhas abaixo do touchpad.** |
| 823 | <b>Presets rápidos:</b> | 'Presets' é anglicismo. | **"<b>Atalhos:</b>"** |
| 884 | Reenvia o padrão atual dos 5 checkboxes ao controle via daemon. | 'checkboxes' e 'daemon' no tooltip de uma ação simples. | **Envia de novo ao controle as luzes marcadas acima (útil depois de reconectar).** |
| 901 | Checkboxes e presets enviam imediatamente ao hardware. Use "Aplicar LEDs" para reenviar o padrão atual (útil após reconectar o controle ou trocar de perfil). As marcações ficam salvas no perfil ativo. | 'Checkboxes', 'presets', 'hardware' — 3 jargões. Além disso a nota descreve uma incoerência (marcar caixinha aplica na hora, mas trocar a COR exige clicar 'Aplicar no controle' — BUG-8) em vez de resolvê-la. | **"As luzinhas acendem no controle assim que você marca. Use 'Aplicar LEDs' para mandar de novo (depois de reconectar o controle). A escolha fica salva no perfil ativo."** |
| 917 | Lightbar | Rótulo da aba em inglês técnico; dentro dela o título já traduz ('barra de LED'). | **Luz** |
| 930 | Política de rumble | 'Política' é palavra de sysadmin; 'rumble' é jargão. | **Força da vibração** |
| 1040 | Motor fraco (weak) | Tradução seguida do inglês entre parênteses (idem 'Motor forte (strong)' na 1058). | **Motor leve (zumbido)  /  na 1058: Motor pesado (tranco)** |
| 1058 | Motor forte (strong) | Idem: bilíngue redundante. | **"Vibração pesada (motor da esquerda)"** |
| 1084 | Testar por 500 ms | Milissegundos são unidade de programador. | **Testar (meio segundo)** |
| 1090 | Aplicar | COLIDE com o botão 'Aplicar' do rodapé (main.glade:2403), que faz outra coisa (aplica o perfil inteiro). Dois botões idênticos na mesma tela com ações diferentes. | **"Deixar vibrando" (deixa claro que é o rumble fixo, não o 'Aplicar' global)** |
| 1097 | Força silêncio dos motores (re-afirmado pelo daemon). Para devolver a vibração ao jogo, use 'Devolver rumble ao jogo'. | 're-afirmado pelo daemon' expõe implementação interna; 'daemon' é jargão. | **"Trava os motores em silêncio até você mandar o contrário. Para o jogo voltar a vibrar, clique em 'Deixar o jogo vibrar'."** |
| 1103 | Devolver rumble ao jogo | 'rumble' no rótulo do botão; o label vizinho (1114) já diz 'Estado da vibração'. | **Devolver vibração ao jogo** |
| 1124 | Os valores acima passam pela política selecionada antes de chegar ao hardware. Throttle mínimo: 20 ms entre comandos. | 'política', 'hardware', 'throttle', '20 ms' — nota inteira em jargão. | **A força escolhida acima também vale para estes testes.** |
| 1141 | Rumble | Aba com nome em inglês; o resto do app já fala 'vibração'. | **Vibração** |
| 1191 | Abre dialogo para criar um perfil em branco | Impreciso (não abre diálogo nenhum — preenche o editor) e sem acento em 'diálogo' | **Prepara o editor para criar um perfil novo em branco** |
| 1216 | Ativar | Não avisa que a escolha manual pode ser desfeita pelo perfil automático ~30 s depois | **Manter 'Ativar' + tooltip: 'Aplica este perfil agora. Se outro perfil combinar com a janela em foco, ele pode voltar sozinho depois de ~30 segundos.'** |
| 1270 | Ativa campos técnicos (window_class, title_regex, process_name) | Jargão cru no tooltip do switch | **Mostra os campos técnicos da regra (classe da janela, título, nome do processo)** |
| 1314 | Quanto maior, mais prioritário que outros perfis (0-100) | Não explica o efeito prático | **Se dois perfis servirem para a mesma janela, vence o de número maior** |
| 1378 | Nome do executável do jogo (sem extensão no Linux) | 'Executável' e 'extensão' são jargão | **Nome do programa do jogo no sistema (ex.: eldenring). Dica: aparece na aba Início quando o jogo está aberto.** |
| 1404 | window_class: | Chave interna crua como rótulo (mesmo sendo modo avançado, dá para ser bilíngue) | **Classe da janela (window_class):** |
| 1411 | CSV: Steam,firefox | 'CSV' é jargão de planilha | **separe por vírgula: Steam,firefox** |
| 1418 | title_regex: | Idem | **Título da janela (regex):** |
| 1425 | regex (re.search) | 're.search' é referência de API Python num placeholder de UI | **padrão de texto (regex), ex.: Elden.*Ring** |
| 1432 | process_name: | Idem | **Nome do processo (process_name):** |
| 1439 | CSV: doom.x86_64,celeste | 'CSV' jargão | **separe por vírgula: doom.x86_64,celeste** |
| 1449 | AND entre campos preenchidos, OR dentro de cada lista. Campos vazios são ignorados. | Lógica booleana crua (AND/OR) para usuário final | **O perfil é usado quando TODOS os campos preenchidos combinam com a janela. Dentro de um campo, basta um dos itens da lista. Campos vazios são ignorados.** |
| 1459 | Avancado | Sem cedilha/acento (título da página da stack) | **Avançado** |
| 1475 | Modo (o que este perfil liga ao ativar) | Frase truncada/técnica | **Modo do controle enquanto este perfil estiver ativo** |
| 1495 | Preview do perfil (JSON) | 'Preview' e 'JSON' são jargão | **Detalhes técnicos (como o perfil será salvo)** |
| 1505 | (selecione um perfil para ver o preview) | 'Preview' em inglês | **(selecione um perfil para ver os detalhes)** |
| 1558 | Unit: | Jargão systemd; a linha inteira (Unit: hefesto-dualsense4unix.service) é irrelevante para leigos. | **Remover a linha (ou, se mantida em modo avançado: "Serviço:")** |
| 1582 | Auto-start: | Anglicismo; não diz auto-start de quê nem quando. | **Ligar sozinho ao iniciar o computador:** |
| 1602 | Iniciar | Iniciar o quê? Sem objeto, leiga não conecta com o Hefesto. | **Ligar o Hefesto** |
| 1614 | Parar | Duplica o 'Desligar Hefesto' da Início com semântica diferente (volta sozinho na próxima abertura) e não avisa. | **Desligar até eu reabrir o painel (e tooltip: "O Hefesto religa sozinho quando você abrir o painel de novo. Para desligar de verdade, use a aba Início.")** |
| 1632 | Ver Logs | 'Logs' é jargão. | **Ver o que aconteceu** |
| 1638 | Reiniciar daemon | Jargão 'daemon'. | **Reiniciar o Hefesto** |
| 1639 | Executa systemctl --user restart hefesto-dualsense4unix.service | Tooltip é a linha de comando crua. | **Desliga e liga o Hefesto — use se o controle parou de responder.** |
| 1645 | Migrar para systemd | Jargão puro; leiga não sabe o que é systemd nem por que migrar. | **Corrigir modo de execução (recomendado) (tooltip: "O Hefesto está rodando de um jeito improvisado, sem religar sozinho se falhar. Clique para deixá-lo no modo normal.")** |
| 1663 | Anti-storm / Sistema | 'Storm' é jargão interno do projeto. | **Saúde da conexão do controle** |
| 1663 | <b>Anti-storm / Sistema</b> | 'Storm' é jargão dos docs internos; o próprio README já traduziu para 'travamento do USB' (seção 'Jogar sem travar') mas a GUI manteve o termo do doc. | **<b>Travamento do USB / Sistema</b>** |
| 1683 | Reaplicar fixes seguros | 'Fixes' é anglicismo; 'reaplicar' pressupõe que já aplicou. | **Corrigir automaticamente** |
| 1684 | Sem sudo: desliga Steam Input (se a Steam não estiver aberta) e configura o WirePlumber | 'sudo' e 'WirePlumber' são jargão. | **Não pede senha: desliga o Steam Input (feche a Steam antes) e ajusta o áudio para o controle não virar microfone padrão.** |
| 1690 | Copiar opções p/ jogos | Vago — copiar o quê, colar onde? É o passo essencial para vibração sem duplicar e está enterrado numa aba técnica. | **Copiar ajuste da Steam (vibração sem controle duplicado) — e mover o botão para a aba Início, junto do modo 'Jogar pelo Hefesto'** |
| 1702 | Saída de systemctl status | Jargão. | **Detalhes técnicos (para pedir ajuda)** |
| 1730 | Daemon | Título da aba é jargão Unix; leiga não sabe que 'daemon' = o motor do Hefesto. | **Sistema** |
| 1747 | UINPUT: | Nome de módulo do kernel como rótulo. | **Controle virtual do sistema:** |
| 1759 | Device: | Anglicismo. | **O jogo vê:** |
| 1770 | VID:PID: | Jargão USB; inútil para leigos. | **Remover a linha (ou "Código do modelo:" em modo avançado)** |
| 1781 | Gamepads: | Lista nós /dev/input/js* crus sem explicar o que são. | **Controles visíveis para os jogos: (e renderizar "2 físicos + 2 virtuais" em vez dos caminhos)** |
| 1805 | Modo jogo: segure o botão PS para suspender a emulação de mouse/teclado | 'Emulação' é jargão; o tooltip do botão (1948) cita OUTRO gesto (PS+Options) — instruções divergentes na mesma tela. | **Modo jogo: segure o botão PS (ou PS+Options) para o controle parar de mexer no mouse/teclado do PC** |
| 1805 | &lt;b&gt;Modo jogo&lt;/b&gt;: segure o botão PS para suspender a emulação de mouse/teclado | Terceira cópia do gesto morto, agora no .glade. Se só a legenda Python (mouse_actions.py:38) for corrigida, este label continua ensinando errado. | **&lt;b&gt;Para o controle parar de mexer no PC&lt;/b&gt;: aperte PS + Options ao mesmo tempo. Aperte de novo para voltar.** |
| 1834 | Buffer: | Valor fixo (150) sem significado para o usuário; nada o altera. | **Remover a linha** |
| 1845 | Passthrough em emulação: | Jargão duplo + valor fixo 'Não' que nunca muda. | **Remover a linha** |
| 1866 | Testar criação de device virtual | 'Device virtual' é jargão. | **Testar controle virtual (tooltip: "Cria e remove um controle de teste para conferir se o sistema permite. Não use no meio de um jogo.")** |
| 1878 | Ver daemon.toml (referência) | Abre um arquivo de config que o programa NÃO lê — armadilha para o usuário. | **Remover o botão** |
| 1894 | Gamepad p/ jogos: | Difere do texto da Início ('O jogo vê o controle como:') para a MESMA função — parecem coisas diferentes. | **O jogo vê o controle como: (idealmente remover o seletor e apontar para a aba Início)** |
| 1906 | Desliga o gamepad virtual. O jogo passa a ver o DualSense cru (prompts PS nos jogos que suportam Sony). | ENGANOSO: sem o Modo Nativo o Hefesto continua reescrevendo o controle (vibração do jogo é zerada a cada 0.5s). O caminho certo é 'Jogar direto (Sony)'. | **Desliga o controle virtual (volta ao modo 'Controlar o PC'). Para jogos com suporte PlayStation, use "Jogar direto (Sony)" na aba Início.** |
| 1913 | Máscara DualSense: mostra prompts de PlayStation, mas a vibração NÃO funciona em jogo e o controle pode aparecer duplicado (o jogo fala com o controle físico). Prefira Xbox 360 para jogar. | Conteúdo correto, mas 'máscara' é jargão — e uma opção visível que a própria UI diz que não funciona não deveria ser oferecida assim. | **Os jogos mostram botões PlayStation (⨯  □ ), mas a vibração não funciona e o controle pode aparecer duplicado. Se quiser botões PlayStation COM vibração, use "Jogar direto (Sony)" na aba Início.** |
| 1920 | Máscara Xbox 360 (recomendada para jogar): a vibração funciona em jogo e o controle não aparece duplicado. Os jogos mostram prompts de Xbox (A/B/X/Y). | 'Máscara' e 'prompts' são jargão. | **Recomendado: vibração funciona e o controle não aparece duplicado. Os jogos mostram botões de Xbox (A/B/X/Y).** |
| 1948 | Suspende a emulação de mouse/teclado (igual ao combo PS+Options). O gamepad continua funcionando no jogo. Transitório — não sobrevive ao reboot. | 'O gamepad continua funcionando' é FALSO quando o modo é 'Controlar o PC' (vpad desligado); 'transitório/reboot' é meio técnico. | **O controle para de mexer no mouse/teclado do PC (igual a segurar PS ou PS+Options). Se você estiver em "Jogar pelo Hefesto", o controle segue funcionando no jogo. Desliga sozinho ao reiniciar.** |
| 1983 | Checa se o Steam Input (PSSupport) está ligado — ele conflita com o daemon. | 'PSSupport' e 'daemon' são jargão. | **Verifica se a Steam está tentando controlar o DualSense por conta própria — isso atrapalha o Hefesto (toques fantasma, microfone).** |
| 1990 | Desliga o Steam Input PSSupport (fecha e reabre a Steam). Evita o conflito com o daemon. | Jargão; e não avisa que precisa fechar a Steam ANTES. | **Impede a Steam de disputar o controle com o Hefesto. Feche a Steam antes de clicar.** |
| 2018 | Libera o mic embutido do DualSense (para jogos que pedem mic). O quirk segura o storm. | 'Quirk' e 'storm' são jargão interno incompreensível. | **Liga o microfone embutido do controle (para jogos com chat de voz). Requer a correção de USB instalada — sem ela o controle pode desconectar.** |
| 2025 | Suprime o mic do DualSense (não vira microfone padrão, sem spam). | 'Suprime' e 'spam' são vagos. | **Desliga o microfone do controle e impede que ele vire o microfone padrão do PC.** |
| 2034 | Gamepad p/ jogos: Xbox 360 é a recomendada — a vibração funciona e o controle não fica duplicado. DualSense mostra prompts de PlayStation, mas a vibração em jogo não funciona. O daemon vira o único leitor do controle. Requer o mód | Frases finais ('daemon vira o único leitor', 'módulo uinput carregado') são jargão sem ação possível para leigos. | **Xbox 360 é o recomendado: vibração funciona e o controle não fica duplicado. DualSense mostra botões PlayStation, mas sem vibração nos jogos. Para botões PlayStation com tudo funcionando, use "Jogar direto (Sony)" na aba Início.** |
| 2046 | Emulação | Título-jargão; o conteúdo útil (máscara, modo jogo) já vive na Início — o resto é diagnóstico. | **Avançado (após fundir o seletor de gamepad com a Início e remover itens mortos)** |
| 2062 | Emular mouse+teclado | 'Emular' é jargão; o modo já se chama 'Controlar o PC' na Início — usar a mesma família de termos. | **Usar o controle como mouse e teclado** |
| 2153 | Mapeamento | Termo técnico; o frame lista o que cada botão faz. | **O que cada botão faz** |
| 2224 | D-pad (↑↓←→) | "D-pad" é jargão de gamer em inglês. | **Direcional (↑↓←→)** |
| 2270 | Requer módulo uinput carregado e regra udev (ver aba Emulação). | uinput/udev na dica final da aba Mouse. | **Se não funcionar, abra a aba Avançado e use "Testar o controle virtual".** |
| 2270 | Útil para navegar o desktop, apresentações e jogos que só aceitam mouse/teclado. Requer módulo uinput carregado e regra udev (ver aba Emulação). | "módulo uinput" e "regra udev" são jargão; falta a dica do PS long-press que se perdeu com o MAPPING_LEGEND morto. | **Útil para navegar no computador, fazer apresentações e usar programas que só aceitam mouse/teclado. Se aparecer um aviso vermelho acima, rode o instalador de novo. Dica: segure o botão PS para pausar o mouse/teclado na hora de jog** |
| 2294 | Bindings do perfil ativo | 'Bindings' em inglês como título de seção. | **Atalhos de botão deste perfil** |
| 2302 | Formato: KEY_* (ex: KEY_C, KEY_ENTER) ou __OPEN_OSK__/__CLOSE_OSK__. Combos com '+' (ex: KEY_LEFTALT+KEY_TAB). | Fallback do glade com o mesmo jargão da legenda Python; manter os dois textos coerentes com a versão simplificada. | **Como escrever a tecla: KEY_ + o nome (ex.: KEY_C, KEY_ENTER). Combinações com + (ex.: KEY_LEFTALT+KEY_TAB).** |
| 2333 | Adicionar | Não diz o que adiciona nem que insere um botão arbitrário com KEY_SPACE. | **Adicionar botão (idealmente com um seletor de qual botão; ver bug correspondente)** |
| 2347 | Restaurar defaults | Mesma palavra grafada diferente do rodapé ('Restaurar Default', linha 2436) — dois botões, duas grafias, ambas em inglês. | **Restaurar padrão (nos dois lugares)** |
| 2404 | Envia toda a configuração (gatilhos, LEDs, rumble, mouse) ao controle | 'rumble' no tooltip do botão mais importante do app. | **Envia toda a configuração (gatilhos, luzes, vibração, mouse) ao controle** |
| 2409 | Aplicar todas as configuracoes / Envia gatilhos LEDs rumble e mouse ao controle | Sem acentos ("configuracoes") e com "rumble" no texto de acessibilidade. | **Aplicar todas as configurações / Envia gatilhos, luzes, vibração, mouse e teclado ao controle** |
| 2436 | Restaurar Default | "Default" é jargão em inglês. | **Restaurar padrão (tooltip: Volta o perfil 'Meu Perfil' ao estado de fábrica)** |

## `src/hefesto_dualsense4unix/app/actions/home_actions.py` (45)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 44 | ("native", "Jogar direto (Sony)") | "(Sony)" não diz nada a leigo — parece marca, não comportamento. E "direto" não deixa claro "direto no quê". | **("native", "Jogar sem o Hefesto")** |
| 48 | O controle vira mouse/teclado do computador (ajustes nas abas Mouse e Teclado). | Promete algo que o clique não faz (o mouse só anda se o switch da aba Mouse estiver ON) — engana enquanto o bug de comportamento não for corrigido. | **O controle vira mouse/teclado do computador. Ligue e ajuste na aba Mouse. (E corrigir o comportamento para o clique já ligar o mouse — ver bug.)** |
| 49 | O controle vira mouse/teclado do computador (ajustes nas abas Mouse e Teclado). | Promete algo que o código NÃO faz (ver bug HIGH: escolher este modo não liga a emulação de mouse). Texto e comportamento têm de casar. | **Use o controle como mouse e teclado: o analógico mexe a setinha e os botões clicam. Ajuste a velocidade nas abas Mouse e Teclado.** |
| 52 | "Recomendado para a maioria dos jogos: o Hefesto cuida de LEDs, vibração e de um controle por jogador. Para a vibração funcionar e o controle não aparecer duplicado no jogo, use a máscara Xbox 360 e cole as opções da Steam (aba Da | Jargão ('máscara') + transfere para a usuária DOIS trabalhos manuais que são bug nosso: escolher a máscara certa e colar opções na Steam. Um leigo lê isso e não sabe o que é 'opções da Steam' nem por que o controle apareceria dupl | **"Recomendado para a maioria dos jogos: o Hefesto cuida dos LEDs, da vibração e faz cada controle virar um jogador. Se o jogo mostrar o controle duas vezes, abra a aba Daemon e clique em \"Copiar opções p/ jogos\"."  — e resolver a** |
| 53 | Recomendado para a maioria dos jogos: o Hefesto cuida de LEDs, vibração e de um controle por jogador. Para a vibração funcionar e o controle não aparecer duplicado no jogo, use a máscara Xbox 360 e cole as opções da Steam (aba Dae | Queixa #1 em estado puro: 3 linhas, jargão ("máscara", "duplicado") e uma tarefa condicional jogada na usuária ("use a máscara X e cole as opções") que o programa deveria resolver sozinho. | **Escolha certa para quase todos os jogos. O Hefesto acende as luzes, faz o controle vibrar e dá um jogador para cada controle. Se um jogo não sentir a vibração, abra a aba Daemon e clique em "Copiar opções p/ jogos".** |
| 55 | Para a vibração funcionar e o controle não aparecer duplicado no jogo, use a máscara Xbox 360 e cole as opções da Steam (aba Daemon → "Copiar opções p/ jogos"). | 'Máscara' é jargão do doc de sprint (SPRINT-GAME-RUMBLE-01) que vazou para a descrição do modo mais usado. | **Para a vibração funcionar e o controle não duplicar no jogo, deixe o controle aparecendo como Xbox 360 (aqui embaixo) e use o botão "Copiar opções p/ jogos" (aba Daemon).** |
| 62 | Para jogos com suporte PS5 nativo: entrega os gatilhos adaptativos da Sony, mas o jogo fala direto com o controle — em alguns títulos isso desconecta o controle no meio da partida. Se acontecer, use "Jogar pelo Hefesto". | "suporte PS5 nativo", "gatilhos adaptativos" e "fala direto" são jargão. O texto vende um modo e no fim avisa que ele derruba o controle — a usuária não sabe o que fazer com isso. | **Só para jogos feitos para o PlayStation 5 (ex.: Sackboy). Os gatilhos ficam duros de apertar, como no PS5. Alguns jogos derrubam o controle no meio da partida neste modo — se isso acontecer, volte para "Jogar pelo Hefesto".** |
| 69 | Modo jogo (aba Emulação): suspende só mouse/teclado virtuais.  ·  Pausar: congela o daemon sem soltar o controle.  ·  Jogar direto: solta o controle para o jogo.  ·  Desligar Hefesto: para o daemon até você religar. | Glossário da tela inicial usa 'daemon' 2x e 'virtuais'. | **Modo jogo (aba Avançado): pausa só o mouse/teclado.  ·  Pausar: congela o Hefesto sem soltar o controle.  ·  Jogar direto: entrega o controle ao jogo.  ·  Desligar Hefesto: para tudo até você religar.** |
| 70 | Modo jogo (aba Emulação): suspende só mouse/teclado virtuais.  ·  Pausar: congela o daemon sem soltar o controle.  ·  Jogar direto: solta o controle para o jogo.  ·  Desligar Hefesto: para o daemon até você religar. | O glossário que existe para explicar os 4 'parar' usa 'daemon' duas vezes — o termo que ele deveria evitar. | **Modo jogo (aba Emulação): pausa só o mouse/teclado virtuais.  ·  Pausar: o Hefesto congela, mas continua segurando o controle.  ·  Jogar direto: solta o controle para o jogo.  ·  Desligar Hefesto: desliga tudo até você religar.** |
| 71 | Pausar: congela o daemon sem soltar o controle.  ·   | "daemon" é jargão puro e aparece no GLOSSÁRIO — justamente o texto que existe para EXPLICAR os termos. "congela" + "sem soltar" é ambíguo (soltar de quê?). | **Pausar: o Hefesto para de responder ao controle, mas continua sendo o dono dele (o jogo não recebe nada).  ·  ** |
| 73 | Desligar Hefesto: para o daemon até você religar. | "daemon" de novo, no glossário. "religar" não diz onde religar. | **Desligar Hefesto: fecha o Hefesto até você ligar de novo aqui nesta aba.** |
| 89 | parts.append("primário") | "primário" é conceito INTERNO (qual handle o daemon usa para output). A usuária não age sobre isso e o termo compete com o "P1" do título do card, sugerindo (falsamente) que são a mesma coisa. | **Trocar por "principal" e só exibir com 2+ controles E co-op desligado; com co-op ativo, remover a linha (o número do jogador já é a informação).** |
| 106 | return "…" + uniq[-6:]   # ex.: "…c311f0" | O hash não serve a NENHUMA tarefa da usuária: ela não tem onde ler esse número no controle físico (não está gravado no aparelho), então não consegue casar cardcontrole por ele. A distinção real que ela usa é o LED de jogador aces | **Remover a linha do card. Substituir pela pista que ela confere olhando para o controle: "luz de jogador 2 acesa" (com co-op ativo), ou nada.** |
| 128 | Gtk.Frame(label="O que o controle faz agora") | Bom (é o único título da aba escrito pela ação). Falta paralelismo com o applet, que usa caixa-alta "O QUE O CONTROLE FAZ" (app.rs:655) — sem o "agora". | **Manter "O que o controle faz agora" e alinhar o applet (app.rs:655) para o MESMO texto.** |
| 157 | Gtk.CheckButton(label="Cada controle é um jogador (padrão com 2+ controles)") | Queixa #2: elemento que não deveria existir. "(padrão com 2+ controles)" é a UI se explicando por não ter certeza de si. Desmarcar produz o estado "todos são o mesmo jogador", que ninguém quer. | **REMOVER o widget. Substituir por uma linha informativa só quando houver 2+ controles: "2 controles conectados = 2 jogadores." (sem checkbox, sem opt-out na UI).** |
| 158 | Cada controle é um jogador (padrão com 2+ controles) | Queixa direta da mantenedora: opção que ninguém quer desligar não deveria ser visível — mover para um expander 'Avançado' ou remover; se ficar, sem o parêntese técnico. | **(ocultar por padrão; se mantida) Cada controle é um jogador** |
| 158 | label="Cada controle é um jogador (padrão com 2+ controles)" | A mantenedora pediu explicitamente que este checkbox seja SEMPRE ligado e INVISÍVEL. Além disso o texto expõe uma decisão que ninguém quer tomar ('padrão com 2+ controles' é ruído: com 1 controle a opção não faz nada; com 2+, desl | **REMOVER o checkbox da interface (é o pedido literal). O co-op passa a ser sempre ligado: `coop_enabled` fica True e o gate real vira 'há 2+ controles?'. Se for preciso manter um opt-out para caso raro, mover para a aba Daemon como** |
| 167 | Gtk.Label(label="O jogo vê o controle como:") | A pergunta certa seria "por que eu escolheria isso?". Se a máscara DualSense sair do Início (recomendado), a linha inteira sai junto. | **Remover a linha do Início. Se ficar: "Como o jogo mostra os botões:"** |
| 167 | flavor_label = Gtk.Label(label="O jogo vê o controle como:") | Sobra da era 'máscara'. Descreve o mecanismo ('o jogo vê como') em vez da consequência que a usuária percebe (quais botões aparecem desenhados na tela). | **flavor_label = Gtk.Label(label="Ícones dos botões no jogo:")** |
| 172 | ("xbox", "Xbox 360 (vibra)") | "(vibra)" só faz sentido em contraste com a outra opção — é a UI pedindo desculpa pela opção quebrada ao lado. | **Se as duas opções continuarem: ("xbox", "Botões A B X Y (recomendado)"). Se a DualSense sair do Início: remover o seletor inteiro.** |
| 173 | ("dualsense", "DualSense (botões PS, sem vibrar)") | Queixa #3. Além de shipar uma opção que não vibra, o rótulo OMITE a consequência pior e já documentada no código (uinput_gamepad.py:93-102): o jogo passa a enxergar DOIS controles (o físico + o virtual), porque o vpad usa o mesmo  | **Tirar do Início. Mover para a aba Emulação como opção avançada com texto honesto: "Botões    □ (avançado — nesta opção o jogo NÃO vibra e pode enxergar dois controles)."** |
| 207 | Gtk.Frame(label="Sessão") | "Sessão" é vocabulário de programador; não descreve nada que a usuária reconheça. | **Gtk.Frame(label="Ligar e desligar")** |
| 215 | Gtk.Button(label="Desligar Hefesto (voltar ao Linux puro)") | "Linux puro" é jargão e não é o que a usuária quer saber — ela quer saber se o controle vai parar de funcionar. | **Gtk.Button(label="Desligar o Hefesto") com tooltip: "O controle continua funcionando nos jogos, mas sem luzes, sem gatilhos e sem os seus ajustes."** |
| 277 | "Daemon desligado — religue na aba Daemon (Iniciar)." | Dois problemas. (a) "Daemon" é jargão. (b) É MENTIRA em timeout: essa string aparece sempre que o state_full estoura 0,25s (home_actions.py:266), mesmo com o Hefesto vivo — manda a usuária "religar" algo que já está ligado. | **"O Hefesto não respondeu. Se ele estiver desligado, ligue na aba Daemon (Iniciar)." — e só dizer "desligado" com certeza (após N falhas seguidas ou socket ausente).** |
| 277 | Daemon desligado — religue na aba Daemon (Iniciar). | "Daemon" é a palavra mais jargão do app inteiro, e aparece na PRIMEIRA aba, no estado de erro (justo quando a usuária está perdida). Manda procurar uma aba em vez de oferecer o botão. | **"O Hefesto está desligado — o controle está funcionando sozinho." + um botão "Ligar o Hefesto" ali mesmo (chamando o mesmo caminho de daemon_actions.py:479, que limpa o _user_stopped_daemon).** |
| 314 | origin_bits.append("nativo ligado pelo perfil ativo") | "nativo" não é nenhum dos 3 rótulos que a usuária vê (ela vê "Jogar direto (Sony)"). Vocabulário interno vazando. | **origin_bits.append("o perfil deste jogo escolheu este modo sozinho")** |
| 316 | origin_bits.append("gamepad ligado pelo perfil ativo") | Idem: "gamepad" não é o rótulo do modo ("Jogar pelo Hefesto"), e a frase é idêntica em função à de cima — duas mensagens para o mesmo fato. | **Unificar com a linha 314 numa só: "o perfil deste jogo escolheu este modo sozinho".** |
| 318 | origin_bits.append(f"co-op: {coop.get('players')} jogador(es)") | "co-op" é jargão (queixa #1) e "jogador(es)" com parêntese é gambiarra de plural — com 1 controle sai literalmente "co-op: 1 jogador(es)". | **players = coop.get('players'); origin_bits.append("1 jogador" if players == 1 else f"{players} jogadores")** |
| 345 | Gtk.Label(label="Nenhum controle conectado.") | Texto certo, ramo inalcançável no caminho online (ver bug do card fantasma) e ambíguo no offline, onde aparece junto de "Daemon desligado" e a usuária não sabe se o problema é o controle ou o programa. | **Online sem controle: "Nenhum controle ligado. Conecte pelo cabo USB ou segure PS + Share para parear." Offline: "—" (a mensagem do Hefesto desligado já explica).** |
| 357 | name = f"Controle {idx + 1} — {player}"   # player = f"P{idx + 1}" | "Controle 1 — P1" é redundante (dois números iguais para dizer a mesma coisa) e vira MENTIRA com co-op desligado (todos são P1) — ver bug HIGH. | **Com co-op ativo: f"Jogador {n}" (n = índice REAL do CoopManager). Sem co-op ativo: f"Controle {idx+1}" sem o "— Pn".** |
| 380 | grab falhou — input pode dobrar no jogo | 'grab' e 'input' num AVISO de erro para leigo. | **Atenção: o jogo pode receber os comandos em dobro — desconecte e reconecte este controle** |
| 380 | Gtk.Label(label="grab falhou — input pode dobrar no jogo") | "grab" e "input dobrar" são jargão de kernel exibido direto na cara da usuária, sem dizer o que ela deve FAZER. | **"O jogo pode estar vendo este controle duas vezes. Feche o jogo e volte a abri-lo."** |
| 380 | warn = Gtk.Label(label="grab falhou — input pode dobrar no jogo") | Jargão puro em texto de ERRO, que é justamente onde o leigo mais precisa entender. 'grab' e 'input dobrar' não significam nada fora do projeto, e o aviso não diz o que fazer. | **warn = Gtk.Label(label="Este controle pode aparecer duas vezes no jogo. Feche o jogo, desconecte e reconecte o controle.")** |
| 398 | Modo aplicado: {mode_id} | Mostra o id interno em inglês ('gamepad'/'native'/'desktop') em vez do rótulo que o usuário clicou; idem 'Máscara do gamepad: {flavor_id}' na linha 487. | **Modo aplicado: Jogar pelo Hefesto (usar o label de _MODE_ITEMS; na 487: 'O jogo agora vê: Xbox 360')** |
| 398 | self._status_toast("home", f"Modo aplicado: {mode_id}") | `mode_id` é o ID interno cru — a usuária lê "Modo aplicado: gamepad" / "Modo aplicado: native" / "Modo aplicado: desktop". Palavras que não existem na interface (os botões dizem "Jogar pelo Hefesto", "Jogar direto (Sony)", "Contro | **Usar o rótulo do `_MODE_ITEMS`: `label = dict(_MODE_ITEMS).get(mode_id, mode_id)` e o toast vira `f"Pronto — agora: {label}"` (ex.: "Pronto — agora: Jogar pelo Hefesto").** |
| 403 | self._status_toast("home", f"Falha ao mudar o modo ({exc})") | `exc` é o `IpcError`, cujo __str__ é `f"[{code}] {message}"` (ipc_client.py:27). A usuária lê literalmente "Falha ao mudar o modo ([-32003] gamepad.emulation.set exige 'enabled' boolean)" ou "([-1] conexão timeout)". Código JSON-R | **Mapear por tipo: timeout/offline → "Não consegui falar com o Hefesto. Ele está ligado? (aba Daemon → Iniciar)"; demais → "Não deu para mudar o modo agora. Tente de novo." e mandar o `exc` para o logger, não para a tela.** |
| 460 | ("Co-op ligado" if enabled else "Co-op desligado") + extra | "Co-op" é jargão puro (queixa #1). O sufixo `extra` vira "Co-op ligado (2 jogadores)". | **"Agora cada controle é um jogador (2 jogadores)" / "Agora todos os controles jogam como o jogador 1".** |
| 460 | "home", ("Co-op ligado" if enabled else "Co-op desligado") + extra | 'Co-op' é jargão. Se o checkbox for removido (wording #3), este toast morre junto; enquanto existir, precisa falar português. | **"home", ("Cada controle é um jogador" if enabled else "Todos os controles agem como o mesmo jogador") + extra** |
| 466 | self._status_toast("home", f"Falha no co-op ({exc})") | "co-op" é jargão + `exc` vaza "[-32003] ...". Além disso a queixa #2 diz que esse controle nem deveria estar visível. | **Se o checkbox sumir (recomendado), a string morre junto. Enquanto existir: "Não deu para mudar quem é cada jogador. Tente de novo."** |
| 468 | self._status_toast("home", f"Falha no co-op ({exc})") | Jargão + exceção crua. | **Remover com o checkbox.** |
| 487 | self._status_toast("home", f"Máscara do gamepad: {flavor_id}") | Dois jargões numa frase só: "máscara", "gamepad" — e `flavor_id` cru ("xbox"/"dualsense"). O próprio seletor logo acima já fala em português ("O jogo vê o controle como:"). | **`f"Pronto — o jogo agora vê o controle como {label}"`, com label = "um Xbox 360 (vibra)" ou "um DualSense (botões PS, sem vibrar)".** |
| 508 | text="Desligar o Hefesto?" | Nenhum — é a única string da aba que fala a língua da usuária. | **Manter "Desligar o Hefesto?"** |
| 511 | O daemon para e o controle volta ao comportamento puro do Linux.\nA GUI continua aberta e NÃO religa o daemon sozinha — religue na aba Daemon (Iniciar) ou feche e abra o painel. | "daemon" (2x), "GUI", "comportamento puro do Linux" — 3 jargões num diálogo de confirmação, que é exatamente onde a usuária precisa entender a consequência. | **"O controle continua funcionando nos jogos, mas sem luzes, sem gatilhos e sem os seus ajustes.\n\nEsta janela fica aberta. Para religar, use o botão \"Ligar o Hefesto\" aqui na aba Início."** |
| 531 | Hefesto desligado — controle no modo puro do Linux | "modo puro do Linux" não é um modo; é uma metáfora de programador. | **"Hefesto desligado — o controle está funcionando sozinho."** |
| 540 | "Falha ao desligar via systemd" + (f" ({err})" if err else "") + " — se o daemon roda avulso, pare-o na aba Daemon." | "systemd", "daemon", "roda avulso" + stderr cru. A usuária não sabe (nem deve saber) se o processo é avulso ou de serviço. | **"Não consegui desligar o Hefesto. Tente pela aba Daemon → Parar." (systemd/stderr só no logger).** |

## `packaging/cosmic-applet/src/app.rs` (29)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 470 | Modo jogo / Sair do modo jogo | colide com 'Jogar pelo Hefesto' (dois conceitos de 'jogo' no mesmo popover); não diz o que faz | **Pausar mouse/teclado do controle / Reativar mouse/teclado do controle** |
| 470 | "Modo jogo" / "Sair do modo jogo" | Ambíguo ao lado do seletor 'Jogar pelo Hefesto' — parece ser o modo de jogar, mas só suspende mouse/teclado | **"Pausar mouse/teclado (modo jogo)" / "Reativar mouse/teclado"** |
| 470 | ("input-gaming-symbolic", "Modo jogo") | "Modo jogo" colide de frente com o comutador "O QUE O CONTROLE FAZ" logo acima, que já tem "Jogar pelo Hefesto" e "Jogar direto (Sony)". Três coisas diferentes chamadas "jogo" na MESMA tela — a usuária não tem como saber que esta  | **"Desligar mouse e teclado do controle" / (ativo) "Religar mouse e teclado do controle".** |
| 508 | "Abrir painel" / "Fechar painel" | No COSMIC, 'Painel' é a barra do sistema (Configurações > Painel) — colide com o vocabulário do desktop | **"Abrir o Hefesto" / "Fechar a janela do Hefesto" (aplicar também em app/tray.py:164)** |
| 551 | "Daemon desconectado" | Jargão 'daemon' para leigos | **"Hefesto desligado — use 'Abrir painel' para religar"** |
| 553 | Daemon desconectado | 'Daemon' é jargão que leigo não entende | **Hefesto desligado** |
| 560 | Consultando… | verbo técnico | **Verificando…** |
| 593 | "Jogando direto (pelo perfil)" | 'pelo perfil' é conceito interno; a usuária pensa em 'o jogo ativou' | **"Jogando direto (ativado pelo jogo)"** |
| 627 | ligado (mouse/teclado suspensos) | 'suspensos' é formal; ok mas dá pra simplificar | **ligado (o controle não mexe no mouse/teclado)** |
| 627 | "ligado (mouse/teclado suspensos)" | "suspensos" é técnico e não diz o efeito prático. | **"ligado (o controle não mexe mais o cursor)".** |
| 633 | Pausado (sem enviar input) | 'input' é jargão | **Pausado (o controle não age no PC)** |
| 635 | "Pausado (sem enviar input)" | Jargão 'input' | **"Pausado (o controle não age no PC)"** |
| 636 | "Pausado (sem enviar input)" | "input" é jargão. | **"Pausado (o controle não faz nada até você retomar)".** |
| 655 | O QUE O CONTROLE FAZ | GUI usa 'O que o controle faz agora' — leve divergência de paridade | **O QUE O CONTROLE FAZ AGORA** |
| 683 | [x] Cada controle = um jogador — 2 jogadores | mantenedora decidiu que isso deve ser sempre ligado e invisível (ninguém liga 2 controles para 1 jogador); se mantido, o plural quebra com 1 ('1 jogadores') e '[x]' é gambiarra visual | **Remover o toggle do popover (co-op sempre ligado); se mantido em 'avançado': 'Cada pessoa joga com um controle — 2 jogadores' com singular/plural correto** |
| 685 | format!("[x] Cada controle = um jogador — {} jogadores", state.coop.players) | Queixa #2: esse toggle deveria ser sempre ligado e INVISÍVEL. Além disso "[x]"/"[ ]" é checkbox ASCII de terminal dentro de um applet gráfico do COSMIC. | **Remover o botão. Se a contagem for útil, vira linha de status só-leitura: "Jogadores: 2 (um por controle)".** |
| 688 | "[x] Cada controle = um jogador — {n} jogadores" / "[ ] Cada controle = um jogador" | Queixa 2 da mantenedora: ninguém conecta 2 controles esperando controlar o mesmo jogador — o toggle não deveria ser exposto; e '[x]/[ ]' é afordância pobre | **Remover o toggle do popover e mostrar só informação: "Jogadores: {n} (um por controle)"; se mantiver o toggle, "Cada controle é um jogador ({n} jogadores)"** |
| 701 | Máscara DualSense / Máscara Xbox | 'Máscara' é jargão; falta a informação crítica (DualSense = sem vibração nos jogos) que a GUI dá | **Xbox 360 — vibração funciona / DualSense — botões PS, sem vibração nos jogos (paridade com a GUI: 'Xbox 360 (vibra)' / 'DualSense (botões PS, sem vibrar)')** |
| 701 | "Máscara DualSense" / "Máscara Xbox" | Jargão 'máscara' + não diz a consequência (vibração) + ordem e nome divergem da GUI ('Xbox 360 (vibra)' primeiro, 'DualSense (botões PS, sem vibrar)' depois) | **Trocar por, na mesma ordem da GUI: "Xbox 360 (vibra nos jogos)" e "DualSense (botões PS, sem vibração)" sob o cabeçalho "O jogo vê o controle como:"** |
| 701 | let flavors = [("dualsense", "Máscara DualSense"), ("xbox", "Máscara Xbox")]; | Jargão "máscara" + NÃO diz a consequência. A GUI já foi corrigida para "Xbox 360 (vibra)" / "DualSense (botões PS, sem vibrar)" (home_actions.py:171-174) e ordena Xbox primeiro; o applet ficou para trás e ainda lista DualSense pri | **Espelhar a GUI, inclusive a ordem: `[("xbox", "Xbox 360 (vibra)"), ("dualsense", "DualSense (botões PS, sem vibrar)")]`, sob um caption "O JOGO VÊ O CONTROLE COMO".** |
| 730 | CONTROLE-ALVO | 'alvo' é linguagem de engenharia; usuário não sabe o que está mirando | **APLICAR AJUSTES EM** |
| 730 | "CONTROLE-ALVO" | Jargão técnico ('alvo' de output) — não explica o efeito | **"APLICAR AJUSTES EM"** |
| 730 | text::caption_heading("CONTROLE-ALVO") | "alvo" é tradução literal de "target" — não diz o que faz. A GUI não tem esse conceito em lugar nenhum, então não há de onde aprender. | **"APLICAR AJUSTES EM" (fica "APLICAR AJUSTES EM: Todos os controles / Controle 1 — USB").** |
| 734 | Todos (broadcast) | 'broadcast' é jargão de rede | **Todos os controles** |
| 734 | "Todos (broadcast)" | Jargão 'broadcast' | **"Todos os controles"** |
| 734 | format!("{todos_mark}Todos (broadcast)") | "broadcast" é jargão de rede. A usuária não faz ideia do que é. É o item DEFAULT — a primeira palavra estranha que ela vê no seletor. | **"Todos os controles".** |
| 748 | let label = format!("{mark}Controle {} — {transporte}", c.index + 1); | O fallback de transporte é "?" (app.rs:746), então em transporte desconhecido a usuária lê "Controle 2 — ?". | **Omitir o traço quando desconhecido: "Controle 2". E, com bateria disponível, "Controle 2 — USB · 87%" (paridade com o card da aba Início).** |
| 771 | Indisponível (daemon offline) | 'daemon offline' é jargão duplo | **Indisponível (Hefesto desligado)** |
| 772 | "Indisponível (daemon offline)" | Jargão 'daemon offline' | **"Indisponível (Hefesto desligado)"** |

## `install.sh` (25)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 29 | --yes, -y             responde sim a todos os prompts (autostart, hotplug, AppIndicator extension, etc) e assume --format=native. | Mentira funcional: com -y o hotplug fica NÃO (default 'n' na linha 834) e o storm-watch liga (linha 869). | **--yes, -y             usa as respostas recomendadas em todos os prompts (autostart SIM, abrir-ao-plugar NÃO, storm-watch SIM) e assume --format=native.** |
| 211 | >>> Alguns passos precisam de sudo (udev, cura do storm, applet COSMIC). | Três jargões numa linha (sudo/udev/storm/applet) na primeira mensagem que o leigo vê. | **>>> Alguns passos precisam da sua senha de administrador (permissões do controle, correção de USB e ícone do painel). Vou pedir a senha UMA vez só.** |
| 238 |   1) native    venv editável + atalho (instalação de desenvolvimento, atual/default) | A opção RECOMENDADA é descrita com jargão de programador ('venv editável', 'desenvolvimento') — leigo acha que não é para ele e escolhe outra (que hoje pula metade dos passos). | **  1) padrão    instala a partir desta pasta e cria o atalho no menu (recomendado)** |
| 496 | step "3/11" "udev rules (hidraw + uinput + autosuspend)" | Título do passo é 100% jargão. | **step "3/11" "permissões do sistema para o controle funcionar"** |
| 518 | copiando %d regras canônicas + modules-load uinput (sudo) | 'regras canônicas' e 'modules-load uinput' não dizem nada ao leigo. | **aplicando %d regras do sistema (usa a senha de administrador)** |
| 532 | (73/74 descontinuadas; 75 áudio-off é opt-in via --disable-usb-audio) | Nota interna de manutenção vazando para o usuário — e cita uma flag que o install.sh nem aceita. | **Remover a linha do output (ou: "opcional: desligar o áudio USB do controle — sudo bash scripts/install_udev.sh --disable-usb-audio").** |
| 583 | step "3c" "cura de raiz do storm (snd_usb_audio quirk — preserva mic+fone)" | 'storm', 'quirk' e 'snd_usb_audio' são jargão; leigo não sabe que problema está sendo curado. | **step "3c" "correção do defeito de desconexão USB do DualSense (mantém microfone e fone)"** |
| 595 | cura persistente OK em %s + ativada (replug do controle p/ valer já) | 'persistente', caminho de arquivo e 'replug' — instrução escondida no jargão. | **correção aplicada — desconecte e reconecte o controle para valer agora (e fica salva para os próximos boots)** |
| 597 | cura NÃO persistiu — ${SND_QUIRK_CONF} ausente (sudo recusado?) | Leigo não entende 'persistiu' nem o caminho; não sabe o que fazer. | **a correção NÃO ficou salva (faltou a senha de administrador). Rode: sudo bash scripts/install_snd_quirk.sh** |
| 668 | o autoswitch de perfil precisa de uma das opções abaixo: | 'autoswitch' é jargão. | **para o Hefesto trocar o perfil sozinho conforme o jogo aberto, escolha uma das opções abaixo:** |
| 700 | ativar GDK_BACKEND=x11 no atalho (recomendado como complemento)? | Nome de variável de ambiente num prompt sim/não para leigo. | **usar o modo de compatibilidade de janelas (XWayland) no atalho? (recomendado no COSMIC)** |
| 718 | Comment=Daemon de gatilhos adaptativos para DualSense no Linux | 'Daemon' no texto do atalho do menu que o leigo vê ao passar o mouse (idem packaging/hefesto-dualsense4unix.desktop:2). | **Comment=Configure seu controle de PS5 (DualSense): gatilhos, vibração, luz e jogadores** |
| 791 | step "6/11" "daemon systemd --user" | 'daemon systemd --user' é jargão puro. | **step "6/11" "serviço em segundo plano que mantém o controle funcionando"** |
| 804 | habilitar auto-start do daemon no boot? | 'auto-start do daemon no boot' — três jargões. | **iniciar o Hefesto automaticamente quando ligar o computador? (recomendado)** |
| 815 | unit instalada (auto-start desativado — subir só quando abrir a GUI) | 'unit', 'subir', 'GUI' — leigo não sabe o que foi instalado nem o efeito. | **serviço instalado (só liga quando você abrir o programa)** |
| 825 | step "7/11" "hotplug USB → abre a GUI automaticamente" | 'hotplug' e 'GUI' são jargão (e a feature está morta — corrigir antes de reescrever). | **step "7/11" "abrir a janela do Hefesto sozinha ao conectar o controle"** |
| 952 | compilando + instalando (1a build do libcosmic e LONGA, >10 min) | 'build do libcosmic' não diz nada; usuário pode achar que travou. | **preparando o ícone do painel do COSMIC — a primeira vez pode levar mais de 10 minutos, pode deixar rodando** |
| 954 | applet instalado — adicione em Config. > Paineis > Miniaplicativos | 'applet' é jargão; 'Config.' abreviado não bate com o nome do app de Configurações. | **ícone do painel instalado — ative em Configurações > Painéis > Miniaplicativos** |
| 974 | step "10/11" "audio: impedir o DualSense de virar o microfone padrão" | Bom, mas 'audio' sem acento e sem dizer o sintoma que o leigo reconhece. | **step "10/11" "áudio: impedir que o controle 'roube' o microfone do sistema"** |
| 990 | pulado (use --with-wireplumber-disable-mic ou --with-wireplumber-fix, ou: scripts/doctor.sh --fix) | Duas flags compridas de jargão como primeira opção; a ação simples (doctor --fix) vem por último. | **pulado — se o controle virar o microfone padrão do sistema, rode: bash scripts/doctor.sh --fix** |
| 1004 | step "11/11" "Steam: desligar PSSupport do PlayStation Controller" | 'PSSupport' é nome interno de chave do vdf, invisível para o usuário da Steam. | **step "11/11" "Steam: impedir que a Steam tome o controle do DualSense (evita botão duplicado e mouse fantasma)"** |
| 1011 | Steam Input PSSupport zerado em todos os localconfig.vdf | 'PSSupport zerado' e 'localconfig.vdf' são jargão de arquivo interno. | **pronto — a Steam não vai mais interceptar o controle (para desfazer: bash scripts/disable_steam_input.sh --restore)** |
| 1028 | guard do Steam Input habilitado (path + timer 30min) | 'guard', 'path', 'timer' — o usuário não fica sabendo O QUE isso faz nem que a config da Steam será desfeita sozinha. | **proteção ativada: se a Steam tentar retomar o controle (após updates), o Hefesto desfaz sozinho. Para desativar: ./uninstall.sh ou systemctl --user disable --now hefesto-steam-input-guard.timer hefesto-steam-input-guard.path** |
| 1041 |  Abrir:       hefesto-dualsense4unix-gui | Manda o leigo para o terminal; o caminho fácil (menu de apps) não é citado. | ** Abrir: procure "Hefesto" no menu de aplicativos (ou digite hefesto-dualsense4unix-gui no terminal)** |
| 1059 | O quirk de áudio USB segura o storm -71 com o mic ligado. | 'quirk', 'storm -71' — o aviso mais importante do rodapé é ilegível para leigo. | **Vai usar o MICROFONE do controle? Aplique também esta correção extra (evita quedas de USB com o microfone ligado): bash scripts/install_usb_quirk.sh** |

## `src/hefesto_dualsense4unix/app/actions/trigger_specs.py` (25)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 34 | TriggerParamSpec("position", "Posição", 0, 9, default) | "Posição" sozinho não diz posição de quê nem que 0=solto e 9=fundo. | **"Ponto do gatilho (0 = solto, 9 = fundo)"** |
| 38 | TriggerParamSpec("start", "Início", lo, hi, default) | "Início" sem unidade nem referência; o usuário não sabe que é ponto do curso do gatilho. | **"Começa no ponto"** |
| 42 | TriggerParamSpec("end", "Fim", lo, hi, default) | Idem 'Início'. E nada avisa que Fim precisa ser maior que Início (ver BUG-3). | **"Termina no ponto (precisa ser maior que o início)"** |
| 50 | TriggerParamSpec("force", "Força (0-8)", 0, 8, default) | O '(0-8)' no rótulo é ruído: o slider já mostra o número e o range. | **"Força" (deixar o range para o slider)** |
| 54 | TriggerParamSpec("strength", "Intensidade (0-8)", 0, 8, default) | Mesma coisa: range no rótulo é redundante com o slider. | **"Intensidade"** |
| 58 | TriggerParamSpec("frequency", "Frequência", 0, 255, default) | "Frequência" (0-255) não tem significado físico para o usuário — não é Hz. | **"Velocidade das batidas"** |
| 67 | "Rigid", "Rígido (Rigid)" | Nome bilíngue: repete o termo técnico em inglês entre parênteses sem acrescentar nada para leigo. | **"Trava firme" — descrição: "O gatilho trava num ponto e não passa dali."** |
| 72 | "SimpleRigid", "Rígido simples" / description="Atalho de Rigid em escala 0-8." | A descrição cita o nome interno 'Rigid' e a 'escala 0-8', que é detalhe de implementação HID. | **Label: "Trava firme (fácil)" — descrição: "Igual à Trava firme, com um único controle de força."** |
| 77 | "Pulse", "Pulso" / description="Pulso único." | "Pulso único." não diz o que a mão sente nem em que jogo usar. | **Label: "Batida única" — descrição: "Dá um tranco só quando você aperta o gatilho."** |
| 82 | "PulseA", "Pulso A" / description="Pulso entre duas posições (curva A)." | "curva A" não significa nada para o usuário; A e B são só variantes do bit HID. | **Label: "Batida contínua (suave)" — descrição: "Bate repetidamente entre dois pontos do curso do gatilho."** |
| 87 | "PulseB", "Pulso B" / description="Pulso entre duas posições (curva B)." | Idem 'curva B'; indistinguível de 'Pulso A' para quem lê. | **Label: "Batida contínua (seca)" — descrição: "Como a Batida contínua, mas com tranco mais duro."** |
| 92 | "Resistance", "Resistência" / description="Resistência constante a partir de uma posição." | "a partir de uma posição" é abstrato — o usuário não sabe que 'posição' é o quanto o gatilho já foi apertado. | **Label: "Peso constante" — descrição: "A partir do ponto escolhido, o gatilho fica pesado até o fim."** |
| 96 | "Bow", "Arco (Bow)" | Nome bilíngue redundante. | **"Arco e flecha" — descrição já boa: "Tensão crescente com disparo ao soltar." → "Vai ficando duro conforme você puxa e solta de repente."** |
| 106 | "Galloping", "Galope (Galloping)" | Nome bilíngue redundante. | **"Galope" — descrição: "Batidas em ritmo de cavalo galopando."** |
| 110 | TriggerParamSpec("first_foot", "Pata 1 (0-7)", 0, 7, 7) | "Pata 1" é tradução literal de 'first_foot' — sem a metáfora do galope explicada, é incompreensível. | **"Força da 1ª batida" (e "Força da 2ª batida" na linha 111)** |
| 120 | TriggerParamSpec("end", "Fim (start+1..8)", 3, 8, 6) | Rótulo com SINTAXE DE CÓDIGO e nome de variável em inglês ('start+1..8') exposto ao usuário final. | **"Termina no ponto (depois do início)"** |
| 135 | "Machine", "Metralhadora (Machine)" / description="Metralhadora com dois picos de amplitude." | Nome bilíngue + "dois picos de amplitude" é jargão de sinal. | **Label: "Metralhadora" — descrição: "Rajada rápida, alternando entre dois trancos."** |
| 147 | "Feedback", "Feedback" / description="Feedback simples em posição específica." | "Feedback" é palavra em inglês e a descrição usa a mesma palavra que tenta explicar (circular). | **Label: "Ponto de resistência" — descrição: "O gatilho fica mais pesado num ponto do curso."** |
| 152 | "Weapon", "Arma (Weapon)" / description="Disparo de arma padrão." | Nome bilíngue redundante. | **Label: "Tiro de arma" — descrição: "Resiste até um ponto e cede de uma vez, como um gatilho de pistola."** |
| 162 | "SlopeFeedback", "Feedback em rampa" / description="Feedback com intensidade variando em rampa." | "Feedback" em inglês + descrição circular ('rampa com rampa'). | **Label: "Peso crescente" — descrição: "Começa leve e vai ficando pesado até o fim do curso."** |
| 172 | "MultiPositionFeedback", "Feedback por posição" / description="Intensidade customizada por cada uma das 10 posições." | "Feedback" em inglês; "customizada" é anglicismo. | **Label: "Peso ponto a ponto" — descrição: "Você escolhe o peso em cada um dos 10 pontos do curso do gatilho."** |
| 182 | "MultiPositionVibration", "Vibração por posição" / description="Vibração com perfil de amplitude por posição." | "perfil de amplitude" é jargão de engenharia. | **Label: "Vibração ponto a ponto" — descrição: "Você escolhe a força da vibração em cada um dos 10 pontos do curso."** |
| 195 | "Custom", "Custom (raw HID)" / description="Envia valores HID crus (mode + 7 forces)." | Pior string da aba: 'Custom' + 'raw HID' + 'mode' + 'forces' — 4 termos técnicos em inglês numa opção visível por padrão a qualquer usuário. | **Label: "Avançado (valores crus)" — descrição: "Só para quem sabe o que está fazendo: envia os números diretos para o controle. Se não souber, use os modos acima." (idealmente atrás de um 'Modo avançado', como já existe na aba Perf** |
| 197 | TriggerParamSpec("mode", "Mode HID (byte)", 0, 255, 0) | Três jargões em inglês num rótulo de slider: 'Mode', 'HID', 'byte'. | **"Código do modo (0-255)"** |
| 201 | TriggerParamSpec(f"force_{i}", f"Force {i}", 0, 255, 0) | Rótulo em INGLÊS visível na GUI ('Force 0' .. 'Force 6'). | **f"Valor {i+1}" (ou "Força {i+1}")** |

## `README.md` (19)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 23 | Estado: runtime validado em Pop!_OS 22.04 e 24.04 COSMIC com DualSense USB+BT; 2022 testes unit, ruff clean, mypy zero; CURA DE RAIZ do travamento do USB (storm -71) instalada por padrão... (parágrafo único de ~200 palavras com st | A primeira coisa que o usuário lê é um parágrafo-rio de jargão técnico (storm -71, hidraw, vpad implícito, MAC, quirk) — é changelog disfarçado de estado. | **Estado: funciona em Pop!_OS 22.04/24.04 (COSMIC) com DualSense por cabo e Bluetooth, até 4 controles — cada um vira um jogador. Vibração dos jogos, luzes, gatilhos e microfone funcionando; o defeito que desconectava o controle no ** |
| 60 | 7 defaults (`navegacao`, `fps`, `aventura`, `acao`, `corrida`, `esportes`, `meu_perfil`) | Existem 12 presets; os 5 ausentes (point_and_click, sackboy_nativo, coop_local, bow, fallback) são justamente os que carregam features novas. | **12 perfis de fábrica (navegação, fps, aventura, ação, corrida, esportes, meu_perfil, bow, fallback, point_and_click, sackboy_nativo, coop_local)** |
| 61 | Troca de perfil automática por janela ativa (X11 nativo, Wayland via portal XDG) com lock de 30 s após escolha manual via tray/CLI | Promete detecção Wayland via portal que não funciona (o próprio README:529 admite); engana usuário COSMIC. | **Troca de perfil automática pela janela em foco (jogos Steam/Proton e apps X11; apps Wayland nativos no COSMIC ainda não são detectados — use o atalho PS+setas). Trava por 30 s após escolha manual.** |
| 86 | A GUI principal expõe 10 abas no `GtkNotebook` central, cada uma cobrindo um eixo do controle. | Diz 10 abas mas a tabela lista 9 — falta a Início, a mais importante (modos, co-op, máscara, desligar). | **A interface tem 10 abas. Adicionar a linha: \| **Início** \| Escolher o que o controle faz agora. É a primeira aba. \| Botões 'Controlar o PC' / 'Jogar pelo Hefesto' / 'Jogar direto (Sony)'; como o controle aparece pro jogo (Xbox ** |
| 90 | Dashboard ao vivo do controle e do daemon. É a primeira aba e onde você confirma se conectou. | Status não é mais a primeira aba desde a v3.12 (Início é — main.glade:153); e 'daemon' é jargão. | **Painel ao vivo do controle. É onde você confirma se o controle conectou (fica logo depois da aba Início).** |
| 91 | combobox **Modo** (19 modos: Off, Rigid, Pulse...), combobox **Preset** | Os combos foram extintos (viraram botões segmentados nas v3.10/3.11 por causa do bug de foco do COSMIC); usuário procura um dropdown que não existe. | **botões de **Modo** (19 efeitos: Off, Rigid, Pulse, Galloping, Machine, Bow, Automatic Gun, etc.), botões de **Preset** (leve/média/dura)** |
| 96 | Gamepad virtual Xbox 360 via `uinput`, pra jogos que só aceitam controles Microsoft. \| Toggle **on/off** de `/dev/input/js*` virtual com forward 60 Hz; status do device emulado; mapeamento dos botões DualSense → Xbox360. | Descrição de 2 versões atrás: hoje o gamepad virtual é o coração do modo 'Jogar pelo Hefesto', tem duas máscaras e o cartão reflete a máscara real. | **O controle virtual que o jogo enxerga no modo 'Jogar pelo Hefesto'. \| Estado do controle virtual e de como ele aparece pro jogo (Xbox 360 ou DualSense); 'modo jogo' (pausa o mouse/teclado virtuais); cartão anti-travamento do USB.** |
| 168 | o driver de áudio USB (`snd-usb-audio`) sonda o mixer do controle e satura o canal de controle (EP0), o que derruba o USB (`can't add hid device: -71`) num laço | EP0, mixer e código de erro do kernel no meio de uma seção voltada a quem só quer jogar. | **ao reconectar, o Linux tenta configurar o áudio do controle de um jeito que sobrecarrega a conexão USB e derruba o controle, de novo e de novo. (Detalhe técnico: sondagem do mixer `snd-usb-audio` saturando o EP0 — `can't add hid d** |
| 177 | No modo "Jogar pelo Hefesto", use a máscara **Xbox 360** (aba Início, ou por perfil). Com a máscara DualSense, o jogo fala com o controle _físico_ por outro caminho e ignora o controle virtual — a vibração nunca chega. | 'Máscara' é jargão interno dos sprints; nunca é definida para o leitor. | **No modo "Jogar pelo Hefesto", deixe o controle **aparecer pro jogo como Xbox 360** (aba Início, ou por perfil). Se aparecer como DualSense, o jogo acha o controle de verdade por um atalho e ignora o controle do Hefesto — a vibraçã** |
| 185 | Steam → jogo → **Propriedades** → **Opções de inicialização**. Isso faz o jogo enxergar só o gamepad do Hefesto (fim da duplicação), mantendo a vibração. | Falta o caveat que o próprio código tem (daemon_actions.py:162-165): as opções escondem QUALQUER 054c:0ce6 — quebram a máscara DualSense e o modo 'Jogar direto (Sony)'. | **Acrescentar: "Atenção: essas opções valem para o modo 'Jogar pelo Hefesto' com o controle aparecendo como Xbox 360. Se nesse jogo você usar 'Jogar direto (Sony)' ou a aparência DualSense, apague as opções — com elas o jogo deixa d** |
| 191 | o `uinput` do Linux só carrega **botões, eixos e vibração** (force-feedback). Tudo que depende do canal HID cru do DualSense **não trafega pelo controle virtual** | uinput, force-feedback e 'canal HID cru' sem tradução. | **o controle virtual do Linux só transmite **botões, direcionais/gatilhos e vibração**. O que precisa de conversa direta com o DualSense (luzes, resistência dos gatilhos, sensor de movimento, touchpad) **não passa pelo controle virt** |
| 201 | \| Bateria dentro do jogo \| não _(a GUI mostra)_ \| **sim** \| `uinput` não tem `power_supply` (SDL vê "wired") \| | Contradiz a auditoria de paridade (SDL vê UNKNOWN, não 'wired') e usa jargão. | **\| Bateria dentro do jogo \| não _(o painel do Hefesto mostra)_ \| **sim** \| o controle virtual não informa bateria (o jogo vê "desconhecida") \|** |
| 205 | Com a máscara DualSense (prompts PlayStation), o driver HIDAPI do jogo adota o controle _físico_ pelo `/dev/hidraw` e ignora o controle virtual — o rumble nunca chega ao pipeline do Hefesto. | HIDAPI, /dev/hidraw e pipeline em um parágrafo de orientação ao jogador. | **Com a aparência DualSense (botões PlayStation no jogo), o jogo encontra o controle de verdade por um atalho e ignora o controle do Hefesto — a vibração nunca passa por nós. (Detalhe: SDL/HIDAPI via /dev/hidraw.)** |
| 220 | sudo apt install ./hefesto-dualsense4unix_3.8.1_amd64_py3XX.deb | Versão congelada em 3.8.1 (atual 3.13.3); idem AppImage (linhas 252/255) e Flatpak 3.3.0 (linha 267). | **sudo apt install ./hefesto-dualsense4unix_<versão>_amd64_py3XX.deb  # baixe sempre a mais recente em releases/latest (e aplicar o mesmo padrão <versão> nas linhas 252, 255 e 267)** |
| 329 | Todos os 3 aplicam o mesmo conjunto canônico de **5 regras + uinput modules-load** (sincronizados via `assets/`) | O conjunto canônico tem 6 regras (70, 71, 72, 76, 77, 78 — install_udev.sh:28-33); a 78 (sensor de movimento fora da lista de joysticks) nem é mencionada. | **Todos os 3 aplicam o mesmo conjunto canônico de **6 regras (70, 71, 72, 76, 77, 78) + uinput modules-load** (sincronizados via `assets/`)** |
| 438 | a GUI é trazida ao foco pela regra udev `74-ps5-controller-hotplug-bt.rules` (instalada por `./scripts/install_udev.sh`) | Promessa morta: o install_udev.sh:58-59 REMOVE as regras 73/74 (aposentadas por alimentar o storm). | **Após pareado, o daemon detecta o controle automaticamente em até 5 s. (Remover a menção à regra 74 — ela foi aposentada.)** |
| 495 | \| Pop!\_OS 24.04 \| COSMIC alpha \| OK \| OK \| janela compacta\* \| OK (portal + wlrctl) \| Validado 2026-05-15; tray nativo aguarda v3.4 \| | Célula presa em 2026-05: o applet COSMIC nativo existe desde v3.6 e instala por padrão desde v3.13.3; 'portal + wlrctl' não é o mecanismo real (é Xlib/XWayland). | **\| Pop!\_OS 24.04 \| COSMIC \| OK \| OK \| applet COSMIC próprio (padrão) \| OK p/ jogos Steam/Proton (XWayland) \| Máquina principal de validação (2026-07) \|** |
| 646 | *.rules         # udev (70..74) | Árvore desatualizada: as regras vão de 70 a 78 e as 73/74 foram aposentadas. | ***.rules         # udev (70-72, 75-78; 73/74 aposentadas)** |
| 651 | tests/unit/       # 1856 testes pytest | Contradiz o badge (linha 8) e o Estado (linha 23), que dizem 2022. | **tests/unit/       # 2022 testes pytest (manter em sincronia com o badge — ou trocar ambos por 'suite pytest' sem número)** |

## `src/hefesto_dualsense4unix/app/actions/emulation_actions.py` (16)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 103 | — (gamepad virtual desligado) | Ok-ish, mas 'gamepad virtual' difere dos termos da Início. | **— (controle virtual desligado)** |
| 112 | python-uinput não instalado — pip install python-uinput | Mandar leiga rodar pip contradiz a regra do projeto (tudo via install.sh). | **Falta um componente do Hefesto — rode o instalador (install.sh) de novo.** |
| 117 | sem permissão em /dev/uinput — carregue módulo uinput e configure udev rule (ver README) | Jargão de kernel/udev. | **O sistema não deixou criar o controle virtual. Rode o instalador (install.sh) e reinicie o computador.** |
| 133 | start() retornou False — veja logs do daemon | Mensagem de programador. | **Não deu certo criar o controle virtual — veja 'Ver o que aconteceu' na aba Sistema.** |
| 183 | Módulo ok, sem permissão em /dev/uinput | Jargão (também nas variantes 187-189 e 192). | **Quase pronto — falta permissão do sistema (rode install.sh) / 'Falta um componente (rode install.sh)' para as demais variantes** |
| 200 | Nenhum /dev/input/js* detectado | Caminho de kernel na cara do usuário. | **Nenhum controle visível para os jogos agora** |
| 263 | desligado (suprimido) | 'Suprimido' é redundante e técnico. | **desligado** |
| 268 | script do WirePlumber não encontrado | Jargão. | **Não encontrei os arquivos de correção — reinstale o Hefesto (install.sh).** |
| 294 | Mic ligado — ATENÇÃO: sem o quirk de áudio USB ativo isso pode reabrir o storm -71; rode scripts/install_usb_quirk.sh (vale no próximo boot) | 'Quirk', 'storm -71' e caminho de script são jargão puro num aviso importante. | **Microfone ligado — ATENÇÃO: sem a correção de USB instalada o controle pode começar a desconectar. Rode o instalador (install.sh) e reinicie o computador.** |
| 365 | desligado — emulação normal | 'Emulação' é jargão. | **desligado — o controle mexe no mouse/teclado normalmente** |
| 372 | daemon offline | Jargão (idem linha 394 'daemon offline — gamepad não alterado'). | **Hefesto desligado — ligue na aba Início ou Sistema** |
| 400 | Gamepad virtual desligado | Ok, mas não diz o que acontece agora. | **Controle virtual desligado — o controle volta a controlar o PC** |
| 403 | Gamepad DualSense ligado (prompts PS) | 'Prompts' é anglicismo. | **Controle virtual DualSense ligado (botões PlayStation, sem vibração nos jogos)** |
| 406 | Gamepad Xbox 360 ligado (fallback) | '(fallback)' CONTRADIZ o resto da UI, que diz que Xbox 360 é a opção recomendada. | **Controle virtual Xbox 360 ligado (recomendado)** |
| 434 | Modo jogo: mouse/teclado suspensos (gamepad ativo) | '(gamepad ativo)' é falso quando o vpad está desligado. | **Modo jogo ligado: o controle não mexe mais no mouse/teclado (condicionar o sufixo ao estado real do gamepad)** |
| 488 | ligado (conflita!) | 'Conflita' com o quê? | **ligado — atrapalha o Hefesto (clique em 'Desligar Steam Input')** |

## `src/hefesto_dualsense4unix/app/actions/profiles_actions.py` (14)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 53 | ("any", "Qualquer") | 'Qualquer' solto não diz qualquer O QUÊ | **("any", "Sempre")** |
| 66 | ("none", "Sem opinião") | 'Sem opinião' é antropomórfico e confuso para leigos | **("none", "Não mudar")** |
| 66 | Sem opinião | Expressão ambígua para 'este perfil não muda o modo'. | **Não mudar o modo** |
| 74 | ("dualsense", "DualSense (PS)") | Opção oferecida sem aviso de que a vibração in-game NÃO funciona com essa máscara (queixa nº 3) | **("dualsense", "PlayStation — vibração pode falhar em jogos")** |
| 126 | (0, "Nome"), (1, "Prio"), (2, "Match") | 'Prio' abreviação críptica; 'Match' é inglês/jargão | **"Nome", "Prioridade", "Quando usar"** |
| 207 | O que ativar este perfil liga: controlar o PC, jogar pelo Hefesto ou jogar direto (Sony) | Frase de difícil leitura ('O que ativar este perfil liga') | **Escolha o que acontece quando este perfil entra em ação** |
| 220 | Co-op local (cada controle = um jogador) | 'Co-op' é jargão E o checkbox nasce desmarcado — ninguém quer 2 controles no MESMO jogador (queixa nº 2); desmarcado ele DESLIGA o co-op global ao ativar | **"Cada controle é um jogador" marcado por padrão — ou remover o checkbox e herdar o comportamento global (ver bug HIGH)** |
| 225 | Máscara: | 'Máscara' é jargão interno (queixa nº 1) | **O jogo vê o controle como:** |
| 229 | Como o gamepad virtual aparece para o jogo | 'Gamepad virtual' jargão; não orienta a escolha | **Como o controle aparece para o jogo. Xbox 360 funciona com mais jogos (a vibração funciona).** |
| 237 | Sem opinião = ativar este perfil não mexe no modo do sistema. | Repete o jargão e 'modo do sistema' é vago | **Não mudar = este perfil respeita o modo escolhido na aba Início.** |
| 489 | Editor preenchido com cópia completa; ajuste o nome e Salvar | Telegráfico ('e Salvar') | **Cópia criada no editor: mude o nome e clique em Salvar** |
| 541 | Falha (daemon offline?) | Jargão + interrogação vaga, sem ação | **Não foi possível ativar: o serviço não está rodando (aba Daemon → Iniciar)** |
| 551 | f"Inválido: {exc}" | Vaza mensagem crua do pydantic em inglês no toast | **f"Não foi possível salvar — confira os campos: {exc}" (e traduzir os erros mais comuns)** |
| 689 | store.append([profile.name, profile.priority, profile.match.type, weight]) (exibe 'criteria'/'any') | Valor interno em inglês vaza cru na coluna da lista | **Mapear: 'any' → 'Sempre', 'criteria' → 'Regra própria'** |

## `src/hefesto_dualsense4unix/app/actions/rumble_actions.py` (14)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 46 | "Modo Auto: ajusta intensidade conforme a bateria do controle.\nBateria >50%: 100% (Máximo). 20-50%: 70% (Balanceado). <20%: 30% (Economia).\nTransições com debounce de 5 segundos para evitar oscilação." | 'debounce' é jargão de engenharia. Pior: diz 'a bateria DO CONTROLE' (singular) quando na verdade usa só a bateria do controle primário e aplica em todos (BUG-5) — com 4 controles a frase é falsa. | **"Automático: quanto menos bateria, mais fraca a vibração — para o controle durar mais.\nAcima de 50%: força total. Entre 20% e 50%: 70%. Abaixo de 20%: 30%.\nA mudança leva 5 segundos para não ficar oscilando." (+ com 2 ou mais co** |
| 92 | "Política exibida = estado atual do daemon; o perfil não tem opinião (escolha uma política para salvá-la no perfil)." | String mais hermética da aba: 'daemon', 'o perfil não tem opinião', sinal de igual como conectivo. Perfil não tem 'opinião' — ninguém entende isso. | **"Mostrando a força de vibração que está valendo agora. Este perfil ainda não guardou uma escolha — clique numa opção para gravá-la no perfil."** |
| 204 | f"Política de rumble: {policy}" | Mostra a CHAVE INTERNA na barra de status: 'Política de rumble: max' / ': economia' — em inglês/abreviado, diferente do botão que ela acabou de clicar ('Máximo'). | **Mapear para o label do botão: f"Força da vibração: {LABEL[policy]}" — ex.: "Força da vibração: Máximo"** |
| 293 | f"Rumble FIXO em weak={weak}, strong={strong} — enquanto fixo o jogo NÃO controla a vibração; clique 'Devolver ao jogo' para jogar" | 'Rumble', 'weak=', 'strong=' — sintaxe de código na barra de status. E cita um botão "Devolver ao jogo" que não existe: o botão real é "Devolver rumble ao jogo" (main.glade:1103). | **f"Vibrando sem parar (leve {weak}, pesada {strong}). Enquanto estiver assim, o jogo não controla a vibração — clique em 'Deixar o jogo vibrar' para jogar."** |
| 309 | "Falha (daemon offline?)" | Aparece em 4 lugares da aba (linhas 296, 309, 343 e via _toast_rumble): 'daemon' é jargão e o '?' transfere ao usuário um diagnóstico que a GUI já tem. | **"O Hefesto não está rodando — ligue na aba Daemon (botão Iniciar)."** |
| 311 | Testando por 500 ms (weak={weak}, strong={strong}) | Unidade e nomes de motor em inglês num toast. | **Testando por meio segundo (leve={weak}, pesado={strong})** |
| 311 | f"Testando por 500 ms (weak={weak}, strong={strong})" | 'weak='/'strong=' em sintaxe de código. | **f"Testando meio segundo (leve {weak}, pesada {strong})"** |
| 325 | "Rumble parado (fixo em silêncio) — 'Devolver ao jogo' para o jogo voltar a controlar a vibração" | 'Rumble' em inglês + nome de botão errado ('Devolver ao jogo' vs o real 'Devolver rumble ao jogo'). | **"Vibração travada em silêncio. Clique em 'Deixar o jogo vibrar' para o jogo voltar a comandar."** |
| 428 | self._toast_rumble("Teste encerrado — vibração devolvida ao jogo") | Nenhum — é exemplo de texto BOM (ação + consequência, sem jargão). Citado só para que a reescrita dos vizinhos siga este mesmo registro. | **MANTER como está. Usar como referência de tom para os itens acima.** |
| 446 | '<span foreground="#2d8">o JOGO controla a vibração</span>' | Pinta VERDE (=tudo certo) mesmo quando a máscara é DualSense, na qual o jogo comprovadamente nunca vibra (ver CONFLITO-1). Verde afirma um sucesso que pode não existir. | **Verde só quando flavor=='xbox': "a vibração está liberada para o jogo". Com flavor=='dualsense', laranja: "liberada para o jogo, mas a máscara DualSense impede a vibração — troque para Xbox 360 na aba Emulação".** |
| 450 | '<span foreground="#e0a020">FIXA em silêncio (clique "Devolver ao jogo")</span>' | 'FIXA em silêncio' é tradução literal de rumble_active=(0,0). A usuária lê e não entende que o jogo inteiro está sem vibração por causa disso. | **'<span foreground="#e0a020">desligada à força — nenhum controle vibra no jogo (clique "Devolver ao jogo")</span>'** |
| 452 | '<span foreground="#e0a020">FIXA em silêncio (clique "Devolver ao jogo")</span>' | Cita botão inexistente ('Devolver ao jogo'); o real é 'Devolver rumble ao jogo'. | **"travada em silêncio — clique em 'Deixar o jogo vibrar'"** |
| 455 | f'FIXA em weak={active[0]}, strong={active[1]} (clique "Devolver ao jogo" para jogar)' | 'weak='/'strong=' em sintaxe de código + nome de botão errado. | **f"travada (leve {active[0]}, pesada {active[1]}) — clique em 'Deixar o jogo vibrar' para jogar"** |
| 455 | f'<span foreground="#e0a020">FIXA em weak={active[0]}, strong={active[1]} (clique "Devolver ao jogo" para jogar)</span>' | Mesmo problema: 'FIXA', 'weak', 'strong' expostos crus. | **f'<span foreground="#e0a020">travada no teste (motor leve {active[0]}, motor forte {active[1]}) — clique "Devolver ao jogo" para jogar</span>'** |

## `src/hefesto_dualsense4unix/app/actions/daemon_actions.py` (13)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 118 | Reaplicando fixes seguros (sem sudo)... | 'Fixes' e 'sudo'. | **Aplicando correções (não pede senha)…** |
| 153 | Fixes reaplicados. Se a Steam estava aberta, feche-a e clique de novo para desligar o Steam Input. | 'Fixes' anglicismo. | **Correções aplicadas. Se a Steam estava aberta, feche-a e clique de novo para desligar o Steam Input.** |
| 204 |  (dica: troque a máscara para Xbox 360 na aba Início p/ vibração sem duplicar) | 'Máscara' é jargão interno. | ** (dica: na aba Início, escolha "Xbox 360 (vibra)" para ter vibração sem controle duplicado)** |
| 231 |  Consultando... | Ok, mas o tooltip (233) cita systemctl. | ** Verificando… (tooltip: "Verificando se o Hefesto está rodando. Aguarde.")** |
| 471 | serviço hefesto-dualsense4unix.service não instalado — rode install.sh | Meio técnico; ok como tooltip mas pode ser mais claro. | **O Hefesto ainda não foi instalado como serviço. Rode o instalador (install.sh) uma vez.** |
| 549 | systemctl não encontrado — sistema sem systemd --user. | Jargão em diálogo de erro. | **Este sistema não tem o gerenciador de serviços esperado (systemd). Rode o instalador (install.sh) ou inicie o Hefesto manualmente.** |
| 570 | systemctl --user restart hefesto-dualsense4unix.service → ok | Comando cru como confirmação. | **Hefesto reiniciado.** |
| 592 | Não foi possível reiniciar o daemon | Jargão 'daemon' no título do diálogo. | **Não foi possível reiniciar o Hefesto** |
| 781 | systemctl {action} {unit} → rc={rc} | Toast dos botões Ligar/Desligar/auto-start é comando cru + código de retorno; leiga não distingue sucesso (rc=0) de falha (rc=1). | **Sucesso: "Pronto — Hefesto ligado." / "Hefesto desligado." / "Vai ligar sozinho com o computador."; falha: "Não consegui — veja 'Detalhes técnicos' abaixo."** |
| 802 |  Online (systemd + auto-start) | Jargão systemd/auto-start no status principal. | ** Funcionando (liga sozinho com o computador)** |
| 810 |  Online (processo avulso, sem systemd) | 'Processo avulso' e 'systemd' não dizem nada a leigos. | ** Funcionando (modo improvisado — clique em 'Corrigir modo de execução')** |
| 818 | systemd reporta unit ativa mas o processo ainda não escreveu o pid file. Aguarde alguns segundos. | Tooltip com jargão (unit, pid file). | **O Hefesto está terminando de ligar. Aguarde alguns segundos e clique em Atualizar.** |
| 822 |  Offline | Anglicismo; e o tooltip (824-827) manda usar linha de comando. | ** Desligado (tooltip: "O Hefesto não está rodando. Clique em 'Ligar o Hefesto'.")** |

## `src/hefesto_dualsense4unix/integrations/desktop_notifications.py` (13)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 244 | tr_label = {"usb": "USB", "bt": "Bluetooth"}.get(transport.lower(), transport) | 'USB' é sigla técnica; para leigo o conceito é 'cabo'. E o fallback devolve o valor CRU do transporte se não for usb/bt (string interna vazando para a tela). | **{"usb": "cabo", "bt": "Bluetooth"} com fallback "cabo" — texto final "Controle conectado por cabo." / "...por Bluetooth."** |
| 247 | DualSense detectado via {tr_label}. | Com 2..4 controles não diz QUAL controle conectou (nem número de jogador nem posição). A mantenedora tem 2 controles agora e a meta é 4 — 'DualSense detectado via USB' é inútil para saber quem entrou. Chamado em lifecycle.py:382 e | **"Controle {n} conectado por {cabo\|Bluetooth}. Agora são {total} controles." — ex.: "Controle 2 conectado por Bluetooth. Agora são 2 controles." (o total já está em describe_controllers(); o índice do jogador, em CoopManager.playe** |
| 260 | body = "DualSense desconectado." if not reason else f"DualSense desconectado ({reason})." | O ramo com `reason` só existe para imprimir jargão interno entre parênteses (ver linhas acima). Nenhum valor de `reason` no código é texto para humano. | **body = "Controle desconectado. Se foi sem querer, reconecte o cabo ou aperte o botão PS." (sem interpolar `reason`; manter `reason` só no log)** |
| 279 | summary="Bateria baixa do DualSense" | 'DualSense' é o nome comercial Sony; o resto da UI chama de 'controle'. Inconsistência de vocabulário. | **"Bateria fraca no controle {n}"** |
| 280 | Bateria em {pct}%. Conecte via USB para carregar. | Com 2..4 controles não diz QUAL controle está fraco (a pessoa olha para os 4). 'via USB' = jargão para 'com o cabo'. | **"Controle {n} com {pct}% de bateria. Ligue o cabo nele para carregar."** |
| 301 | Hefesto trocou para o perfil: {name}. | Aceitável, mas 'perfil' sozinho não diz o efeito; e a frase é impessoal. | **"Ajustes de '{name}' aplicados ao controle."** |
| 318 | Rode 'hefesto-dualsense4unix doctor' ou corrija/exclua o arquivo. | Manda o leigo abrir terminal e digitar comando — contraria a meta 'tudo via interface'. Disparado por lifecycle.py:1400-1405 (_audit_config_on_boot). 'perfil(is) ignorado(s)' com plural em parênteses também é feio de ler. | **Summary: "Alguns perfis estão com problema" → body: "{n} perfil(s) não pôde ser carregado: {nomes}. Abra o Hefesto na aba Perfis para corrigir ou excluir." + botão de ação ("open", "Abrir Hefesto") como já existe em notify_control** |
| 333 | summary="Hefesto: reparo recomendado" | 'reparo' sem dizer do quê assusta e não informa. Disparado por lifecycle.py:1436-1441 (_check_system_on_boot). | **"O Hefesto precisa de um ajuste no sistema" + body curto e botão "Abrir Hefesto"** |
| 334 | Hefesto: reparo recomendado | "reparo" sem sujeito: reparo em quê? No controle? No PC? Assusta sem informar. | **Hefesto: encontrei algo para ajustar no sistema** |
| 351 | Modo jogo ligado | "Modo jogo" colide com os 3 modos da aba Início ("Controlar o PC" / "Jogar pelo Hefesto" / "Jogar direto (Sony)"). A usuária lê "Modo jogo ligado" e acha que trocou de modo na Início — mas isso só suspende mouse/teclado. | **Mouse e teclado do controle: desligados** |
| 352 | Emulação de mouse/teclado desativada. Segure o PS de novo para reativar. | FACTUALMENTE ERRADO no default + jargão. `ps_long_press_ms` default = 0 (lifecycle.py:121, hotkey_daemon.py:48) e o gesto só roda se `> 0` (hotkey_daemon.py:174). Segurar o PS NÃO reativa nada — abre a Steam (ps_button_action='ste | **Summary: "Modo jogo ligado" → body: "O controle agora vai só para o jogo — não mexe mais no cursor nem digita. Aperte PS + Options juntos para voltar."** |
| 354 | Modo jogo desligado | Mesma colisão com os modos da aba Início. Além disso "desligado" soa como se algo tivesse parado de funcionar, quando na verdade o mouse/teclado VOLTARAM. | **Mouse e teclado do controle: ligados** |
| 355 | Emulação de mouse/teclado reativada. | Jargão ('emulação'). Não diz o que a pessoa ganha de volta. | **Summary: "Modo jogo desligado" → body: "O controle voltou a mexer o cursor e digitar no computador."** |

## `src/hefesto_dualsense4unix/app/actions/status_actions.py` (11)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 266 | Controle alvo das ações (lightbar, gatilhos, LEDs, rumble). 'Todos' aplica a todos os controles. | Jargão (lightbar, rumble, LEDs) na única explicação do seletor | **Escolha qual controle recebe os ajustes (cor da luz, gatilhos, vibração). 'Todos' aplica em todos de uma vez.** |
| 477 | Desconectado — abra a aba Daemon e clique em Iniciar | 'Desconectado' ambíguo (controle? serviço?); bom que é acionável | **O serviço não está rodando — abra a aba Daemon e clique em Iniciar** |
| 480 | Offline (sem resposta do daemon) | Jargão duplo | **Parado (sem resposta)** |
| 571 | f"...{len(conectados)} controles: {partes}" (ex.: '2 controles: USB + BT') | 'BT' críptico; negrito do primário não é explicado | **'2 controles: USB + Bluetooth' (e tooltip: 'em negrito, o controle principal')** |
| 581 | Conectado Via USB | 'Via' capitalizado no meio da frase | **Conectado via cabo (USB) / Conectado via Bluetooth** |
| 587 | Online | Par Online/Offline é jargão; 'Offline' sugere internet | **Rodando** |
| 598 | Tentando Reconectar... | Capitalização de título no meio de frase | **Tentando reconectar…** |
| 606 | Daemon Offline | Dois jargões juntos no header mais visível da janela | **Serviço parado** |
| 608 | Offline | Idem: leigo lê 'sem internet' | **Parado** |
| 789 | transport.upper() (exibe 'BT' / 'USB') | Sigla 'BT' é críptica para leigos | **Mapear para texto: USB → 'Cabo (USB)', BT → 'Sem fio (Bluetooth)'** |
| 807 | suffix = " (Controle 1)" | Diz de quem é a bateria, mas nada avisa que os sticks/botões/gatilhos acima TAMBÉM são só do Controle 1 | **" (Controle 1 — principal)" + um rótulo no frame: 'Mostrando o Controle 1'** |

## `src/hefesto_dualsense4unix/app/actions/input_actions.py` (8)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 37 | <b>Formato de tecla:</b> KEY_* (ex: KEY_C, KEY_ENTER) ou __OPEN_OSK__ / __CLOSE_OSK__ para teclado virtual.\n<b>Combos:</b> separar por '+' (ex: KEY_LEFTALT+KEY_TAB).\n<b>Default:</b> Options=Super, Share=PrintScreen, L1=Alt+Shift | KEY_*, tokens __*__, "OSK", "Default" e "Super" são jargão; diz "Share" mas a tabela abaixo mostra o botão como "create" (inconsistente). | **<b>Como escrever a tecla:</b> KEY_ + o nome (ex.: KEY_C, KEY_ENTER). Para combinações, use + (ex.: KEY_LEFTALT+KEY_TAB). __OPEN_OSK__ / __CLOSE_OSK__ abrem/fecham o teclado na tela.\n<b>Padrão de fábrica:</b> Options abre o menu d** |
| 38 | <b>Formato de tecla:</b> KEY_* (ex: KEY_C, KEY_ENTER) ou __OPEN_OSK__ / __CLOSE_OSK__ para teclado virtual. | "KEY_*", "__OPEN_OSK__", "OSK", "teclado virtual" — quatro jargões numa linha só. Uma leiga não tem como adivinhar que precisa escrever o prefixo KEY_ nem o que é OSK. | **<b>Como escrever a tecla:</b> KEY_ + o nome da tecla (ex.: KEY_C para a letra C, KEY_ENTER para o Enter).\n<b>Teclado na tela:</b> escreva __OPEN_OSK__ para abrir e __CLOSE_OSK__ para fechar.** |
| 40 | <b>Combos:</b> separar por '+' (ex: KEY_LEFTALT+KEY_TAB). | "Combos" é jargão de fighting game; aqui significa "duas teclas ao mesmo tempo". | **<b>Duas teclas juntas:</b> separe com '+' (ex.: KEY_LEFTALT+KEY_TAB faz Alt+Tab).** |
| 41 | <b>Default:</b> Options=Super, Share=PrintScreen, L1=Alt+Shift+Tab, R1=Alt+Tab, L3=abrir OSK, R3=fechar OSK. | "Default" (inglês), "Super" (nome da tecla que ninguém reconhece — é a tecla Windows) e "OSK" duas vezes. | **<b>Já vem pronto assim:</b> Options = tecla Windows, Share = PrintScreen, L1 = Alt+Shift+Tab, R1 = Alt+Tab, L3 = abre o teclado na tela, R3 = fecha o teclado na tela.** |
| 130 | store.append([button, format_binding(binding)]) — células mostram tokens crus: "cross", "dpad_up", "touchpad_left_press", "create"... | A coluna "Botão" exibe identificadores internos em inglês para uma usuária leiga. | **Traduzir para exibição (mantendo o token internamente): cross→"Cruz (X)", circle→"Círculo", triangle→"Triângulo", square→"Quadrado", dpad_up→"Direcional ↑", l1→"L1", options→"Options", create→"Create (Share)", ps→"Botão PS", touch** |
| 159 | Todos os botões já têm binding — edite os existentes. | "binding" é jargão. | **Todos os botões já têm tecla — edite os que estão na lista.** |
| 182 | Bindings do teclado restaurados para o default. | Jargão duplo e mente sobre o estado (só vale após Aplicar). | **Teclas de fábrica restauradas — clique em Aplicar para valer no controle.** |
| 200 | Binding inválido: {exc} | "Binding" é jargão; {exc} vaza mensagem técnica em inglês. | **Tecla inválida — escreva como KEY_C ou KEY_LEFTALT+KEY_TAB.** |

## `src/hefesto_dualsense4unix/app/actions/mouse_actions.py` (7)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 38 | <b>Modo jogo:</b> segure o botão PS para suspender a emulação de mouse/teclado (e segure de novo para retomar). | Mesmo gesto morto da notificação (long-press desligado por default). É a legenda FIXA da aba Mouse — a usuária lê isso toda vez que abre a aba e o gesto nunca funciona. | **<b>Para o controle parar de mexer no PC:</b> aperte PS + Options ao mesmo tempo. Aperte PS + Options de novo para voltar.** |
| 175 | Mouse emulado {ligado\|desligado} | "Mouse emulado" é jargão; e ao ligar durante o modo de jogo o toast omite que o jogo perdeu o controle. | **"O controle agora move o mouse" / "O controle parou de mover o mouse" (e, se o gamepad estava ligado: "O controle agora move o mouse — saiu do modo de jogo")** |
| 181 | Falha ao comunicar com o daemon. Mouse não alterado. | "daemon" é jargão. | **Não consegui falar com o serviço do Hefesto — nada mudou. Veja a aba Daemon.** |
| 319 | uinput disponível | "uinput" é jargão de kernel; a informação útil é "vai funcionar". | **Tudo pronto — pode ligar** |
| 323 | sem permissão em /dev/uinput — rode ./scripts/install_udev.sh | Caminho de device + script manual contradizem o princípio "tudo via instalador"; leiga não abre terminal. | **Falta uma permissão do sistema — rode o instalador de novo (./install.sh) para corrigir** |
| 327 | módulo ok, /dev/uinput ausente (modprobe uinput) | "módulo", "/dev/uinput" e "modprobe" são jargão puro. | **Falta um componente do sistema — rode o instalador de novo (./install.sh)** |
| 332 | python-uinput não instalado (pip install python-uinput) | Nome de pacote Python + comando pip na cara da usuária. | **Falta um componente do Hefesto — rode o instalador de novo (./install.sh)** |

## `src/hefesto_dualsense4unix/profiles/trigger_presets.py` (7)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 58 | "plateau_central": "Plateau central" | 'Plateau' é estrangeirismo técnico (gráfico), não descreve a sensação. | **"Mais firme no meio"** |
| 59 | "stop_hard": "Stop hard" | Rótulo 100% em inglês num seletor PT-BR. | **"Trava seca no fim"** |
| 60 | "stop_macio": "Stop macio" | Portunhol técnico: metade inglês ('Stop'), metade português. | **"Trava suave no fim"** |
| 61 | "linear_medio": "Linear médio" | 'Linear' é jargão de gráfico; não diz que o peso é o mesmo do começo ao fim. | **"Peso igual no curso todo"** |
| 68 | "machine_gun": "Machine gun" | Rótulo em inglês, sendo que a aba já tem 'Metralhadora' em PT-BR no modo Machine (trigger_specs.py:135) — duas palavras diferentes para a mesma coisa. | **"Metralhadora"** |
| 70 | "senoide": "Senoide" | Termo de matemática/engenharia; ninguém escolhe um gatilho por 'senoide'. | **"Onda suave (sobe e desce)"** |
| 71 | "vibracao_final": "Vibracao final" | ERRO DE ACENTUAÇÃO visível na GUI: 'Vibracao' sem cedilha/til. Único label da área com acento faltando. | **"Vibração só no fim"** |

## `src/hefesto_dualsense4unix/tui/app.py` (6)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 89 | daemon offline — mostrando perfis do XDG | 'daemon' + 'XDG' são jargões | **Hefesto desligado — mostrando os perfis salvos no computador** |
| 89 | "[yellow]daemon offline[/] — mostrando perfis do XDG" | Jargão 'daemon' e 'XDG' | **"Hefesto desligado — mostrando os perfis salvos no disco"** |
| 122 | Hefesto - Dualsense4Unix v… — daemon de gatilhos adaptativos para DualSense | 'daemon' no título da TUI | **Hefesto - Dualsense4Unix v… — seu DualSense no Linux** |
| 123 | "— daemon de gatilhos adaptativos para DualSense" | Branding desatualizado (só gatilhos) + jargão 'daemon' | **"— seu DualSense completo no Linux"** |
| 238 | não foi possivel ativar '{name}' (daemon offline?) | 'possivel' sem acento; 'daemon offline' | **não foi possível ativar '{name}' (o Hefesto está desligado?)** |
| 238 | f"não foi possivel ativar '{name}' (daemon offline?)" | Acento faltando ('possivel') + jargão 'daemon offline' | **f"não foi possível ativar '{name}' (o Hefesto está desligado?)"** |

## `src/hefesto_dualsense4unix/app/actions/footer_actions.py` (6)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 104 | Aplicando perfil inteiro... | "perfil inteiro" é linguagem interna do código; a usuária clicou para aplicar o que vê. | **Aplicando as configurações no controle...** |
| 119 | ERRO ao aplicar perfil (daemon offline?). | "daemon offline" é jargão. | **Não deu para aplicar — o serviço do Hefesto parece desligado. Ligue-o na aba Daemon.** |
| 187 | Perfil salvo em {caminho} | Mostra caminho de arquivo cru na statusbar. | **Perfil '{nome}' salvo.** |
| 291 | Perfil importado: {nome} -> {caminho} | Caminho cru e seta ASCII. | **Perfil '{nome}' importado com sucesso.** |
| 325 | Asset 'meu_perfil.json' não encontrado — Restaurar Default indisponível. | "Asset" e nome de arquivo interno são jargão. | **O arquivo de fábrica do perfil não foi encontrado — reinstale o Hefesto para restaurar.** |
| 363 | meu_perfil restaurado para {destino} | Nome interno em snake_case + caminho cru. | **'Meu Perfil' voltou ao padrão de fábrica.** |

## `src/hefesto_dualsense4unix/cli/cmd_gamepad.py` (5)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 25 | Gamepad virtual (DualSense/Xbox) pelo daemon — máscara p/ os jogos. | 'gamepad virtual', 'daemon' e 'máscara' na mesma linha | **Controle para jogos: o jogo vê um Xbox 360 (vibra) ou um DualSense.** |
| 25 | help="Gamepad virtual (DualSense/Xbox) pelo daemon — máscara p/ os jogos." | Jargão 'gamepad virtual', 'daemon', 'máscara' concentrados | **"Modo 'Jogar pelo Hefesto': cria o controle que o jogo enxerga (Xbox 360 ou DualSense)."** |
| 41 | f"[red]daemon offline[/red] (socket IPC inacessível): {exc}" | Jargão 'socket IPC' (repetido em cmd_coop.py:43, cmd_native.py:38, cmd_mouse.py:46, cmd_controller.py:43) | **"o Hefesto não está rodando — inicie com 'hefesto-dualsense4unix daemon start' (detalhe: {exc})"** |
| 51 | Máscara do controle: dualsense (prompts PS) \| xbox (XInput-only). | não avisa que dualsense fica sem vibração nos jogos; 'XInput-only' é jargão; e o default deveria ser xbox | **Como o jogo vê o controle: xbox = vibração funciona (recomendado) \| dualsense = botões PS, sem vibração nos jogos. (E trocar o default para 'xbox'.)** |
| 51 | help="Máscara do controle: dualsense (prompts PS) \| xbox (XInput-only)." | Orientação ERRADA para o fato provado: xbox é o que faz a vibração funcionar (e é o default do daemon); 'prompts PS'/'XInput-only' é jargão | **"Como o jogo vê o controle: xbox (padrão; vibração funciona) \| dualsense (botões PlayStation; a vibração falha em muitos jogos)" — e mudar o default para omitir o campo (manter a máscara atual)** |

## `src/hefesto_dualsense4unix/app/compact_window.py` (4)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 200 | Sair | o botão desliga GUI + daemon (o controle para de funcionar), mas 'Sair' sugere só fechar o widget | **Desligar Hefesto** |
| 200 | Gtk.Button.new_with_label(_("Sair")) | 'Sair' encerra GUI E daemon (on_quit=quit_app) — parece só fechar o widget | **"Desligar" (ou "Sair e desligar")** |
| 275 | Daemon offline | jargão | **Hefesto desligado** |
| 275 | "Daemon offline" | Jargão 'daemon' | **"Hefesto desligado"** |

## `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py` (4)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 114 | f"Cor RGB {self._current_rgb} a {pct}% aplicada" | Mostra a TUPLA PYTHON crua na barra de status: 'Cor RGB (255, 128, 0) a 100% aplicada'. 'RGB' + sintaxe de tupla. | **f"Luz acesa a {pct}% de brilho" (a cor já está visível na prévia e no botão de cor)** |
| 167 | "Lightbar apagada" | 'Lightbar' em inglês. | **"Luz do controle apagada"** |
| 209 | label = " ".join("x" if b else "-" for b in bits) → f"Player LEDs aplicados: {label}" | Saída críptica: 'Player LEDs aplicados: - - x - -'. 'Player LEDs' em inglês + notação x/- que ninguém decifra. | **Nomear o padrão quando bater com um preset: "Luzinhas: Jogador 1"; senão "Luzinhas: 3ª acesa" (listar as posições acesas por extenso).** |
| 237 | f"Player LEDs: {label}" if ok else f"Player LEDs: {label} (daemon offline?)" | Mesma notação x/- + 'daemon offline?' como pergunta ao usuário — a GUI deveria SABER se o daemon está no ar (ela já consulta daemon.state_full a 10 Hz). | **"Luzinhas atualizadas" / "O Hefesto não está rodando — ligue na aba Daemon."** |

## `src/hefesto_dualsense4unix/cli/app.py` (3)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 21 | Daemon de gatilhos adaptativos para DualSense no Linux. | 'Daemon' e 'gatilhos adaptativos' juntos afastam leigos logo no --help | **Hefesto: seu controle DualSense no Linux (gatilhos, vibração, luzes e perfis).** |
| 21 | help="Daemon de gatilhos adaptativos para DualSense no Linux." | Escopo desatualizado (hoje: modos, multi-controle, vibração, perfis) + jargão 'daemon' na 1ª linha do --help | **"Hefesto: controle DualSense completo no Linux — modos de uso, vibração, gatilhos, perfis e vários controles."** |
| 49 | Controle do daemon de background. | jargão duplo (daemon, background) | **Liga/desliga o serviço do Hefesto (roda sozinho em segundo plano).** |

## `src/hefesto_dualsense4unix/integrations/tray.py` (3)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 99 | Hefesto - Dualsense4Unix: carregando... | reticências ASCII e dois-pontos; padrão das outras superfícies é '(carregando...)' | **Hefesto - Dualsense4Unix (carregando…)** |
| 110 | Abrir TUI | 'TUI' é sigla de desenvolvedor | **Abrir no terminal** |
| 165 | Perfil: {name} | prefixo redundante (itens já estão sob o menu) e sem marcador do perfil ativo — AppTray e applet usam '> ' | **'> {name}' para o ativo e '{name}' para os demais (igual às outras superfícies)** |

## `src/hefesto_dualsense4unix/app/tray.py` (3)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 181 | Sair do Hefesto - Dualsense4Unix | não deixa claro que o daemon também é desligado (o controle para); applet usa 'Sair (desligar Hefesto)' | **Sair (desligar Hefesto)** |
| 181 | "Sair do Hefesto - Dualsense4Unix" | Não avisa que também DESLIGA o daemon (quit_app em app.py:380 encerra GUI+daemon) — o controle para de funcionar | **"Sair e desligar o Hefesto" (paridade com o applet: "Sair (desligar Hefesto)")** |
| 273 | "Tray icon indisponivel no COSMIC. Habilite o applet 'Area de status' no cosmic-panel (Configurações > Painel) ou use a janela principal. Este aviso só aparece uma vez." | Sem acentos ('indisponivel', 'Area'), jargão 'Tray icon'/'cosmic-panel', mistura inglês | **"Ícone da bandeja indisponível no COSMIC. Habilite o miniaplicativo 'Área de status' em Configurações > Painel, ou use a janela principal. Este aviso aparece só uma vez."** |

## `src/hefesto_dualsense4unix/cli/ipc_client.py` (3)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 27 | super().__init__(f"[{code}] {message}") | Este __str__ é o que vaza nos toasts da GUI (home_actions.py:403,466) — é a origem do "[-32003]" na tela. O código JSON-RPC não significa nada para a usuária. | **Manter o formato técnico em `repr`/log, e expor `.message` limpo para a UI; a GUI deve formatar por `.code` (-1 = "não respondeu") em vez de interpolar a exceção inteira.** |
| 66 | raise IpcError(-1, "conexão timeout") | "conexão timeout" é meio inglês, meio português, e chega na tela via toast como "([-1] conexão timeout)". | **"o Hefesto não respondeu a tempo".** |
| 116 | raise IpcError(-1, "conexão fechada pelo servidor antes da resposta") | "servidor" não existe no vocabulário do produto (não há servidor; há o daemon local). | **"o Hefesto fechou a conexão antes de responder".** |

## `src/hefesto_dualsense4unix/core/backend_pydualsense.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 552 | input pode ficar zerado se kernel hid_playstation capturar evdev | Hint de log com jargão de kernel ('hid_playstation', 'evdev') — inútil para leigo se aparecer no doctor. | **Não encontrei o canal de leitura do controle: os botões podem não responder. Desconecte e reconecte o controle; se continuar, reinicie o computador.** |
| 1053 | pydualsense não inicializado — chamar connect() antes | Jargão de biblioteca ('pydualsense', 'connect()') numa mensagem de erro que, se um dia for propagada por IPC/CLI, chega crua ao usuário. (Hoje o método é código morto — se mantido, o texto deve ser leigo.) | **Nenhum controle conectado. Conecte o controle pelo cabo USB ou por Bluetooth e tente de novo.** |

## `src/hefesto_dualsense4unix/core/evdev_reader.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 460 | outro leitor exclusivo? físico ficaria DOBRADO no jogo | Hint de log que o doctor/suporte mostra à usuária: 'leitor exclusivo' e 'físico DOBRADO' são jargão; não diz o que fazer. | **Não consegui reservar o controle só para o Hefesto — outro programa pode estar usando ele. O jogo pode enxergar o controle duas vezes. Feche outros programas de controle (ex.: Steam aberto em Big Picture) e tente de novo.** |
| 503 | grab falhou ao reabrir o device; o controle pode dobrar input | 'grab', 'device' e 'dobrar input' são jargão em mensagem que aparece em diagnóstico. | **Não consegui reservar o controle ao reconectar. O jogo pode enxergar o controle duas vezes. Desconecte e reconecte o controle.** |

## `src/hefesto_dualsense4unix/cli/cmd_native.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 23 | Modo Nativo — solta o controle para o jogo (gatilhos nativos da Sony). | GUI chama esse modo de 'Jogar direto (Sony)' — nomes diferentes para a mesma coisa | **Jogar direto (Sony) — o jogo fala direto com o controle, com os gatilhos da Sony.** |
| 23 | help="Modo Nativo — solta o controle para o jogo (gatilhos nativos da Sony)." | Nome diverge da GUI/applet ('Jogar direto (Sony)') — mesma feature com dois nomes | **"Jogar direto (Sony) — o jogo fala com o controle sem o Hefesto no meio (o mesmo modo da aba Início)."** |

## `src/hefesto_dualsense4unix/cli/cmd_status.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 42 | connected / transport / active_profile / battery_pct (rótulos da tabela) | chaves internas em inglês exibidas cruas numa tabela em português | **Conectado / Conexão (USB ou Bluetooth) / Perfil ativo / Bateria (%)** |
| 42 | for key in ("connected", "transport", "active_profile", "battery_pct"): ... table.add_row(key, ...) | Tabela de status mostra as chaves cruas em inglês (connected/battery_pct) para o usuário final | **Mapear rótulos: "Conectado", "Conexão (USB/Bluetooth)", "Perfil ativo", "Bateria (%)"** |

## `src/hefesto_dualsense4unix/cli/cmd_tray.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 34 | tray ativo — clique no icone pra acessar o menu. | 'icone' sem acento; 'tray' é jargão | **Ícone na bandeja ativo — clique nele para abrir o menu.** |
| 72 | f"Bat {bateria}% \| Perfil: {perfil}" | Mostra 'Bat None%' quando a bateria é desconhecida; abreviação 'Bat' críptica | **f"Bateria {bateria if bateria is not None else '?'}% \| Perfil: {perfil}"** |

## `src/hefesto_dualsense4unix/cli/cmd_coop.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 27 | help="Co-op local: cada controle vira um jogador (P1, P2, …)." | Jargão 'co-op' (queixa 1); o resto da frase já explica bem | **"Vários jogadores: cada controle vira um jogador (P1, P2, …)."** |
| 56 | lembre: precisa do gamepad virtual ligado (hefesto-dualsense4unix gamepad on) + 2+ controles. | 'gamepad virtual' é jargão; ok para CLI mas dá pra alinhar com o nome do modo da GUI | **lembre: precisa do modo 'Jogar pelo Hefesto' ligado (hefesto-dualsense4unix gamepad on) e 2 ou mais controles.** |

## `uninstall.sh` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 307 | ERRO: sudo recusado/sem TTY — udev rules NÃO foram removidas. | 'sem TTY' e 'udev rules' não dizem ao leigo o que aconteceu nem o que fazer. | **ERRO: sem a senha de administrador não deu para remover as regras do controle. Rode o ./uninstall.sh de novo num terminal e digite a senha quando pedir.** |
| 516 |  Hefesto - Dualsense4Unix desinstalado (wipe completo) | 'wipe' é jargão em inglês. | ** Hefesto - Dualsense4Unix desinstalado por completo (seus perfis foram preservados; use --purge-config para apagá-los)** |

## `src/hefesto_dualsense4unix/daemon/ipc_handlers.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 719 | raise ValueError("gamepad.emulation.set exige 'enabled' boolean") | Toda a família de ValueError dos handlers (ipc_handlers.py:135,138,139,165,194,251,523,562,742,763...) vira CODE_INVALID_PARAMS e é interpolada crua no toast da GUI. Texto de contrato de API dentro de um aviso para leigo. | **Manter as mensagens como estão (são úteis no log/CLI), mas a GUI NUNCA deve interpolar `exc` — ver sugestão de home_actions.py:403. Alternativa: separar `message` (para humano) de `data` (para dev) no erro JSON-RPC.** |
| 789 | plugins não habilitados neste daemon | "daemon" + "habilitados". Não diz COMO habilitar, então o erro é um beco sem saída. | **Os plugins estão desligados. Ligue 'plugins_enabled' na configuração do Hefesto e reinicie antes de recarregar.** |

## `src/hefesto_dualsense4unix/core/system_check.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 64 | regras udev de hotplug desatualizadas (nome de unit antigo) — rode: sudo bash scripts/install_udev.sh | JARGÃO PESADO direto na notificação (udev, hotplug, unit, sudo bash, caminho de script). É o body de notify_system_warnings (lifecycle.py:1441). Leigo não tem chance. | **"O Hefesto não está detectando o controle sozinho quando você o conecta. Abra o Hefesto e clique em 'Consertar' na aba Início."** |
| 69 | WirePlumber fixou o DualSense como microfone padrão — rode: scripts/doctor.sh --fix | Jargão (WirePlumber, doctor.sh --fix) + comando de terminal. Mesmo caminho de notificação. | **"O som do computador está sendo gravado pelo microfone do controle. Abra o Hefesto e clique em 'Consertar' na aba Início."** |

## `src/hefesto_dualsense4unix/app/actions/triggers_actions.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 481 | f"{side.upper()} -> {preset_id} aplicado" | Saída em inglês e em código: 'LEFT -> Rigid aplicado'. 'side.upper()' vira LEFT/RIGHT e 'preset_id' é a chave interna (Rigid, Galloping, MultiPositionFeedback). O usuário vê o nome PT-BR no botão e outro nome em inglês na barra de | **Usar o lado em PT-BR e o label do spec: f"Gatilho {'esquerdo (L2)' if side=='left' else 'direito (R2)'}: {spec.label} ligado" — ex.: "Gatilho esquerdo (L2): Trava firme ligado".** |
| 483 | f"{side.upper()} -> {preset_id} falhou (daemon offline?)" | Culpa o daemon por QUALQUER falha, inclusive erro de validação (start >= end) que é culpa dos sliders. Ver BUG-3. | **Distinguir os dois casos: sem daemon → "O Hefesto não está rodando — ligue na aba Daemon."; com erro de valor → "Esse ajuste não é possível: o 'Fim' precisa ser maior que o 'Início'."** |

## `src/hefesto_dualsense4unix/integrations/uinput_gamepad.py` (2)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 53 | XBOX360_NAME = "Microsoft X-Box 360 pad (Hefesto - Dualsense4Unix virtual)" | String que a usuária LÊ na lista de controles da Steam/do jogo. Três problemas: (a) 'Dualsense4Unix virtual' é nome interno de repositório, não fala com leigo; (b) com co-op, os 4 vpads recebem o nome IDÊNTICO — a Steam mostra 4 l | **XBOX360_NAME = "Controle Hefesto — Jogador 1"  # e, por jogador: f"Controle Hefesto — Jogador {n}". Mantém o VID/PID Xbox 360 (que é o que faz o jogo vibrar) e muda só o rótulo: o jogo continua tratando como Xbox, e a usuária vê '** |
| 58 | DUALSENSE_NAME = "Sony Interactive Entertainment DualSense Wireless Controller" | É o nome do CONTROLE FÍSICO, byte a byte (o mesmo nome que a regra assets/78-dualsense-motion-not-joystick.rules casa em ATTRS{name} e que o kernel hid_playstation publica). Com a máscara DualSense o jogo/Steam lista DUAS entradas | **DUALSENSE_NAME = "DualSense (Hefesto) — Jogador 1"  # e, por jogador: f"DualSense (Hefesto) — Jogador {n}". Nome distinto do físico + número do jogador: o jogo passa a listar 'DualSense (Hefesto) — Jogador 1..4' e a usuária identi** |

## `src/hefesto_dualsense4unix/cli/cmd_mouse.py` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 24 | Emulação de mouse+teclado pelo DualSense (via daemon). | 'emulação' e 'daemon' são jargões | **O controle vira mouse e teclado do PC (mesma função da aba Mouse).** |

## `run.sh` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 19 | erro: .venv/ não encontrado. Rode ./scripts/dev_bootstrap.sh primeiro. | O run.sh é o Exec do .desktop do usuário final; a instrução aponta para o script de DESENVOLVEDOR em vez do instalador. | **erro: instalação incompleta (.venv ausente). Rode ./install.sh primeiro.** |

## `packaging/debian/control` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 17 | e GUI GTK3 com 9 abas (Status, Gatilhos, Lightbar, Rumble, Perfis, Daemon, Emulacao, Mouse, Teclado). | Desatualizado: são 10 abas — falta a aba Início (a mais importante para o leigo). | **e GUI GTK3 com 10 abas (Inicio, Status, Gatilhos, Lightbar, Rumble, Perfis, Daemon, Emulacao, Mouse, Teclado).** |

## `scripts/install-host-udev.sh` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 21 | USB que derruba a conexão e disparam hotplug-GUI (USB + BT). | Header afirma que as regras disparam hotplug-GUI, mas as rules 73/74 foram removidas do conjunto — documentação stale. | **USB que derruba a conexão. (As regras de hotplug-GUI 73/74 foram descontinuadas.)** |

## `scripts/install_udev.sh` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 91 |   - Desconecte e reconecte o DualSense (USB) ou reemparelhe (BT). | 'reemparelhe' é impreciso (basta reconectar; re-parear é só para o caso SDP) e não há instrução de COMO. | **  - Desconecte e reconecte o controle (cabo USB) ou desligue e ligue de novo (Bluetooth: segure o botão PS).** |

## `docs/process/sprints/2026-07-13-sprint-paridade-de-features.md` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 90 | - [ ] SPRINT-GAME-RUMBLE-01 (acima) — primeiro item da fila. - [ ] Matriz de paridade completa — executar em seguida. | Checkboxes abertos para trabalho já EXECUTADO (resultado em 2026-07-14-auditoria-paridade-resultado.md e fixes na v3.13.0) — doc de intenção diverge do estado e induz retrabalho de auditoria. | **- [x] SPRINT-GAME-RUMBLE-01 — executado 2026-07-14 (causa provada: máscara DualSense; ver CHANGELOG 3.13.0). - [x] Matriz de paridade — executada 2026-07-14 (ver 2026-07-14-auditoria-paridade-resultado.md).** |

## `src/hefesto_dualsense4unix/daemon/ipc_server.py` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 285 | f"método desconhecido: {method}" | Chega na tela via toast com o nome do método interno: "Falha ao mudar o modo ([-32601] método desconhecido: coop.set)" — cenário REAL quando a GUI é mais nova que o daemon instalado. | **"esta versão do Hefesto não conhece essa ação (atualize o Hefesto)" — o nome do método fica no log.** |

## `src/hefesto_dualsense4unix/daemon/connection.py` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 244 | notify_controller_disconnected("probe offline") | JARGÃO INTERNO VAZANDO PRA TELA. Vira o body "DualSense desconectado (probe offline)." (desktop_notifications.py:260). 'probe offline' é nome de rotina interna; leigo não faz ideia. | **notify_controller_disconnected() sem razão — body deve ficar "Controle desconectado. Se foi sem querer, reconecte o cabo ou aperte o botão PS."** |

## `src/hefesto_dualsense4unix/daemon/lifecycle.py` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 1499 | self.bus.publish(EventTopic.CONTROLLER_DISCONNECTED, {"reason": str(exc)}) | `str(exc)` é a mensagem CRUA da exceção (ex.: '[Errno 19] No such device'). Esse `reason` alimenta o mesmo canal de desconexão que chega ao usuário — traceback-ês na notificação. | **Publicar reason="leitura_perdida" (código interno) e manter o texto humano só na camada de notificação: "Controle desconectado. Se foi sem querer, reconecte o cabo ou aperte o botão PS."** |

## `src/hefesto_dualsense4unix/daemon/subsystems/metrics.py` (1)

| Linha | Atual | Problema | Proposta |
|---|---|---|---|
| 252 | somente /metrics está disponível | Frase truncada, sem sujeito. Aparece no navegador de quem ligou as métricas e abriu 127.0.0.1:9090 na raiz (o caminho mais natural). | **Este endereço não existe. As métricas do Hefesto ficam em /metrics.** |
