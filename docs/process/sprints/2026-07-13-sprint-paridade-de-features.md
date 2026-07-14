# Sprint FEAT-PARITY-REVIEW-01 — o que mais seguramos e esquecemos de devolver?

Pedido da mantenedora (2026-07-13, durante gameplay ao vivo do Sackboy): "se
desativamos a vibração e afins, fico pensando o que mais não devemos ter
desativado anteriormente — precisamos de uma sprint de revisão de features para
encontrar problemas como esses".

Contexto: dois bugs da mesma família foram flagrados AO VIVO no mesmo dia:

1. BUG (nativo): o keepalive do report_thread pisoteava o rumble que o JOGO
   escrevia no hidraw — rumble morto no Modo Nativo (corrigido:
   FEAT-NATIVE-OUTPUT-MUTE-01).
2. BUG (vpad): o gamepad virtual não anunciava force-feedback — jogos nunca
   vibravam o DualSense no modo "Jogar pelo Hefesto"
   (corrigido: FEAT-VPAD-FF-PASSTHROUGH-01).

O padrão-raiz: o Hefesto se coloca ENTRE o jogo e o controle e, para cada
capacidade do DualSense, precisa decidir explicitamente — encaminhar, emular ou
ceder. Capacidade sem decisão explícita = capacidade silenciosamente MORTA.

## Método

Auditar a MATRIZ capacidade × modo × direção, exigindo para cada célula um
veredito com evidência (file:line ou teste ao vivo): FUNCIONA / DEGRADADO /
MORTO / N-A (com justificativa).

Modos: desktop (Controlar o PC) · vpad (Jogar pelo Hefesto, P1 e co-op P2..PN)
· nativo (Jogar direto).
Direções: jogo→controle (output) e controle→jogo (input).

## Matriz de capacidades a auditar

| Capacidade | desktop | vpad P1 | vpad co-op PN | nativo |
|---|---|---|---|---|
| Botões/sticks/gatilhos (input) | mouse/teclado |  (validado) |  (validado) |  |
| Rumble (jogo→controle) | N/A | FF passthrough (novo — validar ao vivo) | FF por player (novo — validar) | mute de output (novo — validar) |
| Gatilhos adaptativos (jogo→controle) | N/A | ? IMPOSSÍVEL via uinput — documentar como limitação + orientar nativo | idem |  (raison d'être) |
| Lightbar (jogo→controle) | perfil | ? jogo seta lightbar via SDL no vpad? (uinput não expõe LED — provavelmente MORTO; decidir: aceitável?) | idem |  com mute (validar cor do jogo) |
| Player LED (jogo→controle) | perfil | ? (nosso, por jogador — ok) |  novo |  com mute |
| Giroscópio/acelerômetro (controle→jogo) | N/A | ? Motion Sensors ficam no device físico; vpad NÃO os expõe — jogos com aim-gyro no vpad = MORTO? A regra 78 tirou-os da enumeração de joystick (SDL ainda os acha por udev?) | idem |  direto |
| Touchpad (controle→jogo) | vira mouse (nosso) | ? vpad não expõe touchpad — jogos Sony esperam | idem |  direto (mas o TouchpadReader NOSSO segue lendo? conflita?) |
| Microfone/áudio do controle | quirk anti-storm | idem | idem | ? áudio USB segue utilizável no nativo? |
| Bateria (controle→jogo/SDL) | GUI ok | ? vpad não reporta bateria (SDL mostra unknown) — aceitável? documentar | idem |  |
| Botão PS/mute (controle→sistema) | hotkeys nossos | ? suprimido? Steam abre overlay em cima do vpad? | idem | ? PS vai pro jogo — hotkeys nossos mortos no nativo (esperado? documentar) |
| Headset jack | passa | passa | passa | passa |

Células "?" = investigar. Para cada MORTO encontrado: classificar
(bug corrigível / limitação de uinput a documentar / decisão de produto).

## Entregáveis

1. Relatório da matriz preenchida com evidências (agentes de leitura + testes
   ao vivo com jogo — Sackboy para Sony-features, um jogo SDL genérico para
   gyro/lightbar).
2. Fixes para os corrigíveis (mesmo padrão FF/mute desta noite).
3. Seção "Limitações por modo" no README (honestidade com quem usa: o que só
   funciona no nativo — gatilhos adaptativos, gyro, touchpad — e por quê).
4. Testes de regressão por célula corrigida.

## Status

- [ ] Agendada — executar após o release v3.12.0 (rumble validado ao vivo).
- [x] Rumble vpad/nativo: corrigidos nesta mesma noite (ver CHANGELOG).
