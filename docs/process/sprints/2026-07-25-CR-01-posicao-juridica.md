# CR-01 — Fechar a posição jurídica antes de medir qualquer coisa

**Status:** EM ANDAMENTO (aberta em 2026-07-25)
**Bloqueia:** CR-02, CR-03, CR-04 — nenhum valor de curva entra no repositório
antes desta sprint e da CR-02 estarem concluídas.
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Deixar registrado, com data, o que o projeto encontrou, avaliou e recusou —
antes de existir uma única curva própria. A ordem importa: um registro escrito
**depois** de os valores existirem vale muito menos que um escrito antes.

## Por que primeiro

A defesa de um projeto que não copiou não está no código: está na
rastreabilidade da decisão. Este é o único item da série que precisa
necessariamente vir antes, porque é o que datará a intenção.

## Entregas

- [x] `NOTICE` ganha a seção "O que este projeto deliberadamente NÃO
      incorporou", nomeando as curvas do DSX, o repositório onde estão, a razão
      da recusa (`license: null`) e a consequência assumida (os doze modos não
      funcionam).
- [x] `docs/process/CLEAN-ROOM.md` — as quatro regras do processo.
- [x] Distinção explícita, no mesmo texto, entre o que o projeto **usa** do
      ecossistema DSX (ordinais do enum = fato de interoperabilidade; formato do
      report = hardware da Sony) e o que **não usa** (as curvas).
- [ ] Auditoria do repositório inteiro atrás de material de terceiro não
      declarado. **Parcial:** varredura de 2026-07-25 encontrou 243 menções a
      DSX e projetos derivados, todas em `daemon/udp_server.py` e
      `docs/protocol/udp-schema.md`, e **nenhuma é código copiado** — são
      ordinais de protocolo citados de quatro fontes para dirimir divergência.
      Falta estender a varredura a `assets/dkms/**` (código de kernel derivado
      do Linux, GPL-2.0) e confirmar que o `NOTICE` declara essa proveniência.
- [ ] Decisão sobre a licença do projeto (MIT hoje). **Não é pré-requisito das
      demais sprints** — a licença do Hefesto governa o que terceiros fazem com
      o nosso código, não o que podemos fazer com o dos outros. Fica registrada
      aqui porque a mantenedora levantou, e porque o momento de decidir é agora:
      com um contribuidor só, mudar é barato; com o projeto crescido, exige
      concordância de todos.

## Achado que motivou a sprint

Durante a implementação do protocolo UDP (2026-07-25), as tabelas de curva dos
doze modos "prontos" foram localizadas em `WujekFoliarz/DualSenseY-v2`. São
cerca de treze tabelas de oito bytes — trabalho de minutos. A decisão de não
copiar foi tomada na hora e registrada no código
(`daemon/udp_server.py`, constante `DSX_TRIGGER_MODES`).

Esta sprint transforma aquela decisão pontual em posição documentada do projeto.

## Critério de conclusão

Um leitor externo, abrindo o repositório sem contexto, consegue responder: o
que o projeto usa de terceiros, sob que licença, e o que recusou usar e por quê.
