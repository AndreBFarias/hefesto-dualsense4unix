# CONFIG-07 — a janela

**Depende de:** CONFIG-01. Independente das outras — pode correr em paralelo.

## O que entrega

Seção 5: ajustes do programa, não dos controles.

| Ajuste | Estado hoje |
|---|---|
| Tamanho do texto | **Backend pronto, escala 0-8, sem tela.** É ligar fio, não construir |
| Ícone na barra do sistema | Existe; falta dizer o que fazer quando não aparece |
| Ambiente da área de trabalho | Lido de `XDG_CURRENT_DESKTOP`, exibido, corrigível |
| Ligar junto com o computador | Já existe na aba Sistema — **aqui só espelha, com link** |

## O aceite COSMIC / GNOME

É esta sprint que carrega o requisito dos dois ambientes.

O ícone da bandeja usa AppIndicator, tentando `AyatanaAppIndicator3` e depois
`AppIndicator3` (`integrations/tray.py:50-61`). No COSMIC aparece sozinho. No
GNOME moderno depende de extensão instalada.

**A regra:** o ambiente detectado informa a **mensagem de ajuda**, nunca o
comportamento. `XDG_CURRENT_DESKTOP` pode vir vazia ou composta (`pop:GNOME`), e
a aba precisa abrir igual nos três casos.

Quando a bandeja não sobe no GNOME, a aba diz o que falta instalar — em vez de o
ícone sumir calado, que é o que acontece hoje.

**Aceite:** as capturas saem iguais em COSMIC e em GNOME; a aba abre com
`XDG_CURRENT_DESKTOP` vazia; e num GNOME sem a extensão, a seção mostra a
instrução em vez de um estado mudo.
