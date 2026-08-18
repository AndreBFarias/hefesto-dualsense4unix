# PERFIL-SALVA-TUDO-01 — salvei em todas as abas e só parte ficou

- **Status:** **PARCIAL — a E3 está ENTREGUE EM CÓDIGO, AGUARDANDO A PALAVRA
  DELA; as E1, E2, E4, E5 e E6 seguem ABERTAS.** Remarcada em 09/08/2026: as
  abas Emulação e Início ganharam escritor de rascunho em `2bbfa22` e `665aff7`
  (30/07/2026), com o gesto de máscara acrescentado em `ae32c10` (06/08/2026).
  **Rótulo anterior: "ABERTA — medida ponta a ponta, nenhuma linha de código
  escrita"**, preservado aqui. Ver a nota datada no fim
- **O que falta ela validar, em uma linha (só da E3):** mexer no seletor de Modo
  e na máscara, salvar o perfil, fechar e reabrir a janela — e ver os dois
  valores voltarem como ela deixou
- **ATENÇÃO — a queixa-mãe NÃO está curada.** A E1 (o gate que rebaixa) e a E2
  (o 5 mágico) continuam abertas, e são elas que respondem por *"salvei e só
  parte ficou"*
- **Prioridade:** CRÍTICA — é a queixa-mãe *"a configuração que eu deixo nunca é
  respeitada"* na sua forma mais direta: ela mexe, ela salva, e o arquivo nasce
  com metade do trabalho e com valores de fábrica no lugar da outra metade
- **Faixa:** 1 — o produto desfaz trabalho dela, em silêncio, no gesto que
  existe para preservá-lo
- **Aberta em:** 29/07/2026, a partir da queixa dela de hoje
- **Pedido dela:** *"fiz alterações em todas as abas e salvei o perfil, e essas
  configurações de outras abas não ficam salvas"* — a transcrição **literal**,
  com a grafia dela intacta, está na seção abaixo
- **Impacto para ela:** ela mexe em cinco abas, clica em Salvar, a janela
  continua mostrando tudo certo — e o arquivo em disco nasce com metade do
  trabalho e com valores de fábrica no lugar da outra metade. A perda só aparece
  quando ela reabre a janela ou quando o perfil reativa e o hardware volta ao
  que o arquivo diz
- **Medido** nos arquivos de perfil dela em
  `~/.config/hefesto-dualsense4unix/profiles/`, no journal do usuário e no
  código no `HEAD` (`e8e18b9`). Nada foi executado do projeto.

## O sintoma, nas palavras dela

Transcrito **literalmente**, sem correção de grafia nem de acento — é o que ela
escreveu:

```
temos o perfil do jogo tipo pragmata, ai em todas as abas fiz alteracoes e
salvei o perfil, ai essas configs de outras abas nao ficam salvas
```

## O fato que resume a sprint

**O "Salvar Perfil" grava as cinco seções que o rascunho POSSUI e reescreve como
padrão de fábrica as cinco que ele apenas TRANSPORTA.**

| seção | o rascunho a edita? | o que acontece no save |
|---|---|---|
| `triggers` | sim (`app/actions/triggers_actions.py:289-290`) | **gravada** |
| `leds` | sim (`app/actions/lightbar_actions.py:286`, `:695`) | **gravada** |
| `rumble` | sim (`app/actions/rumble_actions.py:242`, `:298`) | **gravada** |
| `mouse` | sim (`app/actions/mouse_actions.py:273`, `:288`) | **gravada** |
| `key_bindings` | sim (`app/actions/input_actions.py:354`) | **gravada** |
| `controllers` (por MAC) | sim (`app/actions/triggers_actions.py:302`, `app/actions/lightbar_actions.py:291`) | **gravada** |
| `match` | não — só transporta | **reescrita** como `{"type": "any"}` |
| `priority` | não — só transporta | **reescrita** como `5` |
| `mode` | não — só transporta | **reescrita** como `null` |
| `suppress_desktop_emulation` | não — só transporta | **reescrita** como `false` |
| `mic` | **nunca recebeu escritor nenhum** | sempre `null` |

E as abas continuam mostrando o certo depois do save, porque elas leem o
**rascunho em memória**, não o disco. **A janela mente a favor dela** — e ela só
descobre a perda quando reabre a janela ou quando o perfil reativa e o hardware
volta ao que o arquivo diz.

## O que foi medido — a cadeia, elo por elo

### Elo 1 — a fotografia nasce certa

`app/app.py:947` chama `_bootstrap_draft_async` (definido em `app/app.py:690`),
que roda `_compute_draft_from_active_profile` (`app/app.py:629`) numa thread
worker: ele lê `active_profile` do `daemon.state_full`, acha o perfil no disco
com `load_all_profiles()` e monta o rascunho com `DraftConfig.from_profile`
(`app/app.py:651-654`).

Nesse momento, `app/draft_config.py:391-396` grava a **fotografia** do perfil de
origem: `source_match`, `source_mode`, `source_suppress`, `source_priority`,
`source_controllers` e `source_name`.

O perfil ativo dela é `Pragmata2` — o daemon o restaurou de
`~/.config/hefesto-dualsense4unix/session.json` (`{"last_profile":
"Pragmata2"}`).

### Elos 2 a 5 — cinco abas ESCREVEM no rascunho

| aba | onde escreve |
|---|---|
| Gatilhos | `app/actions/triggers_actions.py:289-290` (global, via `_persist_params_to_draft`, definido em `:261`) e `:302` (override por MAC) |
| Lightbar | `app/actions/lightbar_actions.py:286` (cor/brilho/LEDs de jogador), `:291` (por MAC), `:695` (cores automáticas) |
| Vibração | `app/actions/rumble_actions.py:242` (política) e `:298` (multiplicador) |
| Navegação/Mouse | `app/actions/mouse_actions.py:273` e `:288` |
| Teclado | `app/actions/input_actions.py:354` (e `:305`, o "limpar") |

**Essas funcionam.** As quatro seções de hardware estão **preenchidas** nos dois
arquivos dela.

### Elo 6 — a aba EMULAÇÃO não escreve uma linha no rascunho

```
$ grep -c 'self\.draft' src/hefesto_dualsense4unix/app/actions/emulation_actions.py
0
```

Os três gestos dela nessa aba vão direto ao estado vivo do daemon:

- "Modo jogo" -> `app/actions/emulation_actions.py:664` ->
  `_set_suppress` (`:635`) -> IPC `daemon.emulation.suppress` (`:649`);
- máscara -> `app/actions/emulation_actions.py:617`/`:625`/`:632` ->
  `_apply_mode` (`:593`) -> `apply_mode` (`:615`);
- microfone -> `app/actions/emulation_actions.py:430`/`:447` -> script externo
  (`_run_mic`, `:411`).

**Nada disso encosta no rascunho.**

### Elo 7 — a aba INÍCIO também não

```
$ grep -c 'self\.draft' src/hefesto_dualsense4unix/app/actions/home_actions.py
0
```

Modo em `app/actions/home_actions.py:973-997`, máscara em `:1004`, co-op em
`:1040-1076`, cadeado em `:1082-1112` — todos IPC global.

### Elo 8 — o gesto de salvar

`app/actions/footer_actions.py:257` abre
`gui_dialogs.prompt_profile_name(default_name=active_name)` — um campo de texto
**livre** (`app/gui_dialogs.py:64-66`: um `Gtk.Entry` pré-preenchido com o nome
ativo). Depois, `app/actions/footer_actions.py:281`:

```python
return save_profile(draft.to_profile(nome))
```

### Elo 9 — o gate que decide entre preservar e zerar é uma igualdade de string crua

`app/draft_config.py:463`:

```python
mesmo_perfil = self.source_name is not None and name == self.source_name
```

**Igualdade de string crua, sem slug.** O projeto **tem** a comparação por slug —
`profiles/slug.py:52`, `mesmo_slug`, cuja docstring (`:53-59`) conta o R-10:
*"com 'Navegação' no disco, salvar um perfil chamado 'Navegacao' (sem acento)
passava batido pelas duas guardas... e o arquivo `navegacao.json` era substituído
SEM aviso nenhum"*. Ela é usada em `app/actions/profiles_actions.py:1492` e em
`:1441`. **Não é usada aqui.**

### Elo 10 — o estrago, com `mesmo_perfil` False

`app/draft_config.py:466-477`:

```python
priority=(self.source_priority if (mesmo_perfil and ...) else priority),
match=(self.source_match if (mesmo_perfil and ...) else MatchAny()),
mode=self.source_mode if mesmo_perfil else None,
suppress_desktop_emulation=self.source_suppress if mesmo_perfil else False,
```

E `priority` é o **default do parâmetro**, `app/draft_config.py:399`:

```python
def to_profile(self, name: str, priority: int = 5) -> Profile:
```

### Elo 11 — a seção `mic` morre em silêncio, nas duas pontas

`app/draft_config.py:442-446` emite `mic=None` porque `self.mic.dirty` e
`self.mic.in_profile` são False. E **nada** na janela os liga:

```
$ grep -rn 'MicDraft' src/hefesto_dualsense4unix/ | grep -v app/draft_config.py
(vazio — zero escritores)
$ grep -in 'toggles_system' src/hefesto_dualsense4unix/gui/main.glade
(vazio — zero widgets)
$ grep -rn 'profile\.mic' src/hefesto_dualsense4unix/profiles/manager.py \
     src/hefesto_dualsense4unix/daemon/lifecycle.py
(vazio — zero leitores na ativação)
```

O único consumidor é `daemon/ipc_draft_applier.py:391-411` (`_apply_mic`,
chamado em `:87`) — e ele nunca recebe a seção, porque `to_ipc_dict` a gateia em
`self.mic.dirty` (`app/draft_config.py:901-905`).

**Medido em todos os 15 perfis dela: `mic` é `null` ou ausente em todos.**

### Elo 12 — o disco

`profiles/loader.py:629` grava o dump denso. O resultado, lido do disco dela:

```
~/.config/hefesto-dualsense4unix/profiles/pragmata2.json   (mtime 27/07 23:01:35)
{
  "name": "Pragmata2",
  "match": {"type": "any"},          <-- ramo "nome novo"
  "priority": 5,                     <-- default do parametro
  "triggers": {"left": {"mode": "SemiAutoGun", "params": [3, 6, 8]},
               "right": {"mode": "Pulse", "params": []}},   <-- PREENCHIDO
  "leds": {"lightbar": [97, 53, 131], "lightbar_brightness": 1.0,
           "auto_player_colors": true},                     <-- PREENCHIDO
  "rumble": {"passthrough": true, "policy": "economia"},    <-- PREENCHIDO
  "key_bindings": null,
  "mouse": null,
  "mic": null,
  "mode": null,
  "suppress_desktop_emulation": false,
  "controllers": {"a0fa9c0000f0": {"leds": {"lightbar": [97, 53, 131]}}}  <-- PREENCHIDO
}
```

### Elo 13 — a fotografia não é reapontada, e o SEGUNDO save rebaixa de novo

`app/actions/footer_actions.py:283-299` (`_on_saved`) atualiza
`_active_profile_name` (`:287`) e `_draft_baseline` (`:292`), mas **não** chama
`with_profile_identity`.

```
$ grep -rn 'with_profile_identity' src/ tests/
src/hefesto_dualsense4unix/app/actions/profiles_actions.py:1497
```

**Um único chamador**, e ele é da aba Perfis. Consequência: o **segundo**
"Salvar Perfil" com o mesmo nome novo cai no ramo "nome novo" **outra vez** e
rebaixa o perfil que ela acabou de criar.

### Elo 14 — o caminho alternativo (aba Perfis) também descarta

`app/actions/profiles_actions.py:1576` só usa o rascunho como base quando
`_edita_o_perfil_do_rascunho(name)` (`:1414-1451`) devolve True — que exige
`mesmo_slug(name, ativo)` ou que a linha selecionada seja o perfil ativo num
rename. Com o ativo = `Pragmata2` e ela salvando `Pragmata` selecionado na lista,
devolve **False** e `app/actions/profiles_actions.py:1596` usa **o disco** como
base: todas as edições das outras abas são descartadas sem aviso. E
`app/actions/profiles_actions.py:1059-1064` nem chama `profile_switch` (o salvo
não é o ativo), então nada muda na tela nem no controle.

O comentário de `app/actions/profiles_actions.py:1563-1573` já registra
exatamente essa classe de estrago e cita a conclusão dela: *"as configs que eu
faço não impactam"*.

### Elo 15 — o efeito no hardware, na próxima ativação

`profiles/manager.py:463-480` aplica `suppress_desktop_emulation` **do arquivo**
em toda ativação (False, para ela) e `profiles/manager.py:487-500` aplica `mode`
do arquivo (`null`). O "modo jogo" e a máscara que ela deixou são desfeitos.

Medido no journal dela, no minuto seguinte ao save de 27/07:

```
2026-07-27T23:01:42.855117 profile_apply_respeita_override_manual categorias=['led', 'rumble', 'trigger'] profile=Pragmata2
2026-07-27T23:01:42.855498 profile_mode_revert_skipped mode_from_profile=None motivo=catch_all_sem_opiniao profile=Pragmata2
2026-07-27T23:01:42.855540 profile_activated name=Pragmata2 origin=manual priority=5
```

O `mode_from_profile=None` do arquivo **em ação**, e o `priority=5` carimbado no
próprio log de ativação.

## A causa

**Duas causas somadas, as duas em `app/draft_config.py`.**

**(1) O gate é uma igualdade de string crua e ninguém reaponta a fotografia.**
`app/draft_config.py:463` decide o que reemitir comparando o nome digitado com
`draft.source_name`. Qualquer nome que não bata **exatamente** faz `priority`,
`match`, `mode` e `suppress_desktop_emulation` nascerem do zero
(`app/draft_config.py:466-477`). E o rodapé — **único** consumidor desse gate —
nunca reaponta `source_name` depois de gravar
(`with_profile_identity`, `app/draft_config.py:514`, tem um chamador só:
`app/actions/profiles_actions.py:1497`).

**(2) Três seções do esquema não têm escritor nenhum na janela:**

- `mic` — nenhum widget no `gui/main.glade`, nenhum escritor de `MicDraft`,
  nenhum leitor na ativação;
- `suppress_desktop_emulation` (`profiles/schema.py:444`) — a aba Emulação manda
  `daemon.emulation.suppress` (`app/actions/emulation_actions.py:649`) e o
  comentário de `app/actions/emulation_actions.py:661` diz por escrito: *"Suppress
  suspende SÓ mouse/teclado e NÃO persiste"*;
- `mode` — só a aba Perfis o escreve, via `_mode_section_from_editor`
  (`app/actions/profiles_actions.py:452`, usado em `:1621`).

**A cura de 28/07 não alcança isto.** O commit `8d7fd45` ("Salvar pela aba
Perfis parou de rebaixar", 28/07 19:44) cobriu **só** `match`/`priority` e **só**
no caminho da aba Perfis (`app/actions/profiles_actions.py:1637-1652`). O
`git show 8d7fd45 --stat` lista 12 arquivos e **`draft_config.py` não está entre
eles**. O último commit que tocou `app/draft_config.py` é `d92b544`, de **25/07
19:12**.

## O que NÃO é a causa

### O rascunho NÃO desconhece as seções das abas

**REFUTADO.** `DraftConfig` (`app/draft_config.py:271`) tem `triggers`, `leds`,
`rumble`, `mouse`, `emulation`, `mic` e `key_bindings`. **Cinco** delas têm
escritor real (tabela do "fato que resume"), e as quatro seções de hardware estão
**preenchidas** nos dois arquivos dela.

### NÃO é "salva tudo mas o daemon não reaplica"

**REFUTADO.** `app/actions/profiles_actions.py:1059-1064` chama `profile_switch`
quando o perfil salvo é o ativo (o daemon relê o disco) e
`profiles/manager.py:231` reaplica. O defeito não está em reaplicar: está **no que
o arquivo passou a dizer**.

### NÃO é a cura de 28/07 que ainda não está instalada

**REFUTADO.** A cura existe e está no `HEAD`:
`app/actions/profiles_actions.py:1637-1644` calcula `prioridade_final` e
`regra_final` e só reescreve se ela mexeu. Ela cobre **só** `match`/`priority` e
**só** no caminho da aba Perfis; `draft_config.py` não é tocado desde 25/07.

### NÃO é o autoswitch sobrescrevendo depois de salvar

**REFUTADO.** O cadeado está ligado
(`~/.config/hefesto-dualsense4unix/autoswitch_locked.flag` = `1`) e o journal
mostra `autoswitch_congelado_pelo_cadeado candidate=Navegação current=
wm_class=steam` em 28/07 21:07:25 e de novo hoje em 17:13:38, 18:11:49 e
20:14:33. Quem desfaz o trabalho dela é **a ativação** (boot, `profile_switch`,
restauro do último perfil) lendo o arquivo empobrecido.

### A aba NÃO mente mostrando o valor errado — ela mente A FAVOR dela

**REFUTADO, e é o contrário.** As abas Gatilhos/Lightbar/Vibração/Navegação leem
o **rascunho** (`_refresh_all_tabs`, `app/actions/footer_actions.py:593`, chamado
em `app/app.py:711`) e continuam mostrando o valor **certo** mesmo depois de o
arquivo perder as seções. Por isso a perda só aparece quando ela **reabre a
janela** (o bootstrap lê o disco, `app/app.py:648-654`) ou quando o perfil
reativa.

### A prioridade 5 NÃO foi escolha dela no slider

**REFUTADO.** O cálculo de prioridade da aba Perfis é
`_prioridade_acima_dos_catch_all` (`app/actions/profiles_actions.py:1398-1412`),
que soma `_FOLGA_ACIMA_DO_CATCH_ALL = 10`
(`app/actions/profiles_actions.py:78`) ao maior catch-all do disco, e o teto da
escala é `PRIORIDADE_MAXIMA = 200` (`app/actions/profiles_actions.py:74`). O
número 5 não vem de gesto nenhum: é o default do parâmetro em
`app/draft_config.py:399`.

```
$ grep -rn 'priority: int = 5' src/hefesto_dualsense4unix/
src/hefesto_dualsense4unix/app/draft_config.py:399
```

**Uma ocorrência.** E o único chamador que a deixa cair no default é
`app/actions/footer_actions.py:281` — o outro,
`app/actions/profiles_actions.py:1585`, sobrescreve com
`base.update({"priority": prioridade_final})` em `:1646-1652`.

**Prioridade 5 num arquivo é assinatura digital de save pelo rodapé, no ramo
"nome novo".** Refinamento honesto da medição: dos cinco catch-all dela, só
`pragmata.json` e `pragmata2.json` têm 5. `meu_perfil.json` tem 1, `vitoria.json`
e `fallback.json` têm 0 — esses vieram por outro caminho e não são prova deste
defeito.

### O "Aplicar" e o "Salvar" NÃO gravam as mesmas seções

**REFUTADO, e a diferença importa.**

| | Aplicar (`app/draft_config.py:866-918` -> `daemon/ipc_draft_applier.py:74-87`) | Salvar (`app/draft_config.py:464-499`) |
|---|---|---|
| `leds`, `triggers`, `controllers` | sim | sim |
| `rumble` | só `weak`/`strong` | `passthrough`/`policy`/`custom_mult` |
| `mouse` | **só velocidade**, sem `enabled` (HARM-05) | seção inteira |
| `keyboard`/`key_bindings` | sim | sim |
| `mic` | gateado por `dirty` (`:901-905`) — nunca chega | sempre `None` |
| `match`, `priority`, `mode`, `suppress` | não | sim, **do jeito errado** |

Nenhum dos dois toca `mode`/`suppress` a partir de gesto dela. E a **política**
de vibração nunca viaja no Aplicar: ela é aplicada na hora pela própria aba
(`app/actions/rumble_actions.py:246`).

### A aba Perfis NÃO lê de volta as outras seções

**Medido, e é o que sustenta a E6.** `_populate_editor`
(`app/actions/profiles_actions.py:1228-1316`) preenche nome (`:1240`),
prioridade (`:1242`), modo (`:1245`) e regra (`:1247+`).

```
$ grep -n 'leds\|triggers\|rumble\|mouse\|key_bind\|mic' \
    src/hefesto_dualsense4unix/app/actions/profiles_actions.py \
    | awk -F: '$1>=1228 && $1<=1316'
(vazio)
```

**Nenhuma superfície da janela mostra o que o ARQUIVO diz dessas seções.**

## Como isto aparece no disco dela — a assinatura digital

`pragmata.json` (mtime 27/07 23:00:50) e `pragmata2.json` (mtime 27/07 23:01:35)
são **byte-idênticos fora o campo `name`**:

```
$ diff <(sed 's/"Pragmata2"/"X"/;s/"Pragmata"/"X"/' pragmata.json) \
       <(sed 's/"Pragmata2"/"X"/;s/"Pragmata"/"X"/' pragmata2.json)
(vazio)
```

Dois perfis com a mesma regra (`any`), a mesma prioridade (5) e a mesma
configuração. É o EMPATE-01 nascendo do mesmo mecanismo — e o journal confirma
que os cinco competem entre si a cada janela de jogo:

```
2026-07-29T18:53:00.631528 profile_select_catch_all_sem_autoridade_em_jogo \
  candidatos=['Pragmata', 'Pragmata2', 'fallback', 'meu_perfil', 'vitoria'] \
  wm_class=steam_app_3357650
```

E o daemon tem **vivo** o que os perfis não têm:
`gamepad_emulation.flag` = `dualsense` e
`mouse_emulation.flag` = `{"enabled": false, "speed": 9, "scroll_speed": 1}` —
máscara e velocidade **vivas** no daemon e **ausentes** dos dois perfis
(`mode: null`, `mouse: null`).

## O rastro que não existe

```
$ journalctl --user --since 2026-07-25 -o cat | grep -cE 'footer_|gui_'
0
```

Nem `footer_save_profile_ok` (`app/actions/footer_actions.py:285`) nem
`gui_draft_reconciliado` (`app/app.py:762`) chegam ao journal: a janela sobe pelo
`.desktop`, não por unit. E não existe arquivo de log da janela —
`~/.local/state/hefesto-dualsense4unix/` tem `kernel.log`, `storm.log`,
`launch_env/`, `proton-pin-lock.json`, `broker-owner.conf` e
`cmdline-owners.conf`, e **nada de GUI**. E o handler `profile.apply_draft`
(`daemon/ipc_handlers.py:434-456`) **não loga sucesso**: um "Aplicar" que
funcionou não deixa linha.

**O rastro indireto que sobra**, e ele é preciso: `launch_env_materializado` (o
`_notify_launch_env_refresh` que todo save chama —
`app/actions/footer_actions.py:298` e `app/actions/profiles_actions.py:1081`)
aparece no journal em **28/07 21:13:26.132**, e o mtime de `meu_perfil.json` é
**28/07 21:13:26.104**. **Vinte e oito milissegundos** de distância, e sem nenhum
`profile_switch`/`profile_activated` na sequência — a assinatura exata de salvar
um perfil que **não** é o ativo.

**Consequência prática:** enquanto a E5 não entrar, **a única forma de medir um
save é mtime + conteúdo do JSON**.

## As entregas

Ordenadas por preço crescente.

### E1 — fechar o gate que rebaixa

**O que faz:**

- (a) `mesmo_perfil` passa a comparar por **slug**, com o `mesmo_slug` que o
  projeto já tem (`profiles/slug.py:52`) — "Navegação" e "Navegacao" deixam de
  ser perfis diferentes no gate que decide preservar;
- (b) o rodapé **reaponta a fotografia** depois de gravar:
  `self.draft = draft.with_profile_identity(profile)` no `_on_saved`, do mesmo
  jeito que a aba Perfis faz em `app/actions/profiles_actions.py:1497`.

**Os arquivos:** `app/draft_config.py:463`;
`app/actions/footer_actions.py:283-299`.

**Como PROVAR (o teste que morde):**

- **Teste A:** salvar pelo rodapé com um nome NOVO **duas vezes seguidas** e
  exigir que a segunda gravação preserve `match`/`priority`/`mode`/`suppress` da
  primeira. **Este teste já está vermelho hoje**: o segundo save volta a
  `MatchAny`, prioridade 5 e `mode: None`. Arrancar a linha do
  `with_profile_identity` o faz reprovar de novo.
- **Teste B:** `source_name = "Navegação"`, salvar como `"Navegacao"`, exigir
  preservação de `match` e `priority`. Arrancar o `mesmo_slug` reprova.
- **Teste C, o que morde do outro lado:** um save deliberado com nome novo tem de
  continuar nascendo `MatchAny` no **primeiro** save. É o contrato R-11
  (`app/draft_config.py:448-462`), e a medição que o justifica está escrita ali:
  *"com o FPS ativo, 'Salvar Perfil' como 'MadJack' produzia um perfil com o
  regex de título do FPS e prioridade 60"*.

**Risco:** o teste **tem** de morder dos dois lados (A/B e C). Sem C, a cura
reabre "perfil novo nasce com a regra de outro perfil".

### E2 — tirar o 5 mágico

**O que faz:** remove o default `priority: int = 5` da assinatura de `to_profile`
e obriga o chamador a passar a prioridade que a usuária **vê na tela** (a do
perfil de origem, ou a calculada por `_prioridade_acima_dos_catch_all`). Nenhum
perfil pode sair da janela com um número que ela não escolheu.

**Os arquivos:** `app/draft_config.py:399` e `:466-470`;
`app/actions/footer_actions.py:281`.

**Como PROVAR (o teste que morde):** salvar pelo rodapé com um perfil de
prioridade 100 na origem e exigir 100 (ou o valor calculado) no arquivo — nunca
5. Devolver o default `= 5` à assinatura faz o teste reprovar. Mais um portão de
busca: `priority: int = 5` não pode existir como default em nenhuma assinatura de
gravação.

**Risco:** BAIXO, e o efeito colateral é o desejado — um chamador esquecido passa
a estourar `TypeError` em vez de gravar silenciosamente errado. Exige varrer os
**dois** callsites (`app/actions/footer_actions.py:281` e
`app/actions/profiles_actions.py:1585`) e os dublês de teste.

### E3 — dar escritor de rascunho às abas Emulação e Início

**O que faz:** `mode` (máscara/nativo/desktop + co-op) e
`suppress_desktop_emulation` — **o "modo jogo" dela, que ela ESCLARECEU hoje ser
suspender mouse e teclado** — deixam de ser somente estado vivo e passam a ser
**configuração do perfil**: o gesto na aba escreve no rascunho, e o "Salvar
Perfil" persiste.

**Os arquivos:** `app/actions/emulation_actions.py:615`, `:649`, `:664`, `:667`;
`app/actions/home_actions.py:973-997`, `:1004`, `:1040-1076`;
`app/draft_config.py:301-303` e `:476-477` (os campos deixam de ser `source_*`
só-transporte e ganham donos editáveis);
`app/actions/profiles_actions.py:1620-1621`.

**Como PROVAR (o teste que morde):**

1. ligar "modo jogo" na aba Emulação -> Salvar Perfil -> o JSON tem
   `suppress_desktop_emulation: true`. Arrancar a escrita no rascunho reprova;
2. **o que morde de verdade:** reativar o perfil e exigir que o applier de
   `profiles/manager.py:463-480` receba `True`. Hoje ele recebe **sempre** o
   `False` do arquivo, então este teste **já nasce vermelho**.

**Risco:** **ALTO, e precisa do olho dela.** Os cinco perfis dela são catch-all;
um `suppress: true` persistido num catch-all **suspende mouse e teclado no
desktop dela**. Depende do gate R-02 (`_perfil_tem_opiniao`,
`daemon/lifecycle.py:1472`, alcançado pelo `profile=profile` que
`profiles/manager.py:468` já passa ao applier) e de validação na tela: ligar,
salvar, **sair do jogo**, confirmar que o mouse volta.

Ver também a sprint irmã EMULACAO-NO-JOGO-01: lá, a supressão automática por
sinal de jogo foi **descartada** justamente porque `apply_profile_suppression`
recusa liberar em catch-all (`daemon/lifecycle.py:1472-1478`,
`IGNORADO_CATCH_ALL`). **As duas entregas conversam** e não podem ser feitas em
desacordo.

### E4 — decidir o destino de `Profile.mic`

**O que faz:** ou o campo ganha widget na aba Emulação (ao lado do liga/desliga
do microfone que já existe lá, `app/actions/emulation_actions.py:430`/`:447`),
escritor de `MicDraft` e um applier no `ProfileManager` — ou **sai do esquema**.
Hoje ele é fantasma nas duas pontas.

**Os arquivos:** `profiles/schema.py:322-346` e `:435`;
`app/draft_config.py:140-160` e `:442-446`; `gui/main.glade` (bloco do microfone
da aba Emulação); `profiles/manager.py:446-520` (applier novo, ao lado do
mouse/supressão/modo); `daemon/ipc_draft_applier.py:391-411` (**já pronto do
outro lado**).

**Como PROVAR (o teste que morde):** ponta a ponta — marcar o toggle na aba,
salvar, reativar o perfil e exigir `daemon.config.mic_button_toggles_system`
mudado. Hoje passa vazio dos **dois** lados (não escreve e não lê), então o teste
nasce vermelho em dois pontos independentes: arrancar só o applier, ou só o
widget, o mantém vermelho.

**Risco:** MÉDIO, e o cuidado é de **posse**, não de código. Não confundir este
campo com a posse do microfone: `mic unmute` **toma a posse** e mata o botão
físico até `mic release`. Este campo só decide se o botão do controle alterna o
mute do sistema. Se as duas coisas se misturarem, um perfil salvo pode deixar o
botão físico dela morto.

### E5 — rastro e limpeza

**O que faz:**

- (a) remove os dois campos mortos do rascunho: `EmulationDraft.xbox360_enabled`
  (`app/draft_config.py:132-137`) e `LedsDraft.mic_led`
  (`app/draft_config.py:73`) — zero referências fora do próprio arquivo
  (medido: `grep -rn 'EmulationDraft\|xbox360_enabled' src/` fora de
  `draft_config.py` = 0; `grep -rn 'mic_led' src/hefesto_dualsense4unix/app/`
  fora de `draft_config.py` = 0);
- (b) faz salvar e aplicar **deixarem rastro**: o structlog da janela passa a
  escrever num destino que sobrevive (arquivo em
  `~/.local/state/hefesto-dualsense4unix/` ou o journal), e o handler
  `profile.apply_draft` (`daemon/ipc_handlers.py:455-456`) loga o resultado com
  `applied`/`failed`.

**Os arquivos:** `app/draft_config.py:73`, `:132-137`, `:271-293`;
`utils/logging_config.py`; `daemon/ipc_handlers.py:455-456`.

**Como PROVAR (o teste que morde):** salvar um perfil e exigir, no destino de
log, uma linha com o nome do perfil **e a lista das seções gravadas**. Hoje o
`grep -cE 'footer_|gui_'` no journal dá 0 e não existe arquivo de log — o teste
nasce vermelho. Para os campos mortos: portão de busca que reprova qualquer campo
do `DraftConfig` sem escritor **nem** leitor.

**Risco:** MÉDIO-BAIXO, com uma armadilha nomeada: **não logar caminho de perfil
com MAC dentro**. O mapa `controllers` é indexado por MAC (o override dela é
`a0fa9c0000f0`) e há purga de MAC no histórico deste repositório. O log da janela
tem de nascer com o mesmo higienizador do resto.

### E6 — a janela passa a MOSTRAR o que está no arquivo

**O que faz:** a aba Perfis ganha um painel de **leitura** com as seções que hoje
ela não exibe (lightbar, gatilhos, vibração, mouse, teclado, mic, modo,
supressão, overrides por controle) e um **aviso quando o rascunho em memória
diverge do disco**. É o fim do "a janela mostra certo e o arquivo está errado".

**Os arquivos:** `app/actions/profiles_actions.py:1228-1316`; `gui/main.glade`
(painel de resumo na aba Perfis); `app/actions/footer_actions.py:593`
(`_refresh_all_tabs`); `app/app.py:728-731` (`_tem_edicao_pendente`, que **já
calcula** a divergência e hoje só serve ao aviso de troca de perfil em
`app/app.py:749-755`).

**Como PROVAR (o teste que morde):**

1. com o disco dizendo `mode: null` e o rascunho dizendo gamepad, a aba tem de
   exibir o aviso de divergência. Arrancar o aviso reprova;
2. o painel de leitura **nunca** pode sobrescrever o rascunho dela sem gesto
   explícito — mutar o painel para escrever no rascunho reprova.

**Risco:** MÉDIO-ALTO, todo em produto. Nunca recarregar o rascunho a partir do
disco sem gesto dela — a lição R-08 está escrita em `app/app.py:739-743`:
*"Recarregar por baixo de uma edição é perda de trabalho, que é justamente a
queixa que este conjunto de correções ataca"*. O painel é **leitura**; um botão
"trazer do disco" precisa de confirmação. E a validação na tela é obrigatória
porque **é a única entrega que muda o desenho de uma aba que ela já reprovou uma
vez** (a Status, em 27/07: *"só distanciou as coisas"*).

## O que NÃO fazer

### NÃO migrar os arquivos dela em silêncio

`pragmata.json`, `pragmata2.json`, `meu_perfil.json` e `vitoria.json` ficam como
estão **até ela decidir**. Migração silenciosa foi a classe que causou o rollback
de 26/07, e o próprio `8d7fd45` registra a decisão de não tocar no perfil já
instalado.

### NÃO afrouxar `mesmo_perfil` a ponto de um nome NOVO herdar a regra de origem no PRIMEIRO save

Reabre o R-11 (`app/draft_config.py:448-462`), em que "Salvar como MadJack" com o
FPS ativo produzia um perfil com o regex de título do FPS e prioridade 60 — e
nenhuma regra para o jogo dela.

### NÃO persistir `suppress_desktop_emulation: true` num perfil catch-all sem o gate R-02

Os cinco perfis dela são catch-all (medido nos arquivos e no journal de hoje). Um
`suppress` persistido em catch-all **suspende mouse e teclado no desktop dela** —
trocaria uma perda de configuração por um desktop sem ponteiro. Os **únicos dois**
perfis dela que hoje têm `suppress: true` (`sackboy_nativo.json` e
`coop_local.json`) casam por `criteria`, e isso não é coincidência.

### NÃO gravar `rumble.passthrough: false` a partir do "Aplicar"/"Parar"

`app/actions/rumble_actions.py:361-384` documenta que isso congela a trava no
JSON e ressuscita "testei os motores e o jogo não vibra mais"
(SPRINT-GAME-RUMBLE-01) junto com o RUMBLE-PRESO-01.

### NÃO densificar as entradas parciais de `controllers` em nenhum caminho novo

`app/actions/profiles_actions.py:1597-1605` e `app/draft_config.py:500-510`
avisam, os dois, que `model_dump` marca os defaults do esquema como explícitos e
**apaga a lightbar do controle**. O override dela — `a0fa9c0000f0`, com **só**
`leds.lightbar` — é exatamente uma entrada parcial em risco.

### NÃO tocar nos três perfis que dependem do que têm

`point_and_click.json` é o **único** dos 15 com `key_bindings` próprio
(`r1 -> KEY_DOT`) e com `mouse.enabled: true`. `sackboy_nativo.json` e
`coop_local.json` são os **únicos dois** com `suppress_desktop_emulation: true`.
Qualquer migração tem de deixar esses três byte-idênticos.

### NÃO tentar diagnosticar o próximo save pelo journal

`journalctl --user --since 2026-07-25 | grep -cE 'footer_|gui_'` = **0** e não
existe arquivo de log da janela. Enquanto a E5 não entrar, medir save é **mtime +
conteúdo do JSON**.

### Exige o olho dela na tela — quatro provas

1. Ligar "modo jogo" na aba Emulação, salvar o perfil, **fechar e reabrir a
   janela**, e conferir que a aba mostra "ligado". É o único teste que separa "o
   arquivo tem" de "a janela mostra".
2. Depois de (1), **sair do jogo** e confirmar que mouse e teclado **voltam**. Se
   não voltarem, a E3 fez estrago pior que o defeito.
3. Com `Pragmata` e `Pragmata2` empatados, salvar **um** e conferir que o **outro
   não mudou** (mtime **e** conteúdo). O rename/sobrescrita por slug já comeu um
   perfil dela em silêncio antes (R-10, `profiles/slug.py:53-59`).
4. Conferir que a prioridade que ela vê no slider é a que fica no arquivo. É o
   número que decide qual configuração vale, e hoje ele nasce 5 sem ela ter
   tocado em nada.

## O que fica sem medição

- **Não vi a tela dela.** Toda afirmação sobre o que a janela mostra vem de
  leitura do `gui/main.glade` e do Python que o preenche, não de captura. As
  quatro provas de tela acima existem por isso.
- **Não sei qual save produziu qual arquivo.** A janela não deixa rastro
  (`grep -cE 'footer_|gui_'` = 0), então a atribuição é por **assinatura**
  (prioridade 5 + `match: any` + seções nulas + `launch_env_materializado` no
  mesmo milissegundo), não por log. É evidência forte e circunstancial, não
  registro.
- **Não sei o que ela mexeu em cada aba naquela sessão.** A queixa diz "em todas
  as abas"; o disco mostra quatro seções de hardware preenchidas e cinco
  reescritas. Qual gesto ela fez na aba Emulação e na Início naquele momento é
  relato, não medição.
- **Não reproduzi o save.** Nenhum script do projeto foi executado, nenhum perfil
  foi gravado. Todos os "como PROVAR" são projeto de teste, não teste existente,
  e **nenhum foi executado**.
- **Não medi o comportamento do rename.** `_edita_o_perfil_do_rascunho`
  (`app/actions/profiles_actions.py:1414-1451`) tem um ramo dedicado a rename que
  li mas não exercitei; o efeito de E1 sobre ele é raciocínio, não medição.
- **Não sei se `Pragmata` e `Pragmata2` deveriam ser dois perfis.** Eles são
  byte-idênticos fora o nome. Pode ser que ela tenha querido dois; pode ser que o
  segundo tenha nascido de uma tentativa de consertar o primeiro. **É pergunta
  para ela**, e a resposta muda se a cura deve incluir apagar um.
- **Não olhei os presets de fábrica.** `acao`, `aventura`, `corrida`, `esportes`,
  `fps` carregam `mode: {"kind": "gamepad", "gamepad_flavor": "xbox"}` da migração
  de 25/07 18:28 (já registrada na PERFIL-JOGO-01, entrega 6, e ainda **aberta**).
  Não avaliei a interação disso com E3.

---

## NOTA DATADA — 09/08/2026: a E3 saiu, e a queixa-mãe continua devendo

**Nada acima foi apagado.** A medição ponta a ponta e as seis entregas continuam
inteiras — inclusive as cinco que **ainda devem**, que são a maioria e são as
que respondem pela queixa que abriu a sprint.

**O que está de pé — GRAU: MEDIDO em 09/08/2026 contra a árvore de hoje.**

| entrega | estado | onde está |
|---|---|---|
| **E3** — dar escritor de rascunho às abas Emulação e Início | ENTREGUE EM CÓDIGO, aguardando a palavra dela | `src/hefesto_dualsense4unix/app/actions/home_actions.py:529` (*"o gesto de MODO chega ao RASCUNHO"*) e `src/hefesto_dualsense4unix/app/actions/profiles_actions.py:592`, `:803`, `:829` — as quatro linhas citam a sprint por nome |

**Commits:** `2bbfa22` e `665aff7` (30/07/2026); a máscara como gesto de modo
(`profiles_actions.py:803`) entrou em `ae32c10` (06/08/2026).

### O que continua ABERTO nesta sprint — e não foi remarcado

- **E1** — fechar o gate que rebaixa.
- **E2** — tirar o 5 mágico.
- **E4** — decidir o destino de `Profile.mic`.
- **E5** — rastro e limpeza.
- **E6** — a janela passa a MOSTRAR o que está no arquivo.

**Isto importa mais que a marca:** a E1 e a E2 são a causa direta de *"salvei em
todas as abas e só parte ficou"*. Enquanto elas não entrarem, **a queixa dela
continua de pé**, e esta sprint não pode ser lida como resolvida.

### Por que a E3 não é ENTREGUE e sim ENTREGUE EM CÓDIGO

Porque a própria sprint tem uma seção chamada *"Exige o olho dela na tela —
quatro provas"*, e nenhuma das quatro foi feita. Os cinco perfis dela são
catch-all: a sprint mediu risco **ALTO** e disse, por escrito, que precisa do
olho dela.
