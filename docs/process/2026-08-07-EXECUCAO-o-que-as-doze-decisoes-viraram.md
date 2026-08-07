# O que as doze decisões viraram — diário de execução, 07/08/2026

Companheiro de [as doze respostas dela](2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md).
Lá está **o que ela decidiu**; aqui, **o que a decisão virou em código**, em que
ordem, e o que cada onda mediu pelo caminho.

Existe porque ela pediu, com a sessão anterior ainda fresca na memória:

> *"não esquece de ir materializando e documentando os avanços"*

**Grau de cada afirmação:** **MEDIDO** = há teste que reprova com a cura
arrancada, ou medição em bancada com instrumento declarado; **SUSPEITA COM
MECANISMO** = o caminho foi lido e fecha; **SEM PROVA** = está dito e ninguém
verificou.

---

## O método, e por que ele é assim

As ondas são **serializadas por colisão de arquivo**, não por assunto. A lição
que produziu essa regra é de 06/08 e está em [CLEAN-ROOM.md](CLEAN-ROOM.md):
agentes em paralelo mutando a mesma árvore contaminaram **22 medições** e
acusaram de instável uma bancada que não era.

Então, antes de cada onda, os arquivos de cada frente são mapeados. Frentes que
se cruzam **não** correm juntas — mesmo quando o assunto é diferente.

Foi por isso que as três mudanças de interface, que são três assuntos distintos,
foram feitas por **um agente só, em série**: as três tocam o mesmo `main.glade`.

---

## Onda 1 — commit `3745bd1`

Quatro frentes de arquivos disjuntos: licença, língua do produto, notas datadas,
e os dois números do co-op.

| decisão | o que virou |
|---|---|
| 2 e 4 | o `LICENSE` ficou com o MIT canônico e nada antes; o `NOTICE` virou dono da ressalva; curvas em CC0 |
| 10 | o convite a traduzir saiu de onde era falso, com portão que impede voltar |
| — | `LICENSES/` criado (CR-05), com texto canônico e SHA-256 fixado por teste |
| — | `coop status` passou a imprimir os dois números nomeados (E0a) |

### O que a onda 1 mediu, e ninguém tinha medido

**O remédio escrito na sprint estava incompleto.** A CR-05 mandava criar
`LICENSES/GPL-2.0.txt`. Só que `assets/dkms/rtw88-usb/usb.c:1` declara
`GPL-2.0 OR BSD-3-Clause`, e `MODULE_LICENSE("Dual BSD/GPL")` na linha 1504 —
**licença dupla, quem redistribui escolhe**. Mandar só a GPL é mandar um dos dois
caminhos. Entrou também o `BSD-3-Clause.txt`. **Grau: MEDIDO.**

**O portão de anonimato reprovava o texto canônico da GPL** em três linhas —
duas com `made by`, e o `written by James Hacker` que a própria licença dá como
exemplo de aviso de copyright. Não há correção do lado do arquivo: **licença
editada é licença outra**. A exclusão entrou estreita (só `LICENSES/*.txt`), o
`README.md` de lá continua no portão — provado com isca — e os `.txt` não viram
esconderijo porque o SHA-256 está fixado.

---

## Onda 2 — commit `6b1cb62`

Interface (as três, em série) e a lâmpada dos externos.

| decisão | o que virou |
|---|---|
| 1 | a caixinha que TIRA um jogo do Steam Input, no editor do perfil sob o jogo |
| 5 e 6 | "Montar do zero", "Arco de flecha (Bow)", "Disparo (Weapon)" |
| 7 | o interruptor do mic por Bluetooth, no card do controle junto do medidor |
| 12 | a luz calou nos externos |

### Três coisas que a medição decidiu, e não o gosto

**O limite de 22 caracteres não se confirmou.** Remedido em 07/08 com a fonte +3
que ela aceitou e os **dois** lados da aba montados, como o produto monta: o
botão no piso mede **152px** (a sprint registrava 157), e o corte real é **19
caracteres**, não 22.

Três rótulos de 20 quebram na janela encolhida: `Arma semi-automática`,
`Vibração por posição` — que ela nunca foi convidada a rever — e, agora,
`Arco de flecha (Bow)`, que ela **acabou de escolher**. Baixar o teto reprovaria
os três. O teto ficou em 22 e a verdade ficou escrita no teste, com tabela.

**Grau: MEDIDO**, instrumento declarado (PyGObject 3.48.2 / GTK 3.24.41,
`Gtk.OffscreenWindow`). E três armadilhas ficaram registradas para ninguém
repagar: a quebra é por **palavra**; medir **um** lado dá 212px e nada quebra; e
`apply_theme` (`app/theme.py:154`) **compõe** a fonte — duas medições no mesmo
processo não são comparáveis.

**O interruptor do mic mudou de lugar por geometria.** Em linha própria custava
30px de altura e punha a coluna do som em 292px contra 246 da maior vizinha —
um teste reprovou. Passou a dividir a linha do botão "Silenciar": custo zero de
altura. No card compacto o rótulo sai e fica só o interruptor; com ele, dois
cards pediam 1188px numa janela de 1180.

**O texto da caixinha teve de ser reescrito contra a medição dela.** A frase que
o projeto usava — *"o Hefesto sai da frente"* — está **refutada pela metade** pelo
experimento que ela fez em 06/08: a marca entrega a **entrada**, e o Hefesto
**mantém a saída**. A cor e os gatilhos dela seguraram com o jogo aberto.

### Um defeito medido e NÃO curado, por ordem dela

O teste do jogador duplicado nasceu **vermelho**, com `xfail strict`, e a raiz
está escrita: **o número da lâmpada e o número do jogo saem de lugares
diferentes**. A lâmpada vem da fila de identidade (ordem de primeira aparição,
persistida em `controllers.json`); o jogo vem de `player_indexes()`. Ninguém casa
os dois espaços — e o vpad, que só existe no segundo, carrega o número no
**nome**. É por isso que "Hefesto P1" acende 3.

Não foi curado porque a cura toca a adoção dos externos, que ela **adiou** até a
máscara por controle existir.

> **CORREÇÃO DATADA — 07/08/2026: a última frase do parágrafo acima está errada,
> e o resto continua de pé.** O vpad `Hefesto P1` **não** acende 3: ele acende só
> a lâmpada do meio da barra, que é o padrão canônico do jogador **1**
> (`core/led_control.py:105-119` — o número do jogador é o **padrão** das cinco
> lâmpadas, não o nome do nó `:white:player-N`). Quem acende o padrão do 3 é o
> **DualSense físico** — medido de novo em 07/08 lendo os cinco nós de cada
> aparelho, e ela já tinha lido certo de olho: *"o dualsense branco dessa vez
> conectado como player 3"*.
>
> **O diagnóstico do parágrafo sobrevive inteiro, e fica mais preciso:** os dois
> espaços de numeração continuam desencontrados, só que o desencontro não é
> "dois aparelhos no mesmo número" — é **o mesmo jogador exibindo dois números
> diferentes**: `3` na lâmpada do plástico e `P1` no nome que o jogo lê. O
> mecanismo está nomeado no nosso código
> (`integrations/uhid_gamepad.py:351-355`, *"o exato P3"*): o `hid-playstation`
> numera por ordem de registro e conta o nosso vpad como mais um DualSense.
> **GRAU: SUSPEITA COM MECANISMO, forte.** A correção inteira, com a tabela e a
> lição, está na nota datada de 07/08/2026 da
> [LUGAR-À-MESA-01](sprints/2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md).

### E a luz calou sem enterrar a capacidade

A função continua viva e testável; o **chamador** é que está desligado, com a
condição de volta escrita ao lado, e há teste garantindo que ninguém apague o
código. A decisão dela foi *"até a entrega existir"* — então o caminho de volta
tem de ser **uma linha**, não uma leva.

---

## O que ficou aberto, e é dívida conhecida

1. **A frase "o Hefesto sai da frente" está em cerca de 25 lugares** de `src/` e
   `docs/usage/`, e está refutada pela metade desde 06/08. Só os textos tocados
   pela onda 2 foram corrigidos. Os outros pedem varredura própria, com nota
   datada em cada. Os mais visíveis: `app/actions/daemon_actions.py:545`
   (`format_game_broken_result`, o toast do botão da aba Sistema) e o docstring
   de `cli/cmd_steam.py:8-12`. **Grau: MEDIDO** (a contagem por `grep`).
2. **`docs/usage/assets/perfis-jogo-da-steam.png` está órfã** — nenhuma página a
   referencia. É a foto de estado que mostra a caixinha nova.
3. **Três rótulos quebram na janela encolhida** (acima). Nenhum quebra em 1920.
4. **O `README.md` e o `docs/usage/modos.md`** ganharam notas datadas sobre os
   externos "entrarem na contagem"; a varredura pode ter deixado irmãos.

---

## O que vem, e por que nesta ordem

A **`MASCARA-01`** virou pré-requisito por decisão dela (resposta 3), e por isso
é a próxima. Mas ela declara `IDENT-01` como *"pré-requisito duro"* — e a
`IDENT-01` **caducou em 06/08**, substituída pela `REGRA-NAO-REGISTRO-01`, que
resolve por regra em vez de registro.

Uma sprint que espera por uma dependência morta não anda. Por isso a onda 3
começa por **reavaliar** as dependências e as seis entregas contra a árvore de
hoje, e só executa o que a reavaliação liberar.

Depois dela, e só depois: `E3` e `E4` da `LUGAR-A-MESA-01`.
