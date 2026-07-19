# ÍNDICE — Onda 2026-07-18 "Fim da guerra de escritores" (rumo à v1 de produção)

> Origem: frota de 10 agentes sobre a sessão real de co-op 4P misto de 2026-07-18.
> Estudo consolidado: `docs/process/estudos/2026-07-18-estudo-guerra-de-escritores-hidraw.md`
> (brutos em `2026-07-18-frota-coop-4p/`). Decisão de produto: esta onda fecha os P0/P1 do
> co-op misto e prepara a v1; broker root e IMU do vpad ficam materializados para a próxima.

## Sprints

| # | Arquivo | Frente | Prioridade |
|---|---------|--------|-----------|
| 1 | `2026-07-18-sprint-nucleo-fim-da-guerra.md` | GUERRA-01 (envs Proton + keepalive neutro + reassert cache) · BTREPORT-02 (report 0x31 correto) · REPLICA-03 (output do jogo → físico: triggers/lightbar/player-LEDs) | P0 |
| 2 | `2026-07-18-sprint-externos-e-gui.md` | EXT-04 (identidade + LED no daemon, leitura pura) · GUI-05 (diálogo temado, segmented de modo, aviso wrapper honesto) | P1 |
| 3 | `2026-07-18-sprint-infra-kernel-install.md` | PATH-06 (wrapper no PATH + launch options) · KERNEL-07 (udev: vpad na 70, js-Motion, 78 ampliada) · MISC-08 (mult max, autoswitch GUI-neutra, EBADF, telemetria) | P1 |
| 4 | `2026-07-18-sprint-futuro-broker-imu-rdr2.md` | NÃO EXECUTAR HOJE — broker root hide-hidraw (P2 raiz), IMU/touchpad reais no vpad (DEDUP-02), 2ª causa RDR2 (BT-07) | futuro |
| 5 | `2026-07-18-sprint-plataforma-proton-usb-bt.md` | NÃO EXECUTAR HOJE (pedido 2026-07-18, roda após esta onda) — Proton PINADO pelo install, broker promovido, USB sem economia, BT máximo, Game Mode COSMIC | próxima onda |

Nota de estado (2026-07-18 ~22h): o 8BitDo caiu do BT (storm joycon_enforce_subcmd_rate — ver
estudo; EXT-04 cura o nosso agravante) e a mantenedora o ligou NO CABO — validações a partir
de agora contam DOIS "Pro Controller" USB (057e:2009): o Nintendo real e o 8BitDo.

## Os 6 problemas do dia → onde são curados

- **P1 rumble morto no branco USB** → GUERRA-01 (keepalive neutro + PROTON_DISABLE_HIDRAW) + REPLICA-03.
- **P1 lightbar verde-limãoazul** → GUERRA-01 (jogo perde acesso ao físico; reassert com cache).
- **P2 duplicado sem wrapper** → PATH-06 (wrapper acessível + aplicado) + GUI-05 (aviso honesto); cura de RAIZ no broker (sprint futuro).
- **P3 numeração 8BitDo LED≠jogo** → REPLICA-03 (player-LED do jogo nos DualSense) + EXT-04 (identidade estável + fim do bombardeio que MATAVA o 8BitDo).
- **P4 "dropdown" de modo na ficha** → GUI-05 (segmented read-only; dropdown é vetado por design).
- **P5 diálogo do wrapper claro** → GUI-05 (classe de tema + varredura de toplevels).
- **P6 Motion Sensors viram jsN** → KERNEL-07 (regra js-Motion MODE 0000; 78 ampliada).

## Regras da onda (invariantes)

1. Install SEM FLAGS: toda cura nova entra como default simétrico (uninstall remove).
2. Gate local = `pytest tests/` completo com **0 skipped** + `ruff check src/ tests/` (0.15.20) +
   `mypy src/hefesto_dualsense4unix` + `scripts/check_anonymity.sh`. Linhas tocadas com
   acentuação limpa (dívida antiga não conta).
3. Testes de GUI: NUNCA `import gi` no topo; padrão `_install_gi_stubs` de
   `tests/unit/test_rumble_actions.py:22-40`; GTK-real só com guarda por atributo + espelho stub.
5. Ordem obrigatória: keepalive neutro JUNTO ou ANTES do fix do report BT (nunca o BT sozinho —
   ver "Riscos" do estudo).
6. NÃO reiniciar o daemon de produção durante o desenvolvimento (controles em uso); o ciclo
   install+restart acontece UMA vez ao final, na validação.

## Gates humanos que continuam abertos (a mantenedora é o gate)

Power-off + lightbars acesas (Reset-0x08) · rumble+layout PS em jogo real (o desta onda) ·
BT-07/RDR2 · wrapper no Sackboy com 8BitDo de 3º · 8BIT-05 (modo do 8BitDo) · roteiros do
CHECKLIST_MANUAL.md §COR-07/STATUS-05/PERFIL-05.
