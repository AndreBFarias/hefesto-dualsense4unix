# CONFIG-03 — a declaração persiste

**Depende de:** CONFIG-02. [D-A3 decidida](DECISOES-ABERTAS.md): `maquina.json`.

## Por que esta sprint é maior do que parece

Não existe lugar para configuração que não seja de perfil. Esta sprint **cria a
camada**, e por isso é a maior da leva:

- `~/.config/hefesto-dualsense4unix/maquina.json` — arquivo novo, schema pydantic
  com `version: 1`, no molde de `profiles/schema.py`.
- Leitura no daemon. Hoje **nenhum módulo de `daemon/` importa `gui_prefs`** — o
  caminho de leitura é novo.
- Migração: o arquivo pode não existir, e ausência é estado válido.

## Invariantes

1. **Todo campo nasce em "não sei".** Ausência de declaração nunca quebra nada.
2. **A declaração não muda comportamento nesta sprint** — só persiste e chega ao
   daemon. Quem consome é CONFIG-04 e CONFIG-05.
3. **Diferida:** grava no "Aplicar" do rodapé, conforme [D-A4](DECISOES-ABERTAS.md).

## Prova de trabalho

```bash
pytest tests/unit/ -k "maquina or config" -q
# ida e volta real: declarar, fechar, reabrir
```

**Aceite:** declarar hub, fechar a janela, reabrir — a declaração está lá. Apagar
o arquivo à mão e reabrir — a aba abre em "não sei", sem erro.
