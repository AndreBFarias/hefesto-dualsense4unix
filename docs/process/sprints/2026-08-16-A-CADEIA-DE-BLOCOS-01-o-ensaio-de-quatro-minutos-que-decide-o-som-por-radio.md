# A CADEIA DE BLOCOS-01 — o ensaio de quatro minutos que decide o som por rádio

> **O QUE ISTO CUSTA DE VOCÊ, e é a primeira linha de propósito: 6 minutos de
> olho, uma vez só.** Quatro minutos no **E-7** (oito observações da lightbar) e
> dois no **passo do ruído** que fecha a frouxidão do E-1 (dez observações). Nada
> de ouvido, nada de som, nenhuma escuta cega. Se o E-7 abrir a porta, o **E-5**
> volta redesenhado e pede **mais 8 minutos** noutra sessão; se fechar, o E-5
> custa **zero** e você economiza a hora de ouvido que o desenho original pedia.
> **Você pode não rodar nada hoje e nada se perde** — o instrumento é código, e
> código roda sem você.

- **Escrito em:** 16/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  com a árvore suja e os controles na mesa.
- **Grau:** **DESENHO.** Nada aqui foi executado. Nenhum `/dev/hidraw` foi aberto
  por esta passagem, nenhum byte foi escrito em controle nenhum, ninguém tocou no
  hardware, e o daemon não foi reiniciado.
- **Alicerce, e ele já fez o trabalho difícil:**
  [E-5 O TERRENO](2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md).
  Esta sprint **não repete** o terreno — ela o transforma em coisa executável por
  quem chegar amanhã sem ter vivido esta madrugada.
- **De onde vêm os ensaios:**
  [ESCADA-QUE-RESPONDE-01](2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md)
  (o E-5 original) e a M-7 da
  [PONTE-UNIVERSAL-01](2026-08-15-A-PONTE-UNIVERSAL-01-o-cabo-como-pedra-de-roseta.md).
- **Depende de:** a **D-31** já autorizada, na faixa mais estreita dela —
  *"autoriza só o que NÃO manda payload"*. O bloqueio da família `0xF0`-`0xF7`
  (**D-32**) continua de pé e esta sprint não o toca.

---

## 1. A frase curta, para quem só vai ler o começo e o fim

**O E-5 não roda. O que roda no lugar dele é o E-7, e ele derruba a premissa que
sustenta as outras cinco: existe uma CADEIA de blocos no corpo do degrau?**

Esta casa **nunca escreveu dois blocos no mesmo report** — nem aqui, nem em
lugar nenhum desta árvore. Toda a conversa sobre "onde o bloco de áudio vai"
pressupõe um encadeamento que ninguém jamais produziu. O E-7 produz o primeiro, e
o sensor é o mais barato e o mais honesto que temos: **o olho dela na lightbar**.

**A sacada, e ela é uma linha de desenho:** pôr o bloco candidato **primeiro** e o
bloco de cor **depois dele**. Aí *"a cor obedeceu"* deixa de ser ambíguo — ela só
pode obedecer se o parser tiver andado por cima do candidato usando o comprimento
declarado. No E-1 o bloco de cor vinha antes, e um ensaio cujo sensor está a
montante do que ele quer medir não mede aquilo: mede a si mesmo.

**E há o achado que valida a leitura inteira:** a cabeça do `0x32` **é TLV**,
medido no E-1 do outro agente (commit `08db454`), com o próprio microfone como
sensor e o bit `report[55] & 0x04` como veredito, em duas unidades do rádio. O
`common` de 47 bytes está **REFUTADO nos dois braços**. É isso que dá chão ao
`BLOCO_SPEAKER = 0x13`, declarado em 25/07 e nunca referenciado por linha nenhuma.

---

## 2. O que tem de estar de pé antes de qualquer byte

Cada item aqui já produziu medição falsa nesta casa. Nenhum é formalidade.

| # | a pré-condição | como se confere, e não é por suposição |
|---|---|---|
| 1 | **A Steam FECHADA** | ela apaga a lightbar por escrita crua em hidraw, por cima de nós — medido por ela em 16/08 01h05, com par de eliminação completo. Confere-se por **processo segurando hidraw**, e o instrumento tem de **recusar rodar** e nomear a Steam |
| 2 | **O sysfs NÃO serve de conferência** | ele leu `[0 255 0]` com a barra apagada e com a barra verde — guarda o **pedido**, nunca o **aceso**. Nenhum passo desta sprint lê `multi_intensity` para nada |
| 3 | **O alvo está no RÁDIO** | a escada `0x31`-`0x39` só existe no rádio. Casamento `hidrawN` → `uniq` pelo `uevent`, **nunca** pela ordem de enumeração, e `--alvo` com MAC conferido |
| 4 | **A porta é o broker, com o daemon VIVO** | parar o daemon derruba os quatro vpads e o co-op. Escrita crua por `os.write` no fd que o broker serve |
| 5 | **A lightbar está no campo de visão dela** | e nenhuma outra fonte de luz colorida perto. É o único sensor deste ensaio |
| 6 | **O `btmon` só no passo 7** | nos passos 1 a 6 ele é ruído; no 7 ele é o que separa "perda de rádio" de "achado" |

---

## 3. O que falta de código antes do E-7 — 35 minutos de máquina, zero dela

O instrumento já existe: `scripts/ensaios/corpo_do_degrau.py`. Ele já recusa
report fora de `0x31`-`0x39`, já monta o envelope BT com o `bt_crc32` do produto
(semente `0xA2`), já apaga entre os passos, já pausa esperando ela dizer o que
viu, e já imprime *"O RETORNO DO os.write NÃO É A MEDIÇÃO"*. **O que falta é
pouco, e está listado para que ninguém reescreva o que está pronto.**

1. **O modo de cadeia (`--cadeia`)** — os sete passos da seção 4, montados byte a
   byte como a tabela manda. É o grosso dos 35 minutos.
2. **A recusa por hidraw ocupado**, nomeando a Steam. **É o único acréscimo
   OBRIGATÓRIO**: sem ele o sensor pode estar morto e o ensaio inteiro sai falso.
3. **Os dois negativos como alvos próprios** (`--negativo crc`,
   `--negativo tag-zero`), cada um com **cor exclusiva** — ver a armadilha 8.
4. **`--repeticoes N`** para o passo 7, alternando duas cores.
5. **O bruto escrito sozinho**, `.txt` e `.csv`, em `docs/data/ensaios-brutos/`,
   com passo, id do report, tamanho no fio, os bytes `[2]` e `[3]`, cor pedida, o
   que ela viu e a hora. **Ensaio que não vira linha de tabela vira lembrança**, e
   a seção 7 mostra o preço que já pagamos por isso.
6. **`--dry-run`** que imprime os pacotes e não escreve nada. É como se confere o
   montador sem gastar bancada dela.

**A mordida do instrumento, e ela não mudou:** rode com os nós trocados na linha
de comando. Se o relatório não trocar de endereço junto, ele está lendo a ordem
de enumeração e não o aparelho.

---

## 4. O E-7, passo a passo

**Degrau:** `0x32` — 142 bytes no fio, 88 de recheio depois do `common`. Barato
de montar, barato de ler no `btmon`, e o bloco candidato de 8 bytes cabe folgado.
**Não é o `0x39`**: o `0x39` é o degrau do E-5, por aritmética de payload, e aqui
não há payload nenhum.

### 4.1 O layout de cada passo, byte a byte

O envelope é sempre o mesmo: `[0]` = `0x32`, `[1]` = `seq << 4`, os quatro
últimos bytes = CRC-32 little-endian com semente `0xA2`, e o resto zerado.

```
   PASSO 1 — o controle POSITIVO, a linha de base já medida        VERMELHO
       [2]=0x10  [3..49]=common(47)                      RGB em [47..49]

   PASSO 2 — O ACHADO: o bloco candidato ANTES da cor              VERDE
       [2]=0x93        tag 0x13|0x80, o BLOCO_SPEAKER declarado em 25/07
       [3]=0x08        len do bloco candidato
       [4..11]         oito zeros — o valor do candidato
       [12]=0x10       a tag do SetState, AGORA depois do candidato
       [13..59]=common(47)                               RGB em [57..59]

   PASSO 3 — o mesmo do 2 com o len UMA UNIDADE MENOR              AZUL
       [3]=0x07        e o resto dos bytes IDÊNTICO ao passo 2
                       (o SetState continua fisicamente em [12])

   PASSO 4 — o mesmo do 2 com tag DESCONHECIDA                     AMARELO
       [2]=0x9E        0x1E|0x80 — longe da família 0xF, de propósito

   PASSO 5 — o SetState com len EXPLÍCITO, sem candidato nenhum    CIANO
       [2]=0x10  [3]=47  [4..50]=common(47)              RGB em [48..50]

   PASSO 6 — a M-7 refeita com o layout certo                      MAGENTA
       [2]=0x90  [3]=47  [4..50]=common(47)              RGB em [48..50]

   PASSO 7 — o ruído do E-1, N=10, com btmon             BRANCO/VERMELHO
       [2]=0x10  [3..49]=common(47)  [50..137]=ruído, semente 20260816
```

**Por que o passo 3 é o que ele é:** os bytes vão para o fio **iguais** aos do
passo 2 e só o `len` declarado muda, de 8 para 7. Se o firmware honra o `len`, ele
procura a tag seguinte em `[11]` — que é zero — e a cadeia quebra: **o azul não
aparece**. Se o azul aparecer certinho, o formato é **posicional**, e o `len` é
decoração.

**Por que o passo 6 existe:** a M-7 da PONTE-UNIVERSAL, como está escrita, mantém
o `common` em `[3..49]` e troca só o `[2]` para `0x90`. Sob a leitura TLV que ela
quer testar, esse pacote é **malformado** — com bit7 ligado o `len` tem de estar
em `[3]`, e `[3]` traz `valid_flag0`. Rodada assim, ela produz um "não" que parece
medição e não é. **O passo 6 é a M-7 com o layout que a hipótese dela exige.**

### 4.2 Os dois controles negativos, e sem eles o passo 2 não prova nada

| negativo | o pacote | cor pedida | o que tem de acontecer |
|---|---|---|---|
| **N1 — CRC errado** | o pacote do passo 2, com o CRC deliberadamente invertido (`--crc-errado`, que já existe) | **LARANJA** (255,128,0) | **não pode acender.** Se acender, o firmware não está consumindo o nosso pacote, e a escada inteira significa outra coisa |
| **N2 — `[2] = 0x00`** | o layout do **passo 1** (`[3..49]=common`), com `[2]` zerado | **ROSA** (255,0,128) | **não pode acender.** Sem ele, "acendeu no passo 2" é compatível com "o firmware acende com qualquer coisa em `[2]`" |

> **A correção que esta sprint faz no desenho do terreno, e ela importa:** o
> terreno põe o N2 no layout do passo 2, em cadeia. **Isso o quebra como
> negativo.** Se o passo 4 acender — tag desconhecida pulada pelo `len` —, então
> `[2]=0x00` com `[3]=8` é um bloco desconhecido de 8 bytes, o parser o pula, e o
> pacote **deve** acender. O negativo viraria positivo e ninguém saberia dizer
> qual dos dois estava acontecendo. **N2 roda no layout simples**, onde a única
> leitura possível de acender é "o `[2]` não é lido".

### 4.3 Os comandos, na ordem

Nada aqui foi executado. Os MACs são os **mascarados** do caderno (octetos 4 e 5
zerados); troque pelo alvo da mesa daquele dia.

```bash
# 0. a conferência que vem antes de tudo — não escreve byte nenhum
.venv/bin/python scripts/ensaios/corpo_do_degrau.py --listar

# 1. o positivo e o achado, na mesma corrida, com os dois negativos no meio
.venv/bin/python scripts/ensaios/corpo_do_degrau.py \
    --alvo 14:3a:9a:00:00:ab --report 0x32 --cadeia \
    --passo 1 --passo 2 --negativo crc --negativo tag-zero

# 2. a gramática: len, tag desconhecida, len explícito, e a M-7 refeita
.venv/bin/python scripts/ensaios/corpo_do_degrau.py \
    --alvo 14:3a:9a:00:00:ab --report 0x32 --cadeia \
    --passo 3 --passo 4 --passo 5 --passo 6

# 3. o passo do ruído, N=10, com o btmon gravando NOUTRO terminal
sudo btmon -w docs/data/ensaios-brutos/2026-08-16-E7-a-cadeia-de-blocos.btsnoop
.venv/bin/python scripts/ensaios/corpo_do_degrau.py \
    --alvo 14:3a:9a:00:00:ab --report 0x32 --cadeia --passo 7 --repeticoes 10
```

### 4.4 O que ela olha, e é só isto

Em cada parada o instrumento **apaga a barra, pergunta se está apagada**, manda o
pacote e pergunta **que cor apareceu**. A resposta é uma palavra.

```
   passo 1   -> apagada?  ...  VERMELHO apareceu?
   passo 2   -> apagada?  ...  VERDE apareceu?
   N1        -> apagada?  ...  LARANJA apareceu?   (tem de continuar APAGADA)
   N2        -> apagada?  ...  ROSA apareceu?      (tem de continuar APAGADA)
   passo 3   -> apagada?  ...  AZUL apareceu?
   passo 4   -> apagada?  ...  AMARELO apareceu?
   passo 5   -> apagada?  ...  CIANO apareceu?
   passo 6   -> apagada?  ...  MAGENTA apareceu?
   passo 7   -> dez vezes, alternando BRANCO e VERMELHO
```

**"Apagada?" não é zelo excessivo:** o firmware guarda a cor sem reforço por mais
de dois minutos, e essa é a armadilha que fabrica falso positivo mais barato desta
família inteira.

---

## 5. A tabela de desfechos — se acontecer X, o próximo é Y

**Os três que mandam PARAR vêm primeiro, de propósito.**

| se | então a leitura é | e o próximo passo é |
|---|---|---|
| **o passo 1 NÃO acende** | o instrumento quebrou, a Steam está aberta, ou o alvo está errado | **PARE.** Nada do resto significa o que se pensa. Confira a Steam por processo, o broker e o `uevent` do alvo |
| **o N1 (CRC errado) ACENDE** | o firmware não está consumindo o nosso pacote | **PARE.** A escada inteira passa a significar outra coisa, e isso é frente nova, maior que esta |
| **o N2 (`[2]=0x00`) ACENDE** | o byte `[2]` não é lido; não há tag nenhuma | **PARE.** O passo 2 deixa de provar cadeia, e a leitura TLV cai inteira — inclusive a do microfone |
| **o passo 2 ACENDE, com N1 e N2 mudos** | **A CADEIA EXISTE.** O parser andou por cima de um bloco `0x13` de 8 bytes pelo comprimento declarado | siga os passos 3 a 6, e o **E-5 volta redesenhado** (seção 6) |
| **o passo 2 não acende e o passo 5 ACENDE** | o SetState aceita `len` explícito — e então a cadeia do passo 2 começava **um byte depois** de onde a pusemos | rode a **variante 2-B** antes de concluir qualquer coisa: `[2]=0x93 [3]=8 [4..11]=zeros [12]=0x10 [13]=47 [14..60]=common`. Erro de um byte é o modo de falha mais barato desta família |
| **o passo 2 e a 2-B não acendem, e o passo 1 acende** | não há cadeia no `0x32` pelo caminho do SetState | sobra a **P2** do censo do terreno: um bloco `0x13` **sozinho** em `[2]`, sem `common` nenhum — que é a forma que o microfone já usa e que funciona em produção desde 25/07. O E-5 nasce com essa forma, **e o preço é perder a lightbar como testemunha no mesmo pacote** |
| **o passo 3 NÃO acende** (com o 2 aceso) | o `len` é lido de verdade | o E-5 pode declarar comprimento e confiar nele. É o desfecho que mais simplifica o montador |
| **o passo 3 ACENDE azul** (com o 2 aceso) | o formato é **posicional**, não TLV | o E-5 tem de pôr o bloco num offset fixo, e o `len` vira decoração. Isso muda o montador inteiro |
| **o passo 4 ACENDE** | TLV **genérico**: tag desconhecida é pulada pelo `len` | o `0x13` não precisa ser "conhecido" para caber na cadeia. **E atenção: isso REDUZ o valor do passo 2** — se qualquer tag é pulada, o passo 2 não disse nada sobre o `0x13` em particular |
| **o passo 4 NÃO acende** | só tags conhecidas são puladas | a lista do módulo (`0x10`, `0x11`, `0x12`, `0x13`, `0x16`) é a lista inteira, e o E-5 fica preso a ela |
| **o passo 5 ACENDE** | o corpo é TLV **homogêneo**: até o SetState carrega `len` | uma linha nova na canônica, e um montador mais simples |
| **o passo 6 ACENDE magenta** | `[2]` é **campo**, não constante mágica de envelope | a M-7 fecha, com o layout certo, e a contradição da seção 4 do terreno se resolve |
| **o passo 7: as dez obedecem** | o recheio em `reserved[24]` é ignorado, agora com N=10 | a frase do E-1 pode ser escrita, **estreita**: *"o `reserved[24]` do `0x32` é ignorado"*. Nunca *"o excedente é ignorado"* |
| **o passo 7: alguma falha, e o `btmon` mostra o `ACL Data TX`** | o pacote saiu e o firmware não obedeceu | **há estrutura**, e o bruto tem o byte exato. A semente é fixa: refaz-se byte a byte |
| **o passo 7: alguma falha, e o `btmon` NÃO mostra o TX** | perda de rádio | descarte aquela repetição e repita. Não é achado |

---

## 6. O E-5, e ele só existe depois

**Gatilho:** o passo 2 (ou a variante 2-B) acender, com N1 e N2 mudos. Fora
disso, o E-5 **não roda** — nem redesenhado.

O terreno já esboça o redesenho na seção 6.3, e o que segue é o resumo executável.
**O que muda em relação ao E-5 da ESCADA-QUE-RESPONDE-01, e por quê:**

| item | como fica | por quê |
|---|---|---|
| **degrau** | `0x39` (547 B) | 402 bytes de payload não cabem nos 88 do `0x32` e cabem nos 493 do `0x39`. **O número é o argumento** |
| **posição** | o `0x13` **primeiro**, o SetState de cor **depois** | é a mesma sacada do E-7: a lightbar continua sendo testemunha de que o parser andou por cima dos 402 bytes |
| **tag** | duas variantes, duas cores: `0x93` com dois blocos de `len` 200, e `0xD3` (`\|BLOCO_DUPLO`) com `len` 200 e dois sub-blocos | é a leitura literal do módulo, e seria a **primeira vez** que o `BLOCO_DUPLO` sai do comentário |
| **conteúdo** | **MONO**, e em duas aritméticas: os 200 B do DS5Dongle **e** os 71 B que a entrada realmente usa | o alto-falante interno é mono, medido em 16/08 00h05. Mandar estéreo para ele é cheiro de desenho. A segunda aritmética é de graça: o módulo já monta quadro de 71 B |
| **timbre** | **os dois timbres dela** do `tres_casos_de_som.py`: 180 Hz contínuo e 1300 Hz pulsado a 2 Hz | o desenho é dela, de 15/08, e já provou que resolve relato ambíguo. **Um seno de 440 Hz é o tom mais confundível que existe** |
| **positivo do canal** | a cor, no mesmo pacote | prova que o report foi consumido, no mesmo milissegundo, sem depender de som nenhum |
| **positivo do OUVINTE** | o mesmo timbre tocado pelo alto-falante de um controle **no CABO**, que já está medido, gravado pela mesma webcam, na mesma distância, no mesmo minuto | **é a lacuna mais séria do E-5 original.** Sem isto, *"não ouvi nada"* é indistinguível de *"o instrumento não pegaria nem o som que funciona"* |
| **negativo 3** | os outros três controles desligados ou fora da sala, a saída do sistema em mudo, e 10 s de gravação basal antes de qualquer escrita | é o que a observação não replicada de 16/08 00h10 exige: ela ouviu ~6 s de um timbre reconhecível vindo de um controle **no rádio**, quatro tentativas de replicar deram negativo, e ninguém sabe de onde veio. **É o falso positivo mais caro que este ensaio pode produzir** |
| **quem observa** | webcam por FFT — **e não existe instrumento** | não há um único script com FFT nem com webcam nesta árvore. É trabalho novo, e o custo abaixo já o conta |
| **teste CEGO** | ela relata sem saber o que foi enviado | é o desenho da madrugada de 15-16/08, e é o que produziu 177 ensaios que valem alguma coisa |

**Custo:** **8 minutos dela** — 2 de mão, posicionando controle e webcam, e 6 de
ouvido em teste cego — e **2 h 30 de máquina**: o codificador Opus por `ctypes`
(o `opus_encoder_create`/`opus_encode` existem na libopus 1.4 desta máquina e o
módulo já tem o carregador), mais o instrumento de gravação e FFT, que não existe.
**Outra sessão, nunca a mesma do E-7.**

---

## 7. O buraco de registro, e ele se tapa ANTES de qualquer célula se mover

**O resultado do E-1 não está no caderno.** Conferido: `docs/data/ensaios.csv` tem
177 ensaios e **nenhuma linha** do E-1 da escada; não há bruto daquela corrida em
`docs/data/ensaios-brutos/`; e o instrumento está em `git add`, não commitado.

Esta casa tem um portão feito exatamente contra isso —
`tests/unit/test_o_grau_forte_exige_ensaio_no_caderno.py`, nascido de uma mutação
de 12/08 em que grau forte passou com zero ensaios no CSV. **Enquanto o E-1 viver
só na memória da sessão, nenhuma célula pode dizer "o excedente é ignorado".**

E há uma divergência concreta que só o bruto resolve: as cores relatadas na
madrugada **não batem** com a tabela de passos do instrumento
(`corpo_do_degrau.py:129-135` diz passo 2 = VERDE e passo 3 = AZUL; o relato diz
magenta, e cita um recheio `0xF0` que não está em tabela nenhuma). O `0xF0` é
reconhecível: é o ruído com a semente reiniciada a cada byte, o defeito que a
própria docstring registra ter pego na primeira execução de 16/08. **Duas passadas,
uma com o gerador quebrado, e a memória juntou as duas.** Isso não se resolve
lembrando.

**O que falta, e é barato:** duas linhas em `docs/data/ensaios.csv`, o bruto da
corrida em `docs/data/ensaios-brutos/`, e o commit do instrumento.

---

## 8. O que vai para o mapa quando cada um fechar, com a célula pelo nome

Nenhuma linha abaixo se escreve antes de a seção 7 estar tapada, e nenhuma se
escreve sem a linha correspondente em `docs/data/ensaios.csv`.

| quando fechar | célula, pelo nome | o que ela passa a poder dizer |
|---|---|---|
| **passo 2 acende** | `plataforma.escada_de_output@dualsense` | *"o corpo do `0x32` é uma CADEIA de blocos: o firmware anda por cima de um bloco `0x13` de 8 bytes pelo comprimento declarado e executa o SetState que vem depois. Medido em 16/08/2026, olho dela, N unidades."* |
| **passo 2 não acende, 2-B não acende** | idem | *"não há cadeia no `0x32` pelo caminho do SetState. O bloco em `[2]` sozinho continua sendo a única forma medida."* |
| **passos 3, 4 e 5** | idem, e a seção do envelope BT da [canônica](../../protocol/dualsense-referencia-canonica.md) | a gramática: o `len` é honrado / é posicional; tag desconhecida é pulada / não é; o SetState aceita `len` explícito / não aceita |
| **passo 6** | idem, e fecha a **M-7** da PONTE-UNIVERSAL-01 | *"o byte `[2]` é CAMPO, não constante de envelope"* — ou o contrário, com o layout que a hipótese exige |
| **passo 7 (N=10)** | `audio.saida_dedicada.payload_do_degrau@dualsense` | *"o `reserved[24]` do `0x32` (`[50..73]`, `hid-playstation.c:351-359`) é ignorado — N=10, com `btmon` conferindo o TX."* **Estreito assim, e não mais que isso** |
| **E-5, e SÓ ele** | `audio.alto_falante@dualsense`, rádio | **só aqui** a palavra "alto-falante por rádio" pode aparecer com grau `O APARELHO OBEDECEU`. Enquanto o E-5 não fechar, nenhuma célula diz que existe saída de som por rádio |

**As linhas do caderno**, uma por desfecho, com `linha_id` a célula acima,
`transporte = radio`, `observado_por = olho-dela`, e a `nota` dizendo o pacote
byte a byte e o que ela viu. **Uma linha por desfecho, nunca uma por corrida** —
foi assim que os pares com/sem da madrugada de 15-16/08 se salvaram de virar
lembrança.

---

## 9. As armadilhas, e onde cada uma morde NESTE desenho

1. **O `os.write` que devolve sucesso sem veredito do firmware.** Morde em todos
   os passos, e já pegou o kernel aceitando um pacote de tamanho errado que era o
   controle negativo. O instrumento imprime *"O RETORNO DO os.write NÃO É A
   MEDIÇÃO"* e pausa esperando ela. **Quem mede é o olho dela.**
2. **A FALÁCIA DO CANAL QUE RESPONDE.** Morde no passo 2: *"a cor acendeu depois
   de um bloco `0x13`"* prova que **o parser andou a cadeia**. Não prova que a tag
   `0x13` significa alto-falante, não prova que o bloco foi consumido com sentido,
   e não prova que 200 bytes de Opus ali dentro fariam som. A redação de cada
   desfecho já está escrita na seção 5 para que ninguém a escreva melhor do que é.
3. **Controle positivo E negativo, sempre.** O E-7 nasce com dois positivos (o
   passo 1, e o apagar conferido antes de cada parada) e dois negativos (CRC
   errado, `[2]=0x00`). **Se um dos negativos acender, o ensaio para** — e isso é
   resultado, não fracasso.
4. **A proibição de `SET_FEATURE` na família `0xF0`-`0xF7`.** Intacta, e é a
   **D-32**. Nada aqui toca feature report nenhum. O `0x9E` do passo 4 é uma **tag
   de bloco**, que é outro espaço de nomes — e a tag base é `0x1E`, escolhida longe
   de qualquer coisa perto de `0xF` justamente para que ninguém leia a linha errado
   com pressa.
5. **A Steam apaga a lightbar** (16/08). Todo ensaio cujo sensor é a lightbar é
   **inválido** com a Steam aberta. O instrumento tem de recusar rodar e nomear a
   Steam — é o único acréscimo obrigatório de código antes do E-7.
6. **O sysfs não sabe o que a barra mostra** (16/08). Nenhum passo lê
   `multi_intensity` para nada.
7. **O instrumento que lê a ordem de enumeração em vez do aparelho.** Casamento
   `hidrawN` → `uniq` pelo `uevent`, `--alvo` com MAC conferido, e a mordida
   continua a mesma: rode com os nós trocados e veja o relatório trocar junto.
8. **A cor repetida, e esta é nova.** Sete cores distinguíveis e nove paradas: se
   um negativo pedir a mesma cor do passo anterior, "acendeu" e "continuou aceso"
   viram a mesma observação. Por isso os dois negativos têm **cor exclusiva**
   (laranja e rosa) e o passo 7 **alterna** branco e vermelho.
9. **O negativo que vira positivo por causa do layout, e esta também é nova.** Ver
   a caixa da seção 4.2: o `[2]=0x00` em cadeia colide com a própria hipótese do
   passo 4. Ele roda no layout simples.
10. **Erro de um byte.** É o modo de falha mais barato desta família e o E-1 não
    podia distingui-lo de "ignorado". A variante 2-B da seção 5 existe só para isso.

---

## 10. O que NÃO está decidido, e é dela

1. **O E-7 roda hoje?** São 6 minutos e você virou a noite. Se a resposta for
   "amanhã", nada se perde: o modo de cadeia é código, e código roda sem você.
2. **O E-5 fica na fila mesmo se o E-7 abrir a porta?** São 2 h 30 de máquina e 8
   minutos seus, e há frentes com preço menor por decisão fechada.
3. **A colisão de nome "E-1".** Duas sprints da mesma semana têm um ensaio E-1, e
   eles concluem coisas diferentes sobre o mesmo report — um mediu o `reserved` do
   `0x32`, o outro mediu que a cabeça do `0x32` é TLV. Renomear um dos dois é
   decisão de vocabulário, e vocabulário é seu.
4. **O nome da falácia gêmea** continua sendo a **D-33**, e esta sprint a usa pelo
   nome proposto sem tomar a decisão por você.

---

## 11. O que esta sprint NÃO prova, repetido no fim de propósito

- **Não prova que existe cadeia de blocos.** Prova que ninguém aqui jamais
  escreveu uma, que o E-1 não podia tê-la detectado, e desenha o ensaio que
  decide.
- **Não prova que o E-1 errou.** Ele fechou uma posição, com controle positivo e
  negativo, e fechar posição é o trabalho. O que ele não sustenta é a frase larga
  *"o excedente é ignorado"* — o que ele mediu foi o `reserved[24]`, numa cadeia
  que nunca abriu, no degrau em que o payload não cabe.
- **Não prova nada sobre áudio.** Nem um byte de áudio de saída foi escrito por
  esta casa, nem hoje nem nunca. **Não existe ponte de áudio de saída por rádio**,
  e esta sprint não a aproxima — ela diz onde procurar o chão antes de construir.
- **O que continua provado, e é bastante:** o canal existe, transporta 552 bytes
  num pacote, o firmware executa o `common` de 47 bytes em três degraus
  diferentes, e a cabeça do `0x32` é TLV.
