# INSTALL-QUE-NÃO-CARREGA-01 — as descobertas que nunca viraram código

- **Aberta e executada em:** 07/08/2026, sobre `restauro/inicio-da-sessao`
- **Pedido dela, literal** (citação não se corrige):
  > *"alem de atualizarmos o install com as descobertas que fizemos e ate as
  > que nao foram integradas"* <!-- noqa-acento -->
- **Estado:** **DUAS ENTREGAS APLICADAS** (E1 e E2, com mordida provada por
  arrancamento) e **cinco em lista**, cada uma com o motivo de não ter entrado
- **Método:** leitura pura. Nada foi escrito em hidraw, nenhum serviço
  reiniciado, nenhum controle derrubado, nenhum instalador executado. A máquina
  dela estava com três controles na mesa e o DualSense carregando durante a
  varredura inteira
- **Graus, como manda a casa:** **MEDIDO** = li nesta árvore, hoje, ou vi um
  teste reprovar com a cura arrancada; **SUSPEITA COM MECANISMO** = o caminho
  foi lido e fecha, o efeito não foi observado; **SEM PROVA** = está dito e
  ninguém verificou

---

## O que a varredura procurava, e o que ela achou

A segunda metade do pedido é a difícil: descobertas que **não** foram
integradas. Elas não aparecem em `git log` — por definição, ninguém as
escreveu. Então a busca foi pelo formato delas no acervo: regra que alguém
mediu ser necessária, verificação que um lado faz e o outro não, e passo que
alguém teve de dar à mão.

**O primeiro achado é bom, e precisa abrir o documento para os outros serem
lidos na proporção certa: a dívida antiga do instalador está quase toda paga.**
Reconferido hoje, item a item, contra a
[SIMETRIA-INSTALL-02](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md)
e a [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md),
que eram os dois documentos abertos com mais dívida de instalação:

| item | onde foi aberto | estado hoje (**MEDIDO**) |
|---|---|---|
| fontes que o install põe e o uninstall não tira | SIMETRIA-INSTALL-02 E1 | **paga** — `uninstall.sh:451-453` chama `install_fonts.sh --remove` |
| `purge.sh` aceitava o que não entendia | E3 | **paga** — `scripts/purge.sh:64-68`: `--help` sai 0, desconhecido sai 2 |
| `install_udev.sh` com o mesmo parser frouxo | E3 | **paga** — `scripts/install_udev.sh:43-47` |
| `sudo bash uninstall.sh` sugerido no erro | E4 | **paga** — `grep -n "sudo bash" uninstall.sh` não devolve o script inteiro |
| `--keep-udev` deixava as regras 82/83 órfãs | E2 | **paga** — teste com dono em `test_uninstall_simetrico_ao_install.py` |
| `hefesto-dsx-recover.service` com três histórias | E6 | **decidida pela opção A** — há teste que impede o nome de voltar |
| quatro params órfãos (uninstall desarma, install não rearma) | ÁRVORE-DIVERGENTE-01 | **paga** — `install.sh:642-645` e `:821` |
| portão `-w` em `/sys/module`, falso para ela | ÁRVORE-DIVERGENTE-01 | **paga** — virou portão de existência (`-e`), com o motivo escrito em `install.sh:626-630` |

**Nada abaixo contradiz isso.** As duas entregas desta leva são o que sobra
quando o núcleo está certo — e as duas têm a mesma forma, que é a forma mais
cara de defeito desta casa: **uma cura que foi aplicada em um lugar e não no
gêmeo**.

---

## E1 — a paridade a quente que foi paga em um sentido só

**Registro de origem:** `2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md:114-118`,
o achado AUTO-01.7, que dizia:

> *"O caminho de instalação por pacote escreve os parâmetros a quente
> (`scripts/install-host-udev.sh:306`); o `install.sh` **não**. Todos os
> parâmetros envolvidos são graváveis em tempo de execução."*

**A cura veio, e o `install.sh` alcançou** — o comentário dela está lá, em
`install.sh:619-621`, dizendo com todas as letras que aquilo é *"paridade com o
caminho de instalação por PACOTE (scripts/install-host-udev.sh), que já fazia
isto e o install.sh não"*.

**E aí a casa parou de olhar para o outro lado.** Os parâmetros que nasceram
DEPOIS entraram só no `install.sh`. Medido hoje, comparando os dois conjuntos de
`/sys/module/<mod>/parameters/<p>` escritos por cada script:

| parâmetro | `install.sh` | `install-host-udev.sh` (antes desta leva) |
|---|---|---|
| `hid_nintendo/bt_probe_retries` | sim | sim |
| `hid_nintendo/skip_tx_on_rate_exceeded` | sim | sim |
| `hid_playstation/feature_retries` | sim | sim |
| `hid_playstation/ds4_short_pairing_info` | sim | sim |
| `hid_playstation/ds4_synthetic_mac` | sim | sim |
| `btusb/enable_autosuspend` | sim | sim |
| **`hid_nintendo/usb_cmd_pad_to_report`** | `:643` | **não** |
| **`hid_nintendo/usb_send_conn_status`** | `:644` | **não** |
| **`hid_nintendo/usb_probe_degrade`** | `:645` | **não** |
| **`rtw88_usb/hang_reset`** | `:821` | **não** |

GRAU: **MEDIDO** para as dez linhas.

### Por que isso morde, e não é higiene

O `uninstall.sh` zera os quatro de propósito (`:874-876` e `:913`). Os três do
`hid_nintendo` são lidos **na probe** do módulo, e recarregar módulo é
**proibido** nos dois instaladores — derrubaria os controles em uso. Então a
conf do `modprobe.d`, que traz os três, só vale no **próximo boot**.

O `install.sh` sabe disso e escreve o motivo ao lado da cura, em `:637-641`:
*"O uninstall os devolve a 0, logo o rearme aqui é obrigatório: sem ele o ciclo
uninstall+install deixa o 8BitDo no cabo sem cura até o boot seguinte."*

**A frase vale igual para quem instalou por pacote — e para essa pessoa o rearme
não existia.** No intervalo entre o `uninstall.sh` e o boot seguinte, o 8BitDo
Pro clone (057E:2009) no cabo volta a morrer na probe — *"Failed to get joycon
info; ret=-110"*, sem driver, sem hidraw, sem input, sem LEDs.

E o `install-host-udev.sh` não é caminho hipotético: é o que o próprio
`scripts/doctor.sh` manda rodar, em `:3211` e `:3271`, para quem instalou por
`.deb`/`.rpm`/Arch.

O `hang_reset` tem um agravante próprio, e ele é **MEDIDO**: é o **único**
parâmetro desta casa sem conf de `modprobe.d`. `ls assets/modprobe.d/` traz
`btusb`, `hid-nintendo` e `hid-playstation` — não há nenhum do `rtw88`. Ou seja,
o valor só vem do default compilado (`Y`) ou de uma escrita a quente. Depois do
`uninstall.sh`, o caminho de pacote reinstalava o módulo patchado e deixava a
detecção rodando **com o reset desligado**.

### O que entrou

`scripts/install-host-udev.sh` passa a escrever os quatro, na forma que o
próprio arquivo já usava (best-effort, `2>/dev/null || true`, portão de
existência).

### A mordida

`tests/unit/test_paridade_quente_dos_instaladores.py`. Ele **não** compara duas
listas escritas à mão — foi digitar a lista à mão que deixou os órfãos da
ÁRVORE-DIVERGENTE-01 passarem despercebidos. Ele deriva do `uninstall.sh` o
conjunto de parâmetros desarmados e exige que **os dois** instaladores rearmem
cada um, com uma única exceção declarada (o `snd_usb_audio/quirk_flags`, que o
`install.sh` rearma pelo dono do valor, `install_snd_quirk.sh --runtime`) — e
essa exceção tem teste próprio, para não virar buraco por omissão.

**Arrancada e devolvida, hoje:** tirando as três linhas do patch 0003, o teste
reprova nomeando os três; tirando a do `hang_reset`, reprova nomeando
`hang_reset`. Devolvidas, verde. Ele descarta linhas de comentário de propósito:
um parâmetro citado num comentário passaria por rearme sem nenhuma escrita
acontecer.

---

## E2 — a licença que não viajava pelo caminho que ela usa

**Registro de origem:** a [CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md),
fechada hoje mesmo, e o `LICENSES/README.md` que nasceu com ela.

A CR-05 fez a parte difícil: `LICENSES/` existe, com texto canônico e SHA-256
registrado, e **os cinco alvos de empacotamento** que carregam `assets/dkms/`
passaram a carregar o diretório junto. O `LICENSES/README.md` enumera onde os
textos viajam e diz, com razão, quem **não** carrega e por quê (o wheel e o
AppImage não levam `assets/dkms/`).

**Faltou uma pergunta, e ela é a que atinge a máquina dela:** *quais caminhos
põem os fontes GPL-2.0 no disco?* São dois, e nenhum é empacotamento —
`./install.sh` e `scripts/install-host-udev.sh`. Os dois chamam a mesma
`dkms_install_patched_module`, que em `scripts/dkms_lib.sh:249` copia
`assets/dkms/<mod>/.` para `/usr/src/<pkg>-<ver>/` e mais nada.
`grep -rn LICENSES install.sh scripts/*.sh` devolvia **zero**. GRAU: **MEDIDO**.

Não é lacuna de doutrina — é lacuna de enumeração: o `README.md` não os listava
nem como carregadores nem como exceção justificada. Ficaram fora da conta.

### O que entrou

`scripts/dkms_lib.sh` ganha um resolvedor (`_dkms_licenses_dir`, com os mesmos
três contextos que o resto da casa já resolve: checkout, `/usr/share`, `/app`) e
um passo `1-bis` que copia `LICENSES/` para dentro de `/usr/src/<pkg>-<ver>/`.

Duas propriedades que valem estar escritas:

1. **A simetria não custa uma linha no `uninstall.sh`.** O `dkms remove --all`
   apaga `/usr/src/<pkg>-<ver>` inteiro (o próprio `uninstall.sh:836-838`
   registra isso) — a licença sai junto com o fonte que ela cobre.
2. **É best-effort integral.** O contrato da biblioteca é que nada ali aborta o
   install, e licença ausente não vale um módulo a menos.

### A armadilha, que é maior que a entrega

O passo 1 decide se re-sincroniza comparando `diff -rq` entre origem e destino.
`LICENSES/` existe **só no destino**. Sem excluí-lo, o `diff` acharia diferença
em **toda** execução, e cada install passaria a `dkms remove --all` + recopiar +
**reconstruir os três módulos DKMS** — o oposto exato do contrato de
idempotência escrito no cabeçalho da biblioteca. Daí o `-x LICENSES` ao lado do
`-x patch` que já existia.

E uma segunda, que **um teste que já existia pegou primeiro**: copiar a licença
a cada execução deixava
`tests/unit/test_dkms_lib.py::test_segunda_chamada_e_no_op_real` vermelho, e ele
estava certo — a reexecução não pode repetir passo nenhum. A cópia ganhou guarda
de `diff` própria. **Fica registrado como acerto do teste antigo, não como
descuido do novo:** foi ele que impediu a entrega de nascer com um defeito.

### A mordida

`tests/unit/test_licenca_viaja_com_o_fonte_dkms.py`, por **execução** da
biblioteca real (raízes em `tmp`, stubs de `sudo`/`dkms`, sem root, sem tocar o
sistema) — não por busca de trecho, que é como o portão gêmeo da CR-05 funciona
e é o certo para ele.

**Arrancada e devolvida, hoje:** apagar o bloco `1-bis` reprova em
`test_licenca_chega_ao_usr_src_na_execucao`; tirar o `-x LICENSES` do `diff`
reprova em `test_a_licenca_no_destino_nao_quebra_o_no_op_da_segunda_chamada`,
flagrando o `dkms remove` da segunda chamada. Há ainda um teste de controle
(`test_o_repositorio_tem_o_que_copiar`): sem `LICENSES/` no repositório os
outros passariam por vacuidade.

O `LICENSES/README.md` ganhou as duas linhas na tabela e uma **nota datada** com
o que a tabela original respondia — a regra da casa é que decisão medida não se
apaga.

---

## O que NÃO entrou, e por quê — a lista que é dela

Cinco achados reais que não viram código nesta leva. Cada um diz o que é, onde
está registrado, o que o install faz hoje, e o motivo exato de estar aqui e não
lá em cima.

### L1. A ausência do drop-in 51 continua indistinguível de escolha dela

- **Onde:** [DROPIN-AMBIGUO-01](2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md),
  **aberta**, entregas E1 a E5
- **GRAU:** MEDIDO para o mecanismo (`scripts/doctor.sh:544-548` lê a ausência
  do drop-in 51 como promoção explícita)
- **O que o install faz hoje, e é melhor do que a sprint registra:** o passo 10
  chama `scripts/fix_wireplumber_default_source.sh --install`, e esse script
  **honra** `HEFESTO_DUALSENSE4UNIX_DUALSENSE_MIC_INTENDED` desde sempre
  (`:71-76`: com a variável ligada, `install` vira `enable-mic`). Ou seja, a
  promessa do cabeçalho do `install.sh:203` **é cumprida**, por delegação.
  Conferido por leitura; **SEM PROVA** por execução — rodar aquele script mexe
  no WirePlumber da sessão dela, e a máquina está em uso
- **O que falta é o que a sprint chama de E1:** a marca **persistente** do
  gesto de promover. A variável de ambiente morre com o terminal; quem rodou
  `hefesto mic promote` numa terça não tem como o install de quinta saber disso
- **Por que não entrei:** a própria sprint diz que o nome, o lugar e a migração
  (E4) são decisão de quem a executar, e que escolher a migração em silêncio
  *"seria reescrever a escolha dela em silêncio"*. Inventar a marca aqui seria
  exatamente isso. **PRECISA DA PALAVRA DELA**

### L2. O salva-vidas de bonds que ninguém aciona

- **Onde:** [BONDS-QUE-SOBREVIVEM-01](2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md),
  defeito D1, **aberta**
- **GRAU:** MEDIDO — o `install.sh` copia `bt_bonds_restore.sh`, o
  `uninstall.sh` o apaga, e **nenhum timer, nenhum `ExecStopPost`, nenhum
  caminho de código o invoca**
- **O que o install deveria fazer:** ou instalar um acionador, ou parar de
  fingir que a corrente existe
- **Por que não entrei:** instalar acionador é criar unit nova de sistema que
  restaura credencial de pareamento sozinha, numa máquina onde o `bluetoothd`
  aborta quatro vezes em cinco dias
  ([o defeito do BlueZ](../estudos/2026-08-07-o-defeito-do-bluez-que-ela-lembrou-e-os-outros-cinco.md),
  §3A). O mesmo documento mede que o restaurador **sobrescreve chave nova com
  chave velha** (D3) — automatizá-lo antes de curar o D3 é armar o laço de
  autenticação que ele existe para evitar. **PRECISA DA PALAVRA DELA**

### L3. A procedência das regras que o install grava em `/etc` aponta para o vazio

- **Onde:** [a economia de energia e a bancada](../estudos/2026-08-07-a-economia-de-energia-e-a-bancada.md),
  seção "O que fica ABERTO", último item
- **GRAU:** MEDIDO — `assets/81-hefesto-usb-power.rules:2`,
  `assets/81-hefesto-usb-host-power.rules:2`,
  `assets/modprobe.d/hefesto-btusb-no-autosuspend.conf:8` e
  `assets/bluetooth/hefesto-fastconnectable.conf:2` citam estudos
  `2026-07-18-*.md` que **não existem nesta árvore** (`find docs -iname
  "*2026-07-18*"` devolve vazio; eles vivem na tag `arquivo/processo-pre-1.0`)
- **Por que o portão não pega:** `scripts/validar-referencias-docs.py` só varre
  `docs/`. As regras estão corretas e medidas; é a procedência que aponta para
  lugar nenhum — e ela é lida no `/etc` de quem for auditar a máquina
- **Por que não entrei:** a varredura mostrou que **não são quatro arquivos, são
  doze** — `assets/hefesto-steam-input-guard.{service,path,timer}` citam uma
  sprint `FEAT-STEAM-INPUT-SELF-HEAL-01.md` inexistente,
  `assets/systemd/hefesto-hidraw-broker.{service,socket}` e
  `assets/systemd/hefesto-bt-agent.service` citam estudos de 19 e 20/07 também
  arquivados. Corrigir doze arquivos de `assets/` e estender o portão a eles é
  uma leva inteira, com decisão embutida (apontar para o caminho na tag, como o
  estudo do BlueZ faz, ou tirar a citação). **SEGURO, mas é outra leva** — não
  cabia sem inchar esta

### L4. O `nix run` do README continua impossível por construção

- **Onde:** SIMETRIA-INSTALL-02 E5, metade 2
- **GRAU:** MEDIDO — `packaging/nix/package.nix:79` ainda tem `lib.fakeSha256`
- **Por que não entrei:** é o que a própria sprint escreveu — não há `nix`
  nesta máquina, e *"gravar um hash que ninguém consegue conferir troca um erro
  visível por um erro silencioso"*. **Não é entregável desta bancada**

### L5. Os presets de fábrica que são biografia dela

- **Onde:** [o que só funciona na máquina dela](../estudos/2026-08-06-o-que-so-funciona-na-maquina-dela.md),
  §3.1
- **GRAU:** MEDIDO — `scripts/install_profiles.sh` semeia 12 JSONs, e quatro são
  dela: `sackboy_nativo`, `point_and_click`, `bow` e o `meu_perfil` com
  prioridade 1, que na máquina de outra pessoa vira o catch-all efetivo do
  desktop, com a lightbar azul dela e o LED de jogador 3
- **Por que não entrei:** o mesmo estudo diz que a pergunta que decide isto está
  em aberto e é dela — *"o Hefesto é a ferramenta DELA, ou é um produto para
  outras pessoas?"*. **PRECISA DA PALAVRA DELA**, e a resposta muda cinco
  lugares de uma vez, não este

---

## Como ela confere na tela

Os três primeiros são de olho, sem terminal.

1. **Nada muda na janela dela.** Esta leva não toca `src/`, nem `gui/`, nem o
   daemon. Se qualquer aba mudou de aparência, ela extrapolou e reprova.
2. **Nada muda na máquina dela agora.** As duas entregas só têm efeito na
   próxima execução de um instalador. E a E1 mexe **apenas** no
   `scripts/install-host-udev.sh`, que é o caminho de quem instalou por pacote —
   ela instala do checkout.
3. **Os três controles continuam na mesa.** Nenhum módulo foi carregado ou
   descarregado, nenhum parâmetro de `/sys` foi escrito por esta leva.
4. **Quando ela rodar `./install.sh` de novo**, o passo dos módulos DKMS tem de
   imprimir `source ... já sincronizado` como sempre — e **não** um rebuild. Se
   aparecer `dkms remove`/rebuild dos três módulos, o `-x LICENSES` saiu do
   lugar e a E2 reprova na hora.
5. Depois disso, `ls /usr/src/hefesto-hid-nintendo-*/LICENSES/` tem de mostrar
   `GPL-2.0.txt`, `BSD-3-Clause.txt` e `README.md`.

## O que eu NÃO medi

- **Nenhum instalador foi executado.** As duas entregas foram conferidas por
  leitura dos scripts e por execução da biblioteca DKMS em `tmp`, com stubs. O
  ciclo `install` → `uninstall` real continua proibido nesta máquina, pelo mesmo
  motivo de sempre: o daemon e a janela dela estão vivos
- **O caminho de pacote nunca rodou aqui.** A E1 foi provada por comparação de
  texto e por teste; que ela cure o 8BitDo clone numa máquina instalada por
  `.deb` é **SUSPEITA COM MECANISMO** — o mecanismo é o mesmo que o `install.sh`
  já usa e mediu, mas não há máquina de pacote nesta bancada
- **Se `LICENSES/` chega ao `/usr/src` de verdade.** Provado com `HEFESTO_DKMS_SRC_ROOT`
  apontado para `tmp`. O `/usr/src` real exige `sudo` e um `dkms` de verdade
- **A execução do `fix_wireplumber_default_source.sh`** com a variável de
  ambiente ligada (a base do L1). Ler o código fecha; executar mexeria no áudio
  da sessão dela

## Relacionado

- [O que existe e não chega — a cobertura do install](../estudos/2026-08-07-O-QUE-EXISTE-E-NAO-CHEGA-a-cobertura-do-install.md)
  — **o vizinho desta leva**, escrito no mesmo dia e a partir da outra metade da
  pergunta dela. Ele audita 40 curas e acha 13 que não chegam inteiras; esta
  sprint entrega duas que ele não cobre (ele não cita `install-host-udev.sh`,
  nem os params a quente, nem o `LICENSES`). Os dois documentos se citam de
  propósito: a casa já pagou caro por *"três fontes que não se citam"*
- [SIMETRIA-INSTALL-02](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md)
  — a régua de simetria que esta leva aplica ao segundo instalador
- [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md)
  — a contagem de params órfãos que originou a regra do `9c944a8`
- [AUTO-01](2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md) — o item AUTO-01.7, a
  paridade que ficou pela metade
- [CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md) — a proveniência
  que criou o `LICENSES/`
- [a economia de energia e a bancada](../estudos/2026-08-07-a-economia-de-energia-e-a-bancada.md)
  — de onde sai o L3
