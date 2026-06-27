# SESSÃO 2026-06-26 — Storm do DualSense: investigação completa + estado pré-reboot

> **LEIA ESTE DOC PRIMEIRO quando a Vitória voltar.** É o estado-da-arte da investigação.
> Ela reiniciou para o TESTE LIMPO (o kernel só fica default após reboot). Se ela disser
> "não deu certo", vá direto à seção **§7 (se ainda stormar pós-reboot)**.
> Contextos brutos dos agentes da auditoria: `docs/process/audits/2026-06-26-storm-audit/`.

## §0. O problema, em uma frase
DualSense entra em **storm** (`error -71`, link cai 480→12 Mbps, "device not accepting address",
disconnect/reconnect em loop) **"quando jogo"**, no Pop!_OS desta máquina (Ryzen 5800X, B450M).

## §1. O FATO DECISIVO (a Vitória estava certa o tempo todo)
Funciona **perfeito no Windows** E num **Linux default recém-formatado** (mesmo com o mic do
controle ligado). ⇒ **NÃO é hardware/cabo/porta/link-marginal.** É uma **REGRESSÃO da config NOSSA**.
(Erro meu grave: insisti em "trocar de porta"/"margem de link" por mensagens a fio antes de ouvir.)

## §2. Auditoria multi-agente (workflow `wf_b3d93182-740`, 7 agentes)
Frentes: kernel-cmdline, udev, audio-stack, git-timeline, hefesto-usb, power-mgmt + síntese.
Achados completos em `docs/process/audits/2026-06-26-storm-audit/achados-por-agente.md`.
Síntese crua em `.../sintese-resultado.json`.

**Ranking de causa (síntese):**
1. **ALTA** — Cabo-de-guerra de áudio USB: o **WirePlumber** fixava o mic do DualSense como
   **source padrão** + perfil **pro-audio** → a cada conexão corria pra abrir a captura do mic
   (o *OSD de volume do mic* que aparece antes do colapso) numa rajada de control-transfers,
   enquanto a **regra 75** desbindava o `snd-usb-audio`. Um puxa, o outro empurra → re-enum →
   sob carga o link tomba. **Nada disso existe no default.**
2. MÉDIA — `dsx-recover` (authorized-toggle = re-enum por SW); estava disabled mas latente.
3. MÉDIA — `threadirqs` (threada a IRQ do xHCI; sob carga perde a janela de completion).
4. BAIXA / **INOCENTADOS** — `usbcore.quirks=054c:0ce6:k` (NO_LPM, nulo em USB2) e
   `processor.max_cstate=1`: eram TENTATIVAS-DE-FIX adicionadas DEPOIS do storm (git-timeline:
   o "-71" só aparece narrado a partir do v3.12). Já removidos.
5. BAIXA / **MANTER** — `usbcore.autosuspend=-1`, `pcie_aspm=off`, udev 72/99: protetivos
   (impedem autosuspend/ASPM que derrubaria um HID em polling). Reverter PIORA.

## §3. O que foi APLICADO nesta sessão (cirúrgico, mantendo o hefesto)
Sistema (todos já valendo, exceto onde indicado "próximo boot"):
-  Matei o `audio_catcher.py` (leftover MEU de debug que reunbindava em loop de 30ms — eu
  **piorei** o problema nesta sessão; assumido).
-  `fix_wireplumber_default_source.sh --disable-source` → mic do DualSense **fora** do
  default-source + supressão. Source agora = onboard analog. Voz pela **C920**.
-  Removida a linha `...DualSense...=pro-audio` de `~/.local/state/wireplumber/default-profile`.
-  Removido `~/.config/environment.d/90-hefesto-dualsense-mic.conf` (MIC_INTENDED=1).
-  **Removidas as udev 75 (audio-unbind) e 76 (touchpad-ignore)** de `/etc/udev/rules.d/`
  (a Vitória pediu: deixar o áudio bindado-e-quieto como no default; sem o `unbind` disruptivo).
-  `dsx-recover` apagado de vez (`/etc/systemd/system/hefesto-dsx-recover.service` +
  `/usr/local/sbin/dsx_recover.sh`).
-  **`threadirqs` removido** do bootloader (`kernelstub --delete-options threadirqs`) +
  comentado na Aurora **v3.25** (linha ~713) + propagado p/ `/usr/local/sbin`. **(vale no reboot)**
-  `usbcore.quirks=...:k` e `max_cstate=1` já removidos (v3.24). **(valem no reboot)**

hefesto (fork, instalação editável — código rodando = repo). Bugs corrigidos hoje:
- `FEAT-EMULATION-GAMEMODE-COMBO-01` — modo-jogo agora é **PS+Options**; long-press OFF
  (`ps_long_press_ms=0`, configurável).
- `FEAT-HOTKEY-COMBO-NO-LEAK-01` — combo não vaza Meta/setas pra emulação (matava o "Control travado").
- `FEAT-EMULATION-GAMEMODE-FLUSH-01` — solta teclas ao suprimir (sem modificador preso).
- `FEAT-MOUSE-PERSIST-01` — toggle de mouse persiste em restart/reboot (provado).
- `DURABILIDADE-DIST-UPGRADE-01` — install.sh recria o venv se o Python bumpar.
- Emulação de mouse **provada** funcionando ao vivo (cursor 658 ev, clique dir, teclas).
- Sprints: `docs/process/sprints/2026-06-26-correcao-*` e `2026-06-26-validacao-*`.
- **NÃO commitado ainda** no git do fork (oferecer commit).

## §4. POR QUE "não deu certo" no teste de agora (honesto)
Às 03:18 o storm continuou (no `3-4`). **Mas este boot NUNCA foi limpo**: `threadirqs` e o quirk
**ainda estavam ativos** (só saem no reboot), e a regra 75 (unbind) só foi removida DEPOIS desse
storm. Ou seja: o teste de agora ainda tinha 3 dos suspeitos ativos. Eu me precipitei dizendo
"resolvido ao vivo" — não dava pra concluir sem reboot.

## §5. ESTADO PRÉ-REBOOT (verificado)
- `/etc/kernelstub/configuration`: **sem** threadirqs/quirk/max_cstate. Mantém autosuspend=-1,
  pcie_aspm=off, mitigations=off, acpi_enforce_resources=lax, nvidia-*.
- udev `/etc/udev/rules.d/`: **70, 71, 72, 99** (75 e 76 REMOVIDAS).
- WirePlumber: DualSense **fora** do default-source e **sem** pro-audio (persistido).
- Sem dsx-recover, sem audio_catcher.
- `/proc/cmdline` deste boot AINDA tem threadirqs+quirk (normal — somem no próximo boot).

## §6. TESTE PÓS-REBOOT (o teste LIMPO de verdade)
1. `cat /proc/cmdline` → **NÃO** deve ter `threadirqs`, `usbcore.quirks`, `processor.max_cstate`.
   Deve ter `usbcore.autosuspend=-1 pcie_aspm=off`.
2. `ps -eo comm | grep xhci` → **não** deve haver `irq/*-xhci_hcd` (IRQ voltou a hardirq).
3. `wpctl status` → Default Source **≠** DualSense; o card do DualSense **não** em pro-audio.
4. Plugar o controle, `lsusb -t` → **480M estável**. As interfaces de áudio agora **bindam e ficam**
   (snd-usb-audio), idle — como no default (não tem mais a regra 75 desbindando).
5. **TESTE DE CARGA (a condição real):** jogar OU `stress-ng --cpu $(nproc)` por uns minutos com o
   controle, monitorando `sudo dmesg -w | grep -iE 'error -71|not accepting|full-speed'` →
   **não deve stormar**; o OSD do mic **não** deve piscar.
6. Gatilhos do hefesto seguem funcionando (resistência/LED/rumble).
   → **Se passar:** RESOLVIDO. O mic do DualSense fica bindado idle (não capta voz mesmo; voz = C920).

## §7. SE AINDA STORMAR PÓS-REBOOT (escalonamento)
Aí já teremos neutralizado TODA a config de áudio (sem WP-grab, sem pro-audio, sem regra 75) E o
kernel estará default (sem threadirqs/quirk). Próximos passos, em ordem:
1. **Teste decisivo de hardware vs software:** bootar um **Linux live USB** (Pop/Ubuntu) e plugar o
   controle SOB CARGA. Se funcionar no live → o culpado é UMA das nossas config restantes (ir
   removendo: udev 72/99, depois `usbcore.autosuspend=-1`, depois `pcie_aspm=off` — um a um, testando).
   Se STORMAR até no live → é a porta/controlador/firmware DESTA máquina (e "funciona no default"
   precisa ser re-confirmado no MESMO hardware/porta).
2. Confirmar se o **dongle BT rtw88_8822bu** (mesmo controlador Matisse Bus 3/4) compete por banda —
   testar removendo o dongle.
3. Testar o controle numa porta do **chipset (Bus 1/2, robusto)** vs Matisse (Bus 3/4) sob carga,
   agora com a config de áudio neutra (antes a porta foi red herring por causa do áudio).
4. Reavaliar `acpi_enforce_resources=lax` (default não tem) e `mitigations=off`.

## §8. Pendências / TODO ao voltar
- [ ] Ler ESTE doc + `achados-por-agente.md` + a memória `dualsense-pssupport-guerra`.
- [ ] Rodar §6 (teste pós-reboot) e classificar: resolvido OU §7.
- [ ] Se resolvido e estável: oferecer **commit** das mudanças do fork + reintegrar a regra 75? (NÃO —
      ficamos sem ela; o áudio idle é o estado default desejado).
- [ ] Relançar o `storm_detector.py` (scratchpad) pro teste de carga (ele me avisa na hora do -71).
- [ ] Watcher/detector e logs em: `/tmp/claude-1000/.../scratchpad/` (game_watch.log, storm_detector.log).
