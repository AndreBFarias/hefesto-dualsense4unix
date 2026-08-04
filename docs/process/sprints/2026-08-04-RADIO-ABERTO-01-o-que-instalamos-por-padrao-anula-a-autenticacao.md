# RADIO-ABERTO-01 — o que instalamos por padrão anula a autenticação

- **Achado em:** 04/08/2026, por um cético de segurança numa auditoria de sete
  agentes que investigava outra coisa
- **Gravidade:** **MÁXIMA** — é o único item desta leva que pode terminar em
  execução de comando na máquina de quem instala
- **Estado:** aberta
- **Pré-requisito:** nenhum

> ### PRECISÃO ANTES DE TUDO — o que está e o que NÃO está em vigor
>
> Conferido na máquina dela em 04/08 às 03:10:
>
> - `/etc/bluetooth/main.conf.d/` está **VAZIO** — o `JustWorksRepairing` **não
>   está ativo** aqui e agora;
> - `kernel.core_pattern` é o `apport` padrão do Pop!\_OS — a janela de captura
>   de core **não está armada**.
>
> **Isto NÃO diminui o achado.** O `install.sh:1268-1269` instala o arquivo
> **por padrão**, sem flag, em toda máquina que rodar o instalador. O risco é do
> produto, não do estado atual desta máquina — e é exatamente a diferença que
> ela nomeou: *"eu tô programando algo só pra eu usar? se é open source deveria
> funcionar pra geral"*.

---

## S1 — a combinação instalada por padrão remove a última barreira

Três peças, cada uma defensável sozinha, e juntas um buraco:

| peça | onde | o que faz |
|---|---|---|
| `JustWorksRepairing = always` | `assets/bluetooth/hefesto-justworks.conf:28`, instalado por `install.sh:1268` **sem flag** | o BlueZ aceita **re-pareamento** de quem já tem bond, por Just Works |
| `bt-agent --capability=NoInputNoOutput` | `assets/systemd/hefesto-bt-agent.service:23`, `enabled` | agente **padrão do sistema**; `NoInputNoOutput` dos dois lados = Just Works = **zero proteção contra MITM** |
| `FastConnectable=true` | `assets/bluetooth/hefesto-fastconnectable.conf` | page scan agressivo — de propósito, para o controle reconectar rápido |

### O cenário, passo a passo

1. atacante ao alcance de rádio faz page no BD_ADDR do adaptador — endereço
   público em qualquer conexão, e nós o deixamos **mais pageável de propósito**;
2. apresenta-se com o BD_ADDR de um controle já bondado. **BD_ADDR é escrevível
   por comando de fabricante** em dongles CSR e Realtek comuns;
3. inicia SSP. `NoInputNoOutput` dos dois lados ⇒ Just Works;
4. `JustWorksRepairing=always` remove a **última** recusa — a que existe
   justamente para dizer *"não re-pareio por Just Works quem já tem bond"*;
5. a LinkKey existente é **sobrescrita sem nenhuma interação humana**;
6. o device sobe HIDP — e **o descritor de relatório quem escolhe é ele**. Nada
   em HIDP obriga a ser gamepad. Descritor de **teclado** ⇒ injeção de teclas na
   sessão dela.

O passo 6 é o que transforma isto de "roubaram meu pareamento" em "digitaram no
meu computador".

### Por que a justificativa original não sustenta o estado atual

O cabeçalho do `hefesto-justworks.conf` justifica **dois eventos pontuais** — a
janela de migração do backport do BlueZ. E entrega um **regime permanente**. Uma
autorização de migração que nunca expira deixou de ser migração.

### A cura

**E1. `JustWorksRepairing = confirm`, nunca `always`.** E, se `always` for
mesmo necessário em alguma janela, que seja **com prazo** — armado por um gesto
e desarmado por um timer, não por memória de quem armou.

**E2. O agente padrão do sistema não pode ser o `bt-agent` genérico.** Um agente
nosso, em processo, que **autoriza por política**: aceita Just Works só quando
(a) a janela ou a CLI abriu um pareamento **explícito**, com carimbo de tempo, e
(b) a classe do device é periférico/gamepad — **recusando** `RequestAuthorization`
para HID de teclado fora dessa janela.

**E3. O alarme que já existe e ninguém usa.** `MGMT_EV_NEW_LINK_KEY` para um
endereço que **já tinha bond**, com `val` diferente, é a assinatura exata da
sobrescrita de chave. Custa uma comparação, e é o detector do próprio ataque.

---

## S2 — o socket de mgmt é um cofre de chaves, e é bidirecional

Confirmado no header do kernel dela
(`/usr/src/linux-headers-*/include/net/bluetooth/mgmt.h`):

```c
struct mgmt_link_key_info { struct mgmt_addr_info addr; __u8 type; __u8 val[16]; __u8 pin_len; }
```

`val[16]` é **a LinkKey BR/EDR crua**. O `MGMT_EV_NEW_LONG_TERM_KEY` faz o mesmo
para a LTK do LE.

Qualquer observador que a casa escreva sobre esse socket passa a ser um processo
**permanente, escrito por nós, com todo material de chave da máquina no espaço
de endereçamento**. Um `--debug` que faça hexdump, um core, ou uma linha que
grave o frame "para depurar depois" publica chaves.

**E o fd é bidirecional:** com `CAP_NET_ADMIN` o mesmo socket aceita
`MGMT_OP_UNPAIR_DEVICE`, `MGMT_OP_LOAD_LINK_KEYS`, `MGMT_OP_SET_DISCOVERABLE`.
Um observador comprometido não só lê chaves — **injeta chaves, despareia e abre
o rádio**.

### A cura

**E4. Partir em dois.** Um leitor mínimo com `CAP_NET_ADMIN` que só faz `read()`
e emite linhas normalizadas num pipe; e o classificador **sem capability
nenhuma** do outro lado.

**E5. Nunca reter o frame.** Parsear os campos usados, zerar o buffer, jamais
guardar os bytes inteiros.

**E6. `LimitCORE=0`** na unit do observador, mais o molde de blindagem que a casa
já usa em `hefesto-bt-bonds-snapshot.service`, e
`RestrictAddressFamilies=AF_BLUETOOTH AF_UNIX`.

**O teste que morde:** injetar um frame sintético com uma `val` marcada e
**reprovar** se a marca aparecer em stdout, no journal ou em arquivo. Arranca-se
a supressão, o teste fica vermelho.

---

## S3 — a janela de diagnóstico publica as chaves junto com o core

`scripts/bt_crash_capture.sh --on` grava `kernel.core_pattern` **global** e
instrui, textualmente, `coredumpctl gdb bluetoothd`.

**Um core do `bluetoothd` contém todas as LinkKeys, LTKs e IRKs residentes**,
mais MACs e nomes de todos os aparelhos da casa.

**O cenário que quase aconteceu:** esta leva quer mandar patch upstream sobre o
crash de heap. O caminho natural de um relatório de corrupção de heap é **anexar
o core** — e o mantenedor upstream vai pedir. Anexar = publicar as credenciais
de rádio de todos os aparelhos dela num rastreador público.

### A cura

**E7. Política escrita:** *core do `bluetoothd` **nunca** sai da máquina*. Para
upstream vai **backtrace** (`coredumpctl info`), nunca o core.

**E8. O `--on` arma o próprio `--off`** por timer, em N horas. `core_pattern` é
global e o desligamento hoje depende só da memória de quem ligou.

**E9. Um portão** que reprove qualquer documento desta casa que instrua anexar
core. A casa já tem o hábito de virar portão a regra que custou caro.

---

## S4 — restaurar snapshot de origem não confiável é escrita arbitrária como root

`scripts/bt_bonds_restore.sh`, linhas **88, 91 e 106**: `cp -a`.

**`cp -a` preserva symlinks — não os segue.** Um snapshot preparado contendo
`<adaptador>/<MAC>/info -> /etc/sudoers.d/x` é copiado tal e qual para
`/var/lib/bluetooth`, e então **o `bluetoothd`, como root, escreve através do
link**.

Hoje o acervo é local e só o root escreve nele, o que limita o alcance. Mas a
`BONDS-QUE-SOBREVIVEM-01` propõe **acionar a restauração automaticamente** — e
qualquer futuro que inclua importar, sincronizar ou receber um snapshot
transforma isto em execução remota.

### A cura

**E10.** O restaurador **recusa** qualquer entrada que não seja arquivo ou
diretório comum: nada de symlink, nada de device, nada de hardlink para fora da
árvore. E copia **conteúdo**, não nós — `cp` sobre caminho validado, com o
conjunto de nomes esperado (`info`, `attributes`, `settings`, `cache/<MAC>`)
declarado explicitamente, e tudo o mais recusado com recado.

**O teste que morde:** um snapshot de mentira com `info` apontando para fora da
árvore. Sem a cura, o arquivo de fora é escrito; com ela, o restore recusa e
diz por quê.

---

## Aceite

1. instalação limpa **não** deixa `JustWorksRepairing=always` permanente;
2. um device HID que se apresente como **teclado** fora de uma janela de
   pareamento explícita é **recusado**;
3. sobrescrita de LinkKey de um MAC já bondado **gera alarme** — no log e na
   tela;
4. nenhum caminho do produto grava material de chave em disco, journal ou
   stdout, e há teste que prova isso injetando uma marca;
5. o restaurador recusa symlink e nomes fora do conjunto esperado;
6. nenhum documento da casa instrui anexar core, e há portão que reprova.

---

## O que este achado ensina sobre método

Ele saiu de uma auditoria que investigava **outra coisa** — a recuperação de
pareamentos perdidos. Nenhum dos sete agentes tinha "segurança" como tarefa
principal; um deles tinha **a lente**.

Cada peça aqui foi escrita por uma boa razão, medida, e documentada com
honestidade. `JustWorksRepairing` nasceu para curar uma migração real.
`NoInputNoOutput` nasceu porque controle não tem teclado. `FastConnectable`
nasceu para o controle reconectar rápido. **O buraco não está em nenhuma delas —
está na composição**, que é a mesma forma de defeito que esta leva inteira vem
encontrando: o produto falha por **composição de comportamentos corretos**.

---

## Relacionado

- [BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md) — o desenho que S4 obriga a endurecer
- [CURA-QUE-FERE-01](2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md) — a mesma lição, em outra camada
