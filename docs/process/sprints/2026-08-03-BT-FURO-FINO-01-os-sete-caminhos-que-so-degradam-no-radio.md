# BT-FURO-FINO-01 — os sete caminhos que só degradam no rádio

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** ALTA para os defeitos 1 e 2; MÉDIA para o resto
- **Faixa:** 1 (defeitos 1-3) e 2 (defeitos 4-7)
- **Causa-raiz:** **PROVADA no código** nos sete
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Irmã da:** [BT-SURDO-01](2026-08-03-BT-SURDO-01-o-controle-parado-no-radio-nao-recebe-ordem.md) —
  aquela é o acoplamento estrutural; **esta é a lista dos furos finos**, cada um
  pequeno, todos na mesma direção: *o caminho foi escrito quando "o transporte"
  era o cabo e "o controle" era um só*

---

## Defeito 1 — o espelho de motion aceita o pacote de ÁUDIO como se fosse input

**O mais grave da sprint.** `core/physical_report_reader.py:236-245`:

```python
if report[0] == INPUT_REPORT_BT:
    if len(report) != INPUT_REPORT_BT_SIZE:
        return None
    crc = int.from_bytes(report[-4:], "little")
    if bt_crc32(report[:-4], seed=BT_INPUT_CRC_SEED) != crc:
        return None
    return _BT_STRUCT_BASE          # <-- e pronto
```

**Não testa o bit1 de `report[1]`** — o flag que diz *"este pacote é ÁUDIO, não
input"*.

O pacote de áudio do microfone tem **o mesmo report id (`0x31`), o mesmo tamanho
(78 bytes) e CRC válido**. Logo `extract_motion_window` entrega **bytes de Opus
como giroscópio, acelerômetro, `sensor_timestamp` e pontos de toque**, e
`extract_touchpad_click` lê um quadro Opus como clique de touchpad.

### A prova de que a disciplina existe e não foi replicada

O irmão, `integrations/dualsense_bt_audio.py:262-266`, **faz** a checagem:

```python
return (
    len(raw) == INPUT_REPORT_BT_SIZE
    and raw[0] == INPUT_REPORT_BT
    and bool(raw[1] & INPUT_FLAG_AUDIO)      # <-- o bit que falta do outro lado
)
```

E define a constante com o comentário certo (`:186-189`): *"bit0 = o pacote traz
o estado de input; bit1 = o pacote traz um quadro de áudio do microfone"*.

**Duas metades do mesmo protocolo, no mesmo repositório, com disciplinas
diferentes.**

### E isso explica o que JÁ funcionava

A ponte de microfone por Bluetooth é **opt-in e nasce desligada**
(`daemon/lifecycle.py:188`, `bt_mic_enabled: bool = False`). Sem ela, nenhum
pacote de áudio existe no fio — o caminho nunca foi exercitado.

**Consequência:** no dia em que ela ligar o microfone por BT, ~100 pacotes/s de
Opus viram sticks, botões, giroscópio e cliques de touchpad **daquele jogador**.

### Cura, e ela é uma linha

`_struct_base` recusa o report quando `report[1] & INPUT_FLAG_AUDIO`. A
constante já existe; falta importá-la.

**Aceite:** um report `0x31` com o bit de áudio ligado e CRC válido devolve
`None` em `extract_motion_window` e `extract_touchpad_click`. Medível sem
hardware.

**A mordida:** montar um pacote de áudio sintético com CRC válido e afirmar que
o motion o **recusa**. Arranque o filtro e veja o teste reprovar.

> **Registro para quem for além:** o `dualsense_parse_report` do DKMS desta
> máquina (`hid-playstation.c`) também confere só id/tamanho/CRC antes de seguir
> para `&data[2]`. Se isso se confirmar, o **kernel** injeta o mesmo lixo no
> evdev, e aí é patch de módulo, não deste projeto. **Não medido aqui** — fica
> como pergunta, não como fato.

---

## Defeito 2 — sem nó em sysfs, a lightbar e os player-LEDs não têm caminho nenhum, e a falha é silenciosa

`core/backend_pydualsense.py:1789-1795` marca
`handle._suppress_leds = (key in mapping or transport == "bt")` — **no
Bluetooth a supressão é incondicional** (`LIGHTBAR-BT-NEVER-01`, e ela está
certa).

Sob supressão, `_build_common` (`:706-716`, `:756-762`) apaga
`LIGHTBAR_CONTROL_ENABLE|PLAYER_INDICATOR_CONTROL_ENABLE` do flag1, apaga o
`SETUP|BRIGHTNESS` do flag2 e deixa `common[41..46]` zerados.

**Mas o *fallback* de `_for_each_led` (`:2065-2068`) e de
`_write_partial_output` (`:2135-2143`) é justamente
`handle.light.setColorI(...)` / `playerNumber`** — que sob supressão **nunca sai
do processo**.

**Não há exceção, não há log, e o campo é gravado no `_desired`: o daemon
responde "ok".**

Basta um controle ficar fora do mapa de sysfs — nó ainda não registrado, ou
`multi_intensity` sem permissão (`core/sysfs_leds.py:81-88`) — para ele ficar
**sem cor e sem número de jogador, em silêncio**.

**É o mecanismo exato por trás da "hipótese 1" que a
[LIGHTBAR-BT-CLAIM-01](2026-08-02-LIGHTBAR-BT-CLAIM-01-a-barra-apagada-com-o-sysfs-certo.md)
deixou aberta** (`sem_no_sysfs=[...]`) e do defeito 3 da `BT-E-VPAD-01` (*"a tela
mente"*): o `desired` é gravado num caminho que não existe.

**Cura:** o fallback suprimido **loga e devolve falha**, em vez de sumir. Quem
chamou precisa saber que não escreveu.

**Aceite:** com o controle fora do mapa de sysfs no BT, `led.set` **não**
responde "ok" — responde que não há caminho, e a tela diz por quê.

**O que NÃO fazer:** afrouxar a supressão. Ela é uma das assimetrias
intencionais (`LIGHTBAR-BT-NEVER-01`), paga com a barra latcheada até o
power-off. **O que se corrige é o silêncio, não a política.**

---

## Defeito 3 — `native_bt_fragil` olha só o transporte do primário

`daemon/ipc_handlers.py:1630-1632`:

```python
result["native_bt_fragil"] = bool(
    result["native_mode"] and result["transport"] == "bt"
)
```

E `result["transport"]` vem de `get_transport()`, que devolve `self._transport`
— **o transporte do primário** (`core/backend_pydualsense.py:1665`).

Com o primário no cabo e três no Bluetooth, a flag sai `False` e o banner
`NATIVE_BT_FRAGIL_TEXT` (`app/actions/home_actions.py:277-281`) **não aparece
para os três que de fato estão frágeis**.

**A informação por controle existe e está a doze linhas dali:**
`result["controllers"]` (`ipc_handlers.py:1642-1645`).

**Aceite:** com um controle no cabo e um no BT em modo nativo, o aviso aparece —
e diz **para qual controle** vale.

---

## Defeito 4 — o restore do broker antes de reabrir é inalcançável

`daemon/connection.py:399-404` chama `_restore_hidden_before_reopen` no `except`
do `reconnect_loop`, justificando: *"a classe 'permissão hidraw' inclui o nó
AINDA ESCONDIDO pelo broker"*.

**Mas `connect()` engole a exceção de cada device**
(`core/backend_pydualsense.py:1481-1489`: `logger.debug("backend_open_one_failed")`
+ `continue`) desde a `LIGHTBAR-BT-ADOPT-01`. **Um `EACCES` do `hidapi.Device`
nunca sobe.**

Resultado: um controle cujo nó ficou escondido fica **permanentemente
não-adotado**, retentado a cada ≤30 s, com uma linha de DEBUG.

**A cronologia mostra que nasceu morto:** o `except` per-device é de **18/07**
(`bbfe74d`); o restore é de **21/07** (`4184f79`).

**É a mesma família do check cego da `BT-SDP-VAZIO-01`** — uma rede que só pega
o que já não precisa dela.

**Aceite:** um controle com o nó escondido é adotado no ciclo seguinte, não em
nenhum. **A mordida:** um device falso que dá `EACCES` uma vez e adota na
segunda.

---

## Defeito 5 — `determineConnectionType` vaza o `hidapi.Device`

`pydualsense.py:157-169`: report de tamanho diferente de 64 ou 78 ⇒
`ConnectionType.ERROR` ⇒ `init()` levanta `"Couldn't determine connection type"`
**depois** de o device já estar aberto e **antes** de qualquer `close()`.

`core/backend_pydualsense.py:1416-1424` só trata `"No device detected"`; o resto
propaga, e o `connect()` engole (defeito 4). **O objeto some sem fechar o fd.**

**Grau:** o vazamento é **PROVADO no código**; o gatilho por Bluetooth é
**HIPÓTESE** — a janela entre o `connect` do BlueZ e o probe do
`hid-playstation`, em que o controle pode não estar no report estendido.

**Aceite:** `_open_one` fecha o device em **qualquer** falha de `init()`, não só
na conhecida. É irmã da E2 da `BT-SURDO-01` e deve ser feita junto.

---

## Defeito 6 — o teto de silêncio de 30 s paga um round-trip de broker por controle

`core/physical_report_reader.py:141-142`: por Bluetooth o teto é **30 s** (contra
1 s no cabo) — e isso é **assimetria intencional**, paga com um laço a 1 Hz e
~1.600 linhas de journal em 45 min (`GYRO-BT-SILENCIO-01`). **Não mexer nela.**

O que **não** foi calculado para quatro controles é o que acontece quando o teto
vence (`:570-580`): o reader **larga o fd**, chama `set_motion_streaming(False)`
— que zera a janela de motion e **solta o clique do touchpad no vpad**
(`integrations/uhid_gamepad.py:1304-1307`) —, dorme 0,1 s e reabre pelo
`make_broker_opener`.

**Com quatro controles: até quatro ciclos de largar-e-reabrir a cada 30 s** em
menu ou pausa, cada um com I/O de socket do broker (timeout de 2 s por chamada) e
**um blip de IMU neutra no vpad daquele jogador**.

**Cura:** o teto continua; o que muda é o custo do vencimento. Reabrir sem soltar
o clique do touchpad, e escalonar os quatro em vez de deixá-los coincidir.

**Aceite:** com quatro controles parados, o journal não mostra quatro ciclos
simultâneos de reabertura.

---

## Defeito 7 — o broker recusa o DualSense Edge FÍSICO

O daemon adota `{0x0CE6, 0x0DF2}` (`core/evdev_reader.py:29`). O broker aceita
**só** `0x0CE6` e rejeita `0x0DF2` explicitamente
(`broker/hidraw_broker.py:82-83, 260-264`), porque é a identidade que **o vpad
forja**.

Um DualSense Edge **físico** não pode ser escondido nem servido por fd:
`read_calibration` e o `PhysicalReportReader` dele caem no `os.open` por caminho.

**As regras que saberiam distinguir já estão no arquivo** — D1 (USB real nunca é
uhid) e D2 (`HID_PHYS hefesto-vpad` / `HID_UNIQ 02:fe`), em
`broker/hidraw_broker.py:212-216`. **A rejeição do `0x0DF2` acontece ANTES
delas.**

**Grau:** provado no código; **hipotético na prática — ela não tem um Edge.**

**Aceite:** um Edge físico (identidade real de BT/USB, sem `hefesto-vpad` no
`phys`) é aceito; o vpad continua rejeitado. **E entra nas Limitações conhecidas
do README enquanto não for feito.**

---

## Testes que vão reprovar

```
pytest tests/unit tests/core -k "motion or physical_report or sysfs or broker or native or connect"
```

## O que NÃO fazer

- **Não afrouxar o `LIGHTBAR-BT-NEVER-01`** (defeito 2) nem o **teto de 30 s**
  (defeito 6) — as duas são assimetrias com defeito medido atrás;
- **Não aceitar `0x0DF2` no broker sem as regras D1/D2** (defeito 7): sem elas,
  o broker passaria a poder esconder o próprio vpad, que é por onde o jogo fala;
- **Não tratar o defeito 1 como teórico.** Ele é inerte só porque a ponte de mic
  está desligada — e ligá-la é um recurso que o projeto anuncia.

## O que fica ABERTO

- **se o kernel também aceita o pacote de áudio como input** (defeito 1) — não
  medido aqui; se sim, é patch de DKMS;
- **o experimento do defeito 1 tem custo**: com `HEFESTO_DUALSENSE4UNIX_BT_MIC=1`
  e um `evtest` no nó do controle parado, eventos sem ninguém tocar confirmam.
  **Se confirmar, o controle fica inutilizável enquanto o mic estiver no ar** —
  avise antes de rodar.
