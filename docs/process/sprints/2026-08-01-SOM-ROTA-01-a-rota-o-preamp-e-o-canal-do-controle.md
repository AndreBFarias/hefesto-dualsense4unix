# SOM-ROTA-01 — a rota, o pré-amplificador e o canal do controle

- **Status:** PROPOSTA, escrita em 01/08/2026 para sobreviver à queda da sessão
- **Prioridade:** ALTA — destrava 60% do controle deslizante que hoje é inerte,
  e entrega o efeito que ela descreveu com o Zelda
- **Fonte:** [a referência canônica do protocolo](../../protocol/dualsense-referencia-canonica.md),
  §3
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)

## A pergunta de desenho que ela fez, e a resposta

Ao saber que o kernel escreve três campos e nós escrevemos um, ela perguntou:

> *"então aqui a solução de design é setar pra impedir que o user quebre a
> feature?"*

**Não. É o contrário, e a diferença importa para o desenho inteiro.**

A curva que ela mediu em 01/08 — **mudo até 38, satura em 102**, 60% do curso
inerte — não é o usuário quebrando nada. É o registrador de volume lutando
contra um **ganho de entrada no valor padrão**. O kernel 6.18, para fazer o
alto-falante soar quando o fone sai, escreve **três** campos:

```c
common->audio_control  = FIELD_PREP(...OUTPUT_PATH_SEL, 0x3);   /* a ROTA */
common->speaker_volume = 0x64;                                  /* 100 */
common->audio_control2 = FIELD_PREP(...SP_PREAMP_GAIN, 0x2);    /* o PRÉ-AMP */
```

Escrevendo os três, **o curso inteiro passa a valer**. A entrega é dar a ela
mais alcance, não menos — e é assim que a sprint deve ser desenhada e escrita
na tela.

**O "impedir que quebre" é outro eixo, e já está resolvido nesta casa:** assim
que o Hefesto manda volume, ele **toma a posse** do registrador e o botão físico
do controle para de valer. Por isso existe o botão **Devolver**, e por isso a
dica avisa antes do clique. Essa disciplina não muda nesta sprint — ela se
estende aos campos novos.

## O que existe hoje, e o que falta

| campo | offset | escrito hoje? |
|---|---|---|
| `headphone_volume` | 4 | sim |
| `speaker_volume` | 5 | sim |
| `mic_volume` | 6 | **não** (e o máximo é `0x40`, não `0xFF`) |
| `audio_control` (a rota) | 7 | **não** |
| `audio_control2` (o pré-amp) | 37 | **não** |

E falta a constante do bit que valida o pré-amp: `valid_flag1` **bit7**
(`AUDIO_CONTROL2_ENABLE`) não existe em `core/ds_output_report.py`.

## Entregas

### E1 — os três campos que fazem o alto-falante soar

`set_audio_volumes` passa a aceitar `mic` e `path`; `_build_common` passa a
escrever `common[6]`, `common[7]` e `common[37]`, cada um com seu bit de
autorização.

**Onde:** `core/backend_pydualsense.py` (`set_audio_volumes`, `_build_common`) e
`core/ds_output_report.py` (a constante nova).

**Clamps corretos, que hoje estão errados:** o fone é **0–0x7F**, o mic é
**0–0x40**. A árvore trata os quatro como 0–255.

**Armadilha que a `AUDIO-OWNER-01` já pagou:** autorizar um byte sem escrevê-lo
é mandar **zero**. O bit de autorização de cada campo só pode ligar quando
alguém deste projeto escreveu um valor naquele campo. A poda existente
(`flag0 &= ~VALID_FLAG0_AUDIO_MASK`) precisa ganhar os campos novos.

### E2 — a régua do volume é remedida com os três botões

O `core/speaker_scale.py` guarda a curva medida com **só o volume**. Remedir
com a rota em `3` e o pré-amp em `2`, pelo mesmo método instrumental de 01/08
(o microfone do próprio controle como instrumento, com a tela desligada para
excluir o HDMI).

**Expectativa a confirmar:** a faixa útil deixa de ser 64 passos. **Se não
mudar, a hipótese está errada e a E1 precisa ser remedida antes de seguir.**

**Aceite:** a curva nova no lugar da velha, com a data e o método.

### E3 — o caso do Zelda: o efeito no controle, a trilha na TV

Ela descreveu: *"o speaker do controle faz os barulhos da espada do Link
enquanto na tela tem o som que sai normal do jogo"*.

Isso é **`OUTPUT_PATH_SEL = 2`** — canal esquerdo para o fone/TV, canal direito
para o alto-falante do controle. **Um byte.**

A entrega tem duas metades:

- **o byte**: expor a rota na aba de som e no perfil, com as quatro opções
  nomeadas pela consequência (não pelo número);
- **a fonte do som**: um caminho no PipeWire que mande "só o que vai para o
  controle" no canal direito. Esta metade é a cara — é UX e roteamento de
  áudio, não protocolo.

**Aceite:** ela consegue mandar um som só para o alto-falante do controle
enquanto o resto do áudio segue na saída normal.

### E4 — o microfone ganha os campos que nunca teve

`audio_control` também carrega o **caminho do microfone**: forçar o interno,
forçar o do headset, cancelamento de eco, cancelamento de ruído, e o
`INPUT_PATH` (ambos / chat / ASR). E `audio_control2` bit4 é o **beam forming**.

**Por que isto entra nesta sprint e não na do mic:** é o mesmo byte, e mexer
nele em duas levas separadas é convidar a segunda a apagar a primeira.

**Alvo declarado:** o `BT-MIC-GATING-01` — o firmware declarando o mic mudo em
55-75% dos quadros — **nunca foi remedido depois da cura de 25/07**, e ganha
aqui quatro hipóteses novas e testáveis.

### E5 — a detecção de fone deixa de ser adivinhação

O byte 53 do report de **entrada** carrega `HP_DETECT` (bit0), `MIC_DETECT`
(bit1) e `MIC_MUTE` (bit2) — novidade documentada no kernel 6.18.

Hoje o projeto **adivinha** se há fone plugado. Com esses bits, não precisa. E
isso conecta com um furo do gamepad virtual: **ele nunca escreve o byte 53**,
então anuncia "fone sempre plugado" — o pior default possível justamente para o
caso do alto-falante.

## Testes que vão reprovar

`pytest tests/unit -k "audio or speaker or som"`.

| teste | por quê |
|---|---|
| `test_audio_owner_report.py` | trava que os bytes de áudio saem zerados e sem autorização quando não há dono. A E1 acrescenta campos — a regra continua, a lista muda |
| `test_daemon_speaker_wiring.py` | o applier de perfil **não pode** armar a trava `audio`. O comentário diz que *"o teste da SEGUNDA ativação é o mais importante do arquivo"* |
| `test_speaker_regua_unica_cli_e_janela.py` | a régua é dono único. A E2 remede — o número muda, o dono não |
| `test_som_02_devolucao_da_posse.py` | a devolução da posse. Os campos novos entram nela |

## O que NÃO fazer

- **Não desenhar isto como "proteger o usuário".** A entrega é destravar o
  curso, não limitá-lo. Ver a seção de abertura.
- **Não autorizar byte sem escrever valor** — é mandar zero, e foi o defeito que
  a `AUDIO-OWNER-01` curou.
- **Não mexer no `common[7]` sem o `OUTPUT_PATH_SEL` inteiro.** O byte carrega a
  rota **e** o caminho do mic; escrever meio byte muda o outro meio.
- **Não prometer restauração na devolução.** O DualSense não devolve o volume:
  não há report de entrada nem feature que o leia. "Devolver" devolve o
  controle, nunca o valor.
- **Não esquecer que a camada 1 vence a camada 2.** Volume perfeito num sink
  mudo no PipeWire é trabalho invisível.
