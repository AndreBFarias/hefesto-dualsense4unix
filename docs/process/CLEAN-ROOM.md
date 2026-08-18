# Processo de sala limpa — efeitos de gatilho próprios

**Vigente desde 2026-07-25.** Este documento é normativo: enquanto ele estiver
aqui, as regras abaixo valem para qualquer pessoa que trabalhe nos efeitos de
gatilho do Hefesto.

## Por que este processo existe

O Hefesto precisa de efeitos de gatilho com nome — a conveniência de escolher
"pesado" em vez de calibrar sete parâmetros. O DSX resolve isso com doze modos
prontos, cujas curvas de força estão publicadas em um repositório **sem
licença** (ver a seção correspondente no `NOTICE`). Copiá-las é ilícito;
copiá-las e disfarçar é pior, porque cria obra derivada **e** aparência de
ocultação.

A saída é criar efeitos próprios. Mas "criar do zero" só protege o projeto se
for possível **demonstrar** que foi do zero. Este documento é o que torna a
demonstração possível.

> **A assimetria que justifica tudo isto:** sem registro, quem não copiou tem
> de provar uma negativa — impossível. Com registro datado de como cada valor
> nasceu, o ônus se inverte: a origem independente está documentada, e cabe a
> quem alega o contrário mostrar a semelhança.

## As quatro regras

### R1 — Separação de acesso

Quem **implementa** valores de curva não consulta implementação de terceiros
durante o trabalho. Pesquisar o protocolo (formato do report, semântica dos
campos) é livre e necessário; ler tabelas de curva alheias, não.

Se você já viu aquelas tabelas antes, deixe o assunto descansar e trabalhe a
partir da **sensação no controle**, nunca da lembrança do arquivo. O ponto de
partida legítimo é o hardware na sua mão.

### R2 — Nomes próprios

Efeitos nossos usam vocabulário nosso, em português: `Pesado`, `Macio`,
`Trepidante`. **Nunca** `Hard`, `Soft`, `Choppy`.

Isto não é cosmético. Nomes iguais convidam à comparação byte a byte, e é a
comparação que cria o problema — inclusive quando não houve cópia. Nome
diferente e curva medida por você não têm o que comparar.

### R3 — Proveniência datada, sem exceção

Todo valor entra no projeto com o registro de como nasceu, em
`docs/protocol/curvas-proprias.md`: quem mediu, quando, com que controle e por
que aqueles números. O dado e a origem **nunca** se separam.

Valor sem proveniência não entra. Não há atalho aqui: um único número órfão na
tabela contamina a defesa da tabela inteira.

### R4 — Fronteira explícita no código

No arquivo, deve estar visualmente separado o que é:

  - **fato do protocolo** — formato do report, posição dos bytes, semântica dos
    campos. É do hardware da Sony, descoberto por medição, não é obra de
    ninguém;
  - **criação nossa** — as curvas. Escolha autoral, com proveniência.

São coisas juridicamente distintas e devem ser legíveis como distintas por quem
abrir o arquivo daqui a dois anos.

## O que fazer se uma regra for violada

Sem drama e sem apagar rastro: **registre**. Um valor que entrou sem
proveniência sai da tabela e volta medido. Uma consulta indevida se anota no
documento de proveniência, e os valores tocados por ela são refeitos.

O histórico do git é imutável e público — tentar limpar rastro é o
comportamento que efetivamente compromete um projeto. Corrigir à vista, não.

## Ordem de execução

As sprints em `docs/process/sprints/` estão numeradas e são **sequenciais**.

| Sprint | O que fecha | Depende de |
|---|---|---|
| **CR-01** | posição jurídica registrada, com data | — |
| **CR-02** | formato que recusa valor sem proveniência | CR-01 |
| **CR-03** | a bancada de medição | CR-02 |
| **CR-04** | os efeitos da casa | CR-03 |
| **CR-05** | `NOTICE` declara toda a proveniência de terceiros | CR-01 |
| **CR-06** | curvas publicadas como material livre | CR-04 |

Nenhum valor de curva entra no repositório antes de CR-01 e CR-02 concluídas.
A CR-05 corre em paralelo às demais — é higiene documental, não bloqueia
medição.

## Sobre reescrever o histórico

**Não se apaga histórico por causa deste assunto.** A tentação existe e é
compreensível: parece que sumir com os commits afasta o risco. Faz o contrário.

Reescrever histórico onde **não houve** infração cria a aparência de que houve.
O force-push fica registrado nos forks, nos clones já baixados, no cache da
plataforma e nas execuções de CI — e a pergunta que sobra para quem olhar é "o
que foi apagado?", sem que exista mais o histórico para responder.

O histórico é a defesa: ele mostra a decisão de recusa sendo tomada, com data,
no momento em que o material foi encontrado. Isso é prova de independência.

`filter-repo` é a ferramenta certa para **vazamento de dado sensível** — senha,
chave privada, endereço de hardware de uma pessoa. Ali a exposição é o dano, e
o dado precisa sumir. Decisão técnica documentada é o oposto: a exposição é a
proteção.

## O que este processo NÃO é

Não é obstrução ao ecossistema DSX. O Hefesto continua **aceitando o protocolo
do DSX** — envelope e seis instruções, documentado em
`docs/protocol/udp-schema.md`. Interoperabilidade é legítima e desejável; o que
não se faz é copiar a implementação alheia.

Também não é ocultação. O `NOTICE` declara em voz alta o que foi recusado e por
quê. Um projeto que esconde a existência da fonte age mal; um que a nomeia e
recusa, não.
