# Design — Caminho Universal anti-storm do DualSense (mic+fone preservados)

Origem: incidente Sackboy 2026-07-14 (rumble funcionou, controles caíram em loop -71).
Workflow design-caminho-universal-sem-haptic-audio (6 agentes). Documento para decisão.

I have all the grounding I need. Confirmed the crux facts independently (SDL fallback, PROTON_ENABLE_HIDRAW semantics, the version-dependent Proton caveats) and verified the profile schema already supports the mode switch. Here is the design document.

---

# Documento de Design — "Caminho Universal" anti-storm do DualSense (mic + fone preservados)

**Contexto:** incidente Sackboy 2026-07-14. Objetivo: tudo passa pelo Hefesto e funciona na hora de jogar, **sem** a vibração-via-áudio (haptic-de-áudio do PS5) que derruba o controle, **sem cortar mic nem fone**. Solução configurável, reversível e exposta na GUI/doctor.

## TL;DR

- **A causa-raiz do storm é o KERNEL**, não o jogo: a cada re-enumeração USB, o `snd-usb-audio` sonda o mixer UAC do controle martelando o EP0 (linhas `cannot get min/max values for control` / `failed to get current value for ch 0 (-22)`), colide com o `usbhid` anexando a interface HID → `can't add hid device: -71` → USB disconnect → loop. Provado no repo: com daemon **e** WirePlumber parados, ainda flapa.
- **O gatilho controlável é o JOGO no caminho nativo**: no incidente, o Sackboy rodava em Modo Nativo (`emulation_suppressed=True`, `PROTON_ENABLE_HIDRAW=1`), abrindo o hidraw físico e carregando o barramento na janela frágil de enumeração. A janela saudável (mesmo dmesg, minutos antes, com o vpad Xbox criado) enumerou limpa.
- **Nenhuma das 5 abordagens mata a causa-raiz preservando mic+fone.** A melhor jogada real é **remover o gatilho**: forçar o jogo pelo **vpad Xbox do Hefesto** e **isolar o hidraw físico** do jogo (nível HID, não evdev). Isso é a **convergência corrigida das abordagens #1 e #5**. Preserva mic+fone 100% (não encosta na classe de áudio USB) e roteia o rumble pelo FF do vpad — o caminho que já foi validado fisicamente ("amassou").
- **Honestidade:** isto é **mitigação forte do gatilho, não cura da raiz**. Um storm espontâneo (evento de energia, re-enum sem jogo) ainda é possível. O único corte de raiz que existe hoje (regra 75 / `authorized=0`) mata mic+fone e está **fora** por decisão de produto.

---

## 1. Ranking das abordagens

Critério composto: **(preserva mic+fone) × (mata o storm) × (viabilidade)**.

| # | Abordagem | Mic+Fone | Mata storm | Viável | Veredito | Evidência-chave |
|---|-----------|:--------:|:----------:|:------:|----------|-----------------|
| **1º** | **#5 `defesa_fecha_hidraw_nativo` + #1 `sdl_proton` (convergência)** — tirar o jogo do caminho nativo e isolar o hidraw físico; jogo só vê o vpad Xbox | **SIM** | **Provável (remove o gatilho)** | **Parcial** | **RECOMENDADO** | Storm no incidente rodou em Modo Nativo (`ev_daemon.txt` L17-19); janela saudável tinha o vpad criado. SDL com `SDL_JOYSTICK_HIDAPI=0` cai pra evdev (o físico é grabbed; jogo vê o vpad). Não toca áudio → mic+fone intactos. |
| — | **#4 `hefesto_intercepta_converte`** (null-sink + DSP → FF) | SIM | **NÃO** | **NÃO** | Descartar | Camada errada: storm nasce no *probe* do kernel (EP0), não no *stream* de áudio (isocrono, nem usa EP0). E no caso real o Sackboy usa rumble HID, não PCM — não há stream para interceptar. Alto esforço, zero eliminação do storm. |
| — | **#2 `pipewire_desliga_so_haptic_sink`** | (mataria fone) | **NÃO** | **NÃO** | Descartar | Refutado por experimento já feito: WirePlumber parado e **ainda** flapa (kernel). E não existe "sink de haptic" separável — fone+haptic são o **mesmo PCM 4ch** de If1; `node.disabled` derruba o fone junto. |
| — | **#3 `usb_interface_seletiva`** (`authorized=0` só no haptic) | **NÃO (mata fone)** | Provável | **NÃO** | Descartar | Granularidade da autorização USB é por-**interface**, não por-canal/endpoint. Fone e haptic dividem If1 → cortar haptic corta o fone. Só o mic (If2) é separável. |

**Observação sobre #1 e #5:** as duas convergem na **mesma conclusão** ("tire o jogo do caminho nativo → use o vpad → rumble por FF"), mas cada uma tinha um erro de mecanismo que a outra corrige:
- #1 achava que "SDL dirige o haptic-de-áudio" — **falso** (o driver PS5 do SDL só faz rumble HID). A parte aproveitável de #1 não é "env de SDL", é "tirar do nativo".
- #5 propunha `EVIOCGRAB` (evdev) como isolamento — **insuficiente**: o SDL HIDAPI abre `/dev/hidraw` direto e ignora o grab de evdev. A isolação de verdade tem de ser **no nível HID** (`SDL_JOYSTICK_HIDAPI=0` + sem `PROTON_ENABLE_HIDRAW`).

A recomendação abaixo é a **síntese corrigida** das duas.

---

## 2. Design recomendado: "Caminho Universal pelo vpad" (Recipe A — Steam Input OFF)

### A ideia em uma linha
Para jogos storm-prone, o Hefesto vira a **única entidade** que toca o DualSense físico. O jogo enxerga **só** um gamepad virtual Xbox (uinput/evdev, sem hidraw). O rumble do jogo volta ao controle pelo FF do vpad. Mic e fone continuam no device de áudio real, intocados.

### A cadeia completa no fim (o que passa por onde)

| Sinal | Caminho final | Passa pelo Hefesto? |
|-------|---------------|:-------------------:|
| **Input (botões/sticks/gatilhos-como-eixo)** | DualSense físico → daemon (dono do hidraw+evdev, com `EVIOCGRAB` no evdev físico) → **vpad Xbox (uinput)** → jogo lê o vpad | **SIM** |
| **Rumble** | Jogo emite rumble XInput → **FF no vpad** → `daemon.apply_game_rumble` → `rumble_sink` → `FF_RUMBLE` HID nos motores do DualSense físico ("amassou" já validado) | **SIM** |
| **Haptic-de-áudio (PS5 HD)** | **Nunca é engatado** — em XInput o jogo usa rumble clássico, não abre o card de áudio-haptico. (Tradeoff assumido, já decidido em memória: "haptics-de-áudio ficam fora por decisão anti-storm".) | Desligado por design |
| **Gatilhos adaptativos nativos** | **Perdidos** para esse jogo (só existem no caminho nativo). Tradeoff explícito. | — |
| **Microfone** | Interface de captura (If2) → PipeWire/WirePlumber → apps, **exatamente como hoje** (`HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED=1` permanece) | Intocado |
| **Fone (headset no controle)** | Sink de saída (If1, canais L/R) → PipeWire, **exatamente como hoje** | Intocado |

### Por que preserva mic+fone (garantido, não "provável")
A abordagem **não encosta em nenhuma interface de áudio USB**: sem regra 75, sem `authorized=0`, sem troca de profile do card, sem `node.disabled`. Tudo o que muda é **qual dispositivo de INPUT o jogo enxerga**. Logo mic+fone são trivialmente verdes — é a diferença central para a regra 75, que é tudo-ou-nada.

### Por que remove o gatilho do storm
Sem o jogo abrindo/martelando o hidraw físico (nem via nativo, nem via SDL HIDAPI), a re-enumeração passa a ocorrer só com os drivers de kernel — como no ciclo que **deu certo** no próprio `ev_dmesg.txt`. Some a carga concorrente do jogo na janela frágil, e o death-loop não começa. Empiricamente os storms estão correlacionados ao jogo no físico.

### A receita concreta (Recipe A — resolve a contradição do Steam Input)
1. **Perfil do jogo:** `mode.kind = "gamepad"`, `gamepad_flavor = "xbox"` (o schema **já suporta** isto — `profiles/schema.py:250-252`; nenhuma mudança de schema é necessária para o switch de modo). Sackboy **sai de nativo, vai para vpad/xbox**.
2. **Steam Input:** **DESLIGADO** para o app. Isto **mantém a postura atual** do Hefesto (`storm_doctor.check_steam_input` já marca ON como WARN; `disable_steam_input.sh` já desliga) — **eliminando a contradição** que a abordagem #1 tinha levantado (ela queria Steam Input ON). Com Steam Input OFF, o Steam entrega os devices crus e o jogo cai no nosso vpad via SDL/evdev. (Recipe B, Steam Input ON, é pior: o próprio Steam Input abre o hidraw do DualSense, reintroduzindo contenção e brigando com o vpad.)
3. **Launch options do jogo:** `SDL_JOYSTICK_HIDAPI=0 %command%` **e remover** `PROTON_ENABLE_HIDRAW=1`. Sem hidapi e sem o bind-mount do hidraw no pressure-vessel, o jogo não alcança o físico; o SDL cai pra evdev e lê o vpad Xbox.
4. **Rumble:** já roteado pelo FF do vpad (`uinput_gamepad.py` + `gamepad.py`) — nada a fazer além de garantir que o perfil está em `gamepad`.

### Limite honesto (o que esta solução NÃO faz)
- **Não cura a raiz.** O `snd-usb-audio` continua sondando o mixer a cada enumeração. Se algo re-enumerar o controle **sem** o jogo (energia, cabo, suspend), o storm pode reaparecer. Esta é uma mitigação de **gatilho**, com `n=1` de correlação.
- **O Hefesto não edita launch options do Steam de forma confiável** (`steam_launcher.py` só abre/foca a Steam — prova de que não há injeção de env hoje). Os itens 2-3 são **orientação + verificação**, não aplicação automática.
- **Caveat de versão do Proton:** `PROTON_ENABLE_HIDRAW` e o fallback não-hidraw têm bugs conhecidos e dependentes de versão (Proton #8672 "não funciona desde 10.0-1"; #9034 "fallback não-hidraw falha em device com múltiplas interfaces de input" — e o DualSense tem várias). Por isso a **Fase 1 empírica é obrigatória**: confirmar na máquina real, no Proton em uso, que o jogo vê **só** o Xbox vpad.

### Trilha ortogonal para a raiz (fora das 5, mencionar à mantenedora)
Se ela quiser atacar a **causa-raiz** mantendo mic+fone, as únicas alavancas que preservam os dois áudios são de **hardware/kernel**, não userspace:
- **Topologia USB:** mover o controle para o controlador USB mais robusto (chipset `02:00.0`, Bus 1/2) — aumenta a margem do link e pode absorver a rajada do probe. Reversível, não corta nada.
- O **quirk `gn`** (`DELAY_INIT`+`DELAY_CTRL_MSG`) **já está aplicado e não bastou** — não adianta "adicionar DELAY_CTRL_MSG". Um fix fino de kernel (fazer o `snd-usb-audio` pular/adiar o mixer-parse deste device) **não existe** como alavanca hoje; o único ponto que impede o probe é `authorized=0` (regra 75), que mata áudio.

Conclusão de produto: **adotar o Caminho Universal pelo vpad como o "correto e reversível"**, e tratar a raiz como trilha separada de HW/kernel (topologia primeiro, por ser reversível e sem custo de áudio).

---

## 3. Plano faseado

### Fase 1 — Teste diagnóstico reversível (nada permanente instalado)
Objetivo: provar/refutar a abordagem antes de escrever código. Tudo por ajuste manual, revertível em segundos.

1. **Colocar Sackboy no vpad/xbox temporariamente:** editar o perfil (ou `hefesto profile ...`) para `mode.kind=gamepad`, `gamepad_flavor=xbox`; reverter é voltar para `native`.
2. **Steam Input OFF** para o app; **launch options** = `SDL_JOYSTICK_HIDAPI=0 %command%`, **remover** `PROTON_ENABLE_HIDRAW`.
3. **Rodar A/B** com `dmesg -w` (ou `journalctl -k -f`) filtrando `usbhid|snd|disconnect|-71|min/max|ch 0`:
   - **Run A (controle, nativo):** deve **reproduzir** o storm do `ev_dmesg.txt`.
   - **Run B (vpad-isolado):** esperado **ZERO** `cannot get min/max`, **ZERO** `can't add hid device: -71`, **ZERO** `USB disconnect` por uma sessão longa (>10 min do trecho pesado).
4. **Aceite de isolação:** `fuser -v /dev/hidraw*` mostra **só o daemon** segurando o hidraw do DualSense (não o processo do jogo/proton); e **dentro do jogo o controle aparece como "Xbox 360 Controller", exatamente UM** (não "2 controles" — cobre o risco histórico de `js0-js5` expostos ao jogo).
5. **Aceite de áudio:** durante a Run B, `wpctl status` mostra Source (mic) e Sink (fone) do DualSense; gravar do mic e ouvir áudio no fone fisicamente.

**Critério de decisão:** se Run B fica limpa por uma sessão longa **e** mic+fone funcionam → abordagem confirmada, seguir para Fase 2. Se Run B ainda storma → a raiz é o `snd-usb-audio` sozinho e a mitigação de gatilho não basta; pular para a trilha de topologia/kernel (nada foi instalado, custo zero).

### Fase 2 — Implementação (opt-in, reversível, exposta na GUI/doctor)
Arquivos e pontos concretos (sem eu implementar — só o mapa):

- **Perfis (`profiles/`)** — nenhum schema novo obrigatório: reposicionar `sackboy` (e futuros storm-prone) para `mode.kind=gamepad`/`gamepad_flavor=xbox` nos `assets/profiles_default`. *Opcional aditivo:* um campo `mode.isolate_hid: bool` (default off) só para **dirigir a orientação/verificação** abaixo — mantém compat (extra="forbid" exige aditivo consciente).
- **GUI (aba de perfil / aba Início):**
  - Renomear/rotular o toggle por-perfil: **"Jogar pelo Hefesto (vpad — anti-storm, recomendado)"** vs **"Modo Nativo (DualSense puro — pode desconectar em jogos com haptic de áudio)"**. Deixar o vpad como **default** para jogos.
  - Como o Hefesto **não edita launch options**, mostrar um painel **"Passos no Steam"** com botão **copiar**: `SDL_JOYSTICK_HIDAPI=0 %command%`, "remover `PROTON_ENABLE_HIDRAW`", "Steam Input: Desligado". Orientação + verificação, não aplicação.
- **Doctor (`integrations/storm_doctor.py`)** — adicionar checks read-only (o bloco já existe e é read-only):
  - **`check_hidraw_owner`** (novo): via `fuser`/`/proc`, alertar se um processo **que não é o daemon** segura o hidraw do DualSense enquanto um perfil storm-prone está ativo → "vazamento de isolação".
  - **`check_profile_native_stormprone`** (novo): perfil em `native` **e** jogo marcado storm-prone (ou `PROTON_ENABLE_HIDRAW` presente) → WARN com a ação "troque para vpad".
  - Manter `check_steam_input` como está (ON = WARN) — **agora coerente** com a recomendação (Recipe A quer OFF). Não há mais contradição a reconciliar.
- **NÃO tocar** em `audio_control.py`, `fix_wireplumber_default_source.sh`, `install_udev.sh --disable-usb-audio`, nem na regra 75 — são justamente o que preserva (ou o que mataria) mic+fone. Ficam como estão, opt-in agressivo separado.
- **Reversibilidade:** trocar o modo do perfil de volta para `native` restaura o comportamento anterior; nenhum arquivo de sistema é escrito.

### Fase 3 — Validação (mic+fone OK **e** storm sumiu)
- **Storm sumiu:** Sackboy >10 min no vpad-isolado com `scripts/storm_watch.sh` (ou `dmesg -w` filtrado) → 0 linhas de `-71`/`can't add hid device`/`USB disconnect`; no daemon, ausência de `controller_disconnected reason=probe_offline` repetido. Comparar contra a Run A (nativo, que ainda deve stormar) como controle.
- **Isolação:** `fuser -v /dev/hidraw*` = só o daemon; jogo vê exatamente 1 "Xbox 360 Controller"; rumble dispara fisicamente (teste do "amassou").
- **Mic+fone OK:** `wpctl status` + `pactl list cards | grep -A25 -i dualsense` mostram Source e Sink presentes; gravar com o mic e ouvir no fone **durante** o jogo.
- **Regressão honesta:** confirmar que os gatilhos adaptativos **não** respondem mais nesse jogo (tradeoff esperado do XInput) — documentar, não "esconder".

---

## 4. O que descartar e por quê

- **#3 `usb_interface_seletiva` (authorized=0 só no haptic)** — **inviável para o objetivo**: a autorização USB é por-interface; fone e haptic são o **mesmo** If1 (PCM 4ch). Cortar haptic = cortar fone. Viola "manter fone". (Só o mic, If2, é separável — e não é o que ela quer sacrificar.) Fonte: descritor `nondebug/dualsense`.
- **#2 `pipewire_desliga_so_haptic_sink`** — **inviável e refutado**: (a) não existe sink de haptic separável (mesmo node 4ch → `node.disabled` mata o fone); (b) mesmo que existisse, o PipeWire opera **acima** do ponto do storm — experimento no repo mostrou WirePlumber parado e **ainda** flapando. Pior: automatizar troca de profile é um dos **gatilhos** de estresse.
- **#4 `hefesto_intercepta_converte` (null-sink + DSP → FF)** — **inviável na prática**: ataca a camada errada (o storm é o *probe* do kernel no EP0, não o *stream* isocrono), e no caso real o Sackboy nem emite haptic como PCM (usa rumble HID, que o vpad já cobre). Alto esforço (thread RT + DSP + latência 10-40 ms + routing por-app frágil) para **zero** eliminação do storm. Se um dia entrar, é feature de **fidelidade de haptic**, jamais vendida como anti-storm.
- **Regra 75 / `authorized=0` total** — **fora por produto**: mata mic+fone+haptic juntos. É o único corte de raiz que existe hoje, mas viola a restrição central.

---

## 5. Incerteza e esforço (honesto)

- **Confiança na recomendação: MÉDIA.** A direção é sólida e a preservação de mic+fone é **certa**. Mas o "mata o storm" é **probabilístico** (remove o gatilho-jogo; não a raiz-kernel) e depende de comportamento **version-dependent** do Proton (`PROTON_ENABLE_HIDRAW`/fallback não-hidraw têm bugs abertos). Por isso a Fase 1 empírica é a porta de entrada — barata e reversível.
- **Esforço:** Fase 1 ≈ uma sessão de teste (0 código). Fase 2 ≈ baixo-médio (rótulos na GUI, 2 checks read-only no doctor, reposicionar perfis; **sem** schema novo obrigatório, **sem** DSP, **sem** mexer em áudio). A parte "launch options" é orientação/verificação, não automação — limite conhecido.
- **Tradeoff de produto assumido:** o Caminho Universal pelo vpad **abre mão dos gatilhos adaptativos e do haptic HD nativo** nos jogos storm-prone — exatamente a razão pela qual o Modo Nativo existe. É uma decisão consciente (alinhada à memória: "haptics-de-áudio ficam fora por decisão anti-storm"). O Modo Nativo **permanece** disponível, agora com aviso de storm.
- **Risco residual não coberto:** storm espontâneo por re-enumeração sem jogo. Endereçá-lo exige a trilha de topologia USB (reversível, sem custo de áudio) ou um fix de kernel que hoje **não existe** como alavanca fina.

---

## Fontes e arquivos

**Evidência do incidente:** `…/scratchpad/ev_dmesg.txt` (ciclo saudável com vpad vs. ciclo que falha: `cannot get min/max values`/`failed to get current value for ch 0 (-22)` → `usbhid …:1.3: can't add hid device: -71` → `USB disconnect` em loop); `ev_daemon.txt` (L17-19 `emulation_suppressed=True`+`sackboy_nativo`; disconnect ~30s depois); `ev_journal_sistema.txt`.

**Código do repo (grounding da Fase 2):** `src/hefesto_dualsense4unix/profiles/schema.py:227-252` (`ProfileModeConfig`: `kind∈{desktop,gamepad,native}`, `gamepad_flavor∈{dualsense,xbox}`, `coop` — switch de modo **já suportado**); `integrations/uinput_gamepad.py:50-95` (flavors xbox `045e:028e` / dualsense `054c:0ce6`), `:502` (o próprio código admite "máscara DualSense atraindo o hidraw"); `daemon/subsystems/gamepad.py:66-89,227-295` (grab = `EVIOCGRAB`/`set_grab` — evdev, **não** esconde hidraw); `integrations/storm_doctor.py` (bloco read-only: `check_quirk`, `check_steam_input` ON=WARN, `check_wireplumber`, `check_authorized_rule`); `integrations/steam_launcher.py` (só abre/foca a Steam — **prova de que o Hefesto não injeta env/launch options**); `integrations/audio_control.py` (mute do mic — **intocado**). Regra agressiva fora de escopo: `assets/75-ps5-controller-disable-usb-audio.rules`.

**Descobertas do repo (raiz do storm):** `docs/process/discoveries/2026-06-26-mic-usb-audio-e-a-causa-real-do-storm.md` (WirePlumber parado e ainda flapa → kernel `snd-usb-audio`); `…/2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md` (If1 única saída 4ch = fone+haptic juntos; mecanismo EP0/probe; alavancas quirk `gn` vs `authorized=0`).

**Web (confirmações independentes):**
- SDL_JOYSTICK_HIDAPI=0 → fallback para evdev/joydev: [SDL2 Wiki HIDAPI](https://wiki.libsdl.org/SDL2/SDL_HINT_JOYSTICK_HIDAPI), [ArchWiki Gamepad](https://wiki.archlinux.org/title/Gamepad).
- `PROTON_ENABLE_HIDRAW` habilita o caminho hidraw nativo (whitelist inclui o PS5); default do Proton = hidraw off → XInput: [nick.tay.blue Wine+DualSense](https://nick.tay.blue/2024/01/21/wine-dualsense/), [Heroic #4168 (disable hidraw → age como Xbox360/XInput)](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/issues/4168).
- **Caveats version-dependent (risco):** [Proton #8672 (`PROTON_ENABLE_HIDRAW` quebrado desde 10.0-1)](https://github.com/ValveSoftware/Proton/issues/8672), [Proton #9034 (fallback não-hidraw falha em device com múltiplas interfaces)](https://github.com/ValveSoftware/Proton/issues/9034), [Proton #8644 (DualSense desaparece no caminho nativo)](https://github.com/ValveSoftware/Proton/issues/8644).
- Origem das mensagens de mixer do `snd-usb-audio`: [raspberrypi/linux #6943](https://github.com/raspberrypi/linux/issues/6943).
- Fone+haptic = mesmo device 4ch (inseparável no nível USB): descritor `nondebug/dualsense`, [PCGamingWiki Controller:DualSense](https://www.pcgamingwiki.com/wiki/Controller:DualSense).
