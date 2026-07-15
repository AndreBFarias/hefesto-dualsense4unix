# Prompt — fechar as pendências de harmonia (cole numa sessão nova)

Levantadas pelos 6 revisores adversariais das ondas 2 e 3 (2026-07-15). Nenhuma é
regressão: são incompletudes do `SPRINT-HARMONIA-01`. Todas com arquivo:linha e
cenário concreto, já confirmadas por leitura de código.

---

Trabalhe no repo `/home/vitoriamaria/Desenvolvimento/hefesto-dualsense4unix`, no branch
`sprint/harmonia-uhid` (ou num branch a partir dele).

Leia primeiro, nesta ordem:
1. `docs/process/sprints/2026-07-15-INDEX-harmonia.md` — o mapa da onda e o contexto.
2. `docs/process/sprints/2026-07-15-sprint-harmonia-um-dono-por-conceito.md` — o sprint
   destes itens. A tese: **um dono por conceito**. O que quebra não é cada fix isolado,
   é a coexistência — o mesmo conceito com dois ou três donos que se sobrescrevem em
   silêncio.
3. `src/hefesto_dualsense4unix/app/actions/mode_transition.py` — o dono único da
   transição de modo, criado nessa onda. Boa parte do trabalho abaixo é **fazer as
   superfícies que sobraram passarem por ele** (ou pelo daemon).

## Regras da casa (não negociáveis)

- Gate: `.venv/bin/python -m pytest -q` + `.venv/bin/python -m ruff check src/ tests/`
  (ruff **pinado 0.15.20** — é o que o CI roda) + `mypy`. Applet: `cd
  packaging/cosmic-applet && cargo check`.
- **Sem emoji** em código/commit (há sanitizer no commit). Texto, comentário e docstring
  em **pt-BR com acento**.
- Comentário só onde explica o **porquê** que o código não mostra (armadilha, decisão,
  medição). Nunca narrando a linha seguinte. Siga o estilo do arquivo vizinho.
- Teste hermético; veja `tests/unit/test_home_render_state.py` e
  `test_mode_transition_um_dono.py` para o padrão de fake/monkeypatch.
- **Não use `git checkout`** em arquivo com trabalho não commitado (já custou código nesta
  onda).

## A lição que essa onda cobrou caro

**Gate verde não prova nada sobre hardware.** Oito bugs desta onda passavam em suíte
verde — inclusive um `& 0x01` que mataria 100% da vibração, com o fixture do teste
fossilizando o bit que o hardware nunca manda. Quando o item tocar comportamento real,
valide contra o daemon vivo (há 2 controles na máquina: 1 USB, 1 BT) e diga o que mediu.

Scripts de validação ao vivo prontos, no scratchpad da sessão anterior
(`/tmp/claude-1000/-home-vitoriamaria-.../scratchpad/`): `valida_onda2.py` (roteiro de
modos contra o daemon), `valida_harm16.py` (rumble ao sair do modo),
`valida_jogo_completo.py` (simula um jogo SDL sobre o vpad).

---

## Item 1 (HIGH) — O rodapé "Aplicar" ainda é um segundo dono do modo

`src/hefesto_dualsense4unix/app/actions/footer_actions.py:130` + `app/draft_config.py:381`

O aceite do `HARM-05` é **"nenhum 'Aplicar' muda o modo do sistema"**. O fix atual baixa o
`dirty` no callback de sucesso (`footer_actions.py:130`) — ou seja, **depois** de o
Aplicar já ter ido e voltado. O Aplicar danoso é justamente o primeiro, que a limpeza não
alcança.

Repro: Início em "Controlar o PC" → aba Mouse liga o switch → vá para "Jogar pelo Hefesto"
→ clique em "Aplicar" (por qualquer motivo: mudou um gatilho) → o payload leva
`mouse.enabled=true` → o daemon aplica a exclusão mútua → **o vpad morre no meio do jogo**.

Correção sugerida pelo revisor (avalie, não copie cego): o dono do liga/desliga do mouse é
o **modo**, então `enabled` não pode viajar num payload de Aplicar fora do modo desktop.
`to_ipc_dict` (`draft_config.py:381`) deixa de emitir a seção mouse — ou emite só
`speed`/`scroll_speed`, sem `enabled` — quando o modo vivo não é desktop.

**Aceite**: com o modo em gamepad, nenhum "Aplicar" derruba o vpad; teste que monta o
payload com o draft sujo e afirma que `enabled` não está lá.

## Item 2 (MED) — A CLI é o último segundo dono do modo

`src/hefesto_dualsense4unix/cli/cmd_gamepad.py:68` e `cli/cmd_native.py:45`

O Conceito 1 do sprint diz "Dono: aba Início. Ninguém mais decide modo". GUI e applet
foram convertidos; a CLI não. `gamepad on` manda `gamepad.emulation.set {enabled: True}`
cru — exatamente o que o `mode_transition` foi criado para abolir — e `native on` manda
`native.mode.set` sem desligar o gamepad. Resultado: a CLI reproduz o **jogo sem controle
nenhum** do `HARM-01` por fora da GUI.

O revisor propõe a cura de raiz, e ela é boa: **fechar no daemon**, que é o único ponto por
onde TODAS as superfícies passam (GUI, applet, CLI, perfil, hotkey, autoswitch) — a CLI não
pode importar `mode_transition` sem arrastar `app.ipc_bridge`/GTK. Em
`Daemon.set_gamepad_emulation(enabled=True)`, sair do nativo antes; em
`set_native_mode(True)`, derrubar o gamepad antes.

**Cuidado**: se o daemon passar a garantir a ordem, os passos extras do
`plan_mode_transition` viram redundância (não bug). Decida se o plano da GUI simplifica —
e se simplificar, o teste de paridade `tests/unit/test_applet_paridade_modo.py` precisa
acompanhar.

**Aceite**: `hefesto-dualsense4unix gamepad on` com o nativo ligado não deixa os dois
ligados juntos. Validar ao vivo (`valida_onda2.py` cobre o roteiro).

## Item 3 (MED) — HARM-16 incompleto: o terceiro caminho de saída

`src/hefesto_dualsense4unix/daemon/lifecycle.py:683`

O `zero_motors_on_mode_exit` foi ligado em 2 dos 3 caminhos: saída do Modo Nativo
(`lifecycle.py:534`) e `set_gamepad_emulation(False)` (`:812-815`). Ficou de fora
`set_mouse_emulation(enabled=True)`, que derruba o gamepad em `:683` via
`self._stop_gamepad_emulation()` — o wrapper de `:1307-1311`, que chama
`stop_gamepad_emulation(self)` direto, **sem zerar os motores**. O controle vibra para
sempre.

Correção sugerida (e é a tese do sprint): mover o zero para dentro do próprio
`subsystems.gamepad.stop_gamepad_emulation` — assim ele é **consequência de parar o vpad**
e não precisa ser lembrado em cada caller novo.

**Aceite**: os três caminhos zeram; teste por caminho. Validar com `valida_harm16.py`.

## Item 4 (MED) — Aba Rumble chuta um valor quando o daemon demora

`src/hefesto_dualsense4unix/app/actions/rumble_actions.py:119`

`_sync_policy_from_state` chama `daemon.state_full` sem `timeout_s` (default 0,25 s) e o
`_on_err` (`:115-117`) **afirma um valor**: `_apply_policy_to_widgets("balanceado", 0.7)`.
Cenário: o daemon está em `policy="max"`; a usuária abre a aba durante hotplug; o state_full
passa de 250 ms; a aba pinta "Balanceado / 70%" **por cima da política real**.

Correção: `timeout_s=STATE_IPC_TIMEOUT_S` (de `app.actions.mode_transition`) nas duas
chamadas, e o `_on_err` **não chuta** — sem resposta, a aba não sabe a política: deixe os
widgets como estão (ou marque indisponível). Nunca invente.

## Item 5 (MED) — Toast do rumble acusa o daemon de estar morto

`src/hefesto_dualsense4unix/app/actions/rumble_actions.py:223`

`rumble_policy_set` delega a `_safe_call`, cujo docstring (`ipc_bridge.py:73-84`) diz que
devolve `(False, None)` **também para erro JSON-RPC do servidor** — daemon VIVO que
recusou. O toast novo afirma categoricamente "O Hefesto não está rodando". O texto antigo
ao menos hesitava ("daemon offline?").

Correção: dar ao rumble o tratamento dos gatilhos — um `rumble_policy_set_checked` que
devolva `(ok, motivo)` distinguindo `IpcError` com `CODE_INVALID_PARAMS` (daemon vivo,
pedido recusado → mostrar o motivo) de erro de transporte (→ "O Hefesto não está rodando"),
com `timeout=STATE_IPC_TIMEOUT_S`.

## Item 6 (MED) — Applet: timeout de 250 ms para trocar de modo

`packaging/cosmic-applet/src/ipc.rs:28`

`IPC_TIMEOUT = 250ms` cobre **todas** as chamadas do applet, inclusive `native.mode.set` e
`gamepad.emulation.set`. A GUI já documenta que não cabe: `MODE_IPC_TIMEOUT_S = 2.0`
("trocar de modo cria uinput + grab"). E esta onda **dobrou a exposição**, ao fazer o
applet mandar 2-3 chamadas em vez de 1.

Correção: separar os dois timeouts, espelhando o que o `mode_transition` já elegeu —
`IPC_TIMEOUT` (250 ms) para leitura/refresh e um `MODE_IPC_TIMEOUT = Duration::from_secs(2)`
para as chamadas de modo (`call_raw` ganha um parâmetro, ou um `call_raw_with_timeout`).

## Item 7 (MED) — Applet oferece "Modo jogo" em "Controlando o PC"

`packaging/cosmic-applet/src/app.rs:465`

O `HARM-03` foi implementado só no GTK: `_sync_gamemode_button`
(`emulation_actions.py:338-361`) desabilita o botão em modo desktop e mostra a razão. O
applet segue oferecendo — e ligar lá deixa o controle **sem função nenhuma**.

Correção: usar `system_mode(state)` (já existe, `app.rs:792`) e, quando
`mode == SystemMode::Desktop && !game_mode`, remover o `.on_press` (menu_button sem
`on_press` já renderiza inerte no libcosmic). **Mantenha "Sair do modo jogo" sempre
sensível** — é a saída de emergência de quem caiu em desktop+suspenso pelo combo
PS+Options (foi decisão deliberada na GUI).

## Item 8 (MED) — Glossário da Início manda ligar "nesta aba"

`src/hefesto_dualsense4unix/app/actions/home_actions.py:102`

O `_GLOSSARY` termina em "Desligar Hefesto: para tudo até você ligar de novo **aqui nesta
aba**." A Início não tem botão de ligar — o único é o `shutdown_btn` (`:277`); o "Ligar o
Hefesto" mora na aba Sistema. Os outros dois textos da própria Início (`:341`, `:528`) já
dizem "aba Sistema" — estes é que estão certos.

Correção: alinhar a linha 102 com eles. (Ou dar o botão de ligar à Início — mas aí é
decisão de produto, não conserto de texto.)

---

## Ordem sugerida

Item 1 (é o único HIGH, e derruba o vpad no jogo) → Item 3 (mesma família: motor ligado) →
Item 2 (fecha o último dono do modo) → 4 e 5 (a aba Rumble parar de mentir) → 6, 7 (applet)
→ 8 (texto).

## Ao terminar

Rode o gate completo, valide ao vivo o que tocar comportamento, e **diga o que mediu** —
não "deve funcionar". Se um teste antigo falhar, entenda **por que** antes de mexer nele:
nesta onda um agente truncou uma feature real (o slider de vibração de 0-200%) porque
acreditou no handler em vez de investigar de onde vinha a faixa. O teste antigo estava
certo e o agente errado.
