# Estudo 2026-07-18 — Broker root `hide-hidraw` (FUT-01 / PLAT-02): SPEC pronta para implementar

> Missão BROKER da onda futura. Projeto A FUNDO do serviço system root que esconde o hidraw do
> DualSense **físico** do processo do jogo SEM depender de env de Proton — cura de raiz do "P2
> duplicado", funciona com QUALQUER loader (SDL, winebus-hidraw, libScePad, HIDAPI).
> Coleta 100% read-only na máquina de referência (MeowSystem, kernel 7.0.11-76070011-generic,
> sessão real de 2026-07-18 noite: DualSense branco USB = hidraw3, roxo BT = hidraw7, vpads P1/P2
> = hidraw6/hidraw8, Pro/8BitDo USB = hidraw2/hidraw13). Toda afirmação de sysfs abaixo tem
> evidência local anexada. Nada foi aplicado; nenhum arquivo de código foi tocado.

Unit canônica (nome já fixado em PLAT-02): **`hefesto-hidraw-broker.service`** (+ `.socket`).

---

## TL;DR — o desenho em 8 linhas

1. **Serviço system root hardened** ativado por socket (`hefesto-hidraw-broker.socket`, `Accept=no`).
2. Socket unix em `/run/hefesto-hidraw-broker/broker.sock`; **SO_PEERCRED** exige uid da sessão.
3. Protocolo **JSON-por-linha** (mesma casa do IPC do daemon): `hide` / `restore` / `restore_all` / `status` / `ping`.
4. Validação por **HID_ID do uevent do pai HID imediato** (transport-independent: cobre USB E BT),
   não por passeio até `idVendor` (que no BT acha o adaptador, não o controle — provado abaixo).
5. **Hide** = `setfacl -b` + `chmod 0600 root:root` no nó; o fd já aberto do daemon **sobrevive**
   (permissão é checada só no `open(2)`). **Restore** = re-`setfacl` explícito + `chmod 0660` (uid
   vem do SO_PEERCRED / gravado no hide) — mais robusto que `udevadm trigger` para o fail-safe.
6. **Fail-safe por construção**: a conexão de controle do daemon É a lease. Daemon morre → kernel
   fecha o fd → o broker vê EOF → **restaura tudo que aquele cliente escondeu**. "Duplicado > zero".
7. **Hooks no daemon**: hide ao **grabar** o físico com vpad vivo (`_set_controller_grab(…, True)`);
   restore ao **soltar** o grab (`…, False`); re-hide a cada tick de hotplug (`connect()`); gate por Modo Nativo.
8. **Install SEM FLAGS**: unit+socket+RuntimeDirectory; auth sem polkit (SO_PEERCRED); uid da sessão
   gravado no install (SUDO_UID). Uninstall simétrico + `restore_all` no stop.

---

## §0 — Por que na raiz (recap curto, não repetir pesquisa)

Daemon, Steam e jogo rodam com o **mesmo uid** (1000) → o DAC não separa. A regra udev 70
(`assets/70-ps5-controller.rules`) dá ao físico `MODE 0660 + TAG uaccess`, e o logind transforma
`uaccess` em ACL `user:vitoriamaria:rw` — provado ao vivo:

```
# getfacl -p /dev/hidraw3   (DualSense branco USB, físico do vpad P1)
# owner: root
# group: root
user::rw-
user:vitoriamaria:rw-      <-- a ACL do uaccess: é isto que o jogo usa para abrir o físico
group::rw-
mask::rw-
other::---
# ls -l /dev/hidraw3  -> crw-rw----+ 1 root root 237, 3   (o '+' = ACL presente)
```

`EVIOCGRAB` cobre só o **evdev**; o canal **hidraw** do físico segue aberto a qualquer processo do
uid (o "duplicado" — estudo 2026-07-18 guerra-de-escritores, FATO 1: o winebus dos Protons 10/11 dá
hidraw à família Sony por default, ignorando o IGNORE do SDL). `PROTON_DISABLE_HIDRAW`/IGNORE só
funcionam SE o jogo foi lançado pelo wrapper `hefesto-launch` — e a sessão real de 18/07 rodou SEM
o wrapper (FATO 0). O broker corta na raiz: **se o processo do jogo não consegue `open()` o hidraw
do físico, não há vazamento em backend nenhum**. Com o broker, `PROTON_DISABLE_HIDRAW`/IGNORE viram
defesa em profundidade, não a cura.

---

## §1 — Modelo de processo: unit system root hardened + socket

Dois assets novos. **Ativação por socket** (`Accept=no`): o systemd cria o socket de escuta como
root ANTES do serviço (elimina a corrida "daemon conecta antes do broker subir") e sobe o serviço na
primeira conexão. O serviço é **uma instância longa** que aceita as conexões ela mesma (necessário
para o fail-safe por EOF, §7).

### 1.1 `assets/systemd/hefesto-hidraw-broker.socket`

```ini
[Unit]
Description=Hefesto — socket de comando do broker root hide-hidraw
Documentation=file:docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md

[Socket]
# Socket em /run (system, root) — NÃO em /run/user (ProtectHome do serviço esconderia,
# e o dono seria o usuário, não root). RuntimeDirectory no serviço cria o diretório.
ListenStream=/run/hefesto-hidraw-broker/broker.sock
# Accept=no: passa o socket de ESCUTA (fd 3) a UMA instância; o broker faz accept()
# e mantém a conexão viva como lease de crash-restore.
Accept=no
# DAC de primeira barreira: só o grupo da sessão alcança o socket. O SO_PEERCRED
# (in-band, §3.3) é a barreira AUTORITATIVA — a DAC é conveniência/anti-DoS.
SocketMode=0660
SocketUser=root
SocketGroup=__SESSION_GROUP__   # gravado pelo install = `id -gn $SUDO_UID` (ex.: vitoriamaria)
# O diretório /run/hefesto-hidraw-broker precisa ser atravessável pelo usuário.
DirectoryMode=0755

[Install]
WantedBy=sockets.target
```

### 1.2 `assets/systemd/hefesto-hidraw-broker.service`

```ini
[Unit]
Description=Hefesto — broker root que esconde o hidraw do DualSense físico do jogo (FUT-01/PLAT-02)
Documentation=file:docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md
# O serviço só faz sentido com o socket; se o socket cair, o serviço para junto.
Requires=hefesto-hidraw-broker.socket
After=hefesto-hidraw-broker.socket
# Baseline limpo: se o broker morreu sujo numa sessão anterior e o systemd o reinicia,
# começa restaurando tudo (o ExecStartPre abaixo) — nunca herda um físico escondido órfão.

[Service]
Type=notify                       # sd_notify READY=1 após bind+scan inicial (systemd sabe quando está pronto)
NotifyAccess=main
ExecStart=/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker
# uid autorizado (a sessão dona); gravado pelo install a partir de SUDO_UID.
Environment=HEFESTO_BROKER_ALLOWED_UID=__SESSION_UID__
# Se o broker cai/é parado, RESTAURA todo físico que tenha ficado escondido (belt final).
ExecStopPost=/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker --restore-all-and-exit
Restart=on-failure
RestartSec=1

# --- HARDENING (cada diretiva justificada; ver §1.3 "o que NÃO pode entrar") ---
User=root                         # PRECISA de root: setfacl/chmod em nó root:root
NoNewPrivileges=yes
ProtectSystem=strict              # /usr /boot /etc read-only; /dev e /run seguem graváveis (chmod/setfacl OK)
ProtectHome=yes                   # /home, /root, /run/user inacessíveis — o broker nunca os toca
PrivateTmp=yes
PrivateNetwork=yes                # sem rede: AF_UNIX (socket de arquivo) funciona em netns privado
RestrictAddressFamilies=AF_UNIX   # o broker só fala unix socket
ProtectKernelTunables=yes         # /sys/proc read-only — leitura de uevent (validação) segue OK; ver §5.3
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
ProtectProc=invisible
ProcSubset=pid
RestrictNamespaces=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RemoveIPC=yes
UMask=0077
SystemCallArchitectures=native
SystemCallFilter=@system-service
SystemCallFilter=~@privileged @resources @mount @debug @cpu-emulation @obsolete @raw-io @reboot @swap @clock
# Capabilities: uid 0 mas bounding set mínimo. FOWNER = mexer no modo/ACL do nó;
# DAC_OVERRIDE/DAC_READ_SEARCH = atravessar diretórios e ler /sys mesmo com bits restritivos.
CapabilityBoundingSet=CAP_FOWNER CAP_DAC_OVERRIDE CAP_DAC_READ_SEARCH
AmbientCapabilities=
# Device cgroup: o broker NUNCA abre um nó de device (só muda metadata via path) → nega tudo.
DevicePolicy=closed
# (sem DeviceAllow: mínimo absoluto — ver §1.3)
# Diretório de runtime do socket, root-only por dentro, atravessável por fora.
RuntimeDirectory=hefesto-hidraw-broker
RuntimeDirectoryMode=0755
# Baseline limpo no start: restaura qualquer físico deixado escondido antes de aceitar comandos.
ExecStartPre=/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker --restore-all-and-exit

[Install]
WantedBy=multi-user.target
```

### 1.3 Diretivas de hardening — o que **NÃO** pode entrar (senão quebra setfacl/chmod)

Estas três são a diferença entre "hardened" e "não funciona". Documentar no cabeçalho da unit:

| Diretiva PROIBIDA | Por que quebraria |
|---|---|
| `PrivateDevices=yes` | Dá ao serviço um `/dev` **esfregado** só com null/zero/random/tty — **sem `/dev/hidraw*`**. `chmod /dev/hidraw3` viraria `ENOENT`. O broker PRECISA do `/dev` real (`PrivateDevices=no`, o default). |
| `ProtectSystem=full`/`strict` remontando `/dev` | Não faz isso: `strict` NÃO remonta `/dev` (devtmpfs) nem `/run` como read-only — por isso `chmod`/`setfacl` em `/dev/hidraw*` e o socket em `/run` funcionam. (Só `/usr /boot /efi /etc` ficam ro.) |
| `DeviceAllow=/dev/hidraw* rw` | **Desnecessário e contraproducente.** `DeviceAllow` governa o **device cgroup** = quem pode **abrir** o char device. O broker **não abre** o hidraw — só altera metadata do inode (`chmod`/`setxattr` via path). Então `DevicePolicy=closed` **sem** nenhum `DeviceAllow` é o mínimo correto: nega toda abertura de device e ainda assim `chmod`/`setfacl` passam (operam no inode, não no device). Este é o "DeviceAllow mínimo p/ /dev/hidraw*" pedido: o mínimo é **nenhum**. |
| `udevadm trigger` no restore + `ProtectKernelTunables=yes` | Incompatíveis: `trigger` **escreve** em `/sys/.../uevent`, e `ProtectKernelTunables=yes` deixa `/sys` **read-only**. Como o restore recomendado é `setfacl` explícito (§5.3, não toca `/sys`), mantemos `ProtectKernelTunables=yes`. Se um dia o restore via udev for desejado, a diretiva tem de cair (trade-off documentado). |

Notas de compatibilidade das que ENTRAM:
- `ProtectKernelTunables=yes` deixa `/sys` **legível** (só não gravável) → a validação por leitura de
  `/sys/class/hidraw/hidrawN/device/uevent` (§4) continua funcionando.
- `SystemCallFilter=@system-service` já inclui `@file-system` (contém `chmod`/`fchmodat`/**`setxattr`**
  — POSIX ACL é o xattr `system.posix_acl_access`) e `@io-event`/`@network-io` (socket AF_UNIX). O
  `~@privileged` nega `chown`/`setuid`/… — o broker **não faz chown** (dono já é root), então a
  negação é segura.
- `CapabilityBoundingSet` mantém `CAP_DAC_OVERRIDE`: para uid 0, sem essa cap o próprio root pode
  ser barrado por bits de modo ao atravessar/abrir caminhos — mantê-la evita surpresa.

---

## §2 — Binário do broker: forma e implementação

Um único executável Python autocontido, instalado em
`/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker` (não no `$PATH` do usuário — é infra
root). Roda o mesmo interpretador do projeto (shebang para o venv do sistema OU stdlib pura — **usa
só stdlib**: `socket`, `struct`, `os`, `json`, `selectors`, `pathlib`, `ctypes` p/ libacl OU
subprocess p/ `setfacl`). Recomendado **stdlib + `ctypes`→`libacl`** para não depender de import do
pacote nem de `execve` (mantém o `SystemCallFilter` apertado; ver §5.2).

Modos:
- default: `sd_listen_fds()` pega o fd 3 do socket, `ExecStartPre`/`--restore-all-and-exit` já rodou,
  faz `sd_notify(READY=1)`, entra no loop de accept.
- `--restore-all-and-exit`: varre `/sys/class/hidraw/*`, identifica os físicos 054c:0ce6 (§4) que
  estejam "escondidos" (dono root, sem ACL de usuário, modo 0600) e restaura cada um; sai. Usado no
  `ExecStartPre` (baseline) e `ExecStopPost` (belt final). Idempotente e best-effort.

---

## §3 — API do socket

### 3.1 Transporte e formato de mensagem

`SOCK_STREAM` AF_UNIX. **Mensagens JSON delimitadas por `\n`** (uma requisição por linha, uma
resposta por linha) — mesma convenção do IPC do daemon (`ipc_server.py` usa `readline()` +
resposta `+ b"\n"`), então a casa já conhece o padrão e o `socat`/manual debugging é trivial. Binário
foi descartado: o volume é baixíssimo (um punhado de comandos por sessão de jogo), a legibilidade
para doctor/logs vale mais que os bytes.

Requisição:
```json
{"cmd": "hide",    "node": "/dev/hidraw3"}
{"cmd": "restore", "node": "/dev/hidraw3"}
{"cmd": "restore_all"}
{"cmd": "status"}
{"cmd": "ping"}
```
Resposta (sempre com `ok` boolean + eco de contexto):
```json
{"ok": true,  "cmd": "hide",    "node": "/dev/hidraw3", "state": "hidden"}
{"ok": true,  "cmd": "restore", "node": "/dev/hidraw3", "state": "exposed"}
{"ok": false, "cmd": "hide",    "node": "/dev/hidraw6", "error": "reject_not_physical_dualsense"}
{"ok": false, "cmd": "hide",    "node": "/dev/hidrawX", "error": "reject_bad_path"}
{"ok": true,  "cmd": "status",  "hidden": ["/dev/hidraw3"]}
{"ok": true,  "cmd": "ping",    "peer_uid": 1000}
```
Regras: linha > 4 KiB → descarta+erro (`reject_oversize`); JSON inválido → `reject_malformed`;
`cmd` desconhecido → `reject_unknown_cmd`. Nunca levanta para o cliente; erro é sempre
`{"ok": false, "error": …}`.

### 3.2 Semântica de estado / lease por conexão

O broker mantém **`hidden_by_conn: dict[conn_fd, set[str]]`** — o conjunto de nós que CADA conexão
escondeu. `hide` adiciona; `restore` remove; **fechar a conexão restaura tudo o que ela escondeu**
(§7). Um `set` global `currently_hidden` deduplica (single-daemon: 1 escritor; mas o design
tolera 2 — refcount por nó). Isso torna o crash-restore automático e sem heartbeat.

### 3.3 SO_PEERCRED — como validar e como testar

No `accept()`, ANTES de ler qualquer comando:
```python
import socket, struct
creds = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
pid, uid, gid = struct.unpack("3i", creds)
if uid != ALLOWED_UID:            # ALLOWED_UID = int(os.environ["HEFESTO_BROKER_ALLOWED_UID"])
    log("peer_rejected", peer_uid=uid, peer_pid=pid); conn.close(); return
```
`SO_PEERCRED` devolve a credencial **do momento do `connect()`** (kernel-autoritativa, não
forjável pelo cliente). Um segundo uid autorizado (multi-sessão) seria um `set`; no desktop
single-user é um só. Combinado com a DAC do socket (`SocketGroup`), são duas barreiras.

**Como validar (doctor / teste de aceite):**
- `{"cmd":"ping"}` como a usuária → `{"ok":true,"peer_uid":1000}`.
- `sudo -u nobody socat - UNIX-CONNECT:/run/hefesto-hidraw-broker/broker.sock` → conexão **recusada**
  na DAC (grupo) OU aceita-e-fechada no SO_PEERCRED; em ambos, zero comando processado (checar log
  `peer_rejected`).
- `stat -c '%a %U %G' /run/hefesto-hidraw-broker/broker.sock` → `660 root <grupo-sessão>`.

---

## §4 — Validador: SÓ nós filhos do DualSense físico 054c:0ce6

Esta é a parte de segurança mais delicada: o broker **nunca** pode aceitar um caminho arbitrário
(`../`, symlink, `/dev/hidraw` do teclado, o **vpad 0df2**, etc.). Duas descobertas ao vivo governam
o desenho:

**Descoberta A — o passeio até `idVendor` MENTE no Bluetooth.** Andar da pasta do nó para cima
buscando `idVendor`/`idProduct` funciona no USB mas no BT encontra o **adaptador**, não o controle:

```
hidraw3 (branco USB)  parent chain -> .../usb3/3-4/3-4:1.3/0003:054C:0CE6.0004
                      subir até idVendor -> 054c / 0ce6    (nível usb_device 3-4)
hidraw7 (roxo BT)     parent chain -> .../3-1/.../bluetooth/hci0/hci0:1/0005:054C:0CE6.000A
                      subir até idVendor -> 2357 / 0604     (é o adaptador TP-Link!)
```

**Descoberta B — o pai HID imediato tem a identidade certa nos dois transportes.** O
`/sys/class/hidraw/hidrawN/device` aponta para o **nó HID** (`0003:054C:0CE6.xxxx` no USB,
`0005:054C:0CE6.xxxx` no BT), cujo `uevent` traz `HID_ID=<bus>:<vendor>:<product>` — provado:

```
hidraw3: HID_ID=0003:0000054C:00000CE6  HID_NAME=... DualSense ...  DRIVER=playstation   -> ACEITA
hidraw7: HID_ID=0005:0000054C:00000CE6  HID_NAME=DualSense ...       DRIVER=playstation   -> ACEITA (bus BT)
hidraw6: HID_ID=0003:0000054C:00000DF2  HID_NAME=Hefesto Virtual...   (vpad P1)            -> REJEITA (0df2)
hidraw8: HID_ID=0003:0000054C:00000DF2  (vpad P2)                                          -> REJEITA (0df2)
hidraw13:HID_ID=0003:0000057E:00002009  Nintendo Pro/8BitDo                                -> REJEITA
```

O `HID_ID` (e o `modalias` `hid:b….v0000054Cp00000CE6`) é **transport-independent**: `<bus>` varia
(0003 USB / 0005 BT), `<vendor>=054C` e `<product>=0CE6` não. É a chave canônica.

### 4.1 Pseudo-código do validador (rejeita tudo que não for físico 054c:0ce6)

```python
import os, re
_HIDRAW_RE = re.compile(r"^hidraw([0-9]+)$")
_HID_ID_RE = re.compile(r"^HID_ID=[0-9A-Fa-f]{4}:0*([0-9A-Fa-f]+):0*([0-9A-Fa-f]+)\s*$")
PHYS_VENDOR, PHYS_PRODUCT = 0x054C, 0x0CE6      # DualSense/DualSense standard físico
VPAD_PRODUCT = 0x0DF2                            # DualSense Edge (nosso vpad) — SEMPRE rejeitar

def validate_physical_node(node: str) -> str | None:
    """Devolve o basename canônico 'hidrawN' se `node` é um DualSense FÍSICO 054c:0ce6;
    None (rejeita) em qualquer outro caso. NUNCA abre o device; nunca segue caminho do cliente."""
    # 1) Caminho canônico e literal: exatamente /dev/hidrawN, sem '..', sem symlink.
    if not isinstance(node, str) or not node.startswith("/dev/"):
        return None
    base = os.path.basename(node)
    m = _HIDRAW_RE.match(base)
    if m is None:                       # rejeita /dev/hidraw (sem N), /dev/../, /dev/tty, etc.
        return None
    if node != "/dev/" + base:          # rejeita '/dev/foo/../hidraw3', barras extras
        return None
    # 2) O nó real precisa SER o char device de classe hidraw (não um symlink plantado).
    #    os.path.realpath resolve; exigimos que /sys/class/hidraw/<base> exista e que
    #    /dev/<base> seja um char device cujo (major,minor) casa o do sysfs.
    sys_dir = f"/sys/class/hidraw/{base}"
    if os.path.realpath(node) != node:  # /dev/hidraw3 não pode ser symlink
        return None
    try:
        st = os.stat(node)              # segue para o char device real
        if not os.path.stat.S_ISCHR(st.st_mode):
            return None
        dev_sysfs = open(f"{sys_dir}/dev").read().strip()   # "237:3"
        if dev_sysfs != f"{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}":
            return None
    except OSError:
        return None
    # 3) Nunca um device VIRTUAL (defende contra um uhid forjado que se anuncie 0ce6).
    hid_parent = os.path.realpath(f"{sys_dir}/device")
    if "/devices/virtual/" in hid_parent:
        return None
    # 4) Identidade pelo HID_ID do pai HID imediato (USB e BT). NÃO subir até idVendor.
    try:
        uevent = open(f"{sys_dir}/device/uevent").read()
    except OSError:
        return None
    vendor = product = None
    for line in uevent.splitlines():
        mm = _HID_ID_RE.match(line)
        if mm:
            vendor, product = int(mm.group(1), 16), int(mm.group(2), 16)
            break
    if vendor != PHYS_VENDOR or product == VPAD_PRODUCT or product != PHYS_PRODUCT:
        return None
    return base                          # aceito: é DualSense físico 054c:0ce6
```

Pontos-chave da robustez:
- **Só o basename `hidrawN`** é usado depois da validação; o caminho do cliente nunca é
  reconstruído por concatenação com input arbitrário. O broker opera em `/dev/<base>` e
  `/sys/class/hidraw/<base>/…` — ambos derivados do `N` numérico validado.
- Casamento `(major,minor)` sysfs×`st_rdev` fecha o ataque "symlink `/dev/hidraw3 -> /dev/sda`":
  o cliente não pode plantar symlink em `/dev` (é root-only), mas a checagem é barata e definitiva.
- `product == VPAD_PRODUCT` explicitamente rejeitado ANTES do `!=` — deixa claro no código que o
  **vpad 0df2 nunca é escondido** (ele PRECISA do hidraw: é por ele que rumble/triggers/lightbar do
  jogo chegam — invariante do estudo guerra-de-escritores decisão 1).

---

## §5 — Mecânica do hide / restore

### 5.1 Hide

Estado antes (canônico, rule 70): `0660 root:root` + ACL `user:<uid>:rw` + `mask::rw`.
Operação de esconder (nesta ordem):
```
setfacl -b /dev/hidraw3        # remove TODA ACL estendida (some o user:<uid>:rw e o mask)
chmod 0600 /dev/hidraw3        # tira group rw; sobra owner(root) rw; other ---
```
Resultado: `crw-------  root root` — **só root abre**. (Observação: `chmod 0600` sozinho já bastaria
para NEGAR o usuário, porque com ACL presente o `chmod` zera o *mask* e a entrada `user:<uid>:rw`
fica com efetivo `---`; fazemos os dois para não deixar entrada órfã e para o `ls`/`getfacl` lerem
limpo.)

### 5.2 Prova: revogar ACL/modo **NÃO** fecha o fd já aberto do daemon

Semântica POSIX/Linux: a checagem de permissão (DAC + POSIX ACL) acontece **no `open(2)`**; uma vez
existindo a *open file description*, `read(2)`/`write(2)` **não re-checam** permissão. `chmod`/
`setfacl`/`setxattr` alteram o **inode**, não a descrição aberta — o fd do `hidapi` do daemon (aberto
no `_open_one`/`connect()`) **segue válido**. Não há `revoke()` utilizável no Linux para fds
arbitrários, o que é justamente por que isto funciona sem derrubar o daemon (contraste com a tentativa
`chmod 000` refutada no sprint dedup, que derrubava o próprio daemon **porque ele reabria** pelo
mesmo uid — aqui o daemon NÃO reabre: mantém o fd).

**Corolário de timing (limitação a documentar):** o hide é **preventivo, não retroativo**. Se o jogo
já tinha `open()` no físico ANTES do hide, o fd dele também sobrevive. Por isso o daemon esconde o
**mais cedo possível** (no grab, que ocorre no start do vpad — bem antes de um launch) e **re-esconde
a cada hotplug** (o nó recriado nasce com a ACL do uaccess de novo). O caso "jogo já rodando quando o
físico é replugado" fica coberto pelo re-hide no `connect()`.

Implementação recomendada **sem `execve`** (mantém o `SystemCallFilter` apertado): `os.chmod()` +
POSIX ACL via `ctypes`→`libacl` (`acl_from_text`/`acl_set_file` no xattr `system.posix_acl_access`,
`acl_delete_def_file` não; para access-ACL usa `acl_set_file(path, ACL_TYPE_ACCESS, acl)`).
Alternativa aceitável (mais simples, custo: liberar `execve` no filtro + garantir `/usr/bin/setfacl`
do pacote `acl`): `subprocess.run(["setfacl","-b",node])` + `subprocess.run(["chmod","600",node])`.
A spec fixa a **semântica** (os comandos acima); a implementação escolhe libacl (default, hardening
máximo) ou setfacl (fallback).

### 5.3 Restore — `setfacl` explícito **vs** `udevadm trigger`: qual é mais robusto?

Duas rotas:

| Rota | Como | Robustez | Dependências |
|---|---|---|---|
| **A. re-setfacl explícito (RECOMENDADA)** | `chmod 0660 <node>` + `setfacl -m u:<uid>:rw <node>` (uid do SO_PEERCRED; no fail-safe, o uid **gravado no hide**) | **Determinística**: reverte exatamente o que o hide fez, sem depender de sessão ativa/logind/seat. Funciona mesmo se a sessão ficou inativa ou o nó não gera novo uevent. | nenhuma além de libacl/setfacl |
| B. `udevadm trigger --action=change /sys/class/hidraw/<base>` | re-roda as regras; a rule 70 re-aplica `MODE 0660 + uaccess`, o logind re-injeta a ACL | **Canônica** (reconcilia com a regra vigente), mas depende de: sessão do seat **ativa** no momento, `/sys` gravável (conflita com `ProtectKernelTunables=yes`, §1.3), e do timing do processamento udev. Assíncrona. | udev + logind + seat ativo |

**Veredito: A é a primária** — para o invariante sagrado "duplicado > zero controles", o restore
tem de ser **garantido e síncrono**, e no fail-safe (daemon morreu) não há SO_PEERCRED nem certeza
de seat ativo; o broker restaura pelo **uid que gravou no hide**. B fica como **belt opcional** só
quando `/sys` for gravável (i.e., se um dia se abrir mão de `ProtectKernelTunables=yes`) — a spec
default NÃO usa B, para manter o hardening. O restore do broker também **verifica** o resultado
(`getfacl`/`stat`) e loga `restore_verify_failed` se o nó não ficou acessível ao uid — sinal para o
doctor.

**Hotplug e restore:** um nó escondido que é fisicamente removido (unplug) simplesmente some; o
broker limpa a entrada de `currently_hidden` ao detectar `ENOENT` no restore (não é erro). O nó
recriado no replug **nasce exposto** (rule 70/uaccess) e o daemon o re-esconde no `connect()`.

---

## §6 — Integração com o daemon (hook points EXATOS, com arquivo:linha)

O hide/restore do hidraw é o **análogo exato do EVIOCGRAB do evdev**: as duas operações "tiram o
físico do jogo" e têm o MESMO ciclo de vida (vpad vivo). Por isso os hooks canônicos ficam colados no
grab. Um módulo cliente novo — **`src/hefesto_dualsense4unix/daemon/hidraw_broker_client.py`** —
abre UMA conexão longeva ao broker (lazy, na primeira necessidade) e a mantém (é a lease de §7);
expõe `hide(node)`, `restore(node)`, `restore_all()`, `is_available()`. Toda chamada é best-effort:
broker ausente/indisponível → log + segue (o comportamento degrada para o de hoje: duplicado, nunca
zero).

### 6.1 HIDE — "adotar físico COM vpad vivo"

1. **`src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:652`** — dentro de
   `start_gamepad_emulation`, logo após `_set_controller_grab(daemon, True)`. O grab confirma que o
   vpad do P1 está no ar e o físico foi tomado; aqui pede-se `hide` do hidraw do físico primário via
   `daemon.controller.hidraw_path()` (resolve `/dev/hidrawN` do primário — `backend_pydualsense.py:558`).
   *Melhor ainda:* embutir a chamada **dentro** de `_set_controller_grab` (gamepad.py:101), no ramo
   `grab=True`, para um único choke-point simétrico (ver §6.4). Gate: só backend pydualsense
   (`callable(getattr(controller,"hidraw_path",None))` — o mesmo gate de `controller_allows_uhid`,
   gamepad.py:393) e `not daemon.is_native_mode()`.
2. **`src/hefesto_dualsense4unix/daemon/connection.py:239`** — no `reconnect_loop`, imediatamente após
   `await daemon._run_blocking(daemon.controller.connect)`. `connect()` é o tick de hotplug
   (`backend_pydualsense.py:817`) e **recria o nó com a ACL do uaccess** quando o físico volta
   (replug/wake BT gera outro `hidrawN`). Aqui: se `daemon.config.gamepad_emulation_enabled and not
   daemon.is_native_mode()`, **re-hide** de todos os hidraw físicos atuais (idempotente — o broker
   no-op se já escondido). Este é o "daemon re-esconde no connect" do risco de hotplug.
3. **Co-op** — **`src/hefesto_dualsense4unix/daemon/subsystems/coop.py:457`** (`_promote_player`, onde
   o vpad secundário nasce via `make_virtual_pad`, coop.py:470) e o grab confirmado em
   `_spawn_player` (coop.py:344). Após promover, `hide` do hidraw daquele jogador:
   `daemon.controller.hidraw_path(uniq=<identity MAC>)` (o backend aceita `uniq`,
   `backend_pydualsense.py:558`). Só quando o jogador tem vpad vivo (nunca esconder sem vpad).

### 6.2 RESTORE — teardown / Modo Nativo / exit

O choke-point simétrico é o **release do grab**, que só ocorre quando o físico volta ao jogo:
1. **`src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:690`** — em `stop_gamepad_emulation`,
   dentro do `if release_grab:` logo após `_set_controller_grab(daemon, False)`. **restore** de todos
   os físicos escondidos. Crucialmente **gateado por `release_grab`**: na troca de flavor o
   `stop_gamepad_emulation(..., release_grab=False)` (chamado de gamepad.py:589) **não** solta o grab
   e **não** deve restaurar (o vpad é recriado na hora; restaurar+re-esconder exporia o físico numa
   janela). Colar o restore no `_set_controller_grab(…, False)` garante essa semântica de graça.
2. **Modo Nativo** — coberto pela cadeia existente: `_release_controller_to_game`
   (**`lifecycle.py:594`**) chama `set_gamepad_emulation(False, origin="profile")` (lifecycle.py:612)
   → `stop_gamepad_emulation(daemon)` (release_grab default True) → **restore** (via item 1). Modo
   Nativo **precisa** do hidraw exposto (o jogo é dono) — e é exatamente o que o restore entrega.
   Não há hook adicional a escrever aqui: o gate por modo cai fora naturalmente porque o nativo
   sempre passa por `stop_gamepad_emulation`.
3. **Exit/shutdown** — **`src/hefesto_dualsense4unix/daemon/connection.py:395`** — `shutdown()` já
   chama `stop_gamepad_emulation(daemon, persist=False)` (release_grab default True) → **restore**.
   Além disso, o fechamento do socket no shutdown dispara o fail-safe do broker (§7) como belt.
4. **Co-op teardown** — **`src/hefesto_dualsense4unix/daemon/subsystems/coop.py:534`**
   (`player.reader.set_grab(False)` no teardown do jogador) → **restore** daquele hidraw.

### 6.3 Gate por Modo Nativo (resumo)

- Entrar no nativo: `set_native_mode(True)` → `_release_controller_to_game` → `stop_gamepad_emulation`
  → **restore** (físico exposto para o jogo).
- Sair do nativo: `set_native_mode(False)` re-ativa emulação → `set_gamepad_emulation(True)` →
  `_set_controller_grab(True)` → **hide** de novo.
- Boot já em nativo (`lifecycle.py:317`, `load_native_mode()`): emulação não sobe → grab nunca liga →
  hide nunca é pedido → físico exposto.  (correto: nativo = jogo é dono.)

### 6.4 Forma recomendada (mínima e simétrica)

Embutir as duas chamadas dentro de `_set_controller_grab` (gamepad.py:101):
```python
# ... após o EVIOCGRAB observável existente ...
if callable(getattr(controller, "hidraw_path", None)) and not daemon.is_native_mode():
    client = _broker(daemon)                      # lazy singleton do hidraw_broker_client
    if grab:
        node = controller.hidraw_path()           # primário
        if node: client.hide(node)
    else:
        client.restore_all()                      # solta tudo que este daemon escondeu
```
Mais os hooks de **re-hide no hotplug** (connection.py:239) e **co-op** (coop.py:457/534) que o grab
único do primário não cobre. Assim o conjunto de pontos de escrita fica em 4 lugares, todos já
existentes e já responsáveis pela posse do físico.

---

## §7 — Fail-safe: o broker restaura tudo se o daemon sumir

**A conexão de controle É a lease.** O daemon abre UMA conexão longeva ao broker (no
`hidraw_broker_client`) e a mantém pela vida do processo. Se o daemon morre por QUALQUER via
(crash, SIGKILL, OOM, `run.sh --daemon --force` takeover), o kernel fecha os fds do processo →
o broker recebe **EOF/`recv()==0`** naquela conexão → **restaura todos os nós de
`hidden_by_conn[aquela_conn]`**. Sem heartbeat, sem polling: o EOF é imediato e garantido pelo
kernel. (Heartbeat opcional só como telemetria; não é necessário para correção.)

Camadas de defesa (todas convergem para "físico exposto = duplicado, nunca zero"):
1. **EOF da conexão** (principal): daemon some → restore imediato daquela lease.
2. **`ExecStartPre --restore-all-and-exit`**: se o BROKER reiniciar, começa restaurando qualquer
   físico deixado escondido (cobre "broker morreu enquanto escondia").
3. **`ExecStopPost --restore-all-and-exit`**: parar/desinstalar o broker restaura tudo.
4. **`restore_verify_failed`**: se um restore não deixou o nó acessível ao uid, loga para o doctor
   e tenta o belt B (udevadm) se disponível.

Reforço da regra de ouro no daemon: **nunca pedir `hide` sem vpad vivo confirmado** (o hide está
colado no grab `held`; sem grab não há hide). Se o broker estiver indisponível, o daemon **não
falha** — segue sem esconder (duplicado). O `hide` jamais é pré-condição para o jogo ter controle.

---

## §8 — Install SEM FLAGS, auth sem polkit, uninstall simétrico, coexistência

### 8.1 Install (entra por DEFAULT, sem flag — igual ao resto da onda PLATAFORMA)

Passo novo no `install.sh` (e no par `scripts/install-host-udev.sh`/`.deb`/flatpak host):
1. `install -Dm755 assets/broker/hefesto-hidraw-broker.py` →
   `/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker` (root:root).
2. Renderizar as units com os placeholders resolvidos:
   - `__SESSION_UID__` = `${SUDO_UID:-$(id -u)}`
   - `__SESSION_GROUP__` = `id -gn "${SUDO_UID:-$(id -u)}"`
   Instalar em `/etc/systemd/system/hefesto-hidraw-broker.{service,socket}` (as_root install -m644).
3. `as_root systemctl daemon-reload`; `as_root systemctl enable --now hefesto-hidraw-broker.socket`
   (socket-activated: o `.service` sobe sozinho na 1ª conexão do daemon). **Não** habilita o
   `.service` diretamente (o socket é o gatilho).
4. Registrar no estado de instalação (`~/.local/state/hefesto-dualsense4unix/` ou o registro do
   install) que o broker é **nosso** (uninstall remove só o nosso — mesma disciplina do cmdline
   PLAT-03).
5. Reusar o `acquire_sudo`/`as_root` já existentes (install_snd_quirk.sh:58, install_usb_quirk.sh:61)
   — o prime de sudo do install já cobre (a seção "udev/cura do storm/applet" já pede root).

Este é o **primeiro** serviço systemd de **sistema** do projeto (hoje todos são `--user`:
`hefesto-dualsense4unix.service`, `-storm-watch`, `-steam-input-guard`). O install passa a ter um bloco
"systemd system" além do "systemd --user". Documentar no cabeçalho do install.

### 8.2 Auth sem polkit

Não há D-Bus nem polkit: a autorização é **só** SO_PEERCRED (uid) + DAC do socket (grupo). Zero
diálogo, zero regra polkit, zero dependência de sessão gráfica. É o "polkit-free" pedido em PLAT-02.

### 8.3 Uninstall simétrico

`uninstall.sh`:
1. `systemctl disable --now hefesto-hidraw-broker.socket hefesto-hidraw-broker.service` (o
   `ExecStopPost --restore-all-and-exit` restaura qualquer nó escondido).
2. `rm -f /etc/systemd/system/hefesto-hidraw-broker.{service,socket}` +
   `/usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker`; `systemctl daemon-reload`.
3. `rmdir /run/hefesto-hidraw-broker` (best-effort; o RuntimeDirectory some sozinho no stop).
4. Remove só o que o registro marca como **nosso** (não toca units de terceiros).

### 8.4 "Broker root já existe no projeto?" — NÃO, e a interação com a onda PLATAFORMA

Busca no repo: **nenhum** serviço system root existe hoje (grep por `/etc/systemd/system`,
`systemctl --system`, `SO_PEERCRED`, `broker` em `src/`, `assets/`, `install.sh` → zero). O
"broker root promovido" da memória refere-se à **decisão** (PLAT-02 promoveu FUT-01 de "sprint
futura" para "executável"), não a código existente. O sprint dedup (2026-07-16) **refutou** um
esqueleto de broker por feature-creep (linha 123) e registrou a limitação (linhas 395-401): "consertar
isso exige broker root com fd-passing (SCM_RIGHTS) ou uid próprio". **Este desenho escolhe a rota
'esconder o nó' (ACL/chmod), não fd-passing** — mais simples, sem mudar como o daemon abre o hidraw,
e compatível com o "sudo-zero em runtime" (o daemon segue sem root; o root vive só no broker
isolado). Nenhuma outra parte do projeto compete pelo hidraw como root.

### 8.5 Coexistência com Modo Nativo (que PRECISA do hidraw exposto)

Gate por modo já resolvido em §6.3: o Modo Nativo sempre passa por `stop_gamepad_emulation` (restore)
ao entrar e o hide só religa ao sair (via re-grab). O broker em si é **agnóstico de modo** — ele só
executa hide/restore que o daemon pede; a política de "quando" mora no daemon, no ponto único de
posse do físico (o grab). Isso mantém a decisão de modo no daemon (onde o autoswitch/hotkey/perfil já
convergem) e o broker burro-e-seguro.

---

## §9 — Riscos mapeados e mitigação

| Risco | Mitigação |
|---|---|
| **Hotplug recria o nó com ACL** (replug/wake BT → novo `hidrawN` exposto) | Re-hide no `connect()` (connection.py:239), que roda a cada tick de hotplug do `reconnect_loop`. Idempotente. |
| **Jogo já tinha o físico aberto antes do hide** (fd sobrevive) | Hide é preventivo: colado no grab (start do vpad, antes de qualquer launch). Documentado como limitação; o re-hide no hotplug cobre replug com jogo vivo. |
| **Broker indisponível/crash deixa físico escondido** | 3 camadas: EOF da lease, `ExecStartPre` e `ExecStopPost` restore-all. "Duplicado > zero" preservado. |
| **Segurança do socket** (outro usuário local tenta comandar) | SO_PEERCRED (uid) autoritativo + DAC `0660 root:<grupo-sessão>`. Caminho validado (§4) impede escrever em nó alheio mesmo se a auth furasse. |
| **Caminho arbitrário / symlink / `..` / vpad 0df2** | Validador §4: basename `hidrawN` canônico, `(major,minor)` sysfs×rdev, rejeita `/devices/virtual/`, exige `HID_ID` = 054c:0ce6 e **rejeita 0df2 explicitamente**. |
| **BT: validar acha o adaptador** (Descoberta A) | Identidade pelo `HID_ID` do pai HID imediato, nunca subir até `idVendor`. Provado com hidraw7. |
| **Steam Input reabrindo o físico** | Steam roda com o mesmo uid; com o físico em `0600 root` ela também não abre — é o objetivo. O vpad 0df2 permanece exposto (uaccess), então a Steam mapeia o vpad. Se a Steam abriu o físico ANTES do hide, cai no caso "fd já aberto" (re-hide no hotplug + hide-cedo mitigam). |
| **`ProtectKernelTunables=yes` × restore por udev** | Restore primário é setfacl explícito (não toca /sys). udevadm só como belt opcional se a diretiva cair. |
| **Dois daemons (takeover)** | `hidden_by_conn` por conexão + refcount por nó: o daemon novo abre nova lease; o velho, ao morrer, restaura só a sua; o refcount evita expor um nó que o novo já re-escondeu. |
| **hide falhar** (setfacl/permissão) | Best-effort: log `hide_failed`, o daemon segue. Físico continua exposto = duplicado. **Nunca** o jogo fica sem controle por causa de um hide falho. |

---

## §10 — Plano de teste (gate de aceite)

**Unit/pytest (sem root, com sysfs/fs fake):**
- Validador: aceita fixtures de hidraw USB (HID_ID 0003:054C:0CE6) e BT (0005:054C:0CE6); rejeita
  vpad (0df2), Nintendo (057e), caminho `../`, symlink, basename não-`hidrawN`, `(major,minor)`
  divergente, `/devices/virtual/`.
- Protocolo: parse de JSON-linha, respostas `ok/erro`, oversize, malformed, unknown_cmd.
- Lease: fechar conexão restaura o set; refcount por nó com 2 conexões.
- `compose`/hook gating: mock do `hidraw_broker_client` no daemon — hide chamado em grab-on **só** com
  backend pydualsense e fora do nativo; restore em grab-off; **não** restaura em `release_grab=False`
  (troca de flavor); re-hide após `connect()` quando emulação ativa.
- SO_PEERCRED: teste com `socketpair` simulando uid autorizado/negado (injeção do leitor de cred).

**Ao vivo (máquina de referência, gate humano — o critério do sprint PLAT):**
- Com vpad P1 ativo e jogo lançado **SEM** wrapper: `lsof /dev/hidraw3` **não** mostra o processo do
  jogo (`winedevice`), enquanto `lsof /dev/hidraw6` (vpad) mostra. Prova cabal do PLAT-02.
- `getfacl /dev/hidraw3` durante o jogo: sem `user:1000` (escondido); ao sair do jogo/emulação: volta
  `user:1000:rw`.
- Kill -9 no daemon com físico escondido → em <1s `getfacl /dev/hidraw3` volta a ter `user:1000`
  (fail-safe por EOF).
- Modo Nativo ligado: `getfacl /dev/hidraw3` tem `user:1000` (exposto) — o jogo é dono.
- `sudo -u nobody socat - UNIX-CONNECT:/run/hefesto-hidraw-broker/broker.sock` → recusado.
- Doctor: nova subseção "Broker hide-hidraw" reporta socket presente/ativo, uid autorizado, e nós
  atualmente escondidos (`{"cmd":"status"}`).

---

## §11 — Pronto-para-implementar: manifesto de arquivos

**Novos:**
- `assets/broker/hefesto-hidraw-broker.py` — o binário (stdlib + ctypes/libacl; modos default e
  `--restore-all-and-exit`; validador §4; protocolo §3; lease/fail-safe §7).
- `assets/systemd/hefesto-hidraw-broker.socket` — §1.1.
- `assets/systemd/hefesto-hidraw-broker.service` — §1.2 (hardening §1).
- `src/hefesto_dualsense4unix/daemon/hidraw_broker_client.py` — cliente longevo (lazy singleton),
  `hide/restore/restore_all/is_available`, best-effort, guarda a conexão-lease.
- `tests/…` — validador, protocolo, lease, gating dos hooks (§10).

**Editados (hooks — 4 pontos, todos já donos do físico):**
- `daemon/subsystems/gamepad.py:101` (`_set_controller_grab`): hide em `grab=True`, restore_all em
  `grab=False`; gate `hidraw_path` + `not native`.
- `daemon/connection.py:239` (`reconnect_loop`, pós-`connect()`): re-hide no hotplug quando emulação
  ativa e não-nativo.
- `daemon/subsystems/coop.py:457` (`_promote_player`) e `:534` (teardown): hide/restore por jogador
  secundário (`hidraw_path(uniq=<mac>)`).
- `install.sh` + `uninstall.sh` + `scripts/install-host-udev.sh` + `docs`/doctor: §8.

**Constantes reusadas do código atual (não reinventar):**
- Resolver o hidraw do físico: `controller.hidraw_path(uniq=None|<mac>)`
  (`backend_pydualsense.py:558`).
- Gate "backend real (pydualsense)": `controller_allows_uhid`/`callable(hidraw_path)`
  (`gamepad.py:393`).
- MACs/uniq por jogador: `primary_uniq` / identity do co-op (`backend_pydualsense.py:585`,
  `coop.py:_primary_identity`).

---

## §12 — Evidências ao vivo coletadas (2026-07-18, read-only)

- `getfacl /dev/hidraw3` → `user:vitoriamaria:rw` (a ACL do uaccess da rule 70).
- `ls -l /dev/hidraw3 /dev/hidraw6 /dev/hidraw7` → `crw-rw----+ root root` (ACL presente nos três).
- Cadeia de pais + `HID_ID`/`modalias` de hidraw3 (USB físico), hidraw7 (BT físico), hidraw6/8 (vpad
  0df2), hidraw13 (Nintendo) — tabela §4. Prova de que `idVendor` mente no BT (acha 2357:0604) e o
  `HID_ID` do pai HID acerta nos dois transportes.
- `loginctl` → sessão 3, uid 1000 vitoriamaria, seat0, **active** (base do SO_PEERCRED e da DAC do
  socket).
- Repo: `grep -rn` por `/etc/systemd/system`, `SO_PEERCRED`, `broker` em `src/`/`assets/`/`install.sh`
  → nenhum serviço system root pré-existente (o broker é o primeiro).

— fim do estudo —
