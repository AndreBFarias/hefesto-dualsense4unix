# ENTREGA-QUE-NÃO-LIGOU-01 — o código que existe e ninguém chama

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA**, e por um motivo que não é o tamanho dos defeitos:
  **três sprints desta casa estão marcadas como entregues e não estão de pé.**
  Enquanto isso não for corrigido, o placar de qualquer índice é ficção
- **Faixa:** 3 — o processo mente sobre si mesmo
- **Causa-raiz:** **PROVADA por `grep` e leitura** nos três casos
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)

---

## O padrão que une os três

> **Cada um destes commits escreveu um artefato, testou o artefato, e nunca
> testou o encontro dele com o resto do sistema.** Os testes passam porque medem
> exatamente o que o commit escreveu — o método, o descritor, a string na regra
> — e nunca perguntam se alguém *chama*, se o dado *sai*, ou se o casador do
> outro lado ainda *casa*.

É a mesma classe do achado de método de 02/08, registrado na
[BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md):
*"um check que filtra só o que é sadio o bastante fica cego na proporção da
gravidade"*.

---

## Defeito 1 — `forward_jack` não tem chamador, e não emitiria se tivesse

**A [BT-E-VPAD-01](2026-08-01-BT-E-VPAD-01-o-que-so-existe-no-cabo-e-os-seis-furos.md)
declara o furo 2 ENTREGUE** (linha 214-218): *"`forward_jack` espelha
`HP_DETECT`, `MIC_DETECT` e `MIC_MUTE` do físico"*. E a mensagem do commit
`5801de9` afirma que o byte *"passou a acompanhar o físico"*.

**Medido em 03/08 — o `grep` na árvore inteira:**

```
src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:1378:  def forward_jack(...)   <- a definição
tests/unit/test_bt_e_vpad_01.py:190:   pad.forward_jack(0b101)                        <- teste
tests/unit/test_bt_e_vpad_01.py:207:   pad.forward_jack(0xFF)                         <- teste
docs/.../BT-E-VPAD-01...md:216                                                        <- a sprint
```

**Nenhum chamador em produção.** O byte 53 do vpad continua saindo
`_STATUS1_NEUTRO = 0x00` para sempre — que é **exatamente** o defeito que o furo
2 foi curar, e cujo custo a referência canônica descreve: o vpad anuncia *"fone e
microfone sempre plugados"*, o pior default possível para o caso do
alto-falante.

### E há um segundo furo, dentro do primeiro

`integrations/uhid_gamepad.py:1394-1397`:

```python
novo = int(status1) & _STATUS1_BITS_CONHECIDOS
if novo == self._status1_byte:
    return
self._status1_byte = novo          # <-- e acabou
```

Compare com o irmão `forward_battery` (`:1399-1414`), que termina em
`self._emit_if_changed()`.

**A docstring do `forward_jack` afirma:** *"Segue o desenho do `forward_battery`:
sai cedo quando nada muda, para não sujar o caminho de emissão com report
idêntico."* **Não segue.** Mesmo com chamador, o byte esperaria outro report
mudar para sair.

### Por que os testes passam

`tests/unit/test_bt_e_vpad_01.py:180` declara a mordida:
*"Mordida: apagar a linha `body[_STATUS1_OFFSET] = ...` do `_encode_body`."*

O teste trava que o **`_encode_body` usa** o `_status1_byte`. Correto e
insuficiente: ele não trava que alguém **chame** `forward_jack`, nem que o
report **saia**. É uma mordida na metade errada da cadeia.

---

## Defeito 2 — `DESLIGADO_OFICIAL` foi criado e nunca usado; "Desligar" pode não desfazer

> ### MEDIDO EM 05/08/2026 — A PARTE GRAVE FOI REFUTADA
>
> **"Desligar" DESFAZ "Rígido".** A E2 fez o que devia: impediu que se
> escrevesse código sobre uma suspeita que o fio não confirma.
>
> Medido com a mão dela, no controle por USB, com o daemon vivo e **tudo pelo
> IPC** (`trigger.set`, nunca `--raw` — o instrumento que briga com o produto):
>
> | passo | o que foi ao fio | o tato dela |
> |---|---|---|
> | `Rigid` posição 0, força 255 | `0x21` + as dez zonas ativas | *"duro"* |
> | `Off` | **`0x00`** | *"soltou"* |
>
> **O `0x00` é um OFF que o firmware honra.** O passo C (mandar `0x05` por
> `Custom`, que o IPC aceita) ficou dispensado: não havia mais o que decidir.
>
> **O que CAI:** a suspeita de que "Desligar" não desfaz — e com ela a urgência
> desta seção.
>
> **O que CONTINUA VÁLIDO:**
>
> - **`DESLIGADO_OFICIAL = 0x05` segue órfão** (definido, zero uso em `src/`).
>   Vira dívida de símbolo morto — que é exatamente o que a **E5** desta sprint
>   já propõe portar. A E5 não muda;
> - **o agravante 1 é o que sobrou de grave:** não há reset de gatilho ao
>   desconectar nem ao parar o daemon. Um controle que cai fica com o gatilho no
>   estado em que estava, e por Bluetooth isso é rotina.
>
> **E a medição pagou uma dívida de OUTRA sprint:** o agravante 3 dizia que *"os
> bytes novos nunca foram sentidos"*, e a `TRIGGER-CANON-01` fechou pedindo
> justamente isso (*"o próximo passo honesto é ela sentir os sete presets
> curados… este é o aceite que falta"*). **O `Rigid` curado endureceu no fio.
> O aceite está pago.**
>
> **E rendeu um defeito novo, achado ao restaurar o perfil dela:**
> [TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md)
> — e ele é da MESMA família desta sprint: mais uma entrega declarada
> (`SOM-02/E4`) que a ordem do código impedia de acontecer.
>
> Nota de proveniência: a referência canônica lista `0x05 = Off (oficial)` e
> **não listava o `0x00`**. Passou a listar, com grau **MEDIDO AQUI**
> (`docs/protocol/dualsense-referencia-canonica.md` §4).

**Nasceu no commit `36caa11`** (os sete presets de gatilho curados).

`core/trigger_effects.py:109` acrescentou:

```python
DESLIGADO_OFICIAL = 0x05
#: O OFF que o firmware entende no bloco de gatilho. Distinto do `0x00`
```

**Medido em 03/08:** o símbolo aparece em **três** lugares — a definição, e dois
`assert` em `tests/unit/test_trigger_canon_01.py:126-127`. **Zero uso em
`src/`.**

Todo caminho de desligar continua mandando `0x00`: `off()`
(`trigger_effects.py:300-301`), `trigger.reset`
(`daemon/ipc_handlers.py:669-671`), o release do Modo Nativo
(`daemon/lifecycle.py:918-921`), o fim de sessão de jogo
(`core/backend_pydualsense.py:3108-3115`).

E a tabela canônica lista `0x05 = Off (oficial)` e **não lista `0x00`**
(`docs/protocol/dualsense-referencia-canonica.md:224`).

### Por que isso nunca custou nada antes — e por que custa agora

Antes de `36caa11`, `rigid()` mandava `0x05`, que **era** OFF. O gatilho nunca
endurecia; mandar `0x00` para desligar nunca precisou funcionar.

**Agora `rigid()` manda `0x21` com zonas ativas de verdade.** Se `0x00` não for
o OFF que o firmware entende, "Desligar" não desfaz o que "Rígido" fez.

**Grau: SUSPEITA COM MECANISMO.** A divergência plano×entrega está provada por
leitura; a semântica do fio exige a mão dela.

### Três agravantes, todos verificados

1. **Não existe reset de gatilho ao DESCONECTAR nem ao parar o daemon.**
   `core/backend_pydualsense.py:3070-3072` sai cedo com `handle is None`, e não
   há `set_trigger(off)` no shutdown — só `force_rumble_stop`. **Um controle que
   cai do Bluetooth fica com o gatilho no estado em que estava.** Com quatro
   controles caindo o tempo todo, isso é rotina;
2. **É broadcast quando o seletor está em "Todos"** — um clique endurece os
   quatro (ver a [POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md));
3. **Os bytes novos nunca foram sentidos.** A própria TRIGGER-CANON-01 fecha
   dizendo: *"o próximo passo honesto é ela sentir os sete presets curados…
   Este é o aceite que falta"* (linhas 396-400). A medição de 01/08 validou os
   bytes **velhos**.

---

## Defeito 3 — o rename do vpad quebrou a regra udev 78 e cegou o doctor

**Nasceu no commit `5801de9`** (o furo 1 da BT-E-VPAD-01, o nome do vpad).

O nome virou `DualSense Wireless Controller (Hefesto P{n})`
(`integrations/uhid_gamepad.py:876`) e vai direto para o `UHID_CREATE`
(`:1174`). O `hid-playstation` deriva o nó de sensores como
`<nome> Motion Sensors`.

**Dois consumidores casam pelo nome ANTIGO — medido em 03/08:**

```
assets/78-dualsense-motion-not-joystick.rules:20
    ATTRS{name}=="Hefesto Virtual DualSense P* Motion Sensors"      <- não casa mais

scripts/doctor.sh:2478
    alvo = ($0 ~ /Hefesto Virtual DualSense P[0-9]+ Motion Sensors/)  <- não casa mais
```

E as outras linhas da regra 78 não cobrem o buraco: a linha 18 casa
`"DualSense Wireless Controller Motion Sensors"` **exato**, e o nome novo tem
`(Hefesto P1)` no meio.

**Consequências:**

- **a rede que zera `ID_INPUT_JOYSTICK`** nos nós de sensores dos vpads caiu.
  *Honestidade:* o comentário da própria regra (linhas 12-16) diz que o builtin
  `input_id` do kernel atual já classifica certo e que estas linhas são **defesa
  em profundidade**. O impacto visível hoje é a perda da rede, não
  necessariamente joysticks fantasmas — mas com quatro vpads em co-op é
  justamente onde a rede mais valia;
- **`check_vpad_motion` do doctor virou falso alívio**: passa a imprimir
  *"nenhum nó Motion de vpad agora (emulação desligada…)"* com a emulação
  ligada. **É o mesmo padrão do `check_bt_sdp_cache_envenenado` que deu `[ OK ]`
  no meio do defeito**, e que esta casa já registrou como lição de método.

### Por que a suíte não pegou

- `tests/unit/test_udev_kernel07_path06.py:88` afirma que **a string** está no
  arquivo de regras — a string continua lá, apenas não casa mais nada;
- `tests/unit/test_doctor_vpad_motion.py:51-61` alimenta um
  `/proc/bus/input/devices` **falso, com o nome antigo**.

**Nenhum dos dois deriva o nome de `UhidDualSense.name`.** Os dois ficam verdes
para sempre.

---

## As entregas

### E1 — `forward_jack` ganha chamador e emissão

Duas coisas, e as duas são necessárias:

1. `forward_jack` termina em `self._emit_if_changed()`, como o irmão que a
   docstring diz seguir;
2. alguém o chama. O dado (byte 53 do report de entrada do físico) está **fora**
   da janela de motion (15..39), então precisa de caminho próprio — e o
   precedente existe: é o mesmo que foi feito para o **clique do touchpad**
   (`core/physical_report_reader.py:265`, `extract_touchpad_click`).

**Aceite:** plugar e desplugar o fone no controle muda o byte 53 do vpad.
Medível sem hardware com um report de entrada sintético.

**A mordida que faltava, e ela é a entrega de método:** um teste que afirme que
**o report SAI** — que o `_encode_body` emitido depois de um `forward_jack`
chegou ao `UHID_INPUT2`. Um teste que só afirma que o campo foi montado não
distingue "entregue" de "escrito e engavetado".

### E2 — decidir o byte do OFF, e usá-lo em toda a árvore

**A medição vem antes** (dez segundos, com a mão dela):

> Aplicar "Rígido" com força alta em L2. Sentir. Aplicar "Desligado". Sentir de
> novo.
> - **o gatilho soltou** ⇒ `0x00` funciona; o `DESLIGADO_OFICIAL` vira nota
>   datada explicando por que não é usado;
> - **o gatilho continua duro** ⇒ trocar `off()` para `DESLIGADO_OFICIAL` é uma
>   linha, e os quatro caminhos de desligar passam a usá-la.

**Aceite:** `Desligar` desfaz `Rígido`, pelo tato dela.

### E3 — o gatilho é solto quando o controle sai

Independente da E2: **um controle que cai não pode ficar com o gatilho armado.**
Hoje `core/backend_pydualsense.py:3070-3072` sai cedo quando o handle já morreu
— e é justamente aí que a ordem precisava ter saído.

O ponto certo é **antes** de fechar o handle (`_close_handles`,
`core/backend_pydualsense.py:1449`), não depois.

**Aceite:** desligar o controle com "Rígido" aplicado e religá-lo → o gatilho
está solto. **Esta é a entrega que mais aparece com quatro controles no
Bluetooth**, porque cair é rotina.

### E4 — os dois casadores por nome passam a derivar do código

**A regra:** nenhum consumidor casa o nome do vpad por literal digitado à mão.

- `assets/78-dualsense-motion-not-joystick.rules:20` passa a casar um padrão que
  cubra o nome atual (`*Hefesto P* Motion Sensors` cobre os dois formatos, o
  antigo e o novo — e um instalador que não regenere regras continua funcionando);
- `scripts/doctor.sh:2478` idem.

**E o teste que morde, que é o valor real da entrega:** um teste que **derive**
o nome de `UhidDualSense(player=1).name`, monte `<nome> Motion Sensors` e afirme
que a regra 78 e o awk do doctor **casam essa string**. Trocar o nome do vpad
passa a reprovar os dois na hora.

Hoje os dois testes existentes travam literais — e por isso o rename passou.

### E5 — o portão contra a classe inteira

Os três defeitos têm a mesma assinatura: **símbolo público definido em `src/` e
nunca referenciado por `src/`**.

Um portão barato, no espírito dos que a casa já tem: varrer os símbolos públicos
de `integrations/` e `core/` e reprovar quando um método/constante **nascido
nesta leva** só tenha referências em `tests/`.

**Cuidado obrigatório, senão o portão vira ruído:** há símbolos legitimamente
sem chamador (API de plugin, escape hatch como `custom()`, código chamado por
reflexão). O portão precisa nascer com uma **lista de dispensas nomeada e
datada** — dívida com nome, no modelo do `PENDENCIA_DO_SANITIZADOR` que já existe
em `tests/unit/test_versao_publicada_data_e_paginas_de_uso.py`.

**Aceite:** o portão, rodado contra a árvore de 02/08, **acha o `forward_jack` e
o `DESLIGADO_OFICIAL`**. Se não achar, ele não serve.

---

## Testes que vão reprovar

```
pytest tests/unit -k "uhid or trigger_canon or udev or doctor_vpad or bt_e_vpad"
```

## O que NÃO fazer

- **Não marcar o furo 2 da BT-E-VPAD-01 como entregue de novo** sem a E1
  completa (chamador **e** emissão). A sprint já o declarou uma vez;
- **Não trocar `off()` para `0x05` sem a medição da E2.** `0x00` pode estar
  certo — e trocar às cegas é a mesma pressa que criou o símbolo não usado;
- **Não voltar o nome do vpad para o antigo** para "consertar" a regra 78. O
  nome novo existe porque jogos casam por `Wireless Controller`, e isso foi
  medido (furo 1);
- **Não fazer o portão da E5 sem lista de dispensas.** Um portão que reprova o
  legítimo é desligado na primeira semana, e aí não protege nada.

## O que fica ABERTO

- **o aceite dela nos sete presets curados** — pendência herdada da
  TRIGGER-CANON-01, que a E2 aproveita;
- **quantos outros símbolos órfãos existem** — a E5 responde ao ser escrita, e o
  número é o dado interessante.
