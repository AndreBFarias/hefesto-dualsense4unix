# PERFIL-REESCRITO-NA-PARTIDA-01 — o perfil dela era reescrito sozinho no meio da partida

- **Achado em:** 05/08/2026, na madrugada, lendo o journal do daemon de produção
  dela **durante uma sessão de Sackboy viva**. Nenhum dos seis itens estava
  sendo procurado: a leva tinha ido investigar a **escrita** de perfil, e o que
  apareceu foi o que acontece **depois** que o perfil está escrito
- **Estado:** **CURA APLICADA nos seis itens**, com teste que morde em **dez**
  dos dezoito casos
- **Gravidade:** **ALTA** — atinge a experiência dentro do jogo: gatilhos, cor,
  máscara do gamepad, vibração e a emulação de mouse/teclado do desktop
- **Causa-raiz:** **PROVADA no código nos seis itens**; **MEDIDA no journal
  dela** em quatro (1, 2, 3 e 4). Ver *"Como ler os graus"*
- **Leva:** [O sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)
  (itens D-17, D-19, D-20, D-21, D-22, D-23 e D-24 daquele estudo)
- **Parentes, e distintas:**
  - [TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md)
    — irmã da mesma noite. Aquela é sobre a **ordem** do clear da trava manual
    na rota **manual**; esta é sobre o que a ativação **não conta** e sobre o
    que o **autoswitch** faz sozinho. Ver *"Por que não é a TRAVA-QUE-SOLTA-TARDE-01"*;
  - [ÁUDIO-QUE-TRANCA-01](2026-08-03-AUDIO-QUE-TRANCA-01-um-toque-no-volume-congela-a-troca-de-perfil.md)
    — mesmo campo (`manual_override_categories`); esta sprint **relata** o que
    aquela trava silencia, e **não** cura a trava;
  - [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md)
    — o pano de fundo: os perfis dela viraram catch-all, e é isso que arma
    quatro dos seis itens abaixo;
  - [ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
    — o padrão do item 6: a decisão certa tomada numa rota e o preço colateral
    pago nas outras.

---

## Como ler os graus

Esta sprint marca cada afirmação, porque **quatro dos seis itens têm journal e
dois não têm**:

- **MEDIDO** — há linha de journal da máquina dela, leitura direta do disco
  dela, ou execução verificada por mim hoje;
- **SUSPEITA COM MECANISMO** — o caminho de código foi lido e fecha, mas o
  efeito específico não foi observado;
- **SEM PROVA** — dito, não medido. Fica dito assim.

**Aviso que vale para o documento inteiro (MEDIDO):** o daemon vivo na máquina
dela é o **PID 1670, no ar desde 04/08 23:39:46**. Todas as curas desta sprint
são posteriores. **Nada disto está rodando lá.** O journal citado é, portanto,
o do produto **de ontem** — que é exatamente o que o torna prova do defeito, e
o que impede que ele sirva de prova da cura.

---

## O sintoma

Ela está jogando. Escolhe o perfil do jogo na janela — clica **Ativar** —, e
por um instante está tudo certo.

Aí, **sem que ela toque em nada**, a coisa anda sozinha: o controle muda de cor,
a vibração muda de força, a máscara do gamepad se rearranja, e o mouse e o
teclado do controle simplesmente **param de funcionar no desktop** e não voltam.
Ela clica "Ativar" de novo. E de novo. **Quatro vezes**, num intervalo de dois
minutos, no meio da partida.

E o daemon responde **"ativado"** todas as vezes — sem nunca dizer que metade
do perfil não entrou.

## A prova, com o daemon de produção dela

Tudo abaixo é `journalctl --user -t hefesto-dualsense4unix`, PID 1670, na noite
de 04 para 05/08. **MEDIDO.**

### A crença do autoswitch estava 2 h 44 min atrasada

```
04/08 23:40:18  profile_activated  name=vitoria origin=system  priority=0
05/08 00:03:22  profile_activated  name=vitoria origin=manual   priority=0
...
05/08 02:24:41  autoswitch_cadeado_cedeu_a_regra_de_jogo  candidate=sackboy_nativo  current=
05/08 02:24:42  profile_activated  name=sackboy_nativo origin=autoswitch priority=200
05/08 02:24:42  profile_autoswitch adiado=[] from_=None to=sackboy_nativo wm_class=steam_app_1599660
```

**`current=` vazio. `from_=None`.** O perfil `vitoria` estava ativo **desde o
boot**, e ela ainda o reativou na mão às 00:03:22. O autoswitch não sabia de
nada disso: para ele, **nenhum perfil jamais tinha sido ativado nesta sessão**.

Dois campos independentes do journal — o do cadeado e o da troca — mentem a
mesma mentira, porque leem a mesma variável.

### A supressão de mouse e teclado só sabia ligar

```
02:24:42  emulation_suppressed_changed  suppressed=True
02:28:08  emulation_suppressed_changed  suppressed=True
02:30:29  emulation_suppressed_changed  suppressed=True
02:51:25  emulation_suppressed_changed  suppressed=True
```

**Quatro transições para `True`. Zero para `False`** em toda a vida do daemon
(contagem literal: `grep -c "suppressed=False"` devolve **0**). E o perfil ativo
dela, lido hoje direto do disco:

| arquivo | prioridade | `match` | `suppress_desktop_emulation` |
|---|---|---|---|
| **`sackboy_nativo.json`** | **191** | **`any`** (catch-all) | **`true`** |
| `vitoria.json` | 0 | `any` | `false` |
| `meu_perfil.json` | 1 | `any` | `false` |
| `fallback.json` | 0 | `any` | `false` |
| `pragmata.json` | 5 | `any` | `false` |

Um catch-all com `suppress: true` **ligava**; e nenhum outro catch-all tinha
autoridade para desligar.

### A política de vibração era revertida dentro da partida

```
02:24:42.182270  profile_rumble_policy_reverted  mult=0.7 policy=balanceado
02:24:42.182400  profile_autoswitch  ... wm_class=steam_app_1599660
```

**130 microssegundos** separam as duas linhas: a reversão da política de rumble
aconteceu **no mesmo tique** que leu a janela do **jogo em foco**. E de novo às
`02:48:56`, na quarta tentativa dela de reativar o `sackboy_nativo` na mão.

### E o relatório da ativação não contava nada disso

```
02:48:56  profile_apply_respeita_override_manual  categorias=['led','rumble','trigger']  profile=sackboy_nativo
02:48:56  profile_activated  name=sackboy_nativo origin=manual priority=22
02:51:10  profile_apply_respeita_override_manual  categorias=['led','rumble','trigger']  profile=sackboy_nativo
02:51:10  profile_activated  name=sackboy_nativo origin=manual priority=191
```

São **sete** ocorrências de `profile_apply_respeita_override_manual` na sessão.
Em todas, a resposta que sobe para a janela é **"ativado"**, e as categorias
puladas ficam só no journal — que ela não lê.

E o **modo jogo padrão** apareceu **quatro** vezes recusando trabalhar
(`estado=ignorado_sem_jogo`, `estado=adiado_lock_manual`) sem **nenhum** canal
para o relatório.

### A dança das prioridades, que é de outra sprint

O mesmo `sackboy_nativo` aparece no journal com **`priority=200`** (02:24 a
02:29), **`priority=22`** (02:29 a 02:48) e **`priority=191`** (02:49 em
diante) — o número mudou **duas vezes em vinte minutos**, e hoje o disco tem
191.

**Isto NÃO é esta sprint.** É a escrita de perfil, e a origem do 191 continua
**indeterminada** (DIV-1 do estudo da leva: catraca do rodapé, arrasto do
slider ou o cenário "Novo perfil + nome existente" — três teses incompatíveis,
e o instrumento que decide, o `profile_salvo`, só nasceu nesta madrugada). Está
aqui por um motivo só: **é o que explica por que quatro dos seis itens desta
sprint ficaram agudos agora**. Com os perfis dela virados catch-all, os buracos
de simetria que ninguém sentia passaram a doer todos ao mesmo tempo.

---

## Os seis itens, e a causa-raiz de cada um

### Item 1 — a crença do autoswitch era cega aos gestos dela

**Grau: MEDIDO.**

`AutoSwitcher._current_profile` tinha **um único escritor em toda a árvore**: o
commit do próprio `_activate` (`profiles/autoswitch.py:670`; confirmado por
`git grep -n "_current_profile" -- src/`). **Nada** o sincronizava com
`store.active_profile`, que é onde `ProfileManager.activate` publica o perfil
ativo em **toda** ativação, de qualquer origem.

O portão da troca é `autoswitch.py:405`:

```python
if stable and candidate and candidate != self._current_profile:
```

Com a crença presa em `None`, `candidate != None` é **sempre verdade**. O
autoswitch "entra" num perfil que **já é o ativo** e reescreve gatilhos, LEDs,
modo e política de rumble por cima do que ela acabou de escolher na mão. É a
linha `from_=None to=sackboy_nativo` do journal, com `vitoria` ativo havia
2 h 44 min.

**É o item de maior alcance da leva**, porque ele é a porta pela qual os itens
2, 3 e 4 entram: cada reativação indevida dispara os quatro appliers de novo.

### Item 2 — a supressão de emulação era uma armadilha de mão única

**Grau: MEDIDO no código e no disco; SUSPEITA COM MECANISMO no efeito
observado.**

`daemon/lifecycle.py`, `apply_profile_suppression` (`:1552`): o ramo que
**LIBERA** sempre teve o gate de catch-all (R-02, `_perfil_tem_opiniao`); o
ramo que **LIGA** não tinha **nenhum**. Aceitava a ordem de qualquer perfil —
inclusive de um catch-all, que por definição chegou ali porque **nenhuma regra
casou**.

O que a assimetria produz com o disco dela: `sackboy_nativo` (catch-all,
`suppress: true`) liga; e como todos os outros perfis dela também são catch-all,
**nenhum consegue desligar**. O mouse e o teclado do controle morrem no desktop
até um gesto manual dela.

**Honestidade sobre o que o journal prova e o que não prova:** as quatro
transições para `True` e as zero para `False` são MEDIDAS. A **atribuição** de
que a armadilha causou a ausência de `False` é SUSPEITA COM MECANISMO — a única
tentativa de liberar registrada na sessão (`02:30:45
profile_suppression_skipped_manual_lock desired=False remaining_sec=13.7`) foi
barrada **antes** pelo lock de gesto manual, e nunca chegou ao gate. O que
fecha o caso no código é a leitura do ramo; o journal dá o contexto.

**Duas fontes da casa já avisavam por escrito**, e é isso que torna o item
grave: `app/draft_config.py:697` e o veto nº 3 da `PERFIL-SALVA-TUDO-01`. **A
escrita da janela produziu exatamente a configuração que dois documentos
proibiram.**

### Item 3 — a política de rumble não tinha guarda nenhuma

**Grau: MEDIDO (o evento); SUSPEITA COM MECANISMO (qual guarda barraria cada
um).**

`apply_profile_rumble_policy` (`lifecycle.py:2398`) é o terceiro irmão de
`apply_profile_mode` e `apply_profile_suppression`. Os dois primeiros já tinham,
no ramo de reversão, as **duas** guardas — `catch_all_sem_opiniao` e
`janela_de_jogo_em_foco`. Este **não tinha nem uma**.

Não podia ter: o applier **nem recebia o perfil**. A assinatura terminava em
`(policy, custom_mult, *, origin)`. Sem `profile=`, o daemon não conseguia
distinguir *"o perfil deste jogo não quer política"* de *"caiu num catch-all
porque nenhuma regra casou"* — e a segunda hipótese revertia a vibração
**dentro da partida dela**, que é o `profile_rumble_policy_reverted` das 02:24:42
e das 02:48:56.

**A doutrina R-02 não tem por que valer para dois eixos e não para o terceiro:
ausência de regra não é ordem, em nenhum deles.**

### Item 4 — o relatório da ativação omitia o que não entrou

**Grau: MEDIDO.**

Duas metades, e nenhuma delas era um bug de cálculo — era um valor **calculado
e jogado fora**.

**(a) as categorias travadas na mão.** `ProfileManager.apply` (`manager.py:267`)
já sabia quais categorias iria pular: consulta `_categorias_travadas()`, emite
`profile_apply_respeita_override_manual` no journal e converte os campos
correspondentes em `None` no `OutputSpec`. Só que `apply` **não recebia o
`relatorio`** — o `activate` (`:201`) o repassava a `apply_emulation` e não a
`apply`. Resultado: o `profile.switch` responde `"ativado"` com uma lista de
seções que **não menciona** o gatilho e a cor que ficaram de fora.

**(b) o modo jogo padrão.** É o único eixo que o tique mexe **fora** do
`ProfileManager` — o daemon liga o vpad quando é jogo e nenhum perfil opina. O
par `aplicar_modo_jogo_padrao` / `reverter_modo_jogo_padrao` já **devolvia
estado** no vocabulário certo (`aplicado`, `adiado_lock_manual`,
`ignorado_sem_jogo`, `ignorado_gesto_dela`), e `_sincronizar_modo_jogo_padrao`
(`autoswitch.py:433`) **descartava o retorno**.

**O agravante que fecha o caso** (do estudo da leva, D-12): a janela também
descartava o relatório inteiro. **Os dois canais que poderiam contar isso a ela
estavam fechados ao mesmo tempo** — o daemon não preenchia, e a janela não lia.

### Item 5 — o log do autoswitch contava metade

**Grau: MEDIDO no código; SUSPEITA COM MECANISMO no efeito sobre o journal
dela.**

`autoswitch.py`, no `profile_autoswitch`, o campo `adiado=` era montado assim:

```python
adiado=[secao for secao, estado in relatorio.items() if estado.startswith("adiado")]
```

O filtro deixa passar **só** `adiado*`. Logo `ignorado_catch_all`,
`ignorado_janela_de_jogo`, `ignorado_trava_manual`, `ignorado_gesto_dela`,
`ignorado_sem_jogo` e `falhou` **nunca apareciam** — e são justamente os
estados em que a ativação *"deu certo"* **sem aplicar a seção**. O journal
tinha um campo que só sabia relatar adiamento, num sistema que tem seis formas
de recusar.

**Onde a prova para:** na sessão dela existem **dois** `profile_autoswitch`
(`adiado=[]` e `adiado=['suppression']`), e os `ignorado_*` que de fato
dispararam — três `profile_mode_revert_skipped motivo=catch_all_sem_opiniao`
às 02:40:22-24 — caíram em trocas **manuais**, que não emitem
`profile_autoswitch`. Então o mecanismo está provado no código e a classe de
evento está medida, mas **a linha específica dela que teria mudado não existe
nesta sessão**. Dito assim de propósito.

### Item 6 — sair do Modo Nativo não restaurava três seções

**Grau: MEDIDO no código; SEM PROVA de episódio na sessão dela.**

`_reapply_last_profile` (`lifecycle.py:940`) tem **um único chamador**:
`set_native_mode(False)` em `:893`. Ele monta um `ProfileManager` próprio — e
era **a única das cinco rotas** que o montava **sem** `mode_applier`,
`rumble_policy_applier` e `speaker_applier`:

| rota | onde | `rumble_policy` | `speaker` | `mode` |
|---|---|---|---|---|
| autoswitch | `subsystems/autoswitch.py:177,243` | sim | sim | sim |
| janela e CLI | `subsystems/ipc.py:44,98` | sim | sim | sim |
| PS + D-pad | `subsystems/hotkey.py:123` | sim | sim | sim |
| restore de boot | `connection.py:219` | sim | sim | **não, deliberado** |
| **saída do Modo Nativo** | **`lifecycle.py:963`** | **não** | **não** | **não** |

O `mode_applier` **ausente era uma decisão medida**, e ela continua de pé: a
`FEAT-PROFILE-MODE-01` o tirou porque, ao **sair** do nativo, `_native_mode` já
é `False`, e um `last_profile` com `mode.kind=native` seria **religado no mesmo
instante** — desfazendo o gesto que ela acabou de fazer.

**O que não se justifica é o preço colateral.** Barrar `native` custou também
`gamepad`, `desktop`, a reversão do modo, **a política de rumble e o volume do
alto-falante** — três seções que não têm nada a ver com o laço. É o padrão da
`ENTREGA-QUE-NÃO-LIGOU-01` visto pelo avesso: a decisão certa numa rota,
cobrando de quem não devia.

**Nota datada (05/08/2026):** a decisão da `FEAT-PROFILE-MODE-01` **não
caducou**. O que caducou foi a **implementação por remoção**. O comentário
antigo de `lifecycle.py` ("SEM `mode_applier` aqui de propósito") foi
substituído pela nota que explica os dois lados, e o veto continua executável —
agora dentro de `_mode_applier_ao_sair_do_nativo` (`:993`).

**Por que SEM PROVA:** não há **nenhuma** transição de Modo Nativo no journal
da sessão de 04-05/08 (`native_mode_changed` não aparece; todos os
`launch_env_materializado` trazem `native=False`). O defeito está provado por
leitura de código e por teste; **o episódio dela, não**.

---

## O alcance

| item | quem sofre | quando |
|---|---|---|
| 1 | **toda** troca manual dela (janela, CLI, PS + D-pad) | a cada tique de 2 Hz depois do gesto |
| 2 | mouse e teclado do controle no desktop | enquanto o perfil ativo for catch-all com `suppress: true` |
| 3 | a vibração, inclusive dentro do jogo | a cada ativação de perfil sem `rumble.policy` |
| 4 | a resposta da janela e do applet ao "Ativar" | sempre que houver trava manual ou modo jogo padrão em jogo |
| 5 | quem lê o journal — inclusive a próxima leva | toda troca automática |
| 6 | gatilhos entram, máscara/vibração/volume não | ao **desligar** o Modo Nativo |

Os itens 1 a 5 vivem no **caminho quente**: o autoswitch decide a **2 Hz**
(`autoswitch.py:41`). O item 6 é raro e caro — acontece uma vez por sessão de
jogo, e é exatamente o momento em que ela espera *"voltar ao normal"*.

## Por que a suíte não pegou

Nenhum dos seis é área descoberta. **Os seis têm testes vizinhos, e os seis
ficam verdes com o produto quebrado.** Cada linha abaixo foi conferida por
`grep` hoje.

| item | o que existe | por que não morde |
|---|---|---|
| 1 | `test_autoswitch.py` (25 casos), `test_autoswitch_manual_lock.py`, `test_subsystem_autoswitch.py` | **nenhum** ativa perfil por fora do `AutoSwitcher` e depois tica. Todos constroem um `AutoSwitcher` novo e conduzem tudo por ele — **a crença nunca pode divergir**. O único `manager.activate` desses arquivos (`test_autoswitch_manual_lock.py:119`) é um embrulho para espionar |
| 2 | `test_profile_suppression_lock.py` | o helper `_perfil()` (`:70-78`) é, textualmente, *"específico por default (R-02)"*, e `catch_all=True` aparece **uma única vez no arquivo** — na linha **276**, e **só no ramo que LIBERA**. O ramo que LIGA nunca viu um catch-all |
| 3 | `test_profile_rumble_policy.py` (23 casos) | `grep` por `catch_all`, `e_catch_all`, `janela_de_jogo` e `record_window_detect_read` devolve **zero**. Não havia o que testar: sem `profile=` na assinatura, a guarda era inexprimível |
| 4 | os testes de IPC leem `resposta["secoes"]` | leem as seções que o **daemon** preenche. As que o `apply` silencia nunca chegavam lá — e o teste conferia o dicionário que o produto montava, não o que ele **deveria** montar |
| 5 | os testes de log do autoswitch | conferem `adiado=`. O campo que faltava **não existia**, e um teste não reprova por ausência de campo que ninguém pediu |
| 6 | `test_native_mode.py` | **monkeypatcha `_reapply_last_profile` para não fazer nada** em três lugares (`:57`, `:74`, `:91`). O único assert sobre ele é `reapplied == ["x"]` (`:78`) — mede **"foi chamado"**, nunca **o que aplicou** |

O item 6 é o caso mais puro da *"mordida na metade errada da cadeia"* que a
`ENTREGA-QUE-NÃO-LIGOU-01` catalogou: o teste substitui pelo dublê exatamente o
trecho onde mora o defeito, e depois afirma sobre o dublê.

## Por que não é a TRAVA-QUE-SOLTA-TARDE-01

As duas nasceram na mesma noite e tocam `manual_override_categories`. São
distintas, e vale registrar porque é fácil confundi-las:

- a **TRAVA** é sobre a **ordem**: o `clear` rodava **depois** do `activate`,
  na rota **manual**, e a cura foi subir o clear. Ela faz o perfil **entrar**;
- **esta** é sobre o que acontece **quando a trava legitimamente vence**: o
  perfil não entra naquela categoria, isso está certo, e **ninguém conta a
  ela** (item 4). E é sobre o **autoswitch**, que a TRAVA declarou correto —
  e era, **naquele eixo**.

**As duas se completam, e a ordem importa:** com a cura da TRAVA de pé, o
`ignorado_trava_manual` do item 4 passa a ser **raro na rota manual** (a trava
foi limpa antes) e frequente nas ativações do **autoswitch** e no **restore de
boot**. É a nota que a janela precisa ter ao interpretar `resposta["secoes"]`.

## A cura, item por item

### 1 — a crença passa a ser lida, não lembrada

`autoswitch.py:200` `_store_de_estado()` e `:215` `_perfil_corrente()`, chamados
na **primeira linha** de `_tick` (`:279`) e no topo de `_activate` (`:583`).

Três decisões, e cada uma tem motivo:

1. **zero I/O.** A primeira versão relia o disco por `manager.get()`, e o
   **CANÁRIO-FS-01 flagrou escrita de `.lock` no diretório de perfis REAL
   dela**. Trocada por leitura de `store.active_profile`, que é memória;
2. **na divergência, `_current_especifico` vira `True`** — palpite conservador.
   Um nome novo com a especificidade do perfil **antigo** seria uma terceira
   crença errada; `True` apenas torna mais **caro** sair do perfil rumo a um
   genérico (12 s em vez de 0,5 s), e depois de um gesto explícito dela **ficar
   tem custo zero**. O palpite é corrigido **de graça** no mesmo tique
   (`:331`), quando o candidato selecionado é o perfil corrente;
3. **`active_profile` vazio, ausente ou não-string não derruba a crença.** Sem
   evidência positiva, vale o comportamento histórico — dublês e stores parciais
   continuam funcionando.

**Colateral declarado na docstring, porque é real e é bom:** o autoswitch deixa
de "entrar" no perfil que o **boot** acabou de restaurar. Isso **respeita** o
`BUG-BOOT-RESTORE-FLIPS-EMULATION-01` — o restore de boot monta o manager com
`mouse_applier=None` e `mode_applier=None` de propósito, e a re-ativação pelo
autoswitch **reintroduzia por acidente exatamente o que aquela cura removeu**.

### 2 — a supressão fica simétrica

`lifecycle.py:1621`: gate `catch_all_sem_opiniao` no ramo que **LIGA**, via
`_perfil_e_catch_all` (`:1784`).

O predicado é **novo e de evidência positiva** — irmão de `_perfil_tem_opiniao`,
e a diferença entre os dois **é a resposta na dúvida**, que é por isso que são
dois e não uma negação:

- ao **reverter** (guardas antigas, todos os chamadores já passam `profile=`), a
  dúvida vale "sem opinião": não reverter é o fail-safe;
- ao **ligar** (guarda nova), a dúvida **não bloqueia**: perfil ausente é o
  chamador direto (CLI, dublê) e `e_catch_all` ausente é objeto parcial. Uma
  guarda nova não pode transformar silêncio em recusa para quem nunca teve
  guarda nenhuma.

Para um `Profile` de verdade os dois coincidem — e em produção o perfil
**sempre** chega, porque `apply_emulation` passa `profile=` a cada ativação.

**O que NÃO foi tocado:** o gate R-02 no ramo de **LIBERAR**. O buraco era o
outro ramo.

### 3 — a política de rumble ganha as guardas dos irmãos

Assinatura (`lifecycle.py:2398`) ganha `profile=` por keyword; o callsite
(`manager.py:582`) passa. As duas guardas entram em `:2464-2493`.

**Ficam dentro do `if self._rumble_policy_from_profile:` de propósito:** sem
política de perfil de pé não há reversão a barrar, e devolver `ignorado_*` para
um no-op encheria o relatório da janela de recusas onde nada seria feito de
todo jeito.

**Ordem preservada:** o lock de gesto manual de 30 s continua sendo avaliado
**antes** das guardas novas — tem teste só para isso.

### 4 — o relatório passa a carregar as duas metades

- **(a)** `manager.py:238` — o `relatorio` desce de `activate` para `apply`;
  `:370` grava `IGNORADO_TRAVA_MANUAL` para as categorias travadas.
  `_CATEGORIAS_SILENCIADAS_NO_APPLY = frozenset({"trigger", "led"})` (`:78`) é
  **só o que este método de fato silencia** — `audio` é reportado por
  `apply_speaker`, `rumble` fora da ativação, e **reportá-los aqui seria
  inventar um silêncio que este código não produziu**;
- **(b)** `autoswitch.py:474/485` guardam o estado devolvido pelo par;
  `:680-681` o injeta como seção própria, `modo_jogo_padrao`.

O literal `"ignorado_trava_manual"`, que já existia solto em `apply_speaker`,
virou a constante `IGNORADO_TRAVA_MANUAL` (`manager.py:70`) — escrita no
`manager` e não no `lifecycle` porque **quem a produz é o manager**, e importar
o lifecycle no topo deste módulo fecharia um ciclo.

### 5 — o log diz a verdade inteira

`autoswitch.py:702`: campo novo `secoes=["secao=estado", ...]`, **ordenado**
para o diff entre dois tiques ser legível.

**O `adiado=` fica exatamente onde estava.** Não é redundância: é o campo que a
leitura de journal desta casa já procura, e trocá-lo quebraria toda análise
anterior. O novo campo acrescenta; não substitui.

### 6 — sair do Modo Nativo restaura as três seções

`lifecycle.py:986-988` injeta os três appliers, e o `mode_applier` vai
**embrulhado** em `_mode_applier_ao_sair_do_nativo` (`:993`), que barra **só**
`kind="native"` e devolve `IGNORADO_GESTO_DELA` — o estado certo do
vocabulário, porque a decisão já é dela e é mais específica que o que o perfil
pede.

**`getattr` nos três** pelo mesmo motivo das outras rotas: este método é chamado
desligado da instância por dublês da suíte, e um atributo ausente **não pode
derrubar a saída do Modo Nativo** — sem o applier, a seção volta a ser
ignorada, que é o comportamento histórico.

## A tabela item → cura → teste, com a mordida

`tests/unit/test_perfil_reescrito_na_partida_01.py` — **18 casos**, bancada
hermética (`ProfileManager` real + `StateStore` real + `FakeController`, com o
diretório de perfis isolado em `tmp_path`; nem hardware, nem D-Bus, nem a
`~/.config` dela).

**Mordida verificada por mim em 05/08/2026**, arrancando cada cura da árvore de
trabalho, rodando, e devolvendo com `git checkout --` a partir do índice (a
leva inteira está **staged e não commitada**; `git stash` a perderia). Ao fim,
a árvore foi conferida **byte a byte** contra a cópia de segurança e o arquivo
volta a **18 verdes**.

| item | cura (arquivo:linha) | teste que reprova sem ela | reprovas |
|---|---|---|---|
| **1** | `autoswitch.py:200,215` + chamadas em `:279` e `:583` | `test_ativacao_manual_seguida_de_tique_com_o_mesmo_candidato_nao_reativa` | **1** |
| **2** | `lifecycle.py:1621` (gate) + `:1784` (`_perfil_e_catch_all`) | `test_catch_all_com_suppress_true_nao_liga_a_supressao`; `test_o_disco_dela_dois_catch_all_nao_prendem_a_emulacao` | **2** |
| **3** | `lifecycle.py:2464-2493` + `profile=` em `:2402` e `manager.py:582` | `test_catch_all_nao_reverte_a_politica_de_rumble`; `test_janela_de_jogo_em_foco_nao_reverte_a_politica_de_rumble` | **2** |
| **4a** | `manager.py:238,370` (+ `:70`, `:78`) | `test_relatorio_registra_as_categorias_travadas_na_mao`; `test_log_do_autoswitch_reporta_estados_ignorados` | **2** |
| **4b** | `autoswitch.py:474,485,680` | `test_relatorio_do_autoswitch_carrega_o_modo_jogo_padrao` | **1** |
| **5** | `autoswitch.py:702` (`secoes=`) | `test_relatorio_do_autoswitch_carrega_o_modo_jogo_padrao`; `test_log_do_autoswitch_reporta_estados_ignorados` | **2** |
| **6** | `lifecycle.py:986-988` + `:993` (embrulho) | `test_sair_do_nativo_restaura_a_politica_de_rumble_do_perfil`; `test_sair_do_nativo_aplica_as_demais_secoes_de_modo` | **2** |

**São dez testes distintos que mordem**, dos dezoito. Dois deles mordem **duas**
curas cada — são testes de cadeia: `test_log_do_autoswitch_reporta_estados_ignorados`
precisa do relatório (4a) **e** do campo no log (5); e
`test_relatorio_do_autoswitch_carrega_o_modo_jogo_padrao` precisa do estado
guardado (4b) **e** do campo (5). **É a forma certa: eles medem o caminho
inteiro, não a metade.**

**Duas confirmações que a arrancada deu de graça**, e que valem mais que a
contagem:

- arrancado o item 1, a bancada emitiu
  `profile_autoswitch adiado=[] from_=None to=sackboy_nativo wm_class=steam_app_1599660`
  — **a assinatura do journal dela, reproduzida em bancada hermética**;
- arrancado o item 3, a bancada emitiu
  `profile_rumble_policy_reverted mult=0.7 policy=balanceado` — **a linha das
  02:24:42 e das 02:48:56, com os mesmos valores**.

### Honestidade sobre os oito casos que passam nos dois estados

Não é esquecimento — são **guardas da cura**, e estão marcados como tal na
docstring de cada um. Eles fixam o que a cura **não pode** ter quebrado:

- a troca automática continua acontecendo quando o perfil ativo é **outro**
  (`test_sincronizar_nao_congela_a_troca_para_outro_perfil`) — sem isto, a cura
  do item 1 teria matado o automatismo inteiro;
- quem **tem** opinião continua mandando nos dois sentidos, e o chamador sem
  perfil preserva o comportamento histórico;
- a reversão **legítima** no desktop continua ocorrendo, e o lock de gesto
  manual continua vencendo as guardas novas;
- o relatório **não inventa** seção ignorada;
- sair do Modo Nativo **continua sem religar** o nativo — a decisão da
  `FEAT-PROFILE-MODE-01`, que agora tem teste próprio pela primeira vez.

## O que fica ABERTO

**Bloqueantes de processo** (nenhum é código):

1. **Commitar.** Tudo está **só no índice**. Um `git stash` ou um `checkout`
   perde a leva inteira;
2. **Reiniciar o daemon dela.** PID 1670 é de 04/08 23:39:46, e o install é
   *editable* — **nenhuma cura desta sprint está valendo na máquina dela**. É
   **decisão dela**: havia sessão de jogo viva;
3. **O aceite em uso real.** A bancada prova o `relatorio`, o `OutputSpec` e os
   estados. Que o controle pare de mudar de cor sozinho no meio da partida,
   **só o uso dela fecha** (PROVA-DE-TELA-01: a palavra final é dela).

**Dívidas que esta sprint declara e não paga:**

- **a janela precisa saber ler `resposta["secoes"]` com a nota do parentesco**:
  `trigger`/`led` = `ignorado_trava_manual` aparecem sobretudo em ativações do
  **autoswitch** e no **restore de boot** (na rota manual a TRAVA limpa antes),
  e `modo_jogo_padrao` só existe no relatório do **autoswitch**;
- **a trava manual continua sem afordância na tela.** Ela não é exportada por
  `daemon.state_full`, e não há nada dizendo *"esta seção está travada"*. Esta
  sprint abre o canal; **ninguém ainda o mostra a ela**;
- **`manual_override_categories` continua global** (`set[str]`, sem eixo por
  controle) — é a `POSSE-POR-CONTROLE-01/E1`, e ela **colide** com o restore
  por categoria que a TRAVA introduziu (M-13 do estudo da leva);
- **o `clear_manual_trigger_active("audio")` continua não existindo** —
  `ÁUDIO-QUE-TRANCA-01/E1`, intocada aqui;
- **o `secoes=` ainda não tem consumidor de leitura de journal.** O campo nasce
  nesta sprint; nenhum script da casa o lê ainda;
- **o modo jogo padrão continua ligando e soltando por foco de janela dentro da
  partida** (D-24 do estudo). Esta sprint faz o eixo **contar** o que fez; não
  muda **o que ele faz**;
- **a origem do 191 continua indeterminada** (DIV-1). O instrumento que decide
  — o `profile_salvo` no journal e o `.historico/` — nasceu nesta madrugada e
  já capturou uma linha; **falta o próximo gesto dela**;
- **o item 6 não tem episódio medido.** A cura tem teste que morde, mas o
  defeito nunca foi visto acontecer com ela. Se alguém for reabrir, é aqui que
  falta medição.

**O que NÃO deve ser tocado, por decisão medida:**

1. **o gate R-02 no ramo de LIBERAR** de `apply_profile_suppression` — o buraco
   era o ramo de LIGAR, e foi esse que se corrigiu;
2. **o veto ao `mode.kind=native` ao sair do Modo Nativo** — a
   `FEAT-PROFILE-MODE-01` continua de pé; o que mudou foi **como** ele é
   expresso;
3. **o `adiado=` do `profile_autoswitch`** — é o campo que a leitura de journal
   já procura. O `secoes=` acrescenta, não substitui;
4. **o debounce assimétrico 0,5 s / 12 s** (`autoswitch.py:41-58`) — e note que
   a cura do item 1 **mexe no que arma o lado lento**: na divergência de crença
   ela assume `True` justamente para **não** encurtar a saída. Trocar esse
   palpite por `False` reabriria o flap que a UX-04 fechou;
5. **os arquivos de perfil dela, sem a mão dela** — inclusive o
   `sackboy_nativo.json`, inclusive "só para normalizar". Ele é o perfil
   **ATIVO**, catch-all, 191, `suppress: true`, e é o dado que arma quatro dos
   seis itens desta sprint. **Nenhuma linha desta leva o reescreve.**
