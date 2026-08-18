# A escada que responde — o áudio por rádio deixou de ser "impossível"

- **Medido em:** 15/08/2026, madrugada, na máquina dela, com quatro DualSense
- **Quem mediu:** ela com o controle na mão, eu com o `hidraw` e o `btmon`
- **Grau:** **MEDIDO NO APARELHO.** A parte que é hipótese está marcada como tal.
- **Nasceu de:** uma correção dela, de manhã: *"se no PlayStation via BT tudo
  isso funciona é pq tem um meio físico pra isso funcionar e ainda não
  descobrimos. só falta mapear cientificamente pra tirarmos os achismos"*

## O que o mapa dizia, e o que caiu

A célula `audio.saida_dedicada`, lado rádio, dizia:

> IMPOSSÍVEL por A2DP/HFP: zero cards. A ponte por HID é o ÚNICO caminho
> concebível, e a metade de saída não tem código.

A palavra "impossível" caiu duas vezes no mesmo dia. De manhã pelo argumento
dela — o PS5 faz, logo existe caminho. De madrugada pelo aparelho.

## A mesa que permitiu medir

Decisão dela: **dois controles no cabo e dois no rádio, ao mesmo tempo**.
O motivo é metodológico e é o que dá valor a tudo abaixo — o mesmo instrumento,
no mesmo minuto, na mesma máquina. Toda diferença observada é do TRANSPORTE.

| controle | MAC | transporte | `hardware_version` |
|---|---|---|---|
| VERMELHO | `44:46:48:00:00:03` | rádio | `0x0811` BDM-050 |
| BRANCO | `14:3a:9a:00:00:ab` | rádio | `0x0711` BDM-050 |
| ROXO | `a0:fa:9c:00:00:f0` | **cabo** | `0x0710` BDM-050 |
| AZUL | `d4:2f:4b:00:00:d8` | **cabo** | `0x1111` BDM-060M |

O mapeamento MAC↔cor foi **medido**, não inferido: ela desligou um controle de
cada vez e eu vi qual `hidraw` sumiu.

## 1. A primeira assimetria apareceu sozinha

Com a mesa montada, `/proc/asound/cards` mostrou **duas** placas USB Audio —
exatamente os dois do cabo. Os dois do rádio não expõem placa nenhuma.

Isso confirma no aparelho o que o mapa afirmava por leitura de código.

## 2. Os descritores HID divergem, e a divergência tem forma

`/sys/class/hidraw/hidrawN/device/report_descriptor`, lido dos quatro:
**cabo 289 bytes, rádio 320 bytes.**

| id | CABO | RÁDIO |
|---|---|---|
| `0x02` | OUTPUT 47 B | — |
| `0x31` | — | OUTPUT 77 B + INPUT 77 B |
| `0x32` | — | OUTPUT 141 B |
| `0x33` | — | OUTPUT 205 B |
| `0x34` | — | OUTPUT 269 B |
| `0x35` | — | OUTPUT 333 B |
| `0x36` | — | OUTPUT 397 B |
| `0x37` | — | OUTPUT 461 B |
| `0x38` | — | OUTPUT 525 B |
| `0x39` | — | OUTPUT 546 B |
| `0xF6` | — | FEATURE 546 B |

**O cabo tem UM output. O rádio tem NOVE, em escada de +64 bytes.**

## 3. O canal transporta 552 bytes — visto no rádio

`btmon` durante as escritas:

```
< ACL Data TX  Handle 3  dlen 83     (0x31 de 78 B + header)
< ACL Data TX  Handle 3  dlen 147    (0x32 de 142 B)
< ACL Data TX  Handle 3  dlen 105    (0x32 de 100 B, tamanho errado)
< ACL Data TX  Handle 3  dlen 552    (0x39 de 547 B)
```

## 4. O ACHADO: o firmware EXECUTA os degraus

O teste que decide. Mesmo `common` de 47 bytes pedindo cor de lightbar
(`valid_flag1 = 0x04`, RGB em `[44..46]`), com envelope BT completo
(`[1]=seq<<4`, `[2]=0x10`, CRC-32 semente `0xA2` nos quatro últimos), mandado
por **report IDs diferentes**. Ela olhando a lightbar do BRANCO:

| passo | report | pedido | **o que ela viu** |
|---|---|---|---|
| 1 | `0x31` 78 B | vermelho | **vermelho** — controle positivo |
| 2 | `0x31` 78 B | apagar | apagou |
| 3 | **`0x32` 142 B** | verde | **VERDE** |
| 4 | `0x31` 78 B | apagar | apagou |
| 5 | **`0x39` 547 B** | azul | **AZUL** |
| 6 | `0x31` 78 B | apagar | apagou |

**O firmware aceita e executa `0x32` e `0x39` por Bluetooth**, processando neles
o mesmo `common` do `0x31`. Os degraus da escada não são declaração vazia no
descritor: são reports vivos.

## 5. O que isto prova, e o que NÃO prova

**PROVA:** o firmware lê e executa reports de output de 142 e 547 bytes por
rádio; o canal Bluetooth os transporta; e o `common` de 47 bytes vale igual em
todos.

**NÃO PROVA:** que os bytes além do `common` são áudio. Isso continua hipótese —
forte, porque o controle já está inteiramente servido pelos 47 bytes e não há
outra função de controle conhecida para 469 bytes adicionais, e porque o PS5
manda som para este mesmo aparelho. Mas hipótese.

**O próximo ensaio que a decide:** mandar o mesmo degrau com conteúdo variado
nos bytes extras e observar se a cor ainda obedece. Se obedecer sempre, o
excedente é ignorado naquela posição; se alguma variação quebrar a obediência,
o excedente tem estrutura — e é onde o formato mora.

## 6. Um instrumento que mentiu, e o controle negativo que o pegou

A primeira tentativa usou `os.write()` num `hidraw` e concluiu "aceitou" para os
quatro pacotes — **inclusive para o controle negativo de tamanho errado**, que
tinha de ser recusado.

O `os.write()` devolve sucesso quando o KERNEL aceita a entrega; ele não espera
veredito do firmware. Sem o controle negativo, o relatório teria dito que o
degrau estava provado, com uma medição que não aferia coisa nenhuma.

É a regra da casa se pagando: *"o instrumento mente mais que o produto"*.
**Todo ensaio desta família nasce com controle positivo E negativo.**

## 7. Medições de bancada que saíram de brinde

- **Por rádio, `GET_FEATURE` exige retry.** Cabo: 10 de 16 reports em 7,1 s, sem
  retry nenhum. Rádio: 13 de 16 em 18,5 s, com retry em 13 deles. Cada falha
  custa ~3 s (o `REPORT_REQ_TIMEOUT` do BlueZ).
- **O rádio responde MAIS reports que o cabo** — 13 contra 10. Os seis que o cabo
  recusa (`0x08`, `0x80`, `0x82`, `0xF0`, `0xF4`, `0xF7`) o rádio entrega.
  Inverte a expectativa de que o cabo é o caminho completo.
- **`hardware_version` distingue os quatro** sem root, em sysfs. Não é cor: é
  revisão de placa, e dois controles da mesma cor teriam o mesmo valor.

## 8. Onde isto entra

O `0xF6` — FEATURE de 546 bytes, **só no rádio** — é o próximo suspeito, e a
hipótese é que seja negociação: dizer ao controle qual codec e qual taxa vêm a
seguir. O mapa já registra que o **microfone** por rádio atravessa hoje em Opus
no input `0x31`; se a entrada é Opus, a saída provavelmente também.

E fica registrado o que esta casa aprendeu duas vezes hoje: **ausência de achado
não é prova de impossibilidade.** A forma do erro tem nome — *falácia do perfil
ausente* — e ela custou a este projeto uma célula que dizia "impossível" sobre
um canal que responde.
