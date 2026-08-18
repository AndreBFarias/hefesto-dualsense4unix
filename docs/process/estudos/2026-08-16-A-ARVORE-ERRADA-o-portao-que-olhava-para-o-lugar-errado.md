# A árvore errada — a cura, e o vigia que já acordava na hora certa

**16/08/2026, madrugada.** Este documento é a **cura**. O diagnóstico está em
[A linha que a Steam come](2026-08-16-A-LINHA-QUE-A-STEAM-COME-o-censo-dos-campos-e-a-arvore-errada.md),
escrito na mesma noite por outra frente — que mediu as três árvores `apps`,
provou que as duas secundárias foram escritas por nós, e recomendou a **Ação A**:
ancorar o caminho no leitor e no escritor.

A Ação A foi executada. É isto aqui.

---

## O que mudou, em uma tabela

| | |
|---|---|
| **A âncora** | `e_a_arvore_canonica()` em `steam_launch_options` — um lugar só, usado pelo leitor **e** pelo escritor |
| **O efeito imediato** | `censo_do_wrapper()` passou de `faltantes: 0` para `SEM wrapper (regressao): PRAGMATA` |
| **A automação** | A reposição pegou carona no `hefesto-steam-input-guard`, que já acordava no instante certo |
| **A régua nova** | `prontuario_dos_jogos` — o cruzamento por jogo, que **recusa** dizer "funciona" |
| **Um irmão de brinde** | `pastas_steamapps()` devolvia a mesma pasta duas vezes |

---

## 1. Como a contradição apareceu — e por que o método importa

Dois relatos se cruzaram com dez minutos de diferença:

- um agente: *"MEDIDO 05h35: PRAGMATA segue sem o wrapper"*;
- eu, rodando o instrumento oficial: `censo_do_wrapper()` → `faltantes: 0`.

Não havia como os dois estarem certos, e *"o agente errou"* era a hipótese
confortável — eu tinha usado a ferramenta do próprio projeto. A regra da casa diz
o contrário: **o instrumento mente mais que o produto.** Escrevi um parser na
hora, que não compartilhava uma linha com o de produção, e ele mostrou as três
árvores.

O agente estava certo. **A discordância entre duas réguas independentes era o
achado**, e ela só apareceu porque a segunda régua não herdou nada da primeira.

No caminho eu errei duas vezes, e as duas foram baratas porque fui conferir o
contrato antes de acusar o código: chamei `parece_infraestrutura` achando que
filtrava jogos (filtra executáveis), e comparei o wrapper sem desescapar o VDF —
o que me fez ver "0 jogos com wrapper" onde havia 62.

## 2. A âncora

`e_a_arvore_canonica(pilha)` responde se o parser está em
`…/Software/Valve/Steam/apps/<appid>`. Por **sufixo**, não pelo caminho inteiro:
o que se exige é que `apps` esteja pendurado em `Software/Valve/Steam`, e o nome
da raiz (`UserLocalConfigStore` aqui) fica de fora do julgamento.

Um lugar só, usado pelos dois lados:

- **o leitor** (`read_apps_by_appid`) parou de fundir as três árvores num
  dicionário por appid — era essa fusão que fazia o wrapper da árvore morta
  encobrir a linha comida da árvore viva;
- **o escritor** (`apply_wrapper_vdf_text`) parou de sujar as árvores da Steam
  com um `LaunchOptions` que ninguém lê.

Efeito medido, imediatamente depois:

```
[sentinela-wrapper] jogos COM o wrapper: 62
[sentinela-wrapper] SEM wrapper (regressao): PRAGMATA (appid 3357650)  →  VKD3D_CONFIG=no_upload_hvv %command%
```

`regressao`, não `novo`: o registro sabia que aquele jogo já tivera o wrapper.

## 3. A automação — e a peça que já existia

Repor não bastava. **A Steam regrava o `localconfig.vdf` ao sair e engole
qualquer edição feita com ela viva.** Havia cura, havia gatilho na GUI, e mesmo
assim sobrava uma janela em que ninguém repunha nada: a janela em que ela está
jogando, que é o tempo todo.

O gatilho certo já existia e estava ligado nesta máquina:
`hefesto-steam-input-guard.path` vigia `~/.steam/steam/userdata` desde o
`FEAT-STEAM-INPUT-SELF-HEAL-01`, e acorda no instante em que a Steam grava o
vdf — que é o instante em que ela **acabou de sair**.

A sentinela do wrapper pegou carona no mesmo `.service`. Nada de unit novo, nada
de timer novo, **nada de botão** — o desenho é dela: *"nem precisa ter um botão
na gui, mas ele se auto corrigir"*.

Verificado ao vivo às 05h52, com a Steam aberta:

```
[steam-input]       Steam rodando — adiado (não vou fechar; reaplico quando a Steam sair)
[sentinela-wrapper] SEM wrapper (regressao): PRAGMATA (appid 3357650)
[sentinela-wrapper] reparo: adiado_steam_aberta
Finished hefesto-steam-input-guard.service
```

O `-` na frente do segundo `ExecStart` é deliberado: adiar sai com rc 3, e adiar
é o caso comum. Sem ele o guard entraria em `failed` toda vez que ela estivesse
jogando — e **um serviço cronicamente vermelho é um serviço que ninguém mais
lê.**

Isto é a contraparte feliz do defeito mais caro daqui ("a casa sabe e o produto
não faz"): desta vez a casa sabia acordar na hora certa, e passou a usar isso.

## 4. O censo que o cruzamento revelou

Com o leitor consertado, deu para cruzar pela primeira vez três leituras que já
existiam separadas — a linha de inicialização, a API de entrada do executável, e
o Steam Input por jogo. Os 24 jogos instalados dela:

| API de entrada | jogos | o que significa |
|---|---|---|
| `entende_dualsense` | 7 | SDL ou o plugin DualShock no binário — o vpad chega direto |
| `indeciso` | 15 | XInput e mais nada — o vpad **só chega por espelho** |
| `sem_evidencia` | 2 | nenhuma agulha, ou executável ilegível |

**Quinze dos vinte e quatro dependem de um espelho XInput do nosso vpad
`054c:0df2`.** Não é detalhe de um jogo: é a maioria da biblioteca dela, e muda
o peso de tudo que se decidir sobre Steam Input e sobre o `xinput1_4` do Wine.

Uma discrepância nova apareceu junto, no **Sackboy**: está na allowlist do Steam
Input com `UseSteamControllerConfig = 0`. A allowlist só **preserva** o que já
estava ligado — nunca liga. O gesto dela de pôr o jogo na lista não teve efeito.
Nomeado no prontuário como `excecao_inerte`, com a cura descrita; **a decisão é
dela**, porque daqui não dá para distinguir "a lista entrou tarde" de "eu
desliguei depois e mudei de ideia".

## 5. O que o prontuário recusa dizer

`prontuario_dos_jogos` responde por jogo, mas **nunca diz "funciona"**. O balde
bom se chama `sem_impedimento_conhecido` — frase mais longa e mais honesta.

A razão está medida: `Duskfade` e `DON'T SCREAM` têm a **mesma** assinatura no
disco — mesmo motor, mesmas famílias de API, mesmo wrapper, mesmo Steam Input
desligado. Um funciona e o outro não. Um prontuário que pintasse os dois de
verde estaria certo sobre um e errado sobre o outro, sem meio de saber qual.

Essa é a informação, não a falha do instrumento: **a causa do Duskfade não está
no disco.** Está no que acontece em tempo de execução, e é o que
`scripts/ensaios/quem_o_jogo_abre.py` mede — com os dois jogos abertos, lado a
lado. É bancada com ela.

## 6. O irmão de brinde

`pastas_steamapps()` devolvia a mesma pasta duas vezes: `~/.steam/steam` é um
link para `~/.steam/debian-installation`, e o `libraryfolders.vdf` lista o
segundo. A comparação era por texto de caminho.

Latente — os dois consumidores da época não erravam a conta por sorte de forma.
Mas o primeiro consumidor novo a iterar a lista foi um **censo**, e ele imprimiu
**65 jogos instalados** onde há 33 manifests. A armadilha esperava exatamente o
tipo de código cujo produto é um número.

Curado na fonte, não em cada consumidor: **quem chama não pode precisar saber
que a fonte repete.**

## 7. O que ficou aberto

1. **A causa do Duskfade.** Não é o wrapper, não é a engine, não é a falta de
   espelho, não é o Steam Input. O par com o DON'T SCREAM está pronto para rodar
   — precisa dos dois jogos abertos, é bancada com ela.
2. **O Sackboy na allowlist inerte** — decisão dela (§4).
3. **Limpar as 11 linhas** que escrevemos nas árvores secundárias. Inócuas (a
   Steam não as lê) e o `uninstall --strip` já as tira. Exige Steam fechada;
   não fiz com ela dormindo, para não mexer no vdf sem necessidade.
4. **Os portões que contam em vez de nomear**, achados pela outra frente e ainda
   não consertados — o `hidden_count` do broker é o mais grave. Estão em
   [O que a Steam come em silêncio](2026-08-16-O-QUE-A-STEAM-COME-EM-SILENCIO-o-censo-dos-campos-de-uma-linha-so.md).

## O que mudou no código

| arquivo | o quê |
|---|---|
| `integrations/steam_launch_options.py` | `e_a_arvore_canonica` — a âncora nos dois lados; e a deduplicação de `pastas_steamapps` |
| `integrations/prontuario_dos_jogos.py` | novo — o cruzamento por jogo, que recusa dizer "funciona" |
| `assets/hefesto-steam-input-guard.service` | o segundo `ExecStart`: a sentinela na carona do gatilho que já existia |
| `install.sh` | renderiza `__SENTINELA__`; sem flag, como manda a casa |
| `tests/unit/test_arvore_errada_01_*.py` | 18 testes — a âncora nos dois lados, o caso do Pragmata do vdf real |
| `tests/unit/test_biblioteca_dobrada_01_*.py` | 9 testes — a pasta que saía repetida |
| `tests/unit/test_carona_no_guard_01_*.py` | 10 testes — o `ExecStart` que não pode sumir |
| `tests/unit/test_prontuario_01_*.py` | 28 testes — inclusive o que trava que Duskfade e DON'T SCREAM saem iguais |

Cada um dos quatro arquivos de teste foi arrancado, visto reprovar, e devolvido.
