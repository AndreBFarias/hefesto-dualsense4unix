# ONDE PARAMOS — o estado para a próxima sessão

- **Escrito em:** 11/08/2026, no fim de uma sessão longa, a pedido dela: *"de
  forma que se eu der um barra clear o próximo Claude vá saber o que fazer"*.
- **Reescrito em 12/08/2026**, no fim da bancada de 11→12/08. O que estava aqui
  descrevia uma sessão de **documentação**; depois dela veio uma sessão de
  **bancada**, com o controle na mão dela, e três coisas mudaram de lugar. O
  nome do arquivo continua o mesmo de propósito: o `CLAUDE.md` da raiz aponta
  para ele, e renomear quebraria o primeiro link que uma sessão nova segue.
- **Para quem chega agora:** leia o `CLAUDE.md` da raiz primeiro (ele diz a
  ordem), depois este arquivo. Ele responde três coisas: **o que mudou**, **o
  que está aberto**, e **o que é dela**.
- **Grau:** os números são MEDIDOS na árvore de 12/08. O que depende de medição
  que não existe está dito com todas as letras.

---

## 1. O que mudou nesta bancada, em uma tela

**Foi uma sessão de MEDIR NO APARELHO.** A sessão anterior reconciliou papel com
código; esta pôs quatro DualSense na mesa — dois no cabo, dois no rádio — e
percorreu o checklist do
[`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md) item por item. Três
features fecharam, **cada uma com dono diferente de defeito**, e um suspeito
novo contaminou dezesseis dias de investigação passada.

**A página inteira da bancada, com a prova de cada linha, é a sprint
[CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md).**
Não a duplique: o que está abaixo é o resumo para decidir por onde continuar.

| o que fechou | a prova, em uma linha |
|---|---|
| **O rumble que o jogo manda ao controle físico** | o keepalive do daemon zerava os motores; a constante de 0,5 s para 8,0 s fez a vibração durar **oito segundos exatos** |
| **A escada da intensidade de vibração** | decisão dela: **Economia 0,3× · Balanceado 1,0× · Máximo 1,5×**, com o deslizador livre até 200 |
| **A lightbar por Bluetooth, depois de dezesseis dias** | a Steam mantém o `hidraw` de cada DualSense aberto em **leitura+escrita** e repinta a barra a cada conexão nova: **98** reports de saída no fio contra **6** sem ela |

**Números na árvore de 12/08:** **8949** testes coletados (é contagem de
coleta, **não** de verdes — a leva desta bancada ainda está aberta), **293**
linhas no mapa de canais, **53** ensaios no caderno, **52** deles com
`observado_por = olho-dela`.

> **A ÁRVORE NÃO ESTÁ COMMITADA, e isto é a primeira coisa a fazer.** Em 12/08
> o `git status` tem **61** caminhos mexidos — `src/`, `tests/`,
> `docs/data/*.csv`, `specs.html`, scripts de ensaio novos e a própria sprint.
> A regra da casa é que **a árvore de trabalho é o que roda**, e esta casa já
> perdeu uma leva inteira por ficar horas no índice sem commit. Rode
> `git status` antes de qualquer coisa e decida o que fecha.

### 1.1 O rumble — causa isolada, e com número

**GRAU: MEDIDO**, `docs/data/ensaios.csv:16-24`, com o olho dela.

O jogo que fala com o **DualSense físico** — sem controle virtual e fora da
Conexão Nativa — manda a vibração por força-feedback no `evdev`. O **keepalive**
do daemon reescrevia `common[2]`/`common[3]` zerados a cada 0,5 s e apagava o
motor. Com o daemon vivo, 40 s de vibração deram **nada** no cabo e **um único
tranco** no rádio; com ele parado, contínuo nos dois.

**A dose-resposta é o que transforma indício em causa:** com a constante em
8,0 s a vibração passou a durar **oito segundos exatos**, nos dois transportes.
A constante foi revertida no mesmo ensaio.

**E a segunda metade derrubou a premissa de uma cura inteira.** O que estava
escrito apostava que **desligar os bits de autorização** bastava para o firmware
conservar o motor de outro dono. Um único report com os bits **desligados**
pedindo `common[2]=200` e `common[3]=0` fez o tremor **trocar de lado** na mão
dela — *"esquerda e senti que foi pra direita e lá morreu"*. **O firmware honra
os BYTES.** Isso é fato de protocolo e está na canônica
([§2, *Os BITS de vibração não são porteiro dos BYTES de motor*](../protocol/dualsense-referencia-canonica.md)).

A cura que ficou: **o keepalive deixou de ser perpétuo** e passou a valer só na
janela de confirmação depois de cada mudança real. O único write não-destrutivo
é o write que **não acontece**.

### 1.2 A política de vibração — decisão dela, com o preço na mesa

**GRAU: DECISÃO DELA**, 11/08, depois de o preço de cada opção ir para a mesa.

- **Economia 0,3× · Balanceado 1,0× · Máximo 1,5×.** O Balanceado era 0,7 e o
  tooltip prometia *"do jeito que o jogo pediu"* — duas afirmações e uma
  mentira. O Máximo era 1,0, ou seja, não aumentava nada.
- **O 2,0 foi considerado e descartado por ela:** a 2,0 metade da faixa satura
  em 255 e a variação da vibração some. A 1,5 satura de 170 para cima — um
  terço, e é o preço aceito.
- **O deslizador vai a 200 e isso não é incoerência:** os quatro botões são
  **presets seguros**; o deslizador é o ajuste livre de quem aceita o preço.
- **O produto passou a avisar** quando não há gamepad virtual **nem** Modo
  Nativo — o estado em que o multiplicador **não age**. O aviso mora em cima
  dos quatro botões da aba Rumble.

Onde isso já está escrito para quem usa:
[`interface.md`](../usage/interface.md) e [`modos.md`](../usage/modos.md).

### 1.3 A lightbar por Bluetooth — o suspeito que ninguém olhou em dezesseis dias

**GRAU: MEDIDO** quanto ao fato; **o suspeito ainda NÃO está fechado**, e o
caderno está certo em recusar.

Com o daemon parado, `readlink` sobre `/proc/*/fd` mostrou o processo `steam`
com `/dev/hidraw4..7` abertos e o `fdinfo` confirmou **leitura+escrita**. No fio,
por `btmon`: **98** pacotes de saída durante a probe com a Steam viva (as três
barras nasceram apagadas) contra **6** sem ninguém no `hidraw` (as três nasceram
acesas, e as três obedeceram a verde puro).

Três coisas que a bancada mediu e que mudam o desenho de qualquer cura:

1. **A rajada tem hora.** Duas rajadas, `t+0`–`t+3 s` e `t+15`–`t+18 s`, com
   silêncio entre elas. A Steam bombardeia na **probe** e depois cala.
2. **A rajada é por EVENTO, não por controle.** Cada conexão nova faz a Steam
   repintar **todos**. Um protótipo que escrevia 1,5 s depois de cada conexão
   perdeu dois dos três.
3. **A rota decide.** Com a Steam aberta, `sysfs` não muda a barra; o report
   `0x31` cru no `hidraw` pintou os três. E o Hefesto **suprime** a rota
   `hidraw` por Bluetooth de forma incondicional — hoje o rádio tem uma rota só,
   e é a que perde.

**O desenho da cura, com aceite dela na bancada** (*"perfeito"*): um gatilho que
**arma a cada conexão e só dispara quando a sequência sossega**, escrevendo
então em **todos** os controles pela rota `hidraw`. **Não está no produto.**

A medição inteira, com os números e o limite de cada um, está em
[a pilha do Steam Input](../protocol/pilha-steam-input-xpad-sdl.md), seção
6-bis.

### 1.4 O preço deste achado: ele contamina o passado

Dezesseis dias perseguiram, um a um, o `0x08`, o keepalive, a adoção por
Bluetooth, o cache do sysfs, a instância de conexão e a revisão de hardware — **e
a Steam esteve com a caneta na mão o tempo inteiro, inclusive durante as
medições que concluíram cada uma daquelas hipóteses**.

Isso **não** torna aquelas leituras erradas. Torna-as **incapazes de isolar
qualquer coisa**, porque a variável que hoje se sabe decisiva estava livre em
todas. Quem for reabrir qualquer conclusão de lightbar anterior a 12/08 pergunta
primeiro: *quem estava com o `hidraw` aberto naquele instante?*

---

## 2. O que está EM ABERTO — e é aqui que a próxima sessão começa

### 2.1 O que a bancada deixou aberto

Sete itens, e cada um declara o próprio grau. A lista comentada está na seção 7
da [CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md).

| # | o que falta | por que importa |
|---|---|---|
| 1 | **A VOLTA do ensaio da lightbar** — subir os controles com a Steam viva na probe, de propósito, e ver o defeito voltar | só a volta distingue causa de coincidência. A ida está feita; a volta parou quando dois controles caíram do rádio |
| 2 | **O elemento específico do gatilho** não está isolado | funciona, e ninguém sabe de qual bit ou byte depende. É onde o rumble estava na manhã de 11/08 |
| 3 | **Sete dos oito modos de gatilho** nunca foram tocados | só `Rigid` foi exercitado, com **um** jogo de parâmetros |
| 4 | **Algo apaga o efeito de gatilho com período de MINUTOS** | medido o fenômeno (aos 120 s a leitura se inverteu), **sem suspeito nomeado**. Candidatos a ler no código: o tick do daemon e o `reassert_resolved_outputs` |
| 5 | **O cancelamento é total com dois alvos e parcial com quatro** | medido e **não explicado**. Registrado assim de propósito |
| 6 | **A mordida da cura do rumble** — `mordida_provada_em` está **vazio** no mapa | ninguém arrancou a cura do arquivo de produção e viu reprovar. É o que impede tudo isto de voltar na próxima mexida. Vale igual para `luz.lightbar.cor` |
| 7 | **A poda não foi feita** | é a metade que dá lucro: o que foi inocentado pode **parar de ser acionado**, e nada saiu do produto nesta sessão |

**Se for escolher uma:** a **1** e a **6**. A primeira fecha o suspeito mais caro
da casa; a segunda é a única que impede a regressão de voltar.

### 2.2 As sprints de correção, da família A

Fonte: `sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md`, seção
5. Elas existiam porque sete documentos novos contradiziam páginas antigas.

**A regra que governa todas** (fixada por ela, e já no `CLAUDE.md`): **fato
errado se substitui; decisão medida se data.** O teste que separa os dois: *se
apagar isto faria alguém repetir trabalho ou pagar custo já pago?*

**Onze das doze fecharam** nos commits de 11/08 — A-0 e A-9 em `91cfd39`, A-1,
A-2, A-4, A-6 e A-7 em `b9b7dee`, A-3 e A-8 em `788564c`, A-10 (128 citações
realinhadas) e A-11 em `a0e71a8`.

**A-5 continua ABERTA, e tem uma armadilha medida.** O nome errado
(`DirectInput/PS4`) aparece em 17 arquivos, mas em **dois sentidos diferentes**:
o modo do 8BitDo que se disfarça de DualShock 4 (`054c:05c4` — que no vocabulário
da 8BitDo é o modo **macOS**), e referências ao **DualShock 4 de verdade** —
`assets/dkms/hid-playstation/patch/0002-*.patch` é sobre o DS4 real, e o
cabeçalho dele vai para o upstream. **Substituição cega quebra o segundo.**
Quem for executar: separe os dois sentidos antes de trocar qualquer palavra, e
lembre que o D-input verdadeiro do 8BitDo é `B + Start`, `2dc8:6001` (medido em
11/08).

### 2.3 O caminho até a versão final

Fonte: `2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md`.

**Nove dias e meio de bancada, ou dois e meio no caminho mínimo.** A ordem é por
dependência, não por importância, e a ETAPA 1 é pré-requisito de tudo: enquanto
o `doctor` sair verde com curas ausentes, nenhum critério de aceite significa
alguma coisa.

**Versão recomendada: `0.9.4`, não `1.0.0`** — pela doutrina da própria casa,
`ENTREGUE EM CÓDIGO` não é `VALIDADO POR ELA`. O `1.0.0` é o número que se põe
**depois** de o PC novo passar.

### 2.4 O que só o aparelho responde

- **A captura de Bluetooth** (`tests/fixtures/hid_capture_bt.bin`) continua
  devendo desde 31/07. O gravador está consertado e provado
  (`scripts/record_hid_capture.py`); o modo guiado precisa das mãos dela.
- **Os três módulos DKMS nunca foram construídos contra outro kernel** que não o
  `7.0.11-76070011-generic`. É o furo com maior chance de decidir a instalação
  numa máquina nova.
- **Ninguém rodou o produto com Secure Boot ligado.** Com a chave MOK não
  enrolada, o kernel recusa o `.ko` e **não volta ao in-tree** — a máquina fica
  pior do que sem a cura.
- **Os `.deb` do backport do BlueZ não existem.** A receita vive na árvore
  (`estudos/2026-07-19-*`), mas gerar os pacotes continua sendo trabalho. É o
  único `FAIL` que um PC novo levaria no caminho `native`.
- **Três perguntas novas de protocolo** entraram na canônica em 12/08, e nenhuma
  se responde lendo arquivo: de quantos bits o firmware precisa para vibrar; se
  os bits são porteiro dos blocos de **LED** e **áudio**; e quem reaplica o
  gatilho com período de minutos.

---

## 3. O que é DELA, e não se decide sem ela

**Decisões novas, de 11 e 12/08, e as três primeiras já estão no código ou na
configuração da máquina dela:**

- **A escada da vibração: 0,3× / 1,0× / 1,5×**, com o 2,0 considerado e
  descartado por ela, e o deslizador livre até 200. Ver 1.2.
- **Nada de MAC, nada de personalização por controle** — literal, 12/08:
  *"nada de macs, nada de personalização por controle; se eu conectar controle
  virgem ele tem que funcionar via produto"*. Foi **aplicado à configuração
  dela** (o `order` do `controllers.json` de 9 MACs para 0, e o bloco
  `controllers` de quatro perfis), com backup em
  `~/.config/hefesto-dualsense4unix/backup-limpeza-20260811-233704`. **O que
  isso implica para o CÓDIGO — o override por peça, `PERFIL-01` e
  `POR-UNIDADE-01` — não foi decidido, e é dela.** De brinde, a limpeza mediu
  uma coisa boa: o produto numerou os três controles sozinho, **sem nenhum MAC
  conhecido**.
- **Quem manda na barra, por modo** — literal, 12/08: *"no modo nativo
  devolvemos o controle pra steam e no modo conexão também, todo o resto é o
  hefesto"*. É a cerca do gatilho da cor, e é a mesma do
  `FEAT-NATIVE-OUTPUT-MUTE-01` aplicada ao LED.
- **O aviso dela sobre reincidência**, e ele vale como método: a rota de escrita
  já foi apontada como causa nesta casa antes, e *"reconectar cura"* foi
  concluído e derrubado **quatro vezes desde 17/07**. Quem for mexer na cura da
  lightbar responde primeiro o que derrubou a conclusão anterior.

**As decisões antigas que continuam abertas:**

- **A procedência da arte dos SVG.** Ela não lembra a origem e os desenhos foram
  editados aqui. Fica como **risco aberto de licença**. Uma saída, sem pressa:
  redesenhar os três do zero a partir dos aparelhos dela.
- **O `1.0.0`** — quando o produto está pronto é decisão dela, e o critério é
  ver funcionando num PC novo.
- **As perguntas abertas nos índices de 07/08 e 08/08** continuam válidas;
  nenhuma foi respondida.

E há uma coisa fora do código que continua de pé: **a senha dela está em cinco
commits públicos desde 22/05**. Registrado em memória; só ela pode trocar.

---

## 4. Como não repetir o que já custou caro

Cinco armadilhas, escolhidas por preço. A lista completa e numerada — **doze**
hoje — está em [`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md), e a de tela
em [`COMO-OLHAR-A-TELA.md`](COMO-OLHAR-A-TELA.md).

1. **Pergunte QUEM MAIS está escrevendo neste dispositivo — e com que
   permissão.** É a pergunta 1 do método lida por inteiro, e foi a que custou
   dezesseis dias: o Steam com `hidraw` aberto em leitura+escrita nunca entrou
   na lista de suspeitos. O comando é barato:
   `readlink /proc/*/fd/* 2>/dev/null | grep hidraw`.
2. **Nunca peça cronômetro à mão humana.** Duas rodadas se perderam pedindo *"em
   que instante parou"*, e as duas respostas eram incompatíveis entre si —
   **defeito do instrumento, não dela**. A terceira fechou a questão trocando o
   tremor **de lado**: ou muda de mão, ou não muda. Redesenhe para que a resposta
   seja **sentida**, não medida.
3. **Controle negativo não é prova de obediência.** O R2 ficar solto enquanto o
   L2 endurece prova que o comando **não vazou de lado**; **não** prova que o
   lado direito obedece. Foi registrado errado, e ela pegou.
4. **Uma medição que só existe em docstring envelhece sem que ninguém note.**
   Uma frase de docstring foi copiada para o caderno como se fosse medição — e
   era falsa: a escavação achou quatro acendimentos dentro do período que ela
   dava como morto. Toda medição que muda um veredito **vira linha em
   `ensaios.csv` no mesmo dia**.
5. **Para provar obediência de cor, use uma cor que NINGUÉM MAIS QUEIRA, e com o
   daemon parado.** Escrever verde com o daemon vivo quase fez registrar
   `não obedece`: o daemon reescreveu a cor dele por cima em menos de um minuto,
   e a barra **estava** obedecendo — a ele.

**As cinco de 11/08 não sumiram, e continuam valendo** (cada uma agora mora
onde é usada): ler o **fonte** antes de medir por olho (canônica §5); **provar
que a peça responde** antes de perguntar de que lado ela falha (método, B2);
conferir **geometria de SVG na imagem**, não na aritmética; **valor de domínio
nunca leva acento** (`scripts/validar-acentuacao.py`); e **editar um arquivo
invalida as citações de linha dele** em todo o repositório — realinhe por diff,
não à mão.

---

## 5. Se você só tem cinco minutos

Rode isto, nesta ordem, e você sabe onde está:

```bash
git status --short                             # a leva aberta, antes de tudo
git log --oneline -15                          # o que já entrou
.venv/bin/python scripts/eliminacao.py         # o veredito do caderno de ensaios
python3 scripts/check_paridade_transporte.py   # a dívida do mapa, em número
```

E leia, nesta ordem, se for tocar no aparelho: o
[`METODO-DE-ISOLAMENTO.md`](METODO-DE-ISOLAMENTO.md) — o checklist é o que
comprou esta bancada — e a
[CANETA-NA-MÃO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md),
que é o que ele produziu numa noite.
