# Auditoria geral do projeto — o que treze agentes mediram em 31/07/2026

- **Pedido dela, literal:** *"Estude e audite o projeto, sua documentação, suas
  regras e afins. Use agentes"* — e, no meio da rodada: *"veja o que ficou pelo
  caminho em termos de sprints e afins também"*
- **Medido sobre:** `HEAD 7bd0cb7`, branch `restauro/inicio-da-sessao`, com a
  **v0.4.0 publicada** em 30/07 e o daemon **vivo** na máquina dela
- **Método:** nove auditores particionados por área, em paralelo, **mais quatro
  verificadores independentes com poder de reprovar** — o padrão que em 29/07
  pegou o `--default-branch` inexistente antes de nenhuma release publicar
- **Custo:** 13 agentes, 682 chamadas de ferramenta, 1,86 milhão de tokens,
  24 minutos de relógio
- **Regra desta rodada:** somente leitura. Nenhum arquivo do repositório foi
  alterado durante a medição, nenhum `systemctl`, nenhum script com `--fix`.
  Sudo só para ler (`/sys`, `systemctl cat`, `dkms status`, `getfacl`, journal)

## O que o verificador mudou — e por que ele existe

Dos oito achados que os auditores classificaram como graves, o verificador
independente **confirmou cinco e reenquadrou três**. Nenhum dos três
reenquadrados era invenção: eram fatos reais com moldura errada. Vale registrar
os três, porque é o tipo de erro que a casa comete quando tem pressa.

1. **O `display_authority`.** O auditor disse "cai com o jogo aberto" e citou
   seis transições do journal. O verificador foi atrás do contexto de cada uma:
   em duas o marcador do wrapper estava fresco (o que implica processo do jogo
   **morto**, não vivo), e três vêm logo depois de `steam_input_excecao_encerrada`
   seguidas de horas sem nenhuma evidência de jogo — ou seja, **fechamento real**,
   que é o comportamento projetado. O falso negativo existe, mas o cenário é mais
   estreito do que o alegado. Virou média, com uma entrega nova: reproduzir a
   queda com jogo comprovadamente vivo, que **ninguém nunca mediu**.
2. **O NOTICE e os drivers GPL.** O fato é verdadeiro e grave à primeira vista —
   o projeto se declara MIT e embarca três drivers de kernel GPL-2.0 em
   `assets/dkms/`. O verificador encontrou o que o auditor não procurou: a sprint
   **CR-05**, aberta em 25/07, já diagnostica exatamente isso, e o vetor real de
   redistribuição é o tarball mais o instalador — o `PKGBUILD` **não** empacota
   `assets/dkms`, e `grep dkms` nos workflows devolve vazio. Não é achado novo, é
   pendência conhecida que atravessou uma release.
3. **A entrega 3 da PERFIL-JOGO-01.** O auditor disse que ela mira metade do
   alvo. O verificador leu a sprint e mostrou que ela **já cita as duas portas do
   cadeado por extenso**, com data de nascimento e commit. Quem errou foi o
   índice de 30/07, que resume a exceção como se fosse uma porta só — e ainda
   atribui o furo por título ao predicado errado (`perfil_e_regra_de_jogo`
   **recusa** título de propósito; quem aceita é a segunda porta). A conclusão
   operacional do índice continua verdadeira; o mecanismo descrito, não.

O verificador também **matou uma lenda** por medição própria: a suspeita de que
as branches antigas do `origin`, não alcançadas pela purga de 20/07, ainda
exporiam MACs reais. Varridos os 256 commits exclusivos das linhagens
pré-reescrita: o único padrão de MAC é `AA:BB:CC:DD:EE:FF`, exemplo didático.
**Não repetir esta investigação.**

### E o reenquadramento do `display_authority` rendeu mais do que corrigir a moldura

Ao escrever a sprint que nasceu desse achado, a máquina dela entrou sozinha no
cenário — **PRAGMATA.exe vivo há 20 minutos** durante a redação — e a medição ao
vivo achou o que nenhuma das duas rodadas anteriores tinha visto:

**O jogo dela não passa pelo wrapper do Hefesto.** A opção de lançamento é
`VKD3D_CONFIG=no_upload_hvv %command%`, e `~/.local/state/hefesto-dualsense4unix/launch_env/`
não tem `last_run` nem `last_exit` — só os quatro `.env`. Ou seja: **a evidência
nº 3 do sinal de jogo está estruturalmente ausente do jeito que ela joga.** Não é
marcador expirado; é marcador que nunca foi escrito.

Somado ao fato de que a evidência nº 2 (regra de perfil) só recebe `wm_class` e
os perfis dela casam por título, sobra **uma evidência só**: enxergar a janela. É
ponto único de falha, e o gate de foco do `xlib` — 13 episódios de cegueira
nessa mesma sessão — é exatamente quem o derruba.

O achado original apontava o sintoma certo pelo mecanismo errado. Foi preciso o
verificador para tirar a moldura falsa **e** a redação da sprint para achar a
verdadeira.

---

## O retrato em uma tela

| Área | Estado | O que decide a leitura |
|---|---|---|
| Testes e portões | **Verde de verdade** | 6097 passam, 0 falham, 0 skip, 124,62s; os 7 portões saem exit 0 |
| Broker root e emulação | **Sólido** | validação por `HID_ID` do pai confirmada; traversal, symlink e TOCTOU fechados e testados |
| CI e release | **Motor bom, metadado mentindo** | matriz 3.10/3.11/3.12, guarda fail-closed que recusou 4 runs vermelhos; mas o AppStream publicado conta a versão errada |
| Instalação | **Espelho do repo** | 14 regras udev, 7 units, 7 scripts e 4 confs byte a byte idênticos ao que roda |
| Núcleo do daemon | **Funciona, e é grande demais** | `Daemon` com ~95 métodos e acoplamento de volta por `getattr` |
| Janela | **Cinco defeitos reais** | do latch que para de reconciliar ao botão morto em pacote |
| Documentação | **É a área mais fraca** | 7 das 9 contradições de 26/07 persistem, e nenhuma das 7 entregas foi executada |
| Árvore do git | **Duas armadilhas armadas** | a `main` local aponta para o repositório de outra pessoa |
| Sprints | **41 de 50 cabeçalhos mentem** | e 13 identificadores vivem sem documento |

---

# O que foi CONFIRMADO como grave

Cinco achados sobreviveram ao verificador com prova reproduzida do zero.

## 1. O `install.sh` que roda tem quatro portões sempre-falsos

`grep -n -- '-w /sys/module' install.sh` devolve as linhas **620, 686, 696 e
700**. Cada portão guarda um `sudo tee`, e `ls -l /sys/module/hid_playstation/parameters/`
mostra `root:root 0644` — para o install rodado do jeito certo (**sem** sudo,
que é a regra desta casa), `-w` é **sempre falso**. Consequência: o ciclo
`uninstall` mais `install` desliga em silêncio as curas de conexão do 8BitDo no
cabo, do handshake do clone e do reset do dongle, até o próximo boot.

A correção existe e está pronta — `9c944a8`, com `-w` virando `-e`, o rearme
explícito de `usb_cmd_pad_to_report`, `usb_send_conn_status`, `usb_probe_degrade`
e `hang_reset`, mais dois testes de simetria. Ela vive **só na `main` descartada**:
`git merge-base --is-ancestor 9c944a8 HEAD` reprova.

Estado vivo hoje, medido: `ds4_short_pairing_info=Y`, `ds4_synthetic_mac=Y`,
`feature_retries=2`, `hang_reset=Y` — **rearmadas pelo boot de 31/07**. O defeito
está latente, não ativo. Foi exatamente isto que ela sofreu em 26/07.

**Onde atacar:** a entrega E2 da ÁRVORE-DIVERGENTE-01 já está especificada.

## 2. A `main` local aponta para o repositório do André

`git config branch.main.remote` devolve **`upstream`**, e `upstream` é
`https://github.com/AndreBFarias/hefesto-dualsense4unix.git`. A prova mais
direta, que o verificador obteve: `git rev-parse --abbrev-ref 'main@{push}'`
resolve **`upstream/main`**, com `push.default`, `remote.pushDefault` e
`branch.main.pushremote` todos vazios.

Ou seja: **um `git push` estando na `main` mira o repositório de outra pessoa.**
E `git checkout main` nesta máquina entrega uma árvore 25 commits atrás
(`2d8527a`, de 26/07).

A tag `arquivo/main-antes-da-v030` resolve para **o mesmo commit** que a `main`
local — então mover ou apagar a ref não perde histórico nenhum. É a decisão E0 do
documento ÁRVORE-DIVERGENTE-01, e é dela.

## 3. O primeiro exemplo do guia de perfis não funciona

`docs/usage/creating-profiles.md:19` ensina `"left": {"mode": "Medium", "params": []}`.
`profiles/schema.py:163-168` rejeita modo fora de `PRESET_FACTORIES` com
`ValueError`. O verificador mediu `PRESET_FACTORIES` com o venv do projeto:
**19 nomes, e `Medium` não é um deles**. Depois colou o JSON exato do exemplo em
`Profile.model_validate()` e recebeu `ValidationError`.

Quem copia o primeiro exemplo do guia não consegue criar um perfil. É o item 8
da DOC-VERDADE-01, e ele **piorou**: era colisão teórica, virou receita quebrada.

## 4. As duas receitas de ligar plugins estão mortas

`docs/adr/017-plugin-system.md:73-74` ensina duas vias: `config.toml` com
`plugins_enabled = true`, e a variável `HEFESTO_PLUGINS_ENABLED=1`. Medido: o
daemon **não lê arquivo de configuração nenhum** (`daemon/main.py:91-110` só lê
envs, e o próprio código admite em `emulation_actions.py:450`
— `BUG-DAEMON-TOML-DEAD-01`), e a variável real é
`HEFESTO_DUALSENSE4UNIX_PLUGINS_ENABLED` (`plugins.py:194`).

O README documenta a variável **certa**, contradizendo o ADR. E o commit `e96dea8`
corrigiu só a seção "Impacto no código" do arquivo, deixando a seção "Ativação"
errada — o diff começa na linha 117.

## 5. Sete das nove contradições da DOC-VERDADE-01 persistem

Recontadas uma a uma, com prova própria. `git log --since=2026-07-26 -- docs/protocol/`
devolve **vazio**; `ls docs/adr/` devolve 19 arquivos, sem o ADR-020 prometido;
"Nota de verificação" existe só nos ADRs 003, 008 e 016.

Uma foi curada (o glifo do troubleshooting), uma foi parcialmente curada, e
**nenhuma das sete entregas da sprint foi executada**. O pouco que andou veio de
carona de outra leva.

O caso mais instrutivo é o `udp-schema.md:5`, que ainda vende porta configurável
em `daemon.toml`: o texto **foi tocado** para atualizar o caminho do arquivo, e a
ficção ficou. É o pior estado possível — parece revisado.

---

# O que foi medido e está BOM

Registrar o que está de pé importa tanto quanto o defeito, porque impede a
próxima leva de "consertar" o que funciona.

## A suíte inteira rodou, e os números são reais

**6097 passed, 0 failed, 0 skipped, 0 xfail, 5 warnings, em 124,62 segundos**,
na máquina dela, com Python 3.12 e o `.venv` do projeto. Bate exato com o que o
commit `84c0f83` alegava. O README diz 6089 — o emblema é pintado à mão e
defasou oito testes.

Zero skip porque o PyGObject real está presente: os 119 marcadores declarados não
disparam aqui. E **não existe marcador de skip por hardware Bluetooth** — o
buraco de BT não é skip visível, é ausência estrutural de casos.

Os sete portões, rodados direto pelos scripts: `check_anonymity`,
`check_version_consistency` (9 alvos em 0.4.0), `check_packaging_parity`,
`check_test_data`, `validar-acentuacao --all`, `validar-glifos --all` e `ruff` —
**todos exit 0**.

E as duas curas da v0.4.0 escolhidas para prova **mordem**: o gate do R1 é
testado por comportamento (Daemon real, poll loop, par diferencial
suspenso-cala × desktop-emite, esperando por condição em vez de relógio), e o
perfil-nasce-vencendo tem o cálculo testado contra a fixture do disco dela.

## O broker root é sólido — e a regra da casa está confirmada

Socket `0660 root:vitoriamaria` por socket-activation do systemd, medido ao vivo.
`SO_PEERCRED` como barreira autoritativa. E a regra que a casa escreveu está
cumprida: **a validação é pelo `HID_ID` do pai HID imediato**, nunca por
`idVendor` de topologia; o vpad `0df2` é rejeitado explicitamente antes do check
geral.

O auditor testou empiricamente que `canonical_hidraw_base` rejeita
`/dev/../etc/hidraw0`, subdiretório, nome de symlink e nomes não-canônicos. O
TOCTOU e o reuso de minor são fechados com pin por inode (`O_PATH` + `fstat`
cruzado com sysfs) e revalidação por `HIDIOCGRAWINFO` no próprio fd. O binário
instalado é **byte-idêntico** ao do repo.

Um processo local malicioso do mesmo usuário consegue apenas esconder/restaurar/
abrir o DualSense físico — negação de serviço da própria sessão, nunca hidraw
alheio. **Não é escalação de privilégio.**

## A medição pendente do índice de 30/07: resolvida, e a favor

O índice de 30/07 deixou escrito que não conferiu se `player_leds` é retido junto
com `led` quando o portão `_game_wins()` fecha (entrega 2 da PERFIL-JOGO-01).

**É retido.** `backend_pydualsense.py:2780-2785` monta o dicionário `fields` com
`led` **e** `player_leds` pelo mesmo caminho; `:2793-2796` retém os dois no mesmo
`retido.update(fields)`; `:1170-1171` faz o merge da camada `game` inteira, por
campo, simetricamente. E o teste morde:
`test_game_output_replica.py:288` escreve `player_leds` sob autoridade `daemon` e
exige que o hardware **não** seja tocado. 87 testes rodados na vizinhança, todos
verdes.

**A entrega 2 pode sair da lista de pendências.**

## O sistema instalado é espelho do repositório

As 14 regras udev em `/etc/udev/rules.d` (instaladas 30/07 13:03) são byte a byte
idênticas a `assets/`. As 7 units `hefesto-*` mais o drop-in de resiliência,
idênticas a `assets/systemd/` — com o broker renderizado corretamente para uid
1000 e grupo `vitoriamaria`. Os 7 scripts `bt_*` e o broker em `/usr/local/lib`,
idênticos a `scripts/`. Os 4 confs de `modprobe.d` e o `modules-load`, idênticos.
`dkms status` com os três módulos `installed`. `getfacl` de `/dev/uhid` e
`/dev/uinput` com grupo `hefesto` e a ACL dela. `/etc/sudoers.d` **sem resíduo**
de NOPASSWD.

E o desastre histórico está curado: `uninstall.sh --help` sai 0 sem tocar em
nada, e argumento desconhecido aborta com exit 2.

## O guarda de CI funciona, e recusou quatro vezes

O guarda do release pergunta a conclusão do `ci.yml` na **mesma SHA** via API, é
fail-closed em todos os ramos (`release.yml:296-361`), e recusou **quatro runs
vermelhos** da v0.4.0 antes de a release final publicar os seis artefatos. Cinco
testes estruturais travam o desenho.

A premissa que a casa carregava está desatualizada, e é boa notícia: a matriz é
**3.10, 3.11 e 3.12**, e o validador de acentuação trata `FSTRING_MIDDLE`
(`validar-acentuacao.py:619-621`) — **a cegueira a f-string está curada e
travada**. O job "Interface com GTK REAL" existe, prova a typelib **completa**
antes de coletar (a cura da armadilha que derrubava a coleta) e passou no último
run.

---

# O que ficou pelo caminho — a tabela-mestra

Ela pediu isso no meio da rodada. A base é o índice de 30/07, que foi **validado
por amostragem** (oito das nove afirmações centrais se mantêm) e completado.

## (A) O que desfaz o trabalho dela

| Item | O que falta | Onde conferir |
|---|---|---|
| **PERFIL-JOGO-01** | entregas 1, 3, 4 e 6; a 5 é parcial. **A 2 saiu da lista — foi medida hoje e está paga** | `profiles/manager.py:206-208` segue reaplicando a cada ativação |
| **AUTOMATISMO-MORTO-01** | cadeado ligado desde 28/07 + 5 perfis catch-all disputando | flag de 2 bytes; journal de 3 dias sem `profile_autoswitch` |
| **ÁRVORE-DIVERGENTE-01** | E0 a E5 — hoje **17 × 25** commits | E2 é o achado grave nº 1 desta auditoria |
| **SINAL-DE-JOGO-01** *(nova)* | o documento que não existia, agora escrito | `lifecycle.py:3163`, `game_signal.py:109-126` |
| **DUPLO-REGISTRO-01** | a cura R-D; o remendo de 26/07 é o que segura | — |
| **EMPATE-01/E2** | a aba não mostra que há disputa | `profiles_actions.py:139` traduz `"any"` para `"Sempre"` |

Duas correções ao índice de 30/07, medidas hoje: o cadeado tem **duas portas**
(`perfil_e_regra_de_jogo` **ou** `perfil_declara_modo_de_jogo`), e o furo por
título vem da **segunda** — a primeira recusa título de propósito. Os perfis
`fps.json` e `coop_local.json` dela furam pela porta 2.

## (B) O que ela vê todo dia

| Item | O que falta |
|---|---|
| **CARD-OCUPA-01** *(nova, pedido dela hoje)* | touchpad, lightbar, microfone e alto-falante ocuparem o vão que o teto elástico devolveu |
| **JANELA-FIEL-01** *(nova)* | cinco defeitos: latch de reconciliação, pollers por índice, "Restaurar Padrão" morto em pacote, conflito por nome cru × slug, TUI que mente |
| **LIGHTBAR-JOGADOR-01** | E0 a E5, inteiras |
| **LARGURA-01** | E2 a E9; a E1 entrou só na aba Rumble |
| **SOM-02** | E1 a E5, sem uma linha de código |
| **MIC-BT-01** | 3 das 4 caixas |
| **GATILHO-PALAVRA-01** | só o rótulo `Custom` — 24 caracteres contra teto de 22. **A palavra é dela** |
| **STEAM-INPUT-01** | o item 0, a frase da regra padrão, e o desfazer dentro da janela |
| **CONTAGEM-E-COOP-01** *(documento enfim escrito)* | o aviso antes de derrubar três jogadores; e a aba Emulação conta nós `js*` crus |
| **BOTÃO-QUE-NÃO-MENTE-01** | entregas 5 e 6 |
| **JOGO-01/E2** | superfície da exceção de Steam Input — pendência declarada **dentro do código** e fora de todas as faixas |

## (C) O que protege a casa

| Item | O que falta |
|---|---|
| **DOC-VERDADE-02** *(nova)* | as 7 contradições que persistem + 4 mentiras novas |
| **PUBLICAÇÃO-FIEL-01** *(nova)* | AppStream com data errada, `[REDACTED]` no README publicado, doc de instalação uma release atrás, job pypi fora do guarda |
| **SIMETRIA-INSTALL-02** *(nova)* | fontes nunca removidas, regras órfãs no `--keep-udev`, `purge.sh` sem `--help`, `sudo bash` sugerido |
| **TESTE-HONESTO-01** *(nova)* | 297 testes contra GTK de mentira; 9 usos de BT contra 196 de USB |
| **CHECKLIST de hardware** | 31 caixas, 0 marcadas |
| **PROVA-DE-TELA-01** | não virou rotina |
| **PROMESSA-NÃO-CUMPRIDA-01** | B2, B4, C1-C3, metade do D, E e F |
| **PALAVRA-01/E5** | o quinto hook do pre-commit |
| **CR-05** | o NOTICE declarar os três drivers GPL-2.0 — diagnosticado em 25/07, atravessou a v0.4.0 |

## (D) As órfãs e as esquecidas

**Treze identificadores de sprint vivem sem documento.** Um deles,
`CODIGO-MORTO-01`, é citado **dentro do código-fonte** (`xlib_window.py:1`).
Os outros: MIC-FAIXA-01, SLOT-JOGADOR-01, RUMBLE-PRESO-01, APLICAR-VERDADE-01,
AVISO-VIVO-01, IPC-SEM-TRAVA-01, TESTE-QUE-MEDE-01, JANELA-CEGA-02,
FONTE-PADRÃO-01, PACOTE-COM-NOME-01, CONTAGEM-E-COOP-01 (materializado hoje) e
SEGUNDA-JANELA-01.

**Três superfícies de interface nunca foram medidas por índice nenhum:** o applet
COSMIC (instalado em `/usr/local/bin`, versionado 0.4.0, fonte intacto desde
25/07), a janela compacta e a bandeja. É a sprint RADAR-01, nova.

**IDENT-01 e MÁSCARA-01** têm desenho completo e zero menções em `src/`.
**CR-03**, a bancada de medição, é a menos rastreada da casa: zero commits que a
citem.

E o campo `Status:` continua mentindo: **41 dos 50 documentos dizem ABERTA**,
incluindo entregas provadas. O custo já foi pago quatro vezes — toda sessão
re-deriva o estado do zero.

## (E) O que só ela pode decidir

As seis do índice de 30/07 continuam de pé: o que o R1 deve fazer (o padrão
continua Alt+Tab); religar ou não o hold do PS; o destino de `pragmata.json` e
`pragmata2.json`; manter ou afrouxar o drop-in 51 do microfone; a migração de
25/07 nos seis presets; a palavra do rótulo `Custom`.

Somam-se três, desta auditoria:

7. **A ref local `main`** — retargetar, apagar ou deixar (a armadilha do push).
8. **O `[REDACTED]` no README publicado** — URL real do fork de release, ou
   marcador honesto com nota. Não há ADR registrando a política.
9. **O destino do `hefesto-dsx-recover.service`** — o doctor ensina a instalar a
   unidade que o storm-audit classificou como realimentação positiva do storm.
   Três fontes incompatíveis, e nenhuma cita as outras.

Uma mudou de estado, para melhor: **a fonte de captura padrão hoje é a entrada
do DualSense**, não um monitor. `pactl get-default-source` devolve
`alsa_input.usb-Sony...DualSense...iec958-stereo`. A cura de `84c0f83` elegeu
certo e grudou. O residual estrutural continua verdadeiro, mas muda de redação:
não é "o sistema grava o monitor", é "sem o controle plugado ninguém reelege a
fonte".

---

# Os riscos estruturais que nenhuma sprint cobre

Três coisas que a auditoria achou e que não são defeito de hoje — são o formato
do problema de amanhã.

**A classe `Daemon` tem ~95 métodos e ~3280 linhas**, cobrindo onze
responsabilidades. O acoplamento **volta** dos subsistemas por `getattr`: 66
ocorrências em `ipc_handlers.py`, 49 em `gamepad.py`, 21 em `coop.py`. Como
`getattr` com default tolera ausência em silêncio, renomear um método do `Daemon`
pode desligar comportamento em três subsistemas **sem erro nenhum**. A
recomendação medida não é reescrever: é extrair primeiro os aglomerados já
coesos e trocar `getattr`-com-default por protocolo tipado onde o daemon é sempre
real.

**A porta UDP 6969 não tem autenticação.** Está em `127.0.0.1` (medido vivo, pid
3615), o que contém a rede, e a ausência de auth é compatibilidade com o DSX —
o protocolo não tem. Mas qualquer processo local escreve deadzone de gatilho:
`TriggerThreshold` em 255 mata o gatilho dentro da partida. A recomendação é
tornar o loopback **invariante dura** (recusar bind fora dele sem opt-in
explícito) e dizer no `udp-schema.md` que a porta é autoridade local irrestrita.

**438 `replace refs` do `filter-repo` seguem ativos**, e quase enganaram esta
auditoria: `git cat-file commit <hash-antigo>` devolve o conteúdo do commit
**novo**, em silêncio, a menos que se use `--no-replace-objects`. Não afeta o
produto; afeta toda arqueologia futura por hash.

---

# O que esta auditoria NÃO mediu

Escrito de propósito, para não virar afirmação por omissão.

- **A janela não foi aberta.** Nenhum clique, nenhuma captura da GUI viva. Toda
  afirmação sobre interface vem de código e de `.glade`. O daemon dela está no ar
  e a regra da rodada proibia encostar.
- **Nenhum ciclo `install`/`uninstall` foi executado** — a simetria foi conferida
  por leitura item a item dos dois scripts, não por execução.
- **Nenhum pacote foi construído ou instalado.** A paridade veio do gate estático
  e da leitura; os seis artefatos da v0.4.0 não foram baixados.
- **`nix build` não rodou** (o `nix` não existe nesta máquina) — a conclusão do
  `fakeSha256` é de leitura.
- **A suíte rodou uma vez.** Sem repetição, não há afirmação sobre estabilidade
  dos testes de timing; os cinco avisos de `os.fork()` são o único sinal visível.
- **Cobertura de linhas não foi medida** — 6097 verdes não dizem quanto de `src/`
  é exercitado.
- **Nenhum `git diff` de equivalência** foi feito para dez dos dezessete commits
  da `main`; os quatro marcados foram diffados, os outros aceitos da triagem.
- **O applet não foi construído nem executado**, e o binário instalado não foi
  comparado com o fonte — é justamente o objeto da RADAR-01.
- **`docs/history/` e `docs/research/`** ficaram fora, por decisão registrada: ali
  contradição pode ser registro correto de decisão superada.
- **O gate `check_anonymity` deu verde**, e vale dizer por quê: a árvore estava
  limpa. Ele usa `git grep` e continua **estruturalmente cego a arquivo
  untracked** — a ordem correta continua sendo `git add` **antes** dos portões.

---

## Os documentos que esta sessão materializou

Dez sprints, escritas a partir desta auditoria e **remedidas** contra o código de
hoje uma a uma — o que fez três delas corrigirem o próprio achado de origem
(registrado dentro de cada documento):

| Sprint | O que fecha |
|---|---|
| [CARD-OCUPA-01](../sprints/2026-07-31-CARD-OCUPA-01-o-desenho-ocupa-o-vao-que-o-teto-devolveu.md) | o pedido dela de 01h34: os desenhos ocuparem o vão lateral |
| [CR-SEQUÊNCIA-01](../sprints/2026-07-31-CR-SEQUENCIA-01-o-que-avanca-sem-a-mao-dela-e-o-que-nao.md) | a dúvida dela sobre a sala limpa: o que avança sem a mão dela, e o que não |
| [SINAL-DE-JOGO-01](../sprints/2026-07-31-SINAL-DE-JOGO-01-o-daemon-desiste-do-jogo-antes-do-jogo-acabar.md) | o `display_authority` e a linha `healthy` × `seeing` |
| [JANELA-FIEL-01](../sprints/2026-07-31-JANELA-FIEL-01-a-janela-que-para-de-reconciliar-e-o-botao-morto-no-pacote.md) | os cinco defeitos da GUI |
| [SIMETRIA-INSTALL-02](../sprints/2026-07-31-SIMETRIA-INSTALL-02-o-que-o-install-deixa-para-tras.md) | as bordas do instalador |
| [PUBLICAÇÃO-FIEL-01](../sprints/2026-07-31-PUBLICACAO-FIEL-01-o-que-a-release-conta-de-errado.md) | o metadado que a release publica errado |
| [RADAR-01](../sprints/2026-07-31-RADAR-01-as-tres-superficies-que-ninguem-nunca-olhou.md) | applet, janela compacta e bandeja |
| [DOC-VERDADE-02](../sprints/2026-07-31-DOC-VERDADE-02-a-recontagem-e-as-quatro-mentiras-novas.md) | a recontagem e as mentiras novas |
| [CONTAGEM-E-COOP-01](../sprints/2026-07-31-CONTAGEM-E-COOP-01-o-aviso-antes-de-derrubar-tres-jogadores.md) | a promessa de documento mais antiga da casa |
| [TESTE-HONESTO-01](../sprints/2026-07-31-TESTE-HONESTO-01-os-297-verdes-que-nao-medem-interface.md) | a cobertura que finge |

A ordem de execução está no
[índice das ondas](../sprints/2026-07-31-INDICE-as-ondas-depois-da-auditoria.md),
separado por **quem precisa estar presente**: dezessete itens que saem sem ela,
dez que precisam do olho dela na tela, e dez que são decisão dela.

### As correções que a redação fez à auditoria

Escrever obriga a conferir cada rua do mapa, e três sprints derrubaram o próprio
achado de origem:

- **O `.deb`, o AppImage e o Flatpak embalam os perfis padrão.** O auditor disse
  que não: `build_deb.sh:133` copia `assets/.` inteiro, e o AppImage e o Flatpak
  os instalam de propósito desde 30/07. O botão "Restaurar Padrão" morre mesmo
  assim — mas **pelo resolvedor, não pelo pacote**, o que muda a correção.
- **A bandeja não é "a que ela realmente vê".** O `cosmic-applet-status-area` não
  está no painel dela nem está rodando (medido: zero processos), então a bandeja
  GTK não tem onde aparecer. O que ela vê é o **applet Rust**, vivo no PID 4505.
  Isso reordena as entregas da RADAR-01.
- **O caminho que derruba o co-op foi percorrido 20 vezes em três dias**, a
  última durante esta sessão. A CONTAGEM-E-COOP-01 subiu de MÉDIA para MÉDIA-ALTA
  por medição, não por opinião.
- **Os 297 testes NÃO rodam contra widget de mentira na máquina dela.** O auditor
  disse que sim; medido, os 17 arquivos carregam a guarda `GATE-SKIP-MASK-01` e
  `_install_gi_stubs()` **volta antes de plantar** quando o PyGObject real está
  presente. Dezesseis terminam o import com o `gi` verdadeiro. **O falso-verde
  acontece no CI**, e é reproduzível: simulando o ambiente do job `lint-test`
  (que não instala PyGObject), `test_rumble_actions.py` devolve **29 verdes
  contra `Gtk.Box = object`** — enquanto um arquivo com a guarda certa
  desaparece da coleta em vez de fingir. Isso não salva os 17; muda **onde** o
  defeito mora, e portanto qual é a cura.
- **A praga de 25/07 não está de volta.** O estudo daquele dia mediu ~240 asserts
  travando o texto do código, um deles proibindo a correção de um defeito. Hoje
  são 21 chamadas de `inspect.getsource` mais 22 leituras de fonte por texto, e
  **nenhuma proíbe corrigir bug**. A direção é de queda.
