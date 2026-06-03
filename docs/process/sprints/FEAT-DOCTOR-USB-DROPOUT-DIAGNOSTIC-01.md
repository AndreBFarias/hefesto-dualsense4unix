# FEAT-DOCTOR-USB-DROPOUT-DIAGNOSTIC-01 — diagnóstico de dropout `-71` e recomendação de porta/BT no doctor

**Tipo:** feat (diagnóstico; observabilidade de plataforma).
**Wave:** V3.9 — recuperação de áudio + diagnóstico USB.
**Estimativa:** M — nova checagem no doctor + modo watch + parsing de `lsusb`/`journalctl`.
**Dependências:** decisão [[018-usb-power-scope-vs-dropout]]; contexto em ADR-008, ADR-013.
**Status:** PENDING.

---

## Contexto

O `-71` (`EPROTO`) do controlador xHCI em AMD Ryzen derruba o DualSense (e
vizinhos do mesmo barramento) por baixa energia do controlador (Power Supply Idle
Control / BIOS). [[018-usb-power-scope-vs-dropout]] decidiu que o Hefesto **não
corrige** isso (é BIOS), mas **diagnostica e recomenda**. Hoje o `doctor.sh` não
diz nada sobre dropout: o usuário descobre na marra.

O estudo `docs/research/2026-05-28-dualsense-dropout-usb-e-wireplumber-source.md`
mostrou que a máquina tem dois controladores xHCI (`02:00.0` chipset, `0c:00.3`
Matisse) e que mover o controle para o controlador "saudável" é uma mitigação
real — mas o mapeamento portacontrolador exige inspeção que o usuário não sabe
fazer. Na sessão montou-se um vigia ad-hoc de `-71` via `journalctl -kf`.

## Decisão / Entrega

Dar ao `doctor.sh` três capacidades novas, todas **read-only** (nunca edita BIOS,
cmdline ou regras de outro dono — fronteira de [[018-usb-power-scope-vs-dropout]]):

1. **Localização do barramento.** Nova seção que detecta em qual controlador
   PCI / Bus o DualSense (`054c:0ce6`/`0ce6`+`0df2`) está conectado — parse de
   `/sys/bus/usb/devices/*/` (resolvendo o `0000:XX:00.Y`) e de `lspci`. Reporta
   ex.: "DualSense em Matisse `0c:00.3` (Bus 003); teclado/mouse em chipset
   `02:00.0`".
2. **Contagem de dropout.** Conta `error -71` / `device descriptor read/64,
   error` no `journalctl -b -k`. Se > 0: `[WARN]` com a contagem e a recomendação
   — "mova o controle para uma porta do outro controlador (`<pci>`), de
   preferência USB 2.0 traseira; ou use Bluetooth (ADR-008). Causa-raiz é Power
   Supply Idle Control na BIOS — fora do escopo do Hefesto corrigir." Se 0:
   `[ OK ] sem dropout -71 neste boot`.
3. **Modo `--watch-dropout`.** Vigia o journal e bloqueia até o primeiro sinal de
   dropout, então imprime a linha e sai (equivale ao vigia ad-hoc da sessão):
   `journalctl -kf -o cat --since now | grep -m1 -iE 'error -71|device descriptor
   read/64, error|not accepting address|device not responding'`. Documentar que
   é uma sessão de observação (roda até disparar ou Ctrl-C); incluir nota de que
   desconexões manuais não casam o filtro (foca em `-71`, não em `disconnect`).

A recomendação de porta deve ser cautelosa quanto ao BT: na topologia observada
o dongle BT também está no Matisse — o doctor avisa "BT contorna a porta do
controle, não necessariamente o controlador" quando o adaptador BT está no mesmo
PCI do DualSense.

## Critérios de aceite

- [ ] `doctor.sh` mostra o controlador/Bus do DualSense e o dos demais HID (teclado/mouse) quando presentes.
- [ ] Com `error -71` no journal do boot, `doctor.sh` emite `[WARN]` com a contagem e recomenda porta alternativa + BT, citando que a correção é BIOS (não Hefesto).
- [ ] Sem `-71`, reporta `[ OK ] sem dropout -71 neste boot`.
- [ ] `doctor.sh --watch-dropout` bloqueia e retorna ao primeiro `-71`, imprimindo a linha do kernel; sai limpo no Ctrl-C.
- [ ] Quando o adaptador BT está no mesmo controlador do DualSense, a recomendação de BT inclui a ressalva.
- [ ] Nenhuma escrita em `/sys`, cmdline, BIOS ou regras udev de terceiros (read-only).
- [ ] `./scripts/check_anonymity.sh` vazio; acentuação PT-BR verde.

## Arquivos tocados

- `scripts/doctor.sh` — nova seção `== USB / dropout ==`, parsing `/sys` + `lspci` + `journalctl`, flag `--watch-dropout`, atualização do `--help`/uso.
- `tests/unit/` — fixtures de `journalctl` (com e sem `-71`) e de `/sys/.../uevent` para o parsing de controlador.
- `docs/process/CHECKLIST_HARDWARE_V2.md` — item de verificação do diagnóstico em hardware real.

## Proof-of-work runtime

```bash
scripts/doctor.sh | sed -n '/USB/,/Steam/p'     # seção nova: controlador + contagem -71
scripts/doctor.sh --watch-dropout                # bloqueia; dispara no primeiro -71
journalctl -b -k | grep -c 'error -71'           # confere a contagem reportada
```

## Fora de escopo

- Corrigir o `-71` (BIOS/Power Supply Idle) — [[018-usb-power-scope-vs-dropout]].
- Editar kernel cmdline / `99-usb-*.rules` / tunável global — dono é o usuário/Aurora.
- Forçar o controle a um controlador específico via software — não há alavanca
  confiável; a recomendação é física (trocar o cabo de porta).
- Diagnóstico de timeout L2CAP do Bluetooth — issue distinta (já notado em ADR-013).
