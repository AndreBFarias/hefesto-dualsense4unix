# Sprint SPRINT-INFRA-01 — o install garante, ou não é install

Pedido da mantenedora (2026-07-15): *"tudo deve funcionar via script install e afins"* /
*"A ideia é termos tudo fácil a nível de no install garantirmos o funcionamento de tudo."*

Regra da casa que este sprint faz valer: **se precisa de um passo manual, o instalador
está incompleto.** E a simétrica: **se o install aplica sem flag, o uninstall remove sem
flag.**

O instalador nativo é maduro (sudo cacheado com keepalive, udev canônico, cura do storm
por default com post-check, applet default-on, Steam Input desligado com guard). Os
furos abaixo são o que a auditoria encontrou — quase todos do mesmo tipo: **o install
promete e não entrega, em silêncio.**

## Prioridade 1 — Coisas que o install promete e não entrega

- `INFRA-01` — **Os formatos flatpak/appimage/deb saem cedo demais.** `install.sh:363` dá
  `exit 0` **antes dos steps 6-11** — então quem instala por pacote **não recebe**: o
  desligamento do Steam Input (o conflito clássico volta na hora: touchpad vira cursor,
  mic spam, botões em background), o applet COSMIC e o autostart.
  **Aceite**: instalar por `.deb`/Flatpak/AppImage entrega o mesmo conjunto do nativo, ou
  diz **exatamente** o que não deu e como completar. Teste por formato.

- `INFRA-02` — **A feature "abrir GUI ao plugar" está MORTA.** O prompt e a unit
  continuam (`install.sh:852`), mas as regras udev 73/74 que a disparavam **são deletadas
  pelo próprio `install_udev.sh`** (removidas em 2026-06-23 por causa do storm). Pior:
  habilitar a unit faz a GUI abrir **em todo login**.
  **Decidir e executar**: ou ressuscita o gatilho de um jeito que não realimente o storm
  (o `snd`-quirk já cura a causa-raiz — reavaliar), ou **remove o prompt e a unit**.
  **Aceite**: nenhum prompt oferece o que não existe.

- `INFRA-03` — **`/dev/uinput` e `/dev/uhid` sem permissão até o reboot.**
   **Corrigido nesta sessão** (`udevadm trigger --subsystem-match=misc --action=add`):
  os nós já existem quando as regras chegam, então sem o trigger a regra só valia no
  próximo boot — e sem ela **não há vpad nenhum**: co-op de 4 jogadores morto.
  Falta: **teste de regressão** que instale as regras com o módulo já carregado e afirme
  o `getfacl`.

- `INFRA-04` — **Paridade da regra `71-uhid.rules` nos seis caminhos.**
   **Corrigido nesta sessão**: native, `.deb` (glob `71-*`), Flatpak (manifesto), Arch
  (PKGBUILD), Fedora (`.spec`) e **Nix** (`package.nix`), mais `modprobe uhid` no
  `install-host-udev.sh` e o módulo no `modules-load`.
  Falta: estender o `check_packaging_parity` para cobrir **Arch/Fedora/Nix** — hoje ele só
  olha `assets/ × instaladores` (foi ele que pegou o Flatpak faltando, mas não veria os
  outros três).
  **Aceite**: o teste de paridade falha se **qualquer** formato ficar para trás.

- `INFRA-05` — **`doctor.sh` não sabia o que o install passou a fazer.**
   **Corrigido nesta sessão**: conhece a `71-uhid.rules` (4 canônicas), checa `/dev/uhid`
  e o driver `hid_playstation` (do qual dependem lightbar e player-LED por sysfs).
  E o `check_uinput` deixou de dar **falso positivo**: ele só olhava se o nó *existia* —
  dava `[OK] /dev/uinput presente` com o nó root-only e o daemon incapaz de criar vpad
  nenhum. Agora checa se é **gravável**, que é o que importa.
  Verificado ao vivo: `/dev/uhid` em 0600 → o doctor avisa e diz o que se perde; o
  `udevadm trigger --subsystem-match=misc` do install cura.
  Regra que fica valendo: **um item no install = um check no doctor**.

## Prioridade 2 — Coisas que o install faz e não devia

- `INFRA-06` — **Fecha a Steam (e o jogo aberto) sem perguntar**, no step 11, por default
  (`install.sh:1010`).
  **Aceite**: pergunta, ou espera, ou explica antes — nunca mata um jogo em andamento.

- `INFRA-07` — **Aceita flags contraditórias em silêncio**:
  `--with-usb-quirk` (intenção: **manter** o mic) junto de `--with-wireplumber-disable-mic`
  (**mata** o mic); quirk usbcore + regra 75 (áudio-off) documentados como "use uma OU
  outra" sem nada impedir a coexistência.
  **Aceite**: combinação contraditória **falha cedo** com uma frase que explica o conflito.

- `INFRA-08` — **O guard do Steam Input reverte escolha consciente.** Path unit + timer de
  30 min desligam o Steam Input **mesmo quando a pessoa o religou na Steam de propósito**,
  sem nenhuma pista de como parar isso.
  **Aceite**: o guard é desligável e diz como; ou só age quando o daemon está ativo.

- `INFRA-09` — **`FORCE_XWAYLAND` no `.desktop` derrota o opt-out.** O `GDK_BACKEND=x11`
  gravado no atalho vence o `HEFESTO_DUALSENSE4UNIX_NO_XWAYLAND=1` do `run.sh`.
  **Aceite**: um único dono da decisão de backend gráfico.

- `INFRA-10` — **`uninstall.sh` zera o `quirk_flags` inteiro do `snd_usb_audio`** em
  runtime (`uninstall.sh:325`) — **apaga os quirks de outros dispositivos** de áudio USB
  da máquina, que não são nossos.
  **Aceite**: remove **só** as entradas do DualSense (054c:*), preservando o resto.
   Mesma família: `uninstall.sh` não re-dispara o subsystem `misc`, então a ACL de
  `/dev/uhid` sobrevive à desinstalação.

## Prioridade 3 — Convivência e honestidade

- `INFRA-11` — **Native e `.deb` coexistem sem se detectarem**: duas units de daemon (user
  vs `/usr/lib`) e dois binários, com precedência silenciosa do `~/.config`.
  **Aceite**: o install detecta a outra instalação e resolve (ou recusa com instrução).

- `INFRA-12` — **O nativo prende a pasta do clone.** Guard do Steam Input, units e
  launcher apontam para o caminho do clone; **mover ou apagar a pasta quebra tudo** e
  ninguém avisou.
  **Aceite**: ou o install copia o que precisa para fora do clone, ou avisa em bom
  português que a pasta virou parte da instalação.

- `INFRA-13` — **O `--help` mente e corta.** A lista de flags é truncada na linha 42
  (`--with-wireplumber-fix`, `--with-wireplumber-disable-mic` somem); o `--yes` diz
  responder "sim a todos os prompts" e há prompts que ele não cobre; imprime
  `--disable-usb-audio`, que **o install.sh não aceita** (é flag do `install_udev.sh`).
  **Aceite**: `--help` lista o que existe, e só.

- `INFRA-14` — **`prerm` do `.deb` com pattern velho** (`hefesto\.app\.main` — o módulo foi
  renomeado): a GUI **não é encerrada** ao remover o pacote.
  **Aceite**: remover o `.deb` encerra o que ele iniciou.

- `INFRA-15` — **`~/.local/bin` pode não estar no PATH** e a instrução final manda rodar
  `hefesto-dualsense4unix` mesmo assim.
  **Aceite**: o install confere e, se faltar, diz o que fazer.

## Prioridade 4 — Bluetooth e a meta dos 4 controles

- `INFRA-16` — **O install não detecta nem orienta Bluetooth.** Para a meta de 4 controles
  (mistura USB+BT) não há nenhum passo que confira adaptador, pareamento ou o caso
  conhecido do **SDP HID ausente** (o "Connected: yes" sem hidraw/evdev, que já custou uma
  sessão inteira).
  **Aceite**: o install diagnostica o BT e, no caso SDP, dá a receita (remove + pair +
  trust + botão PS).

- `INFRA-17` — **`doctor.sh` assume UM controle**: o loop de localização USB sobrescreve
  `ds_dev` a cada match (o último vence) e o check de BT dá **PASS** só porque o controle
  "aparece no `bluetoothctl`" — o caso SDP-sem-hidraw passa como saudável.
  **Aceite**: `doctor.sh` reporta **cada** controle conectado, com transporte e saúde real
  (hidraw + evdev presentes), e detecta o SDP ausente.

- `INFRA-18` — **Escala das regras udev: verificado, está OK.** As regras 70/72/75/77/78
  casam por device (não por índice) e escalam para N controles sem limite. Não é bug — é a
  verificação que o `SPRINT-4P-01` pediu, registrada aqui para ninguém refazer.

## Validação (obrigatória)

Numa máquina limpa (ou container), por formato (`native`, `.deb`, Flatpak, AppImage):
instalar → **sem tocar em mais nada** → plugar 1 controle USB + 1 BT → jogar, vibrar,
mudar cor, co-op de 2 → `doctor.sh` verde → `uninstall.sh` → conferir que **nada** ficou
para trás (`/etc/udev/rules.d`, `/etc/modules-load.d`, `/etc/modprobe.d`, units, applet,
`quirk_flags` dos outros dispositivos intactos).

## Ordem

INFRA-01 e INFRA-02 (o install mente hoje) → INFRA-04/05 (fechar a paridade e o doctor) →
INFRA-10 (destrutivo) → INFRA-06/07/08/09 → INFRA-16/17 (BT e 4 controles) →
INFRA-11/12/13/14/15 → INFRA-03 (teste).
