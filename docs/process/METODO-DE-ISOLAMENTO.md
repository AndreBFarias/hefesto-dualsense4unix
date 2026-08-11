# O método de isolamento — a lista que nos impede de errar

- **Escrito em:** 10/08/2026, depois do primeiro ensaio de bancada dela e minha
  (rumble do DualSense por Bluetooth).
- **Nasceu de:** *"a ideia é terminarmos aqui com uma to do list de método boa o
  suficiente pra nunca errarmos"*.
- **Para que serve:** um ciclo repetível para isolar qualquer feature de qualquer
  controle em qualquer canal — e, no fim, **encolher o produto**.

O molde é o estudo `LIGHTBAR-BT-CULPADO-01`. Ele levou dezesseis dias, e a lição
que este documento existe para não deixar esquecer: **o que fechou aquela conta
não foram os seis ensaios com o suspeito presente — foi o único em que ele estava
ausente.** Correlação vira causa no ensaio que discrimina, nunca no acúmulo.

---

## Antes de qualquer ensaio — as cinco perguntas

Ordem importa. A primeira que falhar interrompe: um ensaio feito sobre premissa
errada não é ensaio, é folclore com data.

### 1. O instrumento briga com o produto?

A armadilha mais cara desta casa. `test trigger --raw` disputa o hidraw com o
daemon e **imprime "aplicado" sem ter aplicado**.

```bash
# o comando que vamos usar passa pelo daemon, ou escreve no hidraw direto?
grep -n 'ipc\|hidraw\|_safe_call' src/hefesto_dualsense4unix/cli/cmd_test.py
```

Passa pelo IPC → segue. Escreve direto no hidraw com o daemon de pé → **pare** e
use o IPC, senão o ensaio mede a briga, não a feature.

### 2. O daemon vivo é mais velho que o código?

Instalação editável: o código no disco pode estar curado e o processo em memória
não. O sintoma é traiçoeiro — a **ausência** de um dado, não um erro.

```bash
systemctl --user show hefesto-dualsense4unix.service -p ActiveEnterTimestamp
git log -1 --format=%cd -- src/    # o código é mais novo que o processo?
```

### 3. O transporte é mesmo o que eu penso?

Não confie no rótulo da janela nem na memória.

```bash
cat /sys/class/hidraw/hidrawN/device/uevent | grep HID_ID
#   0005:... = Bluetooth      0003:... = USB
```

### 4. O que este ensaio pode derrubar?

Escreva a hipótese **antes**, e o que ela prevê para cada lado. Ensaio cuja
resposta não muda nada é passatempo.

### 5. A hipótese explica o que JÁ funcionava?

Regra da casa. Se a explicação só cobre o defeito e não explica por que aquilo
funcionava ontem, ou no outro transporte, ela está incompleta — e o que vier
depois é contorno, não cura.

---

## O ciclo — os oito passos

### Passo 1 · Levantar os suspeitos LENDO O CÓDIGO

Nunca por palpite. Abra o caminho e liste tudo que é escrito para aquela feature.

O rumble do DualSense, medido em 10/08, é o exemplo do porquê:

```python
if not rumble_asserted:
    flag0 &= ~(COMPATIBLE_VIBRATION | HAPTICS_SELECT)   # dois bits
    flag1 &= ~MOTOR_POWER                               # um
    flag2 &= ~COMPATIBLE_VIBRATION2                     # um
```

**Quatro bits de autorização em três flags, mais dois bytes de intensidade.**
Seis coisas escritas para uma feature — e ninguém nunca mediu de quantas o
aparelho precisa. Foi assim na lightbar: cinco canais, um importava.

### Passo 2 · A LINHA DE BASE, antes de mexer em nada

Aciona no estado normal. Funciona?

- **Funciona** → há o que eliminar. Siga.
- **Não funciona** → não há o que eliminar ainda; o defeito é anterior aos
  suspeitos. Ache-o primeiro.

### Passo 3 · Um suspeito por vez, e os DOIS lados

A regra que o `scripts/eliminacao.py` implementa e que não se negocia:

> Um suspeito só é julgado quando existem ensaios **com** ele e **sem** ele.

Enquanto houver só um lado, o veredicto é `inconclusivo` — e o instrumento diz
**qual ensaio falta**. Essa frase é a que ninguém tinha durante os dezesseis dias
da lightbar.

### Passo 4 · O ensaio que DISCRIMINA

Melhor que repetir o mesmo ensaio é achar um que separe duas hipóteses de uma
vez. Em 10/08, `--weak 0 --strong 200` respondeu três perguntas num disparo:
o rumble funciona no rádio, os motores são endereçáveis em separado, e `strong`
é o esquerdo — porque **só um lado vibrou**.

### Passo 5 · O controle negativo

O que **não** deveria mudar o resultado, e não muda. Na lightbar foi o `0x08`
disparado fora da janela: o mesmo report, sem travar — foi ele que provou que a
variável era a **janela**, não o report.

### Passo 6 · Registrar na hora

```bash
.venv/bin/streamlit run bancada.py     # o formulário de ensaio
```

Cada ensaio grava: suspeito, presente sim/não, resultado, quem observou, e a
nota do que mais estava valendo. **Uma prova sem data é folclore**, e um ensaio
não registrado no mesmo dia vira lembrança.

### Passo 7 · A PODA — a metade que dá lucro

Todo suspeito que ficar `não é a causa` é candidato a **parar de ser acionado**.

Foi o que ela descreveu: *"de 5 canais, um deles é o que realmente impactava;
após isso passamos a usar somente ele, e deixamos o projeto menos complexo"*.

A causa isolada responde **por onde acionar**. Os inocentados respondem **o que
dá para parar de fazer** — e é essa a pergunta que encolhe o código.

Cuidado único: `não sei se faz efeito` **não é** `provei que não faz efeito`.
Podar por inconclusivo é arrancar a cura de alguém achando que era enfeite.

### Passo 8 · O teste que MORDE

Sem ele, tudo isto volta na próxima mexida.

```bash
# 1. escreva o teste     2. rode: passa
# 3. ARRANQUE a cura DO ARQUIVO DE PRODUÇÃO
# 4. rode: TEM de reprovar        5. devolva a cura
```

**Arrancar de verdade, não simular.** Em 10/08 escrevi um teste que "provava" a
mordida com um `move_to()` no lugar de remover a linha: passava com a cura
arrancada. Teste que passa sem a cura não protege nada — e é pior que teste
nenhum, porque dá sossego falso.

---

## As sete armadilhas, todas medidas

Cada uma custou tempo real. Nenhuma é hipotética.

| # | Armadilha | Como ela aparece |
|---|---|---|
| 1 | **O instrumento disputa o hidraw** | Diz "aplicado" e não aplicou |
| 2 | **O daemon vivo é mais velho que o código** | Falta um dado que deveria estar lá |
| 3 | **Medir contra a régua errada** | Número absurdo (uma posição relativa deu `1,207`, impossível) |
| 4 | **Teste que não morde** | Verde com a cura arrancada |
| 5 | **Relatório de agente não é prova** | Reportou `aplicado=true` sem ter escrito no arquivo |
| 6 | **Colisão de nomes silenciosa** | `getElementById('corpo')` devolveu o `<g>` do SVG, não a tabela; nenhum erro |
| 7 | **Só um lado do ensaio** | Seis ensaios "com" e nenhum "sem": zero poder de prova |

A número 5 merece nota: em 10/08 um agente relatou a cura aplicada e com mordida
provada, e o arquivo estava intacto. **Conferir o arquivo é parte do método**, não
desconfiança.

---

## O que registrar em cada linha do mapa

| coluna | o que é |
|---|---|
| `grau` | **MONTOU** (montou o report) → **SAIU NO FIO** (o byte saiu, algo voltou) → **O APARELHO OBEDECEU** (acendeu, girou, saiu som) |
| `provado_por` | `ci` / `bancada` / `olho-dela` — só `olho-dela` sustenta *O APARELHO OBEDECEU* |
| `provado_em` | a data. Sem ela a prova não vence nunca, e prova que não vence vira mito |
| `teste_que_morde` | o nó do pytest que reprova se aquilo quebrar |
| `mordida_provada_em` | quando alguém **de fato** arrancou a cura e viu reprovar |

Tratar **MONTOU** como **funciona** é a mentira mais cara desta casa.

---

## Como isto replica entre os três controles

É para isto que a chave canônica existe. `vibracao.rumble.esquerdo` é a mesma
chave nos três; o que muda é a peça e o código evdev:

| | DualSense | Nintendo Pro | 8BitDo SN30 |
|---|---|---|---|
| convergência | `common[2]/[3]` | report `0x10` | report `0x10` |
| envelope cabo | `0x02` | direto | direto |
| envelope rádio | `0x31` + CRC32 | igual ao cabo | igual + rate limiter 60 ms |

Isolado num controle, o outro é **trocar o nome da variável** — que foi a frase
dela. E o que **não** replica precisa estar escrito: a lightbar do DualSense é
`impossível` no 8BitDo, que não tem LED RGB.

---

## O primeiro ensaio completo — 10/08/2026

Registro do que serve de gabarito para os próximos.

**DualSense, Bluetooth confirmado por `HID_ID=0005`, daemon ativo.**

| ensaio | comando | resultado |
|---|---|---|
| linha de base | `--weak 220 --strong 220` | vibrou |
| discrimina | `--weak 0 --strong 200` | **só o esquerdo** |
| discrimina | `--weak 200 --strong 0` | **só o direito** |
| parada | `--weak 0 --strong 0` | parou de fato |

Veredicto do caderno, calculado sozinho: `common[3]` (strong) **é a causa** do
motor esquerdo; `common[2]` (weak), do direito. Grau **O APARELHO OBEDECEU**,
observado por ela.

Achado de brinde: o *"trava sem fim"* da `ONDA-U` **não se reproduziu** — o zero
parou o motor na hora.

E o instrumento se validou: `test rumble` chama o mesmo `rumble_set` do
`ipc_bridge` que a aba Rumble da GUI chama. **O ensaio percorreu o caminho real
do produto**, não um atalho de teste.

### O que ficou aberto nesta feature

Os quatro bits de autorização continuam sem ensaio. Sabemos que o conjunto
inteiro funciona; **não sabemos de quantos o aparelho precisa**. É a poda que
sobra — e o `HAPTICS_SELECT` tem urgência própria: a pesquisa de 10/08 registra
que ele **mata os haptics de áudio do jogo**, e ninguém mediu se ele é preciso
para vibrar.
