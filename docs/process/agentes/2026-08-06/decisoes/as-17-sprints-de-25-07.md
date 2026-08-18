# leitura complementar: as 17 sprints de 25/07 que ficaram sem cobertura

Read all 17 in full, then verified each against the tree (`src/`, `LICENSE`, sprints of 26/07–06/08, and the study `2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md`).

## Cobertura

17 de 17 lidos inteiros. Todos em `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/`.

| sprint | estado hoje |
|---|---|
| `2026-07-25-ABAS-01-...md` | **RESOLVIDA** — entregue `d92b544`; o resíduo (ABAS-11, código morto) mudou de dona para `EMULACAO-NO-JOGO-01` e `CODIGO-MORTO-01` |
| `2026-07-25-AUTO-01-...md` | **PARCIAL** — entregue `8fe735d`, com nota datada de 06/08 (o botão de co-op saiu porque o co-op deixou de ser opção). Sobra a tabela "Defaults a rever" |
| `2026-07-25-CHECKLIST-...md` | **ABERTA** — 31 caixas `[ ]`, **zero** marcadas; mesmo número de 30/07 |
| `2026-07-25-CONTAGEM-01-...md` | **PARCIAL** — E2 e E4 pagas; E1 aberta (medido: `daemon/ipc_handlers.py:1849` ainda publica `len(vistos)`, não lista), E5 aberta, E6 presa à MÁSCARA-01 |
| `2026-07-25-CR-01-...md` | **PARCIAL** — a varredura fechou pela CR-05; **a única caixa que sobra é decisão dela** |
| `2026-07-25-CR-02-...md` | **RESOLVIDA** — entregue 31/07, mordida provada por arrancamento; `profiles/curva_propria.py` existe |
| `2026-07-25-CR-03-...md` | **ABERTA** — zero código; a bancada não existe. É trabalho, não decisão |
| `2026-07-25-CR-04-...md` | **ABERTA** — bloqueada pela CR-03; `grep -rn "Trepidante" src/` → 1 ocorrência, nenhuma curva no repositório |
| `2026-07-25-CR-05-...md` | **RESOLVIDA** com uma caixa — `LICENSES/` confirmadamente não existe. Remédio escrito, é trabalho |
| `2026-07-25-CR-06-...md` | **ABERTA** — bloqueada pela CR-04; a licença do artefato é dela |
| `2026-07-25-IDENT-01-...md` | **SUPERADA** — o desenho (declarar, gesto na janela, desfazer) **caducou em 06/08** |
| `2026-07-25-INDICE-...md` | **RESOLVIDA** como índice, desatualizado (só IDENT-01 aparece aberta) |
| `2026-07-25-JOGO-01-...md` | **PARCIAL** — E1 entregue e a semântica **reescrita por ela** em 06/08; E2 migrou para `CONTAGEM-E-COOP-01`; E3 e E4 abertas |
| `2026-07-25-LEGIBILIDADE-01-...md` | **PARCIAL** — Fases 0 a 5 entregues (`tests/unit/test_contraste_css.py` existe; `app/theme.py:ESCALA_PADRAO = 3`). Falta o aceite do olho dela e a Fase 6 |
| `2026-07-25-MASCARA-01-...md` | **ABERTA / BLOQUEADA** — grau SEM PROVA declarado pela própria sprint; a dependência da IDENT-01 ficou mais dura em 03/08 |
| `2026-07-25-MIC-BT-01-...md` | **PARCIAL** — caixa 1 paga; 2, 3 e 4 sem código (só o gate `HEFESTO_DUALSENSE4UNIX_BT_MIC=1`, zero superfície no glade) |
| `2026-07-25-MIC-USB-01-...md` | **RESOLVIDA** — entregas 2, 3, 5 e 7 pagas; a 4 tem `scripts/fix_wireplumber_default_source.sh` |

## Decisões que dependem dela

### 1. Qual licença o Hefesto tem, agora que ele é "pra comunidade"

A declaração de 06/08 (*"é open source né… a ideia é ele ficar pra comunidade apenas"*, em `docs/process/estudos/2026-08-06-a-conversa-inteira-o-dia-que-a-sessao-nao-guardou.md:218`) confirma o **rumo**, e não escolhe a licença — a caixa da CR-01 continua literalmente `[ ]`, com a nota de 31/07 dizendo *"a decisão continua dela e continua aberta"*.

- **Manter MIT** — qualquer projeto, inclusive fechado, pega o código dela e não devolve nada. É o que está no disco hoje.
- **Trocar por copyleft (GPL/LGPL)** — quem distribuir derivado devolve o fonte. Coerente com os módulos DKMS que o projeto já carrega em 5 dos 7 artefatos, e com o problema que originou a série CR (curvas presas em repositório sem licença).
- **Dupla** — MIT no código, copyleft nos dados.

**Custo de não decidir:** hoje ela é a única contribuidora e trocar é uma linha. A própria sprint diz: com o projeto crescido, mudar exige concordância de **todos** — e "ficar pra comunidade" é justamente o que traz contribuidores.
**Esforço:** só responder.
**Fonte:** `docs/process/sprints/2026-07-25-CR-01-posicao-juridica.md`, §Entregas, última caixa.

### 2. O bloco de escopo fica no topo do `LICENSE`, ou desce para o rodapé

Verificado: hoje o bloco *"ESCOPO — leia antes do texto da licença"* está nas linhas 1-19 do `LICENSE`, antes do texto MIT. Foi posto ali de propósito, e o preço foi registrado "para ela pesar".

- **Fica no topo** — quem abre o arquivo lê a ressalva do `assets/dkms/` antes do juridiquês. O GitHub provavelmente deixa de rotular o repositório como "MIT" e passa a "View license".
- **Desce para o rodapé** — o GitHub volta a mostrar "MIT" na página, e a ressalva vira o que a sprint chama de *"ressalva depois do juridiquês, que ninguém lê"*.

**Custo de não decidir:** enquanto não decide, o repositório fica sem o rótulo de licença na vitrine — e isso pesa mais agora que o alvo é a comunidade, porque é o rótulo que faz alguém clicar.
**Esforço:** só responder (uma linha de edição).
**Fonte:** `docs/process/sprints/2026-07-25-CR-01-posicao-juridica.md`, §Entregas, "Custo colateral registrado para ela pesar".

### 3. Sob que licença as curvas medidas por ela saem para os outros projetos

- **CC0** — domínio público; ninguém precisa creditar, e some qualquer dúvida sobre "dado factual tem autoria?".
- **MIT** — permissiva com crédito; quem usar tem de nomear o Hefesto.
- **A mesma do projeto** — um arquivo só para tudo, e o dado herda o que o código decidir no item 1.

**Custo de não decidir:** nenhum hoje (a bancada da CR-03 não existe, então não há curva). Mas é o mesmo argumento da CR-02: decidir com zero curvas custa zero; decidir com o catálogo cheio e já publicado custa recontatar quem usou.
**Esforço:** só responder.
**Fonte:** `docs/process/sprints/2026-07-25-CR-06-devolver-ao-ecossistema.md`, §Entregas, segunda caixa.

### 4. Onde ela gasta a próxima meia hora com os quatro controles na mesa

Existem **duas listas concorrentes** para o mesmo hardware, e as duas pedem a mesma sessão dela: as 31 caixas do CHECKLIST de 25/07 (zero marcadas em treze dias) e as 41 medições do protocolo de 06/08.

- **O CHECKLIST de 25/07** — é **aceite**: confirma que oito sprints já entregues funcionam na mão dela. Fecha dívida.
- **O protocolo de 06/08** — é **descoberta**: cada item tem P0/ANTES/CONTRASTE/PREVISÃO e destrava sprints paradas.
- **As duas, nesta ordem** — mais longo, e o aceite ficaria contaminado se algo do protocolo mudar o produto no meio.
- **Aposentar o CHECKLIST de 25/07** — assumir que treze dias sem marcar uma caixa é a resposta, e parar de contá-lo como dívida.

**Custo de não decidir:** as 31 caixas seguem `[ ]` e o projeto continua sem saber se as curas de 25/07 funcionam fora do teste. O placar do estudo de 06/08 registra isso como *"nada andou em sete dias"*.
**Esforço:** sessão de teste.
**Fonte:** `docs/process/sprints/2026-07-25-CHECKLIST-validacao-em-hardware.md` (inteiro) e `docs/process/estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md`, §7.

### 5. A vibração nasce a 70% da força, sem avisar

Verificado no código de hoje: `daemon/lifecycle.py:192` traz `rumble_policy: RumblePolicy = "balanceado"` e `:193` traz `rumble_policy_custom_mult: float = 0.7`. A tabela da AUTO-01 marcou isso como default a rever e ninguém o reviu — `grep` em `docs/` não acha outra decisão sobre o assunto.

- **Manter `balanceado`** — 70% da força. Poupa bateria e ruído; o jogo entrega menos do que mandou.
- **`max`** — força cheia, o que o jogo pediu chega inteiro. Mais bateria consumida e mais barulho na mesa.
- **`auto`** — o daemon decide pelo contexto; ela não sente o mesmo em jogos diferentes.

**Custo de não decidir:** todo perfil que ela cria hoje nasce entregando 70% da vibração, e a tela não diz isso em lugar nenhum — a sensação que ela ajusta na bancada não é a que o jogo mandou.
**Esforço:** minutos com o controle na mão (jogo aberto, alternar e sentir).
**Fonte:** `docs/process/sprints/2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md`, §Defaults a rever, primeira linha.

### 6. O interruptor da ponte de microfone por Bluetooth: onde mora, e se sai do opt-in

Ela pediu isto em 03/08 (pedido 3b do `PEDIDOS-DELA-01`). Verificado: a ponte existe (`integrations/dualsense_bt_audio.py`), o subsystem sobe (`daemon/subsystems/bt_mic.py`), e **não há uma linha sobre ela no `gui/main.glade`** — só a variável de ambiente. São duas perguntas.

**Onde o interruptor vive:**
- **No card do controle, junto do medidor** — ligar está onde o efeito aparece; com quatro controles são quatro interruptores.
- **Na aba Emulação, junto do controle de mic que já existe** — um lugar só; ligar fica longe de onde o nível aparece.

**Se ela aceita o custo:**
- **Continuar opt-in** — o rádio fica intacto; ela não vê o nível de voz de ninguém no cenário-alvo (quatro por Bluetooth), que é onde ela vai usar.
- **Ligar por padrão** — ela vê quem está falando, e paga: ~35% dos reports de entrada consumidos, o firmware mudo entre 55% e 75% do tempo (causa em aberto), e a ponte disputa o contador de sequência do report `0x32` com o driver. O "Cuidado" da sprint pede medir com os quatro conectados **antes** disso, exatamente porque é o tipo de coisa que derruba tudo em partida.

**Custo de não decidir:** com quatro controles por rádio, o medidor simplesmente **some** — e "sumiu" é indistinguível de "não existe", que é a caixa 3 da mesma sprint.
**Esforço:** só responder (onde mora) + sessão de teste com os quatro por rádio (para sair do opt-in).
**Fonte:** `docs/process/sprints/2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md`, §Entregas e §Cuidado.

### 7. O aceite da fonte +3

O código foi entregue — `src/hefesto_dualsense4unix/app/theme.py:ESCALA_PADRAO = 3`, com o comentário dizendo *"medido e aprovado no orçamento de largura e altura"*. Só que o critério que a própria sprint declara não é o orçamento: é **"ela ler o rodapé sem se aproximar da tela"**. Essa caixa nunca foi marcada, a sprint segue ABERTA, e a regra da casa (PROVA-DE-TELA-01) diz que interface só fecha com o olho dela.

- **Aceitar o +3** — a sprint fecha.
- **Pedir mais** — o teto de segurança é 8 (`ESCALA_MAXIMA`); acima disso a janela deixa de caber numa tela 1080p.
- **Voltar para +2** — a sprint registra +2 como "o degrau seguro" se algo estourar.

**Custo de não decidir:** a LEGIBILIDADE-01 fica aberta indefinidamente com o código já em produção, e ninguém sabe se a queixa original (*"fontes minúsculas e cores que não permitem leitura"*) foi de fato resolvida.
**Esforço:** minutos com a tela.
**Fonte:** `docs/process/sprints/2026-07-25-LEGIBILIDADE-01-texto-legivel-alvo-clicavel.md`, §Como validar, última linha.

### 8. Onde a caixinha do Steam Input mora na aba Perfis

Descendente direta da JOGO-01/E3 (*"o botão que põe precisa do gêmeo que tira"*). A semântica já é dela — mediu em 06/08 —, falta o lugar. **Provavelmente já trazida pelo leitor anterior**: está no §"O que está ABERTO, e é DELA" do índice de 06/08. Registro aqui só para a JOGO-01 não ficar sem cobertura.
**Esforço:** só responder.
**Fonte:** `docs/process/sprints/2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md`, §Entrega 3.

## O que eu derrubei

- **IDENT-01 inteira — "ela declara qual endereço é apelido de qual".** Parecia o caso mais puro de decisão dela ("O desenho: ela declara, o projeto obedece"). Caducou. `grep -n "IDENT-01" docs/process/sprints/2026-08-06-REGRA-NAO-REGISTRO-01-*.md` aponta a nota datada §"Na varredura anterior de identidade": *"A ficha propunha declaração de identidades irmãs, gesto na janela, desfazer. Caducou em 06/08/2026, pela pergunta dela citada no topo: um registro só existe na máquina onde alguém declarou… A proposta não estava errada para o caso dela — estava errada para o alcance do defeito."* A cura tem de ser **regra**, não registro.
- **AUTO-01.2 — "Preparar co-op (N jogadores)" na aba Início.** Parecia decisão de tela. Está resolvida **dentro do próprio arquivo**, na NOTA DATADA de 06/08: o botão saiu porque o co-op deixou de ser opção. Repropor invalidaria o item.
- **JOGO-01/E1 — a allowlist derruba o vpad daquele jogo.** Parecia trade-off de risco. Ela mediu em 06/08 e a semântica é dela (`CONTROLE-SONY-MEDIDO-01`, commit `0b5a3a2`). Não se repropõe.
- **CR-05, a caixa aberta (`LICENSES/GPL-2.0.txt`).** Parecia decisão jurídica. `ls LICENSES/` → não existe, confirmado; mas a própria sprint escreve o remédio inteiro ("texto canônico, sem modificação, mais uma linha em cada um dos cinco alvos"). É trabalho com resposta certa.
- **CR-04, os nomes `Pesado`/`Macio`/`Trepidante`/`Trava`/`Dois Estágios`.** Vocabulário de produto é sempre dela — mas a sprint diz que são *"hipóteses de partida, não a lista final; a bancada é que decide"*, e a bancada (CR-03) não existe. `grep -rn "Trepidante" src/` → 1 ocorrência, nenhuma curva no repositório. Pedir o nome agora é pedir que ela batize uma sensação que ainda não pode sentir.
- **LEGIBILIDADE-01 Fase 6, "as 11 classes órfãs: ou são aplicadas, ou saem do arquivo".** A sprint chama isso de *"a decisão que falta"*. Não é dela: `grep -c` nas classes contra `gui/main.glade` → **0 usos**, e nenhuma consequência visível na tela em qualquer dos dois caminhos. É higiene técnica.
- **MIC-USB-01/E5, "`speaker.set` ou ganha superfície ou sai".** Já decidido, e registrado no código: `src/hefesto_dualsense4unix/app/ipc_bridge.py:644` — *"DECISÃO DA MIC-USB-01… Ele FICA, e ganha superfície junto com o microfone"*.
- **CONTAGEM-01, o vão vertical.** Ela já deu o desenho na própria sprint (*"essa parte vazia poderia ser os botões aparecendo maiores e mais distribuídos, e no final a parte do mic"*), e `VAO-01` / `CARD-OCUPA-01` executaram. E2 e E4 estão pagas.
