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

## 4. A ordem de execução

Cada sprint só existe porque um defeito datado a justifica. A ordem não é de
importância: é de **dependência**.

| # | Sprint | Entrega | Depende de |
|---|---|---|---|
| 1 | `MAPA-SVG-01` | Os três desenhos padronizados e nomeados | — (**feito em 10/08**) |
| 2 | `MAPA-CSV-01` | O `mapa-controles.csv` semeado por auditoria | 1 |
| 3 | `MAPA-TELA-01` | `specs.html` standalone + bancada Streamlit | 1, 2 |
| 4 | `PARIDADE-PORTAO-01` | O censo no CI: cobra o código contra o mapa | 2 |
| 5 | `PARIDADE-BYTE-01` | Transporte vira dimensão do caso de teste | 2, 4 |
| 6 | `PARIDADE-FORMA-01` | A mordida estrutural (nomes udev, constantes) | 4 |
| 7 | `UNIDADE-COR-01` | Identidade por unidade + colorway na tela | 2, 3 |
| 8 | `BANCADA-01` | O que só o aparelho responde | 2, 4 |

A 4 entrega um validador novo, irmão dos nove portões que a casa já tem:
`check_paridade_transporte.py`. <!-- ref-externa: arquivo que ESTA SPRINT propõe criar; ainda não existe -->

A 1 está feita. A 3 é a que ela pediu para ver primeiro, e está detalhada em
[MAPA-TELA-01](2026-08-10-MAPA-TELA-01-o-layout-do-mapa-de-canais.md).

## 5. A correção de desenho que a pesquisa impôs

Um controle **no cabo** matava a saída do controle **no BT**: o laço de
`sendReport` saturava o controlador USB, e o adaptador de rádio vive no mesmo
controlador. A feature funciona no cabo, funciona no rádio, e quebra quando os
dois estão na mesa.

**O CSV como (controle × feature × transporte) é cego a isso por construção** —
não existe linha para uma combinação. Por isso `MAPA-CSV-01` nasce com uma seção
de **linhas de combinação**, ou o mapa nasce com um ponto morto exatamente onde
ela mais usa.

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
