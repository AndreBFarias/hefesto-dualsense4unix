# PALAVRA-01 — a janela fala a língua de quem joga

- **Estado:** **CONCLUÍDA — a E5 ENTROU** (verificado em 21/08/2026:
  `scripts/validar-palavra-de-tela.py` é hook `palavra-de-tela` no
  `.pre-commit-config.yaml`, com `--all` e `always_run`, e tem job próprio no CI
  — `.github/workflows/ci.yml:88` e `:109`; o jargão banido está travado por
  `tests/unit/test_palavra_a_janela_fala_a_lingua.py:239`)
- **Status em 31/07/2026, preservado:** **PARCIAL — as palavras entraram; a E5
  continua ABERTA** (conferido em 31/07: `.pre-commit-config.yaml` declarava
  quatro hooks —
  `acentuacao-strict`, `glifos`, `anonimato` e `ruff-check` — e **nenhum** olha
  capitalização ou jargão de texto de tela; é o portão que impediria a próxima
  leva de desfazer a janela em português)
- **Prioridade:** ALTA — melhor retorno por risco da fila: texto não quebra
  funcionalidade e é reversível linha a linha
- **Aberta em:** 27/07/2026, a pedido dela: *"em termos de texto, nomes de botões
  e de áreas, acha que podemos melhorar? acho que todas as abas caberiam isso"*
- **Escopo decidido por ela, na hora:**
  - **os nomes das nove abas ficam** — com **uma exceção**: *"tirar o dsx ali do
    nome"*;
  - *"veja a acentuação também. E a capitalização da primeira letra, que é
    obrigatório"*
- **Regra da casa que isto aplica:** R-C (um nome, um conceito) e a regra de
  escrita do `CONTRIBUTING`

## A medição

### Capitalização — 28 textos que ela vê começam em minúscula

Varredura sobre `app/`, resolvendo o markup Pango (é por dentro dele que a
maioria escapa de qualquer revisão):

```
textos de tela definidos em Python:   80
comecam com letra minuscula:          28
```

Os que aparecem na tela dela hoje:

| Texto | Onde |
|---|---|
| `ligado`, `desligado`, `desligado (suprimido)` | `emulation_actions.py:407,409,535` |
| `desligado — emulação normal` | `emulation_actions.py:556` |
| `daemon pausado`, `daemon offline` | `emulation_actions.py:554,564` |
| `ligado — {máscara}` | `emulation_actions.py:531` |
| `uinput disponível` | `mouse_actions.py:362` |
| `o mouse virtual está sem permissão` | `mouse_actions.py:366` |
| `o mouse virtual ainda não está pronto` | `mouse_actions.py:371` |
| `falta um componente do mouse virtual` | `mouse_actions.py:376` |

Nota de honestidade sobre a varredura: quatro dos 28 achados são `status_daemon`,
`status_connection` e afins — **nomes de widget**, não texto de tela. Falso
positivo do meu filtro, não erro do código. O número real de textos visíveis em
minúscula é 24.

### Acentuação — o glade está limpo

```
rotulos do glade com texto:            194
erros de acento encontrados:             0
rotulos comecando em minuscula:          3
```

Os três são `window_class:`, `title_regex:` e `process_name:` — nomes de campo
técnico literal do modo avançado. Não é descuido: é jargão exposto, e entra pelo
bloco de vocabulário abaixo, não pelo de capitalização.

### Tooltip — a lacuna maior de todas

```
rotulos com texto na janela:  194
que tem tooltip:                6
```

**188 controles não explicam nada.** É o número que mais pesa contra quem chega
sem saber o que a palavra significa.

### Jargão exposto no rótulo visível

`UINPUT:`, `VID:PID:`, `Buffer:`, `Passthrough em emulação:`, `Gamepads:`,
`Travar Proton validado`, `Restaurar Default`, `Custom (raw HID)`, `daemon`,
`uinput`, `allowlist`.

## Entregas

### E1. Toda frase de tela começa com maiúscula

Os 24 textos visíveis. `ligado` vira `Ligado`, `daemon offline` vira o que o
bloco E3 decidir, e assim por diante.

**Cuidado medido:** vários estão dentro de `set_markup` com Pango. Mexer ali sem
cuidado quebra a renderização inteira do rótulo — o markup precisa continuar
válido, e a cor do `<span>` não muda.

### E2. A aba perde o nome de produto de terceiros

`Navegação DSX` passa a dizer o que a aba faz. Entrou como **"Usar como mouse"** e, em 28/07, ela pediu o nome curto: **"Navegação"**.

O `DSX` é o nome de um programa de outra casa. Ele descreve de onde a ideia veio,
não o que o botão faz — e é a única aba cujo nome ela mandou trocar.

**O `id` do widget não muda**, só o rótulo visível e o `accessible-name`. Nenhum
perfil salvo é afetado.

### E3. Jargão sai da tela principal

| Hoje | Vira |
|---|---|
| `Restaurar Default` | `Voltar ao padrão` |
| `Travar Proton validado` | `Fixar a versão que funciona` |
| `Aplicar correções` | `Consertar problemas conhecidos` |
| `Testar criação de device virtual` | `Testar o controle virtual` |
| `daemon offline` | `O Hefesto está desligado` |
| `daemon pausado` | `O Hefesto está em pausa` |
| `uinput disponível` | `Pronto para usar como mouse` |
| `Gamepads:` | `Controles detectados:` |
| `window_class:` / `title_regex:` / `process_name:` | `Janela:` / `Título:` / `Programa:` |
| `UINPUT:` / `VID:PID:` / `Buffer:` / `Passthrough em emulação:` | vão para dentro de `Detalhes técnicos` |

O rodapé, que hoje diz

> *"Política exibida = estado atual do daemon; o perfil não tem opinião (escolha
> uma política para salvá-la no perfil)."*

passa a dizer o que acontece:

> *"Mostrando o que está ligado agora. Este perfil não guarda essa escolha —
> escolha uma para salvar nele."*

### E4. Tooltip onde a decisão é da pessoa

Não nos 188. Nos que **mudam o hardware** ou **tomam uma decisão que ela não
consegue desfazer** — que são os que custam caro quando mal compreendidos.

### E5. Um gate, para não voltar

Um teste que reprova quando:

- um texto de tela começa com letra minúscula (com lista de exceções explícita e
  justificada, não implícita);
- um rótulo visível contém termo da lista de jargão banido.

**Prova de que morde:** rodado contra o estado de hoje, ele **reprova nos 24**.
Depois da entrega tem de passar; e reintroduzir `daemon offline` num rótulo tem
de reprovar de novo.

## O que NÃO entra

- **Os outros oito nomes de aba ficam.** Ela decidiu, e o motivo é bom: nome de
  aba é memória muscular, e trocar oito de uma vez custa mais do que rende.
- **Nada de i18n.** Os catálogos existem e estão pela metade; misturar as duas
  coisas transforma uma sprint de baixo risco numa de alto.
- **Nenhum `id` de widget, nenhum nome de handler, nenhuma chave de perfil.** Só
  o que aparece escrito na tela.

## Como você valida

De olho, sem terminal:

1. Abrir as nove abas e ler os rótulos: **nenhuma frase começa em minúscula.**
2. A aba que era `Navegação DSX` agora diz o que faz.
3. Aba Emulação: onde dizia `desligado (suprimido)` agora está em português de
   gente, com maiúscula.
4. O rodapé não fala mais em "política" nem em "daemon".
5. Passar o mouse sobre um botão que muda o controle: **ele explica o que vai
   acontecer.**
6. Nada mudou de lugar. Esta sprint não move um pixel — só troca palavra.
