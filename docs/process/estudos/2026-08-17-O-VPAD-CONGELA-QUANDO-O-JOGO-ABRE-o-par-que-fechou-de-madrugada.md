# O vpad congela quando o jogo abre — o par que fechou de madrugada

**17/08/2026, 00h20, controle no CABO, DON'T SCREAM.** Depois de vinte horas de
bancada, um par fechou limpo. Ele não resolve o defeito, mas o **localiza** — e
localizar é o que faltava.

---

## A medição

Mesmo controle, mesmo cabo, mesmo daemon, mesmo vpad. A única variável é o jogo
estar aberto ou não:

| | vpad (`/dev/hidraw4`) |
|---|---|
| **sem** jogo aberto | 46 pares de eixo distintos — movimento real |
| **com** jogo aberto | 1573 reports, **`LX` travado em 129** |

**O vpad continua emitindo** — 1573 relatórios em 10 s, cadência normal. O que
para é o CONTEÚDO: os eixos congelam no valor de repouso.

## O que isso derruba

**Não é "o jogo não usa o que recebe".** Essa era a leitura do dia inteiro, e ela
estava errada. O jogo recebe um controle que não se mexe — comportar-se como se
não houvesse controle é o certo da parte dele.

**Não é gate de estado.** Medido no mesmo instante, com o jogo aberto e os eixos
congelados:

```
paused = False            emulation_suppressed = False
native_mode = False       primary_grab_state = held
game_signal.authority = daemon
```

Todos os portões abertos. Nenhum deles explica.

**Não é perda de descritor.** O daemon segue com `event25 event26 event27
hidraw5` abertos — exatamente os nós do físico, conferidos contra
`/proc/bus/input/devices` no mesmo minuto.

## O que sobra, e tem endereço

O daemon **tem o dispositivo certo aberto e não recebe eventos dele**. É o mesmo
estado do `state_stale_neutral_warning`, agora reproduzido no CABO e com gatilho
conhecido: **abrir o jogo**.

### Os dois candidatos desta madrugada, e por que os dois caíram

O log do instante trazia duas linhas que esta página tratou como sintomas do
mesmo problema:

```
backend_hotplug_reconcile  trigger=input_dir_change     (8 vezes em 10 min)
gatilho_disparou  nome=lightbar  resultado={}           (resultado VAZIO)
```

**As duas leituras estavam erradas, e a leitura do fonte C e do nosso próprio
código as derrubou em 17/08 de manhã.** Ficam aqui pelo mesmo motivo que a casa
guarda o resto: para ninguém gastar o dia refazendo o caminho.

**1. O `resultado={}` NÃO é referência perdida — é a resposta certa.** O gatilho
da lightbar pinta **só por Bluetooth**: a lista de alvos é filtrada por
`_detect_transport(handle) == "bt"` (`core/backend_pydualsense.py:2883-2887`), e
a docstring da própria função já dizia isto em `:2870` — *"Vazio significa
'nenhum DualSense no rádio' ou 'Modo Nativo' — resposta, não erro"*. **O controle
estava no CABO.** Um gatilho de rádio devolvendo vazio no cabo é o resultado
trivial, e lê-lo como perda de referência mandaria a próxima pessoa investigar
um subsistema são.

**2. O `backend_hotplug_reconcile` é uma LINHA DE LOG, não uma ação.** Ele não
fecha descritor, não recria o `EvdevReader`, não refaz grab e não troca a
referência do backend. Quem age é o `controller.connect()` da volta seguinte — e
ele tem retorno antecipado em dois pontos: controle já presente não é reaberto
(`backend_pydualsense.py:1966-1968`) e, se o primário não MUDA, o
`_recompute_primary` sai sem tocar em nada (`:2231-2232`). Com o controle no cabo
e sem troca de primário, oito reconciles custam oito enumerações de hidapi e
**não encostam no leitor de evdev**. Logo: nem é a causa, nem seria a cura.

Os oito reconciles continuam sendo verdade — são o Proton mexendo em
`/dev/input`, que é o que ele faz. Só não são o fio.

### O que era, e a régua estava na própria casa

**O `LX` travado em 129 é a prova, e ninguém tinha lido o número.** 129 não é o
valor de fábrica do snapshot — esse é **128 cravado** (`EvdevSnapshot.lx`). O 129
é o que a `_semear_posicao_de_repouso` escreve **no open**, lendo do `absinfo` a
posição real daquela unidade (SEMENTE-DO-REPOUSO-01, 15/08; nenhuma das quatro
unidades da mesa repousa em 128, e o centro medido desta em 17/08 é `ABS_X=127`).

Ou seja, o número diz uma frase inteira: **o nó foi REABERTO com sucesso, e a
partir daquele open zero `EV_ABS` chegou.**

E "o vpad continua emitindo" nunca foi consolo, porque **quem emitia não era quem
tinha parado**. O vpad tem dois leitores alimentando o mesmo report: o
`PhysicalReportReader` (hidraw — giro, touch, acel) e o `EvdevReader` (sticks,
botões, gatilhos). Os ~157 Hz medidos não cabem nos 60 Hz do poll loop
(`lifecycle.py`, `DEFAULT_POLL_HZ`) e cabem nos 250 Hz do espelho de motion
(`physical_report_reader.py:227`): **quem emitia era o ramo do hidraw, vivo. O
ramo do evdev é que estava mudo** — e é dele que sai o que o jogo joga.

**A causa, com endereço:** o `EvdevReader` não tinha teto de silêncio. O irmão
`PhysicalReportReader` tem desde a GYRO-BT-SILENCIO-01
(`physical_report_reader.py:258-259`, aplicado em `:833-844`): larga o fd e
re-resolve. O `EvdevReader` só sabia se curar quando o nó **trocava de número**
(`is_stale`) — e este modo de falha não troca. Um nó que parasse de entregar
mantendo o mesmo `event25` ficava mudo **para sempre**, fd aberto, sem `ENODEV`,
sem exceção, sem uma linha no journal. Era por isso que só `systemctl restart`
curava.

**A cura (17/08, VIGIA-DO-MUDO-01):** copiar o teto do irmão seria um segundo
defeito — o hidraw entrega 250 Hz mesmo com o controle parado na mesa, então lá
silêncio É link morto; o evdev só emite quando algo MUDA, e um controle em
repouso fica legitimamente mudo. A régua tinha de ser outra, e a casa já a tinha
escrito: o `EVIOCGABS` lê o estado do `input_dev`, **não a nossa fila de
eventos** — medido em 17/08 com o daemon segurando o grab do `event25`, um
segundo leitor sem grab recebe zero eventos e mesmo assim vê o `absinfo`
acompanhar o kernel. O vigia pergunta ao kernel a cada 2 s de silêncio; duas
discordâncias consecutivas e ele larga o fd. Portão:
`tests/unit/test_vigia_do_mudo_01_o_leitor_que_ficava_mudo_para_sempre.py`.

## O que NÃO foi medido, e por que

Ao fim da sessão o controle parou de entregar movimento **mesmo sem o jogo** — 9
pares de eixo contra os 46 de uma hora antes. Duas leituras possíveis, e nenhuma
foi isolada:

- o estado degradou ao longo da sessão (vários restarts do daemon, troca de
  perfil de áudio, o controle indo e voltando entre rádio e cabo);
- ou a mão dela cansou depois de vinte horas, e o gesto não foi o mesmo.

**A segunda possibilidade é motivo suficiente para parar.** Um ensaio que depende
do gesto humano vale o que vale a atenção de quem faz o gesto — e essa é uma
variável que também precisa estar controlada. Insistir aqui produziria número
para registrar, não verdade para usar.

## O ensaio que a próxima sessão deve fazer PRIMEIRO

**NOTA DATADA (17/08/2026, 03h30).** O ensaio abaixo foi desenhado para decidir
entre "o reconcile é a causa" e "o reconcile é sintoma", e **essa pergunta caiu
antes de ele rodar** — a leitura do código respondeu por menos: o reconcile é
linha de log e não encosta no leitor. O ensaio fica registrado porque o desenho
dele continua bom (par com/sem, uma variável), mas contar reconciles não decide
mais nada. O instrumento que substitui é o
`scripts/ensaios/o_vpad_quando_o_jogo_abre.py`, que separa o que este dia não
sabia separar: o vpad **MORRER** (o nó some) do vpad **CONGELAR** (o nó vive e o
conteúdo para). São dois defeitos, com duas curas.

O ensaio original, como foi escrito:

1. daemon recém-reiniciado, controle no cabo, **nenhum jogo**;
2. medir o vpad com um gesto (deve dar dezenas de pares de eixo — é o gabarito);
3. **abrir o jogo** e medir de novo, sem tocar em mais nada;
4. ~~se congelar, contar os `backend_hotplug_reconcile` da janela~~ — caducou.

## O segundo defeito, que este dia não sabia que existia

Medido em 17/08 com par fechado, e ele não é o congelamento: **o vpad também
MORRE**, e por outro caminho. Mesmo daemon, mesmo minuto, única variável o perfil
ativo:

| perfil ativado | `/dev/hidraw4` |
|---|---|
| `Dont Scream` (tem `mode.kind=gamepad`) | **nasce** |
| `Navegação` (sem campo `mode`) | **some** |

O perfil de desktop dela casa com `steam` e `Steam` no `window_class`. Logo,
alternar para a janela da Steam no meio da partida destruía o controle virtual, e
o jogo ficava com um descritor órfão. Não era regressão de 16/08: a reversão por
"perfil sem opinião" é de 13/07 (`c106ee3`), estreitada em 23/07 (`19bc7e9`) com
duas guardas — e a que devia proteger a partida (`lifecycle._janela_de_jogo_em_foco`)
só reconhecia `steam_app_<id>`, sendo **cega justamente para a janela do cliente
Steam**. Curado em 17/08 por decisão dela; portão em
`tests/unit/test_vpad_na_janela_da_steam_01_o_alt_tab_que_matava_o_controle.py`.

**A lição de método:** "o vpad continua emitindo" e "o vpad sumiu" produzem o
MESMO relato de quem joga — *"o controle não funciona"* — e têm curas que não se
parecem. Enquanto os dois estiverem juntos num só sintoma, metade das medições
mede o outro defeito.

## O que este dia acrescenta à metodologia

Uma quarta regra, irmã das três de ontem:

> **A atenção de quem faz o gesto é uma variável do ensaio.** Depois de muitas
> horas, "mexa o analógico" deixa de ser um estímulo controlado. Medição que
> depende da mão humana tem hora para acabar, e reconhecer isso é parte do
> método — não desistência.
