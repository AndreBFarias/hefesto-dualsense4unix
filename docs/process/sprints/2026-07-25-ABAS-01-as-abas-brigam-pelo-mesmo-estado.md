# ABAS-01 — as abas brigam pelo mesmo estado

- **Status:** ENTREGUE em 25/07/2026 pelo commit `d92b544`
- **Prioridade:** ALTA — há perda silenciosa de dados
- **Aberta em:** 25/07/2026

## O pedido

> "preciso que explore os conflitos entre as abas, procure por placeholders que
> temos que corrigir ou funções mockadas."

## O que estrutura todos os achados

Uma linha da tabela de atualização explica a maioria dos defeitos:

| aba | de onde se reconstrói ao entrar |
|---|---|
| Início, Emulação | **daemon** |
| Gatilhos, Lightbar, Rumble | **rascunho de edição** |
| **Perfis** | **disco** — nunca lê o rascunho |
| Sistema | systemd |

A aba **Perfis** é a única que edita e persiste perfil **sem nunca ler o
rascunho**. É de onde saem os três defeitos com perda de dados.

## Perda silenciosa de dados

### ABAS-01 — o "Salvar Perfil" do rodapé apaga o Modo que a aba Perfis gravou
`app/draft_config.py:476` · `app/actions/profiles_actions.py:1204`

A aba Perfis grava a seção `mode` **direto no disco** e nunca escreve de volta no
rascunho — não há uma única atribuição a `self.draft` no arquivo inteiro. O
rodapé, ao salvar com o mesmo nome, reemite o `mode` que fotografou na
inicialização.

Reprodução: aba Perfis → Modo = "Jogar pelo Hefesto" → Salvar *(grava certo)* →
aba Lightbar → muda a cor → rodapé "Salvar Perfil" → **a seção `mode` some do
arquivo**. Vale igual para critério de janela, prioridade e supressão.

Isso conecta com MODO-01: mesmo fazendo tudo certo, o modo do perfil evapora.

### ABAS-02 — arrastar o brilho em "Todos" destrói as cores por controle
`app/actions/lightbar_actions.py:138-174`

Com o alvo em "Todos", mover o controle de brilho **um pixel** limpa o campo de
cor de todos os ajustes por controle e não os re-semeia — a lista de alvos está
vazia nesse ramo. Controle 1 azul e Controle 2 vermelho viram nada, e o "Salvar
Perfil" persiste a perda. O evento dispara a cada movimento do arraste.

### ABAS-03 — renomear na aba Perfis descarta o rascunho inteiro
`app/actions/profiles_actions.py:1163`

A mesclagem com o rascunho só ocorre quando o nome bate com o perfil ativo. Ao
renomear, o nome já mudou — então a base vem **do disco** — e em seguida o perfil
antigo é apagado. Toda edição de cor, gatilho, vibração e teclado feita na sessão
é perdida, sem aviso.

### ABAS-04 — "Parar" a vibração não pega, e ela volta sozinha
`app/actions/rumble_actions.py:361`

"Parar" e "Devolver ao jogo" zeram os controles deslizantes mas **não escrevem no
rascunho**. O próximo "Aplicar" de qualquer aba re-trava a vibração que ela
mandou parar, e voltar à aba Rumble repinta os valores antigos — a aba **mente**
sobre o estado parado.

## Ações que vazam entre abas

### ABAS-05 — o "Desligar" dos gatilhos destrava LED e vibração de outras abas
`app/actions/triggers_actions.py:562` → `daemon/state_store.py:190`

`trigger.reset` limpa a trava manual **sem categoria** — apaga `led`, `trigger` e
`rumble` de uma vez. A própria documentação do arquivo diz que a granularidade por
categoria existe justamente para isso não acontecer. Efeito: desligar **um**
gatilho reabre a troca automática para reescrever a cor que a aba Lightbar acabou
de aplicar. **É a queixa histórica "a config que eu deixo não fica".**

### ABAS-06 — o "Desligar" é o único comando da janela que ainda vai para todos
`app/actions/triggers_actions.py:562`

`trigger_reset` não tem parâmetro de controle. Com "Controle 2" selecionado,
"Desligar" zera o gatilho **dos quatro**. O "Aplicar" ao lado manda para um só.
O mesmo defeito foi corrigido no "Apagar" da Lightbar e não foi replicado aqui.

### ABAS-07 — a aba Rumble inteira ignora o seletor de alvo
`app/ipc_bridge.py:361`

O tooltip do seletor promete literalmente *"controle alvo das ações (lightbar,
gatilhos, LEDs, **rumble**)"*. Nenhum dos comandos de vibração aceita alvo. A
janela mostra "Editando: Controle 2" e vibra os quatro.

### ABAS-08 — todo "Aplicar" congela a troca automática, sem dizer
`daemon/ipc_draft_applier.py:51`

O rascunho emite as três seções **sempre**, então qualquer "Aplicar" — mesmo o
feito só porque ela mexeu no brilho — arma a trava manual para LED, gatilho e
vibração. Nenhum aviso na tela. E o único jeito de soltar pela janela é o
"Desligar" dos gatilhos, que é o ABAS-05.

## Placeholders e código morto

### PLACEHOLDER-01 — a funcionalidade de microfone no rascunho não tem widget
`app/draft_config.py:140`

A documentação do `MIC-EXPOSE-01` afirma que o campo existia *"só dentro do
dataclass do daemon — nenhuma superfície o mostrava nem o editava"*. **Continua
exatamente assim**: não há widget no glade. O campo nunca fica sujo, então o
"Aplicar" nunca envia a seção de microfone. Casa com MIC-USB-01.

### PLACEHOLDER-04 — botão que abre um arquivo que o daemon não lê
`app/actions/emulation_actions.py:274`

O botão **cria** `daemon.toml` e o conteúdo escrito começa com
`"# REFERÊNCIA — o daemon NÃO lê este arquivo."` A janela oferece um botão que
abre um editor para configuração inerte.

### PLACEHOLDER-05 — falha da camada de co-op reportada como sucesso
`daemon/subsystems/coop.py:1084`

A exceção é registrada como aviso e a função **devolve sucesso**; o cache local
não é atualizado. O chamador acredita ter aplicado, e o cache diverge do hardware.

### PLACEHOLDER-12 — os cartões inventam valores em vez de mostrar ausência
`app/widgets/controller_card.py:1042`

Gatilho ausente vira `0` e analógico ausente vira centro — desenhados como se
fossem leitura real. O comentário do próprio arquivo promete o oposto: *"`—`
honesto, nunca o último valor congelado"*.

### Funções sem nenhum chamador
`_query_gamepad_state` · `_stop_metrics` *(o servidor de métricas nunca é
encerrado)* · `_stop_hotkey_manager` · `_stop_mouse_emulation` · `_start_mic_hotkey`
· `_stop_plugins` · `_read_player_calibration` · `reset_counters` · `mark_disconnected`
· `short_button_label` · `_identity_for`.

E **`speaker.set`** no IPC, sem um único chamador no produto — enquanto `mic.set`,
que ela precisa, não existe.

## Contradições visíveis na tela

- **ABAS-11** — a aba Navegação DSX contradiz a si mesma: a legenda estática diz
  que o X é o botão esquerdo do mouse, e o editor logo abaixo oferece o X para
  atribuir tecla, escolhendo-o como primeiro candidato. Com o mouse ligado, o X
  vira clique **e** espaço. O R3 é pior: mapeado para teclado virtual num lugar e
  botão do meio no outro.
- **ABAS-16** — oito donos do valor padrão de máscara, num módulo criado
  explicitamente para haver só um.
- **ABAS-17** — os dois caminhos de "criar perfil" usam prioridades padrão
  diferentes (5 e 0) para o mesmo conceito.
- **PLACEHOLDER-10** — os multiplicadores de vibração existem em três lugares,
  incluindo texto fixo no XML da janela, com valores que vivem num quarto.
- **PLACEHOLDER-17** — a janela mostra `docs/usage/jogos-e-mascaras.md` e
  `KEY_*`/`__OPEN_OSK__` para quem instalou pelo pacote.

## O que foi verificado e está correto

Vale registrar para ninguém reauditar: **os 66 manipuladores de sinal do glade
existem em Python** — nenhum botão morto; **nenhum import morto** em todo o
código; o cartão de atalhos da aba Emulação é alimentado do gerenciador vivo; e
os travessões iniciais dos rótulos são a convenção honesta da casa, substituídos
em tempo de execução.

## Ordem de execução

1. **ABAS-01, -02, -03, -04** — perda de dados. A raiz comum é a aba Perfis não
   reconciliar com o rascunho; consertar isso resolve três de uma vez.
2. **ABAS-05 e -06** — o botão "Desligar" faz três coisas erradas ao mesmo tempo.
3. **ABAS-07 e -08** — honestidade do alvo e da trava. Ou o tooltip passa a ser
   verdade, ou o texto muda.
4. **PLACEHOLDER-01, -04, -05, -12** — o que a janela promete e não entrega.
5. **Código morto** — remover, ou dar uso e testar. Ficar no meio é o pior dos
   três.

## Critério de aceite

**Nenhuma sequência de cliques entre abas pode perder configuração sem aviso.**
É o teste que resume a sprint, e o que ela vem relatando desde 23/07 como *"a
config que eu deixo nunca é respeitada"*.
