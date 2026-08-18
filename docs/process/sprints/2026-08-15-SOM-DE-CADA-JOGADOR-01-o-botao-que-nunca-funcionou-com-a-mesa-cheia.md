# SOM-DE-CADA-JOGADOR-01 — o botão que nunca funcionou com a mesa cheia

- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf`.
- **Grau:** **MEDIDO** na máquina dela, em 14/08, com os módulos de produção
  importados e alimentados pelo `pactl` e pelo `state_full` vivos. **Nenhuma cura
  foi aplicada** — o único comando que rodou foi um desmute manual, fora do
  produto.
- **Índice da leva:** [a cor do controle e o som de cada jogador](2026-08-14-INDICE-a-cor-do-controle-e-o-som-de-cada-jogador.md)
- **Depende de:** a **D-26** e a **D-28** para a parte de SFX. Os dois primeiros
  defeitos **não dependem de nada**.
- **Custo mínimo:** 4 h 45 (quatro entregas, a mais cara de 1 h 50)

---

## 1. O que ela pediu, e o que ela viu

Ela descreveu o alvo em 14/08 às 18:36:

> *"o canal 3 do dualsense tem uma saída de som pra efeitos sonoros sfx de cada
> joguinho (diferente da saída padrão do hdmi) a ideia é conseguirmos usar os 3
> mic e os 3 saídas de som de cada controle (sackboy por exemplo no playstation
> funciona assim)"*

E o que ela viu ao tentar:

> *"o que pega é que tentando usar ele hoje pra testar pra ver se ao menos o
> botão da guia status estava funcionando mas não funcionou em nenhum dos
> controles, não sei o que pode ter ocorrido."*

**A resposta é que nada ocorreu.** São **dois defeitos independentes, os dois
antigos**, e **nenhum é regressão de hoje**. O `storm_doctor.py` — reescrito na
mesma tarde — foi conferido e é **leitor puro** (zero `subprocess`, zero `pactl`,
zero escrita): não é suspeito.

---

## 2. Defeito A — o botão é insensível, e com quatro controles ele NUNCA funcionou

### 2.a A causa, exata

`src/hefesto_dualsense4unix/app/mic_monitor.py:221`, o último degrau de
`escolher_fonte` (`:183-223`):

```python
    if len(fontes) == 1 and len(uniqs_com_audio) == 1 and uniqs_com_audio[0] == uniq:
        return fontes[0]
    return None
```

`escolher_sink` (`:226-246`) **delega inteiramente**: o corpo é
`return escolher_fonte(sinks, uniq, uniqs_com_audio)`.

**Estado real medido na máquina dela:** 2 sinks DualSense, 3 `uniq` com áudio.
`len(fontes) == 1` é **falso** → devolve `None` **para os quatro controles**.

### 2.b A cadeia até o pixel

| passo | endereço | resultado |
|---|---|---|
| escolha do sink | `app/mic_monitor.py:221` | `None` |
| `_sink_unico_de` | `app/actions/status_actions.py:961` (`nomes.pop() if len(nomes) == 1 else ""`) | `""` |
| a ação da rota | `app/audio_saida.py:573-574` — `if not estado.sink_do_controle: return AcaoRota(TEXTO_ROTA_PARA_O_CONTROLE, False, DICA_ROTA_SEM_SINK, "")` | **`sensivel=False`, `alvo=""`** |
| a segunda tranca | `app/actions/status_actions.py:1075` (`_on_rota_de_som_clicada`, `not acao.alvo`) | o clique não faz nada |

O widget é o `btn_som_no_controle`, que nasce `sensitive=False` em
`gui/main.glade:494` e é **realojado** por `status_actions._alojar_botao_da_rota`
para o bloco "Alto-falante" do card primário (SOM-ROTA-NO-CARD-01) — o que
significa que ele **pode não estar onde ela procurou**.

### 2.c A prova, com os dados vivos

```
sinks DualSense vistos: 2 / sources DualSense vistas: 2
controle 1: sink=None  BOTÃO rótulo='Ouvir no controle' SENSÍVEL=False alvo=''
controle 2: sink=None  BOTÃO SENSÍVEL=False alvo=''
controle 3: sink=None  BOTÃO SENSÍVEL=False alvo=''
controle 4: sink=None  BOTÃO SENSÍVEL=False alvo=''
```

**O mesmo `None` derruba o medidor de microfone de TODOS os cards** — não é só o
botão.

### 2.d Não é bug: é recusa deliberada de 01/08, e ela está escrita em quatro lugares

`mic_monitor.py:207-210` (docstring de `escolher_fonte`):

> *"Dois DualSense no cabo publicam sources cujo nome não distingue um do outro
> (a string USB é a mesma), e exibir o mic do controle errado é pior que não
> exibir nenhum — é a regra do 'não invente dado na interface'."*

`mic_monitor.py:229-244` (`escolher_sink`) diz *"Medido nesta máquina em
01/08/2026"* e nomeia o `-00` como *"desempate posicional do PipeWire"*. A dica
de tela já explica ao usuário (`audio_saida.py:494-502`,
`DICA_ROTA_SEM_SINK`), e o mapa registra a mesma coisa
(`docs/data/mapa-controles-v1.csv:190`).

**A regra era certa e a premissa envelheceu.** *"O nome não distingue"* continua
verdade. *"Logo não dá para distinguir"* é falso — e a §2.e prova.

### 2.e A cura, provada: o sysfs distingue o que o nome não distingue

O hidraw (interface USB `:1.3`) e a placa de áudio (interface `:1.0`) do MESMO
controle penduram **no mesmo dispositivo USB pai**. Medido:

```
card1 -> /sys/devices/…/usb3/3-2/3-2:1.0/sound/card1
card3 -> /sys/devices/…/usb3/3-3/3-3:1.0/sound/card3

hidraw4  HID_PHYS=usb-0000:0c:00.3-2/input3   /sys/devices/…/usb3/3-2/3-2:1.3/…
hidraw5  HID_PHYS=usb-0000:0c:00.3-3/input3   /sys/devices/…/usb3/3-3/3-3:1.3/…
```

| controle | hidraw | porta USB | card ALSA | nome do PipeWire |
|---|---|---|---|---|
| 1º no cabo | hidraw4 | **3-2** | card1 | `…Controller-00` |
| 2º no cabo | hidraw5 | **3-3** | card3 | `…Controller-00.2` |

**Algoritmo:** subir no sysfs a partir de `/sys/class/hidraw/hidrawN/device` e de
`/sys/class/sound/cardN/device` até o nó que tem `idVendor`, e casar pelo
`basename`. O script que provou isto rodou e funcionou.

E o PipeWire **já publica pronto**: `device.bus_path =
"pci-0000:0c:00.3-usb-0:2:1.0"` (card1) contra `"…-usb-0:3:1.0"` (card3), e o
`sysfs.path` completo em cada nó.

### 2.f O limite honesto: a cura vale para 2 dos 4

Os dois no **cabo** expõem placa própria, sink próprio e mic próprio, e o sysfs
os distingue. **Os dois no rádio não expõem placa de áudio nenhuma.** Por
Bluetooth o áudio seria por HID (reports `0x32`–`0x39`), e o mapa registra **zero
linhas de implementação** para o alto-falante — é trabalho novo, não conserto.

**Isto é o que o ENSAIO 2+2 que ela pediu mede de graça**, e é a razão de ele
valer: com dois no cabo e dois no rádio no mesmo minuto, a assimetria deixa de
depender de memória de numeração de placa.

---

## 3. Defeito B — o botão de mic de um controle muta o microfone de outro

### 3.a A causa, exata

`src/hefesto_dualsense4unix/integrations/audio_control.py:143`, dentro de
`toggle_default_source_mute` (`:116`):

```python
self._run(["pactl", "set-source-mute", "@DEFAULT_SOURCE@", "toggle"])
```

(o ramo `wpctl`, em `:140`, usa `@DEFAULT_AUDIO_SOURCE@` — mesma família.)

Acionado por `daemon/subsystems/hotkey.py:308`, gateado por `hotkey.py:280`
(`mic_button_toggles_system`, que está **`true`** no estado de hoje).

### 3.b O laço, medido

`@DEFAULT_SOURCE@` resolve para a fonte **padrão do sistema**, que hoje é o mic
do **controle 1**:

```
pactl get-default-source → alsa_input.usb-…DualSense…-00.iec958-stereo   (card 1)
wpctl status             → *  83. DualSense … [vol: 1.00 MUTED]
```

E é o **próprio Hefesto** que a põe ali: o drop-in
`assets/wireplumber/51-hefesto-dualsense-no-default-source.conf` dá
`priority.session = 1500` / `priority.driver = 1500`, acima da placa-mãe, que
está em **1109** porque nenhuma porta de captura dela está disponível.

**O laço completo:** ela aperta o botão de mic **no controle 2** → o daemon muta a
**fonte padrão** → que é o mic do **controle 1** → o WirePlumber **persiste** →
fica mudo para sempre.

### 3.c O mute persistido, achado no disco

`~/.local/state/wireplumber/default-routes`, linha literal:

```
alsa_card.usb-Sony…DualSense_Wireless_Controller-00:input:iec958-stereo-input=
{"mute":true, "channelVolumes":[1.000000, 1.000000], …}
```

O card irmão `-00.2` tem `"mute":false` — **só o card 1 estava mudo**. E
persistido significa persistido: **sobrevive a reboot e a reinstalação**.

**Quando começou, com a honestidade que a evidência permite:** o backup
`default-routes.hefesto.bak` de 14/08 às **05:40** **já traz `mute:true`** → o
mute é anterior a isso. O último `mic_hotkey_toggle` no journal é de **09/08
18:41:01, `muted=True`**, sem um `False` depois dentro da retenção. **O
`default-routes` não carimba por linha, então a data exata não se sabe** — e não
se inventa.

**O desmute manual foi rodado** (`pactl set-source-mute … 0`). O defeito de
produto continua inteiro.

### 3.d Um fato ERRADO no caminho, que manda consertar o lugar errado

O bloco *"REVISÃO MIC-USB-01"* em
`assets/wireplumber/51-hefesto-dualsense-no-default-source.conf` afirma que
`input:iec958-stereo` *"é S/PDIF e não carrega sinal (camada 2)"*.

**É falso, e foi medido:** ALSA cru em `hw:1,0` e `hw:3,0` dá **RMS 53,0 nos
dois**; pelo PipeWire, no perfil iec958 do card 3, `parecord` dá **RMS 44,8, pico
201**. O hardware capta.

O motivo real de o perfil cair no iec958: a porta `analog-input-headset-mic` só
fica disponível com **headset plugado no jack do controle** (`Headset Mic Jack =
off` nos dois). Sem headset, `input:analog-stereo` fica indisponível, e o iec958
— que abre o **mesmo `hw:X,0`** — é o caminho que resta **e que funciona**.

Pela regra dela de 11/08, **este comentário sai por substituição**: é uma
afirmação que a medição derrubou, e mantê-la faz a próxima pessoa consertar o
que não está quebrado.

---

## 4. O canal 3 — a contradição que só o ouvido dela resolve

**Aqui há dois modelos, e os dois estão com ZERO prova.** Registrar isso é o
serviço que esta seção presta.

| modelo | quem sustenta | evidência |
|---|---|---|
| **canais 3-4 = SFX**, uma segunda saída de som | **ela**, por uso no PlayStation (Sackboy) | observação de produto, não de aparelho |
| **canais 3-4 = motores voice-coil** (haptics) | `docs/data/mapa-controles-v1.csv:148` e `:190` | a linha está sob `aparelho_confianca = inferido-do-codigo`, e a **evidência dela é a AUSÊNCIA**: busca na árvore por `voicecoil`, `VCM`, `PCM`, `Surround` devolve **só comentários**, *"nenhuma linha de implementação"* |

**O `chmap` não desempata.** Os dois cards publicam
`Playback: Channels 4 / S16_LE / 48000 / Channel map: FL FR RL RR` — que é o mapa
**genérico de surround da USB Audio Class**, não uma declaração da Sony sobre o
que cada canal faz.

**A régua que resolve é a D-28: o ensaio às cegas.** Tocar num canal por vez e
ela dizer o que ouviu, sem saber qual. É o único desenho que separa "som" de
"vibração" sem depender do que qualquer documento diz.

**E há uma coisa que já funciona hoje, e que ninguém contou nesta conta:** a
escolha **fone x alto-falante não é por canal PCM** — é por **registrador HID**.
`OUTPUT_PATH_SEL` = `common[7]` bits 4-5 do output `0x02`, autorizado por `flag0`
bit 7. Valores `0` estéreo→fone, `1` L→fone mono, `2` L→fone **e** R→alto-falante,
`3` R→alto-falante. **Medido com a orelha dela em 02/08.** Implementado em
`core/backend_pydualsense.py:259-287`, exposto no IPC como `speaker.set {rota}`.

E ele **já é por controle**, endereçado por `uniq`: **mandar som para o
alto-falante de UM controle específico entre quatro já funciona hoje.** O que
falta é ter um sink por controle para alimentá-lo — que é o Defeito A.

---

## 5. As quatro entregas

| # | entrega | grau | custo |
|---|---|---|---|
| **E1** | **O casamento por sysfs** — um quarto caso em `escolher_fonte`, antes do degrau 1:1: casa quando a evidência do sysfs é exata, `None` quando não resolve (Bluetooth, por exemplo). Destrava o botão **e** o medidor de mic de cada card | conserto | 1 h 50 |
| **E2** | **O botão de mic muta o mic DAQUELE controle** — `audio_control` deixa de mandar em `@DEFAULT_SOURCE@` e passa a receber o nome da source, que a E1 sabe produzir | conserto | 1 h 10 |
| **E3** | **O fato errado sai** do bloco REVISÃO MIC-USB-01 do drop-in do WirePlumber, substituído pela medição de 14/08 | substituição | 20 min |
| **E4** | **A dica de tela deixa de mentir por omissão**: hoje `DICA_ROTA_SEM_SINK` diz *"o sistema publica sinks com o mesmo nome"* — verdade que deixa de ser motivo depois da E1. Com a E1, a recusa que sobra é **do Bluetooth**, e é isso que a dica tem de dizer | palavra de tela | 25 min |

**A E1 é pré-requisito de tudo o que ela pediu**: SFX por jogador, mic por
jogador, e o botão da aba Status. Ela não é uma frente de áudio — é a **chave**
delas.

**A E4 é palavra de tela e por isso é dela**, e depende da E1 estar escrita: a
frase certa muda conforme o quanto a E1 alcança.

---

## 6. O teste que MORDE

Arquivo novo, `tests/unit/test_som_de_cada_jogador_01_o_sysfs_desempata.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — dois no cabo com o mesmo nome (é a principal)

**Arrancar:** manter só os três casos de `escolher_fonte`
(`mic_monitor.py:183-223`).

**Por que reprova:** o teste monta uma árvore de sysfs falsa com **dois** cards
de nome idêntico exceto pelo `-00` / `-00.2`, pendurados em portas USB
diferentes, e dois hidraw com `uniq` distintos nas mesmas portas. Exige que cada
`uniq` receba **o sink da sua porta**. Sem o quarto caso, os dois recebem `None`
e o teste cai.

Esta é a principal porque é o caso dela — e porque é a única mordida que prova
que a interface **passa a saber** o que hoje ela recusa saber.

### Mordida 2 — a recusa continua quando a evidência não é exata

**Arrancar:** fazer o quarto caso "chutar" quando o sysfs não resolve — casar por
ordem, por índice, por proximidade de nome.

**Por que reprova:** o teste dá dois controles por **Bluetooth** (sem placa
nenhuma no sysfs) e um sink solto, e exige `None`. É a mordida que preserva a
regra de 01/08 que continua certa — *"exibir o mic do controle errado é pior que
não exibir nenhum"* — e impede que a E1 troque uma recusa honesta por um palpite.

### Mordida 3 — o mute que vai para o controle errado

**Arrancar:** deixar `audio_control` mandando em `@DEFAULT_SOURCE@`
(`audio_control.py:143`).

**Por que reprova:** o dublê tem quatro controles e a fonte padrão do sistema
apontando para o **primeiro**. O teste aperta o botão de mic do **terceiro** e
exige que o comando emitido nomeie a source do terceiro. Com `@DEFAULT_SOURCE@`
o comando é o mesmo para os quatro, e o teste cai.

### Mordida 4 — a dica que descreve o motivo que já não existe

**Arrancar:** deixar `DICA_ROTA_SEM_SINK` como está depois da E1.

**Por que reprova:** o teste exige que o texto da recusa **nomeie o transporte**
quando a recusa é do Bluetooth. É aviso com lista, e a lista nasce das frases
que a E4 escrever.

### O que estes testes NÃO provam

**Que o som sai.** Nenhuma mordida aqui aciona alto-falante nenhum. Que o SFX
chega ao ouvido dela é a D-28 e é bancada.

---

## 7. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **D-26 — o SFX sai do ALTO-FALANTE do controle ou do FONE plugado nele?** O registrador `OUTPUT_PATH_SEL` já faz as duas coisas; o produto tem de escolher um padrão | escrever o padrão que ela disser |
| **D-28 — o ensaio às cegas do canal 3.** É a única régua que separa o modelo dela do modelo do mapa, e nenhum dos dois tem prova hoje | conduzir o ensaio, e escrever o resultado sem torcer por nenhum lado |
| **A E4** — palavra de tela | propor, e escrever a dela |
| — | E1, E2, E3 e as quatro mordidas |

---

## 8. Duas dívidas que ficam registradas e NÃO consertadas aqui

1. **O P4 (rádio) vem com `speaker: null`** no `state_full`, enquanto os outros
   três trazem o bloco. Não investigado. É o único dos quatro que não tem o
   bloco, e ninguém sabe se é do transporte, da unidade ou do enriquecimento.
2. **O BleachBit foi inocentado desta vez** (`default-profile` intacto desde
   25/07, drop-in intacto), **mas a cerca não cobre o caso**: hoje ela é
   `filesystems=!xdg-data/applications` apenas, e `~/.config/wireplumber/` e
   `~/.local/state/wireplumber/` seguem **dentro** do alcance do sandbox. O
   `default-routes` que carregava o mute mora exatamente ali.
