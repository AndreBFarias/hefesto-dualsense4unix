# O DESLIGADO DE ONTEM — o produto inerte por uma decisão antiga, em silêncio

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"o touchpad não tá funcionando e o giroscópio não funciona
  também e se tão no modo nativo ou hefesto dualsense, deveriam funcionar por
  default"*
- **Status:** **ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA**
- **Grau:** MEDIDO na máquina dela, com o controle no cabo e 85 % de bateria

---

## 1. O estado que ela viveu

```
native_mode: False | emulacao: False | vpads vivos: 0 | perfil ativo: nenhum
~/.config/hefesto-dualsense4unix/gamepad_disabled.flag  ->  09/08 23:50:16
```

Nem Conexão Nativa, nem "Jogar pelo Hefesto". **Fora dos dois.** E sem gamepad
virtual não existe caminho pelo qual o giroscópio chegue a jogo nenhum.

O daemon dizia o porquê a cada dois segundos — no journal, que ninguém lê:

```
gamepad_multiplos_controles_adiado  controles=0  motivo=desligada_de_proposito
last_profile_restore_pulado_perfil_de_janela  name=Pragmata
```

## 2. A cadeia, datada

| quando | o que aconteceu |
|---|---|
| **09/08 23:50** | a emulação foi desligada — gesto legítimo, opt-out gravado em disco |
| **10/08 03:53** | a emulação foi LIGADA, mas por PERFIL (`origin="profile"`) |
| — | a R-07 decide que perfil **não** escreve preferência: o flag de ontem continua |
| **10/08 05:33** | o daemon reinicia; o flag vence de novo, e nada mais liga |

Some a isso que o último perfil dela é de **jogo**, e perfil de jogo não é
restaurado no boot — por decisão, e a decisão está certa: ele entra quando o jogo
abre.

## 3. O que **não** é o defeito

**O opt-out ser permanente.** É a R-07 (*só o gesto manual escreve preferência em
disco*) e é a regra dela mesma — *"a vontade na GUI prevalece sempre"*. Uma
automação que religasse o que a dona desligou seria pior que o silêncio.

**A tela estar errada.** Ela mostrava "Controlar o PC", que era a verdade.

## 4. O defeito era o silêncio em volta

A tela dizia **o que** estava valendo, e não que aquilo vinha de uma decisão de
**ontem** que continua valendo hoje. Ela passou a noite concluindo que o produto
estava quebrado — e o produto estava obedecendo.

A aba Início passa a avisar, com as duas saídas nomeadas pelos rótulos da própria
aba, e o aviso **some no instante em que ela troca de modo**: é aviso de estado,
nunca pedido repetido. Cinco silêncios, cada um com a razão escrita e com mordida
verificada — sem opt-out, com a emulação já ligada, em Conexão Nativa, sem
controle na mesa, e sem daemon.

## 5. O requisito dela JÁ é o desenho — medido, não suposto

| modo | giroscópio | touchpad | som do controle | vibração |
|---|---|---|---|---|
| **Conexão Nativa (Sony)** | o jogo fala direto com o controle | idem | idem | idem |
| **Jogar pelo Hefesto · DualSense** | pelo vpad uhid (IMU) | pelo vpad uhid | sim | sim |
| **Jogar pelo Hefesto · Xbox 360** | **não** — limite da API do controle de Xbox | **não** | sim | sim |

E o acesso está no lugar, conferido no disco dela:

```
event2  perms=660  ACL-dela=1   DualSense Wireless Controller
event3  perms=660  ACL-dela=1   ... Motion Sensors
event4  perms=660  ACL-dela=1   ... Touchpad
/etc/udev/rules.d/72-hefesto-touchpad-motion-uaccess.rules   presente
```

**O que faltava era um modo estar ATIVO.**

## 6. O microfone, medido no mesmo dia

Saudável pelo lado do sistema: é a **fonte padrão** (`* 62. DualSense wireless
controller (PS5)`), volume 1.00, sem drop-in de supressão — só o promotor (51).

O que **falta** é outra coisa, e fica aberto: o daemon não publica o estado do
mic **no controle** (`mic_muted: None`, `mic_led: None`), então a aba Status não
tem o que mostrar. E a seção `mic` do perfil é **consumidor sem produtor** —
nenhuma superfície da janela a escreve, e o `ProfileManager` nem tem applier dela
(ver `PERFIL-SALVA-TUDO`, xfail estrito).

## 7. Um defeito meu, com a lição que já estava escrita

O widget novo do aviso derrubou **51 testes de cinco arquivos**: os dublês da aba
montam só os widgets do caso deles. Curado com `getattr` defensivo. É a mesma
lição de `registrar_modo_no_rascunho` — código de aba tem de sobreviver a dublê
parcial, senão cada widget novo cobra pedágio em arquivos que não têm nada a ver
com ele.

## 8. O que fica ABERTO

- **A palavra dela sobre o aviso na tela** (PROVA-DE-TELA-01).
- **O estado do mic no controle** não sobe ao `state_full`.
- **A seção `mic` do perfil** continua sem escritor e sem applier.
- **O rumble** segue sem causa provada; o instrumento do anel espera uma sessão
  de jogo.
