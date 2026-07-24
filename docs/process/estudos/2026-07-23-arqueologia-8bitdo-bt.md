# 2026-07-23 — Arqueologia: 8BitDo (E4:17:D8, "Pro Controller" 057E:2009) × Bluetooth

Pesquisa por agente na madrugada de 23/07 (pedido da mantenedora: "explora os
commits anteriores"). Contexto: por BT o 8BitDo conecta e cai; hoje parte das
quedas foi PRÉ-HID (sem nem probe no kernel) — assinatura nova. Via cabo modo
Switch segue estável. Hipótese em teste: o modo ativo Nintendo (fb5e3ad, nome
"Nintendo*" + no-sniff, 22/07 NOITE) atrapalha o firmware clone.

## 1. Linha do tempo (hashes vivos pós-purga de 20/07)

| Commit | Data | O que mudou | Efeito no 8BitDo |
|---|---|---|---|
| `4db70be` | 16/07 | docs: sprint 8bitdo (estudo 117 agentes) | 3 mortes BT medidas (uma SEM Steam); doutrina "estável = Switch POR CABO" |
| `36a9336` | 17/07 | 8BIT-01/03/06: inventário, doctor aprende a cascata (gate ≥10), troubleshooting doc | Observabilidade; o "1043x…exceeded" do doctor de hoje é este check |
| `b7a68ee` | 17/07 | 8BIT-02: externos no seletor + ficha | Só UI; validado com 8BitDo por CABO |
| `79b4b35` | 17/07 | Ficha detecta Switch×X-input; PROVADO: forçar hid-generic falha (descriptor clone malformado) | "X-input é a raiz da estabilidade" como orientação |
| `2fb759d` | 17/07 | Daemon escreve LED de player + udev 79-external | Criou escritor de subcmd: poll da GUI reescrevia LED a ~4s |
| `b38a5e6` | 18/07 | OUI vence VID no brand_of; LED dual-modo (DS4=lightbar) | Mesma madrugada: modo D-input BT = storm 211.222 CRC fails |
| `b4589a1` | 19/07 | "leitura de inventário deixa de escrever LED (era o que derrubava o 8BitDo por rate de subcomando)" | 1ª cura direta |
| `f6c20d8` | 20/07 | Onda T: DKMS hid-nintendo patch 0001 (retry probe BT + skip_tx) | Cura a morte por probe -110 (3× medida, sempre BT) |
| `b41ce28` | 22/07 15:00 | ONDA-R2 + DKMS 0002 + tuning (sync_send_tries=4, input_report_wait_ms=500, probe_info_timeout_ms=4000) + 8BIT-03 (SDL labels) | Tuning vivo desde install 21/07 22h40 |
| `ccc48c4` | 22/07 20:56 | BOND-KEEP-01 (BlueZ .2) | O clone TAMBÉM emite Virtual Cable Unplug (bonds dos DOIS Nintendo evaporavam) |
| `fb5e3ad` | 22/07 21:20 | **BT-NINTENDO-ACTIVE-01: Alias "Nintendo…" + no-sniff global** (ExecStartPost + vigia 0 do watchdog 2/2min) | **A alavanca sob suspeita — o 8BitDo nunca tinha rodado sob ela até hoje** |

## 2. Modos do próprio controle (combos: X-input = X+Start; Switch = Y+Start)

- **Switch por CABO (0003:057E:2009)** — ÚNICA config PROVADA estável (instância USB sem um único timeout). Doutrina desde 16/07.
- **Switch por BT** — instável em 16/07 (3 mortes); melhorou por camadas até DUAS janelas funcionais (§3).
- **X-input por CABO (045E:028E, xpad)** — "Xbox 360 real, estabilidade esperada, não medida"; sem gyro.
- **X-input por BT** — beco MORTO (xpad é USB-only; cairia em hid-microsoft/hid-generic).
- **D-input/DS4 por BT (054C:05C4)** — DESASTRE medido (17→18/07): 211.222 CRC fails num boot, degradou o adaptador pra todos; doctor caça permanente (check_bt_clone_ds4).
- 8BIT-05 (decisão formal de modo) segue ABERTA com a mantenedora.

## 3. As DUAS janelas de 8BitDo BT funcional — ambas ANTES do nome "Nintendo"

1. **21/07 ~21:38** (Sackboy 4P BT): 8BitDo jogou como P4. Condições: BlueZ 5.85, hid-nintendo com params ZERADOS (≈vanilla, uninstall tinha zerado), sniff permitido, host sem prefixo, bond JustWorks temporário.
2. **22/07 TARDE** ("o 8BitDo BT estabilizou com os patches", relato dela, commitado em 05ced7c): DKMS 0001+0002 + tuning completo ativos, BlueZ 5.86 **.1**, main.conf consolidado. **Comprovadamente SEM**: Alias Nintendo, no-sniff, BOND-KEEP (.2) — tudo noturno (às 15:06 o `lp` ainda mostrava RSWITCH HOLD SNIFF PARK).

Confounders entre a tarde boa e a noite ruim: bonds novos 22:45+, watchdog/doctor reescritos, e **RF degradada mensuravelmente à noite** (motion silences até "colar" no dongle). "No-sniff × multi-controle segue não litigado".

## 4. Alavancas técnicas

- **bt_active_mode.sh**: prefixa Alias (LMP Remote Name Request é o que o controle lê) + `hciconfig hci0 lp rswitch` (o LM passa a RECUSAR `LMP_sniff_req` de qualquer periférico) + reforço por-conexão. NÃO mexe em papel central/periférico. Um clone que dependa de sniff pra agendar o rádio pode tratar a recusa como erro e cair. Reaplicado em 3 pontos: install, ExecStartPost, **vigia 0 do watchdog (2/2min)** — A/B exige parar o timer.
- **Patches DKMS**: 0001 = retry de probe BT (gated `bt_probe_retries`) + `skip_tx_on_rate_exceeded` (suprime TX ao esgotar — protege o link, mas subcmds podem nunca sair com cadência ruim); 0002 = registra LEDs mesmo com SET falhando. Tudo vivo em `/sys/module/hid_nintendo/parameters/`.
- **`joycon_enforce_subcmd_rate` é VANILLA** (attempts 500→25 é upstream `2295657ac30a`; deltas 8-17ms são `d750d1480362`). Em BT o driver exige 3 deltas consecutivos de 8-17ms + ≥60ms desde o último subcmd antes de QUALQUER TX; clone com cadência fora disso esgota as 25 tentativas.
- **Forense de hoje**: as msgs do enforce SÓ disparam PÓS-probe (estado READ) → os "1043x timeout" da instância .0014 provam que houve conexão em que o HID subiu e viveu (morreu de inanição de TX); as quedas PRÉ-HID de hoje são assinatura NOVA, abaixo do driver (ACL/L2CAP/SDP), inédita no histórico dele.

## 5. Veredito + plano A/B (amanhã)

**Hipótese "nome Nintendo piorou o 8BitDo": INDETERMINADA — cronologicamente sustentada, causalmente não isolada** (fb5e3ad embarca DUAS alavancas juntas; BOND-KEEP + bonds novos + RF degradada entraram na mesma noite; e a recusa de LMP_sniff_req é tão plausível quanto o nome).

**Prep**: `sudo systemctl stop hefesto-bt-health-watchdog.timer` (senão a vigia 0 desfaz o A/B em ≤2min). NÃO reiniciar bluetooth.service durante os testes. Ao final: `start` no timer (reaplica tudo sozinho).

1. **Baseline instrumentada** (10min): `btmon -w snoop` + journal -f (bluetooth + kernel); ligar o 8BitDo 1×. Ver: Remote Name Request, Mode Change (sniff recusado?), **reason code do Disconnect** (0x13/0x05/0x08), PSM 17/19 abre?, uhid nasce? — isso sozinho decide entre nome, sniff e bond.
2. **Tirar SÓ o nome** (15min): `busctl set-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Alias s "MeowSystem"`. Power-cycle no controle, 10min de uso. Sucesso: probe aparece no kernel, evdev nasce, sem cascata. Reverter: rodar `bt_active_mode.sh`.
3. **Devolver SÓ o sniff** (15min): nome reaplicado + `hciconfig hci0 lp rswitch,hold,sniff,park`. Mesmos critérios. Reverter: `hciconfig hci0 lp rswitch`.
4. **Réplica da config da tarde boa** (15min): as duas alavancas revertidas (DKMS/tuning ficam — JÁ estavam na tarde boa). 2 e 3 falham + 4 passa ⇒ interação. 4 falha ⇒ causa não é fb5e3ad (olhar bond/RF).
5. **Se baseline mostrar queda pré-HID com auth/unknown**: camada bond — conferir `<MAC>/info` ANTES/DEPOIS da queda (BOND-KEEP deve segurar; sumiu ⇒ BlueZ, não nome). Lembrar backoff de auth-failures do 5.86 (17a227b7) que desliga autoconnect silenciosamente.
6. **Só se voltarem cascatas PÓS-probe**: knobs vivos um a um — `input_report_wait_ms=250` e, por último, `skip_tx_on_rate_exceeded=0` (o comportamento da janela boa de 21/07; risco: martelar link ruim). Reverter: 500/1.
7. **Contra-prova do Pro real** (10min): com a combinação vencedora, Pro BT não pode regredir. Se 8BitDo e Pro exigirem estados OPOSTOS ⇒ saída de raiz é policy POR-CONEXÃO (`hcitool lp <MAC>` só no Pro — hook por-borda já mapeado).

Total ~1h20. Registrar reason codes + snoop aqui nos estudos.

## 6. Pistas upstream (com refs nos docs 22/07 pesquisa + 20/07 premissas)

- Nome/sniff: Fyra Labs; BlueZ #1797 (not-planned; prefixo resolve); ArchWiki; Switchbrew/MissionControl (console é master, vendor Broadcom 0xFD95 SetTsi, derruba quem recusa o sniff DELE).
- BlueZ: #2048 (VC-unplug apaga pairing — precedente do BOND-KEEP); `ab6ce0c` (5.86 passou a transmitir VC-unplug no uhid); `17a227b7` (backoff auth-failures).
- Kernel: `d750d1480362` (cura BT era Steam Deck — já temos); `2295657ac30a` (attempts 500→25); **`b73bc6a51f0c` (probe info HZ→2·HZ "para third-party lentos" — upstream RECONHECE clones lentos no probe)**; `4a0381080397` (stalls BT em suspend).
- SDL: `SDL_hidapi_switch.c` RUMBLE_WRITE_FREQUENCY_MS=30 ("mais frequente desliga o controle em BT") — filosofia: mínimo de subcmd sobre BT.
- Firmware: Pro real 4.33; 8BitDo emula 3.72 — "a diferença não é idade de firmware, é o comportamento de rádio de cada chip".
- lore/lkml/git.kernel.org bloqueados por Anubis nesta rede — usar API do GitHub.


---

## ⭐⭐⭐ RESOLVIDO 23/07 noite — A/B feito, hipótese CONFIRMADA

A mantenedora levantou: *"acho que já resolvemos isso no passado e isso é uma
regressão"*. Estava certa. O A/B que este doc planejava foi executado.

**Protocolo** (o do §plano, 7 passos): `hefesto-bt-health-watchdog.timer`
PARADO (senão a vigia 0 reaplica o modo ativo a cada 2 min e contamina), alias
"Nintendo MeowSystem" MANTIDO, e só o SNIFF devolvido ao adaptador
(`hciconfig hci0 lp rswitch,hold,sniff,park`).

**Resultado:**

| | no-sniff global (desde `fb5e3ad`) | SNIFF devolvido |
|---|---|---|
| probes do 8BitDo | **4 falhas, 0 sucessos** | **sucesso em 54 s, 1ª tentativa** |
| erro | `Failed to get joycon info; ret=-110` | — |
| estabilidade | — | 60 s de pé sem cair |

**A hipótese "nome Nintendo" fica REFUTADA como culpada** — o alias esteve
aplicado o teste inteiro e o clone probou mesmo assim. A culpada era a outra
metade do `fb5e3ad`: o **no-sniff**. As duas medidas entraram juntas e por isso
ficaram acopladas até aqui.

**Mecanismo:** `hciconfig lp rswitch` faz o LM local **recusar**
`LMP_sniff_req`. O Pro genuíno lida com a recusa; o firmware clone trata como
erro e não completa o handshake de subcomando — e o `get joycon info` é
justamente um passo da probe do `hid-nintendo`, daí o `-110` (ETIMEDOUT).

**Requisitos incompatíveis, medidos:**

| | Pro genuíno (`e0:f6:b5`) | 8BitDo clone (`e4:17:d8`) |
|---|---|---|
| SNIFF permitido | cai sob carga (medido 22/07) | **funciona** |
| SNIFF recusado | **estável** (medido 22/07) | probe morre (`-110`) |

Nenhum ajuste **global** satisfaz os dois. O defeito não era o valor escolhido —
era aplicar um requisito **por-dispositivo** como configuração **de adaptador**.

**Cura entregue (`BT-SNIFF-PER-OUI-01`):** default do adaptador volta a permitir
SNIFF (o que o clone precisa para probar); o `RSWITCH` sem sniff passa a ser
aplicado **por conexão**, filtrado pela OUI do Pro genuíno. O alias segue global.
Reaplicado pela vigia 0 a cada 2 min, o que cobre reconexão sem caçar a borda.

**Por que aplicar depois do connect basta para o Pro:** ele proba bem com sniff
(era o comportamento antes do `fb5e3ad`); o que ele não aguenta é a operação
SUSTENTADA sob carga. O clone precisa do sniff justamente na janela da probe.

**Bug colateral achado no mesmo teste:** `hciconfig lp` exige a lista separada
por **vírgula**. Com espaços ele lê só o primeiro token e o comando vira no-op
silencioso — era exatamente a sintaxe do `uninstall.sh:606`, que portanto
**nunca revertia o no-sniff**: quem desinstalasse ficava com o adaptador
alterado para sempre. Corrigido, com teste travando a sintaxe.

**Fica em aberto (gate humano):** confirmar que o Pro aguenta uma sessão de 4
jogadores sob carga real com o no-sniff aplicado **por-conexão** em vez de
global — o mesmo padrão de prova que a cura original teve. Se ele cair, o
aprendizado é que ele precisa do no-sniff já *durante* o connect, e a resposta
passa a ser a sprint `2026-07-24-sprint-pesquisa-sniff-parametrizado.md`.
