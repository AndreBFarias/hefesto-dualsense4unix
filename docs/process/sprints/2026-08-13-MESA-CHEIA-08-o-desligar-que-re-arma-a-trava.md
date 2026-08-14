# MESA-CHEIA-08 — o "Desligar" que re-arma a trava que acabou de soltar

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Índice da leva:** [as ondas da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** nada. **É a primeira coisa a consertar depois de medir.**
- **Custo mínimo:** 40 min
- **É regressão de cura**, não defeito novo: a **R-19** está desfeita, e o teste
  que a protege **não morde**

---

## 1. O defeito, medido — degrau a degrau, e cada degrau foi aberto

O botão **"Desligar"** da aba Gatilhos existe para **soltar** a trava manual que
pausa a troca automática de perfil. É o que o próprio docstring dele promete
(`app/actions/triggers_actions.py:549-563`), com todas as letras:

> *"Botão «Desligar» — LIBERA a trava, não a re-arma (R-19). (…) o botão que a
> usuária usa para «voltar ao normal» era mais um jeito de PAUSAR a troca
> automática de perfil, sem nada na tela dizendo isso."*

**Ele solta, e 300 ms depois re-arma.**

```
  _reset_trigger  (app/actions/triggers_actions.py:549)
        │
        ├─ :567   combo.set_active_id("Off")
        │           │
        │           └─ SegmentedSelector.set_active_id EMITE "changed"
        │              (app/widgets/segmented_selector.py:139-152; o docstring
        │               diz "Ativa o botão do id e EMITE «changed»", e :152 é
        │               a chamada a _emit_changed)
        │                    │
        │                    └─ _on_mode_changed (:221)
        │                         └─ :239  _schedule_live_preview
        │                              └─ :249  GLib.timeout_add(300, ...)
        │
        └─ :570   trigger_reset(...)  ──▶  daemon LIMPA a trava
                                           clear_manual_trigger_active("trigger")
                                           (daemon/ipc_handlers.py:994)

                         300 ms
        ─────────────────────────────────────────────────────────────▶
              _fire_live_preview → _apply_trigger → trigger.set
                                    │
                                    └─ mark_manual_trigger_active("trigger")
                                       (daemon/ipc_handlers.py:957)
                                          ◀── A TRAVA VOLTA
```

**Ressalva honesta, e ela importa para o teste:** se o modo já estava em `"Off"`,
o `set_active_id` é no-op — `app/widgets/segmented_selector.py:139-152` só emite
quando o id **muda**. O caso que dói é o normal: aplicar "Rígido" e depois
"Desligar".

**Como ela sente isto:** *"a config que eu deixo não fica"* — o perfil não volta
a trocar sozinho depois do botão que promete "voltar ao normal", e nada na tela
diz por quê. É a queixa histórica que a R-19 tinha curado.

### 1.1 E o teste que deveria proteger passa por dois desvios do dublê

`tests/unit/test_triggers_actions.py:545` assere exatamente a coisa certa:

    assert mixin._trigger_set_calls == [], (
        "trigger.set aqui re-armaria a trava que o botão deveria soltar"
    )

**E passa com o defeito de pé**, por dois motivos independentes, os dois no
dublê:

| o desvio | onde | o que ele apaga |
|---|---|---|
| o `set_active_id` do dublê **não emite** `"changed"` — o corpo inteiro é `self._active_id = the_id` | `tests/unit/test_triggers_actions.py:274-275` | o primeiro degrau: sem "changed" não há `_on_mode_changed` |
| `GLib.timeout_add` é `lambda *_a, **_kw: 0` | `tests/unit/test_triggers_actions.py:385` | o último degrau: o timer nunca dispara |

Qualquer um dos dois, sozinho, já faz o teste passar. **Um teste que passa com a
cura arrancada não testa nada** — é a regra desta casa, e este é o exemplo dela.

---

## 2. O que muda

**Nada na tela.** Muda o comportamento invisível: depois do "Desligar", a troca
automática de perfil **volta a acontecer**.

O conserto tem dois lados e é decisão de desenho qual deles vale — as duas
opções estão na seção 4:

```
   OPÇÃO A — o "Desligar" não deixa o preview nascer
   _reset_trigger cancela o timer pendente do lado DEPOIS de trocar o combo
   (o handle já é guardado: _trigger_live_preview_timer, :241-249)

   OPÇÃO B — o "Desligar" troca o combo SEM emitir
   um caminho de "set silencioso" no SegmentedSelector, como o GtkComboBox
   resolve com handler_block

   Nos dois casos o resultado é o mesmo: `trigger.set` NÃO sai depois
   de um `trigger.reset`, e a trava fica solta.
```

---

## 3. O teste que MORDE

O arquivo **já existe** — `tests/unit/test_triggers_actions.py` — e o conserto
começa por fazer o dublê parar de mentir. **Isto é entrega, não preparação:**
sem ela, qualquer conserto é declarado sem prova.

### Mordida 1 — o dublê que emite (é a mordida principal)

**Arrancar:** deixar o `set_active_id` do dublê como está hoje
(`tests/unit/test_triggers_actions.py:274-275`), sem emitir `"changed"`.

**Por que reprova:** o dublê passa a espelhar o widget real
(`app/widgets/segmented_selector.py:139-152`): emite quando o id muda, é no-op
quando não muda. Com o dublê honesto e a cura arrancada, a asserção de
`tests/unit/test_triggers_actions.py:545` **reprova hoje** — que é exatamente o
que se quer ver antes de consertar.

### Mordida 2 — o relógio que dispara

**Arrancar:** deixar `GLib.timeout_add` como `lambda: 0`
(`tests/unit/test_triggers_actions.py:385`).

**Por que reprova:** o defeito é **temporal** — acontece 300 ms depois, não na
chamada. O dublê passa a guardar o callback e o teste o **dispara à mão** depois
do `trigger_reset`. Sem isso, a mordida 1 sozinha ainda deixa passar a versão em
que o `"changed"` é emitido mas o timer é engolido.

### Mordida 3 — o caso que NÃO deve mudar

**Arrancar:** cancelar o preview em toda troca de modo, e não só na vinda do
"Desligar".

**Por que reprova:** o live-preview é feature pedida
(`app/actions/triggers_actions.py:235-239`: *"aplica o modo no hardware em 300 ms
para o usuário sentir o efeito sem precisar clicar «Aplicar»"*). O teste muda o
modo pelo gesto normal e exige que o `trigger.set` **saia**. Uma hipótese tem de
explicar o que já funcionava — matar o preview inteiro é contorno.

### Mordida 4 — o "Desligar" com o modo já em "Off"

**Arrancar:** nada; é o caso de controle.

**Por que existe:** documenta a ressalva. Com o modo já em `"Off"`, não há
`"changed"`, não há timer, e não há re-arme nem antes nem depois. O teste
registra os dois caminhos para que ninguém "conserte" o caso que nunca esteve
quebrado.

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **A tela avisa que a troca automática voltou?** Hoje o gesto é mudo dos dois lados — armar e soltar. O cadeado do autoswitch já tem lugar na Início | escrever o aviso que ela aprovar, ou nenhum |
| **Opção A (cancelar o timer) ou B (trocar sem emitir)?** A é local ao botão; B é um caminho novo no widget que serve a outros lugares | recomendo a **A**: mexe num arquivo só e não muda a semântica de um widget usado em seis telas |
| — | o dublê honesto, as quatro mordidas, e o conserto |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: tudo.** É mixin com dublê, sem GTK real, sem daemon e sem
controle. Este é o item mais barato da leva e o de dano medido mais direto.

**A bancada dela fecha uma coisa só, e é a que dá a palavra final:** aplicar
"Rígido", clicar "Desligar", abrir o jogo e ver o perfil trocar sozinho. Hoje
não troca.

**E ela pode ver isto HOJE, com o único controle ligado** — não depende de mesa
cheia. É a razão de esta sprint vir cedo mesmo sem ser sobre os quatro
jogadores: ela entra numa leva chamada "mesa cheia" porque foi o censo dos
quatro controles que a encontrou.

---

## 6. Nota datada — 14/08/2026: os dois furos que o ceticismo mediu

A cura da seção 2 (opção A) foi escrita, atacada por três céticos independentes
e **sustentada**. Mas o ataque encontrou **dois furos residuais** que a sprint
não previa. Ficam registrados aqui porque nenhum relatório os marcava como
pendência — e o que não está em arquivo não existe na próxima sessão.

### 6.1 O furo do OUTRO lado — CURADO em 14/08

`_cancelar_live_preview(side)` mata só o lado do botão. A **trava manual não
tem lado**: `daemon/state_store.mark_manual_trigger_active` recebe uma
categoria só (`"trigger"`) para os dois gatilhos, e
`daemon/ipc_handlers._handle_trigger_reset` limpa essa mesma categoria única.
Então mexer no modo do gatilho **direito** e, dentro de 300 ms, clicar
"Desligar" no **esquerdo** deixava o `trigger.set` da direita cair **depois**
do `trigger.reset` da esquerda, re-armando a trava que o botão acabou de
soltar. É o dano da seção 1 por uma janela mais estreita.

Reproduzido antes da cura, nesta árvore:

```
disparados: 1  trigger.set: [('right', 'Rigid', [5, 200])]
```

**A cura ADIANTA, não cancela** (`_adiantar_live_preview`, em
`app/actions/triggers_actions.py`): o preview pendente do outro gatilho é uma
aplicação que ela pediu, num gatilho que ela **não** mandou desligar —
cancelá-lo seria o mesmo contorno que a mordida 3 já proíbe. Adiantando, o
mesmo `trigger.set`, com os mesmos bytes, sai **antes** do `trigger.reset`; o
"Desligar" volta a ser a última palavra, e o comportamento fica idêntico ao de
qualquer outro instante (quando o preview já tinha disparado sozinho).

**O que MAIS mudou, medido e não estimado.** Sete sequências de cliques foram
rodadas contra o fonte de antes e o de depois, e a saída das duas comparada
byte a byte. Só **duas** cenas mudam:

1. *(a cura)* aplicar à direita e, antes dos 300 ms, "Desligar" à esquerda: a
   ordem no socket vira `set → reset` em vez de `reset → set`, e não sobra
   preview pendente.
2. *(efeito colateral, aceito)* aplicar à direita e, antes dos 300 ms, clicar
   "Desligar" nos **dois** lados: antes, o `trigger.set` "Rígido" da direita
   era **descartado em silêncio** (o `set_active_id("Off")` do próprio
   "Desligar" da direita substituía o timer, e o cancelamento o matava);
   agora ele sai, e o `trigger.reset` da direita o desfaz logo em seguida. O
   estado final do aparelho e da trava é o mesmo nos dois casos — muda um
   `trigger.set` a mais no fio, desfeito no mesmo gesto.

As outras cinco cenas (aplicar/esperar/desligar do mesmo lado; "Desligar" com
o modo já em Off; aplicar à direita, **esperar**, e desligar à esquerda;
aplicar e desligar no mesmo lado dentro dos 300 ms; trocar de modo nos dois
lados sem desligar) saem **idênticas**, chamada por chamada.

Coberto por dois testes que mordem, em `tests/unit/test_triggers_actions.py`:
`test_o_desligar_de_um_lado_nao_deixa_o_outro_re_armar_a_trava` (a ordem) e
`test_o_desligar_de_um_lado_nao_engole_o_preview_do_outro` (o caso que não
deve mudar).

**O preço da cura, dito por inteiro** (anotado pelo ceticismo de 14/08, e
conferido no fonte: `daemon/ipc_handlers.py:1141` arma, `:1199` limpa, e a
limpeza é incondicional — a categoria é uma só). Na cena curada, o gesto
termina com a trava **limpa** enquanto o gatilho DIREITO carrega o modo que ela
acabou de escolher; ou seja, a troca automática de perfil pode passar por cima
desse modo. Antes da cura a trava terminava **armada** e o protegia. **Não é
regressão**: é exatamente o que já acontecia no caminho lento — aplicar à
direita, **esperar** os 300 ms e só então desligar à esquerda —, que é o
comportamento pré-existente e o mais comum dos dois. A causa é a trava sem
lado do daemon, não a ordem no fio. Quem for mexer na granularidade da trava
(`mark_manual_trigger_active`/`clear_manual_trigger_active` por lado) resolve
os dois de uma vez, e aí esta cura da GUI vira redundante.

### 6.2 O furo do «Desligado» do seletor — ABERTO, é decisão dela

A aba tem **dois gestos que apagam o gatilho e prometem a mesma coisa na
tela**:

| gesto | o que sai no socket | a trava manual |
|---|---|---|
| botão **«Desligar»** (`trigger_left_reset`, tooltip *"Tira a resistência do L2"*) | `trigger.reset` | **solta** |
| botão **«Desligado»** do seletor de modos (`app/actions/trigger_specs.py:83`, id `Off`) | `trigger.set` "Off", pelo live-preview de 300 ms | **arma** |

Medido em 14/08, nesta árvore:

```
disparados: 1  trigger.set: [('left', 'Off', [])]  trigger.reset: []
```

**Não está declarado como defeito, e por isso não foi curado.** "Desligado" é
um modo como os outros dezoito, e armar a trava é coerente com *"ela escolheu
isto à mão, o perfil automático não pode passar por cima"*; o botão
«Desligar» é que nasceu (R-19) para **soltar**. Os dois são defensáveis — o
que ninguém pode decidir no lugar dela é se dois controles vizinhos, que a
tela descreve igual, devem continuar com efeitos invisíveis opostos, ou se um
deles some.

O comportamento de hoje está fixado em
`test_o_desligado_do_seletor_ainda_manda_trigger_set` — que é **retrato, não
cura**: não há nada a arrancar nele. Ele existe para que a mudança, quando ela
decidir, seja deliberada.

**Como reproduzir os dois** (sem aparelho, sem daemon, ~1 s):

```bash
.venv/bin/python -m pytest -q -p no:randomly \
  tests/unit/test_triggers_actions.py \
  -k "re_armar_a_trava or preview_do_outro or desligado_do_seletor"
```

Com a árvore de hoje, os três passam (o furo 6.1 curado, o 6.2 retratado).
Para **ver o furo 6.1 morder**, arranque a chamada
`self._adiantar_live_preview(...)` de `_reset_trigger`:

```
E   AssertionError: o trigger.set do outro gatilho caiu DEPOIS do trigger.reset
E                   e re-armou a trava manual, que é uma só para os dois lados
E   assert ['reset'] == ['set', 'reset']
```

### 6.3 A afirmação falsa sobre o dublê — SUBSTITUÍDA em 14/08/2026

Circulou em relatório desta leva que esquecer um nome na tupla do
`_build_mixin` (`tests/unit/test_triggers_actions.py`) "passaria por
`AttributeError` silencioso". **É falso, e foi medido.** Nenhum dos dois
descuidos possíveis é silencioso — e cada um falha de um jeito diferente, que é
a razão de três agentes terem descrito a mesma linha de três jeitos
incompatíveis: cada um rodou um experimento e nenhum soube do outro.

| descuido | onde estoura | quanto derruba |
|---|---|---|
| nome **fora** da tupla, método no fonte | `AttributeError` no primeiro uso, dentro do código de produção (`_reset_trigger`) | 6 failed, 26 passed |
| método **fora** do fonte, nome na tupla | `KeyError` no `__dict__[name]`, ainda na **montagem** do dublê | 29 failed, 3 passed |

Medido nesta árvore, com `-p no:randomly`, arrancando um item por vez e
devolvendo por `md5sum`. A contagem do primeiro caso era 4 antes desta leva:
subiu para 6 porque os dois testes da seção 6.1 também passam pelo
`_cancelar_live_preview`.

Isto **não é decisão a preservar**: é fato errado substituído pelo certo, e o
lugar dele é o código. Está escrito em cima da própria tupla, onde a próxima
pessoa esbarra nele antes de medir de novo. A tupla não precisa de portão
próprio justamente porque as duas falhas são barulhentas.
