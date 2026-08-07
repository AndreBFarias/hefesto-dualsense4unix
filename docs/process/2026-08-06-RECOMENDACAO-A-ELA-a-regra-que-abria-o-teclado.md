# Recomendação a ela — a regra que abria o teclado

- **Medido em:** 06/08/2026, entre 20h50 e 21h20, na máquina dela
- **Natureza:** **recomendação, não entrega.** O arquivo em questão **não é
  deste projeto** e não foi tocado por ninguém do lado do Hefesto
- **Decisão:** dela

---

## Por que este documento existe

O `doctor.sh` do Hefesto vinha imprimindo, quatro vezes seguidas:

```
[WARN] /dev/hidraw0 está 0666 (rw global) — provável ajuste manual;
       esperado é 0660+uaccess
```

**Não era ajuste manual.** O doctor estava acusando a única pessoa que não
tinha feito aquilo, e mandando procurar onde não estava. Isso já foi corrigido
do nosso lado (o aviso agora nomeia o arquivo). Este documento é a outra
metade: **o que foi medido, e o que fica para ela decidir.**

---

## O que estava acontecendo

A causa era **uma linha**, em `/etc/udev/rules.d/60-openrgb.rules`:

```
KERNEL=="hidraw*", MODE="0666"
```

`MODE="0666"` quer dizer "leitura e escrita para **qualquer** usuário local", e
`KERNEL=="hidraw*"` quer dizer "**todos** os nós hidraw", sem distinguir
aparelho. O efeito medido:

| nó | modo | o que é | quem mandava nele |
|---|---|---|---|
| hidraw0, hidraw1 | `crw-rw-rw-` | receptor 2.4G — **teclado e mouse** | a regra do OpenRGB |
| hidraw4, hidraw5 | `crw-rw-rw-` | receptor 2.4G — **mouse e teclado** | a regra do OpenRGB |
| hidraw2, hidraw3, hidraw7 | `crw-rw----+` | 8BitDo, vpad, Pro Controller | regras do Hefesto, com ACL |
| hidraw6 | `crw-------` | DualSense físico | exclusivo do daemon |

Os nós abertos eram, precisamente, **os receptores do teclado e do mouse**. E
`hidraw` entrega os relatórios de entrada **crus**, em paralelo ao caminho
`evdev`: quem abre `/dev/hidraw0` para leitura lê **o que está sendo digitado**.
O `/dev/input/event*` é `0640` + ACL exatamente para impedir isso; o bit de
leitura para "outros" desfazia a proteção para todo processo local — um jogo,
um script, um instalador.

**GRAU:** MEDIDO para as permissões e para a classe dos aparelhos (a
classificação saiu de `ID_INPUT_KEYBOARD` / `ID_INPUT_MOUSE` no udev). **SUSPEITA
COM MECANISMO** para a captura efetiva de teclas — não abri os nós dela para
ler, porque seria exatamente o abuso que este documento descreve.

O bit de escrita é o segundo lado, menos citado: permite **enviar** relatórios
ao dongle. **SEM PROVA** sobre o que esse dongle específico aceita.

### O contraste é a melhor prova de que as regras do Hefesto funcionam

Nenhum `chmod` feito à mão escolheria com precisão o **complemento exato** do
conjunto de regras do Hefesto, nem sobreviveria ao reboot (os nós abertos
tinham carimbo do boot). Os três nós que o Hefesto reivindica saíram
`0660`+ACL; os que ninguém reivindicava ficaram com o que a regra 60 deixou. As
nossas regras (`70-*` a `84-*`) rodam **depois** da 60 e vencem — que é a ordem
que ela pediu.

---

## O que já mudou (medido às 21h20 de 06/08)

O arquivo **já foi corrigido**, com nota datada dentro dele, e a linha agora é:

```
KERNEL=="hidraw*", MODE="0660", TAG+="uaccess"
```

Conferido: `~/.config/zsh/scripts/60-openrgb.rules` e
`/etc/udev/rules.d/60-openrgb.rules` têm o **mesmo** md5, então a fonte-de-verdade
do self-heal e o arquivo em vigor estão de acordo — a correção **não vai ser
desfeita** no próximo ciclo do ritual. E os oito nós hidraw estão agora em
`0660` (ou `0600`, o do DualSense).

Por que isso resolve sem quebrar o OpenRGB: o `uaccess` faz o `systemd-logind`
dar a ACL do aparelho ao usuário da **sessão ativa**. O OpenRGB roda como ela,
na sessão dela — continua enxergando tudo. O que sai é o acesso de **terceiros**:
outro usuário, um serviço de sistema, um processo que ela não iniciou.

**Ressalva honesta:** quebraria nos casos de borda — OpenRGB fora de sessão de
seat (por SSH), sob outro uid, ou num contêiner com uid diferente. **GRAU:
SUSPEITA COM MECANISMO** (não reiniciei o OpenRGB para confirmar; ele não estava
no ar durante a medição).

---

## O que ainda ficaria melhor — e é decisão dela

**Estreitar por fabricante.** O ideal é trocar o `hidraw*` genérico por uma
linha por aparelho RGB:

```
KERNEL=="hidraw*", ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="yyyy", MODE="0660", TAG+="uaccess"
```

É assim que o OpenRGB distribui as regras dele upstream hoje. Não fiz porque
não é possível fazer às cegas: sem a lista dos aparelhos RGB desta máquina,
estreitar quebraria o RGB de qualquer periférico não enumerado. Quando a lista
for conhecida (`openrgb --list-devices` com ele no ar), o passo é mecânico.

**O `i2c` e o `nvidia_*` continuam `0666`.** Não são o achado, e mexer neles
arriscaria a detecção de RGB da placa-mãe e da GPU sem ganho medido. Se um dia
forem revistos, a mesma troca é o caminho.

---

## O que o Hefesto NÃO vai fazer, e por quê

Foi avaliado instalar uma regra nossa (numerada entre 61 e 70) que devolvesse
todo nó hidraw a `0660+uaccess`. **Tecnicamente funciona**, e a numeração é
carga estrutural: tem de ser **> 60** (senão a regra do OpenRGB regrava por
cima), **< 71** (porque `/usr/lib/udev/rules.d/71-seat.rules` é quem deriva a
tag `seat` da `uaccess`) e **< 73** (porque `73-seat-late.rules` é quem
transforma a tag em ACL). Fora dessa janela o resultado é **pior que o
problema**: um arquivo numerado 99 produziria `0660` root:root **sem ACL
nenhuma**, e trancaria o OpenRGB e todo o resto.

**Mesmo funcionando, não vamos instalar isso por padrão.** Três razões:

1. um `TAG+="uaccess"` genérico em `hidraw*` dá acesso ao usuário da sessão
   sobre **todo** nó hidraw — incluindo tokens FIDO, leitores e aparelhos que
   nada têm a ver com jogo. É menos ruim que `0666`, mas ainda é **um projeto
   de gamepad legislando a política de segurança da máquina inteira**;
2. reescrever, sem ser convidado, a permissão de aparelhos de que nada sabemos
   é invasão de configuração alheia — mesmo com a intenção certa;
3. qualquer cura que **editasse ou removesse** o arquivo dela perderia a guerra
   para o self-heal pessoal, que o reinstala a cada ciclo, e viraria um
   ping-pong invisível.

**O que o Hefesto passou a fazer:** o aviso do doctor agora **nomeia o arquivo e
a linha**, agrega um aviso por causa (não um por nó), diz o que o aparelho é
("teclado", "mouse"), e afirma em voz alta que o arquivo **não é nosso**. Ele
faz o oposto do que fazia: em vez de acusar, **inocenta o Hefesto com prova** e
entrega o endereço para quem quiser decidir. O grau continua `[WARN]` de
propósito — fazer a configuração de um programa de terceiro reprovar o portão de
saúde do Hefesto seria pressioná-la a desinstalar o vizinho para o nosso
relatório ficar verde.

Se um dia ela quiser a regra do lado do Hefesto, o desenho certo é **opt-in
explícito** (`install_udev.sh --restaurar-hidraw-uaccess`), com o texto dizendo
em voz alta que aquilo **estreita o acesso que o OpenRGB hoje tem**.
Consentimento informado, nunca default.

---

## Sobre outros programas que fazem o mesmo

Separando o que foi medido do que não foi:

- **MEDIDO aqui:** OpenRGB, via arquivo pessoal, sem dono de pacote.
- **SEM PROVA nesta máquina:** que as versões atuais do OpenRGB upstream ainda
  distribuam a regra genérica.
- **NÃO acuso por nome** Solaar, Piper/libratbag, ckb-next ou headsetcontrol.
  Meu entendimento é que estreitam por fabricante, mas **não medi**, e lista de
  suspeitos envelhece, erra e ofende.

Por isso o doctor **não carrega lista de programas**: ele varre e reporta **o
arquivo que realmente existe na máquina**, seja ele qual for. Isso cobre os
cinco citados e os que ainda não conhecemos.

---

## O que conferir, se ela quiser ver com os próprios olhos

```bash
stat -c '%n %a' /dev/hidraw*                     # todos 0660/0600 agora
grep -rn 'hidraw' /etc/udev/rules.d/*.rules | grep MODE
scripts/doctor.sh --quiet                        # o aviso não aparece mais
```
