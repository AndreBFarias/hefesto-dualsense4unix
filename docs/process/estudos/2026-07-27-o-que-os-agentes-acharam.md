# O que os agentes acharam — leva de 27/07/2026

- **Levantado em:** 27/07/2026, ao longo de três levas multiagente
- **Por quê:** o pedido foi *"documenta tudo... as descobertas dos agentes e
  afins"*. Achado que só existe em relatório de agente se perde
- **Como ler:** cada bloco é independente. O que **refuta** algo escrito vem
  primeiro, porque é o que muda decisão

## Parte 1 — o que foi REFUTADO, com medição

Uma passada adversarial foi rodada contra as conclusões da própria sessão. Ela
derrubou seis afirmações — três estavam escritas em sprints abertas, duas eram
instruções minhas aos agentes, e uma era um "conserto seguro" que teria reaberto
bug curado. **Todas reconferidas à mão antes de entrar aqui.**

### R1. O teto de 100 não era o que impedia o perfil do jogo de vencer

`profiles/manager.py:624` ordena por `(not p.e_catch_all, p.priority)` —
**especificidade antes de prioridade**. Qualquer perfil com critério vence
qualquer catch-all, mesmo com prioridade 0. E `manager.py:614-621` **veta todos
os catch-all** quando a janela é de jogo.

No disco dela: `pragmata.json` tem critério e prioridade **100**;
`vitoria.json` é catch-all e prioridade **0**. O estado que se dizia alcançável
só escrevendo `110` à mão está em 100, dentro da escala da janela.

**Consequência:** subir o teto para 200 não conserta nada medido e re-ranqueia
perfis de mesma especificidade. A regra R-A continua boa; a *prova* dela precisa
ser trocada.

### R2. As fontes da identidade visual ESTÃO instaladas

`fc-match "Space Grotesk"` e `fc-match "JetBrains Mono"` devolvem as fontes
certas. Cai a premissa de que "toda discussão de legibilidade aconteceu com a
fonte errada". O que sobra: `grep -c install_fonts install.sh` devolve **0** —
instalação nova continua sem elas.

### R3. Esconder aba não reindexa — mas há DOIS índices crus

Medido com GTK real: esconder a página 0 não muda `get_current_page()`.

O que é verdade e é pior: `status_actions.py:1189` (`!= 1`, o tique de 10 Hz dos
analógicos) e `home_actions.py:663` (`== 0`, o poller da aba Início) comparam
índice cru. Qualquer reordenação de abas quebra os dois **em silêncio e sem log**.

### R4. Tirar `vexpand` não são "duas linhas"

Os quatro roladores com `vexpand=True` têm **também** `packing expand=True`. No
GtkBox3 o filho recebe folga se qualquer um dos dois for verdadeiro. E
`max-content-height` limita o *pedido*, não a *alocação*.

### R5. Dar largura ao botão "Parar" reabriria bug curado

`main.glade:1266-1275` documenta que aquela fileira está **sem `homogeneous` de
propósito**: com ela, os quatro botões recebiam a largura do maior rótulo e a
fileira sozinha respondia por **1004 dos 1066 px** de largura mínima da janela
inteira. Ênfase por cor e ordem — nunca por largura.

### R6. Tirar `wrap=True` dos rótulos da Emulação sobe a largura mínima

Os textos reais são multi-palavra (`desligado (suprimido)`,
`ligado — DualSense (PS)`). Sem quebra, a largura mínima da aba sobe — e largura
é a **restrição dura** desta janela, porque a rolagem horizontal é `never`. Usar
`width-chars`.

## Parte 2 — instruções minhas que os agentes recusaram, e estavam certos

A regra dada a eles foi: *"se a instrução se revelar errada ao medir, NÃO faça e
explique. Medição vence instrução."* Três a exerceram.

### As cinco caixas fantasma NÃO podiam ser removidas

Mandei remover `player_led_1..5` do glade (invisíveis que declaravam sinal). O
agente mediu: elas são **o único lugar onde a interface guarda o desenho
escolhido**. `get_current_player_leds` (`lightbar_actions.py:860`) as lê pelo id,
e `builder.get_object` de id inexistente devolve `None` **sem estourar**, com
todos os bits em `False`.

Removê-las faria o "Aplicar o desenho" **apagar as cinco luzes** e gravar "tudo
apagado" no perfil dela logo depois de ela clicar em "Desenho do P1". Trocaria
dívida invisível por defeito visível.

Ele tirou só os cinco `<signal>`, que eram provadamente inalcançáveis — e é essa
a dívida que a sprint nomeava.

### O `cmd_steam.py` que mandei editar não existia

E o módulo mais próximo por busca (`cmd_doctor.py`) **não serve**: não é um
sub-app registrado, então comando novo ali seria inalcançável. O agente mediu os
pontos de entrada reais antes de escrever.

### O terceiro teste da BOTÃO-QUE-NÃO-MENTE-01 não foi escrito

A regra proposta era "handler que só escreve no rascunho, sem marca de pendente,
reprova". Rodada contra o código de hoje, ela acusa **zero** handlers — inclusive
os dois que a sprint nomeia, porque ambos repintam a prévia e um emite aviso.

Escrevê-lo assim viraria teste-muralha. O agente entregou os outros dois e
explicou. **Não entregar era a resposta certa.**

## Parte 3 — descobertas que ninguém tinha pedido

### O `andromeda-autosync` mutila arquivos a cada 10 minutos

Um segundo higienizador, descoberto durante a cura do primeiro. O timer commita
`~/.config/zsh` a cada 10 minutos, e um hook daquele repositório roda
`grep -viE '[Cc]o-[Aa]uthored-[Bb]y'` sobre tudo que estiver staged — apagando a
**linha inteira**, sem olhar se é mensagem de commit ou código.

Isso quebrou o `universal-sanitizer.py` com `TypeError` **duas vezes** durante a
entrega, porque a expressão regular dele contém esse token literalmente. Há
precedente: o commit `6260537`, de 20/03/2026, chama-se *"restaurar variaveis e
identidade removidas pelo auto-sanitize"*.

Por que nunca tinha aparecido: o arquivo existia havia anos e **nunca era
editado**, logo nunca era staged. Editá-lo foi o gatilho.

### O self-heal desfazia a cura do hook sozinho

O self-heal do ambiente dela, fora deste repositório, reinstala `~/.config/git/hooks/pre-commit` a
partir de `~/.config/zsh/hooks/pre-commit`, **de hora em hora**. Curar o hook em
uso sem propagar para a fonte canônica desfaz a cura no passe seguinte. Os dois
foram curados e o autosync já commitou.

### O cinza do `fallback` é semente do projeto

`assets/profiles_default/fallback.json:11` traz `"lightbar": [40, 40, 40]` —
cinza quase preto. **Toda instalação nova nasce assim.** Combinado com o empate
alfabético dos catch-all, é a causa medida de *"o controle no bt tá sem cor"*.

O `player_leds` do mesmo arquivo está **certo**: acender só a luz central é o
padrão PS5 para um jogador.

## Parte 4 — duas classes de defeito que apareceram duas vezes cada

### Teste-muralha: o portão que precisa de sujeira para provar que funciona

Aconteceu **duas vezes no mesmo dia**, com dois agentes diferentes:

1. o teste do portão de glifos usava as duas estrelas proibidas de
   `troubleshooting-8bitdo.md` — arquivo real — como material da prova;
2. o teste do portão de referências cravava `LINHA_DA_PROVA = 18` e
   `NOME_FANTASMA = "guardian.py"` e exigia `returncode == 1` **contra a árvore
   real**.

Nos dois casos, corrigir o defeito **quebrava o teste**. O segundo quebrou de
verdade: o agente corrigiu o ADR-011 (que era a tarefa dele) e o teste reprovou
por ele ter feito o trabalho certo.

**A cura, nos dois:** montar o defeito numa caixa de areia própria, e trocar o
teste contra a árvore real por um que trave o **zero**.

**A regra que fica:** um portão que precisa de sujeira na árvore para provar que
funciona deixa de provar no instante em que alguém limpa.

### Quando a tela é suspeita, ela não pode ser a testemunha

Rebaixei a EMPATE-01 de ALTA para MÉDIA com o argumento *"a aba Status diz
'Perfil ativo: Nenhum', logo o mecanismo não está mordendo"*.

Errado. "Perfil ativo: Nenhum" não prova que nenhum perfil forneceu os LEDs —
prova que **a tela não nomeia o vencedor**, que é parte do próprio defeito. A
pergunta certa não era à tela: era ao controle, que estava cinza o tempo todo.

Ela achou em dois segundos, olhando o controle: *"o controle no bt tá sem cor"*.

## Parte 5 — números que vale guardar

```
194  rótulos com texto na janela
  6  têm tooltip                     <- 188 não explicam nada
 24  textos de tela começam com letra minúscula
 13  termos técnicos crus no rótulo visível

145  controles acionáveis no cenário simples
 66  handlers do glade, todos vivos, zero órfãos
  0  GtkComboBox (todos viraram seletor segmentado, por bug de foco no cosmic-comp)

222  glifos protegidos pelo ADR-011 que o higienizador apagaria, em 5 arquivos
  0  portões rodando no caminho do commit, antes desta leva
```
