# MÁSCARA-POR-JOGADOR-01 — a decisão de 14/08 esbarra na de 10/08

- **Status:** **PARADA, esperando ELA.** Não é falta de plano nem de código: é
  que executar a **D-5** exige reescrever uma decisão dela que está escrita, com
  data, dentro do esquema.
- **Escrito em:** 15/08/2026.
- **Grau:** **MEDIDO no código** (todas as linhas citadas foram abertas e lidas
  nesta data), salvo onde estiver escrito *NÃO MEDIDO*.
- **De onde veio:** uma varredura achou que
  `daemon/subsystems/external_mask.py` era uma cura escrita e nunca ligada —
  *"a casa sabe e o produto não faz"*. É, e o portão da casa já a acusava por
  nome. Mas a razão que o portão dava (*"o desenho da tela é decisão dela e está
  pendente"*) **caducou em 14/08**, e a razão de verdade é outra.

---

## O resumo, em cinco linhas

1. `ExternalMaskRegistry` está inteiro, testado e **desligado** — zero
   chamadores em `src/`.
2. **Ela já decidiu o que ele deve fazer**: a **D-5** de 14/08 diz *máscara do
   **jogador**, com a do jogo como padrão herdado*.
3. Só que a máscara por jogador **contradiz** a decisão dela de **10/08**, que
   está escrita em `profiles/schema.py`:637.
4. A própria D-5 previu isso e mandou **parar e devolver a ela** em vez de
   contornar.
5. É o que este documento faz. **A pergunta está na seção 4.**

---

## 1. O que existe hoje, e o que não existe

**O que existe** — `daemon/subsystems/external_mask.py`, entregue como a `E1` da
[MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) em
07/08/2026 (commit `7ffd205`). São 509 linhas que guardam, validam e
**persistem** a máscara por identidade de aparelho, em arquivo próprio
(`controller_masks.json` em `config_dir()`), com versão própria, save
read-modify-write que preserva o que não entende, e um normalizador **estrito**
que devolve `None` em vez de cair em `"xbox"` — a cicatriz da
`ESCOLHA-DELA-VENCE-01`.

**O que não existe** — chamador. As duas únicas ocorrências de `external_mask`
fora do próprio módulo, em toda a `src/`, são **comentários**
(`integrations/uinput_gamepad.py`:146 e `daemon/ipc_handlers.py`:4162-4163).

### A armadilha que vai pegar a próxima pessoa

> **`ExternalMaskRegistry` NÃO é um subsystem, e não é caso de
> `SUBSYSTEM_REGISTRY`.**

Quem chegar por uma varredura de importadores vai ver a classe morando em
`daemon/subsystems/` e concluir que basta acrescentá-la à lista. Dois fatos
medidos dizem que não:

- a classe **não implementa o protocolo** de `subsystems/base.py` — não tem
  `name`, não tem `start`, não tem `stop`. Ela é um **registro de disco**, e
  mora ali por vizinhança;
- mesmo que tivesse, **não adiantaria**: o docstring de
  `daemon/subsystems/__init__.py`:13 avisa, desde a `BT-MIC-REGISTRY-01`, que a
  lista é **declarativa** e *"não é iterada por ninguém em produção"*. Quem sobe
  subsystem é o `Daemon.run()`, uma chamada por vez. Foi exatamente assim que o
  `BtMicSubsystem` nasceu órfão.

Isto agora está escrito também na entrada do portão, para não custar a tarde de
ninguém.

---

## 2. A contradição, com as duas frases dela lado a lado

**10/08/2026** — `profiles/schema.py`:637, na lista *"fora porque NÃO TÊM
RESPOSTA HONESTA por unidade"* de `ControllerOverrides`:

> `mode` e a máscara do gamepad são da **SESSÃO**, não da peça (decisão dela,
> 10/08/2026): duas unidades pedindo modos diferentes no mesmo perfil não têm
> resposta.

**14/08/2026** — a **D-5** de
[`DECISOES-DE-PO`](../2026-08-14-DECISOES-DE-PO-as-onze-respostas-da-mesa-cheia.md):

> A máscara do gamepad é **do jogador**, com a máscara do jogo como padrão
> herdado — override **por unidade**, o mesmo desenho que o
> `ControllerOverrides` já usa para leds/triggers/rumble/speaker.

As duas são dela e as duas estão certas no que cada uma resolvia. **O documento
de 14/08 já viu o choque e escreveu o que fazer:**

> **NOTA:** a metade da D-5 que é *máscara* e a D-6 que é *modo* estão na mesma
> frase daquele esquema. (…) Se ao executar a D-5 ficar claro que separar as
> duas exige reescrever aquela decisão dela, **a D-5 para e volta para ela** —
> não se contorna decisão escrita.

**Ficou claro. Por isso este documento existe.**

---

## 3. A medição que torna a pergunta respondível

A justificativa de 10/08 é *"duas unidades pedindo X diferentes não têm
resposta"*. Ela foi escrita para `mode` **e** para a máscara, na mesma frase.
Medido hoje, ela é **verdadeira para o `mode` e falsa para a máscara** — e é
isso que faz a pergunta valer a pena:

| | `mode` (modo nativo) | máscara (*flavor*) |
|---|---|---|
| Quantos existem no daemon | **um só** — é estado do processo inteiro | **um por jogador** — cada um tem o seu gamepad virtual |
| Duas unidades pedindo coisas diferentes | **não tem resposta** — o daemon não pode estar em dois modos | **tem resposta** — cada vpad nasce com o `flavor=` dele |

**O que sustenta a coluna da direita:** o co-op **já cria um vpad por jogador**,
um por MAC (`daemon/subsystems/coop.py`), e cada vpad **já carrega o próprio
atributo `flavor`**.

**E aqui está o ponto que muda o preço da pergunta:** a máscara ser da sessão
hoje **não é omissão — é maquinário ativo**. Em `coop.py`:394 o ciclo calcula um
`desired_flavor = self._flavor()`, que lê **um único** `config.gamepad_flavor`
(`:481-485`), e em `:417-424` **derruba e recria** qualquer jogador cujo
`vpad.flavor` divirja dele. O docstring do módulo (`:31`) declara a regra: *"os
secundários seguem a mesma máscara/flavor"*.

Esse laço **é uma cura**, não um descuido — o comentário de `:387-393` diz por
quê:

> a máscara (flavor) do P1 pode ter mudado em runtime (…). O vpad de cada
> secundário nasce com o flavor vigente na criação, mas não se repropaga sozinho
> — sem isto, **P2+ ficam presos no flavor antigo (rumble morto e prompts
> divergentes do P1)**.

**Consequência, e é a que ela precisa saber para decidir:** a máscara por
jogador **não custa escrever um mecanismo novo — custa transformar um mecanismo
que hoje força a igualdade num que respeita a diferença.** O `desired_flavor`
deixa de ser um valor e passa a ser uma função do MAC. A cura da
`SPRINT-GAME-RUMBLE-01` **tem de sobreviver por unidade**: cada vpad continua
sendo recriado quando **a máscara DELE** mudar. Se isso for feito errado, o
sintoma que volta é o que aquela sprint consertou — rumble morto no P2+.

---

## 4. A PERGUNTA — é esta, e só esta

> **Em 10/08 você escreveu que a máscara do gamepad é da SESSÃO, não da peça,
> pelo mesmo motivo do `mode`. Em 14/08 você escolheu a máscara POR JOGADOR.**
>
> **Medindo, os dois casos se separaram: o `mode` é mesmo um só no daemon, mas a
> máscara já tem um lugar por jogador — cada controle tem o gamepad virtual
> dele. A frase de 10/08 continua certa para o `mode` e ficou larga demais para
> a máscara.**
>
> **Você reescreve a frase de 10/08 para valer só para o `mode`, e a máscara
> passa a ser por jogador? Ou a frase fica como está, e a D-5 cai?**

### O que cada resposta custa

| | **A — a frase fica** (máscara é da sessão) | **B — a frase é reescrita** (máscara por jogador) |
|---|---|---|
| **Custa** | uma frase na tela declarando o escopo — o mesmo desfecho da **D-6** | ≈ **480 min** (estimativa da D-5) |
| **O que muda no código** | nada | campo novo em `ControllerOverrides`; `desired_flavor` do co-op vira função do MAC; a rota de emulação aceita alvo; e **aí sim** o `ExternalMaskRegistry` ganha o chamador que nunca teve |
| **Risco** | nenhum novo | **NÃO MEDIDO:** um jogo pode não aceitar controles heterogêneos na mesma sessão — a D-5 já declarava isso |
| **O que acontece com as 509 linhas** | ficam sem futuro — a **poda é decisão dela**, símbolo público não se apaga por conta própria | ficam ligadas |

---

## 5. O que muda NA TELA — ela decide vendo, não lendo

**Hoje:** a escolha *"como este controle aparece nos jogos"* vive nas abas
**Início / Emulação** e vale **para todo mundo ao mesmo tempo**. Trocar para
*Xbox* troca os quatro.

**Com a resposta B:** aquele mesmo quadro ganha **as quatro marcas da D-3**, e
clicar numa marca troca **de quem** é a máscara que está sendo editada — igual
ao que a D-3 já decidiu para o resto da janela. Um controle sem opinião mostra
**"herdado"** e segue a máscara do jogo, que é o valor de hoje. Ninguém precisa
escolher por jogador para o produto funcionar; quem escolher, assume.

**Com a resposta A:** o quadro ganha **uma frase** dizendo que aquela escolha
vale para a sessão inteira — e a pergunta *"por que aqui não tem as quatro
marcas?"* deixa de existir.

> **A foto tem de vir antes** ([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)):
> nenhuma das duas se desenha sem ela ver o antes e o depois.

---

## 6. O ensaio que a mesa de hoje pode resolver de graça

A D-5 declarou um **risco não medido** e disse que ele *"tem de ser medido com a
mesa cheia"* **antes** de virar código. A mesa de quatro controles está montada
para outro ensaio — este cabe no mesmo dia, e **não depende de nenhuma linha
deste plano**:

1. abrir um jogo que use *Steam Input*, com os quatro conectados;
2. hoje os quatro vpads têm a **mesma** máscara. Trocar a máscara global de
   `dualsense` para `xbox` e confirmar que os quatro trocam juntos — isso mede o
   laço de `coop.py`:417-424 funcionando;
3. o que **não** dá para medir sem a resposta B: um jogo com um vpad `dualsense`
   e outro `xbox` na mesma sessão. **Esse é o risco.** Se ela responder **A**,
   ele nunca precisa ser medido.

---

## 7. O que este documento NÃO faz

- **Não liga nada.** Nenhuma linha de `src/` foi tocada. Ligar aqui é escolher
  comportamento de produto, e a escolha é dela.
- **Não apaga a decisão de 10/08.** Ela é decisão medida, e decisão medida não
  se apaga — ganha nota datada se ela a reescrever.
- **Não reabre a D-6.** O `mode` continua sendo da máquina. A medição da seção 3
  só diz que a máscara e o `mode` são coisas diferentes, e **reforça** a D-6.

---

## Onde isto está registrado fora daqui

- `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py` —
  `_SEM_CAMINHO_HOJE["daemon/subsystems/external_mask.py::ExternalMaskRegistry"]`
  aponta para este documento. A razão antiga (*"o desenho da tela é decisão dela
  e está pendente"*) foi **substituída**, não guardada ao lado: ela mandaria a
  próxima pessoa refazer um painel de decisão que ela já respondeu.
- O dia em que a máscara ganhar chamador, **a entrada do portão é apagada** — e
  quem cobra isso é `test_nenhuma_lapide_sobreviveu_a_propria_cura`, não a
  memória de ninguém.
