# AUTO-01 — um clique em vez de dez

- **Status (09/08/2026):** **PARCIALMENTE PAGA — o grosso ENTREGUE EM CÓDIGO,
  AGUARDANDO A PALAVRA DELA.** Seis dos sete itens estão de pé (`.1`, `.3`,
  `.4`, `.5`, `.6` e metade do `.7`), o `.2` foi **superado por decisão dela**, e
  **quatro restos continuam ABERTOS** (listados no fim). Primeira entrega em
  `8fe735d` (25/07/2026), última em `1c75a1a` (08/08/2026). Conferência item a
  item na [nota datada de 09/08/2026](#nota-datada-09082026--seis-de-sete-e-os-quatro-restos), no fim
- **O que falta ela validar, em uma linha:** numa instalação limpa, plugar
  quatro controles, abrir um jogo, e ver se saem quatro jogadores **sem** abrir
  terminal, editar arquivo ou reiniciar nada — que é o critério de aceite
  escrito no fim deste documento, e ninguém nunca o mediu
- **Status anterior:** ABERTA (assim desde 25/07/2026). O rótulo **não se
  apaga**: sprint marcada como aberta é lida como dependência viva. Esta ficou
  **quinze dias** assim, e o próprio documento foi editado em 06/08 — **doze
  dias depois** do commit que pagou o primeiro item — sem que ninguém tocasse no
  cabeçalho
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026

## O pedido

> "preciso de verdade que veja as features do projeto (…) à procura de facilidade
> do usuário: ao clicar em tal coisa, ele não precisar alterar 10 coisas em abas,
> fechar a Steam, abrir, aplicar x, y e z, tudo de forma manual mas de forma
> automática, o máximo que der."

Vinte e nove pontos de fricção foram mapeados. Esta sprint pega os que **impedem
os quatro jogadores**; os demais estão em AUTO-02 (Steam), AUTO-03 (fluxo de
jogo) e AUTO-04 (o que só existe no terminal).

## O achado que resume a queixa

**O instalador fecha e reabre a Steam duas vezes, e depois falha no terceiro
passo — porque ele mesmo acabou de reabrir a Steam.**

```
passo 11   install.sh:2265  → fecha, edita Steam Input, REABRE
passo 11b  install.sh:2310  → fecha, migra opções de lançamento, REABRE
passo 11c  install.sh:2339  → "Steam aberta" → recusa → ADIADO
```

O terceiro passo (`proton_pin --lock`) não tem a opção de fechar a Steam que os
outros dois têm. E a recusa é praticamente garantida: o passo imediatamente
anterior baixa cerca de 450 MB de Proton, dando minutos para a Steam voltar
sozinha. A mensagem final manda a usuária **rodar um comando no terminal**.

Isso é literalmente o que ela descreveu: fechar a Steam, abrir, aplicar x, y e z,
tudo manual.

## O que impede os quatro jogadores hoje

### AUTO-01.1 — a emulação de gamepad nasce desligada, e o co-op depende dela

`daemon/lifecycle.py:132` define a emulação como desligada por padrão, e
`daemon/subsystems/coop.py:186` só ativa o co-op quando ela está de pé. O
`coop_enabled=True` da inicialização é decorativo enquanto isso for falso.

**Numa instalação nova, quatro DualSense plugados alimentam um cursor só.**

Conserto: ligar a emulação quando houver dois ou mais controles físicos. Um
segundo controle na mesa é a declaração de intenção mais clara possível.

### AUTO-01.2 — co-op não existe na janela

`grep -ci coop gui/main.glade` → **zero**. A funcionalidade central do projeto —
quatro jogadores — só existe por linha de comando.

O próprio código admite: `utils/session.py:446` explica que uma migração precisou
existir porque, sem ela, o co-op ficaria desligado *"sem nenhum caminho de volta
na interface"*.

Conserto: um botão **"Preparar co-op (N jogadores)"** na aba Início encadeando
modo de jogo, ativação do co-op e renumeração. **Todo o IPC necessário já
existe** — é ligação, não implementação.

> **NOTA DATADA (06/08/2026) — o botão SAIU, e a entrega não foi desfeita: foi ao
> limite.** Decisão dela, tomada mais de uma vez: *"todos e tudo no Hefesto tem
> que tá com o permitir co-op ligado (…) se eu conecto 4 controles no PC eu
> espero, com 4 pessoas jogando, que cada um controle o próprio personagem"*.
> Preparar o co-op deixou de ser um gesto porque **o co-op deixou de ser uma
> opção**: o piso do daemon nasce ligado, `coop.set {enabled:false}` recusa em
> voz alta e o perfil parou de governar o campo.
>
> O que este item tinha de insubstituível — o **ciclo FORÇADO** do co-op, que o
> botão alcançava de carona no `coop.set` — mudou de dono **antes** da remoção:
> virou o IPC `coop.sync`, no botão **"Reconciliar jogadores"** da mesma aba.
> Sem essa ordem, tirar o botão tiraria dela o gesto de recuperação do "P2 que
> dura dois segundos". Roteiro:
> [PEDIDOS-DELA-01, pedido 1](2026-08-03-PEDIDOS-DELA-01-o-roteiro-dos-seis-pedidos-da-interface.md).

### AUTO-01.3 — o preset de co-op perde para sete outros perfis

Prioridades semeadas de fábrica:

```
80 sackboy_nativo   70 Aventura   65 Ação   60 FPS   60 point_and_click
55 Esportes   55 Corrida   50 Navegação   45 coop_local   10 bow   1 meu_perfil
```

O `coop_local` (45) perde até para o `Navegação` (50), que casa a janela da
Steam. **Abrir um jogo de co-op pela Steam entrega o perfil de navegação.**

Conserto: prioridade 75 ou mais. Uma linha.

### AUTO-01.4 — o instalador nunca aplica o wrapper aos jogos

O passo 11b roda apenas a migração — troca opções de lançamento venenosas
antigas. A função que aplica o wrapper a todos os jogos existe
(`integrations/steam_launch_options.py:466`) mas **não tem modo de linha de
comando** e não é chamada pelo instalador. Um jogo que nunca teve opção
venenosa **nunca recebe o wrapper** até alguém abrir a janela e clicar.

### AUTO-01.5 — dois donos do valor padrão de máscara

O daemon usa `dualsense` (`lifecycle.py:140`); a janela e os presets usam `xbox`
(`integrations/uinput_gamepad.py:136`). **`gamepad on` pela linha de comando e
"Jogar pelo Hefesto" pela janela entregam máscaras diferentes** — e a máscara
decide se o jogo reconhece o controle.

### AUTO-01.6 — a máscara escolhida na aba Início não persiste

`app/draft_config.py:476` reemite o modo fotografado na inicialização; só o
editor da aba Perfis grava a seção. Trocar a máscara na Início e clicar em
"Salvar Perfil" **perde a máscara**. É o mesmo mecanismo do ABAS-01.

### AUTO-01.7 — parâmetros de módulo que exigem reboot sem precisar

O caminho de instalação por pacote escreve os parâmetros a quente
(`scripts/install-host-udev.sh:306`); o `install.sh` **não**. Todos os
parâmetros envolvidos são graváveis em tempo de execução. Copiar três linhas faz
as curas de conexão valerem **sem reiniciar** — inclusive a do segundo DualSense
que some.

Relacionado: `--no-dkms` derruba os **três** módulos de uma vez, incluindo a cura
medida do "segundo DualSense some". Precisa de opções separadas.

## Defaults a rever

| item | hoje | deveria | por quê |
|---|---|---|---|
| vibração | `balanceado` = ×0,7 | `máximo` ou `auto` | o padrão entrega 70% da vibração sem avisar |
| presets de gênero | 10 de 12 sem seção de modo | os de jogo com modo `gamepad` | casa com MODO-01: perfil sem modo não liga nada |
| catch-all | **dois** semeados | um só | dois catch-all disputando é parte do veto de MODO-01 |
| `--help` do instalador | corta no meio | mostrar inteiro | omite opções reais |

## Ordem de execução

1. **AUTO-01.1 + .2 + .3** — o co-op deixa de exigir terminal e passa a
   acontecer. É o que desbloqueia os quatro jogadores.
2. **AUTO-01.5 + .6** — um dono para a máscara, e ela persiste.
3. **AUTO-01.4 + .7** — instalação que termina o serviço, sem reboot.
4. **Defaults** — baratos, e cada um remove uma surpresa.

## Critério de aceite

Instalação limpa, quatro controles plugados, jogo aberto: **quatro jogadores,
sem abrir terminal, sem editar arquivo, sem reiniciar nada.**

E o instalador termina **sem pedir nada** — nem um comando para copiar.

---

## NOTA DATADA (09/08/2026) — seis de sete, e os quatro restos

Conferido no código de hoje, item a item. **O texto acima não foi reescrito** —
inclusive a nota de 06/08 sobre o botão de co-op, que continua valendo.

| item | veredito | onde está hoje | commit |
|---|---|---|---|
| **.1** a emulação nasce desligada | **ENTREGUE** | `daemon/lifecycle.py:1465` `aplicar_gamepad_para_multiplos_controles`, chamada no tique de 2 s em `:3673`. As três preferências vivem em `utils/session.py:486` `load_gamepad_preference` — a escolha dela vence sempre | `8fe735d` 25/07/2026 |
| **.2** co-op não existe na janela | **SUPERADO POR DECISÃO DELA** | o botão saiu porque o co-op deixou de ser opção (`daemon/lifecycle.py:167` `coop_enabled: bool = True`). O gesto insubstituível mudou de dono **antes** da remoção: `app/actions/home_actions.py:390` `RECONCILIAR_LABEL`, botão em `:991`, IPC `coop.sync` registrado em `daemon/ipc_server.py:163` e servido por `daemon/ipc_handlers.py:3569` | `ae32c10` 06/08/2026 |
| **.3** o preset de co-op perdia para sete perfis | **ENTREGUE** | `assets/profiles_default/coop_local.json:8` tem `priority: 75` (era 45; o `navegacao` é 50). Quem já instalou é migrado por `profiles/loader.py:385` `migrate_modo_jogo_nos_presets`, chamada em `:464` | `54f1f3b` 25/07/2026 |
| **.4** o instalador nunca aplicava o wrapper | **ENTREGUE** | passo `11b-bis` em `install.sh:2645`, que chama `python3 "${LAUNCH_MIGRATE_PY}" --apply --stop-steam` em `:2528`. O modo de linha de comando que faltava existe: `integrations/steam_launch_options.py:1228` | `108b711` 04/08/2026 |
| **.5** dois donos do valor padrão de máscara | **ENTREGUE, com resíduo** | `app/actions/mode_transition.py:54` `plan_mode_transition` deixou de mandar `flavor` quando ela não escolheu, e o daemon preserva a sua. O `DEFAULT_FLAVOR` de `integrations/uinput_gamepad.py:136` sobrevive só como fallback declarado | `8fe735d` 25/07/2026 |
| **.6** a máscara da aba Início não persistia | **ENTREGUE** | `app/draft_config.py:702` `with_mode` marca o rascunho como sujo e `:616` decide se o modo vai junto; escritor único em `app/actions/home_actions.py:699` `registrar_modo_no_rascunho`, chamado pelo Aplicar em `app/actions/footer_actions.py:349` | `2bbfa22` 30/07 e `1c75a1a` 08/08/2026 |
| **.7** parâmetros de módulo exigindo reboot | **METADE ENTREGUE** | a escrita a quente existe: `install.sh:631-633` e `:702-713` gravam em `/sys/module/.../parameters/` sem recarregar módulo. **A outra metade não**: o `--no-dkms` continua único (`install.sh:239`), derrubando os três módulos de uma vez | `8fe735d` 25/07/2026 |

Os testes de aceite vivem em
`tests/unit/test_auto01_um_clique_em_vez_de_dez.py` — inclusive o
`test_as_duas_portas_de_entrada_pedem_a_mesma_coisa` (`:549`), que é a mordida
do item `.5`.

### Os defaults a rever

| item | veredito | onde |
|---|---|---|
| vibração `balanceado` = 0,7 | **NÃO ENTREGUE** | `daemon/lifecycle.py:197` e `:198`, intocados |
| presets de gênero sem seção de modo | **ENTREGUE** | sete dos treze têm `mode` hoje; lista em `profiles/loader.py:382` (`54f1f3b`, 25/07) |
| dois catch-all semeados | **NÃO ENTREGUE** | `assets/profiles_default/fallback.json:4` e `assets/profiles_default/meu_perfil.json:4` continuam ambos com `match: any` |
| `--help` cortando no meio | **ENTREGUE** | `install.sh:253-265`: a faixa fixa virou `awk` que cresce com o cabeçalho (`fc9a9f6`, 25/07) |

### Os quatro restos, que são o que sobra desta sprint

1. **O `--no-dkms` único** — precisa de opções separadas, ou desligar um módulo
   derruba a cura medida do "segundo DualSense some";
2. **O resíduo do `.5`, e ele é uma porta que ninguém tinha contado.** Os sete
   presets de jogo gravam `gamepad_flavor: "xbox"` fixo
   (`assets/profiles_default/`), então **ativar um preset impõe xbox** sobre o
   `dualsense` do daemon. A porta da linha de comando e a da janela foram
   unificadas; a **porta do perfil** não;
3. **O default de vibração** — o produto entrega 70% sem avisar;
4. **Os dois catch-all** disputando entre si.

### O grau, como manda a casa

**MEDIDO** para cada elo acima — há símbolo, chamador e teste. **SEM PROVA**
para o critério de aceite da sprint: *"instalação limpa, quatro controles
plugados, jogo aberto, quatro jogadores"*. Isso é **hardware na mão dela**, e o
código não pode responder por ele. O que o código prova é que cada elo existe;
o que falta é ver a corrente inteira puxar.
