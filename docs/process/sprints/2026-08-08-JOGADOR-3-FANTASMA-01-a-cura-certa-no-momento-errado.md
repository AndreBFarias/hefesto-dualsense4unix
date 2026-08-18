# JOGADOR-3-FANTASMA-01 — a cura certa no momento errado

- **Escrito em:** 08/08/2026, tarde, na branch `restauro/inicio-da-sessao`
- **O que esta sprint registra:** um defeito medido na tela dela, uma cura que
  **funcionou no mecanismo e quebrou os controles**, e a reversão
- **Natureza:** defeito aberto, com causa MEDIDA e cura **revertida**
- **Por que existe:** errar o *momento* de uma cura correta é o tipo de erro que
  se repete se ninguém escrever

---

## 1. O defeito, na tela dela

Com o Sackboy aberto e marcado na allowlist do Steam Input, e dois DualSense no
cabo, o jogo mostrava um **"Jogador 3"** que era o próprio controle duplicado.

**GRAU: MEDIDO.** Estado do `sysfs` no instante:

```
FISICO 0003:054C:0CE6.0047   hidraw=hidraw1     ← exposto
FISICO 0003:054C:0CE6.004F   hidraw=hidraw0     ← exposto
VPAD   0003:054C:0DF2.0050   hidraw=hidraw2     ← de pé
VPAD   0003:054C:0DF2.0051   hidraw=hidraw3     ← de pé
```

**Quatro dispositivos onde havia dois controles.**

---

## 2. A causa, em duas metades

**GRAU: MEDIDO** nas duas.

### Metade 1 — o gesto que ganha pela metade

```
13:17:42  autoswitch_janela_propria_ignorada  wm_class=Hefesto-Dualsense4Unix
13:17:49  steam_input_vpad_retomado           motivo=gesto_manual
13:17:50  gamepad_grab_pulado_steam_input     motivo=excecao_por_appid   ← grab PULADO
13:17:50  broker_hide_pulado_steam_input      motivo=excecao_por_appid   ← hide PULADO
13:17:50  gamepad_emulation_started           flavor=dualsense           ← vpad DE PÉ
```

O ramo do gesto manual em `daemon/subsystems/gamepad.py` devolvia o vpad e
**mantinha o grab e o esconde-esconde pulados**, porque a exceção seguia ativa.
Físico exposto + vpad de pé = duplicado por construção.

E o código declarava o preço como aceitável:

> *"O preço — este jogo volta a ver dois dispositivos — é escolha dela, e fica no
> journal."*

**Não era escolha.** Ela não clicou em nada: **abriu a janela do Hefesto**, a
pedido de quem conduzia o teste. E a única pista do preço estava num log que
ninguém lê durante a partida.

### Metade 2 — o `env` que sobrescreve sem olhar

`daemon/launch_env.py` escrevia o `steam_app_<appid>.env` do ramo da allowlist
para **todo** appid da lista, sempre, sem conferir se a exceção estava valendo.
O arquivo seguia dizendo *"físico é o único dispositivo"* com o vpad de pé.

O comentário do próprio bloco já enunciava a condição que não era testada ali:

> *"omitir o IGNORE só está certo porque o gamepad virtual sai de cena enquanto o
> jogo da allowlist estiver em sessão"*

**A regra estava escrita e não era imposta.** É a mesma classe do rótulo
`"allowlist Steam Input (físico é o único dispositivo)"`, que a `JOGO-01` criou
justamente para declarar essa invariante.

---

## 3. A cura tentada, e por que ela funcionou

**O gesto passaria a ganhar inteiro:** pedir o gamepad do Hefesto com o jogo
aberto **dispensava** a exceção para aquele appid — grab retomado, hidraw
escondido, `env` com máscara.

E o mecanismo **funcionou**, medido no journal:

```
steam_input_excecao_dispensada_por_gesto  appid=1599660
gamepad_controller_grab  grab=True ok=True state=held     ← antes era "pulado"
launch_env_allowlist_pulada_por_dispensa  appid=1599660
```

Onde antes se lia `gamepad_grab_pulado_steam_input`, passou a se ler `grab=True
state=held`. **As duas metades fecharam.**

---

## 4. E por que ela quebrou tudo

**GRAU: MEDIDO.** Relato dela, imediato:

> *"nenhum dos dois controles tem os inputs reconhecidos nem com o hefesto
> fechado nem com ele aberto… em nenhum momento ficaram desconectados"*

**O jogo lê o `env` UMA VEZ, na abertura.** O wrapper termina em
`exec env "$@"` (`assets/hefesto-launch.sh:320`) — as variáveis entram no
processo do jogo e ficam. Nenhuma reescrita posterior alcança o jogo em curso.

Então a cura produziu, no meio da sessão:

- o **jogo**, lançado com o `env` da allowlist, procurando o **controle físico**;
- a **máquina**, com o físico **agarrado** pelo grab que a cura retomou.

O jogo olhava para um dispositivo que tinha acabado de emudecer. **Nenhum input,
nem físico nem virtual.**

### A regra que eu tinha e não apliquei

A investigação da madrugada anterior já a tinha escrito, e ela está no relatório
daquela onda:

> *a suspensão do vpad só pode acontecer na **ABERTURA** da sessão do jogo e só
> pode ser desfeita quando a sessão **ACABA**, nunca por mudança de foco.*

A [PARTIDA-PICOTADA-01](2026-08-08-PARTIDA-PICOTADA-01-a-caixinha-que-tirava-o-jogador-2-a-cada-piscada.md)
curou a primeira metade — *"nunca por mudança de foco"* — e funcionou: seis tiques
cegos na sessão de teste, **zero** derrubadas. Esta cura **criou uma segunda troca
no meio da sessão**, que é o mesmo erro pelo outro lado.

**O achado de método, e é o motivo desta sprint existir:** uma cura pode estar
certa no mecanismo e errada no **momento**. O teste unitário não pega isso —
todos os nove passaram, e a suíte inteira ficou verde em 7.808. O que pega é a
mesa dela.

---

## 5. A reversão

**Revertida por completo**, com `git checkout HEAD --` nos dois arquivos, e o
daemon reiniciado com o jogo fechado. Estado confirmado depois:

```
FISICO 0003:054C:0CE6.0047   hidraw=hidraw1     ← livre
FISICO 0003:054C:0CE6.004F   hidraw=hidraw0     ← livre
gamepad_controller_grab  grab=False ok=True state=off
```

**Ela confirmou:** *"voltaram sim"*.

**Nada desta cura está na árvore.** O que ficou é este registro e os testes de
comportamento, que descrevem o defeito real e continuarão válidos para a cura
certa.

---

## 6. O desenho que a medição impõe

**GRAU: MEDIDO** o bloqueio; **DECISÃO DELA** o caminho.

O `exec env` deixa só dois estados honestos:

| quando a mudança acontece | resultado |
|---|---|
| **antes** de o jogo abrir | o jogo e a máquina concordam — funciona |
| **com o jogo aberto** | o jogo tem uma configuração e a máquina outra — quebra |

Foram oferecidas a ela duas saídas — recusar o gesto, ou fazê-lo valer só na
próxima abertura. **Ela recusou as duas**, com a razão certa:

> *"não gosto de nenhuma das duas. Temos que fazer isso funcionar."*

E propôs a terceira, que é a única que **resolve** em vez de evitar:

> *"se implementarmos e dermos um restart hefesto pra ele se reconectar e zerar
> não funcionaria? […] o tempo de reconexão seria um bom pagamento pra termos ele
> funcionando"*

E, ao saber que reiniciar o daemon não faz o jogo reler o `env`, apontou o
precedente da própria casa:

> *"quando clicamos na gui em reiniciar o hefesto isso não funcionaria? No pior
> caso apareceria uma janela que nos pergunta se queremos aplicar agora e ela fala
> que vai fechar o jogo aberto (reiniciando a steam) fizemos algo parecido já."*

**O precedente existe** e é exatamente esse: `app/actions/daemon_actions.py:247`,
*"Diálogo ÚNICO de 'posso fechar a Steam?' — HONESTIDADE-STEAM-01"*. E a linha
1140 registra o comportamento de hoje — *"Se algum jogo estiver aberto eu não
faço NADA"* —, que é **recusar em silêncio**. O passo que falta é **perguntar**.

### As duas curas aprovadas por ela

**Parte 1 — abrir a janela não toca no gamepad.** O `gesto_manual` disparou sete
segundos depois de ela abrir a janela, sem nenhuma chamada dela no meio.
Sincronizar estado é **ler**, não **escrever**. Curada esta parte, o caso que
quebrou hoje deixa de existir sem diálogo nenhum.

**Parte 2 — o diálogo que oferece relançar.** Quando a mudança de fato exigir que
o jogo reabra, o produto pergunta, no padrão do `HONESTIDADE-STEAM-01`, com três
saídas: fechar-e-aplicar, aplicar-na-próxima-abertura, cancelar.

---

## 7. O que fica ABERTO

1. **O gatilho da Parte 1 não está localizado.** A busca por `gamepad.start` em
   `app/` não devolve nada, e a aba Início só usa `daemon.state_full`,
   `coop.sync` e `identity.renumber`. **A hipótese viva** é promoção silenciosa
   de origem — algum caminho transformando um pedido de perfil ou de
   sincronização em `origin="manual"`.
2. **O fantasma continua vivo** na máquina dela, com a marca ligada.
3. **A numeração é um terceiro defeito, e foi medida hoje.** Ela viu o roxo com
   LED de jogador 4 e lightbar verde, e o branco com jogador 3 e lightbar azul —
   enquanto a janela dizia **P1 e P2**. Os vpads estão nos slots 3 e 4 (padrões
   `10101` e `11011`). **Três contabilidades discordando no mesmo controle.** É a
   [DUAS-CONTABILIDADES-01](2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md),
   agora com prova de que alcança o gamepad virtual.
4. **Ela vai comprar mais dois DualSense este mês**, e disse que a solução tem de
   valer até o jogador 4. **Conferido e MEDIDO que a forma escala:**
   `cobertura_total = fisicos <= 0 or len(backends) >= fisicos` é contagem, e o
   `_IGNORE_VALUE` é por par VID/PID, não por dispositivo. **A corrida do `env`,
   porém, piora com quatro** — mais vpads, mais estados intermediários.

## 8. Nota de honestidade

**A cura foi aplicada na máquina dela e quebrou os controles dela.** O daemon foi
reiniciado duas vezes, sempre com o jogo fechado, e a reversão foi imediata assim
que ela relatou.

**E o gesto que disparou o defeito foi pedido por quem conduzia o teste** — o
passo 2 do protocolo mandava abrir a janela do Hefesto no meio da partida. A
frase do código que chamava aquilo de *"escolha dela"* estava errada nas duas
pontas: não era escolha, e não foi dela.
