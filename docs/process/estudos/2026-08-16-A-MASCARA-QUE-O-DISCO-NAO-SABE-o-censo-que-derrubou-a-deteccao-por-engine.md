# A máscara que o disco não sabe — o censo que derrubou a detecção por engine

**Data:** 16/08/2026, madrugada. **Steam fechada, daemon parado, nenhum jogo
aberto, nenhum controle tocado.** Tudo aqui é leitura de disco: `stat`, `mmap`,
`strings(1)` e leitura de `localconfig.vdf`.

**O que este estudo decide:** a cura *"o produto descobre a engine do jogo e
escolhe a máscara sozinho"* **não pode ser construída como foi pedida**, e o
motivo é medido, não opinado. O instrumento que prova isso ficou no repositório
(`scripts/ensaios/api_de_entrada_dos_jogos.py`, 9 segundos para rodar), e o
teste que impede a volta do erro ficou em
`tests/unit/test_api_de_entrada_01_a_assinatura_de_disco_nao_separa.py`.

---

## 1. Primeiro, os espelhos `28de:11ff` — o achado que podia mudar tudo

A pergunta era: *os 8 espelhos medidos em 16/08 existem sempre, ou só com a
Steam aberta?* Se existirem sempre, o XInput tem o que enumerar e a causa do
Duskfade é outra.

**MEDIDO, com a Steam fechada:**

```
grep -c "28de" /proc/bus/input/devices   ->  0
grep -i "x-box|xbox|X360" /proc/bus/input/devices  ->  ZERO
```

**Zero espelhos.** Eles nascem e morrem com a Steam — é coerente com o
mecanismo já documentado (`docs/protocol/pilha-steam-input-xpad-sdl.md` §2.2:
o `steamclient.so` os cria escrevendo em `/dev/uinput`).

**E o registro da própria Steam confirma que eles voltaram.** O arquivo
`~/.steam/debian-installation/config/virtualgamepadinfo.txt`, com carimbo de
**16/08/2026 03:24** — a última sessão dela — tem duas fatias:

| slot | nome | VID:PID | type |
|---|---|---|---|
| 0 | DualSense Edge Wireless Controller | `054c:0df2` | `ps5` |
| 1 | DualSense Wireless Controller | `054c:0ce6` | `ps5` |

O slot 0 é **o nosso vpad**. A Steam está espelhando o gamepad virtual deste
projeto, exatamente como a TRES-CONTROLES-01 descreveu.

### 1.1 O que isto SUBSTITUI na canônica

A canônica registra, em §2.4-bis item 4 (11/08/2026), *"zero espelhos"* com um
jogo em sessão. **Esse número está vencido para 16/08.** Não é decisão medida a
preservar — é um fato de estado que a máquina mudou —, então a regra da casa
manda substituir, e a linha nova é: *os espelhos existem quando a Steam está
aberta; com ela fechada são zero; o registro dela é o
`config/virtualgamepadinfo.txt`.*

### 1.2 E ainda assim não é isto que quebra o Duskfade

Porque `UseSteamControllerConfig = 0` está em **todos** os appids do
`localconfig.vdf` dela — é a doutrina de exceção da casa, não um acidente. Com
o Steam Input desligado para o appid, o espelho existe no `/dev/uinput` mas não
é alimentado para aquele jogo. O espelho não é a resposta.

---

## 2. As quatro fontes de detecção, pesadas — e as três que perderam

| fonte | funciona antes de rodar? | cobertura medida | custo | veredito |
|---|---|---|---|---|
| **imports do PE + varredura de agulhas** | **sim** | 21 de 24 jogos | 0,00–1,09 s/jogo, **9,0 s no total** | a melhor — e mesmo assim não basta (§3) |
| log do Unreal (`Saved/Logs/*.log`) | não | **1 de 24** | trivial | **perdeu** |
| `ControllerTypesUsed` do `localconfig.vdf` | sim | **0 de 24** | trivial | **perdeu** |
| arquivos-marca (`Engine/`, `*_Data/`) | sim | 24 de 24 | trivial | **perdeu** |

**O log do Unreal perdeu por cobertura.** Foi a sorte que revelou o
`XInputDevice` do Duskfade, mas varrendo `steamapps/common` **e** os prefixos
de `compatdata`, só o Duskfade tem log de jogo. Nenhum jogo que FUNCIONA tem
log — então nem como contraprova ele serve: não há com que comparar. Um sinal
que só existe na segunda execução e cobre 4% da biblioteca não sustenta
decisão de produto.

**O `ControllerTypesUsed` perdeu por escopo, e este é um erro que valia
cometer no papel e não no código.** Ele *parece* ser por jogo. Não é: em
`localconfig.vdf:1346` há **uma única ocorrência**, fora do bloco `apps`, no
nível da conta:

```
"ControllerTypesUsed"  "controller_ps5,controller_xboxone,controller_xbox360,
                        controller_switch_pro,controller_generic,controller_ps4,"
```

É a lista de todo tipo de controle que ela já usou na vida. Não distingue jogo
nenhum.

**Os arquivos-marca perderam sozinhos:** dão a ENGINE, não a API de entrada. Os
cinco Unreal da biblioteca têm a mesma marca e comportamentos diferentes.

---

## 3. O CENSO — e o número que fecha a discussão

Os 24 jogos instalados dela, pela melhor fonte disponível:

```
indeciso            14
entende_dualsense    7
sem_evidencia        3
```

Os **14 `indeciso`** têm todos a mesma assinatura — `rawinput,xinput`, sem SDL,
sem DualShock:

| jogo | imports do PE | XInput por `LoadLibrary`? | funciona hoje? |
|---|---|---|---|
| **Duskfade** | nenhum de entrada | sim | **NÃO — é o defeito** |
| **DON'T SCREAM** | nenhum de entrada | sim | **SIM** (perfil dela, `dualsense`) |
| **Big Walk** | nenhum de entrada | sim | **SIM** (perfil dela, `dualsense`) |
| **Sackboy** | `xinput1_4.dll` | não | **SIM** (perfil dela, `dualsense`) |
| **Stray** | `xinput1_3.dll` | não | **SIM** |
| PEAK, MMJ, Mad King (×2), Mr. Sleepy Man, Scarlet Deer Inn, オバケイドロ, REANIMAL, DON'T SCREAM TOGETHER | nenhum de entrada | sim | sem perfil dela |

**Duskfade e DON'T SCREAM são indistinguíveis no disco.** Nenhum import de
entrada; `XINPUT1_4.dll` presente só como string, carregada por `LoadLibrary`;
zero SDL na pasta. Um está quebrado, o outro funciona.

> **A heurística erraria em 13 dos 14.** Ela marcaria como Xbox um balde onde o
> defeito é UM jogo.

### 3.1 A confirmação independente veio da nossa própria interface

O rótulo `emulation_gamepad_hint_label` do `gui/main.glade` anuncia quatro
jogos como DualSense-completos — *"vibração, giroscópio e lightbar"*. Passando
os quatro pelo censo:

| jogo que a GUI anuncia | veredito do censo |
|---|---|
| Sackboy | **indeciso** |
| Mad King Redemption | **indeciso** |
| Mullet Mad Jack (MMJ) | **indeciso** |
| Pragmata | `entende_dualsense` |

**Três dos quatro jogos que o produto afirma, por escrito e na tela, entregarem
giroscópio e lightbar, seriam marcados como Xbox pela heurística — e perderiam
exatamente o giroscópio e a lightbar que a tela promete.** A contraprova não
veio de fora: veio da documentação da própria casa.

E o preço de cada erro está medido em
`docs/protocol/pilha-steam-input-xpad-sdl.md` §1.5: a máscara Xbox
(`045e:028e`) **não tem onde pôr** giroscópio, touchpad, lightbar, gatilhos
adaptativos e bateria. Treze jogos perderiam cinco features cada para consertar
um.

**Os dois erros não custam o mesmo, e a assimetria aponta para onde já
estamos.** Errar para DualSense deixa a pessoa sem controle naquele jogo —
grave, mas visível e contornável pela GUI. Errar para Xbox degrada em silêncio
um jogo que funcionava, e ninguém percebe que perdeu o giroscópio até procurar
por ele. **Na dúvida, o produto erra para DualSense** — que é exatamente o
comportamento de hoje.

### 3.2 O detalhe que quase virou um segundo erro de medição

A primeira rodada do censo deu `sem_evidencia` para sete jogos Unity. Estava
lendo o arquivo errado duas vezes: elegia o `UnityCrashHandler64.exe` (que não
tem entrada nenhuma dentro), e mesmo com o `.exe` certo a Unity não põe a
entrada no executável — põe no `UnityPlayer.dll` ao lado, onde estão
`xinput1_3.dll`, `xinput1_4.dll` e `HID.DLL`.

Corrigidas as duas coisas, `sem_evidencia` caiu de 11 para 3 — e os jogos
Unity migraram todos para `indeciso`, **incluindo o Big Walk, que funciona**.
A correção do instrumento não salvou a heurística: piorou a conta dela.

Fica registrado porque é a armadilha nº 1 desta casa outra vez — *o instrumento
mente mais que o produto* —, e desta vez ela mentiu para o lado que teria feito
a heurística parecer melhor do que é.

---

## 4. A terceira via — os dois vpads ao mesmo tempo

A pergunta era se dá para oferecer ao jogo incerto um vpad DualSense **e** um
vpad Xbox, resolvendo sem escolher.

**Hoje não dá, e o motivo é de arquitetura, não de esforço.** O `flavor` é uma
propriedade **do daemon**, não do vpad: `daemon/subsystems/coop.py:35` diz que
os jogadores secundários *"seguem a mesma máscara/flavor"*, e `coop.py:665`
tira o flavor de `config.gamepad_flavor`, um só. Não existe hoje o conceito de
dois vpads com máscaras diferentes convivendo.

E o preço, mesmo se fosse construído, seria alto do lado errado: a máscara é
global, então **todos os jogos que funcionam** passariam a mostrar dois
controles, não só os incertos. A doutrina *"duplicado > zero controles"*
(`launch_env.py:959`) é aceita como último recurso para quem ficaria sem nada —
não como estado normal de uma biblioteca que funciona.

---

## 5. O que fica, e o que NÃO foi feito

**Fica:**

- `src/hefesto_dualsense4unix/integrations/api_de_entrada.py` — lê a evidência
  de disco e a reporta. **Não troca a máscara de ninguém**, e o veredito
  `SO_XINPUT` não existe no enum, de propósito;
- `scripts/ensaios/api_de_entrada_dos_jogos.py` — o censo, 9 segundos, leitura
  pura;
- o teste que morde, com fixtures forjados dos dois casos (nenhum byte da
  biblioteca real dela é tocado).

**NÃO foi feito, e é decisão:** nada em `daemon/launch_env.py` nem em
`profiles/schema.py` consulta o veredito. Ligar os dois é a mudança que este
censo reprova.

---

## 6. O que ficou em aberto, e é dela

1. **A causa real do Duskfade continua desconhecida.** O que se sabe agora é o
   que ela **não** é: não é o wrapper (intacto, com o `VKD3D_CONFIG` preservado
   ao lado — a SENTINELA-WRAPPER-01 funcionou), não é a falta de espelho, e não
   é a engine (DON'T SCREAM é a mesma engine, a mesma assinatura, e funciona).
   O próximo passo é **em bancada, com o jogo aberto**: ver quais nós de
   `/dev/input` o processo do Duskfade abre, e comparar com o DON'T SCREAM
   rodando. É a comparação pareada que esta casa já usa para tudo, e não custa
   nada além de uma sessão com o olho dela.

2. **A pergunta que eu não devia responder sozinho:** o único caminho universal
   que sobrou é **observar em vez de adivinhar** — o produto perceber que o
   jogo não pegou nenhum vpad e reagir. Isso conserta na segunda execução, e a
   regra dela diz que *"um jogo que só funciona na segunda vez é meio
   defeito"*. Meio defeito é melhor que defeito inteiro? Não sei, e a escolha
   é dela.
