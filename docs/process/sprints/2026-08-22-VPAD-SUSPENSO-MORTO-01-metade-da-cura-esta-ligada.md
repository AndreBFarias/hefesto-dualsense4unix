# VPAD-SUSPENSO-MORTO-01 — metade da cura está ligada

**22/08/2026.** Achado da auditoria de 228 sprints, por um cético que conferia
outra coisa. Não estava em lista nenhuma.

**Estado:** ABERTA

---

## O defeito, em uma linha

**Existe quem RETOMA o vpad e não existe quem o SUSPENDE.** A flag
`_steam_input_vpad_suspenso` só pode andar para `False`.

| Função | O que faz | Chamada em `src/` |
|---|---|---|
| `suspend_vpads_for_steam_input()` | põe `True` (`gamepad.py:882`) | **nenhuma** |
| `resume_vpads_after_steam_input()` | põe `False` (`gamepad.py:977`) | `gamepad.py:526` |
| `start_gamepad_emulation_desfecho()` | põe `False` (`gamepad.py:1956`) | (caminho de subida) |

A `suspend_*` só é exercitada por quatro arquivos de teste
(`test_coop_nao_cai_em_silencio`, `test_jogo01_um_dispositivo_por_controle`,
`test_esconder_em_vez_de_sair_01`, `test_aviso_falso_do_coop_01`). **A suíte
verde é o que esconde o defeito:** a função é testada, então ninguém percebe que
produção nunca a chama.

## Por que importa

`steam_input_vpad_suspenso()` é lida em três lugares de produção
(`lifecycle.py:2183`, `subsystems/hotkey.py:258`, e o par que a aba Emulação
consome). **Nenhuma dessas leituras pode ser verdadeira hoje.**

O par `(excecao_ativa, vpad_suspenso)` existe para distinguir dois estados:

- **os dois `True`** — o jogo da allowlist rodando com a entrada entregue a ele;
- **primeiro `True`, segundo `False`** — o jogo da allowlist rodando com o vpad
  **de pé**, porque a suspensão não pôde ser armada.

Como o segundo nunca é `True`, **o produto sempre relata o segundo estado**, e
quem olhar conclui que a suspensão falhou — mesmo quando não havia suspensão a
fazer. É pior que ausência de dado: é dado que mente sempre para o mesmo lado.

E a `CALADA_VPAD_SUSPENSO = "vpad_suspenso_pelo_steam_input"`
(`lifecycle.py:390`) é uma razão de calada que **nunca pode ser emitida**.

## O que NÃO é

Não é a JOGO-01/E2. Aquela sprint pede que a **frase da aba Emulação** leia o
par; esta diz que **metade do par está morta**. Ligar a frase agora escreveria
na tela um estado que o daemon não consegue produzir — foi por isso que a
triagem de 22/08 reclassificou a JOGO-01 de `SO_LIGAR` para **caducada**.

Também não é regressão de hoje: a `resume_*` foi ligada e a `suspend_*` não, e
não achei commit que tenha desligado a segunda. Se alguém achar, a nota vai
aqui.

---

## Entregas

### E1 — descobrir se a suspensão deve existir

**Antes de ligar, medir.** A função existe desde a JOGO-01 (25/07). Três saídas
possíveis, e a resposta muda tudo o que vem depois:

1. **Deve ser chamada e ninguém ligou** — é a família "a casa sabe e o produto
   não faz". Liga-se, com teste que morde.
2. **Foi desligada de propósito** — então a decisão existe em algum lugar e o
   código não a registra. Vira nota datada, e o par de estados vira um só.
3. **Foi substituída** por outro mecanismo (a escada de pontes, de 19/08, faz
   coisa parecida por outro caminho). Aí a `suspend_*` e a flag saem, e as três
   leituras de produção saem junto.

**Prova:** um parágrafo com a resposta e o commit ou a sprint que a sustenta.

### E2 — a consequência, seja qual for

- Se (1): a chamada entra no caminho de produção, com teste que reprova quando
  arrancada.
- Se (2) ou (3): a flag, a `CALADA_VPAD_SUSPENSO` e as três leituras saem —
  **fato errado sai, não ganha lápide** (ADR-021).

### E3 — o portão contra a classe inteira

O defeito é **assimetria de par**: uma metade ligada, a outra não. Um portão que
pegue a família: para todo par `armar/desarmar` (ou `suspend/resume`,
`enable/disable`) em `daemon/`, se um dos dois tem chamador em produção e o
outro não, reprova nomeando os dois.

Isso é irmão do `portao_a_casa_sabe_e_o_produto_nao_faz.py`, que hoje **não
pega** este caso: ele mede alcance por símbolo, não por par.

### E4 — o observável na aba Configurações

Pedido dela em 22/08: o estado tem de **aparecer na tela**, não só existir.

Lugar: a seção **"Está tudo certo?"** da aba Configurações, que é onde mora o
diagnóstico. A linha diz se o par de estados está coerente — e, enquanto a E1
não fechar, ela diz a verdade incômoda: *o produto não sabe relatar este
estado.*

**Depende de `CONFIG-09`** (a seção "Está tudo certo?"), que depende de
`CONFIG-01` (feita em 22/08, commit `c6b8daa`) e de `CONFIG-02`. Enquanto a
seção não existir, esta entrega não tem onde morar — e é assim que fica escrito,
em vez de a linha nascer solta noutra aba.

---

## Como morde

Arranque a chamada que a E1 acrescentar e o teste da E2 reprova. Sem o portão da
E3, a próxima assimetria de par entra igual — com a suíte verde, que foi
exatamente o que aconteceu aqui.

## O que este achado ensina

**Teste que exercita não prova que produção chama.** Os quatro testes da
`suspend_*` passam há semanas, e nenhum deles pergunta quem a invoca fora dali.
É a mesma lição do `prontuario_dos_jogos.py`, medida no mesmo dia: `pytest`
verde não derruba "capacidade sem chamador em produção".
