# A madrugada em que o produto era o réu — índice de 08/08/2026

- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que este arquivo é:** o **ponto de entrada** de quem for executar o que
  sobrou desta noite. Não é resumo: é a fila, com o que já entrou e o que falta
- **Por que ele existe:** ela pediu — *"salve a documentação das sprints à medida
  que as ondas avançam"* — e passou o projeto: *"seja o dono do projeto"*

**Grau, como manda a casa:** **MEDIDO** = há journal, `grep` ou teste que fecha a
conta; **SUSPEITA COM MECANISMO** = o caminho foi lido e fecha, o efeito não foi
observado; **SEM PROVA** = está dito e ninguém verificou; **DECISÃO DELA** = não
se repropõe.

---

## 1. A noite em uma frase

**Ela relatou seis defeitos. Cinco eram nossos, e quatro já estão curados.**

O padrão que atravessa a noite inteira, e que é o achado de método mais caro:
**quase tudo o que a atrapalhou era proteção nossa funcionando como escrita.** Um
watchdog que ligamos, uma vigia que reinicia, uma caixinha que ela marcou, um
agente que sumia — nenhum deles é bug de descuido. São decisões corretas em
isolamento, produzindo dano em conjunto.

---

## 2. O que ENTROU nesta madrugada

| # | sprint | o que curou | teste que morde |
|---|---|---|---|
| 1 | [PARTIDA-PICOTADA-01](2026-08-08-PARTIDA-PICOTADA-01-a-caixinha-que-tirava-o-jogador-2-a-cada-piscada.md) | tique cego não derruba mais a exceção de Steam Input — o vpad para de ser recriado no meio da partida | `test_partida_picotada_01.py` (4 de 9 reprovam sem a cura) |
| 2 | [BLUETOOTHD-MORTO-POR-NÓS-01](2026-08-08-BLUETOOTHD-MORTO-POR-NOS-01-o-watchdog-que-ligamos-matou-o-radio-dela.md) | `WatchdogSec=0` — paramos de mandar o systemd matar o `bluetoothd` dela | `test_bt_resilience_assets.py` (exige o zero) |
| 3 | *(mesma sprint)* | o agente de pareamento volta em 250 ms, não em 5 s | `test_agente_que_some_01.py` |
| 4 | *(mesma sprint)* | a vigia exige **dois aparelhos** distintos antes de reiniciar o rádio | `test_vigia_que_derruba_01.py` |
| 5 | [CADERNO-QUE-NÃO-ESCREVE-01](2026-08-08-CADERNO-QUE-NAO-ESCREVE-01-o-reboot-provou-o-fflush-e-salvou-os-eventos.md) | `mawk -W interactive` — o caderno da vigia volta a escrever | `test_caderno_que_nao_escreve_01.py` (reprova com zero byte) |
| 6 | [SEGUNDO-ESCRITOR-01](2026-08-08-SEGUNDO-ESCRITOR-01-o-driver-do-kernel-tambem-escreve-a-barra.md) | *(diagnóstico)* o segundo escritor do storm é o driver do kernel | — |

**Estado da árvore:** suíte inteira verde (**7.782** testes), `ruff` limpo, `mypy`
limpo em 165 arquivos, os oito portões da casa em zero.

---

## 3. A causa da regressão que ela sentiu

**GRAU: MEDIDO**, com carimbo de hora.

> *"na semana passada no sábado jogamos horas com 3 controles do usb nenhum
> problema"*

O delta é **um appid numa lista**:

```
~/.config/hefesto-dualsense4unix/steam_input_apps.txt   mtime 08/08 01:43:16
    # marcado no editor de perfil
    1599660
```

Ela marcou a caixinha do Steam Input no editor do perfil do Sackboy às
**01:43:16**. A primeira suspensão de gamepad virtual veio **14 segundos depois**.

| janela | duração | quedas de vpad | por hora |
|---|---|---|---|
| sábado 01-02/08 | **48 h** | 15 (todas de outro jogo) | 0,31 |
| 08/08, a partida dela | **1h25** | **12** | **8,5** |

**Vinte e sete vezes mais.** Cada queda derrubava o jogador 2 do co-op.

E o gatilho de cada ciclo não era o jogo sair da frente — era um tique que **não
sabia de nada**: `wm_class=unknown` (o backend não leu) ou a classe da **própria
janela do Hefesto**, quando ela ia mexer na configuração. O autoswitch já filtrava
as duas; a exceção de Steam Input lia a mesma leitura e não filtrava nenhuma.

---

## 4. O que espera a palavra dela

**Isto não é trabalho: é decisão.** Nenhuma deve ser respondida por quem executa.

| # | assunto | a pergunta, pronta |
|---|---|---|
| 1 | **a semântica da caixinha** | *"Você decidiu que a allowlist do Steam Input NÃO tira o Hefesto da frente. No código, marcar a caixinha faz o oposto: solta o grab, derruba o gamepad virtual e tira o jogador 2. Qual das duas fica — a caixinha passa a preservar o co-op, ou ela recusa a marca quando há dois controles?"* |
| 2 | **o appid na sua lista** | *"O Sackboy continua marcado. A cura de hoje impede que a marca pique a partida, mas ela continua tirando o jogador 2 quando o jogo está na frente. Desmarco?"* |
| 3 | **o ciclo desinstalar/instalar** | *"Está tudo pronto para rodar, e há um perigo medido: o desinstalador apaga os snapshots de pareamento. Rodo com uma cópia deles fora, ou você prefere acompanhar?"* |
| 4 | **o `main.conf` colapsado** | *"O seu `/etc/bluetooth/main.conf` tem 38 linhas; o original da distro tem 384. Em comportamento não muda nada, mas a documentação no disco se perdeu. Restauro o original antes do próximo install?"* |

---

## 5. O que espera o hardware na mão dela

| # | o que | custo dela | o que decide |
|---|---|---|---|
| 1 | **a prova da cura** — abrir o Sackboy com os dois controles e ver se o vpad para de cair | 10 min | é a única prova que falta da PARTIDA-PICOTADA-01 |
| 2 | **ligar e desligar o Pro três vezes** | 2 min | fecha a causalidade da SEGUNDO-ESCRITOR-01 (hoje: duas ocorrências, sem contraste) |
| 3 | **o storm com quatro controles** | uma sessão | a refutação *"o storm não derruba o Pro"* foi medida com dois a três |

---

## 6. O que fica ABERTO, em ordem de execução

### LEVA A — o que ela sente, e ainda não foi curado

| item | o que entra | custo | grau |
|---|---|---|---|
| **A-1** | `apply_profile_mode` devolve APLICADO sem olhar se o gamepad subiu. Medido: `gamepad_start_recusado_steam_input` e, **138 µs depois**, `mode=aplicado` | P | MEDIDO |
| **A-2** | o portão anti-recriação de vpad é cego para o caminho da exceção — ele cobre `Daemon.set_gamepad_*`, e a suspensão chama `stop_gamepad_emulation` por baixo | P a M | MEDIDO |
| **A-3** | o engasgo tem **duas** causas: a nossa (recriação de vpad) e uma **elétrica** (a porta USB derrubou o segundo DualSense 16 vezes em 3 h). A segunda não é nossa e não foi tocada | M | MEDIDO |

### LEVA B — o rádio, o que sobrou

| item | o que entra | custo | grau |
|---|---|---|---|
| **B-1** | **restauro automático de bonds.** Decisão dela de 08/08: manual com `sudo` não é produto. O snapshot já grava sozinho; falta o gatilho da volta, e ele tem de ser **seletivo** — restaurar chave velha quando o par rotacionou gera loop de autenticação | G | DECISÃO DELA |
| **B-2** | o `main.conf` colapsado (384 linhas viraram 38) | P | MEDIDO |
| **B-3** | 41 backups `main.conf.bak.hefesto-*` acumulados em `/etc/bluetooth` | P | MEDIDO |

### LEVA C — máquina limpa (a régua da resposta 17)

| item | o que entra | custo | grau |
|---|---|---|---|
| **C-1** | **nenhuma cura de Bluetooth entra no `.deb`** — nem o drop-in, nem os dois timers, nem as units. Quem instalar pelo pacote não recebe nada disto | G | MEDIDO |
| **C-2** | o portão de paridade é **cego** a toda a camada de Bluetooth de sistema | M | MEDIDO |
| **C-3** | **OQ-6** — a regra de udev dos nós de entrada nunca foi escrita; o touchpad e o giroscópio dela só funcionam porque ela está no grupo `input` **por fora** | M | MEDIDO |
| **C-4** | o áudio inteiro é pulado nos formatos flatpak/appimage/deb | M | MEDIDO |
| **C-5** | os drop-ins de WirePlumber não são empacotados | G | MEDIDO |
| **C-6** | a ponte de mic por Bluetooth não tem gate em instalador nenhum | G | MEDIDO |

### LEVA D — o instrumento

| item | o que entra | custo | grau |
|---|---|---|---|
| **D-1** | a `CR-9`: o `storm_watch.sh` roda com `-n0`, então o caderno começa do zero a cada partida. **Anda junto com a cura de hoje** — destravado o cano, ele passa a crescer, e não tem teto | P |  MEDIDO |
| **D-2** | a previsão do E-1 precisa de nota datada: *"zero recusas"* é inatingível, porque o driver produz 1-2 por conexão de externo | P | MEDIDO |

---

## 7. O que NÃO entra, e por quê

| o que | por quê |
|---|---|
| **desmarcar o Sackboy da allowlist dela** | é a marca **dela**, feita na tela. Desfazer sem pedir é a casa decidindo no lugar dela. A cura entrou no código, que é o que vale para quem instalar amanhã |
| **o dongle / a porta USB como causa do rádio** | **ela vetou por escrito**, e tem razão pelo histórico: *"já perdemos dias na tese de ser o dongle ou porta usb, não é… É nossa configuração."* Era |
| **o `[General]` duplicado no `main.conf`** | parecia defeito nosso de escrita. O parser real (GKeyFile) **aceita e faz merge** — conferido contra a biblioteca de verdade, não contra a réplica |
| **o diário de bateria como causa do engasgo** | era o suspeito nº 1 da encomenda. **INOCENTE** |
| **o co-op nascer ligado** | já nascia ligado no sábado — não é o delta |
| **o commit `10f4818`** | não quebrou o caminho do jogo |

---

## 8. Os três achados de método desta noite

Valem além dos defeitos que os produziram.

1. **Um portão que aceita qualquer valor não trava valor nenhum.** O teste do
   `WatchdogSec` exigia `\d+` e ficou verde enquanto o valor matava o rádio dela.
   Se o que importa é o número, o número tem de estar no teste.
2. **Uma bancada que só mede a hipótese favorita confirma a hipótese favorita.** A
   cura do caderno "era" `fflush()` — plausível, com mecanismo, e errada. O que a
   derrubou foi medir **três variantes lado a lado**.
3. **A auditoria de risco de uma leva não pode parar no título dela.** O commit
   `6b1cb62` se chama *"a caixinha que TIRA… e a luz que calou"*; a metade da luz
   é mesmo só dos externos, mas a **mesma leva** trouxe a caixinha — e é por ali
   que aquele commit chegou ao DualSense por cabo.

E um quarto, que é de instrumento e já custou quatro medições falsas em dois dias:
**`journalctl -k` implica o boot atual.** Em qualquer janela que atravesse reboot
ele devolve zero, e zero é indistinguível de "não houve nada". Use
`_TRANSPORT=kernel`.

---

## 9. Nota de honestidade

**O que foi tocado na máquina dela:** nada. Nenhum serviço reiniciado, nada escrito
em `/etc`, nenhuma configuração dela alterada, nenhum controle derrubado. As curas
estão no **repositório**, e valem na máquina dela no próximo `install.sh` — que é
a régua que ela fixou hoje.

**O que foi tocado no repositório:** cinco arquivos de código e cinco de teste,
quatro sprints e este índice.

**Duas ondas de agentes rodaram e as duas foram interrompidas** por limite de
conta, depois de 70 investigações concluídas. Os resultados foram recuperados do
journal das ondas e estão citados aqui; as verificações adversariais que não
rodaram estão declaradas como o que são — **não rodaram**, e por isso os achados
que dependiam só delas não viraram cura.

**Um erro meu foi corrigido por nota datada, não apagado:** a sprint do caderno
afirmava que o reboot provou o `fflush` e promovia o grau a MEDIDO. Era falso em
duas frentes — o `SIGTERM` destrói o buffer em vez de descarregar, e a causa nem
era o buffer de saída. A nota está lá, com o porquê.
