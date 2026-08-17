# ÍNDICE — a bancada de oito horas

- **Escrito em:** 16/08/2026 à noite, na branch `restauro/inicio-da-sessao`,
  sobre `66b3057` (último commit do dia, 21h26).
- **Grau:** **REGISTRO DE EXECUÇÃO.** Não é plano. O plano do que sobrou é o
  [PONTO-A-PONTO-01](2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md),
  e esta página **não o duplica** — aponta.
- **O que cobre:** a bancada com ela, **com o aparelho na mão**, de **13h42**
  (primeira medição registrada) a **21h26** (último commit). Cinco commits.
  A madrugada do mesmo dia (01h18 e 06h1x, quinze commits) é outra leva e está
  na §7, porque nenhum índice a citava.
- **As três fontes primárias**, e tudo aqui tem endereço numa delas:
  - [O RÁDIO MEIO MUDO](../estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md)
    — os três defeitos, os onze suspeitos eliminados, os três erros de régua.
  - [O PS PRESO](../estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md)
    — o defeito que **eu** causei durante a medição, e as duas rodadas dele.
  - [PONTO A PONTO 01](2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md)
    — a lista dela, em sete pontos, na ordem do que custa mais por dia.

---

## 1. Como ler, se você tem cinco minutos

1. **§2** — o que quebrou e foi consertado, com o commit de cada um.
2. **§3** — os **quinze suspeitos eliminados**. Vale tanto quanto as curas: são
   becos que ninguém precisa percorrer de novo.
3. **§5** — as **três regras novas** de metodologia. Duas nasceram de defeito
   meu, hoje.
4. **§4** — o que segue aberto, com dono e endereço.

**A frase dela que reorientou o dia inteiro:**

> *"a falha não pode ser o jogo. (…) o dont scream e o pragmata funcionavam no
> rádio, o duskfade que nunca funcionou no cabo e no radio teve input que
> funcionou."*

Ela separou três casos que estavam sendo tratados como um. A medição confirmou:
**DON'T SCREAM e Pragmata** são o defeito 1; **Duskfade** é caso próprio.

---

## 2. O que quebrou e foi consertado

| # | o quê | commit | endereço da cura | portão |
|---|---|---|---|---|
| 1 | **Áudio do mic lido como estado de botão.** Com a ponte do mic ligada, o DualSense manda Opus no MESMO report `0x31`, 78 bytes, **CRC-32 válido**. Só o bit `0x02` do byte 1 separa áudio de input, e o `_struct_base` não o conferia: os bytes de Opus caíam sobre `buttons[2]`, onde moram MIC e PS | `702f5b6` | `core/physical_report_reader.py:382` (filtro) e `:143` (`INPUT_FLAG_AUDIO` espelhado, travado por teste no valor de `integrations/dualsense_bt_audio.py:189` — o caminho quente não pode importar `ctypes`/`libopus`) | `tests/unit/test_ps_preso_01_audio_lido_como_botao.py` — 10 testes; arrancar o filtro reprova 8 |
| 2 | **O portão do ciclo conecta-cai-reconecta**, que não existia. Havia teste para a PERDA e para o estado estático; nenhum para a transição, que é onde mora o defeito 1 | `a053265` | — (é portão, não cura) | `tests/unit/test_reconexao_bt_01_o_leitor_tem_de_voltar_sozinho.py` — 3 testes. **Passam contra o código de hoje**, e é esse o resultado: eliminam o `EvdevReader` como culpado (§3) |
| 3 | **`quem_o_jogo_abre.py` acusava a própria cura de não existir** — lia o environ do **primeiro** processo da árvore, o `reaper` da Steam, que roda ANTES do wrapper | `5fb46df` | `scripts/ensaios/quem_o_jogo_abre.py`, função `processo_do_jogo` — critério **estrutural** (o processo mais fundo que casa com o padrão), nunca por conteúdo | — |
| 4 | **O microfone não tinha volume nem mudo no perfil**, só um booleano; o alto-falante tinha os dois. A assimetria aparecia na tela | `66b3057` | `profiles/schema.py` (`ProfileMicConfig`: `volume` 0–100, `muted`, os dois opcionais, `None` = sem opinião) | `tests/unit/test_mic_button_exposto.py` — 13 testes |
| 5 | **`Soltar` virou `Liberar`** nos DOIS blocos, mic e alto-falante | `66b3057` | `app/widgets/controller_card.py` | dois testes que travavam texto literal foram reancorados na constante |

**Volume do mic é do CAMINHO, não do firmware** (`medido` como decisão de
desenho, `inferido-do-codigo` como comportamento): é o *source* do sistema, por
isso vale igual no cabo e no rádio — que é o *"independente de saber se tá via
bt ou via cabo"* do pedido dela. O DualSense não expõe ganho de captura; o que
existe no firmware é o mudo, e quem fala com ele é o `muted`.

### 2.1. O que foi diagnosticado e NÃO foi consertado hoje

| defeito | estado | onde |
|---|---|---|
| **1 — a reconexão BT mata a entrada** | reproduzido ponta a ponta, **sem cura**. Cura de hoje: `systemctl --user restart hefesto-dualsense4unix` (verificado: o input volta na hora) | O RÁDIO MEIO MUDO, "DEFEITO 1"; plano em PONTO-A-PONTO §1 |
| **2 — no rádio, metade do controle não atravessa** | lightbar e LED de jogador funcionam; gatilho, vibração, som, touchpad e giro falham **dentro do jogo**. O repasse do vpad foi medido e está **íntegro** | O RÁDIO MEIO MUDO, "DEFEITO 2" |
| **3 — o vpad pode nascer morto** e o daemon diz `{"enabled": true, "degraded": false}` | medido às 13:42:42: `0003:054C:0DF2.0038` com driver NENHUM. Recriar resolve → é **corrida**, não defeito permanente. `wait_for_bind()` existe (`integrations/uhid_gamepad.py:1883`) e **não segurou**; ninguém sabe por quê | O RÁDIO MEIO MUDO, "DEFEITO 3" |
| **4 — a ponte do mic disputa o hidraw** com o `motion_reader` (mesmo `/dev/hidraw5`, sem arbitragem) | **causado por mim durante a medição.** Ponte parada, módulo do PipeWire descarregado, `bt_mic: enabled=false`. Sem cura de produto | O PS PRESO, parte 1 |
| **5 — PS preso vira laço de spawn**, sem debounce nem limite | sem cura | O PS PRESO, parte 2 |
| **6 — `wmctrl` ausente transforma foco em lançamento** | sem cura. É `warning` em `integrations/steam_launcher.py:83` e nunca chega a ela; o fallback está em `:178` (`refocus_fallback_spawn`) | O PS PRESO, parte 3 |

**O defeito 1 é o que estragou a sessão dela** e mandou horas de investigação
para o lugar errado. O gancho da cura já existe e hoje **só avisa**:
`state_stale_neutral_warning` (`daemon/ipc_handlers.py:2142`) já sabe dizer que
estagnou, e `evdev_read_lost` (`core/evdev_reader.py:1116`) é logado sem
tratador nenhum.

---

## 3. O que foi ELIMINADO, e com que medição

Isto é metade do valor do dia. **Não repita nenhum destes.**

| suspeito | como caiu | grau |
|---|---|---|
| o jogo / o Proton | ela: os três funcionavam antes. E o controle **não respondia nem no desktop** — jogo nenhum envolvido | medido |
| o wrapper `hefesto-launch` | presente e correto no ambiente do processo do jogo: `PROTON_DISABLE_HIDRAW=0x054C/0x0CE6` | medido |
| o vpad ser pego pelo próprio IGNORE | o vpad é Edge `054c:0df2`; o IGNORE é `054c:0ce6`. Esconde só o físico, como projetado | medido |
| o jogo não enxergar o vpad | o `winedevice.exe` tinha o `hidraw4` aberto, e o jogo mostrava "Estilo de entrada: PlayStation" | medido |
| CRC do BT | 97 no dia (~1/min) e **zero** em 12 s de movimento contínuo. O kernel não reclamou | medido |
| o grab oscilando | `grab=held`, `regrab=0` em 7 amostras; `poll.tick` subindo ~59/s | medido |
| o gate de foco X11 | `x11_focus_gate_no_x_focus` é do autoswitch (troca de perfil), não do despacho de input | inferido-do-codigo |
| o daemon parar de emitir | o vpad emitia 500 eventos/8 s e 525 reports/6 s. Emitia — só que **neutros** | medido |
| a supressão de emulação | `emulation_suppressed` é da emulação de desktop; `gamepad_emulation.enabled` seguia `true` | medido |
| o perfil não entrar | `active_profile: Pragmata`, autoswitch pegou, `supressao=aplicado` | medido |
| `launch_arm_pulado_allowlist_steam_input` | intencional: para jogo na allowlist pula-se **só** a seção `mode` | inferido-do-codigo |
| **os `VALID_FLAG*` / "o vpad está meio mudo"** | duas réguas independentes: giro 7 231 no vpad contra 19 435 no físico; touchpad 2 807 contra 3 660; e no report de 64 bytes do `hidraw4` variam `2,3 · 7 · 16–27 · 28–32 · 33–36`. **O vpad entrega tudo, pelos dois caminhos** | medido |
| **o `EvdevReader` como culpado da reconexão** | os 3 testes do ciclo (`a053265`) **passam** contra o código de hoje: ele reabre no nó novo, não insiste no número velho, sobrevive a sumiço prolongado. O `_locate` procura por IDENTIDADE, e segura | medido (portão permanente) |
| **os bytes de Opus como causa do travamento da ponte** | com o filtro do bit de áudio já no daemon (reiniciado às 21:04 — conferido), a ponte travou **em 10 segundos**, igual. O filtro está certo e fica; só não era esta causa | medido |
| a emulação de mouse/teclado do daemon no episódio do PS | `mouse_emulation.enabled=false`, `keyboard_emulation.despachando=false` | medido |

**E o par que fechou o dia**, o ensaio mais limpo: mesma sessão do jogo, mesmo
vpad (`003C` dos dois lados, não recriado), mesmo daemon, **única variável cabo
→ rádio**. **Funciona no cabo. Para no rádio.** Uma variável, um veredito.

---

## 4. O que continua aberto

**O plano é o [PONTO-A-PONTO-01](2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md)**,
ordenado por quanto custa a ela por dia. Aqui vai só o mapa, para você escolher
por onde entrar:

| # | item | prioridade |
|---|---|---|
| 1 | a reconexão BT que mata a entrada | P0 |
| 2 | as regressões, e o portão do CICLO que impede a volta | P0 |
| 3 | o som do alto-falante no rádio — **dívida de GRAU**, não de número | P1 |
| 4 | parear campo a campo o que o físico manda e o que o virtual repassa | P1 |
| 5 | mic, giro e touch nos jogos que **funcionavam** (DON'T SCREAM, Big Walk) | P1 |
| 6 | o touchpad engasgando — primeira suspeita sou eu, com os instrumentos | P2 |
| 7 | Duskfade — caso próprio, sem causa | P3 |

Fora dessa lista, ficam abertos:

- **Quem alimenta o quê no rádio** — o `motion_reader` cicla a cada 30 s em
  silêncio (`core/physical_report_reader.py:840`) e o giroscópio chega ao vpad
  assim mesmo. Os dois fatos podem conviver (dois caminhos de leitura), mas
  **ninguém mediu qual alimenta qual**. Grau: `incerto`.
- **Por que o `wait_for_bind` não segurou** o vpad natimorto.
- **Arbitrar o hidraw** entre a ponte do mic e o `motion_reader`. O broker já é
  o dono da posse (`integrations/hidraw_broker_client.py:168`): é ele que tem de
  recusar o segundo pedido, ou multiplexar. **A ponte não volta a subir sem
  isto** — decisão do dia, e a razão é nova (não é mais o storm nem a banda:
  medido hoje, 131 → 339 reports/s).
- **Debounce no PS**, e em qualquer atalho que abra programa.
- **`wmctrl` ausente tem de aparecer para ela.**

**A hipótese que sobrou de pé para o travamento da ponte** (grau: `incerto`, e
com endereço): dois escritores para um contador. O log mostra a ponte mandando
`seq=1`, começando do zero, enquanto o daemon mantém a própria sequência por
handle. E `held_ms` de **17 ms**, três vezes seguidas — mão nenhuma faz isso;
17 ms é o intervalo entre reports a ~60 Hz. Ninguém mediu a sequência dos dois
lados no mesmo instante.

---

## 5. As três regras que este dia acrescentou à metodologia

### 5.1. Um ensaio mede UM gesto

Pedi *"gire o controle E passe o dedo no touchpad"* ao mesmo tempo. O touchpad
saiu `0/8 bytes variam`, e eu quase escrevi que o produto não preenchia o
touchpad no report HID. **Com o gesto isolado, os bytes 33–36 variam
normalmente.**

Gesto composto produz **ausência falsa**. A casa já exigia uma variável por vez
no ESTADO; passa a exigir também no GESTO que se pede a ela. Vale na bancada
inteira: um controle só, distância curta, o resto removido — que foi como ela
montou hoje, por conta própria.

### 5.2. Instrumento que ESCREVE ou toma posse de recurso não é instrumento

Subi a ponte do mic **à mão**, no meio da bancada, só para colher um número de
banda. Três minutos depois o botão PS estava preso, o daemon abria a Steam em
laço, e ela desligou o controle com medo:

> *"tive que desligar o controler pq o teclado, o mouse (…) foi muito mas muito
> estranho"*

**A régua virou o defeito.** É a armadilha nº 3 desta casa, agora entre dois
pedaços do próprio produto.

Pior: **a casa tinha o aviso escrito** — no comentário do MIC-BT-01, em
`app/widgets/controller_card.py`, dizendo que a ponte disputa o contador de
sequência do `0x32` com o driver. Eu subi assim mesmo, **duas vezes**. Um aviso
que mora só no comentário de um widget não alcança quem está mexendo no módulo
de integração três diretórios adiante.

> **A regra:** instrumento que escreve ou toma posse só entra com o mesmo
> cuidado de uma cura — uma variável por vez, e com o caminho de volta pronto
> ANTES.

### 5.3. Erro dela também se corrige — deferência excessiva é não ajudar

**Grau: `decisão de método`, vinda da conversa da bancada, não de medição.**
Registro aqui porque sem ela as duas de cima não bastam.

A observação dela é fonte primária nesta casa, e continua sendo. Isso **não** é
o mesmo que aceitar o enquadramento dela sem conferir. Dois casos de hoje:

- **Os três jogos como um caso só.** DON'T SCREAM, Pragmata e Duskfade estavam
  no mesmo balde. A medição separou: os dois primeiros são o defeito 1;
  **Duskfade nunca funcionou em transporte nenhum** e em 16/08 deu os primeiros
  inputs da vida dele. Para ele o defeito 1 era agravante, não causa. Tratar os
  três juntos teria escondido o caso 7.
- **O `Soltar` → `Liberar`.** Ela pediu no bloco do microfone. Fazer **só** o
  que foi pedido deixaria dois botões com a mesma função e nomes diferentes na
  mesma tela — trocar um problema por outro. Mudou nos dois.

O critério que separa isto de desobedecer: **corrigir enquadramento e nomeação;
nunca reverter medição dela.** A memória dela sobre o som do alto-falante no
rádio (PONTO-A-PONTO §3) é o exemplo do outro lado — é observação, entra como
`medido` e derruba o `inferido-do-codigo` que está no mapa hoje.

---

## 6. Os três erros de instrumento do dia

Três vezes a régua mentiu **antes** do produto, e as três custaram tempo. Não
estão escondidos de propósito.

| # | o erro | o que ensinou |
|---|---|---|
| 1 | **`quem_o_jogo_abre.py` respondia "o WRAPPER rodou? NÃO"** para os dois jogos. Lia o environ do `reaper` da Steam, que roda ANTES do wrapper; o `/proc` do processo do jogo tinha a variável | *Um instrumento que acusa a própria cura de não existir manda a investigação para o lugar mais caro possível.* Corrigido por critério **estrutural** (o processo mais fundo que casa com o padrão) — nunca por conteúdo, que seria o instrumento confirmando a si mesmo |
| 2 | **Comparei o wrapper sem desescapar o VDF** e vi "0 jogos com wrapper" onde havia **62** | Formato antes de veredito |
| 3 | **Usei `parece_infraestrutura` achando que filtrava jogos** — ela filtra executáveis | Ler o contrato da função antes de usar o resultado dela |

Nas três, conferir o contrato antes de acusar o código foi o que evitou um
diagnóstico falso. **É barato conferir e caro acusar errado.**

Os outros dois tropeços do dia não estão nesta tabela porque viraram regra:
o gesto composto (§5.1) e a ponte do mic (§5.2).

---

## 7. Antes da bancada — a madrugada de 16/08

Quinze commits entre 01h18 e 06h19, de outra leva, que **nenhum índice citava**.
Ficam aqui para não se perderem; cada um tem o próprio documento.

| commit | o quê |
|---|---|
| `4de4762` | a sentinela do wrapper, e a carona nos cinco gestos que salvam perfil |
| `045d3d0` | o censo lia o bloco `apps` que a Steam não lê, e dava o Pragmata por são |
| `912617a` | o vigia da Steam repõe o wrapper sozinho |
| `7dd6292` | o prontuário por jogo, que recusa dizer "funciona" |
| `dca7170` | sai o contador do doctor que dizia 76 onde havia 63 |
| `a7cffe9` | o escritor cru da lightbar, e o terreno dos três modos de som |
| `60b95ce` | o `LEIA-PRIMEIRO` das specs, o mapa atualizado, e o alvo dela em sprint |

Os documentos: [O WRAPPER QUE SUMIU](2026-08-16-O-WRAPPER-QUE-SUMIU-01-uma-variavel-nova-apaga-a-ponte-em-silencio.md),
[SENTINELA WRAPPER](2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md),
[A MÁSCARA QUE O PRODUTO ESCOLHE](2026-08-16-A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01-o-jogo-nao-enxerga-e-a-culpa-nao-e-da-pessoa.md),
[TRÊS MODOS DO SOM](2026-08-16-TRES-MODOS-DO-SOM-01-o-que-sai-onde-e-quem-escolhe.md),
[A CADEIA DE BLOCOS](2026-08-16-A-CADEIA-DE-BLOCOS-01-o-ensaio-de-quatro-minutos-que-decide-o-som-por-radio.md),
[ESCRITOR CRU](2026-08-16-ESCRITOR-CRU-01-a-steam-apaga-a-barra-e-o-produto-nao-reagia.md),
[E5 O TERRENO](2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md),
[JOGÁVEL EM TODOS](2026-08-16-JOGAVEL-EM-TODOS-01-o-alvo-dela-e-cada-jogo-nos-dois-transportes.md),
[A ÁRVORE ERRADA](../estudos/2026-08-16-A-ARVORE-ERRADA-o-portao-que-olhava-para-o-lugar-errado.md),
[A LINHA QUE A STEAM COME](../estudos/2026-08-16-A-LINHA-QUE-A-STEAM-COME-o-censo-dos-campos-e-a-arvore-errada.md),
[O QUE A STEAM COME EM SILÊNCIO](../estudos/2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md),
[A MÁSCARA QUE O DISCO NÃO SABE](../estudos/2026-08-16-A-MASCARA-QUE-O-DISCO-NAO-SABE-o-censo-que-derrubou-a-deteccao-por-engine.md).

---

## 8. O agravante que atravessa o dia

Três portões desta casa passaram **verdes com o defeito vivo**: o contador do
wrapper, a árvore errada do VDF e o `hidden_count` do broker. E o portão que
faltava — o do ciclo conecta-cai-reconecta — só nasceu hoje, depois do defeito.

> **Um portão que olha para o lugar errado é pior que portão nenhum, porque
> encerra a busca.**

Por isso a preocupação dela — *"me preocupa o fato de serem regressões e me
preocupa o fato de que isso possa voltar no futuro"* — é a régua de todo item
da §4: **só fecha com teste que morde.** Arranque a cura, veja reprovar,
devolva.
