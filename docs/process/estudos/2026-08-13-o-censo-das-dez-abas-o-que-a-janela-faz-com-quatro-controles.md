# O censo das dez abas — o que a janela faz com quatro controles

> **Como esta página nasceu.** Rodada de censo em paralelo, **somente leitura**, em
> **13/08/2026**, contra a árvore em **`cc768d4`** — a mesma que carrega a tag
> **`v0.9.4.2`** —, branch `restauro/inicio-da-sessao`. **Nove agentes mediram uma aba
> cada**; uma décima síntese somou os nove e descobriu que **a janela tem dez abas**.
> Nada foi escrito em hardware, nenhum serviço reiniciado: o DualSense dela seguiu por
> USB e o daemon seguiu vivo durante a medição inteira.
>
> **O pedido dela que originou o censo, literal (13/08):** *"caso os outros controles
> estivessem instalados, cada seleção deles com cada estilo ficaria marcado na cor do
> lightbar deles, igual jogo quando selecionamos um personagem, aí cada player poderia
> escolher o seu estilo de gatilho. **isso valeria pra todas as abas**."*
>
> **A correção dela, que este censo foi medir:** *"todas as abas vão ter problemas nesse
> sentido, acho que a aba status é outra. **deve ter mais**."*
>
> **Como ler os graus.** Cada achado traz o seu, e graus não se misturam na mesma frase:
>
> | grau | significa |
> |---|---|
> | **medido** | saiu de um comando rodado nesta árvore, nesta data (`grep`, `sed`, medição offscreen) |
> | **lido-no-código** | o caminho foi lido no fonte e fecha; o efeito não foi observado no aparelho |
> | **inferido** | dedução a partir de duas leituras, sem execução que confirme |
>
> **A janela não foi aberta.** Toda afirmação sobre interface veio de código, de
> `main.glade` e dos PNG de `docs/usage/assets/`. O aceite continua sendo o olho dela,
> pela regra da
> [PROVA-DE-TELA-01](../sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).
>
> **Nada foi provado com dois ou mais controles.** Ela tem **um** DualSense por USB
> agora. Os veredictos "mira certo" são leitura de código somada ao ensaio dela de 12/08
> (`docs/data/ensaios.csv:67` — gatilho Rigid por `uniq` no rádio, com os outros três R2
> soltos como controle negativo).

---

## O que o transporte para o repositório corrigiu

Amostrei **mais de quarenta** endereços `caminho:linha` do censo e abri cada um contra
`cc768d4`. A taxa dos nove agentes é alta: **a grande maioria abre exatamente no que
promete**. As correções abaixo mudam o **endereço**, nunca o fato — o fato foi
reconferido e sobrevive em todos os casos.

| Endereço no censo | Endereço certo | O que muda |
|---|---|---|
| `home_actions.py:1090` (*"O jogo vê o controle como:"*) | **`home_actions.py:1093`** | `:1090` é um `pack_start`. O rótulo existe e é literal |
| `home_actions.py:344-348` (banner `native_bt_fragil`) | **`home_actions.py:372`** | `:344` é o banner do **wrapper ausente**, outro aviso. O `native_bt_fragil` é lido em `:372`, e a docstring que o cita está em `:362` |
| `rumble_actions.py:430` (`rumble_policy_set_checked`) | **`rumble_actions.py:433`** | a chamada global existe e é logo depois da gravação por peça |
| `rumble_actions.py:432` (toast *"Intensidade da vibração: ..."*) | **`rumble_actions.py:435`** | `:432` é comentário; o toast é montado em `:435` |
| `rumble_actions.py:539` (`uniq = self._rumble_edit_uniq()`) | **`:540`**, com `with_controller_rumble` em **`:551`** | um a menos |
| `triggers_actions.py:566` (`combo.set_active_id("Off")`) | **`:567`** (`:566` é o `if combo is not None`) | a docstring do defeito é `:550-564`, não `:549-563` |
| `ipc_handlers.py:3314-3336` (`_handle_rumble_policy_set`) | **`:3318-3336`** | a faixa começava quatro linhas antes do `def` |
| `external_mask.py:178-330` (`ExternalMaskRegistry`) | classe em **`:157`**; `:178` é o `__init__` | a faixa está dentro da classe, mas a cabeça não |
| `status_actions.py:426` (`_edit_target_uniq`) | **`:427`** (`:426` é o comentário) | um a menos |
| `backend_pydualsense.py:1943` (`next(iter(self._handles))`) | **`:1944`** | um a menos; o outro agente já citava `:1944` |
| *"20 ocorrências de `_edit_target_uniq` em `src/`"* | **19** (medido: 11 em `status_actions.py`, 2 em cada um de `lightbar`, `triggers`, `rumble`, `draft_config`) | a prova negativa fica igual: nenhuma nos módulos acusados |

**Um aviso vivo, que não é erro de ninguém.** `controller_card.py:1989` abre exatamente
em `self._uniq = uniq if isinstance(uniq, str) and uniq else None` **no commit
`cc768d4`**. Na árvore de trabalho de agora ele está em **`:2050`**: outros agentes desta
mesma leva estavam escrevendo enquanto esta página era medida.

**Todo endereço desta página está ancorado em `cc768d4`.** Quatro dos arquivos citados já
divergem da árvore de trabalho, e os endereços deles vão derivar quando a leva de hoje for
commitada (medido com `git diff HEAD --numstat`, 13/08):

| arquivo | delta na árvore de trabalho |
|---|---|
| `app/widgets/controller_card.py` | +189 / -1 |
| `gui/main.glade` | +27 / -0 |
| `app/actions/profiles_actions.py` | +15 / -3 |
| `core/led_control.py` | +23 / -4 (as linhas citadas aqui **não** se moveram) |

Os demais arquivos citados estão idênticos ao commit. *Medido.*

**O que eu não consegui reconferir:** a medição de geometria (*"quatro cards pedem
1626 px numa janela de 830"*). O denominador confere — `main.glade:110` declara
`default-height` 830 —, mas o numerador saiu de uma montagem offscreen do agente da
Status e reproduzi-la exigiria abrir GTK. Fica como **medido pelo agente, não
reconferido**.

### Onde moram os arquivos citados

O texto abrevia pelo nome do módulo, como a casa escreve. Esta tabela é o que faz cada
endereço abreviado **abrir**. As **81 citações distintas** desta página resolvem para um
único arquivo da árvore e estão dentro da faixa em `cc768d4` — conferido por varredura,
além da amostra aberta à mão.

| como aparece no texto | caminho na árvore |
|---|---|
| `main.glade` | `src/hefesto_dualsense4unix/gui/main.glade` |
| `status_actions.py` | `src/hefesto_dualsense4unix/app/actions/status_actions.py` |
| `home_actions.py` | `src/hefesto_dualsense4unix/app/actions/home_actions.py` |
| `triggers_actions.py` | `src/hefesto_dualsense4unix/app/actions/triggers_actions.py` |
| `lightbar_actions.py` | `src/hefesto_dualsense4unix/app/actions/lightbar_actions.py` |
| `rumble_actions.py` | `src/hefesto_dualsense4unix/app/actions/rumble_actions.py` |
| `app/app.py` | `src/hefesto_dualsense4unix/app/app.py` |
| `controller_card.py` | `src/hefesto_dualsense4unix/app/widgets/controller_card.py` |
| `painel_no_jogo.py` | `src/hefesto_dualsense4unix/app/widgets/painel_no_jogo.py` |
| `segmented_selector.py` | `src/hefesto_dualsense4unix/app/widgets/segmented_selector.py` |
| `backend_pydualsense.py` | `src/hefesto_dualsense4unix/core/backend_pydualsense.py` |
| `core/controller.py`, `core/led_control.py` | `src/hefesto_dualsense4unix/core/` |
| `ipc_handlers.py`, `daemon/ipc_server.py` | `src/hefesto_dualsense4unix/daemon/` |
| `coop.py`, `external_mask.py`, `daemon/subsystems/rumble.py` | `src/hefesto_dualsense4unix/daemon/subsystems/` |
| `profiles/schema.py` | `src/hefesto_dualsense4unix/profiles/schema.py` |
| `storm_doctor.py` | `src/hefesto_dualsense4unix/integrations/storm_doctor.py` |
| `test_triggers_actions.py`, `portao_a_casa_sabe_e_o_produto_nao_faz.py` | `tests/unit/` |

---

## 1. A tabela das dez abas

**São dez páginas no `main_notebook`** (`main.glade:212`), e este foi o primeiro achado
do censo, porque muda a conta: `main.glade` põe os dez containers nas linhas 219, 251,
**678**, 692, 1018, 1501, 1874, 2397, 2735 e 3270. *Medido.*

A terceira é a **"No jogo"** (`tab_no_jogo_box`, `main.glade:678`; rótulo em
`main.glade:685`), montada em código por `install_no_jogo_tab`
(`app/actions/status_actions.py:541`). **Nenhum dos nove agentes a mediu** — ela não
estava na lista que eles receberam. É lacuna declarada, não achado: onde a tabela diz
"não medida", ninguém olhou.

| # | Aba | Natureza | Honra o alvo? | Com quatro controles | O que falta |
|---|---|---|---|---|---|
| 1 | **Início** (`tab_home_box`) | edita-global (modo, máscara, cadeado, reconciliar, energia) | **não** — zero `_edit_target_uniq` em 2007 linhas | aplica em todos, **e a fita mente por cima** | cor nos cards, `FlowBox`, nomear o jogador no banner; `native_bt_fragil` por controle |
| 2 | **Status** (`tab_status_box`) | mostra-estado + edita-por-controle (áudio) | **não lê — é a DONA** do alvo | **mira certo**: 4 cards, 4 MACs, 4 cores | caber na tela; duas guardas de áudio |
| 3 | **No jogo** (`tab_no_jogo_box`) | mostra-estado, **um painel por controle** | não, e não precisa | **não medida** — o código diz um painel por controle, com título certo e **zero cor** | a cor; e o censo que ninguém fez |
| 4 | **Gatilhos** (`tab_triggers_box`) | edita-por-controle pura | **sim**, nos dois eixos | **mira certo** — e diz "aplicado" em três casos em que nada saiu | `aplicado_em` no `trigger.set`; dizer o alvo dentro da aba |
| 5 | **Lightbar** (`tab_lightbar_box`) | edita-por-controle (a mais disciplinada da casa) | **sim**, em seis pontos | **mira certo**: "Todos" vira quatro pedidos por MAC | a faixa dos quatro; dois toasts honestos |
| 6 | **Rumble** (`tab_rumble_box`) | **mista dentro do mesmo clique** | **sim no rascunho, não no daemon vivo** | **a única que desobedece um alvo que existe** | `rumble_active` virar mapa; `rumble.set` aceitar endereço |
| 7 | **Perfis** (`profiles_paned`) | edita-global (nome, prioridade, "Aplica a:", Modo) | **não** — `grep -c uniq` = **0** em 3357 linhas | global; **guarda as quatro faces e nunca as mostra** | vitrine das faces; uma palavra de tooltip |
| 8 | **Sistema** (`daemon_box`) | edita-global (systemd, Steam, WirePlumber) | **não** — e está certo em não honrar | não se aplica — mas fala "o controle" no singular três vezes | contagem em vez de `re.search`; plural |
| 9 | **Emulação** (`emulation_box`) | mista (diagnóstico + máquina) | **não** — zero ocorrências | aplica em todos, **e promete o que três de quatro não têm** | endereço nas rotas; N leitores |
| 10 | **Navegação** (`tab_navegacao_dsx`) | edita-global (mouse, teclado, atalhos) | **não** — e o perfil **proíbe** por decisão dela | global no ajuste, **um controle só no efeito** | dizer quem comanda o PC; decisão |

### O mesmo mapa, em três colunas

```
                     mira      a tela        o que
   ABA               certo?    mente?        falta
   ─────────────────────────────────────────────────────────
 1 Início             n/a       SIM (fita)    tela + 1 flag
 2 Status             SIM       meia (áudio)  tela          <- O MOLDE
 3 No jogo            n/a       não medida    tela          <- o 2o molde, sem cor
 4 Gatilhos           SIM       SIM (volta)   daemon + tela
 5 Lightbar           SIM       SIM (borda)   tela
 6 Rumble           MEIO (*)    SIM (grave)   daemon        <- A ÚNICA que erra o alvo
 7 Perfis             n/a       SIM (fita)    tela
 8 Sistema            n/a       SIM (plural)  tela
 9 Emulação           n/a       SIM (grave)   daemon
10 Navegação          n/a       SIM (fita)    tela + decisão

 (*) Rumble: o card de BAIXO (Testar/Aplicar/Parar) mira certo.
     O card de CIMA (Intensidade) grava na peça e aplica nos quatro.
```

**Nove das dez abas têm trabalho.** Só a Status já resolveu o endereçamento — e mesmo
ela tem duas mentiras de áudio e não cabe com quatro cards.

**Sobre os custos.** Os nove agentes estimaram minutos por item. **Nenhuma dessas
estimativas foi medida**, e elas não entram nesta tabela por isso; ficam nas ondas do
índice de sprints, onde há espaço para a ressalva. A ordem de grandeza que eles somaram:
cerca de 27 h de tela e daemon sem decisão nova, e cerca de 50 h de mecanismo que espera
decisão dela. *Estimativa, não medição.*

---

## 2. As abas que mentem

Uma tela limitada custa menos que uma tela que mente. As mentiras vêm em duas famílias, e
a primeira é **uma peça só, compartilhada pelas dez abas**.

### 2.a — A mentira herdada: a fita nunca sabe em que aba está

**Seis das dez abas** ficam embaixo de uma fita que promete um alvo que elas ignoram. Não
é defeito de aba nenhuma: é defeito de arquitetura, e o conserto é um só.

**O texto que fica na tela:** `_("Ajustes vão para:")` — `status_actions.py:1497` —, os
chips *"Sony 1 · USB"* ao lado, e o selo `_("Editando: {alvo}")` (`status_actions.py:1858`).

**A prova, medida com `grep`:** `_set_target_strip_visible`
(`app/actions/status_actions.py:1673`) tem **exatamente três chamadores** —
`status_actions.py:2094`, `:2177` e `:2505` — e os três decidem por **contagem de
controles** ou por daemon offline. O `_on_notebook_switch_page` (`app/app.py:957`) **não
a menciona**: não existe um único `if` de aba em todo o caminho. *Medido.*

```
   ┌─ header_bar (main.glade:136) ───────────────────────────────┐
   │  Ajustes vão para:  (o)Sony 1·USB  ( )Sony 2·BT  ( )Todos   │  <- sempre visível
   │  Editando: Controle 2 (BT)                                  │
   ├─ main_notebook (main.glade:212) ────────────────────────────┤
   │  Início │Status│No jogo│Gatilhos│Lightbar│Rumble│Perfis│...  │
   │                                                             │
   │   ...e aqui embaixo nada obedece àquele "Controle 2".       │
   └─────────────────────────────────────────────────────────────┘

   A fita É VERDADE em 4 abas:  Status · Gatilhos · Lightbar · Rumble (em parte)
   A fita É FALSA   em 6 abas:  Início · No jogo · Perfis · Sistema ·
                                Emulação · Navegação
```

A ressalva existe — e mora onde ninguém lê. O **tooltip** da fita
(`status_actions.py:1485`) enumera o escopo real: *"Controle alvo das ações (lightbar,
gatilhos, LEDs, rumble)"*. A lista está **certa**, e exclui as seis de propósito. Mas é
tooltip: invisível até alguém parar o ponteiro em cima. Esta casa já reconheceu esse
padrão como defeito uma vez, quando o PLAYER-01 tirou o terceiro papel do chip de dentro
de um tooltip.

### 2.b — As mentiras autoradas, aba por aba

Cada uma com a linha do código **e** o texto que a tela mostra.

| Aba | O que a tela diz | O que o código faz | Gravidade |
|---|---|---|---|
| **Rumble** | selo *"Editando: Controle 2"* (`status_actions.py:1858`) e toast *"Intensidade da vibração: Máximo"* (`rumble_actions.py:435`) | o mesmo clique grava o rascunho **só na peça** (`rumble_actions.py:540-551`) e manda `rumble.policy_set` **global** (`:433` → `ipc_handlers.py:3318-3336`, que escreve `daemon_cfg.rumble_policy`, campo único da máquina) | **a pior**: o alvo existe e é desobedecido |
| **Emulação** | *"Modo jogo: PS + Options suspende mouse e teclado"* (`main.glade:2863`) | existe **um** `EvdevReader`, atrelado ao primário (`backend_pydualsense.py:1955`); `read_state` declara em comentário próprio *"INPUT vem SEMPRE do controle PRIMÁRIO... single-controller por construção"* (`:2192-2195`) | **grave**: falso para três de quatro pessoas na sala |
| **Gatilhos** | *"Gatilho esquerdo (L2): Rigid aplicado"* (`triggers_actions.py:599`) | com o controle **desconectado**, `apply_output_for` registra o override e **pula a escrita em silêncio** (`backend_pydualsense.py:3417-3423`); idem sem MAC 12-hex (`:3402-3407`). E `trigger.set` devolve `{"status": "ok"}` seco (`ipc_handlers.py:958`) enquanto `led.set` já devolve `aplicado_em` (`:1061`) | diz "aplicado" sem byte nenhum ter saído |
| **Lightbar** | *"Cor enviada ao controle ({pct}% de brilho)"* (`lightbar_actions.py:54`) | mesmo silêncio do `apply_output_for`; e o alvo é **mantido de propósito** quando o controle some (R-16) | idem |
| **Lightbar** | toast *"Desenho das luzes aplicado"* (`lightbar_actions.py:986`) **contra** o rótulo logo abaixo: *"Aceso agora: o desenho do co-op — com o co-op ligado, é ele que manda nas 5 luzes"* (`:163-167`) | com co-op, `_desired_coop_by_uniq` vence no merge | **a mesma tela se contradiz** |
| **Status** | seletor em *"Todo o som do PC"*, cuja dica promete *"todo o som do computador passa a sair pelo alto-falante dele"* (`controller_card.py:622-626`) | com 2+ controles o sink é indeterminado: `_sink_do_controle_para_a_rota` devolve `""` (`status_actions.py:948`) e `_aplicar_rota_do_sistema` sai calado no `if sink:` (`:1041`) | metade do gesto evapora em silêncio |
| **Status** | título *"Controle 2 — USB"* | card sem MAC é chave válida (`_status_card_keys_for`, `status_actions.py:1095`), manda `uniq=None`, e o daemon cai no **primário** (`backend_pydualsense.py:3275-3277`) | escreve no controle errado |
| **Início** | *"O jogo vê o controle como:"* (`home_actions.py:1093`), no singular | a máscara é reescrita nos **quatro** vpads a partir de um `gamepad_flavor` só (`daemon/subsystems/coop.py:473-477`) | singular para um gesto plural |
| **Início** | o banner `native_bt_fragil` (`home_actions.py:372`) **cala** | `result["native_bt_fragil"] = bool(result["native_mode"] and result["transport"] == "bt")` (`ipc_handlers.py:2006-2008`), e `transport` é o do **primário** | **falso negativo**: P1 no cabo cala o aviso para P2/P3/P4 em BT |
| **Sistema** | *"áudio do controle presente (mic+fone do DualSense ativos)"* | `re.search(r"DualSense", cards_text)` em `/proc/asound/cards` (`storm_doctor.py:299-306`) — **um** basta para dizer "presente" | 1 de 4 vira "tudo certo" |
| **Sistema** | *"cura do travamento agendada (reconecte o controle p/ ativar)"* (`storm_doctor.py:279`); *"o controle continua jogando"* (`main.glade:2457`, repetido na descrição acessível em `:2463`) | são quatro a reconectar | singular |
| **Perfis** | tooltip do Ativar: *"os gatilhos, a cor e a vibração dele vão para o controle"* (`main.glade:1975`) | `profile.switch` atinge os quatro | uma palavra |
| **Navegação** | *"Emular mouse"* (`main.glade:3302`), *"Emular teclado"* (`:3589`), sem sujeito | o efeito é do **primário**, que é *ordem de plugar*, não número de jogador (`backend_pydualsense.py:1937-1944`, docstring literal: *"Primário = 1ª chave de inserção ainda presente"*) | promete a todos, entrega a um |

Todas as linhas desta tabela foram abertas e conferidas neste transporte. *Medido.*

---

## 3. O molde — a Status já resolveu, e a casa já a copiou uma vez

Ela disse *"acho que a aba status é outra"*. É outra, e por um motivo mais forte do que
ela disse: **a Status já resolveu o problema inteiro**. Não é aba a consertar — é a aba a
copiar.

### 3.a — O que exatamente se copia

Os endereços abaixo estão ancorados em **`cc768d4`**; `controller_card.py` cresceu na
árvore de trabalho enquanto esta página era escrita (ver o aviso vivo no topo).

| # | A peça | Onde | O que ela resolve |
|---|---|---|---|
| 1 | **O endereço DENTRO do widget** | `controller_card.py:1989` — `self._uniq = uniq if isinstance(uniq, str) and uniq else None`, carregado em toda chamada de áudio do card | um card por controle **não tem alvo a escolher: ele É o alvo**. É isto, e não o desenho, que faz a Status mirar certo |
| 2 | **A cor vinda do `state_full`, não da paleta** | `rotulo_lightbar` em `controller_card.py`, lendo `lightbar_rgb`/`lightbar_on`/`lightbar_source` que o daemon publica | se ela pintar um controle de roxo à mão, o card mostra **roxo**; e sabe dizer *"cor desconhecida"* em vez de inventar |
| 3 | **O quadradinho de 14x14** | `Gtk.DrawingArea` no card, pintado por `_on_draw_swatch` | é literalmente o que ela pediu, já escrito |
| 4 | **A regra de contraste** | `accent_do_card` + `ensure_min_contrast` — decisão **D8**: o quadradinho com a cor **crua**, só os traços ajustados | o azul do P1 em brilho baixo contra o fundo escuro é o caso difícil, e já está resolvido |
| 5 | **O título** | `titulo_do_card` — *"Controle 4 — BT · Jogador 4"* | o vocabulário já existe, e ela já o lê |
| 6 | **A distribuição** | `_status_card_keys_for` (`status_actions.py:1095`) + `zip(..., strict=True)` | `controllers[i]` vira card `i`, sem chance de trocar |
| 7 | **O contra-exemplo que barateia tudo** | `speaker.set`/`mic.set` roteiam por MAC hoje **sem** campo no `OutputSpec` | não é preciso esperar o `OutputSpec` crescer: o áudio ganhou rota própria por `uniq` no IPC e funciona |

### 3.b — O segundo molde já existe, e nasceu sem cor

**Este é o achado que barateia a leva inteira.** A aba **"No jogo"** — a terceira página,
que nenhum agente mediu — **já é** um painel por controle, montado pelas mesmas chaves da
Status:

- `_sync_paineis_no_jogo` (`status_actions.py:766`) usa `_status_card_keys_for` e
  `zip(keys, conectados, strict=True)` (`:821`) — o mesmo mecanismo do item 6 acima;
- `app/widgets/painel_no_jogo.py:468` **já reusa** `titulo_do_card`, importado em `:84` —
  o mesmo rótulo *"Controle 2 — BT · Jogador 2"*;
- e o módulo declara, no cabeçalho, que **chama** a regra do card em vez de reimplementá-la.

**Mas ele não tem uma linha de cor.** `grep -c 'lightbar\|accent\|swatch\|player_slot'` em
`painel_no_jogo.py` devolve **0**. *Medido.*

```
   A Status  ->  título + quadradinho colorido + accent + endereço no widget
   No jogo   ->  título                                    (e mais nada)
                        ^
                 a casa copiou o molde uma vez
                 e deixou a cor para trás
```

Conclusão operacional: **copiar a Status funciona — já foi feito, e o resultado está de
pé.** O que se perdeu na cópia foi exatamente a peça que ela pediu. A leva não é "inventar
um desenho de quatro jogadores": é **terminar uma cópia que a casa já começou**, e
repeti-la nas demais.

### 3.c — A divergência que precisa da palavra dela ANTES da cópia

Já existem **dois donos da verdade sobre "a cor dele"**, e eles divergem sempre que ela
pinta um controle à mão ou desliga as cores automáticas:

- **A cor VIVA:** `lightbar_rgb` do `state_full`, que o card do Status pinta — decisão D8.
- **A PALETA:** `player_slot_color` (`core/led_control.py:158-164`), que a aba Lightbar
  consulta direto para a prévia (`lightbar_actions.py:409-411`) — e o comentário ali
  registra que isso nasceu de um achado ao vivo: *"a prévia ficava roxa enquanto o
  controle estava azul"*.

Paleta canônica, conferida em `core/led_control.py:146-155`: **1 azul (0,0,255) ·
2 vermelho (255,0,0) · 3 verde (0,255,0) · 4 rosa (255,0,128)**; 5..8
amarelo/ciano/laranja/roxo (R-25); slot 9 ou maior cai no branco. *Medido.*

Qualquer marca colorida nova herda essa divergência **no dia um**. É a decisão **D-1** da
seção 6, e ela vem antes de qualquer pixel.

---

## 4. Os defeitos que ninguém tinha escrito

Quatro achados novos, nenhum registrado em lugar nenhum deste repositório antes desta
página.

### 4.1 — O rumble fixo MIGRA de controle quando ela troca o alvo

`daemon_cfg.rumble_active` é uma **tupla global** (`ipc_handlers.py:3248`), mas o destino
dela é o ponteiro mutável `_output_target_key`: `_for_each_com_key`
(`backend_pydualsense.py:2320`) lê `target = self._output_target_key` em `:2336` e escreve
só naquele handle.

A cadeia fecha em quatro degraus, todos abertos neste transporte:

```
  reassert_rumble  (daemon/subsystems/rumble.py:134, 5 Hz)
        │  :150   active = cfg.rumble_active        <- tupla GLOBAL, sem dono
        └─ :176   daemon.controller.set_rumble(weak=..., strong=...)
                      │
                      └─ backend_pydualsense.py:2845  set_rumble
                            └─ :2859  self._for_each_com_key(_do, ...)
                                  └─ :2336  target = self._output_target_key
                                            <- o ponteiro que o SELETOR move
```

Ela aplica 160/220 no Controle 2, troca o seletor para o 3 por outro motivo, e a partir do
tique seguinte o `reassert_rumble` passa a marretar o **3** com os valores do **2**.
*Lido-no-código* — o caminho fecha linha a linha; o efeito não foi observado no aparelho.

### 4.2 — O comando do PC troca de dono em silêncio

Se o primário cai, `_recompute_primary` promove o próximo mais antigo
(`backend_pydualsense.py:1944`), re-atrela o evdev a ele (`:1955`) e escreve um
`logger.info("controller_primary_bound", ...)` que ninguém lê (`:1969`). O cursor passa a
obedecer outro controle no meio do uso, e nada na tela diz isso. *Lido-no-código.*

Agravante do mesmo eixo: **primário é ordem de plugar**, não número de jogador — a
docstring diz *"Primário = 1ª chave de inserção ainda presente"* (`:1937`) —, enquanto o
número do jogador ela pode trocar pela janela. "Controle 1" no seletor e "quem move o
cursor" podem ser aparelhos diferentes.

### 4.3 — Dois botões da aba Sistema apagam o alvo de todas as outras abas

`_output_target_key` só existe na RAM do backend (`backend_pydualsense.py:1165`) e ninguém
o persiste. "Desligar o Hefesto" (`main.glade:2456`) e "Reiniciar" (`:2483`) devolvem o
daemon a broadcast, enquanto a janela mantém o alvo antigo de propósito (R-16). Janela e
daemon divergem sem aviso. *Lido-no-código.*

### 4.4 — O "Desligar" dos gatilhos RE-ARMA a trava 300 ms depois

**É regressão da cura R-19**, e o docstring do próprio método descreve o defeito que
voltou (`triggers_actions.py:550-564`): *"o botão que a usuária usa para 'voltar ao
normal' era mais um jeito de PAUSAR a troca automática de perfil"*.

```
  _reset_trigger (triggers_actions.py:549)
        │
        ├─ :567  combo.set_active_id("Off")
        │            │
        │            └─ SegmentedSelector.set_active_id EMITE "changed"
        │               (segmented_selector.py:139-152 — docstring literal:
        │                "Ativa o botão do id e EMITE changed")
        │                     │
        │                     └─ _on_mode_changed → _schedule_live_preview
        │                        (triggers_actions.py:239 → :249,
        │                         GLib.timeout_add(300, ...))
        │
        └─ :570  trigger_reset(...)  →  LIMPA a trava
                                        (ipc_handlers.py:994,
                                         clear_manual_trigger_active)
                                            ⏱ 300 ms
        ─────────────────────────────────────────▶
           _fire_live_preview → _apply_trigger → trigger.set
                → mark_manual_trigger_active("trigger")
                  (ipc_handlers.py:957)          <- A TRAVA VOLTA
```

*Lido-no-código*, degrau a degrau, cada linha aberta neste transporte.

**E o teste que a protege não morde.** `tests/unit/test_triggers_actions.py:545` afirma
`assert mixin._trigger_set_calls == []` com a mensagem *"trigger.set aqui re-armaria a
trava que o botão deveria soltar"* — e passa por **dois desvios independentes do dublê**:

- o `set_active_id` do dublê (`test_triggers_actions.py:274-275`) só atribui
  `self._active_id` e **não emite "changed"**;
- o `GLib` é substituído por um `SimpleNamespace` cujo `timeout_add` é
  `lambda *_a, **_kw: 0` (`:385`) — o timer nunca dispara.

*Medido.* Os dois desvios foram abertos e conferidos.

**Ressalva honesta:** se o modo já estava em "Off", o `set_active_id` é no-op — a
docstring diz *"Só emite quando o id efetivamente muda — ids inexistentes ou iguais ao
ativo são no-op"* (`segmented_selector.py:142-143`), e a guarda que a implementa está em
`:148-149` — e não há re-arme. O caso que dói é o normal: aplicar Rígido e depois
Desligar.

---

## 5. O que eu errei — a contagem, sem diplomacia

Isto fica registrado porque é **decisão medida**, e a casa não apaga decisão medida. A
afirmação que eu tinha feito antes do censo:

> *"o buraco do rumble (o `OutputSpec` não tem campo de rumble, então `rumble.set` não
> consegue mirar por MAC) travaria a aba Rumble e liberaria as outras."*

Ela respondeu: *"todas as abas vão ter problemas nesse sentido, acho que a aba status é
outra. deve ter mais."*

| Afirmação | Quem | Veredicto | A evidência |
|---|---|---|---|
| *"o `OutputSpec` não tem campo de rumble"* | eu | **certa e IRRELEVANTE** | `core/controller.py:49-68` tem cinco campos (`trigger_left`, `trigger_right`, `led`, `player_leds`, `mic_led`) e nenhum de rumble — conferido. Mas rumble é **transitório** e nunca entra no estado desejado: `_for_each_com_key` diz isso em docstring própria (`backend_pydualsense.py:2332-2333`, *"quem usa isto (o rumble) é TRANSITÓRIO e nunca entra no estado desejado"*). Pôr campo ali seria consertar o lugar errado |
| *"então `rumble.set` não consegue mirar por MAC"* | eu | **ERRADA** | `rumble.set` **mira**. O endereço viaja por fora da chamada: `controller.target.set` arma `_output_target_key` (`backend_pydualsense.py:4152`) e `_for_each_com_key` o honra (`:2336-2340`). Feio, mas funciona |
| *"travaria a aba Rumble"* | eu | **meia certa** | trava a **intensidade** (`rumble.policy_set` é global, `ipc_handlers.py:3318-3336`), não o pulso. E a causa é outra: falta `uniq` **na rota**, não campo na struct — `daemon/ipc_server.py:113-117` roteia cinco verbos de rumble e nenhum aceita endereço |
| *"e liberaria as outras"* | eu | **ERRADA, e é o erro caro** | **nove das dez abas** têm trabalho, e **zero** delas está travada pelo `OutputSpec` |
| *"todas as abas vão ter problemas nesse sentido"* | **ela** | **CERTA — 9 de 10** | só a Status já resolveu o endereçamento; e mesmo ela tem duas mentiras de áudio e não cabe com quatro |
| *"acho que a aba status é outra"* | **ela** | **CERTA, e mais forte do que ela disse** | a Status não é "outra": é **o molde**. Um card por controle, o MAC dentro do widget (`controller_card.py:1989`), a cor vinda do `state_full` |
| *"deve ter mais"* | **ela** | **CERTA de um jeito que ela não previu** | há uma **décima aba** (`tab_no_jogo_box`, `main.glade:678`) que nenhum agente mediu — e ela já é um painel por controle, **sem cor** |

**Placar: ela 3 de 3. Eu 1 de 4** — e o único acerto (a Rumble é a pior no endereçamento)
foi acerto pela razão errada.

### Onde ela está incompleta, e isto se diz com a evidência

A frase *"isso valeria pra todas as abas"* é **diagnóstico certo** e **receita errada**.
Em três lugares o conserto honesto não é rota por MAC:

- **Navegação** — o PC tem **um** cursor e **um** foco de teclado. Quatro escolhas não
  cabem no mundo físico. *(A parte "quatro mouses virtuais somariam no mesmo ponteiro" é
  **inferida**: não há uma linha neste repositório que a prove.)*
- **Sistema** — o alvo é systemd, Steam e PipeWire; o endereçamento sempre foi por APPID
  e VID/PID, e para *"Este jogo não funciona"* esconder os quatro físicos é o
  comportamento **certo**.
- **Início, no quadro "Quando o jogo abrir"** — o MODO é da máquina **por decisão dela
  mesma**, de 10/08/2026, escrita no esquema (`profiles/schema.py:637-639`: *"`mode` e a
  máscara do gamepad são da SESSÃO, não da peça (decisão dela, 10/08/2026): duas unidades
  pedindo modos diferentes no mesmo perfil não têm resposta"*).

Nessas três, o que falta é **declarar o escopo** — não mirar. Nas outras sete, falta
mirar, mostrar, ou as duas.

---

## 6. As dez decisões dela

Cada uma com as opções e **o preço de cada lado**. Nenhuma é escolhida aqui.

### D-1 — Que cor é "a cor dele"?

**Trava tudo o que é colorido. É a primeira.**

| Opção | O que ganha | O que custa |
|---|---|---|
| **A cor VIVA do lightbar** (`lightbar_rgb`, o que o card da Status já pinta — decisão D8) | segue o controle de verdade: se um jogo pinta o P2 de branco, a marca fica branca. **É o léxico já decidido**, e não cria dono novo | dois controles da mesma cor ficam com marcas iguais; e quando `lightbar_source` é "desconhecida" **não há cor para mostrar** |
| **A paleta do slot** (`player_slot_color`, `core/led_control.py:158-164`) | sempre quatro cores distintas e previsíveis — literalmente *"igual jogo quando selecionamos um personagem"*, que é a frase dela | cria o **segundo dono da verdade**: a marca diz vermelho e a barra na mão dela está branca. A aba Lightbar já registra esse achado ao vivo (`lightbar_actions.py:405-408`) |
| **Viva com paleta de reserva** | resolve o caso "desconhecida" | é a mais difícil de explicar numa tela, e ainda pode dar duas iguais |

### D-2 — A fita "Ajustes vão para:", nas seis abas em que não vale

| Opção | Preço |
|---|---|
| **Esconder** | mais limpo; mas o contexto some ao trocar de aba e volta ao voltar — pisca |
| **Requalificar** (uma frase tipo *"esta aba vale para todos"*) | mantém o contexto e ensina; mas é mais texto numa fita já densa |

O gancho é o mesmo nos dois casos: gate por id de página no `_on_notebook_switch_page`
(`app/app.py:957`), que já identifica a aba por id do Glade e nunca por posição
(`app/app.py:964`).

### D-3 — Quatro painéis lado a lado, ou um painel com quatro marcas coloridas?

| Opção | O que ganha | O que custa |
|---|---|---|
| **Quatro painéis** (a leitura literal do pedido dela) | cada jogador vê e mexe no seu ao mesmo tempo — "igual jogo" | **largura**: cada grade de 19 modos de gatilho ocupa metade da tela; e muda o significado de *"Ajustes vão para:"*, que hoje é **um alvo por vez** |
| **Um painel + quatro marcas** | cabe; reusa o `SegmentedSelector`, que é mono-seleção por construção (`segmented_selector.py:139-152`) | não é "cada um escolhe o seu **ao mesmo tempo**" — é "eu escolho por cada um, um de cada vez" |
| **Híbrido**: a faixa dos quatro **mostra** as quatro escolhas, e clicar num troca o alvo | cabe, mostra as quatro, e usa `_sync_edit_target`, que já existe | ela vê as quatro mas mexe numa por vez |

**Os números para decidir** (medidos offscreen pelos agentes, **não reconferidos neste
transporte**): na Gatilhos sobra **altura** (~600 px vazios abaixo das grades) e não sobra
**largura**; na Status a conta é a inversa — quatro cards pedem ~1626 px numa janela cuja
altura padrão é 830 (`main.glade:110`, este sim conferido).

### D-4 — A intensidade da vibração é da peça ou da máquina?

Hoje o produto **responde as duas ao mesmo tempo**: o mesmo clique grava o rascunho só na
peça (`rumble_actions.py:540-551`) e manda ao daemon uma ordem global (`:433`).

| Opção | Preço |
|---|---|
| **Da peça** | `daemon_cfg.rumble_active` vira mapa por `uniq`, `reassert_rumble` itera o mapa, `rumble.set`/`rumble.stop` aceitam endereço — e o `set_rumble_for(uniq, weak, strong)` de que isso precisa **já existe e tem mordida** (`backend_pydualsense.py:3642`, hoje usado só pelo co-op e pelo passthrough). Em troca morrem os três defeitos de §4.1-4.3 |
| **Da máquina** | trocar um rótulo (*"Intensidade global:"*, `main.glade:1571`, já é honesto). Mas então o rascunho grava por peça um número que ninguém lê — e isso é dívida, não conserto |

### D-5 — A máscara do gamepad é do jogo ou do jogador?

**Do jogador:** campo novo em `ControllerOverrides` (que hoje tem `leds`, `triggers`,
`rumble`, `speaker` e nenhum campo de modo/máscara, `profiles/schema.py:658-661`),
`_flavor()` resolvido por uniq (`coop.py:473-477`), `gamepad.emulation.set` aceitando
alvo. **E metade já está escrita e desligada:** `ExternalMaskRegistry`
(`daemon/subsystems/external_mask.py:157`) guarda, valida e persiste máscara por
identidade, e tem **zero chamadores** fora do próprio módulo — o único lugar que a
menciona na árvore é o portão que a acusa por nome
(`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:39`: *"quer GUI e não quer
install"*). *Medido.*

**Do jogo:** uma frase declarando o escopo.

**Risco não medido, e é dela decidir se aceita:** um jogo pode não aceitar controles
heterogêneos na mesma sessão.

### D-6 — O MODO é da máquina ou do jogador?

Ela já decidiu "da máquina", por escrito e com data (`profiles/schema.py:637-639`,
10/08/2026). **Se a resposta continuar sendo essa, o pedido dela não se aplica ao quadro
"Quando o jogo abrir" e o item cai inteiro** — o que sobra ali é declarar o escopo. Se
mudar, `native.mode.set` é estado do daemon inteiro e toda a fiação de transição
(`app/actions/mode_transition.py`) é global.

### D-7 — "Cada player escolhe o seu" inclui quem não é DualSense?

O 8BitDo e o Pro Controller **não têm card na Status**, por decisão de produto EXT-COUNT-01
(`status_actions.py:1109-1112`: *"Card de externo NÃO existe (EXT-COUNT-01: read-only por
decisão de produto)"*). Se o jogador 3 estiver num Pro, ele existe no cabeçalho, existe no
LED de número, e **some** de toda faixa colorida que a leva desenhar.

Incluir custa desenho novo; não incluir custa a pergunta *"cadê o jogador 3?"* na primeira
vez que ela jogar com um externo.

### D-8 — O que "Todos" significa quando os quatro estão na tela?

Hoje "Todos" é um estado real e distinto: `lightbar_actions.py:639` parte o fluxo em três
(`alvos = self._uniqs_conectados() if self._edit_uniq() is None else []`), e o chip só
aparece com 2+ controles (SELETOR-UNO-01). Com os quatro cards marcados, o que fica
marcado quando o alvo é "Todos" — os quatro, ou nenhum? Some, ou vira "marcar os quatro de
uma vez"?

### D-9 — Aplicar num controle desconectado é "aplicado" ou "guardado"?

Hoje a tela diz "aplicado" e o aparelho não recebeu nada: o override fica registrado e
pega no hotplug (`backend_pydualsense.py:3417-3423`), e o alvo é mantido de propósito
quando o controle some (R-16). É **vocabulário puro**, e decide o texto de todos os toasts
de Gatilhos e Lightbar.

### D-10 — A Navegação é "cada um escolhe o seu" ou "quem comanda o PC agora"?

**Esta tem evidência de um lado, e a palavra continua sendo dela.** Gatilho, luz e vibração
acontecem **no controle**: quatro escolhas, quatro aparelhos, nenhum conflito. Mouse e
teclado acontecem **no PC**, que tem um cursor e um foco de teclado.

| Opção | Preço |
|---|---|
| **"Quem comanda o PC agora"** — mostrar o dono, avisar quando troca, e deixar escolher | `is_primary` já chega no `state_full`; mas **poder escolher** o primário exige rota nova: hoje é `next(iter(self._handles), None)` (`backend_pydualsense.py:1944`), ordem de plugar |
| **"Cada um escolhe o seu"** — N leitores, N devices | esbarra no compositor (*inferido*), briga de grab com o co-op, e **reabre uma decisão dela**: o perfil PROÍBE `mouse` e `key_bindings` por unidade, com a razão escrita em `profiles/schema.py:642-655` e `extra="forbid"` em `:656` |

**A parte que aguenta por jogador**, se ela quiser meio-termo, é a **tabela de atalhos**: o
botão de cada controle digitando coisa diferente não esbarra em cursor nenhum.

---

## 7. As dívidas de fundo

Grandes demais para uma leva. Ficam registradas para não virarem surpresa.

**O leitor único.** Existe **um** `EvdevReader` no backend, re-atrelado ao primário a cada
hotplug (`backend_pydualsense.py:1955`), e é dele que saem `state` e `buttons_pressed` do
poll. Mouse, teclado, touchpad e **todos** os combos PS+X são privilégio exclusivo do
controle 1 — `read_state` diz isso em comentário próprio (`:2192-2195`). Isto não é
ajuste, é arquitetura; e barateia por o co-op **já** criar um `EvdevReader` por MAC, com
grab, em produção (`daemon/subsystems/coop.py`).

**A máscara por controle já está escrita e desligada.** Ver D-5.

**`rumble_active` é uma tupla, e devia ser mapa.** Ver D-4 — o conserto mata os três
defeitos de §4 de uma vez.

**O alvo não sobrevive ao restart.** `_output_target_key` só vive na RAM
(`backend_pydualsense.py:1165`). Ver §4.3.

---

## 8. O que este censo NÃO mediu

Escrito aqui para que a próxima sessão não confunda lacuna com achado.

- **A janela não foi aberta.** O aceite continua sendo o olho dela.
- **Nada foi provado com dois ou mais controles.** Um DualSense por USB, e só.
- **A aba "No jogo" não foi auditada — foi descoberta.** Tudo o que esta página diz sobre
  ela é leitura de `status_actions.py:541`, `:766-821` e `painel_no_jogo.py`. **Medi-la é
  o primeiro item de qualquer leva daqui**: planejar contra um mapa de nove abas é
  planejar contra um mapa incompleto.
- **Nenhum custo em minutos foi medido.** São estimativas dos agentes.
- **A geometria dos quatro cards (1626 px) não foi reconferida** neste transporte.
- **Os endereços de `controller_card.py` e `profiles_actions.py` estão ancorados em
  `cc768d4`** e vão derivar quando a leva de hoje for commitada.

---

## Procedência

| item | valor |
|---|---|
| Data | 13/08/2026 |
| Árvore | `cc768d4`, tag `v0.9.4.2`, branch `restauro/inicio-da-sessao` |
| Agentes | nove de medição (uma aba cada) + uma síntese + este transporte |
| Abas medidas | nove de dez — a **"No jogo"** ficou de fora |
| Modo | somente leitura; daemon dela vivo, um DualSense por USB, nada escrito no aparelho |
| Citações reconferidas | mais de quarenta; dez endereços corrigidos, **nenhum fato derrubado** |
