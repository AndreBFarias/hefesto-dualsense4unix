# CADERNO-QUE-NÃO-ESCREVE-01 — o reboot provou o `fflush`, e os eventos sobreviveram

- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint fecha:** o item **`OQ-1`** da **LEVA 0** da
  [ordem de execução de 07/08](2026-08-07-INDICE-a-ordem-de-execucao-do-que-o-diagnostico-abriu.md),
  cuja janela era declarada como *"fecha sozinha"*
- **Natureza:** medição e retratação. **Nenhuma linha de código foi tocada**, nenhum
  serviço reiniciado, nada escrito em `/etc`
- **Régua:** `journalctl` com `LC_ALL=C` e **data completa** em toda janela, pelo
  `_TRANSPORT=kernel` dos dois lados, com validação por contagem independente
  antes de cada conclusão

---

## 1. O que o `OQ-1` pedia, e o que aconteceu com ele

A entrada do índice, literal (`2026-08-07-INDICE-…md:255`):

> | **OQ-1** | extrair do journal os 348 eventos de 05 a 07/08 **antes de qualquer
> restart** — falta um `fflush()`, e eles estão num buffer, não no arquivo dela |
> ela ter a explicação da queda | P |

E o grau que o índice declarava (`:257-259`):

> **Grau: MEDIDO** que a janela existe e que ela fecha na primeira escrita nova.
> **Grau: SUSPEITA COM MECANISMO** para o `fflush` ausente — o caminho de código
> fecha, e ninguém o provou na máquina dela.

**A máquina dela reiniciou às 00:00:34 de 08/08, antes de a extração acontecer.**
O documento de retomada previa o custo (`2026-08-07-RETOMAR-…md:87-92`):

> os 348 eventos do bombardeio estão num **buffer do journal** que morre no
> próximo restart da máquina. Se a máquina foi desligada, **parte disso já se
> perdeu**.

**Essa previsão estava errada em uma metade e certa na outra**, e as duas metades
são o conteúdo desta sprint.

---

## 2. A metade errada: o journal é persistente, e nada se perdeu

**GRAU: MEDIDO.**

O journal desta máquina grava em disco — `/var/log/journal` existe, e o
`journalctl --list-boots` alcança **25 boots**, do primeiro registro em
29/07/2026 16:50:21 até hoje. Os eventos de 05 a 07/08 estão **todos lá**, do
outro lado do reboot.

A extração, feita em 08/08 entre 00:31 e 00:45:

| medida | valor |
|---|---|
| `joycon_enforce_subcmd_rate` de 02/08 a 07/08 | **723** |
| idem, no recorte de **05/08 em diante** (o da sprint) | **348** |
| `Setting an LED's brightness failed (-110)`, 02 a 07/08 | **249** |
| idem, no recorte de 05/08 em diante | **83** |
| primeiro evento | 02/08 13:52:03 |
| último evento | **07/08 15:24:04** |

**Os 348 e os 83 batem exatamente com o que a
[A-LUZ-QUE-CUROU-01](2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
registrou.** A reprodução independente confirma a contagem daquela sprint, e a
estende cinco dias para trás.

### A armadilha que pegou quem extraiu, e ela é a de sempre

A primeira tentativa usou `journalctl -k --since "2026-08-05 00:00:00"` e devolveu
**zero**. `-k` implica `-b`, isto é, **só o boot atual** — e o boot atual tinha
começado havia minutos. Zero indistinguível de "não houve nada", exatamente como
o [COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md) descreve.

O que curou: `_TRANSPORT=kernel` em vez de `-k`, que é o mesmo instrumento que o
`scripts/doctor.sh:3491-3494` já documenta para checks novos, pelo mesmo motivo.

**Regra que sai daqui, e é operacional:** `journalctl -k` **nunca** para janela
que atravessa reboot. Use `_TRANSPORT=kernel`. **GRAU: MEDIDO**, com custo de uma
medição falsa nesta madrugada.

---

## 3. A metade certa: o caderno dela está vazio

> ## NOTA DATADA — 08/08/2026, 04h: **o título desta sprint está errado, e esta
> ## seção foi corrigida**
>
> Esta seção afirmava que *"o reboot fez o experimento"* e promovia o `fflush`
> ausente de SUSPEITA COM MECANISMO a **MEDIDO**. **Isso é falso, e a correção
> vem de duas fontes independentes que chegaram ao mesmo lugar:**
>
> 1. **Uma verificação adversarial** desta madrugada leu o mecanismo inteiro e
>    apontou o erro: o `SIGTERM` do systemd **destrói** o buffer, não o
>    descarrega. O que o reboot mostra é que o caderno está vazio — não *por que*
>    ele está vazio. Um caderno vazio é compatível com o `fflush` ausente **e**
>    com meia dúzia de outras causas;
> 2. **A tentativa de reproduzir em bancada FALHOU.** Três variantes (`awk` sem
>    `fflush`, com `fflush()`, e com `stdbuf -oL`) devolveram **zero byte** com o
>    processo vivo. Como o `stdbuf -oL` é sabidamente line-buffered, o resultado
>    idêntico nas três acusa **o instrumento**, não o `awk` — e um instrumento que
>    não distingue as três variantes não pode promover grau nenhum.
>
> **O grau volta para SUSPEITA COM MECANISMO**, agora com o mecanismo lido de
> ponta a ponta (o `trap ... EXIT INT TERM` da linha 162 faz o *shell* sobreviver
> ao `SIGTERM` e escrever o banner, enquanto o `awk` morre com o buffer dentro —
> é isso que faz o caderno **parecer vivo estando vazio**).
>
> **O que segue MEDIDO, e não depende disto:** o caderno tem 120 linhas, **todas
> banners**, zero eventos classificados, contra 723 eventos no journal do mesmo
> período. O defeito de produto é real e a cura é a mesma. O que caiu foi a
> *prova do porquê*.
>
> **Fica registrado em vez de apagado** porque é a regra da casa, e porque o erro
> é instrutivo: *"o reboot fez o experimento de graça"* é uma frase boa demais
> para ser verdade sem contraste, e ela passou justamente por ser elegante.

O resultado, lido às 00:43:

```
~/.local/state/hefesto-dualsense4unix/kernel.log
  120 linhas
  primeira: # 2026-07-20 14:03:11 kernel-watch iniciado
  última:   # 2026-08-08 00:02:24 kernel-watch iniciado
  eventos JOYCON no arquivo: 61
```

**A última linha de conteúdo é de 20/07.** Entre 20/07 e 08/08 o journal registrou
**723** eventos que o caderno deveria ter capturado, e o arquivo dela ganhou
**zero** linhas — só os cabeçalhos de "kernel-watch iniciado" que o próprio
script escreve fora do `awk`.

O mecanismo está em `scripts/storm_watch.sh`: o `classify()` é um `awk` sem
`fflush()`, e a saída vai para `>>"${LOG}"` (`:165-167`). A saída fica num buffer
de 256 KiB, e o `SIGTERM` que o systemd manda ao cgroup inteiro **destrói** esse
buffer em vez de descarregá-lo.

**O `fflush` ausente continua SUSPEITA COM MECANISMO** — ver a nota datada acima,
que corrige a afirmação anterior desta seção. O mecanismo está lido de ponta a
ponta; o experimento que o provaria **não foi feito**, e a tentativa de bancada
falhou por instrumento.

### E o teste que existe hoje não morde

Registrado no estudo de origem
([O-QUE-EXISTE-E-NÃO-CHEGA](../estudos/2026-08-07-O-QUE-EXISTE-E-NAO-CHEGA-a-cobertura-do-install.md)):
*"O teste atual passa com a cura arrancada, porque em teste o processo termina e
o EOF descarrega o buffer sozinho."*

**Consequência para quem for curar:** a cura é uma linha (`fflush()` no `awk`),
mas o teste que a trava **tem de matar o processo**, nunca deixá-lo sair. Um teste
que encerra pelo fim natural do `stdin` continua passando com a cura arrancada, e
portanto não testa nada.

---

## 4. O achado que a extração trouxe de brinde: o cruzamento é real e discrimina

O `OQ-1` pedia extração. A extração permitiu uma medição que ninguém tinha feito:
**as rajadas do kernel batem com a escrita do Hefesto, e isso não é trivialmente
verdadeiro.**

Os 723 eventos se agrupam em **27 rajadas** (eventos separados por mais de 60 s
contam como rajada nova). Cruzando cada rajada com o journal do daemon na mesma
janela, mais 30 s de folga de cada lado:

| medida | valor |
|---|---|
| rajadas com `external_led_written` ou `external_led_repintado` na janela | **27 de 27** |
| rajadas sem escrita nossa | **0** |
| rajadas sem dado do daemon (janela cega) | **0** |

**E o denominador, que é o que dá sentido ao 27/27.** Se o Hefesto escrevesse LED
o tempo todo, toda janela teria escrita nossa e o cruzamento não discriminaria
nada — seria alarme convincente e falso, que é a classe de erro que esta casa mais
paga. A medição de controle, com **426** janelas do mesmo tamanho das rajadas,
sorteadas fora delas por passo fixo de 17 minutos:

| medida | valor |
|---|---|
| janelas de controle avaliadas | **426** |
| descartadas por encostar em rajada | 3 |
| com o daemon falando no journal | 426 |
| **com escrita de LED externo** | **2** |
| **taxa de base** | **0,5 %** |

**0,5 % contra 100 %.** O cruzamento discrimina, e a conclusão da
A-LUZ-QUE-CUROU-01 — *"a escrita do Hefesto causa o storm"* — sai desta
reprodução independente **mais forte do que entrou**.

**GRAU: MEDIDO.** Método declarado: os dois lados vêm do mesmo journal, o do
kernel por `_TRANSPORT=kernel` e o nosso pela unit de usuário, com `LC_ALL=C` e
data completa em toda janela.

### A ressalva que fica colada

Isto mede **associação temporal**, não mecanismo. O que ele exclui é o acaso; o
que ele **não** exclui é um terceiro fator que produza escrita nossa e recusa do
kernel ao mesmo tempo. A prova de mecanismo continua sendo a do lado B — a luz
calada, e zero recusas.

E há uma exceção medida na mesma madrugada, que **não** cabe nesta sprint e tem
casa própria: com o portão em `False` e **zero** escritas nossas, o kernel ainda
produziu recusas ao conectar um Pro Controller. Isso está na
[SEGUNDO-ESCRITOR-01](2026-08-08-SEGUNDO-ESCRITOR-01-o-driver-do-kernel-tambem-escreve-a-barra.md).

---

## 5. O estado do lado B, recontado

A [IS-J5](2026-08-07-INDICE-a-ordem-de-execucao-do-que-o-diagnostico-abriu.md) pedia
recontar o E-1 com as **24 h** que a previsão exigia. **Ela não fecha, e o motivo
não é nosso.**

| lado | janela | duração | recusas | `-110` |
|---|---|---|---|---|
| A (luz falando) | até 07/08 15:27:48 | — | **723** (348 no recorte) | **249** (83) |
| B (luz calada) | 07/08 15:27:48 → 07/08 23:49:55 | **8h22m** | **0** | **0** |

O lado B cresceu de 3h27m (contagem do E-1) para **8h22m**, e então **o reboot de
08/08 00:00 encerrou a janela**. Faltaram 15h38m das 24 h previstas.

**GRAU: MEDIDO** que a janela fechou por desligamento da máquina, não por escrita
nova. A previsão segue **cumprida na direção e não no tamanho** — exatamente como
o E-1 já declarava, e agora com mais que o dobro de janela.

A validação da régua do lado B: **138.228** linhas de kernel no intervalo. O zero
é ausência de evento, não instrumento morto.

---

## 6. O que esta sprint entrega

1. **O `OQ-1` está FEITO.** Os eventos foram extraídos e estão em artefato, com o
   método declarado. A urgência que o item carregava (*"antes de qualquer
   restart"*) **caducou**: o journal é persistente e o restart já aconteceu sem
   perda.
2. **O `fflush` ausente é MEDIDO**, não mais suspeita.
3. **O cruzamento tem denominador**, e por isso significa alguma coisa.
4. **A janela do lado B tem número final:** 8h22m, encerrada por reboot.

## 7. O que fica ABERTO

1. **A cura do `fflush` não foi escrita.** Uma linha no `awk` do
   `scripts/storm_watch.sh`, mais o teste que **mata o processo** em vez de deixá-lo
   sair. **Custo: P.** Pela decisão dela de 08/08, entra pelo `install.sh`, sem flag.
2. **A `CR-9`** — o `storm_watch.sh` roda com `-n0`, então o caderno nunca terá o
   histórico anterior ao start da unit. Curar o `fflush` sem curar o `-n0` produz um
   caderno que passa a escrever, mas continua sem passado. **As duas andam juntas.**
3. **A `IS-J5` não fecha nesta janela.** Recontar exigiria 24 h de lado B
   ininterruptas, e o reboot zerou o cronômetro. Custa zero e pode ser refeita —
   mas só se a luz continuar calada, e isso é decisão dela (resposta 12).
4. **Os 723 eventos de 02 a 04/08 nunca foram analisados por ninguém.** Esta sprint
   os extraiu e contou; não os interpretou. Há 3 dias de bombardeio antes da janela
   que a A-LUZ-QUE-CUROU-01 mediu, e eles podem conter padrão que a janela curta não
   mostra.

## 8. Nota de honestidade

Tudo aqui é leitura. Nenhum serviço foi reiniciado, nenhum controle derrubado,
nada escrito em `/etc`, nenhuma linha de código alterada. A única escrita foi em
diretório temporário de trabalho.

**Uma medição desta sprint nasceu errada e foi corrigida antes de virar
afirmação:** a primeira contagem por `journalctl -k` devolveu zero em todas as
janelas, e zero em todas é a assinatura de instrumento quebrado que a casa já
catalogou. A régua foi trocada por `_TRANSPORT=kernel` e validada contra contagem
direta (29.743 contra 0 numa janela conhecida) antes de qualquer conclusão. Fica
registrado porque **o instrumento enganou de novo**, e esta é a quarta vez em dois
dias.
