# Desenho 2026-07-20 — Onda S: broker hide-hidraw reimplementado com FD-INJECTION

> DESENHO EXECUTÁVEL da reimplementação do broker root hide-hidraw (BROKER-01/FUT-01/PLAT-02),
> incorporando as 6 lições da auditoria que parkou a 1ª implementação (9 HIGH) e a ARMADILHA
> BLUEZ-UHID-01. Base: sprint `docs/process/sprints/2026-07-19-sprint-broker-hide-hidraw-onda-dedicada.md`,
> spec original `docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md` (a MECÂNICA
> ACL/chmod continua válida) e código parkado `docs/process/future-broker/` (read-only, referência).
> Evidência viva desta máquina (2026-07-20): DualSense BT reais em
> `/sys/devices/virtual/misc/uhid/0005:054C:0CE6.0006` e `.0007`, ambos com
> `HID_ID=0005:0000054C:00000CE6`, `HID_PHYS=d8:44:89:00:00:05` (MAC do adaptador) e
> `HID_UNIQ=<MAC do controle>` — físicos REAIS apesar de "virtual" no caminho.

Invariante sagrado em toda decisão abaixo: **"duplicado > zero controles"** — nenhuma falha do
broker pode deixar o jogo sem controle. Broker ausente/quebrado ⇒ comportamento de hoje.

---

## §0 — A mudança de espinha dorsal: por que fd-injection mata a classe broker×motion

A 1ª implementação escondia o nó (`setfacl -b` + `chmod 0600 root`) e o motion reader — que roda
como a usuária — precisava REABRIR o mesmo nó por caminho (silêncio de 1s, retarget de primário,
wake BT, corrida de nascimento). DAC não distingue daemon de jogo (mesmo uid) ⇒ EACCES em loop,
gyro morto no meio do jogo (achados #1/#6/#8/#12/#13).

**A cura por construção**: o broker é root — para ele o nó escondido continua abrível. O novo
cmd `open` faz o broker validar o nó, abri-lo com `O_RDWR|O_CLOEXEC` e devolver o **fd via
SCM_RIGHTS** na MESMA conexão AF_UNIX. O reader **NUNCA reabre por caminho**: pede fd ao broker;
o hide deixa de ter qualquer interação com o ciclo de vida do motion. Sem broker (ausente,
recusou, timeout) o opener cai em `os.open(path, O_RDONLY)` — exatamente o comportamento de
hoje. A classe inteira de bugs broker×motion desaparece porque a visibilidade do nó deixa de
ser pré-condição de reopen.

O que fica da spec de 18/07 (validado pela auditoria — REUSAR do parkado):
- validador por `HID_ID` zero-preenchido do pai HID imediato (nunca `idVendor` — no BT acha o
  adaptador);
- ACL via `os.setxattr`/`os.removexattr` em `system.posix_acl_access` (header v2 LE + entradas
  `<HHI`), byte-idêntica ao `setfacl` — zero `execve`, `SystemCallFilter` intacto;
- protocolo JSON-por-linha + SO_PEERCRED; lease = conexão (EOF restaura);
- hardening das units (com as mudanças do §5 — `open` muda o device cgroup).

O que muda: validador ganha a semântica BLUEZ-UHID-01 (§3), lease/restore ganham as lições 2-3
(§4), units perdem o `RuntimeDirectory` assassino de socket e ganham `DeviceAllow` (§5), o
daemon ganha o opener injetável no reader (§6), install/uninstall/doctor/packaging ganham o
passo system-root com registro de posse (§7).

---

## §1 — Protocolo: cmds herdados + NOVO cmd `open` com SCM_RIGHTS

### 1.1 Transporte e formato

`AF_UNIX SOCK_STREAM`, JSON-por-linha (uma requisição por linha, uma resposta por linha) — o
mesmo padrão do IPC do daemon e do broker parkado. Regras herdadas intactas: linha > 4096 B ⇒
`reject_oversize`; JSON inválido ⇒ `reject_malformed`; cmd desconhecido ⇒ `reject_unknown_cmd`;
o broker NUNCA levanta para o cliente. `SO_PEERCRED` no accept, ANTES de qualquer comando
(`peer_credentials()` do parkado, reusado literalmente).

Comandos:

```json
{"cmd": "ping"}
{"cmd": "status"}
{"cmd": "hide",       "node": "/dev/hidraw3"}
{"cmd": "restore",    "node": "/dev/hidraw3"}
{"cmd": "restore_all"}
{"cmd": "open",       "node": "/dev/hidraw3"}          <- NOVO
```

Respostas de `hide`/`restore`/`restore_all`/`status`/`ping`: idênticas ao parkado
(`BrokerState.handle_line`). Resposta de `open`:

```json
{"ok": true,  "cmd": "open", "node": "/dev/hidraw3", "state": "hidden"}   + 1 fd em ancillary
{"ok": false, "cmd": "open", "node": "/dev/hidraw6", "error": "reject_not_physical_dualsense"}
{"ok": false, "cmd": "open", "node": "/dev/hidraw3", "error": "open_failed", "errno": 19}
{"ok": false, "cmd": "open", "node": "/dev/hidraw3", "error": "reject_stale_node"}
```

`state` ecoa se o nó está `hidden`/`exposed` no momento (telemetria; o open funciona nos dois).
`open` NÃO altera lease/refcount — é ortogonal ao hide (o reader pode pedir fd antes, durante
ou depois do hide). Erro nunca carrega fd; resposta `ok:true` carrega EXATAMENTE 1 fd.

### 1.2 Lado broker (servidor) — validar, abrir, revalidar no fd, enviar

```python
def _cmd_open(self, conn_id: int, node: object) -> tuple[dict[str, object], int | None]:
    """Valida, abre O_RDWR|O_CLOEXEC|O_NOFOLLOW e devolve (resposta, fd|None).

    O fd devolvido é enviado pelo servidor via sendmsg(SCM_RIGHTS) JUNTO com a
    linha de resposta; a cópia local é fechada SEMPRE após o sendmsg (finally).
    """
    raw = node if isinstance(node, str) else None
    base = canonical_hidraw_base(raw, dev_root=self._dev_root)
    if base is None:
        return ({"ok": False, "cmd": "open", "node": raw, "error": "reject_bad_path"}, None)
    if self._validate(raw) is None:
        return ({"ok": False, "cmd": "open", "node": raw,
                 "error": "reject_not_physical_dualsense"}, None)
    canon = f"{self._dev_root}/{base}"
    try:
        fd = os.open(canon, os.O_RDWR | os.O_CLOEXEC | os.O_NOFOLLOW)
    except OSError as exc:
        return ({"ok": False, "cmd": "open", "node": canon,
                 "error": "open_failed", "errno": exc.errno}, None)
    # LIÇÃO 5 (minor-reuse): REVALIDAÇÃO pós-open NO PRÓPRIO FD — fstat(fd)
    # pina o inode; se o rdev não casa mais o sysfs, o nome foi reciclado
    # entre validar e abrir. Fecha e recusa (o cliente re-tenta com o nó novo).
    st = os.fstat(fd)
    if not stat.S_ISCHR(st.st_mode) or self._sysfs_rdev(base) != (
        os.major(st.st_rdev), os.minor(st.st_rdev)
    ):
        os.close(fd)
        return ({"ok": False, "cmd": "open", "node": canon, "error": "reject_stale_node"}, None)
    state = "hidden" if canon in self.hidden else "exposed"
    return ({"ok": True, "cmd": "open", "node": canon, "state": state}, fd)
```

Envio no servidor (o fd viaja NA MESMA mensagem da resposta — nunca em mensagem separada, para
o pareamento respostafd ser inambíguo):

```python
def _send_with_fd(self, sock: socket.socket, payload: dict[str, object], fd: int) -> bool:
    line = json.dumps(payload).encode("utf-8") + b"\n"
    try:
        sock.sendmsg([line], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack("i", fd))])
        return True
    except OSError:
        return False
    finally:
        os.close(fd)   # a duplicata do kernel já está em trânsito (ou perdida); a nossa fecha
```

Por que `open` funciona MESMO com o nó escondido: o hide é `0600 root:root` sem ACL — e o
broker É root com `CAP_DAC_OVERRIDE`. É exatamente esta assimetria que o design explora: o
único caminho de (re)abertura privilegiada passa pelo broker, que valida identidade antes.

### 1.3 Lado cliente Python — recvmsg/ancillary em detalhe

Novo método em `HidrawBrokerClient` (assinaturas exatas; o resto do cliente parkado é reusado):

```python
def open_fd(self, node: str) -> int | None:
    """Pede ao broker um fd O_RDWR do nó. None = indisponível/recusado (best-effort).

    O fd devolvido é do CHAMADOR (dono único; CLOEXEC garantido). Nunca levanta.
    """

_FD_INT_SIZE = struct.calcsize("i")           # 4
_ANCILLARY_SPACE = socket.CMSG_SPACE(2 * _FD_INT_SIZE)  # espaço p/ ATÉ 2 fds: detectar excesso

def _request_with_fds(self, payload: dict[str, Any]) -> tuple[dict[str, Any] | None, list[int]]:
    """Uma requisição → (resposta, fds recebidos). Chamado sob self._lock."""
    line = (json.dumps(payload) + "\n").encode("utf-8")
    sock = self._ensure_sock_locked()
    if sock is None:
        return None, []
    fds: list[int] = []
    buf = bytearray()
    try:
        sock.sendall(line)
        while b"\n" not in buf:
            if len(buf) > _MAX_RESPONSE_BYTES:
                raise OSError("resposta do broker sem fim de linha")
            # MSG_CMSG_CLOEXEC: o kernel instala O_CLOEXEC no fd JÁ NA RECEPÇÃO —
            # sem janela em que um fork/exec do daemon vazaria o hidraw.
            data, ancdata, flags, _addr = sock.recvmsg(
                4096, _ANCILLARY_SPACE, socket.MSG_CMSG_CLOEXEC
            )
            if flags & socket.MSG_CTRUNC:
                # Ancillary truncado = fds possivelmente vazados no kernel do
                # NOSSO lado. Aborta a conexão inteira (lease nova na próxima).
                raise OSError("ancillary truncado (MSG_CTRUNC)")
            for level, ctype, cdata in ancdata:
                if level == socket.SOL_SOCKET and ctype == socket.SCM_RIGHTS:
                    n = len(cdata) // _FD_INT_SIZE
                    fds.extend(struct.unpack(f"{n}i", cdata[: n * _FD_INT_SIZE]))
            if not data:
                raise OSError("broker fechou a conexão")
            buf.extend(data)
    except OSError:
        for fd in fds:
            with contextlib.suppress(OSError):
                os.close(fd)
        self._close_locked()
        return None, []
    raw = bytes(buf[: buf.find(b"\n")])
    try:
        response = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        response = None
    if not isinstance(response, dict):
        for fd in fds:
            with contextlib.suppress(OSError):
                os.close(fd)
        return None, []
    return response, fds

def open_fd(self, node: str) -> int | None:
    with self._lock:
        response, fds = self._request_with_fds({"cmd": "open", "node": node})
    ok = bool(response is not None and response.get("ok"))
    if ok and len(fds) == 1:
        logger.info("hidraw_broker_fd_recebido", node=node, state=response.get("state"))
        return fds[0]
    # Qualquer outra combinação é anomalia: fecha TUDO que veio (mais de um fd
    # = protocolo violado; fd com ok:false = broker bugado). Nunca vaza fd.
    for fd in fds:
        with contextlib.suppress(OSError):
            os.close(fd)
    if ok and len(fds) != 1:
        logger.warning("hidraw_broker_fd_count_invalido", node=node, count=len(fds))
    else:
        self._log_falha("open", node, response)
    return None
```

Decisões de robustez (todas obrigatórias na implementação):
- **CMSG_SPACE**: reservamos espaço para 2 fds de propósito — se o broker (ou um impostor no
  socket) mandar 2+, queremos RECEBÊ-los para poder FECHÁ-los; com espaço para só 1, o excesso
  seria descartado pelo kernel com `MSG_CTRUNC` (também tratado: conexão abortada).
- **Mais de um fd = erro**: contrato é exatamente 1 fd por `open` ok. `len(fds) != 1` fecha
  todos e devolve None.
- **`MSG_CTRUNC`** derruba a conexão (não dá para saber o que se perdeu).
- **EINTR**: PEP 475 — `recvmsg` re-tenta sozinho em EINTR quando não há timeout expirado; com
  `settimeout(2.0)` do cliente, estouro vira `socket.timeout` (subclasse de OSError) ⇒ fecha
  fds recebidos + fecha lease + None. O chamador (opener) cai no fallback `os.open`.
- **Fds parciais**: se a resposta chegou em pedaços e o erro veio no meio, TODO fd já
  acumulado é fechado no except. Nenhum caminho de código sai com fd órfão.
- **Retry**: `open_fd` NÃO re-tenta sozinho (diferente de `hide`/`restore`): quem re-tenta é o
  loop do reader (backoff próprio) — evita dupla-espera no caminho do gyro.

### 1.4 Compat: cliente novo × broker velho e vice-versa

Broker sem `open` responde `reject_unknown_cmd` ⇒ `open_fd` devolve None ⇒ fallback `os.open`.
Nunca há janela de versão que quebre o gyro. (Não existe broker velho instalado em produção —
o parkado nunca foi instalado — mas a regra custa zero.)

---

## §2 — Sequência canônica de posse do físico

### 2.1 Nascimento (boot / liga emulação)

```
nó visível (rule 70 + uaccess: 0660 root:root + ACL user:uid:rw)
  └─> backend pydualsense connect() ABRE o handle hidapi (por caminho, nó visível)
  └─> start_gamepad_emulation:
        make_virtual_pad (vpad uhid Edge no ar)
        start_motion_reader (reader nasce com opener broker-aware — §6.4;
                             o 1º open pode ser via broker OU os.open: nó visível, tanto faz)
        _set_controller_grab(daemon, True)      <- EVIOCGRAB
          └─> _broker_sync_grab(daemon, True)   <- HIDE (só aqui, com vpad vivo + grab held)
```

Ordem REAL do código atual preservada: `start_motion_reader` (gamepad.py:748) já roda ANTES de
`_set_controller_grab(True)` (gamepad.py:751) — o hide entra colado no grab, DEPOIS do reader
existir. O backend garante o fd dele por construção (o grab pressupõe controle adotado =
`connect()` já abriu o hidapi handle). O reader nem precisa da ordem: o opener dele fura o
hide via broker. **Regra de ouro mantida: nunca hide sem vpad vivo confirmado** (o hide mora
dentro do grab; sem grab não há hide).

### 2.2 Hotplug / retarget / wake BT (re-hide idempotente)

```
nó novo NASCE VISÍVEL (rule 70/uaccess re-aplicados pelo udev — sempre)
  └─> reconnect_loop tick: controller.connect() adota/reabre handle (nó visível)
  └─> rehide_physical_hidraw(daemon)           <- re-hide de TODOS os nós adotados (P1+co-op)
        broker re-APLICA o fs mesmo para nó já rastreado (lição 2: nó recriado
        com o mesmo hidrawN nasceu exposto; idempotência por-conexão que não
        toca o fs deixaria exposto com o broker jurando escondido)
  └─> motion reader: silêncio/ENODEV/request_reopen → _resolve_path() → opener
        └─> broker cmd open (funciona escondido OU visível) → fallback os.open
```

O `hidraw_path()` do backend re-resolve o nó ATUAL — o rename hidraw7→hidraw9 do wake BT
converge sozinho: o reader pede fd do nó novo; o broker esconde o nó novo no mesmo tick; o nó
velho escondido some (`ENOENT` no restore = `restore_node_gone`, não é erro).

### 2.3 Janela de exposição residual (documentada e aceita)

Entre "nó novo nasce visível" e "re-hide do próximo tick" existe uma janela (pior caso: o
fatiamento do `reconnect_loop` online, `RECONNECT_HOTPLUG_POLL_INTERVAL_SEC`; tipicamente
<2 s) em que um jogo já rodando pode `open()` o físico — e o fd dele sobrevive ao hide (a
permissão só é checada no `open(2)`, spec §5.2 de 18/07). Por que é aceitável:
1. O hide é **preventivo, não retroativo** — sempre foi a semântica (o caso principal, jogo
   lançado DEPOIS do grab, tem o nó escondido desde antes do launch).
2. A 2ª camada segue de pé: wrapper `hefesto-launch` + `PROTON_DISABLE_HIDRAW`/IGNORE cobrem o
   duplicado dos jogos lançados pelo hefesto.
3. A alternativa (segurar o connect até o broker confirmar) inverteria o invariante: falha do
   broker atrasaria/derrubaria a adoção do controle ⇒ risco de ZERO controles. Recusado.
4. Encolher a janela é otimização legítima (re-hide também no evento `CONTROLLER_CONNECTED`),
   não requisito de corretude.

### 2.4 Restore (teardown / Modo Nativo / shutdown / crash)

- `stop_gamepad_emulation(release_grab=True)` → `_set_controller_grab(False)` →
  `_broker_sync_grab(False)` → `restore_all` da lease.
- `release_grab=False` (troca de flavor / promoção uinput→uhid) **NÃO restaura**: o
  `_set_controller_grab(False)` nem é chamado nesse ramo — o físico fica escondido durante a
  recriação do vpad (restaurar+re-esconder abriria janela para SDL/winebus). De graça, pela
  colocação do hook (mesma malha do EVIOCGRAB).
- Modo Nativo: entrar passa por `stop_gamepad_emulation` (cadeia `_release_controller_to_game`,
  lifecycle) ⇒ restore; sair religa emulação ⇒ grab ⇒ hide. Boot já em nativo: grab nunca liga,
  hide nunca é pedido. Nenhum hook novo.
- Shutdown: `stop_gamepad_emulation` no `connection.shutdown()` restaura; depois o
  `daemon._hidraw_broker_client.close()` explícito fecha a lease (belt); o EOF cobre morte suja.
- Crash/SIGKILL/OOM/takeover: kernel fecha o socket ⇒ broker vê EOF ⇒ restaura tudo da lease.

---

## §3 — Validador: identidade BLUEZ-UHID-01, nunca topologia

### 3.1 A armadilha que o parkado NÃO cobre

O validador parkado tem `if "/devices/virtual/" in hid_parent: return None` — com BlueZ 5.85
(instalado nesta máquina) TODO controle BT físico mora em `/devices/virtual/misc/uhid/`. A
regra parkada MATARIA os DualSense BT reais (o mesmo bug BLUEZ-UHID-01 que cegou o daemon em
19/07). O validador novo espelha a semântica do fix — **identidade pelo uevent do pai HID
imediato (`HID_ID`/`HID_PHYS`/`HID_UNIQ`), jamais topologia** — exatamente como
`_is_virtual_hidraw` (backend_pydualsense.py:137) e `_is_virtual_evdev` (evdev_reader.py:54),
que podem ser LIDOS e ter a semântica reusada, nunca alterados.

Constantes de identidade do vpad (espelhadas de backend_pydualsense.py:114-115 — o broker é
stdlib autocontido, não importa o pacote; o teste de paridade trava os valores):

```python
VPAD_PHYS_PREFIX = "hefesto-vpad"   # HID_PHYS do blueprint do nosso vpad
VPAD_UNIQ_PREFIX = "02fe"           # HID_UNIQ forjado 02:fe:... (normalizado sem ':')
_MAC_RE = re.compile(r"^[0-9a-f]{2}(:[0-9a-f]{2}){5}$")   # MAC bem-formado
```

### 3.2 Pseudocódigo do validador novo

```python
def validate_physical_node(
    node: object,
    *,
    dev_root: str = "/dev",
    sys_class_hidraw: str = "/sys/class/hidraw",
    sys_class_bluetooth: str = "/sys/class/bluetooth",
    stat_fn: Callable[[str], Any] = os.stat,
    lstat_fn: Callable[[str], Any] = os.lstat,
) -> str | None:
    """Basename canônico `hidrawN` se `node` é DualSense FÍSICO 054c:0ce6; senão None.

    Barreiras na ordem (1-3 e 5 herdadas do parkado; 4 é a decisão BLUEZ-UHID-01):
      1. caminho canônico literal `/dev/hidrawN` (canonical_hidraw_base, reusada);
      2. não-symlink + char device;
      3. (major,minor) do nó casa /sys/class/hidraw/<base>/dev;
      4. identidade do pai HID (uevent): HID_ID zero-preenchido BUS:VVVV:PPPP com
         bus∈{0003,0005}, vendor 054C, product 0CE6 (0DF2 = vpad, SEMPRE rejeitado
         ANTES do != geral; 057E Nintendo cai no vendor);
         + regras da subárvore /devices/virtual/misc/uhid/ (abaixo);
      5. o caminho do cliente nunca é reconcatenado — só o basename validado.
    """
    base = canonical_hidraw_base(node, dev_root=dev_root)
    if base is None:
        return None
    sys_dir = f"{sys_class_hidraw}/{base}"
    ... # barreiras 2-3 idênticas ao parkado (lstat/stat/S_ISCHR/dev_sysfs)
    hid_parent = os.path.realpath(f"{sys_dir}/device")
    uevent = _parse_uevent(f"{sys_dir}/device/uevent")     # dict chave=valor
    bus, vendor, product = _parse_hid_id(uevent.get("HID_ID", ""))   # regex do parkado
    if bus not in (0x0003, 0x0005) or vendor != 0x054C:
        return None
    if product == 0x0DF2:      # vpad: explícito ANTES do != geral (invariante)
        return None
    if product != 0x0CE6:
        return None
    # ---- decisão BLUEZ-UHID-01: /devices/virtual/ NÃO é veredito ----
    if "/devices/virtual/" in hid_parent:
        if "/misc/uhid/" not in hid_parent:
            return None            # uinput/virtual puro jamais é físico
        # uhid: físico SÓ se for o padrão do bluetoothd (BT real):
        if bus != 0x0005:
            return None            # (D1) USB real NUNCA é uhid: 0003 sob uhid = forjado
        phys = uevent.get("HID_PHYS", "").strip().lower()
        uniq = uevent.get("HID_UNIQ", "").strip().lower()
        if phys.startswith(VPAD_PHYS_PREFIX):
            return None            # (D2) nosso vpad, mesmo que anuncie 0CE6
        if uniq.replace(":", "").startswith(VPAD_UNIQ_PREFIX):
            return None            # (D2)
        if not _MAC_RE.match(uniq):
            return None            # (D3) BT real tem HID_UNIQ = MAC do controle
        if not _MAC_RE.match(phys):
            return None            # (D3) BT real tem HID_PHYS = MAC do adaptador
        # (D4) belt OPCIONAL e best-effort: HID_PHYS casa o address de algum
        # hci*? Só REJEITA se a leitura dos adaptadores FUNCIONOU e nenhum
        # casou. Ilegível/vazio (adaptador down, rfkill — visto ao vivo nesta
        # máquina: hci0 sem `address` legível) ⇒ NÃO decide, aceita pelas
        # D1-D3. Nunca pode matar um DualSense BT real por sysfs instável.
        adapters = _adapter_addresses(sys_class_bluetooth)   # set[str] ou None
        if adapters is not None and adapters and phys not in adapters:
            return None
    # uevent ILEGÍVEL sob /devices/virtual/ ⇒ None (rejeita): o broker é o
    # inverso do daemon aqui — na dúvida, NÃO esconder/abrir (fail-closed).
    return base
```

Diferença deliberada do daemon: em `_is_virtual_hidraw`, uevent ilegível ⇒ `True` (trata como
virtual) porque o risco maior lá é auto-adoção. No broker, ilegível ⇒ **rejeita** (fail-closed):
o risco maior é agir sobre nó errado. As duas escolhas derivam da mesma regra "na dúvida, o
lado seguro".

### 3.3 Revalidação validar→agir (lição 5, minor-reuse) — padrão O_PATH

Entre `validate_physical_node()` e o `chmod`/`setxattr` (hide/restore) o nome pode ser
reciclado para OUTRO device (unplug + replug rápido reusa `hidrawN` e até o minor). O parkado
agia por caminho (TOCTOU real). O novo `FsAclOps` **pina o inode** com `O_PATH`:

```python
class FsAclOps:
    def _pin(self, node: str, base: str) -> int | None:
        """O_PATH no nó + fstat×sysfs. None = nó sumiu/reciclado (tratar como gone)."""
        try:
            fd = os.open(node, os.O_PATH | os.O_NOFOLLOW | os.O_CLOEXEC)
        except OSError:
            return None
        st = os.fstat(fd)
        if not stat.S_ISCHR(st.st_mode) or self._sysfs_rdev(base) != (
            os.major(st.st_rdev), os.minor(st.st_rdev)
        ):
            os.close(fd)
            return None
        return fd

    def hide(self, node: str, base: str) -> None:
        fd = self._pin(node, base)
        if fd is None:
            raise FileNotFoundError(node)       # vira restore_node_gone/hide "gone"
        try:
            ref = f"/proc/self/fd/{fd}"         # operações no INODE pinado, não no nome
            with contextlib.suppress(OSError):  # ENODATA = já sem ACL
                os.removexattr(ref, _ACL_XATTR)
            os.chmod(ref, 0o600)
        finally:
            os.close(fd)

    def restore(self, node: str, base: str, uid: int) -> None:
        fd = self._pin(node, base)              # nome stale ⇒ FileNotFoundError (gone)
        if fd is None:
            raise FileNotFoundError(node)
        try:
            ref = f"/proc/self/fd/{fd}"
            os.chmod(ref, 0o660)
            os.setxattr(ref, _ACL_XATTR, encode_access_acl(uid))   # blob do parkado, reusado
        finally:
            os.close(fd)
```

(`ProcSubset=pid` mantém `/proc/self/fd/` acessível — só esconde o resto de /proc.) O mesmo
padrão fstat-pós-open cobre o cmd `open` (§1.2). `encode_access_acl`/`decode_acl_user_uids`/
`is_exposed_to` do parkado são reusados byte a byte (validados ao vivo contra blob do setfacl).

### 3.4 Tabela de casos aceita/rejeita

| Caso (uevent do pai HID imediato) | Onde mora | Veredito | Barreira |
|---|---|---|---|
| USB físico `HID_ID=0003:0000054C:00000CE6` | `/devices/pci.../usb3/...` | **ACEITA** | identidade |
| BT físico BlueZ 5.85 `0005:...:00000CE6`, `HID_UNIQ=a0:fa:9c:00:00:01`, `HID_PHYS=d8:44:89:00:00:05` | `/devices/virtual/misc/uhid/` | **ACEITA** | BLUEZ-UHID-01 (D1-D4) — evidência viva `.0006`/`.0007` |
| vpad nosso `0003:...:00000DF2` | uhid | rejeita | product 0DF2 explícito |
| vpad hipotético anunciando 0CE6 (`HID_PHYS=hefesto-vpad*` ou `HID_UNIQ=02:fe:*`) | uhid | rejeita | D2 (identidade do vpad) |
| Nintendo/8BitDo `...:0000057E:...` | qualquer | rejeita | vendor ≠ 054C |
| uhid forjado por processo user: `0003:0000054C:00000CE6` | `/devices/virtual/misc/uhid/` | rejeita | D1: USB real nunca é uhid |
| uhid forjado: `0005:...:00000CE6` com `HID_UNIQ` não-MAC ou `HID_PHYS` não-MAC | uhid | rejeita | D3 |
| uhid forjado: `0005:...:00000CE6` com UNIQ/PHYS MACs plausíveis, PHYS ≠ address de hci* legível | uhid | rejeita | D4 (belt, quando sysfs BT legível) |
| uhid forjado PERFEITO (0005 + MACs plausíveis + PHYS do adaptador real, ou sysfs BT ilegível) | uhid | **aceita** | risco residual — §3.5 |
| `/dev/../dev/hidraw3`, symlink, `/dev/hidraw`, basename estranho | — | rejeita | canonical + lstat |
| (major,minor) divergente do sysfs; reciclagem entre validar e agir | — | rejeita/gone | barreira 3 + O_PATH/fstat (§3.3) |
| uevent ilegível sob `/devices/virtual/` | uhid | rejeita | fail-closed do broker |

### 3.5 uhid forjado: investigação, mitigações e risco residual

**Fato investigado nesta máquina**: `/dev/uhid` tem `MODE 0660 + TAG uaccess`
(assets/71-uhid.rules) — QUALQUER processo do uid da sessão pode criar um device uhid com
`HID_ID`/`HID_UNIQ`/`HID_PHYS` arbitrários (o kernel não valida), e a rule 70 dá uaccess ao
hidraw resultante (ela casa `KERNELS=="0005:054C:0CE6.*"`). O sysfs NÃO expõe o uid criador do
device uhid (conferido: uevent/diretório são root:root, sem attr de dono) — "dono do uhid" não
é um sinal disponível. "Uniq colidindo com físico já visto" exigiria estado histórico no broker
(que renasce limpo a cada vida) — considerado e DESCARTADO: estado extra, ganho nulo (abaixo).

**Análise de ganho do atacante** (por que o risco residual é aceitável): o forjador é, por
definição, um processo do MESMO uid da sessão (é o único que abre `/dev/uhid` via uaccess e o
único que o SO_PEERCRED deixa falar com o broker). O que ele consegue com um forjado perfeito:
1. `hide` do nó forjado ⇒ esconde o PRÓPRIO device — DoS contra si mesmo, nada muda para os
   nós reais (refcount por-nó é independente).
2. `open` do nó forjado ⇒ recebe fd de um device que **ele mesmo criou e já podia abrir** via
   uaccess. Zero elevação.
3. O broker JAMAIS abre/toca outro nó por causa do forjado: toda operação é no
   `/dev/hidrawN` validado + inode pinado; não há caminho do forjado para o hidraw do teclado,
   de outro uid, ou de outro seat.
O único abuso real de um cliente malicioso do mesmo uid é `restore`/`restore_all` expondo o
físico no meio do jogo — que NÃO depende de forjar uhid (qualquer conexão autorizada pode), e é
o mesmo risco já aceito no desenho parkado: mesmo-uid = mesma sessão = já era dono do device
pelo uaccess. **Defesa escolhida**: SO_PEERCRED (uid único) + DAC do socket + validador
fail-closed + operações pinadas por inode; o forjado perfeito fica documentado como residual de
severidade baixa (sem elevação de privilégio possível).

---

## §4 — Lease, refcount e restore à prova de falha (lições 2-3)

Estruturas herdadas do parkado (`hidden: dict[str, _HiddenNode]` com `uid` gravado no hide +
`refcount`; `by_conn: dict[int, set[str]]`), com QUATRO correções obrigatórias:

1. **Hide re-aplica o fs mesmo já rastreado** (lição 2 / achado "idempotência deixa nó recriado
   exposto"):

```python
def _cmd_hide(self, conn_id, peer_uid, node):
    ...validação idêntica...
    held = self.by_conn.setdefault(conn_id, set())
    entry = self.hidden.get(canon)
    try:
        self._ops.hide(canon, base)          # SEMPRE toca o fs (idempotente e barato);
    except FileNotFoundError:                # nó recriado renasce exposto e o estado
        ...                                  # em memória não é prova de nada.
    except OSError as exc:
        self._log("hide_failed", node=canon, err=str(exc))
        return {"ok": False, "cmd": "hide", "node": canon, "error": "hide_failed"}
    if entry is None:
        self.hidden[canon] = _HiddenNode(uid=peer_uid)
    elif canon not in held:
        entry.refcount += 1
    held.add(canon)
    return {"ok": True, "cmd": "hide", "node": canon, "state": "hidden"}
```

2. **Só destrackear DEPOIS do restore de fs OK** (lição 2 / "restore falho orfaniza o nó"):

```python
def _fs_restore(self, canon: str, base: str, uid: int) -> dict[str, object]:
    for tentativa in (1, 2, 3):                    # retry com backoff curto (0/50/200 ms)
        try:
            self._ops.restore(canon, base, uid)
        except FileNotFoundError:
            return {"ok": True, "state": "gone", ...}          # unplug: não é erro
        except OSError as exc:
            if tentativa == 3:
                self._log("restore_failed", node=canon, err=str(exc))
                return {"ok": False, "error": "restore_failed", ...}
            time.sleep((0, 0.05, 0.2)[tentativa])
            continue
        if self._ops.is_exposed_to(canon, uid):    # restore VERIFICADO (getfacl/stat)
            return {"ok": True, "state": "exposed", ...}
        self._log("restore_verify_failed", node=canon, uid=uid, tentativa=tentativa)
    return {"ok": False, "error": "restore_verify_failed", ...}   # doctor enxerga

# no _cmd_restore / on_conn_closed: o pop de self.hidden[canon] SÓ acontece
# quando _fs_restore devolveu ok=True (exposed OU gone). ok=False mantém o nó
# rastreado (na lease e no hidden) — o retry natural (próximo restore_all, EOF,
# ExecStopPost, baseline do restart) tenta de novo. NUNCA "esquecer" um nó 0600.
```

3. **OSError num nó NÃO derruba a lease inteira** (lição 3): `on_conn_closed` e
   `_cmd_restore_all` iteram TODOS os nós SEMPRE — falha em um vira log + nó mantido no
   rastreio, e o loop segue para os demais (o parkado já iterava; a mudança é não destrackear
   o falho e nunca abortar o loop):

```python
def on_conn_closed(self, conn_id: int) -> list[str]:
    restored, failed = [], []
    for canon in sorted(self.by_conn.get(conn_id, set())):
        entry = self.hidden.get(canon)
        if entry is None:
            continue
        if entry.refcount > 1:                 # outra lease viva segura o nó
            entry.refcount -= 1
            continue
        response = self._fs_restore(canon, _base_of(canon), entry.uid)
        if response["ok"]:
            del self.hidden[canon]
            restored.append(canon)
        else:
            failed.append(canon)               # rastreado; belts cobrem
    self.by_conn.pop(conn_id, None)
    if failed:
        self._log("lease_restore_parcial", conn=conn_id, failed=",".join(failed))
    return restored
```

4. **Criação de lease sob lock** (lição 3 / corrida de GC): o broker novo continua
   single-thread (selectors) — a corrida do parkado era do CLIENTE (duas threads do daemon
   criando `HidrawBrokerClient` simultâneos ⇒ a lease perdedora era GC'd e o `__del__`/close
   desfazia hides). Correções: (a) `broker_client_for(daemon)` cria o singleton sob um
   `threading.Lock` de módulo (double-checked); (b) `HidrawBrokerClient` NÃO fecha a conexão em
   `__del__` (só `close()` explícito) — GC de um cliente duplicado acidental nunca dispara
   restore; (c) o cliente é criado no `lifecycle` (campo `_hidraw_broker_client`) uma única vez.

Belts das units mantidos: `ExecStartPre=... --restore-all-and-exit` (baseline limpo — nunca
herda físico 0600 órfão de vida anterior) e `ExecStopPost=... --restore-all-and-exit` (parar/
desinstalar restaura tudo). `restore_all_physical()` do parkado é reusado com o validador novo
e o `FsAclOps` pinado.

---

## §5 — Units systemd: socket sobrevive a restart + DeviceAllow para o cmd open

### 5.1 Mudanças estruturais vs parkado

| Mudança | Motivo |
|---|---|
| **REMOVER** `RuntimeDirectory=hefesto-hidraw-broker` do `.service` | Lição 4 (#10): RuntimeDirectory é apagado em TODO stop/crash do serviço — levava o `broker.sock` junto e a lease nunca renascia. O DONO do caminho é a **socket unit**: `ListenStream=` cria o diretório-pai com `DirectoryMode=0755` e só remove o socket quando a PRÓPRIA socket unit para (disable intencional). Restart/crash do serviço mantém o socket de pé e as conexões pendentes enfileiradas. |
| **TROCAR** `DevicePolicy=closed` sem allow → `DevicePolicy=closed` **+ `DeviceAllow=char-hidraw rw`** | O desenho antigo não abria device nenhum ("o mínimo é nenhum"). Com o cmd `open` isso MUDA: o broker faz `open(2)` real de `/dev/hidrawN`. O device cgroup governa exatamente esse open. |
| Manter todo o resto do hardening | Revisado diretiva a diretiva na matriz 5.3. |

**Por que `DeviceAllow=char-hidraw rw` e não as alternativas**:
- major numérico (`DeviceAllow=/dev/char/237:* `): o major do hidraw é **dinâmico** (alocado no
  boot; 237 hoje, outro amanhã) — quebraria silenciosamente num kernel novo.
- `DeviceAllow=/dev/hidraw3 rw`: nós são dinâmicos e `DeviceAllow` de caminho não aceita glob
  por nó — inviável.
- `char-hidraw` referencia o GRUPO de char devices pelo NOME registrado em `/proc/devices`
  (linha `237 hidraw`) — o systemd resolve o nome→major na aplicação do filtro, à prova de
  major dinâmico. É a forma documentada para grupos dinâmicos (`systemd.resource-control(5)`).
  hidraw é builtin (CONFIG_HIDRAW=y — sempre presente antes do boot da unit).
- `rw` e não `r`: o fd servido é `O_RDWR` (§1.2) — `r` faria o open falhar com EPERM.
- O_PATH do §3.3 não é "acesso a device" para o cgroup (não há read/write no open) — mas a
  allow cobre de qualquer forma; `ExecStartPre`/`ExecStopPost` rodam na mesma unit e herdam.

### 5.2 `assets/systemd/hefesto-hidraw-broker.socket` (delta do parkado)

```ini
[Socket]
ListenStream=/run/hefesto-hidraw-broker/broker.sock
Accept=no
SocketMode=0660
SocketUser=root
SocketGroup=__SESSION_GROUP__
# A SOCKET UNIT é a dona do diretório e do arquivo de socket (lição 4/#10):
# ela cria /run/hefesto-hidraw-broker (DirectoryMode) e só o remove quando ELA
# parar. O .service NÃO tem RuntimeDirectory nenhum — restart/crash do serviço
# não pode apagar o socket debaixo da lease do daemon.
DirectoryMode=0755
```

### 5.3 `assets/systemd/hefesto-hidraw-broker.service` — matriz operação×diretiva

Delta do parkado: sem `RuntimeDirectory`/`RuntimeDirectoryMode`; com
`DeviceAllow=char-hidraw rw`; comentário de cabeçalho atualizado (a justificativa antiga "o
broker nunca abre device" morreu com o cmd open). CADA diretiva revisada contra as operações
REAIS:

| Operação real do broker | Syscalls | Diretiva que governa | Veredito |
|---|---|---|---|
| ler `/sys/class/hidraw/*/dev`, `device/uevent`, `realpath` | openat/read/readlinkat | `ProtectKernelTunables=yes` (só leitura — OK); `@file-system` ∈ `@system-service` | passa |
| ler `/sys/class/bluetooth/hci*/address` (belt D4) | openat/read | idem (leitura) | passa |
| pinar inode (`O_PATH\|O_NOFOLLOW`) + `fstat` | openat/fstat | O_PATH sem acesso de leitura/escrita ao device; `DeviceAllow` cobre por segurança | passa |
| `chmod` via `/proc/self/fd/N` | fchmodat | `CAP_FOWNER` no bounding set; `@file-system`; `ProcSubset=pid` mantém `/proc/self` | passa |
| `setxattr`/`removexattr`/`getxattr` do ACL | \*xattr | `@file-system` (a razão de zero-execve continuar); `CAP_FOWNER` | passa |
| **`open(2)` O_RDWR do hidraw (cmd open)** | openat | **`DeviceAllow=char-hidraw rw`** (novo); `CAP_DAC_OVERRIDE` (nó 0600 root — uid 0 já passa como owner, cap mantida por robustez) | passa |
| **`sendmsg` com SCM_RIGHTS** | sendmsg/recvmsg (cmsg é payload, não syscall própria) | `@network-io` ∈ `@system-service`; `RestrictAddressFamilies=AF_UNIX` | passa — **verificado: nenhum filtro extra necessário para ancillary** |
| accept/recv/close das conexões | accept4/recvfrom/... | idem | passa |
| `sd_notify` (AF_UNIX dgram) | socket/sendto | idem | passa |
| `--restore-all-and-exit` (varre sysfs + restore) | os de cima | mesmas; roda como ExecStartPre/StopPost NA unit (herda tudo) | passa |
| O que o broker NÃO faz | chown, execve, mount, ptrace, ioctl em device | `~@privileged` etc. seguem negando | mantidos |

Diretivas que continuam PROIBIDAS (herdado, documentado no cabeçalho da unit):
`PrivateDevices=yes` (esfregaria /dev — sem hidraw, o open/chmod viram ENOENT) e `udevadm` no
restore (escreveria em /sys × `ProtectKernelTunables`). `MemoryDenyWriteExecute`,
`NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateNetwork`,
`CapabilityBoundingSet=CAP_FOWNER CAP_DAC_OVERRIDE CAP_DAC_READ_SEARCH`, `Type=notify` +
`ExecStartPre`/`ExecStopPost` restore-all: todos mantidos como no parkado.

---

## §6 — Fiação no daemon (reconstruída do README do parkado, com o opener novo)

### 6.1 `daemon/subsystems/gamepad.py`

```python
def _broker_sync_grab(daemon: DaemonProtocol, grab: bool) -> None:
    """Hide/restore do hidraw do físico colado ao EVIOCGRAB (BROKER-01).

    Best-effort SEMPRE: broker ausente ⇒ log debug e segue (duplicado > zero).
    Gates: backend com `hidraw_path` (só pydualsense) e, no hide, fora do Modo
    Nativo. O restore NÃO tem gate de modo: expor nunca é errado.
    """
    with contextlib.suppress(Exception):
        hidraw_fn = getattr(getattr(daemon, "controller", None), "hidraw_path", None)
        if not callable(hidraw_fn):
            return
        from hefesto_dualsense4unix.integrations.hidraw_broker_client import broker_client_for
        client = broker_client_for(daemon)
        if grab:
            if daemon.is_native_mode():
                return
            node = hidraw_fn()
            if isinstance(node, str) and node:
                client.hide(node)
        else:
            client.restore_all()
```

Chamada: última linha de `_set_controller_grab` (gamepad.py:101) — fora do `suppress` do
EVIOCGRAB, com o próprio suppress. Ganha de graça: `release_grab=False` (troca de flavor,
gamepad.py:682) não passa por `_set_controller_grab(False)` ⇒ **não restaura** — o físico segue
escondido durante a recriação do vpad.

```python
def _vpad_vivo(daemon: DaemonProtocol) -> bool:
    """VIDA do vpad, não existência do objeto (lição 6/#17): uhid conta como
    vivo só com `_started` True (UHID_STOP do probe derruba); uinput vivo = objeto."""
    device = getattr(daemon, "_gamepad_device", None)
    if device is None:
        return False
    started = getattr(device, "_started", None)
    return started is not False

def rehide_physical_hidraw(daemon: DaemonProtocol) -> None:
    """Re-hide de TODOS os hidraw físicos com vpad vivo (P1 + jogadores co-op).

    Idempotente por design do broker (lição 2: re-aplica o fs). Chamado do
    reconnect_loop a cada reconciliação online — nó recriado por replug/wake BT
    nasce exposto e é re-escondido aqui. Roda em executor (I/O de socket).
    """
    if daemon.is_native_mode():
        return
    if not getattr(daemon.config, "gamepad_emulation_enabled", False):
        return
    if not _vpad_vivo(daemon):
        return
    hidraw_fn = getattr(daemon.controller, "hidraw_path", None)
    if not callable(hidraw_fn):
        return
    from hefesto_dualsense4unix.integrations.hidraw_broker_client import broker_client_for
    client = broker_client_for(daemon)
    nodes: set[str] = set()
    node = hidraw_fn()
    if isinstance(node, str) and node:
        nodes.add(node)
    coop = getattr(daemon, "_coop_manager", None)
    players = getattr(coop, "_players", None) or {}
    for identity, player in players.items():
        if player.vpad is None or identity.startswith("path:"):
            continue                      # jogador sem vpad vivo NUNCA autoriza hide
        n = hidraw_fn(identity)
        if isinstance(n, str) and n:
            nodes.add(n)
    for n in sorted(nodes):
        client.hide(n)
```

Export no `__all__`: `rehide_physical_hidraw` (o `_broker_sync_grab` é privado do módulo).

### 6.2 `core/physical_report_reader.py` — opener injetável

**Mapa COMPLETO dos call-sites de reopen**: existe UM único `os.open` no reader —
`physical_report_reader.py:336`, dentro de `_run()`. Todos os gatilhos convergem nele:

| Gatilho de reopen | Caminho no código | Passa pelo opener? |
|---|---|---|
| start inicial da thread | `_run()` 1ª iteração → os.open:336 | sim |
| silêncio ≥1 s (`_SILENCE_REOPEN_S`) | `_read_until_lost` return:403 → loop `_run` | sim |
| retarget de primário (`request_reopen`, backend `_recompute_primary`) | flag+wake → return:381/394 → loop | sim |
| wake BT / hotplug-out (ENODEV no read / fd morto sob select) | return:387/409/411 → loop | sim |
| falha de open (backoff exponencial) | except:337 → loop | sim |

Logo, a injeção é UM parâmetro no construtor e UMA linha trocada:

```python
def __init__(
    self,
    path_provider: Callable[[], str | None],
    vpad: Any,
    *,
    max_hz: float = MOTION_EMIT_MAX_HZ,
    time_fn: Callable[[], float] = time.monotonic,
    opener: Callable[[str], int] | None = None,   # NOVO — broker-aware injetado
) -> None:
    ...
    # Contrato do opener: devolve fd pronto para select/read; levanta OSError
    # em falha (o loop já trata com backoff). Default = comportamento de hoje.
    self._opener = opener if opener is not None else (
        lambda path: os.open(path, os.O_RDONLY)
    )

# _run(), linha única alterada:
-               fd = os.open(path, os.O_RDONLY)
+               fd = self._opener(path)
```

GYRO-FD-01 intacto: o fd continua sendo aberto/fechado SOMENTE pela thread do reader; o opener
é chamado da própria thread; fd via broker já chega CLOEXEC (MSG_CMSG_CLOEXEC).

### 6.3 Opener broker-aware (em `integrations/hidraw_broker_client.py`)

```python
def make_broker_opener(daemon: Any) -> Callable[[str], int]:
    """Opener p/ PhysicalReportReader: broker primeiro, os.open de fallback.

    - broker responde `open` ⇒ fd root-aberto (funciona com o nó ESCONDIDO);
    - broker ausente/recusa/timeout ⇒ os.open por caminho (comportamento de
      hoje; se o nó estiver escondido isso dá EACCES e o backoff do reader
      cobre — só acontece na janela broker-morto, em que o próprio broker/
      systemd já restaurou tudo via EOF/ExecStopPost).
    """
    def _open(path: str) -> int:
        fd = broker_client_for(daemon).open_fd(path)
        if fd is not None:
            return fd
        return os.open(path, os.O_RDONLY)
    return _open
```

Call-sites da injeção (os DOIS únicos construtores de `PhysicalReportReader` no repo):
- `gamepad.start_motion_reader` (gamepad.py:539):
  `PhysicalReportReader(path_provider=_primary_hidraw, vpad=device, opener=make_broker_opener(daemon))`
- `coop._start_player_motion_reader` (coop.py:587):
  `PhysicalReportReader(path_provider=_player_hidraw, vpad=vpad, opener=make_broker_opener(self._daemon))`

### 6.4 `daemon/subsystems/coop.py` — hooks por jogador

```python
def _player_hidraw_node(self, identity: str) -> str | None:
    """/dev/hidrawN do físico DESTE jogador via hidraw_path(uniq), ou None."""
    if identity.startswith("path:"):
        return None                       # externo sem MAC: sem handle, sem hide
    hidraw_fn = getattr(self._daemon.controller, "hidraw_path", None)
    if not callable(hidraw_fn):
        return None
    with contextlib.suppress(Exception):
        node = hidraw_fn(identity)
        return node if isinstance(node, str) and node else None
    return None

def _broker_hide_player(self, player: _SecondaryPlayer) -> None:
    """Hide do físico do jogador — SÓ com vpad confirmado (fim do _promote_player)."""
    if player.vpad is None or self._daemon.is_native_mode():
        return
    node = self._player_hidraw_node(player.identity)
    if node is not None:
        with contextlib.suppress(Exception):
            broker_client_for(self._daemon).hide(node)

def _broker_restore_player(self, identity: str) -> None:
    """Restore do físico do jogador no _teardown_player (best-effort; ENOENT ok)."""
    node = self._player_hidraw_node(identity)
    if node is not None:
        with contextlib.suppress(Exception):
            broker_client_for(self._daemon).restore(node)
```

Pontos de chamada: `_broker_hide_player(player)` como ÚLTIMA linha do caminho feliz de
`_promote_player` (depois de `_start_player_motion_reader`, coop.py:499 — reader já nasceu com
o opener); `_broker_restore_player(identity)` no início de `_teardown_player` (antes de
`player.reader.set_grab(False)`, coop.py:609 — obs.: o nó re-resolve por identity; se o
controle já saiu fisicamente, devolve None e o EOF/ENOENT do broker cobre). Controles externos
(8BitDo/Nintendo, `path:*`) nunca têm hide — não têm handle por-uniq e o validador os rejeita
de qualquer forma (defesa dupla).

### 6.5 `daemon/connection.py`

- `reconnect_loop`: após o `connect()` de cada iteração (connection.py:239), quando
  `is_connected`:

```python
with contextlib.suppress(Exception):
    from hefesto_dualsense4unix.daemon.subsystems.gamepad import rehide_physical_hidraw
    await daemon._run_blocking(rehide_physical_hidraw, daemon)
```

  (no executor — o cliente do broker faz I/O com timeout 2 s; nunca no event loop.)
- `shutdown()`: após o bloco `stop_gamepad_emulation` (connection.py:395), close explícito da
  lease:

```python
client = getattr(daemon, "_hidraw_broker_client", None)
if client is not None:
    with contextlib.suppress(Exception):
        client.close()                    # EOF imediato ⇒ broker restaura o que restou
    daemon._hidraw_broker_client = None
```

### 6.6 `daemon/protocols.py` + `daemon/lifecycle.py`

```python
# protocols.py, bloco "Subsystems opt-in" (após _motion_reader):
    # BROKER-01: lease-cliente do broker root hide-hidraw
    # (`integrations.hidraw_broker_client.HidrawBrokerClient`) ou None.
    _hidraw_broker_client: Any

# lifecycle.py, dataclass Daemon (após _motion_reader: Any = None):
    _hidraw_broker_client: Any = None
```

`broker_client_for(daemon)` (parkado, + lock de módulo do §4.4) continua o accessor lazy único.

### 6.7 `tests/conftest.py` — isolamento hermético

Na fixture autouse `_hefesto_fake_env`:

```python
    # BROKER-01: aponta o cliente do broker para um socket INEXISTENTE. Na
    # máquina da mantenedora o broker REAL está de pé — um teste que resolvesse
    # o default esconderia/abriria hidraw DE VERDADE no meio da suíte.
    monkeypatch.setenv("HEFESTO_BROKER_SOCKET", str(tmp_path / ".xdg" / "no-broker.sock"))
```

### 6.8 Gate por Modo Nativo (resumo, sem hook novo)

Entrar no nativo ⇒ `_release_controller_to_game` ⇒ `stop_gamepad_emulation` (release_grab=True)
⇒ `_broker_sync_grab(False)` ⇒ restore_all. Sair ⇒ re-grab ⇒ hide. Boot em nativo ⇒ grab nunca
liga ⇒ hide nunca pedido. O broker permanece agnóstico de modo (política mora no daemon).

---

## §7 — Install/uninstall/doctor/packaging (lição 6)

### 7.1 `install.sh` — passo novo `3h` (system root, DEFAULT sem flag)

Posição: após o 3g (bloco "plataforma/system"), reusando `acquire_sudo`/`as_root` existentes.

```
step "3h" "broker root hide-hidraw (cura de raiz do P2 duplicado — BROKER-01)"
1. uid="${SUDO_UID:-$(id -u)}"; grupo="$(id -gn -- "${uid}")"
   [[ "${uid}" == "0" ]] && { warn "SESSION_UID resolveu 0 (root) — o broker
       autorizaria ROOT e nenhum daemon de usuária conectaria. Rode ./install.sh
       da SESSÃO da usuária (sudo é pedido internamente). Passo ABORTADO."; }
   # NUNCA renderizar uid 0: aborta o PASSO (não o install) com o erro acima.
2. as_root install -Dm755 src/hefesto_dualsense4unix/broker/hidraw_broker.py \
       /usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker
3. render (sed) __SESSION_UID__/__SESSION_GROUP__ das duas units p/ tmp +
   as_root install -m644 → /etc/systemd/system/hefesto-hidraw-broker.{service,socket}
   # guarda pós-render: grep -q '__SESSION_' nos instalados ⇒ FALHA do passo
4. as_root systemctl daemon-reload
5. as_root systemctl enable --now hefesto-hidraw-broker.socket
   # SÓ o .socket (socket-activation); o .service sobe na 1ª conexão do daemon
6. registro de posse p/ uninstall (mesma disciplina do cmdline-owners PLAT-03):
   ~/.local/state/hefesto-dualsense4unix/broker-owner.conf com os caminhos
   instalados + sha256 de cada um; e as units levam header
   "# instalado por hefesto-dualsense4unix (install.sh) — remoção: uninstall.sh"
```

Sem TTY/sudo recusado: `warn` + pula (padrão da casa — reference_install `sudo exige TTY`);
o daemon degrada para "sem broker" (comportamento de hoje). Idempotente: re-render + re-install
+ re-enable são no-ops seguros.

### 7.2 `uninstall.sh` — simétrico, restore ANTES de remover

```
_NEEDS_SUDO: += [[ -e /etc/systemd/system/hefesto-hidraw-broker.service ]] && _NEEDS_SUDO=1
1. sudo systemctl disable --now hefesto-hidraw-broker.socket hefesto-hidraw-broker.service
   # o stop dispara ExecStopPost --restore-all-and-exit ⇒ NENHUM nó fica 0600
2. belt explícito (cobre unit editada/broker morto):
   sudo /usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker --restore-all-and-exit || true
   # roda ANTES do rm (o binário precisa existir ainda) — ordem obrigatória
3. remove SÓ o que o broker-owner.conf registra E que carrega nosso header
   (nunca toca unit de terceiros): rm units + binário; systemctl daemon-reload
4. rm broker-owner.conf
```

### 7.3 `scripts/doctor.sh` — `check_hidraw_broker`

```
check_hidraw_broker() {
  1. unit instalada?  systemctl cat hefesto-hidraw-broker.socket  (system, SEM --user)
     ausente ⇒ info "broker não instalado (rode ./install.sh)" e retorna
  2. socket ativo?    systemctl is-active hefesto-hidraw-broker.socket
  3. ping (python3 stdlib, JSON-por-linha no broker.sock):
       ok ⇒ peer_uid ecoado deve ser $(id -u)
  4. status ⇒ lista de nós escondidos:
       - escondidos > 0 SEM daemon ativo  ⇒ FAIL (invariante: belts falharam;
         cura: systemctl restart hefesto-hidraw-broker.service)
       - escondidos > 0 em Modo Nativo    ⇒ WARN (nativo exige físico exposto)
       - cruza com getfacl: nó listado deve estar SEM user:$(id -u) (coerência)
  5. validação de recusa a outro uid (best-effort, só se sudo -n disponível):
       sudo -n -u nobody python3 -c "<connect+ping>" ⇒ esperado: conexão
       fechada sem resposta (peer_rejected no journal). Sem sudo ⇒ "pulado".
}
```

### 7.4 Packaging — paridade deb/arch/fedora/flatpak (lição 6/#21)

O problema central: as units precisam de RENDER por-máquina (uid/grupo da sessão) — pacote não
renderiza em build. Desenho uniforme:

- **Todos os formatos** empacotam o binário (`/usr/lib/hefesto-dualsense4unix/hefesto-hidraw-broker`
  nos pacotes; `/usr/local/lib/...` no nativo) e as units-TEMPLATE em
  `/usr/share/hefesto-dualsense4unix/systemd/` (com placeholders). A ATIVAÇÃO (render + enable)
  é sempre um passo pós-install rodado como o install nativo faz — no deb via `postinst`
  interativo NÃO (postinst roda como root sem sessão ⇒ SUDO_UID ausente ⇒ renderizaria 0 —
  PROIBIDO): o postinst só instala arquivos e imprime a instrução; quem ativa é
  `hefesto-dualsense4unix --setup-broker` (novo entrypoint fino que chama o mesmo render, com
  a MESMA guarda uid≠0) ou o próprio install.sh.
- **Remoção por pacote** (achado #21 — purge não pode deixar unit root órfã habilitada):
  `prerm`/`postrm` (deb), `pre_remove` (PKGBUILD .install), `%preun` (spec) executam:
  `systemctl disable --now hefesto-hidraw-broker.socket hefesto-hidraw-broker.service || true`
  + `hefesto-hidraw-broker --restore-all-and-exit || true` + rm das units renderizadas em /etc.
- **Flatpak**: sandbox não instala unit de sistema — `scripts/install-host-udev.sh` (o caminho
  host que já existe para as regras udev) ganha a seção broker (binário + render + enable),
  chamada pela doc do flatpak como hoje.
- `scripts/check_packaging_parity.sh` ganha a seção "paridade do broker": para CADA forma
  (build_deb.sh, PKGBUILD, spec, flatpak yml, install-host-udev.sh) exige referência a
  `hefesto-hidraw-broker` (binário E units E caminho de remoção); `uninstall.sh` obrigatório.
  `tests/unit/test_check_packaging_parity.py` ganha `_seed_broker_parity` (fixture que quebra a
  paridade e comprova que o check FALHA — regra falha-sem/passa-com).

---

## §8 — Manifesto de arquivos por lote (SEM interseção)

**B1 — broker core + units + testes do core** (nada de daemon; testável hermético):
- `src/hefesto_dualsense4unix/broker/__init__.py`
- `src/hefesto_dualsense4unix/broker/hidraw_broker.py` (stdlib autocontido; base = parkado +
  §1 open/SCM_RIGHTS + §3 validador BLUEZ-UHID-01 + §3.3 FsAclOps O_PATH + §4 lease)
- `assets/systemd/hefesto-hidraw-broker.service` (§5, sem RuntimeDirectory, com DeviceAllow)
- `assets/systemd/hefesto-hidraw-broker.socket` (§5)
- `tests/unit/test_hidraw_broker_validator.py` (tabela §3.4 completa, incluindo os casos uhid
  reais desta máquina e os forjados D1-D4)
- `tests/unit/test_hidraw_broker_protocol.py` (cmds herdados + lease/refcount + lições 2-3)
- `tests/unit/test_hidraw_broker_open_fd.py` (NOVO: `_cmd_open` + `_send_with_fd` via
  socketpair real — fd chega, é CLOEXEC, fstat casa; reject_stale_node; fd nunca vaza em erro)
- `tests/unit/test_hidraw_broker_assets.py` (placeholders __SESSION_*, DeviceAllow presente,
  RuntimeDirectory AUSENTE, socket unit dona do path)

**B2 — cliente + fiação do daemon + reader + conftest + testes de fiação**:
- `src/hefesto_dualsense4unix/integrations/hidraw_broker_client.py` (parkado + `open_fd`/
  `_request_with_fds` §1.3 + `make_broker_opener` §6.3 + lock de criação §4.4)
- `src/hefesto_dualsense4unix/core/physical_report_reader.py` (SÓ o opener injetável §6.2)
- `src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py` (`_broker_sync_grab`,
  `_vpad_vivo`, `rehide_physical_hidraw`, injeção do opener no start_motion_reader)
- `src/hefesto_dualsense4unix/daemon/subsystems/coop.py` (`_player_hidraw_node`,
  `_broker_hide_player`, `_broker_restore_player`, opener no reader por jogador)
- `src/hefesto_dualsense4unix/daemon/connection.py` (re-hide no reconnect_loop; close da lease
  no shutdown)
- `src/hefesto_dualsense4unix/daemon/protocols.py` (campo `_hidraw_broker_client`)
- `src/hefesto_dualsense4unix/daemon/lifecycle.py` (campo `_hidraw_broker_client = None`)
- `tests/conftest.py` (env `HEFESTO_BROKER_SOCKET` → inexistente)
- `tests/unit/test_hidraw_broker_client.py` (parkado + open_fd: 1 fd ok; 2 fds ⇒ fecha tudo;
  MSG_CTRUNC ⇒ conexão cai; timeout ⇒ None; fds fechados em TODO caminho de erro)
- `tests/unit/test_hidraw_broker_hooks.py` (gating: hide só com grab+vpad+não-nativo;
  release_grab=False NÃO restaura; rehide gateado por `_vpad_vivo`; coop por jogador;
  `path:*` nunca esconde)
- `tests/unit/test_motion_reader_broker_opener.py` (NOVO: opener injetado é usado em TODOS os
  gatilhos de reopen — silêncio, request_reopen, ENODEV; fallback os.open quando broker nega;
  OSError do opener cai no backoff existente)

**B3 — install/uninstall/doctor/packaging + testes**:
- `install.sh` (passo 3h §7.1, guarda uid≠0, registro de posse)
- `uninstall.sh` (§7.2, restore-all ANTES de remover, _NEEDS_SUDO)
- `scripts/doctor.sh` (`check_hidraw_broker` §7.3)
- `scripts/install-host-udev.sh` (seção broker p/ flatpak/host)
- `scripts/build_deb.sh` (binário+templates+prerm/postrm §7.4)
- `packaging/arch/PKGBUILD` (+ `packaging/arch/hefesto-dualsense4unix.install` pre_remove)
- `packaging/fedora/hefesto-dualsense4unix.spec` (%install/%files/%preun)
- `flatpak/br.andrefarias.Hefesto.yml` (bundla templates p/ install-host)
- `scripts/check_packaging_parity.sh` (seção paridade do broker)
- `tests/unit/test_check_packaging_parity.py` (`_seed_broker_parity`)
- `tests/unit/test_install_broker_step.py` (NOVO: render das units — sed produz uid/grupo
  reais; uid 0 ABORTA com a mensagem; guarda pós-render pega placeholder sobrando)

Interseção B1∩B2∩B3 = ∅ (conferido arquivo a arquivo).

Regras da casa aplicadas a TODOS os lotes: py3.10 + mypy strict + ruff 0.15.20; pytest zero
skips; todo teste novo falha-sem/passa-com; textos em pt-BR acentuado nas linhas tocadas;
NUNCA tocar `_is_virtual_hidraw`/`_is_virtual_evdev` (só reusar semântica), fiação
`game_signal`/`display_authority`, nem `docs/process/future-broker/` (read-only). O
orquestrador commita; install SEM FLAGS (broker por DEFAULT, opt-out se algum dia existir será
`--no-broker`); uninstall simétrico. NÃO reiniciar bluetoothd nem mexer no daemon vivo.

---

## §9 — Riscos mapeados e plano de aceite

| Risco | Mitigação / posição |
|---|---|
| Janela residual hotplug→re-hide (§2.3) | Aceita e documentada; hide preventivo + wrapper como 2ª camada; encolher via evento é otimização futura. |
| uhid forjado perfeito por processo do mesmo uid (§3.5) | D1-D4 fecham quase todo o espaço; residual sem elevação de privilégio (o forjador já era dono do device); SO_PEERCRED + operações pinadas por inode. |
| Qualquer processo do uid pode pedir `restore` (expõe no meio do jogo) | Herdado do desenho original e aceito: mesmo-uid = mesma sessão dona; jogo não conhece o socket; DAC 0660 root:grupo. |
| `DeviceAllow=char-hidraw` não resolver | hidraw é builtin (nome presente em /proc/devices desde o boot); doctor cobre com teste funcional de `open`. |
| Backend hidapi sob nó escondido (enumerate/reopen por caminho no `connect()`) | Por design o backend NÃO reabre nó adotado (mantém handle); nó recriado nasce visível antes do re-hide. **Ponto de atenção do gate ao vivo**: confirmar que `hid_enumerate` com nó 0600 não faz o backend declarar unplug (se fizer, tratar EACCES-de-enumerate como "presente-sem-acesso" — correção localizada no backend, fora deste desenho). |
| fd O_RDWR no reader (que só lê) | Disciplina de código + auditoria adversarial; O_RDWR é exigência do contrato do broker (§1.2) e futura via de feature-report. |
| Cliente lento/travado no caminho do grab | timeout 2 s por operação + chamadas via executor (§6.5); hide/restore best-effort jamais bloqueiam start/stop da emulação. |
| Restore falho persistente (fs esquisito) | Nó permanece rastreado (nunca destrackear sem fs OK) + retry + `restore_verify_failed` no doctor + belts ExecStartPre/StopPost/uninstall. |
| Pacote purgado deixando unit root habilitada | prerm/preun/pre_remove com disable+restore (§7.4) + paridade travada no check + teste. |

**Gate de aceite ao vivo** (depois da auditoria adversarial, antes de considerar entregue):
1. Com vpad P1 + jogo SEM wrapper: `lsof /dev/hidrawN(físico)` sem processo do jogo;
   `getfacl` sem `user:1000` durante o jogo; vpad visível ao jogo.
2. **Gyro vivo o tempo todo** (a razão da onda): com físico escondido, forçar silence-reopen
   (1 s), retarget (troca de primário) e wake BT — `motion_hz` > 0 contínuo no doctor, zero
   `motion_reader_open_failed` com EACCES no journal.
3. `kill -9` no daemon ⇒ `getfacl` volta `user:1000` em <1 s (EOF da lease).
4. `systemctl restart hefesto-hidraw-broker.service` NÃO apaga o broker.sock (lição 4) e o
   daemon re-esconde no tick seguinte.
5. Replug USB + reconexão BT com jogo aberto: nó novo re-escondido; duplicado nunca vira zero.
6. Modo Nativo: entrar expõe, sair re-esconde; boot em nativo nunca esconde.
7. `sudo -u nobody` no socket ⇒ recusado; doctor verde em todos os checks novos.
8. Uninstall com nó escondido ⇒ nó restaurado ANTES da remoção; re-install idempotente.

— fim do desenho —
