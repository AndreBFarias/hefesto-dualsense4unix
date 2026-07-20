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
