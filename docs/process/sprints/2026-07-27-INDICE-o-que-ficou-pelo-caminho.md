# O que ficou pelo caminho — fechamento da sessão de 27/07/2026

- **Fechado em:** 27/07/2026, 22h40, a pedido dela: *"levanta o que ficou pelo
  caminho"*
- **Commit da leva:** `e96dea8`, publicado em `restauro/inicio-da-sessao`
- **Serve para:** a próxima sessão começar sabendo o que está pendente e por quê

## O que entrou, em uma linha

Anti-emoji curado dos dois lados; portões de commit e de CI construídos; espaço
redistribuído em cinco abas; aba Status com glifos legíveis e analógicos
alinhados; o desfazer do Steam Input passou a existir. **5587 testes verdes**,
`mypy --strict` limpo, quatro gates em zero.

## Faixa 1 — o que desfaz trabalho dela

### EMPATE-01 — CRÍTICA, e é a primeira da fila

O controle dela está **sem cor** porque três perfis catch-all empatam em
prioridade 0 e o desempate é a **ordem alfabética do arquivo**: `fallback`
(lightbar cinza `[40,40,40]`) vence `vitoria` (roxo). E o cinza é **semente do
projeto** — `assets/profiles_default/fallback.json:11` —, então toda instalação
nova nasce assim.

Não foi executada porque mexe no caminho que roda durante a partida, e a regra da
casa é que isso entra sozinho, com ela vendo a cor mudar antes e depois.

Documento: [EMPATE-01](2026-07-27-EMPATE-01-tres-perfis-empatados-e-quem-ganha-e-o-alfabeto.md)

## Faixa 2 — o que ela vê

| Sprint | O que falta |
|---|---|
| [STATUS-SIMETRIA-02](2026-07-27-STATUS-SIMETRIA-02-distanciar-nao-e-organizar.md) | os cinco defeitos que ela nomeou olhando a aba Status: títulos com número de linhas diferente, touchpad sem bloco próprio, botões mal distribuídos, vazios, e falta o som |
| [MIC-PRESENTE-01](2026-07-27-MIC-PRESENTE-01-o-microfone-nao-pode-sumir-da-faixa.md) | o microfone some da faixa e faz o layout inteiro pular. Entra junto com a de cima, porque muda a distribuição |
| [LIGHTBAR-JOGADOR-01](2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | a aba mostra o rascunho, não o que está aplicado; o jogador vira protagonista; o painel das cinco luzes sai |
| [PALAVRA-01](2026-07-27-PALAVRA-01-a-janela-fala-a-lingua-de-quem-joga.md) | 24 textos em minúscula, jargão, 188 controles sem tooltip, e o DSX sai do nome da aba |

## O que ficou incompleto dentro do que foi entregue

- **A entrega 1 da STATUS-SIMETRIA-01** (microfone à direita dos analógicos) não
  apareceu, porque o microfone está escondido. Depende da MIC-PRESENTE-01.
- **As cinco caixas fantasma `player_led_1..5` continuam no glade.** Só os sinais
  mortos saíram. Elas são o único lugar onde a interface guarda o desenho
  escolhido; saem no mesmo passe em que o Python guardar esse estado fora dos
  widgets.
- **Dois handlers ficaram órfãos do glade:** `on_emulation_open_toml` e
  `on_player_led_toggled`. O primeiro pode sair junto com o botão removido; o
  segundo tem o resto do arquivo vivo e necessário.
- **O terceiro teste da BOTÃO-QUE-NÃO-MENTE-01** não foi escrito, por medição: a
  regra proposta acusa zero handlers hoje, e escrevê-la assim viraria
  teste-muralha.
- **A entrega E5 da VÃO-01** (tokens de espaçamento) ficou de fora de propósito:
  é a única não reversível em uma linha.

## O que nunca foi medido, e devia

- **O daemon está vivo e ninguém consultou o estado real dele.** Os números de
  flapping que sustentam as sprints de perfil são de 26/07 e **não foram
  reproduzidos**.
- **`autoswitch_locked.flag` está ligado desde 24/07 20:42** — é a configuração
  real dela, e **nenhuma sprint de perfil diz o que muda com o cadeado ligado**.
- **A escala de fonte máxima (8)** nunca foi medida. A escala dela é 3, que é o
  padrão e não uma escolha. O pior caso do orçamento de largura é a 8.
- **`app/compact_window.py` e a bandeja** ficaram fora de todos os levantamentos.
  Se a segunda janela repete card ou rótulos, as renomeações saem pela metade.
- **A aba Status com dois cards lado a lado.** Toda a avaliação foi com um
  controle só.
- **Os 734 testes de interface continuam pulando no CI**, e o pulo é
  **silencioso** (`importorskip`), não uma falha.

## Dívida de processo

- **`PROVA-DE-TELA-01` existe como documento e nunca foi aplicada.** A regra da
  casa diz que ela é "a última a construir e a primeira a usar" — e esta leva foi
  validada de olho, mas sem a folha preenchida.
- **`CONTAGEM-E-COOP-01`** continua sem documento.
- **Três identificadores seguem existindo só em mensagem de commit:**
  `MIC-FAIXA-01`, `SLOT-JOGADOR-01` e `RUMBLE-PRESO-01`.

## Alertas de ambiente, fora deste repositório

Os dois foram curados hoje, mas moram fora da árvore e podem voltar:

1. **O `andromeda-autosync` commita `~/.config/zsh` a cada 10 minutos** e apaga
   qualquer linha com o token de co-autoria, inclusive dentro de código. Quebrou
   o higienizador com `TypeError` duas vezes durante a entrega.
2. **O self-heal reinstala o hook de commit de hora em hora** a partir de uma
   fonte canônica. A cura foi propagada para as duas pontas e o autosync já
   commitou — mas qualquer edição futura precisa fazer o mesmo.

## O erro meu que vale lembrar na próxima

Rebaixei a EMPATE-01 usando a tela como testemunha (*"Perfil ativo: Nenhum, logo
não está mordendo"*). O controle estava cinza o tempo todo, e ela achou em dois
segundos olhando o hardware.

**Quando a tela é suspeita, ela não pode ser a testemunha.**
