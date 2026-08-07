# SELO-VERDE-CEDO-DEMAIS-01 — o doctor afirmava o que só valia nesta bancada

- **Achado em:** 06/08/2026, por **verificação adversarial** sobre curas do
  próprio dia — nenhum destes defeitos veio de queixa dela
- **Estado:** **CURA APLICADA** nos três, com testes que mordem
- **Gravidade:** **ALTA** no primeiro (carimba VERDE um rádio ainda aberto),
  **MÉDIA** nos outros dois
- **Causa-raiz:** **MEDIDA** nos três — reprodução em bancada antes da cura
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
    — é a sprint que **manda** o `JustWorksRepairing=confirm`; esta é sobre o
    doctor **mentir** que a cura já chegou;
  - [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md)
    — a cura de lá **criou** o segundo defeito desta;
  - [CURA-QUE-FERE-01](2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md)
    — mesma lição noutra camada: a cura tem de provar o estado inteiro, não o
    estado em que ela foi escrita.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O que os três têm em comum

Nenhum destes é um erro de cálculo. Nos três, o doctor **afirmava**, sem
condição, uma coisa que era verdadeira **só no estado desta bancada** — e a
frase saía com selo de quem mediu.

É a classe de defeito mais cara que um diagnosticador tem, porque o dano não é
o defeito: é a pessoa **fechar o terminal achando que está tudo certo**.

---

## Defeito 1 — o `[ OK ]` saía antes de o daemon carregar a cura

**Gravidade: ALTA. Grau: MEDIDO.**

O `check_bluez_justworks_repairing` lia o `main.conf` **do disco** e, achando
`confirm`, imprimia:

```
[ OK ] JustWorksRepairing=confirm no main.conf — re-pareamento de quem já tem
       bond passa pelo agente (RADIO-ABERTO-01)
```

O problema é que o `bluez_config.sh` grava e **não reinicia o `bluetoothd` de
propósito** — reiniciar derrubaria os controles conectados na hora. Ele diz isso
por escrito, em duas linhas (`scripts/bluez_config.sh:988` e `:1056`):

> `JustWorksRepairing=... + FastConnectable=true garantidos — VALEM NO PRÓXIMO
> BOOT (ou restart natural do bluetoothd)`

Entre a cura e o próximo start, o **daemon vivo continua com `always`**. O rádio
segue aberto, e o doctor carimba verde.

E a ressalva **já existia no arquivo**: o irmão `FastConnectable` diz *"vale
desde o último start do bluetoothd"* desde sempre (`scripts/doctor.sh:1737` e
`:1739`). Faltava justamente na chave de **segurança**.

### A cura: medir os dois relógios em vez de ressalvar

Ressalvar todo mundo seria transformar o `[ OK ]` em ruído. Em vez disso o
doctor compara o `mtime` do `main.conf` com o `ActiveEnterTimestamp` do
`bluetooth.service`: se a config é **mais nova** que o start do daemon, o disco
ainda não é o que o daemon carregou, e sai um `[WARN]` nomeando o que falta.

`scripts/doctor.sh:1831-1867`.

Na máquina dela, em 06/08 às 22:18, a medição saiu assim — e **corretamente não
avisou**:

| | horário |
|---|---|
| `main.conf` escrito | 20:53:18 |
| `bluetoothd` no ar desde | 21:04:41 |

O daemon subiu **depois** da escrita, então ele já tem o valor novo.

**Mordida:** `tests/unit/test_doctor_justworks_comportamento.py`,
`TestOSeloVerdeNaoSaiAntesDoDaemonCarregar` — três testes que exercitam os dois
ramos por injeção (`HEFESTO_BT_ATIVO_DESDE`), porque o `systemctl` de mentira
da bancada não tem relógio.

---

## Defeito 2 — a cura do defeito 1 tinha o mesmo vício que curava

**Gravidade: ALTA. Grau: MEDIDO.**

Este é o mais instrutivo da leva, e foi achado **pela suíte**, não por um agente.

A primeira escrita da cura acima terminava assim:

```bash
_t_bluez="$(date -d "$(systemctl show bluetooth.service \
    -p ActiveEnterTimestamp --value 2>/dev/null)" +%s 2>/dev/null || echo 0)"
```

O `|| echo 0` parecia proteger o caso em que o systemd não responde. **Não
protegia nada**, porque não havia erro para capturar:

```
$ date -d "" +%s
1785985200      # = 06/08/2026 00:00, e rc=0
```

**O GNU `date` interpreta string vazia como meia-noite de hoje** (MEDIDO em
06/08/2026). Então em toda máquina onde o `bluetooth.service` não reporta
`ActiveEnterTimestamp` — serviço inativo, mascarado, container sem systemd — o
doctor comparava o `main.conf` contra **meia-noite**, e o aviso do defeito 1
saía **em falso** para qualquer arquivo tocado naquele dia.

Ou seja: a cura escrita para impedir uma afirmação sem medida **afirmava sem
medir**. E o sintoma na bancada foi exatamente esse: dois testes de linha de
base que esperavam `warns=0` passaram a ver `warns=1`.

### A cura da cura

Capturar a saída do `systemctl` **primeiro**, e só chamar o `date` se ela não
for vazia. `scripts/doctor.sh:1848-1862`.

**Mordida:** `test_sem_systemd_que_responda_o_aviso_se_cala` — devolvi o
`date -d` sem guarda e vi **quatro** testes ficarem vermelhos, inclusive as duas
linhas de base que o defeito havia derrubado.

---

## Defeito 3 — "os aparelhos do Hefesto não são afetados" era falso em três estados

**Gravidade: MÉDIA. Grau: MEDIDO.**

A cura do [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md)
terminava tranquilizando quem lê:

> *os aparelhos do Hefesto não são afetados: a `70-ps5-controller.rules` roda
> depois e os devolve a 0660+uaccess.*

Isso é verdade **só quando o culpado está numerado abaixo das nossas regras** —
que é o estado desta bancada (culpado em `60`, nós em `70`+). É **falso** em
três estados plausíveis, e o primeiro é o mais provável de todos:

1. **`99-hidraw-permissions.rules`** — a receita de internet mais copiada para
   hidraw roda **depois** de nós, e vence;
2. **`MODE:=`** — atribuição final, que regra nenhuma desfaz;
3. **a máquina sem as nossas regras instaladas** — que é exatamente a máquina em
   que alguém roda o doctor.

### A cura: a frase passa a ser medida

Só sai quando o menor número de regra nossa é maior que o do culpado **e**
nenhum culpado usa `:=`. Nos outros casos saem os ramos honestos: `ATENÇÃO: a
regra acima roda DEPOIS das do Hefesto`, ou `as regras do Hefesto NÃO estão
instaladas aqui`.

`scripts/doctor.sh:3002-3036`.

**Mordida:** devolvi a frase incondicional e vi
`test_o_texto_diz_o_que_esta_aberto_e_de_quem_e_o_arquivo` ficar vermelho.

---

## O achado de bancada: a janela de 2600 caracteres

**Grau: MEDIDO.**

Três testes do `test_acusa_o_culpado_01_*.py` liam a função assim:

```python
i = texto.index("check_perms_soft()")
corpo = texto[i : i + 2600]
```

A função tem **3581 bytes**. A janela cortava 981 — e tudo que entrasse no
**fim** ficava fora da medição. Duas consequências, e as duas são ruins:

- uma asserção `not in` passava **por não enxergar** (é o caso do
  `test_o_grau_continua_warn_e_nao_reprova_o_exit_code`, que jurava não haver
  `fail "` num pedaço que ele nem lia);
- uma asserção `in` reprovava **por corte**, sem nada ter quebrado.

Substituída por `_funcao_inteira()`, que extrai do cabeçalho à chave que fecha
na coluna 0 — o mesmo critério que o `test_doctor_justworks_comportamento.py` já
usava por `awk`.

---

## Nota datada — o que caducou

A asserção `assert "70-ps5-controller.rules" in corpo` cobrava a **afirmação**
que o defeito 3 provou enganosa. Ela não foi apagada: foi **substituída** por
asserções que cobram a **medição** (`_culpado_tardio`, o ramo de `ATENÇÃO`, o
ramo da máquina sem as regras), com a justificativa datada no docstring do
próprio teste.

## O que fica ABERTO

- **A cura do defeito 1 avisa, mas não age.** Ela diz que o rádio só fecha no
  próximo boot e oferece o `systemctl restart bluetooth` — que **derruba os
  controles conectados na hora**. Não há caminho que feche a janela de Just
  Works sem custo enquanto ela joga. **Grau: MEDIDO** (o custo), **SEM PROVA**
  (que não exista alternativa — ninguém procurou).
- **O defeito 3 não sabe ler `ENV{...}` nem `GOTO`.** Uma regra de terceiro que
  abra o hidraw por caminho indireto passa pela varredura. **Grau: SUSPEITA COM
  MECANISMO** — o caminho foi lido, o caso não foi construído.
