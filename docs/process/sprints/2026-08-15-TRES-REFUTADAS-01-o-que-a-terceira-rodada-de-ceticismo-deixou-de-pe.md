# TRÊS-REFUTADAS-01 — o que a terceira rodada de ceticismo deixou de pé

- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf`.
- **Grau:** **MEDIDO.** Cada defeito abaixo foi reproduzido por um cético que
  refez as mordidas por conta própria, com saída de terminal colada no relatório.
  Nada aqui é leitura de código sem execução.
- **Depende de:** nada. As três entregas de onde estes defeitos vieram **já estão
  commitadas** (`4d9e992` e `410d1e1`) e o que fica de pé é o resíduo.
- **Custo mínimo:** 4 h 30 (três frentes, a mais cara de 2 h)

---

## Como ler

A onda 1 da MESA CHEIA teve onze entregas, cada uma julgada por um cético
independente, depois consertada, depois julgada de novo, e depois uma terceira
vez. **O placar final foi 4 sustentadas (1.1, 1.2, 1.6, 1.7) e 3 refutadas.**

Esta sprint é só das três refutadas. Cada uma tem **o defeito medido**, **o que
já está de pé e não se refaz**, e **a mordida que falta**.

**O que é comum às três, e vale mais que qualquer uma delas:** em todas, a cura
de produto está certa e o que caiu foi a **justificativa escrita para não olhar o
resto**. Esse padrão tem documento próprio —
[A-LINHA-QUE-DISPENSA-01](2026-08-15-A-LINHA-QUE-DISPENSA-01-o-defeito-mora-onde-a-autora-escreveu-que-nao-precisava-olhar.md).

---

## 1. A 1.5 — a frase que soma as pendências é CORTADA na tela

### 1.a O defeito, medido

A frase de guardado passou a somar as pendências em vez de escolher uma
(`app/textos_de_aplicacao.py`, `frase_de_guardado`). A cura está certa. **A
frase não cabe.**

Medido com `Gtk.OffscreenWindow` sob `xvfb-run`, com o `theme.css` da casa
carregado e a fonte do sistema dela (`Fira Sans`, lida de `gsettings`), com o
rodapé forçado à largura padrão da janela:

```
rodapé 1180 px   →   statusbar 711 px   →   rótulo 703 px
                     footer_buttons_box  415 px  (quatro botões)

frase de DUAS pendências: 182 caracteres, 993 px
cabem: 127 caracteres
```

O que aparece na tela:

```
Desenho das luzes (LEDs acesos: 1, 3 e 5) — guardado: com o co-op ligado,
quem manda nas 5 luzes é ele; o Controle 2 não está n
```

**O que some inteiro é `"Vale quando o co-op sair e o Controle 2 voltar."`** — a
metade que diz **o que ela precisa fazer**. O rótulo da `GtkStatusbar` tem
`ellipsize: PANGO_ELLIPSIZE_END`, `line wrap: False`, `max_width_chars: -1`
(lido no widget).

**E este é o estado NORMAL da mesa dela**, não o pior caso: co-op ligado (fica
ligado) + alvo fora da mesa (a R-16 mantém o alvo justamente quando o controle
cai). A própria docstring do módulo o chama assim.

Os outros comprimentos, para dimensionar:

| combinação | caracteres | cabe? |
|---|---|---|
| uma pendência | 69 | **sim**, a única |
| co-op + alvo fora (a normal) | 182 | não — perde a liberação inteira |
| a trinca (co-op + Nativo + alvo fora) | 250 a 256 | não |
| a trinca com o prefixo `_AVISO_D4` | **314** | não |

O prefixo `_AVISO_D4` não é hipótese: o próprio método o compõe
(`app/actions/lightbar_actions.py:816-817` e `:1109-1110`).

### 1.b O erro de medição, e ele está GRAVADO no repositório

A autora mediu a largura da **janela** e a chamou de largura da **barra de
status**. O `footer_box` (`gui/main.glade:3756-3833`) é uma `GtkBox`
**horizontal** com dois filhos: a `GtkStatusbar` e o `footer_buttons_box` com
«Aplicar», «Salvar Perfil», «Importar» e «Restaurar Default». **Os 415 px dos
botões nunca foram descontados.** O padding sai de `theme.css:1143`.

O erro é de **1,64x**, sempre para o lado otimista — e está escrito em
`tests/unit/test_mesa_cheia_09_toasts_honestos.py:315-323`, na docstring de
`TestAsPendenciasSomam`, com a instrução explícita de que serve *"para a decisão
não precisar ser remedida"*:

> *"Na largura padrão da janela (`default-width` 1180 no `main.glade`) cabem ~183
> caracteres"* · *"A de duas pendências cabe raspando (1123 px de 1156 px)"*

**Pela regra dela de 11/08, isto SAI por substituição** — *"substituir pela info
certa não seria melhor?"*. Não é decisão medida a preservar: é um número que a
medição derrubou, e mantê-lo obriga a próxima pessoa a escolher entre dois
números.

### 1.c O defeito que MUDOU DE LUGAR, e que ninguém relatou

A cadeia `if/elif` que a 1.5 veio matar **continua viva** em
`app/actions/triggers_actions.py:695-700`: `fora = alvo_fora_da_mesa(self)` é
calculado e **descartado** no ramo do Modo Nativo. Provado com o host do próprio
arquivo de teste dela (`_HostGatilhos`, alvo fora **e** Modo Nativo):

```
Gatilho esquerdo (L2): Rigid — guardado; em Modo Nativo quem manda no
controle é o jogo. Vale quando o Modo Nativo sair.
```

O controle está fora da mesa e a frase não diz. É exatamente a mentira que a 1.5
matou na aba Lightbar, viva na aba Gatilhos.

### 1.d As entregas da 1.5

| # | entrega | custo |
|---|---|---|
| **E1** | **A frase caber**: encurtar os motivos, ou levá-la para fora da statusbar. **É decisão dela** — §4 | 60 min |
| **E2** | **A medição errada sai** de `test_mesa_cheia_09_toasts_honestos.py:315-323`, substituída pela de hoje | 20 min |
| **E3** | O `if/elif` de `triggers_actions.py:695-700` passa a somar, como o da Lightbar | 25 min |

### 1.e O que já está de pé na 1.5, e não se refaz

`alvo_fora_da_mesa` sem a guarda do mapa vazio; o quinto gesto no
`on_lightbar_off`; `frase_de_guardado` somando; `com_artigo`; três testes novos
(26 → 29) e as cinco mordidas. **`git diff -- src/` do cético voltou vazio: a
cura de produto não precisa ser reescrita.**

---

## 2. A 1.4 — três estados opostos com a MESMA resposta

### 2.a O defeito, medido

`_destinos_do_broadcast` (`daemon/ipc_handlers.py:1046-1106`) devolve
`guardado_em: []` em três estados que significam coisas **opostas**. Medido
sobre `tests/fixtures/state_full_quatro_controles.json`, com a árvore intacta:

```
### A) MODO NATIVO, pedido SEM uniq, dois na mesa
   resposta: {'status':'ok', 'aplicado_em': [], 'guardado_em': []}
   _desired_default.trigger_left GUARDADO?  True
   handles ARMADOS?  [Rigid_A, Rigid_A]
   depois do DESMUTE, o gatilho chega?  [True, True]

### B) MESA VAZIA, pedido SEM uniq
   resposta: {'status':'ok', 'aplicado_em': [], 'guardado_em': []}
   _desired_default.trigger_left GUARDADO?  True
   depois do HOTPLUG o controle novo chegou ARMADO?  33

### C) alvo do seletor SEM MAC estável
   resposta: {'status':'ok', 'aplicado_em': [], 'guardado_em': []}
   _desired_by_uniq: {}
   _desired_default.trigger_left: None
```

**A e B guardaram e vão valer. C não guardou nada.** A tela recebe o mesmo
objeto nos três, e o terceiro estado é **irrepresentável**.

A resposta verdadeira de A estava a uma linha: a lista que a própria função já
calculou em `_uniqs_conectados()`.

### 2.b Isto contradiz o contrato publicado — nas duas direções

`docs/protocol/ipc-unix-socket.md:136` diz:

> `guardado_em` = *o override ficou REGISTRADO e vale DEPOIS: quando o controle
> voltar (hotplug) **ou quando o Modo Nativo sair (desmute)***

É exatamente o estado A, e a rota responde vazio.

E `ipc-unix-socket.md:137` — *"as duas VAZIAS = escrita global sem registro por
controle"* — era verdade **antes** do conserto e ficou **falsa depois**: com dois
na mesa fora do Modo Nativo, `trigger.set` sem `uniq` agora responde
`aplicado_em` com os dois MACs. **A contradição foi INTRODUZIDA pelo conserto e
não foi relatada.**

### 2.c O terceiro defeito: o ramo do seletor não confere conexão

O primeiro ramo da função filtra por `_uniqs_conectados()`; o ramo *"seletor
mirando um"* (`ipc_handlers.py:1100-1106`) **não confere**:

```
describe:            [('aabbcc0000d8', True), ('aabbcc000003', False)]
_uniqs_conectados:   ['aabbcc0000d8']
get_output_target_uniq: aabbcc000003
RESPOSTA:  {'status':'ok', 'aplicado_em': ['aabbcc000003'], 'guardado_em': []}
```

**É a D-9 ao contrário**: afirma escrita num MAC que a própria função filtrou
como fora da mesa. O estado é alcançável e está documentado no backend —
`core/backend_pydualsense.py:653-657` (`except OSError: self.connected = False;
break`, bloco QUEDA-QUE-PENDURA-01 de 04/08). O handle fica pendurado até o
reconcile, `_apply_trigger` só arma `h.triggerL.mode` sem I/O, e a thread que
escreveria **está morta**. Nenhum teste da casa combina `connected=False` com
`trigger.set`.

### 2.d A rota irmã continua mentindo, e a divergência só trocou de polaridade

```
### led.set SEM uniq em MODO NATIVO
   {'status':'ok', 'aplicado_em': ['aabbcc0000d8','aabbcc000003'], 'guardado_em': []}
### trigger.set SEM uniq no MESMO estado
   {'status':'ok', 'aplicado_em': [], 'guardado_em': []}
```

`apply_output_for` devolve `['registrado','registrado']` (nada saiu no fio) e
`_registrar_em_todos` **descarta a palavra do backend** e responde os dois MACs.
A motivação declarada da entrega — *"duas rotas irmãs, respostas opostas"* — não
foi alcançada: a divergência inverteu de lado.

### 2.e As entregas da 1.4

| # | entrega | custo |
|---|---|---|
| **E1** | `guardado_em` **preenchido** nos estados A e B — a lista já existe em `_uniqs_conectados()` | 45 min |
| **E2** | O ramo do seletor **conferir conexão**, como o primeiro ramo já faz | 25 min |
| **E3** | `_registrar_em_todos` **respeitar** a palavra do backend, e o `led.set` parar de afirmar sob mute | 50 min |
| **E4** | As duas linhas do contrato (`ipc-unix-socket.md:136` e `:137`) refeitas contra o comportamento de hoje | 15 min |

**Aviso para quem executar a E1:** vai ser preciso **apagar uma asserção que se
apresenta como decisão medida** —
`tests/unit/test_conserto_1_4_a_rota_classica_diz_onde_pegou.py:224-236`,
`test_em_modo_nativo_nao_diz_aplicado`, com a mensagem *"não há promessa POR
CONTROLE a publicar"*. Ela está errada, e o motivo está na §2.a.

---

## 3. A 1.11 — o QUARTO andar da escotilha do portão de frases

### 3.a O defeito, medido

O portão que impede a tela de dizer *"o controle"* quando são quatro tem uma
escotilha que já foi fechada três vezes, e ela continua aberta no quarto andar.

`oracoes_ofensoras`
(`tests/unit/test_mesa_cheia_11_a_janela_conta_quatro.py:741`) é:

```python
SINGULAR_RE.search(_sem_as_marcas(s)) and _justificado(s) is None
```

A marca passou a ser apagada antes da pergunta — mas **`_justificado(s)`
continua sendo literalmente `marca in s` sobre a oração CRUA**, com as 17 marcas
vivas de `SINGULAR_LEGITIMO`. Uma oração única que traga uma exceção viva **mais**
um *"o controle"* sem dono **isenta a si mesma inteira**.

A docstring de `_sem_as_marcas` (`:735-736`) declara esse andar morto ao dizer
que ele *"é o terceiro andar do mecanismo, e o **ÚNICO QUE SOBRAVA**"*.
**Medida-falsa.**

### 3.b A prova: quatro frases plantadas, uma reprovou

Plantadas no `.glade` de verdade, em quatro propriedades traduzíveis do
`btn_footer_apply`. **A mesma mentira nas quatro; muda só o que une as duas
orações:**

```
plantada-e:       "…ao controle selecionado e os gatilhos e a vibração vão para o controle."
plantada-mas:     "…ao controle selecionado mas os gatilhos e a vibração vão para o controle."
plantada-porque:  "…ao controle selecionado porque os gatilhos e a vibração vão para o controle."
plantada-virgula: "…ao controle selecionado, e os gatilhos e a vibração vão para o controle."
```

Saída:

```
E  AssertionError: orações no singular sem justificativa em SINGULAR_LEGITIMO:
E      btn_footer_apply.plantada-virgula: e os gatilhos e a vibração vão para o controle.
1 failed, 68 deselected in 0.33s
```

**Uma de quatro.** `oracoes()` devolve **1** para um período com duas orações
coordenadas por conjunção nua (`e`, `mas`, `porque`, `que`), e **2** só quando há
vírgula.

E a prova aditiva, com o léxico real da casa, no tooltip `player_leds_apply`:

```
"Mostra a bateria do controle e manda os gatilhos e a vibração para o controle."
     ^ exceção viva de SINGULAR_LEGITIMO      ^ a frase nº 1 da própria sprint

71 passed in 0.53s      ← setenta e uma verdes com a mentira na tela
```

O teste novo dela mede **a um caractere do buraco**: `:991` planta
`"Mostra a bateria do controle, e {MENTIRA}."` — **com** vírgula acusa, **sem**
fica em silêncio.

### 3.c O número novo que o próprio conserto errou

O comentário de `ORACAO_RE` (`:550-555`) afirma *"a UNIÃO, que é o número
honesto, é **135**"*. Recontagem:

```
trechos 470 | vírgula 88 | travessão 34 | '(' 42     (todos CONFEREM)
UNIÃO REAL dos três declarados = 139        ← o comentário diz 135
conjunto do regex `fraca` do teste          = 135
```

**135 é a contagem de um predicado diferente** (exige travessão espaçado e aceita
parêntese de fechamento). Cinco números "reescritos" descrevem dois conjuntos
diferentes costurados numa frase só. É a **terceira** contagem para a mesma
grandeza em três relatórios (164 → 135 → 139).

### 3.d A cura que falta, e os dois céticos concordam nela

**Parar de isentar a UNIDADE e passar a isentar só a OCORRÊNCIA.** Para cada
casamento de `SINGULAR_RE`, perguntar se **aquele trecho** faz parte de uma
marca — em vez de perguntar se a marca existe em algum lugar do recorte.

O mínimo aceitável, se a ocorrência for cara: `_justificado` perguntar sobre o
texto **sem** as marcas, igual ao que `oracoes_ofensoras` já faz do outro lado.

### 3.e As entregas da 1.11

| # | entrega | custo |
|---|---|---|
| **E1** | `_justificado` por **ocorrência**, não por unidade | 55 min |
| **E2** | O número do comentário de `ORACAO_RE` substituído, com o predicado declarado | 15 min |
| **E3** | O teste das quatro conjunções nuas, plantado e permanente — não como experimento de rodada | 30 min |

---

## 4. O teste que MORDE

### Mordida 1 — a frase que não cabe (1.5)

**Arrancar:** encurtar a frase e não medir a largura.

**Por que reprova:** teste novo, em `tests/unit/test_a_frase_cabe_na_barra.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->
Ele mede o rótulo real da `GtkStatusbar` sob `Gtk.OffscreenWindow` — **nunca
`Gtk.Window`**, que fica 1x1 sem gerenciador de janelas — com o `theme.css`
carregado, e exige que **as sete combinações** que `frase_de_guardado` produz
caibam. Hoje seis das sete reprovam.

**A ressalva de método, e ela é real:** medir texto é medir fonte, e a fonte do
CI não é a dela. O teste tem de declarar a fonte que usou e falhar com a margem
explícita, não com um número mágico.

### Mordida 2 — os três estados que voltam a ser um (1.4)

**Arrancar:** preencher `guardado_em` só no Modo Nativo e deixar a mesa vazia
vazia.

**Por que reprova:** o teste roda os **três** estados e exige **três respostas
distinguíveis**. Preencher um só faz A e B se separarem de C mas continuarem
iguais entre si — e a tela precisa dos três, porque *"vai valer no desmute"* e
*"vai valer no hotplug"* pedem esperas diferentes dela.

### Mordida 3 — a conjunção nua (1.11)

**Arrancar:** curar só a vírgula, de novo.

**Por que reprova:** as quatro frases da §3.b entram **no arquivo de teste**, e
as quatro têm de acusar. É a mordida que impede o quinto andar: qualquer cura que
continue perguntando *"a marca aparece aqui?"* passa em uma e reprova em três.

### O que estes testes NÃO provam

Que as frases novas são boas, e que a frase encurtada da 1.5 diz o que ela
precisa. Palavra de tela é dela.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **A 1.5 é a única que trava numa palavra dela.** A frase de duas pendências tem 182 caracteres e cabem 127. **Encurtar o texto** (perder detalhe) ou **tirar a frase da statusbar** (um lugar novo na tela)? | escrever a que ela escolher, e medir a que ela escolher |
| Se for encurtar: o que sai primeiro — o **motivo** (*"quem manda nas 5 luzes é ele"*) ou a **liberação** (*"Vale quando…"*)? A medição diz que hoje some a liberação, que é a parte acionável | propor cortar o motivo, salvo palavra dela |
| — | a 1.4 inteira, a 1.11 inteira, e as três mordidas |

**A 1.4 e a 1.11 não precisam dela.** São correção de resposta de protocolo e de
régua de teste: nenhum pixel novo, nenhuma palavra de tela.

---

## 6. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: quase tudo.** A 1.4 se prova com dublê sobre a fixture de quatro
controles; a 1.11 é varredura de texto; a 1.5 se prova sob `xvfb-run` com
`Gtk.OffscreenWindow`.

**Só a bancada dela:** que a frase escolhida na §5 **cabe na tela dela**, com a
fonte dela e o tema dela — foto antes e depois, por PROVA-DE-TELA-01. O
instrumento sob Xvfb é a régua; o olho dela é o veredito.
