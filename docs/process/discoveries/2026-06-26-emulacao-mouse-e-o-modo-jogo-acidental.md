# 2026-06-26 — Emulação de mouse "não funcionava" = modo-jogo alternado por acidente

> Sessão com a Vitória, logo após estabilizar o storm (áudio off). Sintoma relatado:
> "isso só altera o botão R, a função de mouse via analógicos não funciona, e a flag
> ali não ativa." Investigação ao vivo via logs do daemon + leitura do código.

## TL;DR

A emulação de mouse (analógico → cursor) **estava ligada o tempo todo** — o que não
funcionava era o **despacho**, porque o **modo-jogo (supressão) estava ATIVO**. E o modo-jogo
estava sendo alternado **por acidente**: o gesto de "segurar o PS ~1s" (que a Vitória usa
tentando abrir a Steam) caía exatamente no limiar de **long-press de 1000ms**, que alterna a
supressão. O log provou: vários `ps_long_press_fired held_ms≈1003` seguidos, alternando
`emulation_suppressed` True/False, terminando em **True** (suprimido) — por isso o cursor não
andava.

Pior: o limiar de 1000ms **nem era configurável de fato** — o `HotkeyManager` era instanciado
**sem** config (`subsystems/hotkey.py`), então `ps_long_press_ms` ficava preso no default,
ignorando qualquer ajuste.

## Por que cada sintoma acontecia

- **"a função de mouse via analógicos não funciona"** — `lifecycle.py:685-689`: o poll loop só
  despacha mouse/teclado `if not self._emulation_suppressed`. Com supressão ON, o analógico→cursor
  e todos os botões mapeados (X→clique, etc.) são **pulados inteiros**. Os devices uinput continuam
  vivos; só o despacho para.
- **"isso só altera o botão R"** — os **gatilhos adaptativos** (R2/L2) são independentes da emulação
  e **continuam funcionando** mesmo com a supressão ON. Então a única coisa que "respondia" no
  controle era o gatilho (sentido no R2) — daí a impressão de "só o botão R".
- **"a flag ali não ativa"** — o toggle "Emular mouse+teclado" da GUI controla
  `mouse_emulation_enabled` (estava ON, `uinput disponível` verde). Mas o **estado efetivo** estava
  bloqueado pela supressão, e **a GUI não tem indicador de modo-jogo** — então o toggle parecia não
  ter efeito nenhum.

## Evidência (journal do daemon)

```
01:57:01  ps_long_press_fired held_ms=1003.6  → emulation_suppressed=True
01:57:42  ps_solo_released   held_ms=641.9               (toque curto = abriu Steam)
01:57:47  ps_long_press_fired held_ms=1002.7  → emulation_suppressed=False
01:57:50  ps_long_press_fired held_ms=1000.3  → emulation_suppressed=True
01:57:55  ps_long_press_fired held_ms=1002.6  → emulation_suppressed=False
02:00:08  ps_long_press_fired held_ms=1002.3  → emulation_suppressed=True   ← estado final
```

O gesto natural dela de "abrir Steam" mira ~1s e colide com o limiar de 1000ms do modo-jogo.
A janela toque-curto (Steam) vs. hold (modo-jogo) era estreita demais.

## Correção (decidida com a Vitória: combo deliberado em vez de long-press)

Ideia dela: **PS + Options (Start)** alterna o modo-jogo, "ao invés de pressionar" (segurar). É a
solução robusta — um toque no PS sozinho **nunca mais** alterna o modo-jogo; o combo é deliberado e
não colide com PS-solo (Steam) nem com PS+dpad (troca de perfil).

### Mudanças no código (fork)

- `integrations/hotkey_daemon.py`
  - `HotkeyConfig.gamemode_toggle: tuple = ("ps","options")` (novo) + `DEFAULT_COMBO_GAMEMODE`.
  - `observe()`: registra o combo `gamemode` (só se não-vazio — `frozenset()` vazio é subconjunto de
    tudo e dispararia a cada tick).
  - `_fire()`: roteia `gamemode` → `on_ps_long_press` (reaproveita o callback de toggle da supressão).
  - `_observe_ps_solo()`: **guarda `ps_long_press_ms > 0`** — `0` desliga o long-press do PS (o PS
    solo passa a só abrir Steam).
  - `should_passthrough()`: inclui `gamemode_toggle` (o combo não vaza pro gamepad virtual em emulação).
- `daemon/lifecycle.py` — `DaemonConfig.ps_long_press_ms: int = 1000` (novo campo de config).
- `daemon/subsystems/hotkey.py` — **BUGFIX**: `start_hotkey_manager` agora **propaga a config** pro
  `HotkeyManager` (`HotkeyConfig(ps_long_press_ms=daemon.config.ps_long_press_ms)`). Antes a config
  nunca chegava → limiar preso em 1000ms.
- `daemon/main.py` — lê `HEFESTO_DUALSENSE4UNIX_PS_LONG_PRESS_MS` (default 1000).

### Config aplicada para a Vitória

- `~/.config/environment.d/91-hefesto-dualsense-gamemode.conf` → `..._PS_LONG_PRESS_MS=0`
  (persiste em reboot/login). Long-press do PS **desligado**; modo-jogo só pelo combo.
- Para a sessão atual: `systemctl --user set-environment ..._PS_LONG_PRESS_MS=0` +
  `daemon.reload {ps_long_press_ms: 0}` (aplicou ao vivo, sem esperar re-login).
- Des-supressão imediata: IPC `daemon.emulation.suppress {suppressed: false}`.

### Validação (sem hardware, via `HotkeyManager`)

4 cenários passaram: (1) PS+Options → toggle modo-jogo, **não** abre Steam; (2) long-press OFF →
segurar PS 2s **não** alterna nada, soltar abre Steam; (3) toque curto → Steam; (4) compat upstream:
com `ms=1000` o long-press ainda funciona.

## Como usar agora

- **PS (toque curto)** → abre/foca a Steam.
- **PS + Options (Start)** → liga/desliga o modo-jogo (suprime a emulação de mouse/teclado sem
  desligar o toggle). Útil pra alternar entre "navegar o desktop com o analógico" e "jogar".
- **Analógico esquerdo** → cursor; **direito** → scroll (com a emulação ligada e modo-jogo OFF).
- Equivalente ao modo-jogo, pela GUI: o toggle "Emular mouse+teclado" (desliga a emulação de vez).

## Durabilidade pós dist-upgrade (pergunta da Vitória)

- **`main`/instalação atualizados?** Sim. Instalação é **editável** (`.pth` aponta pro `src/` do
  repo) → o código que roda **é** o repo. Após o restart do daemon, as mudanças já estão no ar.
- **Steam full upgrade**: o guard do PSSupport edita um *valor* no `localconfig.vdf` (formato
  estável); baixo risco. O guard (`hefesto-steam-input-guard.path/.timer`) sobrevive a upgrades.
- **Sistema full dist upgrade**: o risco real é o **venv quebrar** se o Python do sistema bumpar
  (ex.: 3.11→3.12) — `bin/python` do venv aponta pra um interpretador removido. O `install.sh`
  **antes** só recriava o venv no caso pyenv (`home != /usr/bin`); **não** pegava bump de versão.
  - **Hardening aplicado** (`install.sh`, `DURABILIDADE-DIST-UPGRADE-01`): detecta `bin/python`
    inexecutável **ou** divergência de minor version (venv vs. sistema) e **recria o venv**.
    Idempotente — no-op quando a versão bate. Após um dist upgrade, basta re-rodar `./install.sh`
    (idempotente) que ele se auto-cura.

## Pendências / próximos passos

1. **GUI**: mostrar o estado do **modo-jogo** (suprimido sim/não) na aba Mouse — hoje não há
   indicador, o que fez a "flag parecer que não ativa". Idealmente um controle dedicado + expor
   `gamemode_toggle` e `ps_long_press_ms` nas preferências.
2. **CLI**: expor um `mouse suppress on/off` (hoje o toggle de supressão só via IPC/long-press/combo).
3. **Commit** dessas mudanças no fork (não commitado ainda no fim da sessão).
4. Confirmar ao vivo: PS+Options alternando o cursor durante o jogo, e PS-curto abrindo a Steam sem
   nunca mais cair no modo-jogo.
