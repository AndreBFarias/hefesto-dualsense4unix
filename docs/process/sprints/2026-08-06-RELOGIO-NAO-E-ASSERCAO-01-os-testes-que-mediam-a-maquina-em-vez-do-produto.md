# RELOGIO-NAO-E-ASSERCAO-01 — os testes que mediam a máquina em vez do produto

- **Achado em:** 05 e 06/08/2026, por **auditoria da própria suíte** e por
  **verificação adversarial** — três dos quatro foram achados pelo instrumento
  reprovando a si mesmo, não por queixa dela. O quarto
  (**BURACO-DO-PORTAO-01**) saiu da varredura de *o que só funciona na máquina
  dela*, aberta pela pergunta que ela fez ao saber que o projeto é público:
  *"se um amigo meu usar o mesmo app, vai funcionar lá também?"*
- **Estado:** **CURA APLICADA** nos quatro, com testes que mordem, em
  `ae32c10` (RELOGIO-NAO-E-ASSERCAO-01), `c3829c7` (a aplicação de 05/08 do
  BUG-TEST-DBUS-NOTIFY-NONHERMETIC-01 e o desvio do BUG-MOUSE-TRIGGERS-01),
  `86c32ab` e `0b5a3a2` (BURACO-DO-PORTAO-01). Esta sprint é a
  **materialização atrasada** — o código e os testes existem desde 05 e 06/08;
  o documento que explica **por quê** é que faltava, e nenhum dos quatro
  códigos aparece em `docs/` fora dos comentários do próprio código.
- **Gravidade:** **ALTA** no BURACO-DO-PORTAO-01 — é vazamento de privacidade
  num repositório público, com o portão **verde**. **MÉDIA** nos outros três:
  nenhum quebra o produto; os três estragam a capacidade de saber se o produto
  quebrou, que é o que a casa usa para decidir tudo.
- **Causa-raiz:** **MEDIDA** nos quatro, e reconferida no repositório ao
  escrever esta página.
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [CANARIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md)
    — mesma família, outro recurso: ali a suíte escrevia no `HOME` dela; aqui
    ela fala com o D-Bus da sessão dela;
  - [SUITE-QUE-SUJA-O-JORNAL-01](2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
    — a mesma família de novo, no journal do sistema;
  - [PERFIL-REESCRITO-NA-PARTIDA-01](2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md)
    — é a leva **cujo teste** carrega dois destes quatro códigos; ela conta os
    seis defeitos de produto, esta conta os defeitos do instrumento que os mede;
  - [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
    — a janela de 2600 caracteres de lá é irmã do defeito 4 daqui: asserção que
    passa **por não enxergar**;
  - [CLEAN-ROOM.md](../CLEAN-ROOM.md) — normativa que já nomeia, por escrito, o
    `filter-repo` como a ferramenta do **endereço de hardware de uma pessoa**.
    O defeito 4 é exatamente esse caso, e a normativa é anterior a ele.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O que os quatro têm em comum

A armadilha número 1 desta casa diz que **medir contra a biblioteca errada
produz alarme convincente e falso**. Os quatro defeitos abaixo são a mesma
armadilha com outro sujeito: o instrumento não estava medindo o produto, estava
medindo **a bancada**.

Em quatro formas distintas, e vale nomeá-las porque cada uma engana de um jeito:

1. o teste mediu **o relógio da máquina** e chamou aquilo de invariante;
2. o teste mediu **a sessão gráfica dela**, porque abria o D-Bus de verdade;
3. o teste queria medir uma coisa que **o próprio produto escondia**, e teve de
   cegar um gate para enxergar;
4. o portão mediu **a grafia que a casa escreve** em vez da grafia que o
   **produto gera** — e por isso passou verde sobre um vazamento.

O dano dos três primeiros não é o defeito: é a suíte deixar de ser autoridade.
O dano do quarto é o vazamento em si.

### Sobre as datas, para não repetir a conta

**Grau: MEDIDO** (`git log -S`, conferido em 06/08). Dois destes códigos são
mais velhos do que a leva que os trouxe à tona:

| código | nasce em | volta em |
|---|---|---|
| BUG-MOUSE-TRIGGERS-01 | 21/04/2026, issue #69 | 05/08, no teste do relatório |
| BUG-TEST-DBUS-NOTIFY-NONHERMETIC-01 | 07/07/2026 | 05/08, em `c3829c7` |
| RELOGIO-NAO-E-ASSERCAO-01 | 06/08/2026, `ae32c10` | — |
| BURACO-DO-PORTAO-01 | 06/08/2026, `86c32ab` | fecha só em `0b5a3a2` |

Os dois primeiros são **reincidências**: a cura existia, num arquivo, e não
tinha virado regra da casa. É o que esta página passa a impedir.

---

## Defeito 1 — o relógio de parede era a asserção

**Gravidade: MÉDIA. Grau: MEDIDO.**

`tests/unit/test_keyboard_wire_up.py`, no teste que prova a invariante A-09
(*um snapshot de botões por tique, reaproveitado por teclado, mouse e hotkey*).
A versão anterior era literalmente isto:

```python
await asyncio.sleep(0.06)
...
assert ticks >= n_ticks          # n_ticks = 8
```

A 200 Hz, 60 ms preveem **12 tiques** — folga de quatro. Medido em 06/08: com a
suíte inteira rodando e a máquina sob carga, o laço perde a corrida e o teste
reprova; sozinho, e com a máquina quieta, passa. **Duas de quatro execuções
completas reprovaram**, e a mesma suíte no commit anterior passou.

O efeito é o pior possível para quem depende da suíte: o teste **acusa de
regressão quem só deixou a máquina mais ocupada**. Quem recebe esse vermelho vai
procurar defeito no código que acabou de escrever, e não há defeito nenhum.

### A cura: separar a invariante do hardware

A invariante que o teste existe para provar é `dispatch` **uma vez por tique**.
Quantos tiques cabem em 60 ms **não é asserção, é hardware**. A cura espera os
tiques acontecerem, com prazo generoso, em vez de apostar que cabem no relógio
de parede:

```python
prazo = time.monotonic() + 5.0
while daemon.store.counter("poll.tick") < n_ticks and time.monotonic() < prazo:
    await asyncio.sleep(0.005)
```

E o `assert ticks >= n_ticks` sobreviveu — mudou de significado. Agora ele só
dispara quando o laço deu menos de oito tiques **em cinco segundos**, que não é
lentidão de máquina ocupada: é o laço parado. A mensagem do teste diz isso com
todas as letras, para quem vier depois não repetir a investigação.

**Mordida:** a asserção que morde continua sendo `len(dispatch_calls) == ticks`
— com o dispatch pulando um tique, reprova. **Grau: MEDIDO** em 06/08 conforme
`ae32c10`, com a suíte verde e oito núcleos ocupados de propósito.

---

## Defeito 2 — o teste falava com o D-Bus da sessão dela

**Gravidade: MÉDIA (ALTA no incômodo). Grau: MEDIDO.**

`Daemon.set_emulation_suppressed`, em
`src/hefesto_dualsense4unix/daemon/lifecycle.py`, termina assim, sem condição
nenhuma:

```python
logger.info("emulation_suppressed_changed", suppressed=new_state)
notify_emulation_suppressed(new_state)
```

E isso é **decisão de produto, não descuido**: o docstring de
`notify_emulation_suppressed`, em
`src/hefesto_dualsense4unix/integrations/desktop_notifications.py`, diz que este
é feedback de uma ação **deliberada** dela (o toque longo do PS) e por isso
notifica **sempre**, à revelia do opt-in de notificações. Sem aviso visível, ela
não saberia se o gesto pegou.

O preço apareceu na bancada: cada teste que tocava a supressão abria uma conexão
**real** com o D-Bus de sessão e jogava um popup *"Modo jogo ligado/desligado"*
na tela dela, no COSMIC, no meio da suíte — e podia travar **até 2 s por
chamada** se o notificador estivesse lento.

### A cura: um dublê silencioso, e por que ele funciona

Uma fixture `autouse` por arquivo, em
`tests/unit/test_profile_suppression_lock.py` e em
`tests/unit/test_perfil_reescrito_na_partida_01.py`, que troca
`notify_emulation_suppressed` por uma função muda.

O detalhe que faz o dublê pegar, e que vale registrar porque a forma óbvia
**não** funcionaria: o `import` de `notify_emulation_suppressed` mora **dentro**
de `set_emulation_suppressed`, não no topo do módulo. Por isso o alvo do
`monkeypatch` é o atributo no módulo de notificações, resolvido na hora da
chamada. Trocar um nome de módulo em `lifecycle` não teria efeito — o nome nem
existe lá.

**Mordida:** este é dos poucos casos em que a mordida é do lado de fora — o
sintoma era a **tela dela**. **Grau: MEDIDO** pelo docstring do próprio teste,
que descreve o popup e os 2 s; **SEM PROVA** de que a suíte de hoje ainda os
produziria sem o dublê, porque a prova custaria disparar popups na tela dela de
novo, e ninguém vai fazer isso para confirmar o que já está escrito.

---

## Defeito 3 — o produto escondia o que o teste queria medir

**Gravidade: MÉDIA. Grau: MEDIDO.**

Este é o mais sutil dos quatro, e o mais fácil de escrever errado sem perceber.

O **BUG-MOUSE-TRIGGERS-01** é uma trava legítima e antiga do produto
(`src/hefesto_dualsense4unix/profiles/autoswitch.py`, dentro de `_activate`):
com um ajuste manual dela em vigor — gatilho, LED ou vibração —, a troca
automática de perfil **suspende**, senão ligar a aba Mouse (que move o cursor e
muda o foco de janela) reaplicaria o perfil por cima do que ela acabou de
ajustar. Quem arma a trava é
`src/hefesto_dualsense4unix/daemon/ipc_handlers.py`, no `trigger.set`; quem a
solta é `trigger.reset` ou um `profile.switch` explícito.

O item 5 da PERFIL-REESCRITO-NA-PARTIDA-01 precisava medir outra coisa: que o
log `profile_autoswitch` **para de esconder** os estados `ignorado_*` — entre
eles o `ignorado_trava_manual`. Ou seja, o teste precisa de uma ativação **que
aconteça** com a trava armada. Só que a trava, exatamente por existir, faz a
ativação **não acontecer**.

O produto e o instrumento disputando a mesma chave. A saída está no arquivo, em
três linhas:

```python
store.clear_manual_trigger_active()
manager.store.mark_manual_trigger_active("trigger")
sw.store = None
```

Lido devagar: `store` e `manager.store` são **o mesmo objeto** — a bancada do
arquivo devolve o `StateStore` que ela mesma injetou no `ProfileManager`. A
trava continua armada. O que muda é o `sw.store = None`: o gate do
BUG-MOUSE-TRIGGERS-01 consulta `self.store` **direto**, então cegar essa
referência desliga o gate, enquanto o `ProfileManager` — que ainda enxerga a
mesma trava — produz o relatório que o teste quer ler.

Funciona por causa de uma assimetria real no código, e é ela que merece ficar
registrada: a **crença** do autoswitch é sincronizada por `_store_de_estado()`,
que cai no `manager.store` quando `self.store` é `None`; o **gate da trava**,
não — ele lê `self.store` e pronto. Uma assimetria que o produto tem por bons
motivos vira, na bancada, a única alavanca disponível.

**Grau: MEDIDO** — está escrito no arquivo, com o comentário que nomeia o
código, e os 18 testes daquele arquivo passam hoje.

**O que isto custa, e é o motivo de estar nesta sprint:** um teste que precisa
desligar um gate do produto para enxergar mede **um produto que não existe**. O
custo aqui é pequeno e consciente (o relatório é gerado no `ProfileManager`, que
segue intacto), mas a forma é perigosa, e ela já se espalhou — ver a seção
aberta no fim.

---

## Defeito 4 — o portão exigia separador, e o produto não usa separador

**Gravidade: ALTA. Grau: MEDIDO.**

O portão de anonimato de hardware — `tests/unit/test_docs_mac_anonimato.py` — é
o único que cobre endereço de rádio em `docs/process/`, porque o
`scripts/check_anonymity.sh` **é cego a MAC** (só caça menções a provedores de
IA) e ainda exclui `docs/process/**` por caminho.

O regex dele casava assim, e só assim:

```
OUI · separador · dois hex · separador · dois hex · separador · dois hex
```

Ou seja: exigia **separador** entre os octetos. E a forma **contígua** — doze
hex colados, sem separador nenhum — passava batida.

O problema é que a forma contígua é justamente **a que o produto gera**. É
assim que o endereço sai do `controllers.json` (chave `addr`), do journal
(campo `uniq=`) e da saída do `bluetoothctl`. Toda página desta casa que cola
uma linha de journal ou um trecho de configuração cola **a grafia que o portão
não via**.

### A contagem, conferida no repositório

Reconferido ao escrever esta página, rodando o regex do portão de hoje contra as
árvores versionadas de então. **Grau: MEDIDO.**

| medida | valor |
|---|---|
| ocorrências da forma contígua na árvore de `86c32ab^` | **24, em 7 arquivos** |
| dessas, com o sufixo **exposto** (fora da máscara da casa) | **16, em 6 arquivos** |
| sufixos na forma **elidida**, num sétimo arquivo | **2** |
| total de endereços publicados de fato | **18, em 7 arquivos** |

As duas contagens de "7 arquivos" são coincidência, e vale dizer para ninguém
somar errado: o conjunto de 24 inclui **oito ocorrências já mascaradas**, todas
num arquivo só, e não inclui a página de usuária onde estava a forma elidida.

A divergência com a mensagem de `86c32ab`, que fala em "24 ocorrências", é
só de método: lá se contou **toda** a forma contígua, mascarada ou não. O número
de vazamentos reais é 18.

E um deles estava em `docs/usage/troubleshooting-8bitdo.md` — **página de
usuária, publicada**.

### As três grafias, e por que a terceira é a pior

1. **com separador** — a grafia que os documentos desta casa escrevem à mão. Era
   a única que o portão via.
2. **contígua** — a grafia que o **produto** gera. Passava.
3. **elidida** — o OUI omitido, só o sufixo escrito. Passava, e é a mais
   traiçoeira das três: o que identifica o aparelho é justamente o **sufixo**, e
   o OUI costuma estar **na mesma frase**, porque é público e a explicação
   precisa dele. Cada pedaço passava pelo portão por estarem em símbolos
   separados; remontar os dois endereços completos era juntar as pontas de uma
   linha só.

Faltava ainda um **OUI na lista**: o do segundo DualSense da bancada. A ausência
estava registrada como buraco desde 29/07, e o endereço daquele controle
circulou o tempo todo. Hoje ele está na tabela, com nota datada no próprio
arquivo.

### A cura, e a mordida

As três grafias passam a reprovar, com a mesma máscara da casa — octetos 4 e 5
zerados — nas três. O portão ganhou um segundo teste, dedicado à forma elidida,
que se exclui do próprio varrimento pelo nome do arquivo (senão ele se acusaria,
porque precisa citar a forma no texto para explicá-la).

**Mordida:** verificada nas duas metades em 06/08 conforme `86c32ab` —
devolver um endereço contíguo e um sufixo elidido, ver reprovar, devolver. O
docstring do segundo teste deixa a receita escrita para quem for repetir.
**Grau: MEDIDO.**

---

## O achado desta materialização: o portão mede a árvore, e o vazamento mora no commit

**Grau: MEDIDO**, ao escrever esta página. É novo, e é o mais desconfortável.

O portão monta a lista de arquivos com `git ls-files` e lê o **conteúdo em
disco**. Ou seja, ele mede a **árvore de trabalho** — que é a regra desta casa
("a árvore de trabalho é o que roda") e é por isso que os portões são cegos a
arquivo novo antes do `git add`.

Só que o que vai para a comunidade não é a árvore de trabalho: é o **histórico**.
E rodando o regex do portão de hoje contra cada árvore versionada da noite de
06/08, o resultado é este:

| commit | endereços expostos na forma contígua |
|---|---|
| `86c32ab` (a cura do BURACO-DO-PORTAO-01) | 4, em 2 arquivos |
| `53f6d8b` | 4, em 2 arquivos |
| `febe3e0` | 4, em 2 arquivos |
| `0b5a3a2` | 0 |

Os dois arquivos que ficaram para trás foram mascarados só no último commit da
noite, que é o que diz, ele mesmo, que *"os quatro commits de hoje são recortes
de um mesmo dia de trabalho, e alguns arquivos foram tocados por mais de um"*.

Nada disso é contradição com os portões: `53f6d8b` e `febe3e0` declaram **7249
verdes**, e é plausível que estivessem verdes — a árvore de trabalho já tinha os
dois arquivos limpos quando os portões rodaram, e a limpeza só foi commitada no
recorte seguinte. **Grau: SUSPEITA COM MECANISMO** para essa explicação; o que é
**MEDIDO** é que três commits publicados carregam os quatro endereços.

A conclusão operacional, e ela é a razão desta seção existir: **um portão que
mede a árvore de trabalho não protege o histórico**. Para vazamento de dado
pessoal, o que importa é o commit.

---

## Nota datada — o que caducou, e o que virou preço aceito

**O `store` do `AutoSwitcher` é opcional por causa da bancada.** Está escrito no
código, sem disfarce: *"opcional para permitir testes legados que instanciam
AutoSwitcher sem store; em produção, o Daemon injeta o store compartilhado"*.

Conferido em 06/08 (**MEDIDO**): as **duas** rotas de subida em
`src/hefesto_dualsense4unix/daemon/subsystems/autoswitch.py` injetam o store, e
são as únicas em `src/`. Então a invariante de produção está de pé hoje.

Não se apaga decisão medida, e esta continua valendo — mas ela tem preço, e o
preço agora está escrito: um campo cujo `None` **só existe para a suíte** é um
campo que a suíte vai usar. Foi exatamente o que aconteceu no defeito 3.

---

## O que fica ABERTO

- **O histórico continua com os endereços.** A `CLEAN-ROOM.md` já nomeia o
  `filter-repo` como a ferramenta certa para *"vazamento de dado sensível —
  senha, chave privada, endereço de hardware de uma pessoa"*, e diz que ali a
  exposição **é** o dano. Já houve uma purga de MAC neste repositório, em 20/07,
  e os endereços **voltaram** depois dela. **Grau: MEDIDO** (que voltaram, e que
  três commits publicados os carregam); **SEM PROVA** de que uma nova purga
  valha o custo — há 438 `replace refs` da purga anterior ainda ativos, e essa
  conta ninguém refez.
- **Nenhum portão varre o histórico.** O de MAC lê a árvore de trabalho; é a
  regra da casa e ela é correta para tudo, menos para isto. **Grau: MEDIDO** (o
  portão usa `git ls-files` e lê o disco). O que seria um portão de histórico
  viável — varrer só os commits novos de cada leva, por exemplo — **SEM PROVA**:
  ninguém desenhou.
- **A lista de OUIs é escrita à mão.** Aparelho novo na bancada entra sem
  cobertura, silenciosamente, e é exatamente o que aconteceu com o segundo
  DualSense — buraco aberto desde 29/07, fechado só em 06/08. **Grau: SUSPEITA
  COM MECANISMO**: o mecanismo é a lista literal, e o caso já ocorreu uma vez.
- **A mesma forma do defeito 1 continua em pelo menos 23 lugares da suíte**, em
  12 arquivos: `await asyncio.sleep(<constante>)` com asserção sobre contador ou
  tamanho nas oito linhas seguintes — a varredura é por forma, então o piso é
  confiável e o teto não. Dois deles são a forma idêntica à curada —
  `tests/unit/test_poll_loop_evdev_cache.py` (0,15 s para exigir 10 tiques a
  200 Hz) e `tests/unit/test_daemon_lifecycle.py` (0,2 s para exigir 5). **Grau:
  MEDIDO** que a forma existe e onde; **SUSPEITA COM MECANISMO** de que
  reprovem sob carga — as folgas ali são bem maiores (30 tiques previstos para
  10 exigidos) do que a do teste que quebrou (12 para 8), e nenhum deles foi
  visto vermelho.
- **O prazo de 5 s do defeito 1 é ele próprio um número de bancada.** Numa
  máquina muito mais lenta ou num CI compartilhado, o teste volta a reprovar.
  **Grau: SEM PROVA** — mas com uma diferença que importa: agora ele reprova
  **dizendo** que o laço está parado, em vez de acusar regressão.
- **O dublê do D-Bus é por arquivo, não da casa.** `tests/conftest.py` não tem
  guarda contra notificação. Recontado em 06/08, e desta vez **com o critério
  escrito**, para a conta poder ser refeita: `grep -rlE 'emulation.*suppress'
  tests/` devolve **12 arquivos**, e só **4** deles trocam o
  `notify_emulation_suppressed` por uma função muda — **8 ficam sem**.
  **Grau: MEDIDO** a contagem, por esse critério; **SUSPEITA COM MECANISMO** de
  que algum desses 8 alcance de fato o `notify_emulation_suppressed` — o
  caminho existe e está lido, mas nenhum foi executado com a tela dela à vista
  para confirmar. **Nota datada — 06/08:** a primeira escrita desta página dizia
  *"13 arquivos, 9 sem o dublê"*, sem dizer como contou, e nenhum critério
  reproduz esses dois números. O número não foi apagado: foi **substituído por
  um que se refaz**.
- **Onze construções do `AutoSwitcher` na suíte não passam `store`** — e nessas,
  o gate do BUG-MOUSE-TRIGGERS-01 está **desligado**, pela mesma alavanca que o
  defeito 3 usou de propósito. **Grau: MEDIDO** a contagem. Quantas delas
  *deveriam* estar medindo com a trava viva é **SEM PROVA**: exigiria ler os
  onze, um a um, e decidir caso a caso.
- **Não existe portão que proíba a forma "relógio como asserção".** A lição
  desta sprint mora hoje num comentário de um teste. **Grau: SEM PROVA** de que
  um portão desses seja construível sem falso positivo em massa — o padrão
  legítimo (dormir para provar que algo **não** acontece) é sintaticamente
  idêntico ao ilegítimo.
