# STEAM-QUE-DECIDE-01 — ela não tem como saber quando ligar

- **Escrita em:** 05/08/2026, por volta das 23h, com o daemon vivo, a Steam
  aberta e o guarda do Steam Input rodando o ciclo dele de 30 em 30 minutos
- **Para quem:** agentes, em execução autônoma. Cada entrega traz a **mordida**
  esperada e o **veto**. Nenhuma precisa de auditoria nova para começar — mas a
  **E1 é portão de entrada das demais** e não se pula
- **Base factual:**
  [o sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md),
  seção 1.5 (D-31 a D-34) e as linhas M-04 e M-05 da tabela de suspeitas
- **Sprints de que esta nasce, e que ela NÃO substitui:**
  [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md)
  e
  [DUPLO-REGISTRO-01](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md)

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, arquivo no disco ou `git grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou. Esta sprint declara o grau em
cada bloco e **não herda** o grau das duas que cita.

---

## O relato dela

> *"não faço ideia de quando é pra ativar os controles Steam e quando não. Ou
> quando é pra ir colocar os comandos da Steam em cada app, ou se os botões lá
> prestam ou não."*

Dito em 05/08/2026. Não é a mesma queixa de 26/07 com outras palavras — é a
mesma queixa **dez dias depois de a sprint que prometia resolvê-la ter sido
escrita**, e agora com um terceiro eixo (*"os comandos da Steam em cada app"*,
que é a lane das opções de inicialização) misturado ao primeiro.

---

## A NOTA DATADA QUE ESTA SPRINT EXISTE PARA ESCREVER

> **NOTA DATADA — 05/08/2026.** A
> [STEAM-INPUT-01](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md)
> se chama **"ela nunca mais precisa decidir quando ligar a entrada Steam"**.
> Aquele nome descreve o objetivo, não o produto. **Dez dias depois, o estado
> medido é o oposto: ela precisa decidir, o tempo todo, sem critério e sem
> informação — e quando decide, o produto desfaz a decisão em silêncio.**
>
> A decisão original **não se apaga e continua certa**: o alvo é ela não
> precisar saber que existe uma coisa chamada Steam Input. O que caducou é a
> leitura de que as nove entregas daquela sprint chegavam lá. Cinco delas foram
> pagas (grau MEDIDO, conferido nesta árvore em 05/08): a frase que mandava ir
> à Steam saiu (`app/actions/daemon_actions.py:435-464`), o rótulo morto do
> `storm_doctor` virou "Aplicar correções" (`integrations/storm_doctor.py:160-168`),
> o tooltip do glade parou de prometer desfazer (`gui/main.glade:2452`), o
> desfazer ganhou porta pela linha de comando (`cli/cmd_steam.py`, registrado em
> `cli/cmd_gamepad.py:34`) e a frase de "o vpad saiu de propósito" ganhou
> consumidor (`daemon/subsystems/gamepad.py:310`, lido em
> `daemon/lifecycle.py:1867` e `daemon/ipc_handlers.py:1445`).
>
> **O que nenhuma delas resolveu é o miolo da pergunta dela**: para *este* jogo,
> ligo ou não? Todas as nove tratavam de **como o produto conta o que fez**.
> Nenhuma trata de **quem decide, com que critério, e o que acontece com a
> decisão dela depois**.

---

## O QUE FOI MEDIDO HOJE

### F1 — A previsão do D-31 se cumpriu, e há testemunha datada

**Grau: MEDIDO**, em 05/08 às 23h, lendo o `localconfig.vdf` da máquina dela e o
journal do usuário. **Só o appid é citado aqui — ele é público; a pasta de
`userdata` e o número da conta não entram em arquivo versionado.**

O appid **1599660** (Sackboy: A Big Adventure) estava com
`UseSteamControllerConfig "2"` — **ligado, por ela**. Hoje está `"0"`.

A troca tem hora e testemunha. O próprio guarda copia o arquivo antes de editar,
e essa cópia sobreviveu:

```
cópia feita pelo guarda   05/08 14:51:59   appid 1599660 -> "2"
arquivo vivo              05/08 14:52:12   appid 1599660 -> "0"

journal (systemd --user), 05/08 14:52:12:
  hefesto-steam-input-guard.service: [steam-input] editado (backup em ...)
  hefesto-steam-input-guard.service: [steam-input] resultado=aplicado
```

Treze segundos entre a cópia e a escrita. **A escolha dela foi zerada às
14:52:12, sem aviso, sem toast, sem uma linha na tela.** O único registro de que
isso aconteceu é uma linha de journal que diz `resultado=aplicado` — a mesma
linha que sai quando o guarda não muda nada de dela.

Os dois appids da allowlist saíram intactos na mesma passagem — `3357650`
(Pragmata) e `2111190` (Mullet Mad Jack) continuam `"2"`. **O guarda funcionou
exatamente como projetado.** O defeito não é ele errar; é ele acertar em
silêncio contra um gesto deliberado dela.

A regra está em `scripts/disable_steam_input.sh:269-272` (per-app zerado, exceto
quem estiver na allowlist lida em `:226`); os globais em `:267-268` morrem
sempre.

### F2 — O guarda está vivo, e o ciclo dele é público no journal

**Grau: MEDIDO**, em 05/08 às 23h00.

```
systemctl --user list-timers hefesto-steam-input-guard.timer
  NEXT  Wed 2026-08-05 23:15:14      LAST  Wed 2026-08-05 22:45:14
  ActiveState=active   UnitFileState=enabled   OnUnitActiveSec=30min
```

Janela de 24 h no journal do usuário, contada por resultado:

```
  24  resultado=adiado-steam-aberta
  23  resultado=aplicado
```

Quarenta e sete execuções em um dia. **Metade delas não fez nada porque a Steam
estava aberta** — o que significa que o guarda espera ela fechar a Steam para
agir, e é por isso que a decisão dela some **depois**, quando ela já esqueceu
que tomou. O estudo registrou 24/24 na janela dele; a diferença é a janela
deslizando, não divergência.

**Detalhe que interessa à E3:** `resultado=aplicado` não distingue *"reapliquei
o global, nada de dela mudou"* de *"apaguei uma escolha que ela tomou hoje"*.
São a mesma string. O D-32 já apontou o irmão desse defeito no pré-voo do
`--apply` (`scripts/disable_steam_input.sh:418` usa `needs_fix` em `:123` quando
existe `needs_real_fix` em `:339`).

### F3 — O único critério legível por jogo do projeto inteiro é um arquivo que ela não pode editar pela janela

**Grau: MEDIDO**, por leitura do arquivo dela e por `grep`.

`grep -rE "suporte nativo|entende DualSense|xinput_only|xbox_only|native_dualsense" src/ assets/`
devolve **zero linhas**. Não existe, em código ou em dado versionado, nenhuma
noção de "este jogo entrega DualSense por conta própria" ou "este jogo precisa
da Steam no meio".

O que existe é o `steam_input_apps.txt` dela, escrito à mão, com comentário em
português explicando **por que** cada appid está lá:

```
# Mullet Mad Jack — SetDualSenseTriggerEffect via Steamworks:
2111190

# Pragmata — suporte nativo a DualSense entregue PELA Steam.
# Registrado em 26/07/2026 depois de medir 4 joysticks para 1 controle:
# a Steam ja tinha UseSteamControllerConfig=2, mas o Hefesto nao sabia
# e mantinha o vpad de pe. Ver DUPLO-REGISTRO-01.
3357650
```

Duas linhas de dado e seis de raciocínio. **É o documento mais útil que este
projeto tem sobre a pergunta dela — e ele não é versionado, não é semeado pelo
`install.sh` (`grep steam_input_apps install.sh` devolve zero), não aparece em
lugar nenhum da janela, e o cabeçalho canônico que o produto sabe escrever
(`integrations/steam_launch_options.py:731-739`) tem as regras do arquivo e
**nenhum critério de jogo**.**

O segundo lugar com esse conhecimento é prosa:
`docs/usage/jogos-e-mascaras.md:61-67`, que lista **Sackboy**, **Pragmata** e
**Mad King Redemption** como "suporte nativo a DualSense". **Sackboy está nessa
lista e é exatamente o jogo cuja escolha o guarda apagou hoje** — ou seja, a
documentação diz que ele não precisaria de Steam Input, ela ligou assim mesmo, e
ninguém sabe qual dos dois está certo, porque **não foi medido em jogo** (é o
M-17 do estudo, que já registra a contradição irmã entre o tooltip do glade e o
preset `assets/profiles_default/sackboy_nativo.json`).

### F4 — Ela pode PÔR pelo botão e não pode TIRAR pelo botão

**Grau: MEDIDO**, por `git grep`.

| Função | Onde | Chamador vivo |
|---|---|---|
| `add_appid_to_steam_input_allowlist` | `integrations/steam_launch_options.py:772` | `app/actions/daemon_actions.py:1182`, dentro de `on_steam_game_broken` (`:1158`) — **um clique** |
| `remove_appid_from_steam_input_allowlist` | `integrations/steam_launch_options.py:828` | `cli/cmd_steam.py:206,215` — **só terminal**. Zero em `app/`, zero em `gui/` |

O caminho de saída existe e é bom (`gamepad steam-input list` mostra o **nome**
do jogo, resolvido do `appmanifest_<appid>.acf` por `cli/cmd_steam.py:82`; o
`remove` aceita nome ou número). Ele só não existe **para quem não abre
terminal**, que é a pessoa para quem o projeto foi escrito.

### F5 — Um comentário de código que envelheceu e agora mente

**Grau: MEDIDO.** `gui/main.glade:2437-2449`, o comentário do bloco do botão
"Este jogo não funciona", afirma duas coisas que eram verdade em 26/07:

- *"integrations/steam_launch_options.py:821"* — a função está hoje em `:828`;
- *"Não há superfície de remoção nenhuma: nem aqui, **nem na linha de
  comando**"* — **falso desde que `cli/cmd_steam.py` entrou**. O `remove` roda
  hoje.

O **tooltip** do mesmo bloco (`:2452`) já foi tornado honesto e continua correto
(*"ainda não existe um botão para desmarcar"* — não existe mesmo, na janela). É
só o comentário que ficou para trás. Conserto de dois minutos, listado como E7
para não se perder.

### F6 — Um ponteiro de tela ainda manda para a aba errada

**Grau: MEDIDO.** `gui/main.glade:2867` (o texto de ajuda das máscaras, na aba
**Emulação** — o rótulo dela está em `:3073`) diz:

> *"...use a exceção por jogo em "Steam Input" na aba Emulação."*

Não existe exceção por jogo na aba Emulação. O que existe ali são
`emulation_steam_input_check_button` (`:2991`, "Verificar") e
`emulation_steam_input_disable_button` (`:2998`, "Desligar Steam Input"). O
opt-in por jogo é o `btn_steam_game_broken` (`:2450`), na aba **Sistema**
(rótulo em `:2554`). A entrega 9 da STEAM-INPUT-01 pagou o gêmeo deste em
`docs/usage/jogos-e-mascaras.md:43`; este ficou.

---

## O QUE ISSO SOMA, DO PONTO DE VISTA DELA

Ela abre o jogo. Não funciona direito. **Não há nada na tela que diga se este
jogo é dos que precisam de Steam Input** — a única lista existe num `.txt` que
ela não vê. Ela então faz a coisa razoável: liga pela janela da Steam, que é
onde a opção mora e onde o mundo inteiro documenta que se faz isso.

Naquele instante funciona. Horas depois — quando ela fechar a Steam e o guarda
finalmente pegar a vez — **o Hefesto desfaz, sem dizer nada**. No dia seguinte o
jogo está diferente de novo e ela não tem como ligar uma coisa à outra.

E se ela usar o caminho do produto ("Este jogo não funciona"), o registro fica
**só do lado do Hefesto**: a Steam continua sem saber. São dois cadastros do
mesmo fato — a DUPLO-REGISTRO-01, aberta desde 26/07 — e **os dois gestos
naturais escrevem em cadastros diferentes**.

---

## E1 — O EXPERIMENTO M-04: a exceção por jogo funciona mesmo?

> **Esta entrega vem ANTES de qualquer linha de código de Steam Input desta
> sprint. É o portão zero da STEAM-INPUT-01, declarado por ela mesma em
> `2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md:244-250`, e
> nunca executado.**

**Grau da pergunta: SEM PROVA.** Ninguém, em nenhuma sessão, verificou.

> **NOTA DATADA — 06/08/2026, 19:56. A E1 FOI EXECUTADA, E O M-04 FECHOU
> POSITIVO.** Nada abaixo é apagado: o protocolo estava certo, o veto estava
> certo, e a pergunta era a pergunta certa. O que caducou é o **grau** e **duas
> frases**.
>
> **O grau.** *"SEM PROVA"* passa a **MEDIDO**: em 06/08/2026, das 19:34 às
> 19:56, com o guarda parado, o global `SteamController_PSSupport "0"` e um
> DualSense físico, o `Microsoft X-Box 360 pad 1` do Steam Input **nasceu só no
> jogo da allowlist** (Mullet Mad Jack, `2111190`) e **não existiu** no jogo fora
> dela (Sackboy, `1599660`). **A Steam honra o per-app com o global desligado.**
> O registro completo está em
> [CONTROLE-SONY-MEDIDO-01](2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md),
> seção *O RESULTADO*.
>
> **Primeira frase que caduca**, no bloco *"Por que isso decide metade da
> sprint"*: *"O que faria os jogos da allowlist funcionarem seria apenas o
> Hefesto sair da frente (ungrab + vpad suspenso)"*. Esse cenário era o do
> **fracasso** do per-app, e o per-app **não fracassou**. E a frase erra também
> na descrição do mecanismo: **"sair da frente" só vale para a ENTRADA.** Durante
> a exceção o Hefesto **mantém a saída inteira** — com o Mullet aberto, os
> gatilhos que ela aplicou seguraram (duros) e o vermelho dela ficou na lightbar,
> com `hidraw abertos pelo daemon: 1`. Não há portão da exceção no caminho de
> saída: os **oito** chamadores de `steam_input_excecao_ativa` estão todos em
> `daemon/subsystems/gamepad.py`, nenhum em `core/` (**MEDIDO** por `grep` nesta
> árvore, 06/08).
>
> **Segunda frase que caduca**, na mesma lista: *"a allowlist não é 'a lista dos
> jogos com Steam Input' — é 'a lista dos jogos em que o Hefesto se cala'"*. O
> Hefesto **não se cala** na allowlist. A leitura certa, medida por contraste
> entre os dois jogos, é a **inversa**: **na** lista o Hefesto perde a entrada e
> **ganha** a saída (os ajustes dela vencem); **fora** dela ganha a entrada e
> **perde** a saída (o jogo escreve no vpad, a réplica chega ao físico, e a
> camada GAME é o topo da precedência declarada em
> `core/backend_pydualsense.py:1253-1259`). **Exceção: no rumble a usuária vence
> nos dois casos** (`gamepad.py:747-748`).
>
> **O terceiro resultado possível — o mais traiçoeiro — está descartado por
> medição:** os recursos de PlayStation **não** dependiam do global. Eles
> obedeceram a ela com o global em `"0"`.
>
> **Consequência para esta sprint:** o portão zero está aberto. **As entregas E2
> a E6 seguem como escritas**, que é exatamente o que a primeira linha da tabela
> *"Como ler cada resultado"* mandava fazer.

### A pergunta, em uma linha

O produto **sempre** zera `SteamController_PSSupport` (o global) e conta com
`UseSteamControllerConfig "2"` (o per-app) para que a Steam continue entregando
o DualSense naquele jogo. **A Steam moderna honra o per-app com o suporte global
de PlayStation desligado?**

O estado atual da máquina dela é exatamente a configuração a testar, e está
**MEDIDO** em 05/08: global `SteamController_PSSupport "0"`, per-app `"2"` em
`2111190` e `3357650`.

### Por que isso decide metade da sprint

- **Se o per-app for honrado:** a arquitetura está certa, e as entregas E2 a E6
  seguem como escritas.
- **Se o per-app for ignorado com o global em `"0"`:** o botão **"Este jogo não
  funciona" nunca funcionou de verdade**. O que faria os jogos da allowlist
  funcionarem seria apenas o Hefesto sair da frente (ungrab + vpad suspenso, em
  `daemon/subsystems/gamepad.py:231` e `:425`), e não a Steam entregar coisa
  alguma. Nesse caso a allowlist não é "a lista dos jogos com Steam Input" —
  é "a lista dos jogos em que o Hefesto se cala", o nome está errado, os textos
  estão errados, e a E5 e a E6 mudam de forma.
- **Terceiro resultado possível, e o mais traiçoeiro:** a Steam honra o per-app
  para **entregar entrada** (os gamepads virtuais nascem) mas **não** os
  recursos de PlayStation (gatilhos adaptativos, lightbar), porque o gate desses
  é o global. Nesse caso a exceção entrega meia coisa, e é justamente a metade
  que ela citou como o que funcionava (*"lightbar, trigger, vibração tudo"*).

### PROTOCOLO — passos que ela pode seguir

Precisa: **um DualSense**, a **Steam**, e **dois jogos** — o `2111190` (Mullet
Mad Jack, na allowlist) e qualquer outro jogo dela que **não** esteja na
allowlist. Duração estimada: 20 minutos.

**Passo 0 — trancar o cenário.** O guarda roda a cada 30 min e reescreve o
arquivo no meio do experimento. Antes de tudo, pausar as duas unidades:

```
systemctl --user stop hefesto-steam-input-guard.timer
systemctl --user stop hefesto-steam-input-guard.path
```

E, **ao terminar o experimento**, devolver — sem isto o produto dela fica sem
rede de segurança:

```
systemctl --user start hefesto-steam-input-guard.path
systemctl --user start hefesto-steam-input-guard.timer
```

**Passo 1 — fotografar o antes.** Com a Steam aberta e o controle ligado, **sem
jogo nenhum aberto**, anotar quais dispositivos existem:

```
grep -E '^N: Name' /proc/bus/input/devices
```

O que importa: quantas linhas dizem `X-Box 360 pad` (são os gamepads virtuais
que o Steam Input cria), quantas dizem `DualSense` e se aparece o
`Hefesto Virtual DualSense`.

**Passo 2 — o jogo da allowlist.** Abrir o **Mullet Mad Jack** (`2111190`).
Esperar chegar ao menu. Rodar o mesmo comando do passo 1, e **dentro do jogo**
observar três coisas, uma de cada vez:

1. o controle **anda** no menu?
2. os **gatilhos** oferecem resistência (o efeito adaptativo) em algum momento?
3. a **lightbar** muda de cor com o jogo?

**Passo 3 — o jogo de controle (fora da allowlist).** Fechar o primeiro, abrir o
segundo jogo. Repetir o passo 2, com as mesmas três perguntas.

**Passo 4 — só se o passo 2 falhar, e só com a Steam FECHADA.** Ligar o global à
mão para isolar a causa: com a Steam encerrada, trocar
`"SteamController_PSSupport"` de `"0"` para `"2"` no `localconfig.vdf`, reabrir a
Steam e repetir o passo 2. **Se com o global ligado funcionar e com ele
desligado não, o global é o gate e o per-app é decorativo.** Ao terminar, é o
`scripts/disable_steam_input.sh --apply` (com a Steam fechada) que devolve o
estado do produto.

### Como ler cada resultado

| Observação no passo 2 (allowlist) vs. passo 3 (fora) | Veredito | Consequência |
|---|---|---|
| Os `X-Box 360 pad` aparecem só no jogo da allowlist, e os gatilhos/lightbar respondem | **Per-app honrado, inteiro.** M-04 fecha positivo | E2..E6 seguem como escritas |
| Os `X-Box 360 pad` aparecem nos dois, iguais | O per-app não está discriminando nada; o que muda é só o Hefesto sair da frente | a allowlist muda de nome e de texto (E5, E6) |
| Não aparecem em nenhum dos dois | **Per-app ignorado com o global em `"0"`.** M-04 fecha negativo | o botão "Este jogo não funciona" nunca entregou o que promete; a sprint muda de forma |
| Aparecem só na allowlist, mas gatilhos/lightbar **mortos** | **Meia entrega.** O gate dos recursos de PS é o global | a exceção precisa ligar o global durante o jogo, ou parar de prometer gatilho |

**A mordida:** esta entrega não tem teste — ela tem **registro**. O produto dela
é uma seção nova aqui, com data, com o que foi observado em cada passo e com o
veredito, no mesmo grau MEDIDO. **Enquanto essa seção não existir, nenhuma outra
entrega desta sprint pode ser dada por fechada**, porque todas assumem que a
exceção per-app faz alguma coisa.

**Veto:** não rodar o passo 4 com a Steam aberta. A regra da casa é **nunca
escrever no `localconfig.vdf` com a Steam viva** — a Steam reescreve o arquivo
inteiro ao sair e come a edição. E não deixar as unidades do guarda paradas ao
fim da sessão: o `systemctl --user start` das duas é parte do protocolo, não
apêndice.

---

## E2 — O gesto natural dela passa a contar (DUPLO-REGISTRO-01, entrega 1)

**Grau do defeito: MEDIDO** (F1 + F3 acima; é o D-34 do estudo).

Ligar o Steam Input pela janela da Steam — **o gesto natural, o que ela fez, e o
que o mundo inteiro documenta** — não escreve nada em
`steam_input_apps.txt`. O Hefesto decide olhando **só** a allowlist
(`scripts/disable_steam_input.sh:226`), então para ele aquele jogo nunca entrou
na exceção. Dois cadastros do mesmo fato, divergindo em silêncio.

**Depende do M-05, e é ele o primeiro passo desta entrega:** é seguro **ler** o
`localconfig.vdf` em runtime com a Steam viva? A casa já tem regra de nunca
**escrever** com a Steam aberta; ler é outra coisa, mas o arquivo é reescrito
pela Steam inteiro e pode ser lido no meio de uma escrita. **Grau hoje: SEM
PROVA.**

**O que fazer, em ordem:**

1. **Responder o M-05.** O piso é honesto e barato: ler o arquivo N vezes ao
   longo de uma sessão de Steam viva (incluindo durante um encerramento da
   Steam) e contar quantas leituras saem com VDF sintaticamente quebrado. Se
   houver **qualquer** leitura quebrada, o consumidor precisa de leitura
   tolerante (falha em ler = "não sei", nunca "está desligado"). **Nunca
   interpretar leitura falha como ausência de opt-in** — seria a mesma classe da
   DROPIN-AMBÍGUO-01.
2. **Comparar os dois cadastros** na subida da janela e a cada varredura do
   guarda.
3. **Quando divergirem, perguntar** (a forma está na E6). O piso escrito na
   DUPLO-REGISTRO-01, entrega 2, continua valendo: nome do jogo, dois botões,
   linha no journal.

**A mordida:** um teste com um `localconfig.vdf` de fixture contendo
`UseSteamControllerConfig "2"` num appid **ausente** da allowlist de fixture. O
comparador tem de acusar a divergência **e nomear o appid**. Arrancado o
comparador, o teste reprova. Segundo caso: leitura de um arquivo truncado no
meio de um bloco tem de devolver "não sei", e **não** "não tem opt-in" — arrancar
o ramo de tolerância reprova.

**Veto:** não transformar isto em **escrita** no `localconfig.vdf`. Esta entrega
lê e pergunta. Escrever na Steam com a Steam viva é o defeito que a casa já
proibiu por escrito.

---

## E3 — O guarda avisa antes de apagar

**Grau do defeito: MEDIDO** (F1: 14:51:59 → 14:52:12, `resultado=aplicado`).

Hoje o guarda zera a escolha dela e **não há como saber que isso aconteceu**:
`resultado=aplicado` é a mesma string para "reapliquei o global" e para "apaguei
o que ela ligou hoje".

**O mínimo honesto, e é mínimo de propósito:** o guarda **continua fazendo o que
faz** — mudar a política dele é decisão de produto e não cabe aqui. O que muda é
que ele passa a **contar o que apagou**:

1. `_transform_vdf` (`scripts/disable_steam_input.sh:231`) passa a registrar
   quais appids ele rebaixou de `"2"`/`"1"` para `"0"` — a informação já está no
   `awk`, no ramo do `else` de `:269-272`; hoje ela é descartada;
2. o `resultado=` ganha um irmão que distingue o caso:
   `resultado=aplicado-zerou-per-app appids=1599660`. **Sem trocar o contrato
   existente** — `_frase_steam_input` (`app/actions/daemon_actions.py:301-321`)
   trata tag desconhecida como "rodou sem confirmação", então uma tag nova não
   quebra a janela velha; a tag antiga continua saindo quando nada de dela mudou;
3. um marcador em `~/.local/state/hefesto-dualsense4unix/` com os appids
   rebaixados e a hora, para a janela poder contar a história **depois** — que é
   quando ela vai abrir a janela, e não às 14:52.

**A mordida:** o arnês de bash já existe e roda o script de verdade
(`tests/unit/test_steam_input_honestidade.py:118-136`). O caso novo: `vdf` de
fixture com um appid **fora** da allowlist em `"2"`, `--apply-quiet` com a Steam
fechada; a saída tem de trazer a tag nova **com o appid**. Arrancado o registro,
o teste reprova. Caso irmão, que é o que impede a tag nova de virar ruído: só
appids **da** allowlist ligados ⇒ a tag antiga, sem o sufixo.

**Bônus de uma linha, do mesmo bloco:** o D-32 continua aberto — o pré-voo em
`scripts/disable_steam_input.sh:418` e `:452` usa `needs_fix` (`:123`), que casa
a allowlist também, quando `needs_real_fix` (`:339`) existe e é exatamente o
predicado certo. Efeito medido: **a Steam dela foi fechada e reaberta para não
mudar nada**, e a janela traduziu o `resultado=aplicado` para *"a Steam não
sequestra mais o seu controle"* (`app/actions/daemon_actions.py:320`).

**Veto:** não fazer o guarda **parar** de zerar por conta desta entrega. Um
guarda que respeita tudo que encontra é um guarda que não guarda nada, e o
motivo pelo qual ele existe (o Steam Input global sequestrando o controle) não
caducou. Quem decide mudar a política é ela, informada — que é a E6.

---

## E4 — A allowlist ganha superfície na janela

**Grau do defeito: MEDIDO** (F4; é o D-34 do estudo).

Ela pode **entrar** na exceção com um clique e **não pode sair** sem terminal.

**O que fazer:**

1. Um botão de desfazer ao lado de "Este jogo não funciona"
   (`gui/main.glade:2450`, aba Sistema), chamando
   `remove_appid_from_steam_input_allowlist` **no mesmo lugar** em que
   `on_steam_game_broken` chama o `add`
   (`app/actions/daemon_actions.py:1182`), **inclusive com o
   `_recarregar_apos_allowlist` depois** (`:1194`, definido em `:1208`) — é ele
   que faz a mudança valer sem reiniciar nada. A própria docstring de
   `integrations/steam_launch_options.py:828` já deixou isso escrito para quem
   viesse ligar.
2. **A lista, com nome de jogo, em vez da contagem.** Hoje a aba Emulação diz
   `Exceção por jogo: N jogo(s)` (`app/actions/emulation_actions.py:1272`) e o
   `storm_doctor` diz `Steam Input LIGADO em N perfil(is)`
   (`integrations/storm_doctor.py:167`) — **e "perfil(is)" ali conta arquivos
   `vdf`, não jogos** (D-33). O resolvedor de nome **já existe e é leitura pura,
   sem rede**: `nome_do_appid` (`cli/cmd_steam.py:82`) lê o
   `appmanifest_<appid>.acf`. Ele precisa sair da lane da CLI para um lugar que
   a janela possa importar sem puxar `typer`.
3. **O tooltip acompanha.** Quando o botão existir, a frase *"ainda não existe um
   botão para desmarcar"* (`gui/main.glade:2452`) sai — e **não antes**.

**A mordida:** três testes. (a) o teste que já guarda a órfã
(`tests/unit/test_steam_input_desfazer.py:202`,
`test_a_remocao_nao_voltou_a_ser_orfa`) passa a exigir chamador em `app/`
também — arrancado o gatilho da janela, reprova; (b)
`tests/unit/test_janela_sem_mentira.py:421`
(`test_tooltip_que_promete_desfazer_tem_de_desfazer`) já é o portão do texto e
tem de continuar verde nos dois estados; (c) a lista com dois appids de fixture
mostra **dois nomes**, e um appid sem manifest mostra `(não instalado)` em vez
de inventar — o critério é o mesmo que `cli/cmd_steam.py` já tomou.

**Veto:** **não apagar comentário dela do `steam_input_apps.txt`.** O `remove`
preserva tudo de propósito (a decisão está escrita na docstring em
`integrations/steam_launch_options.py:828`): o arquivo é dela, tem cabeçalho de
sete linhas e anotações próprias, e adivinhar "o comentário de cima" acerta a
nota nossa e a dela com a mesma facilidade. O preço é uma nota órfã; o preço da
outra escolha é apagar o raciocínio dela.

---

## E5 — O critério por jogo sai da prosa

**Grau do defeito: MEDIDO** (F3: `grep` em zero; D-34).

Hoje o conhecimento *"este jogo entrega DualSense sozinho / pela Steam / só
entende Xbox"* vive em **dois lugares, nenhum deles legível por código**:
`docs/usage/jogos-e-mascaras.md:61-67` (prosa versionada) e os comentários do
`steam_input_apps.txt` dela (não versionado).

**Onde ele deve morar — a proposta, e ela é conservadora de propósito:** um
dado versionado em `assets/`, uma entrada por appid, com **três campos e nada
mais**: como o DualSense chega ao jogo (`direto` | `pela_steam` | `so_xbox`),
**quem mediu e quando**, e a frase de uma linha que a janela mostra. O
`docs/usage/jogos-e-mascaras.md` continua sendo a fonte da verdade em prosa (o
próprio arquivo se declara assim em `:6-10`) e o dado é **derivado dele**, nunca
o contrário — se divergirem, o `.md` ganha.

**E agora a honestidade sobre o custo, que é a parte que não pode faltar:**

- **Uma lista dessas envelhece.** Um patch de jogo, uma atualização da Steam ou
  uma troca de motor mudam a resposta, e ninguém avisa. A `jogos-e-mascaras.md`
  já carrega a cicatriz: o Mullet Mad Jack circulou como exemplo de jogo
  Xbox-only até 25/07, e **era falso** (`:57-59`).
- **Ela tem três jogos medidos.** Uma lista de três linhas não responde *"e o
  jogo que eu comprei ontem?"* — que é a pergunta real. **Uma lista pequena que
  parece completa é pior que lista nenhuma**, porque o silêncio dela vira
  resposta.
- **Por isso o dado precisa saber dizer "não sei".** Appid ausente da lista
  **não** é "funciona direto"; é *"ninguém mediu este jogo aqui"*, e a tela tem
  de dizer isso com essas palavras.

**Alternativa que precisa ser considerada antes de escrever a lista**, e é mais
barata: **não manter lista nenhuma e medir ao vivo**. O sinal já existe e já é
lido — `_steam_input_excecao_status`
(`app/actions/emulation_actions.py:1217`) sabe dizer se o controle físico está
visível agora. *"Neste jogo, agora, o controle está sendo entregue pela Steam"*
é uma frase medida, que nunca envelhece e não precisa de curadoria.
**Recomendação: fazer a E6 com medição ao vivo primeiro, e só criar a lista se
ela provar que a medição sozinha não responde a pergunta dela.**

**A mordida (se a lista for escrita):** um portão que reprove entrada sem quem
mediu e quando — o campo existe justamente para a linha poder caducar com nota
datada, como manda a casa. E um teste de coerência: todo appid que aparece no
dado e na `jogos-e-mascaras.md` tem de dizer a mesma coisa nos dois. Divergiu,
reprova. Arrancado o comparador, reprova.

**Veto:** **não** semear a allowlist dela com appids da lista. A allowlist é a
**intenção declarada por ela**; a lista é **conhecimento sobre o jogo**. Fundir
as duas é reinventar o duplo registro do outro lado.

---

## E6 — A pergunta que ela realmente fez

**Grau do defeito: MEDIDO** — é o relato do topo, e a queixa de 26/07 repetida.

Ela não perguntou como o Steam Input funciona. Ela perguntou **"para ESTE jogo,
ligo ou não?"**. Nenhuma superfície do produto responde isso hoje: a aba
Emulação diz um estado global e uma contagem
(`app/actions/emulation_actions.py:1272`), o `storm_doctor` conta arquivos
(`integrations/storm_doctor.py:167`), e o botão da aba Sistema
(`gui/main.glade:2450`) pede que **ela já saiba** que este é um jogo que não
funciona.

**A forma proposta — um cartão por jogo, no jogo que está aberto agora.** O
appid do jogo em sessão já é conhecido (`_appid_do_jogo_ativo`,
`app/actions/daemon_actions.py:1118`, é o que o botão usa). Com ele, a tela
responde em três linhas, nesta ordem de precedência:

1. **O que está valendo agora, medido.** *"Neste jogo o controle está sendo
   entregue pelo Hefesto"* ou *"...pela Steam"*. Vem de
   `_steam_input_excecao_status` (`app/actions/emulation_actions.py:1217`), que
   já distingue "controle liberado agora" de "só valendo durante o jogo".
2. **O que se sabe deste jogo** — a linha da E5, se ela existir; e **"ninguém
   mediu este jogo aqui"** quando não existir. Nunca silêncio.
3. **A escolha, em duas frases de quem joga, sem a palavra "Steam Input":**
   *"O controle está funcionando neste jogo?"* → [ Está ] [ Não está ]. "Não
   está" é o `add`; e, no jogo já marcado, a pergunta vira *"quer voltar ao
   controle do Hefesto (com cor, gatilhos e co-op)?"*, que é o `remove` da E4.

E o caso que fecha o círculo com a E2 e com o F1: quando o cadastro da Steam e o
do Hefesto divergirem, o cartão **pergunta em vez de repreender** —
> *"Você ligou a entrada Steam em **Sackboy** pela Steam. O Hefesto ainda vai
> desligar isso sozinho. Manter ligado?"* [ Manter ] [ Deixar desligado ]

"Manter" grava na allowlist, e a partir daí o guarda respeita. **É o que
transforma a decisão técnica numa escolha que ela consegue tomar sem saber o que
é Steam Input** — que era, desde o começo, o alvo da STEAM-INPUT-01.

**A mordida:** o cartão montado a partir de um appid de fixture com (a) exceção
ativa, (b) exceção inativa, (c) appid desconhecido da lista da E5, (d)
divergência entre os dois cadastros. Quatro textos distintos, e o (c) **tem de
conter a frase de "ninguém mediu"** — arrancado o ramo do desconhecido, reprova.

**Veto:** **texto de interface é decisão dela.** Nenhuma frase deste cartão
fecha sem foto e sem a palavra dela
([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).
E **não** montar o cartão com jogo fechado prometendo o que só vale em sessão: o
grab e o vpad suspenso são estado de sessão (`daemon/subsystems/gamepad.py:425`).

---

## E7 — Os dois textos que envelheceram

**Grau: MEDIDO** (F5 e F6). Entrega barata, independente, sem risco.

1. **`gui/main.glade:2437-2449`** — o comentário do bloco do botão "Este jogo não
   funciona" diz *"nem na linha de comando"*, e o caminho de CLI **existe hoje**
   (`cli/cmd_steam.py`, registrado em `cli/cmd_gamepad.py:34`); e cita
   `steam_launch_options.py:821`, que hoje é `:828`. O **tooltip** (`:2452`)
   está correto e **não** se mexe. **Não apagar o comentário** — ele registra por
   que o tooltip parou de prometer desfazer, e essa decisão não caducou. Ganha
   nota datada de 05/08 dizendo o que mudou.
2. **`gui/main.glade:2867`** — manda usar a exceção por jogo *"na aba
   Emulação"*. Ela está na aba **Sistema**, no botão "Este jogo não funciona".
   É o gêmeo do ponteiro que a entrega 9 da STEAM-INPUT-01 já corrigiu em
   `docs/usage/jogos-e-mascaras.md:43`.

**A mordida:** `tests/unit/test_steam_input_ponteiros.py` já é o portão desta
classe (rótulo de botão e aba citados em texto têm de existir). O caso novo:
nenhum texto do `main.glade` pode mandar procurar a exceção por jogo numa aba
que não a contém. Devolvido o texto velho, reprova.

---

## ORDEM DE EXECUÇÃO

1. **E1 — o experimento M-04.** Portão de tudo. Precisa dela, do controle e de
   dois jogos; nenhum agente fecha esta sozinho.
2. **E7** — os dois textos. Independente, barata, pode rodar em paralelo com o
   experimento.
3. **E4** — a superfície de remoção na janela. Independente do resultado do M-04
   (tirar da lista é reversão de um gesto dela, valha o per-app o que valer).
4. **E3** — o guarda que conta o que apagou. Independente, e é o que dá material
   para a E6.
5. **E2** — o M-05 primeiro, depois o comparador dos dois cadastros.
6. **E6** — o cartão. Depende da E2 (a divergência), da E4 (os dois botões) e do
   veredito da E1 (o que a tela pode prometer).
7. **E5** — a lista, **e só se a E6 provar que a medição ao vivo não basta**.

Antes de fechar qualquer leva, o bloco do `CLAUDE.md`, **depois** do `git add -A`
(os portões são cegos a arquivo novo).

**Nada de emoji em documento nenhum** — o sanitizer do pre-commit bloqueia
U+2713/U+2717, e o `validar-glifos.py --all` **não** pega isso.

---

## O QUE ESTA SPRINT NÃO COBRE — e é decisão, não esquecimento

- **O terceiro eixo da queixa dela** — *"quando é pra ir colocar os comandos da
  Steam em cada app"* — é a lane das **opções de inicialização**
  (`integrations/steam_launch_options.py`, o botão "Deixar tudo pronto" em
  `gui/main.glade:2425`), e não a do Steam Input. Está na mesma frase dela
  porque na tela dela são o mesmo assunto, mas **misturar as duas nesta sprint
  faria as duas mal**. Fica registrado aqui como pendência nomeada.
- **O `FEAT-STEAM-INPUT-SELF-HEAL-01.md` que as três units instaladas citam na
  linha 2 (`assets/hefesto-steam-input-guard.timer`, `.path`, `.service`)
  continua não existindo.** É a entrega 8 da STEAM-INPUT-01, ainda aberta, e não
  é desta sprint. <!-- ref-externa: a ausência deste arquivo é o achado da frase; as três units instaladas apontam para ele -->
- **Os perfis e as máscaras.** Se a máscara certa para o Sackboy é `xbox` ou
  `dualsense` é o M-17 do estudo, e se resolve em jogo, não em código.
- **Consertar o Sackboy dela.** Um agente **não** deve editar o
  `localconfig.vdf` nem a allowlist dela para "devolver" o `"2"`. Ela ligou
  aquilo por um motivo que ninguém perguntou, e a E6 existe justamente para
  perguntar.

---

## O QUE NÃO FOI MEDIDO

- **Nenhum jogo foi aberto nesta sessão.** Tudo aqui é arquivo, journal e
  código. É exatamente por isso que a E1 existe.
- **Não sei por que ela ligou o Steam Input do Sackboy.** Sei que ligou (o `"2"`
  no backup das 14:51:59), sei que o Hefesto desligou treze segundos depois, e
  sei que a `docs/usage/jogos-e-mascaras.md:66` lista o Sackboy como jogo de
  suporte **nativo** — que em tese não precisaria de Steam Input. **Os dois não
  podem estar certos ao mesmo tempo, e nenhum foi medido em jogo.**
- **Não sei se o `"2"` do Sackboy sobreviveu a algum ciclo anterior do guarda** —
  a cópia de 14:51:59 é a testemunha mais antiga que ainda existe no disco dela
  com esse valor.
- **Não medi se ler o `localconfig.vdf` com a Steam viva é seguro** (M-05). É o
  primeiro passo da E2, e continua **SEM PROVA**.
- **Não vi a tela nesta sessão.** Nenhuma afirmação sobre a janela veio de foto;
  todas vieram do `gui/main.glade` e dos mixins de `app/actions/`.
