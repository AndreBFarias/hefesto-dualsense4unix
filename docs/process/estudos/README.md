# Estudos (retornos brutos dos workflows de agentes)

Materialização de segurança dos retornos dos estudos multi-agente, para o conhecimento
sobreviver a queda de sessão/limite. **Não são sprints** — são a matéria-prima deles.
Os sprints derivados vivem em `../sprints/`.

## 2026-07-16 — Estudo 1: o que a onda UHID/Harmonia entregou e o que falta

- `2026-07-16-estudo1-onda-uhid-retorno-completo.json` — síntese consolidada (117 agentes):
  estado geral, entregue-e-validado vs entregue-não-validado, bloqueadores de release,
  próximos passos, riscos. **Achado central: a launch option
  `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` é um veneno persistente** — quando o
  vpad não sobe como Edge `0df2` (BT flaky, hotplug sem promoção, modo Nativo), ela esconde
  físico E vpad e o jogo fica com zero controles.
- `2026-07-16-estudo1-journal-117-agentes.jsonl` — retorno individual de cada agente
  (leitores de dimensão, verificadores adversariais das 109 pendências, síntese).

## 2026-07-16 — Estudo 2: dedup sem launch option + multi-controle (escopo enxuto)

- `2026-07-16-estudo2-DIGEST-frentes.md` — legível por humanos: causa-raiz, solução
  proposta, evidências e itens de sprint de cada frente investigada (dedup udev, BT mudo,
  8BitDo, aba Status por controle, perfis por controle, cores automáticas, autoswitch/UX,
  vpad-sempre-Edge).
- `2026-07-16-estudo2-retornos-parciais.jsonl` — retornos estruturados brutos, incluindo as
  revisões adversariais (3 lentes: técnica, regressão, escopo) de cada frente.

Regra de ouro ditada pela mantenedora para toda a onda do estudo 2: **tudo tem que estar no
install funcionando sem flags** (flag só como opt-out; uninstall simétrico; GUI/daemon
sudo-zero em runtime; nada de "cole este comando" como requisito).
