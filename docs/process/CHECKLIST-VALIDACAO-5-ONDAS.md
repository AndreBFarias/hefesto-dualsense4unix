# Checklist de validação ao vivo — 5 ondas (fazer APÓS commit + re-install)

> Ordem: (1) auditoria cross-cutting verde → (2) commit anônimo → (3) re-rodar install →
> (4) reboot recomendado (aplica udev novas + cmdline) → (5) este checklist.
> Cada item aponta a onda e o sintoma original da mantenedora.

## Pré-condições
- [ ] `scripts/doctor.sh` roda 100% verde (inclui a nova seção "Rádio e pareamento").
- [ ] `hefesto-bt-agent.service` ativo (`systemctl is-active hefesto-bt-agent.service`).
- [ ] bluetoothd 5.85 sem crash no journal do dia (`journalctl -u bluetooth --since today | grep dumped`).

## Numeração e LEDs (Onda N + U)
- [ ] **Cliente Steam aberto SEM jogo**: DualSense branco PERMANECE azul/player-1 (não vira
      verde/player-3). UM só "player 3" visível na mesa. (aceite N — o "perfil eterno"/verde curado)
- [ ] **2 DualSense no cabo**: NÃO aparece "sony 1 / sony 4"; se aparecer, botão **"Renumerar
      agora"** compacta para 1,2. (U2/U10)
- [ ] Escrita estrangeira de LED (Steam) repintada em ≤2s (no máximo um piscar). (N defend_display)

## GUI — os sintomas que a mantenedora relatou (Onda U)
- [ ] **"Perfil eterno"**: aplicar cor/rumble/gatilho na aba e trocar de foco de janela NÃO
      reverte a edição. (U3/U4/U9/U11 — Causa A)
- [ ] Aba **Início offline**: botão mostra "Ligar o Hefesto" e liga in-place (não manda pra aba
      Sistema). Online mostra "Desligar". (U1)
- [ ] Aba **Lightbar**: presets rápidos e player-LEDs manuais FUNCIONAM (não são reescritos pela
      paleta automática). Brightness default do perfil `meu_perfil` = 100%. (U9)
- [ ] Aba **Rumble**: "Testar motores" e "Devolver ao jogo" funcionam e NÃO prendem o autoswitch
      (após testar, um novo foco de janela ainda reaplica o perfil ativo normalmente). (U-fix HIGH)
- [ ] Aba **Perfis**: duplo-clique acidental na lista NÃO troca o perfil ativo por engano. (U3-B)
- [ ] Config sobrevive à troca de aba (se ainda sumir, capturar journal — U4 era hipótese Causa A).

## Jogo real (Onda N REPLICA-03 + install)
- [ ] Sackboy com launch option `hefesto-launch %command%`: SEM race "Jogar pelo Hefesto × Sony"
      (curado pelo wrapper no PATH). (U6)
- [ ] Em jogo, DualSense exibem o número DO JOGO; ao fechar o jogo com a Steam viva, a paleta
      volta em ≤~32s. (N)
- [ ] Rumble + gatilhos adaptativos no jogo (branco USB e BT). (guerra de escritores)

## Gyro / motion (Onda G + gyro anterior)
- [ ] DualSense: gyro aiming chega ao jogo via vpad (USB e BT). (GYRO-01, já entregue antes)
- [ ] **Nintendo Pro NO CABO**: `enable_imu` liga o IMU — evtest no node "(IMU)" mostra eixos
      vivos (antes congelados em 0,0,0). 8BitDo intocado. (G1 — só USB nesta fase)
- [ ] `[JOYCON]` limpo no journal durante a adoção do Pro (se houver timeouts, o enable_imu por BT
      segue bloqueado por design).

## Rádio / estabilidade (Onda R)
- [ ] Abrir a Steam NÃO derruba os BT (lembrete: o assassino medido foi o **dongle WiFi Archer
      T3U** associando — se cair, jogar com o WiFi USB realocado/fora, ou aceitar a queda como do
      dongle, não da Steam). Ver `achado-incidente-wifi-bt`.
- [ ] Re-pareamento de controle com bond antigo funciona sem "rejeição" (JustWorksRepairing).
- [ ] `doctor.sh` não acusa "Connected sem hidraw" nem "Paired sem Bonded".

## Áudio (U12 — já resolvido ao vivo)
- [ ] Áudio do sistema funciona (o sink HDMI estava MUTED global; o doctor agora avisa se
      remutar). Nenhum código do daemon mexe em sink.

---

# Ondas S / T / W / L (leva 2026-07-20 tarde — sintoma por sintoma)

> Estas exigem o **ciclo uninstall→install** rodado (aplica o broker, os DKMS e a fiação nova) e
> um **reboot** (os patches DKMS de T e W só valem no próximo boot — o install NÃO recarrega módulo
> com controle/WiFi em uso, por design fail-safe).

## Broker hide-hidraw (Onda S)
- [ ] `systemctl is-active hefesto-hidraw-broker.socket` = active; `scripts/doctor.sh` mostra a
      seção "broker hide-hidraw" verde (ping peer_uid confere, cmd open serviu fd real).
- [ ] **Duplicado curado**: jogo lançado SEM o wrapper (ex.: abrir um Proton direto) — `lsof` no
      hidraw FÍSICO do DualSense não mostra o processo do jogo (`winedevice`), só o do vpad. O
      controle NÃO dobra no jogo.
- [ ] **Gyro sobrevive ao hide**: com o broker ativo, o giroscópio segue chegando ao jogo (o
      motion reader recebe o fd por injeção, não reabre por caminho) — USB e BT.
- [ ] **Fail-safe**: `kill -9` no daemon com físico escondido → em <1s o hidraw volta acessível
      (getfacl com a ACL do usuário) — "duplicado > zero controles" preservado.

## hid-nintendo patchado (Onda T) — VALIDAR APÓS REBOOT
- [ ] `scripts/doctor.sh` seção "DKMS hid-nintendo": mostra o módulo do hefesto carregado
      (`/sys/module/hid_nintendo/parameters/` existe com `bt_probe_retries`, `skip_tx_on_rate_exceeded`).
- [ ] **A/B da cura (gate humano)**: Pro Controller por BT + dongle WiFi ativo (rádio degradado) —
      com o patch, ao cair o link o driver NÃO desregistra: o controle **reconecta sozinho** quando
      o rádio volta (antes morria no probe -110 e só voltava com replug). Observar `[JOYCON-PROBE]`
      no kernel-watch antes/depois.
- [ ] Se um controle Nintendo/8BitDo **regredir** (algo pior que antes), reverter é 1 comando:
      `sudo ./uninstall.sh` volta o in-tree, ou editar `/etc/modprobe.d/hefesto-hid-nintendo.conf`
      (zerar `bt_probe_retries`/`skip_tx_on_rate_exceeded`) e replugar.

## rtw88 patchado + WiFi (Onda W) — VALIDAR APÓS REBOOT
- [ ] `scripts/doctor.sh`: sem "device USB fantasma" e com o rtw88_usb do hefesto carregado
      (`/sys/module/rtw88_usb/parameters/hang_reset`).
- [ ] **Teste do fantasma (gate humano)**: mover o dongle WiFi de porta USB → o `usb X-Y: USB
      disconnect` sai no mesmo segundo (`journalctl _TRANSPORT=kernel -f`), SEM precisar de `unbind`
      manual; `lsusb` × `/sys/bus/usb/devices` sem device órfão; replug reusa o nome `wlx…` sem
      "Arquivo existe".
- [ ] **Medição do LPS (opcional, gate humano)**: `sudo scripts/medir_w2_lps.sh --run` (A/B do
      powersave via nmcli) — se `powersave=2` ganhar com margem clara em p95/perda, ativar por
      `sudo ./install.sh --wifi-powersave-off` (opt-in). Sem número que prove, NÃO ativar.
- [ ] **Coexistência (opcional)**: `sudo scripts/medir_w3_coex.sh --run --evdev <nó>` mede WiFi×BT
      nos 3 braços (ocioso/carga/rfkill). Se a EMI provar culpa do xHCI compartilhado, mover o
      dongle para uma porta do controlador `02:00.0` (portas SuperSpeed livres) — mudança de
      topologia, não gambiarra. **NÃO** usar cabo de rede.

## Lightbar no wake (Onda L)
- [ ] **Gate humano do wake**: com os DualSense em BT exibindo a cor/número certos, **suspender e
      acordar o PC** (ou deixar o controle dormir em BT e acordar) → a lightbar e os player LEDs
      voltam sozinhos à cor/número certos, SEM precisar desconectar/reconectar (antes, um wake sem
      reabrir o handle deixava a lightbar apagada).
- [ ] **Não pisca à toa**: em uso normal (sem wake), a lightbar NÃO fica reenviando reset/piscando —
      o reenvio só dispara na assinatura do wake (nó voltou ao azul-default do kernel).
- [ ] Em **Modo Nativo** (jogo dono do LED), o daemon NÃO reescreve a lightbar (nem na adoção nem
      no wake) — o jogo controla a cor sem interferência.
