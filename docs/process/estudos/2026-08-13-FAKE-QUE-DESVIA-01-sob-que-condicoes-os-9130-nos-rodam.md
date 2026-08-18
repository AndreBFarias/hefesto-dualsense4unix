# FAKE-QUE-DESVIA-01 — sob que condições os 9130 nós rodam

- **Levantado em:** 13/08/2026, sobre `restauro/inicio-da-sessao`, `v0.9.4.2`,
  HEAD `cc768d4`. Estudo somente-leitura: nenhum byte de `src/` ou de `tests/`
  foi alterado
- **A pergunta:** `tests/conftest.py:1109` é o único `autouse=True` do arquivo e
  liga `HEFESTO_DUALSENSE4UNIX_FAKE=1` em toda a suíte. Quais ramos de `src/`
  só são alcançados com esse flag AUSENTE? Quantos dos 9130 nós mudam de
  resultado sem ele? E — a que importa — **algum dos `teste_que_morde` do mapa
  vive num ramo que o flag desvia?** Se vivesse, aquela célula teria grau forte
  sustentado por um teste que nunca tocou o caminho real, que é exatamente a
  doença que o mapa existe para impedir
- **A resposta, em uma linha:** **nenhum.** Zero dos 9130 nós muda de desfecho
  sem o flag, e zero das 40 células com `teste_que_morde` vive num ramo desviado
- **O preço de perguntar:** o experimento como a leva o descreve — *"rodar a
  suíte com o autouse desligado"* — é **destrutivo nesta máquina**, e a seção 2
  mostra a corrente inteira, de `conftest.py:1132` até os quatro controles dela.
  A medição foi feita numa caixa `bwrap` onde os ramos reais são **tomados** e o
  recurso do outro lado **não existe**
- **Portões:** `validar-glifos.py` e `validar-acentuacao.py` rodados sobre este
  arquivo com caminho explícito, porque ele é novo

---

## 1. O que o flag desvia — os três sítios, lidos no fonte

O flag tem **exatamente três consumidores** em `src/`, mais um que só rotula
log e um derivado. A lista é completa: sai de `grep -rn
"HEFESTO_DUALSENSE4UNIX_FAKE" src/` cruzado com os usos de `fake_mode_enabled`.

| | Onde | Comparação | Com `FAKE=1` | Com o flag AUSENTE |
|---|---|---|---|---|
| **R1** | `utils/xdg_paths.py:33`, consumido em `:56` por `ipc_socket_name()` | `== "1"` | `hefesto-dualsense4unix-fake.sock` | **`hefesto-dualsense4unix.sock`** — o socket de PRODUÇÃO |
| **R2** | `daemon/main.py:18`, em `build_controller()` | `== "1"` | `FakeController` | **`PyDualSenseController()`** — hardware real |
| **R3** | `daemon/subsystems/keyboard.py:322`, em `_start_touchpad_reader()` | verdade | pula o reader | **enumera evdev e faz `reader.start()`** |
| derivado | `daemon/main.py:54`, `single_instance_name()` | herda de R1 | `daemon-hefesto-dualsense4unix-fake` | **`daemon`** — o lock de PRODUÇÃO |
| só log | `daemon/main.py:113` | `== "1"` | campo `fake=True` | campo `fake=False` (sem efeito) |

Duas assimetrias que aparecem só quando se lê os três lado a lado:

**A primeira é uma armadilha de valor.** R1 e R2 comparam `== "1"`; R3 testa
verdade. Então `HEFESTO_DUALSENSE4UNIX_FAKE=0` produz um estado que ninguém
pretendeu: **controlador REAL com o leitor de touchpad PULADO**. Não é defeito
de hoje — nada no produto seta `0` —, mas é uma borda que um `export` distraído
alcança.

**A segunda é uma promessa maior que a entrega.** O docstring de
`tests/conftest.py:1113-1118` diz que subsistemas que fazem probing de hardware
real *"devem pular a inicialização quando o flag está presente"*, e dá o
`TouchpadReader` como exemplo. Só que `daemon/sensor_hub.py:311-339` também
constrói `TouchpadReader` e `MotionSensorReader`, e também descobre nós evdev —
**sem consultar o flag**. O `SensorHub` se protege por injeção
(`sensor_hub.py:79-82`: as fábricas reais são só o default de parâmetros que o
teste substitui), não pelo flag. Ou seja: dos dois subsistemas que fazem
probing, **um honra o flag e o outro usa outra disciplina**. A frase do
docstring descreve um contrato que vale num lugar só.

## 2. Por que o experimento literal é destrutivo aqui

A leva pede para rodar a suíte com o guarda desligado. Esta máquina, medida
hoje às 11h da manhã, tem:

- o **daemon vivo**, PID 1681 (`hefesto-dualsense4unix daemon start --foreground`);
- o **broker hidraw vivo**, PID 3448, com o socket de pé em
  `/run/hefesto-hidraw-broker/broker.sock`, modo `srw-rw----`, grupo
  `vitoriamaria` — quer dizer, **gravável por quem roda o pytest**;
- `/dev/hidraw0` a `/dev/hidraw5`, e o `getfacl` do primeiro devolve
  `user:vitoriamaria:rw-` — **sem sudo nenhum**;
- o socket IPC vivo em
  `/run/user/1000/hefesto-dualsense4unix/hefesto-dualsense4unix.sock`.

A corrente do flag até os controles dela tem quatro elos, todos citáveis:

1. `tests/conftest.py:1132-1133` liga o flag. Tire-o e R1 dispara.
2. R1 faz `ipc_socket_name()` devolver o nome de PRODUÇÃO. **Medido**, não
   inferido: a sonda da seção 3 imprimiu
   `assert 'hefesto-dualsense4unix.sock' == 'hefesto-dual...nix-fake.sock'`.
3. `ipc_socket_path()` (`xdg_paths.py:128`) compõe esse nome com o
   `runtime_dir()`, e `XDG_RUNTIME_DIR` **não é isolado de propósito** — o
   comentário em `conftest.py:1134-1137` explica por quê. O caminho resultante é,
   literalmente, o socket do daemon vivo dela.
4. `cli/ipc_client.py:63` — `path = socket_path or ipc_socket_path()`. Todo teste
   que construa um cliente sem passar caminho passa a **falar com o daemon dela**,
   e um `call()` de LED, gatilho ou rumble atravessa até os quatro controles.

O `IpcServer` não completa a corrente, e vale registrar por quê: o probe de
vivacidade de `ipc_server.py:210-239` (ADR-010) conecta antes de apagar e
**recusa o start** com `socket ocupado por outro daemon` quando alguém responde.
Ele protege o arquivo — mas o probe ainda é uma conexão ao socket vivo, e o
cliente do elo 4 não tem essa proteção.

E há uma distinção que a leva funde e que muda tudo: **"desligar o autouse" não
é "tirar o FAKE"**. Aquela fixture faz cinco coisas, e o flag é uma. Desligá-la
inteira também:

- desisola `XDG_CONFIG_HOME` e irmãos (`conftest.py:1144-1153`) — a suíte volta a
  escrever nos perfis reais dela, que é o defeito BUG-TEST-CONFIG-LEAK-01
  registrado ali mesmo, e o CANARIO-FS-01;
- devolve o `HEFESTO_BROKER_SOCKET` ao default (`conftest.py:1162-1167`), cujo
  aviso é explícito: *"um teste que resolvesse o default esconderia/abriria
  hidraw DE VERDADE no meio da suíte"* — e esse broker está de pé agora;
- religa a semeadura de presets (`conftest.py:1154-1161`).

São quatro experimentos diferentes. **Este estudo mediu um: o flag.** É o que a
pergunta do mapa exige, e é o único que se consegue isolar.

## 3. Como medi — a caixa que toma o ramo e tira o recurso

A saída não é desviar o ramo: é deixar o ramo real ser tomado e **sumir com o
recurso do outro lado**. Uma caixa `bwrap`, sem privilégio nenhum:

```bash
bwrap --ro-bind / /  --proc /proc  --dev /dev \
      --tmpfs /run  --dir /run/user  --dir /run/user/1000 --chmod 0700 /run/user/1000 \
      --tmpfs /tmp  --bind "$SCRATCH" "$SCRATCH" \
      --setenv HOME "$LAR_FALSO" --setenv XDG_RUNTIME_DIR /run/user/1000 \
      --setenv TMPDIR /tmp  --unshare-pid --die-with-parent --new-session -- "$@"
```

Dentro dela não há `hidraw`, não há `uinput`, não há `input/event*`, não há o
socket do daemon vivo, não há o socket do broker, e o namespace de PID impede
sinalizar qualquer processo de fora (`ls /proc` mostra `1` e `2`). O `/dev/hidraw*`
some porque `--dev` monta um `/dev` mínimo; conferido: a caixa lista catorze nós,
e nenhum é de HID.

O flag foi retirado por uma fixture que **depende** do autouse — é o que garante
a ordem, porque uma fixture que pede outra roda depois dela:

```python
@pytest.fixture(autouse=True)
def _estudo_sem_fake(_hefesto_fake_env, monkeypatch):
    monkeypatch.delenv("HEFESTO_DUALSENSE4UNIX_FAKE", raising=False)
```

Assim o autouse faz tudo o que faz — isolar XDG, apontar o broker para o vazio,
pular a semeadura — e só então o flag sai. **Um efeito por vez.**

Cinco braços, todos na mesma caixa, em série (dois `pytest` disputando CPU
mediriam a máquina, não o flag), com um registrador idêntico em todos gravando
`desfecho` por `nodeid`:

| Braço | O que muda | Para quê |
|---|---|---|
| **A** | nada | controle |
| **A2** | nada | piso de ruído |
| **B** | só o flag, ausente | a variável do estudo |
| **P** | só o `SKIP_PRESET_SEED`, ausente | controle positivo (falhou; ver 5) |
| **M2** | `fake_mode_enabled()` forçado a `False` por nó | controle positivo que funcionou |

## 4. Os números

```
nós coletados ................................. 9130
piso de ruído (A vs A2) ....................... 0 nós mudaram
sinal do flag (A vs B) ........................ 0 nós mudaram
controle positivo (A vs M2) ................... 4 nós mudaram
```

O braço B se auditou: a fixture registrou `fixture_aplicada_em 9130` e
`flag_ausente_no_inicio_do_no 9130`. **Não é "a fixture não pegou": o flag
estava mesmo ausente nos 9130 nós, e nenhum reparou.**

O alcance dos três sítios, medido com espiões reinstalados a cada nó, sem
desviar ramo nenhum:

```
R1  xdg_paths.fake_mode_enabled ......... 76 nós  (71 com flag='1', 5 sem)
R2  daemon.main.build_controller .........  0 nós  — NUNCA ALCANÇADO
R3  keyboard._start_touchpad_reader ......  0 nós  — NUNCA ALCANÇADO
```

R2 e R3 nunca são executados pela suíte, e a leitura do fonte concorda:
`build_controller()` tem **um** chamador, `daemon/main.py:90`, dentro de
`run_daemon()`, que por sua vez só é chamado de `cli/app.py:313`. Nenhum teste
entra por ali. Quer dizer: **o ramo que abriria o hardware de verdade não é
alcançável pela suíte** — o que é uma boa notícia, e também significa que
`FakeController` vs. `PyDualSenseController` não tem nó nenhum que o prove.

Por que então B deu zero, se 76 nós chegam ao R1? Porque os nós que dependem do
flag **o administram eles mesmos**: cinco chegam ao R1 já com o flag ausente
porque o apagaram (`test_xdg_paths.py:41,115`,
`test_daemon_single_instance_name.py:20`), e os que exigem o modo fake o religam
(`test_xdg_paths.py:96,107,117`, `test_daemon_single_instance_name.py:28`). Os
outros 71 passam pelo R1 sem que o resultado dependa do que ele devolve.

Os 4 nós que o controle positivo derruba são exatamente esses guardiões:

```
tests/unit/test_daemon_single_instance_name.py::test_fake_sem_env_auto_isola_lock
tests/unit/test_gravador_recusa_com_daemon_vivo.py::test_recusa_e_nao_grava_com_o_socket_de_pe
tests/unit/test_xdg_paths.py::test_fake_auto_isola_socket_sem_override
tests/unit/test_xdg_paths.py::test_fake_e_producao_usam_sockets_distintos
```

A cura BUG-FAKE-SOCKET-SYNC-01 **tem** quem a defenda. O que não tem defensor é
a linha `conftest.py:1132-1133`: apagá-la hoje não reprova nó nenhum.

## 5. As duas vezes em que o instrumento mentiu

Vale mais que os números, porque a próxima pessoa vai cair nas mesmas.

**A primeira: a caixa matou a testemunha.** A primeira versão pôs o `TMPDIR` no
scratchpad, cujo caminho tem 105 bytes. O limite de `sun_path` do `AF_UNIX` é
108. Resultado: `OSError: AF_UNIX path too long`, e **131 nós morriam no setup**,
concentrados nos arquivos que abrem socket Unix — que são justamente os que
exercitam o ramo sob estudo. A primeira rodada dava "zero nós mudaram" com a
testemunha amordaçada. Depois de pôr o `TMPDIR` em `/tmp` e recriar
`/run/user/1000` vazio dentro da caixa, `test_ipc_apply_draft.py` saiu de "5
passados e 16 erros" para tudo verde, e junto com `test_ipc_server.py` deu **45
passados**. O erro era do instrumento, com cara de defeito do produto.

**A segunda, e esta é para guardar: `tests/unit/test_single_instance.py:86` faz
`importlib.reload(xdg_paths)` no meio da suíte, e isso APAGA qualquer mutação
feita por patch de atributo de módulo.** Medido, com a mesma mutação nos dois
casos:

```
pytest tests/unit/test_xdg_paths.py                                  -> 2 failed, 5 passed
pytest tests/unit/test_single_instance.py tests/unit/test_xdg_paths.py -> 30 passed
```

A mutação some porque `reload` reconstrói o dicionário do módulo. Como
`test_single_instance` vem antes de `test_xdg_paths` na ordem alfabética, todo
alvo depois do `s` fica **imune sem que ninguém perceba** — o relatório continua
verde e parece prova. Foi assim que meu primeiro controle positivo contou 2 em
vez de 4, e que o primeiro alcance do R1 contou 65 em vez de 76. A cura é
aplicar a mutação **por nó**, numa fixture `autouse`, em vez de uma vez em
`pytest_configure`.

O alcance disto passa deste estudo. `tests/conftest.py:1184-1188` guarda uma
medição por mutação — *"trocar R por B dentro de `_build_common` deixava a suíte
INTEIRA verde"* — que é uma das pernas do mapa. **Se aquela mutação foi feita
editando o fonte, o `reload` não a afeta e o número está de pé**; se foi feita
por patch de atributo em tempo de execução, ela pode ter sido apagada no meio do
caminho. Não estou derrubando o número: estou dizendo qual pergunta o mantém de
pé, e que ela tem uma resposta certa.

## 6. O cruzamento com o mapa — a pergunta que a leva mandou responder

`docs/data/mapa-controles.csv` tem 293 linhas, **40 células** com
`teste_que_morde` preenchido, apontando **28 nós distintos** — uma célula,
`vibracao.rumble.ff`, aponta dois nós separados por `;`, o que dá 41 pares
célula-alvo; e os dois nós que ela cita já aparecem sozinhos em outras células.

```
alvos que o mapa aponta e a suíte NÃO coleta ....... 0
alvos que MUDAM de desfecho sem o flag do fake ..... 0
```

**Nenhuma célula do mapa se apoia num teste que o FAKE desvia.** E de lambuja, o
mapa não tem ponteiro morto: os 28 nós existem e são coletados, com sufixo de
parametrização (`[usb]`/`[bt]`) quando é o caso.

A doença que esta leva foi caçar **não está no mapa**. É um resultado negativo, e
era para ser: valia rodar porque, se estivesse, teria invalidado células de grau
forte.

## 7. O que fica

Nada aqui vira código sem decisão dela. Em ordem de tamanho:

1. **O `reload` que apaga mutação** (seção 5) é o achado com maior alcance. Vale
   uma nota onde a casa fala de prova por mutação, para que ninguém repita a
   medição pelo caminho que mente.
2. **O guarda não tem guarda.** Apagar `conftest.py:1132-1133` hoje não reprova
   nada. A mordida existe e é barata — um nó que afirme que o flag chega ao
   teste —, mas é cura, e esta leva era resposta.
3. **R2 e R3 não têm nó nenhum.** Nenhum teste distingue `FakeController` de
   `PyDualSenseController`, nem exercita o desvio do leitor de touchpad.
4. **A borda do `FAKE=0`** (seção 1) e a **frase larga demais** do docstring de
   `conftest.py:1113-1118` sobre o `sensor_hub`.
