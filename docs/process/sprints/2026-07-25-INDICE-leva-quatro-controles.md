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
| **JOGO-01** — o jogo enxerga quatro controles onde existe um | **máxima** | ABERTA |
| AUTO-01 — um clique em vez de dez | alta | ABERTA |
| NUM-01 — quem está na mesa é 1..N | alta | ABERTA |
| MODO-01 — o modo jogo liga sozinho | alta | ABERTA |
| MIC-USB-01 — três mutes empilhados | alta | ABERTA |
| ABAS-01 — as abas brigam pelo mesmo estado | alta | ABERTA |
| PLAYER-01 — um número de jogador, editável | média | ABERTA |
| LEGIBILIDADE-01 — texto legível, alvo clicável | média | ABERTA |

JOGO-01 subiu para máxima depois de aberta: ela é a única que impede **jogar**,
que é o propósito do projeto. As demais degradam a experiência; essa a impede.
