# PERFIL-SEM-RASTRO-01 — o perfil mudava e nada registrava quem mudou

- **Achado em:** 05/08/2026, de madrugada, quando ela perguntou *"como sabemos
  se algum teste ou algo a mais corrompeu algo?"* — e a resposta honesta foi
  **não dá para saber**
- **Estado:** **CURA APLICADA**, com testes que mordem; **dívida de uso e uma
  lacuna de teste registradas abaixo, as duas em aberto**
- **Gravidade:** ALTA — não é um defeito de comportamento, é a **ausência do
  instrumento** que decide todos os outros. Enquanto ela não existia, três
  agentes independentes chegaram a três culpados diferentes para o mesmo `191`
- **Causa-raiz:** **PROVADA no código** (`os.replace` sem cópia anterior; zero
  linhas de journal na gravação) e **confirmada por medição negativa** no disco
  dela
- **Estudo que a origina:**
  [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  (D-36, DIV-1)
- **Índice:** **NENHUM.** A faixa de perfis está órfã desde 30/07 — é o item 5
  dos bloqueantes de processo do estudo, e esta sprint nasce sem casa de
  propósito, para que a falta apareça

---

## O sintoma

Os perfis dela foram encontrados corrompidos: `sackboy_nativo` com
`match: {"type": "any"}` e prioridade **191**, quando de fábrica era
`criteria: steam_app_1599660` com prioridade 80. O perfil do jogo perdia dentro
do próprio jogo e ganhava no desktop inteiro.

A pergunta dela não foi *"conserta"*. Foi **"quem fez isso?"** — e a resposta
tinha de escolher entre três hipóteses vivas:

| tese | quem propôs | o que explicaria o `191` |
|---|---|---|
| A catraca do rodapé | funil de gravação | `10 → 20 → 30 …`, +10 por save |
| O controle deslizante da aba Perfis | integridade | `0–200` é o curso do slider; 191 é o polegar dela parando ali |
| "Novo perfil" com nome existente | prioridades | reproduz `match=any, prio=191, suppress=True` **exatamente** |

**Nenhum dos três podia ser confirmado nem descartado.** O disco só guardava o
resultado.

## A causa-raiz, em duas camadas

### Camada 1 — a versão anterior deixava de existir no mesmo instante

`profiles/loader.py`, `save_profile`, antes desta sprint: montava o payload e
escrevia por cima, com `mkstemp` + `os.replace`. A escrita era **atômica**, o
que protege contra truncamento — e **não protege contra sobrescrita
semanticamente errada**, que é exatamente o que aconteceu. Sem cópia anterior
não há nem conserto (voltar ao que estava) nem perícia (comparar o antes com o
depois).

**Grau: MEDIDO.** O único backup que existia no disco dela
(`backup-20260726-233630/`) é **órfão** — manual, sem criador no repositório
(`scripts/purge.sh:86` e `uninstall.sh:1262` criam um irmão *externo*, outro
diretório). Por sorte, foi a única testemunha do estado pré-corrupção.

### Camada 2 — nem uma linha de journal, e depois o carimbo cego

Gravar perfil era **o único caminho do projeto que mudava o disco da usuária
sem deixar UMA linha dizendo o quê**. Medição: `grep -cE 'footer_|gui_'` no
journal = **0**; e o `stderr` da janela não chega ao journal
([JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md),
`:626-634`: *"zero linhas da janela nos últimos sete dias"*).

E aqui está **o defeito que esta sprint existe para curar**, escrito na sua
forma exata: mesmo depois de emitir a linha, o registro cairia no **basename do
processo** (`sys.argv[0]`) — e **para a janela o basename é sempre o mesmo**.
O rodapé, a aba Perfis, o import e o "Restaurar Default" são quatro gestos
diferentes que produzem quatro escritas diferentes **do mesmo processo, com o
mesmo nome**.

**Foi essa cegueira que impediu, na madrugada de 05/08, decidir se a prioridade
191 do disco dela veio da catraca do rodapé ou do controle deslizante.** As
teses A e B não são distinguíveis por conteúdo — as duas terminam num arquivo
com `priority: 191` —, só por **origem do gesto**. O comentário que registra
isso está em `app/actions/profile_writer.py:109-115`, junto da linha que o cura.

## A cura aplicada

### 1. Histórico versionado, dentro do diretório de perfis

`profiles/loader.py:623-730`:

- `HISTORICO_DIR_NAME = ".historico"` (`:635`) e `HISTORICO_MAX_VERSOES = 10`
  (`:639`);
- `historico_dir(slug, ensure=)` (`:642`) → `profiles/.historico/<slug>/`;
- `_arquivar_versao(slug, bruto)` (`:703`) grava os **bytes** da versão atual
  num arquivo carimbado (`20260805T031500_123456.json`, ordenável
  lexicograficamente, com desempate por sufixo);
- `_podar_historico(destino, manter)` (`:692`) mantém as **10 mais recentes**.

Três decisões, cada uma com motivo:

1. **fica DENTRO de `profiles/`**, e não num diretório irmão: quem faz backup do
   `~/.config` leva o histórico junto. É invisível às varreduras porque todas
   usam `glob("*.json")` não recursivo ou `find -maxdepth 1` — conferido no
   loader, em `doctor.sh:1479` e em `_perfis_inalcancaveis`;
2. **best-effort por contrato** (`:703-730`): falha ao arquivar (disco cheio,
   permissão) loga `profile_backup_failed` e **não impede o save**. A hierarquia
   de danos é essa: nada pode impedir a usuária de salvar o perfil dela. A
   ausência fica visível porque o `profile_salvo` registra `backup=None`;
3. **dez versões, não infinitas**: perfil tem ~1 KB, e dez cobrem uma sessão
   inteira de ajuste fino na janela sem virar depósito.

**Custo medido:** o arquivamento é uma leitura e uma escrita **dentro do
`FileLock` que a gravação já segurava** (`:844-850`). E os mesmos bytes lidos
uma vez servem ao backup **e** ao "antes" do journal — a perícia não custa uma
segunda leitura.

### 2. `restaurar_do_historico` devolve os BYTES, não uma reserialização

`loader.py:890-945`. Valida contra o esquema antes de escrever
(`Profile.model_validate`, `:925`) — lixo guardado não volta ao disco —, mas
escreve `bruto` **como está**, via `_atomic_write_bytes` (`:1007`).

**O porquê, e não é estética:** se a restauração reserializasse, a formatação
mudaria, e comparar o antes com o depois deixaria de provar coisa alguma. Um
instrumento de perícia que altera a prova não é instrumento.

`_atomic_write_bytes` passou a ser o único ponto de escrita: `_atomic_write_json`
(`:1002`) agora só codifica e delega. Mesmo `mkstemp` + `fsync` + `os.replace` de
antes, num lugar só.

E a versão **atual** é arquivada antes de ser pisada (`:933-935`) — restaurar por
engano também tem volta.

### 3. O journal de toda gravação

`_registrar_gravacao` (`:855-887`) emite **`profile_salvo`** com:

| campo | para quê |
|---|---|
| `nome`, `arquivo`, `criado` | qual perfil, e se nasceu agora |
| `match_antes` / `match_depois` | `criteria → any` **é a perda da regra**, nomeada |
| `priority_antes` / `priority_depois` | a catraca aparece como salto, não como estado |
| `origem` | **quem fez o gesto** (ver abaixo) |
| `pid` | qual processo, quando há mais de um |
| `backup` | onde está a versão anterior — ou `None`, confessado |

Irmãos: **`profile_apagado`** (`:991-999`, e `delete_profile` também arquiva —
apagar é a gravação mais destrutiva de todas) e **`profile_restaurado`**
(`:937-944`).

**Nenhum dos três levanta** (`contextlib.suppress(Exception)`): registrar não
pode derrubar uma gravação que já aconteceu.

`_estado_gravado` (`:749-770`) tem uma sutileza que vale a linha: quando o
arquivo anterior **não decodifica**, devolve `("ilegivel", None)` em vez de
sumir. Um perfil corrompido é justamente o caso em que saber o "antes" mais
importa.

### 4. `save_profile(..., origem=)` — a cura da camada 2

`save_profile(profile, *, origem: str | None = None)` (`:787`). Sem `origem`,
cai em `_origem_do_processo()` (`:773-784`), o basename. Com `origem`, quem sabe
quem é **declara**.

O único chamador de produção que declara hoje é o funil da janela:
`app/actions/profile_writer.py:116` → `origem=f"janela:{evento}"`, com `evento`
vindo dos três botões do rodapé (`footer_actions.py:432` `footer_save_profile`,
`:538` `footer_import`, `:618` `footer_restore_default`).

### 5. A CLI, para que o backup seja dela e não nosso

`cli/cmd_profile.py`:

- **`profile historico <nome>`** (`:233`) — tabela com *Quando* (carimbo
  traduzido por `_quando_legivel`, `:320`), *Match*, *Prioridade* e *Arquivo*.
  `_resumo_da_versao` (`:298`) lê o **JSON cru** de propósito: uma versão que
  não valida contra o esquema é exatamente a que se quer ver na lista — ela
  aparece como *ilegível* em vez de sumir;
- **`profile restore <nome> [--em <carimbo>]`** (`:267`) — sem `--em`, volta a
  **mais recente**, que é a versão de antes da última gravação, e portanto a
  resposta certa para *"desfaça o que a janela acabou de fazer com meu perfil"*.

**Um backup que ela não consegue restaurar sozinha não é backup.** É o motivo de
a CLI entrar na mesma sprint, e não na seguinte.

## O que o instrumento já capturou

Uma linha real, no disco dela:

```
profile_salvo ... match_antes=criteria match_depois=any priority_antes=10 priority_depois=191
```

**Grau: MEDIDO.** E o que ela diz: **um único save que salta de 10 para 191** —
o que **não** é a catraca de +10 (que daria 20) e **não** é só o slider (que não
mexe no `match`).

**Grau: SEM PROVA** — a atribuição do `191` a um gesto específico **continua
aberta**. A diferença é que agora é **decidível**: basta ler o `.historico/` e o
`profile_salvo` do próximo gesto dela. É o registro honesto do DIV-1 do estudo,
e esta sprint não o fecha; ela o torna fechável.

## Os testes que mordem

`tests/unit/test_profile_historico.py` (16 casos) e
`tests/unit/test_cli_profile_historico.py` (9 casos, dos quais 5 são desta
sprint e 4 do `doctor --perfis` da PERFIL-NASCE-CERTO-01/E4). Bancada hermética:
fixture `dir_perfis` monkeypatcha `loader_module.profiles_dir` para um `tmp_path`
— **nada toca o `~/.config` dela**.

Verificado em 05/08: **34 verdes** rodando os três arquivos novos juntos
(`test_profile_historico`, `test_cli_profile_historico`, `test_conftest_canario_fs`).

As mordidas, anotadas caso a caso na docstring de cada teste:

| arrancar isto | reprova |
|---|---|
| `_arquivar_versao` de dentro de `save_profile` | `test_tres_saves_guardam_duas_versoes_anteriores` (lista vazia) |
| o subdiretório `.historico/` (guardar solto em `profiles/`) | `test_historico_vive_fora_do_alcance_das_varreduras` — `load_all_profiles` devolveria as cópias como perfis |
| `_podar_historico` | `test_historico_retem_apenas_as_ultimas_n` (contagem estoura) |
| `_atomic_write_bytes` por uma reserialização | `test_restore_devolve_a_versao_byte_a_byte` |
| o arquivamento dentro de `restaurar_do_historico` | `test_restore_arquiva_a_versao_atual_antes_de_pisar` |
| o `Profile.model_validate` do restore | `test_restore_recusa_versao_que_nao_valida` — JSON quebrado voltaria a ser o perfil ativo |
| o arquivamento de `delete_profile` | `test_delete_guarda_a_ultima_versao` |
| o `logger.info("profile_salvo", …)` | `test_journal_registra_a_transicao_criteria_para_any` (AssertionError no espião) |
| o comando `restore` da CLI | `test_restore_devolve_o_perfil_pela_linha_de_comando` (exit code vira 2) |

E um caso que **não** morde o defeito, registrado como tal:
`test_backup_quebrado_nao_impede_a_gravacao` protege a política best-effort — a
borda que a *cura* introduziu, não o defeito original. Mesma honestidade da
[TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md).

## A DÍVIDA DE USO — classe DOC-VERDADE-01

**Grau: MEDIDO, por grep, em 05/08.** Os três comandos novos têm **zero menção**
na documentação de uso:

| comando | `docs/usage/cli.md` | `README.md` |
|---|---|---|
| `profile historico` | ausente | ausente |
| `profile restore [--em]` | ausente | ausente |
| `doctor --perfis` | ausente | ausente |

Concretamente:

- `docs/usage/cli.md:23` lista `profile list/show/activate/create/delete/apply/save`
  — a linha não conhece `historico` nem `restore`;
- `docs/usage/cli.md:106-119` repete a lista em blocos de exemplo, também sem os
  dois;
- `docs/usage/cli.md:212` documenta `doctor` com `--fix`, `--fix-safe` e
  `--quiet` — **sem `--perfis`**;
- no `README.md`, a palavra "histórico" só aparece na linha 316, e é o
  `CHANGELOG`.

**Por que isto é grave e não cosmético:** este é o caso exato da
[DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md)
e da [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
vistos de outro ângulo. O código existe, é testado, e **ela não tem como saber
que existe**. Um mecanismo de recuperação que a dona da máquina não consegue
descobrir é, do ponto de vista dela, um mecanismo que não foi entregue.

**Fica ABERTO.** A dívida é de três parágrafos em `cli.md` e uma linha no
`README.md`, e é entrega desta faixa, não da seguinte.

## A lacuna de teste — e uma correção ao briefing

O briefing desta sprint afirmava que `_reject_traversal` *"não tem um único
caso"*. **Isso é falso, e a correção fica registrada em vez de a afirmação ser
apagada** (regra da casa).

**Grau: MEDIDO.** `_reject_traversal` (`loader.py:56-74`) tem **seis** casos em
`tests/unit/test_profile_loader.py:245-275`, sob o rótulo
`AUDIT-FINDING-PROFILE-PATH-TRAVERSAL-01`: path absoluto, `..` com separador,
backslash, null byte, `..` puro, e o caso positivo do slug acentuado. Há ainda
dois casos de boundary no IPC (`tests/unit/test_ipc_server.py:412` e `:429`).

**A lacuna real, que sobrevive à correção, é mais estreita e mais séria:**
**todos os oito casos passam por caminhos de LEITURA** — `load_profile` e
`profile.switch`. Esta sprint deu à função **dois chamadores novos**
(`historico_dir:650` e `_slug_para_historico:682`) e, por trás deles, **três
caminhos de ESCRITA** que não existiam:

- `_arquivar_versao` → `historico_dir(slug, ensure=True)` → **`mkdir` + escrita**;
- `restaurar_do_historico` → `profiles_dir()/f"{slug}.json"` → **escrita no
  perfil**;
- a poda → **`unlink`**.

**Nenhum desses três tem um caso de traversal.** E `_reject_traversal` é a
**única** barreira entre o identificador de um perfil e uma escrita fora de
`profiles/`.

Dois pontos conferidos enquanto isto era escrito, para não deixar dúvida
pendurada:

- **`_slug_para_historico` prefere o identificador literal** quando
  `(raiz / identifier).is_dir()` (`:684-685`). Isso é seguro **porque**
  `_reject_traversal` já rodou na linha `:682`. Tirar essa linha abre o buraco
  inteiro, e nenhum teste avisaria;
- **o `carimbo` de `restaurar_do_historico` NÃO passa por `_reject_traversal`**
  (`:912-921`) — e não precisa: ele é comparado contra `v.name` da lista já
  produzida pelo `glob`, então não pode nomear arquivo fora do diretório.
  **Grau: MEDIDO, por leitura do código.** Registrado aqui para que a próxima
  pessoa não "conserte" o que está certo.

**Fica ABERTO:** um teste que chame `historico_dir("../../etc")`,
`listar_historico("..")` e `restaurar_do_historico("../x")` e exija `ValueError`
— e que, com o `_reject_traversal` arrancado dos dois chamadores novos, reprove.

## O que fica ABERTO

- **a dívida de uso** (`cli.md`, `README.md`) — seção própria acima;
- **a lacuna de traversal nos caminhos de escrita** — seção própria acima;
- **a origem do `191` continua indeterminada** (DIV-1). O instrumento existe;
  falta o próximo gesto dela;
- **a aba Perfis não declara `origem`.** `profiles_actions.py:1429`
  (`on_profile_save`, o caminho do controle deslizante) chama `save_profile(profile)`
  **sem** `origem=`, e cai no basename do processo. Na prática **ainda é
  distinguível** do rodapé — que carimba `janela:footer_*` —, mas **por ausência,
  não por nome**: o segundo caminho da janela que esquecer o `origem=` colide com
  este em silêncio. Grau: MEDIDO por grep em `src/`. É uma linha, e não entrou
  aqui porque o arquivo estava sendo escrito por um agente irmão na mesma
  madrugada;
- **`manager.py:170` também grava sem `origem`** — mesma classe, caminho do
  daemon;
- **nenhum índice.** A faixa de perfis está órfã desde 30/07, e o estudo mede a
  queda: menções às sprints da faixa caem de **15** (índice de 30/07) para **4**
  (31/07) e **0** (01/08, 03/08 e ONDAS). **É a explicação estrutural de por que
  meias-entregas passaram nesta faixa: ninguém estava olhando.**

## Nota datada — o que caducou

**05/08/2026.** A seção 5.7 do estudo consolidado registra, sob *Hermeticidade*,
que `_ALLOWLIST_PATH` e `_WP_DROPIN_DIR` *"continuam constantes de módulo"*.
**Caducou no mesmo dia**, por decisão dela — ver
[CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md).
A frase do estudo fica onde está: era verdade quando foi escrita, e o registro
de que deixou de ser é esta nota.

## Relacionado

- [o sistema de perfis, o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  — D-36 (nem validação, nem backup, nem registro), DIV-1 (as três teses), 5.4
- [CANÁRIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md)
  — a outra metade da mesma pergunta dela: *"foi um teste?"*
- [PERFIL-NASCE-CERTO-01](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md)
  — a E4 é o `profiles/sanidade.py` e o `doctor --perfis`, que compartilham o
  arquivo de teste desta sprint
- [DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md)
  — a classe da dívida de uso registrada aqui
- [JANELA-FIEL-01](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md)
  — *"zero linhas da janela nos últimos sete dias"*, que é por que o `stderr` não
  servia de rastro
