# Como controlar e fotografar a janela do Hefesto no COSMIC

- **Levantado em:** 27/07/2026, fazendo — não lendo
- **Por quê:** o pedido foi *"controle cada aba da interface... tira prints igual
  vc já fez no passado, com tela maximizada"*. Levou cinco tentativas frustradas
  até achar o caminho que funciona, e o caminho não é óbvio
- **Serve para:** qualquer sprint de interface daqui em diante. É a base
  operacional da [PROVA-DE-TELA-01](../sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)

## O que funciona

```
wtype -M ctrl -k Next  -m ctrl     # próxima aba do GtkNotebook
wtype -M ctrl -k Prior -m ctrl     # aba anterior
claude-screenshot.sh               # imprime o caminho do PNG
```

Determinístico, e sem risco de acertar o botão de fechar. Exige a janela **em
foco**.

### A armadilha que estragou duas rodadas

**Rajada de teclas perde eventos.** Com 0,12 s entre os envios, um passo se perde
e **todas as fotos saem deslocadas em uma aba** — a foto chamada `gatilhos` mostra
`status`, e assim por diante. Aconteceu duas vezes antes de eu perceber.

O `wtype` cria e destrói um teclado virtual a cada chamada; o compositor precisa
de tempo para ver o dispositivo novo. **Mínimo de 0,45 s entre teclas**, e ainda
assim não confie: verifique.

## O sensor que resolve de vez: medir a aba ativa pelo sublinhado rosa

O tema declara, em `gui/theme.css`, que o rosa (`#ff79c6`) aparece em **dois
lugares apenas**: a marca e a aba ativa. Isso faz do pixel rosa na faixa da barra
de abas um sensor confiável de qual página está aberta.

```
convert <foto> -crop 1000x14+0+245 +repage -depth 8 txt:-
    -> procurar pixels com r>200, 90<g<160, b>170
    -> o centro do grupo diz qual aba, comparando com os centros conhecidos
```

Centros medidos, janela maximizada em 1920x1080:

```
Inicio 56 | Status 139 | Gatilhos 232 | Lightbar 332 | Rumble 429
Perfis 515 | Sistema 602 | Emulacao 706 | Navegacao DSX 840
```

Com o sensor, a captura vira um laço que **navega verificando**: tira foto, mede
onde está, manda a tecla que aproxima do alvo, repete. Zero deslocamento.

Ferramenta versionada em `scripts/gui-captura/`: `aba_ativa.sh` (o sensor),
`capturar_verificado.sh` (o laço que navega verificando) e
`retrato_offscreen.py` (o render de 1920x1080 para comparar antes e depois).

## O que NÃO funciona nesta máquina

| Tentativa | Resultado |
|---|---|
| `ydotool mousemove --absolute` | a versão instalada só tem `mousemove` **relativo** |
| `ydotool mousemove` relativo | o libinput acelera de forma não linear — medi desvio de **mais de 4x** numa calibração |
| `ydotool click 0xC0` | sintaxe nova; esta versão usa `click 1` |
| `wmctrl`, `grim`, `slurp` | não instalados |
| Ponteiro absoluto próprio via `/dev/uinput` | escrito e **não comprovado** — o compositor pode recusar o dispositivo |

**Consequência prática:** não dá para mirar num botão de 24 px com segurança. O
botão de fechar fica a 40 px do de maximizar, e o custo de errar é fechar a
janela dela. **Não force o clique; use teclado.**

E o `cosmic-screenshot` **não desenha o cursor**, então mover o ponteiro e
fotografar não prova onde ele está. Verificar posição por hover é inconclusivo.

## Maximizar: o problema sem solução automática encontrada

Com `autotile = true` (a configuração dela), uma janela nova **sempre** entra em
tiling e divide a tela com o terminal — cerca de 950 px de largura, onde o
conteúdo corta.

Tentei, e nenhum funcionou: `Super+M`, `Super+Up`, `F11`, duplo clique na barra
de título, `Super+Y`.

**O que resta é pedir a ela** — é um gesto de um segundo, e é mais barato que
arriscar fechar a janela. Registrado como limite honesto da automação, não como
tarefa pendente.

## Render offscreen: quando serve e quando engana

Para medir geometria e comparar antes/depois com a mesma régua, o caminho é
carregar o glade num `GtkOffscreenWindow` de 1920x1080 com o tema aplicado. O
"antes" sai de um `git worktree` do `HEAD`, sem tocar na árvore de trabalho.

```
git worktree add -f /tmp/hefesto-head HEAD
HEFESTO_RAIZ=/tmp/hefesto-head GDK_BACKEND=x11 python retrato_offscreen.py <saida>
git worktree remove /tmp/hefesto-head --force
```

**O limite, e ele me enganou uma vez:** o offscreen renderiza só o que está no
glade. Os cards da aba Status, os seletores segmentados e a lista de perfis são
construídos em **runtime**, em Python — então a aba Status aparece **vazia** e
comparar dois renders dela não mostra diferença nenhuma, mesmo com 150 linhas
alteradas.

Para a aba Status, só a janela real, com controle conectado, prova alguma coisa.

## A métrica que não mede o que promete

Usei "percentual de linhas de fundo liso" para diagnosticar o vazio das abas, e
o número foi útil: Rumble 75%, Gatilhos 58%, média de 47%.

**Ela não serve para medir a melhoria.** Ao compactar o conteúdo, o vazio deixa
de ficar espalhado e vira um bloco contíguo maior — então o percentual **sobe**.
Depois da VÃO-01 ele piorou em cinco abas, enquanto o defeito real (botão a 830
px do que ele comanda) tinha sido corrigido.

**Régua de diagnóstico não é régua de validação.** Para validar, o que vale é a
distância entre o controle e o conteúdo que ele governa.

## Guardar as fotos no repositório

Recortar a janela e reduzir a paleta deixa as nove abas em cerca de 680 KB —
mesma ordem de grandeza da convenção da casa:

```
convert entrada.png -crop 1910x975+5+45 +repage -strip -colors 128 saida.png
```

Destino: `docs/process/estudos/assets/<data>-<assunto>/`.

## Uma coisa que quebrei, para ninguém repetir

Para carregar código novo é preciso reiniciar a janela. Fiz assim:

```
nohup python -m hefesto_dualsense4unix.app.main >log 2>&1 &
```

e o processo **morreu junto com o comando** — ela ficou sem janela nenhuma até eu
perceber. O certo é desacoplar de verdade:

```
setsid python -m hefesto_dualsense4unix.app.main </dev/null >log 2>&1 &
```

E avisar antes: reiniciar a janela dela **fecha o que ela estava olhando**.
