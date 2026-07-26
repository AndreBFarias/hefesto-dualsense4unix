# MIC-USB-01 — três mutes empilhados, e nenhum deles se resolve pela janela

- **Status:** ENTREGUE em 25/07/2026 pelo commit `8f83897`
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026, com diagnóstico completo ao vivo

## O relato, em duas partes

> "o microfone aparece sempre como mudo na aba de status mesmo com USB"

e, depois de curadas duas camadas:

> "microfone aparece ativo mas as ondas sonoras não funcionam nele"

## O achado que organiza tudo

**A aba Status nunca mentiu.** Em nenhum dos dois momentos. O microfone estava
mudo de verdade — por três motivos diferentes, empilhados, em três camadas do
sistema. Cada cura revelava a de baixo.

Isso importa como método: a primeira reação foi suspeitar do medidor. Medir a
fonte real custou um comando e mostrou que o problema era o oposto — o medidor
era a única coisa funcionando.

## As três camadas, na ordem em que foram descascadas

### Camada 1 — o WirePlumber guardava o mute por rota

```
~/.local/state/wireplumber/default-routes:
alsa_card.usb-Sony…DualSense…-00:input:iec958-stereo-input={"mute":true, …}
```

O estado de mute é persistido **por rota de placa** e restaurado fielmente a cada
conexão, **sem nada no log**. Sobrevive a reboot, replug e reinstalação.

Já havia sido diagnosticado nesta mesma máquina hoje mais cedo — e **voltou**. É
a prova de que a cura anterior foi um gesto manual, não código. Um conserto que
não é código não é conserto: é adiamento.

Verificação:
```bash
grep -o 'DualSense[^}]*mute":[a-z]*' ~/.local/state/wireplumber/default-routes
```

### Camada 2 — o perfil da placa apontava para uma entrada sem sinal

> ** REFUTADO POR MEDIÇÃO EM 26/07/2026 — leia antes de agir sobre esta seção.**
>
> O que está escrito abaixo — que `input:analog-stereo` é "onde o microfone
> realmente vive" e que `input:iec958-stereo` é "sem sinal" — **não se sustentou
> quando foi medido de novo**, no mesmo controle, pelo cabo:
>
> - com `output:analog-surround-40+input:analog-stereo` (a cura que esta sprint
>   prescreve, e que o `scripts/doctor.sh --fix-mic` aplica), a source aparece
>   **sem nenhuma porta de captura** (`active_port` nulo, lista de portas vazia)
>   e entrega **327.680 bytes com pico 0 e RMS 0** — silêncio digital perfeito;
> - com `output:analog-surround-40+input:iec958-stereo`, o mesmo controle
>   gravou **pico 4606 e RMS 374**, com envelope de voz ao longo do tempo.
>
> Ou seja: nesta máquina, **o perfil que esta sprint manda evitar é o que
> capta**, e o que ela manda aplicar produz um nó sem porta. A tabela abaixo
> continua descrevendo corretamente o que o ALSA *reporta* sobre
> disponibilidade — o que caiu foi a conclusão de qual entrada carrega o áudio.
>
> **O critério confiável não é o nome do perfil, é a porta de captura.** Uma
> source sem porta ativa não entrega áudio, em qualquer perfil. É esse o teste
> que a faixa de microfone da aba Status passou a usar, e por isso nenhuma cura
> dela aponta para o `--fix-mic`.
>
> **Fica em aberto**, e não é honesto fingir que não: por que a medição de 25/07
> (pico 596 no perfil analógico) e a de 26/07 discordam. As hipóteses não
> testadas são estado da detecção de jack e o replug entre as duas — o perfil
> **reverte a cada reconexão do cabo**, o que também foi reproduzido.

Perfil ativo medido: `output:analog-surround-40+input:iec958-stereo`.

O DualSense expõe duas entradas possíveis:

| perfil | disponível | o que é |
|---|---|---|
| `input:analog-stereo` | **não** | onde o microfone realmente vive |
| `input:iec958-stereo` | sim | entrada digital S/PDIF — **sem sinal** |

O WirePlumber escolhe pela disponibilidade, e marca a analógica como
indisponível porque a detecção de jack não vê fone plugado — a porta se chama
`analog-input-headset-mic`, com grupo de disponibilidade `Legacy 1`. Mas o
microfone **embutido** do controle usa esse mesmo caminho: no mixer ALSA o
controle de captura se chama literalmente `Headset` e está ativo em 31%.

Resultado: sem fone plugado, o WirePlumber conclui que não há entrada analógica e
cai no S/PDIF, que não carrega áudio nenhum. **Gravação de 4 segundos: pico 0.**

Forçando o perfil analógico, a fonte nasce e fica `RUNNING`:
```bash
pactl set-card-profile alsa_card.usb-Sony…DualSense…-00 \
  "output:analog-surround-40+input:analog-stereo"
```

### Camada 3 — o firmware do controle estava com o microfone mudo

Mesmo com as camadas 1 e 2 curadas, a gravação continuou dando pico 0. O daemon
sabia, e dizia:

```json
audio = {"fone_plugado": false, "mic_externo": false, "mic_mudo": true}
```

O mute vive no **firmware do controle** — o mesmo estado que o botão de microfone
alterna e que acende o LED. Depois de apertar o botão físico:

```json
audio = {"fone_plugado": false, "mic_externo": false, "mic_mudo": false}
```

```
pico=176/32768  rms=32.5   →  MICROFONE CAPTANDO
```

## O defeito de produto, que é o que sobra

Nenhuma das três camadas tem cura pela janela do Hefesto.

Pior, a camada 3: o backend **tem** `set_microphone_mute`, e ele **não está
exposto**. Entre os 31 métodos do IPC há `speaker.set` — que não tem um único
chamador no produto — e **não há `mic.set`**. O único caminho para desmutar o
microfone hoje é o botão físico do controle.

Ou seja: o projeto sabe ler o estado do microfone, sabe mostrá-lo corretamente na
tela, tem a função para mudá-lo, e não oferece o botão.

## Entregas

1. **`mic.set` no IPC**, expondo `set_microphone_mute` por controle (`uniq`),
   com a semântica de três estados que o projeto já descobriu: `True` muta,
   `False` desmuta, `None` não opina. Cuidado registrado: `False` não é o mesmo
   que "não mexer" — foi exatamente esse o defeito dos dois escritores.
2. **Botão de microfone na aba Status**, ao lado do medidor. Quando estiver mudo,
   dizer **por qual das três camadas** e oferecer a cura daquela camada. Um
   medidor que some quando está mudo é pior que um medidor que explica.
3. **Cura das camadas 1 e 2 no `doctor --fix`**: detectar `mute:true` no
   `default-routes` do DualSense e o perfil S/PDIF sem sinal, e corrigir os dois.
   São ~10 linhas de verificação e o `doctor` já tem a estrutura.
4. **O drop-in 51 precisa de revisão.** Ele rebaixa a prioridade da fonte
   (`priority.session = 50`) para o DualSense não virar microfone padrão sem ela
   pedir — o que é correto e **não** é o culpado do mute. Mas hoje isso também
   impede que ela **escolha** o DualSense como padrão pela janela: o
   `set-default-source` foi sobrescrito de volta para o monitor da saída. Deve
   haver como promover explicitamente.
5. **`speaker.set` sem chamador**: ou ganha superfície junto com o microfone, ou
   sai. Método de IPC que ninguém chama é dívida com aparência de recurso.

## Como validar

```bash
# camada 1
grep -o 'DualSense[^}]*mute":[a-z]*' ~/.local/state/wireplumber/default-routes
# camada 2
pactl list cards | grep -A400 "alsa_card.usb-Sony" | grep -i "perfil ativo"
# camada 3 + prova de ponta a ponta
parecord --device=alsa_input.usb-…-00.analog-stereo -d 4 /tmp/mic.wav
```

**Critério de aceite:** com o controle no cabo e o microfone desmutado, o medidor
da aba Status se mexe quando ela fala. E quando estiver mudo, a tela diz qual das
três camadas está segurando — e oferece o botão que resolve aquela.

## O que a validação de 25/07 à noite acrescentou

Duas coisas, ambas levantadas por ela e ambas confirmadas por medição.

### A cura funciona — e a camada 2 VOLTA sozinha

Depois de um `uninstall` + `install` completos, o perfil da placa **voltou
sozinho** para a entrada digital sem sinal. O `doctor --fix-mic` entregue nesta
sprint detectou e curou:

```
[ OK ] perfil da placa do DualSense trocado para …input:analog-stereo (camada 2)
[ OK ] source do DualSense não está muda (camada 1)
```

Gravação logo depois: **pico 596** — captando. Isso confirma o que a sprint
supunha e agora está medido: **a camada 2 reaparece**, e sem cura automática ela
precisaria ser refeita à mão toda vez.

###  O instalador NÃO chama a cura — e devia

> *"isso não deveria estar por default no install sem rodar doctor?"*

Está certo, e é falha do que entregamos. Medido: **zero** ocorrências de
`--fix-mic` no `install.sh`.

O passo 10 do instalador existe e faz outra coisa — impede o DualSense de virar
o microfone **padrão** do sistema, o que é correto e deliberado. Mas ele não
toca no perfil da placa nem no mute persistido. O resultado é que **uma
instalação limpa deixa o microfone mudo**, com a cura pronta no repositório e
ninguém a chamando.

**Entrega adicional (7):** o instalador chama a cura das camadas 1 e 2 no passo
de áudio, depois de instalar o drop-in. As duas ações são complementares e não
conflitam: uma decide *quem é o microfone padrão*, a outra garante que *o
microfone funciona quando escolhido*.

Cuidado a respeitar: a cura precisa ser silenciosa quando não há DualSense
presente na hora da instalação, e nunca pode abortar o passo — vale a mesma regra
best-effort do resto do instalador.

## Relação com MIC-BT-01

A sprint MIC-BT-01 (aberta em 25/07) trata do medidor por Bluetooth, onde o áudio
chega como quadros Opus dentro dos relatórios HID. As duas se encontram na
entrega 2: **o mesmo botão e o mesmo medidor** devem servir aos dois transportes,
dizendo a verdade em cada um. Fazer duas superfícies separadas seria repetir a
divisão que já causou o problema dos cinco números de jogador.
