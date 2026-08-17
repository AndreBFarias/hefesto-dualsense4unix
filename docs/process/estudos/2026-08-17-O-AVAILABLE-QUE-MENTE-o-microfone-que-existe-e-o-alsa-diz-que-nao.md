# O `available` que mente — o microfone existe e o ALSA diz que não

**16/08/2026, madrugada de 17, com o controle no cabo e a voz dela.** O
microfone do DualSense voltou a funcionar, e o caminho até lá derrubou uma
premissa que estava escrita no `doctor.sh`.

---

## O fato, medido

Com o perfil `output:analog-surround-40+input:analog-stereo` **ATIVO**:

| | |
|---|---|
| voz dela, 6 s | pico **4016** de 32767 — **12,3%** |
| silêncio, 5 s | pico 135 — 0,4% |
| o que o ALSA diz do perfil | **`available: no`** |

**O perfil que captou a voz dela está marcado como indisponível.** Não é
ambiguidade de leitura: é o mesmo `pactl list cards`, na mesma máquina, no mesmo
minuto.

## Por que o flag mente

A explicação já estava no `doctor.sh:1150-1157`, e a medição de hoje a confirma:

> O DualSense expõe `input:analog-stereo` (onde o microfone realmente vive,
> marcado `available: no`) e `input:iec958-stereo` (S/PDIF, `available: yes` e
> **sem sinal**). O WirePlumber escolhe por disponibilidade (…) porque a
> detecção de jack não vê fone plugado — a porta se chama
> `analog-input-headset-mic`. Mas o microfone EMBUTIDO usa esse mesmo caminho.

Ou seja: **o sistema esconde o microfone embutido porque acha que ele precisa de
um fone para existir.** Sem fone, o perfil analógico cai para "indisponível", o
WirePlumber elege o S/PDIF — que é entrada digital óptica e não carrega sinal
nenhum — e a gravação dá pico zero.

## As camadas, e qual curou o quê

O microfone estava bloqueado por duas, empilhadas:

| camada | estado ao chegar | o que curou |
|---|---|---|
| 1 — mudo persistido no WirePlumber | mudo | `doctor.sh --fix` (funcionou) |
| 2 — perfil da placa em S/PDIF | S/PDIF | `pactl set-card-profile … input:analog-stereo`, à mão |
| 3 — mudo no firmware | não estava mudo | nada a fazer |

**A camada 2 é a que o `--fix` não conseguiu**, e o motivo é o assunto deste
documento.

## Por que o doctor não trocou, e por que ele estava CERTO em não trocar

`doctor.sh:1425-1437` só troca para um perfil que o ALSA marque disponível. E a
cautela tem uma cicatriz escrita ao lado:

> *"Foi exatamente aqui que a versão anterior estragava a máquina: trocava um
> perfil que captava por outro que o ALSA marca indisponível, e a source nascia
> sem porta — silêncio digital."*

**As duas coisas são verdade ao mesmo tempo**, e é isso que torna o caso
interessante:

- confiar no `available` deixa o microfone do DualSense escondido para sempre;
- ignorar o `available` já estragou a máquina uma vez.

**Nenhuma regra baseada no flag resolve**, porque o flag não é confiável em
nenhuma das direções.

## A cura que isto pede — MEDIR, não confiar

O que funcionou hoje não foi um palpite melhor sobre o flag: foi **trocar e
conferir**. A cura para o `--fix` é a mesma disciplina da casa aplicada aqui:

1. guardar o perfil atual e se a source de hoje capta (pico numa janela curta);
2. trocar para o perfil analógico, mesmo com `available: no`;
3. **medir se a source nova nasceu com porta e capta de verdade**;
4. se não captar, **voltar ao perfil anterior** — e dizer que voltou.

O passo 3 é o que a versão antiga não tinha, e é o que separa esta cura daquela
que estragou a máquina. Um `set-card-profile` sem verificação é aposta; com
verificação e reversão, é ensaio.

**Custo:** uma janela de captura de ~1 s por controle, uma vez por sessão, e só
quando a source atual não capta. Não roda quando já está bom.

## O que precisa entrar, e onde

Ela pediu, textual: *"se funcionar toma nota pra corrigirmos no install e no
gui"*.

| onde | o quê |
|---|---|
| `scripts/doctor.sh` (camada 2, ~1425) | trocar-medir-reverter em vez de confiar no `available` |
| `install.sh` | rodar a mesma cura, sem flag — regra dela de 08/08 |
| aba Status, bloco Microfone | quando a source não capta, dizer **por quê** e oferecer o conserto; hoje as ondas ficam paradas e "sem sinal" é indistinguível de "este controle não tem microfone" |
| `mapa-controles.csv` | `audio.microfone@dualsense` no **cabo**: medido, com o pico de 12,3% e a ressalva do `available` |

## O que este documento NÃO afirma

- **Não diz que o rádio está resolvido.** Isto foi tudo no CABO. No rádio o
  DualSense não expõe placa de áudio nenhuma, e o caminho é a ponte de
  `dualsense_bt_audio.py` — que funciona e **não é segura** (ver
  `2026-08-16-O-PS-PRESO-*`).
- **Não diz que o perfil fica.** O WirePlumber reescolhe por disponibilidade a
  cada reconexão, e o flag continua dizendo `no`. Sem a cura no install, isto
  volta no próximo replug — e um conserto que não é código é adiamento, que é
  a frase que o próprio `doctor.sh` usa sobre a camada 1.
- **Não mediu outro DualSense.** Um controle, um cabo, uma máquina.
