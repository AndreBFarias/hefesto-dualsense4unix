# A fila do jogador — o que atacar, em que ordem, e por quê

- **Aberto em:** 26/07/2026, depois do checkpoint `v0.2.0`
- **Sucede:** [2026-07-26-INDICE-o-que-falta.md](2026-07-26-INDICE-o-que-falta.md),
  que continua valendo para o registro do rollback. Este documento reordena a
  fila com um critério declarado, e acrescenta as sprints abertas depois dele
- **Critério desta fase, dito pela mantenedora:** *qualidade de vida de quem
  joga, interface e uso vêm primeiro*

## O checkpoint

Antes de qualquer sprint desta fila, a árvore virou release. `v0.2.0`, publicada
em 26/07: os 31 commits da leva de quatro controles que nunca tinham sido
lançados, 5.529 testes verdes, `mypy --strict` limpo, quatro gates lidos.

Isso existe para que qualquer sprint daqui em diante tenha um lugar conhecido
para onde voltar. A v0.1.2 fica marcada como **retirada** no CHANGELOG, sem
reescrever histórico — a regra do `CLEAN-ROOM.md` vale também quando o
constrangimento é nosso.

## As quatro regras desta fase

Não são sprints. São invariantes: qualquer entrega desta fila que as viole
reprova, mesmo entregando o que prometeu. Elas saíram das causas medidas, não de
preferência.

### R-A. Conceito de implementação não aparece na tela

Prioridade numérica é o caso flagrante. Ela existe no arquivo e no schema, e não
tem por que existir como escolha livre de quem só quer jogar. A pessoa responde
*"aplica a: este jogo / uma categoria / tudo"*; a ordem sai daí.

**A prova de que a regra é necessária:** a escala da janela trava em 100
(`profiles_actions.py:1111`), e o catch-all dela estava exatamente em 100. Não
existia número escolhível pela interface que fizesse o perfil de um jogo vencer.
Consertar exigiu escrever `110` num arquivo JSON à mão. Não foi erro de uso — foi
um beco sem saída construído por nós.

### R-B. Nada age em silêncio

Todo clique ou produz efeito imediato, ou diz que ficou pendente e qual botão o
completa. Dez controles hoje escrevem só no rascunho sem nenhum aviso — é o que
produz *"clico e não acontece nada"* numa janela cujos 66 handlers estão todos
vivos.

### R-C. Um nome, um conceito

"Modo jogo" nomeia seis coisas; "jogador" nomeou cinco números; há dois botões
"Salvar" e seis "Aplicar" na mesma janela; um botão chamado "Modo jogo" **não**
liga o modo jogo. Cada colisão dessas já custou uma sprint inteira nesta casa.

### R-D. Um cadastro só por fato

O Steam Input está escrito em dois lugares — no `localconfig.vdf` da Steam e na
allowlist do Hefesto — e o produto consulta só um. Isso produziu quatro
joysticks para um controle. Onde houver dois registros do mesmo fato, um deles é
derivado ou o defeito volta.

## A fila

### Faixa 1 — desfaz trabalho dela

Estas entram primeiro porque o custo não é irritação: é ela perder o que já
tinha feito, no meio da noite de jogo.

| # | Sprint | Estado | Por que aqui |
|---|---|---|---|
| 1 | [**PERFIL-NASCE-CERTO-01**](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md) | ABERTA | Causa-raiz medida ao vivo em 26/07. O perfil do jogo nasce catch-all com prioridade 0 e **não há como fazê-lo vencer pela janela**. Absorve AUTO-03.1 e 03.2 |
| 2 | [**PERFIL-JOGO-01**](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | ABERTA | O flapping do modo jogo a cada troca de foco. É o sintoma no daemon do que a #1 causa nos perfis. Mexe no que roda durante a partida — por isso vem depois |
| 3 | [**DUPLO-REGISTRO-01**](2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) | ABERTA | Input duplicado medido: 4 joysticks para 1 controle. Remendo aplicado em 26/07; a cura é R-D |

### Faixa 2 — o que ela vê

| # | Sprint | Estado | Por que aqui |
|---|---|---|---|
| 4 | [**STATUS-SIMETRIA-01**](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md) | ABERTA | **Dívida do rollback.** É a única coisa que ela autorizou, e foi a extrapolada. Escopo trancado, um arquivo, valida de olho em dois minutos |
| 5 | [**BOTÃO-QUE-NÃO-MENTE-01**](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) | ABERTA | 145 controles na tela, 10 que agem em silêncio, 2 que mentem no tooltip. É R-B e R-C aplicadas |
| 6 | **CONTAGEM-E-COOP-01** | ABERTA — **sem documento** | Três denominadores na mesma janela; entrar na exceção do Steam Input derruba o co-op sem avisar |

### Faixa 3 — o que decide por ela

| # | Sprint | Estado | Por que aqui |
|---|---|---|---|
| 7 | [**STEAM-INPUT-01**](2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) | ABERTA | A tela não diz a regra, e o "desfazer" prometido não existe. Tem portão de medição no item 0 |
| 8 | **PROVA-DE-TELA-01** | ABERTA — **sem documento** | Dez minutos de olho antes de qualquer leva. Última a construir, **primeira a usar** |

### Faixa 4 — dívida que não morde hoje

| # | Sprint | Estado |
|---|---|---|
| 9 | [**DOC-VERDADE-01**](2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md) | ABERTA — contradições doccódigo |
| 10 | [**PROMESSA-NAO-CUMPRIDA-01**](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md) | ABERTA — dois itens ALTOS: as fontes nunca instaladas e o gate de emoji que nunca existiu |
| 11 | [PLAYER-LED-01](2026-07-25-PLAYER-LED-01-o-numero-do-jogo-chega-ao-controle.md) · [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md) · [MÁSCARA-01](2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) · [MIC-BT-01](2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) | ABERTAS, da leva de 25/07 |
| 12 | CR-01 a CR-06 — sala limpa | Fora de escopo por decisão dela; CR-02 segue bloqueando qualquer curva própria |

## Notas de arquitetura sobre as sprints existentes

Revisão feita depois de **olhar as capturas das nove abas**, não só o código.

### Sobre STATUS-SIMETRIA-01: o vazio é o material, não o estorvo

A sprint lista os 448 px de buraco horizontal como "o espaço que paga os três
primeiros defeitos" — está certo. Mas ela deixa **fora do escopo** os 307 px de
vazio **vertical** abaixo dos cards, com a nota "assunto de outra conversa".

Olhando a captura da aba Status, o vazio vertical é maior que isso: **os cards
terminam por volta de y=730 numa janela que vai até y=1050.** Cerca de um terço
da tela é preto liso, enquanto dentro do card os analógicos estão espremidos e os
dezesseis botões do DSX ocupam 9,2% da largura em 20 px cravados.

**Não estou pedindo para mudar o escopo dela.** O escopo trancado é o pagamento
da dívida do rollback e é sagrado — mexer nele repetiria exatamente o erro. Fica
registrado como o **próximo** passo natural, e com o argumento pronto: o card não
cresce para ocupar a janela, e é por isso que tudo dentro dele parece pequeno. A
legibilidade que ela pede tem espaço de sobra esperando; falta o card tomá-lo.

### Sobre a aba Status: uma contradição visível na própria captura

No canto superior direito a janela diz, em vermelho, **"Controle Desconectado"** —
enquanto dois cards abaixo mostram bateria de 67% e 74%. É a CONTAGEM-01 em
imagem. Vale como prova de que o defeito não precisa de teste para ser achado:
precisa de alguém olhando.

E na mesma captura: os dois cards dizem **"Lightbar: apagada"** logo acima de uma
barra colorida mostrando a cor. Duas frases sobre o mesmo estado, discordando,
a 20 px de distância.

### Sobre PERFIL-JOGO-01: a causa está uma camada acima

Aquela sprint abre com um aviso de honestidade dizendo que a causa não estava
isolada e que quatro sintomas cabiam na frase dela. A medição de 26/07 fecha
parte disso: **o perfil dela nunca vencia** (PERFIL-NASCE-CERTO-01), e por isso
o caminho do modo jogo padrão era o único que sobrava. As duas continuam
separadas — uma é a escolha do perfil, outra é o flapping do modo —, mas a
ordem entre elas agora tem razão medida.

## O que continua sem documento

Duas sprints existem só como seção de índice, e a regra que nasceu do rollback
vale para elas: **nenhuma entra em código antes de ganhar arquivo próprio.**

- **CONTAGEM-E-COOP-01**
- **PROVA-DE-TELA-01**

E três identificadores da madrugada seguem existindo só em mensagem de commit —
`MIC-FAIXA-01`, `SLOT-JOGADOR-01`, `VÃO-01` (`grep -rn` em `docs/` → zero
linhas). Mais `RUMBLE-PRESO-01`, entregue em 25/07 sem documento.

Há também três nomes órfãos citados dentro das sprints de 26/07 que não
correspondem a arquivo nenhum: `PERFIL-FIRME-01`, `STEAM-UMA-CHAVE-01` e
`STEAM-INPUT-SELF-HEAL-01`. São nomes provisórios que sobreviveram ao rascunho —
o mesmo defeito de "um nome, um conceito", aplicado ao processo em vez da tela.

## O que esta fila não resolve

- **A validação continua sendo de uma máquina só.** O checklist de hardware tem
  43 caixas e zero marcadas. PROVA-DE-TELA-01 existe para mudar isso e é a última
  da fila a ser construída — o que significa que, até lá, o que protege a
  interface é ela olhando.
- **734 testes de interface pulam no CI.** A camada onde a leva de 26/07 quebrou
  é justamente a menos coberta automaticamente.
- **Nenhuma sprint desta fila torna o Bluetooth mais confiável.** As duas causas
  de perda de pareamento seguem sem cura daqui, e o microfone por rádio segue
  entregando ~40% do sinal com a causa em aberto.
