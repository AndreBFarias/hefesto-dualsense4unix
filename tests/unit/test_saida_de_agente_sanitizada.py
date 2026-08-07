"""O que está em ``docs/process/agentes/`` passou pelo sanitizador.

Este portão existe porque o irmão não cobre este chão: ``check_anonymity.sh``
**isenta** ``docs/process/**``, e o ``.gitignore`` diz por escrito que bloquear
``docs/process/audits/`` era "a defesa real". Em 06/08/2026 ela pediu que a saída
dos agentes passasse a ser versionada — o que reabre exatamente o caminho por
onde a senha ``sudo`` dela vazou em 26/06/2026, para cinco commits que hoje estão
em ``origin/main``.

A troca é: a saída entra, mas com um portão que morde.

Para arrancar e ver morder: escreva ``echo hunter2 | sudo -S ls`` em qualquer
arquivo de ``docs/process/agentes/``, ou devolva um MAC real a um deles.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from scripts.sanitizar_saida_de_agente import (
    _OUIS_COMO_TRIO,
    recusar,
    sanitizar,
)
from tests.unit.test_docs_mac_anonimato import _OUIS_REAIS_OCTETOS

AGENTES = RAIZ / "docs" / "process" / "agentes"


def _arquivos() -> list[Path]:
    """A saída de agente: as levas datadas, não a documentação do portão.

    O `README.md` do diretório EXPLICA os padrões proibidos, e por isso os
    contém — é a mesma isenção que `test_docs_mac_anonimato.py` dá a si mesmo.
    Só entram aqui as pastas de leva (`2026-08-06/` e as que vierem), que é onde
    a saída crua mora. Um arquivo novo na raiz não passa despercebido: ele
    simplesmente não é saída de agente, e o portão de MAC do repositório inteiro
    continua olhando para ele.
    """
    if not AGENTES.is_dir():
        return []
    return sorted(
        p
        for p in AGENTES.rglob("*")
        if p.is_file() and p.suffix == ".md" and p.parent != AGENTES
    )


def test_a_lista_de_ouis_tem_dono_unico() -> None:
    """Duas fontes para a mesma regra é a classe de defeito desta casa.

    O sanitizador importa os OUIs do portão de MAC. Se alguém copiar a lista
    para o script, este teste continua verde por acidente — então ele checa a
    IDENTIDADE do objeto derivado, não só o conteúdo.
    """
    esperado = {"".join(o) for o in _OUIS_REAIS_OCTETOS}
    assert esperado == _OUIS_COMO_TRIO, (
        "a lista de OUIs do sanitizador divergiu da do portão de MAC — "
        "há duas fontes para a mesma regra"
    )


@pytest.mark.parametrize("arquivo", _arquivos(), ids=lambda p: p.name)
def test_nenhum_arquivo_de_agente_tem_segredo(arquivo: Path) -> None:
    """Segredo faz o arquivo ser RECUSADO — nunca corrigido em silêncio."""
    texto = arquivo.read_text(encoding="utf-8", errors="replace")
    motivos = recusar(texto)
    assert not motivos, (
        f"{arquivo.relative_to(RAIZ)} tem segredo e não podia estar versionado:\n"
        + "\n".join(motivos)
        + "\n\nRode: python3 scripts/sanitizar_saida_de_agente.py ORIGEM DESTINO"
    )


@pytest.mark.parametrize("arquivo", _arquivos(), ids=lambda p: p.name)
def test_nenhum_arquivo_de_agente_tem_mac_real(arquivo: Path) -> None:
    """Sanitizar de novo não pode mudar nada — se muda, passou algo cru."""
    texto = arquivo.read_text(encoding="utf-8", errors="replace")
    assert sanitizar(texto, home=None) == texto, (
        f"{arquivo.relative_to(RAIZ)} tem MAC real (com separador, colado ou com "
        "o OUI elidido) — a máscara da casa é octetos 4 e 5 zerados"
    )


def test_o_sanitizador_recusa_a_forma_que_vazou() -> None:
    """A mordida do portão: a forma EXATA do vazamento de 26/06/2026."""
    assert recusar("echo hunter2 | sudo -S rm -rf /"), (
        "o sanitizador parou de recusar `echo <senha> | sudo -S`, que é como a "
        "senha dela entrou no repositório em 26/06/2026"
    )


def test_a_mencao_solta_ao_sudo_nao_recusa() -> None:
    """E a contrapartida: um portão que reprova citação vira ruído e morre.

    Os relatórios de agente citam `sudo -S` para EXPLICAR um achado — foi o caso
    de `tres-achados-da-noite.md`, que registra que a leva reiniciou o
    `bluetoothd` contra a regra explícita. Recusar isso apagaria a auto-auditoria.
    """
    assert not recusar("o relatório cita: sudo -S systemctl restart bluetooth")


def test_o_oui_publico_sobrevive_a_mascara() -> None:
    """Mascarar o OUI destruiria a informação sem proteger nada.

    O portão de MAC diz por escrito que "os OUIs em si já são públicos no repo".
    O que identifica o aparelho é o SUFIXO.
    """
    oui = ":".join(_OUIS_REAIS_OCTETOS[0])
    texto = f"o adaptador tem OUI {oui} e o sufixo dele importa"
    assert oui in sanitizar(texto, home=None)


def test_um_mac_real_completo_e_mascarado() -> None:
    """As três grafias, porque a forma colada é a que o produto gera."""
    a, b, c = _OUIS_REAIS_OCTETOS[1]
    limpo = sanitizar(f"{a}:{b}:{c}:c3:11:f0 e {a}{b}{c}c311f0", home=None)
    assert "c3:11" not in limpo and "c311" not in limpo, limpo
    assert f"{a}:{b}:{c}:00:00:f0" in limpo, limpo
