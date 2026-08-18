# O que só fecha com o controle na mão dela

Esta é a fila de medições que dependem do hardware, da tela ou da palavra dela — 41 perguntas
em aberto, conferidas contra o **código** de 06/08/2026 (nunca contra o campo `Status:` dos
documentos). Use assim: escolha um bloco da seção 3(a), leia o protocolo inteiro **antes** de
ligar qualquer coisa, execute o Passo 0, meça, e preencha a tabela de leitura — que já vem
escrita, para que nenhum resultado vire interpretação livre depois. O que não estiver na
seção 3(a) não deve ocupar tempo dela hoje.

---

## 1. O método que funcionou em 06/08

Em 06/08/2026 um experimento com o hardware na mão dela fechou o **M-04** (*"o
`UseSteamControllerConfig` por jogo funciona com o global desligado?"*) em **25 minutos**,
depois de a pergunta ficar **11 dias** aberta, desde 26/07. GRAU: MEDIDO (o experimento e o
seu registro).

O que fez aquilo funcionar, e que todo protocolo desta fila copia:

1. **Passo 0 que TRANCA o cenário.** Havia um guarda com timer de 30 min que reescreveria o
   arquivo no meio da medição; sem pará-lo, o resultado não queria dizer nada. E o protocolo
   **inclui religar no fim** — parte dele, não apêndice.
2. **Uma foto do ANTES, numérica.** Sem régua inicial os passos seguintes não têm com o que
   comparar.
3. **Um caso de CONTRASTE.** Sem ele não se conclui nada: o efeito observado pode ter outra
   causa.
4. **Uma PREVISÃO falsificável antes de medir, derivada do código.** Isso transforma
   observação em teste. Naquele dia a previsão acertou duas vezes, e uma vez a medição
   derrubou uma conclusão do assistente — que é exatamente para isso que ela serve.
5. **Divisão de trabalho explícita.** Ela na interface e no controle; o assistente no shell.
6. **O assistente mede NO INSTANTE em que ela avisa.** Uma medição tirada 30 segundos depois
   pegou a transição e não o estado, e teve de ser refeita.
7. **Tabela de leitura do resultado escrita ANTES de medir**, com uma linha por desfecho
   possível, **inclusive os intermediários**.

E um oitavo, que veio de brinde: **grau declarado e separado**. O comportamento observado
virou MEDIDO; a *explicação* do comportamento ficou SUSPEITA COM MECANISMO até ser fechada
por outra medição.

---

## 2. O inventário mudou no meio desta varredura — leia antes da fila

A fila abaixo foi montada contra um inventário levantado às ~20h12 de 06/08, em que **só o
DualSense** estava vivo. Às **20h27 do mesmo dia** eu reli o hardware e o quadro é outro.

**MEDIDO agora** (`hefesto-dualsense4unix controller list --external --json`,
`/proc/bus/input/devices`, `/sys/class/hidraw/*/device/uevent`, `lsmod`):

| aparelho | transporte | como o Hefesto o vê | número exibido |
|---|---|---|---|
| DualSense | Bluetooth | primário, bateria 95%, giroscópio vivo, lightbar por `sysfs` | 1 |
| **Pro Controller genuíno** (OUI `e0:f6:b5`) | **Bluetooth, CONECTADO** | externo, `057e:2009`, driver `nintendo` | 2 |
| **8BitDo em modo PS4** (OUI `e4:17:d8`) | **Bluetooth, CONECTADO** | externo, `054c:05c4`, driver `playstation` | 3 |
| vpad do Hefesto (P1) | uhid | saída do co-op | — |

Ausentes: o **segundo DualSense** (rank 1 do registro, sem bond no adaptador) e o **8BitDo em
modo Switch** (rank 4 do registro, sem bond). GRAU: MEDIDO.

Consequências imediatas, e elas reordenam a fila:

- **Três controles físicos estão no rádio agora.** Cenários que a varredura marcou como "ela
  precisa ligar o aparelho" já estão de pé — em especial o contraste
  `QUATRO-NO-RÁDIO-01`/d2+d3 (item A-6 abaixo), que pede exatamente esta mesa.
- **Os módulos `hid_nintendo` e `hid_playstation` estão carregados**, com `ff_memless` preso
  aos dois. GRAU: MEDIDO. A previsão de autocarga do DKMS se confirmou.
- **A suíte de testes NÃO está rodando neste instante** (GRAU: MEDIDO). Era o principal
  bloqueio de Passo 0 do inventário anterior. Ela volta a bloquear assim que alguém a
  disparar — reconferir sempre.
- **Uma premissa da fila caiu na hora.** Ver a seção 6, item *"a IMU do Pro por Bluetooth"*.

---

## 3. A fila, por valor e depois por custo

Total: **41 medições pendentes**. Pela leitura do inventário das 20h27, **32 dão para fazer
agora** (a), **6 esperam ela ligar/religar um aparelho que ela tem** (b) e **3 dependem de
aparelho que ela talvez não tenha** (c).

Convenção dos protocolos: **P0** = passo que tranca o cenário (com o destrancar embutido);
**ANTES** = foto numérica; **CONTRASTE** = o caso sem o qual nada se conclui; **PREVISÃO** =
falsificável, derivada do código; **ELA** / **ASSISTENTE** = divisão de trabalho;
**LEITURA** = tabela escrita antes de medir.

Regra de instrumento que vale para a fila inteira, e nasceu de defeito real: **amostrar
`daemon.state_full`, nunca `/sys/class/leds`** — o `state_full` publica por controle
`player_slot`, `lightbar_rgb`, `lightbar_source`, `inputs`, sensores e áudio
(`daemon/ipc_handlers.py:2139` e `:2141`). GRAU: MEDIDO.

Segunda regra, que já custou uma medição inteira: **`journalctl` sempre com data completa**.
`--since "23:20"` sem data devolve zero em todas as janelas, e zero em todas é sinal de
instrumento quebrado, não de ausência de defeito. GRAU: MEDIDO.

---

### (a) DÁ PARA MEDIR AGORA, com o que está na mesa

---

#### A-1. `RADIO-ABERTO-01`/E1-bis+E2 — o furo de segurança que continua no disco dela

**Pergunta.** Com `JustWorksRepairing=confirm` no disco e o agente de pareamento vivo, um
re-pareamento legítimo dela ainda completa?

**Por que é a primeira.** É o **único item da fila inteira cujo pior caso não é "um controle
que não funciona"**. Custo: 20 min.

**O estado, conferido agora.** `/etc/bluetooth/main.conf` linha 25 diz
`JustWorksRepairing=always`, dentro do bloco `# >>> hefesto bluetooth >>>` escrito por versão
anterior deste projeto. `hefesto-bt-agent.service` está `active`. A cura existe na árvore e
**nunca tocou o disco**: `scripts/bluez_config.sh` (60 KB, com `aplicar`/`remover`/
`verificar`/`podar`), já chamado por `install.sh` e `uninstall.sh`, e `scripts/doctor.sh:1732`
(`check_bluez_justworks_repairing`) já reprova com `always`. GRAU: MEDIDO (leitura direta do
arquivo e do `systemctl`, 06/08).

**P0 — trancar.** Parar o `hefesto-bt-health-watchdog` (o `.timer` está `active` agora — GRAU:
MEDIDO): ele mexe em trust/bond durante a janela e reescreveria o cenário no meio da medição.
**Destrancar no fim**: religar o timer, e conferir que voltou a `active`. Isto é passo do
protocolo, não apêndice.

**ANTES.** `grep JustWorksRepairing /etc/bluetooth/main.conf`; `systemctl is-active
hefesto-bt-agent.service`; e a lista de bonds lida pelo D-Bus, **não** pelo `bluetoothctl` —
ver a nota de instrumento no fim deste bloco.

**CONTRASTE.** Re-parear **um** controle **antes** da troca (com `always`) e o **mesmo**
controle depois (com `confirm`). Sem o "antes", um fracasso depois não distingue "o `confirm`
quebrou" de "este controle já não pareava".

**PREVISÃO, derivada do código.** Com `confirm` no disco e o agente `active`, o pareamento de
um controle já bondado **completa**. Se falhar, a E2 (agente próprio que autoriza por
política) deixa de ser "a que fecha o cenário" e vira **bloqueante de uso** — e a decisão
muda de "seguir" para "reverter para `always` até a E2 existir".

**ELA.** Segura o botão de pareamento e diz o que a interface do sistema mostrou.
**ASSISTENTE.** Roda `sudo bash scripts/bluez_config.sh aplicar`, confere o `main.conf`, e lê
o journal do agente no instante do aviso dela.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| `confirm` no disco e o re-pareamento completa | a cura é segura | E1-bis FECHA; E2 vira melhoria, não bloqueio |
| `confirm` no disco e o re-pareamento falha **com o agente `active`** | o agente não autoriza este caso | E2 vira **bloqueante**; reverter para `always` e registrar o motivo datado |
| `confirm` no disco e o re-pareamento falha **com o agente caído** | é fragilidade do agente, não da política | a `CURA-QUE-FERE-01` sobe de prioridade; já caiu duas vezes em 04/08 |
| o `aplicar` não muda o disco | o dono único do bloco não está funcionando | defeito de instalação — para tudo e conserta o script antes |
| o pareamento nem começa (rádio mudo) | instrumento quebrado | refazer; nada acima vale |

**Nota de instrumento, e ela derruba passo de protocolo.** `bluetoothctl` está **MUDO nesta
máquina**: `show`, `list`, `devices`, `devices Paired` e `devices Bonded` devolvem string
vazia com saída 0, enquanto o `bluetoothd` está ativo e o D-Bus responde tudo. GRAU: MEDIDO
para o sintoma; SEM PROVA para a causa. **Nenhum passo pode depender do `bluetoothctl` para
ler estado** — use `busctl --system call org.bluez / org.freedesktop.DBus.ObjectManager
GetManagedObjects`. E `scripts/bt_bonds_restore.sh` shell-a o `bluetoothctl`: testar antes de
usá-lo como instrumento.

---

#### A-2. `PERFIL-JOGO-01`/E1 — qual dos quatro sintomas ela chama de "o perfil muda"

**Pergunta.** Quando ela diz "o perfil muda ao abrir o jogo", o que muda: o **nome do
perfil**, o **número do controle**, a **cor**, ou os **gatilhos**?

**Por que é a segunda.** É a **entrega zero declarada** da sprint: *"nada deve ser corrigido
antes dele"*. As E3 e E4 dependem do resultado, e a **E4 precisa ser reescrita** antes de
virar código. Sem isto, qualquer cura é chute. GRAU: SEM PROVA (a pergunta nunca foi feita
separada). Custo: 25 min.

**P0 — trancar.** Congelar o autoswitch (`autoswitch.lock`) **não** serve aqui: é justamente o
comportamento sob teste. O que tranca é o oposto — garantir que **nenhuma troca manual** de
perfil aconteça durante a janela, e anotar qual perfil está ativo no início. **Destrancar:**
nada a religar; só registrar o perfil final.

**ANTES.** `daemon.state_full` completo com o jogo **fechado**, guardando por controle:
`uniq`, `player_slot`, `lightbar_rgb`, `lightbar_source`, `player_leds`, e o nome do perfil
ativo, mais os gatilhos aplicados.

**CONTRASTE.** As mesmas quatro perguntas em **três** momentos: (1) antes de abrir o jogo, (2)
depois de abrir, (3) **depois de dois alt-tabs**. O passo do alt-tab é o que separa o defeito
2 de todos os outros — sem ele, os quatro sintomas continuam colados.

**PREVISÃO, derivada do código.** Se o sintoma for a **cor**, o journal traz troca de perfil
por `game_signal`; se for o **número**, não traz troca de perfil nenhuma e o que mudou foi a
numeração do co-op; se forem os **gatilhos**, houve `apply_output_defaults` sem troca de
perfil. Os três deixam rastro diferente — e se os três rastros estiverem ausentes, a queixa é
de outra camada.

**ELA.** Responde **quatro perguntas separadas**, uma por sintoma, em cada um dos três
momentos. Não perguntar "o perfil mudou?" — perguntar "o **nome** que aparece na janela é o
mesmo?", "o **número** do controle é o mesmo?", "a **cor** é a mesma?", "os **gatilhos**
estão iguais?".
**ASSISTENTE.** Tira `state_full` **no instante** de cada aviso e cola o journal da janela.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| só o **nome** muda | é troca de perfil de verdade | as E3/E4 miram o autoswitch |
| só o **número** muda | é numeração do co-op, não perfil | o alvo é `QUATRO-NA-MESA-01`/defeito 2 |
| só a **cor** muda | é a camada de lightbar | o alvo é a autoridade do jogo (`SINAL-DE-JOGO-01`) |
| só os **gatilhos** mudam | é `apply_output_defaults` | o alvo é a trava por categoria |
| **mais de um** muda | são defeitos distintos somados | E4 reescrita para tratar um por vez, e a ordem passa a importar |
| **nada** muda com o jogo aberto, e muda só depois dos alt-tabs | o gatilho é a troca de janela | fecha o defeito 2 e mata os outros três |
| nada muda em momento nenhum | a queixa é de outra sessão/versão | pedir a ela um caso reprodutível antes de gastar mais tempo |

---

#### A-3. `PARIDADE-SONY-01`/E1 — o carimbo de áudio muda quando ela abre um JOGO?

**Pergunta.** O carimbo `audio_do_jogo` muda dentro de um jogo, ou continua a assinatura do
kernel (alto-falante 100, rota `0x30`)?

**Estado.** O carimbo é MEDIDO e reproduzível; a **autoria dentro do jogo** é SEM PROVA — a
medição anterior foi feita com a Steam fechada e nenhum jogo aberto. Custo: 15 min.

**P0 — trancar.** Nenhum guarda a parar; o que tranca é **não mexer no volume nem na rota**
durante a janela, e conferir que a suíte de testes não está rodando (ela derruba a chamada
IPC: durante a suíte o `controller list` devolveu `daemon recusou chamada: conexão timeout` na
primeira tentativa — GRAU: MEDIDO). **Destrancar:** nada.

**ANTES.** Três leituras de `daemon.state_full`, guardando `audio_do_jogo` e `visto_ha_s`:
(1) daemon de pé **sem** Steam; (2) Steam aberta **sem** jogo; (3) **dentro** do jogo.

**CONTRASTE.** A leitura (1) é o controle negativo. Se ela já divergir da assinatura conhecida
sem nada aberto, o instrumento mudou e o resto não vale.

**PREVISÃO, derivada do código.** Se a amostra dentro do jogo continuar `alto-falante 100` e
`rota 0x30`, a autoria é do kernel e a sprint fecha como CICATRIZ. Se mudar, a E2 começa com
a prova na mão **e já sabendo qual campo replicar** — que é a única coisa que hoje impede a
E2 de começar.

**ELA.** Abre o jogo e **avisa no instante**.
**ASSISTENTE.** Lê `daemon.state_full` no instante do aviso. Leitura tardia pega a transição,
não o estado.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| dentro do jogo o carimbo muda de valor | o jogo escreve mesmo | E2 começa, com o campo identificado |
| continua `100` / `0x30` nos três momentos | a autoria é do kernel | sprint fecha como CICATRIZ, sem código |
| muda na Steam **sem** jogo e não muda mais dentro | quem escreve é a Steam, não o jogo | alvo muda: é camada Steam, não jogo |
| `visto_ha_s` cresce sem parar (carimbo velho) | ninguém escreve nada | instrumento ou caminho de áudio fora do ar — refazer |

---

#### A-4. `SINAL-DE-JOGO-01`/E1 (o M-09) — a autoridade cai com o jogo comprovadamente VIVO?

**Pergunta.** A autoridade do jogo cai depois dos 30 s de histerese **mesmo com o jogo vivo**?

**Estado.** Mecanismo MEDIDO: `daemon/subsystems/game_signal.py:62` (`HYSTERESIS_SEC = 30.0`)
e a queda em `:179`, que loga `evidencia="daemon_histerese_expirada"`. As **seis transições
apresentadas como prova foram DERRUBADAS** pelo verificador. Custo: 20 min.

**P0 — trancar.** A telemetria da E2 **não foi entregue**: no journal, *"o detector cegou"* e
*"o jogo fechou"* saem **byte a byte iguais** (GRAU: MEDIDO — a linha `:179` é a única, e não
distingue os dois). Por isso o P0 é montar o instrumento que falta: **`ps -o etimes` do
processo do jogo, amostrado em laço e colado ao lado de cada carimbo**. **Sem isso a medição
não vale** — foi exatamente essa omissão que invalidou as seis anteriores. **Destrancar:**
matar o laço de amostragem no fim.

**ANTES.** PID do jogo, `etimes` inicial, e o estado de autoridade no `state_full`.

**CONTRASTE.** Repetir com o jogo **fechado de verdade**. As duas séries têm de produzir o
mesmo carimbo no journal — é isso que prova que o journal, sozinho, não distingue os casos.

**PREVISÃO, derivada do código.** Com o jogo vivo (`etimes` crescendo) e 90 s sem tocar em
nada numa janela Wayland nativa, a autoridade **cai** aos ~30 s e o journal traz
`daemon_histerese_expirada` — enquanto o `etimes` prova que o jogo nunca morreu. **Se a
autoridade não cair com o jogo vivo, a leitura está errada e o M-09 cai.**

**ELA.** Abre o jogo, faz alt-tab para uma janela Wayland nativa, **fica 90 s sem tocar em
nada**, volta e avisa.
**ASSISTENTE.** Mantém o laço de `etimes` + `state_full` e crava o segundo da queda.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| autoridade cai aos ~30 s com `etimes` crescendo | M-09 **CONFIRMADO** | E2 e E3 destravam |
| autoridade **não** cai em 90 s | M-09 **REFUTADO** | a histerese não é o mecanismo; reabrir a hipótese |
| cai, mas só depois de bem mais de 30 s | há um segundo relógio no caminho | achado novo — medir o segundo relógio antes de curar |
| cai e volta sozinha antes dos 90 s | o detector piscou | é cegueira do detector, não expiração — muda o endereço da cura |
| o jogo morre no meio (`etimes` some) | rodada inválida | refazer; é o erro que invalidou as seis anteriores |

---

#### A-5. `SOM-ROTA-01`/E2 — a faixa útil do volume deixa de ser 64 passos?

**Pergunta.** Com o pré-amp e a rota escritos, a faixa útil do volume deixa de ser 64 passos?

**Estado.** A régua atual — **mudo até 38**, **satura em 102** — está no código
(`core/speaker_scale.py:58` e `:61`) e foi medida **só com o volume**, sem pré-amp e sem rota.
A faixa nova é SEM PROVA. Custo: 25 min. Exige o **ouvido dela**, sala silenciosa e a tela
desligada.

**P0 — trancar.** **Conferir a porta de captura antes de medir.** Em 02/08 o instrumento
automático falhou e quase deu veredito falso: o `parec` leu zero bytes porque a fonte do
controle estava em `iec958-stereo`, sem porta de captura. Confirmar a porta, e só então
medir. **Destrancar:** devolver a rota e o volume ao valor inicial no fim.

**ANTES.** A régua numérica atual: o valor do registrador em que ela deixa de ouvir e o valor
em que ela para de perceber diferença — os dois medidos **antes** de escrever pré-amp e rota.

**CONTRASTE.** A mesma varredura **sem** pré-amp e **sem** rota, na mesma sessão e na mesma
sala. Sem essa segunda série a comparação com os números de 02/08 mistura sala, hora e ouvido.

**PREVISÃO, derivada do código.** A faixa útil (`_SPEAKER_REG_SATURA_EM -
_SPEAKER_REG_MUDO_ATE` = 64 passos) **cresce**. **Se não mudar, a hipótese cai e a E1 precisa
ser remedida antes de qualquer código.**

**ELA.** Ouve e diz onde começa e onde para de crescer. É o instrumento.
**ASSISTENTE.** Escreve os registradores e anota os valores no instante de cada fala dela.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| a faixa cresce (mudo cai abaixo de 38 e/ou satura acima de 102) | hipótese **confirmada** | reescrever a régua e devolver curso ao controle deslizante |
| a faixa é a mesma, 64 passos | hipótese **cai** | remedir a E1 antes de tocar em código |
| a faixa **encolhe** | o pré-amp está atrapalhando | achado novo — o pré-amp vira suspeito, não cura |
| ela não ouve nada em faixa nenhuma | porta de captura/rota erradas | P0 falhou; descartar a rodada |

---

#### A-6. `QUATRO-NO-RÁDIO-01`/d2+d3 — o 8BitDo em PS4 e o Pro em Switch caem JUNTOS?

**Pergunta.** O 8BitDo em modo PS4 e o Pro Controller em modo Switch sobrevivem por Bluetooth
a uma sessão com os outros no ar, ou caem juntos?

**Por que subiu de posição.** A ficha marcava este item como "precisa de aparelho não ligado".
**Ele está de pé agora**: os dois estão conectados por Bluetooth junto com o DualSense (GRAU:
MEDIDO, 20h27). Custo: 25 min, e o cenário já está montado.

**É o contraste barato da tempestade.** Se os dois caírem **juntos**, a causa é do **rádio**;
se cair só um, a causa é do **modo**. Nenhuma outra medição desta fila separa essas duas
hipóteses tão barato.

**P0 — trancar.** (1) Conferir que a **suíte de testes não está rodando** — durante ela o IPC
chega a recusar chamada por timeout (GRAU: MEDIDO). (2) Declarar o `storm_watch.sh` no
protocolo: três processos de pé agora, lendo contadores de erro do adaptador a cada
`HEFESTO_KERNELWATCH_BT_INTERVAL` (padrão 300 s). Ele é **só leitura** — não é guarda a parar,
mas gera log periódico que **vira ruído** se não for declarado. **Destrancar:** nada a religar;
só registrar que o `storm_watch` estava de pé.

**ANTES.** `hefesto-dualsense4unix controller list --external --json` completo, com o
`player_slot` de cada um, mais o instante inicial em relógio de parede.

**CONTRASTE.** O **DualSense** é o controle positivo: ele tem de sobreviver à mesma janela. Se
o DualSense cair junto, não há informação sobre modo nenhum — é queda de rádio geral.

**PREVISÃO, derivada do código e do acervo.** A tabela da casa marca o **Pro em modo Switch**
como PROVADO instável por BT; o **8BitDo em PS4** é SEM PROVA. Previsão: o Pro cai primeiro e
o 8BitDo sobrevive. **Se caírem no mesmo minuto, a previsão está errada e a causa é o rádio.**

**ELA.** Só avisa quando um controle parar de responder — e **qual**. Não precisa fazer mais
nada; a sessão é de uso normal.
**ASSISTENTE.** Amostra `controller list --external --json` em laço (intervalo fixo) e crava o
instante de cada desaparecimento; e lê o journal com **data completa**.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| os dois caem no mesmo minuto | a causa é o **rádio** | o modo deixa de ser suspeito; alvo vira contenção/topologia |
| só o Pro (Switch) cai | a causa é o **modo Switch** | confirma a tabela; documentar e recomendar PS4 |
| só o 8BitDo (PS4) cai | previsão **derrubada** | o modo PS4 vira suspeito; a recomendação da casa muda |
| nenhum cai em toda a sessão | não se reproduz nesta mesa | registrar a duração; sem isso o "instável" fica sem régua |
| o **DualSense** cai junto | contraste falhou | queda geral de rádio — descartar a rodada |

**Combo, e ele já enganou protocolo.** O modo PS4/DirectInput do 8BitDo é **`Start + A`**
(MEDIDO com ela, 03/08, em `docs/usage/troubleshooting-8bitdo.md`). `X+Start` é o **X-input**
e `Y+Start` é o **Switch**. Vários documentos do acervo mandam para o modo errado no passo 1 —
não copiar linha de combo de sprint velha.

---

#### A-7. `BT-FURO-FINO-01`/defeito 1 — o giroscópio anda com o controle parado?

**Pergunta.** O leitor de movimento aceita pacote de **áudio** como input?

**Estado.** MEDIDO no código: `core/physical_report_reader.py:236-244` testa **id**, **tamanho**
e **CRC** — e **não** testa o bit de áudio do relatório. O efeito é SUSPEITA COM MECANISMO.
Custo: 15 min.

**AVISO A ELA, ANTES DE COMEÇAR.** Se confirmar, **o controle fica inutilizável enquanto a
ponte de microfone estiver no ar**. Este aviso é parte do protocolo, não cortesia.

**P0 — trancar.** Subir a ponte de microfone de propósito (`HEFESTO_DUALSENSE4UNIX_BT_MIC`),
com o controle **parado na mesa**, e confirmar que a ponte realmente subiu antes de olhar o
`evtest`. **Destrancar:** derrubar a ponte no fim e conferir que o giroscópio voltou ao
normal.

**ANTES.** `evtest` no nó de movimento do DualSense com a ponte **desligada**, controle parado:
a régua de ruído. Sem ela, "andou" não tem número.

**CONTRASTE.** A mesma janela com a ponte desligada é o controle negativo. E o controle
positivo é mover o controle de propósito: se o `evtest` não registrar nem isso, o instrumento
está errado.

**PREVISÃO, derivada do código.** O pacote de áudio tem o **mesmo** id `0x31`, os **mesmos**
78 bytes e CRC **válido** — logo a extração da janela de movimento **vai** devolver bytes de
Opus como giroscópio. **Se o `evtest` não mostrar eventos**, ou a ponte não subiu, ou o kernel
filtra antes — e nesse caso **o endereço da cura muda para o DKMS, não o nosso leitor**.

**ELA.** Confirma que **não está tocando no controle**. Só isso.
**ASSISTENTE.** Roda o `evtest`, conta eventos por segundo nas duas fases e compara com a
régua de ruído.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| eventos muito acima do ruído com a ponte ligada, controle parado | defeito **CONFIRMADO** | a cura é nossa: testar o bit de áudio antes de extrair movimento |
| eventos iguais ao ruído nas duas fases | nosso leitor **não** é o culpado | a cura vira do DKMS/kernel; fechar o defeito 1 como não reproduzido aqui |
| eventos só quando o mic **está captando** som | é conteúdo de áudio virando eixo | confirma o mecanismo com detalhe extra — a cura é a mesma |
| a ponte não sobe | P0 falhou | refazer; nada acima vale |
| nem o movimento de propósito aparece | instrumento errado | descartar a rodada |

---

#### A-8. `CHECKLIST`/§1 (o M-06) — um controle físico vira UM dispositivo dentro do jogo?

**Pergunta.** Um controle físico vira **um** dispositivo de jogo dentro do jogo, ou o input
duplicado voltou?

**Estado.** O remendo de 26/07 **nunca foi confirmado ao vivo**. GRAU: SEM PROVA. Custo:
10 min — e **vale rodar na mesma sessão** de qualquer outro item com jogo aberto, porque olha
a mesma tela de configuração de controle.

**P0 — trancar.** Anotar quantos controles físicos estão no rádio (hoje: **três**) antes de
abrir o jogo. Com três físicos e o co-op ligado, a contagem esperada muda — e é aí que o
defeito, se existir, aparece. **Destrancar:** nada.

**ANTES.** `cat /proc/bus/input/devices` com o jogo **fechado**, contando nós `js*` e
`event*` de gamepad; mais `daemon.state_full` para saber quantos o Hefesto acha que existem.

**CONTRASTE.** A mesma contagem **dentro** do jogo. E, como segundo contraste, a mesma
contagem com **um só** controle no rádio: se o duplicado só aparece com três, é problema de
co-op, não do remendo.

**PREVISÃO, derivada do código.** O `SDL_GAMECONTROLLER_IGNORE_DEVICES` é
`_IGNORE_VALUE = "0x054c/0x0ce6"` — **um par cravado** (`daemon/launch_env.py:83`, GRAU:
MEDIDO). O DualSense físico casa; o **Pro** (`057e:2009`) e o **8BitDo em PS4** (`054c:05c4`)
**não casam**. Previsão: o DualSense aparece uma vez só; **os dois externos podem aparecer
duplicados** (físico + vpad do co-op). Se os externos aparecerem uma vez só, a previsão está
errada e há um caminho de supressão não lido.

**ELA.** Abre a tela de configuração de controle do jogo e diz **quantos** controles ele lista
e com que nome.
**ASSISTENTE.** Fotografa `/proc/bus/input/devices` nos dois momentos e conta.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| um físico = um dispositivo, para todos | M-06 **CONFIRMADO** ao vivo | marca a caixa §1 do checklist |
| o DualSense aparece uma vez e os externos, duas | o `IGNORE` de um par só é o buraco | achado com dono: `MÁSCARA-01`, e a lista tem de virar lista |
| o DualSense também duplica | o remendo de 26/07 **não** pega | reabrir o M-06 como defeito vivo |
| o jogo lista **menos** controles que o esperado | é grab/exclusividade, não duplicação | alvo vira `evdev_grab_failed` |
| a contagem muda entre dois alt-tabs | há corrida na adoção | achado novo — medir antes de curar |

---

#### A-9. M-07 — a tela diz que aplicou a máscara enquanto o gate recusa?

**Pergunta.** Com jogo aberto, a janela informa que aplicou a máscara enquanto o gate a recusa?

**Estado.** MEDIDO no código: em `daemon/subsystems/gamepad.py`, o ramo bloqueado por jogo
devolve `True` com o comentário escrito — *"True porque a emulação SEGUE ativa (com a máscara
anterior) — o contrato de retorno é 'ativo ao final', não 'aplicou o pedido'"* (linhas 1425 a
1432). O que a **tela** informa é SEM PROVA. Custo: 5 min, e **cabe dentro de qualquer outra
sessão de jogo** desta fila.

**P0 — trancar.** Nenhum guarda; só garantir que a máscara de partida é **diferente** da que
ela vai pedir, senão o teste não distingue nada. **Destrancar:** devolver a máscara original.

**ANTES.** A máscara ativa, lida do `state_full`, com o jogo já aberto.

**CONTRASTE.** A mesma troca de máscara com o jogo **fechado** — aí ela tem de aplicar de
verdade. Sem esse positivo, um "aplicou" falso não se distingue de um "aplicou" verdadeiro.

**PREVISÃO, derivada do código.** Com jogo aberto e vpad vivo, o retorno do IPC é `True`, a
máscara **não** muda, e a janela informa sucesso. **Se a janela informar recusa, o relatório
já distingue os casos e o M-07 cai.**

**ELA.** Troca a máscara pela janela e **lê em voz alta** o que a tela disse.
**ASSISTENTE.** Lê o retorno do IPC e a máscara efetiva **no mesmo instante**.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| tela diz sucesso, máscara não mudou | M-07 **CONFIRMADO** | o contrato de retorno precisa de um terceiro estado |
| tela diz recusa, máscara não mudou | M-07 **REFUTADO** | a janela já é honesta; fechar sem código |
| a máscara **mudou** com jogo aberto | o gate não pegou | achado novo e mais grave: o jogo perde o controle na mão dela |
| com jogo fechado também não aplica | contraste falhou | é defeito de aplicação, não de relato — outro alvo |

---

#### A-10. `MODO-01` / `CHECKLIST`/§3 — o modo jogo com o cadeado de perfil ligado

**Pergunta.** Um jogo que casa `coop_local` **por título** liga o modo jogo com o **cadeado de
perfil ligado** — e, ao fechar o jogo, o controle segue funcionando no desktop?

**Estado.** MEDIDO em parte (três jogos **sem** perfil próprio, 25/07). O caso **com o
cadeado** é SEM PROVA. Custo: 15 min.

**P0 — trancar.** Ligar o cadeado do autoswitch de propósito (`autoswitch.lock`) e **confirmar
que ligou** pelo `state_full` — é a condição sob teste, e não adianta supor. **Destrancar:**
soltar o cadeado no fim, e conferir que soltou. Passo do protocolo.

**ANTES.** Perfil ativo, estado do cadeado e estado do modo jogo, com o jogo fechado.

**CONTRASTE.** O mesmo jogo com o cadeado **desligado** — é o caso já medido em 25/07, e serve
de positivo.

**PREVISÃO, derivada do código.** Com o cadeado ligado, o modo jogo **liga assim mesmo** (o
cadeado é da troca de perfil, não do modo), e ao fechar o jogo o controle **segue funcionando
no desktop** — é o caso que a trava `ligou_gamepad` protege. **Se o controle morrer no desktop
ao fechar o jogo, a trava não cobre este caminho.**

**ELA.** Abre um dos jogos do casamento por título (Sackboy, Overcooked, It Takes Two ou
Cuphead), joga um minuto, fecha, e **tenta usar o controle no desktop**.
**ASSISTENTE.** Amostra o journal procurando `profile_mode_aplicado` e a origem, e o
`state_full` antes e depois de fechar.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| modo liga com cadeado, controle vivo no desktop depois | caso **fechado** | marca §3 do checklist |
| modo **não** liga com o cadeado | o cadeado alcança o modo | achado: separar cadeado de perfil e de modo |
| modo liga, mas o controle morre no desktop | a trava `ligou_gamepad` não cobre | defeito com dono, e é o que mais dói |
| o jogo nem casa por título | o casamento é por outro critério | remedir o casamento antes de tudo |

---

#### A-11. `SENSOR-VIVO-01`/E4 — o clique do touchpad dentro do jogo

**Pergunta.** Num jogo que usa o touchpad como botão, o clique **abre a coisa** — e o cursor
do mouse **não** anda enquanto ela desliza o dedo?

**Estado.** O código entrou e está MEDIDO: `core/physical_report_reader.py:265`
(`extract_touchpad_click`), o encaminhamento em `:618` e `:621`, e o contador já exposto pelo
IPC. O **efeito no jogo** é SEM PROVA. Custo: 10 min.

**P0 — trancar.** Confirmar que a emulação de mouse pelo touchpad está no estado que ela usa
normalmente — se estiver desligada, a segunda pergunta não mede nada. **Destrancar:** devolver
ao estado inicial.

**ANTES.** O contador de cliques encaminhados, lido pelo IPC, com o jogo fechado.

**CONTRASTE.** O mesmo gesto **fora** do jogo: o clique tem de contar e o cursor tem de andar
(ou não), conforme a configuração. É o positivo do instrumento.

**PREVISÃO, derivada do código.** Dentro do jogo, "com dedo" **maior que zero** e "com clique"
**maior que zero** — antes da cura o segundo era zero. **Se "com clique" ficar em zero, a cura
não chegou ao jogo.**

**ELA.** Aperta o touchpad dentro do jogo e diz se abriu; e desliza o dedo e diz se o cursor
andou por cima do jogo.
**ASSISTENTE.** Lê os dois contadores no instante.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| abre e o cursor não anda | E4 **ACEITA** | fecha a sprint (o segundo aceite, do jogador 2, fica para quando houver dois DualSense) |
| abre e o cursor **anda** | metade paga | achado: a supressão do cursor não cobre a janela do jogo |
| não abre, mas o contador sobe | o clique sai e o jogo ignora | é mapeamento do jogo, não nosso — registrar e fechar |
| não abre e o contador fica em zero | a cura não chega ao jogo | reabrir a E4 como não entregue de fato |

---

#### A-12. M-17 — qual máscara entrega tudo no Sackboy

**Pergunta.** Qual máscara entrega vibração, giroscópio e lightbar no Sackboy: a de DualSense
ou a de Xbox?

**Estado.** MEDIDO que a **contradição existe**: o tooltip da janela
(`gui/main.glade`, linha 2845) diz que o Sackboy *"funciona completo com DualSense (PS)"*,
enquanto `assets/profiles_default/sackboy_nativo.json` grava `"gamepad_flavor": "xbox"` (linha
43), e `profiles/loader.py:191` guarda o marcador da migração `dualsense` para `xbox`. Qual
lado está certo é SEM PROVA. Custo: 15 min. Roda na mesma sessão do A-8.

**P0 — trancar.** Fixar a máscara **manualmente** e confirmar pelo `state_full` — sem isso o
autoswitch pode trocar no meio e a rodada não diz nada. **Destrancar:** devolver a máscara ao
padrão do perfil dela.

**ANTES.** Máscara ativa, e o estado de vibração/giroscópio/lightbar antes de abrir.

**CONTRASTE.** Abrir o **mesmo** jogo com **cada** máscara, na mesma sessão. Sem as duas
metades não há veredito.

**PREVISÃO, derivada do código.** A migração de 26/07 foi feita **de propósito**, com marcador
persistido — ou seja, a casa já decidiu uma vez a favor de `xbox`. Previsão: `xbox` entrega
vibração e **não** entrega giroscópio; `dualsense` entrega os três. **Se `dualsense` não
entregar vibração, a migração estava certa e o tooltip é que mente.**

**ELA.** Diz, para cada máscara: vibrou? o giroscópio mexeu? a barra acendeu na cor do jogo?
**ASSISTENTE.** Confirma a máscara efetiva no instante de cada resposta.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| `dualsense` entrega os três | o **asset de fábrica** está errado | corrigir o asset; a migração ganha exceção |
| `xbox` entrega os três | o **tooltip** está errado | corrigir o texto da janela |
| cada uma entrega uma parte | não há máscara certa | a contradição vira decisão de produto, e é dela |
| nenhuma entrega giroscópio | o giroscópio não passa por máscara nenhuma | outro alvo: o espelho de movimento |

---

#### A-13. `SEM-DONO`/RUMBLE-FIXADO-GLOBAL-01 — fixar o rumble de um cala o jogo em todos?

**Pergunta.** Fixar ou parar o rumble de **um** controle pela aba Rumble bloqueia o retorno de
força do jogo em **todos**?

**Estado.** MEDIDO no código: `daemon/subsystems/gamepad.py:747` checa
`daemon.config.rumble_active` — um valor **único, sem endereço** — **antes** de qualquer
direcionamento. A reafirmação, essa sim, respeita o seletor da janela. Efeito percebido: SEM
MEDIÇÃO. Custo: 5 min. **Nenhuma sprint reivindica este achado**, e ele é irmão exato do
defeito 1 da `POSSE-POR-CONTROLE-01`.

**Cabe agora**: há três controles no rádio, e o co-op dá vpad a cada um.

**P0 — trancar.** Confirmar `rumble_passthrough` verdadeiro no `state_full` antes de começar —
se já houver rumble fixado de uma sessão anterior, a medição começa contaminada.
**Destrancar:** `rumble.passthrough` no fim, e conferir que voltou.

**ANTES.** `rumble_passthrough` e `rumble_active` no `state_full`, com o jogo vibrando.

**CONTRASTE.** `rumble.passthrough` tem de devolver a vibração **aos dois** (ou três). Se não
devolver, o instrumento está errado e o bloco não vale.

**PREVISÃO, derivada do código.** `rumble.stop` mirando **um** controle **para os dois**.
**Se só o controle mirado parar, a leitura está errada** e o gate não é global.

**ELA.** Diz, pelo tato, quais controles pararam de vibrar.
**ASSISTENTE.** Dispara `rumble.stop` e lê `rumble_active` no instante.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| os dois param | achado **CONFIRMADO** | vira defeito 5 da `POSSE-POR-CONTROLE-01` |
| só o mirado para | achado **REFUTADO** | fechar; o gate respeita o alvo por outro caminho |
| param os dois e o passthrough não devolve | há um segundo bloqueio | achado novo, pior que o original |
| nenhum vibrava desde o começo | instrumento/jogo sem retorno de força | descartar a rodada |

---

#### A-14. `SEM-DONO`/EXTERNO-PRIMEIRO-01 — o externo ligado primeiro fica com o lugar 1?

**Pergunta.** O controle externo ligado **antes** de qualquer DualSense fica com o lugar 1
para sempre, atravessando boot?

**Estado.** Cadeia MEDIDA no código: `daemon/lifecycle.py` decide **por escrito** rodar o tique
de externos **antes** do gate de conexão (*"o 8BitDo/Pro Controller merece número mesmo sem
nenhum DualSense plugado"*, linhas 3546 a 3549); sem DualSense na mesa, `_ds_reserve` devolve
piso **0** (`daemon/subsystems/external_identity.py:993` e a atribuição do piso); e
`external_identity.py:501` (`rank = max([*ocupados, int(reserve), 0]) + 1`) dá **rank 1** ao
externo, persistível porque o endereço é de hardware. Efeito na mesa: SEM MEDIÇÃO. Custo:
10 min. Explica a queixa dela — *"o 8bitdo entrou como player 1 igual o dualsense branco"* —
que hoje **não tem sprint dona**.

**Estado da mesa agora, e ele NÃO é o caso do defeito.** Com o DualSense ligado primeiro, os
números exibidos são 1 (DualSense), 2 (Pro) e 3 (8BitDo) — GRAU: MEDIDO às 20h27. É o caso
**bom**. O defeito exige inverter a ordem.

**P0 — trancar.** **Copiar o `controllers.json` para fora antes de tudo** — ele é o guarda
desta medição: com a fila antiga no disco, o resultado não quer dizer nada. Depois apagar ou
renomear o original. **Destrancar: restaurar a cópia no fim.** Sem isso a fila dela fica com
lixo de bancada.

**ANTES.** `controller list --external --json` e o conteúdo do `controllers.json` (a fila só é
registrada no carregamento — **não há leitura viva dela por IPC**; GRAU: MEDIDO).

**CONTRASTE.** A **mesma sequência com o DualSense ligado primeiro** tem de dar 1 e 2 na ordem
certa. É o caso que já está de pé agora e serve de positivo — mas precisa ser refeito
**depois** de limpar o `controllers.json`, senão compara réguas diferentes.

**PREVISÃO, derivada do código.** Com todos os DualSense **desligados**, ligando só o externo
e esperando dois tiques (~4 s): externo = **1**. Ligando o DualSense depois: DualSense = **2**.
E persiste no reboot, porque o endereço é de hardware. **Se o externo entrar como 2, a leitura
está errada** e a defesa citada no código cobre mais do que parece.

**ELA.** Desliga o DualSense, liga só o externo, avisa; depois liga o DualSense e avisa de novo.
**ASSISTENTE.** Lê o inventário **dois tiques depois** de cada aviso — não antes, ou pega a
transição.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| externo = 1, DualSense = 2, e persiste | achado **CONFIRMADO** | a queixa dela ganha dona; o "Renumerar agora" precisa de cura |
| externo = 1, mas o DualSense o desloca para 2 depois | há renumeração viva | achado menor: só a persistência incomoda |
| externo = 2 mesmo sozinho | achado **REFUTADO** | fechar; a ordem de chamadas protege |
| o número muda a cada tique | há duas fontes de numeração | é o defeito 2 da `QUATRO-NA-MESA-01` aparecendo aqui |
| depois do reboot os números trocam | a persistência não é confiável | achado novo, e muda a cura |

---

#### A-15. `IDENTIDADE-DUPLA-01`/E1 — os dois endereços do 8BitDo aparecem JUNTOS?

**Pergunta.** Os dois endereços 8BitDo (OUI `e4:17:d8`) aparecem **juntos**, ou cada modo tem
um endereço fixo e distinto?

**Estado.** A **existência** das duas identidades é MEDIDA: o registro tem o mesmo plástico nos
ranks **4** e **5**. A **correspondência modo/endereço** é SEM PROVA — e o journal de 03/08
parece **refutar** o critério de fusão proposto pela sprint. Custo: 15 min.

**Meia medição já está feita.** Agora, com o 8BitDo em **modo PS4**, **um só** endereço aparece
no inventário vivo (o do rank 5); o outro (rank 4) existe **só no disco**. GRAU: MEDIDO, 20h27.
Falta a outra metade: o modo Switch.

**P0 — trancar.** (1) Parar o watchdog de bonds — ele mexeu em trust/bond do 8BitDo em 03/08 e
reescreveria o cenário. (2) **Copiar o `controllers.json`.** **Destrancar: religar o watchdog
e restaurar o `controllers.json`** — os dois, no fim, como parte do protocolo.

**ANTES.** `controller list --external --json` **mais** o `controllers.json` lido do disco.

**CONTRASTE.** O **Pro Controller** (OUI `e0:f6:b5`), que a `IDENT-01` mediu como endereço
único em todo o período. Se o Pro também mostrar dois endereços, o fenômeno não é do 8BitDo e
a hipótese muda de alvo.

**PREVISÃO, derivada do código.** Com um modo só ligado, o inventário mostra **um** endereço e
o número exibido é estável; o segundo endereço existe **só** no `controllers.json`, nunca no
inventário. **Se os dois aparecerem vivos ao mesmo tempo, a hipótese "um controle, dois modos"
morre** e o que há é bond fantasma.

**ELA.** Liga o 8BitDo em **PS4** (`Start + A`), avisa; desliga, liga em **Switch**
(`Y+Start`), avisa.
**ASSISTENTE.** Lê o inventário no instante de cada aviso e anota o OUI e o modo — **nunca o
endereço completo em arquivo versionado**.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| cada modo, um endereço fixo e distinto, **nunca** simultâneos | hipótese das irmãs **viva** | executar a `IDENT-01` (declaração dela), **não** a regra automática |
| os dois endereços no inventário **ao mesmo tempo** | hipótese **MORTA** | são dois aparelhos ou bond fantasma — cura diferente |
| o mesmo modo entra ora com um, ora com outro | firmware com endereço instável | nenhuma regra por modo funciona; só declaração manual |
| só um endereço em qualquer modo, o outro só no disco | fantasma de pareamento antigo | poda do registro, sem nada de irmãs |
| o **Pro** também mostra dois | o fenômeno não é do 8BitDo | alvo muda inteiro; refazer a hipótese |

**Fusão recomendada, e ela é decisão de acervo, não medição.** A `IDENTIDADE-DUPLA-01` é uma
redescoberta da `IDENT-01` (mesma máquina, mesmo OUI, mesma tabela). A `IDENT-01` tem desenho
mais maduro (declaração explícita, sugestão sem aplicar, desfazer, verificação no doctor) e
**rejeita por escrito** a regra automática que a `IDENTIDADE-DUPLA-01` propõe. Nenhuma das
duas tem uma linha de código. GRAU: MEDIDO.

---

#### A-16. `MIC-BT-DONO-01`/E2 — o bit de mudo volta a zero na reconexão?

**Pergunta.** Derrubando o Bluetooth e religando **sem tocar em nada**, o bit de mudo do
microfone volta a zero em até um tique de hotplug?

**Estado.** MEDIDO: o mapa por controle **não existe** —
`core/backend_pydualsense.py:481` guarda `_mic_mute_desejado` como atributo **de instância**, e
`_mic_mute_by_uniq` não existe em lugar nenhum. Custo: 5 min. É o mais barato desta lista.

**P0 — trancar.** Deixar o mudo num estado **conhecido** antes de derrubar o rádio.
**Destrancar:** devolver ao estado que ela usa.

**ANTES.** `mic_mudo` e `mic_mudo_desejado` do `state_full` (os dois campos existem e são
publicados por controle — GRAU: MEDIDO no inventário de agora).

**CONTRASTE.** A mesma leitura **sem** derrubar o rádio, um minuto depois: o bit tem de ficar
onde estava.

**PREVISÃO, derivada do código.** Como o desejo é por instância e a instância morre com a
conexão, o bit **volta a zero** na reconexão. **Se o desejo sobreviver, existe persistência não
lida.**

**ELA.** Nada — este cabe inteiro no shell, salvo confirmar que não tocou no controle.
**ASSISTENTE.** Derruba e religa o Bluetooth e amostra os dois campos a cada tique.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| volta a zero em até um tique | E2 **CONFIRMADA** | a cura é o mapa por endereço |
| o desejo sobrevive | há persistência não lida | achar o caminho antes de escrever a E2 |
| volta a zero, mas só depois de vários tiques | há corrida na readoção | a cura precisa de ordem, não só de mapa |
| os campos não aparecem | ponte/áudio fora do ar | refazer |

**Honestidade que o protocolo tem de carregar.** O alvo é **55% a 75% de mudo**, não 0% — o
`BT-MIC-GATING-01` segue aberto e a casa já mediu que 0% **não** é obtido. Prometer 0% é
prometer o que já se sabe impossível hoje. E a reafirmação é a **2 Hz**, não a ~125 Hz: a
diferença é de continuidade, não de latência. GRAU: MEDIDO.

---

#### A-17. `TRIGGER-CANON-01` — o aceite dos sete presets curados

**Pergunta.** Os sete presets curados fazem o que o nome promete, no tato dela?

**Estado.** MEDIDO que a cura entrou e que sete presets que não faziam nada passaram a fazer.
A **sensação** é SEM PROVA — e só o tato dela fecha. Custo: 15 min.

**P0 — trancar.** Fixar o perfil e travar o autoswitch (`autoswitch.lock`), senão uma troca de
janela reaplica gatilho no meio da rodada. **Destrancar: soltar o cadeado no fim.**

**ANTES.** O preset ativo e os bytes efetivamente escritos, por controle.

**CONTRASTE.** Um preset que ela **já** conhece e aprova, intercalado entre os sete. Sem esse
positivo, "não senti diferença" não distingue preset ruim de mão cansada.

**PREVISÃO, derivada do código.** Os sete escrevem bytes distintos entre si. **Se dois presets
diferentes produzirem a mesma sensação, ou o nome está errado ou os bytes colidem** — e a
segunda hipótese é verificável no shell, sem ela.

**ELA.** Sente cada um e diz se o **nome descreve a sensação**.
**ASSISTENTE.** Confirma o preset efetivo no instante de cada resposta.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| os sete nomes descrevem o que ela sente | sprint **FECHA** | nada a fazer |
| um ou mais nomes não descrevem | é vocabulário | renomear — a palavra é dela |
| dois presets sentem igual | os bytes podem colidir | conferir no shell antes de culpar o nome |
| nenhum sente diferente do anterior | os gatilhos não estão sendo escritos | defeito, não vocabulário — reabrir |

**O que baratearia isto e não foi entregue.** A E5 (ler o **nibble alto** do byte de status do
gatilho) tornaria a validação verificável **sem a mão dela**. Enquanto ela não entrar, **cada
rodada de gatilho custa tempo dela**. GRAU: MEDIDO (não há leitura desse nibble em `src/`).

---

#### A-18. `RADIO-BOMBARDEADO-01`/F2 — a tempestade vem de STREAMAR áudio?

**Pergunta.** A tempestade de 44.718 frames vem de **streamar** áudio (banda isócrona
reservada) e não de enumerar?

**Estado.** As hipóteses 1 e 2 foram **REFUTADAS por medição**; a 3 é SUSPEITA COM MECANISMO.
Custo: 20 min, e **não precisa dela** — é pilotável por CLI.

**P0 — trancar.** (1) **A suíte de testes PARADA**, e confirmado que parou: 17 teclados uinput
por execução, cada um disparando enumeração de todos os controles no rádio. (2) `journalctl`
**sempre com data completa**. (3) Declarar o `storm_watch.sh` (de pé agora, três processos, só
leitura). **Destrancar:** nada a religar; registrar que a suíte ficou parada durante a janela.

**ANTES.** Contagem de frames corrompidos por minuto na linha de base, com o controle no rádio
e **nenhum** fluxo de áudio.

**CONTRASTE.** As duas fases são o contraste uma da outra: **5 min sem fluxo de áudio** e
**5 min com** captura e reprodução no controle. A fase de repouso é o controle negativo.

**PREVISÃO, derivada do código e do acervo.** A carga produz frames; o repouso, não. **Se as
duas produzirem, a causa é topologia** — e aí entra a F3 (item B-4).

**ELA.** Nada nesta fase. (A F3, sim, precisa da mão dela no cabo do dongle.)
**ASSISTENTE.** Roda as duas fases e conta.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| carga produz frames, repouso não | hipótese 3 **CONFIRMADA** | cura de produto: a tela avisa **durante** a sessão |
| as duas produzem | é topologia ou outra causa | executar a F3; o doctor passa a nomear a porta |
| nenhuma produz | o gatilho é outro | volta ao bloco F1 — e a suíte vira a principal suspeita |
| a contagem é zero em **todas** as janelas | instrumento quebrado | quase certo: `journalctl` sem data completa |

**E o mesmo experimento decide outra sprint.** A correlação com a
`SUITE-QUE-SUJA-O-JORNAL-01` **não está resolvida**, e é este F2 que a fecha. Estado dela hoje:
`integrations/uinput_keyboard.py:43` ainda é
`DEVICE_NAME = "Hefesto - Dualsense4Unix Virtual Keyboard"`, **sem sufixo de teste**; nenhum
portão. GRAU: MEDIDO.

---

#### A-19. `PERFIS-DELA`/C-1 — que regra cada um dos quatro perfis dela deveria ter

**Pergunta.** Qual regra cada um dos quatro perfis dela deveria ter? O `sackboy_nativo` virou
catch-all em prioridade **191** (o asset de fábrica é por critério, com prioridade **80**), e
há **três empates**.

**Estado.** MEDIDO no disco em 05/08. Custo: 30 min. **Não é medição — é trabalho dela com a
janela aberta**, e por isso não tem tabela de leitura: cada resposta é uma decisão.

**P0 — trancar.** Copiar a pasta de perfis dela para fora **antes de qualquer edição**.
**Destrancar:** manter a cópia até ela confirmar que o resultado ficou bom.

**Por que não dá para adiar.** As sete curas entregues **impedem estrago novo** e **nenhuma
conserta o já feito**; o histórico só grava a partir de 05/08 e **não alcança as versões
velhas**. GRAU: MEDIDO. Cada dia que passa não melhora este item.

**Ordem sugerida:** o `sackboy_nativo` primeiro (é o catch-all que atropela todo o resto),
depois os três empates, depois os demais.

---

#### A-20. `INVENTARIO-VIVO-01`/P1 e P2 — duas perguntas de 30 segundos que destravam a fila

**P1.** *"Quantos 8BitDo e quantos DualSense existem **fisicamente** na casa?"* O registro
guarda **dois** DualSense e **dois** endereços 8BitDo; o adaptador conhece **um** de cada.
GRAU: MEDIDO no disco; **SEM PROVA** sobre o mundo físico. Custo: 2 min, e **não precisa de
hardware — precisa da resposta dela**.

**O que ela destrava.** Se houver **um** 8BitDo só, a `IDENT-01` e a `IDENTIDADE-DUPLA-01`
seguem como estão. Se houver **dois**, as duas sprints **caem inteiras** e o que resta é
numeração normal. E o rank 1 do registro — um DualSense que o adaptador não conhece — só pode
ser podado depois desta resposta; hoje ele **empurra todo mundo para baixo**.

**P2.** *"Foi ela que pôs o alias `Nintendo MeowSystem` e a Class do adaptador para o Pro
aceitar o pareamento?"* MEDIDO que o alias existe; MEDIDO que **não vem deste repositório**
(nada em `assets/bluetooth/` escreve `Alias`); a causa é SUSPEITA COM MECANISMO. Custo: 2 min.

**Por que importa agora.** Se o alias/Class for **pré-requisito** do pareamento do Pro, mexer
no adaptador durante qualquer protocolo — inclusive o A-1 — **derruba o Pro no meio da
medição**. Esta pergunta é Passo 0 de todo protocolo que toca o adaptador.

---

#### A-21. `EMULACAO-NO-JOGO-01`/C-4 — o Alt+Tab do R1 era de propósito?

**Pergunta.** Ela usava o Alt+Tab do R1 **de propósito** no desktop? E o que o R1 deveria
fazer?

**Estado.** MEDIDO: **9 pressionamentos em 7 dias, todos dentro de janela de jogo**. A
**intenção** é SEM PROVA. Custo: 3 min. Não é medição — é uma pergunta, e sem ela ninguém
muda o padrão do R1 no lugar dela.

Registro honesto que acompanha: **o efeito do Alt+Tab no compositor segue sendo inferência,
não medição**. GRAU: SEM PROVA.

---

#### A-22. `JOGO-COMPLETO-01`/E4 — os dois interruptores no instalador

**Pergunta.** Os dois interruptores (broker e wrapper) ligam sem quebrar nada, e o instalador
é idempotente sobre as opções de lançamento?

**Estado.** SEM PROVA — e o motivo está escrito: o `install.sh` precisa ser **rodado de
verdade** na máquina dela. Custo: 25 min. **É o item de maior risco desta lista.**

**Aviso de risco, e ele é parte do protocolo.** A ordem é **irreversível na prática**: ligar o
broker **antes** do wrapper *"tira a rede de segurança que existe hoje sem pôr outra no
lugar"* — e pode deixar ela **sem controle nenhum no jogo**. Ligar o **wrapper primeiro**.

**P0 — trancar.** Copiar as opções de lançamento atuais para fora antes de rodar.
**Destrancar:** restaurar se qualquer passo falhar.

**Regras da casa que valem aqui, e reprovam se ignoradas.** `install.sh` **nunca com `sudo`**
(o `HOME` vira `/root`); sem TTY exige `--yes`. E **a idempotência só se prova rodando duas
vezes**.

**LEITURA.**

| desfecho | leitura | consequência |
|---|---|---|
| liga, jogo funciona, segunda execução não muda nada | E4 **ACEITA** | sai de trás da flag |
| liga e o jogo funciona, mas a segunda execução duplica opções | não é idempotente | corrigir antes de sair da flag |
| liga e ela fica sem controle no jogo | pior caso previsto | restaurar a cópia **imediatamente** |
| o instalador falha antes de mudar nada | rodada limpa | ler o erro e refazer |

---

### (b) PRECISA DE APARELHO QUE ELA TEM, MAS NÃO ESTÁ LIGADO

Aqui vai só o **esboço** e o que falta. Nenhum destes deve ser executado antes de ela ligar o
aparelho — e para o item B-1, antes de a `COOP-QUE-NÃO-DESMONTA-01` estar curada.

**B-1. `QUATRO-NO-RÁDIO-01`/d1+d4+d5 — quatro no rádio com um jogo aberto.** Quantos
`evdev_grab_failed` e `coop_player_removed` aparecem, quantos erros de CRC, e o rumble
sobrevive? Falta: **o quarto controle** (hoje há três no rádio) e, principalmente, a
`COOP-QUE-NÃO-DESMONTA-01` — **não medir a mesa antes dela**, porque com o Jogador 2 durando
dois segundos **dois dos quatro são o mesmo jogador** e a medição não mede o que se quer. GRAU
do bloqueio: MEDIDO. Custo: 40 min. É a medição de maior valor da casa, e a mais bloqueada.

**B-2. `NOME-HONESTO-01`/E1+E2 — o que a tela chama o 8BitDo no CABO.** MEDIDO com entradas
sintéticas: em **modo Switch por cabo** a ficha diz *"Pro Controller"* e a marca diz
*"Nintendo"* — e `friendly_type` e `brand_of` usam ordens **opostas** entre OUI e VID
(`app/actions/external_controllers.py:88` e `:108`). Falta: o **cabo USB** e ela abrir a ficha
e fotografar, nos dois modos. Sem a foto, a E2 (*o rótulo não pode ultrapassar o sinal*) não
tem como ser aceita. Custo: 10 min.

**B-3. `IDENTIDADE-DUPLA-01`/E1, metade Switch.** Ver A-15: a metade PS4 já está medida; falta
ela ligar o 8BitDo em **`Y+Start`**. Custo: 5 min a mais.

**B-4. `RADIO-BOMBARDEADO-01`/F3 — o dongle em porta de outro barramento.** Só entra **se** a
F2 (A-18) devolver *"as duas fases produzem frames"*. É o único ponto da F2/F3 que exige a mão
dela no cabo. Custo: 10 min.

**B-5. M-08 — a máscara do perfil sobrevive ao reboot?** Mecanismo MEDIDO:
`daemon/connection.py:220-224` passa `mode_applier=None` no restore, **com o motivo escrito** —
quem manda no boot são os flags persistidos, não o perfil. Falta: **um reboot** da máquina
dela, com o controle na mesa. E o roteiro obrigatório (`git log -S "mode_applier"`) **nunca foi
executado**. Custo: 15 min, e o reboot é o que ela precisa querer.

**B-6. `BORDA-DE-QUEDA-01`/defeito 1 — a confirmação numérica.** Ela **já confirmou pelo tato**
em 03/08 (*"desliga sozinho e o controle branco segue vibrando"*); falta só cronometrar os ~3 s
(o teto do expirador). Precisa de **dois controles no rádio com um jogo vibrando** — e os dois
controles existem agora, mas o defeito foi descrito com dois DualSense. A cura **pode ser
escrita sem isto**, e os defeitos 2 e 3 da mesma sprint já estão MEDIDOS no código. Custo:
5 min. Valor: baixo.

---

### (c) PRECISA DE APARELHO QUE ELA TALVEZ NÃO TENHA

**C-1. M-15 / `MIC-BT-DONO-01`/E4 — os botões de gesto dos controles 2, 3 e 4.** Exige **dois
DualSense**: o botão de microfone **só existe neles**, e o inventário vê **um**, com o segundo
sem bond no adaptador (GRAU: MEDIDO). **Inexecutável hoje** — e isso é dado, não falha.
Mecanismo MEDIDO e mais largo do que o M-15 diz: `core/backend_pydualsense.py:1981` abre com
*"INPUT vem SEMPRE do controle PRIMÁRIO"*, e `core/evdev_reader.py:782` registra por extenso
que **`mic_btn` não tem keycode evdev** — é injetado só na leitura do primário. Ou seja:
**todo gesto** do produto nasce do primário, não só o microfone. Quando houver dois: previsão
= `mic_btn` **nunca** aparece para um secundário e **sempre** para o primário; contraste
obrigatório = o mesmo botão no primário, e depois **trocar quem é o primário**. Custo: 10 min,
quando existir o segundo aparelho.

**C-2. GYRO-02 / M-5 — o enable-IMU do Pro Controller por CABO.** Exige o Pro **por cabo**:
`daemon/subsystems/external_identity.py:165` (`_IMU_ENABLE_ALLOWED_BUS = "usb"`) **recusa BT de
propósito**, e o gate de OUI está em `:859`. Falta o **cabo USB**. **Mas a pergunta mudou de
forma hoje** — ver a seção 6. Previsão falsificável que sobrevive: **por cabo o endereço pode
ser sintético** (o degradador forja endereço começando por `02`), e nesse caso o gate de OUI
`e0:f6:b5` **nunca dispara** e o enable **nunca é enviado**. Custo: 15 min com o cabo na mão.

**C-3. `SOM-ROTA-01`/E4+E5 — o caminho do microfone e o byte 53.** Exige um **fone de 3,5 mm
plugado no controle**. O inventário **não lista fone**; se ela não tiver, **o item não
existe**. GRAU: SEM PROVA. Custo: 15 min. Valor: baixo.

---

## 4. M-12: a bancada vem antes da mesa

O **M-12** (*"a trava manual congela a cor dos quatro, e não só do controle mexido?"*) ficou
fora das três listas de propósito, e a razão é de método.

**Mecanismo MEDIDO:** `daemon/state_store.py:102` é um conjunto **único, sem endereço**
(`self._manual_override_categories: set[str]`), e `profiles/manager.py:388-391` obedece com
`None` — *"não mexe"* — **para todos**. Efeito na mesa: SEM MEDIÇÃO.

**Por que não está na fila dela:** isto é **reproduzível em bancada com dois endereços falsos**,
sem hardware nenhum. A recomendação é escrever a bancada primeiro; **ela mede só para confirmar
que a bancada representa a mesa** — e aí o custo dela cai de 25 min para 5.

**Ponto de colisão a vigiar, e ele é real:** a cura da `TRAVA-QUE-SOLTA-TARDE-01` restaura por
categoria **sem endereço** em `daemon/ipc_handlers.py:463` e
`daemon/subsystems/hotkey.py:186`. A união dos baldes resolve a *leitura*; a *reescrita* dessas
duas linhas continua global. GRAU: MEDIDO.

---

## 5. O aceite de TELA que está devendo

Nada aqui precisa de hardware. Precisa do **olho dela**, e a regra de tamanho da
`PROVA-DE-TELA-01` vale: *uma leva que toca a janela vai até **uma aba por vez***.

| # | o que | estado real, conferido no código | o que ela faz |
|---|---|---|---|
| T-1 | **As nove abas maximizadas** (`ALINHA-DUAS-LINHAS-01`, `JANELA-QUE-RESPIRA-01`, `CARD-ÚNICO-01`) | ENTREGUES em código, com medição em bancada. Aceite: SEM PROVA | passar pelas nove abas com a janela **real** maximizada e dizer se a queixa *"tá absolutamente muito feio"* foi paga |
| T-2 | **Os três diálogos novos de 05/08** | existem em `app/gui_dialogs.py:105`, `:154` e `:198` (rebaixar casamento, rebaixar prioridade, descartar edição pendente) e **ninguém nunca os fotografou**. GRAU: MEDIDO | abrir os três e dizer se o texto é claro |
| T-3 | **`LIGHTBAR-JOGADOR-01`/E0** | **ZERO linhas escritas**, e os cinco widgets de luz de jogador seguem vivos na janela. GRAU: MEDIDO. É queixa direta dela: *"essas cores que não fazem sentido"* | dizer **o que as cinco luzes deveriam mostrar**, se é que devem existir. A sprint inteira depende disso |
| T-4 | **`RADAR-01`/E1 (o applet do painel)** | `packaging/cosmic-applet/src/ipc.rs` **não tem** campo `autoswitch_locked` (GRAU: MEDIDO — grep por `autoswitch` devolve zero) | é a **única** superfície do projeto que não dá para fotografar por bancada; o olho dela é obrigatório |
| T-5 | **`CARD-OCUPA-01`** | ABERTA; é pedido literal dela de 31/07 | dizer se os desenhos (touchpad, lightbar, microfone, alto-falante) ocuparam bem o vão lateral do cartão |
| T-6 | **`LARGURA-01`/E8** | `app/widgets/segmented_selector.py:33` ainda é `_WRAP_COLUNAS = 3` fixo. GRAU: MEDIDO | dizer se a grade de três colunas da aba Gatilhos está boa na largura real. **Entra sozinha**: a aba Gatilhos já teve um commit rejeitado |
| T-7 | **`STATUS-SIMETRIA-01`** | a própria sprint declara: *"o número final é decisão dela, olhando a tela"* | um número, olhando a aba |
| T-8 | **`RADAR-01`/E2 (a bandeja)** | `app/tray.py:273` ainda diz `"Tray icon indisponivel no COSMIC. "` — sem acento e com termo em inglês. GRAU: MEDIDO | decisão de produto: vale manter as 463 linhas de uma bandeja que **não aparece** na máquina dela? |
| T-9 | **`FIAÇÃO-QUE-FALTA-01`/E1** | o verificador `profiles/sanidade.py` tem **406 linhas** e só `cli/cmd_doctor.py` o chama. GRAU: MEDIDO | só **depois** de a fiação existir. E o veto já está escrito: **o aviso não pode bloquear o salvar** |

**Armadilha de aceite registrada, e ela reprova correção por engano.** O texto da bandeja (T-8)
só aparece **uma vez por máquina**, por causa de uma flag persistente. Ela **não vai ver a
correção** sem apagar a flag ou rodar com `HEFESTO_DUALSENSE4UNIX_RESET_TRAY_WARNING=1`. Isso
precisa ser dito **no momento** de validar, não depois. GRAU: MEDIDO
(`app/tray.py` cita a variável).

**Regra que fecha a seção.** Antes e depois de qualquer leva que toque a janela, rodar
`scripts/gui-captura/retratar_abas.py`: sai um PNG por aba, sem clique, e a documentação nunca
fica velha.

---

## 6. O que NÃO precisa de medição

Esta seção existe para ela **não gastar tempo**. Cada linha abaixo parece pendente e não é —
ou porque já foi paga, ou porque um leitor **refutou a premissa**.

### 6.1 Premissas refutadas nesta varredura

**A IMU do Pro Controller por Bluetooth — a premissa caiu hoje.** O acervo diz que a IMU do Pro
*"nasce em STANDBY"* e que **por Bluetooth o Hefesto não a liga** (verdade no código:
`_IMU_ENABLE_ALLOWED_BUS = "usb"`, `external_identity.py:165`). Disso o acervo concluiu que
**por Bluetooth não há giroscópio**. **Medi agora e não é isso:** o nó `Pro Controller (IMU)`
existe e está **transmitindo** — **1.825 eventos de eixo em 6 segundos**, com gravidade
estável num eixo (~4.180) e ruído de giroscópio nos outros, com o controle **parado na mesa** e
conectado **por Bluetooth**. GRAU: **MEDIDO**. Consequência: a pergunta *"o enable-IMU faz
alguma coisa?"* **não é mais sobre ter giroscópio por rádio** — ele já tem, e vem do DKMS. A
pergunta que sobra é estritamente sobre o caminho **USB**, e continua valendo a previsão do
endereço sintético (item C-2). **Não gastar sessão dela para descobrir se o Pro tem giroscópio
por rádio: tem.**

**A `IDENTIDADE-DUPLA-01` descreve um dano que outra onda já matou.** A premissa *"come um slot
de co-op / empurra o quarto controle"* **não se reproduz**: a numeração desacoplou lugar-na-fila
de número exibido — a contagem considera só quem está **presente**
(`daemon/subsystems/external_identity.py`, a função de posição). Prova ao vivo, hoje: o disco
tem os externos nos ranks **3** e **5**, e a tela mostra **2** e **3**. GRAU: MEDIDO. O dano
que **sobra** é outro e é real: entrada fantasma permanente no registro, inflação de rank, e um
número devolvido para aparelho que não está na mesa.

**As seis transições do `SINAL-DE-JOGO-01` não são prova.** Foram **derrubadas** pelo
verificador. Qualquer protocolo que as cite como linha de base começa errado. GRAU: MEDIDO.

**O critério de fusão da `IDENTIDADE-DUPLA-01` pode já nascer refutado.** A regra proposta
(*"duas identidades só são a mesma se nunca aparecerem conectadas ao mesmo tempo"*) é
contradita pelo parágrafo acima dela no próprio documento, que afirma escritas de LED para
**ambos** no mesmo período. E a `IDENT-01` **já havia recusado por escrito** esse mesmo
critério: *"verdadeiro, mas insuficiente — um aparelho ausente pode simplesmente estar
desligado"*. **A forense do journal decide isso sem hardware** — fazer antes de pedir os dois
modos a ela. GRAU: SEM PROVA (a contradição é MEDIDA; qual lado vale, não).

**A `BT-SURDO-01`/E0-E1 foi REFUTADA.** O rádio **não** emudece em repouso: ~300 Hz com o
controle parado, 1.402.128 bytes em 60 s. GRAU: MEDIDO. Não repetir.

**A `LIGHTBAR-BT-CLAIM-01` foi REFUTADA em 03/08** — a cura proposta lá **apaga** a barra.
GRAU: MEDIDO.

### 6.2 Já pago, e o documento ainda pede

- **`LIGHTBAR-BT-CULPADO-01`/E1 está APLICADA** (o `0x08` saiu da adoção por Bluetooth), apesar
  de o cabeçalho dizer *"nenhuma linha de código tocada"*. GRAU: MEDIDO. **Não refazer a
  lightbar.**
- **`MIC-BT-01`, entrega 1, está FEITA** (`app/mic_monitor.py` descobre a fonte da ponte pelo
  prefixo). GRAU: MEDIDO.
- **`MIC-USB-01`, entregas 2 e 7, estão PAGAS**: o botão de microfone da aba Status com as três
  camadas existe, e o `install.sh` já chama o doctor com correção de microfone. GRAU: MEDIDO.
- **`SENSOR-VIVO-01`/E4 e E5 estão em CÓDIGO** — o que falta é **aceite**, não implementação
  (item A-11). GRAU: MEDIDO.
- **O medidor de microfone da aba Status já foi aceito por ela em 04/08.** Não repetir.
- **`UI-SELETOR-01` está PAGA** (absorvida pela ordenação por número de identidade); só o
  cabeçalho do documento está errado. GRAU: MEDIDO.
- **`CONTAGEM-01`/E2 e E4 estão PAGAS** (contagem única somando externos; a aba Emulação parou
  de contar nó). **E1 e E5 seguem abertas.** GRAU: MEDIDO.
- **`WRAPPER-EM-TODOS-01`/E1 e E2 estão ENTREGUES**, apesar do cabeçalho dizer PROPOSTA. **E3
  não.** GRAU: MEDIDO.
- **`CONTAGEM-E-COOP-01`/E1a e E2 estão ENTREGUES; E1b não** — e o portão que falta (*perguntar
  antes de marcar "este jogo não funciona" com 2+ jogadores*) **subiu de prioridade**, porque
  com o co-op sempre ligado o preço passa a ser cobrado **sempre**. GRAU: MEDIDO.
- **`EMPATE-01` está inteira entregue**, e dois índices ainda a pedem. GRAU: MEDIDO.
- **`RADIO-ABERTO-01`/E8, E9 e E10 estão FEITAS.** GRAU: MEDIDO.
- **`BT-SDP-VAZIO-01`, `BT-AGENT-TRAVA-O-RESTART-01` e `BT-SNAPSHOT-SANDBOX-01` estão
  CURADAS.** GRAU: MEDIDO.

### 6.3 Medível sem ela — não ocupa sessão dela

Estes estão abertos no código e **um assistente fecha sozinho**. Valem porque **liberam** a
fila de cima.

- A **bancada dos quatro controles com relógio virtual** (`COOP-QUE-NÃO-DESMONTA-01`/E4)
  **não existe**, e **três sprints dependem dela** — inclusive o item B-1, que é a medição de
  maior valor da casa. GRAU: MEDIDO. **É o item de maior alavancagem da varredura inteira.**
- A **bancada de dois endereços falsos** da `POSSE-POR-CONTROLE-01` (o M-12, seção 4).
- **`ESTADO-QUE-MENTE-01`/E1+E2** — o topo do `state_full` não deriva da lista
  (`daemon/ipc_handlers.py:1612`), e o próprio documento diz que é reproduzível **sem
  hardware**. GRAU: MEDIDO.
- **`BT-SURDO-01`/E2, E3 e E4** — device não fechado no abandono, ioctl de 5 s segurando o
  bloqueio central, e a chamada síncrona no laço de eventos do boot. GRAU: MEDIDO.
- **`BONDS-QUE-SOBREVIVEM-01`/D1 a D4** — **ninguém aciona** a restauração (nenhum timer,
  nenhum gancho de parada, nenhum código chama o script); a poda é por **contagem**, não por
  tempo (doze snapshots de 1 bond apagam o de 4); e **nenhuma vigia conta bonds**. GRAU: MEDIDO.
- **A fiação de `window_detect_reason` já existe** — o estudo diz que *"ficou fora de escopo"*,
  e é **falso hoje**: o autoswitch já repassa a razão. Falta só **ler** no daemon vivo. GRAU:
  MEDIDO. **Não gaste sessão dela nisto.**
- **`SINAL-DE-JOGO-01`/E5** — `daemon/state_store.py` já tem o estado de "enxergando", e
  `daemon/lifecycle.py:3456` **ainda lê** o de "saudável". A cura é **uma linha**. GRAU:
  MEDIDO. (O **aceite** precisa dela olhando a lightbar, e entra sozinho, num commit só,
  **depois** das E3 e E4.)
- **A previsão do defeito 4 da `QUATRO-NA-MESA-01`** — contar no journal os descartes de cache
  de lightbar para nó que **não** é novo.
- **A forense do journal da `IDENTIDADE-DUPLA-01`** (seção 6.1): decide se vale pedir os dois
  modos a ela.

### 6.4 Um portão da casa tem furo — e não é medição, é conserto

O portão de anonimato de endereço exige **separador** entre octetos, e o outro portão só varre
`tests/`. **A forma compacta, de 12 dígitos corridos, passa pelos dois.** Existem hoje
ocorrências em documentos versionados, inclusive em três dos que esta varredura cita. E um dos
OUIs da bancada **nem está** na lista do teste. GRAU: MEDIDO (`bash scripts/check_anonymity.sh`
passa com as ocorrências de pé).

**Nada foi alterado nesta varredura** — o registro fica aqui porque **qualquer sprint nova que
cite journal vai reproduzir o vazamento achando que o portão a protege**.

### 6.5 O que não cabe em protocolo nenhum

- A **queda do Bluetooth em si** (a sprint que a trataria ainda não foi escrita).
- O **`BT-MIC-GATING-01`** (por que o firmware mantém 55% a 75% de mudo).
- A **ponte de saída de áudio por Bluetooth** — precisa resolver uma contradição de relatório
  **antes** da primeira linha de código.
- A **`MÁSCARA-01`**: *"o critério que os jogos usam nunca foi medido neste projeto"* — as
  afirmações existentes sobre ordem de enumeração são **inferência, não experimento**. GRAU:
  SEM PROVA, declarado pela própria sprint. E ela depende da `IDENT-01`.

---

## 7. O placar, para não se perder

- **41** medições pendentes conferidas contra o código.
- **31** caixas do `CHECKLIST` de 25/07 seguem `[ ]`; **zero** marcadas. É o mesmo número de
  30/07 — **nada andou em sete dias**. GRAU: MEDIDO (contagem).
- **32** dão para fazer agora, pelo inventário das 20h27 de 06/08.
- **3** são inexecutáveis hoje por falta de aparelho (dois DualSense, cabo USB, fone de 3,5 mm).
- **1** item domina tudo o que sobra: a bancada dos quatro com relógio virtual, que **não
  precisa dela** e destrava a medição de maior valor da casa.

E a regra que este documento inteiro serve para lembrar: **hipótese tem de explicar o que JÁ
funcionava**, e **teste tem de morder**. Se o resultado couber em qualquer linha da tabela de
leitura, a medição valeu. Se não couber em nenhuma, a tabela estava incompleta — e é a tabela
que se conserta, não o resultado.
