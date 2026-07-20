# HANDOFF 2026-07-20 — maratona das 5 ondas (retomar aqui)

> **ESTE É O PONTO DE RETOMADA.** Supersede o ÍNDICE da maratona como ponteiro atual.
> Leia a memória do projeto + este arquivo antes de tocar em qualquer coisa.
> Regra da mantenedora nesta noite: **materializar tudo, nada pode passar despercebido.**

## Onde estamos numa frase

5 ondas (N, R, HANG-01, G, U) **implementadas, verdes e auditadas em isolamento**, TODAS no
**working tree NÃO commitado**. Falta: (1) folhear o resultado da auditoria cross-cutting em voo;
(2) commit anônimo; (3) re-rodar install; (4) validação ao vivo; (5) Onda S (broker); (6) uns
poucos residuais listados abaixo. NADA foi commitado; NADA foi instalado pós-ondas.

##  Auditoria cross-cutting — CONCLUÍDA (workflow wkrw0pbxv)

Rodou e ACHOU 3 bugs REAIS de interação entre ondas que as auditorias isoladas não pegaram —
todos corrigidos, com a suíte re-verde. Prova de que valeu:
1. **HIGH** — `led.set`/`led.player_set` (U) armavam a trava manual no mesmo handler cujo caminho
   de escrita ignora `display_authority=='game'` (N), matando o único auto-reparo (a cor manual
   ficava presa até o alt-tab). FIX: chamar `reassert_resolved_outputs()` ANTES de armar a trava
   (ipc_handlers.py ~408-420) — em jogo, a cor do jogo vence na hora.
2. **MEDIUM** — `identity.renumber` (U) tomava o lock do external_registry síncrono e sem timeout
   no event loop, furando o isolamento do HANG-01. FIX: `asyncio.wait_for(asyncio.to_thread(
   _renumber_locked), timeout=5s)` → devolve `{ok:false, reason:"lock_timeout"}` em vez de travar
   (ipc_handlers.py ~534-563, `_IDENTITY_RENUMBER_LOCK_TIMEOUT_SEC`).
3. **MEDIUM** — `enable_imu` (G) segurava a seção crítica do `ExternalLedSync.tick` ANTES do laço
   de LED-defense (N NUMA-03.4), apagando a defesa dos OUTROS devices até o próximo hotplug. FIX:
   enable_imu reestruturado fora da seção crítica do LED-defense (external_identity.py ~594-645).

**GATE FINAL VERDE (autoritativo, medido à mão pós-fix): 3948 passed, 0 failed, 0 skipped; ruff
0.15.20 limpo; mypy limpo (147 arq.); check_anonymity OK; bash -n install/uninstall OK.**
Diff acumulado final: 55 arquivos, +4964/-365. As 5 ondas estão prontas para commit.

## Estado técnico exato

- Branch `sprint/harmonia-uhid`, HEAD 27b51d5. **Working tree: 55 modificados + 23 novos**
  (+4964/-365). Gate final verde (pós-cross-cutting, medido à mão): **3948 passed, 0 failed,
  0 skipped**; ruff 0.15.20 limpo; mypy limpo (147 arquivos); check_anonymity OK; bash -n OK.
- Arquivo novo de src: `daemon/subsystems/game_signal.py`. 13 arquivos de teste novos.
- Fix não-commitado que PRECEDE as ondas: **BLUEZ-UHID-01** (identidade phys/uniq nos filtros
  `_is_virtual_hidraw`/`_is_virtual_evdev` — NÃO reverter; sem ele o daemon fica cego aos BT no
  BlueZ 5.85).

## O que cada onda entregou (todas com teste falha-sem/passa-com + auditoria adversarial)

1. **N — numeração una** (`sprint-numeracao-una.md`): game_signal + display_authority
   (game/daemon/unknown); gate de exibição no backend (só funde camada GAME quando `_game_wins`);
   retain-latest + replay 1x; defend_display (repinta escritor estrangeiro); NUMA-03.4 (LED de
   externo defendido por autoridade); NUMA-04 (CONTROLLERS_FILE_LOCK + cross-check no load);
   NUMA-05 (fim do posicional, state_full game_signal, doctor). Auditoria: HIGH réplica retida
   vazava pós-UHID_CLOSE → purge no close; MEDIUM wrapper_game_running.
2. **R — rádio/install** (`sprint-onda-r-radio-install.md` + `estudo-bluez-backport-onda-r.md`):
   install integra backport BlueZ 5.85 (idempotente, SHA256, VERSOES-ANTERIORES, aviso, --yes,
   no-op ≥5.79), JustWorks como asset canônico (`assets/bluetooth/hefesto-justworks.{conf,block}`),
   dep bluez-tools + `assets/systemd/hefesto-bt-agent.service` (enable --now), DEBIAN_FRONTEND=
   noninteractive nas apt calls. Uninstall simétrico com --keep-bluez. Higiene: SwitchSupport no
   disable_steam_input.sh, TAG uaccess morta removida das .rules ≥73, storm.conf órfão no
   --keep-udev.
3. **HANG-01** (`sprint-hang-01-tick-resiliente.md`): poll loop nunca bloqueia — _sync_external_leds
   vira task com wait_for(10s) + guard de reentrância + degradação (re-arma no input_dir_change);
   **pool DEDICADO `_external_executor` (hefesto-ext, 1 worker) isolado do pool do read_state** (fix
   do HIGH da auditoria — o hang voltaria adiado sem isso); side-fix thread-safety no close do evdev.
4. **G — gyro/doctor** (`sprint-onda-g-gyro02-doctor.md`): `enable_imu` (USB-only + OUI E0:F6:B5,
   1x/adoção, backoff; 8BitDo/BT BLOQUEADOS por design); doctor seção "Rádio e pareamento" (bluez
   <5.79, bt-agent, Connected-sem-hidraw, Paired-sem-Bonded, sink muted); ff_play_count/motion_hz
   por vpad no state_full.
5. **U — 13 regressões GUI** (`sprint-onda-u-gui-regressoes.md` + `estudo triagem`): **Causa A**
   (o "perfil eterno") = trava manual armada em todos os apply-IPCs + clear no rumble.passthrough;
   identity.renumber (compact sob lock, gated por sessão); toggle Início in-place; D4 estende p/
   player_leds; brightness meu_perfil 0.4→1.0. Auditoria: HIGH trava-sem-fim do rumble transitório
   → clear no passthrough; MEDIUM TOCTOU no renumber → lock_for_renumber.

## PENDÊNCIAS ORDENADAS (retomada) — NADA pode passar despercebido

**A. Fechar as 5 ondas (o que a mantenedora escolheu, adiado para a próxima):**
1. Folhear/rodar a auditoria cross-cutting (wkrw0pbxv) e confirmar suíte verde pós-fix.
   ver `feedback` de anonimato). Sugestão de fatiamento: (i) estudos/mapa/triagem + scrub de MACs;
   (ii) N; (iii) R; (iv) HANG-01; (v) G; (vi) U. Ou um commit único da leva — decidir.
3. **Re-rodar install** (EU consigo, método PTY validado — ver
   [[reference_sudo_ticket_tty_notty]]):
   `script -qec "bash -c 'echo ***SENHA-REMOVIDA-DO-HISTORICO*** | sudo -S -v 2>/dev/null && ./install.sh --yes'" /dev/null`
   Isso aplica no SISTEMA: udev 77/79 novas, doctor novo, bt-agent.service, passo do backport
   (no-op, 5.85 já instalado), JustWorks (já no main.conf), SwitchSupport. **HOJE o install NÃO foi
   re-rodado após as ondas** — só o código do daemon (venv editável) está ativo; a metade-sistema não.
4. **Validação ao vivo** — ver `CHECKLIST-VALIDACAO-5-ONDAS.md` (materializado junto).

**B. Onda S — broker fd-injection (a mais cara/arriscada, dedicada):**
- Base: `docs/process/future-broker/` (código parkado, usa ACL/chmod — TROCAR por fd-injection) +
  `estudo-broker-hide-hidraw.md` + `sprint-broker-hide-hidraw-onda-dedicada.md`.
- Regras: cmd `open` + SCM_RIGHTS (reader nunca reabre por caminho); sequência visível→abrir-fds→
  hide; 9 HIGH conhecidos; re-auditoria antes do install.
- **ARMADILHA NOVA**: com BlueZ 5.85 os físicos BT moram em `/devices/virtual/misc/uhid/` — o
  validador de identidade do broker precisa da MESMA lógica do BLUEZ-UHID-01 (HID_PHYS/HID_UNIQ do
  uevent do pai HID; jamais topologia).

**B2. Onda T — o que derruba o Pro Controller BT** (`sprint-onda-t-proBT-coexistencia.md`):
a mantenedora relatou 20/07 que AINDA cai. **A Onda S NÃO cura isso** — o broker só tira o cliente
Steam (contribuinte); os assassinos medidos são o dongle WiFi (EMI/xHCI vizinho) e o muro do
kernel hid-nintendo. **T2 é a cura de raiz e a prioridade: PATCH do driver `hid-nintendo`** (parar
de desistir do controle sob rádio degradado — esgotamento não-fatal com backoff, tolerância por
transporte, module params; hoje há ZERO params), entregue por DKMS + preparado para upstream.
A parte de rádio WiFi migrou para a Onda W. "Usar cabo" foi REJEITADO como gambiarra.

**B3. Onda W — WiFi na raiz** (`sprint-onda-w-wifi-raiz.md`): DÍVIDA — pedido de 19/07 que caiu no
vão (nenhuma linha nossa toca WiFi). W1 = patch do `rtw88` para o bug do FANTASMA USB (driver
segura o device em loop de -71; disconnect nunca completa — provado ao vivo 20/07), via DKMS +
upstream; W2 = `disable_lps_deep=Y` com medição A/B; W3 = coexistência WiFi×BT medida (não
"usar cabo" — REJEITADO como gambiarra pela mantenedora); W4 = avaliar driver out-of-tree.

**C. Residuais que NÃO podem sumir:**
- **U — INVESTIGAR_AO_VIVO** (triagem): U4 (config some ao trocar aba — hipótese = Causa A, re-testar
  isolado), U7 (Gatilhos não aplica — já protegido, reproduzir se persistir), U8 (por-controle não
  persiste ao reconectar — aplicar Causa A e testar reconexão isolada). **U5/U6** = re-teste
  (curados por install: botão "Aplicar aos jogos" existe, wrapper no PATH). **U13** = documentar
  convivência input-remapper no doctor/README (só doc, não feito).
- **R — 3 minors cosméticos**: --keep-bluez no cabeçalho narrativo (não no bloco "Flags:") do
  uninstall; VERSOES-ANTERIORES.txt hardcoda `:amd64`; (ambos inofensivos em amd64).
- **Higiene de fora das ondas** (mapa §3.7): CI incluir tests/core; faixa cega ~120-140 testes GUI
  headless; venv legado; acentuação só-linhas-tocadas; cosmic-settings/applet dessincronizam pós-
  restart do bluetoothd (bug da System76 — nota no doctor, não vale patch agora).

## Estado do SISTEMA vivo (para não recriar o que já existe)

- **bluez 5.85** backport INSTALADO (.debs + SHA256SUMS + VERSOES-ANTERIORES.txt em
  `~/.cache/hefesto-dualsense4unix/bluez-backport/`). Bonds antigos migraram fora; os 4 controles
  foram re-pareados hoje (agora só 1 conectado — normal, a mantenedora desligou os outros).
- `/etc/bluetooth/main.conf` tem 2 blocos hefesto por sentinela: FastConnectable + JustWorksRepairing.
- `hefesto-bt-agent.service` NÃO instalado (install não re-rodado) — o asset existe.
- daemon `hefesto-dualsense4unix.service` ativo (venv editável = código das ondas ATIVO).
- `controllers.json`: externals {Nintendo E0:F6:B5=2, 8BitDo E4:17:D8=3}, slots DualSense vazios.

## Regras invioláveis (lembrete)
Install SEM FLAGS; uninstall simétrico; gate = pytest 0-skipped + ruff 0.15.20 + mypy +
check_anonymity; commits anônimos; testes GUI sem `import gi` no topo; não reiniciar bluetoothd em
runtime; não tocar nos filtros _is_virtual_* (BLUEZ-UHID-01); materializar estudos + memória.
