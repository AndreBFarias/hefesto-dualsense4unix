# ONDE PARAMOS — o estado para a próxima sessão

- **Escrito em:** 11/08/2026, no fim de uma sessão longa, a pedido dela: *"de
  forma que se eu der um barra clear o próximo Claude vá saber o que fazer"*.
- **Para quem chega agora:** leia o `CLAUDE.md` da raiz primeiro (ele diz a
  ordem), depois este arquivo. Ele responde três coisas: **o que mudou hoje**,
  **o que está aberto**, e **o que é dela**.
- **Grau:** os números são MEDIDOS na árvore de 11/08. O que depende de medição
  que não existe está dito com todas as letras.

---

## 1. O que mudou hoje, em uma tela

Foi uma sessão de **medir e reconciliar**, não de construir features. O produto
funciona igual; o que mudou é que agora se sabe **por quê**, e onde a casa
estava mentindo para si mesma.

| entregue | onde |
|---|---|
| Quatro referências de driver, lidas no **fonte C** dos módulos DKMS desta máquina | `docs/protocol/driver-*.md`, `pilha-*.md`, `externos-firmware-*.md` |
| O portão do mapa de canais passou a poder reprovar | `scripts/check_paridade_transporte.py` |
| Transporte virou **dimensão do caso de teste** | `tests/unit/test_paridade_transporte_*.py` |
| O `install.sh` reconhece a máquina e garante o que os módulos precisam | `install.sh`, passo 1 |
| A matriz de versões validadas | `docs/usage/versoes-validadas.md` |
| O delta da máquina limpa e o plano até a versão final | `docs/process/2026-08-11-*.md` |
| O índice das contradições que a leva abriu | `docs/process/sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md` |

**Números no fim do dia:** 8886 testes verdes, `mypy` limpo em 169 arquivos,
todos os portões passando, 291 linhas no mapa de canais.

### As cinco coisas que ficaram sabidas, e não eram

1. **O P4 do LED de jogador é `xx-xx`.** O código desta casa sempre esteve
   certo; a canônica confundia com o nosso próprio `_PLAYER_LED_OVERFLOW`. A
   fonte é `assets/dkms/hid-playstation/hid-playstation.c:1836-1842`. E as cinco
   figuras do driver são **palíndromos**, o que torna a pergunta "esquerda ou
   direita" mal formulada — ela consumiu quatro tentativas de leitura por olho
   antes de alguém abrir o fonte.
2. **A leitura por sysfs de player LED é cache, não retrato.** O
   `brightness_get` devolve uma variável em RAM do kernel, sem ida ao aparelho.
   A **escrita** sai no report; o que não existe é releitura. Medido com o
   daemon parado E confirmado no código. Qualquer diagnóstico que confie no
   `cat` daquele nó mente — inclusive `scripts/doctor.sh:497`.
3. **As taxas foram medidas:** cabo 250,0 Hz exatos, por duas réguas
   independentes; rádio variável em rajadas, **nunca os 1000 Hz que o SDL
   declara**. A canônica dizia "nunca medido em transporte nenhum".
4. **O verde do `doctor` não provava nada numa máquina limpa.** Módulo DKMS
   ausente saía como `info`, e `info` não conta falha. Com os três módulos
   falhando, a conferência final saía verde. A causa raiz — o `install.sh` não
   garantir `dkms` nem os headers — foi curada hoje.
5. **A cura do espelho da Steam foi medida em jogo**, e o veredito é matizado: o
   atalho do SDL vence mesmo (a variável está em 1 até no processo do jogo),
   **mas não há espelho para ele autorizar**. O defeito é potencial, não atual.

---

## 2. O que está EM ABERTO — e é aqui que a próxima sessão começa

### 2.1 As sprints de correção, da família A

Fonte: `docs/process/sprints/2026-08-11-INDICE-duas-verdades-no-mesmo-repositorio.md`,
seção 5. **Doze sprints, cerca de 42 horas.** Elas existem porque sete
documentos novos contradizem páginas antigas — e duas verdades no mesmo
repositório é como nasce o defeito mais caro daqui.

**A regra que governa todas** (fixada por ela hoje, e já no `CLAUDE.md`):
**fato errado se substitui; decisão medida se data.** O teste que separa os
dois: *se apagar isto faria alguém repetir trabalho ou pagar custo já pago?*

Estado no fim de 11/08 (confira antes de confiar — este documento envelhece):

| sprint | assunto | estado |
|---|---|---|
| A-0 | a regra da simplificação no `CLAUDE.md` | **feita** |
| A-1, A-2, A-4 | a canônica do DualSense: P4, taxas, régua de fontes | em execução por agente |
| A-3 | o ADR-008 e a fixture que nunca existiu | em execução |
| A-5 | o nome do modo do 8BitDo (17 arquivos, e um patch que vai ao upstream) | **aberta** |
| A-6, A-7 | os externos e o `PROVADO` sem escopo | em execução |
| A-8 | as sete páginas de `docs/usage/` — **a mais cara** | em execução |
| A-9 | três nomes citados como documento e que não existem | **feita** |
| A-10 | as citações de `install.sh` reancoradas | **feita** (128 realinhadas) |
| A-11 | as 18 células que o fonte do driver responde | em execução |

**A-9 foi fechada em 11/08**, e a saída foi a segunda: nasceu
[DIVERGENCIAS-NOMEADAS.md](DIVERGENCIAS-NOMEADAS.md), onde um apelido assume não
ser sprint, e o portão `tests/unit/test_nome_citado_como_sprint_existe.py` cobra
que todo nome citado como documento exista de um dos dois jeitos. Ele foi
estreitado no caminho: pegava `FEAT-`, `BUG-`, `CHORE-` e irmãos, que são **IDs
de tarefa** e nunca foram documento — um portão que acusa demais é desligado na
primeira semana.

**A-5 continua ABERTA, e tem uma armadilha medida.** O nome errado
(`DirectInput/PS4`) aparece em 17 arquivos, mas em **dois sentidos diferentes**:
o modo do 8BitDo que se disfarça de DualShock 4 (`054c:05c4` — que no vocabulário
da 8BitDo é o modo **macOS**), e referências ao **DualShock 4 de verdade** —
`assets/dkms/hid-playstation/patch/0002-*.patch` é sobre o DS4 real, e o
cabeçalho dele vai para o upstream. **Substituição cega quebra o segundo.**
Quem for executar: separe os dois sentidos antes de trocar qualquer palavra, e
lembre que o D-input verdadeiro do 8BitDo é `B + Start`, `2dc8:6001` (medido em
11/08).

### 2.2 O caminho até a versão final

Fonte: `docs/process/2026-08-11-PRODUTO-EM-MAQUINA-NOVA-o-plano-de-unificacao-para-a-versao-final.md`.

**Nove dias e meio de bancada, ou dois e meio no caminho mínimo.** A ordem é por
dependência, não por importância, e a ETAPA 1 é pré-requisito de tudo: enquanto
o `doctor` sair verde com curas ausentes, nenhum critério de aceite significa
alguma coisa.

**Versão recomendada: `0.9.4`, não `1.0.0`** — pela doutrina da própria casa,
`ENTREGUE EM CÓDIGO` não é `VALIDADO POR ELA`. O `1.0.0` é o número que se põe
**depois** de o PC novo passar.

### 2.3 O que só o aparelho responde

- **A captura de Bluetooth** (`tests/fixtures/hid_capture_bt.bin`) continua
  devendo desde 31/07. O gravador foi consertado hoje e está provado
  (`scripts/record_hid_capture.py`), mas o modo guiado precisa das mãos dela.
- **Os três módulos DKMS nunca foram construídos contra outro kernel** que não o
  `7.0.11-76070011-generic`. É o furo com maior chance de decidir a instalação
  numa máquina nova.
- **Ninguém rodou o produto com Secure Boot ligado.** Com a chave MOK não
  enrolada, o kernel recusa o `.ko` e **não volta ao in-tree** — a máquina fica
  pior do que sem a cura.
- **Os `.deb` do backport do BlueZ não existem.** A receita passou a viver na
  árvore hoje (`docs/process/estudos/2026-07-19-*`), mas gerar os pacotes
  continua sendo trabalho. É o único `FAIL` que um PC novo levaria no caminho
  `native`.

---

## 3. O que é DELA, e não se decide sem ela

- **A procedência da arte dos SVG.** Ela respondeu que não lembra a origem e que
  os desenhos foram editados aqui. Fica registrado como **risco aberto de
  licença**, não como item fechado. Uma saída, sem pressa: redesenhar os três do
  zero a partir dos aparelhos dela.
- **O `1.0.0`** — a decisão de quando o produto está pronto é dela, e o critério
  é ver funcionando num PC novo.
- **As perguntas abertas nos índices anteriores** (07/08 e 08/08) continuam
  válidas; nenhuma foi respondida hoje.

E há uma coisa fora do código que continua de pé: **a senha dela está em cinco
commits públicos desde 22/05**. Registrado em memória; só ela pode trocar.

---

## 4. Como não repetir o que já custou caro hoje

Cinco armadilhas pagas nesta sessão. Elas valem mais que o resto deste
documento, porque são o tipo de coisa que se repete.

1. **Ler o fonte antes de medir por olho.** Quatro tentativas de ler o padrão de
   LED por foto falharam, e o fonte do driver respondeu em cinco minutos. A
   ordem certa é: fonte -> instrumento -> olho dela. O olho dela é aceite, não
   descoberta.
2. **Antes de perguntar "de que lado", prove que responde.** O teste de controle
   (tudo apagado contra tudo aceso) devia ter vindo primeiro, e teria poupado
   três rodadas.
3. **Geometria em SVG se confere na imagem, não na aritmética.** Uma caixa
   calculada por varredura de `path` conta pontos de controle de curva como
   extremidades, e as peças nasceram no lugar errado. Renderizar e olhar
   corrigiu em um passo.
4. **Valor de domínio nunca leva acento.** Uma acentuação em massa no
   `mapa-controles.csv` reescreveu `nao-tem` e `inferido-do-codigo`, e o censo
   saltou de 15 para 368 reprovações. Prosa leva acento; chave, não. Está
   documentado em `scripts/validar-acentuacao.py`.
5. **Editar um arquivo invalida as citações de linha dele em todo o
   repositório.** O `install.sh` cresceu 119 linhas hoje e **128 citações** em 30
   documentos ficaram deslocadas. Se for mexer num arquivo muito citado,
   realinhe depois — por diff, não à mão.

---

## 5. Se você só tem cinco minutos

Rode isto, nesta ordem, e você sabe onde está:

```bash
git log --oneline -15                      # o que entrou hoje
python3 scripts/check_paridade_transporte.py   # a dívida do mapa, em número
bash scripts/doctor.sh | tail -20          # o que a máquina dela diz de si
```

E leia, se for tocar em protocolo, a seção 3 do `CLAUDE.md` — as quatro
referências de driver. Elas foram escritas para você não reaprender o que já foi
lido no C.
