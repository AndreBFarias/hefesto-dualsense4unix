# PARTIDA-PICOTADA-01 — a caixinha que tirava o jogador 2 a cada piscada

- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint responde:** o relato dela, ao vivo, depois de tentar jogar
  Sackboy com dois controles no cabo
- **Natureza:** defeito medido, com cura escrita e teste que morde
- **Grau:** **MEDIDO** na causa, no carimbo de hora e no contraste

---

## 1. O relato dela, literal

> *"tentei a experiência de jogar com dois controles no sackboy e ainda assim foi
> péssima mesmo com cabo, na semana passada no sábado jogamos horas com 3
> controles do usb nenhum problema, agora os problemas que notei foram
> shuttering (que voltou e deixou o jogo insustentável) […] os controles não
> respeitavam o perfil do sackboy e as minhas configs mesmo nesse controle não
> continuavam no jogo. foi um caos abrir e fechar o jogo direto. A troca do
> perfil que rolava direto matava a gameplay direto"*

**Quatro queixas. Uma causa.** E a causa não é a que o nome dela sugere: **não
era o autoswitch trocando de perfil.**

---

## 2. O que estava acontecendo

**GRAU: MEDIDO.** Journal dela, 08/08, entre 01:43 e 03:03.

Em toda a noite houve **UMA** troca de perfil por janela (`profile_autoswitch
… to=Sackboy`, às 02:12:11). No mesmo período, **oito ciclos completos** disto:

```
steam_input_excecao_ativada appid=1599660
  → coop_player_removed
  → coop_derrubado_pela_excecao_steam_input  secundarios_derrubados=1
  → gamepad_controller_grab grab=False
  → hidraw_broker_restored_all
  → gamepad_emulation_stopped                    ← o vpad MORRE
        … (ela mexe em alguma janela) …
  → steam_input_excecao_encerrada
  → steam_input_vpad_retomado flavor=dualsense
  → gamepad_emulation_started                    ← o vpad RENASCE
  → coop_player_added
```

Oito vezes, no meio da partida: 01:43:30, 01:44:39, 01:49:28, 01:53:08, 02:12:11,
02:28:35, 02:32:18, 02:48:29. Sete delas com o aviso
`coop_derrubado_pela_excecao_steam_input`.

**Cada ciclo destrói e recria o gamepad virtual e derruba o jogador 2.** É isso
que ela sentiu como *"a troca do perfil matava a gameplay"* — só que o que
trocava não era o perfil, era o controle inteiro sumindo e voltando.

### O contraste, que é o que fecha a conta

| janela | duração | quedas de vpad | por hora |
|---|---|---|---|
| **sábado 01-02/08** (o dia que funcionou) | **48 h** | **15** | 0,31 |
| **08/08, a partida dela** | **1h25** | **12** | **8,5** |

**Vinte e sete vezes mais.** E no sábado as duas únicas exceções de Steam Input
foram do **appid 3357650** (Pragmata) — **zero** do Sackboy.

---

## 3. A causa, com carimbo de hora

**GRAU: MEDIDO.**

```
~/.config/hefesto-dualsense4unix/steam_input_apps.txt
  mtime: 2026-08-08 01:43:16.928
  últimas linhas:
      # marcado no editor de perfil
      1599660
```

**Ela marcou a caixinha do Steam Input no editor do perfil do Sackboy às
01:43:16.** A primeira suspensão de vpad veio **14 segundos depois**, às
01:43:30.

A string `"marcado no editor de perfil"` só é escrita em
`app/actions/profiles_actions.py:1273` — código que nasceu no commit `6b1cb62`
(07/08 02:59, *"a caixinha que TIRA"*). A caixinha tinha **23 horas de idade**
quando ela a usou pela primeira vez.

**Este é o delta exato entre o sábado e a partida de ontem:** mesma máquina,
mesmo daemon, mesmo jogo, mesma detecção de janela. O que mudou foi **um appid a
mais numa lista**.

---

## 4. Por que uma marca única produz oito ciclos

Marcar a caixinha diz *"este jogo está na allowlist do Steam Input"*. A função
que decide se a exceção está ativa **agora** é
`daemon/launch_env.py:steam_input_exception_appid`, e ela tem duas evidências: o
marker do wrapper, e **a janela em foco, lida CRUA**.

A crueza é deliberada, e o docstring diz por quê: usar o sinal *sticky* faria a
exceção sobreviver 30 s depois do alt-tab, deixando o controle físico exposto ao
desktop.

**O defeito é que "leitura crua" virou "leitura CEGA derruba a exceção".** Os
encerramentos, no journal dela, vêm **todos** colados a um tique que não sabe de
nada:

```
02:27:28.797  autoswitch_window_info_unavailable current=Sackboy wm_class=unknown
02:27:29.505  steam_input_excecao_encerrada
02:27:29.781  gamepad_emulation_started            ← vpad recriado

01:44:42.859  autoswitch_janela_propria_ignorada wm_class=Hefesto-Dualsense4Unix
01:44:43.116  steam_input_excecao_encerrada
01:44:43.387  gamepad_emulation_started            ← ela abriu a janela do Hefesto
```

**Duas famílias, nenhuma delas significa "o jogo saiu da frente":**

1. **`wm_class=unknown`** — o backend não conseguiu ler. Sob COSMIC/Wayland isso
   acontece o tempo todo, e o `current=Sackboy` na mesma linha mostra que o jogo
   **estava** lá;
2. **a janela do próprio Hefesto** — ela abrindo a configuração no meio da
   partida, que é exatamente o que a janela existe para permitir.

**E a assimetria que denuncia o defeito:** o **autoswitch** já filtra as duas
(`profiles/autoswitch.py:_tick_sem_informacao` e `_janela_propria`, chamados na
linha 304). A exceção de Steam Input lê **a mesma leitura** e **não** filtra
nenhuma. Por isso houve uma troca de perfil e oito ciclos de vpad: a proteção
existia, e só um dos dois consumidores a usava.

---

## 5. As outras três queixas, e a mesma raiz

### *"os controles não respeitavam o perfil do sackboy"*

**GRAU: MEDIDO.** `daemon/launch_env.py:669` — quando o appid está na allowlist,
o armar do perfil **pula a seção `mode` de propósito** e devolve
`{"armado": False, "motivo": "allowlist_steam_input"}`. No journal dela:

```
01:49:28  launch_arm_pulado_allowlist_steam_input appid=1599660 profile=Sackboy
01:53:08  launch_arm_pulado_allowlist_steam_input appid=1599660 profile=Sackboy
```

**A cadeia de escolha do perfil está sã** — o perfil Sackboy existe, casa, vence
e é ativado. O que não chega é a máscara, porque a marca a desliga.

### *"as minhas configs não continuavam no jogo"*

Mesma raiz. Cada recriação de vpad refaz o estado do controle, e o que ela
ajustou à mão não sobrevive à recriação.

### *"shuttering que voltou"*

**GRAU: SUSPEITA COM MECANISMO** para a parte que é nossa. Cada recriação de vpad
bloqueia o laço do daemon e produz uma cascata de eventos `udev` — e cada evento
`udev` faz o SDL/Proton **re-enumerar os controles** dentro do jogo. Doze
recriações em 1h25 é uma re-enumeração a cada sete minutos, no meio da partida.

**Ressalva honesta, e ela não é opcional:** há também causa **elétrica** medida na
mesma janela — a porta USB derrubou o segundo DualSense várias vezes. O engasgo
provavelmente tem dois pais, e esta sprint só cura o nosso. **Não está provado
que curar este lado acaba com o engasgo dela.**

---

## 6. A contradição de produto que a caixinha criou

**GRAU: DECISÃO DELA, contrariada.** Está registrado que ela decidiu:

> a allowlist **NÃO** tira o Hefesto da frente — permitir a allowlist faz o
> Hefesto **CONTINUAR** funcionando.

Mas hoje, marcar a caixinha significa, no código: solta o grab, desfaz o
esconde-esconde do hidraw, **derruba o gamepad virtual** e **derruba o jogador 2
do co-op**. É o oposto do que ela pediu.

**E a combinação é indocumentada:** *"allowlist do Steam Input"* e *"co-op de dois
controles"* são hoje **mutuamente exclusivas**, e nada em lugar nenhum diz isso.
A caixinha aceita a marca em silêncio e o jogador 2 some.

---

## 7. A cura que ENTRA nesta sprint

**Uma condição, no lugar onde a assimetria estava.**
`daemon/launch_env.py:steam_input_exception_appid` passa a distinguir *"outro app
está na frente"* de *"não sei"*:

- **leitura cega** (`unknown`, vazio, `None`) ou **janela do próprio Hefesto**
  ⇒ não decide nada; consulta o sinal *sticky* e mantém o que valia;
- **leitura positiva de outra janela** ⇒ encerra a exceção **no mesmo tique**,
  como antes.

**O medo do docstring continua coberto**, e isso é o ponto: um alt-tab de verdade
produz leitura positiva da outra janela, e essa apaga a exceção imediatamente. O
físico não fica exposto esperando um sticky decair.

### O teste morde

`tests/unit/test_partida_picotada_01.py`, nove casos. **Arrancada a cura, quatro
reprovam** — os três de tique cego e o da janela própria. Os cinco restantes são
o contrapeso, e existem para impedir a "cura" preguiçosa de tornar tudo sticky:

- alt-tab de verdade **tem** de encerrar no mesmo tique;
- cego **sem** sticky não pode inventar exceção do nada;
- cego com sticky de outro app não ativa.

---

## 8. O que fica ABERTO

1. **A semântica da caixinha contradiz a decisão dela** (seção 6). Curar isto é
   decisão de produto, não de código: ou a exceção passa a preservar os
   secundários do co-op, ou a caixinha **recusa em voz alta** quando o perfil é de
   co-op, ou o texto dela passa a dizer *"este jogo vai ver UM controle só"*.
   **Nada disso se escolhe sem ela.** Custo: M a G.
2. **O perfil não é armado quando o appid está na allowlist** — por decisão
   declarada, não por acidente. Enquanto a semântica da caixinha não for
   reconciliada, marcar continua desligando silenciosamente a máscara do perfil
   que ela acabou de configurar.
3. **`apply_profile_mode` devolve APLICADO sem olhar se o gamepad subiu.** O par
   das 02:12:11 fecha a conta: `gamepad_start_recusado_steam_input` às
   02:12:11.531935 e, **138 microssegundos depois**, `profile_autoswitch …
   secoes=['mode=aplicado']`. O relatório mente. **GRAU: MEDIDO.** Custo: P.
4. **O portão anti-recriação de vpad é cego para este caminho.**
   `tests/unit/test_vpad_anti_recreate.py` cobre `Daemon.set_gamepad_*`; a
   suspensão da exceção chama `stop_gamepad_emulation` por baixo e passa. O
   portão trava a camada errada para este defeito. Custo: P a M.
5. **O engasgo tem uma causa elétrica não coberta aqui** (seção 5).
6. **A cura não foi provada na partida dela.** Ela é MEDIDA em teste e derivada de
   journal, mas ninguém jogou depois. **A prova é ela abrir o Sackboy com os dois
   controles e o vpad não cair.**

## 9. Nota de honestidade

O diagnóstico é leitura pura de journal e de código: nenhum serviço foi
reiniciado, nenhum controle derrubado, nada escrito na configuração dela. **A
allowlist dela não foi tocada** — tirar o `1599660` de lá devolveria o
comportamento do sábado em um segundo, mas é a marca **dela**, feita por decisão
dela na tela, e desfazê-la sem pedir seria a casa decidindo no lugar dela.

**A cura entra no código, não na configuração dela**, e é isso que a faz valer
para quem instalar o produto amanhã — que é a régua que ela fixou hoje.

**Suspeitos que caíram**, e ficam registrados para ninguém os perseguir de novo:

- **o diário de bateria** (novo em 07/08, era o suspeito nº 1): **INOCENTE**;
- **o co-op nascer ligado**: já nascia ligado no sábado — não é o delta;
- **o commit `10f4818`** (*"cinco jeitos de perguntar isto é um jogo viram um
  só"*): não quebrou o caminho do jogo;
- **a metade "calar a luz" do `6b1cb62`**: é mesmo só dos externos. Mas a **mesma
  leva** trouxe a caixinha — e é por aí que aquele commit chega ao DualSense por
  cabo. **O achado de método fica:** a auditoria de risco de uma leva não pode
  parar no título dela.
