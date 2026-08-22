# CONFIG-09 — "Está tudo certo?"

**Depende de:** CONFIG-02.

> Nasceu de um pedido durante a revisão do mockup: *"seria maneiro rodar um scan
> tipo o doctor mas pra saúde das portas usb e do bt. ficando verde com um check
> pra dizer que o app funciona como deveria."*

## Por que esta é, talvez, a sprint mais valiosa da leva

O `scripts/doctor.sh` tem **4920 linhas** e **26 funções** dedicadas a energia
USB, autosuspend, BlueZ, pareamento, CRC de rádio e estado do DKMS. É um dos
ativos mais fortes do projeto.

E é **invisível para quem não abre terminal** — ou seja, para a maior parte de
quem usa o produto.

Esta sprint não constrói diagnóstico novo. Ela dá cara de gente ao que já existe:
um selo verde com um check dizendo *"Pronto para jogar"*, e seis linhas abaixo
dizendo o que foi conferido.

## O que aparece

```
✓ Pronto para jogar        [ Examinar de novo ]        Há 2 minutos

✓ Firmware dos adaptadores      ✓ Economia de energia desligada
✓ Energia das portas            ✓ Pareamentos salvos
✓ Suporte ao controle           ! Vizinhança das portas
```

Três estados, e a semântica de cor do projeto manda em cada um:

| Estado | Cor | Quando |
|---|---|---|
| Certo | Verde `@green` | Nada a fazer |
| Atenção | **Amarelo** `@yellow` | Funciona, mas dá para melhorar — e é reversível |
| Problema | Vermelho `@red` | Algo está quebrado agora |

**Vizinhança de porta ruim é amarelo, nunca vermelho.** A regra do projeto é
explícita: *"pintar de vermelho ensinaria ela a ver problema onde não há"*.
Vermelho é para o que destrói e não tem volta.

## A decisão de arquitetura

O reconhecimento deixou a pergunta em aberto — a aba é superfície gráfica do
doctor, ou um segundo diagnóstico independente? O projeto responde sozinho, em
`ipc_handlers.py:2605-2612`:

> *"Duas descrições do mesmo fato se afastam na primeira mudança."*

**Portanto: fonte única.** A aba não reimplementa nenhuma checagem. Duas saídas
possíveis, e a escolha é de custo, não de princípio:

1. **`doctor.sh --json`** — modo novo de saída no script que já existe. O custo é
   real: os testes fazem *grep de texto* na saída dele (`test_plataforma_wiring.py:216`
   assere que a string `RSSI` aparece), então mexer exige cuidado.
2. **Extrair as checagens para um módulo Python** que o doctor e a aba consomem.
   Mais limpo, mais caro, e mexe em 4920 linhas.

**Recomendo a 1**: `--json` é aditivo, não altera a saída de texto existente, e
os testes continuam passando.

## Não pode

- **Rodar sozinho a cada tique.** O exame é caro. Roda ao abrir a aba e no botão.
- **Pedir senha.** A GUI é sudo-zero por doutrina. Checagem que precisa de root
  aparece como *"não deu para conferir"*, jamais como falha.
- **Consertar nada por conta própria.** Diz o que achou e o que fazer. Quem age
  é a pessoa.

## Prova de trabalho

```bash
scripts/doctor.sh --json | python3 -m json.tool | head -40
pytest tests/unit/test_plataforma_wiring.py -q
```

**Aceite:** numa máquina saudável, selo verde. Desligando o adaptador Bluetooth,
a linha do firmware fica vermelha e o selo do topo acompanha. Com um Wi-Fi USB
na porta vizinha, a vizinhança fica amarela e o selo continua verde — porque
amarelo não impede de jogar.
