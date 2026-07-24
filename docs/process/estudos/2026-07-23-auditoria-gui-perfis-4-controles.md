# 2026-07-23 — Auditoria: abas da GUI × perfis × config por-controle (4 controles)

Auditoria por agentes pedida pela mantenedora com os 4 controles ligados:
*"faça uma auditoria completa na interação entre as abas, veja a questão dos
perfis pré-setados, e nas configs que o user faz e que parecem não impactar
controle a controle"*.

Método: 14 dimensões lidas em paralelo (autoswitch, casamento de perfil,
config por-controle, estado entre abas, modo/flavor, co-op/slots/LEDs, seeding
de presets, BT, IPC, lançamento de jogo, testes esquecidos, lightbar,
rumble/gatilhos, broker) → **100 achados brutos** → verificação **adversarial**
com 3 lentes independentes por achado (refutação / reprodução / impacto),
confirmando só o que teve maioria.

> **Custo e interrupção:** a 1ª rodada consumiu 6,3 M tokens e bateu no limite
> de sessão com 265 dos 316 agentes cancelados. Os 51 que rodaram entregaram os
> **10 confirmados** da §2. Os `0/0` na lista de descartados **não foram
> refutados — foram cancelados**; a 2ª rodada (§4) os retoma.

## 1. As queixas, na palavra dela

1. *"quando eu escolho o sackboy e o madjack, a config dos controles que eu
   deixo ou o modo de jogar **nunca** é respeitado quando abro o jogo"*
2. *"as configs que o user faz parecem não impactar controle a controle"*
3. Player LEDs duplicados: dois "player 2" e dois "player 1" em vez de 1-2-3-4
4. 8BitDo só conecta manualmente
5. *"testes que tenham marcado os controles e tenhamos esquecido de atirar"* —
   estado armado que nunca é liberado

## 2. Achados CONFIRMADOS (1ª rodada)

### 2.1  CRÍTICO — `draft-nunca-recarrega-ao-trocar-perfil` (3/3)

`app/app.py:654` — **o pai da queixa (1).**

`_bootstrap_draft_async()` é o **único** ponto que popula `self.draft` a partir
do perfil ativo, e só é chamado em `show()` e no ramo oculto de `run()`. Não
existe listener nem tick que recarregue o draft quando o perfil ativo muda — e
ele muda por **quatro** caminhos: botão "Ativar" da aba Perfis, menu do tray,
hotkey PS+D-pad e **o autoswitch quando ela abre o jogo**.

Depois disso: as abas Lightbar/Gatilhos/Rumble/Teclado mostram o perfil
**antigo**; o "Aplicar" do rodapé empurra as seções globais do perfil antigo
para o hardware **por cima do perfil do jogo**; e o "Salvar Perfil" pré-preenche
o nome obsoleto.

> Cenário: GUI aberta com FPS ativo → abre o Sackboy (autoswitch ativa
> `sackboy_nativo`) → alt-tab para a GUI, que continua mostrando FPS → ela
> ajusta e aplica → **o FPS é empurrado por cima do perfil do jogo**.

**Correção** (com 4 refinamentos que a proposta original não cobria): um dono só,
no tick lento que já existe. Não comparar contra `_active_profile_name` (ele fica
stale quando o perfil não existe em disco → IPC em loop); usar campo separado
`_draft_reload_for`, marcado **antes** do disparo; guard de reentrância; e não
sobrescrever edição pendente.

### 2.2  CRÍTICO — `perfis-salvar-reconstroi-do-disco-e-descarta-o-draft` (3/3)

`app/actions/profiles_actions.py:921`

`_build_profile_from_editor()` monta o perfil a partir de `_profiles_cache`
(= **disco**). O `self.draft` **não é consultado em nenhuma linha do módulo** —
e as abas Lightbar/Gatilhos/Rumble/Mouse/Teclado gravam **exclusivamente** no
draft. E é pior que perder o arquivo: `on_profile_save` chama
`profile_switch()` quando o perfil salvo é o ativo, então o daemon relê o JSON
velho e **reverte no hardware**.

> Cenário: escolhe vermelho na Lightbar (funciona) → põe L2 em "Weapon"
> (sente) → vai em Perfis marcar o Modo e salva → **a cor volta e o gatilho
> morre na hora**, sem mensagem. Ela conclui "as configs que eu faço não
> impactam".

### 2.3  CRÍTICO — `rodape-salvar-reescreve-mode-match-prioridade-do-bootstrap` (3/3)

`app/draft_config.py:396`

`DraftConfig.to_profile()` reemite `match`, `mode`, `suppress_desktop_emulation`,
`priority` e `controllers` a partir dos campos `source_*` — preenchidos **uma
vez, no bootstrap**, e que **nenhum handler da aba Perfis atualiza**. A aba
Perfis e o rodapé são **dois escritores do mesmo arquivo com snapshots
diferentes**, e o último a escrever ganha sobre o dict inteiro.

> Cenário: aba Perfis põe Modo = "Jogar pelo Hefesto" e salva (o JSON ganha
> `mode`) → aba Lightbar muda a cor → "Salvar Perfil" no rodapé → `to_profile()`
> emite `mode=self.source_mode`, que ainda é o valor do **boot** (`None`) → **a
> seção `mode` é apagada do JSON**.

### 2.4  CRÍTICO — `autoswitch-fallback-vira-perfil-de-jogo` (3/3)

`profiles/autoswitch.py:258` — **explica o Mullet Mad Jack.**

A exceção F2 foi documentada como "a janela em foco casando `steam_app_*` com
perfil **próprio** vence o override", mas o código **não verifica que o perfil
candidato casou por causa do `steam_app_*`**. O teste é só: (a) a wm_class é de
um jogo Steam e (b) o nome do candidato difere do ativo.

Como existem **três** perfis MatchAny no disco dela (`vitoria` prio 5,
`fallback` prio 0, `meu_perfil` prio 0) e **não existe perfil para o MMJ**
(appid 2111190), o vencedor para a janela do MMJ é o `vitoria` — perfil genérico
de desktop. Ele é tratado como "perfil do jogo": `clear_manual_trigger_active()`
apaga as **três** categorias de override manual e o genérico é aplicado por cima.

> A trava manual existe (a cura da Onda U está lá, `ipc_handlers.py:403/466/496`).
> Mas **o único momento em que ela mais importa — abrir o jogo — é exatamente
> quando ela é descartada.** Log emitido: `autoswitch_manual_override_cedeu_ao_jogo`.

**Correção de raiz (mínima):** *um perfil MatchAny nunca é "o perfil do jogo"*.
O objeto `Profile` já está disponível no `_tick`; basta propagá-lo em vez de só
o nome. Menos invasivo que devolver `matched_by` do `select_for_window`.

### 2.5 🟠 ALTA — `perfil-reescreve-flag-persistida-do-gamepad` (3/3)

`daemon/subsystems/gamepad.py:901`

`start/stop_gamepad_emulation` gravam em disco **sem olhar o `origin`**. Isso
contradiz duas decisões explícitas do próprio módulo (HARM-06 em `gamepad.py:832`
e FEAT-COOP-DEFAULT-ON-01 em `lifecycle.py:1024`: *"só gesto MANUAL persiste"*).

> Ela escolhe Xbox (flag=`xbox`) → abre Sackboy → o perfil força `dualsense` e
> **reescreve a flag** → fecha o jogo e a escolha dela sumiu. Pior: alt-tab para
> o navegador → Navegação (sem `mode`) → `stop_gamepad_emulation` com
> `persist=True` → **a flag é apagada** → no próximo boot não há vpad nenhum.

### 2.6 🟠 ALTA — `gesto-manual-nao-limpa-mode-from-profile` (2/2)

`daemon/lifecycle.py:961`

A semântica declarada em `lifecycle.py:258` é *"gesto manual da usuária nunca é
derrubado pelo autoswitch"*. Dois eixos cumprem
(`_suppress_from_profile`, `_rumble_policy_from_profile`) e `set_native_mode`
também. Mas `set_gamepad_emulation` e `set_coop_enabled` com `origin='manual'`
só carimbam `_emu_manual_ts` (proteção de **30 s**) e **não limpam**
`_mode_from_profile`. Passada a janela, o primeiro perfil sem `mode` — *quase
todos os dela* — desliga o vpad que ela ligou na mão.

**Correção:** limpar `self._mode_from_profile = None` junto do carimbo (paridade
com os outros dois eixos). Complemento descoberto na verificação: em
`set_native_mode` a limpeza está **depois** do early-return de idempotência.

### 2.7 🟠 ALTA — `edit-target-cai-para-global-com-menos-de-2-dualsense` (3/3)

`app/actions/status_actions.py:632` — **explica a queixa (2) hoje.**

`_refresh_controller_target_combo` roda no tick de 2 Hz **sem guarda de aba
visível** e decide `editavel = len(conectados) >= 2`, contando **só DualSense**
(Pro Nintendo e 8BitDo entram como "externos", que por construção não são alvo
de edição). Com `editavel` False ele força `_sync_edit_target(None)` e repopula
as abas com a seção **global**.

> Com o roxo zumbi, há **um** DualSense com nó no kernel → `_edit_target_uniq`
> é permanentemente `None` → **a edição "controle a controle" está literalmente
> desligada, sem nenhuma mensagem dizendo isso.**

E o tick faz isso **no meio da edição**: o badge some e o "Aplicar no controle"
seguinte vai pelo ramo global, aplicando em todos e desligando
`auto_player_colors`.

### 2.8 🟠 ALTA — `ativacao-de-perfil-apaga-overrides-por-controle` (2/3)

`profiles/manager.py:218`

`ProfileManager.apply()` faz `apply_output_defaults` (broadcast real, ignora o
seletor de alvo) e depois `reset_output_overrides()`, que **substitui o
`_desired_by_uniq` inteiro** — exatamente onde vivem as configurações
por-controle da GUI. Como só `navegacao.json` tem seção `controllers`, **qualquer
outro perfil ativado apaga o ajuste por-controle** e reescreve o mesmo padrão de
player-LED em todos. Isso alimenta as queixas (2) **e (3)**.

>  A lente de impacto **rejeitou a correção original** ("dois mapas no
> backend" reintroduz o bug de override ressuscitando no hotplug). O ponto certo
> é a **borda da cessão** no `autoswitch.py:258` — sinalizar à GUI em vez de
> silenciar.

### 2.9 🟠 ALTA — `restaurar-default-nao-atualiza-nome-do-perfil-ativo` (3/3)

`app/actions/footer_actions.py:426`

`_on_restored` troca `self.draft` pelo de `meu_perfil` mas **nunca atualiza
`_active_profile_name`** — que é justamente o que pré-preenche o diálogo de
salvar. Os dois botões vivem **lado a lado no mesmo rodapé**.

> "Restaurar Default" com FPS ativo → todas as abas mostram `meu_perfil` → ela
> clica "Salvar Perfil" achando que salva o que vê → o diálogo vem com **"FPS"**
> → confirma → **o conteúdo inteiro de `meu_perfil` é gravado por cima do FPS**.

### 2.10 🟡 MÉDIA — `reload-profiles-store-clobbera-o-editor-da-aba-perfis` (3/3)

`app/actions/footer_actions.py:255`

Salvar/importar pelo rodapé chama `_reload_profiles_store()`, que faz
`store.clear()` + repopula + `select_iter()` → emite `changed` → `_populate_editor`
sobrescreve o editor. Sem `select_name`, o alvo vira **a primeira linha**.

> Ela monta o perfil do MMJ na aba Perfis (nome, `steam_app_2111190`, Modo), não
> salva ainda, vai ajustar a cor e clica "Salvar Perfil" no rodapé → **o perfil
> que estava montando some**, sem diálogo, sem toast.

## 3. Padrão de fundo

Os 4 críticos são **a mesma doença arquitetural**: existem **três escritores do
mesmo perfil** — `self.draft` (abas de hardware), o editor da aba Perfis
(disco), e os campos `source_*` do rodapé (snapshot do boot) — **sem um dono
único e sem sincronização entre eles**. O último a escrever ganha sobre o dict
inteiro, e o autoswitch é um quarto escritor que entra por fora.

Isso explica por que a queixa dela é *"**nunca** é respeitado"* e não *"às vezes
falha"*: em qualquer ordem de cliques, algum dos três descarta o trabalho dos
outros.

## 4. 2ª rodada — 85 achados pendentes

Os `0/0` da 1ª rodada foram **cancelados pelo limite de sessão, não refutados**.
Distribuição: **19 críticos, 43 altos, 23 médios**. Retomados com 1 cético por
achado, com o contexto dos 10 já confirmados para marcarem `duplicata_de` em vez
de recontar a mesma raiz.

Achados pendentes que merecem atenção pelo título (ainda **não** verificados):
`coop-local-criteria-vazio-nunca-casa`, `perfil-any-vence-perfil-do-jogo`,
`coop-e-slot-brigam-pelo-mesmo-led`, `externos-consomem-numero-de-jogador`,
`aba-gatilhos-arma-trava-sem-botao-de-soltar` (candidato direto à queixa 5),
`parar-vibracao-mata-rumble-dos-4-para-sempre`,
`troca-de-mascara-no-meio-do-jogo-com-env-congelada`.

Resultado consolidado e plano por causa-raiz: ver a sprint
`2026-07-23-sprint-gui-perfis-por-controle.md`.

## 5. Falsos-positivos notáveis (refutados com prova)

- `sackboy-preso-em-mascara-dualsense` (1/2) — a narrativa era "a migração
  one-shot dualsense→xbox gravou o marker sem migrar". Refutado por **cinco**
  guardas, incluindo forense de mtime: o `coop_local.json` está em `xbox` com
  mtime **anterior** ao marker e preservando a formatação compacta do asset —
  prova de que a migração encontrou os presets já corrigidos. E o `dualsense` do
  `sackboy_nativo.json` é de **32 h depois**, edição manual. A correção proposta
  seria **regressão**: tornaria a migração re-executável e ela reverteria a
  escolha manual a cada boot, *agravando* a queixa (1).
