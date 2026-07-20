# Estudo — Onda T: validação de premissas do patch `hid-nintendo` (pré-patch, read-only)

> Data: 2026-07-20 · Máquina: MeowSystem (Pop!_OS 24.04, kernel `7.0.11-76070011-generic`, System76)
> Sprint alvo: `docs/process/sprints/2026-07-20-sprint-onda-t-proBT-coexistencia.md` (T2.1)
> Método: 100% read-only no sistema/repo; downloads e build de teste SÓ neste scratchpad.
> Artefatos ao lado deste arquivo: `hid-nintendo-pop.c` (source exato do kernel em uso),
> `hid-nintendo-vanilla-7.0.11.c`, `hid-ids.h`, `build-test/hid-nintendo.ko` (prova DKMS),
> `commit-*.json` (diffs upstream), `log-torvalds.json` (histórico do arquivo).

---

## Sumário de vereditos

| # | Premissa | Veredito |
|---|----------|----------|
| 1 | Obter source EXATO do kernel em uso; difere do vanilla? | **CONFIRMADA (obtido)** — rota (b) pop-os/linux @ `3af2f9de4317`; **idêntico byte a byte ao vanilla v7.0.11** |
| 2 | Ao esgotar tentativas o driver "desiste/desregistra" | **PARCIAL** — o `exceeded max attempts` é warning **não-fatal**; o driver só desiste no **PROBE** (`probe - fail = -110`, 3× medidas); a desregistração pós-probe vem do stack BT (uhid/hidp), não do driver |
| 3 | Zero module params hoje | **CONFIRMADA** — 0 `parm:` no modinfo, 0 `module_param` no source, `/sys/module/hid_nintendo/parameters/` inexistente |
| 4 | Timeouts/tentativas hardcoded iguais p/ USB e BT | **PARCIAL** — timeout de espera (250ms), max attempts (25) e tries (2) são iguais; mas o **rate limiter JÁ diferencia por bus** (USB 20ms / BT 60ms, linha 823-825) |
| 5 | Existe fix upstream para portar? | **REFUTADA (nada a portar)** — os 4 commits relevantes de 2025 **já estão** no 7.0.11; nenhum torna nada não-fatal nem adiciona params; o mais recente (out/2025) foi na direção OPOSTA (500→25 attempts) |
| 6 | Viabilidade DKMS (compila out-of-tree contra os headers) | **CONFIRMADA** — compilou limpo com só `hid-nintendo.c` + `hid-ids.h` + Makefile de 2 linhas; vermagic bate; `depmod.d` já prioriza `updates/` |
| 7 | Assinatura da morte no journal (todos os boots) | **CONFIRMADA** — 1010× `timeout waiting` + 669× `exceeded` desde 16/07; morte de hoje (11:56:41→11:57:11) totalmente reconstruída; **duas assinaturas distintas** (rádio morto × jitter) + 3 mortes por probe |

---

## Premissa 1 — Source exato do kernel em uso

**Rota (a) `apt source`: VIÁVEL mas não usada.** `deb-src` já está habilitado
(`/etc/apt/sources.list.d/pop-os-release.sources:3: Types: deb deb-src`; idem `system.sources`)
e o pacote existe na versão EXATA:

```
linux-source-7.0.11  Candidato: 7.0.11-76070011.202606011647~1783638829~24.04~3af2f9d  (apt.pop-os.org/release noble/main)
```

Não usada só para evitar download de ~200MB — a rota (b) resolve com 90KB.

**Rota (b) pop-os/linux: FUNCIONOU (rota vencedora).** O sufixo `~3af2f9d` da versão do pacote é
o commit do repo github.com/pop-os/linux. Resolvido pela API do GitHub:
`3af2f9de43174ce5063110f94b7b01226499ba13` (author Tim Crawford/System76 2026-07-06, committer
Jeremy Soller 2026-07-09 — bate com o mtime do `.ko` instalado: `jul 9 20:13`,
`/lib/modules/7.0.11-76070011-generic/kernel/drivers/hid/hid-nintendo.ko.zst`). Baixado
`drivers/hid/hid-nintendo.c` (2847 linhas) e `drivers/hid/hid-ids.h` desse commit.

**Rota (c) kernel.org: FUNCIONOU (para o diff).** `git.kernel.org/...stable...plain/drivers/hid/hid-nintendo.c?h=v7.0.11`.

**Pop difere do vanilla? NÃO.** `diff hid-nintendo-pop.c hid-nintendo-vanilla-7.0.11.c` → vazio
(**idênticos**, 2847 linhas ambos). O patch pode ser desenvolvido contra o vanilla v7.0.11 sem
medo de delta System76.

## Premissa 2 — Quem espera, quanto, quantas vezes, e o que acontece ao esgotar

Todas as linhas abaixo referem-se a `hid-nintendo-pop.c` (== vanilla v7.0.11 == árvore do kernel
em uso).

### `joycon_wait_for_input_report()` — linhas 789-812
- Espera **HZ/4 = 250ms** (linha 804-806) pelo flag `received_input_report`, **uma única vez por
  chamada**, e **só quando `ctlr_state == JOYCON_CTLR_STATE_READ`** (linha 798).
- Ao estourar: loga `"timeout waiting for input report"` (linha 810) e **PROSSEGUE** — o
  comentário do próprio driver na linha 807: `/* We will still proceed, even with a timeout here */`.
- **Não-fatal. Sem retries próprios.** É a origem exata da 1ª mensagem da assinatura.

### `joycon_enforce_subcmd_rate()` — linhas 826-866
- Constantes (linhas 818-825):
  ```c
  #define JC_INPUT_REPORT_MIN_DELTA     8
  #define JC_INPUT_REPORT_MAX_DELTA     17
  #define JC_SUBCMD_TX_OFFSET_MS        4
  #define JC_SUBCMD_VALID_DELTA_REQ     3
  #define JC_SUBCMD_RATE_MAX_ATTEMPTS   25
  #define JC_SUBCMD_RATE_LIMITER_USB_MS 20
  #define JC_SUBCMD_RATE_LIMITER_BT_MS  60
  #define JC_SUBCMD_RATE_LIMITER_MS(ctlr) ((ctlr)->hdev->bus == BUS_USB ? ... : ...)
  ```
- Loop `do/while` (837-850): a cada volta chama `joycon_wait_for_input_report()` (até 250ms) e
  checa (i) 3 deltas consecutivos válidos entre input reports (8-17ms) e (ii) ≥20/60ms desde o
  último subcmd. Sai quando as condições valem, o estado muda, ou `attempts >= 25`.
- **Ao esgotar (linhas 852-855):** `hid_warn(ctlr->hdev, "%s: exceeded max attempts", __func__)`
  e `return`. A mensagem `joycon_enforce_subcmd_rate: exceeded max attempts` **existe** (o `%s`
  é `__func__`) e **a consequência é NENHUMA remoção**: a função é `void`, o chamador não fica
  sabendo, e o envio **acontece mesmo assim** logo em seguida.
- Custo de bloqueio no pior caso: 25 × 250ms = **6,25s por chamada** (segurando
  `output_mutex`) — bate exatamente com a cadência medida no journal (um `exceeded` a cada
  ~6-7s, ver premissa 7).
- **Nuance perigosa (alvo de patch):** após o `exceeded`, o subcmd é transmitido SEM rate-limit e
  sem o offset de 4ms — exatamente o que o comentário das linhas 814-817 diz que **causa
  desconexões BT**: `/* Sending subcommands and/or rumble data at too high a rate can cause
  bluetooth controller disconnections. */`. Ou seja, sob rádio degradado o driver martela o
  controle no pior momento possível, ajudando o firmware/stack a derrubar o link.

### `joycon_hid_send_sync()` — linhas 868-906
- `tries = 2` (linha 872, hardcoded). Cada try: `joycon_enforce_subcmd_rate()` (até 6,25s) →
  `__joycon_hid_send()` → `wait_event_timeout(ctlr->wait, ctlr->received_resp, timeout)`
  (linha 887; `timeout` vem do chamador).
- Esgotadas as 2 tries sem resposta: retorna **`-ETIMEDOUT`** (linha 897). Pior caso de bloqueio
  de UM subcmd: 2 × (6,25s + timeout).
- Timeouts dos chamadores (por subcmd, iguais p/ USB e BT): `HZ/4` (LEDs, linhas 969/1305),
  `HZ` (report mode/IMU/rumble-enable, 1010/1292/1318), `5×?` não — data_len; `2*HZ` só no
  `joycon_read_info` (linha 2423, veio do commit upstream b73bc6a51f0c).

### O que realmente mata o device — dois caminhos, só um é do driver
1. **PROBE (fatal, driver desiste de verdade):** `nintendo_hid_probe` (2628) → `joycon_init`
   (2688) → `joycon_read_info` (2497) → falha → `"Failed to retrieve controller info"` (2499) →
   `goto err_close` → `hid_hw_close`+`hid_hw_stop` (2722-2724) → `"probe - fail = -110"` (2728).
   O device **nunca registra**; não há re-tentativa nem re-probe. **Medido 3× nesta máquina**
   (17/07 00:08:08, 17/07 02:09:01, 18/07 21:26:47 — sempre `ret=-110`/`-ETIMEDOUT`, sempre BT
   `0005:`). Detalhe importante: durante o probe `ctlr_state == INIT`, então
   `joycon_enforce_subcmd_rate` é **no-op** (early return na linha 834-835) e
   `joycon_wait_for_input_report` não espera (guard na linha 798) — **a cascata
   `timeout waiting`/`exceeded` NUNCA vem do probe**; a assinatura do probe é outra
   (`Failed to get joycon info; ret=-110` → `probe - fail = -110`).
2. **Pós-registro (o driver NÃO se desregistra):** com o controle registrado e o rádio
   degradado, os escritores (LED classdev, `joycon_rumble_worker` 1805, battery) enfileiram
   subcmds que geram a cascata; TODOS os erros são só logados
   (ex.: linha 1820-1822 `"Failed to set rumble; e=%d"`). `nintendo_hid_remove` (2732) é chamado
   **de fora** — pelo hidp/uhid quando o link BT cai (supervision timeout, ou o bluetoothd
   destrói o device uhid). Evidência da morte de hoje: `leds ...:green:player-4: Setting an
   LED's brightness failed (-19)` às 11:57:11 — o `-ENODEV` vem de
   `joycon_send_subcmd` linha 934-936 (estado `REMOVED`), i.e. o remove JÁ tinha rodado.

**Veredito: PARCIAL.** "O driver desiste" é verdade **somente no probe** (e sem a mensagem
`exceeded`). A cascata `timeout waiting → exceeded` medida é pós-registro e não-fatal por si —
a desregistração observada é o **stack BT** derrubando o link (com provável contribuição do
próprio driver, que após o `exceeded` transmite fora do ritmo seguro).

## Premissa 3 — Zero module params

**CONFIRMADA.**
- `modinfo hid_nintendo` na máquina: **nenhuma linha `parm:`** (saída completa conferida;
  `intree: Y`, `vermagic: 7.0.11-76070011-generic`).
- `ls /sys/module/hid_nintendo/parameters/` → "Arquivo ou diretório inexistente" (com o módulo
  carregado: `lsmod | grep nintendo` → `hid_nintendo 53248 0`).
- `grep -n "module_param\|MODULE_PARM" hid-nintendo-pop.c` → **0 resultados**.
- Todos os limiares são `#define` (linhas 818-825) ou literais (`HZ/4` linha 806, `tries = 2`
  linha 872, timeouts por chamada).

## Premissa 4 — Diferenciação por transporte hoje

**PARCIAL — a premissa do sprint estava incompleta.** O que JÁ diferencia por `hdev->bus`:
- **Rate limiter**: `JC_SUBCMD_RATE_LIMITER_USB_MS 20` × `JC_SUBCMD_RATE_LIMITER_BT_MS 60`
  (linhas 823-825) — BT já é 3× mais folgado NESTE ponto.
- Linhas 1751-1752: em USB, `consecutive_valid_report_deltas` é forçado ao máximo (o critério de
  "3 deltas válidos" só trava BT).
- `joycon_using_usb()` (769-772) decide handshake/baudrate no init e o resume
  (2757: BT é no-op de resume — commit 4a0381080397).

O que é **igual e hardcoded** para os dois transportes (alvos do patch):
- Espera por input report: **HZ/4 = 250ms** (linha 806);
- **`JC_SUBCMD_RATE_MAX_ATTEMPTS 25`** (linha 822);
- **`tries = 2`** no send_sync (linha 872);
- Timeouts de resposta por subcmd (HZ/4, HZ, 2*HZ nos call sites).

Nota para o patch: o device de hoje entrou via **uhid** (BlueZ 5.85) e mesmo assim reporta
`bus 0005` (BLUETOOTH) — o uhid propaga o bus real, então diferenciação por `hdev->bus`
**continua funcionando** no mundo pós-BlueZ-5.85 desta máquina.

## Premissa 5 — O que já existe upstream (não reinventar)

Histórico completo do arquivo obtido via API do GitHub (`log-torvalds.json`, 50 commits até
2026-06-18). Commits relevantes dos últimos ~2 anos, com diff conferido (`commit-*.json`):

| Commit | Data | O quê | Já no 7.0.11? |
|--------|------|-------|----------------|
| `2295657ac30a` | 2025-10-30 | **Reduce JC_SUBCMD_RATE_MAX_ATTEMPTS 500→25** (Willy Huang/Google, Reviewed-by Ogorchock): corta o pior caso de bloqueio de 60s→3s | **SIM** (nosso 25 da linha 822 é ESTE commit) |
| `b73bc6a51f0c` | 2025-10-07 | **Wait longer for initial probe** (Vicki Pfau): `joycon_read_info` HZ→**2*HZ** p/ third-party lentos | **SIM** (linha 2423) |
| `b8874720b2f3` | 2025-10-07 | Rate limit IMU compensation message (`hid_warn_ratelimited`) | **SIM** (journal mostra "callbacks suppressed") |
| `4a0381080397` | 2025-05-13 | **avoid bluetooth suspend/resume stalls**: estado `SUSPENDED` + resume no-op p/ BT — reconhece EXATAMENTE o nosso cenário ("bluetooth controllers which lose connectivity... joycon_enforce_subcmd_rate can result in repeated retries") mas só protege suspend/resume | **SIM** (linhas 2751-2791) |
| `d7b7ce3dc616` | 2026-01-13 | pm_ptr em vez de #ifdef CONFIG_PM | SIM |
| `9146038120a6` | 2026-05-27 | Suporte HORI Wireless Switch Pad | SIM |
| `7cde5613006c` | 2026-06-03 | %pM para MAC | SIM |

**Conclusão: NÃO existe patch upstream que (i) torne o esgotamento/probe não-fatal, (ii) adicione
module params, ou (iii) trate BT degradado pós-registro.** Nada a portar — o patch da Onda T é
trabalho novo. Pontos estratégicos para o upstream depois (T2.4):
- O tema é ativo e aceito: dois fixes de 2025 mexeram exatamente nessas constantes, e o
  `4a0381080397` do próprio Ogorchock descreve o cenário de rádio degradado (mas só no suspend).
- A direção de `2295657ac30a` (REDUZIR bloqueio, Reviewed-by do mantenedor) sugere que um patch
  que **aumente** timeouts fixos teria resistência — module params com defaults atuais +
  supressão de TX após `exceeded` (que REDUZ tráfego no pior momento) é a narrativa vendável.
- Ecossistema DKMS já praticado para este driver: `emilyst/hid-nx-dkms` e
  `nicman23/dkms-hid-nintendo` (referências de estrutura de dkms.conf; nenhum dos dois cura o
  nosso problema — são o driver de época empacotado/renomeado).
- Discussão do `2295657ac30a` está em lkml.org/lkml/2025/10/30/1460 (inacessível desta rede —
  Anubis; o Reviewed-by no commit confirma o aceite).

## Premissa 6 — Viabilidade DKMS

**CONFIRMADA por build real** (dentro do scratchpad, nada instalado, módulo NÃO carregado):
```
build-test/
├── hid-nintendo.c   (cópia exata do source do kernel em uso)
├── hid-ids.h        (do mesmo commit pop-os; único header local necessário)
└── Makefile         (2 linhas: obj-m := hid-nintendo.o
                                 ccflags-y := -DCONFIG_NINTENDO_FF=1)
$ make -C /usr/src/linux-headers-7.0.11-76070011-generic M=$PWD modules
  → CC/MODPOST/LD OK → hid-nintendo.ko gerado
```
- **Dependências de arquivo**: só `hid-ids.h` além do `.c` (o include local da linha 31); o
  resto são headers públicos (`linux/hid.h`, `linux/unaligned.h`, etc.) presentes no pacote de
  headers.
- **Símbolos externos**: `hid` e `ff-memless` (o `.ko` gerado declara `depends: hid,ff-memless`)
  — CRCs resolvidos pelo `Module.symvers` dos headers, MODPOST sem warnings de símbolo.
- **Config**: in-tree é `CONFIG_HID_NINTENDO=m` + `CONFIG_NINTENDO_FF=y` (conferido em
  `/boot/config-7.0.11-76070011-generic`); out-of-tree replica-se com `-DCONFIG_NINTENDO_FF=1`
  (o código usa `IS_ENABLED`, linha 1835).
- **vermagic do .ko gerado bate**: `7.0.11-76070011-generic SMP preempt mod_unload modversions`.
- **Precedência sobre o in-tree é automática**: `/etc/depmod.d/ubuntu.conf` =
  `search updates ubuntu built-in` — DKMS instala em `updates/dkms`, que vence o in-tree sem
  precisar de blacklist (ainda assim recomendo `dkms.conf` com `AUTOINSTALL=yes` e o install.sh
  validando com `modinfo -F filename hid_nintendo` == caminho updates).
- Avisos benignos do build: "pahole version differs" e "Skipping BTF generation... unavailability
  of vmlinux" — padrão em builds out-of-tree Ubuntu/Pop (headers não trazem vmlinux); módulos
  DKMS (ex.: nvidia desta máquina) convivem com isso.
- Caveat honesto: `srcversion` do .ko gerado (`E510116794E5943C26F761D`) difere do in-tree
  (`098AB755D743D99788D82ED`) — esperado (o hash MD4 inclui contexto de build/caminhos, não só o
  texto do .c, que é idêntico). Não afeta carga nem funcionamento; o doctor NÃO deve usar
  srcversion como critério de "é o nosso" — usar o caminho do .ko e (pós-patch) a presença de
  `/sys/module/hid_nintendo/parameters/`.

## Premissa 7 — Assinatura real no journal (todos os boots, `_TRANSPORT=kernel`)

**CONFIRMADA e enriquecida.** Totais desde 16/07 (journal completo, NUNCA `-k`):
- `timeout waiting for input report`: **1010** ocorrências (primeira: 16/07 12:38:47; última:
  20/07 11:57:11) — sempre em device `0005:*` (BT).
- `joycon_enforce_subcmd_rate: exceeded max attempts`: **669** ocorrências.
- `probe - fail = -110`: **3** (17/07 00:08:08 `.0008`, 17/07 02:09:01 `.000A`,
  18/07 21:26:47 `.000F`) — a morte "invisível" que a premissa 2 revelou.

**Morte de hoje, reconstruída (20/07, device `0005:057E:2009.0041`, via uhid/BlueZ 5.85):**
```
11:56:41  conecta (hidraw4 BLUETOOTH HID), MAC E0:F6:B5:00:00:01, player 1, input877/878 (uhid)
11:56:42  "compensating for 4/10 dropped IMU reports" (rádio já degradando)
11:56:43  1º "exceeded max attempts"
11:56:43→11:57:11  ~112 "timeout waiting" a 4/s  ← 4/s == 4 × 250ms: prova o HZ/4 da linha 806
11:56:43,:50,:56, 11:57:03,:09  "exceeded" a cada ~6,5s  ← 25 × 250ms = 6,25s: prova o 25 da linha 822
11:57:11  "leds ...green:player-4: Setting an LED's brightness failed (-19)"
          ← -ENODEV do estado REMOVED (linha 934-936): o link BT caiu e o remove() já rodou.
          O driver NÃO desregistrou; o transporte morreu por baixo dele.
```

**Duas assinaturas distintas de `exceeded` (diagnóstico novo, útil pro doctor):**
- **Rádio morto** (19/07 14:52-16:27 e 20/07 11:56): `exceeded` em cadência de **~6,5s** —
  cada uma das 25 voltas queima os 250ms inteiros (zero input reports chegando).
- **Reports fluindo com jitter** (18/07 20:15-20:23, dia da guerra de escritores): `exceeded`
  **1-2 por segundo** durante 8 minutos — as esperas retornam rápido (reports chegam), mas os
  deltas nunca ficam 3× seguidas na janela 8-17ms, e as 25 voltas queimam em <1s. Assinatura de
  interferência/contenda, não de silêncio.
- O gate atual do kernel-watch (≥10 timeouts antes do exceeded) só enxerga a primeira; a segunda
  quase não emite `timeout waiting`. E NENHUMA das duas cobre a morte por probe
  (`Failed to get joycon info; ret=-110` → `probe - fail = -110`) — adicionar essa assinatura.

## Becos percorridos (não repetir)

- `lkml.org`, `git.kernel.org` (web) e `lore.kernel.org` estão **bloqueados por Anubis** nesta
  rede — a rota que funciona para histórico/diffs upstream é a **API do GitHub**
  (`api.github.com/repos/torvalds/linux/commits?path=...` e `/commits/<sha>` com `.files[].patch`).
- O patch do AUR `0006-HID-nintendo-improve-subcommand-reliability.patch` (linux-llvm) **não
  existe mais** no branch (404) — era quase certamente o backport da série de 2021
  (`e93363f716a2` "ratelimit subcommands and rumble"), que já está no in-tree. Sem valor.
- `apt source`: viável (deb-src habilitado + `linux-source-7.0.11` na versão exata), mas
  desnecessária — manter como plano B para a fase de patch se quisermos a árvore inteira.
- `journalctl -k` segue proibido (implica `-b`); todos os números acima são de
  `_TRANSPORT=kernel` no journal completo.

## Recomendação de desenho do patch (T2.2 revisado contra o código real)

A hipótese do sprint ("tornar o esgotamento não-fatal") precisa de ajuste: **o esgotamento já é
não-fatal**; os problemas reais são (A) a morte por probe, (B) o TX fora de ritmo após o
`exceeded`, e (C) a impossibilidade de tuning. Alvos concretos (linhas do v7.0.11):

1. **[B] Não transmitir no pior momento** — `joycon_enforce_subcmd_rate()` (826) passa a
   retornar `int`; ao esgotar (852-855) retorna `-EAGAIN` e `joycon_hid_send_sync()` (868)
   **pula o TX** dessa try (hoje ele envia às cegas na linha 881). Efeito: sob rádio degradado o
   driver silencia em vez de martelar — reduz a chance de o firmware derrubar o link (comentário
   814-817 do próprio driver). É também a narrativa upstream-friendly (reduz tráfego e bloqueio,
   mesma direção de `2295657ac30a`).
2. **[A] Probe resiliente em BT** — `joycon_read_info` falhou = morte hoje. Opções em ordem de
   conservadorismo: (i) elevar `tries` de 2 para N em `joycon_hid_send_sync` quando
   `!joycon_using_usb()` **apenas durante o probe**; (ii) laço de retry em torno de
   `joycon_init()` no probe (2688) com backoff curto; (iii) `-EPROBE_DEFER` — evitar, semântica
   duvidosa para HID/uhid.
3. **[C] Module params com defaults atuais** (zero regressão): `input_report_wait_ms` (default
   250 — linha 806), `subcmd_rate_max_attempts` (default 25 — linha 822), `sync_send_tries`
   (default 2 — linha 872), `probe_info_timeout_ms` (default 2000 — linha 2423),
   `bt_probe_retries` (default do item 2). Só isto já destrava a investigação empírica de campo
   (T2.2 item 3) e dá o marcador de "patch carregado" para o doctor
   (`/sys/module/hid_nintendo/parameters/`).
4. **Diferenciação por transporte**: já existe o padrão no código (823-825) — se necessário
   após medição, params separados `*_bt`/`*_usb` seguindo `JC_SUBCMD_RATE_LIMITER_*`; não
   inventar mecanismo novo.
5. **Doctor/kernel-watch**: adicionar as assinaturas que faltam — `probe - fail = -110`
   (morte por probe) e o padrão "exceeded denso sem timeouts" (jitter/interferência), além do
   gate atual.
6. **DKMS**: estrutura provada em `build-test/`; `dkms.conf` com `BUILT_MODULE_NAME=hid-nintendo`,
   install em `updates/dkms` (precedência automática via `search updates ubuntu built-in`),
   install.sh idempotente com warn honesto se faltarem headers, uninstall simétrico
   (`dkms remove` + `depmod` → in-tree volta sozinho). Fail-safe natural: se o build falhar num
   kernel novo, o in-tree continua lá.

**Limite honesto do patch:** ele não impede o link BT de cair sob EMI (isso é a Onda W / rádio);
ele garante que (a) o controle não morre no probe ao reconectar, (b) o driver não piora a
degradação martelando TX, e (c) tudo vira mensurável/ajustável. O "volta sozinho quando o rádio
volta" depende do re-probe pós-reconexão do BlueZ — que hoje falha pelo item (A) e é exatamente
o que o item 2 cura.
