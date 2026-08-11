# workflow perfil-por-jogo-e-cura-do-bt

- runId: wf_26c86ba1-7c4 | status: completed | agentes: 20 | tokens: 2,189,243 | duracao: 80 min
- summary: Entender a allowlist e a biblioteca Steam, desenhar a flag do perfil e o fluxo jogo->perfil, e integrar a cura de seguranca do BT no install/uninstall
- fases: Entender, Desenhar, Sintetizar, Implementar, Verificar

## RESULTADO

### apresentacao

Documento escrito em `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/docs/process/estudos/2026-08-06-desenho-a-flag-do-jogo-e-o-perfil-a-partir-da-biblioteca.md` (578 linhas). Quatro portoes verdes; zero U+2713/U+2717/emoji (checado por regex de categoria Unicode). Staged, nao commitado.

O QUE APRESENTEI (10 linhas)
1. Abertura de 5 linhas sem jargao: caixinha no editor, botao "Novo para um jogo da Steam", nao e modo novo, vale no clique, e o arquivo passa a ter UM nome nas tres abas.
2. ASCII de tres telas: editor com vizinhos reais (barra de botoes, Aplica a, mascara, "Salvar este perfil"), o dialogo do botao novo, e o ANTES/DEPOIS do botao da aba Sistema.
3. Densidade cortada de 5 sub-linhas para 2; o "quando marcar" foi para o tooltip, que e onde a casa ja poe contexto (`profiles_actions.py:105-108`).
4. Tabela de procedencia de cada rotulo, com grau por linha; correcao minha em publico: "entrada da Steam" NAO e texto de tela (so comentario em `daemon_actions.py:321,522,532`) — troquei por "Steam Input" (`main.glade:2951,2977`).
5. Nota datada resolvendo "dobrado" vs "duplicado": convivem na MESMA frase em `main.glade:2829`; proponho "duplicado" e registro que "dobrado" e a palavra dela.
6. Armazenamento: um fato, um arquivo, um dono — o perfil nao ganha campo; a caixinha e posicionada pelo DISCO releito, nunca pelo clique, com numero de geracao contra corrida.
7. Secao propria "o codigo faz o contrario": 4 de 5 comportamentos batem, o 5o (derrubar o vpad e o co-op) e o oposto — MEDIDO, com a docstring citada e o experimento 2.4 declarado SEM PROVA.
8. "O que isto NAO faz" com 10 itens, incluindo o achado novo e desconfortavel: marcar NAO liga o Steam Input (o `awk` de `disable_steam_input.sh:269-273` so PRESERVA), e as 2 contas escondidas (9 arquivos de teste quebram pelo sinal novo; `gui_dialogs.py` nao tem lista com colunas).
9. Sete portoes novos que tem de morder, mais os cinco existentes que vao avaliar.
10. Lista de arquivos tocados, com o subconjunto que so entra se o experimento fechar positivo.

AS TRES PERGUNTAS PARA ELA
- P1: O mesmo arquivo passa a ter um nome so nas tres abas — renomear "Este jogo nao funciona" para "Por este jogo na lista de excecoes"? RECOMENDO SIM: duas portas so param de confundir com a mesma placa, e chamar de "nao funciona" um jogo que ela marcou de proposito porque FUNCIONA e a confusao que ela reprovou.
- P2: A caixinha vale no clique, sem esperar o "Salvar este perfil"? RECOMENDO SIM: o dado e do JOGO, nao do perfil; adiar reintroduz a mentira "caixinha marcada, disco intocado".
- P3: Entregamos agora com a frase do preco de hoje, ou esperamos o experimento 2.4? RECOMENDO AGORA: a tela sobrevive aos dois desfechos, a frase vem do daemon e muda sozinha, e esperar mantem o desmarcar so por linha de comando.

### implementacao

**Relatório**

1. **install.sh** — o passo 3d (antes 1253-1324, hoje 1253-1281) perdeu a lógica inline e chama `bash "${ROOT_DIR}/scripts/bluez_config.sh" aplicar`. O mecanismo migrou para `/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh` (`aplicar`/`remover`/`verificar`, raiz falsa por `HEFESTO_BT_ETC`) — MEDIDO: era intestável, todo portão lia install/uninstall como texto, e foi isso que escondeu o defeito.
2. **O caso real desta máquina** (MEDIDO: `/etc/bluetooth/main.conf:25` = `always`, dentro do bloco `# >>> hefesto bluetooth >>>`, escrito por versão anterior nossa): o `aplicar` **reconhece** o valor divergente antes de reescrever e **diz em voz alta** `ATENÇÃO: JustWorksRepairing=always escrito por uma versão ANTERIOR do hefesto`. Chave ativa **fora** do bloco é **neutralizada** com `#hefesto-desativou# `, não apagada.
3. **Assimetria fechada (a estrutural)** — `if -d main.conf.d` / `elif -f main.conf` virou **cumulativo**: o `main.conf` é sempre normalizado e os drop-ins entram **por cima**. Antes, com o diretório presente o install anunciava `confirm` sem nunca abrir o arquivo que o BlueZ lê (MEDIDO: `strings` do bluez 5.86 tem `%*s/main.conf`, zero `main.conf.d`).
4. **uninstall.sh** — os três removedores (589-662) viraram uma chamada a `remover`. Fecha: UM backup por execução (eram três numa máquina com legados+unificado); `sed '/A/,/B/d'` sem fechamento — que apagava até o fim do arquivo — virou **recusa**; devolve a chave de terceiro neutralizada; e o priming de `sudo` (uninstall.sh:280-288) passou a conhecer a sentinela **unificada**, que faltava — sem isso `--keep-udev` deixava o bloco com `always` para trás.
5. **Poda** — MEDIDO 37 backups / 272 KB, zero poda em install/uninstall/doctor. Retenção **declarada**: 10 mais recentes por mtime (`HEFESTO_BT_BACKUPS_MANTER`), cega a backup que não case `main.conf.bak.hefesto-`.
6. **doctor.sh** — novo `check_bluez_justworks_repairing` (**`[FAIL]`** com `always`; **`[WARN]`** quando `confirm` está ativo com `hefesto-bt-agent.service` fora do ar — a troca passa a depender do agente); e `check_bluez_fastconnectable` parou de atribuir a "terceiro" o bloco que este projeto escreveu.
7. **Mordidas — `tests/unit/test_bluez_config_sh.py`, 30 testes, raiz falsa, sem root, sem tocar `/etc`.** VERIFICADAS arrancando cada cura: tirar o `_skip` do awk → 9 vermelhos; tirar a neutralização → 1; voltar o `if/elif` → 2 (`test_dropin_presente_nao_deixa_always_no_main_conf`); backup antes do `cmp` → 3.
8. Cobrem exatamente o pedido: valor inseguro preexistente vira `confirm`; idempotência (3 execuções byte-idênticas, sem backup novo, sem bloco duplicado); `remover` devolve o arquivo **byte a byte** ao original; drop-in escrito e removido; faixa sem fechamento não come o resto; poda não toca backup alheio; `verificar` não escreve nada.
9. **Prova ao vivo, só leitura, sem escrever em `/etc`:** `HEFESTO_BT_SUDO= bash scripts/bluez_config.sh verificar` na máquina dela devolve `JustWorksRepairing: always`, `backups-hefesto: 37`, `veredito: INSEGURO`, rc=1 — o detector que não existia acusa o defeito real.
10. **Portões atualizados** — `test_plataforma_wiring.py` e `test_bt_resilience_assets.py` retargetados para o dono novo **mais** o contrato novo (install chama `aplicar`, uninstall chama `remover`); `scripts/check_packaging_parity.sh` ganhou a seção `assets/bluetooth × bluez_config.sh` (antes `grep -n bluetooth` no arquivo dava zero).
11. **Documentado** — nota datada de 06/08/2026 em `docs/process/sprints/2026-08-04-RADIO-ABERTO-01-*.md` (a E1 estava escrita e não chegava à máquina; a caixa "PRECISÃO ANTES DE TUDO" de 04/08 olhou `main.conf.d`, que **não existe**, numa máquina que só usa o outro caminho; nova linha E1-bis) + linha no `CHANGELOG.md`. Dívidas registradas com número: `assets/bluetooth/` não viaja em `.deb`/`.rpm`/`PKGBUILD`/flatpak; e o colapso de 404→3 linhas do `main.conf` em 22/07, fora de qualquer execução do install (SUSPEITA COM MECANISMO).
12. **Portões, todos verdes:** `pytest` **7119 passed, 1 skipped** (base 7087+1: +30 da bancada, +2 de retarget/parametrize); `ruff check src/ tests/`; `mypy` 163 arquivos; acentuação, glifos, referências; `check_anonymity.sh`; `check_packaging_parity.sh`; `check_test_data.sh`; `check_version_consistency.py`; `bash -n` nos cinco shell tocados. **Nada commitado**; `install.sh`/`uninstall.sh` nunca foram executados contra o sistema; `bluetoothd` intocado.

### placar

[
  {
    "desenho": "desenho-pelo-dado",
    "media": 7.333333333333333
  },
  {
    "desenho": "desenho-minimo",
    "media": 7
  },
  {
    "desenho": "desenho-pela-duvida-dela",
    "media": 6
  }
]

### verificacoes

[
  {
    "aprovado": false,
    "veredito": "A CURA CENTRAL RESISTE: provei com o próprio parser do bluetoothd (GLib 2.80 GKeyFile, o mesmo que o bluez 5.86-0ubuntu0.1~hefesto24.04.3 desta máquina usa) que, depois de `aplicar`, o main.conf resultante devolve JustWorksRepairing='confirm' em TODOS os casos que construí: bloco antigo do hefesto com `always` (o caso real dela), chave solta fora do bloco, chave duplicada, com tabs, com `;` no fim, com main.conf.d presente, e blocos legados de antes de 21/07. As formas que o awk NÃO neutraliza (JUSTWORKSREPAIRING=, justworksrepairing=) são MEDIDO-inertes: o GKeyFile é sensível a caixa e o bluez ignora as duas. Chave comentada fica intacta. Sentinela sem fechamento vira recusa honesta (rc=1, arquivo intocado) nos dois modos. O ciclo aplicar+remover no caminho normal devolve o arquivo ao original e volta ao default embutido do bluez (`never`, documentado em /etc/bluetooth/main.conf.dpkg-dist:103) — ou seja, MAIS estrito que `confirm`, não menos. A bancada MORDE: arranquei o tratamento dos blocos legados e 1 teste ficou vermelho. NÃO APROVO por três caminhos, todos reproduzidos: (1) `./install.sh --no-udev` pula a correção inteira SEM UMA PALAVRA — na máquina dela o `always` sobrevive ao install; o buraco espelhado do uninstall (--keep-udev) foi fechado neste mesmo diff, o do install não; (2) o `remover` re-arma JustWorksRepairing=always EM SILÊNCIO, enquanto o `aplicar` grita ATENÇÃO — a assimetria exata que a sprint existe para matar; (3) a poda apaga, na próxima execução do install na máquina dela, 28 backups, incluindo todos os anteriores ao colapso de 22/07 que a própria entrega registra como suspeita ABERTA. Nenhum dos três é o defeito original de volta; os três são consequências novas desta entrega.",
    "achados": [
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/install.sh:1351-1396",
        "o_que": "`./install.sh --no-udev` pula a cura do BlueZ inteira e não diz nada. O passo 3d é gateado por `if [[ \"${SKIP_UDEV}\" -eq 0 ]] && command -v sudo ...` e NÃO tem `else` (o `fi` de 1283 é seguido direto pelo comentário do 3d-bis). Com a flag, `step \"3d\"` nem imprime — ao contrário do 3d-bis (linhas 1297-1298), que anuncia `pulado (--no-udev)`. O eixo das flags foi considerado só de um lado: o buraco espelhado do uninstall (`--keep-udev` não primava sudo pela sentinela unificada) FOI fechado neste mesmo diff, em uninstall.sh:291-293. O texto de cura do detector novo (scripts/doctor.sh, check_bluez_justworks_repairing) diz `Cura: rode ./install.sh`, sem ressalva.",
        "prova": "MEDIDO por leitura das linhas exatas 1238 e 1279-1283 de install.sh: extraí o intervalo 1235-1285 e conferi a estrutura if/else/fi — há `else` em 1242 e em 1247, nenhum para o gate de 1238. Não executei install.sh contra o sistema, por regra da casa."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh — _remover (devolução da marca) versus _aplicar (bloco ATENÇÃO)",
        "o_que": "O `remover` devolve JustWorksRepairing=always ao estado ATIVO sem emitir uma linha sequer de aviso. O `_aplicar` tem o reconhecimento em voz alta (`ATENÇÃO: ... ativo fora do bloco hefesto`); o `_remover` não tem equivalente nenhum — imprime só `main.conf reescrito (backup: ...)` e `(vale no próximo boot/restart)`. É defensável como política (devolver a config de terceiro), mas o comentário do próprio script diz que correção silenciosa foi o que deixou o `always` viver quatro dias; a operação inversa continua muda exatamente sobre o valor que a sprint classifica como injeção de teclas.",
        "prova": "MEDIDO em raiz falsa (HEFESTO_BT_ETC + HEFESTO_BT_SUDO vazio). Entrada `[General]\\nName = BlueZ\\nJustWorksRepairing=always\\n`. O `aplicar` imprime `ATENÇÃO: JustWorksRepairing=always ativo fora do bloco hefesto`. O `remover` imprime apenas `main.conf reescrito (backup: ...)` e `(vale no próximo boot...)`. O arquivo final volta a JustWorksRepairing=always — confirmado pelo GKeyFile (GLib 2.80): 'always'. Nenhum teste da bancada cobre a mensagem do `remover`."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:191 (_podar_backups, retenção 10 por mtime)",
        "o_que": "A poda apaga o MAIS ANTIGO, que é justamente o mais próximo do original pré-hefesto — e, na máquina dela, apaga a evidência de uma investigação que esta mesma entrega registra como ABERTA (o colapso de 404 para 3 linhas do main.conf em 22/07, item 11 do relatório, grau SUSPEITA COM MECANISMO). Some tudo que é anterior ao colapso e que carrega a linha do tempo de qual execução do install/uninstall escreveu o quê. O ganho é da ordem de 100 KB. Colide com a regra da casa 'não se apaga decisão medida'. Atenuante MEDIDO: main.conf.bak.claude-1784689791 (16176 B, de terceiro) e main.conf.dpkg-dist sobrevivem, então o CONTEÚDO pré-colapso não some por completo — só a série hefesto.",
        "prova": "MEDIDO: repliquei em raiz falsa a população real de /etc/bluetooth (38 arquivos main.conf.bak.*, nomes + mtimes + tamanhos via `find -printf '%T@\\t%s\\t%f'` e `touch -d @ts`) e rodei `aplicar`. Saída: `poda: 28 backup(s) antigo(s) do hefesto removido(s)`. A lista de apagados inclui main.conf.bak.hefesto-1784487794 (13920 B, 19/07), -1784596506 (14791 B), -1784645908, -1784650427, -1784672963 e os quatro `uninstall-` de 13-15 KB, todos anteriores ao colapso. Sobrevivem 10 mais o novo, e o main.conf.bak.claude-* (corretamente intocado)."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh — _remover, awk `index($0, MARCA) == 1 { print substr(...) }`",
        "o_que": "Esta é a única resposta SIM à pergunta 'o uninstall pode deixar a máquina MENOS segura que antes de instalar'. A devolução da marca é incondicional: qualquer linha que COMECE com `#hefesto-desativou# ` é reativada, sem checar se o `aplicar` foi quem a escreveu nem qual valor ela carrega. Um main.conf que chegue ao install já com essa linha (inerte, um comentário) sai do ciclo install+uninstall com a chave ATIVA. A marca é fixa, pública e documentada no próprio script. A pré-condição é incomum (nenhum `aplicar` cria a marca sem que a chave estivesse ativa antes) e quem escreve em /etc/bluetooth já é root — por isso baixa, não alta.",
        "prova": "MEDIDO em raiz falsa. Original: `[General]\\nName = BlueZ\\n#hefesto-desativou# JustWorksRepairing=always\\n` (chave INERTE — GKeyFile devolve ausente). `aplicar` seguido de `remover` produz `JustWorksRepairing=always` na coluna 1, e o GKeyFile (GLib 2.80) lê 'always'. Antes do install o efetivo era o default embutido `never` (/etc/bluetooth/main.conf.dpkg-dist:103); depois do uninstall é `always`."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh — _aplicar, ramo `else _diz \"sem ${MAIN_CONF} (BlueZ ausente?)\"` e o `if [[ \"${rc}\" -eq 0 ]]` final",
        "o_que": "Com /etc/bluetooth existente e main.conf AUSENTE, o `aplicar` não escreve nada e mesmo assim imprime `JustWorksRepairing=confirm + FastConnectable=true garantidos`, com rc=0. O comentário imediatamente acima dessa linha afirma o contrário: 'A frase da garantia só sai quando a garantia EXISTE'. É a mesma classe de defeito de comunicação que a sprint existe para matar, em forma branda. Direção segura (sem main.conf o bluez usa o default `never`), e por isso baixa — mas nenhum teste cobre: test_sem_bluez_nada_explode só afirma rc==0, não olha o stdout.",
        "prova": "MEDIDO em raiz falsa: diretório criado vazio, sem main.conf e sem main.conf.d. Saída literal: `sem <raiz>/main.conf (BlueZ ausente?) — bloco não apensado` seguido de `JustWorksRepairing=confirm + FastConnectable=true garantidos — VALEM NO PRÓXIMO BOOT`, rc=0. Mesmo comportamento com main.conf.d presente e main.conf ausente."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/check_packaging_parity.sh:540-542",
        "o_que": "As duas linhas que dizem checar que o `bluez_config.sh limpa o bloco legado FastConnectable/JustWorksRepairing` são vácuas: `grep -qF \"FastConnectable\" scripts/bluez_config.sh` é satisfeito pelo nome da chave na regex de neutralização, que existe independentemente do tratamento dos legados. O portão passa com o tratamento legado inteiramente arrancado. Não é regressão de segurança — a bancada nova cobre o comportamento de verdade —, mas é uma linha que LÊ como proteção e não protege, num arquivo cuja mensagem de falha invoca o defeito de 06/08.",
        "prova": "MEDIDO por mutação: troquei _RE_ABRE/_RE_FECHA por `'^# >>> hefesto bluetooth >>>'` e `'^# <<< hefesto bluetooth <<<'`, removendo todo o tratamento dos dois blocos legados. `bash scripts/check_packaging_parity.sh` continuou imprimindo `[ OK ] config do BlueZ: dono único, chamado nos dois lados, com detector no doctor` e `paridade de empacotamento OK`. O pytest, esse sim, ficou vermelho: 1 failed (test_blocos_legados_de_instalacao_antiga_tambem_saem), 29 passed. Arquivo restaurado; md5sum da árvore igual ao `git show :scripts/bluez_config.sh`."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh — _despir_main_conf, regra `/^[[:space:]]*$/ { _b++; next }` (e o relatório, item 8)",
        "o_que": "A afirmação de que o `remover` devolve o arquivo 'byte a byte ao original' tem exceção não declarada: as linhas em branco do FIM do arquivo original são descartadas. É consequência deliberada da cura do BUG-INSTALL-MAIN-CONF-CRESCE-01, mas a invariante é enunciada sem a ressalva, e o teste que a defende (test_remover_devolve_o_arquivo_sem_chave_nossa) usa um original que não termina em branco — então não pode acusar.",
        "prova": "MEDIDO: original `[General]\\nName = BlueZ\\n\\n\\n` (duas linhas em branco no fim). Após aplicar+remover, o `cmp` diverge: as duas linhas em branco finais somem (diff 3,4d2). Os demais round-trips que testei (simples, terceiro-never, vazio) voltam idênticos."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh — _valor_ativo, _tem_bloco_nosso e o `grep -qsF \"${MARCA}\"` do _remover",
        "o_que": "Três leituras do main.conf rodam SEM o prefixo `_r` de root, ao contrário de todo o resto do script (awk, cmp, cp, install, rm usam `_r`). Se o main.conf não for legível pelo usuário que invoca (hoje é 644, então não é o caso), o `aplicar` deixa de emitir a ATENÇÃO, o `verificar` reporta 'ausente'/'SEM-BLUEZ' com veredito enganoso, e — o pior dos três — o `_remover` conclui que não há nada nosso e NÃO remove o bloco. Assimetria de privilégio dentro do mesmo script; não é caminho para `always`, é cegueira.",
        "prova": "SUSPEITA COM MECANISMO: leitura do fonte. `_valor_ativo` chama `sed` direto; `_tem_bloco_nosso` chama `grep -qs` direto; o guarda do `_remover` é `_tem_bloco_nosso || grep -qsF \"${MARCA}\" \"${MAIN_CONF}\"`. Todos os outros pontos de acesso ao arquivo passam por `_r`. Não reproduzi com modo restrito porque exigiria chmod em /etc."
      }
    ]
  },
  {
    "achados": [
      {
        "gravidade": "alta",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:191-215 (_podar_backups), chamada em :275 (_aplicar) e :329 (_remover)",
        "o_que": "A poda apaga, na PRIMEIRA execucao de `aplicar` na maquina dela, 27 dos 37 backups — e entre eles estao os dois arquivos que sao a unica prova medida do colapso 404 -> 3 linhas do main.conf, colapso que esta MESMA leva registra como suspeita EM ABERTO, sem cura, no doc de sprint. A retencao por mtime descarta primeiro o que tem mais valor (o estado pre-hefesto e o instante do estrago) e guarda os 10 mais recentes, que na maquina dela sao todos de 11 a 1395 bytes, ou seja, ja pos-colapso. Nao ha aviso previo, nao ha `--dry-run`, nao ha regra de 'o primeiro backup nunca sai' e nao ha teste que trave isso (test_poda_* so conta arquivos). Pior: o caminho que dispara a poda e exatamente o que o doctor novo manda ela rodar (scripts/doctor.sh:1729 diz 'rode ./install.sh ... ou sudo bash scripts/bluez_config.sh aplicar'), entao a destruicao acontece no ato de seguir o conselho da propria ferramenta. Isso colide com a regra da casa 'nao se apaga decisao medida'.",
        "prova": "MEDIDO, simulacao SO-LEITURA do pipeline exato do script contra /etc/bluetooth (nenhum rm executado): `find /etc/bluetooth -maxdepth 1 -type f -name 'main.conf.bak.hefesto-*' -printf '%T@\\t%p\\n' | sort -rn -k1,1 -k2,2 | tail -n +11 | cut -f2-` devolve 27 caminhos de 37. Entre eles: main.conf.bak.hefesto-1784672963 (404 linhas, 14797 bytes, 21/07 19:29) e main.conf.bak.hefesto-1784694261 (3 linhas, 59 bytes, 22/07 01:24) — exatamente os dois pontos '404 linhas em 21/07 19:29' e '3 linhas em 22/07 01:24' citados em docs/process/sprints/2026-08-04-RADIO-ABERTO-01-*.md na secao 'O que continua ABERTO'. So sobrevive o de 426 linhas porque tem prefixo alheio (main.conf.bak.claude-1784689791). REPRODUZIDO em bancada com raiz falsa (scratchpad/bancada/I e /J): o backup mais antigo, marcado como unica copia, foi apagado e sobraram 10."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:172-190 (_gravar_se_mudou, linhas 179-180: `_r cp` + `_r install -m644`)",
        "o_que": "A reescrita do conffile NAO e atomica: `install -m644 tmp /etc/bluetooth/main.conf` escreve NO LUGAR (mesmo inode, O_TRUNC). Disco cheio, queda de energia ou kill no meio deixa o main.conf DELA truncado. E o estado resultante e um beco sem saida: como o bloco fica no fim do arquivo, o corte quase sempre cai dentro dele e o arquivo passa a ter sentinela de abertura sem fechamento — a partir dai `aplicar` E `remover` RECUSAM para sempre (:254 e :303), e o unico conselho automatizado (doctor: 'rode ./install.sh') nao pode funcionar. A cura e uma linha: escrever num temporario no MESMO diretorio e `mv` (rename atomico), em vez de mktemp em /tmp + install.",
        "prova": "MEDIDO o comportamento do install(1): dest de 3000 bytes, `( ulimit -f 2; install -m644 src dest )` deixa dest com 1024 bytes e o MESMO inode (3279442 antes e depois) — trunca no lugar, nao substitui. REPRODUZIDO ponta a ponta na bancada (scratchpad/bancada/J) com um `install` de PATH que escreve metade e falha: main.conf ficou com 600 bytes terminando em '# FastConnectable=true — page scan agressivo: o botao PS reconecta ' (sentinela aberta, sem fechamento). Em seguida (scratchpad/bancada/H), com esse arquivo: `aplicar` rc=1 'sentinela de abertura sem fechamento', `remover` rc=1 idem, `verificar` diz 'JustWorksRepairing: ausente / veredito: INSEGURO'."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:275 e :329 (_podar_backups chamada ANTES do teste de rc)",
        "o_que": "A poda roda mesmo quando a cura FALHOU e mesmo quando o arquivo nao foi tocado. Ou seja: no exato cenario em que os backups sao o que resta (escrita abortada, main.conf truncado, sudo negado, /etc somente-leitura), o script apaga os backups mais antigos e so DEPOIS anuncia que nao conseguiu garantir nada. Ordem invertida: podar e uma operacao destrutiva e deveria acontecer so depois de um sucesso confirmado, se e que deve acontecer sem consentimento.",
        "prova": "REPRODUZIDO (scratchpad/bancada/J): saida na ordem 'nao consegui reescrever ... / poda: 3 backup(s) antigo(s) do hefesto removido(s) / config do BlueZ NAO ficou garantida', rc=1, com o main.conf truncado em 600 bytes E o backup mais antigo (main.conf.bak.hefesto-1700000000, rotulado 'UNICO BACKUP BOM') apagado de fato. Repetido com /etc falso somente-leitura (bancada/D): a poda tambem roda depois da falha."
      },
      {
        "gravidade": "media",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:149-171 (_despir_main_conf, regras `$0 ~ ABRE {_skip=1}` e `_skip {next}`)",
        "o_que": "Qualquer coisa que a pessoa tenha escrito DENTRO do bloco de sentinelas e apagada em silencio. O reconhecimento que a leva orgulhosamente adicionou cobre so o JustWorksRepairing divergente (:238-244); linhas que ela editou ali dentro (por exemplo ControllerMode ou MultiProfile, chaves que gente poe no main.conf para fone e headset funcionarem) somem sem uma palavra na tela. E o bloco convida a isso: o proprio texto dele diz que e o bloco gerenciado do main.conf. A recuperacao existe so no backup — e o backup expira pela poda (achado 1): com 2 backups por ciclo install+uninstall, a retencao de 10 cobre cerca de 5 ciclos.",
        "prova": "REPRODUZIDO (scratchpad/bancada/A): main.conf com 'ControllerMode = bredr' e 'MultiProfile = multiple' dentro do bloco, mais o comentario '# --- editado por mim em 03/08: sem isto o meu fone nao conecta ---'. Depois de `aplicar`: rc=0, `grep -c ControllerMode` = 0, e a unica mensagem na tela foi sobre o JustWorksRepairing. Nenhum teste da bancada nova cobre esse caso."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:257-260 e :279-281",
        "o_que": "Com /etc/bluetooth presente, sem main.conf e sem main.conf.d, o `aplicar` nao escreve NADA e mesmo assim sai rc=0 anunciando 'JustWorksRepairing=confirm + FastConnectable=true garantidos'. E o mesmo padrao de anunciar garantia inexistente que motivou a leva (o comentario em :277-279 promete o contrario). O risco de seguranca e pequeno (sem main.conf o BlueZ cai no default), mas a frase e falsa e o install repassa o rc=0 como sucesso.",
        "prova": "REPRODUZIDO (scratchpad/bancada/B): diretorio criado vazio; saida foi 'sem .../main.conf (BlueZ ausente?) — bloco nao apensado' seguida de 'JustWorksRepairing=confirm + FastConnectable=true garantidos', rc=0, e `ls` mostra o diretorio ainda vazio."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:210-212",
        "o_que": "A poda ANUNCIA remocao que pode nao ter acontecido: `_r rm -f ... || true` engole a falha e o `_diz` de :212 imprime a contagem incondicionalmente. Quem le o log acredita que os backups sairam quando eles continuam la (ou o contrario, em caso de remocao parcial).",
        "prova": "REPRODUZIDO (scratchpad/bancada/D, diretorio somente-leitura): saida 'poda: 6 backup(s) antigo(s) do hefesto removido(s)' e, na sequencia, `ls` com os 16 arquivos intactos."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:250-256 (else de `if _despir_main_conf`) e :238 (_valor_ativo sob `set -o pipefail`)",
        "o_que": "Dois diagnosticos errados no caminho de erro. (a) QUALQUER saida nao-zero do awk vira a mensagem 'sentinela de abertura sem fechamento ... conserte a mao' — inclusive falha de leitura ou falta de espaco no temporario; ela e mandada procurar um defeito que nao existe. (b) Se o main.conf estiver ilegivel, o pipefail do `_valor_ativo` mata o script em :238 com rc=2 e ZERO linhas de saida, nem em stderr; o install so imprime o warn generico.",
        "prova": "REPRODUZIDO (scratchpad/bancada/E): `chmod 000 main.conf` e `aplicar` -> rc=2, saida completamente vazia. E a mensagem de (a) e a unica que o ramo `else` sabe emitir (leitura de :250-256)."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:334 (comentario) versus /mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/doctor.sh:1691-1737",
        "o_que": "Afirmacao falsa no codigo: 'verificar — so leitura, e e o que o doctor consome'. O doctor NAO chama o bluez_config.sh; ele reimplementa o mesmo `sed` inline. Sao dois lugares declarando a mesma regra, que e a classe de defeito que esta leva veio fechar, e o portao novo (check_packaging_parity.sh) so exige `grep -qF JustWorksRepairing scripts/doctor.sh`, o que a duplicata satisfaz.",
        "prova": "MEDIDO: `grep -n bluez_config scripts/doctor.sh` devolve apenas a linha 1729, dentro de uma STRING de conselho ('sudo bash scripts/bluez_config.sh aplicar'); nenhuma chamada. O `sed -n -E 's/^[[:space:]]*JustWorksRepairing...'` aparece identico em bluez_config.sh:140-141 e doctor.sh:1712-1713."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:317-318 (`> \"${tmp}.devolvido\"` e `mv`)",
        "o_que": "O segundo temporario nao vem de mktemp: e o nome do primeiro com sufixo fixo, criado por redirecionamento (sem O_EXCL) num diretorio compartilhado. Rodar o `remover` como root e caminho DOCUMENTADO — uninstall.sh:634 imprime 'rode: sudo bash .../bluez_config.sh remover' e doctor.sh:1729 sugere o `aplicar` com sudo — e nesse modo a criacao acontece como root sobre um caminho que qualquer conta local pode pre-criar como link simbolico (o nome do mktemp e visivel em /tmp). Numa maquina de um usuario so o risco e teorico; a cura e um segundo mktemp.",
        "prova": "SUSPEITA COM MECANISMO (leitura fecha): `tmp=\"$(mktemp)\"` em :306, escrita em `\"${tmp}.devolvido\"` em :317 sem O_EXCL, e /tmp e 1777 com listagem permitida; o redirecionamento e feito pelo shell, que e root quando o script inteiro roda sob sudo."
      },
      {
        "gravidade": "baixa",
        "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:161-165 (regra de neutralizacao) e :238-244 (aviso)",
        "o_que": "A neutralizacao trata igual valor perigoso e valor MAIS restritivo que o nosso, e so o JustWorksRepairing ganha aviso. Quem tiver escolhido `FastConnectable = false` de proposito tem a escolha desativada com `#hefesto-desativou# ` sem uma unica linha na tela; quem tiver escolhido `JustWorksRepairing = never` (mais seguro que o nosso `confirm`) e rebaixado, ao menos com aviso.",
        "prova": "REPRODUZIDO (scratchpad/bancada/K): main.conf com 'FastConnectable = false' e um comentario dela; depois de `aplicar` a linha virou '#hefesto-desativou# FastConnectable = false' e a saida nao menciona FastConnectable em nenhum momento. E (bancada/F) com 'JustWorksRepairing = never' a saida foi 'ATENCAO: JustWorksRepairing=never ativo fora do bloco hefesto — neutralizando e assumindo confirm'."
      }
    ],
    "aprovado": false,
    "veredito": "REFUTADO como seguro para o arquivo dela — nao pela cura em si, que e boa, mas pela poda e pela escrita nao-atomica.\n\nO QUE RESISTIU AO ATAQUE (e resistiu bem, tudo MEDIDO em bancada de raiz falsa, nada contra /etc):\n- em operacao normal nenhum caminho corrompe nem trunca o main.conf: bloco antigo com `always` vira `confirm`, tres execucoes dao arquivo byte-identico sem backup novo, `remover` devolve o original byte a byte, chave de terceiro volta ao estado ativo;\n- a RECUSA diante de sentinela de abertura sem fechamento e a decisao certa, e vale para os dois modos — o `sed '/A/,/B/d'` antigo comia ate o fim do arquivo;\n- ha backup antes de toda escrita do main.conf, e o `cmp` antes do backup faz o no-op ser honesto (bancada/A: um backup, uma reescrita);\n- a bancada NAO escreve fora dela: `ls -la --time-style=full-iso /etc/bluetooth | md5sum` deu o MESMO hash antes e depois de rodar os tres arquivos de teste tocados (106 testes), e o gate estrutural test_todo_caminho_deriva_da_raiz_configuravel impede literal de /etc no script;\n- /etc/bluetooth continua intocado por esta sessao (main.conf com mtime de 02/08 02:33, 1394 bytes) — o relato de que install/uninstall nunca rodaram contra o sistema confere;\n- portoes reproduzidos: `pytest` 7119 passed, 1 skipped (exatamente o numero relatado) e `check_packaging_parity.sh` OK.\n\nO QUE REFUTA:\n1. (alta) A poda apaga 27 dos 37 backups na primeira execucao, e leva junto os arquivos de 404 e de 3 linhas — os dois pontos de medicao do colapso do main.conf que ESTA MESMA leva registra como suspeita em aberto e sem cura. A destruicao e disparada pelo conselho do proprio doctor novo. Enquanto a poda entra assim, a leva apaga prova medida no ato de curar.\n2. (media) A escrita usa `install` no lugar, que trunca (inode preservado, MEDIDO): disco cheio ou queda de energia deixam o main.conf cortado, e o corte cai dentro do bloco, o que trava `aplicar` e `remover` para sempre na recusa — com o doctor mandando rodar exatamente o que nao pode funcionar. Reproduzi o encalhe ponta a ponta.\n3. (media) A poda roda ANTES do teste de rc: no cenario em que os backups sao a ultima linha de defesa, ela apaga os mais antigos e so depois anuncia que nao curou nada.\n4. (media) Conteudo que ela tenha editado dentro do bloco desaparece sem uma palavra na tela, e a janela de recuperacao expira com a poda.\n\nNada disso pede reescrever a entrega: sao tres ajustes locais (temporario no mesmo diretorio mais `mv`; poda opt-in, so depois de sucesso, e com o backup mais antigo protegido; um aviso quando a reescrita descarta linha ativa que nao e nossa) mais um teste por defeito. Enquanto a poda existir na forma de hoje, a recomendacao concreta e nao rodar `install.sh` nesta maquina antes de copiar /etc/bluetooth/main.conf.bak.hefesto-1784672963 e -1784694261 para fora de /etc."
  }
]

### achadosAltos

[
  {
    "gravidade": "alta",
    "onde": "/mnt/Apate/Desenvolvimento/hefesto-dualsense4unix/scripts/bluez_config.sh:191-215 (_podar_backups), chamada em :275 (_aplicar) e :329 (_remover)",
    "o_que": "A poda apaga, na PRIMEIRA execucao de `aplicar` na maquina dela, 27 dos 37 backups — e entre eles estao os dois arquivos que sao a unica prova medida do colapso 404 -> 3 linhas do main.conf, colapso que esta MESMA leva registra como suspeita EM ABERTO, sem cura, no doc de sprint. A retencao por mtime descarta primeiro o que tem mais valor (o estado pre-hefesto e o instante do estrago) e guarda os 10 mais recentes, que na maquina dela sao todos de 11 a 1395 bytes, ou seja, ja pos-colapso. Nao ha aviso previo, nao ha `--dry-run`, nao ha regra de 'o primeiro backup nunca sai' e nao ha teste que trave isso (test_poda_* so conta arquivos). Pior: o caminho que dispara a poda e exatamente o que o doctor novo manda ela rodar (scripts/doctor.sh:1729 diz 'rode ./install.sh ... ou sudo bash scripts/bluez_config.sh aplicar'), entao a destruicao acontece no ato de seguir o conselho da propria ferramenta. Isso colide com a regra da casa 'nao se apaga decisao medida'.",
    "prova": "MEDIDO, simulacao SO-LEITURA do pipeline exato do script contra /etc/bluetooth (nenhum rm executado): `find /etc/bluetooth -maxdepth 1 -type f -name 'main.conf.bak.hefesto-*' -printf '%T@\\t%p\\n' | sort -rn -k1,1 -k2,2 | tail -n +11 | cut -f2-` devolve 27 caminhos de 37. Entre eles: main.conf.bak.hefesto-1784672963 (404 linhas, 14797 bytes, 21/07 19:29) e main.conf.bak.hefesto-1784694261 (3 linhas, 59 bytes, 22/07 01:24) — exatamente os dois pontos '404 linhas em 21/07 19:29' e '3 linhas em 22/07 01:24' citados em docs/process/sprints/2026-08-04-RADIO-ABERTO-01-*.md na secao 'O que continua ABERTO'. So sobrevive o de 426 linhas porque tem prefixo alheio (main.conf.bak.claude-1784689791). REPRODUZIDO em bancada com raiz falsa (scratchpad/bancada/I e /J): o backup mais antigo, marcado como unica copia, foi apagado e sobraram 10."
  }
]

### reprovou

true


## LOGS

desenho-pelo-dado: 7.3
desenho-minimo: 7.0
desenho-pela-duvida-dela: 6.0
verificacao: 2 lentes, 2 reprovaram, 1 achados de gravidade alta
