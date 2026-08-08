# Retomar — o estado da mesa quando a máquina desligou

**Escrito em 07/08/2026, ao fim da sessão, a pedido dela:**

> *"deixa documentado pra que possamos desligar o pc sem perder nada do seu
> planejamento central e pra onde iremos"*

Este arquivo é o **primeiro** que se lê ao voltar. Ele não repete o que os outros
dizem — aponta para eles e diz **em que ordem**.

---

## Em uma página: o que este dia foi

07/08 foi um dia de **diagnóstico**, não de cura. Isso é deliberado e está
registrado: a numeração dos controles **não** foi consertada, e a razão é uma
cadeia que ela mesma criou, com bom motivo.

O que entrou em código: a licença resolvida, a língua do produto assumida, o
símbolo do painel, o interruptor do microfone, a caixinha do Steam Input, o
diário de bateria, a máquina da máscara, e quatro portões novos.

O que **não** entrou: a adoção dos controles externos, a cura do número trocado,
e a volta da luz. Os três esperam a cadeia abaixo.

---

## Os quatro documentos que dizem tudo

Leia nesta ordem:

| ordem | arquivo | responde |
|---|---|---|
| 1 | [a ordem de execução](sprints/2026-08-07-INDICE-a-ordem-de-execucao-do-que-o-diagnostico-abriu.md) | **em que ordem executar** — doze levas |
| 2 | [as decisões dela](2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md) | **o que ela decidiu** — 23 respostas que não se repropõem |
| 3 | [o diário de execução](2026-08-07-EXECUCAO-o-que-as-doze-decisoes-viraram.md) | **o que virou código**, e o que cada onda mediu |
| 4 | [a canônica dos externos](../protocol/externos-referencia-canonica.md) | **o que o Pro e o 8BitDo entendem** |

O dia anterior tem o seu:
[o dia dos cento e dezesseis agentes](sprints/2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md).

---

## A cadeia que manda em tudo

```
MASCARA-01 (as SEIS entregas, escritas e testadas)
        |
        v
   adoção dos externos (E3/E4 da LUGAR-À-MESA-01)
        |
        v
   a luz volta, com o número certo
```

**Duas travas dela seguram isso**, e as duas são decisão registrada:

- **resposta 3:** a adoção só depois da máscara por controle;
- **resposta 12:** a luz dos externos fica calada **até a entrega existir** — e
  ela manteve isso inteiro quando lhe ofereceram uma etapa intermediária que lhe
  daria dois controles numerados já.

**A resposta 18 desfez um impasse circular** que travaria tudo: a entrega 3 da
máscara conta como pronta quando a função **existe e é mordida por teste** —
ligar o fio é parte da adoção.

### E o fato que complica, medido

**Calar a luz curou, por acidente, um bombardeio que matava o Pro Controller**:
348 recusas do firmware com a luz ligada, **zero** desde as 15h27:48 de 07/08.

Voltar a escrever nos externos pode reabrir isso. A
[A-LUZ-QUE-CUROU-01](sprints/2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
tem o mecanismo inteiro, e a regra que dela nasce:

> **Nenhuma cura de luz entra antes da cura da numeração.** Acender antes é
> voltar a acender número errado, com mais confiança.

---

## O primeiro passo ao voltar, e ele tem prazo

**A leva 0 é a única cuja janela fecha sozinha.** Ela precisa acontecer **antes**
da primeira escrita nova de LED:

- recontar o experimento do Pro com as 24 horas completas;
- os 348 eventos do bombardeio estão num **buffer do journal** que morre no
  próximo restart da máquina.

Se a máquina foi desligada, **parte disso já se perdeu** — e não é grave: o
número principal (348 contra 0) está registrado na sprint. O que se perde é a
granularidade.

---

## O que está medindo sozinho, agora

**O diário de bateria começou a gravar às 21h35 de 07/08.** Primeira amostra: o
DualSense branco na faixa 70, o roxo na faixa 90.

Ele existe porque a hipótese mais forte para as quedas de link é **carga no fim**
— e até hoje o daemon media no escuro. **Ao voltar, a primeira coisa a olhar é o <!-- noqa-acento: "media" aqui é o pretérito imperfeito de MEDIR, que não leva acento; a sugestão "média" (o substantivo) falsificaria a frase. -->
que ele gravou:**

```
journalctl --user -u hefesto-dualsense4unix.service | grep bateria
```

**E a armadilha que quase custou a noite:** o `install` é editable, então **toda
cura de daemon só vale no próximo start**. O medidor ficou inerte por horas
porque o daemon vivo era anterior a ele. Ao retomar, conferir sempre:

```
systemctl --user show hefesto-dualsense4unix.service -p ExecMainStartTimestamp --value
```

---

## O que espera a palavra dela

Treze perguntas seguem abertas, e estão na seção 4 da
[ordem de execução](sprints/2026-08-07-INDICE-a-ordem-de-execucao-do-que-o-diagnostico-abriu.md),
com o texto pronto. As mais caras:

- **o desenho do ícone do painel** — três renderizados, esperando o olho dela;
- **a ordem da fila**: hoje é a ordem da *primeira vez* que cada controle
  apareceu; ela descreveu a ordem da *sessão*. Trocar revoga três decisões
  medidas de 25/07;
- **o backtrace do BlueZ** — exige gravar configuração global do kernel;
- **a auditoria de 26/06** — continua fora do `git`, e é onde a senha dela vazou.

---

## O que espera o hardware na mão dela

Ela já decidiu a ordem (resposta 9): **o protocolo de 06/08 vem primeiro**, com
41 medições. Depois dele, onze itens, e os três mais baratos:

| medição | custo | o que fecha |
|---|---|---|
| a régua de bateria do Pro | 5 min | ele **não** publica percentual, só cinco degraus — o amostrador leria o campo errado |
| o que o clique faz | 2 min | destrava a cura do "conecta e desliga" |
| o 8BitDo traduz a cor? | 30 s | decide se a numeração dele já funciona ou escreve no vazio |

---

## Os três defeitos vivos que ela sente

1. **O "conecta e desliga"** — a busca de serviços estoura o tempo na reconexão
   automática, e o clique dela força o caminho que completa. Sprint:
   [BUSCA-QUE-ESTOURA-01](sprints/2026-08-07-BUSCA-QUE-ESTOURA-01-o-sdp-que-nao-responde-a-tempo.md).
2. **O número trocado** — o controle que o jogo chama de Jogador 1 acende 4 no
   plástico, e o que ele chama de Jogador 2 acende 1. Os dois mentem, e mentem
   trocados. Sprint:
   [DUAS-CONTABILIDADES-01](sprints/2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md).
3. **O cabo no meio da partida** — trocar de transporte pode derrubar o jogador e
   recriá-lo, e o jogo vê um controle sumir. **Até isso ser curado: não plugar o
   cabo no controle do Jogador 2, 3 ou 4 no meio de uma partida que importe.**

---

## O que NÃO se deve fazer ao retomar

- **não reacender a luz dos externos** antes da cura da numeração;
- **não começar a adoção** antes das seis entregas da máscara;
- **não confiar em medição sem validar o instrumento** — ele enganou três vezes
  em 07/08, e duas viraram afirmação errada dita a ela;
- **não reiniciar o daemon com ela jogando** — derruba os controles;
- **não rodar agentes em paralelo na mesma árvore** sem separar os arquivos: foi
  o que contaminou 22 medições em 06/08 ([CLEAN-ROOM.md](CLEAN-ROOM.md)).

---

## O estado da árvore quando a máquina desligou

Branch `restauro/inicio-da-sessao`, **árvore limpa**, tudo commitado. A suíte
passa inteira, os nove portões da casa em zero, `mypy` limpo.

O que está **à frente do remoto** ainda não foi empurrado — é decisão dela
quando publicar.
