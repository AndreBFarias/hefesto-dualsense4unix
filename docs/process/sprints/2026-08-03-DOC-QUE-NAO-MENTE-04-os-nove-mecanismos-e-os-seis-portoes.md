# DOC-QUE-NÃO-MENTE-04 — os nove mecanismos, e os seis portões que os fecham

- **Status:** PROPOSTA, escrita em 03/08/2026
- **Prioridade:** **ALTA** — o primeiro comando que a documentação manda copiar
  **falha na primeira linha**
- **Faixa:** 3 — a documentação afirma o que o código desmente
- **Método:** quatro agentes varreram README, `docs/usage/`, `docs/adr/` e
  `docs/protocol/` **contra o código**, com verificação adversarial. Cada achado
  tem `arquivo:linha` dos dois lados
- **Índice:** [A leva do Bluetooth de primeira classe](2026-08-03-INDICE-o-bluetooth-de-primeira-classe.md)
- **Pedido dela, literal:** *"temos que ter correção de informações
  desatualizadas, tipo o readme, se tá assim lá imagina o resto da
  documentação"*. **Estava certa.**
- **Sucede:** `DOC-VERDADE-01`, `DOC-VERDADE-02` e a
  [DOC-QUE-NÃO-MENTE-03](2026-08-03-DOC-QUE-NAO-MENTE-03-a-foto-vazia-a-env-negada-e-a-tag-velha.md)
  desta mesma leva

---

## A LIÇÃO CENTRAL — leia antes da tabela

> **Estes achados não são descuido. São NOVE MECANISMOS, cada um com assinatura
> própria, e cada um produziu mais de um erro.** Corrigir as trinta frases sem
> fechar os mecanismos garante que a próxima leva reabra as mesmas.

É por isso que a entrega principal desta sprint são os **seis portões** (E2),
não as correções (E1).

---

## Os achados de dano ALTO

Só os confirmados pela verificação adversarial, ordenados por dano.

| onde | afirma | o código diz | classe |
|---|---|---|---|
| `README.md:89`, `instalacao.md:38`, `quickstart.md:36`, `flatpak.md:40` | `git clone https://github.com/[REDACTED]/…` | **o primeiro comando das três páginas de instalação falha na primeira linha.** O marcador é escrito por um hook **fora** do repositório | MENTIRA |
| `README.md:75`, `:91` | tag corrente é `v0.7.0` | `pyproject.toml:7` = **0.8.0**; instala a versão sem os 7 presets de gatilho consertados | CADUCADO |
| `gui/main.glade:2446` | *"ainda não existe um botão para desmarcar"* | `cli/cmd_steam.py:196` é `@app.command("remove")` — **nasceu no mesmo commit** (`e96dea8`) que o tooltip que o nega | MENTIRA |
| `troubleshooting.md:122-136` | janela compacta é *"default v3.3.0+"*, e manda `COMPACT_WINDOW=0` | `app/compact_window.py:64-79`: **OPT-IN, default DESLIGADO**. E o diagnóstico da página **confirma o estado errado** | MENTIRA |
| `docs/protocol/trigger-modes.md:107`, `:118` | `test trigger --raw --mode Pulse_AB --forces …` | **três defeitos num comando**: `--forces` não existe (é `params`); `--raw` faz `int(mode)` e aborta com nome; `--raw` é recusado com daemon vivo | MENTIRA |
| `cli.md:184-186` | os `test` *"pulam o daemon"* | os três tentam **IPC primeiro** (`cmd_test.py:141`, `:109-115`, `:206-212`). É a armadilha nº 3 do `CLAUDE.md` **ensinada como fato** | MENTIRA |
| `cli.md:52-61` | *"Falha conhecida, não corrigida"* no `--brightness` | curada em `a7438e0`, **25/07** — o mesmo dia da medição citada no aviso | CADUCADO |
| `troubleshooting.md:40-51` | storm: *"use uma OU outra"* | as duas curas de hoje são **padrão** e estão ausentes da página; e `install_snd_quirk.sh:18` diz que são **ortogonais**. Manda mexer em bootloader já configurado | CADUCADO |
| `bluetooth.md:104-105` | áudio por BT *"(fone e microfone) fora de escopo"* | falso desde 25/07 — **foi a fonte do erro do assistente em 03/08**. O **fone** continua correto: a frase erra por juntar os dois | MENTIRA |
| `README.md:270-280` | mic BT: *"~40% do sinal, causa em aberto"* | a cura tem nome de comando (`mic unmute`), e `grep -c unmute README.md` = **0** | CADUCADO |
| `README.md:129-134` | *"com os padrões de fábrica… um parâmetro no cmdline, cada um com sua flag de opt-out"* | `install.sh:203` `WITH_USB_QUIRK=0` — **opt-IN vendido como opt-OUT** | MENTIRA |
| `quickstart.md:101` | *"ligue Emular mouse+teclado"* | esse rótulo governava **só o mouse**, e foi o defeito `EMULACAO-NO-JOGO-01` (*"desligado e ainda levava Alt+Tab dentro do jogo"*). Hoje são **dois** interruptores | CADUCADO |
| `ADR-018:44-48` | a regra 75 é *"reversível via `…_DUALSENSE_MIC_INTENDED=1`"* | **nenhum leitor da env toca `authorized`/`bind`**. A reversão é remover o arquivo + replugar — e a env **rebaixa o alarme do doctor a `info`**, silenciando o diagnóstico | MENTIRA |
| `ADR-015:49`, `:66-71`, `:98` | *"a ordem de start é definida por `SUBSYSTEM_REGISTRY`"*, *"apenas criar um arquivo e registrá-lo"* | `subsystems/__init__.py:10-17`: *"esta lista é **declarativa** … acrescentar um subsystem aqui **NÃO o liga**. Foi assim que o `BtMicSubsystem` nasceu órfão"* | MENTIRA |
| `bluetooth.md:82` | re-parear *"sempre resolve"* | bond sem SDP exige `RemoveDevice` **e** `rm -f …/cache/${mac}` — *"o cache TEM de sair junto"* (`doctor.sh:1765`) | IMPRECISO |
| `README.md:228-247` | pareamentos somem *"por dois motivos"* | há uma **terceira** causa, com cura própria e acionável, que o `doctor` já conhece | IMPRECISO |
| `cli.md:27`, `:214` | `mic` aceita 5 ações | são **dez** (`cmd_mic.py:118-119`). **A ausente mais cara é `mic unmute`** — a que devolveu o áudio hoje | IMPRECISO |
| `cli.md:26`, `:195-207` | os subcomandos de `gamepad` | falta `gamepad steam-input list\|remove` — **o desfazer** do jogo marcado | IMPRECISO |
| `assets/78-…rules:20` + `doctor.sh:2478` | casam `Hefesto Virtual DualSense P*` | o nome mudou em `5801de9`. **A regra e o diagnóstico estão mudos** — produto, não doc | CADUCADO |

---

## Os NOVE MECANISMOS

**1. A nota que reafirma o veredito no dia em que ele caduca.** A ADR-016
reafirmou *"não há chave de usuário"* às 04:26; a env entrou às 17:54 do mesmo
dia. O README publicou *"causa em aberto"* **quatro minutos** depois da cura.
*O texto é escrito quando a pessoa acabou de estudar o assunto — que é
exatamente quando outra pessoa está mexendo nele.* **A datação não protege: ela
dá autoridade.**

**2. O documento fixa o DEFAULT; o código o muda sem tocar no doc.** Três
formas do mesmo erro: opt-in descrito como **inexistente** (métricas), como
**padrão de fábrica** (`--with-usb-quirk`), como **opt-out** (janela compacta).
*O default é o dado mais volátil do produto e o mais copiado para prosa
afirmativa.*

**3. O portão trava o NÚMERO e deixa passar a CONCLUSÃO.**
`test_doc_verdade_02_contagens_derivadas.py` confere que a ADR-016 diz *"quatro
parâmetros"* e **não olha a frase seguinte**, que é a mentira. Mesmo formato do
`check_bt_sdp_cache_envenenado`, que deu `[ OK ]` no meio do defeito.
**Portão cego na proporção da gravidade.**

**4. O teste verde certifica o texto MORTO do produto.**
`test_udev_kernel07_path06.py:88` exige que a regra 78 **contenha a string
antiga**; `test_doctor_vpad_motion.py` alimenta o fixture com o nome antigo. Os
dois passam **enquanto a regra e o `doctor` estão mudos**.

**5. A cura entra no código e o texto fica com a doença.** `--brightness`, mic,
storm, rota, pré-amp, lightbar — em todos, o commit da cura **não tocou nenhum
`.md`**. O sintoma diagnóstico é a frase *"falha conhecida, não corrigida"*:
**ela nunca é revisitada**, porque quem corrige está lendo código.

**6. Rename de rótulo sem varredura do corpus.** *"Navegação DSX"* → *"Navegação"*
(6 arquivos), *"aba Daemon"* → *"Sistema"*, *"Emular mouse+teclado"* → dois
interruptores, o nome do vpad (**2 regras/scripts quebrados**, 2 comentários
mortos, 2 testes travados). *O rename é feito com cuidado no lugar certo e nunca
com `grep`.*

**7. O quantificador universal.** *"e só delas"*, *"sempre resolve"*, *"100% do
protocolo"*, *"nenhuma das duas existe"*, *"por dois motivos"*, *"apenas criar um
arquivo"*. **O absoluto envelhece na primeira exceção — e é ele que faz a leitora
parar de procurar.**

**8. Comentário de código como documentação sem dono.** O `gerar_icones.sh`
afirmava que o CI o rodava e nenhum workflow o chamava (corrigido hoje).

**9. O escape que sobrevive ao motivo.** O `<!-- ref-externa -->` do
`metrics.md` entrou porque a env **não existia** — e ficou depois que ela passou
a existir, **silenciando o portão exatamente na linha que virou mentira**.

---

## As entregas

### E1 — as correções, agrupadas por mecanismo (não por arquivo)

Corrigir por mecanismo evita a ilusão de "já revisei esse arquivo". A ordem é a
dos mecanismos acima.

**Regra de ADR, que precisa ficar escrita:** *mudou o veredito ⇒ **nota**, corpo
intacto; o corpo continha **receita executável falsa** (comando, caminho, passo)
⇒ **corrige o corpo** e a nota declara a correção.* A casa já tem os dois
precedentes: a ADR-018 usa emenda datada, a ADR-017 reescreveu o corpo e
declarou item a item.

| ADR | forma | o que a nota registra |
|---|---|---|
| **016** | nota nova (não tocar no corpo nem nas notas anteriores) | a env existe desde `75d56a2`, **13 h depois** de a nota de 01/08 negá-la; vale só na subida; e o portão citado como cura trava a contagem, não a conclusão |
| **018** | emenda datada | a regra 75 **não** se reverte pela env; a única reversão é remover o arquivo + replugar; e a env **rebaixa o alarme do doctor a `info`** |
| **015** | **corpo + nota** (é receita executável falsa) | `SUBSYSTEM_REGISTRY` é declarativo; ligar exige `_safe_start` em `run()`; o `BtMicSubsystem` nasceu órfão **por esta receita** |
| **001** | nota datada | o que a `pydualsense` ainda faz e o que passou a ser nosso; e o risco de `pydualsense>=0.7.5` **sem teto** com subclasse de API privada |
| **012** | nota datada | a aba chama-se **Sistema** |

### E2 — OS SEIS PORTÕES (a entrega que vale mais que a E1)

**Cura de raiz do achado nº 1, e é UMA LINHA:**
`test_versao_publicada_data_e_paginas_de_uso.py:49` define
`PAGINAS_DE_USO = (INSTALACAO_REL, "quickstart.md", "flatpak.md")` — **o README
não está na tupla.** *O teste feito para pegar exatamente isto nunca olhou o
arquivo mais lido do projeto.*

| portão | o que faz | pega |
|---|---|---|
| **A — comando copiável tem de existir** | extrai todo bloco ```` ```bash ```` de `docs/` + README, pega as linhas `hefesto-dualsense4unix …` e valida contra o **AST do Typer** | `--forces`, `profile activate`, e as ações omitidas de `mic` e `gamepad` |
| **B — `[REDACTED]` nunca dentro de bloco executável** | reprova a combinação *"bloco bash + marcador"*, forçando a forma `https://github.com/<seu-fork>/…` que **sobrevive ao sanitizador** | README + as 3 páginas de instalação + o badge de CI |
| **C — default de env derivado do código** | varre `os.environ.get(N, "0") == "1"` em `src/` e cobra coerência com toda frase que cite a env e as palavras *default/opt-in/opt-out* | a janela compacta e o parágrafo do cmdline |
| **D — "não existe" é afirmação verificável** | toda frase da forma *"X não existe no código / zero ocorrências"* vira um `grep` executado | `metrics.md:19` (que hoje tem **4** ocorrências). **Corolário obrigatório: o `<!-- ref-externa -->` NÃO pode silenciar este portão** |
| **E — a env do subsystem entra na conta** | estender `_envs_lidas_na_subida` de `daemon/main.py` para todo `daemon/`, e trocar o assert de **contagem** por assert de **conclusão** | `hotkeys.md:29`, e impede que a próxima env nasça invisível |
| **F — o nome do vpad é derivado, não literal** | teste que lê `UhidDualSense.name` e exige o literal (com curinga) em toda `assets/*.rules` e todo `awk` do `doctor.sh` que pretenda casar o vpad | **substitui os dois testes que hoje travam o nome morto** |

### E2-bis — ÍCONE-VIVO-01: o portão que JÁ FOI APLICADO em 03/08

**Esta entrega está FEITA** — fica registrada porque é o mecanismo nº 8 em
estado puro, e porque a correção precisa de dono documental.

**O que se achou:** `scripts/gerar_icones.sh:10` afirmava, no próprio cabeçalho,
que `--check` *"é o que o CI roda"* — e `grep gerar_icones` em
`.github/workflows/` devolvia **zero**. A proteção existia só de lado, pelo
`test_icones_refletem_o_svg.py`, que chama o script de dentro do pytest:
funcionava, mas por um caminho diferente do declarado, e só avisava **minutos
depois do commit**.

**O que foi feito:**

1. **hook de pre-commit** `icones-refletem-o-svg` — roda `--check`, **avisa,
   nunca gera**. Gerar automaticamente poria PNG binário no commit sem revisão, e
   esta casa já pagou por ferramenta que edita arquivo sozinha (o higienizador
   que apagava glifo permitido). Os outros quatro hooks também são validadores;
2. **job `icones` no `.github/workflows/ci.yml`** — onde o script dizia estar;
3. **o comentário mentiroso do script foi corrigido**, e passou a listar os três
   lugares que rodam o `--check` de verdade;
4. **os ícones foram regenerados** — a divergência era real (o SVG do logo tinha
   sido editado sem regerar).

**Aceite (cumprido):** `scripts/gerar_icones.sh --check` sai zero; o YAML valida;
o hook está na lista; a suíte passou a 6792 verdes, sem a falha dos ícones.

### E3 — a regra 78 e o `doctor` (produto, não documentação)

Os dois casam o nome antigo do vpad e estão **mudos**. Sai junto com o portão F,
que impede a volta. *(Já registrado na
[ENTREGA-QUE-NÃO-LIGOU-01](2026-08-03-ENTREGA-QUE-NAO-LIGOU-01-o-codigo-que-existe-e-ninguem-chama.md);
aqui fica a referência cruzada.)*

---

## Testes que vão reprovar

```
pytest tests/unit -k "versao or doc or referencia or udev or doctor_vpad"
python3 scripts/validar-referencias-docs.py --all
```

## O que NÃO fazer

- **não corrigir linha a linha sem os portões** — são nove mecanismos, e a
  próxima leva reabre as mesmas frases;
- **não reescrever corpo de ADR** quando o que mudou é o veredito — a regra está
  na E1;
- **não exigir a URL real no portão B** — quem escreve o marcador é um hook fora
  do repositório; o portão cobra a **forma** que sobrevive a ele;
- **não deixar o `<!-- ref-externa -->` silenciar o portão D** — foi assim que a
  mentira das métricas sobreviveu.

## O que fica ABERTO

- **o hook global que escreve `[REDACTED]`** vive fora deste repositório e não
  pode ser consertado daqui — só contornado pela forma que o portão B exige;
- **a contagem completa dos achados de dano MÉDIO e BAIXO**, que a auditoria
  levantou e esta sprint não lista para não afogar o que importa.
