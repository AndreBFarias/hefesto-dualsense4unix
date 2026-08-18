# OITO DEFEITOS — a fila que a verificação adversarial derrubou inteira

- **Escrito em:** 08/08/2026, noite, na branch `restauro/inicio-da-sessao`
- **Por que existe:** ela parou o trabalho, e com razão:
  > *"os problemas só se acumulam e estamos ainda no teste A, falta o B e o C.
  > Não tá produtivo ou eficiente de forma alguma."*
- **O que este arquivo é:** o estado honesto dos oito defeitos abertos, e o
  registro de que **as oito curas propostas foram derrubadas** por verificação
  adversarial — antes de ela pagar por qualquer uma delas

---

## 1. O resultado, sem maquiagem

Dezessete agentes: oito investigaram, oito refutaram, um sintetizou.
**Confirmados: zero. Derrubados: oito.**

Isso **não** significa que os defeitos não existem — eles estão todos na tela
dela. Significa que **todas as curas que eu teria escrito estavam erradas**, e
que a verificação as pegou antes da máquina dela.

Depois de um dia em que **três curas corretas quebraram outra coisa**, esse é o
resultado mais útil que a fila podia dar.

---

## 2. Os oito, e o que a refutação achou de mais grave

### 2.1 O diálogo está no botão errado

**Ela:** *"quando eu clico ali no inferior no verde em aplicar, ele não aplica e
não abre o pop up"*.

**MEDIDO:** o botão verde é o `btn_footer_apply` do rodapé
(`gui/main.glade:3616-3620`, verde por `.btn-apply` em `gui/theme.css:836`). E
o payload dele **não carrega modo nem máscara** — `app/draft_config.py:1030-1133`
tem triggers, leds, rumble, mouse, mic, keyboard, controllers, e nada de modo.

**Eu liguei o diálogo no `on_profile_save`** (aba Perfis). Gesto errado.

**E a refutação achou um dano que eu não vi:** o `aplicar=` que passei só grava o
arquivo e retorna — pulando o `delete_profile` do rename, a reconciliação do
rascunho, o reload e o `profile_switch`. Com jogo aberto e "Aplicar agora", o
jogo reabriria **com o modo velho**. O diálogo mentiria exatamente onde promete
mais.

**Ação tomada: REVERTIDO.** A ligação saiu.

### 2.2 A máscara pergunta a cada clique

**Ela:** *"clicar em dualsense ainda pede pra aplicar agora, ao invés de ser só
no botão aplicar"*.

**A cura óbvia — os seletores só registram no rascunho — QUEBRA a aba Início.**
`home_actions._render_home` reescreve os seletores a cada tique a partir do
daemon (`:1059`, `:1076`): a escolha dela **voltaria sozinha** no tique seguinte,
e a linha da máscara nem apareceria (ela só aparece quando o daemon diz gamepad).

Segurar uma escolha pendente exige um **segundo dono do valor** — que é
textualmente o defeito enterrado na `AUTO-01.3`: *"o dono da máscara é o DAEMON,
a GUI só ECOA"*.

**Grau: MEDIDO** que a cura quebraria. **A cura definitiva não está desenhada.**

### 2.3 "1 jogador saiu" com os dois controles na tela

Aparece em vermelho no topo enquanto os dois controles estão listados abaixo,
conectados. Conta jogadores **virtuais**, não controles físicos — e cada reinício
do daemon derruba e recria os vpads.

### 2.4 O "Jogador 3" fantasma

Ainda aberto. A sprint
[JOGADOR-3-FANTASMA-01](2026-08-08-JOGADOR-3-FANTASMA-01-a-cura-certa-no-momento-errado.md)
tem o caso inteiro e a cura revertida.

### 2.5 O rumble

**Ela corrigiu a minha hipótese** — *"funcionava o rumble sendo xbox, playstation
ou apenas sony"* —, então a máscara **não** é a causa. Não foi tocado.

### 2.6 Numeração e cor oscilam

Três leituras diferentes no mesmo dia, com os mesmos dois controles. É a
`DUAS-CONTABILIDADES-01`, e depende da decisão 19 dela.

### 2.7 O método

O defeito mais caro da lista, e é meu. Ver a seção 4.

### 2.8 A tela mostra o que não confere

"Controle 2 — P1" ao lado de "Controle 1 — P2"; o seletor dizendo DualSense
enquanto o journal registrava `gamepad_emulation_started flavor=xbox`.

---

## 3. O defeito que a verificação achou e que era MEU, ativo

**DEPOIS-QUE-APLICAVA-AGORA-01.** O botão *"Aplicar na próxima abertura"*
chamava `aplicar()` **incondicionalmente**.

Meu raciocínio, escrito no código: *"a marca dela mora no disco, então escrever é
o certo"*. Isso vale para a caixinha do Steam Input, cuja aplicação **é** a
escrita. **Não vale para a máscara:** ali `aplicar()` chama
`gamepad.emulation.set`, que **recria o vpad ao vivo** — exatamente o dano que o
diálogo existe para evitar.

Ou seja: na máscara, *"aplicar depois"* fazia a mesma coisa que *"aplicar agora"*
— **sem fechar o jogo**, e portanto deixando o jogo e a máquina em desacordo. É
provável que seja a causa do *"1 jogador saiu"* que ela viu logo após clicar.

**Ação tomada: CURADO.** Agora só aplica o que é escrita; o que recria
dispositivo não é aplicado, e o toast **diz isso**:

> *"Não mudei nada agora — isto só vale quando o jogo abre. Refaça a escolha
> depois de fechar Sackboy."*

Dizer "guardado" ali seria a mentira mais cara possível: ela terminaria a partida
confiando, e a mudança não estaria lá.

---

## 4. O método, que é o defeito 7 e o mais caro

**O padrão do meu erro hoje, medido no próprio git log:**

1. curar sem medir o efeito colateral — **três vezes**, e as três quebraram algo
   que funcionava;
2. mandá-la testar com o daemon **mais velho que a cura** (o install é editable);
3. curar **um lado** de uma assimetria e não o outro — duas vezes;
4. ligar uma cura no gesto errado por não ter conferido **qual botão ela usa**.

**A regra que teria evitado a maioria, e que passa a valer:**

> Antes de aplicar qualquer cura na máquina dela, um cético independente responde
> **"o que esta cura quebra?"** — e a cura só sai se a resposta for "nada" com
> caminho:linha.

Foi exatamente o que esta fila fez, e o saldo é: **oito curas ruins não chegaram
nela.** O custo de descobrir isso foi de agentes; o custo de não descobrir teria
sido a partida dela, de novo.

---

## 5. O que fica ABERTO, e o que ela precisa saber

**Nenhum dos oito está curado.** Duas coisas foram feitas, e as duas são de
higiene, não de entrega:

- a ligação errada do diálogo no `on_profile_save` foi **revertida** (2.1);
- o *"aplicar depois"* deixou de aplicar ao vivo o que recria dispositivo (3).

**O que trava o resto:** a cura do 2.2 exige resolver *"quem é o dono do valor"*
entre a janela e o daemon, e isso é decisão de arquitetura — a `AUTO-01.3` já
decidiu que **o daemon é o dono**, e o desenho que ela pediu (acumular e aplicar
no fim) pede o contrário. **Isso precisa dela**, e não de mim.

**A pergunta, pronta:**

> *"Você pediu para passar pelas abas e aplicar no fim. Hoje o daemon é o dono do
> que a tela mostra, e a tela só ecoa — foi assim que a casa curou um defeito
> antigo de dois donos. Para acumular, a janela precisa segurar a sua escolha
> contra o daemon até você clicar. Vale abrir essa exceção, ou prefere que só a
> máscara pergunte na hora, como está?"*

## 6. Nota de honestidade

Este arquivo registra **fracasso de desenho**, não progresso. As oito curas foram
escritas, verificadas e descartadas antes de tocarem a máquina dela. O que sobrou
foi uma reversão e uma correção de defeito meu.

**E o que ela pediu — terminar os testes A, B e C — continua bloqueado**, porque
os defeitos abertos contaminam a medição: com o "1 jogador saiu" falso e a
numeração oscilando, ela não consegue reportar o que vê com confiança. Curar o
que contamina medição vem antes de retomar os testes, e isso está dito porque é a
única coisa desta fila com ordem clara.
