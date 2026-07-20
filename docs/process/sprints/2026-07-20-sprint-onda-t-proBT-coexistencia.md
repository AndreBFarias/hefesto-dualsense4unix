# Sprint Onda T — o que derruba o Pro Controller BT (coexistência WiFi×BT + muro do kernel)

> A mantenedora relatou (20/07): "ainda tem algo derrubando o BT do Pro Controller". Este sprint
> existe porque a **Onda S (broker) NÃO resolve isso** — o broker só tira o cliente Steam da
> guerra de escritores; o assassino do Pro BT é OUTRO. Evidência medida em
> `docs/process/estudos/2026-07-19-mapa-retomada-e-incidente-wifi-bt.md` e memória
> [[achado-incidente-wifi-bt-20260719]].

## As 3 camadas do problema (por ordem de força da evidência)

1. **[MEDIDO — mais forte] Dongle WiFi Archer T3U (rtw88_8822bu) derruba o BT.** No segundo em que
   associou ao AP (14:43:46), o Pro BT perdeu ~2700 IMU reports. Topologia fatal: BT TP-Link
   RTL8761BU em 3-1, WiFi em 3-2, DualSense em 3-3 — portas adjacentes do MESMO xHCI (0c:00.3).
   Mecanismos: EMI de USB3 SuperSpeed + disputa de banda no xHCI + varredura de fundo do
   NetworkManager em 2.4G. A banda NÃO é o mecanismo (a conexão é 5 GHz).
2. **[MEDIDO — muro do kernel] hid-nintendo BT desiste sozinho.** Assinatura: cascata
   `timeout waiting for input report` → `joycon_enforce_subcmd_rate: exceeded max attempts` →
   driver desregistra. Função hardcoded, ZERO parâmetro de módulo (modinfo). Morte provada SEM
   Steam e SEM código nosso na cadeia — basta o rádio degradar.
3. **[contribuinte, não assassino] Cliente Steam** escreve subcomandos no hidraw BT do Pro
   (uaccess do steam-devices cobre 057E:2009). O broker (Onda S) tira ESTE fator — mas sozinho
   não cura, porque 1 e 2 continuam.

## T0 —  CORREÇÃO DE UM ERRO DE DIAGNÓSTICO (20/07)

Uma versão anterior deste sprint afirmava que o dongle WiFi era NOVO (19/07) e recomendava
"voltar o cabo de rede". **As duas coisas estavam erradas** e foram removidas:
- O dongle está na máquina **desde ≥02/07** (341 registros no journal de todos os boots). O erro
  veio de usar `journalctl -k`, que **implica `-b`** (só o boot atual). Usar
  `journalctl _TRANSPORT=kernel` para histórico.
- "Voltar o cabo" foi **REJEITADO pela mantenedora como gambiarra**. A diretriz é ter WiFi bom E
  BT estável ao mesmo tempo, consertando na raiz (kernel/baixo nível liberados).

O trabalho de WiFi (incluindo o bug do fantasma USB do `rtw88`, que é de driver) foi movido para
o sprint próprio: **`2026-07-20-sprint-onda-w-wifi-raiz.md`**. Aqui ficam só as camadas do
Pro Controller.

## T1 — (movido) Coexistência WiFi×BT

Todo o trabalho de rádio WiFi (tunables do rtw88, bug do fantasma USB, coexistência medida e
driver alternativo) vive agora em `2026-07-20-sprint-onda-w-wifi-raiz.md`. O que importa AQUI: a
degradação de rádio é o GATILHO que faz o `hid-nintendo` desistir — por isso T2 (patch do driver)
é a cura de raiz do lado do controle, independente de quem degradou o rádio.

## T2 — CURA NA RAIZ: patch do kernel `hid-nintendo` (entrega por DKMS)

> **Decisão da mantenedora (20/07): "a ideia é arrumarmos o kernel na raiz pra tudo funcionar."**
> Não é contorno — é consertar o driver. Este é o item de maior valor da onda e o espírito do
> projeto: fazer o que as equipes de kernel/Nintendo/Sony/System76 deixaram por fazer.

### T2.1 — Pesquisa antes de escrever (obrigatória, materializar em estudo)
- Baixar o source do `hid-nintendo` da versão EXATA em uso (kernel 7.0.11-76070011-generic,
  Pop!_OS/System76) — `apt source linux` ou o repo do kernel do System76.
- Ler `joycon_enforce_subcmd_rate()` e o caminho do `timeout waiting for input report`
  (`joycon_hid_event`/`joycon_send_subcmd`/`joycon_wait_for_input_report`): quem espera, quanto
  espera, quantas tentativas, e **o que o driver faz ao estourar** (retorna erro? desregistra?).
- Checar o que JÁ existe upstream: linux-input mailing list, commits recentes em
  `drivers/hid/hid-nintendo.c`, e issues conhecidas de Pro Controller por BT. **Não reinventar** —
  se já houver patch upstream, portá-lo é melhor que escrever do zero.

### T2.2 — O patch (hipótese de design; confirmar contra o código real)
Alvo: sob rádio degradado, o driver não pode DESISTIR do controle; deve degradar e se recuperar.
1. **Tornar o esgotamento não-fatal**: em vez de abandonar/desregistrar ao exceder as tentativas,
   devolver `-EAGAIN`/reagendar com backoff, preservando o device registrado para quando o rádio
   voltar (é o comportamento que o usuário espera: o controle volta sozinho).
2. **Tolerância adaptativa por transporte**: BT tem latência e perda muito maiores que USB —
   parametrizar o timeout de espera do input report e o número de tentativas por `bus`
   (BT mais folgado). Hoje é hardcoded, igual para os dois.
3. **Module params** para os limiares (timeout ms, max attempts, backoff), para ajuste de campo
   SEM rebuild — hoje `modinfo hid_nintendo` mostra ZERO parâmetros (medido), o que impede
   qualquer tuning. Este item sozinho já destrava a investigação empírica.
4. Manter o comportamento atual como DEFAULT dos params (patch conservador: sem regressão para
   quem não ajusta).

### T2.3 — Entrega: DKMS (replicável por script, sobrevive a update de kernel)
> **Pré-requisitos JÁ CONFERIDOS na máquina (20/07): `dkms` instalado e
> `/usr/src/linux-headers-7.0.11-76070011-generic` presente.** Caminho livre — não re-verificar.
- Módulo out-of-tree `hid-nintendo` empacotado em **DKMS** (`/usr/src/hefesto-hid-nintendo-<ver>/`
  + `dkms.conf`), que substitui o in-tree via `modprobe` config. Regra do projeto: tudo replicável
  por script, então o build/instalação entra no `install.sh` (idempotente, com detecção de kernel
  headers e warn honesto se faltarem) e sai no `uninstall.sh` (simétrico: `dkms remove` + volta ao
  módulo in-tree).
- Segurança: se o DKMS falhar em qualquer kernel novo, o sistema cai no módulo in-tree (nunca
  ficar sem controle) — mesmo princípio fail-safe do wrapper.
- Doctor: check "hid-nintendo do hefesto ativo?" (`modinfo`/`/sys/module/hid_nintendo/parameters/`
  presentes = patch carregado) + versão.

### T2.4 — Validação e upstream
- A/B ao vivo: com o patch carregado, reproduzir a degradação (Pro BT + dongle WiFi ativo) e
  confirmar que o driver **não desregistra** — o controle reconecta sozinho quando o rádio volta.
- Medir a assinatura `[JOYCON]` antes/depois no kernel-watch.
- **Preparar o patch para upstream** (formato `git format-patch`, mensagem explicando o cenário
  medido, `Signed-off-by`) e avaliar envio para `linux-input`. É a contribuição de volta que dá
  sentido ao "fazer o que esqueceram".

### T2.5 — Enquanto o patch não está pronto
- A GUI/doctor AVISA quando a assinatura `[JOYCON]` aparecer (gate ≥10 timeouts antes do
  `exceeded`, já existente no kernel-watch), em vez de o controle cair calado. É transparência,
  não solução — a solução é o patch de T2.

## T3 — Interação com a Onda S (broker)
- Depois do broker instalado, RE-MEDIR o Pro BT com a Steam aberta e o WiFi controlado: quanto o
  broker sozinho melhora (tira o escritor Steam)? Isola a contribuição real do fator 3.

## Aceite
- Doctor cobre o check de T2 (assinatura [JOYCON] → aviso); os checks de rádio vivem na Onda W.
- Medição A/B materializada: Steam aberta com WiFi realocado × no xHCI vizinho — o Pro BT
  sobrevive no primeiro? (fecha ou reabre a hipótese 1).
- Mitigação (cabo / WiFi fora) documentada na GUI e no README.
- NADA de knob de rtw88/kernel sem medição A/B ao vivo (regra do projeto: sem gambiarra).
