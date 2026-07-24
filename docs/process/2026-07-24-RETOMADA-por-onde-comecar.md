# 2026-07-24 — RETOMADA: por onde começar quando voltarmos

Índice único do estado após a maratona de 23-24/07. Tudo que ficou de pé, o que
falta validar AO VIVO, e a ordem sugerida. **Ler este primeiro.**

## Estado entregue (v4.0.0, publicada e instalada)

- **As 24 causas-raiz da auditoria GUI × perfis × 4 controles — TODAS corrigidas.**
- Frente Bluetooth: SDP-CACHE-01, BT-SNIFF-PER-OUI-01, WATCHDOG-TRUST-DEADLOCK-01.
- Dois extras do diálogo ao vivo: PERFIL-MANUAL-VENCE-01 e FEAT-AUTOSWITCH-LOCK-01
  (o cadeado "Não trocar de perfil sozinho").
- Migração one-shot do `coop_local` inalcançável (aplicada ao vivo).
- **4724 testes verdes, ruff e mypy limpos.** Release v4.0.0 publicada com
  AppImage/Flatpak/2×.deb/wheel/sdist. Tudo pushado.

## Onde estão os estudos (para não refazer nada)

| Documento | O que guarda |
|---|---|
| `sprints/2026-07-23-sprint-gui-perfis-por-controle.md` | O PLANO: 24 causas-raiz, ordem, contradições resolvidas, mapa queixa-por-queixa |
| `estudos/2026-07-24-relatorios-agentes-implementacao-causas-raiz.md` | Os relatórios BRUTOS dos 6 agentes: decisões por-arquivo, provas de regressão, desvios do plano |
| `estudos/2026-07-23-auditoria-gui-perfis-4-controles.md` | Os achados detalhados + falsos-positivos refutados |
| `estudos/2026-07-23-diagnostico-sdp-cache-e-controle-zumbi.md` | A cadeia BT do controle zumbi (+ hipóteses refutadas) |
| `estudos/2026-07-23-arqueologia-8bitdo-bt.md` | O A/B do 8BitDo (com o desfecho: era regressão nossa) |
| `sprints/2026-07-24-sprint-pesquisa-sniff-parametrizado.md` | Pesquisa ABERTA: afinar sniff em vez de recusar (pode apagar o split por-OUI) |

Memórias (recall automático): `sprint_gui_24_causas_raiz_completa_20260724`,
`bt_sniff_por_oui_e_trust_deadlock_20260723`, `auditoria_gui_perfis_4_controles_20260723`,
`achado_sdp_cache_zumbi_20260723`, `arqueologia_8bitdo_bt_20260723`.

## O QUE FALTA — todos são GATE HUMANO (exigem você jogando)

Nenhuma pendência é de código travado. São validações ao vivo:

### G1 — Sessão de co-op real com os 4 controles (o teste-mãe)
Ordem sugerida, num daemon reiniciado (nunca com jogo aberto):
1. Numeração 1-2-3-4 estável nos player-LEDs (R-13/R-14/R-15).
2. Abrir Sackboy → máscara e co-op valem do 1º frame (R-04/R-05/R-03).
3. Abrir Mullet Mad Jack → NADA é desligado, a config fica (R-01/R-02).
4. Ajustar um controle na GUI → só ele muda (R-16/R-17/R-20).
5. Ligar o cadeado "Não trocar de perfil sozinho" → abrir jogo → perfil fica.

### G2 — R-03 (lock manual x modo do perfil), validação específica
Exige reiniciar o daemon:
- (a) mexer na máscara e, em <30 s, "Ativar" o `sackboy_nativo` → máscara vira
  na hora, resposta com `mode_aplicado: true`.
- (b) mexer na máscara e abrir o Sackboy em <30 s → journal com UM
  `profile_mode_deferred` e UMA `profile_mode_pendencia_aplicada` (ou
  `..._aguardando_jogo` enquanto o jogo tem a autoridade), sem repetição a 2 Hz.

### G3 — Bluetooth sob carga (o gate do BT-SNIFF-PER-OUI-01)
- O Pro Controller genuíno aguenta 4 jogadores sob carga com o no-sniff aplicado
  **por-conexão** (não mais global)? Se cair, o aprendizado é que ele precisa do
  no-sniff já DURANTE o connect → abre a sprint de sniff parametrizado.
- O 8BitDo por BT ainda cai sob carga (a probe destrava com o sniff, mas a
  operação sustentada não). **Cabo é a via confiável hoje.**

### G4 — A vigia 3 do watchdog (SDP) nunca validada no caminho (a)
Só o caso (b) — controle travado — apareceu ao vivo. Falta reproduzir um controle
com cache truncado que RESPONDA ao `sdptool browse` e confirmar que o `Connect()`
do watchdog levanta o HID sozinho.

## Débitos técnicos pequenos (uma linha cada, não urgentes)

Extraídos dos relatórios dos agentes (§ estudo dos relatórios):
- **Case-insensitive em `MatchCriteria.matches`** (schema.py): o agente do R-12
  removeu o `.lower()` que corrompia o dado, mas a cura completa (comparar
  case-insensitive) ficou pendente porque o schema estava ocupado por outro
  agente. É uma linha.
- **`doctor.sh` listando "perfis inalcançáveis"**: o R-12 deu visibilidade na GUI
  ("Só manual (nunca ativa sozinho)"), mas um check no doctor seria bom.
- **Sentinel `{"type":"manual"}` no schema** para perfis manuais-only, em vez de
  criteria vazio (hoje resolvido por regex real no coop_local).

## Como NÃO desperdiçar o trabalho

1. **Ler este doc + a sprint antes de tocar em qualquer coisa** — o plano tem as
   contradições já resolvidas; refazer uma é regressão.
2. Os agentes JÁ pesquisaram o BlueZ, o hid-nintendo e o SDL — está nos estudos.
   Nunca refazer pesquisa (regra da mantenedora).
3. Rodar A/B de BT sempre com o `hefesto-bt-health-watchdog.timer` PARADO (a
   vigia 0 reaplica o modo ativo a cada 2 min e contamina) — e lembrar de religar.
