# 2026-07-22 (noite) — Incidente pós-reboot: watchdog derruba BT são + lag por RF

Sessão ao vivo pós-reboot (boot 22:34), com Sackboy aberto durante quase todo o
diagnóstico — por isso TODA a investigação foi read-only e as únicas mudanças
vivas foram atômicas e sem reinício de processo (Trusted=true; scripts oneshot).

Docs-irmãos: `2026-07-22-pesquisa-pro-controller-bt-e-lightbar-keepalive.md`
(BOND-KEEP-01, BT-NINTENDO-ACTIVE-01, KEEPALIVE-01),
`2026-07-22-diagnostico-gui-perfis-autoswitch-e-fixes.md` (autoswitch F2,
RESET-03), `2026-07-21-sprint-pesquisa-bluez-estabilidade.md` (ONDA-R2,
COMPAT BLUEZ-586-CTL-01).

## Timeline medida (journal do boot 22:34)

- 22:34 — boot; bluetoothd 5.86 (backport .2, BOND-KEEP-01) sobe; controles
  reconectam ao longo dos minutos seguintes.
- 22:41:42 — `hefesto-bt-watchdog: estado doente confirmado (8 recusas/10min,
  0 conectados) — reiniciando bluetooth.service` — **com 3 controles
  conectados** (o MESMO tick aplicou link policy em 3 handles vivos: roxo,
  Pro, 8BitDo).
- 22:43:13 — stop+start efetivo do serviço → todos os controles caem ("um a
  um" na UI; applet mostra BT off; depois "liga do nada"). No mesmo segundo,
  o snapshot do ExecStopPost FALHA: `install: não foi possível mudar as
  permissões de .../bt-bonds/20260722-224313: Arquivo ou diretório
  inexistente` (DOIS processos de snapshot no mesmo segundo — PIDs 7169/7184).
- 22:43–22:45 — 8BitDo E4:17:D8:00:00:02 órfão (bond comido no crash #6 de
  21/07; re-pair explícito estava pendente) martela reconexão: `Refusing
  connection ... unknown device` a cada ~20s. Watchdog segue contando
  "doente" (11→13→14 recusas) mas o rate-limit segura novos restarts.
- ~22:45–48 — re-pairs pós-restart (página BT do COSMIC + JustWorks) gravam
  bonds EM DISCO: **4/4 MACs com `<MAC>/info` + LinkKey** (primeira vez desde
  o achado "bonds temporários"). 8BitDo desligado pela mantenedora → recusas
  cessam 22:45:52 e envelhecem pra fora da janela de 10 min.
- 22:48:33 — autoswitch (AUTOSWITCH-HEAL-01, curado ontem) cede o override
  manual ao jogo: `profile_activated name=sackboy_nativo origin=autoswitch`
  → lightbar+gatilhos mudam = **checklist F2 funcionando como desenhado**
  (a mantenedora estranhou porque o autoswitch passou dias morto).
- 22:48:37 — `uhid_replica_ativa` trigger L/R players 1–2: o caminho
  jogo→vpad→físico de gatilhos adaptativos está VIVO.
- 22:4x–22:56 — `motion_reader_silencio_reabrindo` recorrente (silêncios
  >1.1s no hidraw BT ≈ centenas de reports perdidos por rajada) até ela
  APROXIMAR os controles do dongle; depois cessa. RSSI então: -34/-37 dBm.
  Relato dela: antes ~2 m sem lag; agora precisa "colar" = link budget caiu.

## Causas-raiz

1. **WATCHDOG-FP-01 — falso-positivo duplo do bt_health_watchdog.sh:**
   a. Contagem de conectados via `bluetoothctl devices Connected` → o 5.86 é
      MUDO no one-shot e a função-sombra interativa TAMBÉM se provou cega
      nessa consulta → `CONECTADOS=0` sempre → o guard "nunca derrubo sessão
      viva" nunca agiu. (O gate "0 conectados" nem estava especificado nos
      docs de desenho — lacuna; o aviso COMPAT BLUEZ-586-CTL-01 previa a
      sombra.)
   b. Recusas de MAC SEM objeto no BlueZ contadas como doença. Recusar órfão
      é o daemon SÃO cumprindo o protocolo; a doença real medida em 21/07 era
      recusar device PRESENTE na lista.
   Efeito colateral: vigias 2/2b iteravam lista vazia → 4 controles com
   `Trusted=false` a sessão toda (reconexão entrante por conta do agente).
2. **SNAPSHOT-LOCK-01** — ExecStopPost + segunda instância no mesmo segundo →
   colisão no diretório-timestamp → `install -d` falha no chmod. Regressão
   inédita (o invariante "nunca fotografa vazio" trata de OUTRA coisa).
3. **doctor.sh cego nos checks BT** — `timeout 4 bluetoothctl ...` executa o
   BINÁRIO e pula a função-sombra → `check_bt_clone_ds4` e `check_bt_radio`
   mudos (o warn de `Trusted: no` existia e nunca disparou).
4. **Input lag "absurdo" em todos os controles BT = camada RF**, não pipeline:
   silêncios de motion >1.1s; vpad P1 a 58 syn/s com maxgap 145 ms vs P2
   105/s; melhora imediata ao aproximar; WiFi já preso em 5 GHz (canal 161);
   dongles em xHCI separados (Bus 001 × Bus 004) → **EMI aérea** (ruído
   broadband do link USB3 do T3U cai em 2.4–2.5 GHz) + margem RF. Saturação
   multi-controle segue refutada (2 DS + 8BitDo conviviam bem); latência do
   no-sniff global em multi-controle segue ponto NÃO litigado.

## Curas entregues (22/07 noite)

- `scripts/bt_health_watchdog.sh` (**WATCHDOG-FP-01**): toda consulta de
  estado via D-Bus (`_dbus_device_paths`/`_dbus_device_prop`); recusa só
  conta com objeto presente (órfãs viram log informativo); vigias 2/2b agora
  enxergam de verdade. `bluetoothctl` fica SÓ no pair via `_btctl_lento`.
- `scripts/bt_bonds_snapshot.sh` (**SNAPSHOT-LOCK-01**): `flock -w 30` no
  DST_ROOT + sufixo `-$$` no timestamp + criação do DST tolerante (loga e
  sai 0; o timer cobre).
- `scripts/doctor.sh`: `check_bt_clone_ds4`/`check_bt_radio` reescritos sobre
  D-Bus (helpers `_dbus_bt_*`); conselho de trust atualizado para busctl.
- Instalados pontualmente em `/usr/local/lib/hefesto-dualsense4unix/`
  (`install -m 755`, mesmos alvos do install.sh:1229) — scripts oneshot,
  NENHUM processo vivo reiniciado. Watchdog novo rodado 1x ao vivo: rc=0,
  silêncio (saúde), sessão intacta.
- Estado vivo saneado: `Trusted=true` nos 4 via busctl; 4/4 bonds com
  LinkKey em disco; snapshot 22:51 fotografou o estado bom.
- Suíte: `tests/unit/test_bt_resilience_assets.py` 17/17 (asserts de
  invariantes preservados de propósito: "nunca derrubo sessão viva",
  "rate-limit", "promoted-", "_btctl_lento 25 pair", "snapshot recusado",
  "COMPAT BLUEZ-586-CTL-01").
-  3 arquivos UNCOMMITTED (`bt_health_watchdog.sh`, `bt_bonds_snapshot.sh`,
  `doctor.sh`) — commit é decisão da mantenedora.

## Tradução dos sintomas relatados

| Sintoma relatado | Explicação medida |
|---|---|
| "desligaram um a um / BT off do nada / ligou do nada" | restart do bluetooth.service pelo watchdog (22:43); bonds sobreviveram (BOND-KEEP + re-pair) e tudo voltou |
| "8BitDo conecta e desliga em loop na página do BT" | órfão de bond martelando page + `unknown device`; parou quando o bond foi regravado (22:45) e ele foi desligado |
| "lightbar/gatilhos mudaram sozinhos ao abrir o jogo" | autoswitch cedendo ao perfil `sackboy_nativo` (decisão F2, funcionando pela 1ª vez em dias) |
| "gatilhos não ficam conectados" | `sackboy_nativo` tem `triggers: Off` = o JOGO manda os efeitos (e mandou às 22:48:37); em menu/contexto sem efeito o gatilho fica solto |
| "numeração estranha do Nintendo" | renumeração pós-restart do serviço; perfis por-MAC preservados; Steam Input confirmado OFF no Sackboy |
| "input lag absurdo em todos" | camada RF (EMI/margem), melhora ao aproximar; ver §4 |

## Pendências / gates

1. Religar o 8BitDo: LIBERADO (watchdog não pune mais órfão; bond+trust em
   disco). Se pedir pareamento do zero, fazer com jogo fechado.
2. BSSID lock da Beholder + desligar background scan do NM — **conferir o
   BSSID real na hora** (docs divergem: 48:B2:5D:00:00:07 × 48:b2:5d:00:00:06);
   aplicar só com rede/jogo ociosos.
3. Física RF (decisão dela): extensor USB2 ≥20 cm pro dongle BT fora da
   sombra do painel USB3/T3U; ou T3U fora durante co-op; ou voltar o cabo.
4. Gate lightbar BT (RESET-03/KEEPALIVE-01): reconectar o roxo BT com jogo
   fechado → barra na cor do slot.
5. Rodar `scripts/doctor.sh` pós-sessão — os checks BT agora falam.
6. Lacuna aberta: latência do no-sniff global com 3+ controles — só medir
   (A/B) se o lag persistir com RF limpo.

## Adendo madrugada 23/07 (00:30–01:15) — re-pairs, evaporação em massa e recuperação

- **Roxo**: Pair() explícito scriptado OK (bluetoothctl interativo + agent
  NoInputNoOutput + default-agent). 1ª reconexão morreu com `auth_callback()
  Access denied` → **hefesto-bt-agent ZUMBI** (não respondia; o systemd só o
  matou com SIGKILL/timeout). Agente travado = RequestAuthorization sem
  resposta = input negado = firmware desliga sozinho (~10 s, azul default,
  sem player LED). **Lição: após bluetoothctl interativo com default-agent,
  SEMPRE reciclar o hefesto-bt-agent** (e ele trava pra morrer: kill -9 +
  start). 2ª falha: probe `hid_playstation` `Failed to retrieve feature
  reportID 32: -5` → probe morta (kernel NÃO retenta; reconectar = nova
  probe) — passou na reconexão seguinte.
- **8BitDo**: re-pair saiu pelo caminho entrante (meu pair explícito deu
  `AlreadyExists`). BT segue conecta-e-cai PRÉ-HID (kernel sem nem a probe).
  Cabo modo Switch = estável. A/B pra amanhã: prefixo "Nintendo" no host
  (entrou 22/07 NOITE, fb5e3ad) × "8BitDo BT estabilizou" (22/07 TARDE, sem
  o prefixo) — hipótese não-litigada; agente de arqueologia despachado.
- **MMJ "3 modos quebraram"**: trocas de modo a quente 00:50:03→00:51:12 com
  o jogo abrindo 00:51:31 → pads órfãos do Steam Input (o "↑ infinito", como
  21/07). Protocolo: modo → 5 s → abrir o jogo; órfão = fechar jogo +
  reiniciar Steam. Ideia da mantenedora (hefesto matar/reabrir a Steam ao
  aplicar perfil): REJEITADA como automático (autoswitch troca perfil o
  tempo todo; SIGKILL arrisca corromper localconfig.vdf no flush); fica o
  trio: vpad-neutro-antes-de-destruir + GUI impedir troca de modo com jogo
  aberto (ambos já candidatos de 22/07) + ação OPT-IN "Reiniciar Steam"
  graciosa (`steam -shutdown`, nunca kill).
- ⭐⭐ **CAUSA-RAIZ NOVA — TemporaryTimeout completa o que o VCU começou**:
  o BOND-KEEP-01 bloqueia o `device_remove_bonding()` imediato, mas o
  caminho do Virtual Cable Unplug ainda marca o device TEMPORARY → ~30 s
  após o disconnect o BlueZ remove o device INTEIRO, **storage em disco
  incluso**. Medido: roxo+8BitDo pro cabo (00:54) e branco+Pro desligados
  (~01:0x) → os 4 bonds evaporaram (mtime do adapter dir 01:04); bluetoothd
  vivo (PID 7188), lista vazia, `hcitool con` vazio. → **patch .3**: manter
  o device não-temporário no unplug (ou re-marcar temporary=false).
- ⭐ **Recuperação por-idade-de-key** (conceito novo): snapshot válido é
  POR CONTROLE = o mais recente APÓS o último (re-)pair daquele controle
  (é a key que o controle ainda carrega). Restaurado num stop único:
  branco←003613 (re-pair 23:41), Pro←000613 (re-pair 23:44), roxo←005113
  (pair 00:31); 8BitDo SEM foto válida (key 00:42 nunca fotografada) →
  re-pair manual amanhã. Final: 3× Paired+Bonded+Trusted em disco e no
  D-Bus; snapshot novo 20260723-011411 (3 bonds).
- ⭐ **Lição operacional — bus-activation cancela stop**: com GUI/applet
  consultando org.bluez, todo `systemctl stop bluetooth` é cancelado por
  D-Bus activation ("Job canceled"; o restore.sh das 01:05 abortou
  silencioso assim: set -e no stop cancelado, e o "restaurado" nunca
  imprimiu). Stop de verdade: `systemctl mask --runtime bluetooth.service`
  → stop → mexer no storage → unmask → start. → **fix no
  bt_bonds_restore.sh amanhã** (incorporar mask/unmask + verificação
  is-active pós-stop).
- Pós-restart do bluetoothd o **hefesto-bt-agent precisa re-registrar**
  (registro morre com o daemon) — reciclado e "Default agent requested" .
