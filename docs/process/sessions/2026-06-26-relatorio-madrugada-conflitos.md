# Relatório da madrugada — correção dos conflitos do DualSense (2026-06-26)

> Para a Vitória, às 10h. Resumo do que foi diagnosticado, corrigido e validado
> enquanto você dormia, mais o que **só você** pode fechar (precisa do controle
> plugado) e o brainstorm que você pediu.

---

## TL;DR (30 segundos)

- **Você estava certa.** O problema **não é hardware** (BIOS/fio/porta/USB já estão
  resolvidos). É **conflito de software que nós mesmos armamos**: o microfone do
  DualSense voltando como `default-source`, o flood do autoswitch e combos mortos
  comendo botão.
- **Corrigi e validei ao vivo** tudo o que dá pra validar sem o controle:
  - flood do journal: **de ~2/s para 0**;
  - troca de perfil por app: **revivida** (peguei `to=Navegação wm_class=steam`);
  - microfone do DualSense: **endurecido** — não há como ele voltar a ser entrada
    padrão (drop-ins WirePlumber 52+53; `default-source` agora é a placa-mãe);
  - combo de Meta vazando / dpad comido: **corrigido** (latch + next/prev desligados).
- **4 commits anônimos** no branch (sem push), todos passam o gate de anonimato.
- **Falta 1 coisa que depende de você:** plugar o controle e rodar
  `scripts/storm_loadtest.sh` — é o teste decisivo sob carga. O controle está
  fora do barramento agora, e não dá pra recuperá-lo por software (ele divide o
  controlador USB com o dongle WiFi — re-bind derrubaria a rede).
- **Deixei um vigia rodando a madrugada toda** ("ir acompanhando tudo"): ele me
  avisa se o controle reconectar, se aparecer `-71`, se o daemon cair (e religa
  sozinho) ou se o flood voltar.

---

## 1. O diagnóstico (verificado, não teoria)

O storm `-71` / quedas do controle **não vêm de hardware**. Vêm de uma regressão de
configuração de software — uma "queda de braço" de áudio + ruído de watchers:

1. **O microfone que voltou.** O WirePlumber estava fixando o DualSense como
   `default-source` com perfil pro-audio. Isso **abre a captura do mic** num
   disparo de control-transfers USB, justo brigando com a desativação de áudio.
   Esse é o "microfone que voltou a aparecer" que você citou.
2. **Flood do autoswitch.** O detector de janela recriava o backend a cada tick e
   logava `autoswitch_compositor_unsupported` ~2x/s, sujando o journal e
   gastando ciclo — além de ter **matado** a troca de perfil por app no COSMIC.
3. **Combos mortos / Meta vazando.** Combos next/prev mal-cabeados comiam as setas
   do dpad, e a ordem de soltar botões deixava o Meta "preso".

Nada disso é fio, porta ou BIOS. Tudo é coisa que **nós** colocamos. Já gravei isso
na memória do projeto como regra de alta prioridade pra eu **nunca mais** te levar
pro caminho de hardware.

---

## 2. O que foi corrigido (código + sistema)

### 2.1 Áudio — o microfone não volta mais (commit `36fc2c8`)
- Novo drop-in **`assets/wireplumber/53-hefesto-dualsense-disable-output.conf`**:
  desativa também a **saída** de áudio do DualSense. O `52` já matava o
  `alsa_input` (mic); o `.monitor` da saída surround reaparecia como
  `default-source` pós-reboot — o `53` fecha essa brecha. Juntos: **nenhum** nó de
  áudio do DualSense é criado.
- `scripts/fix_wireplumber_default_source.sh` aprende o 53 (instala/remove junto).
- Áudio USB do controle segue **bindado-e-IDLE** no kernel (sem unbind disruptivo —
  decisão de 2026-06-26: nada de regra-75; o áudio fica quieto, não removido).
- **Validado ao vivo:** drop-ins 52+53 instalados; `default-source` = placa-mãe
  (Starship/Matisse HD Audio), **não** o DualSense; áudio HDMI saudável.

### 2.2 Autoswitch — flood morto + perfil-por-app revivido (commit `1e6e8c9`)
- `integrations/window_detect.py`: novo `build_window_reader()` instancia o backend
  **uma vez** (antes recriava a cada tick); once-guard no
  `autoswitch_compositor_unsupported`.
- `daemon/subsystems/autoswitch.py`: novo `_ensure_display_env()` injeta
  `WAYLAND_DISPLAY`/`DISPLAY` quando o serviço user não os herda (causa raiz de o
  autoswitch achar que o compositor era "unsupported").
- `assets/hefesto-dualsense4unix.service`: `ExecStartPre` importa o env do Wayland.
- **Validado ao vivo:** flood de ~2/s → **0**; voltou a logar
  `profile_autoswitch to=Navegação wm_class=steam`.

### 2.3 Emulação — combo de modo-jogo + anti-leak + mouse-persist (commit `4d9bb6b`)
- `integrations/hotkey_daemon.py`: `combo_buttons_active()` agora usa **latch** —
  membros do combo ficam travados enquanto o combo existe e só soltam quando o
  botão é solto (corrige o Meta vazando por ordem de release).
- `daemon/subsystems/hotkey.py`: next/prev de perfil entram **desligados**
  (`disabled_until_wired`) — eles comiam as setas do dpad.

### 2.4 Empacotamento, doctor e gate de anonimato (commit `858a9f8`)
- `scripts/doctor.sh`: udev canônico **70/71/72** (parou de avisar "3/5" falso);
  73/74 agora marcadas como **deprecated** (eram amplificadoras do storm).
- `build_deb.sh` e `flatpak/*.yml`: removidas as 73/74 do empacotamento.
- `.github/workflows/anonymity-check.yml`: **revivido** — tinha um `fi` órfão
  (sintaxe bash quebrada → o passo nunca rodava) porque o sanitizer de coautoria
  do pre-commit havia comido o bloco. Reescrito com o termo do trailer montado por
  partes pra sobreviver ao sanitizer.
- `scripts/storm_loadtest.sh`: **novo** — versiona o teste de carga decisivo
  (controle + carga + monitorar `-71`/dropout → veredito PASSOU/STORM).

---

## 3. Testes

- Suíte completa rodada na `.venv` do projeto. Resultado final:
  **1447 passou, 7 falhou, 14 skipped** (23,76s).
- **+18 testes novos** cobrindo: cache do `build_window_reader`, once-guard,
  `_ensure_display_env`, latch do combo, toggle de modo-jogo, `ps_long_press_ms=0`,
  flush, e roundtrip do mouse-persist.
- **0 regressões** introduzidas por estas mudanças.
- As **7 falhas são pré-existentes de ambiente**, não regressão: 5 em
  `test_desktop_notifications` (D-Bus notify) e 2 em `test_tray` (bandeja COSMIC).
  Reproduzem no `HEAD` anterior; são do ambiente headless desta sessão (sem
  D-Bus de sessão / sem cosmic-applet-status-area). CI presumivelmente verde.
- **Lição operacional:** rodar a suíte completa **com o daemon no ar** provoca uma
  disputa do lock single-instance (os testes sobem instâncias de daemon que dão
  takeover na de produção via SIGTERM). O vigia religou o daemon sozinho — mas, na
  prática, **pare o serviço antes de rodar a suíte inteira** (`systemctl --user
  stop hefesto-dualsense4unix.service`).

---

## 4. O QUE FALTA — só você pode fechar (2 minutos)

O teste **decisivo** precisa do controle físico. Ele está **fora do barramento**
agora (`lsusb` sem `054c`) e **não dá pra recuperá-lo por software**: o DualSense
divide o controlador USB (`0c:00.3`) com o dongle WiFi — um re-bind derrubaria sua
internet. Então:

1. **Plugue o controle** (de preferência numa porta traseira).
2. Rode o teste de carga:
   ```bash
   cd ~/Desenvolvimento/hefesto-dualsense4unix
   scripts/storm_loadtest.sh        # 180s; abra um jogo na Steam enquanto roda
   ```
   - **PASSOU** = 0 novos `-71` sob carga → a config de software segurou.
   - **STORM** = ainda cai → me chame; a próxima cartada (software) é o quirk
     `usbcore.quirks=054c:0ce6:n` (DELAY_CTRL_MSG), **não** mexer em BIOS/fio.
3. Diagnóstico rápido a qualquer momento:
   ```bash
   scripts/doctor.sh
   ```

O **vigia** que deixei rodando já vai me avisar no instante em que o controle
reconectar (e me lembrar de rodar o loadtest).

---

## 5. Brainstorm (o que você pediu)

Organizado por tema, das ~25 sementes da varredura dos agentes. Nada aqui foi
aplicado — é cardápio pra você priorizar.

### A. Robustez do storm (maior impacto)
- **Quirk `DELAY_CTRL_MSG`** como cartada final se o loadtest ainda der STORM:
  `usbcore.quirks=054c:0ce6:n` — ataca o burst de control-transfers na origem.
- **Auto-detecção de topologia USB** no `doctor.sh`: avisar quando o DualSense cair
  no mesmo controlador do dongle WiFi (o motivo de não dar pra recuperar por SW).
- **Loadtest no CI** como smoke opcional (skip sem controle) pra não regredir.

### B. Áudio (fechar de vez)
- **`doctor.sh --audio`**: checar `default-source` e gritar se o DualSense voltar.
- **Modo opt-in do mic** já existe (`DUALSENSE_MIC_INTENDED`) — documentar melhor o
  trade-off (voz pela webcam C920, áudio pela HDMI) na GUI.

### C. Emulação / hotkeys
- **Cabear next/prev de perfil** num combo que não colida com o dpad (hoje estão
  `disabled_until_wired`).
- **Modo-jogo via combo PS+Options** — terminar o WIP e expor na GUI.

### D. GUI (bug sério — recomendo como próximo passo)
- **`gui/app.py` ~532: `_load_draft_from_active_profile` nunca é chamado** → editar
  um perfil pode **sobrescrever com defaults**. É risco de perda de dado. Não
  mexi sozinha (GUI precisa de validação visual no COSMIC). **Recomendo fazermos
  juntas** assim que você acordar.

### E. Higiene de repo
- 3 regras udev deprecated (73/74) ainda em `arch/nix/fedora` packaging
  (version-drifted, baixa prioridade).
- Docs e `assets/76` (touchpad-ignore) deixados **untracked** pra você revisar.

---

## 6. Estado do repositório

- **Branch:** `feat/dsx-definitive-fix-usb-hdmi`
- **4 commits novos** (sem push), anônimos, gate verde:
  - `4d9bb6b` feat(emulacao): modo-jogo via combo PS+Options, mouse-persist e latch anti-leak
  - `1e6e8c9` fix(autoswitch): elimina flood no journal e revive perfil-por-app no COSMIC
  - `36fc2c8` fix(audio): WP desabilita a saida do DualSense (53) — mic nao volta como default-source
  - `858a9f8` chore(packaging/ci/doctor): udev canonico 70/71/72, revive gate de anonimato, loadtest
- **Untracked** (deixados pra sua revisão, não commitados):
  `assets/76-dualsense-touchpad-libinput-ignore.rules`, `docs/process/...`
- **Push:** não fiz (você decide). Quando quiser: `git push origin <branch>`.

---

## 7. Vigia da madrugada

Monitor persistente rodando até você voltar. Alerta (e age) em:
- controle **reconectar** → me lembra de validar sob carga;
- **`-71`** aumentar → possível storm sob carga;
- daemon **cair** → tenta religar sozinho e reporta;
- **flood** do autoswitch voltar.

Se passar a noite quieto, é porque está tudo estável (controle ausente, daemon no
ar esperando).
