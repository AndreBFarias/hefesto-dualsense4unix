# FEAT-DSX-RECOVER-01 — Auto-recuperação do storm -71 do DualSense

Status: **DONE** (2026-06-03) — porém  **SUPERADO (2026-06-26)**: a premissa de causa-raiz estava
errada e a estratégia de recuperação deste watcher **amplifica** o storm. Ver
"Premissa superada" abaixo. Parte do guarda-chuva
[FEAT-DSX-DEFINITIVE-FIX-01](FEAT-DSX-DEFINITIVE-FIX-01.md).

##  Premissa superada (2026-06-26) — leia antes de reusar
A afirmação original "o `-71` é fragilidade do controlador Ryzen (não corrigível por software)" está
**ERRADA** e foi superada. Verdade canônica atual (ver
[2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md](../discoveries/2026-06-26-storm-audio-pesquisa-profunda-quirk-vs-audiooff.md)):

- O `-71` é causado pela **enumeração das interfaces de áudio USB** (kernel `snd-usb-audio`) sob carga:
  uma rajada de control-transfers no EP0 que tomba o link → `-71` → re-enumeração. **Não** é o
  controlador Ryzen, BIOS, cabo ou porta (port-independente, provado A/B: áudio off = 0 storm em
  qualquer porta, inclusive a do chipset; Ryzen 7 5800X **Vermeer**).
- O `-71` **É corrigível por software**, por uma de duas alavancas alternativas (uma OU outra):
  (A) **quirk** de cmdline `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` (`g`=DELAY_INIT, `n`=DELAY_CTRL_MSG)
  que **preserva o áudio** espaçando a rajada (`scripts/install_usb_quirk.sh` ou
  `./install.sh --with-usb-quirk`); ou (B) regra udev **75** (`authorized=0`) que **desliga o áudio**
  USB (sem mic/fone) (`scripts/install_udev.sh --disable-usb-audio`).
- **Este watcher foi ABANDONADO**: o passo de "re-bind suave via `authorized` toggle" é exatamente
  uma **re-enumeração por software** — ou seja, *amplifica* o storm em vez de curá-lo. A correção
  definitiva ataca a causa (rajada do EP0 de áudio), não os sintomas pós-queda.

## Problema (registro histórico — premissa superada acima)
Premissa **incorreta** da época: o `-71` seria fragilidade do controlador Ryzen (não corrigível por
software). Quando o storm acontecia, o controle ficava conectando/desconectando até intervenção
manual. O timer do Aurora (2min/1h) era lento demais — a reação precisaria ser **em segundos**.

## Solução (ABANDONADA — registro histórico)
>  Abordagem superada: o passo 3 (`authorized` toggle) re-enumera por software e **amplifica** o
> storm. Use a correção definitiva (quirk DELAY_CTRL_MSG ou regra 75 audio-off). Mantido só como
> histórico.

Watcher orientado a evento, serviço de **sistema (root)**:

- `scripts/dsx_recover.sh` — `journalctl -kf -o cat --since now` filtrando
  `error -71` / `USB disconnect` / `not accepting address` / `unable to enumerate`. Ao ver
  **≥4 sinais em 10s** (throttle de 20s anti-loop), recupera **sem mexer em porta física**:
  1. re-pin de power dos devices `054c` + xHCI (`power/control=on`, `autosuspend=-1`);
  2. `udevadm trigger --attr-match=idVendor=054c`;
  3. re-bind suave via `authorized` toggle (re-enumera por software) —  **este passo é o que
     amplifica o storm**: re-enumeração por SW dispara nova rajada de EP0 do áudio;
  4. `systemctl --user restart` do daemon hefesto **se** instalado (via `runuser` no usuário gráfico).
- `assets/hefesto-dsx-recover.service` — `Restart=always`, `StartLimitBurst=5/60s`.
  Instalado em `/etc/systemd/system/`, script em `/usr/local/sbin/dsx_recover.sh`.

## Por que root e não Aurora
Precisa escrever em `/sys/.../power/control` e `.../authorized` (root). É específico do DualSense
(VID 054c), do escopo do hefesto. O Aurora cuida do power **global**; o watcher reusa esse estado
e age **pontual e em tempo real**.

## Verificação
```bash
systemctl status hefesto-dsx-recover.service
ps --ppid "$(systemctl show -p MainPID --value hefesto-dsx-recover.service)"   # deve ter journalctl -kf + bash
sudo journalctl -u hefesto-dsx-recover.service -f    # observar "recovery concluído" num storm real
```

## Limitações (honestas)
- O re-bind via `authorized` é **melhor-esforço**: num controlador glitchando forte pode não
  recuperar em 100% dos casos. Transforma "controle morto até eu agir" em "auto-cura em segundos".
- Os logs do bash podem sair em blocos (buffer de stdio do serviço); as **ações** executam na hora
  independente disso. Se precisar de log imediato, trocar o ExecStart por
  `/usr/bin/stdbuf -oL /usr/local/sbin/dsx_recover.sh`.
- Threshold 4/10s evita reagir a uma desconexão manual única; ajustável no topo do script.
