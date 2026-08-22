# BLUETOOTHD-MORTO-POR-NÓS-01 — o watchdog que nós ligamos matou o rádio dela

- **Estado:** CONCLUÍDA — a cura está no `install.sh:2215` (`WatchdogSec=0`, com o nome da sprint dentro) e no drop-in de resiliência anunciado em `:2264`; `scripts/bt_health_watchdog.sh` e `tests/unit/test_bt_resilience_assets.py` de pé (verificado em 21/08/2026)
- **Escrito em:** 08/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que esta sprint responde:** a frase dela, dita no meio da noite —
  *"o bt tá se auto desligando"* — e a perda dos quatro pareamentos
- **Natureza:** defeito nosso, medido, com cura no `install.sh` e portão que morde
- **Grau:** **MEDIDO** na causa e na origem

---

## 1. O que aconteceu, com hora

**GRAU: MEDIDO.** Journal de 08/08/2026:

```
00:27:35  bluetooth.service: Watchdog timeout (limit 30s)!
00:27:35  bluetooth.service: Killing process 1106 (bluetoothd) with signal SIGABRT
00:27:52  bluetooth.service: Main process exited, code=dumped, status=6/ABRT
00:27:54  hefesto-bt-bonds: snapshot de bonds gravado ... (4 bond(s))
00:27:58  bluetoothd volta — sem os pareamentos
```

Ela ficou **sem controle nenhum**, no meio de uma sessão de medição. O Pro
Controller perdeu o bond de vez; os DualSense tiveram de ser repareados à mão.

**O `bluetoothd` não caiu de defeito próprio — ele foi MORTO pelo systemd**, por
uma linha que **nós** escrevemos.

---

## 2. A origem é nossa, e não há dúvida

**GRAU: MEDIDO.**

O pacote do BlueZ entrega o watchdog **desligado**:

```ini
# /usr/lib/systemd/system/bluetooth.service   (do pacote, intocado)
#WatchdogSec=10          ← COMENTADO. desligado de fábrica.
```

E o nosso drop-in ligava, com o triplo do valor que o upstream nem usa:

```ini
# /etc/systemd/system/bluetooth.service.d/10-hefesto-resilience.conf   (NOSSO)
WatchdogSec=30
```

Três coisas fecham a atribuição:

1. o `ls` do diretório de drop-ins mostra **um arquivo só**, e é o nosso;
2. `systemctl show bluetooth -p WatchdogUSec` devolvia `30s`;
3. o valor está **versionado** neste repositório, em
   `assets/systemd/bluetooth-dropin-10-hefesto-resilience.conf`, e é o
   `install.sh` que o instala.

### Por que 30 s é curto demais

**GRAU: SUSPEITA COM MECANISMO**, e o mecanismo fecha. O laço do `bluetoothd`
bloqueia por motivos **legítimos**. Na mesma noite, um `sdptool browse` estourou
**35 segundos** contra um controle que aceitava o ACL e não respondia nada acima
dele. Trinta segundos de silêncio não são prova de daemon travado — são o custo
normal de falar com um aparelho ruim. **O upstream entrega a linha comentada
exatamente por isso.**

---

## 3. O portão que existia e ficou verde o tempo todo

**GRAU: MEDIDO.** Havia um teste travando esse valor:

```python
assert re.search(r"^WatchdogSec=\d+$", text, re.M)
```

`\d+` aceita **qualquer número**. O portão travava a **presença da linha** — que
nunca foi o risco — e ficou verde enquanto o valor matava o rádio dela.

**Achado de método, e ele vale para todo portão desta casa:** um portão que
aceita qualquer valor não trava valor nenhum. Se o que importa é o número,
o número tem de estar no teste.

---

## 4. A cura

**Uma linha, e ela é o zero explícito.**

```ini
WatchdogSec=0
```

**Por que `0` e não apagar a linha:** apagada, o arquivo pareceria ter esquecido;
escrita, ele diz que a casa **decidiu**. E um `systemctl show -p WatchdogUSec`
mostra a decisão sem precisar abrir o repositório.

**Entra pelo `install.sh`, sem flag**, no passo que já existe (`3e-bis`, que grava
o drop-in) — conforme a decisão dela de 08/08: *"não quero nenhuma correção na
mão, quero tudo dentro do install sem flag"*. Máquina já instalada recebe a
correção no próximo `install.sh`, que reescreve o drop-in.

**E o texto que mentia foi corrigido junto:** o `install.sh` anunciava
*"WatchdogSec=30"* como benefício em duas linhas, e o `scripts/doctor.sh` vendia o
watchdog como proteção contra *"hang sem crash"*. Os três textos agora dizem o que
o arquivo faz.

### O portão passa a morder

`tests/unit/test_bt_resilience_assets.py` exige `^WatchdogSec=0$`. Trocar o valor
de volta para qualquer outro número **reprova**.

---

## 5. O risco de desligar, declarado

**É risco de OMISSÃO, não de ação.** Um `bluetoothd` genuinamente travado — laço
morto, sem crash — deixa de ser morto pelo systemd.

Três coisas contêm esse risco:

1. **não é regressão nova.** É voltar ao que o BlueZ entrega e ao que todo
   Pop!\_OS roda hoje, sem drop-in nenhum;
2. **o watchdog do systemd só sabe MATAR.** Ele não distingue "travado" de
   "ocupado com um aparelho ruim" — e foi justamente por não distinguir que ele
   custou a ela quatro pareamentos;
3. **quem cobre o hang de verdade é a vigia da casa**, que SONDA o D-Bus em vez de
   esperar um ping. Ela precisa de conserto (seção 6), mas o instrumento certo é
   ela, não o ping.

**Ressalva de instância viva:** o drop-in vale a partir do próximo *start* do
`bluetoothd`. O `install.sh` faz `daemon-reload` e **nunca** reinicia o serviço —
reiniciar derrubaria os controles dela. Então na máquina dela o `WatchdogUSec`
continua 30 s **até o próximo boot**, e isso é de propósito.

---

## 6. O segundo defeito da mesma noite: a vigia reinicia por diagnóstico errado

**GRAU: MEDIDO**, e esta sprint **não** o cura — declara.

```
00:54:26  estado doente suspeito (9 recusas/10min) mas há 3 device(s) conectado(s) — restart adiado
00:56:26  estado doente confirmado (9 recusas/10min, 0 conectados) — reiniciando bluetooth.service
00:58:26  estado doente (9 recusas/10min) — restart segurado pelo rate-limit
```

**Às 00:56:26 a nossa vigia reiniciou o Bluetooth dela** — o mesmo segundo em que
o `hefesto-bt-agent` recebeu `SIGUSR1` e morreu.

O critério é `LIMIAR_RECUSAS=8` numa janela de 10 min
(`scripts/bt_health_watchdog.sh:40-41`), contando linhas de
`Refusing connection from …: unknown device`. As nove "recusas" eram de **um
aparelho só**, sem bond, insistindo.

**E o diagnóstico está errado no conceito:** `unknown device` significa **bond
faltando**, não daemon doente. **Reiniciar o serviço não cria bond nenhum** — só
derruba quem estava de pé. A vigia conta **eventos**, e o que importa é **quantos
aparelhos distintos**.

O laço que isso fecha:

```
aparelho sem bond insiste  →  BlueZ recusa (unknown device)
        ↑                              ↓
  mais recusas              a vigia conta ≥8 e reinicia
        ↑                              ↓
alguns não voltam    ←    restart derruba TODOS + mata o agente
```

**Cura desenhada, não escrita:** rachar o critério em dois. `unknown device` vira
**aviso** (é sintoma de bond, e há sprint dona disso); o restart fica reservado a
assinatura de daemon realmente travado, medida por sonda de D-Bus. Custo: **M**.

---

## 7. O terceiro: a janela sem agente de pareamento

**GRAU: MEDIDO** nos números; **SUSPEITA COM MECANISMO** no efeito.

O `hefesto-bt-agent.service` tem `TimeoutStopSec=3s`, `SendSIGKILL=yes` e
`RestartSec=5`. O `bt-agent` **não trata `SIGTERM`**, então é sempre morto por
`SIGKILL`: **36 quedas e 36 `SIGKILL` desde 29/07 — 100%**. A janela sem agente
registrado, medida em 08/08, foi de **3 a 5 s** por ciclo.

Com `JustWorksRepairing=confirm` no `/etc/bluetooth/main.conf` — linha **nossa** —
todo repareamento nessa janela é recusado, porque não há quem confirme.

**GRAU: MEDIDO** que o `StartLimitBurst=5/60s` **nunca foi atingido** — o medo de
o agente parar de vez não se materializou. **Cura desenhada:** `RestartSec` de 5 s
para 250 ms e `Restart=always`. Custo: **P**.

---

## 8. O que fica ABERTO

1. **As curas 6 e 7 não entraram** — são M e P, com desenho pronto, e ficam para a
   próxima leva desta madrugada.
2. **O restauro automático de bonds continua sem existir.** Ela decidiu em 08/08
   que restauro manual com `sudo` **não é produto**. O snapshot funciona sozinho
   (gravou os 4 bonds 2 s depois do crash); falta o gatilho da volta, e ele precisa
   ser **seletivo** — restaurar chave velha quando o par rotacionou a dele gera
   loop de autenticação, que é a classe de gatilho do crash de heap. Custo: **G**.
3. **O `/etc/bluetooth/main.conf` dela está colapsado.** O arquivo tem 38 linhas,
   das quais 35 são o nosso bloco; o `main.conf.dpkg-dist` da distro tem **384**.
   Um ciclo `uninstall` → `install` **não devolve o original**. Em comportamento
   não muda nada (as 380 linhas eram comentários e defaults), mas quem abrir esse
   arquivo daqui a um mês não vê mais default nenhum documentado. **GRAU: MEDIDO.**
4. **Sobram 41 backups `main.conf.bak.hefesto-*`** em `/etc/bluetooth`. Higiene, e
   é gesto dela.
5. **Nenhuma das curas de Bluetooth entra no `.deb`** — nem o drop-in, nem os dois
   timers, nem as units. Quem instalar pelo pacote **não recebe nada disto**. É a
   dívida de máquina limpa da resposta 17, e é **G**.

## 9. Nota de honestidade

O diagnóstico é leitura de journal e de código. **Nada foi reiniciado por nós**: o
`bluetoothd` foi morto pelo systemd às 00:27:35 e reiniciado pela nossa vigia às
00:56:26, ambos sem intervenção humana — o que é exatamente o defeito.

**Uma tese foi perseguida e abandonada por ordem dela**, e fica registrada para
não voltar: a de que o dongle ou a porta USB seriam a causa. Ela disse, e tem
razão pelo histórico: *"já perdemos dias na tese de ser o dongle ou porta usb,
não é… É nossa configuração."* Era. O `WatchdogSec` é nosso, o limiar da vigia é
nosso, e o `JustWorksRepairing=confirm` é nosso.

**Uma segunda tese caiu por medição:** o `[General]` duplicado no `main.conf`
parecia defeito de escrita nosso. O parser real (GKeyFile) **aceita e faz merge** —
conferido com a biblioteca de verdade, não com a réplica. Descartado.
