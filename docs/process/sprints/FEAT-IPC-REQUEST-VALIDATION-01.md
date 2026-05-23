# FEAT-IPC-REQUEST-VALIDATION-01 — resiliência do dispatcher IPC (anti-regressão)

**Tipo:** FEAT · **Wave:** V3.8 · **Estimativa:** P · **Dependências:** — · **Status:** DONE (escopo ajustado)

## Contexto

O plano previa schemas pydantic por método para validar entradas do IPC. A auditoria mostrou que a
validação/resiliência **já estava madura**: o dispatcher (`ipc_server._dispatch`) rejeita payload
não-objeto (PARSE_ERROR), `params` não-objeto (INVALID_PARAMS) e método desconhecido
(METHOD_NOT_FOUND), e captura toda exceção do handler mapeando para JSON-RPC limpo
(`ValueError`→INVALID_PARAMS, `Exception`→INTERNAL com log, sem derrubar o servidor). Os handlers
validam tipos e ranges (led rgb 0-255, brightness 0.0-1.0, rumble clamp) levantando `ValueError`,
e já havia testes amplos (método desconhecido, JSON malformado, led fora de byte, path traversal
sem leak, payload limit).

Reescrever 19 handlers com pydantic seria desproporcional e arriscado para ganho ~nulo.

## Decisão / Entrega

Escopo ajustado para o que faltava de fato: **anti-regressão** da resiliência.
- `tests/unit/test_ipc_server.py`: 2 testes novos — (1) `params` não-objeto (lista) via cliente cru
  retorna INVALID_PARAMS sem derrubar; (2) handler que levanta exceção inesperada vira INTERNAL e o
  servidor **sobrevive** (a chamada seguinte ainda funciona).

## Critérios de aceite

- Cliente bugado (params não-objeto, exceção no handler) não derruba o daemon; erro JSON-RPC limpo.
- pytest `test_ipc_server` verde (23).

## Arquivos tocados

- `tests/unit/test_ipc_server.py` (2 testes + import de `CODE_INTERNAL`).

## Nota

Validação declarativa (pydantic) fica como refino opcional futuro; a resiliência funcional já está
garantida e agora coberta por anti-regressão.
