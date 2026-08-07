# RECEITA-ERRADA-01 — o doctor mandava rodar o que não resolvia

- **Achado em:** 06/08/2026, em duas frentes. A primeira metade **na máquina
  dela**, sem webcam e sem o controle no cabo, rodando o doctor; a segunda por
  **auditoria** do state do WirePlumber instalado, lendo o código do `sed` ao
  lado do código que o WirePlumber usa para ler o mesmo arquivo
- **Estado:** **CURA APLICADA** nos dois, commitada em `53f6d8b`; esta sprint é
  a **materialização atrasada** — o código e os testes que mordem existem desde
  06/08, o documento é que faltava
- **Gravidade:** **MÉDIA** no efeito imediato do primeiro e **ALTA** no
  desperdício (mandava procurar e rodar onde não havia solução);
  **ALTA** no segundo, porque o dano é **irreversível** — apaga preferência
  antiga dela que ninguém tem como reconstruir
- **Causa-raiz:** **MEDIDA** nos dois. No primeiro, com reprodução na bancada
  dela em 29/07, 30/07 e 06/08; no segundo, no código dos **dois** lados — o
  `sed` que estava aqui e o `collectStored` do WirePlumber 0.5.12 instalado
- **Índice:** [O dia dos cento e dezesseis agentes](2026-08-06-INDICE-o-dia-dos-cento-e-dezesseis-agentes.md)
- **Parentes, e distintas:**
  - [SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md)
    — é a sprint da **política** que fabrica o estado, e continua **ABERTA**;
    esta aqui é sobre o doctor **falar** dele. As três linhas que aquela lista
    como "já curado em 06/08" são exatamente o que este documento registra por
    inteiro;
  - [DIALOGO-QUE-MATA-A-JANELA-01](2026-08-06-DIALOGO-QUE-MATA-A-JANELA-01-o-aviso-que-deixou-a-janela-dela-morta.md)
    — mesma classe noutra camada: a receita que leva ao lugar errado;
  - [ENTREGA-QUE-NAO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
    — o antecedente direto da segunda metade: o filtro de porta existia,
    documentado e testado por dentro, e **ninguém o chamava**;
  - [MIC-USB-01](2026-07-25-MIC-USB-01-tres-mutes-empilhados.md)
    — as camadas de mudo do mesmo microfone; a promoção explícita citada aqui
    é entrega dela;
  - [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
    — de onde vem a lição de backup que reaparece no que fica aberto aqui;
  - [ACUSA-O-CULPADO-01](2026-08-06-ACUSA-O-CULPADO-01-o-doctor-acusava-quem-nao-tinha-feito-nada.md)
    e
    [SELO-VERDE-CEDO-DEMAIS-01](2026-08-06-SELO-VERDE-CEDO-DEMAIS-01-o-doctor-afirmava-o-que-so-valia-nesta-bancada.md)
    — mesmo turno, mesmo commit, mesma família: o doctor dizendo algo que não
    se sustenta.

**Grau de cada afirmação**, como manda a casa: **MEDIDO** = há reprodução em
bancada, linha de journal, ou teste que reprova com a cura arrancada;
**SUSPEITA COM MECANISMO** = o caminho de código foi lido e fecha, o efeito não
foi observado; **SEM PROVA** = está dito e ninguém verificou.

---

## O que os dois têm em comum

São dois defeitos do mesmo turno, do mesmo commit e do mesmo aparelho: o
**microfone dela**. E os dois são a mesma forma de mentira — **duas verdades
convivendo dentro do mesmo programa**, com a errada sendo a que aparece:

- no primeiro, o **check** e a **cura** do doctor tinham, cada um, o seu
  critério de "fonte elegível". A tela mostrava o critério do check; quem agia
  era o da cura. O que ela lia era o que não ia acontecer;
- no segundo, o **comentário** da função prometia *"preserva o resto do state"*
  e o **código** ao lado dele destruía o histórico inteiro. Quem lia o
  repositório via a promessa; quem rodava o script recebia o código.

Nenhum dos dois aparecia como erro: o primeiro imprimia uma receita com a
autoridade de um diagnóstico, e o segundo terminava devolvendo `0`, calado.

---

## Defeito 1 — RECEITA-ERRADA-01: o comando que não podia funcionar

**Gravidade: MÉDIA no efeito, ALTA no desperdício. Grau: MEDIDO, nas duas
metades.**

O `check_default_source_monitor` reprova quando a fonte de captura padrão é um
**monitor** — o loopback da saída, que faz qualquer aplicativo gravar o som que
**sai** do computador em vez da voz. Reprovar está certo. O problema era o que
vinha depois do `[FAIL]`: a receita.

### Metade A — mandava rodar um comando impotente (MEDIDO em 06/08)

Na máquina dela, sem webcam, sem nada plugado no jack e com o controle fora do
cabo, a tela dizia:

```
[FAIL] a fonte de captura padrão é um MONITOR (...) — rode: scripts/doctor.sh --fix-mic
```

E o `--fix-mic`, quando rodado, respondia:

> *não há nenhuma fonte de captura com porta usável para eleger*

e não fazia nada. Ele **só sabe eleger outra fonte de captura**, e não havia
nenhuma. O doctor mandava rodar um comando que, naquele estado, era impotente
por construção.

### Metade B — oferecia o alvo que a própria cura recusa (MEDIDO em 29 e 30/07)

Quando havia o que oferecer, o alvo saía **errado**. O check calculava o
candidato a partir de uma lista **sem** filtro de porta, e chegava à entrada
analógica da onboard:

```
[FAIL] ... — cura: pactl set-default-source alsa_input.pci-0000_0c_00.4.analog-stereo
```

A medição da mesma máquina, no mesmo instante, é o que condena esse alvo:

| porta | aparelho | disponibilidade |
|---|---|---|
| `analog-input-front-mic` | onboard | `not available` |
| `analog-input-rear-mic` | onboard | `not available` |
| `analog-input-linein` | onboard | `not available` |
| `iec958-stereo-input` | DualSense | `availability unknown` |

O `pactl set-default-source` **aceita** esse nó — ele não valida porta. O
WirePlumber, que não consegue honrar uma fonte sem porta usável, reelege
sozinho e devolve o **monitor** em segundos. A receita levava ao lugar errado, o
defeito voltava por conta própria, e agora com a chancela do doctor.

E a cura do próprio doctor **já sabia disso**: o `fix_default_source_monitor`
descartava a onboard e elegia o mic do controle. O doctor imprimia na tela dela
um comando que o doctor se recusava a executar.

### A raiz: dois critérios de elegibilidade no mesmo programa

Não são dois defeitos, é um: **o check e a cura não compartilhavam o critério**.
O filtro de porta (`_source_porta_ativa_indisponivel`, `scripts/doctor.sh:563`)
existia com a medição escrita ao lado, e era chamado **inline, só dentro da
cura**. O check calculava por conta própria.

Enquanto o critério for escrito duas vezes, ele diverge — e o pior lugar para a
divergência aparecer é a tela, porque é ali que ela vira instrução.

### A cura, em duas partes

**Um filtro só, com nome.** O critério inline virou a função
`_sources_com_porta_usavel` (`scripts/doctor.sh:623`), que recebe o texto longo
de `pactl list sources` e deixa passar apenas as fontes cuja porta ativa não
está explicitamente `not available`. O check (`:636`) e a cura (`:713`) passam
pelo **mesmo cano** antes de escolher. Assim eles não podem mais discordar: o
alvo oferecido é, por construção, o alvo que seria eleito.

`unknown` continua contando como **usável** — é o caso da entrada do DualSense,
que grava de verdade (pico 4606 medido em 26/07; pico 441 / RMS 73 num quarto
silencioso em 30/07). Confundir `unknown` com `not available` descartaria o
único microfone de verdade da máquina dela.

**Quando não há alvo, o texto muda de assunto.** Em vez de apontar para um
comando, o doctor passa a dizer o que está acontecendo e o que resolve:

```
[FAIL] a fonte de captura padrão é um MONITOR (...) — o que qualquer app gravar
       é o áudio de SAÍDA do sistema, não a voz, e o medidor de nível ainda
       mostra sinal (parece funcionando)
[INFO]   o --fix-mic NÃO resolve este caso: ele só sabe ELEGER outra fonte de
         captura, e não há nenhuma com porta usável nesta máquina agora
[INFO]   o que resolve é hardware: conecte um mic, uma webcam com mic, ou o
         DualSense (no cabo, ou por Bluetooth com o mic ligado)
```

Citar o `--fix-mic` para dizer que ele **não** serve é honestidade; mandar
rodá-lo é que era o defeito.

A mesma correção alcançou a cura (`scripts/doctor.sh:758`): quando não há alvo,
ela não sai mais com um "não consegui" seco. Dizer que não deu não basta,
porque **o estado em que ela fica é o defeito inteiro de pé** — e ele não parece
defeito: o medidor de nível mostra sinal, que é o áudio de saída da máquina. O
`[WARN]` agora diz a consequência de privacidade por escrito.

### As mordidas

Em `tests/unit/test_fonte_padrao_01_e_cura_do_fix_mic.py`:

- `test_sem_fonte_alguma_o_check_nao_manda_rodar_o_fix_mic` — cobra que
  `rode: scripts/doctor.sh --fix-mic` **não** apareça no estado sem fonte, e que
  apareçam `NÃO resolve` e `conecte um mic`;
- `test_sem_fonte_alguma_a_cura_diz_a_consequencia_de_privacidade` — cobra o
  `áudio de SAÍDA` no `[WARN]` da cura;
- `test_a_cura_e_oferecida_no_texto` — cobra que o alvo oferecido seja o do
  controle **e** que a onboard **não** apareça.

Em `tests/unit/test_fonte_padrao_ignora_porta_indisponivel.py`, classe
`TestFiacao`, o portão que pega a regressão que já aconteceu de verdade: a
função existir e **não ser chamada**. Ele verifica a cadeia por **invocação**,
nunca por menção — a primeira versão desse teste procurava o nome solto e
passava com a chamada arrancada, porque o nome também aparece no comentário
logo acima. Teste tautológico é o defeito que esta casa nomeia.

- `test_o_check_oferece_o_alvo_que_a_cura_elegeria` — a metade nova: o check
  tem de conter a chamada `| _sources_com_porta_usavel "`, e ela tem de vir
  **antes** da chamada do seletor;
- `test_a_cura_filtra_por_porta_antes_de_escolher` — idem para a cura;
- `test_o_filtro_compartilhado_chama_mesmo_o_criterio_de_porta` — o elo do meio
  não pode ser um cano oco: `_sources_com_porta_usavel` tem de invocar
  `_source_porta_ativa_indisponivel` por dentro.

**MEDIDO em 06/08/2026 nesta bancada:** os três arquivos de teste desta sprint
rodam com **68 verdes** (`.venv/bin/python -m pytest -q`).

### Nota datada — o contrato que mudou de alvo

Até 06/08, `test_a_cura_e_oferecida_no_texto` exigia o **contrário**: que o
check oferecesse `pactl set-default-source <onboard>`. A decisão não foi
apagada — está no docstring do próprio teste, com a data e o motivo de ter
caducado. E o registro é constrangedor no detalhe que importa: **a própria
suíte já sabia**, três classes abaixo, que a cura descarta a onboard. Duas
asserções do mesmo arquivo cobravam coisas opostas, e nenhuma reprovava,
porque nada cobrava a **concordância** entre elas.

O que ficou travado no lugar não é mais um alvo específico: é a concordância.

---

## Defeito 2 — PILHA-TRUNCADA-01: o histórico de microfone que sumia

**Gravidade: ALTA (dano irreversível). Grau: MEDIDO no código dos dois lados;
SUSPEITA COM MECANISMO no efeito em produção.**

`remove_configured_dualsense`, em `scripts/fix_wireplumber_default_source.sh`,
existe para tirar **uma** entrada do state do WirePlumber: a fonte padrão
persistida que aponta para o mic do controle, para ele não ser reeleito no
próximo boot. O comentário prometia *"preserva o resto do state"*. O que estava
escrito era:

```bash
sed -i.bak '/^default\.configured\.audio\.source=.*[Dd]ual[Ss]ense/Id'
```

### A raiz: uma pilha contígua não é um conjunto de chaves

É esta a frase inteira do defeito, e vale para muito mais coisa que áudio.

Olhando o arquivo, `~/.local/state/wireplumber/default-nodes` **parece** um
`.ini`: uma chave por linha, cada uma independente da outra. Apagar uma linha
de um `.ini` afeta só aquela linha.

Só que este arquivo não é lido assim. Ele guarda um **histórico ordenado de
preferência**, e o WirePlumber o lê por **caminhada**, parando no primeiro
buraco. O código está em
`/usr/share/wireplumber/scripts/default-nodes/state-default-nodes.lua`, função
`collectStored`, linhas 141-155 da versão 0.5.12 instalada nesta máquina:

```lua
key = key_base                      -- default.configured.audio.source
repeat
  local v = state_table [key]
  table.insert (stored, v)
  key = key_base .. "." .. tostring (index)
  index = index + 1
until v == nil                      -- PARA no primeiro buraco
```

Ou seja: `...source`, `...source.0`, `...source.1` não são três chaves — são
**três degraus de uma escada**. Some o primeiro degrau e os outros dois não
deixam de existir: eles ficam **inalcançáveis**, que dá no mesmo e é pior,
porque continuam ocupando lugar no arquivo e não aparecem em lugar nenhum.

Esse histórico não é enfeite. Ele é o que decide a eleição quando há empate de
prioridade: quem está na pilha soma `+20001 - i` na conta do WirePlumber
(`state-default-nodes.lua:48`). Perder a pilha é perder a memória de todas as
escolhas de microfone que ela já fez naquela máquina.

### O `=` que só via a chave-base

O padrão tinha `source=` colado. O `=` logo depois de `source` faz o casamento
pegar a chave-base e **não** pegar `...source.0=` nem `...source.1=`. Dessa
única linha saem **dois** defeitos, opostos entre si — e o state real da máquina
dela, em 06/08, exibia os dois ao mesmo tempo, porque ele tem três degraus:
base = a onboard, `.0` = o mic do DualSense, `.1` = um sink que já foi fonte
(a assinatura de "um monitor já foi eleito aqui", porque a camada pulse resolve
`<sink>.monitor` para o nó **sink**, e é o nome do nó que fica gravado).

- **quando a base NÃO é o DualSense** — que era o caso de 06/08 — o `grep` e o
  `sed` não casavam nada, e a função era um **no-op**: as duas entradas do
  DualSense que ela existe para tirar ficavam exatamente onde estavam;
- **quando a base É o DualSense**, casava, apagava a base, e a leitura do
  WirePlumber passava a parar na primeira volta: `.0` e `.1` ficavam
  inalcançáveis. **Some o histórico inteiro de preferência de microfone dela**,
  não só a linha do controle.

Falhar em fazer o trabalho e destruir o histórico são os **dois lados da mesma
linha**. E nenhum dos dois aparecia no log: os dois terminavam com a função
devolvendo `0`.

### A cura: reescrever a pilha, contígua, sem as entradas do controle

A função pura `_pilha_sem_dualsense`
(`scripts/fix_wireplumber_default_source.sh:195`) recebe o state na entrada
padrão e devolve o state corrigido na saída padrão. Ela:

1. deixa passar intacta **toda** linha que não seja da pilha de `audio.source`
   — inclusive a pilha de `audio.sink` inteira, inclusive a entrada do DualSense
   nela: quem desliga o mic não está pedindo para esquecer o alto-falante do
   controle;
2. descarta os degraus cujo valor casa `dualsense`;
3. **renumera o que sobra**, em ordem: quem sobra vira base, `.0`, `.1`, ...

O passo 3 é o que faz a diferença entre curar e trocar de defeito. Sem
renumerar, sobra um buraco no meio da escada — e o `collectStored` para nele
exatamente como parava antes.

O casamento do portão da função também foi aberto para a pilha inteira
(`...audio\.source(\.[0-9]+)?=`, `:218`), senão o `grep` que guarda a porta
continuaria cego às chaves indexadas e nada rodaria.

É o que o comentário sempre prometeu, e o que o código não fazia.

### As mordidas

`tests/unit/test_pilha_truncada_01_o_historico_de_microfone_que_sumia.py` roda a
**função shell de verdade**, por `source`, em vez de reimplementá-la em Python —
e o `HOME` é de mentira, em `tmp_path`, porque um teste que apontasse para o
`HOME` real ficaria lendo o state de áudio de quem roda a suíte (é para isso
que o canário de sistema de arquivos desta casa existe).

O detalhe que faz esses testes morderem de verdade: o helper `_fontes()`
**reimplementa o `collectStored`** — ele lê a saída caminhando pela escada e
parando no primeiro buraco, que é como o WirePlumber leria. As asserções são
sobre o que o WirePlumber **enxergaria**, não sobre as linhas do arquivo.

- `test_base_e_o_controle_o_resto_da_pilha_sobrevive` — o caso que destruía: o
  WirePlumber tem de continuar lendo a onboard e a webcam;
- `test_a_pilha_fica_contigua` — cobra a renumeração, e cobra que **não** sobre
  um degrau a mais;
- `test_no_estado_real_as_duas_entradas_do_controle_saem` — o outro lado, com o
  state real de 06/08 copiado sem alteração: antes, aqui, a função não fazia
  nada;
- `test_a_pilha_de_sink_nao_e_tocada` — o histórico de saída é escolha dela;
- `test_sem_dualsense_nenhum_o_state_sai_identico` — idempotência: o que não tem
  o defeito não pode ser reescrito;
- `test_o_grep_da_funcao_ve_as_chaves_indexadas` — o portão do casamento; se ele
  não casar `.0`, nada roda e a função volta a ser um no-op silencioso.

### O grau, dito por inteiro

Aqui a casa exige uma distinção que é fácil de borrar:

- **MEDIDO:** o `sed` antigo e o `collectStored` do WirePlumber 0.5.12 — os dois
  foram lidos, e o state real da máquina dela foi lido junto. O mecanismo fecha
  nos dois sentidos;
- **SUSPEITA COM MECANISMO:** o efeito **em produção**. Esta função edita o
  arquivo com o WirePlumber **vivo**, e o próprio script documenta, no irmão
  `unmute_dualsense_routes`, que o WirePlumber **grava o estado ao sair** e
  sobrescreveria a edição. Então, em campo, ou o `sed` era sobrescrito (no-op
  silencioso) ou vencia e truncava — e ninguém observou qual dos dois.

Essa ordem de escrita **não foi mexida** nesta leva. Está logo abaixo.

---

## O que fica ABERTO

- **A edição acontece com o WirePlumber vivo.** No modo `--disable-source`, o
  despacho chama `install_disable_dropin`, `remove_configured_dualsense` e só
  então `restart_wireplumber` (`scripts/fix_wireplumber_default_source.sh:501-504`).
  O irmão `unmute_dualsense_routes` faz `systemctl --user stop wireplumber`
  **antes** de editar o arquivo de rotas (`:341`) — a assimetria está no mesmo
  script, a poucas dezenas de linhas. **Grau: MEDIDO** na ordem (é o que o
  código faz); **SUSPEITA COM MECANISMO** no efeito, porque a corrida não foi
  reproduzida. É o item que a própria cura declara, por escrito, como pendente.
- **`remove_configured_dualsense` não tem mordida de comportamento.** Nenhum
  teste a **invoca**: o que existe é a função pura `_pilha_sem_dualsense` e um
  contrato de texto sobre o `grep` dela. O backup, o `mktemp`, o `mv` e o ramo
  de erro não são exercitados por ninguém. **Grau: MEDIDO** — `grep -rn
  "remove_configured_dualsense" tests/` devolve só o docstring e o contrato de
  texto.
- **O backup se sobrescreve.** `cp -f "${STATE_FILE}" "${STATE_FILE}.bak"` usa
  nome fixo: a segunda execução apaga a única cópia do histórico anterior, e é
  justamente o histórico que este defeito destruía. É a mesma classe que a
  [RADIO-ABERTO-01](2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md)
  já registrou noutro lugar. **Grau: MEDIDO** no código; **SEM PROVA** de que já
  tenha custado alguma coisa.
- **O ramo de preferência do CHECK não é distinguido por teste nenhum.** O check
  consulta `_prefere_mic_do_dualsense` para decidir se o controle vem primeiro
  ou por último, mas na amostra da suíte a onboard já sai pelo filtro de porta,
  então `prefere=0` e `prefere=1` chegam ao mesmo alvo. Numa máquina com webcam
  **e** o mic do controle, os dois ramos divergem, e nada morde a diferença **do
  lado do check** (a cura tem `test_com_opt_in_a_cura_elege_o_controle`).
  **Grau: MEDIDO** na leitura dos testes; **SUSPEITA COM MECANISMO** no efeito.
- **A concordância entre check e cura é travada por contrato de texto.** Há um
  cenário em que os dois foram medidos e concordam (os dois elegem o mic do
  controle), e o resto é garantido por buscar a **chamada** do filtro dentro de
  cada função. Um desvio que mantenha a chamada e mude outra coisa — a ordem dos
  argumentos, o valor de `prefere` — passa. **Grau: MEDIDO** (um cenário);
  **SEM PROVA** para os demais.
- **A política que fabrica o estado continua de pé.** O drop-in 51 rebaixa o mic
  do DualSense para `priority.session = 50`, abaixo de alto-falantes de 696 e
  736 — numa máquina em que o controle é o único microfone, o monitor ganha. O
  sintoma ficou honesto; a causa ficou. Isso é a
  [SEM-MICROFONE-NENHUM-01](2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md),
  que está **ABERTA** e tem pré-requisito de medição declarado. **Grau: MEDIDO**
  (o rebaixamento e as prioridades); **SEM PROVA** da medição que aquela sprint
  exige antes de qualquer entrega.
- **`_sources_com_porta_usavel` revarre o texto longo uma vez por fonte.** Ele
  abre um `awk` por linha da lista curta, cada um lendo o `pactl list sources`
  inteiro. Com meia dúzia de fontes isso não dói; a forma é quadrática mesmo
  assim. **Grau: MEDIDO** na leitura do código; **SEM PROVA** de que custe algo
  em máquina real.
