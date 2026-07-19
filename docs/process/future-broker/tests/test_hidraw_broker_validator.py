"""Validador do broker hide-hidraw (BROKER-01, spec §4) — hermético.

Prova, com árvore sysfs/dev FAKE (nunca /dev real):
- aceita SÓ DualSense físico 054c:0ce6, nos DOIS transportes (USB 0003 e BT
  0005), com o `HID_ID` no formato ZERO-PREENCHIDO real do kernel
  (`0003:0000054C:00000CE6` — verificado ao vivo);
- rejeita o vpad 0df2 (o nó por onde o jogo fala com o controle), Nintendo/
  8BitDo 057e:2009, bus desconhecido, `/devices/virtual/` (uhid forjado);
- rejeita caminho não-canônico (`..`, barras extras, basename não-hidrawN),
  symlink plantado e (major,minor) divergente do sysfs.

Char device não dá para criar sem root — `stat_fn` é injetado com um stat
falso S_IFCHR (o validador aceita o injetável exatamente para isso).
"""
from __future__ import annotations

import os
import stat
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from hefesto_dualsense4unix.broker.hidraw_broker import (
    canonical_hidraw_base,
    validate_physical_node,
)

#: HID_IDs REAIS coletados na máquina de referência (2026-07-18, read-only).
HID_ID_USB = "HID_ID=0003:0000054C:00000CE6"
HID_ID_BT = "HID_ID=0005:0000054C:00000CE6"
HID_ID_VPAD = "HID_ID=0003:0000054C:00000DF2"
HID_ID_NINTENDO = "HID_ID=0003:0000057E:00002009"

_RDEV = os.makedev(237, 3)


def _chr_stat(rdev: int = _RDEV) -> Any:
    """stat falso de char device (S_IFCHR) — o que os testes não podem criar."""
    return SimpleNamespace(st_mode=stat.S_IFCHR | 0o660, st_rdev=rdev)


def _make_tree(
    tmp_path: Path,
    *,
    base: str = "hidraw3",
    hid_id: str = HID_ID_USB,
    dev: str = "237:3",
    virtual: bool = False,
    uevent: str | None = None,
) -> tuple[str, dict[str, str]]:
    """Monta dev/ + sys/class/hidraw/<base>/ fake; devolve (node, kwargs)."""
    dev_root = tmp_path / "dev"
    dev_root.mkdir(exist_ok=True)
    node = dev_root / base
    node.touch()
    sys_hidraw = tmp_path / "sys" / "class" / "hidraw"
    entry = sys_hidraw / base
    entry.mkdir(parents=True, exist_ok=True)
    (entry / "dev").write_text(dev + "\n", encoding="ascii")
    if virtual:
        # uhid forjado: o pai HID mora em /devices/virtual/ (symlink real,
        # resolvido pelo realpath do validador).
        target = tmp_path / "sys" / "devices" / "virtual" / "misc" / "uhid" / "0003:054C:0CE6.000B"
        target.mkdir(parents=True, exist_ok=True)
        (entry / "device").symlink_to(target)
    else:
        (entry / "device").mkdir(exist_ok=True)
    conteudo = (
        uevent
        if uevent is not None
        else f"DRIVER=playstation\n{hid_id}\nHID_NAME=DualSense Wireless Controller\n"
    )
    (entry / "device" / "uevent").write_text(conteudo, encoding="ascii")
    kwargs = {"dev_root": str(dev_root), "sys_class_hidraw": str(sys_hidraw)}
    return str(node), kwargs


class TestCanonicalBase:
    def test_aceita_caminho_literal(self) -> None:
        assert canonical_hidraw_base("/dev/hidraw3") == "hidraw3"
        assert canonical_hidraw_base("/dev/hidraw13") == "hidraw13"

    def test_rejeita_traversal_e_lixo(self) -> None:
        assert canonical_hidraw_base("/dev/foo/../hidraw3") is None
        assert canonical_hidraw_base("/dev/../dev/hidraw3") is None
        assert canonical_hidraw_base("//dev/hidraw3") is None
        assert canonical_hidraw_base("/dev/hidraw") is None
        assert canonical_hidraw_base("/dev/hidrawX") is None
        assert canonical_hidraw_base("/dev/tty0") is None
        assert canonical_hidraw_base("/dev/hidraw3 ") is None
        assert canonical_hidraw_base("") is None
        assert canonical_hidraw_base(None) is None
        assert canonical_hidraw_base(3) is None

    def test_dev_root_injetavel(self) -> None:
        assert canonical_hidraw_base("/x/hidraw1", dev_root="/x") == "hidraw1"
        assert canonical_hidraw_base("/dev/hidraw1", dev_root="/x") is None


class TestValidateAceita:
    def test_dualsense_usb(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path, hid_id=HID_ID_USB)
        assert (
            validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs)
            == "hidraw3"
        )

    def test_dualsense_bt(self, tmp_path: Path) -> None:
        # BT: o pai HID é 0005:...:0CE6 — o bus muda, a identidade não.
        node, kwargs = _make_tree(tmp_path, base="hidraw7", hid_id=HID_ID_BT)
        assert (
            validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs)
            == "hidraw7"
        )

    def test_uevent_real_completo(self, tmp_path: Path) -> None:
        # O uevent inteiro como o kernel emite (com MODALIAS etc.).
        uevent = (
            "DRIVER=playstation\n"
            f"{HID_ID_USB}\n"
            "HID_NAME=Sony Interactive Entertainment DualSense Wireless Controller\n"
            "HID_PHYS=usb-0000:2d:00.3-4/input3\n"
            "HID_UNIQ=e8:47:3a:aa:bb:cc\n"
            "MODALIAS=hid:b0003g0001v0000054Cp00000CE6\n"
        )
        node, kwargs = _make_tree(tmp_path, uevent=uevent)
        assert (
            validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs)
            == "hidraw3"
        )


class TestValidateRejeita:
    def test_vpad_0df2(self, tmp_path: Path) -> None:
        # O vpad 0df2 JAMAIS é escondido — é por ele que o jogo fala.
        node, kwargs = _make_tree(tmp_path, base="hidraw6", hid_id=HID_ID_VPAD)
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_nintendo_057e(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path, base="hidraw13", hid_id=HID_ID_NINTENDO)
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_bus_desconhecido(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path, hid_id="HID_ID=0006:0000054C:00000CE6")
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_vendor_errado(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path, hid_id="HID_ID=0003:0000045E:00000CE6")
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_uevent_sem_hid_id(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path, uevent="DRIVER=playstation\n")
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_uevent_ausente(self, tmp_path: Path) -> None:
        node, kwargs = _make_tree(tmp_path)
        os.unlink(Path(kwargs["sys_class_hidraw"]) / "hidraw3" / "device" / "uevent")
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_traversal(self, tmp_path: Path) -> None:
        _node, kwargs = _make_tree(tmp_path)
        fora = f"{kwargs['dev_root']}/../dev/hidraw3"
        assert validate_physical_node(fora, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_symlink_plantado(self, tmp_path: Path) -> None:
        # /dev/hidraw4 -> hidraw3: mesmo com sysfs válido para hidraw4, o
        # lstat pega o link e rejeita (nó plantado).
        node, kwargs = _make_tree(tmp_path, base="hidraw4")
        os.unlink(node)
        os.symlink("hidraw3", node)
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_nao_char_device(self, tmp_path: Path) -> None:
        # stat REAL: o arquivo comum do tmp não é S_IFCHR → rejeita.
        node, kwargs = _make_tree(tmp_path)
        assert validate_physical_node(node, **kwargs) is None

    def test_major_minor_divergente(self, tmp_path: Path) -> None:
        # sysfs diz 237:4, o nó é 237:3 → symlink/nó plantado → rejeita.
        node, kwargs = _make_tree(tmp_path, dev="237:4")
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_devices_virtual_uhid_forjado(self, tmp_path: Path) -> None:
        # uhid malicioso anunciando 0ce6: o pai em /devices/virtual/ entrega.
        node, kwargs = _make_tree(tmp_path, virtual=True)
        assert validate_physical_node(node, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_no_inexistente(self, tmp_path: Path) -> None:
        _node, kwargs = _make_tree(tmp_path)
        ausente = f"{kwargs['dev_root']}/hidraw9"
        assert validate_physical_node(ausente, stat_fn=lambda _p: _chr_stat(), **kwargs) is None

    def test_nao_string(self, tmp_path: Path) -> None:
        _node, kwargs = _make_tree(tmp_path)
        assert validate_physical_node(None, **kwargs) is None
        assert validate_physical_node(42, **kwargs) is None
