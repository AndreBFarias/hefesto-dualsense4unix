# Para esta página valer de verdade

O mockup mostra **como tudo deve ficar ao final das sprints** — não o que dá para
fazer hoje. Esta lista é a diferença entre os dois.

## Depende de outra frente

| # | O quê | Onde está hoje | O que falta |
|---|---|---|---|
| 1 | **Cor do plástico por rádio** | Provado possível numa outra máquina; a leitura por cabo já funciona (ensaio E7, `cor_do_plastico.py:159-165`) | Medir nesta bancada e levar a leitura para dentro do produto — hoje ela só existe em `scripts/ensaios/` |
| 2 | **Borda na cor do plástico** | Desenhado em `ONDE-A-COR-MORA-01` (D-16, D-17, D-18); custo estimado ~120 linhas em `status_actions.py`, ~30 no `theme.css` | Executar. A aba Configurações **consome** essa borda, não a implementa |
| 3 | **O tom de cada cor** | O aparelho entrega `05`, a tabela entrega *Starlight Blue*, e **ninguém entrega um RGB** | Definir os seis tons. É pergunta aberta da própria `ONDE-A-COR-MORA-01` |
| 4 | **Número de jogador fixo por controle** | `identity.number.set` existe, funciona nos dois registros | A GUI nunca oferece para controles externos |
| 5 | **Máscara por aparelho** | `ExternalMaskRegistry.set_mask` pronto e **sem chamador** desde 15/08 | Ligar aos três degraus fora do módulo (`virtual_pad`, `coop.py`, `gamepad.py`) e o lado da escrita |
| 6 | **`doctor.sh --json`** | O doctor tem 4920 linhas e 26 funções de diagnóstico, só em texto | Modo de saída aditivo — ver [CONFIG-09](CONFIG-09-esta-tudo-certo.md) |
| 7 | **Escala tipográfica** | Backend pronto, escala 0-8 | Nunca teve tela — ver [CONFIG-07](CONFIG-07-a-janela.md) |

## Nasce nesta leva

| # | O quê | Sprint |
|---|---|---|
| 8 | `maquina.json` — a camada de configuração que não é de perfil | [CONFIG-03](CONFIG-03-a-declaracao-persiste.md) |
| 9 | O medidor de ocupação do rádio | [CONFIG-04](CONFIG-04-o-medidor-de-radio.md) |
| 10 | Orçamento como teto sobre as features das outras abas | [CONFIG-05](CONFIG-05-orcamento-como-teto.md) |
| 11 | Detecção de hub e de rádios concorrentes | [CONFIG-02](CONFIG-02-o-que-a-mesa-ja-sabe-dizer.md) |

## Nasce da revisão de interface

| # | O quê | Onde | Estado |
|---|---|---|---|
| 12 | **Escolher a cor do plástico** quando a leitura falha | Card do controle | A lista de seis cores existe em `cor_do_plastico.py:159-165`; falta o RGB de cada nome |
| 13 | **Altura igual entre cards** de controles diferentes | `Gtk.Grid` com `row_homogeneous=True` | Desenhado; ver [CONFIG-06](CONFIG-06-controles-que-nao-sao-dualsense.md) |
| 14 | **Campo livre em "Outro"** na lista de rádios | Seção "A mesa" | `Gtk.Entry` que aparece com a opção marcada |
| 15 | **Cinco controles simultâneos na tela** | Toda a aba | O fixture de captura hoje é de quatro (`--mesa-cheia`); precisa de um de cinco |

## Scripts que precisam de atualização

| Script | O que muda | Por quê |
|---|---|---|
| `scripts/gui-captura/retratar_abas.py` | Passa a fotografar **onze** abas, e `NOMES` ganha `readme_configuracoes` | O script confere os nomes no fim e avisa se a documentação não bate |
| idem | Fixture novo de **cinco** controles, ao lado do `state_full_quatro_controles.json` | A mesa real desta casa é de cinco; a captura de quatro não mostra o pior caso de largura |
| `scripts/doctor.sh` | Modo `--json` aditivo, sem tocar na saída de texto | É a fonte única da seção "Está tudo certo?" — ver [CONFIG-09](CONFIG-09-esta-tudo-certo.md) |
| `scripts/doctor.sh` | `hci0` fixo em `:2555`, `:2563`, `:2823` | Mente numa mesa de dois ou três adaptadores, que é o caso desta leva |
| `scripts/ensaios/cor_do_plastico.py` | A leitura sai de `ensaios/` e entra no produto | Hoje a cor só existe fora do app |
| `scripts/validar-palavra-de-tela.py` | Roda sobre os rótulos novos | Portão de pré-commit; a aba tem ~110 textos novos |

**Uma armadilha do ambiente, registrada:** `retratar_abas.py` morre com
`Failed to load ... image-missing.svg` quando o terminal é um snap — ele exporta
o cache de loaders do próprio confinamento. A cura é
`GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache`
antes de chamar. Mesmo problema que o commit `911d099` tratou para o ícone da
bandeja.

## Medições pendentes

Nenhuma bloqueia a leva; todas melhoram o que a aba consegue afirmar.

1. Cor do plástico por rádio nesta bancada — item 1 acima.
2. O modelo do 8BitDo desta casa: SN30 Pro ou SN30 Pro+.
3. Default da Steam para `SteamController_SwitchSupport` quando a chave não existe.
4. Se o Hefesto enxerga o controle em modo D-input.
5. Se as quatro luzes do plástico do 8BitDo respondem ao comando de lightbar.
6. **O RGB de cada nome de cor.** O aparelho entrega `05`, a tabela entrega
   *Starlight Blue*, e ninguém entrega um tom. É pergunta aberta da própria
   `ONDE-A-COR-MORA-01`, e a borda dos cards depende dela.
7. **O conflito do jogador 4 — DECIDIDO em 21/08.** Ele é rosa
   `(255, 0, 128)` na paleta de lightbar (`core/led_control.py:146`), e rosa é a
   cor da marca e da aba ativa. **A paleta da interface passa a ser remapeagem
   da de hardware**, não cópia: a tela deriva os tons de identidade sem herdar a
   colisão. O hardware não muda — as cores que ela já viu na bancada continuam
   as mesmas.

## A dívida que a aba não pode aumentar

**"Poupar bateria" já é promessa feita na tela hoje, sem número medido por trás.**
Não existe medição de mA nem de horas de autonomia neste projeto. O orçamento
diz consequência verificável — *"a vibração chega com no máximo 40 % da força"* —
e nunca uma porcentagem de bateria economizada.

Converter o desconto de rumble em minutos de autonomia é sprint própria, e vale
a pena. Mas é outra.
