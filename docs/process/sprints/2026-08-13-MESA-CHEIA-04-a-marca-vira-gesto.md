# MESA-CHEIA-04 — a marca vira gesto, e o limite que a metáfora encontra

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Índice da leva:** [a mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** a [02](2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md)
- **Custo mínimo:** 3 h
- **Esta é a sprint que tem de dizer NÃO a uma parte do pedido dela**, e o não
  está medido.
- **O censo de 13/08 confirmou esta sprint inteira** e lhe deu nome: ela é a
  **opção híbrida da D-3** — a faixa mostra os quatro, e clicar num troca o
  alvo. O caminho de troca já existe (`_sync_edit_target`,
  `app/actions/status_actions.py:1901`) e já repopula as abas
  (`_refresh_target_tabs`, `:2036-2058`).

---

## 1. A falta, medida

Depois da 02, a tela **mostra** onde cada jogador está. Ela não deixa ninguém
**mover** nada: a única forma de trocar quem está sendo editado continua sendo o
chip do cabeçalho (`_on_target_button_toggled`,
`app/actions/status_actions.py:2182`).

A metáfora dela era outra: *"igual jogo quando selecionamos um personagem"*. Em
tela de escolher personagem, **cada jogador move o próprio cursor**.

## 2. O limite, e ele é medido — não é preguiça minha

**Quatro pessoas não movem quatro cursores com um mouse.** Isso é óbvio. O que
não é óbvio é se o produto poderia deixar cada um mover o cursor **com o próprio
controle**, e a resposta de hoje é: **não, e por dois motivos de fundo
diferente.**

### Motivo 1 — o input de navegação vem de um controle só

`core/backend_pydualsense.py:2193-2194`, no `read_state`:

> *"INPUT vem SEMPRE do controle PRIMÁRIO (`self._ds`). Emulação de
> mouse/teclado/gamepad é, portanto, single-controller por construção."*

A POR-UNIDADE-01 já tinha registrado essa mesma recusa em 10/08, para outra
pergunta: mouse e teclado não podem ser por peça porque há **um**
`_mouse_device` e **um** `_keyboard_device` no daemon.

### Motivo 2 — o input dos outros três chega, mas devagar e só numa aba

Isto é o que salva a ideia de ser impossível para sempre, e por isso está aqui:

- o `state_full` **traz `inputs` por controle**, inclusive `buttons`, e os
  secundários vêm de `CoopManager.live_snapshots()`
  (`daemon/ipc_handlers.py:2545-2553`, `daemon/subsystems/coop.py:257-263`);
- mas o tique que busca isso é o de **10 Hz**, e ele **só roda com a aba Status
  à vista** — com outra aba na frente ele devolve cedo
  (`app/actions/status_actions.py:2204-2212`);
- e o motivo do gate está escrito, com número: *"um poller cego já custou 104%
  de um núcleo nesta casa"* (`app/actions/status_actions.py:769-774`).

**Conclusão honesta:** "cada jogador move o próprio cursor com o próprio
controle" não é impossível — é uma sprint de **input**, não de tela, e ela paga
um tique de 10 Hz numa aba que hoje não tem nenhum. **Não está nesta leva.** Se
ela quiser, vira uma sprint própria, com o custo de CPU medido antes.

### Motivo 3 — o censo de 13/08 acrescentou um terceiro, e ele é pior

**O comando do PC troca de dono sozinho, em silêncio.** Se o primário cai,
`_recompute_primary` promove o próximo mais antigo
(`core/backend_pydualsense.py:1943`), re-atrela o evdev (`:1955`) e escreve um
`logger.info` que ninguém lê (`:1969`). O cursor passa a obedecer **outro
controle** no meio do uso, e nada na tela diz isso.

E o critério de quem é o primário é **ordem de plugar**, não número de jogador:
`next(iter(self._handles))` (`core/backend_pydualsense.py:1944`), com o docstring
dizendo *"Primário = 1ª chave de inserção ainda presente"* (`:1937-1944`). Com
quatro na mesa, *"Controle 1"* no seletor e *"quem move o cursor"* podem ser
aparelhos diferentes, e **nada na janela permite descobrir qual é qual**.

**Por que isto entra numa sprint sobre gesto:** a metáfora dela é escolher
personagem, e escolher personagem pressupõe saber quem é você. O censo propôs a
resposta honesta e ela é a **D-10**: em vez de *"cada um escolhe o seu"*, a
Navegação passa a dizer *"quem comanda o PC agora: Controle N"*, na cor dele,
com aviso quando o comando troca de dono. O dado já chega — `is_primary` sai de
`describe_controllers` (`core/backend_pydualsense.py:3984`). **Não está nesta
sprint**, e está registrada na onda 2 do índice.

---

## 3. O que muda na tela nesta sprint

O que **cabe** hoje: a marca deixa de ser só desenho e vira **atalho**.

```
   Clicar na marca ■3 dentro do botão "Galope"...
   ┌───────────┬───────────┬───────────┐
   │Resistência│Arco flecha│  Galope   │
   │           │           │        ■3 │  <- clique aqui
   └───────────┴───────────┴───────────┘

   ...faz duas coisas, e só estas duas:
   1. o cabeçalho passa a "Ajustes vão para: [■ Sony 3 · BT]"
   2. a grade repinta com a moldura no modo do jogador 3

   NÃO faz: mudar o modo de ninguém. Clicar na MARCA seleciona o jogador;
   clicar no BOTÃO continua escolhendo o modo — para o alvo atual.
```

Essa separação é a decisão de desenho inteira desta sprint: **a marca é quem, o
botão é o quê.** Um clique que fizesse as duas coisas ao mesmo tempo trocaria o
gatilho de alguém por engano — e essa é a classe de defeito que a ABAS-06 curou
em 25/07 (o "Desligar" que zerava o gatilho dos quatro, citado em
`daemon/ipc_handlers.py:960-967`).

E ganha um caminho de teclado, porque a fita do cabeçalho tem um e a marca não
pode ter menos: `Tab` chega à marca, `Enter` seleciona.

---

## 4. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_04_a_marca_seleciona.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — o clique que troca o modo junto

**Arrancar:** deixar o clique na marca propagar para o `toggled` do botão do
modo.

**Por que reprova:** o dublê tem o alvo em "Todos" e o jogador 3 em "Galope".
Clicar na marca `■3` com a propagação viva grava "Galope" no **global** — o
teste assere que `draft.triggers` não mudou e que só `_edit_target_uniq` mudou.
Sem `stop_emission`, reprova.

### Mordida 2 — a seleção que não chega ao daemon

**Arrancar:** setar `_edit_target_uniq` direto, sem passar pelo caminho que o
chip usa.

**Por que reprova:** o chip do cabeçalho não só marca o escalar — ele avisa o
daemon e mantém `output_target_index` em sincronia
(`app/actions/status_actions.py:2182-2199`). Sem isso, o próximo tique de 2 Hz
**reverte** a seleção, porque o sync com o daemon vence
(`_refresh_controller_target_combo`, `app/actions/status_actions.py:2060-2100`).
O teste roda um tique de sync depois do clique e exige que o alvo tenha ficado.

Esta mordida é a que importa: ela pega a versão "funciona no teste, pisca na
tela".

### Mordida 3 — o teclado

Arrancar o `set_can_focus` da marca: a asserção de que `Tab` alcança as quatro
marcas reprova.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **A marca é clicável, ou o cabeçalho continua sendo o único lugar?** Duas portas para o mesmo gesto é conveniência e também é ambiguidade | montar ou não montar |
| **Clicar na marca de um jogador que NÃO está na mesa (perfil com override de um controle desligado)?** Hoje esse jogador nem aparece — a 02 só marca os conectados | manter só os conectados, salvo pedido dela |
| **A metáfora completa — cada um com o próprio controle — vale a sprint de input?** O preço está na seção 2 | medir o custo de CPU antes de propor, se ela quiser |
| — | `stop_emission`, foco por teclado, e reusar o caminho do chip em vez de duplicá-lo |

---

## 6. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho:** as três mordidas, com dublê de GTK e um tique de sync
simulado.

**Só a bancada dela:** que o clique na marca **não escorrega** para o botão do
modo na tela de verdade — o COSMIC tem histórico de roubar foco no clique, e é a
razão de esta casa ter trocado combos por botões segmentados
(`app/widgets/segmented_selector.py:1-6`, cosmic-epoch#2497). Um clique que
troca o gatilho de alguém por engano é pior que não ter o atalho.
