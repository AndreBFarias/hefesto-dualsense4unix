# GATILHO-PALAVRA-01 — os dezenove modos em português

- **Status:** ABERTA — esta sprint entrega a LISTA para ela escolher. Nenhum
  rótulo foi renomeado em código nesta rodada.
- **Prioridade:** MÉDIA — é texto de tela, reversível linha a linha, e não toca
  em nada que o controle sinta. O que a torna barata é justamente o que está
  medido abaixo: o nome que ela vê e o nome que o disco guarda são campos
  diferentes.
- **Aberta em:** 29/07/2026, a pedido dela
- **Sucede:** [PALAVRA-01](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md),
  que tirou o jargão de tela mas parou nos rótulos dos gatilhos — a lista de
  jargão banido dela é `start+1`, `raw HID`, `Mode HID`, `Force `, `Pos `
  (`tests/unit/test_palavra_a_janela_fala_a_lingua.py:239`), e "Feedback"
  nunca entrou nessa lista
- **Relacionada:** [VAO-01](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md),
  que definiu a grade de três colunas onde estes nomes vivem, e
  [INDICE-o-que-ficou-pelo-caminho](2026-07-27-INDICE-o-que-ficou-pelo-caminho.md)
- **Cuidado de ordem, com a
  [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md):** a
  entrega E8 daquela sprint propõe fazer `_WRAP_COLUNAS`
  (`app/widgets/segmented_selector.py:33`) deixar de ser 3 fixo e depender da
  largura recebida — a MESMA grade que dá o limite de 22 caracteres medido aqui.
  As duas se encaixam porque a E8 mantém **3 colunas como piso**, e é no piso
  (1040px, três colunas) que este documento mediu o corte. Se algum dia o piso
  passar a ser 4 colunas, o limite de 22 caracteres cai junto e esta lista
  precisa ser remedida — não deduzida
- **Referência técnica:** `docs/protocol/trigger-modes.md` (os dois níveis:
  modo HID e preset de alto nível)
- **Rodada:** é um dos seis documentos de 29/07; a ordem de leitura está no
  [índice da documentação da v0.3.0](../estudos/2026-07-29-INDICE-a-documentacao-da-v030.md)

## A frase dela, literal

> *"preciso que renomeie os nomes dos tipos de gatilhos que temos pra sinonimos
> pode fazer uma lista pra gente?"*

Ela pediu a **lista**, não a renomeação. Então a lista é a entrega, e a escolha
é dela: cada um dos dezenove tem três opções e uma recomendação marcada, para
ela só precisar discordar do que não gostar.

## O contrato que NÃO pode mudar

Cada modo tem **dois** nomes no código, e só um deles é texto de tela:

| Campo | Onde nasce | Quem lê |
|---|---|---|
| `name` | `app/actions/trigger_specs.py:27` | disco, IPC e protocolo DSX |
| `label` | `app/actions/trigger_specs.py:28` | os olhos dela, e mais nada |

O `name` é **chave serializada**, e está serializado em quatro lugares medidos:

1. **Perfil no disco dela.** O campo é `triggers.left.mode` / `triggers.right.mode`
   em `profiles/schema.py:146`, e o validador rejeita qualquer valor fora do
   registro `PRESET_FACTORIES` (`profiles/schema.py:161-169`). Os perfis dela
   hoje guardam, com essa grafia exata: `Vibration` e `PulseA` em
   `~/.config/hefesto-dualsense4unix/profiles/esportes.json:25,33`; `Resistance`
   e `MultiPositionVibration` em `corrida.json:26,33`; `Rigid` em
   `acao.json:23`; `SemiAutoGun` em `pragmata.json:10`.
2. **O registro canônico**, `core/trigger_effects.py:361-381` — dezenove chaves,
   com teste que trava a contagem em `tests/unit/test_trigger_effects.py:217`.
3. **O IPC.** O comando `trigger.set` recebe `mode` como string e a repassa
   direto para `build_from_name` (`daemon/ipc_handlers.py:483-491`); o mesmo
   vale para o applier de rascunho (`daemon/ipc_draft_applier.py:167`).
4. **O protocolo DSX.** `resolve_dsx_trigger_mode` traduz o ordinal do mod para
   o nome do preset do Hefesto e devolve a string literal — `return "Custom", ...`
   em `daemon/udp_server.py:230`, chamado de `udp_server.py:513`.

**Trocar um `name` quebra os perfis que ela já salvou** — o `_validate_mode`
levantaria `ValueError` no carregamento, e o perfil pararia de abrir. Esta
sprint não encosta em `name`. Só o `label` (e a `description` logo abaixo dele)
mudam de palavra.

## O que foi medido, antes de propor

### Os dezenove de hoje, conferidos no arquivo

Lido em `app/actions/trigger_specs.py:61-207`, na ordem em que aparecem na tela:

| # | `name` (contrato) | `label` hoje | linha |
|---|---|---|---|
| 1 | `Off` | Desligado | 63 |
| 2 | `Rigid` | Rígido (Rigid) | 67 |
| 3 | `SimpleRigid` | Rígido simples | 72 |
| 4 | `Pulse` | Pulso | 77 |
| 5 | `PulseA` | Pulso (curva A) | 81 |
| 6 | `PulseB` | Pulso (curva B) | 86 |
| 7 | `Resistance` | Resistência | 91 |
| 8 | `Bow` | Arco (Bow) | 96 |
| 9 | `Galloping` | Galope (Galloping) | 106 |
| 10 | `SemiAutoGun` | Arma semi-automática | 117 |
| 11 | `AutoGun` | Arma automática | 126 |
| 12 | `Machine` | Metralhadora (Machine) | 135 |
| 13 | `Feedback` | Feedback | 147 |
| 14 | `Weapon` | Arma (Weapon) | 152 |
| 15 | `Vibration` | Vibração | 157 |
| 16 | `SlopeFeedback` | Feedback em rampa | 162 |
| 17 | `MultiPositionFeedback` | Feedback por posição | 172 |
| 18 | `MultiPositionVibration` | Vibração por posição | 182 |
| 19 | `Custom` | Personalizado (avançado) | 195 |

A tabela do pedido bate com o arquivo, item por item.

### A largura do botão: o limite prático é 22 caracteres

Os dezenove viram botões de um `SegmentedSelector` com `wrap=True`
(`app/actions/triggers_actions.py:108-119`), que monta uma **grade de três
colunas fixas** (`app/widgets/segmented_selector.py:33`), com `max_width_chars`
de 16 no rótulo (`segmented_selector.py:36,227`) e fonte de 12px
(`gui/theme.css:913`).

Medido de verdade, com a grade montada e alocada numa `Gtk.OffscreenWindow` e o
`theme.css` carregado — widget sem alocação devolve 1x1 e qualquer conta sobre
ele seria inventada:

| Largura da janela | Largura de um botão | Espaço de texto | Cabe em uma linha |
|---|---|---|---|
| 1040px (o piso: `gui/main.glade:321`) | 157px | 139px | até **22 caracteres** |
| 1180px (a janela abre assim: `gui/main.glade:81`) | 180px | 162px | até ~25 caracteres |
| 1920px (maximizada) | 303px | 285px | folga |

O piso é que manda, porque é a largura em que a janela ainda tem de funcionar. O
corte foi medido caractere a caractere: `Metralhadora xxxxxxxxx` (22) fica numa
linha, `Metralhadora xxxxxxxxxx` (23) quebra.

**Passar de 22 custa altura, não só estética.** Quando um rótulo quebra, a linha
inteira da grade sai de 32px para 42px, e a altura mínima da grade sobe de
**306px para 357px**. Esse número não é local: o `GtkNotebook` adota o maior
mínimo entre as páginas, e foi exatamente esse mecanismo que já produziu a barra
de rolagem que a VAO-01 curou (o motivo está escrito em
`segmented_selector.py:168-180`).

Hoje **um** rótulo já estoura no piso: `Personalizado (avançado)`, com 24
caracteres. A lista recomendada abaixo tem 22 no maior deles e **não quebra
nenhum** — ou seja, a troca de nomes sai de graça em geometria, e ainda corrige
o único que estourava.

### Cinco nomes que obrigam a ler até o fim

Este é o defeito que ela sentiu sem nomear. Na grade de hoje, a coluna do meio
mostra em sequência:

```
Feedback            Feedback em rampa    Feedback por posição
Vibração            Vibração por posição
```

Cinco dos dezenove começam por uma de duas palavras. Numa grade de três colunas,
o olho varre a PRIMEIRA palavra de cada botão; com estes cinco, ele é obrigado a
ler a linha inteira, cinco vezes, para descobrir qual é qual. E "Feedback" é a
pior das duas: é a única palavra em inglês da grade que não é nome de modo em
guia de jogo nenhum — é nome de função interna que vazou para a tela.

### O achado que explica por que "Feedback" não diz nada

Lendo as fábricas: `feedback(position, strength)` emite `RIGID_B`
(`core/trigger_effects.py:189-193`) — **o mesmo modo HID** que
`rigid(position, force)` (`trigger_effects.py:73-78`) e que
`simple_rigid(strength)` (`trigger_effects.py:81-86`). A diferença entre os três
é só onde a barreira começa e em que escala a força é dada (0 a 8 via `_amp`,
ou 0 a 255 via `_byte`).

Isto é, "Feedback" **é** um rígido — com escala grossa e posição escolhida. O
rótulo de hoje esconde isso; a lista abaixo assume: os três viram nomes que
falam de barreira, firmeza e ponto duro, e a `description` de cada um diz a
diferença.

## Os critérios, na ordem em que decidiram

1. **O que a mão sente, não o que o código faz.** "Feedback" descreve a função
   `feedback()`; "Ponto duro" descreve o que o dedo encontra.
2. **Termo técnico entre parênteses só onde ajuda a achar o modo num guia em
   inglês.** Ficam `(Rigid)`, `(Bow)`, `(Galloping)`, `(Machine)` e `(Weapon)`,
   que é o conjunto que o teste de hoje já protege
   (`tests/unit/test_palavra_a_janela_fala_a_lingua.py:247-249`). Não ganham
   parênteses `Feedback`, `Custom`, `Vibration`, `Resistance` nem os dois
   `MultiPosition*`: ninguém procura por essas palavras num guia.
3. **Primeira palavra distinta.** É o critério que resolve os cinco nomes
   irmãos. Na lista recomendada, as dezenove primeiras palavras são: Sem,
   Barreira, Firmeza, Tranco, Tranco, Tranco, Resistência, Arco, Galope, Tiro,
   Rajada, Metralhadora, Ponto, Disparo, Vibração, Rampa, Curva, Tremor,
   Montar. A única repetição é "Tranco", nos três modos da família `Pulse` — e
   ela é deliberada (ver o item 4 da lista).
4. **Caber em 22 caracteres**, pelo motivo medido acima.

## A lista: três sinônimos para cada um dos dezenove

Legenda: **R** marca a recomendação. A contagem entre parênteses é o número de
caracteres, contra o limite de 22 do piso.

### 1. `Off` — hoje: "Desligado"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Sem resistência (15) | Diz o que a mão sente: o gatilho fica solto do começo ao fim. Não se confunde com o "Desligado" do daemon, que aparece em outras cinco telas |
| Solto (5) | Se ela quiser o nome mais curto possível da grade; perde a explicação |
| Desligado (9) | Mantém a palavra de hoje; o problema é que "Desligado" já significa "o Hefesto está desligado" em `app/actions/emulation_actions.py` e na aba Status |

### 2. `Rigid` — hoje: "Rígido (Rigid)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Barreira fixa (Rigid) (21) | "Rígido" é adjetivo sem sujeito; "barreira" é o objeto que o dedo encontra, e "fixa" diz que ela não anda de lugar |
| Parede num ponto (Rigid) (24) | Mais concreto ainda, mas estoura o limite de 22 e quebra em duas linhas no piso |
| Trava firme (Rigid) (19) | Se ela achar "barreira" comprido demais; "trava" sugere fim de curso, que não é bem o caso |

### 3. `SimpleRigid` — hoje: "Rígido simples"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Firmeza única (13) | O modo é o rígido com posição zero e uma só escala de 0 a 8: firmeza igual do começo ao fim, um único número para mexer |
| Barreira simples (16) | Deixa claro que é irmão do de cima; custa a primeira palavra repetida, e o olho volta a ter de ler a linha inteira |
| Peso do começo ao fim (21) | O mais literal do que se sente; longo, e "peso" não é usado em nenhum outro rótulo da janela |

### 4. `Pulse` — hoje: "Pulso"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Tranco único (12) | "Pulso" em português é batimento cardíaco antes de ser solavanco; "tranco" é o que o dedo leva, e "único" separa dos dois de baixo |
| Batida única (12) | Se ela achar "tranco" regional demais |
| Solavanco (9) | Curto e expressivo, mas não deixa claro que é um só |

### 5. `PulseA` — hoje: "Pulso (curva A)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Tranco no trecho (A) (20) | Diz as duas coisas que importam: é o mesmo tranco do item 4, e ele acontece entre duas posições. A letra vai para o fim porque é o que distingue do item 6 |
| Vaivém no trecho (A) (20) | Se ela sentir vaivém e não tranco ao testar; o nome fica mais fiel à sensação, menos fiel ao parentesco |
| Pulso A entre dois pontos (25) | Mantém a palavra de hoje; estoura o limite e quebra em duas linhas no piso |

### 6. `PulseB` — hoje: "Pulso (curva B)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Tranco no trecho (B) (20) | Gêmeo do item 5, de propósito: os dois são o mesmo efeito com curva diferente, e dar nomes diferentes a eles seria mentira. A letra final é o único discriminador honesto |
| Vaivém no trecho (B) (20) | Só faz sentido se o item 5 também virar "Vaivém": os dois andam juntos |
| Pulso B entre dois pontos (25) | Mesmo problema do 5: quebra a linha no piso |

### 7. `Resistance` — hoje: "Resistência"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Resistência constante (21) | A palavra de hoje está certa, só está incompleta: o que a distingue dos rígidos é ser contínua a partir de um ponto, e não uma parede |
| Peso constante (14) | Mais curto e mais físico; "peso" é palavra nova na janela |
| Aperto contínuo (15) | Se ela sentir aperto no dedo e não peso; o "contínuo" é o que precisa sobreviver em qualquer opção |

### 8. `Bow` — hoje: "Arco (Bow)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Arco de flecha (Bow) (20) | "Arco" sozinho é ambíguo em português (arco de círculo, arco elétrico); "de flecha" resolve em três sílabas, e o `(Bow)` continua achando o modo no guia |
| Tensão que dispara (Bow) (24) | Descreve exatamente o efeito — tensão crescente com disparo ao soltar — mas quebra a linha no piso |
| Arco e flecha (Bow) (19) | Igualmente claro; "de flecha" é preferido por dizer que o gatilho é o arco, não a flecha |

### 9. `Galloping` — hoje: "Galope (Galloping)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Galope (Galloping) (18) | Este já está bom: é imagem única, curta, e o termo em inglês está lá para o guia. Trocar seria mexer no que funciona |
| Cavalgada (Galloping) (21) | Se ela achar "galope" pouco descritivo; ocupa mais e ganha pouco |
| Trote (Galloping) (17) | Mais curto; trote e galope são cadências diferentes, e o modo é galope |

### 10. `SemiAutoGun` — hoje: "Arma semi-automática"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Tiro a tiro (11) | É o que a mão faz: cada puxada dá um tiro, com coice curto. Curtíssimo, e a primeira palavra separa dos outros três de arma |
| Coice curto por tiro (20) | O mais fiel à sensação; mais comprido, e "coice" pode soar estranho a quem não atira em jogo |
| Arma semi-automática (20) | O de hoje; "semi-automática" é a palavra mais longa da grade inteira (15 caracteres) e o nome descreve a arma, não o gatilho |

### 11. `AutoGun` — hoje: "Arma automática"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Rajada contínua (15) | Enquanto segura, treme sem parar. "Rajada" já é o vocabulário de quem joga tiro, e a primeira palavra é única na grade |
| Arma automática (15) | O de hoje; continua nomeando a arma em vez do que o dedo sente, e o primeiro termo empata com "Arma semi-automática" |
| Segurar e tremer (16) | O mais literal de todos; deselegante ao lado dos outros dezoito |

### 12. `Machine` — hoje: "Metralhadora (Machine)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Metralhadora (Machine) (22) | Está no limite exato de 22 e cabe. A palavra é única, a imagem é imediata e o `(Machine)` acha o modo no guia |
| Martelete (Machine) (19) | O efeito tem dois picos de amplitude, que é mais britadeira do que arma; se ela usar o modo fora de jogo de tiro, este nome fica melhor |
| Broca dupla (Machine) (21) | Nomeia o que o modo tem de particular (os dois picos); mais obscuro para quem chega |

### 13. `Feedback` — hoje: "Feedback"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Ponto duro (10) | É o modo mais mal nomeado da grade e o que mais ganha: o dedo desce livre e encontra um ponto duro no meio do curso. Curto, primeira palavra única, e tira a única palavra em inglês que não serve para achar nada |
| Aperto num ponto (16) | Se ela quiser dizer que a resistência continua depois do ponto, e não que é um obstáculo isolado |
| Firmeza num ponto (17) | Aproxima do item 3 (`Firmeza única`) e mostra que são parentes — de fato são o mesmo modo HID, `RIGID_B`; custa a repetição da primeira palavra |

### 14. `Weapon` — hoje: "Arma (Weapon)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Disparo (Weapon) (16) | "Arma" sozinho não diz nada num painel com outras três armas; "disparo" é o evento que o dedo provoca, e a primeira palavra fica única |
| Gatilho de arma (Weapon) (24) | O mais claro em texto corrido; quebra a linha no piso, e "gatilho" é a palavra que nomeia a aba inteira |
| Trava e dispara (Weapon) (24) | Descreve o efeito (resistência até o ponto, depois solta); mesmo problema de largura |

### 15. `Vibration` — hoje: "Vibração"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Vibração contínua (17) | Mantém a palavra que ela já conhece e acrescenta o que a separa do item 18: aqui é uma vibração só, contínua, num ponto |
| Zumbido contínuo (16) | Libera a palavra "Vibração" para o item 18 e deixa as duas primeiras palavras bem distintas |
| Tremor num ponto (16) | Se ela preferir que "Tremor" seja o par de "Tremor por posição" do item 18; então o 18 precisaria virar "Vibração por posição" |

### 16. `SlopeFeedback` — hoje: "Feedback em rampa"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Rampa de força (14) | A rampa é o que o modo tem de próprio, então ela vai para a frente do nome — que é exatamente o que a grade precisa. Sai o "Feedback" |
| Aperto em rampa (15) | Combina com a opção "Aperto num ponto" do item 13, se ela escolher aquela |
| Força crescente (15) | O mais explícito, mas o modo também faz decrescente (basta inverter início e fim), e o nome passaria a mentir na metade dos casos |

### 17. `MultiPositionFeedback` — hoje: "Feedback por posição"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Curva de força (14) | É o que a tela mostra: dez posições, cada uma com sua força — uma curva desenhada à mão. Primeira palavra única e curta |
| Perfil por posição (18) | Se ela preferir a palavra "perfil"; o risco é confundir com os perfis de jogo, que é o vocabulário mais carregado do produto |
| Força posição a posição (23) | O mais literal; estoura o limite e quebra a linha no piso |

### 18. `MultiPositionVibration` — hoje: "Vibração por posição"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Tremor por posição (18) | Guarda "por posição" (que é o parentesco real com o item 17) e troca a primeira palavra, que é onde o olho bate |
| Vibração desenhada (18) | Se ela quiser manter "Vibração" nos dois modos de vibrar; volta a empatar a primeira palavra com o item 15 |
| Zumbido por posição (19) | Só faz sentido se o item 15 virar "Vibração contínua" e este ficar com uma palavra bem diferente |

### 19. `Custom` — hoje: "Personalizado (avançado)"

| Opção | Quando esse nome é melhor |
|---|---|
| **R** Montar do zero (14) | Diz o que a pessoa vai fazer: escolher um modo cru e sete forças na mão. Cabe com folga e resolve o único rótulo que hoje já quebra a linha no piso. O aviso "avançado" desce para a descrição |
| Valores crus (avançado) (23) | Honesto sobre o que acontece (vai direto para o controle); estoura o limite e "cru" é jargão |
| Personalizado (avançado) (24) | O de hoje; é o rótulo que quebra a linha no piso e sobe a altura mínima da grade |

## A lista recomendada, pronta para ela riscar

| `name` (não muda) | `label` hoje | Proposta | ch |
|---|---|---|---|
| `Off` | Desligado | Sem resistência | 15 |
| `Rigid` | Rígido (Rigid) | Barreira fixa (Rigid) | 21 |
| `SimpleRigid` | Rígido simples | Firmeza única | 13 |
| `Pulse` | Pulso | Tranco único | 12 |
| `PulseA` | Pulso (curva A) | Tranco no trecho (A) | 20 |
| `PulseB` | Pulso (curva B) | Tranco no trecho (B) | 20 |
| `Resistance` | Resistência | Resistência constante | 21 |
| `Bow` | Arco (Bow) | Arco de flecha (Bow) | 20 |
| `Galloping` | Galope (Galloping) | Galope (Galloping) | 18 |
| `SemiAutoGun` | Arma semi-automática | Tiro a tiro | 11 |
| `AutoGun` | Arma automática | Rajada contínua | 15 |
| `Machine` | Metralhadora (Machine) | Metralhadora (Machine) | 22 |
| `Feedback` | Feedback | Ponto duro | 10 |
| `Weapon` | Arma (Weapon) | Disparo (Weapon) | 16 |
| `Vibration` | Vibração | Vibração contínua | 17 |
| `SlopeFeedback` | Feedback em rampa | Rampa de força | 14 |
| `MultiPositionFeedback` | Feedback por posição | Curva de força | 14 |
| `MultiPositionVibration` | Vibração por posição | Tremor por posição | 18 |
| `Custom` | Personalizado (avançado) | Montar do zero | 14 |

Dois dos dezenove ficam **iguais** ao que já são (`Galloping` e `Machine`):
estão certos, e trocar nome que funciona é custo sem retorno.

Medido com esta lista montada na grade real, no piso de 1040px: **nenhum rótulo
quebra** e a altura mínima da grade fica em 306px — o mesmo número de hoje,
sendo que hoje um rótulo já quebra. A troca não custa um pixel.

### As descrições acompanham

A `description` de cada modo aparece em itálico logo abaixo da grade
(`app/actions/triggers_actions.py:437`), e é onde cabe o que não coube no botão.
As quatro que mudam de conteúdo, e não só de palavra:

| `name` | Descrição proposta |
|---|---|
| `SimpleRigid` | Barreira do começo ao fim, com um só ajuste de 0 a 8. |
| `Feedback` | Barreira a partir de uma posição, com força de 0 a 8. |
| `Custom` | Avançado: envia um modo e sete forças direto ao controle. |
| `Weapon` | Resistência até um ponto e o disparo ao vencê-lo. |

## O custo, medido

### Quantos arquivos mudam: três

| Arquivo | O que muda |
|---|---|
| `src/hefesto_dualsense4unix/app/actions/trigger_specs.py` | 19 `label` e 4 `description` — linhas 63 a 205 |
| `tests/unit/test_palavra_a_janela_fala_a_lingua.py` | a lista de cinco termos em `test_o_termo_tecnico_fica_so_onde_ajuda_a_achar_o_modo_em_guia`, linhas 247-249 |
| `src/hefesto_dualsense4unix/app/widgets/segmented_selector.py` | um comentário na linha 179 cita `Feedback em rampa` como exemplo do que quebra linha; passa a citar o rótulo novo |

Varredura feita rótulo a rótulo (os dezenove textos, procurados em `*.py`,
`*.md`, `*.glade` e `*.json` fora do `.venv`): **nenhum outro arquivo** contém
qualquer um deles. `docs/protocol/trigger-modes.md` documenta os modos pelo nome
da FÁBRICA (`rigid()`, `feedback()`, `slope_feedback()`), não pelo rótulo — não
precisa de uma vírgula.

### O teste que trava rótulo hoje

Só um, e ele trava exatamente os cinco termos entre parênteses:

```
tests/unit/test_palavra_a_janela_fala_a_lingua.py:244-249
    para termo em ("Rígido (Rigid)", "Arco (Bow)", "Galope (Galloping)",
                   "Metralhadora (Machine)", "Arma (Weapon)"):
        assert termo em rotulos
```

Dos cinco, a proposta mantém dois intactos (`Galope (Galloping)`,
`Metralhadora (Machine)`) e reescreve três (`Barreira fixa (Rigid)`,
`Arco de flecha (Bow)`, `Disparo (Weapon)`). **O teste tem de ser reescrito
junto, e não apagado**: o valor dele é garantir que o termo em inglês continua
lá dentro. A forma correta é trocar a asserção de "o rótulo é exatamente X" para
"o rótulo contém `(Rigid)`", que é o que o teste realmente quer dizer e que
sobrevive a qualquer troca futura de sinônimo.

Os outros três testes do mesmo grupo passam sem tocar:
`test_gatilhos_nao_mostram_jargao_em_ingles` (linha 237) proíbe `start+1`,
`raw HID`, `Mode HID`, `Force ` e `Pos ` — nenhum aparece na proposta; e
`test_o_arquivo_de_gatilhos_nao_guarda_mais_o_texto_antigo` (linha 252) olha o
fonte pelos mesmos termos banidos.

Nenhum outro teste da suíte usa os rótulos. Os que aparecem procurando por
`MultiPositionFeedback`, `SlopeFeedback` e afins
(`tests/unit/test_triggers_actions.py`, `test_draft_config.py`,
`test_gui_review_fixes.py`, `test_schema_multi_position.py`) usam o **`name`**,
que não muda.

### O catálogo `po/`: nenhum `msgid` muda, e o motivo é uma dívida

Medido: `app/actions/trigger_specs.py` tem **zero** ocorrências de `_(` — os
dezenove rótulos são literais nus. E `scripts/i18n_extract.sh:39-42` extrai do
Python só o que estiver dentro de `_()` ou `N_()`.

Portanto: **nenhum dos dezenove rótulos está em `po/hefesto-dualsense4unix.pot`,
em `po/pt_BR.po` nem em `po/en.po`**. Conferido por busca direta — `Rigid)`,
`Bow)`, `Galloping)`, `Machine)`, `Weapon)`, `Pulso` e `Rígido` não aparecem em
nenhum dos três arquivos. O `Desligado` que existe em `po/pt_BR.po:1062` vem do
glade, não do trigger: hoje ele está em `gui/main.glade:2422`, é o botão de
desligar a emulação e não tem relação com gatilho. (De passagem: o comentário de
procedência nesse mesmo `msgid` aponta para `gui/main.glade:1922`, linha que hoje
tem outro rótulo — o catálogo está desatualizado em relação ao glade, o que é
mais uma medida da dívida de i18n descrita acima.)

Consequências, as duas:

1. **Custo de tradução desta sprint: zero.** Não há `msgid` a mexer, nem
   tradução a refazer, nem `msgmerge` a rodar.
2. **A dívida que isso revela:** a aba de gatilhos inteira é **intraduzível**
   hoje. Quem rodar a janela em inglês vê "Vibração por posição". Isso não é
   problema desta sprint — a PALAVRA-01 já decidiu que i18n não entra junto com
   troca de texto (`2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md`,
   seção "O que NÃO entra") — mas fica registrado aqui, com o número medido, em
   vez de ser descoberto de novo daqui a um mês.

## Como você valida

Na tela, depois que a lista for escolhida e aplicada:

1. Abrir a aba **Gatilhos**. A grade de modos continua com sete linhas de três
   botões, na mesma altura de hoje — **nada mudou de lugar**.
2. Passar o olho pela **primeira palavra** de cada botão: dá para achar o modo
   sem ler a linha inteira. Não há mais dois botões começando por "Feedback"
   nem dois começando por "Vibração".
3. Encolher a janela até o tamanho de projeto: **nenhum rótulo quebra em duas
   linhas**, e a grade não empurra barra de rolagem. Hoje, no mesmo teste,
   "Personalizado (avançado)" quebra.
4. Escolher um modo qualquer: a linha em itálico embaixo da grade explica o que
   o botão não coube dizer.
5. **A prova que importa:** abrir um perfil que ela já tinha salvo — `acao`,
   `corrida`, `esportes` ou `pragmata` — e conferir que o gatilho continua
   selecionado no modo certo, com os mesmos valores. É a prova de que só o
   rótulo mudou e o `mode` do disco continua sendo lido.
6. Aplicar no controle e sentir: o efeito é o mesmo de antes. Nenhum byte mudou.

## O que NÃO entra

- **Nenhum `name` muda.** O motivo está medido na primeira seção: são chaves
  gravadas nos perfis dela, no IPC e no protocolo DSX. Renomear "Feedback" para
  "PontoDuro" no contrato faria `acao.json` e companhia pararem de abrir.
- **Nada de i18n.** Vale a decisão da PALAVRA-01. Envolver os dezenove rótulos
  em `_()` é uma sprint própria, com catálogo a preencher, e misturá-la aqui
  transformaria uma troca de texto reversível numa entrega de risco.
- **Os rótulos do "Efeito pronto" ficam para depois.** Existe um segundo nível
  de nomes, exibido quando o modo é `MultiPositionFeedback` ou
  `MultiPositionVibration` (`profiles/trigger_presets.py:55-71`): `Stop hard`,
  `Stop macio`, `Plateau central`, `Machine gun`, `Senoide`, `Linear médio`,
  `Personalizar`. Há inglês cru e há mistura de idioma numa lista só. É o mesmo
  problema desta sprint, num lugar que só aparece em dois dos dezenove modos —
  fica registrado, e entra numa rodada própria se ela quiser.
- **Os rótulos dos parâmetros ficam.** "Posição", "Início", "Fim", "Força",
  "Intensidade", "Frequência", "Pata 1", "Pata 2", "Amplitude A", "Amplitude B",
  "Período" já estão em português e já passaram pelo crivo da PALAVRA-01.
- **Consolidar os modos que são o mesmo modo HID não entra.** `Rigid`,
  `SimpleRigid` e `Feedback` são os três `RIGID_B` — é tentador reduzir a um só
  com escala configurável, e seria errado fazer isso aqui: mudaria o conjunto de
  dezenove, que é contrato do DSX e está travado por teste
  (`tests/unit/test_trigger_effects.py:217`).
- **Nada foi renomeado nesta rodada.** Esta sprint é a lista. A escolha é dela.
