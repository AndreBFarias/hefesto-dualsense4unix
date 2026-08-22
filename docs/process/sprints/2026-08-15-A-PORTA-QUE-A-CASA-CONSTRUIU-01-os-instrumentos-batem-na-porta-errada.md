# A-PORTA-QUE-A-CASA-CONSTRUIU-01 — os instrumentos batem na porta errada

- **Estado:** CONCLUÍDA — a porta está declarada em
  `integrations/hidraw_broker_client.py:150` e usada por toda a bancada
  (`scripts/ensaios/comum.py`, `censo_features.py:201`, `capture_blueprint.py`,
  `record_hid_capture.py`, `doctor.sh`, `disable_steam_input.sh`), com portão em
  `tests/unit/test_a_porta_que_a_casa_construiu_01.py` e uso ao vivo no cabeçalho
  de `docs/data/ensaios-brutos/2026-08-15-E1-corpo-do-0x32.txt`
  (verificado em 21/08/2026)
- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf`.
- **Grau:** **MEDIDO** na máquina dela, agora, com os quatro controles ligados —
  **dois no cabo e dois no rádio**, que é a configuração do ENSAIO 2+2 que ela
  pediu às 04:20.
- **Depende de:** nada. É pré-requisito de **todo** ensaio que toque o aparelho,
  inclusive o 2+2.
- **Custo mínimo:** 2 h 25
- **Urgência:** esta é a única sprint da leva que **bloqueia o que ela vai fazer
  em seguida**.

---

## 1. O defeito, medido agora

Nenhum dos quatro DualSense **físicos** pode ser aberto por um processo dela. Os
quatro gamepads **virtuais** podem.

```
hidraw4   mode=660  ACL user:vitoriamaria:rw-   0003:054C:0DF2   (Hefesto P1)
hidraw7   mode=660  ACL user:vitoriamaria:rw-   0003:054C:0DF2   (Hefesto P2)
hidraw9   mode=660  ACL user:vitoriamaria:rw-   0003:054C:0DF2   (Hefesto P3)
hidraw11  mode=660  ACL user:vitoriamaria:rw-   0003:054C:0DF2   (Hefesto P4)

hidraw6   mode=600  SEM ACL   0003:054C:0CE6  usb3/3-2/3-2:1.3   ← físico, CABO
hidraw10  mode=600  SEM ACL   0003:054C:0CE6  usb3/3-3/3-3:1.3   ← físico, CABO
hidraw5   mode=600  SEM ACL   0005:054C:0CE6  uhid               ← físico, RÁDIO
hidraw8   mode=600  SEM ACL   0005:054C:0CE6  uhid               ← físico, RÁDIO
```

Consequência direta, medida hoje por dois agentes diferentes:

- `scripts/capture_blueprint.py` falha com
  `'/dev/hidraw8' inacessível ([Errno 13] Permission denied)`;
- o censo dos dezessete feature reports **não pôde ser feito** pela primeira
  frente que tentou;
- a leitura da cor (`0x80`/`0x81`) esbarra na mesma porta.

---

## 2. A causa NÃO é a que parecia, e a diferença importa muito

**A leitura fácil — e um relatório de agente de hoje a fez — é que a regra udev
não cobre o Bluetooth.** Está errada, e mandaria consertar o lugar errado.

`assets/70-ps5-controller.rules` está **instalada e idêntica à árvore**
(`diff` limpo contra `/etc/udev/rules.d/70-ps5-controller.rules`), e a regra
**pegou**:

```
udevadm info -q all -n /dev/hidraw6
E: TAGS=:seat:uaccess:
E: CURRENT_TAGS=:seat:uaccess:
```

A etiqueta está lá. O nó está `0600` sem ACL mesmo assim.

**Quem tira é o próprio Hefesto, de propósito.** `broker/hidraw_broker.py:417-425`:

> *"`setfacl -b` + `chmod 0600` → só root abre. Fd já aberto sobrevive."*

É o `hide` — o mecanismo que **esconde o controle físico do Steam Input e do
jogo**, para que o jogo veja só o vpad. O `restore` (`:430-436`) devolve
`chmod 0660` + `ACL u:<uid>:rw`.

**Não é bug. É o produto funcionando.** E a casa **já construiu a porta**: o
broker devolve um descritor `O_RDWR` do nó escondido, por `SCM_RIGHTS`, no socket
`/run/hefesto-hidraw-broker/broker.sock` — `srw-rw---- root:vitoriamaria`,
serviço `active`.

**O defeito é que os instrumentos não usam a porta.**

---

## 3. Quem bate na porta errada

Instrumentos que abrem `/dev/hidraw*` direto:

| arquivo | o que ele faz |
|---|---|
| `scripts/capture_blueprint.py` | captura o `0x20` que forja os vpads — **falha hoje** |
| `scripts/record_hid_capture.py` | grava tráfego HID |
| `scripts/ensaio_rumble_um_bit_por_vez.py` | a bancada do rumble |
| `scripts/ensaio_o_keepalive_mata_o_rumble.py` | a dose-resposta de 11/08 |
| `scripts/doctor.sh` | diagnóstico |
| `scripts/disable_steam_input.sh` | — |

**Os dois `ensaio_*` são a bancada dela.** Eles funcionaram em 11/08 porque
naquele dia o controle não estava escondido. Com a mesa cheia e o co-op ligado —
que é o estado normal de agora — eles medem `EACCES` e param.

**E é o mesmo modo de falha do EVIOCGRAB**, um andar abaixo: o co-op também
esconde o **evdev** físico (grab exclusivo), medido em dois ensaios hoje. Um
instrumento ingênuo lê zero evento e conclui que o aparelho está calado. Nos dois
casos o produto está certo e o instrumento é que fala com o nó errado.

---

## 4. As três entregas

| # | entrega | custo |
|---|---|---|
| **E1** | **Um cliente do broker, um só, importável** — abre pelo socket, cai para `open()` direto quando o broker não existe, e **diz qual dos dois usou** no cabeçalho do relatório | 55 min |
| **E2** | **Os seis instrumentos passam a usá-lo.** Nenhum abre `/dev/hidraw*` por conta própria | 60 min |
| **E3** | **O instrumento declara a porta e o estado do grab** no cabeçalho, ao lado da biblioteca que já declara. Hoje ele declara com que biblioteca mede e não declara se o que ele mede está escondido | 30 min |

**A E3 é a que fecha a família.** A regra desta casa é *"todo instrumento tem de
declarar qual biblioteca está usando"* — porque medir contra a biblioteca errada
produz alarme convincente e falso. **O mesmo vale para a porta:** medir no nó
escondido produz zero convincente e falso.

**A E1 já está prevista** no índice da leva da cor e do som (ONDA 1, item 1.8 —
*"Pôr o caminho do broker dentro dos instrumentos"*). Esta sprint dá a ela o
defeito medido e as mordidas.

---

## 5. O teste que MORDE

Arquivo novo, `tests/unit/test_a_porta_que_a_casa_construiu_01.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — o instrumento que abre o nó escondido (é a principal)

**Arrancar:** deixar um instrumento chamando `open("/dev/hidrawN")` direto.

**Por que reprova:** o teste varre `scripts/` procurando abertura literal de
`/dev/hidraw` fora do cliente do broker e cobra que cada ocorrência esteja numa
lista de exceções **com motivo**. `scripts/install_udev.sh` e
`scripts/install-host-udev.sh` são exceções legítimas (escrevem a regra, não
abrem o nó) e nascem na lista.

Esta é a principal porque é a que impede o próximo instrumento de nascer cego.

### Mordida 2 — a queda silenciosa para `open()` direto

**Arrancar:** fazer o cliente cair para `open()` sem dizer.

**Por que reprova:** o teste dá um socket de broker inexistente e exige que o
relatório do instrumento **contenha a palavra que declara a porta usada**. Um
fallback silencioso é pior que a falha: ele produz uma medição que parece boa e
não diz que mediu por um caminho diferente do outro braço do ensaio — que é
exatamente o que o desenho 2+2 existe para impedir.

### Mordida 3 — o zero que vem do grab, não do aparelho

**Arrancar:** deixar um instrumento de evdev reportar "0 eventos" sem checar o
grab.

**Por que reprova:** o teste simula o `EVIOCGRAB` do co-op sobre o nó físico e
exige que o instrumento **distinga** *"o controle não emitiu"* de *"eu não posso
ler"*. Hoje as duas coisas saem como zero.

### O que estes testes NÃO provam

Que o broker devolve o fd certo. Isso já tem dono e teste próprios — o que estas
mordidas provam é que os instrumentos **pedem** por ali.

---

## 6. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **Nada.** Não muda comportamento de produto, não muda pixel, não escolhe entre dois caminhos | as três entregas e as três mordidas |

**Só uma ressalva de escopo, e ela é de coordenação, não de decisão:** há um
agente escrevendo `scripts/ensaios/` **agora**. A E2 tem de esperar essa leva
fechar, ou os dois vão editar o mesmo diretório.

---

## 7. Duas dívidas irmãs que ficam registradas

1. **`primary_grab_state: "failed"` com o vpad de pé = input DOBRADO para o P1.**
   Medido hoje: `evdev_grab_failed err='[Errno 16] Dispositivo ou recurso está
   ocupado' path=/dev/input/event265`. Se o grab do primário falha e o vpad
   sobe assim mesmo, o jogo recebe **os dois** — o físico e o virtual. É a
   **D-29** do índice da leva, e não tem sprint. **Não é desta frente**, mas é da
   mesma família: o produto esconde e alguém não fica escondido.

2. **`integrations/uhid_blueprint.py` fossiliza `hw_version = 0x0710`** em todo
   vpad — o `hardware_version` de **uma** unidade específica dela. Já está
   registrado no índice da leva (§12.1) e continua sem dono. Vira defeito no dia
   em que alguém usar `hardware_version` como chave de diagnóstico — que é
   exatamente o uso que o censo de hoje recomenda para os **físicos**.
