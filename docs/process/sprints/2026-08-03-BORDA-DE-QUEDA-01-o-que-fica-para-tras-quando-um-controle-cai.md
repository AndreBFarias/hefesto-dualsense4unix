# BORDA-DE-QUEDA-01 — o que fica para trás quando um controle cai

- **Status:** PROPOSTA, escrita em 03/08/2026. Nenhuma linha de código tocada
- **Prioridade:** **ALTA** — o rumble preso **voltou na sessão dela**, quatro
  vezes em 28 segundos, com valores altos nos dois jogadores
- **Faixa:** 1 — o produto deixa o hardware num estado ruim
- **Causa-raiz:** o rumble é **SUSPEITA COM MECANISMO** (a evidência é forte e o
  experimento está escrito); os outros dois são **PROVADOS no código**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Evidência:** [a sessão de quatro controles](../estudos/2026-08-03-a-sessao-de-quatro-controles-e-o-que-o-journal-provou.md),
  achado 3


> ### **JÁ MEDIDO — pode executar.**
>
> Ela confirmou em 03/08: *"desliga sozinho e o controle branco segue vibrando"*. O defeito está **reproduzido**, e a sprint está livre.

---

## A pergunta desta sprint

Por Bluetooth, um controle cair é **rotina**. O que o daemon faz na borda de
subida está bem coberto (adoção, priming, reassert, hotplug). **A borda de
descida é o buraco:** o que fica para trás quando o device some no meio de tudo.

Três coisas ficam. As três aparecem só com o rádio, e as três pioram com quatro
controles.

---

## Defeito 1 — o rumble fica preso quando o jogo NÃO CHEGA a mandar a parada

### A evidência: os dois fatos convivem, e é isso que interessa

Da sessão de 02/08:

```
5922  uhid_parada_do_sdl_honrada     <- a cura de 02/08 (commit 5801de9) FUNCIONA
   4  uhid_rumble_preso_expirado     <- e mesmo assim o rumble prendeu
```

Os quatro travamentos:

```
21:52:05  player=2  silencio_s=5.69  teto_s=3.0  ultimo=(12, 0)
21:52:15  player=1  silencio_s=3.36  teto_s=3.0  ultimo=(230, 230)
21:52:15  player=2  silencio_s=3.29  teto_s=3.0  ultimo=(114, 114)
21:52:33  player=2  silencio_s=3.9   teto_s=3.0  ultimo=(127, 0)
```

Numa janela de 50 segundos em torno deles, **43** paradas do SDL foram honradas.
O discriminador está reconhecendo as paradas — e `(230, 230)`, vibração quase
máxima, ficou pendurado até o teto de 3 s cortar.

### A pista, a um segundo de distância

```
21:52:05  uhid_rumble_preso_expirado  player=2
21:52:06  sensor_hub_reader_iniciado  identity=14:3a:9a:00:00:ab  tipo=motion
21:52:06  sensor_hub_reader_iniciado  identity=a0:fa:9c:00:00:f0  tipo=motion
21:52:15  uhid_rumble_preso_expirado  player=1 E player=2, no MESMO milissegundo
```

Os readers dos **dois** controles reiniciaram entre o primeiro e o segundo
travamento, e os dois jogadores travaram **juntos**. Um evento comum derrubou os
dois.

### A hipótese, e ela explica o que já funcionava

> **A cura de 02/08 trata o caso em que o jogo MANDA a parada. Este é o caso em
> que ele NÃO CHEGA a mandar** — porque o device sumiu debaixo dele: reconexão
> de Bluetooth, vpad recriado, jogador derrubado pelo `sync`.

`integrations/uhid_gamepad.py:1626-1633` mostra por que o silêncio é o único
sinal que sobra:

```python
if not body[_VALID_FLAG0_OFFSET] & _VIBRATION_FLAGS:
    # este report NÃO fala de vibração ... encaminhá-los mataria a vibração
    # em curso. Mas o silêncio precisa ser CRONOMETRADO
    return
```

Enquanto o jogo fala de outras coisas, o rumble pendurado é decidido pelo teto.
Se o jogo **para de falar**, nada acontece até os 3 s.

**Por que nunca apareceu no cabo:** o device não some. **Por que a cura de 02/08
não cobre:** ela é sobre o conteúdo do report, e aqui não há report.

A própria `BT-E-VPAD-01` previu isto ao manter o teto: *"A cura tira a causa
conhecida; a rede continua para as desconhecidas."* **Esta é uma das
desconhecidas, e agora tem nome.**

---

## Defeito 2 — um `restore_all` do Jogador 1 desnuda o hidraw dos QUATRO

**PROVADO no código.**

- **quem esconde, esconde por nó:** `daemon/subsystems/gamepad.py:213-215` (P1) e
  `daemon/subsystems/coop.py:634` → `_broker_hide_player` (`coop.py:872`);
- **quem restaura, restaura a LEASE INTEIRA:**
  `daemon/subsystems/gamepad.py:217` e `:279` chamam `client.restore_all`, e no
  servidor `broker/hidraw_broker.py:689-694`:
  ```python
  for canon in sorted(self.by_conn.get(conn_id, set())):
      response = self._cmd_restore(conn_id, canon)
  ```
  **todos** os nós daquela conexão — e o daemon inteiro usa **uma conexão só**
  (`integrations/hidraw_broker_client.py:67`).

**O agravante:** o re-hide seguinte é refém do P1 —
`daemon/subsystems/gamepad.py:656-657`:

```python
if not _vpad_vivo(daemon):
    return
```

**antes** do laço que percorre os jogadores de co-op (`:670-683`). Se o vpad do
P1 estiver morto, ninguém reesconde ninguém.

**O que ela veria:** *"de repente o jogo passa a ver oito controles"* — cada
jogador duplicado — e some sozinho ~30 s depois. Ou não some, se o Controle 1
estiver degradado.

**Por que já funcionava:** com um controle, `restore_all` é indistinguível de
`restore(node)`. O defeito nasce da pluralidade.

---

## Defeito 3 — a reaplicação do alto-falante depois da reconexão só alcança o P1

**PROVADO no código.** `daemon/connection.py:88-131` chama
`reapply_speaker_after_connect` sempre com `uniq=None`.

Com quatro controles reconectando por Bluetooth, **P2, P3 e P4 nunca recebem a
reaplicação** — voltam com o volume e a rota que o firmware tiver, não com o que
ela configurou.

É a mesma família do achado 5 da BT-SURDO-01: caminhos escritos quando "o
controle" era um só.

---

## As entregas

### E1 — o rumble é zerado na BORDA de destruição, não pelo relógio

Quatro pontos onde o device do jogo desaparece e o rumble tem de ser zerado
**explicitamente**, antes de o vpad morrer:

1. `_teardown_player` do co-op (`daemon/subsystems/coop.py:905`+);
2. a destruição do vpad do P1 (`daemon/subsystems/gamepad.py`, o caminho de
   `stop_gamepad_emulation`);
3. o `UHID_STOP` recebido do kernel (o vpad morto que o `sync` detecta,
   `coop.py:305-309`);
4. a queda do controle físico (`_close_handles`,
   `core/backend_pydualsense.py:1449`) — o motor está no **físico**, e é ele que
   fica vibrando.

**O teto de 3 s FICA**, e não é redundância — está escrito na
[BT-E-VPAD-01](2026-08-01-BT-E-VPAD-01-o-que-so-existe-no-cabo-e-os-seis-furos.md#o-que-foi-entregue--02082026)
por que: o log de 25/07 registrou 17 disparos em 90 minutos, com valores presos
que desenham um fade-out cujo último passo se perdeu. **A E1 tira mais uma
causa; a rede continua.**

**Aceite:** derrubar o Jogador 2 com o rumble ativo → o motor do controle dele
para **imediatamente**, não em 3 s. Medível sem hardware: espionar
`force_rumble_stop`/`_emit_rumble` no teardown.

**Por que é raiz e não contorno:** baixar o teto de 3 s seria contorno — trocaria
a duração do defeito pela chance de cortar vibração legítima. A borda de
destruição é o momento em que a informação existe: **nós sabemos que o device
morreu; o jogo não.**

### E2 — o hide/restore do broker passa a ser por NÓ

`restore_all` continua existindo para o que ele foi feito: o EOF da conexão, que
é a lease inteira morrendo. **O que muda é quem o chama.**

`daemon/subsystems/gamepad.py:217` e `:279` operam sobre o **P1** e devem
restaurar **o nó do P1**.

**Aceite:** parar a emulação do P1 **não** altera o estado de exposição dos nós
dos secundários. **A bancada:** o broker real sobre um `tmpfs` com quatro char
devices falsos, com o cliente único do daemon — os testes de hoje exercitam uma
lease com **um** nó.

**Armadilha nomeada:** o `restore_all` na saída é uma **assimetria intencional** —
*"o restore NÃO tem gate de modo: expor nunca é errado"*
(`daemon/subsystems/gamepad.py:181-185`), doutrina *"duplicado é melhor que zero
controles"*. **Não a desfaça.** O que se corrige é o **alcance** de duas
chamadas, não a política.

### E3 — o re-hide deixa de ser refém do vpad do P1

O `if not _vpad_vivo(daemon): return` de `gamepad.py:656-657` roda **antes** do
laço dos secundários. Ele precisa guardar **só** o hide do P1.

**Aceite:** com o vpad do P1 morto e os do co-op vivos, os nós dos secundários
continuam escondidos.

### E4 — a reaplicação de áudio alcança todos os conectados

`daemon/connection.py:88-131` passa a reaplicar por MAC, para cada controle que
reconectou — não só o primário.

**Aceite:** reconectar o Controle 3 por Bluetooth devolve a ele o volume e a
rota que ela configurou.

### E5 — a bancada da borda de descida

Junto com a bancada da
[COOP-QUE-NÃO-DESMONTA-01](2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md#e4--o-teste-que-morde-a-bancada-dos-quatro-controles-com-queda-programável)
(elas usam o mesmo enumerador com roteiro), as asserções desta sprint:

1. rumble ativo + jogador derrubado → `_emit_rumble(0,0)` **antes** do vpad
   morrer. *Arranque a E1 e veja reprovar*;
2. `stop_gamepad_emulation` do P1 → os nós dos secundários seguem escondidos;
3. vpad do P1 morto → o re-hide dos secundários **acontece**;
4. reconexão de P2 → a reaplicação de áudio foi chamada com o MAC de P2.

---

## Testes que vão reprovar

```
pytest tests/unit -k "rumble or broker or hide or coop or speaker or connect"
```

## O que NÃO fazer

- **Não baixar o teto de 3 s.** Ele é a rede para as causas ainda desconhecidas,
  e baixá-lo aumenta a chance de cortar vibração legítima — que é o defeito
  oposto, e pior;
- **Não desfazer o `restore_all` no EOF da conexão.** Ali ele está certo: a
  lease inteira morreu;
- **Não tirar o gate `_vpad_vivo` do hide do P1** — ele existe para o hide não
  acontecer sem vpad, que é a receita de zero controles;
- **Não tratar o defeito 1 como "o SDL não manda a parada".** Ele **manda**,
  5922 vezes na sessão. O caso desta sprint é aquele em que **não há mais
  ninguém para mandar**.

## O que fica ABERTO

- **a confirmação do defeito 1 em campo.** O experimento: com dois controles no
  BT e um jogo vibrando, **desligar** o Controle 2. Se o motor dele continuar
  vibrando por ~3 s, está provado. Ela sente sem terminal nenhum;
- **por que os readers reiniciaram às 21:52:06** — o log mostra o efeito, não a
  causa. Pode ser a queda que a `BT-QUE-NÃO-CAI-01` vai investigar.
