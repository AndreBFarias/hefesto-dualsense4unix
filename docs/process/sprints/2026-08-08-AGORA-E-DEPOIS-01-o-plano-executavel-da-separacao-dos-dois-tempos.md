# AGORA E DEPOIS — o plano executável da separação dos dois tempos

- **Escrito em:** 08/08/2026, noite, na branch `restauro/inicio-da-sessao`
- **Para quem:** quem for executar **sem ter vivido a sessão de 08/08**. Este
  arquivo é autossuficiente: tudo o que você precisa saber está aqui ou apontado
  com `caminho:linha`
- **O que ele resolve:** cinco dos oito defeitos da
  [OITO-DEFEITOS-01](2026-08-08-OITO-DEFEITOS-01-a-fila-que-a-verificacao-adversarial-derrubou-inteira.md),
  **por construção** — não por remendo
- **Grau:** o diagnóstico é **MEDIDO**; o desenho é **DECISÃO DELA**, aprovada em
  08/08
- **Estado (08/08, noite):** os **passos 1 a 5 estão FEITOS** — código, testes
  que mordem e foto. As quatro decisões que faltavam estão na **§9**, e o
  **passo 6** (a pendência gravada em disco, §10) é a única coisa deste plano
  que continua aberta. Falta o aceite dela na tela (PROVA-DE-TELA-01)

> **ANTES DE COMEÇAR, LEIA A SEÇÃO 6.** Ela tem oito fatos medidos que, se você
> não souber, farão você escrever uma cura que já foi escrita e revertida hoje.

---

## 1. O problema, em uma página

A janela mistura **dois tempos verbais** na mesma tela, com a mesma aparência:

| tempo | o que é | dono | quando vale |
|---|---|---|---|
| **AGORA** | cor, brilho, gatilho, vibração, microfone | o daemon | na hora — ela mexe e sente |
| **DEPOIS** | o modo e a máscara | **ela** | só quando o jogo **abre** |

Os dois são seletores lado a lado, na aba Início. Parecem iguais e **não são**:

**O jogo lê a configuração UMA VEZ, na abertura.** O wrapper termina em
`exec env "$@"` (`assets/hefesto-launch.sh:320`) — as variáveis entram no
processo e ficam. Mudar depois não alcança o jogo em curso, e mexer no
grab/vpad ao vivo invalida os handles que ele já abriu.

**Todo defeito desta noite nasceu de tentar aplicar o DEPOIS como se fosse
AGORA.** Em 08/08 isso custou, na máquina dela: uma partida sem controle nenhum,
um "Jogador 3" fantasma, e três curas revertidas.

---

## 2. O desenho aprovado

A aba Início se divide em **duas caixas com nomes diferentes**:

```
┌─ Agora ─────────────────────────────────────────────┐
│  (o que está valendo — vindo do daemon, só leitura) │
│  Controle 1 — P1 · USB · 85%                        │
│  Controle 2 — P2 · USB · 75%                        │
│  [ Reconciliar jogadores ]                          │
└─────────────────────────────────────────────────────┘

┌─ Quando o jogo abrir ───────────────────────────────┐
│  O que o controle faz agora:                        │
│    [Controlar o PC] [Jogar pelo Hefesto] [Nativa]   │
│  O jogo vê o controle como:                         │
│    [Xbox 360] [DualSense (botões PlayStation)]      │
│                                                     │
│  ● vai mudar para: DualSense (botões PlayStation)   │
└─────────────────────────────────────────────────────┘
                              [ Aplicar ]  ← o verde do rodapé
```

**A regra de ouro, e é ela que desfaz a tensão de arquitetura:**

> Não há dois donos do MESMO valor. Há o valor **vigente** (o daemon é dono, a
> caixa "Agora" ecoa) e o valor **escolhido** (ela é dona, mora na caixa "Quando
> o jogo abrir"). São **campos diferentes**, com nomes diferentes.

Isso importa porque a `AUTO-01.3` já enterrou o defeito de "dois donos da
máscara" — e uma leitura apressada deste plano o reabriria. Ver seção 6, fato 2.

---

## 3. O que cada defeito vira

| # | defeito | como este plano o resolve |
|---|---|---|
| **1** | o diálogo está no botão errado | passa a ter **um lugar óbvio**: o "Aplicar" do rodapé, que é onde a mudança sai |
| **2** | a máscara pergunta a cada clique | o clique **não aplica mais** — só marca a escolha. Nada a perguntar |
| **4** | o "Jogador 3" fantasma | ~~**impossível**: o modo nunca muda no meio da partida sem passar pelo relançamento~~ **CADUCOU em 08/08, noite** — ela decidiu que só a máscara pergunta (§9, decisão 1). O modo pendente aplica direto, e o caminho do fantasma continua aberto na `JOGADOR-3-FANTASMA-01` |
| **8** | a tela mostra o que não confere | separa "é" de "vai ser" — cada caixa tem uma fonte só |
| **3** | "1 jogador saiu" falso | ver seção 5 (é leva própria, pequena) |

**Não resolve, e é honesto dizer:** o **5** (rumble) é investigação, não desenho.
O **6** (numeração oscilante) depende da decisão 19 dela. O **7** (método) já tem
regra escrita na OITO-DEFEITOS-01.

---

## 4. A execução, passo a passo

**Cada passo é commitável sozinho e deixa a árvore verde.** Não pule a ordem: o
passo 2 depende do 1, e o 4 depende dos dois.

### Passo 1 — o campo da escolha (sem tocar a tela)

**Onde:** `src/hefesto_dualsense4unix/app/actions/home_actions.py`

Hoje `_render_home` escreve os seletores a partir do daemon a cada tique
(`:1059` `selector.set_active_id(mode)`, `:1076` idem para o flavor). **Não mexa
nisso.** Acrescente, ao lado, o estado da escolha dela:

```python
#: AGORA-E-DEPOIS-01: o que ELA escolheu e ainda não aplicou. `None` = nada
#: pendente, e a caixa "Quando o jogo abrir" espelha o vigente.
self._escolha_pendente: dict[str, str] | None = None
```

A regra do `_render_home`, e ela é a coisa mais importante deste passo:

- **enquanto `_escolha_pendente` for `None`** → os seletores espelham o daemon,
  exatamente como hoje;
- **quando houver escolha pendente** → os seletores mostram a **escolha dela**, e
  o `_render_home` **não os sobrescreve**.

**A guarda cobre o VALOR, não a visibilidade** (§9, decisão 2). A linha
`self._home_gamepad_opts.set_visible(mode == "gamepad")` (`home_actions.py:1063`,
onde `mode` é o do daemon) **fica exatamente como está**: a caixa da máscara só
nasce quando "Jogar pelo Hefesto" já está **valendo**. Ela escolheu pagar dois
Aplicar em vez de ganhar uma guarda a mais.

**Teste que morde** (o arquivo ainda NÃO existe — quem executar o cria, e o
nome sugerido é `test_agora_e_depois_01`, no padrão da casa): com escolha
pendente, dois tiques de `_render_home` seguidos não mudam o que o seletor
mostra.
Arranque a guarda e ele reprova (é o defeito de "a escolha dela volta sozinha").

### Passo 2 — o clique deixa de aplicar

**Onde:** `home_actions._on_home_mode_changed` e `_on_home_flavor_changed`.

Hoje eles chamam `apply_mode(...)` e `call_async("gamepad.emulation.set", ...)`.
Passam a **só** gravar em `_escolha_pendente` e pedir um redesenho.

**Leve o `registrar_modo_no_rascunho` junto** (§9, decisão 3). Ele hoje mora
dentro dos callbacks `_done` do IPC (`home_actions.py:1226` e `:1286`) — sem o
IPC, ninguém mais o chama, e o "Salvar este perfil" passaria a gravar perfil
**sem a seção `mode`**, em silêncio. Ele vai para o callback de sucesso do
Aplicar (passo 4): o rascunho continua descrevendo **o que ficou de pé**, nunca
uma intenção que pode ter falhado.

**Cuidado (fato 3 da seção 6):** o `_home_guard` já existe e impede que o
`set_active_id` do próprio `_render_home` dispare o handler. **Ele continua
necessário** — não o remova achando que o campo novo o substitui.

**Teste que morde:** clicar no seletor **não** produz chamada IPC nenhuma.

### Passo 3 — o rótulo do pendente

**Onde:** a caixa "Quando o jogo abrir", abaixo dos seletores.

Uma linha, no léxico da tela: `● vai mudar para: DualSense (botões PlayStation)`.
Some quando não há pendência. **Sem essa linha o plano vira defeito**: ela clica,
nada acontece na hora, e sem o rótulo ela não sabe se o clique registrou.

Texto e função pura em `app/actions/relancar.py` (ver fato 7).

### Passo 4 — o "Aplicar" aplica o DEPOIS também

**Onde:** `src/hefesto_dualsense4unix/app/actions/footer_actions.py:195-253`.

Hoje o botão manda `profile.apply_draft` com as sete seções de
`app/draft_config.py:1030-1133` — e **nenhuma delas é modo ou máscara** (fato 4).

Ele passa a, **antes** do `apply_draft`:

1. se `_escolha_pendente` é `None` → segue como hoje, sem nenhuma mudança;
2. se há pendência **e não há jogo aberto** → aplica pelo caminho que já existe
   (`mode_transition.apply_mode`), depois segue com o `apply_draft`;
3. se há pendência **e há jogo aberto** → abre o diálogo de relançamento que já
   existe (`base._perguntar_antes_de_relancar`, fato 7).

**O passo 3 vale para a MÁSCARA, não para o modo** (§9, decisão 1). Chame o
helper com `mudanca="mascara"` e ele já faz a coisa certa sozinho: `"modo"` não
está em `EXIGEM_RELANCAR` (`relancar.py:49-62`), então uma pendência **só de
modo** cai no `return False` de `base.py:87-88` e aplica direto — que é
exatamente o comportamento de hoje, e é o que ela decidiu manter. **Não devolva
`"modo"` à lista** para "fechar o caso": isso reabriria a decisão dela da
`RELANCAR-ORDEM-01` por conta própria.

**NÃO** ponha a transição de modo dentro do `apply_draft` do daemon. Fato 5
explica por quê — e o erro produz "ERRO ao aplicar" com o modo já aplicado, que
é a mentira que o `APLICAR-VERDADE-02` foi escrito para matar.

**Teste que morde:** com pendência e sem jogo, o Aplicar dispara a transição; com
pendência e jogo aberto, ele abre o diálogo e **não** dispara nada antes da
resposta.

### Passo 5 — a foto, e a palavra dela

`scripts/gui-captura/retratar_abas.py` **antes e depois**. A
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
vale inteira: interface só fecha com o olho dela.

---

## 5. A leva pequena que vale fazer junto (defeito 3)

**"1 jogador saiu — não foi você; volta sozinho"** aparece com os dois controles
dela na tela, conectados. Ele conta **jogadores virtuais**, e cada reinício do
daemon derruba e recria os vpads.

**A regra de produto, em uma linha:** *o produto fala do que ela vê.* O aviso diz
**controle**, não jogador virtual — se os físicos estão todos presentes, ele cala.

**O contrapeso, obrigatório:** quando um controle **dela** cair de verdade, o
aviso tem de aparecer. Sumir com ele nesse caso seria trocar um defeito por outro
pior, e o teste tem de travar os dois lados.

---

## 6. OS OITO FATOS QUE VOCÊ PRECISA SABER

Cada um destes custou uma cura errada em 08/08. Todos **MEDIDOS**.

1. **O jogo lê a configuração uma vez.** `assets/hefesto-launch.sh:320` termina em
   `exec env "$@"`. Nenhuma reescrita posterior alcança o processo em curso.

2. **O daemon é o dono do que a tela mostra** (`AUTO-01.3`, comentário em
   `home_actions.py:1067-1074`). Este plano **não** revoga isso: ele cria um
   campo NOVO para a escolha dela. Se você fizer os seletores "segurarem" o valor
   vigente, reabre o defeito dos dois donos.

3. **`_render_home` reescreve os seletores a cada tique** (`:1059`, `:1076`) e
   esconde a linha da máscara quando o daemon não diz `gamepad` (`:1061`). Sem a
   guarda do passo 1, a escolha dela volta sozinha — e a máscara **nem aparece**.

4. **O botão verde é o `btn_footer_apply`** (`gui/main.glade:3616-3620`, verde por
   `.btn-apply` em `gui/theme.css:836`), e o payload dele **não carrega modo nem
   máscara** (`app/draft_config.py:1030-1133`, `daemon/ipc_draft_applier.py:46-88`).

5. **Não mova a transição de modo para dentro do daemon.** `apply_mode`
   (`app/actions/mode_transition.py:159-181`) é da GUI e dispara até 3 chamadas de
   2,0 s cada; o `apply_draft` do rodapé tem `timeout_s=1.5`
   (`footer_actions.py:250`). A conta não fecha, e o resultado é "ERRO" com o modo
   aplicado.

6. **`mode_of_state` devolve só `native`/`gamepad`/`desktop`** — **nunca** o
   flavor (`mode_transition.py:198-212`). Qualquer comparação de "mudou?" que use
   só isso é **cega à máscara**. Foi assim que uma cura de hoje nunca disparou.

7. **O diálogo de relançamento JÁ EXISTE e funciona.** Módulo puro em
   `app/actions/relancar.py` (listas `EXIGEM_RELANCAR`/`MUDA_NA_HORA`, textos,
   `precisa_perguntar`), o gancho em `app/actions/base.py`
   (`_perguntar_antes_de_relancar`, `_relancar_decidir`, `_relancar_o_jogo`), e o
   construtor de diálogo em `daemon_actions.build_consentimento_dialog`.
   **Reuse — não escreva outro.**

8. **O install é editable: cura de daemon só vale no PRÓXIMO start.** Se o passo
   tocar `src/hefesto_dualsense4unix/daemon/`, reinicie antes de pedir teste —
   e **nunca** com jogo aberto. Isso já custou uma rodada inteira em 08/08.

---

## 7. O que NÃO fazer

| não faça | por quê |
|---|---|
| pôr o diálogo no "Salvar este perfil" | gesto errado, e trunca o save (rename, reload, `profile_switch`). Foi feito e revertido em 08/08 |
| fazer o `_escolha_pendente` guardar modo/máscara **e aplicá-los** no ramo "Aplicar na próxima abertura" | `base._MUDANCAS_QUE_SAO_ESCRITA` existe justamente para impedir isso: aplicar ali recria o vpad ao vivo |
| inventar vocabulário novo na tela | ela recusa nome que não deriva do que existe. "Agora" e "Quando o jogo abrir" saem do próprio produto |
| aplicar na máquina dela antes de o desenho fechar | regra de método da OITO-DEFEITOS-01: um cético responde *"o que isso quebra?"* antes |

---

## 8. Como saber que terminou

**Os portões da casa** (`CLAUDE.md`, "Antes de fechar qualquer leva"), todos em
zero, com `git add -A` **antes** — eles não veem arquivo novo.

**E o teste dela, que é o que importa:**

1. abre o Sackboy com dois DualSense;
2. vai ao Hefesto **no meio da partida**, passa pelas abas, muda a máscara;
3. **nada acontece na hora**, e a linha `vai mudar para:` aparece;
4. clica em **Aplicar**;
5. o diálogo pergunta **uma vez**, com as três saídas;
6. escolhendo *"Aplicar agora e reiniciar o jogo"*, o jogo fecha e a Steam o
   reabre com a máscara nova valendo.

**Se o passo 3 falhar, pare** — é o coração do desenho, e o resto não vale nada
sem ele.

---

## 9. AS DECISÕES DELA — 08/08/2026, noite

Quatro perguntas foram à mesa com o preço de cada saída escrito. **Estas são
decisões dela: não se repropõem.** Onde uma delas caduca algo escrito acima, a
linha antiga ficou riscada, com a data — não foi apagada.

> **AS DECISÕES 1 E 2 CADUCARAM NA MESMA NOITE, VENDO A TELA.** Ela abriu a
> janela, clicou em "Jogar pelo Hefesto" e a caixa da máscara **sumiu** — porque
> o daemon ainda estava em desktop. A leitura da tela não é "a máscara ainda não
> cabe aqui"; é "a máscara sumiu". A revisão está na **§12**, e é ela que vale.
>
> As duas ficam escritas abaixo porque explicam o raciocínio, e porque o preço
> que cada uma cobrava era real — só não era o preço certo.

### Decisão 1 — só a máscara pergunta. O modo, não.

Com jogo aberto e pendência **só de modo**, o Aplicar executa a transição **sem
diálogo**, como o produto faz hoje. A `RELANCAR-ORDEM-01` fica **de pé**.

**O preço, declarado antes da escolha e aceito:** o defeito 4 (o "Jogador 3"
fantasma) **sai do alcance deste plano**. Trocar de modo com jogo aberto continua
mexendo no `compose_env` ao vivo, e a cura daquilo é o que a
[JOGADOR-3-FANTASMA-01](2026-08-08-JOGADOR-3-FANTASMA-01-a-cura-certa-no-momento-errado.md)
já dizia que era: impedir o estado meio-a-meio, não perguntar mais.

### Decisão 2 — a caixa da máscara continua obedecendo ao daemon

Ela só nasce quando "Jogar pelo Hefesto" está **valendo**. Escolher o modo e a
máscara na mesma passada exigiria uma guarda de visibilidade, e ela preferiu o
caminho de menos código: **dois Aplicar**, um por decisão.

**Consequência que quem executar vai ver e não deve "consertar":** com o daemon em
gamepad e uma pendência de "Controlar o PC", a caixa da máscara **continua
visível**, ecoando a máscara vigente. Está certo — aquela caixa mostra o que o
daemon tem, e o Aplicar leva a pendência.

### Decisão 3 — o modo entra no rascunho quando o Aplicar confirma

Nunca no clique. O rascunho segue descrevendo **o que ficou de pé**, e um Aplicar
que falhe ou um diálogo cancelado não deixam rastro no perfil.

### Decisão 4 — a escolha adiada é gravada em DISCO

No diálogo, *"Aplicar na próxima abertura"* passa a **guardar de verdade**: a
escolha sobrevive a fechar a janela e a reiniciar o daemon, e é aplicada sozinha
**quando o jogo fechar**. O toast volta a poder dizer *"Guardado — aplico assim
que {jogo} fechar"* sem mentir.

**Isto é leva própria, e é a maior das cinco.** Ver o passo 6.

---

## 10. Passo 6 — a pendência que sobrevive (decisão 4)

**Faça-o DEPOIS dos passos 1 a 5**, e num commit próprio: os cinco primeiros
fecham sozinhos e valem por si.

Três peças, e nenhuma existe hoje:

1. **Onde gravar.** Um arquivo em `~/.config/hefesto-dualsense4unix/`, no padrão
   do `steam_input_apps.txt`. Dono: o **daemon**, não a janela — ela pode estar
   fechada na hora de aplicar, e é justamente isso que a decisão 4 promete.

2. **O gatilho.** Ele **já existe e não precisa ser inventado**: o
   `game_signal` emite `game_signal_transition {de, para, evidencia}` a cada
   mudança real de autoridade (`daemon/subsystems/game_signal.py:12-22`), com
   histerese de 30 s na queda para `daemon` (`:54-62`). A queda `game → daemon` é
   "o jogo fechou", e a histerese é uma **vantagem**: alt-tab curto não dispara a
   aplicação no meio da partida.

3. **O gesto de cancelar.** Se ela pode marcar, tem de poder desmarcar — a linha
   `● vai mudar para:` precisa de saída, e o produto não pode aplicar uma escolha
   que ela esqueceu que fez há dois dias.

**O que muda no que já existe:** o `_MUDANCAS_QUE_SAO_ESCRITA` (`base.py:50`) e o
`guardou=` do `toast_da_escolha` (`relancar.py:190-210`) nasceram da
`DEPOIS-QUE-APLICAVA-AGORA-01`, que é de 08/08 e cuja premissa era *"a janela não
tem onde guardar"*. Com o passo 6 essa premissa **deixa de valer**, e a máscara
passa a poder dizer `guardou=True`. **Enquanto o passo 6 não existir, ela não
pode** — e a linha da tela tem de sumir junto, ou a tela contradiz o rodapé.

**A proibição da seção 7 continua inteira:** guardar **não** é aplicar. O ramo
"na próxima abertura" nunca chama `apply_mode` com jogo aberto — ele escreve a
pendência e vai embora. Quem aplica é o gatilho, com o jogo já fechado.

---

## 11. O que a execução dos passos 1 a 5 aprendeu

Três coisas que não estavam no plano e que custaram tempo. Ficam escritas para
não serem redescobertas.

### 11.1 O retrato oficial precisa do Python do venv

`scripts/gui-captura/retratar_abas.py` tem shebang `python3`, e o Python do
sistema não tem `structlog` nem `platformdirs`. Rodado assim, ele **não avisa
alto**: imprime `aba Início não montada (No module named 'structlog')` no meio
de outras linhas e salva um PNG **vazio** — que passa por retrato.

**Rode `.venv/bin/python scripts/gui-captura/retratar_abas.py`.** É a armadilha
nº 1 da casa (medir contra a biblioteca errada) na roupa do instrumento de foto.

### 11.2 O retrato não fotografa estado transitório, e isso não é defeito nosso

A linha `● vai mudar para:` só existe **depois de um clique**, e o retrato
oficial renderiza um estado de daemon sem pendência — ele nunca a mostra.

Tentar forçar (montar a aba e renderizar duas vezes num roteiro próprio) produz
**foto em branco com a aba montada**: medido, com a caixa tendo os 5 filhos e o
rótulo respondendo `get_text()`/`get_visible()` corretamente. E o mesmo roteiro
contra o **código de antes desta leva**, num `git worktree` do `HEAD`, produz a
mesma foto vazia — é limitação do `OffscreenWindow`, não regressão.

**O que funciona** é a técnica que o `retratar_dialogos.py` já usava: tirar o
miolo (`tab_home_box`) do pai, pô-lo numa `Gtk.OffscreenWindow` própria,
`show_all()` no MIOLO primeiro (para medir a largura natural), `set_size_request`
e só então `show_all()` na janela.

### 11.3 Método de mixin quebra dublê parcial — de novo

`_render_pendente` nasceu método de `HomeActionsMixin` e derrubou 26 testes de
uma vez: os dublês desta base copiam handlers avulsos (`_HomeStub`), e chamada
entre mixins não existe neles. É **a mesma lição** já escrita em
`registrar_modo_no_rascunho`, paga uma segunda vez.

`reconciliar_pendente`, `render_pendente` e `marcar_escolha` são funções de
MÓDULO pelas duas razões de sempre: o rodapé precisa das mesmas, e função não
depende da montagem do dublê.

---

## 12. A REVISÃO DE 08/08 À NOITE — o que ela viu na tela

As decisões 1 e 2 da §9 foram tomadas **lendo o preço**; estas foram tomadas
**vendo o efeito**. Onde as duas discordam, valem estas — e a diferença entre
elas é a razão de a PROVA-DE-TELA-01 existir.

### 12.1 A máscara volta a aparecer com a escolha dela (revoga a decisão 2)

> *"a máscara volta ao que era. Não temos que burocratizar aí. Clico hefesto, a
> máscara aparece, clico em jogar xbox ou dualsense e ao clicar em aplicar lá
> embaixo o efeito aplica de fato. só isso"*

A visibilidade da caixa passa a seguir o **modo escolhido**, não o vigente
(`home_actions._render_home`, o `set_visible(modo_exibido == "gamepad")`). Um
"Aplicar" só, com modo e máscara decididos juntos.

**O que a decisão 2 acertava:** o custo em código é real — é uma guarda a mais.
**O que ela errava:** o preço não era "dois Aplicar", era uma caixa sumindo da
tela no meio de um gesto. Preço de código se paga uma vez; preço de tela se paga
toda vez que ela abre a janela.

### 12.2 Com jogo aberto, o modo também pergunta (revoga a decisão 1)

> *"se o jogo tiver aberto aparece o popup falando em fechar o jogo pra aplicar e
> afins. e isso vai permitir aplicar tudo que alterar em todas as abas"*

`"modo"` volta a `relancar.EXIGEM_RELANCAR`. **A opinião dela não mudou — o
LUGAR da pergunta mudou.** A `RELANCAR-ORDEM-01` tirou o modo da lista porque o
diálogo nascia no CLIQUE, antes de ela escolher a máscara; agora ele nasce no
"Aplicar", com a decisão inteira na mão. O motivo da retirada caducou.

E isto **fecha o caminho** pelo qual o "Jogador 3" fantasma era alcançado sem
aviso — o que a §3 deste plano tinha dado por perdido às 20h. A cura do estado
meio-a-meio continua sendo a `JOGADOR-3-FANTASMA-01`; o diálogo é o que impede
de chegar lá sem ela saber.

### 12.3 O contrato dos dois botões do rodapé, na palavra dela

> *"aplicar aparece lá embaixo igual já era antes e isso aplica no perfil atual
> que tá ativo e se eu clicar em salvar, ele salva as modificações de cada aba
> naquele perfil ativo"*

É o que o produto faz, e agora vale para os dois tempos: o **Aplicar** manda ao
vivo (as sete seções + o modo/máscara pendentes) e o **Salvar** persiste o
rascunho no perfil ativo. O modo entra no rascunho quando o Aplicar confirma
(decisão 3, que **não** caducou), então salvar depois de aplicar leva o modo
junto.

**O canto que fica declarado:** salvar **sem** ter aplicado grava o perfil com o
modo/máscara ANTIGOS — a escolha pendente ainda não é "o que ficou de pé". É
coerente com a decisão 3 e ninguém reclamou dele ainda; está escrito aqui para
não ser descoberto numa partida.

### 12.4 Nada disto vale só para o cabo, nem só para o DualSense

> *"cada decisão nossa não é pra funcionar só via cabo mas via bt também e deve
> ser universal, caso eu tenha 4 novos controles dual sense ou novos pro
> controler ou 8bitdo e afins"*

**MEDIDO:** o caminho da escolha pendente não lê transporte, índice, `uniq` nem
contagem de controles em lugar nenhum — modo e máscara são do **sistema**, e o
payload da transição (`plan_mode_transition`) nunca foi por-controle.

Mas "não lê hoje" é fácil de perder amanhã, então virou portão
(`test_agora_e_depois_01.py`, grupo 5):

- a escolha resiste ao tique com **1, 2 e 4** controles, por **USB e por BT**
  (parametrizado nos dois eixos);
- ela continua de pé com a **mesa vazia** — nenhum controle conectado. É o caso
  que prova a ausência de acoplamento: modo e máscara descrevem o que o sistema
  vai entregar ao jogo, não o que um aparelho faz;
- o payload do "Aplicar" **não pode** conter `uniq`, `index` nem `transport`.
  Um payload por-controle faria a máscara valer para um aparelho e não para os
  outros, e a mesa de quatro viraria quatro verdades sobre o que o jogo vê.
