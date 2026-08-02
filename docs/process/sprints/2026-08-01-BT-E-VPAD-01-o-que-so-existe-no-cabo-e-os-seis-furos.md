# BT-E-VPAD-01 — o que só existe no cabo, e os seis furos do gamepad virtual

- **Status:** PROPOSTA, escrita em 01/08/2026 para sobreviver à queda da sessão
- **Prioridade:** ALTA para os dois defeitos de Bluetooth (ela os encontrou
  usando); MÉDIA para os furos
- **Índice:** [O controle inteiro no jogo](2026-08-01-INDICE-o-controle-inteiro-no-jogo.md)
- **Referência:** [o protocolo canônico](../../protocol/dualsense-referencia-canonica.md)

## A hipótese dela, confirmada por medição

Com o controle no Bluetooth, ela notou que a lightbar estava apagada e que o
botão do microfone não obedecia. E disse:

> *"engraçado que os gatilhos funcionam no BT. Talvez algo não esteja pareado
> pra tudo funcionar via BT — cada uma das features esteja setada pra funcionar
> só via cabo, o que é um erro de design nosso."*

**Está certa.** Esta casa já tem isso registrado com nome: *"a premissa
USB-é-o-mundo"*, listada como bug recorrente. Os dois defeitos abaixo são duas
instâncias novas dela.

## Defeito 1 — o botão do microfone alterna o microfone ERRADO no Bluetooth

**Medido em 01/08:** com o controle no BT, `pactl list short cards | grep -i
dualsense` devolve **zero**. No Bluetooth o DualSense **não tem placa de som
nenhuma** — o áudio vai dentro dos reports HID e depende da ponte deste projeto
(que é opt-in e estava desligada).

O código do botão (`daemon/subsystems/hotkey.py`, `mic_button_loop`) faz:

```python
muted = await daemon._run_blocking(audio.toggle_default_source_mute)
await daemon._run_blocking(daemon.controller.set_mic_led, muted)
```

Ou seja: alterna o mudo da **fonte padrão do sistema** e acende o LED do
controle para refletir esse estado. **No cabo isso funciona** porque a fonte
padrão é o próprio controle. **No Bluetooth a fonte padrão é outra coisa** —
nesta máquina, o microfone da placa-mãe.

**A prova no log**, três toques dela:

```
20:15:54  mic_hotkey_toggle  muted=True
20:16:31  mic_hotkey_toggle  muted=True
20:16:43  mic_hotkey_toggle  muted=True
```

Sempre `True`, porque não é o microfone do controle que está sendo alternado.

**A cura tem de decidir o que o botão significa**, e são três opções com preços
diferentes:

- **(a)** o botão só age quando a fonte padrão **é** o controle; fora disso,
  não mexe em nada e o LED não mente. É a mais honesta e a mais barata;
- **(b)** o botão passa a mutar o **registrador do firmware** (o
  `power_save_control` bit4), que existe nos dois transportes — mas isso **toma
  a posse** e o botão físico para de valer, que é o oposto do que ela espera de
  um botão físico;
- **(c)** no Bluetooth, o botão comanda a **ponte de mic por BT**, se ela
  estiver de pé.

**Aceite:** com o controle no BT, apertar o botão do mic ou faz algo verdadeiro
no microfone do controle, ou não faz nada — nunca muta outro dispositivo.

## Defeito 2 — a lightbar apagada no Bluetooth

**Medido no mesmo log:**

```
lightbar_reset_enviado    key=a0:fa:9c:00:00:f0
sysfs_led_cobertura       cobertos=[]  sem_no_sysfs=['a0:fa:9c:00:00:f0']
```

O daemon manda o reset de LED e **acredita ter aplicado** — o `state_full`
reporta `lightbar_rgb: [255,128,0], on: True, source: desired`. A luz está
apagada.

A pista está na segunda linha: **no Bluetooth o LED não tem nó em sysfs**. O
caminho de escrita por sysfs, que é o normal no cabo, não existe ali — e o
caminho por report HID (que funciona, como os gatilhos provam) ou não está
sendo usado, ou está sendo desfeito.

**Contexto que esta casa já tem**, e que precisa ser relido antes de mexer:
`LIGHTBAR-BT-ADOPT-01`, `LIGHTBAR-BT-RESET-01`, `LIGHTBAR-BT-RESET-03` e
`LIGHTBAR-BT-KEEPALIVE-01` — todos em `core/backend_pydualsense.py`, todos
provados ao vivo em 17-22/07. **A cura não pode desfazer nenhum deles.**

**A primeira entrega é diagnóstica, não corretiva:** descobrir se o report de
cor está sendo escrito no BT e sendo ignorado, ou se não está sendo escrito.
São duas causas diferentes com curas opostas.

**Aceite:** com o controle no BT, aplicar uma cor na aba Lightbar acende o LED —
ou a tela diz por que não pode.

## Defeito 3 — a tela mente sobre a lightbar

Independente da causa acima: o `state_full` diz `source: desired` e a GUI mostra
a cor aplicada, com o rodapé escrevendo *"Cor aplicada no controle (100% de
brilho)"*. **Isso é afirmar o que não se mediu** — a mesma família da
`APLICAR-VERDADE-01`.

**Cura:** `desired` significa "mandamos", não "está aceso". A tela precisa
distinguir os dois, como o rodapé aprendeu a fazer com as seções do perfil.

## Os seis furos do gamepad virtual

Levantados em 01/08 cruzando o que os jogos esperam com o que o vpad entrega.

### Furo 1 — o nome não contém "Wireless Controller"

O vpad se chama `Hefesto Virtual DualSense P1`. Sob Proton esse nome vira o
`FriendlyName` do lado Windows, e **jogos casam por essa substring** para achar
o controle e o device de áudio.

Incoerência interna: o fallback uinput **acerta**
(`Sony Interactive Entertainment DualSense Edge Wireless Controller`), o uhid
não.

**Cura barata:** `DualSense Wireless Controller (Hefesto P1)` — mantém a
distinção humana e contém a substring. O `phys` (`hefesto-vpad`) e o `uniq`
(MAC forjado) continuam sendo o discriminador real do daemon, então nada quebra.

### Furo 2 — o byte 53 nunca é escrito

`_encode_body` escreve o byte 52 (bateria) e **nunca o 53**, que carrega
`HP_DETECT`, `MIC_DETECT` e `MIC_MUTE`.

Com zero fixo, **o vpad anuncia "fone e microfone sempre plugados"** — e esse é
o **pior default possível** para o caso do alto-falante que ela quer: um jogo
que só roteia som para o alto-falante quando não há fone vai achar que sempre
há.

**Cura:** espelhar o byte 53 do físico. O dado está fora da janela de motion
(15..39), então precisa de caminho próprio — igual ao que já foi feito para o
clique do touchpad.

### Furo 3 — os bytes de áudio do jogo são descartados em silêncio

O `_replicate_from_output` replica quatro categorias (gatilhos, lightbar,
player-LEDs) e ignora os sete campos de áudio. Ver a
[PARIDADE-SONY-01](2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md),
que trata disso com portão de medição.

### Furo 4 — o PID do Edge é invisível para uma classe de jogos

O vpad usa `0x0DF2` (Edge) para desduplicar do físico. Jogos que fixam
`0x0CE6` (o DualSense comum) **não o reconhecem** — é um defeito documentado no
hardware real do Edge também.

**Não é argumento para voltar a `0x0CE6`** (o motivo do Edge continua válido),
mas é um limite que precisa estar **documentado** e, idealmente, configurável
por perfil.

### Furo 5 — o vpad se declara Edge e entrega a taxa do comum

O SDL, ao ver um Edge por USB, anuncia giroscópio a **1000 Hz**. O espelho
entrega os ~250 Hz do físico. Um jogo que integre velocidade angular pela taxa
declarada teria **escala 4× errada** na mira por movimento.

**Não medido.** Verificação barata: comparar a taxa que o SDL reporta com a
medida.

### Furo 6 — a causa-raiz do rumble preso

Está documentada na
[referência canônica](../../protocol/dualsense-referencia-canonica.md), §8, com
o discriminador exato que separa "parada do SDL" de "report de gatilho". O
comentário no código diz *"isto é MITIGAÇÃO, não a cura"* — a cura existe agora.

## Testes que vão reprovar

`pytest tests/unit -k "lightbar or mic or hotkey or uhid or replica"`.

Atenção aos que travam as curas de BT já pagas (`LIGHTBAR-BT-*`) — elas foram
provadas ao vivo e **não podem ser desfeitas** por esta leva.

## O que NÃO fazer

- **Não desfazer as curas de lightbar por BT** de 17-22/07. Releia os quatro
  comentários antes de tocar.
- **Não fazer o botão do mic tomar a posse do registrador** sem decidir
  explicitamente — é o oposto do que se espera de um botão físico.
- **Não voltar o PID para `0x0CE6`** sem resolver a desduplicação.
- **Não medir taxa de giroscópio contra a `libSDL2` do sistema.** Ver a lição
  de método no estudo de 01/08.
