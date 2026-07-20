Assuma o hefesto-dualsense4unix como cérebro e executor. Ultracode ON, agentes em Sonnet.

LEIA PRIMEIRO, nesta ordem: a memória do projeto, depois
docs/process/HANDOFF-2026-07-20-maratona-5-ondas.md (ponteiro de retomada, tem TUDO: as 5 ondas
prontas no working tree não commitado, gate final 3948/0/0, pendências ordenadas e residuais).

Sudo pré-autorizado: senha ***SENHA-REMOVIDA-DO-HISTORICO***. Você CONSEGUE rodar o install sozinha — método PTY validado
(ver memória reference_sudo_ticket_tty_notty):
script -qec "bash -c 'echo ***SENHA-REMOVIDA-DO-HISTORICO*** | sudo -S -v 2>/dev/null && ./install.sh --yes'" /dev/null

EXECUTE nesta ordem, materializando sprints antes de despachar agentes:

1. COMMIT das 5 ondas prontas (N/R/HANG-01/G/U). Commits temáticos, ANÔNIMOS (check_anonymity é
   mypy + check_anonymity.

2. INSTALL: rode você mesma pelo método PTY acima. O install NÃO foi re-rodado depois das ondas —
   a metade-sistema (udev 77/79, doctor novo, hefesto-bt-agent.service, passo do backport BlueZ,
   JustWorks, SwitchSupport) ainda não está aplicada. Depois: doctor.sh e confirme verde.

3. ONDA S — broker fd-injection (a mais cara/arriscada; specs em
   docs/process/sprints/2026-07-19-sprint-broker-hide-hidraw-onda-dedicada.md +
   docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md + código parkado em
   docs/process/future-broker/). Regras: cmd `open` + SCM_RIGHTS (o motion reader NUNCA reabre por
   caminho); sequência visível→abrir-fds→hide; os 9 HIGH conhecidos da auditoria anterior.
   ARMADILHA NOVA E OBRIGATÓRIA: com BlueZ 5.85 os controles BT FÍSICOS moram em
   /devices/virtual/misc/uhid/ — o validador de identidade do broker precisa da MESMA lógica do
   fix BLUEZ-UHID-01 (HID_PHYS/HID_UNIQ do uevent do pai HID; JAMAIS topologia), senão o broker
   trata os controles BT reais como vpad.

4. ONDA T — o que derruba o Pro Controller BT (sprint já materializado:
   docs/process/sprints/2026-07-20-sprint-onda-t-proBT-coexistencia.md). ATENÇÃO: a Onda S NÃO
   cura isso; os assassinos medidos são o dongle WiFi (EMI/xHCI vizinho — a mantenedora já trocou
   a porta, MEDIR o efeito A/B) e o muro do kernel hid-nintendo.
   *** T2 É PRIORIDADE E É CURA NA RAIZ, NÃO CONTORNO ***: a mantenedora decidiu CONSERTAR O
   KERNEL. Patch do driver hid-nintendo (parar de DESISTIR do controle sob rádio degradado:
   esgotamento não-fatal com backoff, tolerância adaptativa por transporte BT×USB, e module params
   para os limiares — hoje há ZERO params, medido), entregue por DKMS integrado ao install
   (idempotente, uninstall simétrico, fallback pro módulo in-tree se o DKMS falhar), com A/B ao
   vivo e o patch formatado para envio ao linux-input. Pesquisar upstream ANTES de escrever (pode
   já existir patch para portar). Entregue também T1 (coexistência + check no doctor).

5. ONDA W — WiFi na raiz (sprint: docs/process/sprints/2026-07-20-sprint-onda-w-wifi-raiz.md).
   DÍVIDA RECONHECIDA: a mantenedora pediu isso em 19/07 e NADA foi feito (grep por
   rtw88/wifi/wlan no repo = vazio). Entregas: W1 patch do rtw88 para o BUG DO FANTASMA USB
   (driver segura o usb_device em loop de -71 e o disconnect nunca completa — PROVADO ao vivo),
   via DKMS + upstream; W2 disable_lps_deep=Y medido A/B; W3 coexistência WiFi×BT medida (contadores
   HCI + reports perdidos, com WiFi ocioso/carregado/rfkill) e separação de xHCI; W4 avaliar driver
   out-of-tree 88x2bu com dados. PROIBIDO propor "usar cabo de rede" — a mantenedora rejeitou como
   gambiarra; a meta é WiFi bom E BT estável ao mesmo tempo.

6. AUDITORIA ADVERSARIAL FINAL de TUDO (as 5 ondas já commitadas + S + T juntas), incluindo lentes
   de INTERAÇÃO entre ondas — foi assim que pegamos 3 bugs reais que as auditorias isoladas não
   viram. Verifique cada achado com um refutador antes de corrigir. Gate final verde.

7. VALIDAÇÃO AO VIVO: entregue à mantenedora o docs/process/CHECKLIST-VALIDACAO-5-ONDAS.md
   atualizado com os itens de S e T, para ela jogar em família e conferir sintoma por sintoma.

LIÇÃO METODOLÓGICA (erro real cometido em 20/07): `journalctl -k` IMPLICA `-b` (só o boot atual).
Para histórico use `journalctl _TRANSPORT=kernel`. Uma conclusão forte ("nunca existiu") foi tirada
de uma busca cega e estava ERRADA — sempre confirme o alcance da consulta antes de concluir.

REGRAS DA CASA (invioláveis): install SEM FLAGS (flags só opt-out), uninstall simétrico; gate =
pytest 0-skipped + ruff 0.15.20 + mypy + check_anonymity; commits anônimos; testes de GUI NUNCA
importam gi no topo; não reiniciar bluetoothd em runtime; NÃO tocar nos filtros
_is_virtual_hidraw/_is_virtual_evdev (BLUEZ-UHID-01) nem na fiação game_signal/display_authority;
materializar todo estudo de agentes em docs/ + memória; nunca re-pesquisar o que os estudos já
cravaram (há 20 becos refutados catalogados no mapa).
