# VÃO-01 — a tela sobra e o conteúdo aperta

- **Status:** **ENTREGUE em 27/07/2026** (E1 a E4). E5 fica fora, por decisão
- **Prioridade:** MÉDIA (nenhum item desfaz trabalho dela)
- **Aberta em:** 27/07/2026, a pedido dela: *"queremos arrumar os espaços mal
  otimizados dos botões"*
- **Opção de layout escolhida por ela em 27/07:** **A — só devolver o espaço.**
  As nove abas ficam. Nenhum rótulo muda, nenhum `id` do Glade muda, nenhuma
  página troca de lugar
- **Não confundir com** [STATUS-SIMETRIA-01](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md),
  cujo escopo está trancado no card da aba Status. **Nada desta sprint entra na
  aba Status.** O card é dela

## O que ela vê, medido nas fotos

Nove abas fotografadas da janela real em 27/07 — maximizada, 1920x1080, controle
conectado por Bluetooth. Percentual da área entre a barra de abas e o rodapé que
é fundo liso:

| Aba | Vazio | Maior faixa contínua |
|---|---:|---|
| Rumble | 75% | 305 px a partir de y=661 |
| Gatilhos | 58% | 338 px a partir de y=565 |
| Início | 57% | disperso (máx. 44 px) |
| Lightbar | 57% | 290 px a partir de y=663 |
| Perfis | 46% | 117 px |
| Status | 43% | 25 px |
| Emulação | 39% | 115 px |
| Navegação DSX | 24% | 15 px |
| Sistema | 23% | 24 px |

Média: **47% da área útil é fundo liso** — e ao mesmo tempo há rótulo cortado,
botão de emergência com o menor alvo da tela e glifo de 20 px.

Capturas em `docs/process/estudos/assets/2026-07-27-abas/`.

## A causa mecânica: o espaço não tem dono

Duas medições explicam quase tudo.

**1. O tema governa cor e tipografia, e não governa espaço.**
`gui/theme.css` tem 19 `@define-color` com papel documentado e uma escala
tipográfica nomeada de 14 degraus. De espaçamento: **nada**. Os cerca de 150
valores de `spacing`, `margin` e `row/column-spacing` estão crus no Glade, em 9
valores distintos de espaço e 8 de margem. Mudar o espaçamento global hoje exige
editar 150 atributos à mão — por isso ninguém muda, e por isso **cada aba resolve
a folga de um jeito diferente**.

**2. A folga vertical tem quatro donos, e nenhum mostra algo que ela leia.**
`grep` no Glade inteiro devolve **quatro** `vexpand=True`:

| Linha | Widget | O que é |
|---|---|---|
| :513 | rolador de parâmetros do gatilho esquerdo | quase sempre vazio |
| :644 | rolador de parâmetros do gatilho direito | quase sempre vazio |
| :1366 | rolador da lista de perfis | lista curta |
| :1949 | `daemon_log_scroll` | caixa de texto em branco até alguém pedir diagnóstico |

Toda a folga da janela vai para esses quatro. É por isso que na aba Gatilhos
existem **830 px** entre o rótulo `Modo:` e o botão `Aplicar em L2` que o obedece,
e por que metade da aba Sistema é um retângulo em branco.

## As entregas

> **Item 0, antes de qualquer edição.** Rodar
> `tests/unit/test_layout_orcamento_altura.py` no HEAD e **guardar a saída no
> documento**. Toda a aritmética abaixo parte de números de LEGIBILIDADE-01, não
> da folga atual — e ninguém rodou esses testes neste ramo. Sem a linha de base,
> não há como saber se uma reprovação depois é regressão ou fato novo.

### E1. Tirar a folga dos quatro donos que não a usam

**Não é remover uma propriedade — são duas por widget.** No GtkBox do GTK3 o
filho recebe folga se `compute_expand` **ou** o `packing expand` for verdadeiro.
Tirar só o `vexpand` mantém os 830 px:

| Widget | `vexpand` | `packing expand` |
|---|---|---|
| rolador do gatilho esquerdo | `main.glade:513` | `:521` |
| rolador do gatilho direito | `:644` | `:652` |
| rolador da lista de perfis | `:1366` | `:1380` |
| `daemon_log_scroll` | `:1949` | `:1961` |

Pelo mesmo motivo, **`max-content-height` não resolve o log**: ele limita o
*pedido*, não a *alocação*. Com `packing expand=True` o widget continua engolindo
a folga inteira. Para o log, a saída correta é o expansor `Detalhes técnicos`
(`:1938`), que já existe: o bloco só ocupa espaço quando há o que mostrar.

**Cuidado declarado:** a aba Gatilhos foi o alvo do commit `b39fec9`, rejeitado.
Ela **não pega carona** aqui — entra com print antes e depois, isolada, e é a
única entrega desta sprint que exige aval visual antes do commit.

### E2. Os rótulos de estado da Emulação que já cortam hoje

Quatro `GtkLabel` com `wrap=True` (`main.glade:2170`, `:2226`, `:2271`, `:2308`).
Um rótulo com quebra reporta largura mínima de praticamente um caractere, então
num box horizontal ele perde toda a disputa para os botões irmãos: recebe 15 px
contra 23 de mínimo. **Já corta hoje**, com o texto sendo apenas um travessão.

**A correção NÃO é remover o `wrap`.** Os textos reais são multi-palavra —
`emulation_actions.py:409` escreve `desligado (suprimido)`, e há
`ligado — DualSense (PS)`. Sem quebra, a largura mínima da aba **sobe**, e
largura é a restrição dura desta janela: `test_layout_orcamento_altura.py`
existe justamente porque a rolagem horizontal é `never` e o mínimo sobe intacto
até a janela.

Usar `width-chars` / `max-width-chars` dimensionado pela palavra mais longa, e
rodar o teste de orçamento **de largura** antes e depois.

### E3. O botão de emergência da vibração

`rumble_stop` (`main.glade:1292`) é a parada de emergência que nasceu do incidente
*"tremendo sem parar"* de 25/07. Na tela ele tem cerca de 70 px, contra 460 px dos
seletores de política logo acima. Razão de 6 para 1. E ele é indistinguível dos
três vizinhos — um dos quais, `Deixar o jogo controlar a vibração`, desfaz o
efeito dele.

**A correção NÃO é dar largura a ele.** O Glade documenta, em `:1266-1275`, que
essa fileira está **sem `homogeneous` de propósito**: com distribuição homogênea
os quatro botões recebiam a largura do maior rótulo, e a fileira sozinha
respondia por **1004 dos 1066 px** de largura mínima da janela inteira. Foi
LEGIBILIDADE-01/R1 que a curou, e é essa largura devolvida que hoje paga o
aumento de fonte.

Ênfase por **cor, ordem e separação** — não por largura. O precedente de ênfase
por borda já existe na aba Gatilhos.

### E4. Piso de alvo clicável na barra de abas

`theme.css:600` estiliza `notebook > header > tabs > tab` com `padding: 8px 14px`
e `font-size: 13px`, e **não declara `min-height`** — enquanto `button` ganhou
`min-height: 24px` em `:186` por decisão explícita da casa (*"o piso de alvo
clicável passa a ser nosso"*). O principal meio de navegação da janela ficou de
fora da única regra de alvo que o projeto escreveu.

**Cuidado declarado:** engordar a tira de abas **baixa o teto de altura de todas
as nove páginas**, porque o orçamento por aba é derivado descontando o cromo do
notebook. A aba mais alta já estava em 626 de 654. Esta entrega só passa se o
teste de orçamento continuar verde — e se não continuar, ela **não entra**, vira
achado.

Cuidado adicional já registrado no arquivo: `theme.css:977-981` avisa que a ordem
das regras é estrutural. Acrescentar dentro do bloco existente, nunca mover blocos.

### E5. Tokens de espaço (a única entrega não reversível em uma linha)

Criar três ou quatro classes CSS de espaçamento e migrar os atributos do Glade
para `<style>`, **uma aba por vez**. O GTK3 não tem variável CSS nem `calc()`
(registrado em `app/theme.py:15-19`), então classe é o único canal possível.

**Depois** das entregas E1 a E4, nunca antes: é a única que não se desfaz
apagando uma linha.

## Como você valida

De olho, sem terminal, com a janela maximizada:

1. **Gatilhos:** o `Aplicar em L2` está perto do que ele aplica, não a meia tela.
2. **Sistema:** a caixa de log não ocupa mais metade da aba quando está vazia.
3. **Emulação:** as palavras de estado cabem inteiras — nenhuma cortada.
4. **Rumble:** o `Parar` se distingue dos vizinhos à primeira olhada.
5. **Abas:** clicar numa aba não exige mira.
6. **Todas as nove:** abrir uma por uma. **Se algo mudou de lugar na aba Status,
   esta sprint extrapolou e reprova** — o card é da STATUS-SIMETRIA-01.

E a regra da casa, aplicada a esta sprint: nenhuma entrega vai para o commit sem
print antes e depois guardado junto.

## O que a entrega de 27/07 mediu, com a prova ao lado

Provas em `docs/process/estudos/assets/2026-07-27-vao-01/`, renderizadas em
1920x1080 com o tema e a escala de fonte reais — antes a partir de um `git
worktree` do HEAD, depois da árvore de trabalho, com a mesma régua.

| Onde | Antes | Depois |
|---|---|---|
| Gatilhos: distância do `Modo:` até o `Aplicar em L2` | cerca de 830 px | cerca de 70 px |
| Perfis: distância do cabeçalho até os cinco botões da lista | cerca de 880 px | cerca de 100 px |
| Sistema: altura do log **vazio** | cerca de 410 px (metade da aba) | cerca de 75 px |
| Alocação dos roladores de gatilho | 514 px cada | 110 px cada |
| Suíte | 5558 testes, orçamento de altura 7/7 | idêntico |
| Glade | 205 ids, 70 sinais | 205 ids, 70 sinais, zero aviso do GtkBuilder |

**Três correções da própria sprint foram refutadas pela medição durante a
entrega, e é assim que devia ser:**

1. **E4 não entrou com 24 px.** `min-height` no nó `tab` do notebook **substitui**
   o piso herdado em vez de somar. O piso herdado nesta máquina já é 30 px, então
   declarar os 24 px do botão **encolheria** a tira. Entrou 30 px: idêntico na
   tela, e o piso passa a ser nosso — que é o objetivo escrito da entrega.
2. **Os roladores sem folga somem.** Com `expand=False` um `GtkScrolledWindow`
   sem piso pede zero e desaparece. Entrou faixa no lugar da folga: perfis
   200/320 px, log 140/260 px.
3. **A premissa do "15 px contra 23" era margem, não corte.** Os 8 px de
   diferença eram o `margin-end` do próprio rótulo. O defeito de largura existe,
   mas a conta estava errada.

### O que ficou visivelmente diferente, e você decide se fica

**Aba Emulação:** os rótulos de estado passaram a reservar a largura da palavra
mais longa. O ganho é que `desligado (suprimido)` e `ligado — DualSense (PS)`
passam a caber — antes cortavam. O efeito colateral é que, no estado ocioso (o
rótulo é só um travessão), os botões nascem cerca de 80 px mais à direita.

Vale registrar o outro lado: **antes os botões estavam desalinhados** entre si
(começavam em 148, 118 e 190 px); agora começam todos na mesma coluna. Se o
alinhamento não compensar o espaço reservado, reverter são quatro linhas de
`width-chars`.

**Aba Gatilhos:** a folga saiu de entre o `Modo:` e o `Aplicar em L2`, mas foi
para **baixo** dos botões — o card do gatilho continua expandindo, e ele não
estava na lista de widgets que a entrega podia tocar. Melhorou o que a sprint
prometia; não zerou o vazio da aba.

## O que NÃO foi medido

- **Os testes de layout no HEAD.** É o item 0 e ainda não rodou.
- **O efeito com a escala de fonte alta.** `theme.py:50` permite até `ESCALA_MAXIMA
  = 8`; a escala dela é 3, que é o padrão e não uma escolha
  (`gui_preferences.json` só tem `advanced_editor`). O pior caso do orçamento de
  largura é a escala 8 e ninguém a mediu.
- **`app/compact_window.py` e a bandeja.** Ficaram fora deste levantamento. Se a
  segunda janela repete card ou rótulos, uma correção de espaço feita só na janela
  principal sai pela metade.
- **Se o vazio incomoda.** Medi que ele existe e onde. Se 47% de fundo liso é
  desconforto ou é respiro é opinião dela, não medição minha — e é por isso que a
  opção escolhida foi a que não move nada de lugar.
