# FD ZUMBI DO INIT TIMEOUT 01 — o descritor que ficou para trás

**15/08/2026.** Defeito **visto na máquina dela** durante a investigação do
co-op, confirmado no `/proc` do daemon vivo, rastreado no fonte, medido no
journal e **curado com teste que morde**. Nenhuma unit foi parada, nada foi
escrito no aparelho.

---

## 1. O que se viu

Ao inspecionar `/proc/<pid-do-daemon>/fd`, apareceu um descritor para
**`/dev/hidraw8 (deleted)`** — um nó que já não existe. Aberto às **06:29:45**,
o mesmo instante em que o journal registra:

```
2026-08-15T06:29:45.254687 [warning] pydualsense_init_timeout — kernel pode
estar bloqueado em hidraw (hid_playstation conflict) path=b'/dev/hidraw8'
timeout_sec=5.0
```

e ainda aberto **mais de uma hora depois**, no mesmo processo (pid 1597, de pé
desde as 03:44:08 — não houve restart entre a abertura e a observação).

**O que se viu DEPOIS, e que corrige a leitura ingênua:** na reconferência
(08:33) o descritor **já não estava lá**, e não havia nenhuma thread
`hefesto-ds-init` viva. Ou seja: naquele caso o vazamento foi **transitório** —
durou o tempo que o kernel levou para destravar, e o coletor do Python fechou o
fd por tabela. O vazamento é real; o que ele **não** é, é sempre permanente. A
seção 3 separa os dois desfechos, porque a diferença entre eles é a diferença
entre "incômodo" e "o produto escrevendo num controle que ele não sabe que
abriu".

---

## 2. O caminho, no fonte

`PyDualSenseController._open_one`
(`src/hefesto_dualsense4unix/core/backend_pydualsense.py:1616`) roda `ds.init()`
numa thread daemon com teto de `INIT_TIMEOUT_SEC` (5 s por padrão). Se o join
estoura, ela logava o aviso e devolvia `None` — **sem mais ninguém no processo
segurando o `ds`**.

O fd nasce **dentro** desse `init()`. A cadeia é:

```
_open_one
  -> ds.init()                                   (upstream, pydualsense.py:118)
       -> self.__find_device()
            -> _PinnedPyDualSense._pydualsense__find_device   (backend:565)
                 -> hidapi.Device(path=...)      -> hid_open_path -> open(2)  <-- o fd
       -> self.determineConnectionType()         -> self.device.read(100)     <-- pendura aqui
       -> self.report_thread.start()             (upstream, pydualsense.py:140)
```

Isto é, no instante do timeout **o descritor já existe** e quem o segura é um
objeto que a função acabou de largar. O `_PinnedPyDualSense` já tinha `close()`
com teto (QUEDA-QUE-PENDURA-01, `backend:697`) — só que ninguém o chamava neste
ramo.

---

## 3. Os dois desfechos, e por que o segundo é o grave

**(a) O `init()` termina com ERRO depois do timeout.** O `ds` fica sem
referência, e o fd só volta quando o coletor destrói o objeto
(`hidapi.Device.__del__`). Foi o caso de hoje: mais de uma hora com o fd preso,
e depois liberado sozinho. Custo: um fd por evento, por tempo indeterminado.

**(b) O `init()` termina BEM depois do timeout.** Este é o grave. A última linha
do `init()` do upstream sobe o `report_thread`, e essa thread segura o `ds` vivo
**para sempre** (`while self.ds_thread`). Nasce um **zumbi**: um handle que
escreve report de output num controle real e que **o backend nem sabe que
abriu**, porque nunca entrou no `self._handles`. Nada o alcança — nem o
`_refresh_sysfs_leds`, nem o mute de Modo Nativo (`backend:1743`), nem o
`_close_handles`: os três só varrem `self._handles`.

Este zumbi **não é novidade da casa** — o comentário do `_suppress_leds`
(`backend:459`) já o citava por nome: *"inclusive o zumbi do init-timeout, que
nenhum refresh alcança"*. A casa sabia; o produto não fazia nada. Nasceu
suprimido de LED, e só.

---

## 4. O dano real, medido — sem exagerar

| Grandeza | Medida |
|---|---|
| fds por evento | **1** (mais 1 thread) |
| Teto de fds do daemon | **1024** (soft; hard 1048576) |
| Em uso agora | **64** — ou seja, ~960 de folga |
| Eventos nos últimos 7 dias | **67** |
| Eventos nos últimos 30 dias | **68** (o journal só alcança 08/08) |

**A frequência média engana, e por isso não é o número que decide.** Os eventos
não se espalham: eles vêm em **tempestade**, sempre no mesmo nó, retentando a
cada ~10 s. Por vida de daemon:

| Dia | pid | nó | eventos |
|---|---|---|---|
| 10/08 | 3704654 | `/dev/hidraw1` | **23** |
| 10/08 | 3708007 | `/dev/hidraw1` | 11 |
| 10/08 | 3699221 | `/dev/hidraw1` | 9 |
| 10/08 | 3383851 | `/dev/hidraw0` | 9 |
| 08/08 | 2235636 | `/dev/hidraw0` | 7 |
| 15/08 | 1597 | `/dev/hidraw8` | 1 |

**A conta honesta.** Pior tempestade observada: 23 eventos numa vida de daemon.
Com ~960 fds de folga, seriam precisas ~42 tempestades daquele tamanho **na
mesma vida do processo** para bater no teto. Na cadência de 10/08 (~10 s por
retentativa) isso é da ordem de **duas a três horas de tempestade
ininterrupta** — possível, mas nunca observado. Fora de tempestade, com ~10
eventos por dia no pior dia medido, **o teto levaria meses**, e o daemon
reinicia muito antes disso.

**Dito na cara: pelo lado do esgotamento de fds, isto não era urgência.** O que
justifica o conserto é o desfecho (b) — um handle órfão escrevendo num controle
da mesa dela sem o backend saber, imune ao mute de Modo Nativo. Esse não tem
teto nem cronômetro: basta acontecer uma vez.

---

## 5. A cura

Um **handoff atômico** em `_open_one`: caller e runner decidem **sob o mesmo
lock** de quem é o handle. Quem perde a posse, fecha.

- Não dá para decidir por `t.is_alive()`: entre o `is_alive()` dizer "viva" e o
  `return None` cabe o runner terminar o `init()`, e aí ninguém fecha o handle
  que ninguém recebeu. A decisão virou um estado (`terminou` / `desistido`) lido
  e escrito só dentro do lock.
- O `close()` roda **na thread do runner**, depois que o `init()` voltou —
  nunca por cima de um `hid_read` em curso, que seria puxar o `hid_device`
  debaixo de quem está lendo.
- O `close()` da subclasse já derruba o `report_thread` com teto, o que mata o
  desfecho (b) junto com o fd.
- Um aviso novo, `pydualsense_init_orfao_fechado`, deixa o evento medível no
  journal da próxima vez.

### O que NÃO foi fechado, e por quê

**O ramo do `init()` que nunca volta.** Se a thread segue pendurada em D-state
para sempre, o fd continua preso — e tem de continuar. Fechá-lo de fora seria
fechar o descritor debaixo de um `hid_read` ativo. Esse caso se resolve sozinho
quando o kernel destrava, que foi exatamente o que se observou hoje.

**Nada do que o produto usa.** A separação é estrutural, não estatística: o `ds`
do `_open_one` é local e **só chega ao `self._handles` pelo `connect()` depois
que a função retorna o handle**. No ramo do timeout ela retorna `None` — o
handle que a thread fecha nunca foi visto por ninguém. E cada `hidapi.Device`
faz o **seu** `open()` do nó, então o fd fechado é o desta tentativa, e não o de
um handle vivo que por acaso aponte para o mesmo `/dev/hidrawN`. Isto importa
porque **fd já aberto sobrevive ao `hide` do broker**: é assim que o produto
mantém acesso ao nó escondido, e fechar no ramo errado quebraria o controle em
produção.

---

## 6. A mordida

`tests/unit/test_backend_init_timeout_nao_vaza_fd.py`, cinco testes.

**Os testes não usam flag `fechado = True`.** Flag prova que alguém chamou
`close()`, não que o descritor voltou — e é o descritor que vazava. O dublê abre
um `os.pipe()` de verdade dentro do `init()` (a mesma ordem do `hidapi`) e fica
com a ponta de escrita; o teste fica com a de leitura, não-bloqueante. Enquanto
houver escritor vivo, ler dá `BlockingIOError`; quando a ponta fecha **de
verdade**, a leitura devolve `b""`. **É o kernel que responde, não o dublê.**

Prova nos dois lados, com a cura arrancada e devolvida:

| Teste | Com a cura | Sem a cura |
|---|---|---|
| `..._termina_depois_do_timeout_devolve_o_fd` (o zumbi) | passa | **reprova** |
| `..._estoura_e_depois_falha_tambem_devolve_o_fd` | passa | **reprova** |
| `test_handle_nunca_e_entregue_e_fechado_ao_mesmo_tempo` (borda, 40x) | passa | **reprova** |
| `test_init_rapido_nao_fecha_o_handle_entregue` (protege a mesa) | passa | passa |
| `test_excecao_dentro_do_prazo_continua_propagando` | passa | passa |

Os dois últimos passam nos dois lados **de propósito**: eles não guardam a cura,
guardam contra ela. São o contrapeso que reprovaria se o conserto fechasse
demais.

---

## 7. Estado

Curado na árvore. **A cura só vale no próximo start do daemon** — o daemon vivo
é mais velho que o código, e nada foi reiniciado: a mesa dela estava de pé (dois
controles no cabo, dois no rádio).

Portões: `ruff check src/ tests/` limpo, `mypy src/hefesto_dualsense4unix` sem
achados em 174 arquivos, e 108 verdes nas suítes vizinhas do backend.
