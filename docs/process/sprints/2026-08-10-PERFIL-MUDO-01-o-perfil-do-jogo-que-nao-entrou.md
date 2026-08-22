# PERFIL-MUDO-01 — o perfil daquele jogo que não entrou, e a janela que não dizia

- **Estado:** CONCLUÍDA — `profiles/porque_nao_entrou.py` nasceu desta sprint, seis arquivos de `src/` e quatro de `tests/` a citam, e o `if perfil.e_catch_all: continue` que passava arrancado MORREU de `profiles/simple_match.py` (verificado em 21/08/2026)
- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"mas sumiu na interface fui jogar pragmata pra testar o
  touchpad, o giroscopio e ele tá duplicado"*
- **Grau:** o RESULTADO é MEDIDO (journal de 30 dias dela + reprodução isolada).
  O MECANISMO (o que o Proton faz com o `/proc/PID/exe`) é **SEM PROVA** — e por
  isso não aparece em lugar nenhum do que foi entregue.

---

## 1. O que ela viu, e o que estava acontecendo

Ela abriu o Pragmata para testar touchpad e giroscópio. O controle veio
duplicado. O perfil `Pragmata` estava no disco, com o appid certo
(`steam_app_3357650`) — e **não entrou**.

O daemon **sabia**. Quatro vezes no journal, a mais recente às 00:40 de hoje:

```
profile_select_catch_all_sem_autoridade_em_jogo candidatos=['fallback'] wm_class=steam_app_3357650
```

`candidatos` é a lista de quem **casou**. Só o `fallback` casou. O perfil que ela
escreveu para aquele jogo não estava lá.

**E a janela não disse nada.** O journal não é interface.

---

## 2. A causa, isolada

Reprodução fora do journal, com os perfis dela e o mesmo código:

| o critério do `pragmata.json` | candidatos |
|---|---|
| como está no disco | `['fallback']` |
| tirando **só** o `PRAGMATA.exe` | `['fallback', 'Pragmata']` |

O critério é `window_class: ["steam_app_3357650"]` **e**
`process_name: ["PRAGMATA.exe"]`, e o `MatchCriteria.matches` é **AND**. Um campo
separa o perfil do jogo dele.

### O tamanho disso, no journal de 30 dias dela

| perfil | como identifica | o autoswitch já elegeu? |
|---|---|---|
| `Sackboy`, `Big Walk`, `Dont Scream`, `Navegação` | `window_class` | **sim** |
| `Pragmata` | `window_class` **+** `process_name` | **não** — só `origin=manual`, 6x |
| `Ação`, `Aventura`, `Corrida`, `Esportes`, `FPS` | só `process_name` | **nunca**, nenhuma vez |

**Cinco perfis dela nunca ativaram em 30 dias, e ela não tinha como saber.**

---

## 3. O que NÃO foi feito, e por quê

**Não se mexeu no perfil dela.** *"A vontade na GUI prevalece sempre"* — quem
escreveu `PRAGMATA.exe` foi ela, e apagar seria o produto decidindo no lugar dela
exatamente onde ela mandou que não decidisse.

**Não se afirmou nada sobre o Proton.** A leitura tentadora — "sob Proton o
`/proc/PID/exe` é o binário do wine, não o `.exe`" — **não foi medida**: nenhum
jogo Proton estava aberto durante a investigação. Ela pode estar certa e continua
sem prova, então não entrou em código, em frase de tela nem em veredito do
doctor. É a regra desta casa, e o `[[o-instrumento-mente-mais-que-o-produto]]`
custou o suficiente para ela valer aqui.

**O doctor ficou de fora, de propósito.** Sem janela de jogo aberta ele só
poderia SUPOR que um campo não vai casar. O que se mediu foi resultado, não
mecanismo — e resultado só se observa com o jogo na frente, que é justamente
onde a janela agora fala.

---

## 4. O que foi entregue

**A aba "No jogo" passa a dizer, em amarelo, o perfil que é daquele jogo e não
entrou** — com o que ele exigiu e o que o Hefesto viu, lado a lado:

> O seu perfil "Pragmata" é deste jogo, mas não entrou: ele exige nome do
> processo "PRAGMATA.exe", e aqui vê "wine64-preloader".
> Enquanto isso, vale o perfil "fallback".

Decisões do desenho, cada uma com o defeito que ela evita:

- **factual, nunca prescritiva** — não manda apagar campo, não chama a
  configuração dela de errada, não nomeia o Proton;
- **só as regras DAQUELE jogo** — na máquina dela, doze perfis "não entram" a
  cada janela de desktop, todos por funcionarem como deveriam. Mostrar os doze
  seria ruído que ensina a ignorar o aviso;
- **o fecho diz qual perfil valeu** — sem ele, a aba deixaria a pergunta óbvia
  (*então qual entrou?*) sem resposta na mesma tela;
- **aparece nos três modos**, inclusive junto do recado global: o perfil que não
  entrou é fato do disco e da janela, não depende de haver gamepad virtual — e
  na Conexão Nativa é justamente o perfil dela que ligaria o modo certo;
- **duas regras do mesmo jogo aparecem as duas** (ela teve `Pragmata` e
  `Pragmata2` no disco em 01/08): escolher uma seria o produto decidindo qual
  configuração dela importa;
- **o rótulo é o do editor** ("nome do processo", não `process_name`), senão a
  frase manda ela procurar um campo que a tela não tem.

E o custo foi tratado como parte da entrega: o `state_full` roda a **10 Hz** e
`load_all_profiles()` lê o disco inteiro. Sem cuidado seriam ~140 leituras de
JSON por segundo com os 14 perfis dela. Duas guardas, as duas com teste que
morde: fora de janela de jogo **não toca no disco**, e dentro dela o resultado
fica em cache chaveado pela tripla que o matcher consome.

---

## 5. Uma linha de código MORREU aqui

O primeiro desenho tinha `if perfil.e_catch_all: continue` na varredura. O teste
que dizia mordê-la **passava com ela arrancada**: um `MatchCriteria` catch-all é,
por definição, o que não tem campo nenhum preenchido — e esse não produz
reprovado, então a poda seguinte já o descartava.

A linha foi retirada em vez de ganhar um teste. Um `continue` que nunca executa
não é cinto: é a aparência de um.

---

## 6. O que fica ABERTO, e é dela

**O `PRAGMATA.exe` continua no arquivo dela.** Agora a janela diz o que ele
custa, e a decisão é dela — que é como ela decide: **vendo**.

Se ela quiser tirar, é pelo editor de perfil, na aba Perfis, campo "nome do
processo". Não precisa de terminal.

**Os cinco perfis que só têm `process_name`** (`Ação`, `Aventura`, `Corrida`,
`Esportes`, `FPS`) estão na mesma situação e **não** disparam o aviso — eles não
nomeiam appid nenhum, então nunca são "regra daquele jogo". Medido: nenhum
ativou em 30 dias. Fica registrado aqui porque é achado, e porque a cura, se ela
quiser uma, é outra conversa: dar a esses perfis um `window_class` é decidir
quais jogos são "de ação", e isso não é do produto.
