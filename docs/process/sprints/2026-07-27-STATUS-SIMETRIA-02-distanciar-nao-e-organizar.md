# STATUS-SIMETRIA-02 — distanciar não é organizar

- **Status:** **ENTREGUE — o teto elástico e a repartição da sobra entraram em
  `8d7fd45`** (conferido em 31/07: `STATUS-SIMETRIA-02` está citada em
  `app/widgets/controller_card.py` e em `gui/main.glade`; o aceite dos 200px de
  vão é cobrado por `test_status_faixa_blocos.py:251`, com
  `VAO_MAXIMO_ENTRE_BLOCOS = 200` em `:59`). **Duas heranças continuam abertas em
  outras sprints, e não aqui:** o miolo do frame Estado (E2 da
  [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md)) e os
  desenhos que não cresceram junto com o teto
  ([CARD-OCUPA-01](2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md),
  pedido dela em 31/07)
- **Prioridade:** ALTA — é a avaliação dela, de olho, sobre a entrega da
  STATUS-SIMETRIA-01
- **Aberta em:** 27/07/2026, 22h18, com a janela maximizada e um controle por
  Bluetooth
- **Sucede:** [STATUS-SIMETRIA-01](2026-07-26-STATUS-SIMETRIA-01-a-aba-que-era-pra-mexer.md),
  cujas entregas 2, 3 e 4 foram validadas (glifos legíveis, círculos alinhados,
  meio do card ocupado) — e cujo resultado ela reprovou como **incompleto**

## O veredito dela, literal

> *"só distanciou as coisas mas um nome dos analógicos tem 3 linhas outro dois.
> não tem a parte do som (acho que vem depois), o touchpad não tem um espaço
> próprio, os botões não tão bem distribuídos e tem vários espaços vazios."*

**A frase que resume, e ela é o título:** distanciar não é organizar. A entrega
anterior espalhou os módulos pela largura do card. Espalhar resolveu o
amontoamento e **não** produziu leitura.

## Os cinco defeitos, um a um

### 1. Os títulos dos analógicos quebram em número diferente de linhas

Medido na captura de 22h18:

```
Analogico       Analogico
Esquerdo        Direito (R3)
(L3)
   ^ 3 linhas       ^ 2 linhas
```

O `Gtk.SizeGroup` vertical da entrega 2 fez o que prometia: **os dois círculos
estão na mesma altura**. Mas ele iguala a *altura do bloco*, não o *número de
linhas do texto* — então o desenho está alinhado e a legenda não.

**A cura:** as duas legendas precisam ocupar a mesma quantidade de linhas por
construção. Duas saídas honestas:

- textos de comprimento equivalente (`Analógico esquerdo (L3)` /
  `Analógico direito (R3)` já são quase iguais — a quebra vem da largura
  disponível, não do texto);
- ou largura igual para as duas colunas, o que força a mesma quebra.

**O teste que morde tem de mudar:** hoje ele compara o Y dos círculos. Precisa
comparar também **o número de linhas renderizadas de cada legenda**. Trocar uma
palavra de rótulo tem de reprovar.

### 2. O touchpad não tem espaço próprio

Hoje `Touchpad`, o retângulo dele, `sem toque`, `Lightbar`, a barra de cor e
`#0000ff` são **seis elementos empilhados numa coluna única**, sem nenhuma
separação entre os dois assuntos. São duas coisas diferentes (uma superfície de
toque e uma luz) coladas como se fossem uma lista.

### 3. Os botões não estão bem distribuídos

O grid de dezesseis glifos está ancorado na ponta direita, e as quatro linhas
têm espaçamento próprio que não conversa com o resto do card. Ficou legível —
que era o pedido — e não ficou arrumado.

### 4. Vários espaços vazios

Medidos na captura maximizada:

| Onde | Aproximadamente |
|---|---|
| entre a coluna do touchpad e os analógicos | 700 px de nada |
| abaixo de todo o conteúdo do card | 90 px |
| entre o fim do card e o rodapé da janela | 100 px |

### 5. Falta o som

A entrega 1 da sprint anterior (microfone à direita dos analógicos) **não
aparece**, e a causa já está medida e escrita:
[MIC-PRESENTE-01](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md)
— `controller_card.py` chama `hide()` no bloco do microfone quando não há sinal,
e por Bluetooth não há sinal quase sempre.

Ela mesma anotou *"acho que vem depois"*, e vem: as duas sprints entram juntas,
porque o espaço do microfone muda a distribuição da faixa inteira.

## O que esta sprint propõe

**Parar de distribuir por espaçamento e passar a distribuir por grade.** Os
módulos da faixa deixam de ser uma fileira com folga entre eles e passam a
ocupar colunas de largura declarada, cada assunto com o seu bloco:

```
[ Touchpad ] [ Luz ] [ Analógico esquerdo ] [ Analógico direito ] [ Microfone ] [ Botões ]
```

Cada um com moldura própria ou separação visível, como o card do `Estado` já faz
no alto da aba. O vazio deixa de ser distância entre coisas e vira margem de
bloco.

## Como você valida

1. Os dois títulos de analógico ocupam **o mesmo número de linhas**.
2. O touchpad tem bloco próprio, separado da luz.
3. O microfone está lá, à direita dos analógicos — mesmo sem sinal.
4. Não há faixa de mais de 200 px sem nada entre dois módulos.
5. Aumentar a escala de fonte: nada se desalinha, nada quebra em linha a mais.
6. Nenhuma outra aba mudou.

## O que NÃO foi medido

- **Se a grade cabe na largura** com o microfone de volta. A medição da sprint
  anterior dizia que mic e glifo maiores somados consumiam quase toda a folga
  disponível — e era sem o tema aplicado. **Medir com o tema e a escala 3 antes
  de escrever código** é o item 0.
- **Como fica com dois cards lado a lado.** Toda a avaliação de hoje foi com um
  controle só.
