# ÍNDICE — o mapa que vira portão

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"tivemos várias regressões de features antes consolidadas pq
  não tínhamos isso mapeado. tipo tínhamos algo para o cabo e na hora do vamos
  ver a versão de BT não funcionava. a ideia é que ao final de tudo eu e vc
  possamos mapear cada canal, cada feature de cada controle e assim possamos
  desenvolver com segurança e sem tentativa e erro."*
- **Grau:** a PESQUISA é medida (20 agentes, três frentes, contagens e mutação
  reproduzíveis). A EXECUÇÃO abaixo é plano, não entrega — nenhuma linha destas
  sprints virou código ainda.

> **Nota de 11/08/2026 — a segunda frase do Grau caducou; a primeira, não.**
> A pesquisa continua medida, e nada dela foi tocado. Mas *"nenhuma linha
> destas sprints virou código ainda"* deixou de valer às 01:51 de 11/08, no
> commit `a2a9429`: as sprints **1, 2 e 3** da tabela da seção 4 entraram — os
> três desenhos, as 264 linhas de `docs/data/mapa-controles.csv`, o `specs.html`
> gerado por `scripts/gerar-mapa.py` e a bancada em `bancada.py`. E a **4**
> entrou no mesmo dia, algumas horas depois, quando o censo virou portão de CI,
> e a **5** andou metade do caminho. A frase fica escrita como estava porque era
> verdade em 10/08. O estado de hoje está na
> coluna **Rótulo** da tabela da seção 4, e o que a leva de 11/08 fechou e
> deixou aberto está em
> [MAPA-QUE-VIRA-PORTÃO-02](2026-08-11-MAPA-QUE-VIRA-PORTAO-02-o-que-entrou-e-o-que-continua-sendo-dela.md).

---

## 1. A frase que reclassifica o pedido

Ela não pediu documentação. Pediu **rede contra regressão**.

Um mapa que só se olha não impede consolidar uma feature no cabo e descobrir no
"vamos ver" que o Bluetooth nunca funcionou. Por isso cada linha do CSV que
afirmar `funciona por BT = sim, medido` tem de ser afirmação **que um teste
consegue checar** — senão o mapa vira mais uma prosa convincente, que é a mesma
doença de [O instrumento mente mais que o produto].

## 2. O que a medição achou, e que justifica cada sprint

Três números fecham o diagnóstico, todos medidos em 10/08 contra a suíte de
**8589 testes coletados**:

| medida | valor |
|---|---:|
| Testes que MENCIONAM transporte | 718 (9,7%) |
| Testes que tocam o envelope de um transporte no nível de BYTE | **93 (1,1%)** |
| `@pytest.mark.parametrize` cruzando os DOIS transportes | **0**, de 233 |
| Fixtures parametrizadas por transporte | **0** |
| Capturas HID gravadas na suíte | 1, e é USB |

> **Nota de 11/08/2026 — uma linha desta tabela foi recontada e o número
> publicado estava errado.** Onde se lê *"`@pytest.mark.parametrize` cruzando os
> DOIS transportes: **0**, de 233"*, o medido é **1 de 233**: o decorador
> `@pytest.mark.parametrize("transporte", ["usb", "bt"])` já existia em
> `tests/unit/test_agora_e_depois_01.py:978` desde 08/08 (commit `10f013a`),
> antes da medição — e o denominador, 233, confere na árvore daquele dia. Na
> árvore de hoje são 241 decoradores e o mesmo cruzamento único. **O
> diagnóstico não muda de lado:** esse caso é de interface (escolha de mesa com
> `fake_gtk`) e não toca byte nenhum, que é justamente o que a frase do fim
> desta seção afirma. As outras linhas foram reconferidas e continuam de pé —
> zero fixture parametrizada por transporte, e `tests/fixtures/hid_capture_usb.bin`
> segue sendo a única captura HID da suíte, e é do cabo. O número fica escrito
> como estava, com esta nota ao lado: não se apaga medição, corrige-se com data.

E a prova por mutação, que é a que não deixa dúvida:

- Trocar **R por B** dentro de `_build_common` — vermelho por azul no lightbar —
  deixa a suíte **inteira verde**: 8584 passaram.
- Matar os gatilhos adaptativos **só no BT**, com envelope e CRC perfeitos,
  reprova **1 teste em 8589** (e é o genérico "o payload sai verbatim", que não
  sabe o que é gatilho). A mesma morte no cabo reprova 2.

O `hid_capture_bt.bin` que o **ADR-008 afirma existir nunca existiu**.

**O diagnóstico em uma frase:** cada feature é provada uma vez, no transporte que
estava na mesa de quem escreveu o teste — quase sempre o cabo — e o transporte
**nunca é dimensão do caso**, é rótulo dentro de um dict.

O envelope, esse, está travado: mexer no `_BT_STRUCT_BASE` reprova 6, deslocar o
payload reprova 5, CRC invertido reprova 6. **O buraco é o andar de cima, entre a
feature e os bytes.**

## 3. A cobertura que o mapa vai expor

> **Nota de 11/08/2026 — o grão mudou, os números desta seção são do v1.**
> O CSV foi migrado para `(chave, controle)`: o cabo e o rádio passaram a viver
> na MESMA linha, em colunas `cabo_*` / `radio_*`, e cada feature virou um bloco
> de três linhas adjacentes, uma por controle. As 204 linhas do v1 viraram 264
> (88 chaves x 3 controles), das quais 136 carregam a medição do v1 e 128 são
> linhas novas que dizem, com todas as letras, que aquele controle nunca foi
> respondido naquela chave. O v1 está guardado em
> `docs/data/mapa-controles-v1.csv` — a migração prova campo a campo que nada se
> perdeu (`scripts/migrar-mapa-v2.py --provar`, 4986 campos conferidos). O que
> motivou: *"cada feature de cada um deles deve ter o canal via bt ou cabo NA
> MESMA LINHA e todos os 3 controles devem ser possíveis de serem comparados"*.

204 linhas levantadas, e a assimetria é o produto:

| Controle | Features | Medidas | Incertas |
|---|---:|---:|---:|
| DualSense | 42 | 31 | 7 |
| Nintendo Pro | 44 | 12 | 2 |
| 8BitDo SN30 Pro | 50 | **9** | 10 |

No DualSense três em cada quatro linhas são medidas. No SN30, **menos de uma em
cinco**. O resto é papel — e papel foi o que produziu as regressões dela.

**A mesma conta no v2, ao lado — contada às 10h18 de 11/08/2026 sobre as 264
linhas de `docs/data/mapa-controles.csv`.** A tabela acima fica como está: ela é
do v1 e conta o que o v1 sabia contar. As colunas mudaram de sentido porque o
grão mudou, e por isso os números não se comparam linha a linha:

| Controle | Linhas | O aparelho TEM | Ao menos um lado medido | O Hefesto ACIONA |
|---|---:|---:|---:|---:|
| DualSense | 88 | 62 | 25 | 50 |
| Nintendo Pro | 88 | 30 | 17 | **8** |
| 8BitDo SN30 Pro | 88 | 29 | 12 | 12 |

**Esta contagem tem hora porque o CSV estava sendo preenchido enquanto ela era
feita**, por outra frente da mesma leva de 11/08. O número vivo é o que o
`specs.html` publica; quem garante que a tela e o CSV não divirjam é o portão
que entrou nesta leva. O retrato de fundo, esse, não mudou: **no Nintendo Pro o
produto aciona 8 das 30 features que o aparelho tem.** As 88 linhas de cada
controle são as 88 chaves canônicas — boa parte ainda diz, com todas as letras,
que ninguém respondeu nada ali.

## 4. A ordem de execução

Cada sprint só existe porque um defeito datado a justifica. A ordem não é de
importância: é de **dependência**.

| # | Sprint | Entrega | Depende de | Rótulo em 11/08/2026 |
|---|---|---|---|---|
| 1 | `MAPA-SVG-01` | Os três desenhos padronizados e nomeados | — (**feito em 10/08**) | **ENTREGUE** (`dad60ae`, 10/08) |
| 2 | `MAPA-CSV-01` | O `mapa-controles.csv` semeado por auditoria | 1 | **PARCIAL** — a semente entrou (`a2a9429`); as linhas de combinação da seção 5 não nasceram |
| 3 | `MAPA-TELA-01` | `specs.html` standalone + bancada Streamlit | 1, 2 | **ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA** |
| 4 | `PARIDADE-PORTAO-01` | O censo no CI: cobra o código contra o mapa | 2 | **ENTREGUE EM CÓDIGO** — quem valida é o CI, não ela |
| 5 | `PARIDADE-BYTE-01` | Transporte vira dimensão do caso de teste | 2, 4 | **PARCIAL** — a fixture existe e morde em seis famílias; o resto da suíte, não |
| 6 | `PARIDADE-FORMA-01` | A mordida estrutural (nomes udev, constantes) | 4 | **ABERTA** |
| 7 | `UNIDADE-COR-01` | Identidade por unidade + colorway na tela | 2, 3 | **ABERTA** |
| 8 | `BANCADA-01` | O que só o aparelho responde | 2, 4 | **ABERTA** |

**A coluna Rótulo nasceu em 11/08/2026.** Até então a tabela não tinha nenhuma,
e o único estado declarado era o *"feito em 10/08"* da linha 1, que fica onde
estava. Cada rótulo foi medido contra o disco de hoje, um por um:

- **1 — `MAPA-SVG-01`, ENTREGUE.** Os três arquivos existem e carregam **76
  grupos com `id`** (26 no DualSense, 27 no Pro, 23 no SN30), nenhum órfão,
  commit `dad60ae`. O que ainda falta dos desenhos não é código: é a procedência
  da arte e a posição do LED de jogador do Pro, e as duas estão na seção 8.
- **2 — `MAPA-CSV-01`, PARCIAL.** `docs/data/mapa-controles.csv` tem 264 linhas
  (88 chaves x 3 controles) e a semente por auditoria entrou. Mas as **linhas de
  combinação** que a seção 5 declarou obrigatórias — o controle no cabo matando
  a saída do que está no rádio — **não existem: zero linhas**, e continuavam
  zero às 10h18 de 11/08, com o preenchimento já em curso. Cinco colunas seguem
  100% vazias, e três delas — `provado_em`, `provado_por` e `validade_dias` —
  dependem de uma decisão dela (seção 8, terceiro item).
- **3 — `MAPA-TELA-01`, ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA.**
  `specs.html` (653 KB), `scripts/gerar-mapa.py` e `bancada.py` estão no disco e
  commitados. O último item da sprint continua aberto **por desenho, não por
  esquecimento**: é a foto antes e depois, e a palavra é dela.
- **4 — `PARIDADE-PORTAO-01`, ENTREGUE EM CÓDIGO.** Esta linha mudou **duas
  vezes no mesmo dia**, e as duas ficam registradas: às 03h de 11/08 ela era
  `ABERTA`, porque `scripts/check_paridade_transporte.py` não existia; às 10h18
  o arquivo estava no disco e o CI o chamava, junto com o `--check` do gerador,
  que também passou a rodar no `.pre-commit-config.yaml`. **Sem sufixo de
  aceite:** quem valida portão é o CI, não ela — é a regra escrita na
  [RÓTULOS-DE-SPRINT-01](2026-08-09-ROTULOS-DE-SPRINT-01-entregue-no-codigo-nao-e-validado-por-ela.md).
  Ressalva honesta: quando isto foi escrito o trabalho dessa frente ainda estava
  **na árvore, sem commit**.
- **5 — `PARIDADE-BYTE-01`, PARCIAL.** Esta linha também mudou dentro do dia.
  Às 03h: 241 decoradores `parametrize` na suíte, **um só** com o transporte
  como eixo, e de interface; **zero** fixtures parametrizadas por transporte.
  Às 10h18 a fixture existe (`tests/conftest.py`, `params=["usb", "bt"]`), e
  **40 casos** em seis arquivos a pedem — lightbar, rumble, gatilhos, áudio, LED
  de jogador e o envelope —, cada um rodando duas vezes, com ids `[usb]` e
  `[bt]`, e com mordida provada por mutação fora da árvore. **PARCIAL, e não
  entregue:** as seis famílias são seis das 88 chaves do mapa; no resto da suíte
  o transporte continua sendo rótulo dentro de um dict. Continua verdade também
  que **não há captura HID de Bluetooth** na árvore.
- **6 — `PARIDADE-FORMA-01`, ABERTA.** Nada da leva de 10 e 11/08 tocou a forma:
  os testes de regra udev que existem são os de antes, e nenhum deles morde nos
  dois sentidos a partir do mapa.
- **7 — `UNIDADE-COR-01`, ABERTA.** Os três SVG já aceitam `data-colorway`, mas
  `scripts/gerar-mapa.py` **não menciona colorway uma única vez**: a tela de hoje
  não pinta por unidade.
- **8 — `BANCADA-01`, ABERTA.** A superfície de medição veio junto com a 3, e
  isso não é a sprint: `docs/data/ensaios.csv` tem 14 ensaios, todos de 03/08 e
  10/08 — anteriores a esta leva — e as colunas `provado_*` do mapa continuam
  vazias em todas as 264 linhas.

**O que falta ela validar, em uma linha:** abrir o `specs.html` com dois cliques
e dizer se aquela é a tela que ela pediu — e, no CSV, se pode confiar na origem
das linhas que a auditoria semeou.

A 4 entrega um validador novo, irmão dos nove portões que a casa já tem:
`check_paridade_transporte.py`. <!-- criado em 11/08/2026 por outra frente da mesma leva; a isenção ref-externa saiu porque o arquivo existe -->

A 1 está feita. A 3 é a que ela pediu para ver primeiro, e está detalhada em
[MAPA-TELA-01](2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md).

> **Nota de 11/08/2026:** a 1 continua feita, e agora a 2 e a 3 também estão no
> disco — a 3 com a prova de tela dela ainda em aberto. O que entrou, o que
> outras frentes de hoje estão fechando e as três perguntas que só ela responde
> estão em
> [MAPA-QUE-VIRA-PORTÃO-02](2026-08-11-MAPA-QUE-VIRA-PORTAO-02-o-que-entrou-e-o-que-continua-sendo-dela.md).

## 5. A correção de desenho que a pesquisa impôs

Um controle **no cabo** matava a saída do controle **no BT**: o laço de
`sendReport` saturava o controlador USB, e o adaptador de rádio vive no mesmo
controlador. A feature funciona no cabo, funciona no rádio, e quebra quando os
dois estão na mesa.

**O CSV como (controle × feature × transporte) é cego a isso por construção** —
não existe linha para uma combinação. Por isso `MAPA-CSV-01` nasce com uma seção
de **linhas de combinação**, ou o mapa nasce com um ponto morto exatamente onde
ela mais usa.

> **Nota de 11/08/2026 — o mapa nasceu com o ponto morto.** O CSV entregue em
> `a2a9429` tem 264 linhas e **nenhuma** delas é de combinação: procurados os
> termos de coexistência no arquivo inteiro, o resultado é zero. A migração para
> `(chave, controle)` pôs cabo e rádio na mesma linha, o que resolve a
> comparação **entre transportes** — e não resolve o caso dos dois **ao mesmo
> tempo**, que é o que esta seção descreve. O aviso desta seção continua válido
> palavra por palavra; ele só deixou de ser um risco e virou um estado.

## 6. As quatro camadas do portão, e o que cada uma NÃO pega

| Camada | Roda onde | Pega |
|---|---|---|
| 0 — o censo | CI, sem hardware | A **ausência**: célula sem teste que morda, teste que o pytest não coleta, prova vencida |
| 1 — a mordida de byte | CI, sem hardware | Offset, tag, CRC, o byte da feature no envelope certo |
| 2 — a mordida estrutural | CI, sem hardware | Nome, escopo e forma: regra udev que casa de menos **ou demais**, constante de tempo sem transporte declarado |
| 3 — a bancada | Máquina dela, com o controle | Taxa real, o aparelho obedecendo, o que só o olho resolve |

**Dito na cara: o latch da lightbar por BT nenhuma delas pega.** O report é
bem-formado, o CRC bate, o offset está certo — o que separa travar de não travar
é o **tempo desde a conexão** (~3,4 s), dimensão que não existe em teste
unitário. O que a rede faz é outra coisa: prazo de validade curto naquela célula,
para o CI reprovar quando a prova vencer.

## 7. O caso que teria custado 25 dias a menos

A regra udev 76 do touchpad **nunca pegou o touchpad em Bluetooth**: casava o
nome exato do USB, `Sony Interactive Entertainment...`, e o BlueZ publica sem o
prefixo do fabricante. Vinte e cinco dias entre escrever e descobrir. O curinga
que curou isso caducou pelo lado oposto em 09/08 e **ela perdeu o cursor** que
tinha antes do Hefesto.

A camada 2 morde nos **dois sentidos**: casar de menos e casar demais reprovam
igual, porque a casa já pagou pelos dois. É a mordida mais barata da rede
inteira, e está em `PARIDADE-FORMA-01`.

## 8. O que continua sendo dela

- **A procedência da arte.** Decisão de 10/08: fica como está por ora, e a
  alteração na origem se documenta quando formos mexer. O `LICENSE` é **MIT** —
  não GPL-3 — e a atribuição, quando existir, respeita isso.
- **A posição dos LED de jogador do Nintendo Pro.** Que existem está registrado;
  onde ficam não está escrito em lugar nenhum do repositório. O grupo já existe
  no SVG com `data-posicao="nao-localizada"`. Uma foto dela fecha.
- **Quem escreve a linha de "provado".** Vale o produto ter lido uma vez? Vale
  ela ter VISTO funcionar? Só vale teste? A resposta define se "nunca tentei"
  aparece igual a "tentei e falhou" — e não deveria.

> **Nota de 11/08/2026 — os três continuam dela, e agora custam preço medido.**
> Nenhum dos três foi respondido, e o mapa entregue mostra o tamanho de cada um:
> a arte viaja inline dentro do `specs.html`, que vai no release; duas peças ainda nascem com
> `data-posicao="nao-localizada"` nos desenhos (o LED de jogador do Pro e a
> lightbar do DualSense); e `provado_em`, `provado_por` e `validade_dias` estão
> vazias nas 264 linhas, porque ninguém tem autorização para escrevê-las. As
> três viraram perguntas curtas, prontas para ela responder, na seção 4 de
> [MAPA-QUE-VIRA-PORTÃO-02](2026-08-11-MAPA-QUE-VIRA-PORTAO-02-o-que-entrou-e-o-que-continua-sendo-dela.md).

## Nota datada de 11/08/2026 — o que este índice passou a dizer

Este documento afirmava, no cabeçalho, que nenhuma linha destas sprints tinha
virado código. Virou, no commit `a2a9429` de 11/08/2026, 01:51 — e mais ainda
durante o próprio dia. Nada foi apagado: cada afirmação de 10/08 ficou onde
estava e ganhou a nota ao lado.

| onde | o que caducou | o que vale hoje |
|---|---|---|
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md:9-11` | *"nenhuma linha destas sprints virou código ainda"* | as sprints 1, 2, 3 e 4 entraram, e a 5 pela metade (`dad60ae`, `a2a9429` e a leva de 11/08) |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md:47` | *"`parametrize` cruzando os DOIS transportes: 0, de 233"* | é 1 de 233, e o cruzamento é de interface, não de byte |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md:97` | as 204 linhas e a tabela por controle | 264 linhas; a nota da seção 3 já registrava a migração |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md:134-141` | tabela sem nenhum rótulo | oito rótulos medidos contra o disco |
| `2026-08-10-INDICE-o-mapa-que-vira-portao.md:217-218` | as linhas de combinação como risco futuro | o mapa nasceu sem elas: zero linhas |

**O que continua aberto, nominalmente:**

1. `PARIDADE-BYTE-01` — o resto da suíte, além das seis famílias que já mordem.
2. `PARIDADE-FORMA-01` — a mordida estrutural, nos dois sentidos.
3. `UNIDADE-COR-01` — a cor da unidade na tela; hoje o gerador a ignora.
4. `BANCADA-01` — a campanha de medição; as colunas `provado_*` estão vazias.
5. `MAPA-CSV-01` — as linhas de combinação da seção 5.
6. `MAPA-TELA-01` — a prova de tela dela, que é o item aberto por desenho.
7. Os três itens da seção 8, que são decisão dela e de mais ninguém.

A `PARIDADE-PORTAO-01` saiu desta lista às 10h18 de 11/08, quando o validador
apareceu no disco e o CI passou a chamá-lo. **O que ela entregou é o censo, não
a prova:** o censo cobra a ausência de teste que morda, e a mordida de byte
continua sendo da `PARIDADE-BYTE-01`.
