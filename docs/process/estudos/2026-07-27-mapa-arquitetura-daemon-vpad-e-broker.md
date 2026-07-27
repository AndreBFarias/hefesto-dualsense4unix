# Mapa: a arquitetura do daemon, do gamepad virtual e do broker

- **Levantado em:** 26-27/07/2026, sobre `restauro/inicio-da-sessao` (`v0.2.0`)
- **Escopo:** `core/`, `daemon/`, `broker/`, `profiles/`, `integrations/`,
  `utils/`, `plugin_api/`, `testing/` — 98 arquivos, 43.425 linhas
- **Natureza:** retrato, não proposta. Descreve o que existe

## Por que este documento existe

O `docs/adr/001-pydualsense-backend.md` continua sendo o primeiro texto que
alguém lê para entender como o projeto fala com o controle, e ele descreve uma
arquitetura que o produto abandonou (ver
`sprints/2026-07-26-DOC-VERDADE-01-...`). Este mapa é o retrato de hoje, para
que o próximo estudo não precise refazer a leitura de 43 mil linhas.

## Peso por subpacote

| Subpacote | Arquivos | Linhas | Maiores módulos |
|---|---:|---:|---|
| `daemon/` | 33 | 18.449 | `lifecycle.py` 3378, `ipc_handlers.py` 2736, `subsystems/gamepad.py` 1570, `subsystems/coop.py` 1405 |
| `integrations/` | 26 | 10.239 | `uhid_gamepad.py` 1441, `dualsense_bt_audio.py` 1286, `proton_pin.py` 1194 |
| `core/` | 15 | 7.871 | `backend_pydualsense.py` 3271, `evdev_reader.py` 1453 |
| `profiles/` | 8 | 3.296 | `manager.py` 838, `schema.py` 721 |
| `utils/` | 8 | 1.674 | `session.py` 549 |
| `broker/` | 2 | 1.237 | `hidraw_broker.py` 1229 |
| `plugin_api/` | 4 | 423 | |
| `testing/` | 2 | 236 | |

A densidade de comentário é atipicamente alta: a maior parte dos módulos carrega,
em docstring, o histórico do defeito que motivou cada decisão. Isso infla a
contagem de linhas e **é a documentação de arquitetura real** do projeto.

## O fluxo, ponta a ponta

```
                    DualSense fisico (USB ou Bluetooth)
                              |
        +---------------------+----------------------+
        | INPUT                                      | OUTPUT
        v                                            ^
 /dev/input/eventN            /dev/hidrawN (RO)      |  /dev/hidrawN (RW)
 (via hid_playstation)        report cru             |  + /sys/class/leds/*
        |                          |                 |
        | thread evdev             | thread motion   |
        v                          v                 |
 EvdevReader.snapshot()   PhysicalReportReader       |
 core/evdev_reader.py     core/physical_report_      |
                          reader.py:210              |
        |                          |                 |
        v                          |          _merged_desired_for_key()
 PyDualSenseController.read_state()|          camadas, de baixo p/ cima:
 core/backend_pydualsense.py:1809  |            default broadcast
        |                          |            < auto (cor do slot)
        | ControllerState (frozen) |            < perfil
        v                          |            < usuaria
 Daemon._poll_loop  (60 Hz)        |            < co-op
 daemon/lifecycle.py:3014          |            < JOGO
        |                          |                 ^
        +-> StateStore             |                 |
        +-> EventBus -> plugins, hotkeys              |
        +-> dispatch_gamepad ------+                  |
        +-> CoopManager.forward_all (P2..PN)          |
        +-> mouse / teclado (so se o vpad estiver OFF)|
                                                      |
  VirtualPad (P1..PN)                                 |
  +- backend uhid: /dev/uhid -> hid_playstation faz bind ->
  |  hidraw + lightbar + motion + touchpad reais -> O JOGO abre esse hidraw
  |     ^ UHID_INPUT2 (report 0x01 forjado)
  |     v UHID_OUTPUT (o jogo escreveu rumble/gatilho/luz)
  |        +--> sinks -> apply_game_* -> controle FISICO ---------+
  +- backend uinput: so evdev (mascara Xbox), FF e o unico retorno

  CONSUMIDORES LATERAIS
  +- IPC unix socket JSON-RPC  -> GUI / TUI / CLI / applet COSMIC
  +- UDP 6969 (dialeto DSX)    -> mods de jogo
  +- HTTP 127.0.0.1:9090       -> Prometheus (sem chave de usuario, ver DOC-VERDADE-01)

  CONTROLE DE ACESSO
  broker root (hide / restore / open)  -> esconde o hidraw FISICO do jogo
  a conexao do daemon E a lease; EOF restaura tudo
```

### Quem lê e quem escreve

- **Input** vem do `EvdevReader` (thread própria, `select`), não da
  `pydualsense` — ela ficou como fallback degradado e como caminho do botão de
  microfone (`core/backend_pydualsense.py:1838`).
- **Motion** vem de um segundo descritor, aberto somente-leitura no hidraw
  físico, com cópia byte a byte de uma janela de 25 bytes. O kernel replica
  input reports para todos os descritores, então não há disputa.
- **Output** tem dois caminhos: `sysfs` (`core/sysfs_leds.py`) quando o nó é
  gravável — é o que faz a cor colar no Bluetooth — e `sendReport` para
  gatilhos, rumble e microfone.
- **O jogo** enxerga apenas o gamepad virtual. O físico é escondido por dois
  mecanismos ortogonais: `EVIOCGRAB` no evdev (esconde do SDL) e `hide` do
  broker no hidraw (esconde do winebus e do Proton).

## As três peças que não são óbvias

### 1. O gamepad virtual é um device HID de verdade

`integrations/uhid_gamepad.py:1-47` explica por que não é uinput: um pad uinput é
**apenas evdev**; o SDL, vendo máscara DualSense, procura o hidraw, não acha, e o
rumble morre. Registrando via `/dev/uhid`, o `hid_playstation` faz bind e constrói
o DualSense inteiro de graça — hidraw, lightbar, LEDs de jogador, sensores de
movimento, touchpad, conector de fone.

Detalhes que custaram caro e estão travados por teste:

- **Blueprint canônico embutido** (`integrations/uhid_blueprint.py:104`):
  descritor USB de 289 bytes e os features 0x05, 0x09 e 0x20 vêm de constantes no
  código, nunca lidos do controle na hora de nascer. O modo de falha eliminado:
  por Bluetooth, com o controle ocioso, o firmware emudece e cada `GET_REPORT`
  estoura o tempo limite por **minutos** — o vpad caía para uinput e ficava
  indistinguível do físico.
- **MAC próprio por jogador** (`02:fe:00:00:00:0N`): MAC duplicado derruba o
  probe com `-EEXIST`, e um co-op de quatro viraria um.
- **Apresenta-se como DualSense Edge `054c:0df2`**, nunca `0ce6`. É a chave do
  fim do controle duplicado: a variável que esconde o `0ce6` esconde só o físico.
  Invariante VPAD-06, travado por teste em todos os caminhos de criação.
- **`UHID_BIND_TIMEOUT_S = 0.5`** é medido: o START chega em 2,3 ms, e o valor
  baixo importa porque a espera acontece dentro do laço de polling.

### 2. O broker existe porque o Unix não separa quem pode abrir o dispositivo

`broker/hidraw_broker.py:1-17`: daemon, Steam e jogo rodam com o **mesmo uid**.
Nenhuma permissão tradicional os distingue. Sem isso, nenhuma opção de
inicialização resolve — o winebus dos Protons 10 e 11 entrega hidraw à família
Sony inteira por padrão.

Desenho: serviço systemd de **sistema**, root, endurecido, ativado por socket.
Três comandos:

- `hide` / `restore` — manipula a ACL do `uaccess` por `os.setxattr` direto no
  atributo `system.posix_acl_access`. A escolha está documentada
  (`hidraw_broker.py:35-43`): zero `execve`, o que mantém o `SystemCallFilter`
  intacto, e zero dependência de ABI de biblioteca. O descritor já aberto do
  daemon sobrevive, porque permissão só é checada no `open(2)`.
- `open` — **injeção de descritor**: abre como root e devolve o fd por
  `SCM_RIGHTS` na mesma conexão.

Invariantes:

- **A conexão é a lease.** EOF do socket restaura tudo o que aquela lease
  escondeu. Sem heartbeat: o kernel garante o EOF. O cliente nunca fecha entre
  chamadas e **não tem `__del__`**, de propósito.
- **Validador com cinco barreiras** (`hidraw_broker.py:191`): caminho canônico
  literal, não-symlink e char device, `(major,minor)` batendo o sysfs,
  identidade do pai HID pelo `HID_ID`, e nunca reconcatenar o caminho do
  cliente. `HIDIOCGRAWINFO` no próprio descritor fecha a corrida de reuso de
  minor — sem isso o broker poderia servir um fd root de um teclado Bluetooth ao
  mesmo uid, que é primitiva de keylogger.
- **Falha assimétrica e declarada:** o broker rejeita na dúvida (fail-closed); o
  daemon considera virtual na dúvida (fail-open). Os riscos são opostos.
- **Best-effort sagrado no cliente:** broker ausente devolve `False`/`None` e
  nada levanta. Doutrina: *duplicado é melhor que zero controles.*

### 3. O modelo de precedência tem seis camadas e merge por campo

`core/backend_pydualsense.py:273-295`. O merge é **por campo, nunca por objeto**
(`_merge_desired`, linha 307) — um override parcial precisa herdar a cor global.
Cada campo tem dono registrado por MAC (`_desired_owner_by_uniq`): a ativação de
perfil substitui só o que é dela e nunca apaga o que a usuária ajustou na mão.

Antes era substituição do mapa inteiro. Como o autoswitch ativa perfil a cada
troca de janela, o ajuste por controle era apagado segundos depois — a causa
histórica de *"a config que eu deixo nunca é respeitada"*.

Somam-se três travas temporais: lock manual de 30 s
(`state_store.py:31`), categorias de override (`trigger`, `led`, `rumble`) e o
cadeado do autoswitch.

## Padrões e pontos de extensão

| Abstração | Onde | Papel |
|---|---|---|
| `IController` (ABC) | `core/controller.py:105` | Contrato do controle. **Síncrono por ADR-001** — acoplar a asyncio travaria um backend futuro em C ou Rust |
| `Subsystem` (Protocol) | `daemon/subsystems/base.py:16` | `start`/`stop`/`is_enabled` |
| `DaemonProtocol` | `daemon/protocols.py` | Quebra o ciclo de importação entre `lifecycle` e `subsystems` mantendo `mypy --strict` |
| `VirtualPad` (Protocol) | `integrations/virtual_pad.py:63` | uinput e uhid indistinguíveis para quem chama |
| `WindowBackend` | `integrations/window_backends/base.py` | xlib / portal / wlrctl / null |

Extensões: novo backend de controle (implementar `IController` + trocar
`build_controller()`); novo backend de vpad (cumprir `VirtualPad` + entrar em
`make_virtual_pad`); novo subsistema (**duas** edições — registro e `run()`);
novo método IPC; nova instrução DSX; novo preset de gatilho (o schema valida
sozinho a partir de `PRESET_FACTORIES`).

## Regra estrutural que se confirmou

**`core/` nunca importa `daemon/` nem `integrations/`** — verificado nos imports.
Toda dependência inversa entra por injeção (`set_auto_output_provider`,
`set_game_authority_provider`, `set_feature_opener`, `attach_motion_reader`).
`core/` depende apenas de `utils/`.

## Assimetrias intencionais — conhecer antes de "consertar"

Estão documentadas no código e parecem defeito para quem chega agora:

- o grab nunca é pulado no ungrab;
- `hide` falha aberto, o validador falha fechado;
- debounce do autoswitch é **0,5 s para entrar** e **12 s para sair** rumo a
  catch-all — com 0,5 s nos dois lados, o journal mostrava troca de perfil a cada
  18-28 s no meio do jogo;
- o tempo limite do tique de LEDs externos **vaza o worker de propósito**: um
  travamento de GIL sob desconexão em massa travava o laço de polling para
  sempre, e a mitigação aceita vazar uma thread para não perder o daemon.

## O que este mapa registra como dívida estrutural

1. **`lifecycle.py` tem 3.378 linhas** e é chamado de "orquestrador slim" no
   próprio cabeçalho. A extração para `subsystems/` cobriu mecanismo, não
   política: ali ainda moram `DaemonConfig`, o laço de polling, todos os
   aplicadores de perfil e o cabeamento de quatro registros.
2. **`SUBSYSTEM_REGISTRY` não é iterado em produção**
   (`daemon/subsystems/__init__.py:41`, e o próprio arquivo avisa). Quem sobe
   subsistema é `Daemon.run()`, linha a linha. Foi assim que o `BtMicSubsystem`
   nasceu órfão. Há teste travando a paridade, mas continuam **duas fontes de
   verdade**.
3. **`backend_pydualsense.py` acumula três responsabilidades**: adaptador da
   biblioteca, resolvedor de camadas de output e gerente de sessão de jogo.
4. A complexidade combinatória do modelo de precedência (6 camadas x 3 travas x
   3 origens de ativação) vive quase toda em `manager.apply` e nos
   `apply_profile_*`.
