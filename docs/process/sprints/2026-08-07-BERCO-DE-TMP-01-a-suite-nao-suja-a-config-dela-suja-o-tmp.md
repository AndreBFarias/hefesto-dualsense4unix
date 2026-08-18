# BERÇO-DE-TMP-01 — a suíte não suja a config dela; suja o `/tmp`

- **Pedido dela, 07/08/2026:** *"salvo engano também ficamos de ver uma forma
  automática de limpar as configs do projeto após os testes pra deixarmos tudo
  certo"*
- **Estado:** **CURA APLICADA** para o `/tmp`, com testes que mordem; o `$HOME`
  já estava limpo e agora tem um segundo instrumento (aviso); o que sobra está
  listado em *O que fica ABERTO*
- **Gravidade:** MÉDIA para o disco (2 MB e 906 diretórios acumulados), **ALTA
  para o diagnóstico** — a medição desta sprint achou a suíte fazendo o daemon
  VIVO dela escrever e mexer em `/dev/hidraw2`
- **Mãe:**
  [CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md)
  — esta paga o item *"o canário não vigia fora das três árvores"* daquela
- **Irmã:**
  [SUÍTE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
  — mesmo defeito de fundo (a suíte tocando o sistema vivo); esta traz **prova
  nova** de que ele continua aberto

---

## A pergunta dela, respondida por medição antes de qualquer código

Ela pediu uma faxina das configs depois dos testes. A primeira coisa a fazer
não era escrever o faxineiro — era **medir se há sujeira**, e onde.

**O instrumento:** um retrato do disco (`caminho | mtime_ns | tamanho`, uma
linha por entrada) tirado imediatamente antes e imediatamente depois de uma
suíte inteira, sobre `~/.config/hefesto-dualsense4unix`, `~/.config/wireplumber`,
`~/.local/share/hefesto-dualsense4unix`, `~/.local/state` (recursivo), `~/.cache`
(recursivo), `/tmp`, `~/.config` e `~` (primeiro nível). **116.687 entradas
antes, 116.703 depois.**

**A suíte medida:** `7619 passed, 1 skipped, 2 xfailed, 2 failed` em **232,51 s**
(as duas falhas são de outro workflow que estava mutando a árvore ao lado —
`test_coop_derrubado_aparece_no_banner` e `test_home_autoswitch_lock_hint` —, e
não têm relação com esta leva).

**O delta: 16 CRIADOS, 0 APAGADOS, 34 MUDADOS.**

### A boa notícia, e ela é a resposta direta à pergunta dela

**Grau: MEDIDO.** A suíte **não escreveu um byte** em
`~/.config/hefesto-dualsense4unix`, em `~/.config/wireplumber` nem em
`~/.local/share/hefesto-dualsense4unix`. O CANÁRIO-FS-01 ficou **calado** a
execução inteira.

Os únicos deltas naquele diretório foram **mtime de `*.json.lock`, com conteúdo
idêntico** — que é exatamente o vaivém do `filelock` tocado pelo daemon e pela
janela DELA, medido em 05/08 e a razão de o canário comparar sha256 em vez de
mtime. **Não há config dela para limpar depois dos testes.**

### A má notícia: o lixo existe, e mora em `/tmp`

| o quê | quantos por execução | quem cria |
|---|---|---|
| `tmp<8>/` | **9** | `tempfile.mkdtemp()` **sem limpeza**, nos dois arquivos de teste de migração de perfil |
| `tmp.<10>` | **6** | `mktemp` de **shell**, dentro de script sob teste |
| `pulse-<12>/` | **1** | a libpulse, criando o runtime dir |
| `hefesto_teste_pactl_chamadas.txt` | reescrito | **caminho FIXO** num teste |

**Grau: MEDIDO**, e a causa dos 9 foi confirmada duas vezes — por leitura do
código (`d = Path(tempfile.mkdtemp())` sem `finally`, 7 chamadas em
`tests/unit/test_coop_default_on_migration.py` e 2 em
`tests/unit/test_preset_flavor_migration.py`) e pelo **conteúdo dos diretórios
no disco**, que são os arquivos daqueles testes.

**O acumulado no dia da medição:**

- **906** diretórios `tmp<8>` em `/tmp`, **892** deles ainda com os arquivos que
  só aqueles dois testes escrevem;
- **99** `pulse-*` (um por execução da suíte);
- **3** `hefesto-arvore-congelada-*` que o `atexit` não alcançou porque a sessão
  foi morta;
- `/tmp/pytest-of-vitoriamaria` com **1,3 GB** e 13 diretórios numerados (a
  retenção do pytest guarda 3).

### A notícia grave: a suíte faz o daemon VIVO dela escrever

Quatro arquivos de `~/.local/state/hefesto-dualsense4unix/launch_env/` foram
**regravados às 16:19:38**, dentro da janela da suíte. Essa árvore estava fora
de todo instrumento desta casa.

Não foi a suíte que escreveu — ela roda com `XDG_STATE_HOME` isolado. Foi o
**daemon dela**, e o journal nomeia o mecanismo:

```
16:19:14–16:20:56  kernel: input: Hefesto - Dualsense4Unix Virtual Keyboard   (17 vezes)
16:19:38  hefesto-dualsense4unix[2870305]: launch_env_materializado  arquivos=4   (3x)
16:19:57  hefesto-dualsense4unix[2870305]: backend_hotplug_reconcile  trigger=input_dir_change
16:19:57  hefesto-dualsense4unix[2870305]: hidraw_broker_hidden  node=/dev/hidraw2
```

**Os 17 teclados virtuais da SUÍTE-QUE-SUJA-O-JORNAL-01 estão vivos hoje, com o
NOME DE PRODUÇÃO** — a E1 e a E2 daquela sprint continuam abertas, e agora há
prova de que o efeito não para no journal: o daemon dela **reage** ao que a
suíte faz em `/dev/input`, reescreve estado no disco e **esconde um nó de
hidraw**.

**Reproduzido na execução de aceite**, três horas depois e com a cura do `/tmp`
já aplicada: os MESMOS quatro `.env` foram regravados de novo, e desta vez cada
rajada de `launch_env_materializado` (16:39:16, 16:42:12, 16:43:49) veio logo
depois de um par de `backend_hotplug_reconcile trigger=input_dir_change`
(16:38:54/56, 16:40:34/36, 16:43:28/30), com 51 teclados virtuais nascendo na
mesma janela. E no dia inteiro **toda** rajada de materialização cai dentro de
uma janela de rajada de uinput — 15:46, 15:50, 15:59, 16:01, 16:03, 16:19,
16:29, 16:31, 16:39, 16:42, 16:43.

**Grau:** a escrita, os horários e a correlação são **MEDIDOS**; o elo causal é
**SUSPEITA COM MECANISMO FORTE** — cada elo da cadeia está nomeado no próprio
log do daemon (`input_dir_change` → `reconcile` → `materializado`), mas falta o
braço de controle (daemon de pé, suíte parada) que transformaria correlação em
causa. Ele não cabia nesta leva: a máquina está em uso e outra suíte roda ao
lado.

---

## Os `.lock` órfãos — a pergunta 2, e a resposta muda a decisão

Três órfãos em `~/.config/hefesto-dualsense4unix/profiles/`:
`meu_perfil.json.lock`, `pragmata2.json.lock`, `sackboy_nativo.json.lock`, sem o
`.json` correspondente.

**Quem cria:** o `filelock`, por `_lock_path()` (`profiles/loader.py:78`), em
onze pontos do loader. O `filelock` deixa o arquivo no disco depois de soltar a
trava — é o mesmo comportamento que produziu os 15 falsos positivos da estreia
do canário.

**Quem deveria remover:** ninguém remove. `delete_profile`
(`profiles/loader.py:948`) arquiva a última versão em `.historico/<slug>/` e faz
`candidate.unlink()` — **só do `.json`**.

**A prova de que foi o produto, e não um teste — MEDIDO.** O mtime de cada
`.lock` órfão bate **ao microssegundo** com o nome do arquivo que o histórico
guardou no mesmo instante:

| `.lock` órfão | mtime | arquivo guardado no `.historico/` |
|---|---|---|
| `meu_perfil.json.lock` | `20:51:44.924013713` | `20260806T205144_924092.json` |
| `pragmata2.json.lock` | `20:18:15.285193750` | `20260806T201815_285294.json` |
| `sackboy_nativo.json.lock` | `20:17:21.985209856` | `20260806T201721_985379.json` |

**Consequência para o desenho:** os órfãos **não são lixo de teste** e **não
entram em nenhuma faxina automática**. A suíte roda com `XDG_CONFIG_HOME`
isolado e nunca chegou perto deles. É conserto no produto (`delete_profile`
apagar o `.json.lock` junto), e mexer na config dela é decisão dela.

---

## A cura

### 1. O BERÇO — `tests/conftest.py`

`pytest_sessionstart` cria `/tmp/hefesto-berco-<pid>` e aponta
`tempfile.tempdir` **e** `TMPDIR`/`TMP`/`TEMP` para lá. `pytest_sessionfinish`
leva o diretório inteiro embora.

Isso alcança, de uma vez, **duas das três origens medidas**: `tempfile`
(Python) e `mktemp` (shell, dentro dos scripts sob teste, pelo ambiente). E
alcança **a próxima**, que ninguém escreveu ainda.

**A terceira não: REFUTADO POR EXECUÇÃO em 07/08.** A primeira versão desta
sprint afirmava que o berço alcançaria *"qualquer biblioteca que respeite
`TMPDIR`, inclusive a libpulse"*. A execução de aceite mostrou o contrário: com
o berço armado, **dois `pulse-<12>` nasceram no `/tmp` real**, fora dele — a
libpulse não resolve o runtime dir pelo `TMPDIR`. A afirmação errada fica
registrada aqui em vez de ser apagada; o `pulse-*` continua sendo caso de
relatório da faxina, e não de faxina.

**O critério de "isto é lixo de teste" é POSITIVO, e é o ponto do desenho.** Não
é *"não reconheço este arquivo, então apago"* — é *"este diretório foi criado
por ESTA sessão de pytest, com ESTE pid no nome, e tudo que está dentro nasceu
depois disso"*. Fora do berço, nada é tocado por nenhum caminho de código.

Cinco detalhes, cada um com um defeito por trás:

1. **O `basetemp` do pytest fica FORA do berço**, resolvido à força antes do
   desvio (`_fixar_basetemp_do_pytest`). Dois motivos medidos: o pytest já
   guarda as 3 últimas execuções (é o que se olha quando um teste cai), e o
   `sun_path` de um `AF_UNIX` tem ~108 bytes — há teste desta casa cujo socket
   sob `tmp_path` já chega a 95, e somar os 27 do berço seria trocar um defeito
   por outro;
2. **`_SESSAO_REAL`** — só a Session que armou o berço pode varrê-lo. **Isto é
   defeito medido, não zelo:** nove testes de `test_conftest_canario_fs.py`
   chamam `pytest_sessionfinish` com uma Session de mentira, de propósito, para
   provar o portão do canário. Sem a guarda, a primeira dessas chamadas varria o
   berço da sessão VIVA no meio dela e devolvia `tempfile.tempdir` ao `/tmp`
   real — a suíte voltava, **em silêncio**, ao comportamento que o berço veio
   curar, e a única pista eram quatro testes pulando;
3. **Berço de sessão morta é varrido na sessão seguinte**, pelo pid do nome. Uma
   sessão morta a `kill` não roda `sessionfinish` — foi assim que os 3
   `hefesto-arvore-congelada-*` chegaram ao `/tmp` dela;
4. **Sessão vermelha PRESERVA o berço.** O que a suíte deixou pode ser prova, e
   guardar custa um diretório que a próxima sessão varre sozinha;
5. **O relato do que o berço engoliu.** Varrer em silêncio esconderia o defeito
   de origem; o relato é o que permite consertar o teste que vaza.

**Escotilha:** `HEFESTO_SEM_BERCO_TMP=1`, mesma lógica do canário — uma
escotilha declarada é melhor que um portão contornado no escuro.

**Verificado em 07/08, em dois níveis.** Primeiro no pequeno: com o berço
armado, `test_coop_default_on_migration.py` e `test_preset_flavor_migration.py`
rodaram os mesmos 13 testes e o `/tmp` foi de **915 diretórios `tmp<8>` para
915** — os 9 nasceram e saíram no berço, e o relato os nomeou.

Depois no aceite, com a suíte inteira (**7713 passed, 1 skipped, 2 xfailed em
234,74 s**) e o mesmo retrato do disco dos dois lados:

| | antes da cura | depois da cura |
|---|---|---|
| entradas novas em `/tmp` | **16** | **1 a 2** (só `pulse-*`, que a libpulse cria ignorando `TMPDIR`) |
| entradas alteradas em `/tmp` | 1 (`hefesto_teste_pactl_chamadas.txt`) | **0** |
| deltas nas 3 árvores do canário | 0 | **0** |
| berço órfão de sessão morta | — | **1 varrido sozinho** no início da sessão seguinte |

O berço engoliu **16 entradas** nessa execução e as levou embora, nomeando-as no
relato. E a linha `APAGADO /tmp/hefesto-berco-3172608` do retrato é o
autoconserto funcionando: um berço de sessão morta que a sessão seguinte varreu
pelo pid.

**Nenhum teste quebrou com o `TMPDIR` desviado** — o risco medido de antemão era
o limite de ~108 bytes do `sun_path`, e ele não foi atingido porque o `tmp_path`
do pytest ficou fora do berço. Duas execuções inteiras fecharam em
**7713 passed, 1 skipped, 2 xfailed**.

### Um defeito de terceiro que a própria bancada pegou, e vale registrar

Uma das execuções de aceite voltou com **5 vermelhos** no
`test_conftest_canario_fs.py`, e a ARVORE-CONGELADA-01 já dizia o motivo no
mesmo relatório: `MUDADO scripts/faxina-de-testes.py` — eu tinha salvado um
ajuste **enquanto a suíte estava medindo**. O guarda funcionou contra quem o estava
usando, que é o teste mais honesto que ele podia passar.

O que ficou de aprendizado, e virou linha de código: aqueles testes chamam o
`pytest_sessionfinish` DE VERDADE, e ele carrega três guardas. A da
ARVORE-CONGELADA-01 mede a árvore REAL e **também** escreve `exitstatus = 1` —
então, numa árvore viva, ela derrubava asserções de `exitstatus == 0` por um
motivo que nada tem a ver com o canário. O `_lar_falso` passou a neutralizá-la
(`monkeypatch.setattr(canario, "_deltas_do_congelado", lambda: [])`), com o
porquê escrito ali. **Não afrouxa nada:** a mordida do canário é o
`exitstatus = 1` que o bloco DELE escreve, e essa continua valendo linha por
linha — provada de novo depois da mudança. **Grau: MEDIDO** (5 vermelhos com a
árvore em movimento, 0 com a árvore parada, mesma leva).

### 2. O canário ganha uma lista que AVISA e não reprova

`_CANARIO_ALVOS_AVISO` acrescenta `~/.local/state/hefesto-dualsense4unix`.

**Por que aviso e não portão:** o que muda ali é o daemon VIVO dela reagindo à
suíte, não a suíte escrevendo. Reprovar deixaria a suíte vermelha na máquina
dela e verde na CI — o portão que se aprende a desligar na semana seguinte, que
é a lição do DIV-11 (os 15 `.lock` da estreia do canário). O que faltava era
**enxergar**: essa árvore estava fora de todo instrumento.

**E nada é restaurado, nunca.** Está escrito no código e nos testes: desfazer
escrita da daemon dela seria o dano maior. Para o `$HOME` o desenho continua
sendo prevenir e DETECTAR.

### 3. O caminho fixo consertado

`tests/unit/test_doctor_mic_camada2.py` gravava em
`/tmp/hefesto_teste_pactl_chamadas.txt`. Caminho fixo tem **dois** defeitos, não
um: fica para trás **e colide entre sessões** — nesta máquina rodam várias
execuções de `pytest` ao mesmo tempo, e duas delas escreviam no mesmo arquivo. O
nome passou a vir do `tempfile` (nasce no berço) e o teste o remove ele mesmo.

### 4. A faxina do passivo — `scripts/faxina-de-testes.py`

O berço resolve o futuro; o passivo de 906 diretórios precisa de um comando. **O
critério foi escrito antes do código**, e está no cabeçalho do arquivo. Quatro
regras, cada uma com prova de **quem criou**:

| regra | alvo | a prova |
|---|---|---|
| **R1** | `hefesto-berco-<pid>/` | o nome é escrito por `tests/conftest.py`, e o pid **não está vivo** |
| **R2** | `hefesto-arvore-congelada-<8>/` | prefixo escrito por `arvore_congelada()`, e mais velho que a idade mínima |
| **R3** | `tmp<8>/` | contém um dos marcadores que **só** as migrações escrevem **e** todo nome lá dentro está num conjunto **FECHADO** |
| **R4** | `hefesto_teste_pactl_chamadas.txt` | nome literal **e** conteúdo começando com `pactl ` |

Um único nome fora do conjunto fechado e o diretório é **RECUSADO com o
motivo** — porque aí ele pode ser de outra coisa. O erro cai sempre para o lado
de não apagar.

**O que ele se recusa a fazer, por decisão declarada:** apagar `pytest-of-*` (é
do pytest, tem retenção própria e pode estar em uso), apagar `pulse-*` (é da
libpulse, que roda fora da suíte), aceitar `$HOME` — ou qualquer diretório
dentro ou acima dele — como raiz, seguir link simbólico, e tocar em entrada de
outro dono. **O padrão é só relatar**; apagar exige `--apagar`, porque a decisão
sobre o que já está no disco dela é dela.

**Rodado em modo relato no `/tmp` real, 07/08:** 911 alvos provados (2,0 MB), e
o berço de uma sessão de pytest que rodava ao lado naquele instante apareceu
corretamente na lista de **recusas**, com o motivo *"berço de sessão VIVA"*.

---

## Os testes que MORDEM

`tests/unit/test_berco_de_tmp.py` (26 casos) e
`tests/unit/test_faxina_de_testes.py` (26 casos), mais 5 casos novos em
`tests/unit/test_conftest_canario_fs.py`.

Cada mordida foi provada **arrancando a cura numa cópia da árvore** — nunca na
árvore de trabalho, porque outro workflow rodava `pytest` nela ao mesmo tempo, e
é exatamente o defeito que a
ARVORE-CONGELADA-01 mede (a guarda mora em `tests/conftest.py`, e a reprodução
em três braços está registrada no comentário dela).

| arrancar isto | reprova |
|---|---|
| `tempfile.tempdir = <berço>` | `test_tempfile_passa_a_nascer_dentro_do_berco`, `test_a_arvore_congelada_nasce_dentro_do_berco` |
| o `rmtree` da varredura | `test_a_varredura_leva_o_berco_inteiro` + mais 2 |
| a guarda `_SESSAO_REAL` | `test_sessao_de_mentira_nao_varre_o_berco_da_sessao_viva` |
| o `isdigit()` de `_pid_do_berco` | 4 casos de `test_nome_que_nao_e_berco_nunca_e_alvo` |
| o `_pid_vivo` de `_bercos_orfaos` | `test_berco_de_sessao_viva_nunca_entra_na_varredura` + 1 |
| **trocar o critério positivo pelo negativo** (varrer o que "parece temporário" ao lado) | `test_arquivo_real_dela_ao_lado_do_berco_nao_e_tocado` |
| o conjunto fechado da R3 | `test_um_nome_fora_do_conjunto_fechado_salva_o_diretorio_inteiro` + 1 |
| a exigência do marcador na R3 | `test_diretorio_sem_marcador_nem_e_mencionado` |
| o `_pid_vivo` da faxina | `test_berco_de_sessao_viva_e_recusado` + 1 |
| a recusa do `$HOME` como raiz | `test_o_home_dela_nunca_pode_ser_raiz` + 1 |
| a recusa de seguir link | `test_link_simbolico_nunca_e_alvo` |
| o padrão "só relatar" | `test_o_padrao_e_relatar_sem_apagar_nada` |
| pôr o aviso do canário dentro do bloco que reprova | `test_mudanca_na_arvore_de_aviso_relata_e_nao_reprova`, `test_o_aviso_nao_engole_o_portao` |

**O caso perigoso tem teste dos dois lados**, e é o que decide se estes
mecanismos podem existir: um arquivo REAL dela no meio da sujeira, na mesma
execução em que o lixo é removido, precisa sair intacto —
`test_arquivo_real_dela_ao_lado_do_berco_nao_e_tocado` e
`test_com_apagar_leva_o_alvo_e_deixa_o_resto`.

---

## O que fica ABERTO

- **Os 17 teclados uinput com o NOME DE PRODUÇÃO** continuam nascendo a cada
  execução — E1 e E2 da SUÍTE-QUE-SUJA-O-JORNAL-01, agora com prova de que o
  daemon dela **reage** a eles escrevendo em `~/.local/state` e escondendo
  `/dev/hidraw2`. Isto subiu de prioridade;
- **o elo causal do `launch_env`** precisa de braço de controle (suíte parada,
  daemon de pé) para virar MEDIDO;
- **os 3 `.lock` órfãos**: conserto no produto (`delete_profile` remover o
  `.json.lock` junto do `.json`), e limpar os que já estão lá é decisão dela;
- **`/tmp/pytest-of-vitoriamaria`, 1,3 GB em 13 diretórios numerados** — a
  retenção do pytest guarda 3 e não está dando conta, provavelmente por travas
  de sessões concorrentes. A faxina só RELATA;
- **o canário continua sem ver LEITURA** — o limite estrutural registrado na
  CANÁRIO-FS-01 não mudou;
- **`utils/i18n.py` e `core/system_check.py` continuam lendo o `$HOME` real sob
  teste**, e o `HOME` continua não isolado no autouse;
- **rodar a faxina com `--apagar`** no `/tmp` dela: 911 alvos, 2,0 MB. É dela a
  palavra.

---

## Relacionado

- [CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md)
  — o instrumento que respondeu "o `$HOME` está limpo", e cujo limite declarado
  ("não vigia fora das três árvores") esta sprint paga
- [SUÍTE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
  — onde já estava escrito que *"não há o que remover"* no caso do uinput; aqui
  há, e é outro recurso
- ARVORE-CONGELADA-01, no comentário de `tests/conftest.py` — a razão de as
  mordidas desta sprint terem sido provadas numa cópia da árvore
- [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md)
  — o `.historico/` que serviu de relógio para datar os `.lock` órfãos
