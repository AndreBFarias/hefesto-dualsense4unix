# ÍNDICE — a casa mudou de endereço, e o rádio é a próxima parada

**21/08/2026.** Este é o índice aberto mais recente: o que o `CLAUDE.md` manda
ler antes de começar qualquer coisa. Substitui, como ponto de entrada, o
[ÍNDICE da bancada de oito horas](2026-08-16-INDICE-a-bancada-de-oito-horas.md),
que continua valendo para o que ele mediu — não foi apagado, foi ultrapassado.

O dia teve duas metades. A primeira foi infraestrutura: o repositório saiu de uma
conta pessoal, o histórico foi reescrito, o CI voltou ao verde e a 0.9.4.5 foi
republicada contendo o que faltava. A segunda chegou de fora: o desenho da
décima primeira aba, com nove sprints prontas para executar.

---

## 1. Se você tem cinco minutos

Três coisas mudaram e afetam **todo** trabalho a partir de agora:

1. **O trabalho nasce na `dev`.** A `main` só recebe no lançamento de uma
   release. As duas existem nos dois repositórios; `dev` é o ramo padrão.
2. **O repositório vive na organização `Hefesto-Team`.** Não é mais conta
   pessoal. O `upstream` local aponta para lá.
3. **O `pre-commit` global desta máquina barra segredo** — 9 regras mais um
   cofre de literais em `~/.config/git/segredos-literais`. Se você trocar a senha
   da máquina, troque lá também.

E a próxima parada de bancada está na seção 2, não na 3.

---

## 2. A PRÓXIMA PARADA — a medição do rádio, para parear o BT em definitivo

Decisão dela, 21/08: *"vamos focar na parte da medição do specs pra parearmos o
bt em definitivo"*. Esta seção existe porque a régua já está construída e o
resultado dela hoje é **zero**.

### O que já existe

Os dois instrumentos da direção de ENTRADA nasceram em `e0a5837` e são
independentes de propósito — portão em série engana, duas réguas é o que revela
quando uma olha para o lugar errado:

- `scripts/ensaios/o_jogo_segura_o_nosso_no.py` — casa por **inode**, nunca por
  caminho; identidade por `HID_PHYS` e pelo prefixo `02:fe:`, nunca por
  `vid`/`pid`, porque o vpad forja `054c:0df2` de propósito;
- `scripts/ensaios/o_jogo_no_log_do_proton.py` — a assinatura
  `HID_PHYS=hefesto-vpad` atravessa a fronteira do Wine;
- `src/…/integrations/no_do_vpad.py` mais o `state_full` — o produto passou a
  declarar **qual nó ele é** (`evdev`, `hidraw`, `inode`, `game_open`).

### O que o censo diz hoje, e é honesto

```
scripts/check_paridade_transporte.py
  graus que a suíte não sustenta sozinha...... 36
       desses, na direção de ENTRADA (o jogo). 0
  linhas que alcançam o jogo por `uhid`....... 16
       dessas, com afirmação forte............ 4
```

**Zero células preenchidas na direção de ENTRADA**, e não por preguiça. Três
travas foram medidas, e a terceira é a que interessa:

1. **A régua do log é cega ao transporte**, e o mapa é um mapa de transporte. O
   byte que responde cabo-ou-rádio está na mesma linha que ela já lê. É a
   distância mais curta entre "mede" e "preenche".
2. **Só há um log de Proton nesta máquina, e é sessão de cabo.** Sem log de
   rádio, a coluna de rádio não tem matéria-prima.
3. **As duas réguas são de NÓ, não de tecla.** Elas respondem "o jogo segura o
   nosso nó", nunca "o A chegou". Das 26 células candidatas, **22 são de tecla**
   e precisam da régua que abre o nó — que não foi construída porque abrir o nó
   dispara `UHID_OPEN`, arma o modo jogo, e fechar por último deixa o controle
   vibrando. Exige a máquina viva e um jogo aberto.

A trava 2 é a que casa com o pareamento definitivo do Bluetooth: **uma sessão de
rádio com jogo aberto produz o log que falta.**

### O procedimento de pareamento

`GUIA-RADIO-DA-SALA.md`, na raiz (376 linhas, chegou hoje). Traz inventário,
hardware, mapa das conexões, montagem, e a seção 6 — como distribuir os
controles entre vários adaptadores, tirando de um e pareando noutro **com o
cache junto**. É o roteiro para a mesa de cinco desta casa.

### Ordem sugerida para a bancada

| # | O quê | Por quê nesta ordem |
|---|---|---|
| 1 | Parear a mesa pelo `GUIA-RADIO-DA-SALA.md` | Sem os controles distribuídos, não há sessão de rádio para medir |
| 2 | Abrir um jogo **por rádio** e guardar o log do Proton | Derruba a trava 2 — é a única matéria-prima que falta para a coluna de rádio |
| 3 | Ensinar a régua do log a ler o transporte | Trava 1; o byte já está na linha que ela lê |
| 4 | Rodar `check_paridade_transporte.py` e ver o censo sair de zero | A prova de que a direção de ENTRADA fecha alguma coisa |

A trava 3 (régua de tecla) fica para depois: ela pede desenho próprio, porque
abrir o nó tem efeito colateral no controle.

---

## 3. A leva que chegou de fora — a aba Configurações

`docs/process/sprints/2026-08-21-ABA-CONFIGURACOES/`, de AndreBFarias, 20
arquivos e 5525 linhas. **Nada foi implementado** — são o desenho, as decisões e
nove sprints prontas.

**A tese, e é boa:** as dez abas de hoje operam sobre o que o produto **mede**.
Esta é onde entra o que ele **não tem como medir** e precisa que a pessoa
declare — onde o dongle está fisicamente, o que é aquele rádio vizinho, a cor do
plástico quando a leitura falha. O teste de admissão de qualquer controle novo é
uma pergunta só: *o Hefesto descobriria isso sozinho?* Se sim, o lugar não é ali.

Por onde entrar, na ordem que o próprio README declara:

| # | Arquivo | O que responde |
|---|---|---|
| 1 | `README.md` da pasta | O desenho em cinco minutos; abre o mockup |
| 2 | `COMO-EXECUTAR.md` | O roteiro sprint por sprint, com molde e prova de trabalho |
| 3 | `INDICE.md` | Por que a aba existe e por que cada decisão foi tomada |
| 4 | `DECISOES-ABERTAS.md` | As cinco perguntas de doutrina — **as cinco já respondidas em 21/08** |
| 5 | `TODO-INTEGRACAO.md` | O que depende de outra frente e as medições pendentes |
| 6 | `TOOLTIPS.md` | O texto exato de cada dica |

O desenho é autocontido e não pede rede:

```bash
xdg-open docs/process/sprints/2026-08-21-ABA-CONFIGURACOES/mockup/aba-configuracoes.html
```

### A ordem interna, e o portão

**CONFIG-01 é bloqueante.** Enquanto a décima primeira aba não abrir vazia sem
quebrar as dez existentes, nenhuma das outras oito tem onde morar.

| ID | Entrega | Bloqueada por |
|---|---|---|
| **CONFIG-01** | A aba existe e está vazia — **O PORTÃO** | nada |
| CONFIG-02 | Leitura de sysfs: adaptadores, hub, vizinhança de rádio | 01 |
| CONFIG-03 | `maquina.json`, a persistência que não é de perfil | 01 (e 02) |
| CONFIG-04 | O medidor de ocupação do rádio | 01, 02, 03 |
| CONFIG-05 | Orçamento como teto sobre as outras abas | 01, 03 |
| CONFIG-06 | Cards de controles que não são DualSense | 01, 03 |
| CONFIG-07 | A janela: escala do texto, ambiente, bandeja, autostart | 01 |
| CONFIG-09 | "Está tudo certo?" — o exame e o selo | 01, 02 |
| CONFIG-08 | A aba entra na documentação | **todas** — serial, e a última |

**CONFIG-08 é a última por medição, não por gosto:**
`tests/unit/test_as_fotos_acompanham_a_versao.py:94-116` compara topologia de
commits — o commit que toca `src/…/app` ou `src/…/gui` tem de ser ancestral do
que toca `docs/usage/assets`. As outras oito tocam `app/` ou `gui/`.

### Onde esta leva encosta na medição do rádio

**CONFIG-02 e CONFIG-04 consomem exatamente o que a bancada da seção 2 vai
produzir.** A aba precisa saber quais adaptadores existem, quem está em qual
controlador, e quanta faixa cada um ocupa. Fazer a bancada primeiro é o que
impede a aba de nascer declarando o que ninguém mediu.

---

## 4. O que este dia mudou na infraestrutura

| O quê | Antes | Depois |
|---|---|---|
| Dono do repositório | conta pessoal `AndreBFarias` | organização `Hefesto-Team` |
| Ramo padrão | `main` | `dev` |
| `main` | aberta a push direto | protegida: exige PR, sem force-push, admin pode contornar |
| Gatilhos de CI | `anonymity-check` e `flatpak` só em `main` | `main` e `dev` |
| Branches | 47 locais, 15 no seu repo, 11 na org | **2**, **2** e **3** |
| Histórico | a senha sudo em 5 commits desde 22/05 | filtrado; zero refs locais a alcançam |
| Release 0.9.4.5 | publicado 8 commits atrás do produto | regerado, contendo tudo |

**O que a reescrita NÃO resolveu, e é dela:** as refs `refs/pull/110`, `112`,
`113` e `114` na org ainda carregam os 5 commits. Ref de pull request é criada e
mantida pelo GitHub; não se apaga por push. Só sai com chamado no Suporte
pedindo garbage collection — e agora ela é admin e pode abrir.

**E o passo que de fato encerra o assunto continua aberto: trocar a senha da
máquina.** O filtro é higiene; enquanto a senha for válida, o que já foi clonado
continua servindo.

---

## 5. O que continua aberto das levas anteriores

Nada aqui foi fechado hoje. A lista existe para não se reaprender o que já
custou.

| Sprint | O que ficou |
|---|---|
| [PROVA-NO-PLASTICO-01](2026-08-19-PROVA-NO-PLASTICO-01-o-roteiro-de-quarenta-minutos-com-o-controle-na-mao.md) | O roteiro de quarenta minutos com o controle na mão; as cinco cores da piscada e o carimbo depois de um gesto seguem sem prova de plástico |
| [O-QUE-PRECISA-DE-VOCE](2026-08-19-O-QUE-PRECISA-DE-VOCE.md) | Sete itens que só ela responde, incluindo a allowlist do Steam Input e o «Parar» no Modo Nativo (este último **foi decidido e curado** em 20/08) |
| [TRES-PORTOES-01](2026-08-19-TRES-PORTOES-01-nao-anda-nem-o-microfone.md) | O mecanismo do microfone **não está fechado**; a §3.3 explica por que a explicação anterior não se sustenta |
| [JANELA-CORTADA-01](2026-08-17-JANELA-CORTADA-01-o-rodape-que-o-gtk-diz-que-cabe.md) | Duas coisas que o GTK jura que cabem e a tela dela mostra que não |
| [FOCO-ERRANTE-01](2026-08-18-FOCO-ERRANTE-01-o-x-aponta-para-a-steam-e-leva-o-perfil-junto.md) | Escrito com o defeito acontecendo durante a amostragem |

---

## 6. As armadilhas que este dia acrescentou

Três, e todas da mesma família — **o instrumento mostrou o que eu queria ver**:

1. **`grep -c` de sucesso engole erro.** Um push foi reportado como "52 refs
   atualizadas" quando o `main` tinha sido **recusado**: o comando contava as
   linhas de sucesso e descartava as de erro. Conte o código de saída, não as
   linhas bonitas.
2. **`cancelled` não é `failure`.** O build da release foi interrompido pela
   transferência do repositório, com a anotação `repository transferred`. Lido
   como falha, mandaria investigar o build — que estava certo.
3. **`grep -qP "$padrao"` sem `-e` lê padrão que começa com `-` como OPÇÃO**, e
   sai calado. A regra de chave privada do hook global passou no primeiro teste
   por isso, sem erro nenhum. Todo padrão vai com `-e`.

E uma quarta, de fluxo, que quase passou: **portão não segue o trabalho
sozinho.** Mudar o ramo de trabalho para `dev` sem tocar nos gatilhos teria
levado o dia a dia para um ramo que nenhum workflow olhava — o mesmo defeito de
27/07 (PORTÃO-VIVO-01 bloco C), ressuscitado por mudança de fluxo em vez de
mudança de código.

---

## 7. Ordem de execução, daqui para frente

1. **A bancada de rádio da seção 2** — é o que ela decidiu, e destrava a coluna
   de rádio do mapa de canais.
2. **CONFIG-01**, o portão da aba nova. Pequeno (~330 a 420 linhas) e bloqueia
   as outras oito.
3. **CONFIG-02**, que consome a leitura de rádio que a bancada tiver produzido.
4. O resto da ordem da seção 3, com `CONFIG-08` sempre por último.

O que **não** entra nesta ordem, e é decisão dela quando entrar: o microfone da
TRES-PORTOES-01, e as duas medidas de janela da JANELA-CORTADA-01.
