# MODO-01 — o modo jogo liga sozinho

- **Status:** ENTREGUE em 25/07/2026 pelo commit `54f1f3b` — confirmado ao vivo
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026

## O relato

> "modo jogo por exemplo não liga automaticamente."

## Primeiro achado: "modo jogo" são seis coisas

A investigação começou tentando descobrir *qual* modo não liga, e a resposta é
que o projeto tem seis conceitos distintos com esse nome ou próximos dele:

| # | conceito | onde vive | estado medido |
|---|---|---|---|
| 1 | `mode` do perfil (desktop/gamepad/native) | `profiles/schema.py:349` | nunca aplicado |
| 2 | `gamepad_emulation` — o gamepad virtual | flag em disco | **ligado** |
| 3 | `_native_mode` — "Jogar direto (Sony)" | `daemon/state_store.py:204` | desligado |
| 4 | `emulation_suppressed` — o que a aba Emulação **rotula "Modo jogo"** | `daemon/subsystems/hotkey.py:74` | **ligado** |
| 5 | `game_signal` / autoridade de exibição | `daemon/subsystems/game_signal.py:65` | caiu para `daemon` com o jogo aberto |
| 6 | o comutador da aba Início | `app/actions/mode_transition.py:147` | leitura derivada de (2)+(3) |

Só o **(1)** tem automação. O (5) não liga modo nenhum — só decide quem manda na
luz. O (6) não é estado, é espelho.

**Isso é parte do defeito, não contexto dele.** Seis nomes para coisas
diferentes garantem que a usuária e o código estejam falando de coisas
diferentes sempre que o assunto aparece.

## A cadeia medida, com o jogo aberto

Journal do daemon com Mullet Mad Jack em execução:

```
profile_select_catch_all_sem_autoridade_em_jogo candidatos=['fallback','meu_perfil','vitoria'] wm_class=steam_app_2111190
x11_focus_gate_no_x_focus focus=0
autoswitch_window_info_unavailable current= wm_class=unknown
autoswitch_congelado_pelo_cadeado candidate=Navegação wm_class=steam
```

**Elo 0 — o disco.** Dos 13 perfis, **nenhum** casa `steam_app_2111190`, e
**apenas 2** têm seção `mode` (`coop_local` e `sackboy_nativo`). Os outros 11 —
incluindo o `fps`, que estava persistido como ativo — têm `mode: null`.

**Elo 1 — o veto.** `ProfileManager.select_for_window` (`profiles/manager.py:557`):
os três candidatos são catch-all e a janela é um jogo. A regra R-21
(`manager.py:561`) recusa dar autoridade a catch-all sobre janela de jogo e
devolve `None`.

**Elo 2 — nada a ativar.** Sem candidato, `activate` nunca roda; o aplicador de
modo nunca é chamado. Confirmado no journal: **zero** eventos `profile_mode_*`
hoje. O último `profile_autoswitch` foi em **24/07 às 20:37**.

**Elo 3 — o cadeado, que aqui é inocente.** `autoswitch_locked.flag` está ligado
desde 24/07 20:42. Mas mesmo destravado o resultado seria idêntico: sem
candidato, não há troca. O cadeado é redundante **neste** caso.

**Elo 4 — a sessão roda sem perfil.** `last_profile_restore_pulado_perfil_de_janela`
(`daemon/connection.py:143`): o restore de inicialização pula perfis escopados a
janela. Resultado vivo: `active_profile = null`. Nem a inicialização nem a troca
automática põem perfil algum de pé.

## O buraco de projeto — e é ele que ela sente

A regra R-21 trocou *"o catch-all entra num jogo"* por *"**ninguém** entra num
jogo"*, **e não pôs nada no lugar**.

O daemon **sabe** que há um jogo — registrou `game_signal_transition de=daemon
para=game` às 15:43:39. E não faz nada com essa informação em termos de modo. Todo
o automatismo depende de ela ter criado, à mão, um perfil com seção `mode` para
aquele jogo específico.

**E criar o perfil não resolve.** `app/actions/profiles_actions.py:630` faz todo
perfil novo nascer com modo `"none"` — *"Não mexer no modo"*. O fluxo "Jogo da
Steam" monta o critério de janela corretamente e deixa o modo **vazio**. Ela cria
o perfil do jogo, ele entra, e não liga nada. **O caminho que a interface oferece
como solução não soluciona.**

## Os cinco defeitos

### B1 — perfil de jogo nasce sem modo *(o maior)*
`profiles_actions.py:630`. Quando a escolha é "jogo" ou "jogo da Steam", o editor
deve pré-selecionar modo `gamepad` com a máscara corrente.

### B2 — o cadeado congela mais do que promete
`perfil_e_regra_de_jogo` (`profiles/schema.py:602`) exige critério por
`window_class` **e** nome começando com `steam_app_`. Consequências não
pretendidas: `coop_local.json` — que **tem** `mode: gamepad` — casa por título de
janela (Sackboy, Overcooked, It Takes Two, Cuphead) e é congelado; jogos fora da
Steam com perfil próprio idem.

O cadeado é sobre **perfil** — o próprio rótulo diz *"Não trocar de perfil
sozinho ao abrir um jogo"*. Ele não deveria bloquear a entrada em **modo**, que é
outra coisa. Conserto: ceder também quando o perfil não é catch-all e declara
`mode.kind` em `{gamepad, native}` — *"o perfil declara que é de jogo"*.

### B3 — modo jogo padrão quando ninguém opina *(a cura do buraco)*
Quando a autoridade é `game` **e** o veto R-21 disparou — isto é, *é um jogo e
nenhum perfil específico opina* — aplicar um modo jogo padrão **sem trocar de
perfil**:

```python
apply_profile_mode(ProfileModeConfig(kind="gamepad",
                   gamepad_flavor=config.gamepad_flavor), origin="game_signal")
```

O cadeado **não** deve bloquear isso: ele congela a decisão de perfil, não a de
modo. Requer que `select_for_window` devolva o **motivo** do veto — hoje `None` é
ambíguo entre "nada casou" e "vetei um catch-all num jogo".

### B4 — o gate de foco cega a detecção
`integrations/window_backends/xlib.py:248` devolve foco nulo quando o compositor
entrega o foco a uma superfície nativa. Medidos **47 episódios**. Não é o
bloqueador primário — o veto mata a seleção mesmo com a janela lida
corretamente — mas é o que faz a autoridade **cair de `game` para `daemon` com o
jogo ainda aberto**, 30 segundos depois.

### B5 — enxurrada de log
`profile_select_catch_all_sem_autoridade_em_jogo` a 0,5 Hz. A deduplicação usa um
campo de instância (`manager.py:102`), mas `lifecycle.py:2512` cria um
`ProfileManager` **novo a cada tique** — a dedup nunca vale. Medido: 12 linhas
idênticas, exatamente 2,00 s de intervalo.

## Também é configuração, e isso precisa ser dito

Três coisas do estado dela não são defeito do projeto:

- não existe perfil para `steam_app_2111190`;
- 11 dos 13 perfis têm `mode: null`;
- o cadeado está ligado desde ontem, a pedido dela.

O conserto B3 faz o modo jogo funcionar **apesar** disso — que é o comportamento
correto para quem não quer administrar perfil por jogo.

## Como validar

1. Com o cadeado **ligado** e nenhum perfil para o jogo: abrir o jogo → o modo
   jogo liga, o perfil **não** troca. Log: `profile_mode_aplicado
   origin=game_signal`.
2. Com `coop_local` casando por título: abrir Sackboy → o modo liga (hoje é
   congelado pelo cadeado).
3. Criar perfil pelo fluxo "Jogo da Steam" → nasce com modo `gamepad`
   pré-selecionado.
4. Fechar o jogo → volta ao modo anterior.
5. `journalctl --user -u hefesto-dualsense4unix | grep -c catch_all_sem_autoridade`
   → poucas linhas, não uma a cada dois segundos.

## Débito registrado, não corrigido aqui

**Os seis "modo jogo" precisam virar menos.** Não cabe nesta sprint — mexer nos
seis conceitos ao mesmo tempo é como se cria um sétimo. Mas enquanto forem seis,
toda conversa sobre "o modo não liga" começa por descobrir de qual se fala. O
mínimo desta sprint é **não criar nomes novos**.
