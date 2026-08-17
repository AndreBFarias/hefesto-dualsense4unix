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

E o log do instante mostra o candidato:

```
backend_hotplug_reconcile  trigger=input_dir_change     (8 vezes em 10 min)
gatilho_disparou  nome=lightbar  resultado={}           (resultado VAZIO)
```

O Proton cria e destrói nós em `/dev/input` o tempo todo, e o daemon **reconcilia
a cada mudança** (`daemon/connection.py:590`). O `resultado={}` do gatilho de
lightbar é o segundo sintoma: o daemon não achou ninguém para escrever — ele
perdeu a referência do controle sem perder o descritor.

**Hipótese, não conclusão:** a rajada de reconciliação disparada pelo jogo
derruba a leitura sem fechar o fd. Falta medir se o reconcile é a causa ou outro
sintoma do mesmo problema.

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

Ele é curto, e é o que decide:

1. daemon recém-reiniciado, controle no cabo, **nenhum jogo**;
2. medir o vpad com um gesto (deve dar dezenas de pares de eixo — é o gabarito);
3. **abrir o jogo** e medir de novo, sem tocar em mais nada;
4. se congelar, contar os `backend_hotplug_reconcile` da janela.

Se o congelamento coincidir com a rajada de reconcile, a causa tem nome e o
`connection.py:590` é o endereço. Se não coincidir, o reconcile é sintoma e o
alvo passa a ser o que mais acontece quando o Proton sobe.

## O que este dia acrescenta à metodologia

Uma quarta regra, irmã das três de ontem:

> **A atenção de quem faz o gesto é uma variável do ensaio.** Depois de muitas
> horas, "mexa o analógico" deixa de ser um estímulo controlado. Medição que
> depende da mão humana tem hora para acabar, e reconhecer isso é parte do
> método — não desistência.
