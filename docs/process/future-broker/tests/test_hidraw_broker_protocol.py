"""Protocolo + lease + SO_PEERCRED do broker hide-hidraw (BROKER-01) — hermético.

Sem tocar /dev real: as operações de fs são um dublê que só grava chamadas, o
validador é injetado, e as conexões são `socketpair` (a forma sancionada pela
missão de simular o daemon). Prova:
- JSON-por-linha: hide/restore/restore_all/status/ping; comando desconhecido,
  JSON malformado, linha gigante (`reject_oversize`);
- validador aplicado no hide E no restore (caminho ruim vs. não-físico);
- refcount por nó com DUAS conexões (takeover de daemon) e restore no EOF —
  o coração do fail-safe "duplicado > zero controles";
- SO_PEERCRED: uid errado é recusado ANTES de qualquer comando.
"""
from __future__ import annotations

import json
import os
import socket
from typing import Any

from hefesto_dualsense4unix.broker.hidraw_broker import (
    MAX_LINE_BYTES,
    Broker,
    BrokerState,
    decode_acl_user_uids,
    encode_access_acl,
    peer_credentials,
    restore_all_physical,
)

UID = 1000


class FakeOps:
    """Dublê das operações de fs: grava chamadas, nunca toca /dev."""

    def __init__(self, *, fail_hide: bool = False, fail_restore: Exception | None = None):
        self.calls: list[tuple[Any, ...]] = []
        self.fail_hide = fail_hide
        self.fail_restore = fail_restore

    def hide(self, node: str) -> None:
        if self.fail_hide:
            raise OSError("EPERM")
        self.calls.append(("hide", node))

    def restore(self, node: str, uid: int) -> None:
        if self.fail_restore is not None:
            raise self.fail_restore
        self.calls.append(("restore", node, uid))

    def is_exposed_to(self, node: str, uid: int) -> bool:
        return True


def _validator(node: str) -> str | None:
    """Aceita /dev/hidraw3 e /dev/hidraw7 (os 'físicos' da suíte)."""
    base = node.rsplit("/", 1)[-1]
    return base if base in {"hidraw3", "hidraw7"} else None


def make_state(**kw: Any) -> tuple[BrokerState, FakeOps]:
    ops = kw.pop("ops", FakeOps())
    state = BrokerState(
        allowed_uid=UID, ops=ops, validator=_validator, log=lambda *a, **k: None, **kw
    )
    return state, ops


def req(state: BrokerState, conn: int, payload: Any, uid: int = UID) -> dict[str, Any]:
    line = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
    return dict(state.handle_line(conn, uid, line))


class TestProtocolo:
    def test_ping(self) -> None:
        state, _ = make_state()
        assert req(state, 1, {"cmd": "ping"}) == {"ok": True, "cmd": "ping", "peer_uid": UID}

    def test_status_vazio_e_com_no(self) -> None:
        state, _ = make_state()
        assert req(state, 1, {"cmd": "status"})["hidden"] == []
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        assert req(state, 1, {"cmd": "status"})["hidden"] == ["/dev/hidraw3"]

    def test_hide_fisico_ok(self) -> None:
        state, ops = make_state()
        resposta = req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        assert resposta == {"ok": True, "cmd": "hide", "node": "/dev/hidraw3", "state": "hidden"}
        assert ops.calls == [("hide", "/dev/hidraw3")]

    def test_hide_idempotente_na_mesma_conexao(self) -> None:
        # O re-hide do hotplug repete o hide a cada tick: 1 só operação de fs.
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        resposta = req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        assert resposta["ok"] is True and resposta["state"] == "hidden"
        assert ops.calls == [("hide", "/dev/hidraw3")]

    def test_hide_caminho_ruim(self) -> None:
        state, ops = make_state()
        for ruim in ("/dev/foo/../hidraw3", "/etc/passwd", "hidraw3", "", None, 7):
            resposta = req(state, 1, {"cmd": "hide", "node": ruim})
            assert resposta["ok"] is False and resposta["error"] == "reject_bad_path"
        assert ops.calls == []

    def test_hide_nao_fisico(self) -> None:
        # hidraw6 = vpad na convenção do validador fake: caminho ok, identidade não.
        state, ops = make_state()
        resposta = req(state, 1, {"cmd": "hide", "node": "/dev/hidraw6"})
        assert resposta["ok"] is False
        assert resposta["error"] == "reject_not_physical_dualsense"
        assert ops.calls == []

    def test_hide_falha_de_fs_nao_rastreia(self) -> None:
        state, ops = make_state(ops=FakeOps(fail_hide=True))
        resposta = req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        assert resposta["ok"] is False and resposta["error"] == "hide_failed"
        assert state.hidden == {} and ops.calls == []

    def test_restore_devolve_com_uid_do_hide(self) -> None:
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"}, uid=UID)
        resposta = req(state, 1, {"cmd": "restore", "node": "/dev/hidraw3"})
        assert resposta["state"] == "exposed"
        assert ("restore", "/dev/hidraw3", UID) in ops.calls
        assert state.hidden == {}

    def test_restore_nao_rastreado_valida_identidade(self) -> None:
        state, ops = make_state()
        ok = req(state, 1, {"cmd": "restore", "node": "/dev/hidraw7"})
        assert ok["ok"] is True and ok["state"] == "exposed"  # best-effort idempotente
        ruim = req(state, 1, {"cmd": "restore", "node": "/dev/hidraw6"})
        assert ruim["ok"] is False and ruim["error"] == "reject_not_physical_dualsense"
        assert ops.calls == [("restore", "/dev/hidraw7", UID)]

    def test_restore_node_sumiu_enoent(self) -> None:
        # Unplug: FileNotFoundError no restore NÃO é erro (estado "gone").
        state, _ = make_state(ops=FakeOps(fail_restore=FileNotFoundError()))
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        resposta = req(state, 1, {"cmd": "restore", "node": "/dev/hidraw3"})
        assert resposta["ok"] is True and resposta["state"] == "gone"
        assert state.hidden == {}

    def test_restore_all_da_conexao(self) -> None:
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw7"})
        resposta = req(state, 1, {"cmd": "restore_all"})
        assert resposta["ok"] is True
        assert resposta["restored"] == ["/dev/hidraw3", "/dev/hidraw7"]
        assert state.hidden == {}
        restores = [c for c in ops.calls if c[0] == "restore"]
        assert len(restores) == 2

    def test_comando_desconhecido(self) -> None:
        state, _ = make_state()
        resposta = req(state, 1, {"cmd": "format_disk"})
        assert resposta["ok"] is False and resposta["error"] == "reject_unknown_cmd"

    def test_malformado(self) -> None:
        state, _ = make_state()
        assert req(state, 1, b"{nao json")["error"] == "reject_malformed"
        assert req(state, 1, b"[1, 2]")["error"] == "reject_malformed"
        assert req(state, 1, b"\xff\xfe")["error"] == "reject_malformed"

    def test_oversize(self) -> None:
        state, _ = make_state()
        gigante = b'{"cmd": "hide", "node": "' + b"A" * MAX_LINE_BYTES + b'"}'
        assert req(state, 1, gigante)["error"] == "reject_oversize"


class TestLeaseRefcount:
    def test_eof_restaura_tudo_da_conexao(self) -> None:
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw7"})
        restaurados = state.on_conn_closed(1)
        assert restaurados == ["/dev/hidraw3", "/dev/hidraw7"]
        assert state.hidden == {} and state.by_conn == {}
        assert ("restore", "/dev/hidraw3", UID) in ops.calls
        assert ("restore", "/dev/hidraw7", UID) in ops.calls

    def test_refcount_duas_conexoes_takeover(self) -> None:
        # Takeover: daemon novo (conn 2) re-esconde o nó da lease velha (conn
        # 1). A morte da velha NÃO expõe; só a última lease restaura.
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        req(state, 2, {"cmd": "hide", "node": "/dev/hidraw3"})
        assert len([c for c in ops.calls if c[0] == "hide"]) == 1  # fs 1x
        assert state.on_conn_closed(1) == []  # conn 2 ainda segura
        assert "/dev/hidraw3" in state.hidden
        assert state.on_conn_closed(2) == ["/dev/hidraw3"]
        assert state.hidden == {}

    def test_restore_de_no_seguro_por_outra_conexao(self) -> None:
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        resposta = req(state, 2, {"cmd": "restore", "node": "/dev/hidraw3"})
        assert resposta["ok"] is True and resposta["state"] == "hidden"
        assert not any(c[0] == "restore" for c in ops.calls)

    def test_restore_everything_belt_do_shutdown(self) -> None:
        state, ops = make_state()
        req(state, 1, {"cmd": "hide", "node": "/dev/hidraw3"})
        req(state, 2, {"cmd": "hide", "node": "/dev/hidraw7"})
        assert state.restore_everything() == ["/dev/hidraw3", "/dev/hidraw7"]
        assert state.hidden == {} and state.by_conn == {}
        assert len([c for c in ops.calls if c[0] == "restore"]) == 2


class TestPeerCred:
    def test_socketpair_devolve_uid_real(self) -> None:
        # SO_PEERCRED funciona em socketpair: o peer somos nós mesmos.
        a, b = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            pid, uid, gid = peer_credentials(a)
            assert uid == os.getuid()
            assert gid == os.getgid()
            assert pid > 0
        finally:
            a.close()
            b.close()

    def test_broker_recusa_uid_errado(self) -> None:
        state, ops = make_state()
        state.allowed_uid = os.getuid() + 1  # ninguém local casa
        broker = Broker(state, None, log=lambda *a, **k: None)
        a, b = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            assert broker.register_client(a) is None
            # A ponta do "cliente" vê a conexão fechada sem NENHUMA resposta.
            b.settimeout(1.0)
            assert b.recv(64) == b""
            assert ops.calls == []
        finally:
            b.close()

    def test_broker_aceita_uid_da_sessao(self) -> None:
        state, _ = make_state()
        state.allowed_uid = os.getuid()
        broker = Broker(state, None, log=lambda *a, **k: None)
        a, b = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            assert broker.register_client(a) == 1
            b.settimeout(2.0)
            b.sendall(b'{"cmd": "ping"}\n')
            broker.step(timeout=2.0)
            resposta = json.loads(b.recv(4096).split(b"\n")[0])
            assert resposta["ok"] is True and resposta["peer_uid"] == os.getuid()
        finally:
            a.close()
            b.close()


class TestBrokerLoopEOF:
    def _wired(self) -> tuple[Broker, BrokerState, FakeOps, socket.socket]:
        state, ops = make_state()
        state.allowed_uid = os.getuid()
        broker = Broker(state, None, log=lambda *a, **k: None)
        a, b = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
        assert broker.register_client(a) is not None
        b.settimeout(2.0)
        return broker, state, ops, b

    def test_eof_do_daemon_restaura(self) -> None:
        # O CORAÇÃO do fail-safe: matar o "daemon" (fechar o socketpair)
        # restaura tudo que a lease escondeu — sem heartbeat.
        broker, state, ops, cliente = self._wired()
        cliente.sendall(b'{"cmd": "hide", "node": "/dev/hidraw3"}\n')
        broker.step(timeout=2.0)
        assert json.loads(cliente.recv(4096).split(b"\n")[0])["ok"] is True
        assert "/dev/hidraw3" in state.hidden
        cliente.close()  # SIGKILL do daemon = kernel fecha o fd = EOF
        broker.step(timeout=2.0)
        assert state.hidden == {}
        assert ("restore", "/dev/hidraw3", os.getuid()) in ops.calls

    def test_linha_gigante_fecha_e_restaura(self) -> None:
        broker, state, ops, cliente = self._wired()
        cliente.sendall(b'{"cmd": "hide", "node": "/dev/hidraw3"}\n')
        broker.step(timeout=2.0)
        cliente.recv(4096)
        cliente.sendall(b"A" * (MAX_LINE_BYTES * 2))  # sem newline
        # O recv do broker é de 4096 por evento: 2 steps acumulam > MAX_LINE.
        broker.step(timeout=2.0)
        broker.step(timeout=2.0)
        resposta = json.loads(cliente.recv(4096).split(b"\n")[0])
        assert resposta["error"] == "reject_oversize"
        # Conexão derrubada → lease restaurada (duplicado > zero).
        assert state.hidden == {}
        assert any(c[0] == "restore" for c in ops.calls)
        cliente.close()

    def test_duas_requisicoes_na_mesma_leitura(self) -> None:
        broker, _state, _ops, cliente = self._wired()
        cliente.sendall(b'{"cmd": "ping"}\n{"cmd": "status"}\n')
        broker.step(timeout=2.0)
        linhas = cliente.recv(8192).split(b"\n")
        respostas = [json.loads(linha) for linha in linhas if linha.strip()]
        assert [r["cmd"] for r in respostas] == ["ping", "status"]
        cliente.close()


class TestAclBlob:
    def test_roundtrip_do_blob(self) -> None:
        # O blob canônico validado ao vivo (setfacl -m u:1000:rw → 44 bytes).
        blob = encode_access_acl(1000)
        assert len(blob) == 44
        assert decode_acl_user_uids(blob) == {1000}

    def test_blob_identico_ao_do_setfacl_real(self) -> None:
        # Capturado com getxattr após `chmod 660` + `setfacl -m u:1000:rw` na
        # máquina de referência (2026-07-19) — byte a byte.
        esperado = bytes.fromhex(
            "0200000001000600ffffffff02000600e8030000"
            "04000600ffffffff10000600ffffffff20000000ffffffff"
        )
        assert encode_access_acl(1000) == esperado

    def test_decode_rejeita_versao_errada(self) -> None:
        assert decode_acl_user_uids(b"\x01\x00\x00\x00") == set()
        assert decode_acl_user_uids(b"") == set()


class TestRestoreAllPhysical:
    def test_baseline_restaura_so_fisico_nao_exposto(self, tmp_path: Any) -> None:
        # Varredura do --restore-all-and-exit com sysfs fake: só o físico
        # não-exposto é restaurado; o vpad e o já-exposto ficam quietos.
        sys_hidraw = tmp_path / "sys"
        for base in ("hidraw3", "hidraw6", "hidraw7"):
            (sys_hidraw / base).mkdir(parents=True)

        class Ops(FakeOps):
            def is_exposed_to(self, node: str, uid: int) -> bool:
                return node.endswith("hidraw7")  # o 7 já está exposto

        ops = Ops()
        restaurados = restore_all_physical(
            uid=UID,
            ops=ops,
            dev_root="/dev",
            sys_class_hidraw=str(sys_hidraw),
            validator=_validator,  # aceita 3 e 7; rejeita o "vpad" 6
            log=lambda *a, **k: None,
        )
        assert restaurados == ["/dev/hidraw3"]
        assert ops.calls == [("restore", "/dev/hidraw3", UID)]
