# Decisões que são dela, não minhas

> **TODAS RESPONDIDAS EM 21/08/2026.** O que segue guarda a pergunta, a
> recomendação original e a escolha feita — inclusive onde a escolha foi
> contrária à recomendação, que é justamente o caso que vale a pena registrar.
>
> | # | Escolha |
> |---|---|
> | D-A1 | **Dar escopo ao VETO 3** — como recomendado |
> | D-A2 | **Manter a seção 4 na leva agora** — *contrária à recomendação* |
> | D-A3 | **Criar `maquina.json`** — como recomendado |
> | D-A4 | **Aba diferida** — como recomendado |
> | D-A5 | **Espelhar com teto visível** — como recomendado |

O reconhecimento do repositório encontrou cinco pontos em que a aba proposta
esbarra em doutrina **já escrita e já paga** por este projeto. Nenhum é
impedimento técnico; todos são decisão de produto. Cada um vem com a
recomendação e com o custo de decidir para o outro lado.

~~Enquanto D-A1 e D-A2 não forem respondidas, CONFIG-01 não começa.~~
**Respondidas. CONFIG-01 está liberada.**

---

## D-A1 — O VETO 3 proíbe exatamente o que esta aba faz

`REGRA-NAO-REGISTRO-01` (06/08/2026) fixa três vetos. O terceiro:

> *"nenhuma cura que dependa de DECLARAR, CONFIRMAR ou CLICAR"*

A aba Configurações é **declarativa por construção**. A tese inteira é "o que o
produto não consegue medir, a pessoa declara". Os itens (a) topologia de rádio e
(c) controles não-Sony são, os dois, formulários de declaração.

Esta é a colisão mais grave do dossiê, e não se contorna com jeitinho de
implementação.

**Minha leitura:** o VETO 3 nasceu de um caso específico — a **cura de
identidade**, em que fazer a pessoa declarar qual controle é qual seria empurrar
para ela um trabalho que o produto tem obrigação de fazer sozinho. Ali o veto
está certo e deve continuar valendo.

Mas ele não pode ser doutrina geral, porque existe uma classe de fato que
**nenhuma medição alcança**: onde o dongle está fisicamente. Nenhum `sysfs`
distingue um hub em cima do rack de um hub embutido no monitor, e a diferença é
de metros de alcance.

**Recomendação:** manter o VETO 3 com escopo explícito — *proibido declarar o
que o produto pode medir*. Declarar o que ele comprovadamente não pode passa a
ser permitido, com duas salvaguardas escritas na própria regra:

1. **Toda declaração nasce em "não sei", e "não sei" é resposta válida.** Nada
   para de funcionar por falta de declaração.
2. **Onde a medição existe, ela pré-preenche e a declaração só corrige.**
   Declarar nunca é a primeira opção.

**Se a resposta for não:** a aba perde as seções 1, 2 e 4 e sobra o orçamento e a
janela. Continua valendo a pena, mas é outra leva — e menor.

### DECIDIDO em 21/08/2026 — dar escopo ao veto

O VETO 3 passa a valer para **o que o produto pode medir**. Declarar o que ele
comprovadamente não mede fica permitido, com as duas salvaguardas acima escritas
na própria regra.

**Tarefa que nasce daqui:** editar `REGRA-NAO-REGISTRO-01` para registrar o
escopo novo e apontar para esta leva. Um veto que muda de alcance sem deixar
rastro é pior que um veto errado. Entra em CONFIG-08.

---

## D-A2 — O escopo dos controles externos foi ditado, e a seção 4 o reabre

`external_controllers.py:11-14` carrega a fala:

> *"só uma aba pra ver como os controles aparecem, não uma super central"*

A seção 4 do desenho **configura** 8BitDo e Nintendo Pro. É exatamente a "super
central" que foi recusada.

**Recomendação: cortar a seção 4 desta leva.** Três motivos:

1. A decisão foi explícita e recente. Reabrir por conta própria corrói a
   confiança no processo.
2. A área tem **quatro perguntas abertas de medição** — modelo real do 8BitDo,
   default do `SwitchSupport` da Steam, se o modo D-input é visível, se as luzes
   do plástico respondem ao comando. Construir tela sobre isso é construir sobre
   areia.
3. Existem duas capacidades **prontas e sem chamador**
   (`ExternalMaskRegistry.set_mask` e `identity.number.set` para externos). Ligar
   as duas é entrega maior e mais honesta que um formulário novo, e cabe numa
   leva própria.

**Se ela quiser manter:** a seção 4 vira sprint isolada, depois das medições
pendentes — nunca junto com o resto.

### DECIDIDO em 21/08/2026 — manter na leva agora

**Contrário à recomendação, e a decisão é dele.** A seção 4 fica, junto com o
resto. O registro existe para que a origem da escolha não se perca, não para
reabri-la.

**O que muda no desenho, para a escolha sair bem:**

1. **A seção não promete o que depende de medição pendente.** Onde as quatro
   perguntas abertas mordem — modelo real do 8BitDo, default do `SwitchSupport`,
   visibilidade em D-input, resposta das luzes do plástico — o campo nasce em
   "não sei" e a tela diz que não sabe. Nada de valor default chutado.
2. **As quatro medições viram aceite de CONFIG-06, não bloqueio da leva.** Cada
   uma cabe em minutos e está descrita na sprint.
3. **O escopo ditado é reaberto por escrito.** `external_controllers.py:11-14`
   ganha nota datada apontando para cá — a decisão de 06/08 não some, ela passa
   a ter uma segunda data.

---

## D-A3 — Onde mora configuração que não é de perfil

Não existe. Há `profiles/` (por perfil de jogo), alguns arquivos-flag, e **nada
global**. Os três destinos possíveis, todos com problema:

| Destino | Problema |
|---|---|
| `DraftConfig` / `Profile` | É **por perfil de jogo**, trocado a cada alt-tab. Topologia de rádio é da máquina, não do jogo |
| `gui_preferences.json` | Persiste, mas **nenhum módulo de `daemon/` importa `gui_prefs`** — o daemon nunca veria a declaração |
| Método IPC novo + estado no daemon | **Não existe nada parecido com `config.set`**. É construção nova |

**Recomendação: criar o arquivo de configuração de máquina** —
`~/.config/hefesto-dualsense4unix/maquina.json` — que o dossiê aponta como já
prometido duas vezes (Bloco C e a lápide do `daemon.toml`). É a única opção que
não distorce um conceito existente.

Isso **aumenta a leva**: CONFIG-03 deixa de ser "gravar campo" e passa a ser
"criar a camada de configuração de máquina, com schema, leitura no daemon e
migração". É trabalho real, e vale ser nomeado agora e não descoberto no meio.

### DECIDIDO em 21/08/2026 — criar `maquina.json`

Com `version: 1` e schema pydantic no molde de `profiles/schema.py`. CONFIG-03 é
a maior sprint da leva e é a que sustenta as outras.

---

## D-A4 — A aba é diferida ou viva?

As duas convenções coexistem: Início é **diferida** (rascunho + "Aplicar" no
rodapé); Gatilhos e Lightbar são **vivas** (IPC no clique). Misturar as duas é a
causa registrada da sensação de "mockup".

Esta aba tem os dois tipos de conteúdo: topologia é configuração de máquina
(diferida faz sentido), orçamento tem efeito imediato visível (vivo faz sentido).

**Recomendação: a aba inteira é diferida**, com o "Aplicar" do rodapé como único
gesto de fechamento. Misturar dentro de uma aba é pior que escolher errado, e o
histórico tem várias cicatrizes de dois donos do mesmo gesto.

### DECIDIDO em 21/08/2026 — diferida

Nada vale antes do "Aplicar". Vale para as cinco seções, sem exceção.

---

## D-A5 — Agregar é mover ou espelhar?

Se o orçamento manda no brilho da lightbar, o slider da aba Lightbar fica
insensível ou continua editável?

**Recomendação: espelhar com teto visível, nunca mover.** O slider continua
editável e mostra o valor efetivo ao lado — *"100 % · limitado a 25 % pelo
orçamento"*. O padrão de gate insensível já existe (`_sync_mouse_mode_gate`), mas
usá-lo aqui esconderia a causa: a pessoa veria o controle morto sem saber por quê.

**Custo honesto:** espelhar estado entre duas abas foi a classe de bug que a
sprint `ABAS-01` curou. Se for por aqui, o valor efetivo precisa ter **dono
único** — o orçamento calcula, a aba de origem só exibe — e isso entra como
invariante de teste em CONFIG-05.

### DECIDIDO em 21/08/2026 — espelhar com teto visível

O controle da aba de origem continua editável e mostra a razão ao lado. O
**dono único** do valor efetivo é o orçamento; a aba de origem só exibe. Isso é
invariante de teste em CONFIG-05, não recomendação.
