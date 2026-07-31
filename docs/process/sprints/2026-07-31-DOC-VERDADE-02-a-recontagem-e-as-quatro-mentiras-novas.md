# DOC-VERDADE-02 — a recontagem de 31/07 e as mentiras novas

- **Status:** ABERTA — plano com aceite executável. Nesta rodada **nenhum arquivo
  do repositório foi alterado**: o documento é só leitura e medição
- **Prioridade:** MÉDIA-ALTA — não impede jogar, mas duas das entregas abaixo são
  receitas que **quebram na primeira colagem** (o exemplo de perfil e as duas
  vias de ligar plugins), e isso já não é dívida de documento: é defeito de uso
- **Aberta em:** 31/07/2026, sobre `HEAD 7bd0cb7`, branch
  `restauro/inicio-da-sessao`, com a v0.4.0 publicada em 30/07 e o daemon e a
  janela **vivos** na máquina dela — nada aqui encostou nos dois
- **Sucede:** [DOC-VERDADE-01](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md),
  de 26/07, que mediu NOVE contradições e definiu SETE entregas. **Esta sprint
  não a substitui**: a 01 continua sendo o diagnóstico de origem e a régua de
  comparação. Esta recontou item a item e acrescenta o que a auditoria de 31/07
  achou de novo
- **Relacionada:** [CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md)
  (o NOTICE e os drivers GPL — pendência que esta sprint **aponta e não assume**),
  [CR-01](2026-07-25-CR-01-posicao-juridica.md),
  [CR-02](2026-07-25-CR-02-formato-e-proveniencia.md),
  [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md)
  (o que o projeto anuncia e não entrega) e
  [PORTÃO-VIVO-01](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md), que
  pariu o gate de referências que a E10 amplia
- **Rodada:** faz parte da
  [auditoria de treze agentes de 31/07](../estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md),
  em que quatro verificadores independentes tinham poder de reprovar — e
  reprovaram. Onde o verificador reenquadrou um achado, **este documento segue o
  verificador**, e diz por quê

## Por que uma sprint que só diagnostica de novo não serve para nada

A DOC-VERDADE-01 acertou o diagnóstico. O que ela não teve foi como cobrar.

Medido hoje, com comando e saída:

- `git log --since=2026-07-26 -- docs/protocol/` devolve **vazio**. O último
  toque em `docs/protocol/` é o commit `14cd31b`, de **25/07** — um dia *antes*
  da sprint existir.
- `ls docs/adr/` devolve **19 arquivos**. O ADR-020 que a entrega 2 pedia não
  nasceu.
- `grep -l "Nota de verifica" docs/adr/*` devolve **três**: `003`, `008` e `016`
  — exatamente os mesmos de 25/07. A entrega 1, que era terminar a varredura nos
  ADRs 001, 010, 011, 014, 015 e 017, não encostou em nenhum.

**Nenhuma das sete entregas foi executada.** O pouco que andou veio de carona da
leva de 27/07 (`e96dea8`), que corrigiu nomes de pacote em três ADRs, tirou o
botão "Ver daemon.toml" da aba Emulação e removeu o glifo proibido do
`docs/usage/troubleshooting-8bitdo.md`. Carona não é execução: ela cura o que
esbarra e deixa o resto.

A diferença desta sprint é uma só, e é o motivo dela existir:

> **Toda entrega daqui tem aceite que roda.** Um comando, uma saída, um código de
> retorno. Três delas já vêm com o teste que morde escrito — e mordida, nesta
> casa, quer dizer: arranque a cura e o teste tem de FICAR VERMELHO. Teste que
> passa com a cura arrancada não testa nada.

## A recontagem: onde estão as nove de 26/07

Conferi as nove uma a uma no código de hoje. **Sete persistem, uma foi curada e
uma foi curada pela metade.**

| # na 01 | O que ela mediu em 26/07 | 31/07 | Onde eu conferi hoje |
|---|---|---|---|
| 1 | ADR-001 elege um backend que o produto não usa mais | **persiste** | `docs/adr/001-pydualsense-backend.md:9` segue "usar `pydualsense >= 0.7.5` como backend", sem nota; não há ADR-020 |
| 2 | três caminhos para o mesmo socket | **persiste** | `docs/protocol/ipc-unix-socket.md:5`, `docs/adr/010-ipc-socket-liveness-probe.md:7` e `:13`, contra `docs/usage/hotkeys.md:40` |
| 3 | `udp-schema.md` afirma duas coisas que não existem | **persiste, e o texto foi TOCADO** | `docs/protocol/udp-schema.md:5` e `:78` |
| 4 | os ADRs falam de um pacote com outro nome | **parcial** | `e96dea8` curou 014, 015 e a seção final do 017; sobram `004:9` e `:11`, `010:7` e `:13`, `012:28`, e o corpo do `017` (`:25`, `:46`, `:63`, `:84`, `:86`) |
| 5 | ADR-017 repete o buraco que já matou as métricas | **persiste, e dobrado** | `docs/adr/017-plugin-system.md:73-74` — agora são DUAS receitas mortas, não uma |
| 6 | a tabela de métodos do IPC lista 10 de 33 | **persiste** | a tabela tem **10 linhas**; o documento inteiro cita **17 de 34** |
| 7 | "19 modos" nomeia dois conjuntos diferentes | **persiste** | `docs/usage/interface.md:48` contra `docs/protocol/trigger-modes.md:7` e `:38`, e `docs/protocol/udp-schema.md:163` |
| 8 | `Rigid` e `Medium` em colisão com a sala limpa | **metade curada, metade PIOROU** | `Rigid` existe hoje em `PRESET_FACTORIES`; `Medium` não existe e o exemplo do guia **reprova na validação** |
| 9 | glifo proibido no `troubleshooting-8bitdo.md` | **CURADA** | zero ocorrências de U+2B50 (medido em Python, contando o caractere) |

O caso mais instrutivo é o **3**. Alguém abriu o `udp-schema.md`, atualizou o
caminho de `~/.config/hefesto/daemon.toml` para
`~/.config/hefesto-dualsense4unix/daemon.toml` — e **manteve a ficção de que o
daemon lê aquele arquivo**. É o pior estado possível de um documento errado:
parece revisado.

## O que o verificador reenquadrou — e onde eu corrigi o auditor

Quatro correções entram no documento porque medi e o número não bateu.

**1. O NOTICE e os drivers GPL não são achado novo — são a CR-05 por executar.**
O auditor classificou como ALTA e pediu entrega aqui. O verificador achou o que
ele não procurou: a sprint
[CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md), aberta em 25/07,
já diagnostica exatamente isso, com o enquadramento jurídico fechado. Sigo o
verificador: **vira pendência apontada, não entrega desta sprint** (seção
própria, mais abaixo).

**2. O i18n: o auditor escreveu que "traduzir os `.po` não traduz a janela", e
isso é forte demais.** Medi: `src/hefesto_dualsense4unix/gui/main.glade` tem
**309** atributos `translatable="yes"`, e `app/app.py:183` chama
`self.builder.set_translation_domain(TEXTDOMAIN)` — ou seja, **o esqueleto fixo
da janela passa pelo catálogo**. Do lado do catálogo, `po/hefesto-dualsense4unix.pot`
tem 284 mensagens, das quais **243 vêm do glade** e 65 do Python. O defeito é
mais estreito e continua real: o que **não** traduz é o texto que as ações
escrevem em execução. A E6 abaixo usa a minha medida, não a do auditor.

**3. A contagem de módulos das ações estava errada nos dois lados.** O auditor
escreveu "16 de 18". Medido: `src/hefesto_dualsense4unix/app/actions/` tem
**17** arquivos `.py` (contados com `find`), e **15** deles não importam
`gettext` nem o `_` de `utils/i18n`. Os dois que importam são
`app/actions/footer_actions.py:29` e `app/actions/status_actions.py:74`. O
número certo é **15 de 17**.

**4. A tabela do IPC: "17 de 34" é do documento inteiro, não da tabela.** A
tabela "Métodos v1" (`docs/protocol/ipc-unix-socket.md:13-24`) tem **10 linhas**.
Outros sete métodos aparecem em tabelas e parágrafos adiante (`mic.set`,
`speaker.set`, `identity.renumber`, `identity.number.set`, `led.player_set`,
`daemon.state_full`, `daemon.emulation.suppress`). Somando tudo, o documento
menciona 17 dos 34 registrados. As duas frases são verdadeiras e dizem coisas
diferentes; o documento usa as duas com o rótulo certo.

E uma correção que é minha, contra a recomendação do próprio auditor — está na
E4, e vale ler antes de escrever a cura: a frase que ele sugeriu para o
`udp-schema.md` **também é falsa**.

## As entregas

Ordem de leitura: E1 a E3 são as que o verificador confirmou com teste
executado; E4 e E5 fecham o que sobrou da 01; E6 a E9 são o que apareceu de
novo; E10 é o portão que impede a volta de todas.

### E1. O primeiro exemplo do guia de perfis cria um perfil que o daemon recusa

`docs/usage/creating-profiles.md:19` ensina:

```
"left":  {"mode": "Medium", "params": []},
```

`src/hefesto_dualsense4unix/profiles/schema.py:163-168` recusa qualquer `mode`
fora de `PRESET_FACTORIES`, com `ValueError: modo de trigger desconhecido`.

Medi `PRESET_FACTORIES` com o `.venv` do projeto: são **19 nomes** — `AutoGun`,
`Bow`, `Custom`, `Feedback`, `Galloping`, `Machine`, `MultiPositionFeedback`,
`MultiPositionVibration`, `Off`, `Pulse`, `PulseA`, `PulseB`, `Resistance`,
`Rigid`, `SemiAutoGun`, `SimpleRigid`, `SlopeFeedback`, `Vibration`, `Weapon`.
**`Medium` não é um deles. `Rigid` é** — a metade que a 01 discutia como
colisão teórica já se resolveu sozinha.

Colado o JSON exato do exemplo em `Profile.model_validate()`, a saída é:

```
ValidationError: 1 validation error for Profile
triggers.left.mode
  Value error, modo de trigger desconhecido: 'Medium'
```

Isto **chega na janela**: `app/actions/footer_actions.py:388` valida o arquivo
importado pelo mesmo `Profile.model_validate`, e o erro vira o aviso de
`footer_actions.py:444`. Quem copia o primeiro exemplo do guia e clica em
"Importar Perfil" leva uma recusa.

A troca precisa ser um modo real **com parâmetros que façam sentido**. Medida a
assinatura das fábricas: `Resistance(start, force)` pede dois. Validei o exemplo
inteiro com `"mode": "Resistance", "params": [0, 5]` e ele **passa**.

**O que esta entrega não faz:** escrever o guarda de nomes proibidos da
[CR-02](2026-07-25-CR-02-formato-e-proveniencia.md). A fronteira entre *fato de
protocolo* e *criação de terceiro* continua sendo decisão daquela sprint; aqui
só se registra que `Rigid` é nome de modo HID de baixo nível
(`core/trigger_effects.py`) e não pode entrar em lista de proibidos.

**Aceite:** um teste percorre todo bloco ```` ```json ```` de `docs/usage/` que
tenha a chave `triggers` e roda `Profile.model_validate` em cada um. Todos
passam. Hoje esse teste falha em um bloco — o de
`docs/usage/creating-profiles.md:19`.

**Mordida:** devolver `"Medium"` ao exemplo faz o teste ficar VERMELHO com o
mesmo `ValidationError` copiado acima. Um teste que só verifique "o arquivo
contém a palavra Resistance" **não** morde: passaria com qualquer outro nome
inválido escrito ali. É o `model_validate` que precisa rodar.

**Risco:** baixo. É edição de duas palavras num exemplo, com prova executável do
antes e do depois.

**Limite medido, para não vender a mais:** o schema valida o **nome** do modo,
não a **aridade** dos parâmetros. `{"mode": "Resistance", "params": []}` passa
na validação e só explodiria no `apply()` — é exatamente o que o docstring de
`profiles/schema.py:156-158` diz que quis evitar **para o nome**. O teste desta
entrega pega nome errado; não pega parâmetro faltando.

### E2. O ADR dos plugins ensina duas maneiras de ligar plugins, e nenhuma funciona

`docs/adr/017-plugin-system.md:73-74`:

```
- Configuração em `~/.config/hefesto/config.toml`: `plugins_enabled = true`
- Variavel de ambiente: `HEFESTO_PLUGINS_ENABLED=1`
```

As duas são vias mortas, e medi as duas:

- **`config.toml`:** `grep -rn "config\.toml" src/` devolve **nada**. O daemon
  não lê arquivo de configuração nenhum — `daemon/main.py:91-110` monta o
  `DaemonConfig` só com variáveis de ambiente, e o próprio código admite isso em
  `app/actions/emulation_actions.py:450` (`BUG-DAEMON-TOML-DEAD-01: o daemon NÃO
  lê daemon.toml`).
- **`HEFESTO_PLUGINS_ENABLED`:** `grep -rn "HEFESTO_PLUGINS_ENABLED" src/`
  (excluindo o prefixo longo) devolve **nada**. A variável real é
  `HEFESTO_DUALSENSE4UNIX_PLUGINS_ENABLED`, lida em
  `daemon/subsystems/plugins.py:194`; a irmã do diretório é
  `HEFESTO_DUALSENSE4UNIX_PLUGINS_DIR`, em `:157`, e o diretório padrão é
  `~/.config/hefesto-dualsense4unix/plugins/` (`plugins.py:58-62`), não o
  `~/.config/hefesto/plugins/` que o ADR repete em `:25`, `:63`, `:84` e `:86`.

E há a contradição interna: **o `README.md:267-269` documenta a variável
CERTA.** O documento de referência da funcionalidade discorda do README, e quem
confia no ADR não liga plugin nenhum.

Detalhe que explica como isso sobreviveu: `git show e96dea8 -- docs/adr/017-plugin-system.md`
mostra que o diff começa na linha **117**, a seção "Impacto no código". A seção
"Ativação", que é a que ensina, ficou intocada.

**Aceite:** `grep -n "HEFESTO_PLUGINS_ENABLED\|config\.toml" docs/adr/017-plugin-system.md`
devolve **zero** linhas fora de uma nota de verificação datada; e a nota diz a
variável real, o diretório real e que a via `config.toml` nunca existiu. O
formato já existe nesta casa e é bom: `docs/adr/003-udp-port-6969-compat.md:14-22`
— nota datada no fim, sem reescrever a decisão original.

**Mordida:** é a E10 que morde por esta. Com o gate ampliado, devolver
`HEFESTO_PLUGINS_ENABLED` ao ADR faz `validar-referencias-docs.py --all` sair
com código diferente de zero. Sem a E10, esta entrega não tem quem a segure.

**Risco:** baixo. Nota nova no fim do arquivo, nada apagado.

### E3. O caminho do socket tem três grafias, e o documento canônico é uma das erradas

| Onde | O que afirma |
|---|---|
| `docs/protocol/ipc-unix-socket.md:5` | `$XDG_RUNTIME_DIR/hefesto-dualsense4unix.sock` — falta o diretório |
| `docs/adr/010-ipc-socket-liveness-probe.md:7` | `$XDG_RUNTIME_DIR/hefesto/hefesto.sock` — layout curto legado |
| `docs/usage/hotkeys.md:40`, `docs/usage/troubleshooting.md:205` | `$XDG_RUNTIME_DIR/hefesto-dualsense4unix/hefesto-dualsense4unix.sock` |

O terceiro é o que funciona. O real vem de
`src/hefesto_dualsense4unix/utils/xdg_paths.py:120-128`: `ipc_socket_path()`
devolve `runtime_dir(ensure=True) / ipc_socket_name()`, com `runtime_dir` em
`:82-88` e o nome-base resolvido em `:36-58`, cujo default é
`IPC_SOCKET_DEFAULT_NAME = "hefesto-dualsense4unix.sock"` (`:15`). A variável de
isolamento é `IPC_SOCKET_ENV_VAR = "HEFESTO_DUALSENSE4UNIX_IPC_SOCKET_NAME"`
(`:16`) — e não o `HEFESTO_IPC_SOCKET_NAME` que o ADR-010 anuncia em `:13`.

**A entrega não é digitar o caminho certo no documento de protocolo.** É o que a
entrega 3 da DOC-VERDADE-01 já pedia e ninguém fez: **derivar do código**. Um
documento com o caminho digitado à mão volta a divergir na próxima mudança de
`xdg_paths.py` — foi assim que ele divergiu da primeira vez.

**Aceite:** um teste importa `ipc_socket_path` e `IPC_SOCKET_ENV_VAR` de
`utils/xdg_paths.py` e cobra que a forma canônica (`$XDG_RUNTIME_DIR` +
`hefesto-dualsense4unix/` + nome-base) e o nome da env apareçam literalmente em
`docs/protocol/ipc-unix-socket.md`; e que nenhuma linha viva de `docs/` cite
`XDG_RUNTIME_DIR/hefesto/`.

**Mordida:** trocar `IPC_SOCKET_DEFAULT_NAME` no código deixa o teste VERMELHO
enquanto o documento não acompanhar — é exatamente a regressão que a casa quer
que doa. Um teste que só compare o texto do documento consigo mesmo não morde.

**Risco:** baixo-médio. O único cuidado é o modo fake: `ipc_socket_name()`
(`:36-58`) troca o nome-base quando `HEFESTO_DUALSENSE4UNIX_FAKE=1`, então o
teste tem de fixar o ambiente antes de comparar, ou vai medir o socket do fake.

### E4. A porta UDP "configurável" — e a frase que a correção de 25/07 pôs no lugar

`docs/protocol/udp-schema.md:5` diz, hoje:

```
`127.0.0.1:6969` (UDP). Configurável em `~/.config/hefesto-dualsense4unix/daemon.toml`.
```

O daemon não lê esse arquivo — `daemon/main.py:91-110` e a confissão em
`emulation_actions.py:450`. Do lado da janela isso **já está compensado**: o
botão "Ver daemon.toml" saiu na leva de 27/07 e o arquivo que a GUI gera se
declara não-lido na primeira linha (`emulation_actions.py:461`). Falta a metade
documental.

**E aqui eu discordo do auditor.** A recomendação dele era trocar a frase por
*"porta fixa 6969; muda por `daemon.reload` via IPC"*. Isso é uma **mentira
nova, menor**, e é a mesma que a nota de verificação de 25/07 já escreveu no
`docs/adr/003-udp-port-6969-compat.md:20-21` (*"só se altera por `daemon.reload`
via IPC ou no código"*). Medido:

- `udp_port` só é lido em `daemon/subsystems/udp.py:36`, dentro do `start()` do
  subsistema, que roda uma vez — `lifecycle.py:659`.
- `reload_config` (`lifecycle.py:993-1019`) reinicia o gerenciador de hotkeys,
  o mouse e o teclado emulado. **Não toca no UDP.**
- `daemon.reload` aceita `udp_port` como campo conhecido
  (`daemon/ipc_handlers.py:2578-2584` valida contra os campos do `DaemonConfig`),
  grava o valor novo e devolve `status: ok`.

Ou seja: pedir outra porta por IPC é **aceito e silenciosamente inócuo** — o
socket continua ligado em 6969. Pior que recusar.

A frase honesta é: porta fixa em 6969; não há hoje variável de ambiente, arquivo
nem método IPC que a mude num daemon em execução; `daemon.reload` altera o campo
sem reabrir o socket; mudar de verdade exige mexer no código
(`lifecycle.py:122`) e reiniciar. É o mesmo formato de confissão que o
`docs/usage/metrics.md:23-33` já usa para as métricas, e que é uma das páginas
mais honestas do projeto.

**Aceite:** `grep -n "daemon.toml" docs/protocol/udp-schema.md` devolve zero
fora de uma frase que diga que o arquivo **não** é lido; e a nota do ADR-003
ganha uma linha registrando que `daemon.reload` não reabre o socket UDP.

**Junto, e é barato:** `udp-schema.md:78` nega validação pydantic no caminho UDP
e está **certo** (`daemon/udp_server.py` não importa pydantic); quem está errado
é o `docs/adr/003:9`, que a afirma. A nota de 25/07 corrigiu o `daemon.toml` do
ADR-003 e passou por cima deste ponto. A mesma nota resolve os dois.

**Risco:** baixo. Texto e nota. Nenhuma linha de código.

### E5. A tabela de métodos do IPC, gerada do código em vez de digitada

Medido com script próprio contra o dicionário `_handlers`
(`daemon/ipc_server.py:102-151`): **34 métodos registrados**. O
`docs/protocol/ipc-unix-socket.md` menciona **17**; a tabela "Métodos v1"
(`:13-24`) traz **10**.

Os 17 ausentes:

`autoswitch.lock`, `controller.target.set`, `coop.set`, `daemon.pause`,
`daemon.resume`, `gamepad.emulation.set`, **`keyboard.emulation.set`**,
`launch_env.refresh`, `mouse.emulation.restore`, `plugin.list`, `plugin.reload`,
`profile.apply_draft`, `rumble.passthrough`, `rumble.policy_custom`,
`rumble.policy_set`, `rumble.set`, `rumble.stop`.

O destaque não é decorativo. `keyboard.emulation.set` é o interruptor que a
v0.4.0 inteira gira em torno — `CHANGELOG.md:27` o anuncia como entrega
principal ("Interruptor próprio para o teclado emulado, com flag persistida e
método IPC"), e ele nasceu porque o R1 dela trocava de aplicativo **dentro da
partida**. A cura mais importante da release é invisível no documento de
protocolo.

E toda a família `rumble.*` está fora — cinco métodos, incluindo o
`rumble.stop`, que é a parada de emergência nascida do incidente
*"tremendo sem parar"* de 25/07.

A entrega é **gerar**, porque a tabela à mão desatualiza a cada leva: era 10 de
33 em 26/07 e é 10 de 34 hoje. O registro é um `dict` introspectável; a docstring
de cada handler em `daemon/ipc_handlers.py` já traz `Params`, `Retorna` e
`Erros` em formato regular (ver `_handle_daemon_reload`, em `:2555-2568`).

**Aceite:** a seção de métodos do documento é gerada por script, e um teste
compara as chaves de `_handlers` com os métodos listados no documento: as duas
listas são **iguais**, não uma contida na outra.

**Mordida:** registrar um método novo no `ipc_server.py` sem regenerar a tabela
deixa o teste VERMELHO. A prova de que o teste morde é histórica e barata de
refazer: com o teste escrito e a tabela de hoje, ele já reprova apontando os 17
nomes acima.

**Risco:** médio. É a entrega que mexe em mais linhas de documento. Cuidado
declarado: as seções em prosa do `ipc-unix-socket.md` (`:26-43` sobre o `uniq`,
`:45` em diante sobre o áudio) explicam **contrato**, não sintaxe, e não podem
ser esmagadas pela tabela gerada. Gerar a tabela, preservar a prosa.

### E6. O i18n é anunciado em três documentos, e o texto que a janela escreve não passa pelo catálogo

Três páginas convidam a traduzir:

- `.github/CONTRIBUTING.md:149` — *"A partir de v3.4.0 o projeto tem i18n
  baseline com EN + PT-BR"*, seguido da receita de criar um idioma novo;
- `docs/usage/flatpak.md:140-175` — seção "Localização (i18n)", com
  *"Para rodar a GUI em inglês"* e o `flatpak override`;
- `docs/usage/troubleshooting.md:395-420` — sintomas A/B/C de "GUI em EN" e o
  convite final "Adicionar idioma novo (comunidade)".

O que eu medi, e é mais estreito do que o auditor disse (ver a seção de
reenquadramento):

- **O esqueleto fixo TRADUZ.** 309 `translatable="yes"` no
  `gui/main.glade`, com `app/app.py:183` chamando `set_translation_domain`. Dos
  284 msgids do `.pot`, **243 vêm do glade**.
- **O texto de execução NÃO.** Dos 17 arquivos `.py` de
  `src/hefesto_dualsense4unix/app/actions/`, **15 não importam** `gettext` nem o
  `_` de `utils/i18n`. Só `footer_actions.py:29` e `status_actions.py:74`
  importam. Contando só as chamadas de uma linha com literal direto
  (`_toast*`, `set_text`, `set_label`, `set_markup`, `set_tooltip_text`), são
  **73 frases** escritas em português direto no widget — 23 em
  `profiles_actions.py`, 18 em `emulation_actions.py`, 13 em `home_actions.py`,
  10 em `daemon_actions.py`.
- **O catálogo está atrás.** `msgfmt --statistics` hoje: `po/en.po` com 186
  traduzidas, 25 aproximadas e **82 não traduzidas**; `po/pt_BR.po` com 168, 25
  e 91.

Sobre o `pt_BR.po`, uma ressalva honesta que impede a próxima leva de "consertar"
o que não está quebrado: pt-BR é a língua de origem, então mensagem não
traduzida cai no próprio msgid, que já está em português. Aquelas 91 são sinal de
catálogo defasado, **não** defeito visível na tela dela.

A decisão é dela e são duas, excludentes:

1. **Rebaixar o anúncio** nos três documentos: dizer que os rótulos fixos da
   janela e a CLI têm catálogo, e que mensagens de estado, avisos e diagnósticos
   saem em português independentemente do `LANG`. Custo: três parágrafos.
2. **Abrir sprint de `_()`** para envolver as 73 frases (e as que vierem)
   antes de convidar tradutores.

O que **não** pode continuar é o estado atual: convidar alguém a traduzir sem
dizer o que a tradução alcança.

**Aceite (opção 1):** os três documentos dizem o que traduz e o que não traduz, e
um teste cobra o piso: nenhum arquivo novo em `app/actions/` escreve texto
direto no widget sem `_()` — ou, se a casa preferir começar sem trava, o número
de módulos sem `gettext` **não sobe** de 15.

**Mordida:** acrescentar uma chamada com literal a um módulo sem `_()` deixa o
teste VERMELHO. Um teste que só conte arquivos não morde: passa se alguém trocar
um módulo por outro.

**Risco:** baixo na opção 1, alto na 2 — envolver 73 frases toca nove arquivos de
ação e mexe em texto que aparece na tela dela. Se for a 2, ela vê antes
(PROVA-DE-TELA-01).

### E7. "DaemonConfig com três parâmetros" ficou falso em 29/07, e três páginas ainda afirmam

`daemon/main.py:91-110` constrói o `DaemonConfig` com **quatro**: `poll_hz`,
`auto_reconnect`, `ps_long_press_ms` e `keyboard_emulation_enabled` — este
último lendo `HEFESTO_DUALSENSE4UNIX_KEYBOARD_EMULATION`, com o comentário
`EMULACAO-NO-JOGO-01` de 29/07 em `:100-106` explicando por que o campo deixou
de ser configuração morta.

As três páginas que envelheceram na mesma frase:

| Onde | O que diz |
|---|---|
| `README.md:272` | *"o daemon o constrói com três parâmetros só (`poll_hz`, `auto_reconnect`, `ps_long_press_ms`)"* |
| `docs/usage/metrics.md:20-22` | a mesma frase, dentro da confissão sobre as métricas |
| `docs/usage/hotkeys.md:31-33` | *"hoje são três"* variáveis de ambiente, e lista `POLL_HZ`, `PS_LONG_PRESS_MS` e `NICE` — omitindo a quarta |

A ironia vale registrar: **são as três páginas mais honestas do projeto**,
escritas justamente como correção de ficções anteriores. Elas erram por serem
específicas, que é o oposto do defeito das outras. Quem for ligar as métricas
seguindo a receita de `metrics.md:36` (*"como as outras três já são"*) parte de
uma contagem errada.

**Aceite:** um teste importa `daemon.main`, conta as `os.getenv` do bloco que
monta o `DaemonConfig` e cobra que o número apareça por extenso nos três
arquivos. Hoje o teste reprova nos três.

**Mordida:** acrescentar uma quinta env em `daemon/main.py` sem tocar nos
documentos deixa o teste VERMELHO. É o teste que resolve a classe inteira, não
só esta ocorrência — e é barato porque a contagem vem do código.

**Risco:** baixo. Uma palavra por arquivo. O cuidado é não estragar o tom: as
três frases são confissões, e a correção mantém a confissão.

### E8. O ADR-008 atesta dois replays determinísticos e um dos arquivos não existe

`docs/adr/008-bt-vs-usb-polling.md:14`:

> `FakeController` tem dois replays determinísticos:
> `tests/fixtures/hid_capture_usb.bin` e `tests/fixtures/hid_capture_bt.bin`
> [...] Testes W1.3 cobrem ambos.

Medido: `ls tests/fixtures/` devolve `hid_capture_usb.bin` e `__init__.py`. **O
`hid_capture_bt.bin` não existe.** O ADR atesta uma cobertura que a suíte não
tem.

E o ADR **já tem** uma nota de verificação, de 25/07 (`:24-29`) — ela corrigiu o
`daemon.toml` do `poll_hz` e passou ao lado disto. Uma nota que revisa o
documento e não confere a alegação central de cobertura é meia-varredura.

Isto não é detalhe de documento: é a premissa **USB-é-o-mundo**, que a casa já
registrou como classe de bug recorrente. A suíte é cega a Bluetooth por
construção, e o ADR faz parecer o contrário.

**Aceite:** ou a nota de verificação do ADR-008 registra que a fixture BT nunca
existiu e que os testes cobrem só USB, ou a fixture é gravada com o
`scripts/record_hid_capture.py` (que existe, 14 KB, executável) e o ADR passa a
ser verdade.

**Mordida:** um teste que abra `tests/fixtures/hid_capture_bt.bin` e reprove se
o arquivo faltar só serve **se a casa escolher gravar**. Se a escolha for a nota,
a mordida é a da E10: um documento que cite um arquivo inexistente reprova no
gate — e a razão de este caso ter sobrevivido é que `.bin` não está entre as
extensões que o gate cobra hoje (`validar-referencias-docs.py:53-55`).

**Risco:** baixo se for nota; médio se for gravar — o `record_hid_capture.py`
precisa de controle real por Bluetooth, e isso é sessão dela com hardware.

### E9. As três notas baratas: ADRs 004, 012 e a lápide do 014

Três correções de uma linha cada, no formato já provado do
`docs/adr/003:14-22`.

| ADR | O que ele afirma hoje | O que é |
|---|---|---|
| `004-systemd-user-service.md:9` | unidade `hefesto.service`, instalada por `hefesto daemon install-service` | a unit é `hefesto-dualsense4unix.service` e o comando é `hefesto-dualsense4unix` |
| `004-systemd-user-service.md:11` | `--headless` seta `HEFESTO_NO_WINDOW_DETECT=1` | é `HEFESTO_DUALSENSE4UNIX_NO_WINDOW_DETECT`, em `cli/app.py:204` |
| `012-gui-reconnect-state-machine.md:28` | o botão roda `systemctl --user restart hefesto.service` | mesma unit renomeada |
| `014-cosmic-wayland-support.md:43-45` | *"`xlib_window.py` convertido em shim de compatibilidade [...] Código legado não precisa de alteração"* | desde 29/07 é uma **lápide** que levanta erro no import |

O caso do 014 é o mais interessante, e é decisão documentada, não lapso:
`src/hefesto_dualsense4unix/integrations/xlib_window.py:1-20` explica que o shim
lia `_NET_ACTIVE_WINDOW` **sem gate de foco** — o defeito que o backend vivo já
tinha curado — e que a lápide fica no lugar do arquivo apagado porque *"nesta
casa o registro do porquê vale mais do que a linha em branco"*. Há teste
guardando (`tests/unit/test_xlib_window_nao_importavel.py`). O que ficou errado
é só a frase do ADR: hoje "código legado não precisa de alteração" significa
`ModuleNotFoundError` de propósito.

**Aceite:** `grep -rn "hefesto\.service\|HEFESTO_NO_WINDOW_DETECT" docs/adr/`
devolve só linhas dentro de nota de verificação; e o ADR-014 remete à
CODIGO-MORTO-01 com o substituto (`integrations/window_detect.py`,
`build_window_reader`).

**Risco:** o mais baixo da sprint. Quatro linhas.

### E10. O gate que deixou tudo isso passar — e a extensão exata que faltava

`scripts/validar-referencias-docs.py` nasceu na PORTÃO-VIVO-01 e é bom: já
protege o CI (`.github/workflows/ci.yml:82-102`, sem `continue-on-error` desde
27/07). Mas ele cobra **arquivo**, e só. As referências que ele extrai precisam
terminar numa extensão da casa (`:53-55`: `.py .sh .md .yml .yaml .toml .glade
.rules`).

**É por esse buraco que a E2, a E3 e metade da E9 sobreviveram**: variável de
ambiente e método de IPC não são arquivos. A entrega 7 da DOC-VERDADE-01 pedia
exatamente isto e foi feita pela metade.

Medi as duas regras novas contra a árvore de hoje, antes de propô-las — porque
a filosofia escrita no topo do próprio script (`:10-12`) é que **falso positivo
em massa torna o gate inútil**.

**Regra A — variáveis de ambiente.** Token entre crases no formato
`HEFESTO_[A-Z0-9_]+` conferido contra os literais de `src/`. Resultado sobre
`docs/` viva (fora de `history/` e `research/`, já ignorados em `:85`): **9
ocorrências**, e a lista inteira cabe aqui:

| Onde | Variável | Veredito |
|---|---|---|
| `docs/adr/017-plugin-system.md:74` | `HEFESTO_PLUGINS_ENABLED` | achado real — é a E2 |
| `docs/adr/010-ipc-socket-liveness-probe.md:13` | `HEFESTO_IPC_SOCKET_NAME` | achado real — é a E3 |
| `docs/adr/004-systemd-user-service.md:11` | `HEFESTO_NO_WINDOW_DETECT` | achado real — é a E9 |
| `docs/usage/metrics.md:13` e `:18`, `docs/adr/016-prometheus-metrics.md:142` | `HEFESTO_DUALSENSE4UNIX_METRICS` | **menção deliberada de ausência** — precisa de isenção |
| `docs/process/` (3 linhas: o estudo de 31/07 e uma auditoria de junho) | `HEFESTO_PLUGINS_ENABLED`, `HEFESTO_PURE_HID` | registro histórico — precisa de isenção |

**Cuidado que vale a entrega inteira:** sem isenção, a regra A reprovaria
`docs/usage/metrics.md` — a página que existe **justamente para dizer que aquela
variável não existe**. Um gate que castiga a honestidade é pior que gate nenhum.
O escape já existe e é o marcador de linha `<!-- ref-externa: motivo -->`
(`validar-referencias-docs.py:101`), com precedente em cinco sprints.

**Regra B — métodos de IPC.** Token entre crases no formato `a.b` ou `a.b.c`
cujo **primeiro segmento** seja um espaço de nomes que existe no `_handlers`
(`profile.`, `trigger.`, `led.`, `daemon.`, `rumble.`, `mouse.`, `keyboard.`,
`gamepad.`, `controller.`, `identity.`, `coop.`, `plugin.`, `autoswitch.`,
`mic.`, `speaker.`, `native.`, `launch_env.`) e cujo token completo **não**
esteja registrado. Assim `ctx.controller` nunca é cobrado — `ctx` não é espaço de
nomes de IPC.

Medida ingênua: 25 candidatos, quase todos falso positivo (`daemon.toml`,
`keyboard.py`, `autoswitch.py`, `profile.name`). Com dois filtros — descartar
token que termine em extensão de arquivo e token com segmento iniciado por `_` —
e o escopo restrito aos documentos que **ensinam** (`docs/usage/`, `docs/adr/`,
`docs/protocol/`, `README.md`), o resultado é **zero falso positivo hoje**. Os
cinco restantes ficam todos em `docs/process/`, e são legítimos: sprints que
*propõem* métodos (`controller.player.set` na PLAYER-01,
`identity.alias.set` na IDENT-01). Por isso `docs/process/` fica **fora** da
regra B, por escrito.

**Aceite:** `python3 scripts/validar-referencias-docs.py --all` sai com código
**diferente de zero** na árvore de hoje, apontando as três linhas de env da
tabela acima; e sai com **zero** depois que E2, E3 e E9 entrarem.

**Mordida, em duas partes:**

1. Escrever ` `HEFESTO_DUALSENSE4UNIX_PLUGINZ` ` num documento de `usage/` faz o
   gate reprovar. Apagar a regra A faz o teste do gate
   (`tests/unit/test_validar_referencias_docs.py`, que já existe) ficar
   VERMELHO.
2. Escrever ` `profile.trocar` ` num documento de `usage/` faz o gate reprovar;
   ` `profile.switch` ` passa. Renomear um método no `ipc_server.py` sem tocar no
   documento também reprova — que é o cenário real.

**Risco:** médio, e o motivo é o de sempre: gate que reprova demais é gate que
alguém desliga. Por isso as duas regras entram com escopo medido, com a lista
completa de ocorrências acima, e com o escape já existente. Se aparecer falso
positivo que a tabela não previu, a regra sai — vira achado, não fica.

## A pendência que aponta para outra sprint: o NOTICE e os três drivers GPL

Isto **não é entrega desta sprint**, e a razão é o veredito do verificador.

O fato é verdadeiro. Medido hoje, com o cabeçalho de cada arquivo:

| Arquivo | Linha 1 | `MODULE_LICENSE` |
|---|---|---|
| `assets/dkms/hid-playstation/hid-playstation.c` | `// SPDX-License-Identifier: GPL-2.0-or-later` | `"GPL"` (`:3132`) |
| `assets/dkms/hid-nintendo/hid-nintendo.c` | `// SPDX-License-Identifier: GPL-2.0+` | `"GPL"` (`:3299`) |
| `assets/dkms/rtw88-usb/usb.c` | `// SPDX-License-Identifier: GPL-2.0 OR BSD-3-Clause` | `"Dual BSD/GPL"` (`:1504`) |

Mais 8 arquivos `.patch` nos três diretórios. O `NOTICE` tem 61 linhas e cita
apenas as regras udev derivadas do `pydualsense` e as curvas do DSX recusadas —
**zero menção a `assets/dkms/`**. O `LICENSE:1` diz "MIT License" e o
`README.md:9` (emblema) e `:346` dizem MIT sem ressalva.

**Duas correções sobre o achado original, e as duas vêm da medição do
verificador:**

1. O `rtw88-usb/usb.c` é **duplo** (GPL-2.0 **ou** BSD-3-Clause), não GPL puro.
   Numa seção de proveniência, essa diferença importa.
2. O vetor de redistribuição **não** é o pacote binário. `packaging/arch/PKGBUILD`
   não instala `assets/dkms` — cita `dkms` só em `optdepends` (`:56`); `grep -rln
   dkms .github/workflows/` devolve vazio. Quem redistribui os fontes é o
   **tarball/clone do repositório mais o instalador**, que registra os três no
   DKMS da máquina (`install.sh:587`, `:658`, `:767`).

E o principal: **isto já tem dono**. A
[CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md), aberta em 25/07,
é uma sprint inteira sobre exatamente isso, com os três diretórios em caixas de
seleção (`:26-32`) e o enquadramento jurídico já fechado (`:20-22` e `:37-41`:
*"Não há suspeita de irregularidade [...] distribuídos como fonte separada,
compilados no destino — não são linkados"*). A decisão sobre o texto do
`LICENSE` é entrega em aberto da
[CR-01](2026-07-25-CR-01-posicao-juridica.md) (`:37-38`).

Pelo padrão desta casa, dívida já diagnosticada em sprint é **pendência não
executada, não achado novo**. O que esta sprint acrescenta é uma data: a CR-05
atravessou a release **v0.4.0** sem ser executada, e uma release é justamente o
momento em que um `NOTICE` incompleto sai de casa.

## Como você valida na tela

A maior parte desta sprint é dívida de documento e não muda a janela. **Duas
coisas chegam à tela, e as duas pedem o seu olho** (regra PROVA-DE-TELA-01):

1. **O exemplo de perfil que a E1 conserta.** Abra `docs/usage/creating-profiles.md`,
   copie o primeiro bloco JSON para um arquivo `.json` e use o botão **Importar**
   do rodapé da janela. **Hoje ele recusa**, com o aviso "Falha ao importar" e o
   texto do erro de validação. Depois da E1, o mesmo copiar-e-colar entra e vira
   perfil na lista. É o teste de aceitação mais curto desta sprint e é você quem
   o faz.
2. **A janela em inglês, se a E6 for pela opção 2.** Trocar as 73 frases das
   ações por `_()` mexe em texto que aparece na sua tela, em nove arquivos de
   ação. Isso **não entra sem você ver antes e depois**, com a janela
   maximizada, aba por aba. Se for a opção 1 (rebaixar o anúncio), não há nada
   para olhar: são três parágrafos de documento.

Nada nesta sprint pede que você abra terminal. E nada aqui encosta no daemon nem
na janela abertos — as entregas são texto, gate e teste.

## Como se confere sem a tela: os dez aceites, em ordem

| Entrega | O comando que decide |
|---|---|
| E1 | o teste que valida todo bloco JSON de `docs/usage/` com `Profile.model_validate` sai verde |
| E2 | `grep -n "HEFESTO_PLUGINS_ENABLED\|config\.toml" docs/adr/017-plugin-system.md` só acha linha dentro da nota datada |
| E3 | o teste que deriva o caminho de `utils/xdg_paths.py` e o procura em `docs/protocol/ipc-unix-socket.md` sai verde |
| E4 | `grep -n "daemon.toml" docs/protocol/udp-schema.md` só acha a frase que diz que ele **não** é lido |
| E5 | o teste que compara as chaves de `_handlers` com a tabela do documento acusa **igualdade**, não inclusão |
| E6 | os três documentos dizem o que traduz e o que não traduz; o número de módulos de `app/actions/` sem `gettext` não passa de 15 |
| E7 | o teste que conta as `os.getenv` de `daemon/main.py` acha o mesmo número por extenso em `README.md`, `metrics.md` e `hotkeys.md` |
| E8 | ou a fixture existe, ou o ADR-008 tem nota dizendo que ela nunca existiu |
| E9 | `grep -rn "hefesto\.service\|HEFESTO_NO_WINDOW_DETECT" docs/adr/` só acha linha dentro de nota |
| E10 | `python3 scripts/validar-referencias-docs.py --all` sai **≠ 0** hoje e **= 0** depois de E2, E3 e E9 |

## O que fica de fora desta sprint, por escrito

- **O NOTICE e os drivers GPL.** É a CR-05, aberta em 25/07 e não executada, com
  o vetor corrigido (tarball e instalador, não pacote binário) e a licença dupla
  do `rtw88-usb` registrada. Esta sprint aponta; não assume.
- **O ADR-001 e o ADR-020.** O item 1 da DOC-VERDADE-01 persiste inteiro, e
  continua sendo a entrega 2 daquela sprint. Deixo fora de propósito: escrever
  um ADR novo sobre a arquitetura de hoje (evdev, uhid, broker, DKMS) é decisão
  de arquitetura, não correção de texto, e precisa da leitura dela — não de um
  agente decidindo sozinho o que o produto é.
- **Os dois conjuntos de "19".** O item 7 continua de pé:
  `docs/usage/interface.md:48` diz "19 disponíveis" falando dos presets da casa,
  e `docs/protocol/trigger-modes.md:7` e `:38` chamam **os mesmos 19** de
  "efeitos nomeados do DSX", enquanto `udp-schema.md:163` diz que 12 dos 19
  helpers do DSX são recusados. São três conjuntos com o mesmo número. A cura é
  um parágrafo que os separe — e ele esbarra na
  [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md),
  que está trocando os rótulos desses mesmos modos. Escrever o parágrafo agora é
  escrevê-lo duas vezes.
- **Se o `daemon.toml` deveria passar a ser lido.** Três funcionalidades hoje
  sem chave de usuário (métricas, plugins, porta UDP) e um arquivo de
  configuração resolveria as três. É decisão de produto e vive na
  [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md).
  Enquanto ela não for tomada, o documento tem de dizer a verdade de hoje.
- **`docs/history/` e `docs/research/`.** Excluídos do gate por decisão
  registrada (`validar-referencias-docs.py:81-85`) e da varredura da 01 pela
  mesma razão: contradição em documento histórico pode ser registro correto de
  decisão superada — o oposto de defeito.
- **O emblema de testes do README** (`README.md:13`, "testes-6089"). É pintado à
  mão e defasa a cada leva. Ou vira derivado do CI, ou é recalculado no release —
  e nenhuma das duas é dívida de verdade documental.
- **O `CHANGELOG.md` fora do gate.** `validar-referencias-docs.py --all` varre
  `docs/` e não cobre o arquivo na raiz; passado explicitamente, ele acha 4
  referências mortas (uma sprint que foi para a tag de arquivo e três menções a
  um script removido). São históricas por natureza, e incluir o CHANGELOG no
  gate exigiria decidir antes o que fazer com o registro do passado.

## O que eu não medi

- **Não conferi linha a linha o comportamento afirmado em `docs/usage/hotplug.md`,
  `cosmic.md`, `jogos-e-mascaras.md`, `modos.md` e `interface.md`.** Conferi as
  citações de arquivo (passam no gate) e as variáveis de ambiente (todas existem
  no código). As afirmações sobre o que o programa **faz** ficaram por conferir.
- **Não rodei nenhum comando de `cli.md` nem de `hotkeys.md` contra o daemon
  vivo.** O daemon e a janela dela estão de pé e a regra desta rodada era não
  encostar. Tudo o que digo do IPC vem de leitura estática de
  `daemon/ipc_server.py` e `daemon/ipc_handlers.py`.
- **Não olhei a janela.** Nem screenshot: a sessão é dela e capturar entra no
  meio. A afirmação de "nove abas" (`README.md:145`) segue conferida só contra o
  glade, não contra a tela.
- **Não medi se as 25 mensagens "aproximadas" dos `.po` produzem texto errado
  visível.** O `msgfmt` conta; eu não abri uma a uma.
- **Não conferi o `NOTICE` contra as dependências Python** além do
  `pydualsense` — `textual`, `platformdirs`, `jeepney` e as outras ficaram fora.
  Só olhei kernel/DKMS e regras udev.
- **Não medi quanto texto de execução existe fora de `app/actions/`.** As 73
  frases são o que consegui contar com literal de uma linha nos nove arquivos de
  ação; chamadas com variável, `f-string` de múltiplas linhas e o texto que vem
  dos diálogos não entraram na conta. **O número é piso, não teto.**
- **Não sei se ela quer o i18n de verdade.** A E6 oferece duas saídas porque a
  escolha é de produto: um projeto de uma mantenedora brasileira pode
  legitimamente decidir que a janela é em português e que o convite do
  CONTRIBUTING é que está errado.
