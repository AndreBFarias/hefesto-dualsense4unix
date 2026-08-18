# BONDS-QUE-SOBREVIVEM-01 — o salva-vidas que ninguém aciona

- **Nasceu de:** a noite de 03→04/08/2026, em que o `bluetoothd` caiu três vezes
  e comeu **todos** os pareamentos dela
- **Gravidade:** MÁXIMA — o produto tinha tudo para se salvar sozinho e não se
  salvou
- **Estado:** aberta
- **Pré-requisito:** nenhum. Tudo aqui é código e teste.

> ### PODE EXECUTAR HOJE, SEM ELA
>
> Todo o desenho é verificável com um `/var/lib/bluetooth` de mentira (o
> `bt_bonds_snapshot.sh` já aceita `HEFESTO_BT_SRC` para isso). Só o aceite
> final — "ela liga o controle e ele conecta" — pede a mesa dela.

---

## O requisito, na voz dela

> *"a solução tem que ser inteligente e universal. Tá muito específico pros meus
> controles mas e se amanhã eu perder todos e pra piorar, pq eu tô programando
> algo só pra eu usar? **se é open source deveria funcionar pra geral**."*

Ela disse isso depois que eu lhe ofereci três remendos manuais. Estava certa: o
defeito é do produto, e vale para qualquer pessoa que instale isto.

---

## O que aconteceu, medido

| hora | evento |
|---|---|
| 23:51:44 | snapshot com **4** bonds |
| 23:58:07 | 1º core dump do `bluetoothd` (`malloc_consolidate(): unaligned fastbin chunk`) |
| 00:00:08 | snapshot com **3** bonds |
| 00:27:52 | 2º core dump — snapshot com **2** |
| 01:42:32 | snapshot com **1** |
| 02:26:32 | 3º core dump |
| ~02:30 | `/var/lib/bluetooth/<adaptador>/` **sem nenhum device**. Só `cache` |

Não foi um evento — foi **hemorragia**. E o mecanismo de snapshot funcionou o
tempo todo: doze snapshots gravados, cada um fielmente registrando a perda em
curso.

**O produto tinha o remédio na mão e ninguém o deu.**

---

## Os quatro defeitos, achados no código

### D1. Ninguém aciona a restauração. NUNCA.

`grep -rn 'bt_bonds_restore'` no repositório inteiro devolve: o `install.sh`
que o copia, o `uninstall.sh` que o apaga, dois testes, três documentos e **uma
linha de mensagem** no `doctor.sh`. **Nenhum timer, nenhum `ExecStopPost`,
nenhum caminho de código o invoca.**

A corrente vai de "perdeu" até "existe um script" e para ali.

### D2. A poda é por TEMPO, não por VALOR — e já destruiu a prova

`scripts/bt_bonds_snapshot.sh:45` (`KEEP=12`) e `:158`
(`sort | head -n -12`). **Doze snapshots de 1 bond apagam o snapshot de 4.**

E o pior: **depois da perda, cada re-pareamento gera um snapshot novo**, que
empurra o bom para fora. É um mecanismo que se autodestrói exatamente quando
mais importa.

**Medido na máquina dela às 03:04 de 04/08:** o snapshot de 23:51:44 com os
quatro controles — **aquele de onde a restauração desta noite saiu** — **já
tinha sido podado**. Uma hora depois de salvar o Bluetooth dela, o registro que
o salvou não existia mais.

E dos doze lugares, **seis** estavam ocupados por snapshots de 1 ou 2 bonds.

### D3. O restaurador SOBRESCREVE chave nova com chave velha

`scripts/bt_bonds_restore.sh:91` — `cp -a "${DEVDIR}" "${DST}/${BASE}/"`.

O cabeçalho promete *"mescla sem destruir: o que já existe no destino e não
existe no snapshot fica intocado"*. Isso é verdade **só para MACs ausentes do
snapshot**. Para um MAC presente nos dois, o `cp -a` do diretório **sobrescreve
o `info`** — e o `info` carrega a `[LinkKey]`.

**O cenário concreto:** perdeu os bonds, re-pareou um controle na mão, rodou
`--latest`. A chave nova e **funcionando** é substituída pela velha do snapshot.

**O script produz exatamente o laço de autenticação que o próprio cabeçalho diz
existir para evitar.** É a única guarda de conteúdo que ele tem — e ela está no
`cache/`, não na credencial.

### D4. Nenhuma vigia olha para "quantos bonds existem"

As seis vigias do `bt_health_watchdog.sh` cobrem estado doente, trust, bond
temporário, zumbi de SDP e órfão de probe. **Nenhuma conta bonds.**

A vigia 3 percorre `find "${BT_STORAGE}" -name info`. Com **zero** `info`, o
laço não roda e o watchdog sai `exit 0` **sem uma palavra**.

O incidente de 04/08 é, para este script, **indistinguível de uma máquina
recém-instalada**.

---

## A cura

### E1. Distinguir os TRÊS estados que hoje são um só

Este é o coração, e a casa já se queimou com a mesma forma de cegueira duas
vezes esta semana (`DROPIN-AMBIGUO-01`, e o `check_bt_sdp_cache_envenenado` que
dava `[OK]` no meio do defeito).

| estado | como se distingue |
|---|---|
| **nunca houve bond** (instalação nova) | não há snapshot NENHUM para este adaptador |
| **ela despareou de propósito** | há snapshot, e a remoção foi por gesto — o `bluetoothd` emite `Device removed` no D-Bus, e o produto pode carimbar |
| **perdemos os bonds** | há snapshot com N bonds, o disco tem menos que N, e **não houve gesto de remoção** |

Sem o carimbo do gesto, os dois últimos são o mesmo — e restaurar por cima de
uma remoção intencional é reescrever a escolha dela em silêncio.

### E2. Poda por VALOR, com um piso protegido

Duas regras, e nenhuma sozinha basta:

1. **nunca podar o snapshot com o maior número de bonds** para um dado
   adaptador — ele é o "melhor conhecido" e sai da fila por tempo;
2. **nunca deixar um snapshot com MENOS bonds empurrar um com MAIS** para fora.

O acervo passa a ser *"o melhor conhecido + os N mais recentes"*, e não *"os N
mais recentes"*.

### E3. Restauração POR DEVICE, que se verifica e se desfaz

O modelo de risco documentado é **por controle** ("se o CONTROLE já rotacionou a
própria chave"), e a ferramenta só opera por adaptador inteiro. Isso tem de
inverter:

1. `--device <MAC>` e `--dry-run` (hoje não existem);
2. **nunca sobrescrever `[LinkKey]` mais NOVA que a do snapshot** — a cura de
   D3, e ela é uma comparação de data de modificação;
3. restaurar, religar, e **observar a assinatura de falha por device**. Ela está
   medida no journal desta casa:

       profiles/input/device.c:control_connect_cb() connect to <MAC>: <erro>
       src/device.c:search_cb() <MAC>: error updating services: <erro>

4. na janela de observação, **desfazer SÓ o device que falhou** — e dizer isso
   na tela, com o nome dele.

### E4. Alguém ACIONA — a corrente que falta

O watchdog ganha a sétima vigia: *"o disco tem menos bonds que o melhor
snapshot conhecido, e não houve gesto de remoção"* → aciona a restauração por
device de E3, com backoff, e **registra o que fez**.

**O portão que impede o ciclo vicioso:** se um device foi restaurado e falhou,
ele entra numa lista de quarentena por boot. Restaurar o mesmo MAC duas vezes no
mesmo boot é o começo do laço que realimenta o crash — e é proibido.

### E5. Quando só re-parear resolve, o produto ENSINA

Se a chave é velha de verdade, nenhum software resolve: é botão físico. O
produto tem de dizer **qual controle** e **qual combinação** — e ele conhece o
modelo pelo VID/PID.

A tabela tem de ser **dado, não código**: um mapa `VID:PID -> gesto`, extensível
sem tocar em lógica, com **fallback honesto** para modelo desconhecido
(*"segure o botão de pareamento do seu controle até a luz piscar rápido"*), e
sem inventar gesto que ninguém mediu.

**A armadilha desta casa, já paga:** a documentação registrava `X+Start` para o
modo PS4 do 8BitDo *"segundo o manual"*, e o combo real da máquina dela é
**`Start + A`**. Gesto físico **não se infere** — mede-se ou se declara
desconhecido.

### E6. Universalidade

| pressuposto de hoje | o que fazer |
|---|---|
| um adaptador só | o acervo é **por MAC de adaptador**; o snapshot de um não serve para outro, e o restaurador tem de **recusar** em vez de "ter sucesso" sem mudar nada (`bt_bonds_restore.sh:87` recria a árvore com o MAC antigo) |
| `/var/lib/bluetooth` fixo | o restaurador tem constantes cravadas (`:22-23`), ao contrário do snapshot que aceita `HEFESTO_BT_SRC`. Parametrizar é o que **destrava o teste de verdade** — hoje a suíte só o testa por leitura de texto |
| journal em inglês | `bt_health_watchdog.sh:230` casa mensagem em inglês. Numa máquina com journal traduzido a vigia 1 fica **cega** |
| controle é Sony | E5 resolve, se a tabela for dado |
| `sdptool`, `bluetoothctl` interativo | degradar com recado, nunca sair calado |

---

## O que morde

| entrega | o teste, e o que ele faz sem a cura |
|---|---|
| E2 | doze snapshots de 1 bond + um de 4 → o de 4 **sobrevive**. Sem a cura, some |
| E3.2 | destino com `[LinkKey]` mais nova que a do snapshot → restaurar **não a toca**. Sem a cura, sobrescreve |
| E3.4 | um device falha, outro funciona → só o que falhou é desfeito. Sem a cura, todos ficam ou todos caem |
| E4 | disco com menos bonds que o melhor snapshot → o watchdog **age**. Hoje sai `exit 0` calado |
| E1 | instalação nova (sem snapshot) → o watchdog **não** age. Sem a guarda, ele "restaura" o nada |
| E4-quarentena | mesmo MAC falhando duas vezes → a segunda é **recusada** |

---

## Aceite

1. simular a perda (apagar os devices de um `/var/lib/bluetooth` de mentira) e
   ver o produto **restaurar sozinho**, sem ninguém pedir;
2. simular a perda **com um device de chave velha** e ver o produto restaurar os
   bons e **desfazer só o ruim**, dizendo qual;
3. numa instalação sem snapshot nenhum, o produto **não faz nada** e não mente;
4. depois de um `bluetoothctl remove` intencional, o produto **não** ressuscita
   o bond;
5. o snapshot com mais bonds **nunca** é podado;
6. e o aceite dela: liga o controle, ele conecta.

---

## Relacionado

- [BT-SNAPSHOT-SANDBOX-01](2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md)
- [BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md)
- [CURA-QUE-FERE-01](2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md)
- [DROPIN-AMBIGUO-01](2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md) — a mesma família de cegueira
- [BT-SDP-VAZIO-01](2026-08-02-BT-SDP-VAZIO-01-o-bond-sem-servicos-e-o-laco-de-reconexao.md)
