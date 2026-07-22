# Patches do backport BlueZ (fora da árvore do repo)

O backport do BlueZ é construído FORA do repositório (a árvore-fonte completa do
BlueZ não é versionada aqui — só os `.deb` resultantes + `SHA256SUMS` ficam
cacheados em `~/.cache/hefesto-dualsense4unix/bluez-backport/`, e o `install.sh`
passo 3f instala de lá com verificação de hash). Este diretório versiona os
PATCHES próprios para provenance e reprodutibilidade (regra da casa: tudo
replicável por script).

## `bluez-hefesto-0001-input-keep-bond-on-virtual-cable-unplug.patch`

**BOND-KEEP-01** (22/07). Causa-raiz medida ao vivo: o Nintendo Switch Pro
Controller e o 8BitDo (modo Switch) emitem um HID **Virtual Cable Unplug** ao
desligar / perder o link. Desde o 5.85 (input BR/EDR migrou para o caminho
uhid), essa mensagem chega ao `profiles/input/device.c` e dispara
`device_remove_bonding()` → o bond é **apagado do disco** a cada queda,
forçando re-pareamento. O DualSense não emite → o bond sobrevive (por isso a
falha era específica dos controles Nintendo-class). Detalhes e fontes:
`docs/process/estudos/2026-07-22-pesquisa-pro-controller-bt-e-lightbar-keepalive.md`.

O patch mantém o bond por DEFAULT; `BLUEZ_HID_UNPLUG_REMOVES_BOND=1` no ambiente
do serviço restaura o comportamento stock. Só a remoção do bond muda — o
teardown do nó uhid e a limpeza da flag seguem idênticos.

## Receita do build (para o próximo bump)

Árvore-fonte: `~/.cache/hefesto-dualsense4unix/bluez-src-586/bluez-5.86/`
(upstream 5.86 + `debian/` do resolute; ver a receita do 5.86 na sprint
`2026-07-21-sprint-pesquisa-bluez-estabilidade.md`).

1. Colocar o `.patch` em `debian/patches/` e anexar o nome ao fim de
   `debian/patches/series`.
2. Bump em `debian/changelog` (ex.: `...~hefesto24.04.2`).
3. `dpkg-buildpackage -b -us -uc -j4` (o quilt aplica a série no build).
4. Verificar o binário: `strings usr/libexec/bluetooth/bluetoothd | grep BOND-KEEP`.
5. Copiar `bluez_*.deb`, `bluez-cups_*.deb`, `libbluetooth3_*.deb` para
   `~/.cache/hefesto-dualsense4unix/bluez-backport/` e regenerar `SHA256SUMS`
   (`sha256sum bluez_*.deb bluez-cups_*.deb libbluetooth3_*.deb > SHA256SUMS`).
6. Ajustar `_BZ_TARGET` no `install.sh` para a versão completa nova (o
   `dpkg --compare-versions ge` precisa distinguir .1 de .2 — um alvo "5.86"
   nu pularia o upgrade).
7. `./install.sh` (passo 3f detecta o upgrade e instala; o postinst do pacote
   reinicia o bluetoothd — única exceção à regra de não reiniciar o serviço).
