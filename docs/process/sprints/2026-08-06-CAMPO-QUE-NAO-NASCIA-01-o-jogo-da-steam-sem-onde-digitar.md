# CAMPO-QUE-NAO-NASCIA-01 — o jogo da Steam sem onde digitar

- **Achado em:** 05/08/2026, por volta das 23h — **queixa dela**, dita ao vivo
  enquanto outra sprint estava sendo escrita. Não veio de auditoria, nem de
  varredura, nem de bancada: veio de ela tentar usar o produto
- **Estado:** **CURA APLICADA** e commitada em `0bb92a5`; esta sprint é a
  **materialização atrasada** — a cura, os oito testes de GTK real e a doutrina
  ensinada aos seis dublês existem desde 05/08, o documento não
- **Gravidade:** **ALTA** no efeito — o caminho que a própria interface oferece
  para "este perfil é deste jogo da Steam" **não tinha como ser percorrido**, e
  falhava **em silêncio**: sem erro, sem log, sem nada vermelho
- **Causa-raiz:** **MEDIDA** — reproduzida com o GTK de verdade sobre o glade de
  verdade, e **remedida em 06/08** durante a escrita deste documento
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [JOGOS-QUE-ELA-TEM-01](2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md)
    — é a sucessora, e por isso **não** é a mesma: lá o pedido é **não precisar
    do número**; aqui o defeito é o campo em que o número seria digitado nem
    existir na tela;
  - [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md)
    — escrita no mesmo turno e entregue no **mesmo commit**; ela trata do Steam
    Input, não do editor de perfis;
  - [JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md)
    — já tinha registrado, cinco dias antes, que `show_window` é um `show_all()`
    e que widget escondido **sem** `no-show-all` volta sozinho. É o mecanismo do
    item aberto no fim desta página, visto pela outra ponta;
  - [SALVAR-NAO-REBAIXA-02](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md)
    — mora no **mesmo handler** (a marca `_regra_tocada`), e é um dos seis
    arquivos de dublê que passaram por cima deste defeito.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O sintoma, na frase dela

> *"1599660 quando eu clico em jogo da steam não aparece nenhum campo pra
> digitar"*

O `1599660` é o appid que ela tinha em mãos e **não tinha onde escrever**. Ela
clicava em "Jogo da Steam" no seletor "Aplica a:", a linha do formulário abria
espaço — e dentro do espaço não havia nada. Nem o rótulo "Nome do jogo:", nem a
caixa de texto.

Detalhe que ficou registrado no produto: o número da queixa dela virou o
**exemplo do campo**. O placeholder de "Jogo da Steam" é literalmente
`ex.: 1599660` (`profiles_actions.py:100`). **Grau: MEDIDO** (está no
`_CAMPO_LIVRE_DICAS`, e há teste que cobra a string).

---

## Os DOIS códigos: um defeito, duas grafias

Antes do mecanismo, o achado de higiene — porque ele atrapalha quem for
procurar por isto depois.

Existem **duas grafias em circulação**, e nenhuma busca encontra as duas:

| grafia | onde vive | quantos arquivos |
|---|---|---|
| `CAMPO-QUE-NAO-NASCE-01` | só no **produto** (`profiles_actions.py:1067`) e na **mensagem do commit** | 1 |
| `CAMPO-QUE-NAO-NASCIA-01` | só nos **testes** (o arquivo dedicado e os seis dublês) | 7 |

**Grau: MEDIDO**, por `git grep -c` nas duas grafias e por
`git log --grep`, que devolve **vazio** para `NASCIA` e acha o `0bb92a5` só por
`NASCE`.

**É erro de digitação, não dois defeitos.** O comentário de cura e o docstring
do teste descrevem o **mesmo** mecanismo (`no-show-all` no mesmo box), citam a
**mesma** data, a **mesma** frase dela e a **mesma** cura, e entraram no
**mesmo commit**. Não há dois sintomas, dois arquivos ou duas medições.

O custo é real e é de busca: quem parte do produto (`NASCE`) não acha nenhum
teste; quem parte do teste (`NASCIA`) não acha nem o código nem o commit. Um
código de sprint com duas grafias é um código que não serve para o que ele
existe. Esta página adota **`CAMPO-QUE-NAO-NASCIA-01`** — a grafia de sete dos
oito lugares, e a que está no **nome do arquivo em disco**. A unificação da
grafia restante fica como item aberto, e **não** foi feita aqui: a árvore de
trabalho é o que roda, e ninguém pediu.

---

## O mecanismo, e nenhuma das três linhas é nossa

**Grau: MEDIDO**, lido no glade e reproduzido com GTK real.

1. No `main.glade:2049-2069`, o `GtkBox id="profile_game_entry_box"` nasce com
   `visible=False` **e** `no-show-all=True`. As duas de propósito: sem elas, o
   `show_all()` da janela mostraria o campo do jogo antes de ela escolher
   qualquer coisa;
2. a doutrina do GTK é que `no_show_all` faz o `show_all()` **ignorar** o
   widget — e, por não descer nele, os **filhos nunca são mostrados**. Os dois
   filhos deste box (o `GtkLabel` "Nome do jogo:" e o
   `GtkEntry profile_simple_custom_name`, `main.glade:2054-2068`) **não
   declaram `visible` nenhum**: dependiam inteiramente daquela descida;
3. o handler `_on_aplica_a_changed` fazia `box.show()`. O `show()` levanta a
   bandeira **da caixa** e para ali.

Resultado na tela dela: a linha do formulário passa a ocupar espaço, e o espaço
está vazio. O produto tinha feito exatamente o que o código mandava.

### Por que `show_all()` seco também não resolveria

Trocar `box.show()` por `box.show_all()` parece a correção óbvia e **não
corrige nada**: o `no_show_all` faz o `show_all()` ignorar o widget
**inclusive quando chamado nele mesmo**. Isto não é opinião nossa sobre o GTK —
é um caso de teste que roda:
`test_show_all_com_no_show_all_ainda_armado_tambem_nao_mostra_nada`.
**Grau: MEDIDO.**

É por isso que a ordem da cura não é ornamento.

## A cura: duas chamadas, nesta ordem

`profiles_actions.py:1082-1083`, no ramo das escolhas que exigem alvo
(`"game"` e `"steam_game"`):

```python
box.set_no_show_all(False)
box.show_all()
```

Desarmar primeiro, mostrar depois. O `else` do mesmo handler continua fazendo
`box.hide()` (`:1085`), que é o que tira a linha da tela quando ela escolhe
"Qualquer" — e é a ponta oposta, que a cura não podia quebrar.

---

## Por que a suíte inteira passou por cima — e é esta a lição

**Grau: MEDIDO**, remedido em 06/08 durante a escrita desta página.

Seis arquivos de teste já cobriam o "Aplica a". Todos usavam um dublê `_FakeBox`
com um atributo booleano (`.visivel` / `.visible`), e **todos afirmavam sobre a
CAIXA**:

- `test_r12_editor_simples_gui.py`
- `test_profiles_gui_sync.py`
- `test_gui_perfil_manual_editor.py`
- `test_modo01_o_modo_jogo_liga_sozinho.py`
- `test_empate01_a_cor_volta_a_ser_dela.py`
- `test_salvar_nao_rebaixa_02_o_novo_perfil_desligava_as_guardas.py`

O dublê respondia *"estou visível"* ao `show()` — corretamente, aliás, porque a
caixa **estava** visível. **Ninguém perguntava pelos filhos**, que é onde o
defeito morava.

A remedição de hoje devolveu o `box.show()` de antes da cura ao handler, em
memória, sem tocar em arquivo do repositório, e rodou os dois conjuntos:

| conjunto | com a cura | com a cura arrancada |
|---|---|---|
| os seis arquivos de dublê (122 casos) | 122 verdes | **122 verdes** |
| `test_campo_que_nao_nascia_01_*` (8 casos) | 8 verdes | **4 vermelhos** |

Os quatro que caem são exatamente os que perguntam pelo **campo**:
`test_jogo_da_steam_faz_o_campo_nascer_pelo_handler_real`,
`test_jogo_da_steam_traz_a_dica_do_appid_junto_com_o_campo`,
`test_jogo_especifico_tambem_faz_o_campo_nascer` e
`test_qualquer_esconde_o_campo_e_jogo_da_steam_o_traz_de_volta`.

### O que o arquivo novo faz de diferente

Um teste novo com dublê não valeria nada — seria o sétimo a perguntar à caixa.
Por isso `test_campo_que_nao_nascia_01_o_jogo_da_steam_sem_onde_digitar.py`:

- exige **GTK real** logo na primeira linha (`exigir_gi_real`, antes de qualquer
  `import gi`), porque contra o stub da bancada ele passaria sem mostrar nada a
  ninguém;
- monta o **glade real** numa `Gtk.OffscreenWindow` — a armadilha 2 da casa
  ([COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md)): sob Xvfb não há gerenciador
  de janelas e uma `Gtk.Window` fica 1x1 para sempre;
- **abre a aba Perfis** antes de medir, porque `get_mapped()` só vira verdadeiro
  na página corrente do notebook — é a diferença entre "a bandeira subiu" e
  "apareceu na tela dela";
- exercita o **handler de produção** pelo `SegmentedSelector` de verdade, com o
  mesmo `connect("changed", ...)` do `_build_profiles_tab`;
- e **toda asserção central é no `GtkEntry`**, nunca no box.

Tem ainda uma **contraprova** que é o que faz o resto morder:
`test_show_sozinho_revela_a_caixa_e_deixa_o_campo_invisivel` fixa, por escrito e
em execução, o comportamento **antigo** — caixa visível, campo invisível, rótulo
invisível, campo não mapeado. Sem ela, as asserções sobre o entry poderiam estar
passando por acidente e ninguém saberia distinguir a cura do defeito.

Os seis dublês aprenderam a doutrina no mesmo commit: nascem com
`no_show_all=True` como o glade, `show()` para na caixa, e só `show_all()`
desarmado marca `filhos_visiveis`.

---

## Os irmãos do glade: por que só este box adoeceu

**Grau: MEDIDO**, por varredura do `main.glade`.

O `main.glade` tem **dez** widgets com `no-show-all=True`. Só **três** são
recipientes com filhos, e os outros dois estão imunes por motivos diferentes:

| widget | por que não adoeceu |
|---|---|
| `trigger_left_preset_row` (`:689`) | cada filho declara `visible=True` no glade, e o segmentado inserido em tempo de execução leva `show_all()` explícito (`triggers_actions.py:132`) |
| `trigger_right_preset_row` (`:847`) | idem |
| `btn_migrate_to_systemd` (`:2315`) | o rótulo é **propriedade** do botão, não um objeto filho — não há em que descer |
| `profile_game_entry_box` (`:2049`) | **os dois filhos não declaram `visible`**: dependiam da descida do `show_all()` da janela |

Os seis restantes são `GtkLabel` e `GtkScale` sem filhos.

Ou seja: o box do editor de perfis era o **único** que dependia do `show_all()`
da janela para mostrar o próprio conteúdo. Isso explica por que o defeito é
único — e não impede o próximo, porque **nada no repositório cobra** que um
filho de box com `no-show-all` declare o próprio `visible`.

---

## O que a foto de rotina NÃO mostra

**Grau: MEDIDO**, lendo o PNG de 06/08 às 02:48.

A casa manda fotografar antes e depois
([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)),
e o `retratar_abas.py` é o instrumento. Só que em `docs/usage/assets/readme_perfis.png`
o rótulo **"Aplica a:"** aparece com **nada embaixo** — o seletor é montado em
código (`_build_profiles_tab`), e o retrato monta o glade mais o card do
controle, não a aba Perfis inteira.

Consequência honesta: **este defeito e esta cura são invisíveis na foto de
rotina**. Não há retrato do antes nem do depois. O que existe de prova visual é
o teste de GTK real, que mede o `get_visible()` e o `get_mapped()` do campo — e
isso responde "apareceu?", não "ficou bom?".

---

## O que fica ABERTO

- **A grafia dupla continua no produto.** `profiles_actions.py:1067` ainda diz
  `CAMPO-QUE-NAO-NASCE-01`, e é a única ocorrência dessa forma. Unificar é uma
  palavra num comentário; a decisão é dela, e a mensagem do commit `0bb92a5`
  não tem como ser reescrita. **Grau: MEDIDO** (o custo de busca), **SEM PROVA**
  de que unificar o comentário não quebre alguma referência que ninguém enxergou.

- **A cura desarma o `no_show_all` para sempre, e isso tem efeito colateral
  medido.** Depois do primeiro clique em "Jogo da Steam", o box perde a proteção
  que o glade lhe dava. Reproduzido em 06/08 sobre o glade real, numa
  `OffscreenWindow`:

  | passo | `box.visible` | `entry.visible` | `no_show_all` |
  |---|---|---|---|
  | abertura | False | False | True |
  | após "Jogo da Steam" | True | True | False |
  | após "Qualquer" | False | True | False |
  | após um `show_all()` na janela | **True** | True | False |

  E `App.show_window()` é exatamente `self.window.show_all()` + `present()`
  (`app.py:638`) — o caminho da bandeja, do `SIGUSR1` e do botão "Abrir Hefesto"
  das notificações. **Grau: MEDIDO** para o mecanismo em bancada; **SUSPEITA COM
  MECANISMO** para o que chega à tela dela — a janela inteira não foi exercitada,
  e a linha só reaparece se ela tiver passado por "Jogo da Steam" antes. O efeito
  é um campo "Nome do jogo:" órfão sob "Qualquer" — e a
  [JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md)
  já tinha registrado esta mesma classe noutro widget. Nenhum teste cobre este
  caminho hoje.

- **O `filhos_visiveis` dos dublês não é cobrado por ninguém.** Os seis dublês
  aprenderam a doutrina e passaram a marcar o atributo, mas **nenhuma asserção
  da suíte o lê** — a única menção fora das definições está num docstring.
  **Grau: MEDIDO** (`git grep`). É por isso que os 122 casos seguem verdes com o
  defeito de volta: a doutrina dos dublês impede que eles **mintam**, não que
  eles **deixem passar**.

- **Não há portão contra o próximo box igual.** Um `no-show-all=True` novo, com
  filhos que não declarem `visible`, repete o defeito inteiro e nenhum
  verificador reclama. Um validador de glade que cobrasse isso é barato e não
  existe. **Grau: MEDIDO** (a ausência), **SEM PROVA** de que valha a pena — não
  se mediu quantos falsos positivos ele produziria.

- **Ninguém confirmou com o olho dela.** A queixa é de 05/08 e a cura entrou às
  23h53 do mesmo dia; não há registro de ela ter dito que o campo apareceu.
  **Grau: SEM PROVA.** Enquanto isso não acontecer, o que a casa tem é um teste
  verde, e a regra é clara: interface só fecha com o olho dela.
