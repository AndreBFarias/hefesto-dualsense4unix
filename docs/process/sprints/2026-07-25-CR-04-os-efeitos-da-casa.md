# CR-04 — Os efeitos da casa

**Status:** ABERTA
**Depende de:** CR-03
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Criar o conjunto de efeitos com nome do Hefesto, medidos na bancada, com
proveniência. É o trabalho que fecha a lacuna dos doze modos "prontos" do DSX —
não imitando, mas fazendo o nosso.

## O que isto NÃO é

Não é reproduzir os modos do DSX com outro nome. Se o resultado for
`Hard` renomeado, o processo inteiro terá sido teatro.

O ponto de partida é a pergunta **"que sensações um jogo precisa?"**, não a
lista deles. Provavelmente a resposta tem menos de doze itens — e alguns que
eles não têm.

## Ponto de partida sugerido (a validar sentindo)

Nomes em português, vocabulário nosso (regra R2). Estes são **hipóteses de
partida**, não a lista final; a bancada é que decide:

| Nome | Sensação pretendida | Uso típico |
|---|---|---|
| `Pesado` | resistência firme e constante | porta, alavanca, arma pesada |
| `Macio` | resistência leve, curso todo | direção, mira |
| `Trepidante` | vibração ao longo do curso | metralhadora, motosserra |
| `Trava` | resistência que cede de repente | gatilho de arma semiautomática |
| `Dois Estágios` | ponto de resistência no meio | mirar e então atirar |

## Entregas

- [ ] Cada efeito medido na bancada, em **mais de um controle** quando houver
      (a resposta varia entre aparelhos, e a proveniência registra em qual).
- [ ] Nota de sensação escrita por quem mediu — não é enfeite: é o que permite a
      outra pessoa entender a intenção e refinar depois.
- [ ] Efeitos disponíveis na aba Gatilhos como presets, ao lado dos paramétricos.
- [ ] `docs/protocol/curvas-proprias.md` completo, gerado dos perfis.
- [ ] README e `udp-schema.md` atualizados: o que existe agora, e que os doze do
      DSX seguem sem tradução (isso não muda — são coisas diferentes).

## Uma possibilidade que vale considerar no fim

Se os efeitos da casa ficarem bons, eles são material **original do Hefesto**,
sob a licença do projeto — e podem ser oferecidos ao ecossistema Linux como
alternativa livre às tabelas que hoje só existem sem licença. Seria a resposta
mais útil possível ao problema que originou tudo isto.

## Critério de conclusão

Escolher `Pesado` na aba Gatilhos produz uma sensação que a mantenedora
reconhece como a que ela mesma ajustou — e a origem de cada byte está
registrada.
