# DROPIN-AMBIGUO-01 — a ausência do drop-in é indistinguível de escolha dela

- **Descoberta:** 04/08/2026, madrugada, depois de ela dizer *"desarmamos algo
  que não esquecemos de armar corretamente"*
- **Gravidade:** média-alta — um portão que dá `[OK]` no meio do defeito
- **Estado:** aberta
- **Pré-requisito:** nenhum. É código de portão, não toca no rádio.

---

## O que aconteceu

O arquivo `~/.config/wireplumber/wireplumber.conf.d/51-hefesto-dualsense-no-default-source.conf`
**não existia** na máquina dela. Sem ele o WirePlumber promoveu o DualSense a
microfone padrão do sistema, e daí saíram os três sintomas que ela reportou como
*"não funciona nem mic, nem os botões de sons do jogo"*.

O `doctor.sh --fix` o recriou às 00:37 de 04/08. O histórico completo está em
[A noite em que o som do controle voltou](../estudos/2026-08-04-a-noite-em-que-o-som-do-controle-voltou.md).

---

## A causa-raiz: um estado, dois significados

| quem | o que faz |
|---|---|
| `install.sh`, passo 10 | **arma** o drop-in (default; opt-out `--keep-dualsense-mic`) |
| `uninstall.sh:125` | **desarma** |
| `scripts/fix_wireplumber_default_source.sh --promote-source` | desarma, **a pedido dela** |
| `hefesto mic promote` | idem |
| `scripts/doctor.sh:536`, em `_prefere_mic_do_dualsense` | lê a ausência como **promoção explícita** |

O comentário do doctor é honesto sobre o que faz, e vale citar porque é a
decisão que esta sprint precisa preservar:

> *"O drop-in 51 é a política DEFAULT do install: rebaixar. Enquanto ele estiver
> no lugar, o controle é a ÚLTIMA opção — não a primeira. Sua ausência (ex.:
> `--promote-source`, `mic promote`) é a promoção explícita."*

O raciocínio está certo **para o caso que ele imaginou**. O buraco é que a
ausência tem **duas origens** e o arquivo não distingue:

- *"ela pediu para promover o mic do controle"* — decisão dela, a honrar;
- *"o uninstall removeu, e a instalação seguinte não rearmou / nunca houve
  instalação"* — cura desarmada, a reparar.

**Máquina curada e máquina quebrada são o mesmo estado para o portão.** É a
mesma cegueira do `check_bt_sdp_cache_envenenado`, que dava `[OK]` no meio do
defeito porque filtrava só quem já tinha `Services=` — cego **na proporção da
gravidade**.

---

## O que já foi feito, e o que NÃO resolve

Em 04/08 o `install.sh` passou a rodar o `doctor.sh` no fim, por padrão
(`CONFERENCIA-FINAL-01`, opt-out `--no-doctor`). Isso fecha o caso **prático**
mais comum: uma instalação que termine com o drop-in ausente agora imprime a
FALHA do sintoma (*"DualSense é o microfone ATIVO com outra fonte disponível"*).

**Não resolve a ambiguidade**, e é importante ser claro sobre isso:

1. a FALHA depende do **sintoma estar manifesto** — com o DualSense desligado
   na hora da instalação, não há microfone ativo e não há falha a emitir;
2. quem promoveu o mic **de propósito** continua recebendo a mesma FALHA, o que
   ensina a ignorá-la — e um aviso que se aprende a ignorar é pior que nenhum;
3. o `doctor.sh` fora do install segue cego.

---

## A cura

**E1. A promoção deixa marca própria.** Quem promove — `--promote-source`,
`mic promote` — grava um arquivo que diz *"a ausência do 51 aqui é escolha
dela, em <data>"*. O nome e o lugar são decisão da sprint; o requisito é que a
marca seja **do gesto**, não do estado.

Por que a marca vai no gesto de promover, e não no de instalar: o gesto de
promover é raro e explícito; o de instalar é frequente e automático. Marcar o
raro dá um portão que erra para o lado seguro — sem marca, presume-se defeito,
e o pior caso é um aviso a quem promoveu antes desta cura existir.

**E2. O `_prefere_mic_do_dualsense` passa a ler a marca**, não a ausência. Os
outros dois degraus dele (drop-in 52 e `DUALSENSE_MIC_INTENDED`) já são sinais
explícitos e ficam como estão — só o terceiro degrau muda.

**E3. Um check novo, que fala do ARQUIVO e não do sintoma.** Hoje o doctor só
sabe dizer *"o DualSense é o microfone ativo"*. Falta a linha que diz *"a cura
padrão do install não está armada, e ninguém pediu para promover"* — com o
comando exato para rearmar. Este check tem de valer **com o controle desligado**,
que é justamente quando o sintoma não aparece.

**E4. A migração honesta.** Máquinas que hoje têm o 51 ausente por promoção
legítima não têm marca nenhuma. A sprint decide entre: (a) o primeiro `doctor
--fix` depois desta cura pergunta/assume, registrando o que assumiu; ou (b) a
ausência sem marca é tratada como defeito e o aviso ensina a criar a marca.
**Escolher (b) sem dizer isso em voz alta seria reescrever a escolha dela em
silêncio** — que é o defeito que a `PERFIS-SEM-DONO` já custou a esta casa.

**E5. Varrer os irmãos.** O drop-in 51 quase certamente não é o único par
`uninstall remove` / `doctor lê ausência como intenção`. O commit `9c944a8`
("o ciclo uninstall+install desligava SEIS curas em silencio") já pagou por
essa família uma vez. A sprint entrega a **lista completa** dos arquivos que o
uninstall remove, cruzada com quem confere cada um — e diz quantos têm o mesmo
buraco.

---

## Aceite

1. com o drop-in 51 ausente **e sem marca de promoção**, o `doctor.sh` reprova
   e diz o comando de rearmar — **mesmo com nenhum controle conectado**;
2. depois de `mic promote`, o `doctor.sh` **não** reclama do 51;
3. depois de `mic promote` seguido de `install.sh`, o comportamento é o que a
   sprint tiver decidido em E4, **e está escrito no documento** — não descoberto
   por quem for usar;
4. a lista de E5 existe no repositório, com o veredito de cada linha;
5. teste que morde: arrancar a leitura da marca faz reprovar um caso em que hoje
   passa.

---

## Relacionado

- [A noite em que o som do controle voltou](../estudos/2026-08-04-a-noite-em-que-o-som-do-controle-voltou.md)
- [DOC-QUE-NAO-MENTE-04](2026-08-03-DOC-QUE-NAO-MENTE-04-os-nove-mecanismos-e-os-seis-portoes.md) — a família dos portões cegos
