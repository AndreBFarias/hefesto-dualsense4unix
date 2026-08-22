# A aba Configurações — por onde começar

Uma leva de planejamento. **Nada aqui foi implementado** — são o desenho, as
decisões e nove sprints prontas para executar.

## Se você tem cinco minutos

Abra o desenho. Ele é autocontido, não precisa de servidor nem de rede:

```bash
xdg-open docs/process/sprints/2026-08-21-ABA-CONFIGURACOES/mockup/aba-configuracoes.html
```

Passe o mouse nos rótulos com sublinhado pontilhado e nos `?`. Quase todo o
texto explicativo mora nas dicas, não na tela — foi assim que a aba encolheu de
2680 para 1729 pixels de altura.

## Se você vai implementar

Leia nesta ordem:

| # | Arquivo | O que responde |
|---|---|---|
| 1 | [COMO-EXECUTAR.md](COMO-EXECUTAR.md) | O roteiro, sprint por sprint, com arquivo, molde a copiar e prova de trabalho |
| 2 | [INDICE.md](INDICE.md) | Por que a aba existe e por que cada decisão foi tomada |
| 3 | [DECISOES-ABERTAS.md](DECISOES-ABERTAS.md) | As cinco perguntas de doutrina, e o que foi respondido em 21/08 |
| 4 | [TODO-INTEGRACAO.md](TODO-INTEGRACAO.md) | O que depende de outra frente, as medições pendentes e os scripts a atualizar |
| 5 | [TOOLTIPS.md](TOOLTIPS.md) | O texto exato de cada dica — não reescreva na hora |

**CONFIG-01 é o portão.** Enquanto a décima primeira aba não abrir vazia sem
quebrar as dez existentes, nenhuma outra começa.

## A tese, em uma frase

As dez abas de hoje operam sobre o que o produto **mede**. Esta é onde entra o
que ele **não tem como medir** e precisa que a pessoa declare — onde o dongle
está fisicamente, o que é aquele rádio vizinho, qual a cor do plástico quando a
leitura falha.

O teste de admissão de qualquer controle novo é uma pergunta só: *o Hefesto
conseguiria descobrir isso sozinho?* Se sim, o lugar não é aqui.

## Duas coisas que vão te poupar tempo

**A captura de tela morre se o terminal for um snap.** Ele exporta o cache de
loaders do próprio confinamento e o GTK cai no `image-missing.svg`. A cura:

```bash
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/olhar --mesa-cheia
```

**Largura é o recurso escasso, não altura.** A janela nasce em 1180px e não há
rolagem horizontal: o mínimo da página mais larga vira o mínimo da janela. Meça
antes de acrescentar coluna.
