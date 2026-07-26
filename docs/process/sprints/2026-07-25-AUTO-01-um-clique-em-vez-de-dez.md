# AUTO-01 — um clique em vez de dez

- **Status:** ENTREGUE em 25/07/2026 pelo commit `8fe735d`
- **Prioridade:** ALTA
- **Aberta em:** 25/07/2026

## O pedido

> "preciso de verdade que veja as features do projeto (…) à procura de facilidade
> do usuário: ao clicar em tal coisa, ele não precisar alterar 10 coisas em abas,
> fechar a Steam, abrir, aplicar x, y e z, tudo de forma manual mas de forma
> automática, o máximo que der."

Vinte e nove pontos de fricção foram mapeados. Esta sprint pega os que **impedem
os quatro jogadores**; os demais estão em AUTO-02 (Steam), AUTO-03 (fluxo de
jogo) e AUTO-04 (o que só existe no terminal).

## O achado que resume a queixa

**O instalador fecha e reabre a Steam duas vezes, e depois falha no terceiro
passo — porque ele mesmo acabou de reabrir a Steam.**

```
passo 11   install.sh:2146  → fecha, edita Steam Input, REABRE
passo 11b  install.sh:2191  → fecha, migra opções de lançamento, REABRE
passo 11c  install.sh:2220  → "Steam aberta" → recusa → ADIADO
```

O terceiro passo (`proton_pin --lock`) não tem a opção de fechar a Steam que os
outros dois têm. E a recusa é praticamente garantida: o passo imediatamente
anterior baixa cerca de 450 MB de Proton, dando minutos para a Steam voltar
sozinha. A mensagem final manda a usuária **rodar um comando no terminal**.

Isso é literalmente o que ela descreveu: fechar a Steam, abrir, aplicar x, y e z,
tudo manual.

## O que impede os quatro jogadores hoje

### AUTO-01.1 — a emulação de gamepad nasce desligada, e o co-op depende dela

`daemon/lifecycle.py:132` define a emulação como desligada por padrão, e
`daemon/subsystems/coop.py:186` só ativa o co-op quando ela está de pé. O
`coop_enabled=True` da inicialização é decorativo enquanto isso for falso.

**Numa instalação nova, quatro DualSense plugados alimentam um cursor só.**

Conserto: ligar a emulação quando houver dois ou mais controles físicos. Um
segundo controle na mesa é a declaração de intenção mais clara possível.

### AUTO-01.2 — co-op não existe na janela

`grep -ci coop gui/main.glade` → **zero**. A funcionalidade central do projeto —
quatro jogadores — só existe por linha de comando.

O próprio código admite: `utils/session.py:446` explica que uma migração precisou
existir porque, sem ela, o co-op ficaria desligado *"sem nenhum caminho de volta
na interface"*.

Conserto: um botão **"Preparar co-op (N jogadores)"** na aba Início encadeando
modo de jogo, ativação do co-op e renumeração. **Todo o IPC necessário já
existe** — é ligação, não implementação.

### AUTO-01.3 — o preset de co-op perde para sete outros perfis

Prioridades semeadas de fábrica:

```
80 sackboy_nativo   70 Aventura   65 Ação   60 FPS   60 point_and_click
55 Esportes   55 Corrida   50 Navegação   45 coop_local   10 bow   1 meu_perfil
```

O `coop_local` (45) perde até para o `Navegação` (50), que casa a janela da
Steam. **Abrir um jogo de co-op pela Steam entrega o perfil de navegação.**

Conserto: prioridade 75 ou mais. Uma linha.

### AUTO-01.4 — o instalador nunca aplica o wrapper aos jogos

O passo 11b roda apenas a migração — troca opções de lançamento venenosas
antigas. A função que aplica o wrapper a todos os jogos existe
(`integrations/steam_launch_options.py:466`) mas **não tem modo de linha de
comando** e não é chamada pelo instalador. Um jogo que nunca teve opção
venenosa **nunca recebe o wrapper** até alguém abrir a janela e clicar.

### AUTO-01.5 — dois donos do valor padrão de máscara

O daemon usa `dualsense` (`lifecycle.py:140`); a janela e os presets usam `xbox`
(`integrations/uinput_gamepad.py:136`). **`gamepad on` pela linha de comando e
"Jogar pelo Hefesto" pela janela entregam máscaras diferentes** — e a máscara
decide se o jogo reconhece o controle.

### AUTO-01.6 — a máscara escolhida na aba Início não persiste

`app/draft_config.py:476` reemite o modo fotografado na inicialização; só o
editor da aba Perfis grava a seção. Trocar a máscara na Início e clicar em
"Salvar Perfil" **perde a máscara**. É o mesmo mecanismo do ABAS-01.

### AUTO-01.7 — parâmetros de módulo que exigem reboot sem precisar

O caminho de instalação por pacote escreve os parâmetros a quente
(`scripts/install-host-udev.sh:306`); o `install.sh` **não**. Todos os
parâmetros envolvidos são graváveis em tempo de execução. Copiar três linhas faz
as curas de conexão valerem **sem reiniciar** — inclusive a do segundo DualSense
que some.

Relacionado: `--no-dkms` derruba os **três** módulos de uma vez, incluindo a cura
medida do "segundo DualSense some". Precisa de opções separadas.

## Defaults a rever

| item | hoje | deveria | por quê |
|---|---|---|---|
| vibração | `balanceado` = ×0,7 | `máximo` ou `auto` | o padrão entrega 70% da vibração sem avisar |
| presets de gênero | 10 de 12 sem seção de modo | os de jogo com modo `gamepad` | casa com MODO-01: perfil sem modo não liga nada |
| catch-all | **dois** semeados | um só | dois catch-all disputando é parte do veto de MODO-01 |
| `--help` do instalador | corta no meio | mostrar inteiro | omite opções reais |

## Ordem de execução

1. **AUTO-01.1 + .2 + .3** — o co-op deixa de exigir terminal e passa a
   acontecer. É o que desbloqueia os quatro jogadores.
2. **AUTO-01.5 + .6** — um dono para a máscara, e ela persiste.
3. **AUTO-01.4 + .7** — instalação que termina o serviço, sem reboot.
4. **Defaults** — baratos, e cada um remove uma surpresa.

## Critério de aceite

Instalação limpa, quatro controles plugados, jogo aberto: **quatro jogadores,
sem abrir terminal, sem editar arquivo, sem reiniciar nada.**

E o instalador termina **sem pedir nada** — nem um comando para copiar.
