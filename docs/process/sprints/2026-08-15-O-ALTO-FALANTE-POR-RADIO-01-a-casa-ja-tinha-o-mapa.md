# O ALTO-FALANTE POR RÁDIO 01 — a casa já tinha o mapa, e ninguém ligou a saída

- **Escrito em:** 15/08/2026, madrugada, sobre `781dafc`
- **Grau:** **MEDIDO** no que afirma sobre o aparelho; **PLANO** no que propõe.
- **Nasceu de:** uma correção dela sobre método, e de um susto meu.

## O susto, e ele é a lição

Passei a madrugada medindo, com ela segurando o controle, que o firmware do
DualSense executa os reports `0x32` e `0x39` por Bluetooth. Escrevi um estudo.
Comemoramos.

Aí abri `src/hefesto_dualsense4unix/integrations/dualsense_bt_audio.py` e li,
escrito em **25/07/2026**, três semanas antes:

```python
#: Tags dos blocos TLV do corpo. Só usamos o de AudioControl; os demais estão
#: aqui para quem for ler o protocolo depois (0x10 SetState, 0x12 hápticos,
#: 0x13/0x16 alto-falante) e para o teste que trava os valores.
BLOCO_SET_STATE = 0x10
BLOCO_AUDIO_CONTROL = 0x11
BLOCO_HAPTICS = 0x12
BLOCO_SPEAKER = 0x13

#: bit7 do byte de tag = "este bloco está presente". (bit6 = "vêm DOIS
#: sub-blocos do tamanho declarado" — é assim que o 0x39 manda dois blocos de
#: 200 bytes de Opus para o alto-falante com `len` 200. Não usamos.)
BLOCO_PRESENTE = 0x80
BLOCO_DUPLO = 0x40
```

**"Não usamos."**

O caminho inteiro estava mapeado: o report, o envelope TLV, o tag do
alto-falante, o codec, o tamanho dos blocos. Eu redescobri com uma lightbar o
que estava escrito no nosso próprio código, e a frase *"para quem for ler o
protocolo depois"* era um bilhete para mim que eu levei três semanas para abrir.

É o defeito que o `CLAUDE.md` desta casa chama de mais caro: **a cura escrita e
nunca ligada.** Aqui ele aparece na forma mais pura — não é código morto, é um
mapa completo com um "não usamos" no fim.

## O que a medição de hoje ACRESCENTA ao que já estava escrito

Nem tudo foi redescoberta. O que é novo:

| medição | grau |
|---|---|
| o `0x39` de 547 B é aceito e **executa o `common`** (lightbar obedeceu) | MEDIDO |
| o canal BT transporta 552 bytes (`btmon`: `ACL Data TX dlen 552`) | MEDIDO |
| descritor cabo 289 B × rádio 320 B, com a escada só no rádio | MEDIDO |
| `os.write()` em hidraw **não valida** — aceita até tamanho errado | MEDIDO |

O módulo de 25/07 provou o `0x32` (mic). **Hoje provou-se que o firmware
executa o `common` de 47 bytes dentro do `0x39`** — e nada além disso.
**Corrigido em 15/08/2026:** esta frase terminava em *"o `0x39`, que é justamente
o report do alto-falante"*, e a segunda metade é a **FALÁCIA DO CANAL QUE
RESPONDE** — que o `0x39` seja o report do alto-falante é o que o comentário do
nosso módulo diz e o que o E2 existe para medir; a lightbar acendendo não prova
isso. O que ninguém tinha exercitado, esse sim, é fato.

## O que falta, e é curto

O `BLOCO_SPEAKER = 0x13` está declarado e **não é referenciado por nenhum
caminho de escrita** — `grep` fora do próprio módulo devolve só um tooltip da
interface (`controller_card.py:714`, `DICA_BLOCO_SPEAKER`). A casa já explica o
protocolo ao usuário numa dica de tela, e não o implementa.

### E1 — montar o `0x39` com o bloco do alto-falante
O envelope, o CRC e o contador de sequência **já existem** em
`core/ds_output_report.py` e no próprio `dualsense_bt_audio.py`. O que falta é a
montagem do bloco `0x13` com `BLOCO_DUPLO` e dois sub-blocos de 200 bytes.

**Mordida:** o teste que existe hoje trava os valores das constantes; o novo tem
de exercitar a MONTAGEM — report de 547 B, tag `0x13|0x80|0x40`, `len` 200, CRC
semente `0xA2` conferido byte a byte.

### E2 — o ensaio com a orelha dela
Um tom senoidal curto, codificado em Opus (mono, 48 kHz, quadros de 10 ms — os
mesmos parâmetros que o mic **já usa na direção inversa**, e que estão medidos no
módulo), mandado pelo `0x39`.

**Controle positivo:** o mesmo tom pelo alto-falante do controle **no cabo**, que
funciona hoje pela placa USB. Se ela ouvir no cabo e não no rádio, o silêncio é
informação. **Controle negativo:** o mesmo report com o tag trocado (`0x12`,
hápticos) — se sair som, o tag não é o que pensamos.

**Quem observa:** ela. É a mesma régua da rota de saída, medida com a orelha dela
em 02/08 e registrada no mapa.

### E3 — o `0x16`, o irmão não explicado
O comentário cita `0x13/0x16` como sendo os dois do alto-falante, sem dizer o que
os separa. Hipóteses a testar: taxa diferente, canal diferente, ou um deles é
para os motores voice-coil. **Não afirme nada sobre ele antes do E2.**

## As armadilhas desta sprint

1. **O `os.write()` mente.** Ele devolve sucesso quando o KERNEL aceita, sem
   esperar veredito do firmware — aceitou até um pacote de tamanho errado. Todo
   ensaio desta família nasce com controle positivo E negativo, e a prova de que
   o firmware processou é **efeito observável**, nunca o retorno da chamada.
2. **A disputa do contador de sequência** já está analisada no módulo, e a
   conclusão é que escrever `0x39` é seguro pelo mesmo motivo que escrever
   `0x32`: são report IDs diferentes do `0x31` que o kernel governa. Mas o
   `0x39` é **muito maior**, e o efeito de banda (medido para o mic: ligar custa
   ~35% dos reports de input) precisa ser remedido para a saída.
3. **O daemon disputa o hidraw.** O ensaio do mic de 25/07 foi feito com o daemon
   parado. **Para o ensaio da lightbar de hoje as duas páginas desta casa se
   contradizem** — esta linha dizia *"com ele rodando"* e a
   [canônica](../../protocol/dualsense-referencia-canonica.md), na seção da
   escada, declara *"com o **daemon parado** e a autorização dela"*. As duas não
   podem estar certas, e a canônica é a página de registro: **vale "daemon
   parado"** até que alguém mostre o contrário. É por isso que a regra desta
   linha existe: **declare qual, sempre** — e declare no mesmo documento em que
   se publica o resultado.
4. **Não confundir "o canal responde" com "o canal faz o que eu quero".** O
   `0x39` executa o `common` — isso está provado. Que ele toque som é o que o E2
   existe para descobrir.

## O que esta sprint NÃO promete

Não promete áudio por Bluetooth funcionando. Promete **exercitar o caminho que a
casa já mapeou e nunca percorreu**, com o ensaio que decide se ele leva onde
achamos que leva.

## Uma pergunta de processo, e ela é dela

O módulo de 25/07 deixou o mapa e seguiu. Não houve sprint, não houve item em
índice, não houve dívida registrada — só um comentário gentil para o próximo
leitor. **Quantos outros bilhetes desses existem nesta árvore?**

Sugestão: um portão que reprove constante pública declarada e nunca referenciada
fora do próprio módulo. Teria pego o `BLOCO_SPEAKER` em 25/07, e teria nos
poupado uma madrugada de redescoberta — que valeu pelo que mediu de novo, mas
podia ter começado três semanas à frente.
