# ATIVAR-NÃO-MENTE-01 — o botão que parecia falhar, e ativava duas vezes

- **Achado em:** 05/08/2026, lendo o journal dela em busca de outra coisa: uma
  rajada de `profile_activated` idênticos, com um segundo de intervalo
- **Estado:** **CURA APLICADA** nos **dois** lados da fronteira, com nove
  mordidas verificadas uma a uma (05/08, neste documento)
- **Gravidade:** **ALTA** — é o botão principal da aba Perfis, e ele acusava um
  daemon vivo de estar morto **em toda ativação**
- **Causa-raiz:** **PROVADA no código e MEDIDA no journal dela**, com o daemon
  de produção
- **Síntese da leva:**
  [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  — defeitos **D-11**, **D-12** e **D-13**
- **Atravessa a fronteira Python↔Rust:** é a **única sprint desta leva** que
  muda código dos dois lados. Ver *"A fronteira"* — e a decisão de **não**
  esticar o timeout de leitura do applet
- **Irmã na mesma leva:**
  [SALVAR-NÃO-REBAIXA-02](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md)
  — mesmo botão de janela, defeito de escrita; **este** é de ativação

---

## O sintoma, nas palavras dela

Duas queixas que pareciam separadas, e são **o mesmo clique**:

1. *"clico em Ativar e ele diz que falhou"* — o toast lê **"Falha (daemon
   offline?)"** com o daemon vivo e o perfil **já ativo**;
2. *"o perfil que eu ativei não aplica imediatamente as features das abas"* —
   as abas seguem mostrando o perfil anterior.

E o efeito colateral que ninguém pediu: **cada clique é uma ativação real e
completa**. Ela clica de novo porque a tela disse que falhou.

## A prova, com o daemon de produção

**MEDIDO** — journal dela, 05/08:

```
02:40:22.106  profile_activated        name=Pragmata origin=manual
02:40:23.323  launch_env_materializado                       (+1,217 s)
02:40:23.378  profile_activated        name=Pragmata          (clicou de novo)
02:40:24.195  launch_env_materializado                       (+0,817 s)
02:40:24.201  profile_activated        name=Pragmata          (e de novo)
```

**A resposta chega em ~1,2 s. O cliente desistia aos 0,25 s.** E não há retry:
`cli/ipc_client.py:139-144` converte o `readline()` estourado em
`IpcError(-1, "conexão timeout")` e pronto.

**Grau da atribuição da rajada: SUSPEITA COM MECANISMO.** Não existe log do lado
da janela que prove o **gesto** — o `stderr` da janela não chega ao journal
(JANELA-FIEL-01). O espaçamento de ~1 s casa com re-clique humano depois do
toast; a DIV-3 da síntese registra que rajadas com **dezenas** de segundos de
intervalo (02:48:56 → 02:49:43 → 02:50:19) têm outro dono provável — a escolha
dela sendo desfeita pelo autoswitch. **Não são excludentes, e a atribuição de
cada rajada específica não foi fechada.**

## Causa-raiz 1: o timeout de LEITURA numa chamada que MUDA o mundo

`on_profile_activate` chamava `call_async` **sem** `timeout_s`, caindo no
default da ponte: `app/ipc_bridge.py:121`, `timeout_s: float = 0.25`.

Esse número é **certo para o que ele foi feito**: um `daemon.state_full` cabe
nele, e é curto de propósito para a janela não pendurar esperando um daemon
morto. Só que `profile.switch` **não é leitura**. O handler
(`daemon/ipc_handlers.py`) faz, antes de responder: `clear_manual_trigger_active`
→ `manager.activate` (gatilhos, LEDs, teclado, emulação, alto-falante) →
`save_active_marker` → `materialize_launch_env`.

**E o contraste estava no mesmo repositório, em três lugares:**

| chamada | folga | onde |
|---|---|---|
| `profile.apply_draft` (rodapé) | **1,5 s** | `app/actions/footer_actions.py:252` |
| `profile.apply_draft` (ponte) | **1,0 s** | `app/ipc_bridge.py:550` |
| trocar de modo | **2,0 s** | `app/actions/mode_transition.py:37` (`MODE_IPC_TIMEOUT_S`) |
| **`profile.switch`** | **0,25 s** | o default de leitura |

**O handler mais pesado da casa era o único no timeout de leitura.**

## Causa-raiz 2: a janela jogava fora o relatório do daemon

O `profile.switch` responde a verdade **desde a R-03**
(`daemon/ipc_handlers.py:470-492`): `active_profile`, `mode_aplicado`, `motivo`,
`secoes` e `expira_em_sec`.

A janela fazia `on_success=lambda _result: ...`. **Os únicos leitores de
`secoes` no repositório inteiro eram testes** — e o applet COSMIC também ignora
(`packaging/cosmic-applet/src/app.rs:223`).

Consequência: o toast dizia *"Perfil ativado: X"* mesmo quando o lock de gesto
manual fez os appliers descartarem **exatamente a seção que ela sente**. É o
mecanismo direto da queixa *"às vezes pega"*, e é irmão do que a
[TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md)
mediu: os **dois** canais que poderiam contar isso a ela estavam fechados.

**Nota de fronteira interna:** o outro lado deste par — fazer o daemon **relatar
na origem** as categorias que a trava manual silencia — é entrega da
[PERFIL-REESCRITO-NA-PARTIDA-01](2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md).
Esta sprint cuida de **ler** o relatório; aquela, de **preenchê-lo**. Uma sem a
outra deixaria a janela honesta sobre um relatório incompleto.

## Causa-raiz 3: "Ativar" não refazia aba nenhuma

`on_profile_activate` fazia `profile.switch` + toast + negrito na linha +
`_sync_selection_with_active_profile`. **Nenhum refresh.**

As abas só acompanhavam pelo tique de 2 Hz —
`_reconciliar_draft_com_perfil_ativo` (`app/app.py:827`, ligado em `:433`) — e
esse caminho **recusa** quando há edição pendente (`:863`,
`if self._tem_edicao_pendente(): <toast>; return`).

**Com qualquer edição pendente, as abas nunca acompanham.** É a queixa 2 dela,
verbatim, explicada linha a linha.

## A cura aplicada

### 1. Uma fonte só para o número

`app/ipc_bridge.py:49`:

```python
PROFILE_SWITCH_TIMEOUT_S: float = 3.0
```

Usada em **dois** lugares do Python: `on_profile_activate`
(`profiles_actions.py:1226`) e o helper síncrono `profile_switch`
(`ipc_bridge.py:271-282`).

**O segundo é o achado de graça desta sprint.** Quem lê o `bool` de
`profile_switch` é a **CLI** (`cmd_profile`), o **ciclador de perfil** e o
**Salvar da aba Perfis** — e os três anunciavam **falha de uma troca que tinha
acontecido**. Nenhum deles estava sendo investigado. **Grau: MEDIDO no código,
SEM medição ao vivo de cada um dos três.**

Três decisões:

1. **3,0 s, e não 1,5 s.** O medido é ~1,2 s numa máquina sem carga; o handler
   toca hidraw, uinput e disco. A folga é para o caso ruim, não para a média;
2. **constante exportada**, não número literal no callsite — é o que permite o
   teste do applet comparar os dois lados;
3. **o default da ponte NÃO foi mexido.** Esticar `timeout_s` em
   `ipc_bridge.py:121` curaria isto e penduraria **todo refresh de painel** por
   três segundos num daemon morto. **A chamada que muda o mundo ganha a folga
   que a leitura não pode ter** — é a mesma família (e a mesma cura) do
   `MODE_IPC_TIMEOUT_S`.

### 2. A fronteira: o espelho em Rust

**Esta é a única entrega desta leva que atravessa Python↔Rust**, e a razão é
simples: **os dois clientes falam com o MESMO daemon**. Curar um lado só
deixaria o defeito vivo no outro, com o mesmo sintoma e nenhuma pista.

`packaging/cosmic-applet/src/ipc.rs:49`:

```rust
const SWITCH_IPC_TIMEOUT: Duration = Duration::from_secs(3);
```

e `switch_profile` (`:361-372`) passou de `call_raw` para
`call_raw_with_timeout(..., SWITCH_IPC_TIMEOUT)`.

**A decisão que mais importa aqui é a que NÃO foi tomada:** o `IPC_TIMEOUT` de
leitura do applet (`ipc.rs:31`, 250 ms) **continua onde estava, de propósito**.
Ele cobre **todo** refresh do painel, e um applet que pendura 3 s num daemon
morto é um painel travado na barra dela. Por isso a folga é uma **constante
própria**, e não o número antigo esticado — exatamente o desenho que o
`MODE_IPC_TIMEOUT` do mesmo arquivo já tinha inaugurado. O cabeçalho do módulo
passou de *"São DOIS timeouts"* para *"São TRÊS timeouts"*, com o motivo de cada
um escrito ao lado.

**E os dois lados são amarrados por teste, nas duas direções:**

- do Python: `test_o_applet_tem_folga_propria_para_trocar_de_perfil` lê o
  `ipc.rs` e compara o número com `PROFILE_SWITCH_TIMEOUT_S`;
- do Rust: `timeout_do_switch_espelha_o_da_gui` afirma os 3 s e que
  `SWITCH_IPC_TIMEOUT > IPC_TIMEOUT`.

Ambos mordem a **fiação**, não só a constante: `switch_profile_usa_a_folga_e_nao_o_timeout_de_leitura`
(Rust) e `test_o_switch_do_applet_usa_a_folga` (Python) recortam o **corpo** da
função e exigem o nome lá dentro. **Constante certa com chamada errada não cura
nada** — é a forma de meia-entrega que a
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
existe para catalogar.

### 3. A janela LÊ o relatório — no vocabulário que já existia

`relato_da_ativacao` (`profiles_actions.py:345`) traduz o `secoes` do daemon
(`"aplicado"`, `"adiado_lock_manual"`, `"ignorado_*"`, `"falhou"`) para o
`applied`/`failed` que o rodapé já fala; `mensagem_de_ativacao` (`:371`)
**delega o texto a `footer_actions._mensagem_de_aplicacao`** (`:697`).

Três decisões, e as três são sobre **não** criar coisa nova:

1. **vocabulário reusado, nunca reescrito.** Dois donos da mesma frase derivam;
   é a regra RADAR-01/E4 de não inventar uma quarta frase de estado. Há teste
   que reprova se alguém escrever aqui uma segunda frase para a mesma ideia;
2. **`mode_aplicado` e `motivo` NÃO são lidos**, de propósito: os dois **derivam**
   de `secoes["mode"]` no daemon (`ipc_handlers.py:470-477`). Ler a fonte em vez
   dos derivados é o que impede as duas leituras de divergirem;
3. **sem relatório, sem alarme.** Daemon antigo, ou o `True` cru da ponte,
   mantêm a frase de sempre — a mesma regra que o irmão do rodapé já tinha
   (APLICAR-VERDADE-01).

### 4. Ativar refaz as abas — e a decisão é DELA

`_refazer_as_abas_apos_ativar` (`profiles_actions.py:1243`), chamado de
`_on_profile_switch_success` (`:1240`), recarrega pelo caminho canônico
`_bootstrap_draft_async` (worker, nada de disco na thread do GTK) com fallback
para `_refresh_all_tabs`.

**Com edição pendente, PERGUNTA** (`app/gui_dialogs.py:198-243`,
`confirm_discard_pending_edits`). O raciocínio está escrito na docstring e é o
coração desta entrega:

> Recarregar em silêncio seria trocar um jeito de perder trabalho por outro (é o
> que a R-08 já tinha decidido para o tique). Ignorar em silêncio deixa as abas
> mentindo.

**O default do diálogo é MANTER** o que ela não salvou
(`set_default_response(Gtk.ResponseType.CANCEL)`): *um Enter distraído nunca
pode custar edição não salva*. E quando ela manda manter, **o toast diz que as
abas seguem no perfil antigo** — manter em silêncio seria o defeito 3 de volta.

## O teste que morde

`tests/unit/test_ativar_nao_mente_01_o_botao_que_parecia_falhar.py` — **22
casos**, bancada hermética (dublês com a mesma API por-ID da aba; nenhum GTK
real, nenhum daemon, nenhuma escrita no `~/.config` dela). As respostas usadas
são as do journal dela, inclusive `RESPOSTA_COM_MODO_ADIADO`, que é a assinatura
do lock manual virada em fixture.

Do lado Rust, `packaging/cosmic-applet/src/ipc.rs` ganhou **4 testes** (dois com
daemon-dublê lento de 400 ms, um de fiação, um de espelho).

**Mordidas verificadas em 05/08, neste documento** — oito mutações cirúrgicas,
uma cura por vez, arrancada, rodada e devolvida:

| cura arrancada | reprovam |
|---|---|
| `PROFILE_SWITCH_TIMEOUT_S` de volta a `0.25` (o **número**) | **3** — `test_ativar_pede_a_folga_e_nao_o_timeout_de_leitura`, `test_a_folga_e_maior_que_a_leitura`, `test_o_applet_tem_folga_propria_para_trocar_de_perfil` |
| `timeout_s=PROFILE_SWITCH_TIMEOUT_S` no `on_profile_activate` (a **fiação**) | **1** — `test_ativar_pede_a_folga_e_nao_o_timeout_de_leitura` |
| a folga no helper síncrono `profile_switch` (CLI + Salvar) | **1** — `test_o_helper_sincrono_tambem_usa_a_folga` |
| `switch_profile` do applet de volta a `call_raw` | **1** — `test_o_switch_do_applet_usa_a_folga` |
| `on_success=lambda _result:` (o relatório descartado na fiação) | **1** — `test_o_callback_do_ativar_repassa_a_resposta` |
| `mensagem_de_ativacao` deixando de consultar o relato (a **regra**) | **5** — `test_secao_adiada_aparece_com_o_nome_que_ela_le`, `test_nada_aplicado_diz_o_que_o_rodape_diria`, `test_o_texto_do_que_nao_entrou_e_o_do_rodape`, `test_o_toast_da_ativacao_carrega_o_relatorio`, `test_o_callback_do_ativar_repassa_a_resposta` |
| o toast de volta ao `f"Perfil ativado: {name}"` (a **fiação**) | **2** — `test_o_toast_da_ativacao_carrega_o_relatorio`, `test_o_callback_do_ativar_repassa_a_resposta` |
| `_refazer_as_abas_apos_ativar` desligado | **3** — `test_ativar_recarrega_as_abas_do_perfil_ativado`, `test_com_edicao_pendente_a_decisao_e_dela`, `test_ela_pode_mandar_descartar` |

Devolvidas as oito curas: **22 verdes** (41 com a SALVAR-NÃO-REBAIXA-02 no mesmo
comando), e **`cargo test ipc::` = 16 passed, 0 failed** — 12 que já existiam
mais os 4 novos.

**Os pares número/fiação e regra/fiação são de propósito.** São mutações
diferentes e cada uma tem quem a acuse: **constante certa com chamada errada não
cura nada**, e é assim que uma entrega fica meio-ligada sem ninguém notar.

**Honestidade sobre o que NÃO morde.** **Treze** dos 22 mordem pelo menos uma
das oito mutações; os **nove** restantes passam em todas elas, e estão
declarados:

- **guardas anti-correção-demais**:
  `test_o_negrito_e_a_selecao_continuam_acontecendo` (a cura nova não pode
  custar o que já existia), `test_sem_recarregador_ainda_repinta_o_que_esta_em_memoria`
  (o fallback), `test_tudo_aplicado_mantem_a_frase_de_sempre` e
  `test_daemon_sem_relatorio_nao_levanta_suspeita` (o alarme não pode virar
  ruído), e **`test_a_leitura_do_applet_continua_curta`** — este último é o que
  **impede a "cura" preguiçosa** de esticar o `IPC_TIMEOUT` do painel e travá-lo
  três segundos num daemon morto;
- **os dois casos do tradutor puro** — `test_o_relato_traduz_secoes_para_applied_e_failed`
  e `test_secao_desconhecida_aparece_com_o_nome_tecnico`. Eles mordem a remoção
  do `relato_da_ativacao`, que não está entre as oito mutações acima;
- **tema e default do diálogo** — GUI-05/P5 (diálogo sem `_apply_app_theme` abre
  claro no COSMIC sob XWayland) e o `set_default_response` do MANTER.

## O que fica ABERTO

- **a cura não está rodando na máquina dela.** O daemon vivo é anterior a esta
  leva, e o install é *editable* — nada disto vale até o próximo start.
  **Reiniciar é decisão dela**, porque havia sessão de jogo viva (é o D-16 da
  síntese, e vale para a leva inteira, não só para esta sprint);
- **o applet continua ignorando o `secoes`** (`app.rs:223`). Ele ganhou a folga,
  não a leitura do relatório. É a mesma dívida que a janela acabou de pagar,
  no outro cliente;
- **`ipc_bridge.apply_draft()` ainda estreita a verdade para `bool`** —
  APLICAR-VERDADE-01/E2, aberta;
- **não há log do lado da janela** que prove o gesto dela (M-01). Enquanto o
  `stderr` da janela não chegar ao journal, a atribuição da rajada continua
  SUSPEITA. O instrumento irmão para a **escrita** de perfil já nasceu nesta
  leva (`profile_salvo`); o da **janela** não;
- **o aceite de tela.** O diálogo novo e o toast com o que não entrou **nunca
  foram fotografados**. Nenhuma afirmação aqui é sobre aparência, e interface
  não fecha sem o olho dela
  ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md));
- **a verificação em uso real.** A bancada prova a folga, o relatório e o
  refresh. Que o botão "Ativar" pare de mentir **na primeira vez**, no uso dela,
  só o uso dela fecha.
