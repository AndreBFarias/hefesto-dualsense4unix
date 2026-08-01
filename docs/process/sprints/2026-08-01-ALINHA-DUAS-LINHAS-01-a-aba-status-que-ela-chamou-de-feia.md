# ALINHA-DUAS-LINHAS-01 — a aba Status que ela chamou de feia

- **Status:** ENTREGUE EM CÓDIGO em 01/08/2026, com medição antes/depois em
  bancada e **prova de tela**. O aceite final é o olho dela, pela
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
- **Prioridade:** ALTA — é a aba que ela mais olha, e a queixa foi literal:
  *"mas olha só essa interface aqui. tá absolutamente muito feio"*
- **Aberta em:** 01/08/2026, por ela, com print da aba Status maximizada
- **Absorve:** SOM-ROTA-NO-CARD-01, ESTADO-TRES-LINHAS-01, SOM-ROTULO-01 e
  MASCARA-CUSTO-01, que nasceram todas do mesmo print e da mesma conversa

## O pedido, item a item

Cinco coisas, ditas por ela olhando a tela:

1. *"alinha e estica a seção do giroscópio pra ficar entre o microfone e o
   triângulo"*;
2. *"alinha a seção do L2 e R2 pra ficar entre o touchpad e o analógico
   direito"*;
3. *"aquele botão de voltar ao anterior sai de lá de cima e fica no espaço onde
   tem 'não ajustado' no alto-falante"*;
4. *"arruma os dois botões, não sei se faz sentido ter o 'sem dado' e o
   'Devolver' — ou renomeia eles ou remove"*;
5. *"na guia de estado temos 5 linhas. Isso deveria ser no máximo 3 linhas
   sendo a última a bateria e ela usaria 100% da largura horizontal"*.

## O que a medição mostrou antes de qualquer linha mudar

Bancada offscreen na tela dela (1870px, card no teto de 1400):

| bloco | ia de | a | alvo dela |
|---|---|---|---|
| L2/R2 | 281 | 681 | **252 a 947** (touchpad → analógico direito) |
| giroscópio | 943 | 1377 | **968 a 1616** (microfone → último glifo) |

**As duas metades da faixa de baixo já eram os limites certos.** O que faltava
era alguém que os carregasse: a linha de cima era um `Gtk.Grid` com
`column_homogeneous=True`, que divide o card em duas metades IGUAIS — e as
metades da faixa de baixo não são iguais (698 contra 648). Dividir 50/50 punha
as duas divisórias 25px fora do lugar, e era isso que fazia a linha de cima
parecer de outro desenho.

## O que entrou

**1 e 2 — o alinhamento.** A faixa de baixo passou a ter duas METADES nomeadas
(`_metade_esquerda` = sensores + analógicos; `_miolo_inferior` = áudio +
glifos), e dois `Gtk.SizeGroup` amarram cada coluna da linha de cima à metade
correspondente. O `column_homogeneous` saiu. As barras de L2/R2 e o desenho do
giroscópio deixaram de ser presos com `halign=START` e passam a preencher a
coluna que o SizeGroup mediu.

Medido depois: em 1180px o alinhamento é **exato nos dois lados**; em 1870 a
diferença é de 4 a 5px, que é a borda da moldura do bloco.

**O número do giroscópio mudou de lado, e isso não estava no pedido.** Com o
desenho esticado a 640px, um valor ancorado na borda direita ficaria a mais de
meio card do "X" que o nomeia — o defeito 4 da STATUS-SIMETRIA-02 de volta,
pior. O valor agora fica logo depois da letra do eixo, e a barra ocupa o resto:
a distância entre nome e número virou constante do desenho, em qualquer
largura. Ganho de quebra: os três valores ficam alinhados entre si.

**3 — o botão da rota no bloco do alto-falante.** O rótulo de valor saiu da
linha de ações e o botão entrou no lugar dele. O valor foi para o rótulo da
moldura: **"Alto-falante · 71 %"**.

As outras duas casas para o valor foram medidas e cada uma quebra uma regra já
paga: dividir a linha com a barra faz a barra medir 276px debaixo de um medidor
de microfone de 360 (a CARD-OCUPA-01 exige os dois iguais, e há teste); dividir
a linha com a escala encurta o controle deslizante abaixo da barra que ele
comanda (SOM-03, e há teste). O rótulo da moldura já existia e não custa pixel.

O botão continua sendo **UM** — o widget do glade, reparentado para o slot do
card primário por `status_actions._alojar_botao_da_rota`. A segunda razão da
SOM-04 para ele viver no frame Estado (a saída padrão do sistema é um fato
GLOBAL, e dois cards não podem ter dois botões para um interruptor só) continua
inteira. A primeira razão — *"não cabe, +36px"* — valia para ACRESCENTAR uma
peça; aqui ele SUBSTITUI, e o custo medido foi de **8px** numa faixa com 100px
de folga (o card pede 367 dos 467).

**4 — os dois botões.** `sem dado` não era rótulo de ação: era a janela
escrevendo "não sei" dentro de um botão, no lugar onde deveria dizer o que o
clique faz. Ele some — do alto-falante **e do microfone**, que tinha o mesmo. O
botão passa a se chamar sempre pela ação (`Silenciar`) e nasce insensível
enquanto não há leitura; quem explica o porquê é a dica. Um botão cinza não
promete nada.

`Devolver` FICA, e é decisão medida: esta linha é a mais apertada do card e
agora recebe também o botão da rota. *"Devolver ao controle"* custaria ~90px a
mais e faria os três rótulos elipsarem em 1180. Quem diz devolver o quê a quem
é a dica, que cabe inteira.

**5 — o frame Estado em três linhas.** De 2 colunas × 5 linhas para 4 colunas ×
2 linhas, mais a bateria numa caixa própria com largura inteira:

```
Conexão: Conectado      Transporte: USB
Perfil ativo: Nenhum    Hefesto: Ligado
Bateria: [=================================] 75 %
```

Duas armadilhas apareceram na bancada e as duas estão curadas:

- **o número boiando.** O `GtkProgressBar` desenha o texto CENTRADO — numa
  barra de 1244px o "75 %" ficava a 609px de cada borda, que é palavra por
  palavra o defeito que ela apontou nas barras de L2/R2. O `show-text` saiu e o
  número virou um rótulo ao lado, colado no fim da barra;
- **a coluna de valores voltando a 1242px.** A linha da bateria ficou FORA do
  grid, numa caixa vertical: uma célula de `GtkGrid` nunca é mais larga que as
  colunas que ela abrange, então pedir largura inteira de dentro do grid fazia
  as quatro colunas expandirem juntas. E o grid ganhou `halign=start` — sem
  ele o GTK3 despejava todo o excedente na última coluna (1549px para "USB").

## MASCARA-CUSTO-01 — a resposta à pergunta dos sensores

Ela perguntou junto: *"não sei se o alto-falante, giroscópio, microfone e
touchpad na hora de jogar um jogo na Steam vão estar funcionando. Elas precisam
funcionar."*

A auditoria de 01/08 mediu e a resposta tem duas metades:

| recurso | máscara DualSense | máscara Xbox |
|---|---|---|
| giroscópio | FUNCIONA (medido: 158 Hz, 473 janelas distintas em 3 s) | **NÃO EXISTE NA API** |
| touchpad (dedo e clique) | FUNCIONA — o clique tem caminho próprio desde a SENSOR-VIVO-01/E4 | **NÃO EXISTE NA API** |
| microfone | FUNCIONA — é PipeWire, não passa pelo gamepad | igual |
| alto-falante | FUNCIONA — idem | igual |

O gamepad virtual só espelha giroscópio e touchpad no backend `uhid`, e
`integrations/virtual_pad.py` recusa o uhid para todo sabor que não seja
`dualsense`; o vpad `uinput` declara 8 eixos e 11 botões, e não há onde pôr IMU
nem dedo. **Não é defeito: é a API do controle de Xbox.**

**O risco real não é bug, são os perfis.** Medido na máquina dela em 01/08:
`acao`, `aventura`, `corrida`, `esportes`, `fps` e `coop_local` — seis dos oito
— pedem `gamepad_flavor: "xbox"`. Nesses jogos o giroscópio e o touchpad estão
desligados **por configuração, sem nenhuma mensagem**.

A entrega desta sprint é a ETIQUETA DE PREÇO, não a troca dos perfis: trocar a
configuração dela sem pedir é exatamente o que esta casa não faz. Abaixo do
seletor de máscara da aba Início agora aparece, quando a máscara é Xbox, o que
o jogo perde — e o que ele NÃO perde (vibração, microfone e alto-falante
continuam), porque ela citou os quatro recursos juntos e um aviso pela metade
mandaria caçar problema no lugar errado.

**Fica para ela decidir:** trocar os seis perfis para DualSense (a máscara
DualSense foi validada em jogo real — Sackboy, Mad King, Pragmata — e vibra), ou
manter Xbox nos jogos que não usam giroscópio nem touchpad.

## Os testes que mudaram, e por quê

Sete testes travavam a decisão ANTIGA. Nenhum foi apagado; todos passaram a
medir a regra nova, e a mordida de cada um está escrita no docstring.

| teste | o que travava antes | o que mede agora |
|---|---|---|
| `test_a_barra_do_gatilho_nao_toma_a_largura_do_card` | `alocada <= 400` (número fixo) | a barra termina onde a metade esquerda termina |
| `test_o_numero_do_giroscopio_fica_perto_do_nome_do_eixo` | a LARGURA do desenho (315..420) | a DISTÂNCIA entre o nome e o número |
| `test_gyro_oculto_nao_devolve_a_largura_toda_aos_gatilhos` | `column_homogeneous is True` (o mecanismo) | os gatilhos não mudam de largura quando o gyro some (o comportamento) |
| `test_o_numero_da_bateria_nao_boia_no_meio_da_barra` | o vão dentro da barra | `show-text` desligado + a distância barra→número |
| `test_a_coluna_do_som_nao_e_a_mais_alta_da_faixa` | irmãos diretos de `_linha_inferior` | as colunas NOMEADAS (o reagrupamento tirou os glifos da lista) |
| `test_o_botao_mora_no_frame_estado_e_nasce_insensivel` | o botão mora no grid | renomeado; o grid é o BERÇO, a casa é o card |
| `test_o_botao_ocupa_o_vao_horizontal_que_ja_existia` | coluna 2, `height >= 2` (literais) | deriva coluna e linhas do próprio grid |

**Um teste NOVO:** `test_mascara_diz_o_que_custa.py`, quatro casos — a frase
nomeia giroscópio e touchpad; a máscara DualSense não inventa aviso; payload
incompleto não vira aviso (a mesma família de erro que o `or "xbox"` que a
AUTO-01.3 já removeu daqui); e a frase diz o que CONTINUA funcionando.

## O que NÃO foi feito, e por quê

- **Os seis perfis com máscara Xbox continuam como estão.** É configuração
  dela.
- **O `hexpand` da lista de perfis** (aba Perfis) continua: o glade tem a
  decisão contrária escrita logo acima dele.
- **O clique do touchpad e o dedo dentro do jogo** não têm como ser fechados
  sem a mão dela: a medição ao vivo mostrou 473 janelas de IMU distintas em 3 s
  e `com dedo: 0`, `com clique: 0` — que é o esperado com o controle na mesa. O
  aceite é abrir um jogo que use o touchpad como botão e apertar.

## Aceite

**Executável, verde:** suíte completa, oito portões de CI, mypy, coleta.

**O que só ela pode dar:** olhar a aba Status na janela real e dizer se as duas
linhas agora leem como um desenho só. A bancada
(`scripts/gui-captura/`, mais o retrato da aba com o card vivo) prova a
geometria; ela é que diz se ficou bom.
