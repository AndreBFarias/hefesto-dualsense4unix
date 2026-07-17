# Checkpoint 2026-07-17 (madrugada) — Fases 4-5 construídas, ciclo install rodado, máquina validada

Sessão de sequência da onda multicontrole+dedup: a Fase 3 foi fechada (PERFIL-06 + registro
da validação), as Fases 4-5 foram construídas por agentes de execução com verificação
centralizada, o ciclo `uninstall.sh && install.sh` SEM FLAGS rodou na máquina de referência
e o retorno vivo pegou (e curou) um bug de integração que nenhum teste hermético viu.
Branch `sprint/harmonia-uhid`.

## Commits da sessão

| Commit | O quê |
|---|---|
| `17006f2` | Fases 4-5: cor automática por controle (identity MAC→slot + paleta PS5 como camada do meio do merge), aba Status em cards (dono da escrita + priming + contraste ≥ 3.0), toggle D4, diálogo do wrapper 1x/jogo, doctor (7 regras + LED + cascata 8BitDo), inventário externo read-only, PERFIL-06, guia do 8BitDo, hermeticidade do test_enumerate |
| (fix pós-install) | `reassert_resolved_outputs()`: a ativação de perfil converge o físico ao resolvido por-controle — sem ele, boot com controles conectados ficava na cor global até o próximo replug (visto AO VIVO) |

Gate: **pytest 3058→3062/0/0** (era 2712 na Fase 3), ruff limpo, mypy strict limpo,
acentuação limpa nas linhas tocadas (2 violações pré-existentes documentadas).

## O ciclo install (SEM FLAGS) — a regra de ouro cumprida

- `./uninstall.sh --yes` → wipe completo, configs preservadas, **o veneno legado saiu do
  localconfig.vdf com backup** (simetria da Fase 2 funcionando; a linha 914 do Sackboy
  morreu aqui).
- `./install.sh --yes` → 11 passos + 11b: wrapper `hefesto-launch` instalado, quirk do
  mic (WP-51) aplicado, applet COSMIC compilado, PSSupport OFF + guard, 7 regras udev.
- `doctor.sh` pós-ciclo: **os FAILs de ontem sumiram** (wrapper presente, veneno zero,
  7 regras, LED gravável). WARNs restantes: hidraw0-3 em 0666 (receivers 2.4G, ajuste
  manual antigo, fora do escopo) e o detector de janela DEGRADADO (limitação do
  cosmic-comp, conhecida).
- Mic: warning pós-boot do daemon curado com `doctor.sh --fix` (fonte reeleita).

## Validação viva (com o daemon NOVO, dois DualSense pareados por BT)

- **Dois DualSense em BT ao mesmo tempo**: `player_slot 1` e `2` atribuídos;
  `identity_slots_restaurados` no restart (a persistência D2 funcionando ao vivo);
  co-op com **dois vpads uhid** (`vpad_backend: uhid` nos dois; nada de uinput/0ce6);
  `dedup_ok: true`, `degraded: false`; inputs por controle fluindo no `state_full`;
  `lightbar_source: sysfs` com a cor real.
- **O bug de integração pego ao vivo**: os dois controles ficaram com o ROXO global do
  perfil em vez da paleta (azul/vermelho) — a ativação de perfil fazia broadcast do
  global e nunca re-resolvia por-key (a camada automática só rodava em
  hotplug/new_keys/unmute). Fix: `reassert_resolved_outputs()` no fim da ativação
  (manager) e do apply_draft (applier) + 4 testes de regressão do cenário exato.
- **A janela de sono do BT em ação** (o fenômeno do Estudo 1, agora INÓCUO para o
  vpad): após o restart, os dois controles ociosos emudeceram (`pydualsense_init_timeout`
  em loop) — o vpad continuou de pé (blueprint sintético) e o daemon retenta os handles.
  Consequência honesta: a confirmação VISUAL da paleta ficou para quando os controles
  acordarem (qualquer toque) — ao acordar, o probe abre os handles e o
  `_reapply_desired` pinta azul (1) e vermelho (2) sozinho.
- O Pro Controller (8BitDo em modo Switch) **morreu por BT às 23:52 desta madrugada**
  com a assinatura curta do estudo (3× `exceeded max attempts` + re-probe `-110`) — a
  morte de assinatura CURTA fica abaixo do threshold anti-falso-positivo do doctor
  (decisão deliberada do sprint; pode ter sido idle-off). Registrado no doc do 8BitDo.

## Decisões / mudanças visíveis a validar por ela (roteiro no CHECKLIST_MANUAL.md)

1. **Ao tocar nos controles**: azul no Controle 1 e vermelho no Controle 2, sozinhos
   (auto_player_colors nasce ligado — o roxo global do perfil `vitoria` é vencido pela
   paleta; para voltar ao roxo em todos, desligar o toggle novo na aba Lightbar OU
   aplicar a cor com alvo "Todos", que desliga o auto com aviso).
2. Aba Status em cards (1 por controle, inputs tintados) — aceite do compromisso da cor.
3. PERFIL-05 (a/c/d), COR-07, STATUS-05, BT-07 (Sackboy DESENVENENADO + RDR2 por BT),
   8BIT-05 (modo do 8BitDo) — os gates humanos da onda.
4. 8BIT-02 (aba de controles externos) NÃO construído: aguarda o OK dela para
   "100% read-only" (pré-requisito de produto do sprint).

## Estado REAL da máquina ao desligar (a pedido dela, o PC foi desligado ao fim)

- Daemon systemd `active`, autostart habilitado, perfil `vitoria` restaurado, wrapper
  instalado, vdf desenvenenado, launch_env materializado.
- Os dois DualSense pareados (dormindo na mesa); 8BitDo desconectado (morte BT).
- Branch `sprint/harmonia-uhid` commitada e pushada no fork. Release SEGUE SEGURADO
  (decisão dela: falta sentir o controle vibrar num jogo real — agora com o Sackboy
  limpo e o wrapper no lugar, o teste ficou possível de ponta a ponta).
