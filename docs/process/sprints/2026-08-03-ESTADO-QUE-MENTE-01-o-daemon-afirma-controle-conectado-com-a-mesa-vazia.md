# ESTADO-QUE-MENTE-01 — o daemon afirma "conectado" com a mesa vazia

- **Status:** PROPOSTA, escrita em 03/08/2026
- **Prioridade:** ALTA — a aba Status é o **painel da verdade** declarado desta
  casa, e ela mostra bateria de um controle que não existe
- **Faixa:** 2 — o produto mente sobre o próprio estado
- **Causa-raiz:** **MEDIDA** — a contradição está **dentro do mesmo payload**
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Sucede:** a [PAINEL-DA-VERDADE-01](2026-08-01-PAINEL-DA-VERDADE-01-a-aba-status-diz-o-que-chega-ao-jogo.md),
  que declarou o requisito e não cobriu este caminho

---

## O que foi medido

Em 03/08, **sem nenhum controle na máquina** — conferido por três vias
independentes: nenhum device Sony no USB, nenhum device HID de DualSense além do
vpad, e nenhum nó de LED além do vpad.

O journal registrou a saída:

```
17:44:03  controller_disconnected  reason=probe_offline
```

E o `daemon.state_full`, consultado depois disso:

```
connected  : True          <- o topo do payload
transport  : usb
battery_pct: 85
controllers: 1
   -> {'uniq': None, 'connected': False, 'transport': None, 'battery_pct': None}
```

**O topo diz "conectado, USB, 85% de bateria". A lista de controles, no mesmo
JSON, diz "desconectado".** E o `controller.list` concorda com a lista:

```json
{"controllers": [{"connected": false, "transport": null, "is_primary": false}]}
```

## Por que isso importa mais do que parece

1. **a aba Status lê o topo** — ela mostra um controle com 85% de bateria
   enquanto não há controle nenhum;
2. **o CLI também** — `hefesto-dualsense4unix status` imprimiu a mesma coisa;
3. **é estado obsoleto que nunca foi limpo**, não cache proposital: o
   `controller_disconnected` foi registrado e os campos do topo ficaram.

E o defeito **não precisa de hardware para reproduzir** — basta desconectar tudo
e consultar o daemon.

## O que já se sabe do mecanismo

O topo do `state_full` e a lista `controllers` têm **fontes diferentes**. A lista
vem de `describe_controllers` (getattrs baratos, sem I/O). O topo vem de campos
que o daemon atualiza no ciclo de conexão — e que a desconexão **não zera**.

**A investigação da causa exata é a primeira entrega**, e é barata: os dois
valores estão no mesmo handler (`daemon/ipc_handlers.py`, o `state_full`).

---

## As entregas

### E1 — o topo e a lista deixam de poder discordar

**A regra:** se `controllers` está vazia ou não tem nenhum conectado, o topo
**não pode** dizer `connected: True`.

O caminho honesto é o topo **derivar** da lista, em vez de ser mantido em
paralelo — dois campos que descrevem o mesmo fato e são atualizados por caminhos
diferentes vão divergir, é só questão de quando.

**Aceite:** com zero controles, `state_full` responde `connected: False`,
`transport: null`, `battery_pct: null`. Medível **sem hardware**.

**Teste que morde:** um backend falso que reporta zero controles conectados →
asserção de que o topo **não** afirma conexão. Arranque a derivação e reprova.

### E2 — a desconexão limpa o que afirmou

Mesmo com a E1, vale zerar explicitamente na borda de desconexão: o
`controller_disconnected` é o momento em que a informação existe.

**Aceite:** o journal registra `controller_disconnected` e o `state_full`
seguinte já não afirma bateria.

### E3 — a aba Status não inventa bateria

Enquanto E1/E2 não entram, a tela tem duas fontes e escolhe a errada. Depois
delas, o card precisa dizer *"nenhum controle"* em vez de mostrar o último
estado conhecido.

**Aceite (com o olho dela):** desconectar todos os controles → a aba Status diz
que não há controle, e não mostra 85%.

---

## Testes que vão reprovar

```
pytest tests/unit -k "state_full or status or controller_list"
```

## O que NÃO fazer

- **não "consertar" só a aba** — a mentira está no daemon, e a CLI a repete;
- **não zerar o `battery_pct` sem zerar o `connected`** — meia verdade num
  painel que se chama "da verdade" é pior que o erro inteiro.

## O que fica ABERTO

- **por quanto tempo o estado obsoleto sobrevive** — medido que sobrevive ao
  `controller_disconnected`; não medido se algum caminho o limpa depois.
