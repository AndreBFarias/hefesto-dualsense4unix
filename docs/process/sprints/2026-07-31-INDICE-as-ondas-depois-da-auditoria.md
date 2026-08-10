# As ondas de execução, depois da auditoria de 31/07/2026

- **Levantado em:** 31/07/2026, sobre `HEAD 7bd0cb7`, com a **v0.4.0 publicada**
  em 30/07, na branch `restauro/inicio-da-sessao`
- **Base:** a [auditoria de treze agentes](../estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md)
  — nove auditores particionados mais quatro verificadores independentes com
  poder de reprovar
- **Sucede:** o [índice das três faixas](2026-07-30-INDICE-as-tres-faixas-depois-da-v040.md)
  de 30/07, que continua válido no essencial e recebe **três correções** desta
  auditoria (registradas abaixo)
- **Autorização dela, literal, em 31/07:** *"vendo que nossas sprints atuais
  estão desatualizadas, ou são fracas, ou não temos, pode então alterar ou criar
  novas sprints e adicionar elas às próximas ondas de execução"*

## Como ler este índice

**As ondas são separadas por quem precisa estar presente**, não por assunto. É a
única divisão que muda o que dá para fazer hoje à noite e o que espera ela sentar
na frente da tela.

O campo `Status:` dos documentos **continua não sendo fonte** — 41 dos 50 diziam
ABERTA hoje de manhã, incluindo entregas provadas. Esta sessão corrigiu **seis**
cabeçalhos com a evidência do commit que os fechou (EMPATE-01, PALAVRA-01,
PORTÃO-VIVO-01, MIC-PRESENTE-01, STATUS-SIMETRIA-02 e JOGO-01). Os demais
continuam mentindo, e a passada completa é a entrega C7 da onda 3.

---

## As três correções ao índice de 30/07

Medidas hoje, com prova. Quem for atacar a FAIXA 1 daquele índice precisa
destas três antes.

**1. O cadeado do autoswitch tem DUAS portas, não uma.**
`profiles/autoswitch.py:252-262` cede se `perfil_e_regra_de_jogo(profile, info)`
**ou** `perfil_declara_modo_de_jogo(profile)`. A segunda nasceu em `54f1f3b`
(25/07, MODO-01/B2), **cinco dias antes** daquele índice, que a descreve como
porta única em dois lugares (linhas 70-74 e 113-115).

**2. E o furo por título vem da SEGUNDA porta, não da primeira.** O índice
atribui o furo a `perfil_e_regra_de_jogo`, mas esse predicado **recusa título de
propósito** (`schema.py:620-624` diz *"Regex de título não conta"*, `:633` exige
`window_class` preenchido, `:636` exige `steam_app_` em foco). Quem aceita título
é `perfil_declara_modo_de_jogo`. A conclusão operacional do índice continua
verdadeira — `fps.json` e `coop_local.json` dela furam o cadeado — mas pelo outro
caminho.

**2-bis. O jogo dela não passa pelo wrapper — medido ao vivo em 31/07 01:57**,
com o PRAGMATA.exe rodando há 20 minutos. A opção de lançamento é
`VKD3D_CONFIG=no_upload_hvv %command%`, e o `launch_env/` não tem `last_run` nem
`last_exit`. A **evidência nº 3** do sinal de jogo (o marcador do wrapper) está
**estruturalmente ausente** do jeito que ela joga, e a nº 2 não conta porque só
recebe `wm_class`. Sobra **uma evidência só**: a janela. Isso muda o desenho da
[SINAL-DE-JOGO-01](2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md)
inteira — não é hipótese, é o estado da máquina dela agora.

**3. A entrega 2 da PERFIL-JOGO-01 está PAGA e sai da lista.** O índice a deixou
como "medição pendente". Medido hoje: `player_leds` **é** retido junto com `led`
quando `_game_wins()` fecha — mesmo dicionário `fields`
(`backend_pydualsense.py:2780-2785`), mesmo `retido.update`, mesmo gate no merge
(`:1170-1171`) — e o teste morde (`test_game_output_replica.py:288`).

---

# ONDA 1 — o que eu faço sozinha, hoje

Nada aqui precisa dela na frente da tela. Tudo é reversível, e cada item tem
aceite executável.

| # | Item | Sprint | Por que primeiro |
|---|---|---|---|
| 1.1 | **Os 4 portões `-w` do `install.sh`** (linhas 620/686/696/700) viram `-e`, mais o rearme das 6 curas e os 2 testes de simetria | [ÁRVORE-DIVERGENTE-01/E2](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md) | é o achado grave nº 1, a correção já existe pronta em `9c944a8`, e foi isto que ela sofreu em 26/07 |
| 1.2 | **O exemplo do guia de perfis que o daemon rejeita** (`creating-profiles.md:19`, `mode: "Medium"`) | [DOC-VERDADE-02/E1](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md) | uma linha; hoje quem copia o primeiro exemplo não cria perfil |
| 1.3 | **As duas receitas mortas de ligar plugin** no ADR-017 | [DOC-VERDADE-02/E2](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md) | o README já documenta a variável certa — é alinhar o ADR |
| 1.4 | **O metainfo AppStream com a data e o texto da 0.3.0**, e a 0.3.0 devolvida à série | [PUBLICAÇÃO-FIEL-01/E1](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | está publicado no bundle da v0.4.0 agora |
| 1.5 | **`docs/usage/instalacao.md` mandando instalar a v0.3.0** + virar o décimo alvo do verificador | [PUBLICAÇÃO-FIEL-01/E3](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | é a página que a casa aponta como caminho canônico |
| 1.6 | **O job `pypi` fora do guarda de CI** (`needs: guarda-ci` + estender o teste estrutural) | [PUBLICAÇÃO-FIEL-01/E4](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | hoje inerte; vira furo no dia em que a variável existir |
| 1.7 | **As fontes que o `uninstall` nunca remove** — o removedor já existe (`install_fonts.sh --remove`) | [SIMETRIA-INSTALL-02/E1](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | é a única assimetria nova, e viola regra da casa |
| 1.8 | **`purge.sh` sem `--help` e aceitando argumento desconhecido** | [SIMETRIA-INSTALL-02/E3](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | é o script mais destrutivo, com o padrão do acidente que a casa já pagou |
| 1.9 | **`sudo bash uninstall.sh` sugerido no caminho de erro** | [SIMETRIA-INSTALL-02/E4](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | com `HOME=/root` a desinstalação sai pela metade |
| 1.10 | **`lib.fakeSha256` no `package.nix:79`** | [SIMETRIA-INSTALL-02/E5](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | pendência de 26/07 que atravessou a v0.4.0 |
| 1.11 | **O latch `_draft_reload_for` que trava a reconciliação** | [JANELA-FIEL-01/E1](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | é o R-08 voltando por uma fresta: ela edita e salva o perfil **anterior** |
| 1.12 | **Os dois pollers que gateiam por índice de página** (regra EST-10) | [JANELA-FIEL-01/E2](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | bate por sorte; a próxima aba inserida quebra em silêncio |
| 1.13 | **"Restaurar Padrão" morto em instalação empacotada** | [JANELA-FIEL-01/E3](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | o loader já tem o resolvedor de três candidatos |
| 1.14 | **Conflito de perfil checado por nome cru, não por slug** | [JANELA-FIEL-01/E4](2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | "Navegacao" sobrescreve "Navegação" sem a pergunta que a tela promete |
| 1.15 | **O emblema de testes derivado do CI** (6089 → 6097 medidos) | [PUBLICAÇÃO-FIEL-01/E6](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | defasa por construção a cada leva |
| 1.16 | **`tests/integration/` e `tests/shell/` vazios** + os 5 `os.fork()` | [TESTE-HONESTO-01/E4, E5](2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md) | faxina; a árvore mente sobre a própria cobertura |
| 1.17 | **O `NOTICE` declarando os três drivers GPL-2.0** | [CR-05](2026-07-25-CR-05-proveniencia-completa-do-notice.md), pela [CR-SEQUÊNCIA-01/E1](2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md) | **Atenção: depende de ela reabrir o trilho CR** — ver onda 3 |

**Ordem sugerida dentro da onda 1:** 1.1 primeiro (é o único com dano medido no
hardware dela), depois o bloco de documentação (1.2 a 1.5, que são linhas), depois
a janela (1.11 a 1.14, que é onde ela sente), e a faxina por último.

---

# ONDA 2 — precisa do olho dela

Cada item aqui só vira commit com print antes e depois, pela regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md).

| # | Item | Sprint | O que ela precisa fazer |
|---|---|---|---|
| 2.1 | **Os desenhos ocuparem o vão lateral** — touchpad, lightbar, microfone e alto-falante | [CARD-OCUPA-01](2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md) | é **pedido dela de hoje, 01h34**; olhar a aba Status maximizada e dizer se o tamanho ficou bom |
| 2.2 | **O teto elástico nas seis abas** (E4 e E5) | [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | é o *"a mesma largura em todas as abas"* dela; passar pelas nove com Ctrl+PageDown |
| 2.3 | **O miolo do frame Estado** — a barra de bateria com 1242px para dois dígitos | [LARGURA-01/E2](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | maior retorno por linha, e é a aba que ela mais olha |
| 2.4 | **A linha `healthy` → `seeing`** | [SINAL-DE-JOGO-01](2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md) | **Atenção: entra SOZINHA**, com ela olhando a lightbar — a transição repinta o controle |
| 2.5 | **O experimento do sinal de jogo** — reproduzir a queda com jogo comprovadamente vivo | [SINAL-DE-JOGO-01/E1](2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md) | abrir um jogo e deixar rodando; **ninguém nunca mediu isso** |
| 2.6 | **O aviso antes de derrubar o co-op** | [CONTAGEM-E-COOP-01](2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md) | o fato já é emitido pelo daemon; falta a janela mostrar |
| 2.7 | **O radar das outras três superfícies** — applet, bandeja, janela compacta | [RADAR-01](2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md) | olhar o applet na barra e dizer se ele contradiz a janela |
| 2.8 | **EMPATE-01/E2** — a aba mostrar que há disputa | [EMPATE-01](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md) | cinco perfis dela dizem "Sempre" e um vence sem explicação |
| 2.9 | **PERFIL-JOGO-01** — a mais cara e a de maior impacto | [PERFIL-JOGO-01](2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | **Atenção:** a entrega 1 (o experimento) vem antes de qualquer código, e as E3/E4 precisam ser **reescritas** contra as duas portas |
| 2.10 | **LIGHTBAR-JOGADOR-01** — as seis entregas | [LIGHTBAR-JOGADOR-01](2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | só **depois** da 2.9: as duas mexem em quem manda na cor |

> **NOTA DATADA (09/08/2026) — o item 2.6 caducou, e caducou em três minutos.**
> A linha acima diz *"o fato já é emitido pelo daemon; falta a janela mostrar"*.
> **A janela mostra.** O aviso mora no banner — `app/actions/status_actions.py`,
> `_coop_badge` criado em `:1173-1181` e escondido/mostrado em `:1662` — com a
> frase montada por `texto_do_coop_derrubado` (`:255`), e coberto por
> `tests/unit/test_coop_derrubado_aparece_no_banner.py`.
>
> O que dói é o relógio. Este índice entrou em `23c7c94`, **31/07 às 09:43:57**.
> O banner entrou em `cd5eaf1`, **31/07 às 09:47:19** — **três minutos e vinte e
> dois segundos depois**. Ninguém voltou aqui para riscar a linha, e ela ficou
> nove dias na fila dizendo que faltava algo que já estava de pé.
>
> **O texto acima não se apaga**: ele é a prova de que um índice envelhece em
> minutos, e de que a passada de cabeçalhos (a C7 da onda 3, prometida no topo
> deste arquivo) é dívida real, não capricho.
>
> **O que ainda falta nela:** abrir a janela com o co-op montado, deixar um jogo
> com Steam Input derrubar os jogadores 2/3/4, e ver se o aviso aparece no topo
> da janela — de qualquer aba — dizendo quantos caíram e que não foi ela.

---

# ONDA 3 — o que trava esperando decisão dela

Nada disto anda sem ela responder. São perguntas, não tarefas.

| # | A pergunta | Onde está o custo dos dois lados |
|---|---|---|
| 3.1 | **A ref local `main`** — retargetar para `origin`, apagar, ou deixar? Hoje `git push` estando nela mira o repositório do André | [ÁRVORE-DIVERGENTE-01/E0](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md); a tag `arquivo/main-antes-da-v030` é o **mesmo commit**, então nada se perde |
| 3.2 | **Reabrir o trilho da sala limpa?** E a CR-05 pode ir sozinha agora? | [CR-SEQUÊNCIA-01](2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md) — resposta à dúvida dela de hoje |
| 3.3 | **O `(Rigid)`, o `(Bow)` e o `(Galloping)` ficam nos rótulos?** É decisão de sala limpa (regra R2), não de vocabulário | [CR-SEQUÊNCIA-01/E5](2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md) |
| 3.4 | **O `[REDACTED]` no README publicado** — URL real do fork, ou marcador honesto? Não há ADR registrando a política | [PUBLICAÇÃO-FIEL-01/E2](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) |
| 3.5 | **O destino do `hefesto-dsx-recover.service`** — o doctor ensina a instalar a unidade que o storm-audit chamou de realimentação positiva | [SIMETRIA-INSTALL-02/E6](2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) |
| 3.6 | **Trazer ou não os commits que só existem na `main`** (E3, E4, E5) | [ÁRVORE-DIVERGENTE-01](2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md) — o método já está escrito: reaplicar um a um, nunca cherry-pick em bloco |
| 3.7 | **O rótulo `Custom`** — "Personalizado (avançado)" tem 24 caracteres contra teto de 22 | [GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md); a sprint recomenda "Montar do zero" |
| 3.8 | **O que o R1 deve fazer** — o padrão continua Alt+Tab | índice de 30/07, decisão 1 |
| 3.9 | **`pragmata.json` × `pragmata2.json`** — idênticos fora o nome, ambos catch-all, ambos prioridade 5 | índice de 30/07, decisão 3 |
| 3.10 | **Religar o hold do PS**, o **drop-in 51 do microfone** e a **migração de 25/07 nos seis presets** | índice de 30/07, decisões 2, 4 e 5 |

---

# As dívidas de fundo — grandes demais para uma onda

Estas não entram em onda nenhuma como estão: são reforma, não conserto. Ficam
registradas para não virarem surpresa.

**A classe `Daemon` com ~95 métodos e ~3280 linhas**, com o acoplamento voltando
dos subsistemas por `getattr` (66 ocorrências em `ipc_handlers.py`, 49 em
`gamepad.py`, 21 em `coop.py`). Como `getattr` com default tolera ausência em
silêncio, renomear um método pode desligar comportamento em três subsistemas
**sem erro nenhum**. O caminho medido não é reescrever: é extrair os aglomerados
já coesos e trocar `getattr`-com-default por protocolo tipado onde o daemon é
sempre real.

**Os 297 testes contra GTK de mentira** (17 arquivos na `DIVIDA_GI_FALSO`, os
mesmos de 30/07, zero pagos) — mas com a moldura corrigida pela medição: **na
máquina dela eles usam o GTK real**, porque a guarda `GATE-SKIP-MASK-01` volta
antes de plantar. **O falso-verde mora no CI**, e foi reproduzido simulando o
ambiente do job `lint-test`: 29 verdes contra `Gtk.Box = object`. É a entrega E1
da [TESTE-HONESTO-01](2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md),
explicitamente **por lotes** — não cabe numa onda.

**A premissa USB-é-o-mundo**, agora com número: 9 usos de `transport="bt"` contra
196 de `transport="usb"` nos fakes do daemon, e **zero** marcador de skip por
hardware BT. O buraco não é skip visível, é ausência de caso.

**A tradução**, bloco F da PROMESSA-NÃO-CUMPRIDA-01: 16 de 18 módulos de
`app/actions/` não importam `gettext`, então traduzir os `.po` **não traduz a
janela**. Trabalho grande e independente.

**Os 438 `replace refs` do `filter-repo`**, que fazem `git cat-file` de hash
antigo devolver o conteúdo do commit novo **em silêncio**. Não afeta o produto;
afeta toda arqueologia futura por hash. `git replace -d` resolve, fora de uma
sessão somente-leitura.

---

# O que este índice NÃO mediu

- **A janela não foi aberta em nenhum momento da auditoria.** Toda afirmação
  sobre interface vem de código e de `.glade`. O aceite continua sendo o olho
  dela.
- **Nenhum ciclo `install`/`uninstall` foi executado**, nenhum pacote foi
  construído, `nix build` não rodou (o `nix` não existe nesta máquina).
- **Os 13 identificadores de sprint sem documento** foram contados, não
  materializados — dois deles saíram desta sessão (CONTAGEM-E-COOP-01 e o
  radar da SEGUNDA-JANELA-01), e onze continuam fantasmas.
- **Os cabeçalhos `Status:`**: seis corrigidos com prova, o resto continua
  mentindo.
- **O applet não foi construído nem executado** — é justamente o objeto da
  RADAR-01.
- **A suíte rodou uma vez.** Sem repetição, não há afirmação sobre estabilidade
  dos testes de timing.
