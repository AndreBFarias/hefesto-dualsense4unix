# ÁUDIO-QUE-TRANCA-01 — um toque no volume congela a troca de perfil

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA** — três defeitos encadeados, todos nascidos nas levas
  de 29/07 a 02/08, e o primeiro deles **não tem porta de saída**
- **Faixa:** 1 — o produto trava sozinho e não avisa
- **Causa-raiz:** **PROVADA no código** nos três casos
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Paga:** o furo que a
  [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md)
  já nomeou (linha 647, citando `autoswitch.py:505-518`) e que ganhou um
  gatilho novo em 02/08
- **Também no índice:** [A leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)
  — a E1 e a E2 são dívida declarada de **três** sprints daquela leva, e
  nenhuma delas as toca

---

## Nota datada — 05/08/2026: a E2 foi AGRAVADA, e a agravante mora noutro arquivo

**Esta sprint continua PROPOSTA e nada dela foi tocado.** A nota existe porque a
[TRAVA-QUE-SOLTA-TARDE-01](2026-08-05-TRAVA-QUE-SOLTA-TARDE-01-o-gesto-explicito-e-vitima-da-propria-trava.md)
**declara que agrava a E2 desta sprint**, e essa afirmação vivia só no arquivo
novo: a sprint agravada não sabia disso. A referência cruzada é o que esta nota
paga. Nada abaixo foi apagado.

### A frase, e de onde ela vem

A `TRAVA-QUE-SOLTA-TARDE-01` mediu, com o daemon de produção dela, que os
**dois** gestos explícitos de troca de perfil — `profile.switch` (janela e CLI)
e o **PS + D-pad** — chamavam `clear_manual_trigger_active()` **depois** do
`activate`. A trava era limpa **tarde demais para a ativação que a limpou**, e
o perfil entrava pela metade. E escreve, textualmente:

> *"E este agrava a E2 daquela: dar granularidade por categoria ao autoswitch,
> como a E2 propõe, **não cura o caminho manual** — lá o problema não é
> granularidade, é ordem."*

### O que isso muda na leitura desta sprint

**Grau: MEDIDO**, por leitura do código em 05/08.

1. **A E2 nunca teria curado o caminho manual, e o texto acima não dizia isso.**
   A E2 propõe que o autoswitch pergunte pelas categorias que **ele** vai
   aplicar. Só que o gesto explícito dela **não passa pelo autoswitch** — passa
   por `_handle_profile_switch` e por `subsystems/hotkey.py`. Quem lê a E2 hoje
   pode concluir que ela cobre a queixa *"às vezes pega"*: **não cobre**. A
   metade manual daquela queixa foi de outra causa e já foi curada;
2. **a E2 encolheu de alcance e NÃO de importância.** Ela continua sendo a única
   saída para *"um toque no volume mata a troca automática"*, que é o defeito 1
   desta sprint visto pelo lado do autoswitch — e continua sendo a única coisa
   que impede a **próxima** categoria de herdar o mesmo defeito. É a terceira vez
   que a casa paga por isso, e o número não mudou;
3. **o aceite da E2 precisa ser medido no tique, não no clique.** Com a cura da
   `TRAVA` de pé, o gesto explícito **limpa as três categorias antes** de
   ativar — então um teste que arme `audio`, troque de perfil pela janela e
   observe o perfil entrar **passa mesmo sem a E2**. O aceite honesto é: armar
   `audio`, deixar a **troca automática** decidir, e exigir que um perfil sem
   seção de áudio entre. A frase original da E2 (*"com só `audio` armado, um
   perfil que não tem seção de áudio entra normalmente"*) continua certa —
   **falta dizer por qual porta**.

### O que a cura da TRAVA NÃO fez, e continua aqui

**Grau: MEDIDO** por `git grep` em 05/08:

- **`clear_manual_trigger_active("audio")` continua não existindo** em `src/`
  nem em `tests/`. O defeito 1 desta sprint está **intocado**, e a
  `TRAVA-QUE-SOLTA-TARDE-01` o declara em aberto no próprio texto;
- **`manual_trigger_active` continua booleano de tudo-ou-nada**
  (`state_store.py:425-428`), e o autoswitch continua consultando **o booleano**
  (`autoswitch.py:579` e `:624`). A E2 está exatamente onde estava;
- **`_marcar_audio_manual` continua armando também na devolução da posse** — a
  ação que significa *"não tenho mais opinião sobre o áudio"* continua sendo a
  que tranca.

### Os números de linha desta sprint envelheceram

A tabela de clears do defeito 1 foi escrita em 03/08 e **as quatro linhas
mudaram de lugar** com as curas da madrugada de 04-05/08. Conferido em 05/08, e
registrado aqui em vez de reescrito acima:

| clear | linha em 03/08 | linha em 05/08 |
|---|---|---|
| `clear_manual_trigger_active("trigger")` | `ipc_handlers.py:676` | `ipc_handlers.py:710` |
| `clear_manual_trigger_active("rumble")` | `ipc_handlers.py:2671` | `ipc_handlers.py:2705` |
| global, no `profile.switch` | `ipc_handlers.py:412` | **`ipc_handlers.py:430`, e agora ANTES do `activate`** |
| global, na hotkey | `hotkey.py:163` | **`hotkey.py:168`, e agora ANTES do `activate`** |
| global, no autoswitch | `autoswitch.py:508` | `autoswitch.py:627` |

**A lista continua completa e continua sem `"audio"`.** O que mudou foi a
**ordem** nos dois gestos explícitos, e os dois ganharam restauração das
categorias no `except` — ativação que falhou não é gesto cumprido.

### E há canal novo para ver isto acontecer

A [PERFIL-REESCRITO-NA-PARTIDA-01](2026-08-05-PERFIL-REESCRITO-NA-PARTIDA-01-o-perfil-dela-era-reescrito-sozinho-no-meio-da-partida.md)
(item 4) fez o `ProfileManager.apply` **relatar** as categorias que a trava
silencia, com o estado `ignorado_trava_manual`, e a
[ATIVAR-NÃO-MENTE-01](2026-08-05-ATIVAR-NAO-MENTE-01-o-botao-que-parecia-falhar-e-ativava-duas-vezes.md)
fez a janela **ler** esse relatório.

**Consequência prática para quem for executar a E1 e a E2:** o efeito do defeito
1 desta sprint deixou de ser invisível. Ele agora aparece no relatório da
ativação e no `secoes=` do `profile_autoswitch` — e, pela nota de parentesco
daquela sprint, `trigger`/`led` com `ignorado_trava_manual` passam a ser
**raros na rota manual** (a trava é limpa antes) e **frequentes** nas ativações
do autoswitch e no restore de boot. **É por ali que a E2 se mede.**

## Defeito 1 — a categoria `audio` congela a troca automática de perfil INTEIRA

**Nasceu no commit `c10adaf`** (a leva do alto-falante).

### Os dois lados

- **quem arma:** `daemon/state_store.py:58-60` acrescentou `"audio"` a
  `MANUAL_OVERRIDE_CATEGORIES`, com a justificativa correta — *"volume é ajuste
  manual como qualquer outro"*;
- **quem obedece:** `daemon/state_store.py:424-426`:
  ```python
  @property
  def manual_trigger_active(self) -> bool:
      """True se QUALQUER categoria de override manual está armada."""
      return bool(self._manual_override_categories)
  ```
  e é **esse booleano** que o autoswitch consulta (`profiles/autoswitch.py:505-518`).

**Com o booleano ligado, `_activate` retorna para toda troca de janela** — salvo
a exceção estreita "o candidato é regra própria de jogo E difere do ativo".

**Consequência: um toque no volume mata a troca automática de perfil para
gatilhos, LEDs, rumble e modo.**

### E não existe porta de saída

Conferido na árvore inteira — os clears que existem:

```
daemon/ipc_handlers.py:676    clear_manual_trigger_active("trigger")
daemon/ipc_handlers.py:2671   clear_manual_trigger_active("rumble")
daemon/ipc_handlers.py:412    clear_manual_trigger_active()        (global)
daemon/subsystems/hotkey.py:163  clear_manual_trigger_active()     (global)
profiles/autoswitch.py:508       clear_manual_trigger_active()     (global)
```

**Não há `clear_manual_trigger_active("audio")` em lugar nenhum.** As duas
irmãs têm o par armar/limpar; a nova só tem o armar.

Pior: `_marcar_audio_manual` (`daemon/ipc_handlers.py:2960-2975`) arma **também
na devolução da posse** — ou seja, a ação que significa *"não tenho mais opinião
sobre o áudio"* é justamente a que tranca.

### E isso explica o que já funcionava

Antes de `c10adaf`, **nada no caminho de áudio conseguia armar esse booleano**.
A trava existia e era acionada só por gestos que tinham o clear correspondente.

**Agravante que torna o defeito invisível:** por Bluetooth o controle deslizante
do alto-falante *"muda um registrador que não tem o que tocar"* — palavras da
`SOM-02` (`2026-07-29-SOM-02-o-alto-falante-que-funciona.md:511`). **O gesto que
armou a trava foi inaudível.** Ela não teria como associar "mexi no volume" a
"os perfis pararam de trocar".

---

## Defeito 2 — o seletor de canal manda volume ZERO, no controle ERRADO

**Nasceu no commit `19acbeb`** (o redesenho do bloco Alto-falante).

`app/widgets/controller_card.py:3010`:

```python
ok = ipc_bridge.speaker_set(rota=rota)
```

**Sem `volume`. Sem `uniq`.** Os três irmãos do mesmo widget passam identidade:

```python
:2963   ipc_bridge.speaker_set(volume=volume, uniq=uniq)
:3036   ipc_bridge.speaker_set(muted=muted,  uniq=uniq)
:3049   ipc_bridge.speaker_set(release=True, uniq=uniq)
```

### (a) O primeiro clique tranca o alto-falante em zero

O caminho, conferido em `core/backend_pydualsense.py:2337-2366`:

```python
if pref is None:
    pref = 0
handle._speaker_volume_pref = pref
efetivo = 0 if muted else pref          # = 0
...
handle.set_audio_volumes(headphone=efetivo, speaker=efetivo, ...)
```

**Toma a posse dos bytes de áudio e escreve zero nos dois.**

Isto tem nome nesta casa: *"Armadilha 1 — `speaker.set {}` toma a posse e manda
ZERO"* (`2026-07-29-SOM-02-o-alto-falante-que-funciona.md:77`). A regra está
escrita em **três** lugares que o chamador novo viola — inclusive na docstring
do método **irmão, três telas acima** (`controller_card.py:2942-2944`) e num
validador de schema que **recusa** perfil sem `volume`
(`profiles/schema.py:359-392`).

### (b) E escreve no controle errado

Sem `uniq`, o daemon usa o **primário**. Com quatro cards na tela, clicar no card
do Controle 3 escreve no Controle 1.

### (c) E arma o defeito 1

`speaker.set` passa por `_marcar_audio_manual` → autoswitch congelado, sem
clear.

**Os três efeitos saem de um clique num seletor que a usuária lê como "escolher
onde o som sai".**

---

## Defeito 3 — o botão do microfone e a política do instalador se anulam

**Nasceu no commit `5801de9`** (a cura do defeito 1 da `BT-E-VPAD-01`).

A cura fechou o botão atrás de `fonte_padrao_e_o_controle()`
(`integrations/audio_control.py:95-114`), e a decisão está **certa**: não fazer
nada é melhor que mutar o microfone errado.

**O problema é que a condição é impossível por política do próprio projeto.**

- `assets/wireplumber/51-hefesto-dualsense-no-default-source.conf` existe para
  **impedir** o DualSense de virar fonte padrão;
- `scripts/doctor.sh:532` chama isso, por extenso, de *"a política DEFAULT do
  install: rebaixar"*.

Numa instalação com os padrões de fábrica, **o DualSense nunca é a fonte padrão
— logo o botão do microfone nunca age.**

### O paradoxo, e ele está no journal dela

Na sessão de 02/08, duas vezes:

```
21:05:07  system_check_warning  detail='WirePlumber fixou o DualSense como
                                        microfone padrão — rode: scripts/doctor.sh --fix'
```

Nesta máquina o DualSense **está** como fonte padrão (contra a política), e é
**por isso** que o botão do microfone dela funciona. **O projeto avisa duas
vezes por sessão para ela consertar isso — e consertar desliga o botão do
microfone.**

### O que foi REFUTADO nesta investigação, e o registro fica

Uma hipótese levantada e **medida como falsa**: a de que o casador
`"dualsense" in saida.lower()` não casaria o nome real do nó, porque o PipeWire
o montaria como `..._Wireless_Controller-...` sem "DualSense".

**Medido nesta máquina, em 03/08:**

```
alsa_input.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00.iec958-stereo
```

O nome **contém** "DualSense" e o casador devolve `True`. **A hipótese está
refutada e não deve ser reaberta.**

Fica registrada uma dívida menor, e não é a mesma coisa: o casador canônico da
casa usa **três** marcadores (`app/mic_monitor.py:55-60`) porque o PipeWire monta
o nome a partir das strings USB, que variam por firmware. Um marcador só é
frágil — mas é **robustez**, não defeito ativo.

---

## As entregas

### E1 — a categoria `audio` ganha o clear que falta

O par armar/limpar tem de estar completo, como nas irmãs.

**Onde:** o clear entra ao lado de `clear_manual_trigger_active("trigger")`
(`daemon/ipc_handlers.py:676`), no ponto simétrico do caminho de áudio.

**E o `release` para de armar.** `_marcar_audio_manual`
(`daemon/ipc_handlers.py:2960-2975`) é chamado também na devolução da posse; ali
ele deve **limpar**, não armar — devolver a posse é dizer "não tenho mais
opinião".

**Aceite:** ajustar o volume e depois devolver a posse → a troca automática de
perfil volta a funcionar. Medível sem hardware.

### E2 — a trava deixa de ser um booleano de tudo-ou-nada

`manual_trigger_active` responde `True` para qualquer categoria, e o autoswitch
o usa como portão único. Isso significa que **qualquer** categoria futura
herdará este defeito — é a terceira vez que a casa paga por isso.

O autoswitch precisa perguntar pelas categorias que **ele** vai aplicar, não por
"alguma coisa está travada".

**Aceite:** com só `audio` armado, um perfil que não tem seção de áudio **entra**
normalmente. Medível sem hardware, e é a mordida: arranque a granularidade e o
teste reprova.

**Nota de escopo:** a [POSSE-POR-CONTROLE-01](2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md)
mexe no **mesmo** `manual_override_categories`, no eixo por controle. **As duas
entregas tocam a mesma estrutura** — executá-las na mesma leva, e nesta ordem
(categoria primeiro, controle depois), evita duas migrações do mesmo campo.

### E3 — o seletor de canal passa a mandar volume e identidade

`controller_card.py:3010` passa a chamar
`speaker_set(rota=rota, volume=<o vigente>, uniq=uniq)`, como os três irmãos.

**Aceite, e são três:**

1. clicar no seletor de canal **não** muda o volume;
2. clicar no card do Controle 3 escreve **no Controle 3**;
3. clicar no seletor **não** congela a troca de perfil (consequência da E1).

**A mordida:** um teste de card com dois `uniq` distintos, espionando
`ipc_bridge.speaker_set` e conferindo os kwargs. Hoje **nenhum teste cobre
isto** — e é por isso que passou.

### E4 — a regra "quem manda rota manda volume" vira guarda, não convenção

O defeito 2(a) aconteceu porque a regra estava escrita em três documentos e
numa docstring vizinha — e **nada a impunha no código**.

`set_speaker_volume` deve **recusar** (ou herdar explicitamente o vigente) uma
chamada que peça rota sem volume, em vez de silenciosamente assumir zero.

**Aceite:** `speaker.set {rota: 2}` sem volume não zera o alto-falante. O
`profiles/schema.py:359-392` já recusa isso em perfil — **a mesma regra passa a
valer no caminho vivo.**

**Por que é raiz:** o `pref = 0` transforma "não me disseram" em "me disseram
zero". Essas duas coisas nunca deveriam ter o mesmo valor.

### E5 — a política do microfone deixa de brigar consigo mesma

Duas saídas honestas, e a escolha é **de produto, dela**:

- **(a) o botão passa a agir sobre o microfone do controle onde ele foi
  apertado**, independentemente de quem é a fonte padrão do sistema. É o que a
  usuária espera de um botão físico — e resolve de quebra o fato de que o botão
  hoje só existe no controle **primário** (`core/backend_pydualsense.py:1920-1926`
  lê `micBtn` só do primário: **os botões dos controles 2, 3 e 4 nunca viram
  evento**);
- **(b) manter a regra da fonte padrão e retirar o drop-in 51** dos padrões de
  instalação, assumindo que o DualSense seja a fonte padrão quando presente.
  Barato, e muda o comportamento de áudio da máquina inteira dela.

**Recomendação: (a).** Ela é a única que sobrevive a quatro controles.

**Aceite mínimo, qualquer que seja a escolha:** o `system_check_warning` para de
recomendar um conserto que quebra outro recurso. Se a (b) for escolhida, o aviso
sai; se for a (a), o aviso deixa de ter relação com o botão.

---

## Testes que vão reprovar

```
pytest tests/unit -k "speaker or audio or autoswitch or manual or override or mic"
```

O `test_som_*` e o `test_autoswitch_*` travam o comportamento atual em vários
pontos. Confira caso a caso se o teste trava **a regra** (mantenha) ou **o
sintoma** (encare).

## O que NÃO fazer

- **Não tirar `"audio"` da lista de categorias** como cura do defeito 1. A
  justificativa de `c10adaf` está certa: volume é ajuste manual e merece a
  trava. O que falta é o clear e a granularidade;
- **Não fazer o `release` limpar TUDO.** Ele deve limpar `audio`, não a trava de
  gatilho que ela armou noutra aba;
- **Não reabrir a hipótese do casador do microfone** — foi medida e refutada em
  03/08 (o nome contém "DualSense" nesta máquina);
- **Não mexer no drop-in 51 sem decidir a E5.** Ele existe por um defeito real:
  o DualSense virava microfone padrão sozinho e o áudio da máquina ia junto.

## O que fica ABERTO

- **a escolha (a)/(b) da E5** — é dela;
- **o botão do microfone dos controles 2, 3 e 4**, que nunca vira evento. Entra
  na E5(a) se ela escolher essa saída; caso contrário, vira sprint própria.
