# COOP-QUE-NÃO-DESMONTA-01 — o Jogador 2 que dura dois segundos

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA** — é o eixo do pedido dela (*"que eu não note que estou
  no bt ou cabo"*). Quatro ciclos de entra-e-sai em 22 minutos de uso real
- **Faixa:** 1 — o produto desmonta sozinho durante a partida
- **Causa-raiz:** **PROVADA no código e no journal**, em três elos independentes
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Evidência:** [a sessão de quatro controles](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md)
- **Relacionada:** [PS-TOQUE-CURTO-01](2026-08-03-PS-TOQUE-CURTO-01-o-gesto-de-religar-o-controle-abre-a-steam.md)
  (o gesto de recuperação que piora o ciclo)

---

## O sintoma, na mesa dela

Dois DualSense por Bluetooth. O Jogador 2 entra, e **dois segundos depois sai**.
Volta, sai de novo. Quatro vezes em 22 minutos. Entre uma e outra, ela plugou o
cabo — duas vezes.

## A prova

Do journal de 02/08, só as linhas do ciclo:

```
21:07:45  coop_player_added    identity=a0:fa:9c:00:00:f0  player=2  players=2
21:10:15  coop_player_removed  identity=a0:fa:9c:00:00:f0            players=1
21:10:42  coop_player_added    identity=14:3a:9a:00:00:ab  player=2  players=2
21:10:44  coop_player_removed  identity=14:3a:9a:00:00:ab            players=1
21:19:10  coop_player_added    identity=a0:fa:9c:00:00:f0  player=2  players=2
21:28:16  coop_player_removed  identity=a0:fa:9c:00:00:f0            players=1
21:28:24  coop_player_added    identity=a0:fa:9c:00:00:f0  player=2  players=2
23:37:05  coop_player_removed  identity=a0:fa:9c:00:00:f0            players=1
```

E o instante exato da morte do segundo ciclo — **dois segundos de vida**:

```
21:10:41.866  evdev_started            path=/dev/input/event30
21:10:41.867  coop_player_grab_pending path=/dev/input/event30  player=2   <- o co-op pega
21:10:42.135  coop_player_added        identity=14:3a:9a:00:00:ab player=2
21:10:43.700  controller_primary_bound transport=usb                       <- o primário MUDA
21:10:43.754  evdev_started            path=/dev/input/event30             <- o primário pega
21:10:43.754  evdev_grab_failed        [Errno 16] EBUSY
                                       hint='o controle pode dobrar input'
21:10:44.116  coop_player_removed      identity=14:3a:9a:00:00:ab players=1
```

**O `EBUSY` não veio da Steam nem do jogo. Veio de dentro do próprio daemon:**
o co-op pegou o `event30` como Jogador 2 às `.867`, e 1,9 s depois o leitor do
primário foi apontado para o **mesmo** `event30`.

---

## A causa-raiz, em três elos

### Elo 1 — o co-op define "quem é secundário" subtraindo o primário

`daemon/subsystems/coop.py:321,333-337`:

```python
primary = self._primary_identity()
...
want = {
    mac: str(path)
    for mac, path in discover_dualsense_evdevs().items()
    if mac != primary
}
```

E `daemon/subsystems/coop.py:349-350`:

```python
for mac in list(self._players):
    if mac not in want:
        self._teardown_player(mac)
```

**Se o primário muda, o conjunto `want` muda — e quem era secundário vira o
primário, sendo destruído como jogador.**

### Elo 2 — o primário é re-eleito sozinho quando o antigo cai, e o que volta nunca o retoma

`core/backend_pydualsense.py:1651-1661`, e a docstring diz por extenso:

> *"Primário = 1ª chave de inserção ainda presente (`next(iter(...))`).
> Controles novos entram no fim, então nunca roubam o primário de um já
> conectado; se o primário cai, promove o próximo mais antigo."*

A decisão está **certa** e resolveu um defeito real (com dois controles, "menor
node" e "primário do backend" divergiam e o P1 lia outro controle). O que ela
não previu é a **frequência**: no cabo o primário praticamente nunca cai; por
Bluetooth, cair é rotina. Cada queda promove outro controle e faz o Elo 1
disparar.

### Elo 3 — a guarda contra a colisão existe, mas só cobre o boot

`daemon/subsystems/coop.py:326-333`:

```python
# BUG-COOP-BOOT-PRIMARY-DUP-01: o conjunto `want` é keyed por MAC; se o
# primário ainda não resolveu o MAC (`primary_uniq` None no boot/restart
# com controles já plugados → fallback "path:"), não há como excluí-lo de
# `want` e um secundário nasceria para o PRÓPRIO controle do P1 (input
# DOBRADO até o próximo sync ~2s). Adia enquanto não há MAC do primário;
if primary is None or primary.startswith("path:"):
    logger.debug("coop_sync_defer_primary_sem_mac", primary=primary)
    self._retry_spawn = True
    return
```

**A guarda protege o caso "o primário ainda não tem MAC".** Ela não protege o
caso *"o primário mudou de MAC enquanto um secundário já segurava aquele
device"* — que é o que a reconexão por Bluetooth produz o tempo todo.

### E o que JÁ funcionava — a regra da casa

- **no cabo**: o primário é estável, `want` não muda, e o ciclo nunca dispara;
- **com um controle**: não há secundário para colidir;
- **com dois no cabo**: as três coisas acima valem juntas.

O defeito exige *reconexão frequente do primário* — ou seja, exige Bluetooth. É
por isso que a suíte inteira passa: ela é **cega a BT por construção**, e isso
já está registrado nesta casa como bug recorrente ("a premissa USB-é-o-mundo").

---

## As entregas

### E1 — a troca de primário deixa de destruir o jogador que já existe

O `sync` precisa distinguir dois casos que hoje colapsa num só:

- **o controle sumiu da mesa** → derrubar o jogador está certo;
- **o controle continua na mesa e virou o primário** → o jogador tem de ser
  *transferido*, não destruído: solta-se o grab do secundário, o primário assume,
  e o vpad daquele MAC é **desmontado explicitamente** — nunca com um `EBUSY` no
  meio.

**Onde:** `daemon/subsystems/coop.py`, no laço de teardown (linhas 347-376).

**A ordem importa e é o coração da entrega:** hoje o primário é rebindado
(`core/backend_pydualsense.py:1672`, `_evdev.retarget`) **antes** de o co-op
saber que ele mudou — e a colisão acontece nessa janela de ~2 s (o `sync` roda
no poll loop a 2,0 s, `daemon/lifecycle.py:3529-3531`; o `connect()` roda no
`reconnect_loop`, `daemon/connection.py:393`). A cura é o backend **avisar** a
troca de primário, e o co-op soltar antes do retarget — não o co-op descobrir
depois, pelo `EBUSY`.

**Aceite:** derrubar e religar o controle primário por Bluetooth, com um segundo
controle ativo, **não** produz `evdev_grab_failed` e **não** remove o Jogador 2.
Medível no journal: zero `EBUSY` no ciclo.

**Por que é raiz e não contorno:** não estamos aumentando um retry nem
adiando o teardown. Estamos fazendo os dois donos do mesmo `event` combinarem a
transferência, em vez de descobrirem a colisão pelo erro do kernel.

### E2 — a re-eleição do primário deixa de ser gratuita quando o controle volta

Hoje, o controle que cai e volta entra **no fim** do dict e nunca retoma o
posto. Consequência com quatro controles: depois de algumas quedas, quem é o
Jogador 1 é essencialmente aleatório — e o Jogador 1 é quem alimenta o vpad que
o jogo lê como controle 1.

**Duas saídas, e a sprint recomenda a primeira:**

- **(a) primário estável por identidade**: o backend guarda qual MAC *era* o
  primário e o devolve ao posto quando ele reaparece dentro de uma janela (por
  exemplo, a mesma janela de graça que o projeto já usa para reconexão).
  Recomendado — é o que preserva a experiência dela: *"o meu controle continua
  sendo o jogador 1 depois de cair"*;
- **(b) deixar como está e absorver na E1.** Mais barato, e aceitável se a E1
  entregar a transferência limpa — mas não resolve o embaralhamento de quem é
  o Jogador 1.

**Aceite de (a):** o controle que era o Jogador 1, ao cair e voltar em menos de
N segundos, volta a ser o Jogador 1.

**Armadilha nomeada:** `_recompute_primary` re-atrela o evdev **e** re-detecta o
transporte (`_detect_transport`). Uma "estabilidade" que devolva o posto sem
refazer essas duas coisas deixa o daemon achando que o controle está no cabo
quando ele voltou por rádio. Ver a docstring em `backend_pydualsense.py:1652`.

### E3 — o número do jogador para de trocar de dono

`daemon/subsystems/coop.py:398-408` (`_next_player_index`) devolve o **menor
índice livre ≥ 2**, e o índice é liberado no teardown
(`daemon/subsystems/coop.py:905`). Esse índice vira **a identidade do vpad no
kernel**: `integrations/uhid_gamepad.py:539`,
`f"02:fe:00:00:00:{player:02x}"`, carimbado no feature `0x09`
(`integrations/uhid_gamepad.py:1088`).

Com três ou mais controles e uma queda no meio, **o MAC do vpad do Jogador 2
passa a pertencer a outra pessoa**. Em jogo que salve por slot de dispositivo,
os perfis trocam de dono.

**A cura NÃO é "não reusar o índice"** — e isto precisa ficar escrito porque é a
correção intuitiva e errada: o jogo quer P1..PN **contíguos**, e MAC duplicado
mata o probe do uhid com `-EEXIST` (`daemon/subsystems/coop.py:566-570`). A cura
é **desacoplar o MAC do vpad do número exibido**: o MAC passa a derivar da
identidade do controle (um hash estável do uniq), e o número continua contíguo.

**Aceite:** o mesmo controle físico, caindo e voltando com outros na mesa,
mantém o mesmo MAC de vpad. E nenhum instante tem dois vpads com o mesmo MAC.

### E4 — o teste que morde: a bancada dos quatro controles com queda programável

**Esta é a entrega mais valiosa da sprint**, e a que impede tudo isto de voltar.

Não existe hoje bancada que rode `_poll_loop` + `reconnect_loop` + `CoopManager`
contra o **mesmo relógio virtual**. Enquanto ela não existir, cada subsistema
continua verde sozinho — que é exatamente o estado dos 6792 testes durante a
noite ruim dela.

**O que a bancada precisa ter:**

- um enumerador falso que alimente `_enumerate_device_keys` **e**
  `discover_dualsense_evdevs` a partir de um roteiro temporal, com os nós evdev
  **renumerados no retorno** (é o que o replug por BT faz de verdade);
- um roteiro mínimo que reproduz a noite dela:
  `t=0: A,B` → `t=5: B` (o primário A cai) → `t=8: B,A` (A volta com node novo);
- relógio virtual, para o `sync` de 2 s e o `connect()` do `reconnect_loop`
  correrem em ordens diferentes de propósito.

**As asserções que MORDEM** (arranque a cura e veja cada uma reprovar):

1. nenhum `evdev_grab_failed` durante o roteiro inteiro;
2. o vpad que o jogo enxerga como Jogador 1 continua alimentado pelo **mesmo
   MAC** do começo ao fim;
3. nenhum MAC muda de `player_index` sem que aquele controle tenha saído da mesa;
4. nenhum instante tem dois MACs com o mesmo MAC de vpad.

**Onde:** `tests/unit/`, arquivo novo. A suíte é cega a BT por construção — esta
bancada é o começo da cura disso, e vale para as sprints irmãs desta leva.

---

## Testes que vão reprovar

```
pytest tests/unit -k "coop or primary or identity or vpad"
```

Atenção especial a testes que travem o **texto** do `_next_player_index` ou o
formato `02:fe:00:00:00:0N` do MAC — a E3 muda esse formato de propósito, e um
teste-muralha ali **é** a barreira a encarar, não a afrouxar.

## O que NÃO fazer

- **Não aumentar o retry do grab nem adiar o teardown.** O `EBUSY` é sintoma de
  dois donos; escondê-lo com tempo deixa a janela de input dobrado aberta, que é
  o defeito que o teardown existe para evitar
  (`BUG-COOP-GRAB-SILENT-FAIL-01`);
- **Não remover o teardown por grab falho.** Ele está certo: sem grab
  confirmado, o físico dobra o input no jogo;
- **Não "resolver" fazendo o co-op ignorar o primário.** É o que a guarda
  `BUG-COOP-BOOT-PRIMARY-DUP-01` já impede, e por bom motivo: um secundário
  nascendo para o próprio controle do P1 dobra o input;
- **Não mexer nas quinze assimetrias intencionais** listadas no estudo desta
  leva sem ler o motivo de cada uma. Três delas ficam a um passo desta sprint:
  o co-op fora de `_desired_by_uniq`, o `mark_disconnected` sem chamador, e o
  `apply_output_defaults` que ignora o seletor.

## O que fica ABERTO

- **por que o controle cai** — esta sprint cura o **desmonte**, não a queda. A
  queda é a `BT-QUE-NAO-CAI-01`;
- **a escolha (a)/(b) da E2**, que é decisão de produto dela;
- **os controles externos**, que nunca entram no co-op (`want` só enumera
  `discover_dualsense_evdevs`). É outra sprint — ver o estudo, achado 5.
