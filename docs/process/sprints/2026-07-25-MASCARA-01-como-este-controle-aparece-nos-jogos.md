# MÁSCARA-01 — "como este controle deve aparecer nos jogos"

- **Status:** ABERTA. **E1 ENTREGUE em 07/08/2026** — mas **não como estava
  escrita**: o *"bump de esquema"* foi medido como destrutivo e substituído por
  arquivo próprio. Ver a nota datada no fim deste arquivo. Da **entrega 3** saiu,
  no mesmo dia, só a **metade segura** — a função pura que compõe o valor a
  partir de uma LISTA de pares, **não ligada**; a condição para ligá-la está na
  última nota datada
- **Prioridade:** **ALTA desde 07/08/2026** — deixou de ser sprint paralela e
  virou **pré-requisito** da `E3`/`E4` da
  [LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md),
  por decisão dela
  ([as doze respostas](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md),
  resposta 3). Prioridade anterior: MÉDIA (dependia de outras três)
- **Aberta em:** 25/07/2026 — desenho proposto pela mantenedora

## De onde veio

Discutindo por que a numeração do jogo não bate com a nossa, a saída óbvia era
dar gamepad virtual a todos os controles — inclusive Nintendo e 8BitDo — para que
o jogo enxergasse só dispositivos nossos, na ordem que montamos.

O problema dessa saída é o **rótulo dos botões**: um Nintendo Pro apresentado como
DualSense faz o jogo pedir `` onde o botão físico diz `X`.

A proposta dela resolve transferindo a escolha para quem sabe:

> *"na interface ao clicarmos no controle — tipo o Switch — ele abre a tela que
> escolhemos como ele deve aparecer na tela"*

Em vez de o projeto decidir por todos, **cada controle tem a sua máscara, e o
preço é dito na hora da escolha.**

## Por que isto é o que resolve a numeração

Não porque passemos a controlar a ordem — **não controlamos, e isso foi
verificado**. Não existe variável de ambiente nem canal que informe número de
jogador a um jogo, e o critério que os jogos usam nunca foi medido neste projeto
*(as afirmações existentes sobre "ordem de enumeração" são inferência, não
experimento)*.

O que controlamos é o **conjunto**. Se todo dispositivo que o jogo enxerga é um
gamepad virtual nosso, qualquer critério que ele use opera sobre uma lista que
**nós montamos** — e o número que ele atribuir volta pelo caminho de repasse,
fechando o laço.

A única alavanca real que existe hoje é **negativa**: tirar dispositivo de cena.
Esta sprint a usa deliberadamente.

## A tela

```
Como este controle deve aparecer nos jogos?

  ( ) Como ele mesmo — Nintendo Pro
      Os botões batem com o que está escrito neles.
      Este controle é numerado pelo jogo, fora da sua ordem.

  ( ) Como DualSense
      Entra na sua ordem de jogador. Gatilhos, luz e vibração funcionam.
      O jogo vai pedir  onde o seu botão diz X.
      Enquanto a ponte de movimento não existir, perde o giroscópio.

  ( ) Como Xbox 360
      Máxima compatibilidade. Sem gatilhos adaptativos.
```

**Cada opção diz o que custa.** É o que falta na interface hoje, e é metade do
valor desta sprint.

## Onde a máscara mora — a decisão, com o argumento

A máscara é propriedade do **aparelho**, não da configuração do jogo.

*"Este Nintendo Pro se apresenta como DualSense"* é uma verdade sobre o controle e
sobre os rótulos impressos nele. Não muda porque a janela em foco mudou.

E há uma razão dura, além da conceitual: **trocar a máscara derruba e recria o
gamepad virtual.** Se ela morasse na configuração por perfil, cada troca
automática de perfil — cada alt-tab — faria o controle sumir e voltar no meio da
partida. Isso é pior que o defeito que a sprint conserta.

Portanto: registro de identidade, no mesmo arquivo que já guarda a ordem de
preferência, com versão de esquema nova. A configuração por perfil pode, no
máximo, ter uma recusa explícita.

## O que hoje impede

Três coisas, todas encontradas no código:

1. **Os externos não têm gamepad virtual.** Existe comentário dizendo que ganham
   — é letra morta: o conjunto de candidatos vem de uma descoberta fechada em
   fabricante e produto da Sony. Nenhum externo chega a ser promovido.
2. **Os externos não são escondidos do jogo.** As variáveis que escondem os
   físicos carregam **um** par fabricante/produto, cravado. Nintendo e 8BitDo
   nunca entram.
3. **A identidade de externo não é endereço.** Ela é um caminho de dispositivo, e
   **todo** o direcionamento por endereço curto-circuita nesse formato — em
   quatro lugares distintos. Sem identidade estável, o controle mascarado não tem
   alvo.

## Entregas

1. **Máscara por aparelho** no registro de identidade, com bump de esquema.
2. **Descoberta por-jogador que aceite externos** — quando, e só quando, a
   máscara pedir. A descoberta atual continua existindo para o caminho DualSense.

   > **NOTA DATADA — 07/08/2026: esta entrega, COMO ESTÁ ESCRITA, é
   > INCOMPLETA — e saiu daqui.** Ela foi executada como a `E2` da
   > [LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md),
   > que é a versão completa. O que sobra para a MÁSCARA-01 é o **portão**
   > (*"só quando a máscara pedir"*), que é uma camada fina sobre a descoberta,
   > não uma entrega paralela. Ver a nota datada *"a entrega 2 saiu daqui, e por
   > que ela estava incompleta"*, no fim deste arquivo.
3. **As variáveis que escondem os físicos deixam de ser constantes** e passam a
   ser montadas a partir dos controles mascarados.  A lista de variáveis
   permitidas é **espelhada no script de lançamento** — mudar de um lado exige
   mudar do outro, ou o jogo recebe ambiente diferente do que o daemon acha que
   mandou.
4. **A tela**, com o preço em cada opção.
5. **Honestidade na numeração mista.** O controle em "como ele mesmo" sai da
   nossa ordem — o cartão dele **precisa mostrar um travessão**, não um número
   que mentiria. É a mesma regra que o projeto já aplica noutro lugar: nulo
   honesto vale mais que número errado.
6. **Ponte de movimento para externo mascarado.** Hoje o espelho de giroscópio
   exige um caminho de hidraw que não existe para externos, **por decisão**. Sem
   esta entrega, "Como DualSense" num Pro custa o giroscópio — e a tela tem de
   dizer isso enquanto for verdade.

## Dependências

```
JOGO-01  (entregue) ──┐
NUM-01   (entregue) ──┤
IDENT-01 (aberta)   ──┴──> MÁSCARA-01
PLAYER-LED-01 (aberta) ───> (independente, entrega valor sozinha)
```

**IDENT-01 é pré-requisito duro**: sem identidade estável para externo, não há
onde pendurar a máscara nem para onde mandar o repasse.

E enquanto a exceção do Steam Input mantiver gamepad virtual de pé sem
deduplicação, o co-op de quatro continua sendo loteria e **nenhuma numeração se
sustenta** — por isso JOGO-01 vinha primeiro.

## O que foi considerado e recusado

**Adotar a numeração do kernel como nossa.** O contador do kernel reusa o menor
identificador livre e **conta os gamepads virtuais junto com os físicos** — cada
recriação de vpad e cada reconexão por rádio renumeraria a mesa inteira. Seria
trocar a instabilidade que a NUM-01 acabou de curar por outra pior.

**Impor o nosso número ao jogo.** Não existe canal. Verificado.

## Como validar

1. Nintendo Pro em "como ele mesmo" → botões corretos, cartão mostra travessão em
   vez de número.
2. O mesmo Pro em "como DualSense" → entra na ordem, ganha gatilhos e luz, e a
   tela avisou sobre os rótulos antes.
3. Quatro controles mascarados → o jogo vê **quatro** dispositivos, todos nossos.
4. Alt-tab não derruba nenhum vpad *(a máscara não mora no perfil)*.
5. Trocar a máscara com jogo aberto → recusa ou avisa, mas não deixa a pessoa sem
   controle no meio da partida.

---

## NOTA DATADA — 07/08/2026: a E1 saiu, e o "bump de esquema" caducou

**Decisão medida não se apaga.** O texto da `E1` acima continua onde estava —
*"Máscara por aparelho no registro de identidade, com bump de esquema"* —, e a
seção *"Onde a máscara mora"* continua inteira, porque o argumento dela (a
máscara é do APARELHO, e trocá-la derruba o vpad) **não caducou**: é o que a
entrega obedece. O que caducou é **onde** a máscara ia morar.

### O que foi entregue

`daemon/subsystems/external_mask.py` — módulo irmão de `external_identity.py`,
com `ExternalMaskRegistry`: identidade de aparelho → máscara, em **arquivo
próprio** (`controller_masks.json` em `config_dir()`), com **versão própria**.
Chaveado pela identidade que `identity_for_entry` já carimba, que é a MESMA com
que o daemon numera o externo. Sem bump, sem migração, sem renumerar ninguém.

Testes em `tests/unit/test_external_mask.py` — função pura sobre arquivo
forjado, na bancada de `test_external_identity.py` (faixa `aa:bb:cc:*`). Nenhum
aparelho, nenhum GTK, nenhum Xvfb.

**Isto é só o REGISTRO.** Não adota externo, não cria gamepad virtual, não
esconde ninguém do jogo, não desenha tela. As `E2`, `E3`, `E4`, `E5` e `E6`
seguem abertas, e a `E3` da LUGAR-À-MESA-01 (a adoção) continua atrás desta.

### Por que o bump de esquema foi recusado — GRAU: MEDIDO

Quatro fatos na árvore, os quatro já medidos um a um pela
[REGRA-NAO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md),
seção *"O que muda no arquivo"*:

1. **`identity.load` descarta a fila INTEIRA** quando a versão do arquivo
   difere (`identity.py:858`). Um bump renumeraria a mesa dela — trocaria o
   defeito dos rótulos de botão por outro que a `NUM-01` acabou de curar;
2. **`identity._save_locked` só aproveita as entradas do outro lado quando a
   versão bate** (`identity.py:940-950`). O primeiro save do lado DualSense
   depois de um bump — que acontece a cada conexão de DualSense — **apagaria a
   fila dos externos**;
3. **`payload: dict[str, Any] = {}` é montado do zero** (`identity.py:951`):
   chave nova de topo escrita pelo lado externo morre no primeiro save do outro;
4. **`merged_order_payload` devolve exatamente `{addr, kind, rank}`**
   (`identity.py:316`) e **`order_entries` descarta `kind` desconhecido**
   (`identity.py:279`): campo novo POR ENTRADA morre nos DOIS escritores.

O quarto fato sozinho já impede pendurar a máscara numa entrada da fila; os dois
primeiros tornam o bump ativamente destrutivo.

**E a lição do fato 3 foi aplicada contra nós mesmos:** o save do arquivo novo é
read-modify-write e **preserva o que não entende** (chave de topo e campo por
entrada de uma versão futura). Arquivo cuja versão não é a nossa não é lido
**nem sobrescrito** — recusar a gravar é mais barato que destruir a escolha de
alguém.

### O que torna isto executável em 07/08 e não em 25/07

O item 3 de *"O que hoje impede"* dizia que a identidade de externo *"não é
endereço"*. **Isso caducou:** a chave estável existe hoje —
`identity_for_entry` (`external_identity.py:348-362`) é fonte ÚNICA, é
persistível quando é MAC de hardware (`_canonical`, `:415-431`), e MAC de
hardware **nunca é podado** (D2/R-15, `_prune_volatile_locked`, `:550`). O que
continua valendo do item 3 é o direcionamento por endereço nos outros quatro
lugares — território da `E2`/`E3`.

### Os dois limites, declarados — GRAU: MEDIDO

1. **Identidade sintética, `dev:` ou `path:` é volátil.** Máscara pendurada ali
   vale **só na sessão** e não vai ao disco: persistir seria gravar a escolha
   numa chave que dois aparelhos diferentes podem dividir (CLONE-01);
2. **Máscara é por ROSTO, não por grupo.** A `REGRA-NAO-REGISTRO-01` compartilha
   **rank**, nunca identidade — a máscara pendurada num rosto do 8BitDo **não
   vale no outro**. É o mesmo limite que aquela sprint já declara para
   `Profile.controllers`, e a extensão (o lookup consultar os outros rostos do
   grupo) está deliberadamente fora deste desenho.

### O que NÃO mudou, e é de propósito

`CONTROLLERS_SCHEMA_VERSION` continua **3**. `order_entries`,
`merged_order_payload`, o portão de versão do `load` e o `payload = {}` do
`identity.py` **não foram tocados** — nenhuma linha. É isso que garante que a
fila dela sobrevive a esta entrega.

---

## NOTA DATADA — 07/08/2026: a entrega 2 saiu daqui, e por que ela estava incompleta

**GRAU: MEDIDO no código.** A entrega 2 desta sprint e a `E2` da
[LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)
são **a mesma coisa** — e a `E2` é a versão correta. Ela foi executada em
07/08/2026; a nota com o `caminho:linha`, o custo e as mordidas mora **lá**.

### O item BLOQUEANTE que esta sprint não nomeava

A entrega 2, como está escrita acima, pede *"descoberta que aceite externos"* e
para por aí. Descobrir não basta: **o controle descoberto seria injogável.**

`EvdevReader._handle_abs` fazia `value & 0xFF` **seis vezes seguidas**, supondo
"DualSense, 0..255". Com o Nintendo Pro (-32767..32767) o **centro** do
analógico vira `0`, que em 0..255 significa **talo à esquerda e para cima**: um
Pro em *"Como DualSense"* andaria sozinho para o canto e não pararia. A `E2`
traz o normalizador por `absinfo` que fecha isso, mais duas coisas que esta
sprint também não pedia:

- **síntese de gatilho digital** — o Pro não publica `ABS_Z`/`ABS_RZ` (o ZL/ZR
  dele é botão), então sem síntese o gatilho fica **0 para sempre**;
- **reencontro por identidade** — `_locate` só procurava DualSense, e o externo
  nunca voltava de um replug.

**Sem os três, a máscara "Como DualSense" entregaria um controle que a pessoa
não consegue jogar** — e a tela desta sprint teria de dizer isso, junto com o
preço dos rótulos.

### O que fica com a MÁSCARA-01

O portão *"quando, e só quando, a máscara pedir"* — que é uma **camada fina
sobre a descoberta**, não uma entrega paralela: a descoberta já classifica cada
node em `dualsense`/`external` e devolve identidade; o portão só decide quem
recebe tratamento de jogador. Ele **não existe sem a entrega 1** (a máscara por
aparelho), que é onde a pergunta *"esta máscara pediu?"* tem resposta.

**Nada foi apagado:** o texto da entrega 2 fica onde estava, com a marca do que
caducou. Quem for reconstituir a ordem em que as coisas foram sabidas lê os
dois — e o motivo de a MÁSCARA-01 ter virado pré-requisito continua sendo o
dela: *ela recusou o preço de ver botão de PlayStation na tela com o Pro
Controller na mão.*

### O que a saída da entrega 2 NÃO desbloqueia

**A adoção continua vetada.** A `E2` não dá vpad, lugar na partida nem número a
externo nenhum, e o `daemon/subsystems/coop.py` ficou **intocado** — há portão
de texto que reprova se ele passar a enxergar a descoberta unificada. O veto de
19/07 (*"externo não ganha controle virtual"*) foi **adiado com condição**, e a
condição é esta sprint inteira, não a entrega 2 sozinha.

---

## NOTA DATADA — 07/08/2026: a METADE SEGURA da entrega 3, e o que falta para ligá-la

**A entrega 3 continua BLOQUEADA**, e o motivo é o mesmo que a reavaliação de
hoje mediu: *a função pura é escrevível hoje; LIGÁ-LA hoje tira controle do jogo
dela.* O texto da entrega 3 acima **fica onde está**. O que saiu é a metade que
não toca o jogo dela: **as duas variáveis deixaram de carregar um par cravado
dentro da string e passaram a ser COMPOSTAS a partir de uma LISTA de pares —
com a lista de hoje tendo um item só.**

### O que foi entregue

| onde | o que é |
|---|---|
| `daemon/launch_env.py:98` | `PAR_DUALSENSE_FISICO` — o par que estava cravado dentro das duas strings |
| `daemon/launch_env.py:128` | `compor_lista_vidpid(pares, *, maiusculas)` — a função pura |
| `daemon/launch_env.py:213` e `:222` | `valor_ignore_devices` / `valor_disable_hidraw` — a caixa de cada env, com o motivo |
| `daemon/launch_env.py:232` e `:240` | `_IGNORE_VALUE`/`_DISABLE_HIDRAW_VALUE` passam a ser COMPOSTOS, com **um par só** |
| `tests/unit/test_launch_env_lista_vidpid.py` | 13 testes: um par, três pares, zero pares, o formato, a agulha do consumidor, o lixo, e *"a lista não cresceu"* |

**Nada foi ligado.** `compose_env` continua recebendo o par único do DualSense;
nenhum externo, nenhuma máscara e nenhuma mesa alimentam a lista. Há teste que
reprova se o valor emitido ganhar uma vírgula
(`test_compose_env_continua_emitindo_um_par_so`).

### A correção que BARATEOU esta entrega — GRAU: MEDIDO

O aviso da entrega 3 acima (*"a lista de variáveis permitidas é espelhada no
script de lançamento — mudar de um lado exige mudar do outro"*) **não caducou,
mas foi delimitado**: ele vale para **NOME** novo de variável, e aqui não nasce
nenhum.

Lido no `assets/hefesto-launch.sh`:

- `:85-91` — a allowlist do wrapper é um `case "$line" in
  SDL_GAMECONTROLLER_IGNORE_DEVICES=*) ...`, isto é, filtra por **nome**, nunca
  por valor;
- `:309-313` — `while IFS= read -r kv; do set -- "$kv" "$@"` põe cada linha
  **inteira** como **um** argumento do `env(1)`: o valor não sofre word-split.

Logo, compor o VALOR a partir de uma lista exige **zero** mudança no wrapper. O
que continuaria exigindo é uma variável nova.

### O formato, e o grau de cada metade

**`PROTON_DISABLE_HIDRAW` — GRAU: MEDIDO** (07/08/2026, no Proton 10 instalado
na máquina dela). O `is_hidraw_enabled` de
`files/lib/wine/x86_64-windows/winebus.sys` monta a agulha com o molde **wide**
`0x%04X/0x%04X` e procura com **`wcscasestr`** — substring, sem caixa
(`objdump -d --disassemble=is_hidraw_enabled`, mais `strings -el` para os
moldes). Três consequências:

1. o prefixo `0x` e os **quatro dígitos** são obrigatórios — fazem parte da
   agulha, e um token curto (`0x1/0x2`) nunca casa;
2. a **caixa é indiferente**;
3. o **separador é livre** — a vírgula serve.

E o próprio Proton escreve uma lista assim: `proton:1828` (contorno do God of
War Ragnarok no Deck) grava
`0x054C/0x05C4,0x054C/0x09CC,0x054C/0x0BA0,0x054C/0x0CE6,0x054C/0x0DF2`.

**`SDL_GAMECONTROLLER_IGNORE_DEVICES` — GRAU: SUSPEITA COM MECANISMO** (forte;
**nenhum parser do SDL foi executado**). Corroborações: o formato documentado
do hint é lista separada por vírgula de `0xVID/0xPID`; a LaunchOptions **dela**
já foi estendida por vírgula, e o repositório tem regra escrita para não
quebrar isso (`integrations/steam_launch_options.py:147`); e o Proton usa
exatamente esse formato na variável irmã. **Por que parou aqui:** medir o
parser exigiria plantar um joystick falso em `/dev/input` na máquina dela, com
três controles conectados e ela jogando. Recusado.

**A caixa de cada valor não é enfeite — GRAU: MEDIDO.** O IGNORE sai em
minúsculas porque `integrations/steam_launch_options.py:97` compara a
LaunchOptions envenenada contra o token literal
`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6`, byte a byte. Trocar a caixa
faria o `has_poison` deixar de reconhecer o veneno que as versões antigas
persistiram — e veneno com o vpad fora de cena é **zero controles**. Há teste
amarrando as duas pontas.

### A CONDIÇÃO para ligar, escrita — e ela não é hoje

A lista só recebe um **segundo par** quando existir a **`E4` da
[LUGAR-À-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)**:
a **cobertura POR PAR** — *"o par só sai no `IGNORE` se TODO aparelho daquele
par na mesa tiver vpad vivo"*. E a `E4` vem **depois da `E3`** (a adoção dos
externos), que ela **adiou** até a máscara existir.

O que a condição protege, medido naquela sprint: `054c:05c4` é o par do 8BitDo
em modo PS4 **e** o de um DualShock 4 Sony genuíno. Emitir esse par numa mesa
onde o aparelho é um DS4 **sem** vpad some com o controle da pessoa. A mesma
condição está escrita no código, no docstring da função — quem for ligar tropeça
nela antes de conseguir.

### A mordida

A cura foi arrancada **seis** vezes, e as seis reprovaram:

| o que foi arrancado | o que caiu |
|---|---|
| vírgula vira espaço no `join` | 4 testes |
| o prefixo `0x` some do molde | 9 testes |
| o zero à esquerda some (`%x` no lugar de `%04x`) | 9 testes |
| a caixa do IGNORE invertida | 8 testes |
| a faixa de 16 bits deixa de ser conferida | 1 teste |
| o par repetido deixa de ser deduplicado | 1 teste |

### O que esta nota NÃO faz

Não liga a função, não adota externo, não cria vpad para ninguém, não desenha
tela e **não começa a `E3`**. A adoção continua atrás da palavra dela, e o veto
de 19/07 segue valendo enquanto a máscara não estiver inteira.
