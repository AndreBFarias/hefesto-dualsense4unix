# O que a Steam come em silêncio — o censo dos campos de uma linha só

- **Escrito em:** 16/08/2026, entre 05h e 06h30, com ela dormindo. Steam
  **fechada**, daemon **parado**, nenhum controle tocado. Todos os arquivos da
  Steam foram **lidos**; nenhum foi escrito.
- **O pedido que o gerou:** *"eu preciso que seja uma cura de fato universal"* —
  sobre o `LaunchOptions` que a Steam apagou sem avisar. Não é sobre o
  `LaunchOptions`. É sobre **a classe**.
- **O que ele NÃO é:** não refaz a `SENTINELA-WRAPPER-01`, e não escreve cura
  nenhuma. Cada buraco sai daqui com desenho e preço; **construir é decisão
  dela**.

> **Este documento é o SEGUNDO de um par, e o par é deliberado.** O irmão,
> [`2026-08-16-A-LINHA-QUE-A-STEAM-COME`](2026-08-16-A-LINHA-QUE-A-STEAM-COME-o-censo-dos-campos-e-a-arvore-errada.md),
> foi escrito na mesma madrugada por outra frente, e mediu as **três árvores
> `apps`** do `localconfig.vdf` e a fusão que cega o censo. **Não repito as
> tabelas dele.** Este aqui é o que sobrou depois de conferir aquele: uma
> correção de endereço, **dois campos que nenhum dos dois tinha visto** (e que
> não moram no `localconfig.vdf`), **um arquivo inteiro da Steam que ninguém no
> produto vigia**, e **três portões cegos** além do que já foi curado.

> **Grau de cada afirmação**, na convenção da casa: **MEDIDO** = arquivo lido ou
> comando rodado nesta sessão, com o número transcrito; **RECONSTRUÍDO** =
> derivado de nome, data e leitura de código; **SEM PROVA** = está dito, e
> ninguém verificou.
>
> Nenhum MAC de controle físico dela aparece aqui. Onde o nome de um arquivo da
> Steam **é** um MAC real, o arquivo é descrito, não transcrito. Os appids
> aparecem porque são públicos e já estão em páginas versionadas desta casa.

---

## 1. A classe, nomeada

O `LaunchOptions` não é um defeito. É o **exemplar** de uma classe, e a classe
tem três propriedades que precisam estar juntas para doer:

> **1. O campo é de UMA LINHA.** Não há como o produto e a Steam coexistirem
> nele: escrever é substituir. Não existe merge, não existe "a nossa parte".
>
> **2. O dono do arquivo é o OUTRO.** A Steam reescreve quando quer — ao sair,
> ao atualizar, quando a pessoa mexe num painel — e **não avisa ninguém**.
>
> **3. O produto escreveu e foi embora.** Ele nunca relê. E, pior, o instrumento
> que deveria reler **lê a própria escrita de volta**.

Quando as três valem, o defeito tem uma assinatura constante, e é ela que custa
as horas:

> **Tudo continua parecendo certo.** O controle está vivo, o perfil está aceso,
> o daemon responde, o `doctor.sh` dá verde. **Só o jogo não enxerga.** E, como
> funciona no cabo e quebra no rádio, a suspeita vai para o rádio — que é o
> subsistema mais caro de investigar desta casa inteira.

**A quarta propriedade, que só apareceu ao medir, e que é a pior:** quando o
campo é de uma linha e o dono é o outro, o produto tende a **acumular** identidade
lá dentro sem nunca poder tirá-la. Ver a seção 3.

---

## 2. Os três portões que contam em vez de nomear

Esta é a seção que ela pediu primeiro, e é a que vem primeiro **porque produz
diagnóstico errado sobre a própria máquina dela** — o que faz humano e agente
perderem hora atrás de defeito que não existe, ou não acharem o que existe.

A forma é sempre a mesma, herdada do `WRAPPER-EM-TODOS-01`:

> O portão pergunta **"quantos?"**. A pessoa precisa de **"qual?"**. E, como
> `N > 0` é quase sempre verdade, o portão passa verde exatamente no caso
> parcial — que é o caso real, porque o total nunca quebra de uma vez.

### 2.1 O contador do wrapper ainda está lá, e agora diz **76**

**MEDIDO, às 05h35 de hoje**, no `localconfig.vdf` dela (mtime `16/08 05:31`):

| o que se conta | número |
|---|---|
| jogos na árvore viva (`UserLocalConfigStore/Software/Valve/Steam/apps`) com `LaunchOptions` | **63** |
| desses, **com** o wrapper | 62 |
| desses, **sem** o wrapper | **1 — PRAGMATA (appid 3357650)** |
| ocorrências do caminho do wrapper **no arquivo inteiro** | **76** |

E o portão, em `scripts/doctor.sh:1508-1519` (`check_launch_wrapper`), faz
exatamente isto:

```sh
n_wrapper=$((n_wrapper + $(grep -o '.local/share/hefesto-dualsense4unix/bin/hefesto-launch' "${vdf}" | wc -l)))
...
if [[ "${n_wrapper}" -gt 0 ]]; then
    pass "${n_wrapper} jogo(s) com o wrapper hefesto-launch aplicado nas LaunchOptions"
```

Ou seja: **neste instante, com o Pragmata quebrado, este portão imprime em verde
"76 jogo(s) com o wrapper hefesto-launch aplicado"** — e há 63 jogos.

Isso merece ser dito devagar, porque é o achado mais barato de entender e o mais
difícil de desver:

> **O contador reporta mais jogos com o wrapper do que existem jogos.** Ele
> conta as 14 linhas que **nós mesmos** escrevemos nas duas árvores que a Steam
> nunca lê (o mecanismo está medido no documento irmão, §3.2). O número não é
> só cego — ele é **aritmeticamente impossível**, e ninguém notou por 24 dias,
> porque *76* é tão plausível quanto *60*.

**O que a cura de hoje fez e o que não fez.** A `SENTINELA-WRAPPER-01` **somou**
duas réguas honestas — `check_arvore_canonica_do_wrapper` (`doctor.sh:1697+`,
ancorada no caminho inteiro, nomeia o Pragmata) e `check_sentinela_wrapper`. Ela
**não removeu** o contador. Hoje, na tela dela, o `[ OK ] 76 jogo(s)…` sai
**acima** do `[FAIL] … PRAGMATA`. Duas linhas vizinhas, uma verde e falsa, uma
vermelha e verdadeira.

> **Custo em minutos de confusão: alto e recorrente.** Não é o custo de errar o
> diagnóstico uma vez — é o de a tela ensinar, toda vez, que verde-e-vermelho
> juntos são normais aqui. Isso é como um portão morre de verdade: não
> desligado, mas **desacreditado**.

**Desenho da cura (não construída):** a linha 1516 não precisa de régua nova —
a régua honesta já roda trinta linhas abaixo. Ou o contador some, ou vira
`info` sem verde. **Preço de escolher errado: zero.** É a cura mais barata deste
documento.

### 2.2 O broker **tem a lista na mão** e joga fora para ficar com o tamanho

Este é o mais grave dos três, porque o sintoma dele é o defeito histórico mais
caro desta casa: **o controle dobrado no jogo**.

**MEDIDO (leitura de código).** Em `scripts/doctor.sh:3088-3090`, o doctor
pergunta o status ao broker e recebe a **lista** dos nós escondidos:

```python
hidden = resp.get("hidden") or []
print(f"hidden_count={len(hidden)}")
```

A lista morre ali. Vinte linhas de shell depois, em `doctor.sh:3226-3234`:

```sh
if [[ "${hidden_count}" -gt 0 ]]; then
    ...
    pass "broker escondendo ${hidden_count} nó(s) físico(s) — o jogo só vê o vpad"
```

**O que isso deixa passar.** Com dois DualSense na mesa e o broker escondendo
**um**, `hidden_count=1`, `1 > 0`, e o portão afirma, com todas as letras, *"o
jogo só vê o vpad"*. O jogo do P2 vê **dois** controles. O portão nunca compara
`hidden` com o conjunto de DualSense físicos presentes — e nunca diz qual sobrou
de fora.

> **Custo em minutos de confusão: o mais alto do documento.** Controle dobrado
> manda a investigação para o `IGNORE_DEVICES`, para o Steam Input, para o
> espelho Xbox do Steam (ver a memória *"o terceiro controle era o espelho do
> Steam"*) — três frentes caras — enquanto a resposta está numa lista que o
> doctor teve nas mãos e converteu em inteiro.

**Desenho da cura (não construída):** trocar `len(hidden)` por
`",".join(hidden)`, e transformar o veredito de `> 0` em **comparação com o
censo de físicos** — o produto já sabe enumerá-los
(`broker/hidraw_broker.py:111`, `validate_physical_node`). O `pass` só é honesto
quando `escondidos == físicos`; qualquer físico fora da lista é o nome que a
pessoa precisa ler. **A mordida é óbvia:** dois físicos na fixture, um escondido
— o portão de hoje passa, o curado nomeia o que sobrou.

### 2.3 Os bonds: `> 0` responde a pergunta de 22/07, não a de hoje

**MEDIDO (leitura de código)**, `scripts/doctor.sh:2809-2823`
(`check_bt_bonds_persistidos`):

```sh
n_info="$(sudo -n find /var/lib/bluetooth -mindepth 3 -maxdepth 3 -type f -name info | wc -l)"
n_cache="$(sudo -n find /var/lib/bluetooth -mindepth 3 -maxdepth 3 -type f -path '*/cache/*' | wc -l)"
if [[ "${n_info}" -gt 0 ]]; then
    pass "bonds BT persistidos em disco: ${n_info} (cache com ${n_cache} devices vistos)"
```

O portão nasceu (ONDA-R2, 22/07) para pegar uma assinatura **total**: cache
populado com **ZERO** bonds. Para essa pergunta, `> 0` é a régua certa.

Mas o estado que ela vive é **parcial**. Com quatro controles na mesa e o bond
de **um** evaporado, dá `n_info=3`, `3 > 0`, e o portão imprime em verde
*"bonds BT persistidos em disco: 3 (cache com 7 devices vistos)"* — **com a
prova do defeito impressa dentro da própria frase de aprovação**, como
tranquilizante.

> **Custo em minutos de confusão: alto, e com um agravante.** O sintoma — *"um
> controle específico parou de reconectar sozinho depois do boot"* — é
> indistinguível de dezenas de defeitos de rádio já catalogados aqui. É
> exatamente a trilha em que esta casa mais gastou tempo. E o portão que
> resolveria em um segundo diz que está tudo bem.

**Desenho da cura (não construída):** nomear os MACs em `cache/` **sem** `info/`
correspondente — a diferença de conjuntos, não a de contagens. **Ressalva de
anonimato:** o resultado sai na tela dela, nunca em arquivo versionado; se algum
dia for para arquivo, vale a máscara da casa (octetos 4 e 5 zerados).

### 2.4 O meio-caso, dito para não inflar a lista

`scripts/check_paridade_transporte.py:823-838` nomeia **cinco** linhas do CSV
ausentes do `specs.html` e resume o resto como `(e mais N)`.

**Isto não é a mesma doença**, e registro a diferença de propósito: o portão
**reprova** — nunca produz verde falso. O que ele esconde é o **tamanho** do
estrago, não a existência dele. Fica escrito porque a próxima pessoa que varrer
esta classe vai encontrá-lo e precisar da distinção pronta: *contar em vez de
nomear só é fatal quando decide um veredito.*

### 2.5 O que passou na varredura, e por que isso importa

**MEDIDO.** Varri os 61 `check_*` do `doctor.sh`, os quatro portões de shell da
lista de fechamento (`check_anonymity.sh`, `check_packaging_parity.sh`,
`check_test_data.sh`, `check_version_consistency.py`) e os três `validar-*.py`.
**A maioria esmagadora nomeia** — e alguns nomeiam com esmero:

- `check_udev` conta 15 regras **e imprime as que faltam** (`doctor.sh:200`);
- `check_usb_power_devices` / `check_usb_power_hosts` imprimem device e host por
  nome (`doctor.sh:2168`, `doctor.sh:2192`);
- `check_packaging_parity.sh` emite um `[FAIL]` **por arquivo**, com o nome.

E o molde de ouro é o `--status` do `disable_steam_input.sh`: ele **imprime
contagens** mas o veredito é do `needs_real_fix`, que aplica a transformação num
temporário e **compara** — pergunta *"a edição mudaria alguma coisa?"*, não
*"quantas linhas casam?"*.

> **Três em setenta e poucos.** Isso muda a recomendação: a casa **não** precisa
> de uma varredura periódica atrás de contadores. Precisa da regra escrita na
> hora de criar portão novo, e dos três consertos nomeados acima.

---

## 3. Os dois campos que ninguém tinha visto — e não moram no `localconfig.vdf`

O censo irmão olhou o `localconfig.vdf` a fundo. Olhei o **diretório inteiro** da
Steam, e é lá que estão as duas surpresas.

### 3.1 `SDL_GamepadBind` — uma linha, 4.134 bytes, e a nossa identidade dentro dela

**MEDIDO, agora**, em `~/.steam/steam/config/config.vdf`, linha 1656: uma única
chave `"SDL_GamepadBind"` cujo valor é uma string de **4.134 bytes** com
**14 mapeamentos SDL**, um por GUID. É o campo de uma linha mais puro que
encontrei — e é onde a Steam guarda *como um controle deve ser lido*.

Três das 14 entradas param o coração:

| GUID | nome gravado | de onde veio |
|---|---|---|
| `030000004c050000f20d000003000000` | Sony Interactive Entertainment DualSense Edge Wireless Controller | **bate exatamente com o NOSSO vpad** |
| `03000000341200007856000000010000` | **Hefesto Virtual DualSense P2** | nome do produto; vid `0x1234` / pid `0x5678` |
| `03000000010000000100000001000000` | **hefesto-refute-test** | `0001:0001:0001` — o default do `evdev.UInput` |

O primeiro não é coincidência. O GUID do SDL é
`bustype|vendor|product|version`, e o vpad "dualsense" é montado com exatamente
esses quatro valores em `integrations/uinput_gamepad.py`:

```python
BUS_USB = 0x03            # linha 85
DUALSENSE_VENDOR = 0x054C # linha 63
DUALSENSE_EDGE_PRODUCT = 0x0DF2  # linha 77
DEVICE_VERSION = 0x3      # linha 90
```

→ `03000000` `4c050000` `f20d0000` `03000000`. **É o nosso.**

Os outros dois são **restos de bancada**. "Hefesto Virtual DualSense P2" é o nome
que o vpad publica no evdev (`app/actions/emulation_actions.py:97`);
`hefesto-refute-test` é um artefato de ensaio, com os ids default da biblioteca.
Alguém rodou a bancada com a Steam aberta, e a Steam **memorizou para sempre**.

**Por que isto é grave, e não curiosidade.** Há um comentário no nosso próprio
código, `uinput_gamepad.py:71-76`, que declara uma incerteza aberta:

> *"um vpad uinput 0df2 não tem hidraw — o SDL não usa o driver HIDAPI PS5 nele
> e cai no matching evdev com um GUID (version 0x3) **ausente do
> gamecontrollerdb**; esse mapeamento **NUNCA foi validado ao vivo**"*

E é **por causa dessa incerteza** que `daemon.launch_env.compose_env` omite o
`IGNORE_DEVICES` quando um vpad está no backend degradado (DEDUP-04). Ou seja:
uma decisão de produto, hoje, em vigor, apoiada na premissa *"o SDL não sabe ler
este GUID"*.

**Pois a Steam tem uma linha para esse GUID exato, no disco dela, agora.**

- **MEDIDO:** o GUID do nosso vpad está no `SDL_GamepadBind` do `config.vdf`.
- **SEM PROVA:** se a Steam exporta esse campo aos jogos (via
  `SDL_GAMECONTROLLERCONFIG` no ambiente do processo lançado) e, portanto, se
  esse mapeamento **vence** no jogo. **É a pergunta que decide se a premissa do
  DEDUP-04 ainda vale.**

**MEDIDO, e é o dado mais desconfortável da seção:** as cadeias
`SDL_GamepadBind`, `SDL_GAMECONTROLLERCONFIG`, `gyro_data` e `_gyro.vdf` têm
**zero ocorrências** em `src/`, `scripts/`, `assets/` e `docs/`. O produto não
escreve, não lê, não vigia, não documenta. É um ponto cego total.

> **Custo em minutos de confusão: o mais insidioso do documento.** O sintoma
> seria *"os botões saem trocados, mas só neste jogo e só nesta máquina"* — e
> ele é **irreproduzível em qualquer outra máquina**, porque a causa é um
> arquivo local que ninguém no projeto sabe que existe. É a definição de horas
> perdidas.

**Desenho (não construído), e é barato:**

1. **Medir primeiro, dez minutos.** O wrapper `hefesto-launch` **já roda dentro
   do ambiente do jogo** — é o lugar perfeito para despejar `env | grep -i sdl`
   uma vez, num arquivo, e responder de vez se o `SDL_GAMECONTROLLERCONFIG`
   chega. Sem essa medição, tudo abaixo é palpite.
2. **Só depois**, se chegar: o doctor passa a ler o `SDL_GamepadBind`, procurar o
   GUID do vpad ativo e **nomear** a divergência.
3. **Não escrever nele.** É campo de uma linha e de outro dono: escrever aqui
   seria criar o oitavo caso da própria classe que este documento nomeia. **A
   decisão é dela**, e a recomendação é não.
4. As duas entradas de bancada são **sujeira nossa na máquina dela**, e a lição
   é de processo, não de código: *a bancada não roda com a Steam aberta.*

### 3.2 A família `*_gyro.vdf` — um arquivo por identidade que já inventamos

**MEDIDO:** `~/.steam/steam/config/` tem **19** arquivos `*_gyro.vdf`. Cada um é
a calibração de giroscópio de **uma identidade de controle** que a Steam já viu.
O conteúdo do que corresponde ao nosso vpad (`54c-df2-…_gyro.vdf`):

```
"gyro_data"
{
	"gyro_stationary_noise_tolerance"		"0.5"
	"accelerometer_stationary_noise_tolerance"		"12"
	"gyro_drift_per_sample_x"		"0"
	...
}
```

O nome do arquivo é a identidade. Duas convenções convivem: `vid-pid-sufixo` e
`prefixo+MAC`. Quatro deles chamam-se `DSE` + `02fe00000001` … `02fe00000004` —
`DSE` de *DualSense Edge* (o PID `0x0df2` que o vpad apresenta) e o resto é o
`uniq` sintético dos nossos slots, documentado em
`app/actions/emulation_actions.py:55`.

> **A Steam criou uma calibração permanente para cada um dos nossos quatro
> jogadores virtuais.** Nenhum deles tem giroscópio físico.

Há ainda quatro arquivos cujos nomes **são MACs reais dos controles dela** — não
transcritos aqui, pela regra da casa.

**A consequência real, e ela é modesta — o que também importa dizer:** a
calibração é **por identidade**. Toda vez que o produto muda a identidade de um
slot, a Steam abre um arquivo novo e **abandona** o antigo. O sintoma seria
*"o giroscópio ficou com drift depois de eu mexer nas configurações"*, sem nada
no nosso lado que explique. Nenhum comando de desinstalação limpa isso, e nem
deveria — o arquivo é da Steam.

**MEDIDO:** a lista cresce e nunca encolhe. 19 hoje.

> **Custo em minutos de confusão: baixo**, e está aqui por honestidade de censo,
> não por urgência. Vale **uma linha** no
> `docs/protocol/pilha-steam-input-xpad-sdl.md`, para que a próxima pessoa que
> vir drift de giroscópio saiba que existe estado da Steam por identidade. Nada
> mais.

---

## 4. O buraco estrutural: metade dos arquivos que importam não tem vigia

**MEDIDO.** O produto inteiro tem **um** `.path` unit — `assets/hefesto-steam-input-guard.path` — e ele vigia **um** diretório:

```
PathChanged=%h/.steam/steam/userdata
PathChanged=%h/.local/share/Steam/userdata
PathChanged=%h/.var/app/com.valvesoftware.Steam/.steam/steam/userdata
```

Quando dispara, roda `disable_steam_input.sh --apply-quiet`
(`hefesto-steam-input-guard.service:10`), e há um `.timer` de reforço a cada
30 min.

Cruzando isso com os arquivos da Steam que o produto de fato usa:

| arquivo | onde mora | vigiado? |
|---|---|---|
| `localconfig.vdf` | `userdata/<id>/config/` | **sim** (mas só para 3 chaves — ver abaixo) |
| `config.vdf` | `~/.steam/steam/config/` | **NÃO — fora da árvore vigiada** |
| `*_gyro.vdf` | `~/.steam/steam/config/` | **NÃO** |
| `compat.vdf` | `userdata/<id>/config/` | dentro da árvore, mas ninguém o lê |

E o disparo, quando acontece, olha **três chaves**:
`SteamController_PSSupport`, `SteamController_SwitchSupport`,
`UseSteamControllerConfig` (`disable_steam_input.sh:133`).

> **A assimetria, em uma frase:** um `localconfig.vdf` que muda **acorda** o
> guarda; o guarda entra, confere três chaves, e **passa ao lado do
> `LaunchOptions`** — o campo que quebrou. E o `config.vdf`, onde moram o
> `CompatToolMapping` que nós pinamos e o `SDL_GamepadBind` da seção 3.1, **não
> acorda ninguém**, porque está fora dos três caminhos vigiados.

**Desenho (não construído):** o irmão já propôs somar o `LaunchOptions` ao
`ExecStart` do guarda que já existe — uma linha, sem unidade nova. **Acrescento
duas condições que ele não tinha como ver:**

1. **Depende da cura da árvore.** Um guarda que repara com o parser que funde as
   três árvores repara com a régua errada, **em laço, a cada 30 minutos**. A
   ordem importa.
2. **`config.vdf` pede um `PathChanged` próprio**, ou o pin do Proton segue
   valendo só até a Steam decidir o contrário entre um install e o seguinte.

---

## 5. Uma correção de endereço (regra da casa: fato errado se substitui)

O documento irmão localiza o `SteamController_PSSupport` em
`localconfig.vdf`, caminho `Software/Valve/Steam`.

**MEDIDO** — no arquivo dela, o caminho real é a **raiz**:

```
UserLocalConfigStore/SteamController_PSSupport
UserLocalConfigStore/SteamController_Enable_Chord
```

Não afeta o produto — o `_transform_vdf` do `disable_steam_input.sh` casa por
`gsub` na linha inteira, sem âncora de caminho, e por isso acerta de qualquer
jeito. Mas **o próximo instrumento que quiser ancorar por caminho** — e a lição
central de toda esta madrugada é que ancorar por caminho é o certo — usaria o
endereço errado e não acharia a chave. Fica corrigido aqui.

*(De brinde, um campo a mais no censo: `SteamController_Enable_Chord`, valor
`"0"`, global. O produto não escreve nem lê. **SEM PROVA** de que nos afeta.)*

---

## 6. O que ficou aberto, ordenado por consequência

| # | O quê | Onde | Preço de não fazer | Dono |
|---|---|---|---|---|
| 1 | O `pass` do broker passa a **nomear** o físico não escondido, e a comparar com o censo de físicos | `doctor.sh:3090` e `:3232` | Controle dobrado no jogo com o doctor em verde — três frentes caras de investigação para nada | doctor |
| 2 | Matar (ou rebaixar a `info`) o contador `76 jogo(s)` | `doctor.sh:1516` | Verde falso ao lado do vermelho verdadeiro, toda vez: o portão morre de descrédito | doctor |
| 3 | Bonds: nomear os MACs em `cache/` sem `info/` (diferença de conjuntos) | `doctor.sh:2818` | *"Um controle parou de reconectar"* mandado para a trilha mais cara da casa | doctor |
| 4 | **Medir** se `SDL_GAMECONTROLLERCONFIG` chega ao jogo — um `env \| grep -i sdl` dentro do wrapper que **já roda lá** | `assets/hefesto-launch.sh` | A premissa do DEDUP-04 (`uinput_gamepad.py:71-76`) segue não verificada, com a Steam tendo uma linha para o nosso GUID | quem tocar o `launch_env` |
| 5 | Guarda periódico olhar o `LaunchOptions` — **depois** da cura da árvore | `assets/` + `install.sh` | Entre dois installs, qualquer variável nova apaga o wrapper. Antes da cura da árvore, repara errado em laço | `assets/` |
| 6 | `PathChanged` para `~/.steam/steam/config` | `assets/` | O pin do Proton e o `SDL_GamepadBind` mudam sem ninguém acordar | `assets/` |
| 7 | Uma linha na canônica sobre `*_gyro.vdf` (estado da Steam por identidade) | `docs/protocol/pilha-steam-input-xpad-sdl.md` | Drift de giroscópio procurado dentro do nosso código | protocolo |
| 8 | Regra de bancada: **não rodar ensaio de vpad com a Steam aberta** | `docs/process/` | Cada ensaio deixa uma entrada permanente no `config.vdf` dela. Já são duas | processo |

---

## 7. A regra que este documento pede que a casa adote

O irmão já propôs *"portão tem de responder **qual**, não **quantos**"*, e a
varredura desta seção 2 confirma que a casa quase toda já obedece. Acrescento a
que **falta**, e que teria pego os três de hoje:

> **Um portão nunca reduz uma lista a um número.** Se o instrumento **teve** os
> nomes em mãos — e o do broker teve, literalmente, e chamou `len()` neles —
> reduzi-los a um inteiro é destruir a única coisa que a pessoa ia usar.
>
> E o veredito de um portão **nunca** é `N > 0`. É `obtido == esperado`, com o
> nome da diferença impresso. `> 0` responde *"já funcionou alguma vez?"*.
> Ninguém nunca precisou saber isso.

E a que vale para a classe inteira deste documento:

> **Em campo de uma linha e de outro dono, o produto pode escrever — mas nunca
> pode acreditar que escreveu.** Ou existe um vigia com âncora de caminho, ou a
> escrita é uma aposta com prazo desconhecido.

---

## 8. Onde está cada coisa

- `scripts/doctor.sh` — `check_launch_wrapper` (:1508, o contador de 76),
  `check_arvore_canonica_do_wrapper` (:1697, a régua honesta que já nomeia o
  Pragmata), `check_bt_bonds_persistidos` (:2809), o bloco do broker (:3088 e
  :3226)
- `scripts/disable_steam_input.sh` — `_transform_vdf` (:255) e o molde de ouro
  `needs_real_fix` (:363)
- `assets/hefesto-steam-input-guard.path` / `.service` / `.timer` — o único vigia
  do produto
- `src/hefesto_dualsense4unix/integrations/uinput_gamepad.py:54-90` — os quatro
  valores que formam o GUID do vpad, e a incerteza aberta nas linhas 71-76
- `src/hefesto_dualsense4unix/integrations/steam_launch_options.py` — escritores
  e leitores do `LaunchOptions` (**em edição por outra frente; não tocado aqui**)
- `src/hefesto_dualsense4unix/integrations/sentinela_do_wrapper.py` — a sentinela
  (**não tocada aqui**)
- [`2026-08-16-A-LINHA-QUE-A-STEAM-COME`](2026-08-16-A-LINHA-QUE-A-STEAM-COME-o-censo-dos-campos-e-a-arvore-errada.md)
  — o irmão: as três árvores `apps`, a fusão que cega o censo, e a tabela dos
  oito campos do `localconfig.vdf`
- `docs/process/sprints/2026-08-16-SENTINELA-WRAPPER-01-a-steam-guarda-uma-linha-por-jogo-e-comeu-a-nossa.md`
  — a sprint do caso que revelou a classe
