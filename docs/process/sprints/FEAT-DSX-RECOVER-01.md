# FEAT-DSX-RECOVER-01 — Auto-recuperação do storm -71 do DualSense

Status: **DONE** (2026-06-03). Parte do guarda-chuva [FEAT-DSX-DEFINITIVE-FIX-01](FEAT-DSX-DEFINITIVE-FIX-01.md).

## Problema
O `-71` é fragilidade do controlador Ryzen (não corrigível por software). Quando o storm acontece,
o controle fica conectando/desconectando até intervenção manual. O timer do Aurora (2min/1h) é lento
demais — a reação precisa ser **em segundos**.

## Solução
Watcher orientado a evento, serviço de **sistema (root)**:

- `scripts/dsx_recover.sh` — `journalctl -kf -o cat --since now` filtrando
  `error -71` / `USB disconnect` / `not accepting address` / `unable to enumerate`. Ao ver
  **≥4 sinais em 10s** (throttle de 20s anti-loop), recupera **sem mexer em porta física**:
  1. re-pin de power dos devices `054c` + xHCI (`power/control=on`, `autosuspend=-1`);
  2. `udevadm trigger --attr-match=idVendor=054c`;
  3. re-bind suave via `authorized` toggle (re-enumera por software);
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
