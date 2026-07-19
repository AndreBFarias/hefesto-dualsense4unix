"""Cliente do broker root hide-hidraw (BROKER-01) — a conexão É a lease.

O daemon abre UMA conexão longeva ao socket do broker
(`/run/hefesto-hidraw-broker/broker.sock`) e a mantém pela vida do processo.
Se o daemon morrer por QUALQUER via (crash, SIGKILL, OOM, takeover), o kernel
fecha o fd → o broker vê EOF → restaura todo hidraw que ESTA lease escondeu.
Por isso o cliente NUNCA fecha a conexão entre chamadas.

Contrato best-effort sagrado ("duplicado > zero controles"): broker ausente,
socket recusado, timeout — NADA levanta para o chamador; `hide`/`restore`
devolvem False e o daemon segue sem esconder (o comportamento de hoje).
Protocolo JSON-por-linha, o mesmo do IPC do daemon (spec §3 do estudo
2026-07-18-estudo-broker-hide-hidraw.md).
"""
from __future__ import annotations

import contextlib
import json
import os
import socket
import threading
from typing import Any

from hefesto_dualsense4unix.utils.logging_config import get_logger

logger = get_logger(__name__)

#: Onde o systemd (hefesto-hidraw-broker.socket) escuta.
DEFAULT_SOCKET_PATH = "/run/hefesto-hidraw-broker/broker.sock"
#: Override do socket (testes/debug). A suíte hermética APONTA isto para um
#: caminho inexistente (conftest) — na máquina da mantenedora o broker REAL
#: está de pé e um teste que resolvesse o default esconderia hidraw de verdade.
SOCKET_PATH_ENV = "HEFESTO_BROKER_SOCKET"
#: Timeout por operação — o hide roda no caminho do start da emulação; um
#: broker travado não pode congelar o daemon.
_TIMEOUT_S = 2.0
#: Resposta maior que isto é lixo — corta e derruba a conexão.
_MAX_RESPONSE_BYTES = 65536


class HidrawBrokerClient:
    """Conexão-lease com o broker + comandos hide/restore/restore_all/status.

    Thread-safe (lock único): os hooks chamam do executor do daemon e do event
    loop. Reconexão lazy com UMA retentativa por chamada — se o broker
    reiniciou (a lease velha morreu, e com ela o estado escondido foi
    restaurado pelo próprio broker), a chamada seguinte abre lease nova.
    """

    def __init__(
        self, socket_path: str | None = None, *, timeout_s: float = _TIMEOUT_S
    ) -> None:
        self._path = (
            socket_path
            if socket_path is not None
            else os.environ.get(SOCKET_PATH_ENV, DEFAULT_SOCKET_PATH)
        )
        self._timeout_s = timeout_s
        self._lock = threading.Lock()
        self._sock: socket.socket | None = None
        self._indisponivel_logado = False

    # -- API pública -----------------------------------------------------

    def hide(self, node: str) -> bool:
        """Esconde `node` do uid da sessão. False = não escondeu (best-effort)."""
        response = self._request({"cmd": "hide", "node": node})
        ok = bool(response is not None and response.get("ok"))
        if ok:
            logger.info("hidraw_broker_hidden", node=node)
        else:
            self._log_falha("hide", node, response)
        return ok

    def restore(self, node: str) -> bool:
        """Restaura o acesso a `node`. False = broker indisponível/erro."""
        response = self._request({"cmd": "restore", "node": node})
        ok = bool(response is not None and response.get("ok"))
        if ok:
            logger.info(
                "hidraw_broker_restored",
                node=node,
                state=response.get("state") if response else None,
            )
        else:
            self._log_falha("restore", node, response)
        return ok

    def restore_all(self) -> bool:
        """Restaura TUDO que esta lease escondeu (teardown/Modo Nativo)."""
        response = self._request({"cmd": "restore_all"})
        ok = bool(response is not None and response.get("ok"))
        if ok:
            logger.info(
                "hidraw_broker_restored_all",
                nodes=response.get("restored") if response else None,
            )
        else:
            self._log_falha("restore_all", None, response)
        return ok

    def status(self) -> dict[str, Any] | None:
        """Resposta crua do `status` (nós escondidos) — para doctor/telemetria."""
        return self._request({"cmd": "status"})

    def ping(self) -> bool:
        response = self._request({"cmd": "ping"})
        return bool(response is not None and response.get("ok"))

    def is_available(self) -> bool:
        """True se o socket existe E o broker responde (abre a lease)."""
        if not os.path.exists(self._path):
            return False
        return self.ping()

    def close(self) -> None:
        """Fecha a lease explicitamente (o broker restaura o que restou)."""
        with self._lock:
            self._close_locked()

    # -- interno ---------------------------------------------------------

    def _request(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        line = (json.dumps(payload) + "\n").encode("utf-8")
        with self._lock:
            for tentativa in (1, 2):
                sock = self._ensure_sock_locked()
                if sock is None:
                    return None
                try:
                    sock.sendall(line)
                    raw = self._read_line_locked(sock)
                    break
                except OSError:
                    # Lease morta (broker reiniciou?): derruba e tenta UMA vez.
                    self._close_locked()
                    if tentativa == 2:
                        return None
            else:  # pragma: no cover - inalcançável (o for sempre break/return)
                return None
        try:
            response = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return None
        return response if isinstance(response, dict) else None

    def _ensure_sock_locked(self) -> socket.socket | None:
        if self._sock is not None:
            return self._sock
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self._timeout_s)
        try:
            sock.connect(self._path)
        except OSError as exc:
            sock.close()
            if not self._indisponivel_logado:
                # Uma vez por vida do cliente: broker ausente é degradação
                # esperada (install antigo/CI) — o resto vai em DEBUG.
                logger.info("hidraw_broker_unavailable", path=self._path, err=str(exc))
                self._indisponivel_logado = True
            else:
                logger.debug("hidraw_broker_connect_failed", err=str(exc))
            return None
        self._sock = sock
        self._indisponivel_logado = False
        logger.info("hidraw_broker_lease_open", path=self._path)
        return sock

    def _read_line_locked(self, sock: socket.socket) -> bytes:
        chunks = bytearray()
        while b"\n" not in chunks:
            if len(chunks) > _MAX_RESPONSE_BYTES:
                raise OSError("resposta do broker sem fim de linha")
            data = sock.recv(4096)
            if not data:
                raise OSError("broker fechou a conexão")
            chunks.extend(data)
        return bytes(chunks[: chunks.find(b"\n")])

    def _close_locked(self) -> None:
        if self._sock is not None:
            with contextlib.suppress(OSError):
                self._sock.close()
            self._sock = None

    def _log_falha(
        self, cmd: str, node: str | None, response: dict[str, Any] | None
    ) -> None:
        # DEBUG de propósito: com o broker ausente TODO grab logaria — o
        # rastro visível é o `hidraw_broker_unavailable` único da conexão.
        logger.debug(
            "hidraw_broker_cmd_failed",
            cmd=cmd,
            node=node,
            error=(response or {}).get("error"),
        )


def broker_client_for(daemon: Any) -> Any:
    """Cliente-lease singleton por daemon (lazy) — dublês de teste passam direto.

    O cliente vive em `daemon._hidraw_broker_client`; testes injetam um fake ali
    e ele é respeitado. Nunca levanta: daemon sem o atributo gravável devolve o
    cliente sem cachear (funciona, só não reusa a lease — caso teórico).
    """
    client = getattr(daemon, "_hidraw_broker_client", None)
    if client is not None:
        return client
    client = HidrawBrokerClient()
    # Daemon exótico sem atributo gravável funciona igual (só não reusa a lease).
    with contextlib.suppress(AttributeError, TypeError):
        daemon._hidraw_broker_client = client
    return client


__all__ = [
    "DEFAULT_SOCKET_PATH",
    "HidrawBrokerClient",
    "broker_client_for",
]
