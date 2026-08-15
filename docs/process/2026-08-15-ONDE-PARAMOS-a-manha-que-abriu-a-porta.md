# ONDE PARAMOS — a manhã que abriu a porta

**Escrito em 15/08/2026, de manhã, enquanto ela dormia.** Substitui o
`2026-08-11-ONDE-PARAMOS` como porta de entrada. Aquele continua válido para o
que mediu; só deixou de ser o retrato de hoje.

Leia esta página primeiro. Ela cabe em cinco minutos.

---

## 1. O que você precisa saber em três frases

1. **A porta abriu.** Os instrumentos não conseguiam mais medir os controles,
   porque o próprio Hefesto os esconde — e agora eles pedem ao broker. O censo
   do `0x20` saía *"0 de 4 controles legíveis"*; agora dá **4 de 4**.
2. **A mesa virou régua.** Com a porta aberta, os quatro controles responderam
   **dezoito células** que estavam mudas no mapa, e derrubaram duas suspeitas
   antigas.
3. **Um defeito novo foi achado, medido e consertado** — um jogador em quatro
   recebia input praticamente parado, e ninguém sabia.

---

## 2. A mesa ainda está de pé

Dois no cabo, dois no rádio, quatro vpads. **Nada foi reiniciado, nada foi
escrito em aparelho nenhum.** Se você ainda quiser rodar o que precisa de você,
ela está lá.

**Mas dois bonds estão faltando.** O `bluetoothd` travou às 06:29 e apagou três
dos quatro pareamentos segundos antes de abortar (é corrupção de heap no bluez
5.86, com o backport já aplicado — ele não curou). O acervo tem o retrato bom
das 06:29:01, e o restauro automático já está escrito. Ele **recusou** rodar
comigo, e estava certo: escrever com o `bluetoothd` vivo é como o estrago
acontece.

---

## 3. As três coisas que só você pode fazer

### 3.1. Decidir (20 minutos, e destrava quinze frentes)

[`2026-08-15-AS-DECISOES-QUE-ESPERAM-VOCE.md`](2026-08-15-AS-DECISOES-QUE-ESPERAM-VOCE.md)

Vinte e seis decisões numa página só, ordenadas por consequência, cada uma com
o que muda **na tela**, o custo em horas e uma recomendação. Quinze travam
código.

Comece pela **D-30** (a ordem dos jogadores). Ela tem o tratamento maior porque
o achado muda a pergunta: R-15 e R-23 curaram *"o número muda sozinho"*, e você
pede *"o número segue a ordem que eu escolhi"* — as duas coisas só se encontram
no replug. Você já respondeu essa pergunta duas vezes; faltava o preço.

Quatro decisões estavam **já decididas e ninguém marcou**. Quatro perguntas
estão **mal feitas**, e a recomendação é derrubá-las em vez de respondê-las.

### 3.2. Liberar a mesa, quando não precisar mais dela

Três coisas esperam por isso, e **nenhuma pode ser feita com a mesa de pé**:

```bash
# 1. O espelho do P4 — a cura está no código, mas o daemon vivo é mais velho
systemctl --user restart hefesto-dualsense4unix.service

# 2. O restauro de bonds — arma o gatilho (NÃO reinicia o bluetoothd)
./install.sh --yes

# 3. A prova de ponta a ponta do restauro está escrita na sprint
#    2026-08-15-BONDS-QUE-SOBREVIVEM-01 (imita o crash e confere a volta)
```

### 3.3. Olhar a tela

A documentação de uso levou treze correções hoje, contra os retratos de 15/08.
Nenhuma foto nova foi tirada. **A palavra final continua sendo sua.**

---

## 4. O que mudou, por commit

| commit | o que resolve |
|---|---|
| `fix(instrumentos)` | a porta do broker; instrumentos deixam de medir no nó escondido |
| `fix(bonds)` | a causa real do sumiço, e o gatilho da volta |
| `fix(ci)` | o censo tinha folga demais **e** um erro vermelho que ninguém via |
| `test(mapa)` | dezessete afirmações sem rede viraram zero |
| `docs(interface)` | treze derivas entre a tela e o documento |
| `docs(decisões)` | as vinte e seis, e dois fatos falsos substituídos |
| `docs(mesa)` | o plano do que só se mede com quatro |
| `feat(ensaios)` | três instrumentos novos, e o que a mesa respondeu |
| `docs(mapa)` | dezoito células mudas viraram resposta |
| `fix(co-op)` | o espelho que não nascia para quem perdia a corrida |

---

## 5. O que a mesa respondeu, e o que ela derrubou

**Duas suspeitas caíram por medição:**

- **O barramento está inocentado.** O adaptador de rádio e os dois do cabo
  dividem o mesmo controlador xHCI nesta máquina — a pré-condição física da
  suspeita de 10/08 existe. Mas com carga em três patamares, escada percorrida
  subindo e descendo, em duas execuções, a variação é **menor que a dispersão
  natural do rádio**. O próximo suspeito é o laço de escrita.
- **O CRC de entrada por rádio não falha.** Trinta e cinco mil trezentos e
  cinquenta e um quadros, zero falhas. A suspeita escrita no backend cai para a
  entrada; segue aberta para a saída.

**Um fato errado saiu do mapa:** o giroscópio por rádio não faz 1000 Hz. Esse
número é **declaração do SDL, nunca entrega**. A faixa medida hoje é 173–403 Hz.
Ficou escrito de onde vinha o 1000, para ninguém reintroduzir.

**E o que o mapa NÃO pode afirmar** está escrito junto: os ensaios de hoje estão
**confundidos** para "rádio contra cabo", porque são dois aparelhos por braço e
nenhum trocou de lado — os dois do rádio diferem por quase o dobro na mesma
janela. Só a troca de braços separa transporte de unidade, e ela derruba a mesa.

---

## 6. Quatro armadilhas novas, todas pagas hoje

Nenhuma é hipótese: as quatro produziram, ou quase produziram, um resultado
convincente e falso nesta sessão.

1. **O LED mente sobre quem é quem.** O vpad faminto foi atribuído ao controle
   do cabo pela cor; era o do **rádio**. Duas fontes independentes derrubaram a
   atribuição. O campo `player` do rumble é a **fila de chegada**, não o slot do
   vpad — quem casa os dois lados é o MAC.
2. **A régua altera o que mede.** A taxa do vpad faminto subiu de 0,4 para 26 Hz
   às 07:25 sozinha — foi o **nosso próprio instrumento** pedindo o nó ao
   broker, o que manteve o enlace de rádio quente.
3. **O `null` do ALSA não é fonte muda.** Devolve memória não inicializada, e
   teria "provado" captação a partir de lixo. O negativo real é o monitor de um
   sink suspenso.
4. **O `MIC_DETECT` é do jack de 3,5 mm**, não do microfone embutido. Os dois do
   cabo saem com o bit limpo e captam mesmo assim; lê-lo como presença dá a
   conclusão oposta à medição.

---

## 7. O que fica aberto

- **O fd vazado.** O `pydualsense_init_timeout` das 06:29:45 deixou um
  `/dev/hidraw8 (deleted)` aberto no daemon. Some no próximo start; a causa não
  foi investigada.
- **A máscara por jogador** ([sprint
  própria](sprints/2026-08-15-MASCARA-POR-JOGADOR-01-a-decisao-de-14-08-esbarra-na-de-10-08.md)):
  sua decisão de 14/08 esbarra na de 10/08, que está escrita no schema. É
  decisão sua, não execução minha.
- **As 153 células mudas do Pro e do 8BitDo.** Nenhuma hora de ensaio nesta mesa
  as alcança — eles não estão nela.
- **O laço de escrita**, agora que o barramento foi inocentado.
- **A coluna `estado_hoje`** do caderno de bancada: fechar o vocabulário dela é
  decisão sua.

---

## 8. Uma nota sobre o que eu não fiz

Não reiniciei nada, não empurrei nada para o `origin`, e não decidi nenhuma das
vinte e seis. Liberdade para executar não é licença para reverter uma medição
sua sem você ver — e três das decisões abertas fazem exatamente isso.
