# MIC-BT-DONO-01 — a posse do mudo ganha dono e ciclo de vida

- **Status:** PROPOSTA, escrita em 03/08/2026 **depois da medição no hardware**
- **Prioridade:** ALTA
- **Faixa:** 1 — o produto perde a configuração dela sozinho
- **Causa-raiz:** **PROVADA e MEDIDA** (o bit cedeu a uma ordem nossa, e voltou)
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Evidência:** [a noite em que o microfone do Bluetooth voltou](../estudos/2026-08-03-a-noite-em-que-o-microfone-do-bluetooth-voltou.md)
- **Ordem:** executar **depois** da
  [LED-SEM-DONO-01](2026-08-03-LED-SEM-DONO-01-o-common8-ganha-dono-e-os-textos-param-de-mentir.md)
  — sem ela, o LED não serve de instrumento e o aceite do E4 nasce inválido

---

## O VEREDITO — leia antes de tudo

> **Isto NÃO é "a cura do microfone por Bluetooth".** É a cura de um **defeito de
> posse**.

`_mic_mute_desejado` é atributo de instância do `_PinnedPyDualSense`
(`core/backend_pydualsense.py:476`). O handle é **recriado a cada reconexão**, e
o `_reapply_desired` (`:2111-2138`) só re-pendura os `_OUTPUT_FIELDS` e os blocos
crus de gatilho. **Um `mic unmute` evapora no próximo handle novo, em silêncio**,
e o firmware — que retém o mudo — volta a `0x04`.

É exatamente isso que o log medido em 03/08 descreve: `mudo = 100% → 46% → 100%`.

### Duas honestidades que a sprint tem de carregar

**1. O `BT-MIC-GATING-01` continua ABERTO.** O regime que esta cura restaura é o
mesmo que produziu as medições de `integrations/dualsense_bt_audio.py:100-101`
(*"entre 55% e 75% de MUDO… ~40% do sinal"*), feitas em `43d0f0a` (25/07, 02:08)
com o daemon mandando `common[9]=0x00` na cadência do keepalive.

> **O alvo previsto é 55-75% de mudo, não 0%.** Prometer 0% é prometer o que a
> casa já mediu como não obtido com o mic no ar.

**2. A reafirmação é a 2 Hz, não a ~125 Hz.** O `_build_common` não decide quando
se escreve: o `sendReport` deduplica (`:529-535`) e, com o desejado constante, o
report é idêntico — sobra o `OUT_REPORT_KEEPALIVE_SEC = 0.5` (`:228`). Medido em
`tests/unit/test_audio_owner_report.py:12-21` (9 transições em 2 s). **A
diferença entre esta cura e um pulso no `iniciar()` é de CONTINUIDADE — a posse é
reafirmada para sempre, inclusive em handle novo —, não de latência.**

---

## As entregas

### E1 — a posse por-uniq, com camadas, FORA do `_DesiredOutput`

**O que muda:** mapa novo `_mic_mute_by_uniq: dict[str, dict[str, bool]]` ao
lado de `_desired_coop_by_uniq` (`core/backend_pydualsense.py:861`), com duas
camadas: **`usuaria` > `ponte_bt`**. Ausência das duas = `None` = **o kernel é o
dono**. Um aplicador único resolve e chama `handle.set_microphone_mute(...)`
(`:566-581`).

**Por que FORA do `_DesiredOutput` — e a razão que NÃO vale.**

Não use o argumento *"o autoswitch ativa perfil a cada troca de janela"*:
`mic_led` **já está** em `_OUTPUT_FIELDS` (`:317`) e mesmo assim o mic nunca é
colateral de perfil, porque o perfil não define o campo
(`profiles/schema.py:441`; `core/led_control.py:38-44,181`).

As duas razões que valem:

1. **`None` no `_DesiredOutput` significa "herda de baixo"** (`_merge_desired`,
   `:348`, `:370`) — e no mudo `None` é a **ORDEM** *"devolvo ao kernel"*. A
   lição já está escrita em `:2503-2510`;
2. **o precedente exato é o co-op** (`:336`): transitório, com revert que precisa
   reencontrar o padrão intacto embaixo.

**Impedimento mecânico:** `_prune_overrides_locked` varre `_OUTPUT_FIELDS`
(`:1300`).

**A precedência, derivada do R-20** (`:319-331`): **a ponte não desmuta por cima
da usuária.** Se ela mandou `mic mute`, subir a ponte não desfaz — registra
recusa em log. *Um programa que desmuta o microfone de alguém por conta própria
é o que `daemon/subsystems/bt_mic.py:8-13` se proíbe de fazer.*

**Muda a fonte de verdade:** `microphone_mute_for` (`:2491-2518`) hoje lê
`getattr(handle, "_mic_mute_desejado")` e passa a ler o mapa resolvido — senão
responde `None` na janela pós-hotplug e para controle desconectado. É ela que
alimenta o `state_full` (`daemon/ipc_handlers.py:2184`) **e** o ramo do botão do E4.

**Aceite:** com a ponte de pé e `mic mute` da usuária, o resolvido é `True`; sem
camada nenhuma, `microphone_mute_for` devolve `None` e o `flag1 0x02` sai
apagado.

**Teste que morde:** `test_a_ponte_nao_desmuta_por_cima_da_usuaria` — arranque a
precedência e a ponte desmuta o microfone dela sozinha; o teste reprova.

**Armadilha nomeada — o pseudo-MAC:** casar ponte→controle por `_key_to_uniq`
(`:3237-3251`), **com a guarda de 12 hex**. Sem `HID_UNIQ` (caso real,
`dualsense_bt_audio.py:334-341`) **não se reivindica nada e se loga** — e o custo
é honesto: naquele controle o mic **continua mudo**. Sem a guarda, o pseudo-MAC
leva a posse ao controle errado.

### E2 — a reconexão reassume (a cura de raiz)

**O que muda:** em `_reapply_desired` (`:2128-2136`), ao lado do laço que
re-pendura `_raw_trigger_*` — **o precedente exato deste padrão** —, re-pendurar
o mudo **resolvido** no handle novo. **Fora** de `_write_partial_output`
(`:2140`), que é o aplicador do `_DesiredOutput`.

**Por que `new_handles` (`:1657`) basta:** handle novo nasce com o registrador
`None` (é o caso quebrado); handle **reusado** após queda de link conserva o
atributo e o próximo report já reafirma sozinho.

**Aceite:** derrubar o Bluetooth e religar, **sem tocar em nada** — o bit
`STATUS_MIC_MUDO` do byte de estado volta a zero em ≤1 tique de hotplug.

**Teste que morde:** `test_posse_do_mudo_sobrevive_ao_handle_novo`, assertando
**no report do handle B**:
`common[1] & VALID_FLAG1_POWER_SAVE_CONTROL_ENABLE != 0` **E** `common[9] == 0x00`.
Arranque a linha do `_reapply_desired` e o bit sai apagado.

> **Assertar o byte, nunca o atributo — e os DOIS asserts.** `common[9] == 0`
> sozinho **passa com a cura arrancada**.

**Armadilha nomeada — o irmão não curado:** `_volumes_audio` (`:482`) e
`_preamp_audio` também morrem com o handle e **não** estão no `_reapply_desired`.
**Não entregue junto**; registre por escrito que o volume do alto-falante some no
próximo drop de BT pelo mesmo mecanismo.

### E3 — o contrato de posse no fio

**O problema medido:** com a ponte de pé, a camada `usuaria` está vazia; o `null`
que a GUI manda remove nada, o resolvido continua `False`, e o botão **"Devolver
o botão físico"** (`tests/unit/test_mic_captura_e_botao.py:241-251`) não faz
nada — **e `test_o_clique_com_posse_nossa_devolve_o_botao_fisico` (`:348-357`)
continua verde**, porque asserta só o payload. É teste que passa com a cura
arrancada.

**O que muda:**
1. campo novo `mic_posse: "kernel"|"ponte"|"usuaria"` em `audio_status_for`
   (`:2254`) e no `state_full` (`ipc_handlers.py:2149-2186`);
2. `_handle_mic_set` (`ipc_handlers.py:3047`) devolve o **resolvido**, não o eco
   `{"mic_mudo_desejado": muted}`;
3. a GUI decide o rótulo por `mic_posse` — três valores para quatro estados não
   fecha.

**Aceite:** com a ponte de pé e sem camada da usuária, `mic_posse == "ponte"` e a
GUI **não** oferece "Devolver o botão físico".

**Teste que morde:** reescrever o teste acima para assertar o **efeito** (a posse
resolvida depois do clique), não o payload.

### E4 — o botão físico alcança todos os controles

**O que muda:**
1. `BUTTON_DOWN` passa a carregar o `uniq` do controle que emitiu
   (`daemon/lifecycle.py:3638`, hoje `{"button": name, "pressed": True}`) —
   campo **aditivo**, os consumidores atuais ignoram;
2. em `mic_button_loop` (`daemon/subsystems/hotkey.py:262-286`), **antes** da
   guarda `fonte_padrao_e_o_controle`: se a posse daquele `uniq` é nossa, o toque
   inverte **o nosso** valor e não toca no PipeWire; senão, cai no caminho de
   hoje, sem mudança.

**A decisão da BT-E-VPAD-01 fica de pé, e cite-a:** a opção **(b)** daquela
sprint (*"toma a posse e faz o botão físico parar de valer"*) **continua
recusada** — no cabo e no BT **sem ponte** a posse é `None`, o `flag1 0x02` sai
apagado e o botão é do kernel. O que se entrega aqui é a **(c)** do mesmo
documento, que **não foi recusada**.

**Por que E4 vem antes de E5:** sem o `uniq` no `BUTTON_DOWN`, a posse tomada
automaticamente no Controle 2 **desfaz o gesto físico dela em ≤0,5 s, em
silêncio** — que é a opção (b) recusada, entrando pela porta dos fundos.

### E5 — a ponte assume e devolve no ciclo de vida

Só depois de E3 e E4: `iniciar()` reivindica a camada `ponte_bt`; `parar()` a
solta. É a entrega que faz o `mic bt` funcionar **sem** o `mic unmute` manual.

### E6 — o CLI para de mentir por antecipação

Medido em 03/08: `mic unmute` imprimiu *"o controle declara MUDO"* porque releu
**antes de o firmware convergir** — e a mensagem manda a usuária para o
WirePlumber, que é o lugar errado. O hidraw cru, um segundo depois, mostrava
`0x00`.

**Aceite:** o comando ou espera a convergência, ou diz que não esperou.

---

## Testes que vão reprovar

```
pytest tests/unit -k "mic or audio_owner or hotkey or bt_mic"
```

## O que NÃO fazer

- **não prometer 0% de mudo** — o alvo medido é 55-75%, e o `BT-MIC-GATING-01`
  segue aberto;
- **não pôr o mudo no `_DesiredOutput`** — `None` ali significa "herda", e aqui
  significa "devolvo ao kernel";
- **não fazer a ponte desmutar por cima da usuária**;
- **não contradizer a recusa da BT-E-VPAD-01** (o botão do mic tomando a posse do
  firmware por padrão);
- **não entregar o `_volumes_audio` junto** — é o mesmo mecanismo, e misturar as
  duas curas confunde a medição.

## O que fica ABERTO

- **o `BT-MIC-GATING-01`** — por que o firmware mantém 55-75% de mudo com o mic
  no ar. Três hipóteses já foram refutadas por medição, e o "principal suspeito"
  (o daemon como segundo escritor) foi **eliminado em 03/08**;
- **quem repõe o mudo** depois que a posse é solta — medido que volta, não
  medido quem o repõe.
