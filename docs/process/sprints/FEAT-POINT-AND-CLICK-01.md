# FEAT-POINT-AND-CLICK-01 — Modo point-and-click por perfil (Grim Fandango e afins)

**Tipo:** feat (grande — schema + daemon + autoswitch + perfil default + GUI mínima).
**Wave:** V3.11.
**Estimativa:** 2 iterações.
**Dependências:** FEAT-MOUSE-CURSOR-FEEL-01 (cursor digno — sem ele o modo é
inutilizável); BUG-MOUSE-GUI-SYNC-01 (draft com dirty da seção mouse).
**Status:** READY.

---

**Tracking:** labels `type:feat`, `profiles`, `mouse-emu`, `kbd-emu`, `ai-task`,
`status:ready`.

## Contexto

Diagnóstico 2026-07-03, achados A8-A10. A Vitória joga Grim Fandango Remastered — o
jogo TEM point-and-click por mouse oficial (código do mod Grim Mouse incorporado em
2015), então **o modo mouse do hefesto é o caminho certo**; mas hoje:

1. **A10 — bindings de desktop vazam para o jogo**: com emulação ativa, options→Super
   (abre o launcher do COSMIC por cima do jogo — visto no journal de hoje às 21:59),
   create→PrintScreen, l1/r1→Alt+(Shift+)Tab. Não existe supressão automática por
   janela; o modo-jogo é 100% manual (PS+Options).
2. **A8 — wiring A-06 furado**: `profile.switch` via IPC e autoswitch NÃO propagam
   `key_bindings` ao teclado vivo — `start_ipc` (`subsystems/ipc.py:69`) cria
   `ProfileManager` sem `keyboard_device` e `start_autoswitch`
   (`autoswitch.py:105-109`) captura `None` no boot (keyboard sobe depois,
   `lifecycle.py:262/266` vs `271-272`). Repro pytest com wiring real falha; o teste
   existente injeta mock e mascara. Sem esse fix, um perfil point-and-click não
   aplicaria bindings ao focar o jogo.
3. **Perfil não controla mouse**: Profile v1 não tem seção mouse
   (`draft_config.py:196-199` descarta) — impossível "focar o jogo → mouse liga com
   velocidade certa" via autoswitch.
4. **A9 — contexto Steam**: o jogo embarca SDL 2.0.3 + `controllerdef.txt` sem o GUID
   do DualSense (por isso ignora o controle cru — o que, no modo mouse, é até BOM:
   sem input duplicado). Steam Input neste título é incompatível no Linux (bug 2019).
   Rota alternativa de gamepad nativo: máscara xbox360 do gamepad virtual (GUID X360
   Linux presente no arquivo do jogo).

Extra da mesma área: journal inundado por `autoswitch_suppressed_by_manual_override`
a ~2 Hz (1074/1477 linhas em 2h) — rate-limit entra aqui por tocarmos o autoswitch.

## Decisão

1. **Fix A-06 por provider lazy** (pré-requisito):
   - `ProfileManager` ganha `keyboard_device_provider: Callable[[], object | None] | None`;
     `apply_keyboard` resolve `provider() if provider else self.keyboard_device`.
   - `start_ipc` e `start_autoswitch` passam
     `lambda: getattr(daemon, "_keyboard_device", None)`.
   - Migrar também `connection.py:82` e `hotkey.py:92` para o provider (imuniza
     contra device recriado em reload/reconnect — `connection.py:233-236` anula e
     recria).
   - Trocar o teste `test_ipc_profile_switch_propaga_teclado` por um que exercita o
     wiring real: `start_ipc(daemon)` com `_keyboard_device=None`, setar o device
     DEPOIS, invocar `_handle_profile_switch`, afirmar `set_bindings` chamado. Caso
     análogo para o autoswitch.
2. **Profile ganha seção opcional de emulação** (aditivo, sem bump de versão —
   campos opcionais com default None/False; JSONs v1 continuam válidos):
   - `mouse: ProfileMouseConfig | None = None` com `enabled: bool`,
     `speed: int = 6` (1-12), `scroll_speed: int = 1` (1-5).
   - `suppress_desktop_emulation: bool = False` — quando True, ativar o perfil chama
     `daemon.set_emulation_suppressed(True)` (setter existente já faz flush e
     notifica, `lifecycle.py:470-492`); False restaura. Para jogos de GAMEPAD (não é
     o caso do Grim); default False não muda nenhum perfil existente.
   - `ProfileManager.activate` aplica a seção mouse via callable
     `mouse_applier: Callable[[bool, int, int], None] | None` (injetada pelos
     callsites com `daemon.set_mouse_emulation`); `mouse=None` = não toca no estado
     de mouse (comportamento atual).
   - Respeitar toggle manual: se a usuária alternou modo-jogo manualmente há menos de
     `MANUAL_PROFILE_LOCK_SEC`, o autoswitch NÃO mexe na supressão (mesmo padrão do
     lock de perfil manual).
3. **GUI/draft**: `from_profile`/`to_profile` param de descartar a seção mouse quando
   o perfil a tiver (draft já tem `MouseDraft`); aba Perfis/editor não ganha UI nova
   além do que o draft já expõe — salvar perfil com a seção mouse tocada persiste.
   (UI dedicada de "modo point-and-click" fica fora de escopo.)
4. **Perfil default novo** `assets/profiles_default/point_and_click.json`:
   - `match`: `window_class` com `["GrimFandango", "grim", "scummvm", "residualvm"]`
     (verificar o wm_class real da janela ao vivo antes de fechar a lista),
     `priority: 60` (acima de navegacao=50).
   - `mouse`: `{"enabled": true, "speed": 8, "scroll_speed": 1}`.
   - `key_bindings` (override completo — só estes botões emitem; sem Super/Alt+Tab/
     PrintScreen/OSK):
     - `l1` → `KEY_LEFTSHIFT` (correr)
     - `r1` → `KEY_DOT` (pular diálogo)
     - `options` → `KEY_ESC` (menu do jogo)
     - `create` → `KEY_I` (inventário)
     - `touchpad_left_press` → `KEY_E` (examinar)
     - `touchpad_middle_press` → `KEY_U` (usar)
     - `touchpad_right_press` → `KEY_P` (pegar)
   - Mapeamentos fixos do device de mouse completam o esquema: X/L2=clique esquerdo
     (andar/interagir), Triângulo/R2=clique direito, R3=botão do meio, Círculo=Enter
     (confirmar), Quadrado=Esc (voltar), D-pad=setas (andar).
   - `triggers`: Off/Off (jogo de aventura; sem resistência), `rumble.passthrough:
     true`, lightbar livre.
5. **Rate-limit do log do autoswitch**: `autoswitch_suppressed_by_manual_override`
   loga 1x por candidato (ou por mudança de candidato), não a cada tick de 0,5s.

## Critérios de aceite

- [ ] Teste do wiring real (A8): `start_ipc` + device setado depois → `profile.switch`
      propaga bindings; idem autoswitch. O repro que hoje falha vira verde.
- [ ] Perfil com `mouse.enabled=true` ativado (IPC/autoswitch/hotkey/restore): modo
      mouse liga com speed/scroll do perfil; perfil sem seção mouse não toca no
      estado (regressão).
- [ ] Perfil com `suppress_desktop_emulation=true` ativado: emulação suprimida +
      flush; ao trocar para perfil sem o campo: supressão liberada. Lock manual
      respeitado (teste com relógio fake).
- [ ] `point_and_click.json` carrega, valida contra o schema e aparece em
      `profile list`; ativá-lo com FakeController emite `KEY_E/U/P` nas regiões do
      touchpad e `KEY_LEFTSHIFT` no l1 (log `key_binding_emit`).
- [ ] Autoswitch com janela fake `GrimFandango` seleciona o perfil (teste unitário
      do matcher) e o log suprimido não repete por tick.
- [ ] Draft: `from_profile` de perfil com mouse popula `MouseDraft`; `to_profile`
      com seção mouse dirty inclui a seção; perfil legado (sem mouse) round-trip
      inalterado.
- [ ] Suite completa verde; ruff/mypy limpos; smoke USB e BT.

## Arquivos tocados

- `src/hefesto_dualsense4unix/profiles/schema.py` (ProfileMouseConfig +
  suppress_desktop_emulation + validators).
- `src/hefesto_dualsense4unix/profiles/manager.py` (providers/appliers; activate).
- `src/hefesto_dualsense4unix/daemon/subsystems/ipc.py`,
  `.../subsystems/autoswitch.py`, `.../connection.py`,
  `.../subsystems/hotkey.py` (providers + appliers).
- `src/hefesto_dualsense4unix/profiles/autoswitch.py` (rate-limit do log, lock da
  supressão).
- `src/hefesto_dualsense4unix/app/draft_config.py` (round-trip da seção mouse).
- `assets/profiles_default/point_and_click.json` (novo).
- `docs/protocol/` e `docs/usage/` (nota curta da seção mouse do perfil).
- `tests/unit/` (wiring real, schema, activate, autoswitch, draft round-trip).

## Proof-of-work runtime

```bash
.venv/bin/pytest tests/unit -q
.venv/bin/ruff check src/ tests/
.venv/bin/mypy src/
./scripts/check_anonymity.sh
python3 scripts/validar-acentuacao.py --all
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=usb HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke
HEFESTO_FAKE=1 HEFESTO_FAKE_TRANSPORT=bt  HEFESTO_SMOKE_DURATION=2.0 ./run.sh --smoke --bt

# Cenário manual (validação da Vitória, controle via BT, Grim Fandango aberto):
# 1. Confirmar wm_class real: hefesto doctor/journal do autoswitch ao focar o jogo.
# 2. Focar o jogo → autoswitch ativa point_and_click → cursor liga com speed 8;
#    stick move Manny via clique; L1 segura Shift (corre); touchpad E/U/P; Options=menu.
# 3. Alt-tab para o desktop → perfil anterior volta → Super/Alt+Tab de volta ao normal.
# 4. Journal SEM spam de autoswitch_suppressed a 2 Hz.
```

## Notas para o executor

- **Verificar o wm_class real da janela do jogo ao vivo** antes de fechar o match
  (journal do autoswitch mostra o candidato; a memória da sessão indica
  `GrimFandango`). Se o jogo roda via Proton/nativo o wm_class muda — o port Linux é
  nativo (binário `GrimFandango` ELF i386).
- O perfil ativo da Vitória é `vitoria` (override manual, priority 5). Autoswitch só
  vence override manual expirado — documentar no cenário manual que ela precisa
  liberar o lock (trocar para o perfil via autoswitch ou esperar o lock expirar).
- key_bindings com dict = override SEM merge (só os listados emitem) — é exatamente o
  que queremos: nada de Super/Alt+Tab/PrintScreen/OSK dentro do jogo.
- NÃO gatear gamepad virtual por `suppress_desktop_emulation` (footgun "tijolo"
  documentado em 2026-06-27-suporte-multiplos-controles.md:50-54).
- Alternativa de gamepad nativo para o Grim (documentar no doc de usage, sem código):
  `gamepad on` com máscara xbox360 + abrir o jogo DEPOIS do device virtual existir.
  Não é o caminho preferido (o point-and-click por mouse é superior neste jogo), mas
  vale registrar para jogos de gamepad com SDL antigo.
- Steam Input permanece OFF para este título (incompatibilidade conhecida no Linux;
  `UseSteamControllerConfig` pendente será reaplicado pelo guard quando a Steam
  fechar).

## Fora de escopo

- UI dedicada "modo point-and-click" na GUI (usa-se perfis existentes).
- Mapeamentos de BOTÃO DE MOUSE configuráveis por perfil (X/Triângulo/R3/Círculo/
  Quadrado/D-pad continuam fixos do device).
- Editar `controllerdef.txt` do jogo (Steam pode reverter; e não precisamos dele no
  modo mouse).
- Auto-detecção genérica de "é um jogo" (só match por window_class de perfil).
- Persistência do modo-jogo manual entre boots.
