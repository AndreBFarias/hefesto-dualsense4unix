# CONFIG-08 — a aba entra na documentação

**Depende de:** todas as anteriores que forem aprovadas.

## O que entrega

| Alvo | O quê |
|---|---|
| `docs/usage/interface.md` | A aba descrita, no mesmo formato das outras dez |
| `README.md` | A contagem de abas, se estiver citada |
| `docs/usage/assets/` | As capturas refeitas — **as onze abas, nos dois ambientes** |
| `CHANGELOG.md` | A entrada da leva |
| `GUIA-RADIO-DA-SALA.md` | **Versionar.** Está untracked na raiz e é a fonte primária da seção 1 — sem isso, a origem dos números pode desaparecer |
| `REGRA-NAO-REGISTRO-01` | **Registrar o escopo novo do VETO 3.** Ver [D-A1](DECISOES-ABERTAS.md) |
| `external_controllers.py:11-14` | **Nota datada** sobre o escopo reaberto. Ver [D-A2](DECISOES-ABERTAS.md) |

## Prova de trabalho

```bash
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py
python3 scripts/validar-acentuacao.py
python3 scripts/validar-palavra-de-tela.py
```

**Aceite:** `interface.md` descreve onze abas; nenhuma imagem do README ficou
para trás; e a captura roda limpa nos dois ambientes.

## As duas notas de doutrina

Não são burocracia — são a diferença entre uma regra que evoluiu e uma regra que
foi ignorada.

**VETO 3.** A `REGRA-NAO-REGISTRO-01` ganha o escopo decidido: *proibido declarar
o que o produto pode medir; permitido declarar o que ele comprovadamente não
mede*, com as duas salvaguardas. Quem ler a regra daqui a seis meses precisa
entender por que a aba Configurações existe sem parecer que alguém a furou.

**Escopo dos externos.** A fala em `external_controllers.py:11-14` —
*"só uma aba pra ver como os controles aparecem, não uma super central"* —
**não sai**. Ganha nota datada abaixo, dizendo que em 21/08/2026 o escopo foi
reaberto e apontando para [D-A2](DECISOES-ABERTAS.md). O padrão da casa para
decisão revogada é NOTA DATADA dentro do próprio docstring, nunca apagar.
