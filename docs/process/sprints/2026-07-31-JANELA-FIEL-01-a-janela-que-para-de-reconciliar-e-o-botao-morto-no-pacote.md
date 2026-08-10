# JANELA-FIEL-01 — a janela que para de reconciliar, e o botão morto no pacote

- **Status:** **PARCIAL — as E1 a E4 estão ENTREGUES EM CÓDIGO, AGUARDANDO A
  PALAVRA DELA; a E5 (TUI) e a E6 (bandeja) seguem ABERTAS.** Remarcada em
  09/08/2026: entraram em `cd5eaf1` (31/07/2026). **Rótulo anterior: "ABERTA —
  documento de medição e plano. Nenhuma linha de código, de teste ou de
  configuração foi tocada nesta rodada"**, preservado aqui, porque descrevia com
  exatidão a rodada de abertura. Ver a nota datada no fim
- **O que falta ela validar, em uma linha:** deixar a janela aberta por uns
  minutos com um perfil ativo e ver se ela **não troca sozinha** o que está na
  tela — e clicar em "Restaurar Padrão" para ver se ele acha o arquivo
- **Prioridade:** **ALTA** nas entregas E1 e E4 — as duas mexem no perfil dela
  sem perguntar e sem avisar. MÉDIA na E2, E3 e E5. BAIXA na E6
- **Aberta em:** 31/07/2026, a partir da auditoria de nove áreas rodada contra o
  HEAD `7bd0cb7` do ramo `restauro/inicio-da-sessao`, com o daemon
  (`hefesto-dualsense4unix.service`, PID 3615) e a janela dela
  (`python3 -m hefesto_dualsense4unix.app.main`, PID 7271, 51 min de sessão)
  **vivos e intocados** — toda a medição desta sprint é leitura de código, `git`
  e leitura do disco de perfis dela
- **Relacionada:**
  [BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md),
  que é a sprint-mãe do critério "a janela não pode dizer o que não é" — as
  entregas 5 e 6 dela seguem abertas e ficam registradas aqui como **pendência**,
  não como entrega desta sprint
- **Também relacionada:**
  [AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md)
  (a E4 fabrica um SEXTO catch-all, que é exatamente a doença daquela sprint) e
  [PERFIL-SALVA-TUDO-01](2026-07-29-PERFIL-SALVA-TUDO-01-salvei-todas-as-abas-e-so-parte-ficou.md)
  (que escreveu o `to_profile` onde a E4 mora)
- **Não confundir com**
  [CARD-OCUPA-01](2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md)
  nem com [LARGURA-01](2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md):
  aquelas duas são sobre **onde as coisas ficam na tela**. Esta é sobre **a tela
  dizer a verdade**. Nenhuma entrega daqui move um pixel de lugar

## O que esta sprint é, numa frase

São cinco defeitos com a mesma assinatura: **a janela continua desenhando com
confiança um estado que ela deixou de ter**. O perfil que ela edita pode não ser
o perfil ativo; o botão que promete restaurar o padrão não acha o arquivo fora
da máquina de desenvolvimento; o "Salvar Perfil" promete perguntar antes de
sobrescrever e não pergunta; a TUI desenha gatilho e analógico como leitura viva
sem ler nada. Mais uma faxina barata (E6) que ainda não morde, e que é melhor
pagar antes de morder.

## Antes de tudo: eu reconferi cada linha citada

Os achados vieram de outro agente. A regra desta casa é que evidência copiada
não vale — então abri **todos** os arquivos nas linhas citadas, no código de
hoje. O resultado é a tabela abaixo. **Três citações precisaram de conserto e
duas conclusões precisaram de reenquadramento**, e é por isso que a regra existe.

| Citação do achado | Confere? | O que eu encontrei hoje |
|---|---|---|
| `app.py:753`, `:764`, `:707-716`, `:718-723`, `:688-692` | **sim, todas** | exatas, linha a linha |
| `app.py:777-782` (a regra "não identifique aba por índice") | **sim** | o comentário do `_REFRESH_POR_ABA` está exatamente aí; e a regra tem um segundo lugar, `app.py:909-913`, onde ela leva o nome EST-10 |
| `status_actions.py:1269-1271` e `home_actions.py:795-797` | **sim** | os dois gates por índice estão nessas linhas |
| `footer_actions.py:36` e `:464-475` | **sim** | `_MEU_PERFIL_ASSET` e o toast de indisponível |
| `profiles/loader.py:102-105` ("três candidatos") | **corrigido** | a tupla `_DEFAULT_SEED_SOURCE_DIRS` vai de **:101 a :106**; e há mais do que a tupla — existe **`_seed_source_file(fname)` em `:113-126`**, que resolve UM arquivo pela cascata inteira e já é usado em produção (`:273`, `:414`) |
| `footer_actions.py:269-276` (conflito por nome cru) | **sim** | `_existing_names` em `:269-270`, gate `if nome in existentes` em `:273` |
| `draft_config.py:499-508` (a regra R-10) | **sim** | e o exemplo literal "Navegação"/"Navegacao" está em `:501-503` |
| `tui/app.py:151-174` | **sim** | `_tick_preview` inteiro, com o comentário `daemon.status não inclui analog ainda` em `:164` |
| `tray.py:191` e `compact_window.py:122` | **sim** | os dois `timeout_add` com o id descartado |
| `rumble_actions.py:322-326` (o precedente de cancelar timer) | **ajustado** | a função é `:322-327`; o comentário que explica o porquê é `:317-320` |
| `constants.py:34-38` | **ajustado** | o aviso é `:34-36` e `ROOT_DIR` é `:37` |
| `install.sh:1049` (instala `-e`) | **sim** | `-e "${ROOT_DIR}[${_extras}]"` está em `:1049` |
| "o .deb não embala `profiles_default`" | **REFUTADO** | `scripts/build_deb.sh:133` faz `cp -r assets/. .../usr/share/hefesto-dualsense4unix/assets/` — o `profiles_default` **vai junto**, e cai exatamente no terceiro candidato do loader |
| "morto no AppImage e no Flatpak" | **REFUTADO como causa** | `scripts/build_appimage_gui.sh:112-117` e `flatpak/br.andrefarias.Hefesto.yml:170-183` (FIX-FLATPAK-PRESET-SEED-01, de 30/07) instalam o `profiles_default` **de propósito**, no segundo candidato do loader. O botão morre mesmo assim — mas por causa do resolvedor, não do pacote |

E uma nota de método que vale para a próxima leva: as âncoras de linha do
`main.glade` **andaram** desde 29/07. A LARGURA-01 cita `profiles_paned` em
`:1481`; hoje é `:1527`. As quatro primeiras abas não se moveram
(`tab_home_box:197`, `tab_status_box:251`, `tab_triggers_box:461`,
`tab_lightbar_box:759`, `tab_rumble_box:1201`) e tudo depois de Rumble deslocou
cerca de 46 linhas. Citação de glade envelhece rápido — reconferir antes de usar.

## Onde eu me afasto do achado original, e por quê

Quatro reenquadramentos. Em cada um, o que vale é o que eu medi hoje.

1. **E1 — a cura sugerida reabriria um defeito já curado.** O achado recomenda
   "limpar `_draft_reload_for` no `_falhou` e no `_apply` com draft nulo".
   Fazer só isso reabre exatamente o que `app.py:233-237` documenta em texto:
   com um perfil ativo que não existe em disco, o tick de 2 Hz redispararia
   IPC + I/O de disco **para sempre**. E há um teste que congela isso
   (`tests/unit/test_gui_draft_reconcilia_perfil_ativo.py:126-142`). A cura tem
   de **separar** falha transitória de falha permanente — não zerar o latch.
2. **E3 — o pacote não é o culpado.** Três das quatro formas de distribuição
   acusadas **já embalam** o `assets/profiles_default`, e nos lugares certos: o
   `.deb` em `/usr/share/...` (`build_deb.sh:133`), o AppImage e o Flatpak em
   `sys.prefix/share/...` (`build_appimage_gui.sh:112-117`,
   `flatpak/br.andrefarias.Hefesto.yml:182-183`). Quem não acha o arquivo é o
   **rodapé**, que duplicou o caminho com um candidato só em vez de usar o
   resolvedor que a casa já tem. A entrega encolhe para uma troca de import — e
   a mudança de empacotamento sai do escopo.
3. **E5 — o remédio é menor do que o achado sugere.** O achado diz "alimentar
   com `daemon.state_full`, que já traz o bloco `controllers`". Medi: os campos
   estão no **topo** da resposta, não dentro de um bloco —
   `daemon/ipc_handlers.py:1405-1410` devolve `l2_raw`, `r2_raw`, `lx`, `ly`,
   `rx`, `ry`, com os mesmos nomes que `_apply_preview` já recebe. E há uma
   parte do painel que **não** mente: o `BatteryMeter` é alimentado de verdade
   (`tui/app.py:170`). Então não é "os widgets saem" — é "dois widgets passam a
   ler, um já lia".
4. **E6 — são quatro relógios, não três, e o quinto é legítimo.** Com a janela
   escondida seguem correndo os três de `status_actions.py:279-282` **mais** o
   da aba Início (`home_actions.py:790`), que gateia por página e não por
   visibilidade. O da bandeja (`tray.py:191`, a cada 3 s) **deve** continuar:
   ali há alguém olhando. E `CompactWindow.stop()` não tem **nenhum** chamador
   em produção (`grep` hoje: só a definição), o que torna aquele vazamento
   duplamente inerte.

## As decisões que eu NÃO chamo de defeito

Regra da casa: decisão registrada não é lapso. Estas três apareceram no caminho
e ficam anotadas como decisões, com o que fazer **com** elas.

- **O latch `_draft_reload_for` existir e ser separado de
  `_active_profile_name`** é decisão escrita em `app.py:233-237`, com o motivo
  medido ("um perfil ativo que não existe em disco o deixaria stale e o tick de
  2 Hz redispararia IPC + I/O para sempre"). A E1 **preserva** essa decisão e
  ataca só o caso que ela não previu.
- **`on_player_led_toggled` sem sinal no glade** é decisão medida e escrita em
  `main.glade:980-1010` (entrega 4 da BOTÃO-QUE-NÃO-MENTE-01): as caixas ficam
  porque são o único lugar onde a GUI guarda o desenho escolhido; os sinais
  saíram porque eram provadamente inalcançáveis. Sobra só limpar a entrada do
  dicionário — e isso é da entrega 5 daquela sprint, não desta.
- **`on_emulation_open_toml` órfão** idem, com a razão escrita em
  `main.glade:2478-2489`: o botão fabricava um arquivo de configuração falso no
  diretório dela e foi removido de propósito. O handler ficou. Também é da
  entrega 5 de lá.

## E1. O reload que não volta trava a janela no perfil anterior

**É o defeito R-08 de volta por uma fresta.** A reconciliação existe desde a
auditoria de 23/07 e funciona: o tick de 2 Hz vê o perfil ativo mudar por fora
(botão Ativar, bandeja, hotkey PS+D-pad, autoswitch ao abrir o jogo) e recarrega
o rascunho.

O caminho feliz está em `app/app.py:737-770`. O buraco está em três linhas:

| Onde | O que está escrito | O que isso faz |
|---|---|---|
| `app.py:764` | `self._draft_reload_for = ativo` | marca o alvo **ANTES** de disparar o worker — deliberado, o tick roda a 2 Hz |
| `app.py:753` | `if self._draft_reload_inflight or self._draft_reload_for == ativo: return` | enquanto o alvo for o mesmo, **nunca mais tenta** |
| `app.py:707-716` e `:718-723` | `_apply` só escreve `self.draft`/`_active_profile_name`/`_draft_baseline` `if draft is not None`; `_falhou` só solta o `inflight` | **nenhum dos dois limpa `_draft_reload_for`** |

E o worker devolve `(None, "")` em dois casos que ele **não distingue**
(`app.py:688-692`): quando o perfil ativo não existe em disco (permanente) e
quando `daemon_state_full()` não respondeu (transitório). O timeout dessa
chamada é de **0,25 s** e cobre conexão **e** leitura
(`app/ipc_bridge.py:45-66`, `:71`, `:173-178`).

**O que ela vê quando isso acontece:** nada. O aviso da statusbar só existe no
ramo de edição pendente (`app.py:755-762`); com o latch preso, a função retorna
em `:753` antes de qualquer toast. As abas continuam mostrando e editando o
perfil ANTERIOR, o "Salvar Perfil" vem pré-preenchido com o nome anterior
(`footer_actions.py:263-264`) e o "Aplicar" empurra as seções do perfil anterior
por cima do perfil do jogo — que é, palavra por palavra, o estrago que
`app.py:226-231` descreve como já curado.

**Quando o latch se solta sozinho:** só quando o perfil ativo virar um
**terceiro** nome. Enquanto X continuar ativo, a janela fica presa no perfil de
antes de X pelo resto da sessão.

**O caminho mais fácil de reproduzir**, sem depender de sorte de temporização: o
perfil ativo muda, o tick marca o alvo e dispara o worker, e o daemon cai ou
reinicia no mesmo segundo (é o que o botão da aba Sistema faz). O socket some, o
worker devolve `(None, "")`, o daemon volta com o mesmo perfil ativo — e a janela
nunca mais recarrega.

**A cura, e o que ela NÃO pode fazer:** não pode simplesmente zerar o latch no
caminho de falha, porque isso reabre o loop de IPC + I/O que `app.py:233-237`
documenta. Dois desenhos servem:

- **(a) prazo no latch**, como a aba Início já faz. `home_actions.py:800-839`
  tem a receita pronta e a lição escrita em `:803-810`: *"o latch `_home_inflight`
  tem PRAZO. Sem prazo, uma chamada que nunca voltou o deixava ligado para sempre
  e a aba parava de reconciliar em silêncio — foi o que fez uma reconciliação de
  2 s levar 78 s na tela."* É o mesmo defeito, no mesmo arquivo-irmão, já pago
  uma vez;
- **(b) o worker dizer qual das duas falhas foi.** `_compute_draft_from_active_profile`
  passa a devolver um terceiro valor (ou uma exceção própria) que separa "daemon
  não respondeu" de "perfil não existe em disco"; o primeiro solta o latch, o
  segundo o mantém.

A (b) é mais precisa e a (a) é mais barata; as duas juntas são o desenho honesto
— prazo como rede, distinção como regra.

**Aceite:** com o perfil ativo virando X e a leitura de estado falhando no
instante do worker, a janela **volta a tentar** e, na próxima resposta boa do
daemon, as abas passam a mostrar X. Com o perfil ativo sendo um nome que não
existe em disco, a janela tenta **uma vez** e para — sem loop de IPC.

**Mordida:** o teste tem de reprovar com a cura arrancada. Roteiro: perfil ativo
vira X, o worker devolve `(None, "")` por falha de IPC, o relógio avança além do
prazo, o tick roda de novo — **um segundo disparo tem de acontecer**. Com o
`_draft_reload_for` de hoje, não acontece, e o teste falha.

E há uma armadilha no teste que **já existe** e que precisa ser paga junto:
`tests/unit/test_gui_draft_reconcilia_perfil_ativo.py:126-142` diz no comentário
`# 5 segundos de ticks` e roda dez chamadas em sequência — que levam microssegundos
de relógio real. Uma cura por prazo passa nesse teste **sem nunca ser exercitada**.
Ou seja: o teste que hoje protege a decisão vai continuar verde e não vai medir
nada. A entrega tem de dar a ele um relógio injetável, senão a mordida some.

**Risco:** médio. Mexe no ponto onde a GUI decide qual perfil ela está editando —
o mesmo lugar onde nasceu a queixa crônica *"a config que eu deixo nunca é
respeitada"*. Não entra junto com nada; entra sozinha, e é a entrega desta sprint
com maior chance de precisar do olho dela em cima
([PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)).

## E2. Os dois relógios mais rápidos apontam para a aba pelo número dela

A casa escreveu a regra e depois a violou nos dois ticks mais quentes.

A regra, em `app/app.py:777-782`, no comentário do mapa `_REFRESH_POR_ABA`:

> *"Identificar pelo WIDGET, não pelo índice: a fusão de 'Mouse' e 'Teclado' na
> aba 'Navegação DSX' renumerou as páginas, e um mapa por índice teria passado a
> chamar o refresher errado em silêncio — sem exceção, sem log, só a aba
> mostrando dado velho."*

A mesma lição, com o nome EST-10, está em `app.py:909-913`, contando o outro
caso: um `skip` que comparava o **texto** da aba parou de casar quando "Daemon"
virou "Sistema".

E os dois gates que não seguem a regra:

| Onde | A linha | Frequência |
|---|---|---|
| `status_actions.py:1269-1271` | `if notebook is not None and notebook.get_current_page() != 1: return True` | **10 Hz** (`LIVE_POLL_INTERVAL_MS = 100`, `constants.py:41`) |
| `home_actions.py:795-797` | `if notebook is not None and notebook.get_current_page() == 0:` | a cada 2 s (`HOME_POLL_INTERVAL_MS = 2000`, `home_actions.py:49`) |

**Hoje bate por sorte.** Medido no glade de hoje: `main_notebook` em `:190`,
`tab_home_box` em `:197` (página 0) e `tab_status_box` em `:251` (página 1). A
ordem é essa desde sempre — e é a mesma ordem que já mudou uma vez, quando
"Mouse" e "Teclado" viraram uma aba só.

**O que quebra quando alguém inserir, remover ou reordenar uma aba:** o tick de
10 Hz da aba Status passa a rodar numa aba onde ele não pinta nada (ele só chama
`_sync_status_cards`, `status_actions.py:1580-1593`), saturando o executor de
**um** worker; e os cards da aba Status caem para 2 Hz. Não param: o tick lento
também sincroniza o conjunto de cards por decisão escrita em
`status_actions.py:1661-1664` (STATUS-02). Fica só visivelmente mais lento — sem
exceção, sem log, sem ninguém saber por quê. Do outro lado, a aba Início para de
reconciliar pelo tick.

**A cura já existe a setenta linhas de distância.** `_on_notebook_switch_page`
(`app.py:821-842`) desembrulha o `GtkScrolledWindow`, desembrulha o `GtkViewport`
que o GTK insere no meio, e lê `Gtk.Buildable.get_name(alvo)`. Basta extrair
isso num `_id_da_pagina_corrente()` e trocar os dois gates por comparação de id.
O desembrulho **não é opcional**: `_wrap_notebook_pages_in_scroll`
(`app.py:890-935`) envolve oito das nove páginas, então `get_nth_page` devolve o
rolador, não a página.

**Aceite:** nenhum poller da janela decide o que fazer a partir de
`get_current_page()`. Inserir uma aba nova em qualquer posição do glade não muda
o comportamento de nenhum dos dois ticks.

**Mordida:** um teste que monta o notebook com uma **aba a mais antes da
Início** e verifica que o tick de 10 Hz continua rodando na Status e o da Início
continua reconciliando na Início. Com a cura arrancada (de volta ao índice fixo),
o teste reprova nos dois. É o mesmo formato de
`tests/unit/test_notebook_switch_page.py`, que já exercita a identificação por id
e o desembrulho do rolador.

**Risco:** baixo. Não muda o que a janela desenha — muda como ela decide onde
está. Único cuidado: o teste tem de montar o notebook de verdade, porque um
dublê sem `Gtk.Buildable` responde `None` para tudo e o teste passaria com
qualquer coisa.

## E3. "Restaurar Padrão" só acha o arquivo na máquina de quem programou

O botão do rodapé resolve o asset num caminho só:

```
footer_actions.py:36
_MEU_PERFIL_ASSET = ROOT_DIR / "assets" / "profiles_default" / "meu_perfil.json"
```

`ROOT_DIR` é `Path(__file__).resolve().parents[3]` (`constants.py:37`), e o
próprio arquivo avisa, em `:34-36`: *"Em instalação real esses paths podem não
existir — sempre verifique `.exists()` antes de usar."* O rodapé verifica
(`footer_actions.py:464`) e desiste com um toast (`:465-474`).

Na máquina dela funciona porque `install.sh:1049` instala com `-e` (editável), e
aí `parents[3]` cai na raiz do repositório. Num `.deb`, o pacote vive num venv em
`/opt/hefesto-dualsense4unix/venv`, o módulo em `.../site-packages/hefesto_dualsense4unix/app/`,
e `parents[3]` vira `.../venv/lib/python3.X` — um diretório onde `assets/` nunca
existiu.

**E o asset está lá, no lugar certo, em três dos quatro pacotes.** Isto é o que o
achado original errou, e é o que muda a entrega:

| Formato | Embala `profiles_default`? | Onde | Casa com qual candidato do loader |
|---|---|---|---|
| `.deb` | **sim** | `/usr/share/hefesto-dualsense4unix/assets/profiles_default` (`build_deb.sh:133`) | o **terceiro** (`loader.py:105`) |
| AppImage | **sim** | `$APPDIR/usr/share/...` (`build_appimage_gui.sh:112-117`) | o **segundo** (`loader.py:103-104`) |
| Flatpak | **sim**, desde 30/07 | `/app/share/...` (`br.andrefarias.Hefesto.yml:182-183`, FIX-FLATPAK-PRESET-SEED-01) | o **segundo** |
| wheel puro (`pip install`) | **não** | o include do `pyproject.toml:84-91` tem só `gui/*.glade`, `gui/assets/*.png` e os `.mo` | nenhum |

Ou seja: quem instala pelo `.deb`, pelo AppImage ou pelo Flatpak **recebe os
presets** — o daemon e a GUI os semeiam por
`profiles/loader.py:129-152`. Só o botão do rodapé não os encontra, porque ele
não usa a cascata: ele duplicou o caminho com um candidato só.

**A cura é uma troca de import.** `profiles/loader.py:113-126` já expõe
internamente `_seed_source_file(fname)`, que percorre os três candidatos e
devolve o primeiro que existe — e é usado em produção em `:273` e `:414`. Promover
essa função a pública (ou publicar um `asset_de_preset(nome)`) e chamar dela no
rodapé resolve o botão em qualquer um dos três pacotes, **sem tocar em
empacotamento nenhum**.

**Aceite:** com o repositório fora do caminho (nenhum `assets/` acima do módulo)
e o preset presente em `sys.prefix/share/...` **ou** em `/usr/share/...`, o botão
"Restaurar Padrão" restaura. Sem preset em lugar nenhum, ele continua dizendo
que está indisponível — o toast de `:465-474` continua sendo a resposta honesta.

**Mordida:** o teste de hoje não morde por construção.
`tests/unit/test_footer_restore_default.py:69-72` faz `pytest.skip` quando o
asset do repositório não existe — ele só roda porque a máquina é editável. O
teste novo tem de simular a instalação empacotada: `ROOT_DIR` apontando para um
diretório sem `assets/`, um preset plantado num diretório-candidato de mentira, e
o botão restaurando. Com a cura arrancada (de volta ao `ROOT_DIR` sozinho), o
teste reprova com o toast de "asset não encontrado".

**Risco:** baixo. É trocar um caminho por uma função que já existe e já roda em
produção. O único cuidado é o teste de hoje que monkeypatcha `_MEU_PERFIL_ASSET`
como módulo-atributo (`test_footer_restore_default.py:243-246`): se o nome sumir,
esse teste quebra — a substituição precisa manter um ponto de injeção equivalente.

## E4. "Navegacao" sem acento come a "Navegação" dela sem perguntar

O rodapé promete perguntar antes de sobrescrever. O diálogo existe, o texto está
escrito — *"Perfil '%s' já existe."* (`gui_dialogs.py:92`) — e o gate que decide
se ele aparece compara **string crua**:

```
footer_actions.py:269-270   def _existing_names() -> list[str]:
                                return [p.name for p in load_all_profiles()]
footer_actions.py:273       if nome in existentes and not gui_dialogs.prompt_overwrite_existing(...)
```

Mas a identidade de um perfil em disco **não é o nome**. É o slug —
`save_profile` grava `<slugify(name)>.json` (`profiles/loader.py:606-607`), e o
`slugify` tira acento, baixa a caixa e troca espaço e traço por underscore
(`profiles/slug.py:24-36`).

A regra tem nome (R-10), data (auditoria de 23/07) e está escrita em dois lugares
do código, com o exemplo literal:

- `draft_config.py:499-505`: *"a identidade de um perfil em disco é o SLUG, não o
  nome de exibição... Comparar string crua aqui fazia 'Navegação' (no disco) e
  'Navegacao' (digitado no diálogo do rodapé) caírem no ramo 'nome novo'"*;
- `profiles/slug.py:52-71` e `:74-84`, onde `mesmo_slug` e `find_by_slug` existem
  justamente para isto, e o docstring diz que é *"a busca que as guardas da GUI e
  do CLI precisam fazer antes de gravar"*.

**Quem já usa a comparação certa:** a aba Perfis (`profiles_actions.py:977`,
`:1004`, com o comentário em `:999-1003` contando que era *"por aí que 'Novo
perfil' chamado 'Navegacao' comia a 'Navegação' dela em silêncio"*), a linha de
comando (`cli/cmd_profile.py:58`) e o próprio `to_profile`
(`draft_config.py:506-508`). **O rodapé é o último que não usa.**

**Isto não é hipótese: é o disco dela hoje.** Li os perfis dela (só leitura) —
são 15 arquivos, e cinco deles têm nome que colide por acento ou por caixa:

| Arquivo | `name` no disco | Prioridade | Regra |
|---|---|---|---|
| `navegacao.json` | **Navegação** | 50 | `window_class` + `window_title_regex` + `process_name` |
| `acao.json` | Ação | 65 | idem |
| `aventura.json` | Aventura | 70 | idem |
| `fps.json` | FPS | 60 | idem |
| `esportes.json` | Esportes | 55 | idem |

Digitar `Navegacao`, ou `navegação`, ou `fps` em minúsculas — qualquer variação
de acento ou de caixa — passa direto pelo gate e regrava o arquivo.

> **NOTA DATADA — 06/08/2026, 22:53. O NÚMERO CADUCOU; A FRASE, NÃO.**
>
> A tabela acima e o parágrafo que a segue **não se apagam**: medem um defeito
> real e são a prova de disco que sustenta a E4. O que caducou é a **contagem**,
> por três razões — e nenhuma delas é *"não havia colisão"*.
>
> **Primeiro, o sentido — para ninguém reler errado.** *"Colidir por acento ou
> caixa"* nesta casa **nunca** quis dizer um perfil colidir com OUTRO perfil.
> Quer dizer o que o parágrafo acima já explica: o `name` de exibição e o slug do
> arquivo divergem, então **uma variante digitada cai em cima do arquivo que já
> existe** — digitar `Navegacao` grava em `navegacao.json`, que é a `Navegação`
> dela. É o mesmo vocabulário de
> [JOGOS-QUE-ELA-TEM-01](2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md):390
> — *"o `slugify` faz `Navegacao` e `Navegação` caírem no mesmo `.json`"*. Par a
> par, os arquivos dela sempre tiveram slugs distintos, e isso **nunca** foi o
> que se afirmou aqui. **Quem medir "colisão par a par" vai encontrar zero e
> concluir que a frase é falsa — e vai concluir errado.** (Conferido em
> 06/08/2026, 22:53: nenhum par de perfis dela compartilha slug. GRAU: MEDIDO.)
>
> **Segundo, o número já era subcontagem em 31/07.** Pelo critério da própria
> tabela — nome de exibição cujo slug difere do nome —, `pragmata.json`
> (`Pragmata`) e `pragmata2.json` (`Pragmata2`) também divergiam por caixa e
> estavam em disco naquela semana; estão listados no
> [mapa da sessão de 29/07](../estudos/2026-07-29-mapa-da-sessao-e-o-que-os-agentes-mediram.md):85-86.
> A tabela recortou os cinco perfis **com regra de janela**, recorte legítimo
> para o que a E4 precisa mostrar; foi a frase *"cinco dos quinze"* que
> generalizou o recorte para o disco inteiro.
>
> **Terceiro, o disco dela mudou.** Medido em **06/08/2026, 22:53**, só leitura,
> com `ls ~/.config/hefesto-dualsense4unix/profiles/*.json` e o `slugify` de
> `src/hefesto_dualsense4unix/profiles/slug.py`: são **13 arquivos**, não 15.
> `pragmata2.json`, `meu_perfil.json` e `sackboy_nativo.json` **não existem
> mais** — do trio sobraram apenas três `.lock` órfãos, sem `.json` ao lado
> (`meu_perfil.json.lock`, `pragmata2.json.lock`, `sackboy_nativo.json.lock`).
> Dos 13, **nove** têm nome cujo slug difere do nome: `Ação`, `Aventura`,
> `Corrida`, `Esportes`, `FPS`, `Navegação`, `Pragmata`, `Sackboy` e `Vitoria`;
> os outros quatro já estão escritos em forma de slug (`bow`, `coop_local`,
> `fallback`, `point_and_click`). Os cinco da tabela continuam todos em disco —
> só a prioridade de `esportes.json` mudou, de 55 para **57**. **GRAU: MEDIDO em
> 06/08/2026, 22:53.**
>
> **Não trocar "cinco" por "nove" e parar por aí.** Número de disco dela
> envelhece em dias: o *"nove em treze"* vale para 06/08/2026, 22:53, e quem
> reconferir tem de escrever a data **e** o comando, como está acima.
>
> **O que NÃO caducou:** o defeito, o mecanismo, o estrago em dois tamanhos e a
> regra R-10 — que é anterior a esta tabela (auditoria de 23/07, citada logo
> acima), e não nasceu dela. E o defeito vizinho I-1 foi **curado** em 06/08:
> [NUNCA-TROCA-O-ALVO-01](2026-08-06-NUNCA-TROCA-O-ALVO-01-a-janela-trocava-o-nome-e-o-salvar-ia-para-o-arquivo-errado.md):276-306
> fez o `on_import_profile` perguntar por `find_by_slug` nas **duas** metades
> (importar **e** o nome novo do renomear), com `TestOImportarPerguntaPeloSlug`
> em `tests/unit/test_nunca_troca_o_alvo_01_o_salvar_que_mirava_outro_perfil.py:781`.
>
> **Onde a mesma frase está escrita, e que herda esta nota** (cinco lugares, não
> quatro — o quinto é a docstring que transforma a frase em teste):
> [ÍNDICE de 05/08](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md):148,
> [GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md):461,
> [SALVAR-NÃO-REBAIXA-02](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md):337,
> [estudo dos dezessete agentes](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md):103
> e `tests/unit/test_footer_actions.py:281`.
>
> **De quebra, para quem for até o ÍNDICE:** a linha imediatamente abaixo
> daquela, `:149`, carrega um segundo número caducado, e mais caro — *"o perfil
> ATIVO dela: `sackboy_nativo`, prioridade 191"*. Em 06/08/2026, 22:53,
> `sackboy_nativo.json` não existe mais (sobrou só o `.lock`), enquanto
> `~/.config/hefesto-dualsense4unix/session.json` ainda aponta
> `last_profile: sackboy_nativo` — ou seja, quem for atrás do 191 vai atrás de um
> arquivo que sumiu, e o ponteiro do perfil ativo dela está pendurado no vazio.
> **GRAU: MEDIDO em 06/08/2026, 22:53.** Aquela linha merece a sua própria nota
> datada, que esta página não pode escrever no lugar dela.

**E o estrago tem dois tamanhos.** Se o perfil ATIVO for o mesmo que está sendo
sobrescrito, `to_profile` reconhece pelo slug (`draft_config.py:506-508`) e
preserva regra, prioridade e modo: o conteúdo fica coerente, mas o `name` no
disco perde o acento e a lista da aba Perfis passa a exibir "Navegacao". Se o
perfil ativo for **outro**, `mesmo_perfil` é falso e o arquivo é regravado com
`MatchAny()` (`draft_config.py:522-526`) e com a prioridade calculada por
`_prioridade_acima_dos_catch_all` (`profiles_actions.py:1425-1439`): hoje, com os
catch-all dela em 0, 1, 5 e 5, isso dá **15**.

Ou seja: a "Navegação" dela — prioridade 50, com regra de janela e de processo —
vira um **sexto catch-all**, o de maior prioridade entre todos os catch-all do
disco. É literalmente a doença que a
[AUTOMATISMO-MORTO-01](2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md)
mediu, fabricada por um botão do rodapé, sem uma pergunta.

**A cura:** trocar `nome in existentes` por `find_by_slug(nome, perfis)` e
mostrar o diálogo com **o nome do perfil do disco**, não com o que ela digitou —
igualzinho ao que a aba Perfis já faz em `profiles_actions.py:1017`, com o
comentário ao lado: *"`alvo.name` e não `profile.name`: quem some é o perfil do
disco."*

**Aceite:** com "Navegação" em disco e "Navegacao" digitado no rodapé, o diálogo
aparece **e cita "Navegação"**. Recusando, nada é gravado. O mesmo vale para
diferença só de caixa ("fps" contra "FPS").

**Mordida:** o teste de hoje,
`tests/unit/test_footer_actions.py:227-243`, só exercita nome **idêntico**
("existente" contra "existente") — passa com a cura arrancada, então não testa
nada do R-10. O teste novo: disco com "Navegação", nome digitado "Navegacao",
diálogo recusado, e a asserção é dupla — `save_profile` **não** foi chamado, e
`prompt_overwrite_existing` recebeu `name="Navegação"`. Com o `nome in
existentes` de volta, o diálogo nunca é chamado e o `save_profile` é: reprova nas
duas.

**Risco:** baixo em código, ALTO em consequência se ficar como está. É a entrega
mais barata desta sprint e a que protege o arquivo mais exposto do disco dela.

## E5. A TUI desenha gatilho zerado e analógico centrado como se estivesse medindo

`hefesto-dualsense4unix tui` (`cli/app.py:126-131`) abre uma tela com um painel
"Gatilhos" — duas barras L2/R2, um medidor de bateria e dois mini-mapas de
analógico (`tui/app.py:129-137`). Um relógio de 10 Hz atualiza o painel
(`tui/app.py:149`), e o que ele atualiza está em `:151-174`:

```
tui/app.py:163-171
self._apply_preview(
    l2=0,  # daemon.status não inclui analog ainda
    r2=0,
    lx=128, ly=128, rx=128, ry=128,
    battery=status.get("battery_pct"),
)
```

As barras ficam em zero e os analógicos no centro **por constante**, dez vezes por
segundo, com uma conexão IPC nova a cada 100 ms (`IpcClient.connect()` por tick,
`:161`). Quem aperta o gatilho e olha a barra conclui que o gatilho não está
sendo lido.

É a "janela que mente" — a classe de defeito que a
[BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md)
existe para caçar. E o comentário no código prova que a mentira foi consciente e
ficou.

**A parte boa, e que muda o remédio:** o `BatteryMeter` do mesmo painel **é** real
— vem de `status.get("battery_pct")`. Então não é "o painel sai": é "dois widgets
passam a ler".

**E o dado existe.** `daemon.state_full` devolve os seis números no **topo** da
resposta (`daemon/ipc_handlers.py:1400-1411`): `l2_raw`, `r2_raw`, `lx`, `ly`,
`rx`, `ry` — com os mesmos nomes dos parâmetros que `_apply_preview` já aceita
(`tui/app.py:176-195`). A troca é de método e de seis argumentos.

**Aceite:** com o controle no cabo, apertar L2 na TUI move a barra L2; mover o
analógico esquerdo move o mini-mapa esquerdo. Sem daemon, os widgets ficam no
último valor lido (é o que o `except` de `:172-174` já faz) — nunca em zero
apresentado como leitura.

**Se a leitura não vier**, a alternativa escrita é remover os quatro widgets e
deixar só a bateria: é a mesma regra de "ausência é resposta" que o monitor de
microfone segue. O que **não** pode continuar é desenhar zero com cara de medida.

**Mordida:** não há hoje **nenhum** teste tocando `_tick_preview`
(`tests/unit/test_tui_app.py` cobre montagem, `q` e a barra de status). O teste
novo alimenta um cliente IPC de mentira devolvendo `l2_raw=200` e `lx=10`, roda
um tick e verifica que `TriggerBar` marca 200 e o `StickPreview` marca 10.
Com a cura arrancada (de volta aos literais), os widgets marcam 0 e 128: reprova.

**Risco:** baixo em código, médio em custo de IPC — a TUI passa de `daemon.status`
para `daemon.state_full`, que é uma resposta bem maior, dez vezes por segundo.
Vale medir o tamanho da resposta antes de fechar a entrega, e considerar baixar o
relógio da TUI para o mesmo patamar da janela quando ela não está em foco.

## E6. Os relógios continuam correndo com a janela guardada na bandeja

Duas faxinas juntas, ambas baratas, nenhuma urgente.

**(a) Os timers que ninguém remove.** `tray.py:191` e `compact_window.py:122`
criam timers periódicos e **descartam o id** devolvido por
`GLib.timeout_add_seconds`. O `AppTray.stop()` (`:288-296`) só põe o indicador em
`PASSIVE`; o `CompactWindow.stop()` (`:129-135`) só destrói a janela — e o
`_tick_refresh` dela continuaria escrevendo em rótulos de uma janela destruída.

Hoje isso é **inerte**, por duas razões medidas: `stop()` do tray só roda depois
do `Gtk.main_quit()`, numa thread que existe para o processo morrer
(`app.py:440-463`, `:481-485`); e `CompactWindow.stop()` não tem **nenhum**
chamador em produção. Vira defeito no primeiro uso de parar-e-religar em sessão
viva — por exemplo, religar a bandeja quando o `StatusNotifierWatcher` do COSMIC
aparecer depois. O padrão certo já está na casa:
`rumble_actions.py:317-327` guarda o id e chama `GLib.source_remove` no cancelamento.

**(b) Os quatro relógios que rodam com ninguém olhando.** Fechar a janela no X
não encerra: `on_window_delete_event` (`app.py:397-419`) esconde, quando há
acesso persistente (`_has_persistent_access`, `:421-438`). E ali já existe o
precedente do que fazer: a captura de microfone **é** desligada nesse ponto
(`app.py:408-410`), com a razão escrita — *"janela indo para o tray é janela sem
aba Status à vista"*.

Os pollers não receberam a mesma regra:

| Poller | Onde | Gate hoje | Muda ao esconder? |
|---|---|---|---|
| `_tick_live_state` (10 Hz) | `status_actions.py:1263-1271` | página corrente `!= 1` | **não** |
| `_tick_profile_state` (2 Hz) | `status_actions.py:1306-1319` | nenhum | **não** |
| `_tick_reconnect_state` (0,5 Hz) | `status_actions.py:1334-1347` | nenhum | **não** |
| `_tick_home_state` (0,5 Hz) | `home_actions.py:794-798` | página corrente `== 0` | **não** |

Cada chamada abre uma conexão nova e roda um `asyncio.run` próprio
(`ipc_bridge.py:45-66`). Com a janela escondida na bandeja e a aba Status como
corrente, são **12,5 chamadas IPC por segundo** contra o daemon sem ninguém
olhando; com a aba Início corrente, 3 por segundo. O relógio da bandeja
(`tray.py:191`, um a cada 3 s) **deve** continuar — ali há superfície visível.

**Aceite:** com a janela escondida, o tick de 10 Hz e os dois da aba Status
pausam; o da bandeja continua; ao reexibir pelo menu da bandeja, o header e os
cards estão em dia em menos de um segundo (uma leitura imediata no `show_window`,
no mesmo formato dos disparos one-shot de `status_actions.py:291-292`). E
`AppTray.stop()`/`CompactWindow.stop()` removem os timers que criaram.

**Mordida:** um teste que esconde a janela do dublê e conta quantas chamadas IPC
saem em N ticks — tem de ser zero para os três da Status. Com a cura arrancada,
saem N. E, para os timers: chamar `stop()` e verificar que `GLib.source_remove`
foi chamado com o id guardado; sem a cura, o id nem é guardado.

**Risco:** baixo, com um cuidado declarado: `show_window` é
`show_all()` + `present()` (`app.py:559-561`), e `show_all` reexibe widget
escondido que não tenha `no-show-all`. A linha de bateria do frame Estado é
escondida por código (`status_actions.py:1666-1671`) e **não** tem `no-show-all`
no glade (`main.glade:363-372`) — ao voltar da bandeja com dois ou mais controles
ela reaparece até o próximo tick lento. Isso é de hoje, não da entrega; mas quem
mexer no `show_window` passa perto e deve deixar registrado.

## Pendência registrada, não entrega: BOTÃO-QUE-NÃO-MENTE-01, entregas 5 e 6

Isto **não** é entrega desta sprint. Tem documento próprio
([BOTÃO-QUE-NÃO-MENTE-01](2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md),
entregas 5 e 6) e fica lá. Registro o estado remedido hoje para o próximo índice
não ter de re-derivar:

- `on_emulation_open_toml` segue registrado em `app.py:320` e implementado em
  `emulation_actions.py:449`, com **zero** ocorrências no `main.glade` e zero
  `.connect` em código. A não-fiação é decisão escrita em `main.glade:2478-2489`
  (o botão fabricava um arquivo de configuração falso no diretório dela); o que
  falta é limpar a entrada do dicionário — entrega 5, "menos superfície".
- `on_player_led_toggled` (`app.py:271`, implementado em
  `lightbar_actions.py:907`) é a segunda entrada morta da mesma família, com a
  decisão medida e escrita em `main.glade:980-1010`: os sinais saíram de
  propósito na entrega 4, e **as caixas ficam** porque são o único lugar onde a
  GUI guarda o desenho escolhido. Também é limpeza de dicionário, não de
  comportamento.
- O teste guardião só olha **uma** direção:
  `tests/unit/test_glade_signal_handlers.py:45-50` verifica que todo `handler=`
  do glade tem entrada no dicionário. Handler morto **no dicionário** passa sem
  ninguém reclamar — é o "terceiro teste, o que morde" da entrega 6, e continua
  por escrever.

## Como você valida na tela

De olho, sem terminal, com a janela maximizada. Nenhum passo aqui grava nada.

1. **O perfil que a janela acha que está editando (E1).** Abra o jogo e deixe o
   autoswitch trocar o perfil. Alt-tab para a janela, vá na aba **Perfis** e veja
   qual está em negrito. Agora, no rodapé, clique **Salvar Perfil**, **leia o
   nome que vem preenchido** e clique **Cancelar**. Os dois nomes têm de ser o
   mesmo. Se o pré-preenchido for o perfil de antes do jogo, a janela está presa
   — é o defeito da E1. (Cancelar não grava nada: `footer_actions.py:265-266`.)
2. **O mesmo, pela cor (E1).** Com o perfil do jogo ativo, a aba **Lightbar** tem
   de mostrar a cor do perfil do jogo. Se mostrar a cor do perfil anterior, a
   janela não reconciliou.
3. **A aba Status a dez por segundo (E2).** Fique na aba Status com o controle no
   cabo e mexa nos analógicos: os desenhos acompanham sem degrau. Depois, troque
   para a aba Início, volte para a Status e repita — tem de ficar igual. (Esse é
   o comportamento que a E2 protege de quebrar quando alguém mexer na ordem das
   abas.)
4. **O botão do rodapé (E3).** Na máquina dela ele **funciona** e vai continuar
   funcionando — a validação de tela aqui é só garantir que a E3 não o quebrou:
   clique **Restaurar Padrão**, confirme, e a statusbar tem de dizer
   `meu_perfil restaurado para ...`. O defeito da E3 não aparece nesta máquina;
   ele aparece em quem instalou pelo pacote.
5. **O que a E4 protege (E4).** Na aba **Perfis**, olhe a lista: existe
   **Navegação**, com acento, prioridade 50. Depois da entrega, no rodapé, clique
   **Salvar Perfil**, digite `Navegacao` sem acento e confirme: **tem de aparecer
   um diálogo dizendo que "Navegação" já existe**. Clique Cancelar. Hoje esse
   diálogo não aparece e o arquivo é regravado.
6. **A TUI (E5).** Num terminal, `hefesto-dualsense4unix tui`, controle no cabo:
   aperte L2 e olhe a barra L2. Depois da entrega ela se move. Hoje ela fica em
   zero com o gatilho no fundo.
7. **A bandeja (E6).** Feche a janela no X (ela vai para a bandeja), espere um
   minuto e reabra pelo menu da bandeja: o header e os cards têm de estar em dia
   em menos de um segundo, sem "Consultando...".

**Regra que vale para as entregas E1 e E4** — as duas que mexem em qual perfil a
janela grava: nenhuma delas vai para commit sem os passos 1, 2 e 5 feitos **por
ela, na tela**, com foto antes e depois guardada. É a
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md),
e ela é explicitamente exigida aqui.

## O que fica de fora desta sprint, por escrito

- **Mudar empacotamento.** A E3 **não** mexe no `pyproject.toml`, no
  `build_deb.sh`, no Flatpak nem no AppImage. Medido: três dos quatro já embalam
  o `profiles_default` no lugar certo. O wheel puro continua sem ele, e a decisão
  de incluí-lo (ou não) é da área de empacotamento, não desta sprint.
- **Arch, Fedora e Nix.** `grep profiles_default` nos três devolve zero, e eles
  também não instalam os glyphs. Isso não é o botão do rodapé — é semeadura de
  presets, que é defeito de outra família e de outra área. Fica anotado aqui só
  para não se perder.
- **A janela compacta (SEGUNDA-JANELA-01).** O cabeçalho do módulo
  (`compact_window.py:9-12`) descreve o gating ANTIGO (auto por default, opt-out
  por env) e o código quarenta linhas abaixo faz o contrário (`:54-58`, `:61-69`:
  opt-in, default desligado). É contradição de documentação interna, tem
  identificador próprio e não é defeito de comportamento — fica com o documento
  da SEGUNDA-JANELA-01, junto com a decisão de produto de documentar a variável
  de ambiente ou aposentar o módulo.
- **Os dois docstrings do `ipc_bridge`.** `:543-551` diz que o botão de microfone
  é "ponto de fiação deixado pronto, não fiado" — mas o botão existe
  (`controller_card.py:1362`) e o `ipc_bridge.mic_set` já é chamado em
  `controller_card.py:1397`; e `:589-593` promete um controle de volume ao lado
  do medidor que o card decidiu, por escrito, não ter. É dívida de documentação
  interna e pertence à SOM-02, que é quem decide o preço da posse do volume.
- **`_refresh_daemon_view` síncrono** (`daemon_actions.py`), duplicado do
  `_apply_daemon_view` e exercitado só por teste. É faxina de outra família
  (a aba Sistema), com risco próprio — três `subprocess` de `systemctl` com
  timeout de 5 s cada.
- **Redesenhar o painel da TUI.** A E5 faz o painel dizer a verdade. Se a TUI
  merece existir com o painel, com quais widgets e a que taxa, é conversa de
  produto — a ADR-002 aceitou o framework, não o desenho da tela.

## O que eu não medi

- **Nada foi executado contra a janela viva nem contra o daemon dela.** Zero
  cliques, zero chamadas IPC, zero `systemctl`. Todos os comportamentos descritos
  são derivados de leitura de código; nenhum foi cronometrado.
- **Com que frequência o defeito da E1 morde de verdade.** O mecanismo está
  provado no código, o gatilho (uma leitura de estado que não volta em 0,25 s) é
  certo, mas **não** medi quantas vezes por dia isso acontece na máquina dela. E
  não dá para medir pelo log: conferido hoje, o journal do usuário tem **zero**
  linhas da janela nos últimos sete dias (`apptray_started`, `gui_draft_*`,
  `draft_carregado_*`, `footer_*`: nenhuma), enquanto o daemon loga normalmente.
  O escopo `app-cosmic-hefesto-dualsense4unix-7271.scope` tem uma linha só, a de
  início: o `stderr` da janela não chega ao journal. Enquanto isso não mudar, a
  E1 só é observável **na tela**, pelos passos 1 e 2 acima — e isso, por si só,
  é um achado sobre a nossa capacidade de diagnosticar a janela.
- **O custo real de `daemon.state_full` a 10 Hz na TUI (E5).** Não medi o tamanho
  da resposta nem o tempo dela. A entrega deve medir antes de fechar.
- **O transitório do `show_all` ao voltar da bandeja.** Que a linha de bateria
  reapareça por até 500 ms com dois ou mais controles é dedução de leitura
  (`status_actions.py:1666-1671` usa `set_visible` e o glade não declara
  `no-show-all` nesses dois widgets); exigiria rodar a janela para confirmar.
- **Se algum dos gates por índice já mordeu.** Hoje a ordem das abas bate com os
  números, então o defeito da E2 é latente. Não vasculhei o histórico atrás de um
  período em que tenha estado quebrado.
- **A aba Perfis inteira.** Li os pontos que a E4 usa como precedente
  (`profiles_actions.py:955-1019`, `:1425-1439`); as outras mil e setecentas
  linhas do arquivo ficaram fora desta leitura.
- **Se o número 15 é o certo.** A prioridade que o rodapé calcula ao salvar
  (`max(catch-all) + 10`) dá 15 com o disco dela de hoje. Que 15 seja o número
  certo é decisão da PERFIL-NASCE-CERTO-01 e não foi reavaliada aqui — só medida.

---

## NOTA DATADA — 09/08/2026: quatro entregas saíram, e o "nada tocado" caducou

**Nada acima foi apagado.** A auditoria de nove áreas, o diagnóstico do reload
que não volta e as seis entregas continuam inteiros — inclusive as duas que
**ainda devem**.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **E1.** O reload que não volta trava a janela no perfil anterior | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/app/app.py:60` (o prazo do latch), `:101`, `:292` e `:852` — as quatro linhas citam `JANELA-FIEL-01/E1` por nome |
| **E2.** Os dois relógios mais rápidos apontam para a aba pelo número | ENTREGUE EM CÓDIGO, aguardando a palavra dela | mesma leva |
| **E3.** "Restaurar Padrão" só acha o arquivo na máquina de quem programou | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/app/actions/footer_actions.py:54` — o caminho deixou de ser `ROOT_DIR / "assets" / ...` |
| **E4.** "Navegacao" sem acento come a "Navegação" dela sem perguntar | ENTREGUE EM CÓDIGO, aguardando a palavra dela | mesma leva |

**Commit:** `cd5eaf1`, 31/07/2026.

### O que continua ABERTO nesta sprint — e não foi remarcado

- **E5.** A TUI desenha gatilho zerado e analógico centrado como se estivesse
  medindo.
- **E6.** Os relógios continuam correndo com a janela guardada na bandeja.

### Por que o rótulo não é ENTREGUE e sim ENTREGUE EM CÓDIGO

Porque a E1 e a E4 **mexem no perfil dela**, e a prova de que pararam de mexer
não é um teste verde: é a janela dela aberta, com os perfis dela, sem trocar
sozinha o que está na tela. Só ela pode dizer que parou.
