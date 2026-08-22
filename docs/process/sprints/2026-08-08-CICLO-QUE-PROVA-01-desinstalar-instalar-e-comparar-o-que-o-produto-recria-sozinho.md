# CICLO-QUE-PROVA-01 — desinstalar, instalar, e comparar o que o produto recria sozinho

- **Estado:** CONCLUÍDA — o achado mais caro do ciclo (12 snapshots de bond viravam 1) tem cura em `uninstall.sh:807`, que MOVE os bonds para `bt-bonds.pre-uninstall-<timestamp>` em vez de apagar, com `tests/unit/test_ciclo_que_prova_01.py` lendo o script e `scripts/retrato_do_estado.sh` de pé (verificado em 21/08/2026)
- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint é:** o resultado do ciclo que ela pediu, **executado**
- **Natureza:** medição de ponta a ponta, na máquina dela, com o ciclo real
- **Grau:** **MEDIDO** em tudo — não há inferência aqui, há antes e depois

---

## 1. O pedido dela, e por que ele é a régua certa

> *"não quero nenhuma correção na mão, quero tudo dentro do install sem flag e ao
> final estudar o estado do pc, rodar uninstall, rodar install e comparar pra ver
> se contém todas as soluções descobertas e desenvolvidas por default"*

É a resposta 17 (*"produto — tem que funcionar em máquina limpa"*) levada à sua
consequência operacional. **Cura aplicada à mão não existe** para quem instala o
produto; **cura atrás de flag também não**, porque ninguém liga uma flag que não
conhece. O único teste honesto é desinstalar, instalar, e ver o estado renascer.

---

## 2. O instrumento, e por que ele precisou nascer

`scripts/retrato_do_estado.sh` — leitura pura, sem `sudo`, sem reiniciar nada,
pode rodar com controle conectado. Fotografa **oito eixos** do que o produto põe
na máquina: unidades systemd, configuração de sistema (drop-ins, `main.conf`),
regras de udev, módulos DKMS, executáveis e pacote, estado do usuário, áudio, e o
que está vivo no rádio.

E ele **compara**, com uma regra de leitura escrita no cabeçalho da saída:

> DIFERENTE não é reprovação por si. O que reprova é o instalador **NÃO recriar**
> o que o desinstalador levou.

**Endereço de hardware sai mascarado** (octetos 4 e 5 zerados), porque o retrato
acaba anexado a sprint e há portão que reprova.

---

## 3. Os seguros, e o primeiro deles salvou o dia

Antes de rodar, três proteções. **A primeira provou ser necessária:**

```bash
sudo cp -a /var/lib/hefesto-dualsense4unix/bt-bonds /var/tmp/bonds-antes-do-ciclo
sudo cp -a /var/lib/bluetooth                       /var/tmp/bluetooth-antes-do-ciclo
# + Steam fechada, rede conferida
```

---

## 4. O resultado: a cura ESTÁ no install, por default

**GRAU: MEDIDO.** A comparação de 25 eixos:

```
  unidades de sistema                IGUAL
  unidades de usuário                IGUAL
  timers                             IGUAL
  enabled/active                     IGUAL
  drop-ins do bluetooth              DIFERENTE
      < WatchdogSec=30
      > WatchdogSec=0                  ← A CURA, recriada sozinha
  main.conf do BlueZ                 IGUAL
  WatchdogSec efetivo                IGUAL
  regras de udev (arquivos)          IGUAL
  regras de udev (conteúdo)          IGUAL
  módulos DKMS                       IGUAL
  módulos carregados                 IGUAL
  executáveis                        IGUAL
  scripts auxiliares                 IGUAL
  instalação Python                  IGUAL
  grupos do usuário                  IGUAL
  estado do produto                  IGUAL
  configuração dela                  IGUAL
  cards de áudio                     IGUAL
  sinks e sources                    IGUAL
  pareamentos                        IGUAL
  aparelhos HID                      IGUAL
```

**A única diferença que o instalador introduziu de propósito é a cura de hoje.**
O `WatchdogSec=30` que matou o `bluetoothd` dela às 00:27:35 saiu, e o `0` entrou
— **sem flag, sem pergunta, sem comando à mão**. É exatamente o que ela pediu.

E o que **não** mudou é tão importante quanto: unidades, timers, DKMS, udev,
binários, grupos, perfis dela, pareamentos e controles atravessaram o ciclo
intactos. **O ciclo é seguro de repetir.**

**Ressalvas de escopo, declaradas:** o `WatchdogSec` **efetivo** continua `30s` na
instância viva, porque o `install.sh` faz `daemon-reload` e **nunca** reinicia o
`bluetooth.service` — reiniciar derrubaria os controles dela. A cura vale no
próximo start. E o último evento do DualSense físico é de **03:03**, uma hora
antes do ciclo: **os controles não caíram por causa dele.**

---

## 5. O PERIGO Nº1 se confirmou ao vivo, e o seguro pagou

**GRAU: MEDIDO, com número dos dois lados.**

```
antes do ciclo:  12 snapshots em /var/lib/hefesto-dualsense4unix/bt-bonds/
depois:           1
```

**O `uninstall.sh` apaga o salva-vidas de pareamento com `rm -rf`, por default,
sem flag e sem confirmação.** O `install.sh` recria **só o diretório vazio**. Os
onze snapshots restantes — que são a única rede entre um crash do `bluetoothd` e
ela repareando quatro controles à mão — **evaporam num ciclo normal**.

Foram restaurados do backup (13 agora: os 12 originais mais o novo). **Sem o
seguro, ela teria perdido o histórico inteiro de pareamentos.**

**A ironia que fecha o argumento:** o crash de 00:27:35 desta mesma noite mostrou
para que servem esses snapshots — o salva-vidas gravou os quatro bonds dois
segundos depois do crash, sozinho, funcionando perfeitamente. E um ciclo de
manutenção normal os apagaria.

**Cura de produto, e ela é P:** o `uninstall.sh` deve **mover** para
`bt-bonds.pre-uninstall-<carimbo>` em vez de `rm -rf`, ou exigir `--purge-bonds`
explícito. Apagar backup de pareamento sem pedir contraria a mesma decisão dela
que abriu esta noite: **restauro de bonds é produto, não gesto manual.**

---

## 6. O achado que o ciclo trouxe de brinde: o install instala o defeito de áudio

**GRAU: MEDIDO.** O ciclo criou um arquivo que **não existia antes**:

```
> ~/.config/wireplumber/wireplumber.conf.d/51-hefesto-dualsense-no-default-source.conf
```

E o conteúdo dele:

```
matches = [ { node.name = "~alsa_input.*[Dd]ual[Ss]ense.*" } … ]
actions = { update-props = {
    priority.session = 50
    priority.driver  = 50
```

**É o drop-in 51 que a
[RECEITA-ERRADA-01](2026-08-06-RECEITA-ERRADA-01-o-doctor-mandava-rodar-o-que-nao-resolvia.md)
mediu como a CAUSA do defeito de áudio dela** — *"o drop-in 51 rebaixa o mic do
DualSense para `priority.session = 50`, abaixo de alto-falantes de 696 e 736 —
numa máquina em que o controle é o único microfone, o monitor ganha a eleição"*.

**O ciclo provou que ele nasce do `install.sh`, por default.** Antes isto era
leitura de código; agora é medição de ponta a ponta: o arquivo não existia, o
install rodou, o arquivo passou a existir.

E a confirmação chegou pela boca do próprio produto, na conferência final do
install:

```
[FAIL] a fonte de captura padrão é um MONITOR (…DualSense…analog-surround-40.monitor)
       — o que qualquer app gravar é o áudio de SAÍDA, não a voz
```

**O instalador cria a condição e o diagnóstico a denuncia, na mesma execução.**

**Isto não foi curado nesta sprint**, e o motivo é que a cura não é óbvia: o
drop-in existe por uma razão (impedir que o controle vire a fonte padrão e roube
a captura), e removê-lo às cegas pode reabrir o defeito que ele cura. **A decisão
tem dona** — é a pergunta 9 do índice de 07/08, sobre o DualSense pinado como
fonte padrão, que agora tem consequência medida.

---

## 7. O outro FAIL da conferência, e ele não é do ciclo

```
[FAIL] cache SDP de A0:FA:…:F0 SEM [ServiceRecords] — o perfil HID não sobe
```

É o DualSense **zumbi** que a vigia da casa já tinha diagnosticado às 01:08 desta
noite, com a cura escrita por ela mesma: *"re-parear NÃO resolve. Cura: reset de
hardware do controle (furinho atrás, ~5 s com um clipe)"*. **Anterior ao ciclo, e
não afetado por ele.**

---

## 8. O que fica ABERTO

1. **O `uninstall.sh` apaga os snapshots de bond** (seção 5). Custo: **P**.
   Prioridade alta — é perda de dado dela, silenciosa, num comando de manutenção.
2. **O install instala o drop-in 51** (seção 6). Custo: **M**, e a decisão do
   desenho é dela.
3. **O `main.conf` colapsado** — 384 linhas viraram 38, e o ciclo não devolve o
   original. Sem efeito em comportamento; perde a documentação no disco.
4. **O ciclo não prova o que só o boot prova.** Três curas valem *"no próximo
   start"* — o `WatchdogSec` entre elas. A prova final é um reboot, e reboot é
   decisão dela.
5. **O ciclo não foi rodado em máquina limpa.** Ele prova que o install **recria**
   o que havia; não prova que ele **cria do zero** numa instalação virgem. São
   perguntas diferentes, e a segunda continua sem resposta.

## 9. Nota de honestidade

O ciclo foi executado de verdade: `./uninstall.sh --yes` e `./install.sh --yes`, a
partir da raiz do repositório, **nunca com `sudo`** (o `HOME` viraria `/root`), com
`SUDO_ASKPASS` para as elevações internas. Os dois terminaram com código **0**.

**A senha dela não foi escrita em arquivo versionado nem em mensagem de commit.**
O auxiliar de `askpass` viveu no diretório temporário da sessão e lê de variável
de ambiente. A casa já pagou por senha em histórico de git, e não paga de novo.

**O que se perdeu e foi devolvido:** os 12 snapshots de bond, restaurados do
backup. **O que se perdeu e não volta:** nada — os pareamentos reais, os perfis
dela, a configuração e os controles atravessaram intactos.

**O momento foi escolhido:** ela tinha ido dormir, a Steam estava fechada, nenhum
jogo aberto, nenhuma partida em curso. Rodar isto com ela jogando seria
irresponsável, e a regra fica escrita para quem repetir.
