# Estudo 2026-07-18 — RDR2 nativo+BT: a 2ª causa (BT-07 / FUT-03)

> Diagnóstico AO VIVO read-only (2026-07-18 ~21h50) da sessão real de gameplay: DualSense **branco
> USB** (físico do vpad P1, `HID_UNIQ 14:3a:9a:00:00:04`, hidraw3), DualSense **roxo BT** (player 2,
> `HID_UNIQ a0:fa:9c:00:00:01`, hidraw7), 2 vpads uhid (`02:fe:00:00:00:01/02`, hidraw6/8), Pro
> Controller Nintendo USB + 8BitDo no cabo (2× 057e:2009). Daemon PID 2469 vivo, controles em uso.
> **Cenário perfeito:** branco (054c:0ce6) em USB e roxo (054c:0ce6) em BT — MESMO VID/PID em
> transportes diferentes — para testar a hipótese do "gêmeo colapsado no SDL". MACs neste doc são os
> reais da sessão (máquina da mantenedora; redigir na publicação se necessário).

## TL;DR — a 2ª causa mais provável, COM EVIDÊNCIA

**A 2ª causa NÃO é rádio (CRC) nem dedup-de-serial do SDL. É a MESMA "guerra de escritores" do
winebus — um AGLOMERADO de faces Sony no prefixo Proton — só que ela sobra INTACTA no Modo Nativo,
que é exatamente onde o "RDR2 nativo + BT" cai.** A onda fim-da-guerra (`PROTON_DISABLE_HIDRAW` +
IGNORE do SDL) cura o aglomerado nos modos com vpad (hefesto/playstation/xbox), mas por construção
`compose_env` **não emite NADA no Modo Nativo** (`launch_env.py:183-192`) — expor o físico ali é o
próprio objetivo do modo. Logo o cenário "nativo + BT" continua na dependência de dois fatores que
só o gate humano A/B fecha: **(a) PSSupport / Steam Input** e a ordem de binding do SDL do Proton
sobre o físico BT.

## Evidência ao vivo (read-only)

### Quem abre cada hidraw (lsof) — o AGLOMERADO provado

| nó | device | quem tem aberto |
|----|--------|-----------------|
| hidraw3 | branco USB `054C:0CE6` | `hefesto-d` 2469, **`steam` 6034**, **`winedevice` 7347 (2 fds)** |
| hidraw7 | roxo BT `054C:0CE6` | `hefesto-d` 2469, **`steam` 6034**, **`winedevice` 7347 (2 fds)** |
| hidraw6 | vpad P1 `054C:0DF2` | `winedevice` 7347 |
| hidraw8 | vpad P2 `054C:0DF2` | `steam` 6034, `winedevice` 7347 (2 fds) |

O `winedevice.exe` (winebus do Proton) tem **os quatro** abertos ao mesmo tempo — 2 físicos
(USB+BT, mesmo VID/PID) + 2 vpads. É a whitelist default do winebus dando hidraw à família Sony
inteira, confirmando FATO 1 do estudo-guerra. Não é dedup, é MULTIDÃO.

### Serials distintos — a hipótese do "gêmeo" está REFUTADA

`HID_UNIQ`: branco USB `14:3a:9a:00:00:04` · roxo BT `a0:fa:9c:00:00:01` · vpad P1
`02:fe:00:00:00:01` · vpad P2 `02:fe:00:00:00:02`. **Quatro serials diferentes.** Os nomes de
produto também diferem (USB = "Sony Interactive Entertainment DualSense Wireless Controller"; BT =
"DualSense Wireless Controller"). O combine wiredwireless do SDL casa por **serial**; dois físicos
distintos nunca colapsam. O "DualSense BT invisível ao SDL quando o gêmeo USB de mesmo VID/PID está
no HIDAPI" (achado do índice) **não sobrevive**: branco e roxo são controles físicos DIFERENTES,
MACs diferentes — o SDL enxerga os dois. O `identity.py` do daemon confirma a mesma lógica no nosso
lado (chaveia por MAC 12-hex normalizado; branco e roxo caem em slots distintos, o vpad `02fe*` nunca
ganha slot — `identity.py:79,206`).

### Rádio BT — CRC/storm REFUTADO como causa

- `dmesg`: só **2** `DualSense input CRC's check failed` em ~3,5 h (ts 3937 e 10370, device
  `0005:054C:0CE6.000A`). O kernel `hid-playstation` descarta o report ruim em silêncio — não vira
  input travado.
- `hciconfig hci0`: **errors 0** em RX e TX (RX 635 MB / TX 2,6 MB, 0 sco errors).
- Link roxo: `ACL a0:fa:9c:00:00:01 state 1 CENTRAL AUTH ENCRYPT`, **RSSI -72**, `Connected: yes`,
  `Modalias usb:v054Cp0CE6d0100`. Encriptado e saudável.
- **Nenhum clone DS4 `05C4` pareado nesta sessão** (só DualSense + 8BitDo `Pro Controller`
  `e4:17:d8:00:00:02`). O candidato (c) do sprint (clone stormando o adaptador) simplesmente não
  está presente — era o gatilho, e ele não está em campo. Candidato (c) **descartado** para BT-07.

### Sem -EIO/timeout no handshake BT agora

`dmesg` mostra o roxo registrando LIMPO: `Registered DualSense controller hw_version=0x00000710
fw_version=0x0110002a`, feature reports de calibração OK no connect. **Nenhum** `hidp` timeout /
`-EIO` / `-71` no ciclo. O risco `hidp_get_raw_report` (5×HZ → -EIO) do kernel NÃO se manifestou em
repouso — mas ele é sob CONTENÇÃO do canal de controle HID único do BT (daemon keepalive 0,5 s +
Steam probing + jogo probing no MESMO canal), cenário que só existe com RDR2 aberto. Fica como
variável do A/B, não como fato provado.

### Steam Input / PSSupport

`localconfig.vdf` (userdata/1300222895): `SteamController_PSSupport` = **"0"** (linha 1106 — o
default do nosso install), `UseSteamControllerConfig` = "0" no Sackboy (1599660), **sem
`IGNORE_DEVICES`** no vdf (desenvenenado). PSSupport zerado = Steam Input NÃO adota o DualSense como
face PS própria; o físico chega cru ao prefixo. Para "nativo + BT" isso deixa o binding inteiramente
na mão do SDL do Proton — é a alavanca #1 do A/B (religar temporário e ver se o RDR2 passa a ler).

## Conclusão — ranking da 2ª causa

1. **Aglomerado winebus (guerra de escritores) — PROVADO, mas escopo é o Modo Nativo.** É a mesma
   raiz do estudo-guerra; sobra intacta em `compose_env` nativo (`launch_env.py:167-169,183`). Em
   "RDR2 nativo + BT" o jogo vê branco USB + roxo BT + (se houver) vpads como uma multidão de faces
   Sony e faz binding no dispositivo errado / num player-slot que o RDR2 (só player 1) ignora.
2. **PSSupport / binding SDL-do-Proton sobre o físico BT — PROVÁVEL, não fechável read-only.**
   PSSupport=0 hoje; A/B religando (ou desativando Steam Input por-jogo) decide. Único caminho: gate
   humano com RDR2 aberto.
3. **Contenção do canal de controle HID do BT (hidp 5×HZ → -EIO) — POSSÍVEL, só sob carga.** Não
   observado em repouso; observável só com RDR2 + Steam + daemon disputando o canal.
4. ~~Dedup de serial do SDL (b)~~ — **REFUTADO** (4 serials distintos).
5. ~~CRC/clone DS4 stormando (c)~~ — **REFUTADO** (2 CRC/3,5 h, errors 0, nenhum clone pareado).

## O que a onda fim-da-guerra resolve vs o que sobra

| Célula | fim-da-guerra faz | resultado esperado |
|--------|-------------------|--------------------|
| RDR2 + BT em modo **vpad** (hefesto/playstation) | `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` + `SDL...IGNORE_DEVICES=0x054c/0x0ce6` — some o físico (USB E BT) dos DOIS canais; vpad uhid 0df2 fica como face ÚNICA (`launch_env.py:189-191`) | **CURADO** — o aglomerado colapsa para 1 face |
| RDR2 + BT em modo **xbox** | idem + `SDL_JOYSTICK_HIDAPI=0` (SDL lê o evdev grabado); vpad uinput 045e nunca colide com 0ce6 (`:185-188`) | **CURADO** |
| RDR2 + BT em **Modo Nativo** | **NADA** (só shader-cache) — expor o físico é o objetivo do modo (`:167-169,183`) | **NÃO tocado** — depende de PSSupport + binding SDL/Proton |
| Pré-requisito em qualquer célula | precisa do **wrapper `hefesto-launch`** consumir a env; hoje o jogo roda SEM wrapper (FATO 0 do estudo-guerra) | env materializada mas **não consumida** até o wrapper entrar no PATH |

**Resumo:** se a Vitória estava num modo com vpad quando o RDR2 ficou mudo por BT, fim-da-guerra
cobre — DESDE que o wrapper exporte a env. Se estava em **Modo Nativo**, fim-da-guerra é
irrelevante por design e o BT-07 tem de rodar o A/B de PSSupport / Steam Input.

## Matriz de teste BT-07 (executável — gate humano)

**Pré-condições (uma vez):** daemon em `--foreground` (log = stdout, NUNCA `journalctl --user`);
`hefesto-launch` no PATH e a LaunchOption do jogo apontando pra ele (senão a env não chega — FATO 0);
`dmesg -w` num terminal à parte. Roxo pareado/trusted por BT, branco no USB.

**Verificação de env por célula (antes de abrir o jogo):** conferir
`~/.local/state/hefesto-dualsense4unix/launch_env/{default,steam_app_1174180}.env`:
- vpad DualSense (uhid) → deve ter `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` + `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`.
- vpad Xbox → + `SDL_JOYSTICK_HIDAPI=0`.
- Modo Nativo → só `__GL_SHADER_DISK_CACHE*` (sem hidraw env). Confirma o escopo.

**Matriz (appid RDR2 = 1174180; Sackboy = 1599660):**

| # | Jogo | Transporte | Modo | Wrapper | env esperada | resultado esperado |
|---|------|-----------|------|---------|--------------|--------------------|
| 1 | Sackboy | USB | hefesto/PS | sim | DISABLE+IGNORE | joga + vibra (baseline USB) |
| 2 | Sackboy | **BT** | hefesto/PS | sim | DISABLE+IGNORE | joga + vibra por BT (aceite BT-07.1) |
| 3 | Sackboy | BT | **xbox** | sim | +HIDAPI=0 | joga; isola se o problema é layout PS |
| 4 | RDR2 | USB | hefesto/PS | sim | DISABLE+IGNORE | joga (baseline RDR2) |
| 5 | RDR2 | **BT** | **hefesto/PS** | sim | DISABLE+IGNORE | **alvo:** deve jogar (fim-da-guerra) |
| 6 | RDR2 | BT | **xbox** | sim | +HIDAPI=0 | célula obrigatória da revisão técnica |
| 7 | RDR2 | **BT** | **Modo Nativo** | sim | só shader | **célula da 2ª causa** — se falhar, A/B abaixo |

**A/B da célula #7 (RDR2 nativo+BT mudo) — ordem obrigatória do sprint:**
- **A1 — PSSupport:** `steam -shutdown`; editar `localconfig.vdf` `SteamController_PSSupport`
  `"0"→"1"`; reabrir; repetir #7. Passou a ler → causa (a) confirmada. (Reverter ao fim: nosso
  install zera de volta.)
- **A2 — Steam Input por-jogo:** Propriedades do RDR2 → Steam Input → "Desativado"; repetir #7.
  Isola Steam-Input-layer vs SDL-do-Proton.
- **A3 — trocar de modo:** rodar o MESMO RDR2 por BT em modo vpad (#5). Se #5 joga e #7 não, a 2ª
  causa está confirmada como escopo-Modo-Nativo (o que fim-da-guerra não cobre) e a recomendação
  vira "para BT, usar modo vpad" — sem env nova.

**Registro de cada falha (obrigatório):** stdout do daemon `--foreground` + `dmesg` do instante
(procurar `CRC`, `hidp`, `-EIO`, `-71`, `Registered DualSense`), NÃO `journalctl --user`. Anexar
`lsof /dev/hidraw{3,7}` no momento (quem tem o físico BT aberto) e `hciconfig hci0` (errors/RSSI).

**Critério de fechamento (do sprint, honrado):** teste verde sem validação ao vivo NÃO fecha —
BT-07 fecha SÓ com a Vitória confirmando inputs+vibração por BT no Sackboy nos dois modos (#2, #3) e
com o RDR2 por BT ou funcionando (#5/#7) ou com a falha registrada + A/B preenchido.

## Armadilhas que este gate atravessa

- **Wrapper ausente = env fantasma** (FATO 0): `dedup_ok`/`wrapper_used` do state_full têm de dizer
  que o jogo passou pelo `hefesto-launch`, senão a matriz mede o estado errado.
- **Report BT malformado = keepalive no-op protetor**: hoje o rumble do jogo por BT sobrevive por
  bug; se a onda consertar o report 0x31 SEM o keepalive neutro, o roxo PARA de vibrar (risco do
  estudo-guerra) — refazer #2/#5 depois dessa mudança.
- **Modo Nativo recria/solta o físico**: alternar modo mid-game invalida os handles do jogo
  (achado colateral 3 do estudo-guerra) — escolher o modo ANTES de abrir cada célula, nunca no meio.
- **CRC é ruído, não causa**: 2/3,5 h; não perseguir rádio a menos que apareça storm (>dezenas/h)
  com clone `05C4` pareado.
