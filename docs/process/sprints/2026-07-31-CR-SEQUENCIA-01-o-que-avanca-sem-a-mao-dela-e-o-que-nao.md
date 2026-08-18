# CR-SEQUÊNCIA-01 — o que avança sem a mão dela, e o que não

- **Status:** ABERTA — documento de resposta e reordenação do trilho CR. Nenhuma
  linha de código nesta rodada
- **Prioridade:** MÉDIA — nada aqui desfaz trabalho dela; mas destrava um trilho
  parado desde 25/07
- **Aberta em:** 31/07/2026, a pergunta dela, literal:

  > *"na clean room a ideia era nos afastarmos do dsx, mas depois vimos que não
  > temos materialidades do dsx no repo, nesse caso você sozinha conseguiria dar
  > sequência a ele, certo? sem ter a necessidade de eu testar os botões e afins,
  > afinal temos sprints até pra renomear cada tipo de gatilho."*

- **Normativa que manda aqui:** [CLEAN-ROOM.md](../CLEAN-ROOM.md), vigente desde
  25/07 e **não revogada**
- **Reordena:** CR-01 a CR-06, que estão fora de escopo por decisão dela desde
  25/07 (*"essas não faremos hoje"*), mantida em 26, 29 e 30/07

## A resposta curta

**A premissa está certa, e a conclusão é meio certa.** O material que o processo
recusou de fato não está no repositório — isso eu medi. Mas o trilho **não** é
todo executável sozinha: cinco das seis sprints são, e a sexta não é por
proibição do próprio processo, não por limite de capacidade.

A que não é — a **CR-04, os efeitos da casa** — é justamente a que produz os
valores. E o motivo de ela precisar da mão dela é o mesmo motivo de o processo
existir.

## Primeiro, a premissa: o que de DSX existe mesmo no repositório

Medido hoje: **133 arquivos rastreados citam "dsx"**. Não é pouco — mas é preciso
separar o que está de que lado da fronteira R4, e a separação é limpa.

| O que existe | Onde | Lado da fronteira |
|---|---|---|
| O protocolo UDP (envelope + instruções) | `daemon/udp_server.py` (83 menções), `docs/protocol/udp-schema.md` | **Fato de interoperabilidade** — o CLEAN-ROOM abençoa por escrito |
| Os ordinais do enum de instruções | `udp_server.py`, conferidos em quatro implementações | Fato, e a divergência entre elas está documentada |
| A aba "Navegação DSX" e o `dsx_recover.sh` | GUI e scripts | Nome de compatibilidade, não curva |
| **As tabelas de bytes dos 12 modos prontos** | **em lugar nenhum** | É o material recusado |

A prova de que o material recusado está mesmo ausente é bonita, e é por
construção: `daemon/udp_server.py:149-163` declara
`DSX_CANNED_TRIGGER_MODES` com os doze nomes — `GameCube`, `VerySoft`, `Soft`,
`Hard`, `VeryHard`, `Hardest`, `Rigid`, `VibrateTrigger`, `Choppy`, `Medium`,
`VibrateTriggerPulse`, `VibrateTrigger10Hz` — **só para falhar alto**. O
comentário logo acima (`:140-148`) escreve a razão sem eufemismo: a única
transcrição pública está num repositório sem licença, e copiar seria problema de
licença, não de engenharia.

Então sim: **o repositório está limpo do que importa.** A premissa dela está
correta.

## O que eu descobri no caminho, e ninguém tinha ligado

Os **19 presets paramétricos que existem hoje** carregam nome do DSX — e a regra
R2 do processo diz o contrário.

- `core/trigger_effects.py:1` abre com *"Factories dos 19 presets de trigger
  conforme DSX Paliverse"*, e `:30` define
  `AMPLITUDE_SCALE = 32  # Normaliza 0-8 (DSX) -> 0-255 (HID byte)`.
- `app/actions/trigger_specs.py:81-127` rotula, na tela dela: **"Rígido (Rigid)"**,
  **"Arco (Bow)"**, **"Galope (Galloping)"** — o nome em português **com o nome
  do DSX entre parênteses**.
- E a regra R2 do [CLEAN-ROOM.md](../CLEAN-ROOM.md) manda o oposto: *"Efeitos
  nossos usam vocabulário nosso, em português: `Pesado`, `Macio`, `Trepidante`.
  **Nunca** `Hard`, `Soft`, `Choppy`."* — com a razão escrita: *"Nomes iguais
  convidam à comparação byte a byte, e é a comparação que cria o problema —
  inclusive quando não houve cópia."*

Há uma colisão literal para provar que o risco não é teórico: **`Rigid` é ao
mesmo tempo o modo enlatado nº 7 do DSX (que o Hefesto recusa) e um dos 19
presets nossos (que o Hefesto implementa).** Mesmo nome, coisas diferentes, e a
tela dela mostra os dois mundos com a mesma palavra.

**Isto não é violação, e é importante dizer por quê.** Os 19 são **paramétricos**:
quem dá os números é ela, e o código calcula `(mode, forces)` a partir deles —
não há tabela fixa transcrita de lugar nenhum. Eles estão do lado *"fato do
protocolo"* da fronteira R4, e são **anteriores** ao processo de 25/07. A R2 fala
dos **efeitos nossos**, que a CR-04 ainda vai criar.

Mas duas sprints estão falando da mesma coisa sem se citar:
[GATILHO-PALAVRA-01](2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md),
que renomeia os dezenove para o português, e a **R2**, que existe justamente para
que nome nosso não pareça nome deles. Quem executar a GATILHO-PALAVRA-01 sem ler
a R2 vai decidir sozinho se o `(Rigid)` do parêntese fica — e essa decisão é de
sala limpa, não de vocabulário.

## O trilho, sprint por sprint: quem consegue fazer o quê

| Sprint | O que fecha | Sozinha? |
|---|---|---|
| **CR-01** | posição jurídica registrada, com data | **Sim** — é documento |
| **CR-02** | formato que recusa valor sem proveniência | **Sim** — schema, guarda e teste |
| **CR-03** | **a bancada de medição** | **Sim, inteira** — é a maior peça de código do trilho |
| **CR-04** | **os efeitos da casa** | **Não. E o "não" é do processo, não meu** |
| **CR-05** | o `NOTICE` declarando toda proveniência de terceiros | **Sim** — e está atrasada (ver abaixo) |
| **CR-06** | curvas publicadas como material livre | **Sim**, depois da CR-04 |

### Por que a CR-04 não avança sem ela — e por que isso é o ponto, não o obstáculo

A regra **R1** diz onde um valor pode nascer: *"trabalhe a partir da **sensação
no controle**, nunca da lembrança do arquivo. O ponto de partida legítimo é o
hardware na sua mão."*

A regra **R3** diz o que precisa vir junto com o valor, e o formato já está
escrito em `docs/protocol/curvas-proprias.md`: **quem mediu**, **quando**, **com
que controle e transporte**, e **o que a pessoa sentiu e por que parou naqueles
números**. E fecha sem saída: *"Valor sem proveniência não entra. (...) um único
número órfão na tabela contamina a defesa da tabela inteira."*

Uma curva que eu invente não tem mão nem sensação. Ela entraria na tabela com os
campos `Medido por`, `Controle` e `Nota` vazios ou preenchidos com ficção — e a
tabela inteira perderia a defesa, pela regra que o próprio documento escreveu.

E há um segundo motivo, mais duro, que vale registrar sem rodeio: **a defesa que
o processo constrói é exatamente a que eu não posso oferecer.** O CLEAN-ROOM
descreve a assimetria — *"sem registro, quem não copiou tem de provar uma
negativa — impossível. Com registro datado de como cada valor nasceu, o ônus se
inverte"*. Um número gerado por mim é o pior registro possível nessa moldura: eu
não tenho como provar que nunca vi aquelas tabelas. A mão dela no gatilho não é
formalidade — **é a base de prova inteira**.

O que eu posso fazer é tornar a parte dela pequena. É literalmente para isso que
a **CR-03** existe, e está escrito lá: *"Uma bancada boa torna o caminho legítimo
o mais fácil — e é assim que processo de sala limpa sobrevive ao cansaço. Se
medir for penoso e copiar for cômodo, o processo falha na primeira noite ruim."*

Com a bancada pronta, a parte dela é: escolher um controle, mexer nos sete
parâmetros sentindo o gatilho, dar um nome, salvar. Os campos `medido_por`,
`medido_em` e `controle` a bancada preenche sozinha
(`CR-03`, terceira entrega). Minutos por efeito, não horas.

## O que fazer com isso — a ordem proposta

A decisão de reabrir o trilho é dela; esta é a ordem que a medição sustenta.

### E1. CR-05 primeiro, e sozinha — porque já está atrasada

A auditoria de 31/07 mediu o que a CR-05 existe para curar, e o estado é pior do
que quando ela foi aberta: `assets/dkms/hid-playstation/hid-playstation.c:1`
declara `GPL-2.0-or-later`, `hid-nintendo.c:1` declara `GPL-2.0+`, e
`rtw88-usb/usb.c:1` declara `GPL-2.0 OR BSD-3-Clause` — três drivers de kernel
completos mais oito arquivos `.patch` — enquanto `LICENSE:1` diz `MIT License` e
o `README.md:346` diz *"MIT — veja LICENSE"* sem ressalva. O `NOTICE` (61 linhas,
lido inteiro) menciona só as regras udev do pydualsense e as curvas recusadas.

**A CR-05 é a única do trilho que a v0.4.0 atravessou com dano real**, e o
próprio documento dela já traz o enquadramento jurídico pronto (*"não são
linkados"*, distribuídos como fonte separada). É escrever a seção e ajustar duas
frases.

**Aceite:** o `NOTICE` declara os componentes de `assets/dkms/` com licença
própria preservada; `LICENSE` e `README` dizem *"MIT, exceto `assets/dkms/*`"*.
Nenhum arquivo de `assets/dkms/` é tocado.

**Risco:** nenhum. É texto, e a decisão já está registrada na sprint.

**Medição que evita alarme falso:** o vetor de redistribuição é o **tarball mais
o instalador** — `packaging/arch/PKGBUILD` **não** empacota `assets/dkms`
(só `optdepends 'dkms'`, linha 56), e `grep -rln dkms .github/workflows/` devolve
vazio. Nenhum pacote binário publicado carrega os fontes GPL.

### E2. CR-01 e CR-02, sozinhas — o par que destrava o resto

A CR-01 tem duas caixas abertas, e uma delas é a varredura de `assets/dkms/**`
que a E1 acima faz de qualquer jeito. A CR-02 é o formato que recusa valor sem
proveniência: schema, guarda e o teste que morde. **Nenhum valor de curva entra
antes das duas**, por regra escrita.

**Mordida da CR-02:** um efeito com `medido_por` vazio tem de **reprovar**. Teste
que aceita a tabela sem proveniência não testa nada.

### E3. CR-03, a bancada, sozinha — e é a maior peça

Todas as cinco entregas da CR-03 são código: os sete parâmetros ao vivo na aba
Gatilhos, a leitura de L2/R2 ao lado (o widget já existe na aba Status), o salvar
com nome e nota, o aplicar em qualquer um dos quatro controles, e o A/B.

**A restrição declarada na própria sprint continua valendo e é a parte perigosa:**
a bancada escreve **direto no hardware** enquanto está aberta, e precisa devolver
o controle ao daemon ao sair, pelo mesmo caminho que a aba Rumble já usa no teste
de motores. Esta casa já tem a cicatriz de escritor de hidraw sem dono e não vai
criar mais um.

**Cuidado que a auditoria de hoje acrescenta:** com o `display_authority` caindo
sozinho (ver
[SINAL-DE-JOGO-01](2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md)),
a bancada precisa de posse **explícita** enquanto estiver aberta — não pode
depender de quem está ganhando a disputa de exibição naquele segundo, ou o
gatilho muda de sensação no meio da medição e contamina a proveniência.

### E4. CR-04 — a parte dela, e só a parte dela

Depois da bancada: ela senta, sente, nomeia e salva. Cada efeito com a nota do
que sentiu. Nada mais.

### E5. A decisão que a GATILHO-PALAVRA-01 não pode tomar sozinha

O `(Rigid)`, o `(Bow)` e o `(Galloping)` dos rótulos: ficam, saem, ou viram outra
coisa? A R2 recomenda que saiam. O contra-argumento é real e precisa estar na
mesa: o parêntese é o que permite a ela reconhecer, na tela, o modo que um guia
de jogo ou um mod chama pelo nome em inglês.

**Isto é decisão dela**, e é decisão de sala limpa — não de vocabulário. O que
esta sprint entrega é a pergunta bem posta, com o custo dos dois lados medido.

Vale lembrar o que **não** está em disputa: o campo `name` dos dezenove é
**contrato** de disco, IPC e DSX, travado por
`tests/unit/test_gatilho_palavra_rotulos.py`. Só o rótulo muda. Isso não é
negociável, e já está protegido por teste.

## Como você valida

Esta sprint não tem tela para validar — é decisão e ordem. O que ela pede de você
é uma resposta a três perguntas:

1. **Reabrir o trilho CR?** Ele está fora de escopo por decisão sua desde 25/07,
   e nada aqui muda isso sem você mandar.
2. **A CR-05 pode ir sozinha, agora?** É a única com dano medido hoje, é só
   texto, e não depende das outras.
3. **O `(Rigid)` fica no rótulo?** (a E5 acima)

## O que fica de fora, por escrito

- **Escrever qualquer valor de curva.** Não entra sem CR-01 e CR-02 fechadas, e
  não nasce da minha mão em hipótese nenhuma.
- **Mexer nos 19 presets existentes.** Eles são paramétricos, são anteriores ao
  processo, e estão do lado legítimo da fronteira. O que se decide aqui é o
  **rótulo**, e só na E5.
- **Tocar em `assets/dkms/`.** A E1 acrescenta declaração ao `NOTICE`; os fontes
  de terceiros ficam exatamente como estão, com o SPDX intacto — é isso que os
  torna lícitos.
- **Reescrever histórico.** O CLEAN-ROOM tem uma seção inteira sobre isso, e ela
  vale aqui: *"Reescrever histórico onde não houve infração cria a aparência de
  que houve."*

## O que eu não medi

- **Se algum dos 19 presets produz, por coincidência, a mesma curva de um dos 12
  enlatados.** Não comparei bytes — e não vou: comparar exigiria ter as tabelas
  deles, que é exatamente o que a R1 proíbe. O `curvas-proprias.md` já antecipa
  essa pergunta e responde certo: *"a defesa contra essa leitura não é a diferença
  dos números: é o registro de que estes nasceram de medição datada"*.
- **As dependências Python além do `pydualsense`** contra o `NOTICE` (textual,
  platformdirs, jeepney e as demais) — a auditoria conferiu só kernel/DKMS e as
  regras udev. A CR-05 deve varrer todas.
- **Se os oito `.patch` de `assets/dkms/` têm cabeçalho de licença próprio** ou
  herdam o do arquivo que modificam. É item da CR-05.
- **O estado real das caixas da CR-01 e da CR-02** além da leitura dos dois
  documentos: não cruzei entrega por entrega com o código de hoje.
