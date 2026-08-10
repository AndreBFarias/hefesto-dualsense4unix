# WRAPPER-EM-TODOS-01 — a invariante "duplicado > zero" com quatro controles

- **Status (09/08/2026):** **PARCIAL — E1, E2 e E4 ENTREGUES EM CÓDIGO, AGUARDANDO A
  PALAVRA DELA; a E3 continua ABERTA.** A invariante passou a exigir
  **cobertura**: `daemon/launch_env.py:900` `cobertura_total`, com o parâmetro
  `fisicos` em `:846` e a omissão registrada em `:915`. Entregue por `108b711`
  (04/08/2026) — **o mesmo commit que tocou esta sprint por último**.
  Conferência na [nota datada no fim](#nota-datada-09082026--a-frase-nenhuma-linha-de-código-tocada-deixou-de-ser-verdade)
- **O que falta ela validar, em uma linha:** plugar os quatro controles, abrir um
  jogo pela Steam, e ver se cada pessoa move o próprio personagem — a invariante
  desta sprint é *"duplicado é melhor que zero com quatro"*, e só a mesa dela
  diz se o preço valeu
- **Status anterior:** *"PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código
  tocada"*. **A frase não se apaga** — ela é o assunto da nota datada: no dia
  seguinte à escrita, o código foi tocado, e o cabeçalho continuou negando isso
  por cinco dias
- **Prioridade:** **ALTA, e urgente por um motivo de janela:** o passo que abre
  este risco **está na árvore de trabalho dela agora, não commitado**. É mais
  barato resolver antes do commit do que depois
- **Faixa:** 1 — o pior caso é *"o jogo não vê controle nenhum"*
- **Causa-raiz:** **PROVADA no código**; o disparo em campo é **SUSPEITA COM
  MECANISMO**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Sobre:** o passo `11b-bis` do `install.sh` (linhas 2432-2475, não commitado)
  e a `JOGO-COMPLETO-01`/E4

---

## O que mudou, e por que o risco é novo

O passo `11b-bis` aplica a chamada do wrapper `hefesto-launch` a **todos** os
jogos da Steam, sem flag. É pedido literal dela (*"isso deveria estar no install
sem flag"*), e a razão está certa: sem o wrapper, as envs que o projeto
materializa nunca são exportadas e **todo jogo enxerga dois DualSense**.

**O comentário do próprio passo mede o ponto crítico:** antes dele, `--status`
dizia *"veneno estático: 0 / chamadas do wrapper: 0"*.

> **Ou seja: as envs de desduplicação NUNCA foram exercidas em jogo nesta
> máquina.** Este passo liga de uma vez um caminho que nunca rodou em campo — e
> liga para todos os jogos ao mesmo tempo.

---

## O furo: a invariante foi calculada para 1 físico ↔ 1 vpad

A doutrina está escrita em três lugares — `daemon/launch_env.py:806-810`,
`assets/hefesto-launch.sh:19-20`, `install.sh:2455-2458` — e é a regra de ouro do
projeto:

> *"o pior caso continua sendo o controle duplicado de hoje — nunca um jogo que
> não abre."*

**Com quatro controles, ela não vale.** Dois elos provam:

### Elo 1 — `compose_env` decide pelo TIPO dos vpads, nunca pela CONTAGEM

`daemon/launch_env.py:635-638`:

```python
elif flavor == "dualsense" and all(b == "uhid" for b in backends):
    env["PROTON_DISABLE_HIDRAW"] = _DISABLE_HIDRAW_VALUE
    env["SDL_GAMECONTROLLER_IGNORE_DEVICES"] = _IGNORE_VALUE
```

`all(b == "uhid" ...)` pergunta *"todos os vpads que existem são uhid?"* —
**nunca** *"existe um vpad para cada controle físico?"*.

### Elo 2 — `_snapshot` só conta vpads que EXISTEM

`daemon/launch_env.py:665-669`:

```python
for player in players.values():
    vpad = getattr(player, "vpad", None)
    if vpad is not None:
        backends.append(str(getattr(vpad, "backend", "") or ""))
```

**Um jogador de co-op pendente — aguardando o `EVIOCGRAB`, com `vpad is None` —
não entra na lista.** E `backends` com um item só passa no `all(...)`
trivialmente.

### O que isso produz

`SDL_GAMECONTROLLER_IGNORE_DEVICES=0x054c/0x0ce6` esconde **por VID/PID**: os
**quatro** DualSense físicos somem do SDL de uma vez. Só os vpads que **existem**
reaparecem.

**O caso ruim é exatamente a mesa dela na noite de 02/08:** o `EBUSY` do grab
deixava jogadores pendentes o tempo todo (ver
[COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md)).

E o caso pior: **com o co-op desligado**, `player_indexes` diz que *"todos os
controles alimentam o MESMO vpad"* — o jogo veria **um** controle, com quatro na
mesa.

### E isso explica o que já funcionava

Com **um** controle, "todos os vpads são uhid" e "há um vpad por físico" são a
mesma frase. A invariante foi escrita quando as duas coincidiam, e continua
verdadeira nesse caso. **Ela só se separa a partir do segundo controle** — e o
wrapper nunca esteve ligado para provar isso.

---

## O segundo risco: o passo fecha a Steam durante o install

O `11b-bis` roda `--apply --stop-steam`. Ou seja: **fecha a Steam dela durante a
instalação** e reescreve todo `localconfig.vdf` (com backup por execução).

O passo **recusa** rodar com um **jogo** aberto (`rc=3`, nada é tocado) — isso
está certo e é a proteção que importa. Mas fechar a Steam sem aviso prévio é uma
ação que ela não pediu ao rodar `./install.sh`.

---

## As entregas

### E1 — a env de desduplicação passa a exigir COBERTURA, não tipo

`compose_env` só emite `SDL_GAMECONTROLLER_IGNORE_DEVICES` quando **existe um
vpad vivo para cada DualSense físico na mesa**.

**Onde:** `daemon/launch_env.py:628-640`, e `_snapshot` (`:665-669`) passa a
reportar também **quantos físicos** há — hoje ele não tem essa informação, e é
por isso que a decisão não pode ser tomada.

**Quando não houver cobertura total:** cai no comportamento de hoje sem o
`IGNORE` — que é o **controle duplicado**, o pior caso que a doutrina aceita.
`PROTON_DISABLE_HIDRAW` pode continuar (ele não esconde do SDL).

**Aceite:** com dois DualSense físicos e um jogador pendente, o `default.env`
sai **sem** `SDL_GAMECONTROLLER_IGNORE_DEVICES`. Medível sem hardware.

**A mordida:** um `_snapshot` falso com 2 físicos e 1 vpad → asserção de que a
env **não** foi emitida. *Arranque a checagem de cobertura e veja reprovar.*

**Por que é raiz:** a env existe para dizer *"ignore o físico, use o virtual"*.
Emiti-la sem haver virtual para todos é afirmar algo falso ao SDL.

### E2 — o jogador pendente conta como ausente, explicitamente

`_snapshot` hoje **omite** o pendente. Omitir e "não existir" são coisas
diferentes, e a diferença é justamente o que o `all(...)` não enxerga.

**Aceite:** `_snapshot` devolve os pendentes como tais, e `compose_env` os trata
como cobertura faltando — não como se não estivessem lá.

### E3 — o install avisa antes de fechar a Steam

O passo `11b-bis` diz, **antes** de agir, que vai fechar a Steam — e em modo
interativo aceita um "não" (o passo é idempotente; rodar depois com
`--apply` resolve).

Com `--yes` (sem TTY), segue como está: o comportamento não-interativo não muda.

**Aceite:** rodar `./install.sh` num terminal mostra o aviso antes de fechar a
Steam.

### E4 — a bancada que faltou

O caminho inteiro (`_snapshot` → `compose_env` → `materialize_launch_env` → o
`.env` que o wrapper lê) **nunca foi exercitado com mais de um controle**.

**As asserções que mordem:**

1. 1 físico + 1 vpad uhid → **com** `IGNORE` (o caso que funciona hoje);
2. 2 físicos + 2 vpads uhid → **com** `IGNORE`;
3. 2 físicos + 1 vpad (um pendente) → **sem** `IGNORE`;
4. 2 físicos + co-op desligado → **sem** `IGNORE`;
5. máscara `xbox` → o comportamento de hoje, intacto (a E1 não pode mudá-lo).

---

## Testes que vão reprovar

```
pytest tests/unit -k "launch_env or compose_env or wrapper or launch_options"
```

O `tests/unit/test_launch_options_apply_cli.py` (novo, na árvore) cobre o
**`--apply`**, não o `compose_env`. Os dois são caminhos distintos e nenhum
cobre o outro.

## O que NÃO fazer

- **Não reverter o passo `11b-bis`.** Ele é pedido literal dela e conserta um
  defeito real (todo jogo enxergando dois DualSense). O que se corrige é a
  **decisão da env**, não a aplicação do wrapper;
- **Não tirar o `PROTON_DISABLE_HIDRAW` junto com o `IGNORE`.** São coisas
  diferentes: o `DISABLE_HIDRAW` impede o winebus de entregar o hidraw do
  físico; o `IGNORE` esconde do SDL. Só o segundo pode zerar os controles;
- **Não incluir `0x0DF2` no `IGNORE`** — está escrito em
  `daemon/launch_env.py:87-89`: *"o vpad Edge 0df2 PRECISA do hidraw… NUNCA
  incluir 0x0DF2"*. É por ele que rumble, gatilhos e luz do jogo chegam;
- **Não mexer na recusa com jogo aberto** (`rc=3`). Ela protege progresso não
  salvo.

## O que fica ABERTO

- **a confirmação em campo:** subir quatro controles com um co-op parcialmente
  promovido, abrir um jogo e olhar a lista de controles. É a única medição que
  fecha a suspeita — e ela tem custo, porque o pior caso é um jogo sem controle
  nenhum;
- **o `--apply` já rodou na máquina dela?** Se o `install.sh` foi executado com
  o `11b-bis` presente, os jogos já estão com o wrapper. `python3
  src/hefesto_dualsense4unix/integrations/steam_launch_options.py --status`
  responde, e não escreve nada.

---

## NOTA DATADA (09/08/2026) — a frase "nenhuma linha de código tocada" deixou de ser verdade

Conferido no código de hoje. **O texto acima não foi reescrito.**

O cabeçalho afirmava, até hoje, *"Nenhuma linha de código tocada"*. O
`git log -S'_fisicos_na_mesa'` devolve `108b711` (**04/08/2026**) — **o dia
seguinte**. E o mesmo `108b711` é o último commit a tocar este próprio arquivo.
A sprint e a entrega das suas E1/E2/E4 caminharam juntas, e só o cabeçalho não
foi avisado.

| entrega | veredito | onde está hoje |
|---|---|---|
| **E1** — a env exige COBERTURA, não tipo | **ENTREGUE** | `daemon/launch_env.py:900` `cobertura_total = fisicos <= 0 or len(backends) >= fisicos`, consultado nos dois ramos (`:906` e `:910`). O `fisicos` entrou na assinatura em `:846`, e a omissão é registrada em `:915` (`launch_env_ignore_omitido_sem_cobertura`) |
| **E2** — o pendente conta como ausente | **ENTREGUE** | `_snapshot` passou a devolver cinco valores, com `_fisicos_na_mesa(daemon)` (`:930`) no fim (`:985`); consumido em `:1175`. O porquê está escrito em `:961-964` |
| **E3** — o install avisa antes de fechar a Steam | **ABERTA** | `grep` por *"fechar a Steam"* em `install.sh` devolve **zero**. O passo `11b-bis` continua rodando `--apply --stop-steam` sem aviso prévio |
| **E4** — a bancada que faltou | **ENTREGUE** | `tests/unit/test_wrapper_em_todos_cobertura.py` — arquivo dedicado a esta sprint, cobrindo os casos de cobertura parcial |

**A ressalva de método, e ela é minha:** a primeira redação desta nota citou um
símbolo — `garantir_hefesto_launch_em_todos` — que **não existe** neste
repositório. Foi corrigido antes de fechar, conferindo o `grep`. Fica escrito
porque é exatamente o erro contra o qual esta passada existe: remarcar por
dedução é como a fila se corrompe.

### O grau, como manda a casa

**MEDIDO** para a E1 — símbolo, chamador, commit e data. **SEM PROVA** para o
efeito: a invariante desta sprint só se prova com **quatro controles numa
partida de verdade**, e ninguém mediu isso. Enquanto isso não acontecer, esta
sprint é *escrita e parcialmente construída*, não *provada*.
