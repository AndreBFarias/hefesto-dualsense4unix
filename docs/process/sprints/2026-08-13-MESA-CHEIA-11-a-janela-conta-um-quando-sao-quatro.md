# MESA-CHEIA-11 — a janela conta um quando são quatro

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Índice da leva:** [as ondas da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** **PLANO — nada escrito em código**
- **Depende de:** nada
- **Custo mínimo:** 3 h 20 (quatro entregas, a mais cara de 65 min)
- **Zero pixel novo.** É a sprint mais barata da leva e a que mais frases
  conserta

---

## 1. O defeito, medido — duas famílias

Com quatro controles na mesa, a janela **conta um**. Em dois sentidos
diferentes, e o segundo é o grave.

### 1.a — A CEGUEIRA: avisos que calam justamente para quem precisa

| o aviso | o que ele faz | por que cala | onde |
|---|---|---|---|
| **Bluetooth frágil no Modo Nativo** | acende quando o Modo Nativo roda com o físico em BT — nasceu para o jogo não ficar cego ao controle | `result["native_bt_fragil"] = native_mode and transport == "bt"`, e `transport` é o do **primário** | `daemon/ipc_handlers.py:2006`; a janela lê em `app/actions/home_actions.py:372` |
| **áudio do controle presente** | diz *"mic+fone do DualSense ativos"* | é um `re.search(r"DualSense", cards_text)` — **um** basta para a linha dizer "presente" com quatro na mesa | `integrations/storm_doctor.py:299-306` |
| **co-op degradado** | avisa que um jogador subiu em uinput e pode ficar sem vibração | o daemon **sabe qual**: `motivos.append(f"jogador_{rotulo}_uinput")` (`daemon/subsystems/gamepad.py:1206`); a janela só testa `"jogador" in motivo` (`app/actions/home_actions.py:387`) e imprime *"um dos jogadores"* (`VPAD_COOP_DEGRADED_TEXT`, `:300-304`) | acima |

**O `native_bt_fragil` é o pior dos três, e é falso negativo**: com o P1 no cabo
e os P2/P3/P4 no rádio, o aviso **cala para os três que estão frágeis**. É a
situação de co-op mais comum — o primeiro plugado é o dela.

**Os três já têm o dado à mão.** Cada entrada de `controllers` no `state_full` já
carrega o `transport`; o `cards_text` do doctor **já é injetável** — o parâmetro está na própria
assinatura (`integrations/storm_doctor.py:299`), o `storm_report` o repassa
(`:322`) e a suíte já o usa assim (`tests/unit/test_storm_doctor.py:92` e `:96`)
—, o que faz "áudio presente em 3 de 4" se provar com string sintética e zero
aparelho; e o rótulo do jogador já viaja no
`dedup_motivo`.

### 1.b — O SINGULAR: oito frases que dizem "o controle" quando são quatro

Cada uma com o texto literal e o endereço:

| # | o que a tela diz | onde | o que o código faz |
|---|---|---|---|
| 1 | *"…os gatilhos, a cor e a vibração dele vão para o controle."* | `gui/main.glade:1975` (tooltip do Ativar) | `profile.switch` atinge os quatro |
| 2 | *"Desliga o Hefesto: o controle continua jogando…"* | `gui/main.glade:2484` (tooltip do `daemon_stop_button`, `:2483`) e `:2490` (descrição acessível) | são quatro que continuam |
| 3 | *"cura do travamento agendada (reconecte o controle p/ ativar)"* | `integrations/storm_doctor.py:279` | são quatro a reconectar |
| 4 | *"Microfone do DualSense:"* | `gui/main.glade:3219` | quatro microfones |
| 5 | *"Gamepad para os jogos:"* | `gui/main.glade:3013` | quatro vpads |
| 6 | *"Intensidade global:"* | `gui/main.glade:1571` | **este é o inverso**: é o único rótulo honesto sobre o daemon, e hoje contradiz a **gravação**, que é por peça (`app/actions/rumble_actions.py:551`) |
| 7 | *"O jogo vê o controle como:"* | `app/actions/home_actions.py:1093` | a máscara é reescrita nos **quatro** vpads a partir de um `gamepad_flavor` só |
| 8 | *"**Modo jogo**: PS + Options suspende mouse e teclado."* | `gui/main.glade:2890` | existe **um** `EvdevReader`, atrelado ao primário — `read_state` declara *"INPUT vem SEMPRE do controle PRIMÁRIO … single-controller por construção"* (`core/backend_pydualsense.py:2192-2195`). P2, P3 e P4 apertam e **nada acontece, sem erro e sem aviso** |

**A número 8 é a que mais engana**, e ela não se conserta com plural: o efeito
**é** de um só. O texto tem de dizer **qual**, e isso encosta na **D-10**. Por
isso ela entra aqui como *declarar o escopo* — não como promessa de que os
quatro passam a ter mouse.

---

## 2. As quatro entregas

| # | entrega | custo |
|---|---|---|
| **E1** | `native_bt_fragil` **por controle** — a flag deixa de olhar só o primário | 55 min |
| **E2** | o banner do co-op **nomear o jogador** — o `dedup_motivo` já traz o rótulo | 20 min |
| **E3** | `check_snd_audio_healthy` **contar** em vez de `re.search` — *"áudio presente em 3 de 4"* | 60 min |
| **E4** | as oito frases — plural onde é plural, **sujeito** onde o efeito é de um só | 65 min |

**A E4 vem por último de propósito:** se a **D-3** mudar o vocabulário da tela
(quatro painéis × um painel com marcas), oito frases são o mais barato de
refazer da leva inteira.

## 3. O que muda na tela

```
   HOJE  — P1 no cabo, P2/P3/P4 no rádio, Modo Nativo ligado
   ┌──────────────────────────────────────────────────────────┐
   │  (nenhum aviso)                                          │
   └──────────────────────────────────────────────────────────┘
     três controles frágeis e a janela calada

   DEPOIS
   ┌──────────────────────────────────────────────────────────┐
   │ ⚠ Modo Nativo com os Controles 2, 3 e 4 em Bluetooth:    │
   │   alguns jogos não os enxergam.                          │
   └──────────────────────────────────────────────────────────┘


   HOJE                                DEPOIS
   ┌────────────────────────────┐      ┌────────────────────────────┐
   │ O gamepad virtual de um    │      │ O gamepad virtual do        │
   │ dos jogadores do co-op     │      │ Jogador 3 subiu no modo     │
   │ subiu no modo simples…     │      │ simples…                    │
   └────────────────────────────┘      └────────────────────────────┘
     ela testa um por um                ela olha o controle certo

   HOJE: "áudio do controle presente (mic+fone do DualSense ativos)"
   DEPOIS: "áudio presente em 3 de 4 controles"
```

---

## 4. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_11_a_janela_conta_quatro.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — o `native_bt_fragil` do primário (é a principal)

**Arrancar:** manter a flag como `native_mode and transport == "bt"`, com
`transport` do primário (`daemon/ipc_handlers.py:2006`).

**Por que reprova:** o dublê tem quatro controles — o primeiro com
`transport = "usb"` e os outros três com `"bt"` — e o Modo Nativo ligado. A flag
velha devolve `False` e o banner **cala**. O teste exige que o aviso acenda e
que nomeie os três.

Esta é a principal porque é **falso negativo**: o aviso que existe justamente
para não deixar o jogo cego é o que fica cego.

### Mordida 2 — a contagem que vira booleano

**Arrancar:** devolver `"3 de 4"` mas manter o veredito em `OK` quando falta um.

**Por que reprova:** contar sem mudar o veredito é cosmética. O teste injeta um
`cards_text` sintético com três DualSense e um `state` com quatro controles, e
exige veredito **diferente** de "tudo certo". O `cards_text` já é injetável
(`integrations/storm_doctor.py:299`, repassado em `:322`), então isto roda sem
aparelho.

### Mordida 3 — o plural mecânico

**Arrancar:** trocar *"o controle"* por *"os controles"* na frase nº 8
(`gui/main.glade:2890`).

**Por que reprova:** o plural ali **piora** a mentira — passa a prometer a quatro
o que só um tem. O teste assere que a frase dos combos PS+X nomeia **um sujeito**
(quem comanda), não uma quantidade. É a mordida que impede a E4 de virar
`sed s/controle/controles/g`.

### Mordida 4 — a frase que volta a mentir

**Arrancar:** acrescentar uma frase nova no `.glade` dizendo *"o controle"* num
gesto que atinge os quatro.

**Por que reprova:** o teste varre os textos traduzíveis do
`src/hefesto_dualsense4unix/gui/main.glade` procurando o singular *"o controle"*
e cobra que cada ocorrência esteja numa lista de exceções **com motivo**. Sem
isso, as oito frases voltam em três meses.

**Ressalva de método, e ela é real:** esta mordida é a mais frágil das quatro —
varredura de texto por padrão erra nas duas direções. Ela entra como
**aviso com lista**, não como portão cego, e a lista de exceções nasce das
frases que hoje são legitimamente singulares.

### O que este teste NÃO prova

Que as frases novas são boas. Palavra de tela é léxico, e léxico é dela.

---

## 5. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **As oito frases novas** — cada uma é palavra de tela, e palavra de tela é decisão dela por regra da casa. As propostas estão na seção 3 | escrever as que ela aprovar |
| **A nº 8 (combos PS+X) encosta na D-10:** declarar *"só o Controle 1 comanda o PC"* é honesto e é também uma limitação exposta pela primeira vez | declarar o escopo, salvo palavra dela |
| **A nº 6 (*"Intensidade global:"*) espera a D-4:** ela é o **único rótulo honesto** sobre o daemon hoje, e mentirosa sobre a gravação. Mudá-la antes da D-4 é escolher a resposta pela porta dos fundos | **não tocar** nesta até a D-4 — está fora da E4 de propósito |
| **O aviso de BT frágil lista os MACs, os números de jogador, ou só a contagem?** | números de jogador, salvo palavra dela — é o vocabulário que o card já usa |
| — | as três entregas de cegueira, as sete frases liberadas, e as quatro mordidas |

---

## 6. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: tudo.** As três entregas de cegueira são funções puras com
entrada injetável; as frases são texto. Nada aqui precisa da janela aberta, do
daemon vivo dela nem de um segundo controle.

**Só a bancada dela:** que o aviso de BT frágil **acende no caso real** — Modo
Nativo, um no cabo e os outros no rádio — e que a frase cabe no banner sem
quebrar o layout da Início.

**Ela não vê nada disto hoje com um controle só**, e isso é o ponto: são
exatamente os defeitos que só existem com a mesa cheia, e que por isso
atravessaram meses sem ninguém notar.
