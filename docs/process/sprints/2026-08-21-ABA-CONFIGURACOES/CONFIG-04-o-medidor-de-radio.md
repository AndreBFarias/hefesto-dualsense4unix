# CONFIG-04 — o medidor de rádio

**Depende de:** CONFIG-03.

## O que entrega

A barra de ocupação: quanto do rádio de cada adaptador já está comprometido.

## A honestidade obrigatória

O número de **1.600 slots/s é derivado da especificação do Bluetooth Classic —
não foi medido nesta máquina.** O medidor tem de dizer isso na tela. O mockup já
carrega o selo `derivado da especificação`; ele não é decoração.

O que **é** medido, e vem do próprio projeto (`daemon/subsystems/bt_mic.py`,
A/B de 25/07/2026):

```
mic DESLIGADO : input 260.4 Hz   audio   0.0 Hz   total 260.4 Hz
mic LIGADO    : input 170.5 Hz   audio 106.2 Hz   total 276.7 Hz
```

## O risco que precisa estar escrito

Dois controles no **mesmo** adaptador diferiram por quase o dobro na mesma janela
(381,54 contra 191,40 Hz), e a desigualdade sobreviveu à troca de unidades.
`mapa-controles.csv` registra como **ABERTO**.

**Consequência de projeto:** o medidor pode dizer *"a mesa está cheia"* — que é
aritmética de especificação. Não pode dizer *"por isso seu controle está ruim"*,
porque a taxa varia por motivo desconhecido mesmo com a mesa folgada. A frase na
tela precisa respeitar essa fronteira.

**Aceite:** com um controle sem microfone, a barra mostra folga larga. Ligando o
microfone, a fatia de áudio aparece e a de entrada encolhe — e a soma quase não
se move, que é o comportamento medido.
