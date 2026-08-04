# A noite em que o som do controle voltou

- **Quando:** 03→04/08/2026, madrugada, com ela ao vivo
- **Como começou:** *"não funciona nem mic, nem os botões de sons do jogo em
  nenhum dualsense"*
- **Como ela achou a causa, antes de mim:** *"a causa é o sistema de microfone e
  audio. desfizemos algo nos nossos testes (...) desarmamos algo que não
  esquecemos de armar corretamente"*

Ela estava certa, e eu estava medindo a coisa errada — cheguei a afirmar que o
cabo no mesmo barramento USB do dongle Bluetooth destruía o rádio. **A minha
própria medição refutou isso** meia hora depois, e está registrada aqui porque
o erro tem valor: a janela 23:20→23:49 tinha o cabo dentro e **zero** frames
corrompidos. Hipótese que não explica o que JÁ funcionava é hipótese morta.

---

## O que estava quebrado, em três camadas empilhadas

### Camada 0 — a cura que não estava lá

O arquivo `51-hefesto-dualsense-no-default-source.conf` **não existia** na
máquina dela. O `doctor.sh --fix` o criou às 00:37 de 04/08 — carimbo de
madrugada, não de instalação.

Sem ele, o WirePlumber promoveu o DualSense a **microfone padrão do sistema**.
A partir daí tudo o mais é consequência: a nossa própria janela abre um `parec`
ao vivo na captura do controle enquanto a aba Status está visível (é o medidor
de nível, e ele está certo em existir), e o sistema inteiro passou a tratar o
controle como o microfone da casa.

**A assimetria que permite isso está no repositório e é nomeável:**

| quem | o que faz com o drop-in 51 |
|---|---|
| `install.sh`, passo 10 | **arma** (default; opt-out `--keep-dualsense-mic`) |
| `uninstall.sh:125` | **desarma** |
| `scripts/doctor.sh:536` | lê a **ausência** como *"ela promoveu o mic de propósito"* |

Ou seja: a máquina curada e a máquina desarmada são **o mesmo estado** para o
portão. É a mesma cegueira que o `check_bt_sdp_cache_envenenado` já teve — dar
`[OK]` no meio do defeito, e na proporção da gravidade. Fica aberta na
`DROPIN-AMBIGUO-01`.

### Camada 1 — o PipeWire mudo, dos dois lados

Duas coisas mudas ao mesmo tempo, pelo **mesmo mecanismo** e por caminhos
diferentes:

- **a captura**: microfone mudo por estado que o WirePlumber persiste por rota
  em `~/.local/state/wireplumber/default-routes`, restaurado a cada conexão
  **sem escrever nada em log nenhum**. O `doctor.sh` já conhecia esta — é a
  "camada 1" do microfone mudo — e a curou;
- **a saída**: o sink do DualSense estava `MUTED`, e era o sink **padrão do
  sistema**:

      *   45. DualSense wireless controller (PS5) Surround analógico 4.0
              [vol: 1.00 MUTED]

O produto **tinha a doutrina escrita**, no próprio card, e não agia sobre ela:

> *"A camada 1 vence a camada 2: volume e rota perfeitos num sink mudo é
> trabalho invisível."*

E tinha a recusa honesta — o `MOTIVO_SAIDA_MUDA` do tocador. Mas ela só dispara
quando o mute foi **lido com certeza**, e o mapa de mudos do `mic_monitor` só
guarda o que casou com certeza: ausência é "não sei". **E "não sei" seguia para
o tocador**, que gastava um processo para produzir silêncio e devolvia sucesso.

### Camada 2 — o botão que silenciava o alto-falante

`speaker_set(rota=rota)`, sem `volume` e sem `uniq`. Os dois faltavam por
motivos diferentes, e cada um sozinho já era um defeito:

1. **sem volume** o daemon faz `pref = None -> pref = 0`, escreve **zero** nos
   dois registradores e **toma a posse** — de modo que nem o firmware o
   recupera. A regra já estava escrita na `SOM-02` ("Armadilha 1"), o
   `profiles/schema.py` chega a RECUSAR perfil sem volume pela mesma razão, e
   os três irmãos deste mesmo widget a respeitam. Só este chamador escapava;
2. **sem uniq** o daemon cai no controle PRIMÁRIO — com dois cards na tela,
   clicar no card do Controle 2 escrevia no Controle 1.

---

## As curas aplicadas

| defeito | cura | onde |
|---|---|---|
| o seletor de canal silenciava o alto-falante | manda `volume` e `uniq` | `app/widgets/controller_card.py` |
| "não me disseram" virava "me disseram zero" | herda o valor em vigor no handle | `core/backend_pydualsense.py` |
| pedir som num sink mudo produzia silêncio calado | `garantir_saida_audivel()` nos DOIS canais e na troca de sink | `app/audio_saida.py` |
| a instalação podia terminar com cura desarmada | o `doctor.sh` roda no fim, por padrão | `install.sh` (opt-out `--no-doctor`) |

### A prova ao vivo

A cura foi verificada com ela na hora, e o desenho do teste importa: **o sink do
controle foi deixado MUDO de propósito** antes de reiniciar a janela. Ela clicou
no seletor, e:

- o som voltou — *"voltou a funcionar no controle com cabo"*;
- **os dois botões** do seletor, e **o microfone junto**, na palavra dela;
- o `MUTED` **sumiu do sink** sem ninguém tocar no `pactl`.

O segundo ponto é o que fecha a prova: não bastava o som sair (podia ser o
firmware). Foi a **camada 1 que mudou de estado no clique dela**, que é
exatamente o que a cura faz e nada mais no sistema faria naquele instante.

Falta a mesma medição **no rádio** (item E2 do protocolo) — a previsão da casa
é que não sai, porque a ponte de saída de áudio por Bluetooth não está
implementada. Se sair, a previsão está errada e é achado grande.

A conferência final do install nasceu de um pedido dela, literal:

> *"nosso install não deveria rodar o doctor por default sem flag? pra garantir
> tudo tudo real mesmo?"*

Ele **confere** e não cura, de propósito: os passos acima já são as curas. Se
esta conferência precisasse consertar algo, o defeito seria do passo — e
escondê-lo com um `--fix` no fim apagaria justamente o sinal que aponta para o
passo furado.

---

## O daemon que não morria

Achado no journal dela, no meio de outra coisa:

    00:20:19.601  gamepad_emulation_stopped     <- último suspiro
    (silêncio de 90 s)
    00:21:49      State 'stop-sigterm' timed out. Killing.

O `daemon_stopped` — a última linha do `shutdown()` — nunca saiu. A cadeia,
conferida no upstream e no nosso:

    device.read(...)          BLOQUEIA num fd que não entrega mais nada
      report_thread.join()    upstream (pydualsense), SEM TETO
        handle.close()
          disconnect()        SEGURANDO o `_io_lock`
            shutdown()
              systemd: 90 s e SIGKILL

O gatilho foi o 8BitDo se desligando sozinho. Custo real: 90 segundos em que o
serviço não volta, os vpads não renascem e a mesa fica **sem controle nenhum**.

A cura fecha o fd **mesmo assim** — é fechar o fd que faz o `read` pendurado
retornar erro, e o laço já tratava `OSError` como fim de vida. É a mesma
doutrina que o `HANG-01` já escrevera por extenso nos dois executores do
`shutdown`: *"uma thread wedged não impede o processo de encerrar"*. Faltava
valer para o handle.

**O teste morde de um jeito incomum e vale registrar:** com a cura arrancada
ele não reprova — ele **não termina**. `rc=124` em 40 s de `timeout`, que é o
defeito dela reproduzido em bancada.

---

## O que eu errei, e o que isso ensina

1. **Afirmei que o cabo destruía o rádio.** A topologia era sedutora (dongle de
   12 Mbit/s atrás do mesmo hub de um DualSense com dois endpoints isócronos) e
   a correlação temporal era boa. A janela de controle a matou. *Toda hipótese
   tem de explicar o que JÁ funcionava.*
2. **Contei o tempo com `journalctl --since "23:20"`**, sem data — o systemd leu
   "23:20 de hoje", que era futuro, e devolveu zero em todas as janelas. Zero em
   TODAS as janelas era o sinal de que o instrumento estava quebrado, não de que
   não havia defeito.
3. **Ela achou a causa antes de mim, e por um caminho que eu não tinha.** Ela
   sabia o que *nós* tínhamos mexido; eu só via o que a máquina mostrava.

---

## Relacionado

- [DROPIN-AMBIGUO-01](../sprints/2026-08-04-DROPIN-AMBIGUO-01-a-ausencia-do-drop-in-e-indistinguivel-de-escolha.md)
- [SUITE-QUE-SUJA-O-JORNAL-01](../sprints/2026-08-04-SUITE-QUE-SUJA-O-JORNAL-01-os-testes-escrevem-no-journal-do-sistema.md)
- [IDENTIDADE-DUPLA-01](../sprints/2026-08-04-IDENTIDADE-DUPLA-01-o-8bitdo-ocupa-dois-lugares-na-fila.md)
- [A noite em que medimos a lightbar do Bluetooth](2026-08-03-a-noite-em-que-medimos-a-lightbar-do-bluetooth.md)
- [A noite em que o microfone do Bluetooth voltou](2026-08-03-a-noite-em-que-o-microfone-do-bluetooth-voltou.md)
