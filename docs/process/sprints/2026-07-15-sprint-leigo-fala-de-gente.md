# Sprint SPRINT-LEIGO-01 — a interface fala de gente

Pedido da mantenedora (2026-07-15): *"A interface, nome dos botões está de difícil
entendimento para um leigo… não foi verificado conflito de melhoria de cada aba da
interface por palavras mais simples e direta… precisamos vender melhor o programa."*

E, sobre o checkbox de co-op: *"esse quadrado do click não deveria aparecer, ninguém
conecta dois controles no pc esperando que os dois controles controlem a mesma pessoa.
ele deveria ficar confirmado por default mas não aparecer pro user."*

Inventário completo (270 textos, 31 arquivos):
[`2026-07-15-anexo-inventario-de-textos.md`](2026-07-15-anexo-inventario-de-textos.md).

## Princípio

Todo texto responde à pergunta **da usuária**, não descreve a **implementação**.
Se a palavra só existe porque o código a usa (`daemon`, `uinput`, `hidraw`, `máscara`,
`vpad`, `co-op`, `flavor`, `broadcast`, `throttle`, `unit`, `regex`, `CSV`, `JSON`,
`KEY_*`, `rc=1`), ela não aparece na tela — ou aparece só no modo avançado.

## Itens

### LEIGO-01 — Sumir com o checkbox de co-op (a queixa nº 2, literal)

**Atenção — a ordem aqui importa.** O checkbox é o *opt-out visível* de um estado que
**dois outros caminhos desligam pelas costas**. Tirá-lo da tela sem fechar esses caminhos
antes deixa a usuária com o co-op desligado **e sem como religar**:

1. **O applet**: entrar em "Controlar o PC" chama `set_coop(false)` com `origin=manual`
   → **grava o opt-out em disco** (`coop_disabled.flag`). A GUI foi corrigida para
   *preservar* a preferência nessa transição (`home_actions.py:433-435`); o applet não.
   Arquivo: `packaging/cosmic-applet/src/app.rs`.
2. **Os perfis**: o campo `coop` tem default **False** no esquema **e** no editor →
   **todo perfil salvo pela GUI** carrega `coop: false` e desliga o co-op ao ativar.
   Arquivos: esquema de perfil, `app/actions/profiles_actions.py:219-221` (onde o mesmo
   conceito ainda aparece **com outro nome**), `daemon/lifecycle.py:1017-1019`.

Só depois disso:
- Cada controle é um jogador. **Sempre.** O checkbox sai da UI
  (`app/actions/home_actions.py:157-162`) e `coop.enabled` nasce ligado em todas as portas
  de entrada (GUI, applet, CLI, perfil).
- Migrar os perfis já salvos (`coop: false` → herdar o padrão).
- No lugar, só informação: **"2 controles = 2 jogadores"**.
- **Aceite**: não existe caminho — GUI, applet, CLI ou perfil — que faça dois controles
  virarem o mesmo jogador; plugar o segundo controle cria P2 sem nenhum clique; perfis
  antigos não desligam o co-op; nenhum `coop_disabled.flag` é escrito.

### LEIGO-01b — E os números de jogador precisam ser verdade
Achado que impede o LEIGO-01 de ser só cosmético: os cards rotulam **P1/P2/P3 pela
posição na lista** (`idx+1`) **sem olhar `coop.enabled`** — com co-op desligado todos os
controles são o mesmo jogador e a numeração **mente**; com co-op ligado, o número real vem
de `CoopManager._next_player_index` (que **reusa** índices) e diverge da ordem da lista.
Some-se a isso: os slots **embaralham quando o P1 cai e volta** — os jogadores trocam de
personagem no meio da partida (ver `4P-02`).
- **Aceite**: o número no card é o número que o jogo vê, sempre.

### LEIGO-02 — Aba Início: dizer o essencial e calar o resto
- Arquivos: `app/actions/home_actions.py:47-74`.
- A frase de recomendação de 3 linhas (`_MODE_DESCRIPTIONS["gamepad"]`) cita "máscara
  Xbox 360", "opções da Steam" e "aba Daemon → Copiar opções p/ jogos". Ela só existe
  para contornar o defeito que o `SPRINT-UHID-VPAD-01` cura — **remover junto com ele**.
- O `_GLOSSARY` do rodapé enfileira 4 conceitos numa linha ("Modo jogo", "Pausar",
  "Jogar direto", "Desligar Hefesto") — três deles conceitos que o `SPRINT-HARMONIA-01`
  elimina. Reduzir ao que sobrar.
- Cards de controle: `USB · primário · 95%` + `…c311f0`. O hash do MAC não significa
  nada para quem usa; vira identificação por **cor da lightbar** ("Controle 1 — P1 ·
  azul · pelo cabo · 95%"), com o MAC só no modo avançado.
- **Aceite**: a aba Início inteira lida por alguém que nunca ouviu "máscara" ou "daemon"
  sem nenhuma dúvida sobre o que fazer.

### LEIGO-03 — "Daemon" vira "Sistema", e o systemd some
- Arquivos: `gui/main.glade:1730,1558,1582…`, `app/actions/daemon_actions.py`.
- Hoje expõe `Unit: hefesto-dualsense4unix.service`, a **saída crua de `systemctl
  status`** e toasts com `rc=N`. Para quem usa importa: está funcionando? liga sozinho?
  está tudo saudável? — e o botão "Copiar opções p/ jogos", que pertence à Início (ou
  desaparece, com o uhid).
- `Iniciar` deveria ser invisível (o autostart já existe); logs vão para "ver detalhes".
- **Aceite**: nenhuma string com `systemd`, `unit`, `rc=`, `.service` fora do avançado.

### LEIGO-04 — Gatilhos: nomes de pessoa, não de firmware
- Arquivos: `app/actions/trigger_specs.py`, `app/actions/triggers_actions.py`.
- Hoje: `Rígido (Rigid)`, `Galope (Galloping)`, `Pulso A/B`, `Arma (Weapon)`,
  `Feedback em rampa`, `Vibração por posição`, `Custom (raw HID)` — 22 botões
  bilíngues, o inglês entre parênteses sem função.
- Renomear pelo **efeito sentido** (ex.: "Gatilho de arma — resistência até o disparo"),
  agrupar em "Comuns" e "Avançados", e mandar `Custom (raw HID)` para o avançado.
- **Aceite**: nenhum nome de preset em inglês na tela principal.

### LEIGO-05 — Teclado: sem `KEY_*` na cara
- Arquivos: `app/actions/input_actions.py`, `gui/main.glade`.
- Hoje a tabela mostra `KEY_LEFTALT+KEY_TAB`, `__OPEN_OSK__`, `KEY_SYSRQ`,
  `touchpad_left_press`. Trocar por nomes humanos ("Alt+Tab", "Abrir teclado na tela",
  "Print Screen", "Toque à esquerda do touchpad") e **capturar a tecla** em vez de pedir
  que a pessoa digite o identificador (achado: "Adicionar" não deixa escolher o botão).
- **Aceite**: dá para criar um atalho sem saber o que é `KEY_*`.

### LEIGO-06 — Rumble/Lightbar/Perfis: vocabulário
- `Motor fraco (weak)` / `Motor forte (strong)` → "Vibração leve" / "Vibração forte".
- `Política de rumble` → "Intensidade da vibração"; `Throttle mínimo: 20 ms` some.
- `Devolver rumble ao jogo` → "Deixar o jogo controlar a vibração".
- Perfis: coluna `Match` mostra os valores crus `criteria`/`any` → "Quando usar";
  `Prio` → "Prioridade"; `Sem opinião` → "Não mexer no modo";
  `Preview do perfil (JSON)` → "Detalhes técnicos" (avançado).
- **Aceite**: ver o anexo, seção por arquivo.

### LEIGO-06b — O preset do Sackboy mente o próprio nome
Arquivo: `assets/profiles_default/sackboy_nativo.json`. O nome (e o CHANGELOG) dizem
"Jogo direto (Sony)", mas o conteúdo é `mode.kind: "gamepad"`, `gamepad_flavor: "xbox"`,
`coop: true` — foi migrado na v3.13.0 (quando a máscara Xbox virou o caminho da vibração) e
**o nome ficou para trás**. Quem ativa acha que está jogando no modo nativo.
Cuidado: o preset já está instalado no disco de quem usa — renomear exige **migração**
(não basta trocar o arquivo, ou vira preset duplicado). Depois do
`SPRINT-UHID-VPAD-01` a escolha pode inclusive mudar de novo (com o vpad uhid, a máscara
DualSense passa a vibrar) — então o nome novo deve descrever **o jogo**, não a máquina:
`sackboy` + descrição.
- **Aceite**: nenhum preset shipado descreve um modo diferente do que ativa; migração
  testada a partir de um perfil já instalado.

### LEIGO-07 — Um vocabulário, todas as superfícies
- O mesmo recurso tem nomes diferentes por porta de entrada: "Modo Nativo" (CLI/applet)
  vs "Jogar direto (Sony)" (GUI); "Modo jogo" colidindo com "Jogar pelo Hefesto";
  "Sair" significando três coisas.
- Criar um **glossário canônico** (`docs/usage/vocabulario.md`) e um teste que falha se
  a GUI, o applet e a CLI divergirem nos termos-chave.
- **Aceite**: teste de paridade de vocabulário verde.

### LEIGO-08 — i18n: parar de sangrar
- Metade da UI é traduzível (gettext) e a **aba Início e a seção Modo dos Perfis são
  hardcoded** — justamente as telas que este sprint reescreve.
- Passar tudo por `_()` enquanto se reescreve (o custo é zero agora, alto depois).
- **Aceite**: nenhuma string visível fora de `_()`; `.po` atualizado.

### LEIGO-09 — Acentuação
- Achados: `Avancado` (glade:1459), `indisponivel`/`Area` (tray.py:273).
- Regra do projeto: manter limpas as linhas tocadas (`git blame`).
- **Aceite**: `validar-acentuacao` limpo nas linhas do sprint.

## Validação ao vivo

Roteiro do leigo, com os 2 controles conectados: abrir o app, plugar o segundo controle,
fazer os dois jogarem, mudar a cor de um deles, e sair — **sem perguntar nada a ninguém
e sem ler documentação**. Screenshot de cada aba, antes e depois.

## Ordem

LEIGO-01 (a queixa literal) → LEIGO-02 → LEIGO-03 → LEIGO-06 → LEIGO-04 → LEIGO-05 →
LEIGO-07/08/09 (varredura final, junto com o resto).
