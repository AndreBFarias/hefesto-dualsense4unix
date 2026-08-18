# BOTÃO-QUE-NÃO-MENTE-01 — "clico e não acontece nada"

- **Status:** **PARCIAL — a E2 está ENTREGUE EM CÓDIGO, AGUARDANDO A PALAVRA
  DELA; as E5 e E6 seguem ABERTAS.** Remarcada em 09/08/2026. A exceção do
  Steam Input passou a decidir quem entrega o controle em `e96dea8`
  (27/07/2026). **Rótulo anterior: ABERTA**, preservado aqui. Ver a nota datada
  no fim
- **O que falta ela validar, em uma linha (só da E2):** abrir a lista de jogos
  da exceção do Steam Input, clicar no "Desfazer" de um deles e ver o jogo sair
  da lista — sem terminal e sem ir na Steam
- **Prioridade:** ALTA — é a queixa de uso mais ampla já registrada, e a primeira
  cuja causa foi medida botão por botão
- **Aberta em:** 26/07/2026
- **Escopo:** a janela inteira. É a sprint de qualidade de uso da leva

## O relato dela

> *"sinto às vezes que os botões são mockup puro e não funcionam ou estão
> confusos demais ou muito complexos"*

## O veredito, nas duas direções

A frase tem duas afirmações. A medição confirma uma e refuta a outra, e as duas
respostas importam.

**"Mockup puro / não funcionam" — REFUTADO para a esmagadora maioria.**

```
66 handlers declarados no glade
66 existem no dict de sinais de app/app.py:247-349
66 têm def em app/
 0 com corpo vazio (pass/return/docstring)
 0 handlers órfãos
 0 botões que nascem cinza e nunca ligam
```

A cola entre a janela e o código está **fechada**. Isso foi trabalho de alguém, e
está registrado (`BUG-GUI-EMULATION-HANDLERS-UNWIRED-01`). Ela não está olhando
para uma maquete.

**"Confusos demais / muito complexos" — CONFIRMADO, com número.**

```
145 controles acionáveis na tela   (cenário simples: 1 controle, gatilhos desligados)
183 no cenário cheio               (2 gatilhos em "vibração por posição", 4 controles)
  6 botões dizem "Aplicar" alguma coisa
  6 dizem "Desligar/Apagar/Parar"
  2 dizem "Salvar" — com semânticas diferentes, visíveis ao mesmo tempo
 48 dos 85 widgets do glade NÃO têm tooltip
```

**A sensação de "mockup" tem causa própria, e não é a que ela supôs.**

## O achado central: 10 botões que só agem no segundo clique, sem avisar

| Widget | arquivo:linha | O clique faz | Falta |
|---|---|---|---|
| `lightbar_color_button` | `main.glade:765` | grava no rascunho | "Aplicar no controle" (`:796`) |
| `lightbar_brightness_scale` | `main.glade:871` | grava no rascunho | idem |
| `rumble_weak_scale` / `rumble_strong_scale` | `:1234`, `:1252` | **nenhum sinal** | lidos no "Aplicar"/"Testar" |
| `profile_name_entry` e mais 5 campos de Perfis | `:1495`, `:1511`, `:1578`, `:1613`, `:1627`, `:1641` | nenhum sinal | lidos no "Salvar" |

O caso que mais dói é a cor: **escolher uma cor não acende o controle.** O
handler grava no rascunho (`lightbar_actions.py:414`) e a docstring diz, com
todas as letras, *"não aplica no hardware automaticamente"*. O botão que aplica
fica trinta linhas de layout abaixo. E **nenhum dos três tem tooltip.**

Ela clica, o controle não muda, e conclui que está quebrado. Está funcionando —
e não está contando.

Diferir a escrita é uma decisão **correta** (evita escrever no hardware a cada
pixel de arraste do controle deslizante). O defeito não é o adiamento: é o
adiamento **silencioso**.

## Os dois que mentem de verdade

### 1. "Este jogo não funciona" promete um desfazer que não existe

`gui/main.glade:1878`, e o tooltip da linha seguinte termina com **"e dá para
desfazer"**.

- O handler (`app/actions/daemon_actions.py:970`) só chama
  `add_appid_to_steam_input_allowlist`.
- `remove_appid_from_steam_input_allowlist`
  (`integrations/steam_launch_options.py:821`) tem **zero chamadores em `src/`** —
  nove em `tests/`. Foi escrita, testada e nunca ligada.
- Não há **nenhuma** superfície de remoção: nem na janela, nem na linha de
  comando.
- A própria docstring da função órfã descreve o que ela ia resolver: *"tirar
  exigia abrir o `steam_input_apps.txt` num editor de texto — na prática o opt-in
  era irreversível"*.

E o custo do erro está escrito no código: *"um jogo marcado por engano deixa de
ter cor, gatilhos e co-op do Hefesto até ser desmarcado."* Um botão irreversível
com tooltip dizendo que é reversível.

### 2. "Ver daemon.toml" fabrica um arquivo de configuração falso

`gui/main.glade:2148` → `app/actions/emulation_actions.py:274-303`. O clique:

1. **cria** `~/.config/hefesto-dualsense4unix/daemon.toml` se não existir, com
   `[hotkey] buffer_ms=… ps_long_press_ms=…`;
2. abre no editor;
3. avisa "Abri o arquivo de referência no seu editor".

**O daemon não lê esse arquivo** — e o próprio código admite na linha 275
(`BUG-DAEMON-TOML-DEAD-01`). O botão põe, no diretório de configuração dela, um
arquivo que parece configuração, abre num editor, e editar não faz nada. O
"(referência)" no rótulo é a única defesa, e ela não sobrevive ao gesto.

## Os outros ruídos medidos

- **Um botão chamado "Modo jogo" que não liga o modo jogo.**
  `main.glade:2234` (aba Emulação) chama `daemon.emulation.suppress` — suspende
  mouse e teclado. Quem liga o modo jogo é **"Jogar pelo Hefesto"**, na aba
  Início, e a palavra "jogo" nem aparece no rótulo certo. Pior: o botão errado
  **nasce cinza** justamente quando ela mais espera que funcione. A colisão
  "modo jogo" já tinha sido nomeada na MODO-01 como seis conceitos com um nome
  só; este é o resíduo visível dela.
- **Cinco caixas fantasma.** `player_led_1..5` (`main.glade:926-930`) estão numa
  Box com `visible=False`, mas seguem declarando sinal. E o tooltip do botão ao
  lado (`:1022`) **fala delas para a usuária**: *"o texto antigo falava de '5
  checkboxes' que estão ocultos desde a LEDS-SO-PLAYER-01"* — um tooltip de
  produção explicando um refactor interno.
- **Dois "Salvar" na tela ao mesmo tempo**: `profile_save_button` (`:1705`, 149
  linhas, salva o editor) e `btn_footer_save_profile` (`:2746`, salva o rascunho
  inteiro, com outro diálogo). Mesmo rótulo, sentidos diferentes.
- **Um "Aplicar" redundante**: os seis presets de player LED já enviam por IPC
  (`lightbar_actions.py:822`); o "Aplicar o desenho" ao lado repete o que já
  aconteceu — e ensina que o clique anterior não bastou.

## Entregas

### 1. Nenhum controle age em silêncio

Toda mudança ou **acontece na hora**, ou **diz que está pendente**. Para os dez
diferidos:

- cor e brilho da lightbar **aplicam ao soltar** o controle deslizante
  (`button-release`), não a cada pixel — resolve o motivo original de diferir;
- o que continuar diferido ganha marca visível de pendente e o rodapé diz
  **"há mudanças não aplicadas"**, com o botão ao lado.

Critério: **não existe clique cujo efeito seja invisível e não anunciado.**

### 2. O desfazer do Steam Input passa a existir

Ligar `remove_appid_from_steam_input_allowlist` a um botão real, e listar os
jogos da exceção **por nome**, cada um com o seu "Desfazer". Enquanto isso não
existir, **o tooltip para de prometer** — mentira na tela é pior que falta.

### 3. "Ver daemon.toml" sai da janela

Não é reparo, é remoção. O arquivo não é lido; criá-lo é pior que não ter o
botão. Volta quando (e se) houver arquivo de configuração de verdade — o que
está proposto em
[PROMESSA-NAO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md),
bloco C.

### 4. Um nome, um conceito

- O botão da aba Emulação deixa de se chamar "Modo jogo" e passa a dizer o que
  faz: **"Suspender mouse e teclado"**.
- As cinco caixas fantasma saem do glade — invisível que declara sinal é dívida.
- O tooltip que explica refactor interno é reescrito para falar do que a pessoa
  vê.
- Um dos dois "Salvar" é renomeado (o do editor vira **"Salvar este perfil"**).

### 5. Menos superfície

145 controles simultâneos é o número a atacar, e a maior parte está em Gatilhos
(42 no caso simples, até 72). Não entra nesta sprint como redesenho — entra como
**medição de partida**: qualquer sprint de UI a partir daqui informa quantos
controles adiciona ou remove, e o número não sobe sem razão escrita.

### 6. Teste que morde

- Um widget do glade com `visible=False` **e** `<signal>` reprova.
- Um tooltip que contenha "desfazer" cujo handler não chame nenhuma função de
  remoção reprova. (Este teste, rodado hoje, reprova — é a prova de que morde.)
- Handler que só escreve no rascunho, sem marca de pendente na tela, reprova.

## Como você valida

De olho, sem terminal:

1. Aba Lightbar: escolha uma cor. **O controle acende na hora.** Se não acender,
   a tela diz que há mudança pendente e qual botão aplica.
2. Aba Sistema: marque um jogo em "Este jogo não funciona". O jogo aparece numa
   lista, **pelo nome**, com "Desfazer" ao lado. Clique e ele sai.
3. Aba Emulação: não existe mais nenhum botão chamado "Modo jogo", e não existe
   mais "Ver daemon.toml".
4. Passe por todas as nove abas: nenhum controle cinza sem explicação, nenhum
   texto falando de coisa que você não vê.
5. Rode o dedo pela janela: em nenhum lugar você clica e fica sem resposta.

**Critério que resume:** você nunca mais precisa se perguntar se clicou no botão
certo, nem se o clique valeu.

## O que NÃO foi medido

- **Não medi quantos dos 145 controles ela realmente usa.** O número é de
  superfície, não de uso. Reduzir precisa saber o que é supérfluo *para ela*, e
  isso é conversa, não medição.
- **Não medi o custo de aplicar a cor em tempo real.** Diferir foi decisão
  deliberada; `button-release` é a proposta, mas não medi a taxa de escrita que
  ela produz com quatro controles.
- **Não conferi os tooltips um a um** contra o que o handler faz. Achei duas
  promessas quebradas procurando padrões conhecidos; a varredura sistemática
  (comparar texto de tooltip com efeito do handler) é a entrega 6 e ainda não
  rodou.
- **Não sei se os 42 controles da aba Gatilhos incomodam.** São 19 presets ×
  parâmetros, e a densidade pode ser correta para quem ajusta gatilho. A queixa
  dela não nomeou essa aba.

---

## NOTA DATADA — 09/08/2026: a entrega 2 saiu, e o `ABERTA` seco caducou

**Nada acima foi apagado.** A medição botão por botão, os dez diferidos e as
seis entregas continuam inteiros — inclusive as que **ainda devem**.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **2. O desfazer do Steam Input passa a existir** | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/cli/cmd_gamepad.py:31` e `src/hefesto_dualsense4unix/cli/cmd_steam.py:3` — as duas linhas citam a entrega 2 por nome |

**Commit:** `e96dea8`, 27/07/2026.

### O que continua ABERTO nesta sprint — e não foi remarcado

- **A entrega 5 — "Menos superfície".** A regra de informar quantos controles
  cada sprint de interface adiciona ou remove **não virou portão**: nada no
  repositório conta os 145 controles simultâneos.
- **A entrega 6 — "Teste que morde".** Sem portão, sem cobertura medida.

As entregas 1, 3 e 4 não foram reconferidas nesta remarcação e continuam com o
estado que o corpo do documento descreve.

### Por que o rótulo da E2 não é ENTREGUE e sim ENTREGUE EM CÓDIGO

Porque o critério que a própria sprint escreveu é *"não existe clique cujo efeito
seja invisível e não anunciado"* — e isso é a tela dela, que só fecha com o olho
dela
([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).
