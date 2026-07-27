# STEAM-INPUT-01 — ela nunca mais precisa decidir quando ligar a entrada Steam

- **Status:** ABERTA
- **Prioridade:** ALTA — é decisão técnica empurrada para quem só quer jogar, e
  já voltou depois de ter sido dada por resolvida
- **Aberta em:** 26/07/2026, junto com o rollback da leva da madrugada

## O relato dela

> *"agora eu não sei quando é pra ativar entrada steam e quando não é. pensei que
> tivéssemos superado isso"*

O "pensei que tivéssemos superado" é a parte que importa. **O problema não é
ensinar a regra.** Se a resposta desta sprint for uma frase melhor num tooltip,
ela terá falhado: daqui a duas semanas a pergunta volta. O objetivo é ela **não
precisar saber** que existe uma coisa chamada Steam Input.

## A regra que o código realmente implementa

Antes de qualquer entrega, o que está escrito hoje, em uma frase:

> Você nunca liga o Steam Input pela Steam. O padrão é ele desligado em tudo.
> Quando **um** jogo não responder ao controle, abra o jogo, volte ao Hefesto e
> clique **"Este jogo não funciona"**: o Hefesto liga o Steam Input só naquele
> jogo e sai inteiro da frente dele.

Cada pedaço tem endereço:

- **Padrão desligado, sem perguntar.** `install.sh:2181` (passo 11/11) roda
  `scripts/disable_steam_input.sh --apply`. O opt-out é `--keep-steam-input`.
- **Um vigia permanente.** `install.sh:2199` e `install.sh:2204` instalam e
  habilitam `hefesto-steam-input-guard.path` + `.timer` (30 min), que reaplicam o
  desligamento se a Steam reescrever o `localconfig.vdf`.
- **O global sempre morre; o per-app é a exceção.**
  `scripts/disable_steam_input.sh:267-268` zera `SteamController_PSSupport` e
  `SteamController_SwitchSupport` **sempre**;
  `scripts/disable_steam_input.sh:269-272` só zera o `UseSteamControllerConfig`
  do bloco `apps/<appid>` se o appid **não** estiver na allowlist
  (`scripts/disable_steam_input.sh:226`).
- **A allowlist é a única chave, e tem um escritor só.**
  `integrations/steam_launch_options.py:765`
  (`add_appid_to_steam_input_allowlist`), chamado de um lugar só:
  `app/actions/daemon_actions.py:994`, dentro de
  `app/actions/daemon_actions.py:970` (`on_steam_game_broken`).
- **A saída de cena já está entregue nesta árvore** (não é regressão da
  madrugada): `daemon/launch_env.py` grava o `steam_app_<appid>.env` sem
  `SDL_GAMECONTROLLER_IGNORE_DEVICES` e sem `PROTON_DISABLE_HIDRAW`, e
  `daemon/subsystems/gamepad.py:231` (`sync_steam_input_exception`) +
  `daemon/subsystems/gamepad.py:405` (`suspend_vpads_for_steam_input`) retiram o
  gamepad virtual do caminho. Medido no disco dela:

```
~/.local/state/hefesto-dualsense4unix/launch_env/steam_app_2111190.env
# estado: allowlist Steam Input (físico é o único dispositivo) | ... | 2026-07-26T03:26:43
__GL_SHADER_DISK_CACHE=1 ...        (sem IGNORE_DEVICES, sem PROTON_DISABLE_HIDRAW)
```

A regra existe e funciona. **Ela não tem como conhecê-la olhando a tela** — e em
quatro pontos medidos a própria tela ensina o contrário.

## Os pontos medidos em que a regra falha ou se contradiz

### 1. O produto ensina a ir na Steam — o gesto que ele mesmo desfaz

`app/actions/daemon_actions.py:313-317`, no toast do próprio botão:

> *"...na Steam: botão direito no jogo → Propriedades → Controle → 'Ativar'
> (agora o Hefesto respeita essa escolha em vez de desfazê-la)."*

Isso só é verdade para um appid **que já está na allowlist**. Para qualquer outro
jogo é falso: o guarda desfaz. Esta é a frase mais provável na origem da confusão
que ela relatou.

### 2. E foi exatamente isso que aconteceu na máquina dela

```
localconfig.vdf, linha 1225:  "UseSteamControllerConfig"  "2"   dentro do bloco "3357650"  → PRAGMATA
~/.config/hefesto-dualsense4unix/steam_input_apps.txt (mtime 22/07):  contém apenas  2111190
```

Há um jogo com Steam Input ligado **fora** da allowlist. O guarda vai desligar,
sem avisar, na próxima vez que rodar. Ela não fez nada errado — seguiu a frase da
entrega 1.

E `docs/usage/jogos-e-mascaras.md:60` lista **Pragmata** entre os jogos com
suporte nativo a DualSense, ou seja, o jogo que **não** deveria precisar de Steam
Input é justamente o que está com ele ligado.

### 3. A rede de segurança está morta agora

```
systemctl --user show hefesto-steam-input-guard.timer
  ActiveState=active                    (status: "active (elapsed) since 2026-07-26 00:13:55")
  NextElapseUSecMonotonic=infinity      ← nunca mais dispara
  LastTriggerUSec=Sat 2026-07-25 23:43:05
```

As unidades foram reiniciadas às 00:13:55 (leva da madrugada). Com `OnBootSec`
vencido e `OnUnitActiveSec=30min` sem uma ativação posterior em que se ancorar, o
timer ficou `elapsed` e **não tem próximo disparo**. Há mais de cinco horas o
guarda não roda.

O efeito prático é o pior possível para quem só quer jogar: **o estado que ela vê
hoje não é o estado que o Hefesto acha que impôs**, e o comportamento do jogo vai
mudar sozinho no próximo boot.

### 4. O desfazer é prometido na tela e não existe

`gui/main.glade:1880`, tooltip do botão "Este jogo não funciona":

> *"...Não fecha a Steam e dá para desfazer."*

`integrations/steam_launch_options.py:821`
(`remove_appid_from_steam_input_allowlist`) existe, está testada — e tem **zero
chamadores em `src/`**. Só `tests/unit/test_steam_launch_options_vdf.py` a chama.
Não há gatilho nenhum na interface.

### 5. Entrar na exceção mata o co-op de quatro, e ninguém avisa

`daemon/subsystems/gamepad.py` derruba o gamepad virtual e desliga o co-op ao
ativar a exceção. Na prática: num jogo da allowlist, o jogador 1 passa a jogar
pelo controle físico e **os outros três somem**. JOGO-01 chamava o estado
anterior de "loteria"; a cura trocou loteria por "um jogador só" — o que é
honesto, mas não está escrito em lugar nenhum da tela.

### 6. A mensagem manda clicar num botão que não existe, na aba errada

- `integrations/storm_doctor.py:148-149` e `:215` dizem *"clique 'Reaplicar fixes
  seguros'"*. O botão se chama **"Aplicar correções"** (`gui/main.glade:1904`,
  id `btn_storm_fix_safe`). Nenhum widget tem o rótulo citado.
- `docs/usage/jogos-e-mascaras.md:43` e o tooltip da máscara mandam usar *"o
  opt-in em 'Steam Input' na aba Emulação"*. Na aba Emulação existem só
  "Verificar" (`gui/main.glade:2279`) e "Desligar Steam Input"
  (`gui/main.glade:2286`) — **nenhum opt-in por jogo**. O opt-in está na aba
  **Sistema**, com o nome "Este jogo não funciona".

O diagnóstico que alimenta o cartão, rodado agora no ambiente dela:

```
[WARN] Steam Input LIGADO em 1 perfil(is) fora da allowlist — clique 'Reaplicar fixes seguros' para desligar
```

Uma repreensão, sobre um jogo que não é nomeado, mandando clicar num botão que
não existe.

### 7. O vigia permanente não está documentado

`docs/usage/troubleshooting.md:571` e `:581` apresentam `--apply` / `--restore`
como ações pontuais e dizem que `--keep-steam-input` "preserva a configuração
atual da Steam". Não há uma linha explicando que o install instala um guarda que
reaplica o desligamento a cada 30 minutos. A única menção ao guarda em toda a
documentação de usuário é incidental, em
`docs/usage/troubleshooting-8bitdo.md:213`. Quem lê o troubleshooting conclui que
pode ligar de volta pela Steam. O sistema desfaz.

Além disso, as duas units instaladas apontam na linha 2 para
`docs/process/sprints/FEAT-STEAM-INPUT-SELF-HEAL-01.md`. **O arquivo não existe.**

### 8. A contagem não nomeia jogo nenhum

`app/actions/emulation_actions.py:762-764` monta:

```
Steam Input: <estado> · exceção per-app: N jogo(s) — <extra>
```

"1 jogo(s)" é ilegível. Ela não tem como saber que o jogo é o Pragmata, nem que o
"1 perfil fora da allowlist" do outro cartão é o mesmo jogo visto do outro lado.

## Entregas

A ordem é a ordem de impacto sobre a pergunta dela.

1. **Tirar do produto a instrução de ir na Steam.**
   `app/actions/daemon_actions.py:313-317` é a única frase do Hefesto que ensina
   o gesto que ela não deveria precisar fazer, e ela é falsa para todo jogo fora
   da allowlist. Sai.
2. **Uma linha por jogo, com nome, no lugar da contagem.** "Pragmata — controle
   entregue pelo Hefesto", "Mullet Mad Jack — controle entregue pela Steam, sem
   co-op". Substitui `emulation_actions.py:762-764` e o WARN de
   `storm_doctor.py:148`.
3. **O botão de desfazer, que já está escrito.**
   `remove_appid_from_steam_input_allowlist` ganha gatilho ao lado de "Este jogo
   não funciona", com o mesmo recarregamento. Enquanto não tiver, a promessa de
   `gui/main.glade:1880` sai do tooltip — prometer desfazer sem desfazer é pior
   do que não prometer.
4. **Divergência vira pergunta, não repreensão.** Quando o `vdf` tiver Steam
   Input ligado num jogo fora da allowlist, a tela pergunta: *"você ligou o Steam
   Input em **Pragmata** pela Steam — quero manter ou desfazer?"*, com dois
   botões. Manter significa entrar na allowlist. É o que transforma a decisão
   técnica em uma escolha que ela consegue tomar sem saber o que é Steam Input.
5. **O aviso de co-op no clique.** Com mais de um controle presente, "Este jogo
   não funciona" avisa antes: *"neste jogo só o controle 1 vai funcionar"*.
6. **A frase durante o jogo.** `daemon/subsystems/gamepad.py:310`
   (`steam_input_vpad_suspenso`) existe exatamente para responder "por que a
   emulação aparece desligada com o jogo aberto?" e **não tem consumidor na
   GUI** — grep em `src/` só acha a definição e os usos internos do próprio
   módulo. Sem ela, um jogo da allowlist parece ter desligado o Hefesto sozinho,
   o que casa com a queixa 2 do rollback.
7. **Consertar o vigia e mostrar que ele está vivo.** O timer `elapsed` sem
   próximo disparo é um defeito de unidade (`OnBootSec` vencido sem âncora). E o
   cartão precisa dizer, em uma linha, se o guarda está ativo — porque é ele que
   decide se a escolha dela sobrevive ao próximo boot.
8. **Documentar o guarda, ou parar de instalá-lo em silêncio.**
   `docs/usage/troubleshooting.md` descreve um one-shot; o produto instala um
   vigia permanente. E o sprint citado pelas units
   (`FEAT-STEAM-INPUT-SELF-HEAL-01.md`) precisa existir ou sair da referência.
9. **Corrigir os dois ponteiros errados:** o rótulo do botão em
   `storm_doctor.py:148-149` e `:215`, e a aba citada em
   `docs/usage/jogos-e-mascaras.md:43` e no tooltip da máscara.

## Como validar

Tudo olhando a tela, sem terminal.

1. Abrir o Hefesto na aba Sistema. Existe **uma lista de jogos com nome** — não
   uma contagem. Pragmata aparece nela.
2. Para o jogo em que ela ligou o Steam Input pela Steam, a tela **pergunta** se
   é para manter ou desfazer, em vez de mandar clicar em algo.
3. Escolher "manter". Reiniciar a máquina. Abrir o jogo. **Continua valendo** —
   o guarda não desfez.
4. Escolher "desfazer" em outro jogo. A linha daquele jogo muda na hora, e o
   jogo volta a ser entregue pelo Hefesto.
5. Clicar "Este jogo não funciona" com quatro controles na mesa. Antes de aplicar,
   a tela avisa que só o controle 1 vai funcionar naquele jogo.
6. Com um jogo da allowlist aberto, a aba Emulação **não** parece desligada
   sozinha: diz que saiu da frente de propósito, e por qual jogo.
7. Em nenhum ponto da interface aparece a instrução de ir na Steam mexer em
   Propriedades → Controle.

**Critério que resume:** ela nunca precisa responder "ligo a entrada Steam ou
não?" — a tela nomeia o jogo, faz a pergunta em português de quem joga, e a
resposta dela sobrevive ao próximo boot.

## O que NÃO foi medido

- **Não abri nenhum jogo.** Nada aqui foi observado com sessão de jogo em
  andamento — inclusive o efeito da exceção sobre o co-op de quatro, que é
  leitura de código, não observação.
- **Não vi a tela.** Não houve captura nesta sessão; toda afirmação sobre a
  janela vem do `main.glade` e dos mixins.
- **Não sei quem ligou o Steam Input do Pragmata** — se foi ela seguindo o toast,
  ou a própria Steam num update.
- **Não testei se `UseSteamControllerConfig="2"` per-app funciona com
  `SteamController_PSSupport="0"` global.** Esta é a premissa em que a exceção
  inteira se apoia: o produto sempre zera o global e conta com o per-app para
  entregar o DualSense pela Steam. Se a Steam moderna não honrar o per-app com o
  suporte global de PlayStation desligado, **a exceção é decorativa e falha em
  silêncio** — e o botão "Este jogo não funciona" nunca funcionou de verdade.
  Precisa de um teste com jogo aberto, e é o primeiro passo desta sprint.
