# 2026-07-16 — ÍNDICE da onda: multi-controle & desduplicação sem launch option

> **Como este documento nasceu.** O Estudo 1 (117 agentes) mediu ao vivo, nesta máquina, a cadeia
> inteira do bug "em Bluetooth nada funciona". Em cima dele foram escritos **8 sprints (50 itens,
> 29 P0)**, e cada frente passou por **2–3 revisores adversariais independentes** que re-executaram
> as medições e re-abriram cada `file:line` citado. Este índice é o mapa da onda: a causa-raiz em
> linguagem direta, o veredito central, a ordem de execução, o que só a Vitória pode validar e —
> igualmente importante — **as ideias que os revisores mataram**, para ninguém reconstruí-las.

---

## 1. Por que em Bluetooth nada funciona (leia isto primeiro)

A cadeia tem três elos. Todos provados ao vivo nesta máquina.

**Elo 1 — o vpad nasce lendo o controle físico.** O gamepad virtual (vpad) via `/dev/uhid`
precisa ler três blocos do DualSense físico na hora de nascer (calibração `0x05`, MAC `0x09`,
firmware `0x20`). Por cabo, essa leitura responde sempre. Por Bluetooth, com o controle ocioso, o
firmware dele simplesmente **para de responder**: cada leitura estoura o timeout de 5 s do kernel
com `EIO`, e a janela dura **minutos** (medimos episódios de ~20 min contínuos), com o BlueZ
jurando `Connected: yes` o tempo todo. Detalhe medido: é o **controle** que emudece (gyro por BT =
0 eventos em 8 s; o gêmeo USB ocioso ao lado = 10.502 eventos), não o link que cai — o ACL segue
em modo ativo, sem sniff.

**Elo 2 — quando a leitura falha, o vpad vira um clone do físico.** Blueprint ilegível → o vpad
cai **em silêncio** (nada na GUI; só warnings no journal) para o plano B: uinput apresentando
`054c:0ce6` — o MESMO VID/PID do DualSense físico. Dois agravantes de código: ligar o controle
DEPOIS do daemon deixa o vpad no plano B para sempre (`upgrade_primary_vpad_to_uhid` só roda no
boot — `lifecycle.py:388-393` é o único call site; o `reconnect_loop` em `connection.py:208-231`
não promove), e re-selecionar "DualSense" na GUI é no-op (o early-return em `gamepad.py:296-298`
compara só o flavor — os dois backends respondem `dualsense`).

**Elo 3 — a launch option esconde tudo.** A
`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` persistida na Steam (localconfig.vdf, linha
914, appid do Sackboy) manda o jogo ignorar tudo que for `054c:0ce6`. Com o vpad degradado, ela
esconde o físico **e** o vpad → **jogo com zero controles**. No modo Nativo/Sony não existe vpad
nenhum: ela esconde o físico → zero controles do mesmo jeito. Por cabo tudo funciona porque a
leitura nunca falha: o vpad sobe como Edge `054c:0df2`, que a option não toca.

**A parte honesta.** A cadeia acima explica o **Sackboy** — o único appid com o veneno
persistido. O RDR2 por BT falhou **sem launch option nenhuma** (conferido: appid 1174180 sem
entry no vdf) — existe uma **segunda causa em aberto**. O candidato mais forte que os revisores
acharam: com o gêmeo USB de mesmo VID/PID rastreado pelo HIDAPI, o DualSense **BT fica invisível
ao SDL por inteiro** (o backend evdev deferencia ao HIDAPI por VID/PID) — somado ao emudecimento
do BT ocioso. Por isso a validação humana (BT-07) é **investigação**, não formalidade: os sprints
prometem "cura da cadeia provada", nunca "cura do BT".

Dois bugs irmãos que contaminavam o quadro:

- **Autoswitch** — quando a janela vira `unknown` (limite XWayland/COSMIC), o autoswitch caía no
  perfil padrão (MatchAny, mode=null) e **desligava a emulação no meio do jogo** (medido
  13:07:18). Cura: histerese (leitura sem informação não troca perfil) + gate de foco X
  (`get_input_focus` mata a leitura rançosa de `_NET_ACTIVE_WINDOW`, provada ao vivo).
- **8BitDo SN30 Pro** — o hefesto está **fora da cadeia causal** (filtro Sony-only no código;
  morte por BT provada até sem Steam rodando: boot 12:31, morte 12:38, Steam só às 12:46). É
  firmware clone × `hid-nintendo` do kernel, por Bluetooth. A saída é decisão humana de modo
  (cabo/X-input/Steam Input), não código nosso.

---

## 2. Veredito central: udev × consertar o fallback × os dois

**Os dois, em fases — com o desenho corrigido pelos revisores.**

1. **A regra udev, como desenhada em 2026-07-13, morreu como mecanismo central.**
   `ID_INPUT_JOYSTICK=0` só cega o caminho evdev do SDL; o caminho **HIDAPI** (default do SDL
   para PS5, e que a máscara Edge mantém ligado de propósito via `PROTON_ENABLE_HIDRAW=1`)
   enumera `/dev/hidraw` direto e **ignora propriedades udev** — provado ao vivo por três
   revisões independentes. E cortar o acesso ao hidraw do físico cortaria o próprio daemon
   (mesmo uid dos jogos), o que exigiria broker root — fora do sudo-zero.
2. **Só consertar o fallback também não fecha.** Mesmo com o vpad sempre Edge, o modo Nativo
   (sem vpad) continua refém da option persistida, e "cole isto na Steam" continua violando a
   regra de ouro.
3. **O plano vencedor, em fases:**
   - **Fase A — VPAD SEMPRE EDGE** (sprint `vpad-sempre-edge`, peça central VPAD-03): blueprint
     canônico USB **embutido no código** (descriptor de 289 B + features reais; dump `0x09`
     REGENERADO — o do scratchpad está corrompido). O vpad nasce uhid/Edge `054c:0df2`
     **sempre** — em BT, em USB, até sem controle conectado — e nunca mais lê o físico ao
     nascer. O fallback uinput também vira `0df2` (condicionado à validação SDL do mapping);
     promoção no hotplug com latch anti-churn; early-return por `(flavor, backend)`; degradação
     sempre **visível** (badge + doctor). Código puro, zero artefato novo de install.
   - **Fase B — MATAR A DEPENDÊNCIA DA LAUNCH OPTION** (sprints `dedup-sem-launch-option` +
     partes de `bluetooth-vpad-mudo`/`autoswitch`): wrapper `hefesto-launch` (env dinâmica por
     appid; gate por `connect()` real no socket de produção + estado real do vpad por jogador;
     fail-safe: daemon morto → nenhuma env → físico visível → jogo sempre jogável) +
     **migração obrigatória** do veneno já persistido no vdf (Steam fechada, backup, só tokens
     nossos) + `compose_launch`/`doctor.sh` param de recomendar a option. **Toda remoção é
     gateada por prova ao vivo no caminho HIDAPI** (jogo real vê exatamente 1 controle com
     HIDAPI ligado) — nunca por "regra instalada".
   - A udev pode voltar como **coadjuvante** do caminho evdev — e, se voltar, ancorada em
     **ancestralidade de barramento** (`SUBSYSTEMS=="usb"`/`"bluetooth"`, como o próprio repo já
     faz em `_is_virtual_evdev`/`_is_virtual_hidraw`), nunca em ATTRS de VID/PID soltos. Assim
     ela é imune ao PID do vpad por construção e não respinga em nenhum outro controle.
4. **Honestidade sobre o estado final.** A launch option **não morre nesta onda por fé** — morre
   quando o substituto estiver provado ao vivo. Até lá, o pior caso pós-install passa a ser
   **controle duplicado, nunca zero controles** — e a GUI/doctor apontam esse estado. A morte
   total do "esconder sem env" (broker root ou daemon com uid próprio) fica registrada como
   limitação, decisão de outra onda.

---

## 3. Os 8 sprints da onda

| Ordem | Sprint (arquivo em `docs/process/sprints/`) | Itens | P0 | Em uma linha |
|-------|---------------------------------------------|-------|----|--------------|
| 1 | `2026-07-16-sprint-vpad-sempre-edge.md` | 9 | 7 | Blueprint canônico embutido: o vpad nasce Edge `054c:0df2` sempre (até sem controle), 4 redes de segurança, teste-invariante, fallback nunca silencioso. |
| 2 | `2026-07-16-sprint-autoswitch-e-launch-options.md` | 7 | 3 | Histerese + gate de foco X curam o drop da emulação no meio do jogo; extinção da option gateada por prova HIDAPI; NÃO fundamentado ao popup automático. |
| 3 | `2026-07-16-sprint-dedup-sem-launch-option.md` | 6 | 6 | Wrapper `hefesto-launch` fail-safe (gate IPC real) + migração do veneno no vdf — mata o "zero controles" por construção no momento do launch. |
| 4 | `2026-07-16-sprint-bluetooth-vpad-mudo.md` | 6 | 3 | O que resta do BT pós-Fase A: coerência doctor/compose, desenvenenamento gateado e a investigação da segunda causa (RDR2); BT-07 é o gate humano. |
| 5 | `2026-07-16-sprint-perfis-por-controle.md` | 6 | 4 | Fundação por-controle: `_desired` por-uniq com merge por campo, mapa `controllers` no perfil, `origin` na ativação e autoload do perfil 'vitoria'. |
| 6 | `2026-07-16-sprint-cores-e-led-automaticos.md` | 8 | 3 | Cor automática estilo PS5 + LED do número por DualSense via registro MAC→slot de sessão, aplicado no reconcile de hotplug do backend. |
| 7 | `2026-07-16-sprint-status-por-controle-e-cores.md` | 6 | 3 | Aba Status vira 1 card por DualSense com inputs tintados na cor real do lightbar (contraste ≥ 3.0, cor segue o dono da escrita, priming do sysfs). |
| 8 | `2026-07-16-sprint-8bitdo-e-outros-controles.md` | 6 | 0 | O hefesto está fora da cadeia causal do 8BitDo: decisão humana de modo destrava, doctor gateado no journal, aba read-only fundida com multi-controle. |

Total: **50 itens, 29 P0.**

---

## 4. Ordem de execução e por quê

1. **`vpad-sempre-edge` (Fase A)** — primeiro porque é código puro, pequeno, e é o
   pré-requisito para conviver com a launch option **legada** persistida (qualquer dedup por
   VID/PID explode enquanto o vpad puder ser `0ce6`). Cura o nascimento degradado em BT, o boot
   sem controle e o hotplug. Atenção: **regenerar o dump `0x09`** antes de embutir (o do
   scratchpad tem 21 B — corrompido; o correto tem 20 B com `08 25 00` nos offsets 7–9) e nunca
   commitar o dump cru (MAC real = quebra de anonimato).
2. **`autoswitch-e-launch-options` (parte histerese + gate de foco)** — segundo porque é
   cirúrgico e é pré-condição de QUALQUER validação humana confiável: sem ele, o drop da
   emulação no meio do jogo contamina o teste e condena a frente errada. Os itens de launch
   option deste sprint se subordinam ao dono único da frente DEDUP (ver §5).
3. **`dedup-sem-launch-option` (Fase B)** — wrapper + migração do vdf. É o pacote que destrava o
   modo Nativo do Sackboy dela (a migração remove a string velha) sem regredir o único cenário
   hoje perfeito (USB + máscara Xbox). Depende da Fase A.
4. **`bluetooth-vpad-mudo`** — o que sobra pós-Fase A: coerência interna (doctor.sh:387 e
   `compose_launch` param de recomendar o veneno), desenvenenamento automático gateado, e a
   **investigação da segunda causa** (RDR2 + nativo + BT). O BT-07 (validação humana, matriz
   USB/BT × máscaras) é o **gate de entrega** da metade dedup/BT da onda.
5. **`perfis-por-controle`** — fundação `_desired` por-uniq (4P-01) + mapa no perfil + autoload
   do 'vitoria'. É a fundação técnica das duas frentes visuais seguintes (o STATUS-06 foi
   movido para cá; a frente COR consome o desired por-controle). PERFIL-01/02/04 são unidade
   atômica de entrega (schema sem GUI perde dados no primeiro "Salvar Perfil").
6. **`cores-e-led-automaticos`** — consome a fundação da frente 5 (registro MAC→slot +
   aplicação no reconcile do backend). Entrega o pedido 3 dela (cor de coluna + LED do número).
7. **`status-por-controle-e-cores`** — consome a cor por controle das frentes 5/6 (sem elas os
   cards nascem todos da mesma cor — dependência declarada). Entrega o pedido 1 dela.
8. **`8bitdo-e-outros-controles`** — sem P0; a decisão de modo (8BIT-05) é da Vitória e pode
   acontecer **a qualquer momento, em paralelo, com custo zero de código**. O restante (doctor
   gateado, aba read-only) é P1/P2 fundido com a frente multi-controle.

---

## 5. Coordenação entre frentes — donos únicos (para não implementar duas vezes)

Vários sprints nasceram de investigações paralelas e convergiram nos mesmos mecanismos. Cada
mecanismo tem **um dono**; os demais sprints **referenciam**, não re-implementam:

| Mecanismo | Dono | Referências cruzadas |
|-----------|------|----------------------|
| Blueprint canônico embutido (vpad nasce Edge) | VPAD-03 (`vpad-sempre-edge`) | BT-01 |
| Fallback uinput vira `054c:0df2` | VPAD-04 | BT-02 |
| Desenvenenamento do vdf (migração + strip de tokens nossos) | DEDUP-05 (`dedup-sem-launch-option`) | BT-06, UX-04 |
| Desenvenenamento no **uninstall** (incondicional — sem hefesto não há vpad; a option órfã = zero controles para sempre) | uninstall.sh, junto do DEDUP-05 | — |
| `_desired` por-uniq no backend | PERFIL-01 (`perfis-por-controle`) | COR-02, STATUS-06 (movido) |
| Superfície de backend degradado na GUI | Reforma da aba Status (pedido 1) | UX-03, BT-03, VPAD-05 |
| Aba de controles externos (read-only) | Frente multi-controle | 8BIT-01/02 (fundidos) |
| Remoção da recomendação do veneno em `doctor.sh:387` e `compose_launch` | Uma única mudança, no sprint DEDUP/BT que chegar primeiro | UX-05 |

Regras transversais que valem para TODOS os itens:

- **Regra de ouro** (§8): tudo default no install sem flags; uninstall simétrico; sudo-zero em
  runtime; doctor verifica o que o install põe.
- Paths de teste corretos: `tests/unit/…` (não `tests/` na raiz).
- Nenhum caminho novo de escrita de LED pode contornar o gate `output_mute` do Modo Nativo.
- Nenhum item pode ancorar em `notify_controller_connected`/`CONTROLLER_CONNECTED` para lógica
  por-controle: esses só disparam na transição offline→online do backend INTEIRO.

---

## 6. O que só a Vitória pode fazer (validação humana)

1. **Gameplay com a máscara DualSense (layout PS)** — sentir rumble + conferir botões num jogo
   real. É a pendência que já segura o release da onda Harmonia.
2. **Matriz BT pós-fix (BT-07 / VPAD-07 / DEDUP-02)** — Sackboy e RDR2 por Bluetooth, nas
   máscaras DualSense E Xbox (célula de controle), incluindo **gyro e touchpad** (as features do
   vpad agora vêm de template). É a investigação da segunda causa do RDR2 — só o teste dela
   revela. Pré-condição: limpar a option persistida do Sackboy ANTES de testar o modo Nativo,
   senão o teste reprova a frente errada.
3. **Decisão do 8BitDo (8BIT-05)** — cabo em modo Switch (provadamente estável) × X-input no
   power-on (só por cabo vira Xbox de verdade; por BT nunca foi testado; mata o gyro) × Steam
   Input off. O trade-off estabilidade × gyro é dela. Custo zero de código, pode fazer hoje.
4. **Cores e LED (frente COR)** — validar cores distintas por controle, LED do número, replug
   mantendo o slot; e o comportamento de "Todos" × automático.
5. **Aba Status (STATUS-05)** — aceitar (ou vetar) o compromisso visual: o swatch mostra a cor
   crua, os traços dos inputs são clareados para dar contraste — NÃO será literalmente "a mesma
   cor" quando o lightbar estiver escuro (a cor atual dela, 16/32/72, tem contraste 1.12:1 —
   invisível crua).
6. **Perfis (PERFIL-05)** — ativar 'vitoria' manualmente UMA vez após o fix (seed do restore);
   validar que o override por-controle sobrevive a replug; aceitar que o autoswitch continua
   trocando perfil por janela por cima do autoload (ou pedir a decisão de produto que o
   suprime).
7. **OKs de produto explícitos** — (a) o NÃO fundamentado ao popup automático do pedido 5 (a
   extinção da launch option atende o espírito: zero colagem); (b) UX-06 (GUI como janela
   neutra no autoswitch) e a retenção de perfil que vem junto; (c) controles externos read-only
   na aba multi-controle.
8. **Ações físicas de Bluetooth** — re-parear o controle (remove+pair+trust+PS) se o SDP HID
   sumir; tocar no controle para acordá-lo durante testes de janela de EIO.

---

## 7. Ideias mortas — refutadas pelos revisores adversariais (NÃO reconstruir)

Cada item abaixo foi derrubado com prova ao vivo ou de código. Se alguém propuser de novo, apontar
para cá.

1. **"Regra udev `ID_INPUT_JOYSTICK=0` desduplica sozinha."** MORTA. O SDL/winebus enxergam o
   DualSense físico pelo HIDAPI (`/dev/hidraw` direto), que ignora propriedades udev — provado
   ao vivo (enumeração com `path=/dev/hidraw2`). A regra só cega o caminho evdev. Nunca remover
   a launch option com base em "regra instalada"; só com prova ao vivo no caminho HIDAPI.
2. **"Retry com backoff (~8 s) conserta o blueprint em BT."** MORTO como fix principal. A janela
   de EIO não é de ~5 s: foi medida **persistente por minutos** (2/2 sondas diretas e 4/4
   enumerações SDL falharam no mesmo nó). Retry de ≤8 s falharia em 100% das amostras. O caminho
   default é o blueprint canônico; retry+cache são otimização (cache só salva controle já visto).
3. **"Gate do wrapper = o socket IPC existe."** MORTO. Socket UNIX sobrevive a crash (o próprio
   `ipc_server` remove socket stale no startup — e havia um `daemon.pid` órfão + socket fake
   ACEITANDO conexão na máquina durante a revisão); e daemon vivo com vpad degradado passaria no
   gate. Gate correto: `connect()`+ping no socket de PRODUÇÃO por nome exato + estado real do
   backend por jogador.
4. **"Prepend preservando o LaunchOptions existente."** MORTO como escrito. Preservaria o próprio
   veneno já persistido (linha 914). Migração obrigatória: remover as strings NOSSAS conhecidas
   antes do prepend; "não clobberar" vale para opções do usuário, não para nosso legado. E o
   wrapper TEM que terminar em `exec env "$@"` — senão `VAR=VAL %command%` vira argumento
   não-executável e o jogo não abre.
5. **"O wrapper roda dentro do pressure-vessel do Proton."** MORTO. Launch options embrulham o
   `%command%` inteiro (que inclui o entry point do SLR) e executam no **HOST**, antes do
   container — é assim que a env colada de hoje já chega ao jogo. Testar "dentro de bwrap"
   valida um cenário que não existe. O risco real: helpers do host herdam
   `LD_LIBRARY_PATH`/`LD_PRELOAD` do Steam Runtime — sanitizar ao invocar, preservar no exec.
6. **"Esqueleto de broker root (DEDUP-07) como item de sprint."** MORTO. Contraria o sudo-zero
   (decisão bfd51db) e o escopo mínimo dela. Vira um parágrafo de limitação no doc.
7. **"Banner de vpad degradado dizendo 'reconecte o controle'."** MORTO. Reconectar não promove
   (a promoção só roda no boot) e re-selecionar máscara é no-op — o conselho é ineficaz e
   reforçaria o "hefesto não funciona". Texto honesto ("reinicie o Hefesto") ou entra junto com
   o fix da promoção no hotplug.
8. **"Popup automático da launch option (pedido 5 literal)."** Respondido com um NÃO
   fundamentado: automatizaria a distribuição do veneno provado (zero controles quando o vpad
   degrada ou no Nativo). O espírito do pedido (zero colagem) é atendido pela extinção da
   option. Precisa do OK explícito dela.
9. **"Strip cego de `SDL_JOYSTICK_HIDAPI=0` / `PROTON_ENABLE_HIDRAW=1` em todos os appids."**
   MORTO. São variáveis legítimas (a máscara Xbox emite HIDAPI=0 de propósito; o
   PROTON_ENABLE_HIDRAW transporta o rumble do vpad Edge). Só remover tokens co-ocorrendo com a
   assinatura nossa (`IGNORE_DEVICES=0x054c/0x0ce6`) na MESMA linha. E o gate do strip é em
   **runtime dentro do script** — a unit do guard executa o script do working tree, então "só no
   mesmo release" não gateia nada.
10. **"Steam segurando o hidraw = conflito de dois mestres (8BitDo)."** MORTO como detector. O
    Steam segura o hidraw de TODO controle suportado — inclusive os DualSense saudáveis com
    PSSupport=0. O doctor gateia na assinatura real de morte no journal do kernel (cascata de
    `timeout waiting for input report` → `joycon_enforce_subcmd_rate`), via `journalctl -b -k`
    (funciona sem sudo, grupo adm) — senão vira alarme falso permanente.
11. **"X-input por BT vira Xbox 360 real via xpad."** MORTO. O xpad é USB-only (zero aliases
    hid). Por BT o modo X-input cai em hid-microsoft/hid-generic e NUNCA foi testado nesta
    máquina. Só o cabo garante `045e:028e`/xpad.
12. **"O hefesto interfere no 8BitDo."** MORTO. Morte por BT provada SEM Steam rodando e com o
    daemon real vivo mas filtrado (Sony-only em `evdev_reader.py:26-27`; zero referências a
    057e no src). É firmware clone × hid-nintendo. Nenhum código nosso conserta — e a frente
    inteira do 8BitDo tem zero P0.
13. **"Ancorar cor/lógica por-controle em `notify_controller_connected`."** MORTO. É notificação
    de desktop, disparada só na transição offline→online do backend INTEIRO — plugar o 2º
    controle não gera evento nenhum. O ponto certo é o reconcile de hotplug do backend
    (`_reapply_desired` / `_refresh_sysfs_leds`).
14. **"`default_profile` como chave nova em session.json."** MORTO como escrito.
    `save_last_profile` reescreve o arquivo inteiro (o próprio módulo documenta a armadilha) — a
    chave morreria na primeira ativação manual. Arquivo próprio ou read-modify-write.
15. **"Resolução do desired como `by_uniq.get(uniq) or default` (por objeto)."** MORTA. Override
    parcial (só triggers) apagaria a cor global no replug. Merge POR CAMPO + reset do mapa
    por-uniq a cada ativação de perfil (senão o override do perfil anterior ressuscita no
    hotplug sob outro perfil).
16. **"multi_intensity do sysfs = a verdade do hardware" / "0 0 0 = lightbar apagada."** MORTO.
    No probe o kernel zera as intensidades da classe LED e acende a lightbar de AZUL por fora
    dela — controle recém-conectado lê `0 0 0` com o LED aceso. Precisa de priming (o daemon
    escreve a cor vigente via sysfs em todo nó novo) e de "cor desconhecida" quando nunca
    escrevemos. E quando o nó não é gravável (escrita foi por hidraw), o valor lido está stale —
    a cor exibida segue o DONO da escrita.
17. **"Slot do registro MAC→slot alimenta direto o player_index do co-op."** MORTO como escrito.
    O player_index vira o MAC do vpad (`02:fe:00:00:00:0N`); colisão dá `-EEXIST` e derruba o
    jogador para uinput em silêncio — o caminho envenenado de novo. Separar slot de exibição/LED
    do índice de alocação do vpad. E o slot é numeração de SESSÃO (controle sozinho = slot 1),
    não identidade eterna.
18. **"Leitura de lightbar crua dentro de `describe_controllers()`."** MORTA. Esse método roda no
    caminho quente do FF do jogo (a cada evento de rumble). O enriquecimento mora no handler IPC
    ou em cache com TTL.
19. **"O critério de aceite 'a GUI mostra vitoria após reboot'."** MORTO como escrito: o
    autoswitch continua trocando perfil por janela depois do restore (contrato preservado). O
    aceite verifica session.json + log `last_profile_restored`; o que a aba mostra depende da
    janela focada.
20. **"Fail-safe por construção — nenhum estado do daemon volta a dar zero controles."**
    Overclaim corrigido: a env é congelada no spawn do jogo. A promessa vale para o MOMENTO do
    launch; degradação pós-launch é coberta pelo guard/histerese/banner. E o fail-safe troca
    "zero controles" por "controle duplicado" — o novo pior caso, que a GUI/doctor apontam.

---

## 8. Regra de ouro desta onda (ditada pela Vitória)

> "não queremos burocratizar a solução, mas tudo tem que tá no install funcionando SEM FLAGS."

- Tudo que a solução precisa (regra udev, drop-in, serviço, permissão) entra por DEFAULT no
  `install.sh`. Flag só existe como opt-out.
- `uninstall.sh` SIMÉTRICO — inclusive o desenvenenamento do vdf no uninstall (incondicional).
- Nada de "cole isto / rode aquilo / exporte tal variável" como requisito. Se só funciona quando
  ela cola algo, não está pronto — essa é exatamente a queixa que originou a onda.
- GUI/daemon seguem SUDO-ZERO em runtime (decisão bfd51db). Sudo só no install, com TTY.
- `doctor.sh` verifica tudo que o install põe (e para de recomendar o veneno na linha 387).

---

*Índice escrito em 2026-07-16, após as revisões adversariais das 7 frentes. Os sprints listados
já incorporam todas as refutações e ressalvas — este documento existe para que a memória do que
foi derrubado sobreviva à onda.*
