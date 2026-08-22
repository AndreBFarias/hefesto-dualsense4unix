# JOGO-COMPLETO-01 — os nove recursos dentro do jogo

- **Estado:** CONCLUIDA — o "Status (02/08/2026): ABERTA" abaixo caducou: a E4 está no `install.sh:3369` (passo 11b-bis, sem flag, ordem broker→wrapper em `:3386-3394`), com teste em `tests/unit/test_launch_options_apply_cli.py` (verificado em 21/08/2026)
- **Status (02/08/2026):** ABERTA. A E1 desta sprint foi absorvida pela
  PAINEL-DA-VERDADE-01 e pela PARIDADE-SONY-01 (o `visto_ha_s` é o
  instrumento que ela pedia). A **E4 — os dois interruptores no install —
  NÃO foi feita**, e o motivo está no fim deste arquivo
- **Status original:** PROPOSTA, escrita em 01/08/2026 **para sobreviver à queda da
  sessão**. Tudo o que é preciso para executar está aqui
- **Prioridade:** ALTA — é o pedido dela: *"isso precisa funcionar na parte da
  Sony e também deve funcionar quando eu opto pelo Hefesto na opção
  DualSense"*
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)
- **Ela pediu, literal:** *"vai materializando os outros tópicos pra ir
  colocando e adicionando eles ao modo jogo, tipo aqueles 7 mais mic e
  speaker"*

## A lista dela, e o que a analogia do Zelda quer dizer

Ela nomeou os recursos assim: *"o áudio da tela, o giroscópio do controle
nativo, o touch, o gatilho adaptativo, a possibilidade de usar o mic e temos o
próprio som que sai adicionalmente no próprio controle (outro canal específico
de som)"*. E deu o exemplo que fecha o sentido:

> *"Zelda Skyward Sword: você joga como Link e usa os controles do Wii, o
> speaker do controle faz os barulhos da espada do Link enquanto na tela tem o
> som que sai normal do jogo."*

Isso importa para não confundir dois áudios diferentes: **o som da tela** (o
mix do jogo, que sai onde o sistema mandar) e **o canal do controle** (efeitos
que o jogo manda *só* para o alto-falante do DualSense). São dois, e os dois
precisam existir ao mesmo tempo.

## O estado medido em 01/08/2026

Tudo abaixo foi medido nesta máquina, com o daemon vivo e o DualSense no cabo.
**Leia a seção seguinte antes de confiar na coluna "chega ao jogo"** — houve um
diagnóstico errado nesta mesma data, e ele está corrigido aqui.

| # | recurso | Sony nativo | Hefesto → DualSense | evidência |
|---|---|---|---|---|
| 1 | vibração | nativo | **FUNCIONA** | `ff_play_count`; SDL: `rumble=True` nos dois |
| 2 | lightbar | nativo | **FUNCIONA** | 108 réplicas no journal |
| 3 | player-LEDs | nativo | **FUNCIONA** | 99 réplicas |
| 4 | gatilho adaptativo | nativo | **FUNCIONA** | 28+28 réplicas — e o kernel **não tem** API de gatilho, então só o jogo pode tê-las gerado |
| 5 | alto-falante do controle | PipeWire | **FUNCIONA** | entregue na SOM-02/SOM-04; não passa pelo gamepad |
| 6 | giroscópio | nativo | **provável, não confirmado em jogo** | dado no report do vpad, byte-idêntico ao físico; SDL3 enumera o vpad |
| 7 | acelerômetro | nativo | idem | idem |
| 8 | touchpad (dedo + clique) | nativo | **não confirmado** | dado presente; ver "O caso do touchpad" |
| 9 | microfone | PipeWire (USB) | **USB sim; BT em aberto** | ver "O caso do microfone" |

## A correção de diagnóstico — leia antes de agir

Em 01/08 mediu-se o gamepad virtual pelo SDL e concluiu-se que **só a vibração
chegava ao jogo**. **Esse diagnóstico está errado**, e o erro foi de
instrumento: a medição usou a `libSDL2` **2.30.0 do Ubuntu**, que nenhum jogo
da Steam carrega.

Refeito com a biblioteca certa:

```
SDL2 2.30.0 (sistema Ubuntu):
  054c:0ce6  /dev/hidraw4                        → 1 dispositivo

SDL3 3.4.10 (a que a Steam distribui):
  054c:0ce6  /dev/hidraw4  DualSense Wireless Controller
  054c:0df2  /dev/hidraw5  Hefesto Virtual DualSense P1   ← ENUMERADO
```

**Causa da diferença, com proveniência:** o suporte a dispositivos `uhid` entrou
no `hidapi` upstream em 2020 (PR libusb/hidapi#166) e o SDL3 herdou ao
sincronizar o hidapi em 2023. O SDL2 clássico nunca sincronizou — o ramo
`BUS_USB` dele exige um ancestral `usb_device` em sysfs, e um dispositivo uhid
vive em `/devices/virtual/misc/uhid/`, sem ancestral nenhum.

**Consequência prática:** para jogos que usam a SDL da Steam ou Proton, o vpad é
um DualSense completo. Para um jogo Linux nativo que carregue a libSDL2 do
sistema, ele é um joystick genérico.

**A lição de método, que vale mais que o achado:** *medir contra a biblioteca
errada produz um alarme convincente e falso.* Todo instrumento desta sprint tem
de declarar **qual** SDL está usando.

## O caso do touchpad — a pista dela

Ela observou: *"fora do jogo o touchpad funciona como mouse, no modo jogo não —
talvez a resposta esteja aqui"*. A pista está certa, e leva a **duas coisas
diferentes** que estavam sendo confundidas:

**(a) O touchpad como MOUSE é desligado de propósito no modo jogo.**
`daemon/subsystems/mouse.py`, `discard_touchpad_motion`: *"Drena-e-descarta o
movimento acumulado do touchpad. Chamado pelo poll loop quando a emulação está
suprimida (modo-jogo)"*. Sem isso o cursor andaria durante a partida, e ao sair
do modo jogo o cursor pularia o acúmulo. **Isto é comportamento correto** — não
conserte.

**(b) O touchpad como TOUCHPAD DE DUALSENSE é outro caminho.** Os dois pontos
de toque viajam dentro do report 0x01 do vpad, byte-idênticos aos do físico, e
o clique tem caminho próprio (TOUCH-CLICK-01). Se o jogo lê o hidraw do vpad —
e as réplicas de gatilho provam que ele lê — **o dado está lá**.

**Portanto a pergunta em aberto é só uma:** o jogo consome o touchpad do vpad?
E ela só se responde com jogo aberto.

## O caso do microfone

**Por USB:** funciona, e não passa pelo gamepad — é uma placa de som USB, e o
jogo a pega pelo PipeWire. **Mas está MUDO nesta máquina agora**, medido: 4 s de
captura devolveram RMS 0,00 (silêncio digital absoluto), com três `[FAIL]` do
`doctor` apontando estado persistido do WirePlumber. Cura conhecida:
`bash scripts/doctor.sh --fix`.

**Por Bluetooth:** em aberto. Ela disse: *"nunca tínhamos descoberto por conta
própria o canal certo pra isso"*. O DualSense por BT **não usa A2DP/HFP** —
encapsula áudio em reports HID. Há código parcial em
`integrations/dualsense_bt_audio.py` e a ponte aparece no `state_full` como
`bt_mic.{enabled,running}`. Fechar esse canal é trabalho próprio, e tem sprint
irmã.

## Entregas

### E1 (PORTÃO) — o instrumento que diz a verdade

Antes de qualquer conserto, um instrumento reusável que responda, **por
recurso e por dispositivo**, o que a API que o jogo usa enxerga.

Existe protótipo funcionando: enumera pelo SDL, imprime `path`, `VID:PID`,
`giroscópio`, `acelerômetro`, `touchpads`, `LED`, e **chama de verdade**
`SetLED()` e `SendEffect()` mostrando o erro quando falham. Os probes ficaram
no diretório temporário da sessão de 01/08; se não existirem mais, o desenho
está descrito aqui e são ~60 linhas de `ctypes`.

**Três requisitos, e o primeiro é o que evita repetir o erro do dia:**

1. **declarar qual biblioteca está medindo** — caminho absoluto e
   `SDL_GetRevision()` no cabeçalho da saída. Sem isso o resultado não vale;
2. medir as duas: a do sistema **e** a que a Steam carrega
   (`SteamLinuxRuntime_sniper/.../sdl2-compat/` e `libSDL3.so.0`);
3. **a estrutura `SDL_hid_device_info` tem de estar completa.** Faltar campo
   desloca o ponteiro `next` e o resultado sai errado *sem erro nenhum* — foi o
   que aconteceu na primeira medição de 01/08. A ordem é: `path`, `vendor_id`,
   `product_id`, `serial_number`, `release_number`, `manufacturer_string`,
   `product_string`, `usage_page`, `usage`, `interface_number`,
   `interface_class`, `interface_subclass`, `interface_protocol`,
   **`bus_type` (SÓ no SDL3)**, `next`.

**Onde vive:** `scripts/` (para o `doctor` poder chamar) — é diagnóstico, não
teste.

**Aceite:** rodar e obter a matriz recurso × dispositivo × biblioteca, com a
revisão do SDL impressa.

### E2 — o `doctor` para de afirmar o que não mediu

Hoje ele diz **"giroscópio chegando ao jogo: SIM"** baseado em o daemon estar
*escrevendo* no nó de movimento. Isso prova que **nós entregamos**, não que
**alguém recebe**. É a mesma classe de erro da medição errada acima.

**Onde:** `scripts/doctor.sh`, o bloco `check_vpad_motion` (procure
`giroscópio no jogo`).

**A cura:** ou a frase muda para o que foi medido (*"o daemon está entregando
giroscópio ao gamepad virtual (NNN Hz)"*), ou o cheque passa a usar o
instrumento da E1 e aí pode afirmar o que afirma.

**Aceite:** nenhuma linha do `doctor` afirma "chega ao jogo" sem ter perguntado
à API que o jogo usa.

### E3 — a aba Status para de mentir pela mesma razão

O card escreve **"Giroscópio: fluindo para o jogo (~194 Hz)"**. Mesmo problema,
na tela que ela mais olha.

**Onde:** `app/widgets/controller_card.py`, `texto_motion`.

Esta entrega é irmã da [PAINEL-DA-VERDADE-01](2026-08-01-PAINEL-DA-VERDADE-01-a-aba-status-diz-o-que-chega-ao-jogo.md)
— faça as duas juntas ou nenhuma, para não haver duas frases sobre o mesmo
fato.

### E4 — os dois interruptores entram no install, sem flag

**Pedido literal dela:** *"isso deveria estar no install sem flag"*.

Medido em 01/08, com o `doctor`:

- **`broker hide-hidraw` não instalado** — o hidraw do controle **físico** fica
  visível a qualquer jogo;
- **nenhum jogo com o wrapper** nas opções de inicialização — logo as variáveis
  que o projeto materializa (`SDL_GAMECONTROLLER_IGNORE_DEVICES`,
  `PROTON_DISABLE_HIDRAW`) **nunca são exportadas**.

Consequência: **todo jogo enxerga dois DualSense.** É o defeito do controle
duplicado que este projeto já combateu, de volta pela porta dos fundos.

**Onde:** `install.sh` (a etapa do broker e a etapa das Launch Options — procure
`hide-hidraw`, `LAUNCH_WRAPPER`, `steam_launch_options`), e
`src/hefesto_dualsense4unix/integrations/steam_launch_options.py`.

**Requisitos dela, todos obrigatórios:** viável, **idempotente**, dentro do
install **sem flag**, e sem derrubar a infraestrutura existente.

**Duas armadilhas nomeadas:**

1. **ordem importa.** Ligar o broker enquanto os jogos não têm o wrapper tira a
   rede de segurança que existe hoje (um jogo que adote o físico tem tudo
   nativamente) sem pôr outra no lugar. **O wrapper vem primeiro.**
2. **o broker nunca esconde o vpad** — `hidraw_broker.py` recusa o
   `VPAD_PRODUCT` explicitamente. Logo o REPLICA-03 sobrevive ao broker.
   Confirme isso antes, não depois.

**Aceite:** `doctor` sem os dois avisos; e um jogo enxergando **um** DualSense.

### E5 — o veredito dos quatro recursos em aberto, com jogo

Os recursos 6, 7, 8 (giro, accel, touchpad) e o mic USB precisam de aceite com
jogo rodando. **Mas o teste ficou barato** graças à E1:

| gesto | onde olhar |
|---|---|
| girar o controle | o instrumento da E1 mostra `gyro=True` no vpad, e o jogo responde |
| arrastar o dedo no touchpad | `evtest` no nó de touchpad do vpad + o jogo |
| clicar o touchpad 3× | `touchpad_clicks` no `state_full` vai de 0 a 3 |
| falar no microfone (depois do `--fix`) | `parec` no source do controle: RMS sai de 0,00 |

**Aceite:** a matriz da seção "O estado medido" preenchida sem nenhum
"provável".

## Testes que vão reprovar

Rode antes: `pytest tests/unit -k "motion or vpad or replica or doctor or status"`.

- `test_motion_telemetry.py` — trava as strings exatas de `texto_motion`
  (ex.: `"Giroscópio: fluindo para o jogo (~248 Hz)"`). A E3 muda a frase;
- `test_doctor_vpad_motion.py` — trava a saída do bloco do doctor. A E2 muda;
- os testes de `install.sh` e de simetria com o `uninstall.sh` — a E4 acrescenta
  passos, e a regra da casa é que tudo que o install põe, o uninstall tira;
- `test_uhid_replica.py` — se a E4 mexer no broker, confirme que as réplicas
  continuam.

## O que NÃO fazer

- **Não "consertar" o `discard_touchpad_motion`.** Ele está certo: é o que
  impede o cursor de andar durante a partida.
- **Não medir contra a `libSDL2` do sistema** e concluir coisa alguma sobre
  jogos da Steam. Foi o erro de 01/08.
- **Não ligar o broker antes do wrapper.** Ver armadilha 1 da E4.
- **Não tentar passar áudio pelo gamepad virtual.** Um dispositivo `uhid` não
  tem placa de som — medido: existe **uma** placa ALSA, a do controle físico.
  Microfone e alto-falante correm por fora, e é assim que tem de ser.

---

## Nota de 02/08/2026 — o que foi absorvido, e por que a E4 não entrou

### O que já está entregue por outras sprints

A **E1** (o instrumento que diz a verdade) foi entregue como o `visto_ha_s` da
[PAINEL-DA-VERDADE-01](2026-08-01-PAINEL-DA-VERDADE-01-a-aba-status-diz-o-que-chega-ao-jogo.md),
com uma categoria por recurso e morte por inatividade — e a categoria de áudio
veio na [PARIDADE-SONY-01](2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md).

A **E3** (a aba Status para de mentir) é a linha da verdade do card:

```
No jogo agora: giroscópio (~194 Hz), vibração, luz · sem pedido ainda: gatilho, clique do touchpad.
```

### Por que a E4 NÃO entrou — e ela é o pedido literal dela

*"isso deveria estar no install sem flag"*. Os dois interruptores continuam
desligados, e **todo jogo enxerga dois DualSense**.

A entrega não foi feita porque ela mexe no `install.sh`, e as condições para
fazê-la com segurança não existiam nesta leva:

1. **a ordem importa e é irreversível na prática** — a própria sprint avisa que
   ligar o broker antes de os jogos terem o wrapper *"tira a rede de segurança
   que existe hoje sem pôr outra no lugar"*. Errar a ordem deixa ela sem
   controle nenhum no jogo;
2. **o install não pode ser validado aqui.** As regras desta casa são
   explícitas: `install.sh` **nunca com `sudo`** (o `HOME` vira `/root`), e sem
   TTY exige `--yes`. Um instalador que muda as opções de inicialização da
   Steam dela precisa ser rodado de verdade antes de ser dado como pronto;
3. **os requisitos dela são duros** — viável, **idempotente**, sem flag, e sem
   derrubar a infraestrutura existente. Idempotência em cima do
   `steam_launch_options` é o tipo de coisa que se prova rodando duas vezes.

**A sprint fica aberta com a E4 inteira**, e é a próxima da fila quando houver
uma sessão com a máquina dela para rodar o install e conferir o `doctor`.
