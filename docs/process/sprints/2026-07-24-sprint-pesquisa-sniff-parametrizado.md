# Sprint (pesquisa): afinar o SNIFF em vez de recusá-lo — eliminar o split por-OUI

**Status**: PESQUISA ABERTA. Nada implementado. A correção vigente
(`BT-SNIFF-PER-OUI-01`, 23/07) resolve o problema e é de raiz; esta sprint
investiga se dá para ir **um nível acima** e apagar o caso especial.
**Dona da decisão**: mantenedora. Só vale abrir se a A der trabalho de manter.

## O que já está resolvido (contexto, não repetir)

O A/B de 23/07 provou que os dois controles da linhagem Nintendo têm requisitos
de firmware **incompatíveis entre si**:

| | Pro genuíno (`e0:f6:b5`) | 8BitDo clone (`e4:17:d8`) |
|---|---|---|
| SNIFF permitido | cai sob carga | **funciona** |
| SNIFF recusado | **estável** | probe morre (`-110`) |

Medição: com no-sniff global, o 8BitDo somou **4 probes falhadas / 0 sucessos**,
sempre em `Failed to get joycon info; ret=-110`. Devolvido o SNIFF, probou em
**54 s na primeira tentativa** e ficou de pé. O alias "Nintendo" seguiu aplicado
durante o teste — logo, **o nome não atrapalha o clone**; só o no-sniff.

Entregue: o no-sniff virou **por-conexão, filtrado por OUI** (só o Pro genuíno);
o default do adaptador voltou a permitir SNIFF. Ver `scripts/bt_active_mode.sh`
§2 e `docs/process/estudos/2026-07-23-arqueologia-8bitdo-bt.md`.

## A pergunta desta sprint

O no-sniff é uma **recusa**: o LM local passa a negar `LMP_sniff_req`. É eficaz,
mas é uma marreta — resolve tratando o sintoma do lado do host.

A hipótese é que o problema do Pro não seja o sniff *em si*, e sim o sniff **mal
parametrizado**: intervalos longos demais fazem os reports enfileirarem sob
rumble+IMU até o controle desistir do link. Se for isso, ajustar os intervalos
deixaria o sniff **bom para os dois** — e o split por-OUI poderia ser removido.

## Superfície a investigar

O kernel expõe, por adaptador, em `/sys/kernel/debug/bluetooth/hci0/`:

- `sniff_min_interval` / `sniff_max_interval` — a janela negociada (em slots de
  625 µs);
- `idle_timeout` — quanto tempo de ociosidade antes de propor sniff.

 Armadilha já documentada na pesquisa de 22/07: `conn_min_interval` e
`lecup` são **LE-only** e NÃO se aplicam ao Pro (BR/EDR) — é erro comum nos
guias da internet.

## Perguntas (responder com medição, não com opinião)

- **P1** — Quais são os valores vigentes de `sniff_{min,max}_interval` e
  `idle_timeout` nesta máquina, e o que a spec/kernel usa como default?
- **P2** — Durante uma queda do Pro sob carga **com sniff permitido**, o
  `btmon` mostra o link entrando em sniff antes da queda? Com que intervalo
  negociado? (Sem isso, a hipótese inteira é especulação.)
- **P3** — Reduzir `sniff_max_interval` mantém o Pro de pé sob carga real
  (4 jogadores, rumble+IMU)? Qual o menor valor que ainda economiza energia?
- **P4** — O 8BitDo continua probando com os intervalos ajustados? (Ele precisa
  que o sniff seja **permitido**; não é óbvio que se importe com o valor.)
- **P5** — O ajuste em debugfs **persiste**? Se não, onde ancorar — módulo
  `bluetooth` via `/etc/modprobe.d`, `ExecStartPost` do drop-in, ou udev?
  Debugfs não é interface estável entre versões de kernel: isso é um custo real
  a pesar contra o benefício de apagar o split.

## Critério de sucesso

A sprint só entrega se **todas** valerem:

1. o Pro aguenta uma sessão de 4 jogadores sob carga **sem** o no-sniff;
2. o 8BitDo segue probando e estável na mesma sessão;
3. o ajuste persiste por um caminho suportado (não só debugfs à mão);
4. o resultado é **mais simples** que o split por-OUI — se exigir mais
   maquinaria para manter, a resposta é manter a A e fechar esta sprint como
   "investigada e recusada", o que também é entrega.

## Como NÃO fazer

- Não medir o P2 antes de mexer em valor nenhum = repetir o erro de acoplar
  duas variáveis (nome + no-sniff entraram juntos em `fb5e3ad` e custaram dois
  dias para serem separadas).
- Não rodar A/B com o `hefesto-bt-health-watchdog.timer` ativo: a vigia 0
  reaplica o modo ativo a cada 2 min e contamina o experimento. **Parar o timer
  primeiro** — e lembrar de religar.
- Não usar `hciconfig lp` com a lista separada por espaços: ele lê só o
  primeiro token e o comando vira no-op silencioso (medido 23/07; era o bug do
  `uninstall.sh`). Vírgula: `lp rswitch,hold,sniff,park`.
