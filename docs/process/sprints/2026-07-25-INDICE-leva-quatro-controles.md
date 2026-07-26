# Leva de 25/07/2026 — "no final das contas teremos quatro controles funcionando"

> **A frase que define o escopo**, dita pela mantenedora ao abrir a leva:
>
> > "No final das contas teremos controles via cabo, via BT, tanto os da 8BitDo,
> > como os da Nintendo e os DualSense que são o foco. Os 4 controles são co-op."
>
> Tudo aqui serve a isso. O que não serve a isso não entrou.

## Como esta leva nasceu

Não de uma auditoria programada. Nasceu de sete queixas ditas em sequência
enquanto o projeto era estudado, e a ordem em que apareceram importa — três
delas mudaram de causa depois de medidas, e uma foi resolvida sem tocar em
código.

| # | Queixa, nas palavras dela | O que se descobriu | Sprint |
|---|---|---|---|
| 1 | "o branco sempre liga no player 2 setado" | Reserva de slot permanente por endereço; não é ordem de conexão | NUM-01 |
| 2 | "não tá conectando via cabo, nenhum dos DualSense" | **Cabo físico defeituoso** — o kernel nunca viu o aparelho | *(sem sprint — ver pesquisa)* |
| 3 | "modo jogo não liga automaticamente" | Cinco defeitos independentes, mais um buraco de projeto | MODO-01 |
| 4 | "a escolha do player não sincroniza com o botão superior" | Cinco conceitos numéricos distintos colididos em três widgets | PLAYER-01 |
| 5 | "o microfone aparece sempre como mudo mesmo com USB" | Mute persistido pelo WirePlumber por rota; a tela dizia a verdade | MIC-USB-01 |
| 6 | "não precisar alterar 10 coisas em abas, fechar a Steam..." | 29 pontos de fricção; o instalador fecha a Steam duas vezes e falha na terceira | AUTO-01 |
| 7 | "botões muito pequenos, fontes minúsculas, cores que não permitem leitura" | A escala tipográfica é código morto; 10 pares reprovam contraste AA | LEGIBILIDADE-01 |
| 8 | "no cabo ele fica player 1, mas ao abrir o jogo vai pro player 2 e não funciona" | A allowlist do Steam Input desliga o dedup e o jogo enxerga **quatro** dispositivos | JOGO-01 |
| 9 | "o microfone aparece sempre como mudo mesmo com USB" | Três mutes empilhados, em três camadas; nenhum curável pela janela | MIC-USB-01 |
| 10 | "explore os conflitos entre as abas, procure placeholders" | 17 conflitos, 4 com perda silenciosa de dados | ABAS-01 |

## A queixa que não virou sprint, e por quê

A queixa 2 trazia uma hipótese junto: *"imagino que algum teste esteja ativado e
motivando isso"*. Um único contador do journal do kernel refutou a hipótese sem
abrir uma linha de código do projeto:

```bash
journalctl -k -b 0 | grep -c "idVendor=054c"   # → 0
```

Zero significa que o aparelho **nunca se apresentou ao barramento**. Nenhuma
regra de udev, filtro do daemon, política do broker ou suíte de testes age antes
disso. O kernel havia escrito o diagnóstico 24 vezes:

```
usb usb1-port3: Cannot enable. Maybe the USB cable is bad?
```

A mantenedora trocou o cabo e o controle enumerou em segundos. **Registro
completo em [`docs/research/2026-07-25-forense-usb-cabo-morto-e-crc-bluetooth.md`](../../research/2026-07-25-forense-usb-cabo-morto-e-crc-bluetooth.md)**,
que também documenta um segundo achado colhido no caminho: 163.925 falhas de CRC
em Bluetooth num único boot, com qualidade de enlace 0 e sinal forte — a
assinatura de interferência de rádio, que degrada o co-op sem produzir erro
visível na interface.

**A regra de método que este episódio deixa:** o relato de quem usa traz junto
uma hipótese de causa, e a hipótese é parte do relato, não da evidência. Medir a
camada mais baixa primeiro custa um comando e economiza uma auditoria inteira na
camada errada.

## Ordem de execução

As sprints estão ordenadas por **o que desbloqueia o objetivo dos quatro
jogadores**, não por esforço.

```
AUTO-01  emulação e co-op nascem prontos      ← sem isto, 4 controles = 1 cursor
   │
   ├── NUM-01     quem está na mesa é 1..N
   │      │
   │      └── PLAYER-01  um número só, e ele é editável
   │
   ├── MODO-01    o jogo entra em modo jogo sozinho
   │
   └── AUTO-02    uma janela de Steam, não três
          │
          └── AUTO-03  configurar um jogo em um clique

MIC-USB-01        independente, pode correr em paralelo
LEGIBILIDADE-01   independente, pode correr em paralelo
```

## Fora do escopo desta leva

- **As seis sprints de sala limpa** (CR-01 a CR-06). Decisão explícita da
  mantenedora: *"essas não faremos hoje"*. Continuam válidas e bloqueando a
  entrada de qualquer valor de curva no repositório.
- **MIC-BT-01** e **UI-SELETOR-01**, sprints já abertas em 25/07. UI-SELETOR-01
  é absorvida por PLAYER-01 (mesma superfície, mesmo conserto); MIC-BT-01 segue
  independente e é referenciada por AUTO-04.

## Estado

Todas as sprints nascem **ABERTAS**. Este índice é atualizado conforme cada uma
fecha, com o commit que a fechou.

| sprint | prioridade | estado |
|---|---|---|
| **JOGO-01** — o jogo enxerga quatro controles onde existe um | máxima | **ENTREGUE** `a343ff6` |
| AUTO-01 — um clique em vez de dez | alta | **ENTREGUE** `8fe735d` |
| NUM-01 — quem está na mesa é 1..N | alta | **ENTREGUE** `a343ff6` |
| MODO-01 — o modo jogo liga sozinho | alta | **ENTREGUE** `54f1f3b` — confirmado ao vivo |
| MIC-USB-01 — três mutes empilhados | alta | **ENTREGUE** `8f83897` |
| ABAS-01 — as abas brigam pelo mesmo estado | alta | **ENTREGUE** `d92b544` |
| PLAYER-01 — um número de jogador, editável | média | **ENTREGUE** `14cd31b` |
| UI-SELETOR-01 — ordem dos controles no seletor | média | **ENTREGUE** `14cd31b` — por absorção em PLAYER-01 |
| LEGIBILIDADE-01 — texto legível, alvo clicável | média | **ENTREGUE** `a343ff6` |
| RUMBLE-PRESO-01 — o motor girava para sempre | *(nasceu no meio da leva)* | **ENTREGUE** `603608d` + `c733176` |
| IDENT-01 — um controle, duas identidades | média | ABERTA |

> **Duas correções de registro, feitas em 25/07 à noite.** UI-SELETOR-01 não
> aparecia nesta tabela: ela havia sido entregue dentro de PLAYER-01 e continuava
> marcada como aberta no próprio arquivo. E **RUMBLE-PRESO-01 não tem documento
> de sprint** — existe só como esta linha e como os dois commits; nasceu no meio
> da leva e nunca foi escrita. Fica registrado em vez de parecer perdido.

## O que a validação em hardware provou, e o que ela abriu

Em 25/07 à noite, com os quatro controles na mesa e um jogo real: **os quatro
funcionaram**. A numeração saiu 1, 2, 3, 4, sem pular nem repetir, e sobreviveu a
reinício do daemon.

Dois defeitos novos apareceram justamente por ter chegado até aqui:

- **A numeração do jogo não é a nossa.** Medido pelos LEDs: os quatro controles
  físicos mostravam 1-2-3-4 (nosso número), e o gamepad virtual do jogador 2
  mostrava o padrão do jogador 4 — o número que o **jogo** atribuiu. O jogo
  numera pela ordem em que descobre os dispositivos, e não temos como impor a
  nossa. O caminho é o inverso: deixar o número do jogo chegar ao controle
  físico. O mecanismo existe para o jogador 1 e não alcança os do co-op.
- **O 8BitDo em modo PS4 não sobe pelo cabo.** Causa medida no kernel: ele
  responde ao pedido de endereço com 9 bytes em vez de 16. Patch escrito
  (`8b379ae`), **nunca carregado** — depende do próximo reinício.

## As sprints que a validação abriu

Nenhuma delas existiria sem ter chegado aos quatro controles jogando. Três vieram
da partida, uma da primeira inspeção visual da janela.

| sprint | de onde veio | estado |
|---|---|---|
| **PLAYER-LED-01** — o número do jogo chega ao controle | a numeração dessincronizada que ela viu na partida | **ENTREGUE** `d1177c2` |
| **CONTAGEM-01** — a janela mostra 2, 4 e 8 ao mesmo tempo | inspeção visual da interface | **ENTREGUE** `0c08e77` |
| **IDENT-01** — um controle, duas identidades | a pergunta dela: *"o 8BitDo sempre vai ser o 4?"* | ABERTA (média) |
| **MÁSCARA-01** — como este controle aparece nos jogos | desenho proposto por ela | ABERTA (média) — depende de IDENT-01 |

## As três sprints que só existiam como referência

O AUTO-01 mandava os pontos de fricção restantes para AUTO-02, AUTO-03 e AUTO-04,
e as três nunca ganharam documento. Foram escritas em 25/07 à noite, a partir de
**medição nova** — o mapeamento original dos "29 pontos de fricção" nunca foi
escrito em lugar nenhum, e só o número sobreviveu.

| sprint | o que mede | estado |
|---|---|---|
| **AUTO-02** — uma janela de Steam, não três | o instalador fecha a Steam duas vezes e o terceiro passo vira uma corrida contra ela subindo | ABERTA (alta) |
| **AUTO-03** — configurar um jogo em um clique | sete das nove abas para um jogo só, e dois pontos que descartam configuração em silêncio | ABERTA (alta) |
| **AUTO-04** — o que só existe no terminal | 53 capacidades da linha de comando classificadas contra a janela | ABERTA (alta) |

**O AUTO-02 corrige um erro do AUTO-01**, e a correção fica à vista: a explicação
de que a recusa do pin do Proton vinha do download de 450 MB do passo anterior
está errada em três pontos — o download é do próprio passo, e na maioria das
vezes não acontece. O defeito real é uma corrida, que é pior.

Duas observações dela viraram entrega dentro de sprints já abertas: o instalador
não chama a cura do microfone *(MIC-USB-01)*, e o vão vertical que sobrou na tela
ganha dono — botões maiores e a faixa do microfone *(CONTAGEM-01)*.

**A ordem de ataque, atualizada em 25/07 à noite.** PLAYER-LED-01 e CONTAGEM-01
eram as duas independentes e **foram entregues**. O que sobra, em ordem:

1. **IDENT-01** — é pré-requisito duro de MÁSCARA-01, e sem ela trocar o modo do
   8BitDo continua criando um controle novo que empurra alguém para o slot 5.
2. **MÁSCARA-01** — logo depois, e só depois.
3. **AUTO-02, AUTO-03 e AUTO-04** — independentes entre si e das anteriores.
   AUTO-02 é a que tem defeito com perda silenciosa de dado, então vai na frente.
4. **MIC-BT-01** — independente de todas.

**Nada desta leva noturna foi visto em hardware.** As duas entregas passaram por
39 mutações que derrubaram teste, e mutação não substitui partida — a validação
com os quatro controles continua pendente, e está no CHECKLIST.
