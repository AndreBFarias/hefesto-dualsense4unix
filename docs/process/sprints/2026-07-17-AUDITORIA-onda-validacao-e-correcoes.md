# 2026-07-17 — Auditoria da onda multicontrole+dedup: validação + correções

Auditoria multi-agente (28 agentes, verificação adversarial) sobre as 5 Fases da onda + validação viva da GUI aba-a-aba (2 DualSense BT + 8BitDo USB). **69 achados confirmados** (6 HIGH, 28 MED, 35 LOW).

## Corrigidos neste passe (17)

Inclui TODOS os 6 HIGH + os vazamentos de jargão pro leigo mais claros.

- **[HIGH] COR-03-wake** — Cor automática não re-resolve em wake/reconexão pós-boot — só na ativação de perfil (achado ao vivo confirmado no código)
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py:884`
- **[HIGH] COR-A-toggle-off-destroi-match** — Desligar "Modo avançado" num perfil de jogo e Salvar troca o alvo para "Sempre" sem avisar
  `src/hefesto_dualsense4unix/app/actions/profiles_actions.py:812`
- **[HIGH] RUM-01-botao-fantasma** — Toasts e rótulo de estado mandam clicar 'Devolver ao jogo' — botão que não existe (chama-se 'Deixar o jogo controlar a vibração')
  `src/hefesto_dualsense4unix/app/actions/rumble_actions.py:497`
- **[HIGH] KBD-01-teclado-jargao-total** — Aba Teclado é 100% jargão de programador (nomes internos em inglês + tokens KEY_*/__OSK__) — impossível para leigo
  `src/hefesto_dualsense4unix/app/actions/input_actions.py:130`
- **[HIGH] COR-WAKE-01-reassert-fora-do-hotplug** — reassert_resolved_outputs() nunca é chamado no caminho de probe/hotplug/wake — só na ativação de perfil
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py:727`
- **[HIGH] GOLD-01-readme-veneno** — README §3 ainda manda COLAR o veneno IGNORE_DEVICES e o atribui ao botão que hoje copia o wrapper
  `README.md:182`
- **[MED] EMU-04-mic-manda-rodar-script** — Ligar o microfone manda o leigo 'rodar scripts/install_usb_quirk.sh' e fala em 'storm -71'
  `src/hefesto_dualsense4unix/app/actions/emulation_actions.py:302`
- **[MED] ST-01-daemon-jargao** — Aba Status ainda expõe 'Daemon' — jargão que a onda inteira jurou matar
  `src/hefesto_dualsense4unix/app/actions/status_actions.py:761`
- **[MED] LB-01-rgb-cru-no-toast** — Toast de aplicar cor despeja a tupla RGB crua: 'Cor RGB (255, 128, 0) a 100% aplicada'
  `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py:228`
- **[MED] LB-02-daemon-offline-interrogacao** — Toasts de falha dizem '(daemon offline?)' — jargão + palpite em forma de pergunta (anti-padrão já conhecido)
  `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py:230`
- **[MED] TRG-01-toast-left-off** — Toast dos gatilhos diz 'LEFT -> Off aplicado' (lado em inglês + id interno) em vez do que a pessoa clicou
  `src/hefesto_dualsense4unix/app/actions/triggers_actions.py:554`
- **[MED] JARG-01-daemon-offline** — '(daemon offline?)' / 'daemon' vaza em vários toasts, contradizendo o resto do app que já fala 'ligue na aba Sistema'
  `src/hefesto_dualsense4unix/app/actions/rumble_actions.py:329`
- **[MED] RUM-02-weak-strong-vaza** — Toasts do Rumble vazam 'weak/strong/Rumble' apesar do LEIGO-06 dizer que saíram da tela
  `src/hefesto_dualsense4unix/app/actions/rumble_actions.py:326`
- **[MED] MOU-01-comandos-terminal** — Status do uinput manda o leigo rodar comandos de terminal (install_udev.sh / modprobe / pip)
  `src/hefesto_dualsense4unix/app/actions/mouse_actions.py:383`
- **[MED] COR-WAKE-02-priming-so-new-keys** — _refresh_sysfs_leds re-prima SÓ new_keys; nó já mapeado que o kernel resetou no wake (idea #16) não é re-resolvido
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py:867`
- **[MED] COR-WAKE-03-segundo-controle-sem-restore** — O 2º controle (transição 1→2) não dispara restore_last_profile nem reassert — depende só de _reapply_desired/priming
  `src/hefesto_dualsense4unix/daemon/connection.py:249`
- **[LOW] COR-WAKE-04-reapply-hidraw-nao-cola-bt** — _reapply_desired cai no pydualsense/hidraw quando o nó sysfs ainda não surgiu no instante do hotplug — e hidraw não cola no BT
  `src/hefesto_dualsense4unix/core/backend_pydualsense.py:1146`

## Backlog — não corrigidos neste passe (52)

Priorizados para a próxima sessão. Nenhum é HIGH.


### MED

- **DEDUP-02-gate-gyro-touch** (uhid_gamepad.py:690) — Gate humano de release do DEDUP-02 exige giroscópio/touchpad, que o vpad NÃO entrega
- **COR-04-override-mata-auto-playerled** (draft_config.py:188) — Override de cor por-controle da GUI é DENSO e derruba o LED de número automático (e congela brilho/player_leds) do controle editado
- **COR-01-seletor-por-posicao** (status_actions.py:271) — Seletor de alvo rotula 'Controle N' por POSIÇÃO (index+1), divergindo dos cards/CLI/applet que usam o SLOT — quebra a paridade D6 após replug
- **STATUS-num-01-card-vs-seletor** (controller_card.py:149) — Card diz "Controle 2" (player_slot) mas o seletor/badge da MESMA aba diz "Controle 1" (index+1)
- **EMU-01-toml-morto** (emulation_actions.py:144) — Botao 'Ver daemon.toml (referencia)' abre um arquivo que o daemon NAO le
- **EMU-02-diag-jargao** (emulation_actions.py:195) — Cartao UINPUT/Device/VID:PID/Gamepads e diagnostico de dev com cores de alarme que o leigo nao entende nem resolve
- **EMU-03-test-device-jargao** (emulation_actions.py:119) — Botao 'Testar criacao de device virtual' fala pip/udev/start()==False ao leigo
- **HOME-01-religar-nao-funciona-bandeja** (home_actions.py:629) — Dialogo de 'Desligar Hefesto' sugere 'feche e abra o painel' para religar, mas isso nao religa com o app na bandeja
- **EMU-06-mascara-falha-silenciosa** (home_actions.py:609) — Trocar a mascara (Xbox/DualSense) na aba Inicio pode falhar sem NENHUM aviso e o botao volta sozinho depois
- **ST-02-offline-sem-saida** (status_actions.py:757) — Hefesto que cai NO MEIO do uso mostra 'Daemon Offline' sem dizer o que fazer — o de boot é amigável
- **LB-04-voltar-automatico-sem-seletor** (lightbar_actions.py:344) — 'Voltar ao automático' manda usar um seletor que não existe na tela quando há só 1 controle
- **CARD-01-numeracao-divergente** (controller_card.py:144) — Card numera por player_slot e seletor/badge por index+1 — o MESMO controle pode virar 'Controle 1' e 'Controle 2'
- **COR-B-jogo-sem-nome-vira-sempre** (simple_match.py:38) — "Aplica a: Jogo" com o nome em branco salva como "Sempre" sem avisar
- **COR-C-auto-avancado-parede-de-jargao** (profiles_actions.py:829) — Selecionar um perfil de match complexo joga o leigo em 'Modo avançado' com window_class/title_regex/process_name
- **COR-D-pydantic-cru-no-rodape** (profiles_actions.py:575) — Erro ao salvar mostra o dump técnico do pydantic no rodapé
- **GOLD-02-steam-kill-atoa** (install.sh:1080) — Install step 11b fecha e reabre a Steam da usuária mesmo quando não há nada a migrar, sem avisar
- **GOLD-03-sandbox-veneno-fica** (steam_launch_options.py:617) — Migração RECUSA vdf de Steam Flatpak/Snap e deixa o veneno intacto; doctor manda rodar --migrate (conselho circular)
- **GOLD-04-wrapper-nunca-auto-aplicado** (steam_launch_options.py:270) — Wrapper instalado por default, mas NUNCA aplicado sozinho a nenhum jogo de quem nunca teve o veneno — leigo precisa colar por jogo

### LOW

- **VPAD-INST-01-label** (install.sh:532) — install.sh rotula a regra 71-uhid.rules como 'emulacao Xbox360 via uinput' (fix cosmetico pedido no sprint, nao feito)
- **VPAD-UX-01-banner-advice** (home_actions.py:130) — Banner de degradacao aconselha so 'reinicie o Hefesto', embora VPAD-01/02 ja recuperem por hotplug/re-selecao
- **UX0405-mecanismo-substituido** (disable_steam_input.sh:10) — UX-04 guard-strip e UX-05 dedup_validada NÃO existem como escritos — substituídos pelo wrapper (guard não desenvenena LaunchOptions continuamente)
- **install-fecha-steam-default** (install.sh:1080) — install.sh passo 11b fecha e reabre a Steam por DEFAULT (--migrate --stop-steam)
- **UX03-validacao-visual-pendente** (home_actions.py:153) — UX-03: código e testes prontos, mas o gate humano (ver o banner ao vivo) segue aberto
- **UX06-nao-implementado** (autoswitch.py:150) — UX-06 (GUI como janela neutra no autoswitch) não implementado — corretamente gateado
- **UX07-sem-go-nogo** (2026-07-16-sprint-autoswitch-e-launch-options.md:396) — UX-07 (backend zcosmic, fora do repo): sem decisão go/no-go registrada no doc
- **DEDUP-01-retry-cache-superseded** (uhid_gamepad.py:330) — DEDUP-01 (retry+cache) e o 'detectar 85 31 e substituir' do DEDUP-02 não existem — substituídos pelo canônico-sempre
- **BT02-mapping-uinput-df2** (uinput_gamepad.py:90) — BT-02 crit.2 (mapeamento SDL correto) e inverificavel por codigo; o vpad uinput degradado 054c:0df2 + version 0x3 pode cair no auto-mapping heuristico do SDL (botoes trocados)
- **BT-live-gates-07** (2026-07-16-sprint-bluetooth-vpad-mudo.md:402) — Criterios AO VIVO de BT-01/BT-02/BT-04 e o screenshot do BT-03 sao gate humano (BT-07) ainda pendente — a frente nao pode ser declarada fechada so pelo codigo
- **PERFIL-03-marker-stale-inverte-boot** (session.py:137) — Marker active_profile.txt desatualizado vence o session.json correto no restore de boot
- **PERFIL-04-apply-nao-reseta-overrides** (ipc_draft_applier.py:232) — 'Aplicar' (apply_draft) nao substitui o mapa de overrides por-uniq; override removido na GUI persiste vivo ate a proxima ativacao de perfil
- **COR-05-effective-ausente** (ipc_handlers.py:805) — COR-05 não expõe lightbar_rgb_effective e lightbar_rgb sai PÓS-brilho, não a identidade PRÉ-brilho do contrato D8
- **COR-02-apis-nomeadas-ausentes** (backend_pydualsense.py:1327) — As APIs nomeadas set_led_for/set_player_leds_for do COR-02 não existem — capacidade entregue via apply_output_for
- **STATUS-doc-02-20hz-obsoleto** (ipc_handlers.py:416) — Docstring/comentário do state_full ainda cita '20 Hz' — o sprint pediu explicitamente para não citar
- **STATUS-03-unmute-nao-registra-posse** (backend_pydualsense.py:1571) — Sair do Modo Nativo re-escreve a cor por sysfs mas NÃO chama record_sysfs_write
- **STATUS-04-deferido-nativo-travessao** (ipc_handlers.py:811) — STATUS-04 não construído: em Modo Nativo/emulação-off os cards secundários mostram "—" (por design)
- **8BIT02-no-gui-surface** (:1) — 8BIT-02 não construído: leigo não tem superfície gráfica para o 8BitDo nem para externos
- **8BIT01-cli-render-untested** (cmd_controller.py:137) — Caminho de render da CLI --external (único consumidor vivo do 8BIT-01) sem teste
- **8BIT01-dedup-key-lower-vs-normmac** (evdev_reader.py:304) — Dedup do inventário externo usa .lower() em vez de norm_mac (mais fraco que o caminho DualSense)
- **8BIT04-no-respingo-test-and-xref** (2026-07-16-sprint-8bitdo-e-outros-controles.md:294) — 8BIT-04: teste de não-respingo ausente (re-escopado SEM OBJETO) e requisitos sem cross-ref na frente DEDUP
- **EMU-05-excecao-crua-toast** (emulation_actions.py:455) — Toasts de falha vazam o texto cru da excecao Python para o leigo
- **EMU-07-modo-jogo-mente-no-nativo** (emulation_actions.py:352) — 'Modo jogo' fica clicavel no modo 'Jogar direto (Sony)' e o toast afirma 'gamepad ativo' quando nao ha gamepad
- **EMU-08-passthrough-fixo** (emulation_actions.py:60) — 'Passthrough em emulacao: Nao' e um valor fixo que nunca atualiza (status que pode mentir) e usa jargao
- **EMU-09-vocab-duplicado** (emulation_actions.py:461) — A aba Emulacao repete a troca de modo da Inicio com OUTRAS palavras (Desligado/DualSense/Xbox vs Controlar o PC/Jogar pelo Hefesto), e o nome 'Emulacao' e jargao
- **LB-03-player-leds-cripto** (lightbar_actions.py:457) — Confirmação dos LEDs de Jogador é críptica: 'Player LEDs: x - - - -'
- **ST-03-bt-abreviacao** (status_actions.py:736) — 'BT' abreviado no header, cards e seletor pode não ser óbvio para o leigo total
- **ST-04-conexao-daemon-redundante** (status_actions.py:830) — Frame 'Estado' mostra 'Conexão' e 'Daemon' como duas linhas que dizem quase a mesma coisa
- **UX-E-preview-json-cru** (profiles_actions.py:677) — O painel 'Detalhes técnicos' mostra JSON cru sempre visível
- **UX-F-novo-perfil-underscore** (profiles_actions.py:472) — Perfil novo nasce chamado 'novo_perfil' (com underline)
- **UX-G-mascara-xbox-default** (profiles_actions.py:282) — 'Jogar pelo Hefesto' já vem com máscara 'Xbox 360' — leigo com DualSense vê botões de Xbox
- **TRG-02-preset-off-ingles** (main.glade:363) — Rótulos fixos 'Preset:' e 'Desligar (Off)' expõem inglês na aba Gatilhos
- **KBD-02-add-sem-escolha** (input_actions.py:156) — 'Adicionar' na aba Teclado cria binding silencioso num botão aleatório com 'KEY_SPACE'
- **GOLD-05-nonnative-pula-defaults** (install.sh:372) — Formatos flatpak/appimage/deb dão exit 0 antes de wrapper+mic WP-51+Steam-Input+migração — defaults só valem no native
