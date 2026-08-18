# RADIO-ABERTO-01 — o que instalamos por padrão anula a autenticação

- **Achado em:** 04/08/2026, por um cético de segurança numa auditoria de sete
  agentes que investigava outra coisa
- **Gravidade:** **MÁXIMA** — é o único item desta leva que pode terminar em
  execução de comando na máquina de quem instala
- **Estado:** **PARCIALMENTE CURADA em 05/08/2026** — ver o quadro abaixo
- **Pré-requisito:** nenhum

> ## ESTADO DAS ENTREGAS — 05/08/2026
>
> | entrega | estado | onde |
> |---|---|---|
> | **E1** `JustWorksRepairing` deixa de ser `always` | **FEITA** — os três assets em `confirm` — **mas ver a [NOTA DATADA de 06/08/2026](#nota-datada--06082026--a-e1-estava-escrita-e-nao-chegava-a-maquina): o disco dela continuou com `always` por quatro dias** | `tests/unit/test_radio_aberto_01.py` |
> | **E1-bis** a cura de `confirm` CHEGA ao disco | **FEITA em 06/08/2026** — install/uninstall com dono único e bancada de raiz falsa | `tests/unit/test_bluez_config_sh.py` |
> | **E2** agente próprio, que autoriza por política | **ABERTA** — é o que de fato fecha o cenário | — |
> | **E3** alarme de sobrescrita de LinkKey | **ABERTA** — depende do observador de `mgmt` | — |
> | **E4-E6** blindagem do observador de `mgmt` | **N/A hoje** — *o observador não existe na árvore* (conferido por `grep`); as regras ficam para quem o escrever | política em `POLITICA-core-nunca-sai-da-maquina.md` |
> | **E7** política do core escrita | **FEITA** | [a política](../POLITICA-core-nunca-sai-da-maquina.md) |
> | **E8** o `--on` arma o próprio `--off` | **FEITA** — timer transitório de 8 h | `tests/unit/test_radio_aberto_e7_e9.py` |
> | **E9** portão contra instrução de anexar core | **FEITA** | `tests/unit/test_radio_aberto_e7_e9.py` |
> | **E10** restaurador recusa symlink e nome fora do conjunto | **FEITA** — validação + cópia por conteúdo | `tests/unit/test_radio_aberto_e10.py` |
>
> ### A honestidade sobre a E1, e ela importa
>
> **`confirm` sozinho NÃO fecha o buraco.** Ele devolve ao BlueZ a decisão de
> perguntar — mas quem responde é o agente, e o agente padrão hoje é o
> `bt-agent` genérico com `NoInputNoOutput`, que autoriza. A E1 remove o
> *"sempre aceita, sem nem perguntar"*; **a E2 continua sendo a entrega que
> fecha o cenário**, e segue aberta.
>
> ### O que a E10 ganhou de brinde
>
> A validação virou o modo **`bt_bonds_restore.sh --verificar <ts>`**, que
> confere um snapshot **sem parar o `bluetooth.service`** — e roda antes do
> `stop` no caminho de restauração. Um snapshot recusado deixou de custar a ela
> os controles conectados.
>
> ### Falso positivo pago na primeira execução do portão E9
>
> O primeiro regex casava `post\w*` dentro de *"res**post**a"* e `core` dentro
> do caminho `core/led_control.py`. **O portão reprovou um documento inocente
> de julho.** Corrigido com fronteira de palavra, exclusão de `core/` e proibição
> de atravessar ponto final — e o caso está registrado no próprio teste, porque
> é a armadilha que qualquer varredura por palavra-chave nesta casa vai repetir.

> ### PRECISÃO ANTES DE TUDO — o que está e o que NÃO está em vigor
>
> Conferido na máquina dela em 04/08 às 03:10:
>
> - `/etc/bluetooth/main.conf.d/` está **VAZIO** — o `JustWorksRepairing` **não
>   está ativo** aqui e agora;
> - `kernel.core_pattern` é o `apport` padrão do Pop!\_OS — a janela de captura
>   de core **não está armada**.
>
> **Isto NÃO diminui o achado.** O `install.sh:1381-1382` instala o arquivo
> **por padrão**, sem flag, em toda máquina que rodar o instalador. O risco é do
> produto, não do estado atual desta máquina — e é exatamente a diferença que
> ela nomeou: *"eu tô programando algo só pra eu usar? se é open source deveria
> funcionar pra geral"*.

## NOTA DATADA — 06/08/2026 (fim do dia) — as três primeiras rodadas mediram um produto que mudava debaixo delas

Regra da casa, de novo: nada acima foi reescrito. O que caducou está aqui.

**MEDIDO** por diagnóstico independente, com reprodução em três braços: as
bancadas `tests/unit/test_bluez_config_sh.py` e
`tests/unit/test_doctor_justworks_comportamento.py` executam
`scripts/bluez_config.sh` e `scripts/doctor.sh` **pelo caminho absoluto da
árvore de trabalho**. Nas rodadas 2 e 3 desta entrega, agentes irmãos estavam
mutando esses mesmos arquivos **em paralelo, na mesma árvore** (arrancar a cura
→ rodar → `cp ORIG` de volta). Contagem de execuções de `pytest` com mutação de
OUTRO agente viva: **0** na rodada 1, **8** na rodada 2, **14** na rodada 3.

O experimento de controle, que é o que fecha a questão:

| braço | bancada lê | mutador cicla em | resultado |
|---|---|---|---|
| controle | cópia A | ninguém | 0 falhas / 10 |
| contaminado | cópia A | **cópia A** | 5 falhas / 10, testes **diferentes** a cada vez |
| vizinho | cópia B | cópia A | 0 falhas / 10 |

Carga da máquina e concorrência entre execuções foram **refutadas** como causa
(18 `pytest` simultâneos na árvore real: 0 falhas / 18). O canal era o **arquivo
compartilhado**.

**A contaminação vai nos dois sentidos, e o segundo é o pior.** Mutação alheia
viva produz **vermelho falso** — mordida afirmada que não existe. E um `cp ORIG`
alheio que desfaz a sua mutação antes de o `pytest` rodar produz **verde falso**
— mordida real declarada inexistente. As duas violam a regra "teste tem de
MORDER", e a segunda passa despercebida para sempre.

### A cura (aplicada)

`ARVORE-CONGELADA-01`, em `tests/conftest.py`: as bancadas deixam de ler a
árvore de trabalho e passam a ler uma **cópia tirada uma vez por sessão**. A
mordida não se perde — a cópia sai da árvore como ela está quando o `pytest`
começa, então arrancar uma cura ANTES de rodar continua ficando vermelho; o que
deixa de existir é a janela em que o arquivo muda **durante** a medição.

Efeito MEDIDO da cura, com um mutador ciclando a 2 Hz na árvore durante dez
execuções: as falhas deixaram de ser **sorteadas**. Antes, testes diferentes a
cada rodada; depois, toda rodada vermelha caiu no **mesmo** conjunto de quatro —
exatamente a mordida pretendida da mutação viva. Vermelho reproduzível é
diagnosticável; vermelho sorteado não é.

**O limite, declarado:** congelar torna o veredito COERENTE, não imune. Uma
mutação que já estivesse viva no instante da foto é medida a sessão inteira — e
tem de ser, porque é assim que se prova mordida. Por isso a segunda metade: uma
sonda compara a foto com a árvore no fim da sessão e **REPROVA o run** quando o
produto mudou no meio, dizendo que aquele run não decide nada. Ela compara dois
instantes e não vigia o intervalo: na mesma reprodução acusou 3 das 10.

### A revalidação (feita)

As **nove** mordidas medidas dentro da janela contaminada foram refeitas **em
série, uma por vez, sozinhas na árvore**, com restauração conferida por md5 e
por modo: D1 (`fail`→`pass` no ramo `always`), D2 (detector fora do `main()`),
M1 (backup com resolução de 1 s), o `if (_grupo != "General") next`, P2 (poda
automática de volta no `aplicar`), M6 (sem o `trap`), M7 (promessa única do
`never`), a conferência final do disco, e "o primeiro valor vence". **As nove
mordem.** Saiu uma correção de número: a mutação do grupo derruba **três** casos
da tabela mais o `test_o_veredito_acompanha_o_grupo` (quatro falhas), e não os
"quatro casos" que a rodada 3 registrou.

E saiu uma **retratação**: a rodada 3 afirmou que arrancar o `cmp` de
conferência do backup deixava
`test_backup_parcial_e_apagado_e_o_main_conf_nao_e_tocado` vermelho. **Não
deixa** — medido por terceiro e reproduzido aqui: o shim daquele teste faz o
`cp` sair 1, o `||` curto-circuita e o `cmp` nunca é avaliado. A cura foi
escrever a bancada que faltava (um `cp` que corta o arquivo e **mente** saindo
0), não apagar a frase.

---

## NOTA DATADA — 06/08/2026 — a E1 estava escrita e não chegava à máquina

Regra da casa: *decisão medida não se apaga, ganha nota datada com o que
caducou*. Nada acima foi reescrito. O que caducou está aqui.

### O que foi MEDIDO em 06/08/2026

`/etc/bluetooth/main.conf:25` da máquina dela:

```
JustWorksRepairing=always
```

e a linha está **dentro** do bloco `# >>> hefesto bluetooth >>>` (linha 3) /
`# <<< hefesto bluetooth <<<` (linha 26) — ou seja, **escrita por uma versão
anterior deste próprio projeto**. Não é config de terceiro, não é resíduo de
distribuição: é nossa.

**MEDIDO** também, e é o que explica tudo: pelo carimbo dos backups em
`/etc/bluetooth`, a última vez que o `install.sh` escreveu o bloco foi
**02/08/2026 02:33** (`main.conf.bak.hefesto-1785648797`). Os assets passaram
para `confirm` em **05/08**. **Não houve nenhuma execução do `install.sh` entre
as duas datas.** A E1 mudou o repositório; nada mudou o disco. O mecanismo não
falhou — ele simplesmente nunca rodou, e não havia como saber disso.

### A afirmação de 04/08 que caducou

A caixa **PRECISÃO ANTES DE TUDO** acima diz, conferido em 04/08 às 03:10:

> `/etc/bluetooth/main.conf.d/` está **VAZIO** — o `JustWorksRepairing` **não
> está ativo** aqui e agora

**Isso é falso, e a auditoria olhou o caminho errado.** MEDIDO em 06/08: o
diretório `/etc/bluetooth/main.conf.d/` **não está vazio — ele não existe**
(`ls` responde "diretório inexistente"), e o pacote `bluez` não o cria
(`dpkg -L bluez | grep conf.d` volta vazio). Por isso o `install.sh` sempre usou
o outro caminho, o do bloco apensado — e o `always` esteve **ativo o tempo todo**
em `/etc/bluetooth/main.conf`. A auditoria conferiu o caminho A numa máquina que
só usa o caminho B, e concluiu "não está ativo" de uma ausência que era só do
lugar errado.

A frase seguinte da mesma caixa — *"isto NÃO diminui o achado"* — continua
valendo, e por um motivo mais forte do que ela supunha na época.

### O furo estrutural que isso revelou (e que é pior que o valor errado)

O `install.sh` decidia entre dois caminhos por um único `if -d
/etc/bluetooth/main.conf.d`. Com o diretório **presente**, ele gravava os
drop-ins, imprimia `FastConnectable + JustWorksRepairing via drop-ins
main.conf.d` e **retornava sem nunca abrir o `main.conf`**.

**MEDIDO:** `strings /usr/libexec/bluetooth/bluetoothd` (bluez
`5.86-0ubuntu0.1~hefesto24.04.3`, o backport desta casa) contém **uma** string
de caminho de configuração, `%*s/main.conf`, e **zero** ocorrências de
`main.conf.d`. **SUSPEITA COM MECANISMO** (o `strings` é forte, mas não é
leitura do fonte): este BlueZ não lê `main.conf.d`.

Ou seja: bastava alguém criar aquele diretório — um pacote futuro, outro
projeto, um `mkdir` de quem seguiu um tutorial — para o instalador **anunciar
`confirm` enquanto o `always` seguia vivo no arquivo que o BlueZ lê de fato**.

### O que entrou em 06/08 (E1-bis)

| # | cura | grau |
|---|---|---|
| 1 | a lógica saiu de dentro do `install.sh`/`uninstall.sh` para **`scripts/bluez_config.sh`** (`aplicar` / `remover` / `verificar`), com raiz configurável por `HEFESTO_BT_ETC` | MEDIDO — a bancada roda |
| 2 | o `aplicar` **reconhece e corrige** bloco antigo do próprio Hefesto com valor inseguro, e **diz em voz alta** que corrigiu | MEDIDO |
| 3 | os dois caminhos deixaram de ser `if`/`elif` e viraram **cumulativos**: o `main.conf` é sempre normalizado, e os drop-ins entram por cima quando `main.conf.d` existe. Os dois lugares passam a declarar o mesmo valor | MEDIDO |
| 4 | chave nossa **ativa fora do bloco** é **neutralizada** com a marca `#hefesto-desativou# ` em vez de apagada — e o `remover` **devolve a linha original** | MEDIDO |
| 5 | sentinela de abertura **sem fechamento** faz o script **RECUSAR** em vez de apagar até o fim do arquivo (o `sed '/A/,/B/d'` antigo apagava) | MEDIDO |
| 6 | **um** backup por execução, não um por bloco; e **poda com retenção declarada** (10 mais recentes, `HEFESTO_BT_BACKUPS_MANTER`) | MEDIDO |
| 7 | o priming de `sudo` do `uninstall.sh` passou a conhecer a sentinela **unificada** — antes, numa máquina como a dela, `uninstall.sh --keep-udev` não pedia credencial e **deixava o bloco para trás** | SUSPEITA COM MECANISMO (li a lista inteira; não executei o uninstall) |
| 8 | o `doctor.sh` ganhou `check_bluez_justworks_repairing` — **reprova** (`[FAIL]`) com `always` no disco, e **avisa** quando `confirm` está ativo com o `hefesto-bt-agent.service` fora do ar | MEDIDO no código; o ramo do `always` conferido em bancada |
| 9 | `check_bluez_fastconnectable` deixou de atribuir o bloco a um terceiro (ele só conhecia a sentinela legada e caía no ramo *"já configurado por terceiro"*) | MEDIDO — reproduzi a cadeia de ramos |

### A conta dos backups, e a dívida que ela fecha

**MEDIDO** em `/etc/bluetooth` em 06/08/2026: **37** arquivos
`main.conf.bak.hefesto-*` (23 do install, 14 do uninstall), somando **272 KB**,
mais um `main.conf.bak.claude-1784689791` que **não é de nenhum dos dois
scripts**. `grep -niE "poda|prune|manter os [0-9]+|tail -n \+" install.sh
uninstall.sh scripts/doctor.sh` retornava **zero**: poda não existia em lugar
nenhum. A retenção agora é declarada (10 mais recentes por mtime) e é **cega a
arquivo que não seja nosso** — o `main.conf.bak.claude-*` nunca é tocado, e há
teste que arranca essa garantia.

### O que a troca CUSTA, e é honesto dizer

`always` aceitava **sem depender de ninguém**; `confirm` aceita **só se houver
agente registrado**. A cura troca uma garantia incondicional por uma
condicional, e a condição já falhou duas vezes em 04/08
(`BT-AGENT-TRAVA-O-RESTART-01` e `BT-AGENT-MORTO-FICA-MORTO-01`, ambas anotadas
em `assets/systemd/hefesto-bt-agent.service`). Com o agente morto, o
re-pareamento legítimo **dela** para de funcionar. É por isso que a entrega #8
acima não é decorativa: o `doctor` avisa antes de o controle deixar de conectar.
**MEDIDO em 06/08:** `hefesto-bt-agent.service` está `enabled` e `active`.

### O que continua ABERTO depois desta nota

- a **E2** segue sendo a entrega que fecha o cenário. `confirm` só devolve ao
  BlueZ a decisão de perguntar; quem responde ainda é o `bt-agent`
  `NoInputNoOutput`, que autoriza;
- **DÍVIDA REGISTRADA, MEDIDA:** `assets/bluetooth/` **não é empacotada** em
  formato nenhum (`grep -rn bluetooth scripts/build_deb.sh packaging/debian/*` só
  encontra o `modprobe.d` do btusb). Quem instala pelo `.deb`/`.rpm`/`PKGBUILD`/
  flatpak **nunca recebeu esta configuração** — nem o `always` de antes, nem o
  `confirm` de agora. Fechar isso exige postinst que reescreva um conffile do
  dpkg, e é entrega à parte. O portão novo em `scripts/check_packaging_parity.sh`
  trava o que já é verdade (dono único, chamado pelos dois lados, detector no
  doctor) e **não** finge cobrir o empacotamento;
- **SUSPEITA COM MECANISMO, sem cura nesta leva:** a mesma série de backups
  mostra que o `main.conf` dela **perdeu o template do upstream** — 404 linhas
  em 21/07 19:29, 426 em 22/07 00:09, **3 linhas** em 22/07 01:24. O colapso
  aconteceu na janela do backup com prefixo `claude-`, **não** numa execução do
  `install.sh` (os backups do install de 21/07 mostram o arquivo ainda com 400+
  linhas), e o `awk` do install não tem caminho que apague 400 linhas de
  comentário. O `main.conf.dpkg-dist` íntegro (384 linhas) está ao lado.
  **Nota de 06/08/2026:** os dois pontos desta medição agora estão PROTEGIDOS —
  ver a nota abaixo sobre a poda.

### Nota datada — 06/08/2026: a poda automática de backup foi RETIRADA

A primeira versão do `scripts/bluez_config.sh` podava os
`main.conf.bak.hefesto-*` dentro do `aplicar` e do `remover`, guardando os 10
mais recentes por mtime. **MEDIDO** por simulação só-leitura do pipeline exato
contra o `/etc/bluetooth` dela: a **primeira** execução de `aplicar` apagaria
**27 dos 37 backups**. Entre eles, os dois pontos de medição do colapso descrito
no item acima:

| arquivo | tamanho | quando | seria apagado? |
|---|---|---|---|
| `main.conf.bak.hefesto-1784672963` | 404 linhas, 14797 bytes | 21/07 19:29 | **sim** |
| `main.conf.bak.hefesto-1784694261` | 3 linhas, 59 bytes | 22/07 01:24 | **sim** |

Retenção por mtime **descarta primeiro o que tem mais valor**: o estado
pré-hefesto e o instante do estrago. Os 10 que ficariam são todos pós-colapso,
de 11 a 1395 bytes. O gatilho seria o conselho da própria ferramenta — o
`doctor.sh` manda *"rode ./install.sh"* —, e a regra da casa é **não se apaga
decisão medida**. Cento e poucos quilobytes não valem a única evidência do único
estrago deste projeto ainda sem explicação.

**O que existe hoje, no lugar:**

- `aplicar` e `remover` **reportam** quantos backups há e quantos bytes ocupam,
  e dizem em voz alta que nenhum é apagado automaticamente;
- a poda é um subcomando **explícito**: `bash scripts/bluez_config.sh podar`.
  Ele **simula por padrão** (`--dry-run`); apagar exige `--aplicar`;
- **o mais antigo nunca sai** — é o estado mais próximo do pré-hefesto;
- **conteúdo único nunca sai** — se nenhum outro backup tem os mesmos bytes,
  aquele arquivo é a única cópia daquele estado. É essa regra, e não a retenção,
  que segura os dois arquivos da tabela;
- `HEFESTO_BT_BACKUPS_MANTER` continua existindo, mas só o `podar` a consulta.

Portões: `tests/unit/test_bluez_config_sh.py` (secão 6, com os nomes reais dos
dois arquivos) e `scripts/check_packaging_parity.sh`, que reprova se a poda
automática voltar ou se o subcomando explícito sumir.

### Nota datada — 06/08/2026: `JustWorksRepairing=never` é REBAIXADO, e com aviso

Quem já tinha `never` no `main.conf` escolheu um valor **mais restritivo** que o
`confirm` desta casa: `never` recusa todo re-pareamento por Just Works de quem já
tem bond, sem perguntar a ninguém. O `aplicar` **rebaixa** para `confirm` — mas a
decisão é declarada, não silenciosa. **Por que rebaixar:** com `never`, quando o
bond do controle dela se perde (o caso que a Onda R veio resolver) o
re-pareamento simplesmente não acontece, e o sintoma chega como *"o controle não
conecta mais"*. **O que muda:** a linha dela é **neutralizada**, nunca apagada —
`bluez_config.sh remover` a devolve inteira —, e tanto o `aplicar` quanto o
`doctor.sh` dizem isso na tela, com o comando para desfazer.

---

## S1 — a combinação instalada por padrão remove a última barreira

Três peças, cada uma defensável sozinha, e juntas um buraco:

| peça | onde | o que faz |
|---|---|---|
| `JustWorksRepairing = always` | `assets/bluetooth/hefesto-justworks.conf:28`, instalado por `install.sh:1381` **sem flag** | o BlueZ aceita **re-pareamento** de quem já tem bond, por Just Works |
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
