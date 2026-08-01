# O que a Sony, a Valve e o kernel documentam — estudo de 01/08/2026

- **Levantado por:** dois agentes de pesquisa externa (documentação oficial e
  caminho do jogo) + dois de medição na máquina dela, em 01/08/2026
- **Pedido dela, literal:** *"o SDK da Sony, toda empresa tem acesso à
  documentação da Sony, deve tá público ensinando como programar as features no
  desenvolvimento de jogos"* — e depois: *"pode documentar a pesquisa dos
  agentes e salvar elas permanentemente no projeto como documentação física? E
  atualizar as demais docs principais pra nunca mais termos essa lacuna de
  conhecimento no repo?"*
- **Onde a substância mora:** [a referência canônica do protocolo](../../protocol/dualsense-referencia-canonica.md).
  Este estudo guarda o **processo**, os **vereditos** e as **sprints que
  abriram** — o que se aprendeu, e como

## A resposta à pergunta dela

**Ela estava certa sobre existir, e errada só sobre ser público.** A
documentação da Sony é boa, é completa, e é NDA.

Mas **dois pedaços escaparam por vias legítimas**, e os dois são a base de tudo
que este estudo produziu:

1. **A Valve redistribui o header da Sony** dentro do Steamworks SDK
   (`isteamdualsense.h`, marcado `Copyright (C) 2019 Sony Interactive
   Entertainment`) — traz a enum oficial dos 7 modos de gatilho e as faixas de
   cada parâmetro;
2. **O driver `hid-playstation` do Linux foi escrito por um funcionário da
   Sony** (Roderick Colenbrander, SIE) — e ele explicou por escrito, na lista do
   kernel, **o que deixou de fora e por quê**.

A segunda é a mais valiosa, e por um motivo que este projeto vive: os gatilhos
adaptativos e os haptics ficaram fora do driver **de propósito**, porque *"não
há ainda uma API apropriada no kernel Linux para expô-los"*. **O espaço de
usuário é o dono desses bytes por omissão declarada do autor** — não por
acidente. É a licença para este projeto existir.

## Os cinco vereditos

### 1. A ressalva de proveniência dos bytes de áudio CADUCOU

O `core/ds_output_report.py` marcava `common[4..7]` como *"PROVÁVEL, não
medido"*, porque o kernel os declarava `reserved`. O **Linux 6.18** (patches da
Collabora para o jack de áudio) **os nomeia exatamente assim**. Os bytes 5, 6 e
7 sobem para confiança ALTA.

**Consequência direta:** a sprint `PARIDADE-SONY-01` nasceu com um portão de
medição por causa dessa incerteza. O portão continua valendo (ainda não há
captura de report de jogo), mas a premissa dos bytes deixou de ser suspeita.

### 2. A curva do alto-falante que esta casa mediu está CORROBORADA — e explicada

Em 01/08 mediu-se: **mudo até 38, satura em 102**, 60% do curso inerte. A
explicação apareceu no kernel 6.18: para fazer o alto-falante soar, ele escreve
**três** campos, não um — a **rota** (`OUTPUT_PATH_SEL = 3`), o **volume**
(`0x64` = 100) e um **pré-amplificador** (`SP_PREAMP_GAIN = 2`).

Este projeto escreve só o volume. Os 64 passos úteis são a assinatura disso — e
o `0x64` que o kernel escolhe é exatamente o topo da faixa medida aqui.
**A medição desta casa e o kernel concordam.**

### 3. O caso do Zelda tem um nome no protocolo

Ela descreveu: *"o speaker do controle faz os barulhos da espada enquanto na
tela tem o som normal do jogo"*. Isso é `OUTPUT_PATH_SEL = 2` — **canal
esquerdo para o fone/TV, canal direito para o alto-falante do controle**. Um
byte, documentado no kernel e no `dualsensectl`.

### 4. A causa-raiz do rumble preso foi ENCONTRADA

O código traz o comentário: *"Isto é MITIGAÇÃO, não a cura. A cura seria
descobrir por que o stop se perde"*. Achou-se: quando o SDL manda **parar**, ele
emite um report com os bits de vibração **desligados** e motores zerados — e o
portão deste projeto descarta exatamente esse report.

### 5. Três dos 19 presets de gatilho podem não fazer nada — A CONFIRMAR

Decodificando a nomenclatura de 2020 contra a enum da Sony: `rigid()`,
`simple_rigid()` e `feedback()` mandam `0x05`, que é **OFF**. Ver a
[TRIGGER-CANON-01](../sprints/2026-08-01-TRIGGER-CANON-01-os-modos-de-gatilho-contra-a-enum-da-sony.md).

**Não medido no hardware desta casa** — e a primeira tentativa de medir falhou
por um defeito de instrumento, ver abaixo.

## As três lições de método desta noite

Estas valem mais que os achados, porque impedem os próximos erros.

### Lição 1 — medir contra a ferramenta errada produz alarme convincente e falso

Mediu-se o gamepad virtual pelo SDL e concluiu-se que **só a vibração chegava
ao jogo**. Estava errado: a medição usou a `libSDL2` **2.30.0 do Ubuntu**, que
nenhum jogo da Steam carrega. Contra a **SDL3 3.4.10** que a Steam distribui, o
vpad é enumerado por completo.

A diferença tem causa: o suporte a dispositivos `uhid` entrou no `hidapi`
upstream em 2020 e o SDL3 herdou ao sincronizar em 2023; o SDL2 clássico nunca
sincronizou.

> **Regra que fica:** todo instrumento tem de declarar **qual biblioteca** está
> medindo, com caminho absoluto e revisão.

### Lição 2 — estrutura de dados incompleta corrompe o resultado sem erro nenhum

A primeira medição do SDL usou uma `SDL_hid_device_info` **faltando três
campos**. Isso desloca o ponteiro `next` e a enumeração sai errada **sem
levantar exceção**. O resultado parecia legítimo.

> **Regra que fica:** ao falar com biblioteca C por `ctypes`, conferir a struct
> campo a campo contra o header da versão certa. O SDL3 tem um campo a mais que
> o SDL2 (`bus_type`).

### Lição 3 — o instrumento pode estar brigando com o produto

A tentativa de medir os gatilhos por `test trigger --raw` falhou: com o daemon
vivo, o `--raw` abre um segundo controlador e briga pelo hidraw; o daemon
sobrescreve em ≤ 0,5 s. E a CLI imprime **"trigger aplicado"** de qualquer
jeito.

O mais incômodo: **isso está escrito no próprio código** (`cli/cmd_test.py`,
*"o caminho `--raw` (…) segue direto no hardware"*) e ninguém tinha ligado os
pontos.

> **Regra que fica:** antes de testar uma hipótese, provar que o instrumento
> chega ao alvo. E ferramenta que não aplicou não pode imprimir sucesso.

## O que a pesquisa abriu, por recurso

| recurso | o que se descobriu | sprint |
|---|---|---|
| gatilhos | a enum oficial; o empacotamento em bitmask de zonas; 3 presets possivelmente inertes; a refutação do `FORCA8-01`; a leitura de estado do gatilho | [TRIGGER-CANON-01](../sprints/2026-08-01-TRIGGER-CANON-01-os-modos-de-gatilho-contra-a-enum-da-sony.md) |
| alto-falante | a rota, o pré-amp, e a explicação da curva medida | PARIDADE-SONY-01 + sprint de rota a abrir |
| microfone | caminho chat/ASR, cancelamento de eco e ruído, beam forming, **detecção de jack** (candidata a explicar o gating por BT) | a abrir |
| haptics VCM | por USB são os canais 3-4 da placa de 4 canais; **o bit `HAPTICS_SELECT` que o SDL liga em todo rumble os DESLIGA**; por BT vão pelo túnel do mic | a abrir |
| giroscópio | o vpad se declara Edge (1000 Hz) e entrega 250 — possível escala 4× errada | a abrir |
| touchpad e lightbar | confirmados corretos, inclusive o bit de fade | — |
| vibração | a causa-raiz do rumble preso | JOGO-COMPLETO-01 |
| gamepad virtual | 6 furos, entre eles o nome sem "Wireless Controller" e o byte 53 nunca preenchido (anuncia "fone sempre plugado") | JOGO-COMPLETO-01 |

## O que NÃO se achou, e é honesto dizer

- **O identificador exato da API de áudio do pad no PS5.** A rota existe e está
  documentada no hardware, mas o nome da função no SDK é NDA. **Não inventar.**
- **Nenhuma palestra pública da Sony** descrevendo a API de gatilhos ou haptics.
- **As patentes não ajudam:** descrevem a mecânica do gatilho, não o protocolo.
- **Nenhum jogo de PC usa o microfone do DualSense nativamente** — ele aparece
  como device de captura genérico e a pessoa escolhe à mão.
- **Praticamente não existe jogo de PC que leia giroscópio fora do Steam
  Input** — testar giro exige a camada do Steam ou ferramenta dedicada.

## Bancadas que sobraram prontas

- um dump de capacidades por `ctypes` sobre a `libSDL2`/`libSDL3` já instalada,
  que lista por gamepad o que a API enxerga **e chama de verdade** `SetLED()` e
  `SendEffect()` mostrando o erro. É o teste de maior retorno por esforço, e
  vale virar cheque do `doctor`;
- `libsdl2-tests` (`apt install`) traz `testgamecontroller`, que exercita gyro,
  touchpad, rumble, LED **e gatilho adaptativo** — ciclado pelo botão do
  microfone;
- `SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` esconde o físico e força o
  teste a olhar só o virtual. **Só na linha de comando** — como opção de
  inicialização persistida isso é veneno registrado.
