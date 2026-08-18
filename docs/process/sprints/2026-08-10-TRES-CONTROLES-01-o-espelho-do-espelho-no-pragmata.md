# TRES-CONTROLES-01 — o espelho do espelho, e o jogo com três controles

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"ok inputs ainda tão duplicado na hora do pragmata mesmo
  clicando lá em entregar o controle pra steam"*
- **Status:** **ENTREGUE EM CÓDIGO — AGUARDANDO A PALAVRA DELA.** O que falta é
  ela abrir o Pragmata e contar quantos controles o jogo mostra
- **Grau:** MEDIDO no `/dev/input` dela, com o jogo aberto

---

## 1. O que ela viu

Com a caixinha marcada, a exceção armada e o físico escondido, o controle
continuava dobrado. As três coisas que o produto prometia estavam feitas — e o
defeito estava intacto.

## 2. O que havia em `/dev/input`, medido com o jogo aberto

Quatro aparelhos para **um** controle físico:

| nó | nome | VID:PID | quem é |
|---|---|---|---|
| `event2` | Sony ... DualSense Wireless Controller | `054c:0ce6` | o físico dela |
| `event6` | DualSense Wireless Controller (Hefesto P1) | `054c:0df2` | o nosso vpad |
| `event21` | Microsoft X-Box 360 pad 0 | **`28de:11ff`** | Steam Input |
| `event23` | Microsoft X-Box 360 pad 1 | **`28de:11ff`** | Steam Input |

`28de` é **Valve**. O processo `steam` (pid 3699757) era o **único** com
`/dev/uinput` aberto além do `input-remapper` do sistema, e o `pad 0` nasceu no
**mesmo segundo** em que o daemon logou
`steam_input_excecao_ativada appid=3357650` (02:13:40).

São **dois** espelhos porque o Steam Input enxerga **dois** controles — o físico
e o nosso vpad — e faz um Xbox virtual para cada.

## 3. A causa

O `SDL_GAMECONTROLLER_IGNORE_DEVICES` que o wrapper entregava ao Pragmata listava
**só** `0x054c/0x0ce6`. Os espelhos da Valve nunca estiveram em lista nenhuma
deste projeto — `28de` não aparecia em **uma linha sequer** do caminho de launch.
O jogo ficava com três: o nosso vpad e os dois espelhos.

### Isto explica o que JÁ funcionava

Regra da casa: hipótese que não explica o passado é contorno. Esta explica.

Até 09/08 a exceção do Steam Input **suspendia o nosso vpad**. O Steam via um
controle só, criava um espelho só, e o jogo via um. A decisão dela de 09/08
(`ESCONDER-EM-VEZ-DE-SAIR-01`) manteve o vpad de pé para não derrubar o jogador 2
do co-op junto — **fechou aquela conta e reabriu esta pelo outro lado**.

O invariante da `JOGO-01` (25/07) é o mesmo dos dois lados, e é o que voltou a
valer aqui: *"a allowlist muda QUAL dispositivo o jogo vê, nunca QUANTOS"*.

## 4. A cura

O par `28de:11ff` entrou no `_IGNORE_VALUE` — **no valor, não num ramo novo**, e
isso é a decisão de desenho que mais importa neste arquivo. Assim ele herda, sem
uma linha de gate própria, os três portões que aquela variável já atravessa e que
custaram medição para existir: fora do Modo Nativo, com a emulação ligada, e só
com `cobertura_total` (um vpad por físico).

O invariante que manda aqui é **duplicado > zero controles**: se o IGNORE não
pode sair, o espelho da Valve também não é escondido, e o pior caso continua
sendo o controle dobrado — nunca um jogo sem controle nenhum. Há teste que morde
exatamente isso (`test_sem_cobertura_o_espelho_tambem_nao_e_escondido`).

O `PROTON_DISABLE_HIDRAW` **não** ganhou o par, e a diferença é de mecanismo: ele
faz o winebus negar hidraw, e o espelho da Valve não é um aparelho HID que o
Proton entregue — é um evdev virtual.

## 5. A saída que foi RECUSADA, e por quê

`SDL_GAMECONTROLLER_IGNORE_DEVICES_EXCEPT` resolveria em uma linha ("aceite só o
nosso vpad"), é mais robusta contra a Valve mudar de PID, e **está errada aqui**.

O motivo é uma exigência dela: *"deve ser universal, caso eu tenha 4 novos dual
sense ou novos pro controler ou 8bitdo"*. Um Pro Controller ou um 8BitDo chegam
ao jogo **por si** — o Hefesto os numera e acende o LED, mas não os adota —,
então um `_EXCEPT` com o nosso VID/PID apagaria todos eles da mesa.

Há teste que TRAVA essa decisão (`test_o_except_mataria_os_externos_dela`),
porque ela reaparece como boa ideia toda vez que alguém reencontra o problema.

**Quando isto caduca:** se um dia o produto ADOTAR os externos com vpad próprio
(a `E4` da `LUGAR-À-MESA-01`), o `_EXCEPT` passa a ser o desenho certo, e o teste
ganha uma nota datada.

## 6. Uma trava desta casa foi qualificada, não apagada

O `test_compose_env_continua_emitindo_um_par_so` afirmava, literalmente, que a
lista tinha um item e que não podia haver vírgula. **A razão continua inteira**:
somar o par de um controle **físico** sem a cobertura POR PAR da `E4` esconde
aquele aparelho do jogo sem haver vpad que o devolva.

O que mudou é que o par novo **não é um controle da mesa** — é um espelho, e
escondê-lo subtrai uma cópia, não um aparelho. O teste passou a se chamar
`test_compose_env_nao_esconde_controle_FISICO_sem_cobertura_por_par`, que é o que
ele sempre quis dizer, e a mensagem de falha diz ao próximo o que conferir.

## 7. O que continua ABERTO

- **A palavra dela.** Feche o Steam por inteiro (os espelhos são dele e só somem
  quando ele sai), abra de novo e abra o Pragmata. O jogo tem de mostrar **um**
  controle.
- **Os dois espelhos são criados de qualquer jeito** — a cura os esconde do
  jogo, não impede o Steam de criá-los. Se algum dia o Steam Input passar a
  numerar jogadores por conta própria a partir deles, isto volta por outra porta.
- **O rumble** continua sem causa provada (`ESTADO-DA-NOITE-01` §6). Nada aqui o
  toca, e o instrumento do anel segue esperando uma sessão de jogo.
