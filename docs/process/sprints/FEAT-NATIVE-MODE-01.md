# FEAT-NATIVE-MODE-01 — Modo Nativo: "release total" do controle (Sackboy & cia)

**Tipo:** feat (médio — daemon + IPC + CLI + preset + gates de subsistemas).
**Wave:** V3.12.
**Status:** EM IMPLEMENTAÇÃO.

---

## Contexto

A Vitória quer um **botão de parar que de fato funcione**: jogar Sackboy: Uma
Grande Aventura (e outros jogos de gamepad) com os **gatilhos adaptativos nativos
da Sony** dirigidos pelo próprio jogo, sem o hefesto no meio. Decisão dela
(2026-07-07): **release total global + perfil por-jogo**.

O que o hefesto escreve no controle que pode brigar com o jogo:
- **Gatilhos**: escritos 1x na ativação do perfil (latch no HW). Um perfil
  Off/Off já não impõe resistência; o jogo sobrescreve.
- **Rumble**: `reassert_rumble` re-aplica a cada 200ms SÓ quando
  `config.rumble_active` não é None. `passthrough` (rumble_active=None) → o
  hefesto não toca no rumble (o jogo manda). Sem briga.
- **Emulação (mouse/gamepad virtual)**: segura grab de evdev (EVIOCGRAB) e cria
  device uinput — isso SIM bloquearia/duplicaria o controle no jogo.
- **Autoswitch/hotkey**: re-aplicam perfis (que re-escrevem gatilhos) ao focar
  janela / PS+dpad.

Ou seja: o "hands off" é **gatilhos Off + rumble passthrough + emulação
desligada + nada re-aplicando perfil**.

## Decisão

1. **`Daemon.set_native_mode(enabled: bool)`** (lifecycle.py):
   - **on**: salva o perfil corrente; seta gatilhos Off/Off no controle; põe
     rumble em passthrough (`rumble_active=None`); desliga emulação de
     mouse E gamepad (libera grab/uinput) via os setters `origin="manual"`;
     marca `store.native_mode_active=True` (autoswitch/hotkey consultam e NÃO
     re-aplicam perfil enquanto ativo); `pause()` (para o dispatch de
     input emulado/hotkey de ação); persiste o flag `native_mode.flag`.
   - **off**: limpa `native_mode_active`; `resume()`; restaura o último perfil
     (re-aplica gatilhos/rumble/emulação); remove o flag.
   - Idempotente; notifica (opt-in) e loga `native_mode_changed`.
2. **Gate no autoswitch e no hotkey de ciclo**: `store.native_mode_active` (novo
   flag no StateStore, espelhando `manual_trigger_active`) faz o autoswitch
   pular a ativação e o hotkey de ciclo não trocar de perfil (mas o hotkey de
   SAIR do modo nativo, se houver, ainda funciona). O poll loop já respeita
   `_paused`.
3. **Rota IPC** `native.mode.set {enabled?: bool}` (toggle se ausente) →
   `set_native_mode`; incluída no `daemon.state_full` (`native_mode: bool`).
4. **CLI** `dsx native on|off|status` (via IPC, tudo-via-interface).
5. **Restore no boot**: se `native_mode.flag` existe, sobe em modo nativo
   (não re-aplica perfil por cima).
6. **Perfil por-jogo (preset)**: `assets/profiles_default/nativo.json` —
   gatilhos Off/Off, `rumble.passthrough: true`, SEM seção mouse, sem
   supressão, `priority: 55`. Serve de base; a Vitória aponta o `window_class`
   do jogo (Sackboy/PRAGMATA/etc.) pela GUI. (O autoswitch já resolve o resto.)
   NB: sem o wm_class real do Sackboy, o preset nasce com match vazio (só
   manual) — documentar no usage; capturar o wm_class ao vivo depois.

## Diferença do `pause` e da supressão

- `pause` (FEAT-DAEMON-PAUSE-RESUME): para o DISPATCH de input emulado, mas
  mantém gatilhos/rumble/emulação como estavam. NÃO solta o controle.
- `set_emulation_suppressed` (modo-jogo): para o dispatch de mouse/teclado
  emulado, devices seguem vivos (grab mantido). NÃO solta o controle.
- **Modo Nativo**: SOLTA o controle de verdade (gatilhos neutros, rumble ao
  jogo, emulação/grab off, nada re-aplica). É o "hands off" completo.

## Critérios de aceite

- [ ] `native.mode.set {enabled:true}`: gatilhos viram Off/Off, rumble_active
      None, mouse/gamepad emulação desligados, `native_mode_active` True,
      daemon pausado, flag persistido. Idempotente.
- [ ] `native.mode.set {enabled:false}`: restaura o último perfil (gatilhos/
      rumble/emulação re-aplicados), `native_mode_active` False, resume, flag
      removido.
- [ ] Autoswitch com `native_mode_active`: NÃO ativa perfil ao focar janela.
- [ ] Hotkey de ciclo com `native_mode_active`: NÃO troca de perfil.
- [ ] Restore no boot com `native_mode.flag`: sobe em modo nativo.
- [ ] `dsx native status` reflete o estado; `daemon.state_full` inclui
      `native_mode`.
- [ ] Suite verde; ruff/mypy limpos; smokes USB+BT.
- [ ] (Manual, Vitória) Sackboy: `dsx native on` → gatilhos adaptativos do jogo
      funcionam sem briga; rumble do jogo ok; `dsx native off` → hefesto volta.

## Revisão pós-auditoria (2026-07-07)

A auditoria adversarial achou 5 pontos; o design foi ajustado:
- **NÃO usa mais `pause()`**: o poll loop gateia o dispatch pelo próprio
  `_native_mode` (`input_ready = ... and not self._native_mode`). Isso resolve de
  uma vez: (a) `daemon.resume` durante o Modo Nativo NÃO "des-solta" o controle
  (estado contraditório native+resume); (b) um pause manual anterior não é pisado
  nem some num restart (o bit não vivia mais só em memória).
- **Stash da emulação**: o `native_mode.flag` virou JSON com o estado de
  emulação (mouse/gamepad) capturado ANTES do release. Ao desligar, o gamepad/
  mouse pré-nativo é RESTAURADO (gamepad tem precedência) — antes o release
  apagava o `gamepad_emulation.flag` e o off/boot não o trazia de volta.
- Testes adicionados: boot com flag (não restaura emulação), resume-durante-
  native, restore do gamepad do stash, round-trip do flag JSON + legado.

## Fora de escopo (V3.12+)

- Botão na GUI / no applet / hotkey do controle p/ o modo nativo (entra depois
  do core validado; por ora CLI/IPC).
- Preset com wm_class do Sackboy pré-configurado (precisa capturar ao vivo).
