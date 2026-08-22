# MESA-CHEIA-09 — "aplicado" sem byte nenhum

- **Estado:** CONCLUÍDA — as três entregas estão de pé: `apply_output_for`
  devolve `ResultadoDeSaida` (`core/backend_pydualsense.py:4022`), o par
  `(aplicado_em, guardado_em)` sai em `daemon/ipc_handlers.py:935`, e
  `app/textos_de_aplicacao.py` existe, com portões em
  `tests/unit/test_mesa_cheia_09_*.py` (verificado em 21/08/2026)
- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`, sobre
  `cc768d4` (tag `v0.9.4.2`)
- **Índice da leva:** [as ondas da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
- **Status:** ~~**PLANO — nada escrito em código**~~ — **caducou em
  21/08/2026:** era verdade em 13/08; a cura entrou. Ver **Estado**, acima.
- **Depende de:** nada
- **Custo mínimo:** 2 h 15 (E1 45 min + E2 30 min + E3 60 min)
- **É a raiz de quatro mentiras da janela, e todas as quatro pioram com quatro
  controles na mesa**

---

## 0. Por que é UMA sprint e não três

O censo separou três itens: o retorno do `apply_output_for`, o `aplicado_em` do
`trigger.set`, e os toasts honestos da Lightbar. **Aqui eles são um só**, e o
motivo é mordida: o `trigger.set` só pode devolver `aplicado_em` **verdadeiro**
se o backend lhe disser se escreveu; e o toast só pode ser honesto se o IPC lhe
disser o mesmo. Três sprints em que duas não se provam sozinhas são três levas e
uma prova. Uma sprint com três entregas é uma leva e três provas.

---

## 1. O defeito, medido

**A janela diz "aplicado" em três situações reais em que nenhum byte saiu.**

O ponto único de silêncio é `apply_output_for`
(`core/backend_pydualsense.py:3384`). Ela é a **porta da camada da usuária** — o
próprio docstring o diz (`:3394-3397`: *"os chamadores são o
`led.set`/`trigger.set`/`player.set` com `uniq` (gesto na GUI) e o «Aplicar» do
rodapé"*) — e **devolve `None` em todos os caminhos**:

| o caminho | onde | o que acontece |
|---|---|---|
| **spec vazio** | `core/backend_pydualsense.py:3399-3401` | `return` seco |
| **sem MAC 12-hex** (receiver 2.4G, key por path) | `:3402-3407` | `logger.warning` e `return` |
| **controle DESCONECTADO** | `:3417-3423` | `logger.debug("apply_output_for_desconectado_registrado")` e `return` — o override fica **registrado** no mapa em memória e o hotplug o aplica; **só a escrita de hardware é pulada** |
| **escreveu de verdade** | `:3424-3426` | `_write_partial_output(...)` |

Os quatro caminhos são indistinguíveis de fora. Quem chamou não tem como saber
se o aparelho recebeu algo.

### E o IPC não consegue confirmar porque ninguém lhe contou

| RPC | o que devolve | onde |
|---|---|---|
| `trigger.set` | `{"status": "ok"}` **seco** | `daemon/ipc_handlers.py:958` |
| `trigger.reset` | `{"status": "ok"}` **seco** | `daemon/ipc_handlers.py:995` |
| `led.set` | `{"status": "ok", "aplicado_em": aplicado_em}` | `daemon/ipc_handlers.py:1061` |
| `led.player.set` | `{"status": "ok", "bits": ..., "aplicado_em": aplicado_em}` | `daemon/ipc_handlers.py:1104` |

**O padrão já existe na casa e está no arquivo ao lado.** O comentário que o
introduziu está em `daemon/ipc_handlers.py:1055-1060` e explica o vocabulário:
*"`aplicado_em` diz em QUE controles a intenção ficou registrada na camada que
sobrevive ao reassert — vazio significa «escrita global sem registro por
controle»"*.

### As quatro mentiras que descem daí

| a tela diz | onde | quando é falso |
|---|---|---|
| *"Gatilho esquerdo (L2): Rigid aplicado"* | `app/actions/triggers_actions.py:599` | alvo desconectado; alvo sem MAC; Modo Nativo com output mutado |
| *"Cor enviada ao controle ({pct}% de brilho)"* | `app/actions/lightbar_actions.py:54` | alvo desconectado |
| *"Desenho das luzes aplicado — …"* | `app/actions/lightbar_actions.py:986` | com o co-op ligado — e a **mesma aba** diz o contrário três centímetros abaixo: *"Aceso agora: o desenho do co-op — com o co-op ligado, é ele que manda nas 5 luzes."* (`:163-167`) |
| o `_safe_call` da ponte devolve `True` para **qualquer** resposta que não seja falha de transporte | `app/ipc_bridge.py:85-113` — o `return True, result` está em `:113` | sempre que o daemon responde `"ok"` sem ter escrito |

**Por que isto piora com quatro na mesa:** com um controle, "desconectado" é o
caso raro. Com quatro, **o alvo escolhido no cabeçalho é mantido de propósito
quando o controle some** — é a R-16 — e ela vai continuar clicando "Aplicar" num
controle que saiu da mesa, recebendo "aplicado" a cada clique.

---

## 2. As três entregas, e o que muda na tela

### E1 — `apply_output_for` para de ser silenciosa (45 min)

Ela passa a devolver **o que fez**, no vocabulário que a casa já usa:

    escreveu   -> o byte saiu para o aparelho
    registrado -> o override ficou no mapa; o hotplug aplica quando ele voltar
    sem_alvo   -> não há MAC 12-hex; nada foi guardado

Nada muda na tela ainda. Muda o que o andar de cima **pode** dizer.

### E2 — `trigger.set` e `trigger.reset` devolvem `aplicado_em` (30 min)

Espelho exato do `led.set` (`daemon/ipc_handlers.py:1061`). Mesmo nome de campo,
mesma semântica de vazio, mesmo comentário. **Não é padrão novo — é o padrão do
arquivo ao lado, aplicado ao vizinho que ficou de fora.**

### E3 — os toasts dizem a verdade (60 min)

```
   HOJE, com o "Sony 2" desconectado
   ┌────────────────────────────────────────────────┐
   │ Gatilho esquerdo (L2): Rígido aplicado         │
   └────────────────────────────────────────────────┘
     e nenhum byte saiu

   DEPOIS  (o texto exato é decisão dela — ver D-9)
   ┌────────────────────────────────────────────────┐
   │ Gatilho esquerdo (L2): Rígido guardado para o  │
   │ Controle 2 — ele está fora da mesa; entra       │
   │ quando voltar.                                  │
   └────────────────────────────────────────────────┘


   HOJE, com o co-op ligado
   ┌────────────────────────────────────────────────┐
   │ Desenho das luzes aplicado — Jogador 3          │
   ├────────────────────────────────────────────────┤
   │ Aceso agora: o desenho do co-op — com o co-op   │
   │ ligado, é ele que manda nas 5 luzes.            │
   └────────────────────────────────────────────────┘
     a MESMA tela, contradizendo a si mesma

   DEPOIS
   ┌────────────────────────────────────────────────┐
   │ Desenho guardado — com o co-op ligado, quem     │
   │ manda nas 5 luzes é ele. Vale quando o co-op    │
   │ sair.                                           │
   └────────────────────────────────────────────────┘
```

**A GUI já tem os dois dados que faltam**, e é por isso que a E3 custa uma hora e
não um dia: quem está na mesa vem de `_uniqs_conectados`
(`app/actions/lightbar_actions.py:206-228`) e o co-op ligado já está na instância
(o texto de `:163-167` é escolhido por ele).

---

## 3. O teste que MORDE

Arquivo novo, `tests/unit/test_mesa_cheia_09_aplicado_e_verdade.py`. <!-- ref-externa: arquivo a CRIAR por esta entrega, ainda não existe -->

### Mordida 1 — o retorno que não distingue (E1, é a mordida principal)

**Arrancar:** fazer `apply_output_for` devolver sempre `"escreveu"`.

**Por que reprova:** o dublê de backend tem **dois** MACs no mapa de overrides e
**um** handle em `_handles`. O teste chama a função para os dois e exige
`"escreveu"` no conectado e `"registrado"` no ausente. Um retorno constante
falha no segundo — e é justamente o caso que a tela mente hoje.

### Mordida 2 — o `aplicado_em` que mente por construção (E2)

**Arrancar:** devolver `aplicado_em` com o MAC pedido, sem olhar se escreveu.

**Por que reprova:** mesma mesa da mordida 1. O teste exige que o `trigger.set`
para o MAC ausente devolva `aplicado_em` **vazio**, pela mesma regra que o
comentário do `led.set` já fixou (`daemon/ipc_handlers.py:1055-1060`). Copiar o
nome do campo sem copiar a semântica é o pior dos dois mundos: o cliente passa a
confiar num campo falso.

### Mordida 3 — o toast que ignora o retorno (E3)

**Arrancar:** manter `_toast_trigger` decidindo pelo `ok` booleano de hoje.

**Por que reprova:** o dublê de ponte devolve `{"status": "ok", "aplicado_em":
[]}`. Com o booleano, o toast diz "aplicado"; o teste exige a palavra de
"guardado" (a que ela escolher na **D-9**). É a mordida que liga as três
entregas: sem ela, E1 e E2 entram e a tela continua igual.

### Mordida 4 — a contradição do co-op

**Arrancar:** o gate de co-op no toast do desenho das luzes.

**Por que reprova:** o dublê tem o co-op ligado. O teste assere que o toast e o
rótulo de `app/actions/lightbar_actions.py:163-167` **não se contradizem** —
concretamente, que as duas frases não afirmam donos diferentes das 5 luzes ao
mesmo tempo. É o defeito medido ao vivo em 03/08 e nunca curado do lado da tela.

### O que este teste NÃO prova

Que o byte saiu. Ele prova que a janela **diz** o que o daemon **sabe** — a
distância entre o que o daemon sabe e o que o aparelho recebeu é outra sprint, e
hoje é medida por ensaio (`docs/data/ensaios.csv`).

---

## 4. O que é decisão dela, e o que é execução minha

| decisão dela | execução minha |
|---|---|
| **D-9: aplicar num controle DESCONECTADO é "aplicado" ou "guardado"?** É vocabulário puro, custo zero, e decide o texto das três entregas. Hoje a tela diz "aplicado" e o aparelho não recebeu nada — o override fica registrado e pega no hotplug (`core/backend_pydualsense.py:3417-3423`) | escrever a palavra que ela escolher, uma vez, nos quatro lugares |
| **O toast do co-op some ou muda de texto?** Sumir é limpo; mudar ensina | mudar, salvo palavra dela — sumir deixa o clique sem retorno |
| **O "guardado" merece marca na tela** (um controle com ajuste pendente), ou basta o toast? Marca é o começo de uma fila visível | só o toast, salvo pedido dela |
| — | os três retornos, o campo do IPC, os quatro textos e as quatro mordidas |

---

## 5. O que se prova sem aparelho, e o que só a bancada dela fecha

**Sem aparelho: tudo.** Backend com dublê de handles, IPC com dublê de
controller, GUI com dublê de ponte. Nenhuma linha desta sprint precisa de
aparelho, de janela aberta ou do daemon vivo dela.

**Só a bancada dela**, e é uma coisa só: que o "guardado" **cumpre** — desligar
o controle 2, aplicar Rígido nele, religar, e o gatilho estar lá. O mecanismo
existe — o docstring o promete em `core/backend_pydualsense.py:3390-3392`
(*"o hotplug lê o mapa, não o JSON do perfil, e aplica quando ele chegar"*) — e
**ninguém nunca o viu acontecer** com um controle na mão.

**E há uma armadilha desta casa que vale para a prova de bancada:** com install
editable, cura de daemon só vale no **próximo start**, e o sintoma de esquecer
isso é a **ausência** de dado novo, não um erro.
