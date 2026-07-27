# O mapa do projeto — índice do estudo de 26-27/07/2026

- **Levantado em:** 26-27/07/2026, sobre `restauro/inicio-da-sessao` / `v0.2.0`
- **Por quê:** o pedido foi *"estude o projeto... veja todos os docs que forem
  necessários para ter uma visão total"*. O resultado ficou grande demais para
  caber numa conversa, e conhecimento que só existe numa conversa se perde
- **Como ler:** cada mapa é independente. Este índice diz o que há em cada um e
  registra o que o estudo achou de errado

## Os mapas

| Documento | Cobre |
|---|---|
| [Arquitetura: daemon, vpad e broker](2026-07-27-mapa-arquitetura-daemon-vpad-e-broker.md) | O fluxo do dispositivo até o jogo; por que o vpad é HID e não uinput; por que existe um serviço root; as seis camadas de precedência |
| [Domínio: DualSense, HID e Bluetooth](2026-07-27-mapa-dominio-dualsense-hid-e-bluetooth.md) | Formato dos relatórios, offsets, CRC; cada recurso do hardware; o microfone por rádio; os problemas de Linux que o projeto resolve |
| [Sistema: instalação, udev, DKMS](2026-07-27-mapa-sistema-instalacao-e-empacotamento.md) | O que o instalador toca no host; os três módulos de kernel; a ordem das regras udev; CI e empacotamento |
| [Interfaces e suíte de testes](2026-07-27-mapa-interfaces-e-suite-de-testes.md) | As cinco superfícies de UI; as nove abas; a árvore da CLI; os números e as quatro lacunas da suíte |
| [Decisões e protocolos](2026-07-27-mapa-decisoes-e-protocolos.md) | Os 19 ADRs em uma linha; IPC, UDP, gatilhos; sala limpa; as premissas fundadoras |
| [Inventário de botões da janela](2026-07-27-inventario-de-botoes-da-janela.md) | Todos os 145 controles, um a um, classificados e contados |

## A linha do tempo, para quem chega agora

O repositório é um **fork**. O `main` do upstream parou em `398d3ed` (05/05/2026)
e o último lançamento de lá é a **v3.0.0, de 28/04**. Todo o produto atual vive
no fork.

| Período | O que aconteceu |
|---|---|
| 20-27/04 | Nascimento: alfa, GUI GTK3, daemon, UDP, perfis. Rebrand e 6 sprints de robustez (v3.0.0) |
| 16-23/05 | COSMIC/Wayland, i18n, robustez (v3.1 a v3.8.2) |
| 26/06-14/07 | **A guerra do storm USB.** Auditoria multiagente, causa-raiz eleita e depois **refutada**; cura por quirk de módulo; multi-controle de verdade (v3.12.0) |
| 17-24/07 | Auditorias grandes: 65 defeitos viram 24 causas-raiz, todas corrigidas (v4.0.0) |
| 24/07 | **A renumeração.** `docs/process/` sai da árvore (preservado em tag) e a versão recomeça em 0.1.0 para o primeiro alfa público |
| 25/07 | A leva das sete queixas: 8 sprints entregues. **Os quatro controles jogaram**, numerados 1-2-3-4 |
| 26/07 madrugada | Uma leva de 15 commits e a v0.1.2. **Reprovada de manhã, olhando a tela.** Rollback |
| 26/07 noite | Checkpoint `v0.2.0` com os 31 commits nunca lançados; diagnóstico ao vivo dos dois defeitos do Pragmata |

## O que o estudo achou — e onde foi materializado

Nenhum achado ficou só aqui. Cada um virou sprint com dono:

| Achado | Onde virou trabalho |
|---|---|
| O perfil do jogo nasce catch-all, e a escala trava em 100 — **não havia como vencer pela janela** | [PERFIL-NASCE-CERTO-01](../sprints/2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md) |
| Steam Input tem **dois cadastros** que divergem: 4 joysticks para 1 controle | [DUPLO-REGISTRO-01](../sprints/2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) |
| 145 controles na tela; 10 agem em silêncio; 2 mentem no tooltip | [BOTÃO-QUE-NÃO-MENTE-01](../sprints/2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) |
| Três caminhos para o socket IPC; ADR-001 descrevendo outro backend; tabela de métodos com 10 de 33 | [DOC-VERDADE-01](../sprints/2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md) |
| O gate de emoji **nunca foi construído**; as fontes nunca são instaladas; gates que não rodam | [PROMESSA-NAO-CUMPRIDA-01](../sprints/2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md) |
| A ordem de ataque, com critério declarado | [INDICE-a-fila-do-jogador](../sprints/2026-07-26-INDICE-a-fila-do-jogador.md) |

## Os cinco fatos que mais surpreenderam

Se este estudo tivesse de caber em cinco linhas:

1. **A biblioteca de base monta o relatório Bluetooth errado.** Off-by-one no
   envelope `0x31`; o firmware descarta em silêncio. Era isso o "a cor nunca
   funcionou por Bluetooth". O projeto reescreveu o envelope contra o kernel.
2. **O gamepad virtual é um DualSense de verdade**, registrado em `/dev/uhid`,
   com descritor canônico embutido — e se apresenta como **Edge** de propósito,
   para que a variável que esconde o modelo comum esconda só o físico.
3. **O microfone por rádio é Opus dentro do HID.** O DualSense não fala A2DP.
   Ligar custa 35% dos relatórios de input, porque o áudio não abre canal novo:
   ocupa lugar na mesma fila.
4. **Há mais linhas de teste que de código** (96 mil contra 66 mil), e ainda
   assim a camada onde o produto quebrou em 26/07 é a que **pula no CI**.
5. **O projeto registra por escrito o que recusou copiar.** O `NOTICE` tem uma
   seção do material de terceiros avaliado e negado, com a consequência assumida
   em voz alta: os doze modos prontos do DSX não funcionam aqui.

## O traço que atravessa o repositório inteiro

**A autocrítica é o formato, não a exceção.** Notas de verificação dentro de
ADRs vigentes; banner "SUPERADO" numa pesquisa de maio; a Parte 2 do ADR-018
emendada depois de refutada; dois erros de análise preservados de propósito na
validação dos quatro controles, com o motivo — *"são armadilhas que qualquer um
repete"*.

Isso tem um custo, e o custo apareceu neste estudo: **a documentação envelhece em
pontos que a varredura de 25/07 não alcançou**, e o registro honesto de ontem
convive com a afirmação desatualizada de hoje sem que nada sinalize a diferença.
É por isso que `DOC-VERDADE-01` propõe um gate, e não só uma faxina.

## O que este estudo NÃO cobriu

- **`docs/history/` contra o código.** São documentos declaradamente históricos;
  uma contradição ali pode ser registro correto de decisão superada — o oposto de
  defeito. Precisa de critério antes de varrer.
- **O applet COSMIC em Rust**, além da paridade de modo. 1.745 linhas lidas por
  cima.
- **A validação em hardware.** Tudo aqui é leitura de código, documento e journal.
  Os quatro controles, a noite de jogo e a tela são dela.
