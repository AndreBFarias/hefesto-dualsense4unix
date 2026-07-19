# Broker root hide-hidraw (BROKER-01) — PARKADO para onda dedicada

**Estado: artefato de onda FUTURA. Nada aqui é buildado, instalado, lintado ou testado.**

Este diretório preserva, como referência, o trabalho do broker root hide-hidraw retirado
da árvore ativa em 2026-07-19 (leva `sprint/harmonia-uhid`). A decisão de parkar veio da
auditoria da leva final: o broker, como estava, **colide com o motion** (GYRO-01) — o hide
`chmod 0600 root:root` impede o `PhysicalReportReader` de reabrir o hidraw do físico
(EACCES em loop: silêncio de 1s, retarget de primário, reconexão BT, corrida no
nascimento) — e a robustez do próprio broker foi julgada insuficiente para produção
(hide de nó já rastreado é no-op, restore falho orfaniza o nó, lease derrubada em
timeout restaura tudo e re-esconde só um, `RuntimeDirectory=` no service apaga o
socket, TOCTOU de minor reciclado). Detalhe: achados 1–5, 8–10 e 13–14 do relatório da
auditoria (21 CONFIRMADOS) e o estudo
`docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md`.

A onda futura deve retomar daqui **junto** com o desenho do caminho de abertura
privilegiada para o motion reader (cmd `open` + passagem de fd via SCM_RIGHTS foi a
direção verificada pela auditoria — nunca restore→open→re-hide, que abre janela de
exposição para SDL/winebus).

## Conteúdo (paths originais na árvore ativa)

| Aqui | Era |
| --- | --- |
| `broker/hidraw_broker.py` + `broker/__init__.py` | `src/hefesto_dualsense4unix/broker/` |
| `integrations/hidraw_broker_client.py` | `src/hefesto_dualsense4unix/integrations/hidraw_broker_client.py` |
| `systemd/hefesto-hidraw-broker.service` / `.socket` | `assets/systemd/` |
| `tests/test_hidraw_broker_*.py` (5 arquivos, ~87 testes) | `tests/unit/` |

## Fiação removida da árvore ativa (reconstruir na onda futura)

- `daemon/subsystems/gamepad.py`: `_broker_sync_grab` (hide/restore colado ao
  EVIOCGRAB em `_set_controller_grab`) + `rehide_physical_hidraw` (reconciliação de
  hotplug) + export no `__all__`.
- `daemon/subsystems/coop.py`: `_player_hidraw_node` + `_broker_hide_player`
  (pós-promoção, vpad confirmado) + `_broker_restore_player` (no `_teardown_player`).
- `daemon/connection.py`: re-hide a cada reconciliação online do `reconnect_loop` +
  close explícito da lease no `shutdown`.
- `daemon/protocols.py` / `daemon/lifecycle.py`: campo `_hidraw_broker_client`.
- `tests/conftest.py`: isolamento `HEFESTO_BROKER_SOCKET` → socket inexistente.
- `install.sh` (step 3f), `uninstall.sh` (remoção simétrica + `_NEEDS_SUDO`),
  `scripts/doctor.sh` (`check_hidraw_broker`), `scripts/install-host-udev.sh`
  (paridade deb/flatpak), `scripts/build_deb.sh`, `packaging/arch/PKGBUILD`,
  `packaging/fedora/*.spec` (%install + %files), `flatpak/*.yml`,
  `scripts/check_packaging_parity.sh` (seção de paridade do broker) e
  `tests/unit/test_check_packaging_parity.py` (`_seed_broker_parity`).

O motion (GYRO-01: `core/physical_report_reader.py`, espelho por jogador no co-op,
telemetria `motion_streaming`/`motion_hz`, `check_vpad_motion` do doctor) **ficou na
árvore ativa** — o broker é que saiu.
