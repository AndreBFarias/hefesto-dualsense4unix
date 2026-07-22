# Diagnóstico 22/07 (tarde) — GUI/perfis/autoswitch: 6 causas-raiz medidas e os fixes

**Contexto**: sintomas relatados pela mantenedora ao vivo: (1) "cores automáticas não
funcionam"; (2) "salvar perfil / aplicar / configs por controle não importam"; (3)
"Sackboy muda sozinho pro modo Jogar direto (Sony)"; (4) player LEDs "errados" na aba
Lightbar (P1 acende o LED 3 etc.); (5) seletor do topo mostra "Nintendo — · BT" sem
número e sem botão da Sony com 1 DualSense; (6) MMJ tem badge "DualSense Controller"
na Steam — "é pra funcionar com hefesto + máscara dualsense". Diagnóstico com medição
ao vivo (journal, `state_full` via IPC, `/var/lib/bluetooth`, systemd) + 4 agentes de
leitura de código com evidência arquivo:linha.

## Causas-raiz confirmadas

### 1. Detecção de janela MORTA por race de login → autoswitch cego a sessão toda

- Medido: daemon subiu 13:54:02, logou `autoswitch_compositor_unsupported` +
  `window_detect_diag_seeded backend=null healthy=False`; o processo roda SEM
  `DISPLAY`/`WAYLAND_DISPLAY` no ambiente, MAS o `systemctl --user show-environment`
  TEM os dois (o COSMIC exportou depois do start).
- Mecanismo: `detect_window_backend()` lê só o `os.environ` e o backend é fixado UMA
  vez (`build_window_reader`); `_ensure_display_env()` só roda no start. O
  `ExecStartPre=import-environment` do .service veio vazio (compositor ainda não tinha
  exportado). Sem retry → NullBackend para sempre → perfil-por-jogo letra morta.
- **Fix (AUTOSWITCH-HEAL-01)**: `WindowReaderDiag.maybe_recover()` + re-tentativa
  rate-limitada (1x/15s) dentro do reader instrumentado: re-importa o env do systemd
  --user e re-detecta; ao sair do Null, re-semeia o diagnóstico no store e loga
  `window_detect_backend_recuperado`. Testes em `test_autoswitch_flood_fix.py`.

### 2. Perfil "FPS" preso desde 19/07 → mata a paleta automática

- Medido: `active_profile.txt` = "FPS" (mtime 19/07 23:04); `profile_activated
  name=FPS origin=system` às 13:55:55 = `restore_last_profile` na PRIMEIRA conexão do
  controle (não é autoswitch — com backend null o `_tick` nem avalia match).
- O restore ativava QUALQUER nome persistido, sem checar se o match do perfil faz
  sentido sem janela. Com a detecção morta, não há caminho de reversão (UX-01 retém
  até evidência positiva) → FPS eterno, lightbar do perfil por cima, paleta suprimida.
- **Fix (RESTORE-ESCOPO-01)**: `restore_last_profile` PULA perfis com match por
  janela/título/processo (`MatchCriteria` com campos preenchidos) — eles pertencem ao
  autoswitch; o restore de boot fica com os perfis MatchAny. Log honesto
  `last_profile_restore_pulado_perfil_de_janela`. Testes em `test_session_persist.py`.

### 3. Player LEDs: NÃO é bug — é o padrão OFICIAL do PS5

- `core/led_control.py:98-103` (e os presets da GUI) usam os padrões canônicos do
  console: P1 = LED central (3); P2 = 2 e 4; P3 = 1,3,5; P4 = 1,2,4,5. Exatamente o
  que a mantenedora observou. Ordem física `[L2, L1, centro, R1, R2]`.
- **Fix (UX)**: tooltips nos 4 presets explicando "Padrão oficial do PS5" (glade +
  po/mo). Comportamento intacto.

### 4. "Configs por controle não importam" — dois eixos divergentes (persistir × aplicar)

- A persistência por-controle vai por MAC (`uniq` no draft/perfil), mas os botões
  "Aplicar" de Gatilho/Lightbar aplicavam AO VIVO pelo caminho de índice
  (`_output_target_key`), que cai em **broadcast** quando o alvo desalinha
  (`backend_pydualsense.py:1620-1624`).
- **Fix (PERFIL-05)**: `led.set`/`led.player_set`/`trigger.set` aceitam `uniq`
  opcional; o daemon aplica via `apply_output_for(uniq, OutputSpec(...))` — registra o
  override por-MAC (camada ACIMA da paleta no merge, sobrevive a hotplug) e escreve SÓ
  naquele controle. GUI manda `_edit_uniq()` em todos os call sites. Fallback são para
  backends sem `apply_output_for`. Testes em `test_perfil05_apply_por_uniq.py`.

### 5. "Salvar não salva" — o daemon nunca relê perfil do disco sozinho

- `save_profile` grava o JSON no processo da GUI; o daemon só relê em
  `profile.switch`/boot/autoswitch. Salvar o perfil ATIVO não mudava nada no controle.
- **Fix (PERFIL-SAVE-APPLY-01)**: após salvar, se o perfil é o ativo no daemon, a GUI
  dispara `profile.switch` (relê o disco e reaplica); toast "Perfil salvo e reaplicado".

### 6. Seletor do topo (pedido dela) + slot "—" do externo

- Antes: seletor sumia com <2 controles; botão da Sony só com 2+ DualSense; externo
  sem opinião do registry mostrava "Nintendo — · BT".
- **Fix (SELETOR-UNO-01)**: aparece com 1+; com UM DualSense o botão é o próprio
  controle ("Sony 1 · BT", sem "Todos" — com um único controle são a mesma coisa);
  externo sem slot mostra "Nintendo · BT" limpo (número entra quando o daemon
  numerar); numeração dos externos usa a contagem REAL de DualSense.
- Nota do "—" persistente do screenshot: registry externo descarta o mapa em boot novo
  (gate por boot_id, by design) e o `peek` é leitura pura — a janela até o tick lento
  numerar existe; com o Pro sem evdev (probe BT falho) ela vira permanente.

## MMJ × badge "DualSense Controller" (correção de entendimento)

O badge da página é real — e a via é a **API Steamworks/Steam Input** (o binário chama
`SetDualSenseTriggerEffect`; estudo 2026-07-21-estudo-mmj-caminhos-dualsense.md). O
nosso desvenenamento global (`SteamController_PSSupport=0`) desliga exatamente essa
via; o middleware interno (InControl) não tem perfil p/ Edge 0DF2 → jogo mudo com a
máscara dualsense. Ou seja: o jogo TEM DualSense nativo, via Steam Input — e o nosso
guard revertia o opt-in per-app silenciosamente.

**Fix (STEAM-INPUT-ALLOWLIST-01)**: `disable_steam_input.sh` ganhou allowlist per-app
(`~/.config/hefesto-dualsense4unix/steam_input_apps.txt`, MMJ 2111190 incluso): o
`UseSteamControllerConfig` dos blocos `apps/<appid>` listados é PRESERVADO (transform
awk com pilha de blocos do VDF + cmp para idempotência real); o desvenenamento global
segue intacto. Passo humano: ligar o Steam Input do MMJ na GUI da Steam
(propriedades do jogo → Controle → "Usar configurações do Steam Input") — o guard não
reverte mais.

## BT (medições novas da tarde)

- Re-pair com `Pair()` explícito FUNCIONOU: bonds do roxo (13:55) e do Pro real
  (13:58) nasceram com `info` em disco. MAS o bond do Pro **evaporou de novo** quando
  ele saiu do BT (cabo às 14:08) — device some até do BlueZ. Suspeita: promoção não
  limpou `temporary` de verdade, OU remoção manual. Vigiar no próximo ciclo BT.
- Roxo ficou `Bonded=true` + `Trusted=false` → sem autorização de reconexão entrante.
  **Fix**: vigia 2b no `bt_health_watchdog.sh` — device conectado com Trusted=false
  ganha `Trusted=true` via busctl (idempotente); aplicado no roxo ao vivo.
- Pro BT com patch 0002 ativo: conectou com LEDs ok, mas o link perdeu 4-10 reports de
  IMU continuamente (13:57-13:59) + 3x `exceeded` — perda sustentada de rádio. O
  8BitDo BT estabilizou com os patches (relato dela); o Pro real segue frágil em BT →
  cabo é a rota estável (doutrina), diagnóstico fino de rádio (btmon em janela) é gate
  humano opcional.
- input-remapper INOCENTADO: presets só de teclado/mouse Redragon; autoload não faz
  grab nos controles.

## Outras mudanças

- `DaemonConfig.gamepad_flavor` default: xbox → **dualsense** (HARMONIA-MASK-01;
  decisão dela 22/07 + validação da máscara em jogo real; o flag persistido vence
  sempre — o default só governa instalação nova).
- Observação: o `launch_env` do boot materializou `mascara=xbox` porque o FLAG
  continha "xbox" até ela trocar p/ dualsense às 13:56 — não era bug de leitura.
- `lightbar_rgb=[252,128,0]` no slot 1 com `lightbar_source="sysfs"` = escritor
  estrangeiro (cliente Steam) no nó de LED — família conhecida (Onda N, cache
  GUERRA-01 não re-lê sysfs). Sem mudança nesta leva.

## Adendo 22/07 15h — sessão ao vivo: 2 regressões/incidentes a mais, medidos

### LIGHTBAR-BT-RESET-03 — lightbar BT apagada = regressão do 0x08 por SEQUÊNCIA

Relato dela: "só no cabo fica laranja; em BT apaga — já resolvemos isso". Journal
14:55:05: `lightbar_reset_enviado` + cor escrita logo depois E barra escura →
escrita não colando = claim NÃO devolvido = o 0x08 não está fazendo efeito.

Arqueologia fecha a causa: a cura do 0x08 foi provada em 17/07, quando TODOS os
nossos reports 0x31 saíam com `seq=0`. Em 18/07 o BTREPORT-02 introduziu o nibble
de sequência POR-HANDLE (`writeReport` carimba seq+CRC e incrementa) para
keepalive/réplica — mas o reset continuou escrevendo DIRETO no device com
`seq=0` fixo. Depois que o keepalive avança o contador, o firmware descarta o
reset como fora de sequência → claim preso → todas as escritas de cor ignoradas
(sintoma pré-cura de volta). **Fix**: `send_release_leds` agora recebe o HANDLE
e envia pelo MESMO `writeReport` (seq/CRC na ordem real do fluxo; device cru
segue como fallback) + o cache do nó sysfs é INVALIDADO após cada 0x08
(RESET-01 adoção e RESET-02 wake) — reset enviado ⇒ a reescrita seguinte é real,
nunca `skip_cache`. Validação ao vivo: reconectar o roxo BT após restart do
daemon (jogo fechado!) e ver a barra na cor do slot.

### Incidente Steam Input no Sackboy (15h) — duplicatas + rumble "invertido"

Ela ativou "entrada steam" mirando o MMJ e o opt-in caiu no SACKBOY
(`apps/1599660/UseSteamControllerConfig=2` no vdf). Consequência imediata na
sessão: a Steam criou pads virtuais por cima de cada controle → Nintendo como
P1+P4, Sony (vpad) como P2+P3, e vibração "invertida" (constante em repouso,
para nos eventos = dois escritores de rumble brigando). O daemon estava limpo
(`rumble_active=None`, wrapper_used=True). Cura: fechar o jogo e a Steam — o
guard reverte o Sackboy sozinho (fora da allowlist); o Steam Input do MMJ é a
única exceção. **Follow-up entregue**: os 3 avisos de Steam Input (storm_doctor
da GUI, aba Emulação, doctor.sh via --status do script) agora são
allowlist-aware — opt-in deliberado não acusa mais "conflita!"; o veredito usa
`needs_real_fix` (a transformação mudaria o arquivo?).

### Pro Controller BT às 15:06 (observação do monitor)

Reconectou sem bond do lado PC (JustWorks), probe completou COM LEDs e evdev
(patches agindo), e o link morreu em ~1 min sob cascata de `timeout waiting for
input report` com Sackboy + roxo BT no ar (dois streams no mesmo adaptador).
Reforça: perda de rádio sustentada específica do Pro; cabo é a rota estável;
próximo passo de medição é btmon numa reconexão controlada.
