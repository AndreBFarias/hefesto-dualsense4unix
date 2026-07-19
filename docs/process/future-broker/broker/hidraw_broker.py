#!/usr/bin/env python3
"""hefesto-hidraw-broker — broker root que esconde o hidraw do DualSense FÍSICO.

BROKER-01 (FUT-01/PLAT-02) — cura de RAIZ do "P2 duplicado": daemon, Steam e o
jogo rodam com o MESMO uid, então o DAC não separa quem pode abrir o hidraw do
físico. Este serviço (o PRIMEIRO serviço systemd de SISTEMA do projeto) roda
como root isolado/hardened e, a pedido do daemon, tira a ACL do uaccess do nó
(`setfacl -b` + `chmod 0600`) — o jogo não consegue mais `open(2)`, em QUALQUER
backend (SDL, winebus-hidraw, libScePad, HIDAPI). O fd JÁ ABERTO do daemon
sobrevive: permissão só é checada no open(2).

Spec completa: docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md.

Regras de ouro (invariante "duplicado > zero controles"):
  - A conexão do daemon É a lease: EOF (daemon morreu) restaura TUDO que aquela
    conexão escondeu — sem heartbeat, o kernel garante o EOF.
  - `--restore-all-and-exit` (ExecStartPre/ExecStopPost) restaura qualquer
    físico deixado escondido por uma vida anterior do broker.
  - O validador SÓ aceita hidraw cujo pai HID imediato tem HID_ID de DualSense
    físico (054c:0ce6 em USB 0003 ou BT 0005). O vpad 0df2 é REJEITADO
    explicitamente — é por ele que o jogo fala com o controle.

ESCOLHA DE IMPLEMENTAÇÃO DA ACL (documentada, exigência da spec §5.2): xattr
direto via `os.setxattr`/`os.removexattr` no `system.posix_acl_access` — é o
MESMO xattr que a rota ctypes→libacl escreveria (`acl_set_file` é um setxattr
deste blob) e que o `setfacl` produz. Verificado byte a byte ao vivo na máquina
de referência (blob de 44 bytes, header versão 2 LE + entradas `<HHI`). Ganhos
sobre as duas rotas do estudo: ZERO execve (o `SystemCallFilter=@system-service
~@privileged` da unit fica intacto — `setxattr` já está em `@file-system`) e
zero dependência de ABI da libacl.so. Formato estável do kernel
(`include/uapi/linux/posix_acl_xattr.h`).

Arquivo 100% stdlib e AUTOCONTIDO de propósito: o install copia só este arquivo
para /usr/local/lib/hefesto-dualsense4unix/hefesto-hidraw-broker e ele roda no
python3 do sistema, sem venv e sem importar o pacote.
"""
from __future__ import annotations

import argparse
import contextlib
import errno
import json
import os
import re
import selectors
import signal
import socket
import stat as stat_mod
import struct
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

#: Socket de comando (criado pelo systemd via hefesto-hidraw-broker.socket).
DEFAULT_SOCKET_PATH = "/run/hefesto-hidraw-broker/broker.sock"
#: Env com o uid autorizado (renderizado pelo install a partir de SUDO_UID).
ALLOWED_UID_ENV = "HEFESTO_BROKER_ALLOWED_UID"
#: Linha de protocolo maior que isto é rejeitada (`reject_oversize`, spec §3.1).
MAX_LINE_BYTES = 4096

# Identidade canônica (HID_ID do pai HID imediato — transport-independent).
PHYS_VENDOR = 0x054C  # Sony
PHYS_PRODUCT = 0x0CE6  # DualSense físico
VPAD_PRODUCT = 0x0DF2  # DualSense Edge = NOSSO vpad — NUNCA esconder
BUS_USB = 0x0003
BUS_BT = 0x0005
ACCEPTED_BUSES = frozenset({BUS_USB, BUS_BT})

_HIDRAW_BASE_RE = re.compile(r"^hidraw[0-9]+$")
#: Formato REAL (zero-preenchido) do uevent do kernel: BUS:0000VVVV:0000PPPP —
#: ex.: HID_ID=0003:0000054C:00000CE6 (USB), 0005:0000054C:00000CE6 (BT).
_HID_ID_RE = re.compile(r"^HID_ID=([0-9A-Fa-f]{4}):([0-9A-Fa-f]{8}):([0-9A-Fa-f]{8})$")


def _log(event: str, **fields: object) -> None:
    """Log estruturado simples no stdout (vai ao journal via systemd)."""
    parts = [event] + [f"{key}={value}" for key, value in fields.items()]
    print("[hidraw-broker] " + " ".join(parts), flush=True)


# ---------------------------------------------------------------------------
# Validador (spec §4) — SÓ nós filhos do DualSense físico 054c:0ce6
# ---------------------------------------------------------------------------


def canonical_hidraw_base(node: object, *, dev_root: str = "/dev") -> str | None:
    """Basename `hidrawN` se `node` é EXATAMENTE `<dev_root>/hidrawN`; senão None.

    Checagem puramente textual (sem tocar o fs): rejeita `..`, barras extras,
    prefixo errado e basenames que não são `hidraw<N>`. Depois de validado, o
    broker SÓ opera em caminhos reconstruídos a partir do basename — o caminho
    do cliente nunca é reusado por concatenação.
    """
    if not isinstance(node, str) or not node:
        return None
    base = os.path.basename(node)
    if _HIDRAW_BASE_RE.match(base) is None:
        return None
    if node != f"{dev_root}/{base}":
        return None
    return base


def validate_physical_node(
    node: object,
    *,
    dev_root: str = "/dev",
    sys_class_hidraw: str = "/sys/class/hidraw",
    stat_fn: Callable[[str], Any] = os.stat,
    lstat_fn: Callable[[str], Any] = os.lstat,
) -> str | None:
    """Basename canônico `hidrawN` se `node` é um DualSense FÍSICO; senão None.

    NUNCA abre o device. Barreiras, na ordem:
      1. caminho canônico literal (`canonical_hidraw_base`);
      2. o nó não pode ser symlink e PRECISA ser char device;
      3. `(major, minor)` do nó casa o `/sys/class/hidraw/<base>/dev` (fecha
         "symlink/nó plantado apontando para outro device");
      4. o pai HID não pode ser `/devices/virtual/` (uhid forjado que se
         anuncia 0ce6 é rejeitado aqui);
      5. `HID_ID` do uevent do pai HID imediato — formato zero-preenchido REAL
         `BUS:0000VVVV:0000PPPP` — tem de ser 054c:0ce6 em bus USB (0003) ou
         BT (0005). O passeio até `idVendor` foi descartado de propósito: no
         BT ele acha o ADAPTADOR (descoberta A do estudo).
    `stat_fn`/`lstat_fn` são injetáveis só para os testes herméticos (não dá
    para criar char device sem root); default = os.stat/os.lstat reais.
    """
    if not isinstance(node, str):
        return None
    base = canonical_hidraw_base(node, dev_root=dev_root)
    if base is None:
        return None
    sys_dir = f"{sys_class_hidraw}/{base}"
    try:
        if stat_mod.S_ISLNK(lstat_fn(node).st_mode):
            return None
        st = stat_fn(node)
        if not stat_mod.S_ISCHR(st.st_mode):
            return None
        with open(f"{sys_dir}/dev", encoding="ascii") as fh:
            dev_sysfs = fh.read().strip()
        if dev_sysfs != f"{os.major(st.st_rdev)}:{os.minor(st.st_rdev)}":
            return None
        hid_parent = os.path.realpath(f"{sys_dir}/device")
        if "/devices/virtual/" in hid_parent:
            return None
        with open(f"{sys_dir}/device/uevent", encoding="ascii", errors="replace") as fh:
            uevent = fh.read()
    except OSError:
        return None
    for line in uevent.splitlines():
        match = _HID_ID_RE.match(line.strip())
        if match is None:
            continue
        bus = int(match.group(1), 16)
        vendor = int(match.group(2), 16)
        product = int(match.group(3), 16)
        if bus not in ACCEPTED_BUSES:
            return None
        if vendor != PHYS_VENDOR:
            return None
        if product == VPAD_PRODUCT:
            # Explícito ANTES do != geral: o vpad 0df2 JAMAIS é escondido —
            # é por ele que rumble/triggers/lightbar do jogo chegam.
            return None
        if product != PHYS_PRODUCT:
            return None
        return base
    return None


# ---------------------------------------------------------------------------
# Mecânica de hide/restore (spec §5) — ACL via xattr direto (ver docstring)
# ---------------------------------------------------------------------------

_ACL_XATTR = "system.posix_acl_access"
_ACL_VERSION = 2
_ACL_TAG_USER_OBJ = 0x01
_ACL_TAG_USER = 0x02
_ACL_TAG_GROUP_OBJ = 0x04
_ACL_TAG_MASK = 0x10
_ACL_TAG_OTHER = 0x20
_ACL_PERM_RW = 0x06
_ACL_ID_UNDEFINED = 0xFFFFFFFF


def encode_access_acl(uid: int) -> bytes:
    """ACL binária equivalente a `chmod 0660` + `setfacl -m u:<uid>:rw`.

    Byte-idêntica ao blob que o setfacl grava (validado ao vivo): header u32 LE
    versão 2 + entradas `<HHI` (tag, perm, id) ordenadas por tag.
    """
    entries = (
        (_ACL_TAG_USER_OBJ, _ACL_PERM_RW, _ACL_ID_UNDEFINED),
        (_ACL_TAG_USER, _ACL_PERM_RW, uid),
        (_ACL_TAG_GROUP_OBJ, _ACL_PERM_RW, _ACL_ID_UNDEFINED),
        (_ACL_TAG_MASK, _ACL_PERM_RW, _ACL_ID_UNDEFINED),
        (_ACL_TAG_OTHER, 0x00, _ACL_ID_UNDEFINED),
    )
    return struct.pack("<I", _ACL_VERSION) + b"".join(
        struct.pack("<HHI", tag, perm, eid) for tag, perm, eid in entries
    )


def decode_acl_user_uids(blob: bytes) -> set[int]:
    """uids com entrada USER de leitura+escrita na ACL binária (verificação)."""
    uids: set[int] = set()
    if len(blob) < 4 or struct.unpack("<I", blob[:4])[0] != _ACL_VERSION:
        return uids
    offset = 4
    while offset + 8 <= len(blob):
        tag, perm, eid = struct.unpack("<HHI", blob[offset : offset + 8])
        if tag == _ACL_TAG_USER and perm & _ACL_PERM_RW == _ACL_PERM_RW:
            uids.add(eid)
        offset += 8
    return uids


class FsAclOps:
    """Operações REAIS de fs (hide/restore/verify) — injetável nos testes."""

    def hide(self, node: str) -> None:
        """`setfacl -b` + `chmod 0600` → só root abre. Fd já aberto sobrevive."""
        try:
            os.removexattr(node, _ACL_XATTR)
        except OSError as exc:
            if exc.errno != errno.ENODATA:
                raise
        os.chmod(node, 0o600)

    def restore(self, node: str, uid: int) -> None:
        """`chmod 0660` + ACL `u:<uid>:rw` — reverte exatamente o hide."""
        os.chmod(node, 0o660)
        os.setxattr(node, _ACL_XATTR, encode_access_acl(uid))

    def is_exposed_to(self, node: str, uid: int) -> bool:
        """True se o nó está no estado canônico exposto (0660 + ACL do uid)."""
        try:
            st = os.stat(node)
            if stat_mod.S_IMODE(st.st_mode) != 0o660:
                return False
            blob = os.getxattr(node, _ACL_XATTR)
        except OSError:
            return False
        return uid in decode_acl_user_uids(blob)


# ---------------------------------------------------------------------------
# Estado do broker: protocolo JSON-por-linha + lease/refcount (spec §3 e §7)
# ---------------------------------------------------------------------------


@dataclass
class _HiddenNode:
    """Um nó escondido: uid gravado NO HIDE (fail-safe restaura por ele)."""

    uid: int
    refcount: int = 1


class BrokerState:
    """Protocolo + contabilidade de lease. Puro (fs injetável) e testável.

    `hidden` é o refcount global por nó; `by_conn` é o conjunto que CADA
    conexão escondeu (a lease). Dois daemons em takeover convivem: o novo
    abre lease nova (refcount 2); o velho morre e restaura só a dele — o
    refcount impede expor um nó que o novo re-escondeu (spec §9).
    """

    def __init__(
        self,
        *,
        allowed_uid: int,
        ops: Any | None = None,
        validator: Callable[[str], str | None] | None = None,
        dev_root: str = "/dev",
        sys_class_hidraw: str = "/sys/class/hidraw",
        log: Callable[..., None] = _log,
    ) -> None:
        self.allowed_uid = allowed_uid
        self._ops = ops if ops is not None else FsAclOps()
        self._validator = validator
        self._dev_root = dev_root
        self._sys_class_hidraw = sys_class_hidraw
        self._log = log
        self.hidden: dict[str, _HiddenNode] = {}
        self.by_conn: dict[int, set[str]] = {}

    # -- validação -------------------------------------------------------

    def _validate(self, node: str) -> str | None:
        if self._validator is not None:
            return self._validator(node)
        return validate_physical_node(
            node, dev_root=self._dev_root, sys_class_hidraw=self._sys_class_hidraw
        )

    # -- protocolo -------------------------------------------------------

    def handle_line(self, conn_id: int, peer_uid: int, line: bytes) -> dict[str, object]:
        """Uma requisição JSON-por-linha → uma resposta. NUNCA levanta."""
        if len(line) > MAX_LINE_BYTES:
            return {"ok": False, "error": "reject_oversize"}
        try:
            request = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return {"ok": False, "error": "reject_malformed"}
        if not isinstance(request, dict):
            return {"ok": False, "error": "reject_malformed"}
        cmd = request.get("cmd")
        if cmd == "ping":
            return {"ok": True, "cmd": "ping", "peer_uid": peer_uid}
        if cmd == "status":
            return {"ok": True, "cmd": "status", "hidden": sorted(self.hidden)}
        if cmd == "hide":
            return self._cmd_hide(conn_id, peer_uid, request.get("node"))
        if cmd == "restore":
            return self._cmd_restore(conn_id, request.get("node"))
        if cmd == "restore_all":
            return self._cmd_restore_all(conn_id)
        return {
            "ok": False,
            "cmd": cmd if isinstance(cmd, str) else None,
            "error": "reject_unknown_cmd",
        }

    def _cmd_hide(self, conn_id: int, peer_uid: int, node: object) -> dict[str, object]:
        raw = node if isinstance(node, str) else None
        if canonical_hidraw_base(raw, dev_root=self._dev_root) is None:
            return {"ok": False, "cmd": "hide", "node": raw, "error": "reject_bad_path"}
        assert raw is not None  # narrow p/ mypy: canonical exige str
        base = self._validate(raw)
        if base is None:
            return {
                "ok": False,
                "cmd": "hide",
                "node": raw,
                "error": "reject_not_physical_dualsense",
            }
        canon = f"{self._dev_root}/{base}"
        held = self.by_conn.setdefault(conn_id, set())
        if canon in held:  # idempotente por conexão (re-hide do hotplug)
            return {"ok": True, "cmd": "hide", "node": canon, "state": "hidden"}
        entry = self.hidden.get(canon)
        if entry is not None:  # outra lease já escondeu: só refcount
            entry.refcount += 1
            held.add(canon)
            return {"ok": True, "cmd": "hide", "node": canon, "state": "hidden"}
        try:
            self._ops.hide(canon)
        except OSError as exc:
            self._log("hide_failed", node=canon, err=str(exc))
            return {"ok": False, "cmd": "hide", "node": canon, "error": "hide_failed"}
        self.hidden[canon] = _HiddenNode(uid=peer_uid)
        held.add(canon)
        self._log("node_hidden", node=canon, conn=conn_id, uid=peer_uid)
        return {"ok": True, "cmd": "hide", "node": canon, "state": "hidden"}

    def _cmd_restore(self, conn_id: int, node: object) -> dict[str, object]:
        raw = node if isinstance(node, str) else None
        base = canonical_hidraw_base(raw, dev_root=self._dev_root)
        if base is None:
            return {"ok": False, "cmd": "restore", "node": raw, "error": "reject_bad_path"}
        canon = f"{self._dev_root}/{base}"
        held = self.by_conn.get(conn_id, set())
        entry = self.hidden.get(canon)
        if canon in held:
            held.discard(canon)
            if entry is not None:
                entry.refcount -= 1
                if entry.refcount > 0:  # outra lease ainda segura o nó
                    return {"ok": True, "cmd": "restore", "node": canon, "state": "hidden"}
                del self.hidden[canon]
                return self._fs_restore(canon, entry.uid)
            return self._fs_restore(canon, self.allowed_uid)
        if entry is not None:  # escondido por OUTRA conexão viva: não expõe
            return {"ok": True, "cmd": "restore", "node": canon, "state": "hidden"}
        # Não rastreado: restore best-effort (idempotente), mas SÓ em nó que
        # valida como físico — nunca mexe em hidraw alheio (teclado etc.).
        if self._validate(canon) is None:
            return {
                "ok": False,
                "cmd": "restore",
                "node": canon,
                "error": "reject_not_physical_dualsense",
            }
        return self._fs_restore(canon, self.allowed_uid)

    def _cmd_restore_all(self, conn_id: int) -> dict[str, object]:
        restored: list[str] = []
        for canon in sorted(self.by_conn.get(conn_id, set())):
            response = self._cmd_restore(conn_id, canon)
            if response.get("state") == "exposed" or response.get("state") == "gone":
                restored.append(canon)
        return {"ok": True, "cmd": "restore_all", "restored": restored}

    def _fs_restore(self, canon: str, uid: int) -> dict[str, object]:
        try:
            self._ops.restore(canon, uid)
        except FileNotFoundError:
            # Unplug: o nó sumiu — não é erro (o replug nasce exposto).
            self._log("restore_node_gone", node=canon)
            return {"ok": True, "cmd": "restore", "node": canon, "state": "gone"}
        except OSError as exc:
            self._log("restore_failed", node=canon, err=str(exc))
            return {"ok": False, "cmd": "restore", "node": canon, "error": "restore_failed"}
        if not self._ops.is_exposed_to(canon, uid):
            # Sinal para o doctor (spec §5.3) — nunca fatal.
            self._log("restore_verify_failed", node=canon, uid=uid)
        self._log("node_restored", node=canon, uid=uid)
        return {"ok": True, "cmd": "restore", "node": canon, "state": "exposed"}

    # -- lease (fail-safe §7) --------------------------------------------

    def on_conn_closed(self, conn_id: int) -> list[str]:
        """EOF da lease: restaura tudo que AQUELA conexão escondeu."""
        restored: list[str] = []
        for canon in sorted(self.by_conn.pop(conn_id, set())):
            entry = self.hidden.get(canon)
            if entry is None:
                continue
            entry.refcount -= 1
            if entry.refcount > 0:
                continue  # outra lease viva ainda esconde este nó
            del self.hidden[canon]
            response = self._fs_restore(canon, entry.uid)
            if response.get("ok"):
                restored.append(canon)
        if restored:
            self._log("lease_closed_restored", conn=conn_id, nodes=",".join(restored))
        return restored

    def restore_everything(self) -> list[str]:
        """Belt do shutdown do broker: restaura TODO nó ainda escondido."""
        restored: list[str] = []
        for canon, entry in list(self.hidden.items()):
            del self.hidden[canon]
            response = self._fs_restore(canon, entry.uid)
            if response.get("ok"):
                restored.append(canon)
        self.by_conn.clear()
        return restored


def restore_all_physical(
    *,
    uid: int,
    ops: Any | None = None,
    dev_root: str = "/dev",
    sys_class_hidraw: str = "/sys/class/hidraw",
    validator: Callable[[str], str | None] | None = None,
    log: Callable[..., None] = _log,
) -> list[str]:
    """Varre /sys/class/hidraw e restaura físicos não-expostos (baseline limpo).

    Usado por `--restore-all-and-exit` (ExecStartPre/ExecStopPost): nunca herda
    um físico escondido órfão de uma vida anterior. Idempotente e best-effort.
    """
    fs_ops = ops if ops is not None else FsAclOps()
    restored: list[str] = []
    try:
        entries = sorted(os.listdir(sys_class_hidraw))
    except OSError:
        return restored
    for base in entries:
        node = f"{dev_root}/{base}"
        valid = (
            validator(node)
            if validator is not None
            else validate_physical_node(
                node, dev_root=dev_root, sys_class_hidraw=sys_class_hidraw
            )
        )
        if valid is None:
            continue
        if fs_ops.is_exposed_to(node, uid):
            continue
        try:
            fs_ops.restore(node, uid)
        except OSError as exc:
            log("baseline_restore_failed", node=node, err=str(exc))
            continue
        restored.append(node)
        log("baseline_restored", node=node, uid=uid)
    return restored


# ---------------------------------------------------------------------------
# Servidor: accept + SO_PEERCRED + loop de conexões (spec §1/§3.3/§7)
# ---------------------------------------------------------------------------


def peer_credentials(sock: socket.socket) -> tuple[int, int, int]:
    """(pid, uid, gid) do peer via SO_PEERCRED — kernel-autoritativo."""
    data = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
    pid, uid, gid = struct.unpack("3i", data)
    return int(pid), int(uid), int(gid)


class Broker:
    """Loop de eventos do broker: accept, autoriza (SO_PEERCRED), serve linhas.

    `register_client` é público de propósito: os testes injetam uma ponta de
    `socketpair` sem precisar de socket de escuta nem de /dev real.
    """

    def __init__(
        self,
        state: BrokerState,
        listen_sock: socket.socket | None = None,
        *,
        peercred_fn: Callable[[socket.socket], tuple[int, int, int]] = peer_credentials,
        log: Callable[..., None] = _log,
    ) -> None:
        self._state = state
        self._peercred_fn = peercred_fn
        self._log = log
        self._sel = selectors.DefaultSelector()
        self._listen = listen_sock
        self._next_conn_id = 1
        self._buffers: dict[int, bytearray] = {}
        self._peer_uids: dict[int, int] = {}
        self.stopping = False
        if listen_sock is not None:
            listen_sock.setblocking(False)
            self._sel.register(listen_sock, selectors.EVENT_READ, ("accept", 0))

    def register_client(self, sock: socket.socket) -> int | None:
        """Autoriza e registra uma conexão; None = recusada (e fechada)."""
        try:
            pid, uid, _gid = self._peercred_fn(sock)
        except OSError:
            sock.close()
            return None
        if uid != self._state.allowed_uid:
            self._log("peer_rejected", peer_uid=uid, peer_pid=pid)
            sock.close()
            return None
        conn_id = self._next_conn_id
        self._next_conn_id += 1
        sock.setblocking(False)
        self._sel.register(sock, selectors.EVENT_READ, ("conn", conn_id))
        self._buffers[conn_id] = bytearray()
        self._peer_uids[conn_id] = uid
        self._log("peer_accepted", conn=conn_id, peer_uid=uid, peer_pid=pid)
        return conn_id

    def step(self, timeout: float | None = None) -> None:
        """Uma iteração do selector (testável sem thread)."""
        for key, _events in self._sel.select(timeout):
            kind, conn_id = key.data
            sock = key.fileobj
            assert isinstance(sock, socket.socket)
            if kind == "accept":
                try:
                    client, _addr = sock.accept()
                except OSError:
                    continue
                self.register_client(client)
            else:
                self._service(sock, conn_id)

    def run(self) -> None:
        try:
            while not self.stopping:
                self.step(timeout=1.0)
        finally:
            restored = self._state.restore_everything()
            if restored:
                self._log("shutdown_restored", nodes=",".join(restored))
            self._sel.close()

    # -- interno ---------------------------------------------------------

    def _service(self, sock: socket.socket, conn_id: int) -> None:
        try:
            data = sock.recv(4096)
        except (BlockingIOError, InterruptedError):
            return
        except OSError:
            data = b""
        if not data:
            self._close_conn(sock, conn_id)
            return
        buffer = self._buffers[conn_id]
        buffer.extend(data)
        if len(buffer) > MAX_LINE_BYTES and b"\n" not in buffer:
            # Linha gigante sem fim de linha: cliente quebrado. Fechar é o
            # seguro — o EOF da lease restaura o que ela escondeu.
            self._send(sock, {"ok": False, "error": "reject_oversize"})
            self._close_conn(sock, conn_id)
            return
        while True:
            newline = buffer.find(b"\n")
            if newline < 0:
                return
            line = bytes(buffer[:newline])
            del buffer[: newline + 1]
            if not line.strip():
                continue
            response = self._state.handle_line(conn_id, self._peer_uids[conn_id], line)
            if not self._send(sock, response):
                self._close_conn(sock, conn_id)
                return

    def _send(self, sock: socket.socket, payload: dict[str, object]) -> bool:
        try:
            sock.sendall(json.dumps(payload).encode("utf-8") + b"\n")
            return True
        except OSError:
            return False

    def _close_conn(self, sock: socket.socket, conn_id: int) -> None:
        with contextlib.suppress(KeyError, ValueError):
            self._sel.unregister(sock)
        sock.close()
        self._buffers.pop(conn_id, None)
        self._peer_uids.pop(conn_id, None)
        self._state.on_conn_closed(conn_id)
        self._log("peer_closed", conn=conn_id)


# ---------------------------------------------------------------------------
# Integração systemd (socket activation + notify) — stdlib pura
# ---------------------------------------------------------------------------


def _sd_listen_socket() -> socket.socket | None:
    """fd 3 do systemd (LISTEN_FDS), ou None se não somos socket-activated."""
    if os.environ.get("LISTEN_PID") != str(os.getpid()):
        return None
    try:
        nfds = int(os.environ.get("LISTEN_FDS", "0"))
    except ValueError:
        return None
    if nfds < 1:
        return None
    return socket.socket(fileno=3)


def _sd_notify(message: str) -> None:
    """sd_notify mínimo (READY=1) — best-effort, sem libsystemd."""
    target = os.environ.get("NOTIFY_SOCKET")
    if not target:
        return
    if target.startswith("@"):
        target = "\0" + target[1:]
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
            sock.sendto(message.encode("utf-8"), target)
    except OSError:
        pass


def _manual_listen_socket(path: str) -> socket.socket:
    """Bind manual (debug/execução fora do systemd). Modo 0660."""
    with contextlib.suppress(FileNotFoundError):
        os.unlink(path)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(path)
    os.chmod(path, 0o660)
    sock.listen(8)
    return sock


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--restore-all-and-exit",
        action="store_true",
        help="restaura todo DualSense físico não-exposto e sai (baseline/stop)",
    )
    parser.add_argument(
        "--socket-path",
        default=DEFAULT_SOCKET_PATH,
        help="socket de escuta quando NÃO socket-activated (debug)",
    )
    args = parser.parse_args(argv)

    uid_raw = os.environ.get(ALLOWED_UID_ENV)
    if uid_raw is None or not uid_raw.isdigit():
        _log("allowed_uid_missing", env=ALLOWED_UID_ENV)
        return 1
    allowed_uid = int(uid_raw)

    if args.restore_all_and_exit:
        restored = restore_all_physical(uid=allowed_uid)
        _log("restore_all_done", count=len(restored))
        return 0

    # Baseline em processo também (idempotente; ExecStartPre já cobriu, mas
    # execução manual/debug fica igualmente segura).
    restore_all_physical(uid=allowed_uid)

    listen = _sd_listen_socket()
    if listen is None:
        listen = _manual_listen_socket(args.socket_path)
        _log("listening_manual", path=args.socket_path)

    state = BrokerState(allowed_uid=allowed_uid)
    broker = Broker(state, listen)

    def _stop(_signum: int, _frame: object) -> None:
        broker.stopping = True

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    _sd_notify("READY=1")
    _log("ready", allowed_uid=allowed_uid)
    broker.run()
    return 0


if __name__ == "__main__":  # pragma: no cover - entrypoint real (root)
    sys.exit(main())
