# O delta da máquina limpa — o que só existe NESTA máquina

**11/08/2026.** Auditoria e medição. Nada foi consertado, nada foi instalado,
nada foi removido: só leitura do sistema vivo e do instalador.

A régua é a dela, fixada em 07/08 (resposta 17 do painel de decisões,
[docs/process/2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md](2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md)):
*"produto — tem que funcionar em máquina limpa"*. A pergunta que este documento
responde é uma só: **um PC novo, igual a este, rodando só `install.sh`, o que
NÃO recebe?**

Continua o **F-7** e a **LEVA C** de
[2026-08-09-A-NOITE-DOS-QUATRO-INVENTARIOS-01-o-que-a-casa-sabe-e-o-que-o-produto-faz.md](sprints/2026-08-09-A-NOITE-DOS-QUATRO-INVENTARIOS-01-o-que-a-casa-sabe-e-o-que-o-produto-faz.md)
e de
[2026-08-08-INDICE-a-madrugada-em-que-o-produto-era-o-reu.md](sprints/2026-08-08-INDICE-a-madrugada-em-que-o-produto-era-o-reu.md),
agora com número: quais passos, quais linhas, e o que a medição derrubou.

---

## O veredito em três linhas

1. **A suspeita mais grave era falsa.** Os três módulos DKMS e os onze
   parâmetros ligados agora estão **inteiros no repositório**. Não há
   parâmetro ligado à mão nesta máquina e escrito em lugar nenhum. Medido,
   arquivo por arquivo, byte por byte.
2. **O buraco de verdade é o BlueZ.** Esta máquina roda 5.86; um PC novo roda
   5.72, e o instalador **não consegue mais entregar o 5.86 nem aqui** — o
   cache de onde ele lê os `.deb` não existe mais nesta máquina.
3. **O F-7 tem tamanho medido:** fora do formato `native`, o instalador entrega
   **8 passos de 46**.

---

## A tabela do delta

Ordenada por **o que quebra primeiro** num PC novo. `native` é o formato
padrão; `pkg` abrevia `deb`/`flatpak`/`appimage`.

| # | O que existe aqui | O `install.sh` entrega? | Formatos | Gravidade |
|---|---|---|---|---|
| D-1 | `bluez` 5.86 (backport da casa) | **NÃO** — o cache dos `.deb` não existe nem aqui | nenhum | **BLOQUEIA** |
| D-2 | 15 regras udev, config do BlueZ, cmdline, bt-agent, vigias, fontes, Proton, Steam | Só em `native` (o resto sai por `install.sh:1147`) | `native` | **BLOQUEIA** em `pkg` |
| D-3 | Applet COSMIC nativo em `/usr/local/bin` (23 MB) | Só se `cargo` já existir na máquina | `native` | DEGRADA |
| D-4 | `pcie_aspm=off` no cmdline | **NÃO** — fora do escopo declarado | nenhum | DEGRADA |
| D-5 | `usbcore.autosuspend=-1` + `usbcore.quirks=...` ativos AGORA | Sim, mas só vale **no próximo boot** (e só com `kernelstub`) | `native` | DEGRADA no 1º uso |
| D-6 | `libopus0` + `pulseaudio-utils` (microfone por BT) | Sim, **perguntando** — e só em `native` | `native` | DEGRADA |
| D-7 | `bluez-tools` (fornece o `bt-agent`) | Sim, e só em `native` | `native` | DEGRADA em `pkg` |
| D-8 | Fontes `space-grotesk` + `jetbrains-mono` | Sim, e só em `native` | `native` | COSMÉTICO em `pkg` |
| D-9 | 4 perfis dela + histórico + `steam_input_apps.txt` + 9 flags | **NÃO**, e está certo — é dela | — | NÃO É DEFEITO |
| D-10 | 2 perfis semeados que ela **apagou** aqui | Sim — voltam no PC novo | todos | ATRITO |
| D-11 | 43 `.bak` de `/etc/bluetooth/main.conf` | São resíduo de ciclos daqui | — | NÃO É DEFEITO |
| D-12 | 60 MB de capturas `btmon` em `/var/lib/` | **NÃO** (captura forense nunca é ligada por default) | — | ATENÇÃO (contêm endereços reais) |

O que **NÃO** é delta, medido e conferido, para ninguém refazer o caminho:
os três módulos DKMS e seus parâmetros (§1), as quatro `.conf` de
`/etc/modprobe.d`, as 15 regras udev em `native`, o broker root, o teclado na
tela (`wvkbd`), o drop-in do WirePlumber, e o `input.conf` do BlueZ.

---

## 1. Os módulos DKMS — a bomba que não existe

Era a suspeita mais grave da encomenda: um parâmetro ligado à mão aqui e
escrito em lugar nenhum. **Medido: não há.**

### 1a. Os três fontes estão versionados e batem com o disco

`dkms status` nesta máquina:

```
hefesto-hid-nintendo/1.0.0,   7.0.11-76070011-generic, x86_64: installed
hefesto-hid-playstation/1.0.0, 7.0.11-76070011-generic, x86_64: installed
hefesto-rtw88-usb/1.0.0,      7.0.11-76070011-generic, x86_64: installed
```

`diff -rq` de `assets/dkms/<mod>/` contra `/usr/src/hefesto-<mod>-1.0.0/`, nos
três: **nenhum arquivo difere**. A única assimetria é estrutural e esperada —
`LICENSES/` só existe no `/usr/src` (o `dkms_lib.sh` o cria no build) e
`patch/` só existe no `assets` (é insumo, não vai para o build).

Os três `.ko` carregados agora vêm de `updates/dkms`, não do in-tree
(`modinfo -n` confirma nos três), e `/etc/depmod.d/ubuntu.conf` diz
`search updates ubuntu built-in` — a precedência é a que o `dkms.conf`
documenta.

O instalador instala os três, e **em todo formato**: `install.sh:1953` (3i,
hid-nintendo), `install.sh:1972` (3j, rtw88-usb), `install.sh:1986` (3k,
hid-playstation) no caminho `native`; e `install.sh:1092`, `install.sh:1097`,
`install.sh:1101` dentro do bloco não-`native`. Opt-out compartilhado
(`--no-dkms`), nunca opt-in.

### 1b. Os onze parâmetros do `hid_nintendo`, um a um

Coluna "default no fonte" lida em `assets/dkms/hid-nintendo/hid-nintendo.c`,
linhas 52 a 110. Coluna "conf" lida em
`assets/modprobe.d/hefesto-hid-nintendo.conf` (última linha, `options`).

| Parâmetro | Vivo agora | Default no fonte | Na conf versionada? |
|---|---|---|---|
| `bt_probe_retries` | 3 | 0 | sim, `=3` |
| `skip_tx_on_rate_exceeded` | Y | 0 | sim, `=1` |
| `register_leds_on_set_failure` | Y | 0 | sim, `=1` |
| `sync_send_tries` | 4 | 2 | sim, `=4` |
| `input_report_wait_ms` | 500 | 250 | sim, `=500` |
| `probe_info_timeout_ms` | 4000 | 2000 | sim, `=4000` |
| `usb_cmd_pad_to_report` | Y | 0 | sim, `=1` |
| `usb_send_conn_status` | Y | 0 | sim, `=1` |
| `usb_probe_degrade` | Y | 0 | sim, `=1` |
| `subcmd_silence_streak_max` | 3 | 0 | sim, `=3` |
| `subcmd_rate_max_attempts` | 25 | **25** | não precisa — é o default |

Dez dos onze estão escritos; o décimo primeiro está no valor do próprio fonte.
**Zero órfãos.**

`hid_playstation`: `feature_retries=1`, `ds4_short_pairing_info=Y`,
`ds4_synthetic_mac=Y` — os três na conf versionada, os três com default 0/N no
fonte (linhas 30, 73 e 78 de `assets/dkms/hid-playstation/hid-playstation.c`).

`rtw88_usb`: `hang_reset=Y` e `switch_usb_mode=Y`. **Não há e nem precisa haver
`modprobe.d` para o rtw88** — os dois nascem `true` no próprio fonte do fork
(`assets/dkms/rtw88-usb/usb.c:18` e `:23`), e o instalador diz isso por escrito
em `install.sh:837`.

### 1c. As quatro `.conf` de `/etc/modprobe.d` são cópia exata do repositório

`diff` de cada uma contra o `assets`, todas **idênticas**:

| Arquivo em `/etc/modprobe.d/` | Origem versionada | Passo que instala |
|---|---|---|
| `hefesto-hid-nintendo.conf` | `assets/modprobe.d/` | `install.sh:658` |
| `hefesto-hid-playstation.conf` | `assets/modprobe.d/` | `install.sh:746` |
| `hefesto-btusb-no-autosuspend.conf` | `assets/modprobe.d/` | `install.sh:1500` |
| `hefesto-dualsense-storm.conf` | `assets/modprobe/` | `install.sh:1412` (e `install.sh:1075` em `pkg`) |

### 1d. O único risco real do DKMS numa máquina nova

`assets/dkms/rtw88-usb/dkms.conf:30` carrega
`BUILD_EXCLUSIVE_KERNEL="^7\.0\.11-76070011-"`. Um PC **igual a este** passa;
um PC com kernel diferente não constrói o rtw88, e o instalador degrada com
aviso honesto (`install.sh:1970`, `install.sh:863`) sem abortar. Os outros dois
não têm pino de kernel. Isto não é defeito — é a decisão escrita —, mas é a
linha que muda se um dia o PC novo não for igual.

**Onde mudaria (se mudasse):** `assets/dkms/rtw88-usb/dkms.conf:30`.

---

## 2. D-1 — o BlueZ 5.86 não é reprodutível em lugar nenhum

Este é o item mais grave da auditoria, e ele **já está quebrado nesta máquina**,
não só na nova.

Medido aqui:

```
bluez           5.86-0ubuntu0.1~hefesto24.04.3
bluez-cups      5.86-0ubuntu0.1~hefesto24.04.3
libbluetooth3   5.86-0ubuntu0.1~hefesto24.04.2
```

`apt-cache policy bluez` mostra que o repositório só oferece `5.72-0ubuntu5.5`
e `5.72-0ubuntu5`. O 5.86 **não vem de repositório nenhum** — é um backport
local.

O passo que o entregaria é o **3f** (`install.sh:1779`). Ele lê os `.deb` de
`${HOME}/.cache/hefesto-dualsense4unix/bluez-backport` (`install.sh:1801`),
confere SHA256SUMS e instala. **Esse diretório não existe nesta máquina.**
Medido: `ls` retorna "Arquivo ou diretório inexistente". Ou seja, mesmo aqui,
hoje, rodar `./install.sh` de novo não reaplicaria o backport — cairia no
`warn "backport não encontrado"` de `install.sh:1808`.

A receita para regerar os `.deb` **vivia fora da árvore de trabalho**, num ramo
arquivado (`arquivo/processo-pre-1.0`), e o instalador mandava rodar
`git show arquivo/processo-pre-1.0:...` — um comando que numa máquina nova não
tem como funcionar, porque o ramo não vem no clone. Pior: o `install.sh` já
citava o documento pelo caminho da árvore, **como se ele estivesse aqui**.

> **CURADO no mesmo dia (11/08/2026), depois desta auditoria.** O estudo foi
> recuperado para
> [estudos/2026-07-19-estudo-bluez-backport-onda-r.md](estudos/2026-07-19-estudo-bluez-backport-onda-r.md),
> as mensagens do `install.sh` e do `doctor.sh` passaram a apontar para o
> caminho real, e `tests/unit/test_receita_do_backport_esta_na_arvore.py`
> reprova se alguém devolver a instrução impossível. **O que continua de pé é o
> resto do defeito:** a receita existe, os `.deb` não. Um PC novo ainda fica com
> `bluez` 5.72 — só que agora com um caminho a seguir, em vez de um beco.

**Consequência medida, e ela é um FAIL:** o `doctor.sh` ganhou faixa de duas
pontas (`scripts/doctor.sh:2451-2452`, piso 5.79 e teto 5.87). O veredito de
5.72 é `old`, e `old` é **`fail`** — `scripts/doctor.sh:2487`. Num PC novo,
logo após o `install.sh`, o doctor reprova por aqui. E a mensagem de reprovação
manda o usuário para o mesmo cache que não existe — e a mensagem, essa, foi
corrigida em 11/08 para ao menos dizer onde está a receita.

**Onde teria de mudar (sem mudar):** `install.sh:1801` (a origem dos `.deb`) e
`install.sh:1808` (o que se faz quando não há cache). O que falta é o
instalador **saber gerar** os pacotes, ou trazê-los de algum lugar — hoje ele
só sabe consumi-los de um cache que ninguém enche.

---

## 3. D-2 — o F-7 medido: 8 passos de 46 fora do `native`

O portão está em `install.sh:1062` (`if [[ "${FORMAT}" != "native" ]]`) e o
`exit 0` em `install.sh:1147`. Li o bloco inteiro. Um `pkg` recebe **exatamente
estes oito**:

| Passo | Linha | O que faz |
|---|---|---|
| `cura` | `install.sh:1075` | quirk do `snd_usb_audio` (storm) |
| `broker` | `install.sh:1087` | broker root hide-hidraw |
| `dkms` | `install.sh:1092` | hid-nintendo |
| `dkms-w` | `install.sh:1097` | rtw88_usb |
| `dkms-p` | `install.sh:1101` | hid-playstation |
| `dkms-i` | `install.sh:1106` | initramfs |
| `osk` | `install.sh:1112` | teclado na tela |
| `mic` | `install.sh:1132`/`:1024` | WirePlumber |

E **não** recebe, entre outros: as regras udev (passo 3/11,
`install.sh:1308`), o Bluetooth no máximo com a config do BlueZ e o
`modprobe.d` do `btusb` (3d, `install.sh:1495`), o cmdline (3e,
`install.sh:1589`), a resiliência do `bluetoothd` — drop-in, watchdog e
snapshot de bonds (3e-bis, `install.sh:1709`), o backport (3f,
`install.sh:1779`), o agente de pareamento (3g, `install.sh:1890`), as fontes
(`install.sh:2258`), o `libopus0` (`install.sh:1253`), o Proton pinado (11c,
`install.sh:2832`) e o desligamento do Steam Input (11/11,
`install.sh:2714`).

**Uma correção honesta ao que se supunha:** o `.deb` **não** fica sem regras
udev. O `scripts/build_deb.sh:176-183` copia todas as regras de `assets/` para
`/usr/lib/udev/rules.d/` dentro do pacote, e ainda embala o
`install-host-udev.sh` (`scripts/build_deb.sh:192`) e os fontes DKMS
(`scripts/build_deb.sh:267`, `:285`). Quem fica sem udev é
**flatpak e appimage** — conferido: `flatpak/br.andrefarias.Hefesto.yml` não
menciona regra nenhuma, e nem poderia (sandbox não escreve em `/etc`).

**Consequência medida no doctor**, num flatpak/appimage recém-instalado:
`check_udev` (`scripts/doctor.sh:145`) conta 0 de 15 e **reprova**
(`scripts/doctor.sh:198`); `check_input_uaccess`
(`scripts/doctor.sh:549`) **reprova** em `scripts/doctor.sh:552` — e a
mensagem dela já diz a frase inteira: *"numa máquina nova, não funcionam"*.

**Onde teria de mudar (sem mudar):** `install.sh:1062` (o portão) e
`install.sh:1147` (o `exit 0`).

---

## 4. D-3 — o applet COSMIC depende de um `cargo` que ninguém instala

Aqui existe `/usr/local/bin/hefesto-dualsense4unix-applet`, 23 652 192 bytes,
de 10/08.

Quem o constrói é `install_cosmic_applet` (`install.sh:2569`), e a primeira
coisa que ele faz é `command -v cargo` e `command -v just`
(`install.sh:2571`). Medido nesta máquina:

- `just` 1.42.4 vem do **apt** (`just 1.42.4-1pop1~...~24.04~dd64d0b`) — um PC
  novo do mesmo Pop teria;
- `cargo` 1.97.1 está em `/home/<usuária>/.cargo/bin/cargo`, ou seja **rustup,
  instalado à mão**. Não há passo nenhum do `install.sh` que instale rustup.

Num PC novo: `install.sh:2572` avisa, imprime as instruções manuais
(`install.sh:2574-2577`, inclusive os sete `-dev` que ele **não** instala,
apenas nomeia) e `return 0` — o install segue e termina "com sucesso" sem
applet. O `doctor.sh` classifica isso como `warn`, não `fail`
(`scripts/doctor.sh:670`).

Ela usa COSMIC. O applet é o que aparece no painel dela. Num PC novo ele
simplesmente não nasce.

**Onde teria de mudar (sem mudar):** `install.sh:2571-2578`.

---

## 5. D-4 e D-5 — o cmdline

O cmdline vivo desta máquina tem, além do que o Pop põe sozinho:

```
mitigations=off  usbcore.autosuspend=-1  acpi_enforce_resources=lax
pcie_aspm=off    usbcore.quirks=054c:0ce6:gn,054c:0df2:gn
```

O produto é dono de **dois** desses cinco:
`src/hefesto_dualsense4unix/integrations/kernel_cmdline.py:31-34` declara
`usbcore.autosuspend=-1` e os dois IDs de `usbcore.quirks`, e o passo 3e
(`install.sh:1589`) os aplica por `kernelstub`.

Três achados, todos medidos:

**D-4 — `pcie_aspm=off` não tem dono no produto.** Está declarado fora de
escopo em `docs/adr/018-usb-power-scope-vs-dropout.md:102`, e o estudo de
07/08 (`docs/process/estudos/2026-08-07-a-economia-de-energia-e-a-bancada.md:263`)
atribui a autoria a ela, não ao instalador. Um PC novo não recebe. O estudo
também registra (linha 105) que o `sysfs` **mente** sobre isso: com
`pcie_aspm=off` o `/sys/module/pcie_aspm/parameters/policy` continua exibindo
`[default]` — então nem o `check_pcie_aspm` do doctor
(`scripts/doctor.sh:1960`) pode dizer com certeza que falta.

**D-5a — nesta máquina o instalador não é dono nem dos dois que gerencia.**
`~/.local/state/hefesto-dualsense4unix/cmdline-owners.conf` tem, literalmente,
duas linhas: `cmdline.usbcore.autosuspend=terceiro` e
`cmdline.usbcore.quirks=terceiro`. Ou seja: quando o instalador olhou, os
tokens **já estavam lá** por mão de fora, e ele registrou isso em vez de
reivindicar. Num PC novo ele os escreveria com dono `hefesto`. O comportamento
é o desenhado; o registro é a prova de que esta máquina e a nova não passam
pelo mesmo ramo do código.

**D-5b — no PC novo, o cmdline não vale no dia do install.** `install.sh:1677`
diz, na própria mensagem: *"vale no PRÓXIMO boot"*. Então um PC novo, entre o
fim do `install.sh` e o primeiro reboot, roda **sem** `usbcore.autosuspend=-1`
— justamente a alavanca contra o controle dormindo. E se o bootloader for
GRUB em vez de `kernelstub`, `install.sh:1657` **só avisa** e pede edição
manual de `GRUB_CMDLINE_LINUX_DEFAULT`: nunca escreve.

Note ainda que o quirk de áudio (passo 3b, `install.sh:1392`) é **opt-in**
(`--with-usb-quirk`), enquanto o 3e é default e funde os mesmos IDs — os dois
caminhos existem e só um é automático.

**Onde teria de mudar (sem mudar):** `install.sh:1657` (o ramo GRUB),
`install.sh:1677` (o aviso de próximo boot) e
`src/hefesto_dualsense4unix/integrations/kernel_cmdline.py:31-34` (a lista de
tokens, se `pcie_aspm` entrar).

---

## 6. D-6, D-7, D-8 — os pacotes

Instalados aqui, e o que o instalador garante:

| Pacote | Versão aqui | O `install.sh` instala? | Onde | Formato |
|---|---|---|---|---|
| `bluez` | 5.86 (backport) | **não** (D-1) | `install.sh:1779` | — |
| `bluez-tools` | 2.0~20170911 | sim, se faltar | `install.sh:1895` | `native` |
| `libopus0` | 1.4-1build1 | sim, **perguntando** | `install.sh:1253-1269` | `native` |
| `pulseaudio-utils` | (via `pactl`) | idem | `install.sh:1255` | `native` |
| `wvkbd` | 0.14.3-1 | sim | `install.sh:1112` / `:2188` | **todos** |
| `just` | 1.42.4-1pop1 | não (só nomeia) | `install.sh:2575` | — |
| `fonts-space-grotesk-ttf` | 2.0.0-0ubuntu2 | sim | `install.sh:2258-2275` | `native` |
| `fonts-jetbrains-mono` | 2.304+ds-4 | sim | `install.sh:2258-2275` | `native` |

Dois detalhes que só a leitura do trecho revela:

- **`libopus0` é uma pergunta, não uma garantia.** `install.sh:1258` chama
  `ask_yn` com default `y`; num install `--yes` passa, num install interativo
  ela pode dizer não e o `mic bt` fica indisponível — sem que nada reprove.
- **`wvkbd` é o único que atravessa todo formato**, e o instalador grava uma
  sentinela (`~/.local/state/hefesto-dualsense4unix/teclado-na-tela.conf`) para
  distinguir "o install não instalou" de "ela removeu depois". Nesta máquina a
  sentinela diz `resultado=ja-instalado`, `pacote=wvkbd`, `gerenciador=apt`. Num
  PC novo diria `instalado`. É o desenho certo, e é o modelo que os outros itens
  desta tabela **não** seguem.

---

## 7. D-9 e D-10 — a config dela

`~/.config/hefesto-dualsense4unix/`. O que o produto semeia está listado no
próprio disco, em `profiles/.seeded_presets` (12 nomes), e bate exatamente com
os 12 arquivos de `assets/profiles_default/`.

**Perfis que só existem aqui** (dela, criados na interface — um PC novo não os
terá, e isso não é defeito): `big_walk.json`, `dont_scream.json`,
`pragmata.json`, `sackboy.json`. Mais o diretório `profiles/.historico/` (13
subdiretórios de versões anteriores) e `backup-20260726-233630/`.

**D-10 — o inverso, que é atrito de verdade:** dois perfis **semeados** foram
apagados aqui e sobrou só o `.lock` órfão — `meu_perfil.json` e
`sackboy_nativo.json`. Num PC novo eles **voltam**, porque a semeadura os
entrega. Ela vai reencontrar dois perfis que já tinha decidido não querer.
Sobraram ainda dois `.lock` sem dono de perfis renomeados
(`pragmata2.json.lock`, `vitoria.json.lock`).

**Flags e estado, tudo dela, nada semeado:** `active_profile.txt`,
`autoswitch_locked.flag`, `gamepad_disabled.flag`, `keyboard_emulation.flag`,
`mouse_emulation.flag`, `gui_preferences.json`, `controllers.json`,
`session.json`, `launch_dialog_dismissed.json`, e três marcas de migração
(`.coop_optout_migrated`, `.coop_default_on_migrated`, `.flavor_xbox_migrated`,
`.coop_local_match_migrated`, `.modo_jogo_nos_presets_migrated`).

**`steam_input_apps.txt`** (759 bytes) é **dela**, e conferi que o produto
nunca o semeia: em `src/` só há leitores
(`integrations/steam_launch_options.py:794`, `daemon/launch_env.py:585`,
`integrations/storm_doctor.py:50`) e um escritor acionado pela interface
(`app/actions/relancar.py:75`). Num PC novo a allowlist nasce vazia, e os
jogos cuja via oficial é o Steam Input voltam a passar pelo caminho errado até
ela reconstruir a lista à mão.

---

## 8. D-11 e D-12 — o que se acumulou aqui

**D-11.** `/etc/bluetooth/` guarda **43** arquivos `main.conf.bak.hefesto-*` e
`...-uninstall-*`, de 19/07 a 08/08, alguns com 14 a 16 KB (o `main.conf`
original inteiro). Cada ciclo de install/uninstall deixa mais um, e nada os
recolhe. Num PC novo haveria um ou dois. Não quebra nada; é ruído que só existe
aqui, e o dono do arquivo é `scripts/bluez_config.sh`.

O `main.conf` vivo tem um único bloco `hefesto` bem-formado
(`FastConnectable=true`, `JustWorksRepairing=confirm`) — o doctor passa nos
dois checks (`scripts/doctor.sh:2040` e `:2096`). O `input.conf` está no
default (só `[General]`), então `IdleTimeout` não aparece e o check passa.

**D-12 — e aqui há uma atenção de anonimato.**
`/var/lib/hefesto-dualsense4unix/` contém três capturas `btmon` de 22/07,
somando ~60 MB (`.snoop`). Elas **não** são criadas pelo `install.sh` — a
captura forense é declarada "NUNCA ligada por default" no próprio comentário do
passo 3e-bis. São insumo de medição dela. Um PC novo não as terá, e isso está
certo.

O ponto de atenção: **captura de HCI carrega endereços de rádio reais**. Elas
estão fora do repositório (em `/var/lib/`), então nenhum portão as vê — e
`scripts/check_anonymity.sh` não teria como. Se algum dia alguém as copiar para
dentro da árvore para "documentar", vaza. Registro aqui para que a decisão seja
consciente. **Não transcrevi nenhum endereço**, e não encontrei senha, chave ou
token em nada que li nesta auditoria.

Ainda em `/var/lib/hefesto-dualsense4unix/`: `bt-bonds/` (14 subdiretórios) e
`bt-bonds-protegidos/` — os snapshots do salva-vidas. São específicos dos
pareamentos desta máquina; num PC novo nascem vazios e se enchem sozinhos, o
que é o desenho.

---

## 9. O que o `doctor.sh` reprovaria num PC novo logo após o `install.sh`

Li as 33 condições de `fail` do `scripts/doctor.sh` e cruzei cada uma com o
estado que um PC novo teria. As que **reprovariam**:

| Check | Linha do `fail` | Em que formato | Por quê |
|---|---|---|---|
| `check_bluez_backport_version` | `scripts/doctor.sh:2487` | **todos**, inclusive `native` | 5.72 < piso 5.79, e o backport não tem como ser aplicado (D-1) |
| `check_udev` | `scripts/doctor.sh:198` | `flatpak`, `appimage` | nenhuma regra instalada (D-2) |
| `check_input_uaccess` | `scripts/doctor.sh:552` | `flatpak`, `appimage` | a regra 72-uaccess não existe |
| `check_launch_wrapper` | `scripts/doctor.sh:1467` | `flatpak`, `appimage`, `deb` | o wrapper é do passo 11b, `native` |
| `check_teclado_na_tela` | `scripts/doctor.sh:3145`/`:3149` | qualquer, se o apt falhar | sem rede ou sem `wvkbd` no repositório |

O único que reprova **no caminho padrão, num PC novo, com tudo dando certo**, é
o do BlueZ. Esse é o resultado central desta auditoria.

Reprovariam **também**, mas por estado de uso e não por instalação (portanto
não contam como delta): os checks de bond/SDP/órfão
(`scripts/doctor.sh:2293`, `:2582`, `:2625`, `:2703`, `:2735`), que num PC novo
sem nenhum pareamento nem chegam a rodar.

O `check_applet` (`scripts/doctor.sh:670`) e o `check_service`
(`scripts/doctor.sh:132`) dão **warn**, não fail — então o applet ausente
(D-3) não aparece como reprovação, aparece como aviso. Vale dizer com todas as
letras: **o doctor hoje dá um resultado quase verde para uma máquina sem
applet**, que é a tela dela.

---

## 10. O que eu NÃO consegui medir

Honestidade primeiro. Nada abaixo foi deduzido; foi deixado de fora.

1. **Não rodei o `install.sh` numa máquina limpa.** Toda a análise de "o que o
   PC novo recebe" é **leitura do código** do instalador, não execução. Onde a
   encomenda pedia para abrir o trecho, abri e citei a linha; mas ler não é
   provar. A prova é um ciclo real numa máquina virgem, e ele não foi feito.
   Este é o limite mais importante deste documento.
2. **Não medi o `uninstall.sh`.** A encomenda não pediu, e a simetria
   install/uninstall (a regra "toda cura entra no install, sem flag", 08/08)
   fica sem verificação aqui.
3. **Não sei se `just` está no repositório de um Pop!_OS recém-instalado.**
   Aqui ele veio como `1.42.4-1pop1~...`, o que sugere repositório do Pop, mas
   um PC recém-instalado pode ter conjunto de repositórios diferente do desta
   máquina (que tem histórico de PPAs). Não conferi `apt-cache policy just`
   contra uma lista de fontes limpa.
4. **Não conferi o conteúdo dos `.deb` do backport do BlueZ.** Eles não
   existem nesta máquina; só li o que o instalador espera deles. Não sei se a
   receita do ramo arquivado ainda constrói contra o `noble` de hoje.
5. **Não medi o caminho Arch nem o `.rpm`.** `packaging/arch/PKGBUILD` e o
   `spec` existem e o portão de paridade os cobre, mas esta auditoria olhou
   `native`, `deb`, `flatpak` e `appimage` — os quatro que o `install.sh`
   oferece.
6. **Não medi o efeito, só a presença**, em quase tudo. Que a regra udev está
   no disco eu medi; que a ACL nasceu no nó vivo, não — e o próprio doctor
   separa essas duas perguntas em funções distintas (`check_udev` contra
   `check_input_uaccess`), justamente porque a segunda engana.
7. **Não abri os 46 passos do `install.sh` um a um.** Abri os que a tabela
   cita, mais o bloco não-`native` inteiro. Passos entre 4/11 e 8/11 (atalho,
   symlink, daemon, hotplug, kernel-watch, tray do GNOME) não foram auditados
   contra máquina limpa.
8. **Não sei há quanto tempo o cache do backport sumiu**, nem se foi apagado à
   mão, por limpeza de `~/.cache`, ou por um `uninstall`. Medi que não está lá
   hoje.
9. **Não medi o estado de rede/repositório** — quantos dos passos que dependem
   de `apt` sobreviveriam a um PC novo sem internet no momento do install.
   Vários (`bluez-tools`, `libopus0`, fontes, `wvkbd`) degradam com aviso, mas
   não contei quantos nem testei.
