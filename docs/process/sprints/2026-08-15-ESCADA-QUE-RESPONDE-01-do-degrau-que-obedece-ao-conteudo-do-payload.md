# ESCADA-QUE-RESPONDE-01 — do degrau que obedece ao conteúdo do payload

- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `781dafc` com a árvore suja.
- **Grau:** **PLANO.** Nada aqui foi executado. O que foi **MEDIDO** está no
  estudo que deu origem a esta sprint:
  [a escada que responde](../estudos/2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md).
- **Índice da leva:** [a cor do controle e o som de cada jogador](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
- **Depende de:** a **D-31** (autorizar a bateria de escritas) para os ensaios
  E-1, E-2, E-3, E-5 e E-6; a **D-32** para o `0xF6`. **O E-4 roda sem
  autorização nenhuma** — é leitura pura.
- **Custo:** 1 h 25 de bancada com ela presente, somando os seis ensaios, mais o
  instrumento (estimado, não medido).

---

## 0. O AVISO QUE VEM ANTES DE TUDO — leia mesmo que já saiba

**Quem abrir esta página daqui a um mês vai estar animado como estávamos na
madrugada de 15/08. É este quadro que separa o entusiasmo do achismo.**

| a frase | grau, em 15/08/2026 |
|---|---|
| O firmware lê e **executa** reports de output de 142 B (`0x32`) e 547 B (`0x39`) por rádio | **MEDIDO.** Ela viu a lightbar obedecer, em três cores, com controle positivo e negativo |
| O canal Bluetooth **transporta** 552 bytes num pacote | **MEDIDO.** `ACL Data TX dlen 552` no `btmon` |
| O `common` de 47 bytes vale **igual** em todos os degraus testados | **MEDIDO** para `0x31`, `0x32` e `0x39` |
| Os degraus `0x33` a `0x38` também executam | **NÃO MEDIDO.** Ninguém tentou |
| Os bytes **além** do `common` carregam áudio | **HIPÓTESE.** Nada foi medido sobre eles |
| Existe uma ponte de áudio de saída por rádio | **NÃO EXISTE.** Zero linhas de código |

**A frase honesta, e é a única que pode ser copiada daqui para qualquer outro
documento:**

> **O canal existe, o firmware responde, e o conteúdo do payload ainda não foi
> identificado.** Medido em 15/08/2026, nos quatro DualSense dela, com dois no
> cabo e dois no rádio. O próximo ensaio que avança nisso é o E-1 desta sprint.

**Não se escreve, em lugar nenhum, que "descobrimos o áudio por Bluetooth" ou
que "a ponte funciona".** Não funciona, e não há ponte. Há um canal que
responde. A hipótese de que o excedente é áudio é **forte** — o controle já está
inteiramente servido pelos 47 bytes do `common`, não há outra função de controle
conhecida que peça 469 bytes a mais, e o PS5 manda som para este mesmo aparelho
—, e hipótese forte continua sendo hipótese.

### 0.1 A falácia gêmea, que começa aqui e ainda não tinha nome

Esta casa nomeou em 14/08 a **FALÁCIA DO PERFIL AUSENTE**: tomar *"o aparelho
não anuncia o perfil padrão X"* (medição verdadeira e estreita) como prova de
*"o aparelho não faz Y"* (afirmação forte e falsa). Foi ela que pôs a palavra
"impossível" numa célula do mapa sobre um canal que responde.

**A gêmea nasce hoje, e proponho batizá-la de FALÁCIA DO CANAL QUE RESPONDE:**
tomar *"o canal aceita e executa o que mandamos"* (medição verdadeira e
estreita) como prova de *"o canal faz Y, que era o que a gente queria dele"*
(afirmação forte e não medida).

```
   FALÁCIA DO PERFIL AUSENTE      não achei    ->  logo NÃO EXISTE
   FALÁCIA DO CANAL QUE RESPONDE  respondeu    ->  logo FAZ O QUE EU QUERIA

   uma NEGA demais a partir do silêncio
   a outra AFIRMA demais a partir do eco
```

O nome deriva do léxico que já existe aqui, e é por isso que ele é este e não
outro: as duas erram na mesma junta — **confundir a medição estreita que se tem
com a afirmação larga que se quer.** O batismo é da casa, mas a palavra final
sobre o nome é dela: é a **D-33** do índice.

**Onde ela morderia hoje, se a deixássemos:** o `0x39` executou o `common`;
disso **não** se segue que o bloco `0x13` toca som, nem que 469 bytes sejam
áudio, nem que exista formato conhecido. O E-1 existe exatamente para não
deixarmos a gêmea escrever nada por nós.

---

## 1. O crédito, e ele não é meu

**A derrubada do "impossível" foi dela.** Em 15/08, de manhã, com o mapa ainda
dizendo *"IMPOSSÍVEL por A2DP/HFP"* na célula `audio.saida_dedicada` do rádio:

> *"se no PlayStation via BT tudo isso funciona e pq tem um meio físico pra isso
> funcionar e ainda não descobrimos, pq a documentação oficial é focada no cabo.
> mas muita coisa impossível de fazer acontecer nos fizemos já: lightbar no bt,
> mic funcionando mesmo com processador amd e kernel zuado. só falta mapear
> cientificamente pra tirarmos os achismos nossos do projeto"*

**E a mesa 2+2 — dois controles no cabo e dois no rádio ao mesmo tempo — também
é decisão dela.** Sem esse desenho nada desta sprint existiria: é o instrumento
que faz de "cabo declara 289 bytes de descritor e rádio 320" uma medição de
**transporte**, e não uma diferença entre dois dias, dois humores do BlueZ e
duas unidades diferentes.

A observação dela é fonte primária nesta casa, e nesta frente ela foi duas
coisas ao mesmo tempo: **a hipótese e o instrumento de medida** — foi o olho
dela na lightbar que disse "verde" e "azul" quando o `os.write()` só sabia dizer
"escrevi".

---

## 2. O que já se sabe, e de onde vem cada linha

O detalhe inteiro está no
[estudo](../estudos/2026-08-15-A-ESCADA-QUE-RESPONDE-o-audio-por-radio-deixou-de-ser-impossivel.md).
Aqui fica só o que os ensaios abaixo consomem.

### 2.1 A escada, lida do descritor dos aparelhos dela

| id | CABO | RÁDIO |
|---|---|---|
| `0x02` | OUTPUT 47 B | — |
| `0x31` | — | OUTPUT 77 B + INPUT 77 B |
| `0x32` | — | OUTPUT 141 B |
| `0x33` | — | OUTPUT 205 B |
| `0x34` | — | OUTPUT 269 B |
| `0x35` | — | OUTPUT 333 B |
| `0x36` | — | OUTPUT 397 B |
| `0x37` | — | OUTPUT 461 B |
| `0x38` | — | OUTPUT 525 B |
| `0x39` | — | OUTPUT 546 B |
| `0xF6` | — | FEATURE 546 B |

**Passo de +64 bytes, do `0x31` ao `0x38`.** O `0x39` quebra o passo (seria 589,
e é 546): é **teto**, não degrau.

> **Cuidado de uma unidade, e ele vale antes de dimensionar qualquer buffer:**
> os números acima são **payload**, sem o byte do report ID. O estudo escreve
> `0x39` = 546 B de payload / 547 B no fio; o
> `scripts/ensaios/README.md` anota o `0xf6` como 547 B. **Confira no descritor
> do aparelho na hora**, e imprima os dois números no relatório. Errar em um
> byte aqui produz report recusado e conclusão de que "o degrau não funciona".

### 2.2 O envelope que funcionou, byte a byte

O que ela viu obedecer foi isto, e nada além disto:

```
    [0]        = report id            0x31 | 0x32 | 0x39
    [1]        = seq << 4             nibble de sequência
    [2]        = 0x10                 tag do bloco SetState
    [3..49]    = common de 47 bytes   valid_flag1 = 0x04, RGB em [44..46]
    [.. -5]    = zeros
    [-4..]     = CRC-32 little-endian, semente 0xA2
```

**O que ninguém sabe ainda, e é gratuito de descobrir:** o byte `[2]` valeu
`0x10` — **sem** o bit 7, que o nosso próprio código do microfone chama de
`BLOCO_PRESENTE` e **sempre** liga (`src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py`
monta `[2] = BLOCO_AUDIO_CONTROL | BLOCO_PRESENTE`, isto é `0x11 | 0x80`). Ou o
byte `[2]` é uma **tag TLV** e o firmware aceita as duas formas para o SetState,
ou ele é uma **constante de envelope** no `0x31` e uma tag no `0x32` — e as duas
leituras levam a montadores diferentes. **É o E-3, e custa cinco minutos.**

### 2.3 O lado que JÁ funciona, e que é o melhor ponto de partida desta casa

O microfone por rádio **atravessa hoje, em produção, desde 25/07** — e atravessa
em **Opus**, no input `0x31`, ligado por um output `0x32` com bloco TLV. Tudo
está em `src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py`:

| peça | onde | o que já resolve |
|---|---|---|
| o envelope TLV e as quatro tags | `BLOCO_SET_STATE = 0x10`, `BLOCO_AUDIO_CONTROL = 0x11`, `BLOCO_HAPTICS = 0x12`, `BLOCO_SPEAKER = 0x13` | o vocabulário do corpo do report **já está escrito e nomeado** |
| `BLOCO_DUPLO = 0x40` | bit 6 do byte de tag | *"vêm DOIS sub-blocos do tamanho declarado"* — o comentário do módulo diz que **é assim que o `0x39` manda dois quadros Opus de 200 B** |
| o CRC | `bt_crc32` de `core/ds_output_report.py`, semente `0xA2` | **nenhuma linha de CRC nova a escrever**, e o estudo confirmou o valor |
| Opus | `libopus.so.0` por `ctypes`, já carregada e prototipada | falta **só o codificador**: `opus_encoder_create` e `opus_encode_float` existem na libopus 1.4 desta máquina, e o produto hoje só usa o decodificador |

**Se a entrada é Opus, a saída provavelmente também** — e "provavelmente" é
exatamente a palavra certa até o E-5 rodar.

---

## 3. Os ensaios

**Regra que vale para os seis, sem exceção:**

1. **Todo ensaio nasce com controle positivo E negativo.** Foi o controle
   negativo que pegou o instrumento mentindo em 15/08: `os.write()` num hidraw
   devolve sucesso quando o **kernel** aceita a entrega — ele não espera veredito
   do firmware, e aceitou até o pacote de tamanho errado.
2. **Quem observa é ela**, olhando a lightbar, salvo onde a tabela disser outra
   coisa. O `write` devolver 547 **não prova nada**.
3. **Escrita exige o daemon parado ou o broker.** Leitura convive com o daemon
   (cada fd de hidraw tem a própria fila de entrada); escrita, não —
   `test trigger --raw` já imprimiu "aplicado" sem ter aplicado, disputando o nó
   com o daemon.
4. **O instrumento declara no cabeçalho qual biblioteca e qual transporte**, e
   o casamento `hidrawN` -> `uniq` vem do `uevent`, **nunca** da ordem de
   enumeração. Rode com os nós trocados na linha de comando: se o relatório não
   trocar de endereço junto, ele está lendo a ordem e não o aparelho.
5. **Entre um passo e o seguinte, apague a lightbar pelo `0x31`.** Sem o apagar
   no meio, "acendeu" e "continuou aceso de antes" viram a mesma observação — e
   essa é a forma mais fácil de fabricar um falso positivo aqui.
6. **Cor diferente a cada passo.** Vermelho, verde, azul, amarelo, ciano,
   magenta, branco: sete cores distinguíveis a olho, o bastante para os degraus
   todos. Cor repetida no mesmo minuto é convite ao mesmo erro do item 5.

### E-1 — Variar os bytes extras. **É o ensaio que decide.**

**A pergunta:** os 95 bytes excedentes do `0x32` (e os 500 do `0x39`) são
ignorados, ou têm estrutura?

- **Precisa:** um DualSense **no rádio**; daemon parado ou broker; ela olhando a
  lightbar.
- **Biblioteca declarada:** escrita crua em `/dev/hidrawN` por `os.write`, CRC
  pelo `bt_crc32` do produto. Nenhuma pydualsense, nenhuma SDL.
- **O gesto:** o **mesmo** `common` pedindo cor, no **mesmo** report `0x32`,
  variando só o recheio depois do `common`:

| passo | recheio dos bytes extras | cor pedida |
|---|---|---|
| 1 | tudo zero (é a linha de base já medida) | vermelho |
| 2 | tudo `0xFF` | verde |
| 3 | ruído pseudoaleatório, **semente fixa** (para ser repetível) | azul |
| 4 | um bloco TLV plausível: `0x13 \| 0x80` no primeiro byte livre, `len` coerente, resto zero | amarelo |
| 5 | o mesmo do passo 4 com `len` **incoerente** (maior que o espaço restante) | ciano |

- **Controle positivo:** o passo 1. Se ele não acender, **pare** — não é o
  excedente que está sendo medido, é o instrumento que quebrou.
- **Controle negativo:** repetir o passo 2 com o **CRC deliberadamente errado**.
  Não pode acender. Se acender, o firmware não está consumindo o nosso pacote e
  **nada nesta sprint significa o que a gente acha que significa**.
- **Sucesso:** os cinco passos obedecem -> o excedente é **ignorado naquela
  posição**, e o formato, se existe, não está no lugar onde o pusemos.
- **Fracasso que é o achado:** algum passo **quebra** a obediência -> **há
  estrutura**, e ela mora exatamente no que aquele passo mudou. Anote qual, e o
  E-1 vira o começo do mapa do formato.
- **Tempo:** 20 minutos, contando o `0x39` repetido depois do `0x32`.
- **Ordem:** primeiro no `0x32` (142 B, barato de montar e de ler no `btmon`),
  depois no `0x39` (547 B). Se os dois derem a mesma resposta, isso também é
  informação: o excedente se comporta igual em degraus diferentes.

### E-2 — Subir a escada degrau a degrau: `0x33` a `0x38`

**A pergunta:** o firmware executa **todos** os degraus, ou só os três que já
foram tocados?

- **Precisa:** o mesmo da E-1. Ela olhando.
- **O gesto:** o mesmo `common` de cor, em oito passos — `0x31`, `0x32`, `0x33`,
  `0x34`, `0x35`, `0x36`, `0x37`, `0x38`, `0x39` — **cada um com uma cor
  diferente**, com a lightbar apagada entre um e outro.
- **Controle positivo:** o `0x31`, primeiro passo.
- **Controle negativo, e ele é o mais importante deste ensaio:** um degrau com
  **um byte a menos** que o declarado (por exemplo `0x35` com 333 B em vez de
  334 no fio). **Não pode acender.** Este é o negativo que já pegou o
  `os.write()` mentindo, e sem ele os "sim" de cima valem zero.
- **Sucesso:** sai a tabela dos nove degraus com "obedeceu / não obedeceu", que é
  a primeira medição de **aceitação** da escada inteira. Hoje o índice registra,
  na armadilha 9, que *"descritor prova DECLARAÇÃO, nunca ACEITAÇÃO"* — este
  ensaio é o que converte uma na outra, degrau por degrau.
- **Fracasso interessante:** um degrau **do meio** recusar enquanto os vizinhos
  aceitam. Isso seria estrutura por tamanho — e mudaria a leitura de que "a
  escada é só envelope de tamanho".
- **Tempo:** 15 minutos.

### E-3 — O byte `[2]`: tag TLV ou constante de envelope?

**A pergunta:** o `0x10` que funcionou é uma tag de bloco (e então o bit 7
`BLOCO_PRESENTE` deveria estar ligado, como o nosso código do microfone faz) ou
um byte fixo do envelope do `0x31`?

- **Precisa:** o mesmo da E-1. Cinco minutos.
- **O gesto:** quatro escritas, cada uma com uma cor:

| passo | `[2]` | o que se aprende se obedecer |
|---|---|---|
| 1 | `0x10` | linha de base (já medido) |
| 2 | `0x90` (`0x10 \| 0x80`) | o bit 7 é aceito, e o byte é tag TLV |
| 3 | `0x11 \| 0x80` (AudioControl), com o `common` no mesmo lugar | o firmware **não** está lendo a tag, e sim a posição |
| 4 | `0x00` | o byte não importa — o que derruba a leitura de TLV inteira |

- **Controle negativo:** o CRC errado no passo 2.
- **Sucesso:** qualquer resposta serve, e cada uma escreve uma linha diferente
  na canônica. **Este é o ensaio de melhor razão valor/custo da sprint** — cinco
  minutos para saber se o corpo do report é TLV de verdade ou se a nossa leitura
  do protocolo do microfone estava certa por sorte.
- **Fracasso:** nenhum dos quatro obedecer. Aí o instrumento mudou algo além do
  `[2]`, e o ensaio se refaz.

### E-4 — O `0xF6`, o feature de 546 B que só existe no rádio. **LEITURA PURA.**

**A pergunta:** o gêmeo exato do `0x39`, do lado de FEATURE, é a negociação —
"qual codec, qual taxa, quantos canais vêm a seguir"?

- **Precisa:** nada além do que o `scripts/ensaios/censo_features.py` já faz. **É
  o único ensaio desta sprint que não escreve um byte** — e por isso é o único
  que roda sem a palavra dela.
- **O gesto:** `GET_FEATURE 0xF6` nos dois do rádio, **com retry** (por rádio o
  `GET_FEATURE` falha por timeout de 3 s do BlueZ; em 15/08 um aparelho só
  respondeu na quinta tentativa) e **validando `buf[0] == 0xF6`** (um aparelho já
  devolveu `0x80` no lugar do `0x20` pedido, com o ioctl retornando sucesso).
- **Controle positivo:** um feature já conhecido (`0x20`) lido na mesma rodada,
  para provar que o caminho de leitura está de pé.
- **Controle negativo:** um id que o descritor do rádio **não** declara. Tem de
  falhar. Se "responder", o instrumento está inventando.
- **Sucesso:** os dois aparelhos devolvem os 546 bytes, e a comparação entre eles
  diz se o conteúdo é **constante** (candidato a capacidade/negociação) ou
  **por unidade** (candidato a identidade).
- **Fracasso:** `EPIPE` na hora, em ambos, sem timeout — o que é **resposta
  definitiva do aparelho**: o descritor declara e o firmware não implementa. Isso
  também é medição, e datável.
- **O que está PROIBIDO aqui, e a proibição é da casa:** **nada de
  `SET_FEATURE` na família `0xF0`-`0xF7` sem palavra dela.** Essa família é o
  canal de atualização de firmware. Ler é grátis; escrever, não. É a **D-32**.
- **Tempo:** 10 minutos, quase todo em timeout.

### E-5 — EXP-SPK-01 refeito: o bloco `0x13` com Opus de verdade

**A pergunta:** o bloco `0x13` no `0x39` faz o alto-falante tocar?

**Este é o ensaio que a hipótese pede, e é o que mais precisa do aviso da seção
0** — é aqui que a FALÁCIA DO CANAL QUE RESPONDE se sentaria à mesa se
deixássemos.

- **Precisa:** um DualSense no rádio, daemon **parado**, a webcam C920 gravando,
  ela na sala. **Depende da D-31.**
- **Biblioteca declarada:** `libopus.so.0` por `ctypes` (o mesmo carregador do
  módulo do microfone), escrita crua em hidraw, CRC do produto.
- **O gesto:** montar **um** `0x39` de 547 B com o bloco `0x13` presente
  carregando **dois quadros Opus de 200 B** (estéreo, 48 kHz, 10 ms, CBR
  160 kbps, que é a aritmética que fecha os 545 bytes), e escrevê-lo a 50 Hz por
  3 segundos, com um seno de 440 Hz dentro.
- **Controle positivo:** antes e depois da rajada, um `0x31` acendendo a
  lightbar. Prova que o aparelho está vivo e escutando naquele minuto.
- **Controle negativo 1:** o mesmo report **com o bloco `0x13` removido**. Não
  pode sair som.
- **Controle negativo 2:** o mesmo report **com o CRC errado**. Não pode sair
  som — é o que prova que o firmware está de fato **consumindo** o pacote.
- **Quem observa:** **a webcam, por FFT** — pico em 440 Hz, com a gravação
  guardada. A orelha dela entra como confirmação, **não** como medição: *"achei
  que ouvi"* não é medição, e um sino de 440 Hz na cabeça de quem espera ouvir é
  o viés mais barato do mundo.
- **Sucesso:** pico em 440 Hz na gravação, presente no positivo e ausente nos
  dois negativos.
- **Fracasso, e a redação dele já está escrita:** *"não encontramos o formato do
  bloco `0x13`; descartamos A, B e C; o transporte está provado e o descritor
  declara o degrau"*. **Nunca "não dá".**
- **Três resultados, e os três são informação:** tocou (o caminho é esse); não
  tocou mas o report foi aceito (SAIU NO FIO, falta o formato do payload);
  report recusado (o degrau ou o bloco estão errados).
- **Tempo:** 30 minutos, quase todo escrevendo o codificador.
- **Por que o risco de brick é nulo, e isto vai no cabeçalho do script:** é um
  output report HID **de tamanho declarado pelo próprio descritor do aparelho**,
  pelo canal de interrupção, com CRC válido. Não é feature report, não escreve
  NVS, não toca firmware, e o firmware descarta em silêncio qualquer report BT
  com CRC errado. **É a mesma classe de escrita que a ponte do microfone faz
  nesta casa desde 25/07** — e é a mesma classe que a lightbar já obedeceu em
  15/08, no `0x32` e no `0x39`.

### E-6 — A réplica no cabo: o negativo de transporte

**A pergunta:** a escada é mesmo **do rádio**?

- **Precisa:** a mesa 2+2 dela, e é a única forma de fazer este ensaio.
- **O gesto:** mandar o `0x32` que funcionou por rádio para um controle **no
  cabo**, no mesmo minuto.
- **Controle positivo:** o `0x02` (47 B) acendendo a lightbar do mesmo controle
  no cabo. Prova que o braço do cabo está vivo.
- **O que se espera:** **recusa**. O descritor do cabo declara **um** output
  (`0x02`) e nenhum degrau.
- **Se o cabo aceitar o `0x32`:** a afirmação *"a escada é do rádio"* cai, e o
  que existe é uma escada **não declarada** no cabo. Seria achado maior que o
  desta sprint — e é exatamente o tipo de coisa que só a mesa 2+2 pega.
- **Armadilha que já custou sessão:** **plugar o cabo pode não trocar o
  transporte.** Um DualSense pareado por Bluetooth que recebe o cabo pode
  continuar falando por rádio e só carregar. O braço de cada aparelho se confere
  no `uevent` (`0003` é USB, `0005` é Bluetooth), **nunca** na suposição de que
  "está plugado, logo é USB" — e a conferência entra no relatório, não no
  comentário.
- **Tempo:** 5 minutos, se a mesa já estiver montada.

---

## 4. O instrumento

Um arquivo novo na pasta que já existe — `scripts/ensaios/` —, no molde dos
quatro que estão lá. **Não é código de produto e não mora em `src/`.**

**O que ele tem de fazer, e cada item é dívida paga:**

1. **Cabeçalho declarando biblioteca e transporte**, como os irmãos dele.
2. **Recusar rodar** com o daemon vivo quando for escrever, nomeando o broker em
   vez de dizer "o controle não respondeu" — a assinatura é `0600 root:root`, e
   escrever "o aparelho não respondeu" ali seria calúnia contra o aparelho.
3. **Casar `hidrawN` -> `uniq` pelo `uevent`**, e imprimir o MAC mascarado de
   quem respondeu em cada linha.
4. **Ler os tamanhos do descritor do aparelho na hora**, nunca de constante —
   e imprimir payload e tamanho no fio lado a lado (seção 2.1).
5. **Pausar entre passos esperando ela dizer o que viu**, em vez de rodar tudo e
   perguntar no fim. Memória de sequência de sete cores é do instrumento, não
   dela.
6. **Gravar tudo em CSV**: passo, report id, tamanho, recheio, cor pedida, o que
   ela viu, hora. Ensaio que não vira linha de tabela vira lembrança.
7. **`--dry-run` que imprime os bytes e não escreve nada.** É como se confere o
   montador sem gastar bancada dela.

**A mordida do instrumento:** rode com os nós trocados na linha de comando. Se o
relatório não trocar de endereço junto, ele está lendo a ordem de enumeração e
não o aparelho — a armadilha que já produziu três medições falsas num dia só
nesta casa.

---

## 5. Ordem de execução, e por quê

```
   E-4 (leitura, 10 min)        <- roda hoje, sem autorização nenhuma
        |
   D-31 (a palavra dela)
        |
   E-3 (5 min)   -> decide o montador
   E-1 (20 min)  -> decide se há estrutura       <- o ensaio que decide
   E-2 (15 min)  -> fecha a tabela dos nove degraus
   E-6 (5 min)   -> fecha o negativo de transporte
        |
   E-5 (30 min)  -> só depois que E-1 e E-3 disserem onde o payload mora
```

**O E-5 vem por último de propósito.** Ele é o mais caro e o mais sedutor, e
rodá-lo antes do E-1 é escrever um codificador Opus para um formato que ninguém
sabe se existe naquela posição. Se o E-1 mostrar que o excedente tem estrutura,
o E-5 nasce sabendo onde pôr o bloco.

---

## 6. O que fica escrito no mapa, e com que grau, quando cada ensaio fechar

| ensaio | célula | o que ela pode passar a dizer |
|---|---|---|
| E-2 | `audio.saida_dedicada`, rádio | *"a escada de OUTPUT `0x31`-`0x39` é ACEITA pelo firmware (medido, 15/08, N unidades). O conteúdo do payload além do `common` NÃO foi identificado."* |
| E-1 | idem | *"o excedente é ignorado nas posições A, B e C"* **ou** *"o excedente tem estrutura na posição X"* |
| E-3 | canônica, seção do envelope BT | o byte `[2]` é tag TLV / é constante de envelope |
| E-4 | linha nova para o `0xF6` | existe, tem N bytes, é constante entre unidades / difere por unidade |
| E-5 | `audio.saida_dedicada`, rádio | **só aqui** a palavra "alto-falante" pode aparecer com grau `O APARELHO OBEDECEU` |
| E-6 | linha de transporte | a escada é exclusiva do rádio (medido nos dois braços, no mesmo minuto) |

**Enquanto o E-5 não fechar, nenhuma célula do mapa pode dizer que existe saída
de som por rádio.** O que ela pode dizer é o que o E-2 provar: que o canal
existe e que o firmware responde.

---

## 7. O que esta sprint NÃO prova, repetido no fim de propósito

Está na seção 0 e está aqui de novo porque quem lê uma sprint de bancada lê o
começo e o fim, e o meio quando precisa:

- **Não sabemos o que o payload carrega.** Nem um byte além do `common` foi
  identificado.
- **Não existe ponte de áudio de saída.** Zero linhas de código, e o E-5 é um
  script de bancada, não produto.
- **Não está provado que os degraus `0x33`-`0x38` executam.** Só `0x31`, `0x32`
  e `0x39` foram tocados.
- **Não está provado que o excedente é áudio.** É hipótese forte, e a diferença
  entre hipótese forte e fato é a razão de esta casa existir do jeito que existe.
- **O que está provado, e é bastante:** o canal existe, transporta 552 bytes, e o
  firmware executa o que mandamos por ele.
