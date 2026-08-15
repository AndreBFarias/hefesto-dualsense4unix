# A QUEDA — o que sobreviveu, e o que falta materializar

**15/08/2026, escrito depois.** O terminal fechou às **14:50**, quarenta minutos
depois do último commit, com **cinco agentes no meio do trabalho** e a leva
inteira do dia parada no índice do git.

Esta página é o inventário da queda. Ela existe porque a próxima sessão não
pode ter de reconstruir de cabeça o que dez frentes mediram num dia só — e
porque o material mais valioso do dia é justamente o que ainda **não** virou
commit.

**A boa notícia cabe numa linha:** quase nada de conteúdo se perdeu, e a suíte
completa — que dois agentes morreram tentando rodar e que ninguém tinha visto
fechar — está **verde**. O risco de hoje não é perda, é **fragilidade**.

---

## 1. O que aconteceu

Às 14:10 saiu o commit `4422245`, com as vinte e seis decisões dela
respondidas. Nos quarenta minutos seguintes, seis agentes trabalhavam em
paralelo em territórios exclusivos — a cor do plástico, a ordem dos jogadores,
a máscara por jogador, a renomeação das colunas do mapa, a arqueologia da
lightbar travada e o grab do primário. Às **14:48:09** as chamadas de
ferramenta começaram a ser recusadas em série, e às **14:50** a sessão morreu.
Dois agentes morreram **dentro** da suíte completa do pytest; um foi
interrompido **nove segundos** depois de começar a corrigir a página que ele
mesmo acabara de declarar mentirosa. Nenhum deles chegou a escrever o relatório
final que a tarefa pedia. Nada foi commitado depois das 14:10 — e é esse o fato
que governa todo o resto desta página.

---

## 2. O que JÁ está salvo

### 2.1. O commit

`4422245` — *docs(decisões): as vinte e seis respondidas, e duas perguntas
derrubadas por ela*. Continua sendo o `HEAD`. **É o único commit da tarde.**

### 2.2. O índice, que é onde mora a leva inteira

```
git diff --cached --stat  ->  33 files changed, 5908 insertions(+), 193 deletions(-)
git status --porcelain    ->  36 entradas (5 com mudança TAMBÉM fora do índice)
```

E, ao contrário do que os próprios agentes temiam, **a leva passa em todos os
portões da casa**. Rodados na árvore viva, depois da queda:

| portão | resultado |
|---|---|
| `pytest -q` (a suíte **inteira**) | **9692 passed, 1 skipped, 5 xfailed** em 380,67 s — `rc=0` |
| `ruff check src/ tests/` e também `scripts/ bancada.py` | All checks passed |
| `mypy src/hefesto_dualsense4unix` | Success — 174 arquivos |
| `validar-acentuacao.py --all` · `validar-glifos.py --all` | `rc=0` |
| `validar-referencias-docs.py --all` | OK, 322 documentos |
| `validar-citacoes-de-linha.py --all` | OK, 121 citações |
| `check_paridade_transporte.py` | `rc=0` — 25 graus fortes, 0 sem ensaio |
| `gerar-mapa.py --check` | `rc=0` |
| `check_version_consistency.py` · `check_packaging_parity.sh` · `check_test_data.sh` · `check_anonymity.sh` | todos OK |

**Isto responde a maior pergunta em aberto da queda.** Os dois agentes que
morreram dentro do pytest (a ordem congelada e a máscara por jogador) nunca
souberam se o trabalho deles fechava. Fechava. O que os travou não era defeito
nenhum: era **uma citação de linha podre** em
`docs/protocol/dualsense-referencia-canonica.md:1218`, apontando para
`uhid_gamepad.py:1747` quando `forward_jack` já tinha andado para `:1763` —
colateral de uma terceira frente, e hoje corrigida.

### 2.3. As medições que sobreviveram inteiras

- **A cor do plástico saiu do firmware, por cabo.** `hidraw4`
  (`hardware_version 0x00001111`) devolveu código **05 = Starlight Blue**;
  `hidraw5` (`0x00000710`) devolveu **04 = Galactic Purple**, por
  `SET_FEATURE 0x80` com o par `[1,19]` e resposta `0x81` de 64 bytes com eco
  correto. **Com âncora independente:** a sprint UNIDADE-COR-01 já registrava,
  *sem saber a cor*, que `0x1111` era "o azul" e `0x0710` era "o roxo". Duas
  fontes que não se consultaram disseram a mesma coisa.
- **O rádio foi exercido, com autorização dela, e recusado.** Duas tentativas no
  `hidraw8` (o vermelho, identificado por `HID_UNIQ` e não pela cor do LED),
  uma com CRC-32 semente `0xA3` e outra `--sem-crc`: **`EIO` (errno 5),
  imediato, nas duas**, execução inteira em **0,249 s**.
- **Nenhum controle foi estragado.** Em todas as escritas, o feature `0x20`
  saiu idêntico byte a byte antes e depois (`20 4a 75 6c 20 20 34 20`), o
  `hardware_version` não mudou e 3 de 3 reports de entrada continuaram
  chegando.
- **O código da ordem congelada** (`JANELA_DE_ONDA_SEC = 0,5 s`,
  `JANELA_MESA_ESTAVEL_SEC = 4,0 s`, `_congelar_locked`, `_mesa_mexeu_locked`)
  está em `identity.py`, com 644 linhas de teste e 19 casos.
- **A fiação da máscara por jogador** (`registro_de_mascaras()`,
  `mascara_efetiva()`, `vpad_ficou_para_tras()`) está em `external_mask.py`,
  com 351 linhas de teste.
- **A cura do grab dobrado** (`reconciliar_grab_do_primario`, chamada pelo
  `lifecycle` a cada 2,0 s) está em `gamepad.py`.
- **A renomeação D-13** está feita: `cabo_de_onde_sei`, `radio_de_onde_sei`,
  `cabo_ate_onde_foi`, `radio_ate_onde_foi` no cabeçalho do CSV, em 11 arquivos,
  sem alias, com mordida provada em três pontos.
- **Os estudos:** a arqueologia da lightbar travada (565 linhas) e o par
  doente-contra-são no mesmo rádio, com os 306 atributos de sysfs comparados.

---

## 3. O que sobreviveu só no transcrito

Nove relatórios de recuperação foram escritos a partir dos `.jsonl` das sessões
mortas. Eles vivem em:

```
/mnt/Apate/Desenvolvimento/_recuperacao-2026-08-15/relatorios/
```

| relatório | o que ele guarda que não existe em outro lugar |
|---|---|
| `sessao-principal-3706fe35.md` | a narrativa das 8h45, e **seis falas dela** que ficaram fora do fio normal do transcrito (foram enfileiradas enquanto o assistente trabalhava) |
| `as-28-decisoes.md` | as respostas **literais** dela, que moram nos `toolUseResult` de sete rodadas de `AskUserQuestion` e são invisíveis a uma leitura ingênua do transcrito |
| `interrompido-D-15-cor-do-plastico.md` | as duas mordidas do instrumento da cor, exercidas à mão num terminal que morreu |
| `interrompido-D-30b-ordem-congelada.md` | as **cinco arrancadas** da ordem congelada, com o placar de cada uma |
| `interrompido-mascara-por-jogador.md` | o `morder.py` transcrito por inteiro e o veredito das sete mutações M1 a M7 <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore --> |
| `interrompido-D-13-D-14-colunas-do-mapa.md` | o censo antes e depois do rebaixamento, e o `renomeia.py` como especificação executável <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore --> |
| `interrompido-ja-tentado-e-derrubado.md` | a conferência do estudo da lightbar contra o instrumento |
| `madrugada-e700a182.md` | o script exato do ensaio da escada `0x32`/`0x39`, que só existia no transcrito |
| `evidencias-do-tmp.md` | a auditoria dos 71 arquivos do `/tmp` da sessão morta, com os diffs contra a árvore viva |
| `CONFRONTO-o-que-se-perdeu.md` | a auditoria final, item a item, com prioridade |

**E aqui está o risco estrutural que ninguém fechou:** essa pasta **não é
repositório git**. Os dez relatórios e a cópia inteira do scratchpad da sessão
morta existem numa **única** cópia, sem versionamento e sem remoto. Todo o
trabalho de recuperação está hoje tão frágil quanto estava a sessão que morreu.

### 3.1. Os três achados que a recuperação encontrou e que ninguém procurava

1. **O serial de fábrica dela, inteiro, num arquivo indexado para commit.**
   `scripts/ensaios/cor_do_plastico.py:373` — na docstring da função que serve
   justamente para **mascarar** o serial, como exemplo do "antes".
   `bash scripts/check_anonymity.sh` devolve *"OK: anonimato preservado"*
   porque a régua procura padrão de MAC, não de serial. É a mesma família do
   BURACO-DO-PORTÃO-01: **a régua foi aplicada numa forma só.**
2. **Os mesmos seriais em hexadecimal**, dentro dos relatórios de recuperação,
   num arquivo que afirma sobre si mesmo *"sem serial real, conferido por
   grep"*. O grep procurou a forma ASCII; o hexadecimal passou por baixo. Há
   também MAC real em três relatórios.
3. **O bruto do ensaio pareado é órfão.** A conclusão está versionada e o
   lastro dela não: os dois dumps de 306 atributos de sysfs (o vermelho são e o
   branco doente) e a captura HCI vivem só no scratchpad resgatado, e o estudo
   não os cita por nome — zero ocorrências. O `.btsnoop` ainda carrega o MAC do
   adaptador em binário *little-endian*, que **nenhum portão de texto pega**.

---

## 4. Os cinco agentes interrompidos

### 4.1. A cor do plástico (D-15) — parou nove segundos depois de começar a se corrigir

**O que ele fez.** Escreveu do zero `scripts/ensaios/cor_do_plastico.py` (1.090
linhas) — o **único** instrumento de `scripts/ensaios/` que escreve no
aparelho —, leu a cor dos dois DualSense do cabo, provou os controles sãos
antes e depois de cada escrita, e gerou 607 linhas de evidência bruta
versionada mais o CSV. Parou no rádio por decisão própria; a coordenação voltou
com a autorização dela e quatro condições, e ele estreou o envelope de FEATURE
por Bluetooth com uma trava `--exigir-mac` nova, provada mordendo.

**O achado que o resultado negativo produziu**, e que é útil: (1) o CRC **não**
é o discriminante — com e sem CRC, a mesma falha no mesmo ponto; (2) não é *"o
report não existe neste transporte"*, que daria `EPIPE`; (3) não é o rádio se
perdendo, porque o `REPORT_REQ_TIMEOUT` do BlueZ leva ~3 s e a execução inteira
levou 0,249 s; (4) sobra a hipótese **não medida**: recusa na camada
HIDP/L2CAP, pelo firmware ou pelo BlueZ.

**O que faltava.** Ele tinha acabado de anunciar *"o rádio diz não-exercido, e
isso agora é fato errado"*, fez a **primeira** das edições (a linha de Grau) e
foi cortado. **A sprint UNIDADE-COR-01 continua se contradizendo em seis
trechos**, todos conferidos linha a linha: o cabeçalho já diz "MEDIDO E
RECUSADO NO RÁDIO" e o corpo ainda diz que "no rádio, continua NÃO MEDIDO",
que "ninguém demonstrou", que houve uma "rodada seca", que resta uma "dúvida
honesta" sobre o CRC que a medição já respondeu, e a lista de "como ler a
falha, se vier" não tem a assinatura que **de fato veio**.

**Dado de graça que ele deixou para outra frente:** os dois controles de rádio
publicam o **mesmo** estado no sysfs — o vermelho são e o branco de lightbar
apagada, ambos com `brightness=255 multi_intensity=[0 255 0]`. O kernel acha
que a barra do travado está acesa e verde.

### 4.2. A ordem congelada (D-30(b)) — morreu dentro da suíte, e estava certo

**O que ele fez.** Implementou a decisão (b) dela por inteiro: o número do
jogador passa a sair da **ordem de conexão daquele momento** (fila de sessão
por ondas de 0,5 s), com o `rank` gravado sobrevivendo apenas como
**desempate**, e com **congelamento** quando a mesa fica 4,0 s sem ninguém
entrar nem sair. São 310 linhas novas em `identity.py`, duas docstrings
corrigidas em `coop.py` (nenhuma linha de código) e 644 linhas de teste.

**As duas constantes são medidas, não escolhidas.** `JANELA_DE_ONDA_SEC = 0,5 s`
fica espremida entre um teto e um piso: o teto é o tick lento do `lifecycle` a
cada 2,0 s; o piso é a rajada de uma olhada, que é memória pura.
`JANELA_MESA_ESTAVEL_SEC = 4,0 s` é número que esta casa já mediu duas vezes —
o `VOLATILE_ABSENCE_LIMIT` do MODO-01 e a repintura da Steam.

**O achado mais forte da sessão** veio de arrancar a cura: tirar a onda quebrou
**quatro testes de R-23 que já existiam**, além dos dele. O desempate pelo
gravado não é enfeite — é o que sustenta a decisão anterior.

**O que faltava.** Só o relatório e o commit. Ele estava com ruff, mypy e 1.059
testes filtrados verdes quando o comando `pytest -q tests/` foi cortado aos
22 s. A sprint ORDEM-DE-CHEGADA-01 ainda marca a E2 como `PLANO` e ainda traz o
marcador *"arquivo a CRIAR por esta entrega, ainda não existe"* sobre um
arquivo que existe.

### 4.3. A máscara por jogador — a cura ligada, e o último degrau deixado de fora de propósito

**O que ele fez.** Reescreveu no `profiles/schema.py` a frase dela de 10/08
(*"`mode` e a máscara do gamepad são da SESSÃO"*) para valer só para o `mode`,
com nota datada; ligou ao caminho de produção o `ExternalMaskRegistry`, que
existia desde 07/08 e **nunca tinha chamador** — o defeito mais caro desta casa,
a cura escrita e nunca ligada; e passou `identity=` aos dois backends de vpad.
Separou *"divergência escolhida"* de *"flavor que ficou para trás"* trocando o
alvo da comparação de um valor global por uma função do aparelho, o que
preserva a cura da SPRINT-GAME-RUMBLE-01.

**O portão da casa confirmou sozinho:** às 17:27:24 UTC ele reprovou com
*"`_SEM_CAMINHO_HOJE` declara estes símbolos como sem caminho, e ALGO em
produção já os alcança"*. A lápide foi trocada, não apagada — a nova descreve a
receita exata do que falta no co-op.

**Sete mutações, sete reprovações, duas vezes.** M1 a M7, uma cura arrancada por
vez: 6, 2, 2, 3, 1, 2 e 1 testes caindo. Nenhuma passou.

**O que faltava.** A suíte inteira (recusada às 17:48:09) e o commit. E o
**último degrau, não dado de propósito**: `make_virtual_pad` ainda não aceita
`identity`, e os dois chamadores não passam identidade — logo **o produto se
comporta exatamente como antes**, o que está testado e vigiado por um
`xfail(strict=True)` que reprova no dia em que o degrau chegar. Do lado da
escrita, a rota IPC continua só conhecendo a máscara da sessão: sem ela, não há
como ela escolher a máscara de um jogador pela interface.

### 4.4. A arqueologia da lightbar travada — 565 linhas com conclusão, e três números errados

**O que ele fez.** Escavou o repositório inteiro atrás de cada hipótese já
proposta para a lightbar travada por rádio: quem a derrubou, com que evidência,
e se foi **refutada** ou apenas ficou **sem prova**. Leu sete sprints (2.626
linhas), as duas canônicas e os comentários do `src/`, e produziu um documento
único de 565 linhas em oito seções. Nada de código, nenhum controle tocado — a
frente era só leitura, por regra.

**O que ele impediu:** que a mesma hipótese fosse proposta pela quinta vez. O
candidato *"`common[41] = LIGHT_OUT` como cura"* já é o C6, refutado nos três
pontos em 03/08 — inclusive porque `LIGHT_OUT` significa *"fade light out"*, ou
seja, **a suposta cura apaga**.

**O que ele achou e ninguém tinha cruzado:** das quatro razões que criaram e
mantêm a supressão incondicional de hidraw por Bluetooth, **três caducaram com
data** e a quarta (`LIGHTBAR-BT-KEEPALIVE-01`) tem catorze referências em
código, documentos e testes, **zero** documentos de sprint e **nenhum** ensaio
no caderno. E o item mais quente: os dois defeitos curados na manhã do mesmo
dia produzem a assinatura literal deste defeito — *"o firmware descarta e o log
diz escrito"*.

**O que faltava.** Os quatro portões de idioma, disparados às 14:47 e recusados
às 14:48:09 (rodados depois: passam), e **três números errados**. Onde o
documento diz "treze suspeitos, sete inconclusivo", o instrumento diz
**quinze**: 3 e-a-causa, 3 confuso, 9 inconclusivo, **zero inocentados**.

### 4.5. As colunas do mapa (D-13 e D-14) — a interrupção que não houve

**Correção de fato, e ela importa:** este agente **não foi interrompido**.
Entregou o relatório final às **14:39**, onze minutos antes de a sessão morrer.
O `stoppedByUser` do arquivo de metadados é o encerramento da sessão-mãe, não
uma interrupção dele. Quem contar cinco interrompidos está contando este
indevidamente.

**O que ele fez.** Censo antes de tocar em nada — 19 arquivos nomeavam as
colunas antigas, 11 eram leitores ou escritores vivos —, e **o censo pegou o
que um grep óbvio deixaria passar**: dois leitores em `scripts/gerar-mapa.py`
usam o sufixo **sem** o prefixo (`qualquer(lin, "confianca", …)`). Se tivessem
escapado, o `specs.html` seria gerado sem reclamar, mostrando um traço em toda
a coluna. Renomeou nos 11 arquivos, rebaixou 14 células com nota datada,
atualizou 14 células de prosa e provou a mordida em três pontos.

**O efeito, medido:** `medido` caiu de **112 para 98**; as afirmações fortes, de
**51 para 46**. Nenhum `ate_onde_foi` foi mexido — as contagens de `MONTOU`,
`SAIU NO FIO` e `O APARELHO OBEDECEU` são idênticas antes e depois.

**O buraco que ficou:** `scripts/migrar-mapa-v2.py` escreve o CSV **inteiro** a
partir do cabeçalho dele, e **nenhum teste** o compara com o cabeçalho real.
Uma execução acidental reverte a renomeação sem uma linha de erro.

### 4.6. O sexto, que fechou

O agente do **grab dobrado (D-29)** entregou de ponta a ponta e não foi parado:
causa achada (*"failed" era estado absorvente porque só o secundário tinha
retry*), cura em `reconciliar_grab_do_primario` chamada pelo poll a cada 2 s,
nove mordidas arrancadas e devolvidas, sprint escrita. É a única frente da leva
fechada por inteiro.

---

## 5. O que exige a palavra dela

Nada abaixo é dúvida técnica. São escolhas de produto, e a casa não as toma.

1. **Commitar a leva.** Trinta e três arquivos, 5.908 inserções, todos os
   portões verdes. A decisão de commitar é dela, e a leva mistura territórios
   de seis agentes: ou se separa por frente, ou se fecha de uma vez.
   **A armadilha, medida:** cinco arquivos têm mudança **fora** do índice, feita
   por sessão posterior. Um `git commit` que leve só o índice devolve ao
   vermelho o portão de citações de linha — que foi exatamente o portão que
   matou a suíte dos agentes. O caminho é `git add -A` **primeiro**.
2. **O `EIO` do rádio fecha a D-15, ou há um terceiro envelope a tentar?** O
   orçamento era de duas tentativas e as duas foram gastas. A terceira exigiria
   instrumentar o canal com `btmon` para separar quem recusou — o firmware ou o
   BlueZ.
3. **A supressão incondicional de hidraw por Bluetooth.** O caminho que
   **comprovadamente funciona** — o branco obedeceu de madrugada a três reports
   diferentes, com o daemon parado e escrita hidraw crua — é exatamente o que o
   produto se proíbe de usar. Rever isso é decisão dela, e é o próximo passo da
   frente da lightbar.
4. **O portão de constante órfã**, prometido na mensagem do commit `9281cf0` e
   nunca escrito. Fechá-lo exige rever a decisão medida de 12/08, que exclui
   constantes de módulo **por desenho** — é por isso que o `BLOCO_SPEAKER =
   0x13` escapa há vinte dias.
5. **As sete decisões de interface** (D-16 a D-22) não têm uma linha de código
   nem agente disparado. É o maior bloco parado da leva, e por PROVA-DE-TELA-01
   nada disso fecha sem o olho dela.
6. **As duas ondas perecíveis** que ela autorizou às 13:46 e que ninguém
   executou, porque a emergência da lightbar comeu a janela: **D-31** (a série
   inteira da escada) e **D-32** (ler a família `0xF0`-`0xF7`, só leitura).
   As duas exigem a mesa de pé **e ela presente**.
7. **O `.btsnoop` entra no git?** Ele é o lastro binário do ensaio pareado e
   carrega o MAC do adaptador em *little-endian*, forma que nenhum portão de
   texto alcança.

---

## 6. A ordem de execução para a próxima leva

A ordem não é de importância — é de **dependência e de risco**. Os três
primeiros itens são de contenção: fazem o dia parar de poder ser perdido.

### Antes de qualquer outra coisa

| # | o quê | por quê agora |
|---|---|---|
| 1 | Tirar o serial real de `scripts/ensaios/cor_do_plastico.py:373` (exemplo forjado, como já foi feito na docstring vizinha) | está **indexado para commit**, e o portão passa verde |
| 2 | Mascarar os seriais em hexadecimal e os três MAC dos relatórios de recuperação | a pasta será versionada, e hoje ela mente sobre si mesma |
| 3 | `git add -A`, reconferir `validar-citacoes-de-linha.py --all`, e então commitar | um `reset --hard` apaga 5.908 linhas |
| 4 | Versionar `_recuperacao-2026-08-15/`, ou movê-la para um repositório com remoto | dez relatórios em cópia única |

### Depois, o que é portão e está mentindo

| # | o quê | por quê |
|---|---|---|
| 5 | Corrigir a linha `identidade.cor_do_aparelho` de `docs/data/mapa-controles.csv` | **é a maior lacuna**: o mapa é portão, não documentação, e as três afirmações da ressalva são falsas hoje — ela autorizou, foi enviado, e o aparelho obedeceu por cabo |
| 6 | Substituir os seis trechos contraditórios de UNIDADE-COR-01 | pela regra de 11/08 isto é **fato errado**, não decisão medida: substitui-se, não se preserva com data |
| 7 | Ensinar o `check_anonymity.sh` a reconhecer a **forma** do serial | senão a terceira vez acontece |
| 8 | Corrigir os cinco números do estudo da lightbar (treze para quinze, sete para nove) | o instrumento é a régua, e ele discorda do texto |

Para a célula do mapa, o conteúdo já está apurado: `cabo_de_onde_sei` para
`medido`; `cabo_ate_onde_foi` para `O APARELHO OBEDECEU`; a evidência ganha o
ensaio E7 com os dois códigos e a âncora do `hardware_version`; `radio_aceita`
para `não`; `radio_ate_onde_foi` para `MONTOU`, porque o byte não saiu no fio —
o `ioctl` devolveu `EIO`; e a ressalva do rádio recebe as duas tentativas, o
`EIO` imediato, os 0,249 s, o descarte de `EPIPE` e de timeout, e a hipótese
HIDP/L2CAP. Depois, `check_paridade_transporte.py` e `gerar-mapa.py`.

### Depois, o que faz a próxima sessão achar o caminho

| # | o quê |
|---|---|
| 9 | Escrever o índice da tarde. **Cinco documentos novos não são referenciados por índice nenhum**, e o CLAUDE.md manda a próxima sessão começar pelo índice mais recente — que é o da madrugada, e não conhece a tarde |
| 10 | Atualizar `ONDE-PARAMOS`: as 26 respostas, o restauro de bonds provado na máquina, e a frente da lightbar |
| 11 | Corrigir o índice da madrugada, que diz "NÃO commitadas" sobre trabalho commitado minutos depois em `7c3a0c7` e `9441678` |
| 12 | Marcar a E2 de ORDEM-DE-CHEGADA-01 como entregue; trocar o Status de MASCARA-POR-JOGADOR-01, que ainda diz "PARADA, esperando ELA" quando ela já respondeu e o código está no índice |

### Depois, a dívida técnica com dono claro

| # | o quê |
|---|---|
| 13 | Teste unitário para as travas de `cor_do_plastico.py` — as mordidas foram exercidas só à mão, num terminal que morreu, e cabem num arquivo **sem hardware nenhum** |
| 14 | Teste que compare o cabeçalho do `migrar-mapa-v2.py` com o cabeçalho real do CSV |
| 15 | Versionar os brutos órfãos do ensaio pareado e a segunda corrida do E2 (o par é que é a medição: o mesmo vpad mede 0,30 Hz numa e 26,00 Hz na outra) |
| 16 | Registrar o veredito das sete mutações M1 a M7 na sprint da máscara, e guardar o `morder.py` num lugar durável <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore --> |
| 17 | Substituir as três frases falsas ainda vivas no `src/` — a medição de 08/08 falsificada em 11/08. Importa porque, na própria sessão morta, **outra frente leu essa frase e a tratou como evidência**. O molde pronto está em `cli/cmd_lightbar_reset.py` |
| 18 | Acrescentar os dois OUI que faltam ao portão de anonimato: dois dos quatro controles da mesa não estão na lista, e 17 documentos já os citam mascarados à mão |
| 19 | Renomear `backend_COM_CURA.py` no scratchpad resgatado — **o nome mente**, é o estado ANTES da cura, e quem confiar nele reverte o commit `2877988` achando que o aplica <!-- ref-externa: vive no scratchpad resgatado da sessão morta, fora desta árvore --> |

### Por último, o que é baixo risco e alta memória

Registrar o censo real do rebaixamento (112 para 98, 51 para 46) onde a
previsão de 14/08 está escrita; trocar `cabo_confianca` pelos nomes novos nos
três pontos de `scripts/ensaios/`; substituir o fato errado da V-B, que ainda
chama a arte dos SVG de risco de licença depois de ela ter derrubado a
pergunta; levar o critério de release dela para a página que os portões
consultam, porque hoje ele mora numa única página; e escrever a entrada do
CHANGELOG para D-13 e D-14.

---

## 7. A lição que esta queda cobrou

Três coisas se repetiram, e nenhuma é novidade nesta casa:

1. **Trabalho verde e não commitado é trabalho em risco.** A leva passou em
   treze portões, inclusive na suíte inteira, e mesmo assim ficou quarenta
   minutos a um `reset --hard` de sumir. Portão verde não é durabilidade.
2. **A régua aplicada numa forma só deixa passar a mesma coisa noutra forma.**
   O anonimato foi conferido por MAC e o serial passou; foi conferido em ASCII e
   o hexadecimal passou. É o BURACO-DO-PORTÃO-01 pela terceira vez.
3. **Uma página que se contradiz é pior que uma página vazia.** UNIDADE-COR-01
   hoje afirma e nega o mesmo fato em seis lugares, e quem a ler vai escolher
   pela metade que leu primeiro. O agente foi cortado nove segundos depois de
   começar a consertar isso — e nove segundos foi tudo o que separou o
   documento certo do documento que mente.
