# O backlog real, conferido contra o código

- **Levantado em:** 03/08/2026, sobre `restauro/inicio-da-sessao` (HEAD
  `19acbeb`, v0.8.0), varrendo as 82 sprints de `docs/process/sprints/` e
  conferindo **cada item aberto contra a árvore**
- **Natureza:** retrato verificado. Cada linha tem `arquivo:linha` de prova
- **Por que existe:** porque planejar pelos índices antigos custaria refazer
  trabalho pronto

---

## O ACHADO QUE MUDA O PLANEJAMENTO

> **Os índices estão defasados na direção pessimista.** Eles listam como aberto
> o que já foi entregue — e quem planejar por eles vai refazer trabalho.

| Onde | O índice diz | A árvore diz |
|---|---|---|
| `2026-07-31-INDICE:70-88` | ONDA 1 = **17 itens** por fazer | **16 pagos**; só o 1.10 aberto |
| `2026-07-31-INDICE:108` | CONTAGEM-E-COOP-01 falta a janela mostrar | entregue (`status_actions.py:184,1569,1923`) |
| `2026-07-31-INDICE:122` | `main` divergente, 17 commits | **divergência ZERADA** — `git rev-list --left-right --count main...HEAD` = `0 25`, e `main` (`670315d`) já é ancestral |
| `2026-07-30-INDICE:187` | LARGURA-01 "E2 a E9" | só **E7 e E8** |
| `2026-07-30-INDICE:188` | SOM-02 "E1 a E5 inteiras" | **entregue** (`ipc_server.py:130`, `controller_card.py:2623,2937`) |
| `2026-07-30-INDICE:162` | `chr(0x25CF)` "provável regressão viva" | `main` mesclada; U+25CF documentado (`status_actions.py:266`) |
| `2026-08-01-INDICE:24` | JOGO-COMPLETO-01 "ABERTA na E4" | E4 **em código**, staged e não commitado |

**E onze sprints dizem `Status: ABERTA` na linha 3 com o código de pé:**
`PERFIL-SALVA-TUDO-01`, `EMULACAO-NO-JOGO-01`, `SENSOR-VIVO-01` (E4/E5),
`AUTO-01`, `LEGIBILIDADE-01`, `MIC-USB-01`, `NUM-01`, `PLAYER-01`,
`UI-SELETOR-01`, `MODO-01` (B1/B2/B3/B5), `PERFIL-NASCE-CERTO-01` (E1/E2).

**A decisão 3.1 do índice de 31/07 — o `git push` mirando o repositório do
André — CADUCOU:** o `origin` é o fork dela e a divergência zerou.

---

## O backlog ABERTO e CONFIRMADO no código

Cada linha foi conferida por `grep` do símbolo citado na sprint.

### Perfis e automação

| Sprint | O que falta | Prova |
|---|---|---|
| **PERFIL-JOGO-01** E1,E3,E4,E5 | experimento nunca rodado; o cadeado cede por título; sem histerese no alt-tab; sem a frase de cor/jogador/preset | `profiles/autoswitch.py:237,260-262`; `profiles/manager.py:221-223`; `home_actions.py:1094-1102` |
| **AUTOMATISMO-MORTO-01** | o autoswitch segue morto pelos dois lados | doc **sem campo `Status:`**; único vestígio é comentário em `lifecycle.py:3233` |
| **SINAL-DE-JOGO-01** E1-E5 | a E5 (`healthy`→`seeing`) é a 3ª pendência herdada da JANELA-CEGA-01 desde 28/07 | `lifecycle.py:3279`, em `_gather_game_signal_inputs` (`:3260`) |
| **ESCOLHA-DELA-VENCE-01** E2,E3,E5 | restore não reaplica a máscara; recusa com jogo aberto é silenciosa; empate ainda por ordem de carga | `connection.py:223` (`mode_applier=None`); `gamepad.py:1432`; `manager.py:829` (`vencedor = empatados[0]`) |
| **PERFIL-JOGO-01** E6 | os seis `.json` dela com `xbox` gravado | **exige decisão dela** |

### Bluetooth, vpad e paridade

| Sprint | O que falta | Prova |
|---|---|---|
| **LIGHTBAR-BT-CLAIM-01** | cura **diagnosticada e não aplicada** | `lightbar_reset.py:125` (`__all__` sem o irmão do `0x31`); `backend_pydualsense.py:1533` (sem retomada), `:714` **desliga** o bit da cura |
| **BT-E-VPAD-01** furos 3 e 4 | bytes de áudio fora da replicação; PID do Edge não injetável | `uhid_gamepad.py:1711` e `:713` |
| **PARIDADE-SONY-01** E2 | portão fechou de novo; nenhuma fronteira da tabela tocada | `uhid_gamepad.py:1711` |
| **MIC-BT-01** caixas 2-4 | ponte só por env e CLI; **zero widget** | `daemon/subsystems/bt_mic.py:52`; custo só em docstring `:14-22` |
| **PAINEL-DA-VERDADE-01** E4(metade),E5 | "a fonte padrão não é esta" não chega ao card; o doctor afirma o que não mediu | `pactl get-default-source` só em `audio_control.py:108`; `doctor.sh:2526` |

### Steam, install e infra

| Sprint | O que falta | Prova |
|---|---|---|
| **DUPLO-REGISTRO-01** | dois cadastros do Steam Input, zero comparador | `storm_doctor.py:26` × `steam_launch_options.py:735` |
| **STEAM-INPUT-01** | o desfazer **dentro da janela** | `steam_launch_options.py:828`, único chamador `cli/cmd_steam.py:215` |
| **FONTE-PADRÃO-01** | a cura não tem vigia | `doctor.sh:1070` é o único chamador de `fix_default_source_monitor`; nenhum timer em `assets/` |
| **PROMESSA-NÃO-CUMPRIDA-01** C3,D,E,F | **E piorou**: 27 `inspect.getsource` (eram 21); 10 módulos com `_()` e 107+106 `msgstr ""` | `subsystems/__init__.py:13`; `packaging/nix/package.nix:79` |

### Interface

| Sprint | O que falta | Prova |
|---|---|---|
| **LIGHTBAR-JOGADOR-01** E0-E5 | **nenhuma linha entrou, em nenhuma leva** | `main.glade:1198,1265-1269`; `lightbar_actions.py:967`; `app.py:331`; grep do ID em `src/` = **0** |
| **CONTAGEM-01** E1 | externos ainda são número, não lista | `ipc_handlers.py:1803` |
| **IDENT-01** (inteira) | nenhum método de alias no IPC | `ipc_server.py:104-154` |
| **MÁSCARA-01** (inteira) | máscara é global/por perfil, não por aparelho; **depende da IDENT-01** | `launch_env.py:861`; `home_actions.py:239` |
| **JOGO-01** E2 | a decisão (Steam Input × Hefesto) não aparece na tela | `gamepad.py:318` registra a pendência **no próprio código** |
| **PLAYER-LED-01** E1 + meia E4 | trava de log global, com o dado ao lado já por `uniq` | `backend_pydualsense.py:918` (lida `:2967`, re-armada `:3015`) |
| **ABAS-01** ABAS-07/08 · **LARGURA-01** E7/E8 · **VÃO-01** E5 | sem vestígio no código; a VÃO-01/E5 ficou fora **por decisão** de 27/07 | grep dos IDs = 0 |
| **GATILHO-PALAVRA-01** | rótulo `Custom` (24 chars, teto 22) — **palavra dela** | `trigger_specs.py:227`; exceção viva em `test_gatilho_palavra_rotulos.py:68` |
| **PALAVRA-01** E5 | o 5º hook existe mas é `referencias-docs`, não capitalização | `.pre-commit-config.yaml:59` |
| **RADAR-01** E1,E2 | applet e bandeja **nunca abertos** (E3/E4 pagas) | `packaging/cosmic-applet/Cargo.toml` nunca construído |

### Testes e processo

| Sprint | O que falta | Prova |
|---|---|---|
| **TESTE-HONESTO-01** E1,E2,E3 | 17 arquivos na `DIVIDA_GI_FALSO`, **zero pagos**; **9 `transport="bt"` contra 202 `"usb"`**, e **zero** marcador de skip por hardware BT | `test_guarda_gi_falso_precisa_de_exigir_gi_real.py:50-70` |
| **DOC-VERDADE-01/02** | **sete das nove** contradições persistem | `2026-07-31-DOC-VERDADE-02:60` |
| **CR-01,03,04,05,06** | CR-01 = a decisão de licença; CR-04 bloqueada pela CR-03; CR-06 pela CR-04; CR-05 = a cópia da GPL-2.0 | não existe `LICENSES/` nem `COPYING` na raiz |
| **CHECKLIST hardware** | **31 de 31 caixas vazias** | `2026-07-25-CHECKLIST-validacao-em-hardware.md` |

---

## O QUE FICOU PELO CAMINHO

Itens de índices de 26/07 a 31/07 que **sumiram dos índices novos sem terem sido
entregues nem cancelados**. Esta seção é o valor principal do levantamento.

1. **As cinco caixas fantasma `player_led_1..5` no glade.** Nomeadas em
   `2026-07-27-INDICE-o-que-ficou-pelo-caminho.md:43-46`, nunca mais citadas.
   Vivas em `gui/main.glade:1265-1269`.
2. **A escala de fonte máxima (8) nunca foi medida.** `app/theme.py:50` define
   `ESCALA_MAXIMA = 8` e **zero** teste cita a constante. **Todo o
   orçamento de largura da casa foi medido na escala 3.**
3. **VÃO-01/E5, os tokens de espaçamento** — deixada fora "de propósito, é a
   única não reversível em uma linha". Nenhum índice posterior a menciona.
4. **`display_authority` é grudento e cai sozinho com o jogo aberto.** O índice
   de 30/07 (dívida 2) diz por extenso: *"defeito conhecido e não corrigido.
   Continua vivo e não tem documento nenhum"*. Sumiu do índice de 31/07 em
   diante. Vivo em `gamepad.py:1005`. **É parente da SINAL-DE-JOGO-01.**
5. **"Verde aqui é afirmação fraca" nunca virou regra escrita.** O gate de
   acentuação é cego a f-string no 3.12 e o CI roda 3.10/3.11. Nenhum arquivo de
   `docs/` registra isso hoje.
6. **O checklist de 22 itens do que ela precisa olhar existe só na conversa** —
   e a conversa fechou.
7. **Os 438 `replace refs` do `filter-repo`.** Medido agora: `git replace -l`
   devolve **438**. **Toda arqueologia por hash antigo devolve conteúdo
   diferente em silêncio.**
8. **A ONDA 3 inteira do índice de 31/07 — as dez perguntas que esperam decisão
   dela.** Nenhuma aparece no índice de 01/08. Continuam abertas, entre elas:
   os rótulos `(Rigid)`/`(Bow)`/`(Galloping)`; **o `[REDACTED]` no README**
   (confirmado vivo em `README.md:14`, `:89`, `:335`); o `Custom`; o que o R1
   deve fazer; `pragmata.json` × `pragmata2.json`; o hold do PS, o drop-in 51 e
   a migração dos seis presets. *(A 3.5 resolveu-se sozinha.)*
9. **RADAR-01/E1 e E2 — o applet e a bandeja.** O item 2.7 do índice de 31/07
   some no de 01/08.
10. **`autoswitch_locked.flag` ligado desde 24/07**, e nenhuma sprint de perfil
    diz o que muda com o cadeado ligado.
11. **Os três nomes órfãos de 26/07** — `PERFIL-FIRME-01`, `STEAM-UMA-CHAVE-01`,
    `STEAM-INPUT-SELF-HEAL-01`. O último tem 1 referência viva em `src/`.
12. **`JANELA-CEGA-02` e `TESTE-QUE-MEDE-01`** — nomeadas no índice de 29/07
    como sprints a escrever. Nunca escritas.
13. **O banner da sprint cancelada aponta para arquivo inexistente:**
    `docs/history/sprints-canceladas/PROFILE-DISPLAY-NAME-01_SUPERSEDED.md:10`
    manda ler `PROFILE-SLUG-SEPARATION-01`, que não existe. *(A substituta está
    no código: `profiles/slug.py`.)*

---

## DÍVIDA DOCUMENTAL — os IDs sem documento

Os quatro que o índice de 01/08 nomeia estão **confirmados**, e há muito mais.
Todos citados em `src/`/`tests/`, com **zero** menção em `docs/`:

| ID | citações | nasceu |
|---|---|---|
| **`GUARDA-GI-REAL-01`** | **54** | 28/07 |
| `SOM-CANAL-01` | 19 | 02/08 |
| `HONESTIDADE-STEAM-01` | 15 | 25/07 |
| `CLONE-01` | 14 | 25/07 |
| `LOCK-CEDE-01` | 11 | 25/07 |
| `SALVAR-NAO-REBAIXA-01` | 11 | 28/07 |
| `MIC-REGISTRY-01` · `RUMBLE-PRESO-01` | 9 cada | 25/07 · herdado |
| `AUDIO-STATUS-01` · `EMPILHA-01` · `STATUS-GRID-2COL-01` · `FONTE-PADRAO-01` | 6 cada | 25/07-30/07 |
| `EMPILHA-02` · `GYRO-BT-SILENCIO-01` | 5 cada | 02/08 · 25/07 |
| `ALLOWLIST-SUPRESSAO-01` | 4 | 25/07 |
| `HOTKEY-EXPOSE-01` · `TYPELIB-PARCIAL-01` | 3 cada | 25/07 |
| `BROADCAST-QUE-NAO-MENTE-01` | 2 | 02/08 (não commitado) |
| `SOLTAR-01` · `BLUEZ-PADRAO-INVERTIDO-01` · `ROTA-ORFA-01` · `PROPOSTA-01` · `STATUS-3-LINHAS-01` · `MIC-CAPTURA-01` | 1-2 cada | 28/07-02/08 |

**`GUARDA-GI-REAL-01` é o maior: 54 citações, e é a maior mudança de
confiabilidade da suíte** (o `exigir_gi_real` que matou os 737 falsos-verdes).
Vive só em mensagem de commit. O índice de 29/07 já lhe dera nome
(`TESTE-QUE-MEDE-01`); nunca virou arquivo.

**Rastreáveis dentro de outra sprint** (dívida mais leve): `SOM-03`, `SOM-04`,
`TOUCH-CLICK-01`, `ESTADO-TRES-LINHAS-01`, `SOM-ROTA-NO-CARD-01`,
`MASCARA-CUSTO-01`, `SOM-ROTULO-01`, `ABAS-02/03/04`, `AUDIO-OWNER-01`,
`EXT-COUNT-01`, `VERSOES-RANCOSAS-01`, `CI-GUI-PULAVA-CALADO-01`, `FOCO-01`.

**Entregue e sem documento:** `PACOTE-COM-NOME-01` (`release.yml:257-267`).
**Dívida puramente histórica** (zero referência no código hoje): `MIC-FAIXA-01`,
`SLOT-JOGADOR-01`.

**Nota de método:** o `validar-referencias-docs.py` acha **link morto**, não **ID
órfão** — é cego a esta classe inteira. Fora da era atual há ~300 IDs legados
(`FEAT-*`, `BUG-*`, `AUDIT-FINDING-*`), anteriores a 25/07, que são tags de
commit de outra era e **não** devem entrar num portão.

---

## O que exige a mão dela (nenhuma quantidade de leitura resolve)

`PERFIL-JOGO-01`/E6 (os seis `.json` com `xbox`) · `SOM-ROTA-01`/E2 (remedir a
régua do volume com o pré-amp — `core/speaker_scale.py:33`) ·
`BT-E-VPAD-01` furo 5 (a taxa declarada do Edge, e **só contra a SDL3 da
Steam**) · `PARIDADE-SONY-01` (a medição em jogo) · `TRIGGER-CANON-01` (o aceite
nos sete presets curados) · o CHECKLIST 31/31 · o olho dela em
`JANELA-QUE-RESPIRA-01`, `CARD-ÚNICO-01` e `ALINHA-DUAS-LINHAS-01` ·
`PROMESSA`/B4 (o `install.sh` foi reescrito; a equivalência não foi medida).
