# A NOITE DOS QUATRO INVENTÁRIOS — a distância entre o que a casa sabe e o que o produto faz

- **Escrito em:** 09/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que este arquivo é:** a fila executável do que sobrou da noite de 08→09/08,
  e o registro de **quatro hipóteses minhas derrubadas por medição** — três delas
  derrubadas por ela
- **Grau:** tudo abaixo é **MEDIDO** salvo onde diz o contrário

---

## 1. A noite em uma frase

**O produto sabe muito mais do que faz.** Quatro inventários mediram a mesma
distância por quatro ângulos: a causa do defeito de hoje estava escrita no
repositório desde 25/07; a cura de ontem está no disco dela e não em vigor; doze
passos de cura não entram em nenhum formato que não seja `native`; e a janela não
sabe dizer que um controle sumiu.

---

## 2. As hipóteses que caíram, e quem as derrubou

Fica registrado porque o padrão importa mais que os erros: **três das quatro
foram derrubadas por ela, com observação direta do aparelho.**

| hipótese minha | quem derrubou | com o quê |
|---|---|---|
| o `skip_cache` da lightbar era o culpado | verificação adversarial | o log só sai DEPOIS de uma escrita bem-sucedida, e aparecia igual no dia em que a luz funcionava |
| a `A-LUZ-QUE-CUROU-01` (07/08) causou a regressão da barra | verificação adversarial | aquela sprint não tocou uma linha de código de lightbar |
| a caixinha do Steam Input matou o rumble | **ela** | *"funcionava com o input steam ligado e com ele desligado"* |
| o dongle/porta USB degradando o rádio | **ela**, pela segunda vez em duas semanas | *"milhares de vezes provamos que a tese é inválida"* — e o índice de 08/08 §7 já registrava o veto |
| a curva 12→37 era degradação dos DualSense | dois agentes, em separado | as falhas eram do 8BitDo e do DualShock 4; contadas por aparelho, os DualSense só aparecem em 08/08 |

**A regra que a noite reforça:** hipótese que não explica o que JÁ funcionava é
contorno. As quatro falharam nesse teste, e as quatro eram minhas.

---

## 3. A causa do controle que some — MEDIDA, e escrita desde 25/07

O sintoma dela: um DualSense conecta, acende azul, **sem LED de jogador**, e o
Hefesto não o enxerga. A aba Início chega a dizer *"Nenhum controle conectado"*.

A cadeia, e cada elo tem endereço:

1. `playstation …: Failed to retrieve feature with reportID 32: -5` (×3) →
   `Failed to create dualsense` → `probe with driver playstation failed`;
2. o `-5` é **máscara**: o BT achata qualquer erro de transporte em `-EIO`
   (`assets/dkms/hid-playstation/README.md:62-114`);
3. **quem desistiu foi o BlueZ**, não o kernel: `hidp_report_req_timeout()`,
   `REPORT_REQ_TIMEOUT` = **3 s**. Confirmado no journal dela em 08/08 23:36:14,
   :17 e :20, casado um a um com as três falhas do driver;
4. **o gatilho é dois DualSense subindo no mesmo adaptador com ~1 s de
   diferença** — o segundo perde o canal de controle L2CAP. Em 23:36:10 um
   registrou e o outro nasceu no mesmo segundo.

**Os 6 abortos de 08/08 recuperaram sozinhos** (2 a 20 min), por reconexão — não
por rebind. Não há controle órfão agora.

### 3.1 O achado que é NOSSO, e é a cura de raiz

**O retry que esta casa escreveu no patch do kernel não pode funcionar.**

- cada tentativa custa os **3 s inteiros** do BlueZ;
- o backoff entre elas é de **100 ms e 200 ms**
  (`assets/dkms/hid-playstation/hid-playstation.c:36`, `:902-920`);
- logo, **as três tentativas caem dentro da mesma janela de contenção**. Medido:
  00:17:04 → :07 → :10 → aborto.

O espaçamento é ~30× pequeno demais para o problema que ele se propõe a
atravessar. É por isso que o rebind — que espera **minutos** — cura, e o retry
não. Custo atual: a falha demora ~10 s em vez de ~3,3 s.

**Nota datada devida:** o `README.md:234-244` declarava *"que `feature_retries=2`
de fato cura"* como **NÃO MEDIDO**, com a validação prevista para o próximo boot.
A validação chegou: **6 de 6 abortos retentaram e nenhum foi salvo.** A hipótese
caiu.

E o próximo degrau já estava nomeado no mesmo README, há 14 dias, sem nunca virar
código: *"ou **serializar a subida dos controles** no daemon do hefesto"*.

---

## 4. A FILA — em ordem de raiz, não de esforço

### F-1 — o backoff do retry passa a cavalgar o timeout do BlueZ
`assets/dkms/hid-playstation/` + `assets/modprobe.d/hefesto-hid-playstation.conf`.
De 100/200 ms para além dos 3 s. **Teste que morde:** o patch declara o
espaçamento em função do teto do BlueZ, e um portão reprova quem o reduzir sem
nota. **Grau da cura: SUSPEITA COM MECANISMO** — o mecanismo é medido, o efeito
só se prova no próximo par de conexões simultâneas dela.

### F-2 — serializar a subida de dois controles no mesmo adaptador
O degrau nomeado há 14 dias. Ninguém, no produto, espaça duas conexões BT.
**Aberto: onde mora a serialização** (daemon? agente de pareamento? udev?) —
decisão de desenho, não de código.

### F-3 — o `WatchdogSec=0` em VIGOR, e um portão que meça isso
Na máquina dela, agora: o drop-in tem `WatchdogSec=0` e
`systemctl show -p WatchdogUSec` devolve **`30s`**. **Cura no disco ≠ cura em
vigor**, e o `doctor.sh` **não lê `WatchdogUSec` em lugar nenhum** — máquina
curada e máquina que vai morrer imprimem o mesmo veredito.

### F-4 — detector de probe morto do `hid-playstation` no doctor
Existe para o Pro Controller
(`doctor.sh:3495`, `_check_hid_nintendo_probe_death_signature`) e **não existe**
para o DualSense (`doctor.sh:308-315` só confere se o módulo carregou).

### F-5 — a janela precisa saber dizer "visto no rádio, não adotado"
Hoje `describe_controllers` devolve uma entrada **por handle aberto**; sem
hidraw não há handle, e a aba Início escreve *"Nenhum controle conectado"* para
um controle ligado e pareado. **Não existe no produto a noção de controle
não-adotado.**

### F-6 — as três telas que mentem
- **(a)** aba Status afirma "Conectado · USB · 85%" com a mesa vazia — o topo do
  `state_full` (`daemon/ipc_handlers.py:1644-1648`) é mantido em PARALELO à lista
  (`:1724`), nunca derivado dela. É a `ESTADO-QUE-MENTE-01` de 03/08, ainda
  proposta, sem teste;
- **(b)** o toast *"Cor aplicada no controle"*
  (`app/actions/lightbar_actions.py:636-643`) sai do `ok` do daemon, que
  significa "o report saiu" — nunca "a barra acendeu";
- **(c)** `rumble_ff.plays` só aparece na tela **quando é > 0**
  (`app/actions/rumble_actions.py:571-573`): a linha fica muda exatamente no caso
  em que teria algo a dizer.

### F-7 — o `install.sh` desiste na linha 941
Com `FORMAT != native`, ele roda cinco passos e faz `exit 0`. **Doze passos de
cura** ficam de fora — toda a camada de Bluetooth de sistema, o áudio, o wrapper
`hefesto-launch`, o kernel-watch e a conferência final. E o aviso que o próprio
script imprime (`:936-938`) **lista errado** o que está pulando.

### F-8 — o touchpad e o giroscópio dela funcionam por acidente
Nenhuma regra em `assets/*.rules` dá acesso aos nós `/dev/input/event*`;
`install_udev.sh:81-91` cria o grupo `hefesto` e **nada toca o grupo `input`**.
Ela está no `input` **por fora do produto**. Numa máquina nova, não funciona. O
doctor não checa.

### F-9 — regras-cola empacotadas sem os scripts que elas chamam
As regras 82 e 83 viajam em todos os formatos e chamam alvos em
`/usr/local/lib/...` que **nenhum pacote instala** — ruído permanente no journal
de quem instalar por pacote. O próprio `uninstall.sh:652-660` já nomeia esse modo
de falha.

### F-10 — o portão de paridade, cego ao que mais regride
Não cobre: units/timers/scripts de Bluetooth, os drop-ins de WirePlumber, o
`hefesto-launch`, o `storm_watch.sh`, dependências de tempo de execução
(`bluez-tools`, `libopus0`), o **alvo** de uma regra-cola, e a assimetria inversa
(nada verifica que o `install.sh` **recria** o que o `uninstall.sh` levou).

### F-11 — dívidas menores, todas medidas
- borda de udev existe para o snapshot de bond e **não** para o rebind de órfão —
  o controle fica invisível por até 2 min esperando o timer;
- fuga de fd em `backend_pydualsense.py:1469-1479` quando o `init()` estoura;
- `bt-bonds.pre-uninstall-<carimbo>` é órfão de nascença: o uninstall cria, o
  install não recolhe, ninguém enxerga — e são credenciais;
- o drop-in 51 de áudio repete o defeito de `108b711`: install arma, uninstall
  desarma, e o **doctor lê a ausência como escolha dela**.

---

## 5. O que ENTROU nesta noite

| cura | onde |
|---|---|
| os dois tempos da janela separados (o clique marca, o Aplicar aplica) | `1c75a1a` |
| o AGORA deixa de ser refém do DEPOIS — quatro buracos | `10f013a` |
| o diálogo deixa de depender de qual aba está à vista | `JOGO-ABERTO-SO-NA-INICIO-01`, nesta leva |
| instrumento do 0x08 (`lightbar-reset`) e do isolamento de players (`player-leds`) | nesta leva |

**E o que os instrumentos mediram na mesa dela:**
- o 0x08 **fora** da janela de conexão **não trava** a barra — confirma o
  controle negativo que a sprint de 03/08 tinha e leu ao contrário;
- o 0x08 **apaga os LEDs de jogador**, e eles não voltam sozinhos;
- **a escrita do player-LED NÃO é quem derruba a barra** (hipótese dela,
  eliminada com variável única);
- um **restart do daemon** repinta as barras — o latch não é permanente.

---

## 6. Nota de método

Quatro agentes investigaram em paralelo, nenhum com permissão de editar. Três
mediram melhor do que eu, e um corrigiu a data de uma investigação anterior — o
que derrubou dois suspeitos de uma vez.

O erro de método mais caro da noite foi meu e é digno de registro: **eu contaminei
o experimento do 0x08 com o restart que era necessário para o instrumento
existir.** A barra voltou no restart, dois minutos antes do gesto que eu queria
medir. A lição virou desenho: o instrumento seguinte (`player-leds`) é
**comutável ao vivo**, justamente para não exigir restart.
