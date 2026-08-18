# RESTAURO-SO-COM-SINTOMA-01 — o conserto que ninguém podia chamar

- **Achado em:** 07/08/2026, ao executar a **resposta 16** dela do
  [painel das dezessete](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md)
- **Estado:** **CURA APLICADA** em `scripts/doctor.sh`, com teste que morde em
  `tests/unit/test_restauro_so_com_sintoma_01_o_conserto_que_ninguem_chamava.py`
- **Gravidade:** **MÉDIA** — o sintoma é raro (nó hidraw aberto e órfão), mas
  quando acontece a pessoa não tinha como consertar sem escrever `chmod` à mão
- **Causa-raiz:** **MEDIDA** — o comando não existia em lugar nenhum do código
- **Parentes, e distintas:**
  - [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md)
    — é ela que ensinou o doctor a DETECTAR e a distinguir a causa; esta aqui
    ensina o doctor a CONSERTAR, e usa exatamente aquela distinção como trava;
  - [RECEITA-ERRADA-01](2026-08-06-RECEITA-ERRADA-01-o-doctor-mandava-rodar-o-que-nao-resolvia.md)
    — é dela a regra que manda o check e a cura passarem pelo **mesmo cano**, e
    a que manda **citar** um comando para dizer que ele não serve em vez de
    mandar rodá-lo;
  - [ENTREGA-QUE-NAO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
    — a classe do defeito que este trabalho quase repetiu (ver a correção de
    premissa, logo abaixo).

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## A correção de premissa, primeiro

O trabalho foi encomendado como *"existe um comando `--restaurar-hidraw-uaccess`
que funciona e ninguém chama"*. **Ele não existia.** GRAU: **MEDIDO**, em
07/08/2026:

```
grep -rn "restaurar.hidraw\|restaurar_hidraw" src/ scripts/ assets/ install.sh uninstall.sh tests/
-> 0 ocorrências
```

As quatro ocorrências na árvore inteira eram **prosa**: a
[recomendação de 06/08](../2026-08-06-RECOMENDACAO-A-ELA-a-regra-que-abria-o-teclado.md),
que **desenhou** a opção e explicou por que não a implementava; o
[estudo de 07/08](../estudos/2026-08-07-O-QUE-EXISTE-E-NAO-CHEGA-a-cobertura-do-install.md),
que registra em duas linhas que ela *"não existe (`grep` devolve zero fora da
prosa que a desenha)"*; e a linha 16 da tabela de decisões dela.

Isso muda o que esta sprint é: não é **ligar** um conserto que existia, é
**escrevê-lo** — e o desenho, que era o trabalho difícil, tinha de ser feito
antes de qualquer fio. Registrar isto importa porque a premissa errada tinha uma
saída sedutora: procurar mais um pouco, achar qualquer função vizinha, e ligar
**aquilo**.

## O sintoma, e por que ele é raro e caro ao mesmo tempo

Um nó `/dev/hidraw*` aberto a **outros** entrega os relatórios de entrada crus
do aparelho a qualquer processo local, sem privilégio nenhum. Quando o aparelho
é o receptor do teclado, isso é o que está sendo digitado — foi assim que a
`ACUSA-O-CULPADO-01` encontrou o caso desta casa.

Desde 06/08 o doctor **avisa** e **nomeia o culpado**. O que ele não sabia fazer
é a outra metade: quando **nenhuma** regra explica o nó, não havia conserto
nenhum a oferecer, e a pessoa ficava com um aviso e nenhuma saída.

## A decisão dela, e o motivo dela

> **16** — o `--restaurar-hidraw-uaccess`: **só no `doctor`, quando houver
> sintoma**

E o motivo, na palavra dela: no `install` ele rodaria **sempre**, e reescreveria
permissão que outro programa pôs **de propósito**. O caso concreto desta casa é
o OpenRGB. **Pelo mesmo motivo o restauro também não entra no `--fix`**: o
`--fix` é o laço que roda tudo de uma vez, e roda **antes** dos checks — dali
ele agiria sem sintoma nenhum, que é exatamente o que ela recusou. Há teste que
cobra essa ausência, porque uma linha a mais no `apply_fixes` a desfaz em
silêncio.

---

## O critério de "há sintoma" — a parte difícil

O critério não é "o nó está aberto". É **"o nó está aberto e ninguém
reivindicou isso"**. A diferença entre os dois é a sprint inteira.

Para cada nó aberto a outros, `_hidraw_alvos_do_restauro`
(`scripts/doctor.sh`) devolve uma linha:

| veredito | quando | o que o doctor faz |
|---|---|---|
| `alvo` | nenhuma regra udev explica | **oferece** o conserto |
| `pulo … manta` | uma regra abre TODO hidraw | recusa, e diz onde ela está |
| `pulo … estreita` | uma regra abre **este** aparelho, estreitando por ele | recusa, e diz onde ela está |
| `pulo … incerta` | a regra estreita por chave que a varredura não sabe casar, ou o nó não tem ids legíveis | recusa, e diz que não sabe |

### Por que os três `pulo` são recusa — e as DUAS metades importam

1. **É atropelo.** Quem escreveu a regra escolheu abrir aquilo. Um projeto de
   gamepad reescrevendo permissão de aparelho alheio é invasão de configuração,
   mesmo com a intenção certa.
2. **É inútil.** A regra continua lá. No próximo evento de udev (`add`/`change`)
   ela reabre o nó, e o conserto não dura nem até o replug.

Uma das duas já bastaria para não agir. As duas juntas fazem do `pulo` a única
resposta honesta — e é por isso que o texto na tela diz **as duas**, e não só a
educada.

### O controle positivo que fez este critério existir

**MEDIDO nesta máquina em 07/08/2026**, e é uma regra da distribuição, viva:

```
/usr/lib/udev/rules.d/71-pdp-controllers.rules:8
ACTION!="remove", KERNEL=="hidraw*", ATTRS{idVendor}=="0e6f",
ATTRS{idProduct}=="0185", MODE="0666", TAG+="uaccess"
```

É exatamente a linha que a `ACUSA-O-CULPADO-01` se **recusa a acusar**, por
decisão medida: `MODE="0666"` mirando UM aparelho é decisão de quem escreveu a
regra. Mas a varredura daquela sprint só enumera as regras **manta** — então,
com um controle PDP no cabo, o nó dele apareceria como aberto **e sem regra que
o explique**, porque a regra que o explica é a estreitada, que a varredura
descarta antes de imprimir.

Sem o critério novo, o primeiro conserto oferecido numa máquina com esse
controle seria um atropelo na decisão da distribuição.

### O que mudou na varredura, e o que não mudou

`_udev_hidraw_rw_global` **não mudou de nome, de assinatura nem de saída** — os
testes de 06/08 continuam medindo a mesma coisa. O que aconteceu foi o corpo
virar `_udev_hidraw_scan <manta|estreita>`, com **duas vistas do mesmo `awk`**:

- `manta` — a vista de sempre: `arquivo:linha:conteúdo` das regras que abrem
  todo hidraw. É a **acusação**;
- `estreita` — a vista nova: `arquivo:linha:ids:conteúdo` das regras que abrem
  hidraw **estreitando** por aparelho. Não é acusação: é o **inventário de
  decisões alheias que o restauro tem de respeitar**.

Uma varredura só, porque a lição da `RECEITA-ERRADA-01` é que critério escrito
duas vezes diverge — e o pior lugar para a divergência aparecer é a tela, que é
onde ela vira instrução.

### O casamento é DELIBERADAMENTE frouxo

Um id de 4 hex em comum entre a regra e o nó já basta para o nó ser considerado
explicado. Isso é frouxo de propósito: **todo erro do casamento tem de cair para
o lado de NÃO agir.** Um falso "explicado" custa um conserto que não é
oferecido; um falso "órfão" custa a decisão de outra pessoa, apagada.

Dois exemplos MEDIDOS do que a colheita traz:

- de `KERNELS=="*045e:02ea*"` (regras de distro que embutem `vendor:produto`
  dentro de um curinga) ela tira `045e` e `02ea` — que é o que se quer;
- de `TAG+="uaccess"` ela tira `acce`, porque `a`, `c`, `c` e `e` são dígitos
  hexadecimais válidos. É um identificador fantasma, e ele só pode causar um
  "explicado" a mais. Fica registrado em vez de escondido.

O valor de `MODE=` **sai do texto antes da colheita**, senão `"0666"` viraria um
id fantasma em toda regra estreitada.

---

## O mecanismo do conserto, e por que não é o óbvio

O conserto é **`chmod o=`** nos nós aprovados. Só isso: nenhuma regra udev é
criada, nada é escrito em `/etc`, nenhum acesso é concedido a ninguém.

### Por que não `chmod 0660`

Porque num nó com ACL a classe de **grupo** do `chmod` é a **máscara** — e o
efeito medido de `chmod 0660` não é fechar, é **abrir**. **MEDIDO em bancada,
07/08/2026**, num nó com `user:nobody:rwx` sob `mask::r--`:

```
chmod 0660  ->  mask::rw-   e nobody sai de #effective:r-- para rw-
chmod o=    ->  mask::r--   intacta, nobody continua em r--
```

Ou seja: o `chmod 0660` **concede**, no meio de uma operação chamada restauro,
uma escrita que alguém mascarou de propósito.

### Por que não `setfacl`, apesar do nome da opção

Porque **conceder não é restaurar**. Um `setfacl` nosso num nó alheio daria à
sessão acesso que ela não tinha — e é precisamente o que esta casa recusou por
escrito na
[recomendação de 06/08](../2026-08-06-RECOMENDACAO-A-ELA-a-regra-que-abria-o-teclado.md):
*um projeto de gamepad legislando a política de segurança da máquina inteira*.

Quem **concede** o uaccess aos nós do Hefesto é a regra udev, e quem a reaplica
é o `./install.sh` ou o `scripts/doctor.sh --fix`. **O nome da opção é o dela e
não foi trocado**; a metade "uaccess" do nome descreve o estado a que os nós do
Hefesto voltam, não uma concessão que este comando faça. Isso está dito no
código e na tela — e está listado abaixo como a decisão que é dela para
confirmar ou derrubar.

### Por que não `udevadm trigger`

Seria elegante — reperguntar ao udev em vez de inventar uma política. Foi
recusado porque a afirmação "o `udevadm trigger --action=add` recalcula e
reescreve o modo de um nó já existente" é, aqui, **SEM PROVA**: não foi medida,
e não podia ser medida hoje, com a máquina dela em uso. Mandar rodar o que não
se mediu é a `RECEITA-ERRADA-01` de novo.

---

## O texto diz o que vai acontecer ANTES de acontecer

A cura imprime o plano — os nós, o modo de antes e o de depois, e o que ela
**não** faz — e só então age:

```
       vou tirar o bit de OUTROS destes 1 nó(s), e nada além disso:
         /dev/hidraw0: 666 -> 660   (teclado Receptor de mentira)
       nenhuma regra udev é criada, nada é escrito em /etc, e nenhum acesso é
       concedido a ninguém.
       o que isto NÃO resolve: não IMPEDE o nó de reabrir. Se ele voltar a
       abrir, existe regra que este diagnóstico não lê (ENV{...}, GOTO, ou
       programa fora do udev) — e aí o conserto não dura.
[ OK ] /dev/hidraw0 restaurado (666 -> 660)
```

E quando a resposta é não, ela é **um não com endereço**:

```
       o --restaurar-hidraw-uaccess NÃO resolve este caso, e por isso ele não é
       oferecido aqui:
         /dev/hidraw1: a regra /usr/lib/udev/rules.d/71-pdp-controllers.rules:8
         abre ESTE aparelho, estreitando por ele — a decisão é de quem escreveu
         a regra, e o nó reabriria no próximo evento de udev
       se a permissão desse arquivo estiver errada, o conserto é no arquivo, não
       no nó: edite a regra e rode 'sudo udevadm control --reload-rules'.
```

**O `--quiet` não vale neste modo.** Ele existe para o diagnóstico caber numa
linha de log; aqui ele apagaria justamente o texto que diz o que vai ser feito.
Agir calado é o que não pode acontecer, e há teste que cobra isso.

## Uma frase que estava errada desde 06/08, e a nota datada

Até esta leva, o `check_perms_soft` afirmava:

> `N nó(s) hidraw abertos a qualquer usuário local, e NENHUMA regra udev
> explica — aí sim, ajuste manual é hipótese`

sempre que a varredura de manta voltava vazia. **Isso é falso quando a regra
estreita por aparelho** — o caso do controle PDP acima. A frase **não foi
apagada**: ela continua, palavra por palavra, no ramo em que é verdadeira (há
alvo, ninguém explica), e ganhou uma irmã para o ramo em que não era:

> `… e uma regra udev ESTREITADA por aparelho explica cada um — é decisão de
> quem escreveu a regra, não defeito do Hefesto`

GRAU: **MEDIDO** na leitura (o ramo antigo era alcançável com a regra PDP
presente); **SEM PROVA** de que alguém já tenha lido a frase errada — ela só
aparece com um controle PDP no cabo, e nenhum foi visto nesta bancada.

---

## As mordidas, e a que NÃO mordeu de primeira

`tests/unit/test_restauro_so_com_sintoma_01_o_conserto_que_ninguem_chamava.py`
roda as **funções shell de verdade** contra uma bancada de mentira em
`tmp_path`: nós no lugar de `/dev`, `uevent` no lugar de `/sys`, regras no lugar
de `/etc`. Nenhum nó hidraw real é lido ou escrito, e o `sudo` da bancada é um
dublê que grita se for chamado — o que também prova que a cura **não gasta
elevação** onde não precisa.

**MEDIDO em 07/08/2026:** 27 verdes. Seis arrancadas, uma por cura:

| # | o que foi arrancado | quem reprovou |
|---|---|---|
| 1 | o critério fica cego às regras estreitadas | 8 testes, entre eles `test_a_cura_nao_toca_no_no_de_terceiro` |
| 2 | o check para de oferecer o conserto | `test_o_check_oferece_o_conserto_quando_ha_orfao` |
| 3 | a opção existe e o `main` não a chama | `test_o_main_chama_a_cura` |
| 4 | o restauro entra no `--fix` | `test_o_apply_fixes_nao_chama_a_cura` |
| 5 | `chmod 0660` no lugar de `chmod o=` | `test_a_cura_nao_alarga_a_mascara_da_acl` |
| 6 | o `--quiet` volta a calar a cura | `test_a_cura_fala_mesmo_com_quiet` |

### A número 5 passou verde na primeira tentativa, e isso é o registro que importa

A primeira versão do teste de ACL punha `u:nobody:rw` num nó `0666` e conferia
que a ACL sobrevivia. Com `chmod 0660` no lugar do `chmod o=`, ela **passava** —
porque num nó cuja máscara já é `rw-` os dois comandos chegam ao mesmo lugar.
Era um teste que descrevia a cura sem cobrar nada dela.

Pior: o comentário que eu tinha escrito no código ao lado dizia que o
`chmod 0660` *"poderia cortar acesso de quem tinha"*. A medição mostrou o
**contrário** — ele **alarga** a máscara. A asserção só passou a morder quando a
bancada montou o caso em que os dois comandos divergem (`mask::r--` sob uma
entrada `rwx`), e o comentário foi reescrito para dizer o que foi medido.

O teste antigo **ficou**, com nota datada dizendo que sozinho ele não morde: ele
é a asserção do caso comum, e é quem reprova se a cura um dia passar a apagar a
ACL inteira.

## O que ficou MEDIDO na máquina dela, hoje

Leitura pura, sem escrever em nada, em 07/08/2026:

- os seis nós `/dev/hidraw*` estão `660` com ACL `user:vitoriamaria:rw-`;
- `check_perms_soft` não imprime **nada** — não há sintoma;
- `_hidraw_alvos_do_restauro` devolve **vazio** — não há alvo;
- a única regra estreitada que abre hidraw a outros nesta máquina é a
  `71-pdp-controllers.rules:8`, e o aparelho dela não está conectado.

Ou seja: na máquina dela, hoje, **o conserto novo não aparece e não age**. É o
comportamento correto, e é o teste mais barato de que a oferta é condicionada.

---

## O que fica ABERTO

- **A escolha do mecanismo é dela para confirmar.** O comando fecha o nó
  (`chmod o=`) e **não concede** uaccess a nada. Se a intenção dela na resposta
  16 era um comando que também **conceda** — reinstalando a regra, ou pondo ACL
  —, isto aqui entrega metade. O motivo da escolha está medido e escrito acima;
  a palavra é dela. **GRAU: SEM PROVA** sobre a intenção, que não foi
  perguntada.
- **`udevadm trigger` como mecanismo alternativo não foi medido.** Se ele de
  fato recalcular o modo de um nó existente, é o mecanismo mais correto que este
  — pergunta ao udev em vez de decidir. Exige uma bancada que não seja a máquina
  dela. **GRAU: SEM PROVA.**
- **A varredura continua sem ler `ENV{...}` e `GOTO`** — herdado da
  `ACUSA-O-CULPADO-01`, e agora com uma consequência nova: uma regra que abra
  hidraw por caminho indireto não vira nem acusação nem inventário, e o nó dela
  seria classificado como **órfão**. O restauro nesse caso é atropelo, e o texto
  na tela já avisa que o nó pode reabrir — mas o aviso é consolo, não trava.
  **GRAU: SUSPEITA COM MECANISMO.**
- **A recusa `incerta` é grosseira.** Uma única regra estreitada por chave não
  avaliável (`KERNELS=="usb1"`) tira do doctor a capacidade de oferecer o
  conserto para **aquele nó**, mesmo que a regra fale de outro aparelho. É
  conservador de propósito, mas custa consertos legítimos. **GRAU: MEDIDO** (há
  teste); **SEM PROVA** de que aconteça em máquina real.
- **O caso oposto não é coberto:** nó fechado **demais** (0600 num aparelho que
  as regras do Hefesto deveriam abrir a 0660+uaccess). O `chmod o=` não faz nada
  por ele; quem cura é reaplicar as regras (`./install.sh`,
  `scripts/doctor.sh --fix`). Fica dito para ninguém procurar aqui.
- **Nada disto foi visto por ela na tela.** A `PROVA-DE-TELA-01` não se aplica
  (não há interface), mas o texto do doctor é interface por outro nome, e a
  palavra final sobre ele é dela.
