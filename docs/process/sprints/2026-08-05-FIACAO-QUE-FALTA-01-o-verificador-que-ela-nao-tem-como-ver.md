# FIAÇÃO-QUE-FALTA-01 — o verificador que ela não tem como ver

- **Escrita em:** 05/08/2026, depois de a leva dos perfis ser commitada
  (`c3829c7`, `2342743`, `10f4818`, `bb98278`, `4b4c7dd`) e o daemon reiniciado
- **Para quem:** agentes, em execução autônoma. Cada entrega abaixo é
  independente e traz a mordida esperada — nenhuma precisa de auditoria nova
- **Índice da faixa:**
  [a leva dos perfis que se reescreviam sozinhos](2026-08-05-INDICE-a-leva-dos-perfis-que-se-reescreviam-sozinhos.md)
- **Base factual:**
  [o sistema de perfis — o que dezessete agentes mediram](../estudos/2026-08-05-o-sistema-de-perfis-o-que-dezessete-agentes-mediram.md)

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução,
journal, teste que reprova ou `git grep` que fecha a conta; **SUSPEITA COM
MECANISMO** = o caminho de código foi lido e fecha, o efeito não foi observado;
**SEM PROVA** = está dito e ninguém verificou.

---

## O FIO QUE COSTURA TODAS AS ENTREGAS

A leva dos perfis entregou sete curas de código e um verificador que diagnostica
o estrago. **Nada disso alcança quem não abre terminal.**

> **Grau: MEDIDO**, em 05/08 às 22h40. `hefesto-dualsense4unix doctor --perfis`
> rodado contra a pasta real dela sai **1** e acusa quatro perfis que perderam a
> regra. A janela, aberta ao lado, não diz nada. Nem o daemon.

Esta sprint é a fiação. Nenhuma entrega aqui inventa mecanismo novo — todas
ligam coisa que já existe e está testada a um lugar onde ela consegue ver.

---

## E1 — O verificador aparece na janela

**Grau do defeito: MEDIDO.** `profiles/sanidade.py` tem 393 linhas e 25 casos de
teste. `git grep -n "verificar_perfis" src/` devolve o `cli/cmd_doctor.py` e
mais nada. A aba Perfis não o chama.

**É a entrega 4 da
[PERFIL-NASCE-CERTO-01](2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md)**,
que o próprio arquivo marca como PARCIALMENTE PAGA por causa disto: *"tem
detector, mas não roda sozinha"*.

**O que fazer:**

1. Um aviso na aba Perfis quando a varredura acusa algo. O vocabulário já está
   pronto e em português — cada `Achado` de `sanidade.py` traz `mensagem` e
   `cura`, e a `cura` é uma frase de ação (*"baixe a prioridade de X para 0"*,
   *"dê o alvo de volta na aba Perfis"*). **Não reescreva as frases**: elas
   foram medidas contra o disco dela.
2. A varredura roda no **worker**, nunca na thread GTK — `load_all_profiles()`
   é I/O de disco, e `profiles_actions.py:1981-1983` proíbe reler disco na
   thread da janela (PERF-GUI-PROFILE-LOAD-NONBLOCKING-01).
3. O achado **FAIL** e o **WARN** não podem ter o mesmo peso visual. Hoje o
   terminal os separa por rótulo; a janela precisa de equivalente.

**Veto:** não faça o aviso **bloquear** o salvar. A guarda que pergunta antes de
rebaixar já existe (`SALVAR-NÃO-REBAIXA-02`) e é onde essa conversa mora. Este
aviso é diagnóstico, não portão.

**A mordida:** um teste que monta a pasta de perfis da fixture
`perfis_da_corrupcao` (já existe em `tests/unit/test_profiles_sanidade.py`),
abre a aba e afirma que o texto do achado FAIL aparece. Arrancada a chamada, o
teste reprova.

---

## E2 — A receita do verificador manda fazer o que a interface simples não faz

**Grau: MEDIDO**, em 05/08. O verificador imprime, para três perfis dela:

> *"se ele é mesmo só para ativar na mão, declare `"match": {"type": "manual"}`
> e o aviso some"*

Mas o seletor **"Aplica a:"** tem exatamente sete botões
(`profiles_actions.py:110-118`): **Qualquer, Steam, Navegador, Terminal, Editor,
Jogo, Jogo da Steam**. **Não há "Só manual".** O único caminho na janela é ligar
o **Modo avançado** e deixar os três campos vazios
(`profiles_actions.py:1961-1969`) — o que não é descobrível, e cuja aparência é
a de um formulário incompleto.

Pior: a coluna "Quando usar" **já sabe dizer** `"Só manual (nunca ativa
sozinho)"` (`_MATCH_LABELS`, `profiles_actions.py:152`). A janela lê o estado e
não o oferece.

**O que fazer:** um oitavo item no `_APLICA_A_ITEMS`, com o rótulo que a coluna
já usa. `from_simple_choice` (`profiles/simple_match.py:77`) precisa aprender a
chave, e `detect_simple_preset` (`:114`) a devolvê-la — hoje ela devolve `None`
para `MatchManual` de propósito, e essa decisão **caduca aqui**, com nota
datada.

**Cuidado medido:** `schema.py:127-129` avisa que `{"type":"manual"}` é
rejeitado por binário antigo. Não é exposição nova (o editor avançado e
`profile create --manual` já gravam), mas a nota tem de constar.

**A mordida:** escolher o item novo e salvar grava `match.type == "manual"`;
reabrir o perfil traz o item selecionado (o round-trip, que é onde
`detect_simple_preset` morde).

---

## E3 — Duas sprints cujo CÓDIGO já está commitado e a página não existe

**Grau: MEDIDO** por `git log` e `git grep`.

### E3a — `REGRA-NÃO-SE-PERDE-02`

Código em `c3829c7`. `footer_actions._regra_do_save` é uma escada de três
degraus (disco > fotografia > órfão), o predicado do degrau 2 é **estrutural**
(`e_catch_all`, não `isinstance`), e o ramo órfão nasce `MatchManual()`.
Nove testes em `tests/unit/test_regra_nao_se_perde_02_o_nome_novo_nascia_sem_regra.py`,
com seis mutações verificadas.

O índice já traz o desenho na seção *"REGRA-NÃO-SE-PERDE-02 — a próxima sprint a
escrever"* — **a página é transcrição, não pesquisa**. O que ela precisa
registrar e o índice não registra: que `test_perfil_novo_pelo_rodape_continua_nascendo_sempre`
foi **reescrito no lugar** (premissa que valeu de 23/07 a 05/08), e que duas
docstrings do arquivo do funil caducaram sem o código mudar.

### E3b — `UNIFICA-PREDICADO-01` (o `steam_app_`)

Código em `10f4818`. Cinco implementações viraram uma, em
`profiles/steam_app.py`. A página precisa registrar, porque **nada no código
conta isto**:

- a ordem importou e está provada: arrancada a `IGNORECASE` da fonte, o veto
  R-21 cai em três testes e o catch-all volta a entrar no jogo;
- a fonte desceu para `profiles/` **para não fechar um ciclo que estava a um
  commit de distância** (`profiles.simple_match → daemon.launch_env →
  profiles.manager → daemon.state_store → daemon.launch_env`);
- dois callsites que nenhum levantamento tinha achado (`launch_env.py:763,794`);
- o defeito extra, não procurado: `_detect_steam_appid` era sensível a caixa, e
  um perfil salvo como `Steam_App_2111190` — que **casa com o jogo** — abria no
  editor avançado com o campo do número da loja vazio;
- o efeito colateral registrado: appid com zero à esquerda normaliza no
  round-trip por `int`.

---

## E4 — As três lacunas de teste

Ordem recomendada **3 → 2 → 1** (da mais barata à que exige decisão).

### E4.3 — `_reject_traversal` nos caminhos de ESCRITA

**Grau: MEDIDO.** Os seis casos existentes (`tests/unit/test_profile_loader.py:245-275`)
passam **todos por caminhos de LEITURA**. Os dois chamadores novos
(`historico_dir`, `_slug_para_historico`) abrem três caminhos de escrita sem
nenhum caso. É a única barreira entre um nome de perfil e uma escrita fora de
`profiles/`.

### E4.2 — `_conferir_invariante_de_gravacao` sem mordida, e feito de `assert`

**Grau: MEDIDO.** Roda em todos os testes do funil e **nenhum prova que ele
morde** — não há caso que viole a invariante e espere `AssertionError`.
Agravante: são `assert` puros, que **somem sob `python -O`**. A invariante
central do módulo não tem guarda executável em produção.

**Decisão a tomar na sprint** (e é decisão, não conserto): virar exceção de
verdade, ou aceitar que é rede de teste e dizer isso na docstring. Não deixe
como está — hoje o texto promete produção e entrega teste.

### E4.1 — `sanidade.verificar_perfis_do_disco()` nasceu morta

**Grau: MEDIDO.** Exportada em `__all__`, **zero chamadores em `src/`**, **zero
testes**. O `cmd_doctor` monta o par `load_all_profiles()` + `verificar_perfis()`
à mão em vez de usá-la. É a forma exata que a
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
cataloga.

**A E1 desta sprint é a chance de resolver isto de graça:** se a janela chamar
`verificar_perfis_do_disco()`, ela deixa de ser morta. Se a E1 escolher outro
caminho, então a função **sai** — não fica exportada sem dono.

---

## E5 — O `README.md`

**Grau: MEDIDO** por `grep`. `profile historico`, `profile restore [--em]` e
`doctor --perfis` entraram em `docs/usage/cli.md` em 05/08 e **continuam sem
menção no `README.md`**. Classe DOC-VERDADE-01.

---

## E6 — O aviso que nomeia um travessão

**Grau: MEDIDO**, e foi a foto que revelou —
`docs/usage/assets/dialogos/dialogo_descarta_edicao_pendente_sem_nome.png`.

Com `editando=None`, `confirm_discard_pending_edits` (`app/gui_dialogs.py:228-232`)
usa `editando or "—"` e a frase sai:

> *"As abas mostram alterações de **'—'** que você ainda não salvou."*

**O que fazer:** uma segunda frase para o caso sem nome, não um travessão no meio
da sentença. **Isto é texto de interface: a palavra final é dela**, e a foto tem
de ser refeita e mostrada depois da mudança (`retratar_dialogos.py`).

---

## E7 — A cura de SEGURANÇA do Bluetooth não está na máquina dela

**Grau: MEDIDO**, em 05/08 às 22h30, lendo o arquivo do sistema.

`/etc/bluetooth/main.conf:25` diz `JustWorksRepairing=always`. O repositório diz
`confirm` desde a
[RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md),
e **isso nunca foi instalado**. `/etc/bluetooth/main.conf.d/` não existe nesta
máquina, então o install usa o caminho do bloco em `main.conf`.

**O que fazer:** `bash install.sh --yes` — **nunca com `sudo` na frente** (o
`HOME` vira `/root`; regra do `CLAUDE.md`). Vale no **próximo boot**: o install
deliberadamente **não reinicia o `bluetoothd`**, porque isso derrubaria os
controles conectados.

**Também pendentes no install:** o applet COSMIC (o `packaging/cosmic-applet/src/ipc.rs`
mudou e precisa recompilar) e os dois scripts de BT.

**Veto:** não rode o install sem a palavra dela. Ele mexe em `/etc` com `sudo`, e
o `bluetoothd` guarda os bonds dos controles dela.

---

## O QUE ESTA SPRINT NÃO COBRE — e é decisão, não esquecimento

**Os perfis corrompidos dela.** Quatro perfis perderam a regra, e o conserto é
**dela, na janela** — está escrito na seção *"O estrago que ficou no disco dela"*
do índice da faixa, com os três caminhos e o motivo de o terceiro ser o único
honesto. Um agente **não deve** editar os arquivos de perfil dela: adivinhar a
regra pelo nome é inventar configuração dela, que é a raiz da queixa original.

**A prova de tela dos três diálogos novos.** As cinco fotos existem e estão em
`docs/usage/interface.md`. O aceite da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
é dela e de mais ninguém.

---

## COMO EXECUTAR

Ordem sugerida, por dependência real:

1. **E3a e E3b** — páginas de código já commitado. Independentes, paralelizáveis,
   e são transcrição: baratas.
2. **E4.3** — a lacuna mais barata e a de maior risco de segurança.
3. **E2** — o item "Só manual" no seletor. Independente do resto.
4. **E1** — o verificador na janela. **Decide o destino da E4.1**, então vem
   antes dela.
5. **E4.1** — ligar ou remover, conforme a E1 tiver decidido.
6. **E4.2** — a decisão sobre o `assert`.
7. **E5** — o `README.md`.
8. **E6 e E7** — dependem da palavra dela, e não da nossa.

Antes de fechar qualquer leva, o bloco do `CLAUDE.md`, **depois** do `git add -A`
(os portões são cegos a arquivo novo). Linha de base em 05/08: **7017 passed,
1 skipped**.

**Nada de emoji em documento nenhum** — o sanitizer do pre-commit bloqueia
U+2713/U+2717, e o `validar-glifos.py --all` **não** pega isso. Foi o que
reprovou um commit desta leva.
