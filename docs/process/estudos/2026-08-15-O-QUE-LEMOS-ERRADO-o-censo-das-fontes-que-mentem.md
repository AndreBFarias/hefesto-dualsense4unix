# O que lemos errado — o censo das fontes que mentem

- **Escrito em:** 15/08/2026, à noite, respondendo à pergunta dela: *"o que mais
  podemos estar usando ferramentas antigas ou lendo informações incorretas?"*
- **Estado:** **CENSO. Nenhuma linha de código tocada, nenhum controle tocado,
  nenhum serviço reiniciado.** Leitura do repositório mais leitura do journal do
  sistema (só leitura) e comparação dos scripts instalados contra a árvore
- **O que este documento é:** o **censo de uma classe de defeito** — *fonte que
  pode mentir, lida sem checagem de que ainda vale*. Cada achado traz onde,
  o que lê, quando mente, o que custa acreditar, e o que custa curar
- **O que este documento NÃO é:** não é lista de bugs, não propõe patch, e não
  fecha nada. A ordem é por **consequência**, não por elegância
- **Aviso de simultaneidade:** outra frente **curou o A-1 e o A-3 enquanto este
  censo era escrito**. Os dois ficaram no texto, com a cura registrada, porque o
  molde é o que ensina a procurar a classe. O que mudou de verdade está na
  seção 4

> **Grau de cada afirmação**, na convenção da casa: **MEDIDO** = há linha de
> journal, arquivo lido, comando rodado nesta sessão; **RECONSTRUÍDO** =
> derivado de `git log`, datas e leitura de código; **SEM PROVA** = está dito e
> ninguém verificou.
>
> **Endereços de rádio:** os que aparecem vêm do journal já mascarados pelas
> fixtures de teste (`AA:BB:CC:00:00:0X`). Nenhum endereço real dela está aqui.

---

## 0. A régua deste censo

O molde é o defeito de hoje, e vale a pena escrevê-lo como **classe**, porque é
ela que se procura, não o script:

> Um programa lê uma fonte. A fonte pode estar **certa**, **velha** ou
> **injetada**. O programa não distingue os três casos, e **age** — ou pior,
> **escreve um relato** que outra pessoa vai ler depois como se fosse fato.

O custo grande não é o programa errar. É o **relato falso sobrevivendo ao
programa** e sendo lido por um humano ou por um agente horas depois. Foi isso
que custou vinte minutos hoje, e é por isso que a ordem abaixo é por
consequência sobre o diagnóstico, não por severidade de código.

Três perguntas separam um achado grave de um irrelevante:

1. O relato falso **sai do processo** e fica gravado em algum lugar que alguém
   lê depois? (journal, arquivo de estado, log)
2. Quem lê depois consegue **distinguir** o relato falso do verdadeiro?
3. O relato falso descreve a **máquina dela** ou só o teste?

Quando as três respostas são *sim / não / máquina dela*, o achado vai para o
topo. É exatamente o perfil do caso de hoje.

---

## 1. Os achados, por consequência

### A-1 — a suíte escrevia no journal do sistema relatos de defeito que não houve

**MEDIDO — e CURADO por outra frente enquanto este censo era escrito.** Fica
registrado assim mesmo: o **molde** é o que orienta a busca pela classe, e a
lacuna de instrumento que deixou o defeito passar continua aberta (seção 4).

| | |
|---|---|
| **Onde estava** | `scripts/bt_bonds_autorestore.sh`, a função `log` |
| **Quem disparava** | `tests/unit/test_bonds_que_sobrevivem_01_o_gatilho_da_volta.py:279-280` |
| **O que lê** | `$SERVICE_RESULT`, entregue pelo systemd ao `ExecStopPost` |
| **Quando mente** | sempre que a variável for **injetada** em vez de vir do systemd |

O mecanismo era este:

```bash
log() {
    [[ "${QUIET}" -eq 1 ]] || printf '%s\n' "$*"
    logger -t hefesto-bt-autorestore "$*" 2>/dev/null || true
}
```

O `logger` escrevia no **journal do sistema**, sem condição, sem marcador de
teste, e o `--quiet` **não o desligava** — silenciava só o stdout. O teste roda
o script de verdade com a variável injetada:

```python
# tests/unit/test_bonds_que_sobrevivem_01_o_gatilho_da_volta.py:279
@pytest.mark.parametrize(
    "resultado", ["core-dump", "signal", "watchdog", "timeout", "oom-kill"]
)
```

Cada caso produz, no journal dela, esta linha:

```
ago 15 18:29:45 MeowSystem hefesto-bt-autorestore[1088241]:
    bluetooth.service morreu (SERVICE_RESULT=oom-kill) — conferindo bonds
```

**A contagem bate exatamente com o que ela viu.** Oito ocorrências de
`oom-kill`, 18:29:45 → 21:38:07 (a frente que curou contou **36** linhas do
gênero no dia inteiro, somando os outros valores parametrizados). E o
`systemctl` diz `Result=success`, `NRestarts=2`, ativo desde 14:14:32 — porque o
`bluetoothd` de fato **nunca morreu**.

**Consequência.** Um relato de morte de serviço, com carimbo de hora, no journal
do sistema, **indistinguível de um evento real**. Custou vinte minutos hoje;
custaria mais numa madrugada em que o Bluetooth estivesse realmente ruim, porque
o ruído está exatamente no canal onde se procura o sinal.

**Por que ninguém pegou.** O canário de sistema de arquivos (`CANARIO-FS-01`,
`tests/conftest.py:371`) vigia **quatro árvores dentro do `$HOME`**. O journal
não é uma delas. A suíte tem instrumento para "escrevi no disco dela?" e
**nenhum** para "escrevi no journal dela?" — e essa lacuna sobreviveu à cura.

**A cura que saiu (DIÁRIO-QUE-NAO-MENTE-01), enquanto este censo era escrito.**
É um **destino**, não um interruptor — e a distinção é o que a torna boa:

```bash
LOG_DEST="${HEFESTO_BT_LOG_DEST:-}"
_registrar() {
    case "${LOG_DEST}" in
        "")   logger -t "${LOG_TAG}" "$*" 2>/dev/null || true ;;   # produção
        none) : ;;
        *)    printf '%s %s: %s\n' "$(date -Is)" "${LOG_TAG}" "$*" >>"${LOG_DEST}" ;;
    esac
}
```

Desviar em vez de emudecer **preserva a asserção**: o teste continua podendo
conferir o que foi dito. Emudecer teria jogado fora a capacidade de testar o log
junto com o ruído. A cura tem mordida própria
(`test_bonds_que_sobrevivem_01_o_gatilho_da_volta.py:627`).

Eu ia propor emudecer com base no `${DST}` já desviado. A solução que saiu é
melhor, e fica aqui como **modelo** para os casos que ainda restarem desta
classe.

---

### A-2 — a suíte cria teclados virtuais REAIS na sessão viva dela

**MEDIDO, e é o achado que eu não esperava encontrar.**

Este censo começou pelo journal por causa do A-1 e esbarrou nisto. Entre 18h e
22h de hoje, **119** dispositivos deste nome foram registrados no kernel:

```
ago 15 18:30:25 MeowSystem kernel: input: Hefesto - Dualsense4Unix Virtual Keyboard
                                   as /devices/virtual/input/input458
```

Não são um por hora: são **rajadas** — oito em `18:30:30`, sete em `18:33:51`,
sete em `18:45:10`. As rajadas caem dentro da janela da suíte.

E o `input-remapper` **se prende a cada um deles**:

```
ago 15 18:30:30 MeowSystem input-remapper-service[1105]:
    Request to autoload for "Hefesto - Dualsense4Unix Virtual Keyboard"
```

O nome sai de `src/hefesto_dualsense4unix/integrations/uinput_keyboard.py:43`.

**A cadeia, com o que é medido e o que é inferido.** MEDIDO: a suíte mexe em
`/dev/input`; o daemon **vivo** dela (pid 615228) reage — `backend_hotplug_reconcile
trigger=input_dir_change` aparece **39 vezes** na janela — e rematerializa o
`launch_env`:

```
ago 15 19:27:50 MeowSystem hefesto-dualsense4unix[615228]:
    launch_env_materializado arquivos=9 backends=['uhid','uhid','uhid','uhid']
    emulacao=True mascara=dualsense native=False
```

Os arquivos no disco confirmam: `~/.local/state/hefesto-dualsense4unix/launch_env/*.env`
com mtime `ago 15 19:27`, dentro da janela. E `emulacao=True` diz que a
**emulação de teclado está ligada** no daemon dela.

INFERIDO, e é onde eu paro: que estes 119 teclados sejam o mecanismo do **texto
aparecendo sozinho e do foco pulando** que ela viu duas vezes. A correlação é
forte — dispositivos de teclado nascendo às dezenas na sessão dela, com o
`input-remapper` carregando mapeamento em cima de cada um — mas eu **não** achei
no journal uma linha que registre tecla emitida, e não vou afirmar o que não
medi.

**Como provar, e é barato:** `evtest` (ou `libinput debug-events`) num terminal
do workspace `OS`, rodando enquanto se executa **um só** dos arquivos de teste
que mexem em `/dev/input`. Se sair evento de tecla, está provado; se não sair, o
mecanismo é outro e esta hipótese cai. Vale mais que qualquer leitura de código.

**Observação sobre a origem, que corrige uma nota da casa.** O comentário em
`tests/conftest.py:383` fala da *"primeira rajada de teclados uinput que a suíte
cria"*. A frase é de 07/08. Eu procurei nos testes por `UInput(` e `/dev/uinput`
reais e **não achei**: `test_keyboard_emulator.py:33` injeta um módulo falso via
`sys.modules`, e os irmãos (`test_touchpad_click_no_jogo.py:36`,
`test_uinput_gamepad.py:5`, `test_virtual_pad_factory.py:22`) declaram
explicitamente que não tocam o nó real. Ou seja: **a suíte provavelmente não cria
os teclados — o daemon vivo dela cria, reagindo à suíte.** Isso muda a cura de
lugar, e por isso está escrito aqui.

**Consequência.** Duas, e a segunda é pior que a primeira. (1) Rodar a suíte
mexe na sessão dela — foi o medo dela hoje, e é um medo com base. (2) O
diagnóstico fica poluído: quem for investigar "por que apareceram 119 teclados"
vai atrás do produto, quando a causa é a suíte cutucando o daemon.

**Custo de curar.** Médio, e a decisão é dela, porque há um caminho barato e
errado e um caminho certo e caro:

- *barato e errado* — pedir que ela pare o daemon antes de rodar a suíte. É
  contorno, e a casa não aceita contorno;
- *certo* — a suíte não deve criar nós em `/dev/input` que o daemon vivo adote.
  Ou os nós de teste nascem com um marcador que o
  `backend_hotplug_reconcile` ignora, ou nascem num namespace de dispositivo
  separado. A primeira é bem mais barata e cabe no idioma que o produto já usa
  (o backend **já** sabe ignorar o próprio vpad —
  `tests/unit/test_backend_ignora_vpad_virtual.py`, e a lógica que ele testa).

Antes de qualquer cura: **medir**, como acima. Curar o mecanismo errado aqui
custaria mais que o defeito.

---

### A-3 — a suíte escreve caminhos de `tmp_path` no journal, e o resto não se distingue

**MEDIDO.** Consequência direta do A-1, mas merece linha própria porque mostra o
tamanho real da contaminação — e uma assimetria útil.

Contagem de linhas por tag no journal **de hoje**:

| tag | linhas hoje |
|---|---|
| `hefesto-dualsense` | 10339 |
| `hefesto-bt-autorestore` | 2200 |
| `hefesto-bt-health-watchdog` | 1989 |
| `hefesto-hidraw-broker` | 1669 |
| `hefesto-bt-bonds` | 534 |
| `hefesto-bt-rebind` | 421 |
| `hefesto-bt-bonds-snapshot` | 407 |

Seis scripts chamavam `logger -t` (`bt_bonds_snapshot.sh`,
`bt_bonds_autorestore.sh`, `bt_rebind_orphans.sh`, `bt_health_watchdog.sh`,
`bt_nosniff_now.sh`, `bt_active_mode.sh`) e **todos os seis têm teste que os
executa de verdade**. Conferi ao fechar este censo: **os seis receberam a cura
do A-1** — todos têm `HEFESTO_BT_LOG_DEST`/`_registrar`. O achado está fechado
no código; o que segue abaixo é o retrato do estrago que já está gravado.

A assimetria que importa: algumas linhas **se denunciam**, outras não.

```
ago 15 21:38:07 hefesto-bt-rebind[1415226]: [dry-run] faria:
    echo '0005:054C:0CE6.000F' > /tmp/pytest-of-vitoriamaria/pytest-299/
    test_dry_run_nao_escreve_nada0/drivers/playstation/bind (tentativa 1/3)
```

Esta é inofensiva para o diagnóstico: o caminho `pytest-of-vitoriamaria` grita
"teste". Mas estas outras, do mesmo lote, **não têm marcador nenhum**:

```
ago 15 21:38:07 hefesto-bt-autorestore[1414897]:
    bond de AA:BB:CC:00:00:03 restaurado do snapshot 20260815-062901
ago 15 21:38:07 hefesto-bt-autorestore[1414915]:
    QUARENTENA: AA:BB:CC:00:00:03 já voltou 1x neste boot e sumiu de novo —
    restauração SUSPENSA ...
```

Uma delas manda a humana fazer um gesto: *"bluetoothctl remove ... e parear
outra vez"*. Vindo de um teste.

**Consequência, e ela NÃO acabou com a cura.** O journal de hoje continua com
essas linhas gravadas. Quem consultar `journalctl -t hefesto-bt-autorestore`
amanhã, ou daqui a um mês, vai ler restaurações, quarentenas e conselhos que
nunca aconteceram — e nada no texto delas avisa. A cura impede novas; não apaga
as velhas, e apagar journal não é coisa que se faça de leve.

**O que sobra, então.** Não é código: é **saber a janela**. Toda linha de tag
`hefesto-bt-*` anterior à cura de 15/08/2026 é suspeita, e as janelas de suíte
de hoje (18h–22h) são inteiramente ruído. Vale a pena isso estar escrito em
algum lugar que a próxima caçada leia antes de acreditar no journal — que é,
afinal, o motivo de este documento existir.

---

### A-4 — `_detect_transport` devolve `"usb"` quando não sabe

**MEDIDO** (leitura de código; o comportamento já era conhecido da casa).

```python
# src/hefesto_dualsense4unix/core/backend_pydualsense.py:4517
@staticmethod
def _detect_transport(ds: pydualsense) -> Transport:
    con = getattr(ds, "conType", None)
    if con is None:
        return "usb"
    name = str(getattr(con, "name", con)).lower()
    return "usb" if "usb" in name else "bt"
```

*"Não sei"* e *"é cabo"* saem pela **mesma porta**. E o valor não é decorativo —
mapeei **oito** pontos de decisão que dependem dele:

| linha | o que decide |
|---|---|
| `:1985` | conta conexões BT novas (arma o gatilho da lightbar) |
| `:2069` | telemetria de transporte |
| `:2179` | o `_transport` cacheado do handle primário |
| `:2330` | `_suppress_leds` — **quem manda na lightbar** |
| `:2449` | recálculo após reconexão |
| `:2790` | política por transporte |
| `:2989` | **portão do 0x31/CRC** — sai cedo se não for `bt` |
| `:4297` | o transporte que aparece na interface e no IPC |

**Quando mente.** Quando `conType` ainda não foi preenchido pela `pydualsense` —
janela de inicialização, reconexão, ou um handle que a biblioteca não terminou
de povoar. Aí um controle **por rádio** é tratado como cabo.

**Consequência.** Nos dois pontos que mais doem: `:2989` faz a escrita da
lightbar por rádio **sair cedo sem escrever**, e `:2330` deixa de suprimir os
LEDs. O sintoma resultante é o pior catalogado pela casa — *o log diz "escrito"
e a barra não muda* — e é **exatamente a família do defeito da lightbar travada**
que outra frente está caçando hoje. Não estou afirmando que é a causa dela; estou
dizendo que é uma fonte que mente na direção certa e que sai barato eliminar.

**Custo de curar.** **Baixo, e mais barato do que parece**, porque a resposta
verdadeira já é lida em outro lugar da árvore: o bus real sai do sysfs, em
`src/hefesto_dualsense4unix/core/physical_report_reader.py:299`
(`/sys/class/hidraw/<nó>/device/uevent`), e há outros dois leitores de `uevent`
(`integrations/dualsense_bt_audio.py:344`, `app/usb_pai.py:194`). A cura é fazer
o `None` cair no sysfs em vez de chutar — reúso, não código novo.

**A mordida:** um handle com `conType = None` cujo nó de sysfs diga `bluetooth`
tem de resultar em `"bt"`. Com o chute de volta, o teste reprova.

---

### A-5 — mypy é estrito em tudo, e cego exatamente na fronteira que mente

**MEDIDO.**

```toml
# pyproject.toml:116
[tool.mypy]
strict = true

# pyproject.toml:121
[[tool.mypy.overrides]]
module = ["pydualsense", "pydualsense.*", "textual", ..., "evdev", ..., "gi", "gi.*"]
ignore_missing_imports = true
```

E a dependência não tem teto: `pydualsense>=0.7.5` (`pyproject.toml:25` e
`requirements.txt:14`). Instalada hoje: **0.7.5**.

Junte com o padrão de leitura da biblioteca, que aparece 16 vezes no backend e
duas delas com **default silencioso**:

```python
# :2460
if bool(getattr(ds.state, "micBtn", False)):
```

**Quando mente.** Se um `pydualsense` 0.8 renomear `conType`, `micBtn` ou
`battery.Level`, **nada** falha: `getattr` devolve o default, o produto degrada
em silêncio, o mypy não vê (módulo ignorado) e os testes não veem (todos usam
dublês). O botão do microfone simplesmente nunca mais é detectado.

**Consequência.** Uma classe inteira de regressão futura que passa por todos os
portões. Não está quebrado hoje — está **indefeso**.

**Custo de curar.** Baixo: um teto de versão (`pydualsense>=0.7.5,<0.8`) fecha o
buraco hoje por uma linha. O certo e um pouco mais caro é um teste de contrato
que afirme que os três atributos **existem** na versão instalada — aí a atualização
falha alto, no lugar certo, em vez de degradar calada.

---

### A-6 — `sdptool` (obsoleto) decide o conselho que o vigia dá a ela

**MEDIDO.**

```bash
# scripts/bt_health_watchdog.sh:205
if command -v sdptool >/dev/null 2>&1 \
   && ! timeout 20 sdptool browse "${MAC}" >/dev/null 2>&1; then
    log "controle ${MAC} NÃO responde SDP ... Cura: reset de hardware do
         controle (furinho atrás, ~5 s com um clipe) e ligar de novo"
```

`sdptool` é ferramenta **depreciada** do BlueZ (junto com `hcitool` e
`hciconfig`, todos ainda presentes nesta máquina — conferi). O script usa a
**falha** dela como sinal de saúde do controle.

**Quando mente.** Um `timeout 20` estourado por carga, por contenção do rádio,
ou por uma limitação da própria ferramenta obsoleta é lido como *"o stack do
controle travou"*.

**Consequência.** Mais branda que os anteriores, e é justo dizer: o caminho
**só registra conselho, não age**. Mas o conselho é forte — manda ela abrir um
clipe e resetar o hardware de um controle que pode estar são. É custo dela, em
gesto físico, por leitura de um instrumento velho.

**O crédito devido:** o resto deste arquivo é dos mais bem-raciocinados da
árvore. O comentário em `:236` documenta uma medição de 22/07 em que o watchdog
derrubou uma sessão com três controles vivos por confundir recusa legítima com
doença, e a regra foi corrigida por causa disso. O `sdptool` é o resíduo, não o
padrão.

**Custo de curar.** Baixo-médio: perguntar ao BlueZ pelo D-Bus (o script **já
usa** `busctl` e tem `_dbus_device_prop`) em vez de ao binário obsoleto. Ou, mais
barato ainda e honesto, rebaixar o texto do conselho para condicional enquanto a
fonte for o `sdptool`.

---

### A-7 — 163 citações de linha que nenhum portão consegue conferir

**MEDIDO.** Rodei o portão:

```
$ python3 scripts/validar-citacoes-de-linha.py --all
OK: 121 citação(ões) de linha conferida(s) em 11 documento(s);
    163 de fontes fora desta árvore (kernel, SDL, wine) foram ignoradas.
```

O portão é bom e está verde. Mas a razão é **57% ignorada**: as citações que
apontam para o fonte do kernel, do SDL e do Wine não podem ser verificadas
porque essas árvores não estão aqui.

**Quando mente.** Quando qualquer uma das três se mexe. `drivers/hid/hid-playstation.c`
muda de linha a cada versão do kernel; uma citação `hid-playstation.c:412` de
11/08 aponta para outra coisa depois de um `git pull` no kernel.

**Consequência.** É a categoria 4 dela — *números copiados de documentação em vez
de medidos*. Cai direto sobre as quatro referências de driver que o `CLAUDE.md`
manda ler **em terceiro lugar**, e que a casa declara vencedoras sobre a
canônica. São a fonte mais autoritativa do projeto e a menos verificável.

**Custo de curar.** Médio, e o desenho importa mais que o esforço: não adianta
verificar linha, porque a árvore não está aqui. O que funciona é **gravar a
versão** junto da citação (`hid-playstation.c:412 @ v6.11`) e fazer o portão
exigir o carimbo. Aí a citação para de se apresentar como atemporal, que é a
mentira de verdade.

---

### A-8 — a lista de portões do `CLAUDE.md` é menor que a do CI

**MEDIDO.**

Todos os sete portões listados no bloco *"Antes de fechar qualquer leva"*
existem. Mas dois que **existem e rodam no CI** não estão na lista:

- `scripts/validar-citacoes-de-linha.py`
- `scripts/validar-palavra-de-tela.py`

(`scripts/check_paridade_transporte.py` também não está no bloco, embora esteja
descrito antes no mesmo arquivo.)

**Consequência.** Quem seguir o `CLAUDE.md` à risca fecha a leva achando que
passou por tudo e leva reprovação no CI por portão que nunca rodou local. Baixa
severidade, alta frequência — e num arquivo que **todo agente lê primeiro**.

**Custo de curar.** Trivial: três linhas no bloco.

**Do mesmo arquivo, e da mesma família:** `CLAUDE.md:94` diz `# 6645 verdes em
01/08`. Contei **8356** funções `def test_` na árvore hoje (contagem por `grep`,
antes de parametrização — não é o número de testes coletados, e não deve ser
usado como se fosse). O número do comentário está velho em duas semanas. Pela
régra dela — *apagar isto faria alguém repetir trabalho?* — não faria: é só um
número desatualizado, e **se substitui**, não se preserva com nota.

---

## 2. O que eu conferi e está SÃO

Um censo que só lista defeito ensina a desconfiar de tudo, e isso é tão caro
quanto confiar demais. Estes eu fui conferir esperando achar problema e **não
achei**:

**A renomeação D-13 está completa.** As colunas velhas eram `cabo_confianca`/
`radio_confianca` e `cabo_grau`/`radio_grau` (confirmei no `git show` do commit
`fe6f74c`). Grep por todas as quatro em `scripts/`, `src/` e `tests/`: **zero
ocorrências**. Nenhum instrumento ficou lendo coluna morta. Quatro documentos em
`docs/process/` ainda citam os nomes velhos, mas são registros históricos
descrevendo a própria renomeação — é o lugar certo para eles.

**Os scripts instalados estavam idênticos aos da árvore — e deixaram de estar
durante este censo.** Comparei os sete de `/usr/local/lib/hefesto-dualsense4unix/`
com `scripts/` no começo: **todos iguais** (instalados hoje 14:12). Refiz a
comparação no fim, depois da cura do A-1: **seis dos sete divergem** — só
`bt_bonds_restore.sh` continua igual.

Isso não é crítica à cura: é o funcionamento normal de `install.sh`, que ainda
não rodou. Mas é a **armadilha da casa armando-se em tempo real** — *"o daemon
vivo é mais velho que o código"*. Neste momento, a árvore não escreve mais
mentira no journal e **a máquina dela ainda escreve**. Enquanto o install não
correr, o A-1 está curado no repositório e **aberto na máquina**.

Registro também o método, porque foi ele que pegou isto: `cmp -s` entre
instalado e árvore, sete comandos, dois segundos. Vale rodar no **começo e no
fim** de qualquer sessão — eu só peguei porque repeti.

**Nenhum binário citado está ausente** desta máquina: `bluetoothctl`, `btmgmt`,
`hcitool`, `hciconfig`, `sdptool`, `rfkill`, `udevadm`, `systemctl`, `pactl`,
`wpctl`, `dkms`. E as chamadas aos obsoletos vêm guardadas por `command -v`.
O problema do A-6 é *confiar no que a ferramenta velha responde*, não a ausência
dela.

**O portão de paridade está verde, e a régua dele é séria.** Rodei: 301 linhas,
47 afirmações fortes, **0 sem teste que morda**; 28 graus fortes, **0 sem ensaio
no caderno**. Existe até um portão `prova-vencida` que compara `provado_em +
validade_dias` contra hoje (`check_paridade_transporte.py:847`) — ou seja, o
mapa **tem** defesa contra envelhecer, que é justamente o que a categoria 2 dela
teme. As 14 assimetrias não declaradas são avisos, e o texto do aviso explica
que essa é a forma da regressão que o mapa existe para pegar.

**`controllers.json` é lido com desconfiança exemplar.** Em
`daemon/subsystems/identity.py:1125`: portão por `CONTROLLERS_SCHEMA_VERSION`
(arquivo de schema velho é descartado, `:1151`), `boot_id` **só** para
diagnóstico e deliberadamente não renumera (`:1170`), teto de slots, recusa de
duplicata, `try/except` que jamais derruba o boot. É o modelo de como ler cache
que pode envelhecer, e serve de referência para curar os outros.

**O canário de sistema de arquivos está ligado** (`HEFESTO_SEM_CANARIO_FS`
vazio nesta sessão) e a distinção dele entre lista que reprova e lista que só
avisa é bem pensada — o comentário em `conftest.py:378-391` explica que o delta
em `.local/state` é **a daemon dela reagindo à suíte**, não a suíte escrevendo.
Foi essa nota que me pôs na pista do A-2. O limite dele é de escopo, não de
qualidade: ele vigia `$HOME`, e os A-1/A-3 aconteciam fora do `$HOME`.

---

## 3. O que eu NÃO varri, e por quê

O censo tem limite, e declará-lo é o que o torna utilizável.

**Não varri as docstrings contra o comportamento.** A categoria 5 dela inclui
*"docstring que descreve comportamento que mudou"*. São 175 arquivos em `src/`,
e a verificação não tem atalho: exige ler a docstring e o código lado a lado.
Amostrei o que passou pelo caminho dos outros achados e não vi divergência, mas
**amostra não é censo** e não vou apresentá-la como tal. Se virar frente
própria, o corte com melhor retorno é começar pelos módulos que mudaram nos
últimos trinta dias (`git log --since`), porque é lá que a docstring fica para
trás.

**Não rodei a suíte.** Por instrução, e a instrução estava certa: a máquina
apertou hoje. Consequência direta — os achados A-1, A-2 e A-3 estão provados
pelo **journal de execuções que já tinham acontecido** (18h–22h), não por
execução minha. Isso não os enfraquece (a evidência é do sistema, não minha),
mas significa que **não medi** o que uma execução isolada produz, que é o
experimento que fecharia o A-2.

**Não varri os 1087 arquivos `.sh`.** Fui pelos seis que chamam `logger` e pelos
que aparecem nos portões e no `install.sh`. A maioria dos 1087 está em `venv/` e
`.venv/` (terceiros), mas não conferi um a um, e é possível que exista script
nosso com a mesma classe de defeito fora da minha varredura.

**Não conferi o `install.sh` inteiro** (1711+ linhas). Olhei os caminhos fixos
de `/usr/local/lib/` e a paridade com o `uninstall.sh` pela via dos testes que
já existem. A regra da casa — *toda cura entra no install, sem flag* — mereceria
uma passagem própria, e ela não coube aqui.

**Não medi as variáveis de ambiente em execução.** Levantei as ~30 lidas em
`src/` e li os defaults no código (`window_detect.py:191`, `keyboard.py:101`,
`autoswitch.py:37`, `tray.py:90`, `daemon/main.py:18-21`). Não construí a
matriz *"o que acontece com cada uma ausente"*, que é a pergunta 1 dela por
inteiro. Dos defaults que li, o único que me pareceu perigoso é o do A-4 — os
de sessão gráfica degradam para "sem detecção de janela", que é seguro.

**O A-2 está pela metade de propósito.** A correlação está medida; o mecanismo
não. Escrevi o experimento que o resolve (`evtest` durante um arquivo de teste
só) em vez de escrever uma conclusão que eu não posso sustentar.

---

## 4. O que fazer, na ordem

O A-1 e o A-3 **já foram curados** por outra frente durante este censo, e a cura
que saiu é melhor que a que eu ia propor. O que sobra é isto, em ordem:

**1. Rodar o `install.sh`.** Enquanto ele não correr, os seis scripts curados
estão curados **só no repositório**: a máquina dela ainda tem a versão que
escreve no journal (seção 2). É o passo mais barato e o de maior efeito
imediato.

**2. Dar ao journal o canário que o disco já tem.** É a lacuna que deixou o
defeito de hoje passar, e ela **sobreviveu à cura**: o `CANARIO-FS-01` fotografa
quatro árvores do `$HOME` antes e depois da suíte, e nada faz o equivalente com
`journalctl`. O desenho tem precedente pronto — foto no `pytest_sessionfinish`,
lista que reprova e lista que só avisa — e o custo é uma consulta
`journalctl --since <início da sessão> -t hefesto-*`. Sem isto, o próximo script
que aprender a falar com o `logger` reabre a classe inteira, e ninguém vai
saber.

**3. A-2 — medir antes de curar.** É o que ela viu, e é o único achado que mexe
na sessão dela em tempo real. O experimento está descrito: `evtest` durante um
arquivo de teste só. Curar sem medir aqui sairia caro.

**4. A-4** (reúso do leitor de sysfs que já existe, e cai perto da lightbar
travada), **5. A-5** (uma linha de teto de versão), **6. A-8** (três linhas no
`CLAUDE.md`), e o resto quando der.

E fica registrado o que este censo mostrou por acidente, que talvez valha mais
que a lista: **o journal do sistema não foi, hoje, um canal confiável sobre esta
máquina**, e nenhum instrumento da casa vigiava esse canal. O canário existia
para o disco dela. O journal ficou sem canário — e foi exatamente por ali que a
mentira de hoje entrou.

Duas lições de método, que me pareceram valer mais que os achados:

- **Comparar instalado contra árvore no começo E no fim.** No começo deu tudo
  igual; no fim, seis divergentes. A resposta certa tinha prazo de validade de
  duas horas.
- **A pergunta dela — "o que MAIS lemos errado?" — é melhor que a busca por
  bugs.** Nenhum dos achados acima é um teste vermelho. Todos passam por todos
  os portões. Eles só aparecem quando se pergunta *de onde veio esse número, e
  ele ainda vale?*
