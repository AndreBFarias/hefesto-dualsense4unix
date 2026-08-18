# O dia dos cento e dezesseis agentes — índice de 06/08/2026

- **Escrito em:** 06/08/2026, na branch `restauro/inicio-da-sessao`, **depois de
  a sessão de trabalho ser morta por `SIGKILL` às 22h20** e reconstituída do
  disco (ver *"A sessão morreu, e nada se perdeu"*, abaixo)
- **Por que esta leva existe:** ela abriu o dia com uma pergunta, e a resposta
  honesta era **não**:

  > *"Hoje de madrugada e pela manhã fizemos várias pesquisas com os agentes,
  > tudo foi salvo?"*

  E fechou com outra, que reorganizou o trabalho inteiro:

  > *"faz tudo que for necessário pra não perdermos nada, materializa estudos
  > dos agentes no projeto, materializa o contexto todo da conversa"*

- **O que este índice é:** o ponto de entrada do **dia 06/08** — as curas que
  entraram, as medições que ela fez com o controle na mão, e a lista do que
  ficou **aberto e é dela**. Quem retomar lê este arquivo e depois a sprint que
  for executar.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, teste que reprova ou `git grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou. Este índice declara o seu em cada
seção, e **não herda** o grau das sprints que cita.

---

## A sessão morreu, e nada se perdeu

**Grau: MEDIDO** — a causa está na última linha do transcrito.

Às **22h20 de 06/08** a sessão de trabalho terminou sem aviso, no meio da suíte.
Da cadeira, parece que "fechou do nada". O registro diz outra coisa:

```
Exit code 137
```

`137 = 128 + 9`, ou seja **`SIGKILL`**. O processo foi morto; não houve fechamento.

Nada do trabalho estava só na memória:

| o que | onde ficou | quanto |
|---|---|---|
| conversa das duas sessões | `<sessão>.jsonl` | 11,7 MB |
| subagentes | `<sessão>/subagents/agent-*.jsonl` | **43**, ~30 MB |
| workflows | `<sessão>/workflows/wf_*.json`, com `result` inteiro | **10** |
| agentes dentro dos workflows | contados em `agentCount` | **73** |
| **total de agentes no dia** | | **116** |
| custo | somado de `totalTokens` | **9,7 milhões de tokens** |

**A lição, e ela é de método:** o que morre é o contexto, não o registro.
Recuperar é **ler o disco**, não relançar agente. Está anotado em
[COMO-OLHAR-A-TELA.md](../COMO-OLHAR-A-TELA.md) como a leitura obrigatória de
quem retoma.

---

## O que entrou, em cinco commits

| commit | o que |
|---|---|
| `0bb92a5` | o campo que não nascia, e as mensagens que não diziam o jogo |
| `ae32c10` | o Salvar para de mirar outro perfil; o co-op deixa de ser opção |
| `86c32ab` | **privacidade** — o repositório publicava o endereço de rádio dos controles dela |
| `53f6d8b` | **segurança** — a cura do Bluetooth chega à máquina, e o doctor para de acusar errado |
| `febe3e0` | o aviso que deixou a janela dela **morta** |
| `0b5a3a2` | o experimento dela derruba a doutrina da casa sobre a allowlist |

Fecharam com **7251 verdes**, `mypy` limpo e os nove portões da casa em zero.

---

## As três coisas que ELA derrubou

Este é o registro mais importante do dia, e não é sobre código.

### 1. A semântica da allowlist estava ao contrário — no código e na cabeça de quem escreveu

> *"esse modo do allowlist só usamos quando um jogo tem conexão nativa com
> dualsense (os controles aparecem dobrados lá, tanto xbox quanto sony, por
> conta do emulador). Não faz sentido ter um modo próprio."*

**Ela mediu com o controle na mão** e a medição derrubou a doutrina da casa.
Sprint: [CONTROLE-SONY-MEDIDO-01](2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md).
**Grau: MEDIDO por ela**, em 25 minutos, sobre uma pergunta que estava aberta
havia onze dias.

### 2. Os nomes propostos para a interface eram ruins, duas vezes seguidas

> *"horrível as sugestões. Tão tão confusas quanto antes."*

O que ficou registrado como regra: **partir do léxico que já existe na tela**.
Nome novo que não deriva do que há é sinal de conceito errado, não de falta de
criatividade.

### 3. A pergunta do amigo, que matou um desenho antes de ele custar trabalho

Ao perguntar como o Hefesto se comportaria com o controle de outra pessoa, ela
derrubou um desenho inteiro **antes** de ele virar código. Virou a
[REGRA-NAO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md):
a cura tem de ser **regra**, não registro — funcionar no primeiro boot de um
desconhecido, sem ninguém declarar nada.

---

## As sprints deste dia

### Curas aplicadas, com teste que morde

| sprint | o que fecha |
|---|---|
| [NUNCA-TROCA-O-ALVO-01](2026-08-06-NUNCA-TROCA-O-ALVO-01-a-janela-trocava-o-nome-e-o-salvar-ia-para-o-arquivo-errado.md) | o Salvar gravava noutro perfil |
| [DIALOGO-QUE-MATA-A-JANELA-01](2026-08-06-DIALOGO-QUE-MATA-A-JANELA-01-o-aviso-que-deixou-a-janela-dela-morta.md) | a janela dela ficou **morta**, sem clique, tecla ou "X" |
| [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md) | o doctor acusava ajuste manual que não existia |
| [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md) | o `[ OK ]` carimbava verde um rádio ainda aberto |
| [SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md) | o que ela gravava era o áudio de saída, não a voz |
| [RECEITA-ERRADA-01](2026-08-06-RECEITA-ERRADA-01-o-doctor-mandava-rodar-o-que-nao-resolvia.md) | o doctor apontava para um comando impotente |
| [BACKUP-QUE-SE-COME-01](2026-08-06-BACKUP-QUE-SE-COME-01-a-cura-do-bluetooth-destruia-o-proprio-backup.md) | a cópia de segurança se destruía sozinha |
| [CAMPO-QUE-NAO-NASCIA-01](2026-08-06-CAMPO-QUE-NAO-NASCIA-01-o-jogo-da-steam-sem-onde-digitar.md) | não havia onde digitar o jogo da Steam |
| [REGRA-NAO-SE-PERDE-01](2026-08-06-REGRA-NAO-SE-PERDE-01-o-rodape-gravava-por-fora-do-funil.md) | o rodapé gravava por fora do funil |
| [FEAT-COOP-DEFAULT-ON-01](2026-08-06-FEAT-COOP-DEFAULT-ON-01-o-co-op-deixa-de-ser-opcao.md) | o co-op deixa de ser opção — **decisão dela** |
| [RELOGIO-NAO-E-ASSERCAO-01](2026-08-06-RELOGIO-NAO-E-ASSERCAO-01-os-testes-que-mediam-a-maquina-em-vez-do-produto.md) | os testes mediam a máquina, não o produto |

### A materialização atrasada, e por que ela consta aqui

Sete das sprints acima (`ACUSA-O-CULPADO-01`, `SELO-VERDE-CEDO-DEMAIS-01`,
`RECEITA-ERRADA-01`, `BACKUP-QUE-SE-COME-01`, `CAMPO-QUE-NAO-NASCIA-01`,
`REGRA-NAO-SE-PERDE-01`, `RELOGIO-NAO-E-ASSERCAO-01`) documentam curas que **já
estavam no código e nos testes** desde 05 ou 06/08 — e que **nunca tiveram
página**.

Foram achadas por varredura: **21 códigos de sprint apareciam nas linhas
adicionadas pelos diffs de 05-06/08 e em nenhum arquivo de `docs/`**. A conta é
reprodutível — casar o padrão de código nas linhas `+` dos diffs desses dois dias
e subtrair o que já aparece em `docs/`. **Grau: MEDIDO.**

> **RESSALVA, e ela é do próprio método — 06/08/2026.** "Aparecer numa linha
> adicionada" **não** é o mesmo que "ter nascido ali". Ao escrever as sprints, a
> conferência por `git log -S` derrubou a datação de três casos:
> `FEAT-DSX-COOP-LOCAL-01` é de **27/06** (`e565334`), `FEAT-COOP-DEFAULT-ON-01`
> de **13/07** (`646cadf`), e os dois `BUG-INSTALL-MAIN-CONF-*` de **25/07**
> (`fc9a9f6`). O que 06/08 fez neles foi mexer no código que os cita.
>
> **A varredura continua válida para o que ela promete** — achar código sem
> documento —, e **inválida** para datar. Quem repetir a conta: use o
> `git log -S "<CÓDIGO>"` para a data, sempre.

E um achado de higiene: `CAMPO-QUE-NAO-NASCE-01` e `CAMPO-QUE-NAO-NASCIA-01` são
**o mesmo defeito com duas grafias** — mesmo mecanismo, mesma data, mesmo commit
(`0bb92a5`). Um código de sprint com duas grafias quebra toda busca futura.

**O débito não acabou:** a mesma varredura, sem o filtro de data, encontra **334
códigos** citados no produto e ausentes de toda a documentação. A maioria é
herança de auditorias antigas, cujos relatórios vivem em
`docs/process/audits/` — que o `.gitignore` **exclui do repositório**. Fechar
isso é uma leva própria, e está registrado aqui para não se perder de novo.

### Diagnóstico e desenho, esperando a palavra dela

| sprint | o que espera |
|---|---|
| [LUGAR-A-MESA-01](2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md) | as entregas `E3`/`E4` tocam o veto do `QUATRO-NO-RÁDIO-01` |
| [REGRA-NAO-REGISTRO-01](2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md) | a regra genérica da identidade dupla |
| [JOGOS-QUE-ELA-TEM-01](2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md) | escolher o jogo da biblioteca em vez de digitar o número |
| [CONTROLE-SONY-MEDIDO-01](2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md) | a doutrina nova, propagada aos documentos que a contradiziam |
| [APPLET-MONOCROMÁTICO-01](2026-08-07-APPLET-MONOCROMATICO-01-o-icone-que-destoa-do-painel.md) | **executada em 07/08**, menos duas escolhas dela: **qual desenho** (o aro com o martelo que ela propôs, ou a bigorna de 27/06) e **se o applet nativo volta à barra**. Falta também a prova de tela |

> **NOTA DATADA — 07/08/2026.** A `APPLET-MONOCROMÁTICO-01` nasceu **depois**
> deste índice, do olho dela na própria barra, e por isso não está em nenhuma
> das listas acima. Fica pendurada aqui, como manda a casa. O que ela mediu
> vale para quem mexer em ícone: **PNG nunca é recolorido pelo tema**, e
> contorno feito com `stroke` + `fill="none"` **vira um disco chapado** quando
> o GTK recolore — as duas coisas foram reproduzidas.

---

## Os estudos deste dia

Sprint responde *"o que fazer"*. Estudo guarda *"o que se aprendeu"* — e é o que
some primeiro quando a sessão morre.

| estudo | o que guarda |
|---|---|
| [A conversa inteira](../estudos/2026-08-06-a-conversa-inteira-o-dia-que-a-sessao-nao-guardou.md) | **o contexto**: a ordem das descobertas, as falas dela, e as três vezes em que ela derrubou uma conclusão |
| [O que só fecha com o controle na mão dela](../estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md) | a fila de medições que depende do hardware, com protocolo pronto |
| [O que só funciona na máquina dela](../estudos/2026-08-06-o-que-so-funciona-na-maquina-dela.md) | o que passa aqui e falharia no primeiro boot de outra pessoa |
| [O desenho da flag do jogo](../estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md) | a caixinha do Steam Input e o perfil a partir da biblioteca |
| [O sistema de perfis, por dezessete agentes](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md) | a leva da véspera, que abriu este dia |

**Leia o primeiro se você está retomando depois de uma interrupção** — ele
existe exatamente para isso.

---

## O que estava ABERTO — e foi RESPONDIDO em 07/08

> **NOTA DATADA — 07/08/2026.** As três perguntas abaixo foram levadas a ela num
> painel de nove decisões, depuradas de cem candidatas, e **as três foram
> respondidas**. O texto original fica de pé para quem reconstituir a ordem em
> que as coisas foram sabidas.
>
> - **`E3`/`E4` do `LUGAR-A-MESA-01`:** autorizadas, mas **só depois da
>   `MASCARA-01`**. Ela recusou o preço, não a entrega.
> - **A caixinha do Steam Input:** mora no editor do perfil, sob o jogo escolhido.
>   **Já está na tela** (commit `6b1cb62`).
> - **A fila de medições:** o protocolo de 06/08 vem antes do CHECKLIST de 25/07.
>
> As doze respostas estão em
> [as doze respostas dela](../2026-08-07-DECISOES-DELA-as-onze-respostas-do-painel.md),
> e o que elas viraram em código, em
> [o diário de execução](../2026-08-07-EXECUCAO-o-que-as-doze-decisoes-viraram.md).

## O que estava ABERTO, e era DELA

Nenhum destes andava sem a palavra dela. Estão aqui para ela ler de uma vez.

1. **`E3`/`E4` do `LUGAR-A-MESA-01`** — dar vpad próprio aos controles externos
   toca o veto do `QUATRO-NO-RÁDIO-01`. **Grau: o desenho é MEDIDO; a decisão é dela.**
2. **A caixinha do Steam Input** está destravada, com a semântica que só existe
   porque ela mediu. Falta ela dizer onde, na aba Perfis, a caixinha mora.
3. **A fila de medições com hardware na mão** — protocolo pronto, aguardando
   sessão. Ver [o que só fecha com o controle na mão dela](../estudos/2026-08-06-o-que-so-fecha-com-o-controle-na-mao-dela.md).

E uma que **ninguém sabe responder**, registrada sem promessa:

> **Ninguém, no Linux, diz ao jogo quem é o jogador N.** O jogo numera por ordem
> de enumeração — a luz pode dizer 2 enquanto o jogo diz 3, mesmo com o
> `LUGAR-A-MESA` inteiro pronto. **Grau: SEM PROVA** de que exista caminho; ninguém procurou.

---

## O erro de método do dia, e ele é de quem conduziu

**Grau: MEDIDO** — está em [CLEAN-ROOM.md](../CLEAN-ROOM.md) e na
[quarta rodada do BlueZ](../estudos/2026-08-06-o-que-so-funciona-na-maquina-dela.md).

Agentes rodando em paralelo **mutaram a mesma árvore** enquanto outro agente
fazia a medição do produto. O verificador estava medindo o produto de outra
pessoa, no meio do voo: **22 medições contaminadas**, e uma bancada acusada de
instável que **não era**.

A regra que ficou: **quem mede não divide árvore com quem muta.** Não é
preferência — foi medido.
