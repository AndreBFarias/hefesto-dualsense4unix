# DIÁLOGO-QUE-MATA-A-JANELA-01 — o aviso que deixou a janela dela morta

- **Achado em:** 06/08/2026, às 20h22, **com ela na frente da tela**, no gesto
  que o próprio doctor desta casa recomenda
- **Estado:** **CURA APLICADA**, com sete mordidas verificadas uma a uma
  (06/08, neste documento)
- **Gravidade:** **MÁXIMA** — a janela inteira parou de responder, e o defeito
  é **nosso, de hoje**: o diálogo que travou nasceu na
  [SALVAR-NÃO-REBAIXA-02](2026-08-05-SALVAR-NAO-REBAIXA-02-o-novo-perfil-desligava-as-proprias-guardas.md),
  commitada nesta mesma leva
- **Causa:** **MEDIDA** na parte que prende (o laço modal, pela pilha do
  `py-spy`); **SUSPEITA COM MECANISMO** na parte que esconde (o diálogo que
  nasce sem foco sob o `cosmic-comp`)
- **Alcance:** **dez diálogos bloqueantes** em `app/`, não um
- **Veto respeitado:** o aviso **não** foi removido. Baixar prioridade em
  silêncio já custou configuração dela; o defeito é ele **estrangular** a
  janela, não ele existir

---

## O sintoma, na língua dela

> *"interface travou legal aqui. nem consigo fazer nada nem fechar"*

Ela estava consertando os perfis pela aba Perfis, baixando a prioridade do
perfil **"Vitória"** de **78 para 0**. Clicou em Salvar. A janela ficou lá,
desenhada, inteira, na aba Perfis, com o editor preenchido — e **surda**.
Nenhum clique respondia. Nem o fechar.

A captura de tela dela, tirada no mesmo minuto, mostra a janela principal
**e nenhum diálogo por cima**.

## A pilha, capturada ao vivo

`py-spy` (leitura pura, `sudo`), PID **3878063**:

```
Thread 3878063 (idle): "MainThread"
    run (gi/overrides/Gtk.py:574)                              <- PARADO AQUI
    confirm_downgrade_priority (hefesto_dualsense4unix/app/gui_dialogs.py:193)
    on_profile_save (hefesto_dualsense4unix/app/actions/profiles_actions.py:1621)
    main (gi/overrides/Gtk.py:1694)
    run (hefesto_dualsense4unix/app/app.py:1256)
    main (hefesto_dualsense4unix/app/main.py:202)
```

Estado do processo antes de ser morto: thread principal em
`poll_schedule_timeout` (**o laço do GTK VIVO**), três threads em
`futex_do_wait` (workers, normal), **1,4% de CPU**.

**Isto exclui a explicação óbvia.** Não era travamento de syscall, não era
D-state, não era o daemon. O processo estava **dentro do `dialog.run()`**,
esperando uma resposta que ela **não tinha como dar**, porque o diálogo não
estava visível para ela.

## A causa: são DUAS coisas somadas

### 1. O que ESCONDE — `gtk_dialog_run()` não presenteia

`gtk_dialog_run()` faz `gtk_widget_show()` no diálogo e entra num laço próprio.
Ele **não** chama `gtk_window_present()` — nunca pede levantamento nem foco ao
compositor. Num gerenciador de janelas maduro, um diálogo transiente e modal é
levantado e focado de graça, e ninguém nota a diferença. Sob o `cosmic-comp`
com XWayland, essa gentileza não é garantida.

**Grau: SUSPEITA COM MECANISMO.** O mecanismo está lido no fonte do GTK e o
sintoma bate exatamente (janela viva, diálogo em laço, nada na tela). Não
reproduzi o COSMIC em bancada — e não invento que reproduzi.

### 2. O que PRENDE — `modal=True` mais laço aninhado

Com `modal=True`, o GTK põe um grab: todo evento de ponteiro e teclado da
aplicação vai para o diálogo. Se o diálogo é invisível **e** sem foco, o grab
existe e não tem dono alcançável — cada clique dela é engolido, e o botão de
fechar da janela principal também. **Grau: MEDIDO** (é o que a pilha mostra).

Uma sozinha não mata: um diálogo invisível **com foco** ainda aceita `Esc`; um
diálogo visível **sem** modalidade não prende nada. Somadas, matam a janela.

## O alcance: dez, não um

O `confirm_downgrade_priority` foi o que a derrubou, mas o defeito é de CLASSE.
Levantados por AST em `src/hefesto_dualsense4unix/app/`:

| Onde | Diálogo |
| --- | --- |
| `gui_dialogs.py` | `prompt_profile_name` |
| `gui_dialogs.py` | `prompt_overwrite_existing` |
| `gui_dialogs.py` | `confirm_downgrade_match_to_any` |
| `gui_dialogs.py` | **`confirm_downgrade_priority`** (o desta sprint) |
| `gui_dialogs.py` | `confirm_discard_pending_edits` |
| `gui_dialogs.py` | `prompt_import_conflict` |
| `gui_dialogs.py` | `confirm_restore_default` |
| `gui_dialogs.py` | `confirm_delete_profile` |
| `gui_dialogs.py` | `show_external_controller` |
| `actions/profiles_actions.py` | `dialogo_renomear_ou_copiar` |
| `actions/footer_actions.py` | o `Gtk.FileChooserDialog` do Importar |

São **onze `.run()`**: dez avisos e um seletor de arquivo. **Todos** podiam
deixar a janela morta pelo mesmo caminho; a diferença é que só um deles ela
usou hoje.

## O agravante: a receita do próprio doctor leva ao gesto que trava

`profiles/sanidade.py` — o verificador que esta casa escreveu para ajudá-la a
consertar os perfis — diz, com todas as letras:

> *"baixe a prioridade de 'vitoria' para 0 (é o fundo de escala, o lugar de
> quem vale quando nada mais vale)"*

E o exemplo do cabeçalho do módulo é literalmente `vitoria` **(catch-all,
prioridade 100) vencendo `pragmata`**. Ou seja: **a casa mandou ela fazer
exatamente o gesto que mata a janela**, e o aviso que existe para protegê-la de
perder configuração é o que a deixou sem interface. Remédio pior que a doença,
prescrito por nós.

Some-se o histórico: `BUG-GUI-IGNORES-SIGTERM-DURING-DIALOG-01` (`app.py:192`)
já dizia que diálogo modal é perigoso, e
`BUG-DIALOG-RUN-BLOQUEIA-GTK-MAINLOOP-01` (`daemon_actions._show_restart_error`)
já tinha convertido **um** diálogo para o padrão não-bloqueante. **A lição
existia e não virou regra** — nada impedia o décimo primeiro `run()` cru de
nascer ontem. Agora impede: há portão.

## A cura

Um **envelope único**, `gui_dialogs.executar_dialogo(dialog, nome=...)`, por
onde passam os onze. Quatro camadas, e cada uma tem endereço no defeito:

1. **Mostrar de verdade.** `show_all()` + `present()` **antes** do laço — o
   pedido de levantar e focar que o `gtk_dialog_run()` não faz. Ataca a
   causa (1);
2. **Vigia com socorro e desistência.** Aos **1,5 s**, se o diálogo está
   inalcançável, tenta o resgate (`deiconify` + `show_all` + `present` +
   `keep_above`). Aos **2 s** seguintes, se continua inalcançável, **solta a
   modalidade** e responde por ela com **CANCELAR**. Ataca a causa (2);
3. **O critério é o FOCO, não os pixels.** Está MEDIDO (06/08, Xvfb, GTK 3.24,
   PyGObject 3.48) que as perguntas óbvias **mentem**: com o `GdkWindow` do
   diálogo retirado do servidor, `get_mapped()` e `get_visible()` continuam
   respondendo `True`. Quem diz a verdade é `get_window().is_visible()` e
   `is_active()`. E foco é o critério **certo**, não uma aproximação: sem foco
   ela não tem nem o `Esc`, que é a saída padrão de todo `GtkDialog`;
4. **A trava do "já foi visto" vale para o FOCO, nunca para a TELA.** Um
   Alt+Tab dela não pode virar cancelamento; mas um diálogo que **sumiu** do
   servidor estrangula a janela mesmo tendo aparecido um segundo antes, e aí
   nenhum histórico salva.

**Por que CANCELAR é a resposta de socorro.** Em todos os onze, cancelar é o
lado que **não muda nada**. O aviso continua existindo (é veto); o que muda é
que um aviso invisível deixa de custar a sessão inteira. Ela reclica "Salvar" e
nada foi perdido — e a barra passa a dizer *"O aviso não conseguiu aparecer na
tela — nada foi alterado"* em vez de um `"Operação cancelada."` seco que a
mandaria procurar um clique que ela não deu.

**A segunda saída, independente do diagnóstico.** `show_window` (o handler de
`SIGUSR1`) passou a levantar também o diálogo em curso, não só a janela
principal — que é justamente a que está sob o grab. Está MEDIDO que
`GLib.idle_add` e `GLib.timeout_add` **rodam dentro do laço aninhado do
`run()`** (e é isso que torna o vigia possível), então um `kill -USR1 <pid>` de
fora alcança um diálogo perdido mesmo com a janela travada.

### Por que NÃO o óbvio — trocar tudo por `connect("response")`

É o padrão que `daemon_actions._show_restart_error` já usa, e **ele não
resolveria este defeito**: o que prende a janela é o `modal=True`, não o laço.
Um diálogo modal invisível e não-bloqueante estrangula igual. E o custo seria
alto no lugar errado: os três avisos vivem no meio de `on_profile_save`, uma
transação com seis saídas antecipadas (sobrescrita, rename, delete do antigo,
migração do marker do daemon) — parti-la em continuações para curar um defeito
de **janela** é convidar um defeito de **dado**. O envelope cura os onze de uma
vez, sem tocar em transação nenhuma.

## Cura -> teste, com a mordida de cada um

Todos em `tests/unit/test_dialogo_nao_mata_a_janela.py`. As três testemunhas de
GTK real rodam sob `xvfb-run`, **num subprocesso** — não é preciosismo: o
envelope chama `present()` num toplevel de verdade, e um teste que fizesse isso
no processo do `pytest` abriria uma janela **na tela dela**. O subprocesso é
também o que dá a mordida principal: sem o vigia, o `run()` nunca retorna, o
prazo estoura e o teste reprova com a frase do defeito.

| Cura | Testemunha | Mordida verificada em 06/08 |
| --- | --- | --- |
| o vigia (socorro + desistência) | `test_a_janela_volta_para_ela_quando_o_dialogo_nao_pode_aparecer` | arrancado o `_agendar(PRAZO_ATE_O_SOCORRO_MS, ...)`: **2 vermelhos**, um deles por **estouro de prazo de 30 s** — o estrangulamento reproduzido |
| o socorro PRESENTEIA (não só loga) | `test_o_socorro_ressuscita_o_dialogo_em_vez_de_cancelar` | arrancado o `deiconify/show_all/present` do socorro: **1 vermelho** (*"o socorro não trouxe o diálogo de volta"*) |
| o critério pergunta ao `GdkWindow` | `test_a_janela_volta_...` + `test_o_socorro_ressuscita_...` | trocado `get_window().is_visible()` pelo mentiroso `get_visible()`: **2 vermelhos**, um por estouro de prazo |
| o critério não cancela quem está visível | `test_o_dialogo_nasce_visivel_focado_e_com_pai_transiente` + `test_o_socorro_ressuscita_...` | forçado `dialogo_alcancavel` a `False`: **2 vermelhos** — o "remédio que cancela tudo" não passa |
| o pai transiente | `test_o_dialogo_nasce_visivel_focado_e_com_pai_transiente` | removido o `parent=parent` do `confirm_downgrade_priority`: **1 vermelho** (`transiente_e_o_pai`) |
| o portão da classe | `test_nenhum_dialogo_bloqueante_fora_do_envelope_da_casa` | criado, e apagado em seguida, um arquivo novo em `app/actions/` com `dialog.run()` cru: **1 vermelho**, apontando arquivo, função e linha |
| a cobertura dos onze | `test_todo_dialogo_publico_da_casa_passa_pelo_envelope` | devolvido **um** diálogo (`confirm_delete_profile`) ao `run()` cru: **2 vermelhos** (o portão por AST **e** o espelho por função) |

Tudo devolvido ao lugar: **7 verdes**.

O portão segue o idioma da casa (precedente:
[GRAVA-POR-UM-FUNIL-01](2026-08-04-GRAVA-POR-UM-FUNIL-01-o-rodape-gravava-e-o-rascunho-nao-ficava-sabendo.md)):
lista de autorizados que **só encolhe**, travada por um teste próprio. Hoje ela
tem **três** entradas, e **nenhuma é diálogo** — os dois `app.run()` são o laço
principal do GTK, e o `executar_dialogo` é o envelope.

## As fotos

`scripts/gui-captura/retratar_dialogos.py` continua entregando os **cinco**
estados depois da mudança, com as **mesmas dimensões** de antes
(704x137, 696x137, 696x158, 710x137, 669x137) — a cura **não mexeu na forma dos
diálogos**, então as imagens de `docs/usage/assets/dialogos/` não foram
regravadas (regravar só produziria ruído binário).

A pergunta que faltava responder era o `show_all()` que o envelope acrescentou:
num `Gtk.MessageDialog` ele poderia revelar algum filho que o GTK deixa
escondido. **MEDIDO em 06/08 (Xvfb):** o diálogo de rebaixamento mede
**560x164 com e sem** o `show_all()`, com os **mesmos 13 widgets visíveis** e
nenhuma diferença de visibilidade. O envelope mostra o mesmo diálogo — só que
agora ele também é levantado e focado.

O script mudou de ponto de troca, e a mudança é o que **mantém a rota segura**:
ele trocava `Gtk.MessageDialog.run`, e a segurança dele dependia de um detalhe
do GTK (quem mostra o diálogo é o próprio `run()`). Desde a cura, quem mostra é
o envelope — trocar só o `run()` faria o script **abrir janela de verdade na
tela dela**. Agora ele troca `gui_dialogs.executar_dialogo`, e nada é mostrado.

## O que fica ABERTO

- **a causa (1) segue SUSPEITA COM MECANISMO.** Provar que o `cosmic-comp` não
  levanta/foca um diálogo transiente apenas mostrado exige medir na sessão
  dela, com o produto na mão — e a única testemunha que temos é a foto de tela
  de 06/08. A cura não depende dessa prova (a camada 2 pega qualquer causa que
  produza o mesmo estado), mas **o registro não pode fingir que a prova
  existe**;
- **`app.py:192` diz uma coisa que a medição de hoje contradiz.** O comentário
  do `BUG-GUI-IGNORES-SIGTERM-DURING-DIALOG-01` afirma que, com um diálogo
  modal aberto, *"o GLib mainloop não processa idle callbacks"*. **MEDIDO em
  06/08/2026: processa.** `gtk_dialog_run` roda um `GMainLoop` aninhado no
  contexto padrão, e tanto `idle_add` quanto `timeout_add` executam lá dentro —
  é exatamente o que o vigia usa. As três defesas de sinal daquele bloco
  continuam certas e **não foram mexidas** (nenhuma delas depende da frase
  errada); a nota fica aqui, datada, para quem for reescrever aquele bloco;
- **o `retratar_dialogos.py` fotografa cinco diálogos de onze.** Os seis
  restantes (`prompt_profile_name`, `prompt_overwrite_existing`,
  `prompt_import_conflict`, `confirm_restore_default`, `confirm_delete_profile`,
  `show_external_controller`) **nunca foram vistos**, e o aceite da
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
  segue em aberto para eles;
- **o prazo de 3,5 s é escolhido, não medido.** 1,5 s até o socorro e 2 s até
  desistir são folga generosa sobre o tempo de mapeamento de qualquer
  compositor — mas ninguém mediu o pior caso sob carga. Se um dia um diálogo
  legítimo demorar mais que isso para aparecer, ela vê um cancelamento que não
  pediu (e nada é perdido, porque a resposta de socorro não muda nada);
- **o vigia julga UMA vez, nos primeiros ~3,5 s, e depois se cala.** Um
  diálogo que aparece direito e SOME depois — o compositor o retira, ou algo
  o desmapeia — volta a prender a janela, e aí só a saída externa
  (`kill -USR1`) a devolve. A escolha é deliberada e o motivo é concreto: sob
  X11 **trocar de área de trabalho desmapeia a janela**, e um vigia permanente
  leria isso como estrangulamento e cancelaria o diálogo pelas costas dela.
  Entre errar cancelando e errar deixando passar, esta casa escolheu o segundo
  — mas **é um erro conhecido, e está escrito**;
- **a janela ainda pode ser presa por um diálogo de FORA do `app/`.** O portão
  varre `src/hefesto_dualsense4unix/app/`; um `run()` cru dentro de
  `packaging/` ou de um script de captura não é visto por ele. Nenhum existe
  hoje.
