# PS-TOQUE-CURTO-01 — o gesto de religar o controle abre a Steam

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA** — aconteceu **duas vezes em 45 segundos** na sessão
  de 02/08, e a segunda abriu uma segunda Steam
- **Faixa:** 1 — o produto age contra a usuária
- **Causa-raiz:** **PROVADA no código e no journal.** Não precisa de medição
  nova para executar esta sprint
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Evidência:** [a sessão de quatro controles](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md),
  seção *"O achado principal"*

---

## O sintoma, na mesa dela

O controle cai no Bluetooth. Ela segura o botão PS por alguns segundos para
religá-lo — que é **como se liga um DualSense**, e o gesto que o hardware
ensina. Quando solta, **a Steam abre**.

Na segunda vez, com a Steam já aberta, ele **abriu outra**.

## A prova, em milissegundos

Do journal de 02/08 (a ordem é o achado — leia a coluna da esquerda):

```
21:10:41.479  uhid_motion_streaming      on=False player=1
21:10:41.486  touchpad_reader_read_lost  [Errno 19] path=/dev/input/event259
21:10:41.495  motion_sensors_read_lost   [Errno 19] path=/dev/input/event258
21:10:41.519  evdev_read_lost            [Errno 19] path=/dev/input/event257
21:10:41.525  ps_solo_released           held_ms=5032.8
21:10:41.538  wmctrl_binary_not_found
21:10:41.538  ps_button_action_steam     outcome=refocus_fallback_spawn
21:10:41.538  steam_spawn_requested
```

**Os devices morrem `.479`–`.519`; o PS é solto `.525`.** O botão é a *reação*
dela à queda, não a causa dela. E `held_ms=5032.8` — **cinco segundos** — foi
classificado como *"toque curto"*.

O primeiro episódio, 44 segundos antes, é idêntico: `held_ms=5038.2`,
`outcome=spawned`.

## A causa-raiz

### Elo 1 — o ramo do "toque curto" não tem teto de duração

`integrations/hotkey_daemon.py:212-224`:

```python
if long_press_fired:
    # Long-press ja disparou neste hold — o release não abre Steam.
    logger.debug("ps_solo_suppressed_by_long_press", ...)
    return None

# Release sem combo nem long-press — considera PS solo (toque curto).
held_ms = (t - pressed_at) * 1000
logger.info("ps_solo_released", held_ms=round(held_ms, 1))
self._fire_ps_solo()
return "ps_solo"
```

O comentário **afirma** "toque curto". O código não verifica duração nenhuma. A
única barreira contra um hold longo é `long_press_fired`.

### Elo 2 — o long-press nasce DESLIGADO, então a barreira nunca arma

`daemon/main.py`, na construção do `DaemonConfig`:

> *"FEAT-EMULATION-GAMEMODE-COMBO-01: modo jogo e' so pelo combo PS+Options.
> Default 0 = long-press DESLIGADO (evita o modo-jogo acidental); quem quiser o
> gesto seta `HEFESTO_DUALSENSE4UNIX_PS_LONG_PRESS_MS>0`."*

E `daemon/lifecycle.py:159`: `ps_long_press_ms: int = 0`.

Com `ps_long_press_ms == 0`, `long_press_fired` é **sempre `False`**. Logo
**toda** duração de hold cai no ramo do toque curto — 200 ms ou 5.038 ms, o
mesmo caminho.

**As duas decisões estão certas isoladamente.** Desligar o long-press evitou o
modo-jogo acidental (defeito real, com sprint própria). Tratar o release como
toque é o comportamento normal. O defeito é a **composição**: desligar o
long-press removeu, sem querer, o único teto que existia.

### Elo 3 — a documentação já descreve o comportamento certo

`README.md`, tabela de atalhos: **"PS (toque curto) → abre a Steam"**.

O documento está certo e o código não o implementa. Não há discussão de produto
a fazer: **é só honrar o que já está escrito.**

### Elo 4 — sem `wmctrl`, o dano dobra

`21:10:41.538  wmctrl_binary_not_found` → `outcome=refocus_fallback_spawn`.

Conferido na máquina dela: **`wmctrl` não está instalado**, o `install.sh` não o
instala, o `packaging/debian/control` não o declara e o `scripts/doctor.sh` não
o confere. Só `integrations/steam_launcher.py:30` (`WMCTRL_BINARY = "wmctrl"`) o
usa. Sem ele, "trazer a Steam para frente" vira "abrir a Steam".

### E o que JÁ funcionava — a regra da casa

Esta hipótese explica por que o defeito nunca apareceu antes:

- **no cabo o controle não cai**, então ninguém segura o PS para religar;
- **um toque curto de verdade** (~200 ms) sempre funcionou e continua
  funcionando — a cura não o toca;
- o defeito exige a combinação **Bluetooth instável + gesto de recuperação**,
  que é exatamente a noite de 02/08 e não as sessões anteriores no cabo.

---

## As entregas

### E1 — o "toque curto" ganha teto de duração

Um release cujo hold passou do teto **não é toque**: não dispara ação nenhuma, e
loga o motivo.

**Onde:** `integrations/hotkey_daemon.py`, no ramo das linhas 220-224.

**O valor do teto** é decisão de produto com dois candidatos, e a sprint
recomenda o primeiro:

- **(a) 700 ms**, constante nomeada (`PS_TOQUE_CURTO_TETO_MS`). É folgado para
  um toque humano (um clique intencional fica em 80–250 ms) e corta com sobra os
  5.038 ms medidos. **Recomendado**: número único, sem configuração nova para
  ela entender;
- **(b) reaproveitar `ps_long_press_ms` quando > 0 e cair em 700 ms quando == 0.**
  Mais "elegante" e **pior**: amarra dois gestos independentes ao mesmo número, e
  o dia em que ela ligar o long-press em 2000 ms o toque curto vira 2 s.

**Aceite:** segurar o PS por 5 s e soltar **não abre a Steam**. Um toque de
~200 ms abre, como sempre abriu.

**Não é gambiarra e o porquê:** não estamos filtrando o sintoma ("ignorar o
release quando um controle acabou de cair"). Estamos fazendo o código cumprir a
definição que ele próprio declara em comentário e que o README publica.

### E2 — o hold longo deixa de ser silencioso

Hoje, um hold de 5 s some no `ps_solo_released` como se fosse um toque. Depois
da E1 ele passa a ser recusado — e a recusa tem de **aparecer**, senão a próxima
investigação vai procurar o que não existe:

```
ps_solo_ignorado_hold_longo  held_ms=5032.8  teto_ms=700
```

**Aceite:** o journal distingue as três saídas do botão — toque honrado, hold
longo recusado, combo/long-press suprimido — e cada uma tem evento próprio.

### E3 — `wmctrl` vira dependência declarada, ou a dependência morre

Duas saídas honestas, e a sprint **não escolhe** porque a escolha é de produto:

- **(a) declarar:** `install.sh` instala, `packaging/debian/control` declara,
  `scripts/doctor.sh` confere e ensina o comando. Barato, mas acrescenta um
  binário externo ao caminho quente;
- **(b) remover a dependência:** trazer a janela ao foco pelos backends de
  janela que o projeto **já tem** (`integrations/window_backends/`, com xlib,
  portal e wlrctl). O `steam_launcher` seria o único lugar do projeto a chamar
  um binário externo para uma pergunta que o próprio projeto sabe responder.

**Recomendação:** (b), porque o `wmctrl` é X11-only e ela roda COSMIC/Wayland —
declarar uma dependência que não funciona no compositor dela é dívida nova. Mas
(b) é maior, então (a) é aceitável como passo intermediário **desde que fique
registrado que é intermediário.**

**Aceite:** com a Steam já aberta, o botão PS a traz para a frente — **ou** diz
por que não pode. Nunca abre uma segunda.

### E4 — o teste que morde

Três testes, e o critério de mordida está escrito para não se repetir o erro de
teste que passa com a cura arrancada:

1. `hold de 5038 ms → nenhuma ação disparada`. **Arranque o teto e veja
   reprovar**;
2. `hold de 200 ms → ação disparada`. Protege contra a cura virar "o botão PS
   parou de funcionar";
3. `hold de 5038 ms → o evento de recusa foi logado com held_ms e teto_ms`. Um
   teste que só afirma "não disparou" não distingue *recusado* de *engolido*.

**Onde:** `tests/unit/`, ao lado dos testes existentes de hotkey
(`test_hotkey_*.py`).

---

## Testes que vão reprovar

```
pytest tests/unit -k "hotkey or ps_solo or steam_launcher"
```

Atenção a testes-muralha que travem o texto do ramo do toque curto ou a ausência
de teto. Se algum exigir que **toda** duração dispare, ele **é** a regressão —
encare-o, não afrouxe a cura.

## O que NÃO fazer

- **Não religar o long-press por default** para "resolver de graça". Ele foi
  desligado por um defeito real (modo-jogo acidental) e religá-lo troca um
  defeito por outro;
- **Não filtrar pelo estado do controle** ("ignorar o PS quando um device caiu
  nos últimos N ms"). É contorno: amarra dois subsistemas que não têm relação e
  quebra no dia em que o hold longo acontecer sem queda nenhuma;
- **Não tratar o `ps_solo` como causa da queda dos controles.** A ordem dos
  milissegundos já refutou isso, e a refutação está no estudo. Quem inverter vai
  mandar a cura para o lugar errado;
- **Não declarar `wmctrl` sem conferir se ele funciona no COSMIC/Wayland dela.**

## O que fica ABERTO depois desta sprint

- **por que o controle cai** — esta sprint cura a *reação* ruim à queda, não a
  queda. A queda é a `BT-QUE-NAO-CAI-01`;
- **a escolha entre (a) e (b) da E3**, que é dela.
