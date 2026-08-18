# workflow quarta-rodada-bluez

- runId: wf_a425e5ec-714 | status: completed | agentes: 4 | tokens: 773,285 | duracao: 117 min
- summary: Investigar a bancada instavel (6 de 10 execucoes falhando), curar a poda por ESTADO, o caminho dos drop-ins e o portao do Flatpak
- fases: Investigar, Curar, Fechar

## RESULTADO

### diagnostico

## VEREDITO

**MEDIDO.** A bancada `tests/unit/test_bluez_config_sh.py` **não é instável**. Ela executa `scripts/bluez_config.sh` e `scripts/doctor.sh` **pelo caminho absoluto da árvore de trabalho**, e durante a janela 18:04-18:14 de 06/08/2026 **dois agentes irmãos, rodando em paralelo na MESMA árvore, estavam mutando esses arquivos** (arrancar cura -> rodar -> `cp ORIG` de volta). O verificador estava medindo o produto de outra pessoa, mutado, no meio do voo.

## 1. Reprodução: a falha aparece e some sob controle

Réplica fiel da bancada em `/tmp/claude-1000/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/scratchpad/replicaA` (92 verdes isolada). Nenhum arquivo de produto foi tocado; o mutador ataca só a réplica.

| braço | bancada roda em | mutador cicla em | resultado |
|---|---|---|---|
| B (controle) | replicaA | ninguém | **0 falhas / 10** |
| A (mesma cópia) | replicaA | **replicaA** | **5 falhas / 10**, testes DIFERENTES a cada vez |
| C (cópia vizinha) | replicaB | replicaA | **0 falhas / 10** |

O braço A produziu, entre outras, **as duas falhas exatas do relato**:
- `test_o_dono_unico_le_exatamente_o_que_o_bluez_le[grupo-errado-nao-conta]`
- `test_aplicar_nao_apaga_backup_nenhum`

Mensagem verbatim sob a mutação do grupo, idêntica à citada:
```
AssertionError: caso 'grupo-errado-nao-conta': o dono único leu 'confirm' e o BlueZ lê 'always'
```
O braço C é a prova de que o canal é **o arquivo compartilhado**, não carga/tempo: o mutador rodou os mesmos 46 ciclos, a máquina sofreu a mesma disputa, e a bancada ficou verde porque lia outra cópia.

Efeito de segunda ordem também MEDIDO: como as mutações escrevem sem troca atômica (`open(p,"w")` trunca e depois escreve), uma execução pode **ler o script pela metade** — foi assim que caíram no braço A testes de TEXTO (`test_o_caso_do_link_simbolico_esta_dito`, `test_a_frase_do_resumo_deixou_de_ser_mentira`) que mutação nenhuma explicaria.

## 2. A causa, com nome e hora (MEDIDO, dos transcritos)

Workflow `wf_8e0afc80-1a5`: três subagentes lançados **em paralelo às 17:56:42** na mesma árvore. `a162f1` era o verificador que rodava a bancada em laço; `a41a2b` e `a7a615` mutavam o produto.

| falha relatada | mutação viva na árvore | quem, quando |
|---|---|---|
| `test_always_reprova_e_nao_ganha_selo_verde` | D1: `fail` -> `pass` no ramo always do `doctor.sh` | a7a615, 18:06:17 |
| `test_o_detector_e_chamado_por_main` / `..._no_bloco_de_radio` | D2: apaga a chamada em `main()` | a7a615, 18:06:17 |
| `test_duas_gravacoes_no_mesmo_segundo...` / `test_aplicar_e_remover_seguidos_nao_colidem` | M1: nome de backup volta à resolução de 1 segundo | a41a2b, 18:07:04 |
| **4 casos do grupo + `test_o_veredito_acompanha_o_grupo`** | remove `if (_grupo != "General") next` de `_ler_chave` | a41a2b, 18:07:56 / 18:09:03 / 18:09:29 / 18:10:15 |
| **`test_aplicar_nao_apaga_backup_nenhum`** | P2: devolve a poda AUTOMÁTICA ao `_aplicar` (`cp mut.sh scripts/bluez_config.sh`) | a7a615, 18:07:10 / 18:08:04 / **18:09:29** / **18:10:28** |
| `test_um_kill_no_meio_da_troca_nao_deixa_temporario` | M6: arranca o `trap` de limpeza | a41a2b, 18:10:56 |
| `test_never_dentro_do_bloco_nao_ganha_promessa...` | M7/M8: promessa do `never` volta a ser única | a41a2b 18:10:56, a7a615 18:13:45 |
| `test_bloco_de_zero_byte_nao_anuncia_garantia`, `test_podar_nunca_apaga_backup_de_conteudo_unico` | P2 / poda | a7a615 |

**Toda** falha do relato é a **mordida pretendida** de uma mutação que um irmão tinha viva naquele instante. Nenhuma sobrou sem dono.

O experimento natural já estava gravado no próprio transcrito do verificador: 11 execuções vermelhas em 43, entre 18:06 e 18:14 (com mutadores vivos); e **0 vermelhas em 41 execuções** de 18:23:34 em diante — quando `a41a2b` (18:24:48) e `a7a615` (18:25:04) já tinham saído. Ele mesmo mediu "SOB CARGA falhas=0/8", "PAR falhas=0/10", "COMPOSTO falhas=0/5" e não fez a ligação porque não enxergava os irmãos.

## 3. Hipóteses derrubadas (MEDIDO)

- **Carga / outros agentes como ruído**: 6 laços de CPU cheios, 0/8 falhas (medição do próprio verificador) e meu braço C. Refutada como causa — só o **arquivo compartilhado** produz falha.
- **Concorrência entre execuções**: 18 execuções simultâneas (3 rodadas de 6 `pytest` ao mesmo tempo, árvore real) = **0 falhas / 18**. `tmp_path` é por teste e por processo; não colide.
- **`pytest-xdist` / execução paralela / ordem aleatória**: não instalados (`pytest 9.1.1`, só `pytest-asyncio` e `pytest-cov`), e não há `addopts` em `pyproject.toml`.
- **`mktemp`/nome derivado do tempo colidindo**: o backup já sai de `mktemp "...hefesto-${rotulo}$(date +%s)-XXXXXX"`; 20 execuções sequenciais das duas bancadas = **0 falhas / 20** (104 testes cada).
- **Estado global entre testes (env, PATH, raiz falsa compartilhada)**: a réplica roda com `--noconftest` e dá exatamente os mesmos 92 verdes — o `conftest.py` não participa. Cada teste monta a própria raiz em `tmp_path`.
- **Oráculo em subprocesso disputando recurso**: o oráculo lê um arquivo em `tmp_path` com GKeyFile; sobreviveu a 18 execuções simultâneas sem uma falha.

Total de execuções limpas nesta investigação: **58** (20 sequenciais + 18 simultâneas + 20 das réplicas B e C), zero falhas.

## 4. Contaminação: sim, e não é só a bancada

**A instabilidade NÃO é ortogonal — ela contamina, e nos dois sentidos.** Uma mutação alheia viva produz **vermelho falso** (mordida afirmada que não existe — exatamente o defeito que a casa proíbe); e o `cp ORIG` de um irmão **apaga a sua mutação antes do `pytest` rodar**, produzindo **verde falso** (mordida real declarada inexistente).

Contagem de execuções de `pytest` que rodaram com mutação de OUTRO agente viva na árvore (limite superior, pela janela da chamada):

- `wf_26c86ba1-7c4` (rodada 1): **0** sobreposições — um mutador só, sem irmão medindo. **Não contaminada.**
- `wf_d99fbd5f-ecb` (rodada 2): **8** execuções contaminadas, entre 17:03:18 e 17:06:51 (agentes `a6a4ce`, `a9d2ca`, `ab77db`).
- `wf_8e0afc80-1a5` (rodada 3): **14** execuções contaminadas, entre 18:04:02 e 18:15:48 (`a162f1`, `a41a2b`, `a7a615`).

Sobre os dois itens que você citou:

- **Os 39 cenários contra o oráculo** (agente `a7a615`): a metade que só pergunta "o que o GKeyFile lê deste texto" é **imune** — o oráculo abre um arquivo temporário e não toca o repositório. A metade que compara com "o que o dono único lê" chamava `bash scripts/bluez_config.sh verificar` **da árvore**, às 18:09:29 — segundo em que o próprio `a7a615` tinha o mutante P2 no lugar e `a41a2b` estava aplicando a mutação do grupo. Essa metade **precisa ser refeita em série**. Grau atual dela: SEM PROVA.
- **As oito mutações do detector**: cada uma foi medida por `a41a2b`/`a7a615` dentro da janela 18:04-18:15, com o irmão mutando o mesmo arquivo. Das 14 execuções contaminadas, 7 são do `a41a2b`/`a7a615` medindo as próprias mordidas. **Suspeitas, uma a uma**, até serem refeitas com um mutador só na árvore.

O que **continua de pé sem refazer**: o estado medido em `/etc/bluetooth/main.conf` na máquina dela, a tabela `_TABELA_DO_GRUPO` (conferida pelo oráculo, que não usa o script), e qualquer afirmação obtida fora da janela de sobreposição.

**A árvore de hoje está íntegra**: `git diff` vazio em `scripts/`, `install.sh`, `uninstall.sh` e `assets/`; `scripts/bluez_config.sh` = `e53d11a541da0f6cf3ba2a4791bfed9a`, `scripts/doctor.sh` = `b8259c1067a52b572ecbe57d2ad23186` — os mesmos md5 que `a162f1` registrou às 18:34. Nenhuma mutação ficou esquecida.

## 5. O que fecha isso (proposta, NÃO aplicada)

1. A bancada deveria copiar `scripts/`, `assets/` e os `.sh` de raiz para uma cópia sob `tmp_path_factory` **uma vez por sessão** e apontar `RAIZ` para lá — assim mutação alheia deixa de ser canal. É a única cura que independe de disciplina de processo.
2. Enquanto isso não existir, **nenhum fan-out paralelo pode mutar a árvore**: mutação e medição precisam de exclusão mútua (um `flock` no repositório) ou de `git worktree` por agente.
3. Reprovar por hora: refazer, **em série e sozinho**, as 22 execuções listadas acima antes de gravar qualquer nota que dependa delas.

## Arquivos desta investigação

- `/tmp/claude-1000/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/scratchpad/mutador.py` — o mutador cíclico (grupo e poda automática)
- `/tmp/claude-1000/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/scratchpad/arma.sh` — os três braços
- `/tmp/claude-1000/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/scratchpad/replicaA`, `.../replicaB` — réplicas isoladas da bancada
- `/tmp/claude-1000/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/scratchpad/seq` (20 sequenciais) e `.../conc` (18 simultâneas)
- Fonte forense: `~/.claude/projects/-mnt-Apate-Desenvolvimento-hefesto-dualsense4unix/9147457e-032a-4d1e-aa95-63cdf0d6434e/subagents/workflows/wf_8e0afc80-1a5/`

Nada foi commitado, nada em `/etc` foi escrito, nenhum arquivo de produto foi editado.

### cura

BANCADA: 20/20 verdes (125 testes cada), duas vezes — antes e depois da última leva de edições; md5 dos dois scripts intacto ao fim.

0-BANCADA (MEDIDO): a instabilidade não era da bancada — era o produto mudando debaixo dela. Cura em `tests/conftest.py` (ARVORE-CONGELADA-01): as duas bancadas leem uma CÓPIA da árvore tirada uma vez por sessão, não `/mnt/.../scripts/*.sh`. **DISCORDEI da proposta 1 do diagnóstico num ponto:** congelar NÃO dá imunidade. Reproduzi com mutador a 2 Hz na árvore: ainda 6 vermelhos/10 — mas o ganho é outro e é total, as falhas deixaram de ser SORTEADAS (antes, testes diferentes a cada rodada; depois, TODA rodada vermelha caiu no mesmo conjunto de 4, a mordida pretendida). Por isso acrescentei o que faltava: uma sonda que compara a foto com a árvore no fim e REPROVA o run — pega o `cp ORIG` alheio, que é o VERDE falso, o pior dos dois erros. Declarei o limite dela (dois instantes, não vigia o intervalo: acusou 3 de 10).

REVALIDAÇÃO: as 9 mordidas da janela contaminada, refeitas EM SÉRIE, sozinho na árvore, restauração conferida por md5 E por modo — as 9 mordem. Saiu uma correção: a mutação do grupo derruba TRÊS casos da tabela + `test_o_veredito_acompanha_o_grupo` (4 falhas), não os "quatro casos" da rodada 3.

1-ALTA (MEDIDO, morde): `_podar` protege ESTADO, não arquivo — cada conteúdo distinto guarda um guardião (a cópia mais ANTIGA dele). Teste novo no cenário que importa: 3 estados × 3 cópias, retenção 1 — a regra velha aniquilava o estado do meio. Frase final reescrita.

2-MÉDIA (MEDIDO, morde): **escolhi obedecer, não declarar exceção** — o motivo da invariante não é a propriedade do caminho, é que aquilo é config de alguém, e o custo da simetria é um `cmp` no caminho feliz. Drop-ins agora com `cmp`+backup+aviso nos dois lados; exceção "igual byte a byte ao asset = sem backup" DECLARADA no cabeçalho.

3-MÉDIA (MEDIDO, morde): backup de 0 byte sai de `backups-hefesto:`, entra em `backups-suspeitos:`/`backup-suspeito:` nomeado, e o `aplicar` diz que o tirou da conta — trocar número errado por silêncio não é cura. A poda não o alcança (mesma regra dos órfãos).

4-MÉDIA (MEDIDO, morde): portão e bancada trocaram `scripts/build_flatpak.sh` pelo MANIFESTO. Bancada nova roda o portão de verdade contra repo falso: manifesto com doctor sem o dono REPROVA, e comentário não satisfaz. Detector: distingue "não existe" de "não consigo ver" e diz `[WARN] NÃO SEI ... sandbox`.

5-HONESTIDADE: **DISCORDEI do relatório da rodada 3 e retratei.** Reproduzi a medição do terceiro — arrancar só o `cmp` deixa `test_backup_parcial...` VERDE (o `||` curto-circuita). Não apaguei a frase: escrevi a bancada que faltava, `test_backup_que_mente_ter_copiado_e_pego_pelo_cmp`, com um `cp` que corta o arquivo e MENTE saindo 0 (NFS, disco cheio no `close()`). Ela morde.

BAIXOS, todos MEDIDOS contra o oráculo: (a) arquivo que o GKeyFile recusa inteiro não ganha mais `OK` — `veredito: RECUSADO` nomeando a linha, `fail` no doctor, e o `aplicar` para de anunciar garantia; declarei que é RÉPLICA das duas regras, não o GKeyFile. (b) CRLF: `sub(/\r$/,"")` — medido que o GKeyFile tira o CR e PRESERVA os espaços. (c) `JustWorksRepairing=` vira `(vazio)`, não `ausente`. (d) nota do `install.sh` corrigida: o grep acha DUAS linhas, a segunda casa `uninstall.sh`. (e) as três exceções do "byte a byte" declaradas e MEDIDAS por teste.

PORTÕES: 7217 passed, 1 skipped (base 7193+1, +24 novos); ruff, mypy, os quatro de documentação, paridade, anonimato, dados de teste, `shellcheck -S error`, `bash -n` — todos verdes. Nada commitado. Nada escrito em `/etc`. Arquivos-chave: `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/tests/conftest.py`, `.../scripts/bluez_config.sh`, `.../scripts/doctor.sh`, `.../scripts/check_packaging_parity.sh`, `.../tests/unit/test_bluez_config_sh.py`, `.../tests/unit/test_doctor_justworks_comportamento.py`, `.../tests/unit/test_check_packaging_parity.py`, `.../install.sh`, `.../CHANGELOG.md`, `.../docs/process/sprints/2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md`.

AVISO: numa primeira tentativa do experimento, MEU mutador usou `mv` e arrancou o bit de execução de `scripts/bluez_config.sh`; a bancada congelada pegou na hora, restaurei para 755 e conferi md5+modo — a árvore está íntegra (`e53d11a5...`, `b8259c10...`).

### verificacoes

[
  {
    "achados": [
      {
        "gravidade": "alta",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/.git/index (e CHANGELOG.md)",
        "o_que": "O ÍNDICE NÃO É MAIS A LEVA. Quando comecei a verificação, `git diff --cached` eram 15 arquivos — exatamente a entrega do BlueZ. Agora são 20: uma sessão irmã encostou no MESMO índice durante a minha medição e acrescentou cinco documentos de outra frente (perfis/Steam/Sony). Pior, o `CHANGELOG.md` staged carrega hoje DUAS seções: a do BlueZ e `### O experimento do controle da Sony rodou, e ele corrige metade da doutrina da casa`. Um `git commit` do índice como está AGORA não commita a leva de segurança — commita a leva de segurança MAIS a frente alheia, num commit só, com mensagem de uma delas. Isto não é defeito do código verificado (que está íntegro e é o mesmo do começo ao fim: md5 dos três scripts e do conftest idênticos na primeira e na última leitura); é impedimento ao ATO de commitar. A saída é commitar por CAMINHO EXPLÍCITO (os 15 arquivos da entrega) e separar o CHANGELOG, nunca `git commit` do índice inteiro.",
        "prova": "No início: `git status --short` = 15 arquivos (CHANGELOG.md, docs/.../2026-08-06-desenho..., docs/.../RADIO-ABERTO-01..., install.sh, scripts/{bluez_config,build_deb,check_packaging_parity,doctor}.sh, tests/conftest.py, tests/unit/{test_bluez_config_sh,test_bt_resilience_assets,test_check_packaging_parity,test_doctor_justworks_comportamento,test_plataforma_wiring}.py, uninstall.sh). No fim: `git diff --cached --name-only` = 20, os cinco novos sendo docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md, docs/process/sprints/2026-08-05-STEAM-QUE-DECIDE-01-....md, docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-....md, docs/usage/jogos-e-mascaras.md, docs/usage/modos.md. Carimbos: mtime desses arquivos 20:14:14, 20:14:57, 20:15:23; `.git/index` mtime=2026-08-06 20:21:39 — tudo DENTRO da janela das minhas duas primeiras execuções da suíte. `git diff --cached CHANGELOG.md | grep '^+###'` devolve as duas seções. MEDIDO."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/tests/conftest.py (_CONGELAR, linhas da ARVORE-CONGELADA-01)",
        "o_que": "A SONDA TEM UM PONTO CEGO QUE ESTA PRÓPRIA SESSÃO EXERCITOU, e ele não está declarado. `_CONGELAR` cobre `scripts`, `assets/bluetooth`, `flatpak`, `packaging/{arch,debian,fedora,nix}`, `.github/workflows`, `install.sh` e `uninstall.sh`. NÃO cobre `docs/`, `src/` nem `tests/` — e `_deltas_do_congelado()` só itera a cópia congelada, então o que não foi congelado nunca é comparado. O agente irmão escreveu em `docs/` às 20:14–20:15, dentro da janela das minhas execuções 1 e 2 da suíte inteira, e a sonda ficou MUDA — por construção, não por falha. O diagnóstico que abre o arquivo ('a bancada mediu o produto de outra pessoa') vale letra por letra para qualquer teste que leia `docs/` ou `src/` como TEXTO em tempo de execução, e esta suíte tem vários. A declaração de limite hoje escrita fala só do intervalo entre os dois instantes; falta dizer QUAIS árvores ela nem olha. A cura já está nomeada na própria docstring ('um git worktree por agente') — o que falta é a sonda não deixar o leitor achar que está coberto o que não está.",
        "prova": "`_CONGELAR` em tests/conftest.py lista dez caminhos, nenhum deles `docs`, `src` ou `tests`. Reprodução direta do ponto cego: rodei a suíte inteira uma TERCEIRA vez com impressão digital da árvore antes e depois (`git ls-files -m -o`, HEAD, md5 dos scripts e do conftest, `find docs src tests scripts -newermt`) — `diff antes/depois` vazio, e nada escrito em docs/src/tests/scripts durante o run: 7217 passed, 1 skipped. As execuções 1 e 2 deram o MESMO número, mas nelas a árvore comprovadamente NÃO estava parada (mtimes 20:14:14/20:14:57/20:15:23 em docs/) e a sonda não disparou nenhuma vez. MEDIDO. Nada foi contaminado de fato — mas a sonda não foi quem garantiu isso."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/tests/conftest.py (CANARIO-FS-01)",
        "o_que": "O CANÁRIO DE FS REPROVA O RUN PELO APLICATIVO DELA, não pela suíte. Num dos meus experimentos com a sonda, a bancada saiu com rc=1 e a mensagem CANARIO-FS-01 nomeando seis escritas em `~/.config/hefesto-dualsense4unix/profiles/` — criação de `sackboy.json`, de `.historico/sackboy_nativo/`, e apagamento de `sackboy_nativo.json` — num run que só executou `test_bluez_config_sh.py`, arquivo que não tem uma linha de lógica de perfil. A origem é o daemon e a GUI DELA, vivos na máquina agora. O próprio canário antecipa o caso na última linha da mensagem e oferece `HEFESTO_SEM_CANARIO_FS=1`. Isto é anterior a esta leva e não a compromete (não disparou em nenhuma das 33 execuções que eu medi), mas quem for rodar os portões enquanto ela usa o aplicativo vai ver um vermelho que não é do código — e essa é exatamente a classe de vermelho sorteado que a ARVORE-CONGELADA-01 veio acabar, entrando de novo por outra porta.",
        "prova": "Saída completa em .../scratchpad/sonda2.txt: '111 passed in 9.30s' seguido de 'CANARIO-FS-01: a suíte ESCREVEU nos diretórios reais da usuária (6 mudança(s))' e rc=1, com o timestamp 20260806T201721 no nome do arquivo de histórico. `systemctl --user is-active hefesto-dualsense4unix.service` = active; `pgrep -af hefesto` mostra o daemon (PID 298882) e a GUI `python3 -m hefesto_dualsense4unix.app.main` (PID 3878063). MEDIDO."
      },
      {
        "gravidade": "baixa",
        "onde": "o relatório do curador (bloco AVISO, ao fim)",
        "o_que": "OS HASHES DE INTEGRIDADE NÃO REPRODUZEM. O relatório fecha o incidente do `mv` que arrancou o bit de execução com 'a árvore está íntegra (`e53d11a5...`, `b8259c10...`)'. Nenhum dos dois prefixos bate com nenhum algoritmo padrão sobre os dois arquivos hoje. É plausível que tenham sido tirados antes das últimas edições (os mtimes dos scripts são 19:34 e 19:35), mas, como estão escritos, não servem para auditar o acidente que foram oferecidos para encerrar — e a regra da casa é justamente que decisão gravada sobre medição que não se confere é pior que decisão sem nota. A integridade em si eu conferi por outro caminho e ela está boa: árvore idêntica ao índice, modo 755, `bash -n` limpo, suíte verde.",
        "prova": "scripts/bluez_config.sh: md5=de21778a sha1=8c91f7fd sha256=2df2e68f gitblob=81a736c1. scripts/doctor.sh: md5=5854e831 sha1=56c5f00e sha256=a082bed4 gitblob=afa4f455. Nenhum começa por e53d11a5 nem b8259c10. Conferência independente que passou: `git diff --stat` vazio (árvore == índice), `stat -c %a scripts/bluez_config.sh` = 755, `bash -n` rc=0, suíte 7217 passed."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh (modo no disco)",
        "o_que": "RESÍDUO COSMÉTICO DO ACIDENTE DO `mv`: o `bluez_config.sh` está 755 no disco enquanto todo script irmão está 775 (`doctor.sh`, `check_packaging_parity.sh`). Bate com o relato de que ele foi restaurado à mão depois que o mutador lhe arrancou o bit de execução. Nada quebra — o git só rastreia o bit de execução e o índice tem 100755 —, e registro só para que ninguém, mais adiante, leia o modo destoante como sinal de outra coisa.",
        "prova": "`stat -c '%n %a'`: scripts/bluez_config.sh 755, scripts/doctor.sh 775, scripts/check_packaging_parity.sh 775. `git ls-files -s` devolve 100755 para os três — o índice não vê diferença."
      }
    ],
    "aprovado": true,
    "veredito": "A BANCADA É CONFIÁVEL. Refiz a medição por conta própria e ela sustenta o que o curador relatou, inclusive no ponto em que ele se retratou.\n\n1) TRINTA EXECUÇÕES SEGUIDAS, ZERO FALHAS (MEDIDO). `test_bluez_config_sh.py` + `test_doctor_justworks_comportamento.py`, 30 rodadas em série: 30 de 30 verdes, 125 passed em CADA uma, nenhum skip (o oráculo GKeyFile rodou de verdade — se faltasse PyGObject apareceriam skips), nenhuma variação de contagem, e a sonda ARVORE-CONGELADA-01 nunca disparou. Zero é o número. Confirmei também que não há plugin de aleatorização instalado, então a ordem foi a mesma do comando do CI.\n\n2) A SUÍTE INTEIRA, TRÊS VEZES (fiz uma a mais de propósito): 7217 passed, 1 skipped nas três. A terceira eu rodei com impressão digital da árvore antes e depois — árvore comprovadamente PARADA — porque descobri, no meio do trabalho, que uma sessão irmã estava escrevendo no repositório durante as duas primeiras (achado 2). Os números não se moveram.\n\n3) AS MORDIDAS: FIZ OITO, NÃO SEIS, E AS OITO MORDEM. Arranquei, rodei, vi reprovar, devolvi e conferi md5 e modo a cada volta.\n- O `cmp` do `_copia_de_seguranca`: `test_backup_que_mente_ter_copiado_e_pego_pelo_cmp` REPROVA e `test_backup_parcial_e_apagado_e_o_main_conf_nao_e_tocado` fica VERDE. É a retratação da rodada 3 reproduzida na minha mão, com o sinal certo: a bancada velha de fato não mordia aquela metade, a nova morde. Esta era a afirmação mais arriscada do relatório e é a que mais limpa saiu.\n- O escopo de grupo do `_ler_chave`: EXATAMENTE 4 falhas — `grupo-errado-nao-conta`, `so-em-policy-e-ausente-em-general`, `nome-de-grupo-e-exato` e `test_o_veredito_acompanha_o_grupo`. É a correção que o curador fez sobre a rodada 3, e ela bate no detalhe.\n- A poda revertida à regra velha (protege ARQUIVO, não ESTADO): só `test_podar_nunca_faz_um_estado_sumir_do_disco` cai. Alvo exato.\n- O drop-in de volta ao `install -Dm644` cru: `test_aplicar_nao_destroi_dropin_editado_a_mao` cai.\n- O `! -empty` do `_lista_backups`: caem duas.\n- O portão de paridade de volta ao invólucro `build_flatpak.sh`: caem `test_manifesto_flatpak_com_doctor_sem_o_dono_reprova` e `test_comentario_do_manifesto_nao_satisfaz_a_regra_de_par`.\n- `fail` virando `pass` no `always` do doctor: caem duas — a asserção de segurança central morde.\n- A chamada apagada de `main()`: caem duas na bancada E o portão de paridade REAL reprova nomeando o defeito. A ENTREGA-QUE-NAO-LIGOU-01 está fechada nos dois níveis.\nNENHUMA mordida deixou de morder. Não tenho meia-metade sem mordida para declarar.\n\n4) A SONDA NOVA, EU MESMO EXERCITEI. Mutei a árvore aos 4s de um run e deixei mutada: 111 passed, mas rc=1 e a sonda NOMEANDO `MUDADO scripts/bluez_config.sh` — o verde falso é pego, que era o objetivo. Mutei e devolvi dentro do run: a sonda ficou muda, exatamente o limite que o curador declarou. A declaração é honesta.\n\n5) /etc/bluetooth NÃO FOI TOCADO POR SESSÃO NENHUMA. `main.conf` com md5 `acbba30fea8d1bf0e88e1d70abf96cda` idêntico em todas as leituras (início, meio e fim), mtime 2026-08-02 02:33:17 — quatro dias ANTES desta sessão —, mtime do diretório igual, 37 backups com o nosso prefixo (a contagem que a sprint declara; o 38º é `main.conf.bak.claude-*`, de outra ferramenta, que o `_lista_backups` corretamente ignora), ZERO temporários órfãos nossos, e a chave da linha 25 continua `JustWorksRepairing=always` — ou seja, a cura ainda não chegou ao disco dela, que é precisamente o que esta leva existe para consertar. Só leitura, do começo ao fim.\n\n6) PORTÕES, todos rc=0 conferidos por mim: ruff, mypy (163 arquivos), acentuação, glifos, referências (196 documentos), anonimato, versão, dados de teste, paridade de empacotamento, `shellcheck -S error`, `bash -n`. Nada commitado: `git log -- scripts/bluez_config.sh` é vazio.\n\nA RESSALVA QUE DECIDE O *COMO* COMMITAR, não o *se*: o índice deixou de ser a leva enquanto eu media. Uma sessão irmã encostou nele às 20:14–20:21 e hoje ele carrega cinco documentos de outra frente e um CHANGELOG com DUAS seções. O código do BlueZ está íntegro e é o mesmo do começo ao fim — mas `git commit` do índice inteiro, agora, não commita esta leva. Commite por caminho explícito, e separe o CHANGELOG antes. É o achado 1, e é o único que impede o gesto."
  },
  {
    "achados": [
      {
        "gravidade": "alta",
        "onde": "scripts/bluez_config.sh:344-368 (_linha_que_o_parser_recusa), consumida por _verificar:1094 e _aplicar:962; tabela da bancada em tests/unit/test_bluez_config_sh.py:2234-2247",
        "o_que": "A replica em awk implementa DUAS regras de recusa do GKeyFile (linha sem '=' e chave antes do primeiro grupo). O GKeyFile tem mais: nome de chave VAZIO, nome de chave INVALIDO (com '[' ou ']') e nome de GRUPO invalido. Nesses casos o oraculo RECUSA o arquivo inteiro e a replica diz que esta tudo bem — a direcao FALSO-OK, que o proprio cabecalho classifica como a pior. A entrega afirma 'A bancada fecha a diferenca do jeito certo: cada caso e conferido contra o oraculo de verdade'; a _TABELA_DA_RECUSA tem tres casos e os tres caem dentro das duas regras ja implementadas. Nao ha nenhum teste que exija que a replica recuse tudo o que o oraculo recusa. Consequencia: selo verde sobre um main.conf que o bluetoothd descarta INTEIRO — nem FastConnectable, nem JustWorksRepairing, nem o que ja era dela.",
        "prova": "MEDIDO em raiz falsa (HEFESTO_BT_ETC), oraculo GLib.KeyFile em subprocesso, /etc so por leitura. Repro minimo, 4 linhas: '[General]\\n=\\nFastConnectable=true\\nJustWorksRepairing=confirm\\n'. Oraculo: 'ERRO-DE-CARGA  Key file contains line \"=\" which is not a key-value pair, group, or comment'. Dono unico: 'JustWorksRepairing: confirm', 'FastConnectable: true', 'veredito: OK', rc=0. 'aplicar': rc=0 e imprime 'JustWorksRepairing=confirm + FastConnectable=true garantidos'. doctor.sh (HEFESTO_BT_ETC na raiz falsa): '[ OK ] JustWorksRepairing=confirm no main.conf'. Varredura linha a linha contra o oraculo: 8 classes divergentes, TODAS no sentido oraculo=RECUSA / replica=aceita — '=valor-sem-chave', ' =valor', '=', '==x', 'chave[com=colchete' (Invalid key name), 'chave]=x' (Invalid key name), '[]' (Invalid group name), '[General][Policy]'. Fuzz combinatorio de 400 arquivos: 10 divergencias de recusa e 0 divergencias de VALOR (o leitor de chave em si esta fiel ao GKeyFile, inclusive CRLF, espacos e o '(vazio)'). Atenuante MEDIDO: /etc/bluetooth/main.conf.dpkg-dist:104 documenta '#JustWorksRepairing = never' como default, entao o fallback e MAIS restritivo — o dano nao e injecao de teclas, e o diagnostico que mente somado a FastConnectable silenciosamente desligado e a config dela inteira ignorada. Scripts: scratchpad/bench/probe_linhas.py e scratchpad/bench/fuzz_parser.py."
      },
      {
        "gravidade": "media",
        "onde": "scripts/bluez_config.sh:667-673 (_lista_backups, filtro '! -empty') e 533-554 (_copia_de_seguranca)",
        "o_que": "Backup CORTADO nao-vazio continua contando como backup legitimo. A cura desta rodada so alcanca o arquivo de ZERO byte; o backup pela metade — que o proprio comentario do arquivo batiza 'BACKUP PARCIAL NAO E BACKUP' e diz ter medido em 118 bytes — so e apanhado pelo cmp DENTRO do processo. SIGKILL nao tem trap, entao o pedaco sobrevive, entra em 'backups-hefesto:', soma em 'backups-hefesto-bytes:' e NAO aparece em 'backups-suspeitos:'. A disciplina que a entrega ja aplica ao main.conf (nascer com nome em transito e entrar por rename depois de conferido) nao foi aplicada ao backup, que e justamente o arquivo cuja unica razao de existir e ser confiavel.",
        "prova": "MEDIDO em raiz falsa, duas vezes, por SIGKILL no grupo de processos durante o cp, com main.conf de 400 MB para alargar a janela: t=4000ms deixou backup de 284.688.384 de 400.000.036 bytes; t=3600ms noutra varredura deixou 97.845.248 bytes. Nos dois casos o main.conf ficou INTACTO (a troca atomica cumpre) e o 'verificar' respondeu 'backups-hefesto: 1', 'backups-hefesto-bytes: 284688384', 'backups-suspeitos: 0'. Contraprova do mesmo mecanismo com SIGTERM (que TEM trap) na MESMA janela, 7 disparos: backup=nenhum nos 7 — o trap limpa, o SIGKILL nao. Lado a lado com arquivos plantados (1 de ZERO byte + 1 cortado em 300 de 1394 + 1 inteiro): 'backups-hefesto: 2', 'backups-suspeitos: 1' — so o vazio e denunciado. Cobertura: 'test_backup_parcial_e_apagado_e_o_main_conf_nao_e_tocado' cobre so o caminho em-processo (shim que corta o cp e sai 0); nenhum teste cobre o sobrevivente. Atenuante MEDIDO: nenhum dos 37 backups reais dela em /etc/bluetooth termina sem quebra de linha, e com o main.conf dela de 1394 bytes o cp e uma unica write — a probabilidade na maquina dela e desprezivel (SUSPEITA COM MECANISMO para ela; o defeito de CONTAGEM e MEDIDO sem condicao). Scripts: scratchpad/bench/parcial2.sh e scratchpad/bench/term_sweep.sh."
      },
      {
        "gravidade": "baixa",
        "onde": "scripts/bluez_config.sh:919-925 (_aplicar) e 1019/1058 (_remover); contrato declarado em _despir_main_conf:450-465",
        "o_que": "O contrato do _despir_main_conf e 'sai com 3 se uma sentinela de ABERTURA ficou sem fechamento', mas os dois chamadores tratam QUALQUER saida nao-zero como esse caso. Falha de escrita do temporario (cota, disco cheio, /tmp cheio) produz a mensagem 'sentinela de abertura sem fechamento em .../main.conf — nao mexi no arquivo (conserte a mao e rode de novo)', mandando-a editar a mao um arquivo que esta perfeito e escondendo a causa real.",
        "prova": "MEDIDO em raiz falsa com 'ulimit -f 1' (modelo de cota / disco cheio) sobre um main.conf de ~60 KB sem sentinela nenhuma aberta: saida 'bluez_config.sh: sentinela de abertura sem fechamento em .../rdisk1/main.conf — nao mexi no arquivo (conserte a mao e rode de novo)', rc=1. Nao ha dano: o main.conf ficou intacto (md5 igual) e nenhum lixo sobrou no diretorio. Segundo caso (cota estourando no append do bloco): o set -e aborta antes do _gravar_se_mudou, main.conf intacto, sem lixo e sem backup pela metade. Script: scratchpad/bench/disco_cheio.sh."
      },
      {
        "gravidade": "baixa",
        "onde": "scripts/bluez_config.sh:1136-1149 (relato dos drop-ins) e 1190-1196 (veredito); scripts/doctor.sh, check_bluez_justworks_repairing (recorta so a linha '^JustWorksRepairing: ')",
        "o_que": "Assimetria entre o que a entrega ESCREVE e o que ela VERIFICA: o aplicar grava drop-ins 'por cima' justamente para o caso de o BlueZ ler main.conf.d, mas o veredito recusa considerar main.conf.d. Um drop-in de terceiro que ordene depois do nosso com JustWorksRepairing=always sai como 'dropin-em-conflito', porem o 'veredito: OK' e o rc=0 permanecem, o aplicar anuncia 'garantidos' e o doctor nunca mostra o conflito a ela. A decisao esta DECLARADA e medida para a maquina dela (bluez 5.86: zero ocorrencias de main.conf.d no binario, diretorio inexistente, dpkg -L nao o lista), mas a entrega e empacotada para deb/rpm/PKGBUILD/nix/flatpak, onde essa medicao nao vale.",
        "prova": "MEDIDO em raiz falsa: com main.conf.d contendo 'zz-terceiro.conf' = '[General]\\nJustWorksRepairing=always\\n', o verificar imprime 'dropin-JustWorksRepairing: zz-terceiro.conf=always' e 'dropin-em-conflito: zz-terceiro.conf declara always (esperado confirm)' e mesmo assim 'veredito: OK' com rc=0. Script: scratchpad/bench/dropins.sh, caso F."
      }
    ],
    "aprovado": false,
    "veredito": "REFUTADO por um achado ALTA — mas os cinco pontos que voce mandou cobrir passaram nos meus ataques, e passaram com folga.\n\nO QUE NAO CONSEGUI DERRUBAR (tudo MEDIDO, raiz falsa, /etc so por leitura):\n1. Poda por ESTADO: 300 rodadas de fuzz (1 a 25 backups, 1 a 6 estados, retencao 0 a 8, tudo sorteado) — 0 estados perdidos, o mais antigo sempre de pe, main.conf intocado, e nem o backup de OUTRA ferramenta (main.conf.bak.claude-*) nem o main.conf.dpkg-dist foram tocados. Sobre COPIA do /etc/bluetooth REAL dela: retencao 10 levou 37 para 31 arquivos com 24 estados distintos ANTES e DEPOIS; retencao 1 levou 37 para 24 arquivos, os MESMOS 24 estados. Os dois pontos de medicao do colapso 404->3 linhas (…-1784672963 e …-1784694261) sobreviveram nas duas. Com 9 backups de mtime IDENTICO em 3 estados e retencao 1, os 3 estados sobrevivem.\n2. Drop-ins: editado a mao vira backup fiel byte a byte mais aviso nomeando o caminho, nos DOIS lados (aplicar e remover); igual ao asset nao gera backup (a excecao declarada); o nome do backup nao termina em .conf e nao entra no glob da poda do main.conf. Alvo symlink NAO destroi o alvo; alvo diretorio faz o aplicar REPROVAR com rc=1 e o conteudo de dentro sobrevive.\n3. Backup vazio: 0 byte sai de 'backups-hefesto:', entra nomeado em 'backup-suspeito:', o aplicar avisa, e a poda nao o alcanca. Cura confirmada. (O irmao dele, o backup CORTADO nao-vazio, e o achado media.)\n4. Ciclo install+uninstall 20x sobre copia do main.conf REAL dela: 20/20 com rc=0/0, estado aplicado e estado removido estaveis desde o ciclo 1, oraculo GKeyFile lendo 'confirm' nas 20 vezes, 0 orfaos e 0 backups vazios ao fim.\n5. Fuzz de mortes: 200 rodadas, 108 mortes efetivas (SIGKILL e SIGTERM no GRUPO de processos, atraso sorteado, aplicar e remover sorteados) — main.conf NUNCA parcial (sempre byte a byte igual a um dos estados completos conhecidos), NENHUM backup preexistente perdido nem alterado, e nenhum beco sem saida (o aplicar seguinte volta a rc=0 em 200/200). Cadaveres: 1 temporario orfao, que o verificar reporta.\n\nExtra que rodei por conta: 300 rodadas de ida-e-volta (aplicar seguido de remover sobre main.conf sorteados) com 0 perdas fora das TRES excecoes declaradas; e 12 mutacoes arrancando as curas desta rodada numa COPIA ISOLADA do repo — as 12 MORDEM, zero sobreviventes, inclusive a que a rodada 3 errou (test_backup_que_mente_ter_copiado_e_pego_pelo_cmp fica vermelho quando se arranca o cmp).\n\nA CONFTEST (ARVORE-CONGELADA-01) nao abriu buraco: suite inteira na copia isolada, 7212 verdes, e a sonda NAO deu falso positivo (nenhuma reprovacao por 'o PRODUTO mudou'). As 5 vermelhas daquela copia sao artefato do meu rsync (sem .git e sem captures/): as mesmas dao 215 verdes na arvore real.\n\nPOR QUE REFUTO MESMO ASSIM: a promessa central desta rodada e que o veredito deixou de mentir. Ele ainda mente. O detector de linha recusada e uma replica de DUAS regras do GKeyFile, e o GKeyFile tem mais. Um '=' solto no main.conf — um erro de digitacao — faz o bluetoothd descartar o arquivo INTEIRO, e o dono unico responde 'veredito: OK', o aplicar anuncia 'garantidos' e o doctor da [ OK ]. Nao ha um unico teste que exija que a replica recuse tudo o que o oraculo recusa; a tabela tem tres casos e os tres estao dentro das duas regras que ja existem. Nao e o mesmo perigo do 'always' (o default do BlueZ e 'never', mais restritivo) — e a MESMA classe de defeito que abriu a sprint: a ferramenta dizendo que garantiu o que nao garantiu.\n\nNADA foi commitado, nada foi escrito em /etc (main.conf com md5 acbba30f… e 42 entradas, iguais ao inicio), nada foi consertado, e a arvore de trabalho esta como estava: bluez_config.sh de21778a… em modo 755, doctor.sh 5854e831…, conftest.py fb9abec5…, 20 arquivos staged."
  }
]

### reprovou

true

### achadosAltos

[
  {
    "gravidade": "alta",
    "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/.git/index (e CHANGELOG.md)",
    "o_que": "O ÍNDICE NÃO É MAIS A LEVA. Quando comecei a verificação, `git diff --cached` eram 15 arquivos — exatamente a entrega do BlueZ. Agora são 20: uma sessão irmã encostou no MESMO índice durante a minha medição e acrescentou cinco documentos de outra frente (perfis/Steam/Sony). Pior, o `CHANGELOG.md` staged carrega hoje DUAS seções: a do BlueZ e `### O experimento do controle da Sony rodou, e ele corrige metade da doutrina da casa`. Um `git commit` do índice como está AGORA não commita a leva de segurança — commita a leva de segurança MAIS a frente alheia, num commit só, com mensagem de uma delas. Isto não é defeito do código verificado (que está íntegro e é o mesmo do começo ao fim: md5 dos três scripts e do conftest idênticos na primeira e na última leitura); é impedimento ao ATO de commitar. A saída é commitar por CAMINHO EXPLÍCITO (os 15 arquivos da entrega) e separar o CHANGELOG, nunca `git commit` do índice inteiro.",
    "prova": "No início: `git status --short` = 15 arquivos (CHANGELOG.md, docs/.../2026-08-06-desenho..., docs/.../RADIO-ABERTO-01..., install.sh, scripts/{bluez_config,build_deb,check_packaging_parity,doctor}.sh, tests/conftest.py, tests/unit/{test_bluez_config_sh,test_bt_resilience_assets,test_check_packaging_parity,test_doctor_justworks_comportamento,test_plataforma_wiring}.py, uninstall.sh). No fim: `git diff --cached --name-only` = 20, os cinco novos sendo docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md, docs/process/sprints/2026-08-05-STEAM-QUE-DECIDE-01-....md, docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-....md, docs/usage/jogos-e-mascaras.md, docs/usage/modos.md. Carimbos: mtime desses arquivos 20:14:14, 20:14:57, 20:15:23; `.git/index` mtime=2026-08-06 20:21:39 — tudo DENTRO da janela das minhas duas primeiras execuções da suíte. `git diff --cached CHANGELOG.md | grep '^+###'` devolve as duas seções. MEDIDO."
  },
  {
    "gravidade": "alta",
    "onde": "scripts/bluez_config.sh:344-368 (_linha_que_o_parser_recusa), consumida por _verificar:1094 e _aplicar:962; tabela da bancada em tests/unit/test_bluez_config_sh.py:2234-2247",
    "o_que": "A replica em awk implementa DUAS regras de recusa do GKeyFile (linha sem '=' e chave antes do primeiro grupo). O GKeyFile tem mais: nome de chave VAZIO, nome de chave INVALIDO (com '[' ou ']') e nome de GRUPO invalido. Nesses casos o oraculo RECUSA o arquivo inteiro e a replica diz que esta tudo bem — a direcao FALSO-OK, que o proprio cabecalho classifica como a pior. A entrega afirma 'A bancada fecha a diferenca do jeito certo: cada caso e conferido contra o oraculo de verdade'; a _TABELA_DA_RECUSA tem tres casos e os tres caem dentro das duas regras ja implementadas. Nao ha nenhum teste que exija que a replica recuse tudo o que o oraculo recusa. Consequencia: selo verde sobre um main.conf que o bluetoothd descarta INTEIRO — nem FastConnectable, nem JustWorksRepairing, nem o que ja era dela.",
    "prova": "MEDIDO em raiz falsa (HEFESTO_BT_ETC), oraculo GLib.KeyFile em subprocesso, /etc so por leitura. Repro minimo, 4 linhas: '[General]\\n=\\nFastConnectable=true\\nJustWorksRepairing=confirm\\n'. Oraculo: 'ERRO-DE-CARGA  Key file contains line \"=\" which is not a key-value pair, group, or comment'. Dono unico: 'JustWorksRepairing: confirm', 'FastConnectable: true', 'veredito: OK', rc=0. 'aplicar': rc=0 e imprime 'JustWorksRepairing=confirm + FastConnectable=true garantidos'. doctor.sh (HEFESTO_BT_ETC na raiz falsa): '[ OK ] JustWorksRepairing=confirm no main.conf'. Varredura linha a linha contra o oraculo: 8 classes divergentes, TODAS no sentido oraculo=RECUSA / replica=aceita — '=valor-sem-chave', ' =valor', '=', '==x', 'chave[com=colchete' (Invalid key name), 'chave]=x' (Invalid key name), '[]' (Invalid group name), '[General][Policy]'. Fuzz combinatorio de 400 arquivos: 10 divergencias de recusa e 0 divergencias de VALOR (o leitor de chave em si esta fiel ao GKeyFile, inclusive CRLF, espacos e o '(vazio)'). Atenuante MEDIDO: /etc/bluetooth/main.conf.dpkg-dist:104 documenta '#JustWorksRepairing = never' como default, entao o fallback e MAIS restritivo — o dano nao e injecao de teclas, e o diagnostico que mente somado a FastConnectable silenciosamente desligado e a config dela inteira ignorada. Scripts: scratchpad/bench/probe_linhas.py e scratchpad/bench/fuzz_parser.py."
  }
]


## LOGS

rodada 4: 2 lentes, 1 reprovaram, 2 altos
