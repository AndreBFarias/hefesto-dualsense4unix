# PERFIL-NASCE-CERTO-01 — o perfil do jogo nasce perdendo, e a janela não tem como consertar

- **Status:** ABERTA
- **Prioridade:** CRÍTICA — é a causa medida da queixa "o perfil do controle muda
  ao abrir o jogo", diagnosticada ao vivo em 26/07 com ela jogando
- **Aberta em:** 26/07/2026, durante uma partida de Pragmata
- **Relação:** é a causa-raiz por trás de [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md);
  aquela descreve o sintoma no daemon, esta descreve por que a configuração dela
  nunca chega lá. Absorve AUTO-03.1 e AUTO-03.2

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

### 2. A prioridade sai da tela como número

O controle deslizante 0–100 é substituído pela pergunta que ela realmente
responde, e a ordem sai dela:

```
Aplica a:  ( ) Este jogo — Pragmata          <- mais específico, vence
           ( ) Uma categoria de jogos
           ( ) Tudo (desktop)                <- catch-all, perde para os de cima
```

O número continua existindo no arquivo e no schema. Só deixa de ser uma decisão
que ela precisa tomar sem informação. O editor Avançado mantém o campo cru, com
o teto subindo para 200 para que sempre exista folga de desempate.

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
