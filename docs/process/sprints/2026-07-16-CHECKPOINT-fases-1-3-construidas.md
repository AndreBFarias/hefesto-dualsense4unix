# Checkpoint 2026-07-16 (noite) — Fases 1–3 da onda construídas, validadas ao vivo e pushadas

Sessão ultracode. Dois estudos de manhã (117 + 41 agentes) viraram 8 sprints; à noite as três
primeiras fases foram construídas, revisadas adversarialmente, gateadas e **validadas ao vivo na
máquina de referência**. Branch `sprint/harmonia-uhid` pushada no fork.

## Os commits do dia

| Commit | O quê |
|---|---|
| `d070fbe` | 8 sprints + índice da onda + retornos brutos dos 2 estudos (docs/process/estudos/) |
| `bc68718` | **Fase 1** — blueprint sintético: o vpad nasce DualSense Edge `054c:0df2` SEMPRE (parou de ler o físico; o sono do firmware BT deixou de importar); promoção no hotplug; fallback nunca mais `0ce6` nem silencioso; hermeticidade da suíte (tripwire no quit_app, 22 skips falsos curados); MACs reais removidos de fixtures/docs + teste-guarda de anonimato |
| `f2e2aad` | **Fase 2** — wrapper `hefesto-launch %command%` fail-safe (envs decididas na hora via IPC; daemon morto → nenhuma env → pior caso é duplicado, nunca zero); launch_env materializado por appid; migração/strip do localconfig.vdf (fixtures, recusa com jogo aberto); histerese do autoswitch + gate de foco X rançoso; guard de dedup por jogador + banner honesto |
| `8e59601` | **Fase 3** — perfis por controle (fundação 4P): desired por-uniq com merge por campo e reset na ativação; `Profile.controllers` aditivo; `origin` nos 5 call sites de activate() (o autoswitch parou de sequestrar o session.json; o boot restaura a intenção manual); GUI edita por-controle de verdade |

Gate ao fim de cada fase: ruff 0.15.20 limpo, mypy strict, **pytest 2379 → 2712 (0 fails, 0 skips
com GTK real)**, acentuação, daemon da mantenedora vivo. Cada fase passou por 3 revisores
adversariais + fixador (Fase 1: 1 HIGH + 2 MED corrigidos; Fase 2: 3 HIGH + 9 MED; Fase 3: 1 HIGH
+ 3 MED).

## Validação ao vivo (retorno completo em `../estudos/2026-07-16-validacao-ao-vivo-fases-1-3.json`)

**Veredito: VALIDADO COM RESSALVAS — nenhuma falha do código novo.**

- Vpad Edge `054C:0DF2` via UHID subiu ao vivo (kernel bindou, `dedup_ok=true`, MAC forjado
  `02:fe:...:01`, físico `0CE6` e vpad `0DF2` coexistindo). O caso venenoso (uinput/`0ce6`) não
  ocorreu em nenhum momento.
- Wrapper validado nos 3 estados + latência 16–98 ms + fail-safe com socket zumbi (teto 1 s);
  launch options pré-existentes da usuária sobrevivem.
- Perfil por controle ponta a ponta no hardware: override por uniq venceu o global no sysfs,
  sobreviveu a reload, mapa `controllers` persistiu no JSON.
- Histerese: antes-vs-depois no MESMO journal do dia (instância antiga caía de perfil com
  `unknown`; a nova reteve por ~70 s de cegueira, 1 log). Banner ausente com tudo saudável
  (função pura + screenshot).

**Ressalvas honestas (cobertas só por teste, não ao vivo):** boot frio já com flag dualsense →
Edge direto; caminho negativo do banner (degradar o vpad de propósito não foi feito por
prudência); ramo "perfil nativo omite IGNORE".

## Estado REAL da máquina ao desligar

- **Máscara persistida trocada para `dualsense`** durante a validação (era `xbox`) — é o
  estado-alvo para o teste do layout PS; reverter é 1 clique na GUI.
- **O wrapper `hefesto-launch` NÃO está instalado** (código pronto; o `install.sh` o põe por
  default — ciclo adiado por decisão da mantenedora).
- **O veneno estático segue no `localconfig.vdf`** (appid 1599660): a validação não podia tocar
  na Steam real. Migrar com a Steam fechada (botão da GUI ou `steam_launch_options.py --migrate`).
- Doctor: 2 FAILs **esperados** (wrapper ausente + mic DualSense) — ambos curados pelo
  `./install.sh` sem flags quando rodar.

## O que ficou para a próxima sessão (decisão da mantenedora: "o ponto 3 e o 4 não fazemos agora")

1. **Fase 4**: cores automáticas por controle (MAC→slot, paleta PS5) + aba Status em cards +
   **diálogo do wrapper 1x por jogo (APROVADO por ela nesta sessão** — GTK dialog, nunca popover;
   dispensou → não insiste no appid).
2. **Fase 5**: itens do 8BitDo (doctor gateado na cascata do hid-nintendo, inventário read-only).
3. **Ciclo uninstall → install ambos SEM FLAGS** + doctor (instala wrapper + WP-51 + migração do vdf).
4. **Validação humana**: layout PS + rumble no Sackboy (USB), Bluetooth com journal aberto
   (BT-07), PERFIL-05 (perfil autocarrega + settings por controle), modo do 8BitDo (8BIT-05).
