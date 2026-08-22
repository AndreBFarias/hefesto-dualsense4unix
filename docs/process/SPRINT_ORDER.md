# SPRINT_ORDER — o que está aberto e em que ordem

Este é o arquivo único e de caminho fixo (`docs/process/SPRINT_ORDER.md`) que
diz o que está aberto, em que ordem, e o que espera a palavra dela. Ele existiu
até a faxina de 24/07 (`a639e0d`), foi apagado, e ela o pediu de volta em
21/08/2026.

**Censo de 22/08/2026, 228 sprints:** 74 concluídas, 40 abertas, 87 parciais,
27 índices, 0 indeterminadas. As 127 abertas e parciais estão na seção 3.

---

## 1. A FILA DE AGORA — decidida por ela em 21/08

A ordem e o motivo estão no índice do dia, e não se repetem aqui:
[ÍNDICE — a casa mudou de endereço, e a fila mudou de ordem](sprints/2026-08-21-INDICE-a-casa-mudou-de-endereco-e-a-fila-mudou-de-ordem.md).

| Quando | O quê |
|---|---|
| **Agora** | `CONFIG-01` — a aba Configurações nasce com placeholders (`sprints/2026-08-21-ABA-CONFIGURACOES/`) |
| **22/08**, com o hardware na mesa | a bancada de rádio, pelo `GUIA-RADIO-DA-SALA.md` da mesma pasta |
| Depois | `CONFIG-02`, que consome a leitura de rádio |

### Os oito de CÓDIGO de 22/08, em ordem de custo do silêncio

Saíram da seção 4 porque não são frase errada: são código. A ordem é de custo do
silêncio, e a coluna do meio diz esse custo — o que já foi medido em cada um, não
estimativa de esforço.

| # | Buraco e onde | O que o silêncio custa | Cura medida |
|---|---|---|---|
| 1 | **O carimbo de ponte evapora em TODO salvamento pelo rodapé.** `app/draft_config.py` (sem `source_ponte`), consumido em `.../app/actions/footer_actions.py` e `.../app/actions/profiles_actions.py` | O gesto mais banal dela — Salvar pelo rodapé — apaga o que o produto aprendeu sozinho: o jogo cai do painel de pontes confirmadas, e a data e a origem morrem. A escada recomeça do zero no lançamento seguinte. Custo diário, e derruba a decisão dela de 19/08 | Passthrough SOMENTE-LEITURA, no molde de `source_match` e irmãos, sem nenhum escritor. NÃO dar às abas campo editável: a isenção em `tests/unit/test_perfil_salva_tudo_cobertura_das_secoes.py` explica por quê, e é atualizada junto |
| 2 | **As regras udev 82 e 83 nos CINCO formatos sem os alvos do `RUN+=`.** `install.sh` (o `exit 0` dos formatos contra o passo 3e-bis), `scripts/install_udev.sh`, `scripts/install-host-udev.sh`, `assets/82-nintendo-pro-nosniff.rules`, `assets/83-hefesto-bond-snapshot.rules` | Dívida MEDIDA em 07/08 (estudo da cobertura do install, item 9) e nunca fechada. Em flatpak e appimage a 83 aponta para unit inexistente e falha calada a CADA conexão BT — o salva-vidas de bonds nunca grava para quem instalou por ali, e ninguém é avisado | A ferramenta do portão já existe: `_alvos_run_das_regras`, em `tests/unit/test_uninstall_simetrico_ao_install.py` |
| 3 | **A camada ONDA-R2 só no formato native, e a mensagem final não avisa.** `install.sh`, passo 3e-bis contra a mensagem dos formatos; diagnóstico em `scripts/doctor.sh` | Quatro dos cinco formatos instalam sem a camada e sem uma linha dizendo isso; o doctor ainda manda rodar o `install.sh` para quem já rodou. Fere a regra dela de 08/08: toda cura entra no install, sem flag | Içar o 3e-bis para acima da bifurcação, no molde de `install_broker_host` e `install_osk_host`, e chamá-lo dos dois lados; ou instalar a 83 só onde a unit existe |
| 4 | **A aba Sistema marca a allowlist e a caixinha da aba Perfis não relê.** `.../app/actions/daemon_actions.py`, `.../app/actions/profiles_actions.py`, `app/app.py` | Duas abas mostram estados diferentes do MESMO arquivo, e a tooltip manda usar justamente a que mente. Ela desmarca sem querer o que acabou de marcar | Acrescentar o sincronizador à tupla da aba Perfis (cobre também a CLI, que nenhuma outra cura alcança) e, opcional, chamá-lo por despacho dinâmico logo após a marcação. Obriga a atualizar o teste que congela o mapa com `==` |
| 5 | **O interruptor do teclado emulado ganhou um SEGUNDO escritor (PS + R3), e a aba não relê.** `app/app.py` (o comentário e o mapa de refresh por aba), `.../daemon/subsystems/hotkey.py`, `.../app/actions/emulation_actions.py` | A aba desenha um interruptor que o gesto já virou. O mouse tem o mesmo defeito quando o perfil traz seção de mouse. Abaixo do 4 só porque o gesto ainda não foi visto em hardware | Substituir a frase larga do comentário e trocar o grep por `set_keyboard_emulation(` — o método IPC não pega a chamada em processo. Mexe em dois testes que congelam o desenho atual |
| 6 | **O gate do mic é por SEÇÃO e deveria ser por CAMPO.** `app/draft_config.py`, consumido em `.../daemon/ipc_draft_applier.py` | Mexer no volume marca a seção inteira como tocada, e o Aplicar leva junto um flag de botão de mic que ninguém escolheu. É o menor dos oito por medição: a ativação de perfil ignora o campo, e o valor volta sozinho no restart | O gate passa a ser por campo, como o alto-falante já faz; ou nasce a superfície que falta |
| 7 | **O portão A-CASA-SABE mede alcance PLANO.** `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`, o laço de 1166-1179 e `_TERRITORIOS_DE_PRODUCAO` em 150 | Instrumento, não produto — por isso não é o 1. Mas é o portão da classe de defeito mais cara desta casa: corrente fechada em si mesma passa, e colisão de nome entre módulos perdoa símbolo sem relação nenhuma | NÃO trocar por "chamador fora do próprio arquivo": já medido em 12/08, acusa 846 símbolos. A régua é alcance a partir dos pontos de entrada declarados, pelo grafo de import, com nome resolvido ao módulo. E estreitar o território ao que algum instalador COPIA para fora do checkout |
| 8 | **A aba Configurações afirma na tela três coisas no presente sem uma linha de código.** `.../app/actions/config_actions.py` e `gui/main.glade` | Mentira na tela, na aba que nasceu vazia ontem. O silêncio só custa até a leva que der conteúdo à seção — a dica e a seção andam juntas | A dica viaja com a seção. Corrigir junto o passo 4 do `COMO-EXECUTAR.md` da sprint, senão volta. Critério do portão: enquanto a seção não tiver widget, ela não tem dica |

---

## 2. Como ler a seção 3

As sete faixas abaixo são **ordenação de custo do silêncio, não medição** — o
censo mediu o estado de cada sprint, não a prioridade entre elas. A faixa 1 é a
régua do alvo dela (cada jogo local jogável no cabo e no rádio); a última é a
que só custa tempo da próxima pessoa.

`DELA` = a sprint não fecha sem a mão, o olho ou a palavra dela.

---

## 3. O QUE ESTÁ ABERTO — 127 sprints

### Faixa 1 — o jogo não anda, ou anda e derruba jogador (38)

| Sprint | O que falta | DELA |
|---|---|---|
| [COOP-QUE-NAO-DESMONTA-01](sprints/2026-08-03-COOP-QUE-NAO-DESMONTA-01-o-jogador-2-que-dura-dois-segundos.md) | ABERTA. E1 a E4: a troca de primário destrói o jogador existente. Causa-raiz provada em três elos, com journal | |
| [PARTIDA-PICOTADA-01](sprints/2026-08-08-PARTIDA-PICOTADA-01-a-caixinha-que-tirava-o-jogador-2-a-cada-piscada.md) | Itens 2, 4, 5 e 6. O portão anti-recriação cobre a camada errada, e a suspensão passa por baixo via `stop_gamepad_emulation` | DELA |
| [JOGADOR-3-FANTASMA-01](sprints/2026-08-08-JOGADOR-3-FANTASMA-01-a-cura-certa-no-momento-errado.md) | Os três primeiros itens da seção 7. O `xfail` é a marca honesta de que o ciclo de vida da dispensa não tem código | DELA |
| [BORDA-DE-QUEDA-01](sprints/2026-08-03-BORDA-DE-QUEDA-01-o-que-fica-para-tras-quando-um-controle-cai.md) | ABERTA. E1 a E5. Sintoma reproduzido pela fala dela: quatro travamentos em 28 segundos | |
| [QUATRO-NA-MESA-01](sprints/2026-08-03-QUATRO-NA-MESA-01-o-que-so-quebra-quando-sao-quatro.md) | ABERTA. Os quatro defeitos. O aceite não pode ser escrito contra o sysfs (nota de 04/08) | DELA |
| [QUATRO-NO-RADIO-01](sprints/2026-08-03-QUATRO-NO-RADIO-01-o-checklist-dos-quatro-controles-por-bluetooth.md) | ABERTA. O aceite inteiro, com jogo aberto. Depende de B1, B2 e B4 caírem antes | DELA |
| [JOGAVEL-EM-TODOS-01](sprints/2026-08-16-JOGAVEL-EM-TODOS-01-o-alvo-dela-e-cada-jogo-nos-dois-transportes.md) | ABERTA. Os quatro ensaios da seção 2, o chamador da allowlist, e o `hidden_count` que conta em vez de nomear | DELA |
| [TRES-PORTOES-01](sprints/2026-08-19-TRES-PORTOES-01-nao-anda-nem-o-microfone.md) | Seção 6 inteira: o `origem=`, a recriação do vpad em slot único, os 26 bytes que o vpad nunca escreve, a cadeia do microfone | DELA |
| [DUAS-CONTABILIDADES-01](sprints/2026-08-07-DUAS-CONTABILIDADES-01-a-lampada-conta-a-mesa-inteira-e-o-coop-so-metade.md) | ABERTA. O protocolo do cabo no meio da partida, e o cruzamento no jogador 1 — que é pior que colisão | DELA |
| [CONTAGEM-E-COOP-01](sprints/2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md) | Duas peças do aceite da E3: a frase do Modo jogo durante a exceção, e o preço do gesto manual no toast | DELA |
| [POSSE-POR-CONTROLE-01](sprints/2026-08-03-POSSE-POR-CONTROLE-01-a-trava-de-um-controle-congela-os-quatro.md) | E1 inteira (trava indexada por MAC), o fallback broadcast do rumble em E3, e as quatro bancadas de E4 | DELA |
| [A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01](sprints/2026-08-16-A-MASCARA-QUE-O-PRODUTO-ESCOLHE-01-o-jogo-nao-enxerga-e-a-culpa-nao-e-da-pessoa.md) | Os dois ensaios que a seção 8 exige antes de qualquer linha não têm bruto | DELA |
| [MASCARA-01](sprints/2026-07-25-MASCARA-01-como-este-controle-aparece-nos-jogos.md) | E2, E4 e metade da E3. Pré-requisito da E3/E4 da LUGAR-À-MESA-01, por decisão dela de 07/08 | |
| [MASCARA-POR-JOGADOR-01](sprints/2026-08-15-MASCARA-POR-JOGADOR-01-a-decisao-de-14-08-esbarra-na-de-10-08.md) | O último degrau da 7.2: `make_virtual_pad` resolver a máscara ANTES de escolher o backend, e o lado da escrita no IPC | |
| [LUGAR-A-MESA-01](sprints/2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md) | E3 e E4, presas atrás da MASCARA-01. O grab mais FF em aparelho não-Sony continua sem prova | DELA |
| [JOGO-01](sprints/2026-07-25-JOGO-01-o-jogo-enxerga-quatro-controles.md) | A E2: a frase que distingue os dois estados do opt-in na aba Emulação | |
| [O-WRAPPER-QUE-SUMIU-01](sprints/2026-08-16-O-WRAPPER-QUE-SUMIU-01-uma-variavel-nova-apaga-a-ponte-em-silencio.md) | E2 (o guard de `LaunchOptions` por merge, no instalador e simétrico no uninstall) e E3 (a fração na aba Sistema) | |
| [WRAPPER-EM-TODOS-01](sprints/2026-08-03-WRAPPER-EM-TODOS-01-a-invariante-duplicado-melhor-que-zero-com-quatro.md) | E3 e o aceite de campo: a invariante só se prova com quatro controles numa partida de verdade | DELA |
| [STEAM-INPUT-01](sprints/2026-07-26-STEAM-INPUT-01-ela-nunca-mais-precisa-decidir.md) | E2 e E4 a E8, entre elas a lista por nome de jogo em vez de contagem | DELA |
| [DUPLO-REGISTRO-01](sprints/2026-07-26-DUPLO-REGISTRO-01-o-steam-input-tem-dois-cadastros.md) | ABERTA. A reconciliação dos dois registros, o grab pendente deixar de ser silencioso, e a leitura do `localconfig.vdf` em runtime | |
| [STEAM-QUE-DECIDE-01](sprints/2026-08-05-STEAM-QUE-DECIDE-01-ela-nao-tem-como-saber-quando-ligar.md) | E1 (o experimento M-04), E5, a metade honesta da E3, e o M-05 | DELA |
| [JOGOS-QUE-ELA-TEM-01](sprints/2026-08-06-JOGOS-QUE-ELA-TEM-01-escolher-da-biblioteca-em-vez-de-adivinhar-o-numero.md) | A E4 — perfil por jogo instalado. Nenhum símbolo em `src/` o faz nascer | DELA |
| [CONTROLE-SONY-MEDIDO-01](sprints/2026-08-06-CONTROLE-SONY-MEDIDO-01-o-experimento-que-decide-metade-da-doutrina.md) | A versão do cliente Steam não foi anotada — e é a variável que invalidou o resultado antigo | DELA |
| [AUDIO-QUE-TRANCA-01](sprints/2026-08-03-AUDIO-QUE-TRANCA-01-um-toque-no-volume-congela-a-troca-de-perfil.md) | ABERTA. As cinco entregas. A E1 é uma linha e é o que trava o produto hoje | DELA |
| [PERFIL-JOGO-01](sprints/2026-07-26-PERFIL-JOGO-01-as-configs-somem-ao-abrir-o-jogo.md) | A entrega 1 (rodar o experimento com ela e nomear o sintoma) nunca rodou, e sem ela as 2 a 6 não se sustentam | DELA |
| [PERFIL-NASCE-CERTO-01](sprints/2026-07-26-PERFIL-NASCE-CERTO-01-o-perfil-do-jogo-que-nunca-vence.md) | E3 e o resto da E4: o detector de sanidade existe e ninguém o dispara | |
| [AUTO-01](sprints/2026-07-25-AUTO-01-um-clique-em-vez-de-dez.md) | Dois catch-all semeados ainda em `match: any`, o `--no-dkms` único, e o critério de aceite nunca medido | DELA |
| [CONECTA-E-DESLIGA-01](sprints/2026-08-07-CONECTA-E-DESLIGA-01-a-regressao-que-ela-relatou-e-a-suspeita-que-recai-sobre-nos.md) | ABERTA. A cura, que ela mandou esperar. E a pergunta do item 2 vem antes dela | DELA |
| [OITO-DEFEITOS-01](sprints/2026-08-08-OITO-DEFEITOS-01-a-fila-que-a-verificacao-adversarial-derrubou-inteira.md) | 2.5 (o rumble) sem causa provada; 2.3, 2.6 e 2.8 não reconferidos e sem marca na árvore | DELA |
| [ORDEM-DE-CHEGADA-01](sprints/2026-08-15-ORDEM-DE-CHEGADA-01-a-fila-que-ela-pediu-nao-e-a-fila-que-o-produto-guarda.md) | E3 (o gesto `identity.renumber` alcançável de onde ela está), e o item C da frase dela segue não medido | |
| [ESCOLHA-DELA-VENCE-01](sprints/2026-08-01-ESCOLHA-DELA-VENCE-01-a-mascara-do-perfil-e-o-tooltip-do-xbox.md) | E2 (a máscara sobrevive ao reboot), E3 (a recusa com jogo aberto deixa de reportar sucesso), E5 | DELA |
| [EMULACAO-NO-JOGO-01](sprints/2026-07-29-EMULACAO-NO-JOGO-01-o-r1-troca-de-app-em-vez-de-jogar.md) | E5, duas peças do aceite da E3 não conferidas, e o cabeçalho desatualizado | DELA |
| [PS-TOQUE-CURTO-01](sprints/2026-08-03-PS-TOQUE-CURTO-01-o-gesto-de-religar-o-controle-abre-a-steam.md) | ABERTA. E1 a E4, incluindo declarar o `wmctrl` no install ou a dependência morre | |
| [IDENT-01](sprints/2026-07-25-IDENT-01-um-controle-duas-identidades.md) | ABERTA. As quatro entregas. O documento recusa o palpite automático de propósito | DELA |
| [IDENTIDADE-DUPLA-01](sprints/2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md) | ABERTA. E1 é o MAC de cada modo, 2 minutos da mão dela. Sem ele, E2 a E4 seriam adivinhação por OUI | DELA |
| [REGRA-NAO-REGISTRO-01](sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md) | ABERTA. Fundir os dois rostos do 8BitDo. Ler antes a nota de `0df6825`: quatro pontos declarados errados, um deles destrutivo | |
| [NOME-HONESTO-01](sprints/2026-08-03-NOME-HONESTO-01-a-tela-chama-de-sony-o-que-o-kernel-ja-sabe-que-nao-e.md) | ABERTA. E1 a E5. Nenhuma linha entregue | DELA |
| [CHECKLIST de validação em hardware](sprints/2026-07-25-CHECKLIST-validacao-em-hardware.md) | ABERTA. As 31 caixas. Por construção, só ela pode fechá-las | DELA |

### Faixa 2 — a casa sabe e o produto não faz (14)

| Sprint | O que falta | DELA |
|---|---|---|
| [AUTOMATISMO-MORTO-01](sprints/2026-07-30-AUTOMATISMO-MORTO-01-o-perfil-do-jogo-nunca-entra.md) | ABERTA. Tudo, a começar pela E0 (a janela dizer POR QUE o perfil não trocou). Duas sprints escreveram a cura, nenhuma a ligou | |
| [JANELA-CEGA-01](sprints/2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md) | A fiação do motivo do autoswitch até o IPC — escrita em duas sprints, ausente do daemon | |
| [SINAL-DE-JOGO-01](sprints/2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md) | E1 (o experimento com o jogo vivo, sem bloco de journal no documento) e E2. E4 e E5 não reconferidas | DELA |
| [MODO-01](sprints/2026-07-25-MODO-01-o-modo-jogo-liga-sozinho.md) | O B4: o gate de foco cega a detecção. A AUTOMATISMO-MORTO-01 mediu 135 episódios DEPOIS desta sprint | DELA |
| [ENTREGA-QUE-NAO-LIGOU-01](sprints/2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md) | E3, E4 e E5. Sem prova de nenhuma das três; o defeito 3 não foi conferido | |
| [A-NOITE-DOS-QUATRO-INVENTARIOS-01](sprints/2026-08-09-A-NOITE-DOS-QUATRO-INVENTARIOS-01-o-que-a-casa-sabe-e-o-que-o-produto-faz.md) | F-6(a) confirmado aberto pelo próprio código; F-2 e F-11 abertos e sem marca. F-3, F-7, F-9 e F-10 não reconferidos | DELA |
| [AGORA-E-DEPOIS-01](sprints/2026-08-08-AGORA-E-DEPOIS-01-o-plano-executavel-da-separacao-dos-dois-tempos.md) | O passo 6. As três ausências da seção 10 reproduzidas. Cuidado com o falso positivo `MascaraAdiada`, que mora em memória e morre no restart | DELA |
| [BONDS-QUE-SOBREVIVEM-01](sprints/2026-08-04-BONDS-QUE-SOBREVIVEM-01-o-salva-vidas-que-ninguem-aciona.md) | E5 inteira, E3.1, e o cabeçalho — que diz aberta sobre uma sprint de coração de pé desde 15/08 | DELA |
| [MESA-CHEIA-05](sprints/2026-08-13-MESA-CHEIA-05-o-rumble-por-mac-a-rota-que-ninguem-ligou.md) | A E1: `rumble_active` virar mapa por uniq, `rumble.set` aceitar endereço, e o `state_full` expor os quatro estados | |
| [SOM-DE-CADA-JOGADOR-01](sprints/2026-08-15-SOM-DE-CADA-JOGADOR-01-o-botao-que-nunca-funcionou-com-a-mesa-cheia.md) | E2 — a peça existe desde 20/08 e nunca foi ligada no botão. E3 e as mordidas 1 a 4. O ensaio às cegas do canal 3 não tem bruto | DELA |
| [MIC-BT-DONO-01](sprints/2026-08-03-MIC-BT-DONO-01-a-posse-do-mudo-ganha-dono-e-ciclo-de-vida.md) | ABERTA. Dar ao mudo do mic o tratamento que o LED recebeu. O alvo honesto é 55-75% de mudo, não 0% | |
| [ESTADO-QUE-MENTE-01](sprints/2026-08-03-ESTADO-QUE-MENTE-01-o-daemon-afirma-controle-conectado-com-a-mesa-vazia.md) | ABERTA. Derivar o topo do `state_full` da lista de controles. O painel da verdade mostra bateria de controle que não existe | |
| [PERFIL-SEM-RASTRO-01](sprints/2026-08-05-PERFIL-SEM-RASTRO-01-o-perfil-mudava-e-nada-registrava-quem-mudou.md) | A dívida de descoberta (três parágrafos na doc da CLI e uma linha no README), e o `_reject_traversal` nos caminhos de escrita | |
| [PROMESSA-NAO-CUMPRIDA-01](sprints/2026-07-26-PROMESSA-NAO-CUMPRIDA-01-o-que-o-projeto-anuncia-e-nao-entrega.md) | C3 continua verdadeiro e o código o confessa. A2, A3, C2, D, E e F não conferidos item a item | |

### Faixa 3 — o install e o pacote entregam cura morta (10)

| Sprint | O que falta | DELA |
|---|---|---|
| [INSTALL-QUE-NAO-CARREGA-01](sprints/2026-08-07-INSTALL-QUE-NAO-CARREGA-01-as-descobertas-que-nunca-viraram-codigo.md) | L3 aberta e medida hoje: cinco arquivos de `assets/` citam documentos que não existem, e o portão de referências só varre `docs/`. L5 sem resposta | DELA |
| [SIMETRIA-INSTALL-02](sprints/2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | E3, E4, E6 (decisão dela) e E7. Não reconferido se a E2 fechou ou só foi anotada | DELA |
| [CURA-QUE-FERE-01](sprints/2026-08-04-CURA-QUE-FERE-01-toda-cura-de-systemd-tem-de-provar-o-ciclo-inteiro.md) | E1 a E4: teste de ciclo por unit instalada, o portão da tabela de combinações, unit em failed virar FALHA no doctor, e a tela com o agente morto | |
| [BT-AGENT-TRAVA-O-RESTART-01](sprints/2026-08-04-BT-AGENT-TRAVA-O-RESTART-01-noventa-segundos-de-bluetooth-fora-do-ar.md) | E4 (`flock -n` no `ExecStopPost`) e E5 (`TimeoutStopSec` explícito). E7 é da CURA-QUE-FERE-01 e também segue aberta | |
| [BT-SNAPSHOT-SANDBOX-01](sprints/2026-08-04-BT-SNAPSHOT-SANDBOX-01-o-salva-vidas-que-falhava-so-no-naufragio.md) | O teste que a sprint pediu por escrito (o `ReadWritePaths` cobrir tudo que os `ExecStopPost` escrevem) e a varredura irmã | |
| [DROPIN-AMBIGUO-01](sprints/2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md) | ABERTA. E1 a E5. A E4 é decisão a declarar em voz alta | |
| [RADIO-ABERTO-01](sprints/2026-08-04-RADIO-ABERTO-01-o-que-instalamos-por-padrao-anula-a-autenticacao.md) | E2 (agente próprio, que é o que fecha o cenário) e E3. E4 a E6 seguem N/A | |
| [PUBLICACAO-FIEL-01](sprints/2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | E2 (decisão dela) e E3, que não consegui localizar para reconferir. O cabeçalho precisa deixar de dizer que não houve código | DELA |
| [IDENTIDADE-01](sprints/2026-08-21-IDENTIDADE-01-o-projeto-ainda-se-chama-pelo-nome-dele.md) | Fase 2 (renomear o id, os 15 testes, o CI) e Fase 3 (a migração). As duas na mesma leva: id novo sem migração deixa quem já usava sem os perfis | |
| [ARVORE-DIVERGENTE-01](sprints/2026-07-30-ARVORE-DIVERGENTE-01-o-que-esta-na-main-e-nao-roda.md) | Portar E1, E4 (com o co-op desligado, todo controle conectado ainda vira jogador 1) e E5. A tag citada resolve para outro commit | DELA |

### Faixa 4 — a janela mente, corta, ou não deixa ela ver (25)

| Sprint | O que falta | DELA |
|---|---|---|
| [LIGHTBAR-JOGADOR-01](sprints/2026-07-27-LIGHTBAR-JOGADOR-01-a-cor-e-consequencia-do-jogador.md) | ABERTA. E0 a E4. Queixa direta dela olhando a tela, prioridade ALTA, 25 dias sem uma linha | DELA |
| [MESA-CHEIA-01](sprints/2026-08-13-MESA-CHEIA-01-a-fita-do-alvo-ganha-a-cor-de-cada-um.md) | ABERTA. A entrega inteira: a linguagem de cor do card da Status nos chips da fita, nas dez abas | DELA |
| [MESA-CHEIA-02](sprints/2026-08-13-MESA-CHEIA-02-a-marca-de-quem-escolheu-na-aba-gatilhos.md) | ABERTA. A entrega inteira. É ela que dá o formato da marca de que a 04 e a 06 dependem | DELA |
| [MESA-CHEIA-03](sprints/2026-08-13-MESA-CHEIA-03-a-mesma-marca-na-aba-lightbar.md) | ABERTA. Quatro prévias numeradas, a marca nos seis presets, e a tela saber dizer o terceiro estado | DELA |
| [MESA-CHEIA-04](sprints/2026-08-13-MESA-CHEIA-04-a-marca-vira-gesto.md) | ABERTA. A entrega inteira. Depende da 02 | DELA |
| [MESA-CHEIA-06](sprints/2026-08-13-MESA-CHEIA-06-o-portao-contra-a-marca-que-mente.md) | ABERTA. O portão inteiro. Depende da 02, que daria o primeiro caso real | |
| [MESA-CHEIA-07](sprints/2026-08-13-MESA-CHEIA-07-a-decima-aba-que-ninguem-mediu.md) | A E2 — o painel da aba No jogo não tem uma única linha de cor | DELA |
| [MESA-CHEIA-10](sprints/2026-08-13-MESA-CHEIA-10-a-fita-que-nao-sabe-em-que-aba-esta.md) | ABERTA. A fita se requalificar nas seis abas em que o alvo não é honrado | DELA |
| [ONDE-A-COR-MORA-01](sprints/2026-08-15-ONDE-A-COR-MORA-01-a-borda-diz-quem-e-e-o-anel-diz-o-que-esta-escolhido.md) | ABERTA. As três perguntas da seção 7 são dela; depois, ~190 linhas e as quatro mordidas, incluindo o guarda do alto contraste | DELA |
| [NAVEGA-PELO-CONTROLE-01](sprints/2026-08-15-NAVEGA-PELO-CONTROLE-01-quem-tem-o-foco-decide-o-que-o-R1-faz.md) | ABERTA. Seções 4 a 8 inteiras, a pergunta única da seção 9, e a prova de tela | DELA |
| [NAVEGAR-ESTA-JANELA-01](sprints/2026-08-15-NAVEGAR-ESTA-JANELA-01-a-decisao-ja-esta-tomada-e-o-dado-ja-esta-no-fio.md) | ABERTA. A entrega inteira, as duas perguntas da seção 8, e a prova de tela | DELA |
| [FIACAO-QUE-FALTA-01](sprints/2026-08-05-FIACAO-QUE-FALTA-01-o-verificador-que-ela-nao-tem-como-ver.md) | E1 (o verificador na janela), E4.1, E4.3, E5, E6 (texto de interface, palavra dela) e E3b | DELA |
| [JANELA-FIEL-01](sprints/2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | E5 (TUI) e E6 (bandeja), mais o aceite dela: a janela não trocar sozinha o que está na tela, e o Restaurar Padrão achar o arquivo | DELA |
| [JANELA-CORTADA-01](sprints/2026-08-17-JANELA-CORTADA-01-o-rodape-que-o-gtk-diz-que-cabe.md) | O item 2 — o selo Saída muda dentro do bloco, com bancada fiel à largura real do card | DELA |
| [JANELA-QUE-RESPIRA-01](sprints/2026-08-01-JANELA-QUE-RESPIRA-01-os-consertos-de-largura-que-a-casa-ja-tinha-decidido.md) | O aceite dela na janela real. Não há foto de aceite nem palavra registrada | DELA |
| [LARGURA-01](sprints/2026-07-29-LARGURA-01-a-mesma-largura-em-todas-as-abas.md) | E5 a E8. Só a E8 está provada aberta por símbolo. O `_WRAP_COLUNAS` fixo tranca a GATILHO-PALAVRA-01 | DELA |
| [LEGIBILIDADE-01](sprints/2026-07-25-LEGIBILIDADE-01-texto-legivel-alvo-clicavel.md) | O lugar dos analógicos e a largura a 1180x830, mais a decisão sobre as 11 classes órfãs do CSS | DELA |
| [CARD-OCUPA-01](sprints/2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md) | E4: a aba Estado maximizada, e ela dizer se os quatro elementos ocuparam os vãos laterais | DELA |
| [RADAR-01](sprints/2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md) | E1, E2, E3 e o D1. O applet que ela usa TODO DIA continua sem o olho dela por cima | DELA |
| [BOTAO-QUE-NAO-MENTE-01](sprints/2026-07-26-BOTAO-QUE-NAO-MENTE-01-clico-e-nao-acontece-nada.md) | E5 (a regra de informar quantos controles cada sprint de interface adiciona ou remove) e E6. E1 e E3 não reconferidas | DELA |
| [PERFIL-SALVA-TUDO-01](sprints/2026-07-29-PERFIL-SALVA-TUDO-01-salvei-todas-as-abas-e-so-parte-ficou.md) | E5 e E6, nenhuma provável na árvore. E o cabeçalho, que ainda diz que E1 e E2 estão abertas — as duas estão em código com teste que morde | DELA |
| [PLAYER-LED-01](sprints/2026-07-25-PLAYER-LED-01-o-numero-do-jogo-chega-ao-controle.md) | A entrega 5 — o diagnóstico honesto por controle. A entrega 4 tem sucessora própria, sinal de que o buraco não fechou aqui | |
| [FOCO-ERRANTE-01](sprints/2026-08-18-FOCO-ERRANTE-01-o-x-aponta-para-a-steam-e-leva-o-perfil-junto.md) | Passos 1, 2, 7, 8 e a cura de zero linhas (decisão dela). A ONDA 2 (backend COSMIC) intocada | DELA |
| [PROVA-DE-TELA-01](sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md) | A folha respondida dentro do documento — o passo 4 do próprio procedimento. Hoje as fotos entram e a folha não | DELA |
| [GATILHO-PALAVRA-01](sprints/2026-07-29-GATILHO-PALAVRA-01-os-dezenove-modos-em-portugues.md) | A escolha das dezenove palavras, que é dela por construção. Amarrada à decisão irmã da CR-SEQUENCIA-01/E5 | DELA |

### Faixa 5 — o aparelho: luz, som, gatilho, rádio (28)

A maioria destas destranca com a bancada de 22/08 e o controle na mão dela.

| Sprint | O que falta | DELA |
|---|---|---|
| [PROVA-NO-PLASTICO-01](sprints/2026-08-19-PROVA-NO-PLASTICO-01-o-roteiro-de-quarenta-minutos-com-o-controle-na-mao.md) | ABERTA. Bloco A, B2 a B6, e o bloco C inteiro: 20 células que só o olho dela preenche | DELA |
| [O QUE PRECISA DE VOCÊ (19/08)](sprints/2026-08-19-O-QUE-PRECISA-DE-VOCE.md) | O roteiro de 40 min sem o bloco B1, abrir o Grim Fandango uma vez, olhar as cinco cores, e o chamador automático da allowlist | DELA |
| [A-PONTE-UNIVERSAL-01](sprints/2026-08-15-A-PONTE-UNIVERSAL-01-o-cabo-como-pedra-de-roseta.md) | P-1 (o oráculo de transporte pelo `HID_ID`), P-3, E-2, e a Onda 4 inteira | DELA |
| [ESCADA-QUE-RESPONDE-01](sprints/2026-08-15-ESCADA-QUE-RESPONDE-01-do-degrau-que-obedece-ao-conteudo-do-payload.md) | E-2 a E-6: todos escrevem no aparelho e dependem da D-31 e da D-32. E as linhas no caderno com a coluna do degrau preenchida | DELA |
| [A-CADEIA-DE-BLOCOS-01](sprints/2026-08-16-A-CADEIA-DE-BLOCOS-01-o-ensaio-de-quatro-minutos-que-decide-o-som-por-radio.md) | ABERTA. O acréscimo no instrumento, os 6 minutos de olho dela no E-7, e as quatro perguntas da seção 10 | DELA |
| [O-ALTO-FALANTE-POR-RADIO-01](sprints/2026-08-15-O-ALTO-FALANTE-POR-RADIO-01-a-casa-ja-tinha-o-mapa.md) | ABERTA. E1 (montar o `0x39` com o bloco duplo), E2 (o ensaio com a orelha dela) e E3 | DELA |
| [TRES-MODOS-DO-SOM-01](sprints/2026-08-16-TRES-MODOS-DO-SOM-01-o-que-sai-onde-e-quem-escolhe.md) | ABERTA. As cinco decisões P-1 a P-5 e as cinco ondas. Não conferido se a ONDA 1.2 caducou por outra via | DELA |
| [E5 — O TERRENO](sprints/2026-08-16-E5-O-TERRENO-o-que-o-E1-mudou-no-caminho-do-som.md) | Duas linhas no caderno de ensaios e o bruto da corrida. As três perguntas da seção 10 são dela | DELA |
| [SOM-ROTA-01](sprints/2026-08-01-SOM-ROTA-01-a-rota-o-preamp-e-o-canal-do-controle.md) | E2, metade da E3, E4 e E5 — dependem do hardware e da mão dela | DELA |
| [PARIDADE-SONY-01](sprints/2026-08-01-PARIDADE-SONY-01-o-que-o-jogo-manda-ao-alto-falante.md) | A E2 em diante só destranca com medição de jogo real mostrando valores diferentes dos que o sistema escreve | DELA |
| [CONTROLE-INTEIRO-NO-RADIO-01](sprints/2026-08-07-CONTROLE-INTEIRO-NO-RADIO-01-o-mic-e-o-fone-que-nao-atravessam.md) | A metade da SAÍDA (P5 e P6): não há sink virtual nenhum. E o documento precisa de nota datada dizendo que P0 a P3 caíram | |
| [SEM-MICROFONE-NENHUM-01](sprints/2026-08-06-SEM-MICROFONE-NENHUM-01-o-alto-falante-vira-a-entrada-padrao.md) | ABERTA. A política, e a medição que ela exige: o que o WirePlumber faz sem nenhuma fonte com porta usável. É privacidade | |
| [MIC-BT-01](sprints/2026-07-25-MIC-BT-01-o-medidor-do-microfone-por-bluetooth.md) | Caixa 2 (só reabre com a posse do `/dev/hidraw` arbitrada), e as caixas 3 e 4 não encontradas na árvore | |
| [UNIDADE-COR-01](sprints/2026-08-15-UNIDADE-COR-01-o-controle-sabe-de-que-cor-ele-e.md) | A cor do plástico chegar ao produto. E a metade por rádio da D-15 continua sem caminho | DELA |
| [LIGHTBAR-BT-CULPADO-01](sprints/2026-08-03-LIGHTBAR-BT-CULPADO-01-o-report-que-curava-e-o-que-trava.md) | A E3 e o aceite dela. É a regressão que ela descreve como sempre arrumamos mas sempre volta | DELA |
| [SEGUNDO-ESCRITOR-01](sprints/2026-08-08-SEGUNDO-ESCRITOR-01-o-driver-do-kernel-tambem-escreve-a-barra.md) | ABERTA. A medição de contraste dela. Nada virou código, e nada aponta para ela | DELA |
| [A-LUZ-QUE-CUROU-01](sprints/2026-08-07-A-LUZ-QUE-CUROU-01-calar-parou-o-bombardeio-e-voltar-tem-preco.md) | O protocolo da seção 6 nunca rodou, e a pergunta da seção 7 não aparece respondida no painel de decisões dela | DELA |
| [CANETA-NA-MAO-01](sprints/2026-08-12-CANETA-NA-MAO-01-o-suspeito-que-ninguem-olhou-em-dezesseis-dias.md) | Seção 7, itens 1 a 5 e 7: a volta do ensaio da lightbar, o bit de autorização do gatilho, sete dos oito modos, e a PODA | DELA |
| [O-LACO-DE-ESCRITA-01](sprints/2026-08-15-O-LACO-DE-ESCRITA-01-o-suspeito-que-sobrou.md) | A D-38 (autorização dela) e o E-9. O negativo aposentaria uma justificativa que hoje cobra até 32 ms de latência | DELA |
| [BT-SURDO-01](sprints/2026-08-03-BT-SURDO-01-o-controle-parado-no-radio-nao-recebe-ordem.md) | E2 (o `init()` que deixa thread fantasma), E3 (o ioctl de 5 s segurando o lock central) e E4 | |
| [BT-FURO-FINO-01](sprints/2026-08-03-BT-FURO-FINO-01-os-sete-caminhos-que-so-degradam-no-radio.md) | Os defeitos 2 a 7, sem prova de cura e sem prova de que sigam abertos. O 2 é o outro marcado ALTA | |
| [BT-E-VPAD-01](sprints/2026-08-01-BT-E-VPAD-01-o-que-so-existe-no-cabo-e-os-seis-furos.md) | Furo 5 (a taxa declarada do Edge), não medido e sem nada na árvore que o meça. O furo 4 tem decisão registrada de não fazer | |
| [RADIO-BOMBARDEADO-01](sprints/2026-08-04-RADIO-BOMBARDEADO-01-quarenta-mil-frames-corrompidos-em-meia-hora.md) | ABERTA. O bloco F inteiro e o A/B de dez minutos. ATENÇÃO: a fixture de 20/08 cortou o amplificador citado, e isso muda a linha de base | |
| [BUSCA-QUE-ESTOURA-01](sprints/2026-08-07-BUSCA-QUE-ESTOURA-01-o-sdp-que-nao-responde-a-tempo.md) | ABERTA. A escolha entre os cinco desenhos é dela. Houve movimento lateral em `7c2fb92`, que não é nenhum dos cinco | DELA |
| [CR-03](sprints/2026-07-25-CR-03-bancada-de-medicao.md) | ABERTA. A sprint inteira. Bloqueia a CR-04, que bloqueia a CR-06 | |
| [CR-04](sprints/2026-07-25-CR-04-os-efeitos-da-casa.md) | ABERTA. Todos os efeitos medidos na bancada. Não começa antes da CR-03 | |
| [CR-06](sprints/2026-07-25-CR-06-devolver-ao-ecossistema.md) | ABERTA. A publicação inteira. Não começa antes de CR-03 e CR-04 | |
| [CR-SEQUENCIA-01](sprints/2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md) | E3 (a bancada, com posse explícita do hidraw), E4 (a parte dela), E6 e a decisão E5. O cabeçalho ABERTA é enganoso: metade do trilho já fechou | DELA |

### Faixa 6 — documentação, portões e instrumento (12)

| Sprint | O que falta | DELA |
|---|---|---|
| [MAPA-QUE-VIRA-PORTAO-02](sprints/2026-08-11-MAPA-QUE-VIRA-PORTAO-02-o-que-entrou-e-o-que-continua-sendo-dela.md) | Itens 2 a 5. O 4 caducou pela metade: as três colunas cobrem menos de um quinto das linhas. O item 3 não reconferido | DELA |
| [DOC-QUE-NAO-MENTE-03](sprints/2026-08-03-DOC-QUE-NAO-MENTE-03-a-foto-vazia-a-env-negada-e-a-tag-velha.md) | E2 a E6. A doc de métricas ainda afirma zero ocorrências onde há 4, e os IDs órfãos seguem sem documento nem lápide | |
| [DOC-QUE-NAO-MENTE-04](sprints/2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md) | Os portões A, C, D e E. Sem eles, as duas mentiras da sprint seguem sem quem as pegue | |
| [DOC-VERDADE-02](sprints/2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md) | E7 é a única provada aberta por texto vivo. E1 a E4 e E6 não reconferidas | |
| [DOC-VERDADE-01](sprints/2026-07-26-DOC-VERDADE-01-a-documentacao-descreve-outro-programa.md) | e1 (a varredura nos quatro documentos de protocolo e em seis ADRs) e e6 (a colisão de nomes com os modos HID) | |
| [ROTULOS-DE-SPRINT-01](sprints/2026-08-09-ROTULOS-DE-SPRINT-01-entregue-no-codigo-nao-e-validado-por-ela.md) | A regra 4 do portão continua PROPOSTA. O portão de referências tem só as regras 1, 2 e 3 | DELA |
| [A-LINHA-QUE-DISPENSA-01](sprints/2026-08-15-A-LINHA-QUE-DISPENSA-01-o-defeito-mora-onde-a-autora-escreveu-que-nao-precisava-olhar.md) | E1, E2 e E3 — a E3 é a que teria pego quatro das seis. Cinquenta minutos ao todo | DELA |
| [TRES-REFUTADAS-01](sprints/2026-08-15-TRES-REFUTADAS-01-o-que-a-terceira-rodada-de-ceticismo-deixou-de-pe.md) | 1.5 (E1 e E3), 1.4 (E1 a E4) e o teste permanente das quatro conjunções nuas de 1.11 | DELA |
| [TESTE-HONESTO-01](sprints/2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md) | E2 (a fixture de captura de Bluetooth) e os 68 `importorskip` restantes | |
| [SUITE-QUE-SUJA-O-JORNAL-01](sprints/2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md) | E4 (o portão) — exatamente o que a sprint previu. E o cabeçalho, que diz aberta sobre uma sprint majoritariamente paga | |
| [BERCO-DE-TMP-01](sprints/2026-08-07-BERCO-DE-TMP-01-a-suite-nao-suja-a-config-dela-suja-o-tmp.md) | Quatro dos sete declarados. Rodar a faxina no `/tmp` dela é palavra dela | DELA |
| [GATE-EMOJI-01](sprints/2026-07-27-GATE-EMOJI-01-o-higienizador-apaga-o-que-o-adr-protege.md) | E1: colar um emoji, salvar pelo editor dela, e ver se os 238 glifos do ADR-011 sobrevivem. Só a máquina dela responde | DELA |

---

## 4. BURACOS DE TEXTO — atacados em 22/08, e o que ficou

Os oito buracos de código desta lista foram para a fila da seção 1. Ficam aqui os
oito de texto: **todos foram atacados na leva de 22/08 e nenhum fechou por
completo**. Um cético mediu o que sobrou de cada um, e é só isso que vale ler —
a correção original saiu, porque já foi feita.

| Onde | O que foi atacado em 22/08 | O que FALTA |
|---|---|---|
| `docs/data/LEIA-PRIMEIRO.md` | Os quatro buracos da porta de entrada das specs (o mapa 302x45, as tabelas de 616 e 604, as quatro colunas do eixo de ponte, o parágrafo do `mapa-resumo.csv`). O arquivo de hoje tem 99 linhas e os números novos | A frase da "cura de raiz", no fim da seção 1, diz que o `Resumo do censo` do `scripts/check_paridade_transporte.py` "já imprime quase todos os contadores das seções 1 a 3". MEDIDO em 22/08, rodando o portão: o resumo imprime 18 números, e **11** deles aparecem nessas seções (308, 616, 124, 64, 14, 36, 177, 16, 4 e dois zeros). Continuam digitados à mão os bytes dos 10 arquivos, as 47 colunas, os 13 pares, o `existe`, as duas réguas por valor e as 20 casas do cruzamento. Trocar "quase todos" pelo que é: os do censo do mapa, e só |
| `docs/usage/metrics.md` | A negativa caduca na doc de uso e no `README.md`; o `docs/adr/016-prometheus-metrics.md` ganhou nota datada | O valor antigo sobreviveu no lugar de onde a próxima pessoa copia o fato como medido: `tests/unit/portao_a_casa_sabe_e_o_produto_nao_faz.py`, linhas 360 e 458, ainda afirmam que "a única ocorrência fora de src/" é o changelog do pacote Fedora. Trocar pelo par medido usado em `metrics.md`, e o ponteiro `spec:420` (morto) por `spec:459`. Modelo pronto na entrada irmã da linha 446, que já usa a redação escopada |
| `docs/usage/cli.md` | O bloco do aviso de falha conhecida (defeito corrigido em 25/07) saiu, e o corpo ganhou os comandos e ações que faltavam | (1) A frase nova de 353-355 diz "outras marcas", e `discover_external_gamepads` exclui por VID/PID de DualSense e Edge — um DualShock 4 cai como externo; e os externos ENTRAM em "controles na mesa". (2) A linha 335 e a nota de 06/08 ensinam a saída `jogadores ativos: 1`, que a CLI não produz mais — a nota fica, com uma linha dizendo o que mudou. (3) O `help=` e o docstring de `.../cli/cmd_test.py` contradizem a seção nova: é produto, e o `--help` é a primeira boca. (4) `docs/protocol/trigger-modes.md`, linhas 111 e 118, ainda mandam a linha que a DOC-QUE-NAO-MENTE-04 classificou como mentira em 03/08. (5) Menor: `cli/app.py` na linha 126 faz o comando de produto `led` chamar `cmd_test.cmd_led` |
| `docs/usage/hotkeys.md` | A linha do gesto na tabela, o parágrafo do R3 e a ressalva de prova de plástico | "e o jogo passou a andar" não tem prova: o journal sustenta a troca de máscara e o vpad Xbox subindo com o jogo aberto, e a escada encerrou por `jogo_fechou` sem carimbo. A condição "só com jogo na mão" vale para o aviso de RISCO, não para a sequência de FALHA. O parágrafo da escada precisa da ressalva: sem carimbo, o degrau só vence o ciclo quando o próximo é alcançável ao vivo. Ainda contradizem a página: `docs/process/METODO-DE-ISOLAMENTO.md` (973-976) e `sprints/2026-08-19-O-QUE-PRECISA-DE-VOCE.md` (29). E a bancada de 19→20/08 não está em `docs/data/ensaios.csv` — sem ela, a linha do verde entre as cinco cores fica travada. Nit herdado: `#ffb86c` é "laranja" aqui e "âmbar" em dois documentos |
| `docs/usage/jogos-e-mascaras.md` | O caminho real para desfazer a exceção do Steam Input, mais os dois comandos de CLI, com teste novo que reprova a volta da mentira | A página promete um diálogo que o código não faz nascer: `.../app/actions/profiles_actions.py`, por volta de 1918, não relê o sinal ao vivo antes de perguntar. Ou chamar `_ha_jogo_aberto_agora()` ali (uma linha, com teste que MORDA), ou qualificar a frase. Dentro da mesma função, a docstring de 1877-1880 ainda abre com "Sem diálogo", refutada pelo bloco abaixo dela. Fora dela: `.../integrations/steam_launch_options.py` (1256-1258) repete a frase que a página marca como REFUTADA e que o `gui/main.glade` já corrigiu; `2026-08-07-PAINEL-as-nove-decisoes-que-esperam-ela.md` (25) caducou em 07/08; e `docs/usage/interface.md` (447) precisa espelhar |
| `docs/usage/creating-profiles.md` | A seção `ponte` entrou na doc de perfis, e o gesto na doc de gestos | O gesto está invertido: ele diz "esta ponte NÃO serve" e move a escada; quem carimba é o SILÊNCIO, uma vez só, pelo tique de 1 Hz em `.../daemon/launch_env.py`. Hoje o único caso aparece como secundário. `confirmada_por` promete `gesto` e `escolha_dela`, e nenhum dos dois tem escritor em `src/` — o único chamador grava `silencio`. O mesmo fato errado está no comentário de `.../daemon/ipc_handlers.py` (1897-1901), que é provavelmente a fonte: a varredura do valor antigo não pode parar em `docs/`. E o `volume` do mic não entra em TODA ativação: a trava manual de áudio vence o perfil (`profiles/manager.py`, 822-827) |
| `.../integrations/prontuario_dos_jogos.py` | As três frases falsas (o doctor e a GUI que não consomem, e o "não escreve em lugar nenhum" que caducou em 19/08) | O `COMO-EXECUTAR.md` da sprint da aba Configurações cita a docstring apagada palavra por palavra, nas linhas 2000 e 3090, e manda "copiar a forma" de um padrão que declara existir TRÊS vezes. MEDIDO: são DUAS (`scripts/doctor.sh` nas linhas 1613 e 3235); o prontuário não é consumido por ninguém, e é justamente o terceiro exemplo. Corrigir a citação, o número e o ponteiro `:505`, que hoje é `:519` |
| `.../core/rumble.py` | O número do dono declarado: Máximo vale 1,5, e nunca valeu 2.0 | BLOQUEANTE: `tests/unit/test_politica_de_vibracao_a_escada_que_amplifica.py` diz "200%" na linha 236 e "1,5" na linha 8 — o arquivo se contradiz consigo mesmo. Mesma regra, mesmo tratamento: número errado sai, sem nota nem data. Menor, herdado: o empate do degrau 1.0 do automático com o Balanceado veio de o BALANCEADO subir de 0,7 para 1,0 em `496ba05`, não de o Máximo subir. Menor: a linha 89 continua importando a tabela de `daemon/lifecycle.py` (re-export), não do dono declarado `daemon/subsystems/rumble.py` |

**A lição que custou uma sessão inteira, 22/08/2026:** o commit `c4471a1` curou o
`docs/data/LEIA-PRIMEIRO.md` e, no MESMO commit, escreveu os quatro buracos dele
aqui como abertos. O backlog nasceu defasado, e o agente seguinte gastou a sessão
remedindo buraco já curado. Quem ataca um buraco fecha a linha dele na mesma
leva — esta seção não é registro do que se achou, é fila do que falta.

---

## 4.1. AS 28 PARCIAIS TRIADAS — e por que NENHUMA é barata

Das 87 parciais, 28 não dependem dela. Quatro agentes mediram o custo real de
fechar cada uma, e um cético conferiu as seis que pareciam baratas.

| Classe | Quantas |
|---|---|
| `CONSTRUIR` — falta código de verdade | **12** |
| `SO_TESTE` — a cura existe, falta teste que morda | 5 |
| `NAO_FECHA_SEM_HARDWARE` — o censo não viu que precisa da bancada | 4 |
| `SO_LIGAR` — código pronto, falta chamador | 4 |
| `JA_FECHADA` — o censo teria errado | 2 |
| `SO_DOC` | 1 |

**O cético derrubou as SEIS.** As duas `JA_FECHADA` continuam abertas e as
quatro `SO_LIGAR` não são "só ligar":

| Sprint | Era | É | Por quê |
|---|---|---|---|
| PROMESSA-NAO-CUMPRIDA-01 | `SO_LIGAR` | faxina cara | O item que a sustentava (C1, métricas sem chave) está **fechado desde 01/08**, com código, teste, doc e nota de ADR. A página acusa nove coisas já feitas |
| JOGO-01 | `SO_LIGAR` | **caducada** | `vpad_suspenso` **nunca fica `True`** num daemon de hoje. O dado que se mandaria "ligar" está morto, e o vocabulário foi invertido por decisão dela depois da sprint |
| PERFIL-NASCE-CERTO-01 | `SO_LIGAR` | aberta e cara | O botão existe desde 06/08, mas o **gesto que ele dispara ficou inerte** quando a E2 entrou — e a própria E2 escreveu isso |
| MASCARA-POR-JOGADOR-01 | `SO_LIGAR` | **escolha** | As peças existem; o que falta é decidir, não ligar |
| DOC-VERDADE-01 | `JA_FECHADA` | aberta | A régua da classificação estava errada: grepou nome velho e achou zero |
| ORDEM-DE-CHEGADA-01 | `JA_FECHADA` | aberta | Existe **decisão datada de NÃO ligar**, dentro da própria lápide usada como prova a favor |

**A conclusão prática:** não há fruta baixa nas parciais. O que parecia "uma
hora" é faxina documental, feature caducada ou decisão dela. A contagem do
cabeçalho (74/87/40) **não muda** — as duas `JA_FECHADA` foram derrubadas.

Um achado que vale sprint própria: **`vpad_suspenso` nunca fica `True`**. É
estado publicado que ninguém pode observar, e há texto de tela que depende dele.

---

## 5. O QUE PRECISA DELA — são SEIS, não 84

**O documento é [`DECISOES.md`](../../DECISOES.md), na raiz.** Ele tem o print, as
opções e o custo de cada uma. Esta seção não repete o conteúdo dele.

O censo marcou 84 sprints como dependentes dela. Seis agentes leram uma a uma e
extraíram **163 perguntas**; um cético independente conferiu cada uma, com uma
instrução acima das outras: *antes de aceitar, procure se já foi decidida.*

```
163  perguntas extraídas
 23  descartadas: não eram decisão dela, eram trabalho
 54  DERRUBADAS — já tinham resposta, com data e lugar
  6  sobreviveram        (29 a 39 minutos, no total)
```

O projeto carregava um peso falso. As 54 já respondidas estão no fim do
`DECISOES.md`, em tabela, para ninguém reabri-las — e em quatro delas a coluna
de data ficou com travessão, porque a pergunta estava **mal feita**, não
respondida.

Os quatro gestos abaixo continuam descrevendo o TIPO de trabalho que sobra nas
sprints marcadas `DELA` na seção 3 — a maior parte é bancada e olho na tela, que
não são decisão e por isso não entram no `DECISOES.md`:

| Gesto | O que destranca |
|---|---|
| **Controle na mão, com a bancada** | a faixa 5 quase inteira, a CHECKLIST de hardware, a PROVA-NO-PLASTICO-01 e o roteiro de 40 min de 19/08 |
| **Olho na tela, foto antes e depois** | a faixa 4 inteira — por PROVA-DE-TELA-01, interface não fecha sem a palavra dela |
| **Palavra de vocabulário e de texto de interface** | GATILHO-PALAVRA-01 (as dezenove palavras), ONDE-A-COR-MORA-01 (as três perguntas), TRES-MODOS-DO-SOM-01 (P-1 a P-5), a frase do travessão da FIACAO-QUE-FALTA-01 |
| **Decisão de projeto, com o preço na mesa** | BUSCA-QUE-ESTOURA-01 (os cinco desenhos), DROPIN-AMBIGUO-01 (a migração), RADIO-ABERTO-01 e CONECTA-E-DESLIGA-01 (o preço que ninguém perguntou se ela aceitava), IDENTIDADE-DUPLA-01 (o MAC de cada modo, 2 minutos) |

As perguntas já escritas e ainda sem resposta estão em
[AS DECISÕES QUE ESPERAM VOCÊ](2026-08-15-AS-DECISOES-QUE-ESPERAM-VOCE.md) e em
[O QUE PRECISA DE VOCÊ (19/08)](sprints/2026-08-19-O-QUE-PRECISA-DE-VOCE.md).

---

## 6. A regra deste arquivo

Quem fecha uma sprint atualiza aqui, no mesmo commit — tira a linha da seção 3
e corrige a contagem do cabeçalho. Quem abre uma sprint nova põe a linha na
faixa a que ela pertence. Este arquivo não tem portão: ele vale exatamente o
que a última pessoa que o tocou escreveu.
