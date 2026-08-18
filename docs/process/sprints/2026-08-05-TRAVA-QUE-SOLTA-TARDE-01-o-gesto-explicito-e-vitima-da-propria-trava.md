# TRAVA-QUE-SOLTA-TARDE-01 — o gesto explícito é vítima da própria trava

- **Achado em:** 05/08/2026, ao **restaurar o perfil dela** depois de uma
  medição de gatilho. O defeito não estava sendo procurado
- **Estado:** **CURA APLICADA**, com teste que morde
- **Gravidade:** ALTA — atinge os **dois** gestos explícitos dela, inclusive o
  PS + D-pad que ela usa dentro do jogo
- **Causa-raiz:** **PROVADA no código e MEDIDA ao vivo**, na máquina dela, com
  o daemon de produção
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Parente, e distinta:**
  [ÁUDIO-QUE-TRANCA-01](2026-08-03-AUDIO-QUE-TRANCA-01-um-toque-no-volume-congela-a-troca-de-perfil.md)
  — mesmo campo (`manual_override_categories`), defeito diferente. Ver
  *"Por que não é a ÁUDIO-QUE-TRANCA-01"*

---

## O sintoma

Ela ajusta alguma coisa na mão — um gatilho, a cor, o volume. O daemon carimba
a categoria em `manual_override_categories`, que é o desenho correto: o que ela
fez na mão sobrevive à troca automática de perfil.

Depois ela **troca de perfil de propósito** — pela janela, pela CLI ou pelo
PS + D-pad. E o perfil entra **pela metade**: o daemon responde *"ativado"*, o
nome muda, mas as categorias que ela havia tocado **não são aplicadas**.

Repetir o mesmo gesto uma segunda vez funciona. É indistinguível de
*"às vezes pega"*.

## A prova, com o daemon de produção

Journal dela, duas ativações **idênticas** do **mesmo** perfil, com um ajuste
manual de gatilho carimbado antes:

```
00:02:06  profile_apply_respeita_override_manual  categorias=['audio','trigger']
00:02:06  profile_activated  name=vitoria  origin=manual     <- pulou as duas
00:03:22  profile_activated  name=vitoria  origin=manual     <- aplicou tudo
```

**A mesma ação, repetida, com resultados diferentes.**

## A causa-raiz: a ordem

`daemon/ipc_handlers.py`, no `_handle_profile_switch`, antes desta sprint:

```python
profile = self.profile_manager.activate(name, origin="manual", ...)   # :404
save_active_marker(profile.name)
self.store.clear_manual_trigger_active()                              # :412
```

O `activate` roda **com a trava ainda armada**. Lá dentro,
`profiles/manager.py:326-348` consulta as categorias travadas e emite `None`
nos campos correspondentes do `OutputSpec` — que é o vocabulário de *"sem
opinião"*. O perfil, portanto, não escreve nada naquelas categorias.

**A trava é limpa tarde demais para a ativação que a limpou.** Ela só vale para
a próxima — e é exatamente por isso que a segunda ativação funciona.

### E a intenção contrária está escrita em TRÊS lugares

Este defeito não é uma decisão que envelheceu; é uma ordem que trai o que a
própria casa documenta:

| onde | o que promete |
|---|---|
| `state_store.clear_manual_trigger_active` (docstring) | *"Tudo: `profile.switch` explícito, hotkey de ciclo … os três são 'troquei de perfil', onde soltar as três categorias é o que a usuária pediu"* |
| `profiles/manager.py:312-313` | *"Trocar de perfil pela GUI limpa as TRÊS categorias — então isso NÃO é um estado do qual ela não consiga sair"* |
| `daemon/ipc_handlers.py:410-411` | *"Usuário escolheu perfil explícito: libera autoswitch de novo"* |

## O alcance: dois caminhos errados, um certo

| caminho | ordem | veredito |
|---|---|---|
| `ipc_handlers.py` — janela e CLI | aplicava, **depois** limpava | defeito |
| `subsystems/hotkey.py` — **PS + D-pad** | aplicava, **depois** limpava | defeito |
| `profiles/autoswitch.py:505-518` — troca automática | limpa **antes** de aplicar | **correto** |

**O caminho automático — o mais auditado desta casa — está certo, e os dois
gestos explícitos dela estavam errados.** E o comentário da hotkey dizia,
textualmente, *"paridade com `_handle_profile_switch`"*: **a paridade copiou a
ordem errada**.

### E isso derruba uma entrega declarada

`hotkey.py:132-135` justifica o `speaker_applier` assim, desde a `SOM-02/E4`:

> *"o ciclo PS+D-pad é gesto MANUAL dela — troca explícita de perfil, que limpa
> as categorias travadas (inclusive `audio`) e portanto aplica o volume do
> perfil que entra."*

**Não aplicava.** É o mesmo mecanismo que a
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md)
catalogou — a entrega escrita, testada no artefato, e nunca no encontro com o
resto do sistema.

## Por que a suíte não pegou — e é o padrão já nomeado

Dois testes cobrem esta área. Os dois ficam verdes com o produto quebrado:

- **`test_onda_u_trava_por_categoria.py:144-155`** — chama
  `store.clear_manual_trigger_active()` **à mão**, com o comentário
  `# o que profile.switch chama`, e **nunca chama `_handle_profile_switch`**.
  Ele mede o `StateStore`, não o handler;
- **`test_perfil_respeita_trava_manual.py:122-132`** — faz `clear()` e **depois**
  `apply()`. Ele **documenta a ordem certa que o produto não executava**.

Nenhum dos dois exercita o caminho real. É a *"mordida na metade errada da
cadeia"*.

## Por que não é a ÁUDIO-QUE-TRANCA-01

As duas mexem em `manual_override_categories`, e é fácil confundi-las:

- o **defeito 1** daquela é a **ausência** de `clear_manual_trigger_active("audio")`,
  e o efeito é sobre o **autoswitch**;
- **este** é sobre a **ordem** num clear que **existe** — tanto que aquela
  sprint o lista como cobertura (`ipc_handlers.py:412`, na tabela de clears).
  A medição mostra que ele não serve à ativação que o dispara.

**E este agrava a E2 daquela:** dar granularidade por categoria ao autoswitch,
como a E2 propõe, **não cura o caminho manual** — lá o problema não é
granularidade, é ordem.

## A cura aplicada

Em ambos os caminhos, o clear e o lock passam para **antes** do `activate`:

```python
travadas_antes = getattr(store, "manual_override_categories", ()) or ()
store.clear_manual_trigger_active()
store.mark_manual_profile_lock(now + MANUAL_PROFILE_LOCK_SEC)
try:
    profile = manager.activate(name, origin="manual", ...)
except Exception:
    for categoria in travadas_antes:
        store.mark_manual_trigger_active(categoria)
    raise
```

Três decisões, e cada uma tem motivo:

1. **o lock sobe junto com o clear.** Entre soltar a trava e terminar o
   `activate` não pode existir janela em que nem a trava nem o lock suprimam o
   autoswitch — seria trocar um defeito por outro (o Bug C);
2. **o restore no `except`.** Mover o clear para antes abriu uma borda que não
   existia: um `profile.switch` com nome inexistente apagaria a configuração
   que ela fez na mão. Ativação que falhou não é gesto cumprido. É a mesma
   atomicidade que a docstring do handler já prometia ao marker;
3. **`getattr` na leitura das categorias**, pelo motivo que
   `manager.py:384-387` já documenta: dublês de teste e stores parciais
   continuam funcionando, e *"não sei listar"* vira *"nada a restaurar"*.

## O teste que morde

`tests/unit/test_trava_que_solta_tarde_01.py` — seis casos, bancada hermética
(`ProfileManager` real + `StateStore` real + `FakeController` espião, sem
disco e sem hardware).

**Mordida verificada em 05/08:** com a cura arrancada (`git stash` dos dois
arquivos), **4 dos 6 reprovam**, inclusive
`test_duas_ativacoes_seguidas_sao_indistinguiveis`, que é a assinatura do
journal dela virada em asserção. Devolvida a cura, 6 verdes.

**Honestidade sobre o 5º caso:** `test_falha_na_ativacao_devolve_a_trava` passa
nos **dois** estados. Ele não morde o defeito original — protege a borda que a
*cura* introduziu (sem a cura, o clear nunca rodava no caminho de exceção, e a
trava sobrevivia por acidente). Está registrado como tal na docstring.

## O que fica ABERTO

- **a categoria `audio` continua sem clear próprio** — é o defeito 1 da
  `ÁUDIO-QUE-TRANCA-01`, e esta sprint **não o toca**. Ela só garante que o
  gesto explícito aplique o perfil inteiro;
- **o `manual_trigger_active` continua sendo booleano de tudo-ou-nada** para o
  autoswitch — a E2 da `ÁUDIO-QUE-TRANCA-01`;
- **o aceite em uso real.** A bancada prova o `OutputSpec`; que a cor e o
  gatilho do perfil entrem **na primeira** troca, no uso dela, só o uso dela
  fecha.
