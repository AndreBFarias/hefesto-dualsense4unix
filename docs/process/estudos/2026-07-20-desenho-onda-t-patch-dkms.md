# Desenho — Onda T: patch do `hid-nintendo` + infra DKMS (T2.2/T2.3/T2.4)

> Data: 2026-07-20 · Base: kernel `7.0.11-76070011-generic` (Pop!_OS == vanilla v7.0.11, byte a
> byte — provado no estudo de premissas). Decisão da mantenedora: cura na RAIZ do kernel
> ("tá liberado alterar o kernel").
> Estudo que valida as premissas: `2026-07-20-estudo-premissas-onda-t-hid-nintendo.md` (LER antes).
> Artefatos PRONTOS E TESTADOS no scratchpad (fonte da verdade p/ a fase de implementação):
> `/tmp/claude-1000/-home-vitoriamaria-Desenvolvimento-hefesto-dualsense4unix/9c5a2e4c-d6ac-4e4f-9160-64cb5426f321/scratchpad/onda-t-patch/`
> (`hid-nintendo.c` patchado, `0001-*.patch`, `dkms.conf`, `Makefile`, `dkms_lib.sh`,
> `hefesto-hid-nintendo.conf`, `BASELINE`, `hid-nintendo.ko` compilado).

## Prova de build (obrigatória — FEITA)

```
$ make -C /usr/src/linux-headers-7.0.11-76070011-generic M=<scratchpad>/onda-t-patch modules
  CC [M]  hid-nintendo.o          ← ZERO warnings no nosso código
  MODPOST Module.symvers
  LD [M]  hid-nintendo.ko         ← 833264 bytes
$ modinfo hid-nintendo.ko
  vermagic: 7.0.11-76070011-generic SMP preempt mod_unload modversions   ← bate
  depends:  hid,ff-memless
  parm:     input_report_wait_ms / subcmd_rate_max_attempts / sync_send_tries /
            probe_info_timeout_ms / bt_probe_retries /
            skip_tx_on_rate_exceeded                                    ← 6 params
```
Avisos benignos idênticos ao estudo (pahole/BTF — padrão out-of-tree Ubuntu/Pop). Rebuild após
`make clean` reconfirmado. `CONFIG_HZ=1000` conferido em `/boot/config-…`: `HZ/4` = 250 jiffies =
exatamente `msecs_to_jiffies(250)` e `2*HZ` = `msecs_to_jiffies(2000)` — **equivalência numérica
EXATA dos defaults, VÁLIDA SÓ PARA HZ=1000 (o desta máquina)**. Escopo honesto (achado #3 do
corretor): a fórmula do kernel p/ `HZ<=1000` arredonda para CIMA (`msecs_to_jiffies(250)` em
HZ=250 = (250+3)/4 = **63** jiffies) enquanto `HZ/4` trunca (250/4 = **62**) — em HZ=250 (comum
em kernels Ubuntu/Debian genéricos) o wait fica 1 jiffy (~4ms) MAIOR que o vanilla. Divergência
funcionalmente desprezível, mas REAL: quem reusar este padrão de param (Onda W/rtw88 ou outra
máquina) deve re-verificar a aritmética de arredondamento para o CONFIG_HZ daquele kernel
(`probe_info_timeout_ms=2000` vs `2*HZ` coincide em HZ=1000/250/100; só `input_report_wait_ms`
diverge).

Paridade provada por sha256:
- vanilla v7.0.11: `6b71cb4925c9…db2975`
- patchado:        `cf3a3c6d2a6b…0ca98d` (== vanilla + `0001-*.patch`; `patch -R` devolve o
  vanilla exato — os dois sentidos verificados; sha completo no `patch/BASELINE`)
- `hid-ids.h`:     `a88d22bed083…ad7838` (intocado; único header local do build)

## O patch — 8 mudanças concretas (função:linha do v7.0.11)

Código C em inglês (convenção do subsistema). NENHUMA mudança de comportamento com os defaults —
inclusive [B] (achado #1 do corretor): o skip-TX é gateado pelo param `skip_tx_on_rate_exceeded`
(default 0 == vanilla, transmitir às cegas como sempre); a mudança entra OPT-IN pela conf do
hefesto, reversível AO VIVO via /sys sem recompilar — a validação A/B (T2.4) usa esse knob.

### [C] Module params (topo do arquivo, após os includes — linha 43+)
Bloco novo com 5 params `uint` + 1 `bool` em `0644` (root pode ajustar AO VIVO via
`/sys/module/hid_nintendo/parameters/` — leitura word-sized a cada uso, sem lock, seguro):

| Param | Default | Substitui | Onde é lido |
|---|---|---|---|
| `input_report_wait_ms` | 250 | `HZ / 4` | `joycon_wait_for_input_report()` :806 |
| `subcmd_rate_max_attempts` | 25 | `JC_SUBCMD_RATE_MAX_ATTEMPTS` | `joycon_enforce_subcmd_rate()` :850/:852 (clamp 1..1000) |
| `sync_send_tries` | 2 | `tries = 2` | `joycon_hid_send_sync()` :872 (clamp 1..10) |
| `probe_info_timeout_ms` | 2000 | `2 * HZ` | `joycon_read_info()` :2423 |
| `bt_probe_retries` | **0** | (novo) | `nintendo_hid_probe()` :2688+ (clamp 0..10) |
| `skip_tx_on_rate_exceeded` | **0** (bool) | (novo — gate do [B]) | `joycon_enforce_subcmd_rate()` no ramo "exceeded" |

Os clamps protegem contra valores absurdos (0 attempts = -EAGAIN eterno; tries=0 = nunca envia).
A PRESENÇA do diretório `parameters/` é o marcador "patch carregado" do doctor (o in-tree tem
zero params — confirmado no estudo).

### [B] Não transmitir no pior momento (OPT-IN via `skip_tx_on_rate_exceeded`)
1. **`joycon_enforce_subcmd_rate()` :826 — `void` → `int`.** Retorna `0` nos caminhos atuais
   (estado ≠ READ :834, e janela segura encontrada) e **`-EAGAIN` ao esgotar SE
   `skip_tx_on_rate_exceeded=1`** (default 0: cai no fluxo vanilla e transmite como sempre), logo
   após o MESMO `hid_warn "exceeded max attempts"` (string preservada byte a byte — o
   kernel-watch/doctor atuais continuam casando). Hoje a função esgota e o chamador transmite às
   cegas, sem rate-limit e sem o offset de 4ms — exatamente o que o comentário :814-817 do
   próprio driver diz que derruba o link BT. Achado #1 do corretor: como o efeito real do skip
   sob congestionamento ainda NÃO foi medido ao vivo (risco #4), ele NÃO pode ser incondicional —
   o gate dá opt-out em runtime (`echo 0 > /sys/module/hid_nintendo/parameters/skip_tx_on_rate_exceeded`)
   sem recompilar/remover o módulo.
2. **`joycon_hid_send_sync()` :868 — pula o TX da try.** `ret = joycon_enforce_subcmd_rate();`
   se `-EAGAIN`: `memset(input_buf)` + `ret = -ETIMEDOUT` + `continue` (consome a try SEM
   transmitir). Semântica externa preservada: sob rádio morto o chamador já recebia
   `-ETIMEDOUT` (TX às cegas → sem resposta → timeout); agora recebe o mesmo erro sem ter
   martelado o link. Quando NÃO esgota: fluxo idêntico ao vanilla. `output_mutex`: intocado —
   a função continua sendo chamada com o mutex tomado pelos mesmos donos.
3. **`joycon_send_rumble_data()` :1798 — dropa o pacote de rumble.** `if (ret) return ret;`
   (devolve `-EAGAIN`). Era o segundo call-site que transmitia às cegas (:1800).
4. **`joycon_rumble_worker()` :1820 — silencia o drop.** Condição do warn ganha
   `&& ret != -EAGAIN` (o "exceeded" já foi logado; sem isso cada drop viraria um
   "Failed to set rumble; e=-11" espúrio no journal). Único caller de send_rumble_data — nenhum
   outro código vê o `-EAGAIN` novo.

### [A] Probe BT resiliente (a cura da morte medida 3×)
**`nintendo_hid_probe()` :2688** — em volta do `ret = joycon_init(hdev);`:
```c
if (ret && !joycon_using_usb(ctlr)) {
        int retries = clamp_t(int, bt_probe_retries, 0, 10);
        unsigned int backoff_ms = 100;
        while (ret && retries--) {
                hid_warn(hdev, "init over bluetooth failed (%d); retrying (%d left)\n", ...);
                msleep(backoff_ms);
                if (backoff_ms < 1600) backoff_ms *= 2;
                ret = joycon_init(hdev);
        }
}
```
- **Só BT** (`!joycon_using_usb()`): por USB o transporte é confiável e a falha é significativa.
- **Backoff exponencial 100→200→400…ms** (teto 1600), simples e sem timer.
- **Sem `-EPROBE_DEFER`** (semântica duvidosa p/ HID/uhid — decisão da missão).
- Re-chamar `joycon_init()` inteiro em BT é seguro: o ramo USB (handshake/baudrate) é pulado e o
  caminho BT é só `read_info`+calibração+IMU+report-mode+rumble-enable — cada um dos 5
  subcomandos é reenviável sem estado cumulativo no driver (auditados um a um). CORREÇÃO (achado
  #2 do corretor): a justificativa anterior citava o resume como precedente ("o resume :2763 já
  re-executa joycon_init() no mesmo device desde sempre") — isso é verdade SÓ NO RAMO USB; para
  BT o `nintendo_hid_resume()` é um no-op explícito (`hid_dbg "no-op resume for bt ctlr"`),
  então NÃO existe precedente vanilla de re-chamada de `joycon_init()` no transporte em que o
  retry atua. A segurança se sustenta na auditoria dos subcomandos (acima) + na validação ao
  vivo do checklist, não em precedente — revisor upstream deve ler ESTA versão do argumento.
- Durante o probe `ctlr_state == INIT` ⇒ enforce_rate e wait_for_input_report são no-op (guards
  :834/:798) — o retry NÃO interage com [B].
- Pior caso com retries=3 e link morto: 4×(2 tries×2s) + 0,7s ≈ **16,7s** segurando o probe —
  aceitável (roda em contexto de probe do hidp/uhid; o clamp 10 impede absurdo).

**Defaults `bt_probe_retries=0` + `skip_tx_on_rate_exceeded=0` = comportamento IDÊNTICO ao
vanilla — justificativa da zero-regressão:** o loop de retry nem arma e o skip-TX nem liga. Quem
instala só o módulo DKMS sem configurar nada tem o driver de hoje, bit a bit de comportamento.
A CURA entra pela conf do hefesto: `/etc/modprobe.d/hefesto-hid-nintendo.conf` →
`options hid_nintendo bt_probe_retries=3 skip_tx_on_rate_exceeded=1` (instalada/removida pelo
install/uninstall — auditável, reversível, simétrica; o skip também reversível a quente via
/sys). É também a narrativa upstream vendável: TODO comportamento novo é opt-in, e o [B] ligado
REDUZ tráfego no pior momento (mesma direção do `2295657ac30a`, Reviewed-by do mantenedor).

**Fail-safe da conf provado pelo código do kernel:** se o in-tree carregar com a conf presente
(ex.: DKMS removido/quebrado), `load_module()` usa `unknown_module_param_cb` (kernel/params.c,
desde v3.17): loga `hid_nintendo: unknown parameter 'bt_probe_retries' ignored` e **carrega
normalmente** — nunca ficamos sem controle. (Validar essa linha no journal do 1º boot é item do
checklist ao vivo; a mensagem é até um marcador útil de "in-tree em uso".)

## Infra DKMS — genérica e reutilizável (Onda W reusa p/ rtw88)

### Layout de assets padronizado
```
assets/dkms/<modulo>/            # ex.: assets/dkms/hid-nintendo/
├── dkms.conf                    # PACKAGE_NAME=hefesto-<modulo>
├── Makefile                     # kbuild mínimo (2 linhas p/ hid-nintendo)
├── <fontes>                     # hid-nintendo.c (JÁ patchado) + hid-ids.h
└── patch/                       # NÃO entra no build (o helper exclui)
    ├── 0001-….patch             # format-patch: rebase futuro + submissão upstream
    └── BASELINE                 # kernel base, commit pop-os, sha256 de tudo
assets/modprobe.d/hefesto-hid-nintendo.conf   # options bt_probe_retries=3 skip_tx_on_rate_exceeded=1
scripts/dkms_lib.sh              # helper genérico (biblioteca, source pelo install)
```

### `dkms.conf` (draft pronto no scratchpad)
```
PACKAGE_NAME="hefesto-hid-nintendo"        PACKAGE_VERSION="1.0.0"
BUILT_MODULE_NAME[0]="hid-nintendo"        DEST_MODULE_LOCATION[0]="/updates/dkms"
AUTOINSTALL="yes"
MAKE[0]="make -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build modules"
CLEAN="make -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build clean"
```
Makefile: `obj-m := hid-nintendo.o` + `ccflags-y := -DCONFIG_NINTENDO_FF=1` (o in-tree tem
`CONFIG_NINTENDO_FF=y`; sem isso o rumble sumiria — provado no build-test do estudo).
Precedência: `/etc/depmod.d/ubuntu.conf` = `search updates ubuntu built-in` ⇒ `updates/dkms`
vence o in-tree AUTOMATICAMENTE, sem blacklist. `AUTOINSTALL=yes` reconstrói em update de kernel.

### `scripts/dkms_lib.sh` — API (draft completo e `bash -n`-limpo no scratchpad)
```
dkms_install_patched_module <pkg> <ver> <src_dir> <builtname>
dkms_remove_patched_module  <pkg> <ver>
dkms_module_from_updates    <builtname>     # modinfo -F filename == */updates/dkms/*
dkms_module_loaded          <sysname>
```
Contrato inviolável embutido: (i) **fail-safe** — dkms/headers ausentes ou build falho = warn
honesto + `return 0`, in-tree continua, install NUNCA aborta; (ii) **NUNCA (rm)modprobe** — a
ativação é do chamador e a mensagem é "vale no próximo boot"; (iii) **idempotente** —
re-sincroniza `/usr/src/<pkg>-<ver>` só se os assets mudaram (`diff -rq -x patch`), tolera
add/build/install repetidos, exclui `patch/` do source copiado; (iv) valida com
`modinfo -F filename` apontando p/ `updates/dkms`.

### install.sh — passo novo (DEFAULT ON, opt-out `--no-dkms`)
Regra da casa: install SEM FLAGS aplica o DKMS. Esqueleto do passo (na família 3, após 3d):
```
step "3e" "Cura de raiz do hid-nintendo BT (módulo DKMS + retry de probe)"
if [[ "${NO_DKMS:-0}" == "1" ]]; then  # --no-dkms (CI/sem hardware, como --no-udev)
    printf '      pulado (--no-dkms)\n'
else
    source "${ROOT_DIR}/scripts/dkms_lib.sh"
    dkms_install_patched_module hefesto-hid-nintendo 1.0.0 \
        "${ROOT_DIR}/assets/dkms/hid-nintendo" hid-nintendo
    sudo install -Dm644 "${ROOT_DIR}/assets/modprobe.d/hefesto-hid-nintendo.conf" \
        /etc/modprobe.d/hefesto-hid-nintendo.conf
    # ATIVAÇÃO FAIL-SAFE (padrão btusb): NUNCA recarregar com controle em uso —
    # a mantenedora está jogando com Pro/8BitDo conectados AGORA.
    if [[ -d /sys/module/hid_nintendo/parameters ]]; then
        printf '      módulo patchado JÁ carregado (params visíveis)\n'
    elif [[ -d /sys/module/hid_nintendo ]]; then
        printf '      módulo in-tree em uso — NÃO recarregamos (derrubaria Pro/8BitDo);\n'
        printf '      o patchado vale no próximo boot\n'
    else
        printf '      hid_nintendo descarregado — o patchado entra sozinho no próximo plug\n'
    fi
fi
```
Nota de precisão (diferente do btusb): substituição de módulo NÃO pega em replug — se o in-tree
está CARREGADO, o replug re-liga no módulo carregado. Mensagem honesta = "próximo boot" (replug
só vale se o módulo estiver descarregado). O texto acima já distingue os dois casos.

### uninstall.sh — simétrico (sem flag nova)
```
source scripts/dkms_lib.sh   # (ou cópia inline das 2 funções, padrão do uninstall)
dkms_remove_patched_module hefesto-hid-nintendo 1.0.0
sudo rm -f /etc/modprobe.d/hefesto-hid-nintendo.conf
# in-tree volta SOZINHO no próximo boot (depmod já rodou); o patchado carregado
# continua até lá — inócuo: defaults == vanilla e a conf de options já saiu.
```

## Patch para upstream (T2.4)

- **Onde vive no repo:** `assets/dkms/hid-nintendo/patch/0001-HID-nintendo-do-not-transmit-after-rate-limit-exhaus.patch`
  — duplo propósito: rebase do DKMS + base da submissão a `linux-input@vger.kernel.org`
  (cc Daniel J. Ogorchock). Draft PRONTO no scratchpad, formato `git format-patch`, aplica limpo
  com `patch -p3` (e `git am` após ajustar `-p1`… o caminho já é `a/drivers/hid/hid-nintendo.c`,
  então `git am` funciona direto).
- **Mensagem:** descreve o cenário MEDIDO (burst de `timeout waiting` a 4/s + `exceeded` a cada
  ~6,5s até o link cair; 3 mortes por probe `-110` em bus 0005) e a lógica "transmitir após
  esgotar é o que o próprio comentário do driver diz que derruba BT".
- **Anonimato (gate `check_anonymity`):** SoB placeholder do projeto —
  `Signed-off-by: Hefesto DualSense4Unix Project <hefesto-dualsense4unix@users.noreply.github.com>`.
  **Limite honesto:** o DCO do kernel exige nome real de pessoa; a submissão REAL requer a
  mantenedora trocar o SoB (decisão dela, fora do repo). O repo fica anônimo.
- **Recomendação p/ submissão real:** quebrar em série de 3 ([B] correção, [A] retry opt-in,
  [C] params) — upstream prefere patches atômicos; o combinado fica pro DKMS.

## Sincronização do .c do DKMS (estratégia de rebase)

- **Invariante:** `assets/dkms/hid-nintendo/hid-nintendo.c` == vanilla(BASELINE) + `0001-*.patch`.
  O build usa o `.c` final (não aplica patch em build-time — menos partes móveis no dkms).
  `patch/BASELINE` grava kernel base, commit pop-os/linux e os 3 sha256; teste de paridade
  reverte o patch (`patch -R`) e confere o sha do vanilla — pega qualquer edição manual no `.c`
  que não passou pelo `.patch` (e vice-versa).
- **Update de kernel (mesma série 7.0.x):** `AUTOINSTALL=yes` reconstrói o MESMO `.c` contra os
  headers novos. Se compilar: segue valendo (driver congelado no v7.0.11 — conferir changelog do
  `hid-nintendo` upstream por fixes novos a cada rebase de série).
- **Kernel novo em que o build FALHA (API HID mudou):** dkms pula o módulo → in-tree do kernel
  novo carrega (fail-safe físico); o doctor avisa "DKMS não construído p/ este kernel" (check
  abaixo) para a cura não sumir em silêncio. Rebase: baixar o vanilla novo (rota pop-os/linux ou
  kernel.org do estudo), `patch -p3 < 0001-*.patch` (fuzz), resolver, atualizar BASELINE +
  `PACKAGE_VERSION`, re-provar build, re-rodar install.
- **Risco aceito:** entre o update de kernel e o rebase, ou roda-se o nosso driver de época
  (build OK) ou o in-tree novo (build falho) — nunca "sem driver".

## Doctor / kernel-watch (assinaturas novas)

`scripts/doctor.sh` — check novo `check_hefesto_hid_nintendo_dkms`:
1. `dkms status hefesto-hid-nintendo` instalado p/ `uname -r`? Se instalado p/ OUTRO kernel
   apenas: warn "DKMS não construído p/ este kernel — rebase pendente, in-tree em uso".
2. `modinfo -F filename hid_nintendo` contém `/updates/dkms/`? (== próximo carregamento é o
   patchado). NÃO usar srcversion (armadilha documentada no estudo).
3. Módulo carregado é o patchado? `[[ -d /sys/module/hid_nintendo/parameters ]]` → ok + mostrar
   `bt_probe_retries` efetivo (esperado 3 via conf); DKMS instalado mas params ausentes com
   módulo carregado → warn "in-tree ainda em uso — vale no próximo boot".
4. Assinaturas de journal que FALTAM hoje (ambas do estudo, premissa 7):
   - **morte por probe**: `Failed to get joycon info; ret=-110` seguido de `probe - fail = -110`
     → warn dedicado (é a morte "invisível"; se aparecer também
     `init over bluetooth failed .* retrying`, o retry do patch está agindo — reportar);
   - **exceeded denso sem timeouts** (jitter/interferência): na janela, se
     `exceeded ≥ 5` e `timeouts < exceeded` → warn "interferência/contenda BT" (o gate atual de
     ≥10 timeouts só vê a assinatura de rádio morto).

`scripts/storm_watch.sh` — `GREP_UNION` ganha `probe - fail = -|failed to get joycon info|init
over bluetooth failed`, com tag nova `[JOYCON-PROBE]` (manter `[JOYCON]` intacto — a string
`exceeded max attempts` não mudou no patch).

## Manifesto por lote (CORRIGIDO pelo corretor — achado #10: a lista original
## omitia 5 arquivos que a implementação PRECISOU tocar)

- **dkms** (`assets/**`): `assets/dkms/hid-nintendo/{hid-nintendo.c, hid-ids.h, Makefile,
  dkms.conf, patch/0001-HID-nintendo-do-not-transmit-after-rate-limit-exhaus.patch,
  patch/BASELINE}` + `assets/modprobe.d/hefesto-hid-nintendo.conf`.
- **install**: `scripts/dkms_lib.sh`, `install.sh` (passo 3i + flag `--no-dkms` opt-out),
  `uninstall.sh` (remoção simétrica), `scripts/doctor.sh` (check + assinaturas),
  `scripts/storm_watch.sh` (tag `[JOYCON-PROBE]`).
- **packaging (exigido pelo gate `scripts/check_packaging_parity.sh`, que varre
  `assets/modprobe{,.d}/*.conf` e agora também `assets/dkms/` — o desenho original NÃO previa
  este lote, mas ele é obrigatório):** `scripts/build_deb.sh`, `packaging/arch/PKGBUILD`,
  `packaging/fedora/hefesto-dualsense4unix.spec`, `flatpak/br.andrefarias.Hefesto.yml`,
  `scripts/install-host-udev.sh` (conf + escrita a quente dos params + passo DKMS p/ formatos
  empacotados), `packaging/debian/{control,postinst}`, `scripts/check_packaging_parity.sh`
  (o próprio gate: .spec entrou no bloco de paridade de modprobe.d — antes ficava FORA e uma
  remoção no .spec passava verde — e ganhou o bloco de paridade da cura DKMS).
- **testes** (todos falha-sem/passa-com, headless, ZERO skip):
  `tests/unit/test_dkms_hid_nintendo_assets.py` (dkms.conf campos exatos; Makefile kbuild;
  BASELINE sha256 recalculado do `.c` shipping; paridade reversa do patch; defaults
  250/25/2/2000/0/0 presentes no `.c`; string `exceeded max attempts` preservada; gate do [B]),
  `tests/unit/test_dkms_lib.py` (`bash -n`; fail-safe: PATH sem dkms → return 0 + aviso;
  headers ausentes simulados → return 0; nunca chama modprobe/rmmod — grep negativo; execução
  de ponta a ponta com dkms stub: idempotência real da 2ª chamada, build falho pula install,
  remove falho preserva registro/source e sobrevive a set -e),
  `tests/unit/test_install_dkms_default.py` (DKMS por DEFAULT sem flag; `--no-dkms` é opt-out;
  uninstall simétrico: dkms remove + rm da conf; ativação só anunciada com staging REAL;
  paridade de packaging da cura DKMS),
  `tests/unit/test_doctor_hid_nintendo_signatures.py` (assinatura probe -110 e exceeded-denso
  presentes no doctor; `[JOYCON-PROBE]` no storm_watch; mensagem sem o falso "boot/replug").

## Riscos e limites honestos

1. **Ativação só no próximo boot** com módulo in-tree carregado (replug NÃO troca módulo
   carregado) — install avisa e NUNCA recarrega (Pro/8BitDo em uso; regra inviolável).
2. **Driver congela no v7.0.11**: fixes futuros do in-tree não entram até rebase manual
   (estratégia acima; doctor avisa quando o DKMS não construiu p/ o kernel corrente).
3. **Secure Boot**: se ativo sem MOK, o módulo não-assinado não carrega → in-tree continua
   (fail-safe) — mesma situação do nvidia DKMS desta máquina (que funciona ⇒ assinatura MOK/SB
   já resolvida aqui); doctor pode conferir `mokutil --sb-state` (best-effort).
4. **O patch não impede o link BT de cair sob EMI** (isso é a Onda W): ele cura a morte por
   probe na reconexão, para de piorar a degradação (TX suprimido) e torna tudo
   mensurável/ajustável. A validação A/B ao vivo (T2.4) continua obrigatória.
5. **`-EAGAIN` novo é interno**: send_sync converte p/ `-ETIMEDOUT` (semântica de erro externa
   idêntica à atual); rumble worker silencia o drop. Nenhum consumidor fora do driver vê código
   de erro novo.
6. **Params em 0644 são poder de root**: valores absurdos são clampados no uso (1..1000 attempts,
   1..10 tries, 0..10 retries); `input_report_wait_ms=0` vira busy-ish loop de warns — documentar
   no doctor "não mexa sem medição" (é ferramenta de diagnóstico, não knob de usuário).
7. **`journalctl -k` proibido** segue valendo p/ os checks novos (usar `_TRANSPORT=kernel`,
   armadilha documentada no sprint T0).
