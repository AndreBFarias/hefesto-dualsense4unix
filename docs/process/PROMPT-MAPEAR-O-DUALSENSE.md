# O prompt para mapear o DualSense com os controles na mesa

Cole o bloco abaixo numa sessão nova, dentro deste repositório. Escrito em
11/08/2026, para uma sessão que começa do zero conseguir medir sem repetir o que
já foi medido — e sem cair nas armadilhas que já custaram caro.

---

```
Você vai MEDIR o DualSense com os controles na mesa dela, e escrever o que
medir no mapa de canais. Trabalhe como uma engenheira sênior que já conhece
esta casa.

O QUE ELA TEM NA MESA HOJE: quatro DualSense (dois já usados nas medições de
11/08, dois novos), mais um Nintendo Pro Controller e um 8BitDo SN30 Pro. Isso
importa: metade do que falta no mapa só se responde com DOIS OU MAIS controles
ligados ao mesmo tempo.

LEIA PRIMEIRO, NESTA ORDEM, E NÃO PULE:

1. docs/process/2026-08-11-ONDE-PARAMOS-o-estado-para-a-proxima-sessao.md
   O estado da última sessão: o que mudou, o que está aberto, o que é decisão
   dela, e as cinco armadilhas que já custaram caro. É o arquivo mais barato de
   ler e o que mais economiza.
2. docs/protocol/driver-hid-playstation.md
   O DualSense por dentro do driver, lido no fonte C do DKMS desta máquina.
   Structs com offset por transporte, os três valid_flag bit a bit, a tabela de
   player LEDs, a calibração 0x05, as taxas medidas. QUANDO A PERGUNTA É "o que
   o aparelho faz de verdade", esta página vence a canônica.
3. docs/data/mapa-controles.csv
   O mapa. 97 linhas do DualSense, 194 células de transporte, 156 respondidas.
   É onde o seu trabalho vai ser escrito.
4. docs/process/COMO-OLHAR-A-TELA.md — só se o trabalho tocar a interface.

O QUE FALTA MEDIR, e é a sua fila:

(a) AS NOVE LINHAS DE COMBINAÇÃO (familia = `combinacao`). Nasceram vazias de
    propósito porque exigem dois ou mais controles na mesa. É o ponto cego que
    motivou o mapa inteiro: um controle no CABO saturava o controlador USB e
    matava a saída do outro no RÁDIO — a feature funciona sozinha nos dois
    transportes e quebra quando os dois estão juntos. Cada linha diz na coluna
    `nota` que combinação ela descreve. COMECE POR AQUI: é o que só hoje
    responde.

(b) As demais linhas mudas dos dois lados: cinco de `plataforma`, duas de
    `luz`, uma de `entrada`, uma de `vibracao`.

(c) As 15 células que afirmam `aciona = sim` com `confianca = medido` e não têm
    `teste_que_morde`. Rode `python3 scripts/check_paridade_transporte.py` e
    elas saem nomeadas, com linha e transporte. Ou ganham a mordida, ou baixam
    a confiança para o que de fato são — as duas saídas são honestas.

O MÉTODO DESTA CASA, e cada regra nasceu de um defeito real:

- FONTE PRIMEIRO, OLHO DEPOIS. A ordem certa é: fonte do driver -> instrumento
  -> olho dela. Em 11/08, quatro tentativas de ler um padrão de LED por foto
  falharam, e o fonte respondeu em cinco minutos. O olho dela é ACEITE, não
  descoberta.
- ANTES DE PERGUNTAR "DE QUE LADO", PROVE QUE RESPONDE. O teste de controle
  (tudo apagado contra tudo aceso) vem primeiro. Sem ele, três rodadas foram
  perdidas medindo uma peça que talvez nem obedecesse.
- NÃO MEDIDO É RESPOSTA VÁLIDA; INVENTAR NÃO É. Célula vazia significa
  "ninguém respondeu", e isso é verdade. Nunca escreva `desconhecido` onde o
  certo é vazio, nem generalize de um controle para outro.
- FATO ERRADO SE SUBSTITUI; DECISÃO MEDIDA SE DATA. O teste que separa: se
  apagar isto faria alguém repetir trabalho ou pagar custo já pago? Se sim,
  data. Se não, sai. Na dúvida, guarde.
- TESTE TEM DE MORDER. Escreveu teste? Arranque a cura, veja reprovar, devolva.
  Um teste que passa com a cura arrancada não testa nada.
- VALOR DE DOMÍNIO NUNCA LEVA ACENTO. As colunas `existe`, `*_canal`,
  `*_confianca` e `*_grau` são enumerações (`nao-tem`, `inferido-do-codigo`). A
  PROSA leva acento; a chave, não. Uma acentuação em massa já fez o censo saltar
  de 15 para 368 reprovações. (Exceção medida: `*_aceita` e `*_aciona` usam
  `não` COM acento — é o que `scripts/check_paridade_transporte.py` aceita.)

AS ARMADILHAS DE MEDIÇÃO, todas pagas em dinheiro:

1. O INSTRUMENTO MENTE MAIS QUE O PRODUTO. Todo instrumento declara qual
   biblioteca e qual fonte usa. Medir o gamepad virtual contra a libSDL2 do
   sistema produziu um alarme falso inteiro; a SDL3 que a Steam distribui é
   outra régua.
2. O SYSFS DE LED É CACHE, NÃO RETRATO. Escrever nele não muda o aparelho, e
   `cat` devolve o que foi escrito. Medido com o daemon parado E confirmado no
   fonte (`brightness_get` devolve variável em RAM). Quem escreve de verdade é
   o report HID.
3. O DAEMON DISPUTA O HIDRAW. Para escrever report cru, PARE O DAEMON
   (`systemctl --user stop hefesto-dualsense4unix.service`) e religue depois.
   O gravador de capturas já recusa rodar com ele vivo.
4. MEDIÇÃO QUE DEPENDE DE ELA AGIR NUMA JANELA QUE ELA NÃO VÊ NÃO É MEDIÇÃO.
   Você não consegue abrir uma janela que ela enxergue em tempo real: a
   mensagem "aperte agora" só chega depois que o comando termina. Ou o
   instrumento roda em background por minutos e ela aperta quando quiser, ou —
   melhor — ela roda e vê na hora. `scripts/ver_botao.py` existe por isso.
5. EDITAR UM ARQUIVO MUITO CITADO DESLOCA AS CITAÇÕES DELE NO REPOSITÓRIO
   INTEIRO. O install.sh cresceu 119 linhas num dia e 128 citações ficaram
   erradas em 30 documentos. Se mexer num arquivo assim, realinhe por diff.

OS INSTRUMENTOS QUE JÁ EXISTEM, use antes de escrever outro:

  scripts/ver_botao.py                    ela roda, vê o botão na hora
  scripts/medir_steam_virtual_gamepad.sh  o ambiente da Steam, com jogo aberto
  scripts/record_hid_capture.py           gravador (recusa daemon vivo)
  scripts/check_paridade_transporte.py    o censo do mapa
  scripts/gerar-mapa.py                   CSV -> specs.html (rode no fim)
  scripts/doctor.sh                       diagnóstico da máquina

AGENTES: use para trabalho paralelo DENTRO do repositório — mapear onde algo
está, auditar, medir. Dê a cada um dono exclusivo de arquivos, senão eles se
atropelam. Diga o que NÃO fazer.

O QUE PERGUNTAR A ELA: decisão de produto (nome, comportamento, o que a tela
promete); duas leituras razoáveis que levem a trabalhos diferentes; e aceite no
hardware. Fora isso, decida e siga — ela delegou a caneta em 11/08: "vc no caso
tem o direito de escrever, vamos ir validando juntos ponto a ponto".

ANTES DE FECHAR A LEVA — nesta ordem, porque os portões são cegos a arquivo
novo:

    git add -A
    .venv/bin/python -m pytest -q          # 8890 verdes em 11/08
    .venv/bin/ruff check src/ tests/       # `ruff check .` NÃO é o mesmo
    python3 scripts/validar-acentuacao.py --all
    python3 scripts/validar-glifos.py --all
    python3 scripts/validar-referencias-docs.py --all
    bash scripts/check_anonymity.sh
    bash scripts/check_test_data.sh
    .venv/bin/python scripts/check_version_consistency.py
    bash scripts/check_packaging_parity.sh
    python3 scripts/gerar-mapa.py          # regenera o specs.html
    .venv/bin/mypy src/hefesto_dualsense4unix

COMMIT: mensagem em português, explicando o PORQUÊ e o que foi medido — não a
lista de arquivos. Se algo ficou em aberto, diga qual e por quê.

COMECE assim: leia os quatro arquivos, rode
`python3 scripts/check_paridade_transporte.py` para ver a dívida em número, diga
o que vai medir primeiro e por quê, e comece pelas linhas de combinação — que
são as que só hoje, com quatro controles na mesa, se pode responder.
```

---

## Por que este prompt é assim

**Ele começa pelo handoff, não pela canônica.** A ordem antiga mandava ler a
referência canônica primeiro; em 11/08 descobriu-se que ela estava errada em
pontos que o fonte C corrige. O handoff diz o que caducou.

**Ele nomeia as armadilhas de MEDIÇÃO, não só as de código.** Quatro das cinco
custaram rodadas inteiras da sessão de 11/08, e nenhuma é óbvia: a mais cara —
que o instrumento não pode depender de ela agir numa janela que não vê — levou
três tentativas para ser nomeada.

**Ele diz por onde começar, e o motivo é o hardware.** As nove linhas de
combinação são as únicas que exigem a mesa cheia. Se a sessão gastar o dia em
outra coisa e os controles saírem da mesa, elas ficam para o mês que vem.

**Ele lista os instrumentos que já existem.** Escrever um instrumento novo
quando já há um é a forma mais comum de perder tempo aqui — e o instrumento
novo costuma repetir o erro que o antigo já corrigiu.
