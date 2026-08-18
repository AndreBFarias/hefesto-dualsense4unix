# Mapa: a camada de sistema — instalação, udev, DKMS e empacotamento

- **Levantado em:** 26-27/07/2026
- **Escopo:** `install.sh` (2.318 linhas), `uninstall.sh` (1.341), `scripts/`,
  `assets/`, `packaging/`, `.github/workflows/`

## O que o instalador realmente é

`install.sh` não instala um aplicativo: **provisiona o host.** Ele toca
`/etc/udev/rules.d`, `/etc/modprobe.d`, `/etc/modules-load.d`,
`/etc/systemd/system`, `/etc/bluetooth`, `/etc/NetworkManager/conf.d`,
`/usr/local/lib`, `/usr/src` (DKMS), o cmdline do kernel via `kernelstub`, o
initramfs, o `apt` (backport do BlueZ) e ainda edita a configuração da Steam.

O formato do aplicativo (nativo, flatpak, appimage, deb) é **ortogonal**: quase
toda a camada de sistema roda em todos eles.

## Convenções invioláveis, presentes no código inteiro

- **Fail-safe total no DKMS** — nada aborta o install (`scripts/dkms_lib.sh:9-18`).
- **NUNCA `modprobe -r` ou reload de módulo carregado** — derrubaria controles e
  WiFi em uso.
- **NUNCA `systemctl restart bluetooth`** — a única exceção é o postinst do
  próprio pacote `bluez`.
- **Registro de posse** para reversão cirúrgica: `cmdline-owners.conf` e
  `broker-owner.conf`. O uninstall só remove o que tem o cabeçalho do projeto.

## Os passos que importam

| Passo | O que faz | Root |
|---|---|---|
| 2/11 | venv com `--system-site-packages`; **recria** se veio de pyenv ou se a minor version do sistema mudou por dist-upgrade | apt |
| 3/11 | udev: lista de regras **derivada por glob**, excluindo a 75 | sim |
| 3c | quirk de áudio em `modprobe.d`, com post-check honesto se não persistir | sim |
| 3d | BT no máximo: sem autosuspend do `btusb`, `FastConnectable` e `JustWorksRepairing` por drop-in ou bloco sentinelado reescrito por `awk` idempotente. **Sem restart do bluetoothd** | sim |
| 3e | cmdline gerenciado: merge no token único `usbcore.quirks=`, com guarda anti-reintrodução e registro de dono. Com GRUB apenas **avisa** | sim |
| 3f | backport do BlueZ 5.86, com **SHA256SUMS obrigatório** e `VERSOES-ANTERIORES.txt` para reverter | sim |
| 3i-3k | três módulos DKMS | sim |
| 3l | flush **único** do initramfs | sim |
| 7a/11 | copia, habilita e **reinicia** a unit do daemon — passo criado porque o uninstall a removia e o install nunca a instalava | não |
| 11/11 | Steam Input desligado por padrão + guarda `.path` e `.timer` | não |

**Sudo adquirido uma vez**, com keepalive em segundo plano — a build do applet
COSMIC passa de 10 minutos e estouraria o `timestamp_timeout`.

## Os três módulos DKMS

Todos com `DEST_MODULE_LOCATION[0]="/updates/dkms"` (vence o in-tree por
`depmod.d`) e `PACKAGE_VERSION` fixo de propósito — bump deixaria dois `.ko`
candidatos.

### `hefesto-hid-nintendo` — quatro patches
1. **Não transmitir após esgotar o rate limit** + retry com backoff **só em BT**
   — cura o probe `-110` que mata o Pro e o 8BitDo sem re-probe.
2. **Registrar os LEDs mesmo com o SET inicial falhando**, para uma escrita
   posterior curar os LEDs de jogador.
3. **Clone 8BitDo pelo cabo**: padding do output report `0x80` para 63 bytes,
   handshake de status, e probe que **degrada** em vez de largar o device sem
   driver.
4. **Parar de esperar controle mudo.** Cada subcomando custava 4x25x500 ms = 50 s
   segurando o mutex de saída, a cada escrita de LED. Antes: 500 linhas em 251 s.
   Depois: 3 linhas, zero.

### `hefesto-hid-playstation` — dois patches
1. **Retry de feature reports** na probe. Diagnóstico completo no cabeçalho: com
   dois DualSense pareando com ~1 s de diferença, o segundo perde o canal L2CAP;
   passaram **3,26 s** contra os 5 s de espera do uhid, e quem estourou foi o
   **BlueZ** (`REPORT_REQ_TIMEOUT` de 3 s). O `-5` era máscara: o uhid achata
   qualquer erro de transporte.
2. **Clone 8BitDo em modo PS4 pelo cabo**: responde 9 bytes onde o driver pede 16
   no report `0x12`. **Dos 16, o driver usa 7.** Por BT esse report nem é lido — o
   endereço vem do pareamento. Ambos os interruptores nascem **desligados**.

### `hefesto-rtw88-usb` — dois patches
Backport upstream de vazamento de memória (CVE-2026-63821) e detecção de
device-gone portada do rtw89.

**Pino de ABI:** `BUILD_EXCLUSIVE_KERNEL="^7\.0\.11-76070011-"`. Fora desse build
exato o DKMS **pula** — o layout de `struct rtw_dev` é congelado num header local
e um respin da mesma versão linkaria limpo e corromperia memória.

### Nota de método do próprio README do pacote
**`srcversion` não serve para conferir proveniência** — não é reprodutível entre
build in-tree e out-of-tree. O juiz da identidade do fonte é o `sha256` do `.c`.

### INITRAMFS-01
O juiz de "defasado" é o **mtime** do `.ko` contra a imagem — fix do bug que
reescrevia 141 MB em `/boot` a cada reexecução. E existe o aviso de Secure Boot:
com MOK não enrolada, o kernel recusa o `.ko` e **não** cai no in-tree.

## As regras udev e a ordem que importa

**Descoberta não-óbvia:** o `systemd-logind` só converte `TAG+="uaccess"` em ACL
para regras numeradas **abaixo de 73** — é o `73-seat-late.rules` quem faz a
conversão. A regra do `/dev/uhid` já esteve numerada 79 e o nó nascia root-only.

**E a corrida perdida ao vivo (VPAD-09):** a ACL do `uaccess` é aplicada **no
login**, no mesmo instante em que o daemon de sessão sobe. Cura: `GROUP="hefesto"`
(grupo dedicado, **nunca** `input`, que seria primitiva de keylogger), aplicado
pelo udev na criação do nó — determinístico.

| Regra | Papel |
|---|---|
| 70 | hidraw do DualSense (USB, BT e o vpad), `0660` + `uaccess` |
| 71-uinput / 71-uhid | **abaixo de 73 obrigatoriamente** |
| 72 | autosuspend do DualSense USB |
| 75 | **opt-in**: `authorized=0` na interface de áudio |
| 76 | touchpad fora do libinput |
| 77 / 79 | LEDs graváveis (DualSense / externos) |
| 78 / 80 | Motion Sensors não são joystick |
| 81 (x2) | energia por device **e no host xHCI** — economia no controlador derruba o barramento inteiro |
| 82 | tira o Pro **genuíno** do sniff; escopo estreito porque o clone **precisa** do sniff |
| 83 | snapshot de bonds na borda da conexão |
| 84 | separa Pro genuíno do clone por `bcdDevice` |

Sete `udevadm trigger` seletivos, incluindo **`misc`** — sem ele as regras 71
só valeriam no próximo boot.

## Unidades systemd

**Sistema:** broker (socket-activated, `Type=notify`, endurecimento pesado com
`ProtectSystem=strict`, `PrivateNetwork`, `SystemCallFilter`, `DevicePolicy=closed`),
agente BT, snapshot de bonds e watchdog de saúde. Drop-in no `bluetooth.service`
com `Restart=on-failure` e `WatchdogSec=30`.

O render dos placeholders de uid/grupo **retorna erro sem escrever nada** se
sobrar placeholder, e aborta se o uid resolver 0 — um broker com uid 0
autorizaria só root.

**Usuário:** o daemon (enable + restart), a GUI no início da sessão (opt-in,
padrão não), o kernel-watch e os três do guarda de Steam Input.

## O uninstall é simétrico, e há teste provando

`tests/unit/test_uninstall_simetrico_ao_install.py` compara o glob de
`assets/*.rules` contra as regras citadas **dentro de um `rm -f`** do uninstall —
distingue "remove" de "avisa que preserva".

**Reverte por padrão:** daemon, units de usuário, ícones nas 11 resoluções,
applet, drop-ins do WirePlumber (**com preservação** se o cabeçalho indicar
edição manual), 17 regras udev, grupo, DKMS com parâmetros devolvidos a quente,
BlueZ (inclusive a link policy — que exige **vírgula**, porque com espaços o
`hciconfig` lia só o primeiro token e a reversão era no-op silencioso), Proton,
Steam.

**Não reverte:** config e perfis (padrão `--keep-config`), o quirk de cmdline,
pacotes do sistema, Proton extraído, logs.

**Ordem obrigatória documentada:** `proton_pin --unlock` **antes** do strip das
Launch Options, porque o strip reabre a Steam e o unlock exige fechada.

## CI

| Job | Gate |
|---|---|
| `anonymity` | `check_anonymity.sh` + `check_test_data.sh` |
| `acentuacao` | **ubuntu-22.04 / Python 3.11** |
| `version-check` | 6 alvos versionados contra o `pyproject` |
| `lint-test` | matriz 3.10/3.11/3.12: ruff, `pytest tests/unit`, `pytest tests/core` |
| `typecheck` | `mypy --strict` |
| `runtime-smoke` | matriz transporte x ambiente gráfico; falha se o log tiver `Traceback` |
| `smoke-multi-distro` | fedora e arch **continue-on-error**; debian-12 é gate duro |

Workflow dedicado de anonimato audita o **range de commits** — mensagens,
trailers e e-mails de autor — como required check server-side, para pegar quem
usou `--no-verify` local.

**Honestidade registrada no próprio YAML:** os testes de GUI **pulam** no CI, e o
comentário diz *"não finja que está coberto"*. O recuo foi consciente e
registrado em vez de mascarado.

## Empacotamento

| Formato | Estado |
|---|---|
| `.deb` | **Maduro.** venv bundlado; smoke de install **e remove** no release |
| Flatpak | **Maduro.** `--device=all` porque `input` não cobre `/dev/hidraw*`; a ativação real é `install-host-udev.sh` rodado do host |
| AppImage | Funcional; o release publica só o de CLI |
| Arch / Fedora | Completos em conteúdo, **não publicados** |
| Nix | **Incompleto** — `lib.fakeSha256` como placeholder |
| Applet COSMIC | Funcional, opt-in; **não compilado no CI** |

## Achados registrados como dívida

Todos materializados em
`sprints/2026-07-26-PROMESSA-NAO-CUMPRIDA-01-...`:

1. `scripts/install_fonts.sh` existe e **`install.sh` não o chama** — a janela
   nunca teve a tipografia do desenho.
2. `assets/hefesto-dsx-recover.service` é **órfão**: removido pelo uninstall,
   instalado por ninguém.
3. `--help` truncado por `sed -n '2,128p'`; `--no-snd-quirk` invisível;
   `install.sh:1073` sugere uma flag que aborta com código 2.
4. Regras 82, 83 e 84 **não empacotadas** no PKGBUILD nem no spec do Fedora.
5. `check_packaging_parity.sh` (312 linhas) **não roda em workflow nenhum**.
6. Janela de ordem: as regras 82 e 83 chegam antes dos scripts que invocam.
