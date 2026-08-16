# SEMPRE IDENTIFICADO? — a resposta é sim, é o MAC, e o buraco é outro

- **Escrito em:** 15/08/2026, noite, na branch `restauro/inicio-da-sessao`.
- **A pergunta, textual, dela:** *"nos 4 controles via cabo e bt vamos ter
  sempre identificado né?"*
- **Grau:** **MEDIDO** nos quatro controles, nos dois transportes, em 15/08 às
  22h12. Leitura pura — nenhum byte foi escrito para responder esta pergunta.

---

## A resposta em trinta segundos

**SIM.** O produto sempre sabe qual controle é qual, no cabo e no rádio.

**O identificador é o MAC.** Ele sai de graça no `HID_UNIQ` do sysfs — sem
root, sem abrir hidraw, sem broker, sem escrita, e igual nos dois transportes.
O aparelho confirma o mesmo valor por dentro, no feature `0x09`.

**Onde falha:** o MAC identifica o **aparelho**, não o **jogador**. Qual
controle está alimentando qual vpad continua não observável sem apertar botão.
E o crachá só vale enquanto o controle está conectado — os dois do rádio
desligaram sozinhos por ociosidade nove minutos depois desta medição.

**E a cor?** Fechou em 4 de 4 pelo cabo, e os quatro concordam com o nome que
você usa. Mas ela **não é** o identificador: ela exige uma escrita que o rádio
recusa, e ela colide no dia em que você comprar dois controles da mesma cor.
A cor é o **nome**; o MAC é o **crachá**. São coisas diferentes, e as duas
servem.

---

## 1. A cor: 4 de 4, e nenhum discordou de você

Às 19h você trocou os braços. Os dois controles que nunca tinham sido medidos
foram para o fio, e às 22h09 eles responderam.

| aparelho | `hardware_version` | o firmware diz | você chama de | bate? |
|---|---|---|---|---|
| `14:3a:9a:00:00:ab` | `0x00000711` | **00 — White** | **BRANCO** | **sim** |
| `44:46:48:00:00:03` | `0x00000811` | **02 — Cosmic Red** | **VERMELHO** | **sim** |
| `a0:fa:9c:00:00:f0` | `0x00000710` | 04 — Galactic Purple | (roxo) | sim |
| `d4:2f:4b:00:00:d8` | `0x00001111` | 05 — Starlight Blue | (azul) | sim |

Quatro unidades, quatro códigos distintos, **zero discordância**. A medição por
cabo passou de 2 para 4 unidades.

Cada escrita teve prova de vida antes e depois: feature `0x20` idêntico byte a
byte, `hardware_version` idêntico, 3 de 3 relatórios de entrada, lightbar
inalterada. E o transporte foi **conferido no relatório de entrada** (`0x01` =
USB), não suposto — plugar o cabo pode não trocar o transporte, e aqui trocou.

### O achado de graça: o `EIO` do rádio está julgado

O `44:46:48` é o **mesmo aparelho** que às 14h47 recusou o comando por rádio,
com `EIO` imediato nas duas tentativas. Às 22h09, no fio, ele aceitou o
mesmíssimo comando e devolveu o serial.

Mesmo aparelho, mesmo comando, mesmo dia, só o transporte mudando. É o ensaio
dos dois lados que `scripts/eliminacao.py` exige, e ele agora dá
**`e-a-causa`**:

- a **unidade** está inocentada — não é "aquele controle não sabe responder";
- o **transporte rádio** é a causa da recusa, com prova causal.

O que **continua em aberto**: quem recusa — o firmware do controle, ou a pilha
HIDP/L2CAP do BlueZ. O `EIO` não distingue os dois, e nenhuma escrita nova saiu
por rádio: sua autorização desta noite cobria os dois do cabo, e só eles.

---

## 2. O crachá: cinco candidatos, e só um é crachá de verdade

Cinco feature reports diferiram em 4 de 4 unidades no censo das 19h26. Fui ler
os cinco nos quatro controles, duas vezes cada um, nos dois transportes.

**Os cinco passaram nos três critérios** — distinguem 4 em 4, saem nos dois
transportes, não exigem escrita, e são estáveis entre duas leituras.

**E isso é exatamente onde a contagem engana.** Olhando o *conteúdo* e não a
contagem:

| report | o que ele realmente é | serve de crachá? |
|---|---|---|
| **`0x09`** (20 B) | **É o MAC.** `buf[1..6]` = MAC do controle invertido; `buf[10..15]` = MAC do host pareado | **sim** |
| `0x0b` (42 B) | o mesmo MAC, na mesma posição, com mais campos | sim, mas é cópia |
| `0x22` (64 B) | `buf[3..4]` = revisão de placa; `buf[17..22]` = **o MAC** | só porque **embute** o MAC |
| `0x20` (64 B) | data e hora de compilação do firmware em ASCII | **não — agrupa por placa** |
| `0x05` (41 B) | calibração de fábrica da IMU | não — é trim analógico, e reescrevível |

### Por que o `0x20` não serve, e por que isso importa

Os 19 primeiros bytes do `0x20` são a data de compilação do firmware, e nesta
mesa elas **colidem em pares**:

```
  " Jul  4 2025 10:10:32"  ->  a0:fa:9c  E  14:3a:9a
  " Jul  4 2025 10:38:40"  ->  d4:2f:4b  E  44:46:48
```

Os bytes 48-56 colidem nos mesmos pares. O que resta de distinto no `0x20` são
os bytes 24-25 — que são o `hardware_version`, de novo a placa. E os bytes
60-63 "diferem entre braços" por um motivo que não é identidade nenhuma: no
rádio eles são o CRC-32 do envelope de Bluetooth, no cabo são zeros.

**O `0x20` agrupa por revisão de placa, não por unidade.**

### Sobre o `hardware_version`

Uma correção ao que eu tinha recebido: nesta mesa os quatro valores são
**distintos** (`0x0710`, `0x0711`, `0x0811`, `0x1111`) — nenhum é compartilhado.
Mas isso não o promove a identificador, e o mapa já dizia isso desde a manhã:
é **revisão de placa**, e separa os quatro controles dela **por acaso de lote**.
Dois controles comprados juntos teriam o mesmo valor.

---

## 3. A armadilha da universalidade, e ela é o coração disto

Seus quatro controles são de **quatro revisões de placa diferentes** e de
**quatro cores diferentes**. É a amostra mais favorável que existe — e é
justamente por isso que ela **esconde a colisão**.

Nesta mesa, "distingue 4 em 4" é verdade para o `hardware_version`, para a cor,
para o `0x20` e para o `0x05`. Num PC qualquer, com dois DualSense brancos
comprados no mesmo dia, **todos os quatro colidem no mesmo instante**. A única
coluna que continua distinguindo é o MAC.

Por isso a promoção a "universal" não vem da contagem — vem do **mecanismo**:

> o MAC é atribuído na **fabricação**; a cor, a placa e a data de firmware são
> atribuídas ao **lote**.

`n = 4` é amostra. O que generaliza é o mecanismo, não o placar.

---

## 4. Identificar não é mirar — e isto não repropõe o que você derrubou

Em 13/08 você derrubou o **alvo por MAC** como estratégia de produto: perfil
amarrado a endereço, allowlist por endereço, o usuário tendo de saber o MAC do
próprio controle. **Isso continua derrubado, e nada aqui o repropõe.**

A distinção importa e é esta:

| | **ALVO** (derrubado) | **IDENTIFICAÇÃO** (o que esta medição fecha) |
|---|---|---|
| quem usa | o usuário, na interface | o produto, por dentro |
| aparece na tela? | sim — e era esse o problema | **não, nunca** |
| serve para | amarrar perfil a um endereço | saber que o controle A é o mesmo A de dez minutos atrás |

O MAC serve perfeitamente como **chave interna de correlação**, e é ruim como
**vocabulário de interface**. As duas coisas são verdade ao mesmo tempo.

Para a tela, o léxico que já existe continua sendo o certo — e agora a **cor**,
lida do próprio aparelho e confirmada em 4 de 4, é candidata natural a nome
visível: "o vermelho" é o que você já diz.

---

## 5. Onde a resposta falha — os dois buracos, sem suavizar

### Buraco 1 — identifica o APARELHO, não o JOGADOR

Qual vpad é alimentado por qual MAC **continua não observável sem apertar
botão**. O `quem_e_quem.py` diz isso em todas as rodadas de hoje, e a razão é
que o `state_full` publica `coop.players` como um **número**, não como lista.

Então, em uma frase: **identificar o aparelho, sempre; amarrar aparelho a
jogador, não** — não sem apertar botão, ou sem enriquecer o estado publicado.
São duas perguntas, e só a primeira está fechada.

Esta é, aliás, a curadoria mais barata que sobrou: publicar a lista de `uniq`
por jogador no `state_full` é mudança de dado, não de protocolo.

### Buraco 2 — o crachá só vale com o controle conectado

Às **22h21**, nove minutos depois da medição, os **dois controles do rádio
sumiram**: um passou a devolver `EIO` em tudo, e o nó do outro desapareceu do
sistema de arquivos. O censo achou "2 controles, só cabo".

> **Eu escrevi aqui, primeiro, que a causa provável era o desligamento
> automático por ociosidade. Estava errado, e a medição seguinte derrubou.**
> Às **22h43** o censo achou os quatro de novo — e os dois que tinham sumido
> estavam **no CABO**, com os outros dois no rádio. Os braços foram trocados
> **outra vez**. Um controle que se desliga por ociosidade não reaparece no USB
> sozinho; alguém o moveu. A hipótese do sono caiu por uma leitura de 3 s, e
> fica registrada aqui só para que ninguém a levante de novo achando que é
> nova.

O buraco continua existindo, mas o preço dele é outro: **o crachá é contínuo
enquanto o aparelho está conectado, e nada mais.** Trocar de braço, cair o
rádio ou desligar o controle interrompem a identificação — não a corrompem. Ao
voltar, o MAC é o mesmo, que é exatamente a propriedade que se quer.

**Efeito colateral bom, e é de graça:** com esta terceira configuração, **cada
um dos quatro controles já passou pelos dois transportes** ao longo de 15/08.
Nenhum deles é "o do cabo" ou "o do rádio" — os quatro são os dois.

---

## 6. O que entrou no mapa

| linha | o que mudou |
|---|---|
| `identidade.cracha_nos_dois_transportes@dualsense` | **LINHA NOVA** — a resposta a esta pergunta, que não morava em célula nenhuma |
| `identidade.cor_do_aparelho@dualsense` | a cor por cabo passou de **2 para 4 unidades**; o `EIO` do rádio ganhou o veredicto de causa |
| `identidade.req_dev_info@dualsense` | `cabo_de_onde_sei` subiu de `inferido-do-codigo` para **`medido`** — o `0x09` foi lido no fio |
| `identidade.revisao_de_placa@dualsense` | a ressalva "é lote, não unidade" ganhou **medida** (a colisão em pares do `0x20`) |

Oito linhas novas em `docs/data/ensaios.csv`, com a coluna `presente` dos dois
lados. O julgador fecha **`e-a-causa`** em duas frentes: o transporte rádio
como causa da recusa da cor, e "carregar o MAC" como a propriedade que faz um
report distinguir por unidade.

O portão `check_paridade_transporte.py` fecha **verde** (0 afirmações fortes
sem teste que morda; 0 graus fortes sem ensaio no caderno), e o `specs.html`
foi regerado — 302 linhas.

---

## 7. O que este estudo NÃO prova

- **Não prova que a cor sai por rádio.** Sai no cabo em 4 de 4; por rádio a
  escrita foi recusada em 1 unidade, 2 tentativas. São duas afirmações.
- **Não diz quem recusa no rádio** — firmware ou BlueZ. O `EIO` não distingue.
- **Não toca as 153 células mudas** do Pro Controller e do 8BitDo: não há Pro
  nem 8BitDo nesta mesa.
- **Não amarra vpad a MAC.** É o buraco 1, e ele continua aberto.
- **Não mede unidade nenhuma além destas quatro.** O que sustenta a
  generalização é o mecanismo do MAC, e está escrito como mecanismo — não como
  placar.
