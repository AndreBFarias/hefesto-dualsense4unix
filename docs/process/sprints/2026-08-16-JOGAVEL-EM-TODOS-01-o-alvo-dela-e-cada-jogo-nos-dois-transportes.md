# JOGÁVEL-EM-TODOS-01 — o alvo dela é cada jogo, nos dois transportes

> *"sempre meça tudo tá bom? pensa no qol do user, automação de interface e
> pensa em aplicar cada uma das descobertas de forma universal. contto contigo
> pra tomar as decisões de po nossas. (…) espero de fato que tenhamos tudo
> resolvido e cada um dos jogos locais jogável via cabo ou bt."*
> — ela, 15/08/2026, ao sair para dormir

Este é o sprint do **critério de pronto** que ela nomeou. Não é "o daemon
funciona", não é "a bateria passa": é o jogo dela, na mão dela, nos dois
transportes.

---

## Estado em 16/08/2026, 06h

**24 jogos instalados.** O que a madrugada mediu, por jogo:

| | jogos | |
|---|---|---|
| sem impedimento conhecido | 22 | nada que o disco saiba detectar — **não é promessa de que funciona** |
| impedido, cura automática | 1 | PRAGMATA, sem o wrapper na árvore viva — se conserta sozinho quando a Steam fechar |
| impedido, decisão dela | 1 | Sackboy, allowlist inerte (§3) |

**Por API de entrada** — o número que muda o peso de tudo:

| | jogos | |
|---|---|---|
| `entende_dualsense` | 7 | SDL ou plugin DualShock — o vpad chega direto |
| `indeciso` | **15** | XInput e nada mais — **o vpad só chega por espelho** |
| `sem_evidencia` | 2 | executável ilegível ou sem agulha |

Régua: `.venv/bin/python -m hefesto_dualsense4unix.integrations.prontuario_dos_jogos`

---

## 1. O que já se conserta sozinho (fechado na madrugada)

A cadeia do wrapper está **provada de ponta a ponta na máquina dela**:

- o censo parou de mentir (âncora de caminho, `ARVORE-ERRADA-01`);
- a sentinela nomeia o Pragmata como `regressao`;
- o `hefesto-steam-input-guard.path` dispara quando o `userdata` muda —
  **verificado ao vivo às 06h05**, tocando o diretório e vendo o service rodar;
- com a Steam viva ele **adia** (05h52, também verificado), e adiar não derruba
  o serviço;
- ao salvar/aplicar perfil, a carona repõe pelos cinco gestos da GUI.

Nada disso precisa de clique. **Quando ela fechar a Steam, o Pragmata volta.**

Ver [A árvore errada](../estudos/2026-08-16-A-ARVORE-ERRADA-o-portao-que-olhava-para-o-lugar-errado.md).

## 2. O que só a mão dela mede — a bancada, em ordem

A ordem é por **quanto cada ensaio derruba de hipótese**, não por facilidade.

### 2.1 O par Duskfade × DON'T SCREAM  *(o mais valioso — 10 min)*

Os dois têm a **mesma assinatura no disco**: mesmo motor, `rawinput`+`xinput`
por `LoadLibrary`, mesmo wrapper, mesmo Steam Input desligado. Um funciona, o
outro não. **A causa não está no disco** — está em tempo de execução.

```
# com os DOIS jogos abertos ao mesmo tempo
.venv/bin/python scripts/ensaios/quem_o_jogo_abre.py
```

Ele lê `/proc` de cada um: nós de `/dev/input` abertos, `hidraw`, variáveis de
ambiente e a árvore de processos (sob Proton quem abre pode ser o `wineserver`).

**O que o resultado decide:** se o Duskfade abrir menos nós que o DON'T SCREAM,
a causa é enumeração e o alvo é o broker. Se abrir os mesmos, a causa está
acima, no que o jogo faz com o que abriu.

### 2.2 O Pragmata no rádio, depois que a Steam fechar  *(5 min)*

Confirma a cura de ponta a ponta com a mão dela, que é a única prova que vale:

1. fechar a Steam por completo;
2. conferir: `.venv/bin/python -m hefesto_dualsense4unix.integrations.prontuario_dos_jogos`
   — o Pragmata tem de sair de `impedido`;
3. abrir e jogar **no rádio**.

### 2.3 Os espelhos `28de:11ff`, nos dois estados  *(decisão dela de 15/08:
"medir de novo antes")*

Há uma contradição aberta: o registro da Steam mostra o vpad no slot 0, e a
canônica de 11/08 diz "zero espelhos". Medir com a Steam **aberta** e
**fechada**, antes de mexer em qualquer linha da canônica.

### 2.4 O E-7 (4 min, olho dela) — e só depois o E-5

## 3. A decisão que é dela

**O Sackboy está na allowlist do Steam Input com o Steam Input desligado.**

A allowlist só **preserva** o que já estava ligado — ela nunca liga. Ou seja, o
gesto de pôr o Sackboy na lista não teve efeito nenhum.

Daqui não dá para distinguir dois casos, e eles pedem coisas opostas:

- *a lista entrou tarde* (o guard já tinha desligado antes) → ligar o Steam
  Input do Sackboy na Steam, e a exceção passa a valer;
- *ela desligou depois e mudou de ideia* → tirar o Sackboy da lista, para a
  lista voltar a dizer a verdade.

O prontuário nomeia como `excecao_inerte` e para aí. **Não decidi por ela.**

Pergunta aberta de produto: **a allowlist deveria LIGAR, e não só preservar?**
Hoje o nome "lista de exceções" promete mais do que ela entrega.

## 4. As dívidas que a madrugada abriu e não pagou

| | onde | por quê não foi feito |
|---|---|---|
| `hidden_count` do broker conta em vez de nomear | `doctor.sh:3088` | achado pela outra frente; é o mais grave dos três |
| `check_launch_wrapper` imprime "76 jogos" onde há 63 | `doctor.sh:1508` | contador somando as três árvores; cura de custo zero |
| `check_bt_bonds_persistidos` passa com `n_info > 0` | `doctor.sh:2809` | régua de 22/07 respondendo à pergunta de hoje |
| as 11 linhas nas árvores secundárias | `localconfig.vdf` | inócuas (a Steam não as lê) e o `uninstall --strip` já as tira; exige Steam fechada |
| `SDL_GamepadBind` no `config.vdf` | ponto cego total | ninguém no projeto sabia que o campo existia; o `.path` não o vigia |

## 5. O que este sprint recusa prometer

**Que os 22 jogos "sem impedimento conhecido" funcionam.** Eles não têm motivo
*conhecido* para falhar — e o Duskfade está entre eles, quebrado.

Essa distinção é o produto do `prontuario_dos_jogos`, e não é pessimismo: é o
que impede o próximo relatório de dizer "24 de 24 prontos" e mandar a
investigação para o lugar errado. O placar honesto do alvo dela hoje é:

> **1 jogo confirmado quebrado (Duskfade), 1 se consertando sozinho (Pragmata),
> 1 decisão dela (Sackboy), e 21 sem veredito porque ninguém jogou ainda.**
