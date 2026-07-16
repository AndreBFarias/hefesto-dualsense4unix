# Sprint 2026-07-16 — VPAD sempre Edge: o vpad nunca mais divide VID/PID com o físico

**Status: PLANO. Nada deste doc foi implementado.** Frente derivada do Estudo 1 (117
agentes, 2026-07-16) + revisão adversarial em 3 lentes (técnica, regressão, escopo).
Branch `sprint/harmonia-uhid`. Fase A da dupla "vpad sempre Edge" (este doc) → "dedup
por udev" (Fase B, `2026-07-16-sprint-edge-dedup-e-fechamento.md` e sucessor).

Relato da Vitória que motiva a frente: por cabo tudo funciona (as duas máscaras); por
BT os DualSense ficam conectados **sem nenhum input** em qualquer modo; e a launch
option `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` está **persistida** na Steam
(localconfig.vdf, appid 1599660/Sackboy) esperando qualquer degradação do vpad para
esconder físico E vpad ao mesmo tempo → jogo com ZERO controles.

## TL;DR

O vpad só vira DualSense Edge (`054c:0df2`, uhid) num caminho feliz estreito: físico
conectado no boot **e** blueprint legível naquele instante. Fora disso ele nasce
`uinput` com o catálogo `FLAVORS["dualsense"]` = **`054c:0ce6` — o mesmo VID/PID do
físico** — em silêncio. Com a launch option persistida, isso é a receita exata do
"zero controles". A cura central é **parar de depender do físico**: embutir no pacote
um **blueprint canônico USB** (descriptor 289 B + features 0x05/0x09/0x20) e o vpad
nasce Edge/uhid **sempre**, até sem controle conectado. Em volta dela, quatro redes de
segurança: promoção no hotplug (VPAD-01), promoção pela GUI (VPAD-02), fallback uinput
nunca mais `0ce6` (VPAD-04) e fallback nunca silencioso (VPAD-05). Um teste-invariante
(VPAD-06) trava tudo. **Regra de ouro honrada de graça: esta frente é 100% código** —
o install.sh já põe por default a `71-uhid.rules` + modules-load (`uinput`, `uhid`),
nada novo para colar, exportar ou rodar depois.

## A causa-raiz (PROVADA — sobreviveu às duas revisões adversariais)

O vpad só vira Edge/uhid quando **duas** condições valem ao mesmo tempo:

1. o físico já estava conectado quando o vpad foi criado — senão `hidraw_path=None` →
   uinput (`integrations/virtual_pad.py:147-149`);
2. o blueprint do físico foi legível **naquele instante** — EIO em BT → `None` →
   uinput (`virtual_pad.py:153-157`; `uhid_gamepad.py:376-380`).

Fora desse caminho feliz, três buracos — todos PROVADOS NO CÓDIGO, manifestação ao
vivo provada pelo Estudo 1:

- **(a) Hotplug tardio nunca promove.** O bloco offline→online do `reconnect_loop`
  publica `CONTROLLER_CONNECTED`, notifica e restaura perfil, mas **não** chama
  `upgrade_primary_vpad_to_uhid` — o único caller no repo é o connect inicial do boot
  (`daemon/connection.py:208-231`; caller único em `daemon/lifecycle.py:388-393`).
  E o upgrade do boot ainda exige hidraw legível NA HORA
  (`daemon/subsystems/gamepad.py:251-252`) — na janela ruim do EIO, nem ele salva.
- **(b) Re-selecionar DualSense na GUI é no-op.** O early-return de
  `start_gamepad_emulation` compara **só o flavor** (`gamepad.py:295-298`) e os dois
  backends respondem `'dualsense'` (`uhid_gamepad.py:465-473`) — não existe caminho
  pela interface para forçar a promoção.
- **(c) O fallback é venenoso.** Blueprint falhou → `UinputGamepad` com
  `FLAVORS['dualsense']` product=`0x0CE6` (`uinput_gamepad.py:56-57` + `80-91`) —
  idêntico ao físico. O log avisa (warning) mas nada chega à usuária.

Agravante estrutural (PROVADO AO VIVO nesta máquina): o descriptor do físico por
**Bluetooth** tem 321 B **com** o item `85 31` (input 0x01 de ~10 B) — copiar o
blueprint do físico em BT produz um vpad `BUS_USB` torto **mesmo quando a captura
funciona**. O EIO do estudo é intermitente (janelas de ~5,1 s; o mesmo nó leu OK 3/3
na revisão), então retry não é garantia. A dependência do físico é o defeito de raiz,
não só o EIO.

## Evidências e confiança (honestidade brutal)

| Evidência | Onde | Confiança |
|---|---|---|
| Reconnect não promove; caller único no boot | `connection.py:208-231`, `lifecycle.py:388-393` | PROVADO NO CÓDIGO |
| Early-return por flavor; GUI no-op | `gamepad.py:295-298`, `uhid_gamepad.py:465-473` | PROVADO NO CÓDIGO |
| Fallback uinput = `054c:0ce6` | `virtual_pad.py:147-157`, `uinput_gamepad.py:56-57+80-91` | PROVADO NO CÓDIGO |
| Descriptor USB 289 B sem `85 31`; features 0x05/0x09/0x20 = 41/20/64 B | hidraw2 ao vivo (mesmo controle/firmware `0x0630` do bfd51db) | PROVADO AO VIVO |
| Descriptor BT 321 B **com** `85 31`; EIO intermitente | hidraw4 ao vivo (legível na revisão, EIO no estudo) | PROVADO AO VIVO |
| `compose_launch` admite o ramo "inseparável" | `app/actions/daemon_actions.py:205+220-235` | PROVADO NO CÓDIGO |
| Probe exige os 3 features (`GET_REPORT` responde de `self._features`) | `uhid_gamepad.py:832+875-888` | PROVADO NO CÓDIGO |
| Install já cobre udev/modules por default; uninstall simétrico | `install.sh:12-16+515-545`, `uninstall.sh:319+338`, `assets/71-uhid.rules` | PROVADO NO CÓDIGO |
| Vpad uinput `0df2` sem hidraw mapeia certo no SDL | — (nunca testado) | **HIPÓTESE** (bloqueia parte do VPAD-04) |
| Blueprint **embutido** binda igual ao capturado | dump byte-idêntico conferido; bind com embutido nunca rodou | **HIPÓTESE** até a validação viva do VPAD-03 |

Invariante do projeto: **teste verde sem validação ao vivo NÃO fecha item.** A única
validação uhid-Edge existente (bfd51db) foi com blueprint **capturado do físico** — o
canônico embutido precisa de UMA validação viva própria antes do VPAD-07.

## O que a revisão adversarial REFUTOU (e este plano acata)

1. **REFUTADO — o dump sanitizado da feature 0x09 no scratchpad está corrompido.**
   Tem **21 bytes** (um `00` extra na área do MAC, deslocando a assinatura `08 25 00`
   dos offsets 7-9 para 8-10); o report real tem **20 bytes** (é o
   `DS_FEATURE_REPORT_PAIRING_INFO_SIZE=20` do `hid-playstation.c`). O valor sanitizado
   CORRETO, derivado ao vivo do físico, é:
   `0900000000000008250000000000000000000000` (20 B; bytes 7-9 = `08 25 00`; bytes
   1..6 e 10..15 zerados). **Regenerar antes de embutir.** Agravante: o comentário do
   arquivo no scratchpad contém o hex CRU com o MAC real do controle e do host —
   **esse comentário NÃO pode ir para o repo** (regra de anonimato). O descriptor
   (289 B) e os features 0x05/0x20 do scratchpad foram conferidos byte a byte com o
   físico e estão íntegros — só o 0x09 está corrompido.
2. **REFUTADO — o critério de aceite original do VPAD-04 pré-decidia shipar com
   validação negativa** ("se o mapping vier errado, documentar e manter"). Inaceitável:
   um vpad uinput `054c:0df2` version `0x3` **sem hidraw** não usa o driver HIDAPI PS5
   do SDL (é o hidraw que fez o uhid-Edge funcionar) e cai no matching
   evdev/gamecontrollerdb com um GUID que não existe no db (o Edge real é version
   `0x8111`; ver o comentário de `DEVICE_VERSION` em `uinput_gamepad.py:65-68`). Se o
   mapping vier errado E o `compose_launch` novo anunciar `IGNORE_DEVICES` no ramo
   degradado, o resultado é UM controle "descontrolado" — pior que o status quo. A
   decisão vira **condicional** (ver VPAD-04, plano B explícito).
3. **RESSALVA — "pré-requisito da frente udev" reformulado.** É verdade para a launch
   option (o SDL só enxerga VID/PID) e para uma regra udev ingênua (ATTR de VID/PID no
   próprio node). É **falso** para uma regra udev bem escrita: matching por
   **ancestralidade** (`SUBSYSTEMS=="usb"`/`"bluetooth"`, ou parent HID
   `DRIVERS=="playstation"`) **nunca** casa vpad nenhum, com qualquer PID — o vpad
   uinput vive em `/sys/devices/virtual/input` e o uhid sob
   `/sys/devices/virtual/misc/uhid`, sem ancestral USB/BT (o `BUS_USB` do CREATE2 é
   forjado, sem nó em `/sys/bus/usb`). O próprio repo já usa esse critério para não se
   auto-adotar (`_is_virtual_evdev` em `evdev_reader.py:43-59`; `_is_virtual_hidraw`
   em `backend_pydualsense.py:57-80`). Portanto: **a Fase A é obrigatória por causa da
   launch option LEGADA persistida (a mina em campo) e como defesa em profundidade —
   não porque a udev seria impossível sem ela.** A Fase B **herda a obrigação** de
   ancorar a regra na ancestralidade física, nunca em ATTRS de VID/PID soltos — o que
   também cobre o dono de um DualSense Edge FÍSICO real (`0df2`), que nenhuma dedup
   por VID/PID separa do vpad.

As demais ressalvas obrigatórias das duas revisões estão incorporadas nos itens e nas
seções abaixo — nenhuma ficou de fora.

## A solução (Fase A) — peça central + redes de segurança

**Peça central (VPAD-03): blueprint canônico embutido no pacote.** O vpad nasce
Edge/uhid **sempre**, já no boot, mesmo sem controle conectado. Consequências: o gate
`hidraw_path` some; EIO em BT deixa de existir como modo de falha; o perigo do
descriptor BT (`85 31`) morre por construção; o co-op herda via factory (com decisão
de produto explícita — ver VPAD-09). `capture_dualsense_blueprint` sai do caminho de
produção e vira ferramenta de diagnóstico. O MAC do report 0x09 já é sobrescrito por
`player_mac()` no `start()` (`uhid_gamepad.py:554-571`), então o dump com MACs zerados
é seguro e funcional.

**Redes de segurança** (com o VPAD-03, viram raridade — mas são o que impede o
retorno do veneno quando o uhid quebra de verdade):

- **VPAD-01** — promoção uinput→uhid no hotplug (reconnect_loop);
- **VPAD-02** — re-selecionar DualSense na GUI força a promoção (botão de força);
- **VPAD-04** — o fallback uinput NUNCA mais divide VID/PID com o físico;
- **VPAD-05** — fallback nunca silencioso (badge na GUI + doctor);
- **VPAD-06** — teste-invariante que teria pegado o bug antes do estudo de 117 agentes;
- **VPAD-08** — o modo FAKE não registra um Edge real no kernel (regressão nova que o
  VPAD-03 criaria — pega antes de nascer).

### Alternativas descartadas (e por quê)

- **Retry da captura no EIO**: janelas de ~5 s, intermitentes; `make_virtual_pad`
  roda no caminho do poll loop (o projeto já encolheu `UHID_BIND_TIMEOUT_S` de 2 s
  para 0,5 s exatamente por isso — `virtual_pad.py:37-45`). Retry bloquearia input.
- **Cache em disco da última captura boa**: mantém os 4 modos de falha + o caso
  primeira-execução-em-BT-sem-cache, e cachearia um descriptor BT torto.
- **Manter o fallback em `0ce6` "com aviso"**: aviso não desarma a mina — qualquer
  dedup por VID/PID esconderia o vpad junto.
- **Só consertar o fallback e cancelar a Fase B**: a launch option continuaria
  requisito colável (viola a regra de ouro) e continuaria quebrando o modo Nativo.
- **Promover a cada tick do poll loop**: churn com jogo aberto; as bordas certas são
  reconnect (VPAD-01) e re-seleção na GUI (VPAD-02).
- **Recriar sem cooldown no early-return**: com uhid persistentemente quebrado, cada
  apply de perfil do autoswitch derrubaria o vpad em loop no meio do jogo.

## O que esta frente NÃO conserta (com todas as letras)

- **(a) Modo Nativo/Sony com a launch option persistida = zero controles CONTINUA.**
  No Nativo não há vpad nenhum; a opção colada esconde o físico. Só a Fase B
  (dedup por udev + remoção/aviso da opção persistida no `localconfig.vdf`) conserta.
  **A limpeza da opção persistida da Sackboy precisa acontecer ANTES da validação
  humana (VPAD-07)** — senão o teste reproduz o bug e condena a frente errada.
- **(b) O 8BitDo "descontrolado" tem outra causa** e está fora desta frente (a dedup
  cirúrgica por udev na Fase B é o que o deixa em paz; o comportamento dele no co-op
  entra só como teste no VPAD-09).
- **(c) O "BT conectado sem input" nos modos Sony diretos** idem — fora desta frente.

## Regra de ouro (da Vitória) — como esta frente a honra

"Tudo tem que estar no install funcionando SEM FLAGS." Esta frente é **100% código**:

- O install.sh já copia por DEFAULT as regras canônicas `assets/[0-9][0-9]-*.rules`
  (inclui a `71-uhid.rules`) + modules-load (`uinput`, `uhid`); `--no-udev` é opt-out
  (`install.sh:12-16+515-545`). O uninstall remove a 71-uhid explicitamente
  (`uninstall.sh:319+338`) — simetria histórica respeitada.
- A regra é numerada **71 < 73**, então a TAG `uaccess` vira ACL de verdade
  (regra da `73-seat-late.rules`).
- Nenhum "cole isto"/"exporte aquilo" novo. O colar-launch-option continua existindo
  **até a Fase B** — eliminá-lo é assumidamente dela.
- GUI/daemon seguem **sudo-zero em runtime** (decisão do bfd51db): nada aqui pede
  senha em clique de botão.
- Detalhe cosmético a aproveitar: a descrição impressa pelo install para o prefixo
  `71-*` diz só "emulação Xbox360 via uinput" e hoje cobre dois arquivos (71-uinput e
  71-uhid) — corrigir o texto de passagem.

## Itens

### VPAD-03 — Blueprint canônico USB embutido (a peça central) — P0 — CLAUDE

**O que fazer.** Embutir em `integrations/uhid_gamepad.py` o blueprint canônico:
descriptor USB de 289 B + features 0x05 (41 B) / 0x09 (20 B) / 0x20 (64 B).
**ATENÇÃO à refutação nº 1**: o 0x09 do scratchpad está corrompido (21 B) — usar o
valor correto `0900000000000008250000000000000000000000` ou re-capturar do físico por
cabo com o script; e o comentário com hex cru (MACs reais) NÃO entra no repo.
`_try_uhid` passa a usar o canônico SEMPRE; remover o gate `hidraw_path` de
`virtual_pad.py:147-149` e o gate `resolve_hidraw_path` de `gamepad.py:251-252`
(**junto com o VPAD-08 e a ressalva do VPAD-01 — a remoção desses gates sem os dois é
regressão**); `capture_dualsense_blueprint` vira ferramenta de diagnóstico;
remover/ajustar o warning `uhid_blueprint_bt_descriptor` (morre por construção).
**Materialização obrigatória**: o dump sanitizado e o script de recaptura existem hoje
SÓ no scratchpad (`/tmp/claude-1000/...-8752b91c.../scratchpad/blueprint_canonico_usb.txt`
+ `capture_blueprint.py`), que **morre no reboot** — ambos entram no repo (constante
Python/asset + `scripts/` ou `tools/`) **no primeiro commit** da frente.
**Anotar no código** as limitações aceitas (ver seção "Limitações aceitas").

**Arquivos**: `src/hefesto_dualsense4unix/integrations/uhid_gamepad.py`,
`integrations/virtual_pad.py`, `daemon/subsystems/gamepad.py`,
`daemon/subsystems/coop.py`, `tests/unit/test_virtual_pad_factory.py`, script de
recaptura em `scripts/` ou `tools/`.

**Critério de aceite (verificável).**
- Unitário: `make_virtual_pad('dualsense')` com `hidraw_path=None` e uhid fake
  disponível devolve `backend=='uhid'` (hoje devolve uinput).
- Unitário do dump: descriptor de exatamente 289 B **sem** `b'\x85\x31'`; feature 0x09
  de **exatamente 20 B** com bytes 7-9 == `08 25 00` e bytes 1..6 e 10..15 zerados;
  0x05/0x20 com 41/64 B.
- **Ao vivo (obrigatório antes do VPAD-07)**: reiniciar o daemon com o controle
  DESCONECTADO e ver hidraw novo `054c:0df2` + `Registered DualSense controller` no
  dmesg — a validação viva PRÓPRIA do canônico (a do bfd51db foi com blueprint
  capturado, não vale para este item).

### VPAD-08 — Modo FAKE e backends sem hidraw não registram um Edge real — P0 — CLAUDE

**O que fazer.** Sem o gate de `virtual_pad.py:147-149`, o daemon FAKE
(`run.sh --fake`, usado em smoke NA MÁQUINA DELA) passaria a registrar um DualSense
Edge REAL no kernel, visível pela Steam — e o histórico do projeto inclui um smoke que
já matou o daemon dela. **Decisão tomada aqui**: o caminho fake/`IController` declara
explicitamente "sem uhid" — a factory ganha um parâmetro explícito (ex.:
`allow_uhid=False`) que o subsistema passa quando o backend ativo é o fake (o único
`def hidraw_path` do repo é do backend pydualsense — `backend_pydualsense.py:329`;
`FakeController`/`IController` não têm). **Entra no MESMO commit do VPAD-03.**

**Arquivos**: `integrations/virtual_pad.py`, `daemon/subsystems/gamepad.py`,
`daemon/subsystems/coop.py`, `tests/unit/test_virtual_pad_factory.py`.

**Critério de aceite.** Unitário: factory com `allow_uhid=False` devolve uinput mesmo
com uhid disponível. Ao vivo (ambiente de teste): `run.sh --fake` não cria NENHUM
hidraw `054c:0df2` (conferir `ls /sys/class/hidraw` antes/depois).

### VPAD-01 — Promoção uinput→uhid no hotplug (reconnect_loop) — P0 — CLAUDE

**O que fazer.** No bloco offline→online do `reconnect_loop`
(`connection.py:208-231`, após o publish de `CONTROLLER_CONNECTED`), chamar
`upgrade_primary_vpad_to_uhid(daemon)` sob `contextlib.suppress`, espelhando
`lifecycle.py:388-393`, serializado com `getattr(daemon, '_emu_lock',
contextlib.nullcontext())` (o lock existe — `lifecycle.py:220`).
**Ressalvas obrigatórias incorporadas**:
- `reconnect_loop` e `_poll_loop` são tasks do MESMO event loop
  (`lifecycle.py:340+414-415`) e o upgrade é síncrono (pior caso ~0,5 s no
  `UHID_BIND_TIMEOUT_S`) — **envolver em `_run_blocking`** ou justificar o bloqueio
  por escrito no código;
- com o gate `resolve_hidraw_path` removido pelo VPAD-03, o upgrade ganha **precheck
  `uhid_available()`** e **compartilha o cooldown do VPAD-02** — senão, com uhid
  persistentemente quebrado (permissão de `/dev/uhid`, kernel sem `hid_playstation`),
  CADA reconexão BT (frequente nesta máquina) destruiria e recriaria o vpad uinput no
  meio do jogo (input drop em loop).
O no-op quando o vpad já é uhid (isinstance, `gamepad.py:246-248`) garante zero churn
nas reconexões normais — com o VPAD-03, este item vira raridade de recuperação.

**Arquivos**: `daemon/connection.py`, `daemon/subsystems/gamepad.py`,
`tests/unit/test_daemon_reconnect_loop.py`, `tests/unit/test_vpad_upgrade_para_uhid.py`.

**Critério de aceite.** Unitário: transição offline→online invoca o upgrade exatamente
1x por transição (0x quando já conectado no boot ou seguindo offline); com
`uhid_available()==False` o upgrade NÃO faz stop+start. Ao vivo: subir o daemon SEM
controle, plugar depois, e nunca mais ver `uinput_device_created flavor=dualsense
product=0xce6` no journal após hotplug.

> **NOTA DE RESOLUÇÃO (2026-07-16, pós-revisão adversarial da Fase 1).** Este item
> conflitava com o **BT-04(c)** do doc irmão (`2026-07-16-sprint-bluetooth-vpad-mudo.md`),
> que mandava "aposentar/simplificar `upgrade_primary_vpad_to_uhid` EM VEZ DE adicionar
> call site no reconnect_loop". Decisão registrada nos dois docs: **o VPAD-01 vence** —
> o call site existe (`daemon/connection.py`, bloco offline→online) como rede de
> segurança, com precheck `uhid_available()` e cooldown compartilhado com o VPAD-02. A
> premissa do BT-04(c) ("disponibilidade do uhid é estática") não vale: a ACL do
> `/dev/uhid` pode ser aplicada DEPOIS do boot do daemon (primeira sessão pós-install),
> e a borda de conexão é o único gatilho automático de recuperação desse cenário.
> Complemento anti-churn: o latch do BT-04(b) foi implementado por ORIGEM —
> `origin='profile'` nunca promove por apply idêntico (só gesto manual da usuária), então
> autoswitch/perfil flapando não recriam o vpad degradado em loop.

### VPAD-02 — Early-return por (flavor, backend): a GUI ganha botão de força — P0 — CLAUDE

**O que fazer.** Em `start_gamepad_emulation` (`gamepad.py:295-298`): se
`key=='dualsense'`, `existing.backend=='uinput'` e `uhid_available()`, recriar
(stop `persist=False release_grab=False` + start) em vez de retornar True. Cooldown de
30 s (ex.: `daemon._last_rebackend_ts`, **compartilhado com o VPAD-01**) para o caso
uhid persistentemente quebrado. Backend já uhid ou flavor xbox continuam no-op.
**Ressalva obrigatória**: o no-op por cooldown NÃO pode ser silencioso para a usuária
— o segundo clique dentro dos 30 s devolve True e a GUI mostraria sucesso sem nada
acontecer ("cliquei e nada", queixa clássica). Logar o motivo
(`rebackend_suprimido_por_cooldown`) e manter o badge de degradado do VPAD-05 visível.

**Arquivos**: `daemon/subsystems/gamepad.py`, `tests/unit/test_vpad_backend_wiring.py`.

**Critério de aceite.** Unitários: (1) dualsense+uinput+uhid disponível → stop+start;
(2) backend uhid → True sem stop; (3) flavor xbox → no-op; (4) segunda tentativa
dentro do cooldown → no-op COM log + badge mantido. Ao vivo: com vpad degradado,
re-selecionar DualSense na aba Início troca o backend
(`state_full` → `gamepad_emulation.backend=='uhid'`, exposto em
`ipc_handlers.py:411-428`).

### VPAD-04 — Fallback uinput vira Edge `054c:0df2` (PID já; launch option condicional) — P0 — CLAUDE

**O que fazer (parte incondicional, P0 — necessária para o VPAD-06).** Em
`uinput_gamepad.py`, `FLAVORS['dualsense']` passa a product=`0x0DF2` e nome
"Sony Interactive Entertainment DualSense Edge Wireless Controller", mantendo
`DEVICE_VERSION`. **Ressalvas obrigatórias**:
- mudar **SOMENTE** `FLAVORS['dualsense']['product']` — as constantes
  `DUALSENSE_PRODUCT`/`DUALSENSE_VENDOR` (`0ce6`) identificam o controle FÍSICO em
  `uhid_gamepad._is_dualsense` (linha 316), `evdev_reader.py:26-27` e
  `backend_pydualsense` (via `DUALSENSE_PIDS`) e **não podem ser tocadas**;
- `DUALSENSE_PIDS = {0x0CE6, 0x0DF2}` já trata `0df2` como PID de físico: a única
  proteção contra o daemon adotar o próprio vpad uinput-0df2 é o filtro de
  ancestralidade `_is_virtual_evdev` (`evdev_reader.py:119-120`) — **travar com teste
  que `discover_dualsense_evdevs` e `_enumerate_device_keys` NÃO adotam o vpad 0df2**
  (é o feedback loop que o projeto já sofreu no UHID-02);
- atualizar o comentário-invariante de `uhid_gamepad.py:96-110`.

**Parte CONDICIONAL (refutação nº 2 acatada).** A mudança do `compose_launch`
(`daemon_actions.py:208-235`) para o ramo dualsense+uinput anunciar
`IGNORE_DEVICES=0x054c/0x0ce6` **só entra se a validação SDL ao vivo passar**: vpad
evdev `054c:0df2` sem hidraw reconhecido com inputs corretos num jogo SDL2 (GUID novo:
version `0x3` ≠ `0x8111` do Edge real, sem entrada no gamecontrollerdb, sem HIDAPI —
**HIPÓTESE não validada**). **Plano B, por escrito**: se o mapping vier errado, o PID
`0df2` FICA (pelo invariante VPAD-06 e pela launch option legada, que ao menos não
esconde mais o vpad), mas o ramo degradado do `compose_launch` **mantém a dica honesta
atual SEM `IGNORE_DEVICES`** (`daemon_actions.py:229-235`) — shipar `IGNORE_DEVICES`
com mapping errado = um único controle "descontrolado", pior que o status quo. Nota:
o dono de um DualSense Edge físico real passa a dividir VID/PID com o vpad — só a
regra udev por ancestralidade (Fase B) cobre esse caso.

**Arquivos**: `integrations/uinput_gamepad.py`, `app/actions/daemon_actions.py`,
`integrations/uhid_gamepad.py`, `core/evdev_reader.py` (só testes),
`tests/unit/test_vpad_backend_wiring.py`.

**Critério de aceite.** Unitários: `UinputGamepad.for_flavor('dualsense').product ==
0x0DF2`; discover/enumerate não adotam o vpad 0df2. Condicional: `compose_launch`
('dualsense','uinput') só passa a conter `IGNORE_DEVICES` (e sem
`PROTON_ENABLE_HIDRAW`) **depois** do teste SDL ao vivo positivo, documentado neste
doc; caso negativo, teste assertando a dica honesta sem `IGNORE_DEVICES`.

### VPAD-06 — Teste-invariante: flavor dualsense NUNCA expõe `054c:0ce6` — P0 — CLAUDE

**O que fazer.** Teste de regressão dedicado travando o invariante do estudo: nenhum
caminho da factory (uhid ok, uhid indisponível, start falhou, bind falhou,
`allow_uhid=False`) produz vpad com flavor 'dualsense' e product `0x0CE6` — o PID é
sempre `0x0DF2`, uhid E uinput. É o teste que teria pegado o bug da Vitória antes do
estudo de 117 agentes. **Sequenciamento (ressalva acatada)**: o invariante em TODOS os
ramos só vale com a parte incondicional do VPAD-04 aplicada — por isso o VPAD-04 (PID)
subiu para **P0 junto deste teste**; eles entram juntos ou o teste não passa.

**Arquivos**: `tests/unit/test_virtual_pad_factory.py`,
`tests/unit/test_vpad_backend_wiring.py`.

**Critério de aceite.** Teste parametrizado sobre todos os ramos de fallback da
factory assertando `product != 0x0CE6` quando flavor=='dualsense'; gate completo verde
**contando os skips** (regra dos 22 skips falsos: nenhum teste novo pode skipar em CI).

### VPAD-05 — Fallback nunca silencioso: badge na GUI + doctor — P1 — CLAUDE

**O que fazer.** Quando `start_gamepad_emulation` terminar com flavor=='dualsense' e
backend=='uinput': `store.bump('gamepad.uhid.fallback')` (`state_store.py:100`) +
aviso visível na GUI (aba Início/Sistema — `state_full` já expõe
`gamepad_emulation.backend`) do tipo "Vibração e anti-duplicação degradadas —
reconecte o controle ou re-selecione DualSense". O mesmo badge cobre o no-op por
cooldown do VPAD-02. `doctor.sh`: check que consulta o `state_full` e reprova
dualsense+uinput com dica de reparo (regra do projeto: o doctor verifica o que o
install põe/o daemon promete). Nada de env var/flag — só leitura de estado existente.
**Armadilha COSMIC**: o aviso deve ser banner/label estático, nunca
popover/dropdown (cosmic-comp fecha popups — bug conhecido do compositor).

**Arquivos**: `daemon/subsystems/gamepad.py`, `app/` (aba Início/Sistema),
`scripts/doctor.sh`, testes.

**Critério de aceite.** Unitário do bump no caminho de fallback; ao vivo: forçar o
fallback (`chmod 000 /dev/uhid` **num ambiente de teste, NÃO na máquina dela**) e ver
o badge na GUI e o doctor apontando "vpad degradado" com instrução de recuperação.

### VPAD-09 — Co-op com controles não-DualSense: decisão anunciada + teste com o 8BitDo — P1 — AMBOS

**O que fazer.** Mudança de comportamento que o VPAD-03 causa e que a revisão exigiu
tornar explícita: hoje `_hidraw_for` devolve `None` para jogadores com controle
não-DualSense (8BitDo SN30 Pro, Nintendo Pro — os controles reais da casa;
`coop.py:395-420`) → vpad uinput. Com o canônico, cada jogador desses passa a ganhar
um vpad **uhid DualSense Edge** real no kernel. **Decisão de produto, tomada às
claras: SIM, desejado** — uniformidade, dedup segura e rumble via hidraw para todos os
players; e os prompts PS para quem segura layout Nintendo/Xbox **não são novidade
deste sprint** (o vpad uinput `0ce6` com máscara DualSense já fazia isso) — a novidade
é só backend/PID. O que precisa ser provado é que não regride: MAC próprio por jogador
(`02:fe:00:00:00:0N` — probe falha com MAC duplicado), sem feedback loop de adoção.

**Arquivos**: `daemon/subsystems/coop.py` (conferir herança via factory sem mudança de
assinatura), testes de co-op, validação ao vivo.

**Critério de aceite.** Unitário: promoção de jogador com identidade sem hidraw produz
vpad uhid com `player` correto e MAC distinto. Ao vivo (hardware disponível AGORA):
co-op com o 8BitDo por cabo como P2 → vpad Edge sobe, inputs do 8BitDo fluem pelo
vpad, `dmesg` sem `probe failed -17`, e o daemon não adota o vpad como físico.

### VPAD-07 — Validação humana: BT + hotplug + layout PS com o vpad sempre-Edge — P0 — VITORIA_HUMANO

**Pré-condições (obrigatórias, nesta ordem):** (1) validação viva própria do canônico
(critério do VPAD-03) já feita; (2) **a launch option persistida da Sackboy foi
removida/limpa do `localconfig.vdf`** — item da Fase B que precisa ser puxado para
ANTES deste teste, senão o cenário Nativo reproduz o zero-controles e condena a frente
errada.

**Roteiro.** (1) Ligar o DualSense por BT DEPOIS do daemon e conferir na aba Início
backend=uhid (hotplug promovido); (2) jogar Sackboy por BT com máscara DualSense:
prompts PS + inputs + vibração + sem controle duplicado; (3) repetir com o controle
por cabo plugado no MEIO do jogo (hotplug quente); (4) se houver fôlego, cena co-op
com o 8BitDo por cabo (VPAD-09).

**Armadilha conhecida no meio do caminho**: o autoswitch desliga a emulação quando a
janela vira "unknown" (limite XWayland/COSMIC — medido no estudo às 13:07:18; fix é
histerese em `profiles/autoswitch.py:69-74`, frente separada). Se os inputs morrerem
no meio, conferir o perfil ativo ANTES de culpar esta frente.

**Critério de aceite.** Relato dela: nas três cenas, zero "controle conectado sem
input" e zero duplicação, com journal SEM nenhuma ocorrência de
`uinput_device_created flavor=dualsense product=0xce6`.

## Ordem

VPAD-03 + VPAD-08 (mesmo commit; a peça central sem o guard do fake é regressão) →
VPAD-04 (parte PID) + VPAD-06 (entram juntos; o invariante depende do PID) →
VPAD-01 → VPAD-02 → VPAD-05 → VPAD-09 → validação viva do canônico (critério do
VPAD-03) → **limpeza da launch option persistida (item puxado da Fase B)** → VPAD-07.
A parte condicional do VPAD-04 (`compose_launch` com `IGNORE_DEVICES`) só depois do
teste SDL ao vivo — com plano B documentado se reprovar.

## Limitações aceitas do blueprint canônico (anotar NO CÓDIGO)

- **Congela a calibração (0x05) de UMA unidade e o firmware (0x20 = "Jul 4 2025",
  ver `0x0630`)** — e o firmware decide `use_vibration_v2` no driver
  (`uhid_gamepad.py:126-139`; limiar `0x0215`). Inócuo hoje: o vpad emite motion
  neutro e as duas unidades da máquina são `0x0630`. **Se um dia houver passthrough de
  gyro/touchpad, a calibração por unidade volta a importar** — o comentário no código
  deve dizer isso.
- **O par (kernel `hid_playstation`, blueprint congelado) vira a matriz de
  compatibilidade**: um kernel futuro que exija um feature novo no probe derruba o
  bind e cai no fallback — que o VPAD-05 torna visível (é por isso que o badge não é
  opcional).
- O vpad continua `BUS_USB` emitindo report 0x01 de 64 B independente do transporte
  do físico — por design (o descriptor BT com `85 31` é impróprio por construção).

## Armadilhas conhecidas que esta frente atravessa

- **MAC próprio por vpad** (`02:fe:00:00:00:0N`, bytes 1..6 do report 0x09 em LE):
  MAC duplicado = `probe failed -17`. O canônico com MAC zerado é seguro porque o
  `start()` sobrescreve (`uhid_gamepad.py:554-571`).
- **valid_flag do rumble é máscara `0x03`, nunca só `0x01`** (firmware >= `0x0215`
  usa `COMPATIBLE_VIBRATION2`) — não tocar nesse invariante ao mexer no uhid_gamepad.
- **`_INPUT_PAYLOAD_SIZE = 63`** (64 com o report ID): o driver descarta calado
  tamanhos errados.
- **udev numerada < 73** para `uaccess` virar ACL (a 71-uhid.rules já cumpre); nós em
  `SUBSYSTEM=="misc"` precisam de `udevadm trigger --subsystem-match=misc` — o
  install já faz.
- **Sudo-zero na GUI**: nenhum item desta frente pede sudo em runtime; qualquer
  necessidade root é do install (que já cobre tudo).
- **Dropdowns/popovers quebram no COSMIC** (cosmic-epoch#2497 + NVIDIA): o badge do
  VPAD-05 tem de ser estático.
- **GIL/throttling**: o upgrade é síncrono no MESMO event loop do poll loop e do IPC
  (pior caso ~0,5 s) — daí o `_run_blocking`/precheck do VPAD-01; nada desta frente
  pode adicionar espera bloqueante no caminho do input.
- **Gate "verde" com skips falsos**: já escondeu 1 vermelho — todo critério de aceite
  aqui exige contagem de skips dos testes novos.
- **Anonimato**: o dump entra SANITIZADO (MACs zerados); o hex cru do scratchpad
  (contém o MAC do controle e do host) não pode aparecer em nenhum commit.

## Referências

- Estudo 1 (117 agentes, 2026-07-16) — EIO intermitente medido, launch option
  persistida, descriptors USB/BT reais.
- `2026-07-15-sprint-uhid-dualsense-de-verdade.md` — PoC uhid, os 5 bugs que só o
  hardware pegou, `UHID_BIND_TIMEOUT_S`.
- `2026-07-16-sprint-edge-dedup-e-fechamento.md` — UHID-04 (vpad Edge via captura),
  compose_launch, §BT com o risco do descriptor.
- Insumos da implementação (materializar no repo no 1º commit — hoje só no
  scratchpad, que morre no reboot): `blueprint_canonico_usb.txt` (com o 0x09
  REGENERADO — o atual está corrompido) + `capture_blueprint.py`.
- Kernel: `drivers/hid/hid-playstation.c` (`DS_FEATURE_REPORT_PAIRING_INFO_SIZE=20`,
  `dualsense_get_mac_address`, `use_vibration_v2`), `linux/uhid.h`.
