# A blindagem — índice da leva de 27/07/2026

- **Aberto em:** 27/07/2026
- **Pedido dela, literal:** *"controle cada aba da interface... me proponha as
  soluções com as opções pra resolvermos os problemas... temos a parte dos anti
  emojis que tá quebrando o projeto... queremos arrumar os espaços mal otimizados
  dos botões... quero que após isso vc melhore as sprints de tal forma que seja
  impossível o projeto quebrar novamente"*
- **Sucede:** [INDICE-a-fila-do-jogador](2026-07-26-INDICE-a-fila-do-jogador.md),
  que continua valendo. Esta leva **acrescenta** e **corrige**; não reordena a
  fila dela

## As três decisões dela, 27/07

Tomadas depois de ver as nove abas fotografadas e os números medidos:

| Pergunta | Escolha |
|---|---|
| Layout | **A — só devolver o espaço.** As nove abas ficam; nada muda de lugar |
| Anti-emoji | **Os dois lados** — curar o higienizador do ambiente **e** construir o gate do repositório |
| Escopo desta sessão | **Sprints escritas primeiro, código depois.** Nenhuma linha de código antes de ela ler |

A terceira decisão é a mais importante, e a razão dela está escrita: a leva de
26/07 foi reprovada por ter entregado demais de uma vez.

## O que foi EXECUTADO em 27/07, à noite

Ela autorizou a execução depois de ler as sprints. Resultado medido:

| Sprint | Estado | Prova |
|---|---|---|
| GATE-EMOJI-01 | **ENTREGUE** | o higienizador preserva os 238 glifos que apagava; a estrela proibida agora faz o commit **reprovar** |
| PORTÃO-VIVO-01 | **ENTREGUE** (A a F) | gate de acento enxerga f-string; CI dispara no ramo e em tag; 4 jobs novos |
| VÃO-01 | **ENTREGUE** (E1 a E4) | ver a tabela de antes e depois na própria sprint |
| PROVA-DE-TELA-01 | entregue como documento | não tem código |
| EMPATE-01 | **não executada** | o item 0 respondeu contra ela |

**Suíte: 5558 testes verdes.** `mypy --strict` limpo em 155 arquivos. Orçamento de
altura nos mesmos 7 testes da linha de base. Glade com os mesmos 205 ids e 70
sinais do HEAD, sem um aviso do GtkBuilder. **Nada commitado.**

### Duas coisas continuam vermelhas, de propósito

Os dois gates novos que reprovam hoje entraram com `continue-on-error` e
comentário dizendo que é temporário — relatam sem barrar a leva:

- `validar-referencias-docs.py`: **25 referências mortas** em `docs/`;
- `shellcheck -S error`: **1 erro real**, `scripts/build_appimage_gui.sh:90`.

São dívida declarada com número, que é o oposto de gate que ninguém roda.

### O achado que apareceu durante a execução

O `andromeda-autosync.timer` commita `~/.config/zsh` **a cada 10 minutos**, e um
hook daquele repositório apaga qualquer linha que contenha o token de
co-autoria — inclusive **dentro de código**. Isso quebrou o `universal-sanitizer.py`
com `TypeError` duas vezes durante a entrega, porque a expressão regular dele
contém exatamente esse token. Há precedente registrado: o commit `6260537`, de
20/03/2026, se chama *"restaurar variaveis e identidade removidas pelo
auto-sanitize"*.

É a mesma classe do defeito que esta leva curou — reescrita silenciosa que quebra
o arquivo — só que num segundo lugar e com dez minutos de intervalo.

## A segunda leva, e o que ela abriu — 27/07 à noite

Ela autorizou tocar a aba Status e mandou executar. Entregue e validado de olho:

| Sprint | Estado |
|---|---|
| **STATUS-SIMETRIA-01** | ENTREGUE as entregas 2, 3 e 4 (glifos legíveis crescendo com a escala, círculos dos analógicos alinhados, meio do card ocupado). A entrega 1 (microfone) **não apareceu** |
| **BOTÃO-QUE-NÃO-MENTE-01** | ENTREGUE 1 a 4: cor acende ao soltar; "Ver daemon.toml" removido; "Modo jogo" virou "Suspender mouse e teclado"; tooltips pararam de mentir; desfazer do Steam Input existe |
| Dívidas do CI | PAGAS: 25 referências mortas e o erro de shellcheck viraram zero; os dois portões deixaram de ser `continue-on-error` |

**5587 testes verdes**, `mypy --strict` limpo em 156 arquivos, e os quatro gates
em zero.

### As sprints que a validação dela abriu

Ela olhou a aba Status maximizada e reprovou como **incompleta**, com cinco
defeitos nomeados. Cada um virou documento:

| Sprint | O que ataca |
|---|---|
| [**EMPATE-01**](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md) | **CRÍTICA** — o controle sem cor: `fallback` cinza vencendo `vitoria` pelo alfabeto, e o cinza é semente do projeto |
| [**LIGHTBAR-JOGADOR-01**](2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | a aba mostra o rascunho e não o que está aplicado; o jogador vira protagonista |
| [**PALAVRA-01**](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md) | 24 textos em minúscula, jargão, 188 controles sem tooltip, e o DSX sai do nome da aba |
| [**STATUS-SIMETRIA-02**](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md) | *"distanciar não é organizar"* — títulos com número de linhas diferente, touchpad sem bloco próprio, vazios |
| [**MIC-PRESENTE-01**](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md) | o microfone some da faixa e faz o layout inteiro pular |

E dois estudos guardam o que se aprendeu fazendo:

- [Como controlar e fotografar a janela](../estudos/2026-07-27-como-controlar-e-fotografar-a-janela.md) — o método, as cinco tentativas que falharam, e o sensor de aba ativa pelo sublinhado rosa
- [O que os agentes acharam](../estudos/2026-07-27-o-que-os-agentes-acharam.md) — as seis refutações medidas, as três instruções minhas que os agentes recusaram com razão, e as duas classes de defeito que apareceram duas vezes cada

## As cinco sprints desta leva

| Sprint | O que ataca | Prioridade |
|---|---|---|
| [**GATE-EMOJI-01**](2026-07-27-GATE-EMOJI-01-o-higienizador-apaga-o-que-o-adr-protege.md) | O higienizador apaga os cinco glifos que o ADR-011 nomeia e deixa passar o proibido. 222 ocorrências em 5 arquivos versionados | ALTA |
| [**EMPATE-01**](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md) | Três catch-all empatados em prioridade 0; quem vence é a ordem alfabética do arquivo. `fallback` ganha de `vitoria` | ALTA |
| [**PORTÃO-VIVO-01**](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md) | Zero portões rodando no commit; gate de acento cego a f-string; CI que não vê este ramo | ALTA |
| [**PROVA-DE-TELA-01**](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md) | O portão humano. Existia só como seção de índice desde 26/07 | ALTA |
| [**VÃO-01**](2026-07-27-VAO-01-a-tela-sobra-e-o-conteudo-aperta.md) | 47% de fundo liso em média nas nove abas, com rótulo cortado e botão de emergência minúsculo | MÉDIA |

## O que esta leva REFUTOU do material existente

Uma passada adversarial foi rodada contra as próprias conclusões desta sessão, e
ela derrubou cinco afirmações — três delas escritas em sprints já abertas. **Cada
uma foi reconferida à mão antes de entrar aqui.**

### 1. O teto de 100 não era o que impedia o perfil do jogo de vencer

A regra **R-A** da fila do jogador traz como *"prova de que a regra é
necessária"*: *"não existia número escolhível pela interface que fizesse o perfil
de um jogo vencer"*.

Medido no código: `profiles/manager.py:624` ordena por
`(not p.e_catch_all, p.priority)` — **especificidade antes de prioridade**.
Qualquer perfil com critério vence qualquer catch-all, mesmo com prioridade 0. E
`manager.py:614-621` **veta todos os catch-all** quando a janela é `steam_app_*`.

Medido no disco dela, hoje: `pragmata.json` tem critério e prioridade **100**;
`vitoria.json` é catch-all e prioridade **0**. O estado que se dizia só alcançável
escrevendo 110 à mão está em 100, dentro da escala da janela.

**Consequência:** subir o teto para 200 não conserta nada medido, e re-ranqueia
perfis de mesma especificidade — mexendo num tuning de 50 a 80 que o próprio
módulo diz ser validado. A regra R-A continua boa; **a prova dela precisa ser
trocada**. E o buraco real que sobra é outro: o perfil novo nasce catch-all
(`profiles_actions.py:704`), embora a interface já tenha a opção certa.

### 2. As fontes da identidade visual ESTÃO instaladas nesta máquina

`PROMESSA-NAO-CUMPRIDA-01`, bloco B1, afirma que *"a janela nunca teve a
tipografia que o desenho especifica"* e que *"toda discussão de legibilidade até
hoje aconteceu com as fontes erradas"*.

Medido: `fc-match "Space Grotesk"` devolve `SpaceGrotesk-Regular.ttf`;
`fc-match "JetBrains Mono"` devolve `JetBrainsMono-Regular.ttf`. As duas estão lá.

**O que sobra de verdadeiro:** `grep -c install_fonts install.sh` devolve **0** —
uma instalação nova continua sem elas. O item deixa de ser ALTO e vira uma linha
no instalador.

### 3. O timer do guarda do Steam Input está vivo

`STEAM-INPUT-01` descreve, na entrega 7, um estado de timer parado. Medido:
`hefesto-steam-input-guard.timer` está **active**, disparou há menos de um minuto
e tem o próximo agendado — ciclo de 30 minutos.

### 4. Esconder aba não reindexa — mas há DOIS sites de índice cru, não um

Medido com GTK real: esconder a página 0 **não** muda `get_current_page()`. O
pré-requisito que se atribuía à opção D de layout é falso.

O que é verdade, e é pior: existem **dois** lugares comparando índice cru —
`status_actions.py:1189` (`!= 1`, o tique de 10 Hz dos analógicos) e
`home_actions.py:663` (`== 0`, o poller da aba Início). Qualquer reordenação ou
fusão futura quebra os dois, em silêncio e sem log. Não é problema da opção A
escolhida, mas fica registrado para quando o assunto voltar.

### 5. Fazer o higienizador reprovar, sozinho, não faz nada

`~/.config/git/hooks/pre-commit:206` chama o higienizador com `2>/dev/null`, sem
`||` e sem testar o código de saída, e re-adiciona os arquivos em `:208-210`.
Mudar o script sem mudar o hook é inócuo. Isso está incorporado na entrega 1 da
GATE-EMOJI-01.

## O que continua sem medição, e é o maior buraco desta leva

- **O daemon está vivo agora e ninguém consultou o estado real dele.** O journal de
  hoje não tem nenhum evento de troca de perfil ou de modo solto. Os números de
  flapping citados nas sprints de perfil são de 26/07 e **não foram reproduzidos**
  antes de virarem entrega.
- **`autoswitch_locked.flag` está ligado desde 24/07 20:42** — é a configuração
  real dela, e nenhuma sprint de perfil diz o que muda com o cadeado ligado.
- **Os testes de layout não rodaram neste ramo.** Toda a aritmética de espaço parte
  de números de uma sprint anterior. É o item 0 da VÃO-01.
- **`app/compact_window.py` e a bandeja** ficaram fora de todos os levantamentos.

## Ordem sugerida

| # | Sprint | Por que aqui |
|---|---|---|
| 1 | **GATE-EMOJI-01** | É o que ela apontou como quebrando o projeto, e o dano é silencioso: o teste fica verde com a função quebrada |
| 2 | **EMPATE-01, item 0** | Dois minutos de olho. Se confirmar, sobe para o topo — é a classe "desfaz trabalho dela" |
| 3 | **PROVA-DE-TELA-01** | É a última a construir e a **primeira a usar**. Sem ela, tudo abaixo entra sem caixa de validação |
| 4 | **PORTÃO-VIVO-01, blocos A e B** | O gate de acento cego e o commit sem portão. Baratos e mordem hoje |
| 5 | **VÃO-01** | Depois da folha de prova existir, porque é a única desta leva que muda o que ela vê |

E a trava que vale para todas: **nenhuma entrega desta leva entra em código antes
de ela ler este índice.** Foi a escolha dela, e é a resposta direta ao que deu
errado em 26/07.
