# DOC-VERDADE-01 — a documentação descreve, em vários pontos, outro programa

- **Status:** ABERTA
- **Prioridade:** MÉDIA — não impede jogar. Mas é a classe de defeito que já
  produziu erro de produto duas vezes nesta casa, e o custo cresce sozinho
- **Aberta em:** 26/07/2026, a partir de um estudo do repositório inteiro
- **Origem:** varredura completa de `docs/` contra o código em `src/`

## Por que esta sprint existe

Este repositório tem uma qualidade rara: ele registra quando errou. Notas de
verificação dentro dos ADRs 003, 008 e 016; banner `SUPERADO` na pesquisa de
maio; dois erros de análise preservados de propósito na validação dos quatro
controles. Isso é ativo, não passivo.

Só que a varredura que produziu essas notas, em 25/07, **parou no meio**. Ela
cobriu ADR-003, ADR-008, ADR-016 e quatro páginas de `usage/`. Não chegou aos
documentos de protocolo nem aos ADRs 010, 014, 015 e 017.

E o precedente já cobrou o preço duas vezes:

- `docs/usage/metrics.md` ensinava **duas** formas de ligar métricas, as duas
  ficção — corrigido em `5115aac`.
- A aba Emulação chamava o Mullet Mad Jack de "jogo que só entende controle de
  Xbox", o que é falso; quem lia o código acertava, quem lia a tela errava
  (`47921f8`).

Documentação errada não fica parada: ela vira texto de tela, vira decisão de
quem contribui, e vira defeito de produto.

## O que foi medido

### 1. O ADR-001 elege um backend que o produto não usa mais

`docs/adr/001-pydualsense-backend.md` decide `pydualsense` como backend HID,
isolado atrás de `IController`. Está marcado **aceito** e nunca foi revisado.

Desde então o produto incorporou, sem que nenhum ADR registre:

- `core/evdev_reader.py` — fonte **primária** de input, contornando o driver;
- `integrations/uhid_gamepad.py` — device HID próprio via `/dev/uhid`;
- `broker/hidraw_broker.py` — serviço root com injeção de descritor;
- `core/ds_output_report.py` — envelope de saída reescrito **contra o kernel**,
  porque o da `pydualsense` é malformado no Bluetooth;
- três módulos de kernel próprios em `assets/dkms/`.

O ADR não está errado sobre o que decidiu em abril. Está errado como retrato do
que o programa é hoje, e é o primeiro documento que alguém lê para entender a
arquitetura.

### 2. Três caminhos diferentes para o mesmo socket

| Documento | Caminho que afirma |
|---|---|
| `docs/adr/010-ipc-socket-liveness-probe.md` | `$XDG_RUNTIME_DIR/hefesto/hefesto.sock` |
| `docs/protocol/ipc-unix-socket.md` | `$XDG_RUNTIME_DIR/hefesto-dualsense4unix.sock` |
| `docs/usage/hotkeys.md`, `troubleshooting.md` | `$XDG_RUNTIME_DIR/hefesto-dualsense4unix/hefesto-dualsense4unix.sock` |

Os exemplos de `usage/` são os que funcionam. O documento **de protocolo** — o
que deveria ser canônico — é o que está errado.

### 3. `udp-schema.md` afirma duas coisas que não existem

- Linha ~195: a porta é *"Configurável em `~/.config/hefesto-dualsense4unix/daemon.toml`"*.
  **O daemon não lê `daemon.toml`.** A nota de verificação do ADR-003 e
  `docs/usage/hotkeys.md` já dizem o contrário, no mesmo repositório.
- O mesmo arquivo diz que **não** há validação pydantic no caminho UDP, enquanto
  `docs/adr/003-udp-port-6969-compat.md` decide que há.

Consequência que já chegou à tela: a aba Emulação tem um botão **"Ver
daemon.toml"** que abre um arquivo que o daemon não lê — o próprio arquivo diz
isso na primeira linha. Registrado em
[CONTAGEM-01](2026-07-25-CONTAGEM-01-a-tela-diz-dois-com-quatro-na-mesa.md).

### 4. Os ADRs falam de um pacote com outro nome

ADRs 010, 014, 015 e 017 referenciam `src/hefesto/…`, `~/.config/hefesto/` e
`hefesto.service`. Os nomes reais são `hefesto_dualsense4unix`,
`~/.config/hefesto-dualsense4unix/` e `hefesto-dualsense4unix.service`. O
ADR-014 mistura os dois **no mesmo arquivo**.

### 5. O ADR-017 repete o buraco que já matou as métricas

`docs/adr/017-plugin-system.md` manda ativar plugins por
`~/.config/hefesto/config.toml` (`plugins_enabled = true`). Esse caminho é
impossível pela mesma razão que tornou as métricas inalcançáveis: **o daemon não
lê arquivo de configuração**. O ADR-016 já ganhou nota de verificação por isso; o
017 não ganhou, e é o próximo a cobrar.

### 6. A tabela de métodos do IPC lista 10 de 33

`docs/protocol/ipc-unix-socket.md` traz uma tabela "Métodos v1" com dez entradas.
`daemon/ipc_server.py:99-144` registra **33**. Faltam da tabela, entre outros,
`mic.set`, `speaker.set`, `identity.renumber`, `identity.number.set`,
`led.player_set`, `daemon.state_full`, `plugin.list`, `plugin.reload`,
`controller.target`.

### 7. "19 modos" nomeia dois conjuntos diferentes

`docs/usage/interface.md` diz que a aba Gatilhos tem "19 disponíveis";
`docs/protocol/trigger-modes.md` chama sua lista de "os 19 efeitos nomeados do
DSX". Mas `docs/protocol/udp-schema.md` e o `NOTICE` dizem que **12 modos do DSX
não existem aqui**. São conjuntos distintos com o mesmo número, e a coincidência
faz parecer que a cobertura é total.

### 8. `Rigid` e `Medium` estão em colisão com a regra de sala limpa

`2026-07-25-CR-02-formato-e-proveniencia.md` exige um guarda que **rejeite** os
doze nomes do DSX, `Rigid` e `Medium` entre eles. Mas:

- `Rigid` é o nome canônico do modo HID de baixo nível
  (`core/trigger_effects.py:27-39`) — **fato de hardware da Sony**, não curva de
  terceiro;
- e o perfil de exemplo de `docs/usage/creating-profiles.md` usa
  `"mode": "Medium"`, que `udp-schema.md` lista como **não traduzido**.

O guarda da CR-02, escrito como está, reprovaria um nome de hardware legítimo e
um exemplo da própria documentação. A fronteira entre *fato do protocolo* e
*criação de terceiro* — que é a regra R4 do `CLEAN-ROOM.md` — não está resolvida
para esses dois nomes.

### 9. Uma violação viva do ADR-011

`docs/adr/011-glyphs-vs-emojis.md` proíbe o bloco Emoji_Presentation e permite
Geometric Shapes, Block Elements e Box Drawing.
`docs/usage/troubleshooting-8bitdo.md`, linhas 29 e 48, usa **U+2B50 WHITE MEDIUM
STAR** — que é Emoji_Presentation, portanto proibido. Os gates não pegaram
(tratado em [PROMESSA-NAO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md)).

## Entregas

1. **Terminar a varredura de 25/07**, nos alvos que ela não alcançou: os quatro
   documentos de `docs/protocol/`, e os ADRs 001, 010, 011, 014, 015 e 017. O
   formato já existe e é bom — a nota de verificação datada no topo, sem reescrever
   a decisão original.
2. **ADR-020, novo: "o backend deixou de ser um só"** — registrando evdev, uhid,
   broker e DKMS como as camadas que hoje conversam com o hardware, e marcando o
   ADR-001 como *emendado* (não superado: a decisão de isolar atrás de
   `IController` continua valendo, e foi ela que permitiu a migração).
3. **Um caminho canônico para o socket**, escrito no documento de protocolo e
   derivado de `utils/xdg_paths.py`, não digitado.
4. **Corrigir `udp-schema.md`** nos dois pontos, e **remover o botão "Ver
   daemon.toml"** da aba Emulação ou fazê-lo abrir o que o daemon realmente lê.
5. **Gerar a tabela de métodos do IPC**, em vez de mantê-la à mão. Uma tabela
   escrita à mão desatualiza; foi assim que ela virou 10 de 33.
6. **Resolver a colisão `Rigid`/`Medium`** antes de a CR-02 escrever o guarda:
   a lista de nomes proibidos é sobre **curvas**, e precisa excluir os nomes de
   modo HID que são fato de hardware.
7. **Um gate que impede a volta**: uma varredura que reprova quando um documento
   cita caminho de arquivo, variável de ambiente ou método de IPC que não existe
   no código. Começa pelos casos acima e cresce.

## Como você valida

Esta sprint não tem validação de olho na janela — é dívida de documento. A
validação é:

1. Abrir qualquer ADR e o que ele descreve existir com aquele nome no código.
2. Copiar um comando de `docs/protocol/` e colar no terminal: funciona.
3. Um documento novo que cite um caminho inexistente **reprovar** no gate.

## O que NÃO foi medido

- **Não conferi `docs/history/` contra o código.** São documentos declaradamente
  históricos, e uma contradição ali pode ser registro correto de uma decisão
  superada — o oposto de defeito. Precisa de critério antes de varrer.
- **Não medi quantos comentários no código apontam para docs movidos.** O README
  menciona 20 que citam `docs/process/...`; não os conferi um a um.
- **Não sei se `daemon.toml` deveria passar a ser lido** em vez de as menções
  serem apagadas. Há três funcionalidades hoje sem chave de usuário (métricas,
  plugins, porta UDP) e um arquivo de configuração resolveria as três de uma vez.
  Isso é decisão de produto, não de documentação, e está em
  [PROMESSA-NAO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md).
