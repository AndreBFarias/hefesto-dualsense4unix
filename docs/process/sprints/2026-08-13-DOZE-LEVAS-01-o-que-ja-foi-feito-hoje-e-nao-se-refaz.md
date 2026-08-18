# DOZE-LEVAS-01 — o que já foi feito hoje, e não se refaz

- **Escrito em:** 13/08/2026, na branch `restauro/inicio-da-sessao`
- **Grau:** **REGISTRO DE EXECUÇÃO.** Não é plano e não é proposta: as doze
  levas **já rodaram** e estão no commit `874fdda`. Cada `caminho:linha` deste
  documento foi **reaberto na árvore de hoje**, depois do commit — a seção 6
  diz quantos e quais tiveram de ser corrigidos.
- **Por que ele existe:** a triagem que produziu estas doze levas vivia só em
  `/tmp`. Sem ela, a próxima sessão reabre trinta e um itens que já estão
  fechados, e refaz a peneira que já derrubou dez.
- **O outro documento de hoje é outra coisa:** o
  [índice da mesa cheia](2026-08-13-INDICE-a-mesa-cheia-cada-jogador-na-cor-dele.md)
  é **PLANO** — nenhuma linha dele virou código. Este aqui é o oposto: só o que
  virou. Os dois saíram do mesmo dia e não se sobrepõem em nenhum arquivo.

---

## Como ler

A ordem é a de quem chega sem contexto e precisa decidir o que fazer agora:

1. **A tabela** — o que cada leva entregou. Se o item que você ia abrir está
   aqui, ele está feito.
2. **As três quedas** — e por que nenhuma delas é "já estava feito".
3. **Os descartados** — dez itens que **documentos da casa davam como abertos e
   o código já fechara**. É a seção que evita o trabalho mais caro: o
   desnecessário.
4. **O que continua sendo dela** — dez perguntas, com o preço em minutos dela.
5. **O método** — a peneira que deixou passar, e a que rejeitou.
6. **A conferência** — a prova de que este registro não afirma o que não foi
   feito.

---

## 1. As doze levas

**90 candidatos** vindos de quatro frentes de leitura da manhã viraram **31
itens** distribuídos em 12 levas, montadas para que **dois agentes nunca
tocassem o mesmo arquivo**. Custo planejado somado: **1845 minutos** de agente,
rodados em paralelo.

**60 mordidas provadas.** Mordida, aqui, é o contrato da casa: *arranca a cura,
o teste tem de reprovar; devolve a cura, o teste volta a passar* — as duas
saídas coladas no relatório. Um teste que passa com a cura arrancada não testa
nada.

| # | leva | o que entregou | itens | mordidas | onde caiu |
|---|---|---|---|---|---|
| 1 | **O seletor que apaga a medição mais cara da casa** | O `ESTADOS` da bancada passou a conter os dois valores que o CSV já tinha em `estado_hoje` — as prosas da dose-resposta do keepalive, de 11/08. Sem isso, a primeira gravação apagava a medição feita com quatro controles na mesa | 1 | 3 | `bancada.py:116-125` · `tests/unit/test_bancada_nomeia_coluna_que_o_csv_nao_tem.py` |
| 2 | **O mapa e o caderno** | As 6 mordidas provadas em 11/08 estavam no docstring dos testes e nunca tinham chegado à coluna que o portão lê: **0 de 293 viraram 6**. O caderno ganhou `resultado_da_feature`, que o próprio portão encomendara por escrito. E peça órfã no SVG deixou de ser aviso: reprova | 3 | 7 | `docs/data/mapa-controles.csv` · `docs/data/ensaios.csv` · `scripts/gerar-mapa.py:148,178` · `scripts/check_paridade_transporte.py:226-228` |
| 3 | **O portão que acusa de dívida quem está certo** | A varredura passou a enxergar Python dentro de heredoc de shell — ela acusava de órfã uma função que o `uninstall.sh:1166` chama desde julho. E parou de ler artefato de build (18 GB, 42738 arquivos) como se fosse código | 3 | 3 | `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py:156,866,1150` · `src/hefesto_dualsense4unix/core/led_control.py:176-181` |
| 4 | **Os portões do CI** | Portão novo que exige `run` ou `uses` em todo passo dos quatro workflows e delata chave duplicada. A régua do meta-portão deixou de casar substring solta. O piso da coleta subiu de 5100 para **7850**, dimensionado contra medição. E nasceu o validador da palavra de tela | 4 | 9 | `.github/workflows/ci.yml:420` · `tests/unit/test_workflow_bem_formado.py` · `tests/unit/test_portoes_da_casa_estao_ligados_no_ci.py:224,242,279` · `scripts/validar-palavra-de-tela.py` |
| 5 | **Os três portões de shell que erravam para o lado de aprovar** | `check_anonymity.sh` era o **último portão cego a arquivo novo** — trocada a busca pela lista. Nove `produtor \| grep -q` que perdiam a corrida do SIGPIPE viraram here-string. E a régua das chamadas ficou cega a cinco chamadas reais do `install.sh` | 3 | 5 | `scripts/check_anonymity.sh:139` · `scripts/check_packaging_parity.sh` · `tests/unit/test_install_serve_os_dois_lados_da_cerca.py:212` |
| 6 | **Os testes que passavam contra um GTK de mentira** | Seis arquivos passaram de "32 verdes contra `Gtk.Box = object`" para **6 skipped honestos** sem PyGObject, e entraram no job `gtk-real`. A allowlist ganhou teto que **só desce** | 3 | 4 | `tests/conftest.py:210` · `tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py:80` |
| 7 | **As fiações de texto puro que reprovavam refactor legítimo** | Os 8 `assert <substring> in inspect.getsource(...)` saíram e viraram observação de comportamento. Hoje os três arquivos têm **zero** ocorrências | 1 | 10 | `tests/unit/test_home_autoswitch_lock_hint.py` · `test_wrapper_banner.py` · `test_gui_review_fixes.py` |
| 8 | **A taxa do rádio, e o teto que ninguém segurava** | As dez ocorrências de "~765 Hz" como taxa do rádio saíram de `src/`; sobrou **uma**, qualificada e datada, dizendo que aquilo era média de janela curta. E nasceu o primeiro código que segura `MOTION_EMIT_MAX_HZ` — o grep em `tests/` voltava vazio | 2 | 4 | `src/hefesto_dualsense4unix/core/physical_report_reader.py:37` · `tests/unit/test_teto_de_emissao.py` |
| 9 | **Os textos que mandavam fazer o errado** | O `doctor` parou de afirmar EFEITO que nunca mediu. O rodapé virou tabela que diz, por botão, se o trabalho fica salvo — **Aplicar: não**. O README do DKMS parou de ensinar `sudo bash install.sh`. E nasceu o ADR-020 | 6 | 4 | `scripts/doctor.sh:480-488` · `docs/usage/interface.md:375-380` · `src/hefesto_dualsense4unix/cli/cmd_test.py:46` · `assets/dkms/hid-nintendo/README.md:204-209` · `docs/adr/020-o-backend-deixou-de-ser-um-so.md` |
| 10 | **As fotos da versão publicada** | A aba Perfis deixou de ser casca na foto: **41.608 para 78.395 bytes**, montada sobre a mixin de produção. Portão novo compara as fotos com a versão por **topologia**, não por relógio. E a tabela dos scripts de tela passou a ter os cinco | 3 | 5 | `scripts/gui-captura/retratar_abas.py:430,674` · `docs/usage/assets/readme_perfis.png` · `docs/process/COMO-OLHAR-A-TELA.md:96-104` |
| 11 | **Os documentos que têm de ser GERADOS** | O contrato IPC publicado virou bloco gerado do dispatcher (**37 métodos, contra os 10 escritos à mão**) e a tabela de curvas saiu do catálogo. E um portão novo **abre** cada `arquivo:linha` citado em `docs/protocol/`: 122 citações conferidas, três da canônica estavam podres | 3 | 4 | `docs/protocol/ipc-unix-socket.md:42` · `docs/protocol/curvas-proprias.md:51` · `scripts/gerar-contrato-ipc.py` · `scripts/gerar-tabela-de-curvas.py` · `scripts/validar-citacoes-de-linha.py` |
| 12 | **Sob que condições os 9130 nós rodam** | Estudo, não edita nada: enumeração por leitura do fonte dos **três** consumidores do flag de fake em `src/` | 1 | 2 | `docs/process/estudos/2026-08-13-FAKE-QUE-DESVIA-01-sob-que-condicoes-os-9130-nos-rodam.md` |

**Totais:** 33 entradas em "feito", 3 em "caiu", **60 mordidas**.

> **Por que 33 entradas para 31 itens, e por que isso não é contradição.** As
> levas 3 e 6 dividiram um item em entregas separadas ao relatar — a 6 relatou
> "o lote A", "o teto que só desce" e "três frases falsas substituídas" como três
> entradas do mesmo `TESTE-HONESTO-01/E1`. **A conta que vale é a de itens: 31
> planejados, 31 fechados**, conferidos um a um na seção 6. O número 33 é de
> entradas de relatório, e está aqui só para que ninguém procure dois itens que
> não existem.

**Esta leva não é o commit inteiro.** O `874fdda` tem 100 arquivos e carrega
também o censo das dez abas, o plano da mesa cheia, o Status que dançava no
ritmo do giroscópio e o campo do jogo que aprendeu a ler endereço da Steam —
trabalho de outros agentes do mesmo dia. O que está na tabela acima é a parte
que veio destas doze levas.

---

## 2. As três quedas — e por que nenhuma é "já estava feito"

**A moldura que eu recebi dizia que três itens tinham caído por já estarem
prontos. Li os três relatórios: não é isso.** As três quedas são **afirmações
falsas da própria triagem**, derrubadas por medição na hora de executar. O
trabalho dos itens foi feito nas três.

Isso é mais valioso do que a moldura sugeria, e por um motivo prático: um item
"já feito" só custa o tempo de descobrir. **Uma contagem errada na triagem
contamina a próxima triagem**, porque ela é o documento que a próxima sessão vai
abrir.

### 2.a — "18 arquivos plantam `gi` falso" — são 17

A triagem listou `tests/unit/test_input_actions_gtk.py` entre os arquivos que
plantam stub de `gi` sem guarda. **Ele não planta stub nenhum.** A única
ocorrência de `sys.modules` no arquivo está dentro de um **comentário**, em
`tests/unit/test_input_actions_gtk.py:21`.

A triagem contou com grep de texto. O detector do próprio portão conta **por
AST** justamente para não cair nisso — e já tinha um teste de regressão nomeado
para este arquivo, `test_arquivo_real_que_so_cita_em_comentario_nao_e_acusado`.
Rodado contra a árvore, o detector devolve **17**.

**A lição, que vale para toda triagem futura:** grep conta texto, não estrutura.
Quando o número vai virar lista de trabalho, conte com a régua que o portão usa.

### 2.b — O artefato de build: o dano de TEMPO é real, o de VERDADE é latente

`P3-TARGET-01` afirmava dois danos ao portão ler `packaging/cosmic-applet/target`:
tempo e verdade. **O tempo é real e medido:** 18 GB e 42738 arquivos, os dois
medidos em 13/08/2026. **A verdade não:** nenhum arquivo sob aquela pasta
transforma lacuna em "tem porta" — `grep -rlE '^HEFESTO_[A-Z0-9_]+='` devolveu
zero linhas.

A cura foi feita mesmo assim, porque o mecanismo está provado por mordida. O que
mudou foi o **texto do portão**, que passou a distinguir os dois: não se afirma
dano que não se mediu.

### 2.c — "só `strip_quirks_token` tem chamador fora de `.py`" — são duas

A triagem disse que a frente de leitura conferira os 23 símbolos e que **só um**
tinha chamador fora de `.py`. Com a varredura ampliada, **`forbidden_reintroductions`
também tem** — e o `install.sh:1634` a chama para abortar o passo do cmdline,
dentro de um heredoc de Python.

A entrada dela na lista de isenções afirmava *"Instrumento: o docstring diz
`Guarda de teste`"* — falso do mesmo jeito. **Caíram duas entradas da lista de
isenções, não uma.**

---

## 3. Os descartados: dez itens que documentos davam como abertos

Esta é a seção que economiza mais trabalho, e é por isso que ela vem antes do
método. **Cada linha abaixo é um item que algum documento da casa dava como
aberto e que o código já tinha fechado** — ou que caiu por não ser verificável.

| o que o documento pedia | o que a árvore diz | quem estava desatualizado |
|---|---|---|
| **LIGHTBAR-DOCSTRING-01** — substituir a frase falsa "cinco dias e vinte adoções por BT sem nenhum `0x08`, e a barra continuou morta" | `cli/cmd_lightbar_reset.py:21-36` **já traz** a seção "CORREÇÃO DATADA (11/08/2026), porque a afirmação abaixo era falsa", com as quatro observações dela datadas e o texto exato que o item propunha | a frente de leitura da manhã |
| **C-2 SYSFS-NÃO-É-PROVA-01** — trocar "estado físico via classe" por "último valor escrito via classe" | `core/sysfs_leds.py:238-245` **já diz** "escrita crua por hidraw não atualiza a classe, então isto é o último valor VIA CLASSE". A nota datada completa está em `core/external_leds.py` | a frente de leitura da manhã |
| **A ONDA 1 inteira do índice de 31/07** — quinze dos dezessete itens | Todos no código: os portões `-w` viraram `-e` com o motivo escrito em `install.sh:771-775`; o metainfo abre em `<release version="0.9.4.2" date="2026-08-13">` (`flatpak/br.andrefarias.Hefesto.metainfo.xml:27`); `.github/workflows/release.yml:437` tem `needs: [build, guarda-ci]`; `uninstall.sh:451-453` chama `install_fonts.sh --remove`; `scripts/purge.sh:52,64-68` tem `--help` e sai 2 no desconhecido | [2026-07-31-INDICE-as-ondas-depois-da-auditoria.md](2026-07-31-INDICE-as-ondas-depois-da-auditoria.md) — **é o documento a corrigir** |
| **ONDA-1/1.3** — as receitas mortas de plugin no ADR-017 | `docs/adr/017-plugin-system.md:73-77` já ensina as duas rotas, e `daemon/subsystems/plugins.py` lê as duas | o mesmo índice de 31/07 |
| **ONDA-1/1.15** — o emblema de testes que defasava | `README.md:13` deixou de trazer número: `testes-mais%20de%207000`. Não há o que derivar | o mesmo índice de 31/07 |
| **CÓDIGO-MORTO-01** e **PACOTE-COM-NOME-01** | `integrations/xlib_window.py` é lápide de 41 linhas com `raise ImportError` no fim; `release.yml:272-281` grava `Hefesto-Dualsense4Unix-${VERSION}-x86_64.flatpak` | o mesmo índice de 31/07 |
| **TODO/FIXME/XXX/HACK** — 199 ocorrências | Não há dívida marcada nenhuma: as 199 são a palavra portuguesa "todo/todos". Com marcador estrito sobra **uma**, e é uma **citação** do upstream em `core/backend_pydualsense.py:9` | o grep ingênuo de quem contou |
| **ONDA-1/1.10** — o `lib.fakeSha256` em `packaging/nix/package.nix:85` | Sai por **ferramenta ausente**, não por decisão: o hash é o que o `nix` calcula, e o `nix` não existe nesta máquina. Chutar um hash é exatamente o defeito. O que dava para fazer já está feito: `tests/unit/test_purge_argumentos_e_readme_nix.py:134-166` obriga o README a avisar enquanto o placeholder existir | ninguém — é limite de máquina |
| **Oito itens marcados `so-o-documento-diz`** — PARIDADE-FORMA-01, P1-DIRETORIO-01, CONTRADICAO-0x32-01, PILHA-STEAM-1079-01, CANONICA-GRAU-01, ENSAIOS-VALIDADOR-01, GUIA-V2-01, LEITURA-QUE-FALTOU-01 | **Nenhum é falso — são NÃO VERIFICADOS.** Saíram da lista porque a triagem não abriu os arquivos citados. Quem os quiser, confirme primeiro | a própria triagem, por honestidade |
| **GATILHO-DA-COR-PAGINA-01** | Parcialmente derrubado: o apelido já aparece em `docs/process/estudos/2026-08-13-o-projeto-inteiro-num-mapa-so.md` e o módulo existe (`core/lightbar_gatilho.py`). Falta só uma página de protocolo dedicada — bem menos que "não tem página nenhuma" | a frente de leitura da manhã |

**Dois números do material de entrada foram recontados, e o segundo ensinou mais
que o próprio conserto.**

O primeiro: os ensaios observados **pelo olho dela são 73 de 77** — os outros 4
são `bancada`. Recontado hoje em `docs/data/ensaios.csv`, e continua 73/4. Numa
casa cujo caderno inteiro existe para separar **quem observou o quê**, atribuir
quatro observações de instrumento ao olho dela é o erro que o caderno foi feito
para impedir.

O segundo: a contagem de **métodos IPC sem contrato em prosa**. A triagem a
recontou em 14 contra os 18 que recebera — mas o gerador que a leva 11 escreveu
registra, em `docs/protocol/ipc-unix-socket.md:33-36`, que aquele número *"já
saiu 15, 17, 18 e 14 no mesmo dia, sem commit no meio"*. **Nenhum dos dois lados
da discussão estava certo, porque a discussão era sobre a régua.** Pela régua
que hoje está no repositório, são **18 de 37** — a coluna "Contrato em prosa" do
bloco gerado (`docs/protocol/ipc-unix-socket.md:42-88`). A lição ficou escrita no
próprio documento, e vale para além do IPC: *número que quatro réguas não
reproduzem não se escreve à mão*.

---

## 4. O que continua sendo dela

Dez itens, **200 minutos dela** somados. Não são tarefas: são perguntas. Cada
uma tem, ao lado, o que custa **depois** da resposta.

| o que ela decide | por que não é de agente | dela | depois |
|---|---|---|---|
| As sete sprints **entregue em código, aguardando a palavra dela** (ABAS-01, MIC-USB-01, PLAYER-01, STATUS-SIMETRIA-01, UI-SELETOR-01, SOM-02) e as sete parciais | PROVA-DE-TELA-01: interface só fecha com o olho dela. As fotos da leva 10 existem para que ela decida em dez minutos em vez de abrir a janela sete vezes | **30 min** | — |
| O portão P0 pula no CI, e a saída que o material oferecia está **proibida** | Versionar o `CLAUDE.md` daria CI vermelho no primeiro push: `.github/workflows/anonymity-check.yml:154-159` reprova o build se ele estiver rastreado, e `.gitignore:90` o lista. Sobra uma saída, e ela é decisão de publicar parte da lei da casa | **5 min** | 90 min |
| `stop_ipc` / `stop_udp` / `stop_autoswitch`: o `shutdown` passa a chamá-las, ou elas somem? | **Duas leituras da casa discordam com a mesma árvore na frente** — `daemon/connection.py:838-846` fechou o caso idêntico do `_stop_metrics` mandando fiar; o portão recusou, dizendo que é desenho e vale para as três juntas. Isso é pergunta, não tarefa | **5 min** | 75 min |
| O `doctor` passa a contar os checks pulados por falta de aparelho, e a relatar sanidade de perfil? | Acrescentam **saída nova** ao instrumento que ela lê justamente quando algo quebrou. Doctor que fala demais é doctor que ninguém lê | **5 min** | 145 min |
| O nome do modo do 8BitDo: `DirectInput/PS4` está errado em 23 arquivos **e tem dois sentidos** que a troca cega funde | Vocabulário de produto é dela, e há uma armadilha: `assets/dkms/hid-playstation/patch/0002-*.patch` é sobre o DualShock 4 real e o cabeçalho vai para o **upstream**. Um `sed -i` global quebra o patch. É o item com maior chance de estrago silencioso da lista | **10 min** | — |
| As 13 células `sem-mordida` que são `@sn30` e `@pro`: baixar a confiança ou esperar a bancada? | Das 18 reprovações do portão do mapa, só **cinco** são `@dualsense` e viram teste de unidade. As outras treze perguntam *"o aparelho faz isto naquele transporte?"* — baixar confiança de célula que ela mandou marcar como medida é decisão sobre o que a casa afirma saber | **10 min** | 120 min |
| O `brand_of` deixa de chamar o clone de "Sony" no cabo — mas passa a chamá-lo do quê? | A abertura está confirmada em `docs/protocol/externos-firmware-e-modos.md:236-244`, grau ALTA. Os três comentários errados de `app/actions/external_controllers.py:63,79,114` são de agente. **O rótulo que aparece no lugar de "Sony" é o que ela vê na tela** | **5 min** | 180 min |
| A tradução: os 16 módulos de `app/actions/` que escrevem string crua | O catálogo pt_BR é nativo — `_()` devolve o próprio msgid e **nada muda na tela** hoje. Um `_()` mal colocado dentro de f-string quebra rótulo em silêncio. Alto para o tamanho do ganho | **10 min** | — |
| A bancada com o controle na mão: a lightbar acendendo pelo produto com a Steam viva, o LED do mudo, os bits `flag0` um por vez, os sete modos de gatilho nunca tocados, o anel de Home do 8BitDo | Exige o controle na mão e o daemon reiniciado. A de maior retorno é a primeira: converte `luz.lightbar.cor` de MONTOU para **O APARELHO OBEDECEU** | **90 min** | — |
| Os serviços externos: PyPI, o `origin/main` 144 commits atrás, a v0.9.4 sem tag | Conta dela. Uma consequência mecânica vale citar: com `origin/main` 144 commits atrás, **worktree de agente nasce no commit errado** — isso custa tempo em toda sessão, não só no release | **30 min** | — |

---

## 5. O método: as duas peneiras

Um item só entrou nas doze levas se passou pelas **duas** perguntas. Elas não
são a mesma pergunta feita duas vezes.

**Peneira 1 — o agente consegue fazer do começo ao fim?**
Não "consegue começar". Do começo ao fim: escrever a cura, escrever o teste que
morde, arrancar a cura, ver reprovar, devolver, ver passar.

**Peneira 2 — eu consigo provar sozinha que ficou certo?**
As quatro provas que valem: `pytest`, os portões da casa, **mutação** (a
mordida), e **foto que eu leio** — a ferramenta de leitura enxerga imagem, e
isso é mais rápido e mais fiel que qualquer alternativa.

**O que a peneira 2 rejeitou, e é por isso que a seção 4 existe:**

- **precisa do olho dela** — interface não fecha sem PROVA-DE-TELA-01;
- **precisa do controle na mão** — o aparelho é dela e estava ligado; nesta
  sessão, parar o daemon, falar com o socket ou disparar rumble estava proibido;
- **é decisão de produto** — vocabulário, rótulo de tela, o que a casa afirma
  saber;
- **é serviço externo** — conta dela, `git push`, settings do GitHub.

**A regra que mais derrubou item foi a mais simples:** *se eu não abri o arquivo,
o item não entra*. Oito itens saíram por isso (seção 3, penúltima linha). Nenhum
deles é falso — e é exatamente por não saber se são falsos que eles custariam uma
leva inteira.

**E uma regra de desenho, não de mérito:** as levas foram montadas para que
**dois agentes nunca tocassem o mesmo arquivo**. Foi isso que permitiu rodar as
doze em paralelo sem conflito de árvore.

---

## 6. A conferência contra a árvore de hoje

**A triagem foi escrita contra `cc768d4`. O commit `874fdda` mexeu em 100
arquivos.** Endereço que abria de manhã podia não abrir à noite — e um registro
de execução que afirma ter feito o que não fez é pior que registro nenhum.

**Os 31 itens foram conferidos na árvore de hoje, um a um. Todos fecharam.**
Nenhum ficou aberto. As confirmações que mais valem, porque são contagem e não
leitura:

- **`mordida_provada_em`**: `csv.DictReader` sobre `docs/data/mapa-controles.csv`
  devolve **exatamente 6** células preenchidas em 293 linhas — as linhas 53, 89,
  95, 98, 149 e 281, que são as seis que a triagem nomeou. Eram **zero**.
- **`resultado_da_feature`**: presente no cabeçalho de `docs/data/ensaios.csv`.
- **`| grep -q` em `scripts/check_packaging_parity.sh`**: cinco ocorrências
  sobrevivem, e **as cinco estão em comentário** (linhas 31, 47, 51, 95 e 877).
  No código executável: zero.
- **`inspect.getsource`** nos três arquivos da leva 7: **0, 0 e 0**.
- **"~765 Hz" em `src/`**: de dez para **uma**, e a que sobrou é a linha
  qualificada de `core/physical_report_reader.py:37`, que diz que aquilo era
  média de janela curta.
- **`TETO_DA_DIVIDA = 11`** em
  `tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py:80`, com
  `exigir_gi_real` definido em `tests/conftest.py:210`.
- **`PISO=7850`** em `.github/workflows/ci.yml:420`.
- **`readme_perfis.png`**: 41.608 para 78.395 bytes no `git show --stat`.
- **O contrato IPC**: a seção "Métodos v1" de `cc768d4` tinha **10 linhas** de
  método (`git show cc768d4:docs/protocol/ipc-unix-socket.md`); o bloco gerado
  de hoje tem **37**. O "10 contra 37" da tabela da seção 1 é contado, não
  herdado da mensagem de commit.
- **Os sete portões** da lista desta sessão passam com o documento no índice.
  O `validar-citacoes-de-linha.py` conferiu 122 citações, mas **só varre
  `docs/protocol/`** — as citações deste documento não estão sob ele, e é por
  isso que a auditoria dos 43 endereços acima foi feita à mão.

**Endereços reabertos: 43. Abriram no que prometiam: 39. Corrigidos: 4.**

| endereço da triagem | endereço de hoje | o que aconteceu |
|---|---|---|
| `core/sysfs_leds.py:242-244` | **`:238-245`** | o docstring cresceu; a frase "último valor VIA CLASSE" está em `:245` |
| `install.sh:1633` | **`:1634`** | deslocou uma linha |
| `scripts/check_paridade_transporte.py:188` | **`:226-228`** | o arquivo cresceu 175 linhas **e o texto mudou**: a encomenda de 12/08 agora registra que a coluna chegou em 13/08 |
| `install.sh:618-630` | **`:771-775`** | endereço podre já na origem: 618-630 é o dono do broker, e o motivo do `-w` que virou `-e` está em 771-775 |

**Quatro endereços que pareciam podres e não eram** ficam registrados para que
ninguém os "corrija" de volta: `.github/workflows/anonymity-check.yml:154-159`
(o laço que reprova, não a lista, que está em `:145-150`), `uninstall.sh:1166`
(`kc.strip_quirks_token(tok)`), `utils/xdg_paths.py:56` (`if fake_mode_enabled():`)
e `app/actions/external_controllers.py:63`. Os quatro abrem exatamente no que a
triagem prometeu.

---

## 7. O que não foi transportado, e por quê

Para que ninguém procure:

- **Os JSON crus da triagem e do diário das levas.** O que valia deles está
  nas seções 1 a 5. O resto é cabeçalho de agente, `agentId` e repetição.
- **O texto integral das 60 mordidas.** Cada uma traz o comando, o diff da cura
  arrancada e as duas saídas — dezenas de páginas. A contagem por leva está na
  tabela; o valor de guardar era saber **que existem e quantas**, não relê-las.
- **Os `como_eu_valido` item a item.** Viraram a seção 6, que é a mesma coisa
  medida **depois** do commit, e não antes.
- **O `arquivos_que_toca` planejado**, onde ele divergiu do entregue. A tabela
  cita os arquivos **verificados na árvore**, não os previstos.
