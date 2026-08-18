# O ESTADO DA NOITE — o que ela achou com o controle na mão

- **Escrito em:** 10/08/2026, madrugada, na branch `restauro/inicio-da-sessao`
- **O que este arquivo é:** o **ponto de retomada**. A sessão de 09→10/08 foi longa
  demais para caber numa conversa; isto é o que precisa sobreviver a ela
- **Grau:** tudo MEDIDO salvo onde diz o contrário

---

## 1. A frase da noite

**Ela achou quatro defeitos que nove agentes não acharam — ligando o controle e
usando.** Nenhum apareceu em auditoria de código:

| o que ela achou | o que era |
|---|---|
| o touchpad não move o cursor | regra nossa (`76-*.rules`), um curinga que apagava o touchpad em **todos** os modos |
| "o botão emular teclado não funciona" | o motor funciona; **nenhum atalho de fábrica digita letra**, e o único caminho para texto (L3 → teclado na tela) depende de um programa que o produto **não instala** |
| cliquei em "Controlar o PC" e nada | o modo entra e **restaura** a preferência de mouse — que estava desligada. A tela não dizia |
| a caixinha do Steam Input sumiu | o perfil dela do Pragmata tem `process_name` junto do `window_class`, e `_detect_steam_appid` (`profiles/simple_match.py:198`) exige **só** a classe — o editor abre como "Vale sempre" e a caixinha, que só existe em "Jogo da Steam", some |

**A regra que isto reforça:** a observação dela é fonte primária. Nesta sessão ela
derrubou **quatro hipóteses minhas** (a caixinha como causa do rumble, o
dongle/porta USB, a máscara, e a mistura entre rumble e controle duplicado).

---

## 2. O que ENTROU e está commitado (`7a0a655` e antes)

| cura | prova |
|---|---|
| **touchpad e giroscópio ganham acesso (OQ-6)** | ACL medida antes/depois no disco dela; pegou sem replug |
| **o aviso falso do co-op** | conta controle FÍSICO, não vpad; contrapeso travado nos dois lados |
| **o "Modo jogo" guarda em catch-all** | o gate do daemon já existia desde 05/08 — a janela recusava por 4 dias sem saber |
| **volume, mudo e canal do alto-falante chegam ao perfil** | a função tinha **zero chamadores** desde 01/08 |
| **o diálogo deixa de depender de qual aba está à vista** | defeito meu, horas depois de eu entregar a cura que ele furava |
| **o AGORA deixa de ser refém do DEPOIS** | quatro buracos meus no "Aplicar" |
| **doctor detecta controle abortado no probe** | distingue órfão AGORA de aborto já recuperado |
| **backoff do retry cavalga os 3 s do BlueZ** | eram 100 ms — 30x pequeno demais |
| **as telas param de mentir** | "Cor **enviada**", e o rumble fala no zero |

---

## 3. O que está na árvore, NÃO commitado (10/08, madrugada)

Tudo com teste que morde e suíte verde (**8351**, oito portões em zero).

1. **O touchpad volta a ser touchpad do sistema, em todos os modos.** A regra
   deixou de ser curinga: só o **vpad** fica fora do libinput (era ele quem
   duplicava o toque); o físico é liberado, e o `TouchpadReader` se cala quando o
   sistema é o ponteiro. **VALIDADO POR ELA**: funciona no desktop e no jogo, sem
   dobrar.
   - **Preço aceito por ela:** as três regiões do touchpad **saíram** da aba de
     teclas (o clique já é clique de mouse; somar tecla faria um clique apagar
     texto). Reverter é a mesma decisão do outro lado — está escrito no código.
2. **Aba nova "No jogo"** — responde *"o jogo está recebendo?"* com uma linha por
   recurso, na mesma ordem, sempre. Distingue "no jogo agora" / "parou" / "sem
   pedido ainda" / "a máscara Xbox não tem giroscópio" / "não há vpad neste modo".
3. **"Controlar o PC" passa a dizer** quando entra com mouse ou teclado
   desligados, e onde ligar. (Curou junto uma frase que citava abas que não
   existem desde 28/07.)
4. **A aba de teclas passa a dizer o que NÃO digita** — os onze botões sem tecla
   eram **escondidos**, e a lista parecia completa.
5. **A vibração ganhou instrumento**: anel dos últimos 8 pedidos crus, com bytes,
   ramo e idade. E **um defeito real na máscara Xbox**: o backend uinput nunca
   teve os contadores, então a aba dizia *"o jogo pediu força zero"* com a
   vibração funcionando — um modo inteiro era impossível de medir.
6. **A bateria do controle chega ao jogo** (era fixa: "5% descarregando para
   sempre"), e **o som do jogo aparece no card** (nome escolhido por ela: *"som do
   controle"*).
7. **17 sprints remarcadas** com o rótulo `ENTREGUE EM CÓDIGO — AGUARDANDO A
   PALAVRA DELA`, cada uma com uma linha do que ela precisa validar.

---

## 4. O que está RODANDO (agentes, 10/08 ~01h)

- **o teclado na tela entra no install, sem flag** — hoje o produto promete L3 e
  `grep -c onboard install.sh` devolve **0**. Inclui escolher entre `onboard` (X11)
  e `wvkbd` (Wayland nativo — a máquina dela é COSMIC);
- **a caixinha que sumiu** — `_detect_steam_appid` e o round-trip do editor.

---

## 5. O QUE ESPERA A PALAVRA DELA

1. **as fotos das abas** — `retratar_abas.py` não foi rodado com a aba nova; o
   `CLAUDE.md` cobra as imagens antes de release;
2. **o nome da aba nova** ("No jogo"), e "giroscópio" vs. "movimento";
3. **a migração automática de máscara nos presets** (`profiles/loader.py:188`) —
   quatro perfis dela estão em `xbox` por uma migração de 25/07 cuja premissa
   ("a DualSense faz o jogo ignorar o vpad") está **medida como falsa hoje**: o
   jogo pede vibração ao vpad na máscara DualSense. Ela decidiu trocar os quatro,
   **e eu parei** ao descobrir que a migração os traria de volta. **Aberto.**

---

## 6. O QUE CONTINUA ABERTO, medido

- **a vibração** — o jogo pede e chega zerado. **Sem causa provada.** O que caiu:
  regressão nossa (não houve commit na janela), o wrapper (medido), a máscara, a
  caixinha, o dongle. O instrumento novo (o anel) é o que fecha isso na próxima
  sessão de jogo;
- **o Pragmata duplicado** — a marca está no arquivo e a exceção **não armou**
  (`excecao_ativa: False` com o jogo aberto). São possivelmente **duas** coisas: o
  perfil não reconhecido (§1) e a exceção não disparando;
- **com o DualSense desconectado, o jogador 2 do co-op fica sem input** — o laço
  que alimenta os vpads só roda se o físico responder (`daemon/lifecycle.py:3696`).
  **Sem dono**;
- **`install.sh:941`** — `exit 0` quando o formato não é `native`: doze passos de
  cura ficam de fora de flatpak/appimage/deb;
- **as onze funções sem chamador** de 25/07 continuam sem chamador (medido em
  09/08, quinze dias depois).

---

## 7. Regras dela, fixadas nesta sessão

- *"a vontade na GUI prevalece sempre"* — o produto não decide no lugar dela;
- *"tudo tem que focar em funcionar na interface do app e no install"* — cura que
  só existe em código, ou só por terminal, **não é entrega**;
- *"deve ser universal"* — cabo e Bluetooth, N controles, e os externos;
- *"o rumble tem que funcionar em todos os modos"* — e aí a máscara volta a ser
  escolha dela, não contorno.

---

## 8. Nota de método

**Três vezes nesta sessão a casa já sabia e o produto não fazia**: a causa do
controle abortado estava escrita desde 25/07; o gate do "Modo jogo" existia desde
05/08; o acesso aos nós de entrada tinha nome (OQ-6) desde 07/08.

E **duas vezes o instrumento mentiu**: uma "prova de ausência" convincente e falsa
(o `grep` procurou nos arquivos errados), e a leitura de `plays: 4` como *"o jogo
pediu e veio zero"* — o contador não sabe **quem** escreveu, e o driver do kernel
também escreve ali.
