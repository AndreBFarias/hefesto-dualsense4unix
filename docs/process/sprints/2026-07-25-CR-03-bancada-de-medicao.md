# CR-03 — A bancada: criar efeito sentindo o controle na mão

**Status:** ABERTA
**Depende de:** CR-02
**Bloqueia:** CR-04
**Processo:** [CLEAN-ROOM.md](../CLEAN-ROOM.md)

## Objetivo

Uma tela onde se mexe nos valores, aperta o gatilho, sente, ajusta e salva com
um nome. O efeito nasce **medido pela pessoa**, já no formato com proveniência
da CR-02.

## Por que isto é o coração do processo

A regra R1 diz que o ponto de partida legítimo é o hardware, não o arquivo de
terceiro. Uma bancada boa torna o caminho legítimo o mais **fácil** — e é assim
que processo de sala limpa sobrevive ao cansaço. Se medir for penoso e copiar
for cômodo, o processo falha na primeira noite ruim.

## Entregas

- [ ] **Bancada na aba Gatilhos** — os sete parâmetros do efeito ao vivo,
      aplicando no controle a cada ajuste, sem passo de "aplicar".
- [ ] **Leitura do gatilho na mesma tela** — a barra analógica de L2/R2 (que já
      existe na aba Status) ao lado dos controles, para ver a resposta enquanto
      se aperta. Sentir e medir no mesmo lugar.
- [ ] **Salvar como efeito próprio** — pede nome (validado pela guarda da CR-02)
      e a nota do que se sentiu; preenche `medido_por`, `medido_em` e `controle`
      sozinho, a partir do controle selecionado.
- [ ] **Aplicar em qualquer um dos controles conectados**, não só no primário:
      a sensação muda entre aparelhos, e a proveniência registra em qual foi.
- [ ] **Comparar A/B** — alternar entre dois conjuntos de valores sem perder o
      que já foi ajustado. Sem isso, calibrar por sensação vira adivinhação.

## Restrições

- A bancada escreve **direto no hardware** enquanto está aberta. Precisa ceder
  o controle de volta ao daemon ao sair, pelo mesmo caminho que a aba Rumble já
  usa para o teste de motores — o projeto já tem a cicatriz de escritor sem dono
  e não vai criar mais um.
- Com quatro controles conectados, a tela precisa deixar **evidente** em qual
  está aplicando. Ambiguidade aqui contamina a proveniência.

## Critério de conclusão

Uma pessoa consegue, sem sair da janela: escolher um controle, mexer até gostar,
nomear, salvar — e o efeito aparece em `curvas-proprias.md` com data e autoria,
sem que ela tenha escrito nada à mão.
