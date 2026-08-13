# MESA-CHEIA-06 — o portão contra a marca que mente

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a [02](2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md)
  (o portão precisa do primeiro caso real para não travar um formato imaginário)
- **Custo mínimo:** 3 h
- **Quem valida é o CI, não ela** (regra da
  [RÓTULOS-DE-SPRINT-01](2026-08-09-ROTULOS-DE-SPRINT-01-entregue-no-codigo-nao-e-validado-por-ela.md)).

---

## 1. O risco, medido

> **CORREÇÃO DE 13/08/2026, pelo censo das dez abas.** A versão anterior desta
> sprint tratava *"a marca"* como **uma coisa só** e concluía que ela cabe em
> três abas de dez. **São DUAS coisas, e elas têm alcances diferentes** — o
> texto foi substituído porque a confusão entre as duas é justamente o erro que
> este portão existe para impedir.
>
> | a marca | o que ela afirma | onde cabe |
> |---|---|---|
> | **a COR por jogador** (o swatch) | *"este pedaço da tela é do jogador N, e a barra dele está desta cor"* | **NOVE abas de dez** — é identidade, não ajuste. A "No jogo" já é um painel por controle e só não tem cor |
> | **as QUATRO ESCOLHAS** (a marca `■N` num botão) | *"o jogador N escolheu esta opção"* | **TRÊS abas** — Gatilhos, Lightbar e Rumble. Nas outras o ajuste é da sessão ou do perfil, e quatro marcas ali seriam mentira |
>
> **A linha da "No jogo" mudou de lado por medição, não por gosto:** ela reusa
> `titulo_do_card` (`app/widgets/painel_no_jogo.py:468`) e as mesmas chaves da
> Status, e `grep -c 'lightbar\|accent\|swatch\|player_slot'` no arquivo devolve
> **0**. Ela é um painel por controle **sem cor** — a cópia que a casa começou e
> não terminou. É a
> [MESA-CHEIA-07](2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md).

Ela disse *"isso valeria pra todas as abas"*. A leva vai entregar **cor** em
nove abas e **escolha marcada** em três, e a razão de cada limite **já está
medida** — mas não está **travada**. Um portão é a diferença.

### Quais abas honram o alvo hoje, contado

O alvo de edição é `_edit_target_uniq`
(`app/actions/status_actions.py:427`). Quem o lê, na árvore inteira de `src/`:

| aba | módulo | honra o alvo? | **cor?** | **escolha marcada?** | endereço |
|---|---|---|---|---|---|
| Status | é a **dona** do alvo | — | **já tem** | não (é o molde) | `app/actions/status_actions.py:427` |
| Gatilhos | `triggers_actions.py` | **sim** | sim | **SIM** | `:164-166` |
| Lightbar | `lightbar_actions.py` | **sim** | sim | **SIM** | `:230-237` (`_edit_uniq`) |
| Rumble | `rumble_actions.py` | **sim, no rascunho** | sim | **SIM** | `:505-514` (`_rumble_edit_uniq`) — o pulso ao vivo obedece; a intensidade não: é a [05](2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md) |
| **No jogo** | `painel_no_jogo.py` | não — e não precisa | **SIM** | não | já é um painel por controle (`:468`), sem uma linha de cor |
| Início | `home_actions.py` | **não** | **SIM** (cards de controle) | não | zero leituras do alvo; `lightbar_rgb` chega e é descartado |
| Perfis | `profiles_actions.py` | **não** | **SIM** (as faces guardadas) | não | `grep -c uniq` = **0** em **3357** linhas |
| Navegação | `mouse_actions.py`, `input_actions.py` | **não** | **SIM** (quem comanda o PC) | não — e o perfil **proíbe** | zero ocorrências nos dois |
| Emulação | `emulation_actions.py` | **não** | não | não | as ocorrências de `uniq` ali são agrupamento de nós de `/dev/input`, não alvo de edição |
| Sistema | `daemon_actions.py` | **não** | contagem, não cor | não | o alvo é systemd/Steam/PipeWire |

**Escolha marcada: três abas.** **Cor: nove de dez** — só a Sistema fica de
fora, e mesmo ela ganha **contagem** em vez de singular
([MESA-CHEIA-11](2026-08-13-MESA-CHEIA-11-a-janela-conta-um-quando-sao-quatro.md)).

E `_refresh_target_tabs` (`app/actions/status_actions.py:2036-2058`) lista
exatamente três métodos de repintura — é a lista viva de quem muda quando o alvo
muda, e ela bate com a coluna "escolha marcada".

### Por que as outras sete não marcam ESCOLHA — e cada motivo tem data

Nenhum destes é julgamento meu:

- **Início e Emulação** — *"modo e máscara são da SESSÃO, não da peça de
  plástico"*: decisão dela, 10/08/2026, POR-UNIDADE-01 §2;
- **Navegação** — medido no código: há **um** `_mouse_device` e **um**
  `_keyboard_device`, alimentados por um `read_state()` por tique, e o
  `read_state` diz *"INPUT vem SEMPRE do controle PRIMÁRIO"*
  (`core/backend_pydualsense.py:2193-2194`);
- **Perfis** — `name`, `match` e `priority` são a identidade do perfil, não
  configuração de peça (POR-UNIDADE-01 §2);
- **Sistema** — não é seção de perfil;
- **No jogo** — é painel de leitura: mostra o que está acontecendo, não oferece
  escolha. **Ganha cor e não ganha marca de escolha**, e a distinção entre as
  duas coisas é o assunto deste portão.

**O risco em uma frase:** nada impede alguém de, daqui a dois meses, achar que
"vale para todas as abas" significa quatro marcas na aba Início — e entregar
uma tela em que quatro jogadores parecem ter quatro modos, quando o modo é um
só. Seria a mesma classe de defeito que a POR-UNIDADE-01 chamou de *"campo
aceito-e-ignorado vira comportamento errado silencioso meses depois"*.

---

## 2. O que muda

Nada na tela. Muda o CI.

O portão é um teste — não um script novo. A casa já tem dez scripts de portão e
esta pergunta não precisa de um décimo primeiro: ela se responde lendo o próprio
código-fonte da janela, por AST, como o `validar-referencias-docs.py` já faz
para ler o `_handlers` do servidor IPC.

```
   O que o portão lê                    O que ele cobra
   ┌───────────────────────┐   ┌──────────────────────────────────────────┐
   │ app/actions/*.py      │──▶│ 1. Aba que marca ESCOLHA tem de LER o    │
   │  quem chama           │   │    alvo (`_edit_target_uniq`)             │
   │  marcas_do_lado /     │   │                                          │
   │  previas_da_mesa /    │──▶│ 2. Aba na lista de RECUSA não pode        │
   │  _edit_target_uniq    │   │    marcar ESCOLHA — e PODE ter COR        │
   └───────────────────────┘   │                                          │
   ┌───────────────────────┐   │ 3. Cada linha da tabela tem veredito nas  │
   │ a tabela da §1        │──▶│    DUAS colunas, com motivo e data        │
   │ (cor × escolha)       │   │                                          │
   └───────────────────────┘   │ 4. A cor sai de UMA função só — nenhuma   │
   ┌───────────────────────┐   │    aba reimplementa a regra do card       │
   │ o `main.glade`        │──▶│                                          │
   │ (as dez páginas)      │   │ 5. Aba nova sem veredito REPROVA          │
   └───────────────────────┘   └──────────────────────────────────────────┘
```

**A asserção 2 é a que a correção de 13/08 acrescentou, e ela é a mais fácil de
errar nos dois sentidos:** um portão que proíbe *"marca"* sem distinguir cor de
escolha impediria a "No jogo" de ganhar a cor que lhe falta — reprovaria a cura.
Um portão que permite *"marca"* sem distinguir deixaria a Início mostrar quatro
modos quando o modo é um só.

**E a asserção 4 é a lição da cópia inacabada:** a "No jogo" copiou o título
chamando `titulo_do_card` e não reimplementando; a cor tem de entrar pela mesma
porta, ou a casa passa a ter dois donos da verdade sobre "a cor dele" **dentro**
da própria janela — que é o risco da **D-1** repetido num andar mais baixo.

E uma sexta asserção, que não é sobre abas e é sobre a armadilha que mais
assusta esta leva:

**6. A lista de controles da janela nunca inclui virtual.** O Steam Input cria
um espelho Xbox de cada controle que vê, inclusive do nosso vpad
([TRES-CONTROLES-01](2026-08-10-TRES-CONTROLES-01-o-espelho-do-espelho-no-pragmata.md)).
Hoje isso **já está resolvido**: `discover_external_gamepads` exclui tudo sob
`/devices/virtual/`, e a docstring nomeia os vpads do Steam Input
(`core/evdev_reader.py:739-742`). Uma tela que mostra "os quatro jogadores"
com um espelho no meio mostraria cinco, e ninguém saberia qual apagar.

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_06_a_marca_nao_mente.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — a marca na aba errada

**Arrancar:** acrescentar uma chamada a `marcas_do_lado` em
`app/actions/home_actions.py` (a aba Início).

**Por que reprova:** a asserção 2. O portão lê os módulos de aba por AST, acha
a chamada num módulo da lista de recusa e reprova com o motivo datado
("modo e máscara são da SESSÃO — decisão dela, 10/08/2026").

**Esta é a mordida principal.** Ela é o portão inteiro: sem ela, a tabela desta
sprint é prosa.

### Mordida 2 — a marca sem alvo

**Arrancar:** tirar a leitura de `_edit_target_uniq` de `triggers_actions.py`,
deixando a marca desenhada.

**Por que reprova:** a asserção 1 — uma aba que mostra quatro estados e não sabe
qual deles está sendo editado desenha quatro seleções e nenhum foco. É o defeito
que a sprint 02 evita com a moldura.

### Mordida 3 — o portão que confunde COR com ESCOLHA

**Arrancar:** escrever o portão contra *"marca"* sem distinguir as duas colunas,
e acrescentar o swatch da cor na aba "No jogo".

**Por que reprova:** este é o teste do teste, e ele morde nos **dois** sentidos.
(a) Com o portão indistinto, a cor legítima da "No jogo" — que é a
[MESA-CHEIA-07/E2](2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md) —
**reprova**, e um portão que reprova a cura é pior que portão nenhum. (b) Com o
portão indistinto no outro sentido (permitir tudo), uma marca `■N` na Início
**passa**. O teste exige as duas: cor na "No jogo" **aprova**, escolha na Início
**reprova**.

**Esta mordida entrou em 13/08 e é a razão de a sprint ter sido reescrita.**

### Mordida 4 — a cor reimplementada

**Arrancar:** escrever uma segunda função de cor num módulo de aba, em vez de
chamar a do card.

**Por que reprova:** a asserção 4. O portão conta as definições de "regra de cor
por controle" em `src/` e exige **uma**. A casa já tem dois donos da verdade
sobre a cor — o `lightbar_rgb` do `state_full` e o `player_slot_color`
(`core/led_control.py:158-164`) — e essa divergência é a **D-1**. Um terceiro
dono, dentro da própria janela, seria o mesmo erro num andar mais barato de
evitar.

### Mordida 5 — o espelho de volta na conta

**Arrancar:** tirar o filtro `_is_virtual_evdev` de `discover_gamepads`
(`core/evdev_reader.py:621` na docstring, `:659` no laço).

**Por que reprova:** o dublê de `/sys` tem um nó sob `/devices/virtual/` com
caps de gamepad (o espelho `28de:11ff` que a TRES-CONTROLES-01 mediu no
`/dev/input` dela). A asserção 6 exige que a lista da janela continue com
quatro entradas, não cinco.

### Mordida 6 — a lista que envelhece calada

**Arrancar:** acrescentar uma aba nova ao notebook sem entrada na tabela.

**Por que reprova:** o portão compara a lista de páginas do
`src/hefesto_dualsense4unix/gui/main.glade` com a tabela; aba sem veredito nas
**duas** colunas reprova. **Isto não é hipótese:** foi exatamente assim que a
*"No jogo"* (`gui/main.glade:678`) atravessou um censo de dez agentes sem ser
medida — a lista de abas que eu entreguei tinha nove nomes, e nada no
repositório a conferiu.

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **A tabela das duas colunas está certa?** Cor em nove abas, escolha em três — cada linha com motivo e data. Se ela quiser escolha marcada em alguma das sete, a decisão de 10/08 é revista, e é dela | escrever a tabela que ela aprovar, com a data de cada veredito ao lado |
| **A distinção cor × escolha se sustenta como vocabulário?** Ela nasceu do censo de 13/08 e é minha, não dela. Se as duas palavras não se distinguirem na cabeça de quem lê o portão, o portão vira ruído | renomear para o par que ela preferir; o mecanismo não muda |
| **O portão reprova ou avisa?** Reprovar trava; avisar apodrece | reprovar, salvo palavra dela — é o padrão dos dez portões da casa |
| — | o teste por AST, os dublês, e a entrada no `.pre-commit-config.yaml` e no CI, junto dos portões que já existem |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: tudo.** Este é o único item da leva que fecha sozinho — é
teste sobre código-fonte, sem GTK, sem daemon e sem controle.

**A bancada dela não fecha nada aqui**, e isso é de propósito: portão que espera
a mão dela para valer não é portão.

---

## 6. Por que este portão vem DEPOIS, e não antes

Escrever o portão antes da sprint 02 travaria um formato que ainda não existe —
o nome da função de marca, a forma da lista, o jeito de a aba declarar que
desenha marca. Um portão escrito contra uma API imaginária cobra a API
imaginária, e é o que a casa chama de contorno.

A ordem certa é: a 02 entrega o primeiro caso real, e a 06 congela o que ele
provou.
