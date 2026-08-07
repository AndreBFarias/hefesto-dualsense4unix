# SEM-MICROFONE-NENHUM-01 — sem nenhum mic, o alto-falante vira a entrada padrão

- **Medido em:** 06/08/2026, na máquina dela, entre 20h50 e 21h10
- **Estado:** ABERTA. O sintoma foi curado no TEXTO (o doctor parou de mandar
  rodar um comando impotente); a **política** não foi mexida — é o trabalho
  desta sprint, e depende de uma medição que ainda não foi feita
- **Gravidade:** alta para um projeto open source — é privacidade, e o estado
  defeituoso **não parece** defeituoso
- **Pré-requisito:** a medição do item "O que precisa ser medido ANTES"

---

## O sintoma

Sem webcam, sem mic plugado no jack e com o DualSense fora do cabo, o
WirePlumber elegeu como **fonte de captura padrão**:

```
alsa_output.pci-0000_0c_00.4.iec958-stereo.monitor
```

Um **monitor** é o loopback da SAÍDA. Enquanto ele for a fonte padrão, todo
aplicativo que grave sem escolher a fonte na mão capta **o áudio que sai do
computador** — o jogo, a música, a chamada inteira — e nunca a voz.

E o pior: **não parece quebrado.** O medidor de nível mostra sinal. Passa por
"funcionando".

Resolveu-se sozinho quando ela plugou uma webcam. Numa máquina **sem** webcam e
**sem** mic, o produto deixa o sistema assim — calado.

---

## O mecanismo, medido na fonte instalada (WirePlumber 0.5.12)

**Quem elege é o WirePlumber, não o pipewire-pulse.**
`/usr/share/wireplumber/scripts/default-nodes/rescan.lua:68-70`:

```lua
    pushSelectDefaultNodeEvent (source, si_om, devices_om, "audio.source", "out", {
      "Audio/Source", "Audio/Source/Virtual", "Audio/Duplex", "Audio/Sink"
    })
```

`Audio/Sink` está na lista de candidatos a **fonte** padrão. Os sinks têm portas
de direção `out` (`monitor_FL`/`monitor_FR`), então passam o filtro de
`collectAvailableNodes`.

A conta que fecha, por `priority.session` medido com `pw-dump`:

| nó | classe | prioridade |
|---|---|---|
| entrada da onboard | Audio/Source | 2009 |
| webcam C920 | Audio/Source | 2109 |
| **sink iec958 (o que venceu)** | **Audio/Sink** | **736** |
| sink HDMI | Audio/Sink | 696 |

A entrada da onboard, apesar de existir, é **descartada antes da disputa**: as
três portas de captura dela estão `not available` (nada plugado no jack), e
`haveAvailableRoutes` a tira da lista. Sem webcam, sem controle e com a onboard
descartada, **sobram só os dois sinks** — e o de maior prioridade vira a
"fonte". Quando a C920 entrou (2109 > 736), ganhou sozinha.

---

## O que é NOSSO nisto (e é a parte incômoda)

O achado original supunha que a culpa fosse dos drop-ins 52 e 53. **Não é** — e
a correção de premissa importa: `install.sh:204-205` traz
`WITH_WIREPLUMBER_DISABLE_MIC=0`, e a máquina dela tem **só** o
`51-hefesto-dualsense-no-default-source.conf` instalado (conferido por md5
contra o asset).

O culpado nosso é o **51**, que é a política **default** do install.
`assets/wireplumber/51-hefesto-dualsense-no-default-source.conf:62-79` rebaixa o
mic do DualSense para `priority.session = 50` — contra sinks de **696 e 736**.

**Consequência:** numa máquina em que o DualSense é o **único** microfone (que é
o caso de muita gente que instala um driver de DualSense), o mic do controle
perde para **qualquer alto-falante**, e o monitor ganha. **O nosso drop-in
default fabrica o estado que o nosso próprio doctor reprova como `[FAIL]`.**

Na máquina dela isso hoje não aparece porque a pilha persistida salva o dia
(`state-default-nodes.lua:48` soma `+20001 - i` a quem está no histórico, e o
mic do DualSense está lá). **Numa instalação nova não há pilha.**

### Duas das três linhas do 51 são INERTES (MEDIDO)

- **linha 69** — `{ node.name = "~alsa_output.*[Dd]ual[Ss]ense.*[Mm]onitor" }`:
  `node.name` de sink **nunca** contém "monitor". O `.monitor` é sufixo da
  camada pulse, não nome de nó (medido: os nomes reais são
  `alsa_output.pci-...iec958-stereo`, e o próprio state dela guarda
  `...analog-surround-40`, **sem** `.monitor`). A correção de 30/07 descrita nos
  comentários do arquivo **não pegou** — e nem bastaria, porque o sink que
  venceu em 06/08 foi o da **onboard**, não o do controle;
- **linha 66** — `{ device.name = "~alsa_card.*DualSense.*" }` casa o objeto
  **device**, e os nós ALSA não carregam `device.name` (só `device.id`,
  `device.api`, `card.profile.device`), enquanto `find-best-default-node.lua:38`
  lê props do **nó**. GRAU: SUSPEITA COM MECANISMO forte.

Das três linhas de `matches`, **só a primeira funciona** — e é justamente ela
que empurra o único microfone da casa para debaixo dos alto-falantes.

---

## O que precisa ser medido ANTES de qualquer entrega

**Isto é o pré-requisito, e é o motivo de esta sprint não ter virado cura hoje.**

`libpipewire-module-protocol-pulse.so` contém as strings `Audio/Sink`,
`Audio/Source`, `priority.session` e `default.audio.source`. É plausível que o
**pipewire-pulse faça a própria seleção** quando a metadata está vazia — e
nesse caso zerar `default.audio.source` **não muda** o que `pactl
get-default-source` devolve, e qualquer cura pelo lado do WirePlumber não
resolveria o sintoma visível. **GRAU: SEM PROVA.**

Sem essa medição, propor entrega é adivinhar.

---

## Os caminhos, e por que três estão descartados

1. **`node.features.audio.monitor-ports = false`** (`node/create-item.lua:38-39`)
   — é a única chave que tira o nó do jogo, mas é **global**: some o monitor de
   **todos** os sinks e quebra gravação de tela com áudio, OBS, tudo.
   **Descartado.**
2. **Rebaixar `priority.session` dos sinks** — não serve: `lib/node-utils.lua`
   usa o **mesmo** getter para a eleição de `audio.sink`. Rebaixar o sink para
   ele perder a fonte é rebaixá-lo para perder o alto-falante. **Descartado.**
3. **`node.disabled = true`** no sink de uso geral — absurdo. **Descartado.**
4. **Um hook lua próprio**, carregado por `wireplumber.components`, rodando
   `after = { "default-nodes/find-best-default-node" }`, que rejeita o nó
   selecionado quando ele é `Audio/Sink` **e** a seleção veio da eleição
   automática. O discriminador é numérico e medido: escolha configurada soma
   `+30000`, histórico soma `+20001 - i`, automático usa a prioridade crua
   (sinks: 696/736). Regra: rejeitar `Audio/Sink` só quando a prioridade da
   seleção for `< 20000`. **Quem pediu o monitor continua com o monitor**; quem
   nunca pediu deixa de recebê-lo por escassez, e o monitor continua listado e
   selecionável. Custo honesto: é script lua na config dela, não um `.conf`
   declarativo — mais superfície, e amarrado a nomes de hook do 0.5.x.

---

## Qual é o comportamento CERTO sem microfone nenhum

O upstream já implementa "nenhuma fonte padrão" nativamente:
`apply-default-node.lua:35-37` faz `metadata:set (0, "default.audio.source",
nil, nil)` quando nada foi selecionado. Não é estado exótico — é o caminho
previsto.

1. **Nenhuma fonte padrão** — o mais honesto. "Não há microfone" é a verdade; o
   aplicativo pergunta, ou falha de forma visível. Depende inteiramente da
   medição pendente.
2. **Fonte nula** (`Audio/Source/Virtual`, aceita em `rescan.lua:69`) — troca
   "gravei o desktop" por "gravei silêncio". Melhor para privacidade,
   igualmente confuso, e acrescenta um nó permanente à máquina de quem instalou
   um driver de **joystick**. Fora do nosso mandato.
3. **Monitor com aviso** — o estado atual, e o pior dos três em privacidade.

Comparação com outros ambientes de áudio: **SEM PROVA.** Não medi, e não
promovo lembrança a fato.

---

## Aceite

1. a medição do pipewire-pulse está feita e escrita, com grau;
2. o drop-in 51 deixa de rebaixar o mic do DualSense **abaixo dos sinks** —
   qualquer que seja a política, um microfone de verdade não pode perder para
   um alto-falante;
3. as linhas 66 e 69 do 51 saem ou passam a casar de fato, com teste que prove
   qual dos dois (hoje elas são decoração, e atravessaram duas revisões);
4. existe teste que modele a ELEIÇÃO, não só o sintoma — hoje `grep
   'priority.session\|Audio/Sink'` em `scripts/doctor.sh` e em
   `src/hefesto_dualsense4unix/core/system_check.py` devolve **nada**, e foi
   por esse buraco que o furo do 51 passou duas vezes;
5. arrancar a cura escolhida faz o teste reprovar.

---

## O que JÁ foi curado em 06/08 (e não é esta sprint)

- o `check_default_source_monitor` deixou de mandar rodar `--fix-mic` quando
  não há fonte alguma para eleger — a receita levava a um comando impotente;
- o check passou a oferecer **o mesmo alvo que a cura elegeria** (antes
  oferecia a onboard, que a cura recusa e o WirePlumber desfaz);
- a cura passou a dizer a consequência: enquanto durar, tudo o que se gravar é
  o áudio de saída.

Nada disso muda a política de eleição. O sintoma ficou honesto; a causa ficou.

---

## Relacionado

- FONTE-PADRAO-01 — o registro do defeito e da cura vive no teste
  `tests/unit/test_fonte_padrao_01_e_cura_do_fix_mic.py`, com as medições de 26,
  29 e 30/07 no cabeçalho
- [DIALOGO-QUE-MATA-A-JANELA-01](2026-08-06-DIALOGO-QUE-MATA-A-JANELA-01-o-aviso-que-deixou-a-janela-dela-morta.md)
  — a mesma classe: a receita que leva ao lugar errado
- [A noite em que o som do controle voltou](../estudos/2026-08-04-a-noite-em-que-o-som-do-controle-voltou.md)
