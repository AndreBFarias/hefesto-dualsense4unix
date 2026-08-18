# O que as nove dimensões mediram e a síntese não usou — 13/08/2026

> **O que é esta página.** O estudo em paralelo da madrugada de 13/08 produziu nove
> relatórios crus, cerca de 380 KB, contra a árvore em `cc768d4`. A síntese deles
> está em
> [o projeto inteiro num mapa só](2026-08-13-o-projeto-inteiro-num-mapa-so.md) e
> cobre o essencial. **Os 380 KB não foram despejados aqui, de propósito.** Esta
> página guarda só o que passou no critério da casa: *se apagar isto faria alguém
> repetir um trabalho ou pagar um custo já pago?*
>
> São três coisas: **os números que só o relatório cru tem** (§1), **as perguntas
> abertas que a síntese comprimiu** (§2), e **as divergências entre os agentes**
> (§3). O que ficou de fora está listado com o motivo em §4 — essa lista é parte
> da entrega.
>
> **Tudo foi remedido contra a árvore de HOJE (`874fdda`), não contra `cc768d4`.**
> O commit da tarde mexeu em 100 arquivos, e mexeu justamente onde o estudo da
> manhã tinha medido: `docs/data/ensaios.csv`, `docs/data/mapa-controles.csv`,
> `scripts/check_paridade_transporte.py`, `bancada.py`, `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`.
> Onde o número mudou, está a mudança; onde a pergunta foi respondida, está dito
> que foi — e por quem.

---

## 1. Os números que só o relatório cru tem

A síntese publica o **censo do portão** (293 linhas, 586 células, 185 mudas, 48
afirmações fortes…). O que ela não publica é o **domínio real de cada coluna** — o
que os campos de fato contêm, contado no arquivo em vez de prometido no cabeçalho.
Isso é caro de refazer e é o que impede a próxima pessoa de inventar um valor novo
para uma coluna que já tem vocabulário.

### 1.1 O domínio de cada coluna do mapa de canais

**Medido em 13/08/2026 contra `874fdda`**, com `csv.DictReader` sobre
`docs/data/mapa-controles.csv` — 293 linhas × 45 colunas, 99 chaves canônicas
(`dualsense` 99, `pro` 97, `sn30` 97).

| coluna | domínio real, com a contagem |
|---|---|
| `familia` | `plataforma` 72 · `luz` 45 · `audio` 33 · `combinacao` 27 · `movimento` 24 · `vibracao` 21 · `gatilho` 18 · `energia` 15 · `entrada` 14 · `identidade` 12 · `toque` 12 |
| `existe` | `tem` 127 · `desconhecido` 81 · `nao-tem` 66 · `parcial` 19 |
| `cabo_aceita` | `sim` 109 · vazio 99 · `não` 67 · `parcial` 11 · `desconhecido` 7 |
| `radio_aceita` | `sim` 106 · vazio 94 · `não` 69 · `parcial` 13 · `desconhecido` 11 |
| `cabo_aciona` | `não` 120 · vazio 95 · `sim` 61 · `parcial` 17 |
| `radio_aciona` | `não` 121 · vazio 90 · `sim` 64 · `parcial` 18 |
| `cabo_canal` | vazio 122 · `hidraw` 60 · `outro` 37 · `evdev` 28 · `sysfs` 26 · `uhid` 16 · `alsa-pipewire` 4 |
| `radio_canal` | vazio 117 · `hidraw` 56 · `outro` 49 · `evdev` 28 · `sysfs` 24 · `uhid` 16 · `dbus` 3 |
| `cabo_confianca` | `inferido-do-codigo` 140 · vazio 95 · `medido` 53 · `incerto` 3 · `afirmado-no-doc` 2 |
| `radio_confianca` | `inferido-do-codigo` 150 · vazio 90 · `medido` 45 · `afirmado-no-doc` 5 · `incerto` 3 |
| `cabo_grau` | vazio 252 · `MONTOU` 34 · `O APARELHO OBEDECEU` 7 |
| `radio_grau` | vazio 249 · `MONTOU` 36 · `O APARELHO OBEDECEU` 8 |
| `provado_por` | vazio 257 · `aparelho` 22 · `fonte-do-driver` 12 · `descritor` 2 |
| `validade_dias` | vazio 260 · `180` 33 |

E o preenchimento das colunas de rede: `peca` **125 de 293** · `evdev` **27**
(pro 14, sn30 13, dualsense **0**) · `teste_que_morde` **40** · `mordida` **40** ·
`mordida_provada_em` **6** · `provado_em` **36** · `assimetria_declarada` **39** ·
`nota` **194** · `id_v1` **136** · `estado_hoje` **2**.

**As três leituras que só esta tabela dá:**

1. **`SAIU NO FIO` não aparece uma única vez** — 0 de 586 células. O degrau do meio
   da escada de grau nunca foi usado por ninguém. Ou ele é degrau morto (e a escada
   é de dois), ou falta o instrumento que separa "o byte saiu" de "o aparelho
   obedeceu". A distinção decide se `GRAUS_QUE_EXIGEM_ENSAIO`
   (`scripts/check_paridade_transporte.py:316`) tem metade decorativa.
2. **`olho-dela` não aparece em `provado_por` em nenhuma linha das 293** — o
   vocabulário que o método prevê (`ci` / `bancada` / `olho-dela`) e o que o CSV usa
   (`aparelho` / `fonte-do-driver` / `descritor`) são **dois vocabulários numa coluna
   só**. Enquanto isso não for decidido, a coluna não pode ganhar domínio, e continua
   sendo a única coluna de honestidade sem auditor.
3. **`afirmado-no-doc` é o valor mais raro do mapa inteiro** — 2 células no cabo, 5 no
   rádio, contra 140 e 150 de `inferido-do-codigo`. Quem afirmar que "o mapa repete
   documentação de terceiro" está errado por duas ordens de grandeza.

### 1.2 O caderno de bancada, por dentro

**Medido hoje** sobre `docs/data/ensaios.csv` — **77 ensaios**, 12 colunas:

- `transporte`: `radio` **56** · `cabo` **21**;
- `observado_por`: `olho-dela` **73** · `bancada` **4**;
- `presente` (o suspeito estava presente?): `sim` **45** · `não` **32**;
- linhas do mapa cobertas por ensaio: **12**, e **todas `@dualsense`** —
  `combinacao.cabo_e_radio.saida`, `combinacao.dois_no_radio.saida`,
  `combinacao.rumble_simultaneo`, `combinacao.slot_jogador.estabilidade`,
  `combinacao.tres_na_mesa`, `gatilho.adaptativo`, `gatilho.direito.adaptativo`,
  `gatilho.esquerdo.adaptativo`, `luz.lightbar.cor`, `vibracao.rumble.direito`,
  `vibracao.rumble.esquerdo`, `vibracao.rumble.ff`.

O `radio` ser quase três vezes o `cabo` não é acaso: é onde a casa apanhou. E os
**4 ensaios `bancada` contra 73 `olho-dela`** dizem, em número, o que o `CLAUDE.md`
diz em prosa — aqui a observação dela é fonte primária, não confirmação.

> **Caducou entre a manhã e a tarde:** o caderno tinha **11** colunas na leitura do
> estudo. Hoje tem **12** — `874fdda` acrescentou `resultado_da_feature`, preenchida
> em **1 de 77** (`obedece`). Ver §3.

### 1.3 O grau forte cruzado com o veredicto da própria casa

Este é o número mais desconfortável do estudo, e a síntese não o carrega. **Medido
hoje**, cruzando as células de grau forte do mapa com `scripts/eliminacao.py`, o
julgador que a casa escreveu:

| veredicto do julgador | células de grau forte |
|---|---:|
| `inconclusivo` | **11** |
| `e-a-causa` | 4 |
| **total** | **15** |

As quatro conclusivas são `combinacao.rumble_simultaneo@dualsense [radio]`,
`luz.lightbar.cor@dualsense [radio]`, `vibracao.rumble.ff@dualsense [cabo]` e
`[radio]`. As outras onze — inclusive as três linhas de gatilho adaptativo que o
portão `grau-sem-ensaio` flagrou e que foram pagas com medição nova — têm ensaio,
como a regra exige, e **o ensaio não conclui**.

**O que isso significa, com precisão:** a regra 6 do portão cobra **existência** de
ensaio, nunca **veredicto**. Ela está certa em cobrar existência primeiro — foi assim
que pegou três afirmações falsas da casa em 12/08. Mas *"O APARELHO OBEDECEU"* com
veredicto `inconclusivo` é uma afirmação mais forte do que a evidência sustenta em 11
dos 15 casos. Promover a regra a exigir `e-a-causa` custaria **11 reprovações novas**;
é decisão dela, e o número é este.

**E o portão só olha para cima.** O oposto também existe e ninguém avisa:
`vibracao.rumble.direito@dualsense [radio]` e `vibracao.rumble.esquerdo@dualsense
[radio]` têm veredicto **`e-a-causa`** no caderno e grau **`MONTOU`** no mapa — a
melhor evidência que a casa tem está **subdeclarada**, e nenhuma das onze regras
repara nisso.

### 1.4 `confianca = medido` quer dizer o quê?

**Medido hoje:** das **98** células com `confianca = medido`, **81 não têm um único
ensaio no caderno**, e **61 dessas não têm nem `provado_em`**.

Nenhuma regra cobra isso — a regra 6 olha o **grau**, não a **confiança**. Ou
`medido` quer dizer "alguém viu no aparelho", e falta o registro em 81 células; ou
quer dizer "o produto foi exercitado por teste", e aí é a mesma coisa que `MONTOU` e a
palavra está inflacionada. Estender a regra 6 à confiança é decisão de política, não
de código.

### 1.5 O censo dos graus da canônica

`docs/protocol/dualsense-referencia-canonica.md` **hoje**: 1.132 linhas, das quais
**56 carregam ao menos um marcador de grau** (64 ocorrências, porque algumas linhas
trazem dois): `ALTA` 32 · `MEDIDO AQUI` 13 · `MÉDIA` 7 · `FONTE DESTA MÁQUINA` 7 ·
`BAIXA` 5. Das **93 linhas de tabela** (fora separadores), apenas **8** trazem grau na
própria linha.

**A leitura:** a página **governa por herança de seção, não linha a linha**. Os
offsets, os bytes e os modos moram nas 93 linhas de tabela e quase todas herdam o grau
de um cabeçalho. Isso é econômico e é frágil pelo mesmo motivo — e é exatamente por
isso que o achado C-5 da síntese (o §2 declarar `FONTE DESTA MÁQUINA` sobre 29 bytes
que o driver não nomeia) é caro: **um cabeçalho generoso empresta autoridade de fonte
a tudo que vem embaixo.**

> **Ressalva de instrumento, que esta casa exige.** A régua acima é minha: conto
> ocorrência da palavra do grau por linha, com `str.count`. O relatório cru mediu
> `1.125` linhas e `ALTA` 28 / total 60 contra `cc768d4`. Parte da diferença é o
> arquivo ter crescido 7 linhas em `874fdda`; **parte pode ser régua diferente, e eu
> não comparei as duas.** Os números estruturais — 56 linhas com grau, 93 de tabela,
> 8 com grau próprio, 15 declarações de seção — bateram nos dois.

### 1.6 A forma da suíte e dos portões

**Medido hoje:**

- **9130 nós** coletados (9118 em `tests/unit`, 12 em `tests/core`, 529 arquivos), em
  ~15 s. Não há pasta `integration`.
- `tests/conftest.py` tem **1.463 linhas** e não é arquivo de fixtures — é arquivo de
  **guardas**, cada uma nascida de um defeito medido: `GUARDA-GI-REAL-01` (`:28`, o
  `gi` falso de um arquivo não vaza para o seguinte pela ordem alfabética),
  `CANARIO-FS-01` (`:339`, a suíte não escreve no `~/.config` dela),
  `BERCO-DE-TMP-01` (`:518`, a suíte devolve o `/tmp` como encontrou),
  `ARVORE-CONGELADA-01` (`:929`, a bancada não mede um produto que mudou debaixo
  dela) e a fixture parametrizada `transporte` (`:1384`), que faz cada caso rodar
  `[usb]` e `[bt]`.
- O portão da promessa, `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`,
  coleta **27 testes** (eram 23 em `cc768d4`) e **continua fora de `pytest -q`** por
  não se chamar `test_*`. Os dois registros dele hoje: **`_SEM_CAMINHO_HOJE` com 19
  entradas** (`:580`) e **`_NAO_E_PROMESSA` com 11** (`:472`) — eram 23 e 10.

### 1.7 Números soltos que valem mais que o parágrafo em que estavam

- **`check_test_data.sh` varre só `tests/`, e só `.py` e `.json`**
  (`scripts/check_test_data.sh:31` e `:36`). Quem confiar nele para `src/` ou `docs/`
  está confiando em cobertura que não existe; quem cobre isso é o
  `test_docs_mac_anonimato.py`, e essa divisão de trabalho não está escrita em lugar
  nenhum.
- **O `.glade` está fora do portão de acentuação**, por whitelist explícita
  (`scripts/validar-acentuacao.py:434`) — e é onde moram as strings que ela lê na
  tela. Tirá-lo da lista exigiria ensinar o validador a pular comentário XML e id de
  widget: **77 ocorrências não-visíveis reprovariam de imediato**.
- **`hefesto test trigger|led|rumble` não sabe mirar** — a palavra `uniq` não aparece
  uma única vez em `src/hefesto_dualsense4unix/cli/cmd_test.py` (medido hoje: 0
  ocorrências). Com quatro DualSense na mesa, a janela consegue escolher um e o
  comando de bancada não.
- **Os 14.105 `hidraw_broker_hidden` em sete dias** estão cravados num docstring
  marcado MEDIDO (`src/hefesto_dualsense4unix/daemon/battery_journal.py:55`) e **não
  há script versionado que os reproduza**. É número sem origem conferível dentro do
  repositório — o tipo exato de afirmação que a régua desta casa desce de nível.
- **Ninguém sabe quem apara o espaço no fim das linhas do `specs.html`.** O
  `normaliza()` do gerador presume que existe alguém (`scripts/gerar-mapa.py:977-989`,
  o `rstrip()` em `:989` com a razão escrita em `:982`), o `.pre-commit-config.yaml`
  **não tem hook de trailing-whitespace** (medido hoje: os dez hooks são outros), e
  nenhum script da árvore o faz. **Dois agentes chegaram a essa pergunta por caminhos
  independentes.** Se a resposta for "o editor dela", há um `rstrip()` dentro de um
  portão de CI compensando comportamento de ferramenta pessoal — funciona, e está
  documentado como se fosse da casa.

---

## 2. As perguntas abertas que a síntese comprimiu

A síntese tem uma §6 excelente para *decidir o que fazer a seguir*. O que ela
comprime é a **pergunta técnica** de cada dimensão — a frase que diz o que se deixaria
de saber. Estas são as que sobreviveram ao corte e **continuam abertas hoje**; as que
o commit da tarde fechou estão em §3.

### 2.1 Protocolo — o que o aparelho entende

1. **O alto-falante toca?** O descritor prova que o DualSense **aceita** nove degraus
   de report de output por rádio (`0x31`=77 B até `0x39`=546 B, escada de +64 B).
   Prova aceitação, **não efeito**: nenhum byte de áudio de saída por rádio foi escrito
   nesta casa, nunca. A pergunta certa, que substitui a velha *"0x32 ou 0x39?"*: **um
   bloco TLV de alto-falante no degrau de tamanho compatível faz o alto-falante
   tocar?** Isso já é ESCRITA no controle — **muda a classe de risco do ensaio**, e é
   por isso que ela não é a mesma pergunta de antes.
2. **`weapon()` e `vibration()` fazem alguma coisa no dedo?** Os dois mandam bytes que
   a própria canônica chama de errados (`PULSE_B` = 0x06 e `PULSE_A` = 0x22, em
   `src/hefesto_dualsense4unix/core/trigger_effects.py:128-129`, usados em `:461-466`
   e `:469-481`). **E a decisão dela de 01/08 já diz qual lado vence:** *"as duas
   temos nomes perfeitos, pq essa é a sensação de usar ambas"* — ou seja, o resultado
   do ensaio pode ser **trocar o NOME, não o byte**. Quem for corrigir "o modo errado"
   sem ler isto vai desfazer uma escolha dela.
3. **Quem reaplica o efeito de gatilho com período de minutos?** Aos 120 s a leitura
   se inverteu (L2 solto, R2 vivo) e **o resultado não é monotônico** — logo não é
   decaimento. O suspeito hoje tem nome que não tinha em 11/08: a rajada da Steam é
   **por evento** e repinta todos os controles a cada conexão nova. Mas isso foi
   medido para a **lightbar**, não para o bloco de gatilho. Vale repetir a rodada de
   120 s **com a Steam fechada** — a variável que ninguém isolou.
4. **De quantos bits de autorização o firmware precisa para vibrar?** Sabe-se que o
   conjunto inteiro funciona e que os bytes agem **sem** os bits; não se sabe qual bit
   ainda compra alguma coisa. **É a pergunta que dá lucro**, porque é a poda: foi
   assim que a lightbar encolheu de cinco canais para um.
5. **Os bits são porteiro dos blocos de LED e de áudio?** Medido para os motores (não
   são) e para o gatilho (o mecanismo é outro). Para **cor e volume, nada**. O desenho
   é o mesmo da troca-de-lado: mudar o valor com o bit desligado e ver se muda.
6. **O bit `0x10` (autorização do volume do fone) existe neste firmware?** Ele **não
   aparece no driver em forma nenhuma** — o fonte define exatamente cinco bits de
   `valid_flag0`, BIT(0), BIT(1), BIT(5), BIT(6) e BIT(7)
   (`assets/dkms/hid-playstation/hid-playstation.c:206-211`). Nenhuma leitura de fonte
   pode promovê-lo: o `0x10` desta árvore é de comunidade. Só ensaio com headset no
   jack fecha.
7. **Qual taxa o SDL DECLARA ao jogo para o vpad**, que se anuncia Edge? O lado do
   aparelho está fechado (cabo 250,0 Hz; rádio variável, nunca 1000). A conta sugere
   erro de escala de 4x num jogo que integre pela taxa declarada, mas **ninguém
   observou o efeito** — e a régua é metade do ensaio: só vale contra a SDL3 que a
   Steam distribui.
8. **O que decide QUAL controle a Steam repinta?** O magenta pegou nos três no
   instante e não durou nos três: *"dois dos controles ficaram magenta e o branco tá
   vermelho no player 2"*. Não medido — **e é o que separa o gatilho de cor de ser
   cura ou paliativo.**
9. **As 98 escritas da Steam na probe foram CONTADAS, não DECODIFICADAS.** Não se sabe
   que report ela manda, nem se algum pede a barra apagada. **As capturas ficaram em
   `/tmp/hefesto-probe-lightbar/`, e `/tmp` não sobrevive a reboot.** Se ainda
   existirem, decodificá-las é leitura pura — e é a única desta lista com prazo de
   validade físico.
10. **Nenhuma linha de `pro` ou `sn30` tem grau `O APARELHO OBEDECEU`** — as 15 são
    todas do `dualsense`, e os 77 ensaios também. Isso é retrato honesto (nunca se
    ensaiou nada neles) ou é medição feita e não registrada? Antes de qualquer
    afirmação forte sobre os externos, essa **assimetria de evidência** precisa de
    resposta explícita.

### 2.2 O mapa, o caderno e os portões

1. **O portão deve exigir VEREDICTO, e não só existência de ensaio?** Custo medido
   hoje: 11 reprovações novas (§1.3).
2. **Deve existir regra para grau BAIXO demais?** Hoje a melhor evidência da casa está
   subdeclarada e ninguém avisa (§1.3).
3. **`OLHO_DELA_REPROVA = True` custaria ZERO reprovações hoje.** O interruptor está em
   `scripts/check_paridade_transporte.py:242`, e o próprio comentário ao lado diz que
   promovê-lo *"custaria ZERO reprovações novas, então o preço de deixá-la avisando é
   só o futuro"*. A razão escrita para mantê-lo `False` é que cobrar QUEM observou
   *"é uma segunda regra, que ninguém pediu"* — mas o `METODO-DE-ISOLAMENTO.md` já a
   pede. **Ligar agora trava o degrau mais alto de graça.**
4. **O resumo do censo conta o caderno inteiro, não os casados.**
   `scripts/check_paridade_transporte.py:645` soma todas as listas de
   `ensaios_por_lado`, então **ensaio órfão continua sendo contado como cobertura**:
   com 9 órfãos injetados, o resumo continuou dizendo 77. Hoje são **0 órfãos** — e é
   por isso que a hora de consertar é agora, enquanto o conserto não muda número
   nenhum.
5. **`_sim('')` devolve `False`** (`scripts/eliminacao.py:77-78`), então um `presente`
   vazio vira silenciosamente "SEM o suspeito" e **pode fabricar um veredicto**. Hoje
   0 de 77 estão vazias, e nada impede: o formulário da bancada só oferece COM/SEM, e
   edição à mão do CSV não passa por régua nenhuma.
6. **O `ensaios.csv` continua sem validador próprio.** `resultado` é texto livre,
   `linha_id` não é cobrado contra o mapa, o esquema não é conferido. Hoje casam 12 de
   12 por cuidado. O portão teria de cobrar **só forma, nunca semântica** — porque o
   `resultado` é justamente a coluna que o próprio portão explica por que não se pode
   cobrar como falha (`scripts/check_paridade_transporte.py:121-130`).
7. **`aceita` vazio com `aciona` respondido: buraco de censo ou desenho?** As 8 células
   nesse estado incluem quatro medições da bancada de 12/08 que a tela pinta como
   "ninguém respondeu". **As duas curas são opostas e só uma é reversível:** preencher
   `cabo_aceita`/`radio_aceita` nas quatro linhas (dado, reversível), ou trocar a ordem
   em `simboloLado` para o silêncio só valer quando os DOIS estiverem vazios (régua,
   muda 193 células de uma vez).
8. **`entrada.botoes` promete no rótulo os botões de face e os ombros, e a `peca` só
   aponta o D-pad** — enquanto `cross circle square triangle` acendem por
   `plataforma.inventario`, e o `l1`/`r1` do DualSense não acende por linha nenhuma.
   Realocar as peças é dado, não código; **mas o rótulo dos três controles está
   escrito no léxico da Nintendo, inclusive na linha do DualSense**, e isso é decisão
   de vocabulário dela.
9. **O `id` `led-jogador` está duplicado em `assets/control-svg/8bitdo-sn30-pro.svg`,
   nas linhas 229 e 252.** Depois do prefixo os dois viram `sn30__led-jogador` e
   `getElementById` devolve só o primeiro. A pergunta não é o defeito, é o desenho: os
   dois grupos deveriam ter ids distintos (`led-jogador-topo` / `led-jogador-frente`)?
   **Quem sabe é quem desenhou.**
10. **`estado_hoje` fica sendo vocabulário curto ou texto livre?** O risco de perda de
    dado foi fechado em `874fdda` (ver §3), e a decisão de fundo é dela, escrita no
    próprio `bancada.py:107`.

### 2.3 O daemon e o contrato do IPC

1. **O `trigger.set` deve ganhar `aplicado_em` (ou um `escrito_em`) pelo menos para o
   caso da mesa vazia?** Hoje o cliente não tem como distinguir "aplicado nos quatro"
   de "não havia ninguém". A justificativa de merge que dispensou a cura no LED **não
   cobre esse caso**. É decisão de contrato, não de mecanismo.
2. **O `aplicado_em` do ramo por-`uniq` deve passar a significar CONECTADO** (como no
   ramo broadcast) **ou deve ganhar um segundo campo** (`registrado_em` contra
   `escrito_em`)? Hoje o mesmo nome carrega duas verdades no mesmo handler, e a versão
   por-`uniq` é a que pode mentir. **A bifurcação é a decisão** — a síntese registra o
   defeito (A-1) e não registra as duas saídas.
3. **A reabertura da janela de confirmação do keepalive por mudança de COR ou de
   GATILHO — e não só de vibração — é aceitável?** Se for, o comentário do `sendReport`
   precisa dizer isso; se não for, o `_last_change_at` teria de ser **por campo** e não
   pelo report inteiro. E essa é mudança que **só a bancada com quatro controles pode
   aceitar**.
4. **O `dbus` deve continuar no domínio do `check_paridade_transporte.py`** se nenhum
   aparelho o usa como canal de saída em código? São 3 células, todas `@sn30`.
   **Manter um valor que o produto não produz é convidar uma linha futura a
   declará-lo sem prova.**

### 2.4 A suíte e o ritual

1. **`mordida_provada_em`: transcrever à mão ou fazer o portão ler?** A prova mora no
   bloco `MORDIDA PROVADA` do docstring de seis arquivos de teste. Transcrever é
   papelada e liga a regra 11; fazer o portão **ler** o bloco é uma régua a mais — e
   nesta casa o instrumento já mentiu mais que o produto. Em `874fdda` a casa escolheu
   transcrever seis; a pergunta de método continua para as próximas.
2. **O `portao_a_casa_sabe_e_o_produto_nao_faz.py` entra no bloco "Antes de fechar
   qualquer leva"?** Se entrar, ele passa a ser derivado pelo meta-portão — **que hoje
   está cego no CI**. Se não entrar, os 27 testes continuam fora do ritual que a casa
   manda rodar.
3. **`test_paridade_transporte_rumble_em_par.py:22-24` ainda diz que a premissa do
   keepalive neutro "continua sendo a próxima coisa a medir na bancada"** — e ela caiu
   em 11/08, por dose-resposta. Pela regra da casa (fato errado se SUBSTITUI) o
   docstring deveria ser corrigido; **quem decide se o teste passa a se chamar outra
   coisa é ela.** Note o desconforto: o mesmo arquivo ganhou em `874fdda` um bloco
   `MORDIDA PROVADA (13/08/2026…)` logo abaixo da frase caduca.
4. **O piso de coleta do CI sobe?** 5100 contra 9130 reais. Subi-lo fecharia a folga
   onde um módulo inteiro pode sumir calado — e o próprio comentário diz que ele "só
   sobe quando alguém quiser subi-lo".

### 2.5 O que ficou pendurado, e é da mão dela

1. **O suspeito ANTIGO da lightbar continua CONFUSO no caderno** — cinco ensaios, com
   `com` = "não obedece" / "parcial" / "não obedece" e `sem` = "obedece" / "obedece".
   **O `parcial` nunca foi explicado.** Vale reclassificar aqueles cinco para o
   suspeito por btmon, que fechou, ou o CONFUSO fica de pé para sempre?
2. **A divergência de data que a própria
   [CANETA-NA-MÃO-01](../sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md)
   §8 declara:** três ensaios do bloco do Steam com
   `quando = 2026-08-12T23:20` e a nota de um deles
   descrevendo a contaminação como *"a noite inteira de 11/08 até 23h13"*. **Continua
   sem reconciliação e exige o journal na mão.**
3. **As duas medições mais recentes do caderno inteiro não são citadas em página
   nenhuma de `docs/protocol/`.** `gatilho-1500ms-por-controle` (parcial) e
   `gatilho-escrever-no-silencio` (obedece, aceite dela: *"perfeito"*) são as que
   estabelecem que **a rajada da Steam é por EVENTO**, não por controle. Elas estão em
   `docs/data/ensaios.csv:52-53`; a página da pilha cita como fonte
   `docs/protocol/pilha-steam-input-xpad-sdl.md:1001` a faixa `ensaios.csv:41-51`, que
   **não as inclui**.
   > **Cuidado de leitura que vale registrar:** *"gatilho"* nessas duas linhas é o
   > gancho de software da lightbar, **não** o gatilho L2/R2. A mesma palavra nomeia
   > duas coisas dentro do mesmo arquivo CSV.
4. **A quinta lâmpada dos externos.** O produto trata `:blue:player-5` como bit "+5"
   da numeração de jogador (`src/hefesto_dualsense4unix/core/external_leds.py:57`),
   e no driver aquele nó é o **LED HOME**, escrito por um subcomando diferente. O anel
   de Home do 8BitDo acende? **É pergunta de olho, 5 minutos, e decide se corrigir o
   `write_player_number` é conserto ou regressão.**
5. **`provado_em` uma data atrás do que o sustenta:** as três linhas de gatilho
   adaptativo do `dualsense` estão com `provado_em = 2026-08-11`, e o grau forte na
   coluna do RÁDIO só passou a ter ensaio em **12/08** — foi o portão `grau-sem-ensaio`
   que flagrou a falta. Não é erro grave; é o tipo de deriva que faz a próxima pessoa
   procurar um ensaio na data errada.
6. **As 16 branches `worktree-*` e os 740 MB em `.claude/worktrees/`.** Nada aqui apaga
   nada — fica a pergunta de a quem cabe a limpeza, e se alguma delas deve virar
   branch nomeada antes de sumir.

---

## 3. Divergências entre os agentes, e o que caducou entre a manhã e a tarde

**Esta seção é a que mais economiza tempo**, porque cada linha aqui é um número que
alguém repetiria de boa-fé.

### 3.1 Onde os agentes discordaram

| o quê | o que cada um mediu | o que vale |
|---|---|---|
| células mudas do mapa | **193** (régua `aceita`, o que o rodapé do `specs.html` publica) contra **185** (régua `aciona`, o que o censo do portão publica) | **as duas estão certas por definições diferentes**, e a diferença são exatamente 8 células. Enquanto não houver régua única, todo relatório que citar o número precisa dizer **de quem ele é** |
| regras do `84-nintendo-pro-variant.rules` | **seis** (relatório de protocolo) contra **oito** (recontado no transporte) | **oito** |
| lacunas do portão da promessa | **29** (um agente), **33** (o docstring do próprio portão), **23 + 10** (recontado por AST em `cc768d4`) | **hoje: 19 em `_SEM_CAMINHO_HOJE` e 11 em `_NAO_E_PROMESSA`.** Nenhuma das três contagens anteriores vale, e a do docstring era a mais citada |
| a rota do rumble por MAC | um agente concluiu *"escreve direto no controller, que é broadcast"* e propôs **mecanismo novo no backend** | **falso nas duas metades** — o pulso já mira, e `set_rumble_for` já existia. Derrubado pelo censo das dez abas do mesmo dia, e já substituído na síntese |
| quantos agentes | **doze** (quem conduziu) contra **sete dimensões** de material contra **nove** (o crítico de completude) | os três seguem na mesa, sem recontagem — e esta página é a nona e a décima dimensão transportadas |

### 3.2 O que o commit da tarde respondeu, e o estudo listava como aberto

Cada item aqui é uma pergunta que **não se deve mais fazer** — está paga.

- **"Os player LEDs chegam ao aparelho por qual caminho hoje?"** — respondida e
  fechada por `LED-BITS-CHEGAM-01`. Os bits chegam, por **outro** caminho:
  `ProfileManager.apply` emite `player_leds` dentro do `OutputSpec`, e o backend
  converte em `_write_partial_output`. O docstring de
  `src/hefesto_dualsense4unix/core/led_control.py` que afirmava *"os bits nunca chegam
  ao controle"* foi **substituído**, não anotado ao lado, com a razão escrita: *"um
  fato errado não é decisão medida"*. O teste que segura é
  `tests/unit/test_perfil_acende_os_pontinhos_do_jogador.py`.
- **"Como o portão da promessa passa a enxergar `install.sh` e `uninstall.sh`?"** —
  respondida: a varredura passou a ler `.sh`, e `strip_quirks_token` saiu da lista de
  dívida (`tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:29` e `:154` registram
  a causa e a cura).
- **"O `estado_hoje` vai ser apagado pelo formulário da bancada?"** — o risco foi
  fechado por `BANCADA-ESTADOS-01`: as duas prosas longas entraram no `ESTADOS`
  (`bancada.py:123-125`) transcritas byte a byte, **com os acentos que faltam no
  original**, e há teste que reprova se a transcrição divergir de uma letra. A decisão
  de fundo (vocabulário curto ou texto livre) segue dela, e está escrita em
  `bancada.py:107`.
- **"O `resultado` do caderno responde ao suspeito ou à feature?"** — a casa respondeu
  **acrescentando uma coluna**: `resultado_da_feature` existe hoje em
  `docs/data/ensaios.csv`, preenchida em **1 de 77**. A ambiguidade deixou de ser
  ambiguidade e virou dívida de preenchimento.
- **"Nenhum portão olha a coluna `peca`"** e **"a mordida provada mora só no
  docstring"** — fechadas, e já registradas na síntese (B-9 e B-6).

### 3.3 O achado positivo que ninguém precisa refazer

**As citações por número de linha ao `docs/data/ensaios.csv` continuam todas
abrindo** — conferidas de novo hoje, uma a uma: `:22-23` são `keepalive-dose-cabo` e
`keepalive-dose-radio`; `:24` é `keepalive-premissa-troca-de-lado`; `:29-30` são
`gatilho-keepalive-8s` e `-30s`; `:36` é `gatilho-lado-nao-esta-invertido`; `:37` é
`gatilho-quem-apaga-nao-e-o-keepalive`; `:52-53` são as duas de 12/08 23:57; `:63-64`
e `:67` são os três de gatilho isolado.

**E elas sobreviveram a um diff de 156 linhas no arquivo**, porque `874fdda` mexeu em
**coluna**, não em linha: o caderno tem 77 ensaios e 78 linhas físicas, sem campo com
quebra embutida. Citação por número de linha em CSV que cresce é a coisa mais frágil
que esta casa faz — **desta vez ela aguentou, e por um motivo que não se repete
sozinho.**

---

## 4. O que deixei de fora, e por quê

Isto é parte da entrega: o que não está aqui, e a razão.

1. **Os nove relatórios crus inteiros (~380 KB).** A "Resposta direta" e o "Como
   funciona" de cada um são reescrita do que a síntese já diz melhor e mais curto.
   Guardar os dois obrigaria a próxima pessoa a ler duas versões da mesma coisa e
   escolher.
2. **As seções "Achados" das nove dimensões.** A síntese as absorveu, ordenadas por
   importância e com o grau de cada uma, e **corrigiu três** no caminho. Transportá-las
   de novo reintroduziria as versões não corrigidas — que é exatamente o defeito que a
   casa chama de *fato errado guardado ao lado do certo*.
3. **As seções "O que caducou" das nove dimensões.** Estão na §5 da síntese, com 15
   itens já reconciliados. O que sobrou de novo está na §3 desta página.
4. **Os cabeçalhos de agente, os JSON de relatório e as ressalvas de processo**
   ("não abri a GUI", "rodei numa cópia em `/tmp`", "não consigo ver o GitHub daqui").
   São andaime: dizem como o trabalho foi feito naquele dia, não o que se aprendeu.
   **A exceção que guardei** está na §1.5 — a ressalva de instrumento, porque ela muda
   como se lê um número.
5. **As perguntas abertas que já eram decisão dela na §6.2 da síntese** — plugins,
   notificações, PyPI, bonds, cache do BlueZ, os dois workflows, o P1 da caixinha, o
   histórico de perfis. Estão lá com o custo em minutos, que é a forma em que ela
   decide. Repeti-las aqui só faria a lista dela ficar mais longa.
6. **As perguntas que o commit da tarde fechou.** Não sumiram: viraram a §3.2, com o
   nome de quem as fechou. Apagá-las apagaria o motivo de o trabalho ter sido feito.
7. **O número "229 palavras portuguesas sem acento na prosa dos dois CSV".** É medição
   de régua própria não versionada, e eu **não a reproduzi**. Enquanto não houver
   script que a refaça, ela seria mais um número sem origem conferível — o defeito que
   §1.7 acusa em outro lugar.
8. **A crítica do guia de isolamento.** Ela não coube aqui porque é outra coisa: está
   em
   [o crítico do guia de isolamento, e o que sobrou](2026-08-13-o-critico-do-guia-de-isolamento-e-o-que-sobrou.md).

---

## Nota sobre esta página

Escrita em 13/08/2026, sobre material que existia só em `/tmp` e morreria com a
próxima limpeza. Somente leitura: nenhum serviço tocado, nenhum controle derrubado, o
daemon vivo o tempo todo. **Uma única escrita fora de `docs/process/estudos/`**, e ela
está declarada: as duas faixas de linha corrigidas em
`docs/process/METODO-DE-ISOLAMENTO.md:111-113`, pelo motivo explicado na página do
crítico.

Cada número desta página foi remedido contra `874fdda`. Onde a régua é minha, está
dito. Onde o relatório cru mediu outra coisa, os dois números estão na mesa.
