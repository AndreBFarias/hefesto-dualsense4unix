# As onze respostas dela — 07/08/2026

Registro das decisões tomadas sobre o
[painel das nove](2026-08-07-PAINEL-as-nove-decisoes-que-esperam-ela.md).

**Isto não é proposta.** É a palavra dela, e vale como a doutrina da casa: não se
repropõe, e quem quiser mudar precisa de uma medição que derrube o motivo — não
de uma opinião melhor.

**Grau: DECISÃO DELA** em todas. Onde ela escolheu a opção recomendada, a
recomendação está registrada junto, para que ninguém confunda concordância com
delegação.

---

## O que ela decidiu

| # | pergunta | resposta |
|---|---|---|
| 1 | onde mora a caixinha que TIRA um jogo do Steam Input | **no editor do perfil, logo abaixo do jogo escolhido** |
| 2 | qual licença o Hefesto tem | **MIT no código, CC0 nas curvas** |
| 3 | os externos ganham lugar próprio na partida | **só depois da máscara por controle** |
| 4 | o bloco ESCOPO fica no `LICENSE` | **sai; o `NOTICE` vira dono da ressalva** |
| 5 | o nome do modo comprido da aba Gatilhos | **"Montar do zero"** |
| 6 | os nomes "Arco" e "Arma" | **"Arco de flecha (Bow)" e "Disparo (Weapon)"** |
| 7 | onde mora o interruptor do mic por Bluetooth | **no card do controle, junto do medidor** |
| 8 | a fonte +3 está aceita | **sim, aceita** |
| 9 | qual lista come a próxima sessão de hardware | **o protocolo de 06/08 primeiro** |
| 10 | a janela fala inglês | **não — português é a língua do produto** |
| 11 | até onde executar sem ela na cadeira | **tudo, inclusive a tela** |

---

## As três que mudam o plano, e por quê

### A resposta 3 reordena uma leva inteira

Ela **não** autorizou as entregas `E3`/`E4` do
[LUGAR-A-MESA-01](sprints/2026-08-06-LUGAR-A-MESA-01-tres-controles-ligados-e-um-jogador-so.md)
agora: autorizou **depois da máscara por controle**.

Isso promove a `MASCARA-01` de sprint paralela a **pré-requisito**, e o motivo é
o que ela recusou a pagar: quem segurasse o Pro Controller veria botão de
PlayStation na tela do jogo, com A/B e X/Y trocados no plástico.

Consequência para quem for executar: **não comece a adoção dos externos.**
Comece pela máscara. A ordem virou `MASCARA-01` → `E3` → `E4`.

E o veto de 19/07 (*"externo não ganha controle virtual"*) **não foi derrubado —
foi adiado com condição**. Enquanto a máscara não existir, ele vale.

### A resposta 4 tem um efeito que só aparece fora da máquina

O bloco `ESCOPO` sai do `LICENSE` porque é ele que faz o GitHub exibir *"View
license"* em vez de *"MIT"* na vitrine do repositório. A ressalva **não some**:
o `NOTICE` já tem a seção "ESCOPO DESTE ARQUIVO", com a auditoria arquivo por
arquivo, e passa a ser o dono dela.

Quem for executar: o `LICENSE` fica com o texto MIT **canônico e sem nada
antes** — é a forma canônica que o detector de licença do GitHub reconhece.

### A resposta 10 fecha uma promessa que estava falsa

Três páginas do projeto (`CONTRIBUTING`, `flatpak.md`, `troubleshooting.md`)
convidam a traduzir, e a tradução não alcançaria quase nada: 15 dos 18 arquivos
que montam as abas escrevem português direto no widget.

Ela escolheu **assumir o que o produto já é**. O convite sai das três páginas, e
entra um portão que impede o convite de voltar sem o encanamento junto.

O encanamento de i18n **não é removido** — ele está correto, e removê-lo seria
destruir trabalho bom para provar um ponto.

---

## O que a resposta 11 autoriza, e o que ela não autoriza

Ela autorizou executar **tudo, inclusive a tela**. Isso não revoga a
[PROVA-DE-TELA-01](sprints/2026-07-27-PROVA-DE-TELA-01-dez-minutos-de-olho-antes-de-qualquer-leva.md):
a regra da casa continua sendo *foto antes e depois, e a palavra final é dela*.

O que muda é **quando** ela olha: em vez de esperar a autorização para começar,
o trabalho de interface é feito e **apresentado com as fotos**, para ela aprovar
ou mandar refazer. A palavra final continua dela.

**Grau: DECISÃO DELA**, explícita, em 07/08/2026.

---

## O que NÃO foi perguntado, e por quê

Cem candidatas viraram nove perguntas. As 91 restantes foram derrubadas por
verificação adversarial — na maioria, porque **ela já tinha respondido** e a
resposta estava no repositório ou numa fala registrada.

A lista das derrubadas, com o `grep` que provou cada uma, está em
[docs/process/agentes/2026-08-06/decisoes/](agentes/2026-08-06/decisoes/).
Quem quiser reabrir uma delas: leia o motivo antes, porque quase sempre a
pergunta já tem dona.
