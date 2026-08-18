# A saída bruta dos agentes

O que um agente devolveu, como devolveu. **Não é documentação** — é matéria-prima.
Quem quer a conclusão lê a sprint ou o estudo; quem quer conferir de onde ela
saiu, ou reaproveitar uma medição que ninguém materializou, lê aqui.

Existe desde **06/08/2026**, a pedido dela, depois de uma sessão de trabalho
morrer por `SIGKILL` com 116 agentes de pesquisa em voo:

> *"não esquece de ir salvando os outputs dos agentes dentro do repo"*

O motivo é simples: `/tmp` é volátil e o transcrito da sessão mora fora do
projeto. Quem clonar o repositório daqui a um ano não tem nem um nem outro.

## Nada entra sem passar pelo sanitizador

```bash
python3 scripts/sanitizar_saida_de_agente.py ORIGEM DESTINO
```

**Isto não é burocracia.** O `.gitignore` bloqueia `docs/process/audits/` com um
comentário que é a lição inteira:

```
# anonimato isenta docs/process/**, entao o bloqueio aqui e a defesa real.
```

O portão de anonimato **não olha** `docs/process/**`, e saída bruta de agente é
onde vazam coisas. Foi por ali que a senha `sudo` da mantenedora entrou no
repositório em 26/06/2026 e chegou a cinco commits que hoje estão em
`origin/main` — público. A faxina tirou os arquivos da árvore; o histórico
guarda, e nenhuma reescrita desfaz o que já foi clonado.

O sanitizador:

- **mascara** MAC real nas três grafias (com separador, colado, e com o OUI
  elidido), pela convenção da casa — octetos 4 e 5 zerados. O OUI em si fica:
  ele é público, e é o que explica o achado;
- **mascara** o caminho do `HOME`;
- **recusa** o arquivo inteiro se achar `echo <senha> | sudo -S`, senha literal,
  token, chave privada ou credencial `Bearer`. Recusa — não conserta. Mascarar
  segredo automaticamente é a esperteza que cria a próxima falha silenciosa;
- **avisa, sem recusar**, quando vê `sudo -S` solto: os relatórios citam o
  comando para explicar um achado, e recusar a citação faria o portão virar
  ruído, que é como um portão morre.

O portão `tests/unit/test_saida_de_agente_sanitizada.py` reprova se algum
arquivo daqui voltar a ter segredo ou MAC real. A lista de OUIs tem **dono
único** em `tests/unit/test_docs_mac_anonimato.py`, e o teste reprova se as duas
divergirem.

### NOTA DATADA, 07/08/2026 — o filtro estava mirando a forma ERRADA

**GRAU: MEDIDO.** Até esta data o sanitizador reconhecia a senha em duas formas
só: o cano `echo ... | sudo -S` (a de 26/06) e a palavra-chave **com
separador** (`senha:`, `password=`). **Ela não escreve de nenhuma das duas
maneiras.** Ela escreve a senha **solta, sem separador nenhum**, ao lado do
`sudo` — a forma apareceu em 06/08 e de novo em 07/08, nas duas vezes em que ela
autorizou uma leitura com root. Contra essas duas linhas o filtro respondia
**nada**, e o arquivo passaria.

É o mesmo cano de 26/06 com a mira presa na forma anterior — e ele só voltou a
ser perigoso porque em 06/08 ela mandou versionar a saída dos agentes, que é o
que esta pasta é.

**Curado no mesmo dia**, com dois padrões novos em `_SEGREDOS` e a mordida
verificada (arrancados os dois, `1 failed, 120 passed`; devolvidos, `121
passed`). Eles são **apertados de propósito**: só um número solto onde deveria
haver um comando, e só um número colado à palavra-chave. Medido antes de entrar:
**753** arquivos de `docs/`, `scripts/` e `tests/unit/` varridos, **zero**
acertos — nenhum `sudo systemctl`, `sudo python3` ou data reprova.

**O que continua verdade, e não tem cura por portão:** o histórico do `git`
guarda o vazamento de 26/06, e nenhum portão desta casa varre histórico — o de
MAC lê `git ls-files` e o disco, que é a regra certa para tudo, menos para isto.
A árvore está limpa; o passado, não.

## O que há aqui

| pasta | o que é |
|---|---|
| `2026-08-06/subagentes/` | o relatório final de cada subagente, com a tarefa que recebeu |
| `2026-08-06/workflows/` | o resultado completo de cada workflow, com custo e fases |

O `INDICE.md` de cada leva diz quem foi cada agente.

## O que NÃO entra aqui

**O transcrito da conversa.** Ele contém o que ela escreveu, inclusive coisas
que ela mandou em confiança — e uma senha, em 06/08. O contexto da conversa que
vale ser preservado vira estudo, escrito e revisado, em
[`docs/process/estudos/`](../estudos/).
