# workflow o-que-falta-medir-com-o-hardware-dela

- runId: wf_ff5f3f51-7c9 | status: completed | agentes: 7 | tokens: 1,058,543 | duracao: 32 min
- summary: Varrer o acervo de sprints atras de tudo que so fecha com hardware na mao dela, e escrever os protocolos no formato que acabou de funcionar
- fases: Varrer, Priorizar, Escrever

## RESULTADO

### ficha

[
  {
    "codigo": "INVENTARIO-VIVO-01/P1",
    "pergunta": "Quantos 8BitDo e quantos DualSense existem fisicamente na casa? (o registro guarda dois DualSense e dois enderecos 8BitDo; o BlueZ so conhece um de cada — GRAU hoje: MEDIDO no disco, SEM PROVA sobre o mundo fisico)",
    "hardware": "nenhum — so a resposta dela",
    "tem_agora": true,
    "custo_min": 2,
    "valor": "alto",
    "bloqueia": "IDENT-01 e IDENTIDADE-DUPLA-01 inteiras, o M-15, o M-12 e toda medicao de quatro na mesa; e a poda do rank 1 do controllers.json, que hoje empurra todo mundo para baixo"
  },
  {
    "codigo": "RADIO-ABERTO-01/E1-bis+E2",
    "pergunta": "Com o JustWorksRepairing em confirm no disco e o agente vivo, um re-pareamento legitimo dela ainda completa? (o disco dela esta em always agora — MEDIDO; o custo da troca e SUSPEITA COM MECANISMO)",
    "hardware": "root na maquina dela + o DualSense por BT para re-parear; Passo 0 para o hefesto-bt-health-watchdog e o fim religa",
    "tem_agora": true,
    "custo_min": 20,
    "valor": "alto",
    "bloqueia": "a E2 (agente proprio que autoriza por politica) e a E3 (alarme de sobrescrita de LinkKey); enquanto isso o furo de seguranca segue no disco dela, e e o unico item cujo pior caso nao e um controle que nao funciona"
  },
  {
    "codigo": "RADIO-BOMBARDEADO-01/F2",
    "pergunta": "A tempestade de 44.718 frames vem de STREAMAR audio (banda isocrona reservada) e nao de enumerar? (as hipoteses 1 e 2 foram REFUTADAS por medicao; a 3 e SUSPEITA COM MECANISMO)",
    "hardware": "um DualSense — 5 min no radio sem fluxo de audio e 5 min com parec/pw-play no cabo; Passo 0: a suite de testes PARADA e journalctl sempre com data completa",
    "tem_agora": true,
    "custo_min": 20,
    "valor": "alto",
    "bloqueia": "a cura de produto (a tela avisar durante a sessao), e a correlacao com a SUITE-QUE-SUJA-O-JORNAL-01 — o mesmo experimento decide as duas"
  },
  {
    "codigo": "IDENTIDADE-DUPLA-01/E1",
    "pergunta": "Os dois enderecos 8BitDo (OUI e4:17:d8) aparecem JUNTOS, ou cada modo tem um endereco fixo e distinto? (existencia das duas identidades: MEDIDA no controllers.json; a correspondencia modo-endereco: SEM PROVA — e o journal de 03/08 parece refutar o criterio de fusao proposto)",
    "hardware": "o 8BitDo nos dois modos (PS4 e Start+A, medido — NAO X+Start, que e o X-input); Passo 0 para o watchdog de bonds e copia o controllers.json, o fim restaura os dois",
    "tem_agora": false,
    "custo_min": 15,
    "valor": "alto",
    "bloqueia": "IDENT-01/E1 a E4 (declaracao de identidades irmas, gesto na janela, desfazer, check no doctor) e a poda do controllers.json; hoje o mesmo plastico ocupa os ranks 4 e 5 para sempre"
  },
  {
    "codigo": "SEM-DONO/EXTERNO-PRIMEIRO-01",
    "pergunta": "O controle externo ligado antes de qualquer DualSense fica com o lugar 1 para sempre, atravessando boot? (cadeia MEDIDA no codigo: lifecycle.py:3546-3549 roda o tick de externos antes do gate, _ds_reserve devolve piso 0 e external_identity.py:501 da rank 1 persistivel; efeito na mesa SEM MEDICAO)",
    "hardware": "o 8BitDo ou o Pro + o DualSense; Passo 0 copia o controllers.json (e o guarda desta medicao) e o fim restaura",
    "tem_agora": false,
    "custo_min": 10,
    "valor": "alto",
    "bloqueia": "nenhuma sprint reivindica o achado — a queixa dela ('o 8bitdo entrou como player 1 igual o dualsense branco') segue sem dona, e o 'Renumerar agora' segue corroido"
  },
  {
    "codigo": "PARIDADE-SONY-01/E1",
    "pergunta": "O carimbo de audio_do_jogo muda quando ela abre um JOGO, ou continua a assinatura do kernel (alto-falante 100, rota 0x30)? (o carimbo e MEDIDO e reproduzivel; a autoria dentro do jogo e SEM PROVA)",
    "hardware": "o DualSense + um jogo aberto por ela; o assistente le daemon.state_full NO INSTANTE do aviso dela",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "alto",
    "bloqueia": "a E2 (replicar o campo que o jogo manda ao alto-falante) nao comeca sem saber qual campo replicar; se nao mudar, a sprint fecha como CICATRIZ"
  },
  {
    "codigo": "SINAL-DE-JOGO-01/E1",
    "pergunta": "A autoridade do jogo cai com o jogo comprovadamente VIVO depois dos 30 s de histerese? (mecanismo MEDIDO em game_signal.py:62 e :173; as seis transicoes apresentadas como prova foram DERRUBADAS pelo verificador)",
    "hardware": "o DualSense + um jogo + alt-tab para janela Wayland nativa e 90 s sem tocar em nada",
    "tem_agora": true,
    "custo_min": 20,
    "valor": "alto",
    "bloqueia": "E2 e E3 da SINAL-DE-JOGO-01; e sem `ps -o etimes` do processo do jogo colado ao carimbo a medicao NAO vale — foi exatamente essa omissao que invalidou as seis anteriores"
  },
  {
    "codigo": "PERFIL-JOGO-01/E1",
    "pergunta": "Qual dos quatro sintomas ela chama de 'o perfil muda' — o nome do perfil, o numero do controle, a cor ou os gatilhos? (SEM PROVA; e a entrega zero declarada: 'nada deve ser corrigido antes dele')",
    "hardware": "o DualSense + um jogo; quatro perguntas SEPARADAS antes de abrir, depois de abrir e depois de dois alt-tabs",
    "tem_agora": true,
    "custo_min": 25,
    "valor": "alto",
    "bloqueia": "as E3 e E4 da PERFIL-JOGO-01 — e a E4 precisa ser REESCRITA antes de virar codigo, porque depende deste resultado"
  },
  {
    "codigo": "SOM-ROTA-01/E2",
    "pergunta": "Com o pre-amp e a rota escritos, a faixa util do volume deixa de ser 64 passos? (a regua atual, mudo ate 38 e satura em 102, foi MEDIDA so com o volume — sem pre-amp e sem rota; a nova faixa e SEM PROVA)",
    "hardware": "o DualSense (alto-falante), o ouvido dela, sala silenciosa e a tela desligada; Passo 0 confere a porta de captura — o instrumento automatico falhou em 02/08 e quase deu veredito falso",
    "tem_agora": true,
    "custo_min": 25,
    "valor": "alto",
    "bloqueia": "o controle deslizante segue com ~60% de curso inerte; e se a faixa NAO mudar, a hipotese cai e a E1 precisa ser remedida antes de qualquer codigo"
  },
  {
    "codigo": "GYRO-02/M-5",
    "pergunta": "O enable-IMU do Pro Controller genuino faz alguma coisa — os eixos saem de zero? (o codigo esta de pe e o efeito NUNCA foi confirmado; previsao falsificavel: por CABO o uniq pode ser sintetico, e ai o gate de OUI e0f6b5 nunca dispara)",
    "hardware": "o Pro Controller GENUINO, por CABO (external_identity.py:165 recusa BT de proposito)",
    "tem_agora": false,
    "custo_min": 15,
    "valor": "alto",
    "bloqueia": "a fase 2 (IMU por radio) nao tem base para nem ser discutida; e o ExternalImuEnabler segue no repositorio sem ninguem saber se cura — a propria docstring o chama de 'candidato de cura'"
  },
  {
    "codigo": "M-15 / MIC-BT-DONO-01/E4",
    "pergunta": "Os botoes de gesto dos controles 2, 3 e 4 veem algum evento, ou todo gesto do produto nasce do primario? (mecanismo MEDIDO: read_state abre com 'INPUT vem SEMPRE do controle PRIMARIO' e mic_btn nao tem keycode evdev; efeito por controle SEM MEDICAO)",
    "hardware": "DOIS DualSense — o botao de microfone so existe neles; contraste obrigatorio: o mesmo botao no primario, e depois trocar quem e o primario",
    "tem_agora": false,
    "custo_min": 10,
    "valor": "alto",
    "bloqueia": "a E4 da MIC-BT-DONO-01 e todo desenho de gesto por controle; hoje INEXECUTAVEL — o inventario ve um DualSense so, e o segundo nem tem bond"
  },
  {
    "codigo": "M-12 / POSSE-POR-CONTROLE-01/E1",
    "pergunta": "A trava manual congela a cor dos QUATRO, e nao so do controle mexido? (mecanismo MEDIDO: state_store.py:102 e um set unico sem MAC, e manager.py:388-391 obedece com None para todos; efeito na mesa SEM MEDICAO)",
    "hardware": "dois controles que o daemon pinta; Passo 0 faz um profile.switch manual (limpa as tres categorias) e TRAVA o autoswitch, e o fim destrava",
    "tem_agora": false,
    "custo_min": 25,
    "valor": "alto",
    "bloqueia": "E1, E2 e E3 da POSSE-POR-CONTROLE-01; a bancada de dois MACs falsos vem ANTES e ela so confirma que a bancada representa a mesa"
  },
  {
    "codigo": "BT-FURO-FINO-01/defeito-1",
    "pergunta": "O leitor de movimento aceita pacote de AUDIO como input — o giroscopio anda com o controle parado? (MEDIDO que physical_report_reader.py:236-244 testa id, tamanho e CRC e NAO testa o bit de audio; o efeito e SUSPEITA COM MECANISMO)",
    "hardware": "o DualSense no BT com a ponte de mic ligada + evtest no no, controle PARADO na mesa; AVISO a ela antes: se confirmar, o controle fica inutilizavel enquanto o mic estiver no ar",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "alto",
    "bloqueia": "o endereco da cura nao se decide sem isto — se o evtest nao mostrar evento, o problema e do kernel/DKMS e nao do nosso leitor"
  },
  {
    "codigo": "QUATRO-NO-RADIO-01/d1+d4+d5",
    "pergunta": "Com os quatro no radio E um jogo aberto, quantos evdev_grab_failed, coop_player_removed e erros de CRC aparecem — e o rumble sobrevive? (SEM PROVA: os quatro ja conectaram em 03/08, mas nenhum jogo foi aberto)",
    "hardware": "quatro controles (dois DualSense, o Pro e o 8BitDo) + um jogo; amostrar daemon.state_full, NUNCA /sys/class/leds",
    "tem_agora": false,
    "custo_min": 40,
    "valor": "alto",
    "bloqueia": "o aceite final da leva dos quatro; e ela mesma esta bloqueada — NAO medir antes da COOP-QUE-NAO-DESMONTA-01, porque com o Jogador 2 durando dois segundos dois dos quatro sao o mesmo jogador"
  },
  {
    "codigo": "PERFIS-DELA/C-1",
    "pergunta": "Qual regra cada um dos quatro perfis dela deveria ter — o sackboy_nativo virou catch-all em prioridade 191 (o asset de fabrica e criteria/steam_app/prioridade 80), e ha tres empates? (MEDIDO no disco em 05/08)",
    "hardware": "a janela do Hefesto e a pasta de perfis dela — e a palavra dela em cada um",
    "tem_agora": true,
    "custo_min": 30,
    "valor": "alto",
    "bloqueia": "as sete curas impedem estrago NOVO e nenhuma conserta o ja feito; o historico so grava a partir de 05/08 e nao alcanca as versoes velhas"
  },
  {
    "codigo": "CHECKLIST-§1 / M-06",
    "pergunta": "Um controle fisico vira UM dispositivo de jogo dentro do jogo, ou o input duplicado voltou? (o remendo de 26/07 nunca foi confirmado ao vivo — SEM PROVA)",
    "hardware": "o DualSense + um jogo; foto de /proc/bus/input/devices antes e dentro do jogo",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "alto",
    "bloqueia": "o M-06 segue sem confirmacao ao vivo; vale rodar na MESMA sessao do experimento que fechou o M-04 — os dois olham a mesma tela de configuracao de controle"
  },
  {
    "codigo": "NOME-HONESTO-01/E1+E2",
    "pergunta": "O que a tela chama o 8BitDo no CABO, em cada modo? (MEDIDO com entradas sinteticas: em modo Switch por cabo a ficha diz 'Pro Controller' e a marca diz 'Nintendo'; e friendly_type e brand_of usam ordens OPOSTAS entre OUI e VID)",
    "hardware": "o 8BitDo + cabo USB, nos dois modos; ela abre a ficha do controle e fotografa",
    "tem_agora": false,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "a E2 (o rotulo nao pode ultrapassar o sinal) nao tem foto para ser aceita; e a discordancia so aparece com os dois Nintendo-class na mesa"
  },
  {
    "codigo": "INVENTARIO-VIVO-01/P2",
    "pergunta": "Foi ela que pos 'Nintendo MeowSystem' como alias e a Class 0x6C0104 no adaptador para o Pro aceitar o pareamento? (MEDIDO que o alias existe; MEDIDO que NAO vem deste repositorio; a causa e SUSPEITA COM MECANISMO)",
    "hardware": "nenhum — a memoria dela",
    "tem_agora": true,
    "custo_min": 2,
    "valor": "medio",
    "bloqueia": "qualquer protocolo com o Pro Controller: se o alias/Class for pre-requisito do pareamento, mexer no adaptador derruba o Pro no meio da medicao"
  },
  {
    "codigo": "QUATRO-NO-RADIO-01/d2+d3",
    "pergunta": "O 8BitDo em modo PS4 e o Pro em modo Switch sobrevivem por BT a uma sessao com os outros no ar, ou caem JUNTOS? (a tabela marca o Pro em Switch como PROVADO instavel; o 8BitDo em PS4 e SEM PROVA)",
    "hardware": "o 8BitDo (Start+A) + o Pro em modo Switch + o DualSense",
    "tem_agora": false,
    "custo_min": 25,
    "valor": "medio",
    "bloqueia": "nada — mas e o contraste barato que separa 'a culpa e do modo' de 'a culpa e do radio'; se cairem juntos, a causa e o radio"
  },
  {
    "codigo": "RADIO-BOMBARDEADO-01/F3",
    "pergunta": "A tempestade muda com o dongle BT em porta de OUTRO barramento? (topologia como causa: SEM PROVA)",
    "hardware": "o dongle BT TP-Link e a mao dela no cabo — e o unico ponto da F2/F3 que exige ela",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "nada — so entra se a F2 devolver 'as duas fases produzem frames'"
  },
  {
    "codigo": "MIC-BT-DONO-01/E2",
    "pergunta": "Derrubando o Bluetooth e religando sem tocar em nada, o bit de mudo do microfone volta a zero em ate um tique de hotplug? (o mapa por controle nao existe: _mic_mute_desejado e por instancia — MEDIDO)",
    "hardware": "o DualSense no BT",
    "tem_agora": true,
    "custo_min": 5,
    "valor": "medio",
    "bloqueia": "nada — mas o alvo honesto e 55-75% de mudo, nao 0% (o BT-MIC-GATING-01 segue aberto); prometer 0% e prometer o que a casa ja mediu como nao obtido"
  },
  {
    "codigo": "TRIGGER-CANON-01/aceite",
    "pergunta": "Os sete presets curados fazem o que o nome promete, no tato dela? (MEDIDO que a cura entrou e que sete presets que nao faziam nada passaram a fazer; a sensacao e SEM PROVA)",
    "hardware": "o DualSense (gatilhos) e o tato dela",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "medio",
    "bloqueia": "o fechamento da TRIGGER-CANON-01; e enquanto a E5 (ler o nibble alto do byte de status) nao entrar, CADA rodada de gatilho custa tempo dela"
  },
  {
    "codigo": "SENSOR-VIVO-01/E4",
    "pergunta": "Dentro de um jogo que usa o touchpad como botao, o clique abre a coisa — e o cursor do mouse NAO anda enquanto ela desliza o dedo? (o codigo entrou e esta MEDIDO; o efeito no jogo e SEM PROVA)",
    "hardware": "o DualSense + um jogo que use o touchpad como botao; o contador de cliques ja e exposto pelo IPC",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "o fechamento da SENSOR-VIVO-01 — o codigo entrou e ninguem sabe se funciona no jogo; o segundo aceite (jogador 2) precisa de dois controles"
  },
  {
    "codigo": "M-17",
    "pergunta": "Qual mascara entrega vibracao, giroscopio e lightbar no Sackboy — a de DualSense ou a de Xbox? (MEDIDO que a contradicao existe: o tooltip da janela diz uma coisa e o asset sackboy_nativo.json grava outra; qual lado esta certo e SEM PROVA)",
    "hardware": "o DualSense + Sackboy, abrindo com cada mascara",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "medio",
    "bloqueia": "a contradicao entre a janela e o asset de fabrica fica sem arbitro, e a migracao dualsense-para-xbox de 26/07 segue sem veredito"
  },
  {
    "codigo": "SEM-DONO/RUMBLE-FIXADO-GLOBAL-01",
    "pergunta": "Fixar ou parar o rumble de UM controle pela aba Rumble bloqueia o FF do jogo em TODOS? (MEDIDO no codigo: gamepad.py:747 checa rumble_active, um valor unico sem MAC, ANTES de qualquer targeting; a reafirmacao, essa sim, respeita o seletor)",
    "hardware": "dois controles + um jogo vibrando; contraste: rumble.passthrough deve devolver os dois",
    "tem_agora": false,
    "custo_min": 5,
    "valor": "medio",
    "bloqueia": "nenhuma sprint reivindica o achado — e irmao exato do defeito 1 da POSSE-POR-CONTROLE-01 e nao esta la"
  },
  {
    "codigo": "M-08",
    "pergunta": "A mascara do perfil sobrevive a um reboot, ou quem manda no boot sao os flags persistidos? (mecanismo MEDIDO: mode_applier=None no restore, com o motivo escrito; o resultado e SUSPEITA COM MECANISMO)",
    "hardware": "o DualSense + um reboot da maquina dela, com o controle na mesa",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "medio",
    "bloqueia": "nada — mas a FEAT-PROFILE-MODE-01 fica sem veredito, e o roteiro obrigatorio (git log -S mode_applier) nunca foi executado"
  },
  {
    "codigo": "M-07",
    "pergunta": "Com jogo aberto, a tela diz que aplicou a mascara enquanto o gate a recusa? (MEDIDO no codigo: o ramo bloqueado devolve True porque o contrato e 'ativo ao final', nao 'aplicou o pedido'; o que a tela informa e SEM PROVA)",
    "hardware": "o DualSense + um jogo aberto; ela troca a mascara pela janela e diz o que leu, o assistente le o retorno do IPC no mesmo instante",
    "tem_agora": true,
    "custo_min": 5,
    "valor": "medio",
    "bloqueia": "nada — cabe dentro de qualquer outra sessao de jogo"
  },
  {
    "codigo": "MODO-01/CHECKLIST-§3",
    "pergunta": "Um jogo que casa coop_local por titulo liga o modo jogo com o cadeado de perfil ligado — e ao fechar o jogo o controle segue funcionando no desktop? (MEDIDO em parte com tres jogos sem perfil proprio; o caso do cadeado e SEM PROVA)",
    "hardware": "o DualSense + um jogo do casamento por titulo (Sackboy, Overcooked, It Takes Two ou Cuphead)",
    "tem_agora": true,
    "custo_min": 15,
    "valor": "medio",
    "bloqueia": "nada"
  },
  {
    "codigo": "PROVA-DE-TELA-01/nove-abas",
    "pergunta": "As nove abas com a janela real maximizada estao aceitaveis — e os tres dialogos novos de 05/08, que ninguem nunca fotografou? (as tres sprints estao ENTREGUES em codigo com medicao em bancada; o aceite e SEM PROVA)",
    "hardware": "nenhum — a tela dela, janela maximizada, uma aba por vez",
    "tem_agora": true,
    "custo_min": 20,
    "valor": "medio",
    "bloqueia": "o fechamento de ALINHA-DUAS-LINHAS-01, JANELA-QUE-RESPIRA-01 e CARD-UNICO-01, e dos tres dialogos que o indice de 05/08 registra como 'a tela: ninguem olhou'"
  },
  {
    "codigo": "LIGHTBAR-JOGADOR-01/E0",
    "pergunta": "O que as cinco luzes de jogador deveriam mostrar, se e que devem existir? (MEDIDO que ZERO linhas foram escritas e que os cinco widgets seguem vivos na janela; e queixa direta dela: 'essas cores que nao fazem sentido')",
    "hardware": "a tela + o DualSense ao lado para comparar o que a barra faz de verdade",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "a sprint inteira (E0 a E5) nao tem uma linha, e o desenho depende do que ela quer ver"
  },
  {
    "codigo": "RADAR-01/E1",
    "pergunta": "O popover do applet do painel mostra o estado certo — inclusive o cadeado do autoswitch? (MEDIDO que o campo autoswitch_locked NAO existe no ipc.rs do applet; a aparencia e SEM PROVA)",
    "hardware": "a tela dela — o popover do cosmic-panel e a UNICA superficie do projeto que nao da para fotografar com Gtk.OffscreenWindow",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "a E1 do RADAR-01 e a divergencia D2; nenhum instrumento nosso substitui o olho dela aqui"
  },
  {
    "codigo": "CARD-OCUPA-01",
    "pergunta": "Os desenhos (touchpad, lightbar, microfone, alto-falante) ocuparam bem o vao lateral do cartao? (ABERTA; e pedido literal dela de 31/07 — SEM PROVA)",
    "hardware": "a tela, aba Status, janela maximizada",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "medio",
    "bloqueia": "nada — mas e pedido dela, e nenhuma medida de bancada responde por gosto"
  },
  {
    "codigo": "EMULACAO-NO-JOGO-01/C-4",
    "pergunta": "Ela usava o Alt+Tab do R1 de PROPOSITO no desktop, e o que o R1 deveria fazer? (MEDIDO: 9 pressionamentos em 7 dias, TODOS dentro de janela de jogo; a intencao e SEM PROVA)",
    "hardware": "nenhum — a resposta dela",
    "tem_agora": true,
    "custo_min": 3,
    "valor": "medio",
    "bloqueia": "mudar o padrao do R1; e o efeito do Alt+Tab no compositor segue sendo inferencia, nao medicao"
  },
  {
    "codigo": "JOGO-COMPLETO-01/E4",
    "pergunta": "Os dois interruptores (broker e wrapper) ligam sem quebrar nada, e o install e idempotente sobre as opcoes de lancamento? (SEM PROVA — o install precisa ser RODADO de verdade na maquina dela)",
    "hardware": "a maquina dela, install.sh NUNCA com sudo e com --yes sem TTY; um jogo depois para conferir; a ordem e irreversivel na pratica",
    "tem_agora": true,
    "custo_min": 25,
    "valor": "medio",
    "bloqueia": "os dois recursos seguem atras de flag; e a idempotencia so se prova rodando DUAS vezes — ligar o broker antes do wrapper tira a rede de seguranca e pode deixar ela sem controle no jogo"
  },
  {
    "codigo": "BORDA-DE-QUEDA-01/defeito-1",
    "pergunta": "Ao desligar o Controle 2 com o jogo vibrando, o motor do outro segue ~3 s (o teto do expirador)? (ela JA confirmou pelo tato em 03/08 — falta so a confirmacao numerica)",
    "hardware": "dois controles no BT + um jogo vibrando",
    "tem_agora": false,
    "custo_min": 5,
    "valor": "baixo",
    "bloqueia": "nada — a cura pode ser escrita sem isto, e os defeitos 2 e 3 da mesma sprint ja estao MEDIDOS no codigo"
  },
  {
    "codigo": "RUMBLE-PRESO-01/releitura",
    "pergunta": "Depois de o teto cair de 6 s para 3 s, o silencio medido se concentra logo acima de 3 s (pedido atrasado) ou fica muito maior (pedido que nunca chega)? (MEDIDO uma vez com o teto antigo: 90 min, 17 disparos, sete perceptiveis)",
    "hardware": "o DualSense + 30 minutos ou mais de jogo dela — tempo que ela ja gastaria jogando",
    "tem_agora": true,
    "custo_min": 35,
    "valor": "baixo",
    "bloqueia": "nada — e mitigacao declarada, nao cura; a cura exige capturar os bytes que o jogo escreve no gamepad virtual"
  },
  {
    "codigo": "SOM-ROTA-01/E4+E5",
    "pergunta": "Qual e o caminho do microfone e o byte 53 realmente denuncia fone plugado? (SEM PROVA — as duas dependem de medicao no hardware)",
    "hardware": "o DualSense + um fone de 3,5 mm no controle; o inventario NAO lista fone — se ela nao tiver, o item nao existe",
    "tem_agora": false,
    "custo_min": 15,
    "valor": "baixo",
    "bloqueia": "nada"
  },
  {
    "codigo": "RADAR-01/E2",
    "pergunta": "Vale manter as 463 linhas da bandeja, se ela nao aparece na maquina dela? (MEDIDO que o aviso ainda esta sem acento e com termo em ingles; a decisao de produto e dela)",
    "hardware": "a tela; e a flag de aviso ja mostrado APAGADA antes, senao ela ve o texto velho e reprova a correcao por engano",
    "tem_agora": true,
    "custo_min": 5,
    "valor": "baixo",
    "bloqueia": "nada — e pergunta de produto, nao medicao"
  },
  {
    "codigo": "LARGURA-01/E8",
    "pergunta": "A grade de tres colunas fixas da aba Gatilhos esta boa na largura real da janela dela? (MEDIDO que o numero de colunas continua cravado em 3; o aceite e SEM PROVA)",
    "hardware": "a tela, aba Gatilhos, foto antes e depois",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "baixo",
    "bloqueia": "nada — mas a E8 entra SOZINHA: a aba Gatilhos ja teve um commit rejeitado e a VAO-01 proibiu carona"
  },
  {
    "codigo": "STATUS-SIMETRIA-01",
    "pergunta": "Qual e o numero final de simetria da aba Status? (a propria sprint declara: 'o numero final e decisao dela, olhando a tela')",
    "hardware": "a tela, aba Status",
    "tem_agora": true,
    "custo_min": 5,
    "valor": "baixo",
    "bloqueia": "nada"
  },
  {
    "codigo": "FIACAO-QUE-FALTA-01/E1",
    "pergunta": "O aviso do verificador de perfis na aba Perfis esta claro sem atrapalhar? (o verificador existe com 393 linhas e 25 testes e so o doctor o chama — MEDIDO; o aviso na janela ainda nao existe)",
    "hardware": "a tela, aba Perfis — so DEPOIS de a fiacao existir",
    "tem_agora": true,
    "custo_min": 10,
    "valor": "baixo",
    "bloqueia": "nada — e o veto ja esta escrito: o aviso nao pode bloquear o salvar"
  }
]

### possiveis_agora

30

### total

41

### doc

Documento criado, quatro portões verdes.

`/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md` (1.214 linhas).

41 medições pendentes conferidas contra o código; **32 dão para fazer agora**, 6 esperam ela ligar um aparelho que tem, 3 dependem de aparelho que talvez não tenha (dois DualSense, cabo USB, fone de 3,5 mm).

O inventário mudou no meio da varredura e reordenou a fila: às 20h27 medi **três controles físicos no rádio** (DualSense + Pro Controller genuíno + 8BitDo em modo PS4, números 1/2/3), com a suíte de testes parada. Isso promoveu `QUATRO-NO-RÁDIO-01`/d2+d3 e metade da `IDENTIDADE-DUPLA-01`/E1 para "mede agora".

Achado que refuta premissa do acervo (GRAU: MEDIDO): a **IMU do Pro Controller está viva por Bluetooth** — 1.825 eventos de eixo em 6 s, gravidade estável, controle parado — apesar de o código recusar o enable-IMU por rádio de propósito. A pergunta do GYRO-02 encolheu para o caminho USB.

As três primeiras da fila:
1. **`RADIO-ABERTO-01`/E1-bis+E2** (20 min) — com `JustWorksRepairing=confirm` no disco e o agente vivo, um re-pareamento legítimo dela ainda completa? É o único item cujo pior caso não é "um controle que não funciona"; o disco dela continua em `always`.
2. **`PERFIL-JOGO-01`/E1** (25 min) — qual dos quatro sintomas ela chama de "o perfil muda": o nome, o número do controle, a cor ou os gatilhos? É a entrega zero declarada, e a E4 precisa ser reescrita depois dela.
3. **`PARIDADE-SONY-01`/E1** (15 min) — o carimbo `audio_do_jogo` muda dentro de um jogo, ou continua a assinatura do kernel? Se não mudar, a sprint fecha como cicatriz sem uma linha de código.

Item de maior alavancagem, e **não precisa dela**: a bancada dos quatro controles com relógio virtual (`COOP-QUE-NÃO-DESMONTA-01`/E4) não existe e bloqueia a medição de maior valor da casa.

Nada em `src/` nem em `tests/` foi tocado; nada commitado. Portões: acentuação, glifos, referências (197 documentos sem referência morta) e anonimato — todos verdes, mais `test_docs_mac_anonimato.py` e `check_test_data.sh`. Regex confirmou zero emoji, zero U+2713/U+2717 e zero MAC real (com separador ou compacto).


## LOGS

41 medicoes pendentes; 30 possiveis com o hardware que esta na mesa agora
