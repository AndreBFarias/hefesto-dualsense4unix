# CONTROLE-INTEIRO-NO-RÁDIO-01 — o mic e o fone que não atravessam

- **Achado em:** 07/08/2026, na máquina dela, sobre `restauro/inicio-da-sessao`
- **Pedido dela, literal** (citação não se corrige):
  > *"a ideia e usarmos o controle inteiro. pensa num jogo tipo dont scream que* <!-- noqa-acento -->
  > *precisa de Mic ligado, jogar no Bt sem Mic e impossivel."* <!-- noqa-acento -->
- **Estado:** ABERTA. **Nenhuma linha de código nesta leva** — é o levantamento
  que diz o que falta, em que ordem e a que preço. Duas afirmações publicadas da
  casa **caducam** aqui, com nota datada
- **Gravidade:** ALTA para o pedido dela — hoje, no rádio, ela tem **metade** do
  que pediu, e essa metade **não chega ao jogo**. ALTA também para o produto: das
  peças que existem, **nenhuma sobrevive a uma máquina limpa**
- **Causa-raiz:** **MEDIDA, e são duas independentes.** (a) A ponte de áudio
  cobre só o sentido controle→host: o fone dela **não tem código nenhum**
  (`BLOCO_SPEAKER = 0x13` declarado e sem uso). (b) O que existe nasce com
  `priority.session=200`, perdendo a eleição de fonte padrão para tudo — e é a
  fonte padrão que um jogo como o Don't Scream usa
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes:**
  [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) (dois
  números dela caducam aqui) ·
  [MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md)
  (vira pré-requisito, não item de lista) ·
  [SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md)
  (os números da eleição de fonte vêm de lá) ·
  [SOM-ROTA-01](2026-08-01-SOM-ROTA-01-a-rota-o-preamp-e-o-canal-do-controle.md) e
  [PARIDADE-SONY-01](2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md)
  (a rota fone/alto-falante) ·
  [RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)
  (**outro** fenômeno — não misturar) ·
  [BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md)
  (**não** é o modo de falha deste caso) ·
  [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
  (é a mesma dívida de bancada, noutra frente)
- **Método:** **leitura pura.** Nenhum serviço reiniciado, nada escrito em
  `/etc`, nada escrito em hidraw, nenhum controle derrubado. O DualSense dela
  esteve **carregando e desconectado** durante o levantamento inteiro — o que
  limita duas linhas, e as duas estão marcadas
- **Graus, como manda a casa:** **MEDIDO** = li nesta árvore ou nesta máquina,
  hoje; **SUSPEITA COM MECANISMO** = o caminho foi lido e fecha, o efeito não foi
  observado; **SEM PROVA** = está dito e ninguém verificou

---

> ## O QUE DECIDE A LEVA, E VEM PRIMEIRO PORQUE É CARO
>
> **O DualSense NÃO anuncia perfil de áudio Bluetooth. O caminho barato não
> existe.** — **MEDIDO**, hoje, na máquina dela.
>
> O registro do BlueZ do controle dela (`A0:FA:9C:00:00:F0`, Modalias
> `usb:v054Cp0CE6d0100`, *Paired* e *Bonded*) traz **UUIDs = HID `0x1124` +
> PnP `0x1200`, e mais nada**. A *Class of Device* é `0x002508` — major
> Peripheral, minor Gamepad, e nos bits de serviço só o bit 13: **o bit de Áudio
> (`0x200000`) está ausente**. O DualShock 4 dela (`E4:17:D8:00:00:83`,
> `v054Cp05C4`) traz exatamente o mesmo par.
>
> **E não é limitação desta máquina** — este é o contraste que fecha o
> argumento: o adaptador `hci0` expõe `org.bluez.Media1` com *SupportedUUIDs*
> `0000110a` (A2DP Source) e `0000110b` (A2DP Sink), e
> `/usr/lib/x86_64-linux-gnu/spa-0.2/bluez5/` tem a `libspa-bluez5.so` mais os
> codecs aptX, LDAC, LC3, mSBC e G722. **O host sabe fazer A2DP e HFP; o
> controle é que não oferece.**
>
> **Consequência para o orçamento desta leva:** a ponte por HID é o **único**
> caminho, e a metade de saída — o fone dela — **tem de ser escrita à mão**, do
> report ao PipeWire. Não há atalho a comprar.
>
> **Ressalva de honestidade:** o controle está desconectado agora (carregando),
> então este é o registro SDP **resolvido em cache**, não uma consulta ao vivo.
> Ele **não** é o modo de falha da
> [BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md)
> — lá o sintoma era UUIDs vazios; aqui o registro está **preenchido e
> completo**, e bate com o que o mantenedor do BlueZ afirma em `bluez/bluez#892`
> e com o que a
> [referência canônica](../../protocol/dualsense-referencia-canonica.md) já
> registrava: *"Bluetooth: não há A2DP/HFP. Áudio Opus tunelado em HID"*.

---

## 1. O storm está resolvido?

**Resposta curta: a pergunta estava mal colocada, e a resposta honesta é melhor
para ela do que um "sim".** O storm que parou **não era do DualSense**.

### 1.1 São três episódios, não trinta linhas — e os três graves são da webcam

**MEDIDO.** Varredura nos **trinta** boots do journal: seis boots com ocorrência,
e eles se separam em **dois bichos diferentes**.

| quando | porta | linhas | o que era |
|---|---|---|---|
| 27/07 17:06:55-58 | `usb 1-6` | **6** | webcam Logitech C920 |
| 29/07 19:13:30 | `usb 3-4` | 1 | DualSense — enumerou certo na tentativa seguinte |
| 02/08 21:36:29 | `usb 1-3` | 1 | Pro Controller — idem |
| 03/08 17:44:05 | `usb 3-2` | 1 | DualSense — idem |
| 04/08 10:27:09 | `usb 1-6` | **6** | webcam Logitech C920 |
| 04/08 11:27:11 | `usb 1-6` | **6** | webcam Logitech C920 |

Os outros **24 boots: zero**. Os três blocos de seis são rajadas de 1 a 3
segundos (`device descriptor read/64` quatro vezes, depois `not accepting
address` duas vezes). Os três de uma linha são uma tentativa que falhou e a
seguinte que deu certo — **autocorrigiram, e não são storm**.

**A identificação da porta é MEDIDA e é o achado que vira o caso:**
`journalctl _TRANSPORT=kernel | grep 'usb 1-6: Product'` devolve **três linhas,
as três `HD Pro Webcam C920`**. A porta `1-6` **nunca hospedou outra coisa no
journal inteiro**. Em 04/08 às 10:27:04 a C920 enumera; às 10:27:09 vem
`usb 1-6: USB disconnect` mais os erros de áudio dela
(`3:1: cannot set freq 16000 to ep 0x82`); e a rajada de `-71` começa **no mesmo
segundo**. O DualSense por cabo sempre enumerou no barramento 3 (`3-2`, `3-3`,
`3-4`), **nunca** em `1-6`.

Os episódios também se separam por **controlador**: as três rajadas estão todas
na xHCI `02:00.0` (*AMD 400 Series Chipset*); os três eventos de uma linha estão
no barramento 3, `0c:00.3` (*AMD Matisse*). **MEDIDO** por `lspci`.

### 1.2 A parada tem hora, e é física

**MEDIDO.** Não é "entre 04 e 05": é **04/08 às 11:39:13**, quando a C920 saiu da
porta `1-6` e foi para a `3-2`. A sequência é limpa: 11:27:11 storm no boot;
11:39:05 a C920 aparece em `1-6`; 11:39:07 `usb 1-6: USB disconnect` — dois
segundos depois; 11:39:13 ela aparece em `usb 3-2` e **nunca mais sai de lá**
(04/08 14:13, 05/08 14:49, 05/08 20:07, 06/08 21:07). O último evento de qualquer
natureza na porta `1-6` é **04/08T11:39:07**. Hoje, `ls /sys/bus/usb/devices/1-6*`
não devolve nada.

**A causa da parada — SUSPEITA COM MECANISMO, e é o único candidato de pé:** a
porta `usb 1-6`, ou o cabo da webcam nela. Associação **3 rajadas em 3 boots com
a C920 na `1-6`, contra 0 em 9 boots com ela na `3-2` ou na `3-4`**. O mecanismo
fecha: dispositivo *high-speed* enumera, cai do barramento em segundos, o xHCI
queima quatro endereços em *full-speed* e falha com `EPROTO` (`-71`) — assinatura
de link ruim (cabo, contato, alimentação da porta), **não de software**.

### 1.3 Nada nosso cabe no intervalo — três negativos medidos

**MEDIDO, os três:**

1. **A cmdline do kernel é idêntica byte a byte nos trinta boots**, e já trazia
   `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` no boot mais antigo (26/07 22:45).
   **Houve storm com o quirk ligado**, em 27/07 e duas vezes em 04/08.
2. **`/etc/modprobe.d/hefesto-dualsense-storm.conf` tem mtime 02/08 02:33**, e
   houve `-71` **depois** dele em 02/08, 03/08 e duas vezes em 04/08.
3. **Entre o último storm (04/08 11:27) e o boot limpo (04/08 14:13) não houve
   commit, não houve pacote e não houve escrita em `/etc` pelo Hefesto.** O
   `git log --all` tem buraco entre 5f1b588 (04/08 03:19) e c3829c7 (05/08
   21:55); o `dpkg.log` de 03 a 06/08 só traz docker, syncthing, thunderbird,
   github-desktop e um Chrome. **As regras udev do Hefesto em
   `/etc/udev/rules.d/` são todas de 06/08 21:01 — dois dias DEPOIS da parada.**

### 1.4 Três dias de silêncio não são "resolvido" — e aqui são menos ainda

**MEDIDO:** **desde 05/08 22:35 o DualSense não é ligado por cabo nesta máquina.**
Enumerações por dia (`idVendor=054c, idProduct=0ce6`): 01/08 = 6, 02/08 = 4,
03/08 = 4, 04/08 = 1, 05/08 = 4, **06/08 = 0, 07/08 = 0**. Os registros do driver
viraram só rádio (06/08 = 3 BT / 0 USB; 07/08 = 5 BT / 0 USB), e o `lsusb` de
agora não tem **nenhum** `054c` — o controle está carregando fora da máquina.

**Ela migrou para o rádio.** Logo o silêncio de 06 e 07/08 sobre o
DualSense-no-cabo é **NÃO-MEDIDO**: não há exposição para o defeito aparecer.

### 1.5 E o nosso instrumento é cego exatamente a este caso

**MEDIDO, e é um achado à parte.** O `storm_watch.sh` segue o journal com
`journalctl -f -n0` (linha 165 — **zero backlog**) e sobe como unit de usuário
**cerca de um minuto depois do boot**. Os três storms aconteceram entre **+1 s e
+8 s** do boot: kernel-watch iniciado 10:28:11 contra storm 10:27:09;
iniciado 11:27:34 contra storm 11:27:11.

O `kernel.log` dela tem **118 linhas e ZERO eventos** — `grep -vc '^#'` devolve 0;
são todas comentário de início e parada. **Ele não distingue "não houve storm" de
"houve e eu não estava de pé".** Enquanto isso não for corrigido (ler o boot
inteiro com `-b` ou `--since` do boot, em vez de `-n0`), **a casa não pode usar
aquele log como evidência de nada** — nem a favor, nem contra.

### 1.6 A resposta, com grau em cada metade

| afirmação | grau |
|---|---|
| Os três episódios graves eram da webcam C920 na porta `usb 1-6`, e pararam em 04/08 11:39:13 | **MEDIDO** |
| A causa é a porta `1-6` ou o cabo da webcam | **SUSPEITA COM MECANISMO** (3/3 contra 0/9) |
| Nenhuma mudança nossa cabe no intervalo da parada | **MEDIDO** (três negativos independentes) |
| O storm do DualSense **no cabo** está resolvido | **NÃO-MEDIDO** — zero exposição em 06 e 07/08 |
| O `kernel.log` da casa prova ausência de storm | **falso** — o instrumento é cego ao caso (**MEDIDO**) |

**A intuição dela está certa quanto ao fato — parou. Está errada só quanto ao
crédito: não foi cura nossa, e o que parou nem era o controle.**

---

## 2. A regra 75 é necessária?

**Resposta: NÃO. E isso é bom para ela por dois motivos, sendo que o segundo é o
que importa hoje.**

### 2.1 Ela não é o que segura o storm

**MEDIDO.** `ls /etc/udev/rules.d/75*` não devolve arquivo nenhum — a regra 75
está **ausente** desta máquina, confirmado. E os storms aconteceram **assim
mesmo**, em 27/07 e duas vezes em 04/08. Uma cura ausente não explica um efeito
presente.

**E há um motivo mais forte, que a medição de hoje traz:** a regra 75 **nunca foi
testada contra este storm, porque este storm não era do controle**. Ela desliga o
áudio USB **do DualSense**; os três episódios graves foram na porta da webcam.
Não há hipótese em que ela ajudasse.

### 2.2 O preço dela é exatamente o que ela pediu hoje

**MEDIDO** no próprio arquivo: `assets/75-ps5-controller-disable-usb-audio.rules`
faz *unbind* do `snd-usb-audio` nas interfaces de classe 01 do controle e põe
`driver_override=(none)`. **Isso mata o microfone e o fone do DualSense no
cabo** — o recurso inteiro, os dois sentidos.

O pedido dela de hoje é *"usarmos o controle inteiro"*. **A regra 75 é o único
item do acervo que anda na direção contrária**, e por isso esta sprint a marca
como **contraindicada**, não apenas dispensável.

Vale notar o contraste com a cura que **está** instalada e que preserva:
`/etc/modprobe.d/hefesto-dualsense-storm.conf` carrega
`quirk_flags 054c:0ce6:ignore_ctl_error|ctl_msg_delay_1m` e traz no próprio texto
*"PRESERVA mic (If2) E fone do jack: NÃO desliga o áudio"* — **MEDIDO**, lido em
`/sys/module/snd_usb_audio/parameters/quirk_flags`. É o caminho certo: curar sem
amputar.

### 2.3 Nota datada — o que caduca da auditoria de 26/06

> **Nota de 07/08/2026 sobre a
> [auditoria de 26/06](../audits/2026-06-26-storm-audit/sintese-resultado.json).**
> A auditoria recomendava *"regra 75: manter como backup AGORA que o WirePlumber
> não vai mais agarrar o mic"*. **A premissa dessa frase caducou pela metade**
> (**MEDIDO**): o perfil `pro-audio` fixado — a **causa número 1** dela — saiu de
> cena em 25/07 (`default-profile` traz hoje `analog-surround-40`, não
> `pro-audio`), mas o **pin do DualSense como fonte e saída ainda existe**,
> rebaixado, em `default-nodes`, com mtime 06/08 21:37. E o crédito pela parada
> de 04/08 **não pode** ir para essa cura: aquele storm era a webcam.
> **Continua valendo o mecanismo descrito pela auditoria; não vale a atribuição.**
>
> **O que a auditoria mandou desfazer está desfeito, e confere no disco**
> (**MEDIDO**): `threadirqs` fora da cmdline; `processor.max_cstate=1` fora;
> `hefesto-dsx-recover.service` e `/usr/local/sbin/dsx_recover.sh`
> **inexistentes** (`systemctl is-enabled` = *not-found*) — morreu o amplificador
> de realimentação positiva por *authorized-toggle*, que era o que re-enumerava o
> controle e realimentava o próprio storm; `99-usb-power-change.rules` ausente;
> regra 75 ausente. **O que ela mandou manter continua:**
> `usbcore.autosuspend=-1`, `pcie_aspm=off`, `99-storage-no-link-pm.rules`,
> `99-usb-kill-autosuspend.rules` e as udev 70, 71 e 76.

### 2.4 E, pelo critério dela de 07/08, a cura de storm do kernel **não está pronta**

**MEDIDO.** A única alavanca de kernel contra o `-71` que esta máquina tem é
`usbcore.quirks=054c:0ce6:gn,054c:0df2:gn`. Ela é **opt-in e não entra no
pacote**:

- `install.sh` (passo 3b) só roda `if [[ "${WITH_USB_QUIRK}" -eq 1 ]]`, com o
  comentário declarando *opt-in, default OFF*;
- `build_deb.sh` instala apenas o `install_snd_quirk.sh`;
  `grep -rn install_usb_quirk scripts/build_deb.sh packaging/` **não devolve
  nada** — o script nem chega ao `.deb`, e o `postinst` não aplica quirk nenhum;
- **nesta máquina o `gn` está na cmdline por conta do ambiente dela, não do nosso
  instalador.**

**Máquina limpa não recebe.** Pela decisão dela de 07/08 — *o Hefesto é produto,
tem de funcionar em máquina limpa* — isso é **dívida**, e está escrita.

---

## 3. O que falta para o mic e o fone dela por rádio, em ordem, com o custo

O pedido tem duas metades. **Por rádio existe UMA**, e ela não chega ao jogo.

### 3.0 O retrato de hoje

**MEDIDO**, por leitura integral de
`integrations/dualsense_bt_audio.py` (1286 linhas) e de
`daemon/subsystems/bt_mic.py` (137 linhas):

- todo o fluxo é **controle→host**: lê `0x31` com `raw[1]` bit1, extrai 71 bytes
  de Opus, decodifica e escreve num fifo;
- a **única** escrita para o controle é `montar_pedido_de_mic()` — um `0x32` de
  142 bytes que só liga e desliga o mic (`pkt[4] = 0b011` / `0b010`);
- **`BLOCO_SPEAKER = 0x13` está declarado na linha 219 e não é usado em lugar
  nenhum**; `grep '0x39' src/` devolve duas ocorrências, **ambas em comentário**;
- o único vestígio do fone é `STATUS_FONE_PLUGADO` (linha 236), que só **lê** se
  há fone espetado e reporta em `EstatisticaMic.fone_plugado`. **Nada é enviado.**

A [tabela de paridade](../../protocol/paridade-bluetooth-versus-cabo.md) já
registrava a linha: *"Alto-falante — som saindo | não confirmado | NÃO —
`BLOCO_SPEAKER = 0x13` declarado e sem uso | — | NÃO IMPLEMENTADO"*.

**Dito sem rodeio: "jogar no BT com mic e fone" hoje é, na melhor das hipóteses,
jogar no BT com mic — e mesmo esse mic não chega ao Don't Scream sozinho.**

### 3.1 A ordem, e por que é esta

A ordem abaixo **não** é por tamanho. É por dependência dura primeiro, depois por
impacto dividido por custo.

| # | peça | por que vem aqui | custo | grau do diagnóstico |
|---|---|---|---|---|
| **P0** | **filtrar o bit de áudio no espelho de motion** | **pré-requisito duro.** Sem ele, ligar o mic **quebra o giroscópio e o touchpad** | **uma condição + um teste que morde** | **MEDIDO** |
| **P1** | **o desmute com dono e ciclo de vida** | sem ele o mic nasce mudo perto de 100% | **baixo** — a sprint já está escrita | **MEDIDO** |
| **P2** | **a fonte da ponte vencer a eleição** | sem ele o jogo grava a webcam, não a voz dela | **médio** — política, e há medição pendente | **MEDIDO** |
| **P3** | **persistir a ponte e ligá-la em máquina limpa** | hoje ela morre com o processo que a subiu | **médio** | **MEDIDO** |
| **P4** | **medir por qual report o áudio SAI** | a casa tem duas respostas incompatíveis | **meia hora com o controle na mão dela** | **SEM PROVA** |
| **P5** | **escrever a ponte de saída (o fone)** | é a metade que não existe | **sprint inteira** | **MEDIDO** que falta |
| **P6** | **escrever a ROTA (fone contra alto-falante)** | o projeto escreve só o volume | **baixo, depois do P4** | **MEDIDO** |
| **P7** | **remedir o custo de banda com 2+ controles** | o número publicado é de um controle só | **baixo** | **MEDIDO** |

### P0 — o filtro do bit de áudio (o furo que morde antes de tudo)

**MEDIDO.** `core/physical_report_reader.py`, função `_struct_base()` (linhas
221-245), aceita **qualquer** `0x31` de 78 bytes cujo CRC-32 de semente `0xA1`
feche sobre os 74 primeiros bytes — e **não olha `raw[1]` em momento algum**.

E os pacotes de áudio **passam esse CRC**: é o mesmo
`bt_crc32(raw[:74], seed=BT_INPUT_CRC_SEED)` que a ponte usa em
`frame_opus_do_report()` para aceitar áudio de verdade, e áudio de verdade já foi
decodificado e gravado em WAV **duas vezes** (25/07 e 03/08).

Logo, com a ponte no ar, `extract_motion_window()` devolve `report[17:42]` — que
num pacote de áudio são **bytes de Opus** — e `extract_touchpad_click()` lê o bit
`0x02` de outro byte de Opus. **Aproximadamente 106 pacotes de Opus por segundo
entram como estado de input.**

**Consequência que ela sente: mic por Bluetooth e jogo com sensor NÃO coexistem
hoje.** Isto já está na tabela de paridade como item 3 de *"o que falta"*, com a
nota de que é pré-requisito duro dos itens 1 e 2. **Custo declarado lá e
reconfirmado aqui: uma condição.**

### P1 — o desmute com dono

**MEDIDO.** `grep '_mic_mute_by_uniq' src/` **não retorna nada**, e a
[MIC-BT-DONO-01](2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md)
está com **Status: PROPOSTA**. O firmware retém o mudo e ninguém o limpa no ciclo
de vida da ponte.

**Consequência prática na árvore como está:** ligar a ponte por BT deve dar mudo
perto de 100% até alguém rodar `mic unmute` à mão — e esse *unmute* **evapora na
próxima reconexão**.

> ### Nota datada de 07/08/2026 — dois números publicados CADUCARAM
>
> A casa não apaga decisão medida; ela recebe nota com o que caducou.
>
> **(a) Os "55% a 75% de mudo" e o "sobra por volta de 40% do sinal"
> (`README.md`, linhas 305-307, e a
> [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md))
> estão CADUCOS. — MEDIDO.** Eles foram obtidos **com um desmutador acidental
> rodando por baixo**. A cronologia está no
> [estudo de 03/08](../estudos/2026-08-03-a-noite-em-que-o-microfone-do-bluetooth-voltou.md):
> 25/07 02:08 (43d0f0a) o WAV que produziu os 55-75%; 25/07 14:20 (3d9bb7e) a
> cura AUDIO-OWNER-01 **removeu** o escritor sem dono que mantinha
> `common[9]=0x00` no keepalive; 25/07 14:24 (5115aac) o `README.md` publicou os
> "~40%". **A primeira medição limpa, de 03/08, deu 100% de MUDO com o daemon
> parado** — e os 46% a 66% com o daemon vivo eram subproduto do laço
> `mic_hotkey_toggle` alternando cerca de doze vezes por segundo, **defeito, não
> recurso**. **Prometer "~40% do sinal" hoje é prometer o que a casa mediu como
> não obtido.**
>
> **(b) A "disputa do contador de sequência do report `0x32`" (MIC-BT-01, linhas
> 60-63) está com o mecanismo descrito ERRADO. — SUSPEITA COM MECANISMO.** O
> `hid-playstation` rotaciona `ds->output_seq` nos reports **`0x31`** que **ele**
> escreve; a ponte escreve **`0x32`**, ID diferente, contador vivo só neste
> processo. **Não há disputa nesse eixo.** O que sobra é a pergunta em aberto no
> mesmo parágrafo — se o **firmware** mantém contador único para os dois IDs — e
> essa continua **SEM PROVA**: a evidência a favor é indireta (o SDL manda 0 fixo
> em todo report BT e o controle aceita) e a medição direta é minúscula (dois
> *writes*, um controle, uma vez). A própria MIC-BT-01 pedia *"manter opt-in até
> haver medição com os 4 conectados"*. **Isso nunca foi feito.**

### P2 — a fonte tem de vencer a eleição, senão o jogo não ouve

**Este é o achado que separa "publicar" de "chegar ao jogo", e é o que decide o
Don't Scream.**

**MEDIDO.** `dualsense_bt_audio.py`, linhas 609-632, carrega o
`module-pipe-source` com `source_name=hefesto_dualsense_bt_<hex6>`, `format=s16le`,
`rate=48000`, `channels=1` e — de propósito — **`priority.session=200`**.

O número contra vem da
[SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md),
medido com `pw-dump` **nesta máquina**, em 06/08:

| nó | prioridade |
|---|---|
| entrada da placa onboard | **2009** |
| webcam C920 | **2109** |
| sink `iec958` (só o monitor) | **736** |
| sink HDMI (só o monitor) | **696** |
| **a fonte da ponte** | **200** |

**Com 200 ela perde para tudo — inclusive para alto-falante.** Ao vivo, agora,
`pactl get-default-source` devolve
`alsa_input.usb-046d_HD_Pro_Webcam_C920-02.analog-stereo` (**MEDIDO**).

**Um jogo como o Don't Scream usa a fonte PADRÃO do sistema.** Logo, com a ponte
ligada e sem escolha manual, **o jogo grava a webcam** — ou, numa máquina sem
webcam, o **monitor da saída**, isto é, o próprio som do jogo, que foi exatamente
o que a SEM-MICROFONE-NENHUM-01 mediu. **Nunca a voz dela pelo controle.**

**E nenhum caminho de promoção do projeto conhece essa fonte — MEDIDO:**

- `grep 'hefesto_dualsense_bt'` em `src/`, `scripts/`, `docs/` e `assets/`:
  **cinco ocorrências, todas em `src/`. ZERO em `scripts/`;**
- `fix_wireplumber_default_source.sh` (linhas 444-448) responde literalmente
  *"nenhuma fonte de captura do DualSense apareceu"* e imprime **"por Bluetooth
  não existe fonte para promover"** — o script foi escrito para a placa USB do
  controle, que **por rádio não existe**;
- o drop-in `51` instalado por padrão usa `monitor.alsa.rules`, então **nem
  alcança** o nó da ponte: o rebaixamento a 200 é **auto-infligido**.

> **SEM PROVA, e registrado para quem for executar:** `pick_dualsense_source_id()`
> casa por **descrição** contendo "DualSense" sem "monitor", e a ponte se descreve
> *"Microfone DualSense BT (...)"* — então o `promote` **poderia** casar por
> acidente. Contra isso: ela passa `device.description` e não `node.description`,
> e `promote_source_dualsense()` **reinicia o WirePlumber por baixo de uma ponte
> viva**. Ninguém verificou. **Não conte com isso.**

**Dívida de máquina limpa, explícita:** na máquina dela a pilha persistida do
WirePlumber disfarça parte deste problema. **Em máquina limpa não há pilha.**

### P3 — nada disso liga em máquina limpa

**MEDIDO, e é a peça que a decisão dela de 07/08 promove a bloqueio:**

- `grep 'HEFESTO_DUALSENSE4UNIX_BT_MIC'` em `install.sh`, `packaging/`, `assets/`
  e `scripts/`: **ZERO ocorrências.** O gate existe só no código
  (`daemon/subsystems/bt_mic.py`, `daemon/lifecycle.py`,
  `app/widgets/controller_card.py`);
- o serviço dela confirma: `systemctl --user show ... -p Environment` devolve só
  `PYTHONUNBUFFERED=1`;
- as duas formas de subir a ponte **morrem com quem as subiu**: `mic bt` pelo CLI
  — *"a ponte não persiste, morre com o processo do CLI"*, registrado no estudo
  de 03/08 — e o interruptor da GUI (`controller_card.py`, linha 1455,
  `ligar_ponte_bt`), cujo próprio docstring diz *"dura enquanto a janela durar"*;
- dependências: `install.sh` (linhas 1046-1062) **oferece** instalar `libopus0` e
  `pulseaudio-utils`, mas via `run_apt` — **em máquina não-Debian não cobre**.

Nesta bancada está tudo presente (libopus 1.4, `pactl`, `module-pipe-source`), e
o `diagnosticar()` da ponte volta `pronto=False` **só** por *"nenhum DualSense em
Bluetooth"*, porque o controle dela está carregando.

**Custo:** médio — um gate de instalação, um ponto de persistência com dono, e
verificação de dependência que não presuma `apt`.

### P4 — antes da primeira linha do fone, resolver uma contradição interna

**SEM PROVA, e é o bloqueio do P5.** As duas fontes da casa **discordam sobre por
qual report o áudio sai para o controle**, e **nenhuma das duas foi medida aqui**:

| fonte | o que diz |
|---|---|
| `dualsense_bt_audio.py`, linha 31 e linha 222 | report **`0x39`**, hápticos `0x12` e alto-falante `0x13`/`0x16`, dois sub-blocos de 200 bytes de Opus |
| [referência canônica](../../protocol/dualsense-referencia-canonica.md), linhas 196-200 | report **`0x32`**, corpo TLV, `pid 0x12` para áudio (64 bytes), CRC-32 semente `0xA2`, PCM de 3000 Hz, 2 canais, 8 bits com sinal |

E há um agravante de escopo: o caminho descrito na referência canônica é o dos
**motores VCM**, não o do fone. **O pedido dela é o FONE.**

**Custo:** meia hora com o controle na mão dela e um fone espetado. É o
experimento mais barato desta sprint e destrava o item mais caro.

### P5 — escrever a ponte de saída (a metade que não existe)

**MEDIDO que falta**, pela leitura integral dos dois módulos: não há **uma linha**
em toda a árvore que mande áudio no sentido **host→controle** — nem para o
alto-falante, nem para o fone.

**Custo: sprint inteira**, e é o número que a tabela de paridade já publicava.
Depende do P4 e do P0.

### P6 — a rota, que existe no hardware e o projeto não escreve

**MEDIDO.** A [referência canônica](../../protocol/dualsense-referencia-canonica.md)
documenta com grau ALTA que a rota é um campo do report — `audio_control`, byte 7,
**bits 4-5 (`OUTPUT_PATH_SEL`)**:

```
0 = estéreo -> fone
1 = canal L -> fone (mono)
2 = L -> fone,  R -> ALTO-FALANTE
3 = canal R -> alto-falante interno
```

**Este projeto escreve só o volume** — e a medição de 01/08 é a assinatura disso:
**mudo até 38, satura em 102**, 60% do curso inerte, porque o kernel 6.18 escreve
**três** campos (`audio_control` para a rota, `speaker_volume`, e `audio_control2`
para o pré-amp) e a casa escreve um. **Como ela pediu o FONE e não o alto-falante,
a rota não é detalhe: é o que decide onde o som sai.**

**Custo:** baixo depois do P4 — são campos do mesmo `common`.

### P7 — remedir o custo de banda

**MEDIDO, com amostra fina.** O A/B registrado em `dualsense_bt_audio.py` (linhas
74-78): mic desligado = 260,4 Hz de input; mic ligado = 170,5 Hz de input +
106,2 Hz de áudio; desligado de novo = 274,3 Hz. **A queda de 260,4 para 170,5 é
34,5%** — o "~35%" **se sustenta**.

**O que o enfraquece, e precisa estar escrito:** foi **uma** medição, janelas de
**3 s**, **UM** controle, em 25/07, **nunca remedida**. A linha de base já mudou —
a paridade de 03/08 mediu ~300 Hz com os controles parados. E **nunca foi medido
com dois ou mais controles no mesmo rádio**, que é o cenário declarado do projeto,
justamente onde a
`BUG-MULTI-CONTROLLER-BT-CRC-CONTENTION-01` diz que o link degrada.

**Custo:** baixo — é repetir o A/B com quatro controles.

---

## 4. A cura de storm não destrava o pedido dela

Vale dizer com todas as letras, porque a intuição dela liga as duas coisas:

**MEDIDO.** A cura de raiz do storm que esta máquina tem **é USB**
(`snd_usb_audio quirk_flags`, e as gambiarras antigas nem estão instaladas: não
há regra 75 em `/etc/udev/rules.d/`, e não há drop-ins 52 nem 53 em
`~/.config/wireplumber/wireplumber.conf.d/` — só o 51). **Por rádio não existe
placa de som**, então nenhuma delas alcançaria o Bluetooth de qualquer forma:
são `monitor.alsa.rules` e regra `SUBSYSTEM=="usb"`.

**A intuição dela de que o storm parou está CERTA. Ela só não é o que faltava
para o mic e o fone por rádio.** São dois assuntos diferentes que se cruzaram no
calendário.

E, pela mesma razão, **este documento não deve ser lido junto com a
[RADIO-BOMBARDEADO-01](2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md)**:
aquilo é L2CAP no Bluetooth (44.718 frames corrompidos, com `hciconfig`
reportando `errors:0` — remontagem acima do HCI); isto é enumeração USB (`-71`,
`xhci_hcd`). **MEDIDO:** nenhuma das seis ocorrências de `-71` coincide com as
janelas daquela sprint.

---

## O que dá para fazer HOJE, sem a mão dela

Tudo o que segue é código e texto, e nada disso derruba controle:

1. **P0** — a condição no `physical_report_reader.py`, com teste que morde
   (arrancar a condição e ver reprovar);
2. **P1** — a MIC-BT-DONO-01 já está escrita e é PROPOSTA;
3. **a nota datada no `README.md`** — os "~40% do sinal" e os "55% a 75%" são o
   que a casa publica **hoje** e mediu como não obtido. **Custo trivial, e é
   honestidade de produto;**
4. **o conserto do instrumento** — `storm_watch.sh` com `-b` em vez de `-n0`, para
   que o `kernel.log` pare de valer como prova de ausência;
5. **P3, a metade de instalação** — o gate `HEFESTO_DUALSENSE4UNIX_BT_MIC` não
   existe em instalador nenhum.

## O que exige a mão dela, e por que vale

Dois experimentos, curtos, e cada um decide uma frente inteira:

- **P4 — o report do áudio de saída:** meia hora, controle na mão, fone espetado.
  **Destrava a sprint mais cara (P5) e hoje ninguém pode começá-la sem isto.**
- **O storm, para tirar o assunto do repositório:** **plugar um dispositivo
  sabidamente bom na porta `usb 1-6`** e ver se a rajada de `-71` volta. Dois
  minutos. **Se voltar, a causa é a porta e o assunto sai daqui. Se não voltar,
  sobra o cabo da webcam.** Não foi feito nesta leva por ser leitura pura.

---

## O que fica ABERTO

1. **O storm do DualSense NO CABO não foi resolvido nem refutado.** **MEDIDO**
   que não há exposição desde 05/08 22:35 — zero enumerações por cabo em 06 e
   07/08. Enquanto ela ficar no rádio, o silêncio é **NÃO-MEDIDO** e não pode ser
   contado como cura.
2. **A causa física da parada é SUSPEITA COM MECANISMO, não MEDIDO.** Falta o
   experimento da porta `usb 1-6`, que exige a mão dela.
3. **O `kernel.log` da casa não vale como evidência de nada** enquanto o
   `storm_watch.sh` seguir com `-n0`. **MEDIDO:** 118 linhas, zero eventos, e os
   três storms ocorreram antes de a unit subir.
4. **O fone por rádio não tem código.** **MEDIDO.** E antes da primeira linha há
   uma **contradição interna de protocolo** (`0x39` contra `0x32`) que está
   **SEM PROVA** dos dois lados.
5. **Se o firmware compartilha contador de sequência entre `0x31` e `0x32`:
   SEM PROVA.** Medido com dois *writes*, um controle, uma vez. Nunca com os
   quatro conectados, como a MIC-BT-01 pedia.
6. **O custo de banda com 2+ controles: NÃO MEDIDO.** O "~35%" é de um controle,
   em 25/07, com janelas de 3 s.
7. **O pin do DualSense como fonte e saída ainda existe** em `default-nodes`
   (mtime 06/08 21:37), rebaixado de `pro-audio` para `analog-surround-40`.
   **MEDIDO.** Ninguém decidiu se ele fica.
8. **Dívida de máquina limpa — três itens, e os três são bloqueio pelo critério
   dela de 07/08:**
   - **o quirk `usbcore.quirks`** é opt-in no `install.sh` e **não entra no
     `.deb`** (**MEDIDO**);
   - **a ponte de mic não tem gate em instalador nenhum** e **morre com o
     processo** que a subiu (**MEDIDO**);
   - **a eleição de fonte** só não morde aqui porque a pilha persistida do
     WirePlumber dela disfarça; **em máquina limpa não há pilha** (**MEDIDO** o
     mecanismo, **NÃO MEDIDO** em máquina limpa de verdade).

   **Nenhum dos três está pronto. Cura que só funciona nesta bancada é dívida, e
   agora está escrita.**
