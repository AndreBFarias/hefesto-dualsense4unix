# Sprint INFRA 2026-07-18 — PATH-06 · KERNEL-07 · MISC-08

> Causa-raiz e evidências: estudo 2026-07-18 §FATO 0, §P6, §colaterais.

## PATH-06 — o wrapper existe DE VERDADE para a usuária (P1)

1. **Symlink no PATH**: install cria `~/.local/bin/hefesto-launch` →
   `~/.local/share/hefesto-dualsense4unix/bin/hefesto-launch` (mesmo padrão do symlink do
   CLI, install.sh passo 5). Uninstall remove. `which hefesto-launch` passa a funcionar —
   e a LaunchOption pode ser simplesmente `hefesto-launch %command%`.
   ATENÇÃO: manter compatível a string canônica `WRAPPER_LAUNCH`
   (integrations/steam_launch_options.py:61-82) — o formato `sh -c` com caminho absoluto
   continua sendo o que o botão copia (funciona sem PATH); o symlink é conveniência/manual.
2. **Aplicação em massa opcional**: revisar o botão "Aplicar aos jogos da Steam" (aba Sistema):
   deve APLICAR o wrapper a todos os jogos instalados (não só migrar linhas envenenadas) quando
   a Steam está FECHADA (gate `steam -shutdown`/pgrep existente do disable_steam_input) e
   PRESERVAR launch options existentes (prefixar). Diálogo de confirmação temado, contagem
   clara ("N jogos receberão o hefesto-launch"). Se a Steam estiver aberta: instruir e não tocar.
   (Decisão de produto do dia: o popup 1x/jogo continua; isto é a via em-massa consentida.)
3. Doctor: check "wrapper no PATH" + "quantos jogos com wrapper aplicado".

## KERNEL-07 — udev e limpeza (P1)

1. **Regra 70 cobre o vpad**: adicionar match do hidraw do vpad uhid
   (`KERNELS=="0003:054C:0DF2.*"` ou `DRIVERS=="playstation"`) com MODE 0660 + uaccess —
   hoje o acesso do jogo ao vpad depende do steam-devices (terceiro). Portabilidade da v1.
2. **Nova regra js-Motion** (`assets/80-motion-sensors-not-joystick.rules` ou dentro da 78):
   `SUBSYSTEM=="input", KERNEL=="js[0-9]*", ATTRS{name}=="*Motion Sensors*", MODE="0000"` —
   esconde da API js legada os nós de acelerômetro (js2/js4/js6/js8 ao vivo). SDL não usa js*.
3. **Regra 78 ampliada**: cobrir os nomes BT (sem prefixo "Sony Interactive Entertainment") e
   os vpads (`Hefesto Virtual DualSense P* Motion Sensors`) no ID_INPUT_JOYSTICK="" (defesa em
   profundidade; o builtin input_id já cobre o kernel atual).
4. **Assets mortos**: remover do repo `assets/73-ps5-controller-hotplug.rules` e
   `assets/74-*-bt.rules` (descontinuados desde 2026-06-23; install os deleta da máquina) +
   simplificar o skip-list em install.sh:524-527 e o rm compensatório do install_udev.sh
   (manter o rm por 1 release para limpar máquinas antigas — comentário explicando).
5. install/uninstall SIMÉTRICOS para tudo acima, SEM FLAGS. `udevadm trigger` cobrindo
   input (js) além de misc/leds.

## MISC-08 — colaterais do diagnóstico (P1/P2)

1. **policy=max aplica mult 0.7** (BUG): `core/rumble.py:51-91` + quem propaga `custom_mult`
   (profiles/manager, ipc_rumble_policy) — max deve resultar em 1.0; ao vivo
   `profile_rumble_policy_applied mult=0.7 policy=max`. Corrigir + teste de regressão.
2. **Autoswitch GUI-neutra**: wm_class da própria GUI (`Main.py`, `Hefesto-Dualsense4Unix`,
   applet) NÃO conta como janela para troca de perfil (profiles/autoswitch.py) — retém o
   perfil corrente, como o caso "sem informação" da histerese UX-01. Mata o flapping
   vitoriasackboy_nativo do journal (20:15:40-51) e o risco de recriar vpads mid-game.
3. **Vpads não recriam à toa**: toggle de emulação/aplicação de perfil idêntico não faz
   teardown+respawn dos vpads se a config efetiva não mudou (guard por assinatura de config
   nos pontos de `apply_profile_mode`/draft applier) — recriar mid-game invalida os handles
   do jogo (provado ao vivo: Steam nunca reabriu o hidraw6).
4. **EBADF no teardown do co-op**: fechar o fd DEPOIS do join da thread leitora
   (daemon/subsystems/coop.py teardown; warning `evdev_read_lost` 20:15:11).
5. **Telemetria por vpad**: já coberta no REPLICA-03 item 4 (não duplicar).
6. **Doctor**: WARN quando launch_env contém PROTON_ENABLE_HIDRAW (env morta) — sinal de
   estado antigo; refresh via daemon.

## Gate de aceite
- Suíte completa 0 skipped + ruff + mypy + anonimato.
- Ciclo `install.sh` SEM FLAGS rodado na máquina (TTY para o sudo) e `udevadm` provando:
  hidraw do vpad com ACL própria NOSSA (não só steam-devices); js de Motion inacessíveis
  (MODE 0000); `which hefesto-launch` ok.
- journal SEM flapping de perfil com a GUI focada; mult=1.0 com policy=max.
