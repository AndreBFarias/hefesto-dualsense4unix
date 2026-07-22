# Sprint (pesquisa): estabilidade do bluetoothd — qual BlueZ e qual integração

**Status**: pesquisa CONCLUÍDA (22/07 madrugada, 4 agentes + medição local ao vivo);
resultados na seção "Resultados da pesquisa" abaixo. Decisão de versão/integração
pendente — dela.
**Dona da decisão**: mantenedora. Este doc descreve o problema e as perguntas —
sem viés de versão; os resultados da pesquisa é que apontam a melhor versão e a
melhor forma de integrá-la ao projeto.

## Requisito (o que "resolvido" significa)

Bluetooth confiável no uso real: a usuária liga os controles quando quer jogar e
eles conectam — sem o serviço cair, sem perder pareamentos, sem ficar dias sem
usar BT e ele quebrar exatamente na hora do uso. Crash de `bluetoothd` que
destrói bonds é falha CRÍTICA, não ruído aceitável.

## Fatos medidos (nesta máquina; sem interpretação)

1. **BlueZ 5.72 (noble stock, até 19/07)**: 5 crashes registrados em 5 dias
   (heap corruption / SEGV no plugin input / HIDP). Também: família de bugs
   #815 (input vira uhid ≥5.73; curas relevantes só ≥5.79), bond quebrado sem
   re-pair automático, SDP ausente pós-crash. Estes problemas motivaram o
   backport (estudo 2026-07-19).
2. **BlueZ 5.85 (backport, 19→21/07)**: 1 crash registrado (21/07 22:14:34):
   `malloc(): unaligned fastbin chunk detected 2` → ABRT. Gatilho reproduzível
   em tese: dois controles Nintendo (modo Switch) desligados simultaneamente
   (rmmod do driver HID) → bluetoothd entra em loop de reconexão "Host is down"
   nos dois MACs (~2 min) → heap corrompe. Sequelas: TODOS os controles caem;
   bonds destruídos (2 controles) ou degradados (trust perdido); o processo
   renascido opera DOENTE (recusa "unknown device" para device que ele mesmo
   lista; SDP em loop) até restart do serviço.
3. **Sem core dump persistido** do crash de 21/07: `coredumpctl` vazio e
   `/var/crash` sem entrada (apport ignora pacote fora da distro). O crash
   anterior ao backport também não tem dump analisado.
4. Upstream: LP #2137758 (HIDP heap corruption) sem fix conhecido até 5.85
   (verificação de 19/07; re-verificar no estado atual do upstream).
5. Amostras pequenas: 5 crashes/5 dias (5.72) vs 1 crash/2 dias (5.85) NÃO
   estabelecem qual versão é mais estável — os regimes de uso foram diferentes
   (o dia 21 teve churn atípico: 4 controles BT + rmmod com devices vivos).

## Perguntas de pesquisa (responder com fonte/medição, sem opinião prévia)

- **P1 — Mapa de versões**: para cada candidata (5.72 noble, 5.79, 5.82, 5.85,
  5.86+/git HEAD, e o pacote da próxima Ubuntu), quais bugs de heap/input/HIDP
  conhecidos existem/foram corrigidos (changelog + issues upstream + LP)?
  Alguma corrige a assinatura `unaligned fastbin` no caminho input/reconexão?
- **P2 — O que cada versão quebra no NOSSO stack**: matriz das dependências do
  hefesto por versão — input via uhid (BLUEZ-UHID-01), JustWorksRepairing,
  agente NoInputNoOutput, broker/validador D1-D4, re-pair em massa. O 5.72
  resolve alguma coisa que o 5.85 não resolve (e vice-versa)?
- **P3 — Reprodução e captura**: dá para reproduzir o gatilho (2 devices HID em
  loop de reconexão) em bancada? Armar captura ANTES do próximo crash:
  systemd-coredump habilitado p/ o serviço, `MALLOC_CHECK_`/`MALLOC_PERTURB_`,
  build com ASan/valgrind em sessão de teste, `bluetoothd -d` com log rotativo.
- **P4 — Mitigações independentes de versão**: o que reduz o dano SEM trocar o
  BlueZ — backup/restauração automática de bonds (`/var/lib/bluetooth`),
  watchdog que detecta o estado "doente" pós-crash (recusa unknown device /
  SDP em loop) e reinicia o serviço limpo, rate-limit do loop de reconexão,
  regra operacional (nunca rmmod driver HID com devices BT vivos — já em
  memória). Quais valem virar entrega do hefesto independentemente da versão?
- **P5 — Upstream**: com dump capturado, o bug é reportável/bisectável?
  Existe patch proposto na lista do BlueZ para heap no plugin input?
- **P6 — Integração**: dado o vencedor de P1/P2, qual a melhor forma de
  integrar — pacote pinado (como hoje), patch próprio sobre o pacote da
  distro, ou stock + mitigações de P4? Critérios: reprodutibilidade via
  install.sh (regra do projeto: tudo replicável por script), reversibilidade
  (uninstall simétrico), e custo de manutenção a cada kernel/distro upgrade.

## Critérios de decisão (definidos ANTES dos resultados)

1. Zero perda de bond em crash OU crash inexistente no regime de uso real
   (4 controles, conexões/desconexões frequentes) — medido, não presumido.
2. Não regredir as curas que motivaram o 5.85 (P2).
3. Integração replicável e reversível via install/uninstall.
4. Empate técnico → menor divergência da distro vence.

## Artefatos / ponteiros

- Journal do crash de 21/07: `journalctl -u bluetooth --since "2026-07-21 22:10"`
  (assinatura completa e sequência de recusas pós-restart).
- Memórias do projeto: crash crônico (19/07, com o crash #6 anexado),
  estudo do backport 5.85 (19/07), checkpoint 21/07 22h40.
- Gatilho de referência p/ bancada: desligar 2 controles Nintendo BT ao mesmo
  tempo e deixar o serviço em loop de reconexão ~2 min.

---

## Resultados da pesquisa (22/07 madrugada — 4 agentes + medição local)

### Fato novo que muda o problema: bonds nascem TEMPORÁRIOS (medido)

`/var/lib/bluetooth/<adapter>/` está SEM NENHUM diretório de bond (`<MAC>/info`) —
só `cache/` (sendo escrito → não é permissão). O DualSense ficou "Paired: yes"
por horas e, ao desconectar, sumiu por completo da lista de devices. Mecanismo
(leitura do fonte, hipótese forte, sem issue upstream nomeada): `store_device_info()`
só grava se `!temporary`; `btd_device_set_temporary(FALSE)` só é chamado no método
D-Bus `Pair()` explícito ou em `device_profile_connected()` quando a conexão de
perfil completa SEM erro. Um re-pair entrante aceito por `JustWorksRepairing=always`
não passa por `Pair()`; se a resolução de serviços falhar/cair no meio (nosso caso:
pós-crash, SDP em loop), o device morre `temporary=true` e nada persiste.
`trust` NÃO promove temporary→permanente (não está entre os chamadores).
**Playbook novo de re-pareamento: sempre `bluetoothctl pair <MAC>` explícito** e
verificar `Bonded: yes` + `<MAC>/info` no disco (`busctl get-property org.bluez
/org/bluez/hci0/dev_XX org.bluez.Device1 Bonded` sem sudo).

Agravante corrigido em 22/07 00:11: `main.conf` tinha 3 seções `[General]`
duplicadas (appends repetidos do install) — consolidado; o install.sh precisa
escrever config idempotente (bloco `# BEGIN/END hefesto`).

### P1/P2 — mapa de versões (fontes verificadas no git oficial)

- 5.72→5.85: todos os fixes de uhid/input relevantes (5.77 `b94f1be6` #815,
  5.78 `ee39d01f`, 5.79 `9a6a84a8` #952 + `UserspaceHID=persist`, 5.82 `8f853903`
  fallback p/ hidp, 5.84 `4784f58f` destructors errados em profiles/input) já estão
  no 5.85. Nenhuma versão intermediária é "sweet spot" — 5.85 domina.
- **5.86 (2026-02-08)**: `17a227b7` "device: Limit the number of retries on auth
  failures" — retry-limit + backoff exponencial no loop de reconexão; é o retrato
  estrutural do nosso gatilho de crash (storm de reconexão de 2 controles).
  Candidata preliminar. Confiança MÉDIA: trata "auth failure", nosso loop era
  "Host is down" (caminho possivelmente distinto); ler o diff antes de assumir.
- 5.87 (2026-07-03): corrige bug do próprio retry-limit (`7ca74765`) MAS introduz
  use-after-free em `dev_disconnected` (fix `5bc6aa79` só em git HEAD, sem release).
  Evitar.
- Assinatura `malloc(): unaligned fastbin chunk detected 2` em bluetoothd: **inédita
  publicamente** (nenhum issue/LP/commit). Somos os descobridores → capturar
  coredump é pré-requisito para reportar upstream e para decidir com evidência.
- Correção de registro: LP #2137758 é SIGSEGV em `btd_service_connecting_complete`
  (Ubuntu Error Tracker, 5.84-1, Confirmed/sem fix), NÃO "HIDP heap corruption".

### P3/P5 — reprodução e captura

- Gatilho de bancada: 2 controles Nintendo BT desligados simultaneamente → loop
  ~2 min. Reproduzível em tese; só armar DEPOIS da captura estar pronta.
- Captura: `core_pattern` do Pop!_OS é o apport (`enabled=1`), que ignora pacote
  fora da distro (por isso zero dumps). Toggle temporário p/ systemd-coredump via
  sysctl.d (config GLOBAL do kernel — ligar só em janela de diagnóstico) +
  `MALLOC_CHECK_=3`/`MALLOC_PERTURB_` como Environment escopado no drop-in do unit
  (~30% overhead de malloc — aceitável em bluetoothd por janela curta) +
  `bluetoothd -d` opcional. Com dump em mãos, o bug vira reportável/bisectável (P5).

### P4 — mitigações independentes de versão (desenho em camadas)

- **Camada 1 (ganho puro, entrar já)**: install.sh idempotente p/ main.conf.
- **Camada 2 (resiliência)**: (a) `Restart=on-failure` JÁ vem ativo no nosso pacote
  5.85 (medido via `systemctl cat`) — o "doente pós-crash" não é falta de
  supervisão, é o daemon renascido sem os bonds; (b) drop-in `WatchdogSec=30`
  cobre hang-sem-crash (padrão issue #784); (c) snapshot periódico dos `info`
  (`ExecStopPost` + timer; modo 600, tratar LinkKey como credencial) com
  **restauração MANUAL** via doctor/GUI (restauração automática pode restaurar
  chave que o controle já rotacionou → loop de auth-failure = o próprio gatilho do
  crash); (d) watchdog por assinatura de journal ("unknown device"/"error updating
  services" em loop → restart rate-limitado 1/10min) p/ o caso "vivo mas doente" —
  atenção: essas strings também ocorrem em daemon são (issue #1570), usar contagem
  em janela, não ocorrência única.
- **Camada 3 (forense, opt-in)**: `scripts/bt-crash-capture.sh --on|--off`
  (core_pattern + MALLOC_CHECK_ + -d). Nunca default.

### P6 — integração

Pacote pinado (como hoje) segue sendo o formato: reprodutível via install.sh,
reversível via uninstall (--keep-bluez já existe). Se a decisão for 5.86: mesmo
processo de backport do 5.85 (rebuild p/ noble com pin), mantendo Camadas 1-2
independentes da versão. Empate técnico → menor divergência da distro vence
(critério pré-definido).

### Artefatos propostos (nomes concretos)

- `assets/systemd/bluetooth.service.d/10-hefesto-resilience.conf` (WatchdogSec=30)
- `scripts/bt-bonds-snapshot.sh` + `hefesto-bt-bonds-snapshot.{service,timer}`
- `scripts/bt-bonds-restore.sh` (manual, gated pelo doctor)
- `scripts/bt-health-watchdog.sh` + `hefesto-bt-health-watchdog.{service,timer}`
- `scripts/bt-crash-capture.sh` (opt-in)
- install.sh: escrita idempotente de `/etc/bluetooth/main.conf` (bloco marcado)
- doctor.sh: check "cache cheio + zero bonds em disco" e "Paired sem Bonded"

### Critérios de decisão (relidos contra os resultados)

1. Zero perda de bond em crash → coberto pelas Camadas 1-2 (snapshot+restore
   manual) INDEPENDENTE de versão; persistência correta exige também o playbook
   `Pair()` explícito (e possivelmente fix de produto: o daemon/GUI disparar
   `Pair()` quando detectar device conectado-mas-temporary).
2. Não regredir curas do 5.85 → 5.86 as contém todas (P1).
3. Replicável/reversível → mantido pelo formato pacote-pinado + drop-ins.
4. Menor divergência → stock 5.72 está descartado pelos fatos (5 crashes/5 dias +
   família uhid sem curas); entre 5.85 (atual) e 5.86, a divergência é igual —
   decide o ganho do retry-limit vs. o custo de mais um backport.

---

## ENTREGA (22/07 madrugada) — decisão dela: "sobe 5.86 e implementa tudo, via install sem flag"

### O que está NO AR (verificado ao vivo)

- **BlueZ 5.86** rodando (`bluetoothd --version` = 5.86), backport próprio
  `5.86-0ubuntu0.1~hefesto24.04.1` (upstream 5.86 sobre o packaging do
  resolute), .debs + SHA256SUMS em `~/.cache/hefesto-dualsense4unix/
  bluez-backport/` (os de 5.85 preservados como rollback rápido;
  `VERSOES-ANTERIORES.txt` do noble intacto p/ o uninstall).
- Drop-in `10-hefesto-resilience.conf` CARREGADO (`systemctl status` lista;
  `WatchdogUSec=30s` + `Restart=on-failure` confirmados via `systemctl show`).
- Timers `hefesto-bt-bonds-snapshot` (15min) e `hefesto-bt-health-watchdog`
  (2min) ativos; o invariante "nunca fotografa vazio" DISPAROU ao vivo no
  ExecStopPost do primeiro restart (journal: "snapshot recusado de propósito").
- `main.conf` com bloco único gerenciado (install idempotente reescreve;
  `fast-connectable` visível nos settings do hci0).
- Passo novo `3e-bis` no install.sh (antes do 3f de propósito: o postinst do
  backport reinicia o bluetoothd e o drop-in precisa existir para armar nesse
  restart — funcionou exatamente assim na instalação real).
- Gate: 4478 testes verdes (suíte completa + 13 novos de contrato em
  tests/unit/test_bt_resilience_assets.py; 1 teste legado atualizado para o
  bloco unificado).

### Receita do build 5.86 (para o próximo bump)

Nenhum empacotamento 5.86 existia (Debian sid e Ubuntu devel = 5.85-4):
tarball upstream (kernel.org) + `debian/` do resolute 5.85-4ubuntu0.1
(archive.ubuntu.com/pool — o Launchpad estava lento demais). Três pedras no
caminho, todas de packaging:
1. `0013-transport-Fix-set-volume...patch` REMOVIDO da series — o 5.86
   refatorou a API de volume (`media_transport_get_device_volume` não existe
   mais) → undefined reference no link. O 0012 segue válido.
2. `usr/share/man/man1/btmgmt.1` removido de `debian/bluez.manpages` — o 5.86
   não gera mais essa man page (a cópia debian/manpages/btmgmt.1 continua).
3. 6 man pages NOVAS do 5.86 adicionadas ao manifest (bluetoothctl-telephony.1
   + org.bluez.{Call,Telephony,Thermometer,ThermometerManager,
   ThermometerWatcher}.5) — sem isso o dh_missing aborta.
Fonte da árvore de build: `~/.cache/hefesto-dualsense4unix/bluez-src-586/`.

###  Achado novo: bluetoothctl 5.86 MUDO no modo one-shot (COMPAT BLUEZ-586-CTL-01)

`bluetoothctl list` (e qualquer one-shot) imprime NADA com rc=0 — com ou sem
TTY, com ou sem `--timeout`. O modo interativo funciona e o daemon está são
no D-Bus (`busctl tree org.bluez` ok). Regressão do CLIENTE 5.86. Cura
aplicada: função-sombra `bluetoothctl()` no doctor.sh (cobre os ~25 usos num
ponto só) e no bt_health_watchdog.sh, rodando via modo interativo + limpeza
de ANSI/prompt + âncora no eco do comando; `pair`/`trust` usam `_btctl_lento`
(segura o `quit` — pair é assíncrono, quit imediato cancelaria). Pendência
upstream: reportável com reprodução trivial.

### Notas de operação medidas na instalação real

- Pós-upgrade o hci0 demorou a aparecer no D-Bus e o `btmgmt info` também era
  mudo — diagnóstico ficou claro só com `busctl tree org.bluez` (adapter
  registrado, Powered=true) + `hciconfig -a` (UP RUNNING): o rádio e o daemon
  estavam sãos; o "vazio" era o cliente mudo (item acima). A mensagem
  "Failed to set default system config for hci0" no start do 5.86 é
  observável mas NÃO impede o registro do adaptador — acompanhar.
- Os restarts seguidos do bluetooth.service esgotaram o StartLimitBurst do
  hefesto-bt-agent (Requires=bluetooth.service) → `reset-failed` + start
  resolveu; o doctor pegou (WARN) e confirmou a volta.
- rfkill soft-block reapareceu uma vez ao religar o serviço fora do install
  (padrão já conhecido da memória: BT Powered:no = rfkill).

### Validação que falta (gate humano)

1. Re-parear os 3+1 controles com **Pair() explícito** (one-shot mudo ⇒ usar
   `bluetoothctl` interativo: `scan on` → botão de pareamento → `pair <MAC>`
   → `trust <MAC>`) e conferir `Bonded: yes` + `<MAC>/info` no disco — este é
   o teste do achado dos bonds temporários; o watchdog promove sozinho quem
   ficar temporário (1x/boot por device).
2. Regime real de uso (4 controles, liga/desliga frequente) sem crash — o
   critério nº 1 da sprint só fecha com dias de uso; se crashar, ligar
   `bt_crash_capture.sh --on` na hora (agora existe caminho para capturar).
3. A/B de EMI (receita do estudo kernel/rádio) se a intermitência BT voltar
   mesmo com WiFi preso em 5GHz.

### Adendo 22/07 tarde — validação parcial ao vivo (reboot 13:54)

-  **Pair() explícito PERSISTIU**: bonds do DualSense roxo (13:55) e do Pro
  Controller (13:58) nasceram com `<MAC>/info` em disco. Snapshot das 14:09:50
  fotografou os 2 (camada 2 provada de ponta a ponta, dedup no-op às 14:39).
-  **Bond do Pro EVAPOROU de novo** entre 14:09 e 14:24 (janela em que ele
  saiu do BT para o cabo): o device sumiu do BlueZ e o diretório do disco foi
  removido. Hipóteses: (a) o Pair() entrante não limpou `temporary` de fato e
  o disconnect removeu device+storage; (b) remoção manual via COSMIC. O
  snapshot 20260722-140950 guarda a cópia — `bt_bonds_restore.sh` recupera se
  o Pro voltar ao BT. VIGIAR no próximo ciclo BT do Pro (é o teste decisivo).
-  **Vigia 2b nova no `bt_health_watchdog.sh`** (gap medido ao vivo): o roxo
  ficou `Bonded=true` + `Trusted=false` — pair explícito NÃO seta trust, e sem
  trust a reconexão ENTRANTE é recusada. O watchdog agora aplica
  `Trusted=true` via busctl (idempotente) em device conectado sem trust;
  aplicado no roxo na hora.
-  **Rádio do Pro em BT segue com perda sustentada** (4-10 IMU reports/s
  dropados, 13:57-13:59, mesmo com patch 0002 ativo e LEDs ok) — o 8BitDo BT
  estabilizou com os patches (relato da mantenedora); o Pro real fica no CABO
  (doutrina) até um diagnóstico fino de rádio (btmon em janela, opcional).
