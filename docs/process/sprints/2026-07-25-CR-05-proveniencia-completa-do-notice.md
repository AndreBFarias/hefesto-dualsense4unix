# CR-05 — O NOTICE lista tudo que vem de fora, ou não vale nada

**Status:** ABERTA
**Depende de:** CR-01
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Fazer o `NOTICE` declarar **toda** a proveniência de terceiros do projeto, não
só a parte que foi lembrada.

## Por que isto importa mais do que parece

Um `NOTICE` incompleto é pior que nenhum. Ele afirma implicitamente "eis o que
vem de fora" — e cada omissão vira uma inconsistência que enfraquece o
documento inteiro, inclusive as partes corretas. A seção de recusa criada na
CR-01 perde força se o leitor encontrar material de terceiro não declarado três
diretórios adiante.

Não há suspeita de irregularidade aqui. GPL-2.0 é a licença mais conhecida do
mundo, os fontes DKMS trazem cabeçalho, e o projeto os mantém como patch sobre
baseline registrado — o que é a forma correta. O que falta é a **declaração**.

## O que precisa ser auditado e declarado

- [ ] **`assets/dkms/hid-nintendo/`** — `hid-nintendo.c` e `hid-ids.h` são
      código do kernel Linux (**GPL-2.0**), vendorados com patches próprios por
      cima. O `BASELINE` já registra o commit de origem; falta o `NOTICE` dizer
      isso em voz alta, com a licença e o que foi modificado.
- [ ] **`assets/dkms/hid-playstation/`** — mesma situação, pacote criado nesta
      leva.
- [ ] **`assets/dkms/rtw88-usb/`** — mesma situação.
- [ ] **Varredura do resto da árvore** atrás de material de terceiro não
      declarado: `assets/`, `scripts/`, `packaging/`, `flatpak/`, e qualquer
      trecho em `src/` derivado de outro projeto (a raiz `pydualsense` já está
      declarada para as regras udev — confirmar se há mais).
- [ ] **Verificar compatibilidade**: o Hefesto é MIT e os módulos DKMS são
      GPL-2.0. Eles são **distribuídos como fonte separada, compilados no
      destino** — não são linkados ao código Python. Confirmar que essa
      separação está clara na estrutura e no `NOTICE`, porque é ela que torna a
      convivência das duas licenças correta.

## O que esta sprint NÃO é

Não é caça a irregularidade. É higiene documental: o projeto usa material de
terceiro sob licenças que **permitem** esse uso, e o `NOTICE` deve refletir
isso por inteiro para que a seção de recusa (CR-01) tenha o peso que merece.

## Critério de conclusão

`grep` por qualquer arquivo de terceiro na árvore encontra a declaração
correspondente no `NOTICE`, com licença e modificações. Um leitor externo
consegue reconstruir a cadeia de proveniência sem abrir o histórico do git.
