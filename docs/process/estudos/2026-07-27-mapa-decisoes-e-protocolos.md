# Mapa: as decisões arquiteturais e os protocolos

- **Levantado em:** 26-27/07/2026
- **Escopo:** os 19 ADRs, os 4 documentos de protocolo, os 16 de uso, os 4 de
  história e as 5 pesquisas
- **Complemento:** as contradições entre esses documentos e o código estão em
  `sprints/2026-07-26-DOC-VERDADE-01-...`. Aqui fica o **conteúdo**

## Os ADRs, em uma linha cada

| ADR | Decisão | Estado real |
|---|---|---|
| 001 | `pydualsense` como backend, atrás de `IController` | **Vigente no papel, erodido de fato** — o produto migrou para evdev + uhid + broker + DKMS |
| 002 | TUI com Textual | Vigente, mas marginal — o produto é a GUI, que **não tem ADR** |
| 003 | UDP 6969 para compat DSX | Vigente; a nota de verificação desmente a própria ADR sobre `daemon.toml` |
| 004 | Daemon como `systemd --user` | Vigente, **revisado**: eliminou a dualidade normal/headless que era decisão fundadora |
| 005 | Schema de perfil v1 | Vigente, **estendido sem bump de versão** |
| 006 | Detecção de janela por `python-xlib` | Vigente para X11 |
| 007 | Wayland diferido | **SUPERSEDED pelo 014** — o único marcado assim |
| 008 | Poll fixo a 60 Hz; `transport` no estado | Vigente |
| 009 | Escopo `systemd-logind` | Vigente — distros sem logind fora de escopo |
| 010 | Probe de vivacidade do socket IPC | Vigente |
| 011 | Glyphs Unicode preservados, emojis proibidos | **Critério vigente, gate inexistente** |
| 012 | Máquina de 3 estados de reconexão da GUI | Vigente |
| 013 | Autosuspend USB desligado por device | Vigente |
| 014 | Suporte a COSMIC/Wayland | Vigente; substitui o 007 |
| 015 | Padrão de subsystems | Vigente com ressalva (o registro não é iterado) |
| 016 | Endpoint Prometheus | Vigente, **sem chave para ligar** |
| 017 | Sistema de plugins | Vigente; **o caminho de config documentado é impossível** |
| 018 | Fronteira USB: autosuspend x dropout | **Parte 2 refutada por medição** |
| 019 | WirePlumber: validar o default ATIVO | Vigente |

### Os três que ensinam mais

**ADR-010** nasceu de um sintoma real: `systemctl is-active` dizia `active` e a
GUI dizia "daemon offline" por horas, porque o smoke fazia `unlink()` cego no
socket de produção. Três medidas: probe de conexão antes do unlink, **inode
sovereign** (só desfaz o unlink se o `st_ino` ainda for o registrado), e
isolamento por variável de ambiente. Custo assumido: +100 ms no arranque.

**ADR-011** nasceu de um episódio caro: um diff leu "zero emojis" como "zero
não-ASCII", strippou os glifos de estado do código **e adaptou o teste à
regressão**, escondendo o bug. Critério objetivo: proibido é o bloco
`Emoji_Presentation`; permitido é Geometric Shapes, Block Elements, Box Drawing,
Arrows.

**ADR-018** é o melhor exemplo da cultura do repositório: a tese original
("`-71` é do AGESA/BIOS, não há alavanca de software") foi **emendada no próprio
arquivo** depois de refutada por A/B. Inclusive a correção de fato de hardware —
a máquina é Vermeer, não Matisse; o `lspci` rotula o xHCI errado.

## Protocolo IPC — socket Unix, NDJSON, JSON-RPC 2.0

Uma requisição por linha terminada em `\n`. A decisão fundadora explica por que
não há length-prefix: JSON já escapa `\n` interno, então não há ambiguidade.
Socket `0600`.

### `uniq` — o alvo por controle
Os comandos de saída aceitam `uniq` opcional (MAC de 12 hex) e, com ele, escrevem
**só** naquele controle. Omitido = broadcast.

**Exceção semântica registrada:** em `mic.set` e `speaker.set`, omitir **não** é
broadcast — é o controle primário, porque o áudio mora num handle só.

### `mic.set` tem três estados, e dois deles confundem
- `true` — muta no firmware;
- `false` — **desmuta como ORDEM**: enquanto vigorar, o hefesto é dono do
  registrador e o botão físico não manda;
- `null` — **devolve a posse** ao driver.

A chave é obrigatória: omitir levanta erro em vez de virar um "desmuta"
silencioso. Confundir `false` com `null` foi o defeito dos dois escritores do
byte de mute — o keepalive mandava `common[9]=0x00` a 60 Hz por cima do kernel.

### `identity.renumber` e `identity.number.set`
Escrevem a **fila de preferência**, nunca um número absoluto. `renumber` compacta
todos para 1..N; `number.set` permuta só entre os **presentes**, sem rebaixar quem
está na gaveta. Recusas nomeadas: `sessao_de_jogo_aberta`, `controle_ausente`,
`numero_fora_da_mesa`, `lock_timeout`.

Nota de vocabulário: é `number` e não `player` porque "jogador" já nomeia o
número do co-op.

### `mouse.emulation.set` — `enabled` é opcional
**Com** `enabled`, liga ou desliga (cria/destrói device, persiste). **Sem**
`enabled` — a rota dos controles deslizantes da GUI — atualiza só velocidade,
nunca cria device nem religa emulação desligada.

## Protocolo UDP — dois envelopes na porta 6969

Regra de decisão **por conteúdo**: `version` ausente = envelope canônico do DSX;
`version` presente e diferente de 1 = descarte com aviso.

```
{"instructions":[{"type":1,"parameters":[0,2,15,0,9,6,7,10]}]}                    <- DSX
{"version":1,"instructions":[{"type":"TriggerUpdate","parameters":[...]}]}        <- Hefesto
```

**Os ordinais divergem entre implementações**, e por isso foram conferidos em
quatro fontes: `TriggerThreshold` é **4** em TarkovDSX, DualSenseY-v2 e
ForzaDSXlegacy, e **6** no RacingDSX. Seguida a maioria; **o ordinal 6 fica sem
mapeamento de propósito**, para que o dialeto divergente falhe alto em vez de
mexer no LED errado.

### `TriggerThreshold` não é efeito háptico
É corte seco no valor analógico entregue ao pad emulado:
`valor = bruto >= limiar ? bruto : 0`, sem reescala. O DualSense **não tem campo
de limiar** no report de saída, então o Hefesto aplica no mesmo ponto que o DSX —
a fronteira controle físico para pad virtual.

Três consequências para quem escreve mod: só vale com emulação ligada; só vale
para o jogador 1; e é **pegajoso** — sobrevive à saída do mod.

### `controllerIndex` é descartado
Índice 0 é silencioso (o SDK declara constante 0). Diferente de 0 incrementa
contador e avisa, porque rotear exigiria o mapa MAC-para-jogador, que vive no
`CoopManager` e não chega ao handler UDP.

### Honestidade declarada
**Nenhum mod do DSX Windows foi executado ponta a ponta** contra este daemon. O
que foi verificado é o formato do fio, com teste automatizado e medição em socket
real.

## Modos de gatilho — dois níveis

**HID (canônico):** 10 modos + 7 forças. No report: modo e 6 forças em
`common[10..15]`, a 7ª em `common[19]`; o lado esquerdo fica adiante, e **9 bytes
adiante no Bluetooth**.

**Presets (19):** fábricas que produzem `(modo, forças)`. O multiplicador **x32**
normaliza 0-8 para 0-255. `multi_position_*` empacota 10 posições de 3 bits em 4
bytes.

Escape hatch documentado:
`test trigger --raw --mode Pulse_AB --forces 0,9,7,7,10,0,0`.

## Curvas próprias e a sala limpa

`docs/protocol/curvas-proprias.md` está **deliberadamente vazio**, e diz por quê:
a tabela será **gerada dos perfis**, nunca escrita à mão, porque registro mantido
à mão desatualiza e registro desatualizado não defende ninguém.

As quatro regras do `CLEAN-ROOM.md`:

- **R1** separação de acesso — pesquisar protocolo é livre; ler tabela de curva
  alheia, não;
- **R2** nomes próprios em português (`Pesado`, `Macio`, `Trepidante`), porque
  nome igual convida à comparação byte a byte;
- **R3** proveniência datada sem exceção — *"um único número órfão contamina a
  defesa da tabela inteira"*;
- **R4** fronteira explícita no código entre **fato do protocolo** (formato do
  report, hardware da Sony) e **criação nossa** (as curvas).

A razão jurídica: as curvas dos doze modos prontos do DSX estão transcritas num
repositório **sem licença** — `"license": null`, sem `LICENSE`, sem menção no
README. Obra sem licença permanece com todos os direitos reservados. Não há
caminho lícito.

**E a posição sobre reescrever histórico**, que vale além deste assunto:
*"reescrever onde não houve infração cria a aparência de que houve"* — o
force-push fica registrado nos forks, nos clones e no CI, e a pergunta que sobra
é "o que foi apagado?", sem que exista mais o histórico para responder.
`filter-repo` é ferramenta para vazamento de dado sensível, onde a exposição é o
dano. Decisão técnica documentada é o oposto: a exposição é a proteção.

## Pesquisa: o que foi de fato medido

**Polling USB** (6 frequências, controle físico): a CPU **cai** conforme a
frequência sobe — 9,1% a 60 Hz contra 4,7% a 1000 Hz. O custo está no
agendamento, não na leitura. Curiosidade que o CSV mostra e nenhum documento
comenta: a escolha de 60 Hz por "economia de CPU" **não é sustentada** por essa
medição.

**Forense de 25/07** — o comando que separa "o Hefesto rejeitou" de "o kernel não
viu": `journalctl -k -b <n> | grep -c "idVendor=054c"`. Contador zero prova que o
dispositivo **nunca se apresentou**, e nada em espaço de usuário age antes da
enumeração. Isso refutou a hipótese que veio junto com o relato ("algum teste
está ativado") — o cabo era físico.

O documento traz **tabela de grau de certeza por afirmação** (medido / inferido /
hipótese / indeterminado) e a regra de método: *"medir a camada mais baixa
primeiro custa um comando e economiza uma auditoria inteira na camada errada"*.

**Firmware** — as duas pesquisas trazem banner de "exploratória, sem
implementação". O protocolo está extraído (feature `0x20` metadata, `0xF4` chunk,
`0xF5` status; `DS_FIRMWARE_SIZE = 950272` exatos), o blob é **cifrado** e a chave
do DualSense continua secreta. Base legal mapeada (DMCA 1201(f), LDA art. 77,
Diretiva 2009/24/EC art. 6), e a ética declarada: o projeto pode prover helper de
download, **jamais** empacotar ou cachear o blob.

## As premissas fundadoras que ainda governam

De `docs/history/`, o ciclo foi auditoria -> decisão -> auditoria da decisão,
**antes de existir código**. As que sobreviveram:

1. **`IController` síncrona** — recusa explícita de acoplar a asyncio, porque
   backends futuros em C ou Rust também serão síncronos. É o que permitiu toda a
   migração posterior.
2. **Match AND entre campos, OR dentro de listas** — inalterado até hoje.
3. **NDJSON sem length-prefix.**
4. **Rate limit por IP, não por tupla** — cliente pode rotacionar porta de origem.
5. **Nunca adicionar o usuário ao grupo `input`** — udev seletivo e `uaccess`. É
   daí que vem o "combo sagrado" PS + D-pad, desenhado para nunca ser repassado
   ao uinput.
6. **`FakeController` desde a primeira onda; CI só com falso.** Requisitos que
   exigem hardware viram checklist manual e **não bloqueiam o CI** — é a raiz da
   cultura de níveis de prova.
7. **`NOTICE` desde o começo**, atribuindo a regra udev derivada ao pydualsense —
   a semente da disciplina que virou `CLEAN-ROOM.md` quinze meses depois.
8. **Stubs de ADR desde o dia zero**: *"stub vazio é melhor que ADR esquecida"* —
   explica por que os ADRs 001-008 são curtos e os posteriores longos.

## Um registro que vale guardar

`docs/history/releases-nao-publicados.md`: entre 21 e 23/04/2026 as tags v1.0.0 a
v2.1.0 **não produziram release nenhum** — o workflow abortava no gate de tipagem
antes dos jobs de empacotamento, que ficavam em `skipped`. Ninguém percebeu na
época.

É o precedente exato do que a `v0.2.0` corrigiu em 26/07: **trabalho entregue,
tag ausente ou release vazia, e nada avisando.**
