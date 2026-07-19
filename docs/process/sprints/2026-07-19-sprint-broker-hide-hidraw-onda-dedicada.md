# Sprint BROKER hide-hidraw — onda dedicada (parkada de 2026-07-19)

> O broker foi IMPLEMENTADO na leva de 2026-07-19 e PARKADO após a auditoria adversarial achar 9
> HIGH — a maioria da colisão broker×motion e da robustez de restore. Código de referência preservado
> em `docs/process/future-broker/`. Spec base: `docs/process/estudos/2026-07-18-estudo-broker-hide-hidraw.md`.
> Esta sprint incorpora as LIÇÕES da auditoria — resolva-as no DESENHO, não com remendo.

## Por que parkou (não é código ruim — é desenho que precisa da própria onda)
O broker esconde o hidraw do físico com `chmod 0600 root` + remoção de ACL. Mas o **motion reader
é o daemon rodando como a usuária** e precisa REABRIR esse mesmo hidraw — DAC não distingue daemon de
jogo (mesmo uid). Resultado: com o broker ativo, todo reopen do motion (retarget, silence-reopen 1s,
wake BT) falha com EACCES e o gyro morre no meio do jogo. Fora isso, a auditoria achou robustez
insuficiente no restore (orfaniza nó, idempotência deixa nó recriado exposto, lease derruba tudo em
qualquer timeout). Nada disso é aceitável num serviço ROOT na máquina de produção.

## LIÇÕES da auditoria (requisitos de desenho desta onda)
1. **fd-injection, não reopen-por-caminho**: o daemon abre o fd do físico ENQUANTO o nó está visível
   (antes do hide) e ENTREGA o fd ao motion reader; o reader NUNCA reabre por caminho enquanto
   escondido (o fd sobrevive à remoção de ACL — é a premissa do design). No retarget/hotplug: o nó
   novo nasce visível → daemon abre fd(s) (backend + reader) → SÓ ENTÃO hide. Unifica broker×motion.
   (Achados #1/#6/#8/#12/#13 desaparecem por construção.)
2. **restore idempotente e à prova de falha** (#2/#5/#9/#15): só destrackear o nó DEPOIS do restore de
   fs ter sucesso; retry no restore; hide de nó já rastreado por conexão DEVE re-aplicar o fs (nó
   recriado com o mesmo hidrawN nasce exposto — idempotência por-conexão que não toca o fs deixa
   exposto enquanto o broker jura escondido).
3. **lease resiliente** (#4/#18): OSError/timeout no cliente NÃO pode derrubar a lease inteira
   (restaura TODOS os nós); reconectar preservando o conjunto escondido; criação da lease sob lock
   (corrida faz a lease perdedora ser GC'd e desfazer hides).
4. **socket sobrevive a restart** (#10): NÃO usar `RuntimeDirectory=` que apaga o broker.sock em todo
   stop/crash — socket-activation cria o socket; o serviço não deve removê-lo.
5. **minor-reuse** (#11): revalidar major:minor entre validar→chmod e no restore de nome stale (o nó
   pode ter sido reciclado para outro device).
6. **install/uninstall/packaging seguros** (#16/#17/#19/#21): ALLOWED_UID nunca renderiza 0 (root);
   gate do rehide por VIDA do vpad (não existência do objeto); falha do start pós-stop não deixa
   físico escondido sem vpad (= ZERO controles); instalação por PACOTE precisa de caminho de
   remoção do serviço root (purge não pode deixar unit root órfã habilitada). Uninstall dispara
   restore-all ANTES de remover.

## Escopo (quando executar)
Reimplementar o broker com fd-injection do daemon como espinha dorsal, os 6 grupos de lição acima, e
o validador por HID_ID + ACL-via-setxattr (byte-validado — ISSO a implementação parkada acertou, ver
`docs/process/future-broker/`). Auditoria adversarial de novo antes de instalar. Prioridade: é
defesa-em-profundidade (o wrapper já cobre o duplicado dos jogos lançados pelo hefesto), então roda
DEPOIS que o gyro + as ondas atuais estiverem validadas ao vivo e commitadas.

## O que a implementação parkada JÁ ACERTOU (aproveitar)
- Validador por HID_ID zero-preenchido do pai HID (aceita 0003/0005:054C:0CE6, rejeita vpad 0DF2,
  Nintendo, symlink, traversal) — validado ao vivo.
- ACL via `os.setxattr` no `system.posix_acl_access` (header versão 2 + entradas), byte-idêntico ao
  que o `setfacl` produz — mantém o SystemCallFilter da unit sem `execve`. Validado contra blob real.
- Units systemd com hardening completo. Protocolo JSON-por-linha + SO_PEERCRED.
