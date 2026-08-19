# PROVA-NO-PLÁSTICO-01 — o roteiro de quarenta minutos com o controle na mão

19/08/2026. A onda de hoje (`a76e16e`, 52 arquivos) foi construída inteira contra
dublê; a ordem abaixo é por **custo do silêncio**, não pela de construção. A
máquina dela às 12:40: daemon ativo desde 11:35:29 (tem o código da onda);
`pontes_confirmadas: {}`, **nenhum jogo carimbado**; **zero** `aviso_de_modo_*` e
**zero** `ponte_troca_pedida_por_gesto` no journal de hoje — **o gesto nunca foi
apertado neste daemon**; 3 appids na allowlist, os 3 ligados, e **DON'T SCREAM
(2497900) e Duskfade (2542020) fora dela**. A Steam está fechada
(`steam_aberta: false`): é a janela de escrita.

## O PLANO DE VOLTA — digite ANTES de começar

Nenhum gesto **recria** o vpad, e o Nativo não tem volta pelo controle. Da raiz:

```bash
.venv/bin/hefesto-dualsense4unix gamepad status --json           # o que está de pé
.venv/bin/hefesto-dualsense4unix gamepad on --flavor dualsense   # traz de volta
.venv/bin/hefesto-dualsense4unix native off                      # sai do Nativo
systemctl --user restart hefesto-dualsense4unix                  # último recurso
```

## BLOCO A — eu meço sozinha, ela não faz nada (~30 s, antes e depois de cada passo)

| # | Comando | O que a saída significa |
|---|---|---|
| A1 | `systemctl --user show hefesto-dualsense4unix -p ActiveEnterTimestamp` | Anterior a 11:35 de hoje = daemon velho, **recusa o campo `ponte`**; o sintoma é a AUSÊNCIA de dado, não erro. Tudo abaixo fica inválido |
| A2 | `.venv/bin/hefesto-dualsense4unix gamepad status --json` | `flavor` é a ponte VIVA. `degraded: true` ou `ff_supported: false` = o vpad subiu torto |
| A3 | `.venv/bin/python -c "from hefesto_dualsense4unix.app.ipc_bridge import _run_call;print(_run_call('daemon.status',{})['pontes_confirmadas'])"` | `{}` = nada carimbado. Uma entrada por appid = o produto APRENDEU aquela ponte |
| A4 | `.venv/bin/python -m hefesto_dualsense4unix.integrations.steam_input_ponte --estado` | `pendentes` não vazio = a lista pede e a ponte não está de pé. `steam_aberta: true` = escrever agora é inútil, a Steam engole |
| A5 | `journalctl --user -u hefesto-dualsense4unix --since "-10min" \| grep -E "aviso_de_modo\|ponte_troca_pedida\|ponte_ciclo_skip"` | `aviso_de_modo_piscado controles_escritos=0` = pediu e **nenhum** controle recebeu; `=1` = escreveu no plástico; `aviso_de_modo_sem_backend` = a rota não existe naquele transporte |

## BLOCO B — precisa da MÃO dela

### B1 — os dois appids na allowlist, no MESMO ciclo da Steam (7 min, primeiro)

Preço: **exige a Steam FECHADA** — ela regrava o `localconfig.vdf` ao sair e
engole edição feita por baixo. Não derruba o controle.

```bash
cat >> ~/.config/hefesto-dualsense4unix/steam_input_apps.txt <<'FIM'
2497900   # DON'T SCREAM (Unreal/XInput: quem entrega o dispositivo é a Steam)
2542020   # Duskfade
FIM
.venv/bin/python -m hefesto_dualsense4unix.integrations.steam_input_ponte --ligar
```

- `resultado=ponte_ligada` e `2497900: ligado` → abra o jogo. **Controle na tela
  = a hipótese vive**; controle ausente = ela morre e para de custar sessões.
- `resultado=adiada` → a Steam ainda está viva: feche-a e repita. E
  `reguas_divergem` → recusa deliberada: é `ARVORE-ERRADA-01`, não erro dela.

### B2 — `PS + R3` no CABO, sem jogo aberto (2 min)

Segure `PS` e clique o **stick direito**. Ciclo: DualSense → Xbox →
mouse+teclado; recria o vpad, mas sem jogo não há handle a invalidar. Observar
três piscadas rápidas (~0,5 s) e a cor do perfil **voltando**. Piscada **e**
`ponte_troca_pedida_por_gesto` em A5 = o caminho inteiro anda; nenhuma das duas =
o gesto não chegou ao daemon; a linha sem a piscada = a **rota da lightbar**
falhou. Este passo separa os dois defeitos.

### B3 — o mesmo gesto com o JOGO ABERTO e o controle na mão (5 min)

**Preço alto, medido em 23/07 (R-04): a troca destrói e recria o vpad, e o jogo
perde o handle que abriu** — pode exigir replug lógico (menu de controles do
jogo) ou reabrir. Antes da troca vêm dois pulsos VERMELHOS = "isto pode derrubar
o controle"; os dois pulsos **e depois um vermelho longo** = o vpad NÃO subiu,
use o plano de volta. Jogo mudo depois: entre no menu de controles dele.

### B4, B5, B6 — os três de fechamento

**B4, trocar de modo pela JANELA (3 min):** tem de ver o mesmo que o gesto, e é a
única via para **azul claro (Steam Input)** e **branco (Modo Nativo)** — o gesto
não liga um nem entra no outro. **B5, o carimbo por jogo (5 min):** abra um jogo
SEM carimbo, aperte `PS + R3` até ele responder, confira A3 — entrada nova = o
produto aprendeu, `{}` ainda = o carimbo não saiu do gesto. **B6, repetir B2 pelo
RÁDIO (5 min):** solte o cabo, pareie por BT, repita B2 — é aqui que a **rota
avulsa por hidraw** prova o caso "Steam aberta", a que pinta com outro processo
dono do nó; o replug troca o transporte e pode renumerar o controle.

## BLOCO C — o OLHO dela, e nenhum agente fecha isto

[PROVA-DE-TELA-01](2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md)
no plástico: 5 cores × 2 transportes × Steam aberta/fechada = **20 células**.

| Modo | Cor | Hex | Como chegar |
|---|---|---|---|
| Steam Input | azul claro | `#8be9fd` | janela / jogo da allowlist |
| máscara Xbox | verde claro | `#50fa7b` | `PS + R3` |
| Modo Nativo | branco | `#f8f8f2` | janela ou `native on` |
| máscara DualSense | rosa (marca) | `#ff79c6` | `PS + R3` |
| mouse + teclado | âmbar | `#ffb86c` | `PS + R3` |

A piscada é 3 × (0,09 s acesa + 0,07 s apagada), e o apagado é PRETO, não brilho
zero: `luz.lightbar.brilho` tem `aciona=não` nos dois transportes no
[mapa de canais](../../data/mapa-controles.csv) — quem apaga é a COR. Jogo que
pinta a lightbar sozinho pode sobrepintar o aviso: é sinal, não garantia, e a
célula vira "sobrepintado", nunca falha.

## CRITÉRIOS DE PARADA

**Com resposta:** B1 dá `ponte_ligada` e o jogo mostra (ou não) controle; B2 dá
piscada e linha no journal; C tem as 20 células preenchidas. **Sem resposta**, e
o que medir depois: piscada ausente com `controles_escritos=0` pede medir quem
segura o hidraw do físico (`lsof /dev/hidraw*` com privilégio) antes de culpar o
código; `aviso_de_modo_sobreposto` repetido é duas trocas caindo uma sobre a
outra (repita com 2 s de espaço); jogo sem controle depois de B1 pede conferir o
`UseSteamControllerConfig` na árvore `UserLocalConfigStore/apps` — só ela conta.

## O QUE ESTE ROTEIRO **NÃO** RESPONDE

1. **Não prova o ciclo `uninstall` → `install`** (o de hoje às 04:24 é anterior à
   onda): os módulos novos numa árvore recém-clonada, o `btmgmt` presente depois
   do install e a reversão do Alias do adaptador seguem abertos.
2. **Não preenche `O JOGO RECEBEU` nem `O JOGO REAGIU`**: B3 toca um jogo; a
   coluna pede o ensaio jogo a jogo, nos dois transportes.
3. **Não valida o AppImage GUI**, que bundla os loaders do gdk-pixbuf da máquina
   de build; a lacuna do `librsvg2-common` está declarada no portão.
4. **Piscada vista não é ponte confirmada:** a cor diz o modo, e quem diz que o
   jogo funcionou é o carimbo do B5 — que só nasce da mão dela.
