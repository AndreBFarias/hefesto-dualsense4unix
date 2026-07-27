# Inventário: todos os controles interativos da janela, um a um

- **Levantado em:** 27/07/2026, sobre `v0.2.0`
- **Motivo:** a frase *"sinto às vezes que os botões são mockup puro e não
  funcionam ou estão confusos demais ou muito complexos"* merecia número, não
  impressão
- **Método:** parse XML do glade, AST do `app/`, e grep. Nada de leitura por
  amostragem

## Veredito

A frase tem duas afirmações. Uma se refuta, a outra se confirma — e as duas
respostas importam.

**"Mockup puro / não funcionam" — REFUTADO para a maioria esmagadora.**

```
66 handlers declarados no glade
66 existem no dicionario de sinais de app/app.py:247-349
66 tem def em app/
 0 com corpo vazio (pass / return / docstring)
 0 handlers orfaos
 0 botoes que nascem cinza e nunca ligam
```

A cola entre janela e código está **fechada**, e isso foi trabalho de alguém —
está registrado como `BUG-GUI-EMULATION-HANDLERS-UNWIRED-01`.

**"Confusos demais / muito complexos" — CONFIRMADO, com número.**

```
145 controles acionaveis no cenario simples   (1 controle, gatilhos desligados)
183 no cenario cheio                          (2 gatilhos parametricos, 4 controles)
  6 botoes dizem "Aplicar" alguma coisa
  6 dizem "Desligar / Apagar / Parar"
  2 dizem "Salvar", com semanticas diferentes, visiveis ao mesmo tempo
 48 dos 85 widgets do glade NAO tem tooltip
```

## Inventário por aba

Categorias: **VIVO** (chama IPC, roda subprocesso, grava arquivo ou muda estado);
**DIFERIDO** (só escreve no rascunho — nada acontece até um segundo clique
noutro lugar); **INALCANÇÁVEL** (handler vivo, widget invisível); **PROMESSA
QUEBRADA** (tooltip ou rótulo promete o que o código não faz); **MORTO**.

| # | Aba | Glade | Código | Total | VIVO | DIFERIDO | INALCANÇ. | PROM. QUEBR. | MORTO |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | Início | 1 | 8 | 9 | 9 | 0 | 0 | 0 | 0 |
| 1 | Status | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | Gatilhos | 4 | 38 | 42 | 42 | 0 | 0 | 0 | 0 |
| 3 | Lightbar | 19 | 0 | 19 | 12 | 2 | **5** | 0 | 0 |
| 4 | Rumble | 11 | 0 | 11 | 9 | 2 | 0 | 0 | 0 |
| 5 | Perfis | 14 | 13 | 27 | 21 | 6 | 0 | 0 | 0 |
| 6 | Sistema | 13 | 0 | 13 | 12 | 0 | 0 | **1** | 0 |
| 7 | Emulação | 12 | 0 | 12 | 11 | 0 | 0 | **1** | 0 |
| 8 | Navegação DSX | 7 | 0 | 7 | 7 | 0 | 0 | 0 | 0 |
| — | Rodapé | 4 | 0 | 4 | 4 | 0 | 0 | 0 | 0 |
| | **TOTAL** | **85** | **60** | **145** | **128** | **10** | **5** | **2** | **0** |

Observação estrutural: **`GtkComboBox` = 0**. Todos foram trocados por
`SegmentedSelector`, que cria um botão de rádio por item, **todos visíveis ao
mesmo tempo**. Isso resolveu um defeito real de foco no cosmic-comp (dropdowns
fechando sozinhos) e é a maior fonte isolada de contagem de widgets.

## Os 10 DIFERIDOS — a causa da sensação de "mockup"

| Widget | Onde | O clique faz | O que falta |
|---|---|---|---|
| `lightbar_color_button` | `main.glade:765` | grava no rascunho | "Aplicar no controle" (`:796`) |
| `lightbar_brightness_scale` | `:871` | idem — a docstring diz *"não aplica no hardware automaticamente"* | idem |
| `rumble_weak_scale` / `rumble_strong_scale` | `:1234`, `:1252` | **nenhum sinal** | lidos no "Aplicar"/"Testar" |
| 6 campos da aba Perfis | `:1495`, `:1511`, `:1578`, `:1613`, `:1627`, `:1641` | nenhum sinal | lidos no "Salvar" |

**Escolher uma cor não acende nada.** É o caso mais defensável da queixa, e
nenhum dos três controles envolvidos tem tooltip.

Diferir é decisão **correta** — evita escrever no hardware a cada pixel de
arraste. O defeito não é o adiamento: é o adiamento **silencioso**.

## Os 2 que mentem

### 1. "Este jogo não funciona" — `main.glade:1878`

O tooltip termina com **"e dá para desfazer"**. Não dá:

- o handler só chama `add_appid_to_steam_input_allowlist`;
- `remove_appid_from_steam_input_allowlist`
  (`integrations/steam_launch_options.py:821`) tem **zero chamadores em `src/`** —
  nove em `tests/`. Foi escrita, testada e nunca ligada;
- não há **nenhuma** superfície de remoção, nem na janela nem na linha de comando.

A própria docstring da função órfã descreve o problema que ia resolver: *"tirar
exigia abrir o `steam_input_apps.txt` num editor de texto — na prática o opt-in
era irreversível"*. E o custo está escrito no código: *"um jogo marcado por
engano deixa de ter cor, gatilhos e co-op do Hefesto até ser desmarcado."*

### 2. "Ver daemon.toml (referência)" — `main.glade:2148`

O clique **cria** `~/.config/hefesto-dualsense4unix/daemon.toml` se não existir,
com conteúdo que parece configuração, e o abre num editor.

**O daemon nunca lê esse arquivo**, e o próprio código admite
(`emulation_actions.py:275`, `BUG-DAEMON-TOML-DEAD-01`). O botão fabrica
configuração falsa no diretório de configuração da usuária. Sem tooltip. O
"(referência)" no rótulo é a única defesa e não sobrevive ao gesto de abrir um
`.toml` num editor.

## Os 5 inalcançáveis

`player_led_1..5` (`main.glade:926-930`) vivem numa `GtkBox` com
`visible=False` + `no-show-all=True` (`:922`), e **continuam declarando sinal**. O
handler existe e é vivo.

Pior: o tooltip do botão ao lado (`:1022`) **fala deles para a usuária** —
*"o texto antigo falava de '5 checkboxes' que estão ocultos desde a
LEDS-SO-PLAYER-01"*. Um tooltip de produção explicando um refactor interno.

## Colisões de nome medidas

### "Modo jogo" nomeia duas coisas

| Caminho | Cliques | O que faz |
|---|---|---|
| Aba Início -> "Jogar pelo Hefesto" | **1** | liga o modo jogo de verdade (IPC) |
| Aba Emulação -> botão **rotulado "Modo jogo"** (`:2234`) | **2** | outra coisa: suspende mouse e teclado. E **nasce cinza** se você ainda não estiver em "Jogar pelo Hefesto" |

O rótulo do conceito certo é "Jogar pelo Hefesto" — a palavra "jogo" **nem
aparece** nele.

### Dois "Salvar" simultâneos

`profile_save_button` (`:1705`, handler de 149 linhas, salva o editor) e
`btn_footer_save_profile` (`:2746`, 35 linhas, salva o rascunho inteiro com outro
diálogo). Mesmo rótulo, semânticas diferentes, visíveis ao mesmo tempo.

### Um "Aplicar" redundante

Os seis presets de LED de jogador **já enviam por IPC**
(`lightbar_actions.py:822`). O "Aplicar o desenho" ao lado repete o que já
aconteceu — não mente, mas ensina que o clique anterior não bastou.

## Passos de clique para as tarefas comuns

| Tarefa | Cliques | Observação |
|---|---|---|
| Ligar o modo jogo | **1** | pelo caminho certo; 2 e frustração pelo errado |
| Criar perfil para o jogo aberto | **5 + digitação** | em 2 abas, com 2 botões "Salvar" na tela |
| Ligar Steam Input num jogo | **2** | **desfazer: 0 caminhos** |

Na criação de perfil há coisa boa e registrada: o appid é preenchido sozinho se o
jogo está em foco (`profiles_actions.py:620`) e o modo é pré-selecionado
(`:547`).

## Código morto sem efeito na tela

| Função | Onde | Chamadores em `src/` |
|---|---|---|
| `_query_gamepad_state` | `app/actions/daemon_actions.py:567` | **0** (e 0 em testes — morto absoluto, 21 linhas) |
| `short_button_label` | `app/actions/external_controllers.py:134` | **0** (4 em testes) |

## Um resultado que merece registro positivo

Varredura completa por `TODO`, `FIXME`, `XXX`, `stub`, `placeholder`, `mockup`,
`no-op` em `app/`: **57 ocorrências, nenhuma é dívida aberta.** Todas são a
palavra portuguesa "todo(s)", `set_placeholder_text` legítimo, stub de GTK para o
CI sem PyGObject, ou post-mortem de bug já corrigido.

**Não há um único `# TODO:` de trabalho pendente na interface.** Num projeto
deste tamanho, isso é incomum — e é coerente com a regra da casa de que achado
colateral vira sprint com identificador, nunca comentário.

## O que este inventário NÃO mediu

- **Quantos dos 145 controles ela realmente usa.** O número é de superfície, não
  de uso. Reduzir exige saber o que é supérfluo *para ela* — conversa, não
  medição.
- **Os tooltips um a um contra o que o handler faz.** As duas promessas quebradas
  saíram de padrões conhecidos; a varredura sistemática ainda não rodou.
- **Se os 42 controles da aba Gatilhos incomodam.** São 19 presets mais
  parâmetros, e a densidade pode ser correta para quem ajusta gatilho. A queixa
  não nomeou essa aba.
