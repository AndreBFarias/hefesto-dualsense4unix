# IDENTIDADE-01 — o projeto ainda se chama pelo nome dele

**21/08/2026.** O repositório mudou de dono: saiu de uma conta pessoal e passou
a viver na organização `Hefesto-Team`. **A identidade do software não foi
junto.** O aplicativo continua se chamando `br.andrefarias.Hefesto`, e o
endereço antigo aparece em 8 arquivos.

Escrito a pedido dela, depois de eu ter marcado a `<url type="homepage">` do
metainfo como "pendência que não é minha".

---

## O erro que abre esta sprint

Eu afirmei que a homepage do metainfo apontava para **outro repositório**:

```xml
<url type="homepage">https://github.com/AndreBFarias/hefesto</url>
```

**É falso, e a régua estava à mão.** `gh api repos/AndreBFarias/hefesto`
resolve para `Hefesto-Team/hefesto-dualsense4unix` — é o **mesmo** repositório,
pelo nome que ele tinha antes do rename, servido pelo redirecionamento do
GitHub. Eu classifiquei sem conferir e passei a decisão adiante como se fosse
dúvida dela.

Fica registrado porque é a mesma família das três armadilhas de hoje: afirmar
com confiança o que não se mediu.

O redirecionamento funciona, então **nada está quebrado**. Mas o endereço
publicado de um projeto não deve depender de redirect de nome antigo de conta
pessoal: no dia em que a conta for renomeada ou removida, o link morre.

---

## O que existe hoje, contado

| O quê | Onde | Quantos arquivos |
|---|---|---|
| `br.andrefarias` — o **app-id** | tudo | **46** |
| `AndreBFarias` — endereços | metainfo, docs históricos | **8** |

Os 46 do app-id, por área:

```
15  tests/        2  src/          1  NOTICE
14  docs/         2  .github/      1  LICENSES
 5  scripts/      1  install.sh    1  uninstall.sh
 3  flatpak/
```

E os três arquivos do flatpak **têm o id no próprio nome**:

```
flatpak/br.andrefarias.Hefesto.yml
flatpak/br.andrefarias.Hefesto.desktop
flatpak/br.andrefarias.Hefesto.metainfo.xml
```

---

## Por que isto NÃO é um `sed`

O app-id é a identidade do aplicativo para o sistema operacional. Trocá-lo é
**migração**, não renomeação. O que ele carrega:

1. **O nome do pacote flatpak.** Quem tem instalado tem
   `br.andrefarias.Hefesto`; um id novo é um **aplicativo diferente** para o
   flatpak. Não atualiza — instala do lado.
2. **O `.desktop` e o ícone.** `Icon=br.andrefarias.Hefesto`
   (`flatpak/br.andrefarias.Hefesto.desktop:5`). Ícone é resolvido por nome de
   arquivo no tema.
3. **A detecção de flatpak em runtime**, em `app/app.py:619` — o produto
   pergunta se está rodando dentro do próprio sandbox comparando com a string
   literal.
4. **O diretório de configuração do usuário**, se houver. Precisa de leitura do
   caminho antigo e escrita no novo, ou a pessoa perde os perfis dela.
5. **Os 15 testes** que cobram o id nos empacotamentos e no install.

**A decisão dela que abre a execução:** qual é o id novo? Duas formas usuais, e
nenhuma é obviamente melhor:

| Candidato | A favor | Contra |
|---|---|---|
| `io.github.HefestoTeam.Hefesto` | Convenção do Flathub para projeto hospedado no GitHub; não depende de domínio próprio | Amarra a identidade ao GitHub |
| `br.hefestoteam.Hefesto` | Mantém a forma atual, só troca a pessoa pelo time | Pede que o domínio exista algum dia, pela regra do Flathub |

Enquanto ela não escolher, **nada nesta sprint começa** — trocar por um id e
depois por outro é pagar a migração duas vezes.

### DECIDIDO em 21/08/2026 — `io.github.hefesto_team.hefesto_dualsense4unix`

**A decisão está fechada e a sprint está liberada para executar.**

O caminho até ela, porque as duas primeiras formas eram armadilha: a inclinação
inicial dela foi `io.github.HefestoTeam.Hefesto`, e depois `Hefesto_Team`. As
duas reprovam — a conferência está logo abaixo. A forma escolhida é a única das
três que passa em todos os critérios sem exigir mexer em mais nada.

Conferida componente a componente contra a regra publicada:

| Critério | Resultado |
|---|---|
| Componentes | 4 (o Flathub exige ao menos 4 para `io.github.*`, e no máximo 5) |
| Cada componente casa `[A-Za-z_][A-Za-z0-9_]*` | os quatro passam |
| Porção de domínio em minúsculas | `io.github.hefesto_team` — sim |
| Hífen convertido em `_`, não removido | `Hefesto-Team` -> `hefesto_team` |
| Mapeia para repositório existente | `github.com/hefesto-team/hefesto-dualsense4unix` — **existe** |

**O preço aceito:** o id fica amarrado ao nome atual do repositório. Renomear o
repositório um dia obriga a repetir esta migração inteira.

**E há um detalhe técnico que precisa entrar antes de fechar:** o nome da
organização é `Hefesto-Team`, **com hífen** — e hífen **não é válido** num
componente de app-id. A regra (D-Bus e AppStream) é que cada componente case
`[A-Za-z_][A-Za-z0-9_]*`:

| Componente | Vale? |
|---|---|
| `Hefesto-Team` | **INVÁLIDO** — o hífen derruba |
| `HefestoTeam` | válido |
| `Hefesto_Team` | válido |

Então `io.github.Hefesto-Team.Hefesto` **não existe como opção**. Se a escolha
for essa família, o id é `io.github.HefestoTeam.Hefesto` ou
`io.github.Hefesto_Team.Hefesto`.

### CONFERIDO na documentação do Flathub, 21/08/2026

A pendência acima foi fechada na fonte, e o resultado **corrige as duas formas
que estavam na mesa**. Da página de requisitos do Flathub, literal:

> *"Applications using code hosting IDs and hosted on `github.com, gitlab.com,
> codeberg.org, framagit.org` must use `io.github., io.gitlab., page.codeberg.,
> io.frama.` prefixes respectively and must have at least 4 components."*

> *"The domain portion must be in lowercase and must convert dash `-` to
> underscore `_`."*

E o que ninguém tinha visto, que é o achado que importa:

> *"`io.github.example_foo.bar` maps to `https://github.com/example-foo/bar`."*

**O terceiro e o quarto componentes são o dono e o REPOSITÓRIO**, não o dono e o
nome do aplicativo. O Flathub calcula a URL do repositório a partir do id e
confere. Ou seja:

| Candidato | Mapeia para | Existe? |
|---|---|---|
| `io.github.HefestoTeam.Hefesto` | `github.com/HefestoTeam/Hefesto` | **não** — a org é `Hefesto-Team` e o repo é `hefesto-dualsense4unix` |
| `io.github.Hefesto_Team.Hefesto` | `github.com/Hefesto-Team/Hefesto` | **não** — o repo `Hefesto` não existe |
| `io.github.hefesto_team.hefesto_dualsense4unix` | `github.com/hefesto-team/hefesto-dualsense4unix` | **sim** |

A inclinação dela de 21/08 era `io.github.HefestoTeam.Hefesto`, e depois
`Hefesto_Team`. **As duas reprovam:** a primeira por perder o hífen em vez de
convertê-lo (a regra pede `_`, não remoção) e por maiúscula na porção de
domínio; as duas por apontarem para um repositório que não existe.

### As opções que sobram, e o preço de cada uma

| # | Id | O que exige | Contra |
|---|---|---|---|
| 1 | `io.github.hefesto_team.hefesto_dualsense4unix` | nada — casa com o que já existe | Longo, e amarra o id ao nome atual do repositório |
| 2 | `io.github.hefesto_team.Hefesto` | criar um repositório `Hefesto` na org, ou renomear o atual | Renomear repositório de novo, um dia depois da mudança de dono |
| 3 | `br.hefestoteam.Hefesto` ou similar | registrar o domínio e servir a página | Custo e manutenção de domínio; o Flathub cobra que ele exista |

**Nenhuma é obviamente melhor, e a escolha é dela.** O que mudou é que agora as
três estão medidas contra a regra publicada, em vez de contra a memória de quem
escreve.

**Fonte:** [Requirements — Flathub Documentation](https://docs.flathub.org/docs/for-app-authors/requirements)

---

## O roteiro

### Fase 1 — o que não depende da decisão (barato, pode ir agora)

Trocar as 8 ocorrências de `AndreBFarias` que ainda apontam para a conta
pessoal, pela URL da organização. A `<url type="homepage">` do metainfo é uma
delas.

**Não tocar** nas de `docs/process/sprints/2026-07-*` nem no
`estudos/2026-07-31`: ali a URL é registro do que era verdade naquele dia.

**Prova:** `grep -rl AndreBFarias --exclude-dir=.git .` devolve só os históricos.

**Um caso que não é nem um nem outro, e fica para ela decidir:**
`docs/history/gh-repo-config.md`. Mora em `history/`, então se declara registro
— mas o conteúdo são **comandos para executar**, do tipo
`gh repo edit AndreBFarias/hefesto`. Quem rodar hoje depende do redirect. Ou ele
ganha uma nota datada dizendo que o endereço mudou, ou os comandos são
atualizados e ele deixa de ser história. Não é decisão de quem varre `sed`.

### Fase 2 — o app-id, depois da decisão dela

1. Renomear os três arquivos de `flatpak/`.
2. Trocar o `Icon=` do `.desktop` e o nome do ícone em `assets/`.
3. Trocar a string de detecção em `app/app.py:619` e o comentário em
   `app/main.py:148`.
4. `install.sh` e `uninstall.sh`.
5. Os 15 testes — e cada um passa a cobrar o id **novo**, senão a mordida some.
6. `.github/workflows/flatpak.yml`.
7. `NOTICE` e `LICENSES`.

### Fase 3 — a migração de quem já instalou

**É esta fase que separa renomear de migrar, e é a que não pode faltar.**

- Ler a configuração do caminho antigo se o novo não existir, e escrever no
  novo. Uma vez, sem apagar o antigo.
- O `uninstall.sh` precisa conhecer **os dois** ids, ou deixa lixo.
- O `install.sh` precisa avisar quem tem o flatpak antigo que ele virou outro
  aplicativo e deve ser removido à mão.

**Prova de trabalho:** um ciclo `uninstall` → `install` numa máquina que tinha o
id antigo, terminando com os perfis dela intactos e nenhum resto do id velho.

---

## O que esta sprint NÃO faz

Não muda o **nome de exibição** do aplicativo, que continua "Hefesto —
DualSense4Unix". Isto é sobre identidade técnica, não sobre marca.

Não mexe no `LICENSE` nem na autoria dos commits. Quem escreveu continua tendo
escrito.

---

## Tamanho estimado

- **Fase 1:** ~8 linhas em 5 arquivos. Minutos.
- **Fase 2:** ~60 a 90 linhas em 25 arquivos, três deles renomeados.
- **Fase 3:** ~120 a 200 linhas, e é onde mora o risco.

A Fase 1 pode ir sozinha e não bloqueia nada. As Fases 2 e 3 **só depois da
decisão dela sobre o id**, e as duas entram na mesma leva — um id novo sem
migração deixa quem já usava sem os perfis.
