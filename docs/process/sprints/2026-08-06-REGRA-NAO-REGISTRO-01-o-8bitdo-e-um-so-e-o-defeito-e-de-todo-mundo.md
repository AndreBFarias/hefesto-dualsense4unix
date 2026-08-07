# REGRA-NAO-REGISTRO-01 — o 8BitDo é um só, e o defeito é de todo mundo

- **Status:** PROPOSTA, escrita em 06/08/2026. Nenhuma linha de `src/` ou de
  `tests/` foi tocada
- **Prioridade:** ALTA — não pelo tamanho do dano, pelo alcance: **qualquer
  pessoa que tenha um 8BitDo cai nisto no primeiro dia**, com um registro
  recém-nascido
- **Gravidade do sintoma:** MÉDIA (ver *"O que o fantasma faz de verdade"* — o
  sintoma que a `IDENTIDADE-DUPLA-01` descreve já foi curado pela `NUM-01`)
- **Causa-raiz:** **PROVADA no código**; a propriedade do firmware que a
  dispara é MEDIDA em uma unidade
- **Substitui, como desenho:**
  [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)
  — aquela sprint continua sendo a **descoberta**; esta é a **cura**, e corrige
  duas premissas dela por nota datada, sem apagar nada
- **Parente, e distinta:**
  [IDENT-01](2026-07-25-IDENT-01-um-controle-duas-identidades.md) — mesma
  pergunta ("um controle, duas identidades"), objeção diferente e ainda de pé
- **Pré-requisito de HONESTIDADE, não de código:**
  [NOME-HONESTO-01](2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md)
  — ver *"O que esta sprint NÃO resolve"*, item 6
- **Fecho de tela:**
  [PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)

---

## A pergunta dela, que reordenou o desenho

Em 06/08/2026, mapeando os controles físicos dela:

Citação **literal**, como ela escreveu — inclusive sem os acentos. Citação não
se corrige.

> *"to mapeando os meus controles fisicos, mas se por exemplo outro amigo meu
> com os 4 controles iguais aos meus (deles, nao os meus de fato) — ele vai usar <!-- noqa-acento -->
> o mesmo app e vai funcionar la tambem?"* <!-- noqa-acento -->

Essa pergunta não pediu uma resposta. Ela **reprovou um desenho** — o que estava
na mesa até aquele momento — antes que ele custasse trabalho. É o item mais
valioso desta sprint, e vem antes de tudo o que está escrito abaixo.

## O inventário físico, confirmado por ela

| plástico | o que é | quantos rostos |
|---|---|---|
| **8BitDo Pro** (OUI `e4:17:d8`) | **UM** controle, com **DOIS modos**: Pro Controller (Nintendo) e PS4 | dois endereços de hardware + um sintético no cabo |
| **Pro Controller** (OUI `e0:f6:b5`) | Nintendo genuíno | um |
| **DualSense** | Sony | um |
| **DualSense** (segundo) | Sony | um |

**Quatro controles. Cinco entradas no registro dela.** O 8BitDo é **um só
plástico** — isto foi ela quem confirmou, e é o fato que a sprint anterior
tratava como hipótese.

---

## A resposta direta à pergunta dela

**O app funciona na máquina do amigo. O que não viaja é o registro — e o defeito
viaja junto com o firmware do controle.** GRAU: MEDIDO.

O código é idêntico em qualquer máquina. A identidade de um externo é a string
do endereço normalizado, e a fila mora em `config_dir()/controllers.json`, isto
é, por-usuária e por-máquina (`daemon/subsystems/external_identity.py`, método
`_path`, e o espelho em `identity.py`). Quem decide o que restaurar é
`CONTROLLERS_SCHEMA_VERSION` (`identity.py:194`, hoje **3**); o `boot_id` é só
anotação desde a R-23.

Consequência que reordena o trabalho: **qualquer cura por DECLARAÇÃO só existe
na máquina onde alguém declarou.** O 8BitDo do amigo tem o mesmo OUI e sufixo
diferente — nenhuma declaração dela alcança o aparelho dele. **O que viaja é
código.**

E há uma parte que **não viaja e ela vai sentir**, que é grande demais para
ficar implícita: `Profile.controllers` é `dict[str, ControllerOverrides]`
chaveado por MAC de 12 dígitos, com validador que reprova chave que não seja MAC
(`profiles/schema.py:549`, validador em `:617-656`). O **mapeamento de botões
viaja** (é do perfil); o **ajuste por controle** (saída, lightbar, alto-falante)
casa com os aparelhos DELA e fica inerte na máquina dele. GRAU: MEDIDO.

---

## O que está MEDIDO sobre o modelo de identidade

Tudo abaixo foi conferido contra a árvore de 06/08/2026 (`ae32c10`).

### 1. A chave não é o `uniq` cru — são duas funções em série

**(a)** `identity_for_entry` (`external_identity.py:270`) é a fonte ÚNICA da
string com que o projeto numera um externo, e tem três degraus: o campo
`identity` já carimbado no payload (contrato de fio — a janela não tem sysfs);
`_external_dedup_key` (`core/evdev_reader.py`), que devolve o MAC normalizado,
ou `dev:<instância HID do sysfs>`, ou `path:<node>`; e, sem VID/PID legíveis, o
MAC canônico.

**(b)** `_canonical` (`external_identity.py:375`) devolve `(key, persistível)`:
casa `_MAC_RE` (`:106`), minúscula sem separadores, e
`persistível = not _is_synthesized_mac(key)`. E `_is_synthesized_mac` (`:184`) é
**literalmente `key[:2] == "02"`** (`_SYNTHESIZED_MAC_FIRST_OCTET`, `:138`).

**O que isso resolve, e o que NÃO resolve.** Cobre exatamente um caso: o
endereço que o nosso DKMS fabrica no `usb_probe_degrade` e o `02:fe:` do vpad.
**Não vê nada de endereço de hardware.** Um MAC real começa pelo OUI do
fabricante, nunca por `02` — logo os **dois** endereços do 8BitDo são
`persistível=True` e **os dois vão ao disco**. GRAU: MEDIDO.

### 2. A fila no disco, e os três buracos da poda

O `controllers.json` versão 3 é `{"version", "boot_id", "order"}`, com `order`
= lista de `{"addr", "kind", "rank"}` — fila ÚNICA, lida por `order_entries`
(`identity.py:279`) e reescrita por `merged_order_payload` (`:316`), cada lado
preservando as entradas do `kind` do outro.

1. `_prune_volatile_locked` (`external_identity.py:550`) solta o lugar de
   identidade **volátil** ausente após `VOLATILE_ABSENCE_LIMIT = 2` (`:147`).
   **Só volátil.** MAC de hardware ausente nunca é podado — é a assimetria
   deliberada do MODO-01, o ID documentado no cabeçalho daquele módulo.
2. O `load` (`:644`) descarta do disco entradas não-persistíveis e marca
   `_dirty` para reescrever o arquivo sem elas (`:715-728`) — a **migração sem
   bump de versão** que esta sprint vai reusar.
3. **Não existe teto no lado externo.** `_MAX_PERSISTED_SLOTS = 16`
   (`identity.py:215`) é aplicado **só** em `identity.py:896`; `grep` confirma
   que a constante não aparece em `external_identity.py`. A fila de externos
   cresce sem limite: cada modo novo, cada pareamento novo, é entrada
   permanente. GRAU: MEDIDO.

### 3. Não existe, hoje, nenhuma detecção de exclusão mútua

`grep` por `exclusao|mutu|irmao|sibling|alias|mesmo aparelho|gemeo` em `src/`
devolve **zero** ocorrências ligadas a identidade de controle. O registro **nem
vê** os campos que permitiriam suspeitar: `slot_for` (`external_identity.py:473`)
recebe **uma string**. Nome, VID, PID, bus e driver existem no tick
(`ExternalLedSync.tick`, `:1099`, que já monta `identidades` em `:1128` e chama
`sync_connected` em `:1129`) e **não são passados adiante**. GRAU: MEDIDO.

### 4. O que o fantasma faz de verdade — e não é o que a sprint anterior diz

**O fantasma AUSENTE não infla o número exibido.** `_posicao_locked`
(`external_identity.py:455`) conta **só quem está em `_connected`**, mais os
lugares dos DualSense presentes; o espelho do outro lado é `identity.py:646`.
Isso é cura da `NUM-01` (25/07). Disco em 3/4/5, tela em 2/3. GRAU: MEDIDO.

O que sobrou do fantasma, e é o defeito real:

- **infla o lugar de quem chega depois.** `slot_for:501` faz
  `max([*ocupados, int(reserve), 0]) + 1` sobre `_ordem` **inteiro** (presentes
  e ausentes), e o lado DualSense une esses lugares na própria conta
  (`_assign_locked`, `identity.py:586`, que faz `ocupados |= _extra_reserved()`).
  GRAU: MEDIDO;
- **inverte a ordem** entre o 8BitDo e um controle adotado **entre** os dois
  modos. Com o rosto A em 4, um Pro adotado em 5 e o rosto B nascendo em 6: no
  modo A o 8BitDo vem antes do Pro; no modo B, depois. Mesmo plástico, mesma
  mesa, ordem trocada. GRAU: SUSPEITA COM MECANISMO (derivada das funções
  acima, não observada no journal);
- é **permanente** e **sem teto** (buraco 3 acima).

### 5. Correção de premissa: os dois endereços nunca estiveram ativos juntos

A `IDENTIDADE-DUPLA-01` afirma que o journal tem escritas de LED para **ambos**
no mesmo período (23:49 até 00:01) e usa isso contra o critério "nunca
simultâneos". **Não é o que o journal diz, e dois leitores independentes
mediram o mesmo.** Naquela janela o segundo escritor de LED é a identidade
**sintética** do mesmo plástico no cabo, não o outro MAC de hardware; a linha
com três endereços que a sprint cita é `external_fila_restaurada`
(`external_identity.py:730`), que imprime a fila **persistida em disco**,
ausentes inclusive — não presença. Varrendo o journal de 27/07 a 06/08, os dois
endereços de hardware do 8BitDo **nunca escreveram LED no mesmo tick**.
GRAU: MEDIDO.

Consequência: **o critério "nunca simultâneos" não está refutado.** A objeção
que continua de pé é a da `IDENT-01` — *verdadeiro, mas insuficiente: um
aparelho ausente pode simplesmente estar desligado* — e essa é de
**suficiência**, não de contradição empírica. Esta sprint não a refuta; ela a
**desarma**, tornando o custo do erro menor que o custo de não agir.

### 6. São TRÊS rostos, não dois

| rosto | modo / transporte | classe da identidade | destino hoje |
|---|---|---|---|
| endereço 1 | Switch, Bluetooth | MAC de hardware | **persistido** |
| endereço 2 | PS4, Bluetooth | MAC de hardware | **persistido** |
| endereço 3 | PS4, **cabo** | sintética (`02` + VID + PID + bus) | volátil, some sozinha |

O terceiro já é coberto pelo MODO-01. **Os dois primeiros não são cobertos por
nada.** GRAU: MEDIDO.

### 7. A trava de teste que qualquer cura terá de encarar — e a que passa com o defeito vivo

- `tests/unit/test_external_identity.py:703` —
  `test_dois_aparelhos_do_mesmo_oui_nunca_se_fundem` proíbe explicitamente
  herdar lugar por OUI. **Esta cura passa nele sem tocar uma linha**, e isso é
  argumento a favor dela, não coincidência.
- `tests/unit/test_external_identity.py:722` —
  `test_quatro_controles_e_o_fantasma_do_outro_modo_ninguem_no_slot_5` diz na
  docstring que reproduz *"o cenário MEDIDO ao vivo"*, mas o fantasma que ele
  monta é `_KEY_SINTETIZADO` (`:603`), ou seja, a identidade **sintética**. Ele
  testa o MODO-01. **O teste passa hoje e o defeito continua vivo.**
  GRAU: MEDIDO.

---

## Por que a cura por REGISTRO foi descartada

### Nota datada — 06/08/2026

**A ficha da varredura anterior propunha exatamente o desenho errado:**
*declaração de identidades irmãs, gesto na janela, desfazer.* Aquela proposta
não era burra e não se apaga: ela era **correta para a máquina dela**, resolvia
o caso medido, e tinha um gesto de reparo explícito.

**O que a fez caducar foi a pergunta dela, e só ela.** Um registro —
"estes dois endereços são o mesmo plástico" — vive em
`~/.config/hefesto-dualsense4unix/`, isto é, **só existe na máquina onde alguém
declarou**. O amigo dela, com um 8BitDo do mesmo modelo e sufixo diferente,
liga o controle no primeiro dia, troca de modo, e cai no defeito **sem nada
declarado**. Uma cura que precisa de declaração prévia é, por construção, uma
cura que nunca chega em quem mais precisa dela: quem está começando.

Um segundo desenho foi considerado e também recusado: **o produto detecta e
PERGUNTA a ela** (faixa na Home, "é o mesmo controle?" / "são dois"). Ele é
melhor que a declaração pura — a detecção viaja —, mas a **resolução** não:

1. a pergunta é **irrespondível** na máquina do desconhecido enquanto a tela
   mentir o fabricante. `_BRAND_BY_OUI` tem **um** item
   (`app/actions/external_controllers.py:64`), o OUI desta casa. Fora daqui o
   mesmo plástico se chama "Sony" num modo e "Nintendo" no outro, e a faixa
   pergunta *"Sony entrou como novo, é o mesmo que o Nintendo 2?"* — uma
   pergunta que ninguém sabe responder, e cuja resposta errada é **persistida**;
2. o "são dois" fica **irreversível sem terminal**: vai para o disco, o produto
   promete não perguntar de novo, e cumpre. Um toque errado tranca a cura
   naquela máquina para sempre, e o conserto é apagar um JSON à mão.

**O critério que sobrou, e que esta sprint obedece:** a cura tem de ser uma
**regra que reconhece o padrão sozinha, em qualquer máquina, no primeiro boot**,
sem que ninguém declare, confirme ou clique em nada.

---

## A regra escolhida

Nome de trabalho do sinal: **revezamento**. O nome é do *fenômeno observado*
(dois endereços que se revezam na mesa), nunca da conclusão ("são irmãos") — e é
isso que separa esta proposta da que ela derrubou. O produto **nunca vai afirmar**
que dois endereços são o mesmo plástico. Ele vai dizer que eles **dividem um
lugar na fila**, que é uma afirmação sobre numeração, não sobre matéria.

### Em uma frase que cabe num comentário de código

```
# REGRA-NAO-REGISTRO-01: duas identidades de HARDWARE do mesmo OUI que se
# REVEZAM na mesa (uma sai SOZINHA, a outra entra SOZINHA, sem ninguém do
# mesmo OUI mudando de presença no meio) e que se apresentam com VID:PID
# DIFERENTES passam a DIVIDIR um lugar na fila. Nenhum rosto é apagado,
# nunca. E a divisão morre, para sempre, no primeiro tick em que os dois
# aparecem JUNTOS.
```

### As quatro condições, e por que cada uma existe

| condição | o que ela compra | GRAU |
|---|---|---|
| as duas chaves são **MAC de hardware** (`_MAC_RE` e **não** `_is_synthesized_mac`) | não pisa no MODO-01, que já cura a identidade sintética | MEDIDO |
| **mesmo OUI** (`key[:6]`) | necessária, jamais suficiente. Sem ela, um Pro Controller e um 8BitDo que a pessoa usa alternadamente virariam candidatos — e esse é o arranjo mais comum que existe | MEDIDO na unidade dela, **n=1** / SEM PROVA como propriedade do modelo |
| **VID:PID DIFERENTES** | é o que torna **estruturalmente impossível** fundir duas unidades do mesmo modelo. O 8BitDo troca de VID:PID junto com o endereço; dois 8BitDo idênticos do amigo, no mesmo modo, têm **o mesmo** VID:PID e nunca são candidatos | MEDIDO (`docs/usage/troubleshooting-8bitdo.md`, tabela de modos) |
| **revezamento observado** (positivo, nunca por ausência) | nunca se divide lugar por **falta** de prova; divide-se por **prova de troca**. É isto que faz a regra valer no primeiro dia de qualquer máquina | desenho |

**Sobre o "mesmo OUI", com a honestidade que a casa cobra:** o que está medido é
que os dois endereços do 8BitDo **dela** compartilham o OUI — uma unidade, um
lote, uma máquina. Não está provado que todo 8BitDo faça isso. Se algum não
fizer, a regra **falha fechada**: não há candidato, não há divisão, e o
comportamento é exatamente o de hoje. Perda, nunca dano. E não dá para usar
"outros lotes existem" como defeito no item 6 e "MEDIDO" na tabela aqui, para o
mesmo fato.

### "Revezamento" definido sobre EVENTO, nunca sobre relógio

No tick `t`, `A` foi a **única** chave daquele OUI a sair; no tick `u >= t`, `B`
foi a **única** daquele OUI a entrar; entre `t` e `u`, `A` não voltou e nenhuma
outra chave do mesmo OUI mudou de presença; e `u` está na **mesma sessão do
daemon** que `t`.

O "única a sair / único a entrar" mata o falso positivo de **troca em bloco**:
desligar dois controles e ligar outros dois nunca é evidência.

**Por que evento e não janela de relógio:** trocar de modo no 8BitDo **exige
parear de novo** na primeira vez. Isso leva minutos — a pessoa vai às
configurações de Bluetooth do sistema. Uma janela de segundos estaria afinada
para **reconexão** de um bond que já existe, e cegaria a regra exatamente no
**primeiro** contato de alguém com o defeito, que é a pergunta literal dela.

### Grupo, não par

O 8BitDo tem até cinco modos catalogados. A estrutura é um **grupo com N
rostos**, e o tamanho do grupo é **limitado sozinho** pela condição do VID:PID:
um grupo não pode ter dois membros com o mesmo VID:PID, logo não pode crescer
além do número de modos distintos. Nenhum teto arbitrário a inventar.

### Dois níveis de confiança, e só o segundo fala na tela

- **1 revezamento limpo ⇒ o grupo já vale para a numeração**, em silêncio. O
  erro aqui é barato e se desfaz sozinho, e a recompensa é que ela e o amigo
  **nunca chegam a ver o número errado**: a evidência fica completa no mesmo
  tick em que o rosto novo aparece, e a ordem do tick já é `sync_connected`
  (`external_identity.py:1129`) **antes** de `slot_for` (`:1144`).
- **2 revezamentos, cobrindo os dois sentidos (A para B e B para A) ⇒
  confirmado**, e só aí a ficha ganha uma linha. Palavra na tela é cara; número
  não.

O único botão de ajuste é o número de revezamentos exigidos para dividir. Subir
de 1 para 2 custa **um** número errado por aparelho, uma vez na vida dele;
manter em 1 custa o falso positivo descrito adiante, que se autocorrige em um
tick.

---

## Onde a regra mora, e o que muda no `controllers.json`

### O invariante que carrega a durabilidade inteira

> **Nenhum rosto é apagado da fila. Nunca. Nem da memória, nem do disco.**

A divisão de lugar é expressa como **rank COMPARTILHADO**, jamais como remoção.
Este é o ponto em que esta sprint diverge do primeiro esboço da regra, e a razão
é uma falha de durabilidade que a revisão encontrou nele — está registrada
adiante, em *"O erro que este desenho já evitou"*.

### Onde

- **A decisão pura** — um módulo novo, irmão de `external_identity.py`, com uma
  função **sem estado global**: recebe a memória de observação, o conjunto
  presente agora, os traços e o tick, e devolve as uniões e as rupturas. Pura de
  propósito: é o que permite testar a cura inteira sem aparelho nenhum.
  <!-- ref-externa: o módulo novo ainda não existe; esta sprint é a proposta dele -->
- **O ponto de aplicação** — `ExternalIdentityRegistry.sync_connected`
  (`external_identity.py:522`), sob `self._lock`, **antes** do
  `_prune_volatile_locked`. É o único método que vê o conjunto **inteiro** de
  presentes; `slot_for` recebe uma string e não teria como decidir.
- **A concessão do lugar** — o ramo `if key not in self._ordem` de `slot_for`
  (`:494-501`) passa a consultar o grupo antes de fazer
  `max([*ocupados, int(reserve), 0]) + 1`. Se a chave nova é membro de um grupo
  que já tem lugar, ela **recebe aquele lugar**.
- **Os traços (VID/PID/driver/bus)** — já existem no mesmo escopo, sem
  encanamento novo: `ExternalLedSync.tick` (`:1099`) tem `inventory` e
  `identidades` lado a lado e já os percorre com `zip(..., strict=True)`
  (`:1137`). Basta `sync_connected` receber os pares em vez de só as strings, em
  argumento **opcional**, para não quebrar dublê de teste nenhum.
- **A tela** — nenhuma linha nova de lógica: a ficha lê o inventário que o
  daemon já carimba (`_external_inventory`, `daemon/ipc_handlers.py:264`).

### O que muda no arquivo: o formato NÃO muda, a versão NÃO muda

Três fatos MEDIDOS que fecham a porta de guardar a memória dentro do
`controllers.json`:

- `identity._save_locked` monta `payload: dict[str, Any] = {}` **do zero**
  (`identity.py:951`). Qualquer chave nova de topo escrita pelo lado dos
  externos é **destruída** no primeiro save do lado DualSense, que acontece a
  cada conexão de DualSense;
- `merged_order_payload` devolve entradas com exatamente `{"addr", "kind",
  "rank"}` (`identity.py:316`). Campo novo **por entrada** morre nos dois
  escritores;
- `order_entries` (`identity.py:279`) descarta entrada cujo `kind` não seja
  `dualsense` nem `external` — um terceiro `kind` também não serve.

Logo, o desenho:

1. **A união é um rank compartilhado, e ela cabe no formato que já existe.**
   Os dois rostos ficam em `_ordem` com o **mesmo** rank, e os dois vão ao
   disco com o mesmo rank. Nada de campo novo, nada de bump de
   `CONTROLLERS_SCHEMA_VERSION`, nada de migração escrita à mão.
2. **Uma mudança, em um lugar só, no `load`:** para `kind: external`, rank
   repetido deixa de descartar a segunda entrada (`external_identity.py:713-716`)
   e passa a restaurá-la no mesmo grupo. Para `kind: dualsense` nada muda —
   rank repetido lá continua sendo corrupção.
3. **Efeito no arquivo dela:** continua com **cinco** linhas para quatro
   plásticos, mas duas delas carregam o **mesmo** rank — que é a afirmação
   honesta *"estes dois endereços seguram um lugar"*. O arquivo não encolhe, e
   essa é a troca deliberada: abrimos mão de um ganho cosmético para comprar
   *"nada é perdido, nunca"*.
4. **A memória do que foi OBSERVADO vai para um arquivo separado e
   descartável** em `config_dir()`, com versão própria, guardando por grupo: os
   membros, o traço (`vid`, `pid`, `driver`, `bus`) de cada rosto, quantos
   revezamentos em cada sentido, e — o campo que é o freio — a lista dos pares
   que já foram vistos **juntos**.
5. **A ruptura é durável no instante em que acontece.** Ela roda dentro do
   `sync_connected`, que marca `_dirty` e chama `_save_locked` na mesma
   chamada. O rosto que perde o lugar recebe rank novo e o disco recebe a
   separação no mesmo tick. Não existe janela em que a ruptura só more na
   memória.

**Downgrade é seguro:** um daemon anterior lê um `order` perfeitamente normal,
descarta a segunda entrada de rank repetido e o segundo rosto volta a pegar
lugar no fim da fila — ou seja, degrada **exatamente** para o comportamento de
hoje. Se esse daemon anterior **salvar**, ele apaga a linha do segundo rosto, e
ao voltar para o daemon novo o rosto reentra no fim da fila. Também é o
comportamento de hoje. Está dito porque é o pior caso do downgrade, e ele é
igual ao status quo.

### O erro que este desenho já evitou

O primeiro esboço desta regra **removia** o rosto ausente de `_ordem` e deixava
a evidência num arquivo declaradamente descartável. A revisão mostrou por que
isso não fecha: perder aquele arquivo **depois** de uma união não custaria
"aprender de novo" — custaria o **lugar reservado do rosto apagado**, que
voltaria como chave nova no fim da fila. O controle que era jogador 2 viraria
jogador 4, em silêncio, sem gesto que desfizesse. E havia uma segunda janela: a
remoção persistia dentro do `sync_connected`, mas a concessão do lugar acontece
depois, em `slot_for`, que só marca `_dirty` — morrer entre as duas deixaria o
rank órfão no disco.

O invariante *"nenhum rosto é apagado"* fecha **as duas** de uma vez, porque não
há nada a perder e nada a orfanar. Fica registrado aqui porque é a decisão de
desenho mais importante da sprint, e ela nasceu de uma crítica, não de uma
medição.

### Desempate da ruptura, sempre definido

Quando a válvula rompe uma união, **o rosto que já estava em `_connected` no
tick anterior fica com o lugar** (não se move número debaixo da mão de
ninguém). Se nenhum dos dois estava — o caso do **primeiro tick após o boot**,
que é justamente quando a pessoa liga os dois e abre a janela —, desempata a
**ordem lexicográfica da chave**. É arbitrário, e é de propósito: no caso de
erro os dois são controles de verdade, e qualquer escolha é igualmente
arbitrária para quem está olhando. O que não pode existir é um caso sem
desempate.

---

## Quando a regra ERRA — os dois sentidos, e qual é pior

### Erro A — divide um lugar que não devia ser dividido

O caso realista sobrevivente: **dois aparelhos do mesmo fabricante, de
modelos ou modos diferentes, que a pessoa sempre usa um de cada vez** (dois
8BitDo, um deixado em modo Switch e outro em modo PS4, alternados). Mesmo OUI,
VID:PID diferentes, nunca juntos, revezamento limpo. A regra divide.

**Custo enquanto a divisão vale:** o recém-chegado herda o lugar do ausente em
vez de ganhar um novo. Como a divisão só governa o lugar de **quem está fora**,
e a condição "nunca juntos" é o que a sustenta, **em nenhum instante dois
controles presentes dividem número ou LED de jogador**.

**Custo no instante em que a pessoa liga os dois juntos:** a união rompe **no
mesmo tick**, dentro de `sync_connected` (`:1129`), que roda **antes** de
qualquer `slot_for` (`:1144`) e antes de qualquer `external_led_written`
(`:1218`). O incumbente fica; o outro ganha lugar novo no fim da fila no mesmo
tick; o par vai para a lista de coabitação e **nunca mais** volta a se unir.

**Custo residual visível total: um número que pula uma vez, para o rosto que
chegou por último, no momento da separação. Sem gesto, sem diálogo, sem
declaração.** O ato de usar os dois controles **é** a cura.

### Erro B — não divide o que devia

Acontece quando a pessoa nunca troca de modo com o daemon de pé, quando o
firmware não repete o OUI entre os modos, ou quando o inventário não traz
VID/PID.

**Custo: exatamente o defeito de hoje, permanente.** MAC de hardware ausente
nunca é podado; o fantasma infla o `max` de `slot_for:501`; o lado DualSense une
esses lugares na própria conta (`identity.py:586`); a ordem pode inverter; e é
permanente e sem teto.

### Qual é pior

**Em natureza, o erro A é pior**, sem discussão: dois controles presentes com o
mesmo número é literalmente o que a fila existe para impedir — a casa já
escreveu isso no próprio código (`external_identity.py:202-203`, *"buraco na
numeração é aceitável; dois controles com o mesmo número, não"*).

**É por isso que este desenho é feito para tornar o erro A INOBSERVÁVEL, e não
para torná-lo raro.** Duas invariantes carregam o peso:

1. a divisão só decide o lugar **enquanto no máximo um membro está presente**;
2. co-presença **rompe antes de atribuir**, no mesmo tick, pela ordem que o
   `tick` já tem hoje.

Com as duas de pé, o pior caso do erro A (um número que pula uma vez,
autocorrigível pelo uso normal) é **estritamente melhor** que o pior caso do
erro B (fantasma eterno inflando a fila e podendo inverter a ordem).

**E aí a resposta prática se inverte: em expectativa, B é pior**, porque B é o
estado atual, é permanente, e pega **todo mundo que tiver um 8BitDo, no primeiro
dia**.

---

## O VETO

Três recusas de revisão, que valem por melhor que seja a taxa de acerto:

1. **Qualquer implementação que possa exibir, ainda que por UM tick, dois
   controles PRESENTES com o mesmo número ou o mesmo LED de jogador está
   errada.** Trocar um fantasma **ausente** segurando um lugar por uma colisão
   **presente** é regressão, não cura.
2. **Qualquer implementação que APAGUE um rosto da fila — da memória ou do
   disco — está errada.** A união é rank compartilhado. O que se perde num
   arquivo descartável tem de custar, no máximo, "aprender de novo".
3. **Qualquer cura que dependa de alguém DECLARAR, CONFIRMAR ou CLICAR em
   alguma coisa está fora de escopo desta sprint.** A pergunta dela é o
   critério: se não roda sozinha na máquina de um desconhecido, no primeiro
   boot, não é esta cura.

---

## O que a tela mostra

**No nível 1 (divisão valendo, ainda não confirmada): nada.** O efeito visível é
a **ausência** de sintoma — o número não muda quando ela troca de modo. Não é
economia de palavra: é a promessa D2/R-15 que a casa já fez (*"o controle que eu
deixo desligado volta com o mesmo número"*), agora estendida a *"o mesmo
controle em outro rosto volta com o mesmo número"*. Promessa que já existe não
se anuncia de novo.

**No nível 2 (confirmado, dois revezamentos nos dois sentidos): uma linha na
ficha**, montada com vocabulário que já está na árvore — `detail_rows`
(`app/actions/external_controllers.py:304`), que a ficha renderiza como grade
rótulo/valor (`app/gui_dialogs.py:738`). Os rótulos vizinhos são "Controle",
"Como conectou", "Driver do Linux", "Nome do sistema". A linha nova, no mesmo
registro:

> **Também aparece como:** Pro Controller (modo Switch) — o mesmo controle,
> outro modo

O valor sai de `friendly_type` (`external_controllers.py:88`) aplicado ao outro
rosto, sem string nova de tipo. E a ficha **já ensina o conceito de modo** logo
abaixo, no segmentado read-only e no subtítulo dele (`MODE_SELECTOR_SUBTITLE`,
`:258`: *"O modo é uma troca física no controle (combo ao ligar) — veja o
manual."*). A linha nova só fecha o raciocínio que a ficha começa.

**A saída de emergência, em uma frase, no registro do
`RECONCILIAR_JOGO_ABERTO_TEXT`** (`app/actions/home_actions.py:391`, que é o
precedente da casa para "explicar o que NÃO vai acontecer"):

> Se forem dois controles diferentes, ligue os dois ao mesmo tempo: o Hefesto
> separa sozinho.

Isto é o **oposto** de uma declaração. O gesto de correção é a coisa mais
natural do mundo — usar os dois controles.

### O gesto de reparo que FUNCIONA, nomeado primeiro

Se, apesar de tudo, a pessoa quiser trocar dois números de lugar, o gesto certo
é o **seletor de número da aba Status**
(`_on_numero_button_toggled`, `app/actions/status_actions.py:1334`, que fala com
`identity.number.set`). Ele permuta entre **presentes**, que é exatamente o
formato do estrago.

**"Reconciliar jogadores" NÃO conserta isto**, e por isso não pode ser nomeado
primeiro: `RECONCILIAR_LABEL` (`home_actions.py:381`) dispara `coop.sync` e
`identity.renumber`, e o renumber **compacta preservando a ordem relativa**
(`_renumber_locked`, `daemon/ipc_handlers.py:1253`) — clicar nele deixa uma
inversão exatamente onde está, e ainda responde *"A numeração já estava
compacta."* (`reconciliar_toast`, `home_actions.py:417`). Os dois gestos não são
intercambiáveis, e a documentação de usuária tem de dizer qual é qual.

Os dois são recusados com jogo aberto (`{"ok": false, "reason":
"sessao_de_jogo_aberta"}`, `ipc_handlers.py:1059` e `:1100`), que é justamente o
momento em que a pessoa percebe que o LED errado acendeu. **Isso não é defeito
desta sprint, mas é consequência dela ficar sabendo.**

**O que a tela NÃO ganha:** nenhum botão, nenhum diálogo de confirmação, nenhum
"declare que são o mesmo aparelho". O seletor do topo (`button_labels_for`,
`external_controllers.py:186`) não muda: só um rosto do grupo está presente por
vez, então já era um botão só.

**Sem janela ninguém vê nada** — então a contraparte de terminal é obrigatória,
não opcional: `hefesto-dualsense4unix controller list`
(`cli/cmd_controller.py`) precisa mostrar o grupo. O applet COSMIC
(`packaging/cosmic-applet/src/app.rs`) é leitura, e isso tem de estar dito.

**O outro olho é o journal**, no padrão de nomes que já existe
(`external_lugar_atribuido` `:508`, `external_lugar_volatil_liberado` `:581`,
`external_fila_restaurada` `:730`): `external_revezamento_observado`,
`external_lugar_compartilhado`, `external_lugar_separado`. Com o log dá para
auditar a conclusão da máquina sem tocar no aparelho — inclusive remotamente,
na máquina do amigo.

**Regra da casa aplicada:** a linha nova da ficha é interface e só fecha com o
olho dela (PROVA-DE-TELA-01), com `scripts/gui-captura/retratar_abas.py` antes e
depois.

---

## A mordida esperada de cada teste

A cura inteira é uma função pura sobre um log de presença sintético. **Nada
disto precisa de hardware, de GTK ou de Xvfb.** A bancada já existe em
`tests/unit/test_external_identity.py`: faixa forjada `aa:bb:cc:*` (`:43-47`),
`_entry` (`:364`), `led_escritas` (`:378`), `_gravar_fila` (`:92`) e
`_fila_no_disco` (`:77`). **Nenhum MAC real, nenhum OUI real** — e a regra não
precisa de OUI de verdade para nada.

Teste tem de MORDER: arranque a cura, veja reprovar, devolva.

| teste | o que ele afirma | **arranque isto e ele TEM de reprovar** |
|---|---|---|
| 1. o revezamento divide o lugar | A presente 3 ticks, sai; B (mesmo OUI, VID:PID diferente) entra; B recebe o lugar de A | a consulta ao grupo no ramo `if key not in self._ordem` de `slot_for` — B volta a `max+1` |
| 2. **o fantasma de HARDWARE não infla quem chega depois** | o teste que a `IDENTIDADE-DUPLA-01` nunca teve: fantasma é MAC de hardware, não `_KEY_SINTETIZADO` | a regra inteira — e note que `test_quatro_controles_...` (`:722`) **continua verde**, porque testa o MODO-01 |
| 3. dois do mesmo modelo NUNCA se unem | mesmo OUI, **mesmo** VID:PID, dez revezamentos limpos, zero uniões | a condição VID:PID-diferentes — vira união e derruba junto o `test_dois_aparelhos_do_mesmo_oui_nunca_se_fundem` (`:703`) |
| 4. troca em bloco não é evidência | dois saem no mesmo tick, dois entram no seguinte, zero uniões | o "única a sair / único a entrar" — vira união em par cruzado |
| 5. **co-presença rompe ANTES de atribuir** | união montada, `sync_connected([A, B])`: em nenhum instante `slot_for(A) == slot_for(B)`, e nenhum `external_led_written` sai com número repetido | a válvula — o teste falha com "dois controles no mesmo lugar", que é o VETO 1 |
| 6. co-presença uma vez proíbe para sempre | depois da ruptura, dez revezamentos não a refazem | a lista de coabitação — a união volta e o toast de desfazer vira eterno |
| 7. **nenhum rosto some da fila** | depois da união, `snapshot()` tem os DOIS membros, com o MESMO rank; e o disco tem as duas linhas | o invariante do VETO 2 — se a implementação remover, o teste acusa a entrada que sumiu |
| 8. perder a memória custa só aprender de novo | apagar o arquivo de observação: a fila fica **idêntica**, os ranks não mudam, só o aprendizado zera | idem ao 7 — com remoção, o rank do rosto apagado vira tail e o teste reprova |
| 9. traço desconhecido não une (fail-closed) | sem `vid`/`pid` no inventário, nunca há candidato | o fail-closed — vira união por OUI puro |
| 10. sem `sync_connected` não há evidência | `slot_for` sozinho nunca une | a fronteira — fecha o buraco de a janela ou o IPC induzirem união pela rota de LEITURA |
| 11. desempate sempre definido | ruptura no **primeiro** tick após o boot, com ninguém em `_connected` antes: resultado determinístico e repetível | o desempate lexicográfico — o teste vira instável |
| 12. canário de FS | o arquivo novo em `config_dir()` respeita o isolamento XDG do `conftest` | ver [CANARIO-FS-01](2026-08-05-CANARIO-FS-01-a-suite-escrevia-no-home-de-verdade.md) |

---

## O que só fecha com o 8BitDo na mão dela

Todos SEM PROVA hoje. É honesto que fiquem abertos até a bancada.

1. **A adjacência de fato.** Ao trocar de modo, o endereço velho some **antes**
   de o novo aparecer, sem sobreposição? Se houvesse um instante de
   sobreposição, a regra se auto-recusaria — falharia em segurança, mas
   falharia. É comportamento de firmware, n=1 hoje.
2. **O endereço de cada modo é estável entre pareamentos?** Se o 8BitDo
   sorteasse endereço novo a cada pareamento, o revezamento apareceria entre
   rostos de **mesmo** VID:PID e a regra recusaria (perda, não dano) — e a fila
   voltaria a crescer sem teto, que é outro defeito.
3. **O mesmo OUI vale nos dois modos?** É a aposta da tabela, medida uma vez.
   Se não valer, falha fechada.
4. **Os rostos ainda não medidos:** modo Switch por **Bluetooth** (a
   documentação mede o de cabo) e o modo **X-input**, cujo endereço nunca foi
   visto. Se o X-input trouxer um terceiro MAC de hardware, o grupo tem três
   membros — o desenho aguenta, mas o texto da ficha muda.
5. **O terceiro rosto sintético no cabo** não pode virar candidato (não é
   persistível). Confirmar ao vivo, não só por leitura.
6. **A medição de 2 minutos que continua barata e continua faltando**, e que
   daria uma quinta condição de graça:
   `cat /sys/class/input/inputN/id/version` em cada modo. O campo existe nos
   dois transportes, o `python-evdev` já o entrega, e o inventário
   (`core/evdev_reader.py`) **não o publica**. Com ele, a condição
   "VID:PID diferentes" ganharia um irmão que separa **hardware**, não só
   classe.
7. **O olho dela na tela**, pela PROVA-DE-TELA-01, para a linha do nível 2.

---

## O que esta sprint NÃO resolve

1. **Troca de modo com o daemon desligado não gera evidência.** Sem observação,
   sem união — a pessoa vê o número inflado até que uma troca aconteça com o
   daemon de pé. É o preço explícito de aprender com o uso.
2. **O falso positivo residual** — dois aparelhos do mesmo fabricante,
   modelos ou modos diferentes, nunca usados juntos. Reduzido, não eliminado.
   Só se elimina com um discriminador de **hardware** que a árvore ainda não lê
   (`id/version` por evdev, `bcdDevice` no USB,
   `hardware_version`/`firmware_version` do `hid-playstation`).
3. **O aparelho que troca de endereço no MESMO modo** (re-pareamento, reset de
   fábrica). A condição do VID:PID recusa a união — perda deliberada. A fila
   continua ganhando uma entrada por pareamento.
4. **A fila de externos continua sem teto.** `_MAX_PERSISTED_SLOTS`
   (`identity.py:215`) segue aplicado só no lado DualSense (`:896`). Esta cura
   reduz o crescimento do **espaço de ranks**; não limita o número de linhas.
   Defeito separado, e o conserto é espelhar o teto no `load` dos externos.
5. **`Profile.controllers` continua chaveado por MAC**
   (`profiles/schema.py:549`). Unifiquei o **número**, não a **chave de
   perfil**: um ajuste feito no rosto "modo Switch" não vale no rosto "modo
   PS4", nem viaja para a máquina do amigo. A extensão natural é o lookup de
   perfil consultar os outros rostos do grupo, e está deliberadamente fora
   deste desenho.
6. **`NOME-HONESTO-01` continua aberto para quem tem 8BitDo de outro lote.**
   `_BRAND_BY_OUI` (`external_controllers.py:64`) é tabela de **um** item, e o
   Pro genuíno tem gêmeo em `NINTENDO_REAL_OUI` (`external_identity.py:160`),
   consumido no portão estrito da IMU (`:859`). Na máquina do amigo, um 8BitDo
   em modo PS4 de outro lote é chamado de **Sony**, e um Pro genuíno de outro
   lote fica com o giroscópio em STANDBY **sem uma linha de log**. Os dois
   degradam em silêncio. Esta cura não depende do nome para **funcionar** (ela
   não pergunta nada), mas **depende dele para ser explicável** — a linha do
   nível 2 na ficha vai mentir o fabricante. Ver o inventário de portabilidade
   citado no rodapé.
7. **A objeção de suficiência da `IDENT-01` continua de pé:** "nunca vistos
   juntos" nunca prova "mesmo plástico". Esta proposta não a refuta — ela a
   desarma, devolvendo a decisão ao aparelho (ligue os dois e eles se separam).
8. **Não apaga endereço nenhum por conta de ausência.** A reserva eterna do MAC
   de hardware (D2/R-15) continua intacta para aparelho sem irmão — e, pelo
   VETO 2, também para aparelho **com** irmão.
9. **Não mexe no bond do modo não usado**, pendurado no BlueZ. Território do
   watchdog de Bluetooth.

---

## Notas datadas — 06/08/2026

Decisão medida não se apaga; ganha nota datada com o que caducou.

### Na [IDENTIDADE-DUPLA-01](2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)

1. **A E1 ("falta medir, 2 minutos") já estava medida desde 25/07**, em
   `docs/usage/troubleshooting-8bitdo.md`, seção *"O MAC muda com o modo"*, com
   grau MEDIDO. E foi reconfirmada no journal em 06/08 sem tocar no controle.
2. **A evidência de simultaneidade das linhas 27-28 é leitura errada.** Aquela
   linha é `external_fila_restaurada`, que imprime a fila **persistida em
   disco**, ausentes inclusive — não presença. Varrendo o journal de 27/07 a
   06/08, os dois endereços de hardware do 8BitDo **nunca escreveram LED no
   mesmo tick**. Consequência: o critério "nunca simultâneos" **não** está
   refutado; ele é rejeitado como **insuficiente** (objeção da `IDENT-01`), e é
   por isso que esta cura o cerca com mais três condições e uma válvula.
3. **O sintoma "o controle conectado cai no slot 5" já não é o defeito.**
   `_posicao_locked` conta só presentes desde a `NUM-01`. Vender esta cura como
   "conserta o número na tela" seria a interface mentindo. O que ela conserta é
   a inflação de rank, a inversão de ordem e o crescimento sem fim da fila.

### Na varredura anterior de identidade

A ficha propunha **declaração de identidades irmãs, gesto na janela, desfazer**.
Caducou em 06/08/2026, pela pergunta dela citada no topo: um registro só existe
na máquina onde alguém declarou, e o amigo cai no defeito no primeiro dia sem
nada declarado. **A proposta não estava errada para o caso dela — estava errada
para o alcance do defeito**, e foi a pergunta que revelou o alcance.

### Em `core/evdev_reader.py`, docstring de `_evdev_owner_dir`

O docstring diz que `phys` vem vazio nos controles por Bluetooth. **Medido em
06/08: é verdade no nó de input do DualSense e falso no do Pro Controller**, que
traz o endereço do adaptador; e no nível HID o `HID_PHYS` vem preenchido nos
dois. O `phys` vazio é propriedade do **driver**, não do transporte. A decisão
(não usar `phys` como identidade) continua certa; o **motivo** escrito é que
caducou. GRAU: MEDIDO.

---

## Achado fora de escopo, e mais urgente que esta sprint

A regra da casa *"nada de MAC real em arquivo versionado"* **está sendo violada
hoje**, e os dois portões são cegos às duas formas em que ela é violada. O
inventário completo, com a contagem por arquivo, está em
[o que só funciona na máquina dela](../estudos/2026-08-06-o-que-so-funciona-na-maquina-dela.md),
seção 4. Nada foi editado por esta sprint.
