# POR UNIDADE — o override por peça deixa de ser só luz e gatilho

- **Escrito em:** 10/08/2026, na branch `restauro/inicio-da-sessao`
- **Nasceu de:** *"se eu quiser fazer uma guia específica do perfil x pro
  controle branco e outra pro mesmo perfil mas pra um controle preto ele vai
  funcionar pra cada um deles dessa forma."* — e, perguntada sobre quais
  seções: **todas as abas**.
- **Status:** **ENTREGUE EM CÓDIGO — AGUARDANDO O OLHO DELA** (PROVA-DE-TELA-01:
  a palavra final é dela, com foto antes e depois)
- **Grau:** MEDIDO — quatro curas arrancadas do arquivo e vistas reprovar

---

## 1. Não era construção do zero

O mapa `Profile.controllers` (chave = MAC normalizado, 12 hex) existe desde o
PERFIL-02, está **vivo** — 4 dos 14 perfis dela já têm bloco `controllers` para
duas unidades distintas — e já tinha as cinco camadas prontas: escrita pela
janela, leitura na ativação, leitura no "Aplicar", merge POR CAMPO no backend e
a omissão que protege o downgrade.

O que faltava era **alcance**. Só `leds` e `triggers` entravam. Esta entrega
estende, no molde, sem inventar mecanismo novo.

## 2. O levantamento: o que cabe por unidade, e o que não cabe

A pergunta não é "dá para guardar o campo?" — dá sempre. É **"duas unidades
pedindo coisas diferentes têm uma resposta honesta?"**

| Aba | Seção do perfil | Cabe por peça? | Por quê |
|---|---|---|---|
| Lightbar | `leds` | **JÁ CABIA** | cada peça tem a sua barra |
| Gatilhos | `triggers` | **JÁ CABIA** | cada peça tem os seus dois gatilhos |
| Rumble | `rumble.policy` / `custom_mult` | **CABE — ENTREGUE** | cada peça tem os seus dois motores |
| Status (card) | `speaker` | **CABE — ENTREGUE** | cada peça tem o seu alto-falante |
| Rumble | `rumble.passthrough` | **NÃO** | não descreve a peça: descreve **quem manda na vibração agora**. Ele solta o rumble que a GUI TRAVOU, e a trava (`DaemonConfig.rumble_active`) é **uma só** para o daemon inteiro |
| Rumble | `rumble.policy = "auto"` | **NÃO** | o `auto` escala pela **bateria**, e quem a lê é `core.rumble._effective_mult` a partir do controle **primário**. Aceitá-lo por peça faria as duas escalarem pela bateria da mesma |
| Início / Emulação | `mode`, máscara, co-op | **NÃO** | **decisão dela, 10/08/2026**: modo e máscara são da **sessão**, não da peça de plástico |
| Início | `suppress_desktop_emulation` | **NÃO** | irmão do `mode` pelo mesmo eixo — ele cala a emulação **do desktop**, que é uma |
| Navegação | `mouse`, `key_bindings` | **NÃO (medido)** | ver §3 |
| Card / Navegação | `mic.button_toggles_system` | **NÃO (medido)** | ver §3 |
| Perfis | `name`, `match`, `priority` | **NÃO** | é a identidade do perfil, não configuração de peça |
| Sistema | — | **N/A** | não é seção de perfil |

## 3. As duas recusas que são MEDIÇÃO, não opinião

Estas duas eu não decidi — o código já tinha decidido, e está escrito nele.

**Mouse e teclado.** `PyDualSenseController.read_state`, linha 1986:

> `# INPUT vem SEMPRE do controle PRIMÁRIO (self._ds). Emulação de
> mouse/teclado/gamepad é, portanto, single-controller por construção.`

Há **um** `_mouse_device` e **um** `_keyboard_device` no daemon, alimentados por
um `read_state()` por tick do poll loop. Guardar `mouse.speed` por unidade
guardaria um número que ninguém lê — a classe de defeito mais cara desta casa
(*a cura escrita e nunca ligada*), cometida de propósito.

**Microfone.** O `EventTopic.BUTTON_DOWN` publica `{"button", "pressed"}` e
**não carrega `uniq`** (`lifecycle.py:4047`), então o laço do mic não tem como
saber de qual peça veio o toque. Somado: o alvo do gesto é o microfone **padrão
do sistema**, que é um só — e o handler já só age quando a fonte padrão É o
controle (BT-E-VPAD-01).

Quando esses dias chegarem, o que falta **não é o campo do perfil**: é
identidade por peça chegando ao pipeline de input e ao barramento.

## 4. As curas que já estavam escritas e nunca ligadas

As duas seções entregues saíram baratas porque a fiação por-`uniq` já existia
inteira e ninguém a tinha ligado ao perfil:

| já existia | onde | usado por quem, até hoje |
|---|---|---|
| `set_rumble_for(uniq, weak, strong)` | `core/backend_pydualsense.py` | **só o co-op** |
| `apply_speaker(profile, uniq=...)` | `profiles/manager.py` | só o replug (`reapply_speaker_on_connect`) |
| `apply_profile_speaker(..., uniq=...)` | `daemon/lifecycle.py` | ninguém passava `uniq` na ativação |
| `speaker.set` / `mic.set` com `uniq` | `daemon/ipc_handlers.py` | a GUI, ao vivo — o perfil não tinha onde guardar |

## 5. Como a vibração por peça chega ao hardware

O valor que chega ao `set_rumble` **já vem escalado pela política global**
(`apply_rumble_policy`, em todo caminho de rumble). Então o que a peça registra
é um **fator relativo** — `mult_da_peça / mult_global` —, exatamente como a
escala de brilho do R-20 faz com a cor resolvida. Registrar o absoluto
escalaria duas vezes: a peça em "max" dentro de um perfil "economia" ficaria
mais **fraca** que a que não opinou.

O fator mora no backend (`_rumble_scale_by_uniq`, irmão de
`_led_scale_by_uniq`) e é aplicado na **saída de cada handle** —
`_for_each_com_key` é o `_for_each` de sempre, com a key entregue à operação.

Com o global em `auto`, o denominador muda a cada tick: a entrada é **pulada**,
com log. Prometer um fator contra denominador móvel seria pior do que não
entregar.

## 6. O risco central: o DOWNGRADE, não o perfil antigo

`ControllerOverrides` tem `extra="forbid"`. O perigo **não** é o perfil velho
(que valida normal sem a chave nova) — é o **perfil novo lido por um hefesto
velho**: uma chave desconhecida rejeita o `Profile` **INTEIRO**, não a seção.
Voltar uma versão viraria "todos os perfis dela quebrados", inclusive os quatro
que já têm bloco `controllers`.

O antídoto já estava no lugar (`exclude_unset=True` por entrada em
`save_profile`) e a regra é **manter a omissão e nunca semear campo novo por
default no rascunho**. Os dois lados têm portão:

- `test_a_peca_que_so_opina_sobre_luz_nao_ganha_as_chaves_novas` — o disco;
- `test_o_rascunho_intocado_nao_semeia_campo_novo` — a borda de cima.

Arrancar o `exclude_unset=True` faz o primeiro reprovar mostrando o veneno
literal: `{'leds': {...}, 'triggers': None, 'rumble': None, 'speaker': None}`.

## 7. Onde a janela escreve

**O seletor de alvo é a autoridade** — o mesmo `_edit_target_uniq` que a
Lightbar e os Gatilhos já obedecem, com o mesmo selo dizendo qual peça está
sendo editada. A aba Rumble entrou na lista do `_refresh_target_tabs`.

Para o som (que mora no card, e o card sempre soube o próprio `uniq`), a
alternativa "deduzir a peça do card em que ela encostou" foi **medida e
recusada**: com um controle só, todo gesto de volume viraria override por MAC e
a seção global nunca mais seria escrita —
`test_a_secao_do_alto_falante_so_viaja_quando_ela_mexeu_no_som` reprovou
exatamente isso, ao vivo, durante esta entrega. O card diz *de quem foi o
gesto*; o seletor diz *para quem ela quer que valha*, e é essa a pergunta.

**Limite honesto da aba Rumble:** o `rumble.policy_set` que sai ao clicar é
GLOBAL — não existe IPC de política por unidade, e inventar um seria mecanismo
novo. Com uma peça selecionada, o que ela **ouve na hora** é o global; o que ela
**salva** é da peça, e chega ao hardware pelo "Aplicar" e pela ativação.

## 8. NOTA DATADA — os controles EXTERNOS ficam de fora (10/08/2026)

Decisão dela, textual: *"por enquanto não, mas deixe anotado que em breve sim,
após fazermos o mapa de specs completo"*.

Então: **não se construiu nada para externo**, e o caminho fica aberto. O que
faltará quando eles entrarem, para não se reaprender:

1. **Endereço estável.** O validador de `controllers` recusa `uniq` degenerado —
   OUI `00:00:00` e broadcast — porque **medido ao vivo**, o Pro Controller
   reporta `000000000001`, **idêntico entre unidades**. Sem endereço próprio não
   existe "este controle": o override miraria os dois. É o primeiro requisito, e
   ele não é nosso — é do aparelho.
2. **Saber o que a peça TEM.** O 8BitDo não tem lightbar de barra nem gatilho
   adaptativo; o Pro Controller não tem alto-falante. Um override de `speaker`
   num controle sem alto-falante é uma opinião que nunca vira efeito. O
   `docs/protocol/externos-referencia-canonica.md` e o mapa de canais (a frente
   de 10/08) são o inventário que responde isso — é literalmente o *"mapa de
   specs completo"* que ela condicionou.
3. **Onde escrever.** Os externos passam por `subsystems/external_identity.py` e
   `external_mask.py`, não pelo `_handles` do backend do DualSense. As duas
   rotas por-`uniq` desta entrega (`set_rumble_scales`, `set_speaker_volume`)
   falam com handles pydualsense; para externo, cada uma precisa de uma rota
   equivalente, ou de um `IController` que as absorva.
4. **A recusa continua valendo.** Modo, máscara, mouse, teclado e mic **não
   passam a caber** por serem externos — as razões do §2 e do §3 são de
   arquitetura, não de marca.

## 9. Arquivos

| arquivo | o que mudou |
|---|---|
| `profiles/schema.py` | `ControllerRumbleOverride` (novo); `ControllerOverrides` ganha `rumble` e `speaker`; as recusas documentadas na classe |
| `core/backend_pydualsense.py` | `_rumble_scale_by_uniq`, `set_rumble_scales`, `_escalar_rumble`, `_for_each_com_key`; `set_rumble`/`set_rumble_for` escalam |
| `profiles/manager.py` | `_controllers_to_rumble_scales`, `_mult_da_politica`, `apply_controller_speakers`; ativação publica a escala e aplica o som por peça |
| `app/draft_config.py` | `effective_rumble_for`/`with_controller_rumble`, `effective_speaker_for`/`with_controller_speaker`, `_override_vazio`; `_controllers_to_ipc` emite as duas seções; `registrar_alto_falante_no_rascunho` ganha `uniq` |
| `app/actions/rumble_actions.py` | `_gravar_intensidade_no_rascunho` + `_rumble_edit_uniq`; a aba exibe o efetivo do alvo |
| `app/actions/status_actions.py` | a aba Rumble entra no `_refresh_target_tabs` |
| `app/widgets/controller_card.py` | o card passa o próprio `uniq` ao registrar o som |
| `daemon/ipc_draft_applier.py` | `_publicar_escalas_de_vibracao`, `_escrever_alto_falantes_por_unidade` |
| `tests/unit/test_por_unidade_01_todas_as_abas.py` | 22 testes, cada um com a sua mordida escrita no corpo |

## 10. As mordidas, provadas

| cura arrancada DO ARQUIVO | teste que reprovou |
|---|---|
| `_escalar_rumble` no `set_rumble` | `test_a_peca_com_intensidade_propria_vibra_diferente_da_outra` |
| `exclude_unset=True` no `save_profile` | `test_a_peca_que_so_opina_sobre_luz_nao_ganha_as_chaves_novas` **e** `test_o_rascunho_intocado_nao_semeia_campo_novo` |
| o `secao is None: continue` do `apply_controller_speakers` | `test_a_peca_sem_secao_de_som_nao_escreve_nada` |
| o laço inteiro do `apply_controller_speakers` | `test_cada_peca_recebe_o_proprio_volume_na_ativacao` |

Cada arquivo foi restaurado e conferido byte a byte (`diff` limpo) depois de
cada mordida.
