"""Hooks do broker hide-hidraw no daemon (BROKER-01) — gating hermético.

A política mora no daemon; o broker é burro. Prova, sem broker real (dublê
injetado em `daemon._hidraw_broker_client`, que `broker_client_for` respeita):
- hide colado no grab: `start_gamepad_emulation` esconde o hidraw do primário;
- Modo Nativo NUNCA esconde (o jogo é dono do hidraw);
- restore no release do grab: `stop_gamepad_emulation` com `release_grab=True`
  restaura TUDO; com `release_grab=False` (troca de flavor) NÃO restaura;
- backend sem `hidraw_path` (FakeController do smoke) não fala com o broker;
- broker quebrado jamais derruba a emulação (best-effort sagrado);
- re-hide do hotplug (`rehide_physical_hidraw`): primário + jogadores de
  co-op com vpad vivo, com todos os gates (emulação/vpad/nativo);
- co-op: promote esconde o físico do jogador; teardown restaura.
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from hefesto_dualsense4unix.core import physical_report_reader as prr
from hefesto_dualsense4unix.daemon.lifecycle import DaemonConfig
from hefesto_dualsense4unix.daemon.subsystems import gamepad as gp
from hefesto_dualsense4unix.integrations import virtual_pad as vp
from hefesto_dualsense4unix.utils import session


class FakeBroker:
    """Dublê do HidrawBrokerClient: grava chamadas; pode explodir."""

    def __init__(self, *, explode: bool = False) -> None:
        self.calls: list[tuple[Any, ...]] = []
        self.explode = explode

    def hide(self, node: str) -> bool:
        if self.explode:
            raise OSError("broker fora do ar")
        self.calls.append(("hide", node))
        return True

    def restore(self, node: str) -> bool:
        if self.explode:
            raise OSError("broker fora do ar")
        self.calls.append(("restore", node))
        return True

    def restore_all(self) -> bool:
        if self.explode:
            raise OSError("broker fora do ar")
        self.calls.append(("restore_all",))
        return True

    def close(self) -> None:
        self.calls.append(("close",))


class _FakeReader:
    def __init__(self, path_provider: Any, vpad: Any, **_kw: Any) -> None:
        self.path_provider = path_provider

    def start(self) -> bool:
        return True

    def stop(self) -> None: ...


class _FakeVpad:
    def __init__(self, backend: str = "uhid") -> None:
        self.flavor = "dualsense"
        self.backend = backend

    def stop(self) -> None: ...

    def forward_analog(self, **_kw: int) -> None: ...

    def forward_buttons(self, _p: frozenset[str]) -> None: ...

    def pump_ff(self) -> None: ...


class _FakeController:
    def __init__(self, nodes: dict[str | None, str | None] | None = None) -> None:
        self._evdev = SimpleNamespace(set_grab=lambda _g: True, grab_state="held")
        #: uniq (None = primário) → nó hidraw
        self.nodes = nodes if nodes is not None else {None: "/dev/hidraw3"}

    def hidraw_path(self, uniq: str | None = None) -> str | None:
        return self.nodes.get(uniq)

    def read_calibration(self, uniq: str | None = None) -> bytes | None:
        return None

    def attach_motion_reader(self, reader: Any | None) -> None: ...


class _FakeDaemon:
    def __init__(self, *, native: bool = False) -> None:
        self._gamepad_device = None
        self._motion_reader = None
        self._mouse_device = None
        self._coop_manager = None
        self._hidraw_broker_client = FakeBroker()
        self.config = DaemonConfig()
        self.controller = _FakeController()
        self._native = native

    def is_native_mode(self) -> bool:
        return self._native

    @property
    def broker(self) -> FakeBroker:
        client = self._hidraw_broker_client
        assert isinstance(client, FakeBroker)
        return client


@pytest.fixture()
def wired(monkeypatch: pytest.MonkeyPatch) -> _FakeDaemon:
    monkeypatch.setattr(session, "save_gamepad_emulation", lambda *a, **k: None)
    monkeypatch.setattr(session, "save_mouse_emulation_enabled", lambda *a, **k: None)
    monkeypatch.setattr(prr, "PhysicalReportReader", _FakeReader)
    monkeypatch.setattr(vp, "make_virtual_pad", lambda *_a, **_k: _FakeVpad())
    return _FakeDaemon()


class TestGrabP1:
    def test_start_esconde_o_primario(self, wired: _FakeDaemon) -> None:
        assert gp.start_gamepad_emulation(wired, flavor="dualsense") is True
        assert ("hide", "/dev/hidraw3") in wired.broker.calls

    def test_nativo_nunca_esconde(self, wired: _FakeDaemon) -> None:
        wired._native = True
        gp.start_gamepad_emulation(wired, flavor="dualsense")
        assert not any(c[0] == "hide" for c in wired.broker.calls)

    def test_stop_com_release_restaura_tudo(self, wired: _FakeDaemon) -> None:
        gp.start_gamepad_emulation(wired, flavor="dualsense")
        gp.stop_gamepad_emulation(wired)  # release_grab default True
        assert ("restore_all",) in wired.broker.calls

    def test_troca_de_flavor_nao_restaura(self, wired: _FakeDaemon) -> None:
        # release_grab=False (recriação imediata): expor o físico no meio da
        # troca abriria a janela do duplicado — o gate do grab cobre de graça.
        gp.start_gamepad_emulation(wired, flavor="dualsense")
        wired.broker.calls.clear()
        gp.stop_gamepad_emulation(wired, persist=False, release_grab=False)
        assert ("restore_all",) not in wired.broker.calls

    def test_backend_sem_hidraw_nao_fala_com_broker(self, wired: _FakeDaemon) -> None:
        # FakeController do smoke: sem `hidraw_path` (o gate do VPAD-08).
        wired.controller = SimpleNamespace(
            _evdev=SimpleNamespace(set_grab=lambda _g: True, grab_state="held")
        )
        gp.start_gamepad_emulation(wired, flavor="dualsense")
        gp.stop_gamepad_emulation(wired)
        assert wired.broker.calls == []

    def test_primario_sem_no_nao_pede_hide(self, wired: _FakeDaemon) -> None:
        # Offline no boot: hidraw_path() → None; o re-hide do hotplug cobre.
        wired.controller.nodes[None] = None
        gp.start_gamepad_emulation(wired, flavor="dualsense")
        assert not any(c[0] == "hide" for c in wired.broker.calls)

    def test_broker_explodindo_nao_derruba_emulacao(self, wired: _FakeDaemon) -> None:
        # A regra sagrada: duplicado > zero controles.
        wired._hidraw_broker_client = FakeBroker(explode=True)
        assert gp.start_gamepad_emulation(wired, flavor="dualsense") is True
        gp.stop_gamepad_emulation(wired)  # também não levanta
        assert wired.config.gamepad_emulation_enabled is False


class TestRehideHotplug:
    def _daemon_ativo(self, wired: _FakeDaemon) -> _FakeDaemon:
        wired.config.gamepad_emulation_enabled = True
        wired._gamepad_device = _FakeVpad()
        return wired

    def test_rehide_primario(self, wired: _FakeDaemon) -> None:
        daemon = self._daemon_ativo(wired)
        gp.rehide_physical_hidraw(daemon)
        assert daemon.broker.calls == [("hide", "/dev/hidraw3")]

    def test_rehide_cobre_jogadores_do_coop(self, wired: _FakeDaemon) -> None:
        daemon = self._daemon_ativo(wired)
        daemon.controller.nodes["aabbccddee02"] = "/dev/hidraw7"
        daemon.controller.nodes["aabbccddee03"] = None  # externo sem handle
        daemon._coop_manager = SimpleNamespace(
            _players={
                "aabbccddee02": SimpleNamespace(vpad=_FakeVpad()),
                "aabbccddee03": SimpleNamespace(vpad=_FakeVpad()),
                "path:/dev/input/event9": SimpleNamespace(vpad=_FakeVpad()),
                "aabbccddee04": SimpleNamespace(vpad=None),  # sem vpad vivo
            }
        )
        gp.rehide_physical_hidraw(daemon)
        assert ("hide", "/dev/hidraw3") in daemon.broker.calls
        assert ("hide", "/dev/hidraw7") in daemon.broker.calls
        assert len([c for c in daemon.broker.calls if c[0] == "hide"]) == 2

    def test_gates_emulacao_vpad_nativo(self, wired: _FakeDaemon) -> None:
        # Emulação desligada → nada.
        gp.rehide_physical_hidraw(wired)
        assert wired.broker.calls == []
        # Emulação ligada mas SEM vpad vivo → nada (regra de ouro).
        wired.config.gamepad_emulation_enabled = True
        gp.rehide_physical_hidraw(wired)
        assert wired.broker.calls == []
        # Nativo → nada.
        wired._gamepad_device = _FakeVpad()
        wired._native = True
        gp.rehide_physical_hidraw(wired)
        assert wired.broker.calls == []

    def test_no_duplicado_nao_repete_hide(self, wired: _FakeDaemon) -> None:
        # Primário e jogador no MESMO nó (não deve acontecer, mas dedup barato).
        daemon = self._daemon_ativo(wired)
        daemon.controller.nodes["aabbccddee02"] = "/dev/hidraw3"
        daemon._coop_manager = SimpleNamespace(
            _players={"aabbccddee02": SimpleNamespace(vpad=_FakeVpad())}
        )
        gp.rehide_physical_hidraw(daemon)
        assert daemon.broker.calls == [("hide", "/dev/hidraw3")]


class TestCoopHooks:
    def _manager(self, daemon: _FakeDaemon) -> Any:
        from hefesto_dualsense4unix.daemon.subsystems.coop import CoopManager

        return CoopManager(daemon)

    def test_hide_do_jogador(self, wired: _FakeDaemon) -> None:
        wired.controller.nodes["aabbccddee02"] = "/dev/hidraw7"
        manager = self._manager(wired)
        manager._broker_hide_player("aabbccddee02")
        assert wired.broker.calls == [("hide", "/dev/hidraw7")]

    def test_externo_e_sem_mac_ficam_expostos(self, wired: _FakeDaemon) -> None:
        manager = self._manager(wired)
        manager._broker_hide_player("aabbccddee99")  # sem handle → None
        manager._broker_hide_player("path:/dev/input/event9")
        assert wired.broker.calls == []

    def test_teardown_restaura_o_jogador(self, wired: _FakeDaemon) -> None:
        from hefesto_dualsense4unix.daemon.subsystems.coop import _SecondaryPlayer

        wired.controller.nodes["aabbccddee02"] = "/dev/hidraw7"
        manager = self._manager(wired)
        reader = SimpleNamespace(
            set_grab=lambda _g: True, stop=lambda: None, grab_state="held"
        )
        player = _SecondaryPlayer(
            identity="aabbccddee02",
            evdev_path="/dev/input/event99",
            reader=reader,
            player_index=2,
            vpad=_FakeVpad(),
        )
        manager._players[player.identity] = player
        manager._teardown_player(player.identity)
        assert ("restore", "/dev/hidraw7") in wired.broker.calls

    def test_promote_esconde_o_fisico_do_jogador(
        self, wired: _FakeDaemon, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from hefesto_dualsense4unix.daemon.subsystems.coop import _SecondaryPlayer

        wired.controller.nodes["aabbccddee02"] = "/dev/hidraw7"
        manager = self._manager(wired)
        reader = SimpleNamespace(
            set_grab=lambda _g: True, stop=lambda: None, grab_state="held"
        )
        player = _SecondaryPlayer(
            identity="aabbccddee02",
            evdev_path="/dev/input/event99",
            reader=reader,
            player_index=2,
        )
        manager._players[player.identity] = player
        manager._promote_player(player)
        assert player.vpad is not None
        assert ("hide", "/dev/hidraw7") in wired.broker.calls


class TestShutdownFechaLease:
    def test_shutdown_close(self, wired: _FakeDaemon) -> None:
        import asyncio

        from hefesto_dualsense4unix.daemon import connection

        daemon = wired
        # Superfície mínima que o shutdown() toca.
        daemon._plugins_subsystem = None
        daemon._hotkey_manager = None
        daemon._audio = None
        daemon._keyboard_device = None
        daemon._ipc_server = None
        daemon._udp_server = None
        daemon._autoswitch = None
        daemon._last_state = None
        daemon._tasks = []
        daemon._reconnect_task = None
        daemon._executor = None
        daemon.controller.disconnect = lambda: None  # type: ignore[attr-defined]

        async def _run_blocking(fn: Any) -> Any:
            return fn()

        daemon._run_blocking = _run_blocking  # type: ignore[attr-defined]
        broker = daemon.broker
        asyncio.run(connection.shutdown(daemon))
        assert ("close",) in broker.calls
        assert daemon._hidraw_broker_client is None
