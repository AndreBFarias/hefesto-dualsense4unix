# EMPATE-01 — três perfis empatados, e quem ganha é o alfabeto

- **Status:** ABERTA
- **Prioridade:** **CRÍTICA** — subiu de volta em 27/07 às 21h45, quando ela
  olhou o controle e disse *"o controle no bt tá sem cor. deve ter algo a ver com
  os perfis e prioridades deles"*. Estava certa
- **Faixa:** 1 — desfaz trabalho dela
- **Aberta em:** 27/07/2026, a partir da crítica adversarial do estudo desta
  sessão. **Mecanismo novo:** nenhuma sprint existente o cita
- **Medido no disco e no código dela, hoje**, não em documento antigo

## O que foi medido

Ela tem **três perfis catch-all**, todos com prioridade **0**:

| Perfil | Gatilhos | Modo |
|---|---|---|
| `fallback` | `Off` / `Off` | nenhum |
| `meu_perfil` | `Off` / `Off` | nenhum |
| `vitoria` | `Pulse` / `Pulse` | gamepad, DualSense, **co-op ligado** |

Os três empatam. E o desempate não é escolha de ninguém:

1. `profiles/loader.py:568` carrega com `sorted(directory.glob("*.json"))` —
   **ordem alfabética**;
2. `profiles/manager.py:624` ordena com
   `key=lambda p: (not p.e_catch_all, p.priority), reverse=True`;
3. os três produzem a **mesma chave**, `(False, 0)`;
4. o `sort` do Python é **estável**, e `reverse=True` não embaralha empatados —
   preserva a ordem de entrada.

Simulado com a chave real do `manager.py` e a ordem real do `loader.py`:

```
ordem final: [fallback, meu_perfil, vitoria]
vencedor em janela de desktop: fallback
```

## A confirmação — 27/07, 21h45, olhando o controle

Ela disse: *"o controle no bt tá sem cor. deve ter algo a ver com os perfis e
prioridades deles."* Medido no disco, no mesmo minuto:

```
fallback.json   lightbar = [40, 40, 40]      cinza quase preto
vitoria.json    lightbar = [129, 61, 156]    roxo
```

`[40, 40, 40]` num LED RGB é, a olho nu, **apagado**. É exatamente "sem cor".

E os dois empatam em prioridade 0, com `fallback` vencendo pelo alfabeto. **O
controle está sem cor porque um perfil chamado `fallback` ganhou do perfil que
leva o nome dela, por causa da letra F vir antes da V.**

Isso fecha o mecanismo com o sintoma, e é a razão de a prioridade ter subido de
volta para CRÍTICA.

### O erro de análise que isto corrige, e ele fica registrado

Algumas horas antes, o item 0 desta sprint foi respondido com *"a aba Status diz
Perfil ativo: Nenhum, logo o mecanismo não está mordendo"* — e a sprint foi
rebaixada para MÉDIA e tirada da leva.

**Estava errado, e o erro é instrutivo:** "Perfil ativo: Nenhum" não prova que
nenhum perfil forneceu os LEDs. Prova apenas que a tela não nomeia o vencedor —
que é, ela própria, parte do defeito que esta sprint descreve. A pergunta certa
não era à tela: era **ao controle**, que estava cinza o tempo todo.

Fica como armadilha de medição: **quando a tela é suspeita, ela não pode ser a
testemunha.**

## Por que isso importa

**`fallback` vence `vitoria` sempre**, em toda janela que não seja de jogo.

O `vitoria` é o perfil que leva o nome dela, tem gatilhos `Pulse` e tem
**co-op ligado**. O `fallback` desliga os dois gatilhos e não tem modo nenhum.

Isso é um mecanismo plausível — medido, não suposto — para a frase que já custou
uma auditoria inteira a esta casa:

> *"a config que eu deixo nunca é respeitada"*

E ele é **invisível pela janela**: os três aparecem com prioridade 0 e "Sempre" na
coluna *Quando usar*. Nada na tela diz que existe uma disputa, muito menos que ela
é resolvida por ordem de nome de arquivo.

## O que esta sprint NÃO afirma

**Não afirmo que este é o defeito que ela relatou.** Afirmo que:

- o mecanismo existe e está medido;
- o efeito prático é o oposto do que a tela sugere;
- e nenhuma sprint aberta cobre isso.

A queixa dela pode ter outra causa, ou mais de uma. Esta entra na fila como
hipótese **medida**, não como diagnóstico fechado — e o item 0 é justamente
confirmar se ela morde na prática.

## O segundo defeito, e ele é do PROJETO — não da máquina dela

Pergunta dela, 27/07: *"o perfil fallback não deveria ser tipo o padrão sony ou
algo assim pro player 1? pq o fallback ser esse cinza é péssimo"*.

Medido: o cinza **é semente do repositório**, em
`assets/profiles_default/fallback.json:11`:

```json
"leds": {
  "lightbar": [40, 40, 40],
  "player_leds": [false, false, true, false, false],
  "lightbar_brightness": 1.0
}
```

**Toda instalação nova do Hefesto nasce com isto.** Não é configuração dela: é o
padrão que a casa distribui.

E vale separar as duas metades, porque só uma está errada:

| Campo | Veredito |
|---|---|
| `player_leds: [F,F,V,F,F]` | **certo** — acender só a luz central é o padrão PS5 para um jogador |
| `lightbar: [40, 40, 40]` | **errado** — no PS5 o controle do jogador 1 é azul, não cinza |

### E a cura não é trocar cinza por azul

Azul fixo deixaria o **jogador 2 também azul**, quebrando a distinção que a
paleta canônica existe para dar.

A cura é o `fallback` **não ter opinião sobre a cor**: remover o campo
`lightbar` do perfil semeado. Sem opinião, vale a cor automática por jogador
(`core/led_control.py:158`, `player_slot_color`) — azul, vermelho, verde, rosa —
que **é** o padrão Sony, e continua certo com um, dois, três ou quatro controles.

`[40, 40, 40]` nasceu com cara de neutro e não é neutro: é a opinião *"este
controle fica apagado"*, e ela vence quem tinha opinião melhor.

### Cuidado com quem já instalou

Mudar o arquivo semeado **não conserta quem já tem o perfil no disco** — o
`fallback.json` dela já está em `~/.config`. A entrega precisa dizer o que fazer
com o perfil existente, e **migração silenciosa de perfil é a classe de defeito
que causou o rollback de 26/07**: ou o programa avisa e ela decide, ou não mexe.

## Entregas

### E-1. O `fallback` semeado deixa de apagar o controle

Remover o campo `lightbar` de `assets/profiles_default/fallback.json`, e um teste
que reprove se ele voltar. O `player_leds` fica como está.



### Item 0 — RESPONDIDO em 27/07, 19h26

Com o desktop em foco, a aba Status da janela diz:

```
Perfil ativo:  Nenhum
```

E o journal do daemon **não tem nenhum evento de seleção de perfil hoje**.

**Conclusão:** o mecanismo do empate existe e está medido, mas **não está mordendo
agora** — nenhum dos três catch-all está sendo aplicado. Por isso a prioridade caiu
para MÉDIA e a sprint **não entrou** na leva executada de 27/07.

**O que isso não quer dizer:** não quer dizer que o empate seja inofensivo. Quer
dizer que hoje ele está a jusante de outra coisa — muito provavelmente o cadeado
`autoswitch_locked.flag`, ligado desde 24/07 20:42. **Assim que o autoswitch voltar
a aplicar perfil sozinho, é o alfabeto que decide.**

E fica registrada a lacuna que a crítica apontou e que esta sprint não fecha:
**nenhuma sprint de perfil diz o que muda com o cadeado ligado** — que é a
configuração real dela.

### E1 — empate de catch-all deixa de ser silencioso

Quando dois ou mais candidatos produzem a mesma chave de ordenação, o
`manager.py` registra o empate e **quem ganhou**, com os nomes de todos. Hoje ele
só loga o veto de catch-all em janela de jogo (`:614-621`); o empate no desktop
não deixa rastro nenhum.

### E2 — a janela mostra a disputa

Na aba Perfis, a coluna *Quando usar* passa a dizer, para catch-all empatado, que
existe disputa e quem vence. É a regra **R-A** da fila aplicada a este caso: *todo
controle que aceita um valor mostra, ali, o que aquele valor faz.* Prioridade 0
em três perfis não diz nada hoje; tem de dizer *"empatado com fallback e
meu_perfil — quem vale é fallback"*.

### E3 — desempate deixa de ser o alfabeto

Escolher um critério e escrevê-lo: o mais recentemente ativado, ou o marcado como
padrão pela usuária. **Ordem de nome de arquivo não é critério** — é acidente de
`glob`.

**Cuidado:** qualquer critério novo muda o comportamento atual dela. Não entra sem
o item 0 respondido e sem ela saber qual perfil passa a valer.

### E4 — teste que morde

Três catch-alls empatados, e o teste asserta **quem vence pelo critério
declarado**. **A mordida:** trocar o nome do arquivo perdedor para um que venha
antes no alfabeto. Se o teste continuar verde, ele está travando o alfabeto em
vez do critério — e é exatamente o defeito que esta sprint conserta.

## Como você valida

Sem terminal, dois minutos:

1. Com o desktop em foco (nenhum jogo aberto), abrir a aba Perfis e ler qual está
   ativo.
2. Conferir se os gatilhos estão como o `vitoria` manda (`Pulse`) ou como o
   `fallback` manda (desligados).
3. Depois da entrega: a coluna *Quando usar* tem de dizer que há disputa, e qual
   perfil vence.

## O que NÃO foi medido

- **Se o cadeado do autoswitch muda este caminho.** `autoswitch_locked.flag`
  está ligado desde 24/07 20:42 — é a configuração real dela, e **nenhuma sprint
  de perfil diz o que muda com o cadeado ligado**. Isso é lacuna das sprints, não
  desta.
- **Se `meu_perfil` e `fallback` ainda deveriam existir.** Dois perfis idênticos e
  inertes podem ser resíduo de semente. Apagar é decisão dela, não minha.
- **Se o mesmo empate acontece entre perfis específicos** de mesma prioridade —
  há dois pares em 55 e dois em 60 no disco dela. O mecanismo é o mesmo; o efeito
  não foi medido.
