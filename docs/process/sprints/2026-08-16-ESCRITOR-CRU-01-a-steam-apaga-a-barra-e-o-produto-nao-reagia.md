# ESCRITOR-CRU-01 — a Steam apaga a barra, e o produto não reagia

- **Escrito em:** 16/08/2026, 01h, depois de uma madrugada que ela virou medindo.
- **A hipótese é DELA**, levantada enquanto eu perseguia a pista errada:
  *"não é pq a steam tá aberta?"*
- **Estado:** cura na árvore, com teste que morde. **A palavra final na tela é
  dela** ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).

---

## 1. A medição que é o alicerce

Par de eliminação completo, **feito por ela**, nada mais tocado entre os dois
lados:

| condição | o que a barra faz |
|---|---|
| **COM** a Steam aberta | fica **APAGADA** depois de cada comando nosso |
| **SEM** a Steam | volta ao **verde sozinha** |

E o mecanismo, medido no mesmo minuto:

- a Steam segurava os **OITO** `hidraw` (4 a 11);
- o daemon **não reagiu em 60 s**: zero linhas de lightbar, de gatilho ou de
  defesa no journal;
- `lightbar_escritor_estrangeiro` deu **ZERO em três horas**;
- o `sysfs` leu `[0 255 0]` com a barra **apagada** e `[0 255 0]` com ela
  **verde** — o mesmo valor nos dois estados.

**Isto derruba o Aviso 3 do estudo
[A LIGHTBAR TRAVADA](../estudos/2026-08-15-A-LIGHTBAR-TRAVADA-o-que-ja-caiu-e-o-que-nunca-foi-tentado.md)**
(*"a Steam saiu da mesa"*, 15/08, decisão dela). Quem a devolveu à mesa foi ela
mesma, com ensaio pareado — e o item **5.9** daquele estudo (*"a Steam APAGAR a
barra em regime"*, um dos nove `inconclusivo` do caderno) fica **fechado**.

---

## 2. Por que o detector que existia deu zero

A casa tinha UM detector de escritor alheio: o `verify=True` do
`SysfsLedNode.set_rgb`, que re-lê `multi_intensity` e compara com o que
pedimos. Ele **não vê a Steam** — e a docstring do próprio arquivo já dizia por
quê desde 12/08:

> *"escrita CRUA por hidraw que não passa pela classe LED segue INVISÍVEL a
> esta re-leitura"* — `core/sysfs_leds.py`

A Steam escreve exatamente assim. O ZERO não era boa notícia: era **cegueira**,
e ela foi lida como "ninguém está escrevendo". Isso agora é um teste
(`test_a_classe_led_nao_ve_o_escritor_cru`), para que o silêncio daquele
detector nunca mais seja lido como prova.

O `defend_display()` existe e é chamado — mas só sob **réplica de exibição
RETIDA**, que é evidência que nunca chega quando a escrita alheia é crua.

---

## 3. As quatro decisões, e o que decidi em cada uma

### (a) COMO DETECTAR sem a classe LED

Três caminhos na mesa; escolhi o terceiro:

1. **Reler a cor pelo hidraw (feature report).** É a régua que falta (item 5.1
   do estudo), mas **nenhum** dos dezessete feature reports lidos em 14-15/08 é
   conhecido por devolver estado de LED; o `0x22` nunca foi lido por este
   projeto e o `0xf6` não é nomeado em documento nenhum. Some-se o retry do
   `REPORT_REQ_TIMEOUT` de 3 s do BlueZ. **É ensaio de bancada, não detector de
   regime** — e continua aberto;
2. **Comparar o pedido com o que o aparelho reporta.** O report de INPUT do
   DualSense não carrega a cor da barra. Não há o que comparar;
3. **Ver quem SEGURA o nó**, por `/proc/<pid>/fd`. Foi o que a madrugada
   observou, custa ~6 ms para ~4600 fds, funciona sem root e **não toca o
   aparelho**. É o que entrou: `core/escritor_cru.py`.

**O que ele NÃO vê, dito antes que alguém descubra do jeito caro:** só
reconhece a **Steam** (a varredura é restrita aos PIDs dela, os mesmos padrões
do `steam_running` canônico); não sabe QUANDO ela escreveu, só que ela pode; e
degrada em silêncio — ausência de sonda é **"não sondado"**, nunca "ninguém
segura".

### (b) O CUSTO DO MARTELO — quantas escritas por hora

**Primeiro, a confirmação que o orquestrador pediu:** o cache do nó sysfs
**já não faz** o trabalho que o `GUERRA-01` lhe deu. Lido no fonte:
`sysfs_leds.discover()` constrói `SysfsLedNode` **novos** a cada chamada, e
`_refresh_sysfs_leds` troca `self._sysfs` pelo mapa novo em **todo**
`connect()` — que é o tique de 30 s. O `_last_write` não atravessa um tique;
ele só deduplica dentro dele. Quem mantém o tique quieto hoje é outra coisa: o
`reassert_resolved_outputs` **não é chamado** no tique, e o `new_keys` do
priming sai vazio quando o `indicator_dir` não mudou.

Com isso na mesa, o custo desta cura:

| cena | sondas | **escritas** |
|---|---|---|
| mesa parada, Steam aberta o dia inteiro | 2/min (`pgrep`) | **0/h** |
| Steam subindo (uma borda) | idem | **1 por controle, uma vez** |
| ela mexendo na GUI | reaproveita a foto de 5 s | **1 por rajada** de comandos |

A rajada é o `GATILHO-DA-COR-01` que já existia: cada comando **RE-ADIA**, e a
reafirmação sai 1,5 s depois que a sequência sossega. Arrastar o seletor de cor
por dez segundos produz **uma** escrita, não cem.

Comparação com o defeito que o `GUERRA-01` tirou do produto: aquele reassert
escrevia **incondicionalmente** a cada 30 s (120 escritas/h por controle, sem
evidência nenhuma). Este escreve **zero** enquanto ninguém mexe.

### (c) QUEM DEVE GANHAR

O Hefesto prevalece — **menos em Modo Nativo**, regra dela, literal: *"no modo
nativo devolvemos o controle pra steam e no modo conexão também, todo o resto é
o hefesto"*. Ali o escritor cru não é intruso: é o dono. O no-op é **TOTAL** —
nem a sonda roda (há teste que conta as chamadas dela). O `_output_mute` já
protegia a escrita; agora protege também a vigilância.

### (d) O SYSFS MENTE

Nenhuma linha desta cura decide coisa alguma lendo `multi_intensity`. A
evidência é o `fd`, que é observável. E a consequência mais importante é na
tela — ver §5.

---

## 4. O que mudou no código

| arquivo | o quê |
|---|---|
| `core/escritor_cru.py` **(novo)** | a sonda (`pids_da_steam`, `holders_de_hidraw`), o `Veredito` imutável e o `SentinelaDeEscritorCru` (cache + **borda**) |
| `core/backend_pydualsense.py` | contador `_pinturas_de_lightbar` no `_pintar_por_hidraw_bt`; `consumir_pinturas_de_lightbar()`; `nos_hidraw_por_uniq()` |
| `daemon/connection.py` | `sentinela_de_escritor_cru_de` e `vigiar_escritor_cru` — os dois eventos novos do gatilho da cor |
| `daemon/ipc_handlers.py` | campo `lightbar_disputada` por controle; a sonda de holders do 8BIT-01 passa a ser a MESMA do core |
| `app/widgets/controller_card.py` | a frase nova no card |
| `daemon/lifecycle.py`, `daemon/protocols.py` | o atributo do sentinela |

**A cura é o encontro de duas coisas que a casa já tinha e ninguém tinha
ligado:** o report `0x31` avulso que **venceu a Steam** na bancada de 12/08
(`reescrever_lightbar_por_hidraw`) e o mecanismo que **espera a rajada passar**
(`GatilhoDeFimDeSequencia`). O que faltava era o **evento**: o gatilho era
armado por conexão nova e por transição de jogo, e **nunca pelo comando dela**.

Os dois eventos novos, e cada um responde a uma metade da medição:

- `pintura_com_escritor_cru` → *"a barra apaga depois de cada comando nosso"*;
- `escritor_cru_novo` (a borda) → *"o daemon não reagiu em 60 s"*.

---

## 5. Na tela

A aba Status mostrava a cor que o produto **PEDIU** como se fosse a acesa — que
é justamente a mentira que a madrugada mediu. O card ganhou uma frase, no mesmo
lugar e no mesmo tom da que já existe para o Modo Nativo:

> **A Steam também escreve nesta barra**

A bolinha continua na última cor NOSSA (é a informação que existe). O que muda
é que ninguém mais afirma "verde" nem "apagada" sem ter medido. Precedência:
**Nativo > disputada > desconhecida > apagada > cor**.

`lightbar_disputada` sai da **foto** do sentinela (tirada no tique de 30 s):
o handler de status roda a cada segundo e **não** toca `/proc`. Sem sonda o
campo é `False` — um aviso aceso por falta de dado treinaria a usuária a
ignorá-lo.

Retrato do estado novo:
`scratchpad/olhar-disputada/readme_status.png` (fora do repositório — as
imagens da documentação **não** foram trocadas: mostrar o aviso no retrato
padrão é decisão dela).

---

## 6. No install

**Nenhum arquivo novo fora do pacote:** sem regra udev, sem config, sem unidade
de serviço. `core/escritor_cru.py` entra pelo mesmo caminho de todo módulo de
`src/hefesto_dualsense4unix/` — o `check_packaging_parity.sh` cobre isso, e a
cura vale no **próximo start do daemon** (install *editable*: o daemon vivo é
mais velho que o código).

---

## 7. O que fica ABERTO, e é dela

1. **A frase no card.** É a tela dela. Se "A Steam também escreve nesta barra"
   não for a palavra certa, o lugar de mudar é uma linha
   (`rotulo_lightbar`);
2. **Mostrar o aviso no retrato da documentação?** Há precedente dos dois
   lados: o aviso do "perfil que não entrou" aparece de propósito na aba No
   jogo (*"uma imagem que só mostra o caso bom ensina a não procurá-lo"*);
3. **Por CABO a reafirmação não sai.** O `reescrever_lightbar_por_hidraw`
   filtra `transport == "bt"`, porque foi o rádio que a bancada mediu. Os
   controles da madrugada estavam no rádio (`0005:054C:0CE6`), então a cura
   alcança a mesa de hoje — mas um DualSense no cabo com a Steam aberta
   continua sem reafirmação, e isso **nunca foi medido**;
4. **Um segundo escritor cru passa despercebido** — a sonda só conhece a Steam;
5. **A régua que falta continua faltando** (item 5.1 do estudo): ler o estado
   da barra NO APARELHO. Enquanto ela não existir, "quem ganhou a disputa" é
   pergunta para o olho dela, não para o software.
