# AGORA E DEPOIS — o plano executável da separação dos dois tempos

- **Escrito em:** 08/08/2026, noite, na branch `restauro/inicio-da-sessao`
- **Para quem:** quem for executar **sem ter vivido a sessão de 08/08**. Este
  arquivo é autossuficiente: tudo o que você precisa saber está aqui ou apontado
  com `caminho:linha`
- **O que ele resolve:** cinco dos oito defeitos da
  [OITO-DEFEITOS-01](2026-08-08-OITO-DEFEITOS-01-a-fila-que-a-verificacao-adversarial-derrubou-inteira.md),
  **por construção** — não por remendo
- **Grau:** o diagnóstico é **MEDIDO**; o desenho é **DECISÃO DELA**, aprovada em
  08/08; a execução ainda **não começou**

> **ANTES DE COMEÇAR, LEIA A SEÇÃO 6.** Ela tem oito fatos medidos que, se você
> não souber, farão você escrever uma cura que já foi escrita e revertida hoje.

---

## 1. O problema, em uma página

A janela mistura **dois tempos verbais** na mesma tela, com a mesma aparência:

| tempo | o que é | dono | quando vale |
|---|---|---|---|
| **AGORA** | cor, brilho, gatilho, vibração, microfone | o daemon | na hora — ela mexe e sente |
| **DEPOIS** | o modo e a máscara | **ela** | só quando o jogo **abre** |

Os dois são seletores lado a lado, na aba Início. Parecem iguais e **não são**:

**O jogo lê a configuração UMA VEZ, na abertura.** O wrapper termina em
`exec env "$@"` (`assets/hefesto-launch.sh:320`) — as variáveis entram no
processo e ficam. Mudar depois não alcança o jogo em curso, e mexer no
grab/vpad ao vivo invalida os handles que ele já abriu.

**Todo defeito desta noite nasceu de tentar aplicar o DEPOIS como se fosse
AGORA.** Em 08/08 isso custou, na máquina dela: uma partida sem controle nenhum,
um "Jogador 3" fantasma, e três curas revertidas.

---

## 2. O desenho aprovado

A aba Início se divide em **duas caixas com nomes diferentes**:

```
┌─ Agora ─────────────────────────────────────────────┐
│  (o que está valendo — vindo do daemon, só leitura) │
│  Controle 1 — P1 · USB · 85%                        │
│  Controle 2 — P2 · USB · 75%                        │
│  [ Reconciliar jogadores ]                          │
└─────────────────────────────────────────────────────┘

┌─ Quando o jogo abrir ───────────────────────────────┐
│  O que o controle faz agora:                        │
│    [Controlar o PC] [Jogar pelo Hefesto] [Nativa]   │
│  O jogo vê o controle como:                         │
│    [Xbox 360] [DualSense (botões PlayStation)]      │
│                                                     │
│  ● vai mudar para: DualSense (botões PlayStation)   │
└─────────────────────────────────────────────────────┘
                              [ Aplicar ]  ← o verde do rodapé
```

**A regra de ouro, e é ela que desfaz a tensão de arquitetura:**

> Não há dois donos do MESMO valor. Há o valor **vigente** (o daemon é dono, a
> caixa "Agora" ecoa) e o valor **escolhido** (ela é dona, mora na caixa "Quando
> o jogo abrir"). São **campos diferentes**, com nomes diferentes.

Isso importa porque a `AUTO-01.3` já enterrou o defeito de "dois donos da
máscara" — e uma leitura apressada deste plano o reabriria. Ver seção 6, fato 2.

---

## 3. O que cada defeito vira

| # | defeito | como este plano o resolve |
|---|---|---|
| **1** | o diálogo está no botão errado | passa a ter **um lugar óbvio**: o "Aplicar" do rodapé, que é onde a mudança sai |
| **2** | a máscara pergunta a cada clique | o clique **não aplica mais** — só marca a escolha. Nada a perguntar |
| **4** | o "Jogador 3" fantasma | **impossível**: o modo nunca muda no meio da partida sem passar pelo relançamento |
| **8** | a tela mostra o que não confere | separa "é" de "vai ser" — cada caixa tem uma fonte só |
| **3** | "1 jogador saiu" falso | ver seção 5 (é leva própria, pequena) |

**Não resolve, e é honesto dizer:** o **5** (rumble) é investigação, não desenho.
O **6** (numeração oscilante) depende da decisão 19 dela. O **7** (método) já tem
regra escrita na OITO-DEFEITOS-01.

---

## 4. A execução, passo a passo

**Cada passo é commitável sozinho e deixa a árvore verde.** Não pule a ordem: o
passo 2 depende do 1, e o 4 depende dos dois.

### Passo 1 — o campo da escolha (sem tocar a tela)

**Onde:** `src/hefesto_dualsense4unix/app/actions/home_actions.py`

Hoje `_render_home` escreve os seletores a partir do daemon a cada tique
(`:1059` `selector.set_active_id(mode)`, `:1076` idem para o flavor). **Não mexa
nisso.** Acrescente, ao lado, o estado da escolha dela:

```python
#: AGORA-E-DEPOIS-01: o que ELA escolheu e ainda não aplicou. `None` = nada
#: pendente, e a caixa "Quando o jogo abrir" espelha o vigente.
self._escolha_pendente: dict[str, str] | None = None
```

A regra do `_render_home`, e ela é a coisa mais importante deste passo:

- **enquanto `_escolha_pendente` for `None`** → os seletores espelham o daemon,
  exatamente como hoje;
- **quando houver escolha pendente** → os seletores mostram a **escolha dela**, e
  o `_render_home` **não os sobrescreve**.

**Teste que morde:** `tests/unit/test_agora_e_depois_01.py` — com escolha
pendente, dois tiques de `_render_home` seguidos não mudam o que o seletor mostra.
Arranque a guarda e ele reprova (é o defeito de "a escolha dela volta sozinha").

### Passo 2 — o clique deixa de aplicar

**Onde:** `home_actions._on_home_mode_changed` e `_on_home_flavor_changed`.

Hoje eles chamam `apply_mode(...)` e `call_async("gamepad.emulation.set", ...)`.
Passam a **só** gravar em `_escolha_pendente` e pedir um redesenho.

**Cuidado (fato 3 da seção 6):** o `_home_guard` já existe e impede que o
`set_active_id` do próprio `_render_home` dispare o handler. **Ele continua
necessário** — não o remova achando que o campo novo o substitui.

**Teste que morde:** clicar no seletor **não** produz chamada IPC nenhuma.

### Passo 3 — o rótulo do pendente

**Onde:** a caixa "Quando o jogo abrir", abaixo dos seletores.

Uma linha, no léxico da tela: `● vai mudar para: DualSense (botões PlayStation)`.
Some quando não há pendência. **Sem essa linha o plano vira defeito**: ela clica,
nada acontece na hora, e sem o rótulo ela não sabe se o clique registrou.

Texto e função pura em `app/actions/relancar.py` (ver fato 7).

### Passo 4 — o "Aplicar" aplica o DEPOIS também

**Onde:** `src/hefesto_dualsense4unix/app/actions/footer_actions.py:195-253`.

Hoje o botão manda `profile.apply_draft` com as sete seções de
`app/draft_config.py:1030-1133` — e **nenhuma delas é modo ou máscara** (fato 4).

Ele passa a, **antes** do `apply_draft`:

1. se `_escolha_pendente` é `None` → segue como hoje, sem nenhuma mudança;
2. se há pendência **e não há jogo aberto** → aplica pelo caminho que já existe
   (`mode_transition.apply_mode`), depois segue com o `apply_draft`;
3. se há pendência **e há jogo aberto** → abre o diálogo de relançamento que já
   existe (`base._perguntar_antes_de_relancar`, fato 7).

**NÃO** ponha a transição de modo dentro do `apply_draft` do daemon. Fato 5
explica por quê — e o erro produz "ERRO ao aplicar" com o modo já aplicado, que
é a mentira que o `APLICAR-VERDADE-02` foi escrito para matar.

**Teste que morde:** com pendência e sem jogo, o Aplicar dispara a transição; com
pendência e jogo aberto, ele abre o diálogo e **não** dispara nada antes da
resposta.

### Passo 5 — a foto, e a palavra dela

`scripts/gui-captura/retratar_abas.py` **antes e depois**. A
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
vale inteira: interface só fecha com o olho dela.

---

## 5. A leva pequena que vale fazer junto (defeito 3)

**"1 jogador saiu — não foi você; volta sozinho"** aparece com os dois controles
dela na tela, conectados. Ele conta **jogadores virtuais**, e cada reinício do
daemon derruba e recria os vpads.

**A regra de produto, em uma linha:** *o produto fala do que ela vê.* O aviso diz
**controle**, não jogador virtual — se os físicos estão todos presentes, ele cala.

**O contrapeso, obrigatório:** quando um controle **dela** cair de verdade, o
aviso tem de aparecer. Sumir com ele nesse caso seria trocar um defeito por outro
pior, e o teste tem de travar os dois lados.

---

## 6. OS OITO FATOS QUE VOCÊ PRECISA SABER

Cada um destes custou uma cura errada em 08/08. Todos **MEDIDOS**.

1. **O jogo lê a configuração uma vez.** `assets/hefesto-launch.sh:320` termina em
   `exec env "$@"`. Nenhuma reescrita posterior alcança o processo em curso.

2. **O daemon é o dono do que a tela mostra** (`AUTO-01.3`, comentário em
   `home_actions.py:1067-1074`). Este plano **não** revoga isso: ele cria um
   campo NOVO para a escolha dela. Se você fizer os seletores "segurarem" o valor
   vigente, reabre o defeito dos dois donos.

3. **`_render_home` reescreve os seletores a cada tique** (`:1059`, `:1076`) e
   esconde a linha da máscara quando o daemon não diz `gamepad` (`:1061`). Sem a
   guarda do passo 1, a escolha dela volta sozinha — e a máscara **nem aparece**.

4. **O botão verde é o `btn_footer_apply`** (`gui/main.glade:3616-3620`, verde por
   `.btn-apply` em `gui/theme.css:836`), e o payload dele **não carrega modo nem
   máscara** (`app/draft_config.py:1030-1133`, `daemon/ipc_draft_applier.py:46-88`).

5. **Não mova a transição de modo para dentro do daemon.** `apply_mode`
   (`app/actions/mode_transition.py:159-181`) é da GUI e dispara até 3 chamadas de
   2,0 s cada; o `apply_draft` do rodapé tem `timeout_s=1.5`
   (`footer_actions.py:250`). A conta não fecha, e o resultado é "ERRO" com o modo
   aplicado.

6. **`mode_of_state` devolve só `native`/`gamepad`/`desktop`** — **nunca** o
   flavor (`mode_transition.py:198-212`). Qualquer comparação de "mudou?" que use
   só isso é **cega à máscara**. Foi assim que uma cura de hoje nunca disparou.

7. **O diálogo de relançamento JÁ EXISTE e funciona.** Módulo puro em
   `app/actions/relancar.py` (listas `EXIGEM_RELANCAR`/`MUDA_NA_HORA`, textos,
   `precisa_perguntar`), o gancho em `app/actions/base.py`
   (`_perguntar_antes_de_relancar`, `_relancar_decidir`, `_relancar_o_jogo`), e o
   construtor de diálogo em `daemon_actions.build_consentimento_dialog`.
   **Reuse — não escreva outro.**

8. **O install é editable: cura de daemon só vale no PRÓXIMO start.** Se o passo
   tocar `src/hefesto_dualsense4unix/daemon/`, reinicie antes de pedir teste —
   e **nunca** com jogo aberto. Isso já custou uma rodada inteira em 08/08.

---

## 7. O que NÃO fazer

| não faça | por quê |
|---|---|
| pôr o diálogo no "Salvar este perfil" | gesto errado, e trunca o save (rename, reload, `profile_switch`). Foi feito e revertido em 08/08 |
| fazer o `_escolha_pendente` guardar modo/máscara **e aplicá-los** no ramo "Aplicar na próxima abertura" | `base._MUDANCAS_QUE_SAO_ESCRITA` existe justamente para impedir isso: aplicar ali recria o vpad ao vivo |
| inventar vocabulário novo na tela | ela recusa nome que não deriva do que existe. "Agora" e "Quando o jogo abrir" saem do próprio produto |
| aplicar na máquina dela antes de o desenho fechar | regra de método da OITO-DEFEITOS-01: um cético responde *"o que isso quebra?"* antes |

---

## 8. Como saber que terminou

**Os portões da casa** (`CLAUDE.md`, "Antes de fechar qualquer leva"), todos em
zero, com `git add -A` **antes** — eles não veem arquivo novo.

**E o teste dela, que é o que importa:**

1. abre o Sackboy com dois DualSense;
2. vai ao Hefesto **no meio da partida**, passa pelas abas, muda a máscara;
3. **nada acontece na hora**, e a linha `vai mudar para:` aparece;
4. clica em **Aplicar**;
5. o diálogo pergunta **uma vez**, com as três saídas;
6. escolhendo *"Aplicar agora e reiniciar o jogo"*, o jogo fecha e a Steam o
   reabre com a máscara nova valendo.

**Se o passo 3 falhar, pare** — é o coração do desenho, e o resto não vale nada
sem ele.
