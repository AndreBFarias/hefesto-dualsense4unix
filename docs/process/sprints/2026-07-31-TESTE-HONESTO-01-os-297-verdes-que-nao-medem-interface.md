# TESTE-HONESTO-01 — os 297 verdes que não medem interface nenhuma

- **Status:** ABERTA — documento de medição e plano. Nada de código nesta
  rodada; nenhum arquivo de teste, de configuração ou de workflow foi tocado
  para escrever isto
- **Prioridade:** MÉDIA — a suíte NÃO está quebrada. O que esta sprint ataca é
  cobertura que finge, e nada aqui aparece na tela dela
- **Aberta em:** 31/07/2026, sobre `HEAD 7bd0cb7`, branch
  `restauro/inicio-da-sessao`, com a v0.4.0 publicada e o daemon dela VIVO
- **Relacionada:** [PORTÃO-VIVO-01](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md)
  (bloco B: o `core.hooksPath` desta máquina desvia o commit local),
  [PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md)
  (`:227` e `:234` já mediram os dois diretórios vazios em 26/07) e
  [EMULAÇÃO-NO-JOGO-01](2026-07-29-EMULACAO-NO-JOGO-01-o-r1-troca-de-app-em-vez-de-jogar.md)
  (a cura do R1, cujo teste é uma das duas provas de que a suíte morde)
- **Amarrada com:** [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md),
  entrega E8 — a fixture `hid_capture_bt.bin` que o ADR-008 promete e que não
  existe. A E2 daqui e aquela entrega curam o mesmo buraco por lados diferentes
- **Rodada:** uma das nove sprints de 31/07; o retrato está no
  [estudo da auditoria](../estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md)
  e a ordem de execução no
  [índice das ondas](2026-07-31-INDICE-as-ondas-depois-da-auditoria.md), item 1.16

## Abre pelo número bom, porque ele muda o tom

A suíte inteira rodou **na máquina dela**, no venv do projeto:

```
$ .venv/bin/python -m pytest tests/ -q
6097 passed, 5 warnings in 124.62s (0:02:04)
```

Zero falhas, **zero skip**, cinco avisos. Rodei de novo para conferir e deu o
mesmo: `6097 passed, 5 warnings in 134.87s`. A coleta bate com a execução
(`pytest tests --collect-only -q` = `6097 tests collected`).

E os **sete portões**, cada um executado direto pelo script, todos `exit 0`:

| Portão | Comando | Saída |
|---|---|---|
| Anonimato | `bash scripts/check_anonymity.sh` | exit 0 |
| Versão | `python scripts/check_version_consistency.py` | exit 0 (9 alvos em 0.4.0) |
| Paridade de empacotamento | `bash scripts/check_packaging_parity.sh` | exit 0 |
| Dados de teste | `bash scripts/check_test_data.sh` | exit 0 |
| Acentuação | `python scripts/validar-acentuacao.py --all` | exit 0 |
| Glifos | `python scripts/validar-glifos.py --all` | exit 0 |
| Ruff | `python -m ruff check src/ tests/` | exit 0 |

**As duas curas da v0.4.0 mordem de verdade.** Conferi as duas no fonte:

- o gate do R1 é testado por **comportamento** — daemon real, poll loop, R1
  pressionado, par diferencial (jogo suspenso cala, desktop emite) — e a
  correção do `e74077c` está lá: `tests/unit/test_emulacao_no_jogo_teclado.py:466-482`
  espera **por condição** com teto de 5 s em vez de dormir 0,06 s fixo, e ainda
  reprova alto se o cenário não chegou a rodar (`:479-483`: *"o poll loop não
  completou os tiques mínimos em 5 s — o cenário não chegou a ser exercitado,
  então nada abaixo prova coisa alguma"*);
- o perfil que nasce vencendo tem 7 testes em
  `tests/unit/test_footer_salvar_nasce_acima_dos_catch_all.py`, dos quais
  quatro calculam a prioridade contra fixture do disco dela; só o *call site*
  está travado por texto (`:146` lê o arquivo, `:152` procura
  `to_profile(nome, priority=`), com a fraqueza declarada na própria docstring.

**Então o assunto desta sprint não é suíte quebrada.** É o que os 6097 verdes
*não* dizem — e onde o verde é afirmação fraca.

### Uma nota de honestidade sobre a hora da medição

Enquanto eu escrevia este documento, **dois portões ficaram vermelhos por
documentos desta mesma rodada**, ainda em voo na árvore de trabalho, e voltaram
ao verde quando os arquivos aterrissaram:

- `python scripts/validar-glifos.py --all` → `exit 1`, três `U+FE0F` em
  `docs/process/sprints/2026-07-31-INDICE-as-ondas-depois-da-auditoria.md:88`,
  `:106` e `:111`; agora `exit 0`;
- `python scripts/validar-referencias-docs.py --all` → `exit 1`, duas
  referências mortas (`2026-07-25-JOGO-01-...md:9` e
  `2026-07-31-CR-SEQUENCIA-01-...md:188` citavam sprints que ainda não
  existiam); agora `exit 0`, com as onze sprints do dia no lugar.

Nenhum dos dois é defeito da suíte. Ficam registrados por dois motivos: **o
número de portões verdes tem hora**, e este é o mesmo par de portões que a
pendência do fim deste documento discute — quem barra é o CI no push, e o
commit local não vê nada disso.

---

## O que eu reconferi, e as quatro coisas que mudaram de moldura

Regra desta casa: evidência copiada de outro agente é hipótese até eu abrir o
arquivo. Abri. Quatro afirmações mudaram.

### 1. Na máquina dela, os 17 NÃO rodam contra widget de mentira

A leitura original é que os 17 arquivos plantam `gi` falso *até* na máquina
dela. **Medi e não é isso.** Os arquivos carregam a guarda `GATE-SKIP-MASK-01`:
com o PyGObject real disponível, `_install_gi_stubs()` **volta antes de plantar
qualquer coisa** — está escrito em `tests/unit/test_rumble_actions.py:24-36` e
em `tests/unit/test_compact_window.py:17-31`, com a razão ao lado (*"o merge
abaixo mutaria o gi REAL"*).

Prova executada: importei cada um dos 17 num processo próprio e perguntei o que
sobrou em `sys.modules`. Dezesseis terminam com o `gi` **real**
(`Gtk.Box = <class 'gi.overrides.Gtk.Box'>`); o décimo sétimo
(`test_modo01_o_modo_jogo_liga_sozinho.py`) planta só **dentro de função**
(linhas 854-858), então no import nem chega a plantar.

Isso **não** salva os 17 — muda onde o falso-verde acontece, e o lugar certo
importa para a cura. O falso-verde é no CI, e ele é reproduzível:

A receita da simulação, para quem quiser repetir: um `sitecustomize.py` fora do <!-- ref-externa: arquivo de simulação, criado fora do repositório de propósito -->
repositório que insira em `sys.meta_path` um finder levantando `ImportError`
para `gi` e `gi.*`, e rodar o pytest com `PYTHONPATH` apontando para o
diretório dele. É o ambiente do job `lint-test`, que **não** instala PyGObject
(`ci.yml:196-212`, com a frase *"não finja que está coberto"* em `:211`).

```
$ PYTHONPATH=<dir do sitecustomize> .venv/bin/python -m pytest \
      tests/unit/test_rumble_actions.py -q
29 passed in 0.27s
```

Vinte e nove verdes contra `Gtk.Box = object`. E o contraste, no mesmo
ambiente, com um arquivo que **tem** a guarda: `test_gui_dialogs_theme.py`
coleta **19** testes com o `gi` real e **0** sem ele — ele desaparece da coleta
em vez de fingir.

### 2. A muralha de texto encolheu; a praga de 25/07 não está de volta

O [estudo de 25/07](../estudos/2026-07-25-leva-causas-raiz.md) mediu
*"~240 asserts em ~70 arquivos travam o TEXTO do código"* e, pior, um assert que
**proibia a correção** de um defeito. O
[mapa de interfaces de 27/07](../estudos/2026-07-27-mapa-interfaces-e-suite-de-testes.md)
refinou: 34 via `inspect.getsource` e 37 lendo `.py` como texto.

Hoje o mesmo grep devolve **21** chamadas de `inspect.getsource` e **22**
leituras de fonte por `Path(<módulo>.__file__).read_text` (em 11 arquivos). A
régua pode não ser idêntica — o mapa contava asserts, eu contei chamadas — mas
a direção é de queda, e **nenhuma das 21 proíbe a correção de um bug**: 11 são
espelhos com contraparte GTK-real no mesmo arquivo, 2 são guardas de ausência
com a decisão escrita na docstring (`test_autoswitch_lock.py:508-511`: *"montar
o daemon inteiro para provar uma AUSÊNCIA custaria mais do que vale"*), e 8 são
fiação. É a E3, e é BAIXA de propósito.

### 3. A lightbar por Bluetooth já é testada — só que como função pura

A recomendação original manda começar pelos caminhos onde o Bluetooth já
produziu incidente: reconexão, suspensão, lightbar. **A lightbar já está
coberta**: `tests/unit/test_lightbar_reset.py:93-115` tem seis casos de
`should_reclaim_on_wake`, incluindo o diferencial que importa
(`should_reclaim_on_wake("usb", ...) is False` em `:97-99`). O que falta ali não
é o caso BT — é o **fluxo**: nada exercita a borda do wake com um controle
Bluetooth atravessando o daemon.

### 4. A família de asserts de fonte é maior do que 21

O grep de `inspect.getsource` não alcança quem lê o arquivo do módulo como
texto. Achei 22 dessas em 11 arquivos, e uma delas é exatamente a que a E2
precisa: `tests/unit/test_dedup_guard.py:120-124` prova o `native_bt_fragil`
com `assert 'result["native_bt_fragil"]' in fonte` — um assert que **sobrevive
à sabotagem** que ele deveria pegar. Volto a isso na E2.

---

## E1. A dívida do GTK de mentira: 297 testes, 17 arquivos, zero pagos

### O que está medido

`tests/unit/test_guarda_gi_falso_precisa_de_exigir_gi_real.py:50-70` lista
**17 nomes** na `DIVIDA_GI_FALSO`. Rodei o detector do próprio módulo contra a
árvore de hoje:

```
em falta hoje: 17
pagos (na allowlist, já curados): []
novos (fora da allowlist): []
```

Os **mesmos 17 de 30/07**. Nada pago, nada novo — a guarda está fazendo o
trabalho dela (impedir crescimento) e ninguém amortizou nada.

Eles somam **297 testes coletados** (`pytest <os 17> --collect-only -q` =
`297 tests collected`), **4,9% dos 6097**:

| Testes | Arquivo |
|---:|---|
| 53 | `test_modo01_o_modo_jogo_liga_sozinho.py` |
| 30 | `test_auto01_um_clique_em_vez_de_dez.py` |
| 29 | `test_rumble_actions.py` |
| 26 | `test_triggers_actions.py` |
| 26 | `test_proton_lock_button.py` |
| 24 | `test_vpad_degradation_banner.py` |
| 22 | `test_mode_transition_um_dono.py` |
| 19 | `test_profiles_gui_sync.py` |
| 16 | `test_profiles_editor_mode.py` |
| 10 | `test_status_actions_reconnect.py` |
| 10 | `test_daemon_status_matrix.py` |
| 7 | `test_emulation_mic_quirk.py` |
| 7 | `test_compact_window.py` |
| 6 | `test_daemon_autostart.py` |
| 5 | `test_lightbar_persist.py` |
| 4 | `test_daemon_status_initial.py` |
| 3 | `test_emulation_actions_modo_jogo.py` |

E ficam fora do job `gtk-real` **por construção**: a seleção é
`grep -rlE 'exigir_gi_real|skip_sem_gi_real' tests/unit --include='*.py'`
(`.github/workflows/ci.yml:387`), que hoje devolve **39 arquivos** — nenhum dos
17. O comentário logo acima da linha explica por que a seleção é assim, e está
certo; o problema é que 17 arquivos de interface nunca ganharam a senha.

**O resumo honesto:** no CI sem PyGObject eles rodam verdes contra `object`; no
CI com GTK real eles não são convidados; na máquina dela rodam contra o `gi`
real, mas nada os obriga a construir um widget. **297 verdes que não medem
interface nenhuma** — o número da capa desta sprint continua de pé, só que pela
razão certa.

### A entrega: amortizar em quatro lotes, com número por lote

Pagar um arquivo é: chamar `exigir_gi_real()` no topo (antes do bloco de
imports) **ou** trocar o stub cru pelo `instalar_stubs_gi(monkeypatch)` do
`tests/conftest.py` (`:241`), e tirar o nome da allowlist. O `exigir_gi_real`
(`:203`) faz mais do que pular: com o processo envenenado e o ambiente bom, ele
**limpa o stub e devolve o `gi` real** (`:218-229`), e a docstring diz por quê —
*"a máquina de desenvolvimento não pode perder centenas de testes por causa
disso"*.

| Lote | Arquivos | Testes | O que são |
|---|---:|---:|---|
| **A** | 6 | 32 | `emulation_actions_modo_jogo`, `daemon_status_initial`, `lightbar_persist`, `daemon_autostart`, `compact_window`, `emulation_mic_quirk` — os menores, e o lote que ensina o caminho |
| **B** | 4 | 55 | `daemon_status_matrix`, `status_actions_reconnect`, `profiles_editor_mode`, `profiles_gui_sync` — estado do daemon na janela |
| **C** | 4 | 98 | `mode_transition_um_dono`, `vpad_degradation_banner`, `proton_lock_button`, `triggers_actions` |
| **D** | 3 | 112 | `rumble_actions`, `auto01_um_clique_em_vez_de_dez`, `modo01_o_modo_jogo_liga_sozinho` — os três maiores, por último |

**O lote A já está medido, e passa.** Simulei o CI (sem PyGObject) removendo só
os seis arquivos do lote A da suíte `tests/unit`:

```
5396 passed, 95 skipped, 5 warnings in 150.55s
TOTAL  27389 declarações  8038 sem cobrir  71%
```

**Zero falhas, zero erro de coleta**, e a cobertura cai de 72% para 71% — acima
do piso de 70 do `ci.yml:271`. O lote A entra sem quebrar nada; os outros três
precisam da medição do risco 3, logo abaixo, antes de sair do papel.

> **PAGO — lote A, 13/08/2026.** Os seis arquivos ganharam `exigir_gi_real()` no
> topo e saíram da `DIVIDA_GI_FALSO`, que passou de 17 para 11 nomes e ganhou o
> `TETO_DA_DIVIDA` prometido abaixo. Medido nesta árvore, simulando o
> `lint-test` com o `gi` bloqueado por um pacote que levanta `ImportError`:
>
> | | antes | depois |
> |---|---:|---:|
> | `pytest tests --collect-only` (sem PyGObject) | 5602 | **5572** |
> | erros de coleta | 0 | **0** |
> | `grep -rlE 'exigir_gi_real\|skip_sem_gi_real' tests/unit` | 45 | **51** |
> | os seis, sem PyGObject | 32 passed | **6 skipped** |
> | os seis, com o GTK real desta máquina | — | **32 passed** |
>
> O `5602` de base difere do `5502` medido em 31/07 porque a árvore cresceu; a
> queda de 30 é o que importa, e a margem sobre o piso 5100 do `ci.yml:237`
> continua folgada (472). **O risco 3 não se materializou para o lote A**: os 15
> módulos que dependiam dos 17 seguem coletando, e os 291 testes deles passam.
>
> **Os lotes B, C e D continuam de pé, e não por falta de vontade:** o que trava
> é o piso de cobertura de 70 (`ci.yml:271`), e medi-lo exige rodar a suíte
> inteira — o que não se faz com os controles dela vivos na máquina. Enquanto
> essa medição não existir, pagar mais um lote é apostar o `lint-test`.

**Aceite:** ao fim de cada lote, o detector devolve `pagos: [os N do lote]`,
`novos: []`; a `DIVIDA_GI_FALSO` fica com os nomes restantes e **só encolhe**; o
`grep` do `ci.yml:387` passa de 39 para 39+N arquivos; e a suíte rodada **sem
PyGObject** termina com **zero erro de coleta** — que é a prova de que o lote não
derrubou vizinho (ver risco 3).

**Mordida (o que tem de reprovar se a cura for arrancada):** hoje o portão só
pega arquivo NOVO. O lote entrega junto um **teto que encolhe**, igual ao piso
de coleta do CI: `assert len(DIVIDA_GI_FALSO) <= TETO`, com o `TETO` baixado a
cada lote. Recolocar um nome na allowlist reprova; arrancar o
`exigir_gi_real()` de um arquivo pago devolve o nome à lista de "em falta" e
reprova o portão que já existe. A segunda mordida é de ambiente: rodar um
arquivo pago com `HEFESTO_EXIGE_GTK_REAL=1` **sem** GTK real tem de dar
**FAIL**, não skip — é o que `tests/conftest.py:233-238` faz, e é a diferença
entre portão e teatro.

**Risco: ALTO, e não era o que eu esperava.** Medi três coisas antes de
escrever isto, e a terceira derruba a ideia de pagar tudo de uma vez.

1. **O censo de coleta do CI.** `ci.yml:234-255` reprova se a coleta encolher
   abaixo de `PISO=5100` (`:237`). Simulei o ambiente do `lint-test` bloqueando
   o `gi` por `meta_path`: a coleta hoje é **5502** — margem de 402. Um arquivo
   pago **desaparece** da coleta nesse ambiente (medido: `test_gui_dialogs_theme.py`
   coleta 19 com `gi` e 0 sem). Logo:

   | Depois do lote | Coleta sem PyGObject | Margem sobre 5100 |
   |---|---:|---:|
   | hoje | 5502 | 402 |
   | A | 5470 | 370 |
   | B | 5415 | 315 |
   | C | 5317 | 217 |
   | D | 5205 | 105 |

   Pagar tudo cabe, mas come 297 dos 402 de folga. **Por isso os lotes**: cada
   um remede a coleta antes do próximo, e o piso só se mexe por decisão escrita.

2. **O piso de cobertura.** `ci.yml:271` reprova abaixo de `--cov-fail-under=70`.
   Rodei `pytest tests/unit --cov` no ambiente sem PyGObject, com e sem os 17:

   | Cenário | Declarações | Sem cobrir | Cobertura |
   |---|---:|---:|---:|
   | com os 17 (hoje) | 27389 | 7765 | **72%** |
   | sem os 17 | 27389 | 10260 | **63%** |

   **Nove pontos abaixo, e seis abaixo do piso de 70** — pagar os 17 de uma vez
   deixa o `lint-test` vermelho no passo de cobertura. Ressalva de leitura, que
   é o item 3: parte desses 2495 declarações não é cobertura *dos* 297 testes,
   e sim dos testes de 13 outros módulos que **deixam de ser coletados** quando
   os 17 saem.

3. **O que ninguém tinha medido: 15 módulos dependem dos 17 para conseguir
   sequer ser importados no CI.** Removendo os 17 no ambiente sem PyGObject, o
   resultado foi `19 failed, 4871 passed, 79 skipped, 13 errors`. Os 13 erros
   são de **coleta**, em `test_daemon_toasts_leigo`, `test_home_actions_handlers`,
   `test_home_autoswitch_lock_hint`, `test_home_aviso_vivo`,
   `test_home_controller_cards`, `test_home_render_state`,
   `test_numero_do_controle_unico`, `test_profiles_vocabulario_leigo`,
   `test_steam_apply_button`, `test_steam_input_honestidade`,
   `test_steam_modo_simples`, `test_storm_launch_options` e
   `test_wrapper_banner`; as 19 falhas são de `test_multi_controller_ui` e
   `test_r12_editor_simples_jogo_steam`.

   **E não é o `gi` vazando de um arquivo para o outro** — esse buraco já foi
   tapado: o `pytest_collectstart` do `tests/conftest.py:266-295` retira o stub
   antes de cada módulo, e o próprio run avisa em voz alta (*"stub de `gi`
   retirado antes de 1 módulo(s) — a poluição de sys.modules NÃO vazou entre
   arquivos"*). O que vaza é outra coisa: **o módulo de produção fica importado**.
   Um dos 17 importa `hefesto_dualsense4unix.app.actions.base` enquanto o `gi`
   falso está de pé; o hook limpa `sys.modules["gi"]`, mas não desimporta
   `base`. O arquivo seguinte faz `from ...app.actions import home_actions`,
   encontra tudo pronto em `sys.modules` e nunca chega no `import gi`.

   Prova, no ambiente sem PyGObject:

   ```
   $ pytest tests/unit/test_home_render_state.py -q
   ERROR ... base.py:7: in <module> import gi
   ImportError: PyGObject ausente          # sozinho, não coleta

   $ pytest tests/unit/test_rumble_actions.py tests/unit/test_home_render_state.py -q
   59 passed in 1.73s                      # atrás de um dos 17, coleta e passa
   ```

   Ou seja: os 297 verdes não são só cobertura que finge — no CI eles são a
   **fundação** sobre a qual outros 15 módulos de interface se apoiam sem saber.
   É o retrato mais completo do defeito, e muda a entrega.

**O que o risco 3 acrescenta à entrega:** cada lote paga **o plantador e os
beneficiários dele no MESMO commit**. Antes do lote, levantar a lista de
beneficiários é uma medição barata e mecânica — rodar a suíte sem PyGObject
ignorando os arquivos do lote e anotar quem passa a errar na coleta. Cada
beneficiário ganha o caminho honesto (`instalar_stubs_gi(monkeypatch)` do
conftest, que é desfeito no teardown e não deixa módulo de produção importado
por acidente) ou a própria guarda.

**A boa notícia dentro do risco:** isso **não** vira regressão silenciosa. O
censo do `ci.yml:249-254` reprova quando há erro de coleta (`ERROS > 0`), com a
mensagem *"módulo(s) NÃO coletam neste ambiente"*. O portão que a casa escreveu
em 28/07 é exatamente o que pega este caso — ele só nunca tinha sido provocado.

**A entrega irmã, barata e do mesmo assunto:** o job `gtk-real` **não tem piso
de contagem** — ele só exige que a lista de arquivos não seja vazia
(`ci.yml:391`: `test -n "$ALVOS"`). Enquanto testes migram do `lint-test` para
lá, o único lugar que os conta é o censo que eles estão deixando. Dar ao
`gtk-real` o mesmo tipo de trava de encolhimento fecha a porta por onde 297
testes poderiam sumir sem ninguém ver.

---

## E2. A premissa "USB é o mundo", medida — e onde ela ainda decide comportamento

### O número, e o fato de ele não ter se mexido

```
$ grep -rho 'transport="bt"'  tests/ | wc -l   →   9
$ grep -rho 'transport="usb"' tests/ | wc -l   →   196
```

Os nove estão em **quatro arquivos**: `test_state_full_audio_speaker.py:52,148`,
`test_daemon_lifecycle.py:60`, `test_tui_app.py:78` e
`test_controller.py:74,77,80,83,91`. O
[mapa de 27/07](../estudos/2026-07-27-mapa-interfaces-e-suite-de-testes.md) mediu
*"apenas 9 ocorrências de `transport="bt"` em 4 arquivos"*. **Quatro dias
depois, os mesmos 9 nos mesmos 4.**

E o buraco **não é skip**: a suíte inteira roda com **0 skipped** nesta máquina,
e não existe marcador de skip por hardware Bluetooth em lugar nenhum. Um caso
que não existe não pula — ele simplesmente não aparece em relatório algum. É a
classe de defeito que a casa já registrou como recorrente (*"a suíte é cega a BT
por construção"*).

**Uma correção de mecanismo:** a afirmação de 25/07 de que *"o `conftest` força
o transporte USB em todo teste"* **não vale mais** — `grep transport tests/conftest.py`
não devolve nada. O viés hoje é um **valor padrão**:
`src/hefesto_dualsense4unix/testing/fake_controller.py:70`
(`transport: Transport = "usb"`) e o `DEFAULT_STATE` em `:60-66`. Isso é boa
notícia para a entrega: parametrizar custa passar um argumento.

### Onde o transporte decide comportamento de verdade

| Onde | O que muda com `bt` | Coberto hoje? |
|---|---|---|
| `core/lightbar_reset.py:116` | `should_reclaim_on_wake` só devolve `True` em BT | **Sim**, como função pura (`test_lightbar_reset.py:93-115`, com o diferencial USB em `:97-99`). Falta o fluxo |
| `daemon/ipc_handlers.py:1465-1467` | `native_bt_fragil` só é `True` com `native_mode` **e** `transport == "bt"` | **Não** por comportamento: `test_native_mode.py` nunca seta transporte, e o único teste é substring de fonte (`test_dedup_guard.py:120-124`) |
| `core/backend_pydualsense.py:985` | leitura de calibração confere CRC-32 só em BT | Não medi |
| `core/backend_pydualsense.py:1452` e `:1718` | dois desvios de enumeração por transporte | Não medi |
| `daemon/connection.py:60` e `:354` | publica `CONTROLLER_CONNECTED` com o transporte | **Não**: `tests/unit/test_daemon_connection.py:44-45` tem `def get_transport(self) -> str: return "usb"` **fixo**, e as cinco travessias de retry/backoff (`:78-162`) nunca publicam `bt` |

### A entrega

Parametrizar por transporte (`usb` × `bt`) os fluxos onde o Bluetooth já
produziu incidente nesta casa:

1. **Reconexão** — `tests/unit/test_daemon_connection.py`: o `_FakeController`
   local (`:35-46`) ganha `transport` no construtor, e os cinco casos viram
   `@pytest.mark.parametrize("transporte", ["usb", "bt"])`.
2. **Suspensão/wake** — o fluxo que hoje só existe como função pura: um caso de
   ponta a ponta com `FakeController(transport="bt")` atravessando a borda do
   wake, para a decisão da `lightbar_reset` ser exercitada **de dentro do
   daemon**, não só na mesa.
3. **Lightbar e estado publicado** — `native_bt_fragil` medido por
   comportamento: `state_full` com um controle BT em modo nativo devolve `True`,
   e o mesmo cenário em USB devolve `False`.

**Aceite:** `grep -rho 'transport="bt"' tests/ | wc -l` sobe de 9 para pelo
menos 20; os três fluxos acima têm par diferencial (o caso USB tem de dar o
resultado **oposto**, não só passar); e o `native_bt_fragil` deixa de depender
de assert de texto.

**Mordida:** sabote `daemon/ipc_handlers.py:1465` para
`result["native_bt_fragil"] = bool(result["native_mode"])` — a checagem por
transporte some. O teste de hoje (`test_dedup_guard.py:120-124`) **continua
verde**, porque a string `result["native_bt_fragil"]` segue no arquivo; o teste
novo tem de morrer. Se ele não morrer, não foi escrito por comportamento e a
entrega não vale. Mesma prova para a reconexão: fixe o `get_transport` do fake
em `"usb"` de novo e o caso BT tem de reprovar.

**Risco:** baixo em código de produção (a entrega é só de teste), médio em
tempo: parametrizar dobra o número de travessias assíncronas desses arquivos, e
travessia assíncrona é onde mora flake. Cada caso novo espera **por condição**,
nunca por relógio — o padrão já existe e é o do `e74077c`
(`test_emulacao_no_jogo_teclado.py:466-482`).

### O amarre com a DOC-VERDADE-02

O ADR-008 afirma, em `docs/adr/008-bt-vs-usb-polling.md:14`, que o
`FakeController` tem **dois** replays determinísticos —
`tests/fixtures/hid_capture_usb.bin` e `tests/fixtures/hid_capture_bt.bin` — e
que *"testes W1.3 cobrem ambos"*. Medido: `ls tests/fixtures/` devolve
`hid_capture_usb.bin` e `__init__.py`. **A fixture BT não existe**, e o único
consumidor da que existe é `tests/unit/test_fake_controller_capture.py:116`. A
nota de verificação de 25/07 do próprio ADR (`:24-29`) corrigiu o `daemon.toml`
e passou ao largo disto.

`scripts/record_hid_capture.py` existe (executável, 14.913 bytes) e documenta o
comando de gravação em `:21-25`. Gravar a fixture **depende do controle dela na
mesa**, então não entra aqui como entrega de código: entra como a E8 da
[DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md),
que decide entre gravar ou retirar a alegação do ADR. Se a fixture for gravada,
os casos BT da E2 ganham replay determinístico e param de depender de fake
inventado — e é por isso que as duas entregas se citam.

---

## E3. As oito fiações de texto puro — e a lenda que eu quero matar por escrito

### O que a auditoria mediu, e o que ela NÃO mediu

As 21 ocorrências de `inspect.getsource` estão classificadas assim, e conferi
uma a uma:

| Tipo | Quantas | Onde |
|---|---:|---|
| Fiação texto-pura | **8** | `test_home_autoswitch_lock_hint.py:66,72,79,96`; `test_wrapper_banner.py:145,148,156`; `test_gui_review_fixes.py:114` |
| Espelho com contraparte GTK-real no mesmo arquivo | 11 | `test_proton_lock_button.py:380,382,391`; `test_steam_apply_button.py:388,390,404`; `test_launch_wrapper_dialog.py:697`; `test_gui_dialogs_theme.py:86,176,194,206` |
| Guarda de ausência com decisão em docstring | 2 | `test_autoswitch_lock.py:516,524` |

**A lenda que morre aqui:** *"os testes-muralha de 25/07 voltaram"*. Não
voltaram. **Nenhuma das 21 proíbe a correção de um bug.** As 8 de fiação são
asserts do tipo `assert "autoswitch_lock_text(state)" in src` — quebram se
alguém renomear ou colocar a função em linha, sem mudar comportamento nenhum.
É atrito de refactor, não trava de cura. A praga de 25/07 era outra coisa: um
assert que congelava que a janela **nunca** poderia fechar a Steam, enquanto a
função existia e era inalcançável (registrado em
[leva-causas-raiz](../estudos/2026-07-25-leva-causas-raiz.md), item 2). Essa
classe não aparece na medição de hoje.

**Duas coisas que eu achei e a auditoria não:**

1. **Dois dos "espelhos" não têm a senha do CI.** `test_proton_lock_button.py` e
   `test_steam_apply_button.py` não chamam `exigir_gi_real` nem usam
   `skip_sem_gi_real` — eles usam `skip_sem_gtk_response` (`tests/conftest.py:175-178`).
   A contraparte GTK-real deles existe (`test_proton_lock_button.py:397-409`,
   guardada por `_DISPLAY_OK`), mas **só roda na máquina dela**: o job
   `gtk-real` seleciona por outro grep e não os pega. E `test_proton_lock_button.py`
   ainda está na `DIVIDA_GI_FALSO`. O espelho existe e nunca se olha no CI.
2. **A família é maior que 21.** Somando as 22 leituras de
   `Path(<módulo>.__file__).read_text` (11 arquivos) dá **43 pontos** de assert
   sobre texto de fonte, e há ainda uma terceira forma — caminho `.py` montado
   à mão, como `test_footer_salvar_nasce_acima_dos_catch_all.py:145-152`. Não
   classifiquei as 22; a E3 continua com escopo nas 8 medidas mais a de
   `test_dedup_guard.py:120-124`, que a E2 cobra por outro motivo.

### A entrega

Nas 8 de fiação, trocar o assert por substring por **dublê que intercepte a
chamada** — o padrão já está na casa: `test_emulacao_no_jogo_teclado.py:458-459`
usa `MagicMock` com `side_effect` para gravar o que foi despachado. Os espelhos
e as guardas de ausência **ficam como estão**, e isso é decisão, não omissão.

**Aceite:** as 8 ocorrências saem; cada teste novo prova a mesma coisa por
observação (a função pura foi chamada com o estado certo; o rótulo nasce
invisível e imune ao `show_all`); e o grep de `inspect.getsource` cai de 21 para
13.

**Mordida, nos dois sentidos — e os dois têm de valer:**

- **arrancar a cura reprova:** tire a chamada de `autoswitch_lock_text(state)`
  de `_render_home` e o teste novo tem de falhar;
- **refactor legítimo NÃO reprova:** renomeie `autoswitch_lock_text` para outro
  nome, atualize o chamador e o teste novo tem de continuar verde. É este
  segundo lado que o assert de hoje reprova, e é a razão de existir a entrega.

**Risco:** baixo, e dois cuidados declarados.

- `_render_home` é um método de mixin que a GUI monta com widgets reais. O dublê
  tem de interceptar **a função pura**, não o widget — senão a E3 troca uma
  muralha de texto por uma muralha de GTK, que é pior.
- **Dois dos três arquivos desta entrega são vizinhos da E1:**
  `test_home_autoswitch_lock_hint.py` e `test_wrapper_banner.py` estão na lista
  dos 13 módulos que **não coletam** no CI quando os 17 saem (risco 3 da E1).
  Mexer neles agora é seguro — a E3 não tira arquivo nenhum da coleta — mas
  quem executar a E1 vai reencontrá-los, e o commit que der a eles o
  `instalar_stubs_gi` próprio resolve as duas entregas de uma vez.

---

## E4 (barato). Duas pastas prometem camadas que não existem, e escondem as que existem

`tests/integration/` e `tests/shell/` têm **um arquivo cada, `__init__.py`
vazio**, desde maio (`ls -la` nos dois). A conta real da árvore:

```
$ find tests -name 'test_*.py' | sed 's|/[^/]*$||' | sort | uniq -c
    1 tests/core
  349 tests/unit
```

E a cobertura de shell **existe**, só que classificada como `unit`: **40
arquivos** de `tests/unit` combinam `subprocess.{run,Popen,check_output,check_call}`
com um caminho `.sh` — `test_install_headless.py:46` monta um script e o executa
com `bash -c`; `test_check_anonymity.py:43-47` roda o portão de verdade dentro de
um repositório falso; mais `test_dkms_lib.py`, sete `test_doctor_*.py`, os três
`test_bt_*.py`. (A auditoria contou 39; meu critério é ligeiramente diferente e
dá 40. O ponto não muda.)

**Isto não é achado novo, e a sprint registra:** a
[PROMESSA-NÃO-CUMPRIDA-01](2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md)
já mediu os dois diretórios vazios em 26/07 (`:227` e `:234`), e o mapa de
interfaces repetiu em 27/07 (`:135`, `:166`). É pendência de cinco dias, com
um custo pequeno e um risco que ninguém escreveu ainda.

**A entrega é uma escolha entre duas, e a segunda é mais cara do que parece:**

- **(a) apagar os dois diretórios.** A árvore passa a contar a verdade: existem
  `unit` e `core`, e os testes de shell moram em `unit`. Custo: dois `git rm`.
- **(b) mover para `tests/shell/` os 40 arquivos que executam `.sh`.** Fica mais
  bonito e **exige mexer no CI no mesmo commit**.

**O risco medido da opção (b), e é o motivo de eu recomendar a (a):** o CI roda
`pytest tests/unit` (`ci.yml:265-271`) e `pytest tests/core` (`:274-275`), e
**mais nada**. Mover 40 arquivos para `tests/shell/` sem acrescentar o passo
apaga 40 arquivos de cobertura do CI **em silêncio** — o censo de coleta
continuaria verde, porque ele varre `tests` inteiro (`:238`), e a execução
perderia os arquivos sem uma linha vermelha. Seria a mesma classe de defeito que
esta sprint inteira ataca.

**Aceite:** ou os dois diretórios somem, ou eles têm arquivo de teste **e** um
passo próprio no `ci.yml`; e o número de testes executados pelo CI antes e
depois da mudança é o mesmo, publicado no corpo do commit.

**Mordida:** um teste que lê `.github/workflows/ci.yml` e exige que **todo**
diretório sob `tests/` que contenha `test_*.py` apareça em algum passo de
execução. Sabotagem que tem de reprovar: criar `tests/shell/test_x.py` sem <!-- ref-externa: nome hipotético — o arquivo que a sabotagem criaria; não existe de propósito -->
acrescentar o passo — hoje isso passa despercebido, e é exatamente o buraco da
opção (b).

**Risco:** baixo na opção (a); médio na (b), pelo motivo acima.

---

## E5 (barato). Os cinco `os.fork()` num processo com threads

Os **únicos cinco avisos** de toda a suíte são o mesmo aviso:

```
tests/unit/test_single_instance.py:81: DeprecationWarning: This process
(pid=8697) is multi-threaded, use of fork() may lead to deadlocks in the child.
```

Nas linhas **81, 142, 302, 351 e 459**, nos testes
`test_takeover_mata_predecessor`, `test_bring_to_front_chama_callback`,
`test_takeover_ignora_pid_reciclado`, `test_takeover_mata_predecessor_hefesto` e
`test_bring_to_front_ignora_pid_reciclado`. O CPython avisa que `fork()` depois
de criar threads pode deixar o filho em deadlock — e o lugar onde isso acontece
é justamente o teste de **takeover de instância**, que mata o predecessor. Hoje
passa; é o tipo de intermitência que aparece em runner carregado, e a casa já
gastou uma correção inteira (`e74077c`) num teste que só reprovava no 3.10.

**A entrega:** trocar `os.fork()` por `subprocess` (ou `multiprocessing` com
`spawn`) nos cinco. Os testes já dependem de PID real e de arquivo de PID em
`XDG_RUNTIME_DIR`, então sobrevivem à troca.

**Aceite:** a suíte termina com **0 warnings** — hoje são 5, todos deste
arquivo; e os cinco testes continuam provando o que provavam.

**Mordida:** sabote `acquire_or_takeover` para **não** matar o predecessor. Os
cinco têm de reprovar por **teto de espera**, nunca pendurar: o teste que
depende de outro processo morrer precisa de um limite explícito, senão troca um
flake por um travamento (é a mesma lição do `e74077c`, do outro lado).

**Risco:** médio, e o cuidado é específico: o filho de hoje **herda o
monkeypatch do pai** — `test_single_instance.py:76-79` troca
`_is_hefesto_dualsense4unix_process` por `lambda pid: True` antes do `fork`, e o
comentário `:71-75` explica que isso existe porque no CI o `cmdline` do filho
não contém o marcador `hefesto`. Com `subprocess`, o filho nasce limpo: a
substituição precisa virar variável de ambiente ou argumento do script filho, e
o teste tem de continuar medindo o **fluxo de takeover**, não a heurística de
detecção (que já tem testes próprios).

---

## A pendência que não é defeito: no commit local desta máquina não há portão

Medido:

```
$ git config core.hooksPath            → /home/vitoriamaria/.config/git/hooks
$ git config --global core.hooksPath   → /home/vitoriamaria/.config/git/hooks
```

Com o `core.hooksPath` global apontando para fora do repositório, o git **nunca**
executa `.git/hooks/*`, e a própria ferramenta `pre-commit` recusa instalar. Os
**quatro** hooks declarados em `.pre-commit-config.yaml` (`acentuacao-strict:28`,
`glifos:40`, `anonimato:46`, `ruff-check:51`) não rodam no caminho do commit.

**Isso é decisão documentada, não lapso.** Está no cabeçalho do próprio arquivo
(`.pre-commit-config.yaml:1-17`, com a frase *"no caminho do COMMIT desta
máquina, quem protege é o CI"*), veio da
[PORTÃO-VIVO-01](2026-07-27-PORTAO-VIVO-01-os-gates-que-ninguem-roda.md) bloco B,
e a dívida foi paga do outro lado: o job `pre-commit` do `ci.yml:395-401` roda
`pre-commit run --all-files` a cada push, *"onde `hooksPath` de ninguém
alcança"*.

O que fica registrado como consequência operacional, porque custou caro uma vez:

- **commit local nunca é barrado por portão** — quem reprova é o CI, depois do
  push. Rodar os scripts à mão antes de empurrar é o único jeito de saber antes;
- **e a ordem importa:** `check_anonymity.sh` usa `git grep` (`:48`) e é **cego a
  arquivo não rastreado**. O próprio script escreve a lição em `:22`: *"o commit
  `f319c6f` entrou vermelho por causa disso"*. **`git add` primeiro, portões
  depois** — sempre;
- **e nem todo portão é assim:** `validar-referencias-docs.py` percorre o
  **disco** de propósito (`:125-127`: *"`git ls-files` é cego a arquivo novo
  ainda não adicionado ao índice"*), então ele enxerga untracked — foi por isso
  que ele acusou os documentos desta rodada antes de qualquer `git add`. Dois
  portões, duas visões da árvore: quem for escrever o terceiro precisa escolher
  qual, e dizer qual escolheu.

---

## Como você valida na tela

Esta sprint inteira é de teste. **Se ela mudar um pixel, ela extrapolou.** É
isso que você confere, e dá para conferir sem terminal:

1. Abra a janela e passe pelas nove abas com Ctrl+PageDown. **Nada pode ter
   mudado de lugar, de tamanho ou de texto.** Qualquer diferença visível
   reprova a leva, mesmo que a suíte esteja verde.
2. Aba **Status** com o controle ligado: o card, a barra de bateria e o quadro
   de estado continuam iguais aos de antes da leva.
3. Aba **Sistema**: o log continua abrindo e o daemon continua respondendo —
   nenhuma entrega daqui encosta no daemon vivo.

E se você quiser a resposta em número, é uma linha só no terminal:

```
$ .venv/bin/python -m pytest tests/ -q
```

Tem de terminar com **6097 ou mais**, `0 failed`, e — depois da E5 — **0
warnings**.

**Onde o seu olho é o único juiz (regra da
[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)):**
se um dos 17 arquivos, ao ganhar a guarda, **reprovar** contra o GTK real, isso
não é problema de teste — é defeito de janela que estava escondido atrás de um
widget de mentira. Nesse caso a leva **para**, o defeito vira sprint própria com
foto antes e depois, e a decisão de consertar é sua. Consertar caladinho no meio
de uma faxina de testes é exatamente o que esta casa não faz.

---

## O que fica de fora desta sprint, por escrito

- **Reescrever os 297 testes.** A entrega da E1 é dar-lhes a guarda e o job
  certo, não redesenhá-los. Um teste que roda contra GTK real e continua fraco é
  outro assunto, e ele fica para quando a E1 mostrar qual deles é.
- **As 11 ocorrências de espelho e as 2 guardas de ausência.** Ficam como estão,
  por decisão: as guardas têm a justificativa escrita na docstring
  (`test_autoswitch_lock.py:508-511`) e os espelhos acompanham contraparte no
  mesmo arquivo. O que vale registrar é a ressalva do E3: dois desses arquivos
  não entram no job `gtk-real`, e isso se resolve pela E1, não aqui.
- **Os 346 asserts que grepam shell** (medidos no mapa de 27/07, `:166`).
  Defensável enquanto não houver `bats` no projeto — e a E4 explica por que
  mover os arquivos de shell é mais caro do que parece.
- **A migração em massa dos ~240 asserts de texto de 25/07.** Ficou registrada
  naquele estudo como trabalho grande e independente, e continua fora. Esta
  sprint mexe em 8 deles, escolhidos por serem os que não têm contraparte.
- **O emblema de testes do README** (`README.md:13` diz 6089, medido 6097). É a
  E6 da [PUBLICAÇÃO-FIEL-01](2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md),
  e derivá-lo do CI é o jeito de ele não descolar de novo.
- **Gravar a fixture `hid_capture_bt.bin`.** Depende do controle dela na mesa; a
  decisão (gravar ou retirar a alegação do ADR-008) é a E8 da
  [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md).
- **Mexer no `core.hooksPath` global.** É configuração da máquina dela, fora do
  repositório, e a casa já escolheu o outro caminho (o CI). Não se toca por
  causa de uma sprint de testes.
- **Rodar `pre-commit run --all-files` criando ambiente novo.** Os quatro hooks
  foram executados direto pelos scripts, com exit 0 em todos; reproduzir o job
  do CI aqui criaria ambiente e não era o pedido.

---

## O que eu não medi

- **A suíte sob `HEFESTO_EXIGE_GTK_REAL=1` e sob Xvfb**, como o job `gtk-real`
  roda de verdade. Li a seleção e o ambiente no `ci.yml` e simulei a ausência do
  PyGObject bloqueando o `gi` por `meta_path` — não assisti a um run do runner.
  A simulação reproduz o sintoma certo (arquivo com guarda some da coleta,
  arquivo sem guarda roda verde contra `object`), mas não é o runner.
- **Os beneficiários dos lotes B, C e D, um a um.** Medi o lote A (limpo) e a
  remoção dos 17 juntos (13 erros de coleta + 19 falhas). Não medi qual dos 17
  sustenta qual dos 15 — a lista por lote é a primeira coisa a levantar antes de
  cada commit, e é medição de dois minutos.
- **A cobertura por arquivo dos 17.** Medi o agregado (72% com, 71% sem o lote
  A, 63% sem os 17); não sei qual arquivo carrega qual linha, e parte da queda
  de 63% é dos 15 módulos que deixam de coletar, não dos 297 em si.
- **Flakiness.** Dois runs completos (124,62 s e 134,87 s), o que não basta para
  afirmar estabilidade dos testes de fork e de tempo. Os cinco avisos da E5 são
  o único sinal visível.
- **A classificação das 22 leituras de fonte da segunda família.** Contei e
  amostrei duas (`test_dedup_guard.py:120-124` e
  `test_footer_salvar_nasce_acima_dos_catch_all.py:145-152`); as outras 20 podem
  ser espelho legítimo, portão de árvore inteira ou muralha, e não vou chutar.
- **Os dois desvios por transporte em `backend_pydualsense.py:1452` e `:1718`.**
  Vi que existem; não medi se algum teste os alcança.
- **Se algum dos 17, com a guarda posta, reprova contra o GTK real.** Só rodando
  para saber — e é a razão de a E1 ser por lotes e de a validação na tela ser
  dela.
- **O custo em tempo do job `gtk-real` com 297 testes a mais.** O job já morreu
  de OOM uma vez na estreia (registrado em `ci.yml:377-382`), e a lista dele vai
  crescer 44% se a E1 for paga inteira.
- **O cliente do broker contra o broker VIVO** da máquina dela. O `conftest`
  desvia todo teste para um socket inexistente de propósito, e o daemon dela
  está no ar. Não encostei.
