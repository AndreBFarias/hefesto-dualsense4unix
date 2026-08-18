# O crítico do guia de isolamento, e o que sobrou dele — 13/08/2026

> **Por que esta página existe.** O
> [`METODO-DE-ISOLAMENTO.md`](../METODO-DE-ISOLAMENTO.md) foi reescrito em 13/08 e
> entrou na árvore pelo commit `874fdda` (+679/−42 naquele arquivo). **Ele não
> entrou sem passar por um crítico.** Esta página guarda o veredicto desse crítico e
> o desfecho de cada defeito que ele levantou — porque nesta casa a prova de que uma
> página foi criticada antes de entrar vale tanto quanto a página.
>
> **O crítico morreu e foi relançado.** A primeira rodada dele durou 84 s e terminou
> às 03:05 de 13/08, quando a sessão encerrou; o relançamento correu contra o patch
> recuperado de um worktree órfão, com a árvore em `cc768d4`. É o mesmo padrão do dia
> `2026-08-06`: o trabalho existia e a sessão não o guardou.
>
> **O que foi conferido no transporte, em 13/08:** os quatro `caminho:linha` que esta
> página cita foram abertos contra a árvore de HOJE (`874fdda`), e **um deles
> precisou de correção** — a correção está registrada abaixo, na seção "O endereço que
> apodreceu dentro do próprio commit".

---

## O veredicto, na letra dele

**Aprovado: NÃO. Aplica na árvore viva: sim.**

A parte de cima do veredicto é elogio medido, e importa porque é o que diz *até onde*
a crítica chegou:

- os **três defeitos que reprovaram a v1 sumiram, e sumiram direito** — não há
  "EACCES ... 50 ms" em lugar nenhum do arquivo; a tag `uaccess` não foi
  ressuscitada; e "insista até a ACL" deu lugar a *"quem escreve por hidraw tem de
  ser o DAEMON, pelo handle que o broker abriu"*, que é a conclusão literal do ensaio
  `uaccess-nao-gruda-em-device-virtual`;
- **cerca de cinquenta números e vinte e duas citações `caminho:linha` conferidos, e
  nenhum número inventado**;
- as duas runs de CI que o autor jurava ter deixado de fora — e que estavam no
  texto — são **verdadeiras**: a mesma SHA `973c92c` deu `success` às 05:00:39Z e
  `failure` às 05:11:20Z;
- o patch **aplica limpo** (`git apply --check` rc=0), toca **um só arquivo**, e os
  três portões de documento saem verdes na cópia.

E a reprovação, também na letra dele: *"Reprovo assim mesmo, por três coisas baratas
de consertar: DOIS comandos literais NÃO RODAM como escritos e um deles MENTE. Num
guia cuja tese é 'o instrumento mente mais que o produto', entregar instrumento cego é
o defeito que ele mesmo nomeia."*

**A contagem real dos problemas — porque a contagem também é número.** Ele levantou
**doze**, não doze de qualquer jeito: **seis** marcados `corrigir-antes-de-commitar` e
**seis** marcados `nota`. Quem repetir "três bloqueios e nove notas" está repetindo uma
contagem de memória; a lista abaixo é a dele, item a item. Dos números conferidos,
**35 de 38 conferiram** — os três que não conferiram são os itens 4, 3 e 9 da tabela.

---

## Os doze problemas, e o que aconteceu com cada um

Estado conferido na árvore de hoje (`874fdda`), abrindo cada endereço.

| # | peso | o problema | estado hoje |
|---:|---|---|---|
| 1 | bloqueio | `file docs/data/ensaios.csv` não responde a pergunta que o guia manda fazer: o `file` **não diz** "with CRLF line terminators" para o que ele classifica como CSV — só `file -k` diz | **corrigido.** O guia manda `grep -c $'\r' docs/data/ensaios.csv` (`docs/process/METODO-DE-ISOLAMENTO.md:543`) e explica o modo de falha do `file` logo abaixo (`:547-553`) |
| 2 | bloqueio | `scripts/ensaio_rumble_em_par.py --listar` não roda como escrito: modo 664, e quebra em `import evdev` fora do `.venv` | **corrigido.** As duas ocorrências passaram a `.venv/bin/python …` (`:46` e `:402`) |
| 3 | bloqueio | as duas falas da armadilha `A-20` não existem em lugar nenhum da árvore — e uma delas é atribuída a ela | **corrigido declarando a origem.** O guia diz hoje, logo abaixo das falas: *"As duas falas acima são relato da sessão de 12→13/08, não citação de documento. Não as procure na árvore"* (`:831-832`) |
| 4 | bloqueio | a citação `ensaio_rumble_um_bit_por_vez.py:356` era apresentada como "mesma guarda", e a linha 356 é `def daemon_ativo()` — o detector, não a recusa | **corrigido, e caducou de novo.** Ver a seção seguinte |
| 5 | bloqueio | *"Rode isto **antes** de acreditar em qualquer leitura:"* era seguido direto por `### Forma 1`, sem bloco de comando — na bancada, um beco | **corrigido.** A frase agora entrega o comando (`:397-403`) |
| 6 | bloqueio | o bloco de isolar por MAC nunca dizia **como** se descobre o MAC do alvo, e não avisava do modo de falha mais provável | **corrigido nos dois.** O exemplo aponta a origem (`:627`, *"o MAC do alvo, do HID\_UNIQ acima"*) e o guia acrescentou *"se nada acontecer em NENHUM dos quatro, desconfie do MAC, não do produto"* (`:653`) |
| 7 | nota | o relatório do autor contradizia o próprio patch: dizia ter deixado os IDs de run de fora, e o patch os citava | **corrigido no guia.** A linha traz hoje a cláusula que faltava — "runs do GitHub Actions" — e diz por onde conferir (`:484`) |
| 8 | nota | o MAC de exemplo `AA:BB:00:00:EE:FF` zerava os octetos 3 e 4, não a máscara da casa | **corrigido.** Hoje é `AA:BB:CC:00:00:FF` (`:627`), com a máscara explicada em `:634` |
| 9 | nota | *"a régua foi escrita de manhã e na mesma tarde reprovou"* — "de manhã" e "na mesma tarde" não têm origem conferível | **corrigido.** As duas expressões não existem mais no arquivo |
| 10 | nota | achado colateral, fora do patch: `cli/cmd_lightbar_reset.py` continuava afirmando que "a barra continuou morta por cinco dias", frase que o caderno já derrubara | **corrigido — e é a colateral que rendeu mais.** O docstring ganhou o bloco `CORREÇÃO DATADA (11/08/2026), porque a afirmação abaixo era falsa` (`src/hefesto_dualsense4unix/cli/cmd_lightbar_reset.py:22-31`), com os quatro flagrantes de barra acesa e o ponteiro para o ensaio `lightbar-bt-sem-0x08-cinco-dias` |
| 11 | nota | *"o primeiro octeto par é locally administered"* é impreciso: par é o bit 0; localmente administrado é o bit 1 | **corrigido.** O guia diz hoje *"o **bit 1** do primeiro octeto (`0x02`)"* e cita a fonte certa (`:71` → `integrations/uhid_gamepad.py:572-573`, que fala em "faixa **localmente administrada** (bit 1 do primeiro octeto)") |
| 12 | nota | o `grep` do uevent usava `hidrawN` genérico e o guia nunca dizia como se descobre o `N` | **corrigido.** O laço `for d in /sys/class/hidraw/hidraw*` entrou em três lugares (`:62`, `:139`, `:600`) |

**Onze fechados por `874fdda`, e o décimo-segundo fechado duas vezes** — o problema 4
foi corrigido naquele commit e quebrado pelo mesmo commit, e só ficou fechado com a
correção desta leva (seção seguinte). É a leitura honesta da tabela, e ela vale
registrar por um motivo que não é elogio: um crítico que reprova e é atendido inteiro é
barato; o que custa é o crítico que ninguém lê. Este foi lido.

---

## O endereço que apodreceu dentro do próprio commit

O problema 4 é o único com desfecho em duas partes, e a segunda parte é a lição.

O crítico pegou que `ensaio_rumble_um_bit_por_vez.py:356` apontava para
`def daemon_ativo()` — o detector — enquanto a recusa de verdade morava mais abaixo.
O autor corrigiu **contra a árvore `cc768d4`**, e a correção estava certa **naquela
árvore**: em `cc768d4` a faixa `775-784` abria em `def modo_ensaio` e continha o
*"Rode de novo com --confirmo-parar-o-daemon"*, e `791-793` era o segundo aborto.

Só que **o mesmo commit `874fdda` que publicou a correção também mexeu no script**:
acrescentou a coluna `resultado_da_feature` ao escritor do caderno, `+9/-1` linhas,
todas antes da linha 700. Tudo abaixo desceu oito linhas. Hoje:

| o que | onde estava (`cc768d4`) | onde está (`874fdda`) |
|---|---|---|
| `def modo_ensaio` e a recusa | `775-784` | **`783-792`** |
| o aborto "O daemon NÃO parou" | `791-793` | **`799-801`** |
| `daemon_ativo()`, o detector | `356` | `356` (não moveu) |

**Corrigido nesta leva**, em `docs/process/METODO-DE-ISOLAMENTO.md:111-113` — as duas
faixas passaram a `783-792` e `799-801`. As outras duas citações do mesmo bloco
(`scripts/ensaio_o_keepalive_mata_o_rumble.py:281-287` e o `idade_do_daemon()` da linha
`390`) foram abertas e continuam exatas.

**A lição, que já é a armadilha 6 do mapa do projeto e ganhou aqui o caso mais curto
que a casa tem:** o endereço não apodreceu em seis horas, apodreceu **no ato de
publicar**. Corrigir citação contra a árvore que se está prestes a mudar não basta —
tem de ser contra a árvore que vai ficar. E o portão que a casa criou no mesmo dia
(`scripts/validar-citacoes-de-linha.py`) **não pega este caso**, por desenho declarado:
ele vigia só `docs/protocol/` (`scripts/validar-citacoes-de-linha.py:82`), e só cobra
conteúdo quando a citação **nomeia** um símbolo entre crases colado ao endereço — a
faixa `:783-792` do guia não nomeia nenhum.

---

## O guia serve com o controle na mão?

O crítico não parou na leitura: pegou duas seções e tentou executar cada linha, com o
controle na mesa e o daemon vivo. É o teste que a casa chama de PROVA-DE-TELA aplicado
a um documento.

**Seção "Pergunta 0: em QUEM o instrumento está mirando?"** — o primeiro comando do
guia era o que menos funcionava (problema 2, hoje corrigido). O segundo, o `grep` do
uevent, ele rodou em todos os nós `hidraw` da máquina dela e a tabela de leitura **bate
linha a linha**: o nó do vpad traz `HID_PHYS=hefesto-vpad` e `HID_UNIQ=02:fe:…`; o
DualSense físico no cabo traz `HID_PHYS=usb-0000:…:input3`, que é a linha "caminho USB"
da tabela. A linha "MAC do adaptador" não pôde ser conferida ao vivo (não havia
DualSense no rádio naquele momento) e ficou sustentada pelo código
(`scripts/identidade_do_vpad.py:43` e `:57`).

**Seção "Isolar por MAC"** — o bloco Python **confere inteiro** sem precisar rodar nada
contra o daemon dela: o caminho do socket existe no disco como escrito e é socket mesmo
(`srw-------`); o enquadramento por linha bate com o servidor
(`daemon/ipc_server.py:281` faz `reader.readline()` e `:286` responde com `+ b"\n"`); o
handler aceita `side`, `mode`, `params` e `uniq`; e o "Cuidado medido" do guia é exato —
`trigger.set` devolve `{"status": "ok"}` puro enquanto `led.set` devolve `aplicado_em`.

**E daí saiu um achado de produto, que não é do guia.** Lendo `_apply_por_uniq`
(`daemon/ipc_handlers.py:821-840`, o mesmo endereço que o mapa do projeto usa no achado
A-1), o crítico viu que a função devolve `True` assim que chama `apply_for`, **sem
conferir se aquele MAC casa com algum controle conectado**. Consequência na bancada:
com um dígito trocado no MAC, **nada acontece em nenhum dos quatro controles e o daemon
responde `ok`** — e quem estiver medindo lê isso como "o produto não obedeceu". Foi
essa leitura que virou a frase do problema 6, hoje no guia em `:653`.

---

## Os portões, e a prova de que eles mordem

Rodados pelo crítico numa cópia com o patch aplicado e `git add -A` feito antes:

```
python3 scripts/validar-acentuacao.py --all        -> rc=0, saída vazia
python3 scripts/validar-glifos.py --all            -> rc=0, saída vazia
python3 scripts/validar-referencias-docs.py --all  -> rc=0, "OK: 271 documento(s) sem referência morta."
```

**E a mordida, porque nesta casa instrumento verde não vale sem mordida:** ele
acrescentou ao fim do guia uma linha com três palavras portuguesas escritas sem acento
e um emoji. Os dois portões reprovaram na hora e **apontaram o lugar**: o de acentuação
nomeou o arquivo, a linha 919 e a palavra, com a forma acentuada como sugestão ao lado;
o de glifos nomeou a mesma linha, a coluna 59 e o `U+1F680 ROCKET`. Restaurado o
arquivo, os dois voltaram ao verde.
(Esta página não reproduz as três palavras: o portão de acentuação varre `docs/` e
reprovaria a citação delas — a prova da mordida seria uma mordida nova.)

Três portões extras saíram verdes e nenhum foi pedido: `check_anonymity.sh`,
`check_test_data.sh` e `gerar-mapa.py --check`. O `check_paridade_transporte.py` não
roda limpo e é **pré-existente** — mas confirmou os três números que o guia usa:
*"graus fortes 15 / desses, SEM ensaio no caderno: 0 / ensaios lidos do caderno de
bancada: 77"*.

**O que ele não rodou, e disse:** `pytest`, `ruff`, `mypy` e
`check_version_consistency` — o patch é um `.md`, e a suíte cria dispositivos virtuais
numa máquina com quatro DualSense pareados e o daemon vivo. Ficou dito como pendência
de leva, não como resultado. **A árvore dela ficou intacta**: `git status --porcelain`
com zero linhas ao fim, HEAD ainda em `cc768d4`.

---

## O que este episódio deixa para a próxima sessão

1. **Um crítico relançado depois de morrer entrega mais do que um crítico novo.** Ele
   partiu do patch e da lista de defeitos da v1, e por isso pôde medir *o que foi
   consertado*, não só *o que está errado*.
2. **Reprovar por comando que não roda é reprovar pelo que importa.** Os três
   bloqueios de execução eram, os três, sobre o guia funcionar com o controle na mão —
   e um deles (`file` que não diz CRLF) era o defeito que o próprio guia nomeia.
3. **Corrija endereço contra a árvore que vai ficar, não contra a que você está
   lendo.** É o caso mais curto de citação podre que esta casa registrou: apodreceu no
   ato de publicar.
4. **A crítica rendeu fora do arquivo criticado.** O achado colateral do
   `cmd_lightbar_reset.py` e o modo de falha do `_apply_por_uniq` não estavam no
   escopo pedido, e são os dois itens desta página com consequência em `src/`.
