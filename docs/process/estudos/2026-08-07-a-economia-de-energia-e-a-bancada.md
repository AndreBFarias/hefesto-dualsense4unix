# A economia de energia e a bancada

Medição do estado de energia da máquina dela em **07/08/2026**, sobre
`restauro/inicio-da-sessao`, e a pergunta que ela abriu ao lembrar disso.

Toda leitura de `/sys`, `/proc`, `/etc` e do journal foi **pura**: nada foi
escrito em hardware, nenhum serviço reiniciado, nenhum controle derrubado. Os
três controles seguiram na mesa e o DualSense seguiu carregando durante a
medição inteira.

---

## A pergunta dela

Citação literal, sem correção de acentuação — citação não se corrige.

> *"mapear o kernel do Linux pra ver se em algum momento ele ativava o modo
> economia de energia e isso zoava os nossos testes e afins"* <!-- noqa-acento -->

Ela tem duas perguntas dentro de uma, e elas se separam:

1. **de energia** — o kernel liga economia em algum momento?
2. **de método** — se ligar, isso contamina o que a suíte mede?

A resposta da primeira é **não, em lugar nenhum que importe** — e está medida
adiante, aparelho por aparelho. A resposta da segunda é mais desconfortável, e
é o motivo real deste documento: **não é a economia que contamina a bancada; é
a ausência dela.** A máquina está travada no extremo oposto, e é essa trava que
faz 56 asserções em forma de relógio passarem verde.

## Como ler os graus

Como manda a casa, e no mesmo vocabulário da
[referência canônica](../../protocol/dualsense-referencia-canonica.md):

| grau | significa |
|---|---|
| **MEDIDO** | li nesta máquina, nesta árvore, hoje; ou reprovei um teste e devolvi |
| **SUSPEITA COM MECANISMO** | o caminho foi lido e fecha, o efeito não foi observado |
| **SEM PROVA** | está dito e ninguém verificou |

---

## O que já estava medido, e o que caducou

A suspeita dela **tem precedente nesta casa** e ela está certa em lembrar: em
26/06/2026 houve uma auditoria de sete agentes sobre a tempestade de `-71`, que
investigou exatamente autosuspend, C-states, ASPM e `threadirqs`. Ela **não é
versionada** — o diretório `docs/process/audits/` está no `.gitignore` (linha
57) —, então o que ela mediu só sobrevive se for recontado. Foi o que fiz.

O que dela **continua de pé** (reconferido hoje, **MEDIDO**):

- **Nenhum daemon de economia agressivo existe nesta máquina.** `tlp`,
  `powertop`, `tuned-adm`, `cpupower` e `laptop-mode`: binário ausente.
  `power-profiles-daemon`: não instalado. `thermald`: instalado e **inativo**.
  A classe inteira de hipóteses "uma ferramenta de energia derrubou o controle"
  segue eliminada.
- **`usbcore.autosuspend=-1` e `pcie_aspm=off` seguem no cmdline**, e seguem
  apontando na direção **protetiva**, não na destrutiva.
- **O governador segue em `performance`** e o `system76-power` segue em
  `Performance`.

### Nota datada — 07/08/2026: três achados de 26/06 caducaram

Não se apaga decisão medida. Estas três mudaram de estado e ficam registradas
com o que valia antes:

| item | o que valia em 26/06 | o que vale hoje (**MEDIDO**) |
|---|---|---|
| `threadirqs` | ativo no cmdline; a auditoria o elegeu **candidato número 1** a agravador, por threadar a IRQ do xHCI dos controles | **ausente** do `/proc/cmdline` e do `/etc/kernelstub/configuration`; `ps -eo comm` devolve **zero** threads `irq/*-xhci_hcd`. O self-heal dela o desativou na v3.25, com a justificativa escrita no próprio script |
| `processor.max_cstate=1` | vivo no boot de então, já removido da persistência | **ausente** dos dois. E ele virou desnecessário: não há driver de cpuidle nenhum (adiante) |
| `usbcore.quirks=054c:0ce6:k` (`NO_LPM`) | vivo no boot de então, já despersistido | **substituído** por `054c:0ce6:gn,054c:0df2:gn` — a **alavanca (A)** da emenda do [ADR-018](../../adr/018-usb-power-scope-vs-dropout.md), que preserva o áudio do controle |

O eixo de energia que a auditoria de 26/06 deixou como pendência **foi
executado**, e por outra mão que não a nossa. A investigação daquele dia não
precisa ser refeita.

---

## O estado de energia MEDIDO, hoje

Máquina: **AMD Ryzen 7 5800X**, 16 fios. Boot de 05/08 às 20:07:47; **1 dia e
19 horas** de pé no momento da medição.

### 1. Linha de comando do kernel

`/proc/cmdline` deste boot e `/etc/kernelstub/configuration` (próximo boot)
**coincidem token a token** — não há divergência pendente de reinício, que era
justamente a armadilha de 26/06.

Os que tocam energia:

| token | efeito | direção |
|---|---|---|
| `usbcore.autosuspend=-1` | o default do kernel é 2 s; `-1` = nunca suspender nenhum aparelho USB | mantém acordado |
| `pcie_aspm=off` | desliga o Active State Power Management dos enlaces PCIe | mantém acordado |
| `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` | `g` = `DELAY_INIT`, `n` = `DELAY_CTRL_MSG`: espaça a rajada de enumeração do DualSense | mantém acordado |
| `mitigations=off`, `acpi_enforce_resources=lax` | não são de energia; listados por completude do delta contra o Pop!\_OS de fábrica | — |

O journal deste boot confirma o efeito, e não só a intenção: **`PCIe ASPM is
disabled`**. **MEDIDO.**

Registro de precisão que custa caro esquecer, e que o `scripts/doctor.sh` já
protege em `check_pcie_aspm`: com `pcie_aspm=off` o arquivo
`/sys/module/pcie_aspm/parameters/policy` **continua exibindo `[default]`**.
Conferi: exibe. Quem usar esse arquivo como prova conclui o contrário do que a
máquina está fazendo. A prova é o cmdline e a linha do journal.

### 2. CPU — o achado mais relevante para os testes

| medida | valor lido | leitura |
|---|---|---|
| `scaling_driver` | `amd-pstate-epp` (`status=active`, `prefcore=enabled`) | driver moderno, em modo ativo |
| `scaling_governor` | `performance` nos **16** fios | sem economia |
| `energy_performance_preference` | `performance` — e a lista de disponíveis tem **um item só** | em governador `performance`, o `amd-pstate-epp` **tranca** o EPP; não há como estar em economia sem trocar o governador |
| `scaling_min_freq` | **1 727 728 kHz** (1,73 GHz) | é o **piso imposto** |
| `cpuinfo_min_freq` | **575 910 kHz** (0,58 GHz) | é o piso do silício |
| `cpufreq/boost` | `1` | turbo ligado |
| `cpuidle/current_driver` | **`none`** | **não há driver de ociosidade registrado** |
| `/sys/devices/system/cpu/cpu0/cpuidle/state*` | **não existe** | não há estado C nenhum exposto |
| journal | `cpuidle: using governor menu`, `process: using mwait in idle threads` | o governador subiu e não achou driver; a ociosidade cai no `mwait` puro |
| `system76-power profile` | `Performance` | perfil de energia da distro no extremo |

Duas coisas merecem ser ditas em voz alta.

**Primeira: o piso de frequência está 3,0x acima do piso do silício.** A CPU
desta bancada **não consegue** descer abaixo de 1,73 GHz. Uma máquina de
fábrica desce a 0,58 GHz. **MEDIDO.**

**Segunda: não existe driver de cpuidle.** Não é que os estados C profundos
estejam desabilitados por parâmetro — é que o kernel **não achou nenhum** para
registrar. A explicação coerente é que o firmware não expõe os objetos `_CST`,
o que bate com o que a auditoria de 26/06 registrou sobre a BIOS desta máquina
(*Global C-state Control* e *DF C-states* desligados). **Grau: MEDIDO** que o
driver é `none` e que não há diretório de estados; **SUSPEITA COM MECANISMO**
para a atribuição à BIOS — não reli o firmware, e não vou reiniciar a máquina
dela para isso.

O efeito prático é o que importa: **latência de saída de ociosidade
praticamente nula e determinística.** Numa máquina com C6 vivo, a saída custa
centenas de microssegundos; num laço de 200 Hz, cujo período é 5 000 µs, isso é
uma fração real do orçamento. Aqui não custa nada.

### 3. USB

Todos os **nove** nós em `/sys/bus/usb/devices` — os quatro hosts e os cinco
aparelhos — leem exatamente o mesmo:

```
power/control            = on
power/autosuspend_delay_ms = -1000
power/runtime_status     = active
```

Os quatro barramentos penduram em dois controladores xHCI: `0000:02:00.0` (do
chipset) e `0000:0c:00.3` (do I/O die). Ambos com `power/control=on` e
`runtime_status=active`. **MEDIDO.**

**E aqui está o achado que muda a leitura de tudo: nenhum controle está no USB
neste instante.** O que enumera é: dois receptores 2,4 GHz, uma webcam, uma NIC
802.11ac e o adaptador Bluetooth. O par `054c:0ce6` **não aparece** em
`/sys/bus/usb/devices`. O DualSense está no rádio **e** carregando — logo, por
cabo de carga apenas ou por carregador, sem enumerar.

Consequência **MEDIDA**, e ela não é pequena: `assets/72-ps5-controller-autosuspend.rules`
(o [ADR-013](../../adr/013-usb-autosuspend-disabled.md)) e o quirk `gn` do
cmdline estão **inertes agora**. Não estão errados, não estão quebrados: estão
sem alvo. Só voltam a valer quando o controle enumerar no USB. Qualquer medição
de energia sobre "o DualSense" feita neste estado da mesa mede o **rádio**, não
o cabo.

### 4. PCIe

- `pcie_aspm=off` no cmdline, `PCIe ASPM is disabled` no journal. **MEDIDO.**
- De **42** aparelhos PCI, **12** estão em `power/control=auto` e **30** em
  `on`. Os 12 em `auto` são **todos** `pcieport` — pontes, não aparelhos.
- **Cinco** dessas pontes estão em `runtime_status=suspended`. Todas na árvore
  `0000:03:xx` (chipset). **Nenhuma** na cadeia que serve os controles.
- A cadeia do rádio, na íntegra:
  `0000:00:08.1` (ponte, `control=auto`) → `0000:0c:00.3` (xHCI, `control=on`)
  → `usb3` → `3-1` (adaptador Bluetooth).

A ponte `00:08.1` está em `auto`, e à primeira vista isso parece o furo que a
pergunta dela procurava. Não é: ela está **`active`**, presa acordada pelo
filho em `on`. Uma ponte com PM de runtime não suspende enquanto tiver filho
ativo. Quem a segura é a nossa regra
`assets/81-hefesto-usb-host-power.rules`, somada à `99-storage-no-link-pm.rules`
dela. **MEDIDO.**

### 5. Bluetooth — onde a medição quase deu errado

O enunciado da investigação pede `/sys/class/bluetooth/hci0/device/power/*`.
Segui esse caminho e ele tem **um único arquivo**: `async`. Nenhum botão de PM
de runtime.

Isso não é ausência de economia — é **medir no lugar errado**, e vale registrar
porque é a mesma armadilha número 1 da casa em outra roupa.
`/sys/class/bluetooth/hci0/device` resolve para `3-1:1.0`, que é a **interface**
USB. Os botões de PM vivem no **aparelho-pai**, `3-1`. É a mesma razão pela qual
o [ADR-013](../../adr/013-usb-autosuspend-disabled.md) aplica em
`SUBSYSTEM=="usb"` e não em `hidraw`, e está escrito lá desde sempre.

No lugar certo (`/sys/bus/usb/devices/3-1/power/`):

| atributo | valor | leitura |
|---|---|---|
| `control` | `on` | PM de runtime desligado |
| `autosuspend` / `autosuspend_delay_ms` | `-1` / `-1000` | trava redundante |
| `runtime_enabled` | **`forbidden`** | o kernel foi proibido de tentar |
| `runtime_status` | `active` | acordado |
| **`runtime_suspended_time`** | **`0`** | **nunca dormiu** |
| `active_duration` | 157 004 288 ms | **43,6 h** acordado |
| `connected_duration` | 157 004 293 ms | 43,6 h conectado |

As duas últimas linhas são a resposta direta à pergunta dela, e não dependem de
interpretação: **o adaptador ficou acordado 157 004 288 dos 157 004 293
milissegundos em que esteve plugado.** Cinco milissegundos de diferença, e zero
tempo suspenso. **MEDIDO.**

E o módulo: `btusb` com `enable_autosuspend=N`. O default do módulo neste kernel
é `Y` — quem o desliga é o **nosso**
`assets/modprobe/hefesto-btusb-no-autosuspend.conf`, e o `scripts/doctor.sh` já
confere isso em `check_btusb_autosuspend`.

### 6. PM de runtime em geral — o achado negativo

**Há algum aparelho relevante em `power/control=auto` que deveria estar em
`on`? Não.** Varri as duas árvores. Os únicos `auto` são as 12 pontes PCIe, e
nenhuma das cinco suspensas serve os controles. **MEDIDO.**

---

## De quem é cada peça

A separação de donos importa porque metade destes artefatos **não é nossa** e o
nosso desinstalador não pode tocá-los — é o que o
[ADR-018](../../adr/018-usb-power-scope-vs-dropout.md) chama de fronteira de
responsabilidade.

### Nosso — posto pelo `install.sh`, **sem flag nenhuma**

| artefato | o que faz |
|---|---|
| `assets/72-ps5-controller-autosuspend.rules` | autosuspend off por VID/PID (ADR-013) |
| `assets/81-hefesto-usb-power.rules` | controles Sony/Nintendo/8BitDo/Microsoft e adaptadores BT por **classe `e0`** nunca dormem |
| `assets/81-hefesto-usb-host-power.rules` | hosts USB por **classe PCI `0x0c03*`** em `on` |
| `assets/modprobe/hefesto-btusb-no-autosuspend.conf` | `btusb enable_autosuspend=0` |
| `assets/modprobe/hefesto-dualsense-storm.conf` (via `scripts/install_snd_quirk.sh`) | espaça os control-transfers do `snd_usb_audio`; **preserva** microfone e fone |

As três primeiras estão instaladas e conferidas em `check_udev` do
`scripts/doctor.sh` — 14 regras canônicas, as duas `81-*` incluídas.

Um detalhe de **atribuição**, e ele está honesto no código: as duas regras `81`
escrevem **o mesmo valor** que as `99-*` dela já garantem. São inócuas por cima,
e existem para a máquina de outra pessoa ficar íntegra sozinha. O comentário
dentro de `assets/81-hefesto-usb-power.rules` diz isso com todas as letras.

### Dela — o ritual da Aurora, fora do nosso alcance

| artefato | dono |
|---|---|
| `usbcore.autosuspend=-1` e `pcie_aspm=off` no cmdline | Aurora |
| `/etc/udev/rules.d/99-usb-kill-autosuspend.rules` | Aurora (12/04) |
| `/etc/udev/rules.d/99-storage-no-link-pm.rules` | Aurora v3.3 |
| `validate_power_state()`, de hora em hora | `ritual-aurora-self-heal.timer` |

E o nosso instalador **sabe disso**. O registro de dono do PLAT-03, em
`~/.local/state/hefesto-dualsense4unix/cmdline-owners.conf`, tem exatamente duas
linhas nesta máquina:

```
cmdline.usbcore.autosuspend=terceiro
cmdline.usbcore.quirks=terceiro
```

`terceiro` significa: já estava lá, não fomos nós, **o desinstalador nunca
toca**. O mecanismo que decide isso é
`src/hefesto_dualsense4unix/integrations/kernel_cmdline.py`. **MEDIDO** — o
arquivo existe, com esse conteúdo, e o `install.sh` foi lido para confirmar a
semântica.

### Da distro — Pop!\_OS

`amd-pstate-epp` como driver, `system76-power` ativo em `Performance`,
`thermald` instalado e inativo, e as cinco pontes PCIe suspensas do chipset.

### Do firmware

A ausência de driver de cpuidle. **SUSPEITA COM MECANISMO**, conforme dito.

---

## A pergunta que importa: isso zoa os testes?

### A resposta curta: hoje, não. E é justamente esse "hoje" que é o problema.

Rodei a bancada com a máquina **em uso real** — carga de 13,8 nos 16 fios
durante toda a medição, que é a mesma condição sob a qual a
[RELOGIO-NAO-E-ASSERCAO-01](../sprints/2026-08-06-RELOGIO-NAO-E-ASSERCAO-01-os-testes-que-mediam-a-maquina-em-vez-do-produto.md)
viu o defeito 1 ficar vermelho.

| execução | resultado | grau |
|---|---|---|
| os 6 arquivos mais suspeitos, 6 rodadas, carga 13,8 | **46 verdes** todas as vezes; 6,54 s a 6,65 s | **MEDIDO** |
| os mesmos 6, confinados a 2 fios (`taskset`) | 46 verdes, 3 de 3 | **MEDIDO** |
| os mesmos 6, confinados a **1** fio | 46 verdes, 3 de 3 | **MEDIDO** |
| os **23** arquivos com forma de relógio (331 testes) | 331 verdes na base, **e também** sob contenção 8x e 16x | **MEDIDO** |

Então: **no estado de energia de hoje, a economia não contamina a suíte.**
Achado negativo, e bem medido. Ele vale.

Mas ele vale por um motivo específico, e é aí que a resposta vira outra coisa.

### A resposta longa: a bancada não é neutra — ela é uma cura

Repare no que foi medido acima. Governador travado em `performance`, EPP travado
junto, **piso de frequência 3x acima do piso do silício**, **nenhum estado C
profundo**, ASPM desligado, USB proibido de suspender. Esta máquina está no
extremo oposto da economia, em **todas** as camadas ao mesmo tempo.

A suíte não passa porque os testes são robustos. Ela passa porque a bancada é
rápida, previsível e **não desacelera nunca**. Isso é a armadilha número 1 da
casa outra vez: o instrumento está medindo a bancada, não o produto.

Então parei de perguntar "a economia contamina?" e passei a perguntar **"quanta
folga existe antes de contaminar?"** — que é a pergunta que dá para responder
sem escrever em `/sys`.

### O experimento, e o que ele achou

Não posso trocar o governador dela. Mas posso **restringir o meu próprio
processo**: fixar o `pytest` num núcleo e fixar concorrentes de CPU no **mesmo**
núcleo. A máquina dela nem sente — os outros 15 fios seguem livres — e o
processo de teste enxerga uma CPU efetiva fracionada, que é o que a economia de
energia faria com ele.

O resultado, e ele reprova:

```
--- teste no núcleo 0, com 8 concorrentes no MESMO núcleo 0 (~1/9 de núcleo)
    rodada 1: 1 failed, 35 passed
    rodada 2: 1 failed, 35 passed
```

O culpado, isolado:

```
FAILED tests/unit/test_poll_loop_evdev_cache.py::
       test_snapshot_chamado_exatamente_uma_vez_por_tick_sem_consumidores
E       AssertionError: poll.tick esperado >= 10, obtido 0
E       assert 0 >= 10
```

**Este é, textualmente, o teste que a RELOGIO-NAO-E-ASSERCAO-01 listou como
aberto e nunca visto vermelho.** A sprint escreveu, na seção do que fica aberto:

> *"as folgas ali são bem maiores (30 tiques previstos para 10 exigidos) do que
> a do teste que quebrou (12 para 8), e nenhum deles foi visto vermelho."*

Foi visto agora.

### Nota datada — 07/08/2026, sobre a RELOGIO-NAO-E-ASSERCAO-01

Aquele item ficou registrado com **SUSPEITA COM MECANISMO** de que os 23 lugares
restantes reprovassem sob carga. Para
`tests/unit/test_poll_loop_evdev_cache.py`, o grau **sobe para MEDIDO** hoje. A
sprint não errou: ela disse exatamente o que sabia e o que não sabia, e o que
não sabia era isto. O número dela — 23 ocorrências em 12 arquivos — também não
está errado; com o critério mais largo que usei (janela de 8 linhas, incluindo
`time.sleep`), a contagem sobe para **56 ocorrências em 23 arquivos**. São
critérios diferentes, e ambos se refazem.

### O mecanismo, medido

`obtido 0` não é "o laço ficou lento". É **o laço não começou**. Isolei a causa:

| medida | valor | grau |
|---|---|---|
| o teste **sozinho**, primeiro do processo, sob contenção 8x | **reprova 4 de 4** | **MEDIDO** |
| o **mesmo** teste, precedido de um arquivo qualquer (aquecimento), mesma contenção | **passa 4 de 4** | **MEDIDO** |
| custo de importar `daemon/lifecycle.py` + `testing`, um núcleo livre | **105–109 ms** | **MEDIDO** |
| o mesmo, sob contenção 8x | **413–418 ms** | **MEDIDO** |
| a janela que o teste concede | **150 ms** | **MEDIDO** |
| imports preguiçosos (dentro de função) no pacote `daemon/` | **266** | **MEDIDO** (contagem por forma) |

O grafo de módulos do daemon custa 107 ms nesta máquina, **no talo**. O teste
concede 150 ms para o laço subir e dar 10 tiques. Qualquer fração desse custo
que caia **dentro** da janela — e caem, porque o pacote tem 266 imports
preguiçosos — consome o orçamento inteiro assim que a CPU efetiva encolhe. A
4x, já não cabe.

**Grau: MEDIDO** para a reprovação determinística, para o A/B do aquecimento e
para os quatro números. **SUSPEITA COM MECANISMO** para a atribuição exata ao
import preguiçoso dentro de `daemon.run()`: o caminho foi lido e fecha, mas não
instrumentei a subida tique a tique.

### E é aqui que a energia entra

O modo de falha é **partida a frio**. Nenhum outro é tão sensível à economia de
energia, e a razão é mecânica:

- Numa máquina em `powersave`, o governador **ainda não rampou** quando a rajada
  de import chega. Os primeiros 150 ms são servidos na frequência baixa.
- Nesta bancada, o piso é 1,73 GHz. Numa máquina de fábrica, é 0,58 GHz — **3x
  menos**, antes de contar a rampa.
- Some a saída de estado C profundo, que aqui custa zero porque **não há driver
  de cpuidle**.

Ou seja: as três camadas de energia que estão travadas nesta máquina são
exatamente as três que atacam uma partida a frio. **A configuração de energia
dela mascara este defeito.** Não o causa — o mascara.

**Grau: MEDIDO** que ~1/9 de núcleo reprova; **SUSPEITA COM MECANISMO** que
`powersave` num piso de 0,58 GHz produza o mesmo. Só fecha com ela rodando o
A/B, e está no protocolo adiante.

### Os testes reféns do relógio — o inventário

Critério, escrito para a conta poder ser refeita: `await asyncio.sleep(<const>)`
ou `time.sleep(<const>)` com uma asserção sobre contador, `len()` ou contagem de
chamadas nas **oito** linhas seguintes.

**56 ocorrências em 23 arquivos.** Elas se dividem em duas formas, e a segunda
não estava nomeada em lugar nenhum:

**Forma A — `assert contador >= N`.** É a que a RELOGIO-01 nomeou. Reprova
quando a máquina é lenta demais para dar N tiques.

| arquivo | janela | exige | previsto | folga |
|---|---|---|---|---|
| `tests/unit/test_poll_loop_evdev_cache.py` | 0,15 s | 10 a 200 Hz | 30 | 3,0x — **e reprovou** |
| `tests/unit/test_daemon_lifecycle.py` | 0,20 s | 5 a 120 Hz | 24 | 4,8x |
| `tests/unit/test_daemon_connect_grace.py` | 0,15 s | 1 a 200 Hz | 30 | 30x |
| `tests/unit/test_daemon_resilient_subsystems.py` | 0,01 s | 1 a 200 Hz | 2 | 2,0x |

A folga nominal **não previu** quem reprovou: o de 3,0x caiu e o de 2,0x não. É
a prova de que o gargalo é a **partida**, não a taxa.

**Forma B — `assert X == 1` depois de um `sleep` fixo.** É a **maioria**, e é
tão refém quanto a A: se a máquina não chegou lá dentro da janela, o valor é
`0`, e `0 == 1` reprova pelo mesmo motivo. Aparece em
`tests/unit/test_autoswitch.py`, `tests/unit/test_daemon_reconnect_loop.py`,
`tests/unit/test_daemon_hang01_external_tick.py`,
`tests/unit/test_daemon_pause.py`, `tests/unit/test_reconnect_hotplug_fast.py` e
outros. **Grau: MEDIDO** que a forma existe e onde; **SEM PROVA** de que alguma
delas reprove — nenhuma ficou vermelha nos meus experimentos.

**A forma que resiste, e ela já existe na casa.** Dois padrões passaram por tudo
que joguei neles:

- **`wait_for(timeout=...)`** — 17 ocorrências em 6 arquivos. Espera o evento,
  não o relógio.
- **Prazo com laço de espera** — a cura de `ae32c10`, em
  `tests/unit/test_keyboard_wire_up.py`. Variantes dela existem em **10**
  arquivos. Nenhuma reprovou.

A cura já está escrita, testada e usada. O que falta é ela chegar aos outros.

### Uma armadilha que **não** existe — e vale dizer

Varri a suíte procurando asserção sobre **duração medida** (`assert elapsed <
X`, `assert duracao <= Y`). O varredor devolveu três candidatos, e os três são
**falsos positivos**: um mede diferença de matiz de cor, outro mede delta de
contador de erros de rádio, o terceiro é um argumento chamado `delta`.

**Zero asserções sobre tempo decorrido em 431 arquivos de teste.** **MEDIDO.**
Esta casa nunca escreveu "isto tem de rodar em menos de X" — e essa é a
categoria que a economia de energia destruiria de forma mais direta e mais
silenciosa. É um acerto que ninguém registrou, e agora está registrado.

### O que o `scripts/doctor.sh` vê e o que não vê

| eixo | o doctor confere? |
|---|---|
| autosuspend do `btusb` | **sim** (`check_btusb_autosuspend`) |
| ASPM PCIe | **sim** (`check_pcie_aspm`), e já sabe que o sysfs mente |
| as 14 regras udev, incluindo as duas de energia | **sim** (`check_udev`) |
| quirk USB do storm, e conflito com a regra 75 | **sim** (`check_usb_quirk`, `check_usb_storm_config_conflict`) |
| **governador de CPU** | **não** |
| **driver e estados de cpuidle** | **não** |
| **piso de frequência** | **não** |
| **perfil do `system76-power`** | **não** |

O que ele não vê é, ponto por ponto, o eixo **CPU** — que é o único que este
estudo mostrou capaz de mudar o veredito de um teste. **MEDIDO** por leitura do
arquivo.

Antes de virar recomendação: **o eixo CPU é do dono da máquina, não nosso.** O
`check_pcie_aspm` já resolveu esse mesmo dilema do jeito certo — informa, diz
que a política é decisão do dono, e não manda ninguém mudar nada. Se algum dia
formos cobrir CPU, é essa a forma. E isso é **desenho, não medição**: fica como
proposta, não como entrega.

---

## O que fica ABERTO

- **O A/B do governador não foi feito.** É a medição que fecha a pergunta dela
  de verdade, e ela exige escrever em `/sys/devices/system/cpu/*/cpufreq/`. Está
  no protocolo. **SEM PROVA** de qual seria o resultado.
- **`tests/unit/test_poll_loop_evdev_cache.py` continua com a forma antiga.**
  A cura existe em `tests/unit/test_keyboard_wire_up.py` e é de três linhas.
  Não a apliquei: a árvore tem outro trabalho em curso, e mudar teste sem ela
  pedir viola a primeira regra da casa. **MEDIDO** que reprova; a cura é
  entrega de outra leva.
- **As outras 55 ocorrências não foram exercitadas uma a uma.** Contenção 8x e
  16x nos 23 arquivos deu 331 verdes; só a partida a frio isolada reprovou.
  Quantas reprovariam com **cada uma** sendo a primeira do processo é **SEM
  PROVA** — exigiria 23 execuções isoladas, e a máquina dela está em uso.
- **A ordem de coleta é a ordem dos arquivos.** Não há `pytest-randomly` nesta
  árvore (**MEDIDO**: a coleta repetida devolve a mesma ordem). Então o defeito
  é **determinístico** hoje, e só aparece se alguém rodar aquele arquivo
  sozinho — que é exatamente o que se faz ao depurar um teste. Se um dia entrar
  aleatorização de ordem, ele vira intermitente. **SUSPEITA COM MECANISMO.**
- **A auditoria de 26/06 continua fora do git.** Este documento recontou o eixo
  de energia dela, mas não os outros. Se `docs/process/audits/` sair do
  `.gitignore` um dia, é decisão dela — e a
  [CLEAN-ROOM.md](../CLEAN-ROOM.md) é quem manda no que pode ser publicado.
- **A ausência de driver de cpuidle não foi atribuída ao firmware com prova.**
  **SUSPEITA COM MECANISMO.** Fechar exige entrar na BIOS, e isso é um reinício
  da máquina dela.
- **`assets/81-hefesto-usb-power.rules` e `assets/81-hefesto-usb-host-power.rules`
  citam, no comentário, um estudo `2026-07-18-estudo-kernel-hardening.md` que
  **não existe nesta árvore** (`find` devolve vazio). O mesmo vale para o
  `2026-07-18` citado em `assets/modprobe/hefesto-btusb-no-autosuspend.conf`. As
  regras estão corretas e medidas; a **procedência** delas aponta para o vazio.
  O portão de referências não pega porque só varre `docs/`. **MEDIDO.**

---

## PROTOCOLO — o que só fecha com ela rodando

Ela já decidiu, na resposta 9 de 07/08, que a próxima sessão de hardware começa
pelo protocolo de 06/08. **Este protocolo vem depois daquele**, e tem uma
propriedade que vale dizer antes de tudo:

> **Nada aqui toca hidraw, rádio, `bluetoothd` ou serviço nenhum. Nenhum
> controle cai.** É CPU e leitura, só. Pode rodar com os três controles na mesa,
> com o DualSense carregando, sem risco para a sessão.

O que ele decide: **se a bancada estivesse em economia, a suíte mudaria de
veredito?**

### Passo 1 — a linha de base, sem escrever nada

```bash
cd /mnt/Apate/Desenvolvimento/hefesto-dualsense4unix
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq
.venv/bin/python -m pytest -q tests/unit/test_poll_loop_evdev_cache.py
```

Esperado: `performance`, `1727728`, **5 verdes**. Guarde os dois números — são
o estado a devolver no passo 4.

### Passo 2 — a reprovação sem mexer em energia

Confirma, na mão dela, o que medi. Um núcleo, oito concorrentes nele:

```bash
for j in $(seq 1 8); do
  taskset -c 0 .venv/bin/python -c 'import time
fim = time.monotonic() + 60
while time.monotonic() < fim: pass' &
done
sleep 1
taskset -c 0 .venv/bin/python -m pytest -q tests/unit/test_poll_loop_evdev_cache.py
wait
```

Esperado: **`poll.tick esperado >= 10, obtido 0`**. Se der verde, a máquina
dela está ainda mais folgada do que quando medi, e o número `8` precisa subir.

### Passo 3 — o A/B do governador, que é o que decide

**Aqui é o único ponto que escreve fora da árvore.** É reversível, não persiste
por si, e não toca aparelho nenhum:

```bash
# desce para economia
echo powersave | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq

# a suíte de relógio inteira, três vezes
for i in 1 2 3; do
  .venv/bin/python -m pytest -q \
    tests/unit/test_poll_loop_evdev_cache.py \
    tests/unit/test_daemon_lifecycle.py \
    tests/unit/test_keyboard_wire_up.py \
    tests/unit/test_daemon_connect_grace.py \
    tests/unit/test_daemon_reconnect_loop.py \
    tests/unit/test_rumble_persistent.py
done

# e o arquivo suspeito SOZINHO, que é o modo de falha real
for i in 1 2 3; do
  .venv/bin/python -m pytest -q tests/unit/test_poll_loop_evdev_cache.py
done
```

**O que cada resultado significa:**

| resultado | conclusão |
|---|---|
| tudo verde | a folga aguenta o governador; a economia **não** é o eixo. O defeito é de partida a frio e só, e a cura é a de `ae32c10` |
| o arquivo sozinho reprova, o conjunto não | **confirma a hipótese deste estudo**: economia + partida a frio derrubam. A cura vira prioridade |
| o conjunto reprova | é pior do que medi, e a varredura das 56 tem de virar leva |

### Passo 4 — devolver a máquina

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor   # tem de dizer performance
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq   # tem de bater com o passo 1
```

O `system76-power` está ativo e em `Performance`; se o piso não voltar sozinho,
`system76-power profile performance` o restaura. **Nada disso persiste em
reinício** — o governador não é gravado em lugar nenhum.

### Passo 5 — opcional, e só se ela quiser fechar o eixo de firmware

Com o controle **plugado no USB por um cabo de dados** (o de carga não
enumera), conferir que a regra 72 e o quirk `gn` saem da inércia:

```bash
ls -d /sys/bus/usb/devices/*/ | while read d; do
  [ -f "$d/idVendor" ] && grep -q 054c "$d/idVendor" && \
    echo "$d control=$(cat $d/power/control) quirks=$(cat $d/quirks)"
done
bash scripts/doctor.sh 2>&1 | grep -iE "quirk|autosuspend|udev"
```

Esperado: `control=on` e `quirks` com o bit de `DELAY_INIT`/`DELAY_CTRL_MSG`.
Isso **não** foi medido hoje porque o controle não estava no cabo — é o único
item deste estudo que ficou sem medição por estado da mesa, e não por escolha.

---

## O resumo em cinco linhas

1. **O kernel não liga economia em lugar nenhum que importe.** Nove nós USB em
   `on`, adaptador Bluetooth 43,6 h sem dormir um milissegundo, ASPM desligado,
   nenhum driver de cpuidle, governador em `performance`. **MEDIDO.**
2. **A metade disso é nossa** (quatro artefatos, todos sem flag), **a metade é
   dela** (Aurora), e o nosso instalador registra a diferença em vez de
   atropelá-la.
3. **A economia não contamina a suíte de hoje.** Achado negativo, medido sob
   carga real de 13,8. **MEDIDO.**
4. **Mas a bancada é uma cura, não um controle.** Reduzida a CPU efetiva a ~1/9
   de núcleo, `tests/unit/test_poll_loop_evdev_cache.py` reprova **4 de 4** com
   `obtido 0` — o teste que a RELOGIO-01 listou como nunca visto vermelho.
   **MEDIDO.**
5. **O que decide de vez é o A/B do governador, e ele é dela.** Não derruba
   controle, não toca rádio, e se desfaz com um `echo`.
