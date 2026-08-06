# CANÁRIO-FS-01 — a suíte escrevia no `$HOME` de verdade

- **Achado em:** 04/08/2026, dentro da mesma pergunta dela que originou a
  [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md):
  *"como sabemos se algum **teste** ou algo a mais corrompeu algo?"*
- **Estado:** **CURA APLICADA**, com testes que mordem; **o limite do
  instrumento está medido e registrado abaixo — ele não cobre a classe inteira**
- **Gravidade:** ALTA — a suíte roda na máquina dela, ao lado do daemon e da
  janela dela, e havia caminho de **escrita** apontando para a configuração real
- **Causa-raiz:** **PROVADA no código** — `Path.home()` avaliada no **import**,
  antes de qualquer `monkeypatch`
- **Estudo que a origina:**
  [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  (D-35, D-37, DIV-11)
- **Irmã de leva:**
  [SUÍTE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
  — mesmo defeito de fundo (a suíte tocando o sistema vivo), outro recurso.
  Esta paga parcialmente o item 1 da lista *"ainda não medido"* daquela

---

## O sintoma

Ela perguntou se um teste podia ter corrompido os perfis dela. A pergunta parece
paranoia até alguém olhar o que a suíte isola de fato:

| isolado pela `_hefesto_fake_env` | **não** isolado |
|---|---|
| `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_STATE_HOME` | **`HOME`** |
| `HEFESTO_DUALSENSE4UNIX_FAKE=1`, seed de presets, socket do broker | — |

**Grau: MEDIDO.** Não há **um único** `setenv("HOME")` no autouse de
`tests/conftest.py`. Só quatro arquivos de teste protegem o `HOME` por conta
própria.

## A causa-raiz: constante de módulo é avaliada antes de qualquer fixture

Duas linhas, as duas com a mesma forma:

```python
# integrations/storm_doctor.py — LEITURA
_ALLOWLIST_PATH = Path.home() / ".config" / "hefesto-dualsense4unix" / "steam_input_apps.txt"

# app/actions/emulation_actions.py — atributo de classe; DIRETÓRIO DE ESCRITA
_WP_DROPIN_DIR = Path.home() / ".config" / "wireplumber" / "wireplumber.conf.d"
```

`Path.home()` lê o `HOME` **no momento em que a linha roda**. Numa constante de
módulo, isso é **o import** — antes de a primeira fixture existir. Nenhum
`monkeypatch` de `HOME` alcança um valor que já foi calculado.

Consequências, uma por linha:

- **`_ALLOWLIST_PATH`** apontava para o arquivo **real** dela (721 bytes). É
  leitura — mas o resultado de **três arquivos de teste** passava a depender,
  sem ninguém saber, do conteúdo do disco dela. Um teste cujo veredito muda
  conforme o que a dona da máquina configurou não é um teste;
- **`_WP_DROPIN_DIR`** é, em produção, **diretório de escrita**: o botão do
  microfone cria e apaga os drop-ins `52-` e `53-` ali. Um teste que
  exercitasse esse caminho escreveria na configuração real do WirePlumber da
  máquina. **Grau: SUSPEITA COM MECANISMO** — o caminho de escrita foi lido no
  código, e não há registro de que algum teste o tenha exercitado.

## Por que um portão, e não só o conserto das duas linhas

Porque a pergunta dela não era sobre essas duas linhas. Era **"como sabemos?"**.
Consertar duas constantes responde *"estas duas não"*. O que faltava era um
instrumento capaz de responder **"nenhuma"** — e de continuar respondendo depois
que todo mundo esquecer esta sprint.

## A cura aplicada

### 1. O canário de sessão, em `tests/conftest.py:333-521`

Dois hooks de sessão, fora de qualquer fixture:

- **`pytest_sessionstart`** (`:473`) fotografa três árvores **reais** do `$HOME`:

  ```
  ~/.config/hefesto-dualsense4unix
  ~/.config/wireplumber
  ~/.local/share/hefesto-dualsense4unix
  ```

- **`pytest_sessionfinish`** (`:496`) refaz a foto, e se algo mudou **reprova a
  sessão** (`session.exitstatus = 1`) imprimindo a lista `CRIADO` / `APAGADO` /
  `MUDADO`, com a instrução de como caçar a causa.

Cada arquivo entra na foto como **`(mtime_ns, tamanho, sha256)`**
(`_resumo_do_arquivo:406`, `_fotografar_arvore:424`), e o delta compara **só
tamanho e resumo** (`_deltas_do_canario:452`).

**O sha256 não é zelo — é um desenho refutado por execução.** A primeira versão
comparava `(mtime_ns, size)` e **acusou 15 falsos positivos na estreia**, todos
`.lock`, tocados pelo daemon e pela janela **dela**, vivos ao lado da suíte (o
`filelock` toca o arquivo a cada aquisição, inclusive **para ler** —
`loader.py:499-502`). *Um portão que grita no primeiro dia é um portão que
alguém desliga no segundo.* O registro dessa refutação é o DIV-11 do estudo, e
fica.

Três detalhes de desenho, cada um com defeito por trás:

1. **`_CANARIO_ARMADO`** (`:384`) — selo que só vira `True` depois da foto
   inicial. Sem ele, uma sessão que começou com o canário desligado e terminou
   com ele ligado compararia contra um dicionário vazio e acusaria **todo**
   arquivo do `$HOME` de ter nascido durante a suíte. É o alarme mais falso que
   existe;
2. **`HEFESTO_SEM_CANARIO_FS=1`** (`:375`) — escotilha. Existe para não obrigar
   ninguém a **comentar código** quando o daemon está de pé mexendo no
   `session.json` ao lado. Uma escotilha declarada é melhor que um portão
   contornado no escuro;
3. **erros de permissão e diretórios ausentes são pulados em silêncio** —
   máquina limpa (CI) dá foto vazia, sem exceção. O canário mede o que consegue
   ver, e ver menos nunca pode derrubar a suíte por si só.

**Custo medido em 05/08:** 93 arquivos, 356 KB no total. O limite de resumo é
4 MB por arquivo (`:388`) e nada nos diretórios vigiados chega perto.

### 2. As duas constantes viraram função — decisão dela

Decisão dela, registrada nas duas docstrings: *"preciso que as constantes
apontem pros arquivos reais"*. Em produção o `HOME` é o mesmo do começo ao fim,
então **mover para função não muda nada lá** — e devolve à suíte a chance de
desviar o caminho.

| antes | depois |
|---|---|
| `storm_doctor._ALLOWLIST_PATH` (constante) | **`storm_doctor._allowlist_path()`** (`:34`), consumida em `:60` |
| `EmulationActionsMixin._WP_DROPIN_DIR` (atributo de classe) | **`EmulationActionsMixin._wp_dropin_dir()`** (`:726`, `@staticmethod`), consumida em `:751` |

O chamador de teste acompanhou: `tests/unit/test_steam_input_ponteiros.py:193`
passou a fazer `monkeypatch.setattr(sd, "_allowlist_path", lambda: …)`, com o
comentário que explica o porquê — *"a allowlist real da máquina não pode decidir
o resultado do teste"*.

**E o canário continua**, e não por desconfiança destas duas: ele cobre o que
ninguém mapeou — subprocessos, `systemctl`, `uinput`, e a próxima constante que
alguém escrever sem pensar nisso.

## O resultado

**Grau: MEDIDO.** Com o canário armado, a suíte inteira (**6968 passed, 1
skipped**) terminou **sem um único delta** nos três diretórios.

**Hoje nenhum teste escreve no `~/.config` dela.** É a resposta direta à
pergunta dela — e, pela primeira vez, é uma resposta medida em vez de uma
opinião.

Isso converge com a prova negativa que já existia (D-35): as duas janelas em que
a suíte rodou na madrugada estão **vazias** de mtimes nos perfis dela, e os
arquivos alterados têm mtime de **77 minutos depois** da segunda janela. **Foi a
janela que escreveu, não a suíte.**

## Os testes que mordem

`tests/unit/test_conftest_canario_fs.py` — 9 casos, todos contra um `$HOME` de
mentira (`_lar_falso`, `:34`) montado com a árvore que o canário vigia.

| arrancar isto | reprova |
|---|---|
| a comparação de conteúdo (`_deltas_do_canario`) | `test_escrita_em_perfil_real_vira_delta` |
| o `session.exitstatus = 1` do `pytest_sessionfinish` | `test_sessionfinish_reprova_a_sessao_com_delta` — sem ele o relatório existe e **não é portão** |
| o `not _CANARIO_ARMADO` da guarda | `test_canario_desarmado_nao_acusa_o_home_inteiro` — a sessão reprova com a árvore inteira na lista |
| voltar a comparar a tupla inteira, com `mtime_ns` | `test_mtime_sozinho_nao_acusa_ninguem` — é a medição dos 15 `.lock` virada em asserção |

Mais quatro que fecham o contrato pelo outro lado: `CRIADO`/`APAGADO` contam
(`test_arquivo_novo_e_apagado_tambem_contam`), a suíte hermética deixa o canário
**invisível** (`test_sessionfinish_calado_quando_nada_mudou`), a escotilha
desliga de verdade (`test_escotilha_de_saida_desliga_o_canario`) e uma máquina
limpa não estoura (`test_home_sem_a_arvore_nao_estoura`).

Verificado em 05/08: **34 verdes** rodando este arquivo junto com os dois da
PERFIL-SEM-RASTRO-01.

## O LIMITE MEDIDO — e ele é grande

**Este canário é dinâmico e detecta ESCRITA, não LEITURA.**

Consequência que precisa estar escrita com todas as letras: **o `_allowlist_path`
jamais teria sido pego por ele.** Ele lia o arquivo real dela e não mudava um
byte — foto inicial e final idênticas, canário calado, suíte verde, e o
resultado de três arquivos de teste continuando a depender do disco dela.

**A classe *"o teste LÊ o `$HOME` de verdade"* segue inteiramente descoberta.**
A cura das duas constantes foi feita **por leitura de código**, não por
detecção — e nada garante que a próxima seja encontrada do mesmo jeito.

### As quatro `Path.home()` restantes em `src/`, conferidas uma a uma

O briefing desta sprint dizia que havia *"4 outras `Path.home()` avaliadas em
nível de módulo"*. **Conferi as quatro em 05/08, e a afirmação está errada como
enunciada** — a correção fica registrada em vez de a afirmação ser apagada
(regra da casa). O que existe de fato:

| caminho | forma real | veredito |
|---|---|---|
| `gui/widgets/button_glyph.py:74` | dentro de `_resolver_dir_glyphs()`, **mas o resultado é congelado no import** por `GLYPHS_DIR = _resolver_dir_glyphs()` (`:96`) | **congelada no import, uma camada indireta.** Leitura pura (procura de diretório de glifos); nenhuma escrita |
| `utils/i18n.py:61` | dentro de `_candidate_locale_dirs()`, chamada em `:85` e `:119` | **resolve na chamada.** Mas o `HOME` não é isolado, então **lê o `$HOME` real dela** em tempo de teste |
| `core/system_check.py:37` | dentro de `_wireplumber_hijacks_mic()` | **resolve na chamada**, e **lê o arquivo real** `~/.local/state/wireplumber/default-nodes` |
| `daemon/subsystems/plugins.py:61` | dentro de `_default_plugins_dir()`, e **só depois de tentar `XDG_CONFIG_HOME`** | **efetivamente isolada**: a suíte define `XDG_CONFIG_HOME`, então o `Path.home()` nunca é alcançado sob teste |

**A leitura correta dos números:** o problema não é "quatro constantes de
módulo". É que **três destas quatro leem o `$HOME` real dela sob teste** — uma
por congelamento no import, duas por o `HOME` simplesmente não ser isolado. E
**nenhuma das três seria vista pelo canário**, porque nenhuma escreve.

**Grau de tudo nesta tabela: MEDIDO**, por leitura dos quatro arquivos em 05/08.

### O que fecharia a classe, e por que não entrou aqui

Isolar o `HOME` no autouse resolveria as três de uma vez. **Não entrou nesta
sprint**, e a razão é honesta: o `HOME` é lido por muito mais coisa que os
diretórios XDG (Steam, Proton, WirePlumber, glifos, locale), e trocá-lo por um
`tmp_path` em toda a suíte é uma mudança de superfície larga, com risco de
vermelhos difusos, feita numa árvore em que agentes irmãos escreviam em
paralelo. **É entrega própria, e precisa de medição própria.**

## O que fica ABERTO

- **isolar o `HOME` no autouse** — a única cura que fecha a classe da leitura;
- **`utils/i18n.py:61` e `core/system_check.py:37`** continuam lendo o `$HOME`
  real sob teste;
- **`gui/widgets/button_glyph.py:96`** continua congelando no import — leitura
  pura, dano baixo, forma errada;
- **o canário não vê leitura**, e é o limite estrutural do desenho. Um segundo
  instrumento (por exemplo, `atime` ou um `Path` instrumentado) é ideia, **não
  é medição** — **grau: SEM PROVA**, e não deve ser tratada como plano;
- **o canário não vigia fora das três árvores.** `~/.steam`, `~/.local/state` e
  `~/.config/systemd` estão de fora **por decisão de custo**, não por serem
  seguros;
- **rodar a suíte inteira de novo, com `git add -A` antes.** Os 6968 verdes
  foram medidos em árvore viva, com agentes irmãos escrevendo em paralelo.

## Nota datada — o que caducou

**05/08/2026.** A seção 5.7 do estudo consolidado, sob *Hermeticidade*, afirma:
*"`_ALLOWLIST_PATH` … e `_WP_DROPIN_DIR` … continuam constantes de módulo
avaliadas no import — **não foram movidas de propósito**, por serem arquivos de
agentes irmãos e porque `tests/unit/test_steam_input_ponteiros.py:193`
monkeypatcha uma delas pelo nome."*

**Caducou no mesmo dia.** As duas **foram** movidas, por decisão explícita dela,
e o `test_steam_input_ponteiros.py:193` foi atualizado junto. A frase do estudo
fica onde está — era verdade quando foi escrita, e o registro de que deixou de
ser é esta nota.

## Relacionado

- [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  — D-35 (a prova negativa), D-37 (o `HOME` não isolado), DIV-11 (o desenho
  refutado), 5.4
- [PERFIL-SEM-RASTRO-01](2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md)
  — a outra metade da mesma pergunta dela: *"foi a janela?"*
- [SUÍTE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
  — a suíte tocando o sistema vivo por outro recurso; a E4 dela pede exatamente
  um portão desta forma
- [TESTE-HONESTO-01](2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md)
  — *cobertura falsa é pior do que cobertura ausente*, que é o mesmo princípio
  aplicado ao veredito de um teste que depende do disco da mantenedora
