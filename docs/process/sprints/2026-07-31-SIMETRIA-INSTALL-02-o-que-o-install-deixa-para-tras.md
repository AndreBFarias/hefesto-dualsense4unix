# SIMETRIA-INSTALL-02 — o que o install deixa para trás

- **Status:** ABERTA — documento de medição e plano. Nada de código nesta rodada
- **Prioridade:** MÉDIA. Nenhum item desta sprint quebra a instalação que está
  rodando na máquina dela agora. São bordas: o que sobra depois de desinstalar,
  o que acontece quando alguém digita uma flag errada, e o que o projeto promete
  a quem não é ela
- **Aberta em:** 31/07/2026, a partir da auditoria de treze agentes
  ([estudo](../estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md)),
  com o HEAD em `7bd0cb7` e o daemon dela vivo — nada foi executado que mude o
  estado do sistema
- **Sucede:** a cura já paga do `BUG-UNINSTALL-HELP-DESINSTALA-01`, escrita no
  próprio `uninstall.sh:145-150`. Não existe um documento "SIMETRIA-INSTALL-01":
  o -01 desta linhagem foi pago em código, e é dele que sai a régua que esta
  sprint aplica aos scripts que ficaram de fora
- **Relacionada:**
  [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md),
  de onde vêm o B2 (`:149-154`), o B4 (`:166-172`) e o bloco D (`:209-216`); e o
  [índice pós-v0.4.0](2026-07-30-INDICE-as-tres-faixas-depois-da-v040.md), que
  reconfirmou os três em 30/07 (`:277-283`, `:292-295`)
- **Regra da casa que esta sprint aplica:** *uninstall simétrico ao install* —
  registrada no próprio código, em `uninstall.sh:526`
  (`simetria — feedback_uninstall_simetrico_default`)

## Antes de qualquer defeito: o que a medição de hoje diz que está certo

Isto abre o documento de propósito, porque muda como as entregas devem ser
lidas. **O sistema instalado dela é espelho do repositório**, medido hoje:

| O que | Medido | Resultado |
|---|---|---|
| Regras udev | `ls /etc/udev/rules.d` | 17 arquivos, **14 do hefesto** (os outros três são `60-openrgb`, `99-storage-no-link-pm` e `99-usb-kill-autosuspend`, de terceiros), byte a byte iguais a `assets/` |
| Units de sistema | `systemctl list-unit-files 'hefesto*'` | 7 units, nenhuma órfã |
| Units de sessão | `systemctl --user list-unit-files 'hefesto*'` | 5 units |
| Helpers BT | `sudo ls /usr/local/lib/hefesto-dualsense4unix/` | os 7 `bt_*.sh` + o broker, todos de 30/07 13:03 |
| Portão de paridade | `bash scripts/check_packaging_parity.sh` | **exit 0** — "paridade de empacotamento OK" |
| O desastre histórico | `uninstall.sh:145-189` | curado: `--help` sai 0 (`:182`), argumento desconhecido aborta com 2 sem tocar em nada (`:183-187`) |

E a simetria tem teste com dono: `tests/unit/test_uninstall_simetrico_ao_install.py`
cobre as regras udev nos dois sentidos (`:52` e `:60`) e os helpers BT (`:81`).
O arquivo abre explicando por que existe: *"Foi o que aconteceu ao acrescentar
`82-nintendo-pro-nosniff.rules`"* (`:9`).

**Nada nesta sprint contradiz isso.** As seis entregas abaixo são o que sobra
quando o núcleo está certo: um artefato que o install põe e o uninstall não
tira, uma flag que preserva metade do que promete, dois scripts que aceitam o
que não entendem, uma mensagem de erro que ensina o comando errado, uma promessa
de README impossível por construção, e um arquivo que três documentos desta casa
descrevem de três jeitos incompatíveis.

## Onde este documento discorda do auditor, e por quê

Duas correções de citação e um reenquadramento. A regra é que evidência entra
aqui só depois de eu abrir o arquivo na linha citada.

1. **`scripts/install_udev.sh:23` → `:22`.** O `*)` que só avisa está na linha
   **22**; a 23 é o `esac`. Corrigido em toda a E3.
2. **`PROMESSA-NÃO-CUMPRIDA-01:215` cita `package.nix:74-76`; hoje é `:79`.**
   A linha andou. O documento de 26/07 não está errado — envelheceu. A E5 usa o
   número de hoje e registra o antigo.
3. **O B2 (E6) segue o verificador, não o auditor de instalação.** O auditor
   classificou como "asset órfão de instalador, confuso para quem mantém, inócuo
   em runtime". O agente que remediu as pendências mediu outra coisa e é ela que
   importa: o `doctor.sh` **ensina a instalar à mão** a unidade que o
   storm-audit de 26/06 classificou como *realimentação positiva do storm*. O
   asset órfão custa confusão; o conselho custa a noite dela, porque ele só
   aparece num dia de `-71`. Sigo o verificador porque a versão dele é a que
   pode machucar. Detalhe que **nenhum dos dois** citou e que muda a entrega:
   `doctor.sh:3100` já declara, em comentário, *"rede de segurança (watcher) —
   NÃO é a solução, só mitigação"*. O conselho não é irresponsável; ele é
   **isolado**. Três fontes que não se citam.

---

## E1. As fontes que o install põe e o uninstall nunca tira

É a única assimetria nova de verdade, e ela viola diretamente a regra da casa.

**O que o install faz.** O passo 4e (`install.sh:2059`, bloco em `:1957-1972`)
roda por default — o opt-out é `--no-fonts`, documentado no cabeçalho em `:130`,
com a variável nascendo em `:195` e o parse em `:228`. A chamada é best-effort
por decisão escrita em `:1951-1956` (*"Fonte é acabamento, não requisito"*), e
`scripts/install_fonts.sh` grava em
`~/.local/share/fonts/hefesto-dualsense4unix` (`install_fonts.sh:52`) quando não
acha pacote de distro.

**O que o uninstall faz.** Nada. `grep -i font uninstall.sh` devolve **três**
linhas, todas comentário sobre `dkms.conf` ser "fonte da verdade" (`:796`,
`:853`, `:887`). `grep -i font scripts/purge.sh` devolve **zero** — e o
`purge.sh` se anuncia, na própria linha 2, como *"descontaminação TOTAL"* que
*"remove TODAS as formas de instalação"* (`:2-7`).

**O removedor já existe, pronto e testado no desenho.** `install_fonts.sh:86`
tem `--uninstall|--remove) MODO="remover"`, e a função `remover()` (`:233-249`)
apaga **só** o `DEST_DIR` (`rm -rf` em `:239`), com a razão escrita ao lado em
`:235-238`: fonte que veio de pacote da distro sai pelo gerenciador de pacotes,
nunca por aqui. E `:245-247` ainda imprime o `apt remove` para quem quiser tirar
as famílias à mão. Ou seja: falta **uma linha de chamada**, não um recurso.

**Na máquina dela isto não morde, e é importante dizer.** Medido hoje:
`~/.local/share/fonts/hefesto-dualsense4unix` **não existe**; `dpkg -l` mostra
`fonts-jetbrains-mono 2.304+ds-4` e `fonts-space-grotesk-ttf 2.0.0-0ubuntu2`;
`fc-list` acha 20 faces das duas famílias. As fontes dela vieram por pacote, e o
`remover()` não encostaria nelas. Quem paga é quem instala pelo caminho de
download — o caminho normal em distro sem esses pacotes.

**O portão de paridade não cobre isto.** `grep -i font
scripts/check_packaging_parity.sh` devolve 5 linhas (`:319`, `:361`, `:369`,
`:412`, `:456`) e **nenhuma** é fonte tipográfica: são as *fontes* (o
código-fonte) dos módulos DKMS. Um falso positivo de português que esconde a
lacuna de quem for procurar por grep.

**Entrega.** O `uninstall.sh` passa a chamar
`bash scripts/install_fonts.sh --remove`, best-effort, no mesmo molde da chamada
do install; e as fontes entram no `check_packaging_parity.sh`.

**Aceite:** numa máquina **sem** os pacotes da distro, o ciclo
install → uninstall deixa `~/.local/share/fonts/hefesto-dualsense4unix`
inexistente e `fc-list | grep -c "Space Grotesk"` em 0. Na máquina **dela**, o
mesmo uninstall imprime `nada a remover` e o `fc-list` continua com as 20 faces
— nenhum pacote da distro é tocado.

**Mordida:** o teste vai em
`tests/unit/test_uninstall_simetrico_ao_install.py` e tem de contar só as linhas
que **executam** o script, nunca as que o citam. Esse cuidado não é teoria: o
teste gêmeo do lado do install (`test_fonte_padrao_01_e_cura_do_fix_mic.py`,
`_invocacoes` em `:703-721`) documenta ter caído exatamente nessa armadilha, com
a medição ao lado — *"Medido arrancando: 9 testes passaram com o install sem
instalar fonte nenhuma"* (`:706-711`). A cura arrancada aqui é apagar a linha
`bash scripts/install_fonts.sh --remove` do `uninstall.sh` deixando o nome num
comentário: **o teste tem de ficar vermelho**. Se ficar verde, ele está medindo
ortografia.

**Risco:** baixo. É uma chamada protegida por `|| true`, para um script que sai 0
por contrato (`install_fonts.sh:46-48`) e que só apaga o diretório que o próprio
projeto criou.

---

## E2. `--keep-udev` preserva as regras e mata os alvos delas

Quem pede `--keep-udev` está pedindo para o comportamento continuar. Hoje ele
recebe metade.

**O gate.** `uninstall.sh:453` (`if [[ "${REMOVE_UDEV}" -eq 1 ]]`) protege o
bloco que apaga as regras — e as 82, 83 e 84 estão lá dentro (`:486-488`).

**O bloco que não pergunta.** O bloco ONDA-R2 abre em `uninstall.sh:622` com
`if sudo -n true 2>/dev/null; then` e **não consulta `REMOVE_UDEV`**:
`grep -n REMOVE_UDEV uninstall.sh` devolve `138, 174, 175, 242, 244, 453, 522` —
a 622 não está na lista. Esse bloco remove as units de snapshot (`:629-632`) e
os sete helpers (`:645-651`), com `bt_nosniff_now.sh` na `:650`.

**São exatamente os alvos das regras que ficaram.**

| Regra preservada | Linha | O que ela chama | Quem apaga |
|---|---|---|---|
| `82-nintendo-pro-nosniff.rules` | `:23-24` | `RUN+="/usr/local/lib/hefesto-dualsense4unix/bt_nosniff_now.sh"` | `uninstall.sh:650` |
| `83-hefesto-bond-snapshot.rules` | `:26` | `RUN+="/usr/bin/systemctl start --no-block hefesto-bt-bonds-snapshot.service"` | `uninstall.sh:629` |
| `84-nintendo-pro-variant.rules` | — | **não tem `RUN+=`** (só `ENV{}` e `SYMLINK+=`, `:59-68`) | não fica órfã |

Corrijo aqui uma imprecisão que vinha do achado: **a 84 não órfã ninguém**. Ela
entra na entrega por outro motivo, abaixo.

**O sintoma tem forma conhecida, e ela está no journal dela.** Não reproduzi as
82/83 órfãs — para isso eu teria de quebrar a instalação que está rodando. Mas o
`udev` registra falha de `RUN+=` numa linha que já existe no journal desta
máquina, de outro dono: `jul 30 12:55:00 (udev-worker)[424002]: event260:
Process '/bin/input-remapper-control ...' failed with exit code 4`. É essa a
linha que a 82 passaria a produzir a cada device HID por Bluetooth, e é por isso
que o efeito não é só "não funciona": é ruído permanente no log de quem
desinstalou.

**E o efeito silencioso é o que interessa.** Sem `bt_nosniff_now.sh`, o Pro
Controller volta a aceitar sniff na borda da conexão — a cura de raiz da queda
sob carga, medida em 22/07. Sem a unit, o snapshot de bonds na borda para. As
duas morrem sem avisar ninguém.

**A dica manual está incompleta.** `uninstall.sh:515-516` imprime, para quem usou
`--keep-udev`, o `sudo rm` de limpeza posterior. A linha cita 70, 71 (uinput e
uhid), 72 a 81, o `modules-load` e o `modprobe.d` — e **não cita 82, 83 nem 84**.
As três regras mais novas ficam fora da única instrução escrita.

**E a casa já decidiu como resolver este formato de problema.** O bloco
`:519-528` conta a decisão do `BUG-UNINSTALL-STORM-CONF-ORPHAN-KEEP-UDEV-01`: o
`storm.conf` *"não é uma regra udev: é uma cura de `/etc/modprobe.d` com ciclo
de vida PRÓPRIO"*, então sai **sempre**, independente do `--keep-udev`, e o
comentário registra que antes *"nem o texto do 'para remover depois' o citava"*.
É o mesmo desenho, com outros arquivos. Isto não é lapso novo: é uma decisão que
não foi estendida às regras-cola.

**Entrega — e ela é uma escolha, não duas.** As 82 e 83 são regras-cola (existem
só para chamar um alvo), não regras de permissão. Seguindo o precedente do
`storm.conf`, o caminho coerente é **as duas saírem junto com os alvos, mesmo com
`--keep-udev`**. A alternativa (preservar os alvos quando `--keep-udev`) também
fecha o buraco, mas cria um segundo significado para a flag e um segundo lugar
para esquecer. Em qualquer dos dois casos, a lista de `:516` passa a ser gerada
a partir do que ficou, em vez de escrita à mão.

**Aceite:** depois de `./uninstall.sh --keep-udev --yes` numa máquina de teste,
nenhuma regra em `/etc/udev/rules.d` tem `RUN+=` apontando para caminho
inexistente; e o texto impresso lista exatamente as regras que ficaram, sem
nenhuma faltando e nenhuma sobrando.

**Mordida:** dois testes, e eles mordem coisas diferentes.

1. **O que morde comportamento.** Um teste que lê `assets/*.rules`, extrai todo
   `RUN+="<caminho>"`, e exige que, para cada alvo, o `uninstall.sh` decida o
   destino da regra e do alvo **no mesmo gate**. Cura arrancada: mover a remoção
   da 82 para dentro do `REMOVE_UDEV` deixando a `:650` fora — o teste tem de
   reprovar. Este é o teste que impede o defeito de voltar por outra porta.
2. **O que morde só texto, e por isso é declarado como tal.** Toda regra de
   `assets/` aparece na dica de `:516`. Cura arrancada: tirar `82` da linha →
   vermelho. Ele não prova nada sobre execução; existe para a dica não envelhecer
   de novo.

**Risco:** baixo-médio. O que muda de verdade é o **significado** de uma flag que
já está publicada. Se a escolha for as regras-cola saírem sempre, isso tem de
estar escrito no `--help` (`uninstall.sh:159`) e na dica impressa, senão a
próxima pessoa a ler `--keep-udev` vai entender outra coisa — que é exatamente
o defeito de hoje, invertido.

---

## E3. O script mais destrutivo da casa aceita o que não entende

`scripts/purge.sh` tem 153 linhas e se anuncia como *"descontaminação TOTAL"*
(`:2`). O parser dele é este, em `:31-39`:

```
        *) printf '[purge] aviso: argumento desconhecido: %s\n' "$arg" ;;
```

Linha 37. **Sem `exit`.** E não existe case para `--help`/`-h`, então
`./scripts/purge.sh --help` — o reflexo de qualquer pessoa diante de um script
novo — cai no aviso e **segue** para `main()` (`:127`).

**A mitigação é real e tem de constar.** `:129-133` faz o prompt
`[y/N]` com default N antes de qualquer ação. Quem digitar `--help` sozinho vê a
pergunta e responde não. **O buraco é a combinação:** `:129` pula o prompt quando
`AUTO_YES=1`, então `--yes` legítimo mais um typo (`--dry-rum` em vez de
`--dry-run`) executa o wipe sem confirmação, com o aviso rolando para fora da
tela. E o wipe é de verdade: `:81` chama
`bash uninstall.sh --udev "${cfg_flag}" ... --yes`.

**Esta é a classe de acidente que a casa já pagou para curar.** O texto está no
`uninstall.sh:145-150`, e vale copiar inteiro porque é o argumento desta
entrega:

> *"não havia `--help`, e argumento desconhecido só imprimia um aviso e SEGUIA
> desinstalando. Ou seja: `./uninstall.sh --help` — o reflexo de qualquer pessoa
> diante de um script novo — apagava a instalação inteira. (...) Um
> desinstalador é destrutivo por natureza: na dúvida sobre o que a pessoa quis
> dizer, a resposta certa é não fazer nada."*

O `install.sh` recebeu a mesma cura, com o identificador próprio
(`BUG-INSTALL-ARG-DESCONHECIDO-SILENCIOSO-01`, `install.sh:260-268`). O
`purge.sh` — mais destrutivo que os dois — ficou de fora das duas passadas.

**Na mesma passada, o `install_udev.sh`.** `scripts/install_udev.sh:22` tem o
mesmo `*)` que só avisa (e a `:23` é o `esac` — o achado citava a linha errada).
Ali é **inócuo**: o script só reaplica regras e recarrega o udev, e o pior caso
é a pessoa achar que passou uma flag que não existe. Entra por política, não por
risco: manter dois padrões de parser na mesma pasta é o que faz o próximo script
nascer com o frouxo. O `install_udev.sh` também não tem `--help`.

**Entrega.** Replicar no `purge.sh` o padrão do `uninstall.sh`: `uso()` alimentado
pelo próprio cabeçalho (as linhas `:2-20` já são um texto de ajuda pronto),
`--help`/`-h` imprime e sai 0, argumento desconhecido aborta com 2 sem tocar em
nada. Idem em `install_udev.sh:19-24`.

**Aceite:** `./scripts/purge.sh --help` imprime as flags e sai 0 **sem** prompt;
`./scripts/purge.sh --dry-rum --yes` sai 2 sem criar backup, sem chamar o
`uninstall.sh` e sem tocar em `/etc`; `bash scripts/install_udev.sh
--disable-usb-audi` sai 2 sem copiar regra nenhuma.

**Mordida — e o desenho dela importa mais que o de costume, porque o teste roda o
script mais perigoso do repositório.** O teste executa
`bash scripts/purge.sh --dry-rum --dry-run` num subprocesso e exige **exit 2**.
Com a cura arrancada, o `--dry-rum` vira aviso, o `--dry-run` liga o modo
simulado, todo `run()` (`:42-48`) só imprime, e o script sai **0** — vermelho.
Sem a cura o teste falha; com a cura o teste passa; e em nenhum dos dois casos
ele muta o sistema, porque o `--dry-run` está sempre presente. Conferi que todas
as chamadas destrutivas de `main()` passam por `run()`: `backup_profiles`
(`:58-59`), `run_uninstall` (`:81`), `reinforce_leftovers` (`:92-107`),
`purge_deb` (`:115`), `purge_flatpak` (`:123`) e o reforço do Steam Input
(`:143`). Complemento barato, no molde de
`test_install_respeita_o_nao_e_help_completo.py:264-270`: o corpo do `*)` do
parser contém `exit 2`.

**Risco:** baixo em mecanismo — são dois ramos de `case`. O risco real é de
hábito: quem hoje digita `purge.sh --forca` recebe um aviso e o wipe; amanhã
recebe exit 2 e tem de ler. É esse o objetivo.

---

## E4. A mensagem de erro que ensina a rodar o desinstalador como root

`uninstall.sh:466-469`: quando o `sudo -n true` falha no bloco udev, o script
imprime

```
        log "      rode: sudo bash $0 ${*:-} (ou re-execute interativamente)"
```

**A primeira metade da sugestão está errada, e desta vez eu medi em vez de
inferir.** Na máquina dela, hoje: `sudo printenv HOME` devolve **`/root`**
(`/etc/sudoers:9` tem `Defaults env_reset`). O achado original dizia que isto
era inferência da lição de 25/07 sobre o install; não é mais.

**O tamanho do estrago.** O `uninstall.sh` tem **56** referências a `${HOME}` e
**12** chamadas `systemctl --user`. Os alvos de usuário estão declarados juntos
em `:109-131` — `DESKTOP_TARGET`, `ICON_TARGET`, `LAUNCHER`, `BIN_SYMLINK`,
`HOTPLUG_UNIT_TARGET`, os três drop-ins do WirePlumber e o `environment.d` do
modo-jogo — e o backup de configuração em `:1183-1195` monta o caminho a partir
de `${HOME}` também. Rodado com `HOME=/root`, o desinstalador limpa o `/etc`
direitinho e **não remove nada do HOME real dela**: os 5 units de sessão que
`systemctl --user list-unit-files 'hefesto*'` lista hoje sobreviveriam, junto do
atalho, do wrapper e dos drop-ins. Com `--purge-config`, o backup e a purga
aconteceriam em `/root/.config`. O terminal imprimiria "descontaminação
concluída".

**E hoje nada barra isso.** `acquire_sudo` (`:209-210`) trata root como caso
normal: `[[ "${EUID:-$(id -u)}" -eq 0 ]] && return 0 # já é root`.

**O precedente da cura já existe no repositório.** `install.sh:511-518` detecta
o cenário equivalente e **recusa o passo**, com a razão escrita: *"SESSION_UID
resolveu 0 (root) — o broker autorizaria ROOT e nenhum daemon de usuária
conectaria. Rode ./install.sh da SESSÃO da usuária (sudo é pedido
internamente). Passo ABORTADO."* A E4 é esse mesmo desenho aplicado ao
desinstalador — com uma diferença: lá aborta um passo, aqui teria de abortar o
script, porque tudo do lado do usuário sai errado, não só um pedaço.

**Entrega, em duas partes.**

1. Trocar a mensagem de `:469` por *"reexecute `./uninstall.sh`
   interativamente (a senha é pedida uma vez)"*, ou por `SUDO_ASKPASS`. Nunca
   `sudo bash` do script inteiro.
2. Um guarda no topo: se o script está rodando como root **com `SUDO_USER`
   definido** (isto é, alguém fez `sudo`), recusar com exit 2 e imprimir o
   comando certo.

**Decisão que é dela:** recusar, ou re-derivar o `HOME` a partir de `SUDO_USER`
e seguir. Minha leitura é recusar — re-derivar cria um segundo caminho de
resolução de HOME num script que já tem 56 usos do primeiro, e a casa já tem uma
resolução de identidade que precisou de guarda (o `SUDO_UID` do broker).

**Aceite:** `grep -n "sudo bash" uninstall.sh` não devolve nada; e
`sudo bash uninstall.sh --yes` imprime o motivo e sai 2 sem tocar em `/etc` nem
no HOME.

**Mordida:** o teste de texto é trivial (nenhuma linha do `uninstall.sh` sugere
`sudo bash $0`) e morde só a mensagem — arrancar a troca deixa vermelho. O teste
de comportamento tem uma armadilha que precisa estar escrita na entrega: **`EUID`
é somente-leitura no bash**, então um guarda escrito como
`[[ "${EUID:-$(id -u)}" -eq 0 ]]` — que é como a `:210` está hoje — **nunca pode
ser exercitado por teste sem root**, porque o `EUID` sempre existe e o `$(id -u)`
nunca é consultado. O guarda tem de resolver o uid por um caminho que o teste
consiga controlar (um `id` no `PATH` do teste, ou uma variável de override
declarada no código). Se a entrega não fizer isso, o teste que a acompanhar
passa com a cura arrancada, e aí ela não vale nada.

**Risco:** médio-baixo, e o risco é o guarda, não a mensagem. Existe um caso
legítimo hoje suportado: a máquina em que a pessoa **é** root de verdade, sem
`sudo` — é o que a `:210` e a `:211` tratam. O guarda tem de distinguir "sou root
porque me chamaram com sudo" (`SUDO_USER` presente → recusa) de "sou root
mesmo" (segue), e ainda assim precisa de escapatória declarada. Conferido que
**nenhum empacotador chama o `uninstall.sh`**: `packaging/debian/prerm`,
`postrm`, o `.spec` do Fedora e o `.install` do Arch trazem um "belt" próprio
descrito como *"simetrico ao uninstall.sh nativo"*, sem invocá-lo. Então o
guarda não quebra remoção de pacote.

---

## E5. O `nix run` do README é impossível por construção

`packaging/nix/package.nix:79`, dentro da derivação inline do `pydualsense`
(`:71-84`):

```
        sha256 = lib.fakeSha256;
```

Com `fakeSha256`, todo `fetchPypi` falha em hash-mismatch por desenho — é o
marcador que o Nix usa justamente para te dizer o hash real na mensagem de erro.

**E o README promete o contrário, na ordem errada.** `packaging/nix/README.md`
abre em `:6-17` com **"## Uso rapido"** e
`nix run github:AndreBFarias/hefesto-dualsense4unix -- version`; `:19-31` traz
"Build local" com `nix build .#default`. A ressalva existe — e isto é decisão
documentada, não mentira: `:128-131`, em "Limitações conhecidas", diz que o
`sha256` *"esta como `lib.fakeSha256` no template — Nix vai reclamar no primeiro
build pedindo o hash real. Substituir uma vez."*

**O defeito é a ordem, e um detalhe do fluxo remoto.** A ressalva está 111 linhas
abaixo da promessa, e quem lê "Uso rapido" não chega lá. Pior: no caminho
`nix run github:...` **não existe "substituir uma vez"** — não há árvore local
para editar. A instrução da ressalva só vale para quem clonou.

**É pendência registrada e atravessou a v0.4.0.** `PROMESSA-NÃO-CUMPRIDA-01:214-216`
(citando `package.nix:74-76`, que hoje é `:79` — a linha andou) e o índice de
30/07 em `:292-295`. Nenhuma sprint a cura desde 26/07.

**Entrega, em duas metades com ordens diferentes.**

1. **Hoje, custo zero:** a limitação sobe para o topo do README, antes do "Uso
   rapido", e o bloco de "Uso rapido" leva a ressalva junto. Deixa de haver um
   trecho do documento que promete o que o outro nega.
2. **A cura de verdade:** gravar o `sha256` real do `pydualsense` 0.7.5 com
   `nix-prefetch-url`. **Isto não é entregável desta máquina:** `command -v nix`
   devolve vazio aqui. Gravar um hash que ninguém consegue conferir troca um erro
   visível (o Nix reclama e diz o hash certo) por um erro silencioso (o Nix baixa
   outra coisa e aceita). A metade 2 só entra com um `nix build .#default`
   verde ao lado, feito em máquina que tenha nix.

**Aceite:** (1) a primeira seção do `packaging/nix/README.md` depois do título é
a limitação, e nenhum comando do "Uso rapido" aparece sem a ressalva ao lado;
(2) quando a metade 2 entrar, `nix build .#default` termina sem hash-mismatch e
`./result/bin/hefesto-dualsense4unix version` imprime a versão do
`pyproject.toml`.

**Mordida:** um teste que lê o `package.nix` e, **se** achar `lib.fakeSha256`,
exige que a limitação esteja acima do primeiro bloco de comando do README.
Arrancar a cura (voltar as seções de lugar) deixa vermelho. O que faz este teste
valer mais que um lint é a direção contrária: quando alguém gravar o hash real
e esquecer de tirar o aviso, o mesmo teste tem de cobrar a **remoção** do aviso.
Sem essa segunda metade, ele vira um carimbo.

**Risco:** baixo na metade 1 (é ordem de seção num README). A metade 2 não tem
risco porque não entra aqui — e é isso que está escrito.

---

## E6. `hefesto-dsx-recover.service`: três fontes, três histórias — a decisão é dela

Esta entrega **não propõe uma correção**. Ela põe as três versões lado a lado,
medidas, e pede uma escolha. É o B2 da PROMESSA-NÃO-CUMPRIDA-01 (`:149-154`),
aberto desde 26/07 e reconfirmado no índice de 30/07 (`:277-280`).

**As fontes, cada uma reconferida hoje.**

| Fonte | O que ela diz | Onde |
|---|---|---|
| O asset | existe, 15 linhas, `ExecStart=/usr/local/sbin/dsx_recover.sh`, `Restart=always` | `assets/hefesto-dsx-recover.service:10-11` |
| O install | não conhece: `grep -n dsx install.sh` devolve **zero** | — |
| O `.deb` | empacota o **script** e **exclui a unit de propósito**, com a razão escrita | `scripts/build_deb.sh:191-194` e `:313-317` |
| O uninstall | remove: prime o sudo e faz `disable --now` + `rm` | `uninstall.sh:250` e `:357-363` |
| O doctor | **ensina a instalar à mão** | `scripts/doctor.sh:3105` |
| O storm-audit de 26/06 | classifica como *"'cura' por authorized-toggle = re-enumeração por software, realimentação positiva"* e propõe apagar do disco *"para não poder re-armar"* | `docs/process/audits/2026-06-26-storm-audit/sintese-resultado.json` |

**Duas coisas que mudam o enquadramento e que nenhum dos achados trouxe.**

1. **O doctor não é imprudente — é isolado.** `doctor.sh:3100`, o comentário
   imediatamente acima do conselho, já diz: *"rede de segurança (watcher) — NÃO
   é a solução, só mitigação"*. E o próprio bloco, em `:3095`, aponta a cura de
   raiz antes: o quirk `usbcore.quirks=...gn,gn`. O problema é que essas três
   fontes não se citam.
2. **O storm está superado como incidente.** Medido hoje: `/proc/cmdline` tem
   `usbcore.quirks=054c:0ce6:gn,054c:0df2:gn` — a "alavanca A" que o próprio
   doctor nomeia. Na máquina dela o conselho do `:3105` dispara em cima de um
   problema que já está curado por outro caminho.

**E o asset ainda aponta para um documento que não existe.**
`assets/hefesto-dsx-recover.service:2` diz
`# doc: docs/process/sprints/FEAT-DSX-RECOVER-01.md`; `find docs -iname
"*DSX-RECOVER*"` não devolve nada.

**Registro do que NÃO é defeito, para a decisão não desfazer trabalho:** a
exclusão da unit no `.deb` é **decisão escrita**
(`PACKAGING-DEB-SERVICES-EXPLICIT-01`, `build_deb.sh:313-317`), com o motivo —
units que dependem de placeholders que só o install nativo resolve deixariam
units quebradas visíveis no `list-unit-files`. Qualquer opção escolhida abaixo
tem de continuar honrando isso.

**As três opções, com o que cada uma custa.**

- **A — some dos três lugares** (asset, removedores, dica do doctor). A mais
  barata, e não perde nada medido: o storm está curado pelo quirk. Custo: numa
  máquina sem o quirk, deixa de existir rede de segurança.
- **B — o install ganha um passo opt-in** (`--dsx-recover`), fechando a simetria
  de verdade. Custo: uma flag nova, uma unit nova no portão de paridade, e
  institucionaliza como recurso uma mitigação que a auditoria classificou como
  parte do problema.
- **C — o doctor passa a condicionar o conselho:** só sugere o watcher quando o
  quirk **não** está no `/proc/cmdline`, e imprime a ressalva do storm-audit
  junto da sugestão. Mantém a rede para quem não tem o quirk e cala o conselho na
  máquina dela.

**A leitura das medições, para ela decidir e não para decidir por ela:** C é a
única que não fecha porta, e A é a única que faz o `grep dsx` contar uma história
só. As duas juntas — condicionar o conselho e tirar do asset a referência ao
documento inexistente, apontando-a para a auditoria — custam pouco e não
precisam ser desfeitas depois. **B é a única irreversível na prática**, porque
transforma em recurso publicado o que hoje é resíduo.

**Aceite:** `grep -rn dsx assets/ scripts/ install.sh uninstall.sh docs/` conta
**uma** história; e existe uma ADR registrando a escolha e o porquê — o próximo
número livre é `docs/adr/020-*` (a pasta vai até `019`).

**Mordida:** depende da escolha, e uma delas é fraca — declaro qual.
- Se **C**: teste de que a linha de conselho está dentro de um ramo que lê o
  `/proc/cmdline`. Arrancar a condição → vermelho. **Morde comportamento.**
- Se **A**: teste de que a string `hefesto-dsx-recover` não aparece em lugar
  nenhum da árvore. Arrancar → recriar o asset deixa vermelho. **Morde só
  ortografia** — ele impede o arquivo de voltar, não prova nada sobre execução, e
  isso tem de estar escrito no docstring do teste.
- Se **B**: teste de paridade, no molde do `check_packaging_parity.sh` — a unit
  opt-in aparece no install, no uninstall e em todos os formatos. Arrancar de um
  formato → vermelho.

**Risco:** o risco desta entrega é decidir errado, não codar errado. Por isso ela
é a única marcada como **decisão dela**.

---

## E7 (opcional, barata). B4 — a janela de ordem no install, medida

Esta entra como opcional porque **a medição de hoje enfraquece o achado
original**, e o documento segue a medição.

O B4 (`PROMESSA-NÃO-CUMPRIDA-01:166-172`) diz que as regras 82 e 83 são gravadas
no passo 3 e os scripts que elas invocam só chegam no 3e-bis, abrindo uma janela
em que um `ACTION=="add"` dispara `RUN+=` para caminho inexistente.

**A janela existe e foi medida na máquina dela**, no journal do reinstall de
30/07, com precisão de microssegundo:

| Instante | O quê |
|---|---|
| `13:03:41.210486` | regra **82** gravada |
| `13:03:41.214151` | regra **83** gravada |
| `13:03:41.237731` | `udevadm control --reload-rules` — **as regras ficam vivas aqui** |
| `13:03:41.470339` | `bt_nosniff_now.sh` instalado (alvo da 82) |
| `13:03:41.518462` | `hefesto-bt-bonds-snapshot.service` instalado (alvo da 83) |

**233 ms** para a 82 e **281 ms** para a 83.

E dentro dessa janela quase nada pode acontecer, por três motivos medidos:

1. Os `udevadm trigger` do passo 3 **não** disparam `add` em `hid`:
   `install_udev.sh` faz `--action=add` só para `leds` (`:149`) e `misc`
   (`:153`); o que vai para `usb`, `input` e `pci` é `--action=change`
   (`:143`, `:147`, `:156`). Só uma conexão Bluetooth real, exatamente ali,
   dispararia as regras.
2. Um `RUN+=` que falha não impede a criação do device — o udev loga e segue.
3. A 83 usa `--no-block` de propósito, com a razão escrita em
   `assets/83-hefesto-bond-snapshot.rules:22-23`: *"o udev não pode ficar
   esperando o systemd, sob pena de segurar a criação do device"*.

**O que sobra do achado, e é isso que paga a entrega:** `install.sh:1568-1569` —
se o `sudo -n true` falhar no 3e-bis, o passo só **avisa** e o install continua.
As regras ficam apontando para alvos que nunca chegaram, permanentemente, até
alguém reexecutar. É o estado da E2, alcançado por outra porta.

**Entrega.** Mover a instalação dos 7 `bt_*.sh` e das units (3e-bis,
`install.sh:1572` e `:1470-1474`) para **antes** do passo 3. O comentário de
ordem em `:1451-1452` só exige que o 3e-bis venha antes do 3f, porque o postinst
do backport reinicia o `bluetoothd` — nada o prende depois do 3.

**Aceite:** num install limpo, o `install -Dm755` do `bt_nosniff_now.sh` aparece
no journal **antes** do `udevadm control --reload-rules`; e a numeração impressa
dos passos continua legível na tela.

**Risco:** baixo em mecanismo, médio em leitura. O rótulo do passo é contrato com
os olhos dela: um "3e-bis" rodando antes do "3" seria a tela mentindo sobre a
ordem. Quem mover renumera, ou não move.

---

## Como você valida na tela

Os itens 1 a 4 são de olho, sem terminal. Os 5 e 6 exigem uma máquina de teste —
**nunca esta**, com o daemon e a janela vivos.

1. **Nada muda na sua janela.** Abra o Hefesto e passe pelas nove abas. Se
   qualquer coisa mudou de aparência, esta sprint extrapolou e reprova: ela não
   toca em `gui/`, em `src/` nem no daemon.
2. **A aba Sistema continua verde.** O cartão de saúde e os cinco botões
   respondem como antes; o log não ganhou linha nova de erro.
3. **A tipografia continua a mesma.** A E1 não pode mexer nas fontes que já
   estão instaladas na sua máquina — elas vieram por pacote da distro. Se a
   interface mudar de letra depois desta sprint, a E1 apagou o que não era dela
   e **reprova na hora**.
4. **Pegue o controle e conecte por Bluetooth.** O Pro Controller tem de
   continuar entrando sem sniff e o snapshot de bonds tem de continuar rodando —
   nada da E2 pode mudar o comportamento de quem **não** desinstalou.
5. **Numa máquina de teste, o ciclo completo:** `./install.sh --yes` e depois
   `./uninstall.sh --yes`. Ao final, `ls ~/.local/share/fonts/` não pode ter
   pasta do hefesto (E1) e `ls /etc/udev/rules.d/` não pode ter regra nossa.
6. **Na mesma máquina, o teste do dedo torto:** digite `./scripts/purge.sh
   --help`. Tem de imprimir a ajuda e **parar**. Se aparecer qualquer pergunta
   sobre descontaminar, a E3 não entrou.

E vale a regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
**a E6 não vira commit sem a decisão dela por escrito**, e as E2 e E4 não viram
commit sem ela ver, na tela, que o controle continua conectando e que a janela
continua subindo. São entregas que mexem em desinstalação — o modo de falhar
delas é silencioso, e o único jeito de flagrar é olhar.

## O que fica de fora desta sprint, por escrito

- **Rodar o ciclo install → uninstall nesta máquina.** Proibido: o daemon e a
  janela dela estão vivos. Toda a simetria deste documento foi conferida por
  leitura dos dois scripts, item a item, mais o journal do ciclo real que ela
  mesma executou em 30/07.
- **Gravar o `sha256` real do `pydualsense`.** É a metade 2 da E5 e não sai
  daqui: não há `nix` nesta máquina, e hash não conferido é pior que hash
  ausente.
- **As quatro exceções já decididas da simetria.** O quirk de `cmdline`, o
  `bluez-tools`, o Proton **extraído** e a configuração preservada por default
  continuam fora do uninstall **por decisão**, cada uma documentada no cabeçalho
  do `uninstall.sh` (`:32-42`). Esta sprint não as reabre.
- **A exclusão da unit `dsx-recover` do `.deb`.** Decisão escrita
  (`build_deb.sh:313-317`); qualquer opção da E6 tem de continuar honrando.
- **Os `rm` defensivos de artefatos que nada instala hoje.** Regras 73/74
  (`uninstall.sh:475-476`), `environment.d` 91 (`:129-131`, marcado no próprio
  arquivo como *"hoje redundante"*), o `sysctl.d` de coredump e o drop-in de
  debug. São limpeza de instalação antiga, com o motivo escrito ao lado. Mantêm.
- **As falhas antigas do `hefesto-bt-health-watchdog.service`** nos boots de
  26/07 e 27/07. Desde a reinstalação de 30/07 ele roda com status 0 a cada 2
  minutos. É achado de outra área e não vira entrega aqui.
- **A regra 84 como "órfã".** Ela não tem `RUN+=` (conferido: só `ENV{}` e
  `SYMLINK+=`, `:59-68`). Entra na E2 só pela dica incompleta de `:516`.

## O que eu não medi

- **O cenário órfão, ao vivo.** Não rodei `--keep-udev` nem apaguei alvo nenhum:
  isso quebraria a instalação dela. A forma da linha de erro do udev vem do
  journal desta máquina, mas de **outro** dono de `RUN+=` (o
  `input-remapper-control`, três ocorrências em 30/07). O erro específico das
  82/83 órfãs é dedução a partir do mecanismo, não observação.
- **A janela do B4 numa máquina fria.** Os 233 ms de E7 são o **melhor caso**:
  no reinstall de 30/07 tudo entre o passo 3 e o 3e-bis já estava satisfeito.
  Estruturalmente os passos do meio (3b `:1151`, 3c `:1170`, 3d `:1206`, 3d-bis
  `:1306`, 3e `:1336`) são escrita de arquivo e um `tee`, e os pesados — DKMS
  (3i `:1692`, 3j `:1711`, 3k `:1725`) e o apt do 3f (`:1524`) — vêm **depois**
  do 3e-bis. Então a janela deve ficar na mesma ordem de grandeza. **Não medi.**
- **Se o `doctor.sh` detecta regras 82/83 órfãs.** Medido que **não**:
  `grep -n "bt_nosniff_now\|82-nintendo\|83-hefesto-bond" scripts/doctor.sh`
  devolve zero. Ou seja, hoje nada avisa a pessoa que ela está no estado da E2.
  Se isso deve virar uma verificação do doctor é entrega de outra sprint.
- **Builds reais de empacotamento.** Nenhum `build_deb.sh`, PKGBUILD, `.spec`,
  flatpak ou AppImage foi executado. A paridade vem do portão estático
  (`check_packaging_parity.sh`, rodado hoje, exit 0) e de leitura.
- **O comportamento do `sudo` em outras distros.** O `HOME=/root` da E4 foi
  medido **nesta** máquina. Em distro com `always_set_home` desligado e `HOME` no
  `env_keep` o resultado pode ser outro — o que só reforça a entrega: uma
  sugestão que depende da configuração de `sudo` da máquina não deveria ser
  impressa como instrução.
- **Se as fontes por download realmente ficam para trás.** Não instalei o hefesto
  numa máquina sem `fonts-space-grotesk-ttf`. A conclusão da E1 vem de leitura:
  o install grava em `DEST_DIR` e nenhum caminho do uninstall ou do purge cita
  esse diretório.
