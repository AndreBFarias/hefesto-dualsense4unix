# workflow lugar-a-mesa

- runId: wf_eb426e8d-5f7 | status: completed | agentes: 10 | tokens: 1,093,511 | duracao: 37 min
- summary: Diagnosticar e desenhar por que controle externo nao vira jogador no co-op, com a medicao ao vivo dos tres controles
- fases: Medir, Desenhar, Escrever

## RESULTADO

### doc

Sprint escrita, staged (não commitada), quatro portões verdes, e nenhum MAC (nem com separador, nem 12 hex colados) no arquivo.

`/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md`

**O desenho escolhido — UNIFICAR: o externo vira jogador de primeira classe.** Descoberta única de gamepads, normalizador de eixo por `absinfo`, grab, vpad próprio para cada externo e esconde-esconde por par VID/PID. Venceu porque é o **único dos três candidatos que fecha a queixa que ela fez**: os outros dois consertam a legenda, e ela não reclamou da legenda — reclamou de três controles disputarem o mesmo jogador dentro do jogo. Sustenta-se em coisa que já existe: o invariante *"um controle físico produz UM dispositivo de jogo"* (`launch_env.py:44-48`), a fila unificada (`identity.py:543`) que o co-op já consulta para acender a lâmpada, e o promotor do co-op que **já aceita externo por escrito** (`coop.py:567-574`) e nunca recebe nenhum, porque `coop.py:333-337` só enumera `discover_dualsense_evdevs()`.

Cinco enxertos dos juízes entraram: nasceu a **E0** (a luz e a boca param de afirmar antes de tudo), a claim *"para em qualquer degrau sem mentir"* foi registrada como **falsa**, a cura barata (`auto_numbers` OFF, que já existe) foi precificada, a E1 foi partida em CLI-barata e GUI-cara, e lista vazia virou **"não sei"** em vez de zero. Correção de mecanismo: no 8BitDo em modo PS4 o que acende é a **cor** do slot (`write_lightbar_slot`), não barra de jogador — a mentira é a mesma, o teste é outro.

**As três coisas abertas:** (1) **ninguém no Linux diz ao jogo quem é o jogador N** — o jogo numera por ordem de enumeração, e a luz pode dizer 2 enquanto o jogo diz 3, mesmo com a entrega inteira; (2) **o que fazer com a luz até a E3** — manter a mentira, calar de vez (custa a cura medida da R-24/R-25) ou calar só com jogo aberto (contradiz `external_identity.py:930-933` e some com o número em Wayland puro); (3) **grab e FF em aparelho não-Sony são SEM PROVA** — ninguém nesta casa jamais grabou um `hid-nintendo`, e é o pressuposto central da E3.

O **VETO** está registrado nos três lugares (`QUATRO-NO-RÁDIO-01`, `coop.py:770-776`, `lifecycle.py:1411-1414`): E0/E1/E2 não o reabrem; **E3 e E4 não existem sem a palavra dela**. Relações declaradas: absorve a entrega 2 da MÁSCARA-01 e as 1/5 da CONTAGEM-01, contradiz a entrega 2 da CONTAGEM-01 (já caduca desde 29/07), depende de IDENT-01 e REGRA-NÃO-REGISTRO-01 só na E3, torna o IDENTIDADE-DUPLA-01 mais grave sem curá-lo, é vizinha da QUATRO-NA-MESA-01, e **contradiz o alcance** da POSSE-POR-CONTROLE-01 — a E3 cria saída para aparelhos que estão fora do modelo de precedência por MAC do backend.

### vencedora

externo-vira-jogador

### placar

[
  {
    "angulo": "externo-vira-jogador",
    "nota": 7
  },
  {
    "angulo": "duas-contabilidades-que-se-falam",
    "nota": 7
  },
  {
    "angulo": "a-verdade-primeiro",
    "nota": 6
  }
]


## LOGS

externo-vira-jogador: 7
duas-contabilidades-que-se-falam: 7
a-verdade-primeiro: 6
