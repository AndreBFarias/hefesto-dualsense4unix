# NOME-HONESTO-01 — a tela chama de Sony o que o kernel já sabe que não é

- **Status:** PROPOSTA, escrita em 03/08/2026
- **Prioridade:** MÉDIA — não quebra nada, e é o tipo de defeito que ela encontra
  toda vez que abre a janela
- **Faixa:** 2 — o produto exibe informação que ele tem como distinguir
- **Causa-raiz:** **PROVADA no código**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Roteiro:** [PEDIDOS-DELA-01](2026-08-03-PEDIDOS-DELA-01-o-roteiro-dos-seis-pedidos-da-interface.md),
  pedido 4
- **Por que sprint NOVA:** `grep` por `friendly_type|brand_of|external_controllers.py`
  em `docs/process/sprints/*.md` devolve **zero** — nenhuma sprint é dona desta
  superfície. **A `IDENT-01` não é a dona:** "apelido" ali significa *vincular
  dois endereços*, não nome legível

---

## O pedido dela

> *"aqui deveria ser reconhecido o controle do 8bitdo pra ser reconhecido como
> pro controler ou PS4 e **o nome do controle deveria ser 8bitdo e não sony**."*

O diálogo do Controle 4 mostra hoje:

```
Controle:         Sony
Nome do sistema:  Sony Computer Entertainment Wireless Controller
```

O aparelho é um **8BitDo em modo DirectInput/PS4**, que se apresenta como
`054c:05c4` — a identidade de um DualShock 4.

## O que o projeto já sabe, e não usa

O caminho **Bluetooth** já acerta: `_BRAND_BY_OUI`
(`app/actions/external_controllers.py:64`) reconhece o OUI **`E4:17:D8`** e diz
**"8BitDo"**. É o **caminho USB** que erra, porque ali não há OUI para consultar.

**Mas há outro sinal, e ele já existe no código:** o clone **não devolve
endereço** no feature report, e o kernel sintetiza um —
`core/evdev_reader.py:284` (`_is_synthetic_uniq`), função **pura**, sem `evdev`
no topo. Medido nesta máquina em 03/08:

```
uniq = 02:05:4c:00:00:03      <- sintetizado pelo kernel (ds4_synthetic_mac)
```

Um DualShock 4 **genuíno** devolve o MAC real.

---

## As entregas

### E1 — o degrau do endereço sintético

**Onde:** `app/actions/external_controllers.py:88-105` (`friendly_type`) e
`:108-121` (`brand_of`).

**A posição importa: ACIMA do VID e ABAIXO do OUI.** Assim o caminho BT — que já
diz "8BitDo" — sai **byte a byte idêntico**, e só o caminho USB muda.

**A conversão hex→int nasce em `core/`:** `external_controllers.py:18-25` recusa
**por escrito** importar módulo do daemon. Respeite.

### E2 — o rótulo não pode ultrapassar o sinal

Esta é a entrega que separa a cura honesta da mentira nova.

**O que o sinal prova:** *"este firmware não devolveu endereço no report"*.
**O que ele NÃO prova:** a marca.

| rótulo | veredito |
|---|---|
| `"Compatível PS4"` | **sobrevive** — é o que o sinal sustenta |
| `"PS4 (não-Sony)"` | **não** — afirma origem |
| qualquer marca no cabo | **não** |

**E `hardware_version == 0x00000000` não serve como segundo sinal:** não há
DualShock 4 genuíno nesta casa para calibrar, e o `0x00000711` que circulou como
fixture de DS4 é, na verdade, **valor de DualSense**.

### E3 — a simetria obrigatória (senão conserta uma mentira e deixa a gêmea)

O degrau é genérico em VID/PID, e isso tem duas consequências que a entrega
**tem de resolver**:

1. **o Pro Controller genuíno degradado no cabo** cai no mesmo `uniq` sintético
   (`daemon/subsystems/external_identity.py:298`) e **não pode deixar de ser
   "Nintendo"** — e `brand_of` **não tem** o degrau `_TYPE_BY_VIDPID` que
   protege o `friendly_type` (`:95-96`);
2. **o inverso:** um 8BitDo em **modo Switch no cabo** continua sendo exibido
   como "Pro Controller" por `_TYPE_BY_VIDPID:27`.

**A sprint tem de dizer o que faz com essa assimetria.**

### E4 — a ficha do modo PS4 deixa de ser muda

`input_mode:230` devolve `"outro"` para `054c:05c4`, e por isso
`mode_selector_state:269` e `mode_guidance:284` devolvem `None`: **o Controle 4
não tem linha de modo nenhuma** no diálogo.

Ganha o terceiro modo **como rótulo, não como segmentado de três** — porque o
`MODE_SELECTOR_TOOLTIP` (`:263-266`) afirma *"combo ao ligar"*, e um DualShock 4
genuíno **não tem combo**.

### E5 — o Pro genuíno para de receber um seletor de dois modos

Quando o aparelho é um Pro Controller de verdade, oferecer "Nintendo (Switch) /
Xbox (X-input)" promete uma troca que **não é do software** — é combo físico no
controle.

---

## O aceite

Com o 8BitDo no cabo, em modo PS4, o diálogo diz:

```
Controle:         Compatível PS4          (não "Sony")
Marca:            8BitDo                   (quando o sinal sustentar)
Modo:             DirectInput/PS4          (hoje: linha ausente)
```

E com um Pro Controller genuíno no cabo, **nada muda** — continua "Nintendo".

## Testes que vão reprovar

```
pytest tests/unit -k "external or friendly or brand or identity"
```

## O que NÃO fazer

- **não afirmar marca a partir do endereço sintético** — o sinal prova ausência
  de endereço, não origem;
- **não usar `hardware_version` como segundo sinal** sem um DS4 genuíno para
  calibrar;
- **não importar módulo do daemon** em `external_controllers.py` — a recusa está
  escrita em `:18-25`;
- **não consertar `friendly_type` e esquecer `brand_of`** — é a assimetria da E3;
- **não oferecer seletor de modo ao Pro genuíno** — a troca é física.

## O que fica ABERTO

- **o combo do modo PS4 do 8BitDo** não está no repositório e **não se inventa**
  — é gesto dela, e vale documentar quando ela disser qual é;
- **distinguir 8BitDo de outros clones** que também sintetizem endereço: o sinal
  atual só separa *"clone"* de *"genuíno"*, não *"qual clone"*.
