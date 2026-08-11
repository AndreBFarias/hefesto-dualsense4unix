# PERFIL ATUAL — a linha dela ganha cor e o primeiro lugar

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"esse perfil inclusive precisa ter uma linha de cor de destaque
  e aparecer primeiro na guia de perfil pra sempre evidenciar o perfil atual"*
- **Status:** **ENTREGUE EM CÓDIGO — AGUARDANDO O OLHO DELA** (PROVA-DE-TELA-01:
  a palavra final é dela, com foto antes e depois)
- **Grau:** MEDIDO — cada cura foi arrancada do arquivo e vista reprovar

---

## 1. A pergunta que vinha antes do desenho

Pintar uma linha de verde é fácil. Difícil é responder **qual** linha, e a
resposta não era minha. Ela decidiu, no mesmo dia e com estas palavras:

> *"aquele cujo escolho vir na aba perfis e aperto em ativar"*

Então **perfil atual = o que ELA ativou**. Não é o que o autoswitch elegeu pela
janela aberta, e não é o `active_profile` do daemon quando ele está vazio.

E essa última parte não é hipótese. Na máquina dela, agora:

```
~/.config/hefesto-dualsense4unix/autoswitch_locked.flag   -> 10/08, 03:59
daemon.status  ->  active_profile: null
```

A lista se pendurava exatamente nesse `null`: `_active_profile_hint` só ganhava
valor quando o `daemon.status` trazia um nome. **A linha verde nasceria
invisível** — e o primeiro lugar não aconteceria nunca.

## 2. O fato que sobrevive ao `null`

O gesto de Ativar **deixa rastro em disco**, e o rastro já existia:

| arquivo | quem escreve | o que vale |
|---|---|---|
| `session.json` (`last_profile`) | `ProfileManager.activate(origin="manual")` | canônico do boot |
| `active_profile.txt` | `profile.switch` (IPC) e o ciclo por hotkey | **sempre manual-only** |

Desde o PERFIL-03 o autoswitch não encosta em nenhum dos dois, e
`resolve_boot_profile()` já sabe ler os dois e resolver a divergência — é o
**mesmo nome** que o daemon restaura no boot. Na máquina dela os dois dizem
`Pragmata`.

A cura, então, não foi inventar persistência: foi a aba **partir do fato que já
estava escrito** em vez de partir do vazio. `install_profiles_tab` semeia
`_active_profile_hint` com `perfil_que_ela_ativou()`, e o
`_on_daemon_status_for_sync` continua como sempre foi — ele só reescreve a marca
quando traz um **nome**, e o `null` passa direto sem apagar o que ela decidiu.

Efeito colateral bem-vindo: o destaque **sobrevive a fechar e reabrir a janela**.

## 3. O que a lista faz agora

- **A linha inteira em verde** (`@green #50fa7b`, o "ligado" desta casa, o mesmo
  que a janela compacta já usa): 6ª coluna no `ListStore` com o realce, amarrada
  por `attributes=5` nas **três** colunas visíveis. Amarrar só o "Nome" deixaria
  "Prioridade" e "Quando usar" na cor do tema — meia linha verde.
- **Verde no ativo, `None` nos demais** — sem atributo nenhum, quem decide a cor
  das outras linhas volta a ser o tema.
- **Primeiro lugar**, por `ordem_de_exibicao(perfis, ativo)` — função pura, o
  ativo primeiro e **o resto na ordem de carga**.
- **Trocar de perfil move a linha**, sem reler o disco: `store.reorder(...)` em
  `_mark_active_profile_row`, com a ordem-alvo calculada sobre o cache. Trocar
  três vezes **não** empilha as escolhas velhas no topo — a lista mostra o disco,
  não o histórico dela.

O que **não** mudou, de propósito: a coluna 0 continua sendo só o **nome**. Ela é
a identidade do perfil para `_selected_profile_name`, e um marcador textual ali
quebraria Salvar, Ativar, Duplicar e Remover de uma vez. (Classe CSS também não
resolve: `.hefesto-dualsense4unix-window label` vence classe própria por
especificidade, e a célula de um `GtkTreeView` nem é um `GtkLabel`.)

## 4. A foto reprovou a primeira versão — e essa é a história que interessa

A cura óbvia era a coluna `foreground` do `GtkCellRendererText`. Ela foi escrita,
os testes ficaram verdes, e **a foto reprovou**:

| foto | o que apareceu |
|---|---|
| perfil ativo **selecionado** (o caso de abrir a aba) | primeiro, negrito, **branco** |
| perfil ativo **não selecionado** | primeiro, negrito, **verde** |

O GTK3 **descarta o `foreground` da célula quando a linha está SELECIONADA** —
`gtkcellrenderertext.c` só aplica o atributo quando o estado não tem
`GTK_CELL_RENDERER_SELECTED`. E a linha selecionada é justamente a do perfil
ativo: a aba abre nela, e o `_sync_selection_with_active_profile` volta a
selecioná-la a cada resposta do daemon. **O verde sumia no caso mais comum** — o
oposto exato do "**sempre** evidenciar o perfil atual" que ela pediu.

Foto de bancada com as quatro alternativas na mesma imagem, **todas as linhas
selecionadas**:

| mecanismo | sobrevive à seleção? |
|---|---|
| `foreground=` | **não** — vira a cor de texto da seleção |
| `cell-background=` | **não** — fica escondido sob a faixa da seleção |
| `markup=` | sim |
| `attributes=` (`Pango.AttrList`) | sim |

Entre os dois sobreviventes ganhou o `attributes`, porque é o que **não mexe no
conteúdo**: a coluna 0 continua sendo o nome cru, sem escape de markup e sem um
perfil chamado `A & B` quebrar a lista.

Isto é o retrato do que a casa já sabia e voltou a cobrar: **a régua vale mais
que a lembrança**. Nenhum teste unitário desta entrega teria pego — todos liam o
modelo, e o modelo estava certo. Quem pegou foi a foto. Por isso ficou um teste
com a medição escrita dentro (`test_a_cor_nao_volta_a_ser_um_foreground_de_celula`)
para a próxima pessoa que achar que `foreground=` é a mesma coisa uma linha mais
curto — inclusive eu.

## 5. A armadilha que custaria a coluna "Quando usar"

O terceiro termo do desempate entre os "Sempre" é a **ordem de carga** do loader
(EMPATE-01/E2). Reordenar a lista que alimenta `rotulo_quando_usar` e
`explicacao_da_disputa` faria a GUI falar de uma fila que não é a do daemon.

Por isso são **duas listas**: a ordenada só ITERA o `append`; a de carga é a
única que chega às funções da disputa.

**Medição honesta do tamanho da armadilha** (força bruta sobre as funções puras,
10/08): mover **um** item para a frente preserva a ordem relativa de todos os
outros, e quando o movido está entre os empatados ele é o próprio incumbente —
que já ganharia. Ou seja: **o vencedor anunciado não muda**. O que muda é o
**tooltip**, que lista os concorrentes na ordem em que os recebe. A GUI passaria
a recitar `bbb, aaa, zzz` onde o loader lê `aaa, bbb, zzz`. Menor do que se temia,
e ainda assim uma frase divergindo do daemon — que é o que esta casa não entrega.
A guarda fica, e tem teste próprio.

## 6. A mordida

Nove curas arrancadas **do arquivo**, uma a uma, cada uma vista reprovar antes de
voltar:

| # | cura arrancada | reprova |
|---|---|---|
| 1 | a semeadura do disco em `install_profiles_tab` | sim |
| 2 | o `attributes=5` nas colunas visíveis | sim |
| 2b | o `attributes=` virando `foreground=` (a regressão da foto) | sim |
| 3 | a cor verde no `append` da linha ativa | sim |
| 4 | a `ordem_de_exibicao` no populate (o primeiro lugar) | sim |
| 5 | o `reorder` ao ativar outro perfil | sim |
| 6 | a cor no `_mark_active_profile_row` | sim |
| 7 | as duas listas (a ordenada vazando para a disputa) | sim |
| 8 | a ordem de carga no `reorder` (empilhar no topo) | sim |

## 7. Nota datada — os controles externos ficam para depois

Decisão dela, 10/08/2026, sobre 8BitDo e Nintendo Pro:

> *"por enquanto não, mas deixe anotado que em breve sim, após fazermos o mapa de
> specs completo"*

Então **nada foi construído para externo nesta leva**, e nada foi fechado contra
ele. O que faltará quando a hora chegar, escrito aqui para não se reaprender:

1. **Quem é "o perfil dela" quando há dois aparelhos na mesa.** Hoje o perfil é
   da sessão, e o destaque é um só. Com externos entrando, a pergunta vira *"o
   perfil atual de qual controle?"* — e ela já respondeu o princípio geral no
   mesmo dia: **por unidade vale para todas as abas**, com a exceção do que não
   tem resposta honesta por unidade.
2. **A cor precisa continuar sendo uma coluna do modelo**, não uma classe CSS
   nem um `foreground` de célula: quando a lista tiver de mostrar mais de um
   "atual", o que muda é o `AttrList` da 6ª coluna por linha — nada no tema. E se
   um dia forem cores DIFERENTES por unidade, o `AttrList` já aceita: o que hoje
   é uma instância compartilhada vira uma por cor.
3. **`ordem_de_exibicao` já aceita a generalização**: hoje recebe um nome; com
   mais de um ativo, recebe um conjunto e devolve os ativos primeiro, o resto na
   ordem de carga. A assinatura é o único ponto a mexer.
4. **O fato tem de continuar vindo do gesto dela**, não do daemon: `session.json`
   e `active_profile.txt` são de sessão, e por unidade precisariam de um lugar
   próprio — o molde é `controllers.json`, que já tem chave por unidade.

E o pré-requisito continua sendo o dela: **o mapa de specs completo primeiro**.

## 8. O que falta

**O olho dela.** A cor e a ordem são decisões visuais, e nesta casa interface só
fecha com foto e com a palavra dela.
