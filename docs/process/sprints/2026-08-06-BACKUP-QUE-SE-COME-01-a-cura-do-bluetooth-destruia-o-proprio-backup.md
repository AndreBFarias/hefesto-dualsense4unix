# BACKUP-QUE-SE-COME-01 — a cura do Bluetooth destruía o próprio backup

- **Achado em:** 25/07/2026 os dois primeiros (bancada, lendo a série de
  backups do `/etc/bluetooth` dela); 06/08/2026 os três últimos, por
  **verificação adversarial** sobre as curas do próprio dia — segunda, terceira
  e quarta rodadas. **Nenhum destes veio de queixa dela**, e é isso que os torna
  caros: o estrago só apareceria depois de já ter acontecido
- **Estado:** **CURA APLICADA** e commitada em `53f6d8b` (06/08/2026, 22:02).
  Esta sprint é **materialização atrasada**: o código está em
  `scripts/bluez_config.sh`, os testes que mordem estão em
  `tests/unit/test_bluez_config_sh.py` (seções 6, 13 e 14), e o portão de
  empacotamento em `scripts/check_packaging_parity.sh`. **O que faltava era o
  documento** — os códigos `BUG-INSTALL-MAIN-CONF-BACKUP-INFINITO-01` e
  `BUG-INSTALL-MAIN-CONF-CRESCE-01` existem desde 25/07 e nunca tiveram página
- **Gravidade:** **ALTA**. Não pelo espaço em disco: os backups do
  `main.conf` são o **único instrumento de medição** que este projeto tem sobre
  o arquivo de rádio dela, e duas investigações abertas dependem deles. Um
  defeito que come backup apaga a prova de outros defeitos
- **Causa-raiz:** **MEDIDA** nos três de 06/08 (reprodução em bancada antes da
  cura, mordidas arrancadas e vistas vermelhas); **MEDIDA** também nos dois de
  25/07, por série temporal nos próprios backups
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
    — é a leva que criou o `scripts/bluez_config.sh` e registra o colapso
    `404 linhas -> 3 linhas` como **suspeita em aberto**. Esta sprint é sobre o
    que quase apagou a evidência desse colapso, e traz a **nota datada** do que
    caducou lá;
  - [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
    — mesma classe noutra boca: lá o **doctor** afirmava sem medir, aqui é o
    **instalador** que afirmava sem medir ("nenhum é apagado automaticamente");
  - [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md)
    — o outro salva-vidas desta casa (os bonds), e a mesma pergunta: a cópia de
    segurança serve no dia em que for preciso?

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## Por que backup, aqui, não é higiene: é o instrumento

O `/etc/bluetooth/main.conf` dela é conffile do dpkg, e a única coisa neste
projeto que o reescreve é uma execução do instalador. Cada reescrita deixa um
`main.conf.bak.hefesto-<carimbo>` ao lado. Essa série é o **único registro
histórico** que existe do arquivo.

**MEDIDO em 06/08/2026** (a contagem está na RADIO-ABERTO-01): **37** arquivos
`main.conf.bak.hefesto-*` em `/etc/bluetooth`, **23 do install e 14 do
uninstall**, somando **272 KB** — mais um `main.conf.bak.` de outra ferramenta,
que não é nosso.

Dessa série saíram, e só dela:

1. a medição do `BUG-INSTALL-MAIN-CONF-CRESCE-01` — o arquivo crescendo uma
   linha por execução;
2. os **dois pontos do colapso** que a RADIO-ABERTO-01 registra como suspeita
   **sem cura**: `main.conf.bak.hefesto-1784672963` (404 linhas, 14797 bytes,
   21/07 19:29) e `main.conf.bak.hefesto-1784694261` (3 linhas, 59 bytes, 22/07
   01:24). O `main.conf` dela **perdeu o template do upstream** em algum
   momento daquela madrugada, e ninguém sabe por quê.

Apagar backup, nesta casa, não é liberar disco. É apagar a única medição do
único estrago deste projeto ainda sem explicação. **A regra é "não se apaga
decisão medida"**, e cento e poucos quilobytes não compram exceção.

---

## Os dois códigos de 25/07 — a dívida que abre esta sprint

Nasceram no `install.sh`, no commit `fc9a9f6` (25/07/2026), quando a lógica do
BlueZ ainda morava dentro do instalador. Hoje vivem em
`scripts/bluez_config.sh`, comentados em `_despir_main_conf` e em
`_gravar_se_mudou`. **Nunca tiveram documento.**

### `BUG-INSTALL-MAIN-CONF-CRESCE-01` — o arquivo crescia por execução

**Grau: MEDIDO.**

As sentinelas `# >>> hefesto bluetooth >>>` delimitam o **bloco**. A linha em
branco separadora que o instalador apensava antes do bloco ficava **fora**
delas — então a remoção não a levava, e a próxima escrita apensava outra. O
bloco descia uma linha por execução, para sempre.

Duas medições, e as duas na mesma série de backups:

- em 25/07, no commit que curou: **10 linhas em branco acumuladas** entre o
  `[General]` do upstream e a sentinela;
- na releitura de 06/08, escrita hoje no comentário de `_despir_main_conf`:
  **de 27 a 34 linhas em oito execuções**.

A cura é a regra `(c)` do `awk`: guardar as linhas em branco e só imprimi-las
quando vem conteúdo depois. Isso **preserva os brancos internos e descarta os
do fim** — e por isso o `remover` **não** devolve o arquivo byte a byte quando
ele terminava em linha vazia. Essa exceção não foi escondida: está **declarada**
no cabeçalho da função e fixada por
`test_remover_declara_a_excecao_das_linhas_em_branco_do_fim`, para que ninguém
a descubra por acidente e "conserte" a idempotência sem saber o que está
trocando.

### `BUG-INSTALL-MAIN-CONF-BACKUP-INFINITO-01` — backup do que não mudou

**Grau: MEDIDO.**

O backup era feito **antes** de o script saber se havia mudança. Rodar o
instalador duas vezes seguidas, sem nada para alterar, deixava mais um arquivo
no `/etc/bluetooth`. Em 25/07 havia **22** acumulados por esse caminho.

A cura é uma linha, e é a primeira coisa que `_gravar_se_mudou` faz:

```
if _r cmp -s "${candidato}" "${MAIN_CONF}"; then
    _diz "main.conf já está como queremos, byte a byte — nada a reescrever (sem backup novo)"
```

Comparar primeiro é o que torna o no-op **honesto**. Portão:
`test_rodar_duas_vezes_nao_gera_backup_novo` — inverta o `cmp` (backup antes de
comparar) e ele fica vermelho.

**O que a cura NÃO promete, e é bom dizer:** ela não impede a série de crescer.
Ela impede a série de crescer **sem motivo**. Cada mudança real continua
deixando um backup, e deve mesmo. **Grau: SUSPEITA COM MECANISMO** para a
leitura de que a cura segurou na máquina dela — as duas contagens são MEDIDAS
(22 pelo install em 25/07; 23 pelo install em 06/08), mas ninguém auditou o
intervalo arquivo por arquivo.

---

## Defeito A — o nome do backup tinha resolução de um segundo

**Gravidade: ALTA. Grau: MEDIDO** (reprodução em bancada antes da cura;
mordida arrancada, vista vermelha, devolvida).

O nome saía assim:

```
main.conf.bak.hefesto-${rotulo}$(date +%s)
```

Resolução de **um segundo**, com um `cp` **sem `-n`**, **sem** teste de `-e` e
**sem** `mktemp`. Duas gravações do mesmo rótulo dentro do mesmo segundo faziam
a segunda **sobrescrever** o backup da primeira.

Três coisas tornam isso pior do que parece:

1. **Acontece dentro do `aplicar`/`remover`, sem gesto dela.** A sequência
   `aplicar; remover; aplicar` é a que o próprio doctor sugere, e ela roda em
   muito menos de um segundo — os dois `aplicar` compartilham o rótulo vazio.
2. **O destruído é sempre o de maior valor.** Quem morre é o backup do estado
   **imediatamente anterior**, que é justamente o que alguém iria querer para
   entender o que acabou de acontecer.
3. **Nada detectava.** Um arquivo morre, outro nasce, e a **contagem não muda**
   — então o `_resumo_backups` não via nada e a mesma execução imprimia
   *"nenhum é apagado automaticamente"*.

A reprodução, letra por letra: `aplicar` sobre o estado A, edição para o estado
B, `aplicar` de novo dentro do mesmo segundo. Antes da cura: **um** backup no
disco, com o estado B. O estado A dela tinha ido embora.

### A cura: mecanismo, não sorte

`mktemp` com os `X` no **fim** — que é onde o `mktemp` os aceita:

```
backup="$(_r mktemp "${origem}.bak.hefesto-${rotulo}$(date +%s)-XXXXXX")"
```

O nome vem do kernel e a criação é `O_EXCL`: não há janela entre "escolher o
nome" e "criar o arquivo". Não depende de o relógio ter resolução melhor, nem
de o `cp` ter a flag certa.

Na mesma função entraram duas garantias irmãs, ambas **MEDIDAS** em 06/08:

- **backup parcial não é backup.** Um `cp` que morre no meio deixava **118
  bytes cortados dentro do bloco**, sem limpeza e sem uma palavra — e o
  `verificar` os contava como legítimos. A assimetria estava no corpo do
  `_gravar_se_mudou`: o caminho do temporário tinha `rm -f`, o do backup não.
  Hoje o backup só existe se o `cp` sair 0 **e** o `cmp` confirmar byte a byte;
  o que não passar é **apagado e dito**, e o original **não é tocado**;
- **o modo é o do original.** O `mktemp` cria com 600; um backup do conffile
  dela tem de ter o modo **dele**, nem mais aberto nem mais fechado
  (`chmod --reference`).

**Mordidas** (`tests/unit/test_bluez_config_sh.py`, seções 13 e 14):

| arranque isto | fica vermelho |
|---|---|
| o `mktemp`, devolvendo `...hefesto-${rotulo}$(date +%s)` | `test_duas_gravacoes_no_mesmo_segundo_nao_comem_o_backup_anterior` e `test_aplicar_e_remover_seguidos_nao_colidem` |
| a limpeza do backup incompleto | `test_backup_parcial_e_apagado_e_o_main_conf_nao_e_tocado` |
| **só** a metade do `cmp` do `_copia_de_seguranca` | `test_backup_que_mente_ter_copiado_e_pego_pelo_cmp` |

A última linha da tabela existe por uma **retratação registrada**, e ela vale
mais que o teste: a rodada anterior afirmou que arrancar o `cmp` deixava o
teste do backup parcial vermelho. **Não deixa.** Naquele teste o `cp` sai 1, o
`||` curto-circuita e o `cmp` **nunca é avaliado** — com o `cmp` arrancado a
bancada inteira segue verde. Mordida afirmada e não reproduzida é exatamente o
que a regra da casa proíbe, e a cura foi **escrever a bancada que faltava** (um
`cp` que corta o arquivo e mente saindo 0), não apagar a frase.

---

## Defeito B — a poda automática apagaria 27 dos 37 backups dela

**Gravidade: ALTA. Grau: MEDIDO** (simulação só-leitura do pipeline exato
contra o `/etc/bluetooth` dela).

A primeira versão do `scripts/bluez_config.sh` podava dentro do `aplicar` e do
`remover`, guardando os 10 mais recentes por mtime. A simulação disse o que a
**primeira** execução faria na máquina dela:

| arquivo | tamanho | quando | seria apagado? |
|---|---|---|---|
| `main.conf.bak.hefesto-1784672963` | 404 linhas, 14797 bytes | 21/07 19:29 | **sim** |
| `main.conf.bak.hefesto-1784694261` | 3 linhas, 59 bytes | 22/07 01:24 | **sim** |

**27 dos 37**, e entre eles os dois pontos do colapso. O mecanismo é simples e
é o problema de toda retenção por mtime: ela **descarta primeiro o que tem mais
valor**. Os 10 que ficariam são todos pós-colapso, de 11 a 1395 bytes. E o
gatilho seria o conselho da própria ferramenta — o doctor manda *"rode
./install.sh"*.

### A cura, em quatro decisões

1. **A poda deixou de ser automática.** `aplicar` e `remover` só **contam e
   dizem**. Apagar virou o subcomando explícito `bash scripts/bluez_config.sh
   podar`.
2. **`podar` simula por padrão** (`--dry-run`); apagar de verdade exige
   `--aplicar`.
3. **O mais antigo nunca sai** — é o estado mais próximo do pré-hefesto, e na
   máquina dela é literalmente o único arquivo que ainda tem o template do
   upstream.
4. **Nenhum estado some do disco.** De cada conteúdo distinto (por `cksum`)
   fica sempre ao menos uma cópia, **mesmo que todas as cópias dele estejam
   fora da retenção**. A que fica é a **mais antiga** daquele conteúdo: entre
   bytes iguais, a de mtime menor é a que diz **quando aquele estado apareceu**,
   e é essa que interessa a quem for explicar o colapso.
5. **Anunciar remoção que não aconteceu é mentir sobre o disco dela.** O
   desenho anterior tinha um `|| true` que engolia a falha do `rm` e imprimia a
   mesma frase. Hoje cada arquivo é conferido **depois** do `rm`.

### A correção da correção: a promessa era de ESTADO e a proteção era de ARQUIVO

**Grau: MEDIDO. Correção de decisão gravada** — a regra anterior está descrita
na RADIO-ABERTO-01 e **caducou**; ver a nota datada no fim desta página.

A regra da terceira rodada era *"nenhum **outro** backup tem os mesmos
bytes"*. Isso protege só o conteúdo que aparece **uma vez**. Com um conteúdo
repetido em N cópias e **todas** fora da retenção, as N saíam juntas — e aquele
estado do `main.conf` dela sumia do disco por completo, enquanto a última linha
impressa dizia *"os de conteúdo único ficam sempre"*, que se lê como promessa
de **estado**.

Reproduzido com **9 backups em 3 estados de 3 cópias cada, retenção 1**: o
estado do meio perdia as três. Nenhuma das suas cópias é a mais nova (a
retenção salva o estado de cima) nem a mais antiga (essa salva o de baixo).

O teste que existia **não mordia esse cenário** — usava 35 arquivos
**idênticos**, em que a regra velha e a nova dão o mesmo resultado. É a
armadilha clássica: um teste que passa nas duas versões não separa nenhuma
delas. Hoje morde `test_podar_nunca_faz_um_estado_sumir_do_disco`, e ele
verifica as duas metades — que nenhum estado sumiu **e** que a poda **ainda
poda** (das 9 cópias saem as 6 que têm irmã idêntica sobrevivendo).

**Mordidas** (seção 6):

| arranque isto | fica vermelho |
|---|---|
| a chamada de poda dentro do `aplicar`/`remover` | `test_aplicar_nao_apaga_backup_nenhum`, `test_remover_nao_apaga_backup_nenhum` |
| a proteção do mais antigo | `test_podar_nunca_apaga_o_mais_antigo` |
| a proteção por conteúdo | `test_podar_nunca_apaga_backup_de_conteudo_unico` |
| a proteção por **estado** (voltando à regra por arquivo) | `test_podar_nunca_faz_um_estado_sumir_do_disco` |
| o `--dry-run` como padrão | `test_podar_por_padrao_so_simula` |
| o `\|\| true` que engolia a falha do `rm` | `test_podar_nao_anuncia_remocao_que_nao_aconteceu` |

E há um portão **fora** da suíte, em `scripts/check_packaging_parity.sh`: ele
roda o `aplicar` de verdade contra uma raiz falsa povoada com 12 backups e
confere **no disco** que nenhum sumiu. O comentário dele registra as duas
armadilhas que o desenho anterior caiu:

- ele era `grep -qF '_podar_backups'`, o **nome literal** da função removida —
  renomear a função e devolver a chamada passava batido (MEDIDO por mutação);
- os 12 backups têm conteúdo **idêntico de propósito**: com conteúdos
  diferentes a regra "conteúdo único nunca sai" protegeria todos, o `_podar`
  não teria candidato e o portão passaria **verde com a poda automática de
  volta**.

---

## Defeito C — a frase do resumo era mentira, de dois jeitos

**Gravidade: MÉDIA no efeito, ALTA no que ela desarma. Grau: MEDIDO.**

A frase é esta, e sai em toda execução do `aplicar` e do `remover`:

```
backups do hefesto em /etc/bluetooth: 37 arquivo(s), 272000 byte(s)
  — nenhum é apagado automaticamente
```

Não é preciosismo de texto. **É a frase que impede quem lê de desconfiar** — e
é a mesma frase que autoriza mexer no conffile.

**Mentira 1 — o número não mudava quando um backup morria.** Com a colisão do
defeito A, um arquivo morria e outro nascia no mesmo instante: a contagem ficava
igual. A execução que **apagava** um backup imprimia *"nenhum é apagado
automaticamente"* na mesma tela. Portão:
`test_a_frase_do_resumo_deixou_de_ser_mentira`.

**Mentira 2 — o número somava cadáveres.** O `_copia_de_seguranca` cria o
arquivo com `mktemp` (nasce com **zero byte**) e só depois o preenche com `cp`.
Um SIGKILL entre os dois deixa no disco um `main.conf.bak.hefesto-...` de 0
byte — e SIGKILL **não tem trap**, então a limpeza que cobre INT/TERM/HUP não
roda. O `verificar` o contava em `backups-hefesto:` como legítimo e o
`_resumo_backups` o somava na frase: lia-se "37 backups" onde havia 36 e um
cadáver. **Backup vazio com cara de legítimo é o mesmo defeito do backup pela
metade, um passo antes.**

A cura tem duas metades, e a segunda é a que importa: o vazio **sai da conta**
(`! -empty` no `_lista_backups`) **e passa a ser dito** — em `backups-suspeitos:`
no `verificar`, nomeado um a um, e num `ATENÇÃO` no `aplicar`. **Sumir da frase
sem uma palavra seria trocar um número errado por silêncio**, que é a mesma
classe de defeito noutra roupa.

Ele **não é apagado**: um arquivo de 0 byte também é a marca de uma execução
que morreu, e a regra vale igual para os temporários órfãos
(`.main.conf.hefesto-novo.*`, reportados em `temporarios-orfaos:`). **Reportar é
obrigação; apagar não fazemos.**

**Mordidas:** `test_backup_de_zero_byte_nao_conta_como_backup`,
`test_o_resumo_do_aplicar_nao_soma_backup_vazio` (tire o `! -empty` e os dois
ficam vermelhos), `test_a_poda_nao_alcanca_backup_vazio`.

---

## O que a cura declara que NÃO faz

Cada um destes é limite escrito no código, não esquecimento:

- **`rename(2)` dá atomicidade, não durabilidade.** A troca do `main.conf` passa
  por `mv` de um temporário do mesmo diretório — ou o arquivo antigo inteiro, ou
  o novo inteiro, nunca uma mistura. Sem `fsync`, uma queda de energia logo
  depois do `mv` pode deixar no disco o **antigo**. Não pomos `fsync` de
  propósito: a mudança só vale no próximo start do `bluetoothd`, e um boot
  depois de queda de energia re-executaria o install. **A frase anterior dizia
  "queda de energia" e era falsa; foi corrigida em 06/08.**
- **Link simbólico.** Se o `main.conf` for symlink, o `mv -f` o substitui por
  arquivo comum e o alvo fica para trás intocado. **Grau: SUSPEITA COM
  MECANISMO** — não se aplica à máquina dela (**MEDIDO**: é arquivo comum).
- **Os backups de drop-in não entram na conta.** Ficam ao lado do drop-in, em
  `main.conf.d/`, com nome que **não** termina em `.conf` — um BlueZ que leia
  aquele diretório lê `*.conf`, e backup que virasse config seria trocar um
  defeito por outro. Pela mesma razão a poda do `main.conf` **não os alcança**.

---

## Nota datada — 06/08/2026: o que caducou na RADIO-ABERTO-01

A nota *"a poda automática de backup foi RETIRADA"*, na
[RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md),
descreve a proteção assim:

> **conteúdo único nunca sai** — se nenhum outro backup tem os mesmos bytes,
> aquele arquivo é a única cópia daquele estado.

**Essa é a regra por ARQUIVO, e ela caducou no mesmo dia**, pelo defeito B
acima: um conteúdo repetido em três cópias não era "único" nenhuma vez, e o
estado inteiro podia sumir. A regra em vigor é **por ESTADO** — de cada
conteúdo distinto fica ao menos uma cópia, e é a **mais antiga** dele. A frase
lá **não foi apagada**: fica como registro do que se pensou primeiro, e esta
nota é o que diz o que a substituiu. O resto daquela nota (poda explícita,
`--dry-run` por padrão, o mais antigo nunca sai, `HEFESTO_BT_BACKUPS_MANTER` só
consultada pelo `podar`) continua valendo palavra por palavra.

---

## O que fica ABERTO

- **O colapso `404 linhas -> 3 linhas` continua sem explicação.** Esta sprint
  protegeu a evidência; não a leu. Sabe-se que aconteceu na janela de um backup
  com prefixo de outra ferramenta, **não** numa execução do `install.sh`, e que
  o `main.conf.dpkg-dist` íntegro (384 linhas) está ao lado. **Grau: SUSPEITA
  COM MECANISMO** — a série está medida, a causa não.
- **O `podar` nunca foi rodado na máquina dela, nem em `--dry-run`.** Não se
  sabe quantos dos 37 ele proporia remover com a retenção padrão de 10 e a
  proteção por estado. **Grau: SEM PROVA.** O gesto é dela, e é barato: o
  padrão só simula.
- **O doctor não enxerga backup vazio nem temporário órfão.** O `verificar`
  imprime `backups-suspeitos:` e `temporarios-orfaos:`, mas
  `grep -n "backups-suspeitos\|temporario-orfao" scripts/doctor.sh` retorna
  **zero**. Quem só roda o doctor — que é o caminho recomendado — nunca vê
  esses arquivos. **Grau: MEDIDO** (o `grep` no repositório) para a ausência;
  **SEM PROVA** de que exista algum desses arquivos no `/etc` dela hoje.
- **Backup de drop-in não é contado, reportado nem podado por ninguém.** É
  decisão declarada (a poda do `main.conf` não pode alcançá-lo), mas o efeito
  colateral é que ele acumula em silêncio se ela editar o drop-in mais de uma
  vez. **Grau: SUSPEITA COM MECANISMO** — o caminho de código fecha, nenhum
  acúmulo foi observado.
- **A leitura de que o `cmp` do `BACKUP-INFINITO-01` segurou** entre 25/07 e
  06/08 se apoia em duas contagens (22 e 23 pelo install), não numa auditoria
  arquivo por arquivo. **Grau: SUSPEITA COM MECANISMO.**
- **`_lista_backups` depende do `-printf` do `find` do GNU.** Fora do
  coreutils/findutils GNU a listagem sai vazia e a poda vira no-op silencioso.
  Não é problema nesta casa (Linux com GNU), e por isso não virou cura — mas
  não há ramo que **diga** que a listagem falhou. **Grau: SUSPEITA COM
  MECANISMO** — o caminho foi lido, o caso não foi construído.
