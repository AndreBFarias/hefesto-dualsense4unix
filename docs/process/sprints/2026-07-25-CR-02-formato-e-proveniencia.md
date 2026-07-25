# CR-02 — O formato do efeito próprio carrega a própria proveniência

**Status:** ABERTA
**Depende de:** CR-01
**Bloqueia:** CR-03, CR-04
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Fazer com que seja **impossível** um valor de curva entrar no projeto sem dizer
de onde veio. Não por disciplina — por estrutura de dados.

## O problema que isto previne

Documento de proveniência mantido à mão, separado dos dados, é documento que
desatualiza. Seis meses depois ninguém lembra se aquele `Pesado` foi medido ou
chutado, e a defesa evapora junto com a memória.

A regra R3 do processo diz "o dado e a origem nunca se separam". Esta sprint faz
disso uma propriedade do formato, não uma promessa.

## Entregas

- [ ] **Esquema do efeito próprio** em `profiles/schema.py`, com campos
      obrigatórios de proveniência:
      - `nome` — em português, vocabulário nosso (regra R2)
      - `curva` — os bytes
      - `medido_por` / `medido_em` — quem e quando
      - `controle` — modelo e transporte usados na medição
      - `nota` — o que a pessoa sentiu e por que parou nesses valores
- [ ] **Validação que recusa** efeito sem proveniência completa. Não é aviso:
      é erro. Valor órfão não entra.
- [ ] **Guarda de nomes** — a validação rejeita os doze nomes do DSX (`Hard`,
      `Soft`, `Choppy`, `GameCube`, `VerySoft`, `VeryHard`, `Hardest`, `Rigid`,
      `VibrateTrigger`, `Medium`, `VibrateTriggerPulse`, `VibrateTrigger10Hz`),
      com mensagem explicando a regra R2 em vez de só negar.
- [ ] **`docs/protocol/curvas-proprias.md`** — a tabela de proveniência, gerada
      a partir dos perfis, não escrita à mão. Se for escrita à mão, desatualiza.
- [ ] **Teste** que prova a recusa: efeito sem `medido_por` não carrega; efeito
      chamado `Hard` não carrega.

## Decisão de projeto a tomar aqui

Onde os efeitos próprios moram: em cada perfil (isolados, duplicados entre
perfis) ou num catálogo compartilhado que os perfis referenciam. A segunda opção
evita divergência de proveniência para o mesmo nome, que é exatamente o que este
processo quer impedir — mas exige migração de esquema. Decidir com o custo à
vista, não por inércia.

## Critério de conclusão

Tentar gravar um efeito sem proveniência, ou com nome do DSX, falha com
mensagem clara. E a tabela de `curvas-proprias.md` reflete o que está nos
perfis, sem passo manual.
