# MÁSCARA-POR-JOGADOR-01 — a decisão de 14/08 esbarra na de 10/08

- **Status:** **RESPONDIDA E LIGADA ATÉ O PENÚLTIMO DEGRAU** (15/08/2026). A
  pergunta da seção 4 nasceu *"parada, esperando ELA"* — e **ela respondeu no
  mesmo dia**: *"máscara do gamepad: **por jogador.** A frase de 10/08 passa a
  valer só para o `mode`"*
  ([AS-DECISOES-RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md), linha
  23). É a **resposta B** da tabela da seção 4. O código foi escrito e commitado
  (`95fffdd`); o que falta é o **último degrau**, e ele está na seção 7.
- **Escrito em:** 15/08/2026. **Atualizado em 15/08/2026** com a resposta dela,
  com o que virou código, e com o veredito do ensaio de mordida (seção 8).
- **Grau:** **MEDIDO no código** (todas as linhas citadas foram abertas e lidas
  nesta data), salvo onde estiver escrito *NÃO MEDIDO*.
- **De onde veio:** uma varredura achou que
  `daemon/subsystems/external_mask.py` era uma cura escrita e nunca ligada —
  *"a casa sabe e o produto não faz"*. É, e o portão da casa já a acusava por
  nome. Mas a razão que o portão dava (*"o desenho da tela é decisão dela e está
  pendente"*) **caducou em 14/08**, e a razão de verdade é outra.

---

## O resumo, em cinco linhas

1. `ExternalMaskRegistry` estava inteiro, testado e **desligado** — zero
   chamadores em `src/`. **Deixou de estar** em 15/08/2026: ele é consultado na
   criação de **todo** gamepad virtual.
2. **Ela já tinha decidido o que ele deve fazer**: a **D-5** de 14/08 diz
   *máscara do **jogador**, com a do jogo como padrão herdado*.
3. Só que a máscara por jogador **contradizia** a decisão dela de **10/08**, que
   estava escrita em `profiles/schema.py`:637.
4. A própria D-5 previu isso e mandou **parar e devolver a ela** em vez de
   contornar. Foi o que este documento fez — a pergunta está na seção 4.
5. **Ela respondeu B**: a frase de 10/08 foi reescrita para valer só para o
   `mode`, e a máscara passou a ser do jogador. **O que ainda não chegou é o
   último degrau — a identidade do jogador — e ele está na seção 7.**

---

## 1. O que existe hoje, e o que não existe

**O que existe** — `daemon/subsystems/external_mask.py`, entregue como a `E1` da
[MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) em
07/08/2026 (commit `7ffd205`). Nasceu com 509 linhas — hoje tem **685**, depois
do `95fffdd` — que guardam, validam e
**persistem** a máscara por identidade de aparelho, em arquivo próprio
(`controller_masks.json` em `config_dir()`), com versão própria, save
read-modify-write que preserva o que não entende, e um normalizador **estrito**
que devolve `None` em vez de cair em `"xbox"` — a cicatriz da
`ESCOLHA-DELA-VENCE-01`.

**O que não existia** — chamador. Quando este documento foi aberto, as duas
únicas ocorrências de `external_mask` fora do próprio módulo, em toda a `src/`,
eram **comentários** (`integrations/uinput_gamepad.py`:146 e
`daemon/ipc_handlers.py`:4162-4163).

> **CADUCOU no mesmo dia, 15/08/2026** — depois da resposta dela (seção 4), o
> commit `95fffdd` deu ao registro os chamadores que ele nunca teve. O
> levantamento acima fica porque é o **diagnóstico** que abriu a frente, não
> porque descreve o código de hoje; o estado de hoje está na **seção 7**.

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
RESPOSTA HONESTA por unidade"* de `ControllerOverrides`. **Esta frase não existe
mais no arquivo**: ela a reescreveu em 15/08 e o commit `95fffdd` trocou o texto
por uma **nota datada** no mesmo lugar. Quem procurar por ela no código de hoje
não a acha — a versão original é esta:

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

## 4. A PERGUNTA — e a resposta dela

> **RESPONDIDA EM 15/08/2026 — a resposta é a B.** Ela escolheu **máscara por
> jogador**, e a frase de 10/08 *"passa a valer só para o `mode`"*
> ([AS-DECISOES-RESPONDIDAS](../2026-08-15-AS-DECISOES-RESPONDIDAS.md), linha
> 23). A pergunta fica escrita abaixo porque é o que ela leu para decidir — e
> porque a tabela de custos é o preço que ela aceitou pagar, não uma estimativa
> a refazer.

### A pergunta, como foi feita

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

**Ela escolheu a B.** O que a coluna B prometia, conferido contra o código de
hoje: a frase de 10/08 **foi** reescrita (nota datada em `profiles/schema.py`);
o `ExternalMaskRegistry` **ganhou** o chamador que nunca teve; o
`desired_flavor` do co-op **ainda não** virou função do MAC e a rota IPC **ainda
não** aceita alvo. O risco *NÃO MEDIDO* da linha de cima **continua não medido**
— a seção 6 diz como medi-lo, e agora ele importa.

**Uma linha da coluna B não se cumpriu, e de propósito: o "campo novo em
`ControllerOverrides`" NÃO foi escrito.** A execução mediu uma segunda razão,
diferente da de 10/08, para a máscara ficar fora do perfil: trocar a máscara
**derruba e recria o gamepad virtual**, então num campo de perfil cada troca
automática de perfil — cada alt-tab — faria o controle sumir e voltar no meio da
partida. A escolha por unidade mora no `external_mask`, chaveada pelo aparelho,
**com a mesma semântica de herança** que o `ControllerOverrides` teria dado. A
decisão dela é cumprida; o lugar de guardá-la é que é outro.

---

## 5. O que muda NA TELA — ela decide vendo, não lendo

> **O caminho é o da resposta B.** A tela **ainda não mudou** — nenhuma linha de
> GUI foi tocada em 15/08, e nem podia ser: a foto vem antes. O parágrafo da
> resposta A fica só como o desenho que não foi escolhido.

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
   e outro `xbox` na mesma sessão. **Esse é o risco.**

> **Ela respondeu B, então o item 3 deixou de ser hipotético — e ele ainda não
> foi medido** (15/08/2026). Enquanto o último degrau da seção 7 não chegar, a
> mesa não consegue produzir duas máscaras diferentes ao mesmo tempo, então o
> ensaio **não é bloqueante para escrever o degrau** — é bloqueante para
> *prometer* que máscaras heterogêneas funcionam. O roteiro exato está no
> cabeçalho de `daemon/subsystems/external_mask.py`, na seção *"RISCO NÃO
> MEDIDO"*: P1 em `dualsense`, P2 em `xbox`, e então olhar, nesta ordem, se os
> quatro jogadores continuam existindo, se os prompts de cada um saem na máscara
> dele, e se o rumble chega nos quatro.

---

## 7. O QUE JÁ ESTÁ LIGADO, E O DEGRAU QUE FALTA

> **Esta seção dizia *"não liga nada — nenhuma linha de `src/` foi tocada"*. Era
> verdade quando a pergunta estava aberta e deixou de ser no mesmo dia**: depois
> que ela respondeu, o commit `95fffdd` tocou **quatro arquivos de `src/`**. O
> texto antigo não fica ao lado: ele mandaria a próxima pessoa escrever de novo
> o que já está escrito. Tudo abaixo foi conferido no código vivo, linha a
> linha, em 15/08/2026.

### 7.1 O que JÁ está ligado (commit `95fffdd`)

**`daemon/subsystems/external_mask.py`** — o registro ganhou três símbolos
públicos, e é por eles que a decisão dela entra no produto:

- **`registro_de_mascaras()`** (`:592`) — devolve **sempre o mesmo**
  `ExternalMaskRegistry` do processo, criado na primeira chamada sob
  `_REGISTRO_LOCK` (`:586-589`). Não é preguiça de injeção, é correção:
  `_load_locked` lê o disco **uma vez por instância** e nunca mais, então duas
  instâncias divergem na primeira escrita — a que gravou responde a máscara
  nova, a outra segue respondendo a antiga. E os consumidores são três, em
  threads diferentes (criação do vpad no poll loop, comparação do tick do co-op,
  rota IPC que grava o gesto dela). O sintoma da divergência seria o pior
  possível: **vpad recriado em laço eterno** porque quem cria e quem compara
  discordam.
- **`mascara_efetiva(identity, flavor_do_jogo)`** (`:617`) — **é a regra de
  herança da D-5**: a máscara que este aparelho escolheu; sem escolha, a do
  jogo. Não existe "sem máscara" — existe **a máscara do jogo**, que é o valor
  que o produto sempre teve, e é isso que torna o recurso seguro diante do risco
  não medido. O `flavor_do_jogo` passa pelo `normalize_flavor`, que é
  **tolerante**, porque este é caminho interno e caminho interno precisa de uma
  máscara sempre; quem valida gesto de gente é o portão do IPC, com o
  `resolver_flavor` estrito.
- **`vpad_ficou_para_tras(flavor_do_vpad, identity, flavor_do_jogo)`** (`:642`)
  — separa a **divergência escolhida** (o jogador pediu outra máscara, o vpad
  dele já está nela, e ele **sobrevive** destoando de todos os outros) do
  **flavor que ficou para trás** (a máscara mudou, o vpad nasceu na anterior, e
  ele é **recriado**). É a peça que faz a cura da `SPRINT-GAME-RUMBLE-01`
  sobreviver por unidade em vez de forçar a igualdade. **É a única das três que
  ainda não tem chamador** — ver 7.2.

O cabeçalho do módulo também mudou: ganhou a nota datada de 15/08, a lista do
que ainda não chega até ele, a armadilha do primeiro degrau (abaixo) e o
**risco não medido** dos controles heterogêneos, escrito no código e não só aqui.

**`profiles/schema.py`** (`:639-663`) — a frase de 10/08 foi **reescrita**, não
duplicada: o item da lista agora diz só *"``mode`` é da SESSÃO"*, e logo abaixo
vem a **NOTA DATADA — 15/08/2026** (`:644`) contando que a frase original dizia
*"`mode` **e a máscara do gamepad**"*, que ficou larga demais, e que ela a
reescreveu. A nota fecha com uma segunda razão, **medida e diferente da de
10/08**, para a máscara continuar **fora** do `ControllerOverrides`: trocar a
máscara **derruba e recria o gamepad virtual** — num campo de perfil, cada troca
automática de perfil (cada alt-tab) faria o controle sumir e voltar no meio da
partida. Por isso a escolha por unidade mora no `external_mask`, chaveada pela
identidade do aparelho.

**`integrations/uinput_gamepad.py`** (`for_flavor`, `:357-385`) — o método ganhou
o parâmetro `identity: str | None = None`, e a linha que decidia a máscara deixou
de ser `key = normalize_flavor(flavor)` e passou a ser
**`key = mascara_efetiva(identity, flavor)`** (`:381`). O `flavor` deixa de ser a
resposta e vira o **padrão herdado**. Com `identity=None`, nada muda.

**`integrations/uhid_gamepad.py`** (`for_flavor`, `:976-1030`) — mesmo parâmetro,
e o gate *"não é dualsense, logo não é meu"* passou a **perguntar ao registro
primeiro** (`:1019`): um aparelho marcado como `xbox` devolve `None` aqui e segue
para o `UinputGamepad` **mesmo que a máscara do jogo seja dualsense** — a escolha
do jogador serve inclusive para dizer *não*. Sem escolha registrada, a regra
antiga do `flavor` vale intacta.

### 7.2 O que FALTA — o último degrau, que é a IDENTIDADE

As duas fábricas de vpad já sabem perguntar *"de quem é este gamepad virtual?"*.
**Ninguém responde.** Faltam três chamadas e uma comparação:

| onde | o que está lá hoje | o que falta |
|---|---|---|
| `integrations/virtual_pad.py`:150 | `make_virtual_pad(flavor, *, …)` — **não aceita `identity`** | aceitar o parâmetro e repassá-lo aos dois backends |
| `integrations/virtual_pad.py`:192 | `key = normalize_flavor(flavor)`, e é esse `key` que vai ao `_try_uhid` (`:221`) | resolver com `mascara_efetiva` **ANTES** de escolher o backend |
| `daemon/subsystems/coop.py`:394 | `desired_flavor = self._flavor()` — um valor **GLOBAL**, de um único `config.gamepad_flavor` (`_flavor()`:481-485) | o alvo deixa de ser um valor e vira função do MAC |
| `daemon/subsystems/coop.py`:417-419 | `getattr(player.vpad, "flavor", None) != desired_flavor` | `vpad_ficou_para_tras(getattr(p.vpad, "flavor", None), mac, self._flavor())` |
| `daemon/subsystems/coop.py`:679 | `make_virtual_pad(self._flavor(), …)` em `_promote_player` | `identity=player.identity` |
| `daemon/subsystems/gamepad.py`:1892 | `make_virtual_pad(key, …)` para o P1 | `identity=` o MAC do primário |
| `daemon/ipc_handlers.py` | só conhece a máscara da **sessão** | o lado da **escrita**: gravar a escolha dela por aparelho |

> **A armadilha do primeiro degrau, e ela tem sintoma conhecido:**
> `make_virtual_pad` tem de resolver a máscara efetiva **antes** de escolher o
> backend. O gate do `_try_uhid` usa a máscara que **recebe**: se continuar
> recebendo a do JOGO, um jogador que escolheu `dualsense` numa sessão `xbox`
> tem o uhid vetado e cai no `uinput` **com máscara DualSense** — que é
> exatamente o par degradado onde a vibração do jogo morre
> (VPAD-05/`SPRINT-GAME-RUMBLE-01`). Resolver na factory é seguro porque
> `mascara_efetiva` é **idempotente**: a máscara efetiva de uma máscara já
> efetiva é ela mesma.

**Enquanto esse degrau não chega, o produto se comporta EXATAMENTE como antes** —
uma máscara só, a do jogo, para os quatro. Isso é de propósito: meia cura que
muda comportamento é pior que nenhuma, e `coop.py` estava sob edição de outra
frente no mesmo dia — derrubar a cura da `SPRINT-GAME-RUMBLE-01` por descuido
reintroduz um defeito **medido**.

### 7.3 Quem vigia o degrau que falta

Não é a memória de ninguém — é um teste que **falha de propósito hoje** e
**reprova no dia em que curar**:

- **`tests/unit/test_mascara_por_jogador_01.py`:332** —
  `@pytest.mark.xfail(strict=True)` sobre
  `test_o_ultimo_degrau_da_mascara_por_jogador_chegou` (`:344-351`). O teste
  afirma que `coop.py` **e** `gamepad.py` passam `identity=` ao
  `make_virtual_pad`. Hoje é falso, o `xfail` o absorve, e a suíte fica verde. No
  dia em que alguém escrever o degrau, o teste **passa** — e o `strict=True`
  transforma o `XPASS` em **reprovação**, obrigando quem curou a apagar o
  marcador e a lápide junto. É a lápide viva.
- **A régua é AST, não `grep`** — `_chama_make_virtual_pad_com_identidade`
  (`:311-329`) percorre a árvore e só aceita `identity=` que seja **keyword de
  uma chamada a `make_virtual_pad`**. Um `grep` de texto daria o degrau por
  pronto: `coop.py` tem dezenas de `identity=` em chamadas de log.

### 7.4 O que este documento continua NÃO fazendo

- **Não apaga a decisão de 10/08.** Ela é decisão medida: foi **reescrita por
  ela** e ganhou nota datada no lugar onde morava, com o texto original citado
  na seção 2 deste documento.
- **Não reabre a D-6.** O `mode` continua sendo da máquina. A medição da seção 3
  só diz que a máscara e o `mode` são coisas diferentes, e **reforça** a D-6.
- **Não desenha tela nenhuma.** A seção 5 continua valendo: a foto vem antes.
- **Não promete máscaras heterogêneas.** O risco da seção 6 segue **não
  medido**.

---

## 8. O VEREDITO DA MORDIDA — sete curas arrancadas, sete reprovações

*"Teste tem de MORDER. Um teste que passa com a cura arrancada não testa nada.
Arranque, veja reprovar, devolva."* Este é o registro do ensaio que cumpre a
regra — ele foi feito em 15/08/2026 e **não estava escrito em documento nenhum**
até agora.

**O instrumento.** Um script que, para cada mutação: guarda o texto original do
arquivo, **arranca uma cura só** por substituição de trecho literal, roda
`pytest tests/unit/test_mascara_por_jogador_01.py -q --no-header -p no:randomly`,
e **devolve o arquivo num `finally`** — a árvore volta ao lugar mesmo se o pytest
explodir. Ele imprime a linha de resumo antes de tudo, depois de cada mutação e
ao final, para que a **devolução** seja auditável junto com a mordida. O
`-p no:randomly` está ali de propósito: ordem aleatória de teste tornaria a
contagem de falhas incomparável entre mutações.

**A linha de base:** `14 passed, 1 xfailed` em ~0,25 s — o `xfailed` é a lápide
viva da seção 7.3, que **tem** de continuar amarela.

### As sete mutações, uma a uma

| id | arquivo | o que foi ARRANCADO | o que reprovou |
|---|---|---|---|
| **M1** | `external_mask.py` | as três linhas de `mascara_efetiva` que consultam o registro (`escolhida = registro_de_mascaras().mask_for(identity)` e o `return` dela) — sobra só o `normalize_flavor`. **A escolha dela vira enfeite** | **6 failed**, 8 passed |
| **M2** | `external_mask.py` | o corpo inteiro de `vpad_ficou_para_tras`, trocado por `return False` — **nenhum vpad é derrubado nunca**: é a cura da `SPRINT-GAME-RUMBLE-01` arrancada pela raiz | **2 failed**, 12 passed |
| **M3** | `external_mask.py` | a mesma linha, trocada pela comparação contra a máscara **GLOBAL** (`normalize_flavor(flavor_do_jogo)`) — **é literalmente o código que o `coop.py` roda hoje** | **2 failed**, 12 passed |
| **M4** | `external_mask.py` | o corpo do singleton de `registro_de_mascaras()`, trocado por `return ExternalMaskRegistry()` — **uma instância nova a cada chamada**, o defeito de disco divergente descrito em 7.1 | **3 failed**, 11 passed |
| **M5** | `uinput_gamepad.py` | `key = mascara_efetiva(identity, flavor)` volta a ser `key = normalize_flavor(flavor)` — **o backend uinput deixa de perguntar de quem é o vpad** | **1 failed**, 13 passed |
| **M6** | `uhid_gamepad.py` | o gate novo de 6 linhas volta ao gate antigo de 2 (`if flavor is not None and normalize_flavor(flavor) != "dualsense": return None`) — **o uhid volta a obedecer só à máscara do jogo** | **2 failed**, 12 passed |
| **M7** | `profiles/schema.py` | a frase reescrita volta a ser larga: `- mode e a máscara do gamepad são da SESSÃO, não da peça` — **a decisão dela de 15/08 desfeita no texto** | **1 failed**, 13 passed |

**Nenhuma mutação passou. Sete arrancadas, sete reprovações — em DUAS rodadas
independentes**, a primeira às 17:32:18 UTC e a segunda às 17:40:39 UTC (depois
do renome do parâmetro `padrao` → `flavor_do_jogo`), com os mesmos sete
vereditos e as mesmas contagens. Nas duas, o **antes** e o **depois** deram
`14 passed, 1 xfailed`: a árvore foi devolvida intacta.

### A mutação que mais importa é a M3

As outras seis provam que a bateria vê a cura sumir. A **M3** prova a coisa mais
difícil: que a bateria mede **a mudança**, e não a si mesma. Ela não arranca a
função — ela recoloca ali **o comportamento de hoje** (comparar o vpad contra a
máscara global) e o teste **reprova**. Sem a M3, uma bateria que só reagisse a
`return False` poderia estar verde por acidente de forma.

### Como repetir

O instrumento nasceu no scratchpad de uma sessão que morreu e sobreviveu na
recuperação, em `_recuperacao-2026-08-15/scratchpad-3706fe35/scratchpad/morder.py` <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore -->
e transcrito na íntegra na §8 do relatório `_recuperacao-2026-08-15/relatorios/interrompido-mascara-por-jogador.md`. <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore -->

**Ele NÃO está nesta árvore, e isso é dívida, não decisão.** Enquanto o
instrumento morar num scratchpad de sessão morta, a mordida só se repete para
quem souber que o scratchpad existe. Guardá-lo num lugar durável é item aberto —
o veredito acima é o que sobra dele se o arquivo sumir, e por isso as sete
mutações estão descritas na tabela por **texto arrancado e texto trocado**, e
não só por nome.

**Conferido hoje, sem mutar a árvore:** os **sete** trechos que as mutações
arrancam **ainda existem, literalmente**, nos quatro arquivos vivos — o ensaio é
reproduzível como está escrito, sem reescrever um caractere. E a bateria segue
em `14 passed, 1 xfailed`.

> **Quando o último degrau da seção 7.2 chegar, o ensaio precisa de duas
> mutações novas** — uma que tire o `identity=` do `coop.py` e outra que
> devolva o `desired_flavor` global ao laço. Sem elas, o degrau novo entra sem
> mordida.

---

## Onde isto está registrado fora daqui

- **`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`:647-656** — a entrada
  `_SEM_CAMINHO_HOJE["daemon/subsystems/external_mask.py::ExternalMaskRegistry"]`
  **foi APAGADA** em 15/08/2026, pelo motivo que ela mesma mandava: **a máscara
  ganhou chamador**. No lugar ficou um comentário dizendo o que aconteceu e para
  onde olhar — não se guarda a entrada velha ao lado da nova, ela mandaria a
  próxima pessoa procurar um chamador que já existe.
- **`…portao_a_casa_sabe_e_o_produto_nao_faz.py`:658-678** — a lápide **nova**,
  `::vpad_ficou_para_tras`, é a do degrau que falta: ela nomeia o chamador único
  (`coop.py`:417-424), o alvo global que precisa cair (`coop.py`:394 →
  `_flavor()`:481-485) e a substituição exata que a fecha. Aponta para este
  documento.
- O dia em que o degrau chegar, **essa entrada também é apagada** — e quem cobra
  isso é `test_nenhuma_lapide_sobreviveu_a_propria_cura`, mais o
  `xfail(strict=True)` da seção 7.3. Não a memória de ninguém.
- **`docs/process/2026-08-15-AS-DECISOES-RESPONDIDAS.md`:23** — a resposta dela,
  na fonte de verdade das decisões do dia. Onde este documento discordar dela, é
  este que está velho.
