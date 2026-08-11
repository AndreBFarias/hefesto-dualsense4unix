# MAPA-TELA-01 — o layout do mapa de canais

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"a ideia aqui é termos um mapa rápido que nos permita ver por
  qual canal via bluetooth acionamos o lightbar e por qual canal via cabo
  acionamos o lightbar. Mas isso pra todas as features de cada controle de tal
  forma vamos conseguir finalmente enxergar o todo, e pararmos com as tentativas
  e erros desesperadas."*
- **Grau:** os DESENHOS estão medidos e entregues (10/08). O LAYOUT abaixo é
  proposta — não existe uma linha de `specs.html` ainda, e a palavra final sobre
  a tela é dela ([PROVA-DE-TELA-01]).

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
`bancada.py`, na raiz. <!-- ref-externa: arquivo que ESTA SPRINT propõe criar; ainda não existe -->

| | `specs.html` | a bancada (Streamlit) |
|---|---|---|
| Para que serve | Consultar, versionar, abrir em qualquer lugar | Medir com o controle na mão |
| Como abre | Duplo clique, sem servidor | `streamlit run`, precisa do venv |
| Quem escreve no CSV | ninguém — é só leitura | ela, durante a medição |
| Vai para o release | **sim** | não |

O `specs.html` é gerado do CSV por `scripts/gerar-mapa.py`, e um portão reprova <!-- ref-externa: arquivo que ESTA SPRINT propõe criar; ainda não existe -->
se ele estiver mais velho que o CSV. Assim a tela nunca mente por atraso — a
mesma disciplina de `retratar_abas.py`, que já impede a documentação de
envelhecer.

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

- [x] `scripts/gerar-mapa.py` — CSV → `specs.html`, autocontido, sem CDN <!-- ref-externa: arquivo que ESTA SPRINT propõe criar; ainda não existe -->
- [x] `specs.html` na raiz, abrindo por duplo clique (357 KB, zero requisição de rede)
- [x] `bancada.py` — a superfície de medição, lendo e ESCREVENDO no mesmo CSV <!-- ref-externa: arquivo que ESTA SPRINT propõe criar; ainda não existe -->
- [x] Portão `gerar-mapa.py --check` — provado nos três casos: fonte mais nova
      reprova (1), depois de regerar passa (0), arquivo ausente reprova (1)
- [ ] Foto antes e depois, e **a palavra final é dela** ([PROVA-DE-TELA-01])

## 9. O que a tela mostrou assim que existiu

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

## 10. O que esta sprint NÃO entrega

A semente do CSV veio da escavação de 10/08 e ainda é `afirmado-no-doc` na
maior parte: **as 204 linhas nascem sem `teste_que_morde`**, o que a própria
tela declara no rodapé. `PARIDADE-PORTAO-01` é quem passa a cobrar isso.

A semente do CSV é
**auditoria, não extração**: decisão dela de 10/08, *"csv nasce mas é preciso
estudar pra ver se as infos de origem estão corretas"*. Os 93 KB de documentos
canônicos entram como `afirmado-no-doc`, nunca como `medido`.

A pesquisa de 10/08 já mostrou por que ela tinha razão: a canônica publica o
padrão P4 do LED de jogador **errado** (o código está certo), e a regra
`report[n] → report[n+2]`, publicada como "a que governa tudo", **só vale na
saída** — na entrada o deslocamento é `+1`.
