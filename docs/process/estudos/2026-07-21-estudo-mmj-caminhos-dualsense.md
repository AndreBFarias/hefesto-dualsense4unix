# Estudo 2026-07-21 — Mullet Mad Jack: por que o vpad DualSense é invisível e o mapa real dos 3 caminhos

**Contexto**: pós-reboot da leva de 21/07, controle "morto" no Mullet Mad Jack (AppID 2111190)
com máscara dualsense; funciona com máscara xbox. Estudo de 7 agentes (4 leitores: história do
repo, código dos modos, wine/Proton, InControl; 3 revisores adversariais das propostas A/B/C).
Dados brutos: journal do workflow `wf_ee8def43-ee4` (sessão 950f8939).

## Fatos medidos na sessão (não re-derivar)

- Kernel INOCENTE: vpad uhid bindou no driver `playstation` (0003:054C:0DF2), criou
  hidraw4 + event21 (pad) + event22 (motion 67 Hz) + touchpad + js0. Pipeline
  físico→daemon→vpad PROVADO: 1017 eventos KEY/ABS no event21 sob toque manual.
- Wrapper hefesto-launch APLICADO (66 jogos): o MMJ lançou com ele nas duas tentativas
  (logs da Steam 20:31 e 20:41), com Proton pinado GE-Proton10-34 e env correto
  (`PROTON_DISABLE_HIDRAW=0x054C/0x0CE6`, `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`).
- `winedevice.exe` abriu o hidraw4 do vpad → o device CHEGA ao Windows-side. Com máscara
  dualsense o jogo ignora; com xbox funciona. O elo defeituoso é RECONHECIMENTO, não transporte.
- Binários do MMJ: Unity IL2CPP + **InControl** (perfis nativos Windows por VID/PID:
  `PlayStation5USBWindowsNativeProfile`/`PlayStation5BluetoothWindowsNativeProfile` = 054C:0CE6;
  **nenhum perfil Edge 0DF2**) + **XInputDotNet** (`XInputInterface64.dll`) + **Steamworks
  Steam Input** (inclusive `SteamAPI_ISteamInput_SetDualSenseTriggerEffect`).
- Bônus: `calibration_read_failed EIO` (feature 0x05 via broker) ao recriar o vpad com o
  físico em BT → vpad nasce sem calibração → drift de gyro esperado até nova cura.

## Causa-raiz por caminho

1. **"Sony direto"** (físico visível ao jogo): morto porque NÓS o escondemos — broker
   (chmod 0600 no hidraw) + envs. Não é bug: é o dedup/guerra de escritores funcionando.
   O jogo reconheceria o físico 0CE6 (perfil InControl PS5). Modo Nativo já entrega o
   mecanismo (restore do broker + zero envs + grab solto).
2. **"DualSense via hefesto"** (vpad): o vpad é DualSense **Edge 0DF2** por decisão UHID-04
   (o esconderijo por VID/PID 0x0CE6 não pode engolir o vpad junto). O InControl **não
   conhece 0DF2 em NENHUMA versão** (nem a v1.8.10 atual) → "Unknown Device" → jogo mudo.
   CAUSA-RAIZ CONFIRMADA. O mesmo vale para qualquer jogo que reconheça DualSense por
   lista de PID (Unity InputSystem antigo, engines caseiras).
3. **Xbox**: XInput funciona sempre (XInputDotNet). **Nenhuma config de winebus faz um PID
   Sony virar XInput** — em jogo XInput-only, a máscara xbox é a solução arquiteturalmente
   correta (é o que DS4Windows faz no Windows), não gambiarra.

**"Os 3 funcionavam antes"**: o suporte DualSense oficial do MMJ é via **Steam Input**
(o dev chama `SetDualSenseTriggerEffect` da API da Steam). Com PSSupport ligado (era o
estado até o desvenenamento), a Steam traduzia qualquer caminho.

**CORREÇÃO da mantenedora (21/07 21h)**: a máscara dualsense FOI validada ao vivo em
jogo real — **Sackboy, Mad King Redemption e Pragmata** (testemunho direto; a Steam
exibe o badge "DUALSENSE CONTROLLER" com o vpad ativo). O que o estudo detectou é uma
LACUNA DE REGISTRO: nenhum doc materializou essas validações (o único registro escrito,
Sackboy 16/07, saiu em interface XBOX). Conclusão ajustada: o caminho vpad-Edge
funciona nos jogos que falam DualSense HID de verdade (SDL moderno etc.); ele falha em
jogos PID-list/XInput-only como o MMJ. A matriz escrita de 7 células segue pendente de
materialização.

## Teto físico de cada caminho NESTE jogo (honestidade)

| Caminho | Input | Vibração | Gyro | Gatilhos adaptativos |
|---|---|---|---|---|
| Sony direto (InControl PS5, **USB only**) | sim | **não** (InControl/DirectInput sem rumble) | **não** (perfil não mapeia) | não |
| vpad dualsense-classic 0CE6 (hipotético) | sim | **não** (idem) | **não** (idem) | não |
| vpad xbox (XInput) | sim | **sim** | não (XInput não transporta gyro) | não |
| Steam Input por jogo (caminho do dev) | sim | sim | sim (config) | **sim** (`SetDualSenseTriggerEffect`) |

Em BT, o caminho "Sony direto" é quebrado POR CONSTRUÇÃO para jogos DirectInput: o
físico em modo BT entrega report 0x31 e o dinput do Wine fica cego (plataforma, não
hefesto). USB-first obrigatório nesse modo.

## Vereditos adversariais (A/B/C — todos "viável com ressalvas")

**A — flavor "dualsense-classic" (vpad 0CE6, opt-in por jogo)**
- BLOQUEANTE como está: `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` mataria o hidraw do PRÓPRIO
  vpad (match por vid/pid, sem serial). Exigiria env por-jogo SEM o 0CE6, confiando só no
  broker — que tem furos documentados (fd aberto antes do hide sobrevive; nó renasce
  visível no replug/wake BT até a reconciliação; Protons ≤9).
- Payoff modesto no caso motivador: mesmo reconhecido, o MMJ dá SÓ input básico (sem
  rumble/gyro via InControl). Vale para jogos que falam HID DualSense de verdade.
- Médios: regra udev uaccess pina KERNELS 0DF2; troca por-jogo exige recriar o vpad
  (unplug/replug na largada); ~17 testes + invariante VPAD-06 pinam 0DF2.

**B — modo nativo por jogo ("sony direto" via perfil `window_class` + `mode.kind=native`)**
- A infra JÁ EXISTE (perfil por jogo + autoswitch + compose_env zera envs + broker restore).
- Ressalvas: USB-first (BT cego por construção); antecipar a revelação no LAUNCH via
  wrapper (hoje só no foco → winedevice enumera sem o Sony e depende do rescan IN_ATTRIB);
  nativo é GLOBAL (mata vpads do co-op inteiro ao focar); restart do daemon durante
  nativo-por-perfil deixa preso no nativo (persistência assimétrica `_native_mode` vs
  `_mode_from_profile`).
- Guerra de escritores neste jogo: descartada (InControl não escreve no device).

**C — Steam Input por jogo, opt-in (caminho oficial do dev p/ DualSense no MMJ)**
- BLOQUEANTE operacional: o NOSSO `hefesto-steam-input-guard` reverte o opt-in per-app
  (`UseSteamControllerConfig` no bloco apps/<appid>) silenciosamente.
- Não verificado: per-app forced-on com `SteamController_PSSupport=0` global reivindica
  um DualSense? **Teste manual de 10 min** decide: pausar o guard
  (`systemctl --user stop hefesto-steam-input-guard.{path,timer}`), ligar Steam Input
  só no MMJ pela GUI da Steam, `lsof` no hidraw4 + jogo responde?
- A favor: o vpad é DualSense completo p/ o SDL/hidapi da Steam (responde GET_REPORT
  0x05/0x09/0x20, motion espelhado com timestamps reais); uhid_replica arbitra a Steam
  como escritora por construção; físico segue escondido (sem duplicado hidraw).

## Recomendação em degraus

1. **HOJE, sem código** (escolha da mantenedora):
   a. Vibração sem Steam Input no MMJ ⇒ perfil por jogo `window_class=steam_app_2111190`
      + `gamepad_flavor=xbox` (única via com rumble sem Steam Input neste jogo); ou
   b. Pacote completo (gyro+vibração+gatilhos) ⇒ teste C-0 de 10 min (guard pausado +
      Steam Input per-app na GUI). Se aprovar, formalizar allowlist per-app no guard.
2. **Sprint curto**: flavor por jogo automático (a infra `gamepad_flavor` por perfil já
   existe) + doc de decisão por título ("que língua este jogo fala?": XInput-only /
   PID-list / HID moderno / Steam Input).
3. **Sprint médio (cura de raiz do caminho 2)**: máscara `dualsense-classic` 0CE6 opt-in
   por jogo com env por-app sem 0CE6 (broker como defesa única nesse modo) — só para
   jogos que leem HID DualSense de verdade; mitigar os furos do broker na borda
   replug/wake antes.
4. **Pendências que o estudo expôs**: (i) validar a matriz Sackboy/RDR2 (nunca executada);
   (ii) cura do `calibration_read_failed` EIO em BT — re-ler a 0x05 na borda de conexão
   do físico (onde `upgrade_primary_vpad_to_uhid` já roda) e re-carimbar o vpad;
   (iii) persistência assimétrica do nativo-por-perfil (item B).

## Becos sem saída (não repetir)

- "Resolver no kernel": o kernel entrega o vpad perfeito; nenhum patch de kernel faz um
  jogo XInput-only ou PID-list reconhecer 0DF2.
- Fazer winebus expor PID Sony como XInput: não existe; a lista xbox-like do wine não
  inclui 054C e não é configurável.
- Remover as envs "porque o broker já esconde": decisão documentada em contrário
  (2026-07-20-desenho-onda-s-broker-fd-injection.md:53-58 — defesa em profundidade;
  broker não cobre fd pré-hide nem Protons ≤9).
- InControl reconhecer o Edge "numa versão mais nova": não existe perfil 0DF2 nem na
  v1.8.10 (mais recente).

---

## Adendo 21/07 noite — sessão 4 controles BT (Sackboy) e as curas de raiz

Fatos medidos com os 4 controles conectados (2 DualSense + Pro Controller
Nintendo + 8BitDo, todos BT):

1. **Morte do Pro Controller real no probe (kernel, linha exata)**: às
   20:25:24, no probe da conexão do boot, `Failed to set players LEDs,
   skipping registration; ret=-110` → 13× `timeout waiting for input
   report` → 2× `joycon_enforce_subcmd_rate: exceeded max attempts`. O
   rádio estava congestionado (IMU do Pro dropando 30–40% dos reports;
   BlueZ logou `Unexpected start frame`). Consequências: o controle ficou
   SEM LEDs de player pela conexão inteira (o vanilla pula o registro) e
   mais tarde sem evdev (morto p/ jogos). A Onda T (retry de probe) não
   cobria esses dois furos.
   **Curas**: patch `0002` do DKMS (registra LEDs mesmo com SET inicial
   falho, opt-in `register_leds_on_set_failure`) + tuning persistido no
   modprobe.d (`sync_send_tries=4`, `input_report_wait_ms=500`,
   `probe_info_timeout_ms=4000`) — decisão da mantenedora: kernel liberado
   via install sem flag; supersede o "só a cura, nada de tuning" da Onda T.
2. **"Switch fantasma" no Sackboy: NÃO houve**. O autoswitch ativou o
   perfil `sackboy_nativo` (21:38:32), que é `mode.kind=gamepad`,
   `flavor=dualsense`, `coop=true` — emulação Hefesto ativa (`native=False`,
   2 vpads uhid). "Nativo" no NOME refere-se aos GATILHOS (`triggers: Off`
   = o jogo manda). Evidência de que o jogo fala com os vpads: 21:38:45
   `uhid_replica trigger_left/right` players 1 e 2 — os efeitos de gatilho
   adaptativos do Sackboy chegando. Item de UX aberto: o nome do perfil
   confunde ("nativo" ≠ modo Jogar direto Sony); a GUI poderia expor o
   perfil ativo + o que ele muda.
3. **Numeração**: fichas persistidas corretas (DualSense A=1, Pro real=2,
   DualSense B=3, 8BitDo=4). LEDs físicos decodificados corretos (P1
   central, P2 dois LEDs, 8BitDo 4 LEDs = padrão Nintendo de P4). O Pro
   real sem LEDs (item 1) era o que parecia "numeração quebrada".
4. **8BitDo com A/B trocados no jogo**: SDL segue as ETIQUETAS Nintendo
   por default. Cura na origem: `SDL_GAMECONTROLLER_USE_BUTTON_LABELS=0`
   (mapeamento por POSIÇÃO física, padrão do ecossistema PC) emitida pelo
   launch_env em toda variante + allowlist do wrapper (8BIT-03). Vale a
   partir do próximo restart do daemon + relaunch do jogo.
5. **Diálogo do controle externo**: parede de texto (3× o mesmo recado)
   reduzida a três linhas sem redundância (HARM-GUI-01); testes pinam
   comprimento máximo.

Pendências desta sessão: (i) install sem flag p/ ativar o DKMS 0002 + conf
(exige fechar o jogo; módulo novo vale ao reconectar/reboot); (ii) validação
ao vivo do Pro real reconectando sob o módulo novo; (iii) EIO da calibração
0x05 em BT (drift de gyro do vpad) segue aberto; (iv) UX do perfil ativo.
