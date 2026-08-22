# As dicas — o texto que saiu da tela

A primeira versão desta aba tinha parágrafo explicativo embaixo de cada seção.
Ficou grande e cansativa. Nesta versão **quase todo texto explicativo virou
dica ao passar o mouse**, e a tela ficou 40 % mais curta.

Este documento é o contrato de escrita delas.

## Onde a dica mora

O projeto **não usa `GtkComboBox`** — usa o `SegmentedSelector`
(`app/widgets/segmented_selector.py`), que já tem o mecanismo pronto:

```python
seletor.set_tooltips({"economia": "...", "balanceado": "...", ...})   # :97-110
```

Para rótulo e caixa de marcar, `widget.set_tooltip_text(...)` direto. Nenhum
widget novo precisa ser inventado para isto.

## As três regras

**1. A dica diz a consequência, não a tecnologia.**
Vale a mesma proibição de jargão do resto da interface: nada de *daemon*,
*systemd*, *uinput*, *polling*, *throttle*, *JSON*.

> ✗ *"Desativa o autosuspend do btusb via regra udev"*
> ✓ *"Se o sistema desligar o adaptador para poupar energia, o controle cai
> sozinho no meio do jogo."*

**2. Nunca esconda numa dica o que a pessoa precisa para decidir.**
Dica é para quem quer entender **por quê**. Quem só quer escolher tem de
conseguir escolher sem passar o mouse em nada. Se a opção não faz sentido sem
a dica, o rótulo está errado — conserte o rótulo.

**3. Duas a quatro linhas. Uma ideia.**
Dica que precisa de parágrafo é sinal de que a decisão está complexa demais
para o lugar em que está.

## Duas afordâncias, e só duas

| Marca | Quando | O que faz |
|---|---|---|
| Sublinhado pontilhado | Rótulo que tem explicação | agente vira `help`; a dica abre no hover |
| `?` em círculo | Cabeçalho de seção e casos de canto | Igual, mais recebe foco pelo teclado (`tabindex`) |

Nada de ícone de ajuda em toda linha. Onde o rótulo se explica sozinho — *"Ligar
junto com o computador"* — **não há dica**, e isso é intencional.

## Acessibilidade

O `?` é focável pelo teclado porque a dica é a única fonte daquela informação.
No GTK, `set_tooltip_text` já responde a foco de teclado além do mouse. O
sublinhado pontilhado, aplicado a rótulo comum, não recebe foco — e nesse caso
a informação é sempre reforço, nunca a única via.

Tempo de espera: **800 ms no mouse, 0 ms no foco por teclado**, que é a regra
que o projeto já segue.

## Capitalização — a regra que estava sendo quebrada

Rótulo, opção e título começam com **maiúscula**. Vale para dentro do
segmentado, que era onde a inconsistência estava:

> ✗ `teclado sem fio` · `mouse sem fio` · `não sei`
> ✓ `Teclado` · `Mouse` · `Não sei`

Frase dentro da dica é frase normal: maiúscula no começo, ponto no fim.

## O inventário

| Onde | Texto da dica |
|---|---|
| >? | O mesmo exame que o Hefesto já sabe fazer pelo terminal, agora com resposta em uma linha. Só lê — não muda nada na máquina. |
| >Examinar de novo | Refaz o exame agora. Leva alguns segundos e não altera nada. |
| >Firmware dos adaptadores | Os adaptadores carregaram o firmware sem erro. Sem isso o Bluetooth nem sobe. |
| >Economia de energia desligada | O sistema está proibido de desligar os adaptadores para poupar energia. Se desligar, o controle cai sozinho no meio do jogo. |
| >Energia das portas | Nenhuma porta está entregando menos corrente do que o aparelho pede. |
| >Pareamentos salvos | Todos os controles têm pareamento salvo e válido. Pareamento pela metade faz o controle cair logo depois de conectar. |
| >Suporte ao controle | O módulo que fala com o DualSense está carregado. |
| >Vizinhança das portas | Há um Wi-Fi USB 3.0 na porta ao lado de um adaptador Bluetooth. Ele emite ruído bem em cima da faixa dos controles. Vale mudar de porta. |
| >? | A borda de cada card é a cor do plástico daquele controle. O anel roxo por dentro marca qual está selecionado no cabeçalho da janela. |
| >Cor: | Lida do próprio controle: o código da cor está no firmware, nos caracteres 5 e 6 do serial de fábrica. |
| >? | Lida do aparelho pelo cabo. Nada a preencher. |
| >Jogador: | Fixa este controle num número de jogador. Sem nenhum marcado, vale a ordem de chegada — que é como o Hefesto trabalha por padrão. |
| >Cor: | Lida do próprio controle, por cabo ou por rádio. |
| >? | Se o Hefesto não conseguir ler, este campo vira uma lista para você escolher. |
| >Modo: | O modo é escolhido na chave física antes de ligar, e o controle não anuncia qual escolheram. |
| >? | Muda só o desenho que aparece na tela. Nada é remapeado no controle. |
| >? | Preto puro sumiria no fundo escuro da janela, então a borda usa um tom clareado do mesmo plástico. |
| >Cor: | O Hefesto não conseguiu ler a cor deste controle. Escolha na lista e a borda passa a usá-la. |
| >Branco  Preto  Vermelho</ | White |
| >Preto  Vermelho | Midnight Black |
| >Vermelho | Cosmic Red |
| >Rosa  Roxo  Azul</bu | Nova Pink |
| >Roxo  Azul | Galactic Purple |
| >Azul | Starlight Blue |
| >? | O Hefesto enxerga os adaptadores, mas não enxerga onde eles estão. Cabo, hub e altura mudam o alcance e não aparecem em lugar nenhum do sistema. |
| >Em hub, com fonte | Lido do barramento USB: o Hefesto reconhece o hub e se ele tem fonte própria. |
| >Altura da antena: | Corpo humano absorve 2,4 GHz. Antena acima da linha das cabeças rende mais que antena perto. Nenhum barramento sabe disto — só você. |
| >Linha de visada: | Sem obstáculo entre a antena e quem joga. Também não há como medir. |
| >Rádio em uso · AA:BB:CC:11:22:33 | Aritmética da especificação do Bluetooth, não medição desta máquina: o rádio tem 1.600 fatias de tempo por segundo e todos os controles do mesmo adaptador as dividem. |
| >? | Tudo aqui divide a faixa de 2,4 GHz com os controles. O Hefesto encontra os aparelhos, mas não sabe para que servem. |
| >Frente · colado no vizinho | Dois rádios encostados um no outro se atrapalham. Vale afastar em portas diferentes. |
| >Trás · vizinho do adaptador 1 | USB 3.0 emite ruído de banda larga bem em cima dos 2,4 GHz. Ao lado do adaptador Bluetooth, atrapalha. |
| >? | Um teto para a mesa inteira. As abas continuam mandando no que fazem — só não passam daqui. Nenhum ajuste seu é apagado. |
| >Economia | Menos bateria gasta. A vibração chega com 40% da força e a barra de luz com 25% do brilho. |
| >Balanceado | Tudo como o jogo pedir, sem teto. |
| >Máximo | Tudo como o jogo pedir, e o giroscópio na taxa mais alta. |
| >Auto | Controle no cabo joga em Máximo. Controle em rádio abaixo de 20% de bateria cai para Economia sozinho. |
| >Ambiente: | O ícone na barra do sistema depende do ambiente. No COSMIC aparece sozinho; no GNOME precisa de uma extensão instalada. |
| >? | Detectado: COSMIC. Corrija se estiver errado. |
| >Reexaminar a mesa | Relê os adaptadores e os rádios. Não muda nada. |

Extraído do mockup. Ao implementar, este é o texto que vai para `set_tooltips` e
`set_tooltip_text` — não reescreva na hora.
