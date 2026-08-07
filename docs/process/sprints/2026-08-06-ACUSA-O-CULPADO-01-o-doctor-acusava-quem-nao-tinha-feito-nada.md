# ACUSA-O-CULPADO-01 — o doctor acusava quem não tinha feito nada

- **Achado em:** 06/08/2026, entre 20h50 e 21h10, **na máquina dela**, no meio
  da medição de outra coisa
- **Estado:** **CURA APLICADA** e commitada em `53f6d8b`; esta sprint é a
  **materialização atrasada** — o código e os testes existiam desde 06/08, o
  documento não
- **Gravidade:** **MÉDIA** no efeito, **ALTA** no desperdício — a frase mandava
  procurar onde não estava
- **Causa-raiz:** **MEDIDA**, com o contraste no mesmo instante
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
    — a cura **desta** criou o segundo defeito **daquela**;
  - [RECEITA-ERRADA-01](2026-08-06-RECEITA-ERRADA-01-o-doctor-mandava-rodar-o-que-nao-resolvia.md)
    — mesmo turno, mesma classe: o doctor mandando fazer o que não resolve.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O sintoma

O doctor imprimia, quatro vezes seguidas:

```
[WARN] /dev/hidraw0 está 0666 (rw global) — provável ajuste manual;
       esperado é 0660+uaccess
```

**O ajuste manual não existia.** Ninguém tinha rodado `chmod` nenhum.

## A causa: uma linha, num arquivo de terceiro

```
/etc/udev/rules.d/60-openrgb.rules:10 -> KERNEL=="hidraw*", MODE="0666"
```

O OpenRGB instala uma regra que abre **todo** nó hidraw para o mundo, sem
estreitar por fabricante. **Grau: MEDIDO.**

## O contraste que prova a inocência do Hefesto

Medido no mesmo instante, e é o que fecha o caso:

| nó | modo | quem manda nele |
|---|---|---|
| hidraw0, 1, 4, 5 | `crw-rw-rw-` | ninguém (a regra de terceiro) |
| hidraw2, 3, 7 | `crw-rw----+` | regras do Hefesto, com ACL |
| hidraw6 (DualSense físico) | `crw-------` | exclusivo do daemon |

Nenhum `chmod` humano escolheria com precisão o **complemento exato** do
conjunto de regras do Hefesto, nem sobreviveria ao reboot.

## O que estava aberto, e por que importa

Os quatro nós abertos eram os receptores do **teclado** e do **mouse** dela. Por
`hidraw`, esses nós entregam os **relatórios de entrada crus** — e o bit de
leitura sozinho já basta: qualquer processo local podia ler o que estava sendo
digitado. **Grau: MEDIDO** (a classe do aparelho saiu de `ID_INPUT_KEYBOARD` /
`ID_INPUT_MOUSE` no udev).

## A cura, em quatro partes

`scripts/doctor.sh`, função `_udev_hidraw_rw_global` e `check_perms_soft`:

1. **Varre `/etc/udev/rules.d` e `/usr/lib/udev/rules.d`** e **nomeia**
   `arquivo:linha` da regra que abre todo hidraw sem estreitar;
2. **Agrega um aviso por causa**, não um por nó — quatro nós com a mesma origem
   viravam quatro avisos idênticos;
3. **Diz a classe do aparelho** (`teclado`/`mouse`), porque é isso que torna o
   aviso acionável;
4. **Amplia o casamento** do literal `666` para "qualquer bit a outros" — `0664`
   deixa qualquer processo **ler** o nó, e é a leitura que vaza a tecla. `0662`
   e `0646` tinham o mesmo buraco.

A frase *"provável ajuste manual"* não foi apagada: **mudou de ramo**. Ela
continua válida — mas só quando nenhuma regra explica o que se vê.

### Por que continua `[WARN]` e não `[FAIL]`

**Decisão medida, não esquecimento.** Só o `fail` alimenta `FAILS`, que é o
código de saída do doctor. Fazer a configuração de um programa de **terceiro**
reprovar o portão de saúde do Hefesto seria dizer "estou doente" por algo que
não é nosso. A gravidade foi para o **texto**.

## Os negativos que impedem o portão de virar ruído

Sem eles, a varredura acusaria meia `/usr/lib/udev/rules.d`:

- **regra estreitada por fabricante não é acusada** — `MODE="0666"` mirando UM
  aparelho é decisão de quem escreveu a regra (controle positivo real:
  `71-pdp-controllers.rules` desta máquina);
- **linha comentada não conta**, inclusive indentada;
- **modo sem bit para outros não conta**;
- **arquivo em `/etc` faz sombra no de `/usr/lib`** — é como o udev resolve. Sem
  isso, a correção que ela fez às 21:20 nunca apareceria como feita.

## O desfecho na máquina dela

MEDIDO em 06/08 às 21:20: o `60-openrgb.rules` foi corrigido para
`0660+uaccess`. O doctor saiu de **1 falha + 12 avisos** para **0 falhas + 10
avisos**, e os dois que saíram eram estes.

A nota datada de por que **não** se estreitou por VID/PID ficou no `zsh` dela:
não foi possível enumerar os aparelhos RGB, e estreitar às cegas quebraria o RGB
de algo que ninguém viu. Backup em `scratchpad/60-openrgb.rules.bak`.

## O que fica ABERTO

- **Estreitar a regra do OpenRGB por VID/PID**, uma linha por aparelho, quando o
  OpenRGB estiver no ar para enumerar. **Grau: SEM PROVA** de que a lista atual
  esteja completa — ninguém a leu.
- **A varredura não lê `ENV{...}` nem `GOTO`.** Regra de terceiro que abra o
  hidraw por caminho indireto passa batida. **Grau: SUSPEITA COM MECANISMO.**
