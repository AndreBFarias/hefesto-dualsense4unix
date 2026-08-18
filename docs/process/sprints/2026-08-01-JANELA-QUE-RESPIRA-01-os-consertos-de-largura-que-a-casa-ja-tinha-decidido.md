# JANELA-QUE-RESPIRA-01 — os consertos de largura que a casa já tinha decidido

- **Status:** ENTREGUE EM CÓDIGO em 01/08/2026, com **prova de tela offscreen
  antes e depois das nove abas**, e com **um aceite pendente**: o olho dela na
  janela real, pela regra da
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
- **Prioridade:** MÉDIA para cada item isolado, ALTA no conjunto — são regras
  que esta casa **escreveu três vezes** (LEGIBILIDADE-01/R1, VÃO-01/E3,
  LARGURA-01/E1, E3 e E9) e aplicou em parte, e o que sobrou é justamente o que
  ela vê
- **Aberta em:** 01/08/2026, por uma auditoria de UI/UX aba a aba sobre o
  retrato offscreen das nove telas em 1920x1080
- **Não abre regra nova.** Todo conserto aqui é a aplicação de uma decisão já
  registrada em sprint anterior. Onde a casa decidiu o contrário por escrito,
  esta leva **não mexeu** — ver "O que ficou de fora, de propósito"

## O fato que resume a sprint

A LEGIBILIDADE-01 escreveu, em 25/07, que `homogeneous=True` numa fileira de
botões dá a **todo** botão a largura do maior rótulo. A VÃO-01 repetiu em
27/07. A LARGURA-01 repetiu em 29/07 e ainda simulou o resultado, item a item,
com a palavra "**ainda reprova**" ao lado dos que não passavam.

Em 01/08, `homogeneous=True` sobrevivia em **sete** fileiras e havia sido
removido em três. O "Auto" da aba Rumble — quatro letras, ~40px de tinta —
recebia **459px**.

O mesmo padrão vale para as outras três regras: a tabela de teto de largura da
LARGURA-01/E1 tinha nove itens e **quatro** foram tratados; o teto de
comprimento de linha da E3 não tinha entrado em lugar nenhum (`grep
max-width-chars` no glade devolvia zero, com seis parágrafos acima de 800px, o
maior deles em **1869px**); e a E9 — pedido literal dela, *"abaixar os botões
pra ficar no rodapé das colunas"* — continuava aberta, com ~770px de vazio
dentro de cada moldura da aba Gatilhos.

Nada disto é decisão nova. É a lista de coisas que a casa já tinha decidido e
não tinha terminado de fazer.

## O que entrou

Medido no retrato offscreen de 1920x1080 (`scripts/gui-captura/retrato_offscreen.py`,
que é a convenção desta casa desde 26/07), antes e depois.

| # | Conserto | Onde | Regra que o manda |
|---|---|---|---|
| 1 | `homogeneous` fora de **sete** fileiras de botão | `gui/main.glade` — gatilhos L2 e R2, aplicar/apagar da Lightbar, presets de desenho, política de vibração, `profiles_btnbox`, `daemon_btns` | LEGIBILIDADE-01/R1 + VÃO-01/E3 |
| 2 | `max-width-chars=100` **+ `halign=start`** em seis parágrafos | `emulation_gamepad_hint_label`, `emulation_hint`, `player_leds_note`, `player_leds_auto_note`, a nota do mouse e o parágrafo de abertura da Lightbar | LARGURA-01/E3 |
| 3 | Teto de largura nos **cinco** itens restantes da tabela E1 | `lightbar_brightness_scale`, `profile_name_entry`, `profile_priority_scale`, `mouse_speed_scale`, `mouse_scroll_speed_scale` | LARGURA-01/E1 |
| 4 | A lista de atalhos ganha faixa e para de esticar | `key_bindings_treeview` — `max-content-height=320`, `propagate-natural-height`, `packing expand=False` | VÃO-01 (a quinta lista, que a tabela da sprint não pegou) |
| 5 | As ações dos Gatilhos vão para o **rodapé** da coluna | `valign=end` + `vexpand` nas duas fileiras | LARGURA-01/E9 — pedido literal dela |
| 6 | `btn_som_no_controle` volta para dentro do card Estado | `halign=start`, `hexpand` removido | LARGURA-01, mesma causa que a E2 tirou da barra de bateria |
| 7 | A abreviação `p/` sai dos dois rótulos de tela | "Copiar opções para os jogos", "Gamepad para os jogos:" | vocabulário leigo (RADAR-01/E4 e as sprints de PALAVRA) |

### A medição que corrigiu o próprio conserto nº 2

`max-width-chars` **sozinho não fez nada** — o retrato "depois" mostrou a linha
de 1869px da Emulação intacta. Em GTK3 essa propriedade limita a largura
**natural** (o que o widget *pede*); o pai segue livre para alocar mais, e um
`GtkLabel` esticado quebra na largura que **recebeu**, não na que pediu.

`halign=start` é o que faz a alocação parar na natural. Com os dois juntos, o
parágrafo caiu de **1869px para ~975px**.

Isto está escrito aqui porque é o tipo de meia-cura que passa despercebida: o
atributo está no arquivo, o teste de presença passaria, e a tela continuaria
igual. **Foi o retrato antes/depois que pegou** — nenhuma leitura de código
teria pegado.

## O achado de fora do escopo: `i18n_extract.sh` destrói tradução manual

Trocar dois rótulos exigia mexer nos catálogos. Rodar
`bash scripts/i18n_extract.sh`, que é o caminho documentado, foi medido:

| | antes | depois |
|---|---|---|
| `msgid` ativos em `po/en.po` | 295 | 367 |
| traduções preenchidas | 211 | 191 |
| entradas obsoletas (`#~`) | 123 | 212 |

Das **37** traduções que saíram, **3** eram desta leva. As outras **34** eram
entradas que levas anteriores adicionaram **à mão** — entre elas as quatro da
APLICAR-VERDADE-01 (`luzes`, `gatilhos`, `vibração`, `microfone`), que a sprint
registra em `po/en.po` e que a janela usa para dizer *"Aplicado, menos: luzes,
gatilhos."*

A causa: essas strings não passam por `_()` no ponto de declaração — o
`_NOMES_DE_SECAO` nasce no import, antes do `init_locale()`, e a tradução
acontece no uso (`footer_actions.py`, decisão registrada na APLICAR-VERDADE-01).
O `xgettext` não as vê, então o `msgmerge` as marca como obsoletas.

**Esta leva reverteu a extração e trocou as três strings à mão nos três
catálogos**, mantendo as 193 traduções ativas. O conserto de verdade —
`xgettext --keyword` ensinado a ver essas strings, ou um gate que reprove queda
no número de traduções ativas — é trabalho da faixa de i18n
(DOC-VERDADE-02/E6 + PROMESSA-NÃO-CUMPRIDA-01/F), e **fica registrado aqui para
não morder a próxima pessoa que precisar trocar um rótulo**.

## O que ficou de fora, de propósito

- **O `hexpand` da lista de perfis.** A auditoria pediu removê-lo; o glade tem,
  logo acima, a decisão contrária por escrito: *"O `hexpand` FICA: a restrição
  dura desta janela é a largura, e a lista divide a linha com o editor."* Não se
  desfaz decisão registrada por causa de uma medição que não a leu.
- **As quatro linhas da Emulação viram `GtkGrid`** (mais o `SizeGroup` dos dois
  cartões do topo, LARGURA-01/E7). É o único item estrutural da lista — entra
  sozinho, com foto.
- **A tradução dos campos do modo avançado dos Perfis** (`window_class`,
  `title_regex`, `re.search`, `CSV`, `AND`/`OR` na tela). É a maior dívida de
  vocabulário que sobrou, e mexe em `msgid` de sete strings — depende do
  conserto do `i18n_extract` acima para não custar 34 traduções.
- **`_WRAP_COLUNAS = 3` do `segmented_selector`** (LARGURA-01/E8), que a própria
  sprint pôs por último com três motivos escritos.

## Teste que morde

Os testes de layout que já existiam continuam verdes e cobrem o que mudou:
`test_largura_a_mesma_em_todas_as_abas.py` (deriva os números do próprio glade),
`test_layout_orcamento_altura.py`, `test_glade_signal_handlers.py` e
`test_glade_vocabulario_leigo.py`.

**A lacuna honesta:** nenhum deles reprova se o `homogeneous` voltar. Eles medem
a largura da PÁGINA, e a página cabe do mesmo jeito com os botões inchados —
foi por isso que sete fileiras atravessaram três sprints com a suíte verde. Um
gate que conte `homogeneous=True` em fileira de botão do glade é uma linha de
teste e ainda não existe; fica anotado como a entrega E1 de quem pegar esta
sprint de novo.

## Aceite

**Executável, já verde:** suíte completa e os oito portões de CI.

**O que só ela pode dar:** abrir a janela e passar pelas nove abas. O retrato
offscreen é o enquadramento maximizado dela e prova a geometria, mas não prova
que a aba ficou *boa* — e a regra desta casa é que interface só fecha com o olho
dela.

Os dois retratos estão lado a lado, nove telas cada, gerados pelo mesmo script e
na mesma resolução, para a comparação ser honesta.
