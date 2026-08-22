# MONITOR-QUE-VENCE-01 e QUEM-DÁ-O-JOGADOR-2-01 — a regra que não podia disparar, e o dono que ninguém declarava

- **Estado:** CONCLUÍDA nas duas Partes — a I em `scripts/fix_wireplumber_default_source.sh:87` (o drop-in `51-…`, invertido no commit `55e3c61`) com `tests/unit/test_monitor_que_vence_01.py`; a II em `app/actions/profiles_actions.py` e `app/actions/home_actions.py` (verificado em 21/08/2026)
- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint responde:** as duas frentes que ficaram abertas no
  [índice da madrugada](2026-08-08-INDICE-a-madrugada-em-que-o-produto-era-o-reu.md),
  e que ela mandou resolver *"de forma inteligente e definitiva"*
- **Grau:** **MEDIDO** nas duas causas; a cura do áudio está **provada ao vivo**

---

## PARTE I — O microfone que perdia para o próprio eco

### 1. O defeito, com os três números que o fecham

**GRAU: MEDIDO**, na máquina dela, com o drop-in instalado pelo `install.sh`:

| nó | `priority.session` |
|---|---|
| `alsa_output…DualSense…analog-surround-40.monitor` | **1109** |
| `alsa_input…DualSense…iec958-stereo` (a voz dela) | **50** |
| `alsa_input.pci-…analog-stereo` (a placa do PC) | 2009 |

**O monitor vencia o microfone por vinte e duas vezes.** A eleição de fonte
padrão entregava o **eco do que sai** no lugar da voz — e o `install.sh` criava
essa condição por default. A conferência final do próprio install denunciava, no
mesmo fôlego:

```
[FAIL] a fonte de captura padrão é um MONITOR — o que qualquer app gravar
       é o áudio de SAÍDA, não a voz
```

### 2. A cura de 30/07 existia, e não podia funcionar

O arquivo `51-hefesto-dualsense-no-default-source.conf` **já documentava este
defeito**. A `FONTE-PADRÃO-01` o tinha visto em 30/07 e acrescentado uma terceira
regra para rebaixar o monitor.

**A regra está escrita, está correta na intenção, e nunca dispara.** A prova é o
1109 intocado. E o mecanismo é estrutural, não erro de padrão:

> `monitor.alsa.rules` só alcança nós criados pelo **monitor de ALSA** do
> WirePlumber; o nó `.monitor` de uma saída não nasce dali — quem o deriva do
> sink é o próprio PipeWire. **A regra mira um nó que aquela camada não vê.**

**Isto é o achado de método da sprint:** uma cura pode estar escrita, revisada e
commitada, e mesmo assim ser **inerte por construção**. O que a expôs não foi ler
o código — foi medir o número que ela deveria ter mudado.

### 3. A cura definitiva: um invariante, não uma regra

Parar de depender de uma regra que não pode disparar. O que o produto precisa se
enuncia em uma linha:

> **um microfone de verdade nunca pode perder para um monitor.**

Monitor é laço de retorno do que sai. Ele nunca é a resposta certa para *"quem é
o microfone padrão?"* — não nesta máquina, não em nenhuma.

Então a entrada do controle passa a viver numa **faixa medida**:

```
   abaixo de qualquer captura real  →  2009 (a placa dela)
   acima de qualquer monitor        →  1109 (o mais alto desta máquina)
   ────────────────────────────────────────────────────────────
   valor escolhido: 1500, com folga dos dois lados
```

**O objetivo original do arquivo continua cumprido** — o controle **não** rouba o
posto de um microfone de verdade, que é a queixa que o criou — e o modo de falha
que ele introduziu **deixa de ser possível**.

A regra do monitor **fica**: não custa nada, documenta a intenção, e passa a valer
sozinha se alguma versão do WirePlumber estender o alcance da camada. O que muda é
que o produto deixou de **depender** dela.

### 4. Provado ao vivo, ponta a ponta

**GRAU: MEDIDO**, na máquina dela, em 08/08:

```
ANTES:   alsa_output…analog-surround-40.monitor    ← o eco
DEPOIS:  alsa_input…iec958-stereo                  ← o microfone
```

E o veredito do produto sobre si mesmo mudou de lado:

```
[FAIL] a fonte de captura padrão é um MONITOR
[ OK ] a fonte de captura padrão é uma entrada de verdade
```

**Por que o controle venceu a placa do PC (2009 > 1500):** porque não há nada
plugado na entrada da placa. Com um headset ligado lá, o headset volta a ganhar —
que é exatamente o comportamento desenhado.

### 5. O portão trava o invariante, não o número

`tests/unit/test_monitor_que_vence_01.py` afirma os **dois** lados, com os valores
medidos escritos como limites:

- a entrada **acima** de 1109 — arrancada a cura, reprova;
- a entrada **abaixo** de 2009 — o contrapeso, que impede a "cura" preguiçosa de
  pôr o controle no topo e reabrir a queixa original.

---

## PARTE II — O jogador 2 que trocava de dono em silêncio

### 6. A correção de uma afirmação minha

O índice desta madrugada dizia que **a caixinha contradiz a decisão dela**. **Está
errado, e a correção vem da medição que ela mesma fez.**

A `CONTROLE-SONY-MEDIDO-01` (06/08, seção *A INVERSÃO*, **grau MEDIDO**) fixou o
que acontece dentro da marca:

- o Hefesto **entrega a ENTRADA** — solta o grab, desfaz o esconde-esconde do
  hidraw e recolhe o gamepad virtual, **que é o que acaba com o controle dobrado**;
- e **mantém a SAÍDA inteira** — os gatilhos dela seguraram e a cor dela ficou.

E a decisão dela diz que *"permitir a allowlist faz o Hefesto continuar
funcionando"*. **As duas coisas casam.** O vpad é entrada, e ela concordou que a
entrada vai. **Não há contradição no mecanismo.**

### 7. O defeito real era o silêncio

O que a marca faz com **dois** controles:

```
coop_derrubado_pela_excecao_steam_input  secundarios_derrubados=1
```

Sete vezes em 08/08. **É o desenho funcionando** — são justamente esses vpads que
produziriam o controle dobrado. Mas muda **quem entrega o jogador 2**: passa a ser
o Steam Input, não nós.

**E nada dizia isso.** Com um controle, o texto antigo estava completo. Com dois,
ele omitia a troca — e a omissão custou a ela uma sessão inteira.

### 8. A cura: dizer o que muda, sem prometer o que não foi medido

O toast passa a conhecer a mesa. Com dois ou mais:

> *"Atenção: com 2 controles, quem passa a dar o jogador 2 é o Steam Input, não o
> Hefesto — confira na tela do jogo se os dois aparecem."*

E o caminho de volta também informa: tirar a marca avisa que **o co-op volta a ser
do Hefesto**.

**O que o texto NÃO promete, de propósito:** que o jogo vai ver dois jogadores.
**Ninguém mediu** se o Steam Input entrega os dois controles físicos ao jogo nesta
máquina. É **SEM PROVA**, e prometer numa caixinha seria pior que calar — ela
confiaria e não conferiria. O texto diz o que muda e manda conferir.

**Três coisas que a cura não podia quebrar, e que o portão trava:**

1. com **um** controle, o texto não muda — aviso irrelevante é ruído;
2. quando a contagem **não é legível**, cai no texto antigo. `None` e `0` são
   coisas diferentes: zero significaria *"não avise"*, e um palpite errado faria a
   caixinha calar justamente com dois na mesa. **Falha para o lado de dizer menos,
   nunca de dizer errado**;
3. a frase da **INVERSÃO** continua inteira. Acrescentar o aviso não podia custar
   a metade que a medição dela conquistou — que a cor e os gatilhos **continuam
   valendo** dentro da marca. É a metade que ela usa.

### 9. Onde a contagem vem, e por que não é uma consulta nova

O toast é **síncrono**; a ponte IPC da janela é assíncrona. Uma chamada nova ou
travaria a interface, ou chegaria depois do texto. A aba Início **já** busca o
estado a cada tique e já filtra os conectados — agora ela guarda a contagem, e a
aba Perfis lê dali. **Uma contagem só, num lugar só**, para as duas abas não
divergirem.

---

## 10. O que fica ABERTO

1. **A medição que fecha a Parte II:** com a marca ativa e dois DualSense, **o
   jogo vê dois jogadores?** Custa 10 minutos dela e é a única coisa que decide se
   a marca é utilizável em co-op. Se a resposta for **não**, o desenho volta à
   mesa — e aí sim haverá uma decisão de produto a tomar.
2. **A cura de áudio não sobreviveu a um ciclo de instalação nesta sprint.** O
   arquivo do repositório está curado e o teste o trava, mas o ciclo
   `uninstall`→`install` não foi repetido depois da mudança. **SUSPEITA COM
   MECANISMO** de que ele entra — o `install.sh` copia este arquivo, e é o mesmo
   caminho que instalou a versão anterior.
3. **A regra do monitor continua inerte.** Ela fica por intenção, mas nenhum
   mecanismo hoje rebaixa o `.monitor`. Se algum dia um monitor passar de 1500, o
   defeito volta — e o portão não pegaria, porque ele mede o arquivo, não a
   máquina. **A rede contra isso é o `doctor`**, que já verifica se a fonte padrão
   é um monitor.

## 11. Nota de honestidade

A cura do áudio foi **aplicada na máquina dela e medida**: o `wireplumber` foi
reiniciado (serviço de usuário, ~5 s, sem partida em curso) e o resultado está na
seção 4. A cura da caixinha é de código e **não** foi vista na tela — a
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
continua valendo, e a palavra final é dela.

**Uma afirmação minha foi corrigida aqui, não apagada** (seção 6): eu disse que a
caixinha contradizia a decisão dela. O mecanismo está certo desde 06/08; o que
faltava era o produto dizer o que faz. Fica registrado porque errar sobre uma
medição **dela** é o tipo de erro que a casa mais paga.
