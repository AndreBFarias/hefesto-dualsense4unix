# MAPA-TELA-01 — o layout do mapa de canais

- **Estado:** CONCLUÍDA — `specs.html` (1215 linhas) abre sem servidor, `scripts/gerar-mapa.py` o gera do CSV, `bancada.py` está na raiz e o portão `scripts/check_paridade_transporte.py` já tem chamador (verificado em 21/08/2026)
- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"a ideia aqui é termos um mapa rápido que nos permita ver por
  qual canal via bluetooth acionamos o lightbar e por qual canal via cabo
  acionamos o lightbar. Mas isso pra todas as features de cada controle de tal
  forma vamos conseguir finalmente enxergar o todo, e pararmos com as tentativas
  e erros desesperadas."*
- **Grau:** os DESENHOS estão medidos e entregues (10/08). O LAYOUT abaixo é
  proposta — não existe uma linha de `specs.html` ainda, e a palavra final sobre
  a tela é dela ([PROVA-DE-TELA-01]).
- **Rótulo em 11/08/2026:** `ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA`
- **Rótulo anterior, preservado por extenso:** *"os DESENHOS estão medidos e
  entregues (10/08). O LAYOUT abaixo é proposta — não existe uma linha de
  `specs.html` ainda, e a palavra final sobre a tela é dela"*
- **O que falta ela validar, em uma linha:** abrir o `specs.html` com dois
  cliques e dizer se aquela é a tela que ela pediu — se não for, o desenho muda.

> **Nota de 11/08/2026 — a frase "não existe uma linha de `specs.html` ainda"
> caducou no commit `a2a9429` (11/08, 01:51).** O arquivo existe, tinha 653 KB
> naquele commit e abre sem servidor; `scripts/gerar-mapa.py` o gera a partir do CSV e
> `bancada.py` está na raiz, como esta sprint desenhou. O que continua aberto é
> **um item só**, o da seção 8: a foto antes e depois, e a palavra dela. Esse
> item está aberto **por desenho, não por esquecimento** — ele É a prova de tela.

---

## 1. A pergunta que a tela tem de responder em um relance

> *Por qual canal, e com qual comando exato, eu aciono esta feature — por cabo?
> e por Bluetooth?*

Tudo o que não servir a essa frase é enfeite e sai do desenho.

E uma segunda, que só aparece quando o mapa existe:

> *Onde estão os buracos?* — quais features são provadas no cabo e nunca no
> rádio. Essa lacuna **é** a causa das regressões dela, e é o produto mais
> valioso da tela.

## 2. As duas superfícies, e por que são duas

Decisão dela de 10/08: **as duas**, lendo o mesmo CSV. A bancada mora em
`bancada.py`, na raiz. <!-- criado em 11/08/2026, commit a2a9429; a isenção ref-externa saiu porque o arquivo existe e o portão agora o guarda -->

| | `specs.html` | a bancada (Streamlit) |
|---|---|---|
| Para que serve | Consultar, versionar, abrir em qualquer lugar | Medir com o controle na mão |
| Como abre | Duplo clique, sem servidor | `streamlit run`, precisa do venv |
| Quem escreve no CSV | ninguém — é só leitura | ela, durante a medição |
| Vai para o release | **sim** | não |

O `specs.html` é gerado do CSV por `scripts/gerar-mapa.py`, e um portão reprova <!-- criado em 11/08/2026, commit a2a9429; a isenção ref-externa saiu porque o arquivo existe e o portão agora o guarda -->
se ele estiver mais velho que o CSV. Assim a tela nunca mente por atraso — a
mesma disciplina de `retratar_abas.py`, que já impede a documentação de
envelhecer.

> **Nota de 11/08/2026 — o gerador nasceu sem portão, e ganhou um no mesmo dia.**
> Às 03h de 11/08 o `--check` estava escrito, respondia certo quando chamado à
> mão e **ninguém o chamava**: nem o CI, nem o `.pre-commit-config.yaml`, nem
> teste algum. A frase *"um portão reprova"* descrevia uma intenção, não uma
> garantia — a
> [ENTREGA-QUE-NÃO-LIGOU](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
> na forma clássica. Às 10h18, medido de novo, o fio estava ligado por outra
> frente da mesma leva: o `--check` roda no CI e no pre-commit, e entrou junto o
> `scripts/check_paridade_transporte.py`, que morde por conteúdo. **As duas
> medições ficam escritas**, porque a distância entre elas é a lição: o mesmo
> commit que se chamava "portão" passou horas sem ser um.

## 3. O layout

Três faixas, de cima para baixo. Nada de abas: a comparação entre controles é o
ponto, e aba esconde justamente o que se quer comparar.

```
┌────────────────────────────────────────────────────────────────────────┐
│  Hefesto — mapa de canais            [cabo] [Bluetooth] [os dois]      │  A
├────────────────────────────────────────────────────────────────────────┤
│    ╭─────────╮        ╭─────────╮        ╭─────────╮                   │
│    │DualSense│        │Nintendo │        │SN30 Pro │                   │  B
│    ╰─────────╯        ╰─────────╯        ╰─────────╯                   │
│   31/42 medidas      12/44 medidas       9/50 medidas                  │
├────────────────────────────────────────────────────────────────────────┤
│ FAMÍLIA   FEATURE            CABO          BLUETOOTH      PROVA        │
│ ───────────────────────────────────────────────────────────────────    │  C
│ luz       Lightbar RGB       ● sysfs       ● sysfs        medido 03/08 │
│ luz       Lightbar brilho    ◐ common[42]  ◐ common[42]   doc 01/08    │
│ vibração  Rumble             ● common[2-3] ● common[2-3]  ZERADA 10/08 │
│ gatilho   Adaptativo         ● common[10]  ○ sem teste    montou       │
│ ...                                                                    │
└────────────────────────────────────────────────────────────────────────┘
```

**Faixa A — o interruptor de canal.** Não é filtro: é o eixo da tela. Em `cabo`,
as colunas de Bluetooth somem e a tabela vira "o que funciona no fio". Em
`os dois`, aparece a coluna que importa de verdade — **a diferença**.

**Faixa B — os três desenhos, sempre os três.** Cada um pintado na cor da
unidade dela. Sob o nome, a razão medidas/features, que é o placar de honestidade
daquele controle. Clicar num desenho filtra a tabela; **passar o mouse sobre uma
peça acende a linha correspondente**, e o inverso também: passar na linha acende
a peça. É essa reciprocidade que faz o mapa ser mapa e não planilha.

**Faixa C — a tabela.** Uma linha por (feature, transporte). Ordenável, e com a
ordem inicial que interessa: **as assimetrias primeiro**.

## 4. Os três símbolos, e por que só três

| | significa |
|---|---|
| ● | o Hefesto aciona, e há teste que morde |
| ◐ | o aparelho aceita, mas o Hefesto não aciona — ou aciona sem teste |
| ○ | não existe, ou ninguém sabe |

O ◐ é o símbolo mais importante da tela: é **onde a casa sabe e o produto não
faz**, o defeito mais caro deste repositório. Ele não pode se parecer com o ●.

> **Nota de 11/08/2026 — a tela nasceu com QUATRO, e o quarto era necessário.**
> O ○ desta seção juntava duas coisas que não são a mesma: *"o aparelho não
> aceita por aquele transporte"* e *"ninguém respondeu por este transporte"*. Na
> tela entregue elas se separaram — o ○ ficou com a recusa e o **◌**, círculo
> pontilhado, ficou com o silêncio. Não é enfeite: o mapa nasceu com **270 das
> 528 células em ◌**, e ainda tinha 196 às 10h18 do mesmo dia. Tratar silêncio
> como recusa é a doença que este mapa existe para curar. A seção 4 fica como
> está; a régua de hoje são quatro símbolos.

## 5. A cor, e a decisão que a separa

Decisão dela de 10/08, em duas frases que não podem se misturar:

- **No mapa, a cor é da UNIDADE** — o plástico. Um Cosmic Red é vermelho hoje,
  amanhã, e com qualquer outro controle ligado ao lado.
- **Na lightbar, a cor continua sendo da POSIÇÃO** — quem é o jogador 1. Como
  hoje, sem quebrar o NUM-01.

São perguntas diferentes e cada uma fica no seu lugar. Se o mapa usasse a cor da
posição, desligar o controle da frente **repintaria** o de trás — e o mapa
deixaria de responder *"esta Cosmic Red está mapeada?"*, que é o motivo dele
existir.

Nos SVG isso já está pronto: o colorway entra por `data-colorway` no elemento
`svg` e pinta **só o contorno do corpo**. Trocar de cor é trocar um atributo.

## 6. O que o desenho já entrega para a tela

Os três SVG foram padronizados em 10/08 e carregam a semântica que o mapa
precisa. **76 grupos nomeados, nenhum órfão, nenhum id duplicado.**

```html
<g id="stick_l" data-entrada="stick_l" data-clique="l3" data-evdev="BTN_THUMBL">
    <title>Analógico Esquerdo (L3)</title>
```

- `id` — a chave de `BUTTON_GLYPH_LABELS`, a mesma do glifo e do widget da aba
  Status. Sem tradutor no meio.
- `<title>` — o rótulo PT-BR, que o navegador ainda mostra como tooltip de graça.
- `data-entrada` — o que o controle **envia**.
- `data-feature` — o que nós **acionamos ou lemos**. Só este tem canal, e é o que
  amarra a peça à linha do CSV.
- `data-evdev` — nos dois Nintendo, lido da fonte do driver desta máquina
  (`hid-nintendo.c:473-481`). Registra a armadilha de que **A e B ficam trocados**
  em relação ao layout PlayStation.

Feature sem corpo visível — giroscópio, motores, bateria — também tem lugar, em
`.oculta`: some por padrão e acende quando a tabela a seleciona. **Onde a coisa
mora no aparelho é informação, não enfeite.**

## 7. As armadilhas do desenho, que a tela herda

Quatro nasceram de defeito medido em 10/08 e estão comentadas dentro dos SVG:

1. **Subpath não é componente.** Partir os paths dava 231.898 pixels de erro: o
   traço fino é preenchimento com furo (`evenodd`), e partir um anel produz dois
   borrões. O par contorno+furo é que é o componente.
2. **O `<g>` do 8BitDo guarda o traço e um `translate` de 18 mil unidades.**
   Emitir os paths soltos: 52.413 pixels, desenho fora do `viewBox`.
3. **Elemento não-`<path>` some se a ferramenta só procurar `<path>`.** O
   Nintendo tem um `<circle>`, e o botão menos desaparecia inteiro.
4. **`width`/`height` com razão diferente do `viewBox`** faz o renderizador
   encaixar com tarja e deslocar meio pixel. Enganou duas vezes: uma medida deu
   posição relativa de **1,207** (impossível), e a prova acusou 19.968 pixels que
   eram só o deslocamento. Os três arquivos hoje **não declaram** `width`/`height`.

E uma que a tela herda direto: **o `librsvg` não entende `var()` do CSS.** O GTK
renderiza por ali; o navegador não. Por isso a cor de fábrica mora em atributo, e
o colorway entra por regra presa a `data-colorway`, inerte quando ninguém define.

## 8. O que fecha esta sprint

- [x] `scripts/gerar-mapa.py` — CSV → `specs.html`, autocontido, sem CDN <!-- criado em 11/08/2026, commit a2a9429; a isenção ref-externa saiu porque o arquivo existe e o portão agora o guarda -->
- [x] `specs.html` na raiz, abrindo por duplo clique (357 KB, zero requisição de rede)
- [x] `bancada.py` — a superfície de medição, lendo e ESCREVENDO no mesmo CSV <!-- criado em 11/08/2026, commit a2a9429; a isenção ref-externa saiu porque o arquivo existe e o portão agora o guarda -->
- [x] Portão `gerar-mapa.py --check` — provado nos três casos: fonte mais nova
      reprova (1), depois de regerar passa (0), arquivo ausente reprova (1)
- [ ] Foto antes e depois, e **a palavra final é dela** ([PROVA-DE-TELA-01])

> **Nota de 11/08/2026 — dois desta lista precisam de correção, e o último está
> aberto de propósito.**
>
> 1. **O "(357 KB)" nunca descreveu este arquivo.** Medido no próprio commit que
>    escreveu a linha: `git show a2a9429:specs.html` são **669.050 bytes = 653
>    KB**, e o arquivo no disco de hoje tem exatamente o mesmo tamanho. Não é
>    número que caducou, é número que já nasceu errado — quase o dobro. O texto
>    fica onde está, com esta nota ao lado.
> 2. **O quarto item dizia "Portão" horas antes de haver portão.** Às 03h de
>    11/08 o `--check` existia e respondia certo à mão (`specs.html:
>    atualizado`, saída 0), mas nenhum arquivo do CI, do
>    `.pre-commit-config.yaml` ou de `tests/` o chamava. Às 10h18 chamava — outra
>    frente da mesma leva ligou o fio e acrescentou o
>    `scripts/check_paridade_transporte.py`. Provado nos três casos era verdade
>    desde sempre; **ligado**, só depois — e a diferença entre as duas coisas é o
>    defeito mais caro desta casa.
> 3. **O quinto item continua `[ ]` por desenho.** Ele É a prova de tela dela; um
>    checkbox aberto aqui é o estado certo, não pendência esquecida. É por causa
>    dele que o rótulo desta sprint é `ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA
>    DELA` e não `ENTREGUE`.

## 9. O que a tela mostrou assim que existiu

**Esta tabela é do v1 — 204 linhas, uma por (controle, feature, transporte).**
A do v2 vem logo abaixo, ao lado, e os números não se comparam um a um porque o
grão mudou. Nada aqui foi reescrito.

Os números que só apareceram quando as 204 linhas ficaram lado a lado:

| | |
|---|---:|
| ● o Hefesto aciona | 69 |
| ◐ o aparelho aceita, o produto não faz | **75** |
| ○ não existe, ou ninguém sabe | 60 |
| ≠ cabo e rádio divergem | 22 |

**As lacunas superam o que o produto faz.** E as 22 assimetrias são a lista
nominal do que produziu as regressões dela — antes disso ninguém tinha essa
lista.

### 9.1 A mesma contagem no v2 — medida em 11/08/2026, com hora

O v2 tem **264 linhas** e cada uma carrega os **dois** lados, o que dá **528
células** (linha x transporte). É a célula que se compara com a linha do v1. A
coluna tem hora porque **o CSV estava sendo preenchido enquanto isto era
contado**, por outra frente da mesma leva:

| | às 03h de 11/08 | às 10h18 de 11/08 |
|---|---:|---:|
| ● o Hefesto aciona | 75 | 121 |
| ◐ o aparelho aceita, o produto não faz | **101** | 114 |
| ○ o aparelho não aceita por aquele transporte | 82 | 97 |
| ◌ ninguém respondeu por este transporte | **270** | **196** |
| ≠ cabo e rádio divergem, na mesma linha | 16 | **23** |

**O número vivo é o que o `specs.html` publica** — e, desde 11/08, há portão
garantindo que a tela não fique atrás do CSV. As duas colunas ficam aqui porque
a diferença entre elas é o trabalho de uma manhã, e apagá-la seria apagar a
medida do progresso.

Três leituras, e nenhuma delas é boa notícia:

- **O ◌ é o número novo, e nasceu maioria.** Mais da metade das células dizia
  "ninguém respondeu", que é diferente de "o aparelho recusa". Confundir esses
  dois é exatamente o que produziu as regressões, e o v1 não tinha como
  distingui-los. Às 10h18 ainda eram 196 de 528.
- **A conclusão do v1 sobreviveu à primeira contagem:** as lacunas (101)
  superavam o que o produto aciona (75). Na segunda a ordem se inverteu (121
  contra 114), e é cedo para comemorar: o que mudou foi o **conhecimento** sobre
  as linhas, não o produto.
- **22 e 16 não são a mesma conta, e por isso a diferença não mede progresso
  nenhum.** No v1 a assimetria saía de uma junção por texto de feature, com 34
  linhas que não pareavam — e entre elas havia assimetria real que o contador
  não via. No v2 os dois lados moram no mesmo registro e a conta sai dele, sem
  junção. **16 é o número que se pode defender hoje**; comparar com 22 é
  comparar dois métodos, não dois estados.

## 10. O que esta sprint NÃO entrega

A semente do CSV veio da escavação de 10/08 e ainda é `afirmado-no-doc` na
maior parte: **as 204 linhas nascem sem `teste_que_morde`**, o que a própria
tela declara no rodapé. `PARIDADE-PORTAO-01` é quem passa a cobrar isso.

> **Nota de 11/08/2026 — confirmado, e são 264.** No CSV entregue a coluna
> `teste_que_morde` estava vazia em **todas** as 264 linhas, e com ela outras
> sete: `mordida`, `mordida_provada_em`, `provado_em`, `provado_por`,
> `validade_dias`, `assimetria_declarada` e `estado_hoje`. Oito colunas 100%
> vazias não eram descuido — eram o contorno exato do que esta sprint não
> entregou.
>
> Às 10h18 do mesmo dia, com outra frente preenchendo: `teste_que_morde` e
> `mordida` já tinham 39 linhas cada, `assimetria_declarada` 26, e **cinco
> colunas continuavam 100% vazias** — `mordida_provada_em`, `provado_em`,
> `provado_por`, `validade_dias` e `estado_hoje`. Três delas (`provado_em`,
> `provado_por`, `validade_dias`) **não se preenchem sem ela**: dependem da
> resposta a *quem tem direito de escrever a linha de "provado"*.

A semente do CSV é
**auditoria, não extração**: decisão dela de 10/08, *"csv nasce mas é preciso
estudar pra ver se as infos de origem estão corretas"*. Os 93 KB de documentos
canônicos entram como `afirmado-no-doc`, nunca como `medido`.

A pesquisa de 10/08 já mostrou por que ela tinha razão: a canônica publica o
padrão P4 do LED de jogador **errado** (o código está certo), e a regra
`report[n] → report[n+2]`, publicada como "a que governa tudo", **só vale na
saída** — na entrada o deslocamento é `+1`.

## Nota datada de 11/08/2026 — o que esta sprint passou a dizer

A tela existe desde o commit `a2a9429` (11/08/2026, 01:51). O texto de 10/08
ficou inteiro onde estava; cada afirmação vencida ganhou nota ao lado, nesta
ordem:

| onde | o que dizia | o que vale hoje |
|---|---|---|
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:9-11` | *"não existe uma linha de `specs.html` ainda"* | existe; 653 KB no commit que o criou, gerado do CSV |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:44` e `:53` | isenção `ref-externa` em `bancada.py` e `scripts/gerar-mapa.py` | os dois existem; a isenção saiu e o portão passou a guardá-los |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:53` | *"um portão reprova se ele estiver mais velho que o CSV"* | nasceu sem chamador às 01h51; às 10h18 do mesmo dia o CI e o pre-commit passaram a chamá-lo |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:82` | o placar do rascunho: 31/42, 12/44, 9/50 medidas | v1; no v2, às 10h18, o Hefesto aciona 50 de 62, 8 de 30 e 12 de 29 |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:111-113` | três símbolos | quatro: o ◌ separou "ninguém respondeu" de "o aparelho recusa" |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:191` | *"(357 KB)"* | 669.050 bytes = 653 KB, e já eram no commit que escreveu a linha |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:228-231` | ● 69 / ◐ 75 / ○ 60 / ≠ 22, em 204 linhas | v1; o v2 está na seção 9.1, em 528 células |
| `2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md:276-278` | *"as 204 linhas nascem sem `teste_que_morde`"* | são 264; eram oito as colunas 100% vazias, e às 10h18 eram cinco |

**O que continua aberto nesta sprint, nominalmente:**

1. **A prova de tela dela** — o item `[ ]` da seção 8. É o único aceite que
   falta, e ele é dela por desenho.
2. **As linhas de combinação** — o CSV continua sem nenhuma, e a seção 5 do
   [índice](2026-08-10-INDICE-o-mapa-que-vira-portao.md) explica por que isso é
   um ponto morto exatamente onde ela mais usa. (O item que estava aqui, *"o
   portão que ainda não é portão"*, saiu às 10h18 de 11/08: o `--check` ganhou
   chamador no CI e no pre-commit.)
3. **As três decisões da seção 8 do índice** — a procedência da arte, a posição
   do LED de jogador do Pro e quem escreve a linha de "provado". As três viraram
   perguntas curtas em
   [MAPA-QUE-VIRA-PORTÃO-02](2026-08-11-MAPA-QUE-VIRA-PORTAO-02-o-que-entrou-e-o-que-continua-sendo-dela.md).
