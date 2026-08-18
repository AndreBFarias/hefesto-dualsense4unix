# PERFIL-NASCE-CERTO-01 — o perfil do jogo nasce perdendo, e a janela não tem como consertar

- **Status:** **PARCIALMENTE PAGA** — reavaliado em 05/08/2026. Dizia **ABERTA**
  até aqui, e o valor antigo fica registrado porque a mudança é datada, não uma
  correção. **A E4 foi paga**; a E3 e o resto da E4 seguem abertos. Ver a
  *"Nota datada"* logo abaixo
- **Prioridade:** CRÍTICA — é a causa medida da queixa "o perfil do controle muda
  ao abrir o jogo", diagnosticada ao vivo em 26/07 com ela jogando
- **Aberta em:** 26/07/2026, durante uma partida de Pragmata
- **Índice:** [A leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)
  — esta sprint ficou **órfã de índice** entre 31/07 e 05/08, e isso é parte do
  motivo de a E4 ter sido paga sem ninguém marcar
- **Relação:** é a causa-raiz por trás de [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md);
  aquela descreve o sintoma no daemon, esta descreve por que a configuração dela
  nunca chega lá. Absorve AUTO-03.1 e AUTO-03.2

---

## Nota datada — 05/08/2026: a entrega 4 foi paga (e o que dela NÃO foi)

**Nada acima nem abaixo foi apagado.** O texto de 26/07 continua descrevendo o
que foi medido naquele dia; esta nota registra o que mudou desde então.

### O que existe hoje na árvore

**Grau: MEDIDO**, por leitura dos três arquivos em 05/08.

| peça | onde | o que faz |
|---|---|---|
| o detector | `src/hefesto_dualsense4unix/profiles/sanidade.py` | compara os perfis **entre si**, sem daemon e sem escrever: catch-all vencendo perfil específico, catch-all com cara de jogo, prioridades empatadas, prioridade fora da faixa, catch-all demais |
| a superfície | `cli/cmd_doctor.py` — `doctor --perfis` (`:117`, `:135`) | bloco *"perfis (coerência entre eles)"*, **read-only**, e **sai com código 1** quando há achado grave — ou seja, **pode virar portão** |
| o mesmo bloco no doctor completo | `cli/cmd_doctor.py:158` | quem só roda `doctor` uma vez por mês também ouve. **Não mexe no `rc`**, pela mesma política do bloco de storm |
| a mordida | `tests/unit/test_profiles_sanidade.py` | **25 casos** |

Isto é o **arranjo exato medido em 26/07** virado em detecção: o cenário
`vitoria` any/100 + `pragmata` any/5 é o que o `_catch_all_vence_especifico`
existe para acusar, e é o que a E5 desta sprint pedia.

### O que da E4 continua ABERTO — e é a metade que o título dela nomeia

A E4 diz *"um detector de armadilha, **rodando sozinho**"*, e detalha: *"na
subida e ao salvar, e a avisar uma vez, com o botão que resolve"*.

**Grau: MEDIDO** (`git grep`, 05/08):

- **não roda na subida.** Nada no daemon chama `sanidade`. A função escrita
  justamente para isso — `verificar_perfis_do_disco()` (`sanidade.py:353`), que
  lê o disco sozinha — está exportada no `__all__` com **zero chamadores e zero
  testes**. É a
  [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
  nascendo na mesma madrugada que a catalogou;
- **não roda ao salvar.** O funil de gravação da janela
  (`app/actions/profile_writer.py`) não consulta o detector;
- **não tem superfície na janela.** A aba Perfis não mostra achado nenhum, e
  **não existe o botão que resolve**;
- **hoje o detector só existe para quem abre um terminal** — e a dona da máquina
  não abre.

**Leitura honesta:** o que foi entregue é a **regra** e o **instrumento**; o que
falta é a **fiação**. É exatamente a forma de meia-entrega que esta casa passou
a leva de 03/08 catalogando, e por isso o Status virou *parcialmente paga* e não
*paga*.

### O estado das outras quatro entregas, conferido no mesmo dia

**Grau: MEDIDO no código; SEM PROVA de aceite em uso real** — nenhuma delas foi
fechada com o olho dela.

| entrega | estado | evidência |
|---|---|---|
| **E1** — nasce com a regra do jogo em foco | **existe** | `_aplicar_nascimento_com_jogo` (`profiles_actions.py:1108`) e `_prioridade_acima_dos_catch_all` (`:1844`) |
| **E2** — o teto sobe de 100 para 200 | **existe** | `PRIORIDADE_MAXIMA = 200` (`:78`), consumido em `:1670` e `:1858` |
| **E2/3** — a tela mostra a consequência | **existe** em parte | `vencedor_da_disputa` (`:221`) e `explicacao_da_disputa` (`:264`) |
| **E3** — *"Neste jogo vai valer: X"* na aba Início | **ABERTA** | a frase não existe na árvore |
| **E5** — teste que morde | **existe** para o detector | os 25 casos acima |

#### Nota datada — 06/08/2026: a E1 vale para o jogo EM FOCO, e não para "Jogo da Steam" escolhido NA MÃO

**Nada acima foi apagado, e a linha da E1 continua verdadeira no que afirma:** o
nascimento com o jogo em foco existe e calcula a prioridade. O que caducou é a
leitura de que a E1 cobre *"o perfil do jogo nasce certo"* — ela cobre **um** dos
caminhos. Existe um terceiro caso, que a sprint de 26/07 não previa e que a
tabela acima não separa: ela escolher **"Jogo da Steam"** no seletor *"Aplica a"*
com o jogo fechado. Esse perfil sai com a escala em **0** e perde.

**Os números de linha da tabela acima também caducaram** (a E1 cita
`profiles_actions.py:1108` e `:1844`): na árvore de hoje são `:1325` e `:2125`.
Os símbolos são a âncora estável, não a linha.

**GRAU: MEDIDO** por leitura de código, cada linha reconferida em 06/08 na árvore
de hoje.

##### O mecanismo, exato: dois prefills no MESMO handler, e só um cuida da prioridade

- `_on_aplica_a_changed` (`app/actions/profiles_actions.py:1032`), ao receber
  `steam_game`, chama `_prefill_modo_de_jogo` (`:1091`, definido em `:1095`) e
  `_prefill_steam_appid` (`:1093`, definido em `:1168`). Pré-preenche o **modo** e
  o **appid**. **Nunca toca `profile_priority_scale`.**
- `_aplicar_nascimento_com_jogo` (`:1325`) é o **único** ponto da aba Perfis que
  chama `_prioridade_acima_dos_catch_all` (`:2125`) — na linha `:1368`.

Logo: o perfil que nasce porque o jogo estava em foco sai com
`max(catch-all) + 10`; o perfil montado à mão sai com o `set_value(0)` que
`on_profile_new` (`:1253`) deixou em `:1265`. Não é um caminho esquecido — é o
**mesmo handler** entregando metade da cura.

##### Onde o furo está, e onde NÃO está

O furo é do **"Salvar este perfil" da aba Perfis**: em
`_build_profile_from_editor` (`:2233`), sem fotografia de disco e sem alvo
existente (`_perfil_que_o_salvar_sobrescreve`, `:2095`, devolve `None`), vale
`prioridade_final = priority` (`:2422`) — o valor do widget, que é 0.

**O rodapé NÃO tem o furo:** `_prioridade_do_save`
(`app/actions/footer_actions.py:364-399`) calcula justamente para quem não existe
em disco (GRAVA-POR-UM-FUNIL-01). Dizer *"nasce 0"* sem qualificar faz o próximo
leitor procurar o defeito no lugar errado.

##### O que isto custa a ela, com nome de jogo

**GRAU: MEDIDO** nos presets em `assets/profiles_default/`, lidos em 06/08: os
presets de gênero são `criteria` — portanto **não** são catch-all. Como
`_chave_de_selecao` devolve `(not e_catch_all, priority)`
(`profiles/manager.py:824-831`), eles **empatam em especificidade** com o perfil
novo e **a prioridade decide**. O perfil dela em 0 perde.

Isso só morde onde o preset **também** casa aquela janela. O caso concreto é o
dela, com o Sackboy: um perfil manual em 0 perde para `coop_local` (prioridade
75, casa "Sackboy" pelo `window_title_regex`) e para `sackboy_nativo` (prioridade
80, casa `steam_app_1599660` — **a mesma janela**). Num jogo cujo título não bate
regex nenhum sobram só os catch-all, e aí a especificidade salva — que é o que o
R-01 e o R-21 já garantem.

##### O que este item NÃO é

Não contradiz o **C-02** do estudo de 05/08
(`docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md:680`),
que **REFUTA** *"a prioridade é a causa de o perfil do jogo não entrar"*. Aquele
refute é sobre **catch-all contra específico**, onde a especificidade vem antes e
o veto R-21 nem lê `priority`. Aqui os dois lados são **específicos** — e nesse
patamar a prioridade é soberana. São afirmações sobre patamares diferentes, e as
duas continuam de pé.

##### A sprint de 06/08 descreve este caminho e não registra o furo

**GRAU: MEDIDO**, por leitura em 06/08. A
[JOGOS-QUE-ELA-TEM-01](2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md)
descreve exatamente este caminho na seção **F4** — o `_on_aplica_a_changed`, o
campo livre, o `_prefill_steam_appid` — e a **F6** promete usá-lo *sem* o jogo
aberto. Nenhuma das duas menciona prioridade. As únicas linhas daquele documento
que falam de prioridade estão na **E4** (semeadura em lote, caminho que ainda não
existe), e ali a prioridade calculada é **suposta**. Ou seja: a sprint que vai
encostar neste seletor não sabe do furo. **Aquele arquivo não foi editado por
esta nota** — o ponteiro fica aqui, e ele tem aviso próprio de que os números de
linha dele envelheceram (o `_prefill_steam_appid` que ele cita em `:1125` está
hoje em `:1168`).

##### O que fazer com isto

**A cura, e é onde a assimetria mora.** O handler que **já sabe calcular** é o
`_aplicar_nascimento_com_jogo` (`app/actions/profiles_actions.py:1325`, chamando
`_prioridade_acima_dos_catch_all` em `:1368`); o que **não chama** é o
`_on_aplica_a_changed` (`:1032`). A mudança é no bloco que já dispara os dois
prefills (`:1090-1093`): aplicar `_prioridade_acima_dos_catch_all()` (`:2125`) à
escala quando `active_id` estiver em `_IDS_COM_CAMPO_LIVRE` (`:70`), com
`_new_profile` ligado e `_prioridade_tocada` (`:517`, marcado por
`_on_prioridade_tocada`, `:2058`) ainda falso — as **mesmas guardas estreitas**
que `_aplicar_nascimento_com_jogo` usa em `:1351-1364`, pelas mesmas razões.

**O teste que faltaria para MORDER.** Hoje não existe:
`tests/unit/test_empate01_a_cor_volta_a_ser_dela.py:476-514` cobre o jogo **em
foco** (nasce 110) e o desktop (continua 0), e nenhum teste da árvore exercita a
escolha **manual**. O caso novo: perfil novo, escolher `steam_game` no *"Aplica
a"* **sem** jogo em foco, digitar o appid, Salvar pela aba Perfis — a prioridade
gravada tem de ficar acima de todo catch-all do disco **e** acima do preset que
casa aquele título. Arrancada a cura, o teste vê 0 e reprova.

**O risco de mexer, e o segundo caso que o mesmo teste tem de fixar.** Trocar o
*"Aplica a"* de um perfil **já salvo** não pode mexer na prioridade dele — esse
teste tem de continuar verde. É a mesma razão pela qual o gate de "perfil novo"
do `_prefill_modo_de_jogo` está visível no chamador (`:1086-1091`) e não escondido
dentro do helper. Um remendo largo — calcular a cada `changed` — promoveria ou
rebaixaria perfis dela sem gesto dela, que é exatamente a classe de defeito que
SALVAR-NAO-REBAIXA-02 e GRAVA-POR-UM-FUNIL-01 acabaram de fechar.

### E duas armadilhas novas que esta sprint não previa

As duas foram medidas na madrugada de 05/08 e vivem em sprints próprias. Estão
aqui porque **mudam o valor prático da E1 e da E2**:

1. **a escala satura no teto** (D-26): com qualquer catch-all ≥ 190, todo perfil
   novo nasce exatamente em **200** e empata — e o desempate cai no incumbente ou
   na **ordem alfabética do nome do arquivo**. O teto de 200 da E2 resolveu o
   empate de 26/07 e **não** resolve o caso geral;
2. **três números convivem** para o mesmo conceito *"nascer acima dos
   catch-all"* — **15**, **`max(catch-all) + 10`** e os defaults **5 / 0**.
   **Ninguém reconciliou os três** (DIV-7, aberta desde 25/07).

**E o veto da casa continua valendo, e vale para esta sprint também:** os
arquivos de perfil dela **não se tocam** sem a mão dela, inclusive *"só para
normalizar"*. O detector **avisa e oferece** — nunca corrige sozinho, que é o
que a entrega 4 já dizia em 26/07 e continua sendo a decisão certa.

## O relato dela

> *"eu usava o modo steam, dualsense hefesto, e modo jogo ligado mas ao abrir o
> jogo sempre o perfil do controle muda, talvez como se fosse um teste sujando
> ele ou coisa assim"*

E, minutos depois, com o conserto já no ar:

> *"agora o controle tá no player 1 e azul"* … *"mas se abrir o jogo ele muda"*

> *"o controle muda de perfil, isso com a steam ativada ou não"*

Essa última frase é a que fecha o diagnóstico: **o defeito do perfil é
independente do Steam Input.** Foram tratados como um problema só até aqui, e
são dois.

## O que foi medido, na máquina dela, com o jogo aberto

### Os dois perfis, como estavam em disco

```
pragmata.json    match = {"type": "any"}    priority = 5      player_leds = jogador 3
vitoria.json     match = {"type": "any"}    priority = 100    player_leds = jogador 4
```

**O perfil que ela criou para o Pragmata não tinha regra de janela nenhuma.**
Nasceu `any` — casa com tudo — e com prioridade 5. O `vitoria`, também `any`,
tem prioridade 100 e vence sempre.

Consequência em três degraus, todos observados no journal:

1. **Fora do jogo**, o `vitoria` é ativado e escreve a lightbar roxa e o desenho
   do jogador 4 no controle:
   ```
   23:26:23  profile_activated  name=vitoria origin=system priority=100
   ```
2. **Dentro do jogo**, a regra R-21 veta: numa janela `steam_app_*` em que
   **todos** os candidatos são catch-all, nenhum tem autoridade. Candidato sai
   vazio:
   ```
   23:28:37  autoswitch_congelado_pelo_cadeado  candidate=  current=  wm_class=steam_app_3357650
   ```
3. **Sem perfil**, entra o modo jogo padrão — e ele entra e sai a cada vez que o
   foco troca entre o jogo e o cliente da Steam:
   ```
   23:21:41  profile_mode_aplicado    wm_class=steam_app_3357650
   23:21:46  modo_jogo_padrao_solto   wm_class=steam   motivo=janela_fora_do_jogo
   23:28:37  profile_mode_aplicado    wm_class=steam_app_3357650
   23:29:40  modo_jogo_padrao_solto   wm_class=steam   motivo=janela_fora_do_jogo
   ```

Nenhum dos dois perfis acende o jogador 1. É por isso que "o controle muda" e
"virou o player 2/3/4": não é o número que se perde, é o perfil errado que é
aplicado por cima.

### Onde o defeito nasce, no código

Três linhas, e cada uma sozinha já bastaria:

```
app/actions/profiles_actions.py:703    self._get("profile_priority_scale").set_value(0)
profiles/simple_match.py:111           return SIMPLE_MATCH_PRESETS.get(choice, MatchAny())
app/actions/profiles_actions.py:1111   prio = max(0, min(100, profile.priority))
```

1. **O perfil novo nasce com prioridade 0** (`:703`). Zero perde para todos os
   presets de fábrica, que vão de 50 a 80.
2. **O `match` cai em `MatchAny()` por omissão** (`simple_match.py:111`). O
   default silencioso do editor é o catch-all — a opção que garante que o perfil
   nunca terá autoridade numa janela de jogo, por causa da R-21.
3. **E a escala da janela trava em 100** (`:1111`). O catch-all dela está
   *exatamente* em 100.

O item 3 é o que transforma um defeito em armadilha fechada: **não existia, pela
interface, número que ela pudesse escolher para o perfil do jogo vencer o
`vitoria`.** O conserto de hoje exigiu escrever `110` direto no arquivo JSON —
um valor que a janela não aceita digitar.

Ela não errou a configuração. A janela não tinha a saída.

### O conserto aplicado hoje, à mão

```
match     : {"type":"any"}  ->  {"type":"criteria", "window_class":["steam_app_3357650"]}
priority  : 5               ->  110
player_leds: jogador 3      ->  jogador 1
```

Preservados sem toque: lightbar (46,194,126), gatilhos Pulse/Pulse, rumble
economia com passthrough, `mode: null`, e o override por controle que ela tinha.

Isto é remendo, não cura. A cura é o perfil **nascer** assim.

## O defeito de fundo, em uma frase

**A janela exige que ela conheça o modelo interno — `match`, `priority`,
catch-all, especificidade — para conseguir uma coisa simples: "quero que este
ajuste valha neste jogo".**

Prioridade numérica é conceito de implementação. Ninguém que senta para jogar
quer escolher entre 5 e 110; quer dizer *neste jogo*. Enquanto o número estiver
na tela como uma escolha livre, haverá uma combinação de números que se
autossabota — e ela vai encontrá-la, porque é ela quem usa todo dia.

## Entregas

### 1. O perfil nasce com a regra do jogo que está aberto — sem perguntar

Salvar um perfil com uma janela de jogo em foco **é** a declaração de intenção.
Não precisa de diálogo, nem de radio, nem de campo a preencher:

- `match` nasce `{"type":"criteria","window_class":["steam_app_<appid>"]}`,
  lido da janela ativa no momento do salvamento;
- `priority` nasce **acima de todo catch-all existente no disco** — calculado,
  não digitado;
- o nome sugerido é o do jogo.

Se não houver janela de jogo em foco, o comportamento atual (catch-all) continua
— aí ele está certo, porque é um perfil de desktop mesmo.

### 2. A lista de perfis fica — o que muda é ela deixar de ser adivinhação

**Decisão dela, 27/07, corrigindo a proposta anterior desta sprint:**

> *"o lance da lista de perfis, depois que vc explicou entendi como usar e vi que
> funcionam bem, talvez só deixar intuitiva, não precisamos desativar ela"*

A versão anterior propunha tirar a prioridade numérica da tela e substituí-la por
um seletor. **Está descartado.** O mecanismo funciona, ela usa, e o problema
nunca foi o controle existir — foi ele não dizer o que faz. Tirar teria custado
poder de expressão para resolver um defeito de comunicação.

O que muda:

1. **O teto sobe de 100 para 200.** É o conserto mínimo e obrigatório: com o teto
   em 100 e um catch-all em 100, não existe número que desempate. Hoje ela tem
   um perfil exatamente no teto — a folga não é luxo, é a diferença entre haver
   e não haver saída.
2. **A tela mostra a consequência, ao lado da escolha.** Enquanto ela move o
   controle, uma linha diz o que aquele número significa naquele momento:
   > *prioridade 110 — vence "vitoria" (100) e todos os presets*

   e, se o número não bastar:
   > *prioridade 5 — **perde para "vitoria" (100)**, que vale em tudo*
3. **A lista de perfis ganha a coluna que falta: quem vence onde.** Ela já mostra
   nome, prioridade e regra. Falta a leitura que ninguém consegue fazer de
   cabeça com treze perfis — qual deles vale na janela que está aberta agora.
4. O editor Simples continua oferecendo "Este jogo / categoria / tudo" como
   atalho, e o Avançado continua com o campo cru. **Os dois caminhos ficam.**

O princípio: o número não é o problema; **o número sem consequência visível é.**

### 2b. Nascer certo continua valendo

A entrega 1 (o perfil nasce com a regra do jogo em foco e prioridade calculada
acima dos catch-all) **não** é afetada por esta correção. Ela resolve o caso de
quem não quer pensar em prioridade nenhuma; a entrega 2 resolve o caso de quem
quer — e hoje nenhum dos dois funciona.

### 3. A janela diz qual perfil vai valer — antes de abrir o jogo

Uma linha, na aba Perfis e na aba Início:

> **Neste jogo vai valer:** Pragmata

E quando houver captura, ela diz quem está capturando:

> **Atenção:** o perfil **vitoria** vale em tudo e tem prioridade 100 — ele vence
> os perfis dos seus jogos.  [ Restringir ao desktop ]

Hoje não existe nenhuma superfície onde ela pudesse ter descoberto isso. A
informação existia inteira no disco e em lugar nenhum da tela.

### 4. Um detector de armadilha, rodando sozinho

Perfil `any` com prioridade ≥ a de qualquer perfil específico é uma configuração
que **sempre** vai machucar, mais cedo ou mais tarde. O Hefesto passa a detectar
isso na subida e ao salvar, e a avisar uma vez, com o botão que resolve.

Não corrige sozinho: corrigir o perfil dela sem pedir é a classe de defeito que
esta casa passou a leva inteira consertando. Avisa e oferece.

### 5. Teste que morde

- Criar perfil com janela de jogo em foco tem de produzir `MatchCriteria` com o
  `window_class` daquele jogo, e prioridade **maior** que todo catch-all do
  disco. Arrancar o cálculo de prioridade tem de reprovar.
- Um cenário com dois catch-all (um em 100) mais um perfil de jogo tem de
  resolver para o perfil do jogo — e reprovar se o catch-all vencer.
- O detector de armadilha tem de disparar no arranjo exato medido hoje
  (`vitoria` any/100 + `pragmata` any/5) e ficar calado quando o perfil do jogo
  tem `match` específico.

## Como você valida

Sem terminal, sem log.

1. Abra o Pragmata. A cor e os gatilhos que você deixou **continuam** — não
   viram os do `vitoria`.
2. Alt-tab para a Steam e volte ao jogo três vezes. Nada muda de cor nem de
   número no meio do caminho.
3. Abra a aba Perfis com o jogo aberto: a linha diz **"Neste jogo vai valer:
   Pragmata"**.
4. Crie um perfil novo com outro jogo aberto. Abra o arquivo pela janela: ele
   nasceu amarrado àquele jogo, não em "Tudo".
5. Volte ao desktop: o `vitoria` volta a valer, como antes.
6. Se você tiver um catch-all de prioridade alta, a janela avisa **antes** de o
   problema acontecer.

**Critério que resume:** você nunca mais precisa saber o que é "prioridade" para
que o ajuste que você fez num jogo continue lá quando o jogo abrir.

## O que NÃO foi medido

- **Não medi se o flip-flop do modo jogo para depois deste conserto.** Ele tem
  causa própria (`profiles/autoswitch.py:237` chama o modo padrão **antes** do
  cadeado, de propósito, e `daemon/lifecycle.py:1812` registra que isso é
  decisão). Com o perfil específico vencendo, o caminho do modo padrão deixa de
  ser exercido nesse jogo — mas **não confirmei ao vivo**. É de PERFIL-JOGO-01.
- **Não medi quantos perfis dela estão nessa armadilha.** Conferi `pragmata` e
  `vitoria`. Há treze arquivos em disco, e dois deles (`fallback`, `meu_perfil`)
  também são `any`, ambos em prioridade 0 — inofensivos hoje, mas não conferi os
  demais um a um.
- **Não medi o caminho do editor Avançado.** O diagnóstico é do editor Simples,
  que é o que ela usa. O Avançado pode ter comportamento diferente ao nascer.
- **Não sei qual perfil ela queria que valesse fora do jogo.** Presumi que o
  `vitoria` continua sendo o de desktop e não o toquei. Se ele foi criado para
  ser o perfil do Pragmata, a leitura muda e o conserto de hoje precisa ser
  revisto com ela.
- **O `window_class` de jogos fora da Steam não foi verificado.** Para Steam é
  `steam_app_<appid>`, medido. Para jogo fora da Steam, o campo existe mas não
  testei o caminho de nascimento.
