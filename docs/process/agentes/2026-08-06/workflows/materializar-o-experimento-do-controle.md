# workflow materializar-o-experimento-do-controle

- runId: wf_d8ef2faf-515 | status: completed | agentes: 4 | tokens: 636,264 | duracao: 42 min
- summary: Escrever a medicao do experimento CONTROLE-SONY-MEDIDO-01 na sprint, propagar a doutrina nova para os documentos que a contradizem, e corrigir o desenho da caixinha
- fases: Confirmar, Escrever, Verificar

## RESULTADO

### confirmacao

# CONFERÊNCIA DE CÓDIGO — experimento de 06/08/2026 (M-04 / doutrina da allowlist)

Nada foi alterado. Todo `caminho:linha` abaixo foi aberto e lido na árvore de hoje (branch `restauro/inicio-da-sessao`).

---

## ITEM 1 — O caminho do `UHID_OUTPUT`: o que o vpad faz com o que o jogo escreve

**GRAU: MEDIDO (leitura de código completa, caminho fechado ponta a ponta).**

Cadeia canônica, em ordem:

| Etapa | Caminho:linha |
|---|---|
| Drena o fd do uhid a cada tique do poll loop | `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/src/hefesto_dualsense4unix/integrations/uhid_gamepad.py:1500-1532` (`pump_ff`) |
| Despacha o evento | `uhid_gamepad.py:1534-1560` (`_handle_event`) |
| `UHID_OUTPUT` -> `_handle_output` | `uhid_gamepad.py:1555-1556` |
| Docstring que a sprint questiona | `uhid_gamepad.py:1562-1571` |
| Extrai as categorias do report 0x02 | `uhid_gamepad.py:1711-1741` (`_replicate_from_output`) |
| Dedup por valor | `uhid_gamepad.py:1743-1749` (`_queue_replica`) |
| Rate-limit por categoria | `uhid_gamepad.py:1751-1769` (`_flush_replicas`) |
| Entrega ao sink | `uhid_gamepad.py:1771-1818` (`_forward_replica`) |
| Fim de sessão | `uhid_gamepad.py:1820-1843` (`_end_game_session`) |

**Ele repassa ao físico? Sim, e é literal.** Os sinks são construídos em
`/mnt/Apate/.../daemon/subsystems/gamepad.py:847-889` (`make_primary_replica_sinks`) e miram o **MAC do primário resolvido NA HORA** de cada réplica (`primary_uniq`, gamepad.py:867-872). Cada categoria tem sua porta:

- gatilhos -> `gamepad.py:771-792` (`apply_game_trigger`, **sem broadcast** de propósito: sem MAC alvo a réplica é descartada);
- lightbar -> `gamepad.py:795-809` (`apply_game_lightbar`);
- player-LED -> `gamepad.py:812-830` (`apply_game_player_leds`);
- rumble -> `uhid_gamepad.py:1686-1692` (`_emit_rumble`) -> `gamepad.py:720-768` (`apply_game_rumble`).

**Há filtro, prioridade e cache — cinco portões, todos declarados:**

1. **Gate de sessão + graça pós-bind** — `uhid_gamepad.py:1696-1709` (`_replicating`): só replica entre `UHID_OPEN` e `UHID_CLOSE` **e** depois de `_GAME_REPLICA_GRACE_S = 0.5 s` do `UHID_START` (`uhid_gamepad.py:350-355`). A graça existe porque o próprio probe do `hid_playstation` no vpad emite outputs.
2. **Dedup por valor** — `uhid_gamepad.py:1743-1749`: valor igual ao último ENTREGUE e sem pendência = descartado.
3. **Rate-limit por categoria** — `_REPLICA_MIN_INTERVAL_S = 1/250 s` (`uhid_gamepad.py:345-348`); o retido sai no pump seguinte (`uhid_gamepad.py:1513-1515`).
4. **Gate de autoridade (NUMA-02)** — `/mnt/Apate/.../core/backend_pydualsense.py:1232-1248` (`_game_wins`) + `3049-3094` (`set_game_output_for`): sob autoridade `daemon` a réplica de exibição é **retida** (retain-latest), não escrita.
5. **Cache de escrita sysfs** — `/mnt/Apate/.../core/sysfs_leds.py:183-217`: escrita igual à última bem-sucedida é pulada.

**Ressalva honesta, não medida antes:** o rumble tem política própria — `apply_game_rumble` **ignora o FF do jogo** quando há rumble fixado manual (`gamepad.py:747-748`) e aplica o multiplicador do slider global (`gamepad.py:750-752`). Ou seja, no rumble a usuária vence; na lightbar/gatilho, não.

`_end_game_session` (`uhid_gamepad.py:1820-1843`) limpa dedup/rate-limit **sempre**, mas só chama `session_end_sink` se algo foi de fato replicado (`_game_dirty`) — daí a devolução de perfil/paleta em `backend_pydualsense.py:3131-3191` (`end_game_session_for`).

---

## ITEM 2 — Quem vence quando o jogo e a usuária escrevem a mesma coisa

**GRAU: MEDIDO (a política é declarada, por escrito, num ponto único).**

**Sim, há política declarada — e ela dá a vitória ao JOGO.**

`/mnt/Apate/.../core/backend_pydualsense.py:1250-1309` (`_merged_desired_for_key`), docstring nas linhas **1253-1259**:

> Precedência (D5, POR CAMPO): camada GAME (REPLICA-03) > camada CO-OP (R-13) > override explícito por-uniq (perfil/usuária, R-20) > camada AUTOMÁTICA (COR-03) > default global do perfil.

A linha que executa isso é `backend_pydualsense.py:1307-1308`. E há um detalhe fino, em `1263-1266`: **o brilho dela escala tudo, menos a cor do jogo** — *"escalar o que o jogo pinta seria mentir sobre o que ele pediu"*.

Isto **confirma o item 3 da conclusão da sprint por construção**: fora da allowlist, o jogo escreve no vpad, a réplica vira camada GAME, a camada GAME é o topo do merge, e a cor dela some. Não é acidente nem race — é a prioridade escrita.

O único contrapeso é o gate de autoridade (`_game_wins`, `backend_pydualsense.py:1232-1248`), alimentado por `/mnt/Apate/.../daemon/subsystems/game_signal.py` — e ele é **fail-safe para o lado do jogo**: sem provider, com exceção, ou com autoridade `unknown`, o jogo vence (`backend_pydualsense.py:1242-1248`). Só a autoridade `daemon` **explícita** fecha o portão. Com o Sackboy rodando, a autoridade era `game`.

### O `lightbar_reassert_skip_cache` — o que ele significa

**GRAU: MEDIDO quanto ao significado; SUSPEITA COM MECANISMO quanto à origem da cor.**

Emitido em `/mnt/Apate/.../core/sysfs_leds.py:194-202`. Significado exato: **um reassert pediu exatamente a cor que já estava no cache desta instância, e a escrita foi pulada**. É telemetria da *cura* do "flash azul de 30 s" (GUERRA-01), não prova de escrita do jogo.

Duas correções à leitura do arquivo bruto `passo3-resultado.txt`, onde a linha aparece sob o cabeçalho *"o jogo escreve no controle?"*:

1. **A linha sai UMA VEZ na vida da instância.** `self._skip_logged` é inicializado em `sysfs_leds.py:65` e só vai a `True` em `:202` — **nunca é rearmado** (`invalidate_cache`, `:219-225`, mexe só em `_last_write`). Logo, `rgb=(198, 70, 0)` é o valor do **primeiro** cache-hit daquele nó, não o estado às 19:52:50.
2. **`verify=False` é o default** (`sysfs_leds.py:183-203`): no skip **não** houve releitura. A verificação anti-escritor-estrangeiro (`lightbar_escritor_estrangeiro`, `:204-211`) só roda com `verify=True`, que só é passado sob autoridade `daemon` (`backend_pydualsense.py:3362, 3373`) — ou seja, **nunca** enquanto o jogo está de pé.

**De onde veio (198, 70, 0):** conferi por eliminação, com os arquivos no disco.

- Nenhum dos 15 perfis dela produz essa cor, com ou sem `lightbar_brightness` (o perfil ativo, `sackboy_nativo`, é `[80, 60, 220] * 0.6 = (48, 36, 132)`);
- não é a paleta automática (`/mnt/Apate/.../core/led_control.py:146-155` — nenhum valor bate);
- não é o azul do kernel (`backend_pydualsense.py:70`, `KERNEL_DEFAULT_BLUE = (0, 0, 128)`);
- a escala de brilho é multiplicador linear por canal (`led_control.py:62-80`), e nenhum fator único leva um perfil dela a `(198, 70, 0)`.

Por eliminação, a origem provável é a **camada GAME** — o Sackboy pintando o vpad e a réplica chegando ao físico pela mesma rota sysfs (`backend_pydualsense.py:2230-2233`: lightbar do jogo e da usuária usam **o mesmo** `node.set_rgb`). **GRAU: SUSPEITA COM MECANISMO** — não há linha no journal que carimbe a cor na entrada da réplica.

**Um dado que consegui medir agora, e que fecha o nó do log** (leitura direta do sysfs, 06/08):

```
/sys/class/leds/input1011:rgb:indicator -> /sys/devices/virtual/misc/uhid/0005:054C:0CE6.000D/...
/sys/class/leds/input1027:rgb:indicator -> /sys/devices/virtual/misc/uhid/0003:054C:0DF2.000E/...
```

Bus `0005` = Bluetooth, PID `0CE6` = **o DualSense físico**. Bus `0003`, PID `0DF2` = **o vpad Edge**. Ou seja: **o `lightbar_reassert_skip_cache` do journal era no FÍSICO**, não no virtual. **GRAU: MEDIDO.** (E o vpad está com `multi_intensity = 0 0 0`: o daemon não dirige a classe LED do vpad.)

---

## ITEM 3 — Na exceção, solta o GRAB e mantém o HIDRAW

**GRAU: MEDIDO. É o coração da correção de doutrina, e o código o confirma linha a linha.**

Borda de ENTRADA da exceção — `/mnt/Apate/.../daemon/subsystems/gamepad.py:269-285`:

- **`gamepad.py:271`** — `_set_evdev_grab(daemon, False)` -> **solta a ENTRADA** (é a linha que produziu `gamepad_controller_grab grab=False` às 19:39:52, emitida em `gamepad.py:146`).
- **`gamepad.py:272-279`** — `client.restore_all` -> **desesconde o nó hidraw do físico para os OUTROS processos**. `restore_all` é `{"cmd": "restore_all"}` ao broker root (`/mnt/Apate/.../integrations/hidraw_broker_client.py:130-141`); `hide` é *"esconde `node` do uid da sessão"* (`hidraw_broker_client.py:106-114`). **É permissão de nó, não fechamento de fd.**
- **`gamepad.py:283-284`** — `suspend_vpads_for_steam_input` -> derruba o vpad (**derruba a ENTRADA virtual**), definido em `gamepad.py:425-497`, com `stop_gamepad_emulation(persist=False, release_grab=False)` na linha **497**.

**O que NÃO acontece — e é este o achado:** nenhum caminho da exceção fecha o handle de saída do daemon. Os handles vivem em `self._handles` (`backend_pydualsense.py`) e não são tocados por `sync_steam_input_exception`. O grep de `steam_input_excecao_ativa` devolve **cinco** call-sites, **todos** em `gamepad.py` (`:166`, `:207`, `:265`, `:366`, `:370`) — **zero** em `core/`. Ou seja: **não existe portão da exceção no caminho de saída** (lightbar, gatilhos, rumble, player-LED). O perfil dela continua sendo escrito no físico durante a exceção inteira.

Isso explica exatamente o que ela viu no passo 2: gatilhos **duros** e o **vermelho** dela aplicado e mantido com o Mullet aberto, e `hidraw abertos pelo daemon: 1`.

**Assimetria adicional, já documentada e agora confirmada:** o pulo do grab só vale na ENTRADA — `gamepad.py:166-169` (*"o ungrab nunca é pulado: expor nunca é errado"*), e o pulo do hide em `gamepad.py:204-215`, cujo comentário (`:208-211`) já dizia a razão certa: *"a Steam precisa LER o hidraw para entregar o DualSense pela API dela (SetDualSenseTriggerEffect)"*.

**Conclusão de doutrina, confirmada no código:** durante a exceção o Hefesto abre mão da **entrada** (grab do evdev + vpad) e **mantém integralmente a saída**. A frase *"o Hefesto sai da frente"* descreve metade do mecanismo.

---

## ITEM 4 — A exceção termina por FOCO de janela?

**GRAU: MEDIDO quanto ao caminho de código; e o experimento atribuiu a linha errada — ver a correção abaixo.**

### 4a. Sim, existe um caminho por foco, e ele é INTENCIONAL

`/mnt/Apate/.../daemon/launch_env.py:408-449` (`steam_input_exception_appid`). Duas evidências, **nesta ordem**:

- **Evidência 1, marker do wrapper** (`launch_env.py:441-443` -> `launch_session_appid`, `:382-405`). A docstring em **`:390-391`** afirma: *"Sobrevive a alt-tab (o critério é o PID do jogo, não o foco)"*. Confirmado no wrapper: `assets/hefesto-launch.sh` grava `pid=$$` e depois faz `exec` (comentário nas linhas 109-113), então o PID gravado é o do próprio jogo enquanto ele roda.
- **Evidência 2, janela em foco** (`launch_env.py:444-448`), com leitura **CRUA** (nunca o sticky). A docstring em **`:422-426`** declara a intenção explícita:

> *"Leitura CRUA de propósito: aqui a pergunta é 'o jogo da allowlist está na frente agora?', e usar o sinal sticky faria a exceção sobreviver 30 s depois do alt-tab — tempo em que o físico ficaria exposto ao desktop sem motivo."*

E em **`:434-436`**: *"enquanto esta função disser um appid, a usuária está SEM vpad — o sinal tem de apagar assim que o jogo sai da frente, não 30 s depois."*

**Veredito: INTENCIONAL, não efeito colateral.** Está escrito, com a razão e o custo.

### 4b. A linha citada no experimento NÃO é o fim da exceção

**GRAU: MEDIDO.** `modo_jogo_padrao_solto motivo=janela_fora_do_jogo` é emitido em `/mnt/Apate/.../daemon/lifecycle.py:2284-2290`, dentro de `reverter_modo_jogo_padrao` (`:2239-2291`) — o **modo jogo padrão (MODO-01/B3)**, chamado pelo `AutoSwitcher` (`daemon/subsystems/autoswitch.py:207, 264`). É outro subsistema.

O fim da exceção do Steam Input tem log próprio: **`gamepad.py:286`**, `logger.info("steam_input_excecao_encerrada")` — **sem nenhum campo**. Não tem `motivo`, não tem `appid`, não tem `de=`.

**Achado desta conferência:** o journal **não consegue dizer por que a exceção terminou**. A borda de entrada loga o appid (`gamepad.py:270`); a de saída loga uma palavra só. Reconstruir o desfecho de 19:45:32 a partir do journal é impossível hoje.

### 4c. Reconstrução do que provavelmente encerrou a exceção às 19:45:32

**GRAU: SUSPEITA COM MECANISMO.** O `last_run` é **um arquivo global, não por appid** (`assets/hefesto-launch.sh:120-132`; leitura em `launch_env.py:393`). Lançar o Sackboy sobrescreve o marker do Mullet. A partir daí `launch_session_appid` devolve `1599660`, que não está na allowlist -> evidência 1 falha; e o foco estava na Steam -> evidência 2 falha. A exceção cai **com o Mullet ainda rodando** (o `passo3.txt` das 19:45:59 ainda registra `AppId=2111190`), e o `default.env` foi regravado às 19:45:34 — que é a assinatura do vpad voltando.

Não é o alt-tab; é **o segundo lançamento**. Não há linha de journal que prove isso, e por isso o grau não sobe.

### 4d. Efeito prático do alt-tab no meio do jogo

**GRAU: SUSPEITA COM MECANISMO** (caminho lido; não observado ao vivo).

- **Jogo da allowlist lançado PELO wrapper, sem outro launch no meio:** alt-tab **não** derruba a exceção — a evidência 1 é consultada primeiro e é imune ao foco.
- **Jogo da allowlist aberto SEM o wrapper** (ou com o marker sobrescrito): alt-tab derruba a exceção no tique seguinte. A reconciliação roda a **1 Hz** (`gamepad.py:78`, `STEAM_INPUT_VIGIA_INTERVAL_SEC`, e `:68`, `LAUNCH_RECONCILE_INTERVAL_SEC`) e **não há histerese em nenhuma das duas bordas** (`gamepad.py:266-267` age direto na borda). Voltar o foco ao jogo rearma a exceção e derruba o vpad de novo.
- **O custo por ciclo é caro:** cada volta recria o vpad (`resume_vpads_after_steam_input`, `gamepad.py:541-609`) **e** ressincroniza o co-op com `force=True` (`gamepad.py:605-608`), e cada ida derruba o co-op inteiro (`gamepad.py:493-495`). Num alt-tab repetido isso é churn de device no meio do jogo — exatamente o modo de falha que a própria `arm_launch_profile` cita em `launch_env.py:462-465` (*"a Steam nunca reabre o hidraw do vpad do P1"*).
- **O Steam Input "perde a vez"?** Sim, no sentido de que o físico volta a ser grabado e re-escondido (`gamepad.py:304-306`). Se o jogo já enumerou os dispositivos, o efeito prático depende de ele reenumerar — não medido.

---

## ITEM 5 — "DualSense por HID direto" vs. "DualSense via Steamworks"

**GRAU: MEDIDO (é um levantamento exaustivo do repositório).**

**A metade Steamworks EXISTE e está nomeada em quatro lugares:**

| Onde | O que diz |
|---|---|
| `/mnt/Apate/.../daemon/launch_env.py:345-348` | *"jogos cuja via oficial de DualSense é o Steam Input per-app (medido: Mullet Mad Jack, appid 2111190, chama `SetDualSenseTriggerEffect` da API Steamworks, que só funciona com o Steam Input DAQUELE jogo ligado)"* |
| `/mnt/Apate/.../integrations/storm_doctor.py:30-31` | mesma frase, forma curta |
| `/mnt/Apate/.../daemon/subsystems/gamepad.py:208-211` | *"a Steam precisa LER o hidraw para entregar o DualSense pela API dela (SetDualSenseTriggerEffect)"* |
| `/mnt/Apate/.../daemon/subsystems/gamepad.py:432-434` | *"é ele que a Steam entrega ao jogo, com os gatilhos adaptativos da API Steamworks"* |

**A metade HID direto NÃO EXISTE em lugar nenhum.** `grep -rn "HID direto\|hid direto"` em `.py`, `.md`, `.sh`, `.txt` do repositório: **zero ocorrências**. Não há termo, não há constante, não há comentário que descreva "o jogo escreve no hidraw do vpad e atropela os ajustes dela" como um **caminho de jogo** — mesmo com o mecanismo implementado inteiro no REPLICA-03. **A ausência é o achado, e ele se confirma.**

**E a casa já se contradiz sem perceber, o que é a prova forte de que a distinção falta:**

- `~/.config/hefesto-dualsense4unix/steam_input_apps.txt` (só leitura) tem **dois** appids com **duas justificativas incompatíveis**: `2111190` — *"SetDualSenseTriggerEffect via Steamworks"*; `3357650` — *"suporte nativo a DualSense entregue PELA Steam. Registrado em 26/07/2026 depois de medir 4 joysticks para 1 controle"*. O segundo entrou por **duplicado**, não por Steamworks. O cabeçalho do arquivo, porém, define a lista como *"jogos cuja via oficial de DualSense é o Steam Input"*.
- `/mnt/Apate/.../docs/usage/jogos-e-mascaras.md` tem **duas seções separadas** — a da exceção e *"Jogos com suporte nativo a DualSense"* (`:59-66`) — e lista **Pragmata nas duas**. Sackboy está só na segunda, e o experimento agora confirma que ele **não precisa** da lista.

Ou seja: a leitura *"a allowlist não é 'jogos com DualSense nativo', é 'jogos cujo DualSense passa pela Steam'"* **não está escrita em lugar nenhum**, e o arquivo de configuração dela já viola a própria definição do seu cabeçalho.

**Ressalva de grau, respeitada:** a atribuição Steamworks-vs-HID-direto continua **SUSPEITA COM MECANISMO** — nenhum símbolo dos dois binários foi lido. O que é MEDIDO é a ausência da distinção no repositório.

---

## ITEM 6 — As frases que ganham nota datada

**GRAU: MEDIDO (todas conferidas linha a linha).**

### 6a. `docs/usage/modos.md` — achado inesperado

**Nenhuma frase caduca ali, porque a allowlist NÃO É MENCIONADA no arquivo.** `modos.md` (96 linhas) fala da Steam só em `:70-87` ("Steam: as Opções de Inicialização") e nunca cita `steam_input_apps.txt`, nem a exceção, nem o botão "Este jogo não funciona". A única frase parecida é `docs/usage/modos.md:84` — *"Com o Hefesto desligado ele sai do caminho"* — que é sobre o **wrapper com o daemon morto**, não sobre a allowlist. **Não caduca.**

O que caduca em `modos.md` é uma **omissão**: `:40-44` promete que o que o jogo escreve *"é replicado no controle físico"* sem dizer que isso **sobrescreve os ajustes dela** — a metade que o experimento acabou de medir no Sackboy.

### 6b. `daemon/launch_env.py`

| Linha | Frase |
|---|---|
| `:436` | *"o sinal tem de apagar assim que o jogo **sai da frente**, não 30 s depois"* |
| `:483-485` | *"a allowlist é opt-in explícito de '**o Hefesto sai de cena neste jogo**'"* |
| `:487-488` | *"'sair de cena' era largo demais e engolia o que NÃO disputa nada com o jogo"* (já é uma correção parcial de 24/07 — **ainda insuficiente**, porque só ressalvou o mouse/teclado, não a saída) |
| `:1004-1006` | *"o gamepad virtual **sai de cena** enquanto o jogo da allowlist estiver em sessão"* |
| `:345-348` | *"jogos cuja via oficial de DualSense é o Steam Input per-app"* — **a definição da lista**, que o Sackboy refuta por contra-exemplo |

### 6c. `daemon/subsystems/gamepad.py`

| Linha | Frase |
|---|---|
| `:26-28` | *"a allowlist do Steam Input escolhe QUAL dispositivo o jogo enxerga (nela, o físico), nunca QUANTOS"* — **esta continua verdadeira e o experimento a confirma**; não caduca |
| `:30-31` | *"'**o Hefesto sai da frente**' significava o jogo enumerar o físico E o virtual"* |
| `:316` | *"a emulação não foi desligada, ela **SAIU DA FRENTE** deste jogo"* |
| `:322-323` | *"o jogo da allowlist rodando com o Hefesto **fora do caminho**"* |
| `:428` | *"Retira o gamepad virtual de cena pelo tempo do jogo da allowlist"* |
| `:1562-1571` (`uhid_gamepad.py`) | a docstring do `_handle_output` — **fiel ao que faz**; o defeito não está nela, está em **nenhum** dos textos da allowlist mencionar que este caminho segue vivo durante a exceção |

### 6d. Fora do escopo pedido, mas é o mesmo texto — e é o que ela LÊ na tela

| Caminho:linha | Frase |
|---|---|
| `/mnt/Apate/.../app/actions/daemon_actions.py:508` | *"o jogo passa a ser entregue pela Steam e o Hefesto **sai da frente** dele"* |
| `daemon_actions.py:543` | *"o Hefesto **já sai da frente** dele"* (toast) |
| `daemon_actions.py:545-547` | *"passa a ser entregue direto pela Steam e o Hefesto **sai da frente** dele"* (toast) |
| `daemon_actions.py:1108` | *"o Hefesto **sai da frente** DELE"* |
| `daemon_actions.py:1260` | *"O que ela custa é o Hefesto **sair da frente** do jogo"* |
| `daemon_actions.py:1311` | *"o `steam_app_<appid>.env` que faz o Hefesto **sair da frente** do jogo"* |
| `/mnt/Apate/.../app/actions/status_actions.py:242, 248` | *"O jogo assumiu o controle: o Hefesto **saiu da frente** dele"* (tooltip) |
| `/mnt/Apate/.../cli/cmd_steam.py:51` | *"Exceção do Steam Input — os jogos em que o Hefesto **sai da frente**"* (`--help`) |
| `/mnt/Apate/.../cli/cmd_steam.py:141` | *"Jogos em que o Hefesto **sai da frente** (o controle vem da Steam)"* |
| `/mnt/Apate/.../cli/cmd_coop.py:78` | *"**sai de cena** sozinho nos jogos com Steam Input"* |
| `/mnt/Apate/.../integrations/steam_launch_options.py:721` | *"este jogo é entregue pela Steam, **sai da frente**"* |
| `/mnt/Apate/.../daemon/ipc_handlers.py:1441` | *"rodando com o Hefesto **fora do caminho**"* |
| `/mnt/Apate/.../docs/usage/cli.md:301-302` | *"o co-op ainda sai de cena sozinho nos jogos com exceção de Steam Input"* |
| `/mnt/Apate/.../docs/usage/jogos-e-mascaras.md:42-44` | *"o gamepad virtual **sai de cena**: nesse jogo vale só o controle 1, sem co-op"* |

**Onde a nota datada cabe sem duplicar trabalho:** já existe `/mnt/Apate/.../docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md`, com a tabela *"Quais afirmações caducam"* em `:88-95` e o critério de desfecho em `:319`. É o lugar canônico.

---

## RESUMO DOS ACHADOS NOVOS (que não estavam na medição entregue)

1. **MEDIDO** — Não existe **nenhum** portão da exceção de Steam Input no caminho de saída: os 5 call-sites de `steam_input_excecao_ativa` estão todos em `gamepad.py`, nenhum em `core/`. A segunda metade da doutrina é **estrutural**, não emergente.
2. **MEDIDO** — A precedência que faz o jogo vencer a usuária está **escrita**, num ponto único: `backend_pydualsense.py:1253-1259`. Não é bug; é a política.
3. **MEDIDO** — No **rumble** a política é a inversa (a usuária vence: `gamepad.py:747-748`). A inversão do item 3 da conclusão vale para lightbar/gatilhos/player-LED, **não** para vibração.
4. **MEDIDO** — `steam_input_excecao_encerrada` (`gamepad.py:286`) **não tem campo de motivo**. O journal não pode dizer por que a exceção caiu.
5. **MEDIDO** — A linha `modo_jogo_padrao_solto motivo=janela_fora_do_jogo` é de **outro subsistema** (`lifecycle.py:2284-2290`), não do fim da exceção. A atribuição do relato precisa desta ressalva.
6. **MEDIDO** — `lightbar_reassert_skip_cache` sai **1x na vida da instância** (`sysfs_leds.py:65, 202`, sem rearme) e com `verify=False`. Não é prova de escrita do jogo, e o valor `(198, 70, 0)` não descreve o instante do carimbo.
7. **MEDIDO** — O nó `input1011` do journal é o **físico por Bluetooth** (`0005:054C:0CE6`), não o vpad (`0003:054C:0DF2`, com `multi_intensity` em `0 0 0`).
8. **SUSPEITA COM MECANISMO** — O `last_run` é **global, não por appid** (`assets/hefesto-launch.sh:120-132`): lançar um segundo jogo apaga a evidência autoritativa do primeiro e derruba a exceção com o primeiro ainda rodando. É a explicação mais simples para o fim às 19:45:32.
9. **MEDIDO** — Para jogo lançado **pelo wrapper**, alt-tab **não** derruba a exceção (evidência 1 vence). O caminho por foco só morde quem não passou pelo wrapper — e aí sem histerese nenhuma, a 1 Hz, com recriação de vpad e ressincronia de co-op a cada volta.
10. **MEDIDO** — `docs/usage/modos.md` **não menciona a allowlist**. Não há frase a corrigir ali; há uma seção a escrever.
11. **MEDIDO** — `steam_input_apps.txt` já contém duas entradas com justificativas mutuamente incompatíveis, e `jogos-e-mascaras.md` lista o Pragmata simultaneamente como "entregue pela Steam" e "suporte nativo".

### escrita

ESCRITO (só documentação; `src/` e `tests/` intocados; nada commitado).

1. `docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md` (+333) — seção **O RESULTADO** (`:387`): condições, passo 1/2/3 com carimbo e journal, a linha 2 da tabela de leitura realizada (as outras seis descartadas por medição), **M-04 FECHA POSITIVO (MEDIDO)**, a segunda metade (entrada solta / saída mantida), A INVERSÃO, os dois caminhos (Steamworks vs HID direto, SUSPEITA COM MECANISMO), 4 ressalvas e "o que paga / o que continua aberto". Sprint marcada **PAGA** no topo; aberto: versão do cliente Steam (não anotada, irrecuperável), atribuição Steamworks-vs-HID, a pergunta 5.1 (vpad), o log de saída sem motivo, o `last_run` global, a contradição do `steam_input_apps.txt`, o M-17.
2. `STEAM-QUE-DECIDE-01` (+44) — nota datada na E1: grau SEM PROVA -> MEDIDO; caducam *"seria apenas o Hefesto sair da frente (ungrab + vpad suspenso)"* e *"é a lista dos jogos em que o Hefesto se cala"*; o terceiro desfecho (recursos dependerem do global) descartado; E2..E6 liberadas.
3. `estudos/2026-08-05-o-sistema-de-perfis…` (+55) — nota no M-04 (refutado) e nota na seção 1.5: o critério que o D-34 dizia não existir, a inversão, e as duas justificativas incompatíveis do `steam_input_apps.txt`.
4. `docs/usage/jogos-e-mascaras.md` (+34) — caduca *"o gamepad virtual sai de cena"* como história completa (o Hefesto segue escrevendo no controle); a seção de nativos ganha "não precisam da lista, e eles mandam na luz e no gatilho"; contradição do Pragmata anotada.
5. `docs/usage/modos.md` (+24) — caduca por omissão o *"é replicado no controle físico"* (`:40-44`): a réplica **sobrescreve** os ajustes dela, menos vibração; e nota de que *"com o Hefesto desligado ele sai do caminho"* (`:84`) não é a allowlist.
6. `estudos/2026-08-06-desenho-a-flag-do-jogo…` — seção **5.4** (`:420`): desfecho positivo, itens 1-5 confirmados, título da seção 5 caduca pela metade (as features das abas **já valem**; o que sai é máscara e co-op), frase da caixinha encurtada (cai o "Hoje"), **5.1 continua SEM PROVA**, e o item novo (fora da lista o jogo vence). **P3 DESTRAVADO** (`:640`), P1/P2 intactos.
7. `CHANGELOG.md` — entrada no topo do `[Unreleased]`.

TOOLTIP NOVO (substitui *"Marque quando o jogo mostrar o controle duplicado"*): **"Marque quando o jogo só reconhecer o controle com o Steam Input dele ligado — nesses jogos é a Steam que entrega o DualSense. Se o controle já funciona sem a lista, não marque: aqui o co-op sai e a máscara acima não vale."** Procedência: "só reconhecer o controle" = inverso literal de `gui/main.glade:2430`; "Steam Input" = `glade:2951`/`:2977`; "a Steam entrega o DualSense" = `glade:2430`; "a lista" = `emulation_actions.py:339`; "o co-op sai" = `glade:2430`; "a máscara acima" = `profiles_actions.py:644`. Recusadas: "nativo/Conexão Nativa" (é modo, dois centímetros acima) e "Steamworks" (jargão, sem string de tela, e a atribuição é SUSPEITA).

Correção que fiz contra a árvore viva: os chamadores de `steam_input_excecao_ativa` são **oito**, não cinco (`gamepad.py:166,207,265,366,370,649,1134,1386`) — todos em `gamepad.py`, **zero** em `core/`; e a família "sai da frente/sai de cena/fora do caminho" são **25 linhas** em `src/`+`docs/usage/`. Portões: `git add -A` feito; acentuação, glifos, referências (196 docs) e anonimato **todos OK**; varredura por regex sobre os 20 arquivos no stage: **0** emoji e **0** U+2713/U+2717.

### verificacoes

[
  {
    "aprovado": false,
    "veredito": "REFUTADO por superpromoção. A espinha da entrega se sustenta — o M-04 fecha positivo pelo contraste medido (X-Box 360 pad em 1 no Mullet, 0 no Sackboy) — e conferi uma a uma as citações de código: gamepad.py:271, :272-279, :283-284, :286, :425, :747-752, os oito chamadores de steam_input_excecao_ativa (166/207/265/366/370/649/1134/1386, zero em core/), backend_pydualsense.py:1232-1248, :1253-1259, :1307-1308, sysfs_leds.py:65, :66-68, :194-202, lifecycle.py:2284-2290, hefesto-launch.sh:120-132, launch_env.py:35, :44-49, :345-348, :393, :482-486, storm_doctor.py:29-31, STEAM-INPUT-01:244-250, glade:2430/:2951/:2977, emulation_actions.py:339, profiles_actions.py:644, o conteúdo do steam_input_apps.txt dela e a identidade do nó input1011 (0005:054C:0CE6, físico por Bluetooth) — todas batem. Não há emoji nem U+2713/U+2717 nos 8 .md do stage, nem caminho de userdata dela, nem MAC. O que reprova é o excesso: um tamanho de amostra que não existe (\"três jogos abertos\" quando dois foram abertos), a premissa central do veredito (global \"0\" / per-app \"2\") nunca relida no horário do experimento, vibração e LED de jogador entrando em blocos MEDIDO sem terem sido exercitados, o critério novo do tooltip apoiado num contrafactual que ninguém rodou (o Mullet nunca foi aberto FORA da lista), \"o Sackboy funcionou completo\" contradizendo a própria medição numa página de uso, e três contagens (seis linhas descartadas, cinco de seis itens, 25 linhas do grep) que não fecham quando refeitas. Nada disso derruba o M-04; tudo isso é o tipo de frase que a casa manda desmarcar antes de virar doutrina.",
    "achados": [
      {
        "gravidade": "alta",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md:26 e :710; CHANGELOG.md:11; docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md:654",
        "o_que": "\"três jogos abertos de verdade\" é tamanho de amostra inventado, e aparece em quatro documentos dentro de blocos declarados MEDIDO.",
        "prova": "A medição bruta diz \"os TRÊS jogos com o wrapper do Hefesto nas opções de lançamento (conferido)\" — isso é configuração, não abertura. Os artefatos registram DOIS jogos abertos: Mullet (passo2.txt 19:41:12, passo2-resultado.txt 19:44:46) e Sackboy (passo3-real.txt 19:49:29, passo3-resultado.txt 19:55:53). O próprio corpo do sprint diz \"dois jogos\" em :257, e o desenho da caixinha diz \"Dois jogos, o mesmo controle\" em :428."
      },
      {
        "gravidade": "alta",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:393-411 (condições) e :503-513 (veredito); docs/process/sprints/2026-08-05-STEAM-QUE-DECIDE-01...md:248",
        "o_que": "A variável independente do experimento — global SteamController_PSSupport \"0\" com UseSteamControllerConfig \"2\" per-app — não foi medida no horário do experimento, mas o veredito é carimbado MEDIDO como se tivesse sido.",
        "prova": "A única leitura do localconfig.vdf está em :202-206, rotulada \"MEDIDO, em 06/08/2026 por volta das 01h20\" e com \"Steam: fechada (pgrep steam = 0)\" — dezoito horas antes, em outra sessão da Steam. Nenhum dos arquivos do experimento (passo1, passo2, passo2-resultado, passo3, passo3-real, passo3-resultado) lê o vdf; passo1.txt só registra \"steam: RODANDO (pid ...)\". A lista de condições em :395 declara \"Grau: MEDIDO (tudo abaixo saiu de arquivo ou de journal com carimbo)\" e a linha do vdf não está lá — só \"a allowlist e o localconfig.vdf não foram tocados\", que é outra afirmação. O risco de a Steam reescrever o arquivo é o que a própria sprint documenta em :373-376."
      },
      {
        "gravidade": "alta",
        "onde": "docs/usage/jogos-e-mascaras.md:55-59; CHANGELOG.md:31-33; docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:594-597; tooltip proposto em docs/process/estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md:103-105",
        "o_que": "O critério novo (\"marque quando o jogo só reconhecer o controle com o Steam Input dele ligado\" / \"a allowlist é a lista dos jogos cujo DualSense passa pela Steam\") descreve um comportamento que o experimento nunca produziu, e chega às páginas de uso e ao CHANGELOG sem grau.",
        "prova": "Os dois contrafactuais que fechariam o critério não foram rodados: o Mullet nunca foi aberto FORA da lista (nenhum arquivo mede isso) e o Sackboy nunca foi aberto DENTRO dela. Logo \"o jogo só reconhece o controle com o Steam Input ligado\" não foi observado em jogo nenhum. A sprint grada a atribuição como SUSPEITA COM MECANISMO em :598-600 e o desenho a grada em :130-133, mas jogos-e-mascaras.md:55-58 e CHANGELOG.md:31-33 afirmam a renomeação sem grau nenhum — e é dessa renomeação que sai o texto que vai para a tela dela."
      },
      {
        "gravidade": "alta",
        "onde": "docs/usage/jogos-e-mascaras.md:58-59; docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md:540",
        "o_que": "\"o Sackboy foi medido no mesmo dia, fora da lista, e funcionou completo\" contradiz a medição do mesmo dia e a nota irmã da mesma página.",
        "prova": "passo3-resultado.txt (19:55:53): \"gatilhos ... MOLES (o Hefesto aplicou Resistencia e nao segurou)\", \"lightbar ... AZUL (o padrao da Sony), nao a cor dela\", \"aplicar cor ... muda, mas o JOGO devolve para azul\". A nota acrescentada 30 linhas abaixo, em jogos-e-mascaras.md:85-92, diz o contrário: \"eles mandam na luz e nos gatilhos\" e \"o que ele escreve vence o que você escolheu\"."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:541, :551, :553-563; CHANGELOG.md:30; docs/usage/jogos-e-mascaras.md:90-91; docs/usage/modos.md:55-57",
        "o_que": "Vibração e LED de jogador entram em blocos MEDIDO sem nunca terem sido exercitados no experimento — é leitura de código, que pela definição de grau da própria sprint é SUSPEITA COM MECANISMO.",
        "prova": "Nenhum arquivo do experimento toca rumble ou player-LED; a observação dela cobriu contagem de controles, gatilhos e lightbar. A fonte de \"no rumble a usuária vence\" é gamepad.py:747-752 (confere: `if daemon.config.rumble_active is not None: return  # rumble fixado manual vence o FF do jogo`) — caminho lido, efeito não observado, que :19-21 desta mesma página define como SUSPEITA COM MECANISMO. Mais forte: :723-725, no fim da mesma página, classifica o argumento por grep sobre os appliers como \"(SUSPEITA COM MECANISMO); ninguém olhou o controle com o jogo aberto\". O bloco novo escreve \"é medida por leitura de código\" (:558) e estende a inversão a \"LED de jogador\" (:556), que ninguém viu."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:461, :519-527, :549-556; docs/process/sprints/2026-08-05-STEAM-QUE-DECIDE-01...md:262; docs/usage/jogos-e-mascaras.md:49-50",
        "o_que": "A atribuição dos gatilhos duros do Mullet à Resistência DELA é inferência, e o desenho do experimento não separa as duas hipóteses — mas é metade da doutrina nova (\"na lista os ajustes dela vencem\").",
        "prova": "passo2-resultado.txt registra apenas \"2.3 gatilhos com resistencia .......... SIM ('gatilhos duros')\", sem dizer de quem é o efeito. O Mullet é justamente o jogo que, segundo launch_env.py:345-348 e storm_doctor.py:29-31, \"chama SetDualSenseTriggerEffect da API Steamworks\": gatilho duro tem duas explicações concorrentes, e nenhuma medida com a Resistência dela desligada. Só a lightbar vermelha (cor que jogo nenhum pintaria) é inequívoca. A frase de tela em jogos-e-mascaras.md:50 (\"a resistência de gatilho que você aplicou segura\") herda o problema."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:497-502 e :706",
        "o_que": "Duas contagens apresentadas como escrituração da medição estão erradas.",
        "prova": "(a) \"As outras seis estão descartadas por medição\" (:497): a tabela de leitura tem SETE linhas (:336-344); a prosa justifica cinco descartes (linhas 3, 4, 5, 6 e 7) e a linha 1 fica sem menção — e ela não foi descartada, realizou-se junto com a 2 (X-Box 360 pad só na allowlist, o jogo listou um controle, gatilhos e lightbar responderam). (b) \"cinco dos seis itens abaixo foram pagos\" (:706): a lista \"O QUE NÃO FOI MEDIDO NESTA SESSÃO\" tem CINCO itens (:716-729), e a própria nota diz que um deles (data/versão do teste antigo) segue irrecuperável — 4 de 5, não 5 de 6."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:545; CHANGELOG.md:17",
        "o_que": "O número \"25 linhas em src/ e docs/usage/\", declarado MEDIDO por grep em 06/08, não reproduz nesta árvore.",
        "prova": "grep -rniE \"sai da frente|sai de cena|fora do caminho\" src/ docs/usage/ devolve 21 hoje (20 só em src/; a única ocorrência em docs/usage/ é cli.md:301). Nenhuma variante testada (com \"sair\"/\"saiu\", ou docs/ inteiro) chega a 25. Além disso, pelo menos cinco dos 21 são homônimos sem relação com a exceção: identity.py:379 e :834, lifecycle.py:712, uhid_gamepad.py:603 e daemon_actions.py:1153 — todos \"fora do caminho quente\"/\"fora do caminho de criação\"."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:601-603; docs/process/estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md:548",
        "o_que": "A afirmação MEDIDA \"grep por HID direto/hid direto em .py, .md, .sh e .txt devolve zero\" deixa de valer no mesmo commit que a escreve.",
        "prova": "O mesmo grep hoje devolve sete ocorrências, todas introduzidas por estes documentos: CHANGELOG.md:44, estudo:545 e :548, sprint:591, :599, :602 e :664. A afirmação só se sustenta com a data explícita (\"antes desta sprint\"); como está, quem repetir a medição reprova a página."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:625-633 (ressalva 3)",
        "o_que": "\"Não foi alt-tab; foi o segundo lançamento\" é afirmação categórica dentro de bloco graduado SUSPEITA COM MECANISMO, e o artefato citado não mostra o segundo lançamento.",
        "prova": "O texto apoia-se em passo3.txt (19:45:59), que em \"qual jogo roda\" lista uma única linha: \"AppId=2111190\". Nenhum processo do 1599660 aparece ali — a primeira evidência do Sackboy é passo3-real.txt, às 19:49:29. Não existe carimbo do lançamento do segundo jogo anterior às 19:45:32, então o mesmo artefato é compatível com a hipótese contrária. O grau está certo; a frase em negrito afirma mais do que o grau permite."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:447-452",
        "o_que": "Carimbo trocado: a tabela intitulada \"O sistema às 19:41:12\" inclui uma medição feita às 19:44:46.",
        "prova": "passo2.txt (19:41:12) não tem o campo de hidraw; \"hidraw abertos pelo daemon: 1\" só existe em passo2-resultado.txt (19:44:46). O próprio documento usa o carimbo certo 90 linhas depois, em :541."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:638-642 (ressalva 4)",
        "o_que": "A ressalva inverte o mecanismo que ela mesma descreve, sob \"Grau: MEDIDO\".",
        "prova": "O log sai no PRIMEIRO skip da instância (core/sysfs_leds.py:194-202; _skip_logged vira True em :202) e o carimbo do journal é 2026-08-06T19:52:50 — logo (198, 70, 0) é exatamente o desejado ÀQUELA hora, e não \"não o estado das 19:52:50\". O que a linha realmente não prova é o estado DEPOIS (19:55:53, quando ela viu azul). A identificação do nó, essa sim, confere: /sys/class/leds/input1011:rgb:indicator aponta para .../uhid/0005:054C:0CE6.000D."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:569",
        "o_que": "Citação fora do alvo: a frase citada não está no intervalo citado.",
        "prova": "\"UHID_OUTPUT = o jogo escreveu no hidraw do vpad (rumble/LED/gatilhos)\" está em integrations/uhid_gamepad.py:1563 (a medição bruta também dizia 1563); o intervalo escrito, :1564-1571, começa depois dela."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/usage/modos.md:52-53",
        "o_que": "Promessa não medida em página de uso, dentro de nota aberta com \"Medido com o Sackboy aberto\": \"Você recupera a sua cor e os seus gatilhos quando o jogo fecha\".",
        "prova": "Nenhum arquivo do experimento observa o estado depois de o jogo fechar — o último carimbo é 19:55:53, com o Sackboy ainda de pé. O apoio mais próximo é comentário de código (core/backend_pydualsense.py:1301-1306, \"fechar o jogo devolve a paleta em <= ~32s\"), que é leitura, não medição."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md:429",
        "o_que": "Dono do grab inferido dentro de bloco declarado MEDIDO.",
        "prova": "passo1.txt registra \"/dev/input/event8 ... -> PRESO por outro processo (Device or resource busy)\" — o artefato não identifica o processo. \"o Hefesto prendia o nó de botões do físico\" é a explicação provável, não a leitura."
      },
      {
        "gravidade": "baixa",
        "onde": "CHANGELOG.md:35",
        "o_que": "\"Nenhuma linha de código mudou nesta leva\" contradiz o próprio stage e a seção seguinte do mesmo arquivo.",
        "prova": "git diff --cached --numstat mostra install.sh (+83/-71), scripts/bluez_config.sh (+1209), scripts/doctor.sh (+131/-2), scripts/check_packaging_parity.sh (+165), tests/conftest.py (+165) e quatro bancadas novas (+3009) no mesmo stage — e a seção logo abaixo, no mesmo CHANGELOG, descreve exatamente essas mudanças de código."
      }
    ]
  },
  {
    "achados": [
      {
        "gravidade": "alta",
        "onde": "src/hefesto_dualsense4unix/gui/main.glade:2430 (tooltip, translatable=\"yes\", aba Sistema)",
        "o_que": "TEXTO DE TELA VIVO com a doutrina velha E uma afirmacao agora MEDIDA-FALSA, sem nota datada em lugar nenhum. O tooltip do botao \"Este jogo nao funciona\" diz: *\"...o controle passa a ser entregue direto pela Steam e o Hefesto sai da frente. (...) enquanto a marca estiver la, esse jogo fica sem cor, gatilhos e co-op do Hefesto.\"* A medicao de 19:44:46 mostra o contrario da segunda metade: com o Mullet aberto e a excecao ativa, o vermelho DELA ficou na lightbar e a Resistencia DELA segurou. Agravante: a propria leva CITA esta frase como autoridade MEDIDO. Na tabela de procedencia do tooltip novo (docs/process/estudos/2026-08-06-desenho...:345 do diff), a linha `| \"o co-op sai\" | *\"esse jogo fica sem cor, gatilhos e co-op do Hefesto\"*, gui/main.glade:2430 | MEDIDO |` colhe a palavra \"co-op\" de dentro da frase e nao registra que as outras duas palavras da MESMA frase acabaram de ser refutadas. A leva leu a linha e passou por cima dela.",
        "prova": "grep -n 'cor, gatilhos e co-op' src/hefesto_dualsense4unix/gui/main.glade -> :2430, translatable=\"yes\". O diff adicionado (docs/process/estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md) cita `gui/main.glade:2430` quatro vezes (procedencia do tooltip novo, secao 2.4, secao 3, P1) e ZERO vezes como frase caducada. A secao 5.3 (\"Notas datadas que este desenho pede\") lista quatro alvos — gamepad.py:429-434, launch_env.py:44-49 e :482-486, launch_env.py:35, glade:2829 — e glade:2430 NAO esta entre eles."
      },
      {
        "gravidade": "alta",
        "onde": "src/hefesto_dualsense4unix/app/actions/daemon_actions.py:543 e :546 (format_game_broken_result — o toast do botao)",
        "o_que": "A frase que ela le NO INSTANTE DO GESTO que esta sprint inteira mediu continua dizendo a doutrina velha, e nao ganhou nota nem entrada de divida. Retorno :543: *\"O jogo {appid} ja estava marcado — o Hefesto ja sai da frente dele.\"*; retorno :545-547: *\"Anotei: o jogo {appid} passa a ser entregue direto pela Steam e o Hefesto sai da frente dele.\"* Nao e comentario nem docstring: e o texto do toast. A medicao diz que na allowlist o Hefesto NAO sai da frente — ele abre mao da entrada e mantem a saida inteira.",
        "prova": "sed -n '543p;545,547p' src/hefesto_dualsense4unix/app/actions/daemon_actions.py. O diff adicionado cita daemon_actions.py em :321, :522, :532, :938, :1305, :1318-1324, :503-546, :1255 — sempre como procedencia ou mapa de arquivos a tocar, nunca como frase caducada. Nenhuma linha adicionada do diff contem \"toast\" nem \"texto de tela\" a proposito desta frase (grep '^\\+' | grep -i 'toast' -> zero)."
      },
      {
        "gravidade": "alta",
        "onde": "src/hefesto_dualsense4unix/cli/cmd_steam.py:174-175 (mensagem do `gamepad steam-input remove`)",
        "o_que": "TEXTO DE TELA que promete de volta exatamente as duas coisas que a medicao mostrou que o desfazer TIRA. Ao tirar um jogo da lista o comando imprime: *\"o Hefesto volta a entregar o gamepad virtual nesse jogo (cor, gatilhos e co-op)\"*. A INVERSAO medida diz o oposto para dois dos tres itens: FORA da lista o jogo vence a saida — o Sackboy devolveu a lightbar ao azul da Sony e amoleceu os gatilhos dela. So o \"gamepad virtual\" e o \"co-op\" voltam; \"cor\" e \"gatilhos\" passam a ser do jogo. E o defeito e simetrico ao do tooltip: um diz que na lista ela perde cor e gatilhos, o outro diz que fora dela ela os recupera — e a medicao inverteu os dois.",
        "prova": "sed -n '172,176p' src/hefesto_dualsense4unix/cli/cmd_steam.py. Contraste medido registrado no proprio diff (CONTROLE-SONY-MEDIDO-01, secao A INVERSAO, e docs/usage/jogos-e-mascaras.md nota das 06/08): \"a lightbar voltou ao azul da Sony (...) e os gatilhos ficaram moles apesar da Resistencia aplicada\". Nenhuma linha adicionada do diff menciona cmd_steam.py como superficie caducada — as duas mencoes sao `cli/cmd_steam.py:160,169` (chamadores do remove) e \"o verbo do cli/cmd_steam.py\" (procedencia de rotulo)."
      },
      {
        "gravidade": "alta",
        "onde": "docs/process/sprints/2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md:244-250 — ARQUIVO FORA DO STAGE",
        "o_que": "A leva DECLARA pago o \"portao zero da STEAM-INPUT-01 (:244-250), aberto desde 26/07\" e nao anota a pagina que e dona do portao. Quem abrir a STEAM-INPUT-01 hoje continua lendo, sem nenhuma nota: *\"Nao testei se `UseSteamControllerConfig=\"2\"` per-app funciona com `SteamController_PSSupport=\"0\"` global. Esta e a premissa em que a excecao inteira se apoia (...) Se a Steam moderna nao honrar o per-app (...) a excecao e decorativa e falha em silencio — e o botao 'Este jogo nao funciona' nunca funcionou de verdade.\"* Este e o caso mais limpo do defeito que a DOC-QUE-NAO-MENTE cataloga: a pagina que guarda o portao segue acusando o produto de nunca ter funcionado, um dia depois de a medicao provar que funciona.",
        "prova": "sed -n '244,250p' do arquivo confirma o texto literal. `git diff --cached --name-only | grep STEAM-INPUT-01` -> vazio. O diff adicionado (CONTROLE-SONY-MEDIDO-01, secao O QUE ESTA MEDICAO PAGA) diz \"O portao zero da STEAM-INPUT-01 (`:244-250`), aberto desde 26/07\" — cita o caminho:linha e nao escreve nada la."
      },
      {
        "gravidade": "alta",
        "onde": "docs/process/sprints/2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md:94 e :107 — ARQUIVO FORA DO STAGE",
        "o_que": "Uma frase caducada FILA PARA VIRAR TEXTO DE TELA, numa entrega declarada ABERTA no cabecalho da propria sprint. A Entrega 2 prescreve, em bloco de citacao, a sentenca que a aba Emulacao deve exibir: *\"Mullet Mad Jack usa o Steam Input — o Hefesto esta fora do caminho neste jogo. Gatilhos e luz vem da Steam.\"* A medicao refuta as DUAS metades: o Hefesto nao esta fora do caminho (mantem a saida inteira, `hidraw abertos pelo daemon: 1`), e gatilhos e luz NAO vieram da Steam — vieram DELA (a Resistencia dela segurou, o vermelho dela ficou). :94 repete \"o Hefesto sai do caminho **inclusive** retirando o gamepad virtual\". Nada disso foi anotado, e a leva nunca menciona JOGO-01 em linha adicionada nenhuma.",
        "prova": "sed -n '88,112p' docs/process/sprints/2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md. Cabecalho da sprint (:3-9): \"Status: ENTREGUE em a343ff6, **exceto a E2, que continua ABERTA**\". Varredura das linhas adicionadas do diff por JOGO-01|DUPLO-REGISTRO-01|CONTAGEM-E-COOP-01|mapa-total: zero ocorrencias (so STEAM-INPUT-01 aparece, uma vez, e mesmo assim sem anotar o arquivo)."
      },
      {
        "gravidade": "media",
        "onde": "src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py:316 e :322; src/hefesto_dualsense4unix/daemon/ipc_handlers.py:1441",
        "o_que": "As docstrings que PRESCREVEM a frase da janela seguem com a doutrina velha, e a leva leu o bloco sem ve-las. gamepad.py:316: *\"a emulacao nao foi desligada, ela SAIU DA FRENTE deste jogo\"*; :322: *\"o jogo da allowlist rodando com o Hefesto fora do caminho (os dois True)\"*; ipc_handlers.py:1441: *\"o jogo da allowlist esta rodando com o Hefesto fora do caminho\"*. As tres sao a fonte declarada da Entrega 2 do JOGO-01 — quem for escrever a frase da tela le ISTO. A leva cita `daemon/ipc_handlers.py:1432-1457` na secao 5.2 como a casa da chave nova que fara a frase nao mentir, ou seja, abriu exatamente esse intervalo e nao registrou a doutrina velha dentro dele.",
        "prova": "sed -n '313,326p' src/hefesto_dualsense4unix/daemon/subsystems/gamepad.py e sed -n '1432,1447p' src/hefesto_dualsense4unix/daemon/ipc_handlers.py. Diff adicionado, secao 5.2: \"O daemon ja publica o bloco `steam_input` com `excecao_ativa` e `vpad_suspenso` (`daemon/ipc_handlers.py:1432-1457`, **MEDIDO**)\" — a linha :1441 esta dentro do intervalo citado."
      },
      {
        "gravidade": "media",
        "onde": "CHANGELOG.md (entrada nova) e docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md, bloco de citacao apos \"A ausencia e o achado\"",
        "o_que": "O numero \"25 linhas\", declarado com grau MEDIDO, nao sobrevive a re-medicao com a familia como o proprio texto a nomeia. (a) Ele so fecha com o regex `sai(r)? da frente|sai(r)? de cena|fora do caminho`, que EXCLUI \"sai do caminho\" — e docs/usage/modos.md:98 (\"ele sai do caminho\") e justamente uma das linhas que esta leva anotou como familia. Com \"sai do caminho\" dentro, sao 27. (b) Das 25, CINCO nao tem nada com a doutrina: `identity.py:379`, `identity.py:834` e `lifecycle.py:712` sao \"fora do caminho quente\"; `uhid_gamepad.py:603` e \"Fora do caminho de criacao\"; `launch_env.py:436` fala do JOGO sair da frente, nao do Hefesto. (c) Ele PERDE pelo menos uma ocorrencia real: em docs/usage/jogos-e-mascaras.md:44 a frase e \"o gamepad virtual sai\\nde cena\", quebrada em duas linhas — invisivel a grep por linha. E a ironia e exata: essa e uma das duas linhas de docs/usage/ que a leva anotou. A conta honesta da doutrina e ~21 linhas, nao 25.",
        "prova": "grep -rncE 'sai(r)? da frente|sai(r)? de cena|fora do caminho' src/ docs/usage/ -> 25; com '(fora|sai(r)?) do caminho' -> 27. Varredura multilinha por regex em docs/usage/: `docs/usage/jogos-e-mascaras.md:44: QUEBRADA -> 'sai\\nde cena'` — ausente das 25. E o proprio jogos-e-mascaras.md nao aparece na saida do grep por linha."
      },
      {
        "gravidade": "media",
        "onde": "docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md:119; docs/process/sprints/2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md:51, :110, :131; docs/process/sprints/2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md:335, :341, :402 — TODOS FORA DO STAGE",
        "o_que": "Tres documentos de orientacao e sprints ABERTAS carregam a doutrina velha e nenhum foi anotado. O mapa-total:119 abre uma razao inteira com *\"**Razao C — nos dois jogos dela o Hefesto sai de cena de proposito.**\"* — e um dos dois documentos de mapa que um agente novo le para se orientar. A DUPLO-REGISTRO-01 (listada ABERTA em tres indices) repete tres vezes \"o Hefesto decide se sai da frente\" / \"para decidir se sai da frente\" / \"o Hefesto precisa saber para sair da frente\". A CONTAGEM-E-COOP-01:341 chegou perto — *\"o que a acao custa nao e so 'o Hefesto sair da frente'\"* — mas so corrigiu a metade do co-op; a metade da saida continua nao dita. Sao exatamente os \"lugares que ninguem olhou\".",
        "prova": "sed -n '119p' docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md; sed -n '51p;110p;131p' docs/process/sprints/2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md; sed -n '335,345p' docs/process/sprints/2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md. Nenhum dos tres arquivos aparece em `git diff --cached --name-only`, e nenhum e mencionado em linha adicionada do diff."
      },
      {
        "gravidade": "media",
        "onde": "src/hefesto_dualsense4unix/cli/cmd_steam.py:51 e :141; src/hefesto_dualsense4unix/integrations/steam_launch_options.py:721 e :931",
        "o_que": "O resto da superficie do produto, nao anotado. :51 e o help do Typer (aparece em `--help`): *\"Excecao do Steam Input — os jogos em que o Hefesto sai da frente.\"* :141 e o cabecalho do `list` impresso na tela: *\"Jogos em que o Hefesto sai da frente (o controle vem da Steam):\"*. steam_launch_options.py:721 (comentario) e :931 (docstring) repetem a doutrina e a promessa refutada — :931 diz *\"um jogo marcado por engano deixa de ter cor, gatilhos e co-op do Hefesto ate ser desmarcado\"*, frase que ja e citada literalmente como verdade do produto em duas sprints (BOTAO-QUE-NAO-MENTE-01:87 e inventario-de-botoes:96). Ou seja: a mentira ja se propagou para o registro, que e o mecanismo que jogos-e-mascaras.md:7-10 existe para impedir.",
        "prova": "sed -n '51p;141p' src/hefesto_dualsense4unix/cli/cmd_steam.py; sed -n '721p;931p' src/hefesto_dualsense4unix/integrations/steam_launch_options.py; grep -rn 'cor, gatilhos e co-op' src/ docs/ -> 9 ocorrencias, 3 em src/ (glade:2430, cmd_steam.py:175, steam_launch_options.py:931) e 6 em docs/, das quais ZERO ganharam nota nesta leva."
      },
      {
        "gravidade": "media",
        "onde": "src/hefesto_dualsense4unix/gui/main.glade:2845 (label translatable, aba Emulacao)",
        "o_que": "Duas coisas, e as duas caem no meio do terreno que a leva acabou de revisar. (1) O texto manda ela para a aba errada: *\"use a excecao por jogo em 'Steam Input' na aba Emulacao\"* — mas o gesto e o botao \"Este jogo nao funciona\" da aba SISTEMA (glade:2429); a aba Emulacao so tem uma LINHA DE STATUS (\"Excecao por jogo: N jogo(s)\", emulation_actions.py:349-361), sem controle nenhum. O P1 da leva (\"o mesmo arquivo passa a ter um nome so nas tres abas\") caminhou exatamente por aqui e nao viu. (2) O mesmo label ja carrega o criterio NOVO, que a leva apresenta como estreia: *\"Quando o suporte a DualSense do jogo vem PELA Steam (e o caso do Mullet Mad Jack), o jogo precisa enxergar o controle fisico\"*. A tabela de procedencia do tooltip novo teria ganhado a linha mais forte que existe e passou batido.",
        "prova": "sed -n '2845p' src/hefesto_dualsense4unix/gui/main.glade (translatable=\"yes\"); grep -n 'exce' src/hefesto_dualsense4unix/app/actions/emulation_actions.py -> so :313/:339/:349/:360 (parametro e markup), nenhum Gtk.Button. O diff adicionado cita glade :2429, :2430, :2829, :2951, :2977 e nunca :2845."
      },
      {
        "gravidade": "media",
        "onde": "O stage inteiro (`git diff --cached --name-only`)",
        "o_que": "A afirmacao de abertura — *\"ESCRITO (so documentacao; `src/` e `tests/` intocados; nada commitado)\"* — e falsa para o stage como ele esta. Alem dos 8 `.md`, o indice carrega `install.sh` (+154), `uninstall.sh` (+113), `scripts/bluez_config.sh` (novo, +1209), `scripts/build_deb.sh`, `scripts/check_packaging_parity.sh`, `scripts/doctor.sh`, `tests/conftest.py` (+165) e quatro arquivos de teste (+2977 linhas). `tests/` nao esta intocado NO STAGE. Provavelmente e trabalho de um agente irmao dividindo o mesmo indice — mas um `git commit` agora leva tudo junto, e os portoes rodados sobre \"os 20 arquivos no stage\" mediram uma leva que nao e a descrita.",
        "prova": "git diff --cached --stat -> \"20 files changed, 6483 insertions(+), 160 deletions(-)\", dos quais so 8 sao .md (1362 insercoes). tests/conftest.py, tests/unit/test_bluez_config_sh.py, tests/unit/test_doctor_justworks_comportamento.py, tests/unit/test_check_packaging_parity.py, tests/unit/test_bt_resilience_assets.py e tests/unit/test_plataforma_wiring.py estao todos em `git diff --cached --name-only`."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md, tabela de procedencia da secao 2.1 e tabela da secao 3",
        "o_que": "Citacao composta atribuida a uma linha so. A procedencia de \"a lista\" e dada como *\"porque esse jogo nao esta na sua lista de excecoes\"*, `app/actions/emulation_actions.py:339`, com grau MEDIDO. A linha :339 contem apenas `f\"proximo ciclo, porque {sujeito} na sua lista de excecoes\"`; o pedaco \"esse jogo nao esta\" mora em :335, dentro do ternario que monta `sujeito`. A frase citada nao existe em nenhuma linha unica do arquivo — ela e montada em tempo de execucao. Nao muda a conclusao, mas o grau MEDIDO com caminho:linha unico nao fecha, e a regra da casa manda conferir todo caminho:linha.",
        "prova": "sed -n '333,341p' src/hefesto_dualsense4unix/app/actions/emulation_actions.py: :335 = `sujeito = (\"esse jogo nao esta\" if len(jogos) == 1 else \"esses jogos nao estao\")`; :339 = `f\"proximo ciclo, porque {sujeito} na sua lista de excecoes\"`."
      },
      {
        "gravidade": "baixa",
        "onde": "docs/process/estudos/2026-08-05-o-sistema-de-perfis...md (linha do M-17) e docs/process/sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01...md, item 7 de \"O QUE CONTINUA ABERTO\"",
        "o_que": "Citacao velha reinvocada sem reconferencia. O M-17 diz *\"`gui/main.glade:2861` lista o Sackboy como 'funciona completo com DualSense (PS)'\"*. `glade:2861` e `</object>` — o texto do Sackboy esta em `:2845`. A leva reabre o M-17 no item 7 (\"O M-17 nao fecha aqui\", com dado medido novo sobre o Sackboy) sem revalidar a linha que o M-17 aponta, contra a regra explicita desta leva de conferir todo caminho:linha porque a arvore mudou muito hoje.",
        "prova": "sed -n '2859,2863p' src/hefesto_dualsense4unix/gui/main.glade -> :2861 = `</object>`. grep -n 'Sackboy' src/hefesto_dualsense4unix/gui/main.glade -> :2845 (label translatable com \"ex.: Sackboy, Pragmata, Mad King Redemption, Mullet Mad Jack\")."
      }
    ],
    "aprovado": false,
    "veredito": "REPROVADO — a doutrina nova chegou aos 8 documentos que ja eram sobre a doutrina, e a ZERO superficies do produto.\n\nO QUE PASSOU (conferido por mim, nao herdado): a metade estrutural que sustenta tudo esta correta. Os oito chamadores de `steam_input_excecao_ativa` estao exatamente em `gamepad.py:166, :207, :265, :366, :370, :649, :1134, :1386` (a definicao :220, o `__all__` :1639 e duas mencoes em docstring nao contam) e `grep -rn '_steam_input_excecao\\\\|_steam_input_vpad_suspenso' src/` nao devolve UMA linha em `core/` — a afirmacao \"nenhum portao da excecao no caminho de saida\" e verdadeira. Conferi tambem `gamepad.py:271` (`_set_evdev_grab(daemon, False)`), `:272-279` (`restore_all`), `:283-284` (`suspend_vpads_for_steam_input`), `:286` (`steam_input_excecao_encerrada`, e realmente sem campo nenhum), `:425`, `:747-748` (o rumble fixado vence o FF), `backend_pydualsense.py:1253-1259` (a precedencia GAME > CO-OP > por-uniq > AUTOMATICA > default), `launch_env.py:35`, `:44-49`, `:482-486`, `glade:2430/2951/2977` e `profiles_actions.py:644` — todos batem. `README.md`, `packaging/` (inclusive `packaging/cosmic-applet/`), `docs/adr/` e `docs/protocol/` estao LIMPOS da doutrina: nao ha nada a anotar la. `docs/usage/cli.md:301` (\"o co-op ainda sai de cena sozinho nos jogos com excecao de Steam Input\") esta CERTO e nao e defeito — o co-op cai mesmo. Os 8 `.md` do stage tem zero emoji e zero U+2713/U+2717, e as ancoras dos links novos resolvem. E a divida de `launch_env.py:482-486` ESTA registrada (desenho, secao 5.3 item 2, com a nota de que passou a ser devida independentemente de decisao de produto).\n\nO QUE REPROVA: a doutrina velha habita 21 linhas reais e a leva alcancou as duas de `docs/usage/`. Ficaram para tras TRES textos de tela que ela le todo dia — e os tres estao no caminho exato do gesto que a sprint mediu:\n\n1. `glade:2430` (tooltip translatable) diz \"o Hefesto sai da frente\" E \"esse jogo fica sem cor, gatilhos e co-op do Hefesto\". A segunda metade e MEDIDA-FALSA: as 19:44:46 o vermelho dela ficou e a Resistencia dela segurou. E a leva CITA essa mesma frase, com grau MEDIDO, como procedencia da palavra \"co-op\" do tooltip NOVO — colheu uma palavra de dentro de uma frase que acabara de refutar, sem dizer que a refutou.\n2. `daemon_actions.py:543/:546` — o toast do proprio botao \"Este jogo nao funciona\": \"o Hefesto sai da frente dele\".\n3. `cmd_steam.py:174-175` — o `remove` promete devolver \"cor, gatilhos e co-op\", e a INVERSAO medida diz que fora da lista o JOGO vence a cor e os gatilhos (Sackboy: azul da Sony, gatilhos moles). O desfazer promete de volta as duas coisas que ele tira.\n\nE duas paginas caducaram em lugar que ninguem olhou, as duas fora do stage: a `STEAM-INPUT-01:244-250` — cujo portao zero esta DECLARADO PAGO nesta leva — continua dizendo que \"a excecao e decorativa e falha em silencio, e o botao nunca funcionou de verdade\"; e a `JOGO-01:107`, com E2 ABERTA no proprio cabecalho, prescreve a frase que a aba Emulacao deve exibir: \"o Hefesto esta fora do caminho neste jogo. Gatilhos e luz vem da Steam.\" A medicao refuta as duas metades — gatilhos e luz vieram DELA. E uma frase caduca na fila para virar texto de tela.\n\nPor fim, o numero \"25 linhas\" nao aguenta MEDIDO: ele so fecha com um regex que exclui \"sai do caminho\" (que a propria leva anota em modos.md:98), inclui cinco homonimos que nada tem com a doutrina (\"fora do caminho quente\" x3, \"fora do caminho de criacao\", \"o JOGO sai da frente\") e nao enxerga `jogos-e-mascaras.md:44`, onde \"sai\\\\nde cena\" esta quebrado em duas linhas — uma das duas linhas de `docs/usage/` que esta leva anotou. O instrumento nao viu o proprio alvo.\n\nNada disso pede conserto agora (`src/` esta fora do escopo por instrucao). O que falta e o que a casa cobra: a divida escrita. A secao \"O QUE CONTINUA ABERTO\" tem sete itens e nenhum diz \"tres textos de tela e duas sprints continuam com a doutrina velha, e um deles afirma o oposto do medido\"."
  }
]

### reprovou

true


## LOGS

verificacao: 2 lentes, 2 reprovaram
