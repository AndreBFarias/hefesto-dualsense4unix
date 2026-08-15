# A lightbar travada por rádio — o que já caiu, e o que nunca foi tentado

- **Escrito em:** 15/08/2026, para que uma frente nova **não repita caminho já
  percorrido**. Duas outras frentes estão medindo o defeito ao vivo neste
  momento — um DualSense branco com a barra travada e um vermelho são ao lado
- **Estado:** **ESTUDO. Nenhuma linha de código tocada, nenhum controle tocado,
  nenhum serviço reiniciado, nenhum controle desligado.** Leitura de
  repositório: `git log`, sprints, canônicas, o mapa de canais, o caderno de
  ensaios, o caderno de eliminação (que só lê o CSV) e os comentários do `src/`
- **O que este documento é:** o **histórico completo desta frente** — cada
  hipótese já proposta, quem a derrubou, com que evidência, e se ela foi
  **refutada** ou apenas ficou **sem prova**. E, no fim, a parte que vale mais:
  **o que nunca foi tentado**
- **O que este documento NÃO é:** não defende hipótese nova, não propõe cura, e
  não fecha nada. Ele existe para que a próxima madrugada seja gasta num caminho
  **novo**

> **Grau de cada afirmação**, na convenção da casa: **MEDIDO** = há ensaio,
> linha de journal, arquivo lido ou olho dela; **RECONSTRUÍDO** = derivado de
> `git log` e das datas, sem documento que o afirme diretamente; **SEM PROVA** =
> está dito e ninguém verificou.
>
> **Endereços de rádio:** nenhum aparece aqui. Onde uma fonte os traz, ficam na
> fonte, já mascarados (octetos 4 e 5 zerados).

---

## 0. Quatro avisos, antes de qualquer tabela

**Aviso 1 — a sprint com o nome mais promissor não é desta frente.** A
[A LUZ QUE CUROU-01](../sprints/2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
*("calar parou o bombardeio, e voltar tem preço")* trata do **Pro Controller e
do 8BitDo**, do limitador `joycon_enforce_subcmd_rate` do `hid-nintendo`, e de
LEDs de **jogador** escritos por `sysfs`. O DualSense não passa por aquele
driver e não tem aquele limitador — a própria sprint diz, com todas as letras,
que o `hid-playstation` *"não tem limitador de taxa nenhum"* e que os dois
DualSense *"não passam pelo `hid-nintendo` e não recebem subcomando nenhum"*.
**Quem for atrás daquele documento procurando a lightbar do DualSense gasta 900
linhas e volta com nada.** GRAU: MEDIDO (a sprint, lida inteira).

**Aviso 2 — a
[RÁDIO BOMBARDEADO-01](../sprints/2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)
também não é.** Ela mede corrupção L2CAP: um problema de **enlace**, não da
máquina de estados da barra. Ela importa como **ambiente** em que as medições de
lightbar aconteceram — e nisso ela importa muito (§5, item 7) —, nunca como
causa proposta.

**Aviso 3 — a Steam saiu da mesa.** O caderno de eliminação **ainda** devolve
`E-A-CAUSA` para *"a Steam ESCREVER no fio durante a probe"* na linha
`luz.lightbar.cor@dualsense [radio]`. Ela derrubou isso duas vezes em 15/08:
**"já superamos a steam"**. O defeito está vivo agora, e a conclusão de 12/08 é
a **última** de uma fila de conclusões que caíram. Aqui a Steam é **mais um item
da tabela do §2**, não o estado da arte.

**Aviso 4 — o enunciado do defeito é mais velho que os fatos.** A linha
`luz.lightbar.cor` do mapa (`docs/data/mapa-controles.csv:153`) carrega hoje
**duas descrições que se contradizem na mesma célula**:

| o que a célula diz | origem | situação |
|---|---|---|
| *"É a feature mais quebrada do aparelho: a barra apaga na adoção e passa a IGNORAR as escritas do kernel (330 mil escritas ignoradas ao vivo), persistindo até o POWER-OFF FÍSICO"* | herdada de 18/07 | **a moldura de julho** — e três dos seus termos já caíram |
| *"A barra obedece nos DOIS transportes — medido em 12/08/2026 com cor arbitrária e daemon parado. O que faz uma conexão de rádio nascer travada continua SEM CAUSA ISOLADA"* | 12/08 | **o veredito atual da própria linha** |

Os três termos que caíram:

- *"apaga na adoção"* — a adoção foi **testada suspeito a suspeito em 03/08 e
  inocentada**: abrir o `hidraw`, o feature report `0x05` de calibração, e o
  `init()` completo com o `report_thread` escrevendo por 2 s. Os quatro,
  inocentes, com a barra confirmada pelo olho dela entre um teste e outro;
- *"persistindo até o POWER-OFF FÍSICO"* — **falso desde 09/08**: um restart do
  daemon repinta, e o latch não é permanente (medido por ela);
- *"330 mil escritas ignoradas ao vivo"* — número de 17/07, **nunca recontado**.
  A afirmação-irmã (*"cinco dias e vinte adoções"*) provou-se, em 11/08, ser
  **docstring registrada como medição**.

**Isto é dívida de documento, e ela ainda está cobrando juros hoje** — ver §6.

---

## 1. A forma do defeito, e por que ela engana

Três propriedades desta frente explicam por que ela caiu tantas vezes, e as três
estão medidas:

1. **O instrumento mede o pedido, não o aceso.** O `multi_intensity` do `sysfs`
   é a memória do último valor escrito **pela classe LED**; escrita por `hidraw`
   não o atualiza. A aba Lightbar mostra o **rascunho do perfil**, não o que
   está no plástico — medido em 27/07, com a aba Status dizendo `#0000ff` e a
   aba Lightbar mostrando laranja **no mesmo instante**. **Toda observação de
   "a barra está apagada" feita por software herda esse defeito.**
2. **O defeito é intermitente, e a intermitência tem mecanismo conhecido.** A
   queixa dela — *"sempre arrumamos mas sempre volta"* — foi explicada em 03/08:
   o caminho que mandava o report saía de `new_handles`, então às vezes o report
   saía e às vezes não. **O produto acertava ou errava um sorteio a cada
   conexão** — e um sorteio produz correlação convincente em amostra pequena.
3. **Há uma janela de ~3,4 s pós-conexão em que o resultado é outro.** Isso é
   medido, e é a razão pela qual **quatro suspeitos foram inocentados por engano
   por terem sido testados FORA da janela**. É a armadilha mais cara desta
   frente.

---

## 2. AS HIPÓTESES JÁ DERRUBADAS

Ordem cronológica de **quando foram propostas**. A última coluna é a que mais
importa: **refutada** (há medição que a contradiz) e **sem prova** (nunca foi
medida, ou ficou inconclusiva) não são a mesma coisa, e tratá-las igual é como
se perde tempo duas vezes.

### 2.1 As causas-raiz — as que viraram código

| # | a hipótese, em uma frase | proposta | quem a derrubou, e com que evidência | veredito |
|---|---|---|---|---|
| **C1** | A cor não obedece por BT por **contenção de dois escritores** (o kernel `hid_playstation` contra a pydualsense pelo `hidraw`); a cura é usar a rota `sysfs` | 28/06, `a35dd85` (`FEAT-DSX-LIGHTBAR-SYSFS-01`) | Ninguém a refutou. Ela ficou **insuficiente**: em 18/07 o próprio nascimento de `_suppress_leds` como `False` virou o culpado seguinte | **de pé e insuficiente** |
| **C2** | A **ADOÇÃO** (abertura do `hidraw` + feature reads do `init`) derruba o *claim* da lightbar no firmware; a cura é o `0x08` (`RELEASE_LEDS`) que o SDL manda e o kernel nunca manda | 18/07, `bbfe74d` | **Refutada em 03/08**, suspeito a suspeito: abrir o `hidraw`, o feature `0x05`, e o `init()` completo com o `report_thread` escrevendo — **os quatro inocentes**, com a barra obedecendo a **seis cores seguidas** por Bluetooth entre os testes | **REFUTADA** |
| **C3** | O `0x08` só cobre handles **novos**; um **wake/resume** que não reabre o handle também derruba o claim, e reenviar o `0x08` na assinatura do wake cura (`RESET-02`, `should_reclaim_on_wake`) | 20/07 | **Refutada em 03/08 por construção:** o gate exige `current_sysfs_rgb == KERNEL_DEFAULT_BLUE`, e o `multi_intensity` mostra o valor **pedido**, nunca o aceso — provado quando o nó nasceu `0 0 0` com a barra acesa em azul. O código registra a frase: *"casou nunca"* | **REFUTADA** (nunca disparou) |
| **C4** | Desde o `BTREPORT-02` (18/07) o `0x08` saía **fora de sequência** (`seq=0` fixo) e o firmware o descartava — por isso o claim nunca voltava (`RESET-03`) | 22/07, `2f9665f` | Não foi derrubada: é fato de protocolo, e continua correto. Ficou **sem alvo** quando o `0x08` inteiro saiu do produto em 04/08 | **de pé, sem alvo** |
| **C5** | O **keepalive** do produto saía com `valid_flag2=0x03`, reengatando o `LIGHTBAR_SETUP_CONTROL_ENABLE` **487 vezes a 2 Hz**; a máquina de setup fica engatada e o firmware aceita a cor no registrador mas não a exibe (`LIGHTBAR-BT-KEEPALIVE-01`) | 22/07, `760855b` | **Ninguém a derrubou — e ela também não curou.** A cura entrou em 22/07 e o sintoma seguiu vivo em 02/08, 03/08, 08/08, 11/08 e 12/08. É a **única** justificativa viva da supressão incondicional (§4) e **nunca foi remedida** | **de pé como mecanismo; NÃO curou** |
| **C6** | O gatilho é o **reinício do daemon**: o `0x08` solta o claim e ninguém do lado do host o retoma; a cura é `common[41] = LIGHT_OUT` para "tomar a barra de volta" (`LIGHTBAR-BT-CLAIM-01`) | 02/08 | **Refutada nos três pontos em 03/08:** (a) o evento 6 é reconexão com o daemon **vivo** e não travou, enquanto outra no mesmo minuto travou; (b) o `0x08` **fora** da janela (19:53:17) e a barra obedeceu; (c) a cura **apaga** — o driver desta máquina diz `lightbar_setup = DS_OUTPUT_LIGHTBAR_SETUP_LIGHT_OUT; /* Fade light out. */`, e testada ao vivo não teve efeito | **REFUTADA nos três** |
| **C7** | O `0x08` enviado **DENTRO da janela de ~3,4 s** pós-conexão trava a barra até o power-off (`LIGHTBAR-BT-CULPADO-01`) | 03/08 | **A correlação continua de pé: 7 de 7**, dois controles no mesmo rádio no mesmo minuto, com controle negativo (o `0x08` fora da janela não trava). **Mas como causa SUFICIENTE ela caiu em 11/08:** o `0x08` foi removido em 04/08 e, no ensaio `lightbar-bt-sem-0x08-hoje-2300` (11/08, olho dela, daemon **parado**, escrita direta), os dois do cabo acenderam e **os dois do rádio não** — *"só os cabo ficaram branco e o do bt não"* | **correlação MEDIDA; causa suficiente REFUTADA** |
| **C8** | A **instância de conexão** é a causa: derrubar o controle pelo BlueZ e acordá-lo pelo botão PS cura (*"reconectar cura"*) | 11-12/08 | **Ela me parou antes de virar registro** (§3): *"não é só instância de conexão, se escavar o projeto vai ver que isso é um falso positivo recorrente"*. E o `scripts/eliminacao.py` já recusava fechar: devolvia `CONFUSO`, porque o mesmo lado dava resultados diferentes. **O instrumento estava certo e eu ia escrever por cima dele** | **REFUTADA como causa; era proxy** |
| **C9** | O culpado é **quem está com o `hidraw` aberto no instante da probe** — e era a **Steam**, com `/dev/hidraw4..7` em leitura+escrita, medido por `readlink` em `/proc/*/fd` e confirmado no `fdinfo` | 12/08 | **Derrubada por ela em 15/08: "já superamos a steam"** — e pelo fato bruto de o defeito estar vivo agora. O próprio caderno de eliminação, que ainda a marca `E-A-CAUSA`, **está desatualizado nesta linha** | **REFUTADA pela observação dela** |
| **C10** | A rota `hidraw` suprimida por BT é a **causa-raiz compartilhada** de rumble, gatilho **e** luz | 11/08 | **Falsa, e derrubada em 12-13/08:** a supressão limpa **só** os bits de LED; rumble e gatilho **sempre** saíram por `hidraw` no rádio, e a bancada os viu funcionando lá. A hipótese vale para **lightbar** e **número de jogador**, e só | **REFUTADA (no escopo largo)** |

### 2.2 Os suspeitos laterais — eliminados um a um

Todos com ensaio, todos com o olho dela. Esta é a metade que dá lucro: ela diz
**o que se pode parar de fazer**.

| suspeito | quando | o que o derrubou | veredito |
|---|---|---|---|
| **perda de pacote no ar** | 02/08 | mais de 100 reescritas reais desde 14:40 — *"perda estocástica não erra cem de cem"* | **REFUTADO** |
| **fila do `uhid` cheia** | 02/08 | zero `Output queue is full` no `dmesg` inteiro | **REFUTADO** |
| **nó de `sysfs` faltando no BT** | 02/08 | `sem_no_sysfs` **vazio** em todas as coberturas do dia, com as duas barras apagadas | **REFUTADO no dia** (volta como corrida — §5.5) |
| **`_output_mute` / Modo Nativo** | 02/08 | o `0x08` e o priming saíram no mesmo milissegundo | **REFUTADO** |
| **o cache do `sysfs_leds` (`skip_cache`)** | 02/08 → 11/08 → 12/08 | a escrita **aconteceu**; e com o daemon **parado** o comportamento é idêntico (ensaio `lightbar-daemon-fora-radio`). É **agravante**, não causa — o que ele impede é a cura agir | **REFUTADO como causa** |
| **broker / vpad / co-op fazendo o firmware perder o dono** | 02/08 | a cor não passa por `hidraw` naquele caminho; e o primeiro a apagar foi o **único** controle da mesa | **REFUTADO** |
| **"dois controles por BT" ser a condição** | 02/08 | o primeiro apagou às 14:13, quando era o único no rádio | **REFUTADO** |
| **o rádio emudecer com o controle parado** (`BT-SURDO-01`) | 03/08 | três medições: ~300, ~326 e ~304 Hz contínuos com os controles parados na mesa | **REFUTADO** |
| **a revisão de hardware** | 12/08 | as três revisões (`0x0710`, `0x1111`, `0x0711`) estavam representadas na mesa, e o resultado não seguiu a revisão | **REFUTADO com prova** |
| **a escrita do LED de JOGADOR derrubar o claim** (hipótese dela) | 08-09/08 | isolada com o instrumento comutável ao vivo `suprimir_player_leds`, variável única: **eliminada** | **REFUTADO** |
| **a personalização por controle** (cor fixa por MAC, ordem por MAC) | 12/08 | esvaziado o `order` do `controllers.json` (9 MACs → 0) e o bloco `controllers` de quatro perfis: o defeito continuou | **REFUTADO** |
| **o firmware esquecer a cor entre conexões** | 12/08 | o controle voltou de uma desconexão completa exibindo **magenta** — a cor escrita por `hidraw` minutos antes, atravessando um `Disconnect` do BlueZ e uma reconexão inteira. *"azul player 4 cor magenta"* | **REFUTADO — e o corolário é grande** (§5.9) |
| **o `systemd-logind` retirando a permissão do nó** | 12/08 | errado: quem esconde o nó é o **broker de `hidraw` do próprio produto**, de propósito, 14.105 vezes em sete dias. A regra udev escrita para "vencer a disputa" não venceu e foi removida | **REFUTADO (o culpado era o produto)** |
| **a Steam APAGAR a barra em regime** | 12/08 | ensaio `steam-pinta-e-nao-apaga`: ela **repinta**, não apaga | **REFUTADO** |
| **a Steam escrever CONTINUAMENTE** | 12/08 | `btmon`: duas rajadas (`t+0`–`t+3 s`, `t+15`–`t+18 s`) e depois silêncio | **REFUTADO** |
| **o `sysfs` ser rota MORTA por rádio** | 12/08 | ensaio `cor-rota-sysfs-sem-steam-2237`: sem outro escritor, **as duas rotas obedecem**. O que derrubava o `sysfs` era a **disputa na probe**, não a rota | **REFUTADO** |

### 2.3 Os que nunca foram cruzados com o sintoma — **sem prova**, não refutados

Esta seção é a que costuma ser lida errado. Nenhum destes foi medido **com o
sintoma presente**. Eles não estão inocentados; estão **por olhar**.

| suspeito | onde foi proposto | por que continua sem prova |
|---|---|---|
| **sem nó de `sysfs`, a cor não tem caminho e a falha é silenciosa** | `BT-FURO-FINO-01`, defeito 2 | leitura de fonte, nunca cruzada com o sintoma; e a medição existente (`sem_no_sysfs` vazio em 02/08) o desqualifica **para aqueles eventos**, não em geral |
| **o `report_thread` fantasma do `init` que estoura o tempo**, escrevendo `0x31` com `_bt_seq` próprio por cima do handle legítimo | `BT-SURDO-01`, E2 (03/08) | o `py-spy dump` na máquina dela **nunca foi rodado**. **Curado hoje, 15/08 (`79ab98c`), sem que ninguém o cruzasse com a lightbar** — ver §5.8 |
| **o pacote de ÁUDIO aceito como input** pelo espelho de motion | `BT-FURO-FINO-01`, defeito 1 | inerte enquanto a ponte de mic nasce desligada; o experimento tem custo declarado e nunca foi rodado |
| **corrupção L2CAP / áudio isócrono degradando o rádio** | `RADIO-BOMBARDEADO-01` | a hipótese do clone DS4 foi **refutada** (janelas disjuntas); a da topologia USB ficou **contradita**; a do fluxo isócrono está **em pé e não medida** — os ensaios F2 e F3 nunca foram executados |
| **o `common[8]` escrito sem dono** (LED do botão de mic, forçado a zero em todo report) | `LED-SEM-DONO-01` (03/08) | ninguém contestou e ninguém mediu. Não é causa da barra — é **causa de erro de medição**: um escritor sem dono no mesmo report `0x31` que carrega a lightbar |
| **o laço de escrita roubando ar do enlace** | `O-LACO-DE-ESCRITA-01` (15/08) | hipótese de hoje, do defeito de **entrada**; o ensaio de quatro patamares espera autorização dela. Nunca cruzada com a lightbar |

---

## 3. AS QUATRO VEZES que "reconectar cura" caiu

**A primeira coisa a dizer é desconfortável: o repositório nunca as enumerou.**
A frase — *"'Reconectar cura' já foi concluído e derrubado **quatro vezes desde
17/07**"* — aparece em **quatro lugares**, e em nenhum deles há a lista:

| onde | fonte que ela cita |
|---|---|
| [`docs/protocol/pilha-steam-input-xpad-sdl.md:1099-1103`](../../protocol/pilha-steam-input-xpad-sdl.md) | nenhuma |
| `docs/process/2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md:589-591` | nenhuma |
| [`CANETA-NA-MÃO-01`](../sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md) `:322-323` e `:346` | **`ensaios.csv:38-39`** |
| `docs/usage/troubleshooting.md:859` | nenhuma |

**E a única fonte citada é circular:** as notas de `docs/data/ensaios.csv:38-39`
repetem a mesma frase em vez de sustentá-la. A contagem é **memória dela**
(alerta verbal de 12/08), e a casa já registrou que, quando a memória dela
contradiz o repositório, a hipótese de trabalho é que **o repositório está
incompleto** — mas a escavação que enumeraria as quatro **nunca foi feita**.

> **Cuidado com uma colisão de números:** existe um *outro* "quatro vezes" nesta
> mesma investigação — os **quatro acendimentos** da barra dentro dos cinco dias
> sem `0x08` (`ensaios.csv:28`, `:31-34`). **Não são as mesmas quatro**, e a
> tabela da `CANETA-NA-MÃO-01` põe as duas em linhas adjacentes.

Segue a **primeira enumeração**. GRAU: **RECONSTRUÍDO** (de `git log`, das datas
e das sprints); a contagem original é dela.

| vez | a conclusão, como foi escrita | quando | o que a derrubou |
|---|---|---|---|
| **1ª** | *"A adoção derruba o claim; mandar o `0x08` na conexão devolve a barra"* — a cura de 17-18/07, que é literalmente "reconectar (com o report certo) cura" | 18/07, `bbfe74d` | **22/07, `2f9665f`:** desde o `BTREPORT-02` todo `0x31` sai com sequência **por handle**, e o reset escrevia direto no `device` com `seq=0`; o firmware descartava e o claim nunca voltava. Registro literal: *"a cura de 17/07 funcionava porque na época TODOS os reports saíam com seq 0"* |
| **2ª** | *"O wake/resume também derruba o claim; reenviar o `0x08` na assinatura do wake cura"* (`RESET-02`) | 20/07 | **03/08:** o gate exige que o nó `sysfs` esteja no azul-default, e o `multi_intensity` mostra o **pedido**, nunca o aceso — provado quando o nó nasceu `0 0 0` com a barra acesa. O código registra: *"a condição está certa e é medida no lugar errado (…) casou nunca"* |
| **3ª** | *"O gatilho é o reinício do daemon"* — isto é, a **re-adoção** — e por isso reconectar/reiniciar muda o resultado (`LIGHTBAR-BT-CLAIM-01`) | 02/08 | **03/08, evento 6:** uma reconexão com o daemon **vivo** não travou, e outra no mesmo minuto travou. *"A diferença é o report, não o daemon"* |
| **4ª** | *"Sem o `0x08`, a reconexão obedece"* — o evento 6 da `CULPADO-01` lido como regra, e a base da remoção de 04/08 | 03-04/08 | **11/08, `lightbar-bt-sem-0x08-hoje-2300`:** sem `0x08` (removido havia sete dias), daemon **parado**, escrita direta — os dois do cabo acenderam e **os dois do rádio não**. O mesmo lado do suspeito com resultados **opostos**, que é a definição de variável não isolada |
| **(5ª, abortada)** | *"A instância de conexão nova cura"* — eu ia registrar isto como causa | 12/08 | **Ela**, antes de virar registro: *"não é só instância de conexão (…) é um falso positivo recorrente"*. E o `eliminacao.py` já devolvia `CONFUSO` para o suspeito |
| **(6ª)** | *"Quem tinha o `hidraw` aberto na probe (a Steam) é a causa"* — a substituta do proxy | 12/08 | **15/08, ela: "já superamos a steam"**, com o defeito vivo na mesa |

**A forma comum das seis, e é ela que se deve reconhecer no espelho:** cada uma
nasceu de uma **assimetria observada entre duas conexões** — uma travou, outra
não —, e cada uma atribuiu a assimetria à **variável que estava à mão**. Nas
seis, a variável era **proxy** de outra coisa que ninguém tinha medido. Enquanto
não existir um instrumento que leia o **estado real da barra** (§5.3), toda
assimetria entre duas conexões vai continuar produzindo uma sétima.

---

## 4. A SUPRESSÃO INCONDICIONAL — quando nasceu, e contra o quê

A linha, hoje, em `src/hefesto_dualsense4unix/core/backend_pydualsense.py:2329-2331`:

```python
handle._suppress_leds = (
    key in mapping or self._detect_transport(handle) == "bt"
)
```

**Ela tem duas idades, e isso importa.** GRAU: MEDIDO (`git log -S`).

- **A primeira metade (`key in mapping`) nasceu em 28/06, `a35dd85`**
  (`FEAT-DSX-LIGHTBAR-SYSFS-01`), e é a regra sã: *coberto pelo `sysfs` ⇒ o
  kernel é o dono*. Ali `_suppress_leds` nascia **`False`**.
- **A segunda metade — `or self._detect_transport(handle) == "bt"`, a supressão
  INCONDICIONAL — nasceu em 18/07, `bbfe74d`**, no **mesmo commit** que
  introduziu o `0x08`. O mesmo commit também fez `_suppress_leds` nascer `True`.

**Contra o que ela foi introduzida.** O corpo do commit é explícito:

> *"por BT a pydualsense fica SEMPRE suprimida (`LIGHTBAR-BT-NEVER-01` — o
> report BT dela é inadequado p/ LED e o nó sysfs atrasado rebaixava a supressão
> por 1 tick, re-envenenando)"*

São **dois** defeitos: (a) o report BT da pydualsense 0.7.5 era **malformado**;
(b) uma **corrida** — o nó `sysfs` chegando atrasado rebaixava a supressão por
um tick, e nesse tick um report com bits de LED saía na janela da adoção.

**As três justificativas históricas, e o que restou de cada uma.** O próprio
código as registra em `backend_pydualsense.py:2294-2320`:

| justificativa | situação hoje |
|---|---|
| *"o report BT da pydualsense 0.7.5 é MALFORMADO"* | **caducou em 19/07** — o `prepareReport` daqui não usa mais o report dela; o `BTREPORT-02` monta o `0x31` do kernel |
| *"a cor via pydualsense NUNCA funcionou por BT"* | **derrubada por MEDIÇÃO em 12/08** — o `0x31` bem-formado escrito no `hidraw` pintou os três controles do rádio |
| *"um write com flags de LED dentro da janela LATCHEIA a barra"* | **errou o culpado** — era o `0x08`, e ele saiu do código em 04/08 |

**Restou uma, e só uma: o `LIGHTBAR-BT-KEEPALIVE-01`.** É ela que sustenta a
supressão incondicional hoje, e é ela que proíbe religar a escrita de LED no
`report_thread`. Sobre ela, cinco fatos que a próxima frente precisa ter na mão:

1. **Ela é de 22/07** (`760855b`), e é **forense de captura**: `btmon` sobre 599
   reports `0x31` TX, todos com CRC válido. Não é ensaio de dois braços.
2. **Ela não tem sprint.** Existem **catorze** referências a
   `LIGHTBAR-BT-KEEPALIVE-01` em código, docs e testes, e **nenhum documento de
   sprint**. A medição vive na mensagem de commit e em comentário — que é
   exatamente a dívida que ela nomeou: *medição que fica só em comentário de
   código é dívida*.
3. **Ela é anterior a 12/08.** A regra que a própria casa escreveu depois de
   descobrir a Steam com a caneta na mão vale para ela também: *"Quem for
   reabrir qualquer conclusão de lightbar anterior a 12/08 pergunta primeiro:
   quem estava com o `hidraw` aberto naquele instante?"* **Ninguém perguntou
   isso à KEEPALIVE-01.**
4. **A cura dela entrou e o defeito continuou.** O `flag2` passou a sair zerado
   em 22/07; a barra seguiu apagada em 02/08, 03/08, 08/08, 11/08 e 12/08.
5. **Não há um único ensaio no caderno com este suspeito.** As quinze linhas de
   `luz.lightbar.cor@dualsense [radio]` não incluem *"o `flag2` de SETUP saindo
   no fluxo"*. Ele nunca entrou no caderno de eliminação.

> **A leitura, sem eufemismo:** a supressão incondicional é **cicatriz da era do
> `0x08`**. Das quatro razões que a criaram e a mantiveram, três caducaram com
> data e a quarta nunca foi remedida desde que a casa aprendeu a medir. Ela pode
> estar certa — e continua sendo a única peça central desta frente que **nunca
> passou pelo caderno**.

---

## 5. O QUE NUNCA FOI TENTADO

Esta é a seção que justifica o documento. Cada item é um caminho que **não
aparece em ensaio nenhum**, e a evidência é a ausência: o caderno de eliminação,
o CSV de ensaios e as sprints foram varridos.

**O estado do caderno, primeiro, porque ele enquadra tudo.** Rodando
`scripts/eliminacao.py` hoje, a linha `luz.lightbar.cor@dualsense [radio]` tem
**quinze suspeitos**: **três** marcados `e-a-causa`, **três** `CONFUSO`, **nove**
`inconclusivo` (um braço só) — e **ZERO inocentados**. Nenhum suspeito do rádio
foi jamais fechado pelos dois lados. **A poda — que ela chamou de a metade que
dá mais lucro — nunca foi feita nesta linha.**

### 5.1 Ler o ESTADO da barra no aparelho, e não o pedido

**Nunca foi tentado, e é a raiz de tudo.** Todo instrumento desta casa lê o que
**nós pedimos**: o `multi_intensity` é a memória da classe LED, a aba Lightbar é
o rascunho do perfil, e o `write(2)` do `sysfs` volta com sucesso antes de o
erro existir. **A única régua confiável em vinte e oito dias foi o olho dela.**

O caminho que apareceu **ontem e hoje** e que ninguém ligou a esta frente: em
14-15/08 os **dezessete feature reports declarados foram lidos nos quatro
controles** por Bluetooth, com duas descobertas de método — o `GET_FEATURE` por
BT exige **retry** (o `REPORT_REQ_TIMEOUT` de 3 s do BlueZ) e **validação de
`buf[0] == report_id`**, porque um dos controles devolveu um report com id
trocado. **Ninguém procurou, entre eles, um que devolva o estado de LED.** O
`0x22` **nunca foi lido por este projeto**; o `0xf6` tem 546 bytes e **não é
nomeado em documento nenhum**.

Este é o item **E3** da `CULPADO-01`, aberto desde 03/08, e a `LIGHTBAR-JOGADOR-01`
o mediu na tela em **27/07**. **Vinte e oito dias com o instrumento cego.**

### 5.2 O par assimétrico — branco travado, vermelho são, lado a lado, AGORA

**Nunca houve ensaio de assimetria entre unidades.** A revisão de hardware foi
refutada em 12/08 porque as três revisões estavam **representadas** — mas isso
responde *"a revisão prediz o resultado?"*, e **não** *"o que difere entre a
unidade travada e a sã na mesma mesa, no mesmo instante?"*.

E a casa **acabou de ganhar a régua**, sem saber: o `hardware_version` do
`sysfs` **distingue os quatro de graça** (achado de 14-15/08), e a cor de
fábrica está no serial (`GET_FEATURE 0x81`, caracteres 5 e 6). **Nada disso foi
cruzado com a lightbar.** A mesa de hoje — um travado e um são, ao vivo — é a
única oportunidade registrada em vinte e oito dias de ler as duas unidades lado
a lado com o defeito presente.

> ### E há um fato de HOJE que ninguém cruzou com esta frente
>
> A escada de reports medida em 15/08
> (`docs/protocol/dualsense-referencia-canonica.md:432-455`) usou **a lightbar
> do controle BRANCO, no rádio**, como instrumento — com o daemon parado, o olho
> dela, e controle positivo e negativo no mesmo desenho:
>
> | passo | report | pedido | o que ela viu |
> |---|---|---|---|
> | 1 | `0x31` 78 B | vermelho | **vermelho** |
> | 2 | `0x31` 78 B | apagar | **apagou** |
> | 3 | `0x32` 142 B | verde | **VERDE** |
> | 5 | `0x39` 547 B | azul | **AZUL** |
>
> **Duas leituras saem daí, e as duas importam para as frentes que estão
> medindo agora:**
>
> 1. **O branco obedeceu hoje, por rádio, em três reports diferentes.** Logo o
>    estado travado de agora **não é uma propriedade da unidade** — é um estado
>    em que ela entrou depois. Isso derruba, para a mesa de hoje, qualquer
>    hipótese de defeito físico ou de firmware permanente daquele plástico.
> 2. **"Apagar" funciona, e funciona por `0x31` com RGB zero.** O mecanismo pelo
>    qual alguém deixa a barra preta **está demonstrado e é barato**. Isto é a
>    ponte que faltava para o §5.7: não é preciso teorizar sobre quem apaga —
>    já se sabe **como** se apaga.
>
> GRAU: MEDIDO (olho dela, 15/08). **A ligação com o defeito é minha, e é SEM
> PROVA** — a escada não foi desenhada para esta frente, e ninguém verificou se
> o travamento de agora começou antes ou depois dela.

### 5.3 Medir o caso DOENTE em mesa limpa

**A probe limpa de 12/08 mediu o caso SÃO.** Com a mesa comprovadamente vazia
(Steam com 0 processos, daemon parado, **0** descritores de `hidraw` abertos por
qualquer processo), os três **nasceram acesos e os três obedeceram**. É um
resultado excelente — e é o **contrário** do que a frente precisa.

**Nunca se mediu, em mesa limpa, um controle que já está travado.** É o item 9
da tabela de abertos do protocolo da pilha (*"a volta do ensaio"*), e o próprio
documento diz que **não é formalidade**: o método desta casa pede ida **e**
volta. A ida está feita. **A volta nunca foi — e hoje ela é de graça, porque o
defeito está vivo.**

### 5.4 Decodificar o que sai no fio

**Nunca foi feito.** O item 7 dos abertos da pilha:

> *"que report a Steam manda nos 98 pacotes da rajada, e algum deles pede a
> barra apagada? — decodificar o payload das capturas em
> `/tmp/hefesto-probe-lightbar/`; **o parser escrito em 12/08 não venceu o
> formato do `btmon`**"*

Contaram-se pacotes; **nunca se leu um**. E o instrumento de captura **já
existe** (`scripts/capturar_a_probe_da_lightbar.sh`): o que faltou foi o
decodificador.

Com a Steam fora da mesa a pergunta melhora: **quem manda apagar?** Na probe
limpa saíram **6** pacotes de saída — *"dois por controle, que é o que o driver
manda sozinho"*. **Esses dois nunca foram decodificados.** São a única escrita
que existe quando não há mais ninguém, e ninguém sabe o que eles dizem.

### 5.5 O protocolo de JANELA

**Nunca foi construído**, e ele é o instrumento cuja falta já custou caro: um
dublê que registre **quando** cada report sai em relação ao
`controller_connected`. A `CULPADO-01` o descreve como *"o protocolo de medição
que faltou a esta casa duas vezes"*, e nomeia o preço: **quatro suspeitos foram
inocentados por engano por terem sido testados fora da janela**.

Enquanto ele não existir, **toda inocência declarada nesta frente vale só para o
regime, nunca para a janela** — inclusive as da §2.2.

### 5.6 O `flag2` de SETUP como suspeito de caderno

Ver §4. **É a única peça central desta frente que nunca entrou no caderno de
eliminação**, e ela é justamente a que hoje **proíbe** a rota mais promissora
(a escrita de LED no fluxo). O ensaio de dois braços que a julgaria — o fluxo
com e sem os bits de SETUP, mesa limpa, cor arbitrária, olho dela — **nunca foi
desenhado**.

### 5.7 Perguntar o que o firmware GUARDA, e quem manda apagar

Em 12/08 mediu-se algo que muda a leitura de *"apagado"* e que **ninguém
explorou**: o controle voltou de uma **desconexão completa** exibindo **magenta**
— a cor escrita por `hidraw` minutos antes, atravessando um `Disconnect` do
BlueZ e uma reconexão inteira.

E ele guarda **sem reforço nenhum**: **136 segundos cronometrados**, daemon
parado e Steam fechada (`cor-rota-hidraw-sem-steam-2235`), o dobro do prazo que
o ensaio pedia.

> **O corolário está escrito na canônica desde 12/08
> (`docs/protocol/dualsense-referencia-canonica.md:1111-1115`) e nunca virou
> ensaio:** uma barra apagada *"NÃO é o aparelho esquecendo a cor. É alguém
> mandando apagar, ou escrevendo preto. A pergunta certa passa a ser **quem
> escreveu, e com que report**."*

**A casa sabe, e o produto não faz** — que é o defeito mais caro daqui. Todas as
hipóteses do §2 perguntaram *"por que a nossa escrita não cola?"*; a pergunta
*"quem escreveu preto?"* está escrita na canônica, **e não existe uma linha de
ensaio para ela**.

### 5.8 O segundo escritor de hoje — e ele acabou de ser curado sem que ninguém ligasse

**Este é o item mais quente da lista.** Hoje, 15/08, dois defeitos foram curados
em `79ab98c` e `2877988`, e a mensagem do segundo descreve a assinatura exata do
sintoma desta frente:

> *"o contador de sequência do rádio não tem lock, e dois escritores no mesmo
> handle podem carimbar o mesmo número — **o firmware descarta e o log diz
> escrito**."*

E o primeiro cura o `fd` zumbi do `init` que estoura o tempo — *"e, às vezes,
uma thread"* de saída sobrevivendo. A `BT-SURDO-01` já tinha desenhado esse
mecanismo em **03/08** (o `report_thread` fantasma escrevendo `0x31` **com o
próprio `_bt_seq`** por cima do handle legítimo), e o `py-spy` nunca foi rodado.

**"O firmware descarta e o log diz escrito" é, palavra por palavra, o sintoma
desta frente** — escreve, o produto declara sucesso, a barra não muda. E a
`RESET-03` já tinha pago esse preço uma vez: *"escrever cru no `device` com seq
0 já matou uma cura desta casa"*.

**Nunca foi cruzado.** Ninguém perguntou se um `seq` duplicado explica as
escritas de cor que não colam. **É a hipótese mais barata da lista e a única que
já tem a cura no disco:** basta medir se o defeito muda de comportamento com o
daemon de hoje contra o de ontem. GRAU da ligação: **SEM PROVA** — e é
exatamente por isso que ela está aqui.

### 5.9 Fechar os nove `inconclusivo` do caderno

Nove suspeitos da linha do rádio têm **um braço só**. Fechar cada um custa **um
ensaio de dez segundos**, e o caderno já diz qual falta, suspeito por suspeito.
Entre eles: *"o daemon reescrevendo a cor DELE por cima de uma escrita externa"*,
*"a Steam APAGAR a barra em regime"*, *"o broker de `hidraw` do próprio produto
escondendo o nó"*. **Nenhum desses nove foi tocado desde 12/08.**

### 5.10 Cruzar a lightbar com o estado do RÁDIO

**Nunca foi feito, e a coincidência é grande demais para ficar sem ensaio.** Os
sete eventos da `CULPADO-01` são de 03/08 entre 17:48 e 20:04. As **44.718**
corrupções L2CAP da `RADIO-BOMBARDEADO-01` são de **23:59 do mesmo dia** até
00:28. **Mesmo boot, mesma mesa, mesma noite** — e **nenhum documento pergunta
se um enlace degradado explica uma barra que não obedece**. Hoje o barramento
foi inocentado e o **laço de escrita** virou o suspeito da frente de entrada; a
ponte com a lightbar continua sem ser feita.

---

## 6. A dívida de documento que ainda está cobrando juros

**Não é observação de estilo. Ela produziu um erro hoje, na minha frente.**

A afirmação *"sem `0x08` nenhum a barra ficou morta por 5 dias e 20 adoções
(medido 08/08)"* foi **falsificada em 11/08**: era docstring registrada como
medição, e a escavação do journal achou a barra **acesa** no rádio dentro
daqueles cinco dias, **quatro vezes**, três delas com fala literal dela (ensaios
`lightbar-bt-aceso-*`, `docs/data/ensaios.csv:31-34`).

O `cli/cmd_lightbar_reset.py` foi corrigido em 13/08 e serviu de molde.

**A dívida foi PAGA em 15/08, no mesmo dia em que esta página a cobrou.** Esta
seção nasceu dizendo *"a frase falsa continua viva em outros três lugares do
`src/`"* e listando os três por arquivo e linha. Os três foram corrigidos —
`core/backend_pydualsense.py` (docstring de `enviar_release_leds`, onde está
agora a correção inteira, com os endereços de ensaio), `cli/app.py` (docstring
do comando `lightbar-reset`, que é o texto do `--help`) e
`daemon/ipc_server.py` (o comentário do registro de `lightbar.reset`) —, e a
quarta cópia, que a auditoria do `src/` não via, saiu do docstring de módulo de
`tests/unit/test_lightbar_medir_o_0x08.py`.

Os endereços de linha da lista original **não** ficam registrados aqui: as
próprias correções moveram as linhas, e esta página não é portão de citação
(`scripts/validar-citacoes-de-linha.py` só cobre `docs/protocol/`), logo um
`arquivo:linha` daqui apodrece sem nada reprovar. O que fica é a busca que
refaz a conferência: `grep -rn "20 adoções" src/ tests/`. Ela é a que morde,
porque *"20 adoções"* é a metade da frase que nenhuma das correções reescreveu
— *"morta por 5 dias"* atravessa uma quebra de linha em
`backend_pydualsense.py` e escapa da busca ingênua. Em 15/08 ela devolve **duas
linhas, as duas em contexto de REFUTAÇÃO** (`backend_pydualsense.py` e
`tests/unit/test_lightbar_medir_o_0x08.py`), e nenhuma afirmativa.

Por que a seção fica de pé mesmo paga: durante a escrita deste documento uma
frente de pesquisa leu a frase no `backend_pydualsense.py`, tratou-a como
medição e concluiu que o `0x08` estava refutado **por aquela evidência**. A
conclusão é certa; a evidência era falsa. **Um fato errado no `src/` não fica
parado: ele recruta** — e este é o caso medido que prova a regra.

A regra dela, de 11/08, decidiu o caso: *fato errado se SUBSTITUI*. Não havia
custo já pago a preservar, só um número que a medição derrubou.

---

## 7. O que eu diria às outras duas frentes

1. **Não gastem um minuto com o `0x08`, com a adoção, com o cache do `sysfs`,
   com a revisão de hardware, com a personalização por MAC ou com o rádio
   emudecendo.** Os seis estão medidos e caídos (§2). Se a medição de vocês
   apontar para um deles, o mais provável é que a régua esteja mentindo.
2. **A Steam saiu, mas a lição dela ficou:** antes de concluir qualquer coisa,
   **anotem quem está com o `hidraw` aberto no instante da probe**
   (`readlink /proc/*/fd` + `fdinfo`) e **quem está no fio** (`btmon`). Toda
   conclusão desta frente anterior a 12/08 caiu por não ter esse denominador.
3. **Não concluam nada a partir do `multi_intensity` nem da aba Lightbar.** Os
   dois mostram o **pedido**. Para provar obediência, use **cor que ninguém mais
   queira**, com o **daemon parado** — a regra que a casa pagou para aprender.
4. **Se a conclusão de vocês tiver a forma "reconectar/reiniciar/re-adotar
   cura", parem.** Ela já caiu quatro vezes documentadas e duas a mais (§3), e
   sempre pela mesma razão: a variável observada era proxy. Antes de escrever,
   respondam **o que derrubou a conclusão anterior**.
5. **O par assimétrico que está na mesa de vocês é o ativo mais raro desta
   frente inteira** (§5.2). Em vinte e oito dias ninguém teve um travado e um são
   lado a lado com instrumento na mão. **Leiam os dois, não só o doente** — e
   registrem `hardware_version` e serial de fábrica dos dois antes de qualquer
   outra coisa.
6. **A pergunta que ninguém fez é "quem mandou apagar?"** O firmware **guarda** a
   cor entre conexões, e por **136 s sem reforço** (medido em 12/08), logo
   apagado não é esquecimento — a canônica já escreveu isso em
   `dualsense-referencia-canonica.md:1111-1115` e **nunca virou ensaio**. Os
   dois pacotes de saída que o driver manda sozinho na probe **nunca foram
   decodificados** (§5.4).
7. **Olhem a escada de HOJE antes de qualquer coisa** (§5.2): o mesmo controle
   branco obedeceu a vermelho, verde e azul por rádio em 15/08, com o daemon
   parado e o olho dela. **O estado travado de agora não é propriedade da
   unidade**, e a operação "apagar" já está demonstrada por `0x31` com RGB zero.
8. **Antes de investigar do zero, olhem o que a casa curou hoje** (§5.8): o
   `seq` sem lock e o `fd`/thread zumbi do `init-timeout` produzem, os dois,
   *"o firmware descarta e o log diz escrito"* — que é a assinatura literal
   deste defeito. **É a hipótese mais barata que existe e a única cuja cura já
   está no disco.**
9. **Não desliguem nenhum controle.** O defeito vivo é a evidência, e um
   power-off físico o apaga junto com ele.

---

## 8. O que fica ABERTO, e é dela

- **A supressão incondicional por BT continua de pé sobre uma única justificativa
  de 22/07 que nunca virou sprint e nunca foi remedida** (§4). Mexer nela é
  decisão de engenharia com risco medido em julho; **remedi-la** não é, e custa
  um ensaio de dois braços.
- **A linha `luz.lightbar.cor` do mapa carrega duas descrições contraditórias**
  (§0, aviso 4) e três afirmações de julho já derrubadas. É a memória externa
  dela — e hoje ela contradiz a si mesma.
- **O caderno de eliminação está desatualizado na conclusão de topo:** marca
  `E-A-CAUSA` para a Steam, que ela derrubou hoje. **Não editei o CSV** — é
  território de outra frente, e o caderno é portão.
- **Nenhum dos quinze suspeitos do rádio está inocentado.** A poda nunca
  aconteceu nesta linha.

---

**Nada neste documento foi executado.** É estudo. A árvore não foi tocada,
nenhuma escrita foi feita em `hidraw`, nenhum serviço foi reiniciado, nenhum
controle foi tocado ou desligado, e a única coisa que rodou foi
`scripts/eliminacao.py`, que só lê `docs/data/ensaios.csv`.
