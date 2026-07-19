# Sprint FUTURO (materializada 2026-07-18, NÃO executar nesta onda)

> Registro das curas de raiz que ficam para a próxima onda, com o racional já pesquisado
> (estudo 2026-07-18) para não repetir investigação.

## FUT-01 — Broker root: esconder o hidraw do físico SEM env (cura de raiz do P2)

Problema: daemon, Steam e jogo rodam com o MESMO UID → DAC não separa; EVIOCGRAB cobre só
evdev; o canal hidraw do físico fica aberto a qualquer processo da usuária. Sem wrapper, o
jogo sempre poderá ver o físico (o "duplicado > zero controles" de hoje).
Desenho proposto:
- Serviço systemd SYSTEM (root, hardened: ProtectSystem=strict, DeviceAllow mínimo) com socket
  de comando validado: `hide <hidrawN>` / `restore <hidrawN>`, aceitando SOMENTE nós cujo
  device pai é DualSense físico 054c:0ce6 (validação via sysfs, nunca caminho arbitrário).
- Ação: `setfacl -b` + `chmod 0600 root:root` no nó (o daemon mantém o fd já aberto; re-open
  passa a ser negado a todos, inclusive Steam/jogo). `restore` devolve MODE/ACL via
  `udevadm trigger` no device (regra re-aplica o estado canônico).
- Daemon chama `hide` ao adotar o físico COM vpad ativo; `restore` no teardown/Modo Nativo.
- Riscos mapeados: Modo Nativo precisa do hidraw exposto (gate por modo); hotplug re-cria o nó
  com ACL (daemon re-esconde no connect); NUNCA esconder sem vpad vivo (fail-safe "duplicado >
  zero controles" continua sendo a regra).

## FUT-02 — IMU/touchpad reais no vpad (DEDUP-02, gate gyro/touch)

O vpad expõe nós de Motion/Touchpad sem dados (uhid_gamepad.py:690). Streaming real:
replicar frames de IMU/touch do físico para o input report 0x31/0x01 do vpad (offsets do
descriptor Edge; o hid_playstation do lado do vpad já cria os devices). Destrava gyro aiming
e o gate humano DEDUP-02. Custo: parsing contínuo do report de input do físico (hoje o evdev
reader lê eventos, não o report cru completo) — avaliar mover a leitura de input para hidraw
puro com repasse integral (arquitetura "espelho de report", elimina 2 camadas de tradução).

## FUT-03 — RDR2 nativo+BT (2ª causa, BT-07)

Candidatos ordenados no sprint BT (2026-07-16-sprint-bluetooth-vpad-mudo.md:402+): PSSupport
temporário; dedup interno do SDL (vpad-evdev × físico-HIDAPI mesmo uniq); CRC fails do rádio
(clone DS4 05C4 stormando o adaptador). Matriz de teste com journal — gate humano.

## FUT-04 — Higiene

- Remover venv/ legado da raiz (só .venv é usado).
- Registrar/usar markers requires_gtk/requires_display do ci.yml ou removê-los.
- Limpar as 45 violações antigas de acentuação (ou assumir a dívida no doc).
- CI: incluir tests/core no job lint-test (hoje só tests/unit — furo sysfs-LED).
