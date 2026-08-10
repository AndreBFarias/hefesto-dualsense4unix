# UI-SELETOR-01 — Os chips do topo aparecem fora de ordem

**Status:** **ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA**, remarcada em
09/08/2026, e **absorvida pela
[PLAYER-01](2026-07-25-PLAYER-01-um-numero-de-jogador.md)**: a ordem dos chips
passou a ser a do número exibido em `14cd31b` (25/07/2026). **Rótulo anterior:
ABERTA**, preservado aqui. Ver a nota datada no fim.
**O que falta ela validar, em uma linha:** ligar quatro controles em qualquer
ordem e ver os chips do topo saírem 1, 2, 3, 4 — e cada chip selecionar o
controle certo.
**Prioridade:** média — não quebra nada, mas confunde justamente quem tem vários
controles, que é o público do co-op.

## O sintoma

Com quatro controles conectados, o seletor do cabeçalho mostra:

```
Todos | Sony 2 · BT | Sony 1 · BT | Nintendo 3 · BT | 8BitDo 4 · BT
```

O jogador 2 vem antes do jogador 1. Os números estão **certos** — quem está
errada é a ordem.

## A causa (medida)

`status_actions.py:380` monta as linhas assim:

```python
rows: list[tuple[str, int | None]] = [(_("Todos os controles"), None)]
for c in conectados:
    ...
```

O laço percorre `conectados` **na ordem em que o daemon devolve** — que é a
ordem do bloco `controllers` do `state_full`, ou seja, ordem de enumeração e
conexão. O rótulo usa `_display_slot(c)` (o número de jogador, correto), mas a
**posição** na barra não segue esse número.

Como o número de jogador é estável entre replugs por MAC e a ordem de conexão
não é, os dois divergem sempre que alguém liga os controles fora de ordem — que
é o caso normal.

## Entrega

- [ ] Ordenar as linhas do seletor por `_display_slot`, mantendo "Todos" na
      posição 0. Controle sem slot conhecido vai para o fim, preservando a
      ordem relativa atual (`sorted` é estável).

## O que NÃO pode quebrar

- O índice carregado em cada linha é o `index` 0-based do bloco `controllers`,
  que é o que o IPC `controller.target.set` espera. **Ordenar a exibição não
  pode reordenar esse índice** — são coisas diferentes e a confusão entre elas
  seria um bug pior que o atual.
- `_target_active_position` (`status_actions.py:387`) acha a posição do alvo
  atual varrendo as linhas; continua funcionando com a lista ordenada, mas
  merece teste depois da mudança.
- O seletor é feito de **botões segmentados**, não de dropdown, porque o
  `cosmic-comp` fecha popups de combo (bug de foco conhecido do projeto). Não
  trocar o widget de passagem.

## Critério de conclusão

Com quatro controles ligados em qualquer ordem, os chips aparecem 1, 2, 3, 4 —
e clicar em cada um seleciona o controle certo.

---

## NOTA DATADA — 09/08/2026: absorvida pela PLAYER-01, e o `ABERTA` caducou

**Nada acima foi apagado.** O sintoma medido com quatro controles é o que
justificou o conserto, e é por ele que se entende a ordenação de hoje.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.** Esta
sprint não ganhou código próprio: ela foi **absorvida** pela
[PLAYER-01](2026-07-25-PLAYER-01-um-numero-de-jogador.md), que resolveu o
número e, com ele, a ordem.

| o que a sprint pedia | onde está hoje |
|---|---|
| os conectados saem na ordem do número exibido | `src/hefesto_dualsense4unix/app/actions/status_actions.py:1012` |
| e a ordem das linhas passa a ser a mesma | `src/hefesto_dualsense4unix/app/actions/status_actions.py:1055` |

As duas linhas citam `UI-SELETOR-01` por nome — a absorção está escrita no
próprio código, não só aqui.

**Commit:** `14cd31b`, 25/07/2026.

### Por que o rótulo não é ENTREGUE e sim ENTREGUE EM CÓDIGO

Porque o critério de conclusão desta sprint, escrito logo acima, **exige quatro
controles ligados** — e ninguém rodou isso na mesa dela desde a entrega.

**Nada ficou em aberto nesta sprint além dessa validação.**
