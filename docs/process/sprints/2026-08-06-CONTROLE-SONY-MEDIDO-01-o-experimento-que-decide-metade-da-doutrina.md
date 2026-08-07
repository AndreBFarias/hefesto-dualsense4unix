# CONTROLE-SONY-MEDIDO-01 — o experimento que decide metade da doutrina

- **Escrita em:** 06/08/2026, de madrugada, com a Steam fechada, o guarda de
  Steam Input vivo (último ciclo 01:15:24, próximo 01:45:24) e o
  `localconfig.vdf` dela exatamente no estado que este experimento precisa
- **Para quem:** para **ela**, no protocolo — este é o único documento desta
  faixa que um agente **não consegue fechar sozinho**. Precisa de um DualSense,
  da Steam e de dois jogos abertos de verdade
- **É o M-04** da tabela de suspeitas do estudo
  [o sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md),
  seção 2, e o **portão zero** declarado pela
  [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md)
  em `:244-250`
- **Sprints de que esta nasce, e que ela NÃO substitui:**
  [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md)
  (a E1 dela é o embrião deste documento) e
  [DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md)

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, arquivo no disco ou `git grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou. Esta sprint declara o grau em
cada bloco e **não herda** o grau de nenhuma das que cita.

> **ESTADO — 06/08/2026, 19:56. A E1 ESTÁ PAGA.** O experimento rodou com ela,
> com um DualSense físico e três jogos abertos de verdade, das **19:34 às
> 19:56**. O registro — que é a entrega — está na seção
> [O RESULTADO](#o-resultado--o-experimento-rodou-em-06082026-das-1934-às-1956).
> **O M-04 fecha POSITIVO, no grau MEDIDO.** O que a medição mostrou **além** da
> pergunta original está na mesma seção, e muda a doutrina da casa pela metade
> que ninguém tinha escrito.
>
> **O que da E1 NÃO foi pago:** a **versão do cliente Steam** não foi anotada —
> a MORDIDA a pedia por escrito, e ela é exatamente a variável que invalidou o
> resultado antigo. Ver *"O que continua aberto"*, no fim da seção do resultado.

---

## Por que esta sprint existe, e por que ela é dela

Ela pediu, em 06/08/2026, com estas palavras:

> *"sobre testar o controle da Sony, coloca como sprint. Na época tínhamos
> testado e tinha dado certo, mas não sei hoje."*

Isso é **informação nova**, e ela muda o grau do M-04.

Até 05/08 o projeto inteiro registrava o M-04 como *"o experimento nunca foi
feito"* — está assim, com essas palavras, na linha M-04 da tabela do estudo, e a
[STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md)
abre a E1 dela com *"Grau da pergunta: SEM PROVA. Ninguém, em nenhuma sessão,
verificou."*

**Isso estava errado, e o erro é nosso.** O experimento foi feito. Deu certo. A
pessoa que o fez foi ela, e ninguém anotou.

### O grau novo, escrito com honestidade

> **TESTADO E FUNCIONOU EM DATA NÃO REGISTRADA; SEM VERIFICAÇÃO DESDE ENTÃO.**
>
> Não é "SEM PROVA" — houve observação, e a testemunha é ela.
> Não é "MEDIDO" — porque **nada foi anotado**: nem a data, nem a versão da
> Steam, nem qual jogo, nem o que exatamente funcionou (só o input? os gatilhos
> adaptativos? a lightbar?), nem em que estado estava o global
> `SteamController_PSSupport` naquele dia.
>
> **Um resultado sem condições registradas não pode ser reproduzido nem
> refutado — e portanto não decide nada.** É exatamente por isso que o
> experimento precisa ser refeito, e desta vez **documentado**: com data, com o
> estado do `localconfig.vdf` antes, com o que foi observado passo a passo e com
> o veredito escrito nesta página.

E há um motivo concreto para não confiar no resultado antigo mesmo tendo
confiança nela: **a Steam se atualiza sozinha.** Entre "a época" e hoje passaram
atualizações de cliente que ninguém contou, e o comportamento sob teste é
justamente o de um componente da Steam. A memória dela é boa evidência sobre o
passado e **nenhuma evidência sobre hoje** — que é o que a própria frase dela
diz: *"mas não sei hoje"*.

---

## A NOTA DATADA DE CORREÇÃO — o que a allowlist faz, segundo ela

> **NOTA DATADA — 06/08/2026.** As sprints anteriores descrevem a exceção por
> jogo **ao contrário**. A correção é dela, e ela é a autoridade sobre a
> intenção do produto:
>
> *Quando um jogo tem conexão nativa com DualSense, os controles aparecem
> **dobrados** — um Xbox e um Sony — por causa do gamepad virtual do Hefesto.
> Permitir a allowlist faz o Hefesto **continuar funcionando**, com a saída
> sendo Xbox ou DualSense e as features que ela marcou nas abas.*
>
> Ou seja: **a allowlist não serve para "o Hefesto sair da frente".** O problema
> que ela resolve é o **duplo**; o resultado desejado é o Hefesto **seguir
> entregando** o controle e os recursos das abas, sem o sósia.

### Quais afirmações caducam (e ficam onde estão, com esta nota apontando)

Nenhuma linha abaixo é apagada. Cada uma foi escrita de boa-fé, e algumas eram a
melhor leitura possível na data em que foram escritas.

| Onde | O que está escrito | Por que caduca |
|---|---|---|
| [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md), E1, no bloco *"Por que isso decide metade da sprint"* | *"O que faria os jogos da allowlist funcionarem seria apenas o Hefesto sair da frente (ungrab + vpad suspenso)"* | descreve "sair da frente" como o **efeito desejado** da allowlist. Segundo ela, é o **efeito colateral a evitar** |
| a mesma E1, na tabela de leitura | *"a allowlist não é 'a lista dos jogos com Steam Input' — é 'a lista dos jogos em que o Hefesto se cala'"* | a conclusão continua sendo **um resultado possível do experimento**, mas deixa de ser a leitura que a sprint recomenda. Se for esse o desfecho, é **defeito**, não renomeação |
| a mesma E1, na linha 2 da tabela | *"o que muda é só o Hefesto sair da frente"* como veredito neutro | o mesmo: passa a ser leitura de **falha**, não de arquitetura correta |

> **NOTA DATADA — 06/08/2026, 19:56, sobre a tabela acima.** As três linhas
> **estão confirmadas pela medição**, e por um motivo mais forte do que a
> intenção do produto: durante a exceção o Hefesto **não sai da frente da
> saída** — os gatilhos dela seguraram e a cor dela ficou, com o jogo da
> allowlist aberto. E há uma quarta afirmação que caduca, que ninguém tinha
> escrito porque ninguém tinha medido: **fora da allowlist é que os ajustes dela
> perdem**, para o próprio jogo. Ver *A INVERSÃO*, na seção do resultado.

**O que NÃO caduca, e continua valendo inteiro:** o restante da
STEAM-QUE-DECIDE-01 — o F1 (o guarda apagou a escolha dela sobre o Sackboy às
14:52:12), o F4 (ela entra na allowlist por um clique e só sai por terminal), o
protocolo do experimento e o veto sobre escrever no `localconfig.vdf` com a
Steam viva. Nada disso depende da semântica corrigida.

### O DUPLO-REGISTRO-01 CONFIRMA a leitura dela — e é medição, não opinião

**Grau: MEDIDO**, em 26/07/2026, durante uma partida de Pragmata, e está
registrado em
[DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md),
seção *"O que foi medido — quatro joysticks para um controle"*:

```
js0  Hefesto Virtual DualSense P1                  <- o vpad do Hefesto
js2  Sony Interactive Entertainment DualSense ...  <- o controle FÍSICO, visível
js4  Microsoft X-Box 360 pad 0                     <- Steam Virtual Gamepad
js5  Microsoft X-Box 360 pad 1                     <- Steam Virtual Gamepad
```

**Um DualSense na mesa, quatro joysticks na frente do jogo.** É exatamente o
"controle dobrado" que ela descreve — e a observação dela de hoje é a **mesma
observação** de 26/07, dita por quem estava jogando em vez de por quem estava
lendo `/proc/bus/input/devices`.

O relato dela naquele dia, que está no topo daquela sprint e nunca foi
contestado, fecha a leitura:

> *"jogos com conexão nativa, devemos usar o ativar steam pra ele funcionar"*
>
> *"eu tava com a steam ativada e tava funcionando perfeitamente, lightbar,
> trigger, vibração tudo"*

Note o que ela cita como o que funcionava: **lightbar, gatilhos e vibração** —
que são recursos que o Hefesto escreve no controle físico, não coisas que a
Steam entrega. Ela não estava descrevendo o Hefesto calado. Estava descrevendo o
Hefesto **funcionando sem o sósia**.

### E agora a tensão que esta sprint tem de registrar, e não pode resolver sozinha

**Grau: MEDIDO por leitura de código, em 06/08.** O que o produto faz hoje,
quando um appid da allowlist entra em sessão, está em
`daemon/subsystems/gamepad.py`, na função `sync_steam_input_exception` (`:231`):

1. **solta o grab do evdev** — o físico volta a ficar visível (`:166-169`, e o
   comentário do R-06 em `:161-164` diz *"a exceção existe justamente para o
   jogo ver o controle físico"*);
2. **para de esconder o hidraw** (`:207-212`), com a justificativa medida de que
   *"a Steam precisa LER o hidraw para entregar o DualSense pela API dela
   (SetDualSenseTriggerEffect)"*;
3. **e retira o gamepad virtual de cena**, por `suspend_vpads_for_steam_input`
   (`:425`), cuja docstring declara o princípio em letras: *"um controle físico
   produz exatamente UM dispositivo de jogo: nos appids da allowlist esse
   dispositivo é o FÍSICO"*.

O item 3 é **literalmente "o Hefesto sai da frente"** — e a decisão tem dono, data
e motivo medido (JOGO-01, 25/07: com o vpad de pé o Mullet Mad Jack dava jogador
1 a um dispositivo e jogador 2 ao outro).

**Os dois lados estão certos sobre metade do problema, e a metade não bate:**

- **Ela está certa sobre o defeito.** O duplo é real, foi medido duas vezes
  (26/07 no Pragmata; 25/07 no Mullet Mad Jack) e é o que estraga o jogo.
- **O código está certo sobre uma cura possível.** Tirar o vpad acaba com o
  duplo — e acaba.
- **Ela está pedindo a OUTRA cura**, a que o código não tentou: acabar com o
  duplo **mantendo** o Hefesto no caminho, com a máscara que ela escolheu e os
  recursos das abas.

**A pergunta que fica, e é o segundo eixo do experimento:** com um jogo da
allowlist rodando *hoje*, o que ela vê na tela do jogo — um controle ou dois? E a
lightbar, os gatilhos e a vibração continuam obedecendo às abas?

> **SUSPEITA COM MECANISMO, e é a única coisa que reconcilia os dois lados:**
> `grep` por `steam_input_excecao_ativa` e `steam_input_vpad_suspenso` em `src/`
> devolve consumidores **só** em `daemon/subsystems/gamepad.py`,
> `daemon/lifecycle.py` e `daemon/ipc_handlers.py` — **nenhum applier de
> lightbar, gatilho ou vibração consulta esses flags**. Ou seja: em tese, a
> exceção retira o **dispositivo de entrada** virtual e **não desliga** os
> recursos que o daemon escreve por hidraw no controle físico. Se isso for
> verdade em jogo, a fala dela e o código descrevem o mesmo comportamento com
> palavras diferentes — "a saída sendo Xbox ou DualSense" seria a única parte a
> conciliar. **Não foi observado em jogo nenhum. É o passo 2.4 do protocolo.**

---

## O que está MEDIDO na máquina dela AGORA — e é o cenário exato do experimento

**Grau: MEDIDO**, em 06/08/2026 por volta das 01h20. **Só appids aparecem aqui —
eles são públicos; a pasta de `userdata` e o número da conta não entram em
arquivo versionado.**

```
localconfig.vdf, linha 1277:  "SteamController_PSSupport"   "0"     <- global DESLIGADO
per-app com UseSteamControllerConfig != "0":
    appid 3357650  ->  "2"     (Pragmata,        NA allowlist)
    appid 2111190  ->  "2"     (Mullet Mad Jack, NA allowlist)
mtime do arquivo: 05/08 14:52:12   <- a hora exata em que o guarda zerou o Sackboy
```

Allowlist dela (`steam_input_apps.txt`, 15 linhas, das quais **duas** são
appids): `2111190` e `3357650`.

Guarda vivo e no ciclo:

```
hefesto-steam-input-guard.timer   ActiveState=active  UnitFileState=enabled
  LAST  2026-08-06 01:15:24        NEXT  2026-08-06 01:45:24
hefesto-steam-input-guard.path    ActiveState=active
Steam: fechada (pgrep steam = 0)
```

**A configuração sob teste é a configuração de produção dela, hoje, sem tocar em
nada.** Global em `"0"`, per-app em `"2"` nos dois jogos da allowlist. É a
premissa em que a exceção inteira se apoia, e é ela que o experimento mede.

A regra que produz esse estado está em `scripts/disable_steam_input.sh`: a
allowlist é lida em `:226`, o `_transform_vdf` começa em `:231`, os globais
(`SteamController_PSSupport` e `SteamController_SwitchSupport`) são zerados
**sempre**, e o `UseSteamControllerConfig` por bloco só é preservado quando o
appid do bloco está na allowlist.

---

## E1 — O EXPERIMENTO

**Grau da pergunta hoje: TESTADO E FUNCIONOU EM DATA NÃO REGISTRADA; SEM
VERIFICAÇÃO DESDE ENTÃO** (ver o bloco de grau, acima).

### A pergunta, em uma linha

`UseSteamControllerConfig "2"` por jogo funciona com `SteamController_PSSupport
"0"` global?

### E o segundo eixo, que a correção dela acrescentou

Com a exceção ativa, **quantos controles o jogo enxerga**, e **os recursos das
abas continuam valendo**?

### O que precisa

Um **DualSense**, a **Steam**, e **dois jogos**: o `2111190` (Mullet Mad Jack,
na allowlist) e **qualquer outro jogo dela que não esteja na allowlist**.
Duração estimada: 25 minutos, sendo 20 de jogo aberto.

### Passo 0 — trancar o cenário

O guarda roda a cada 30 minutos e a unidade `.path` reage a mudança de arquivo.
Sem isto, ele reescreve o `localconfig.vdf` **no meio do experimento** e o
resultado não quer dizer nada:

```
systemctl --user stop hefesto-steam-input-guard.timer
systemctl --user stop hefesto-steam-input-guard.path
```

E, **ao terminar** — isto não é apêndice, é parte do protocolo; sem as duas de
volta o produto dela fica sem rede de segurança:

```
systemctl --user start hefesto-steam-input-guard.path
systemctl --user start hefesto-steam-input-guard.timer
```

### Passo 1 — fotografar o antes

Com a Steam aberta, o controle ligado e **nenhum jogo aberto**:

```
grep -E '^N: Name' /proc/bus/input/devices
```

**O que anotar:** quantas linhas dizem `X-Box 360 pad` (são os gamepads virtuais
que o Steam Input cria), quantas dizem `DualSense`, e se aparece o
`Hefesto Virtual DualSense`.

Este é o **número de referência**. Sem ele, os passos 2 e 3 não têm com o que
comparar.

### Passo 2 — o jogo da allowlist (Mullet Mad Jack, `2111190`)

Abrir, esperar chegar ao menu, e então:

**2.1** — rodar de novo o `grep` do passo 1 e anotar o novo quadro.

**2.2** — **contar os controles DENTRO do jogo**, na tela de configuração de
controle dele. É esta a pergunta dela: *aparece um, ou aparecem dois (um Xbox e
um Sony)?*

**2.3** — as três perguntas de recurso, uma de cada vez:

1. o controle **anda** no menu?
2. os **gatilhos** oferecem resistência (o efeito adaptativo) em algum momento?
3. a **lightbar** muda de cor?

**2.4** — **o eixo novo, e o que decide a NOTA DATADA acima:** com o jogo aberto,
mexer numa coisa da aba Emulação ou de gatilhos **e ver se muda no controle**.
Se a cor que ela escolheu na aba aparece no aparelho com o jogo rodando, o
Hefesto **continua funcionando** durante a exceção, e a leitura dela está certa
por inteiro. Se nada obedece, a exceção **realmente** cala o produto, e é a nota
que caduca — não a fala dela.

### Passo 3 — o jogo de controle (fora da allowlist)

Fechar o primeiro, abrir o segundo jogo, repetir **2.1 a 2.4** com as mesmas
perguntas. Sem este passo o experimento não tem contraste e **não conclui nada**:
os `X-Box 360 pad` podem aparecer por motivo que nada tem a ver com o per-app.

### Passo 4 — SÓ se o passo 2 falhar, e SÓ com a Steam FECHADA

Isolar a causa ligando o global à mão. **Com a Steam encerrada**, trocar
`"SteamController_PSSupport"` de `"0"` para `"2"` no `localconfig.vdf` (linha
1277 hoje), reabrir a Steam e repetir o passo 2.

**Se com o global ligado funcionar e com ele desligado não, o global é o portão e
o per-app é decorativo.** Ao terminar, quem devolve o estado do produto é
`scripts/disable_steam_input.sh --apply`, também com a Steam fechada.

### A tabela de leitura do resultado

| Passo 2 (allowlist) contra passo 3 (fora dela) | Veredito | O que significa para o produto |
|---|---|---|
| Os `X-Box 360 pad` aparecem **só** no jogo da allowlist; o jogo lista **um** controle; gatilhos e lightbar respondem | **Per-app honrado, inteiro.** M-04 fecha positivo | A arquitetura está certa. As entregas E2 a E6 da [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md) seguem como escritas |
| Aparecem só na allowlist, o jogo lista **um** controle, **e o passo 2.4 mostra as abas obedecendo** | **Per-app honrado, e a leitura dela de 06/08 confirmada** | A NOTA DATADA acima vira a doutrina da casa. Todo texto de tela sobre a exceção passa a dizer *"o Hefesto continua entregando"*, e não *"o Hefesto sai da frente"* |
| Aparecem só na allowlist, o jogo lista **um** controle, mas no 2.4 **nada das abas obedece** | **Per-app honrado, produto calado durante o jogo** | A cura atual funciona e o **preço** é real. Ela decide se aceita — e o texto de tela tem de contar o preço, que hoje não conta |
| O jogo lista **dois** controles (um Xbox e um Sony) mesmo na allowlist | **O duplo sobreviveu à exceção** | É a queixa dela, viva, com a exceção ligada. Vira defeito de prioridade alta e **antecede** qualquer trabalho de texto ou de tela |
| Os `X-Box 360 pad` aparecem nos **dois** jogos, iguais | O per-app não está discriminando nada | O que muda entre os dois é só o comportamento do Hefesto. A allowlist não é o que o nome diz, e os textos de tela mudam de forma |
| Não aparecem em **nenhum** dos dois | **Per-app ignorado com o global em `"0"`.** M-04 fecha negativo | O botão *"Este jogo não funciona"* nunca entregou o que promete. Metade da STEAM-QUE-DECIDE-01 muda de forma, e o passo 4 vira obrigatório |
| Aparecem só na allowlist, mas gatilhos e lightbar **mortos nos dois** | **Meia entrega.** O portão dos recursos de PlayStation é o global | A exceção precisa ligar o global durante o jogo, ou o produto para de prometer gatilho adaptativo. É o caso mais traiçoeiro: entrega input e não entrega o que ela citou como o que funcionava |

### A MORDIDA

**Esta entrega não tem teste — ela tem registro.** O produto dela é uma seção
nova **nesta página**, com:

- a **data e a hora** do experimento;
- a **versão do cliente Steam** (Steam → Ajuda → Sobre), que é a variável que
  invalidou o resultado antigo e vai invalidar este também, um dia;
- o `grep -E '^N: Name' /proc/bus/input/devices` **colado cru** dos passos 1, 2
  e 3;
- quantos controles o jogo listou em cada passo;
- as respostas das três perguntas de recurso e do passo 2.4;
- o **veredito**, escolhido na tabela acima, no grau **MEDIDO**.

**A regra que faz esta sprint valer a pena:** se o experimento rodar e o registro
não for escrito, **o experimento não aconteceu** — é exatamente o que houve com o
teste antigo, e é o motivo de estarmos aqui de novo. O registro é a entrega; a
observação é só o insumo.

### O VETO

- **Nada de código de Steam Input antes desta seção existir.** Nenhuma linha em
  `scripts/disable_steam_input.sh`, em `integrations/steam_launch_options.py`,
  no botão da aba Sistema ou no cartão proposto pela
  [STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md).
  Todas essas entregas assumem que a exceção per-app faz alguma coisa, e é isso
  que ainda não sabemos.
- **Não rodar o passo 4 com a Steam aberta.** A regra da casa é nunca escrever no
  `localconfig.vdf` com a Steam viva: ela reescreve o arquivo inteiro ao sair e
  come a edição. Está registrada desde o DUPLO-REGISTRO-01.
- **Não deixar as unidades do guarda paradas.** O `systemctl --user start` das
  duas é passo do protocolo.
- **Um agente não edita a allowlist dela nem o `localconfig.vdf` para "preparar"
  o experimento.** O cenário já está pronto e é o de produção. Mexer nele
  destrói justamente a coisa que se quer medir.
- **Não "consertar" o Sackboy.** Ele foi zerado às 14:52:12 de 05/08 e continua
  fora. Devolver o `"2"` sem perguntar é inventar decisão dela — e essa
  conversa tem lugar próprio, na E6 da STEAM-QUE-DECIDE-01.

---

## O RESULTADO — o experimento rodou em 06/08/2026, das 19:34 às 19:56

**Esta seção é a entrega da E1.** A regra estava escrita na MORDIDA: *"se o
experimento rodar e o registro não for escrito, o experimento não aconteceu"*.
Ele rodou; aqui está o registro.

### As condições, e uma lacuna declarada

**Grau: MEDIDO** (tudo abaixo saiu de arquivo ou de journal com carimbo).

- **Guarda parado**, como manda o Passo 0: `timer=inactive path=inactive` às
  19:34:23.
- **Steam aberta** (processo vivo) e **daemon `active`**.
- **Um DualSense físico**, por Bluetooth.
- **Os três jogos com o wrapper `hefesto-launch` nas Opções de Inicialização**,
  conferido antes de começar.
- **A allowlist e o `localconfig.vdf` não foram tocados**: o cenário medido é o
  de produção dela, como o VETO exigia.

**A lacuna, e ela é nossa:** a **versão do cliente Steam não foi anotada**. A
MORDIDA a pedia com todas as letras, porque é a variável que invalidou o
resultado antigo — e que vai invalidar este também, um dia. **Não há como
recuperá-la depois do fato sem repetir o experimento**, então ela fica declarada
como falta, não como detalhe.

### Passo 1 — a linha de base, 19:34:23, sem jogo aberto

```
X-Box 360 pad                                          : 0
DualSense Wireless Controller (Hefesto P1)  [virtual]  : 4 nós
DualSense Wireless Controller               [físico]   : 3 nós
```

Quem estava preso, no mesmo instante:

```
/dev/input/event8   DualSense Wireless Controller                  -> PRESO (grab exclusivo)
/dev/input/event9   DualSense ... Motion Sensors                   -> LIVRE
/dev/input/event10  DualSense ... Touchpad                         -> LIVRE
/dev/input/event12  DualSense ... (Hefesto P1)                     -> LIVRE
```

Ou seja: **o Hefesto prendia o nó de botões do físico e mais nada** — os nós de
sensores e touchpad do físico, e os quatro nós do virtual, estavam livres.

### Passo 2 — Mullet Mad Jack (appid `2111190`), NA allowlist

**O journal, com carimbo (MEDIDO):**

```
19:39:52  launch_arm_pulado_allowlist_steam_input  appid=2111190
19:39:52  steam_input_excecao_ativada              appid=2111190
19:39:52  gamepad_controller_grab                  grab=False
19:39:52  steam_input_vpad_suspenso                appid=2111190 flavor=dualsense jogadores_coop=0
19:39:52  launch_env_materializado                 emulacao=False
19:39:59  gamepad_start_recusado_steam_input       origem=profile
```

**O sistema às 19:41:12, com o jogo no menu (MEDIDO):**

| | passo 1 (19:34) | passo 2 (19:41) |
|---|---|---|
| `X-Box 360 pad` | 0 | **1** (`Microsoft X-Box 360 pad 1`) |
| Hefesto virtual | 4 nós | **0** — derrubado |
| DualSense físico | 3 nós | 3 nós |
| hidraw abertos pelo daemon | — | **1** |

**O que ela viu na tela do jogo, às 19:44:46 (MEDIDO — a testemunha é ela):**

| Pergunta do protocolo | Resposta |
|---|---|
| 2.2 quantos controles o jogo lista | **UM** |
| 2.2 como aparece | **Xbox** (LT/RT/LB/RB, A/B/X/Y) |
| 2.2 input duplicado no menu | **NÃO** |
| 2.3 gatilhos | **DUROS** — a Resistência que **ela** aplicou segurou |
| 2.4 lightbar com o jogo aberto | o **vermelho dela** foi aplicado e **FICOU** |

A exceção esteve ativa das **19:39:52 às 19:45:32**, e o teste de lightbar do
2.4 (por volta das 19:43) caiu **dentro** dessa janela — não depois dela.

### Passo 3 — Sackboy (appid `1599660`), FORA da allowlist

**O sistema às 19:49:29, jogo rodando (MEDIDO):**

```
Hefesto virtual : 4 nós   (de pé)
X-Box 360 pad   : 0       (nenhum)
DualSense físico: 3 nós, mas ESCONDIDO do jogo pelo default.env:
    PROTON_DISABLE_HIDRAW=0x054C/0x0CE6
    SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6
```

**O que ela viu, às 19:55:53 (MEDIDO):**

| Pergunta | Resposta |
|---|---|
| controles listados | **UM**, com botões de **PlayStation** — a máscara dela foi respeitada |
| o controle anda | **SIM**, normal |
| gatilhos | **MOLES** — a Resistência dela **não** segurou |
| lightbar | **AZUL**, o padrão da Sony; **não** a cor dela |
| aplicar cor pela janela | muda por um instante, e **o jogo devolve ao azul** |

### Qual linha da tabela de leitura se realizou

A **segunda**, literalmente:

> *"Aparecem só na allowlist, o jogo lista **um** controle, **e o passo 2.4
> mostra as abas obedecendo"* -> **Per-app honrado, e a leitura dela de 06/08
> confirmada.**

As outras seis estão **descartadas por medição**: os `X-Box 360 pad` não
apareceram nos dois jogos (linha 5, descartada), apareceram em um deles (linha 6,
descartada), o jogo da allowlist listou **um** controle e não dois (linha 4,
descartada), e gatilho e lightbar **obedeceram a ela** durante a exceção
(linhas 3 e 7, descartadas).

### O VEREDITO — M-04 FECHA POSITIVO

> **GRAU: MEDIDO, 06/08/2026.** `UseSteamControllerConfig "2"` por jogo **é
> honrado** com `SteamController_PSSupport "0"` global. A prova é o contraste:
> o `Microsoft X-Box 360 pad 1` do Steam Input **nasceu só no jogo da allowlist**
> e **não existiu** no jogo fora dela, na mesma máquina, no mesmo intervalo de
> dez minutos, com o mesmo controle e o mesmo global desligado.
>
> **O botão "Este jogo não funciona" entrega o que promete.** A suspeita M-04 —
> *"a exceção per-app pode ser decorativa"* — está **refutada**.

Consequência imediata, e é a que a tabela previa: **as entregas E2 a E6 da
[STEAM-QUE-DECIDE-01](2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md)
seguem como estão escritas**, e o VETO desta sprint (*"nada de código de Steam
Input antes desta seção existir"*) está **cumprido e suspenso**.

### A LEITURA DELA ESTÁ CONFIRMADA — e a doutrina da casa estava pela metade

**GRAU: MEDIDO.** A NOTA DATADA do topo desta página dizia que a allowlist não
serve para *"o Hefesto sair da frente"*, e que o Hefesto **continua entregando**
os recursos das abas. O passo 2.4 mediu exatamente isso: com o Mullet Mad Jack
aberto e a exceção ativa, **os gatilhos dela seguraram e a cor dela ficou**.

E o mecanismo é **estrutural, não sorte**: durante a exceção o Hefesto abre mão
da **ENTRADA** e mantém **integralmente a SAÍDA**.

| O que a exceção faz | Onde | Efeito |
|---|---|---|
| solta o grab do evdev | `daemon/subsystems/gamepad.py:271` | **entrega a entrada** ao jogo (é a linha do `gamepad_controller_grab grab=False` das 19:39:52) |
| desfaz o esconde-esconde do hidraw | `gamepad.py:272-279` (`restore_all`) | o físico volta a ser **legível** pelos outros processos |
| derruba o gamepad virtual | `gamepad.py:283-284` -> `:425` | acaba com o **duplo** |
| **nada** | — | **nenhum caminho fecha o handle de saída do daemon** |

A ausência é o achado. **Grau: MEDIDO por leitura, 06/08 nesta árvore:** os
**oito** chamadores de `steam_input_excecao_ativa` estão **todos** em
`gamepad.py` (`:166`, `:207`, `:265`, `:366`, `:370`, `:649`, `:1134`, `:1386`) e
**nenhum** em `core/`. Não existe portão da exceção no caminho de saída —
lightbar, gatilhos, vibração e LEDs de jogador seguem sendo escritos no controle
físico durante a exceção inteira. É por isso que `hidraw abertos pelo daemon` era
**1** às 19:44:46.

> A frase *"o Hefesto sai da frente"* — e as irmãs *"sai de cena"* e *"fora do
> caminho"*, **25 linhas** em `src/` e `docs/usage/` (MEDIDO por `grep`, 06/08) —
> descreve **só a primeira metade** do mecanismo. Ela está certa sobre a entrada e
> **errada sobre a saída**.

### A INVERSÃO — o que ninguém tinha escrito

**GRAU: MEDIDO quanto ao comportamento observado.**

| | ENTRADA (quem o jogo enxerga) | SAÍDA (luz, gatilhos) |
|---|---|---|
| **NA allowlist** (Mullet) | o Hefesto **perde**: solta o grab, derruba o vpad | o Hefesto **ganha**: os ajustes **dela** vencem |
| **FORA dela** (Sackboy) | o Hefesto **ganha**: o vpad é o único dispositivo | o Hefesto **perde**: o **jogo** vence |

**A exceção da inversão, e ela é medida por leitura de código (06/08):** no
**rumble** a política é a contrária — a usuária vence mesmo fora da allowlist.
`apply_game_rumble` ignora o FF do jogo quando há rumble fixado manual
(`daemon/subsystems/gamepad.py:747-748`) e aplica o multiplicador do slider
global (`:750-752`). **A inversão vale para lightbar, gatilhos e LED de jogador;
não vale para vibração.**

### O MECANISMO da segunda metade — e ele está escrito, é política, não defeito

**GRAU: MEDIDO por leitura de código, 06/08.**

1. `integrations/uhid_gamepad.py:1564-1571` declara o que é um `UHID_OUTPUT`:
   *"o jogo escreveu no hidraw do vpad (rumble/LED/gatilhos)"*, e o REPLICA-03
   replica cada categoria **ao controle físico** daquele jogador.
2. Um jogo com suporte nativo a DualSense escreve **no vpad** — que é um
   DualSense Edge de verdade para o kernel — e o Hefesto **repassa fielmente ao
   físico**. É por isso que o Sackboy devolve o azul e amolece os gatilhos dela.
3. A precedência que faz o **jogo vencer a usuária** está declarada num ponto
   único, `core/backend_pydualsense.py:1253-1259`: *"camada GAME (REPLICA-03) >
   camada CO-OP (R-13) > override explícito por-uniq (perfil/usuária, R-20) >
   camada AUTOMÁTICA (COR-03) > default global do perfil"*, executada em
   `:1307-1308`. **Não é corrida nem acidente: é a política escrita.**
4. O único contrapeso é o gate de autoridade (`_game_wins`,
   `backend_pydualsense.py:1232-1248`), e ele é **fail-safe para o lado do
   jogo**: só a autoridade `daemon` **explícita** fecha o portão.

### HÁ DOIS CAMINHOS para um jogo falar DualSense, e a casa tratava como um só

**GRAU: SUSPEITA COM MECANISMO** quanto à atribuição; **MEDIDO** quanto ao
comportamento e quanto à ausência da distinção no repositório.

| Caminho | Exemplo medido | Precisa de Steam Input? | O que faz com os ajustes dela |
|---|---|---|---|
| **por HID direto** (o jogo escreve no hidraw do dispositivo) | **Sackboy** | **não** — funcionou sem a lista | **atropela**: o jogo pinta o vpad, a réplica chega ao físico, a camada GAME vence |
| **por Steamworks** (`SetDualSenseTriggerEffect`) | **Mullet Mad Jack** | **sim** — o pedido passa pela Steam, e sem o Steam Input daquele jogo não tem por onde chegar | **respeita**: o Hefesto mantém a saída durante a exceção |

**Logo a allowlist NÃO é "a lista dos jogos com DualSense nativo". É "a lista dos
jogos cujo DualSense passa pela Steam".** O Sackboy tem suporte nativo e **não
precisa** da lista — tanto que funcionou sem ela, com a máscara dela respeitada.

**Por que o grau não sobe:** ninguém leu os símbolos dos dois binários. A
atribuição *este usa Steamworks, aquele usa HID direto* é a explicação mais
simples do observado, e continua **SUSPEITA COM MECANISMO** até alguém abrir os
executáveis. **Grau MEDIDO, e este é separado:** a distinção **não existe em
lugar nenhum do repositório** — `grep` por `HID direto`/`hid direto` em `.py`,
`.md`, `.sh` e `.txt` devolve **zero**, enquanto a metade Steamworks está
nomeada em quatro pontos (`daemon/launch_env.py:345-348`,
`integrations/storm_doctor.py:30-31`, `daemon/subsystems/gamepad.py:208-211` e
`:432-434`).

### AS QUATRO RESSALVAS — onde o relato bruto atribuiu a linha errada

Estas correções vêm de leitura de código feita no mesmo dia, e **nenhuma delas
muda o veredito**. Ficam porque a casa não deixa passar atribuição frouxa.

1. **`modo_jogo_padrao_solto motivo=janela_fora_do_jogo wm_class=steam` NÃO é o
   fim da exceção. Grau: MEDIDO.** Essa linha é emitida em
   `daemon/lifecycle.py:2284-2290`, dentro de `reverter_modo_jogo_padrao` — é o
   **modo jogo padrão (MODO-01/B3)**, outro subsistema, chamado pelo autoswitch.
   O fim da exceção do Steam Input tem log próprio: `gamepad.py:286`,
   `steam_input_excecao_encerrada`.
2. **O journal não consegue dizer POR QUE a exceção terminou. Grau: MEDIDO.** A
   borda de entrada loga o appid (`gamepad.py:270`); a de saída
   (`gamepad.py:286`) **não tem campo nenhum** — sem `motivo`, sem `appid`.
   Reconstruir o desfecho das 19:45:32 a partir do journal é **impossível hoje**,
   e isso é dívida de instrumento.
3. **O que provavelmente encerrou a exceção às 19:45:32. Grau: SUSPEITA COM
   MECANISMO.** O marker `last_run` do wrapper é **um arquivo global, não por
   appid** (`assets/hefesto-launch.sh:120-132`; leitura em
   `daemon/launch_env.py:393`). Lançar o segundo jogo **sobrescreveu** o marker
   do primeiro: a partir daí a evidência autoritativa apontava `1599660`, que
   não está na allowlist, e o foco estava na Steam. A exceção caiu **com o Mullet
   ainda rodando** (às 19:45:59 o processo ainda registrava `AppId=2111190`), e o
   `default.env` foi regravado às 19:45:34 — a assinatura do vpad voltando.
   **Não foi alt-tab; foi o segundo lançamento.** Não há linha de journal que
   prove isso, e por isso o grau não sobe (ver a ressalva 2).
4. **`lightbar_reassert_skip_cache rgb=(198, 70, 0)` não é prova de escrita do
   jogo. Grau: MEDIDO.** A linha significa *"um reassert pediu exatamente a cor
   que já estava no cache desta instância, e a escrita foi pulada"*
   (`core/sysfs_leds.py:194-202`) — é telemetria da cura do flash azul da
   GUERRA-01. Ela sai **uma vez na vida da instância** (`_skip_logged` nasce em
   `:65`, vira `True` em `:202` e **nunca** é rearmado; quem tem rearme é o
   `_foreign_logged`, e o comentário de `:66-68` diz isso), então o valor
   `(198, 70, 0)` é o do **primeiro** acerto de cache daquele nó, **não** o
   estado das 19:52:50. E o nó do carimbo, `input1011`, é o **físico por
   Bluetooth** (`0005:054C:0CE6`), **não** o vpad (`0003:054C:0DF2`). A origem da
   cor `(198, 70, 0)` é **SUSPEITA COM MECANISMO**: por eliminação não é perfil
   dela, não é a paleta automática, não é o azul do kernel — sobra a camada GAME,
   e não há linha de journal que carimbe a cor na entrada da réplica.

### O QUE ESTA MEDIÇÃO PAGA

- **A E1 desta sprint**, inteira, menos a versão do cliente Steam.
- **O M-04** do estudo dos dezessete agentes: fecha **POSITIVO**, grau MEDIDO.
- **O portão zero da STEAM-INPUT-01** (`:244-250`), aberto desde 26/07.
- **A NOTA DATADA do topo desta página**: confirmada pela medição, e agora
  **completada** — a leitura dela estava certa, e faltava a metade da inversão.
- **O P3 do desenho da caixinha**
  ([o desenho da flag do jogo](../estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md)):
  ela respondeu *"esperar o experimento"* em 06/08. **O experimento fechou; o P3
  está destravado.**

### O QUE CONTINUA ABERTO — e é decisão, não esquecimento

1. **A versão do cliente Steam do dia do experimento.** Não anotada, não
   recuperável. Quem repetir isto anota **antes** de abrir o primeiro jogo.
2. **A atribuição Steamworks contra HID direto** continua **SUSPEITA COM
   MECANISMO**. Fecha lendo os símbolos dos dois binários — e só isso a fecha.
3. **A pergunta 5.1 do desenho da caixinha** — *a Steam aceita o **vpad** como o
   DualSense que ela entrega ao jogo?* — **NÃO foi respondida**. O experimento
   mediu o mundo como ele é hoje (o vpad é derrubado antes de a Steam olhar), não
   o mundo invertido. Continua **SEM PROVA**, e é outro experimento.
4. **O log de saída da exceção não diz o motivo** (`gamepad.py:286`). Enquanto
   for assim, todo desfecho de exceção é reconstrução, não medição.
5. **O `last_run` global** (ressalva 3) derruba a exceção de um jogo quando um
   segundo é lançado, com o primeiro ainda vivo. Não foi medido em partida real
   dela — foi medido **neste** experimento, por acidente, e merece defeito
   próprio.
6. **A contradição do `steam_input_apps.txt`**: os dois appids da lista têm
   justificativas **incompatíveis entre si** (um por Steamworks, outro por
   duplicado), e o cabeçalho do arquivo define a lista de um jeito só. A doutrina
   nova desta seção diz qual é o critério certo; **ninguém reescreveu o arquivo**,
   e um agente não mexe na lista dela.
7. **O M-17** (qual máscara é a certa para cada jogo) **não fecha aqui.** O que a
   medição acrescenta, e é MEDIDO: o Sackboy rodou com máscara `dualsense`,
   listou **um** controle e mostrou **botões de PlayStation**. Isso é um dado
   sobre o Sackboy, não sobre o preset `sackboy_nativo` — que pede `xbox`.

---

## O QUE ESTA SPRINT NÃO COBRE — e é decisão, não esquecimento

- **A política do guarda.** Ele continua zerando o que encontra fora da
  allowlist. Mudar isso é decisão de produto e depende do veredito daqui.
- **O duplo cadastro** (Steam contra allowlist do Hefesto). É a
  [DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md),
  aberta desde 26/07, e o experimento não a fecha nem a abre.
- **O M-05** — se é seguro ler o `localconfig.vdf` com a Steam viva. Continua
  **SEM PROVA** e é entrada de outra entrega.
- **Qual máscara é a certa para cada jogo** (o M-17 do estudo, a contradição
  entre `docs/usage/jogos-e-mascaras.md` e o preset do Sackboy). Resolve-se em
  jogo, não aqui.

---

## O QUE NÃO FOI MEDIDO NESTA SESSÃO

> **NOTA DATADA — 06/08/2026, 19:56.** Esta lista descreve a sessão de
> **escrita**, de madrugada (01h20). Ela **fica como está**, porque decisão
> medida não se apaga e porque era honesta na hora em que foi escrita. Mas cinco
> dos seis itens abaixo **foram pagos** pelo experimento das 19:34, e a seção
> [O RESULTADO](#o-resultado--o-experimento-rodou-em-06082026-das-1934-às-1956)
> é quem os paga: três jogos foram abertos, ela olhou a tela, os controles foram
> contados **dentro** do jogo, e os appliers de lightbar e gatilho foram medidos
> com o jogo de pé — obedecendo a ela no jogo da allowlist e obedecendo ao
> **jogo** fora dela. **O que continua sem resposta é o primeiro parágrafo do
> teste antigo:** em que data ele foi feito, com que versão da Steam, com qual
> jogo e com o global em que estado. Isso segue irrecuperável.

- **Nenhum jogo foi aberto.** Tudo nesta página é arquivo, journal, `systemctl` e
  código. É exatamente por isso que ela existe.
- **Não vi a tela.** Nenhuma afirmação sobre a janela veio de foto.
- **Não sei em que data o teste antigo foi feito**, nem com que versão da Steam,
  nem com qual jogo, nem se o global estava ligado naquele dia. **Se estivesse
  ligado, o teste antigo não mediu o que a gente precisa saber** — e essa
  possibilidade sozinha já justifica refazer.
- **Não sei se os appliers de lightbar e gatilho continuam escrevendo no controle
  durante a exceção.** O `grep` diz que eles não consultam os flags da exceção
  (SUSPEITA COM MECANISMO); ninguém olhou o controle com o jogo aberto.
- **Não contei os controles dentro de nenhum jogo.** Os quatro joysticks de
  26/07 são de `/proc/bus/input/devices`, não da tela de configuração do jogo —
  e é a tela do jogo que ela vê.
