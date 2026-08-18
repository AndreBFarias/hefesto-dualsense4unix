# CR-06 — Devolver ao ecossistema: curvas livres para todo mundo

**Status:** ABERTA
**Depende de:** CR-04
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Publicar os efeitos de gatilho criados na CR-04 como **material livre**,
utilizável por qualquer projeto — e não só pelo Hefesto.

## A ideia

O problema que originou toda esta série é que as curvas de gatilho com nome só
existem, hoje, dentro de um repositório sem licença. Quem quer implementar
gatilho adaptativo no Linux esbarra na mesma parede: ou copia o que não pode,
ou fica sem.

Se as curvas da CR-04 ficarem boas, elas são **material original do Hefesto**,
medido em hardware próprio, com proveniência registrada. Nada impede que sejam
oferecidas ao ecossistema — e essa é a resposta mais útil possível ao problema:
em vez de mais um projeto contornando a parede em silêncio, uma alternativa
livre que derruba a parede para todos.

O ganho não é só altruísta. Curva usada por vários projetos é curva testada por
várias mãos, em vários controles — o oposto de valor medido numa máquina só.

## Entregas

- [ ] **Formato independente do Hefesto** — as curvas publicadas num arquivo de
      dados legível (JSON ou TOML) que qualquer projeto consiga ler, sem
      depender do nosso esquema de perfil. O formato interno pode continuar o
      que for melhor para nós; o publicado é para os outros.
- [ ] **Licença explícita e permissiva no artefato**, separada da licença do
      código. Dados de curva sob licença restritiva reproduziriam o problema que
      esta série existe para resolver. Avaliar CC0 ou MIT — CC0 tem a vantagem
      de eliminar qualquer dúvida sobre atribuição de dados factuais.
- [ ] **Documentar o método, não só o resultado** — como as curvas foram
      medidas, com que controle, e como reproduzir a medição. Quem quiser
      conferir ou estender precisa do procedimento, não apenas dos números.
      Este item é o que transforma a entrega de "confie em nós" em ciência.
- [ ] **Proveniência junto** — o `curvas-proprias.md` acompanha a publicação. É
      o que distingue material original de tabela sem origem, e é o exemplo que
      queremos que o ecossistema copie.
- [ ] **Anunciar onde faz diferença** — projetos Linux de controle (dualsensectl,
      Steam Input, quem mais estiver na mesma parede). Não é divulgação de
      produto: é avisar quem está preso no mesmo lugar que existe saída.

## Cuidados

- **Só depois da CR-04 concluída e validada.** Publicar curva mal medida como
  referência livre é pior que não publicar — vira dívida do ecossistema inteiro.
- **Nada de comparação com as tabelas do DSX**, nem para dizer "as nossas são
  melhores". A independência é demonstrada pelo método e pela proveniência, não
  por confronto. Comparação convida exatamente a análise byte a byte que o
  processo evita.

## Critério de conclusão

Um projeto Linux qualquer consegue pegar as curvas, entender de onde vieram,
usar sob licença clara, e reproduzir a medição se quiser conferir.
