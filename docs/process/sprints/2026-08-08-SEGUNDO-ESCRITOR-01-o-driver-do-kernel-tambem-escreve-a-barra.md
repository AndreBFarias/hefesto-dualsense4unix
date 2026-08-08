# SEGUNDO-ESCRITOR-01 — o driver do kernel também escreve a barra, e a previsão do E-1 disparou

- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint responde:** a linha que a
  [A-LUZ-QUE-CUROU-01](2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md)
  deixou escrita como condição de falsificação, e que **disparou**
- **Natureza:** diagnóstico. **Nenhuma linha de código tocada**, nenhum serviço
  reiniciado, nada escrito em `hidraw`
- **Régua:** `journalctl _TRANSPORT=kernel` e o journal da unit de usuário, com
  `LC_ALL=C` e data completa, no boot de 08/08/2026

---

## 1. A previsão, e o que ela mandava fazer

O experimento **E-1** do
[estudo ISOLAR](../estudos/2026-08-07-ISOLAR-os-externos-o-metodo-da-lightbar-no-pro-e-no-8bitdo.md)
escreveu a previsão em forma falsificável, e escreveu também o que fazer se ela
falhasse:

> **PREVISÃO, derivada do código.** Com o LED calado: **zero**
> `joycon_enforce_subcmd_rate` e **zero** `-110` numa janela de 24 h com o Pro
> ligado, e **zero** instâncias HID novas do Pro. **Se aparecer uma única linha de
> `joycon_enforce_subcmd_rate` com o gate `False`, existe um segundo escritor** —
> e achar quem é passa a ser o alvo, porque o produto não é o único a mexer nessa
> barra.

E o índice de execução carregou isso como regra de operação (`:167-168`):

> **Uma linha de `joycon_enforce_subcmd_rate` com o portão em `False` significa um
> segundo escritor** — e achar quem é passa à frente de tudo.

**A linha apareceu. Três delas.** Esta sprint diz quem é.

---

## 2. O que foi medido

**GRAU: MEDIDO.** Boot de 08/08/2026, iniciado às 00:00:34.

### As condições da medição

| condição | valor | como se sabe |
|---|---|---|
| portão da luz | `EXTERNAL_PLAYER_LED_ENABLED = False` | `daemon/subsystems/external_identity.py:194` |
| escritas nossas em externo no boot inteiro | **0** | `grep -c 'external_led_written\|external_led_repintado'` na unit de usuário |
| daemon vivo desde | 08/08 00:02:23 | `systemctl --user show -p ExecMainStartTimestamp` |

### O que o kernel registrou

```
00:24:38  nintendo 0005:057E:2009.000A: assigned player 1 led pattern
00:24:39  nintendo 0005:057E:2009.000A: joycon_enforce_subcmd_rate: exceeded max attempts

00:51:46  nintendo 0005:057E:2009.000D: assigned player 1 led pattern
00:51:47  nintendo 0005:057E:2009.000D: joycon_enforce_subcmd_rate: exceeded max attempts
00:51:48  nintendo 0005:057E:2009.000D: joycon_enforce_subcmd_rate: exceeded max attempts
```

**Duas ocorrências independentes, mesmo padrão, com 27 minutos de intervalo:**
o driver `hid-nintendo` anuncia que **atribuiu o padrão de player LED**, e um a dois
segundos depois o firmware recusa subcomando.

**Nenhuma escrita nossa em nenhum dos dois instantes.** O portão estava fechado, e a
função que ele guarda não foi chamada uma vez sequer no boot.

---

## 3. Quem é o segundo escritor

**É o próprio driver do kernel, no `probe` do aparelho.**

`assigned player N led pattern` é mensagem do `hid-nintendo`, emitida quando ele
registra o controle e **escreve o padrão de jogador** — parte normal do `probe`,
sem participação nenhuma do espaço de usuário. É escrita de LED por subcomando,
exatamente da mesma natureza que a nossa, feita pelo mesmo caminho que o firmware
recusa quando está sob pressão.

**GRAU: MEDIDO** que a mensagem é do driver e precede a recusa nas duas ocorrências.
**GRAU: SUSPEITA COM MECANISMO** que a escrita do driver **causa** a recusa: o
caminho fecha e a ordem temporal é consistente nas duas, mas duas ocorrências não
são lei, e não houve braço de contraste.

---

## 4. O que isto NÃO derruba, e a diferença que importa

**A A-LUZ-QUE-CUROU-01 continua de pé, inteira.** Esta sprint não a contradiz —
completa-a. E a diferença entre os dois escritores é de **ordem de grandeza**:

| escritor | quando escreve | custo medido por episódio |
|---|---|---|
| **Hefesto** (lado A, luz falando) | a cada tique de identidade, e a cada repintura | rajadas de **20 a 77** recusas; **19,3** recusas por `external_led_written` |
| **`hid-nintendo`** (probe) | **uma vez por conexão** | **1 a 2** recusas |

O bombardeio que matava o Pro era nosso: **348** recusas em 19 h de lado A, contra
**3** em todo o boot de 08/08 com o portão fechado — e essas três distribuídas em
duas conexões.

**A conclusão da sprint-mãe — a escrita do Hefesto causa o storm — sai desta
medição intacta.** O que muda é que *"zero recusas com o portão fechado"* deixa de
ser o critério: o piso não é zero, é **uma a duas por conexão de externo**.

---

## 5. O que isto muda na fila

### Para a `IS-J5` e para qualquer recontagem do lado B

O critério de sucesso escrito na previsão — **zero** — é **inatingível enquanto
houver conexão de externo na janela**, e não porque alguma cura falhou.

**A previsão precisa de nota datada**, e o critério novo é:

> zero recusas **fora dos instantes de `probe`**; dentro deles, uma a duas por
> conexão, coladas ao `assigned player led pattern`.

Sem essa correção, toda recontagem futura do lado B vai parecer refutada por um
efeito que não é nosso. **GRAU: MEDIDO** que o critério antigo não é atingível;
**a nota datada é a entrega desta sprint para a IS-J5.**

### Para a leva 9 (a escrita idempotente) e para a volta da luz

Três consequências, e nenhuma delas afrouxa a decisão 12 dela:

1. **A idempotência continua sendo pré-requisito, e ganha um motivo a mais.** Se o
   driver já gasta o orçamento de subcomando do firmware no `probe`, a nossa
   primeira escrita depois de uma conexão chega num aparelho que **acabou de
   recusar**. A escrita diferencial (`S4`) importa mais, não menos.
2. **A precedência de LED tem um dono que ninguém tinha contado.** A leva 9 previa
   *"dois escritores"* — nós e a `E3`. São **três**: nós, a `E3`, e o kernel no
   `probe`. Qualquer precedência declarada tem de dizer o que fazer com o padrão
   que o driver escreveu sozinho.
3. **O detector (`S3`) precisa saber disto.** Um detector que compare o estado do
   aparelho contra *"o que nós escrevemos"* vai encontrar, logo após cada conexão,
   um padrão que **nós não escrevemos** — o do driver. Se ele tratar divergência
   como "alguém mexeu, repinta", ele repinta a cada conexão de externo, **de
   graça**. Isto é a semente do laço infinito que a trava da A-LUZ-QUE-CUROU-01
   existe para evitar.

### Para a trava "nenhuma cura de luz antes da cura da numeração"

**Nada muda.** A trava é dela e continua valendo. Esta sprint não reacende lúmen
nenhum: ela mede o que o kernel faz sozinho, com o produto calado.

---

## 6. O que fica ABERTO

1. **A causalidade não está provada.** Duas ocorrências, sem braço de contraste.
   O experimento que fecharia: conectar o Pro **N vezes** e contar recusas por
   conexão, com o portão em `False`. Custa dois minutos **dela** (ligar e desligar
   o controle três vezes) e é a única coisa desta sprint que não fecha sozinha.
   Fica registrado como medição pendente de hardware na mão dela.
2. **Não se sabe se o número recusado importa.** O driver escreveu *"player 1"* nos
   dois casos. Se ele escreve sempre o mesmo padrão, o custo é fixo por conexão; se
   varia com a mesa, o custo varia junto — e isso interage com a numeração.
3. **O 8BitDo não entrou nesta medição.** Ele não passa pelo `hid-nintendo` em modo
   PS4 (é `054C:05C4`, do `hid-playstation`), então o efeito medido aqui **não se
   aplica a ele** — e o que acontece com ele em modo Switch continua sem prova.
4. **A nota datada na previsão do E-1 não foi escrita** no arquivo de origem. Esta
   sprint a declara; colá-la lá é trabalho de documentação, custo P.

## 7. Nota de honestidade

Leitura pura. Nenhum serviço reiniciado, nenhum controle derrubado, nenhuma escrita
em `hidraw`, nenhuma linha de código alterada. As conexões de Pro Controller que
produziram as duas ocorrências foram feitas **por ela**, no uso normal da máquina,
sem pedido nosso — o que é bom para a medição, porque nada foi encenado.

**O que esta sprint não faz:** não propõe reacender luz nenhuma, não afrouxa a
trava da numeração, e não reabre a decisão 12.
