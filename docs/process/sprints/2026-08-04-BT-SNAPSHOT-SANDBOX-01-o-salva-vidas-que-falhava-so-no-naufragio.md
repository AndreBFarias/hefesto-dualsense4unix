# BT-SNAPSHOT-SANDBOX-01 — o salva-vidas que falhava só no naufrágio

- **Medido em:** 03→04/08/2026, no journal dela
- **Estado:** **CURADO em 04/08/2026.** Registro de causa-raiz
- **Gravidade:** alta — o mecanismo falhava **exatamente** na ocasião para a
  qual foi construído
- **Pré-requisito:** nenhum

---

## O defeito, em uma linha

O snapshot de bonds do Bluetooth roda como `ExecStopPost=` do
`bluetooth.service` — ou seja, **no momento em que o BlueZ morre**, que é
precisamente quando os pareamentos correm risco. E era exatamente aí que ele
falhava.

```
23:58:07  bluetooth.service: Main process exited, code=dumped, status=6/ABRT
23:58:07  bt_bonds_snapshot.sh: linha 105:
          /var/lib/hefesto-dualsense4unix/bt-bonds/.lock:
          Sistema de arquivos somente para leitura
```

---

## A causa-raiz

O `ExecStopPost=` **herda o sandbox da unit**. O `bluetooth.service` do BlueZ
declara `ProtectSystem=strict`, que torna `/usr`, `/boot` e **`/var` inteiro**
somente-leitura para tudo o que roda dentro da unit — inclusive os nossos
`ExecStopPost`.

O nosso drop-in acrescentava comportamento à unit sem acrescentar a **permissão
de escrita** que esse comportamento exige. O script está correto; o ambiente em
que ele roda é que não permitia o que ele precisa fazer.

**A perversidade do defeito** é que ele é invisível em operação normal: o
`ExecStopPost` só corre quando o serviço para, e um `systemctl restart` manual
tem o mesmo sintoma — que ninguém olha. Ele só aparece no journal de um crash,
misturado ao ruído do próprio crash.

---

## A cura aplicada

`assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf`:

```
ReadWritePaths=/var/lib/hefesto-dualsense4unix
```

Uma linha, e o mínimo possível: abre-se **só o nosso diretório**, não `/var`.
O `ProtectSystem=strict` do BlueZ continua valendo para todo o resto — a cura
não enfraquece o sandbox de quem não é nosso.

Conferir em vigor:

```bash
systemctl show bluetooth.service -p ReadWritePaths
```

---

## O que isto ensina, e é a parte que vale guardar

**Todo `ExecStartPre`/`ExecStopPost` que a casa acrescenta a uma unit de
TERCEIRO herda o sandbox daquele terceiro** — e o terceiro pode apertá-lo numa
atualização, sem aviso, quebrando o nosso comportamento em silêncio.

**O que a sprint seguinte deve varrer:** todo drop-in nosso em unit alheia,
cruzado com o que o script dentro dele escreve. O comando de partida:

```bash
grep -rln 'ExecStartPre\|ExecStopPost\|ExecStopPre' assets/systemd/
```

Para cada um, a pergunta: *o script escreve em algum lugar? A unit hospedeira
permite?* — e a resposta tem de estar **no arquivo**, não na cabeça de quem
escreveu.

---

## O que morde

Um teste que leia o drop-in e exija `ReadWritePaths` cobrindo **todo caminho
que os `ExecStopPost` dele escrevem**. Arrancar a linha faz reprovar. Sem esse
teste, a próxima pessoa que acrescentar um `ExecStopPost` que escreve noutro
lugar reabre isto — e só descobre no próximo naufrágio.

---

## Relacionado

- [BT-AGENT-TRAVA-O-RESTART-01](2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md) — o outro defeito medido no MESMO crash
- [DOC-QUE-NAO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md)
