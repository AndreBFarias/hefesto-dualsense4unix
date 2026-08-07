# CR-01 — Fechar a posição jurídica antes de medir qualquer coisa

**Status:** ENTREGUE em 2026-08-07. Em 2026-07-31 a varredura foi **fechada**
pela CR-05, e sobrava **uma** caixa — decisão da mantenedora, não trabalho
pendente. Ela respondeu em 07/08/2026: **MIT no código, CC0-1.0 nas curvas**
(grau: DECISÃO DELA). Nada mais está aberto aqui.
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
- [x] Auditoria do repositório inteiro atrás de material de terceiro não
      declarado. **Fechada em 2026-07-31 pela
      [CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md).** A
      varredura de 2026-07-25 já tinha coberto as 243 menções a DSX (todas em
      `daemon/udp_server.py` e `docs/protocol/udp-schema.md`, **nenhuma** código
      copiado — são ordinais de protocolo citados de quatro fontes para dirimir
      divergência). O que faltava era `assets/dkms/**`, e está feito: os três
      módulos de kernel, os oito `.patch`, as dependências Python, as fontes
      tipográficas, os glifos e o crate do applet estão declarados no `NOTICE`,
      cada um com origem e licença medidas arquivo a arquivo.

      Achado da varredura que vale registrar aqui, porque muda a leitura desta
      sprint: os fontes GPL **viajam em cinco dos sete artefatos publicados**
      (sdist, tarball de fonte, `.deb`, `.flatpak`, Arch e Fedora), o que é
      lícito e é o que a GPL-2.0 autoriza — mas foi feito com `LICENSE` e
      `README` dizendo "MIT" sem ressalva até a v0.4.0. Os dois foram corrigidos
      em 31/07. A tabela alvo por alvo, e a hipótese que isso refutou, estão na
      CR-05.
- [x] Decisão sobre a licença do projeto (MIT hoje). **Não é pré-requisito das
      demais sprints** — a licença do Hefesto governa o que terceiros fazem com
      o nosso código, não o que podemos fazer com o dos outros. Fica registrada
      aqui porque a mantenedora levantou, e porque o momento de decidir é agora:
      com um contribuidor só, mudar é barato; com o projeto crescido, exige
      concordância de todos.

      **RESPONDIDA EM 07/08/2026 — grau: DECISÃO DELA.** A resposta é
      **MIT no código, CC0-1.0 nas curvas medidas por ela**. É a resposta 2 de
      [as onze respostas do painel](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md),
      e não é proposta: é a palavra dela, e vale como doutrina da casa. Quem
      quiser mudar precisa de uma medição que derrube o motivo, não de uma
      opinião melhor.

      A separação tem razão medida, e é o problema que abriu esta série: as
      tabelas de curva com nome que existem hoje moram num repositório sem
      licença (`license: null`), e por isso não há caminho lícito a partir
      delas. Publicar as nossas sob dado restritivo reproduziria a parede com
      outro tijolo. CC0 elimina a dúvida sobre atribuição de dado factual —
      é o que faz a curva ser usável por qualquer projeto Linux sem advogado
      no meio. O desdobramento está na
      [CR-06](2026-07-25-CR-06-devolver-ao-ecossistema.md), e o registro em voz
      alta ficou no `NOTICE`, seção "A LICENÇA DAS CURVAS PRÓPRIAS".

      **Estado em 31/07 (nota histórica — não se apaga decisão medida):** a
      decisão continuava dela e continuava aberta. O que tinha mudado é que o
      `LICENSE` já não afirmava MIT sobre a árvore inteira — ele declarava MIT
      para o código próprio e nomeava a exceção de `assets/dkms/*`, com as
      licenças que estão nos cabeçalhos SPDX. Isso não decidia nada: só parava
      de dizer uma coisa que não era verdade enquanto a decisão não vinha.

      Custo colateral registrado em 31/07 para ela pesar: o bloco de escopo
      entrou **no topo** do `LICENSE`, antes do texto MIT, porque uma ressalva
      depois do juridiquês é ressalva que ninguém lê. O preço possível era a
      detecção automática de licença do GitHub deixar de rotular o repositório
      como "MIT" e passar a "View license". Se ela preferisse o rótulo, o bloco
      desceria — era uma linha de edição.

      **CADUCOU em 07/08/2026:** ela preferiu o rótulo, e o bloco não desceu
      para o rodapé — **saiu** do `LICENSE`. É a resposta 4 do mesmo painel, e o
      dono da ressalva passou a ser o `NOTICE`, na seção "ESCOPO DESTE ARQUIVO",
      que hoje carrega palavra por palavra o que o bloco dizia. O `LICENSE` ficou
      com o texto MIT canônico e nada antes dele, que é a forma que o detector
      do GitHub reconhece. O que caducou foi o **endereço** da ressalva, não a
      ressalva.

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
