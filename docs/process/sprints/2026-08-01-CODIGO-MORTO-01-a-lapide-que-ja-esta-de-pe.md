# CODIGO-MORTO-01 — a lápide que já está de pé

- **Status:** CICATRIZ — medido em 01/08/2026 contra o código de hoje: a cura
  está no lugar, com teste que morde, e **não há entrega de código nesta
  sprint**. O que faltava era o documento, e é este
- **Prioridade:** BAIXA para conserto (não há o que consertar), ALTA para
  registro — este identificador é citado de dentro de `src/`, o que faz o
  código apontar para um documento que até hoje não existia
- **Aberta em:** 01/08/2026, pela auditoria de 31/07 que contou treze
  identificadores de sprint sem documento e nomeou este como o mais grave dos
  treze, exatamente por ser citado no fonte
  (`docs/process/estudos/2026-07-31-auditoria-geral-o-que-treze-agentes-mediram.md:315`)
- **Relacionada:**
  [JANELA-CEGA-01](2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md)
  (que diagnosticou o defeito e onde o parágrafo original vive, `:180-189`),
  [DOC-VERDADE-02](2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md)
  (E9, que consertou a frase do ADR-014 por causa desta cura) e o
  `docs/adr/014-cosmic-wayland-support.md` (nota de verificação de 31/07,
  `:155-175`)
- **Não é** uma sprint sobre código morto em geral. O identificador nasceu com
  UM alvo e só um: `integrations/xlib_window.py`, na linha 1400 do mapa de
  17 agentes. Outros módulos suspeitos de estarem mortos continuam sem dono e
  estão listados na seção final

## O fato que resume a sprint

O `integrations/xlib_window.py` guardava 111 linhas que **nenhum código de
produção importava** e que liam o `_NET_ACTIVE_WINDOW` da raiz **sem gate de
foco** — o defeito exato que o UX-02 e o FOCO-01 tinham curado no backend vivo.
Enquanto o arquivo importasse limpo, era armadilha carregada: bastava alguém
achar e usar para reintroduzir o ping-pong de perfil com a suíte verde.

Em 29/07 o arquivo virou **lápide**. Hoje ele tem 41 linhas, levanta
`ImportError` no import, e a mensagem do erro aponta o substituto pelo nome.
Reenquadrar é o resultado: **este documento não abre trabalho, ele registra que
o trabalho já foi feito** — e é isso que o código, que cita `CODIGO-MORTO-01`
duas vezes, precisava ter do outro lado do nome.

## O que já existe, medido em 01/08/2026

| O quê | Onde | Medida de hoje |
|---|---|---|
| A lápide | `src/hefesto_dualsense4unix/integrations/xlib_window.py:1` | 41 linhas; o docstring explica o porquê e cita o identificador |
| O erro alto | `xlib_window.py:41` | `raise ImportError(_MENSAGEM_LAPIDE)` no corpo do módulo — dispara em todo import, não só no primeiro |
| A mensagem que aponta o substituto | `xlib_window.py:32-39` | cita `window_detect.build_window_reader()` para leitura contínua e `window_detect.get_active_window_info()` para leitura pontual |
| O backend vivo, com gate de foco | `integrations/window_backends/xlib.py` | só aceita a leitura quando `get_input_focus()` e `_NET_ACTIVE_WINDOW` concordam |
| A fábrica que todo mundo usa | `integrations/window_detect.py:179` | mantém a assinatura da API antiga, sob outro nome de módulo |
| O teste que morde | `tests/unit/test_xlib_window_nao_importavel.py` | 86 linhas, 5 testes, todos verdes em 01/08 |
| O ADR corrigido | `docs/adr/014-cosmic-wayland-support.md:159-166` | *"o item 3 da Camada 1 caducou"*, com o motivo e os substitutos |
| O diagnóstico de origem | `docs/process/sprints/2026-07-28-JANELA-CEGA-01-o-detector-que-nunca-adoece.md:180-189` | traz a marca `RESOLVIDO em 29/07/2026 pela CODIGO-MORTO-01` |

Três medições que decidem o veredito, e nenhuma vem de campo `Status:` de
documento nenhum — a auditoria de 31/07 provou que 41 de 50 cabeçalhos mentem:

1. **A lápide morde de verdade.**
   `.venv/bin/python -m pytest tests/unit/test_xlib_window_nao_importavel.py -q`
   sai verde, e o que ele afirma não é decorativo: importar levanta
   `ImportError` (`:38-40`), levanta **de novo** na segunda tentativa e não deixa
   meio-módulo em `sys.modules` (`:51-56`), a mensagem cita `window_detect` e
   `build_window_reader` (`:43-48`), e o fonte não tem mais `class XlibClient`,
   `intern_atom` nem `get_full_property` (`:59-65`).
2. **Nenhum módulo de produção voltou a importá-la.** O quinto teste
   (`:68-86`) varre `src/hefesto_dualsense4unix/**/*.py` inteiro procurando
   linha de import que cite `xlib_window`, ignorando comentário. Conferido à
   mão hoje: as cinco ocorrências restantes do nome fora da lápide
   (`window_detect.py:12` e `:179`, `window_backends/xlib.py:3`,
   `window_backends/base.py:30`) são **todas** docstring que descreve a API
   histórica — nenhuma é import.
3. **Nada no repositório importa módulos em massa.** `grep -rn
   "walk_packages\|iter_modules" src/ tests/ scripts/` devolve vazio, e
   `grep -rn "xlib_window" packaging/` também. A lápide viaja dentro do wheel
   (`pyproject.toml:83`, `packages = ["src/hefesto_dualsense4unix"]`) sem que
   nenhum empacotador ou coletor tropece nela — que é a condição para uma
   lápide ser barata.

### O que continua errado, e não é código

Dois documentos ainda descrevem o arquivo como ele era antes da cura:

| Documento | Linha | O que diz | O que é hoje |
|---|---|---|---|
| `docs/process/estudos/2026-07-29-mapa-total-o-estudo-de-dezessete-agentes.md` | `:582-585` | *"continua na árvore: 111 linhas que nenhum código de produção importa"* | 41 linhas que não importam |
| idem | `:1400` | `Código morto que importa limpo` / `CODIGO-MORTO-01, sem documento` | não importa limpo, e agora tem documento |

**Isto não é uma entrega desta sprint, por escrito.** Os dois são `estudos/`, e
estudo é foto datada: reescrever o que dezessete agentes mediram em 29/07 apaga
a medição em vez de a superar. Quem quiser fechar o laço acrescenta a marca de
resolvido, como a JANELA-CEGA-01 fez em `:182-188` — nunca troca o texto
antigo.

## Entregas

### E1. Este documento existe, e o código deixa de apontar para o vazio

**Aceite:** `grep -rn "CODIGO-MORTO-01" src/ docs/` devolve, além das duas
citações no fonte (`xlib_window.py:1` e `:34`), um arquivo em
`docs/process/sprints/` cujo nome carrega o identificador. Nenhuma linha de
`src/` muda.

### E2. O identificador sai da lista de órfãos com o veredito CICATRIZ

O índice do dia
([2026-07-31-INDICE-as-ondas-depois-da-auditoria.md](2026-07-31-INDICE-as-ondas-depois-da-auditoria.md))
e a seção (D) da auditoria de 31/07 contam `CODIGO-MORTO-01` entre treze
identificadores sem documento. Ele passa a ter documento, e o documento diz que
não há trabalho — que é informação diferente de "aberto".

**Aceite:** a próxima recontagem de órfãos encontra doze, não treze, e o motivo
da baixa está escrito aqui e não numa planilha à parte.

### E3. O critério de morte da lápide fica escrito — e não é agora

Uma lápide não é eterna de graça: são 41 linhas que viajam em todo pacote e um
teste que roda em toda suíte. A pergunta *"quando ela sai?"* nunca foi
respondida, e responder agora custa uma frase.

O critério proposto, e ele é conservador de propósito: **a lápide sai quando
uma versão maior (1.0) declarar quebra de compatibilidade de import**, e não
antes. Até lá, quem cair nela por um script antigo, um traceback ou um `grep`
lê o substituto em vez de receber um `ModuleNotFoundError` mudo — que é o
serviço inteiro que ela presta.

**Aceite:** este parágrafo. Se alguém quiser antecipar, a decisão é dela e
passa por aqui — não por uma limpeza de rotina.

## Teste que morde

**Já existe, e é ele que sustenta o veredito desta sprint:**
`tests/unit/test_xlib_window_nao_importavel.py`, cinco testes, coberto pelo job
`lint-test` (que roda `pytest tests/unit`). Ele não precisa de PyGObject, então
morde também no CI headless.

A prova de que morde não é teórica; está no desenho dele. Arrancar a cura tem
duas formas, e as duas reprovam:

| Se alguém... | Reprova em |
|---|---|
| apagar o `raise ImportError` (a lápide vira módulo vazio importável) | `test_importar_levanta_import_error`, `test_mensagem_aponta_o_substituto` e `test_import_falha_de_novo_na_segunda_tentativa` |
| trazer de volta a leitura cega (`class XlibClient`, `intern_atom`, `get_full_property`) | `test_a_leitura_cega_saiu_do_arquivo` |
| escrever `from ...integrations import xlib_window` em qualquer módulo de `src/` | `test_nenhum_modulo_de_producao_importa_o_xlib_window`, que varre a árvore inteira |

**O que este documento NÃO acrescenta:** nenhum teste novo. Um teste a mais
aqui só repetiria o que os cinco já afirmam, e a casa já pagou o preço de
teste-muralha que trava texto sem medir comportamento.

## O que NÃO fazer

- **Não apagar `xlib_window.py` "para limpar".** O arquivo vazio devolve
  `ModuleNotFoundError` mudo e desfaz o serviço da lápide, que é apontar para
  o substituto. O critério de morte está na E3.
- **Não reescrever os dois parágrafos do mapa de 29/07.** São foto datada;
  acrescentar marca de resolvido é o padrão da casa, trocar o texto não é.
- **Não usar este identificador como guarda-chuva de "código morto".** Ele
  cobre um arquivo. Chamar de CODIGO-MORTO-02 o próximo é mais barato do que
  alargar este e perder a rastreabilidade das duas citações que já existem no
  fonte.
- **Não confiar no campo `Status:`** de nenhum documento citado aqui para
  concluir o que quer que seja. A auditoria de 31/07 mediu 41 de 50 dizendo
  ABERTA, incluindo entregas provadas. Tudo nesta página foi derivado do código
  de 01/08.

## O que eu NÃO medi

- **Se há outros módulos mortos em `src/`.** Não varri a árvore atrás de
  módulos sem importador; o escopo deste identificador é um arquivo, e alargar
  o escopo aqui inventaria trabalho em vez de o medir. O mapa de 29/07 lista
  outros suspeitos sem dono (`sensor_hub.py` entre eles, `:1395`) e nenhum tem
  documento.
- **A lápide num pacote real.** Conferi que ela entra no wheel pela declaração
  do `pyproject.toml`; não instalei o `.deb`, o AppImage nem o Flatpak para
  ver o arquivo em disco.
- **O comportamento com `python -O` ou com bytecode pré-compilado antigo.** Um
  `.pyc` de antes de 29/07 num diretório `__pycache__` sobrevivente
  importaria a versão velha; não testei esse caso, e ele é de máquina suja,
  não de release.
