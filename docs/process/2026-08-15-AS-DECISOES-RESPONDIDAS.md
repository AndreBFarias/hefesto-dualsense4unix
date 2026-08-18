# AS DECISÕES — RESPONDIDAS

**Respondidas por ela em 15/08/2026**, no chat, uma a uma, com o preço na mesa.
Esta página é a **fonte de verdade**: onde qualquer sprint discordar dela, é a
sprint que está velha.

A página das perguntas
([AS-DECISOES-QUE-ESPERAM-VOCE](2026-08-15-AS-DECISOES-QUE-ESPERAM-VOCE.md))
fica como está, para quem quiser o contexto e o preço de cada caminho.

**Ela respondeu 26 e derrubou duas perguntas** — a D-13, porque estava mal feita,
e a V-B, porque o risco não existia.

---

## O que muda de imediato

| decisão | resposta dela |
|---|---|
| **D-30** — ordem do jogador | **(b) ordem do momento, CONGELADA quando a mesa estabiliza.** Quem cai e volta recupera o número. O gravado não some: vira desempate |
| **D-19** — navegar × comandar | **duas coisas.** Os quatro navegam a janela ao mesmo tempo. Derruba a rota cara |
| **D-31** — bateria da escada | **a série inteira, com ela presente** |
| **máscara do gamepad** | **por jogador.** A frase de 10/08 passa a valer só para o `mode` |
| **D-15** — a cor física | **a cor do PLÁSTICO**, lida do aparelho, **por cabo E por rádio** |
| **D-16** — onde a cor mora | **da PEÇA, porque a cor mora no APARELHO.** Sem arquivo por endereço |
| **D-18 / D-17** | **anel por dentro** para a seleção, borda = identidade; e os botões 1-2-3-4 com **a cor de quem ocupa** |
| **D-25** — alto-falante por rádio | **nasce ligado**, orçamento de rádio medido antes de soltar, **e** interruptor por controle para quem quiser desligar |
| **D-25** (fone) | **o Hefesto segue o jack sozinho** |
| **D-26** — SFX | **o alto-falante por rádio primeiro** |
| **D-32** — família `0xF0`-`0xF7` | **ler a família inteira, só leitura. Nunca escrever** |
| **D-23** — tabela por controle | **manter fechado.** Um mapeamento de navegação para todos |
| **D-22** — o X vaza para o jogo | **roubado, só os quatro botões, só do dono da navegação** |
| **D-20** — o R1 | **dois significados, decididos pelo foco** |
| **D-21** — círculo e carrossel | **círculo volta à tira de abas; R1 vai para a aba da direita, L1 para a esquerda, em CARROSSEL** (dá a volta) |
| **D-13** — as duas colunas do mapa | **pergunta derrubada.** O problema são os nomes, não a quantidade — ver abaixo |
| **D-14** — rebaixar células | **rebaixar as que sobraram** |
| **D-29** — grab do primário falhando | **abrir frente própria.** É defeito ao vivo |
| **D-27** — amostra da cor | **procurar uma quinta unidade** antes de fechar a afirmação |
| **D-28** — acelerômetro | **em todo lugar** — ver abaixo |
| **D-33** — o nome | **aprovado: FALÁCIA DO CANAL QUE RESPONDE** |
| **V-A** — quando vira `1.0.0` | **critério novo, dela** — ver abaixo |
| **V-B** — a arte dos SVG | **não é mais problema** — ver abaixo |

---

## As quatro que precisam de mais que uma linha

### D-13 — ela derrubou a pergunta, e estava certa

> *"tá ruim mesmo, vamos diferenciar os nomes das colunas melhores? minha
> recomendação ficou ruim, aceito sua escolha"*

O problema nunca foi **uma coluna ou duas**. É que `confianca` e `grau` são nomes
que não dizem o que medem, e por isso se confundem. Renomear resolve o que
fundir resolveria, sem encolher o mapa.

| coluna | nome novo | o que ela responde | domínio |
|---|---|---|---|
| `confianca` | **`de_onde_sei`** | de onde vem a informação | `medido` · `inferido-do-codigo` · `afirmado-no-doc` · `incerto` |
| `grau` | **`ate_onde_foi`** | até onde a prova chegou | `MONTOU` · `SAIU NO FIO` · `O APARELHO OBEDECEU` |

Duas perguntas diferentes, impossíveis de confundir. A escolha do nome foi
delegada a mim; se ela não gostar, é um `sed` e um portão.

### D-28 — o acelerômetro vai a TODO lugar, não só ao diagnóstico

> *"no diagnóstico, na aba, no jogo seja via vpad ou via controle físico. temos
> que garantir até que funcione com steam ligada"*

Ela **expandiu** a pergunta, que oferecia um lugar só. São quatro exigências:

1. no **diagnóstico** (onde as medições moram);
2. na **aba** (visível a quem está jogando);
3. **chegando ao jogo pelo vpad**;
4. **e pelo controle físico** — os dois caminhos.

E a quinta, que é a mais dura: **tem de funcionar com a Steam ligada.** O Steam
Input faz um espelho Xbox de cada controle que vê, inclusive do nosso vpad, e o
Xbox não tem acelerômetro. Isto não é detalhe de layout — é a única exigência
desta lista que pode não ter solução, e ela precisa ser medida antes de
prometida.

### V-A — o critério de release, que não existia antes

> *"vira 0.9.5 quando mapearmos tudo, construirmos todos os canais e concluirmos
> todas as sprints em aberto. após isso vamos ir jogando e ajustando os
> probleminhas de layout que surgirem. com duas semanas sem novas sprints
> teremos a versão 1.0. até lá vamos lançando 0.9.x.x"*

| marco | o que exige |
|---|---|
| **`0.9.x.x`** | lançamentos contínuos no caminho |
| **`0.9.5`** | mapa completo **+** todos os canais construídos **+** nenhuma sprint aberta |
| **`1.0.0`** | **duas semanas sem sprint nova**, depois de jogar e ajustar layout |

O critério antigo (*"ver funcionando num PC novo"*) não foi contrariado — foi
**substituído por um que a casa sabe medir**. "Nenhuma sprint aberta" e "duas
semanas sem sprint nova" são contáveis; "PC novo" não era.

### V-B — o risco de licença não existe

> *"Os controles atuais fomos nós quem criamos (o claude mesmo), e eu alterei via
> Boxy SVG, pode deixar como tá. isso não é mais problema."*

A arte foi criada aqui e editada por ela no Boxy SVG. **Não há obra de terceiro
envolvida**, e portanto não há risco de licença. A recomendação de redesenhar os
três do zero **caduca**, e a distribuição pública deixa de estar travada por
este item.

---

## As três perguntas que morreram por medição, não por escolha

Não são decisões dela, e ficam registradas para ninguém as reabrir:

1. **A D-24 inteira** — perguntava se ela autoriza uma classe de escrita **que
   ela já autorizou e que já foi exercida** em 15/08. O que restava virou a
   D-31, respondida.
2. **O item 2 da D-27** (*"posso sondar `0x80`-`0x83`?"*) — os quatro já foram
   sondados no censo dos dezessete. A pergunta que importava era sobre a
   escrita, e é a D-15.
3. **O item 2 da D-29** (*"o hidraw `0600` é de propósito ou é portão caído?"*) —
   medido: **é de propósito**, é o próprio Hefesto que esconde o nó. O que sobra
   é apagar uma linha `0660` de regra udev, resto de uma era anterior.

---

## O que ela decidiu contra a minha recomendação

Registrado porque a recomendação errada é dado, e porque a próxima sessão
precisa saber que estas foram escolhas conscientes:

| decisão | eu recomendei | ela escolheu |
|---|---|---|
| **D-15** | (a) escolher na interface, sem escrita | **ler do aparelho, cabo e rádio** |
| **D-23** | reabrir a tabela de navegação | **manter fechado** |
| **D-26** | o fone primeiro | **o alto-falante por rádio primeiro** |
| **D-21** | R1 para na última aba | **carrossel, dá a volta** — e ela acrescentou o L1 |
| **D-27** | fechar a amostra em quatro | **procurar uma quinta** |
| **D-28** | só no diagnóstico | **em todo lugar, inclusive com a Steam ligada** |
