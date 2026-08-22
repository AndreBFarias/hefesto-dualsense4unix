# CONFIG-02 — o que a mesa já sabe dizer

Seções 1 e 2 em **somente leitura**. Nenhum campo declarado ainda; só o que a
máquina responde sozinha.

**Depende de:** CONFIG-01.

## O que entrega

- Lista de adaptadores Bluetooth com endereço, chipset e estado do firmware.
- Lista dos outros rádios de 2,4 GHz encontrados no barramento USB.
- Aviso quando dois rádios estão no mesmo controlador USB, em portas vizinhas.

## A decisão de fonte

Três caminhos, e o dossiê elimina dois:

| Fonte | Veredito |
|---|---|
| `bluetoothctl list` | **Não serve.** Está mudo nesta máquina desde o BlueZ 5.86 one-shot |
| Chamar `scripts/doctor.sh` | **Não serve como está.** Ele tem `hci0` fixo em três pontos (`:2555`, `:2563`, `:2823`) e mente numa mesa de dois ou três dongles. Além disso os testes fazem *grep de texto* na saída dele, então mudá-lo é caro |
| Ler `sysfs` direto da GUI | **É o caminho.** `/sys/class/bluetooth/*`, `/sys/bus/usb/devices/*` — sem root, sem subprocess, sem IPC novo |

**Detectar hub é viável e preferível a perguntar:** `bDeviceClass == 09` no
sysfs, com `maxchild` e `bMaxPower`. Onde a leitura acerta, ela pré-preenche —
é a salvaguarda 2 de [D-A1](DECISOES-ABERTAS.md).

## O que NÃO entra

- **RSSI / força de sinal.** Via D-Bus ele só existe durante *discovery*, e
  manter discovery ligado rouba banda do rádio dos controles. Medir pioraria
  exatamente o que a aba quer melhorar.
- **Qual controle está em qual dongle.** O que amarra controle a adaptador é o
  bond, em `/var/lib/bluetooth` — árvore `700`, e a GUI é **sudo-zero por
  doutrina**. A informação mais importante da topologia é justamente a que a aba
  não alcança sozinha. Fica registrada como limite, não como tarefa.

## Prova de trabalho

```bash
pytest tests/unit/ -k config -q
GDK_PIXBUF_MODULE_FILE=/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache \
  scripts/gui-captura/retratar_abas.py /tmp/config02 --mesa-cheia
```

**Aceite:** numa máquina com um adaptador, a seção lista um. Numa com dois,
lista dois — e nomeia cada um pelo endereço, nunca por `hciN`, que inverte entre
boots. A leitura não pode rodar no tique rápido: ela acontece ao abrir a aba e
no botão "Reexaminar a mesa".
