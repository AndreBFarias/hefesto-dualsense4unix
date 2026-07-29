# JANELA-CEGA-01 — o detector que nunca adoece

- **Status:** PARCIALMENTE ENTREGUE (observabilidade entregue; uma linha de
  fiação e a decisão do `game_signal` ficam declaradas abaixo)
- **Prioridade:** ALTA — não desfaz trabalho dela, mas **esconde** quando o
  perfil-por-jogo está morto, que é o defeito que gera as queixas
- **Faixa:** 2 — o produto mente sobre o próprio estado
- **Aberta em:** 28/07/2026, a partir da auditoria dos achados que ficaram em
  aberto na leva de 27/07
- **Medida ao vivo nesta máquina, hoje**, no daemon dela em execução — não em
  documento antigo

## O fato que resume a sprint

**Um detector de janela cego para sempre é, bit a bit, indistinguível de um
saudável.** O daemon dela publicava saúde `true` e uma classe de janela plausível
enquanto o backend devolvia `None` a cada tique.

## A medição ao vivo — 28/07

Daemon em execução, perfil `Pragmata2`, `autoswitch_locked=true`. Resposta crua
do `daemon.state_full`:

```
window_detect_backend    = "xlib"
window_detect_healthy    = true
window_detect_last_class = "Hefesto-Dualsense4Unix"
game_signal.authority    = "daemon"
```

No MESMO minuto, sondando o servidor X do jeito que o backend sonda
(`DISPLAY=:1`, dez amostras a 10 Hz):

```
focos: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]      X.NONE == 0
_NET_ACTIVE_WINDOW: 14680071               (a propriedade rançosa, viva)
```

Dez de dez amostras **sem foco X nenhum**. O gate UX-02 faz a coisa certa e
devolve `None` nas dez. E ainda assim o estado publicado diz `healthy=true` e
exibe `"Hefesto-Dualsense4Unix"` — **a própria janela da GUI**, capturada quando
ela a teve em foco pela última vez, congelada ali como se fosse notícia fresca.

## Os três defeitos encadeados

### 1a — a flag de saúde é um trinco de mão única

Todos os escritores de `window_detect_healthy` em `daemon/state_store.py`:

| Onde | O que faz |
|---|---|
| `__init__` | nasce `False` |
| `set_window_detect_backend` | recebe a semeadura do chamador |
| `record_window_detect_read` | `= True` quando a leitura é útil |

**Nenhum caminho jamais atribui `False` depois da semeadura.** E a semeadura do
`xlib` é uma **presunção**, não medição — o comentário original dizia com todas
as letras: *"backend 'xlib' nasce saudável"*, porque só é escolhido com `DISPLAY`
presente.

### 1b — seis causas distintas colapsavam num `None` só

Em `integrations/window_backends/xlib.py`, seis saídas diferentes devolviam o
mesmo `None`: sem conexão X, foco sem id, sem foco X, foco sem top-level, foco em
desacordo com o `_NET_ACTIVE_WINDOW`, e exceção de consulta. Todas viravam
`_UNKNOWN_WINDOW` no `window_detect.py`, e o consumidor achatava de novo em
`profiles/autoswitch.py` (`_tick_sem_informacao`), onde "info vazio" e
`wm_class="unknown"` entram no MESMO ramo.

O custo: **"app Wayland nativo em foco" (normal, o dia inteiro nesta máquina) era
indistinguível de "o XWayland caiu" (grave).**

### 1c — o estado publicava só a classe STICKY

`window_detect_last_class` só é atualizado em leitura útil e **nunca decai**.
Existia um `window_detect_current_class` (a leitura crua, do NUMA-01) que **não
estava no payload IPC**. E o `daemon.status` não expunha campo `window_detect_*`
nenhum — quem olhasse o status não tinha como saber que o perfil-por-jogo estava
cego.

## Por que o backend aqui é sempre o `xlib`, e o que isso implica

`window_detect.py:detect_window_backend()` testa `DISPLAY` **primeiro**, e o
`systemd --user` desta máquina exporta `DISPLAY=:1` **e**
`WAYLAND_DISPLAY=wayland-1`. Logo, COSMIC/Wayland cai sempre no `XlibBackend`,
que só enxerga XWayland.

Consequência que **não** é defeito: jogos Proton/Steam SÃO XWayland (o journal
dela mostra `wm_class=steam_app_3357650`), então o perfil-por-jogo funciona. O
que fica invisível é o **desktop e os apps Wayland nativos** — e é por isso que
"sem foco X" precisa ser dizível, em vez de virar alarme.

## O que foi entregue

1. **A saúde que CAI, sem mexer em decisão** — `daemon/state_store.py`:
   - `window_detect_seeing(now=None)`: houve leitura útil dentro de
     `WINDOW_DETECT_BLIND_AFTER_SEC`? Cai depois do teto e **volta na primeira
     leitura útil seguinte**, sem restart;
   - `window_detect_useful_age(now=None)`: a idade da última leitura útil — o
     número que denuncia a cegueira ao lado do sticky que nunca decai;
   - `WINDOW_DETECT_BLIND_AFTER_SEC = 300.0`. **Tempo, não contagem**, e a
     justificativa importa: o tique é de 2 Hz e ficar minutos com um app Wayland
     nativo em foco é NORMAL aqui, então contar leituras não-úteis mediria o uso
     dela, não o detector. 300 s são 600 tiques seguidos sem ver **nada** — nem
     jogo, nem Steam, nem a própria GUI. Curto o bastante para a cegueira
     aparecer dentro de um café; longo o bastante para não piscar.
2. **O motivo do `None` para de se perder** — seis constantes `MOTIVO_*` em
   `window_backends/xlib.py`, uma por causa, publicadas em
   `last_failure_reason`; `sem_backend` no `NullBackend`;
   `cascata_wayland_sem_leitura` na cascata; e `janela_sem_classe` /
   `backend_sem_motivo` no leitor. O `Protocol` `WindowBackend` ficou
   **intocado** (`getattr` defensivo): backend de terceiro segue válido.
   `WindowReaderDiag.last_reason` colhe o motivo e o zera na leitura útil;
   `StateStore.record_window_detect_read(..., reason=...)` guarda ao lado da
   leitura crua.
3. **O estado passa a mostrar a cegueira** — `daemon/ipc_handlers.py` ganhou
   `_window_detect_payload()`, usado por `daemon.state_full` **e** por
   `daemon.status` (as duas respostas nunca mais divergem, e há teste que fixa
   isso). Campos novos: `window_detect_current_class` (a leitura CRUA),
   `window_detect_useful_age_sec`, `window_detect_seeing`,
   `window_detect_reason`.

## A decisão que NÃO foi tomada — e por que ela precisa entrar sozinha

O pedido era que **`window_detect_healthy`** passasse a cair. Ele **não** cai, e
isto é deliberado, com medição:

`healthy` tem um consumidor de DECISÃO — `Daemon._gather_game_signal_inputs`
alimenta `game_signal.classify`, onde, sem evidência de jogo,
`window_healthy=False` classifica a autoridade de exibição como `unknown` em vez
de `daemon`. E em `lifecycle._sync_game_signal`, a transição `daemon -> unknown`
chama **`replay_retained_game_outputs()`** — que repinta a lightbar com o que o
jogo deixou retido.

O estado dela **agora** é `game_signal.authority = "daemon"`. Fazer `healthy`
decair nesta leva significaria: a cada vez que ela passasse cinco minutos num app
Wayland nativo, a autoridade cairia para `unknown` e a lightbar seria repintada
por um resíduo de jogo — depois voltaria ao alt-tab seguinte. **Um vaivém na cor
do controle dela, entregue de lambuja numa leva de observabilidade.** É
exatamente a classe de coisa que esta casa manda entrar sozinha, com ela vendo.

Por isso a divisão ficou: **`healthy` é o fail-safe do `game_signal`** (trinco,
documentado como tal na property, com teste que fixa a decisão);
**`seeing` é a resposta honesta sobre o agora** e não decide nada.

**A leva seguinte é de uma linha**: trocar `window_healthy` de `healthy` para
`seeing` em `daemon/lifecycle.py:_gather_game_signal_inputs` — com ela olhando a
lightbar enquanto acontece.

## O que fica (e uma linha que ficou faltando)

### A fiação do motivo — uma linha, fora do escopo desta leva

O motivo chega até o leitor (`WindowReaderDiag.last_reason`) e o store sabe
guardá-lo, mas quem chama o store é `daemon/subsystems/autoswitch.py`, que não
estava no escopo desta leva. Enquanto essa linha não entrar,
`window_detect_reason` sai `null` no daemon vivo. O ponto exato, em
`_build_diag_window_reader`:

```python
store.record_window_detect_read(
    _backend_name(),
    wm_class if isinstance(wm_class, str) else None,
    reason=getattr(reader, "last_reason", None),   # <- isto
)
```

### A cascata Wayland que nunca roda aqui — 385 linhas

`window_backends/wayland_portal.py` (201) + `window_backends/wlr_toplevel.py`
(184) só são instanciados pelo `_WaylandCascadeBackend`, que só é escolhido
**sem** `DISPLAY`. Nesta máquina o `systemd --user` sempre tem `DISPLAY`. São 385
linhas de código que nunca executam aqui — e que o `doctor.sh` já mediu como
inúteis por outra via: o cosmic-comp **não** expõe
`wlr-foreign-toplevel-management`, e o portal XDG não tem `GetActiveWindow`.
Suporte real a Wayland nativo exigiria o protocolo próprio
`zcosmic_toplevel_info_v1`. Enquanto isso não existir, o honesto é a linha na
tela: **"o detector não vê janela Wayland nativa"**.

### `integrations/xlib_window.py` — 111 linhas de código morto com mina armada

Nenhum código de produção o importa (só o `tests/unit/test_xlib_window.py` e
menções em docstrings). Ele lê o `_NET_ACTIVE_WINDOW` **sem gate de foco** — ou
seja, é exatamente o defeito que o UX-02 e o FOCO-01 curaram, preservado inteiro
num arquivo que ainda importa limpo. **Mina armada para quem importar.** Ou vira
um `raise ImportError` explícito, ou some.

### A linha na aba Sistema

Fora do escopo desta leva (a aba não estava entre os arquivos liberados). Com os
campos novos no `state_full`, a linha honesta é barata:
`window_detect_seeing == false` e `backend == "xlib"` -> *"o detector não vê
janela Wayland nativa (só XWayland/jogos)"*.

## Como isto foi provado

Testes novos: `tests/unit/test_janela_cega_01_o_detector_que_adoece.py` (23) e
`tests/unit/test_aplicar_verdade_02_a_contabilidade_do_aplicar.py` (7).

Arrancando a cura (arquivos de volta ao `HEAD`, testes intactos):

- cura do store fora: **ImportError na coleta** (`WINDOW_DETECT_BLIND_AFTER_SEC`
  não existe);
- só a decadência arrancada (`seeing` virando apelido de `healthy`): **8 falhas**;
- store curado, resto fora: **18 falhas**;
- tudo recolocado: **30 verdes**; suíte inteira **5767 verdes**.

## Anexo — APLICAR-VERDADE-02, o irmão que entrou junto

O `e8f9060` curou a FRASE do rodapé ("Perfil aplicado ao controle." com nada
aplicado). Ficou de pé, declarado no próprio commit, o resto:
`app/actions/footer_actions.py` usava `ok = result.get("status") == "ok"` — e
esse `status` é fixo em `"ok"` por contrato do `profile.apply_draft` (é "recebi",
não "apliquei"). Então `_clear_mouse_dirty()` baixava a pendência da aba Mouse
com as sete seções FORA, e o journal carimbava `ok=True`.

Agora são **duas perguntas**: `aceita` (o daemon respondeu — decide a FRASE, e
com isso a cura do `e8f9060` fica de pé) e `aplicou` (alguma seção entrou —
decide o `dirty` e o journal). Mais fino ainda: a pendência do mouse só acaba se
a seção **mouse** entrou — com `applied=["leds"]` e `failed={"mouse": ...}` a
edição do mouse continua pendente, em vez de sumir em silêncio.

Compatibilidade preservada de propósito: resposta **sem** `applied` (daemon
antigo, ou o `True` cru do bridge) continua contando como aplicada — a MESMA
regra que `_mensagem_de_aplicacao` já usava para o texto. As duas não podem
divergir, e há teste para isso.

O `tests/unit/test_harmonia_mouse_um_dono.py` **não** precisou ser tocado: ele
usa `{"status": "ok"}` sem `applied`, que é justamente o caso "sem informação não
há do que desconfiar". Ele protegia algo real (o HARM-05), e continua protegendo.
