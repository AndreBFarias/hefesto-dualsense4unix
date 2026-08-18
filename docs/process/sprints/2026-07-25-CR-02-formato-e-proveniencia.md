# CR-02 — O formato do efeito próprio carrega a própria proveniência

**Status:** ENTREGUE em 2026-07-31 — o formato existe, recusa, e a recusa está
provada por arrancamento
**Depende de:** CR-01
**Bloqueia:** CR-03, CR-04
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Fazer com que seja **impossível** um valor de curva entrar no projeto sem dizer
de onde veio. Não por disciplina — por estrutura de dados.

## O problema que isto previne

Documento de proveniência mantido à mão, separado dos dados, é documento que
desatualiza. Seis meses depois ninguém lembra se aquele `Pesado` foi medido ou
chutado, e a defesa evapora junto com a memória.

A regra R3 do processo diz "o dado e a origem nunca se separam". Esta sprint faz
disso uma propriedade do formato, não uma promessa.

## Entregas

- [x] **Esquema do efeito próprio** — `CurvaPropria`, com os seis campos, todos
      obrigatórios e **sem default nenhum** (default transformaria "não
      informado" em "informado como vazio", que é o buraco que a R3 fecha).
      Mora em `src/hefesto_dualsense4unix/profiles/curva_propria.py`, e **não**
      em `profiles/schema.py` — a razão está na decisão de projeto, abaixo.
- [x] **Validação que recusa** efeito sem proveniência completa. É erro, não
      aviso: `medido_por`, `controle` ou `nota` vazios (ou só com espaço, ou
      `None`, ou ausentes) levantam `ValidationError` com a regra escrita na
      mensagem. A `nota` tem piso de 20 caracteres, porque `"ok"` preenche o
      campo sem cumprir a R3.
- [x] **Guarda de nomes** — recusa os doze nomes do DSX **sem diferenciar
      caixa** (`Hard`, `hard`, `  HARD  `), com a mensagem explicando a R2 em
      vez de só negar. A lista **não é transcrita**: é lida do
      `DSX_CANNED_TRIGGER_MODES` de `daemon/udp_server.py`, porque duas listas
      divergem e uma não. Import tardio para não puxar o daemon.
- [x] **A data é datada de verdade** — entrega que a sprint não pedia e a R3
      exige: `medido_em` tem de ser ISO `AAAA-MM-DD` e não pode ser anterior a
      **2026-07-25**, a data de vigência do `CLEAN-ROOM.md`. Medição que se
      declara anterior ao processo não carrega o registro que o processo exige.
      O limite é uma data **fixa**, nunca o relógio: portão que lê o relógio
      reprova sozinho em máquina com data diferente, e esta casa já tem essa
      cicatriz.
- [x] **`docs/protocol/curvas-proprias.md`** — a função
      `gerar_tabela_markdown(catalogo)` produz a tabela a partir do dado.
      Catálogo vazio devolve exatamente a linha que o documento tem hoje, para
      que ele siga legível antes da CR-04. **O documento continua sem nenhum
      valor**, e há teste cobrando isso: se alguém colar uma curva ali sem
      passar pela medição, o portão avisa.
- [x] **Teste** que prova a recusa —
      `tests/unit/test_cr02_curva_propria_proveniencia.py`, 50 casos.

## A mordida, provada arrancando a cura

Teste que passa com a cura arrancada não testa nada. Os cinco validadores foram
**removidos do arquivo de verdade**, um a um, com a suíte rodando entre cada
remoção e a restauração conferida por `sha256`. Transcrição em
`docs/process/estudos/assets/2026-07-31-onda2/mordida-cr02.txt`:

| Validador arrancado | Testes que reprovaram |
|---|---|
| `_proveniencia_nao_vazia` | 4 |
| `_nome_proprio_e_nao_do_dsx` | 7 |
| `_data_valida_e_sob_o_processo` | 2 |
| `_curva_com_a_largura_do_hardware` | 8 |
| `_nota_diz_alguma_coisa` | 3 |

Com tudo no lugar: **50 passaram**. `sha256` do arquivo antes e depois do ciclo
inteiro: `76dc392250389087c2fc49d12c9d8d153ea9ddea885e5f77d81e86065fcfd938`,
idêntico.

## Decisão de projeto a tomar aqui — TOMADA

A pergunta era: efeitos próprios dentro de cada perfil, ou num catálogo
compartilhado que os perfis referenciam?

**Catálogo compartilhado** (`CatalogoCurvasProprias`), pelo motivo que a própria
sprint dá: dois perfis com o mesmo nome e proveniências diferentes é exatamente
a divergência que este processo existe para impedir. O catálogo recusa nome
repetido, ignorando caixa.

O custo que a sprint temia — migração de esquema — **é zero hoje**, e essa é a
razão de decidir agora e não depois: não existe nenhuma curva própria no
repositório, então não há nada para migrar. Em seis meses existiria.

Consequência prática, e é por isso que o arquivo não é o `schema.py`: o catálogo
é um documento à parte, não um campo do perfil v1. `Profile` fica **intocado** —
nenhuma mudança de formato em disco, de IPC, nem de compatibilidade com binário
antigo (`extra="forbid"` recusaria um campo novo no downgrade). A sprint dizia
`profiles/schema.py`; a medição mostrou que ali sairia mais caro sem comprar
nada.

## Critério de conclusão

Atendido: gravar um efeito sem proveniência, ou com nome do DSX, falha com
mensagem clara — e a tabela de `curvas-proprias.md` sai da função, não da mão de
ninguém.

## O que fica para a CR-03

O formato existe, mas ainda **não tem quem o preencha**: quem grava e lê o
catálogo em disco é a bancada de medição (CR-03, terceira entrega — "o salvar
com nome e nota"). Enquanto ela não existe, o formato é um portão sem porta, e
está certo assim: nenhum valor pode entrar antes da mão dela no gatilho.
