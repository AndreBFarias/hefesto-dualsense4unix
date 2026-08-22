# SENTINELA-WRAPPER-01 — a Steam guarda uma linha por jogo, e comeu a nossa

**Estado:** CONCLUÍDA — as três camadas estão em
`integrations/sentinela_do_wrapper.py` (`censo_do_wrapper:302`,
`frase_do_aviso:393`, `reparar_ou_adiar:448`), chegam ao `scripts/doctor.sh:1599`
e ao `install.sh:3325` sem flag, mordem em
`tests/unit/test_sentinela_do_wrapper_01_a_steam_comeu_o_hefesto_launch.py`, e a
ligação com a janela fechou em `app/actions/carona_do_wrapper.py`
(verificado em 21/08/2026)

**16/08/2026.** Defeito pego ao vivo, no processo do jogo rodando.

## O que ela viu

Jogou Pragmata no **cabo** e funcionou. Passou para o **Bluetooth**:

> *"no inicio travou alguns inputs mas logo em sequencia ele parou de ser
> reconhecido no jogo, mas o perfil de pragmata segue ativo no controle com
> tudo funcionando só não sendo reconhecido. não alterei nada nada na steam."*

E ela não alterou mesmo. O defeito estava plantado havia dias.

## A causa raiz

As Opções de Inicialização do Pragmata (appid 3357650) no `localconfig.vdf`
eram:

```
VKD3D_CONFIG=no_upload_hvv %command%
```

e as dos outros **sessenta** jogos dela eram a chamada do `hefesto-launch`.

**A Steam guarda UMA linha por jogo.** Quando o `VKD3D_CONFIG` foi posto —
quase certo que para curar o crash de VRAM de 14/08 — ele **substituiu** o
wrapper. Ninguém percebeu, porque a Steam não avisa e o campo aceita qualquer
texto.

Censo daquela máquina naquele dia: **60 jogos com o wrapper, 1 sem** — e o
único sem era o Pragmata.

## A cadeia do estrago, medida no `/proc` do jogo vivo

1. o wrapper não rodou ⇒ `PROTON_DISABLE_HIDRAW` no ambiente do jogo: **zero**
   (só o Hefesto escreve essa variável);
2. o `SDL_GAMECONTROLLER_IGNORE_DEVICES` que chegou ao jogo **não era o
   nosso** — era a lista gigante da própria Steam;
3. dentro dela está `0x054c/0x0df2`, o PID do **nosso vpad**, ao lado do
   `0x054c/0x0ce6`, o do físico: o jogo foi instruído a ignorar **os dois**;
4. `event21` (o vpad) — ninguém abriu. `event25` (o físico) — a Steam abriu.
   O jogo ficou sem nenhum.

O daemon estava **saudável o tempo todo**: vpad P1 com os quatro nós, grab
retido (`gamepad_controller_grab grab=True ok=True state=held`), `launch_env`
materializado em `steam_app_3357650.env` às 03:29 com o conteúdo certo. Ele
fez a parte dele. O arquivo nunca foi lido, porque quem o lê é o wrapper.

No cabo funcionava porque ali o jogo alcança o aparelho por outro caminho.

**É o modo de falha mais confuso que existe**: o controle continua vivo, a luz
acesa, o perfil aplicado — e só o JOGO não enxerga. O único jeito de descobrir
era o que ela fez: perder uma noite.

## O pedido dela

> *"temos que criar um fallback pra evitar isso"* e
> *"solução universal dentro da gui pode fazer isso tambem?"* <!-- noqa-acento -->

## A cura, em três camadas independentes

`src/hefesto_dualsense4unix/integrations/sentinela_do_wrapper.py`.

### 1. Detectar — `censo_do_wrapper()`

Quais jogos têm a chamada do wrapper e quais não têm, a qualquer momento.
**Read-only**, portanto seguro **com a Steam aberta** — que é a condição em
que ela está quando o problema aparece. Só a *escrita* no `localconfig.vdf`
exige a Steam fechada.

Duas guardas contra alarme falso, porque aqui o instrumento mente mais fácil
que o produto:

- vdf que parseia para **zero apps** é tratado como erro, não como "a
  biblioteca inteira perdeu o wrapper" — é o retrato de uma leitura pega no
  meio de a Steam regravar o arquivo;
- vdf de Flatpak/Snap é pulado inteiro (lá o wrapper do host é invisível,
  então "não tem wrapper" é o estado **certo**).

### 2. Avisar — `frase_do_aviso()`

A frase pronta, **com o nome do jogo**, para a janela e para o `doctor.sh`
(`check_sentinela_wrapper`). O contador que já existia dizia *quantos* jogos
tinham o wrapper e nunca dizia **qual** não tinha: em 15/08 ele mostrava "60
jogos com o wrapper" e passava em verde enquanto o jogo dela ficava sem
controle.

### 3. Reparar — `reparar_ou_adiar()`

Repõe o wrapper **preservando o que já estava na linha**, ou adia dizendo por
quê. Ordem dos portões, não negociável: **jogo aberto antes de tudo** (fechar a
Steam ali mataria o jogo), depois Steam aberta (a edição seria engolida na
saída dela), e só então a escrita — com backup `.bak.hefesto-launch-<ts>` e
`tmp` + `replace`.

## A composição que preserva a linha dela — medida, não suposta

O reparo do Pragmata tem de manter o wrapper **e** o `VKD3D_CONFIG`: soltar um
dos dois troca "o jogo não vê o controle" por "o jogo fecha sozinho".

A linha que o `migrate_value` **já emitia** faz exatamente isso:

```
sh -c 'W="$HOME/…/hefesto-launch"; [ -x "$W" ] && exec "$W" "$@"; exec env "$@"' \
    hefesto-launch VKD3D_CONFIG=no_upload_hvv %command%
```

Funciona porque o wrapper termina em `exec env "$@"`: o `VKD3D_CONFIG` chega
como argumento do `env(1)`, que o trata como assignment.

**Executado de verdade em 16/08**, com wrapper de mentira e jogo de mentira:
o jogo recebeu `VKD3D_CONFIG`, `PROTON_DISABLE_HIDRAW` e
`SDL_GAMECONTROLLER_IGNORE_DEVICES`, com os argumentos originais intactos. Com
o wrapper **ausente**, recebeu o `VKD3D_CONFIG` e abriu do mesmo jeito.

**Não é preciso — nem se deve — intercalar um `env` extra antes do
`VKD3D_CONFIG`.** A composição de duas camadas já é a certa, e é a mesma dos
outros 60 jogos. Uma segunda forma de escrever a linha quebraria a
idempotência (`WRAPPER_PREFIX in value` deixaria de casar) e, com ela, 60
jogos de uma vez.

## As quatro perguntas do desenho

**"E se ela tirar o wrapper de propósito?"** — Intenção **nunca é inferida**.
A única voz que conta é o `~/.config/hefesto-dualsense4unix/jogos_sem_wrapper.txt`
(`marcar_jogo_sem_wrapper`, um clique). Esses jogos somem do aviso, do reparo
**e do passo sem flag do install** — sem isso, "não quero" duraria até o
próximo `./install.sh`, e escolha que o produto desfaz sozinho não é escolha.
Uma linha que sumiu sozinha é sempre tratada como estrago: a Steam sobrescreve
sem avisar, e é o caso comum.

**"E se a Steam puser LaunchOptions sozinha num jogo novo?"** — O registro
`~/.local/state/hefesto-dualsense4unix/wrapper-visto.json` guarda os appids já
vistos **com** o wrapper. Nunca esteve lá ⇒ `novo`; estava e sumiu ⇒
`regressao`. Os dois são reparados (é o que o install já faz com todo mundo),
mas só a regressão ganha a frase *"parou de funcionar"* — que é a informação
que ela não tinha. Registro corrompido ou ausente = tudo vira `novo`: o
produto ainda repara, só não afirma sem base.

**"O reparo é idempotente?"** — Sim, e não por promessa: delega ao
`apply_wrapper_to_all_games`, cujo gate `WRAPPER_PREFIX in value` pula quem já
tem. Travado por teste (`test_o_reparo_e_idempotente`).

**"Há backup antes de escrever?"** — Sim: `.bak.hefesto-launch-<ts>` ao lado
de cada vdf tocado, antes de escrever. O `localconfig.vdf` guarda a biblioteca
inteira dela.

## Por que não há marcador de pendência

O censo é uma leitura de arquivo. Adiado hoje com a Steam aberta, o reparo
simplesmente **acontece** na próxima passada com ela fechada — install, doctor
ou janela. Estado guardado sobre um vdf que muda sozinho envelheceria errado, e
mentir sobre isso é o que esta sentinela existe para não fazer.

## O que entrou no install (sem flag)

- **11b-ter** — `sentinela_do_wrapper.py --relatorio`: anota quem está com o
  wrapper. Sem essa memória, a regressão de amanhã apareceria como "jogo
  novo". Read-only sobre o vdf, best-effort absoluto.
- **11b-bis** — o `--apply` que já existia passa a **respeitar** o
  `jogos_sem_wrapper.txt`.
- **uninstall** — o registro sai junto (senão a próxima instalação chamaria de
  regressão a remoção que o próprio uninstall fez). O `jogos_sem_wrapper.txt`
  **não** sai: é escolha dela sobre a biblioteca dela.

## A mordida

`tests/unit/test_sentinela_do_wrapper_01_a_steam_comeu_o_hefesto_launch.py`
(18 testes, fixtures em `tmp_path` — nenhum `localconfig.vdf` real é tocado).
Quatro curas arrancadas, quatro reprovações medidas:

| arrancado | reprova | mensagem |
|---|---|---|
| a memória de "já teve o wrapper" | 3 | `assert 'perdeu' in '1 jogo nunca recebeu…'` |
| o respeito à recusa dela (`excluir`) | 1 | o Pragmata marcado como "não quero" recebe o wrapper mesmo assim |
| a leitura do app **sem** a linha | 2 | `assert [] == ['444']` — a linha apagada some do radar |
| a preservação da linha dela | 3 | `assert 'VKD3D_CONFIG=no_upload_hvv' in 'sh -c …hefesto-launch %command%'` |

## O que ficou aberto — e é da janela  *(FECHADO em 16/08, ver nota)*

A camada 2 chega hoje ao `doctor.sh`. **A janela ainda não a consome**: o
`app/` estava com outro dono nesta leva. Quem for ligar chama
`censo_do_wrapper()` e mostra `frase_do_aviso()`; o botão "não quero neste
jogo" chama `marcar_jogo_sem_wrapper()`; o botão de reparo chama
`reparar_ou_adiar()`, que já devolve `adiado_steam_aberta` /
`adiado_jogo_aberto` com a frase certa para o toast.

> **Nota datada — 16/08/2026, e o desenho é dela.** Isto está fechado, e sem o
> botão que o parágrafo acima previa. Ela recusou o botão: *"nem precisa ter um
> botão na gui, mas ele se auto corrigir ao clicarmos em aplicar ou salvar o
> perfil seja dentro ou fora da guia de perfis."* A ligação virou
> `CARONA-DO-WRAPPER-01` — `src/hefesto_dualsense4unix/app/actions/`
> `carona_do_wrapper.py` —, que pendura `reparar_ou_adiar()` em **cinco**
> gestos que já existiam: salvar e ativar na aba Perfis, o funil de gravação do
> rodapé (Salvar/Importar/Restaurar Padrão), o botão verde "Aplicar", e a troca
> de perfil pela bandeja e pela janela compacta. O que sobrou de fora, com
> motivo, está no censo de gestos na docstring daquele módulo.



## Achado colateral, e ele importa

O Pragmata **já estava reparado** quando esta sessão começou (03:33 de 16/08,
backup `.antes-do-wrapper` ao lado). O reparo repôs o wrapper e **jogou fora o
`VKD3D_CONFIG=no_upload_hvv`** — a cura do crash de 14/08 sumiu da linha. Está
assim na árvore dela agora.

E ele foi escrito **com a Steam aberta**: ela regrava o `localconfig.vdf` ao
sair, então esse reparo tende a ser desfeito no próximo fechamento da Steam.
As duas coisas são exatamente o que este sprint existe para não deixar
acontecer de novo — e nenhuma das duas foi tocada aqui, porque a Steam está
aberta e ela está jogando.
