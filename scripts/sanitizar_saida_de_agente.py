#!/usr/bin/env python3
"""Sanitiza saída bruta de agente antes de ela entrar no repositório.

POR QUE ISTO EXISTE
===================

O ``.gitignore:56-57`` bloqueia ``docs/process/audits/`` com um comentário que é
a própria lição::

    # anonimato isenta docs/process/**, entao o bloqueio aqui e a defesa real.

Ou seja: o portão de anonimato **não olha** ``docs/process/**``, e saída bruta de
agente é exatamente onde vazam coisas. Foi por ali que a senha ``sudo`` da
mantenedora entrou no repositório em 26/06/2026 e chegou a cinco commits que
hoje estão em ``origin/main`` — público. A faxina de ``26456fa`` tirou os
arquivos da árvore; o histórico guarda.

Em 06/08/2026 ela pediu que a saída dos agentes passasse a ser salva no
repositório. Este script é o que torna esse pedido seguro: **nada entra sem
passar por aqui**, e o que ele não souber mascarar ele **recusa** — não deixa
passar "na dúvida", porque foi o "na dúvida" que vazou a senha.

O CONTRATO
==========

- **MAC real** (as duas grafias: ``AA:BB:CC:dd:ee:ff`` e ``AABBCCddeeff``) é
  mascarado com a convenção da casa: octetos 4 e 5 zerados.
- **Sufixo com OUI elidido** (reticências seguidas de três octetos) também é
  mascarado: omitir o OUI
  nunca foi máscara, porque o sufixo é o que identifica o aparelho.
- **Segredo** (senha, token, chave) faz o arquivo ser **RECUSADO**, com o
  endereço da linha. Mascarar segredo automaticamente é o tipo de esperteza que
  cria a próxima falha silenciosa.
- **Caminho de HOME** vira ``~``, para não publicar a árvore de diretórios dela.

A lista de OUIs tem **dono único**: ``tests/unit/test_docs_mac_anonimato.py``.
Este script a importa de lá, e ``test_sanitizar_saida_de_agente.py`` reprova se
as duas divergirem — duas fontes para a mesma regra é a classe de defeito que
esta casa mais paga para não ter.

USO
===

    python3 scripts/sanitizar_saida_de_agente.py ORIGEM DESTINO
    python3 scripts/sanitizar_saida_de_agente.py --check ARQUIVO...

Sai 0 se tudo passou, 1 se algum arquivo foi recusado.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from tests.unit.test_docs_mac_anonimato import (  # noqa: E402
    _OUIS_REAIS_OCTETOS,
)

#: A forma com separador: `AA:BB:CC:dd:ee:ff` -> `AA:BB:CC:00:00:ff`.
#: Os exemplos aqui são FICTÍCIOS de propósito: o portão de MAC varre este
#: arquivo também, e um endereço real numa docstring o faria reprovar — foi o
#: que aconteceu na primeira escrita, em 07/08/2026.
_MAC_SEP = re.compile(
    r"(?i)\b(?P<oui>" + "|".join("[:_-]".join(o) for o in _OUIS_REAIS_OCTETOS) + r")"
    r"(?P<s1>[:_-])[0-9a-f]{2}(?P<s2>[:_-])[0-9a-f]{2}(?P<s3>[:_-])(?P<fim>[0-9a-f]{2})\b"
)

#: A forma COLADA, que é como o endereço sai do `controllers.json` e do journal.
_MAC_COL = re.compile(
    r"(?i)\b(?P<oui>" + "|".join("".join(o) for o in _OUIS_REAIS_OCTETOS) + r")"
    r"[0-9a-f]{4}(?P<fim>[0-9a-f]{2})\b"
)

#: A forma ELIDIDA que o portão irmão cobra: reticências e três octetos. Nem o
#: exemplo pode ser escrito aqui — o portão varre este arquivo. Omitir o OUI NÃO é
#: máscara — o sufixo é o que identifica o aparelho. Mesmo regex do portão, de
#: propósito: o sanitizador tem de limpar exatamente o que o portão reprova.
_SUFIXO_ELIDIDO = re.compile(
    r"(?i)(?P<pre>\.\.\.[:_-]?)"
    r"(?P<a>[0-9a-f]{2})[:_-](?P<b>[0-9a-f]{2})[:_-](?P<c>[0-9a-f]{2})\b"
)

#: O buraco de 06/08 (BURACO-DO-PORTAO-01): a página do 8BitDo escrevia, na
#: MESMA linha, os sufixos e o OUI. Cada pedaço passava porque estavam em
#: símbolos separados; remontar era juntar as pontas. Então um trio solto
#: `xx:yy:zz` também é mascarado — mas SÓ quando há um OUI real na mesma linha,
#: senão `12:34:56` de qualquer tabela viraria falso positivo.
_TRIO_SOLTO = re.compile(
    r"(?i)(?<![0-9a-f:_-])(?P<a>[0-9a-f]{2})[:_-](?P<b>[0-9a-f]{2})"
    r"[:_-](?P<c>[0-9a-f]{2})(?![0-9a-f:_-])"
)

#: Qualquer OUI real, nas duas grafias — o gatilho do `_TRIO_SOLTO`.
_QUALQUER_OUI = re.compile(
    r"(?i)\b(?:"
    + "|".join("[:_-]".join(o) for o in _OUIS_REAIS_OCTETOS)
    + "|"
    + "|".join("".join(o) for o in _OUIS_REAIS_OCTETOS)
    + r")\b"
)

#: O que faz o arquivo ser RECUSADO. Cada padrão nasceu de um vazamento real ou
#: de uma classe que já custou caro em algum projeto.
#:
#: O primeiro é a forma EXATA do vazamento de 26/06/2026: `echo <senha> | sudo -S`.
#: Foi assim, e só assim, que a senha dela entrou em cinco commits que hoje estão
#: em `origin/main`. `sudo -S` sozinho NÃO recusa — os relatórios citam o comando
#: para explicar um achado, e recusar a citação faria o portão virar ruído (que é
#: como um portão morre).
#: NOTA DATADA — 07/08/2026: O FILTRO ESTAVA APONTADO PARA A FORMA ANTIGA.
#:
#: GRAU: MEDIDO. Até esta data o `_SEGREDOS` reconhecia duas formas só: o cano
#: `echo ... | sudo -S` (a de 26/06) e o par palavra-chave-COM-SEPARADOR
#: (`senha:` / `password=`). A forma que ela usa de verdade no chat não é
#: nenhuma das duas — ela escreve a senha SOLTA, sem separador nenhum, do lado
#: do `sudo`: `usa sudo <numero> roda ... te autorizo` (07/08) e
#: `senha sudo <numero> pode tomar a decisão que quiser` (06/08). Nas duas, o
#: `\s*[:=]\s*` do padrão antigo não casa, e o arquivo PASSARIA.
#:
#: É o mesmo cano do vazamento de 26/06 com o filtro mirando a forma anterior —
#: e o cano só ficou perigoso de novo porque em 06/08 ela mandou versionar a
#: saída dos agentes. Os dois padrões abaixo fecham a forma nova.
#:
#: Por que tão APERTADOS, e não um `sudo\s+\S+` genérico: um portão que reprova
#: `sudo systemctl`, `sudo python3` ou `sudo chmod 755` vira ruído e é desligado
#: na terceira vez — é a mesma razão por que `sudo -S` sozinho só AVISA. Medido
#: antes de entrar: os dois varreram 753 arquivos de `docs/`, `scripts/` e
#: `tests/unit/` desta árvore com ZERO acertos.
_SEGREDOS = (
    (
        re.compile(r"(?i)(echo|printf)\s+\S+\s*\|\s*sudo\s+-S\b"),
        "senha canalizada para o sudo (`echo ... | sudo -S`) — a forma do vazamento de 26/06",
    ),
    (
        re.compile(r"(?i)\bsudo\s+[0-9]{4,}\b"),
        "senha solta ao lado do `sudo` (`... sudo <numero>`) — a forma dela, 07/08",
    ),
    (
        re.compile(
            r"(?i)\b(?:senha|password|passwd)\s+"
            r"(?:(?:de|do|da|para|e|eh|é)\s+)?(?:sudo\s+)?"
            r"(?<![0-9/-])[0-9]{4,}\b"
        ),
        "senha com número colado, sem separador (`senha sudo <numero>`)",
    ),
    (re.compile(r"(?i)\b(pass(word|wd)?|senha)\s*[:=]\s*\S+"), "senha literal"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token)\s*[:=]\s*\S{8,}"), "chave ou token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "chave privada"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]{20,}"), "credencial Bearer"),
)

#: Não recusam, mas saem no relatório para revisão humana. A diferença entre
#: recusar e avisar é o que decide se alguém continua usando este script.
_SUSPEITOS = (
    (re.compile(r"(?i)\bsudo\s+-S\b"), "menção a `sudo -S` (confira se há senha ao lado)"),
)


def _mascarar_sep(m: re.Match[str]) -> str:
    return f"{m['oui']}{m['s1']}00{m['s2']}00{m['s3']}{m['fim']}"


def _mascarar_col(m: re.Match[str]) -> str:
    return f"{m['oui']}0000{m['fim']}"


def _mascarar_elidido(m: re.Match[str]) -> str:
    if m["a"] == "00" and m["b"] == "00":
        return m.group(0)
    return f"{m['pre']}00:00:{m['c']}"


#: Os OUIs, como trio. Eles são PÚBLICOS — o portão irmão diz isso por escrito
#: ("os OUIs em si já são públicos no repo"), e o que identifica o aparelho é o
#: sufixo. Mascarar o OUI destruiria a informação que explica o achado sem
#: proteger nada.
_OUIS_COMO_TRIO = {"".join(o) for o in _OUIS_REAIS_OCTETOS}


def _mascarar_trio(m: re.Match[str]) -> str:
    if m["a"] == "00" and m["b"] == "00":
        return m.group(0)
    if f"{m['a']}{m['b']}{m['c']}".lower() in _OUIS_COMO_TRIO:
        return m.group(0)
    return f"00:00:{m['c']}"


#: Os emoji que CARREGAM sentido num relatório de agente: veredito em tabela.
#: Remover estes sem trocar apagaria a informação; os demais são decorativos.
#: Escritos por escape de propósito: o portão de glifos varre ESTE arquivo
#: também, e um emoji literal aqui o faria reprovar a si mesmo.
_EMOJI_COM_SENTIDO = {
    "\u2705": "[OK]",   # WHITE HEAVY CHECK MARK
    "\u274c": "[X]",    # CROSS MARK
    "\u2713": "[OK]",   # CHECK MARK — o que derrubou o commit de 07/08
    "\u2714": "[OK]",   # HEAVY CHECK MARK
    "\u2717": "[X]",    # BALLOT X
    "\u2718": "[X]",    # HEAVY BALLOT X
    "\u2716": "[X]",    # HEAVY MULTIPLICATION X
    "\u26a0": "[!]",    # WARNING SIGN
    "\U0001f6a8": "[!]",   # POLICE CARS REVOLVING LIGHT
    "\U0001f534": "[X]",   # LARGE RED CIRCLE
    "\U0001f7e2": "[OK]",  # LARGE GREEN CIRCLE
}


@lru_cache(maxsize=1)
def _carregar_detector_de_emoji() -> Callable[[int], bool]:
    """O `validar-glifos.py` tem hífen no nome, então não é importável direto.

    Carregar por `spec` é feio, e é de propósito: a alternativa era copiar a
    tabela Unicode de apresentação emoji para cá, e duas fontes para a mesma
    regra é a classe de defeito que esta casa mais paga para não ter.
    """
    caminho = RAIZ / "scripts" / "validar-glifos.py"
    spec = importlib.util.spec_from_file_location("_validar_glifos", caminho)
    if spec is None or spec.loader is None:  # pragma: no cover - defensivo
        raise RuntimeError(f"não consegui carregar {caminho}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.tem_apresentacao_emoji  # type: ignore[no-any-return]


#: Os blocos que o ADR-011 manda PRESERVAR. Eles desenham interface em texto
#: (tabelas, barras, setas) e sair deles quebraria a leitura dos relatórios.
_ADR011_PRESERVADOS = (
    (0x2500, 0x257F),  # Box Drawing
    (0x2580, 0x259F),  # Block Elements
    (0x25A0, 0x25FF),  # Geometric Shapes
    (0x2190, 0x21FF),  # Arrows
)

#: As faixas que o hook de pre-commit da casa bloqueia e que o
#: `validar-glifos.py` NÃO pega.
#:
#: MEDIDO em 07/08/2026: os dois portões da casa usam critérios DIFERENTES. O
#: `validar-glifos.py` segue a definição Unicode estrita (Emoji_Presentation),
#: então `U+2713` (CHECK MARK) passa por ele — o caractere tem apresentação de
#: TEXTO, não de emoji. O `universal-sanitizer.py` do pre-commit usa faixas
#: largas, entre elas Dingbats inteiro, e bloqueia o mesmo `U+2713`.
#:
#: Quem sanitiza para o repositório tem de obedecer ao MAIS ESTRITO, senão o
#: material passa no portão do repositório e trava no commit — que foi
#: exatamente o que aconteceu na primeira tentativa desta leva.
_FAIXAS_DO_HOOK = (
    (0x2600, 0x26FF),  # Miscellaneous Symbols
    (0x2700, 0x27BF),  # Dingbats: mora aqui o CHECK MARK que derrubou o commit
    (0x2934, 0x2935),
    (0x2B1B, 0x2B1C),
    (0x2B50, 0x2B50),
    (0x2B55, 0x2B55),
    (0x23E9, 0x23F3),
    (0x23F8, 0x23FA),
    (0x203C, 0x203C),
    (0x2049, 0x2049),
    (0x20E3, 0x20E3),
    (0x2122, 0x2122),
    (0x2139, 0x2139),
    (0x3030, 0x3030),
    (0x303D, 0x303D),
    (0x3297, 0x3297),
    (0x3299, 0x3299),
    (0x200D, 0x200D),
)


def _preservado_pelo_adr011(cp: int) -> bool:
    return any(lo <= cp <= hi for lo, hi in _ADR011_PRESERVADOS)


def _bloqueado_pelo_hook(cp: int) -> bool:
    if _preservado_pelo_adr011(cp):
        return False
    return any(lo <= cp <= hi for lo, hi in _FAIXAS_DO_HOOK)


def normalizar_glifos(texto: str) -> str:
    """Emoji vira texto, porque a casa proíbe emoji em QUALQUER arquivo.

    O ``scripts/validar-glifos.py`` diz isso por escrito, e não abre exceção nem
    para fixture, CHANGELOG ou registro histórico. Isentar a saída de agente
    seria furar uma doutrina declarada; normalizar preserva o sentido e respeita
    o portão. A definição de "é emoji" vem do próprio validador — dono único,
    pela regra da casa contra duas fontes para a mesma regra.

    Mas o validador do repositório **não é o portão mais estrito**: o hook de
    pre-commit da casa bloqueia faixas que ele deixa passar (ver
    ``_FAIXAS_DO_HOOK``). Aqui vale o mais estrito dos dois, senão o material
    passa no repositório e trava no commit. Os blocos que o ADR-011 manda
    preservar ficam intactos nos dois caminhos: é com eles que se desenha tabela.
    """
    tem_apresentacao_emoji = _carregar_detector_de_emoji()
    saida: list[str] = []
    for ch in texto:
        cp = ord(ch)
        if ch in _EMOJI_COM_SENTIDO:
            saida.append(_EMOJI_COM_SENTIDO[ch])
        elif ch == "\ufe0f":
            continue  # VARIATION SELECTOR-16: só força a forma emoji do anterior
        elif _preservado_pelo_adr011(cp):
            saida.append(ch)  # tabela, barra, seta: o ADR-011 manda preservar
        elif tem_apresentacao_emoji(cp) or _bloqueado_pelo_hook(cp):
            continue  # decorativo: sai sem deixar rastro
        else:
            saida.append(ch)
    return "".join(saida)


def sanitizar(texto: str, home: str | None = None) -> str:
    """Devolve o texto com MAC e caminho de HOME mascarados, e sem emoji."""
    texto = normalizar_glifos(texto)
    texto = _MAC_SEP.sub(_mascarar_sep, texto)
    texto = _MAC_COL.sub(_mascarar_col, texto)
    texto = _SUFIXO_ELIDIDO.sub(_mascarar_elidido, texto)
    # O trio solto só é tocado na linha em que um OUI real aparece — ver a nota
    # do `_TRIO_SOLTO`. Feito linha a linha porque o gatilho é a vizinhança.
    linhas = texto.splitlines(keepends=True)
    for i, linha in enumerate(linhas):
        if _QUALQUER_OUI.search(linha):
            linhas[i] = _TRIO_SOLTO.sub(_mascarar_trio, linha)
    texto = "".join(linhas)
    if home:
        texto = texto.replace(home, "~")
    return texto


def recusar(texto: str) -> list[str]:
    """Os motivos para RECUSAR o arquivo. Vazio = pode entrar."""
    motivos: list[str] = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        for padrao, o_que_e in _SEGREDOS:
            if padrao.search(linha):
                motivos.append(f"linha {numero}: {o_que_e}")
    return motivos


def suspeitar(texto: str) -> list[str]:
    """O que não recusa, mas merece o olho de alguém."""
    avisos: list[str] = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        for padrao, o_que_e in _SUSPEITOS:
            if padrao.search(linha):
                avisos.append(f"linha {numero}: {o_que_e}")
    return avisos


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("origem", type=Path, nargs="?")
    p.add_argument("destino", type=Path, nargs="?")
    p.add_argument("--check", type=Path, nargs="*", default=None)
    p.add_argument("--home", default=str(Path.home()))
    args = p.parse_args()

    if args.check is not None:
        problemas = 0
        for arquivo in args.check:
            texto = arquivo.read_text(encoding="utf-8", errors="replace")
            motivos = recusar(texto)
            if sanitizar(texto, args.home) != texto:
                motivos.append("contém MAC real ou caminho de HOME não mascarado")
            if motivos:
                problemas += 1
                print(f"RECUSADO: {arquivo}")
                for m in motivos:
                    print(f"  {m}")
        if problemas:
            print(f"\n{problemas} arquivo(s) recusado(s).")
            return 1
        print(f"OK: {len(args.check)} arquivo(s) sem segredo e sem MAC real.")
        return 0

    if not args.origem or not args.destino:
        p.error("informe ORIGEM e DESTINO, ou use --check")

    arquivos = sorted(args.origem.rglob("*")) if args.origem.is_dir() else [args.origem]
    recusados: list[tuple[Path, list[str]]] = []
    escritos = 0
    for arquivo in arquivos:
        if not arquivo.is_file():
            continue
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        motivos = recusar(texto)
        if motivos:
            recusados.append((arquivo, motivos))
            continue
        relativo = (
            arquivo.relative_to(args.origem) if args.origem.is_dir() else Path(arquivo.name)
        )
        alvo = args.destino / relativo
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(sanitizar(texto, args.home), encoding="utf-8")
        escritos += 1

    print(f"sanitizados e escritos: {escritos}")
    avisados = [
        (a, suspeitar(a.read_text(encoding="utf-8", errors="replace")))
        for a in arquivos
        if a.is_file()
    ]
    avisados = [(a, s) for a, s in avisados if s]
    if avisados:
        print(f"\nPARA O SEU OLHO ({len(avisados)}) — entraram, mas confira:")
        for arquivo, sinais in avisados:
            print(f"  {arquivo.name}: {sinais[0]}")
    if recusados:
        print(f"\nRECUSADOS ({len(recusados)}) — NAO entraram:")
        for arquivo, motivos in recusados:
            print(f"  {arquivo.name}")
            for m in motivos[:3]:
                print(f"      {m}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
