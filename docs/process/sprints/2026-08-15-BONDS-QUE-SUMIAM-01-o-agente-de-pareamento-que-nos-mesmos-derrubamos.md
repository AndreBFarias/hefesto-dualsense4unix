# BONDS-QUE-SUMIAM-01 — o agente de pareamento que nós mesmos derrubamos

- **Estado:** CONCLUÍDA — as duas curas estão commitadas (`KillSignal=SIGKILL` em
  `assets/systemd/hefesto-bt-agent.service:130` e o `reset-failed` em
  `install.sh:2472`, commits `888724a` e `a20b898`), e a E1 que faltava existe:
  três mordidas em `tests/unit/test_o_install_ressuscita_o_agente_de_pareamento.py`
  (verificado em 21/08/2026)
- **Escrito em:** 15/08/2026, de madrugada, na branch `restauro/inicio-da-sessao`,
  sobre `97c2cbf`.
- **Grau:** **MEDIDO e CURADO.** As duas curas estão **na árvore de trabalho e na
  máquina dela**, e **NÃO estão commitadas** — conferir com `git status --short`.
  Este documento é o registro que falta para elas.
  **Caducou em 21/08/2026:** as duas curas estão commitadas.
- **Depende de:** nada.
- **O que sobra:** um portão. A cura roda; o que não existe é o teste que impede
  ela de voltar. **Caducou em 21/08/2026:** o portão existe.

---

## 1. A queixa dela

14/08, 19:11:

> *"tentei conectar os dois controles que estavam via cabo no computador via bt
> depois que conectei a webcam por conta de uma call e os controles vermelho e
> azuis não conectam, **dá aquele problema de conectar automaticamente sem ter
> pedido e desligam em sequência**"*

*"Aquele problema"* tem nome técnico: **bond meio-salvo**. O BlueZ registra
`Paired: yes / Bonded: no`, o controle tenta conectar, o par não fecha, e ele
desliga. Repete com o próximo. É a sequência que ela descreveu.

**E a causa fomos nós.**

---

## 2. Defeito A — a unit ficava `failed` em TODO stop

### 2.a O que estava errado

`assets/systemd/hefesto-bt-agent.service` já tinha **três** camadas contra isso, e
a mais recente era `SuccessExitStatus=SIGKILL` (`:98`). Ela resolve o **código de
saída** do processo.

**O systemd marca a unit `failed` por outro motivo:** o `Result: timeout`, que é o
veredito do **stop**, não do processo. As duas coisas são independentes, e
nenhuma das três camadas tocava na segunda.

### 2.b Reproduzido e curado, na máquina dela

Com a unit exatamente como estava (instalada == fonte, conferido por `diff`):

```
systemctl stop hefesto-bt-agent.service
  is-active -> failed    is-failed -> failed    Result -> timeout
```

E a cura, medida no mesmo minuto com um drop-in em `/run`:

```
KillSignal=SIGKILL
systemctl stop hefesto-bt-agent.service
  is-active -> inactive  is-failed -> inactive  Result -> success
```

### 2.c Por que SIGKILL direto é seguro, e não é violência

O `bt-agent` do `bluez-tools` **não trata SIGTERM** — medido: **36 de 36 quedas
terminaram em SIGKILL desde 29/07**. Ele não tem estado em disco, e o pareamento
em curso, se houver, já falhou de qualquer forma, porque quem o serve é o
`bluetoothd` que está parando.

Mandar o sinal que funciona de primeira **encurta a janela sem agente em ~1 s por
ciclo** e — o que importa — **tira a unit do estado `failed`**, que era o dano
permanente.

---

## 3. Defeito B — e fui eu que quebrei

### 3.a O mecanismo

`scripts/bt_bonds_restore.sh` **para o `bluetooth.service`** para restaurar bonds
com o storage parado (é a parte certa, e o `mask --runtime` que a acompanha é
certo também).

O `hefesto-bt-agent.service` declara `Requires=bluetooth.service`. **Parar o
BlueZ derruba o agente junto.** O agente morre por SIGKILL, fica `failed`, e
**não volta sozinho**: `Restart=always` não cobre a morte durante um `stop`
pedido por outro serviço.

E o `trap` de saída do restore religava **só o `bluetooth.service`**.

### 3.b O custo, com relógio

Em 14/08 o restore restaurou dois bonds às **16:17**. Os dois tinham sumido de
novo às **00:29**. **Por causa da própria restauração.**

**Das 16:17 às 00:31 a máquina dela ficou sem agente de pareamento** — mais de
oito horas. E sem agente registrado o BlueZ recusa a confirmação: **todo bond
novo nasce meio-salvo e some.** É exatamente a queixa das 19:11, e ela a relatou
enquanto o defeito estava acontecendo.

### 3.c A cura

O `trap` passou a religar o agente também, com `reset-failed` **antes** do
`start`:

```sh
trap '
    systemctl unmask --runtime bluetooth.service >/dev/null 2>&1 || true
    systemctl start bluetooth.service
    systemctl reset-failed hefesto-bt-agent.service >/dev/null 2>&1 || true
    systemctl start hefesto-bt-agent.service >/dev/null 2>&1 || true
' EXIT
```

O `reset-failed` é **obrigatório**: sem ele o systemd recusa reiniciar uma unit em
`failed` que já bateu o `StartLimitBurst`. E o `|| true` de sempre — o restore
nunca pode morrer no caminho de volta, ou ela fica com o BlueZ parado e a
`mask` de runtime pendurada.

---

## 4. O estado de agora, conferido

| conferência | resultado |
|---|---|
| `hefesto-bt-agent.service` | **active**, e `is-failed` limpo |
| `bluetooth.service` | **active** |
| unit instalada x fonte da árvore | **idênticas** (o `KillSignal=SIGKILL` já está em `/etc/systemd/system`) |
| bonds no disco (`/var/lib/bluetooth/*/`) | **quatro**, os quatro com `[LinkKey]` |
| snapshot do salva-vidas | `20260815-004917`, **4 bonds** |

Os quatro controles foram **resetados de fábrica por ela** às 03h37 e re-pareados
do zero, um a um. **A mesa está sã.**

---

## 5. A entrega que falta — e é só uma

**A cura roda. O portão não existe.**

| # | entrega | custo |
|---|---|---|
| **E1** | Um teste que **arranca o religar do agente do `trap`** e reprova; e um segundo que **arranca o `KillSignal`** e reprova | 50 min |

Isto não é zelo: as **três camadas anteriores** contra o mesmo sintoma foram
escritas em três datas diferentes, e nenhuma tinha teste. A quarta camada sem
portão é a quinta camada daqui a um mês.

---

## 6. O teste que MORDE

Arquivo novo, `tests/unit/test_bonds_que_sumiam_01_o_agente_volta.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — o trap que esquece o agente (é a principal)

**Arrancar:** devolver o `trap` do `bt_bonds_restore.sh` a
`systemctl unmask …; systemctl start bluetooth.service`.

**Por que reprova:** o teste lê o script e exige que **toda unit parada no corpo
do script apareça no `trap` de saída**, direta ou indiretamente. Hoje o script
para uma (`bluetooth.service`) e derruba outra por `Requires=` — então a régua
tem de ler **também** o `Requires=` do
`assets/systemd/hefesto-bt-agent.service`, e é isso que a torna uma mordida em
vez de um `grep`.

Esta é a principal porque o defeito não estava numa unit esquecida: estava numa
**dependência invisível** entre dois arquivos que ninguém lê junto.

### Mordida 2 — o `reset-failed` que some

**Arrancar:** tirar a linha `reset-failed` e deixar só o `start`.

**Por que reprova:** o teste exige que todo `systemctl start` de uma unit com
`Restart=` e `StartLimitBurst` no `trap` venha precedido de `reset-failed`. Sem
ele o `start` é um no-op silencioso — que é a pior forma de falha, porque o
script sai com zero.

### Mordida 3 — o `KillSignal` que volta a ser SIGTERM

**Arrancar:** tirar `KillSignal=SIGKILL` de
`assets/systemd/hefesto-bt-agent.service`.

**Por que reprova:** o teste assere que a unit de um processo que **não trata
SIGTERM** declare `KillSignal=SIGKILL` **ou** um `TimeoutStopSec` curto o
bastante para não render `Result: timeout`. A lista de quem não trata SIGTERM
nasce com uma linha (`bt-agent`) e um motivo medido (36 de 36).

### O que estes testes NÃO provam

Que o bond sobrevive a um reboot dela. Isso é bancada, e a única prova que vale é
o ciclo completo — que já foi pago hoje, com reset de fábrica nos quatro.

---

## 7. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **Nada.** As duas curas são conserto de defeito medido, sem palavra de tela e sem escolha de comportamento | as curas (feitas) e a E1 (por fazer) |

---

## 8. O que fica registrado e NÃO consertado

**A webcam entrou na história e ninguém a mediu.** Ela disse *"depois que
conectei a webcam por conta de uma call"*, e o relato da falha vem logo depois. A
webcam é USB e o BlueZ dela é USB — **coabitação de barramento é hipótese viva e
não testada**. O que está provado é que o agente caído **basta** para produzir o
sintoma; o que **não** está provado é que a webcam não contribuiu.

Fica escrito para que a próxima sessão não trate a coincidência como causa nem
como ruído.
