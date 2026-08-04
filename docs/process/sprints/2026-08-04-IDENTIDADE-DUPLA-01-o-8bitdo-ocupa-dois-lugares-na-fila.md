# IDENTIDADE-DUPLA-01 — o 8BitDo ocupa dois lugares na fila

- **Descoberta:** 04/08/2026, no journal da sessão de quatro controles dela
- **Gravidade:** média — explica a numeração que "dança" e come um slot de co-op
- **Estado:** aberta
- **Pré-requisito:** nenhum

> ### **MEDIÇÃO DELA (2 min)** — ligar o 8BitDo em cada modo e anotar o MAC.
>
> A E1 é essa medição, e **tudo abaixo dela é chute sem ela**. O que dá para fazer HOJE: a forense do journal (`grep -oE 'e417d8[0-9a-f]{6}'` na fila de externos) e o desenho do mapa de identidades irmãs.


---

## O que está medido

No mesmo boot, o daemon restaurou a fila de externos assim:

    external_fila_restaurada  ordem={'e0f6b5664653': 3,
                                     'e417d81c661a': 4,
                                     'e417d81c9983': 5}

Três MACs para **dois** controles físicos: o Pro Controller (`e0:f6:b5:…`) e o
8BitDo — que aparece **duas vezes**, com `…1c:66:1a` e `…1c:99:83`. O prefixo
`E4:17:D8` é o OUI da 8BitDo, já registrado nesta casa.

E os dois estão ativos: o journal tem escritas de LED para **ambos** no mesmo
período (23:49 → 00:01), em nós hidraw diferentes.

---

## A hipótese, e o que falta para confirmá-la

**Hipótese:** o 8BitDo apresenta um endereço Bluetooth **diferente por modo**.
Ela descreveu o gesto que muda o modo: *"dependendo da forma como eu ativo a
sincronização ele vira ou pro controler ou controle do ps4"*, e o combo do modo
PS4 na máquina dela é **`Start + A`** (medido — a documentação da casa registrava
`X+Start`, que **não** é o que ela usa).

Isso é consistente com o que a casa já sabe: no modo PS4 ele se apresenta como
`054c:05c4` e cai no `hid-playstation`; no modo Switch se apresenta como
Nintendo-class. Um firmware que troca de identidade **inteira** por modo trocaria
o MAC junto.

**Falta medir, e é uma medição de 2 minutos:** ligar o 8BitDo em cada modo e
anotar o MAC que aparece. Se cada modo tiver um MAC fixo e distinto, a hipótese
está confirmada e a cura abaixo se aplica. **Se os dois MACs aparecerem no mesmo
modo, a hipótese cai** e o que há é outra coisa — um bond fantasma de pareamento
antigo, que é defeito diferente e cura diferente.

---

## Por que isto dói

1. **A fila de externos numera por MAC.** Duas identidades = dois lugares. Com o
   Pro na 3, o 8BitDo ocupa a 4 **e** a 5 — e o quarto controle da mesa dela cai
   num slot que já devia estar livre. É candidato direto ao *"o 8bitdo entrou
   como player 1 igual o dualsense branco"* que ela reportou;
2. **a numeração muda quando ela troca de modo** — sem que nada tenha mudado
   fisicamente na mesa;
3. **o bond do modo que ela não está usando fica pendurado** no BlueZ, e a casa
   já mediu que reconexão entrante de device com bond sem trust é recusada como
   *unknown device* (o watchdog aplicou `Trusted=true` em `E4:17:D8:00:00:83`
   às 23:53:27 de 03/08, exatamente por isso).

---

## A cura

**E1. Medir primeiro** (acima). Sem isso, tudo abaixo é chute.

**E2. Se confirmado: a fila conhece "mesmo controle, outra cara".** Um mapa de
identidades irmãs, alimentado pela medição de E1 e pelo OUI + nome. O critério
não pode ser só o OUI — `E4:17:D8` cobre a linha inteira da 8BitDo, e ela pode
ter dois controles da marca; nem só o prefixo dos 4 primeiros octetos, que é
adivinhação sobre o esquema de endereçamento do fabricante.

**A regra que a sprint deve honrar:** duas identidades só são a mesma se **nunca
aparecerem conectadas ao mesmo tempo**. Isso é observável e barato de verificar,
e erra para o lado seguro — dois controles de verdade jamais são fundidos.

**E3. A tela diz a verdade.** Se o produto souber que são o mesmo controle, o
seletor mostra **um**. Se não souber, mostra dois — e nunca "um" por chute. Isto
conversa direto com a `NOME-HONESTO-01`.

**E4. O modo tem nome na tela.** Ela decide o modo por um gesto físico
(`Start + A`) e o produto hoje não lhe diz em qual modo o controle entrou. Como
o modo PS4 é o que funciona por Bluetooth nesta casa e o Switch é o que derruba,
o produto **sabe** o que recomendar — e cala.

---

## Aceite

1. o MAC de cada modo está **medido e escrito** neste documento;
2. com o 8BitDo num modo só, a fila de externos tem **um** lugar para ele;
3. trocar de modo **não** muda o número dos outros controles da mesa;
4. a tela nomeia o modo em que ele entrou, ou diz honestamente que não sabe;
5. teste que morde: dois MACs irmãos na fila, e a cura arrancada devolve dois
   lugares.

---

## Relacionado

- [QUATRO-NO-RADIO-01](2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md)
- [NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md)
- `docs/usage/troubleshooting-8bitdo.md` — a tabela de combos, corrigida em 03/08
