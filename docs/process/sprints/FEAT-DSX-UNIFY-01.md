# FEAT-DSX-UNIFY-01 — Unificar o DualSense Fix (dsx.sh) no hefesto

**Tipo:** feat (médio-grande — CLI + GUI + integração de sistema).
**Wave:** V3.12.
**Status:** CAMADAS 1-2 MATERIALIZADAS (CLI, commit 8471ef1). Camada 3 (cartão na
GUI) DEFERIDA — ver nota abaixo.

## Materializado (2026-07-08)

- `integrations/storm_doctor.py`: diagnóstico READ-ONLY (quirk anti-storm no
  usbcore, Steam Input nos `localconfig.vdf`, drop-in do WirePlumber, regra
  `authorized=0`), paths injetáveis, testado com fixtures. Validado ao vivo:
  achou Steam Input LIGADO + quirk ativo + WP configurado.
- `doctor` mostra o bloco "anti-storm / sistema"; `doctor --fix-safe` roda o
  SEGURO sem sudo (Steam Input OFF via `--apply-quiet` + WirePlumber `--install`);
  `doctor --reapply-all` invoca o `dsx.sh` (motor privilegiado, PEDE SENHA em
  terminal, confirma antes).

**Camada 3 (cartão na GUI) DEFERIDA — decisão de engenharia:** o botão
"reaplicar tudo" é PRIVILEGIADO (sudo). Do daemon/GUI (Wayland) isso exigiria um
askpass GRÁFICO; o `dsx.sh` já resolve sudo em TERMINAL (`Terminal=true` no
`.desktop` "DualSense Fix (dsx)") e o CLI `doctor --reapply-all` roda no terminal
onde o sudo funciona. Duplicar isso num botão de GUI (com askpass gráfico) é mais
frágil e redundante. O caminho primário do privilegiado fica CLI/`.desktop`; um
cartão só-diagnóstico na GUI (sem o botão privilegiado) pode entrar depois se a
Vitória sentir falta.
**Decisão da Vitória (2026-07-07):** *"Absorver o seguro + botão que chama o resto."*

---

## Contexto

Hoje o anti-storm vive num script separado (`dsx.sh`) + atalho `.desktop`
("DualSense Fix (dsx)"). A Vitória quer trazer para dentro do hefesto **sem
perder as melhorias** do dsx. Fronteira crítica (memória
[[reference-aurora-self-heal-owns-usb-power]]): **o kernel cmdline (quirk
anti-storm `054c:0ce6:gn`) e as regras `99-usb-*` são do ritual-Aurora, NÃO do
hefesto** — não absorver isso.

Causa-raiz do storm (memória [[storm-dualsense-e-config-nossa-nao-hardware]]):
o kernel `snd-usb-audio` enumerando o ÁUDIO USB do DualSense sob carga. Alavancas:
(A) quirk DELAY_CTRL_MSG (preserva áudio — Aurora/kernel cmdline);
(B) `authorized=0` nas interfaces de áudio (perde mic/fone do controle).

O `dsx.sh` orquestra: Aurora self-heal → udev do hefesto → Steam Input OFF →
WirePlumber só-HID → re-pin power → udevadm trigger → watcher/guard → restart
daemon → doctor.

## Decisão — 3 camadas

1. **Absorver o SEGURO (nativo, sem sudo/kernel)** no hefesto, via `doctor`:
   - `hefesto-dualsense4unix doctor` já diagnostica; estender com um bloco
     **storm** que REPORTA: quirk presente no cmdline? regra `authorized=0`
     ativa? Steam Input on/off (lê `localconfig.vdf`, memória
     [[reference-steam-input-keys-localconfig-path]])? WirePlumber drop-ins
     presentes? Só LEITURA — nenhuma mutação sem flag.
   - `hefesto-dualsense4unix doctor --fix-safe`: aplica só o que NÃO precisa de
     root e é reversível/idempotente — Steam Input OFF (editar `localconfig.vdf`
     com Steam fechada) e os drop-ins do WirePlumber no `~/.config`. NADA de
     kernel/udev (domínio da Aurora).
2. **Botão que chama o RESTO (privilegiado)**: um comando/opção
   `hefesto-dualsense4unix doctor --reapply-all` (e um botão na GUI aba Daemon)
   que **invoca o `dsx.sh`** para a parte que precisa de sudo (udev, re-pin
   power, udevadm trigger). O `dsx.sh` continua o MOTOR privilegiado; o hefesto
   é a interface. Sudo via askpass (memória [[release-process-fork-anonymity]]),
   confirmando antes (ação de sistema).
3. **GUI (aba Daemon)**: cartão "Anti-storm / Sistema" mostrando o diagnóstico
   (verde/amarelo por item) + 2 botões: "Reaplicar fixes seguros" (--fix-safe) e
   "Reaplicar tudo (pede senha)" (--reapply-all → dsx.sh). O `.desktop` do dsx
   pode continuar existindo (atalho rápido); a GUI passa a ser o caminho
   primário.

## NÃO fazer (fronteira Aurora / footguns)

- NÃO absorver o kernel cmdline nem as regras `99-usb-*` (Aurora é dona).
- NÃO aplicar `authorized=0` (perde mic/fone) por padrão — só o dsx.sh sob flag
  explícita mantém isso.
- NÃO reiniciar o daemon em rajada (re-dispara a enumeração do áudio — memória).
- NÃO escrever "feito por"/nomes de IA em comentários (gate de anonimato).

## Critérios de aceite

- [ ] `doctor` reporta o bloco storm (quirk/authorized/Steam Input/WirePlumber)
      sem mutar nada; testes com fixtures de `localconfig.vdf` e cmdline fake.
- [ ] `doctor --fix-safe`: Steam Input OFF (Steam fechada) + drop-ins WP; sem
      sudo; idempotente; reversível documentado.
- [ ] `doctor --reapply-all`: invoca `dsx.sh` (askpass); confirmação antes.
- [ ] GUI aba Daemon: cartão de diagnóstico + 2 botões, via IPC/subprocess.
- [ ] Suite verde; ruff/mypy; smokes. Validação da Vitória: rodar `doctor`,
      `--fix-safe`, e o botão da GUI num cenário de storm.

## Fora de escopo

- Mover a lógica de kernel/udev para o hefesto (fica na Aurora + dsx.sh).
- Auto-aplicar `authorized=0` (opt-in explícito só no dsx.sh).
