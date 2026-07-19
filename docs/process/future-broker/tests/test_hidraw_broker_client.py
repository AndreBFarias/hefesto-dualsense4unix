"""Cliente-lease do broker (BROKER-01) — ponta a ponta num socket unix REAL.

O servidor é o Broker de verdade (thread própria) com fs FAKE e validador
injetado — nenhum /dev real é tocado. Prova:
- hide/restore/restore_all/status/ping viajam pelo protocolo JSON-por-linha;
- a conexão é UMA e longeva (a lease): fechar o cliente restaura no servidor;
- broker AUSENTE = best-effort silencioso (False, nunca exceção) — a regra
  sagrada "duplicado > zero controles";
- `broker_client_for` respeita o dublê injetado no daemon e cacheia o real.
"""
from __future__ import annotations

import contextlib
import os
import socket
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

import pytest

from hefesto_dualsense4unix.broker.hidraw_broker import Broker, BrokerState
from hefesto_dualsense4unix.integrations import hidraw_broker_client as hbc


class FakeOps:
    def __init__(self) -> None:
        self.calls: list[tuple[Any, ...]] = []

    def hide(self, node: str) -> None:
        self.calls.append(("hide", node))

    def restore(self, node: str, uid: int) -> None:
        self.calls.append(("restore", node, uid))

    def is_exposed_to(self, node: str, uid: int) -> bool:
        return True


def _validator(node: str) -> str | None:
    base = node.rsplit("/", 1)[-1]
    return base if base in {"hidraw3", "hidraw7"} else None


def _short_socket_dir(tmp_path: Path) -> str:
    """Diretório curto para o socket: sun_path tem limite de ~108 bytes.

    O tmp_path do pytest pode morar num TMPDIR profundo (o scratchpad desta
    máquina passa de 100 chars) — nesse caso caímos num mkdtemp direto em
    /tmp, limpo pelo próprio teste.
    """
    candidato = tmp_path / "bk"
    if len(str(candidato / "broker.sock")) <= 90:
        candidato.mkdir(exist_ok=True)
        return str(candidato)
    return tempfile.mkdtemp(prefix="hefesto-bk-", dir="/tmp")


@pytest.fixture()
def live_broker(tmp_path: Path):
    """Broker real numa thread + socket unix real; fs é o FakeOps."""
    sockdir = _short_socket_dir(tmp_path)
    path = os.path.join(sockdir, "broker.sock")
    listen = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    listen.bind(path)
    listen.listen(4)
    ops = FakeOps()
    state = BrokerState(
        allowed_uid=os.getuid(), ops=ops, validator=_validator, log=lambda *a, **k: None
    )
    broker = Broker(state, listen, log=lambda *a, **k: None)
    thread = threading.Thread(target=broker.run, daemon=True)
    thread.start()
    try:
        yield path, state, ops
    finally:
        broker.stopping = True
        # Acorda o selector (senão o run espera o timeout de 1s inteiro).
        with (
            socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as poke,
            contextlib.suppress(OSError),
        ):
            poke.connect(path)
        thread.join(timeout=3.0)
        listen.close()
        if os.path.exists(path):
            os.unlink(path)
        if sockdir.startswith("/tmp/hefesto-bk-"):
            os.rmdir(sockdir)


def _espera(cond, timeout: float = 2.0) -> bool:
    fim = time.monotonic() + timeout
    while time.monotonic() < fim:
        if cond():
            return True
        time.sleep(0.01)
    return False


class TestClienteVivo:
    def test_hide_e_status(self, live_broker: Any) -> None:
        path, _state, ops = live_broker
        cliente = hbc.HidrawBrokerClient(path)
        try:
            assert cliente.ping() is True
            assert cliente.hide("/dev/hidraw3") is True
            assert ("hide", "/dev/hidraw3") in ops.calls
            status = cliente.status()
            assert status is not None and status["hidden"] == ["/dev/hidraw3"]
        finally:
            cliente.close()

    def test_hide_recusado_para_nao_fisico(self, live_broker: Any) -> None:
        path, _state, ops = live_broker
        cliente = hbc.HidrawBrokerClient(path)
        try:
            assert cliente.hide("/dev/hidraw6") is False  # "vpad" do validador
            assert ops.calls == []
        finally:
            cliente.close()

    def test_restore_e_restore_all(self, live_broker: Any) -> None:
        path, state, ops = live_broker
        cliente = hbc.HidrawBrokerClient(path)
        try:
            cliente.hide("/dev/hidraw3")
            cliente.hide("/dev/hidraw7")
            assert cliente.restore("/dev/hidraw3") is True
            assert cliente.restore_all() is True
            assert state.hidden == {}
            assert len([c for c in ops.calls if c[0] == "restore"]) == 2
        finally:
            cliente.close()

    def test_close_da_lease_restaura_no_servidor(self, live_broker: Any) -> None:
        # O fail-safe visto do lado do cliente: fechar a lease (= daemon
        # morrendo) restaura tudo sem nenhum comando extra.
        path, state, ops = live_broker
        cliente = hbc.HidrawBrokerClient(path)
        cliente.hide("/dev/hidraw3")
        assert "/dev/hidraw3" in state.hidden
        cliente.close()
        assert _espera(lambda: state.hidden == {})
        assert ("restore", "/dev/hidraw3", os.getuid()) in ops.calls

    def test_conexao_unica_e_longeva(self, live_broker: Any) -> None:
        path, state, _ops = live_broker
        cliente = hbc.HidrawBrokerClient(path)
        try:
            cliente.ping()
            cliente.hide("/dev/hidraw3")
            cliente.status()
            # UMA lease só: o estado por-conexão do servidor tem 1 entrada.
            assert _espera(lambda: len(state.by_conn) == 1)
        finally:
            cliente.close()


class TestClienteSemBroker:
    def test_tudo_best_effort_sem_excecao(self, tmp_path: Path) -> None:
        cliente = hbc.HidrawBrokerClient(str(tmp_path / "nao-existe.sock"))
        assert cliente.is_available() is False
        assert cliente.hide("/dev/hidraw3") is False
        assert cliente.restore("/dev/hidraw3") is False
        assert cliente.restore_all() is False
        assert cliente.ping() is False
        assert cliente.status() is None
        cliente.close()  # idempotente

    def test_default_honra_env_de_isolamento(self, tmp_path: Path) -> None:
        # O conftest aponta HEFESTO_BROKER_SOCKET para um caminho inexistente:
        # o cliente DEFAULT nunca alcança o broker real da máquina.
        cliente = hbc.HidrawBrokerClient()
        assert cliente._path == os.environ["HEFESTO_BROKER_SOCKET"]
        assert cliente.is_available() is False


class TestBrokerClientFor:
    def test_respeita_duble_injetado(self) -> None:
        class Daemon:
            _hidraw_broker_client = "fake-injetado"

        assert hbc.broker_client_for(Daemon()) == "fake-injetado"

    def test_cria_e_cacheia_no_daemon(self) -> None:
        class Daemon:
            _hidraw_broker_client: Any = None

        daemon = Daemon()
        cliente = hbc.broker_client_for(daemon)
        assert isinstance(cliente, hbc.HidrawBrokerClient)
        assert daemon._hidraw_broker_client is cliente
        assert hbc.broker_client_for(daemon) is cliente
