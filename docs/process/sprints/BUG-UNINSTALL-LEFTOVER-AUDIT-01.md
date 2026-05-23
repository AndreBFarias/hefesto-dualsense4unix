# BUG-UNINSTALL-LEFTOVER-AUDIT-01 — uninstall deixava dir-pai órfão, sobrescrevia workaround do user e atribuía Aurora ao hefesto

**Tipo:** fix (uninstall/limpeza) + clareza de escopo.
**Wave:** V3.8.x — fechamento do ciclo "limpa de verdade".
**Estimativa:** S — três edições contidas em `uninstall.sh` (~30 linhas).
**Dependências:** [[BUG-UNINSTALL-UDEV-DEFAULT-01]] (v3.8.3).
**Status:** DONE (implementado; smoke pós-uninstall na máquina).

---

## Contexto

A mantenedora reportou que após uninstall sobravam coisas "no sistema":
udev rules 99-*, kernel cmdline com `usbcore.autosuspend=-1`, drop-in
WirePlumber e spam de "mic mutado" do COSMIC. Pedido: "atualize o uninstall
pra remover tudo".

Auditoria revelou que **duas das três coisas suspeitas não eram do hefesto**
e a terceira foi recriada de propósito pelo user. Mas o `uninstall.sh` tinha
três bugs reais distintos.

## Diagnóstico (causa-raiz)

1. **Dir-pai órfão** — `BUG-UNINSTALL-GLYPHS-ORPHAN-01` (v3.4.2) removia
   `~/.local/share/hefesto-dualsense4unix/glyphs/`, mas o dir-pai
   `~/.local/share/hefesto-dualsense4unix/` ficava vazio e presente, criando
   rastro detectável por `find ~/.local`.
2. **Workaround do user sobrescrito a cada uninstall** — o drop-in
   `51-hefesto-dualsense-no-default-source.conf` em `~/.config/wireplumber/`
   foi recriado manualmente pelo user (header explícito "Recriado manualmente
   apos o uninstall do hefesto") como workaround standalone. O uninstall.sh
   antigo removia incondicional → cada `./uninstall.sh` desfazia o workaround
   do user.
3. **Atribuição errada de Aurora ao hefesto** — `usbcore.autosuspend=-1` (kernel
   cmdline) e `/etc/udev/rules.d/99-usb-*.rules` vêm do `ritual-aurora-self-heal.sh`
   da mantenedora (toolchain pessoal em `~/.config/zsh/scripts/`), não do hefesto.
   Sem um log informativo, parecia bug do hefesto não-removido — risco real de
   alguém "consertar" removendo o setup pessoal dela.

## Decisão / Entrega

Três edições em `uninstall.sh`:

1. **Remover dir-pai vazio**: após o passo de glyphs, se
   `~/.local/share/hefesto-dualsense4unix/` está vazio, `rmdir` (não-recursivo,
   preserva dados se algo foi colocado lá fora do install).
2. **Preservar workaround marcado**: antes de remover o drop-in WirePlumber,
   `head -5` no header e procurar marker `recriado manualmente|workaround|standalone`
   — se presente, log preservação e segue. Reinstall com
   `--with-wireplumber-fix` sobrescreve com versão canônica do hefesto.
3. **Log "fora do escopo"** no final: lista explícita do que o uninstall
   **não toca** (99-rules, kernel cmdline, dirs compartilhados, pip --user)
   com motivo — cada linha aponta a toolchain dona.

## Critérios de aceite

- [x] `bash -n uninstall.sh` ok (sintaxe).
- [x] Após `./uninstall.sh --yes`: `~/.local/share/hefesto-dualsense4unix/`
      ausente (não fica dir vazio).
- [x] Drop-in com header "Recriado manualmente" sobrevive ao uninstall;
      mensagem "preservando drop-in WirePlumber (marker ...)" aparece no log.
- [x] Log final lista `/etc/udev/rules.d/99-usb-*.rules`,
      `kernel cmdline`, etc. como fora-de-escopo, sem tentar removê-los.

## Arquivos tocados

- `uninstall.sh` (3 blocos).

## Notas para o executor

- O detector de workaround é case-insensitive (`grep -i`) e cobre três markers
  comuns. Falso-positivo (preservar drop-in que era nosso) é benigno — o user
  pode `rm` manualmente; reinstall sobrescreve.
- Sem TTY (CI ou shell sem terminal), `sudo -v` falha mesmo com cache de
  outra sessão. Para teste do passo udev, rodar `./uninstall.sh --yes` em
  shell interativo OU prefixar com `sudo -S` via stdin.

## Proof-of-work runtime

```bash
bash -n uninstall.sh
./uninstall.sh --yes
# esperado no log:
#   preservando drop-in WirePlumber (marker 'recriado manualmente' no header)
#   removendo diretório-pai vazio ~/.local/share/hefesto-dualsense4unix
#   fora do escopo (não removido — não é do hefesto):
#     /etc/udev/rules.d/99-usb-*.rules         — toolchain de power-mgmt do user
#     ...

# validação pós-uninstall
ls /etc/udev/rules.d/ | grep -E '^(70|71|72|73|74)-'    # vazio
find ~/.local/share/hefesto-dualsense4unix             # ausente
ls ~/.config/wireplumber/wireplumber.conf.d/51-hefesto* # presente (workaround user)
```

## Fora de escopo

- Reverter kernel cmdline da Aurora: não é do hefesto, ver
  [[reference-aurora-self-heal-owns-usb-power]] na memória.
- Diagnosticar DualSense USB reset loop (error -71): bug HW/firmware/kernel,
  ver [[project-dualsense-usb-reset-loop-error71]] na memória.
