# ESCOLHA-DELA-VENCE-01 — a máscara do perfil, e o preço do Xbox onde ela escolhe

- **Status:** E1 e E4 ENTREGUES em 01/08/2026 (noite). E2, E3 e E5 seguem
  ABERTAS, e o motivo de cada uma está no fim
- **Status anterior:** PROPOSTA, pronta para executar. Escrita em 01/08/2026 **para
  sobreviver à queda da sessão** — tudo o que é preciso para executar está
  neste arquivo
- **Prioridade:** **ALTA.** O levantamento achou **três caminhos** pelos quais a
  escolha dela some, e um deles é defeito novo, sem teste que o pegue
- **Aberta em:** 01/08/2026, por ela: *"o que eu quero é que minha escolha aqui
  prevaleça sempre. E ao deixar o mouse sobre a opção Xbox, ele falaria que o
  Xbox não tem tais features. Mas em todos eu poderia escolher Hefesto ou Sony
  pra usar e tirar proveito de tudo."*
- **Parente direta:** a família *"a config que eu deixo nunca é respeitada"*,
  que esta casa já pagou uma vez (três escritores do perfil sem dono).
  [ÍNDICE das sprints de 01/08](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)

## O que foi medido, e o veredito

A cadeia **funciona** no caso normal: ela grava a máscara no perfil, o perfil
ativa, e o daemon aplica —
`activate → apply_emulation → apply_profile_mode → set_gamepad_emulation(origin="profile")`.
O perfil inclusive **vence o flag** em tempo de execução.

O problema são as bordas. **Três caminhos onde a escolha dela some**, em ordem
de gravidade:

### Defeito 1 — "sem opinião de máscara" vira **Xbox** sozinho

Um perfil pode dizer `{"kind": "gamepad", "gamepad_flavor": null}`, e `null`
significa, no applier, **"mantém a máscara atual"**
(`profiles/schema.py:701-718`, `daemon/lifecycle.py:1976-1979`).

Só que o editor da GUI converte isso em `"xbox"` **nas duas pontas**:

- ao ABRIR: `flavor = (mode.gamepad_flavor if mode is not None else None) or "xbox"`
  — `app/actions/profiles_actions.py:605`;
- ao SALVAR: `flavor = flavor_sel.get_active_id() or "xbox"`
  — `app/actions/profiles_actions.py:638-640`.

**Consequência:** ela abre um perfil que não tinha opinião sobre máscara, salva
qualquer outra coisa nele, e o perfil passa a **exigir Xbox** — apagando
giroscópio e touchpad naquele jogo. Ela nunca pediu isso, e **nenhum teste
morde**.

### Defeito 2 — a máscara do perfil **não sobrevive ao reboot**

No boot, o restore roda com `mode_applier=None`
(`daemon/connection.py:220-224`). O `mode` do último perfil **não é aplicado**;
quem manda é o `gamepad_emulation.flag`, que guarda o último gesto **manual**
dela.

**Consequência:** ela configura a máscara por perfil, reinicia o computador, e
o daemon sobe com a máscara do último clique manual — que pode ser de semanas
atrás e de outro jogo.

O mesmo vale na saída do Modo Nativo (`daemon/lifecycle.py:964-968`): o restore
vem do stash, que foi capturado do flag (`:868`), não do perfil.

### Defeito 3 — com o jogo aberto, a troca é recusada **e reporta sucesso**

`_recriacao_bloqueada_por_jogo` (`daemon/subsystems/gamepad.py:1008-1039`)
recusa recriar o vpad enquanto `display_authority == "game"`. **A regra é certa
e não deve ser afrouxada** — recriar o vpad no meio do jogo invalida os handles
que ele abriu, e a Steam nunca reabre o hidraw do vpad P1. Isso foi medido ao
vivo.

O defeito é outro: `start_gamepad_emulation` devolve `True` mesmo quando o gate
recusou (`gamepad.py:1433-1434` — o `True` significa "ativo ao final", não
"apliquei o que você pediu"). Então `apply_profile_mode` devolve `APLICADO`, o
relatório do `profile.switch` diz que deu certo, e **o único rastro é um
`logger.warning` e um contador que a janela não mostra**.

Some-se: a mitigação existe (armar a máscara **antes** do jogo executar, em
`daemon/launch_env.py:454-595`), mas ela **só cobre perfis que casam o jogo por
`steam_app_<appid>` no `window_class`** (`_steam_profiles`, `:683-694`). Perfil
que casa por título de janela ou nome de processo **nunca é armado** — chega
tarde, é recusado, e ninguém avisa.

> Vale notar quais dos perfis dela casam por título/processo: os presets de
> gênero (`acao`, `aventura`, `fps`…) usam `title_regex` e `process_name`, que
> é exatamente o caso não coberto.

### E o pedido do tooltip

No editor de perfis, os botões de máscara têm **um tooltip só, no widget
inteiro** (`profiles_actions.py:531-535`: *"Quais desenhos de botão o jogo
mostra na tela"*) — que, além de não ser por botão, **não diz o preço**.

O texto certo **já existe**: `TEXTO_CUSTO_MASCARA_XBOX`
(`app/actions/home_actions.py:222-236`) e a função pura
`texto_do_custo_da_mascara` (`:239-246`), entregues na MASCARA-CUSTO-01. Eles
aparecem na aba Início e **não** no editor de perfis — que é onde ela escolhe
por jogo.

## Entregas

### E1. `null` continua sendo `null` (defeito 1)

O editor para de converter "sem opinião" em `"xbox"`.

**Onde:** `app/actions/profiles_actions.py:605` (abrir) e `:638-640` (salvar).

**A decisão de desenho:** com `gamepad_flavor` ausente, o seletor de máscara
não pode mostrar um dos dois botões como se fosse a escolha dela. Duas saídas,
e a segunda é a recomendada:

- acrescentar um terceiro item `— manter a atual` ao `_MODE_FLAVOR_ITEMS`
  (`:128-131`), que grava `null`;
- **recomendada:** deixar o seletor **sem nenhum ativo** quando o valor é
  `null` (o `SegmentedSelector` já sabe limpar o ativo —
  `tests/unit/test_segmented_selector.py:84-100` cobre isso) e só gravar
  máscara quando houver um botão marcado.

**Aceite:** carregar um perfil com `"gamepad_flavor": null`, salvar sem tocar na
máscara, e o JSON continuar com `null`. **Teste que morde:** o round-trip com
`null` na entrada tem de dar `null` na saída — hoje dá `"xbox"`.

### E2. O perfil sobrevive ao reboot (defeito 2)

**Onde:** `daemon/connection.py:220-224`.

**O cuidado que a torna difícil, e por que ela não é uma linha:** o restore de
boot desligou o applier **de propósito** em algum momento — ligar de volta sem
entender o porquê é reabrir um defeito antigo. Quem executar **tem de**:

1. achar o commit que pôs `mode_applier=None` ali (`git log -S "mode_applier" -- src/hefesto_dualsense4unix/daemon/connection.py`)
   e ler a mensagem;
2. se o motivo tiver caducado, ligar o applier com `origin="restore"` — um
   origin PRÓPRIO, para não se confundir com `"profile"` nem `"manual"` nos
   quatro portões de `apply_profile_mode`;
3. se o motivo continuar válido, a alternativa é **o flag guardar também a
   procedência** (manual × perfil) e o boot respeitar o perfil quando o último
   escritor tiver sido ele.

**Aceite:** ativar um perfil com máscara DualSense, reiniciar o daemon
(`systemctl --user restart hefesto-dualsense4unix`), e a máscara continuar
DualSense.

### E3. Recusa com jogo aberto deixa de ser silenciosa (defeito 3)

**A regra R-04 não muda.** O que muda é que ela passa a ser **visível**.

**Onde:**
- `daemon/subsystems/gamepad.py:1425-1435` — distinguir "apliquei" de "está
  ativo, mas recusei sua troca";
- `profiles/manager.py:515-533` — o relatório do `profile.switch` carregar essa
  distinção;
- a aba Status ou o rodapé mostrando: *"a máscara deste perfil só vale no
  próximo jogo — trocar agora derrubaria o controle no jogo aberto"*.

**Precedente de como dizer isso sem mentir:** a APLICAR-VERDADE-01 fez
exatamente esse movimento no rodapé (a resposta ganhou um campo `failed` e a
frase passou a dizer *"Aplicado, menos: luzes, gatilhos."*). **Releia aquela
sprint antes de desenhar esta** — inclusive o "O que NÃO fazer" dela.

**Aceite:** com um jogo em foco, ativar um perfil de máscara diferente. A tela
diz que a troca foi adiada; não diz que aplicou.

### E4. O preço do Xbox aparece onde ela escolhe

Duas metades:

**(a) tooltip por botão.** O `SegmentedSelector` **não suporta hoje** — o
`set_items` recebe só `(id, label)`
(`app/widgets/segmented_selector.py:63-84`) e `_create_buttons` (`:194-233`)
não toca em tooltip. São quatro passos, e o terceiro é o que esquecem:

1. a lógica pura (`_SegmentedLogic`, `:39-122`) aceitar as dicas — **atenção:**
   a idempotência é `if items == self._items: return` (`:76-77`); mudar a forma
   da tupla muda esse comparador e o `_index_of` (`:105-113`);
2. a classe GTK chamar `btn.set_tooltip_text(dica)` no laço, depois do
   `btn.set_mode(False)` (`:217`);
3. **o stub sem GTK (`:265-297`) precisa da MESMA API** — sem isso, todo teste
   em ambiente sem PyGObject quebra com `AttributeError`;
4. os dublês de widget nos testes também (ex.:
   `tests/unit/test_r12_editor_simples_gui.py:98`).

**(b) o aviso de custo no editor**, como na aba Início. Reusar
`texto_do_custo_da_mascara` — **função pura, já escrita e testada**
(`tests/unit/test_mascara_diz_o_que_custa.py`). Não escrever um segundo texto:
dois donos da mesma frase derivam, e esta casa já tem a regra.

**Aceite:** no editor de perfis, o mouse sobre "Xbox 360" diz que naquele modo
o jogo não recebe giroscópio nem touchpad — e que vibração, microfone e
alto-falante continuam.

### E5. O empate deixa de ser decidido pelo alfabeto (opcional, mas relacionado)

`profiles/manager.py:836-848`: quando o incumbente não está entre os empatados,
vence `empatados[0]` — a ordem alfabética do nome do arquivo. E é o `mode` do
vencedor que entra.

A EMPATE-01 curou a metade do incumbente. Esta metade continua aberta, e é
citada aqui porque **muda a máscara** sem ela pedir. Se não for feita nesta
sprint, some ao índice das pendências.

## Testes que vão reprovar

Rode antes: `pytest tests/unit -k "profile or mode or segmented or empate"`.

| teste | por quê |
|---|---|
| `test_profiles_editor_mode.py` (`:239-320`, `:271-295`, `:327-360`) | o default `"xbox"` do editor é o que a E1 remove |
| `test_segmented_selector.py` (`:76-82`, `:84-100`, `:204-230`) | **a forma da tupla `(id, label)` é load-bearing** |
| `test_profile_mode.py`, `test_r03_lock_manual_adia_modo.py`, `test_r04_gate_destrutivo_vpad.py`, `test_r04_arming_no_launch.py`, `test_modo01_*.py` | qualquer mudança de precedência bate em pelo menos um |
| `test_perfil_salva_tudo_registrar_nao_e_aplicar.py` | **portão por AST**: proíbe o escritor do rascunho disparar aplicação |
| `test_preset_flavor_migration.py` | a migração `dualsense→xbox` dos presets |
| `test_empate01_a_cor_volta_a_ser_dela.py` | o desempate por incumbente |

## Armadilhas nomeadas — leia antes de tocar no código

1. **R-07** (`gamepad.py:1505-1517`): **o perfil NUNCA persiste a máscara no
   disco.** Se você "consertar" a E2 fazendo o perfil gravar o flag, quebra a
   regra que curou *"ela escolhia Xbox, abria o Sackboy e a flag virava
   dualsense"*.
2. **R-04** (`gamepad.py:1008-1039`): não afrouxe o gate. **Torne visível.**
3. **`start_gamepad_emulation` retorna `True` quando o gate recusa** — é por aí
   que o sucesso mentiroso sobe até a GUI.
4. **R-02** (`lifecycle.py:1930-1947`): catch-all não é ordem de reverter, e com
   janela de jogo em foco nenhum perfil reverte modo. Mexer aqui reabre *"abri o
   jogo e os controles morreram"*.
5. **R-03** (`lifecycle.py:2172-2210`): a pendência de modo é **ÚNICA** e
   sobrescrita de propósito. Não transforme em fila.
6. **`ProfileModeConfig` é `extra="forbid"`** (`schema.py:417`) — campo novo no
   JSON quebra a carga de TODO perfil que o tenha.
7. **`coop` não é emitido pelo editor de propósito** (`profiles_actions.py:622-629`)
   — reemitir congela `coop: false` no disco, o defeito que uma migração já
   teve de limpar.
8. **`_modo_tocado`** (`profiles_actions.py:397`, `:567`, `:616`, `:1822-1829`):
   é o que impede o editor de rebaixar o modo que ela ajustou noutra aba. Todo
   `set_active_id` programático DISPARA o handler — quem popula tem de baixar a
   marca DEPOIS.
9. **Rodar os portões DEPOIS do `git add`** — eles são cegos a arquivo novo.
10. **`ruff check .` ≠ `ruff check src/ tests/`** — use o comando exato do CI.

## O que NÃO fazer

- **Não trocar os perfis dela.** Ela respondeu que a escolha é dela e tem de
  prevalecer. A entrega é a precedência e o aviso, nunca o arquivo dela.
- **Não escrever um segundo texto de custo da máscara.** Reuse a função pura.
- **Não misturar esta sprint com a PARIDADE-SONY-01** — ela mexe no mesmo
  subsistema de gamepad, e cruzar as duas torna impossível dizer qual quebrou o
  quê.

---

## O que foi entregue — 01/08/2026, noite

### E1 — `null` voltou a ser `null` (o defeito 1)

O `or "xbox"` saiu das **duas** pontas do editor. Ele era um defeito ativo e
**nenhum teste o pegava**: ela abria um perfil sem opinião sobre máscara,
salvava qualquer outra coisa nele (a cor, o gatilho, o nome), e o perfil
passava a EXIGIR Xbox — apagando giroscópio e touchpad naquele jogo.

Das duas saídas desenhadas, entrou a **recomendada**: com `gamepad_flavor:
null` o seletor fica **sem nenhum botão marcado** (`limpar_ativo`), em vez de
ganhar um terceiro item "— manter a atual". Mostrar um dos dois marcado seria
a tela afirmando uma escolha que ninguém fez.

O `limpar_ativo` **não emite "changed"**, e isso é a parte fácil de errar: é
POPULATE, não gesto dela, e o `_modo_tocado` (armadilha 8 da sprint) separa as
duas coisas. Um sinal ali levantaria a marca como se ela tivesse clicado.

### E4 — o preço do Xbox onde ela escolhe

O `SegmentedSelector` ganhou `set_tooltips({id: texto})` — dica por BOTÃO.

**Ela NÃO entrou na tupla de `set_items`**, e a decisão é de risco: a sprint
avisa que a forma `(id, label)` é load-bearing, e ela tem razão — o comparador
de idempotência (`if items == self._items`) e o `_index_of` desempacotam dois
elementos, e três arquivos de teste travam a tupla. Um método separado entrega
o mesmo sem encostar em nada disso, e funciona nas duas ordens de montagem
(dica antes dos itens e depois).

O texto é o `texto_do_custo_da_mascara`, **reusado** da MASCARA-CUSTO-01. Ele
vivia só na aba Início, que não é onde ela escolhe por jogo.

## O que ficou ABERTO, e por quê

- **E2 (a máscara sobrevive ao reboot).** A própria sprint diz que ela "não é
  uma linha": o restore de boot desligou o applier **de propósito** em algum
  momento, e o passo 1 do roteiro é achar o commit e ler a mensagem antes de
  religar. Fazer isso no fim de uma leva longa, sem poder reiniciar o daemon
  na máquina dela para conferir, é reabrir um defeito antigo às cegas;
- **E3 (a recusa com jogo aberto deixa de ser silenciosa).** Ela toca
  `gamepad.py`, `manager.py` e a tela, e a sprint manda reler a
  APLICAR-VERDADE-01 antes de desenhar. É uma leva própria;
- **E5 (o desempate pelo alfabeto).** Marcada como opcional na própria sprint.

**As três continuam valendo, e o índice as carrega.** O que foi entregue é o
que apagava a escolha dela HOJE, a cada salvamento — e o que ela pediu com
todas as letras.
