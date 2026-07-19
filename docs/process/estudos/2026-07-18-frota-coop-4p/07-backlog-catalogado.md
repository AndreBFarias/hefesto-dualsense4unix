# Agente: v2:23bad62146d666212459564b18a61086a1332e6d6804adcdf238cdbbdb42849a

## report

# BACKLOG COMPLETO — hefesto-dualsense4unix (compilado 2026-07-18, branch sprint/harmonia-uhid, HEAD 62483b2)

## A. AUDITORIA DA ONDA (17/07): 69 achados — o que sobrou

Fonte canônica: `docs/process/sprints/2026-07-17-AUDITORIA-onda-validacao-e-correcoes.md` (28 agentes; 6 HIGH + 28 MED + 35 LOW). Aritmética de fechamento: 17 corrigidos no 1º passe (commit 6f1988f — TODOS os 6 HIGH + 11 MED/LOW de jargão), 41 dos 52 do backlog corrigidos no 2º passe (commit ffe1c27 — "52 MED/LOW; 41 acionáveis por código"). **Restam ~11 itens**, os NÃO acionáveis por código/gateados/decisões. Os certamente ainda ABERTOS (verificados contra os commits e o código atual):

1. **DEDUP-02-gate-gyro-touch** — o gate humano de release do DEDUP-02 exige giroscópio/touchpad que o vpad NÃO entrega (nós existem, dados não fluem) — `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:690` — **P1** (é também a raiz do ruído js2/js4/js6 do P6 de hoje) — ABERTO.
2. **UX03-validacao-visual-pendente** — banner de degradação: código+testes prontos, gate humano de ver ao vivo aberto — `app/actions/home_actions.py:153` — P2 — ABERTO (gate).
3. **UX06-nao-implementado** — GUI como janela neutra no autoswitch, aguarda OK de produto — `daemon/autoswitch.py:150` — P2 — ABERTO (decisão dela).
4. **UX07-sem-go-nogo** — backend zcosmic p/ detecção de janela no COSMIC: sem decisão registrada — `2026-07-16-sprint-autoswitch-e-launch-options.md:396` — P2 — ABERTO (decisão).
5. **BT-live-gates-07** — critérios AO VIVO de BT-01/02/04 + screenshot BT-03 = gate humano BT-07 pendente — `2026-07-16-sprint-bluetooth-vpad-mudo.md:402` — **P0** (gate de entrega da frente dedup/BT) — ABERTO.
6. **BT02-mapping-uinput-df2** — vpad uinput degradado 054c:0df2 + version 0x3 pode cair no auto-mapping heurístico do SDL (botões trocados) — `integrations/uinput_gamepad.py:90` — P1 — ABERTO (inverificável por código).
7. **GOLD-04-wrapper-nunca-auto-aplicado** — wrapper instalado por default mas nunca aplicado sozinho por jogo; hoje há o diálogo 1x/jogo + botão "Aplicar aos jogos da Steam" (aba Sistema), mas nada automático — `integrations/steam_launch_options.py:270` — **P0** (é exatamente o P2 de hoje: plug direto = controle duplicado) — PARCIAL.
8. **GOLD-03-sandbox-veneno-fica** — migração recusa vdf de Steam Flatpak/Snap e deixa o veneno; doctor dá conselho circular — `steam_launch_options.py:617` — P1 — ABERTO (na máquina dela é Steam nativa, sem impacto local).
9. **STATUS-04-deferido-nativo-travessao** — cards secundários mostram "—" em Modo Nativo (por design, não construído) — `daemon/ipc_handlers.py:811` — P2 — DEFERIDO.
10. **COR-02-apis-nomeadas-ausentes** — set_led_for/set_player_leds_for não existem (capacidade via apply_output_for) — `core/backend_pydualsense.py:1327` — P2 — DEFERIDO (design).
11. **UX0405/DEDUP-01-superseded** — notas de doc: guard não desenvenena LaunchOptions continuamente; retry+cache substituídos pelo canônico-sempre — `disable_steam_input.sh:10`, `uhid_gamepad.py:330` — P2 — REGISTRO.
12. **COR-04-override-mata-auto-playerled** — override de cor por-controle derruba o LED automático de número e congela brilho (draft_config foi tocado em ffe1c27, mas o comportamento denso segue documentado) — `app/draft_config.py:188` — P1 — PROVAVELMENTE PARCIAL (**candidato à raiz do P1 de hoje: dois escritores de LED alternando**).
13. **COR-05-effective-ausente** — `lightbar_rgb_effective` não exposto; `lightbar_rgb` sai pós-brilho — `daemon/ipc_handlers.py:805` — P2 — status incerto (backend tocado em ffe1c27).
14. **STATUS-03-unmute-nao-registra-posse** — sair do Nativo re-escreve cor por sysfs sem `record_sysfs_write` (dono-da-escrita fica errado) — `core/backend_pydualsense.py:1571` — P1 — status incerto (**também candidato ao race de LED do P1**).
15. **8BIT01-cli-render-untested / 8BIT01-dedup-key-lower / 8BIT04-no-respingo** — testes ausentes do inventário externo — `cli/cmd_controller.py:137`, `core/evdev_reader.py:304`, doc 8BitDo:294 — P2 — ABERTOS (evdev_reader tocado em ffe1c27, conferir).
16. **8BIT02-no-gui-surface** — SUPERSEDED: 8BIT-02 foi construído em 17/07 (commits 832fc22, 9532eb1, d4c5874, e855f0d).

Nota: os 41 de ffe1c27 cobriram EMU-01..09, HOME-01, ST-02/03/04, LB-03/04, CARD-01/STATUS-num-01/COR-01-seletor (numeração unificada por player_slot), COR-B/C/D, UX-E/F/G, TRG-02, KBD-02, GOLD-02, VPAD-INST-01, PERFIL-03/04 (arquivos ipc_draft_applier/install.sh/main.glade tocados). Para lista exata item-a-item seria preciso diffar cada linha (open question).

## B. GATES HUMANOS PENDENTES (seguram release — a mantenedora é o gate)

Fontes: `~/LEIA-DE-MANHA.md`, `CHECKLIST_MANUAL.md:94-145`, `docs/process/estudos/2026-07-18-estudo-lightbar-bt-adocao.md:83-86`, `2026-07-16-INDICE-onda-multicontrole-e-dedup.md` §6.

1. **Lightbar pós-power-off** — power-off dos 2 DualSense + reconectar + lightbars PERMANECEREM acesas após adoção (aceite do fix Reset-0x08, 62483b2) — **P0, DESTRAVA O RELEASE** — ABERTO (ela está jogando hoje; P1 relatado sugere regressão parcial no USB).
2. **Rumble + layout PS num jogo real com máscara DualSense** — a pendência que segura o release da onda Harmonia desde 15/07 — **P0** — ABERTO (P1 de hoje = rumble NÃO chega no físico do vpad P1: o gate está REPROVANDO).
3. **BT-07** — matriz Sackboy (desenvenenado) + RDR2 por BT, máscaras DualSense E Xbox, com journal — **P0** — ABERTO; inclui a **investigação da 2ª causa do RDR2** (candidatos ordenados no sprint BT linhas 402+: PSSupport temporário, dedup interno SDL vpad-evdev × físico-HIDAPI, CRC fails do rádio).
4. **Wrapper no Sackboy** — colar `hefesto-launch %command%` e ver o 8BitDo entrar como 3º jogador — P0 — ABERTO (`~/LEIA-DE-MANHA.md` item 3).
5. **COR-07 / STATUS-05 / PERFIL-05(a,c,d)** — roteiros no `CHECKLIST_MANUAL.md:99-131` — P1 — ABERTOS.
6. **Diálogo do wrapper 1x/jogo** (o "task #7") — CONSTRUÍDO em 17006f2 (`app/actions/launch_wrapper_dialog.py`), gate humano no `CHECKLIST_MANUAL.md:133-138` ABERTO; e o P5 de hoje (fundo claro) é bug REAL nele: `launch_wrapper_dialog.py:357-365` cria `Gtk.MessageDialog` SEM a classe CSS `hefesto-dualsense4unix-window` — o fix de tema do 9532eb1 só foi aplicado em `app/gui_dialogs.py:249` (ficha do externo) — **P1, fix de 1 linha**.
7. **8BIT-05** — decisão de modo do 8BitDo (cabo-Switch estável × X-input × Steam Input off), custo zero de código — P1 — ABERTA desde 16/07.
8. **Rótulo "8BitDo 3 · BT"** no seletor com ele em BT — P2 — ABERTO.
9. **VPAD-07/DEDUP-02 célula gyro+touchpad** — bloqueado pelo item A.1 (vpad não entrega IMU/touch) — P1 — ABERTO.

## C. MAPEAMENTO DOS PROBLEMAS DE HOJE (P1-P6) → catálogo

- **P1 (rumble não chega no branco USB + lightbar verde-limãoazul)**: NÃO catalogado como está; adjacências: A.12 (COR-04 override×auto), A.14 (STATUS-03 posse da escrita), ideia-morta #16 do INDICE (priming multi_intensity), telemetria `sysfs_led_cobertura`/`lightbar_reset_enviado` agora em INFO no journal (usar!). Verde = cor da paleta do slot 3 (`1=azul,2=vermelho,3=verde` — CHANGELOG 3.14.0): forte indício de que a numeração global com externos (external_slot do d4c5874/9532eb1) contaminou o slot de COR do DualSense — o branco deveria ser azul (slot 1) e algo o pinta de verde (slot 3 = o Pro Controller hoje é LED 3). Rumble: fan-out do co-op (`daemon/subsystems/gamepad.py:184,251`) e rota FF do vpad P1 → físico USB; catalogado que rumble funciona nas 2 máscaras de vpad (memória UHID-04), então é regressão/rota nova.
- **P2 (duplicado sem hefesto/wrapper)**: CONHECIDO E ACEITO POR DESIGN — "o pior caso pós-install passa a ser controle duplicado, nunca zero controles" (`2026-07-16-INDICE` §2.4 e ideia-morta #20); item aberto correspondente = A.7 (GOLD-04). LEIA-DE-MANHA item 3 documenta exatamente isso no Sackboy.
- **P3 (8BitDo LED 2 × jogo vê player 1)**: CONHECIDO — CHECKLIST COR-07 linha 109-112 ("número do controle ≠ número do jogador — documentado, não é reprovação") + ideia-morta #17 (separar slot de exibição do índice de alocação) + memória 17/07 ("falta ela tocar o PS dos DualSense p/ virarem 1+2 e o 8BitDo auto-virar 3" — o daemon numera por sessão, a Steam/SDL enumera por ordem de aparição). Gap de produto real: nada sincroniza o slot do daemon com a ordem SDL.
- **P4 (sem dropdown de modo na ficha do externo)**: O DROPDOWN NUNCA EXISTIU — o 9532eb1 construiu DETECÇÃO + ORIENTAÇÃO read-only ("O jogo vê como: Nintendo (modo Switch)" + texto), porque o modo é de HARDWARE (combo ao ligar), não toggle de software (`app/actions/external_controllers.py:196-244`, linha exibida em `detail_rows` :257-259; popup em `app/gui_dialogs.py:221-`). Se a linha nem aparece, suspeitar de `entry["vid"]` ausente no inventário (`input_mode` exige vid=057e/045e ou driver) — `app/actions/status_actions.py:455` monta o inventário.
- **P5 (diálogo do wrapper claro)**: bug real não catalogado — ver B.6.
- **P6 (Motion Sensors viram js2/js4/js6)**: PARCIALMENTE catalogado — regra `assets/78-dualsense-motion-not-joystick.rules` existe (do estudo 2026-07-13 linha 324) mas (a) casa por `ATTRS{name}` dos controles FÍSICOS Sony — o vpad chama-se "Hefesto Virtual DualSense P{N}" (`integrations/uhid_gamepad.py:479`), o nó Motion dele ESCAPA da regra; (b) `ID_INPUT_JOYSTICK=""` não impede o joydev de criar `/dev/input/js*` — só limpa a propriedade p/ SDL/evdev; jogos que leem js* cru continuam vendo o ruído. Item W1.3 do plano 07-13 nunca teve a parte "esconder js* dos jogos" completada (a udev-central foi REFUTADA no INDICE §2.1, mas a variante Motion-Sensors é o caso coadjuvante permitido).

## D. INVESTIGAÇÕES/DECISÕES ABERTAS

1. **2ª causa RDR2 nativo+BT** — em aberto desde o Estudo 1; candidato forte: DualSense BT invisível ao SDL quando gêmeo USB de mesmo VID/PID está no HIDAPI (`INDICE` §1 "parte honesta") — **P0** (é o BT-07).
2. **Morte do 8BitDo/Pro Controller por BT** — muro de kernel PROVADO (hid-nintendo; sem cura por patch — investigação de 10+5 agentes, LEIA-DE-MANHA item 4); mitigação = cabo/X-input; assinatura curta fica abaixo do threshold do doctor (decisão deliberada, `2026-07-16-sprint-8bitdo`:7-20) — REGISTRO.
3. **Clone DS4 054C:05C4 em BT** — storm de 211k CRC fails degradando o adaptador p/ todos (estudo 18/07, "armadilhas") — suspeito permanente de instabilidade BT — P1 (vigiar).
4. **Broker root / esconder físico sem env** — limitação registrada, outra onda (`INDICE` §2.4) — P2.
5. **OKs de produto pendentes** (INDICE §6.7): NÃO ao popup automático da launch option; UX-06; retenção de perfil no autoswitch por cima do autoload — decisões dela.

## E. LIMITAÇÕES/DÍVIDAS DE INFRA CATALOGADAS

1. **Doctor WARNs conhecidos**: hidraw0-3 em 0666 (receivers 2.4G, ajuste manual antigo, fora de escopo) + detector de janela DEGRADADO no cosmic-comp (`2026-07-17-CHECKPOINT`:27-29) — P2.
2. **5 dropdowns restantes** (gatilhos/perfil) sujeitos ao bug de foco do cosmic-comp (cosmic-epoch#2497); seletor principal já virou botões segmentados — P2.
3. **Testes de GUI exigem gi/cairo completos** — CI headless pula (4097483); custou 4 rounds do release 3.14.0 — P2 (armadilha de processo).
4. **Dívida de acentuação** ~50 violações antigas + 2 pré-existentes documentadas — P2.
5. **Sudo do install exige TTY real** (headless pula passos root) — P2, documentado.
6. **Autoswitch × XWayland**: janela "unknown" tratada por histerese (curado), mas GUI-como-janela-neutra (UX-06) segue aberto — P2.
7. **CHANGELOG [Unreleased]** contém todo o bloco 8BIT-02/lightbar-reset ainda não versionado — release segurado pelo gate B.1/B.2.

## F. FASES 4-6 E TASK #7 (rastreabilidade pedida)

- Onda de 16/07 planejou 8 sprints/50 itens/29 P0; Fases 1-3 = bc68718/f2e2aad/8e59601; a decisão "Fases 4-6 adiadas" caiu em 17/07: **Fase 4** (cores automáticas + cards + diálogo do wrapper = task #7 APROVADO "GTK dialog, nunca popover; dispensou → não insiste") e **Fase 5** (8BitDo) construídas em 17006f2; **"Fase 6"** = ciclo install SEM FLAGS (RODADO 17/07) + validação humana (= os gates da seção B, TODOS abertos). Task #7 está construído com bug de tema (P5) e gate humano aberto.
- Do sprint 8BitDo: 8BIT-01/03/06 construídos; 8BIT-02 construído em 17/07 (4 commits); 8BIT-04 item 1 SEM OBJETO; 8BIT-05 humano ABERTO (doc `2026-07-16-sprint-8bitdo`:7-20).
- Da onda Harmonia (15/07): as 8 pendências dos revisores foram fechadas em 8d00138; sprints ESTETICA/INFRA materializados (cd9463d) — itens residuais absorvidos pela onda 16/07; matriz de paridade (2026-07-13/14) curada pelo uhid EXCETO gyro/touchpad do vpad (A.1).

## key_files

- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-17-AUDITORIA-onda-validacao-e-correcoes.md:44-105 — Fonte canônica dos 69 achados: 17 corrigidos listados (linhas 5-42) + backlog de 52 com file:line cada (linhas 44-105); cruzar com ffe1c27 para saber os ~11 restantes
- /home/vitoriamaria/LEIA-DE-MANHA.md:29-71 — Pendências que dependem da mantenedora HOJE: teste das lightbars (destrava release), wrapper no Sackboy, rótulo 8BitDo BT
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-16-INDICE-onda-multicontrole-e-dedup.md:179-318 — Mapa da onda: causa-raiz BT, veredito dedup, validação humana pendente (§6), 20 ideias mortas que NÃO devem ser reconstruídas (§7), regra de ouro install-sem-flags (§8)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/CHECKLIST_MANUAL.md:94-145 — Roteiro dos gates humanos abertos: COR-07, STATUS-05, PERFIL-05, diálogo do wrapper 1x/jogo, 8BIT-05
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/estudos/2026-07-18-estudo-lightbar-bt-adocao.md:77-96 — Causa-raiz da lightbar BT (adoção derruba o claim) + cura Reset-0x08 + gate humano pendente + armadilhas (cards da GUI não provam lightbar física; clone DS4 05C4 storm)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/launch_wrapper_dialog.py:357-365 — P5: _build_wrapper_dialog cria Gtk.MessageDialog SEM a classe CSS hefesto-dualsense4unix-window — por isso o popup abre claro; fix de tema do 9532eb1 só cobriu gui_dialogs.py:249
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/app/actions/external_controllers.py:196-259 — P4: o 'modo Nintendo vs Xbox' é linha read-only ('O jogo vê como') via input_mode/mode_guidance — dropdown nunca existiu (modo é hardware); linha some se entry['vid'] faltar no inventário
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/assets/78-dualsense-motion-not-joystick.rules:11-12 — P6: regra casa só ATTRS{name} dos DualSense FÍSICOS — o Motion do vpad 'Hefesto Virtual DualSense P{N}' (uhid_gamepad.py:479) escapa; e ID_INPUT_JOYSTICK vazio não impede joydev de criar jsN
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:479, 690 — Nome do vpad (linha 479) que escapa da regra 78; linha 690 = gate DEDUP-02 exige gyro/touchpad que o vpad não entrega (item aberto A.1)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/steam_launch_options.py:270, 617 — GOLD-04 (wrapper nunca auto-aplicado — raiz do P2 duplicado sem hefesto) e GOLD-03 (Flatpak/Snap vdf recusado)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-16-sprint-bluetooth-vpad-mudo.md:390-420 — BT-07 gate humano P0 + plano da investigação da 2ª causa do RDR2 (candidatos ordenados)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-16-sprint-8bitdo-e-outros-controles.md:7-20 — Status vivo da frente 8BitDo (header linhas 7-20): 8BIT-05 aberto, 8BIT-04 sem objeto, validação positiva do inventário pendente
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-17-CHECKPOINT-fases-4-5-construidas.md:22-75 — Estado das Fases 4-5, WARNs conhecidos do doctor (hidraw 0666, detector degradado), gates a validar
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/CHANGELOG.md:7-40 — [Unreleased] = 8BIT-02 completo + numeração externa sincronizada; paleta 1=azul/2=vermelho/3=verde (evidência p/ hipótese do verde-limão do P1)
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:184, 251 — Rotas de FF/rumble do co-op (fan-out linha 184; regra da máscara dualsense linha 251) — ponto de partida do P1 rumble-não-chega
- /home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-07-13-estudo-ui-ux-multicontrole-coexistencia.md:188-193, 318-330 — Catálogo original do ruído js0-js5/Motion Sensors expostos ao jogo (linhas 188-193, 324) — o plano W1.3 nunca completou a parte joydev

## hypotheses

- P1-lightbar verde-limãoazul: a numeração global com externos (external_slot, commits d4c5874/9532eb1) contaminou o slot de COR do DualSense branco — verde é exatamente a cor do slot 3 da paleta (CHANGELOG 3.14.0) e o Pro Controller hoje ocupa o LED 3; a alternância com azul é race entre dois escritores de LED já catalogado como risco (COR-04 override×auto em draft_config.py:188 + STATUS-03 posse-da-escrita em backend_pydualsense.py:1571 + reassert_resolved_outputs de 8d824a6); o journal novo tem sysfs_led_cobertura/lightbar_reset_enviado com timestamps para cravar o escritor.
- P2-duplicado sem hefesto: comportamento DOCUMENTADO por design ('pior caso é duplicado, nunca zero' — INDICE §2.4/ideia-morta #20); a lacuna aberta correspondente é GOLD-04 (steam_launch_options.py:270): o wrapper nunca é auto-aplicado por jogo — sem hefesto-launch nas opções, físico js1 e vpad js3 ficam ambos visíveis ao SDL.
- P3-8BitDo LED 2 vs jogo player 1: gap catalogado 'número do controle ≠ número do jogador' (CHECKLIST COR-07:109-112 + ideia-morta #17): o daemon numera por sessão/MAC e escreve o LED, mas a Steam/SDL enumera por ordem de aparição dos devices — nada sincroniza os dois; com os DualSense dormindo em BT no boot, o 8BitDo é enumerado primeiro e vira player 1 do jogo (memória 17/07 previu exatamente isso).
- P4-dropdown ausente: o dropdown NUNCA foi construído — 9532eb1 entregou detecção read-only + orientação ('O jogo vê como: ...') porque o modo é de HARDWARE (combo ao ligar), não toggle (external_controllers.py:196-244); se nem a linha de texto aparece na ficha, a causa provável é entry['vid'] ausente/vazio no inventário externo montado em status_actions.py:455 (input_mode exige vid 057e/045e ou driver hid-nintendo).
- P5-popup claro: launch_wrapper_dialog.py:357-365 cria Gtk.MessageDialog sem add_class('hefesto-dualsense4unix-window') — o fix de tema do 9532eb1 foi aplicado só em gui_dialogs.py:249 (ficha do externo); no COSMIC o diálogo herda o claro do sistema. Fix de 1 linha.
- P6-Motion viram jsN: a regra 78 existe mas casa ATTRS{name} só dos DualSense FÍSICOS Sony — o nó Motion do vpad 'Hefesto Virtual DualSense P{N}' (uhid_gamepad.py:479) escapa dela; e ID_INPUT_JOYSTICK='' não impede o joydev de criar /dev/input/js* (só limpa a propriedade p/ SDL/evdev) — jogos que enumeram js* cru continuam vendo o ruído; relacionado ao item aberto DEDUP-02-gate-gyro-touch (o vpad expõe nós de IMU sem dados).

## open_questions

- Quais EXATAMENTE são os 11 itens do backlog de 52 que ffe1c27 NÃO cobriu — exige diff item-a-item (o commit diz '41 acionáveis por código' mas não enumera); em particular COR-05, STATUS-03, STATUS-doc-02 e PERFIL-03/04 têm arquivos tocados mas fechamento não confirmado.
- O inventário externo (status_actions.py:455 / controller.list) entrega o campo 'vid' para o Pro Controller USB? Se não, a linha 'O jogo vê como' do P4 nunca renderiza — checar o payload IPC real com o daemon vivo.
- Quem escreve o verde-limão no branco USB: conferir no journal ao vivo sysfs_led_cobertura + record_sysfs_write vs external_slot/player_slot atribuídos aos 4 controles conectados AGORA (o mapeamento MAC→slot da sessão atual).
- O rumble do P1 (branco USB): o jogo está rodando COM ou SEM o wrapper hefesto-launch? Sem ele o FF pode estar indo para o físico duplicado ou para o vpad sem rota — a matriz do BT-07 nunca foi executada.
- O botão 'Aplicar aos jogos da Steam' (aba Sistema, citado no LEIA-DE-MANHA) cobre o GOLD-04 por completo ou só migra jogos já envenenados? (steam_launch_options.py:270).
- A decisão 'Fases 4-6 adiadas' da memória: confirmar que 'Fase 6' = validação humana + ciclo install (não há doc com esse nome; o checkpoint 16/07 lista 4 itens de próxima sessão, dos quais só a validação humana resta).
