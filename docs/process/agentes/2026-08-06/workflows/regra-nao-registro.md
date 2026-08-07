# workflow regra-nao-registro

- runId: wf_c70cffd5-14d | status: completed | agentes: 10 | tokens: 1,211,552 | duracao: 55 min
- summary: Desenhar a cura GENERICA da identidade dupla e varrer o que so funciona na maquina dela
- fases: Medir, Desenhar, Escrever

## RESULTADO

### doc

Dois documentos escritos, `git add -A` feito, seis portões verdes, nada commitado.

**Arquivos (absolutos):**
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/sprints/2026-08-06-REGRA-NAO-REGISTRO-01-o-8bitdo-e-um-so-e-o-defeito-e-de-todo-mundo.md`
- `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/estudos/2026-08-06-o-que-so-funciona-na-maquina-dela.md`

**A regra escolhida** — duas identidades de HARDWARE do mesmo OUI que se REVEZAM na mesa (uma sai sozinha, a outra entra sozinha, sem ninguém do mesmo OUI mudando de presença no meio) e que se apresentam com VID:PID DIFERENTES passam a DIVIDIR um lugar na fila; a divisão morre no primeiro tick em que as duas aparecem juntas.

**Por que ela vence** — é regra, não registro: roda no primeiro boot de um desconhecido sem ninguém declarar nada, que é exatamente o que a pergunta dela cobra. O VID:PID-diferente torna estruturalmente impossível fundir duas unidades do mesmo modelo, e preserva `test_dois_aparelhos_do_mesmo_oui_nunca_se_fundem` sem tocá-lo. O gesto de reparo é o uso normal ("ligue os dois ao mesmo tempo"), não um botão. E o defeito de fusão é inobservável, não raro: `sync_connected` (`:1129`) roda antes de `slot_for` (`:1144`) e de `external_led_written` (`:1218`), então a ruptura acontece antes de qualquer atribuição.

**Enxertos que os juízes forçaram** — (1) o invariante *nenhum rosto é apagado da fila, nunca*: a união é rank COMPARTILHADO, não remoção; isso mata de uma vez a falha de durabilidade (perder a memória custa "aprender de novo", não o lugar) e a janela intra-tick entre remoção salva e concessão não-salva; (2) desempate da ruptura sempre definido, inclusive no primeiro tick após o boot; (3) "mesmo OUI" rebaixado a n=1, com falha fechada; (4) o gesto de reparo que FUNCIONA (`identity.number.set` na aba Status) nomeado antes do "Reconciliar jogadores", que compacta preservando ordem relativa e não conserta inversão.

**Correções de premissa registradas com nota datada** — o sintoma "cai no slot 5" já morreu na NUM-01 (`_posicao_locked` conta só presentes); a "simultaneidade" da IDENTIDADE-DUPLA-01 é leitura de `external_fila_restaurada`, que imprime o disco, não presença; a E1 "falta medir" estava medida desde 25/07. E a ficha da varredura anterior (declaração de irmãs + gesto na janela) caducou pela pergunta dela — não estava errada para o caso dela, estava errada para o alcance.

**Os três piores itens da dívida de portabilidade:**
1. **O repositório publica a identidade de rádio dos aparelhos da casa** — 20 linhas em 7 arquivos na forma 12-hex contígua; `docs/usage/troubleshooting-8bitdo.md:96` remonta os dois endereços do 8BitDo numa página de usuária; e `OUIS_REAIS` não lista o OUI de um dos DualSense, buraco já registrado em 29/07 e ainda aberto. Dano a **ela**, não ao amigo, e o conserto é regex.
2. **As duas tabelas de OUI com um item** — `_BRAND_BY_OUI` (`external_controllers.py:64`) e `NINTENDO_REAL_OUI` (`external_identity.py:160`, portão de `:859`): um 8BitDo de outro lote vira "Sony"; um Pro genuíno de outro lote fica com o giroscópio em STANDBY **sem uma linha de log**. Medi que os dois DualSense dela têm OUIs diferentes e que o `systemd-hwdb` não conhece nenhum dos dois — "um OUI por fabricante" é falso na própria bancada.
3. **A assimetria dos layouts de Steam** — `steam_launch_options.py:111-115` e `storm_doctor.py:146-149` conhecem quatro layouts; `emulation_actions.py:1262/1292` conhece um, e `proton_pin.py:152-165` conhece dois. Achado novo: a exclusão de Flatpak/Snap é uma decisão DELIBERADA e correta para o pino de Proton, mas `pastas_steamapps` reusou `default_steam_root` para traduzir appid em nome — onde o motivo dela não vale. Quem usa Flatpak vê duas verdades na mesma janela.

O único item na categoria QUEBRA é `scripts/gui-captura/retrato_offscreen.py:21`, com `~/...` cravado — e ele já está errado para ela (a árvore viva é `/mnt/Apate/`; funciona por acidente de link).

### vencedora

regra-que-aprende

### placar

[
  {
    "angulo": "regra-que-aprende",
    "nota": 7.5
  },
  {
    "angulo": "regra-conservadora",
    "nota": 6
  },
  {
    "angulo": "regra-mais-gesto",
    "nota": 6
  }
]


## LOGS

regra-que-aprende: 7.5
regra-conservadora: 6
regra-mais-gesto: 6
