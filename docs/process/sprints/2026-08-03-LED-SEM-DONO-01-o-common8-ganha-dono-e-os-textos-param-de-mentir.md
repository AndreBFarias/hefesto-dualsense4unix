# LED-SEM-DONO-01 — o `common[8]` ganha dono, e os textos param de mentir

- **Status:** PROPOSTA, escrita em 03/08/2026
- **Prioridade:** ALTA — e por um motivo que não é o tamanho do defeito: **ela é
  pré-requisito de ACEITE das outras duas sprints do microfone**
- **Faixa:** 2 — o produto destrói a própria evidência
- **Causa-raiz:** **PROVADA no código**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Ordem:** **PRIMEIRA** das três do microfone. Enquanto o `common[8]` sair
  forçado a zero com autoridade, *"o LED está apagado"* não prova nada — e
  qualquer aceite que use o LED como evidência **nasce inválido**

---

## Por que ela vem primeiro

Durante a investigação de 03/08, o assistente perguntou à mantenedora se o LED do
botão de microfone estava aceso. Ela respondeu que **não**. A resposta foi usada
como evidência de que o botão físico não estava mutado.

**Aquela resposta não podia significar nada** — porque **nós forçamos o LED
apagado em todo report**. A pergunta era inútil, e ninguém sabia.

É a definição de instrumento quebrado: **o produto destrói a evidência que a
investigação precisa.**

## A prova, curta

`core/backend_pydualsense.py:690` liga
`flag1 = 0x01 | 0x02 | 0x04 | 0x10 | 0x40`.

O `0x01` (`VALID_FLAG1_MIC_MUTE_LED_CONTROL_ENABLE`,
`core/ds_output_report.py:162`) **não é limpo em ramo nenhum**:

- `:698-699` limpa o `0x02`;
- `:706-716` limpa `0x04|0x10` sob `_suppress_leds`;
- `:724-729` limpa o `0x80`;
- **o `0x01`, nunca.**

> ### **EXECUTE ESTA PRIMEIRO — ela DESBLOQUEIA uma medição.**
>
> Enquanto o daemon forçar `common[8] = 0` em todo report, **o LED do microfone não serve de instrumento** e a medição A2 do protocolo não pode ser feita. Uma pergunta a ela já foi gasta assim, em 03/08.


E `:732` escreve `common[8] = int(self.audio.microphone_led)` **sem `if`** — ao
contrário do mudo, que é condicional em `:735-737`. O default da biblioteca é
zero (`pydualsense.py:882`). Herdado verbatim em `b4589a1` (19/07).

**O kernel trata os dois como gêmeos:** um bloco só, one-shot na borda do botão
(`assets/dkms/hid-playstation/hid-playstation.c:1499-1516`, armado em
`:1592-1601`) — e **nunca lê** `DS_STATUS1_MIC_MUTE` (`:154`, definido e sem uso).

## A cura é "escrever com dono", não "parar de escrever"

Só parar deixaria `mic.set muted=true` **mutando o firmware sem acender o LED** —
o controle continuaria mentindo, agora por omissão.

---

## As entregas

### E1 — o campo de posse e o builder condicional

**O que muda:** `_mic_led_desejado: bool | None = None` ao lado de
`_mic_mute_desejado` (`:476`). A linha `:732` deixa de ser incondicional e vira
irmã de `:735-737`:

- `None` → limpa o `0x01` e deixa `common[8]` inerte;
- `True`/`False` → mantém o bit e escreve `1`/`0`.

Ler por `getattr` — o `__new__` dos testes não passa pelo `__init__`
(`tests/unit/test_audio_owner_report.py:38-55`).

**O comentário tem de dizer quem é o dono, e com precisão:** o dono **em regime**
é o **FIRMWARE**, que retém; o kernel é escritor **ocasional**, na borda do botão.
Escrever *"o dono é o kernel"* replanta em código a ambiguidade que custou o dia
de hoje.

**Não estender `_suppress_leds` ao `0x01`:** lightbar e player-LEDs têm classe LED
no sysfs (`hid-playstation.c:233`, `:252`) e há a quem deferir; o
`mute_button_led` (`:307`) é **só campo de report** — não há sysfs, então a posse
aqui é por escrita explícita e só.

**Teste que morde:** sem dono, `common[1] & 0x01 == 0` **E** `common[8] == 0`.
Devolva o `0x01` ao literal de `:690` e reprova.

> **Este teste substitui `tests/unit/test_audio_owner_report.py:75`, e a frase de
> `:71` (*"Gatilhos/LEDs são nossos e continuam"*) tem de ser reescrita — foi ela
> que causou o furo.**

### E2 — a porta única

**O que muda:** as três chamadas cruas a `handle.audio.setMicrophoneLED(...)` —
`:2179` (reaplicação no hotplug), `:2247` (`set_mic_led`) e `:2628`
(`apply_output_defaults`) — passam a ir por um `set_microphone_led(bool | None)`
do `_PinnedPyDualSense`, que grava `_mic_led_desejado` e espelha em
`self.audio.microphone_led`.

**Armadilha nomeada:** o `_for_each` tipa o handle como `pydualsense` cru
(`:2020-2034`) e o `_write_partial_output` engole exceção em `logger.warning`
(`:2180-2181`) — um `AttributeError` viraria **degradação calada**. Use
`getattr(h, "set_microphone_led", None)` com caminho velho, ou **prove** que todo
handle em `_handles` é `_PinnedPyDualSense`.

### E3 — `set_mic_led` ganha o terceiro estado

`set_mic_led` grava `record={"mic_led": flag}` no `_desired` (`:2249`) e o hotplug
reaplica (`:2178-2179`); e a assinatura **só aceita `bool`**
(`core/controller.py:150`). Sem o terceiro estado, a cura tem meia-vida de um
toque.

### E4 — o aceite que só existe depois desta sprint

**Com o botão físico e um cronômetro:** apertar o botão de mic do controle.

- **hoje:** o LED acende e apaga em ≤0,5 s (o keepalive o reescreve);
- **depois:** ele **fica** aceso, porque o firmware é o dono.

É o aceite mais barato da leva — e o único das três sprints do microfone que
**não depende de nenhuma hipótese não medida**.

---

## Os textos órfãos que saem junto

Eles descrevem o mundo que a `MIC-BT-DONO-01` vai mudar — publicá-los depois
seria escrever duas vezes:

| arquivo:linha | o que afirma | a verdade |
|---|---|---|
| `README.md:270-280` | *"~40% do sinal, causa em aberto"* | medido às 02:08 de 25/07 e invalidado às 14:20 do mesmo dia |
| `docs/usage/bluetooth.md:104-105` | o áudio por BT *"(fone e microfone) continua fora de escopo"* | **falso desde 25/07** — foi a fonte do erro do assistente em 03/08 |
| `cli/cmd_mic.py:15` | *"o install instala 52/53"* | **não instala** — `install.sh:202` = 0, opt-in |
| `integrations/dualsense_bt_audio.py:123-131` | *"principal suspeito não testado"* | **testado em 03/08** e refutado |
| `docs/usage/troubleshooting.md:33-51` | oferece *"quirk de boot OU regra 75"* | ignora a cura de raiz de 14/07 (`snd_usb_audio quirk_flags`), que é a instalada e default |
| `tests/unit/test_audio_owner_report.py:71` | *"Gatilhos/LEDs são nossos e continuam"* | é a frase que autorizou o escritor sem dono |

---

## Testes que vão reprovar

```
pytest tests/unit -k "audio_owner or mic_led or mic"
```

## O que NÃO fazer

- **não simplesmente parar de escrever** o `common[8]` — o mute sem LED é pior
  que o LED forçado;
- **não estender `_suppress_leds` ao `0x01`** — não há sysfs para o LED do mic;
- **não deixar o `getattr` sem caminho velho** no E2 — vira degradação calada;
- **não corrigir os textos sem a nota datada** onde a casa exige (ADR).

## O que fica ABERTO

- **a `MIC-BT-DONO-01`**, que depende desta para ter aceite válido;
- **se o kernel repõe o LED** quando soltamos a posse — não medido.
