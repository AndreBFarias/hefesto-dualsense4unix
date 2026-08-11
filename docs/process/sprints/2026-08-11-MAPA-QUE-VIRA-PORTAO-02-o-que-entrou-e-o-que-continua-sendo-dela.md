# MAPA-QUE-VIRA-PORTÃO-02 — o que entrou, e o que continua sendo dela

- **Escrito em:** 11/08/2026, na branch `restauro/inicio-da-sessao`
- **Rótulo:** `LEVANTAMENTO MEDIDO` — e três perguntas abertas, que são dela
- **Grau:** **MEDIDO**. Cada número desta página foi contado hoje, no disco de
  hoje, e a régua está declarada ao lado de cada um. Nenhum veio de leitura de
  documento.
- **Nasceu de:** o mapa de canais entrou no commit `a2a9429` (11/08, 01:51) e
  **a documentação de processo não acompanhou** — o índice ainda afirmava, no
  cabeçalho, que *"nenhuma linha destas sprints virou código ainda"*, e a
  MAPA-TELA-01 ainda dizia que *"não existe uma linha de `specs.html` ainda"*.
  Documento que nega o disco é pior que documento que falta: ele é convincente.

---

## 1. O que entrou no commit `a2a9429`

Doze arquivos, 5.208 linhas. O que importa deles, medido com `os.path.getsize`,
`wc -l` e contagem direta sobre o CSV com o mesmo leitor que o gerador usa
(`csv.DictReader`):

| o que | onde | medida de hoje |
|---|---|---|
| A tela | `specs.html` | no commit: 669.050 bytes = **653 KB**, 1.172 linhas, zero requisição de rede |
| O dado | `docs/data/mapa-controles.csv` | **264 linhas** (88 chaves x 3 controles), 45 colunas |
| O gerador | `scripts/gerar-mapa.py` | CSV → tela, com `--check` embutido |
| A migração | `scripts/migrar-mapa-v2.py` | prova campo a campo do v1 para o v2 |
| A bancada | `bancada.py` | a superfície de medição, que escreve no mesmo CSV |
| O caderno | `scripts/eliminacao.py` + `docs/data/ensaios.csv` | **14 ensaios**, todos de 03/08 e 10/08 |
| O v1 | `docs/data/mapa-controles-v1.csv` | 204 linhas, guardadas — medição não se apaga |

Os desenhos vieram antes, no `dad60ae` de 10/08: três SVG com **76 grupos
nomeados** ao todo (26 no DualSense, 27 no Nintendo Pro, 23 no 8BitDo SN30 Pro),
contados por expressão regular sobre `<g ... id="...">`, sem órfão e sem id
repetido.

## 2. O que a tela mostrou, na régua do v2

O v1 contava por linha, e cada linha era um transporte. O v2 põe os dois lados
na mesma linha, então a unidade que se compara é a **célula** — 264 linhas x 2
transportes = **528 células**. Contadas duas vezes hoje, com a mesma regra que o
gerador aplica na tela, porque **o CSV estava sendo preenchido no meio do
caminho** por outra frente desta leva:

| | às 03h | às 10h18 |
|---|---:|---:|
| ● o Hefesto aciona | 75 | 121 |
| ◐ o aparelho aceita, o produto não faz | **101** | 114 |
| ○ o aparelho não aceita por aquele transporte | 82 | 97 |
| ◌ ninguém respondeu por este transporte | **270** | **196** |
| ≠ cabo e rádio divergem, na mesma linha | 16 | **23** |

**O ◌ é o retrato honesto desta casa: o mapa nasceu com mais da metade em
silêncio, e o silêncio não é recusa.** Confundir os dois foi o que produziu as
regressões dela, e é por isso que o quarto símbolo teve de existir.

Duas ressalvas, para o número não ser lido como troféu: as duas colunas medem
**quanto se sabe**, não quanto o produto passou a fazer; e o número vivo é
sempre o que o `specs.html` publica, que desde hoje tem portão garantindo que
não fique atrás do CSV.

Por controle, às 10h18, o que o produto **aciona** de tudo o que o aparelho
**tem**: DualSense 50 de 62, Nintendo Pro **8 de 30**, 8BitDo SN30 Pro 12 de 29.

## 3. O que esta leva de 11/08 está fechando, e o que não

Várias frentes correram hoje. Esta página é uma delas, e só pode falar com
segurança do que mediu — por isso o estado abaixo tem hora:

| frente | estado às 10h18 de 11/08 |
|---|---|
| Ligar o portão do mapa | **no disco**: o `--check` roda no CI e no pre-commit, e entrou o `scripts/check_paridade_transporte.py` |
| Fazer o transporte virar dimensão do teste | **no disco, em parte**: a fixture parametrizada nasceu em `tests/conftest.py` e 40 casos a pedem |
| Preencher o que falta no CSV | **em curso**: `teste_que_morde` saiu de 0 para 39 linhas durante a manhã |
| Reconciliar a canônica do protocolo | **em curso**: os três documentos de `docs/protocol/` mudaram na mesma janela |
| Fazer os documentos de processo contarem a verdade | **feito nesta página** |

**Nenhuma das outras quatro frentes estava commitada quando isto foi escrito** — o
trabalho estava na árvore. A regra da casa é que *a árvore de trabalho é o que
roda*, e é contra ela que os rótulos foram medidos.

O que esta frente fechou, nominalmente: o cabeçalho do
[índice](2026-08-10-INDICE-o-mapa-que-vira-portao.md) e o da
[MAPA-TELA-01](2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md) pararam de
negar o disco; as oito sprints da tabela de execução ganharam rótulo medido; os
números do v1 ganharam o número do v2 ao lado, sem que nenhum fosse apagado; e
as três isenções `ref-externa` que diziam *"ainda não existe"* sobre
`bancada.py`, `scripts/gerar-mapa.py` e `scripts/check_paridade_transporte.py`
saíram — os três existem, e agora o portão de referências os guarda de verdade,
em vez de ser calado por um comentário.

**Três defeitos foram achados por medição enquanto se escrevia isto**, e os três
estão registrados com nota datada no documento de origem:

1. **O commit se chama "e ele é portão — não documentação", e passou oito horas
   sem ser portão.** Entre 01h51 e a manhã, o `--check` existia, respondia certo
   à mão e **ninguém o chamava** — nem o CI, nem o `.pre-commit-config.yaml`,
   nem teste algum. É a
   [ENTREGA-QUE-NÃO-LIGOU](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
   na forma clássica. Curado no mesmo dia, por outra frente; o registro fica
   porque o intervalo é a lição, não o defeito.
2. **O "(357 KB)" da MAPA-TELA-01 nunca descreveu este arquivo.** No próprio
   commit que escreveu a linha, `specs.html` já tinha 669.050 bytes. Não é
   número que caducou: é número que nasceu errado, quase o dobro.
3. **O mapa nasceu com o ponto morto que o índice tinha avisado.** A seção 5 do
   índice exigia **linhas de combinação** — o controle no cabo matando a saída
   do que está no rádio. O CSV entregue tem **zero**. A migração pôs cabo e
   rádio na mesma linha, o que resolve comparar os dois; não resolve os dois
   **ao mesmo tempo**, que é o caso que ela mais usa.

E um quarto, no material de pesquisa: o índice publicava *"`parametrize`
cruzando os DOIS transportes: 0, de 233"* e o medido é **1 de 233** — o
decorador já existia desde 08/08. O diagnóstico não muda de lado, porque esse
caso é de interface e não toca byte nenhum, mas o número publicado estava errado
e agora tem nota. **Esse número viajou:** o cabeçalho da fixture nova, em
`tests/conftest.py`, copia a tabela inteira do índice, o zero incluído. Quem for
mexer ali herda a correção — o certo é 1 de 233, e o argumento da fixture
continua de pé sem depender do zero.

## 4. As três perguntas que são dela — RESPONDIDAS em 11/08/2026

> **Nota de 11/08/2026.** As três foram respondidas por ela no mesmo dia, poucas
> horas depois de escritas. As perguntas ficam abaixo como estavam — não se
> apaga o que se perguntou, porque a resposta só se entende com ela ao lado —
> e cada uma ganhou a resposta logo em seguida, com o que destravou.

Nenhuma destas três se responde com código, medição ou pesquisa. Todas travam
alguma coisa hoje.

### Pergunta 1 — de quem é o desenho dos controles?

Os três desenhos vieram prontos, de fora, e hoje viajam **dentro** do
`specs.html`, que é o arquivo que vai no release. Em 10/08 você decidiu deixar
como está por ora.

> **A pergunta:** antes de o mapa sair num release, você quer que a gente
> escreva de onde os desenhos vieram (e o crédito, se houver)? Ou continua como
> está, e a gente escreve isso no dia em que for mexer neles?

**RESPOSTA DELA (11/08/2026), literal:** *"não me lembro a origem correta, mas
editamos eles."*

O que isso fixa, e o que não fixa. **Fixa** que os desenhos de hoje são **obra
derivada**: partiram de arte de terceiro e foram editados aqui. **Não fixa** a
procedência, porque ela não é lembrada — e ninguém deve inventá-la depois para
fechar um campo.

Fica escrito assim, com todas as letras, porque é o estado verdadeiro:

- os SVG em `assets/control-svg/` são derivados de arte externa de **origem não
  lembrada**, editada neste repositório;
- o `LICENSE` é **MIT** — não GPL-3 — e uma atribuição futura respeita isso;
- **isto é um risco aberto de licença, não um item fechado.** Se um dia a
  origem aparecer, ela entra aqui com data, e a decisão de crédito é dela.

Uma sugestão, para quando ela quiser: os três desenhos podem ser **redesenhados
do zero** a partir dos aparelhos que estão na mesa dela. Custa uma tarde e
elimina a dúvida em vez de administrá-la. Não é urgente e não bloqueia nada.

### Pergunta 2 — onde ficam as luzinhas de jogador do Nintendo Pro?

Que elas existem, o repositório sabe. **Onde ficam no aparelho, não está escrito
em lugar nenhum** — e por isso o grupo nasceu no desenho marcado como
`nao-localizada`. A lightbar do DualSense está na mesma situação, pelo mesmo
motivo.

> **A pergunta:** dá para você tirar uma foto do seu Pro com as luzinhas de
> jogador acesas — e uma do DualSense com a lightbar acesa? Uma foto de cada
> fecha as duas, e o desenho passa a acender a peça certa quando a tabela a
> seleciona.

**RESPOSTA DELA (11/08/2026):** duas fotos, do Pro e do 8BitDo, com as palavras
*"pro controller fica na parte de baixo"* e *"no 8bitdo fica na parte de baixo.
esses são os leds do player"*.

**O que as fotos mostram:** quatro LED numa faixa recuada na **aresta frontal**,
entre os grips, no vão que os ombros deixam. No Pro, dois acesos e dois
apagados; no SN30, três acesos e um apagado.

**Duas coisas fecharam, e uma delas ninguém tinha perguntado:**

1. `nintendo-pro.svg` sai de `data-posicao="nao-localizada"` e passa a ter os
   quatro LED desenhados.
2. **O SN30 não tinha grupo nenhum.** O desenho não representava os LED de
   jogador dele, então o mapa nem sabia perguntar por eles. O grupo nasceu
   nesta leva, junto com a peça.

**A geometria não é estimativa** — saiu dos marcos de cada desenho. No Pro,
`ZL`/`L` ocupam `x 19..39` e `ZR`/`R` ocupam `x 61..81`, deixando o vão em
`x 39..61` (centro 50), com a aresta superior do corpo em `y 20.5`. No SN30, o
ombro `L` ocupa `x 55..163` e o `R` ocupa `x 337..445`, vão em `x 163..337`
(centro 250), aresta em `y 75`. Os dois foram **renderizados e olhados** depois
de desenhados, e não só escritos.

**Sobre "parte de baixo".** No aparelho na mão, a faixa fica na aba inferior da
aresta frontal — é o que ela vê e é o que ela disse. Numa vista de cima, que é
como estes desenhos são feitos, a mesma aba projeta no topo, entre os ombros.
As duas leituras concordam sobre **qual extremidade do controle**, e é a
extremidade que o mapa precisa saber. Fica registrado porque quem ler o CSV e o
SVG lado a lado vai estranhar a diferença de palavra.

**Continua aberto:** a **lightbar do DualSense** segue `nao-localizada` em
`dualsense.svg`. Ela não foi fotografada nesta rodada, e desenhar de memória
seria exatamente o que esta sprint recusa. Uma foto fecha.

### Pergunta 3 — quem tem direito de escrever "provado"?

Esta é a que mais custa: **três colunas do mapa estão vazias nas 264 linhas** —
`provado_em`, `provado_por` e `validade_dias` — porque ninguém tem autorização
para escrevê-las. Enquanto isso, *"nunca tentei"* aparece igual a *"tentei e
falhou"*, e essa confusão é a doença que o mapa existe para curar.

> **A pergunta:** para o mapa dizer que uma feature está **provada**, o que
> vale?
>
> - **(a)** ter lido em documento nosso ou de fora;
> - **(b)** você ter visto funcionar, com o controle na mão;
> - **(c)** só um teste automático que reprove quando aquilo quebrar.
>
> Pode valer mais de um, desde que fique escrito qual foi. E, se valer (b), por
> quanto tempo continua valendo antes de precisar ser visto de novo?

**RESPOSTA DELA (11/08/2026), literal:** *"vc no caso tem o direito de escrever,
vamos ir validando juntos ponto a ponto e vc vai isolando."*

Ela delegou a caneta e **manteve a validação**: escrevo, e a conferência é
junto, um ponto por vez. Isso não é licença para afirmar mais — é obrigação de
afirmar com procedência anexada, porque quem confere depois é ela.

### A régua que passa a valer

Três valores em `provado_por`, e cada um tem prazo próprio:

| `provado_por` | o que significa | `validade_dias` |
|---|---|---|
| `teste` | há teste que **reprova** quando aquilo quebra, naquele transporte | **vazio** — o CI reprova a cada run; prazo seria burocracia |
| `aparelho` | observado no controle dela: descritor lido, foto dela, ou ela vendo funcionar | **180** |
| `descritor` | lido do descritor HID do próprio aparelho, sem escrita | **180** |

E a resposta ao item **(a)** da pergunta é **não**: *ter lido em documento não é
prova*. Continua sendo `afirmado-no-doc` na coluna de confiança, e **nunca**
preenche `provado_por`. Foi documento convincente e não medido que produziu as
regressões que este mapa existe para impedir.

Por que 180 dias, e não "para sempre": o **plástico** não muda, mas o firmware
do controle, o kernel e o nosso código mudam — e o que a célula afirma é a
relação entre os três, não o aparelho sozinho. Meio ano é o intervalo em que
esta casa já viu uma feature caducar sem ninguém notar (a regra udev 76 do
touchpad levou 25 dias; o `hid_capture_bt.bin` do ADR-008 levou meses). Se na
prática o prazo incomodar, ele muda com uma nota datada — é número, não dogma.

**O que isso destravou hoje:** quatro linhas saíram de vazias e ganharam a linha
de provado — `luz.led_jogador` do Pro e do SN30 (por `aparelho`, a foto dela) e
`audio.alto_falante` e `plataforma.escrita_crua` do DualSense (por `descritor`,
a leitura de 11/08). As demais continuam vazias, e vazias querem dizer
exatamente o que parecem: ninguém provou ainda.

## 5. Nota datada de 11/08/2026 — o que ficou escrito, e onde

| documento | linha | o que passou a dizer |
|---|---|---|
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md` | `:13-24` | que o cabeçalho de 10/08 caducou no `a2a9429`, e onde ler o estado de hoje |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md` | `:51-63` | que o "0 de 233" era 1 de 233, com a régua e o commit |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md` | `:108-125` | a contagem do v2 ao lado da do v1, sem apagar a do v1 |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md` | `:132-194` | a coluna Rótulo, com as oito sprints medidas uma a uma |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md` | `:220-226` | que o mapa nasceu sem as linhas de combinação |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md` | `:12-24` | o rótulo novo, o anterior por extenso, e o que falta ela validar |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md` | `:58-68` | que o portão nasceu sem chamador e ganhou um na mesma manhã |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md` | `:118-125` | que a tela nasceu com quatro símbolos, não três |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md` | `:197-212` | que o "(357 KB)" nasceu errado, e que o item aberto é aberto por desenho |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md` | `:237-266` | a contagem do v2, em células, ao lado da do v1 |

**O que continua aberto depois desta página, nominalmente:**

1. **As três perguntas da seção 4** — e só ela as responde.
2. **A prova de tela da MAPA-TELA-01** — a foto antes e depois, e a palavra dela.
3. **As linhas de combinação** da `MAPA-CSV-01`, que não nasceram: zero, medido
   às 10h18, com o preenchimento do CSV já em curso.
4. **As cinco colunas ainda 100% vazias** do mapa — e três delas (`provado_em`,
   `provado_por`, `validade_dias`) esperam a resposta da pergunta 3.
5. **`PARIDADE-BYTE-01`, `PARIDADE-FORMA-01`, `UNIDADE-COR-01` e `BANCADA-01`** —
   as quatro continuam abertas, e a justificativa medida de cada uma está na
   seção 4 do [índice](2026-08-10-INDICE-o-mapa-que-vira-portao.md).

**Saíram desta lista durante a própria leva:** a `PARIDADE-PORTAO-01`, inteira,
e metade da `PARIDADE-BYTE-01`. Quando esta página começou a ser escrita, o
validador `scripts/check_paridade_transporte.py` não existia e a suíte não tinha
uma única fixture parametrizada por transporte; às 10h18 o validador estava no
disco com o CI chamando, e a fixture existia com 40 casos rodando dos dois
lados. Fica registrado assim, e não apagado, porque é o exemplo mais curto do
que este repositório aprendeu a temer: **entre "escrito" e "ligado" cabem oito
horas e uma frase de commit que promete o que ainda não é verdade.**
