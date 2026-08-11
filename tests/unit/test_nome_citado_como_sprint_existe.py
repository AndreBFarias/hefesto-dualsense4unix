"""Nome citado como SPRINT ou ESTUDO tem de ter arquivo — ou ser divergência.

Defeito medido em 11/08/2026 (INDICE duas verdades, itens S-5, S-6, P-11): três
apelidos eram citados como documento — `GUERRA-01`, `GYRO-EDGE-RATE-01` e
`NINTENDO-VARIANT-01` — somando 26 citações em 19 arquivos, incluindo `src/` e o
cabeçalho de um patch que vai ao upstream. **Nenhum dos três tinha arquivo.**
Quem lia ia procurar, não achava, e ou perdia tempo ou concluía que a página
estava velha.

Esta casa batiza defeitos, e isso é bom: um nome curto viaja bem. O que não pode
é o nome fingir ser documento. A regra que este teste cobra tem duas saídas, e
só duas:

- **sprint ou estudo** — tem arquivo em `docs/process/sprints/` ou
  `docs/process/estudos/`, e se cita com link;
- **divergência nomeada** — está registrada em
  `docs/process/DIVERGENCIAS-NOMEADAS.md`, e se cita dizendo o que é.

É o irmão pequeno da regra 4 proposta na RÓTULOS-DE-SPRINT-01, seção 5: lá se
cobra que o RÓTULO acompanhe o código; aqui se cobra que o NOME exista.

A MORDIDA, provada em 11/08/2026
================================
Removida a entrada de `GUERRA-01` do DIVERGENCIAS-NOMEADAS.md,
`test_todo_nome_citado_como_documento_existe` reprova nomeando os arquivos que o
citam. Devolvida, verde. Um nome inventado num documento de teste também reprova
(caso `test_nome_inventado_reprova`).
"""
from __future__ import annotations

import re
from pathlib import Path

REGISTRO = Path("docs/process/DIVERGENCIAS-NOMEADAS.md")

#: A forma que MENTE: citar o apelido como se fosse documento. Cobre "a sprint
#: X", "o estudo X", "ver sprint X" — em qualquer caixa.
_CITADO_COMO_DOC = re.compile(
    r"\b(?:a\s+|o\s+|ver\s+|vide\s+)?(?:sprint|estudo)s?\s+`?([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9-]{3,}-\d{2})`?",
    re.IGNORECASE,
)

#: IDs DE TAREFA, que esta casa também batiza — e que NUNCA foram documento.
#: Medido em 11/08 ao ligar este portão: ele pegou `FEAT-METRICS-01`,
#: `REFACTOR-LIFECYCLE-01`, `CHORE-CI-REPUBLISH-TAGS-01` e uma dúzia de irmãos.
#: São identificadores de unidade de trabalho (o que virou commit), de um
#: vocabulário anterior ao de sprints — cobrar arquivo deles seria inventar
#: dívida onde não há, e um portão que acusa demais é desligado na primeira
#: semana.
#:
#: A distinção é de INTENÇÃO: `FEAT-`/`BUG-` nomeiam trabalho; `MAPA-TELA-01` e
#: `RADIO-ABERTO-01` nomeiam um documento que alguém deveria poder abrir.
_PREFIXOS_DE_TAREFA = (
    "FEAT-", "BUG-", "CHORE-", "REFACTOR-", "DOC-", "DOCS-",
    "TEST-", "TESTS-", "PERF-", "FIX-", "CI-", "SPRINT-",
)


def _e_id_de_tarefa(nome: str) -> bool:
    return nome.upper().startswith(_PREFIXOS_DE_TAREFA)


def _raiz() -> Path:
    return Path(__file__).resolve().parents[2]


def _nomes_com_arquivo() -> set[str]:
    """Os apelidos que TÊM documento, lidos dos nomes de arquivo."""
    nomes: set[str] = set()
    for pasta in ("docs/process/sprints", "docs/process/estudos"):
        d = _raiz() / pasta
        if not d.is_dir():
            continue
        for f in d.glob("*.md"):
            # `2026-08-09-ROTULOS-DE-SPRINT-01-entregue...` -> `ROTULOS-DE-SPRINT-01`
            achado = re.search(r"\d{4}-\d{2}-\d{2}-([A-Z][A-Z0-9-]*-\d{2})", f.name)
            if achado:
                nomes.add(achado.group(1).upper())
    return nomes


def _nomes_registrados_como_divergencia() -> set[str]:
    """Os apelidos que assumem NÃO ser documento, e dizem isso no registro."""
    caminho = _raiz() / REGISTRO
    if not caminho.is_file():
        return set()
    texto = caminho.read_text(encoding="utf-8")
    return {
        m.upper()
        for m in re.findall(r"^### `([A-Z][A-Z0-9-]*-\d{2})`", texto, re.MULTILINE)
    }


def test_o_registro_de_divergencias_existe():
    """Sem ele, a segunda saída da regra não existe e tudo vira defeito."""
    assert (_raiz() / REGISTRO).is_file(), (
        f"{REGISTRO} sumiu. Ele é onde um apelido assume não ser sprint — sem "
        "isso, todo nome batizado teria de virar arquivo, o que ninguém vai fazer."
    )


def test_todo_nome_citado_como_documento_existe():
    """Nenhuma citação de 'sprint X' ou 'estudo X' pode apontar para o nada."""
    conhecidos = _nomes_com_arquivo() | _nomes_registrados_como_divergencia()
    violacoes: list[str] = []

    for doc in (_raiz() / "docs").rglob("*.md"):
        # O próprio registro cita os nomes para explicá-los; e o índice que
        # DIAGNOSTICOU o defeito precisa citá-los para descrevê-lo.
        if doc.name == REGISTRO.name or "INDICE-duas-verdades" in doc.name:
            continue
        texto = doc.read_text(encoding="utf-8", errors="replace")
        for numero, linha in enumerate(texto.splitlines(), start=1):
            for nome in _CITADO_COMO_DOC.findall(linha):
                if _e_id_de_tarefa(nome):
                    continue
                if nome.upper() not in conhecidos:
                    rel = doc.relative_to(_raiz())
                    violacoes.append(f"{rel}:{numero}: {nome}")

    assert not violacoes, (
        "nome citado como sprint ou estudo, e não existe arquivo nem entrada em "
        f"{REGISTRO}.\n"
        "Duas saídas: escreva o documento, ou registre como divergência nomeada "
        "e cite dizendo que é.\n" + "\n".join(sorted(set(violacoes))[:25])
    )


def test_nome_inventado_reprova(tmp_path, monkeypatch):
    """A régua morde: um nome que não existe em lugar nenhum é pego.

    Sem este caso, `test_todo_nome_citado_como_documento_existe` poderia estar
    verde por não achar nada — e um regex que não casa nunca reprova.
    """
    conhecidos = _nomes_com_arquivo() | _nomes_registrados_como_divergencia()
    inventado = "NOME-QUE-NUNCA-EXISTIU-99"
    assert inventado not in conhecidos
    achados = _CITADO_COMO_DOC.findall(f"ver a sprint `{inventado}` para o resto")
    assert inventado in [a.upper() for a in achados], (
        "o regex não reconhece a forma 'ver a sprint X' — ele não morderia o "
        "defeito que este teste existe para pegar"
    )


def test_as_tres_divergencias_de_11_08_estao_registradas():
    """As três que motivaram o registro continuam nele.

    Se uma virar sprint de verdade, tire-a daqui E do registro no mesmo passo —
    o teste acima aceita as duas formas, então a troca é segura.
    """
    registradas = _nomes_registrados_como_divergencia()
    for nome in ("GUERRA-01", "GYRO-EDGE-RATE-01", "NINTENDO-VARIANT-01"):
        assert nome in registradas or nome in _nomes_com_arquivo(), (
            f"{nome} saiu do registro sem virar arquivo. As 26 citações que "
            "existem na árvore voltam a apontar para o nada."
        )
