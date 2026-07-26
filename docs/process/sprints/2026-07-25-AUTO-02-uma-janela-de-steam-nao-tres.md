# AUTO-02 — uma janela de Steam, não três

- **Status:** ABERTA
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026, por medição no código do instalador e da janela

## O pedido

> "preciso de verdade que veja as features do projeto (…) à procura de facilidade
> do usuário: ao clicar em tal coisa, ele não precisar alterar 10 coisas em abas,
> **fechar a Steam, abrir, aplicar x, y e z**, tudo de forma manual mas de forma
> automática, o máximo que der."

O trecho em negrito é literalmente o domínio desta sprint. AUTO-01 pegou o que
impedia os quatro jogadores; aqui fica o que ela descreveu palavra por palavra.

### Nota de proveniência

O AUTO-01 abre dizendo que "vinte e nove pontos de fricção foram mapeados". Esse
mapeamento **não existe em lugar nenhum do repositório** — `grep -rn "29
pontos\|fricção" docs/` devolve só as duas linhas que citam o número (o próprio
AUTO-01 e o índice da leva). Sobreviveu o número, não a lista. Portanto os pontos
abaixo são **medição nova**, feita do zero sobre o código de hoje, e não a
recuperação daquela lista. Onde eles coincidirem com a lista perdida, é
coincidência de quem mede a mesma coisa duas vezes.

## O achado que dá nome à sprint

**O instalador fecha e reabre a Steam duas vezes, por dois caminhos diferentes,
em duas linguagens diferentes — e depois falha no terceiro passo, porque ele
mesmo acabou de reabrir a Steam.**

```
passo 11    install.sh:2181  → disable_steam_input.sh --apply    (fecha em bash, REABRE)
passo 11b   install.sh:2226  → steam_launch_options.py --migrate --stop-steam
                                                                  (fecha em Python, REABRE)
passo 11c   install.sh:2255  → proton_pin.py --lock               (Steam aberta ⇒ rc=3, ADIADO)
```

Cada um dos dois primeiros tem a sua própria maquinaria de fechar e reabrir:

- o passo 11 chama `scripts/disable_steam_input.sh --apply`, que fecha por conta
  própria em `disable_steam_input.sh:170` (`steam -shutdown` em :174, escalando
  para `pkill` em :185-192) e reabre em `:401` via `reopen_steam` (`:202`);
- o passo 11b chama o módulo Python, que fecha em
  `integrations/steam_launch_options.py:1031-1038` e reabre em `:1094-1095`.

O terceiro passo não tem essa maquinaria e **não pode ter**: o `argparse` do
`integrations/proton_pin.py:1142-1178` oferece `--ensure`, `--lock`, `--unlock`,
`--report`, `--conf`, `--compat-dir`, `--cache-dir`, `--config-vdf`, `--state`,
`--appids`, `--offline` e `--dry-run`. **Não existe `--stop-steam`.** A recusa em
`proton_pin.py:1091-1096` (rc=3, vinda do `_steam_gate` em `:697-703`) é
estrutural, não azar: com a Steam de pé, aquele passo nunca teve como terminar.

E a saída oferecida é a queixa dela em forma de mensagem — `install.sh:2278-2279`:

```
aviso: Steam (ou um jogo) aberta — trava ADIADA; feche a Steam e rode:
       python3 …/proton_pin.py --lock
aviso:   (ou use o botão 'Travar Proton validado' na aba Sistema da GUI)
```

## Onde o AUTO-01 errou, e por que isso importa

O AUTO-01 explica a recusa assim: *"a recusa é praticamente garantida: o passo
imediatamente anterior baixa cerca de 450 MB de Proton, dando minutos para a
Steam voltar sozinha."* **Medi, e a frase está errada em três pontos.**

1. **O download não está no passo anterior.** O `--ensure` que baixa é
   `install.sh:2265`, **dentro do próprio passo 11c**, sete linhas acima do
   `--lock` em `:2274`. O passo imediatamente anterior (11b) é a migração, que
   não baixa nada.
2. **Na maioria das vezes não há download nenhum.** `ensure_pinned_proton`
   (`proton_pin.py:295`) é offline-first: com o diretório já extraído e sem o
   nosso manifesto, ela devolve `already` em `:321-324` sem tocar na rede.
   Medido nesta máquina, agora, sem rodar o instalador:
   `~/.steam/steam/compatibilitytools.d/GE-Proton10-34/` existe e **não** contém
   o `.hefesto-proton-pin.json` (`MANIFEST_BASENAME`, `proton_pin.py:59`) — ou
   seja, o `--ensure` daqui cai no ramo `already` e responde instantaneamente. O
   tarball ainda está no cache (`~/.cache/hefesto-dualsense4unix/proton/`,
   516.611.656 bytes, de 18/07), então mesmo o pior caso local seria extração de
   cache (`:329-333`), nunca download.
3. **Logo, o intervalo entre o reabrir e a checagem não é de minutos — é do
   tamanho de uma resposta imediata.** O que sobra é uma **corrida**, e ela é
   pior que a recusa previsível que o AUTO-01 descreveu.

O `reopen_steam` do passo 11b (`steam_launch_options.py:643-653`) é
dispara-e-esquece: um `Popen` com `start_new_session=True`, sem esperar. O gate
do passo 11c pergunta por `pgrep -af steamrt64/steam` / `pgrep -x steamwebhelper`
(`steam_launch_options.py:571-585`, espelhado em `disable_steam_input.sh:151`).
Se a Steam recém-lançada já apareceu com esse nome, o gate recusa; se ainda não
apareceu, o gate deixa passar.

**Os dois desfechos são ruins, e nenhum dos dois foi medido em execução** — não
rodei o instalador:

- gate vê a Steam ⇒ `rc=3`, trava adiada, e a usuária recebe um comando de
  terminal para copiar (o cenário que o AUTO-01 descreveu, pelo motivo errado);
- gate não vê a Steam ⇒ o `--lock` edita o `config.vdf` **enquanto a Steam está
  subindo**, e a Steam regrava esse arquivo ao sair. É exatamente a perda que o
  gate existe para impedir, dita pelo próprio código em `proton_pin.py:1093-1094`
  ("editar o config.vdf com ela viva perderia a edição") — só que agora silenciosa,
  porque o passo teria reportado sucesso.

Um instalador cujo resultado depende da velocidade com que a Steam sobe não é um
instalador — é um sorteio.

## A cura já existe na casa, e o instalador é o único que não a usa

`integrations/steam_launch_options.py:663` — `with_steam_closed()` — é
literalmente esta sprint escrita como função: recusa se houver **jogo** aberto,
fecha **uma** vez, roda tudo dentro da janela, reabre **uma** vez, e a reabertura
mora num `finally` para que uma exceção não deixe a usuária sem Steam. O
contrato de retorno (`ok` / `jogo_aberto` / `nao_fechou`, constantes em `:658-660`)
existe justamente para que quem chama nunca anuncie "Pronto" sobre uma recusa.

A janela já a usa em três botões:

- `app/actions/daemon_actions.py:808` — "Aplicar aos jogos da Steam";
- `app/actions/daemon_actions.py:908` — "Deixar tudo pronto";
- `app/actions/emulation_actions.py:892` — desligar o Steam Input pela aba
  Emulação.

O instalador não a usa em passo nenhum. A própria docstring de `with_steam_closed`
(`:668-675`) registra que a maquinaria "era exercitada só pelo `install.sh
--migrate --stop-steam`" e que a GUI foi quem aprendeu a usá-la direito — o
instalador ficou para trás na mesma noite em que a cura nasceu.

## Os pontos de fricção medidos

### AUTO-02.1 — o terceiro passo não sabe fazer o que os dois primeiros fazem

`proton_pin.py:1142-1178` não tem `--stop-steam`; `install.sh:2274` chama
`--lock` sem ter como preparar o terreno. Dois passos sabem fechar a Steam, o
terceiro depende de sorte.

### AUTO-02.2 — três donos da Steam num único instalador

Bash fecha e reabre (`disable_steam_input.sh:170`, `:202`, acionados em `:392`,
`:401`, `:428`, `:437`); Python fecha e reabre
(`steam_launch_options.py:1031-1038`, `:1094-1095`); e o terceiro passo só
observa. Enquanto cada passo decidir sozinho sobre a Steam, a ordem entre eles
vira acaso — o mesmo defeito de "dois donos" que ABAS-01 e CONTAGEM-01 acharam
no estado da janela, aqui aplicado a um processo.

### AUTO-02.3 — o segundo fechamento acontece mesmo quando não há nada a migrar

O script em bash tem um pré-voo: `disable_steam_input.sh:415-424` percorre os
`.vdf` antes de qualquer coisa e, se ninguém precisa de correção, sai com
`nada-a-fazer` **sem fechar a Steam**. O módulo Python **não tem** o equivalente:
`steam_launch_options.py:1031-1038` fecha antes de saber se há o que migrar, o
laço em `:1051-1088` pode não mudar linha nenhuma, e `:1094-1095` reabre de todo
jeito.

Numa reinstalação — o caso comum nesta casa — isso significa fechar e reabrir a
Steam **para zero edições**. E é justamente essa reabertura gratuita que coloca a
Steam na frente do passo 11c.

### AUTO-02.4 — a saída oferecida pelo instalador bate na mesma parede

`install.sh:2279` manda usar o botão "Travar Proton validado". Esse botão
(`daemon_actions.py:1043`) **recusa com a Steam aberta**, em
`daemon_actions.py:1137-1145`, e o diálogo dele ainda diz
`"A Steam precisa estar FECHADA — se estiver aberta, eu aviso e não mexo em
nada"` (`:1079-1080`).

O detalhe que faz disso um defeito, e não uma escolha: **os dois botões vizinhos,
no mesmo arquivo, já aprenderam a fechar a Steam** (`:808` e `:908`). O
comentário em `:664-667` chega a explicar que aquela mesma frase "virou mentira
no momento em que o botão passou a saber fechá-la" — e ela continua viva no botão
do Proton. Três superfícies repetem a instrução manual para a usuária:
`install.sh:2278`, `daemon_actions.py:1079-1080` e `scripts/doctor.sh:1859`.

Resultado prático: o instalador adia a trava e aponta para um botão que adia a
trava.

### AUTO-02.5 — "Deixar tudo pronto" não inclui exatamente o que ficou pendente

`_steam_ready_worker` (`daemon_actions.py:868-927`) encadeia **duas** coisas
dentro da janela do `with_steam_closed`: `disable_steam_input.sh --apply-quiet` e
`apply_wrapper_to_all_games()` (`:890-906`). A trava do Proton não está lá.

O botão chamado "Deixar tudo pronto" é o único lugar da janela onde a usuária
declara "resolva por mim" — e é justamente o passo que o instalador não
conseguiu terminar que ele não cobre.

### AUTO-02.6 — AUTO-01.4 continua aberto: o wrapper não chega aos jogos sem clique

`apply_wrapper_to_all_games` existe em `steam_launch_options.py:466` e sabe
inserir a linha até em jogo que nunca teve `LaunchOptions`
(`apply_wrapper_vdf_text`, `:354`, ramo de inserção em `:401-412`). Mas o
`argparse` do módulo (`:973-986`) só expõe `--status`, `--migrate` e `--strip`:
**não há modo de linha de comando para ela**, e `install.sh:2232` chama
`--migrate`, que por construção "só toca linhas já NOSSAS" (`:357-358`).

O wrapper em si é instalado bem antes, no passo 4b-2 (`install.sh:1855-1858`) —
ele existe em disco desde o começo da instalação e não é aplicado a jogo nenhum.
Um jogo que nunca teve opção de lançamento venenosa **nunca recebe o wrapper**
até alguém abrir a janela e clicar em "Aplicar aos jogos da Steam"
(`daemon_actions.py:717`, único chamador).

Conferido no commit do AUTO-01 (`git show 8fe735d --stat`): ele mexeu no
`install.sh` (+21 linhas), mas os dois blocos alterados ficam em torno das linhas
570 e 626 — helpers de DKMS. O passo 11b não foi tocado. AUTO-01.4 foi
diagnosticado e não entregue.

*(De passagem: as citações do AUTO-01 ao `install.sh` — 2146, 2191, 2220 — estão
35 linhas defasadas hoje, porque `8fe735d` e `8b379ae` acrescentaram 21 e 14
linhas acima daquele bloco depois que o documento foi escrito. Números de linha
em documento envelhecem; é mais um voto a favor de citar sempre o identificador
do commit junto.)*

### AUTO-02.7 — o botão do Proton pode travar jogos numa versão que não está instalada

`lock_games_to_pinned_proton` (`proton_pin.py:706-756`) escreve o
`CompatToolMapping` com o `tool_name` lido do `proton-pin.conf` **sem nunca
verificar se aquela versão foi extraída**. A verificação existe no mesmo módulo —
`pinned_proton_installed` (`:238-241`) — e é usada só pelo `--ensure`.

O instalador se protege: quando o `--ensure` volta com rc=2 ("sem rede e sem
cache"), `install.sh:2268-2269` **não** chama o `--lock`. O botão da GUI não tem
esse cuidado: `_proton_lock_worker` (`daemon_actions.py:1112-1146`) chama
`lock_proton_for_all_games()` (`proton_pin.py:799`) sem rodar o `--ensure` antes.
Numa instalação feita com `--no-proton-pin`, ou numa em que o download falhou, o
clique aponta todos os jogos para uma versão de Proton ausente.

**Não medi o que a Steam faz** com um `CompatToolMapping` apontando para um
`compatibilitytools.d` inexistente — não rodei esse cenário. O que está medido é
que o código não checa.

### AUTO-02.8 — o instalador não diz, no fim, o que ficou pendente

O bloco final (`install.sh:2289-2296`) imprime "Hefesto - Dualsense4Unix
instalado", como abrir e como desinstalar. Nenhum resumo do que foi adiado. Os
`warn` dos passos 11, 11b e 11c rolaram na tela minutos antes, no meio de dezenas
de outras linhas.

Quem termina uma instalação em que a trava do Proton foi adiada **não fica
sabendo**, a menos que rode o `doctor.sh` (que avisa, em `:1849-1862`).

### AUTO-02.9 — o contador de passos diz 11/11 e ainda vêm dois

`install.sh:2181` imprime `[11/11]`; depois vêm `[11b]` (`:2226`) e `[11c]`
(`:2255`). É pequeno, mas é da mesma família de CONTAGEM-01: a tela afirma um
número que ela mesma desmente três linhas abaixo.

### AUTO-02.10 — "Este jogo não funciona" marca a intenção, mas não liga a chave

O botão (`daemon_actions.py:970`) escreve o appid na allowlist, e a allowlist tem
efeito **preservativo**: o `awk` de `disable_steam_input.sh:269-271` só deixa de
zerar um `UseSteamControllerConfig` que **já esteja** em `1|2`. Como o instalador
zerou tudo no passo 11, marcar o jogo depois não devolve o Steam Input a ele —
só impede que o guard o desfaça de novo no futuro.

O código é honesto sobre isso: o toast em `daemon_actions.py:313-317` manda ela
ir na Steam, botão direito no jogo, Propriedades, Controle, "Ativar". Honesto e
correto — e é, palavra por palavra, "aplicar x, y e z, tudo de forma manual". O
mesmo `awk` que escreve `0` saberia escrever `2` para um appid da allowlist; o
que falta é o modo, não a capacidade.

### AUTO-02.11 — o uninstall acertou uma armadilha de reabertura e caiu na outra

`uninstall.sh:1271-1276` traz um comentário exemplar: o `--unlock` roda **antes**
do `--strip` de propósito, "o strip (`--stop-steam`) REABRE a Steam ao final, e o
unlock exige Steam fechada". Alguém já viu este defeito e o contornou pela ordem.

Só que o passo anterior, `uninstall.sh:1264`, chama `disable_steam_input.sh
--apply` — que também reabre a Steam (`:401`) — e ele roda **antes** do `--unlock`
de `:1281`. A mesma armadilha, no mesmo arquivo, um passo mais cedo. **Não medi
em execução**; o que está medido é a ordem das chamadas e o fato de o `--apply`
reabrir.

Vale a nuance que salva o caso comum: o `--apply` tem o pré-voo de
`disable_steam_input.sh:415-424` e não fecha nada quando não há o que corrigir.
A armadilha só arma quando havia mesmo algo a desligar — que é exatamente a
desinstalação de quem estava usando o produto.

### AUTO-02.12 — fora da janela, o único caminho é digitar o caminho do arquivo

Não há subcomando de Steam ou de Proton na linha de comando do produto:
`grep -rn "proton\|steam" src/hefesto_dualsense4unix/cli/app.py` não devolve nada.
As mensagens de erro do instalador, do uninstall e do doctor mandam rodar
`python3 <caminho absoluto do módulo dentro de src/> --lock`. Quem instalou por
pacote e não tem a árvore do repositório à mão não tem esse caminho.

## Entregas

1. **Uma janela de Steam por instalação.** Os passos 11, 11b e 11c passam a rodar
   dentro de **um** `with_steam_closed` — fecha uma vez, faz as três coisas,
   reabre uma vez. A função já existe (`steam_launch_options.py:663`), já é usada
   pela GUI em três lugares e já tem o contrato de recusa. É ligação, não
   implementação.

2. **Nada de fechar a Steam para não fazer nada.** O caminho Python ganha o
   pré-voo que o bash já tem (`disable_steam_input.sh:415-424`): decidir se há o
   que migrar **antes** de mexer no processo da Steam. Com a entrega 1 isso vira
   a pergunta única da janela: "algum dos três passos tem trabalho?".

3. **O `--lock` deixa de depender de sorte.** Duas metades: dentro da janela
   única ele não vê mais uma Steam subindo; e o gate do `_steam_gate`
   (`proton_pin.py:697`) continua onde está, porque ele está **certo** — a lição
   de RUMBLE é que se cura o que fura o gate, não se remove o gate.

4. **O botão "Travar Proton validado" aprende o que os vizinhos já sabem.**
   `daemon_actions.py:1137-1145` passa a usar `with_steam_closed`, com o mesmo
   diálogo de consentimento dos outros dois, e o texto do diálogo
   (`:1079-1080`) para de prometer a parede. Jogo aberto continua sendo recusa.

5. **"Deixar tudo pronto" fica pronto de verdade.** A trava do Proton entra na
   corrente de `_steam_ready_worker` (`daemon_actions.py:890-906`), dentro da
   mesma janela — precedida de um `ensure` ou de uma recusa honesta se a versão
   pinada não estiver em disco.

6. **Modo de linha de comando para `apply_wrapper_to_all_games`** (fecha
   AUTO-01.4). Um `--apply-wrapper` no `argparse` de
   `steam_launch_options.py:973-986`, e o `install.sh` passa a chamá-lo em vez de
   só `--migrate`. Hoje o wrapper é instalado no passo 4b-2 e fica esperando um
   clique que pode nunca vir.

7. **O lock confere se a versão pinada existe.** `lock_games_to_pinned_proton`
   consulta `pinned_proton_installed` (`proton_pin.py:238`) antes de escrever, e
   recusa com motivo próprio — em vez de apontar os jogos para uma pasta ausente.

8. **O instalador termina com um resumo do que ficou pendente**, e cada pendência
   vem com o clique que a resolve (não com o comando de terminal). Se não houver
   pendência, ele diz isso — que é o critério de aceite do AUTO-01.

9. **`uninstall.sh` roda o `--unlock` antes do `disable_steam_input --apply`**, ou
   melhor: dentro da mesma janela única da entrega 1, que torna a ordem
   irrelevante.

10. **"Este jogo não funciona" liga a chave.** Um modo do
    `disable_steam_input.sh` que **reativa** o `UseSteamControllerConfig` do
    appid recém-marcado, em vez de mandá-la ao menu da Steam. O `awk` de
    `:269-271` já entende a allowlist; falta o sentido inverso.

11. **Cosméticos honestos:** o contador de passos deixa de dizer `11/11` com dois
    passos pela frente (`install.sh:2181`).

## Como validar

Cada passo abaixo é observável sem instrumentação especial.

1. **Contar os fechamentos.** Com a Steam aberta e com algo real a corrigir
   (`bash scripts/disable_steam_input.sh --status` acusando `precisa-corrigir`),
   rodar o instalador e contar quantas vezes a janela da Steam some e volta.
   Hoje: até duas. Critério: **uma**.
2. **A trava não pode ser adiada.** No fim da instalação, a saída não pode conter
   `trava ADIADA`, e `python3 …/proton_pin.py --report` tem de voltar com
   `"global_is_pinned": true` e `"games_off_pin": []`.
3. **Reinstalação sem trabalho não fecha nada.** Rodar o instalador duas vezes
   seguidas. Na segunda, com nada a migrar e nada a corrigir, a Steam **não pode
   ser fechada**.
4. **Jogo aberto continua sendo veto.** Com um jogo rodando, o instalador não
   pode fechar Steam nem jogo; tem de recusar os três passos dizendo por quê.
   Este é o gate que não se toca.
5. **O wrapper chega a jogo virgem.** Escolher um jogo que nunca teve opção de
   lançamento do Hefesto, rodar o instalador, e conferir no `localconfig.vdf` que
   a linha `LaunchOptions` do wrapper apareceu — sem abrir a janela.
6. **O botão do Proton fecha a Steam.** Com a Steam aberta, clicar em "Travar
   Proton validado": tem de aparecer o pedido de permissão, não a parede.
7. **"Deixar tudo pronto" deixa.** Depois de clicar, `scripts/doctor.sh` não pode
   ter nenhum aviso de Steam ou de Proton pendente.
8. **O resumo final bate com a realidade.** Forçar uma pendência (rodar com a
   rede desligada e sem cache) e conferir que o instalador **lista** o que ficou
   para trás em vez de imprimir só "instalado".

**Critério que resume:** uma instalação toca na Steam **uma vez só** — e quando
ela terminar, não sobra nenhum comando de terminal para a usuária copiar.

## O que esta sprint deliberadamente não faz

- **Não remove nenhum gate.** Os três ("jogo aberto", "Steam viva", "a Steam não
  fechou") estão corretos e são a razão de o produto não comer o progresso de um
  jogo. A cura é dar a eles um terreno preparado, nunca desarmá-los.
- **Não mede comportamento em execução.** Nada aqui foi obtido rodando o
  instalador, o uninstall ou qualquer caminho que escreva em arquivo da Steam. As
  únicas execuções foram leituras: `proton_pin.py --report` (declarado read-only
  no próprio `argparse`), `ls` no `compatibilitytools.d` e no cache, e `git show`.
  Toda afirmação sobre o que acontece com a Steam **de pé** está marcada como não
  medida.
- **Não decide sobre o tamanho do download.** Os "cerca de 450 MB" do AUTO-01 não
  aparecem em lugar nenhum do repositório; o que existe medido é o tarball em
  cache nesta máquina, com 516.611.656 bytes. A sprint não depende desse número —
  ela depende de o download, na prática, **não acontecer**.
