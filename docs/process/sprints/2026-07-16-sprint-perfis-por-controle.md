# Sprint 2026-07-16 — Perfis por controle (fundação 4P-01/4P-02): identidade por MAC, estado por controle, mapa no perfil e autoload do perfil da usuária

**STATUS: PLANO. Nada desta frente foi construído.** Este doc é o desenho, já corrigido por
três revisões adversariais independentes (lentes técnica, regressão e escopo). Branch
`sprint/harmonia-uhid`.

Pedido da Vitória (2026-07-16, palavras dela): *"cliquei no 1 - BT para mexer no lightbar
dele, mas se eu configurar todas as settings específicas pra ele, ele deveria funcionar
exclusivo dele e isso deveria ficar salvo para aquele controle dentro do meu perfil"* — e o
perfil `vitoria` *"deve ser LIDO SEMPRE que abrir o programa"*.

Invariante do projeto que este doc honra: **teste verde sem validação ao vivo NÃO fecha
item** (PERFIL-05 é o portão humano). E a regra de ouro ditada por ela: *"tudo tem que tá
no install funcionando SEM FLAGS"* — ver §Regra de ouro (esta frente não toca install por
construção, e os três revisores confirmaram isso de forma independente).

## TL;DR

O seletor de controle (50e76c4) funciona AO VIVO (lightbar/gatilhos/player-LED/mic-LED/
rumble-teste miram 1 controle), mas **nada disso persiste**: o backend guarda **UM**
`_DesiredOutput` global, o schema de perfil é flat (`extra="forbid"`) sem lugar para
settings por controle, e o autoswitch **sobrescreve** o session.json a cada troca de
janela — ao vivo, o session.json dela diz `"Navegação"`, não `"vitoria"`. A identidade
estável já existe e foi **PROVADA AO VIVO**: o MAC Bluetooth (`HID_UNIQ` == serial hidapi)
é o MESMO no cabo e no BT para o mesmo DualSense. O plano: (1) estado desejado
**por-uniq** no backend com **merge por campo** e **reset na ativação de perfil**;
(2) mapa aditivo `controllers` no Profile, **omitido do JSON quando vazio**, com o draft
da GUI transportando o mapa **na mesma entrega** (histórico: `to_profile()` já apagou
seções duas vezes); (3) autoload que separa **gesto manual** de **autoswitch** (5 call
sites de `activate()`, não 3); (4) GUI editando por-controle de verdade. Itens
PERFIL-01/02/03/04 são **P0 e uma unidade de entrega** — 01+02 sem a GUI só se usam
editando JSON à mão, que é exatamente a burocracia que a regra de ouro proíbe.

## O que foi provado (honestidade brutal sobre o nível de prova)

### PROVADO AO VIVO (na máquina dela, hoje)

- **Identidade = MAC BT, estável entre USB e BT.** O DualSense no cabo expõe
  `HID_UNIQ=a0:fa:9c:00:00:01` (bus 0003/USB) e esse exato MAC está no cache do BlueZ
  como "DualSense Wireless Controller"; o do BT expõe `14:3a:9a:00:00:04` == MAC pareado
  no bluetoothctl. Todos os nós evdev do mesmo controle carregam o mesmo uniq
  (event17-20 vs event22/27/28). Re-provado por DOIS revisores de forma independente.
- **O autoload está quebrado na prática.** `session.json = {"last_profile": "Navegação"}`
  com `vitoria.json` presente (prioridade 5, MatchAny) — `navegacao.json` (prioridade 50,
  criteria: firefox/chrome/steam/terminal) pisa nela sempre que um browser foca.
- **`active_profile.txt` ao vivo contém `vitoria`** (mtime 07-14, o último gesto manual
  dela) enquanto session.json diz `Navegação` — o codebase JÁ separa gesto manual de
  autoswitch nesse marker; o restore é que lê o arquivo errado.
- **Uniq degenerado fora do DualSense.** Na mesma máquina: Pro Controller USB expõe
  `HID_UNIQ=000000000001` (colidiria entre duas unidades); receivers 2.4G (8BitDo) expõem
  uniq VAZIO. A garantia MAC-como-chave é **DualSense-only**.

### PROVADO NO CÓDIGO (linha a linha, conferido por 3 revisores)

- `_desired` é um único objeto global: `backend_pydualsense.py:294`; todos os setters
  gravam nele ANTES de resolver o alvo (`set_trigger` :908-913, `set_led` :915-916,
  `set_mic_led` :942, `set_player_leds` :964); o hotplug (`connect` :553-556 →
  `_reapply_desired` :871-906) e o reassert sysfs (:668-676) aplicam o global a QUALQUER
  controle novo → o ajuste "só do Controle 2" contamina o Controle 1 no replug (é o
  4P-01; zero referências em `src/`).
- **Agravante**: `ProfileManager.apply()` (manager.py:140-148) usa setters broadcast que
  respeitam `_output_target_key` (backend :800-805, :830-835) — com um alvo selecionado
  na GUI, **ativar um perfil aplica só no alvo**. E é PIOR: o **autoswitch** passa pelo
  mesmo caminho (autoswitch.py:159), então toda troca automática com alvo ativo também
  aplica só no alvo.
- Schema flat: `Profile` com `extra="forbid"` (schema.py:281), sem mapa por-controle;
  `DraftConfig` idem e declara "Persistência entre sessões NÃO é escopo".
- `activate()` grava session.json em TODA ativação (manager.py:127-128) e o autoswitch
  chama `activate()` (autoswitch.py:159); o restore de boot lê session.json
  (connection.py:80-87).
- A chave do backend já é o serial hidapi (== HID_UNIQ == MAC), com guarda de 12 hex e
  fallback por path (`_enumerate_device_keys` :400-428, `_key_to_uniq` :1014-1029); o
  vpad uhid é excluído da enumeração por `_is_virtual_hidraw` (:57-80) — o MAC forjado
  `02:fe:00:00:00:0N` **não** contamina o mapa.
- O co-op já é keyed por MAC e atribui player-LED por controle via sysfs
  (coop.py:460-497) — prova que o padrão por-uniq funciona; e lê o `_desired` global por
  `getattr(ctrl, "_desired", None)` como "padrão do perfil" (:509-513).
- O IPC já expõe uniq + bateria por controle (`ipc_handlers.py:367-399`,
  `describe_controllers` :977-1012) — a GUI tem o que precisa.
- `save_profile` serializa `model_dump(mode="json")` **sem** exclude (loader.py:429-486);
  o vitoria.json em disco já carrega `"mouse": null` etc. — executado pelo revisor: um
  campo novo `controllers=None` apareceria como `"controllers": null` em TODO save.
- `save_last_profile` **reescreve o session.json inteiro** com só `{last_profile}`
  (session.py:36-49); o próprio módulo avisa da armadilha (:238-239, caso do mouse).
- `to_profile()` do draft **reconstrói o Profile do zero** (footer_actions.py:225 +
  draft_config.py:159-168) — a classe de bug que já apagou seções DUAS vezes
  (BUG-FOOTER-SAVE-DROPS-SECTIONS-01, BUG-MOUSE-SAVE-DROPS-SECTION-01).

### HIPÓTESE (plausível, sem prova ainda)

- A corrida do `apply_game_rumble` (gamepad.py:181-199 flipa `_output_target_key`
  temporariamente; setters rodam em executor `max_workers=2`) hoje só mis-roteia UMA
  escrita transitória — **com desired keyed pelo alvo lido na hora, persistiria config no
  controle errado**. Nunca foi observada ao vivo; é risco de desenho, tratado no
  PERFIL-01 por construção (API por-uniq com alvo resolvido na borda).

## Veredicto da revisão adversarial (3 lentes)

**Causa-raiz: SOBREVIVE nas 3 lentes. Solução: SOBREVIVE, mas SÓ com as correções
obrigatórias abaixo** — quatro pedaços do desenho original foram **REFUTADOS** e este doc
já os substitui:

1. **REFUTADO** o aceite "perfil antigo round-trip byte-idêntico" com campo
   `controllers: ... | None`: sem omissão do campo quando None, todo save grava
   `"controllers": null` → aceite inatingível E **todo** perfil salvo pelo binário novo
   seria rejeitado por binário antigo no downgrade (não só os com mapa). → A omissão do
   campo virou **requisito de compatibilidade** (PERFIL-02).
2. **REFUTADA** a resolução `by_uniq.get(uniq) or default` por OBJETO: com override
   PARCIAL (só triggers), o replug aplicaria `led=None` como no-op e o controle ficaria
   sem a cor global. → **Merge POR CAMPO** (PERFIL-01).
3. **REFUTADO** `default_profile` como chave em session.json: `save_last_profile`
   clobbera o arquivo inteiro — a primeira ativação manual apagaria a chave. → Read-
   modify-write preservando chaves desconhecidas OU arquivo próprio (PERFIL-03).
4. **REFUTADO** o aceite ao vivo "abrir a GUI após reboot → mostra vitoria roxo": o
   autoswitch continua mandando conforme a janela focada (contrato preservado de
   propósito) — Navegação/50 reativa ~1s após o restore se um browser/Steam focar. → O
   aceite virou determinístico: session.json + log `last_profile_restored` (PERFIL-03),
   e a decisão de produto sobre autoswitch está explícita (§Honestidade).
5. **REFUTADO** o campo `label` em ControllerOverrides (ela não pediu; identidade visível
   é o 4P-03, outra frente). → Cortado: overrides = `{leds?, triggers?}` apenas.
6. **REFUTADO** o sequenciamento "PERFIL-02 (P0) independente de PERFIL-04 (P1)": shipar
   o campo no schema sem o draft transportá-lo apaga o mapa no primeiro "Salvar Perfil".
   → Transporte do mapa no draft entra no PERFIL-02; PERFIL-04 **promovido a P0**;
   01+02+04 são **uma unidade de entrega**.

## Tabela honesta: setting → estado HOJE (corrigida pela revisão)

| Setting | Alvo ao vivo (seletor) | Persiste no perfil | Vaza no hotplug | Escopo desta frente |
|---|---|---|---|---|
| Lightbar cor/brilho | sim | GLOBAL | sim | **por-controle** |
| Player-LEDs | sim (+ co-op por MAC) | GLOBAL | sim | **por-controle** (co-op vence durante co-op) |
| Gatilhos L2/R2 | sim | GLOBAL | sim | **por-controle** |
| Rumble-teste | sim | não (correto) | n/a | fora (transitório) |
| Mic-LED | sim | **não persiste no PERFIL por decisão** (AUDIT-FINDING-PROFILE-MIC-LED-RESET-01), mas **persiste sim no `_desired` em memória e VAZA no hotplug** (backend :942/:903-904) | sim | fora do mapa nesta fase; o vazamento é curado de carona pelo PERFIL-01 |
| Política de rumble | — | GLOBAL | — | segue GLOBAL |
| Máscara/flavor | — | GLOBAL (co-op recria todos os vpads no flavor global) | — | segue GLOBAL |
| Modo (native/gamepad/desktop) | — | GLOBAL | — | segue GLOBAL |
| Mouse/teclado | só primário | GLOBAL | — | segue GLOBAL |
| Co-op | — | GLOBAL (jogadores keyed por MAC — bom) | — | segue GLOBAL |
| Seletor de alvo | in-memory | nunca persistido (correto: estado de UI) | — | segue in-memory |

**Declaração honesta de escopo** (exigida pela revisão): o "por-controle" desta fase é
**leds (lightbar + player_leds) + gatilhos**, keyed por MAC 12-hex, **DualSense-only**.
O pedido dela fala "todas as settings específicas pra ele" — este doc NÃO vende mais do
que entrega: rumble-policy, modo, máscara, mouse/teclado e co-op seguem globais.
Controles com uniq vazio/degenerado (medido nesta máquina: receivers 8BitDo, Pro
Controller `000000000001`) ficam fora do mapa, com log claro em vez de silêncio.

## Desenho em 4 camadas (já com as correções obrigatórias)

### Camada 1 — Fundação (=4P-01): desired por-uniq no backend

- `_desired` único → `_desired_default` (broadcast) + `_desired_by_uniq:
  dict[mac_12hex, _DesiredOutput]`.
- **Merge POR CAMPO** no hotplug/reassert: `campo = override.campo if not None else
  default.campo` — NUNCA resolução por objeto (refutada; override parcial apagaria a cor
  global).
- **Ciclo de vida explícito** (buraco apontado pelas 3 lentes): a ativação de perfil
  **SUBSTITUI o mapa inteiro** (clear + popular de `profile.controllers`, vazio se
  ausente) — senão o override do perfil anterior ressuscita no hotplug sob o perfil novo
  (e o autoswitch troca de perfil o dia inteiro). Um broadcast ao vivo da GUI ("Todos")
  **limpa a entrada por-uniq do campo escrito** — senão "mudei todos para azul, repluguei
  e um voltou verde".
- **Overrides de controles DESCONECTADOS são REGISTRADOS no mapa** na ativação (só a
  escrita de hardware é pulada) — o hotplug lê o mapa em memória, não o JSON do perfil;
  "ignorar o desconectado" tornaria falso o "aplica quando chegar".
- **API por-uniq explícita** no IController (ex.: `apply_output_for(uniq, parcial)`) que
  NÃO passa pelo `_output_target_key` — e o alvo das escritas da GUI/IPC é **resolvido na
  borda e passado como parâmetro** para TODOS os setters (ou exclusão mútua com o flip do
  `apply_game_rumble`): com desired keyed pelo alvo lido de um global mutável, a corrida
  com o executor multi-thread persistiria config no controle errado.
- **coop.py NO MESMO ITEM**: `_profile_player_leds` lê `getattr(ctrl, "_desired", None)`
  (coop.py:509-513) — um rename seco falha **EM SILÊNCIO** (co-op desligado pararia de
  restaurar o player-LED do perfil, sem teste quebrando). Manter property/alias
  `_desired` → default OU atualizar coop.py, com teste de regressão do revert.
- `ProfileManager.apply()` migra para a API por-uniq em broadcast — corrige o bug
  "perfil aplicado com alvo selecionado só atinge o alvo" nos DOIS caminhos (manual e
  autoswitch).

### Camada 2 — Schema: mapa `controllers` dentro do perfil

- Campo aditivo opcional `controllers: dict[str, ControllerOverrides] | None = None` no
  Profile, keyed por MAC normalizado (12 hex, o mesmo `norm_mac` do backend), validador
  rejeitando key não-12-hex. `ControllerOverrides = {leds?, triggers?}` — tudo opcional,
  `extra="forbid"`. **SEM `label`** (cortado pela revisão: identidade visível é 4P-03).
  **SEM `mic_led`** (decisão deliberada do projeto: mic jamais colateral de profile
  switch — led_control.py:106-111).
- **Serialização OMITE o campo quando None/vazio** (serializer custom ou pop pós-
  `model_dump` em `save_profile`) — requisito de compatibilidade, não estética: sem isso,
  TODO perfil salvo pelo binário novo é rejeitado por binário antigo (`extra="forbid"`),
  não só os que usam o mapa.
- `ProfileManager.apply()`: seção global em broadcast → substitui o mapa por-uniq (ver
  camada 1) → aplica cada override em controle conectado via API por-uniq; desconectado
  fica registrado no mapa para o hotplug.
- **Transporte no draft NA MESMA ENTREGA**: `DraftConfig` ganha passthrough do mapa
  (ex.: `source_controllers`, mesmo padrão dos `source_*` existentes) — `to_profile()`
  reconstrói o Profile do zero e apagaria `controllers` no primeiro "Salvar Perfil"
  (classe de bug já ocorrida 2x). O aceite inclui round-trip
  `DraftConfig.from_profile → to_profile`, não só o loader.

### Camada 3 — Autoload: gesto manual ≠ autoswitch

- `activate()` ganha `origin`; `save_last_profile` só roda em **gesto manual**. Os call
  sites são **CINCO**, não três (a revisão achou dois esquecidos):

  | Call site | Origem | Grava session.json? |
  |---|---|---|
  | `ipc_handlers.py:78` (profile.switch GUI/CLI) | manual | **sim** |
  | `hotkey.py:146` (ciclo PS+dpad, botão físico) | manual | **sim** (faltava na lista original) |
  | `autoswitch.py:159` | automática | não (o fix inteiro) |
  | `connection.py:132` (restore de boot) | sistema | não |
  | `lifecycle.py:599` (saída do Modo Nativo) | sistema | não — **e passa a preferir `store.active_profile`** em vez de `load_last_profile()`: com a nova semântica, sair do nativo re-aplicaria a última escolha MANUAL em vez do perfil ativo pelo autoswitch (mudança não intencional) |

- **Reconciliação com `active_profile.txt`** (achado da lente de regressão): esse marker
  JÁ é manual-only (escrito só por profile.switch e hotkey) e ao vivo contém exatamente
  `vitoria`. Decisão: ele vira o **SEED de migração** — no 1º boot pós-update, se
  session.json aponta perfil que não foi escolha manual, o restore prefere o marker.
  Sem o seed, o 1º restore pós-update ainda ativa "Navegação". Pós-fix, os dois arquivos
  convergem (mesma semântica manual-only) — documentar qual é o canônico (session.json)
  e manter o marker em paridade como hoje.
- **`default_profile` NÃO entra em session.json como está**: ou `save_last_profile` vira
  read-modify-write preservando chaves desconhecidas (com teste), ou arquivo próprio
  (padrão flag-file já existente em utils/session.py). O botão "Usar este perfil ao
  iniciar" é **opcional pós-validação**: o origin-fix sozinho atende "vitoria lido sempre
  que abrir o programa" — entregar o fix primeiro, botão só se a validação ao vivo
  mostrar necessidade.

### Camada 4 — GUI: editar por-controle de verdade

- Seletor num controle específico ("1 - BT") → mudanças de lightbar/gatilhos vão para
  `draft.controllers[uniq]` com badge visível "editando: Controle 1 (BT)"; em "Todos",
  edita a seção global como hoje. "Salvar Perfil" persiste o mapa DENTRO do mesmo
  vitoria.json; "Aplicar" envia via apply_draft com os overrides.
- **Brilho** (achado da lente de escopo): `_DesiredOutput` NÃO guarda
  `lightbar_brightness` — `apply_led_settings` pré-escala o RGB antes do `set_led`
  (led_control.py:113-115). O override por-controle de brilho passa pelo MESMO caminho de
  escala na aplicação, e a GUI lê o brilho **do PERFIL** (não do backend) ao exibir o
  override — senão o valor mostrado diverge do salvo.
- Botões segmentados SEMPRE (nunca dropdown — cosmic-epoch#2497).

## Itens do sprint

> PERFIL-01 + 02 + 04 são **UMA unidade de entrega** (exigência da revisão de escopo):
> 01+02 sem a GUI só se usam editando JSON à mão — a burocracia que a regra de ouro
> proíbe. Não declarar os P0 concluídos sem o caminho visível para ela.

### PERFIL-01 — FUNDAÇÃO (=4P-01): desired POR CONTROLE + API por-uniq `[P0] [CLAUDE]`

**O que fazer**: camada 1 inteira — `_desired_default` + `_desired_by_uniq`, merge POR
CAMPO, reset do mapa na ativação, registro de desconectados, API por-uniq
(`apply_output_for`) sem `_output_target_key`, alvo resolvido na borda para todos os
setters (ou exclusão mútua com o flip do `apply_game_rumble`), `ProfileManager.apply()`
via API por-uniq, e **coop.py atualizado no mesmo commit** (alias/property `_desired` ou
leitura nova, + teste do revert).

**Arquivos**: `src/hefesto_dualsense4unix/core/backend_pydualsense.py`,
`src/hefesto_dualsense4unix/core/controller.py`,
`src/hefesto_dualsense4unix/profiles/manager.py`,
`src/hefesto_dualsense4unix/daemon/subsystems/coop.py`,
`src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py`,
`tests/unit/test_backend_output_target.py`, `tests/unit/test_backend_multi_controller.py`.

**Critério de aceite (verificável)** — testes herméticos novos, TODOS obrigatórios:
1. 2 keys stubadas: cor A broadcast + cor B só na key2; hotplug-out/in da key1 → key1
   recebe A (não B); replug da key2 → recebe B.
2. **Override PARCIAL** (exigido pela revisão): key2 só com triggers no override → replug
   da key2 recebe os triggers do override E a **cor global** (merge por campo).
3. **Reset na ativação**: ativar perfil COM override na key2, depois ativar perfil SEM
   `controllers`, replug da key2 → recebe o default do perfil novo (nada ressuscita).
4. Com alvo=key2 selecionado, `ProfileManager.apply()` atinge as DUAS keys — provado nos
   DOIS caminhos: ativação manual E ativação via autoswitch (mesma cadeia).
5. Regressão do coop: `_profile_player_leds` continua devolvendo o default do perfil após
   o refactor (sem isso a falha seria silenciosa), e o revert do co-op restaura o valor
   certo.
6. Gate completo verde sem regressão nos testes existentes de output/target/coop.

### PERFIL-02 — Schema: mapa `controllers` + serialização que omite + transporte no draft `[P0] [CLAUDE]`

**O que fazer**: camada 2 inteira — campo aditivo `controllers` (keys 12-hex,
`ControllerOverrides = {leds?, triggers?}`, sem label, sem mic_led), **serialização que
OMITE o campo quando None/vazio** em `save_profile`, aplicação por-controle na ativação
(registrando desconectados no mapa), e o **passthrough `source_controllers` no
DraftConfig** para o "Salvar Perfil" não apagar o mapa.

**Arquivos**: `src/hefesto_dualsense4unix/profiles/schema.py`,
`src/hefesto_dualsense4unix/profiles/loader.py` (serialização),
`src/hefesto_dualsense4unix/profiles/manager.py`,
`src/hefesto_dualsense4unix/daemon/ipc_draft_applier.py`,
`src/hefesto_dualsense4unix/app/draft_config.py` (passthrough),
`tests/unit/test_profile_schema.py`, `tests/unit/test_profile_manager.py`.

**Critério de aceite (verificável)** — reescrito conforme a refutação:
1. vitoria.json ganhando `controllers: {"143a9a13ebab": {leds: {lightbar: [0,255,0]}}}`
   valida, ativa aplicando verde SÓ nesse controle (broadcast segue a seção global) e
   sobrevive a save/load sem perda.
2. Perfil antigo (sem o campo): round-trip load→save **não introduz** a chave
   `controllers` no JSON (a omissão torna o aceite byte-idêntico atingível de novo —
   teste compara o dump, não só a validação).
3. Round-trip **via draft**: `DraftConfig.from_profile(perfil com mapa) → to_profile()`
   preserva o mapa intacto (o anti-BUG-FOOTER-SAVE-DROPS-SECTIONS-01 desta frente).
4. Key inválida (não-12-hex, ex.: `path:...` ou `000000000001`) é rejeitada pelo
   validador com mensagem clara.
5. Gate verde.

### PERFIL-03 — Autoload: origin nos 5 call sites + seed do marker + perfil padrão sem clobber `[P0] [AMBOS]`

**O que fazer**: camada 3 inteira — `origin` em `activate()` cobrindo os **5** call sites
da tabela (hotkey GRAVA; saída do Modo Nativo prefere `store.active_profile`); seed de
migração a partir de `active_profile.txt` no 1º boot pós-update; se o "perfil padrão"
explícito entrar, `save_last_profile` vira read-modify-write OU a chave vai para arquivo
próprio — nunca a chave nova no session.json com o save atual (refutado). Botão "Usar
este perfil ao iniciar" fica **opcional pós-validação** (o origin-fix sozinho atende o
pedido dela).

**Arquivos**: `src/hefesto_dualsense4unix/profiles/manager.py`,
`src/hefesto_dualsense4unix/profiles/autoswitch.py`,
`src/hefesto_dualsense4unix/daemon/connection.py`,
`src/hefesto_dualsense4unix/daemon/ipc_handlers.py`,
`src/hefesto_dualsense4unix/daemon/subsystems/hotkey.py`,
`src/hefesto_dualsense4unix/daemon/lifecycle.py`,
`src/hefesto_dualsense4unix/utils/session.py`,
`src/hefesto_dualsense4unix/app/actions/profiles_actions.py`,
`tests/unit/test_session_persist.py` (NÃO existe "test_session.py" — e
`test_activate_chama_save_last_profile` na :80 assevera gravação em TODA ativação: é o
**primeiro teste a atualizar**, previsto como quebra), `tests/unit/test_autoswitch.py`.

**Critério de aceite (verificável)** — reescrito conforme a refutação:
1. Teste: ativar 'vitoria' manualmente, simular 3 ativações do autoswitch (outros
   perfis) → session.json ainda aponta 'vitoria'; restart do daemon restaura 'vitoria'.
2. Teste: ciclo por hotkey (PS+dpad) GRAVA session.json (gesto manual); restore de boot e
   saída do Modo Nativo NÃO gravam; sair do nativo re-aplica `store.active_profile` (não
   a última manual).
3. Teste do seed: session.json='Navegação' + active_profile.txt='vitoria' → 1º restore
   pós-update ativa 'vitoria'.
4. Se houver default_profile: teste de que setá-lo e depois ativar outro perfil
   manualmente NÃO apaga a chave (read-modify-write) — e o boot restaura ele.
5. **Ao vivo (determinístico)**: reboot do daemon → log `last_profile_restored
   name=vitoria` + session.json apontando 'vitoria'. O que a aba Perfis mostra DEPOIS
   depende da janela focada (autoswitch, por contrato) — a verificação visual "vitoria
   ativo + controle roxo [129,61,156]" só vale com a pré-condição declarada: nenhum
   perfil criteria casando com a janela em foco (ex.: GUI do hefesto focada). O lock
   manual de 30s NÃO protege o boot.
6. Pré-requisito operacional registrado: session.json HOJE diz 'Navegação' — ela ativa
   'vitoria' manualmente UMA vez após o fix (ou o seed do item 3 cobre).

### PERFIL-04 — GUI: editar por-controle de verdade (promovido a P0 pela revisão) `[P0] [CLAUDE]`

**O que fazer**: camada 4 — mapa `controllers` no draft alimentado pelo seletor de alvo
(uniq já chega via state_full), badge "editando: Controle N (transporte)", "Salvar
Perfil" persiste o mapa no MESMO perfil, "Aplicar" envia os overrides, brilho lido do
perfil e escalado no mesmo caminho do global. Botões segmentados, nunca dropdown.

**Arquivos**: `src/hefesto_dualsense4unix/app/draft_config.py`,
`src/hefesto_dualsense4unix/app/actions/status_actions.py`,
`src/hefesto_dualsense4unix/app/actions/lightbar_actions.py`,
`src/hefesto_dualsense4unix/app/actions/triggers_actions.py`,
`src/hefesto_dualsense4unix/app/actions/footer_actions.py`,
`tests/unit/test_controller_target_ui.py`.

**Critério de aceite (verificável)**: o fluxo dela de ponta a ponta — selecionar
"1 - BT" → mudar lightbar para azul → "Salvar Perfil" (vitoria) → vitoria.json contém
`controllers[<mac do BT>].leds.lightbar` azul E a seção global intacta; reabrir a GUI
mostra o override (brilho incluso, lido do perfil); ativar o perfil pinta SÓ o BT de
azul. Teste de unidade do mapeamento seletor→draft.controllers e do round-trip do editor
(carregar perfil com mapa → salvar → nada se perde).

### PERFIL-05 — Validação ao vivo (2 controles, USB + BT) `[P1] [VITORIA_HUMANO]`

**O que fazer**: com o hardware disponível (1 DualSense BT + 1 DualSense cabo):
configurar cores/gatilhos DIFERENTES por controle dentro do perfil 'vitoria', salvar, e
exercitar:
- (a) desplugar/replugar o do cabo → cada um mantém SUA cor (aceite do 4P-01, sem
  contaminação);
- (b) restart do daemon → 'vitoria' restaurado sozinho (log `last_profile_restored`) com
  os dois controles certos — com a pré-condição de janela do PERFIL-03 declarada;
- (c) desligar/religar o BT → override re-aplicado quando ele volta (isto só funciona se
  a ativação REGISTROU o desconectado no mapa — é o teste de fogo da correção da
  revisão);
- (d) trocar o controle do cabo para BT → MESMA identidade (MAC provado estável) e MESMOS
  settings.

Registrar o resultado NESTE doc. **Invariante: sem esta validação, os P0 não fecham** —
teste verde sozinho não fecha item neste projeto.

**Arquivos**: `docs/process/sprints/2026-07-16-sprint-perfis-por-controle.md`.

**Critério de aceite (verificável)**: os 4 cenários passam com a Vitória olhando o
hardware (cores visíveis corretas em cada controle). Qualquer contaminação ou perda de
override reprova e volta para PERFIL-01/02.

### PERFIL-06 — Precedência + contrato de compat (coop, downgrade, fallback por path) `[P2] [CLAUDE]`

**O que fazer**:
1. Durante co-op ativo, o player-LED automático por jogador (coop, keyed por MAC) VENCE o
   override de `player_leds` do perfil; desligar o co-op restaura o do perfil — **e o
   REVERT resolve por-uniq** (hoje `_revert_single_player_led`/`_revert_player_leds`
   restauram o global; com overrides, restaurariam o broadcast por cima do override).
2. CHANGELOG descreve o downgrade **nos termos corretos**: com a omissão do campo
   (PERFIL-02), só perfis que USAM `controllers` são rejeitados por binário antigo
   (`extra="forbid"`, warning `profile_invalid`, somem da lista) — aceito porque
   daemon+GUI shippam juntos. Sem a omissão seria TODO perfil salvo — por isso ela é
   requisito, não estética.
3. Controle SEM serial (key de fallback por path) não entra no mapa — comporta-se como
   hoje (só global), com log `perfil_controllers_sem_mac` em vez de silêncio.
4. Registrar NESTE doc, explicitamente, o gate da regra de ouro (ver §Regra de ouro).

**Arquivos**: `src/hefesto_dualsense4unix/daemon/subsystems/coop.py`,
`tests/unit/test_coop_player_leds.py` (arquivo NOVO — não existe hoje), `CHANGELOG.md`,
`docs/process/sprints/2026-07-16-sprint-perfis-por-controle.md`.

**Critério de aceite (verificável)**: teste: perfil com override de player_leds + co-op
ativo → LED mostra o número do jogador; co-op off → volta o override POR-UNIQ do perfil
(não o global). Teste: key `path:...` é ignorada pelo mapa com o log. CHANGELOG menciona
a incompatibilidade de downgrade nos termos acima.

## Alternativas descartadas (e por quê)

- **Persistir o seletor de alvo (`output_target`) como mecanismo de perfil por
  controle** — é estado de UI transitório e posicional; já causa o bug de
  perfil-aplicado-só-no-alvo. A aplicação de perfil precisa de API por-uniq explícita.
- **Um arquivo de perfil POR CONTROLE** (vitoria-controle1.json) — contradiz o pedido
  dela ("salvo para aquele controle DENTRO do meu perfil"), duplica match/prioridade e o
  autoswitch teria de ativar N perfis coerentes ao mesmo tempo.
- **Keyed por índice/posição** ("Controle 1") — a posição muda com hotplug (4P-02:
  desplugar o P1 faz o 2 virar 1 e levar os ajustes do outro). O MAC é estável, provado
  ao vivo nos dois transportes.
- **Keyed por path evdev/hidraw** — `/dev/input/eventN` e `/dev/hidrawN` flutuam a cada
  replug (o projeto já tem watchdog para nó obsoleto).
- **Bump de versão do schema (version=2) com migração de arquivos** — campo aditivo
  opcional + serialização que o omite basta; perfis antigos validam sem tocar em disco.
- **Corrigir aqui a histerese do autoswitch** (wm_class 'unknown' desliga a emulação,
  medido 13:07:18) — é da frente de autoswitch (profiles/autoswitch.py:69-74). Esta
  frente só muda QUANDO o autoswitch grava session.json, não como ele escolhe janela.
- **`label` em ControllerOverrides** — cortado (refutado pela lente de escopo): ela não
  pediu; identidade visível é o 4P-03. Campo aditivo é barato de adicionar depois, caro
  de remover.

## Riscos

1. **Regressão mono-controle/broadcast** — mitigação: sem mapa, TODO o caminho existente
   vira "default sem override" (comportamento atual); seams prontos na suíte
   (`_enumerate_device_keys` stubável, `_ds` setter de compat).
2. **Downgrade** — ver PERFIL-06 item 2 (termos corrigidos pela revisão).
3. **Disputa coop-LED vs override** — precedência explícita + revert por-uniq
   (PERFIL-06 item 1).
4. **Quebra prevista de teste legado** — `test_activate_chama_save_last_profile`
   (tests/unit/test_session_persist.py:80) assevera gravação em toda ativação; atualizar
   junto (PERFIL-03) e validar que o restore não regride quando NUNCA houve escolha
   manual (cai no comportamento atual).
5. **Modo Nativo** — os reasserts por-uniq respeitam `_output_mute` como hoje (gates
   existentes, não remover); e a saída do nativo passa a re-aplicar
   `store.active_profile` (decisão do PERFIL-03, tabela dos 5 call sites).
6. **Corrida do rumble por jogador** — o flip temporário do `_output_target_key`
   (gamepad.py:181-199) + setters em executor multi-thread: resolvido por construção no
   PERFIL-01 (alvo na borda, API por-uniq) ou exclusão mútua explícita.
7. **Falha silenciosa do coop no refactor** — `getattr(ctrl, "_desired", None)` devolve
   None para sempre após rename seco, sem nenhum teste quebrando (por isso coop.py está
   no PERFIL-01, não só no PERFIL-06/P2 — a quebra chegaria antes do conserto).

## Armadilhas conhecidas que esta frente atravessa

- **MAC próprio do vpad** (`02:fe:00:00:00:0N` no report 0x09 LE): o vpad uhid NUNCA
  entra no mapa — `_is_virtual_hidraw` já o exclui da enumeração (conferido pelos
  revisores). Não regredir esse filtro.
- **valid_flag `0x03` no rumble e payload de 63 B** (`_INPUT_PAYLOAD_SIZE=63`):
  invariantes do vpad UHID que esta frente NÃO toca — nenhum item pode mexer no caminho
  do report.
- **udev < 73 para uaccess**: esta frente não adiciona NENHUMA regra udev; a rota sysfs
  de LED por-controle usa a `77-dualsense-leds.rules` que o install JÁ põe por default.
- **Sudo-zero na GUI** (decisão do bfd51db): preservado por construção — a frente é
  código + JSON em `~/.config`, zero sudo em runtime.
- **Dropdowns quebram no COSMIC** (cosmic-epoch#2497 + NVIDIA): seletor por-controle e
  qualquer UI nova = botões segmentados, nunca popup.
- **GIL/throttling**: os reasserts por-uniq no hotplug não podem adicionar varredura
  inline nem trabalho extra no report_thread; o executor de setters é `max_workers=2` —
  a API por-uniq não muda esse contrato.
- **Mic-LED**: persiste no `_desired` em memória e vaza no hotplug (o PERFIL-01 cura de
  carona), mas NÃO persiste no perfil por decisão deliberada
  (AUDIT-FINDING-PROFILE-MIC-LED-RESET-01) — fica FORA do ControllerOverrides.

## Regra de ouro ("tudo no install funcionando SEM FLAGS") — declaração explícita

**Esta frente NÃO exige nenhuma mudança em install.sh, uninstall.sh ou doctor.sh** —
verificado de forma independente pelas três revisões adversariais. É código puro +
arquivos JSON de configuração de usuária em `~/.config/hefesto-dualsense4unix/`:

- Nenhuma regra udev nova, nenhum drop-in, nenhum modprobe.d, nenhuma permissão, nenhum
  serviço (a única dependência de sistema, a `77-dualsense-leds.rules` para a rota sysfs
  dos LEDs, JÁ é instalada por default e o co-op já a usa).
- Nenhum "cole isto", "rode aquilo", "exporte esta variável" — a migração é campo
  opcional + serialização que o omite + seed automático do `active_profile.txt`.
- Simetria install/uninstall intocada. Sudo-zero em runtime intocado.
- Não há nada novo para o doctor.sh verificar.

## Honestidade com a usuária (para a validação ao vivo não virar bug report)

Os overrides por-controle valem **enquanto o perfil que os contém está ativo**. O
autoswitch continua trocando perfil por janela (por desenho): focar o browser ativa
"Navegação" (prioridade 50 > 5) e o broadcast repinta TODOS os controles; voltar ao
desktop/GUI reativa "vitoria" (MatchAny 5 > fallback 0) e os overrides voltam. Se ela
quiser "vitoria SEMPRE, ignorando janela", isso é uma decisão de produto separada
(perfil padrão com precedência sobre o autoswitch, ou repensar "Navegação") — o botão
opcional do PERFIL-03 é o gancho para essa conversa após a validação. Sem este parágrafo
na conversa com ela, "configurei e mudou sozinho" viraria bug report.

## Ordem de execução

PERFIL-01 (fundação — nada aterrissa sem ele) → PERFIL-02 (schema + serialização +
passthrough do draft, atômico com o 01) → PERFIL-04 (GUI — fecha a unidade de entrega
visível) → PERFIL-03 (autoload; independente das camadas 1-2, pode andar em paralelo) →
PERFIL-05 (validação humana — portão de fechamento dos P0) → PERFIL-06 (precedência +
compat).
