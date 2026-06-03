# BUG-WIREPLUMBER-FIX-FALSE-SUCCESS-01 — fix e doctor checam o `configured`, não o default ATIVO

**Tipo:** bug (relatório enganoso / verificação no lugar errado).
**Wave:** V3.9 — recuperação de áudio + diagnóstico USB.
**Estimativa:** S — endurecer dois scripts shell + testes de parsing.
**Dependências:** decisão [[019-wireplumber-default-active-not-configured]].
**Status:** PENDING.

---

## Contexto

Reportado via estudo de campo `docs/research/2026-05-28-dualsense-dropout-usb-e-wireplumber-source.md`.
Continuação de [[FEAT-WIREPLUMBER-DUALSENSE-NOT-DEFAULT-SOURCE-01]] — que está
correta na decisão (rebaixar), mas mente no relatório.

## Diagnóstico (causa-raiz)

O WirePlumber separa `default.configured.audio.source` (preferência persistida em
`~/.local/state/wireplumber/default-nodes`) do default **ativo**
(`pactl get-default-source` / `*` no `wpctl status`). A política só promove a
fonte `configured` se ela estiver *available*.

Dois pontos cegos:

1. **`scripts/fix_wireplumber_default_source.sh`** imprime "fonte padrão reeleita
   para o id N" após `wpctl set-default` + restart, **sem reverificar o ativo**.
   Quando o DualSense é a única fonte available (webcam off + jack onboard
   vazio), o ativo volta ao DualSense e o script declara sucesso assim mesmo.

2. **`scripts/doctor.sh::check_wireplumber_source`** casa
   `^default.configured.audio.source=.*dualsense` no arquivo de estado — i.e.,
   inspeciona o `configured`, não o ativo. Pode imprimir `[ OK ] WirePlumber não
   fixa o DualSense como fonte padrão` enquanto o controle **é** o mic ativo.

Evidência empírica (sessão 2026-05-28): `configured` = onboard, mas
`pactl get-default-source` = DualSense; `wpctl inspect` confirmou DualSense em
`priority 50` (drop-in OK) e onboard em `2009` porém indisponível.

## Decisão / Entrega

Alinhar ambos os scripts à pós-condição canônica de [[019-wireplumber-default-active-not-configured]]:
**o sucesso é o default ATIVO != DualSense**, não a chave `configured`.

1. **`fix_wireplumber_default_source.sh`:** após reset + restart + settle curto
   (poll de `pactl get-default-source`, timeout ~2 s), classificar em três
   estados e reportar honestamente:
   - **OK:** ativo != DualSense → "microfone padrão: <nome> (DualSense rebaixado)".
   - **ÚNICO:** ativo == DualSense **e** não há outra fonte de captura available
     → aviso (não erro): "DualSense é a única fonte de captura disponível;
     conecte webcam/mic ou use `--disable-source`". Exit code distinto (ex.: 2).
   - **FALHA:** ativo == DualSense **com** outra fonte available → erro real
     (drop-in não aplicou / regressão de prioridade). Exit code de erro.
2. **`doctor.sh::check_wireplumber_source`:** trocar a checagem do arquivo de
   estado por `pactl get-default-source` (fallback ao `*` do `wpctl status` se
   `pactl` ausente). Reportar:
   - `[ OK ]` ativo != DualSense;
   - `[WARN]` ativo == DualSense por escassez (única fonte) — com a recomendação;
   - `[FAIL]` ativo == DualSense com outra fonte available.
3. Mensagens em PT-BR, acentuação correta (gate strict).

## Critérios de aceite

- [ ] Com fonte não-DualSense available, após o fix `pactl get-default-source` != DualSense e o script reporta OK.
- [ ] Com o DualSense como única fonte, o script **não** reporta sucesso: emite o aviso "única fonte" e sai com código != 0 de erro real (código dedicado p/ "único").
- [ ] `doctor.sh` distingue os três estados acima; nunca imprime `[ OK ]` quando o ativo é o DualSense.
- [ ] `./scripts/check_anonymity.sh` retorna vazio.
- [ ] `scripts/validar-acentuacao.py --check-file` verde nos arquivos tocados.
- [ ] Teste de parsing do `pactl get-default-source` / `wpctl status` (fixture com `*` em fonte != DualSense, e fixture com DualSense único).

## Arquivos tocados

- `scripts/fix_wireplumber_default_source.sh` (verificação do ativo + três estados).
- `scripts/doctor.sh` (`check_wireplumber_source` lê o ativo).
- `tests/unit/` — fixtures de saída de `wpctl status` / `pactl get-default-source`.

## Proof-of-work runtime

```bash
# webcam desconectada (DualSense único):
bash scripts/fix_wireplumber_default_source.sh --install; echo "exit=$?"   # espera aviso "único" + exit != 0
scripts/doctor.sh | sed -n '/áudio/,/Steam/p'                              # espera [WARN], não [ OK ]
# webcam conectada (fonte sã available):
bash scripts/fix_wireplumber_default_source.sh --install; echo "exit=$?"   # espera OK + exit 0
pactl get-default-source                                                   # != DualSense
```

## Fora de escopo

- Mudar o comportamento de rebaixar para desabilitar — isso é opt-in em [[FEAT-WIREPLUMBER-DISABLE-SOURCE-MODE-01]].
- Política de *sink* (saída) do DualSense.
- Eleição de mic em contexto headless (postinst root sem sessão WirePlumber).
