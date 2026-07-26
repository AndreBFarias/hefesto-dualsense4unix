# UI-SELETOR-01 — Os chips do topo aparecem fora de ordem

- **Status:** ENTREGUE em 25/07/2026 pelo commit `14cd31b` — dentro de
  PLAYER-01, por absorção
- **Prioridade:** média — não quebra nada, mas confunde justamente quem tem
  vários controles, que é o público do co-op.

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

> **Fechamento (25/07/2026):** entregue por **absorção** em PLAYER-01
> (`14cd31b`), não por trabalho próprio desta sprint — a ordem passou a vir de
> `_por_numero_de_identidade` e o índice de cada linha continua sendo o `index`
> da enumeração, como a ressalva acima exigia.

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
