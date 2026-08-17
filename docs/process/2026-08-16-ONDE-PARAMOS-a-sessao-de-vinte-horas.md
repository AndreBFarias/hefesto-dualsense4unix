# ONDE PARAMOS — a sessão de vinte horas

- **Escrito em:** 16/08/2026, no fim do dia, na branch `restauro/inicio-da-sessao`.
- **O que esta página é:** a **porta de entrada**. Ela sucede o
  [2026-08-11-ONDE-PARAMOS](2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md)
  — que é para onde o `CLAUDE.md` da raiz ainda aponta, na linha 11 — e também o
  [2026-08-15-ONDE-PARAMOS](2026-08-15-ONDE-PARAMOS-a-manha-que-abriu-a-porta.md),
  que já tinha se declarado sucessor do de 11/08 e **também** não foi apontado.
  **Ação de um minuto para quem chegar:** repontar a linha 11 do `CLAUDE.md`
  para esta página. Os dois anteriores continuam válidos para o que mediram;
  só deixaram de ser o retrato de hoje.
- **O que ela pediu, textual:** *"não quero que nada se perca aqui"*.
- **O que este dia foi:** **33 commits** entre 01h18 e 23h52, em três levas —
  a madrugada (01h18–06h19, 20 commits), a **bancada com o aparelho na mão dela**
  (19h36–21h26, cinco commits) e o fecho da noite (22h57–23h52, três commits).
- **Grau desta página:** compilação. **Nada aqui foi medido por esta passagem.**
  Nenhum `/dev/hidraw` foi aberto, o daemon não foi reiniciado, o `doctor.sh` não
  rodou, o áudio não foi tocado e a Steam não foi aberta. Cada afirmação carrega
  o endereço do documento, do commit ou do arquivo onde ela foi medida.

**Se você tem cinco minutos:** leia a §1 (o que está quebrado agora) e a §5 (as
três regras novas de método). Se tem quinze, some a §3 — os quinze suspeitos
eliminados são becos que ninguém precisa percorrer de novo.

**Os três índices do dia, e tudo aqui aponta para um deles:**

- [ÍNDICE — a bancada de oito horas](sprints/2026-08-16-INDICE-a-bancada-de-oito-horas.md)
  — registro de execução da bancada, com a madrugada na §7.
- [O QUE FICOU ABERTO-01](sprints/2026-08-16-O-QUE-FICOU-ABERTO-01-e-como-cada-um-fecha.md)
  — oito frentes abertas, cada uma com **como o portão vai morder** quando fechar.
- [PONTO A PONTO-01](sprints/2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md)
  — a lista dela em sete pontos, na ordem do que custa mais por dia.

---

## 1. O que está QUEBRADO agora, na máquina dela

Comece por aqui. É o que importa às 6h da manhã.

### 1.1 A reconexão BT mata a entrada — P0, reproduzido, SEM cura

**É o defeito que estragou a sessão dela e mandou horas de investigação para o
lugar errado.** O controle cai e volta no rádio (ou sai do cabo para o rádio) e o
daemon **nunca reabre os leitores**. O log de 19:15:29 a 19:15:30, e depois disso
nada:

```
evdev_read_lost            errno 19   event25
motion_reader_open_failed  errno 2    /dev/hidraw5
controller_disconnected    reason=probe_offline
```

**A mentira é o detalhe caro.** O vpad segue emitindo — 396 reports em 8 s, ID
`0x01`, 64 bytes, sequência perfeita, **`LX` travado em 128**. Para o jogo é um
controle vivo que nunca se mexe: daí *"recebeu um pouco de input e morreu"*, em
três jogos.

- **Cura de hoje, e ela funciona:** `systemctl --user restart hefesto-dualsense4unix`.
  Verificado — o input volta na hora.
- **Estado:** reproduzido ponta a ponta. **Cura de produto não existe.**
- **Os ganchos que já existem e hoje só avisam:** `evdev_read_lost`
  (`core/evdev_reader.py:1116`) é logado **sem tratador nenhum**; e
  `state_stale_neutral_warning` (`daemon/ipc_handlers.py:2142`) já sabe dizer que
  estagnou — **sete linhas abaixo, em `:2149`, o mesmo dicionário publica
  `"connected": True`**. O aviso e a mentira saem do mesmo payload.
- **Ressalva que a próxima cura precisa carregar:** esse aviso **não é watchdog**.
  Ele nasce dentro do handler do IPC e conta *chamadas de `daemon.state_full`*,
  com limiar 3. Com a janela fechada ninguém chama, ninguém conta, e o daemon
  estagna em silêncio absoluto.
- **Fonte:** [O RÁDIO MEIO MUDO](estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md),
  "DEFEITO 1"; plano em [O QUE FICOU ABERTO-01](sprints/2026-08-16-O-QUE-FICOU-ABERTO-01-e-como-cada-um-fecha.md) §1.

### 1.2 No rádio, metade do controle não atravessa — P1, sem causa

Medido com a mão dela, depois de curado o 1.1 (input voltou, jogo respondendo):

| canal | rádio |
|---|---|
| lightbar (cor do perfil) | **funciona** |
| LED do número do jogador | **funciona** |
| gatilhos adaptativos | falha |
| vibração | falha (zero) |
| som no controle | falha |
| touchpad | falha (funciona **fora** do jogo) |
| giroscópio / mira por movimento | falha (**no cabo a mira responde**) |

**E o repasse do vpad foi medido e está ÍNTEGRO** — ver §3. A causa não está no
que o vpad entrega.

**O que fecha de graça quando o 1.1 fechar:** DON'T SCREAM e **Big Walk** usam
mic, giroscópio e touch, e ela registrou que *"ambos os jogos funcionavam via bt
com gatilho adaptativo e beleza"*. Retestar os dois **logo depois** do 1.1, antes
de abrir investigação nova. Custo: um reteste, zero de investigação.

### 1.3 O vpad pode nascer morto, e o daemon diz que está ótimo — P1

Medido às 13:42:42, durante o autoswitch com o jogo subindo:

```
0003:054C:0DF2.0038   driver: NENHUM   input: NENHUM   hidraw: NENHUM
```

O uhid foi criado e o `hid_playstation` nunca o adotou. Recriar (toggle da
emulação) resolveu — logo é **corrida**, não defeito permanente. O daemon
reportava `{"enabled": true, "degraded": false}` sobre um dispositivo sem driver.
`wait_for_bind()` existe (`integrations/uhid_gamepad.py:1883`) e **não segurou**;
ninguém sabe por quê.

### 1.4 O PS preso vira laço de spawn, sem freio nenhum — P0

Estado: **o gatilho conhecido está desligado** (a ponte do mic, §1.5), mas a
**ausência de freio continua armada** para qualquer gatilho futuro.

O caminho é `daemon/subsystems/hotkey.py` → `open_or_focus_steam()`, disparado
no release do PS por `integrations/hotkey_daemon.py:220-224`. Entre o release e o
`Popen` da Steam **não há debounce, não há teto de tentativas, não há "já pedi
isto há 200 ms"**.

Medido em 16/08 às 21:05: `held_ms` de **17,6 / 17,5 / 17,9 ms** em sequência.
Mão nenhuma faz isso — 17 ms é o intervalo entre reports a ~60 Hz. O botão
apareceu pressionado por exatamente um ciclo de leitura, repetidamente.

Foi isto que ela viu, e é a razão de a sessão ter parado:

> *"tive que desligar o controler pq o teclado, o mouse (tava teclando sem parar
> e o botão direito do mouse também), cara, foi muito mas muito estranho,
> desliguei o controle e parou fiquei com medo"*

**Não era storm e não era o teclado** — a emulação de mouse/teclado do daemon
estava desligada e foi medida assim (`mouse_emulation.enabled=false`,
`keyboard_emulation.despachando=false`).

### 1.5 A ponte do mic BT não é segura — decidido hoje, e ela NÃO sobe

- **Estado atual:** ponte parada, módulo do PipeWire descarregado,
  `bt_mic: enabled=false`, nenhum source `hefesto_dualsense` no sistema.
- **Risco por dia: zero.** A ponte é opt-in por `HEFESTO_DUALSENSE4UNIX_BT_MIC=1`
  ou por `DaemonConfig.bt_mic_enabled` (`daemon/subsystems/bt_mic.py:23,49`), e
  esse campo **não tem escritor em lugar nenhum de `src/`** — a janela não a liga.
  Ela subiu hoje porque **eu** a subi à mão, duas vezes.
- **O veredito, e o método foi dela** (*"testar primeiro, decidir depois"*):
  **testado — não sobe.** A ponte não volta ao caminho automático da interface
  enquanto a sequência do report `0x32` tiver dois donos.
- **O interruptor "Pelo rádio" saiu da janela** no commit `1e96db5`. A
  **capacidade** fica inteira (o módulo, o subsystem, o `mic bt` do CLI, o gate);
  o que saiu é o botão, e ficou escrito no lugar dele como ele volta.
- **Fonte:** [O PS PRESO](estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md).

### 1.6 `wmctrl` ausente transforma "focar" em "abrir" — P0, e custa todo dia

`integrations/steam_launcher.py:83`: sem o binário sai `wmctrl_binary_not_found`,
um `warning` que ela nunca vê; o `_focus_steam_window` devolve `False` e cai no
`_spawn_steam`. **Com a Steam já aberta, cada toque do PS pede um processo novo
em vez de trazer a janela para frente.**

Verificado por leitura: o `wmctrl` **não está no `PATH`** desta máquina, e não
aparece no `install.sh`, no `scripts/doctor.sh` nem no empacotamento. **O produto
depende de um binário que ele nunca pede.**

**A ressalva que impede a cura errada** (grau: `inferido-do-codigo` mais leitura
do ambiente): esta sessão é `XDG_SESSION_TYPE=wayland`, `XDG_CURRENT_DESKTOP=COSMIC`,
com Xwayland em `:1`. O `wmctrl` é ferramenta **X11**. Se a Steam sob Xwayland é
alcançável por ele é **`incerto`, ninguém mediu**. *"Basta declarar a
dependência"* pode ser falso nesta máquina.

### 1.7 Três portões passam VERDES com o defeito vivo

| portão | onde | o que ele diz de errado |
|---|---|---|
| `hidden_count` do broker | `scripts/doctor.sh:3109` imprime `len(hidden)`; o veredito em `:3245-3251` é `hidden_count > 0` | com dois DualSense e o broker escondendo **um**: `1 > 0`, verde, texto *"o jogo só vê o vpad"* — e o P2 vê dois controles |
| `check_bt_bonds_persistidos` | `scripts/doctor.sh:2827-2842`, passa com `n_info > 0` | quatro controles, um bond evaporado: `3 > 0`, verde, e imprime *"bonds BT persistidos em disco: 3"* — **a prova do defeito dentro da frase de aprovação** |
| o contador de jogos com wrapper | curado hoje, `dca7170` | dizia **76** onde havia **63**, somando as três árvores do vdf |

> **Um portão que olha para o lugar errado é pior que portão nenhum, porque
> encerra a busca.**

E o portão que **faltava** — o do ciclo conecta-cai-reconecta — só nasceu hoje,
depois do defeito. É por isso que a preocupação dela é descrição correta do
estado, não receio:

> *"me preocupa o fato de serem regressões e me preocupa o fato de que isso possa
> voltar no futuro."*

### 1.8 Pela metade, e em que estado exatamente

| item | estado | o que falta para fechar |
|---|---|---|
| **O reparo do Pragmata** | o wrapper foi reposto às 03:33 **com a Steam aberta**, e o reparo **jogou fora o `VKD3D_CONFIG=no_upload_hvv`** — a cura do crash de 14/08 sumiu da linha. A Steam regrava o `localconfig.vdf` ao sair, então esse reparo tende a ser desfeito | fechar a Steam; o guard repõe sozinho, agora preservando a linha dela |
| **As 11 linhas nas árvores secundárias do vdf** | escritas por nós antes da âncora de caminho. Inócuas — a Steam não as lê | exige Steam fechada; `uninstall --strip` já as tira |
| **O áudio da bancada da noite** | a camada 1 curada, a camada 2 falhou no `--fix` e foi trocada à mão | §6 inteira |
| **A árvore de trabalho** | dois arquivos modificados e **não commitados**: `integrations/audio_control.py` e `tests/unit/test_mic_volume_01_o_slider_que_faltava.py` — **outra sessão estava editando os dois** | conferir com quem os editou antes de commitar |

---

## 2. O que foi CURADO hoje, com o commit

### 2.1 A bancada (19h36–21h26 e o fecho da noite)

| # | o defeito | o que a medição mostrou | commit | portão |
|---|---|---|---|---|
| 1 | **Áudio do mic lido como estado de botão.** Com a ponte de pé, o DualSense manda Opus no MESMO report `0x31`, 78 bytes, **CRC-32 válido**. Só o bit `0x02` do byte 1 separa áudio de input, e o `_struct_base` não o conferia: os bytes de Opus caíam sobre `buttons[2]`, onde moram MIC e PS | os reports contaminados prendiam MIC e PS | `702f5b6` | `tests/unit/test_ps_preso_01_audio_lido_como_botao.py` — arrancar o filtro reprova. Cura em `core/physical_report_reader.py:382`; a constante `INPUT_FLAG_AUDIO = 0x02` fica espelhada em `:143`, travada por teste contra o valor de `integrations/dualsense_bt_audio.py`, porque o caminho quente não pode importar `ctypes`/`libopus` |
| 2 | **Não havia portão do CICLO** conecta-cai-reconecta. Havia teste para a PERDA do fd e para o estado estático; nenhum para a **transição**, que é onde mora o defeito 1 | — (é portão, não cura) | `a053265` | `tests/unit/test_reconexao_bt_01_o_leitor_tem_de_voltar_sozinho.py` — 3 testes. **Passam contra o código de hoje**, e é esse o resultado: eliminam o `EvdevReader` (§3) |
| 3 | **`quem_o_jogo_abre.py` acusava a própria cura de não existir** — lia o environ do **primeiro** processo da árvore, o `reaper` da Steam, que roda ANTES do wrapper | o `/proc` do processo do jogo tinha a variável o tempo todo | `adf53bb` | **não há portão.** A correção é o critério **estrutural** (o processo mais fundo que casa com o padrão), nunca por conteúdo — que seria o instrumento confirmando a si mesmo |
| 4 | **O microfone não tinha volume nem mudo no perfil**, só um booleano; o alto-falante tinha os dois. A assimetria aparecia na tela | — (pedido dela) | `66b3057` | `tests/unit/test_mic_button_exposto.py`. `ProfileMicConfig` ganha `volume` (0–100) e `muted`, os dois opcionais, `None` = sem opinião |
| 5 | **`Soltar` virou `Liberar`**, nos DOIS blocos — mic e alto-falante. Ela pediu só no do microfone; fazer só o pedido deixaria dois botões com a mesma função e nomes diferentes na mesma tela | — | `66b3057` | dois testes que travavam texto literal foram reancorados na constante |
| 6 | **O microfone ganhou o controle deslizante de volume**, e o interruptor "Pelo rádio" saiu da janela | a geometria confirmou o desenho dela: acrescentar sem tirar levava a coluna do som a **292px de 258 de teto**; substituir custa zero, e tirar o interruptor devolveu a aba de **1236 para 1140px** (teto 1180) e o card de **595 para 505** (teto 590) | `1e96db5` | `tests/unit/test_mic_volume_01_o_slider_que_faltava.py`. Cadeia nova inteira: `mic.volume.set` no IPC → `audio_control` → o source no PipeWire |
| 7 | **Não havia instrumento que parasse físico e virtual campo a campo** | primeira passada, sem gesto, 3 s: giroscópio **302 → 244 (81%)**, acelerômetro **748 → 481 (64%)**. Não é perda total, é **achatamento** — e é a primeira vez que a diferença tem nome | `a34dca4` | é instrumento, não produto. `scripts/ensaios/espelho_fiel.py`: janelas **simultâneas** (threads), **recusa** comparar se um dos lados não entregou nada, e **pede UM gesto por vez, dizendo qual** |

**Volume do mic é do CAMINHO, não do firmware.** É o *source* do sistema, por
isso vale igual no cabo e no rádio — que é o *"independente de saber se tá via bt
ou via cabo"* do pedido dela. O DualSense **não expõe ganho de captura** em
transporte nenhum; o que existe no firmware é o mudo, e quem fala com ele é o
`muted`. Sem fonte (rádio sem a ponte), o daemon responde `sem_fonte` e o
controle fica insensível — um controle que aceita o gesto e não faz nada é a tela
mentindo.

### 2.2 A madrugada (01h18–06h19)

Vinte commits que **nenhum índice citava** até a §7 do
[ÍNDICE](sprints/2026-08-16-INDICE-a-bancada-de-oito-horas.md).

| o defeito | o que a medição mostrou | commit | portão |
|---|---|---|---|
| **A Steam comeu a linha do wrapper do Pragmata.** A Steam guarda **UMA** linha de Opções de Inicialização por jogo; o `VKD3D_CONFIG=no_upload_hvv %command%` posto para curar o crash de 14/08 **substituiu** o `hefesto-launch` | 60 jogos com o wrapper, **1 sem** — o Pragmata. Cadeia medida no `/proc` do jogo vivo: sem wrapper, `PROTON_DISABLE_HIDRAW` zerado; o `SDL_GAMECONTROLLER_IGNORE_DEVICES` que chegou era o da própria Steam, e dentro dele está `0x054c/0x0df2` — **o PID do nosso vpad**. O jogo foi instruído a ignorar os dois | `4de4762`, `912617a` | `tests/unit/test_sentinela_do_wrapper_01_a_steam_comeu_o_hefesto_launch.py` — 18 testes, quatro curas arrancadas e quatro reprovações medidas |
| **O censo lia a árvore `apps` que a Steam não lê** e dava o Pragmata por são | `censo_do_wrapper()` passou de `faltantes: 0` para `SEM wrapper (regressao): PRAGMATA` | `045d3d0` | `tests/unit/test_arvore_errada_01_*.py` — 18 testes, a âncora `e_a_arvore_canonica()` nos dois lados (leitor e escritor) |
| **`pastas_steamapps()` devolvia a mesma pasta duas vezes** (`~/.steam/steam` é link para `~/.steam/debian-installation`; a comparação era por texto de caminho) | o primeiro consumidor novo imprimiu **65 jogos instalados** onde há 33 manifests | `045d3d0` | `tests/unit/test_biblioteca_dobrada_01_*.py` — 9 testes. Curado **na fonte**: quem chama não pode precisar saber que a fonte repete |
| **Nada repunha o wrapper na janela em que ela está jogando** | o `hefesto-steam-input-guard.path` já vigiava `~/.steam/steam/userdata` e acorda no instante em que a Steam grava o vdf — isto é, quando ela **acabou de sair**. Verificado ao vivo às 05h52 (adiando, Steam aberta) e às 06h05 (disparando) | `912617a` | `tests/unit/test_carona_no_guard_01_*.py` — 10 testes, o `ExecStart` que não pode sumir. Sem unidade nova, sem timer novo, **sem botão** — desenho dela |
| **O contador do doctor dizia 76 onde havia 63**, e nunca dizia quem faltava | somava as três árvores do vdf | `dca7170` | quem dá o veredito agora **nomeia** |
| **Não havia prontuário por jogo** | Duskfade e DON'T SCREAM têm a **mesma** assinatura em disco — mesmo motor, mesmas famílias de API, mesmo wrapper, mesmo Steam Input desligado. Um funciona e o outro não | `7dd6292` | `tests/unit/test_prontuario_01_*.py` — 28 testes, inclusive o que trava que os dois saiam iguais. O balde bom se chama `sem_impedimento_conhecido`: o prontuário **recusa dizer "funciona"** |
| **A Steam apaga a lightbar, e o produto não reagia.** A hipótese é dela: *"não é pq a steam tá aberta?"* | par de eliminação completo, feito por ela: COM a Steam a barra fica **apagada** depois de cada comando nosso; SEM a Steam volta ao **verde sozinha**. A Steam segurava os **oito** `hidraw`; o daemon não reagiu em 60 s; `lightbar_escritor_estrangeiro` deu **ZERO em três horas**; e o `sysfs` leu `[0 255 0]` com a barra **apagada** e com ela **verde** | `a7cffe9`, `8e44f86` | `core/escritor_cru.py` (novo) e `test_a_classe_led_nao_ve_o_escritor_cru`. Detecção por **quem segura o nó** (`/proc/<pid>/fd`, ~6 ms para ~4600 fds, sem root, sem tocar o aparelho) |
| **O alto-falante ficava mudo porque ninguém tomava a posse do volume no firmware** | dose-resposta com a orelha dela: nunca escrito = mudo · 85 = soa · 0 = mudo | `efd1c03`, `ac705e0` | `VOLUME_PADRAO_DO_SOM` em `core/backend_pydualsense.py`, tomado na adoção. E o drop-in 54 (`--nunca-dorme`) entra **sem flag, em todo formato** do `install.sh` |
| **O nó suspenso come o começo do som** | medido na orelha dela em 15/08 23h45: com o nó SUSPENSO, o primeiro som depois do silêncio se perde no religar do hardware. O bipe da interface tem **67 ms** — o começo comido é o som inteiro | `ac705e0` | `tests/unit/test_o_alto_falante_nunca_dorme_01.py` |
| **O estado publicado não dizia QUAL controle alimenta qual vpad**, e a placa de som não estava casada com o controle | o casamento é pelo **dispositivo USB pai** — não por MAC, não por nome, não por ordem de enumeração. Em 16/08 00h08, dois controles no cabo, dois timbres ao mesmo tempo, cada um no seu, **sem vazar** | `147bcb0`, `c66f9c9`, `a725371` | `tests/unit/test_a_placa_e_o_controle_pelo_usb_pai.py`, que trava inclusive o caso cruzado |
| **A régua do giroscópio errava por 62x**, e o contador de perda ficava cego justamente no rádio | — | `446a326` | é instrumento |
| **O eixo parado desde antes do `open` chegava ao jogo como centro perfeito** | o A-1 mediu o repouso dos quatro sticks; o repouso é **impressão digital da unidade** | `19b47bf`, `4ed9137` | — |
| **O portão de anonimato não sabia o que é um serial de fábrica**, e um vazou pela própria função que mascara serial | — | `3f8c66d` | o próprio portão, corrigido |
| **A suíte escrevia no journal DELA** a morte de um `bluetoothd` que estava vivo | — | `b3d13ff` | — |
| **A cor por rádio:** a segunda rodada do E7 leva de 2 de 2 para **4 de 4**, e o rádio **recusa com EIO** | — | `4ae4826` | `docs/data/ensaios.csv` |
| **A cabeça do `0x32` é TLV**, e o `common` de 47 bytes está **refutado nos dois braços** | E-1 com o próprio microfone como sensor, bit `report[55] & 0x04` como veredito, em duas unidades do rádio | `3f2786c`, `98d3c96` | o caderno — **177 ensaios** em `docs/data/ensaios.csv` (`caab87a`) |

---

## 3. O que foi ELIMINADO como suspeito

**Isto vale tanto quanto as curas.** São becos que ninguém precisa percorrer de
novo. **Não repita nenhum destes.**

### 3.1 Os onze do defeito da reconexão

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

### 3.2 Os quatro que caíram depois

| suspeito | como caiu | grau |
|---|---|---|
| **os `VALID_FLAG*` / "o vpad está meio mudo"** | duas réguas independentes: giro **7 231** no vpad contra **19 435** no físico; touchpad **2 807** contra **3 660**; e no report de 64 bytes do `hidraw4` variam os bytes `2,3` · `7` · `16–27` · `28–32` · `33–36`. **O vpad entrega tudo, pelos dois caminhos** | medido |
| **o `EvdevReader` como culpado da reconexão** | os 3 testes do ciclo (`a053265`) **passam** contra o código de hoje: ele reabre no nó novo, não insiste no número velho, sobrevive a sumiço prolongado. O `_locate` procura por IDENTIDADE, e segura | medido, **com portão permanente** |
| **os bytes de Opus como causa do travamento da ponte** — a hipótese do Opus sobre `buttons[2]` | com o filtro do bit de áudio já no daemon (reiniciado às 21:04 — conferido, porque o daemon de antes rodava o código velho), a ponte travou **em 10 segundos**, igual, 10 disparos. **O filtro está no lugar e o defeito voltou igual.** O report contaminado **não** é de áudio: é um report de input legítimo com o byte de botões errado. **O filtro continua certo e fica** — áudio lido como input é defeito com ou sem este travamento; ele só não era esta causa | medido |
| a emulação de mouse/teclado do daemon no episódio do PS | `mouse_emulation.enabled=false`, `keyboard_emulation.despachando=false` | medido |

### 3.3 O par que fechou o dia

O ensaio mais limpo: mesma sessão do jogo (não reabriu), **mesmo vpad** (`003C`
dos dois lados, não recriado), mesmo daemon (não reiniciou), **única variável
cabo → rádio**.

> **Funciona no cabo. Para no rádio. Uma variável, um veredito.**

### 3.4 E a separação dos três jogos, que reorientou o dia inteiro

A frase dela:

> *"a falha não pode ser o jogo. (…) o dont scream e o pragmata funcionavam no
> rádio, o duskfade que nunca funcionou no cabo e no radio teve input que
> funcionou."*

A medição confirmou e **separou três casos que estavam sendo tratados como um**:

- **DON'T SCREAM e Pragmata** — funcionavam no rádio e pararam. O defeito 1
  explica inteiro.
- **Duskfade** — caso próprio. **Nunca funcionou em transporte nenhum**, e em
  16/08 deu os primeiros inputs da vida dele. Para ele o defeito 1 era agravante,
  não causa. **A causa não está no disco** (mesma assinatura do DON'T SCREAM);
  está em tempo de execução.

---

## 4. O que continua ABERTO, e de quem é a decisão

O plano completo, com **como o portão morde** em cada frente, é
[O QUE FICOU ABERTO-01](sprints/2026-08-16-O-QUE-FICOU-ABERTO-01-e-como-cada-um-fecha.md).
Aqui vai só o mapa e a separação que importa.

### 4.1 Trabalho de código — ninguém precisa decidir nada

| # | frente | endereço do próximo fio |
|---|---|---|
| 1 | **A reconexão BT** (§1.1) | três fios, e o mais informativo é `primary_grab_state=pending`: em `core/evdev_reader.py:1203` e `:1250` esse estado significa literalmente *"pedido, device ainda não aberto"*. Ou seja, o estado que ela viu ao vivo afirma que **não havia device de evdev aberto** — e isso aponta para a **descoberta** (`find_dualsense_evdev`, `core/evdev_reader.py:404`), não para o laço de reabertura. Grau: `inferido-do-codigo`. Os outros dois: o `motion_reader` com o broker no meio (`core/physical_report_reader.py:759` e o laço a partir de `:744`) e `controller_disconnected reason=probe_offline` (`daemon/connection.py:546-551`) |
| 2 | **O freio do PS** (§1.4) | debounce em `daemon/subsystems/hotkey.py` / `integrations/hotkey_daemon.py`, com relógio injetado, nunca `sleep` real |
| 3 | **Os dois portões cegos** (§1.7) | trocar `len(hidden)` pela **lista** e o veredito por comparação com o censo de físicos (`broker/hidraw_broker.py`, `validate_physical_node`); e nomear os MACs com `cache/` **sem** `info/`. Ressalva obrigatória: o resultado sai na tela dela e **nunca** em arquivo versionado — se um dia for, vale a máscara da casa (octetos 4 e 5 zerados), e há portão que reprova |
| 4 | **Arbitrar o hidraw** entre a ponte do mic e o `motion_reader` | os dois abrem `/dev/hidraw5` sem se conhecerem. O broker já é o dono da posse (`integrations/hidraw_broker_client.py`): é ele que tem de **recusar ou multiplexar** o segundo pedido. **A ponte não volta a subir sem isto** — decisão do dia, e a razão é nova: não é mais o storm nem a banda (medido hoje, 131 → 339 reports/s) |
| 5 | **Por que o `wait_for_bind` não segurou** o vpad natimorto (§1.3) | `integrations/uhid_gamepad.py:1883` |
| 6 | **O `wmctrl`** (§1.6) | **medir antes de empacotar** — ver a ressalva Wayland/COSMIC |

### 4.2 Decisão DELA — não decido por ela

| # | a decisão | o que está na mesa |
|---|---|---|
| **D-a** | **O que a janela mostra quando o estado está degradado.** Hoje ela mostra "conectado" | as opções vão de um selo no cartão do controle até **recusar** o "conectado". É a regra do olho dela (PROVA-DE-TELA-01): não fecha sem foto e sem a palavra dela |
| **D-b** | **O `wmctrl` ausente tem de aparecer para ela** — onde e com que texto. E, maior: se a resposta certa é **declarar a dependência** ou **trocar o mecanismo** por um que fale com o COSMIC | a segunda é mais cara e é a única que sobrevive a um desktop Wayland puro |
| **D-c** | **O alto-falante no rádio: o grau contra a memória dela.** Ela: *"a minha certeza do lance do som no bt do speaker do dualsense, o claude tinha feito funcionar quando testávamos no pragmata"*. O `docs/data/mapa-controles.csv` diz `inferido-do-codigo` nas três linhas de áudio | **a orelha dela é a régua.** O ensaio custa **4 minutos**: repetir no rádio o par que isolou a causa no cabo — mudo, `volume 85`, `volume 0`. Os dois desfechos são vitória: promove a célula para `medido`, **ou** registra que a memória caducou, com data. O empate é o único que não vale nada |
| **D-d** | **Se vale gastar bancada para destravar a ponte do mic.** É uma feature que ela quer, e o preço agora está na mesa | ver §1.5 |
| **D-e** | **Quanto vale o instrumento que pareia físico × virtual.** A ideia é dela; o custo é meu de estimar e dela de aprovar | o `espelho_fiel.py` já existe (`a34dca4`) e deu 81% no giro e 64% no acelerômetro. Falta decidir se vira régua com limiar. **Aviso que a decisão precisa carregar:** ele **lê** dos dois lados e não escreve — é instrumento de verdade pela regra da §5.2 —, mas disputa leitura de nós que o produto está lendo, e é o suspeito nº 1 do touchpad engasgando |
| **D-f** | **Duskfade — a prioridade.** É um jogo, contra frentes que afetam todos | a recomendação é rodar o par com o DON'T SCREAM **depois** do item 1 curado, mesma bancada |
| **D-g** | **O Sackboy na allowlist inerte.** Ele está na allowlist do Steam Input com `UseSteamControllerConfig = 0`. A allowlist só **preserva** o que já estava ligado — nunca liga. O gesto dela não teve efeito | daqui não dá para distinguir *"a lista entrou tarde"* de *"eu desliguei depois e mudei de ideia"*. Pergunta de produto que vem junto: **a allowlist deveria LIGAR, e não só preservar?** Hoje o nome "lista de exceções" promete mais do que entrega |
| **D-h** | **As cinco perguntas dos três modos do som** (P-1 a P-5) | [TRÊS MODOS DO SOM-01](sprints/2026-08-16-TRES-MODOS-DO-SOM-01-o-que-sai-onde-e-quem-escolhe.md) §12. A que não depende de ninguém é a **ONDA 2** (o L+R) — ver §6.5 |
| **D-i** | **O E-7 roda?** 4 minutos de olho dela na lightbar, e ele decide se o E-5 (2h30 de máquina, 8 min dela) roda ou é cancelado | [A CADEIA DE BLOCOS-01](sprints/2026-08-16-A-CADEIA-DE-BLOCOS-01-o-ensaio-de-quatro-minutos-que-decide-o-som-por-radio.md) |

### 4.3 Aberto sem dono ainda — falta medir antes de decidir

- **O touchpad engasgando.** Relato dela: *"durante os testes notei que tava tipo
  engasgando. aí depois voltava."* É tudo o que existe. **Nenhuma medição.**
  **O primeiro suspeito sou eu:** durante a bancada abri `hidraw4`,
  `event21/22/23` e `event25-28` em laços não-bloqueantes com `sleep` de 2 a 4 ms.
  Não vale gastar bancada dela antes do item 1: se for o defeito da reconexão em
  versão branda, some junto.
- **Os 8 espelhos `28de:11ff` contra "zero espelhos".** A canônica de 11/08
  registrou **zero** com grau MEDIDO; em 16/08 de madrugada havia **oito**
  (`Microsoft X-Box 360 pad 0` a `7`). Com a Steam fechada: zero. E o
  `virtualgamepadinfo.txt` da Steam, escrito às 03:24, tem **dois** slots — e o
  **slot 0 é o NOSSO vpad** (`054c:0df2`). Descartado por medição que fosse
  atualização de cliente: o mesmo binário produziu as duas leituras. **O ensaio
  que decide é de um minuto** e está escrito em
  [A MÁSCARA QUE O PRODUTO ESCOLHE-01](sprints/2026-08-16-A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01-o-jogo-nao-enxerga-e-a-culpa-nao-e-da-pessoa.md) §6.
- **Quem alimenta o quê no rádio.** O estudo deixou aberto que o `motion_reader`
  cicla a cada 30 s em silêncio e o giroscópio chega ao vpad assim mesmo. **A
  leitura de que existiriam "dois caminhos" está errada** (grau:
  `inferido-do-codigo`): o giroscópio do vpad tem **uma fonte só**, o
  `PhysicalReportReader`; os leitores de `daemon/sensor_hub.py` alimentam **só** o
  painel do `state_full`, nascem sob demanda e morrem 5 s depois. As duas
  medições são de momentos diferentes. A régua que resolve é o `espelho_fiel.py`.
- **A hipótese que sobrou de pé para o travamento da ponte** (grau: `incerto`,
  com endereço): dois escritores para um contador. A ponte manda `seq=1`,
  começando do zero (`integrations/dualsense_bt_audio.py`), enquanto o daemon
  mantém a própria sequência por handle. **E a árvore contém duas afirmações
  contraditórias sobre isso** — o cabeçalho de `dualsense_bt_audio.py` argumenta
  que a disputa é estruturalmente mitigada; o comentário do MIC-BT-01 em
  `app/widgets/controller_card.py` diz o oposto. **Nenhuma foi medida com a
  sequência dos dois lados no mesmo instante**, e o travamento é o dado que o
  argumento do cabeçalho não explica.
- **`SDL_GamepadBind` no `config.vdf`** — ponto cego total. Ninguém no projeto
  sabia que o campo existe, e o `.path` não o vigia. Ver
  [O QUE A STEAM COME EM SILÊNCIO](estudos/2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md) §3.1.

### 4.4 O placar honesto do alvo dela

O critério de pronto é dela, de 15/08: *"espero de fato que tenhamos tudo
resolvido e cada um dos jogos locais jogável via cabo ou bt."*

**24 jogos instalados.** Por API de entrada: `entende_dualsense` **7**,
`indeciso` **15**, `sem_evidencia` **2** — ou seja, **quinze dos vinte e quatro
dependem de um espelho XInput do nosso vpad**, o que muda o peso de tudo que se
decidir sobre Steam Input.

> **1 jogo confirmado quebrado (Duskfade), 1 se consertando sozinho (Pragmata),
> 1 decisão dela (Sackboy), e 21 sem veredito porque ninguém jogou ainda.**

---

## 5. As armadilhas que este dia acrescentou

Três regras novas de metodologia nasceram hoje. **Elas valem mais que o código.**

### 5.1 Um ensaio mede UM gesto

Pedi *"gire o controle E passe o dedo no touchpad"* ao mesmo tempo. O touchpad
saiu `0/8 bytes variam`, e eu quase escrevi que o produto não preenchia o
touchpad no report HID. **Com o gesto isolado, os bytes 33–36 variam
normalmente.**

**Gesto composto produz ausência falsa.** A casa já exigia uma variável por vez
no ESTADO; passa a exigir também no GESTO que se pede a ela. Vale na bancada
inteira — um controle só, distância curta, o resto removido, que foi como ela
montou hoje, por conta própria:

> *"quer que eu teste no controle azul e deixe o vermelho carregando? eu to
> sentado no lado do bt, removi tudo que poderia bagunçar e to em cima do bt
> agora pra não dar pt por conta da distancia."*

A regra já está embutida no `espelho_fiel.py`, que **pede um gesto por vez e diz
qual**.

### 5.2 Instrumento que ESCREVE ou toma posse de recurso não é instrumento — é mudança de estado

Subi a ponte do mic **à mão**, no meio da bancada, só para colher um número de
banda. Três minutos depois o botão PS estava preso, o daemon abria a Steam em
laço, e ela desligou o controle com medo. **A régua virou o defeito.**

É a armadilha nº 3 desta casa (*o instrumento briga com o produto*), agora entre
dois pedaços do próprio produto.

**Pior: a casa TINHA o aviso escrito** — no comentário do MIC-BT-01, em
`app/widgets/controller_card.py`, dizendo que a ponte disputa o contador de
sequência do `0x32` com o driver. Eu subi assim mesmo, **duas vezes**. Um aviso
que mora só no comentário de um widget não alcança quem está mexendo no módulo de
integração três diretórios adiante. **O portão é o lugar onde um aviso desses
passa a alcançar.**

> **A regra:** instrumento que escreve ou toma posse só entra com o mesmo cuidado
> de uma cura — **uma variável por vez, e com o caminho de volta pronto ANTES.**

### 5.3 Erro dela também se corrige — deferência excessiva é não ajudar

**Grau: `decisão de método`**, vinda da conversa da bancada, não de medição.
Registro porque sem ela as duas de cima não bastam.

A observação dela é fonte primária nesta casa, e continua sendo. Isso **não** é o
mesmo que aceitar o enquadramento dela sem conferir. Dois casos de hoje:

- **Os três jogos como um caso só.** Tratá-los juntos teria escondido o Duskfade
  (§3.4).
- **O `Soltar` → `Liberar`.** Ela pediu no bloco do microfone. Fazer **só** o que
  foi pedido deixaria dois botões com a mesma função e nomes diferentes na mesma
  tela — trocar um problema por outro. Mudou nos dois.

O critério que separa isto de desobedecer: **corrigir enquadramento e nomeação;
nunca reverter medição dela.** O outro lado do critério é a D-c (§4.2): a memória
dela sobre o som do alto-falante no rádio é observação, entra como `medido`, e
derruba o `inferido-do-codigo` que está no mapa hoje. *"Não medi hoje"* NÃO é
*"não está medido"*.

### 5.4 Os erros de INSTRUMENTO do dia — cinco, e nenhum escondido

Três vezes a régua mentiu **antes** do produto, e as três custaram tempo:

| # | o erro | o que ensinou |
|---|---|---|
| 1 | **`quem_o_jogo_abre.py` respondia "o WRAPPER rodou? NÃO"** para os dois jogos, lendo o environ do `reaper` da Steam — que roda ANTES do wrapper. **O instrumento acusou a própria cura de não existir** | manda a investigação para o lugar mais caro possível. Corrigido por critério **estrutural**, nunca por conteúdo — que seria o instrumento confirmando a si mesmo |
| 2 | **Comparei o wrapper sem desescapar o VDF** e vi "0 jogos com wrapper" onde havia **62** | formato antes de veredito |
| 3 | **Usei `parece_infraestrutura` achando que filtrava jogos** — ela filtra executáveis | ler o contrato da função antes de usar o resultado dela |

Os outros dois viraram regra e estão em §5.1 (o gesto composto) e §5.2 (a ponte
do mic). E há um sexto, de outra natureza, que vale registrar: quando duas réguas
independentes discordaram sobre o Pragmata, *"o agente errou"* era a hipótese
confortável — eu tinha usado a ferramenta do próprio projeto. **A discordância
entre duas réguas independentes ERA o achado**, e só apareceu porque a segunda
não herdou uma linha da primeira.

> Nas três da tabela, conferir o contrato antes de acusar o código foi o que
> evitou um diagnóstico falso. **É barato conferir e caro acusar errado.**

---

## 6. O estado do áudio — onde a sessão parou

**Esta é a última coisa medida, com o controle NO CABO.** Grau: medido na bancada
dela ao fim de 16/08 e relatado ao escrever esta página. **Não refeito por esta
passagem** — nada aqui foi reexecutado.

### 6.1 O que foi observado, na ordem

1. **O DualSense aparece como placa de som** quando está no cabo:
   `alsa_card.usb-Sony_Interactive_Entertainment_DualSense_Wireless_Controller-00`.
   **Por rádio não existe placa nenhuma** — nem de captura nem de saída (ensaio
   `mic-radio-sem-placa-alsa-0727`, mesa 2+2: os dois do cabo têm placa, os dois
   do rádio não têm).
2. **O perfil da placa estava em `input:iec958-stereo`** — S/PDIF, `available: yes`
   e **sem sinal**. É a **camada 2** do mudo.
3. **Foi trocado para `output:analog-surround-40+input:analog-stereo`** — o perfil
   que tem fonte de captura **e** preserva a saída (o alto-falante e o canal de
   haptic-de-áudio).
4. **`doctor.sh --fix` curou a camada 1 e falhou na 2.**

### 6.2 As três camadas do mudo, e quem é dono de cada uma

Isto está medido desde 25/07 e é o mapa que explica o item 4 acima
(`scripts/doctor.sh`, bloco MIC-USB-01):

| camada | onde vive | quem cura |
|---|---|---|
| **1 — mute persistido por ROTA** | `~/.local/state/wireplumber/default-routes`, restaurado a cada conexão **sem nada no log**; sobrevive a reboot, replug e reinstalação | `scripts/doctor.sh --fix` / `--fix-mic`, que delega o `sed` ao `scripts/fix_wireplumber_default_source.sh --unmute-routes` — **o dono das escritas no estado do WirePlumber**, porque ele **para o serviço antes de editar** (com o WirePlumber vivo o arquivo é reescrito no shutdown, por cima da edição) |
| **2 — perfil da placa na entrada sem sinal** | o perfil ativo do card | `fix_mic_dualsense` no `scripts/doctor.sh`, via `pactl set-card-profile` |
| **3 — mudo no FIRMWARE do controle** | `daemon.state_full` (`audio.mic_mudo`) | `hefesto-dualsense4unix mic unmute` (IPC `mic.set`) |

**Por que a camada 2 falhou, e a resposta está escrita no código.** O decisor
`_dualsense_perfil_status` foi **reescrito em 26/07** e **nunca escolhe um perfil
que o ALSA marque indisponível** — porque a versão anterior fazia exatamente isso
e produzia uma source **sem porta de captura**, que entregava **327.680 bytes de
silêncio digital**. Hoje ele só considera perfis com `sources: >= 1` **e**
`available: yes`, e **a porta manda, não o nome do perfil**: se a source atual já
tem porta ativa, `fix_mic_dualsense` **não toca em nada** e imprime `pass`.

Logo, o `--fix` "falhar na camada 2" tem duas leituras possíveis, e **elas pedem
coisas opostas** — resolver qual é a primeira tarefa de áudio da próxima sessão:

- ou o `analog-stereo` estava `available: no` naquele instante (a detecção de
  jack não vê fone plugado, e a porta se chama `analog-input-headset-mic` embora o
  microfone **embutido** use esse mesmo caminho — no mixer ALSA o controle de
  captura se chama literalmente `Headset`), e aí o doctor **recusou corretamente**
  trocar para um perfil indisponível, e a troca à mão passou por cima da recusa;
- ou o alvo existia e o `pactl set-card-profile` falhou, e aí é defeito do doctor.

**Não sei qual das duas foi, e não invento.** O comando que separa as duas, em
leitura pura, é `LC_ALL=C pactl list cards` na seção do DualSense: se
`output:analog-surround-40+input:analog-stereo` aparecer com `available: yes` e
`sources: 1`, o doctor tinha alvo e não usou.

### 6.3 O que as regras do WirePlumber fazem — os dois arquivos que ninguém tinha juntado

**Os quatro drop-ins que o produto instala** vivem em
`~/.config/wireplumber/wireplumber.conf.d/`, e vêm de `assets/wireplumber/`:

| arquivo | o que decide |
|---|---|
| **51** — `51-hefesto-dualsense-no-default-source.conf` | a **prioridade** da entrada do controle |
| **52** — `52-hefesto-dualsense-disable-source.conf` | desabilita o mic (`node.disabled`) — opt-in |
| **53** — `53-hefesto-dualsense-disable-output.conf` | desabilita a **saída** (reforço do 52) — opt-in |
| **54** — `54-hefesto-dualsense-alto-falante-nunca-dorme.conf` | `session.suspend-timeout-seconds = 0` no sink do controle. **Sem flag, em todo formato do `install.sh`** |

**O 51 mudou de sentido em 08/08, e é a parte que engana.** Ele **nasceu** como
supressão (`priority.session = 50`, para o controle não virar microfone padrão
sozinho — a queixa original era *"o controle fica diminuindo/mexendo no
microfone"*). Hoje ele é o **PROMOTOR**: a entrada do controle vai para
`priority.session = 1500`, uma **faixa medida**:

```
abaixo de qualquer captura real  ->  2009 (a placa do PC, com mic PLUGADO)
acima de qualquer monitor        ->  1109 (o monitor do sink do controle)
                                     os outros monitores: 736 e 696
1500 fica no meio, com folga dos dois lados.
```

**O invariante que ele existe para garantir:** *um microfone de verdade nunca pode
perder para um monitor.* Sem o 51, medido em 08/08, o monitor (1109) vencia o
microfone (50) **por vinte e duas vezes**, e o que qualquer aplicativo gravasse
era o áudio de **saída** — não a voz dela. Portão:
`tests/unit/test_monitor_que_vence_01.py`.

**Nota de leitura de 14/08, que evita diagnosticar defeito onde não há:** aquele
2009 vale **com microfone plugado**. Sem nada na entrada analógica, as três portas
da placa do PC ficam `not available` e ela **cai para 1109** — aí o 1500 do
controle a vence e o DualSense vira o microfone padrão. **Isso é a faixa
funcionando**, não caducando: sem mic plugado não há captura real para preservar,
e no instante em que ela plugar um a placa retoma o posto sozinha.

**O gate `HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED=1`**, em
`scripts/fix_wireplumber_default_source.sh`, faz `--install` e `--disable-source`
virarem **`--enable-mic`** automaticamente: se a usuária declarou que **quer** o
mic do DualSense, suprimi-lo é o oposto do desejado. O `--enable-mic` remove o
52/53, **garante** o 51 (o promotor), desmuta as rotas (camada 1) e reinicia o
WirePlumber. O `install.sh` tem o equivalente por linha de comando:
`--keep-dualsense-mic`.

**A pegadinha de sinal que a próxima pessoa precisa saber:** a **promoção
explícita** (`--promote-source`, ou `hefesto-dualsense4unix mic promote`)
**remove** o 51 de propósito — porque `doctor.sh:_prefere_mic_do_dualsense` lê a
**ausência** do 51 como *"a usuária promoveu o controle a dedo"*. Manter o arquivo
ali mudaria o significado de um sinal que **outro programa** consome. Já o
`--enable-mic` **mantém** o 51: apagá-lo ali era desarmar a cura de 08/08 (foi o
defeito LIGAR-QUE-APAGAVA-A-CURA-01, portão
`tests/unit/test_ligar_que_apagava_a_cura_01.py`).

**Contexto de decisão:** [ADR-019](../adr/019-wireplumber-default-active-not-configured.md)
— a pós-condição canônica de sucesso é o default **ATIVO**, nunca o `configured`;
e rebaixar **não vence escassez**.

### 6.4 O que precisa entrar no INSTALL e na JANELA

Ela pediu: *"se funcionar toma nota pra corrigirmos no install e no gui"*.
**Nada disto foi construído hoje** — é o que fica escrito com endereço.

| # | o que | onde entra | por quê |
|---|---|---|---|
| **I-1** | **A troca de perfil da placa tem de acontecer no install, sem flag** | `install.sh`, no bloco do passo 10 (que hoje chama `--nunca-dorme` e depois `--install`/`--disable-source`); a lógica já existe em `fix_mic_dualsense` (`scripts/doctor.sh`) | hoje a camada 2 só se cura por `scripts/doctor.sh --fix` / `--fix-mic`, isto é, **à mão**. Pela regra dela de 08/08 — *toda cura entra no install, sem flag* — isso é dívida, não escolha |
| **I-2** | **O install tem de dizer se o microfone do controle capta, não só quem é o padrão** | `install.sh` passo 10, e o critério já existe: `_dualsense_source_tem_porta` em `scripts/doctor.sh` | é a mesma família do INSTALADOR-QUE-APROVOU-O-MONITOR-01: o passo imprimia OK e o doctor reprovava o mesmo estado dois minutos depois. **A pergunta era estreita demais para a afirmação que saía dela** |
| **I-3** | **Um portão que reprove binário externo citado e não declarado** | novo, irmão de `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py` | nasce vermelho hoje no `wmctrl` (§1.6), e passa a proteger os próximos. **É o portão de maior alcance do dia**: a família inteira de *"o produto depende de algo que ninguém instala"* cabe nele |
| **G-1** | **A janela tem de mostrar o estado do microfone por CAMADA**, e nomear qual está mudando | `app/widgets/controller_card.py`, no bloco do microfone que ganhou o controle deslizante em `1e96db5` | hoje as três camadas produzem **o mesmo sintoma visível** (pico 0) e têm três donos diferentes. A aba Status dizia a verdade o tempo todo em 25/07 — o medidor era a única coisa funcionando — e ainda assim o diagnóstico levou horas |
| **G-2** | **A janela tem de oferecer a cura**, não só o diagnóstico | `app/ipc_bridge.py` / `daemon/ipc_handlers.py`, ao lado da cadeia `mic.volume.set` que nasceu hoje | a camada 3 já tem caminho pelo IPC (`mic.set`); as camadas 1 e 2 só têm caminho por script de terminal. Regra dela de 09/08: **tudo tem que chegar na interface e no install** |
| **G-3** | **A janela tem de dizer POR QUE um modo de som está indisponível**, e a frase de hoje está errada | `app/audio_saida.py:1006`: `TEXTO_SONO_SEM_PLACA = "Sem placa de som do controle (no rádio não existe alto-falante)"` | **o alto-falante EXISTE no aparelho** — medido com a orelha dela em 02/08, com controle negativo, e ela mesma derrubou a confusão em 15/08: *"no próprio projeto já fizemos isso, deveria tá mapeado inclusive no specs"*. O que não existe no rádio é a **placa ALSA**. **Há um teste segurando a frase errada** (`tests/unit/test_o_alto_falante_nunca_dorme_01.py`), então a mordida **conserta um teste existente**, não só adiciona um. É palavra de tela: PROVA-DE-TELA-01, e a palavra final é dela |

### 6.5 A dívida de áudio que some sozinha se ninguém olhar

**Hoje o alto-falante do controle funciona por acidente feliz.** Medido em 16/08
00h40, com par com/sem:

- arquivo de **quatro canais nativos** (grave só no front-left, pulsado só no
  front-right): ela ouviu **só o pulsado**. O canal esquerdo **não chega**;
- arquivo **estéreo** no mesmo sink de quatro canais: ela ouviu **os dois**.

Única diferença: o número de canais do arquivo. **Quem soma L+R é a conversão 2→4
do PipeWire**, não o firmware — e isso é **política dele**, não garantia do
aparelho. O mapa (`docs/data/mapa-controles.csv`, `cabo_ressalva` de
`audio.alto_falante.rota@dualsense`) nomeia os três casos em que o acidente some,
e nenhum é exótico: jogo que emita quatro canais nativos; política de upmix
diferente noutra distro ou versão; áudio que chegue por caminho que não passe pela
conversão.

**É a ONDA 2 da [TRÊS MODOS DO SOM-01](sprints/2026-08-16-TRES-MODOS-DO-SOM-01-o-que-sai-onde-e-quem-escolhe.md)
§6, e é a única frente de som que não depende de decisão nenhuma dela.** A
recomendação é fazer por **regra de sistema** (um quinto drop-in), pela coerência
com a decisão já escrita no cabeçalho do 54 — a pergunta P-5 é só se ela aceita
mais um arquivo do produto no áudio da máquina.

O mapa dos canais, medido em teste cego com a orelha dela, no cabo, um canal por
vez (`docs/data/ensaios.csv`):

```
canal 0   front-left    ->  fone L                     · NÃO chega ao alto-falante
canal 1   front-right   ->  fone R (com fone)          · ALTO-FALANTE (sem fone)
canal 2   rear-left     ->  nada, em passada nenhuma
canal 3   rear-right    ->  nada, em passada nenhuma
```

**Três saídas físicas, quatro canais ALSA, dois sem destino.** E isso responde a
hipótese dela de 14/08: **não existe um canal dedicado a SFX no DualSense**. O que
isso **não** diz é que ela viu errado no PlayStation — diz que, se o Sackboy manda
efeito para o alto-falante no PS5, não é por um quarto canal de placa de som. É
API, não fio. **O lado do DualSense é MEDIDO; o lado do PS5 é RACIOCÍNIO, e
ninguém aqui mediu um PS5.**

---

## 7. Onde está cada coisa

| se a pergunta é | leia |
|---|---|
| o que quebrou e foi consertado hoje, com commit | [ÍNDICE — a bancada de oito horas](sprints/2026-08-16-INDICE-a-bancada-de-oito-horas.md) |
| como cada frente aberta **fecha**, e como o portão morde | [O QUE FICOU ABERTO-01](sprints/2026-08-16-O-QUE-FICOU-ABERTO-01-e-como-cada-um-fecha.md) |
| a ordem de atacar, na lista dela | [PONTO A PONTO-01](sprints/2026-08-16-PONTO-A-PONTO-01-a-lista-dela-e-a-ordem-de-atacar.md) |
| o defeito do rádio, e os onze suspeitos eliminados | [O RÁDIO MEIO MUDO](estudos/2026-08-16-O-RADIO-MEIO-MUDO-o-que-atravessa-e-o-que-nao.md) |
| o PS preso, a ponte do mic e as duas rodadas | [O PS PRESO](estudos/2026-08-16-O-PS-PRESO-a-ponte-do-mic-e-o-laco-que-abria-a-steam-sozinho.md) |
| os três modos de som que ela pediu, e as cinco perguntas | [TRÊS MODOS DO SOM-01](sprints/2026-08-16-TRES-MODOS-DO-SOM-01-o-que-sai-onde-e-quem-escolhe.md) |
| o ensaio de 4 minutos que decide o som por rádio | [A CADEIA DE BLOCOS-01](sprints/2026-08-16-A-CADEIA-DE-BLOCOS-01-o-ensaio-de-quatro-minutos-que-decide-o-som-por-radio.md) e [E-5 O TERRENO](sprints/2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md) |
| a Steam apagando a lightbar | [ESCRITOR-CRU-01](sprints/2026-08-16-ESCRITOR-CRU-01-a-steam-apaga-a-barra-e-o-produto-nao-reagia.md) |
| a Steam comendo a linha do wrapper | [SENTINELA-WRAPPER-01](sprints/2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md), [O WRAPPER QUE SUMIU-01](sprints/2026-08-16-O-WRAPPER-QUE-SUMIU-01-uma-variavel-nova-apaga-a-ponte-em-silencio.md) e [A ÁRVORE ERRADA](estudos/2026-08-16-A-ARVORE-ERRADA-o-portao-que-olhava-para-o-lugar-errado.md) |
| o censo dos campos de uma linha só, e os portões que contam | [O QUE A STEAM COME EM SILÊNCIO](estudos/2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md) e [A LINHA QUE A STEAM COME](estudos/2026-08-16-A-LINHA-QUE-A-STEAM-COME-o-censo-dos-campos-e-a-arvore-errada.md) |
| o Duskfade, a máscara Xbox e os 8 espelhos | [A MÁSCARA QUE O PRODUTO ESCOLHE-01](sprints/2026-08-16-A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01-o-jogo-nao-enxerga-e-a-culpa-nao-e-da-pessoa.md) e [A MÁSCARA QUE O DISCO NÃO SABE](estudos/2026-08-16-A-MASCARA-QUE-O-DISCO-NAO-SABE-o-censo-que-derrubou-a-deteccao-por-engine.md) |
| o critério de pronto dela, jogo a jogo | [JOGÁVEL EM TODOS-01](sprints/2026-08-16-JOGAVEL-EM-TODOS-01-o-alvo-dela-e-cada-jogo-nos-dois-transportes.md) |

---

## 8. O que esta página RECUSA afirmar

- **Que o defeito da reconexão está entendido.** Um suspeito caiu, com portão.
  Sobram três, e o mais informativo (`pending`) aponta para a **descoberta** do
  nó, não para o laço de reabertura — e isso é leitura de código, não medição.
- **Que a ponte do mic trava por causa da sequência do `0x32`.** É a única
  hipótese de pé e tem endereço, mas a sequência dos dois lados **não foi medida
  no mesmo instante**, e a árvore contém duas afirmações contraditórias sobre isso.
- **Que instalar o `wmctrl` resolve o §1.6.** A sessão é Wayland/COSMIC e o
  `wmctrl` é X11. Se a Steam sob Xwayland é alcançável por ele é **`incerto`**.
- **Que o alto-falante por rádio funcionou ou não funcionou.** A memória dela é
  fonte primária e o CSV diz outra coisa. A hipótese de reconciliação — que o que
  ela lembra pode ter sido **volume e rota respondendo por rádio**, que é coisa
  diferente de **PCM saindo pelo alto-falante por rádio** — **não foi medida**.
- **Que os 37% do giroscópio (ou os 81% e 64% do `espelho_fiel.py`) são perda.**
  Podem ser decimação de projeto. Ninguém mediu.
- **Que o touchpad engasga por minha causa.** É a primeira suspeita, e nada mais.
- **Que os 22 jogos "sem impedimento conhecido" funcionam.** Eles não têm motivo
  *conhecido* para falhar — e o Duskfade está entre eles, quebrado.
- **Que a camada 2 do áudio falhou por defeito do doctor.** Ver §6.2: há duas
  leituras, e elas pedem coisas opostas.
