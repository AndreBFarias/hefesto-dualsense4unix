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

## O CHECKLIST — o padrão universal de validação de um elemento

- **Acrescentado em:** 11/08/2026, a pedido dela: *"pra que esse padrão de agora
  seja o padrão universal de validação de cada elemento, pra que tenhamos um
  padrão de checklist nesse sentido"*.
- **Nasceu de:** a sessão da mesa cheia — quatro DualSense, dois no cabo e dois
  no rádio — em que rumble, lightbar e gatilho foram validados pela mesma
  sequência, e a sequência se mostrou melhor que a soma das partes.

Os oito passos acima continuam sendo o ciclo. Este checklist é **a ordem em que
se percorre o ciclo para UM elemento**, do zero até poder escrever `O APARELHO
OBEDECEU` no mapa sem mentir.

Marque cada linha. Item pulado é dado — anote que pulou. Item respondido no
chute contamina tudo o que vier depois.

### A — Antes de tocar no aparelho

- [ ] **A1.** As cinco perguntas desta página, na ordem. A primeira que falhar
      interrompe.
- [ ] **A2.** Os suspeitos levantados **lendo o código**, não por palpite
      (Passo 1). Liste tudo que é escrito para aquele elemento: bits de
      autorização, bytes de valor, e quem mais escreve no mesmo lugar.
- [ ] **A3.** **Que grau esta feature tem hoje?** Se está em `MONTOU`, ninguém
      provou que o aparelho obedece — e essa é a pergunta, não um detalhe.

### B — Provar que a peça responde

- [ ] **B1. A linha de base** (Passo 2). No estado normal, aciona? Se não, o
      defeito é anterior aos suspeitos.
- [ ] **B2. O teste de controle: tudo apagado contra tudo aceso.** Antes de
      perguntar *de que lado* falha, prove que **responde**. Em 11/08 três
      rodadas foram perdidas medindo uma peça que talvez nem obedecesse.

### C — Medir NO PAR, que é o que a mesa cheia compra

- [ ] **C1.** Acione o elemento em **um controle no cabo e um no rádio, na mesma
      janela**. Registre o espalhamento do disparo — se não for de milissegundos,
      são dois ensaios em fila, não um ensaio de coexistência.
- [ ] **C2.** Leia o resultado por esta regra, que não se negocia:
      - **`sim` em par** → vale, e é evidência **mais forte** que sozinho: a
        feature sobreviveu à companhia.
      - **`não` ou `parcial` em par** → **ambíguo**. Não se sabe se é o
        transporte ou a coexistência. Re-meça aquele controle **sozinho** antes
        de escrever qualquer coisa.
- [ ] **C3.** O **controle negativo simultâneo**: o que não deveria mudar, na
      mesma mão e no mesmo instante. Em 11/08 foi o R2 continuar solto enquanto
      o L2 endurecia — provou de uma vez que o comando agiu e que não vazou de
      lado.

### D — Isolar o mecanismo, não só o sintoma

- [ ] **D1. Um suspeito por vez, os DOIS lados** (Passo 3), com **ida e volta**:
      tire o suspeito e veja curar, devolva e veja o defeito voltar. Só a volta
      distingue causa de coincidência.
- [ ] **D2. DOSE-RESPOSTA, sempre que o suspeito tiver um número.** Se o
      suspeito é um intervalo, um limite ou uma constante, **mude o número e
      veja a resposta seguir**. Isso é prova causal; sim/não é indício.
      Em 11/08 o keepalive foi fechado assim: `0,5 s` produzia um pulso,
      `8,0 s` produziu **oito segundos exatos** de vibração.
- [ ] **D3. O aparelho honra os BITS de autorização, ou os BYTES de valor?**
      Pergunte sempre, para todo elemento. Em 11/08 ficou medido que o firmware
      do DualSense **obedece aos bytes de motor com os bits de vibração
      desligados** — o que derrubou a premissa de uma cura inteira que estava
      escrita, correta na própria lógica, e mirando o alvo errado.
      **Isto não foi medido para gatilho, LED nem áudio**, e os blocos deles
      também saem escritos em todo report.
- [ ] **D4. A hipótese explica o que JÁ funcionava?** (pergunta 5). Se o
      elemento funcionava em outro transporte, em outro dia, ou no relato dela,
      a explicação tem de cobrir isso também.

### E — O desenho do ensaio, para não desperdiçar a mão dela

- [ ] **E1. Nunca peça cronômetro a um humano.** Se a resposta depende de
      *quando* algo mudou, o instrumento está errado — redesenhe para que a
      resposta seja **sentida**, não medida. Em 11/08 duas rodadas se perderam
      pedindo "em que instante parou", e a terceira fechou a questão trocando o
      tremor **de lado**: ou muda de mão, ou não muda.
- [ ] **E2. Ela não vê a janela do comando.** A mensagem "aperte agora" só chega
      **depois** que o comando termina. Ou o ensaio roda em segundo plano e ela
      age quando quiser, ou dura o bastante para ela pegar o controle depois de
      ler.
- [ ] **E3. Amplitude máxima na primeira tentativa** (`METODO-01`, 01/08). 15%
      contra 100% quase reprovou uma entrega correta; 0 contra 255 a reabilitou
      em trinta segundos.

### F — Fechar

- [ ] **F1. Registrar na hora** (Passo 6) — **inclusive o ensaio que você
      descartou, e por quê**. Um ensaio mal desenhado que foi trocado é
      informação: sem o registro, o próximo o repete.
- [ ] **F2. O teste que MORDE** (Passo 8), arrancado **de verdade** do arquivo
      de produção, visto reprovar, devolvido.
- [ ] **F3. O grau, e ele é honesto por construção:** `MONTOU` → `SAIU NO FIO` →
      `O APARELHO OBEDECEU`. Só o olho dela sustenta o terceiro.
- [ ] **F4. A PODA** (Passo 7): o que foi inocentado pode parar de ser acionado.
- [ ] **F5. A pergunta que ela faz e que fecha o assunto:** *"o elemento
      específico que faz ele funcionar de fato está isolado?"* Funcionar **não
      é** saber por quê. Se o elemento passou em tudo acima e você ainda não sabe
      de qual bit, byte ou condição ele depende, escreva isso na ressalva — em
      vez de deixar a linha parecer fechada.

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
| 8 | **Pedir cronômetro à mão humana** | Duas rodadas com respostas incompatíveis entre si — e nenhuma delas era erro dela |
| 9 | **A janela que ela não vê** | O "aperte agora" só chega depois que o comando terminou |
| 10 | **Confundir controle negativo com prova** | O R2 ficar solto prova que o comando não vazou; **não** prova que o R2 obedece |
| 11 | **Supor que o firmware honra os bits** | A cura desliga os bits de autorização e o aparelho obedece aos bytes assim mesmo |
| 12 | **O caderno envelhecer sem que ninguém note** | Uma medição que só existe em docstring deixa o `eliminacao.py` acusando um culpado removido há sete dias |

A número 5 merece nota: em 10/08 um agente relatou a cura aplicada e com mordida
provada, e o arquivo estava intacto. **Conferir o arquivo é parte do método**, não
desconfiança.

As de 8 a 12 são de 11/08, e três delas são erro meu, registrado de propósito:

- **A 8 e a 9 são de desenho, não de execução.** Quando o ensaio exige da mão
  dela uma precisão que a mão não dá, quem falhou foi o instrumento. A saída não
  é repetir com mais cuidado — é **redesenhar para que a resposta seja sentida**.
- **A 10 aconteceu comigo em pleno registro:** marquei `gatilho.direito` como
  `O APARELHO OBEDECEU` porque o R2 ficou solto enquanto o L2 endurecia. Aquilo
  provava a não-contaminação, não a obediência do lado direito. Ela pegou.
- **A 12 é a mais silenciosa de todas.** O caderno não erra sozinho: ele fica
  certo sobre o dia em que foi escrito. Toda medição que muda um veredito
  **precisa virar linha em `ensaios.csv` no mesmo dia**, ou o instrumento passa a
  mentir com autoridade.

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

---

## O segundo gabarito — 11/08/2026, a mesa cheia

Quatro DualSense: **P2 e P3 no cabo, P1 e P4 no rádio**, identificados pelo
padrão de LED de jogador lido no fonte do driver
(`hid-playstation.c:1836-1842`) e conferidos contra a leitura dela — bateram
quatro de quatro, inclusive o transporte. É o gabarito de como o checklist acima
se percorre de verdade, e do que cada passo comprou.

| passo | o que se fez | o que comprou |
|---|---|---|
| B2 | branco nos quatro lightbars, daemon parado | separou dois defeitos que pareciam um |
| C1 | rumble disparado nos quatro na mesma janela (0,0 ms) | os quatro vibram juntos: `combinacao.rumble_simultaneo` deixou de estar muda |
| C2 | falha em par → re-medido sozinho | evitou registrar *"o cabo mata o rádio"*, que era falso |
| D1 | daemon parado → contínuo; religado → morre | a causa é o daemon, com ida e volta |
| D2 | `OUT_REPORT_KEEPALIVE_SEC` de `0,5` para `8,0` | **oito segundos exatos**: é o keepalive, com número |
| D3 | report com bits desligados e bytes trocados | o firmware obedece aos **bytes** — a premissa de uma cura inteira caiu |
| E1 | o tremor troca de lado, em vez de *"quando parou?"* | fechou numa rodada o que duas não fecharam |
| C3 | R2 solto enquanto o L2 endurece | provou que o comando agiu **e** que não vazou de lado |

**Três features fecharam, e cada uma com dono diferente** — a lição de que o
mesmo sintoma pode ter causas distintas, e de que tratá-las como uma só teria
custado o dia:

| feature | parar o daemon | dono do defeito |
|---|---|---|
| rumble por evdev no nó físico | **cura** | o keepalive do produto |
| lightbar no rádio | não muda nada | fora do nosso código; **continua sem nome** |
| gatilho adaptativo | não foi preciso | nenhum: obedeceu de primeira |

### O que ficou aberto nesta sessão

- **O gatilho está onde o rumble estava de manhã:** funciona, e ninguém sabe de
  qual bit ou byte ele depende. E há uma previsão herdada de **D3** que nunca foi
  medida: os blocos de gatilho (`common[10..20]` e `common[21..31]`) também são
  escritos em todo report, fora de qualquer condicional — se o firmware os tratar
  como trata os bytes de motor, **o keepalive apaga o efeito de gatilho que um
  jogo aplicou**, pelo mesmo mecanismo e sem ninguém perceber.
- **O lado direito do gatilho** e os **oito modos do firmware** seguem sem ensaio
  próprio; só `Rigid` foi exercitado, com um único jogo de parâmetros.
- **A causa da lightbar no rádio continua sem nome.** O `0x08` foi removido do
  produto em 04/08 e a barra continuou morta por cinco dias e vinte adoções por
  Bluetooth; a suspeita viva é **tempo desde a conexão**, dimensão que teste
  unitário nenhum alcança.
