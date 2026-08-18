# E-8 — o contador que o driver joga fora, e a régua que errava 62 vezes

- **Escrito em:** 15/08/2026, noite, na branch `restauro/inicio-da-sessao`.
- **Frente:** B — o giroscópio e a perda de IMU.
- **A porta, declarada:** **broker** (`SCM_RIGHTS`), nos quatro DualSense
  físicos, com o **daemon VIVO** (Lei 1). Bibliotecas: `os`, `struct`, `fcntl`,
  `selectors` — todas da stdlib, e o instrumento imprime o caminho de cada uma
  antes de medir.
- **Escrita no aparelho:** **nenhuma** (Lei 3). O único ioctl que fala com o
  controle é `HIDIOCGFEATURE` (GET_REPORT) do feature `0x05`, e ele roda num fd
  **`O_RDONLY`** — conferido nesta máquina.
- **Instrumento:** [`scripts/ensaios/giro_e_buraco.py`](../../../scripts/ensaios/giro_e_buraco.py), novo.
- **Brutos:** `docs/data/ensaios-brutos/2026-08-15-E8-giro-e-buraco.{txt,csv}` e
  `docs/data/ensaios-brutos/2026-08-15-E8-A-unidade-no-radio-que-dormiu-e-caiu.{txt,csv}`.

---

## O que este estudo fecha, em uma tabela

| célula | antes | agora |
|---|---|---|
| `movimento.giroscopio@dualsense` cabo | `inferido-do-codigo` | **`medido`** |
| `movimento.giroscopio@dualsense` rádio | `inferido-do-codigo` | **`medido`** (pela troca de braços) |
| `movimento.imu.perda@dualsense` cabo | `inferido-do-codigo` | **`medido`** |
| `movimento.imu.perda@dualsense` rádio | `inferido-do-codigo` | **`medido`** |
| `movimento.imu.ligar@dualsense` | premissa "REFUTADA" | fato **substituído** por medição |

---

## 1. A régua estava errada por 62 vezes, e o jeito de errar era o pior possível

O `imu_no_cabo.py` (E-4, de manhã) imprimia o giroscópio dividindo o valor CRU
do fio por `DS_GYRO_RES_PER_DEG_S = 1024`, e a coluna `giro_*_dps` do bruto
`2026-08-15-E4-imu_no_cabo.csv` saiu assim: **+0,02 graus/s**, quatro
aparelhos, um número lindo e falso.

`1024` é a resolução **DE SAÍDA**: a escala do `ABS_RX/RY/RZ` que o kernel
publica **depois** de calibrar. O valor cru do fio está noutra escala. O driver
converte (`hid-playstation.c:1196-1213`) por

```
graus_por_s = cru * speed_2x / sens_denom_do_eixo
```

com `speed_2x` e `sens_denom` lidos do **feature report 0x05 de cada unidade**.
Medido nas quatro:

| unidade | `speed_2x` | `sens_denom` (x y z) | LSB crus por grau/s |
|---|---|---|---|
| `a0:fa:9c` | 1080 | 17694 17688 17683 | 16,38 |
| `d4:2f:4b` | 1080 | 17694 17662 17676 | 16,38 |
| `14:3a:9a` | 1080 | 17734 17577 17829 | 16,42 |
| `44:46:48` | 1080 | 17702 17678 17662 | 16,39 |

**~16,4 LSB por grau/s, não 1024.** A leitura verdadeira de repouso é ~1,3
graus/s, não 0,02.

**Por que isto é grave e não é imprecisão.** A régua errada **torna o controle
negativo impossível de reprovar**. Com ela, um DualSense girando a 60 graus/s
leria "0,96" e passaria por parado; um girando a 600 leria "9,6". Um
instrumento que não consegue falhar não é instrumento — e o teto de "parado"
deste ensaio (5 graus/s) teria sido atendido por qualquer coisa.

É a armadilha `A-3` desta casa em estado puro, e desta vez ela estava dentro do
nosso próprio instrumento.

**O que foi feito:** `imu_no_cabo.py` deixou de publicar graus/s. Ele agora
publica **LSB crus**, que é a única coisa honesta que um instrumento sem a
calibração da unidade pode dizer, e a constante ganhou nota datada explicando o
erro. Quem quer graus/s usa o `giro_e_buraco.py`, que lê o feature 0x05.

---

## 2. O contador de reports que o driver chama de `reserved`

O `struct dualsense_input_report` (`hid-playstation.c:295-315`) tem:

```c
u8  seq_number;      /* corpo[6]      */
u8  buttons[4];      /* corpo[7..10]  */
u8  reserved[4];     /* corpo[11..14] */   <-- este
```

Medido em 15/08/2026, nos quatro aparelhos e nos dois transportes:

| campo | no CABO | no RÁDIO |
|---|---|---|
| `corpo[6]` (`seq_number`) | anda de 1 em 1 | **constante em 1** — delta zero em 100% dos pares |
| `corpo[11..14]` lido como `__le32` | anda de 1 em 1 | **anda de 1 em 1** |

O campo com nome de contador é **mudo justamente no transporte que perde**. O
campo que o kernel chama de `reserved` e nunca lê é um **contador de reports de
32 bits que funciona igual nos dois transportes** — e é, hoje, a única régua de
perda que atravessa cabo e rádio.

Isso responde diretamente à assimetria que o mapa declarava:

> *"uma degradação de link no CABO é invisível para a telemetria"*

Ela é invisível por **escolha de campo**, não por limitação do protocolo. O
`0x01` do cabo não tem CRC — verdade —, mas tem o mesmo contador do `0x31`.

### O que foi medido com ele

**Cabo, 60,0 s, dois aparelhos:** 0 saltos, **0 reports perdidos** em 15012 e
15007 pares consecutivos, a 250,1 Hz. Silêncio máximo entre reports: 8,13 e
11,94 ms — contra **7,99 ms** de maior parada do próprio laço do instrumento, que
é o controle negativo do instrumento e sai impresso ao lado.

**Rádio, na mesma noite:** **2242 reports sumidos num único salto**, num
aparelho cujo enlace degradou dentro da janela — a taxa no host caiu para
27,1 Hz enquanto o relógio DO CONTROLE seguia marcando 398,4 Hz de emissão. Os
dois relógios discordando é o que separa *"o enlace comeu"* de *"o firmware
calou"*, e aqui foi o enlace.

---

## 3. A ELIMINAÇÃO — o que se pode parar de fazer

### 3.1 INOCENTADO: o transporte, como causa da leitura do giroscópio

A troca de braços das 19h é o que fecha este par: as **mesmas unidades** foram
medidas no rádio de manhã e no cabo à noite. O bias de repouso (módulo do vetor
médio, régua do feature 0x05 de cada unidade):

| unidade | no RÁDIO (07h27) | no CABO (22h23) | diferença |
|---|---|---|---|
| `14:3a:9a` | 0,188 graus/s | 0,249 graus/s | 0,061 |
| `44:46:48` | 0,932 graus/s | 0,886 graus/s | 0,046 |

O bias anda com a **UNIDADE**, não com o transporte: diferença por transporte
≤ 0,06 graus/s, contra **5x de diferença entre as duas unidades**. Uma terceira
unidade (`a0:fa:9c`) é consistente: 1,245 no cabo de manhã, 1,311 pela conta do
kernel no rádio à noite.

**Consequência:** ninguém precisa medir giroscópio "no cabo" e "no rádio"
separadamente. É uma coluna a menos para encher, e um ensaio a menos para
repetir.

### 3.2 É A CAUSA: o `seq_number` como contador de perda

Os dois lados deste par são os **mesmos bytes, na mesma janela**, e o que muda
é só o campo lido — por isso nada mais pode estar mandando no resultado.

| | contando por `seq_number` | contando por `reserved` |
|---|---|---|
| rádio (enlace degradando) | **0 detectados** | **2242 detectados** |
| cabo (60 s, 30019 pares) | 0 detectados | 0 detectados |

No rádio o resultado **muda** → o campo escolhido é a causa de a perda ficar
invisível. No cabo o resultado **não muda** → ali os dois são intercambiáveis, e
essa é a armadilha: quem escolhesse olhando só para o cabo não pagaria preço
nenhum e levaria para o rádio um contador que cala.

### 3.3 NÃO HÁ O QUE PODAR: o comando de ligar a IMU

Procurado antes de concluir, por `git grep` em `imu`, `motion`, `enable_motion`
e `ligar` sobre `src/` e `app/`:

- **Não existe**, nesta árvore, código que tente ligar a IMU do DualSense.
- `set_motion_streaming` é flag **do VPAD** — decide se o espelho emite, não se
  o sensor liga.
- O único Enable-IMU do projeto é o subcomando `0x40` do protocolo Switch, em
  `core/external_leds.py:149`, e é do **Nintendo Pro REAL**.

E a medição confirma que não faria falta: sem nenhuma escrita, em transporte
nenhum, os aparelhos entregaram IMU válida — acelerômetro em 1 g e giroscópio
com o bias de fábrica. **Fica registrado que a poda foi procurada e não existe**,
para que ninguém gaste a busca de novo.

---

## 4. O fato errado que eu ia repetir, e que a medição corrigiu

A célula `movimento.imu.ligar@dualsense` dizia, desde 14/08:

> a premissa "por Bluetooth o firmware EMUDECE em repouso" foi **REFUTADA** por
> medição em 03/08 — com os controles PARADOS o hidraw entregou cerca de 300 Hz

Eu comecei este trabalho pronto para usar isso como munição para podar o
`_SILENCE_REOPEN_BT_S = 30.0`. **A medição desta noite disse o contrário**, e
mostrou por que as duas medições anteriores pareciam se contradizer: a premissa
não é falsa, ela é **dependente do tempo de repouso**.

| momento | `a0:fa:9c` (Charging 95%) | `d4:2f:4b` (Discharging 75%) |
|---|---|---|
| 22h05 | 246 Hz | 401 Hz |
| 22h07 | 252 Hz | 305 Hz |
| 22h15 | 273 Hz | **4,2 Hz** |
| 22h17 | 352 Hz | **0 Hz** |
| 22h20 | cai durante a janela | nó já sumiu |
| 22h24 | desconectado | desconectado |

Com repouso **curto** o firmware não emudece — 246 a 401 Hz, que reproduz os
~300 Hz de 03/08. Com repouso **longo** ele desce, cala, e acaba
**desconectando sozinho** do Bluetooth.

O contador de `corpo[11..14]` prova que **não é perda**: enquanto emitiu, andou
de 1 em 1.

**Controle negativo do instrumento:** os dois aparelhos de **cabo**, no mesmo
host e na mesma janela, ficaram em 250,1 Hz com 0 perdidos por 60 s. Ler não
emudece controle nenhum.

**Consequência para o produto:** o `_SILENCE_REOPEN_BT_S = 30.0` de
`core/physical_report_reader.py:251` **não é podável**, e a razão dele volta a
valer com número em vez de com anedota. Quem for "simplificar" isso amanhã tem
esta tabela pela frente.

**Ressalva declarada, e ela importa:** `n` = 1 de cada lado na coluna da
energia. O aparelho `Charging` segurou mais tempo, mas também caiu — carregar
**adia**, não imuniza. E ninguém registrou quando cada um foi tocado pela última
vez, que é a variável óbvia que este ensaio não isolou. **É ACHADO, não
julgamento**, e o ensaio que falta está na seção 6.

---

## 5. Os dois defeitos que o próprio instrumento encontrou em si mesmo

Ficam registrados porque os dois passariam despercebidos e os dois viraram teste.

**5.1 Duas janelas não são a mesma janela.** O controle positivo 2 (comparar a
minha conta com a do kernel) rodava numa janela de 2 s depois da janela de
medição. Às 22h15 um aparelho foi encostado durante uma e não durante a outra, e
o instrumento acusou **1,15 contra 26,18 graus/s** — divergência de instrumento
sem nenhum instrumento errado. Agora o hidraw e o evdev são lidos no **mesmo
`select`**.

**5.2 Um silêncio que não termina não fecha par nenhum.** O silêncio era medido
entre reports consecutivos. Um aparelho que calou nos últimos ~55 s de uma
janela de 60 s apareceu na tabela com **"silêncio máximo 19,03 ms"** — porque o
silêncio que interessava nunca fechou um par, e par nenhum é amostra nenhuma. O
instrumento agora mede a **cauda muda** (do último report ao fim da janela) e
imprime **quanto da janela está coberta** por intervalo medido.

---

## 6. O que falta, e quem pode fazer

**Para o `eliminacao.py` (limitação estrutural, não defeito de dado).** Ele
agrupa por `(linha_id, transporte)`. Quando o suspeito **é o próprio
transporte**, os dois lados caem em baldes diferentes e o veredicto nunca sai —
cada lado fica `INCONCLUSIVO` pedindo o outro, que existe. Os pares de suspeito
`o TRANSPORTE ... como causa` em `ensaios.csv` estão nessa situação de
propósito, e a eliminação da seção 3.1 está feita **no texto**, não pelo
instrumento. A correção é dele, não dos dados, e não foi feita aqui porque
`scripts/eliminacao.py` está fora do território desta frente.

**Para O BLOCO DELA** (precisa da mão, Lei 2):

1. **Acordar os dois DualSense de rádio** (botão PS) e rodar
   `.venv/bin/python scripts/ensaios/giro_e_buraco.py --segundos 60` nos
   primeiros minutos. Isso fecha o braço de rádio do E-8 com os três controles
   passando — hoje ele saiu por evdev, porque o `GET_FEATURE 0x05` devolve `EIO`
   em aparelho de rádio ocioso.
2. **O ensaio que isola a energia:** deixar um DualSense de rádio **no cabo de
   carga** e outro **só na bateria**, os dois tocados no mesmo minuto, e rodar o
   instrumento a cada cinco minutos até um dos dois cair. É o lado que falta do
   par da seção 4, e ele diz se carregar adia ou não faz diferença.
3. **A confirmação do giroscópio que nenhum ensaio parado pode dar:** girar um
   controle devagar, uma volta completa, e conferir se a integral de `|w|` dá
   ~360 graus. É o único jeito de provar que a régua está certa também **longe
   do zero** — todo este estudo mede o aparelho **parado**, e a escala só foi
   validada contra a conta do kernel, que usa os mesmos números do feature 0x05.

**Para o produto, quando ela quiser:** parsear o `__le32` de `corpo[11..14]` em
`core/physical_report_reader.py`. Daria ao **cabo** o contador de perda que ele
nunca teve e ao **rádio** um que mede perda de verdade, em vez do `bt_drops`,
que conta o que o **produto** descartou. Não foi feito aqui: `src/` está fora do
território desta frente.
