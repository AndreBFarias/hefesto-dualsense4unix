# Leva de 21/08/2026 — a aba Configurações

> **A frase que define o escopo**, dita ao abrir a leva:
>
> > "a ideia é deixarmos isso tudo configurável via gui. Pensei em perfis de
> > energia de uma forma geral pegando as features de cada aba também. aí escolha
> > entre economia, moderado e Hefesto (ultra) sei lá. **Não seja brega.**"
>
> E, sobre o plano: *"o seu plano tem que funcionar. Aí deve funcionar no
> ambiente cosmic e ambiente gnome."*

> **As cinco decisões de doutrina foram respondidas em 21/08/2026** —
> [`DECISOES-ABERTAS.md`](DECISOES-ABERTAS.md) guarda cada pergunta, a
> recomendação e a escolha. A leva está liberada, com as cinco seções.

---

## A tese

As dez abas de hoje operam sobre o que o produto **mede**. Quantos controles,
qual bateria, quantos hertz o giroscópio entrega, de que cor está a barra. Abra
qualquer uma delas e todo número na tela veio de um `hidraw`, de um `sysfs` ou
de um report do controle.

Existe uma classe inteira de informação que muda o comportamento do produto e
que **nenhuma dessas fontes carrega**:

- que aquele adaptador está na ponta de um cabo de três metros, dentro de um hub,
  em cima de um rack;
- que o receptor de 2,4 GHz na porta ao lado é do mouse, e não vai sair de lá;
- que hoje a prioridade é bateria durar a noite, não fidelidade;
- que aquele controle genérico é um 8BitDo ligado em modo XInput.

Nada disso é observável. Tudo isso é **declarável**.

**A aba Configurações é onde entra o que o produto não tem como medir e precisa
que a pessoa diga.**

### Para quem esta aba é

Para qualquer pessoa que use o Hefesto — não para uma mesa em particular. O caso
comum é **um adaptador, nenhum hub, nada declarado**, e nesse caso a aba tem de
parecer completa e correta, não vazia e cobrando. Quem tem mesa simples pode
nunca abrir esta aba na vida, e nada deixa de funcionar por isso.

A mesa grande — três adaptadores, hub, cabo, rádios concorrentes — é o caso raro
que a aba **suporta**, não o caso que ela **pressupõe**. O mockup mostra os dois,
nessa ordem, de propósito. É essa a linha que separa a aba nova das dez existentes, e
é ela que impede a aba de virar gaveta de tranqueira — o teste de admissão de
qualquer controle novo é uma pergunta só: *o Hefesto conseguiria descobrir isso
sozinho?* Se sim, o lugar não é aqui.

## As cinco seções

| # | Seção | O que ela resolve |
|---|---|---|
| 0 | **Está tudo certo?** | O exame que hoje só existe no terminal, com resposta em uma linha |
| 1 | **Os controles** | Um card por controle, com a borda na cor do plástico: quem é cada jogador, e o que os não-Sony não anunciam |
| 2 | **A mesa** | Onde cada adaptador está, quanto do rádio já está em uso, e quem mais disputa os 2,4 GHz |
| 3 | **Orçamento** | Um teto de recursos para a mesa inteira, agregando features das outras abas |
| 4 | **A janela** | Ajustes do programa: escala do texto, bandeja, ambiente de área de trabalho |

**O mockup mostra o estado final**, depois de todas as sprints — não o que dá
para fazer hoje. A diferença entre os dois está em
[`TODO-INTEGRACAO.md`](TODO-INTEGRACAO.md).

O desenho está em [`mockup/aba-configuracoes.html`](mockup/aba-configuracoes.html), e
o texto das dicas em [`TOOLTIPS.md`](TOOLTIPS.md).

### Densidade é requisito, não gosto

A primeira versão tinha parágrafo explicativo embaixo de cada seção e ocupava
2680px de altura. A atual tem **1729px** com a mesa cheia — cinco controles, dois
adaptadores e três rádios concorrentes — porque quase todo texto virou dica ao
passar o mouse. A regra que sobrou:

> Quem só quer escolher tem de conseguir escolher **sem passar o mouse em nada**.
> Se a opção não faz sentido sem a dica, o rótulo está errado — conserte o rótulo.

---

## O que o reconhecimento mudou neste plano

Uma varredura do repositório foi feita depois que o desenho ficou pronto. Três
achados mudaram o plano, e um mudou o mockup.

**`GtkComboBox` é proibido, e o motivo é o COSMIC.** O cosmic-comp rouba o foco
no clique e fecha o popup (cosmic-epoch#2497 / pop#3660). O projeto tem um
`SegmentedSelector` de 375 linhas que existe só para substituí-lo, e o uso de
combo no código é **zero**. O mockup nasceu com onze combos e foi corrigido —
com `wrap=True` o seletor monta grade de três colunas fixas, nunca `FlowBox`,
que mediu 606px de altura empilhada.

**Não existe lugar para configuração que não seja de perfil.** Há `profiles/`
(por perfil de jogo), alguns arquivos-flag, e nada global. Isso transforma
CONFIG-03 de "gravar campo" em "criar a camada de configuração de máquina" —
ver [D-A3](DECISOES-ABERTAS.md).

**Largura é o recurso escasso, não altura.** A rolagem horizontal é `NEVER`, então
o mínimo da página mais larga vira o mínimo da janela. A aba mais larga hoje é a
Lightbar, com 1110px para uma janela de 1180. Teto para a aba nova: ~1166px.

**E um número que eu tratava como medido é derivado.** Os 1.600 slots/s vêm da
especificação do Bluetooth Classic, não de medição nesta máquina. O medidor passa
a dizer isso na tela.

---

## Decisões, e por que cada uma

### D1 — Os perfis chamam Economia, Balanceado, Máximo e Auto

**Não** "Hefesto (ultra)". A aba Rumble já mostra hoje, na tela, exatamente
estes quatro rótulos:

```
[ Economia ]  [ Balanceado ]  [ Máximo ]  [ Auto ]
```

Inventar um segundo vocabulário para a mesma ideia — um em Rumble, outro em
Configurações — é dívida de interface: a pessoa aprende duas vezes e nunca sabe
se "moderado" e "balanceado" são a mesma coisa. Reusar custa zero e ensina uma
vez só.

Sobre batizar o nível máximo com o nome do produto: um seletor que diz *Hefesto*
não informa nada a quem está escolhendo — "máximo" informa. E o rótulo envelhece
mal, porque no dia em que o padrão mudar, o nome do produto vira sinônimo de
"a opção que gasta mais bateria". Quem pediu a leva já tinha marcado essa dúvida
com um *"sei lá"* e um *"não seja brega"*; isto é a resposta.

**Auto** não é enfeite: ele já existe em Rumble e tem regra clara aqui — controle
no cabo joga em Máximo, controle em rádio abaixo de 20 % de bateria cai para
Economia sozinho.

**O reconhecimento fortaleceu esta decisão de estética para compatibilidade:**
`RumbleConfig.policy` já grava exatamente esses valores, e o pydantic está com
`extra="forbid"`. Renomear não deixaria a interface feia — **quebraria os perfis
já gravados no disco dela**.

### D2 — O orçamento é teto, não troca

Escolher Economia **não desliga** a vibração. O jogo continua pedindo, a aba
Rumble continua mandando, e o valor chega ao controle limitado a 40 %. Nenhum
ajuste da pessoa é apagado, e voltar para Balanceado devolve tudo como estava.

A alternativa — perfil que sobrescreve os ajustes das abas — cria a pior falha
de confiança que uma interface pode ter: a pessoa configura, troca de perfil,
volta, e o que ela tinha feito sumiu. O produto já tem um lugar onde valores são
multiplicados sem serem destruídos, e é exatamente este, na aba Rumble:

> *"Intensidade global: multiplica a vibração que o JOGO pede — é aqui que se
> aumenta ou diminui a força sem tirar o controle dele."*

O orçamento é essa mesma ideia, estendida às outras features.

### D3 — A aba nova não rouba nenhum controle das existentes

Nada sai de Rumble, Lightbar, Gatilhos ou Sistema. A aba Configurações só
(a) acrescenta o que não existe em lugar nenhum e (b) agrega tetos por cima do
que já existe.

Dois motivos. O primeiro é que mover controle de aba quebra a memória muscular
de quem usa o produto todo dia e a documentação que aponta para eles. O segundo
é o risco: as dez abas somam 145 controles no cenário simples e 183 no cheio
(medido em [`docs/process/estudos/2026-07-27-inventario-de-botoes-da-janela.md`](../../estudos/2026-07-27-inventario-de-botoes-da-janela.md)) —
uma leva que mexesse nessa teia teria superfície de regressão grande demais para
o que entrega.

### D4 — A fita "Ajustes vão para:" fica inativa nesta aba

O cabeçalho da janela carrega um seletor de alvo — `Todos`, `Sony 1 · USB`,
`Sony 2 · BT` — que decide para qual controle vai o que você mexer.

**Tudo nesta aba é da mesa, não de um controle.** Hub, orçamento e ambiente de
área de trabalho não têm como valer "só para o Sony 2". Deixar a fita ativa e
ignorá-la em silêncio seria mentir para quem escolheu um alvo ali em cima.

Então a fita aparece esmaecida, com uma linha ao lado dizendo o motivo. A
exceção é a seção 4: um 8BitDo ligado em modo XInput é declaração **por
controle** — e é por isso que ela é feita de cards por aparelho, e não da fita.

### D5 — O nome "Configurações" fica

Foi o nome pedido, e ele cabe no conjunto: as abas de hoje se chamam Início,
Status, No jogo, Gatilhos, Lightbar, Rumble, Perfis, Sistema, Emulação,
Navegação. Nomes secos, de uma palavra. *Ambiente* descreveria melhor a tese,
mas seria a única aba com nome de conceito no meio de dez abas com nome de
coisa — perderia mais do que ganharia.

---

## O que ficou de fora, e por quê

| Ideia | Por que não entrou |
|---|---|
| Um segundo sistema de perfis | A aba Perfis já faz isso, com prioridade e "aplica a". São eixos diferentes: **Perfis** responde *quando*, **Orçamento** responde *quanto*. Dois sistemas com o mesmo nome seria o defeito, não a feature |
| Desligar rádios concorrentes pelo produto | O produto não tem esse direito. Desplugar o Wi-Fi de alguém para melhorar o próprio link é decisão da pessoa, não do programa. A aba informa; quem age é ela |
| Detectar hub sozinho | Tecnicamente possível pela topologia USB, mas insuficiente: um hub embutido no monitor e um hub em cima do rack são idênticos para o `sysfs` e opostos para o rádio. Onde a leitura acerta, ela pré-preenche; a palavra final é declarada |
| Assistente de primeira execução | Vale a pena, mas é outra leva. Esta entrega a aba; o passo a passo que usa a aba vem depois |
| `EXTERNAL_PLAYER_LED_ENABLED` de volta | A condição de retorno está fixada em `LUGAR-À-MESA-01` e não é "quando alguém achar que já dá". Fora de CONFIG-06 |

---

## Portabilidade — COSMIC e GNOME

O requisito é explícito, e a aba tem três pontos de contato com o ambiente:

1. **A janela.** GTK3 se comporta igual nos dois. O que difere é a escala HiDPI
   e o tamanho de tela — já tratado por [`d6b9396`](../../../../CHANGELOG.md)
   ("a janela nunca nasce maior do que a tela comporta"). A aba nova herda isso
   de graça **se** respeitar a rolagem vertical do notebook e não fixar altura.
2. **A bandeja.** `integrations/tray.py` usa AppIndicator, tentando
   `AyatanaAppIndicator3` e depois `AppIndicator3`. No COSMIC o ícone aparece
   sozinho; no GNOME moderno depende de extensão instalada. A seção 5 mostra o
   ambiente detectado justamente para o produto poder dizer *o que falta* em vez
   de sumir calado.
3. **O `SegmentedSelector` no lugar do combo.** É a defesa direta contra o
   cosmic-comp — e o motivo de o projeto não ter um único `GtkComboBox`.
4. **A leitura do ambiente.** `XDG_CURRENT_DESKTOP` é a fonte, e ela pode vir
   vazia ou composta (`pop:GNOME`). A regra é: exibir o que foi lido, permitir
   correção manual, e nunca condicionar funcionalidade a essa leitura — ela
   informa a mensagem de ajuda, não o comportamento.

**Portão de aceite da leva:** as capturas de `retratar_abas.py` saem iguais nos
dois ambientes, e a aba abre sem erro com `XDG_CURRENT_DESKTOP` vazia.

---

## As sprints

Cada uma entrega algo que funciona sozinho. A ordem é de dependência, não de
importância.

| ID | Título | Entrega | Depende de |
|---|---|---|---|
| **CONFIG-01** | A aba existe e está vazia | A 11ª aba no notebook, registrada, com as seções em branco e a fita de alvo inativa | — |
| **CONFIG-02** | O que a mesa já sabe dizer | Seções 1 e 2 em modo somente-leitura: adaptadores, rádios concorrentes, topologia USB | 01 |
| **CONFIG-03** | A declaração persiste | **Cria a camada de configuração de máquina** (`maquina.json`) — schema, disco e leitura no daemon | 02 |
| **CONFIG-04** | O medidor de rádio | O orçamento de slots calculado a partir do que está conectado e declarado | 03 |
| **CONFIG-05** | Orçamento como teto | Economia/Balanceado/Máximo/Auto aplicados como limite sobre as features existentes | 03 |
| **CONFIG-06** | Controles que não são DualSense | Declaração por aparelho para 8BitDo e Nintendo Pro, com as quatro medições como aceite | 03 |
| **CONFIG-07** | A janela | Seção 5: escala do texto, bandeja, ambiente — com o aceite COSMIC/GNOME | 01 |
| **CONFIG-09** | "Está tudo certo?" | O diagnóstico do `doctor.sh` com selo verde e seis linhas legíveis | 02 |
| **CONFIG-08** | A aba entra na documentação | `docs/usage/interface.md`, README e as capturas refeitas nos dois ambientes | 01–07 |

> **CONFIG-01 é o portão.** Enquanto a 11ª aba não abrir vazia sem quebrar as
> dez existentes, nenhuma das outras começa.

---

## Riscos

| Risco | Sinal de que aconteceu | O que fazer |
|---|---|---|
| A aba vira gaveta | Alguém propõe mover um controle de outra aba para cá | Aplicar o teste de admissão: se o produto consegue medir, não entra |
| Onze abas não cabem | A tira ganha rolagem horizontal em tela pequena | Medir com `retratar_abas.py` já em CONFIG-01, antes de haver conteúdo |
| O teto briga com a aba de origem | Rumble mostra 100 % e o controle vibra a 40 % | O valor efetivo precisa aparecer na aba de origem, não só aqui — resolver em CONFIG-05, não depois |
| A aba vira parágrafo de novo | Alguém acrescenta texto explicativo na tela | Texto novo entra como dica, não como `<p>`. Ver [TOOLTIPS.md](TOOLTIPS.md) |
| Declaração vira obrigação | A pessoa não preenche e algo para de funcionar | Todo campo nasce em "não sei", e "não sei" é resposta válida em todo lugar |
| O medidor promete diagnóstico que não sustenta | A tela diz "por isso seu controle está ruim" | Dois controles no mesmo dongle já diferiram 381 contra 191 Hz **com a mesa folgada**, e o motivo é ABERTO. O medidor fala de ocupação, nunca de culpa |
| A aba promete economia sem número | Aparece "poupa bateria em X %" | Não existe medição de mA nem de horas neste projeto. A tela diz a consequência verificável, não a promessa |


---

## Registro de decisões

| # | Pergunta | Escolha |
|---|---|---|
| D-A1 | O que fazer com o VETO 3 | Dar escopo: proibido declarar o que o produto **pode** medir |
| D-A2 | Seção 4 reabre escopo ditado | **Manter na leva agora** — contrária à recomendação, registrada |
| D-A3 | Onde mora config que não é de perfil | Criar `maquina.json` |
| D-A4 | Aba diferida ou viva | Diferida — nada vale antes do "Aplicar" |
| D-A5 | Agregar é mover ou espelhar | Espelhar com teto visível; dono único do valor efetivo |

Todas em 21/08/2026. O raciocínio de cada uma está em
[`DECISOES-ABERTAS.md`](DECISOES-ABERTAS.md).


---

## O que a revisão de interface mudou

Três rodadas de crítica sobre o desenho, mais uma auditoria de interface
independente, medida no navegador com a escala real da janela.

**Densidade.** 2680px → 1729px, e a mesa cheia passou de três para cinco
controles no caminho. Todo texto explicativo virou dica — o contrato está em
[`TOOLTIPS.md`](TOOLTIPS.md).

**Rosa no medidor era violação.** `theme.css:28` reserva `#ff79c6` para marca e
aba ativa. A faixa de microfone virou ciano, que é o que a casa usa para valor
numérico.

**Nada nasce respondido.** Nove de onze campos vinham com um palpite marcado,
contra a salvaguarda da própria D-A1. Hoje nascem vazios — e no seletor de
jogador, **campo vazio significa ordem de chegada**, que já é o padrão do
produto. Um botão a menos e uma doutrina cumprida.

**Duas perguntas de três estados saíram de checkbox.** Desmarcado dizia "não" e
"não sei" com o mesmo pixel. Viraram `Acima / Abaixo / Não sei`.

**A aba parou de perguntar o que o `sysfs` mede.** Hub e fonte própria são
detectáveis (`bDeviceClass == 09`) e viraram leitura. Sobrou declarado só o que
nenhum barramento sabe: altura da antena e linha de visada.

**Cards de altura igual.** Um controle 8BitDo pede mais campos que um DualSense,
e antes isso deixava os cards desencontrados. Agora o seletor de jogador ancora
no rodapé de todos.

**Cor escolhível.** Quando o Hefesto não lê a cor do plástico, o card oferece a
lista — Branco, Preto, Vermelho, Rosa, Roxo, Azul — com o nome oficial de fábrica
na dica de cada um.

### O que continua aberto

**A altura.** 1729px contra os ~654px que uma página de aba ocupa nesta casa. O
corte que resta é estrutural, não cosmético: **"Os controles" talvez pertença ao
cabeçalho da janela**, onde `ONDE-A-COR-MORA-01` já desenhou os chips coloridos —
e não a esta aba.

**A borda colorida por item do segmentado não é construível hoje**, e por três
motivos reais: o `SegmentedSelector` recebe `(id, label)` e a forma da tupla está
travada por três arquivos de teste; não existe um único `CssProvider` por widget
em todo o `app/`; e o jogador 4 é rosa na paleta de lightbar, o que colide com a
regra do rosa. O terceiro precisa de decisão antes de qualquer implementação.
