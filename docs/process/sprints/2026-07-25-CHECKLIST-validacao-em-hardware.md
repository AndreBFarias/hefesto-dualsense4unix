# Validação em hardware — a leva de 25/07

> **O que este documento é.** A lista do que **nenhum agente conseguiu provar**.
> Oito sprints entraram com 5.507 testes verdes, e testes verdes não dizem se o
> controle funciona na mão de quem joga. Isto aqui é o que falta, e só a
> mantenedora pode responder.
>
> **O que ele não é.** Não é o ritual de checklist pré-release que o projeto
> declarou duas vezes e nunca cumpriu (ver a nota no README sobre os dois
> documentos com zero caixas marcadas). É a lista curta do que esta leva mexeu.

## Antes de começar

O daemon precisa estar rodando o código novo:

```bash
systemctl --user restart hefesto-dualsense4unix.service
journalctl --user -u hefesto-dualsense4unix -f
```

## 1. O jogo enxerga um dispositivo por controle (JOGO-01)

Era o defeito mais grave: com **um** controle no cabo, o jogo via **quatro**
dispositivos — o virtual, o físico e dois pads do Steam Input.

Com o jogo aberto:

```bash
for j in /dev/input/js*; do
  echo "$j -> $(udevadm info -a -n "$j" 2>/dev/null | grep -m1 'ATTRS{name}')"
done
```

- [ ] Um controle físico → **um** dispositivo de jogo
- [ ] Quatro controles em co-op → **quatro**
- [ ] Num jogo da lista de exceção do Steam Input (Mullet Mad Jack), o controle
      responde e a cor não é sequestrada

**Se falhar:** procurar `steam_input_vpad_mantido_de_pe` no journal. É a trava de
segurança avisando que não conseguiu armar a vigia e preferiu o comportamento
antigo a deixar a sessão sem controle.

## 2. Quem está na mesa é 1..N (NUM-01)

- [ ] Ligar só o controle B → é o **jogador 1**
- [ ] Ligar o A também → B continua 1, A vira 2, **ninguém pisca**
- [ ] Desligar o B → A vira **jogador 1**
- [ ] Religar o B → volta A=1, B=2
- [ ] Reiniciar o daemon com os dois ligados → a ordem se mantém
- [ ] Reiniciar a máquina → a ordem se mantém

**O critério que resume tudo: nunca deve existir um jogador 2 sem jogador 1.**

## 3. O modo jogo liga sozinho (MODO-01)

Já **confirmado ao vivo** em 25/07, em três jogos sem perfil próprio:

```
profile_mode_aplicado  origin=game_signal  wm_class=steam_app_2912550
profile_mode_aplicado  origin=game_signal  wm_class=steam_app_1553260
profile_mode_aplicado  origin=game_signal  wm_class=steam_app_1332010
```

Falta:

- [ ] Abrir um jogo que casa `coop_local` por título (Sackboy, Overcooked, It
      Takes Two, Cuphead) → o modo liga **com o cadeado de perfil ligado**
- [ ] Fechar o jogo → volta ao modo anterior, e o controle segue funcionando no
      desktop *(é o caso que a trava `ligou_gamepad` protege)*
- [ ] Criar perfil pelo fluxo "Jogo da Steam" → nasce com modo de jogo já
      escolhido *(medido no código em 25/07: **já funciona** — o pré-preenchimento
      grava `kind="gamepad"`, e o AppID também é preenchido sozinho com o jogo
      aberto. O que falta aqui é só confirmar na mão. Detalhe em AUTO-03.)*

## 4. A vibração não trava (RUMBLE-PRESO-01)

Medido em 90 minutos de jogo: **17 disparos** da rede de segurança, sete deles
perceptíveis. O teto caiu de 6 s para 3 s depois dessa medição.

- [ ] Jogar 30+ minutos → a vibração nunca fica presa
- [ ] Contar os disparos e ler o silêncio medido:

```bash
journalctl --user -u hefesto-dualsense4unix --since today \
  | grep rumble_preso_expirado
```

**O dado que fecha a questão:** se `silencio_s` se concentrar logo acima de 3 s,
o pedido de parada chega atrasado e o teto pode cair mais. Se for sempre muito
maior, o pedido nunca chega — e aí o teto só decide quão cedo a rede age.

**Isto é mitigação, não cura.** A cura exige capturar os bytes que o jogo escreve
no gamepad virtual.

## 5. A configuração fica onde ela foi deixada (ABAS-01)

Quatro caminhos que perdiam configuração **sem aviso**:

- [ ] Aba Perfis → escolher o Modo → Salvar → mexer na cor → "Salvar Perfil" no
      rodapé → **o modo continua no arquivo**
- [ ] Duas cores por controle → alvo em "Todos" → arrastar o brilho → **as cores
      por controle sobrevivem**
- [ ] Editar várias abas → renomear o perfil → Salvar → **as edições estão lá**
- [ ] "Parar" a vibração → "Aplicar" em outra aba → **não volta a vibrar**

## 6. O microfone (MIC-USB-01)

Eram três mutes empilhados. Os dois primeiros agora têm cura automática:

```bash
bash scripts/doctor.sh --fix-mic
hefesto-dualsense4unix mic unmute
```

> **Correção de 25/07 à noite:** este checklist mandava rodar
> `hefesto-dualsense4unix doctor --fix-mic`, e **esse comando não existe** — a
> CLI responde `No such option: --fix-mic`. São dois doctors com o mesmo nome: o
> da CLI repassa só `--fix` e `--quiet` ao script, e a cura do microfone mora no
> doctor de shell, que não está no PATH. Medido e registrado em AUTO-04.

- [ ] `doctor` acusa e cura o mute do WirePlumber e o perfil sem sinal
- [ ] `mic unmute` desmuta pelo terminal, **sem apertar o botão do controle**
- [ ] O medidor da aba Status se mexe quando ela fala

## 7. Co-op sem terminal (AUTO-01)

- [ ] Plugar o segundo controle → a emulação liga **sozinha** em ~2 s
- [ ] Escolher "Controlar o PC" → **não** é religada por cima *(é a distinção
      entre "nunca decidiu" e "decidiu desligar")*
- [ ] Aba Início → "Preparar co-op (N jogadores)" → um clique resolve
- [ ] `gamepad on` pelo terminal e "Jogar pelo Hefesto" pela janela entregam a
      **mesma** máscara

## 8. Legibilidade (LEGIBILIDADE-01)

- [ ] Ler o rodapé **sem se aproximar da tela**
- [ ] Nenhuma aba abre com barra de rolagem
- [ ] Os analógicos aparecem na faixa do microfone e da lightbar

## 9. Um número de jogador, editável (PLAYER-01)

- [ ] A seção agora se chama **"Desenho das 5 luzes"** e não promete mudar o
      jogador
- [ ] "Número deste controle" no cabeçalho **muda o número de verdade**, e os
      cartões das abas Status e Início acompanham
- [ ] Os chips saem em ordem crescente, e clicar em cada um edita o controle
      certo

## 10. O número do jogo chega ao controle (PLAYER-LED-01)

Entregue em 25/07 à noite, **sem nenhuma validação em hardware**.

- [ ] Jogo de co-op com quatro controles → as luzes batem com os números que o
      **jogo** mostra na tela
- [ ] Alt-tab e volta → os números **não piscam** nem trocam de dono
- [ ] O journal **não** mostra retenção de número:

```bash
journalctl --user -u hefesto-dualsense4unix --since today \
  | grep -E "game_output_retido.*player_leds"
```

**Nada aqui é falha:** retenção de `campos=['led']` continua possível e é o gate
protegendo a cor. O que não pode aparecer é `player_leds`.

- [ ] O par honesto aparece no journal: `uhid_replica_ativa` (o jogo pediu) e
      `game_output_aplicado` (o controle recebeu)
- [ ] `hefesto-dualsense4unix controller numbers` mostra, por controle, o nosso
      número × o do jogo × o padrão aceso × o do kernel

## 11. Uma contagem só (CONTAGEM-01)

Também entregue sem validação em hardware.

- [ ] Quatro controles — dois DualSense, um Nintendo, um 8BitDo
- [ ] Cabeçalho diz **4 controles**
- [ ] Botão diz **"Preparar co-op (4 jogadores)"**
- [ ] Seção Controles mostra **quatro** cartões
- [ ] O externo mostra **travessão** no jogador, com a explicação visível
- [ ] Desligar um → tudo cai para três **junto**, sem parte da tela ficar para trás
- [ ] Aba Emulação não chama mais nó de controle (diz físicos × virtuais nossos)

## O teste que vale por todos

**Quatro controles em co-op, dois por cabo e dois por rádio, um DualSense, um
Nintendo Pro e um 8BitDo em modo DirectInput — cada um o seu jogador, do primeiro
quadro, sem abrir terminal.**

É o objetivo desde o começo, e é a única prova que interessa.

---

## O que continua sem cura, e não é honesto esconder

- **A interferência de rádio.** 163.925 quadros corrompidos num único boot, com
  sinal forte e qualidade de enlace zero. O experimento que fecharia a questão —
  medir com o adaptador WiFi removido — **não foi feito**.
- **A causa da perda do pedido de parada da vibração.** Mitigada, não resolvida.
- **O `bluetoothd` que apaga pareamentos.** Problema aberto do BlueZ, sem
  correção conhecida, e a captura forense continua desligada.
