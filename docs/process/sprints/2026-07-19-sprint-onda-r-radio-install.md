# Sprint Onda R — rádio resiliente no install/uninstall (BlueZ + agente + higiene)

> Fonte da verdade p/ os agentes (workflow impl-onda-r-radio-wf_3e56c7c8-25e re-lançável).
> Estudo-base: `2026-07-19-estudo-bluez-backport-onda-r.md`. Território EXCLUSIVO:
> install.sh, uninstall.sh, assets/bluetooth/**, assets/systemd novo,
> scripts/disable_steam_input.sh. NÃO tocar src/, tests/ de src, doctor.sh, hefesto-launch.sh.

## Contexto medido (não re-verificar)
- bluetoothd 5.72 crashou 6×/5 dias (heap corruption input/HIDP); 6º crash comeu bond recém-
  pareado. Backport **bluez 5.85** (rebuild resolute→noble) JÁ INSTALADO nesta máquina; .debs em
  `~/.cache/hefesto-dualsense4unix/bluez-backport/` (bluez, libbluetooth3, bluez-cups +
  SHA256SUMS + VERSOES-ANTERIORES.txt com 5.72-0ubuntu5.5).
- Migração 5.72→5.85 descarta bonds antigos 1× (re-parear); bonds novos persistem (provado).
- main.conf da máquina tem 2 blocos hefesto por sentinela: `# >>> hefesto FastConnectable >>>`
  (asset canônico já existe) e `# >>> hefesto JustWorksRepairing >>>` (apensado À MÃO hoje —
  sem ele o BlueZ REJEITA re-pareamento de device com bond; re-pair em massa validado <2min).
- Bond meio-salvo (Paired sem Bonded) = "No agent available for request type 2" = nenhum agente
  D-Bus registrado na hora do pair. Cura: agente persistente NoInputNoOutput (`bt-agent` do
  pacote bluez-tools, presente no noble).
- REGRA: install NUNCA reinicia bluetoothd; exceção única documentada = postinst do próprio
  pacote bluez quando o passo do backport aplica versão nova (idempotente: já ≥5.79 ⇒ no-op).

## Entregas — lado INSTALL
1. Asset novo `assets/bluetooth/hefesto-justworks.{conf,block}` espelhando o par
   fastconnectable (mesmos comentários-padrão; sentinelas EXATAMENTE
   `# >>> hefesto JustWorksRepairing >>>` / `# <<< hefesto JustWorksRepairing <<<` para o
   install reconhecer o bloco manual de hoje como já-aplicado). Conteúdo: `[General]`
   `JustWorksRepairing = always` + porquê.
2. install.sh passo 3: aplicar JustWorks pelo MESMO mecanismo do FastConnectable
   (main.conf.d se existir; senão bloco apensado com backup timestampado).
3. install.sh passo novo "ONDA-R: BlueZ resiliente": (a) dpkg-query pega versão de bluez;
   <5.79 e .debs presentes com SHA256SUMS ok ⇒ grava VERSOES-ANTERIORES.txt se ausente e aplica
   `apt-get install ./bluez_*.deb ./libbluetooth3_*.deb ./bluez-cups_*.deb --allow-downgrades`
   com AVISO ALTO (reinicia bluetoothd; bonds antigos migram fora — re-parear 1×); sob --yes
   prossegue; (b) .debs ausentes ⇒ warn com instrução de build (referenciar o estudo) e SEGUE;
   (c) ≥5.79 ⇒ no-op. Idempotente.
4. Agente de pareamento: dep `bluez-tools` no check de deps; asset novo
   `assets/systemd/hefesto-bt-agent.service` (system: ExecStart=/usr/bin/bt-agent
   --capability=NoInputNoOutput; After/Requires=bluetooth.service; Restart=on-failure;
   hardening espelhando units do repo); install habilita `enable --now` (seguro: não toca o
   bluetoothd).
5. Conferir idempotência do passo FastConnectable com o main.conf NOVO do 5.85.

## Entregas — lado UNINSTALL + higiene
1. Simetria: remover bloco JustWorks entre sentinelas (e/ou drop-in); desabilitar+remover
   hefesto-bt-agent.service; **restaurar bluez** das versões de VERSOES-ANTERIORES.txt por
   DEFAULT com AVISO ALTO (derruba BT + descarta bonds de novo) e opt-out `--keep-bluez`
   (documentar no help); VERSOES-ANTERIORES.txt ausente ⇒ warn e segue sem falhar.
2. Higiene legada: (a) `scripts/disable_steam_input.sh` cobrir também
   `SteamController_SwitchSupport` (replicar o padrão do PSSupport ~:178-179; atualizar
   --status); (b) uninstall.sh: storm.conf órfão também no caminho `--keep-udev`; (c) remover
   TAG `uaccess` INERTE das regras ≥73 nos assets (uaccess só funciona <73; comentar o porquê;
   NÃO renumerar nada).
3. Simetria completa installuninstall conferida item a item.

## Auditoria (checklist do auditor)
- Idempotência 2×; sentinelas batem com o bloco manual; bash -n nos dois scripts.
- Nenhum caminho reinicia bluetoothd fora do postinst documentado; `enable --now` não trava
  sem TTY; apt não-interativo sob --yes.
- set -e × pipelines/grep sem match; sudo -n gates no padrão da casa.
- disable_steam_input não corrompe o vdf binário; --status coerente.
- .rules: só a TAG morta saiu; sintaxe udev ok.
