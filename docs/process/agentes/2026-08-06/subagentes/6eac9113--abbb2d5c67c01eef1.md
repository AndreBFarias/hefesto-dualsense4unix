# agente abbb2d5c67c01eef1 (sessao 6eac9113)

**tipo:** general-purpose
**tarefa:** Funil de gravação de perfil
**profundidade:** 1  **pai:** -

## O QUE FOI PEDIDO

Repositório /mnt/Apate/Desenvolvimento/hefesto-dualsense4unix. LEVA 2 — IMPLEMENTAR. Você PODE e DEVE alterar arquivos.

SEUS ARQUIVOS (não toque em outros de src/, para não colidir com agentes irmãos):
- `src/hefesto_dualsense4unix/app/actions/footer_actions.py`
- `src/hefesto_dualsense4unix/app/actions/base.py`
- `src/hefesto_dualsense4unix/app/draft_config.py` (só se indispensável)
- testes novos em `tests/unit/`

TAREFA: curar o DEFEITO A e criar o caminho que impede a recaída.

O DEFEITO (provado e medido, não reinvestigue): `footer_actions.py` `_on_saved` (~:352-368) atualiza `_active_profile_name` e `_draft_baseline` mas NUNCA reaponta `self.draft`. O método `DraftConfig.with_profile_identity` (`draft_config.py:629`) existe exatamente para isso, sua docstring (`:644-650`) descreve o caminho do rodapé como o defeito que ele cura, e tem UM ÚNICO chamador em produção: `profiles_actions.py:1719`. Com `source_name` velho, o gate `mesmo_perfil` (`draft_config.py:562-564`) responde False para sempre e todo save seguinte grava `MatchAny()` + prioridade `max(catch-all)+10` — catraca medida: 1º save prio 10, 2º save prio 20.

O QUE FAZER:
1. **Um funil único de gravação.** Criar em `app/actions/base.py` (ou um `profile_writer.py` novo se ficar melhor) o ÚNICO ponto por onde a GUI grava perfil. Ele deve: chamar `save_profile`, reapontar o rascunho via `with_profile_identity(profile)`, atualizar `_draft_baseline`, recarregar a lista e notificar `launch_env.refresh`. Converta os call sites de `footer_actions.py` (save, import, restore — ~:350, :462, :520) para passarem por ele.
   ATENÇÃO de desenho já levantado: hoje `_save()` devolve o `Path`; o funil precisa do `Profile` gravado. Ajuste a forma minimamente.
2. **A invariante, explícita:** *toda gravação de perfil feita pela janela termina com o rascunho apontando para o que ficou em disco* — `draft.source_name == profile.name` e os `source_*` iguais aos do perfil gravado. Documente-a no funil e coloque um assert barato no fim.
3. **A prioridade só é calculada para perfil que NÃO existe em disco.** Para quem já existe, herdar a do arquivo. Hoje `footer_actions.py:344-347` sempre recalcula.
4. **O portão que impede a recaída** (é o pedido central da mantenedora): um teste que faz `grep`/AST por chamadas a `save_profile(` dentro de `src/hefesto_dualsense4unix/app/` e REPROVA qualquer uma fora do funil. Assim quem escrever o quinto botão não precisa lembrar de nada — não consegue gravar por fora. Siga o estilo do

## RESULTADO FINAL

LEVA 2 entregue. Resumo:

## O que mudou

**Funil novo — `src/hefesto_dualsense4unix/app/actions/profile_writer.py` (arquivo novo, 226 linhas)**
- `ProfileWriterMixin._gravar_perfil_async` (:69) — o único ponto de gravação da janela. Constrói → `save_profile` (worker) → toast/log → `_reapontar_rascunho` → recarrega lista → `launch_env.refresh` → gancho do chamador → assert de invariante.
- `_reapontar_rascunho` (:159) com a linha que faltava: `self.draft = draft.with_profile_identity(profile)` (:185), mais `_active_profile_name` e `_draft_baseline`.
- `_conferir_invariante_de_gravacao` (:189) — o assert barato pedido (`source_name` e `source_priority` contra o perfil gravado), só cobrado quando a gravação é a do rascunho.
- A invariante está escrita no topo do módulo, com a medição (10 → 20 → 30) e a linhagem ABAS-01.

**`app/actions/footer_actions.py`**
- Base virou `ProfileWriterMixin` (:113); `save_profile` e `profiles_dir` saíram dos imports.
- `_prioridade_do_save` (:334) — novo: **prioridade só é calculada para perfil que não existe em disco** (:367 herda `existente.priority`). `on_save_profile` passa o `alvo` achado por slug (:325-330).
- Os três call sites convertidos: save (:397), import (:505), restore (:585). O restore usa `depois_no_worker` para reler o rascunho sem voltar I/O para a thread GTK, e agora cai em `from_profile(profile)` quando a releitura falha (antes devolvia `None` e deixava identidade nova com conteúdo velho).

**Portão — `tests/unit/test_gravacao_de_perfil_passa_pelo_funil.py` (novo, 11 testes)**
- `test_nenhuma_gravacao_de_perfil_fora_do_funil`: varre `app/**/*.py` por **AST** (não texto) atrás de chamadas a `save_profile(` e reprova qualquer uma fora da lista.
- `_AUTORIZADOS_A_GRAVAR` tem 2 entradas: o funil e `profiles_actions.py` (exceção datada — não é meu arquivo nesta leva). Dois testes companheiros travam a lista contra crescimento e exigem que todo autorizado chame `with_profile_identity` por conta própria.

## A prova da mordida

| cura arrancada | resultado |
|---|---|
| só `with_profile_identity` | **7 vermelhos** (3 por comportamento + 4 pelo assert de invariante) |
| idem, com o assert também desligado | **3 vermelhos** de comportamento |
| só a herança de prioridade | `10 != 50` em `..._herda_a_prioridade` |
| **as duas** | `"o segundo save subiu a prioridade para 20"` — a catraca medida, reproduzida |

Tudo devolvido: 11 verdes.

## Verificação final
- `pytest -q tests/unit/ -k "footer or draft or perfil or profile"` → **953 passed**
- `ruff check src/ tests/` → **All checks passed**
- `mypy src/hefesto_dualsense4unix` → **Success, 162 arquivos** (precisei anotar `perfil: Profile` em `_construir`, porque `self.draft` é `Any` no mixin)
- Acentuação e glifos nos meus arquivos: rc=0

## O que ficou fora / precisa da sua atenção
1. **Tive de tocar 4 testes que não eram meus** — sem isso ficavam vermelhos, porque a gravação mudou de módulo: `test_footer_actions.py`, `test_abas01_conflito_entre_abas.py` e `test_perfil_salva_tudo_abas.py` repontam o dublê de `save_profile` para `profile_writer`; `test_dedup_guard.py` tinha um portão que contava `>= 3` chamadas de `_notify_launch_env_refresh()` no rodapé — agora é uma só, no funil. Reescrevi o portão para cobrar a **garantia** (o funil avisa + os três botões passam pelo funil) e deixei nota datada explicando o que caducou.
2. **`match` ainda não é herdado do disco.** Item 3 cobriu prioridade. Salvar por cima de um perfil que já existe **e é diferente do ativo** continua gravando `MatchAny()` — quem gateia isso é `mesmo_perfil` no `to_profile`, e mexer ali brigaria com o R-11. Fica como defeito residual medido.
3. `profiles_actions.py:1222` segue gravando fora do funil (não é meu arquivo). Está na lista de autorizados, com a razão escrita e a trava para a lista não crescer.
4. Deixei `profile_writer.py` e o teste novo **staged** (`git add`) — os portões desta casa são cegos a arquivo novo. Nada commitado.
5. A árvore está viva com agentes irmãos: durante o trabalho vi vermelhos transitórios em `daemon/lifecycle.py` e num `test_perfil_reescrito_na_partida_01.py` novo, que não tocam `app/actions/` e sumiram sozinhos. Na última rodada, tudo verde.
